"""V1 on small synthetic panels: the harness's realised-side placebo equals the frozen pre-#1074
production 5e placebo (``frozen_placebo``, engine ``10f0eb19…``) exactly."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core")]

import numpy as np  # noqa: E402
import pytest  # noqa: E402

from research_utils.camp_import import load_camp_sibling  # noqa: E402

H = load_camp_sibling("harness", __file__)
F = load_camp_sibling("frozen_placebo", __file__)


@pytest.mark.parametrize("drift", [0.0, 2.0])
def test_realised_side_reproduces_frozen_pre_1074_placebo(drift):
    rng = np.random.default_rng(1)
    b, ds = H.bar_panel(rng, 40, drift)
    days, trades = H.card_trades(b, ds)
    assert trades
    prod = F.placebo_beaten_share(H.CARD, days, trades, H.COSTS, 200, 7)
    assert H.beaten_shares(days, trades, 200, 7, np.random.default_rng(2))["realised"] == prod


def test_bars_are_path_consistent():
    b, _ = H.bar_panel(np.random.default_rng(3), 5, 0.0)
    assert (b["high"] >= b[["open", "close"]].max(axis=1)).all()
    assert (b["low"] <= b[["open", "close"]].min(axis=1)).all()
