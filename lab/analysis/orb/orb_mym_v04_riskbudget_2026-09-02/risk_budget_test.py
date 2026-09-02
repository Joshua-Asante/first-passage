"""Score the pre-registered `riskBudgetUsd` input (PREREG_risk_budget.md) on the P50 export.

ORR from a canonical bar CSV covering 2020 H1 (session bucketing replicates
load_sessions.load_bars: hour>=18 ET -> next session). This repo's own
`core/data/bar_data/MYM_M15.csv` starts 2020-07-01 and does NOT cover the
2020-02/03 window this screen's worst day falls in — a longer panel is
required. Reproduction:

    python scripts/parse_bar_export.py --symbol MYM \
        --in <local BAR_EXPORT_v0.2_CBOT_MINI_MYM1!_2026-09-01_1b59b.csv> \
        --out /tmp/MYM_M15_long.csv
    python risk_budget_test.py /tmp/MYM_M15_long.csv \
        <local ORB-MYM-1_v0.4_..._2026-09-02_49508.csv>

Both inputs are vendor-sourced / operator-exported and are not committed
(same posture as core/data/bar_data/ and every trade-CSV in this repo).
"""
from __future__ import annotations
import os, sys, json
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "core"))
sys.path.insert(0, str(HERE))
from mc.simulation import HORIZON_CAP, run_seed, simulate_path  # noqa: E402
from mc.preflight import firm_kwargs, summarize_outcomes  # noqa: E402
from _reconcile_lite import load_csv  # noqa: E402

BARS = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "MYM_M15_long.csv"
CSV = sys.argv[2] if len(sys.argv) > 2 else str(
    Path.home() / "Downloads" / "ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-09-02_49508.csv"
)
POINTVALUE, LEGS, SL_MULT, QTY = 0.5, 3, 2.5, 2
SEEDS, N_SIMS = (1, 2, 3), int(os.environ.get("N_SIMS", "4000"))
TIERS = {"Select": ("Tradeify_Select_100K", 0.40), "Growth": ("Tradeify_Growth_100K", None)}

# ---- bars -> per-session ORR (09:15 + 09:30 ET bars, union range) — same construction as feat_lib
b = pd.read_csv(BARS)
ts = pd.to_datetime(b["time"], utc=True).dt.tz_convert("America/New_York")
b = pd.DataFrame({"ts": ts, "high": b["high"].astype(float), "low": b["low"].astype(float)}).sort_values("ts")
hour = b["ts"].dt.hour; date = b["ts"].dt.date
b["session"] = pd.to_datetime(np.where(hour >= 18, pd.DatetimeIndex(date) + pd.Timedelta(days=1), pd.DatetimeIndex(date)))
b["minute"] = b["ts"].dt.hour * 60 + b["ts"].dt.minute
orb = b[b["minute"].isin([555, 570])].groupby("session").agg(high=("high", "max"), low=("low", "min"), n=("high", "size"))
orb = orb[orb["n"] == 2]
orr = (orb["high"] - orb["low"]).rename("orr")
print(f"bars {len(b)}  sessions with both OR bars: {len(orr)}  span {orr.index.min().date()}..{orr.index.max().date()}")

# ---- P50 trade list -> day frame
df = load_csv(CSV); assert list(df["Size (qty)"].unique()) == [QTY]
ent = df[df["Type"].str.startswith("Entry")].copy(); ex = df[df["Type"].str.startswith("Exit")].copy()
ex["day"] = pd.to_datetime(ex["dt"].dt.date); ent["day"] = pd.to_datetime(ent["dt"].dt.date)
tag = ent.set_index("Trade #")["Signal"]; ex["tag"] = ex["Trade #"].map(tag)
ex["hot"] = (ex["tag"].str.contains("Hot") & ~ex["tag"].str.contains("NotHot")).astype(int)
d = ex.groupby("day").agg(pnl=("Net P&L USD", "sum"), hot=("hot", "max"), mae=("Adverse excursion USD", "min"), legs=("Net P&L USD", "size"))
d["pnl_pc"] = d["pnl"] / QTY; d["mae_pc"] = np.minimum(d["mae"] / QTY, 0.0)
d = d.join(orr, how="left")
s = d[d["orr"].notna()].copy()
print(f"P50 traded days {len(d)}; with ORR {len(s)} ({s.index.min().date()}..{s.index.max().date()}); "
      f"ORR median {s.orr.median():.0f} p80 {s.orr.quantile(.8):.0f} p95 {s.orr.quantile(.95):.0f} max {s.orr.max():.0f}")
