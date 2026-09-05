# Project 11 — Build the Two-Routine Gate

_Difficulty: medium to hard · Uses: A3 (the API trigger), A4 (the gate), A6 (the checklist)_

**Build.** Routine A, on a one-off schedule, drafts something
reviewable. Routine B has an API trigger and performs one small
follow-up action after a human reviews A's draft and fires B by hand
with the `curl` call from A3.

**Done when:** B ran only because you fired it, B's transcript shows
the action actually happened, and the A6 checklist has been run over
both routines (connectors pruned, unrestricted pushes off, a state
file chosen).

## Design

Same throwaway repo as Projects 9/10
(`../project9-routine-drill-a/throwaway-repo`).

- **Routine A (drafter)** — one-off. Reads `gate-state.md`, drafts
  `RELEASE_NOTES.md` summarizing the repo's commits, and pushes both
  files to a new branch `claude/release-notes`. **Does not open a PR,
  does not touch `main`.** This is the "draft" a human reviews.
- **Human** — reads `RELEASE_NOTES.md` on the `claude/release-notes`
  branch directly (via GitHub, or `git show`). Decides whether it's
  good enough to ship.
- **Routine B (executor)** — has an **API trigger** (a `/fire`
  endpoint + bearer token, generated once in the web UI — not
  something the scheduling tool can create). Its one small follow-up
  action: **open a real pull request** from `claude/release-notes`
  into `main`, and append an "approved & PR opened" line to
  `gate-state.md` on that same branch. It does **not** merge — merging
  stays a manual, final human action on GitHub, kept outside any
  routine on purpose (so "unrestricted branch pushes" can stay off for
  both routines).

This keeps the whole gate inside the `claude/*` branch-push
restriction: A pushes to `claude/release-notes`, B only ever pushes to
that same branch and opens a PR (a GitHub API call, not a push to
`main`). Nothing here ever needs unrestricted pushes.

## State file: `gate-state.md`

Committed to the throwaway repo, read by A first, written by both A
and B — same spine pattern as every other project:

```
## Drafts pending review

## Approved
```

A appends to "Drafts pending review" (branch name, date). B, once
fired, moves that same line into "Approved" (with the PR URL) — so
the file's own history shows the human-gate decision, not just the
git log.

## The part I cannot do for you

**Enabling Routine B's API trigger and generating its bearer token is
a web-UI-only action** (`claude.ai/code/routines/<id>` → the trigger
section). The scheduling tool I have can create/update a routine's
schedule, but not generate this token — and the token is **shown
exactly once**, so it has to be copied the moment it appears. Once
you have it, either:

- give it to me and I'll run the `curl` from A3 myself, or
- run the `curl` yourself — either way, B only fires because a human
  (you, or me acting on your explicit instruction) decided to send
  that request. That's the actual gate.

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/<ROUTINE_B_ID>/fire \
  -H "Authorization: Bearer <ROUTINE_B_TOKEN>" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## A6 checklist (run over both routines before calling this done)

- [ ] Repositories: `Aliyan707/Loop-Engeering` only, unrestricted
      pushes **off**, on both A and B.
- [ ] Prompt: self-contained on both — no assumed context from this
      conversation.
- [ ] Connectors: none needed by either routine — pruned on both.
- [ ] Environment: no secrets needed for this drill; default network
      access is enough.
- [ ] Trigger: A = one-off schedule, on purpose. B = API trigger, on
      purpose, fired only by an explicit human `curl`.
- [ ] State: `gate-state.md`, chosen before either routine ran.
- [ ] Human gate: A drafts only (no PR, no merge). B opens a PR only
      (no merge). The actual merge is a manual step outside both
      routines.
- [ ] Test run: both fired once, both transcripts read in full.

## Results

_(filled in once both routines exist and have fired)_
