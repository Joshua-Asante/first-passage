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


def _week_bucket(deadline: str) -> str:
    """The Monday-Friday bucket of the deadline's week (round 5, 4111495548)."""
    monday = date.fromisoformat(deadline) - timedelta(
        days=date.fromisoformat(deadline).weekday()
    )
    return f"{monday:%m-%d}{ARROW}{monday + timedelta(days=4):%m-%d}"


def _state(
    *,
    weekly: str = "2026-09-25",
    monthly: str = "2026-10-21",
    rows: list[str] | None = None,
    bucket: str | None = None,
) -> str:
    rows = _rows(2) if rows is None else rows
    bucket = _week_bucket(weekly) if bucket is None else bucket
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


ARCHIVE_SUBDIR = Path("docs/ltm/notes/archive/state")


def _pair(tmp_path: Path, state: str, archive: str | None = None) -> tuple[Path, Path]:
    # Mirror the repo layout: STATE at the root, the archive five levels down,
    # so link rebasing is computed from real relative positions.
    state_path = tmp_path / "STATE.md"
    state_path.write_text(state, encoding="utf-8", newline="")
    (tmp_path / ARCHIVE_SUBDIR).mkdir(parents=True, exist_ok=True)
    archive_path = tmp_path / ARCHIVE_SUBDIR / "archive.md"
    archive_path.write_text(
        archive if archive is not None else _archive(), encoding="utf-8", newline=""
    )
    return state_path, archive_path


def _read(path: Path) -> str:
    # Path.read_text(newline=) exists only from Python 3.13; CI runs 3.11.
    with path.open(encoding="utf-8", newline="") as handle:
        return handle.read()


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
    assert WEEKLY_HEADING.format(deadline="2026-11-06", bucket=_week_bucket("2026-11-06")) in (
        rolled
    )


def test_monthly_rolls_across_year_end(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(weekly="2027-01-01", monthly="2026-12-21"))
    result = _run(state, archive, "2026-12-22")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "monthly: 2026-12-21 -> 2027-01-21\n"
    assert "### Monthly — recurring (rolling; next deadline **2027-01-21**)" in _read(state)


def test_unanchored_monthly_day_above_27_fails_closed(tmp_path: Path) -> None:
    # A clamped deadline cannot carry the intended cadence day across short
    # months, so the roller refuses rather than drift (Jan 31 -> Feb 28 -> Mar 28).
    with pytest.raises(mod.StateRollError):
        mod.next_monthly(date(2027, 1, 31), date(2027, 2, 1))
    state, archive = _pair(tmp_path, _state(weekly="2026-12-04", monthly="2026-10-31"))
    before = _read(state)
    result = _run(state, archive, "2026-11-01")
    assert result.returncode == 2
    assert b"cadence day NN" in result.stderr
    assert _read(state) == before


def test_monthly_day_27_still_rolls() -> None:
    assert mod.next_monthly(date(2027, 1, 27), date(2027, 2, 1)).isoformat() == "2027-02-27"


# --- Codex 4110350208: month-end cadence anchor -------------------------------

MONTHLY_ANCHORED = (
    "### Monthly — recurring (rolling; next deadline **{deadline}**, cadence day {day})"
)


def _monthly_state(deadline: str, day: str | None, weekly: str) -> str:
    heading = (
        MONTHLY_ANCHORED.format(deadline=deadline, day=day)
        if day is not None
        else f"### Monthly — recurring (rolling; next deadline **{deadline}**)"
    )
    return _state(weekly=weekly, monthly="2026-10-21").replace(
        "### Monthly — recurring (rolling; next deadline **2026-10-21**)", heading
    )


def test_hand_clamped_month_end_without_anchor_fails_closed(tmp_path: Path) -> None:
    # The Codex scenario: Jan 31 hand-clamped to Feb 28 reads back as day 28;
    # rolling it would silently move the cadence to the 28th. Refuse instead.
    original = _monthly_state("2027-02-28", None, weekly="2027-03-05")
    state, archive = _pair(tmp_path, original)
    for extra in ((), ("--check",)):
        result = _run(state, archive, "2027-03-01", *extra)
        assert result.returncode == 2
        assert b"cadence day NN" in result.stderr
        assert _read(state) == original


def test_anchored_month_end_keeps_cadence_through_short_months(tmp_path: Path) -> None:
    original = _monthly_state("2027-01-31", "31", weekly="2027-03-05")
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, "2027-02-01")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "monthly: 2027-01-31 -> 2027-02-28\n"
    assert _read(state) == _monthly_state("2027-02-28", "31", weekly="2027-03-05")
    result = _run(state, archive, "2027-03-01")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "monthly: 2027-02-28 -> 2027-03-31\n"
    assert _read(state) == _monthly_state("2027-03-31", "31", weekly="2027-03-05")


@pytest.mark.parametrize(
    ("old", "day", "today", "new"),
    [
        ("2028-01-31", 31, "2028-02-01", "2028-02-29"),  # leap February
        ("2027-01-30", 30, "2027-02-01", "2027-02-28"),
        ("2027-02-28", 30, "2027-03-01", "2027-03-30"),
        ("2027-03-31", 31, "2027-04-01", "2027-04-30"),
        ("2027-04-30", 31, "2027-05-01", "2027-05-31"),
        ("2027-02-28", 28, "2027-03-01", "2027-03-28"),
        ("2027-12-31", 31, "2028-01-01", "2028-01-31"),
    ],
)
def test_next_monthly_with_anchor_clamps_only_the_month(
    old: str, day: int, today: str, new: str
) -> None:
    assert (
        mod.next_monthly(date.fromisoformat(old), date.fromisoformat(today), day)
        == date.fromisoformat(new)
    )


@pytest.mark.parametrize(
    ("deadline", "day"),
    [
        ("2027-03-15", "31"),  # anchor disagrees with the deadline
        ("2027-03-30", "31"),  # March has a 31st
        ("2027-02-28", "27"),
        ("2027-01-31", "32"),
        ("2027-01-31", "0"),
        ("2027-01-31", "x"),
        ("2027-01-31", "31, cadence day 31"),  # duplicate anchor
    ],
)
def test_bad_cadence_anchor_fails_closed(tmp_path: Path, deadline: str, day: str) -> None:
    original = _monthly_state(deadline, day, weekly="2027-06-04")
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, "2027-06-01")
    assert result.returncode == 2
    assert b"cadence day" in result.stderr
    assert _read(state) == original


def test_anchor_is_validated_even_when_nothing_is_due(tmp_path: Path) -> None:
    # A heading the roller cannot read is reported on every run, not only on
    # the day a roll falls due.
    original = _monthly_state("2027-03-15", "31", weekly="2027-03-05")
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, "2027-03-01")
    assert result.returncode == 2
    assert _read(state) == original


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
    assert "](../../../../../../up.md)" in archived
    assert "](../up.md)" not in archived
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
        "[abs](/root.md) [up](../../../../../../p.md) [http](http://x.y) [https](https://x.y) "
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
    new_state, new_archive, _ = mod.plan(
        state_before, archive_before, today, state.parent, archive.parent
    )

    real_replace = mod._replace

    target = state if failing == "state" else archive

    def failing_replace(path: Path, text: str) -> None:
        if path == target:
            raise mod.StateRollError(f"simulated {failing} write failure")
        real_replace(path, text)

    monkeypatch.setattr(mod, "_replace", failing_replace)
    with pytest.raises(mod.StateRollError):
        mod.commit(state, archive, state_before, archive_before, new_state, new_archive)
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
    assert not list(tmp_path.rglob("*.state_roll.tmp"))
    assert not mod.lock_path(state).exists()


