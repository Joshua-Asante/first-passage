"""Breakout under intrabar STOP-LEVEL fill (turtle-style) vs next-open fill.

If breakout is still negative under level-fill, the falsification is convention-robust.
"""
import numpy as np
import usdcad_harness as H


def breakout_stop_entry(bars, rt_cost_pip, side_mode="both"):
    med_atr = np.nanmedian(bars.atr)
    rows = []
    families = [("donchian", N) for N in H.DON_N] + [("orb", M) for M in H.ORB_M]
    for family, param in families:
        for sname, swin in H.SESSIONS.items():
            for vf in H.VOLFLOOR:
                ll, sl, valid = H.build_levels(bars, family, param, swin, vf)
                if valid.sum() == 0:
                    continue
                for k in H.K_STOPS:
                    for emode, eparam in H.EXITS:
                        r = H.simulate_stop_entry(bars, ll, sl, valid, k, emode, eparam,
                                                  rt_cost_pip=rt_cost_pip, side_mode=side_mode)
                        m = H.metrics(r)
                        m.update(family=family, session=sname, k=k,
                                 req=4 * rt_cost_pip * H.PIP / (k * med_atr))
                        rows.append(m)
    import pandas as pd
    return pd.DataFrame(rows)


def main():
    bars = H.load_and_prep()
    for rt in (0.0, 0.8):
        df = breakout_stop_entry(bars, rt)
        e = df[df["n"] >= 100]
        npass = int((e["exp"] >= e["req"]).sum()) if rt > 0 else -1
        print(f"BREAKOUT stop-level fill  rt={rt}p | n_cfg={len(e)} "
              f"frac>0={np.mean(e['exp']>0):.3f} best={e['exp'].max():+.4f} "
              f"mean={e['exp'].mean():+.4f} pass_hurdle={npass if rt>0 else 'n/a'}")
    # best stop-entry breakout config @0.8 for inspection
    df = breakout_stop_entry(bars, 0.8)
    e = df[df["n"] >= 100].sort_values("exp", ascending=False)
    cols = ["family", "session", "k", "n", "exp", "pf", "wr", "req"]
    print("\ntop-6 breakout (stop-entry) @0.8p:")
    print(e[cols].head(6).to_string(index=False,
          formatters={"exp": "{:+.4f}".format, "pf": "{:.3f}".format,
                      "wr": "{:.3f}".format, "req": "{:.3f}".format}))


if __name__ == "__main__":
    main()
