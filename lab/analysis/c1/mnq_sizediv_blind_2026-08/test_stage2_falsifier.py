"""Pre-data unit tests for the Stage-2 falsifier scorer (green BEFORE the semester pull)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from research_utils.camp_import import load_camp_sibling

F = load_camp_sibling("stage2_falsifier", __file__)


def _slots(rows):
    return pd.DataFrame(rows, columns=["date", "r1_bp", "r2_bp"])


def _stats(rows):
    return pd.DataFrame(rows, columns=["date", "A"])


def test_pairing_skips_to_next_full_session_and_signs():
    d1, d2, d3 = pd.Timestamp("2024-01-02").date(), pd.Timestamp("2024-01-03").date(), pd.Timestamp("2024-01-05").date()
    slots = _slots([(d1, 10.0, -2.0), (d2, 5.0, 5.0), (d3, -4.0, 1.0)])
    stats = _stats([(d1, +0.01), (d2, -0.02), (d3, +0.01)])  # d3 has no next -> dropped
    t = F.pair_and_score(stats, slots)
    assert len(t) == 4  # d1->d2 (2 slots), d2->d3 (2 slots)
    r1 = t[(t["cond_date"] == d1) & (t["slot"] == "s1")].iloc[0]
    assert r1["exec_date"] == d2 and r1["signed_bp"] == pytest.approx(+5.0)
    r2 = t[(t["cond_date"] == d2) & (t["slot"] == "s1")].iloc[0]
    assert r2["exec_date"] == d3 and r2["signed_bp"] == pytest.approx(+4.0)  # short * -4.0


def test_zero_and_nan_A_dropped():
    d1, d2 = pd.Timestamp("2024-01-02").date(), pd.Timestamp("2024-01-03").date()
    slots = _slots([(d1, 1.0, 1.0), (d2, 1.0, 1.0)])
    stats = _stats([(d1, 0.0), (d2, np.nan)])
    assert len(F.pair_and_score(stats, slots)) == 0


def test_score_verdicts_fire_as_frozen():
    # Build 40 sessions with alternating A signs and returns that reward the rule
    dates = [pd.Timestamp("2024-01-01").date() + pd.Timedelta(days=i).to_pytimedelta() for i in range(41)]
    slots = _slots([(d, 6.0, 6.0) for d in dates])          # always +6bp per slot
    stats_long = _stats([(d, +0.01) for d in dates])        # always long -> +6bp/trade
    res = F.score(stats_long, slots)
    # mean +6bp > 2xRT PASS threshold, but F2 fires: hit == base (all-positive returns)
    assert res["hit_rate"] == pytest.approx(res["base_rate"])
    assert res["f2_kill"] and res["verdict"] == "KILL"

    # Mixed returns where the rule genuinely discriminates: A sign matches return sign
    rng = np.random.default_rng(7)
    signs = rng.choice([1.0, -1.0], size=41)
    slots2 = _slots([(d, 6.0 * s, 6.0 * s) for d, s in zip(dates, signs)])
    # condition on s predicts s+1: shift signs so A(s) = sign of NEXT session's return
    a_vals = [(dates[i], 0.01 * signs[i + 1]) for i in range(40)]
    stats2 = _stats(a_vals)
    res2 = F.score(stats2, slots2)
    assert res2["mean_signed_bp"] == pytest.approx(6.0)
    assert res2["hit_rate"] == 1.0 and res2["base_rate"] < 1.0
    # F3 relabel: A(s) vs same-session R_s should be ~uncorrelated for shifted signs
    assert not res2["f3_kill"]
    assert res2["verdict"] == "PASS"

    # HOLD band: uniform +1.5bp signed (between 1x and 2x RT), alternating A avoids F2/F3
    slots3 = _slots([(d, 1.5 * s, 1.5 * s) for d, s in zip(dates, signs)])
    stats3 = _stats(a_vals)
    res3 = F.score(stats3, slots3)
    assert res3["mean_signed_bp"] == pytest.approx(1.5)
    assert res3["verdict"] == "HOLD"
