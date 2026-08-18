"""ECON EXPORT v0.1 diff — synthetic fixtures; no TradingView run."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


diff = _load("diff_econ_calendar", "scripts/diff_econ_calendar.py")
parse = _load("parse_econ_export", "scripts/parse_econ_export.py")

CPI_EPOCH = 1704931200000  # 2024-01-11 UTC
CPI_ADJ_EPOCH = 1704844800000  # 2024-01-10 UTC


def _lot_csv(path: Path, epoch: int, field: str = "CPI") -> Path:
    path.write_text(
        "Trade #,Type,Date and time,Signal,Price USD\n"
        f"1,Entry long,2024-01-11 00:00,{epoch}|US|{field}|308.5|America/New_York|D,100\n",
        encoding="utf-8",
    )
    return path


def test_compare_match_and_missing():
    rows = diff.compare_sets(
        limb="RATES-EV-ZF-1",
        field="CPI",
        hand={"2024-01-11", "2024-02-13"},
        tv={"2024-01-11"},
        tv_present=True,
    )
    statuses = {(r.status, r.date) for r in rows}
    assert ("MATCH", "2024-01-11") in statuses
    assert ("MISSING_TV", "2024-02-13") in statuses


def test_compare_tz_shift_not_extra():
    rows = diff.compare_sets(
        limb="RATES-EV-ZF-1",
        field="CPI",
        hand={"2024-01-11"},
        tv={"2024-01-10"},
        tv_present=True,
    )
    assert [r.status for r in rows] == ["TZ_SHIFT"]
    assert rows[0].note == "tv=2024-01-10"


def test_compare_extra_tv():
    rows = diff.compare_sets(
        limb="RATES-EV-ZF-1",
        field="CPI",
        hand={"2024-01-11"},
        tv={"2024-01-11", "2024-06-01"},
        tv_present=True,
    )
    extras = [r for r in rows if r.status == "EXTRA_TV"]
    assert [r.date for r in extras] == ["2024-06-01"]


def test_fomc_always_no_tv_field():
    rows = diff.compare_sets(
        limb="EVT-1",
        field="FOMC",
        hand=set(),
        tv=None,
        tv_present=True,
        no_tv_field=True,
    )
    assert rows[0].status == "NO_TV_FIELD"


def test_await_when_no_export():
    rows = diff.compare_sets(
        limb="RATES-EV-ZF-1",
        field="CPI",
        hand={"2024-01-11"},
        tv=None,
        tv_present=False,
    )
    assert rows[0].status == "AWAIT_TV_EXPORT"


def test_ngsc_zero_rows_is_no_tv_field():
    rows = diff.compare_sets(
        limb="NG-EIA-1",
        field="NGSC",
        hand={"2019-01-03"},
        tv=set(),
        tv_present=True,
    )
    assert rows[0].status == "NO_TV_FIELD"


def test_run_diff_without_export_is_await_and_fomc_gaps():
    rows = diff.run_diff(export_paths=[])
    statuses = {r.status for r in rows}
    assert "AWAIT_TV_EXPORT" in statuses
    assert "NO_TV_FIELD" in statuses
    assert "UNRECOVERABLE_PIN" in statuses
    assert not any(r.status == "MATCH" for r in rows)
    fomc = [r for r in rows if r.field == "FOMC"]
    assert any(r.status == "NO_TV_FIELD" for r in fomc)
    assert any(r.status == "UNRECOVERABLE_PIN" for r in fomc)


def test_run_diff_with_synthetic_cpi_matches_hand_pin(tmp_path: Path):
    csv = _lot_csv(tmp_path / "ECON_EXPORT_v0.1_TV_USCPI_2026-08-18_abcde.csv", CPI_EPOCH)
    rows = diff.run_diff(export_paths=[csv])
    cpi_match = [r for r in rows if r.limb == "RATES-EV-ZF-1" and r.field == "CPI" and r.status == "MATCH"]
    assert any(r.date == "2024-01-11" for r in cpi_match)
    # adjacent-day export is TZ_SHIFT, not a second MATCH
    csv2 = _lot_csv(tmp_path / "adj.csv", CPI_ADJ_EPOCH)
    shifted = [
        r
        for r in diff.run_diff(export_paths=[csv2])
        if r.limb == "RATES-EV-ZF-1" and r.field == "CPI" and r.status == "TZ_SHIFT"
    ]
    assert any(r.date == "2024-01-11" for r in shifted)


def test_require_tv_export_exits_2():
    assert diff.main(["--require-tv-export"]) == 2


def test_imports_hand_pinned_owners_not_copies():
    rates = diff.load_rates_events()
    assert "2024-01-11" in rates["CPI"]
    assert "2024-01-05" in rates["NFP"]
    ng = diff.load_ng_primary()
    assert len(ng) == 323
    echo = diff.load_fomc_echo()
    assert "2024-11-07" in echo
    assert not any(d.startswith("2019-") for d in echo)
    assert not any(d.startswith("2020-") for d in echo)
    assert not any(d.startswith("2021-") for d in echo)
