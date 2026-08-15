#!/usr/bin/env python3
# =============================================================================
# PHAROS — Outcome Simulator v0.1   (built to Q-ICT-SWEEPFVG-1 §7)
# -----------------------------------------------------------------------------
# Resolves each pre-registered sweep->FVG->draw setup to a per-trade R outcome
# and reports best/worst excursion-bounded expectancy plus the inline selection
# battery. Consumes the FROZEN population (setups.csv) + bars; re-derives no join.
#
# *** FIREWALL — READ ***
# This tool is built to spec and DELIBERATELY UN-RUN on the real population.
# Running it on setups.csv reveals outcomes the pre-registration (Q-ICT-SWEEPFVG-1)
# must be authored blind to. Two guards enforce this:
#   (1) BRIEF_LOCKED is False -> the real run aborts unless --i-have-locked-brief
#       is passed (you assert the §7 rules are frozen and you accept outcomes).
#   (2) Costs default to the PROVISIONAL §7.6 placeholder -> the real run aborts
#       unless real Pepperstone US500 costs are supplied (or --provisional given).
# Correctness is proven via `--selftest` (synthetic fixtures, hand-computed
# answers) which touches NO real data. Do that; do not run the real population
# until the brief is locked and the cost spec is in.
#
# EVERY constant below is a FROZEN §7 rule. Changing one post-outcome voids the
# checkpoint (§5 forbidden moves, §10 append-only audit question).
# =============================================================================

import argparse
import hashlib
import sys
import numpy as np
import pandas as pd

# ---- Frozen population identity (§10.1) -------------------------------------
FROZEN_POPULATION_MD5 = "b1e3ba85a2f77d2f83cef92d0e328a2e"   # setups.csv @ window=12

# ---- Frozen §7 rules --------------------------------------------------------
BRIEF_LOCKED        = False          # set True ONLY when Q-ICT-SWEEPFVG-1 is locked
FVG_WINDOW          = 12             # §7.1  (population was generated at this window)
FILL_WINDOW_BARS    = 8             # §7.2  bars after FVG formation to fill, else expire
STOP_BUFFER_ATR     = 0.10          # §7.3  stop = sweep_extreme -/+ 0.10 * ATR_at_sweep
SESSION_FILTER      = None          # §7.7  no session filter
HURDLE_MULT         = 4             # §2/§6 gate: expectancy vs 4x median cost_R
# §7.6 PROVISIONAL costs (index points) — replace with real Pepperstone US500 spec
PROVISIONAL_RT_SPREAD_PTS = 0.4
PROVISIONAL_SLIPPAGE_PTS  = 0.2


# -----------------------------------------------------------------------------
# Guards
# -----------------------------------------------------------------------------
def assert_population_identity(setups_path):
    h = hashlib.md5(open(setups_path, "rb").read()).hexdigest()
    if h != FROZEN_POPULATION_MD5:
        sys.exit(f"HALT (§10.1): setups.csv md5 {h} != frozen {FROZEN_POPULATION_MD5}. "
                 f"The sim must run on the EXACT pre-registered population.")


def assert_runnable(args):
    if not (BRIEF_LOCKED or args.i_have_locked_brief):
        sys.exit("HALT (firewall): brief not locked. Real-population run produces "
                 "outcomes the pre-reg must be blind to. Re-run with --selftest, or "
                 "pass --i-have-locked-brief once Q-ICT-SWEEPFVG-1 is locked.")
    if args.rt_spread is None and not args.provisional:
        sys.exit("HALT (§5.6/§7.6): no real cost spec. Supply --rt-spread/--slippage "
                 "(Pepperstone US500) or pass --provisional to use the flagged placeholder.")


# -----------------------------------------------------------------------------
# Load
# -----------------------------------------------------------------------------
def load_bars(path):
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df["time"] = df["time"].astype("int64")
    return df[["time", "open", "high", "low", "close"]].reset_index(drop=True)


def load_setups(path):
    s = pd.read_csv(path)
    return s[s["matched"] & s["target_present"]].reset_index(drop=True)  # §7.1 complete only


