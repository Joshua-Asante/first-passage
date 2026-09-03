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
        f"### Weekly — recurring (rolling; next deadline **{weekly}**, bucket x)\n\n"
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
