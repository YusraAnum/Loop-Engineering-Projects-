# Project 12 — The Dreaming Loop (Final Capstone)

_Uses: Concept 12 (spine and improvement loop), Concept 11
(maker-checker), Concept 6 (schedule), Part 5 (human gate)_

This loop doesn't do a chore. It watches **Project 8's** dependency-audit
loop and its spine (`project8-full-loop-capstone/audit-progress.md`),
looks for anything that repeats, and proposes the smallest fix to
Project 8's skill — as a PR on a `claude/` branch, never a direct commit.

## Where everything lives

```
../.github/workflows/dreaming-loop.yml        ← heartbeat (weekly cron)
.claude/skills/dreaming-loop/SKILL.md         ← the loop's body
dreaming-state.md                             ← this loop's own spine
```

Same reason as every prior GitHub-Actions project: the workflow file
must live at the repo root.

## The four concepts

| Concept | Where |
|---|---|
| **Spine + improvement loop (12)** | `dreaming-state.md` tracks `## Last checked` so no run re-analyzes old entries; `audit-progress.md` is the thing being watched, never edited by this loop. |
| **Maker-checker (11)** | Skill step 4 drafts the fix in an isolated worktree; step 5 has the same run re-read its own diff before proposing anything, and explicitly permits "found nothing, propose nothing." |
| **Schedule (6)** | `dreaming-loop.yml`'s `cron: "0 10 * * 1"` — weekly, `workflow_dispatch` for manual testing. |
| **Human gate (Part 5)** | Step 6: open a PR, cite evidence, never merge. The hard rule at the top of the skill: never commit to `main`. |

## The planted repeated failure

Project 8's `audit-progress.md` didn't yet have a week's worth of
history, so — per the assignment's own instruction ("a deliberately
planted repeated failure in the logs... add one by hand") — I added 3
backdated entries (2026-08-05, -12, -19) alongside the real 2026-08-26
entry, all genuinely blocked at the same step for the same reason: `gh`
not authenticated (the actual, ongoing GitHub-App access issue this
session has hit all day across Projects 6, 8, 9, 10, and 11 — not a
fabricated scenario). `dreaming-state.md`'s `## Last checked` was set
to 2026-08-01, before all four, so the first real run would see the
whole pattern.

## What the rehearsal actually found

Ran the real beat locally (`claude -p`, same proven method as Project
8), cost **$0.49**, 27 turns. It did **not** just say "gh auth is
broken, fix that" — it found two distinct things in the same window
(entries dated 2026-08-05, -12, -19, -26, all after the spine's
`## Last checked` date of 2026-08-01):

1. **A repeated failure.** Step 5 (post report) was blocked by the
   same "gh not authenticated" cause in all four entries, but the
   escalation language was inconsistent — 08-12 said "same fix needed
   as last week," 08-19 said "third week in a row," yet 08-26 reported
   the block as if it were fresh, with no count at all. It correctly
   recognized that "gh isn't authenticated" itself isn't something a
   skill-level rule can fix — that's an environment problem, out of
   scope — but *how consistently the skill reports a repeating block*
   is exactly in scope.
2. **A dead rule.** Step 2's "check for legacy `requirements-dev.txt`"
   sub-bullet was exercised in all four entries and found the file
   absent every single time (08-26 even notes "this repo has never had
   one"). No entry in the window ever needed it, so it proposed
   removing it.

Both were drafted as a single smallest-fix commit, in an isolated
worktree, on branch `claude/dreaming-loop-gh-auth-escalation`, commit
`4836887`:

```diff
-- Also check for a legacy `requirements-dev.txt` at the repo root (from
-  before this repo consolidated to a single `requirements.txt`) and
-  audit it the same way if present.

+If this step is blocked by the same cause as a prior run (e.g. `gh`
+still not authenticated), check `## Open / needs a human` for prior
+consecutive entries citing that same cause, and always state the count
+explicitly (e.g. "Nth week in a row blocked by the same issue") — do
+not let this escalation language depend on whether it happens to feel
+notable that week.
```

It could not open an actual PR (this repo has no GitHub remote yet,
same open item as every other GitHub-Actions project here) — it said
so plainly in the spine entry instead of pretending otherwise.

## Verified: the three "Done when" conditions

1. **Traces to real, cited log entries, not a guess** — both fixes
   cite the exact dated entries they came from; verify yourself:
   `git show 4836887 -- project8-full-loop-capstone/.claude/skills/dependency-audit/SKILL.md`
   in `../loop-eng-worktrees/wt-dreaming-gh-auth-escalation`.
2. **The planted repeated failure got caught and turned into a
   proposal** — yes, see above.
3. **Nothing changed in the rules file without a merge** —
   confirmed: `project8-full-loop-capstone/.claude/skills/dependency-audit/SKILL.md`
   on `main` still has the old `requirements-dev.txt` bullet and no
   escalation language. The fix exists only on the isolated branch.

## What's still open

- Same GitHub remote/App-access prerequisite as Projects 6, 8, 9, 10,
  11 — once fixed, a real scheduled run can actually open the PR
  instead of stopping short and logging why.
- The draft branch/worktree above is the pending "PR" — review
  `4420e8f`'s diff and merge it (or don't) once there's a remote to
  open it against.
