"""STATE.md Last curated / recurring deadline / past dated-section currency."""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_state_currency.py"

_SPEC = importlib.util.spec_from_file_location("check_state_currency", SCRIPT)
mod = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(mod)


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def _state(
    *,
    curated: str = "2026-09-03",
    newest_decision: str = "2026-09-03",
    weekly: str = "2026-09-04",
    monthly: str = "2026-09-21",
    extra_headings: str = "",
) -> str:
    return (
        "# STATE\n\n"
        f"**Last curated:** {curated}\n\n"
        "## OPERATOR QUEUE — strictly ordered, ≤5 live items\n\n"
        "| # | Item | Owner artifact | Blocks |\n"
        "|---|---|---|---|\n"
        "| 1 | F1 | a | b |\n\n"
        "## Executed operator decisions — decision index\n\n"
        f"- **{newest_decision}** — newest.\n"
        "- **2026-08-01** — older.\n\n"
        "## Dormant cross-session threads\n\n"
        "none.\n\n"
        "## Scheduled forward triggers\n\n"
        f"### Weekly — recurring (rolling; next deadline **{weekly}**, bucket 08-31→09-04)\n\n"
        "- **Venue idle-clock.**\n\n"
        f"### Monthly — recurring (rolling; next deadline **{monthly}**)\n\n"
        "- **Ledger reconfirm.**\n\n"
        "### No fixed date / gated\n\n"
        "- **ungated.**\n\n"
        "### 2026-08-08 — DISCHARGED\n\n"
        "done.\n"
        f"{extra_headings}"
    )


def _run(state: Path, today: str) -> int:
    env = os.environ.copy()
    env["STATE_CURRENCY_TODAY"] = today
    return subprocess.call(
        [sys.executable, str(SCRIPT), "--state", str(state)],
        cwd=REPO,
        env=env,
    )


def test_last_curated_behind_index_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(curated="2026-08-31", newest_decision="2026-09-03"),
    )
    assert _run(state, "2026-09-03") == 1


def test_recurring_deadline_yesterday_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(weekly="2026-08-28"),
    )
    assert _run(state, "2026-09-03") == 1


def test_past_dated_heading_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(extra_headings="\n### 2026-08-24 (Monday)\n\n- **this session.**\n"),
    )
    assert _run(state, "2026-09-03") == 1


def test_discharged_past_heading_passes(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state())
    assert _run(state, "2026-09-03") == 0


def test_current_dates_pass(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state())
    assert _run(state, "2026-09-03") == 0


def test_today_override_freezes_clock(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(weekly="2026-09-04"),
    )
    assert _run(state, "2026-09-04") == 0
    assert _run(state, "2026-09-05") == 1


def test_parser_does_not_read_lab_or_adr() -> None:
    src = SCRIPT.read_text(encoding="utf-8")
    assert "lab/" not in src
    assert "docs/adr" not in src
    assert "STATE.md" in src


def test_newest_index_date_is_max_not_first() -> None:
    text = _state(newest_decision="2026-08-20")
    text = text.replace(
        "- **2026-08-20** — newest.\n- **2026-08-01** — older.",
        "- **2026-08-01** — first.\n- **2026-08-20** — later.",
    )
    assert mod.newest_decision_index_date(text) == date(2026, 8, 20)


def test_today_et_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("STATE_CURRENCY_TODAY", "2026-09-03")
    assert mod.today_et() == date(2026, 9, 3)


def test_weekly_deadline_beyond_horizon_exits_one(tmp_path: Path) -> None:
    state = _write(tmp_path / "STATE.md", _state(weekly="2027-09-04"))
    assert _run(state, "2026-09-03") == 1


def test_weekly_horizon_is_seven_days(tmp_path: Path) -> None:
    on_horizon = _write(tmp_path / "on.md", _state(weekly="2026-09-10"))
    past_horizon = _write(tmp_path / "past.md", _state(weekly="2026-09-11"))
    assert _run(on_horizon, "2026-09-03") == 0
    assert _run(past_horizon, "2026-09-03") == 1


def test_monthly_horizon_is_thirty_one_days(tmp_path: Path) -> None:
    on_horizon = _write(tmp_path / "on.md", _state(monthly="2026-10-04"))
    past_horizon = _write(tmp_path / "past.md", _state(monthly="2026-10-05"))
    assert _run(on_horizon, "2026-09-03") == 0
    assert _run(past_horizon, "2026-09-03") == 1


