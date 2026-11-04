"""Harness self-checks: exact standardisation, exact Sharpe algebra, engine-net identity."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import harness as H  # noqa: E402

from builder import gates  # noqa: E402


@pytest.mark.parametrize("shape", ["normal", "orb_skew"])
def test_shapes_are_standardised(shape):
    u = (np.arange(400_000) + 0.5) / 400_000  # midpoint rule on the quantile function
    z = H.shape_quantile(shape, u)
    assert abs(z.mean()) < 2e-3 and abs(z.var() - 1) < 5e-3


@pytest.mark.parametrize("s,q", [(0.0535, 0.15), (0.0945, 0.85), (0.0, 0.4)])
def test_trade_mean_gives_the_session_sharpe_exactly(s, q):
    mu = H.trade_mean(s, q)
    mean, var = q * mu, q * (1 + mu * mu) - (q * mu) ** 2
    assert mean / math.sqrt(var) == pytest.approx(s, abs=1e-12)


def test_synthetic_trades_carry_their_net_through_the_engine():
    ds = H.dates(3)
    net = np.array([-120.5, 33.25, 250.0])
    t = H.to_trades(np.arange(3), net, ds)
    assert gates.net(H.CARD, t, H.COSTS) == pytest.approx(net)
    assert gates.daily(H.CARD, t, ds, H.COSTS) == pytest.approx(net)


def test_closed_form_matches_the_engines_reachability_line():
    r = gates.reachability(4, 1510)
    assert H.closed_form_5f(0.85, 4, 1510) == pytest.approx(r["p_pass"]["0.85"])


def test_a_series_path_runs_the_real_holdout_and_placement():
    out = H.series_path(np.random.default_rng(0), 1.5, 400, 100, 0.85, "orb_skew", (1, 2), 0.0, 1.0, 0.9)
    assert set(out["5f"]) == {1, 2} and out["placement"] in (None, "clear", "fail")
    assert (out["placement"] is None) == (not out["holdout"])
