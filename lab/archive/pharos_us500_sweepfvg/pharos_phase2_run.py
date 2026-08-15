#!/usr/bin/env python3
# =============================================================================
# PHAROS — Phase-2 VERDICT RUN  (Q-ICT-SWEEPFVG-1)
# -----------------------------------------------------------------------------
# Lifts the firewall under the LOCKED pre-registration
# (docs/briefs/pre-registration/Q-ICT-SWEEPFVG-1-verdict-preregistration.md,
#  pre-registration lock commit, 2026-06-17).
#
# DISCIPLINE: the frozen test object is reused VERBATIM by importing
# pharos_outcome_sim (resolve_setup / load_bars / load_setups /
# run_population / assert_population_identity). The ONLY new logic here is the
# two pre-registered corrections, both frozen blind to outcomes:
#   (1) tradeability floor : drop stop_dist < max(1pt, spread+slip)  [runtime filter]
#   (2) block resampling   : CI + direction-permutation keyed on fvg_bar (effective N)
# Point estimates use all tradeable rows; CIs/permutation resample BLOCKS.
# Costs frozen: rt_spread 0.8 + slippage 0.2 (total 1.0pt). Hurdle locked 0.2883R.
# =============================================================================
import numpy as np, pandas as pd, sys
import pharos_outcome_sim as sim

RT, SL = 0.8, 0.2
FLOOR  = max(1.0, RT + SL)
HURDLE = 0.2883                      # §8 locked
BARS   = "PEPPERSTONE_US500, 15_1ca49.csv"
SETUPS = "setups.csv"
B, K, SEED = 10000, 10000, 0

def block_means(df, col, B, seed):
    rng = np.random.default_rng(seed)
    blocks = [g[col].values for _, g in df.groupby("fvg_bar")]
    nb = len(blocks)
    out = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, nb, nb)
        out[b] = np.concatenate([blocks[i] for i in pick]).mean()
    return out

def iid_means(v, B, seed):
    rng = np.random.default_rng(seed)
    return v.values[rng.integers(0, len(v), size=(B, len(v)))].mean(axis=1)

def mirror_worst_R(bars, row):
    """Mirror geometry (reflect stop/target about entry, flip dir), worst-order R.
    Faithful copy of pharos_outcome_sim.direction_permutation's per-row mirror."""
    high, low, n = bars["high"].values, bars["low"].values, len(bars)
    e, st, tg = row["entry"], row["stop"], row["target"]
    m_dir = "short" if row["direction"] == "long" else "long"
    m_stop, m_tgt = 2*e - st, 2*e - tg
    sd = abs(e - m_stop); rwin = abs(m_tgt - e)/sd; cR = (RT+SL)/sd
    fb = int(row["fill_bar"])
    for j in range(fb, n):
        if m_dir == "long":
            ht, hs = high[j] >= m_tgt, low[j] <= m_stop
        else:
            ht, hs = low[j] <= m_tgt, high[j] >= m_stop
        if ht and hs: return -1.0 - cR          # worst-order
        if ht: return rwin - cR
        if hs: return -1.0 - cR
    return np.nan                                # censored

