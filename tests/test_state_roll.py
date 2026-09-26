"""state_roll.py — deterministic STATE.md rolls (deadlines + keep-15 archive)."""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "state_roll.py"
ARROW = "→"

_SPEC = importlib.util.spec_from_file_location("state_roll", SCRIPT)
mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(mod)

TODAY = "2026-09-26"
ROLLED_WEEKLY = "2026-10-02"
ROLLED_BUCKET = "09-28→10-02"
WEEKLY_HEADING = (
    "### Weekly — recurring (rolling; next deadline **{deadline}**, "
    "bucket {bucket})"
)
ROLLED_HEADER = "**Roll 2026-09-26** (automated keep-15 roll; `scripts/state_roll.py`):"


def _rows(n: int, newest: date = date(2026, 9, 25)) -> list[str]:
    return [
        f"- **{(newest - timedelta(days=i)).isoformat()}** — decision {i} "
        f"[record](docs/notes/{(newest - timedelta(days=i)).isoformat()}.md#a) "
        "[external](https://example.com/x) [fragment](#a) [parent](../up.md)"
        for i in range(n)
    ]


def _state(
    *,
    weekly: str = "2026-09-25",
    monthly: str = "2026-10-21",
    rows: list[str] | None = None,
    bucket: str = "09-21→09-25",
) -> str:
    rows = _rows(2) if rows is None else rows
    return "\n".join(
        [
            "# STATE — First Passage",
            "",
            "**Last curated:** 2026-09-25",
            "",
            "## OPERATOR QUEUE — strictly ordered, ≤5 live items",
            "",
            "| 1 | queue row | owner | blocks |",
            "",
            "## Executed operator decisions — decision index",
            "",
            "Newest 15 consequences; older index lives in the archive.",
            "",
            *rows,
            "",
            "## Dormant cross-session threads",
            "",
            "none.",
            "",
            "## Scheduled forward triggers",
            "",
            WEEKLY_HEADING.format(deadline=weekly, bucket=bucket),
            "",
            "- **Coverage evidence:** operator-owned prose; the roller must not touch it.",
            "",
            f"### Monthly — recurring (rolling; next deadline **{monthly}**)",
            "",
            "- **Subscription reconfirm.**",
            "",
        ]
    )


def _archive() -> str:
    return "\n".join(
        [
            "# STATE executed-decision index — archive (pre keep-15 roll, 2026-08-23)",
            "",
            "Rolled from STATE.md; newest 15 stay on STATE.",
            "",
            "**Seventeenth roll, 2026-09-25** (two entries):",
            "",
            "- **2026-09-03** — archived earlier [record](../../../../../docs/a.md)",
            "",
            "- **2026-09-03** — archived earlier still",
            "",
            "**Sixteenth roll, 2026-09-24** (one entry):",
            "",
            "- **2026-09-02** — older archived row",
            "",
        ]
    )


def _pair(tmp_path: Path, state: str, archive: str | None = None) -> tuple[Path, Path]:
    state_path = tmp_path / "STATE.md"
    state_path.write_text(state, encoding="utf-8", newline="")
    archive_path = tmp_path / "archive.md"
    archive_path.write_text(
        archive if archive is not None else _archive(), encoding="utf-8", newline=""
    )
    return state_path, archive_path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", newline="")


def _out(result: subprocess.CompletedProcess) -> str:
    return result.stdout.decode().replace("\r\n", "\n")


def _run(state: Path, archive: Path, today: str, *extra: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.pop("STATE_CURRENCY_TODAY", None)
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--state",
            str(state),
            "--archive",
            str(archive),
            "--today",
            today,
            *extra,
        ],
        cwd=REPO,
        env=env,
        capture_output=True,
    )


# --- weekly -----------------------------------------------------------------


def test_weekly_past_rolls_to_next_friday_bucket(tmp_path: Path) -> None:
    original = _state()
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, "2026-09-26")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "weekly: 2026-09-25 -> 2026-10-02\n"
    expected = original.replace(
        WEEKLY_HEADING.format(deadline="2026-09-25", bucket="09-21→09-25"),
        WEEKLY_HEADING.format(deadline=ROLLED_WEEKLY, bucket=ROLLED_BUCKET),
    )
    rolled = _read(state)
    assert rolled == expected
    # Coverage text, Last curated and the queue are untouched.
    assert (
        "- **Coverage evidence:** operator-owned prose; the roller must not touch it."
        in rolled
    )
    assert "**Last curated:** 2026-09-25" in rolled
    assert "| 1 | queue row | owner | blocks |" in rolled
    assert _read(archive) == _archive()


def test_weekly_deadline_equal_to_today_is_not_past(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state())
    result = _run(state, archive, "2026-09-25")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "state-roll: nothing to roll\n"
    assert _read(state) == _state()
    assert _read(archive) == _archive()


