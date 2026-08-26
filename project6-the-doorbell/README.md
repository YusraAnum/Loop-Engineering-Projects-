# Project 6 — The Doorbell

Event-driven loop (Concept 7) wired to GitHub via a connector (Concept 10):
no schedule, no clock, no polling. It sits completely idle until GitHub
sends a `pull_request` webhook for this repo, then runs the review on
GitHub's own runner — not this machine.

## Where the actual workflow lives

GitHub Actions only ever reads workflow files from the **repository
root's** `.github/workflows/` directory — never from a project subfolder
like this one — so the functional file is at:

```
../.github/workflows/pr-review.yml
```

This folder just documents Project 6; nothing here needs to run locally.

## What the workflow does

1. **Trigger**: `on: pull_request: types: [opened, reopened, synchronize, ready_for_review]`.
   GitHub — not this repo, not a cron, not our laptop — decides when this fires.
2. **Runner**: a fresh `ubuntu-latest` GitHub-hosted VM, spun up only for
   that event and torn down after.
3. **Agent**: `anthropics/claude-code-action@v1` runs Claude Code inside
   that runner with a plain-text automation prompt (no `@claude` mention
   needed — see [Interactive and automation modes](https://code.claude.com/docs/en/github-actions#interactive-and-automation-modes)).
   It diffs the PR against its base branch, reads whatever files it needs,
   drafts a review, and posts it with `gh pr comment`.
4. **Output**: one PR comment, drafted by the agent, appearing whether or
   not your laptop is even on.

## One-time setup (do this before opening a test PR)

These steps touch your GitHub account/repo settings, so they're left for
you to run rather than done for you:

1. **Push this repo to GitHub** (it currently has no remote):
   ```
   gh auth login          # if not already authenticated
   gh repo create <name> --source=. --private   # or --public
   git push -u origin master
   ```
2. **Install the [Claude GitHub App](https://github.com/apps/claude)** on
   that repository (Settings → Integrations → GitHub Apps, or via the
   link above). It needs Contents, Issues, and Pull requests permissions.
3. **Add the `ANTHROPIC_API_KEY` secret**: repo Settings → Secrets and
   variables → Actions → New repository secret. (Or use a
   `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token` instead — if so,
   change the `anthropic_api_key:` line in the workflow to
   `claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`.)
4. **Open a PR** against the repo. Within a minute or two, a review
   comment should appear, posted by the Claude GitHub App.

## Why this is a loop without a heartbeat

Every other project in this repo (3, 5) needed something to fire it —
`/loop`, a cron, a human running a command. This one needs nothing
running at all between events: GitHub holds the trigger, and the runner
only exists for the seconds it takes to review one PR. That's the
event-driven shape Concept 7 describes, as opposed to the polling/
scheduled shape everything before it used.