# --- Codex review on 861b363 ------------------------------------------------


def _state_bytes(state: Path, archive: Path) -> tuple[bytes, bytes]:
    return state.read_bytes(), archive.read_bytes()


@pytest.mark.parametrize("retry_day", [TODAY, "2026-09-27"])
def test_retry_after_archive_written_but_state_not_does_not_duplicate(
    tmp_path: Path, retry_day: str
) -> None:
    # 4110271923: a kill between the archive write and the STATE write leaves
    # the overflow rows in both files; the retry must not archive them twice.
    rows = _rows(17)
    state, archive = _pair(tmp_path, _state(rows=rows))
    _, new_archive, _ = mod.plan(
        _read(state), _read(archive), date.fromisoformat(TODAY), state.parent, archive.parent
    )
    assert new_archive is not None
    archive.write_text(new_archive, encoding="utf-8", newline="")  # STATE write "lost"

    retry = _run(state, archive, retry_day)
    assert retry.returncode == 0, retry.stderr
    archived = _read(archive)
    for i in (15, 16):
        assert archived.count(f"— decision {i} ") == 1
    assert all(row not in _read(state) for row in rows[15:])
    assert all(row in _read(state) for row in rows[:15])
    # The retry now converges: a third run changes nothing.
    before = _state_bytes(state, archive)
    third = _run(state, archive, retry_day)
    assert third.returncode == 0, third.stderr
    assert _out(third) == "state-roll: nothing to roll\n"
    assert _state_bytes(state, archive) == before


def test_retry_after_partial_archive_adds_only_new_rows(tmp_path: Path) -> None:
    rows = _rows(17)
    state, archive = _pair(tmp_path, _state(rows=rows))
    _, new_archive, _ = mod.plan(
        _read(state), _read(archive), date.fromisoformat(TODAY), state.parent, archive.parent
    )
    assert new_archive is not None
    archive.write_text(new_archive, encoding="utf-8", newline="")
    # A fresh decision lands before the retry, pushing one more row off.
    fresh = _rows(1, newest=date(2026, 9, 28))
    text = _read(state)
    state.write_text(
        text.replace(rows[0] + "\n", fresh[0] + "\n" + rows[0] + "\n", 1),
        encoding="utf-8",
        newline="",
    )
    retry = _run(state, archive, TODAY)
    assert retry.returncode == 0, retry.stderr
    archived = _read(archive)
    for i in (14, 15, 16):
        assert archived.count(f"— decision {i} ") == 1
    assert archived.count(ROLLED_HEADER) == 1
    block = archived.split(ROLLED_HEADER)[1].split("**Seventeenth roll")[0]
    assert block.index("decision 14 ") < block.index("decision 15 ")


def test_monthly_day_above_28_blocks_the_whole_invocation(tmp_path: Path) -> None:
    # 4110271925: the fail-closed Monthly refusal also withholds the Weekly roll
    # and the keep-15 archive of the same invocation; nothing is half-applied.
    state, archive = _pair(
        tmp_path, _state(weekly="2026-10-30", monthly="2026-10-31", rows=_rows(17))
    )
    before = _state_bytes(state, archive)
    for extra in ((), ("--check",)):
        result = _run(state, archive, "2026-11-01", *extra)
        assert result.returncode == 2
        assert b"cadence day NN" in result.stderr
        assert b"rerun" in result.stderr
        assert _state_bytes(state, archive) == before


def test_rebases_parent_and_dot_relative_targets() -> None:
    # 4110271931: every filesystem-relative target is recomputed from STATE's
    # directory to the archive's; schemes, root-absolute and pure anchors stay.
    row = (
        "- **2026-09-09** — [up](../sibling/x.md#f) [dot](./docs/a.md) "
        "[titled](docs/b.md \"t\") [ftp](ftp://h/x) [q](?x=1)"
    )
    assert mod.rewrite_links(row) == (
        "- **2026-09-09** — [up](../../../../../../sibling/x.md#f) "
        "[dot](../../../../../docs/a.md) [titled](../../../../../docs/b.md \"t\") "
        "[ftp](ftp://h/x) [q](?x=1)"
    )


def test_rebase_from_state_and_archive_positions() -> None:
    root = Path("/repo")
    assert (
        mod.rewrite_links("- **2026-09-09** — [a](docs/a.md)", root, root / "x")
        == "- **2026-09-09** — [a](../docs/a.md)"
    )


def test_angle_bracket_link_target_fails_closed() -> None:
    with pytest.raises(mod.StateRollError):
        mod.rewrite_links("- **2026-09-09** — [a](<docs/a b.md>)")


def test_weekly_heading_without_rolling_prefix_rolls(tmp_path: Path) -> None:
    # 4110271936: the roller accepts whatever check_state_currency accepts.
    original = _state().replace(
        WEEKLY_HEADING.format(deadline="2026-09-25", bucket="09-21→09-25"),
        "### Weekly — recurring (next deadline **2026-09-25**, bucket "
        "09-21→09-25; venue idle clock)",
    )
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    assert _out(result) == "weekly: 2026-09-25 -> 2026-10-02\n"
    assert _read(state) == original.replace(
        "**2026-09-25**, bucket 09-21→09-25;", "**2026-10-02**, bucket 09-28→10-02;"
    )


def test_weekly_heading_without_bucket_rolls_deadline_only(tmp_path: Path) -> None:
    original = _state().replace(
        WEEKLY_HEADING.format(deadline="2026-09-25", bucket="09-21→09-25"),
        "### Weekly — recurring (rolling; next deadline **2026-09-25**)",
    )
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    assert _read(state) == original.replace("**2026-09-25**)", "**2026-10-02**)")


def test_weekly_heading_with_unparseable_bucket_fails_closed(tmp_path: Path) -> None:
    broken = _state(bucket="x")
    state, archive = _pair(tmp_path, broken)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"bucket" in result.stderr
    assert _read(state) == broken


def test_duplicate_weekly_heading_fails_closed(tmp_path: Path) -> None:
    broken = _state() + (
        "\n### Weekly — recurring (rolling; next deadline **2026-09-18**)\n"
    )
    state, archive = _pair(tmp_path, broken)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"duplicate" in result.stderr
    assert _read(state) == broken


def test_monthly_heading_with_trailing_text_rolls(tmp_path: Path) -> None:
    original = _state(weekly="2026-10-23").replace(
        "### Monthly — recurring (rolling; next deadline **2026-10-21**)",
        "### Monthly — recurring (next deadline **2026-10-21**, ledger reconfirm)",
    )
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, "2026-10-01")
    assert result.returncode == 0, result.stderr
    assert _out(result) == "state-roll: nothing to roll\n"
    result = _run(state, archive, "2026-10-22")
    assert result.returncode == 0, result.stderr
    assert "### Monthly — recurring (next deadline **2026-11-21**, ledger reconfirm)" in (
        _read(state)
    )


def test_heading_regexes_match_the_currency_checker() -> None:
    spec = importlib.util.spec_from_file_location(
        "check_state_currency", REPO / "scripts" / "check_state_currency.py"
    )
    checker = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(checker)
    assert mod.RECURRING_HEADING_RE.pattern == checker.RECURRING_HEADING_RE.pattern
    assert mod.DEADLINE_RE.pattern == checker.DEADLINE_RE.pattern
    assert mod.MAX_UNANCHORED_MONTHLY_DAY == checker.MAX_UNANCHORED_MONTHLY_DAY
    assert mod.CADENCE_DAY_RE.pattern == checker.CADENCE_DAY_RE.pattern
    assert mod.FORWARD_SECTION_RE.pattern == checker.FORWARD_SECTION_RE.pattern
    assert mod.DECISION_SECTION_RE.pattern == checker.DECISION_SECTION_RE.pattern