def test_weekly_past_by_more_than_a_week_uses_first_friday(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly="2026-09-04"))
    result = _run(state, archive, "2026-09-29")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "weekly: 2026-09-04 -> 2026-10-02\n"
    rolled = _read(state)
    assert WEEKLY_HEADING.format(deadline=ROLLED_WEEKLY, bucket=ROLLED_BUCKET) in rolled
    assert "- **Coverage evidence:**" in rolled


def test_first_friday_is_on_or_after_today() -> None:
    assert mod.first_friday(date(2026, 9, 25)).isoformat() == "2026-09-25"
    assert mod.first_friday(date(2026, 9, 26)).isoformat() == "2026-10-02"
    assert mod.first_friday(date(2026, 9, 28)).isoformat() == "2026-10-02"


# --- monthly ----------------------------------------------------------------


def test_monthly_past_rolls_to_next_month_same_day(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly="2026-11-06", monthly="2026-10-21"))
    result = _run(state, archive, "2026-10-22")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "monthly: 2026-10-21 -> 2026-11-21\n"
    rolled = _read(state)
    assert "### Monthly — recurring (rolling; next deadline **2026-11-21**)" in rolled
    assert WEEKLY_HEADING.format(deadline="2026-11-06", bucket="09-21→09-25") in rolled


def test_monthly_rolls_across_year_end(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly="2027-01-01", monthly="2026-12-21"))
    result = _run(state, archive, "2026-12-22")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "monthly: 2026-12-21 -> 2027-01-21\n"
    assert "### Monthly — recurring (rolling; next deadline **2027-01-21**)" in _read(state)


def test_monthly_day_above_28_fails_closed(tmp_path: Path) -> None:
    # A clamped deadline cannot carry the intended cadence day across short
    # months, so the roller refuses rather than drift (Jan 31 -> Feb 28 -> Mar 28).
    with pytest.raises(mod.StateRollError):
        mod.next_monthly(date(2027, 1, 31), date(2027, 2, 1))
    state, archive = _pair(tmp_path, _state(weekly="2026-12-04", monthly="2026-10-31"))
    before = _read(state)
    result = _run(state, archive, "2026-11-01")
    assert result.returncode == 2
    assert b"roll the Monthly heading by hand" in result.stderr
    assert _read(state) == before


def test_monthly_day_28_still_rolls() -> None:
    assert mod.next_monthly(date(2027, 1, 28), date(2027, 2, 1)).isoformat() == "2027-02-28"


def test_monthly_deadline_today_is_not_past(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly="2026-10-02", monthly="2026-09-26"))
    result = _run(state, archive, "2026-09-26")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "state-roll: nothing to roll\n"


# --- decision index keep-15 -------------------------------------------------


def test_index_overflow_archives_rows_above_existing_roll_header(tmp_path: Path) -> None:
    rows = _rows(17)
    original = _state(rows=rows)
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    assert _out(result) == (
        "weekly: 2026-09-25 -> 2026-10-02\n" "index: archived 2 row(s)\n"
    )

    rolled = _read(state)
    assert rolled == _state(
        rows=rows[:15], weekly=ROLLED_WEEKLY, bucket=ROLLED_BUCKET
    )
    assert all(row in rolled for row in rows[:15])
    assert all(row not in rolled for row in rows[15:])

    archived = _read(archive)
    at = archived.index(ROLLED_HEADER)
    seventeenth = archived.index("**Seventeenth roll, 2026-09-25**")
    assert at < seventeenth
    # Rows keep document order (newest first), each followed by a blank line.
    rewritten = [mod.rewrite_links(row) for row in rows[15:]]
    assert archived[at:] == (
        ROLLED_HEADER
        + "\n\n"
        + "".join(row + "\n\n" for row in rewritten)
        + archived[seventeenth:]
    )
    assert "](../../../../../docs/notes/2026-09-09.md#a)" in archived
    assert "](https://example.com/x)" in archived
    assert "](#a)" in archived
    assert "](../up.md)" in archived
    assert "](docs/notes/" not in archived[at:seventeenth]


def test_index_at_or_below_fifteen_changes_nothing(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly=ROLLED_WEEKLY, rows=_rows(15)))
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    assert _out(result) == "state-roll: nothing to roll\n"
    assert _read(state) == _state(weekly=ROLLED_WEEKLY, rows=_rows(15))
    assert _read(archive) == _archive()


