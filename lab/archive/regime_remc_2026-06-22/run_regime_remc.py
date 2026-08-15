"""Regime-conditional decompounded re-MC — driver (Q-REGIME-ADAPT-1.T2b, 2026-06-22).

Per the COMMITTED pre-registration
(`docs/briefs/pre-registration/Q-REGIME-ADAPT-1-T2b-verdict-preregistration.md`).
Reuses the LOCKED decompound + MC primitives ZERO-FORK (build_daily_panel /
build_week_blocks / _run_seeds, dd_protection C2 via trig/scale). The ONLY new
mechanism is the exogenous VIX brake (`regime_brake.py`, synthetic-tested).

Baseline (no brake) vs +brake on the SAME panel, half-panel H1/H2 per the
regime-gate convention (split at the bday midpoint). Leakage audit (signal lag
+1 extra day). Robustness ladder reported in full; verdict rests on PRIMARY.

Needs the 6 decompound inputs in ../decompound_remc_2026-06-07/inputs/ and VIX
(yfinance ^VIX, cached). Skips cleanly if either is absent.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

_HERE = Path(__file__).resolve().parent
_DECOMP = _HERE.parents[1] / "analysis" / "decompound_remc_2026-06-07"
sys.path.insert(0, str(_DECOMP))
sys.path.insert(0, str(_HERE))

import regime_brake as RB  # noqa: E402

# ── pre-registered config (do not edit post-hoc — see pre-registration) ──
TRIG, SCALE = 0.015, 0.40          # locked dd_protection C2 (unchanged)
THRESH, K, LAG = 20.0, 0.50, 1     # PRIMARY: VIX>20, k=0.50, lag-honest
FLOOR_P99, FLOOR_BUST, MEDIAN_BOUND = 0.05, 0.01, 45
ROBUSTNESS = [(25.0, 0.50), (30.0, 0.50), (20.0, 0.40), (20.0, 0.60)]
VIX_CACHE = _HERE / "vix_close.csv"   # gitignored


def load_vix(start, end):
    if VIX_CACHE.exists():
        s = pd.read_csv(VIX_CACHE, index_col=0, parse_dates=True).iloc[:, 0].astype(float)
        return s
    try:
        import yfinance as yf
    except ImportError:
        return None
    df = yf.download("^VIX", start=str(pd.Timestamp(start).date()),
                     end=str((pd.Timestamp(end) + pd.Timedelta(days=3)).date()),
                     progress=False, auto_adjust=False)
    if df is None or len(df) == 0:
        return None
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    idx = pd.DatetimeIndex(close.index)
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    close.index = idx.normalize()
    close = close.astype(float).rename("VIX")
    close.to_csv(VIX_CACHE)
    return close


def main() -> int:
    import decompound as D
    from decompound import build_daily_panel, build_week_blocks, _run_seeds, SIMS_PER_SEED
    try:
        import joblib  # noqa: F401
        parallel = True
    except ImportError:
        parallel = False

    LOCKED = dict(D.ALLOC)
    NATIVE_1R = {s: LOCKED[s] * D.ACCOUNT for s in LOCKED}

    try:
        static = {s: D.rebank(D.stitch(s), "static") for s in LOCKED}
    except Exception as e:
        print(f"=== SKIP: decompound inputs absent ({e}). Drop the 6 documented exports into "
              f"{_DECOMP / 'inputs'} and re-run. ===")
        return 0

    panel, _ = build_daily_panel(static, LOCKED, fixed_1r_reference=NATIVE_1R)
    strats = tuple(static.keys())
    panel = panel.copy()
    panel.index = pd.DatetimeIndex(panel.index).normalize()

    vix = load_vix(panel.index.min(), panel.index.max())
    if vix is None or len(vix) == 0:
        print("=== SKIP: VIX unavailable (yfinance/network). Cache vix_close.csv or restore egress. ===")
        return 0

    def summarize(sr):
        per = SIMS_PER_SEED
        pr = float(np.mean([r["outcomes"]["pass"] / per for r in sr]))
        br = float(np.mean([(r["outcomes"]["bust_daily"] + r["outcomes"]["bust_static"]) / per for r in sr]))
        dds = [d for r in sr for d in r["max_dds"]]
        days = [d for r in sr for d in r["days_to_pass"]]
        return pr, br, float(np.percentile(dds, 99)), (int(np.median(days)) if days else 9999)

    def run(p):
        return summarize(_run_seeds(build_week_blocks(p), TRIG, SCALE, parallel=parallel, strats=strats))

    mid = panel.index[len(panel) // 2]

    def split(p):
        return p.loc[p.index < mid], p.loc[p.index >= mid]

    def brake(thresh, k, lag):
        fac = RB.align_factor_to_panel(
            RB.regime_factor_series(vix, threshold=thresh, k_derisk=k, lag_days=lag), panel.index)
        return RB.apply_regime_brake(panel, fac), float((fac < 1.0).mean())

    print(f"Panel {panel.index.min().date()}→{panel.index.max().date()} ({len(panel)} bd), "
          f"split @ {mid.date()} | VIX {vix.index.min().date()}→{vix.index.max().date()} "
          f"({len(vix)} obs) | parallel={parallel}", flush=True)

    # Baseline (no brake)
    b_full, b_h1, b_h2 = run(panel), None, None
    h1, h2 = split(panel)
    b_h1, b_h2 = run(h1), run(h2)
    print(f"BASELINE  full {b_full}  H1 {b_h1}  H2 {b_h2}", flush=True)

    # Primary brake
    braked, sfrac = brake(THRESH, K, LAG)
    p_full = run(braked)
    ph1, ph2 = split(braked)
    p_h1, p_h2 = run(ph1), run(ph2)
    print(f"PRIMARY (VIX>{THRESH:.0f}, k={K}, lag={LAG}; stressed {sfrac:.1%} of days)  "
          f"full {p_full}  H1 {p_h1}  H2 {p_h2}", flush=True)

    # Leakage audit (lag +1 extra)
    braked2, _ = brake(THRESH, K, LAG + 1)
    l_h1 = run(split(braked2)[0])
    print(f"LEAKAGE (lag={LAG+1})  H1 {l_h1}", flush=True)

    # Robustness ladder (H1 only; reported in full)
    rob = []
    for thr, k in ROBUSTNESS:
        bk, sf = brake(thr, k, LAG)
        rh1 = run(split(bk)[0])
        rob.append((thr, k, sf, rh1))
        print(f"ROBUST (VIX>{thr:.0f}, k={k}; {sf:.1%})  H1 {rh1}", flush=True)

    # ── verdict (PRIMARY) ──
    def clears(r):
        return r[1] < FLOOR_BUST and r[2] < FLOOR_P99
    h1_clears = clears(p_h1)
    h2_maintained = clears(p_h2)
    median_ok = p_h1[3] <= MEDIAN_BOUND
    leak_robust = clears(l_h1)
    if h1_clears and median_ok and h2_maintained and leak_robust:
        verdict = "RESOLVED-T2b"
    elif h1_clears and h2_maintained and leak_robust and MEDIAN_BOUND < p_h1[3] <= 90:
        verdict = "AMBIGUOUS-HOLD"
    else:
        verdict = "FALSIFIED-T2b"

    md = render(verdict, b_full, b_h1, b_h2, p_full, p_h1, p_h2, l_h1, rob, sfrac, mid, panel, vix)
    (_HERE / "RESULTS.md").write_text(md, encoding="utf-8")
    print("\n" + md)
    print(f"\nWrote {_HERE / 'RESULTS.md'}")
    return 0


def _fmt(r):
    return f"pass {r[0]:.2%} / bust {r[1]:.2%} / p99 {r[2]:.2%} / med {r[3]}"


def render(verdict, b_full, b_h1, b_h2, p_full, p_h1, p_h2, l_h1, rob, sfrac, mid, panel, vix):
    L = ["# Regime-conditional re-MC — RESULTS (Q-REGIME-ADAPT-1.T2b, 2026-06-22)\n"]
    L.append(f"**Verdict: {verdict}** — primary VIX>20 / k=0.50 / lag-1 brake, "
             f"stressed {sfrac:.1%} of days. Pre-registered (commit predates this run).\n")
    L.append(f"**Panel:** decompounded 2026-06-07 canonical, {panel.index.min().date()}→{panel.index.max().date()} "
             f"({len(panel)} bd), H1/H2 split @ {mid.date()}. VIX `^VIX` {vix.index.min().date()}→{vix.index.max().date()}. "
             "Locked allocations + dd_protection C2 unchanged; only the exogenous brake added.\n")
    L.append("\n| config | full | H1 (2020-2023) | H2 (2023-2026) |")
    L.append("|---|---|---|---|")
    L.append(f"| **baseline (no brake)** | {_fmt(b_full)} | {_fmt(b_h1)} | {_fmt(b_h2)} |")
    L.append(f"| **+brake VIX>20 k=0.50** | {_fmt(p_full)} | {_fmt(p_h1)} | {_fmt(p_h2)} |")
    L.append(f"\n**Gate (headline, H1 inside floor):** H1 bust<1% AND H1 p99<5% AND median≤45d AND H2 maintained AND leakage-clean.")
    L.append(f"- H1 +brake: bust {p_h1[1]:.2%} (<1%? {'Y' if p_h1[1]<0.01 else 'N'}), "
             f"p99 {p_h1[2]:.2%} (<5%? {'Y' if p_h1[2]<0.05 else 'N'}), median {p_h1[3]}d (≤45? {'Y' if p_h1[3]<=45 else 'N'})")
    L.append(f"- H2 +brake maintained: bust {p_h2[1]:.2%} / p99 {p_h2[2]:.2%} ({'Y' if p_h2[1]<0.01 and p_h2[2]<0.05 else 'N'})")
    L.append(f"- Leakage (lag-2) H1: {_fmt(l_h1)} → {'robust' if l_h1[1]<0.01 and l_h1[2]<0.05 else 'fragile'}")
    L.append("\n## Robustness ladder (H1; reported in full — verdict rests on PRIMARY only)\n")
    L.append("| signal | stressed% | H1 |")
    L.append("|---|---|---|")
    for thr, k, sf, rh1 in rob:
        L.append(f"| VIX>{thr:.0f}, k={k} | {sf:.1%} | {_fmt(rh1)} |")
    L.append("\n## Read\n")
    base_h1_bust, base_h1_p99 = b_h1[1], b_h1[2]
    L.append(f"- Baseline H1 (the regime-bound tail): bust {base_h1_bust:.2%}, p99 {base_h1_p99:.2%} — "
             f"the breach the brake must fix without an impractical pass-time.")
    if verdict == "RESOLVED-T2b":
        L.append("- The exogenous VIX brake **clears H1 at a practical pass-time** and is leakage-robust → "
                 "promote to a separate, lock-decision re-MC + ADR (the actual sizing change). HOLD lifts only there.")
    elif verdict == "AMBIGUOUS-HOLD":
        L.append("- The brake clears H1 but at median 45–90d (useful but costly) → AMBIGUOUS-HOLD; re-test vs risk appetite.")
    else:
        L.append("- The brake does **not** clear H1 at median ≤45d (or fails leakage/H2) → **FALSIFIED**: "
                 "the exogenous-VIX conditional lever does not beat the static de-risk tradeoff on this panel. "
                 "2026-06-07 HOLD stands. (Likely mechanism if FALSIFIED: VIX flags CRISIS but H1 busts include "
                 "low-VIX chop, OR the de-risk slows pass-time past 45d — the chop-vs-crisis gap T2a flagged.)")
    L.append("\n**Scope:** research (`lab/`); zero `core/` touch; no lock/allocation/dd_protection change. "
             "Vendor inputs + VIX cache gitignored. Reproduce: `python run_regime_remc.py` (inputs + yfinance).\n")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