def test_index_out_of_date_order_fails_closed(tmp_path: Path) -> None:
    # 4110271944: keep-15 is positional, so a misordered index would archive a
    # newer row and keep an older one. Refuse instead.
    rows = _rows(17)
    rows[3], rows[16] = rows[16], rows[3]
    broken = _state(rows=rows)
    state, archive = _pair(tmp_path, broken)
    before = _state_bytes(state, archive)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"order" in result.stderr
    assert _state_bytes(state, archive) == before


def test_same_day_rows_keep_document_order(tmp_path: Path) -> None:
    rows = [row.replace(row[4:14], "2026-09-10") for row in _rows(17)]
    state, archive = _pair(tmp_path, _state(rows=rows, weekly=ROLLED_WEEKLY))
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    assert _out(result) == "index: archived 2 row(s)\n"
    assert all(row in _read(state) for row in rows[:15])


def test_dated_bullet_the_roller_cannot_parse_fails_closed(tmp_path: Path) -> None:
    # A dated bullet with another separator is counted by the checker but would
    # be invisible to keep-15; refuse rather than miscount.
    rows = _rows(16)
    rows[5] = rows[5].replace(" — ", " - ", 1)
    broken = _state(rows=rows)
    state, archive = _pair(tmp_path, broken)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert _read(state) == broken


def test_overflow_row_with_continuation_line_fails_closed(tmp_path: Path) -> None:
    # Moving only the first line would split the record between the files.
    rows = _rows(17)
    rows[16] = rows[16] + "\n  continuation of the same decision"
    broken = _state(rows=rows)
    state, archive = _pair(tmp_path, broken)
    before = _state_bytes(state, archive)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"continuation" in result.stderr
    assert _state_bytes(state, archive) == before


# --- Codex 4110350204: continuation after a blank line ----------------------


@pytest.mark.parametrize("position", [15, 16])
def test_overflow_continuation_after_blank_line_fails_closed(
    tmp_path: Path, position: int
) -> None:
    # A one-line lookahead sees only the blank line; the indented continuation
    # would be orphaned in STATE while its row moves to the archive.
    rows = _rows(17)
    rows[position] = rows[position] + "\n\n  continuation of the same decision"
    broken = _state(rows=rows)
    state, archive = _pair(tmp_path, broken)
    before = _state_bytes(state, archive)
    for extra in ((), ("--check",)):
        result = _run(state, archive, TODAY, *extra)
        assert result.returncode == 2
        assert b"continuation" in result.stderr
        assert _state_bytes(state, archive) == before


def test_overflow_followed_by_blank_lines_then_prose_fails_closed(tmp_path: Path) -> None:
    # Whatever follows the blank lines is not a row and not the section end:
    # the roller cannot tell whether it belongs to the moved record.
    rows = _rows(17)
    rows[16] = rows[16] + "\n\n\nloose paragraph"
    broken = _state(rows=rows)
    state, archive = _pair(tmp_path, broken)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert _read(state) == broken


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_blank_separated_overflow_rows_archive_cleanly(
    tmp_path: Path, newline: str
) -> None:
    rows = [row + "\n" for row in _rows(17)]
    original = _state(rows=rows, weekly=ROLLED_WEEKLY).replace("\n", newline)
    state, archive = _pair(tmp_path, original)
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    assert _out(result) == "index: archived 2 row(s)\n"
    # The moved rows take their separating blank lines with them.
    assert _read(state) == _state(rows=rows[:15], weekly=ROLLED_WEEKLY).replace(
        "\n", newline
    )
    archived = _read(archive)
    for row in _rows(17)[15:]:
        assert row.split(" [record]")[0] in archived


# --- Codex 4110350211: duplicate sections -----------------------------------


def test_duplicate_forward_section_fails_closed(tmp_path: Path) -> None:
    # Only the first section would be rolled while the second keeps a stale
    # deadline; refuse instead of reporting a clean roll.
    broken = _state() + (
        "\n## Scheduled forward triggers (continued)\n\n"
        "### Monthly — recurring (rolling; next deadline **2026-08-21**)\n"
    )
    state, archive = _pair(tmp_path, broken)
    for extra in ((), ("--check",)):
        result = _run(state, archive, TODAY, *extra)
        assert result.returncode == 2
        assert b"Scheduled forward triggers" in result.stderr
        assert _read(state) == broken


def test_duplicate_decision_section_fails_closed(tmp_path: Path) -> None:
    broken = _state(rows=_rows(17), weekly=ROLLED_WEEKLY) + (
        "\n## Executed operator decisions — decision index (older)\n\n"
        + "\n".join(_rows(3, newest=date(2026, 8, 1)))
        + "\n"
    )
    state, archive = _pair(tmp_path, broken)
    before = _state_bytes(state, archive)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"Executed operator decisions" in result.stderr
    assert _state_bytes(state, archive) == before


# --- Codex 4110941070 / 4110941072 + uniqueness class sweep -----------------
#
# Every STATE element the roller assumes is unique (sections, recurring
# headings, the deadline field, bucket, cadence anchor, dated index bullets)
# must be exactly one, and a case/spacing near-miss of it fails closed rather
# than being silently ignored. The currency gate shares the roller's parser,
# so a heading the roller refuses also fails the gate (parity pinned below).

CHECKER_SCRIPT = REPO / "scripts" / "check_state_currency.py"
BASE_WEEKLY = WEEKLY_HEADING.format(deadline="2026-09-25", bucket="09-21→09-25")
BASE_MONTHLY = "### Monthly — recurring (rolling; next deadline **2026-10-21**)"
# Nothing is due on PARITY_TODAY for the base _state(): both scripts pass it.
PARITY_TODAY = "2026-09-25"


def _weekly(suffix: str) -> str:
    return _state().replace(BASE_WEEKLY, BASE_WEEKLY[:-1] + suffix + ")")


def _monthly(suffix: str) -> str:
    return _state().replace(BASE_MONTHLY, BASE_MONTHLY[:-1] + suffix + ")")