# -----------------------------------------------------------------------------
# Core resolution (§7.2 fill, §7.3 stop, §7.4 target, §7.5 path order, §7.6 cost)
# -----------------------------------------------------------------------------
def resolve_setup(bars, s, rt_spread, slippage):
    """Return dict with fill/outcome under both path orderings. Pure §7."""
    direction = s["direction"]
    fvg_bar   = int(s["fvg_bar"])
    atr       = float(s["atr_at_sweep"])
    n         = len(bars)
    high = bars["high"].values
    low  = bars["low"].values

    if direction == "long":
        entry = float(s["fvg_top"])                      # §7.2 proximal edge
        stop  = float(s["sweep_extreme"]) - STOP_BUFFER_ATR * atr   # §7.3
    else:
        entry = float(s["fvg_btm"])
        stop  = float(s["sweep_extreme"]) + STOP_BUFFER_ATR * atr
    target    = float(s["target_level"])                 # §7.4
    stop_dist = abs(entry - stop)
    rwin      = abs(target - entry) / stop_dist if stop_dist > 0 else np.nan
    cost_R    = (rt_spread + slippage) / stop_dist if stop_dist > 0 else np.nan

    base = dict(direction=direction, entry=entry, stop=stop, target=target,
                stop_dist=stop_dist, R_win=rwin, cost_R=cost_R,
                fill_bar=np.nan, status="", R_best=np.nan, R_worst=np.nan)

    # --- §7.2 fill: first bar AFTER formation reaching the proximal edge ----
    fill_bar = None
    for j in range(fvg_bar + 1, min(fvg_bar + 1 + FILL_WINDOW_BARS, n)):
        if direction == "long" and low[j] <= entry:
            fill_bar = j; break
        if direction == "short" and high[j] >= entry:
            fill_bar = j; break
    if fill_bar is None:
        base["status"] = "expired"
        return base
    base["fill_bar"] = fill_bar

    # --- §7.5 walk forward from fill; resolve vs stop/target ----------------
    for j in range(fill_bar, n):
        if direction == "long":
            hit_t = high[j] >= target
            hit_s = low[j] <= stop
        else:
            hit_t = low[j] <= target
            hit_s = high[j] >= stop
        if hit_t and hit_s:                              # ambiguous intrabar order
            base["status"] = "ambiguous"
            base["R_best"]  = rwin - cost_R              # target-first
            base["R_worst"] = -1.0 - cost_R              # stop-first
            return base
        if hit_t:
            base["status"] = "win"
            base["R_best"] = base["R_worst"] = rwin - cost_R
            return base
        if hit_s:
            base["status"] = "loss"
            base["R_best"] = base["R_worst"] = -1.0 - cost_R
            return base
    base["status"] = "censored"                          # open at end of data
    return base


def run_population(bars, setups, rt_spread, slippage):
    rows = [resolve_setup(bars, setups.iloc[i], rt_spread, slippage)
            for i in range(len(setups))]
    out = pd.DataFrame(rows)
    out["sweep_ts_et"] = pd.to_datetime(setups["sweep_ts_et"].values, utc=True)
    return out


# -----------------------------------------------------------------------------
# Inline selection battery (strategy-validation §5 a/d/e on the outcome vector)
# Heavier (b) best-of-K and full (c) label-permutation run via selection_tests.py
# -----------------------------------------------------------------------------
def expectancy(out, order):
    col = "R_best" if order == "best" else "R_worst"
    v = out.loc[out["status"].isin(["win", "loss", "ambiguous"]), col]
    return v.dropna()

def bootstrap_ci(v, hurdle, B=5000, seed=0):
    if len(v) == 0:
        return None
    rng = np.random.default_rng(seed)
    means = v.values[rng.integers(0, len(v), size=(B, len(v)))].mean(axis=1)
    return dict(mean=float(v.mean()), lo=float(np.percentile(means, 2.5)),
                hi=float(np.percentile(means, 97.5)),
                p_le0=float((means <= 0).mean()),
                p_ge_hurdle=float((means >= hurdle).mean()))

def drop_top_k(v, k=3):
    return float(np.sort(v.values)[:-k].mean()) if len(v) > k else np.nan

def thirds(out, order):
    col = "R_best" if order == "best" else "R_worst"
    sub = out[out["status"].isin(["win", "loss", "ambiguous"])].copy()
    if len(sub) < 3:
        return []
    sub = sub.sort_values("sweep_ts_et")
    return [float(g[col].mean()) for g in np.array_split(sub, 3)]

