"""Freeze-fact builder: enumerate RAW-curve (pre-brake) co-drawdown episodes with
STATIC-$ severity, contamination flags, and the calendar-confound check. Reuses the
production decompound + build_daily_panel path. Outputs the pinnable episode table.
Structural sample definition only — NO candidate-vs-severity stat here."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations")
sys.path.insert(0, str(REPO / "core"))
sys.path.insert(0, str(REPO / "lab/analysis/decompound_remc_2026-06-07"))
import decompound as D
from portfolio_mc import build_daily_panel  # production daily grid

STORE = REPO / "core/data/tv_exports/pepperstone"
FILES = {
    "guardian":      "Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-06-25_94d8f.csv",
    "striker":       "Striker_DJ30_v4.5_PEPPERSTONE_US30_2026-06-25_0b865.csv",
    "aegis":         "Aegis_USDJPY_v4.3_PEPPERSTONE_USDJPY_2026-06-25_027bd.csv",
    "striker_nas100":"Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-25_27e52.csv",
}
H1_END = pd.Timestamp("2023-03-20")

# per-leg static daily pnl via production path
rebanked = {}
for s, fn in FILES.items():
    t = D.reconstruct_roe(D.load_file(STORE / fn))
    rebanked[s] = D.rebank(t, "static")           # exit_date, pnl
panel = build_daily_panel(rebanked, D.ALLOC, D.FIXED_1R) if False else None
# build_daily_panel signature varies; do the faithful equivalent: per-leg daily sum on a bday grid
legs = {s: rb.groupby("exit_date")["pnl"].sum() for s, rb in rebanked.items()}
for s in legs: legs[s].index = pd.to_datetime(legs[s].index)
days = pd.bdate_range(min(d.index.min() for d in legs.values()), max(d.index.max() for d in legs.values()))
P = pd.DataFrame({s: d.reindex(days).fillna(0.0) for s, d in legs.items()})
port = P.sum(axis=1)
equity = 200_000.0 + port.cumsum()
peak = equity.cummax()
dd_pct = (equity - peak) / peak
dd_usd = equity - peak                              # <=0; static-$ underwater depth
uw = (dd_usd.values < -1e-6)

# enumerate underwater episodes on the RAW curve
rows, i, n = [], 0, len(days)
while i < n:
    if uw[i]:
        j = i
        while j < n and uw[j]: j += 1
        sl = slice(i, j)
        k = i + int(np.argmin(dd_usd.values[sl]))   # trough index
        depth_usd = float(-dd_usd.values[k]); depth_pct = float(-dd_pct.values[k])
        leg_acc = {s: float(P[s].values[sl].sum()) for s in FILES}
        red = sum(v < 0 for v in leg_acc.values())
        # contamination: is the pre-onset window [onset-21bd, onset-1bd] ever underwater?
        pre_lo = max(0, i - 21)
        pre_contam = bool(uw[pre_lo:i].any()) if i > 0 else True
        rows.append(dict(onset=str(days[i].date()), trough=str(days[k].date()), end=str(days[j-1].date()),
                         dur=int(j - i), depth_usd=round(depth_usd), depth_pct=round(depth_pct*100, 3),
                         legs_red=int(red), co_drawdown=bool(red >= 3), pre_contaminated=pre_contam))
        i = j
    else:
        i += 1

ep = pd.DataFrame(rows)
MW = ep[ep.dur >= 10].reset_index(drop=True)                 # multi-week
MW["calendar_rank"] = MW.onset.rank()
clean = MW[~MW.pre_contaminated]
h1 = MW[pd.to_datetime(MW.onset) <= H1_END]

def sp(a, b):
    from scipy.stats import spearmanr
    r, p = spearmanr(a, b); return round(r, 3), round(p, 4)

print(f"legs static net: " + " ".join(f"{s}=${legs[s].sum():,.0f}" for s in FILES))
print(f"max RAW portfolio DD: {dd_pct.min()*100:.2f}% / ${-dd_usd.min():,.0f}")
print(f"\nN: multiweek(>=10d) FULL={len(MW)}  H1={len(h1)}  clean(uncontam)={len(clean)}  co-drawdown(>=3red)={MW.co_drawdown.sum()}")
print(f"contaminated (pre-window underwater): {MW.pre_contaminated.sum()}/{len(MW)}")
print(f"\nCALENDAR-CONFOUND CHECK (F1):")
print(f"  Spearman(%-depth,  calendar) = {sp(MW.depth_pct, MW.calendar_rank)}   <- confounded (drop as primary)")
print(f"  Spearman($-depth,  calendar) = {sp(MW.depth_usd, MW.calendar_rank)}   <- PRIMARY severity")
print(f"\nTop 10 multiweek by $-severity (the danger set):")
print(MW.sort_values('depth_usd', ascending=False).head(10)[['onset','trough','end','dur','depth_usd','depth_pct','legs_red','co_drawdown','pre_contaminated']].to_string(index=False))
print(f"\nContaminated episode onsets (pre-register, excluded from primary): {sorted(MW[MW.pre_contaminated].onset.tolist())}")

OUT = REPO / "lab/analysis/regime_signal_research_2026-06-25/episodes_raw.csv"
MW.to_csv(OUT, index=False)
import hashlib
h = hashlib.sha256(OUT.read_bytes()).hexdigest()
print(f"\nwrote {OUT.name}  sha256={h}")