DEFECTS = {
    # 4110941070: a second deadline field (the roller rolled only the first).
    "weekly-two-deadlines": _weekly("; next deadline **2026-10-02**"),
    "weekly-near-miss-second-deadline": _weekly("; Next Deadline **2026-10-02**"),
    "weekly-unbolded-second-deadline": _weekly("; next deadline 2026-10-02"),
    "monthly-two-deadlines": _monthly(", next deadline **2026-11-21**"),
    "invalid-deadline-date": _state().replace(
        "next deadline **2026-09-25**", "next deadline **2026-09-31**"
    ),
    # Bucket: exactly one, canonical spelling.
    "bucket-case-near-miss": _state().replace("bucket 09-21", "Bucket 09-21"),
    "bucket-malformed": _state().replace("09-21→09-25", "09-21-09-25"),
    "bucket-duplicate": _weekly("; bucket 09-21→09-25"),
    # 4110941072: the anchor as the roller validates it.
    "anchor-case-near-miss": _monthly(", Cadence Day 21"),
    "anchor-hyphen-near-miss": _monthly(", cadence-day 21"),
    "anchor-out-of-range": _monthly(", cadence day 32"),
    "anchor-zero": _monthly(", cadence day 0"),
    "anchor-non-numeric": _monthly(", cadence day x"),
    "anchor-disagrees-with-deadline": _monthly(", cadence day 20"),
    "anchor-duplicate": _monthly(", cadence day 21, cadence day 21"),
    # Recurring headings: exactly one per kind anywhere in STATE.
    "weekly-heading-case-near-miss": _state()
    + "\n### weekly — recurring (rolling; next deadline **2026-09-18**)\n",
    "weekly-heading-outside-forward-section": _state().replace(
        "none.", "none.\n\n### Weekly — recurring (rolling; next deadline **2026-09-18**)"
    ),
    # Section markers: exactly one, near-misses included.
    "forward-section-near-miss": _state() + "\n### Scheduled forward triggers (old)\n",
    "decision-section-near-miss": _state().replace(
        "## Dormant cross-session threads",
        "## executed operator decisions (older)\n\n## Dormant cross-session threads",
    ),
    # Index rows: every dated bullet is a readable row.
    "index-near-miss-bullet": _state(rows=_rows(2) + ["* **2026-09-01** — star bullet"]),
    "index-bad-separator": _state(
        rows=[_rows(2)[0], _rows(2)[1].replace(" — ", " - ", 1)]
    ),
    # 4111057296 (I6): Unicode spacing, zero-width and compatibility forms are
    # normalised before the look-alike test (NFKC + every Unicode whitespace).
    "forward-section-nbsp-near-miss": _state()
    + "\n## Scheduled forward triggers (old)\n",
    "decision-section-ideographic-space-near-miss": _state().replace(
        "## Dormant cross-session threads",
        "##　Executed operator decisions (older)\n\n"
        "## Dormant cross-session threads",
    ),
    "weekly-heading-nbsp-near-miss": _state()
    + "\n### Weekly — recurring (rolling; next deadline **2026-09-18**)\n",
    "monthly-heading-zero-width-near-miss": _state()
    + "\n### Mon​thly — recurring (rolling; next deadline **2026-08-21**)\n",
    "weekly-heading-fullwidth-near-miss": _state()
    + "\n### Ｗｅｅｋｌｙ — recurring (rolling; next deadline **2026-09-18**)\n",
    "deadline-nbsp-second-field": _weekly("; next deadline **2026-10-02**"),
    "bucket-nbsp-near-miss": _state().replace("bucket 09-21", "bucket 09-21"),
    "anchor-en-space-near-miss": _monthly(", cadence day 21"),
    "index-nbsp-bullet": _state(rows=_rows(2) + ["- **2026-09-01** — nbsp bullet"]),
    "index-fullwidth-digit-bullet": _state(
        rows=_rows(2) + ["- **２０２６-09-01** — fullwidth digits"]
    ),
    # Round 5 (Codex on c07cd66). 4111495537: the gate runs the roller's full
    # index validation (newest-first order, overflow continuation lines).
    "index-out-of-date-order": _state(rows=list(reversed(_rows(2)))),
    "index-overflow-continuation": _state(
        rows=_rows(16) + ["  continuation of the sixteenth row", *_rows(17)[16:]]
    ),
    # 4111495542: two rows fused on one line by a lost line break.
    "index-fused-rows": _state(rows=[_rows(2)[0] + " " + _rows(2)[1]]),
    "index-fused-rows-no-space": _state(rows=[_rows(2)[0] + _rows(2)[1]]),
    # 4111495548: the bucket is real month-days and the deadline's Mon-Fri week.
    "bucket-impossible-dates": _state(bucket="99-99→99-99"),
    "bucket-impossible-day": _state(bucket="09-21→09-31"),
    "bucket-wrong-week": _state(bucket="09-14→09-18"),
    "bucket-not-monday-to-friday": _state(bucket="09-22→09-25"),
}


def _roller_check(state_text: str, tmp_path: Path) -> subprocess.CompletedProcess:
    state, archive = _pair(tmp_path, state_text)
    return _run(state, archive, PARITY_TODAY, "--check")


def _gate(state_text: str, tmp_path: Path) -> subprocess.CompletedProcess:
    state = tmp_path / "GATE_STATE.md"
    state.write_text(state_text, encoding="utf-8", newline="")
    env = os.environ.copy()
    env["STATE_CURRENCY_TODAY"] = PARITY_TODAY
    return subprocess.run(
        [sys.executable, str(CHECKER_SCRIPT), "--state", str(state)],
        cwd=REPO,
        env=env,
        capture_output=True,
    )


def test_parity_baseline_passes_both(tmp_path: Path) -> None:
    roller = _roller_check(_state(), tmp_path)
    assert roller.returncode == 0, roller.stderr
    gate = _gate(_state(), tmp_path)
    assert gate.returncode == 0, gate.stderr


@pytest.mark.parametrize("name", sorted(DEFECTS))
def test_uniqueness_defect_fails_closed_in_roller(tmp_path: Path, name: str) -> None:
    broken = DEFECTS[name]
    assert broken != _state(), name  # the transform actually changed the text
    state, archive = _pair(tmp_path, broken)
    before = _state_bytes(state, archive)
    # TODAY has a due Weekly roll; the defect withholds it and everything else.
    for extra in ((), ("--check",)):
        result = _run(state, archive, TODAY, *extra)
        assert result.returncode == 2, (name, result.stdout, result.stderr)
        assert result.stderr.startswith(b"state-roll: FAIL")
        assert _state_bytes(state, archive) == before


@pytest.mark.parametrize("name", sorted(DEFECTS))
def test_gate_fails_where_roller_refuses(tmp_path: Path, name: str) -> None:
    # 4110941072: a heading the roller refuses must not pass the gate. Both
    # run on a day with nothing due, so only the defect can fail them.
    roller = _roller_check(DEFECTS[name], tmp_path)
    assert roller.returncode == 2, (name, roller.stdout, roller.stderr)
    gate = _gate(DEFECTS[name], tmp_path)
    assert gate.returncode == 1, (name, gate.stdout, gate.stderr)
    assert b"state-currency: FAIL" in gate.stderr


def test_two_deadline_fields_names_the_field(tmp_path: Path) -> None:
    result = _roller_check(DEFECTS["weekly-two-deadlines"], tmp_path)
    assert b"next deadline" in result.stderr


def test_currency_gate_uses_the_roller_parser() -> None:
    spec = importlib.util.spec_from_file_location("check_state_currency", CHECKER_SCRIPT)
    checker = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(checker)
    assert Path(checker.ROLLER.__file__).resolve() == SCRIPT.resolve()
    fields = checker.ROLLER.recurring_fields(_state())[1]
    assert [kind for kind, *_ in checker.recurring_headings(_state())] == list(fields)


# --- archive side: today's header, header order, line endings ---------------


def _archive_with(before_seventeenth: str) -> str:
    return _archive().replace(
        "**Seventeenth roll, 2026-09-25**",
        before_seventeenth + "**Seventeenth roll, 2026-09-25**",
        1,
    )


ARCHIVE_DEFECTS = {
    # Today's automated header twice: which block is "today's" is ambiguous.
    "duplicate-today-header": _archive_with(
        ROLLED_HEADER + "\n\n- **2026-09-04** — x\n\n"
        + ROLLED_HEADER + "\n\n- **2026-09-04** — y\n\n"
    ),
    # Today's header exists below another header: inserting a new copy on top
    # would write a duplicate header.
    "today-header-not-newest": _archive_with(
        "**Eighteenth roll, 2026-09-26** (one entry):\n\n- **2026-09-04** — hand\n\n"
        + ROLLED_HEADER + "\n\n- **2026-09-04** — auto\n\n"
    ),
    # The first header is taken as the newest; out-of-order headers break that.
    "headers-out-of-date-order": _archive().replace(
        "Sixteenth roll, 2026-09-24", "Sixteenth roll, 2026-09-27"
    ),
    # One line ending is chosen for the inserted block; mixed input is ambiguous.
    "mixed-line-endings": _archive().replace("\n", "\r\n", 1),
}