s["planned_risk_pc"] = LEGS * SL_MULT * s["orr"] * POINTVALUE   # $ per contract, full 3-leg position to the stop
print("worst days' ORR / planned $-risk at q2:")
print(s.sort_values("pnl_pc").head(6)[["pnl_pc", "hot", "legs", "orr", "planned_risk_pc"]].assign(risk_q2=lambda x: x.planned_risk_pc * 2).round(0).to_string())


def qty_for(budget: float, cap: int = QTY) -> np.ndarray:
    return np.minimum(cap, np.floor(budget / s["planned_risk_pc"].to_numpy())).astype(int)


def cell(size: np.ndarray, label: str) -> dict:
    idx = pd.bdate_range(s.index.min(), s.index.max())
    p = (s["pnl_pc"] * size).reindex(idx, fill_value=0.0).to_numpy(float)
    q = np.minimum((s["mae_pc"] * size).reindex(idx, fill_value=0.0).to_numpy(float), 0.0)
    nw = len(idx) // 5; u = nw * 5
    blocks, iblocks = p[:u].reshape(nw, 5, 1), q[:u].reshape(nw, 5, 1)
    eq = np.cumsum(p); maxdd = float((np.maximum.accumulate(eq) - eq).max())
    out = {"label": label, "days_traded": int((size > 0).sum()), "mean_qty_on_traded": float(size[size > 0].mean()) if (size > 0).any() else 0,
           "net": float(p.sum()), "maxdd": maxdd, "worst_day": float(p.min())}
    for tier, (fk, cons) in TIERS.items():
        fkw = firm_kwargs(fk, consistency=cons)
        real = simulate_path(p.reshape(-1, 1), 1.0, 1.0, len(p), intraday_low=q, **fkw)
        rs = [run_seed(sd, N_SIMS, blocks, 1.0, 1.0, horizon=HORIZON_CAP, firm_kwargs=fkw, intraday_blocks=iblocks) for sd in SEEDS]
        boot = summarize_outcomes(rs, N_SIMS)
        dtp = np.concatenate([np.asarray(r["days_to_pass"], dtype=float) for r in rs]) if any(r["days_to_pass"] for r in rs) else np.array([np.nan])
        out[tier] = {"bust": round(boot["headline_bust"] * 100, 2), "pass": round(boot["pass_rate"] * 100, 2),
                     "median_days_to_pass": float(np.nanmedian(dtp)), "realized": [real[0], int(real[1]), round(real[2] * 100, 2)]}
        print(f"  {label:34s} {tier:6s} bust={out[tier]['bust']:6.2f}% pass={out[tier]['pass']:6.2f}% "
              f"med-days={out[tier]['median_days_to_pass']:5.0f}  realized={real[0]}@{real[1]} maxDD {real[2]*100:.2f}%", flush=True)
    return out


ones = np.ones(len(s), dtype=int)
cells = [
    ("base q1-flat", ones * 1),
    ("base q2-flat", ones * 2),
    ("PRIMARY budget $1,500", qty_for(1500)),
    ("neighbor budget $1,000", qty_for(1000)),
    ("neighbor budget $2,000", qty_for(2000)),
    ("variant hard-cap only (q2 or skip @$1,500)", np.where(s["planned_risk_pc"].to_numpy() * 2 <= 1500, 2, 0)),
    ("variant budget $1,500 at base qty 1", qty_for(1500, cap=1)),
]
results = []
for label, size in cells:
    print(f"\n[{label}] days={int((size>0).sum())} qty census={dict(zip(*np.unique(size, return_counts=True)))}", flush=True)
    results.append(cell(size.astype(float), label))
    (HERE / "risk_budget_results.json").write_text(json.dumps(results, indent=2, default=str))
print("\ndone", flush=True)
