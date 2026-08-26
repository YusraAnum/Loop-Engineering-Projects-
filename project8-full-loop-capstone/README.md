# Project 8 — The Full Loop, On Real Work

The chore: a weekly dependency audit of this repo's `requirements.txt`
(currently just `pytest==9.1.1` — the one real, pinned dependency this
codebase has, via `project2-make-tests-pass` and `project3-morning-brief`'s
test suites). Check for outdated versions and known CVEs, draft a
version-bump PR when one is warranted, verify it independently, and post
a weekly report — unattended, for a week, on this actual repo.

## Where everything lives

GitHub Actions only reads workflows from the repo root, so, same as
Project 6:

```
../.github/workflows/dependency-audit.yml   ← the heartbeat + connector
.claude/skills/dependency-audit/SKILL.md    ← the skill (the loop's body)
audit-progress.md                           ← the spine
```

## The six parts

| Part | Where |
|---|---|
| **Heartbeat** | `dependency-audit.yml`'s `on: schedule: cron: "0 9 * * *"` — daily, no clock-watching, no laptop required. `workflow_dispatch` added so a human can fire one beat on demand to test it. |
| **Worktree** | Skill step 3: a version bump is drafted in `git worktree add -b deps/<package>-<version> ...`, isolated from the main checkout, tests run inside it before anything is committed. |
| **Skill** | `.claude/skills/dependency-audit/SKILL.md` — the whole procedure, so the workflow's `prompt` is just `/dependency-audit` instead of re-describing six steps in YAML. |
| **Maker-checker** | Skill steps 2–3 draft findings and (maybe) a fix; step 4 has the same agent re-run the checks itself, from scratch, before trusting its own draft — PASS/FAIL, cited. |
| **Connector** | Skill step 5: `gh issue comment` on a standing "Dependency Audit Log" issue — output lands somewhere a human sees it without opening a terminal. |
| **Spine** | `audit-progress.md` — `## Done` read first (no duplicate reports), written last; `## Open / needs a human` if a run is cut short or fails its own checker. |

## Budget guards

- Workflow: `timeout-minutes: 15` (a stuck beat gets killed, not left running all day) and a `concurrency` group so overlapping runs can't pile up.
- Skill: capped at 10 tool calls / 3 turns for the audit-and-report half, and **one PR per run, maximum** — this chore should never open more than one thing to review at a time.
- Model/effort: this is mechanical, low-stakes work (Concept 13) — no reason to run it at a high effort level; the default is plenty.

## Concept 15 — the habit this loop cannot replace

The loop can draft, check, and report on its own. It cannot decide
whether "check `requirements.txt` weekly" is still the right target, or
notice if its own checker started rubber-stamping. That's a human habit,
not a feature to add:

**Once a week, actually open the "Dependency Audit Log" issue and read
what it says** — not just whether the latest comment says PASS. If a
month goes by and every comment says "nothing new," that's either a
genuinely quiet repo or a checker that stopped checking; only reading it
tells you which.

## Status

- [x] Local artifacts built: workflow, skill, spine, `requirements.txt`.
      Worktrees the skill creates (`../loop-eng-worktrees/wt-deps-*`) live
      as sibling directories outside this repo, like Projects 4/5's, so
      no `.gitignore` change is needed.
- [x] First beat rehearsed locally end-to-end (`claude -p`, real
      `pip-audit`/`pip list --outdated`, real independent checker
      re-verification — PASS, cost **$0.23** for this beat). Found and
      fixed two real bugs in the process: `/dependency-audit` as a bare
      slash prompt didn't resolve in headless mode (switched the
      workflow's `prompt` to plain language that explicitly invokes the
      Skill tool, which does work), and `--allowedTools` needs `Skill`
      listed explicitly or the skill can't fire at all.
- [x] The one step that couldn't run locally — posting to GitHub — failed
      **loudly**, exactly as Project 7 wants: no `gh` auth here, so it
      logged the gap under "Open / needs a human" instead of silently
      skipping step 5. That's the correct behavior, not a failure of the
      loop.
- [ ] Pushed to GitHub, `ANTHROPIC_API_KEY` secret added, Claude GitHub
      App installed (same prerequisite Project 6 needed — not yet done).
      Once that's in place, re-run this beat for real so it can actually
      post to the tracking issue.
- [ ] A week of unattended scheduled runs observed.