@pytest.mark.parametrize("name", sorted(ARCHIVE_DEFECTS))
def test_archive_defect_fails_closed(tmp_path: Path, name: str) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)), ARCHIVE_DEFECTS[name])
    before = _state_bytes(state, archive)
    for extra in ((), ("--check",)):
        result = _run(state, archive, TODAY, *extra)
        assert result.returncode == 2, (name, result.stdout, result.stderr)
        assert _state_bytes(state, archive) == before


@pytest.mark.parametrize("name", sorted(ARCHIVE_DEFECTS))
def test_archive_defect_blocks_even_a_weekly_only_roll(tmp_path: Path, name: str) -> None:
    # The pre-state is validated whole before any plan: a corrupt archive
    # withholds a due Weekly roll even when no row needs archiving.
    state, archive = _pair(tmp_path, _state(), ARCHIVE_DEFECTS[name])
    before = _state_bytes(state, archive)
    for extra in ((), ("--check",)):
        result = _run(state, archive, TODAY, *extra)
        assert result.returncode == 2, (name, result.stdout, result.stderr)
        assert _state_bytes(state, archive) == before


# --- Round 4 (Codex on bfcc8fb): rebuilt from invariants I1-I6 ---------------
#
# One test per finding, then one per invariant. The invariants are written in
# the state_roll.py module docstring; validate() is the single checker.


def _archive_lines(*lines: str) -> str:
    return "\n".join(["# archive", "", "intro.", "", *lines, ""])


# I6 / 4111057296 -------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "key"),
    [
        ("## Scheduled  forward\ttriggers", "## scheduled forward triggers"),
        ("###　Weekly — recurring", "### weekly — recurring"),
        ("**Roll 2026-09-26**  \r", "**roll 2026-09-26**"),
        ("Next​Deadline", "nextdeadline"),
        ("ｎｅｘｔ deadline", "next deadline"),
        ("  - **２０２６-09-01**", "- **2026-09-01**"),
        ("", ""),
    ],
)
def test_lookalike_key_normalises_unicode(raw: str, key: str) -> None:
    assert mod.lookalike_key(raw) == key


def test_both_scripts_share_the_lookalike_helper() -> None:
    spec = importlib.util.spec_from_file_location("check_state_currency", CHECKER_SCRIPT)
    checker = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(checker)
    assert checker.lookalike_key.__module__ == checker.ROLLER.__name__
    assert checker.lookalike_key("**Last Curated:**") == "**last curated:**"


# 4111057285: --today older than the newest archive header --------------------


@pytest.mark.parametrize(
    ("archive_text", "today"),
    [
        (_archive(), "2026-09-20"),  # newest header: Seventeenth roll, 2026-09-25
        (
            _archive_with(
                "**Roll 2026-09-27** (automated keep-15 roll; `scripts/state_roll.py`):"
                "\n\n- **2026-09-04** — later block\n\n"
            ),
            TODAY,
        ),
    ],
)
def test_today_older_than_newest_archive_header_refuses(
    tmp_path: Path, archive_text: str, today: str
) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17), weekly="2026-10-02"), archive_text)
    before = _state_bytes(state, archive)
    for extra in ((), ("--check",)):
        result = _run(state, archive, today, *extra)
        assert result.returncode == 2, (result.stdout, result.stderr)
        assert b"older than" in result.stderr
        assert _state_bytes(state, archive) == before


# 4111057294: today's header recognised by its date key ------------------------


@pytest.mark.parametrize(
    "variant",
    [
        ROLLED_HEADER + "  ",  # trailing spaces
        "**Roll 2026-09-26** (edited suffix):",
        "**Roll 2026-09-26** (automated keep-15 roll; `scripts/state_roll.py`):",
        "**roll 2026-09-26**",
    ],
)
def test_today_header_is_recognised_by_date_key(tmp_path: Path, variant: str) -> None:
    rows = _rows(17)
    archive_text = _archive_with(variant + "\n\n- **2026-09-04** — earlier today\n\n")
    state, archive = _pair(tmp_path, _state(rows=rows), archive_text)
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    archived = _read(archive)
    parsed = mod.parse_archive(archived)
    assert [h.day.isoformat() for h in parsed.headers].count(TODAY) == 1
    assert archived.count(variant + "\n") == 1  # the header line is untouched
    block = archived.split(variant + "\n", 1)[1].split("**Seventeenth roll")[0]
    assert block == (
        "\n"
        + "".join(mod.rewrite_links(row) + "\n\n" for row in rows[15:])
        + "- **2026-09-04** — earlier today\n\n"
    )


def test_hand_written_header_for_today_is_not_extended(tmp_path: Path) -> None:
    # Date key identity: the roller neither writes a second header for a date
    # that has one nor adds rows under a hand-written (counted) block.
    archive_text = _archive_with(
        "**Eighteenth roll, 2026-09-26** (one entry):\n\n- **2026-09-04** — by hand\n\n"
    )
    state, archive = _pair(tmp_path, _state(rows=_rows(17)), archive_text)
    before = _state_bytes(state, archive)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"hand-written" in result.stderr
    assert _state_bytes(state, archive) == before


# 4111057290: missing final newline --------------------------------------------


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_today_header_as_final_line_without_newline(tmp_path: Path, newline: str) -> None:
    rows = _rows(17)
    head = _archive_lines().replace("\n", newline)
    state, archive = _pair(
        tmp_path, _state(rows=rows).replace("\n", newline), head + ROLLED_HEADER
    )
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    expected = head + (
        ROLLED_HEADER
        + "\n\n"
        + "".join(mod.rewrite_links(row) + "\n\n" for row in rows[15:])
    ).replace("\n", newline)
    assert _read(archive) == expected
    mod.parse_archive(_read(archive))


def test_last_row_without_final_newline_keeps_whole_rows(tmp_path: Path) -> None:
    rows = _rows(17)
    original = _archive().rstrip("\n")
    state, archive = _pair(tmp_path, _state(rows=rows), original)
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    archived = _read(archive)
    assert archived.endswith("- **2026-09-02** — older archived row\n")
    assert len(mod.parse_archive(archived).rows) == 5


# 4111057288 / I4: one mutator, unique temp files, guarded rollback -----------


def test_second_invocation_while_lock_held_fails_closed(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    before = _state_bytes(state, archive)
    with mod.roll_lock(state) as lock:
        held = lock.read_bytes()
        result = _run(state, archive, TODAY)
        assert result.returncode == 2
        assert b"lock" in result.stderr
        assert _state_bytes(state, archive) == before
        assert lock.read_bytes() == held  # never stolen
    assert not lock.exists()
    assert _run(state, archive, TODAY).returncode == 0


def test_stale_lock_is_never_stolen(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    lock = mod.lock_path(state)
    lock.write_bytes(b"pid 1 (dead)\n")
    before = _state_bytes(state, archive)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert str(lock.name).encode() in result.stderr
    assert b"delete" in result.stderr
    assert lock.read_bytes() == b"pid 1 (dead)\n"
    assert _state_bytes(state, archive) == before


def test_lock_is_released_after_a_refusal(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)), ARCHIVE_DEFECTS["mixed-line-endings"])
    assert _run(state, archive, TODAY).returncode == 2
    assert not mod.lock_path(state).exists()