def direction_permutation(bars, setups, rt_spread, slippage, K=2000, seed=0):
    """Mirror-direction permutation (§6): does entering in the sweep's predicted
    direction beat a random predicted/mirrored choice? Mirrored geometry preserves
    R (stop/target reflected about entry). Worst-order convention for both, apples
    to apples. Also catches drift-only nulls."""
    obs, mir = [], []
    high = bars["high"].values; low = bars["low"].values; n = len(bars)
    for i in range(len(setups)):
        s = setups.iloc[i]
        r = resolve_setup(bars, s, rt_spread, slippage)
        if r["status"] not in ("win", "loss", "ambiguous"):
            continue
        obs.append(r["R_worst"])
        # mirror: same entry, reflect stop & target about entry, flip direction
        e, st, tg = r["entry"], r["stop"], r["target"]
        m_dir = "short" if s["direction"] == "long" else "long"
        m_stop, m_tgt = 2 * e - st, 2 * e - tg
        sd = abs(e - m_stop); rwin = abs(m_tgt - e) / sd; cR = (rt_spread + slippage) / sd
        fb = int(r["fill_bar"])
        status = "censored"; res = np.nan
        for j in range(fb, n):
            if m_dir == "long":
                ht, hs = high[j] >= m_tgt, low[j] <= m_stop
            else:
                ht, hs = low[j] <= m_tgt, high[j] >= m_stop
            if ht and hs: status, res = "amb", -1.0 - cR; break   # worst-order
            if ht: status, res = "win", rwin - cR; break
            if hs: status, res = "loss", -1.0 - cR; break
        mir.append(res if status != "censored" else np.nan)
    obs = np.array(obs); mir = np.array(mir, dtype=float)
    valid = ~np.isnan(mir)
    obs_mean = obs[valid].mean()
    rng = np.random.default_rng(seed)
    perm_means = np.empty(K)
    o, m = obs[valid], mir[valid]
    for k in range(K):
        pick = rng.random(len(o)) < 0.5
        perm_means[k] = np.where(pick, o, m).mean()
    return dict(obs_mean=float(obs_mean), mirror_mean=float(m.mean()),
                p_perm_ge_obs=float((perm_means >= obs_mean).mean()), n=int(valid.sum()))


# -----------------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------------
def report(out, bars, setups, rt_spread, slippage):
    n = len(out)
    counts = out["status"].value_counts().to_dict()
    cost_R_med = float(out["cost_R"].median())
    hurdle = HURDLE_MULT * cost_R_med
    print("=" * 70)
    print("OUTCOME SIM — Q-ICT-SWEEPFVG-1  (built to §7)")
    print("=" * 70)
    print(f"cost spec           : RT_spread={rt_spread} slippage={slippage} pts")
    print(f"median cost_R       : {cost_R_med:.4f}R   -> hurdle (x{HURDLE_MULT}) = {hurdle:.4f}R")
    print(f"population (complete): {n}   status: {counts}")
    for order in ("best", "worst"):
        v = expectancy(out, order)
        ci = bootstrap_ci(v, hurdle)
        wr = float((v > 0).mean()) if len(v) else float("nan")
        print(f"\n--- {order.upper()}-ORDER ---")
        if ci:
            print(f"  expectancy        : {ci['mean']:.3f}R  (95% CI {ci['lo']:.3f}..{ci['hi']:.3f})")
            print(f"  P(<=0) / P(>=hurdle): {ci['p_le0']:.3f} / {ci['p_ge_hurdle']:.3f}")
        print(f"  win rate          : {wr:.3f}   n_resolved={len(v)}")
        print(f"  drop-top-3        : {drop_top_k(v):.3f}R   (gate: stays >= {hurdle:.3f})")
        print(f"  thirds            : {['%.3f'%t for t in thirds(out, order)]}")
    perm = direction_permutation(bars, setups, rt_spread, slippage)
    print(f"\n--- DIRECTION PERMUTATION (worst-order, §6) ---")
    print(f"  obs vs mirror mean: {perm['obs_mean']:.3f} vs {perm['mirror_mean']:.3f}  (n={perm['n']})")
    print(f"  P(perm >= obs)    : {perm['p_perm_ge_obs']:.3f}   (gate: < 0.05)")
    print("\nNOTE: §6 verdict requires BOTH bounds >= hurdle AND perm P<0.05 AND "
          "drop-top-3 holds AND not single-third-confined AND both sides present.")
    print("Heavier (b) best-of-K / full (c) label-permutation -> selection_tests.py.")
    print("FORK (sim v0.2): FVG-alone control panel needs its own pre-registered "
          "geometry; not bundled here.")


# -----------------------------------------------------------------------------
# Selftest — synthetic fixtures with hand-computed answers (NO real data)
# -----------------------------------------------------------------------------
def _bars(rows):
    return pd.DataFrame(rows, columns=["time", "open", "high", "low", "close"])

