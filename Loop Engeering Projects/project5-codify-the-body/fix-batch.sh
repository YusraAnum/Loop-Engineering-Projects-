#!/bin/bash
# fix-batch.sh — fan out N bug-fix issues, one maker per issue in its own
# isolated git worktree (Concept 8), then one independent reviewer per
# issue, using a capped background loop (Concept 5) instead of Claude
# Code's dynamic-workflows engine. This is the "lower-level parts you
# already know" version: this shell script IS the workflow, `claude -p`
# is each agent, and the reviewer's PASS/FAIL text is the checker.
#
# Usage:
#   ./fix-batch.sh <issues-file>
# where <issues-file> has one issue per non-empty line.
#
# Nothing here is specific to one run's issues or leftover from a
# previous run — every invocation gets a fresh timestamped worktree
# parent directory and its own branches, so re-running with a different
# issues file fixes a different batch without touching any prior run.

set -uo pipefail

ISSUES_FILE="${1:?usage: ./fix-batch.sh <issues-file>}"
MAX_CONCURRENT=16   # Concept 5's capped loop: never run unboundedly many at once

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
BASE_COMMIT="$(git rev-parse HEAD)"
RUN_ID="$(date +%Y%m%d-%H%M%S)"
WT_PARENT="$(cd "$REPO_ROOT/.." && pwd)/fix-batch-runs/run-$RUN_ID"
mkdir -p "$WT_PARENT"

mapfile -t ISSUES < <(grep -v '^[[:space:]]*$' "$ISSUES_FILE")
if [ "${#ISSUES[@]}" -eq 0 ]; then
  echo "No issues found in $ISSUES_FILE" >&2
  exit 1
fi

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g' | cut -c1-40
}

SLUGS=()
for issue in "${ISSUES[@]}"; do
  SLUGS+=("$(slugify "$issue")")
done
# De-duplicate slugs within this run (append index if two issues slugify the same)
for i in "${!SLUGS[@]}"; do
  for j in "${!SLUGS[@]}"; do
    if [ "$i" -lt "$j" ] && [ "${SLUGS[$i]}" = "${SLUGS[$j]}" ]; then
      SLUGS[$j]="${SLUGS[$j]}-$j"
    fi
  done
done

echo "== fix-batch run $RUN_ID =="
echo "== base commit: $BASE_COMMIT =="
echo "== ${#ISSUES[@]} issue(s), worktrees under: $WT_PARENT =="
echo

# --- Draft: one maker per issue, each in its own isolated worktree ---
running=0
for idx in "${!ISSUES[@]}"; do
  issue="${ISSUES[$idx]}"
  slug="${SLUGS[$idx]}"
  wt="$WT_PARENT/wt-$slug"
  branch="fix/$RUN_ID-$slug"

  (
    git worktree add -q -b "$branch" "$wt" "$BASE_COMMIT" 2>"$WT_PARENT/wt-$slug.worktree-add.log"
    cd "$wt" || exit 1
    claude -p "You are the maker in a maker-checker bug-fix flow. You are working in an isolated git worktree that is entirely yours — do not touch anything outside it, and never merge, push, or interact with any other branch or worktree.

Fix ONLY this one issue: $issue

Follow this shape: reproduce the bug first and show the actual failing output; locate its exact cause; draft the smallest possible fix (no unrelated refactoring); add or update a regression test that fails before your fix and passes after it; run the affected test suite (or, if none exists for the touched file, the smallest manual repro) and confirm it passes; then commit your change on this branch with a clear commit message. End your reply with a short summary of what you changed and why." \
      --permission-mode bypassPermissions \
      --output-format text \
      > "$wt.maker.log" 2>&1
    echo "[$slug] maker finished (exit $?)"
  ) &

  running=$((running + 1))
  if [ "$running" -ge "$MAX_CONCURRENT" ]; then
    wait -n
    running=$((running - 1))
  fi
done
wait   # do not start grading until every maker has finished

echo
echo "== all makers finished =="
echo

# --- Grade: one independent reviewer per issue, no cross-talk ---
for idx in "${!ISSUES[@]}"; do
  issue="${ISSUES[$idx]}"
  slug="${SLUGS[$idx]}"
  wt="$WT_PARENT/wt-$slug"
  branch="fix/$RUN_ID-$slug"

  (
    cd "$wt" || exit 1
    claude -p "You are an independent reviewer in a maker-checker bug-fix flow. You know nothing about any other issue, worktree, or reviewer in this batch — judge only this one, and do not let anything about 'a batch' influence your verdict.

Review the diff on the current branch ($branch) against base commit $BASE_COMMIT for this claimed fix: $issue

Read the actual diff (git diff $BASE_COMMIT..$branch), read the touched files' current state, run the affected test suite yourself (or the smallest manual repro if there's no test suite) and read the real output, confirm there is a regression test or repro that would genuinely fail before this fix and pass after it, and check for unrelated changes or scope creep. Reply with exactly PASS or FAIL on the first line, followed by concrete bullet reasons citing what you actually ran or read — never a vague 'looks fine'. No other text." \
      --permission-mode bypassPermissions \
      --output-format text \
      > "$wt.review.log" 2>&1
  ) &
done
wait

# --- Report per issue, not a combined judgment ---
echo
echo "================ VERDICTS (run $RUN_ID) ================"
for idx in "${!ISSUES[@]}"; do
  issue="${ISSUES[$idx]}"
  slug="${SLUGS[$idx]}"
  wt="$WT_PARENT/wt-$slug"
  branch="fix/$RUN_ID-$slug"
  echo
  echo "--- Issue $((idx + 1)): $issue"
  echo "    branch:   $branch"
  echo "    worktree: $wt"
  echo "    verdict:"
  sed 's/^/      /' "$wt.review.log"
done
echo
echo "=========================================================="
echo "Nothing merged automatically. Branches and worktrees above are"
echo "left in place for inspection; merge or 'git worktree remove' each"
echo "one yourself once you've read its verdict."