def _flaky_unlink(
    monkeypatch: pytest.MonkeyPatch, lock: Path, failures: int
) -> list[str]:
    # Windows: while any other handle is open on the lock, unlink raises a
    # sharing violation (PermissionError). The first run of the parallel test
    # hit this when refused runs read the lock to name its holder.
    real_unlink = os.unlink
    calls: list[str] = []

    def unlink(path, *args, **kwargs):  # type: ignore[no-untyped-def]
        if Path(path) == lock and len(calls) < failures:
            calls.append(str(path))
            raise PermissionError(13, "sharing violation (simulated)", str(path))
        return real_unlink(path, *args, **kwargs)

    monkeypatch.setattr(mod.os, "unlink", unlink)
    monkeypatch.setattr(mod.time, "sleep", lambda _seconds: None)
    return calls


def test_lock_release_retries_a_transient_sharing_violation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "STATE.md"
    state.write_bytes(b"x")
    lock = mod.lock_path(state)
    calls = _flaky_unlink(monkeypatch, lock, failures=3)
    with mod.roll_lock(state):
        pass
    assert len(calls) == 3
    assert not lock.exists()


def test_lock_that_cannot_be_released_fails_loudly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "STATE.md"
    state.write_bytes(b"x")
    lock = mod.lock_path(state)
    _flaky_unlink(monkeypatch, lock, failures=10**6)
    with pytest.raises(mod.StateRollError, match="delete the lock by hand"):
        with mod.roll_lock(state):
            pass
    assert lock.exists()
    # A body error and a release error are both reported.
    monkeypatch.undo()
    lock.unlink()
    _flaky_unlink(monkeypatch, lock, failures=10**6)
    with pytest.raises(mod.StateRollError, match="body failed.*delete the lock by hand"):
        with mod.roll_lock(state):
            raise mod.StateRollError("body failed")
    monkeypatch.undo()
    lock.unlink()


def test_refused_run_does_not_open_the_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Only the owner may open the lock file (see _flaky_unlink).
    state = tmp_path / "STATE.md"
    state.write_bytes(b"x")
    lock = mod.lock_path(state)
    with mod.roll_lock(state):
        real_open = open
        opened: list[str] = []

        def spy(file, *args, **kwargs):  # type: ignore[no-untyped-def]
            opened.append(str(file))
            return real_open(file, *args, **kwargs)

        monkeypatch.setattr("builtins.open", spy)
        with pytest.raises(mod.StateRollError, match="exists"):
            with mod.roll_lock(state):
                pass
        monkeypatch.undo()
        assert str(lock) not in opened
    assert not lock.exists()