def _setup(**kw):
    base = dict(direction="long", fvg_bar=2, atr_at_sweep=2.0, sweep_extreme=100.0,
                fvg_top=102.0, fvg_btm=101.0, target_level=110.0,
                matched=True, target_present=True, sweep_ts_et="2026-05-14T20:00:00+00:00")
    base.update(kw); return pd.Series(base)

def selftest():
    RT, SL = 0.0, 0.0   # zero cost for clean hand-checks
    fails = []
    def chk(name, got, exp, tol=1e-3):
        ok = (got is exp) if exp is None else (abs(got - exp) <= tol)
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got} exp {exp}")
        if not ok: fails.append(name)

    # entry=102, stop=100-0.2=99.8, target=110 -> R_win=(110-102)/2.2=3.6364
    RWIN = 8 / 2.2

    # F1 clean long WIN: fill bar3 (low 101.5<=102), bar4 high111>=110 first
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,103,103.5,102,102.5],
               [3,102.5,103,101.5,102.8],[4,102.8,111,104,110.5]])
    r = resolve_setup(b, _setup(), RT, SL)
    chk("F1 status", r["status"]=="win" and 1 or 0, 1); chk("F1 R", r["R_best"], RWIN)

    # F2 clean long LOSS: bar4 low 99(<=99.8) only
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,103,103.5,102,102.5],
               [3,102.5,103,101.5,102.8],[4,102.8,105,99,100]])
    r = resolve_setup(b, _setup(), RT, SL); chk("F2 R", r["R_worst"], -1.0)

    # F3 AMBIGUOUS: bar4 spans both 111 and 99
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,103,103.5,102,102.5],
               [3,102.5,103,101.5,102.8],[4,102.8,111,99,105]])
    r = resolve_setup(b, _setup(), RT, SL)
    chk("F3 best", r["R_best"], RWIN); chk("F3 worst", r["R_worst"], -1.0)

    # F4 EXPIRED: no bar after formation dips to 102 within fill window
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,103,103.5,102,103],
               [3,103,106,103.5,105],[4,105,108,104.5,107]])
    r = resolve_setup(b, _setup(), RT, SL); chk("F4 expired", r["status"]=="expired" and 1 or 0, 1)

    # F5 CENSORED: fills bar3, never reaches 110 or 99.8
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,103,103.5,102,102.5],
               [3,102.5,103,101.5,102.8],[4,102.8,104,101,103],[5,103,104,101.5,103]])
    r = resolve_setup(b, _setup(), RT, SL); chk("F5 censored", r["status"]=="censored" and 1 or 0, 1)

    # F6 SHORT WIN: entry=fvg_btm=98, stop=100+0.2=100.2, target=90 -> R_win=8/2.2
    s = _setup(direction="short", fvg_btm=98.0, fvg_top=99.0, target_level=90.0)
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,97,98,96.5,97.5],
               [3,97.5,98.5,97,98],[4,98,99,89,90.5]])  # bar3 high98.5>=98 fills; bar4 low89<=90 wins
    r = resolve_setup(b, s, RT, SL)
    chk("F6 status", r["status"]=="win" and 1 or 0, 1); chk("F6 R", r["R_best"], RWIN)

    # F7 COST applied: RT+SL=0.6 over stop_dist 2.2 -> cost_R=0.2727; net win=RWIN-0.2727
    b = _bars([[0,100,100,100,100],[1,100,100,100,100],[2,103,103.5,102,102.5],
               [3,102.5,103,101.5,102.8],[4,102.8,111,104,110.5]])
    r = resolve_setup(b, _setup(), 0.4, 0.2); chk("F7 net", r["R_best"], RWIN - 0.6/2.2)

    print("\nSELFTEST:", "ALL PASS" if not fails else f"FAILURES {fails}")
    return 0 if not fails else 1


# -----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bars"); ap.add_argument("--setups")
    ap.add_argument("--rt-spread", type=float, default=None)
    ap.add_argument("--slippage", type=float, default=None)
    ap.add_argument("--provisional", action="store_true")
    ap.add_argument("--i-have-locked-brief", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not (args.bars and args.setups):
        sys.exit("Need --bars and --setups for a real run (or use --selftest).")
    assert_runnable(args)
    assert_population_identity(args.setups)
    rt = args.rt_spread if args.rt_spread is not None else PROVISIONAL_RT_SPREAD_PTS
    sl = args.slippage if args.slippage is not None else PROVISIONAL_SLIPPAGE_PTS
    bars, setups = load_bars(args.bars), load_setups(args.setups)
    out = run_population(bars, setups, rt, sl)
    report(out, bars, setups, rt, sl)


if __name__ == "__main__":
    main()
