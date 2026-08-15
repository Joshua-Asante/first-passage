"""Regression tests for the trade-csv-reconcile skill's reconcile.py.

Guards the TradingView export-schema migration: current TV exports renamed
`Trade #`->`Trade number`, `Net P&L USD`->`Net PnL USD`, `Cumulative P&L *`->
`Cumulative PnL *`, and split the excursion columns into USD/%. The reconciler
must parse BOTH the legacy and current schemas, and must attribute pyramid
P&L correctly under the new per-leg layout (each pyramid leg is its own
`Trade number` with Signal "... Add").

The skill had no tests before this file; these lock in both the fix and the
backward-compatible legacy path. See docs/SESSIONS.md 2026-06-27.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SKILL_SCRIPTS = (
    Path(__file__).resolve().parents[1]
    / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
)
sys.path.insert(0, str(_SKILL_SCRIPTS))

import reconcile  # noqa: E402


# --- new (current) TV export schema ---------------------------------------
NEW_HEADER = (
    "Trade number,Type,Date and time,Signal,Price USD,Size (qty),Size (value),"
    "Net PnL USD,Net PnL %,Favorable excursion USD,Favorable excursion %,"
    "Adverse excursion USD,Adverse excursion %,Cumulative PnL USD,Cumulative PnL %"
)

# --- legacy TV export schema ----------------------------------------------
OLD_HEADER = (
    "Trade #,Type,Date and time,Signal,Price USD,Size (qty),"
    "Net P&L USD,Net P&L %,Cumulative P&L USD,Cumulative P&L %,"
    "Favorable excursion USD,Adverse excursion USD"
)


def _write(tmp_path: Path, name: str, header: str, rows: list[str]) -> Path:
    p = tmp_path / name
    p.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
    return p


def test_load_csv_parses_new_schema(tmp_path):
    """Current-schema export must load and expose canonical column names."""
    rows = [
        "1,Entry long,2024-01-01 10:00,Long,100,1,100,0,0,0,0,0,0,0,0",
        "1,Exit long,2024-01-01 11:00,Exit Long,103,1,103,3000,1.5,3100,1.6,-50,-0.03,3000,1.5",
    ]
    csv = _write(tmp_path, "new.csv", NEW_HEADER, rows)
    df = reconcile.load_csv(csv)
    # canonical internal names the rest of the pipeline depends on
    assert "Trade #" in df.columns
    assert "Net P&L USD" in df.columns
    assert "dt" in df.columns
    assert df["dt"].notna().all()


def test_compute_metrics_new_schema_aegis(tmp_path):
    """Headline metrics off a current-schema export (non-pyramid arch)."""
    rows = [
        "1,Entry long,2024-01-01 10:00,Long,100,1,100,0,0,0,0,0,0,0,0",
        "1,Exit long,2024-01-01 11:00,Exit Long,103,1,103,3000,1.5,3100,1.6,-50,0,3000,1.5",
        "2,Entry long,2024-01-02 10:00,Long,100,1,100,0,0,0,0,0,0,3000,1.5",
        "2,Exit long,2024-01-02 11:00,Exit Long,97.5,1,97.5,-2500,-1.25,200,0.1,-2600,-1.3,500,0.25",
        "3,Entry long,2024-01-03 10:00,Long,100,1,100,0,0,0,0,0,0,500,0.25",
        "3,Exit long,2024-01-03 11:00,Exit Long,101,1,101,1000,0.5,1200,0.6,-100,0,1500,0.75",
    ]
    csv = _write(tmp_path, "aegis_new.csv", NEW_HEADER, rows)
    df = reconcile.load_csv(csv)
    m = reconcile.compute_metrics(df, "aegis", account=200_000.0)
    assert m.n == 3
    assert m.wins == 2 and m.losses == 1
    assert m.net == pytest.approx(1500.0)
    assert m.pf == pytest.approx(1.6)  # 4000 / 2500
    assert m.wr_pct == pytest.approx(66.6667, abs=1e-3)
    # DD: trough after the -2500 trade, peak was 203000
    assert m.max_dd_dollars == pytest.approx(2500.0)
    assert m.max_dd_pct == pytest.approx(2500.0 / 203_000.0 * 100, abs=1e-3)


def test_pyramid_share_new_schema_per_leg(tmp_path):
    """New format: each pyramid leg is its own Trade # with Signal '... Add'.

    add-leg realized P&L / total net = (600+400)/1800 = 0.5556.
    """
    rows = [
        "1,Entry long,2024-01-01 10:00,Long,100,10,1000,0,0,0,0,0,0,0,0",
        "1,Exit long,2024-01-01 12:00,Exit Long,110,10,1100,1000,0.5,1100,0.6,0,0,1000,0.5",
        "2,Entry long,2024-01-01 10:30,Long Add,102,10,1020,0,0,0,0,0,0,1000,0.5",
        "2,Exit long,2024-01-01 12:00,Exit Long Add,108,10,1080,600,0.3,700,0.35,0,0,1600,0.8",
        "3,Entry long,2024-01-01 11:00,Long Add,104,10,1040,0,0,0,0,0,0,1600,0.8",
        "3,Exit long,2024-01-01 12:00,Exit Long Add,108,10,1080,400,0.2,500,0.25,0,0,2000,1.0",
        "4,Entry long,2024-01-02 10:00,Long,100,10,1000,0,0,0,0,0,0,2000,1.0",
        "4,Exit long,2024-01-02 11:00,Exit Long,98,10,980,-200,-0.1,50,0,-250,-0.12,1800,0.9",
    ]
    csv = _write(tmp_path, "dj30_new.csv", NEW_HEADER, rows)
    df = reconcile.load_csv(csv)
    share = reconcile.compute_pyramid_share(
        df, df[df["Type"].str.startswith("Exit", na=False)].copy()
    )
    assert share == pytest.approx(1000.0 / 1800.0, abs=1e-4)


def test_pyramid_redflag_is_advisory_under_new_schema(tmp_path):
    """A low add-leg share under the per-leg schema must NOT assert
    'not load-bearing' (the 50% anchor predates the schema); it is advisory."""
    rows = [
        "1,Entry long,2024-01-01 10:00,Long,100,10,1000,0,0,0,0,0,0,0,0",
        "1,Exit long,2024-01-01 12:00,Exit Long,110,10,1100,1000,0.5,1100,0.6,0,0,1000,0.5",
        "2,Entry long,2024-01-01 10:30,Long Add,102,10,1020,0,0,0,0,0,0,1000,0.5",
        "2,Exit long,2024-01-01 12:00,Exit Long Add,104,10,1040,200,0.1,250,0.12,0,0,1200,0.6",
    ]
    csv = _write(tmp_path, "nas_new_lowshare.csv", NEW_HEADER, rows)
    df = reconcile.load_csv(csv)
    m = reconcile.compute_metrics(df, "striker_nas", account=200_000.0)
    assert m.pyramid_pnl_share == pytest.approx(200.0 / 1200.0, abs=1e-4)
    res = reconcile.ReconcileResult(
        strategy="striker_nas", feed="pepperstone", metrics=m, baseline=None
    )
    out = reconcile.format_output(res)
    assert "not load-bearing" not in out
    assert "advisory" in out.lower()


def test_load_csv_still_parses_legacy_schema(tmp_path):
    """Backward compatibility: the legacy schema must still load."""
    rows = [
        "1,Entry long,2024-01-01 10:00,Long,100,1,0,0,0,0,3100,-50",
        "1,Exit long,2024-01-01 11:00,Exit Long,103,1,3000,1.5,3000,1.5,3100,-50",
    ]
    csv = _write(tmp_path, "old.csv", OLD_HEADER, rows)
    df = reconcile.load_csv(csv)
    assert "Trade #" in df.columns
    assert "Net P&L USD" in df.columns
    assert df["dt"].notna().all()


def test_pyramid_share_legacy_qty_apportioned(tmp_path):
    """Legacy format: multiple Entry rows per Trade #, one combined exit.

    qty apportionment preserved: trade 1 has base qty 10 + add qty 90 on a
    +1000 exit (=> 900 pyramid), trade 2 is base-only +500.
    pyramid share = 900 / 1500 = 0.6.
    """
    rows = [
        "1,Entry long,2024-01-01 10:00,Long,100,10,0,0,0,0,0,0",
        "1,Entry long,2024-01-01 10:30,Long,102,90,0,0,0,0,0,0",
        "1,Exit long,2024-01-01 12:00,Exit Long,110,100,1000,0.5,1000,0.5,0,0",
        "2,Entry long,2024-01-02 10:00,Long,100,10,0,0,0,0,0,0",
        "2,Exit long,2024-01-02 11:00,Exit Long,105,10,500,0.25,1500,0.75,0,0",
    ]
    csv = _write(tmp_path, "dj30_old.csv", OLD_HEADER, rows)
    df = reconcile.load_csv(csv)
    share = reconcile.compute_pyramid_share(
        df, df[df["Type"].str.startswith("Exit", na=False)].copy()
    )
    assert share == pytest.approx(0.6, abs=1e-4)


# --- futures-era TV export schema (2026-07, Aegis→6J deep replay) -----------
# "Net PnL %" renamed to "Return %"; trailing "Duration (bars)" column added.
FUT_HEADER = (
    "Trade number,Type,Date and time,Signal,Price USD,Size (qty),Size (value),"
    "Net PnL USD,Return %,Favorable excursion USD,Favorable excursion %,"
    "Adverse excursion USD,Adverse excursion %,Cumulative PnL USD,"
    "Cumulative PnL %,Duration (bars)"
)

# Real trade 1 of the 2026-07-05 6J deep export: short 12 @ 0.008695,
# exit 0.0087045, $1.30/side/contract on pointvalue 12,500,000:
# 12*(0.008695-0.0087045)*12.5e6 - 2*1.30*12 = -1425.00 - 31.20 = -1456.20
_FUT_ROWS = [
    "1,Exit short,2022-01-12 10:15,X-Short,0.0087045,12,1304250,-1456.2,-0.11,0,0.00,-1440.6,-0.11,-1456.2,-1.46,0",
    "1,Entry short,2022-01-12 10:15,AegisShort,0.008695,12,1304250,-1456.2,-0.11,0,0.00,-1440.6,-0.11,-1456.2,-1.46,0",
]


def test_load_csv_parses_futures_era_schema(tmp_path):
    """'Return %' must normalize to the canonical 'Net P&L %'; extra
    'Duration (bars)' column passes through untouched."""
    csv = _write(tmp_path, "fut.csv", FUT_HEADER, _FUT_ROWS)
    df = reconcile.load_csv(csv)
    assert "Trade #" in df.columns
    assert "Net P&L USD" in df.columns
    assert "Net P&L %" in df.columns
    assert "Duration (bars)" in df.columns


def test_futures_identity_passes_on_consistent_short(tmp_path):
    csv = _write(tmp_path, "fut_ok.csv", FUT_HEADER, _FUT_ROWS)
    df = reconcile.load_csv(csv)
    res = reconcile.check_futures_identity(
        df, pointvalue=12_500_000, tick=0.0000005, commission=1.30
    )
    assert res.ok
    assert res.n_checked == 1 and res.n_pass == 1
    assert res.max_abs_dev < 0.01
    assert res.off_grid_prices == 0


def test_futures_identity_catches_corrupt_net(tmp_path):
    rows = [r.replace("-1456.2,", "-1451.2,", 1) for r in _FUT_ROWS]
    csv = _write(tmp_path, "fut_bad.csv", FUT_HEADER, rows)
    df = reconcile.load_csv(csv)
    res = reconcile.check_futures_identity(
        df, pointvalue=12_500_000, tick=0.0000005, commission=1.30
    )
    assert not res.ok
    assert res.n_pass == 0
    assert any("dev=" in f for f in res.failures)


def test_futures_identity_catches_off_grid_price(tmp_path):
    # 0.0087046 / 0.0000005 = 17409.2 — not on the 6J tick grid
    rows = [r.replace("0.0087045", "0.0087046") for r in _FUT_ROWS]
    csv = _write(tmp_path, "fut_grid.csv", FUT_HEADER, rows)
    df = reconcile.load_csv(csv)
    res = reconcile.check_futures_identity(
        df, pointvalue=12_500_000, tick=0.0000005, commission=1.30
    )
    assert not res.ok
    assert res.off_grid_prices >= 1


def test_futures_identity_long_side_sign(tmp_path):
    """Long side: net = qty*(exit-entry)*pv - 2*comm*qty.
    2*(0.0070000->0.0070100)*12.5e6 - 2*1.0*2 = 250 - 4 = 246."""
    rows = [
        "1,Exit long,2024-01-02 11:00,X-Long,0.0070100,2,175250,246,0.02,300,0.03,-50,0,246,0.02,4",
        "1,Entry long,2024-01-02 10:00,Long,0.0070000,2,175250,246,0.02,300,0.03,-50,0,246,0.02,4",
    ]
    csv = _write(tmp_path, "fut_long.csv", FUT_HEADER, rows)
    df = reconcile.load_csv(csv)
    res = reconcile.check_futures_identity(
        df, pointvalue=12_500_000, tick=0.0000005, commission=1.0
    )
    assert res.ok, res.failures