def test_check_reads_without_the_lock(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    with mod.roll_lock(state):
        result = _run(state, archive, TODAY, "--check")
    assert result.returncode == 1, result.stderr


def test_foreign_file_at_the_old_fixed_temp_path_is_untouched(tmp_path: Path) -> None:
    # The old fixed `<name>.state_roll.tmp` was shared by every run; each write
    # now gets its own mkstemp file in the target directory.
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    foreign = [p.with_name(p.name + ".state_roll.tmp") for p in (state, archive)]
    for path in foreign:
        path.write_bytes(b"another writer's bytes")
    result = _run(state, archive, TODAY)
    assert result.returncode == 0, result.stderr
    for path in foreign:
        assert path.read_bytes() == b"another writer's bytes"
    assert len(list(tmp_path.rglob("*.state_roll.tmp"))) == 2


def test_rollback_never_overwrites_an_archive_changed_by_someone_else(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    state_before, archive_before = _read(state), _read(archive)
    planned = mod.plan(
        state_before, archive_before, date.fromisoformat(TODAY), state.parent, archive.parent
    )
    assert planned.archive is not None
    foreign = planned.archive + "foreign edit\n"
    real_replace = mod._replace

    def replace(path: Path, text: str) -> None:
        if path == state:
            archive.write_text(foreign, encoding="utf-8", newline="")
            raise mod.StateRollError("simulated STATE write failure")
        real_replace(path, text)

    monkeypatch.setattr(mod, "_replace", replace)
    with pytest.raises(mod.StateRollError, match="not restored"):
        mod.commit(
            state, archive, state_before, archive_before, planned.state, planned.archive
        )
    assert _read(archive) == foreign
    assert _read(state) == state_before


def test_commit_refuses_files_changed_after_planning(tmp_path: Path) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    state_before, archive_before = _read(state), _read(archive)
    planned = mod.plan(
        state_before, archive_before, date.fromisoformat(TODAY), state.parent, archive.parent
    )
    edited = state_before.replace("none.", "edited meanwhile.")
    state.write_text(edited, encoding="utf-8", newline="")
    with pytest.raises(mod.StateRollError, match="changed"):
        mod.commit(
            state, archive, state_before, archive_before, planned.state, planned.archive
        )
    assert _read(state) == edited
    assert _read(archive) == archive_before


CRASH_DRIVER = """
import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("state_roll", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
real_replace = mod._replace
state = os.path.abspath(sys.argv[2])

def crash(path, text):
    if os.path.abspath(path) == state:
        os._exit(9)  # the process dies after the archive write, before STATE
    real_replace(path, text)

mod._replace = crash
sys.exit(mod.main(["--state", sys.argv[2], "--archive", sys.argv[3], "--today", sys.argv[4]]))
"""


def _row_union(state_text: str, archive_text: str, state: Path, archive: Path) -> set[str]:
    snap = mod.validate(state_text, archive_text, state.parent, archive.parent)
    return set(snap.state_rows) | set(snap.archive.rows)


def test_crash_between_writes_recovers_without_loss_or_duplication(tmp_path: Path) -> None:
    rows = _rows(17)
    state, archive = _pair(tmp_path, _state(rows=rows))
    state_before, archive_before = _read(state), _read(archive)
    union_before = _row_union(state_before, archive_before, state, archive)
    driver = tmp_path / "crash_driver.py"
    driver.write_text(CRASH_DRIVER, encoding="utf-8")
    env = os.environ.copy()
    env.pop("STATE_CURRENCY_TODAY", None)
    crashed = subprocess.run(
        [sys.executable, str(driver), str(SCRIPT), str(state), str(archive), TODAY],
        cwd=REPO,
        env=env,
        capture_output=True,
    )
    assert crashed.returncode == 9, crashed.stderr
    assert _read(state) == state_before
    assert _read(archive) != archive_before
    # The crashed pair is a state the validator accepts (residue rows in both).
    assert _row_union(_read(state), _read(archive), state, archive) == union_before

    lock = mod.lock_path(state)
    assert lock.exists()  # a dead run's lock is never stolen
    blocked_bytes = _state_bytes(state, archive)
    blocked = _run(state, archive, TODAY)
    assert blocked.returncode == 2
    assert b"lock" in blocked.stderr
    assert _state_bytes(state, archive) == blocked_bytes

    lock.unlink()  # the operator clears it by hand after checking no run is live
    retry = _run(state, archive, TODAY)
    assert retry.returncode == 0, retry.stderr
    final_state, final_archive = _read(state), _read(archive)
    snap = mod.validate(final_state, final_archive, state.parent, archive.parent)
    assert set(snap.state_rows) | set(snap.archive.rows) == union_before
    assert not set(snap.state_rows) & set(snap.archive.rows)
    for i in (15, 16):
        assert final_archive.count(f"— decision {i} ") == 1
    third = _run(state, archive, TODAY)
    assert third.returncode == 0, third.stderr
    assert _out(third) == "state-roll: nothing to roll\n"


def test_parallel_runs_lose_and_duplicate_nothing(tmp_path: Path) -> None:
    # Race-sized: many contenders at once. Each either rolls, finds nothing to
    # roll, or is refused by the lock; the final pair always validates.
    rows = _rows(20)
    state, archive = _pair(tmp_path, _state(rows=rows))
    union_before = _row_union(_read(state), _read(archive), state, archive)
    env = os.environ.copy()
    env.pop("STATE_CURRENCY_TODAY", None)
    command = [
        sys.executable, str(SCRIPT), "--state", str(state), "--archive", str(archive),
        "--today", TODAY,
    ]
    procs = [
        subprocess.Popen(command, cwd=REPO, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(8)
    ]
    results = []
    for proc in procs:
        out, err = proc.communicate(timeout=120)
        results.append((proc.returncode, out, err))
    for code, _, err in results:
        assert code in (0, 2), err
        if code == 2:
            # Refused by the held lock, not failing for another reason whose
            # message merely names the lock path.
            assert b"exists: another state_roll run" in err, err
    assert any(code == 0 for code, _, _ in results)
    if not all(code == 0 for code, _, _ in results):
        assert _run(state, archive, TODAY).returncode == 0  # a refused run retries cleanly
    snap = mod.validate(_read(state), _read(archive), state.parent, archive.parent)
    assert set(snap.state_rows) | set(snap.archive.rows) == union_before
    assert not set(snap.state_rows) & set(snap.archive.rows)
    assert len(snap.state_rows) == 15
    assert not mod.lock_path(state).exists()


# I1-I3 / I5: the one validator, on the pre-state and the composed post-state --


def test_validator_accepts_the_real_state_and_archive() -> None:
    # The legacy archive has same-date ordinal headers and a `**First roll,
    # 2026-08-23:**` header; both are valid under I2.
    snap = mod.validate(
        _read(REPO / "STATE.md"), _read(mod.DEFAULT_ARCHIVE), REPO, mod.DEFAULT_ARCHIVE.parent
    )
    assert snap.archive.headers
    assert not set(snap.state_rows) & set(snap.archive.rows)


def test_validator_i1_row_conservation() -> None:
    state_text, archive_text = _state(rows=_rows(17)), _archive()
    before = mod.validate(state_text, archive_text)
    planned = mod.plan(state_text, archive_text, date.fromisoformat(TODAY))
    assert planned.archive is not None
    mod.validate(planned.state, planned.archive, before=before)
    extra = _archive_with("").replace(
        "- **2026-09-02** — older archived row", "- **2026-09-02** — older archived row\n\n"
        "- **2026-09-01** — invented"
    )
    cases = {
        "lost": (planned.state, archive_text),
        "in-both": (state_text, planned.archive),
        "invented": (state_text, extra),
        "state-gained": (_state(rows=_rows(18)), archive_text),
    }
    for name, (state_after, archive_after) in cases.items():
        with pytest.raises(mod.StateRollError, match="I1"):
            mod.validate(state_after, archive_after, before=before)
            pytest.fail(name)


def test_validator_accepts_interrupted_run_residue() -> None:
    # Residue (overflow rows in both files) is the one duplicate the roller
    # removes, and only from STATE.
    state_text, archive_text = _state(rows=_rows(17)), _archive()
    planned = mod.plan(state_text, archive_text, date.fromisoformat(TODAY))
    assert planned.archive is not None
    residue = mod.validate(state_text, planned.archive)
    retried = mod.plan(state_text, planned.archive, date.fromisoformat(TODAY))
    assert retried.archive is None
    mod.validate(retried.state, planned.archive, before=residue)


VALID_LEGACY_ARCHIVE = _archive_lines(
    "**Thirteenth roll, 2026-09-03** (one entry):",
    "",
    "- **2026-08-24** — a",
    "",
    "**Twelfth roll, 2026-09-03** (one entry):",
    "",
    "- **2026-08-23** — b",
    "",
    "**First roll, 2026-08-23:**",
    "",
    "- **2026-08-01** — c",
    "- **2026-07-01** — d",
)


def test_parse_archive_reads_legacy_headers() -> None:
    parsed = mod.parse_archive(VALID_LEGACY_ARCHIVE)
    assert [(h.day.isoformat(), h.automated) for h in parsed.headers] == [
        ("2026-09-03", False),
        ("2026-09-03", False),
        ("2026-08-23", False),
    ]
    assert len(parsed.rows) == 4


I2_DEFECTS = {
    "automated-shares-date-with-ordinal": _archive_lines(
        "**Roll 2026-09-03** (automated):", "", "- **2026-08-25** — x", "",
        "**Thirteenth roll, 2026-09-03** (one entry):", "", "- **2026-08-24** — a",
    ),
    "automated-below-same-date-ordinal": _archive_lines(
        "**Thirteenth roll, 2026-09-03** (one entry):", "", "- **2026-08-24** — a", "",
        "**Roll 2026-09-03** (automated):", "", "- **2026-08-23** — x",
    ),
    "two-automated-same-date": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-24** — a", "",
        "**Roll 2026-09-03** (again)", "", "- **2026-08-23** — b",
    ),
    "out-of-order": _archive_lines(
        "**Roll 2026-09-01**", "", "- **2026-08-24** — a", "",
        "**Roll 2026-09-03**", "", "- **2026-08-23** — b",
    ),
    "row-above-first-header": _archive_lines(
        "- **2026-08-25** — stray", "", "**Roll 2026-09-03**", "", "- **2026-08-24** — a",
    ),
    "prose-inside-a-block": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-24** — a", "", "loose paragraph",
    ),
    "continuation-line": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-24** — a", "  continued",
    ),
    "header-fused-with-row": _archive_lines(
        "**Roll 2026-09-03** (x):- **2026-08-25** — fused", "", "- **2026-08-24** — a",
    ),
    "unreadable-header-lookalike": _archive_lines(
        "**Nineteenth roll 2026-09-03**", "", "- **2026-08-24** — a",
    ),
    "invalid-header-date": _archive_lines("**Roll 2026-02-30**", "", "- **2026-01-24** — a"),
    "duplicate-row": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-24** — a", "", "- **2026-08-24** — a",
    ),
    "lookalike-row": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-24** — a", "", "* **2026-08-23** — star",
    ),
    "nbsp-lookalike-row": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-23** — nbsp",
    ),
    "mixed-line-endings": VALID_LEGACY_ARCHIVE.replace("\n", "\r\n", 1),
    "lone-cr": VALID_LEGACY_ARCHIVE.replace("\n", "\r", 1),
    # Round 5, 4111495542: two rows fused on one line.
    "rows-fused": _archive_lines(
        "**Roll 2026-09-03**", "", "- **2026-08-24** — a - **2026-08-23** — b",
    ),
    # Round 5, 4111495545: two roll headers fused on one line.
    "automated-headers-fused": _archive_lines(
        "**Roll 2026-09-03** (x) **Roll 2026-09-02** (y)", "", "- **2026-08-24** — a",
    ),
    "ordinal-headers-fused": _archive_lines(
        "**Thirteenth roll, 2026-09-03** (one entry):**Twelfth roll, 2026-09-02** "
        "(one entry):",
        "",
        "- **2026-08-24** — a",
    ),
    "headers-fused-case-variant": _archive_lines(
        "**Roll 2026-09-03** (x) **ROLL 2026-09-02**", "", "- **2026-08-24** — a",
    ),
}


@pytest.mark.parametrize("name", sorted(I2_DEFECTS))
def test_parse_archive_refuses_i2_i3_i5_defects(name: str) -> None:
    with pytest.raises(mod.StateRollError):
        mod.parse_archive(I2_DEFECTS[name])


