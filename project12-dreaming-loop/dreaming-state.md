# Dreaming Loop — State

The spine for Project 12's improvement loop. It watches
`project8-full-loop-capstone/audit-progress.md` (the dependency-audit
loop's own spine), never the raw run transcripts. Every run reads
`## Last checked` first, so it never re-scans entries it has already
considered; it writes a new `## Last checked` date and a `## Runs`
entry last, whether or not it found anything.

## Last checked

2026-08-26

## Runs

- 2026-08-26: Checked `audit-progress.md` entries dated after 2026-08-01
  (2026-08-05, -12, -19, -26 — all four entries in the window). Found
  two things:
  1. A repeated failure: step 5 (post report) was blocked by "gh not
     authenticated" in all four entries, but the escalation language
     was inconsistent — 08-12 said "same fix needed as last week" and
     08-19 said "third week in a row," yet 08-26 reported the block as
     if it were fresh, with no count.
  2. A dead rule: step 2's "check for legacy `requirements-dev.txt`"
     sub-bullet was exercised in all four entries and found the file
     absent every single time (08-26: "this repo has never had one").
  Drafted the smallest fix for both in an isolated worktree
  (`../loop-eng-worktrees/wt-dreaming-gh-auth-escalation`) on branch
  `claude/dreaming-loop-gh-auth-escalation`, commit `4836887`, against
  `project8-full-loop-capstone/.claude/skills/dependency-audit/SKILL.md`.
  Could not open the PR: `gh` is not authenticated in this environment
  and no GitHub remote is configured (`gh auth status` and `git remote
  -v` both confirm this) — the same blocker this fix is about. A human
  needs to set up `gh auth login`/`GH_TOKEN` and a remote, then push
  branch `claude/dreaming-loop-gh-auth-escalation` and open the PR
  against `main` (commit `4836887` has the full diff and rationale).

