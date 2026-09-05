---
name: dreaming-loop
description: Weekly improvement loop that reads project8-full-loop-capstone/audit-progress.md since its own last check, finds any failure or correction that repeats, and drafts the smallest rules/skill fix as a PR on a claude/ branch — never a direct commit. Use when asked to run the scheduled dreaming loop.
---

# Dreaming Loop

This loop does not do the chore. It watches the loop that does
(Project 8's dependency audit) and proposes improvements to *how* it
runs — never applying anything itself.

## Hard rule, never bend this

**Never commit directly to `main`. Every proposed change is a PR on a
`claude/*` branch, described with cited evidence, for a human to merge
or reject.** An improvement loop that guesses is worse than none, so
every claim in the PR description must name the specific dated log
entries it's based on — never a plausible-sounding generalization.

## 1. Read the spine first

Read `project12-dreaming-loop/dreaming-state.md`. Note the date under
`## Last checked` — that is your starting point.

## 2. Read what the watched loop actually logged

Read `project8-full-loop-capstone/audit-progress.md` in full. Consider
only entries dated **after** the "Last checked" date from step 1 — do
not re-analyze entries you've already considered in a prior run.

## 3. Look for repetition

Across those entries, find:
- **A failure or correction that appears more than once.** Same root
  cause, same blocked step, same missing thing — even if the wording
  differs slightly between entries.
- **A rule in `.claude/skills/dependency-audit/SKILL.md` that no
  entry in this window ever needed.** Do this check every run, even
  after you've found a repeated failure to fix — finding one issue is
  not a reason to skip looking for the other. Read the skill file
  bullet by bullet, not just step by step: a single sentence buried
  inside a step (e.g. a sub-bullet checking for some specific file or
  condition) counts as "a rule" just as much as a numbered step does.
  For each one, check whether the log entries in this window give
  direct evidence it was exercised and found nothing every single
  time. If so, that is your deletion candidate — cite exactly which
  entries prove it. Only skip proposing a deletion if you genuinely
  find no rule with that kind of direct, repeated "checked and always
  empty" evidence — don't stop looking just because you already found
  something to add.

If nothing repeats and nothing looks unused, say so explicitly in the
spine (step 6) and stop — do not manufacture a finding to seem useful.

## 4. Draft the smallest fix, in an isolated worktree

For a real repeated failure:
1. `git worktree add -b claude/dreaming-loop-<short-slug>
   ../loop-eng-worktrees/wt-dreaming-<short-slug> <base-commit>`
2. In that worktree, edit `.claude/skills/dependency-audit/SKILL.md`
   with the smallest change that would have prevented the repetition —
   not a rewrite, not unrelated cleanup. If a rule looks safe to
   delete per step 3, remove exactly that rule in the same commit.
3. Commit with a message that names the entries this is based on.

## 5. Checker step — verify before proposing

Before opening anything, re-read the diff yourself as if you hadn't
written it: does it actually address the cited entries, and only
those? Does it avoid touching anything the log evidence doesn't
support? If not, revise or drop the change — do not open a
speculative PR.

## 6. Human gate — open a PR, never merge

Open a pull request from the `claude/dreaming-loop-<slug>` branch
against `main` (e.g. `gh pr create`). The PR description must include:
- **Evidence**: the exact dated entries this is based on, quoted.
- **How often**: how many times the pattern repeated, and over what
  span.
- **Why this fix**: why this specific, minimal change stops it.
- Any proposed deletion, with its own evidence.

Never merge it yourself. That decision belongs to whoever reads the
PR.

## 7. Spine — write last, always

Whether or not you found anything, append one entry to
`dreaming-state.md` under `## Runs`: today's date, what window you
checked, what you found (or "nothing repeated"), and the PR link if
one was opened. Then update `## Last checked` to today's date.
