"""Verify PR #259's volume-gate P50 claim on the real trade-list CSV the operator
supplied (986 exit rows / $31,947.96 net matches the RESULTS.md screenshot read
to the cent). Day-level reconstruction + Step-0 + canonical bust engine, same
method as PREREG_filters.md / bust_engine.py, applied to THIS construct.

Reproduction: requires a local, non-committed copy of the operator's
`ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-02_49508.csv` export (the P50-gate
trade list cited in lab/analysis/orb/orb_mym_volume_gate_2026-09-02/RESULTS.md).
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "core"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _reconcile_lite import load_csv  # noqa: E402
from mc.simulation import HORIZON_CAP, run_seed, simulate_path  # noqa: E402
from mc.preflight import firm_kwargs, summarize_outcomes  # noqa: E402

CSV = sys.argv[1] if len(sys.argv) > 1 else str(
    Path.home() / "Downloads" / "ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-02_49508.csv"
)
df = load_csv(CSV)
assert list(df["Size (qty)"].unique()) == [2]
ent = df[df["Type"].str.startswith("Entry")].copy()
ex = df[df["Type"].str.startswith("Exit")].copy()
ex["day"] = pd.to_datetime(ex["dt"].dt.date)
ent["day"] = pd.to_datetime(ent["dt"].dt.date)
tag = ent.set_index("Trade #")["Signal"]
ex["tag"] = ex["Trade #"].map(tag)
ex["hot"] = (ex["tag"].str.contains("Hot") & ~ex["tag"].str.contains("NotHot")).astype(int)

days = ex.groupby("day").agg(pnl=("Net P&L USD", "sum"), n_legs=("Net P&L USD", "size"),
                             hot=("hot", "max"), mae=("Adverse excursion USD", "min"))
days["pnl_pc"] = days["pnl"] / 2.0
days["mae_pc"] = np.minimum(days["mae"] / 2.0, 0.0)

print(f"traded days: {len(days)}  span {days.index.min().date()}..{days.index.max().date()}")
print(f"entry DoW: {ent['dt'].dt.dayofweek.value_counts().sort_index().to_dict()}")
print(f"entry-signal census:\n{ent['Signal'].value_counts().to_string()}")
v = days["pnl_pc"].to_numpy()
gw, gl = v[v > 0].sum(), -v[v < 0].sum()
eq = np.cumsum(v); dd = float((np.maximum.accumulate(eq) - eq).max())
wr_day = float((v > 0).mean())
print(f"\nDAY-LEVEL (per contract): N_days={len(v)}  WR={wr_day*100:.1f}%  Net=${v.sum():,.0f}  "
      f"PF={gw/gl:.3f}  maxDD=${dd:,.0f}  RF={v.sum()/dd:.2f}  worst=${v.min():,.0f}")
print("(cf. LEG-level from RESULTS.md: 986 legs, 57.91% profitable legs, Net $31,947.96, PF 1.451, maxDD $4,621.18)")

hot = days["hot"].to_numpy()
print(f"\nHot-day share: {hot.mean():.3f}  Hot net=${v[hot==1].sum():,.0f} (n={int((hot==1).sum())})  "
      f"NotHot net=${v[hot==0].sum():,.0f} (n={int((hot==0).sum())})")

idx = pd.bdate_range(days.index.min(), days.index.max())
pnl = days["pnl_pc"].reindex(idx, fill_value=0.0)
mae = days["mae_pc"].reindex(idx, fill_value=0.0)
TIERS = {"Select": ("Tradeify_Select_100K", 0.40), "Growth": ("Tradeify_Growth_100K", None)}
SEEDS = (1, 2, 3); N_SIMS = 4000
print("\n=== canonical bootstrap bust/pass, intraday-honest, seeds(1,2,3) x 4000 ===")
for qty in (1, 2):
    p = (pnl * qty).to_numpy(float); q = np.minimum((mae * qty).to_numpy(float), 0.0)
    nw = len(idx) // 5; u = nw * 5
    blocks = p[:u].reshape(nw, 5, 1); iblocks = q[:u].reshape(nw, 5, 1)
    path = p.reshape(-1, 1); low = q
    for tier, (fk, cons) in TIERS.items():
        fkw = firm_kwargs(fk, consistency=cons)
        real = simulate_path(path, 1.0, 1.0, path.shape[0], intraday_low=low, **fkw)
        boot = summarize_outcomes([run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP,
                                            firm_kwargs=fkw, intraday_blocks=iblocks) for sd in SEEDS], N_SIMS)
        print(f"q{qty} {tier:6s} bust={boot['headline_bust']*100:5.1f}%  pass={boot['pass_rate']*100:5.1f}%  "
              f"(realized path: {real[0]}, day {real[1]}, maxDD {real[2]*100:.2f}%)")
