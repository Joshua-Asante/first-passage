"""Control tests for the rank-ρ cert driver — data-independent (no vendor CSVs).

Run: python -m pytest lab/analysis/gbpusd_rank_cert/test_rank_cert.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rank_cert import (  # noqa: E402
    SIGNAL_PARAMS,
    _pine_literal,
    bake_cfg_pine,
    score_block,
)

MINI_PINE = """//@version=6
// scaffold comment
startDate   = input.time(timestamp("2022-01-01"), "Start Date", group=g)
endDate     = input.time(timestamp("2026-12-31"), "End Date",   group=g)
fastLen = input.int(50, "Fast EMA Length", minval=5, maxval=200, step=1, group="s")
slowLen = input.int(200, "Slow EMA Length", minval=20, maxval=400, step=5, group="s")
useSession = input.bool(true, "Use Session Filter", group="s")
atrLength = input.int(14, "ATR Length", minval=5, maxval=30, step=1, group="s")
atrMaLength = input.int(85, "ATR MA Length", minval=20, maxval=150, step=5, group="s")
atrExpansion = input.float(0.28, "ATR Expansion Ratio", minval=0.05, maxval=1.5, step=0.01, group="s")
exitAtrLength = input.int(14, "Exit ATR Length", minval=5, maxval=30, step=1, group="s")
stopAtr = input.float(1.55, "Stop Loss (ATR)", minval=0.5, maxval=5.0, step=0.05, group="s")
tpAtr = input.float(29.0, "Take Profit (ATR)", minval=2.0, maxval=50.0, step=0.5, group="s")
"""

CFG = {
    "fastLen": 30, "slowLen": 60, "useSession": True, "atrLength": 7,
    "atrMaLength": 60, "atrExpansion": 0.1, "exitAtrLength": 14,
    "stopAtr": 1.0, "tpAtr": 20,
}


def test_bake_replaces_every_default_and_dates():
    baked = bake_cfg_pine(MINI_PINE, CFG, index=1, candidate_id="CAND-X")
    assert 'timestamp("2018-01-01")' in baked
    assert 'timestamp("2024-01-01")' in baked
    assert "fastLen = input.int(30," in baked
    assert "useSession = input.bool(true," in baked
    assert "atrExpansion = input.float(0.1," in baked
    assert "tpAtr = input.float(20," in baked
    # version line stays first; header inserted right after it
    lines = baked.splitlines()
    assert lines[0] == "//@version=6"
    assert lines[1].startswith("// >>> RANK-")
    assert "CAND-X__cfg01.csv" in baked


def test_bake_usesession_false_and_tz_line_dropped():
    cfg = dict(CFG, useSession=False)
    baked = bake_cfg_pine(MINI_PINE, cfg, index=3, candidate_id="CAND-X")
    assert "useSession = input.bool(false," in baked
    assert "SET TV CHART TIMEZONE" not in baked
    baked_true = bake_cfg_pine(MINI_PINE, CFG, index=3, candidate_id="CAND-X")
    assert "SET TV CHART TIMEZONE" in baked_true


def test_bake_rejects_unknown_param_and_missing_anchor():
    with pytest.raises(ValueError, match="not a known SIGNAL param"):
        bake_cfg_pine(MINI_PINE, dict(CFG, bogus=1), index=0, candidate_id="C")
    with pytest.raises(ValueError, match="exactly 1 match"):
        bake_cfg_pine(MINI_PINE.replace("fastLen = input.int", "xLen = input.int"),
                      CFG, index=0, candidate_id="C")


def test_pine_literal_bool_lowercase():
    assert _pine_literal(True) == "true"
    assert _pine_literal(False) == "false"
    assert _pine_literal(0.1) == "0.1"
    assert _pine_literal(20) == "20"


def _mk_result(entry_days, returns):
    entry = np.array([np.datetime64(d) for d in entry_days])
    r = np.asarray(returns, dtype=float)
    pnl = r * 1000
    return SimpleNamespace(
        entry_times=entry, returns=r, pnl=pnl, n_trades=len(r),
        metrics={"net_profit": float(pnl.sum()), "profit_factor": 2.0},
    )


def test_score_block_splits_halves_on_entry_time():
    res = _mk_result(
        ["2018-06-01", "2019-01-01", "2021-06-01", "2022-01-01", "2023-01-01"],
        [0.01, -0.02, 0.03, 0.01, -0.01],
    )
    b = score_block(res, "2021-01-01")
    assert b["n_trades"] == 5
    assert b["h1"]["n_trades"] == 2 and b["h2"]["n_trades"] == 3
    assert b["h1"]["net_profit"] == pytest.approx(-10.0)
    assert b["h2"]["net_profit"] == pytest.approx(30.0)
    assert b["h1"]["sharpe"] is not None and b["h2"]["sharpe"] is not None


def test_score_block_single_trade_half_has_no_sharpe():
    res = _mk_result(["2018-06-01", "2022-01-01", "2023-01-01"], [0.01, 0.02, -0.01])
    b = score_block(res, "2021-01-01")
    assert b["h1"]["n_trades"] == 1
    assert b["h1"]["sharpe"] is None        # <2 trades: unrankable, never NaN
    assert b["h2"]["sharpe"] is not None
