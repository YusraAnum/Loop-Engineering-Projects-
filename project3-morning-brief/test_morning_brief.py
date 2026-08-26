"""Tests for morning_brief.append_to_done()."""
import pytest

from morning_brief import append_to_done


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
