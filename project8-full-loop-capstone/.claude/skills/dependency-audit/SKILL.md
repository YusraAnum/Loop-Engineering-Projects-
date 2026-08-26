---
name: dependency-audit
description: Weekly dependency audit for this repo's requirements.txt — checks for known vulnerabilities and available updates, drafts a version-bump PR in an isolated worktree if one is warranted, has an independent checker verify the findings, then posts a report. Use when asked to run the scheduled dependency audit.
---

# Dependency Audit

The body of Project 8's loop. One beat = one run of every step below.
Read `audit-progress.md` first; write to it last. Never skip a step
because "nothing changed" — a run that found nothing still writes a line.

## Budget guard

Cap yourself at **10 tool calls and 3 turns** for the audit-and-report
half (steps 1–4). If you're not done by then, stop, write what you found
so far to `audit-progress.md` under "Open / needs a human," and post
that partial result instead of continuing. Never open more than one PR
per run (step 5's cap).

## 1. Read the spine first

Read `project8-full-loop-capstone/audit-progress.md`. Its `## Done`
section is the record of every prior run: what was audited, when, and
what was found. Do not re-report a finding already logged there unless
its state changed (e.g. a package that was "outdated" is now also
"vulnerable").

## 2. Run the actual audit — maker step

From the repo root, against `requirements.txt`:
- `pip list --outdated` for available updates.
- `pip install pip-audit` (if not already present) then
  `pip-audit -r requirements.txt` for known CVEs. If `pip-audit` cannot
  be installed or run (no network, etc.), say so explicitly in the
  report — do not silently skip the vulnerability check.

Draft findings as plain bullets: package, current version, available
version (if outdated), CVE id and severity (if vulnerable).

## 3. If a version bump is warranted, draft it in an isolated worktree

Only for a genuinely outdated **or** vulnerable package, and only one
PR per run:
- `git worktree add -b deps/<package>-<new-version>
  ../loop-eng-worktrees/wt-deps-<package> <base-commit>`
- In that worktree, bump the pin in `requirements.txt`, run the repo's
  test suites (`project2-make-tests-pass`, `project3-morning-brief`)
  against the new version, and commit only if they pass.
- If tests fail against the new version, do not force it — report the
  failure as a finding instead ("X.Y.Z breaks the test suite: <why>"),
  and leave the worktree for a human to look at.

## 4. Checker step — independent verification

Before anything gets posted, verify the draft findings and any diff
yourself, as if you had not written them:
- Re-run `pip-audit`/`pip list --outdated` yourself and confirm the
  numbers match what step 2 claims — don't trust the maker's own report.
- If a worktree/PR was drafted, run the test suites in it yourself and
  read the real output.
- Reply PASS or FAIL, citing the actual commands you ran. A FAIL means:
  do not open the PR, but still post the audit findings — a bad draft
  fix doesn't excuse hiding a real finding.

## 5. Connector — post the report

Post the week's findings as a comment on the tracking issue (find it
with `gh issue list --search "Dependency Audit Log" --state open`; if
none exists yet, `gh issue create` one, title exactly `Dependency Audit
Log`, and comment on that from then on). Include: date, what was
checked, what was found (or "nothing new"), and the checker's verdict.
If a PR was opened, link it in the comment.

## 6. Spine — write last

Append one entry to `audit-progress.md`'s `## Done` section: date, a
one-line summary of what was found, and the checker's verdict. If the
budget guard cut the run short, or the checker said FAIL, write the
entry under `## Open / needs a human` instead, so a silent partial run
is never mistaken for a clean one.

## Concept 15 — this does not replace you reading it

This loop drafts and checks its own work, but it cannot decide whether
its *target* is still right. Once a week, actually open the tracking
issue and read what it posted — not just whether it posted "PASS." A
loop that always says PASS on a target nobody rechecked is the gaming
failure mode, not a healthy loop.
