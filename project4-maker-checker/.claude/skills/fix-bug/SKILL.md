---
name: fix-bug
description: Steps for fixing a single bug in this repo - reproduce, locate, draft the smallest fix, verify with tests/lint. Use whenever asked to fix a specific bug here.
---

# Fix Bug

A short, repeatable checklist for the implementer to follow on every bug-fix run in this repo.

## 1. Reproduce first

Before touching any code, prove the bug is real:
- Write or run the smallest possible script/command that triggers the broken behavior.
- Capture the actual failure (error message, wrong output, traceback, or hang).
- Do not proceed to a fix based on reading code alone — reproduce it.

## 2. Locate the cause

- Find the exact function/lines responsible, not just the symptom's call site.
- Check whether the bug is already described anywhere in the repo (e.g. a `TODO` comment, an existing failing test) and note it.

## 3. Draft the smallest possible fix

- Change only what's needed to correct the broken behavior.
- Do not refactor, rename, or "clean up" unrelated code in the same pass.
- If the fix changes a function's contract (e.g. it now raises where it used to silently misbehave), make sure that's the intended contract, not a side effect.

## 4. Add or update a test

- Add a regression test that fails before the fix and passes after it.
- Prefer extending the existing test file over creating a new one, unless the repo's layout calls for a new file.

## 5. Verify before calling it done

Run, in this repo:
- The test suite for the affected project (e.g. `python -m pytest` from the project's folder).
- Any linter configured for the touched files, if one exists.

Only call the fix done once both the reproduction case and the full existing test suite pass. A fix that "should work" but wasn't actually run is not done.

## 6. Hand off

- Leave a clear diff: the reproduction/test addition plus the minimal source change.
- Do not open a PR or merge yourself — that decision belongs to the maker-checker flow around this skill (send the diff to the reviewer first).
