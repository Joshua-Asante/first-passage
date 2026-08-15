"""Synthetic-fixture unit tests for the Layer 1M execution harness (harness_1m.py).

TDD for Q-ICT-1M (Q-ICT-CASCADE-1, Layer 4). Every fixture is hand-built in-test with
hand-computed expected R -- NO external export is touched, so these pass NOW with no
vendor data. They pin the FROZEN PREREG-1M rules:
  - cost_R cost-law (PREREG-1M L51,L55 / DRAFT L228,L260)
  - Entry/Exit pairing -> per-trade R (PREREG-1M R-pairing)
  - tradeability floor stop_dist < max(1pt, cost) (PREREG-1M L52, ledger F8)
  - HURDLE = 4 * median(cost_R) (PREREG-1M L55)
  - n-floor 100 -> INSUFFICIENT-N (PREREG-1M L69,L79)
  - entry-event block CI + drop-top-k on blocks (PREREG-1M L62-63,L132)
  - gate-ablation 8 labels; marginal-E[R] CI excludes 0 (PREREG-1M L77,L120)
  - DOW / arm-time-killzone one-slice permutation (PREREG-1M L77-78)
  - static-$200K recompute (PREREG-1M L59,L32)
  - starvation parse / closedtrades < 100 (PREREG-1M B4)

Run directly (the repo default `pytest tests/` does NOT collect lab/):
    python -m pytest lab/analysis/ict_cascade_2026-06-18/test_harness_1m.py -q
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness_1m as H  # noqa: E402


def approx(a, b, tol=1e-9):
    assert abs(a - b) < tol, f"{a} != {b}"


# =============================================================================
# COST_R cost-law (hand-computed; PREREG-1M L51,L55)
#   cost_R = (2*commPct*entry + 2*slipTk*mintick) / stop_dist
#   commPct=0.00002, slipTk=1
# =============================================================================
def test_cost_r_hand_computed():
    # entry=5000, stop_dist=10, mintick=0.1.
    # comm = 2*0.00002*5000 = 0.2 ; slip = 2*1*0.1 = 0.2 ; sum = 0.4 ; /10 = 0.04R
    c = H.cost_r(entry_price=5000.0, stop_dist=10.0, mintick=0.1)
    approx(c, 0.04)


def test_cost_r_scales_inverse_with_stop():
    # halve stop_dist -> double cost_R.
    c1 = H.cost_r(5000.0, 10.0, 0.1)
    c2 = H.cost_r(5000.0, 5.0, 0.1)
    approx(c2, 2.0 * c1)


def test_cost_r_nan_and_nonpositive_stop():
    assert math.isnan(H.cost_r(5000.0, float("nan"), 0.1))
    assert math.isinf(H.cost_r(5000.0, 0.0, 0.1))      # zero stop -> inf -> floor drops it
    assert math.isinf(H.cost_r(5000.0, -3.0, 0.1))


def test_cost_r_zero_commission_pure_slip():
    # comm_pct=0 -> cost is pure slippage: 2*1*0.1/10 = 0.02R
    c = H.cost_r(5000.0, 10.0, 0.1, comm_pct=0.0, slip_tk=1)
    approx(c, 0.02)


# =============================================================================
# R-PAIRING: Entry/Exit rows -> per-trade R (PREREG-1M R-pairing)
# =============================================================================
def _tv_rows(records):
    """Build raw TV List-of-Trades dict-rows from compact tuples.

    Each record = (trade_num, kind, type_side, price, qty, pnl, risk, stop_dist,
                   runup, drawdown, epoch_ms). kind in {'entry','exit'}.
    Produces rows keyed by the canonical header strings the adapter accepts.
    """
    rows = []
    for (tn, kind, side, price, qty, pnl, risk, sd, ru, dd, ep) in records:
        typ = ("Entry " if kind == "entry" else "Exit ") + side
        rows.append({
            "Trade #": str(tn), "Type": typ, "Price": str(price), "Quantity": str(qty),
            "Profit": "" if pnl is None else str(pnl),
            "Risk": "" if risk is None else str(risk),
            "stop_dist": "" if sd is None else str(sd),
            "Run-up": "" if ru is None else str(ru),
            "Drawdown": "" if dd is None else str(dd),
            "epoch_ms": "" if ep is None else str(ep),
        })
    return rows


def _colmap_for(rows):
    return H._build_colmap(list(rows[0].keys()))


def test_pairing_risk_basis_R():
    # PnL=+2000, risk(1R)=1000 -> r_gross = +2.0R.  stop_dist present for cost_R.
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, 1000.0, 20.0, None, None, None),
        (1, "exit",  "long", 5040.0, 1, 2000.0, None, None, None, None, None),
    ])
    trades, stats = H.pair_trades(rows, _colmap_for(rows))
    assert stats["n_paired"] == 1
    t = trades[0]
    assert t.side == 1
    approx(H.r_gross(t), 2.0)            # 2000/1000


def test_pairing_price_basis_R_when_no_risk_col():
    # No risk col -> R from (exit-entry)*side/stop_dist.
    # long entry 5000 exit 5030 stop_dist 15 -> +30/15 = +2.0R
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, None, 15.0, None, None, None),
        (1, "exit",  "long", 5030.0, 1, None, None, None, None, None, None),
    ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    approx(H.r_gross(trades[0]), 2.0)


def test_pairing_short_price_basis_R():
    # short entry 5000 exit 4970 stop_dist 15 -> (4970-5000)*(-1)/15 = +2.0R
    rows = _tv_rows([
        (1, "entry", "short", 5000.0, 1, None, None, 15.0, None, None, None),
        (1, "exit",  "short", 4970.0, 1, None, None, None, None, None, None),
    ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    assert trades[0].side == -1
    approx(H.r_gross(trades[0]), 2.0)


def test_pairing_unpaired_row_counted_not_dropped_silently():
    # trade 2 has only an entry -> unpaired, reported.
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, 1000.0, 20.0, None, None, None),
        (1, "exit",  "long", 5040.0, 1, 2000.0, None, None, None, None, None),
        (2, "entry", "long", 5010.0, 1, None, 1000.0, 20.0, None, None, None),
    ])
    trades, stats = H.pair_trades(rows, _colmap_for(rows))
    assert stats["n_paired"] == 1 and stats["n_unpaired"] == 1


def test_pnl_parses_parentheses_and_currency():
    # accounting-style negative "($1,500.00)" -> -1500.0 ; risk "1,000" -> 1000
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, "1,000", 20.0, None, None, None),
        (1, "exit",  "long", 4970.0, 1, "($1,500.00)", None, None, None, None, None),
    ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    approx(trades[0].pnl, -1500.0)
    approx(H.r_gross(trades[0]), -1.5)   # -1500/1000


def test_compute_per_trade_r_net_is_gross_minus_cost():
    # gross +2.0R, entry 5000, stop_dist 20, mintick 0.1
    # cost = (2*0.00002*5000 + 2*1*0.1)/20 = (0.2+0.2)/20 = 0.02R ; net = 1.98R
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, 1000.0, 20.0, None, None, None),
        (1, "exit",  "long", 5040.0, 1, 2000.0, None, None, None, None, None),
    ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    H.compute_per_trade(trades, mintick=0.1)
    approx(trades[0].cost_r, 0.02)
    approx(trades[0].r_gross, 2.0)
    approx(trades[0].r_net, 1.98)


# =============================================================================
# TRADEABILITY FLOOR: stop_dist < max(1pt, cost) dropped (PREREG-1M L52)
# =============================================================================
def test_tradeability_floor_drops_subspread_stop():
    # mintick=0.1 -> 1pt = 0.1 ; cost_price at entry 5000 = 0.2+0.2 = 0.4 ;
    # floor = max(0.1, 0.4) = 0.4. stop_dist 0.3 < 0.4 -> DROPPED.
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, 1000.0, 0.3, None, None, None),
        (1, "exit",  "long", 5001.0, 1, 100.0, None, None, None, None, None),
        (2, "entry", "long", 5000.0, 1, None, 1000.0, 20.0, None, None, None),  # ok
        (2, "exit",  "long", 5040.0, 1, 2000.0, None, None, None, None, None),
    ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    dropped = H.compute_per_trade(trades, mintick=0.1)
    assert dropped == 1
    drop_t = [t for t in trades if t.trade_num == 1][0]
    keep_t = [t for t in trades if t.trade_num == 2][0]
    assert drop_t.tradeable is False and keep_t.tradeable is True


# =============================================================================
# HURDLE = 4 * median(cost_R) over the tradeable population (PREREG-1M L55)
# =============================================================================
def test_median_hurdle_4x_median_cost():
    # three tradeable trades with cost_R 0.01, 0.02, 0.03 -> median 0.02 -> hurdle 0.08.
    rows = []
    # stop_dist chosen so cost_R = (0.2+0.2)/sd = 0.4/sd : sd=40->0.01, 20->0.02, ~13.33->0.03
    for tn, sd in ((1, 40.0), (2, 20.0), (3, 0.4 / 0.03)):
        rows += _tv_rows([
            (tn, "entry", "long", 5000.0, 1, None, 1000.0, sd, None, None, None),
            (tn, "exit",  "long", 5040.0, 1, 2000.0, None, None, None, None, None),
        ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    H.compute_per_trade(trades, mintick=0.1)
    hurdle, med = H.median_hurdle(trades)
    approx(med, 0.02, tol=1e-6)
    approx(hurdle, 0.08, tol=1e-6)


# =============================================================================
# ENTRY-EVENT BLOCKS + block means + block CI (PREREG-1M L62-63)
# =============================================================================
def _trade(r_net, block, dow=0, kz="nyam", trade_num=0):
    """Lightweight Trade with the fields the block/perm/droptopk paths read."""
    t = H.Trade(trade_num=trade_num, side=1, entry_price=5000.0, exit_price=5040.0,
                pnl=0.0, qty=1, risk=1000.0, stop_dist=20.0, runup=0.0, drawdown=0.0,
                entry_epoch_ms=float("nan"))
    t.r_gross = r_net + 0.02
    t.cost_r = 0.02
    t.r_net = r_net
    t.block_id = block
    t.et_dow = dow
    t.killzone = kz
    t.tradeable = True
    return t


def test_block_means_collapse():
    # block 0 has two trades (0.0, 2.0) -> mean 1.0 ; block 1 one trade (3.0)
    vals = [0.0, 2.0, 3.0]
    bids = [0, 0, 1]
    bm = H.block_means(vals, bids)
    assert sorted(bm.tolist()) == [1.0, 3.0]


def test_assign_blocks_by_epoch_minute():
    # two trades in the same ET minute -> one block; a third a minute later -> second block.
    base = int(pd.Timestamp("2026-06-18T13:00:00Z").value // 1_000_000)
    trades = []
    for k, off in enumerate((0, 30_000, 60_000)):  # 0s, 30s (same min), 60s (next min)
        t = _trade(1.0, block=-1, trade_num=k)
        t.entry_epoch_ms = float(base + off)
        trades.append(t)
    nb, mode = H.assign_blocks(trades, key="auto")
    assert nb == 2
    assert mode == "event"
    assert trades[0].block_id == trades[1].block_id      # same minute
    assert trades[2].block_id != trades[0].block_id


def test_block_ci_brackets_block_mean():
    # 30 blocks, each one trade, r_net ~ +1R with small spread -> CI well above 0.
    rng = np.random.default_rng(0)
    trades = [_trade(float(1.0 + rng.normal(0, 0.1)), block=i, trade_num=i)
              for i in range(40)]
    mean, lo, hi, nb, L = H.block_ci([t.r_net for t in trades],
                                     [t.block_id for t in trades], B=3000, seed=1)
    assert nb == 40
    assert lo > 0.0 and lo < mean < hi


def test_block_ci_uses_block_not_trade_count():
    # 50 IDENTICAL trades all in ONE block -> 1 resampling unit -> CI is degenerate
    # (a single block mean), proving the unit is the block, not the trade row.
    trades = [_trade(0.5, block=0, trade_num=i) for i in range(50)]
    mean, lo, hi, nb, L = H.block_ci([t.r_net for t in trades],
                                     [t.block_id for t in trades], B=1000, seed=1)
    assert nb == 1
    approx(mean, 0.5)
    approx(lo, 0.5)     # one block -> every resample is that same block mean
    approx(hi, 0.5)


# =============================================================================
# DROP-TOP-K on entry-event BLOCKS (PREREG-1M L63,L132)
# =============================================================================
def test_drop_top_k_default_k_scales_to_blocks():
    # 50 blocks -> default k = ceil(0.06*50) = 3.
    trades = [_trade(1.0, block=i, trade_num=i) for i in range(50)]
    out = H.drop_top_k_check(trades)
    assert out["n_blocks"] == 50
    assert out["k"] == 3


def test_drop_top_k_removes_edge_when_concentrated():
    # 19 blocks at -0.1R, 1 block at +100R -> full mean positive but driven by one block;
    # dropping top-1 (k=ceil(0.06*20)=2) -> all negative -> edge removed.
    trades = [_trade(-0.1, block=i, trade_num=i) for i in range(19)]
    trades.append(_trade(100.0, block=19, trade_num=19))
    out = H.drop_top_k_check(trades)
    assert out["full_mean"] > 0.0          # carried by the one fat block
    assert out["dropped_mean"] < 0.0       # edge gone after dropping top-k
    assert out["survives"] is False


def test_drop_top_k_survives_when_broad():
    # 40 blocks all ~ +1R -> dropping top-k still positive -> survives.
    trades = [_trade(1.0, block=i, trade_num=i) for i in range(40)]
    out = H.drop_top_k_check(trades)
    assert out["dropped_mean"] > 0.0 and out["survives"] is True


# =============================================================================
# GATE-ABLATION marginal E[R] (PREREG-1M L77; 8 labels; CI excludes 0)
# =============================================================================
def _labelled_with_bias_effect(on_r=1.0, off_r=-1.0, n_per=30, seed=0):
    """Build the 8 ablation labels where the BIAS gate ON lifts r_net, others neutral.

    Each label gets n_per trades, one block each. Labels with bias=1 -> on_r; bias=0 ->
    off_r. (PD/killzone flags vary but don't change r_net here.)
    """
    rng = np.random.default_rng(seed)
    labelled = {}
    bid = 0
    for label in H.ABLATION_LABELS:
        b, p, k = H._flags_from_label(label)
        base = on_r if b == 1 else off_r
        trades = []
        for _ in range(n_per):
            t = _trade(float(base + rng.normal(0, 0.05)), block=bid, trade_num=bid)
            trades.append(t)
            bid += 1
        labelled[label] = trades
    return labelled


def test_marginal_gate_bias_earns_its_place():
    labelled = _labelled_with_bias_effect(on_r=1.0, off_r=-1.0, n_per=30, seed=1)
    m = H.marginal_gate_er(labelled, "bias", B=2000, seed=2)
    assert m["diff"] > 1.5                  # ON-OFF ~ +2R
    assert m["excludes_zero"] is True       # CI excludes 0 -> earns its place


def test_marginal_gate_pd_adds_nothing():
    # bias drives r_net; PD flag is uncorrelated -> PD marginal CI straddles 0.
    labelled = _labelled_with_bias_effect(on_r=1.0, off_r=-1.0, n_per=30, seed=3)
    m = H.marginal_gate_er(labelled, "pd", B=2000, seed=4)
    assert abs(m["diff"]) < 0.5
    assert m["excludes_zero"] is False


def test_ablation_label_set_is_exactly_8():
    # audit-hook L120: the matrix is exactly 8 distinct labels.
    assert len(H.ABLATION_LABELS) == 8
    assert len(set(H.ABLATION_LABELS)) == 8
    # all flag combos present
    flags = sorted(H._flags_from_label(l) for l in H.ABLATION_LABELS)
    assert flags == sorted((b, p, k) for b in (0, 1) for p in (0, 1) for k in (0, 1))


# =============================================================================
# ONE-SLICE PERMUTATION (PREREG-1M L77-78)
# =============================================================================
def test_one_slice_permutation_detects_concentrated_dow():
    # all positive edge sits in DOW=2 (Wed); other DOWs ~0 -> permutation flags it.
    trades = []
    bid = 0
    for dow in range(5):
        r = 3.0 if dow == 2 else 0.0
        for _ in range(20):
            trades.append(_trade(r, block=bid, dow=dow, trade_num=bid)); bid += 1
    out = H.one_slice_permutation(trades, "et_dow", B=5000, seed=1)
    assert out["slice"] == "2"
    assert out["p"] < 0.05                   # edge lives in one slice


def test_one_slice_permutation_uniform_not_significant():
    # edge spread evenly across DOWs -> no single slice carries it -> large p.
    rng = np.random.default_rng(0)
    trades = []
    bid = 0
    for dow in range(5):
        for _ in range(20):
            trades.append(_trade(float(1.0 + rng.normal(0, 0.2)), block=bid, dow=dow,
                                 trade_num=bid)); bid += 1
    out = H.one_slice_permutation(trades, "et_dow", B=5000, seed=2)
    assert out["p"] > 0.05


def test_killzone_of_windows():
    approx(0, 0);
    assert H.killzone_of(3, 0) == "london"      # 03:00 ET in [02:00,05:00)
    assert H.killzone_of(8, 30) == "nyam"       # 08:30 ET in [07:00,10:00)
    assert H.killzone_of(14, 0) == "nypm"       # 14:00 ET in [13:30,16:00)
    assert H.killzone_of(11, 0) == "out"        # 11:00 ET -> none
    assert H.killzone_of(5, 0) == "out"         # boundary 05:00 excluded


# =============================================================================
# STATIC-$200K RECOMPUTE (PREREG-1M L59,L32)
# =============================================================================
def test_static_200k_one_r_is_1000():
    # 0.5% of $200K = $1000 per 1R. Two +1R trades -> +$2000 total, no DD.
    trades = [_trade(1.0, block=0, trade_num=0), _trade(1.0, block=1, trade_num=1)]
    s = H.static_200k_pnl(trades)
    approx(s["one_r"], 1000.0)
    approx(s["total_dollars"], 2000.0)
    approx(s["max_dd_dollars"], 0.0)


def test_static_200k_drawdown():
    # +1R then -2R -> equity 201000 then 199000 -> peak 201000 -> max DD -2000.
    trades = [_trade(1.0, block=0, trade_num=0), _trade(-2.0, block=1, trade_num=1)]
    s = H.static_200k_pnl(trades)
    approx(s["total_dollars"], -1000.0)
    approx(s["max_dd_dollars"], -2000.0)
    approx(s["max_dd_pct"], -0.01)


# =============================================================================
# STARVATION PARSE (PREREG-1M B4)
# =============================================================================
def test_starvation_parse_insufficient_n(tmp_path):
    p = tmp_path / "starve.json"
    p.write_text(json.dumps({"closedtrades": 42, "skip:cost/R": 311, "skip:no-draw": 88}))
    d = H.parse_starvation(str(p))
    assert d["closedtrades"] == 42 and d["insufficient_n"] is True


def test_starvation_parse_sufficient(tmp_path):
    p = tmp_path / "starve.json"
    p.write_text(json.dumps({"closedtrades": 250, "skip:cost/R": 10}))
    d = H.parse_starvation(str(p))
    assert d["insufficient_n"] is False


def test_starvation_parse_absent_returns_none():
    assert H.parse_starvation("does_not_exist_xyz.json") is None


# =============================================================================
# VERDICT (section 6, per useBody variant; PREREG-1M L75-79)
# =============================================================================
def _full_labelled_resolved(seed=0, n_per=120):
    """8 ablation labels where ALL THREE gates earn their place (each gate ON lifts E[R]),
    and the gate-bearing config (bias1_pd1_kz1) has a broad +R edge spread across
    DOWs/killzones (no one-slice). The variant should RESOLVE.
    cost_r=0.02 -> hurdle 0.08; the all-on edge clears it.

    PREREG-1M L77: RESOLVED needs EACH retained gate (bias/PD/killzone) to show positive
    marginal E[R] with CI excluding 0 -- so the fixture gives each flag an additive +0.5R.
    n_per >= 100 so the gate-bearing export (one label) clears the n-floor: the headline
    population IS that single export's trades (PREREG-1M gate-bearing config = all gates ON).
    """
    rng = np.random.default_rng(seed)
    labelled = {}
    bid = 0
    dows = [0, 1, 2, 3, 4]
    kzs = ["london", "nyam", "nypm", "out"]
    for label in H.ABLATION_LABELS:
        b, p, k = H._flags_from_label(label)
        # each gate ON contributes additively so each gate's ON-vs-OFF marginal is +0.5R.
        base = -0.5 + 0.5 * b + 0.5 * p + 0.5 * k   # all-on -> +1.0R ; all-off -> -0.5R
        trades = []
        for j in range(n_per):
            t = _trade(float(base + rng.normal(0, 0.1)), block=bid,
                       dow=dows[j % 5], kz=kzs[j % 4], trade_num=bid)
            trades.append(t); bid += 1
        labelled[label] = trades
    return labelled


def test_verdict_insufficient_n():
    labelled = _full_labelled_resolved(seed=1, n_per=5)   # 5 trades/label -> default <100
    default = labelled["bias1_pd1_kz1"]
    r = H.verdict_for_variant(default, labelled, use_body=False, mintick=0.1)
    assert r.verdict == "INSUFFICIENT-N"
    assert r.n_trades < H.N_FLOOR


def test_verdict_resolved_when_edge_broad_and_gate_earns():
    labelled = _full_labelled_resolved(seed=2, n_per=120)  # 120 trades/export -> n>=100
    default = labelled["bias1_pd1_kz1"]
    # block_mode="event": the fixture pre-assigns real entry-event block ids (R6-2).
    r = H.verdict_for_variant(default, labelled, use_body=False, mintick=0.1,
                              boot_seed=3, perm_seed=5, block_mode="event")
    assert r.n_trades >= H.N_FLOOR
    assert r.verdict == "RESOLVED", r.reasons
    assert r.er_lo > r.hurdle
    assert r.gate_marginals["bias"]["excludes_zero"] is True


def test_verdict_falsified_when_edge_below_hurdle():
    # gate-bearing config has near-zero edge (r_net ~ +0.01R < hurdle 0.08) -> FALSIFIED.
    rng = np.random.default_rng(7)
    labelled = {}
    bid = 0
    for label in H.ABLATION_LABELS:
        trades = [_trade(float(0.01 + rng.normal(0, 0.05)), block=bid + j,
                         dow=j % 5, kz=["london", "nyam", "nypm", "out"][j % 4],
                         trade_num=bid + j) for j in range(120)]
        bid += 120
        labelled[label] = trades
    default = labelled["bias1_pd1_kz1"]
    r = H.verdict_for_variant(default, labelled, use_body=False, mintick=0.1,
                              boot_seed=8, perm_seed=9, block_mode="event")
    assert r.verdict == "FALSIFIED"
    assert any("subset of" in s or "add nothing" in s or "one slice" in s
               or "removes the edge" in s for s in r.reasons)


def test_verdict_falsified_when_not_every_gate_earns():
    # Only BIAS earns its place (PD/killzone neutral). PREREG-1M L77 requires EACH retained
    # gate to earn -> RESOLVED is denied even though E[R] clears the hurdle and no one-slice.
    rng = np.random.default_rng(21)
    labelled = {}
    bid = 0
    dows = [0, 1, 2, 3, 4]
    kzs = ["london", "nyam", "nypm", "out"]
    for label in H.ABLATION_LABELS:
        b, _p, _k = H._flags_from_label(label)
        base = 1.0 if b == 1 else -1.0          # ONLY bias has an effect
        trades = [_trade(float(base + rng.normal(0, 0.1)), block=bid + j,
                         dow=dows[j % 5], kz=kzs[j % 4], trade_num=bid + j)
                  for j in range(120)]
        bid += 120
        labelled[label] = trades
    default = labelled["bias1_pd1_kz1"]
    r = H.verdict_for_variant(default, labelled, use_body=False, mintick=0.1,
                              boot_seed=22, perm_seed=23, block_mode="event")
    # bias earns, pd + killzone do not -> not all gates earn -> FALSIFIED.
    assert r.gate_marginals["bias"]["excludes_zero"] is True
    assert r.gate_marginals["pd"]["excludes_zero"] is False
    assert r.verdict == "FALSIFIED"
    assert any("every retained gate" in s or "add nothing" in s for s in r.reasons)


def test_verdict_falsified_when_edge_in_one_slice():
    # n>=100, gate-bearing edge ALL in DOW=2 -> one-slice permutation kills it.
    rng = np.random.default_rng(11)
    labelled = {}
    bid = 0
    for label in H.ABLATION_LABELS:
        b, _p, _k = H._flags_from_label(label)
        trades = []
        for j in range(120):
            dow = j % 5
            # only the gate-bearing config concentrates; give bias ON a one-slice spike.
            if b == 1 and dow == 2:
                base = 5.0
            elif b == 1:
                base = 0.02
            else:
                base = -1.0
            trades.append(_trade(float(base + rng.normal(0, 0.05)), block=bid,
                                 dow=dow, kz="nyam", trade_num=bid)); bid += 1
        labelled[label] = trades
    default = labelled["bias1_pd1_kz1"]
    r = H.verdict_for_variant(default, labelled, use_body=False, mintick=0.1,
                              boot_seed=12, perm_seed=13, block_mode="event")
    assert r.verdict == "FALSIFIED"
    assert any("one slice" in s for s in r.reasons)


# =============================================================================
# SCHEMA ADAPTER end-to-end (CSV bytes -> trades) + nearest-pool report-only guard
# =============================================================================
def test_load_list_of_trades_roundtrip(tmp_path):
    csv_text = (
        "Trade #,Type,Date/Time,Price,Quantity,Profit,Risk,stop_dist\n"
        "1,Entry long,2026-06-18 09:00,5000,1,,1000,20\n"
        "1,Exit long,2026-06-18 09:30,5040,1,2000,,\n"
        "2,Entry short,2026-06-18 10:00,5050,1,,1000,20\n"
        "2,Exit short,2026-06-18 10:30,5020,1,1500,,\n"
    )
    p = tmp_path / "lot.csv"
    p.write_text(csv_text)
    trades, stats = H.load_list_of_trades(str(p))
    assert stats["n_paired"] == 2
    H.compute_per_trade(trades, mintick=0.1)
    t1 = [t for t in trades if t.trade_num == 1][0]
    t2 = [t for t in trades if t.trade_num == 2][0]
    approx(t1.r_gross, 2.0)      # 2000/1000
    approx(t2.r_gross, 1.5)      # 1500/1000
    assert t2.side == -1


def test_run_skips_when_export_missing(tmp_path):
    # empty dir -> load_manifest_or_dir reports all 16 missing -> run raises FileNotFound.
    with pytest.raises(FileNotFoundError):
        H.run(str(tmp_path), mintick=0.1)


# =============================================================================
# R6-1: datetime alias must be parsed to epoch_ms when no epoch_ms column exists
#       (loader never reads TV Date/Time -> epoch NaN -> iid + killzone "out").
# =============================================================================
def test_datetime_alias_populates_entry_epoch_when_no_epoch_col(tmp_path):
    # vanilla TV export: human Date/Time cell, NO epoch_ms column. The entry epoch
    # must be parsed (UTC) so compute_per_trade's ET block + killzone engage and
    # assign_blocks uses entry-EVENT minutes (not iid).
    csv_text = (
        "Trade #,Type,Date/Time,Price,Quantity,Profit,Risk,stop_dist\n"
        "1,Entry long,2026-06-18 12:00,5000,1,,1000,20\n"      # 12:00 UTC = 08:00 ET (nyam)
        "1,Exit long,2026-06-18 12:30,5040,1,2000,,\n"
        "2,Entry long,2026-06-18 12:00,5001,1,,1000,20\n"      # same arming minute as #1
        "2,Exit long,2026-06-18 12:45,5041,1,2000,,\n"
        "3,Entry long,2026-06-18 12:05,5002,1,,1000,20\n"      # a later minute -> own block
        "3,Exit long,2026-06-18 12:50,5042,1,2000,,\n"
    )
    p = tmp_path / "lot_no_epoch.csv"
    p.write_text(csv_text)
    trades, stats = H.load_list_of_trades(str(p))
    assert stats["n_paired"] == 3
    # entry epochs populated (NOT nan) from the Date/Time cell.
    for t in trades:
        assert not math.isnan(t.entry_epoch_ms), "entry_epoch_ms must be parsed from Date/Time"
    H.compute_per_trade(trades, mintick=0.1)
    # killzone resolves (12:00 UTC -> 08:00 ET in [07:00,10:00) = nyam), not all "out".
    assert any(t.killzone != "out" for t in trades)
    assert all(t.killzone == "nyam" for t in trades if t.trade_num in (1, 2))
    # assign_blocks yields ENTRY-EVENT blocks: trades #1 and #2 share the 12:00 minute
    # -> n_blocks (2) < n_trades (3); the auto/epoch path engaged (not trade-iid).
    nb, mode = H.assign_blocks(trades, key="auto")
    assert mode == "event"
    assert nb == 2 and nb < len(trades)
    t1 = [t for t in trades if t.trade_num == 1][0]
    t2 = [t for t in trades if t.trade_num == 2][0]
    t3 = [t for t in trades if t.trade_num == 3][0]
    assert t1.block_id == t2.block_id and t3.block_id != t1.block_id


# =============================================================================
# R6-2 / R8-2: iid fallback must be flagged (mode surfaced) and yield INSUFFICIENT-N
#              on a verdict-bearing export; stable block key (not id()).
# =============================================================================
def test_assign_blocks_iid_fallback_is_flagged():
    # no epochs anywhere -> assign_blocks must report mode=='iid' (not silent).
    trades = [_trade(1.0, block=-1, trade_num=k) for k in range(10)]  # entry_epoch_ms=nan
    nb, mode = H.assign_blocks(trades, key="auto")
    assert mode == "iid"
    assert nb == 10                     # one block per trade (stable key, deterministic)
    # stable key: re-running yields identical block ids (no nondeterministic id()).
    ids1 = [t.block_id for t in trades]
    H.assign_blocks(trades, key="auto")
    ids2 = [t.block_id for t in trades]
    assert ids1 == ids2


def test_verdict_insufficient_n_when_iid_fallback_on_verdict_export():
    # n>=100 BUT no epochs -> iid fallback -> the entry-event block instrument is
    # unavailable -> verdict must refuse a PASS and read INSUFFICIENT-N (PREREG-1M L62-63).
    rng = np.random.default_rng(31)
    labelled = {}
    bid = 0
    dows = [0, 1, 2, 3, 4]
    kzs = ["london", "nyam", "nypm", "out"]
    for label in H.ABLATION_LABELS:
        b, p, k = H._flags_from_label(label)
        base = -0.5 + 0.5 * b + 0.5 * p + 0.5 * k
        trades = []
        for j in range(120):
            t = _trade(float(base + rng.normal(0, 0.1)), block=bid,
                       dow=dows[j % 5], kz=kzs[j % 4], trade_num=bid)
            t.entry_epoch_ms = float("nan")   # force the iid fallback
            trades.append(t); bid += 1
        labelled[label] = trades
    # re-block via the harness path (assign_blocks key="auto") so the iid mode is detected.
    for label in H.ABLATION_LABELS:
        H.assign_blocks(labelled[label], key="auto")
    default = labelled["bias1_pd1_kz1"]
    r = H.verdict_for_variant(default, labelled, use_body=False, mintick=0.1,
                              boot_seed=32, perm_seed=33)
    assert r.verdict == "INSUFFICIENT-N"
    assert any("iid" in s.lower() for s in r.reasons)


# =============================================================================
# R6-3: multi-regime BINDING SPEC (Forbidden #4) -- single-regime window flagged.
# =============================================================================
def test_regime_span_single_side_is_flagged():
    # all entry dates in 2021 (one side of a 2023-06-15 split) -> single-regime window.
    import datetime as _dt
    dates = [_dt.date(2021, 3, d % 28 + 1) for d in range(20)]
    flagged, span = H.regime_span_check(dates, split="2023-06-15")
    assert flagged is True
    assert span[0] == _dt.date(2021, 3, 1) or span[0].year == 2021


def test_regime_span_both_sides_not_flagged():
    import datetime as _dt
    dates = [_dt.date(2021, 3, 1), _dt.date(2024, 9, 1)]   # spans the 2023-06-15 split
    flagged, span = H.regime_span_check(dates, split="2023-06-15")
    assert flagged is False


# =============================================================================
# R6-5: no risk AND no stop_dist column -> distinct R-basis diagnostic.
# =============================================================================
def test_no_r_basis_distinct_diagnostic():
    # neither risk nor stop_dist present for any trade -> r_net all nan.
    rows = _tv_rows([
        (1, "entry", "long", 5000.0, 1, None, None, None, None, None, None),
        (1, "exit",  "long", 5040.0, 1, 2000.0, None, None, None, None, None),
    ])
    trades, _ = H.pair_trades(rows, _colmap_for(rows))
    H.compute_per_trade(trades, mintick=0.1)
    diag = H.r_basis_diagnostic(trades)
    assert diag is not None
    assert "no risk and no stop_dist" in diag
    assert "0 of 1" in diag or "0 of" in diag


def test_expected_exports_count_is_16():
    # 8 ablation labels x 2 useBody variants, all gate-bearing range-extreme.
    needed = H._expected_exports()
    assert len(needed) == 16
    assert all("range-extreme" in f for f in needed)
    assert all("nearest-pool" not in f for f in needed)   # Forbidden #5: not in verdict set


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            # crude tmp_path shim for direct-run mode
            if "tmp_path" in fn.__code__.co_varnames:
                import tempfile
                with tempfile.TemporaryDirectory() as d:
                    fn(Path(d))
            else:
                fn()
            print(f"PASS {fn.__name__}"); passed += 1
        except AssertionError as ex:
            print(f"FAIL {fn.__name__}: {ex}")
        except Exception as ex:
            print(f"ERROR {fn.__name__}: {type(ex).__name__}: {ex}")
    print(f"\n{passed}/{len(fns)} passed")
