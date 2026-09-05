# Project 10 — Routine Drill B: Secrets and the Environment

_Difficulty: easy to medium · Uses: A4 (secrets), A2 (the environment)_

**Build.** Write a prompt that needs one secret — a dummy token, since
this drill is about *where the value lives*, not what it unlocks.
First run: token in a gitignored `.env` file, watch the Routine fail to
find it. Second run: token moved to the environment-variables panel,
plus the one prompt line the appendix recommends. Compare the two runs.

**Done when:** the second run reads the token from the environment, and
you can explain the mechanical reason the first run couldn't:
gitignored files never reach GitHub, so the fresh cloud clone never
contains them.

## Reuses Project 9's throwaway repo

Same repo (`../project9-routine-drill-a/throwaway-repo`) — the appendix
frames all three drills as happening in one throwaway repo. Added on
top of Project 9's 3 commits:

- `.gitignore` (excludes `.env`) — **committed and pushed**
- `.env` containing `DUMMY_API_TOKEN=sk-dummy-a1b2c3d4e5f6` — **exists
  locally only, on purpose.** It's gitignored, so `git push` never
  sends it. The GitHub repo — and therefore every fresh cloud clone a
  Routine makes — genuinely does not contain this file. That's the
  entire mechanism this drill demonstrates, not something to work
  around.

## The two runs

### Run 1 — token only in `.env` (expected to fail)

**Prompt:**
> This repo needs one credential to finish its task: `DUMMY_API_TOKEN`.
> Find its value (check environment variables, and a `.env` file if one
> exists) and write a file `SECRET_CHECK.md` at the repo root
> containing exactly: `Token ends in: <last 4 characters>`. Commit and
> push that file to a branch named `claude/secret-drill` (create it if
> needed). If you cannot find the token, say so explicitly in
> `SECRET_CHECK.md` instead of guessing or inventing a value.

Expect this to end **green** (the session completes fine) while the
actual task fails or reports "token not found" — read the transcript to
see exactly what Claude tried (checking for `.env`, checking `os.environ`,
etc.) before concluding it wasn't there.

### Run 2 — token moved to the environment-variables panel

Before this run: add `DUMMY_API_TOKEN=sk-dummy-a1b2c3d4e5f6` in the
routine's **environment → environment variables** panel (claude.ai web
UI — not something the scheduling API/tool exposes, so this step is
manual). Then update the routine's prompt to add the one line the
appendix recommends:

> This repo needs one credential to finish its task: `DUMMY_API_TOKEN`.
> **Credentials are available as environment variables; do not look for
> a `.env` file.** Find its value and write a file `SECRET_CHECK.md` at
> the repo root containing exactly: `Token ends in: <last 4
> characters>`. Commit and push that file to a branch named
> `claude/secret-drill` (create it if needed).

Expect this one to actually find `sk-dummy-a1b2c3d4e5f6` (last 4
characters: `e5f6`), write `SECRET_CHECK.md` with `Token ends in:
e5f6`, and push it.

## What's still needed before either run can fire

1. **The repo needs to be on GitHub** — same open item as Project 9
   (`gh auth login`, `gh repo create --source=. --push` from inside
   `throwaway-repo/`, including the new `.gitignore` commit).
2. **Run 2 only:** the `DUMMY_API_TOKEN` environment variable has to be
   added by hand in the routine's environment settings on
   `claude.ai` before I update the prompt and fire it — that panel
   isn't reachable through the scheduling tool.

## Results

_(filled in once both runs have fired)_
