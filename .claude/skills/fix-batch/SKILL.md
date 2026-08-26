---
name: fix-batch
description: Fan out a list of bug-fix issues, one maker per issue in its own isolated git worktree, each graded by an independent reviewer verdict. Use whenever asked to fix a batch/list of issues via the maker-checker flow, instead of doing them one at a time in the main checkout.
---

# Fix Batch

Codifies the body of the maker-checker loop (fix-bug skill + reviewer subagent) as a
single reusable, repeatable run over a *list* of issues, isolated from each other.

## Input

`args` is the issue list for this run: one issue per line, each naming a file/area and
the bug. If `args` is empty, ask the user for the list before doing anything else.

## Steps

1. **Confirm a clean base.** Run `git status` in the repo root. Note the current commit
   — every worktree below branches from it. Do not stash or commit unrelated work
   yourself; just record the baseline.

2. **Fan out makers, one per issue, in parallel** (single message, multiple `Agent`
   calls, `subagent_type: general-purpose`). For issue *i*, give the maker a
   self-contained prompt (it starts with zero context) that includes:
   - The exact issue text.
   - Instruction to run, from the repo root: `git worktree add -b fix/<slug>
     ../<repo-dir>-wt-<slug> <base-commit>` (pick `<slug>` from the issue, kebab-case).
   - Instruction to `cd` into that worktree and follow `.claude/skills/fix-bug/SKILL.md`
     if the touched files fall under a directory that skill covers, otherwise follow the
     same shape inline: reproduce first, locate the exact cause, draft the smallest
     fix, add/update a regression test, run the affected project's test suite (or the
     smallest manual repro if there's no test suite for that file).
   - Instruction to commit the fix in that worktree with a clear message, and to
     **never merge, push, or touch any other worktree or branch**.
   - Instruction to report back: worktree path, branch name, commit hash, and the
     actual test/repro command output (not a summary claim).

3. **Fan out reviewers, one per issue, in parallel and independent of each other**
   (single message, multiple `Agent` calls, `subagent_type: reviewer`). Each reviewer
   gets only its own issue's worktree path and branch name — never let one issue's
   review see another's diff or verdict, and never let a reviewer's verdict be
   influenced by another reviewer's outcome. Ask each to `git diff <base-commit>..
   fix/<slug>` inside that worktree, run the test suite itself, and reply PASS or FAIL
   per its own instructions.

4. **Report per-issue**, not a combined judgment: for each issue, its PASS/FAIL verdict
   verbatim, the branch name, and the worktree path. Do not merge anything yourself —
   that decision belongs to the user, per the fix-bug skill's handoff step. List the
   worktrees so the user (or a follow-up) can inspect, merge, or `git worktree remove`
   each one independently.

5. **Leave worktrees in place** after reporting. Do not clean them up automatically —
   a FAILed fix's worktree is evidence for debugging, and a PASSed one is what the user
   merges from.

## Reusability

This skill takes a fresh issue list every time — nothing here is specific to one run's
issues. Re-invoke it with a different list to fix a different batch; each run creates
its own worktrees/branches and never touches a previous run's.
