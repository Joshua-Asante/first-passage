"""V1 on small synthetic panels: the harness's realised-side placebo equals production 5e exactly."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core")]

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import importlib.util  # noqa: E402

# Load this camp's harness under a unique key only. research_utils.camp_import.load_camp_sibling
# also publishes the bare name ``harness``, which another camp's plain ``import harness``
# (builder_power_2026-11) would then pick up in the same pytest process.
_spec = importlib.util.spec_from_file_location("_camp_builder_5e_check_2026_11_harness",
                                               Path(__file__).resolve().parent / "harness.py")
H = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = H
_spec.loader.exec_module(H)


@pytest.mark.parametrize("drift", [0.0, 2.0])
def test_realised_side_reproduces_production_placebo(drift):
    rng = np.random.default_rng(1)
    b, ds = H.bar_panel(rng, 40, drift)
    days, trades = H.card_trades(b, ds)
    assert trades
    prod = H.gates.placebo_beaten_share(H.CARD, days, trades, H.COSTS, 200, 7)
    assert H.beaten_shares(days, trades, 200, 7, np.random.default_rng(2))["realised"] == prod


def test_bars_are_path_consistent():
    b, _ = H.bar_panel(np.random.default_rng(3), 5, 0.0)
    assert (b["high"] >= b[["open", "close"]].max(axis=1)).all()
    assert (b["low"] <= b[["open", "close"]].min(axis=1)).all()
