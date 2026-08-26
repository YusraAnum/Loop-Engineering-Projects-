#!/usr/bin/env python3
"""Scheduled loop that reports new TODO comments since the last run.

The spine: progress.md's "## Done" section is the only source of truth
for what has already been reported. Every run reads it first.
"""
import datetime
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "progress.md")
SELF_FILE = os.path.abspath(__file__)

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
INCLUDE_EXT = {".py", ".js", ".ts", ".sh", ".md"}
SKIP_FILES = {"progress.md"}

TODO_RE = re.compile(r"TODO:.*")


def find_todos():
    # skipped: files that raised OSError, so a read failure is reported
    # instead of silently dropping whatever TODOs that file held.
    items = []
    skipped = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fname in filenames:
            if fname in SKIP_FILES:
                continue
            if os.path.splitext(fname)[1] not in INCLUDE_EXT:
                continue
            fpath = os.path.join(dirpath, fname)
            if os.path.abspath(fpath) == SELF_FILE:
                continue
            relpath = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for lineno, line in enumerate(f, start=1):
                        if "TODO:" in line:
                            match = TODO_RE.search(line)
                            text = match.group(0).strip() if match else line.strip()
                            items.append(f"{relpath}:{lineno}: {text}")
            except OSError as e:
                skipped.append(f"{relpath}: could not be read ({e.strerror or e})")
    return sorted(items), skipped


def read_done_section(progress_text):
    recorded = set()
    in_done = False
    for line in progress_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            in_done = stripped == "## Done"
            continue
        if in_done and stripped.startswith("- "):
            recorded.add(stripped[2:].strip())
    return recorded


def append_to_done(progress_text, today, new_items):
    lines = progress_text.splitlines()
    done_idx = next(
        (i for i, l in enumerate(lines) if l.strip() == "## Done"), None
    )
    if done_idx is None:
        raise ValueError("progress.md is missing a '## Done' section")

    end_idx = len(lines)
    for i in range(done_idx + 1, len(lines)):
        if lines[i].strip().startswith("## "):
            end_idx = i
            break

    while end_idx > done_idx + 1 and lines[end_idx - 1].strip() == "":
        end_idx -= 1

    block = ["", f"### {today}"] + [f"- {item}" for item in new_items]
    new_lines = lines[:end_idx] + block + [""] + lines[end_idx:]
    return "\n".join(new_lines) + "\n"


def append_to_needs_human(progress_text, today, notes):
    lines = progress_text.splitlines()
    idx = next(
        (i for i, l in enumerate(lines) if l.strip() == "## Open / needs a human"),
        None,
    )
    if idx is None:
        raise ValueError("progress.md is missing an '## Open / needs a human' section")

    end_idx = len(lines)
    for i in range(idx + 1, len(lines)):
        if lines[i].strip().startswith("## "):
            end_idx = i
            break

    while end_idx > idx + 1 and lines[end_idx - 1].strip() == "":
        end_idx -= 1

    block = ["", f"### {today}"] + [f"- {note}" for note in notes]
    new_lines = lines[:end_idx] + block + [""] + lines[end_idx:]
    return "\n".join(new_lines) + "\n"


def main():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        progress_text = f.read()

    recorded = read_done_section(progress_text)
    found, skipped = find_todos()
    new_items = [item for item in found if item not in recorded]
    today = datetime.date.today().isoformat()
    updated = progress_text

    if new_items:
        print(f"New items found ({len(new_items)}):")
        for item in new_items[:5]:
            print(f"- {item}")
        try:
            updated = append_to_done(updated, today, new_items)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("nothing new since last run ✓")

    if skipped:
        print(f"WARNING: {len(skipped)} file(s) could not be scanned:", file=sys.stderr)
        for note in skipped:
            print(f"  - {note}", file=sys.stderr)
        try:
            updated = append_to_needs_human(updated, today, skipped)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            sys.exit(1)

    if updated != progress_text:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            f.write(updated)

    if skipped:
        sys.exit(1)


if __name__ == "__main__":
    main()
