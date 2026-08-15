"""Loop 2: pre-registered trend-pullback (ema_recovery) grid + H1/H2 decisive gate.

Pre-reg: docs/briefs/pre-registration/PREREG-USDCAD-PULLBACK-2026-06-14.md
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd

import usdcad_harness as H

OUT = Path(__file__).parent / "pullback_results.csv"
H1_END = pd.Timestamp("2026-03-22", tz="UTC")  # ~midpoint of 2026-01..06 by time


def pullback_families():
    return [("pullback", (f, s)) for f in H.EMA_FAST for s in H.EMA_SLOW if f < s]


def run(bars, side_mode="both", rt_cost_pip=None, mask=None):
    rt = H.RT_COST_PIP if rt_cost_pip is None else rt_cost_pip
    med_atr = np.nanmedian(bars.atr)
    rows = []
    for family, param in pullback_families():
        for sname, swin in H.SESSIONS.items():
            for vf in H.VOLFLOOR:
                ls, ss = H.build_signals(bars, family, param, swin, vf)
                if mask is not None:
                    ls = ls & mask
                    ss = ss & mask
                if ls.sum() + ss.sum() == 0:
                    continue
                for k in H.K_STOPS:
                    for emode, eparam in H.EXITS:
                        r = H.simulate(bars, ls, ss, k, emode, eparam,
                                       rt_cost_pip=rt, side_mode=side_mode)
                        m = H.metrics(r)
                        m.update(fast=param[0], slow=param[1], session=sname, volfloor=vf,
                                 k=k, exit=f"{emode}{eparam}",
                                 req_exp=4 * rt * H.PIP / (k * med_atr))
                        rows.append(m)
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    bars = H.load_and_prep()
    df = run(bars, "both")
    df.to_csv(OUT, index=False)
    elig = df[df["n"] >= 100].sort_values("exp", ascending=False)
    cols = ["fast", "slow", "session", "volfloor", "k", "exit", "n", "exp", "pf", "wr",
            "profitR", "maxddR", "req_exp"]
    pd.set_option("display.width", 220, "display.max_columns", 30)
    print(f"=== PULLBACK grid: {len(df)} configs, {len(elig)} eligible (n>=100) "
          f"({time.time()-t0:.1f}s) ===")
    print(f"expectancy: mean={elig['exp'].mean():+.4f} median={elig['exp'].median():+.4f} "
          f"max={elig['exp'].max():+.4f} frac>0={np.mean(elig['exp']>0):.3f} "
          f"pass_hurdle={np.mean(elig['exp']>=elig['req_exp']):.3f}")
    print("\nTOP 12 by net expectancy:")
    print(elig[cols].head(12).to_string(index=False,
          formatters={"exp": "{:+.4f}".format, "pf": "{:.3f}".format, "wr": "{:.3f}".format,
                      "profitR": "{:+.1f}".format, "maxddR": "{:.1f}".format,
                      "req_exp": "{:.3f}".format}))

    # session + anti control
    print("\nmean exp by session (n>=100):")
    print(elig.groupby("session")["exp"].agg(["count", "mean", "max"]).round(4).to_string())
    anti = run(bars, "reversion")
    ae = anti[anti["n"] >= 100]
    print(f"\nANTI control (fade the pullback): best={ae['exp'].max():+.4f} mean={ae['exp'].mean():+.4f}")

    # ---- DECISIVE GATE: H1/H2 stationarity on the in-sample winner ----
    if len(elig) and elig["exp"].iloc[0] > 0:
        w = elig.iloc[0]
        print(f"\n=== H1/H2 stationarity on in-sample winner: "
              f"fast{w['fast']}/slow{w['slow']} {w['session']} vf={w['volfloor']} "
              f"k{w['k']} {w['exit']} (exp {w['exp']:+.4f}) ===")
        swin = H.SESSIONS[w["session"]]
        ls, ss = H.build_signals(bars, "pullback", (int(w["fast"]), int(w["slow"])),
                                 swin, bool(w["volfloor"]))
        ex = w["exit"]
        if ex.startswith("trail"):
            emode, eparam = "trail", float(ex.replace("trail", ""))
        else:
            emode, eparam = "tp", float(ex.replace("tp", ""))
        # H1/H2 masks on signal-bar time (epoch), split at the time midpoint
        times = _bar_times_utc()
        h1 = times < H1_END
        for label, m in [("H1 Jan-Mar", h1), ("H2 Apr-Jun", ~h1)]:
            r = H.simulate(bars, ls & m, ss & m, w["k"], emode, eparam, side_mode="both")
            mm = H.metrics(r)
            print(f"  {label}: n={mm['n']:>4} exp={mm['exp']:+.4f} pf={mm['pf']:.3f} "
                  f"wr={mm['wr']:.3f}")
        print("  GATE: PASS requires BOTH halves exp>0 (strict).")
    else:
        print("\nNo positive in-sample winner -> NULL before deflation.")
    print(f"\ntotal wall: {time.time()-t0:.1f}s")


def _bar_times_utc():
    raw = pd.read_csv(H.DEFAULT_CSV, encoding="utf-8-sig")
    raw.columns = [str(c).strip() for c in raw.columns]
    e = raw[raw["Type"].astype(str).str.startswith("Entry")]
    eps = []
    for _, r in e.iterrows():
        m = H.SIGNAL_PIPE_RE.match(str(r["Signal"]).strip())
        if m:
            eps.append(int(m.group("e")))
    eps = np.sort(np.array(eps))
    return pd.to_datetime(eps, unit="ms", utc=True)


if __name__ == "__main__":
    main()
