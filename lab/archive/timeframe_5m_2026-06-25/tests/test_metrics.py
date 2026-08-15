import numpy as np
import pandas as pd
import metrics

def _exits(pcts):
    return pd.DataFrame({"net_pnl_pct": pcts})

def test_static_pnl_scales_pct_to_200k():
    s = metrics.static_pnl(_exits([1.0, -0.5]))   # 1.0% and -0.5% of 200k
    assert list(s) == [2000.0, -1000.0]

def test_pf_winrate_net():
    m = metrics.compute_metrics(_exits([1.0, 1.0, -0.5]), strategy="striker")
    assert m["trades"] == 3
    assert m["net_usd"] == 2000.0 + 2000.0 - 1000.0          # 3000
    assert abs(m["pf"] - (4000.0 / 1000.0)) < 1e-9           # 4.0
    assert abs(m["win_rate"] - (2 / 3)) < 1e-9

def test_max_dd_and_rf():
    # cumulative static-$ curve: +2000, +1000(after -1000), then +5000
    m = metrics.compute_metrics(_exits([1.0, -0.5, 2.0]), strategy="striker")
    assert m["max_dd_usd"] == 1000.0                          # peak 2000 -> 1000 trough
    assert abs(m["rf"] - (m["net_usd"] / 1000.0)) < 1e-9

def test_r1_fell_back_flag():
    # striker full-stop cohort = |loss| > 1% of 200k = >$2000; here losses are
    # tiny so <5 full stops -> implied_1r falls back to median (the documented trap).
    m = metrics.compute_metrics(_exits([1.0, 1.0, -0.5]), strategy="striker")
    assert m["r1_fell_back"] is True
    # guardian uses median loss by design -> never flagged as fallback.
    g = metrics.compute_metrics(_exits([1.0, -0.5, -0.5]), strategy="guardian")
    assert g["r1_fell_back"] is False
