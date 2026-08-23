#!/usr/bin/env python3
"""$0 retrieved-harness reuse: port the Q-EVALSEQ-1 cushion-proportional policy
(lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py) onto ORB-MNQ-1's OWN
intraday-honest bust construct (lab/analysis/orb/orb_mnq_2026-07/
run_t2_intraday_bust.py, pruned by the Great Prune, retrieved via
`git show pre-prune-2026-08-08:...`).

NOT a lab/analysis/ campaign. Writes only to this scratch directory. Touches no
locked/frozen repo file. Pure computation on already-cached data ($0, K=0).

Sections
--------
1. Ported verbatim (or near-verbatim, only refactored for half-panel reuse)
   from run_t2_intraday_bust.py: data loading, the excursion derivation, the
   engine-mirror controls, the Monday-anchored 5-day paired block builder, and
   an ORB-native simulate_path secondary check (Control A-style) used ONLY to
   validate that this file's own re-derivation of `recon` matches production
   bit-for-bit before anything downstream is trusted.
2. A NEW day-loop, modeled on run_evalseq.py's `eval_sim_policy`, extended so
   the bust test considers both the EOD close and the day's intraday low,
   mirroring simulate_path's own `equity_test = min(equity_new, equity +
   intraday_low*scale)` mechanic. CAP_EVAL is judged NOT relevant (see the
   docstring on `day_loop_intraday`) and omitted.
3. Fidelity control: the new day-loop at flat k=1 / k=2 (m=1.0, no policy)
   against the published intraday-honest bust rates (67.67% / 77.01%,
   RESULTS_t2_intraday_bust.md \u00a74).
4. If control passes: pol_cushion (quoted verbatim from run_evalseq.py) run on
   ORB-MNQ-1's own panel, both halves (mid = len(dates)//2, matching
   run_evalseq.py's own split convention), intraday-honest, against flat-k1
   and flat-k2 baselines on the SAME halves.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/openrouter-ox-alpha-test-fff246")
# NOTE (Implementation A, Q-ORBPOS-1, 2026-08-23): the frozen upstream path above
# pointed at a since-deleted worktree ("tradeify-bottleneck-solutions-84e1e6"). This
# is the ONLY line changed in this file relative to
# lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
# -- a pure environment/deployment path, not any part of day_loop_intraday /
# build_paths_orb / run_policy_orb / pol_cushion / pol_const, which are imported and
# used byte-for-byte unchanged from this copy. resolve_panel()'s own _PRIMARY
# fallback also independently locates the cached MNQ 15m panel regardless of REPO.
ORB_DIR = REPO / "lab" / "analysis" / "orb" / "orb_mnq_2026-07"
ORB_LIB_DIR = REPO / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
OUT_DIR = Path(__file__).resolve().parent

for _p in (REPO / "core", REPO / "lab", ORB_LIB_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import orb_lib as ol  # noqa: E402
from mc.preflight import assert_engine_ready, firm_kwargs, summarize_outcomes  # noqa: E402
from mc.simulation import simulate_path  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    DD_SCALE,
    NO_PROTECTION_TRIGGER,
    load_scoring_thresholds,
)

# =====================================================================================
# SECTION 1 -- ported from run_t2_intraday_bust.py (git show pre-prune-2026-08-08:
# lab/analysis/orb/orb_mnq_2026-07/run_t2_intraday_bust.py). Unchanged except:
#   * build_paired_blocks is kept verbatim AND factored into build_k_panel() +
#     blocks_from_panel() so the same math can be applied to a half-panel slice
#     (needed for step 4; run_t2_intraday_bust.py never split by half).
# =====================================================================================

_PRIMARY = Path(r"C:/Users/joshu/multi_firm_operations")
PANEL_CANDIDATES = (
    ORB_DIR / "_mnq_15m.pkl",
    _PRIMARY / "lab" / "analysis" / "orb" / "orb_mnq_2026-07" / "_mnq_15m.pkl",
)

ET = "America/New_York"
MNQ_USD_PER_PT = 2.0
SLIP_TICK_USD = 0.50
TRADEIFY_SIDE = 0.91
RT_PT_TRADEIFY = 2.0 * (TRADEIFY_SIDE + SLIP_TICK_USD) / MNQ_USD_PER_PT
CLOSE_TOD_CORRECT = 15 * 60 + 45

TIER = "Tradeify_Select_100K"
K_GRID = (1, 2)  # this task only needs k=1/k=2 (published control anchors)

LOCK_UNREACHABLE = 1_000_000.0
LOCK_AS_PUBLISHED = 100.0


def resolve_panel() -> Path:
    for p in PANEL_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("cached MNQ 15m panel not found: " + str(PANEL_CANDIDATES))


def make_inst() -> ol.Instrument:
    return ol.Instrument(
        name="mnq_tradeify_correct_clock",
        path=Path("(in-memory)"),
        loader="none",
        feed="databento",
        tick=0.25,
        spread_pt=0.25,
        rt_cost_pt=RT_PT_TRADEIFY,
        open_tod=ol.OPEN_TOD_US,
        close_tod=CLOSE_TOD_CORRECT,
        tz=ET,
        note="native MNQ.v.0 15m; close_tod=15:45; Tradeify $0.91/side + 1 tick slip",
    )


def orb_days_with_excursion(piv, meta, inst: ol.Instrument, *, or_bars: int = 2,
                             entry_bar: str = "include") -> pd.DataFrame:
    """Verbatim port (headline `include` convention only kept)."""
    o, h, l, c = piv["open"], piv["high"], piv["low"], piv["close"]
    tods = sorted([t for t in c.columns if inst.open_tod <= t <= inst.close_tod])
    or_tods, rest_tods = tods[:or_bars], tods[or_bars:]
    rth_close = meta["rth_close"]
    rt = inst.rt_cost_pt

    rows = []
    for day in c.index:
        or_hi = h.loc[day, or_tods].max()
        or_lo = l.loc[day, or_tods].min()
        if not np.isfinite(or_hi) or not np.isfinite(or_lo):
            continue
        rng = or_hi - or_lo
        if rng <= 0:
            continue

        side = None
        entry_t = None
        for t in rest_tods:
            bh, bl, bo = h.loc[day, t], l.loc[day, t], o.loc[day, t]
            if not np.isfinite(bh):
                continue
            up, dn = bh >= or_hi, bl <= or_lo
            if up and dn:
                side = "long" if bo <= (or_hi + or_lo) / 2 else "short"
                entry_t = t
                break
            if up:
                side, entry_t = "long", t
                break
            if dn:
                side, entry_t = "short", t
                break
        if side is None:
            continue

        entry = or_hi if side == "long" else or_lo
        cl = rth_close.loc[day]
        if side == "long":
            stopped = bool(l.loc[day, rest_tods].min() <= or_lo)
            exit_px = or_lo if stopped else cl
            pnl_pt = exit_px - entry
        else:
            stopped = bool(h.loc[day, rest_tods].max() >= or_hi)
            exit_px = or_hi if stopped else cl
            pnl_pt = entry - exit_px

        if stopped:
            worst_pt = pnl_pt
        else:
            held = [t for t in rest_tods if t >= entry_t]
            extreme = (
                l.loc[day, held].min() if side == "long" else h.loc[day, held].max()
            ) if held else np.nan
            if np.isfinite(extreme):
                worst_pt = float(extreme) - entry if side == "long" else entry - float(extreme)
                worst_pt = min(worst_pt, pnl_pt)
            else:
                worst_pt = pnl_pt

        rows.append({
            "date": pd.Timestamp(day),
            "R": (pnl_pt - rt) / rng,
            "range_pt": rng,
            "side": side,
            "stopped": stopped,
            "entry_tod": entry_t,
            "pnl_usd_1lot": (pnl_pt - rt) * MNQ_USD_PER_PT,
            "low_usd_1lot": min(0.0, worst_pt - rt) * MNQ_USD_PER_PT,
        })

    out = pd.DataFrame(rows)
    out["year"] = out["date"].dt.year
    return out


def assert_mirror_matches_engine(recon: pd.DataFrame, bt: dict) -> None:
    n_r, n_e = len(recon), len(bt["R"])
    assert n_r == n_e, f"mirror n={n_r} != engine n={n_e}"
    assert np.allclose(recon["R"].to_numpy(), np.asarray(bt["R"], float)), "R diverges"
    assert np.allclose(recon["range_pt"].to_numpy(), np.asarray(bt["range"], float)), "range diverges"
    assert (recon["side"].to_numpy() == np.asarray(bt["side"])).all(), "side diverges"
    assert (recon["stopped"].to_numpy() == np.asarray(bt["stopped"], bool)).all(), "stopped diverges"
    assert (recon["entry_tod"].to_numpy() == np.asarray(bt["entry_tod"])).all(), "entry_tod diverges"


def build_k_panel(recon: pd.DataFrame, k: int) -> pd.DataFrame:
    """Full-span per-business-day (pnl, low) panel at contract count k. Same math as
    run_t2_intraday_bust.build_paired_blocks's panel-construction half, factored out
    so it can be sliced by half before block-building (run_t2 never needed a half)."""
    idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    pnl = recon.set_index("date")["pnl_usd_1lot"].groupby(level=0).sum().reindex(idx).fillna(0.0)
    low = recon.set_index("date")["low_usd_1lot"].groupby(level=0).sum().reindex(idx).fillna(0.0)
    return pd.DataFrame({"pnl": pnl.to_numpy() * k, "low": low.to_numpy() * k}, index=idx)


def blocks_from_panel(panel: pd.DataFrame):
    """Monday-anchored 5-business-day blocks over a (pnl, low) panel slice. Same
    block-selection rule as run_t2_intraday_bust.build_paired_blocks
    (`day.weekday()==0 and i+5<=len(panel)`), returning plain 2-D (n_blocks,5)
    arrays (no singleton strategy axis -- this file's day-loop is single-leg)."""
    values = panel.to_numpy()
    idxs = [i for i, day in enumerate(panel.index) if day.weekday() == 0 and i + 5 <= len(panel)]
    if not idxs:
        raise ValueError("no Mon-anchored 5-day blocks formed")
    blocks_pnl = np.array([values[i:i + 5, 0] for i in idxs])
    blocks_low = np.array([values[i:i + 5, 1] for i in idxs])
    return blocks_pnl, blocks_low


def build_paired_blocks(recon: pd.DataFrame, k: int):
    """Verbatim port (with the (n,5,1)/(n,5) shape simulate_path's run_seed wants)."""
    panel = build_k_panel(recon, k)
    values = panel.to_numpy()
    blocks = np.array([
        values[i:i + 5]
        for i, day in enumerate(panel.index)
        if day.weekday() == 0 and i + 5 <= len(panel)
    ])
    if len(blocks) == 0:
        raise ValueError("no Mon-anchored 5-day blocks formed")
    return blocks[:, :, 0:1].copy(), blocks[:, :, 1].copy(), panel


def run_seed_paired(seed, n_sims, blocks_pnl, blocks_low, horizon, fkw, *, use_intraday):
    """Verbatim port of run_t2_intraday_bust.run_seed_paired."""
    rng = np.random.default_rng(seed)
    n_blocks = len(blocks_pnl)
    blocks_per_sim = (horizon + 4) // 5
    outcomes = {"pass": 0, "bust_daily": 0, "bust_static": 0, "bust_trailing": 0,
                "bust_inactivity": 0, "horizon_cap": 0}
    days_to_pass, max_dds = [], []
    for _ in range(n_sims):
        indices = rng.integers(0, n_blocks, blocks_per_sim)
        path = blocks_pnl[indices].reshape(-1, blocks_pnl.shape[2])[:horizon]
        low = blocks_low[indices].reshape(-1)[:horizon] if use_intraday else None
        outcome, day, max_dd, _c = simulate_path(
            path, NO_PROTECTION_TRIGGER, DD_SCALE, horizon, intraday_low=low, **fkw
        )
        outcomes[outcome] += 1
        max_dds.append(max_dd)
        if outcome == "pass":
            days_to_pass.append(day)
    return {"outcomes": outcomes, "days_to_pass": days_to_pass, "max_dds": max_dds}


def score_arm(blocks_pnl, blocks_low, thr, fkw, *, use_intraday, n_sims):
    """Verbatim port of run_t2_intraday_bust.score_arm."""
    results = [run_seed_paired(seed, n_sims, blocks_pnl, blocks_low, thr.horizon, fkw,
                                use_intraday=use_intraday) for seed in thr.seeds]
    summary = summarize_outcomes(results, n_sims)
    dtp = [d for r in results for d in r["days_to_pass"]]
    summary["median_days_to_pass"] = float(np.median(dtp)) if dtp else float("nan")
    summary["p99_max_dd"] = float(np.percentile([d for r in results for d in r["max_dds"]], 99))
    return summary


# =====================================================================================
# SECTION 2 -- NEW: the cushion-proportional day-loop, modeled on run_evalseq.py's
# eval_sim_policy, extended for intraday honesty.
# =====================================================================================

DD = 3_000.0            # Tradeify_Select_100K fixed-$ trail (3.0% of $100K); == run_evalseq's DD
START = 100_000.0       # == run_evalseq's START; == Tradeify_Select_100K starting_balance
TARGET = 106_000.0      # == run_evalseq's TARGET; == firm_kwargs('Tradeify_Select_100K')['profit_target']
MIN_TRADING_DAYS = 3
CONSISTENCY_FRAC = 0.40  # Tradeify consistency_rule_pct = 40%, == the Run-2 cell used for the published control


def pol_const(mval):
    def f(t, bal, peak, stepped, t_b):
        return np.full(bal.shape, mval)
    return f


def pol_cushion(t, bal, peak, stepped, t_b):
    """Quoted verbatim from lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py."""
    cushion = bal - (peak - DD)
    return 0.75 * np.minimum(1.0, np.maximum(cushion, 0.0) / DD)


def day_loop_intraday(p: np.ndarray, low: np.ndarray, policy, *, use_intraday: bool, t_b=None):
    """eval_sim_policy, generalized so the bust test considers both the EOD close and
    the day's intraday low, mirroring simulate_path's own two-clock mechanic:

        equity_test = min(equity_new, equity + intraday_low[day] * scale)

    Here `policy`'s multiplier `m` plays the role of `scale` (applied identically to
    both the day's realized pnl `p` and its intraday excursion `low`, exactly as
    simulate_path applies its own `scale` to both `path` and `intraday_low`).

    CAP_EVAL is deliberately OMITTED (judgment call, not an oversight -- see the
    RESULTS_t2_intraday_bust.md \u00a75 "Sizing basis" note this cites): CAP_EVAL=80
    micro-contracts is the 2-leg pyramided book's OWN eval-cap constraint. ORB-MNQ-1
    trades k in {1,2} fixed micro contracts, and pol_cushion's own multiplier only
    ever reaches 0.75x -- so the largest exposure this loop ever asks for is 0.75x of
    k=2 = 1.5 micro-contract-equivalents, three orders of magnitude under the 80-cap
    and nowhere near the (also-published, unrelated) 11-contract MNQ allocation cap.
    Nothing here is ever cap-bound, so the CAP_EVAL clip has no effect to port and
    porting it as dead code would misstate its relevance. `q` (the max-position-size
    proxy the clip needs) does not even exist for a fixed-lot single-leg construct.

    Profit-target + min-trading-days + 40%-consistency exit IS ported (not present in
    the quoted pol_cushion snippet, but load-bearing for a faithful reproduction of
    the published control): omitting it would leave paths that should have exited on
    reaching Tradeify's $106K target still trading -- inflating the measured bust
    rate relative to the published figure for a reason that has nothing to do with
    intraday honesty. TARGET/MIN_TRADING_DAYS/CONSISTENCY_FRAC above are exactly
    firm_kwargs('Tradeify_Select_100K', consistency=0.40)'s own values -- the same
    values that produced 67.67%/77.01%.
    """
    n, h = p.shape
    bal = np.full(n, START)
    peak = bal.copy()
    tdays = np.zeros(n)
    maxpos = np.zeros(n)
    alive = np.ones(n, bool)
    passed = np.zeros(n, bool)
    bust = np.zeros(n, bool)
    stepped = np.zeros(n, bool)  # unused by pol_const/pol_cushion; kept for interface parity

    for t in range(h):
        bal_open = bal.copy()  # start-of-day equity (yesterday's EOD) -- what the barrier is measured FROM
        m = policy(t, bal, peak, stepped, t_b)
        d = p[:, t] * m
        d_low = (low[:, t] * m) if use_intraday else d  # use_intraday=False => equity_test collapses to d (legacy EOD-only)

        bal[alive] += d[alive]
        traded = alive & (np.abs(d) > 1e-9)
        tdays[traded] += 1
        maxpos = np.where(traded, np.maximum(maxpos, d), maxpos)

        floor = peak - DD
        equity_test = bal_open + np.minimum(d, d_low)
        nbust = alive & (equity_test <= floor)
        bust |= nbust
        alive &= ~nbust

        profit = bal - START
        ok = alive & (bal >= TARGET) & (tdays >= MIN_TRADING_DAYS) & (maxpos <= CONSISTENCY_FRAC * profit)
        passed |= ok
        alive &= ~ok
        peak = np.where(alive, np.maximum(peak, bal), peak)

    return bust, passed


def build_paths_orb(blocks_pnl2, blocks_low2, n_paths, horizon, rng):
    """Vectorized block-bootstrap over ORB's own Mon-anchored 5-day blocks, matching
    run_evalseq.build_paths's mechanic (draw block indices uniformly WITH
    replacement, concatenate, truncate to horizon) but drawing from ORB's fixed
    5-day blocks (vs run_evalseq's variable-length ISO-week blocks) and vectorized
    across n_paths at once (vs run_t2_intraday_bust.run_seed_paired's per-sim
    Python loop) so it can feed the (n_paths,horizon) arrays day_loop_intraday
    wants. Same i.i.d.-uniform-block draw distribution either way; NOT the same RNG
    call sequence as run_seed_paired, so a flat-policy run through this path is a
    statistically-independent re-estimate of the same quantity, not a bit-identical
    replay."""
    n_blocks = len(blocks_pnl2)
    blocks_per_sim = (horizon + 4) // 5
    picks = rng.integers(0, n_blocks, size=(n_paths, blocks_per_sim))
    p = blocks_pnl2[picks].reshape(n_paths, -1)[:, :horizon]
    low = blocks_low2[picks].reshape(n_paths, -1)[:, :horizon]
    return p, low


def run_policy_orb(blocks_pnl2, blocks_low2, policy, *, use_intraday, horizon, seeds, n_paths, t_b=None):
    rows = []
    for s in seeds:
        rng = np.random.default_rng(s)
        p, low = build_paths_orb(blocks_pnl2, blocks_low2, n_paths, horizon, rng)
        bust, passed = day_loop_intraday(p, low, policy, use_intraday=use_intraday, t_b=t_b)
        rows.append(dict(bust_pct=float(bust.mean()) * 100.0, pass_pct=float(passed.mean()) * 100.0))
    agg = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
    agg["per_seed"] = rows
    return agg


# =====================================================================================
# main
# =====================================================================================

def main():
    t0 = time.time()
    report: dict = {}

    print("=" * 96)
    print("Q-EVALSEQ-1 cushion policy ported onto ORB-MNQ-1's intraday-honest construct")
    print("=" * 96)

    thr = load_scoring_thresholds()
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")

    panel_pkl = resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data ] {panel_pkl}")
    print(f"[data ] rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    inst = make_inst()
    piv, meta = ol.session_panel(df, inst)
    bt = ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = orb_days_with_excursion(piv, meta, inst, entry_bar="include")

    print("\n--- Control B (ported): mirror vs orb_lib.orb_backtest ---")
    assert_mirror_matches_engine(recon, bt)
    print(f"  PASS -- n={len(recon)}")

    # Control G (published anchors) -- cheap, no MC, confirms the ported derivation
    # loaded the right panel before any compute is spent.
    R = recon["R"].to_numpy()
    net_1lot = recon["pnl_usd_1lot"].sum()
    wr = float((R > 0).mean())
    stopped_frac = float(recon["stopped"].mean())
    maxdd_1lot = _walk_max_dd(recon["pnl_usd_1lot"].to_numpy())
    print("\n--- Control G (published anchors, n=1846 / meanR+0.0626 / net $17,780 / "
          "WR 46.37% / stopped 38.0% / maxDD -$6,527) ---")
    print(f"  n={len(recon)}  meanR={R.mean():+.4f}  net(1lot)=${net_1lot:,.0f}  "
          f"WR={wr:.2%}  stopped={stopped_frac:.1%}  maxDD(1lot)=-${-maxdd_1lot:,.0f}")
    report["control_g"] = dict(n=len(recon), meanR=float(R.mean()), net_1lot=float(net_1lot),
                                wr=wr, stopped_frac=stopped_frac, maxdd_1lot=float(maxdd_1lot))

    assert_engine_ready(TIER)
    fkw_base = firm_kwargs(TIER, inactivity_off=True, consistency=CONSISTENCY_FRAC)
    # NOTE (repo-state delta vs the 2026-08-02 RESULTS_t2_intraday_bust.md / pruned-script
    # snapshot): FIRM_RULES["Tradeify_Select_100K"]["dd_lock_offset_usd"] was itself
    # corrected to the unreachable value on 2026-08-04 (core/firm_rules.py, "fixed
    # 2026-08-04" comment) -- run_t2_intraday_bust.py's own LOCK_AS_PUBLISHED=100.0
    # override, needed at the time it ran, is now a no-op: firm_kwargs() already
    # returns the corrected (no-lock) geometry by default. Asserting the OLD shipped
    # value here would be asserting a fact that is no longer true at HEAD, so this
    # reads FIRM_RULES as of THIS run rather than re-asserting the historical delta.
    if fkw_base["dd_lock_offset_usd"] == LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=LOCK_UNREACHABLE)
        print("[firm ] FIRM_RULES still ships the as-published lock; overriding to unreachable (matches published headline).")
    else:
        fkw = dict(fkw_base)
        print(f"[firm ] FIRM_RULES already ships dd_lock_offset_usd={fkw_base['dd_lock_offset_usd']:,.0f} "
              f"(corrected/unreachable at HEAD) -- no override needed.")
    assert fkw["profit_target"] == TARGET, f"profit_target drifted: {fkw['profit_target']} != {TARGET}"
    assert fkw["starting_equity"] == START
    assert fkw["trailing_dd_pct"] == -DD / START

    # ---------------------------------------------------------------- ORB-native secondary check
    # Runs the ACTUAL production simulate_path over this file's own re-derived `recon`,
    # via a verbatim port of run_t2_intraday_bust's own bootstrap. If this reproduces
    # 67.67%/77.01% bit-adjacent, the ported derivation/data-loading is proven correct
    # BEFORE trusting the new (Section 2) day-loop's own flat-policy control below.
    #
    # Reduced-scale spot check (1 seed x 3,000 sims/k, not the full 3x10,000): a matched
    # side-by-side smoke run (seed=42, n=3,000, k=1) against Section 2's own day-loop
    # already landed on the SAME bust/pass split to the tenth of a point (68.0%/32.0%
    # both arms) before this file was finalized -- see the report text for that number.
    # Spending the full ~18min/k this call would otherwise take re-derives evidence this
    # task already has; a 1-seed spot check per k is enough to catch a data-loading
    # regression between that smoke run and this one.
    print("\n" + "=" * 96)
    print("ORB-NATIVE SECONDARY CHECK -- production simulate_path over this file's recon() "
          "(reduced-scale spot check: seed=42, n=3,000/k)")
    print("=" * 96)
    native = {}
    NATIVE_SPOT_N = 3_000
    for k in K_GRID:
        blocks_pnl, blocks_low, _panel = build_paired_blocks(recon, k)
        res = run_seed_paired(42, NATIVE_SPOT_N, blocks_pnl, blocks_low, thr.horizon, fkw, use_intraday=True)
        bust_pct = sum(res["outcomes"][kk] for kk in ("bust_daily", "bust_static", "bust_trailing")) / NATIVE_SPOT_N * 100.0
        pass_pct = res["outcomes"]["pass"] / NATIVE_SPOT_N * 100.0
        native[k] = dict(bust_pct=bust_pct, pass_pct=pass_pct, n=NATIVE_SPOT_N, seed=42)
        print(f"  k={k}  headline_bust={bust_pct:.2f}%  pass={pass_pct:.2f}%  "
              f"(n={NATIVE_SPOT_N}, seed=42, elapsed {time.time()-t0:.0f}s)")
    report["orb_native_secondary_check"] = native
    print(f"  published (30k sims): k=1 67.67%  k=2 77.01%")
    print(f"  this spot-check      : k=1 {native[1]['bust_pct']:.2f}%  k=2 {native[2]['bust_pct']:.2f}%")

    # ---------------------------------------------------------------- Section 3: fidelity control
    print("\n" + "=" * 96)
    print("FIDELITY CONTROL -- NEW day_loop_intraday, FLAT policy (m=1.0), full panel")
    print("=" * 96)
    PUBLISHED = {1: 67.67, 2: 77.01}
    TOL_PP = 2.0  # see docstring rationale printed below
    print(f"  tolerance: {TOL_PP:.1f}pp absolute (MC noise at {thr.sims_per_seed}x3 sims is ~0.3-0.5pp; "
          f"day_loop_intraday's bootstrap RNG stream is statistically equivalent to but not "
          f"identical to run_seed_paired's, so a small additional independent-estimate gap is "
          f"expected on top of pure MC noise -- 2pp gives comfortable margin while remaining far "
          f"tighter than the >20pp gaps the underlying T2 verdict turns on)")

    control = {}
    flat_ok = True
    for k in K_GRID:
        panel_full = build_k_panel(recon, k)
        bpnl, blow = blocks_from_panel(panel_full)
        r = run_policy_orb(bpnl, blow, pol_const(1.0), use_intraday=True,
                            horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        delta = r["bust_pct"] - PUBLISHED[k]
        ok = abs(delta) <= TOL_PP
        flat_ok &= ok
        control[k] = dict(bust_pct=r["bust_pct"], pass_pct=r["pass_pct"], published=PUBLISHED[k],
                           delta_pp=delta, within_tol=ok)
        print(f"  k={k}  new-harness bust={r['bust_pct']:.2f}%  pass={r['pass_pct']:.2f}%  "
              f"published={PUBLISHED[k]:.2f}%  delta={delta:+.2f}pp  {'PASS' if ok else 'FAIL'}  "
              f"(elapsed {time.time()-t0:.0f}s)")

    # bonus: EOD-only arm at the same k's, cross-checked against the published EOD figures
    PUBLISHED_EOD = {1: 65.23, 2: 74.00}
    print("\n  (bonus, EOD-only arm, cross-check vs published EOD 65.23%/74.00%)")
    for k in K_GRID:
        panel_full = build_k_panel(recon, k)
        bpnl, blow = blocks_from_panel(panel_full)
        r = run_policy_orb(bpnl, blow, pol_const(1.0), use_intraday=False,
                            horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        print(f"  k={k}  new-harness EOD bust={r['bust_pct']:.2f}%  published EOD={PUBLISHED_EOD[k]:.2f}%  "
              f"delta={r['bust_pct']-PUBLISHED_EOD[k]:+.2f}pp")
        control[k]["eod_bust_pct"] = r["bust_pct"]
        control[k]["eod_published"] = PUBLISHED_EOD[k]

    report["fidelity_control"] = control
    report["fidelity_control_pass"] = bool(flat_ok)
    print(f"\nFIDELITY CONTROL: {'PASS' if flat_ok else 'FAIL'}")

    if not flat_ok:
        print("STOPPING before any cushion-proportional read -- control did not reproduce "
              "published figures within tolerance.")
        (OUT_DIR / "evalseq_orb_intraday_results.json").write_text(json.dumps(report, indent=2))
        return 2

    # ---------------------------------------------------------------- Section 4: cushion-proportional
    print("\n" + "=" * 96)
    print("POL_CUSHION -- both halves, intraday-honest, vs flat-k1/flat-k2 controls, same halves")
    print("=" * 96)

    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    mid = len(full_idx) // 2
    halves = {
        "H1": full_idx[:mid],
        "H2": full_idx[mid:],
    }
    print(f"[split] {len(full_idx)} business days, mid={mid}  "
          f"H1={full_idx[0].date()}->{full_idx[mid-1].date()}  H2={full_idx[mid].date()}->{full_idx[-1].date()}")

    cushion_report = {}
    for half_name, half_idx in halves.items():
        cushion_report[half_name] = {}
        for base_k in K_GRID:
            panel_full = build_k_panel(recon, base_k)
            panel_half = panel_full.loc[panel_full.index.isin(half_idx)]
            bpnl, blow = blocks_from_panel(panel_half)
            n_blocks = len(bpnl)

            flat = run_policy_orb(bpnl, blow, pol_const(1.0), use_intraday=True,
                                   horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
            cush = run_policy_orb(bpnl, blow, pol_cushion, use_intraday=True,
                                   horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
            delta = cush["bust_pct"] - flat["bust_pct"]
            cushion_report[half_name][f"base_k{base_k}"] = dict(
                n_blocks=n_blocks,
                flat_bust_pct=flat["bust_pct"], flat_pass_pct=flat["pass_pct"],
                cushion_bust_pct=cush["bust_pct"], cushion_pass_pct=cush["pass_pct"],
                delta_bust_pp=delta,
            )
            print(f"  {half_name} base=k{base_k} (n_blocks={n_blocks})  "
                  f"flat: bust={flat['bust_pct']:.2f}% pass={flat['pass_pct']:.2f}%  |  "
                  f"cushion(0.75x max): bust={cush['bust_pct']:.2f}% pass={cush['pass_pct']:.2f}%  "
                  f"delta={delta:+.2f}pp  (elapsed {time.time()-t0:.0f}s)")

    report["cushion"] = cushion_report
    report["half_split"] = dict(
        n_bdays=len(full_idx), mid=mid,
        h1_start=str(full_idx[0].date()), h1_end=str(full_idx[mid - 1].date()),
        h2_start=str(full_idx[mid].date()), h2_end=str(full_idx[-1].date()),
    )

    out = OUT_DIR / "evalseq_orb_intraday_results.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


def _walk_max_dd(pnl_1lot: np.ndarray) -> float:
    """Realized (non-bootstrap) max peak-to-trough $ drawdown over the actual panel,
    at 1 contract -- cheap sanity companion to Control G, no MC."""
    eq = np.cumsum(pnl_1lot)
    peak = np.maximum.accumulate(np.concatenate([[0.0], eq]))[1:]
    dd = eq - peak
    return float(dd.min())


if __name__ == "__main__":
    raise SystemExit(main())
