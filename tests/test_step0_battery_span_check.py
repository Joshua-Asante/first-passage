"""Tests for the date-span coverage check in lab/research_utils/step0_battery.py.

Folded in from Guardian filter-sweep hardening
(lab/analysis/guardian_filter_sweep_2026-06-20/). Canonical home is lab/, not the
skill launcher under .claude/skills/…/scripts/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from research_utils import step0_battery as sb

_CSV = """Trade number,Type,Date and time,Price,Net PnL USD
1,Entry long,2024-01-01 14:30:00,100,
1,Exit long,2024-01-01 15:00:00,101,50
2,Entry long,2024-06-01 14:30:00,100,
2,Exit long,2024-06-01 15:00:00,99,-50
"""


def _write_csv(tmp_path: Path) -> Path:
    p = tmp_path / "panel.csv"
    p.write_text(_CSV, encoding="utf-8")
    return p


def _run(monkeypatch, argv) -> int:
    monkeypatch.setattr(sys, "argv", ["step0_battery.py"] + argv)
    with pytest.raises(SystemExit) as exc:
        sb.main()
    return exc.value.code


def test_no_expected_span_is_unaffected(tmp_path, monkeypatch, capsys):
    csv = _write_csv(tmp_path)
    rc = _run(monkeypatch, [str(csv), "--timeframe", "15"])
    assert rc == 0
    assert "time-clustered" not in capsys.readouterr().out


def test_time_clustered_panel_fails_span_coverage(tmp_path, monkeypatch, capsys):
    # Panel spans only Jan-Jun; claimed full period is the whole year -> ~42% coverage.
    csv = _write_csv(tmp_path)
    rc = _run(monkeypatch, [
        str(csv), "--timeframe", "15",
        "--expected-span", "2024-01-01", "2024-12-31",
    ])
    assert rc == 2
    out = capsys.readouterr().out
    assert "time-clustered" in out


def test_full_coverage_panel_passes(tmp_path, monkeypatch, capsys):
    csv = _write_csv(tmp_path)
    rc = _run(monkeypatch, [
        str(csv), "--timeframe", "15",
        "--expected-span", "2024-01-01", "2024-06-01",
    ])
    assert rc == 0
    assert "time-clustered" not in capsys.readouterr().out


def test_custom_cover_frac_threshold(tmp_path, monkeypatch, capsys):
    # Same ~42% coverage, but a lenient threshold now accepts it.
    csv = _write_csv(tmp_path)
    rc = _run(monkeypatch, [
        str(csv), "--timeframe", "15",
        "--expected-span", "2024-01-01", "2024-12-31",
        "--span-cover-frac", "0.30",
    ])
    assert rc == 0
