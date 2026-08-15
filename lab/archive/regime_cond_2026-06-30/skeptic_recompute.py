"""PASS D skeptic — INDEPENDENT recomputation of one residual-state SEP_vol (5d).

Does NOT import conditional.py / panel.py logic. Reimplements:
  - fresh SPY fetch + trailing 20d RV
  - expanding PIT OLS residual of composite_eqw ~ [1, RV]   (own implementation)
  - expanding PIT tercile states on the residual                (own implementation)
  - non-overlapping 5d forward log returns, conditional stdev per state, SEP_vol(off-on)
Goal: confirm the run isn't silently mis-bucketing. Compare to conditional_results.json
residual_states_eqw_PIT 5d SEP_vol ~ -0.0007.
"""
import json, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
WARMUP = 252
RV_WIN = 20

# --- fresh SPY fetch (independent) ---
raw = urllib.request.urlopen(urllib.request.Request(
    "https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=30y&interval=1d",
    headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
r = json.loads(raw)["chart"]["result"][0]
ts = pd.to_datetime(r["timestamp"], unit="s").normalize()
adj = pd.Series(r["indicators"]["adjclose"][0]["adjclose"], index=ts, dtype="float64").dropna().sort_index()
adj = adj[~adj.index.duplicated(keep="last")]
logret = np.log(adj).diff().dropna()
rv = logret.rolling(RV_WIN).std()

# --- frozen composite from panel.csv ---
panel = pd.read_csv(HERE / "panel.csv", index_col=0, parse_dates=True)
comp = panel["composite_eqw"].dropna()
rv_on = rv.reindex(comp.index)

# --- expanding PIT OLS residual: comp ~ [1, rv] (independent impl, loop with np.polyfit on prefix) ---
df = pd.DataFrame({"y": comp, "x": rv_on}).dropna()
yv, xv = df["y"].to_numpy(), df["x"].to_numpy()
n = len(df)
res = np.full(n, np.nan)
for i in range(n):
    if i + 1 >= WARMUP:
        b1, b0 = np.polyfit(xv[:i+1], yv[:i+1], 1)  # slope, intercept
        res[i] = yv[i] - (b0 + b1 * xv[i])
resid = pd.Series(res, index=df.index).dropna()
print(f"corr(residual, RV) = {pd.concat([resid, rv_on], axis=1).dropna().corr().iloc[0,1]:+.4f}  (expect ~ -0.28)")

# --- expanding PIT tercile states on residual (independent impl) ---
rv_arr = resid.to_numpy()
states = np.array([None] * len(resid), dtype=object)
for i in range(len(resid)):
    if i + 1 >= WARMUP:
        hist = rv_arr[:i+1]
        q33, q67 = np.quantile(hist, [1/3, 2/3])
        v = rv_arr[i]
        states[i] = "off" if v >= q67 else ("on" if v <= q33 else "neutral")
states = pd.Series(states, index=resid.index)
print(f"state counts: {states.value_counts().to_dict()}")

# --- 5d non-overlapping forward log returns ---
h = 5
lr = logret.to_numpy(); idx = logret.index
fwd = np.full(len(lr), np.nan)
for i in range(len(lr) - h):
    fwd[i] = lr[i+1:i+1+h].sum()
fwd_s = pd.Series(fwd, index=idx)

joined = pd.DataFrame({"state": states}).join(fwd_s.rename("fwd"), how="inner").dropna()
joined = joined[joined["state"].notna()]
nonov = joined.iloc[::h]
grp = {st: nonov[nonov["state"] == st]["fwd"].to_numpy() for st in ("off", "neutral", "on")}
std = {st: float(np.std(grp[st], ddof=1)) for st in grp}
print(f"n per state (nonoverlap): {{ {', '.join(f'{k}:{len(grp[k])}' for k in grp)} }}")
print(f"stdev off={std['off']:.5f} neutral={std['neutral']:.5f} on={std['on']:.5f}")
sep_vol = std["off"] - std["on"]
print(f"SEP_vol (off-on) = {sep_vol:+.5f}")
print(f"monotone off>neu>on? {std['off'] > std['neutral'] > std['on']}")
print(f"\nRun's reported residual_PIT 5d SEP_vol = -0.00069  ; mine = {sep_vol:+.5f}")
