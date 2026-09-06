"""CLI regressions for routing the living session header to STATE."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_sessions_queue_bind.py"


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _state(*rows: int) -> str:
    table_rows = "\n".join(f"| {row} | item {row} | owner | block |" for row in rows)
    return (
        "# STATE\n\n"
        "## OPERATOR QUEUE — strictly ordered, ≤5 live items\n\n"
        "| # | Item | Owner artifact | Blocks |\n"
        "|---|---|---|---|\n"
        f"{table_rows}\n\n"
        "## Executed operator decisions — decision index\n"
    )


def _sessions(header: str, entry: str = "**Focus:** historical context only.") -> str:
    return (
        "# Session Log\n\n"
        f"{header}\n\n"
        "---\n\n"
        "## 2026-09-05a — historical entry\n\n"
        f"{entry}\n"
    )


def _run(state: Path, sessions: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state), "--file", str(sessions)],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def test_queue_change_does_not_require_a_journal_change(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            "Current priorities live in the [operator queue](../STATE.md#operator-queue).",
            "**Open / next:** session context mentions #1 only.",
        ),
    )
    original_journal = sessions.read_bytes()

    assert _run(state, sessions).returncode == 0
    _write(state, _state(1, 2))
    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr
    assert sessions.read_bytes() == original_journal


def test_historical_entry_without_open_next_is_valid(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions("Current priorities: [STATE queue](../STATE.md#operator-queue)."),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "visible_route",
    [
        "[STATE queue](../STATE.md#operator-queue)",
        "[`STATE.md`](../STATE.md#operator-queue)",
    ],
    ids=["plain-label", "code-formatted-label"],
)
def test_visible_header_link_is_a_valid_route(
    tmp_path: Path, visible_route: str
) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(f"Current priorities: {visible_route}."),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "hidden_route",
    [
        "<!-- [STATE queue](../STATE.md#operator-queue) -->",
        "`[STATE queue](../STATE.md#operator-queue)`",
        "```markdown\n[STATE queue](../STATE.md#operator-queue)\n```",
        "    [STATE queue](../STATE.md#operator-queue)",
    ],
    ids=["html-comment", "inline-code", "fenced-code", "indented-code"],
)
def test_non_rendered_header_route_fails(tmp_path: Path, hidden_route: str) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(f"Current priorities are documented here:\n\n{hidden_route}"),
    )

    result = _run(state, sessions)

    assert result.returncode == 1
    assert "header" in result.stderr


def test_visible_link_after_longer_closing_fence_is_valid(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            "```markdown\n"
            "[example](../OTHER.md)\n"
            "````\n\n"
            "Current priorities: [STATE queue](../STATE.md#operator-queue)."
        ),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "hidden_heading",
    [
        "<!--\n## 2026-09-01a — example\n-->",
        "```markdown\n## 2026-09-01a — example\n```",
    ],
    ids=["html-comment", "fenced-code"],
)
def test_hidden_dated_heading_does_not_end_living_header(
    tmp_path: Path, hidden_heading: str
) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            f"Example:\n\n{hidden_heading}\n\n"
            "Current priorities: [STATE queue](../STATE.md#operator-queue)."
        ),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


def test_reference_style_header_link_is_a_valid_route(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            "Current priorities: [STATE queue][queue].\n\n"
            "[queue]: ../STATE.md#operator-queue"
        ),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


def test_shortcut_reference_header_link_is_a_valid_route(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            "Current priorities: [STATE queue].\n\n"
            "[STATE queue]: ../STATE.md#operator-queue"
        ),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


def test_comment_marker_inside_fence_does_not_hide_visible_route(
    tmp_path: Path,
) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            "```markdown\n"
            "<!-- literal example\n"
            "```\n\n"
            "Current priorities: [STATE queue](../STATE.md#operator-queue)."
        ),
    )

    result = _run(state, sessions)

    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize(
    "hidden_queue",
    [
        "<!--\n" + _state(1) + "-->",
        "```markdown\n" + _state(1) + "```",
    ],
    ids=["html-comment", "fenced-code"],
)
def test_non_rendered_state_queue_fails(tmp_path: Path, hidden_queue: str) -> None:
    state = _write(tmp_path / "STATE.md", "# STATE\n\n" + hidden_queue)
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions("Current priorities: [STATE queue](../STATE.md#operator-queue)."),
    )

    result = _run(state, sessions)

    assert result.returncode == 1
    assert "OPERATOR QUEUE" in result.stderr


@pytest.mark.parametrize(
    "header",
    [
        "Current priorities are elsewhere.",
        "Current priorities: [wrong file](../OTHER.md#operator-queue).",
    ],
)
def test_absent_or_incorrect_header_link_fails(tmp_path: Path, header: str) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    _write(tmp_path / "OTHER.md", _state(1))
    sessions = _write(tmp_path / "docs" / "SESSIONS.md", _sessions(header))

    result = _run(state, sessions)

    assert result.returncode == 1
    assert "header" in result.stderr


def test_state_link_only_in_historical_entry_fails(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(1))
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions(
            "Current priorities are elsewhere.",
            "**Open / next:** [STATE queue](../STATE.md#operator-queue), #1.",
        ),
    )

    result = _run(state, sessions)

    assert result.returncode == 1
    assert "header" in result.stderr


def test_state_without_operator_queue_fails(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", "# STATE\n\n## Decisions\n")
    sessions = _write(
        tmp_path / "docs" / "SESSIONS.md",
        _sessions("Current priorities: [STATE queue](../STATE.md#operator-queue)."),
    )

    result = _run(state, sessions)

    assert result.returncode == 1
    assert "OPERATOR QUEUE" in result.stderr


@pytest.mark.parametrize("missing", ["state", "sessions"])
def test_unreadable_input_fails(tmp_path: Path, missing: str) -> None:
    state = tmp_path / "STATE.md"
    sessions = tmp_path / "docs" / "SESSIONS.md"
    if missing != "state":
        _write(state, _state(1))
    if missing != "sessions":
        _write(
            sessions,
            _sessions("Current priorities: [STATE queue](../STATE.md#operator-queue)."),
        )

    result = _run(state, sessions)

    assert result.returncode == 1
    assert "FAIL" in result.stderr
