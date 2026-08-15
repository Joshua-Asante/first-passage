"""USDCAD up-spike-fade validation — frozen per PREREG-USDCAD-FADE-2026-06-26.

Reuses the triple-audited 2026-06-14 harness UNMODIFIED. Short-only up-fade =
Donchian up-breakout as long_sig, empty short_sig, side_mode="reversion"
(simulate then shorts the up-breakout: stop above, target below).

Gates (frozen §6): (1) cost-hurdle 4x, (2) DSR>0.95 over N=8, (3) regime/OOS
walk-forward, (4) best-of-N null [confirmatory], (5) asymmetry up>down,
(6) stationarity [confirmatory].

Run:  PYTHONIOENCODING=utf-8 python run_fade.py [best_of_n_B]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HARNESS_DIR = Path(__file__).resolve().parents[1] / "usdcad_reverse_2026-06-14"
sys.path.insert(0, str(HARNESS_DIR))
import usdcad_harness as H          # noqa: E402
from dsr import dsr as dsr_stat     # noqa: E402  (general: consumes our config dicts)

USER_CSV = Path(
    r"C:\Users\joshu\Downloads\BAR_EXPORT_v0.1_PEPPERSTONE_USDCAD_2026-06-26_422ca.csv"
)
SPLIT = pd.Timestamp("2023-06-11", tz=H.ET)   # H1/H2 temporal midpoint (frozen)
N_LOOKBACK = (24, 48)
K_STOPS = (2.5, 3.0)
TP = (1.0, 1.5)
NY = H.SESSIONS["ny0811"]
RT = H.RT_COST_PIP                            # 0.8 pip central


def et_index(path: Path) -> pd.DatetimeIndex:
    """Aligned (epoch-sorted) ET timestamp per bar — matches load_and_prep order."""
    raw = pd.read_csv(path, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    e = raw[raw["Type"].astype(str).str.startswith("Entry")]
    eps = [int(H.SIGNAL_PIPE_RE.match(s.strip()).group("e"))
           for s in e["Signal"].astype(str) if H.SIGNAL_PIPE_RE.match(s.strip())]
    eps = np.sort(np.array(eps))
    return pd.to_datetime(eps, unit="ms", utc=True).tz_convert(H.ET)


def sim_fade(bars, N, k, tp, session=NY, volfloor=True, mask=None, side="up"):
    """side: up=fade up-breakout(short) | down=fade down-breakout(long,control) | both."""
    ls, ss = H.build_signals(bars, "donchian", N, session, volfloor)
    zero = np.zeros(bars.n, bool)
    if side == "up":
        L, S = ls, zero
    elif side == "down":
        L, S = zero, ss
    else:
        L, S = ls, ss
    if mask is not None:
        L, S = L & mask, S & mask
    return H.simulate(bars, L, S, k, "tp", tp, rt_cost_pip=RT, side_mode="reversion")


def fmt(m, extra=""):
    return (f"n={m['n']:>5}  exp={m['exp']:+.4f}R  pf={m['pf']:.3f}  wr={m['wr']:.3f}  "
            f"netR={m['profitR']:+8.1f}  maxddR={m['maxddR']:6.1f} {extra}")


def fade_random_best_of_n(bars, configs, B, seed=20260626):
    """Asymmetry-preserving random-entry null: random SHORT entries (real bars/stop/TP),
    matched count per config, best expectancy over configs, repeated B times."""
    rng = np.random.default_rng(seed)
    sess = H._session_ok(bars, NY)
    vf = bars.volfloor_ok
    specs = []
    for c in configs:
        dh = bars.don_high[c["N"]]
        uni = np.where(sess & vf & ~np.isnan(bars.atr) & ~np.isnan(dh))[0]
        ls, _ = H.build_signals(bars, "donchian", c["N"], NY, True)
        specs.append((c, uni, int(ls.sum())))
    obs_max = max(c["exp"] for c in configs)
    null_max = np.empty(B)
    ge = 0
    for b in range(B):
        mx = -9.0
        for c, uni, nsig in specs:
            if nsig == 0 or len(uni) < nsig:
                continue
            pick = rng.choice(uni, size=nsig, replace=False)
            pl = np.zeros(bars.n, bool)
            pl[pick] = True
            r = H.simulate(bars, pl, np.zeros(bars.n, bool), c["k"], "tp", c["tp"],
                           rt_cost_pip=RT, side_mode="reversion")
            if len(r) >= 100:
                mx = max(mx, float(r.mean()))
        null_max[b] = mx
        ge += (mx >= obs_max)
    return obs_max, null_max, ge / B


def main():
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    t0 = time.time()
    bars = H.load_and_prep(USER_CSV)
    tet = et_index(USER_CSV)
    assert len(tet) == bars.n, f"align mismatch {len(tet)} vs {bars.n}"
    year = np.asarray(tet.year)
    is_H1 = np.asarray(tet < SPLIT)
    is_H2 = ~is_H1
    med_atr = float(np.nanmedian(bars.atr))
    print(f"bars={bars.n}  median ATR(14)={med_atr/H.PIP:.2f}p  "
          f"H1={int(is_H1.sum())} bars (<{SPLIT.date()})  H2={int(is_H2.sum())} bars  "
          f"({time.time()-t0:.1f}s)\n")

    def hurdle(k):
        return RT * H.PIP / (k * med_atr)

    # ---- frozen primary grid: short-only up-fade -------------------------
    print("=== PRIMARY GRID (short-only up-spike fade, NY 08-11, volfloor ON) ===")
    configs = []
    for N in N_LOOKBACK:
        for k in K_STOPS:
            for tp in TP:
                r = sim_fade(bars, N, k, tp, side="up")
                m = H.metrics(r)
                sr = float(r.mean() / r.std(ddof=1)) if len(r) > 1 and r.std() > 0 else 0.0
                h = hurdle(k)
                c = dict(N=N, k=k, tp=tp, r=r, sr=sr, hurdle=h, req=4 * h,
                         pass_hurdle=bool(m["exp"] >= 4 * h), **m,
                         param=N, sname="ny0811", emode="tp", eparam=tp)
                configs.append(c)
                print(f"  N{N:>2} k{k} tp{tp}: {fmt(m)}  "
                      f"hurdle={h:.4f} req4x={4*h:.4f} {'PASS' if c['pass_hurdle'] else 'fail'}")

    elig = [c for c in configs if c["n"] >= 100]
    if not elig:
        print("\nNO config clears n>=100 floor -> NULL (insufficient trades).")
        return
    best = max(elig, key=lambda c: c["exp"])
    print(f"\nselected (best full-panel exp, n>=100): "
          f"N{best['N']} k{best['k']} tp{best['tp']}  exp={best['exp']:+.4f}R n={best['n']}")

    # ---- gate 1: cost hurdle ---------------------------------------------
    g1 = best["pass_hurdle"] and best["exp"] > 0
    print(f"\n[GATE 1 cost-hurdle] exp {best['exp']:+.4f}R vs 4x hurdle {best['req']:.4f}R "
          f"-> {'PASS' if g1 else 'FAIL'}")

    # ---- gate 2: DSR over N=8 --------------------------------------------
    d = dsr_stat(configs)
    g2 = d["dsr"] > 0.95
    print(f"[GATE 2 DSR] N={d['N']} E[maxSR|null]={d['e_max_sr']:.4f} bestSR={d['best_sr']:.4f} "
          f"DSR={d['dsr']:.4f} -> {'PASS' if g2 else 'FAIL'}")

    # ---- gate 3: regime / OOS walk-forward -------------------------------
    print("\n=== GATE 3: regime robustness + walk-forward OOS ===")
    rH1 = H.metrics(sim_fade(bars, best["N"], best["k"], best["tp"], side="up", mask=is_H1))
    rH2 = H.metrics(sim_fade(bars, best["N"], best["k"], best["tp"], side="up", mask=is_H2))
    print(f"  pooled-winner  H1(2020-23): {fmt(rH1)}")
    print(f"  pooled-winner  H2(2023-26): {fmt(rH2)}")
    both_sign = (rH1["exp"] > 0) and (rH2["exp"] > 0)

    def select_on(mask):
        cc = []
        for N in N_LOOKBACK:
            for k in K_STOPS:
                for tp in TP:
                    m = H.metrics(sim_fade(bars, N, k, tp, side="up", mask=mask))
                    if m["n"] >= 50:
                        cc.append((m["exp"], N, k, tp))
        return max(cc) if cc else None

    wf_ok = True
    for tag, sel_mask, oos_mask, oos_name in [("H1->H2", is_H1, is_H2, "H2"),
                                              ("H2->H1", is_H2, is_H1, "H1")]:
        sel = select_on(sel_mask)
        if sel is None:
            wf_ok = False
            print(f"  {tag}: no in-sample config -> FAIL")
            continue
        _, N, k, tp = sel
        m = H.metrics(sim_fade(bars, N, k, tp, side="up", mask=oos_mask))
        ok = (m["exp"] > 0) and (m["exp"] >= 4 * hurdle(k))
        wf_ok = wf_ok and ok
        print(f"  {tag}: pick N{N} k{k} tp{tp} on IS -> OOS {oos_name}: {fmt(m)} "
              f"4xhurdle={4*hurdle(k):.4f} -> {'PASS' if ok else 'FAIL'}")
    g3 = both_sign and wf_ok
    print(f"  [GATE 3] both-halves same sign={both_sign}  walk-forward={wf_ok} "
          f"-> {'PASS' if g3 else 'FAIL'}")

    # ---- per-year table (selected config) --------------------------------
    print("\n  per-year (selected config):")
    for y in sorted(set(year)):
        m = H.metrics(sim_fade(bars, best["N"], best["k"], best["tp"], side="up", mask=(year == y)))
        print(f"    {y}: {fmt(m)}")

    # ---- gate 5: asymmetry (up vs down control) --------------------------
    print("\n=== GATE 5: directional asymmetry (up-fade vs down-fade control) ===")
    rdown = H.metrics(sim_fade(bars, best["N"], best["k"], best["tp"], side="down"))
    rboth = H.metrics(sim_fade(bars, best["N"], best["k"], best["tp"], side="both"))
    rall = H.metrics(sim_fade(bars, best["N"], best["k"], best["tp"], side="up", session=None))
    print(f"  up-fade (selected) : {fmt(best)}")
    print(f"  down-fade control  : {fmt(rdown)}")
    print(f"  symmetric control  : {fmt(rboth)}")
    print(f"  all-day up-fade    : {fmt(rall)}")
    g5 = best["exp"] > rdown["exp"]
    print(f"  [GATE 5] up {best['exp']:+.4f} > down {rdown['exp']:+.4f} -> {'PASS' if g5 else 'FAIL'}")

    # ---- gate 6: stationarity / concentration ----------------------------
    print("\n=== GATE 6: stationarity (thirds) + drop-top-k ===")
    rr = best["r"]
    thirds = np.array_split(rr, 3)
    tsigns = [float(t.mean()) for t in thirds]
    print(f"  thirds exp: {[f'{x:+.4f}' for x in tsigns]}")
    same_third = all(x > 0 for x in tsigns)
    srt = np.sort(rr)[::-1]
    dexp = {kk: float(srt[kk:].mean()) for kk in (1, 3, 5)}
    print(f"  drop-top-k exp: " + "  ".join(f"k{kk}={dexp[kk]:+.4f}" for kk in (1, 3, 5)))
    g6 = same_third and all(v > 0 for v in dexp.values())
    print(f"  [GATE 6] thirds same-sign={same_third} drop-top-k all+={all(v>0 for v in dexp.values())} "
          f"-> {'PASS' if g6 else 'FAIL'}")

    # ---- gate 4: best-of-N null (confirmatory, expensive) ----------------
    print(f"\n=== GATE 4: random-entry best-of-N null (asymmetry-preserving, B={B}) ===")
    t1 = time.time()
    obs, nm, p = fade_random_best_of_n(bars, configs, B=B)
    print(f"  observed best exp={obs:+.4f}  null best-of-N: mean={nm.mean():+.4f} "
          f"p95={np.quantile(nm,0.95):+.4f} max={nm.max():+.4f}  ({time.time()-t1:.1f}s)")
    g4 = p < 0.05
    print(f"  P(null best >= observed) = {p:.4f}  -> {'PASS(<0.05)' if g4 else ('weak' if p<0.5 else 'FAIL')}")

    # ---- cost sensitivity -----------------------------------------------
    print("\n=== cost sensitivity (selected config) ===")
    ls_sel, _ = H.build_signals(bars, "donchian", best["N"], NY, True)
    zero = np.zeros(bars.n, bool)
    for rtp in (0.8, 1.2, 1.6):
        mm = H.metrics(H.simulate(bars, ls_sel, zero, best["k"], "tp", best["tp"],
                                  rt_cost_pip=rtp, side_mode="reversion"))
        h_rtp = rtp * H.PIP / (best["k"] * med_atr)
        print(f"  RT {rtp} pip: exp={mm['exp']:+.4f}R  4x-hurdle={4*h_rtp:.4f}R  "
              f"{'clears' if mm['exp'] >= 4 * h_rtp else 'sub-hurdle'}")

    # ---- VERDICT ---------------------------------------------------------
    primary = {"G1 cost-hurdle": g1, "G2 DSR>0.95": g2, "G3 regime/OOS": g3, "G5 asymmetry": g5}
    confirm = {"G4 best-of-N": g4, "G6 stationarity": g6}
    print("\n" + "=" * 60)
    print("PRIMARY GATES:", {k: ("PASS" if v else "FAIL") for k, v in primary.items()})
    print("CONFIRMATORY :", {k: ("PASS" if v else "FAIL") for k, v in confirm.items()})
    overall = all(primary.values())
    print(f"\nOVERALL: {'PASS — validated candidate' if overall else 'NULL — gates not cleared'}")
    print(f"(total {time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
