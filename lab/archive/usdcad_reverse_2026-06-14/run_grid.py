"""Run the pre-registered 960-config grid (+ all-day control + reversion control)."""
import time
from pathlib import Path

import numpy as np
import pandas as pd

import usdcad_harness as H

OUT = Path(__file__).parent / "grid_results.csv"


def run_grid(bars, side_mode="both", rt_cost_pip=None):
    rt = H.RT_COST_PIP if rt_cost_pip is None else rt_cost_pip
    med_atr = np.nanmedian(bars.atr)
    rows = []
    families = [("donchian", N) for N in H.DON_N] + [("orb", M) for M in H.ORB_M]
    for family, param in families:
        for sname, swin in H.SESSIONS.items():
            for vf in H.VOLFLOOR:
                ls, ss = H.build_signals(bars, family, param, swin, vf)
                if ls.sum() + ss.sum() == 0:
                    continue
                for k in H.K_STOPS:
                    for emode, eparam in H.EXITS:
                        r = H.simulate(bars, ls, ss, k, emode, eparam,
                                       rt_cost_pip=rt, side_mode=side_mode)
                        m = H.metrics(r)
                        hurdle = rt * H.PIP / (k * med_atr)
                        m.update(family=family, param=param, session=sname,
                                 volfloor=vf, k=k, exit=f"{emode}{eparam}",
                                 hurdle_R=hurdle, req_exp=4 * hurdle,
                                 pass_hurdle=(m["exp"] >= 4 * hurdle) if m["n"] else False)
                        rows.append(m)
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    bars = H.load_and_prep()
    print(f"bars loaded: n={bars.n}  ({time.time()-t0:.1f}s)")
    t1 = time.time()
    df = run_grid(bars, side_mode="both")
    print(f"grid: {len(df)} configs  ({time.time()-t1:.1f}s)")
    df.to_csv(OUT, index=False)

    elig = df[(df["n"] >= 100)].copy().sort_values("exp", ascending=False)
    print(f"\n=== configs with n>=100: {len(elig)} / {len(df)} ===")
    cols = ["family", "param", "session", "volfloor", "k", "exit",
            "n", "exp", "pf", "wr", "profitR", "maxddR", "req_exp", "pass_hurdle"]
    pd.set_option("display.width", 200, "display.max_columns", 30)
    print("\nTOP 20 by net expectancy (R):")
    print(elig[cols].head(20).to_string(index=False,
          formatters={"exp": "{:+.4f}".format, "pf": "{:.3f}".format,
                      "wr": "{:.3f}".format, "profitR": "{:+.1f}".format,
                      "maxddR": "{:.1f}".format, "req_exp": "{:.3f}".format}))

    print(f"\nexpectancy distribution (n>=100): "
          f"mean={elig['exp'].mean():+.4f} median={elig['exp'].median():+.4f} "
          f"max={elig['exp'].max():+.4f} min={elig['exp'].min():+.4f} "
          f"frac>0={np.mean(elig['exp']>0):.2f} frac_pass_hurdle={np.mean(elig['pass_hurdle']):.3f}")

    # session effect: NY-morning vs all-day control
    print("\n=== session control (mean exp by session, n>=100) ===")
    print(elig.groupby("session")["exp"].agg(["count", "mean", "max"]).round(4).to_string())

    # family effect
    print("\n=== family (mean exp, n>=100) ===")
    print(elig.groupby("family")["exp"].agg(["count", "mean", "max"]).round(4).to_string())

    # reversion negative control (best-of)
    t2 = time.time()
    rev = run_grid(bars, side_mode="reversion")
    rev_elig = rev[rev["n"] >= 100]
    print(f"\n=== REVERSION negative control (n>=100): "
          f"best exp={rev_elig['exp'].max():+.4f} mean={rev_elig['exp'].mean():+.4f} "
          f"({time.time()-t2:.1f}s) ===")
    print(f"\ntotal wall: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
