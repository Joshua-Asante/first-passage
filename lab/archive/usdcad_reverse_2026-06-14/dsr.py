"""Deflated Sharpe Ratio (Bailey & Lopez de Prado) for loop 2 — pre-registered gate 4.
Selection-adjusted significance of the best pullback config given N=916 trials.

Also runs a proper random-entry best-of-N null (preserves real stop/TP asymmetry, unlike
the sign-flip null) on a reduced budget as a cross-check.
"""
import numpy as np
from scipy.stats import norm, skew, kurtosis
import usdcad_harness as H

GAMMA = 0.5772156649


def collect(bars):
    fams = [("pullback", (f, s)) for f in H.EMA_FAST for s in H.EMA_SLOW if f < s]
    out = []
    for family, param in fams:
        for sname, swin in H.SESSIONS.items():
            for vf in H.VOLFLOOR:
                ls, ss = H.build_signals(bars, family, param, swin, vf)
                if ls.sum() + ss.sum() == 0:
                    continue
                for k in H.K_STOPS:
                    for emode, eparam in H.EXITS:
                        r = H.simulate(bars, ls, ss, k, emode, eparam)
                        if len(r) >= 100:
                            out.append(dict(r=r, sname=sname, swin=swin, vf=vf,
                                            param=param, k=k, emode=emode, eparam=eparam,
                                            exp=r.mean(), sr=r.mean() / r.std(ddof=1)))
    return out


def dsr(configs):
    srs = np.array([c["sr"] for c in configs])
    N = len(srs)
    var_sr = np.var(srs, ddof=1)
    e_max = np.sqrt(var_sr) * ((1 - GAMMA) * norm.ppf(1 - 1.0 / N)
                               + GAMMA * norm.ppf(1 - 1.0 / (N * np.e)))
    best = max(configs, key=lambda c: c["sr"])
    r = best["r"]; T = len(r); sr = best["sr"]
    sk = skew(r); ku = kurtosis(r, fisher=False)
    denom = np.sqrt(1 - sk * sr + (ku - 1) / 4.0 * sr ** 2)
    dsr_stat = norm.cdf((sr - e_max) * np.sqrt(T - 1) / denom)
    return dict(N=N, var_sr=var_sr, e_max_sr=e_max, best_sr=sr, best_exp=best["exp"],
                best_cfg=f"{best['param']} {best['sname']} k{best['k']} {best['emode']}{best['eparam']}",
                dsr=dsr_stat, T=T)


def random_entry_best_of_n(bars, configs, B=100, seed=20260614):
    """Proper selection null: random entries per config (real bars+stop/TP), best over all."""
    rng = np.random.default_rng(seed)
    # precompute per-config universe + counts
    specs = []
    for c in configs:
        sess = H._session_ok(bars, c["swin"])
        vf = bars.volfloor_ok if c["vf"] else np.ones(bars.n, bool)
        es = bars.ema[c["param"][1]]
        uni = np.where(sess & vf & ~np.isnan(bars.atr) & ~np.isnan(es))[0]
        specs.append((c, uni))
    # need real long/short counts -> rebuild signals once
    obs_max = max(c["exp"] for c in configs)
    ge = 0
    null_max = np.empty(B)
    for b in range(B):
        mx = -9
        for c, uni in specs:
            ls, ss = H.build_signals(bars, "pullback", c["param"], c["swin"], c["vf"])
            nL, nS = int(ls.sum()), int(ss.sum())
            if nL + nS == 0 or len(uni) < nL + nS:
                continue
            pick = rng.choice(uni, size=nL + nS, replace=False)
            pl = np.zeros(bars.n, bool); ps = np.zeros(bars.n, bool)
            pl[pick[:nL]] = True; ps[pick[nL:]] = True
            r = H.simulate(bars, pl, ps, c["k"], c["emode"], c["eparam"])
            if len(r) >= 100:
                mx = max(mx, r.mean())
        null_max[b] = mx
        if mx >= obs_max:
            ge += 1
    return obs_max, null_max, ge / B


def main():
    bars = H.load_and_prep()
    configs = collect(bars)
    d = dsr(configs)
    print("=== DSR (pre-registered gate 4) ===")
    print(f"  N trials={d['N']}  Var(trial SR)={d['var_sr']:.5f}")
    print(f"  E[max SR | null] = {d['e_max_sr']:.4f}   best SR (per-trade) = {d['best_sr']:.4f}")
    print(f"  best-SR config: {d['best_cfg']}  exp={d['best_exp']:+.4f}R  n={d['T']}")
    print(f"  DSR = {d['dsr']:.4f}   (gate: >0.95 => significant after multiplicity)")
    print(f"  -> {'PASS' if d['dsr'] > 0.95 else 'FAIL'} selection gate")

    print("\n=== random-entry best-of-N null (B=60, proper asymmetry-preserving) ===")
    obs, nm, p = random_entry_best_of_n(bars, configs, B=60)
    print(f"  observed best exp={obs:+.4f}  null best-of-N: mean={nm.mean():+.4f} "
          f"p95={np.quantile(nm,0.95):+.4f} max={nm.max():+.4f}")
    print(f"  P(null best >= observed) = {p:.4f}  (gate: <0.05 => beyond selection noise)")


if __name__ == "__main__":
    main()