def test_second_same_day_roll_reuses_today_block(tmp_path: Path) -> None:
    rows = _rows(17)
    state, archive = _pair(tmp_path, _state(rows=rows))
    first = _run(state, archive, TODAY)
    assert first.returncode == 0, first.stderr
    rolled = _read(state)
    assert rolled == _state(rows=rows[:15], weekly=ROLLED_WEEKLY, bucket=ROLLED_BUCKET)

    # Three fresh decisions land on top of STATE, pushing three more rows off.
    fresh = _rows(3, newest=date(2026, 9, 28))
    refreshed = rolled.replace(
        rows[0] + "\n", "\n".join(fresh) + "\n" + rows[0] + "\n", 1
    )
    state.write_text(refreshed, encoding="utf-8", newline="")
    second = _run(state, archive, TODAY)
    assert second.returncode == 0, second.stderr
    assert _out(second) == "index: archived 3 row(s)\n"

    archived = _read(archive)
    assert archived.count(ROLLED_HEADER) == 1
    assert archived.count("**Seventeenth roll, 2026-09-25**") == 1
    block = archived.split(ROLLED_HEADER)[1].split("**Seventeenth roll")[0]
    assert block.startswith("\n\n- **2026-09-13** — decision 12")
    assert block.count("- **") == 5
    expected_state = refreshed.replace(
        "".join(row + "\n" for row in rows[12:15]), "", 1
    )
    assert _read(state) == expected_state


def test_rewrites_only_relative_link_targets() -> None:
    row = (
        "- **2026-09-09** — a [rel](docs/a.md) [anchor](#frag) [abs](/root.md) "
        "[up](../p.md) [http](http://x.y) [https](https://x.y) [mail](mailto:a@b.c)"
    )
    assert mod.rewrite_links(row) == (
        "- **2026-09-09** — a [rel](../../../../../docs/a.md) [anchor](#frag) "
        "[abs](/root.md) [up](../p.md) [http](http://x.y) [https](https://x.y) "
        "[mail](mailto:a@b.c)"
    )


# --- determinism / idempotence / bytes --------------------------------------


def test_running_twice_changes_nothing(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    first = _run(state, archive, TODAY)
    assert first.returncode == 0, first.stderr
    state_bytes, archive_bytes = state.read_bytes(), archive.read_bytes()
    second = _run(state, archive, TODAY)
    assert second.returncode == 0, second.stderr
    assert _out(second) == "state-roll: nothing to roll\n"
    assert state.read_bytes() == state_bytes
    assert archive.read_bytes() == archive_bytes


def test_independent_copies_roll_identically(tmp_path: Path) -> None:
    copies = []
    for name in ("a", "b"):
        folder = tmp_path / name
        folder.mkdir()
        state, archive = _pair(folder, _state(rows=_rows(19)))
        result = _run(state, archive, TODAY)
        assert result.returncode == 0, result.stderr
        copies.append((state.read_bytes(), archive.read_bytes()))
    assert copies[0] == copies[1]


def test_crlf_input_stays_crlf(tmp_path: Path) -> None:
    rows = _rows(17)
    state, archive = _pair(
        tmp_path,
        _state(rows=rows).replace("\n", "\r\n"),
        _archive().replace("\n", "\r\n"),
    )
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    for path in (state, archive):
        raw = path.read_bytes()
        assert raw.count(b"\n") == raw.count(b"\r\n")
    assert b"\r\r" not in archive.read_bytes()
    assert b"\r\r" not in state.read_bytes()
    rewritten = [mod.rewrite_links(row) for row in rows[15:]]
    expected_archive = _archive().replace(
        "**Seventeenth roll, 2026-09-25**",
        ROLLED_HEADER
        + "\n\n"
        + "".join(row + "\n\n" for row in rewritten)
        + "**Seventeenth roll, 2026-09-25**",
        1,
    )
    assert _read(archive) == expected_archive.replace("\n", "\r\n")
    expected = _state(rows=rows[:15], weekly=ROLLED_WEEKLY, bucket=ROLLED_BUCKET)
    assert _read(state) == expected.replace("\n", "\r\n")


def test_second_same_day_roll_crlf_reuses_today_block(tmp_path: Path) -> None:
    rows = _rows(17)
    state, archive = _pair(
        tmp_path,
        _state(rows=rows).replace("\n", "\r\n"),
        _archive().replace("\n", "\r\n"),
    )
    first = _run(state, archive, TODAY)
    assert first.returncode == 0, first.stderr
    rolled = _read(state)
    fresh = _rows(3, newest=date(2026, 9, 28))
    refreshed = rolled.replace(
        rows[0] + "\r\n", "\r\n".join(fresh) + "\r\n" + rows[0] + "\r\n", 1
    )
    state.write_text(refreshed, encoding="utf-8", newline="")
    second = _run(state, archive, TODAY)
    assert second.returncode == 0, second.stderr
    assert _out(second) == "index: archived 3 row(s)\n"
    archived = _read(archive)
    assert archived.count(ROLLED_HEADER) == 1
    assert archived.count("**Seventeenth roll, 2026-09-25**") == 1
    assert archived.count("- **2026-09-13** — decision 12") == 1
    assert b"\r\r" not in archive.read_bytes()


def test_lf_input_stays_lf(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(), _archive())
    assert b"\r" not in state.read_bytes()
    result = _run(state, archive, "2026-09-26")
    assert result.returncode == 0, result.stderr
    assert b"\r" not in state.read_bytes()
    assert b"\r" not in archive.read_bytes()


# --- --check ----------------------------------------------------------------


def test_check_reports_due_roll_without_writing(tmp_path: Path) -> None:
    rows = _rows(17)
    state, archive = _pair(tmp_path, _state(rows=rows))
    state_bytes, archive_bytes = state.read_bytes(), archive.read_bytes()
    result = _run(state, archive, TODAY, "--check")
    assert result.returncode == 1, result.stderr
    assert _out(result) == (
        "weekly: 2026-09-25 -> 2026-10-02\n" "index: archived 2 row(s)\n"
    )
    assert state.read_bytes() == state_bytes
    assert archive.read_bytes() == archive_bytes


def test_check_exits_zero_when_nothing_is_due(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly=ROLLED_WEEKLY, rows=_rows(15)))
    result = _run(state, archive, TODAY, "--check")
    assert result.returncode == 0, result.stderr
    assert result.stdout == b""