def test_duplicate_weekly_heading_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(
            extra_headings=(
                "\n### Weekly — recurring (rolling; next deadline **2026-09-11**)\n\n"
                "- **duplicate.**\n"
            )
        ),
    )
    assert _run(state, "2026-09-03") == 1


def test_negated_discharged_heading_exits_one(tmp_path: Path) -> None:
    not_discharged = _write(
        tmp_path / "not.md",
        _state(extra_headings="\n### 2026-08-24 — NOT DISCHARGED\n\n- **still owed.**\n"),
    )
    undischarged = _write(
        tmp_path / "un.md",
        _state(extra_headings="\n### 2026-08-24 — UNDISCHARGED\n\n- **still owed.**\n"),
    )
    assert _run(not_discharged, "2026-09-03") == 1
    assert _run(undischarged, "2026-09-03") == 1


def test_heading_is_discharged_requires_affirmative_token() -> None:
    assert mod.heading_is_discharged("### 2026-08-08 — DISCHARGED") is True
    assert mod.heading_is_discharged("### 2026-08-24 — NOT DISCHARGED") is False
    assert mod.heading_is_discharged("### 2026-08-24 — UNDISCHARGED") is False
    assert mod.heading_is_discharged("### 2026-08-24 (Monday)") is False


def test_stale_weekly_fail_names_state_roll(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(
            curated="2026-08-28",
            newest_decision="2026-08-28",
            weekly="2026-08-28",
        ),
    )
    env = os.environ.copy()
    env["STATE_CURRENCY_TODAY"] = "2026-09-03"
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state)],
        cwd=REPO,
        env=env,
        capture_output=True,
    )
    assert proc.returncode == 1
    assert b"for deadline rolls run: python -I scripts/fp.py python scripts/state_roll.py" in proc.stderr


def _fail_text(state: Path, today: str) -> bytes:
    env = os.environ.copy()
    env["STATE_CURRENCY_TODAY"] = today
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(state)],
        cwd=REPO,
        env=env,
        capture_output=True,
    )
    assert proc.returncode == 1
    return proc.stderr


def test_beyond_horizon_fail_asks_for_manual_correction(tmp_path: Path) -> None:
    # Codex 4110271939: state_roll.py only rolls PAST deadlines, so a future
    # (beyond-horizon) deadline must not be pointed at it.
    state = _write(tmp_path / "STATE.md", _state(weekly="2027-09-04"))
    stderr = _fail_text(state, "2026-09-03")
    assert b"state_roll.py" not in stderr
    assert b"correct the heading by hand" in stderr


def test_last_curated_only_fail_does_not_name_state_roll(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(curated="2026-08-31", newest_decision="2026-09-03"),
    )
    assert b"state_roll.py" not in _fail_text(state, "2026-09-03")


def test_past_dated_subsection_fail_does_not_name_state_roll(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(extra_headings="\n### 2026-08-24 (Monday)\n\n- **this session.**\n"),
    )
    assert b"state_roll.py" not in _fail_text(state, "2026-09-03")


@pytest.mark.parametrize("monthly", ["2026-08-31", "2026-08-28"])
def test_past_unanchored_month_end_monthly_fail_asks_for_anchor(
    tmp_path: Path, monthly: str
) -> None:
    # state_roll.py refuses unanchored Monthly days 28-31 (a hand-clamped
    # month end reads back as the 28th-30th), so the hint must not send the
    # operator straight to it; it names the anchor that makes it rollable.
    state = _write(tmp_path / "STATE.md", _state(monthly=monthly))
    stderr = _fail_text(state, "2026-09-03")
    assert b"for deadline rolls run" not in stderr
    assert b"cadence day NN" in stderr


def test_past_anchored_month_end_monthly_fail_names_state_roll(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(monthly="2026-08-31").replace(
            "next deadline **2026-08-31**)", "next deadline **2026-08-31**, cadence day 31)"
        ),
    )
    assert b"for deadline rolls run" in _fail_text(state, "2026-09-03")


# --- Codex 4110350211: duplicate singleton sections -------------------------


