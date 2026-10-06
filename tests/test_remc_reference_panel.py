"""Reference-panel reassembly (card 2026-10-06 §6): synthetic exports only."""
from __future__ import annotations

import pandas as pd
import pytest

from discovery.remc_reference_panel import (
    ACCOUNT,
    ReproductionError,
    STRATS,
    build_reference_panel,
    check_reproduction,
    pair_trades,
    reconstruct_static,
)


def _frame(trades):
    """trades: (n, entry, exit, net, cum_after, cum_pct, adverse). Mirrors load_csv's columns."""
    rows = []
    for n, entry, exit_, net, cum, pct, ae in trades:
        rows.append({"Trade #": n, "Type": "Entry long", "dt": pd.Timestamp(entry), "Net P&L USD": net,
                     "Cumulative P&L USD": cum, "Cumulative P&L %": pct, "Adverse excursion USD": ae})
        rows.append({"Trade #": n, "Type": "Exit long", "dt": pd.Timestamp(exit_), "Net P&L USD": net,
                     "Cumulative P&L USD": cum, "Cumulative P&L %": pct, "Adverse excursion USD": -ae})
    return pd.DataFrame(rows)


# Initial 100,000 implied by the last row: cum 4,000 at 4%.
LEG = [
    (1, "2026-01-05 09:30", "2026-01-05 11:00", -3000.0, -3000.0, -3.0, 3500.0),
    (2, "2026-01-07 09:30", "2026-01-07 11:00", 5000.0, 2000.0, 2.0, 800.0),
    (3, "2026-01-09 09:30", "2026-01-09 11:00", 2000.0, 4000.0, 4.0, 400.0),
]


def test_decompound_matches_archived_rule():
    t = reconstruct_static(pair_trades(_frame(LEG)), 100_000.0)
    assert list(t["equity_before"]) == [100_000.0, 97_000.0, 102_000.0]
    assert t["pnl_static"].iloc[1] == pytest.approx(5000.0 / 97_000.0 * ACCOUNT)
    assert t["adverse_static"].iloc[1] == pytest.approx(800.0 / 97_000.0 * ACCOUNT)


def test_panel_scales_pnl_and_low_identically_and_fills_bdays():
    frames = {s: _frame(LEG) for s in STRATS}
    panel, meta = build_reference_panel(frames)
    assert list(panel.index.strftime("%Y-%m-%d")) == [
        "2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08", "2026-01-09"]
    assert (panel.loc["2026-01-06"] == 0.0).all()
    day = pd.Timestamp("2026-01-07")
    expected_low = -sum(800.0 / 97_000.0 * ACCOUNT * meta["legs"][s]["scale"] for s in STRATS)
    assert panel.loc[day, "intraday_low"] == pytest.approx(expected_low)
    for s in STRATS:
        assert panel.loc[day, s] == pytest.approx(5000.0 / 97_000.0 * ACCOUNT * meta["legs"][s]["scale"])
    assert (panel["intraday_low"] <= 0).all()


def test_missing_leg_and_missing_adverse_column_raise():
    with pytest.raises(ValueError, match="missing required reference legs"):
        build_reference_panel({"striker": _frame(LEG)})
    with pytest.raises(ValueError, match="Adverse excursion USD"):
        pair_trades(_frame(LEG).drop(columns=["Adverse excursion USD"]))


def test_reproduction_check_rejects_scale_or_window_drift():
    meta = {"legs": {"striker": {"scale": 0.5521}, "striker_nas100": {"scale": 0.1254},
                     "aegis": {"scale": 1.0299}},
            "window": ["2020-01-06", "2026-07-01"], "n_bdays": 1693}
    check_reproduction(meta)
    meta["legs"]["aegis"]["scale"] = 1.0302
    with pytest.raises(ReproductionError, match="aegis scale"):
        check_reproduction(meta)
    meta["legs"]["aegis"]["scale"] = 1.0299
    meta["n_bdays"] = 1692
    with pytest.raises(ReproductionError, match="window"):
        check_reproduction(meta)