# --- errors -----------------------------------------------------------------


def test_missing_weekly_heading_exits_two(tmp_path: Path) -> None:
    broken = _state().replace(
        WEEKLY_HEADING.format(deadline="2026-09-25", bucket="09-21→09-25"),
        "### Weekly — recurring (no deadline spelled out)",
    )
    state, archive = _pair(tmp_path, broken)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"Weekly" in result.stderr
    assert _read(state) == broken


def test_missing_state_file_exits_two(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state())
    state.unlink()
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert result.stderr.startswith(b"state-roll: FAIL")


def test_missing_triggers_section_exits_two(tmp_path: Path) -> None:
    broken = _state().replace("## Scheduled forward triggers", "## Somewhere else")
    state, archive = _pair(tmp_path, broken)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"Scheduled forward triggers" in result.stderr


def test_today_env_var_freezes_clock(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state())
    env = os.environ.copy()
    env["STATE_CURRENCY_TODAY"] = "2026-09-27"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state), "--archive", str(archive)],
        cwd=REPO,
        env=env,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert _out(result) == "weekly: 2026-09-25 -> 2026-10-02\n"


def test_next_day_roll_goes_above_previous_automated_block(tmp_path: Path) -> None:
    rows = _rows(16)
    state, archive = _pair(tmp_path, _state(rows=rows))
    assert _run(state, archive, TODAY).returncode == 0

    # Next day: one fresh decision pushes one more row off.
    rolled = _read(state)
    fresh = _rows(1, newest=date(2026, 9, 28))
    state.write_text(
        rolled.replace(rows[0] + "\n", fresh[0] + "\n" + rows[0] + "\n", 1),
        encoding="utf-8", newline="",
    )
    later = (date.fromisoformat(TODAY) + timedelta(days=1)).isoformat()
    second = _run(state, archive, later)
    assert second.returncode == 0, second.stderr

    archived = _read(archive)
    later_header = archived.index(f"**Roll {later}**")
    earlier_header = archived.index(ROLLED_HEADER)
    ordinal_header = archived.index("**Seventeenth roll, 2026-09-25**")
    assert later_header < earlier_header < ordinal_header


@pytest.mark.parametrize("failing", ["state", "archive"])
def test_failed_write_loses_nothing_and_retry_archives_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failing: str
) -> None:
    rows = _rows(17)
    state, archive = _pair(tmp_path, _state(rows=rows))
    state_before, archive_before = _read(state), _read(archive)
    today = date.fromisoformat(TODAY)
    new_state, new_archive, _ = mod.plan(state_before, lambda: archive_before, today)

    real_replace = mod._replace

    target = state if failing == "state" else archive

    def failing_replace(path: Path, text: str) -> None:
        if path == target:
            raise mod.StateRollError(f"simulated {failing} write failure")
        real_replace(path, text)

    monkeypatch.setattr(mod, "_replace", failing_replace)
    with pytest.raises(mod.StateRollError):
        mod.commit(state, new_state, archive, new_archive)
    # Nothing is lost: STATE keeps its overflow rows and the archive is restored.
    assert _read(state) == state_before
    assert _read(archive) == archive_before

    monkeypatch.setattr(mod, "_replace", real_replace)
    retry = _run(state, archive, TODAY)
    assert retry.returncode == 0, retry.stderr
    archived = _read(archive)
    assert archived.count(ROLLED_HEADER) == 1
    for i in (15, 16):
        assert archived.count(f"— decision {i} ") == 1
    assert not list(tmp_path.glob("*.state_roll.tmp"))
