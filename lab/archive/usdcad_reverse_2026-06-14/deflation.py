"""Loop-2 deflation on the pullback in-sample winner: plateau, entry-timing
permutation, cost sensitivity, long/short split. Characterizes the sub-cost edge
(is it real signal or selection noise?). Headline 4x-hurdle gate already FAILED."""
import numpy as np
import pandas as pd
import usdcad_harness as H

RES = "pullback_results.csv"


def sig_for(bars, row):
    swin = H.SESSIONS[row["session"]]
    ls, ss = H.build_signals(bars, "pullback", (int(row["fast"]), int(row["slow"])),
                             swin, bool(row["volfloor"]))
    ex = row["exit"]
    if ex.startswith("trail"):
        emode, eparam = "trail", float(ex.replace("trail", ""))
    else:
        emode, eparam = "tp", float(ex.replace("tp", ""))
    return ls, ss, emode, eparam, float(row["k"]), swin


def main():
    bars = H.load_and_prep()
    df = pd.read_csv(RES)
    elig = df[df["n"] >= 100].sort_values("exp", ascending=False)
    w = elig.iloc[0]
    ls, ss, emode, eparam, k, swin = sig_for(bars, w)
    r = H.simulate(bars, ls, ss, k, emode, eparam)
    m = H.metrics(r)
    print(f"WINNER: fast{int(w['fast'])}/slow{int(w['slow'])} {w['session']} "
          f"vf={w['volfloor']} k{k} {w['exit']}")
    print(f"  exp={m['exp']:+.4f}R n={m['n']} pf={m['pf']:.3f} wr={m['wr']:.3f} "
          f"req_4x_hurdle={w['req_exp']:.3f}  -> {'PASS' if m['exp']>=w['req_exp'] else 'FAIL'} cost gate")

    # ---------- long/short split ----------
    rl = H.simulate(bars, ls, np.zeros(bars.n, bool), k, emode, eparam, side_mode="long")
    rs = H.simulate(bars, np.zeros(bars.n, bool), ss, k, emode, eparam, side_mode="short")
    print(f"\nlong-only:  n={len(rl):>3} exp={np.mean(rl) if len(rl) else float('nan'):+.4f}")
    print(f"short-only: n={len(rs):>3} exp={np.mean(rs) if len(rs) else float('nan'):+.4f}")
    print("  (both sides positive => edge is the pullback mechanism, not one-directional drift)")

    # ---------- plateau: one-knob neighbors ----------
    print("\n=== PLATEAU (one-knob +/-1 step; dome vs needle) ===")
    neigh = []
    # fast 20<->9
    for f2 in ({9, 20} - {int(w["fast"])}):
        neigh.append(dict(w, fast=f2))
    for s2 in [x for x in (50, 100, 200) if x != int(w["slow"]) and abs(
            (50, 100, 200).index(x) - (50, 100, 200).index(int(w["slow"]))) == 1]:
        neigh.append(dict(w, slow=s2))
    ks = [1.5, 2.0, 2.5, 3.0]
    for k2 in [x for x in ks if abs(ks.index(x) - ks.index(k)) == 1]:
        neigh.append(dict(w, k=k2))
    exits = ["tp1.5", "tp2.0", "tp3.0", "trail2.0", "trail3.0"]
    for e2 in [x for x in exits if abs(exits.index(x) - exits.index(w["exit"])) == 1]:
        neigh.append(dict(w, exit=e2))
    neigh.append(dict(w, volfloor=not bool(w["volfloor"])))
    sess_order = ["ny0811", "ny0812", "ln0312", "allday"]
    for sv in [x for x in sess_order if abs(sess_order.index(x) - sess_order.index(w["session"])) == 1]:
        neigh.append(dict(w, session=sv))
    pos = 0
    print(f"  center exp={m['exp']:+.4f}")
    for nb in neigh:
        ls2, ss2, em2, ep2, k2, _ = sig_for(bars, nb)
        r2 = H.simulate(bars, ls2, ss2, k2, em2, ep2)
        m2 = H.metrics(r2)
        chg = next(kk for kk in ("fast", "slow", "k", "exit", "volfloor", "session")
                   if str(nb[kk]) != str(w[kk]))
        pos += m2["exp"] > 0
        print(f"  {chg}->{nb[chg]}: exp={m2['exp']:+.4f} n={m2['n']}")
    print(f"  neighbors positive: {pos}/{len(neigh)}  "
          f"(dome if most positive & center near max)")

    # ---------- entry-timing permutation ----------
    print("\n=== ENTRY-TIMING PERMUTATION (B=2000): does pullback timing beat random? ===")
    sess_ok = H._session_ok(bars, swin)
    vf = bars.volfloor_ok if bool(w["volfloor"]) else np.ones(bars.n, bool)
    es = bars.ema[int(w["slow"])]
    universe = np.where(sess_ok & vf & ~np.isnan(bars.atr) & ~np.isnan(es))[0]
    nL, nS = int(ls.sum()), int(ss.sum())
    rng = np.random.default_rng(20260614)
    obs = m["exp"]
    ge = 0
    B = 2000
    for _ in range(B):
        pick = rng.choice(universe, size=nL + nS, replace=False)
        pl = np.zeros(bars.n, bool); ps = np.zeros(bars.n, bool)
        pl[pick[:nL]] = True; ps[pick[nL:]] = True
        rp = H.simulate(bars, pl, ps, k, emode, eparam)
        if len(rp) and np.mean(rp) >= obs:
            ge += 1
    print(f"  P(random-entry exp >= {obs:+.4f}) = {ge/B:.4f}  (gate: <0.05 to be real signal)")

    # ---------- cost sensitivity ----------
    print("\n=== COST SENSITIVITY of winner ===")
    for rt in (0.8, 1.2, 1.6, 2.0):
        rr = H.simulate(bars, ls, ss, k, emode, eparam, rt_cost_pip=rt)
        print(f"  RT={rt}p: exp={np.mean(rr):+.4f}R  (breakeven at ~{np.mean(rr)>0})")


if __name__ == "__main__":
    main()
