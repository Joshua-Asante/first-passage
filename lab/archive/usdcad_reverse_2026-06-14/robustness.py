"""Robustness of the breakout-NULL / reversion-signal finding to cost & framing.

Decisive question: does breakout lose even GROSS (zero cost)? If yes -> true
directional anti-edge (breakouts fade), not a cost artifact.
"""
import numpy as np
import usdcad_harness as H
from run_grid import run_grid


def grid_at_cost(bars, side_mode, rt_cost_pip):
    df = run_grid(bars, side_mode=side_mode, rt_cost_pip=rt_cost_pip)
    return df[df["n"] >= 100]


def summarize(tag, df, rt):
    hurdle_pass = np.mean(df["exp"] >= df["req_exp"]) if rt > 0 else float("nan")
    print(f"{tag:>26} rt={rt:>3}p | n_cfg={len(df):>3} "
          f"frac>0={np.mean(df['exp']>0):.3f} best={df['exp'].max():+.4f} "
          f"mean={df['exp'].mean():+.4f} pass_hurdle={hurdle_pass if rt==0 else f'{hurdle_pass:.3f}'}")


def main():
    bars = H.load_and_prep()
    print("=== BREAKOUT (pre-registered hypothesis) ===")
    for rt in (0.0, 0.8, 1.6):
        summarize("breakout", grid_at_cost(bars, "both", rt), rt)
    print("\n=== REVERSION (negative control / new observation) ===")
    rev08 = None
    for rt in (0.0, 0.8, 1.6):
        df = grid_at_cost(bars, "reversion", rt)
        summarize("reversion", df, rt)
        if rt == 0.8:
            rev08 = df
    # context on the reversion best-of-K
    print("\n=== reversion @0.8p: how many clear their own 4x-cost hurdle? ===")
    print(f"  configs n>=100: {len(rev08)}  pass 4x-hurdle: {int((rev08['exp']>=rev08['req_exp']).sum())} "
          f"({np.mean(rev08['exp']>=rev08['req_exp'])*100:.1f}%)")
    print("\n  top-8 reversion configs @0.8p:")
    cols = ["family", "param", "session", "volfloor", "k", "exit", "n", "exp", "pf", "wr", "req_exp"]
    top = rev08.sort_values("exp", ascending=False).head(8)
    print(top[cols].to_string(index=False,
          formatters={"exp": "{:+.4f}".format, "pf": "{:.3f}".format,
                      "wr": "{:.3f}".format, "req_exp": "{:.3f}".format}))


if __name__ == "__main__":
    main()
