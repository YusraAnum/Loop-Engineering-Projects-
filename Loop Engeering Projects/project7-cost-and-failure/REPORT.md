# Project 7 — Cost, Failure, and the Log Line

Rehearsing Project 3's (`project3-morning-brief`) overnight failure now,
on purpose, while it's cheap and someone's watching — instead of
discovering it at 3am. Two halves: measure the real cost of one beat
(Concept 13), then deliberately break it and check whether it fails
loudly or silently (Part 6).

## Part 1 — Real cost per beat

Project 3's script itself is pure Python — no model calls. "Real cost"
only exists once a beat is *run as an agent turn* (e.g. a heartbeat
firing `claude -p "run the morning brief and tell me what's new"`),
which is how it would actually be scheduled. Measured with
`claude -p ... --output-format json`, which reports real token usage
and `total_cost_usd` per run:

| Run | Cache state | Cost |
|---|---|---|
| 1st invocation | cold (no prompt cache yet) | **$0.0782** |
| 2nd invocation, run immediately after | warm (cache hit) | **$0.0199** |

The ~4x gap is the first non-obvious finding: **for a once-daily
"morning brief" cadence, every real beat pays close to the cold price**,
because the prompt cache's TTL (minutes to an hour) has already expired
between runs a day apart. A naive estimate using the cheap warm number
would understate the real monthly bill by roughly 4x.

**Monthly projections** (using the honest cold-per-beat price, $0.078,
per Concept 13's method: measure real tokens → multiply by price →
multiply by run count):

| Cadence | Beats/month | Cost/month |
|---|---|---|
| Once a day (its actual purpose) | ~30 | **~$2.35** |
| Once an hour | ~720 | **~$56** |
| Every 5 minutes, day and night | ~8,640 | **~$674** |

Same lesson the course teaches with its own numbers: frequency, not the
command, drives the cost. This particular beat is cheap enough that even
the worst cadence here is trivial — but the same script wrapped in a
heavier prompt or a bigger repo would scale the same way, and the
mistake ("just run it every 5 minutes to be safe") is the same mistake
regardless of the absolute numbers.

## Part 2 — Breaking it on purpose

Rather than injecting an arbitrary bug, I looked for a failure mode
already latent in the shipped code, since that's the one that would
actually bite at 3am.

**Found it:** `find_todos()` had `except OSError: continue` — if any
scanned file became unreadable (permissions, a lock, a transient disk
error), that file's TODOs were dropped with **zero trace**. No print, no
log line, no note in `progress.md`, no non-zero exit. The loop would
report "nothing new since last run ✓" even while sitting on a real,
unreported TODO.

**Reproduced it** (see `test_morning_brief.py::test_find_todos_reports_unreadable_files_instead_of_silently_dropping_them`
for the permanent regression test): planted a real todo comment in a
file, then simulated that one file raising `OSError` on read.

- Before the fix: `find_todos()` returned an empty list. The genuine
  TODO vanished. Nothing printed. Exit code 0.
- This is exactly Part 6's warning in miniature: *"a loop that fails
  silently is worse than no loop, because you believe work is happening
  that is not."*

**Fixed it**, following the "write a line every run, even on failure" /
"fail loudly at the limit" guidance:

- `find_todos()` now returns `(items, skipped)` instead of swallowing
  the error.
- `main()` prints a `WARNING:` line to stderr naming every skipped file.
- Each skipped file is written into `progress.md`'s `## Open / needs a
  human` section (previously a dead section nothing ever wrote to) —
  new `append_to_needs_human()` — so the failure survives past the
  terminal closing, exactly like `## Done` already does for successes.
- `main()` now exits non-zero (`sys.exit(1)`) when anything was skipped,
  so a cron/CI wrapper watching exit codes notices too — not just a
  human reading the log.

**Verified end-to-end, for real, against the real repo:** planted
`_rehearsal_broken_file.py` with a genuine todo comment, then denied
read access to it with a real Windows ACL (`icacls ... /deny`) — not a
mock, not a monkeypatched `open()` — and ran the actual script against
the actual `project3-morning-brief/progress.md`. Output captured
verbatim in [`failure-rehearsal.log`](./failure-rehearsal.log):

```
=== 2026-08-26T08:20:50Z — deliberate overnight-failure rehearsal ===
$ python morning_brief.py
WARNING: 1 file(s) could not be scanned:
  - project7-cost-and-failure/_rehearsal_broken_file.py: could not be read (Permission denied)
nothing new since last run ✓
exit code: 1
```

And `project3-morning-brief/progress.md` gained a real, permanent entry:

```
## Open / needs a human

### 2026-08-26
- project7-cost-and-failure/_rehearsal_broken_file.py: could not be read (Permission denied)
```

**Both artifacts stand on their own** — reading only `progress.md` and
`failure-rehearsal.log`, with no access to this conversation and no
re-running anything, tells you: on 2026-08-26 (08:20:50Z per the log),
the loop hit a real permission error on one file, printed a loud
warning, exited non-zero, and left a dated note under "needs a human"
instead of silently saying "nothing new" and exiting 0 — which is
exactly what the unfixed code did do, back in the "found it" repro
above.

Afterward, the ACL was removed and the rehearsal file deleted (no
reason to leave the repo genuinely broken) — but the log and the
`progress.md` entry were deliberately left in place as the permanent
record, the same way a real incident stays logged after the underlying
cause is fixed.

## Test suite after the fix

```
project3-morning-brief$ python -m pytest -v
7 passed
```

3 new tests: the silent-drop repro (now asserting it's reported, not
dropped), and two for `append_to_needs_human()` (inserts correctly,
raises a clear `ValueError` if the section is ever removed — same
pattern as the existing `append_to_done()` guard).

## What this rehearsal bought

Finding this at 3am would have looked like: the loop ran, said
"nothing new," and a real TODO sat unreported for however long the file
stayed locked — with no way to tell, after the fact, that anything had
gone wrong at all. Finding it now, on purpose, cost one `claude -p`
invocation (~$0.02) and a few minutes.
