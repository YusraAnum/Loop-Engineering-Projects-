# Project 9 — Routine Drill A: Reading Runs Instead of Trusting Green

_Difficulty: easy · Uses: A1 (routines basics), A3 (one-off schedules), A5 (reading runs)_

**Build.** In a throwaway repo, create a Routine whose prompt does one
small, checkable thing — summarizing yesterday's commits onto a
`claude/summary` branch. No repeating schedule: fire it once, read the
full transcript (not the status column), then change the prompt so the
task must fail (reading a file that doesn't exist) and fire it again.

**Done when:** two green runs exist — one whose transcript shows real
success, one whose transcript shows a real failure — and you can state
in one sentence why the status column alone couldn't tell them apart.

## The throwaway repo

`throwaway-repo/` — a tiny local git repo, 3 commits, all backdated to
2026-08-25 (yesterday relative to when this was built) so "summarize
yesterday's commits" has something real to find:

```
46bddb5 2026-08-25 Initial commit
7080c73 2026-08-25 Add calc.py with a basic add() helper
058dfae 2026-08-25 Add subtract() to calc.py
```

Routines only clone from a repository **URL** — a cloud session has no
access to local files at all — so this needs to live on GitHub before
a Routine can use it. Push it yourself, then hand me the URL:

```bash
cd project9-routine-drill-a/throwaway-repo
gh auth login                     # if not already authenticated
gh repo create <name> --source=. --private --push
```

## What happens once it's pushed

1. **Create the routine** (`RemoteTrigger`, `action: "create"`), one-off
   (`run_once_at`, a few minutes out), prompt A below, model
   `claude-sonnet-5`, no MCP connectors (this job needs none), repo =
   the URL you give me.
2. **Fire it, wait, then read the transcript** (`get_run_log`) — not
   just the status color.
3. **Update the same routine** with prompt B (the one designed to
   fail), fire it again with `action: "run"`, and read that transcript
   too.
4. **Compare the two transcripts** and write the one-sentence answer
   this drill is actually testing.

### Prompt A — the success case

> This repository has a small git history. List every commit dated
> 2026-08-25 with its short hash, commit message, and the files it
> touched. Write that list to a new file `SUMMARY.md` at the repo root
> (create it if it doesn't exist; overwrite if it does). Commit that
> file and push it to a branch named exactly `claude/summary` (create
> the branch if it doesn't already exist — do not touch any other
> branch). Do not modify any other file. When you're done, state
> explicitly whether `SUMMARY.md` was written and whether the push to
> `claude/summary` succeeded.

### Prompt B — the deliberate failure case

> Before doing anything else, read the file `commit-notes-from-lead.md`
> at the repo root and include its exact contents as the first section
> of your summary — this file has context the summary must open with.
> Then list every commit dated 2026-08-25 with its short hash, commit
> message, and the files it touched, write the full result (the lead's
> notes plus the commit list) to `SUMMARY.md` at the repo root, commit
> it, and push it to the branch `claude/summary` (create the branch if
> needed). Do not modify any other file.

`commit-notes-from-lead.md` does not exist anywhere in this repo, on
purpose. The session should still end cleanly (green) — the failure is
in the *task*, not the *infrastructure* — which is the entire point of
this drill.

## Results

_(filled in once both runs have fired — see `RESULTS.md` once it exists)_
