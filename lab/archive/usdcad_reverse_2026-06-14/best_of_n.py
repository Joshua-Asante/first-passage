"""Selection-adjusted deflation for loop 2: is the best-of-960 pullback exp (+0.148R)
beyond what selection over 960 zero-edge trial distributions would produce?

Null = sign-flip each trade's R (removes edge, preserves magnitude/structure), recompute
every config's expectancy, take the MAX across configs; repeat. p = P(null max >= observed max).
"""
import numpy as np
import usdcad_harness as H


def collect_eligible_R(bars, rt_cost_pip=None):
    rt = H.RT_COST_PIP if rt_cost_pip is None else rt_cost_pip
    fams = [("pullback", (f, s)) for f in H.EMA_FAST for s in H.EMA_SLOW if f < s]
    arrs = []
    for family, param in fams:
        for _sname, swin in H.SESSIONS.items():
            for vf in H.VOLFLOOR:
                ls, ss = H.build_signals(bars, family, param, swin, vf)
                if ls.sum() + ss.sum() == 0:
                    continue
                for k in H.K_STOPS:
                    for emode, eparam in H.EXITS:
                        r = H.simulate(bars, ls, ss, k, emode, eparam, rt_cost_pip=rt)
                        if len(r) >= 100:
                            arrs.append(r)
    return arrs


def main():
    bars = H.load_and_prep()
    arrs = collect_eligible_R(bars)
    obs_max = max(a.mean() for a in arrs)
    print(f"eligible configs: {len(arrs)}  observed best exp = {obs_max:+.4f}R")

    rng = np.random.default_rng(20260614)
    B = 1000
    ge = 0
    null_maxes = np.empty(B)
    for b in range(B):
        mx = -1e9
        for a in arrs:
            signs = rng.integers(0, 2, size=len(a)) * 2 - 1
            mm = float(np.mean(a * signs))
            if mm > mx:
                mx = mm
        null_maxes[b] = mx
        if mx >= obs_max:
            ge += 1
    p = ge / B
    print(f"sign-flip best-of-N null (B={B}): "
          f"null max exp  mean={null_maxes.mean():+.4f}  p95={np.quantile(null_maxes,0.95):+.4f} "
          f"max={null_maxes.max():+.4f}")
    print(f"P(null best >= observed best {obs_max:+.4f}) = {p:.4f}  "
          f"(gate: <0.05 => best is beyond selection noise)")


if __name__ == "__main__":
    main()