def main():
    sim.assert_population_identity(SETUPS)       # md5 b1e3ba85 guard
    bars   = sim.load_bars(BARS)
    setups = sim.load_setups(SETUPS)             # complete only
    out    = sim.run_population(bars, setups, RT, SL).reset_index(drop=True)
    out["fvg_bar"] = setups["fvg_bar"].values    # block id (direction already present)

    n_complete = len(out)
    out = out[out["stop_dist"] >= FLOOR].reset_index(drop=True)   # (1) floor
    n_trad = len(out)
    med_cR = out["cost_R"].median(); hurdle_chk = 4*med_cR

    print("="*70); print("PHAROS PHASE-2 VERDICT — Q-ICT-SWEEPFVG-1  (firewall lifted under the committed pre-registration)"); print("="*70)
    print(f"cost            : rt_spread {RT} + slippage {SL} = {RT+SL}pt  | floor {FLOOR}pt")
    print(f"population      : complete {n_complete} -> tradeable {n_trad} (dropped {n_complete-n_trad})")
    print(f"hurdle check    : 4*median cost_R {med_cR:.4f} = {hurdle_chk:.4f}R  (locked {HURDLE}R)")
    assert abs(hurdle_chk - HURDLE) < 0.005, "HURDLE DRIFT vs lock — abort"

    res = out[out["status"].isin(["win","loss","ambiguous"])].copy()
    print(f"status          : {out['status'].value_counts().to_dict()}")
    print(f"resolved        : {len(res)}  by dir {res['direction'].value_counts().to_dict()}  blocks {res['fvg_bar'].nunique()}")

    gate = {}
    for order in ("best","worst"):
        col = "R_best" if order=="best" else "R_worst"
        v = res[col]; mean = v.mean()
        bm = block_means(res, col, B, SEED); im = iid_means(v, B, SEED)
        lo,hi  = np.percentile(bm,[2.5,97.5]); ilo,ihi = np.percentile(im,[2.5,97.5])
        dt3 = np.sort(v.values)[:-3].mean() if len(v)>3 else float('nan')
        sub = res.sort_values("sweep_ts_et"); _ix = np.array_split(np.arange(len(sub)), 3)
        thirds = [sub.iloc[i][col].mean() for i in _ix]
        print(f"\n--- {order.upper()}-ORDER ---")
        print(f"  mean {mean:+.3f}R   WR {(v>0).mean():.3f}   n {len(v)}")
        print(f"  block 95% CI [{lo:+.3f}, {hi:+.3f}]    (iid [{ilo:+.3f}, {ihi:+.3f}])")
        print(f"  P(block mean <=0) {(bm<=0).mean():.3f}   P(block mean >= hurdle) {(bm>=HURDLE).mean():.3f}")
        print(f"  drop-top-3 {dt3:+.3f}R   thirds {['%+.3f'%t for t in thirds]}")
        gate[order] = dict(mean=mean, lo=lo, dt3=dt3, thirds=thirds)

    # (2) direction permutation — BLOCK version, worst-order
    res = res.copy(); res["obs"] = res["R_worst"]
    res["mir"] = [mirror_worst_R(bars, r) for _, r in res.iterrows()]
    pp = res.dropna(subset=["mir"]).copy()
    obs_mean = pp["obs"].mean(); mir_mean = pp["mir"].mean()
    blk = list(pp.groupby("fvg_bar"))
    rng = np.random.default_rng(SEED); perm = np.empty(K)
    for k in range(K):
        flips = rng.random(len(blk)) < 0.5
        vals = np.concatenate([ (g["mir"].values if f else g["obs"].values) for f,(_,g) in zip(flips, blk) ])
        perm[k] = vals.mean()
    p_perm = (perm >= obs_mean).mean()
    print(f"\n--- DIRECTION PERMUTATION (block by fvg_bar, worst-order) ---")
    print(f"  obs {obs_mean:+.3f}R  vs mirror {mir_mean:+.3f}R   n {len(pp)} / blocks {len(blk)}")
    print(f"  P(perm >= obs) {p_perm:.4f}   (gate: < 0.05)")

    # ---- §6 GATE ----
    g = gate
    pos_thirds = sum(t>0 for t in g["worst"]["thirds"])
    both_sides = pp["direction"].nunique()==2 and (res["direction"]=="long").any() and (res["direction"]=="short").any()
    crit = {
      "best mean >= hurdle":      g["best"]["mean"]  >= HURDLE,
      "worst mean >= hurdle":     g["worst"]["mean"] >= HURDLE,
      "worst 95% CI lower >= 0":  g["worst"]["lo"]   >= 0,
      "perm block-p < 0.05":      p_perm < 0.05,
      "drop-top-3(worst) >= hurdle": g["worst"]["dt3"] >= HURDLE,
      ">=2 thirds > 0 (not single-third-confined)": pos_thirds >= 2,
      "both directions present":  both_sides,
    }
    print("\n"+"="*70); print("§6 GATE"); print("="*70)
    for k,vok in crit.items(): print(f"  [{'PASS' if vok else 'FAIL'}] {k}")
    verdict = "RESOLVED" if all(crit.values()) else "FALSIFIED"
    # ambiguous-hold nuance: best passes full gate but worst fails ONLY on path penalty
    best_full = (g["best"]["mean"]>=HURDLE and g["best"]["dt3"]>=HURDLE and p_perm<0.05 and pos_thirds>=2 and both_sides)
    worst_only_path = (not crit["worst mean >= hurdle"]) and best_full and (res["status"]=="ambiguous").any()
    if verdict=="FALSIFIED" and worst_only_path: verdict = "AMBIGUOUS-HOLD (best passes; worst fails on ambiguous-bar path penalty)"
    print(f"\n  >>> VERDICT: {verdict} <<<")

if __name__ == "__main__":
    main()