@pytest.mark.parametrize("defect", ["mixed", "lone-cr"])
def test_state_line_ending_defect_fails_closed(tmp_path: Path, defect: str) -> None:
    text = _state(rows=_rows(17))
    broken = (
        text.replace("\n", "\r\n", 1) if defect == "mixed" else text.replace("\n", "\r", 1)
    )
    state, archive = _pair(tmp_path, broken)
    before = _state_bytes(state, archive)
    result = _run(state, archive, TODAY)
    assert result.returncode == 2
    assert b"line ending" in result.stderr
    assert _state_bytes(state, archive) == before


def _drop_one(real):  # type: ignore[no-untyped-def]
    return lambda archive, rows, today: real(archive, rows[:1], today)


def _dup_one(real):  # type: ignore[no-untyped-def]
    return lambda archive, rows, today: real(archive, rows + rows[:1], today)


def _misorder(real):  # type: ignore[no-untyped-def]
    def compose(archive, rows, today):  # type: ignore[no-untyped-def]
        text, message = real(archive, rows, today)
        start = text.index(ROLLED_HEADER)
        end = text.index("**Seventeenth roll")
        return text[:start] + text[end:] + text[start:end], message

    return compose


def _mixed(real):  # type: ignore[no-untyped-def]
    def compose(archive, rows, today):  # type: ignore[no-untyped-def]
        text, message = real(archive, rows, today)
        return text.replace("\n", "\r\n", 1), message

    return compose


@pytest.mark.parametrize("mutation", [_drop_one, _dup_one, _misorder, _mixed])
def test_post_state_breaking_an_invariant_writes_nothing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    mutation,  # type: ignore[no-untyped-def]
) -> None:
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    before = _state_bytes(state, archive)
    monkeypatch.setattr(mod, "archive_overflow", mutation(mod.archive_overflow))
    code = mod.main(
        ["--state", str(state), "--archive", str(archive), "--today", TODAY]
    )
    assert code == 2
    assert "state-roll: FAIL" in capsys.readouterr().err
    assert _state_bytes(state, archive) == before
    assert not mod.lock_path(state).exists()


# --- Round 5 (Codex on c07cd66) ----------------------------------------------


def test_fused_rows_are_refused_not_read_as_one() -> None:
    # 4111495542: with the newline lost, the second row would ride inside the
    # first and keep-15 would count (and move) both as one record.
    with pytest.raises(mod.StateRollError, match="two index rows"):
        mod.decision_index_rows(DEFECTS["index-fused-rows"])
    with pytest.raises(mod.StateRollError, match="two index rows"):
        mod.parse_archive(I2_DEFECTS["rows-fused"])


def test_fused_headers_are_refused_not_read_as_one() -> None:
    # 4111495545: a second header on the first header's line is a block the
    # date-order and same-date checks would never see.
    for name in ("automated-headers-fused", "ordinal-headers-fused"):
        with pytest.raises(mod.StateRollError, match="two roll headers"):
            mod.parse_archive(I2_DEFECTS[name])


def test_row_mentioning_a_bold_date_is_not_a_fused_row() -> None:
    row = "- **2026-09-24** — supersedes **2026-09-01** (see - 2026-09-01 note)"
    assert len(mod.decision_index_rows(_state(rows=[row]))) == 1


@pytest.mark.parametrize(
    ("deadline", "bucket"),
    [
        ("2026-09-25", "09-21→09-25"),
        ("2027-01-01", "12-28→01-01"),  # the week spans the year end
        ("2028-03-03", "02-28→03-03"),  # leap-year February
    ],
)
def test_bucket_is_the_monday_to_friday_week_of_the_deadline(
    deadline: str, bucket: str
) -> None:
    fields = mod.recurring_fields(_state(weekly=deadline, bucket=bucket))[1]
    assert fields["Weekly"].bucket is not None
    assert mod.week_bucket(date.fromisoformat(deadline)) == (
        date.fromisoformat(deadline) - timedelta(days=4),
        date.fromisoformat(deadline),
    )


def test_bucket_error_names_the_expected_week(tmp_path: Path) -> None:
    result = _roller_check(DEFECTS["bucket-wrong-week"], tmp_path)
    assert result.returncode == 2
    # ASCII arrow: stderr is not UTF-8 on every Windows console.
    assert b"expected 09-21->09-25" in result.stderr


def test_real_state_bucket_matches_its_deadline() -> None:
    fields = mod.recurring_fields(_read(REPO / "STATE.md"))[1]
    weekly = fields["Weekly"]
    assert weekly.bucket is not None
    monday, friday = mod.week_bucket(weekly.deadline_date)
    assert weekly.bucket.groups() == (f"{monday:%m-%d}", f"{friday:%m-%d}")


def _record_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fail_dir: Path | None = None
):  # type: ignore[no-untyped-def]
    state, archive = _pair(tmp_path, _state(rows=_rows(17)))
    state_before, archive_before = _read(state), _read(archive)
    planned = mod.plan(
        state_before, archive_before, date.fromisoformat(TODAY), state.parent, archive.parent
    )
    assert planned.archive is not None
    events: list[tuple[str, Path]] = []
    real_replace = os.replace

    def replace(src: str, dst: str) -> None:
        real_replace(src, dst)
        events.append(("replace", Path(dst)))

    def fsync_dir(directory: Path) -> None:
        events.append(("fsync-dir", Path(directory)))
        if fail_dir is not None and Path(directory) == fail_dir:
            raise OSError("simulated directory fsync failure")

    monkeypatch.setattr(mod.os, "replace", replace)
    monkeypatch.setattr(mod, "_fsync_dir", fsync_dir)
    return state, archive, state_before, archive_before, planned, events


def test_commit_makes_the_archive_rename_durable_before_touching_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # 4111495540: an fsynced temp file does not make the rename durable on
    # POSIX; the directory is fsynced after each replace, archive first.
    state, archive, state_before, archive_before, planned, events = _record_commit(
        tmp_path, monkeypatch
    )
    mod.commit(state, archive, state_before, archive_before, planned.state, planned.archive)
    assert events == [
        ("replace", archive),
        ("fsync-dir", archive.parent),
        ("replace", state),
        ("fsync-dir", state.parent),
    ]


def test_failed_archive_directory_fsync_leaves_state_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state, archive, state_before, archive_before, planned, events = _record_commit(
        tmp_path, monkeypatch, fail_dir=tmp_path / ARCHIVE_SUBDIR
    )
    with pytest.raises(mod.StateRollError, match="durable"):
        mod.commit(
            state, archive, state_before, archive_before, planned.state, planned.archive
        )
    assert ("replace", state) not in events
    assert _read(state) == state_before
    # The pair is the residue state a rerun resolves.
    mod.validate(_read(state), _read(archive), state.parent, archive.parent)


def test_failed_state_directory_fsync_does_not_restore_the_archive(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # STATE was replaced (rows gone from it); restoring the archive now would
    # lose those rows (I1). The post-state is kept and reported.
    state, archive, state_before, archive_before, planned, _ = _record_commit(
        tmp_path, monkeypatch, fail_dir=tmp_path
    )
    with pytest.raises(mod.StateRollError, match="archive was kept"):
        mod.commit(
            state, archive, state_before, archive_before, planned.state, planned.archive
        )
    assert _read(state) == planned.state
    assert _read(archive) == planned.archive


def test_fsync_dir_runs_on_posix_and_is_skipped_elsewhere(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    synced: list[int] = []
    monkeypatch.setattr(mod.os, "fsync", synced.append)
    mod._fsync_dir(tmp_path)
    assert len(synced) == (1 if os.name == "posix" else 0)
