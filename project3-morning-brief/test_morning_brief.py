"""Tests for morning_brief.append_to_done() and the TODO_RE scanner."""
import builtins
import os

import pytest

import morning_brief
from morning_brief import TODO_RE, append_to_done, append_to_needs_human, find_todos

# Built via concatenation so this fixture text isn't itself picked up
# as a real todo when morning_brief.py scans the repo.
REAL_TODO_LINE = "# " + "TODO" + ": fix this edge case"


def test_matches_real_todo_comment():
    assert TODO_RE.search(REAL_TODO_LINE)


def test_ignores_prose_mentioning_todo():
    line = "- Check whether the bug is already described anywhere (e.g. a `TODO` comment)"
    assert TODO_RE.search(line) is None


def test_append_to_done_with_done_section_present():
    progress_text = (
        "# Progress\n"
        "\n"
        "## In Progress\n"
        "- something\n"
        "\n"
        "## Done\n"
        "- old_item.py:1: TODO old\n"
        "\n"
        "## Backlog\n"
        "- other thing\n"
    )

    result = append_to_done(
        progress_text, "2026-08-25", ["file.py:1: TODO fix this"]
    )

    assert "### 2026-08-25" in result
    assert "- file.py:1: TODO fix this" in result
    # Existing sections and entries are preserved.
    assert "- old_item.py:1: TODO old" in result
    assert "## Backlog" in result
    assert "- other thing" in result
    # The new block is inserted inside "## Done", before "## Backlog".
    done_pos = result.index("## Done")
    new_block_pos = result.index("### 2026-08-25")
    backlog_pos = result.index("## Backlog")
    assert done_pos < new_block_pos < backlog_pos


def test_append_to_done_raises_value_error_when_done_section_missing():
    progress_text = (
        "# Progress\n"
        "\n"
        "## In Progress\n"
        "- something\n"
        "\n"
        "## Backlog\n"
        "- other thing\n"
    )

    with pytest.raises(ValueError, match="## Done"):
        append_to_done(progress_text, "2026-08-25", ["file.py:1: TODO fix this"])


def test_find_todos_reports_unreadable_files_instead_of_silently_dropping_them(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(morning_brief, "REPO_ROOT", str(tmp_path))
    monkeypatch.setattr(morning_brief, "SELF_FILE", os.devnull)

    broken = tmp_path / "broken.py"
    # Built via concatenation, like REAL_TODO_LINE above, so this fixture
    # text isn't itself picked up when morning_brief.py scans the real repo.
    broken.write_text("# " + "TODO" + ": this should have been found\n")

    real_open = builtins.open

    def flaky_open(path, *args, **kwargs):
        if str(path) == str(broken):
            raise OSError(13, "Permission denied (simulated)")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", flaky_open)

    items, skipped = find_todos()

    assert items == []  # the real TODO in broken.py was never found
    assert len(skipped) == 1
    assert "broken.py" in skipped[0]


def test_append_to_needs_human_inserts_under_correct_section():
    progress_text = (
        "# Progress\n"
        "\n"
        "## Done\n"
        "- old_item.py:1: TODO old\n"
        "\n"
        "## Open / needs a human\n"
        "- existing note\n"
    )

    result = append_to_needs_human(
        progress_text, "2026-08-26", ["broken.py: could not be read (Permission denied)"]
    )

    assert "### 2026-08-26" in result
    assert "- broken.py: could not be read (Permission denied)" in result
    assert "- existing note" in result  # existing content preserved
    needs_human_pos = result.index("## Open / needs a human")
    new_note_pos = result.index("### 2026-08-26")
    assert needs_human_pos < new_note_pos


def test_append_to_needs_human_raises_value_error_when_section_missing():
    progress_text = "# Progress\n\n## Done\n- x\n"
    with pytest.raises(ValueError, match="Open / needs a human"):
        append_to_needs_human(progress_text, "2026-08-26", ["note"])