def test_duplicate_forward_section_exits_one(tmp_path: Path) -> None:
    # A second section's stale deadline would otherwise go unchecked.
    state = _write(
        tmp_path / "STATE.md",
        _state()
        + (
            "\n## Scheduled forward triggers (continued)\n\n"
            "### Monthly — recurring (rolling; next deadline **2026-08-21**)\n"
        ),
    )
    assert b"Scheduled forward triggers" in _fail_text(state, "2026-09-03")


def test_duplicate_decision_section_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state()
        + (
            "\n## Executed operator decisions — decision index (newer)\n\n"
            "- **2026-09-09** — newer than Last curated.\n"
        ),
    )
    assert b"Executed operator decisions" in _fail_text(state, "2026-09-03")


def test_duplicate_last_curated_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state().replace(
            "**Last curated:** 2026-09-03\n",
            "**Last curated:** 2026-09-03\n\n**Last curated:** 2026-08-01\n",
        ),
    )
    assert b"Last curated" in _fail_text(state, "2026-09-03")


# --- Codex 4110941070 / 4110941072 + uniqueness class sweep -----------------


def _monthly_heading(state: str, suffix: str, monthly: str = "2026-09-21") -> str:
    heading = f"next deadline **{monthly}**)"
    assert heading in state
    return state.replace(heading, f"next deadline **{monthly}**{suffix})")


def test_second_deadline_field_exits_one(tmp_path: Path) -> None:
    # 4110941070: the gate read only the first field, so a stale second one
    # passed while the roller rolled only the first.
    state = _write(
        tmp_path / "STATE.md",
        _monthly_heading(_state(), ", next deadline **2026-08-21**"),
    )
    assert b"next deadline" in _fail_text(state, "2026-09-03")


@pytest.mark.parametrize(
    "suffix",
    [
        ", cadence day 20",  # disagrees with the deadline (the 21st)
        ", cadence day 32",
        ", cadence day 0",
        ", cadence day x",
        ", cadence day 21, cadence day 21",
        ", Cadence Day 21",  # case near-miss: the roller would not read it
        ", cadence-day 21",
    ],
)
def test_anchor_the_roller_refuses_fails_the_gate_even_when_not_due(
    tmp_path: Path, suffix: str
) -> None:
    # 4110941072: a regex match of the anchor is not enough; the gate applies
    # the roller's own validation on every run.
    state = _write(tmp_path / "STATE.md", _monthly_heading(_state(), suffix))
    assert b"cadence day" in _fail_text(state, "2026-09-03").lower()


def test_valid_anchor_passes(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md", _monthly_heading(_state(), ", cadence day 21")
    )
    assert _run(state, "2026-09-03") == 0


def test_last_curated_near_miss_exits_one(tmp_path: Path) -> None:
    # A case variant would otherwise be ignored while the first copy passes.
    state = _write(
        tmp_path / "STATE.md",
        _state().replace(
            "**Last curated:** 2026-09-03\n",
            "**Last curated:** 2026-09-03\n\n**Last Curated:** 2026-08-01\n",
        ),
    )
    assert b"Last curated" in _fail_text(state, "2026-09-03")


def test_near_miss_index_bullet_exits_one(tmp_path: Path) -> None:
    # A newer decision written as '* **date**' was invisible to the newest-date
    # read, so a stale Last curated passed.
    state = _write(
        tmp_path / "STATE.md",
        _state().replace(
            "- **2026-08-01** — older.", "- **2026-08-01** — older.\n* **2026-09-09** — newer."
        ),
    )
    _fail_text(state, "2026-09-03")


def test_discharged_requires_no_negated_discharged_token() -> None:
    # First-match reading let a later NOT DISCHARGED pass as discharged.
    assert mod.heading_is_discharged("### 2026-08-24 — DISCHARGED; NOT DISCHARGED") is False
    assert mod.heading_is_discharged("### 2026-08-24 — NOT DISCHARGED; DISCHARGED") is False
    assert mod.heading_is_discharged("### 2026-08-24 — DISCHARGED (DISCHARGED)") is True


def test_partly_negated_discharged_heading_exits_one(tmp_path: Path) -> None:
    state = _write(
        tmp_path / "STATE.md",
        _state(
            extra_headings="\n### 2026-08-24 — DISCHARGED (part); NOT DISCHARGED (rest)\n"
        ),
    )
    _fail_text(state, "2026-09-03")
