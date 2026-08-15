"""Provenance: build glm_inputs.csv (the frozen I1+I2 inputs) from the parent battery's
episodes_raw.csv + the production US500 15m bars. Reuses run_battery.py's EXACT covariate
recipe: asof = last obs strictly before onset; RV = 21d rolling std of US500 daily log-returns.

Output columns:
  onset                  episode first-underwater day (decision point = the bday BEFORE this)
  depth_usd              PRIMARY severity (static-$ trough depth on a flat $200K base)
  rv_at_peak             I2 vol covariate: S&P-500 (US500) 21d realized vol, peak-sampled
  calendar_rank          I2 calendar covariate (onset rank; already in episodes_raw.csv)
  legs_red/co_drawdown/pre_contaminated   context flags
  rv_finite              True for the N=33 usable episodes (the 2020-01-13 episode drops:
                         US500 history starts 2020-01-01 -> no 21d trailing window)
  severity_rank_worst1   1 = deepest co-drawdown

NOTE: US500_M15.csv is gitignored vendor data (lives in the main checkout, not the worktree).
glm_inputs.csv is checked in frozen so score_newfree.py reproduces WITHOUT the raw bars.
"""
from pathlib import Path
import numpy as np, pandas as pd

# US500 bars live under the main checkout's vendor tree (gitignored); adjust if your path differs.
REPO = Path(r"C:/Users/joshu/multi_firm_operations")
BD = REPO / "core/data/bar_data"
HERE = Path(__file__).resolve().parent
PARENT = HERE.parent  # regime_signal_research_2026-06-25/

ep = pd.read_csv(PARENT / "episodes_raw.csv"); ep["onset"] = pd.to_datetime(ep["onset"])
onsets = ep["onset"]


def asof(df, onsets):
    s = df.sort_index()
    return np.array([(s.loc[s.index < o]["v"].iloc[-1] if (s.index < o).any() else np.nan) for o in onsets], float)


def daily_close(path):
    d = pd.read_csv(path)
    d["t"] = pd.to_datetime(d["time"], utc=True).dt.tz_localize(None)
    d["date"] = d["t"].dt.normalize()
    return d.groupby("date")["close"].last()


us500d = daily_close(BD / "US500_M15.csv")
rv = (np.log(us500d).diff().rolling(21).std()).to_frame("v")
RV = asof(rv, onsets)

out = ep[["onset", "depth_usd", "calendar_rank", "legs_red", "co_drawdown", "pre_contaminated"]].copy()
out["onset"] = out["onset"].dt.date
out.insert(2, "rv_at_peak", RV)
out["rv_finite"] = np.isfinite(RV)
out["severity_rank_worst1"] = out["depth_usd"].rank(ascending=False).astype(int)
out.to_csv(HERE / "glm_inputs.csv", index=False)
print(out.to_string(index=False))
print(f"\nUS500 daily span: {us500d.index.min().date()}..{us500d.index.max().date()}")
print(f"N total={len(out)}  RV-finite(usable)={int(out.rv_finite.sum())}")
print(f"wrote {HERE / 'glm_inputs.csv'}")
