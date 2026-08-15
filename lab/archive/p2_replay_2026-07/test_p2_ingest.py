"""Fixture tests — P2 replay ingest (ADR 2026-05-16: fixtures mandatory for
brief-evidence harness code). All fixtures are SYNTHETIC hand-written CSVs —
no vendor data is committed or required.

Schema coverage: the primary diff/pyramid/sanity fixtures use the CURRENT TV
schema ("Trade number"/"Net PnL USD"/"Size (value)"); ``legacy_basic.csv`` and
``dj30_pyramid_legacy.csv`` cover the legacy "Trade #" schema.
"""
from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import (  # noqa: E402
    FirstTradeSanityError,
    GridAlignmentError,
    assert_bar_grid,
    extract_signals,
    filter_signals_window,
    first_trade_sanity,
    load_export,
    to_et_boundary,
)

FIX = _HERE / "fixtures"


# --- both-schema parse cases -----------------------------------------------

def test_current_schema_parses_to_canonical_columns():
    df = load_export(FIX / "pep_diff_new.csv")
    assert "Trade #" in df.columns          # normalized from "Trade number"
    assert "Net P&L USD" in df.columns      # normalized from "Net PnL USD"
    assert "dt_et" in df.columns
    assert str(df["dt_et"].dt.tz) == "America/New_York"


def test_legacy_schema_parses_to_canonical_columns():
    df = load_export(FIX / "legacy_basic.csv")
    assert "Trade #" in df.columns
    assert "Net P&L USD" in df.columns
    assert df["dt_et"].notna().all()


def test_et_normalization_is_dst_aware(tmp_path):
    """Jan timestamps must localize at UTC-5, Jun at UTC-4 (frozen rule)."""
    header = ("Trade number,Type,Date and time,Signal,Price USD,Size (qty),"
              "Size (value),Net PnL USD,Net PnL %,Favorable excursion USD,"
              "Favorable excursion %,Adverse excursion USD,Adverse excursion %,"
              "Cumulative PnL USD,Cumulative PnL %")
    rows = [
        "1,Entry long,2026-01-05 10:00,Long,100,1,100,0,0,0,0,0,0,0,0",
        "1,Exit long,2026-01-05 11:00,Exit Long,101,1,101,1,1,1,1,0,0,1,1",
        "2,Entry long,2026-06-05 10:00,Long,100,1,100,0,0,0,0,0,0,1,1",
        "2,Exit long,2026-06-05 11:00,Exit Long,101,1,101,1,1,1,1,0,0,2,2",
    ]
    p = tmp_path / "dst.csv"
    p.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
    df = load_export(p)
    assert df["dt_et"].iloc[0].utcoffset() == timedelta(hours=-5)
    assert df["dt_et"].iloc[2].utcoffset() == timedelta(hours=-4)


# --- grid alignment (§0.5-d) -----------------------------------------------

def test_grid_alignment_passes_on_15m_export():
    df = load_export(FIX / "pep_diff_new.csv")
    assert_bar_grid(df, "pepperstone")  # must not raise


def test_misaligned_grid_is_hard_error_not_resample():
    df = load_export(FIX / "misaligned_grid_new.csv")
    with pytest.raises(GridAlignmentError) as exc:
        assert_bar_grid(df, "pepperstone")
    assert str(exc.value).startswith("NEEDS_CONTEXT")
    assert "resample" in str(exc.value)


# --- first-trade sanity (§0.5-e, F-1/JPY-153x class) ------------------------

def test_first_trade_sanity_passes_on_consistent_export():
    df = load_export(FIX / "first_trade_clean_new.csv")
    ratio = first_trade_sanity(df, point_value=1.0)
    assert ratio == pytest.approx(1.0)


def test_first_trade_sanity_catches_153x_corruption():
    df = load_export(FIX / "first_trade_corrupt_new.csv")
    with pytest.raises(FirstTradeSanityError) as exc:
        first_trade_sanity(df, point_value=1.0)
    assert "153.0x" in str(exc.value)
    assert str(exc.value).startswith("NEEDS_CONTEXT")


def test_first_trade_sanity_legacy_multi_leg_trade():
    """Legacy pyramid trade: expected P&L sums over ALL entry legs
    ((17100-17000)*10 + (17100-17050)*90 = 5500)."""
    df = load_export(FIX / "dj30_pyramid_legacy.csv")
    assert first_trade_sanity(df, point_value=1.0) == pytest.approx(1.0)


# --- signal extraction, both schemas incl. pyramid adds ---------------------

def test_extract_signals_pyramid_adds_current_schema():
    """Current schema: add leg is its OWN Trade number, Signal 'Long Add'."""
    df = load_export(FIX / "pep_pyramid_new.csv")
    sigs = extract_signals(df)
    assert len(sigs) == 2
    base, add = sigs
    assert base.is_add is False and base.direction == "long"
    assert add.is_add is True
    assert add.ts == to_et_boundary("2026-06-09 11:30")


def test_extract_signals_pyramid_adds_legacy_schema():
    """Legacy schema: 2nd+ Entry row within the same Trade # is an add."""
    df = load_export(FIX / "dj30_pyramid_legacy.csv")
    sigs = extract_signals(df)
    assert len(sigs) == 3
    assert [s.is_add for s in sigs] == [False, True, False]
    assert sigs[1].ts == to_et_boundary("2026-06-09 11:30")


def test_signal_window_filter_requires_explicit_bounds():
    df = load_export(FIX / "pep_diff_new.csv")
    sigs = extract_signals(df)
    out = filter_signals_window(
        sigs, to_et_boundary("2026-06-10"), to_et_boundary("2026-06-16"))
    assert [s.ts for s in out] == [to_et_boundary("2026-06-10 09:30"),
                                   to_et_boundary("2026-06-12 10:00")]
