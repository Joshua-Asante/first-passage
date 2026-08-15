#!/usr/bin/env python3
"""INQHIORI Identify-phase ground-truth producer: NAS100 bar feed vs Striker NAS100 v1 trades (prev 2 years).

Computes the verified I/N corpus ONCE (avoids the anchor-drift trade-csv-reconcile warns about).
Outputs:
  - nas100_bars_utc.csv          canonical UTC OHLCV (via core/bar_export_loader)
  - nas100_trades_paired.csv     per-leg trades, classified base/pyramid_add, bar-matched
  - nas100_identify_stats.json   all headline + regime + juxtaposition stats
This file ONLY characterizes. It does not form hypotheses, replicate Pine entry logic, or route to action.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

REPO = Path(r"C:/Users/joshu/multi_firm_operations/.claude/worktrees/tender-perlman-7824ea")
sys.path.insert(0, str(REPO / "core"))
from bar_export_loader import parse_bar_export  # noqa: E402

DL = Path(r"C:/Users/joshu/Downloads")
BAR_PAGES = [
    DL / "BAR_EXPORT_v0.1_PEPPERSTONE_NAS100_2026-06-20_f780b.csv",  # earlier window
    DL / "BAR_EXPORT_v0.1_PEPPERSTONE_NAS100_2026-06-20_c64de.csv",  # 2026 window
]
TRADES_CSV = DL / "Striker_NAS100_v1_PEPPERSTONE_NAS100_2026-06-20_59840.csv"
OUT = REPO / "lab" / "analysis" / "identify_nas100_2026-06-20"
OUT.mkdir(parents=True, exist_ok=True)

ET = ZoneInfo("America/New_York")
ACCOUNT = 200_000.0
FULLSTOP_THRESH = 0.01 * ACCOUNT  # >$2000 loss = full-stop cohort (striker_nas archetype)

stats: dict = {}


def jround(x, n=4):
    if x is None:
        return None
    if isinstance(x, (np.floating, np.integer)):
        x = x.item()
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)):
        return None
    return round(x, n)


# ───────────────────────── 1. BAR DATA ─────────────────────────
bars = parse_bar_export(BAR_PAGES, symbol="NAS100")
bars["time"] = pd.to_datetime(bars["time"], utc=True)
bars = bars.sort_values("time").drop_duplicates(subset="time").reset_index(drop=True)
bars.to_csv(OUT / "nas100_bars_utc.csv", index=False)

n_bars = len(bars)
t0, t1 = bars["time"].iloc[0], bars["time"].iloc[-1]
span_days = (t1 - t0).total_seconds() / 86400.0

# bar spacing / gaps
dt_min = bars["time"].diff().dt.total_seconds().div(60).dropna()
modal_spacing = dt_min.mode().iloc[0]
gap_counts = dt_min.value_counts().head(8).to_dict()
big_gaps = dt_min[dt_min > 60]  # > 1h
# largest gaps with context
gap_idx = dt_min.sort_values(ascending=False).head(10).index
largest_gaps = []
for i in gap_idx:
    largest_gaps.append({
        "from": str(bars["time"].iloc[i - 1]),
        "to": str(bars["time"].iloc[i]),
        "gap_hours": jround(dt_min.loc[i] / 60, 2),
    })

# index price behavior
c = bars["close"].to_numpy()
logret = np.diff(np.log(c))
roll_peak = np.maximum.accumulate(c)
idx_dd = (c - roll_peak) / roll_peak
max_idx_dd = idx_dd.min()
max_idx_dd_at = str(bars["time"].iloc[int(idx_dd.argmin())])

# true range / ATR(11) RMA (Wilder) -- DESCRIPTIVE regime context, NOT entry-filter replication
h, l = bars["high"].to_numpy(), bars["low"].to_numpy()
prev_c = np.concatenate([[c[0]], c[:-1]])
tr = np.maximum.reduce([h - l, np.abs(h - prev_c), np.abs(l - prev_c)])
atr = pd.Series(tr).ewm(alpha=1 / 11, adjust=False).mean().to_numpy()  # RMA approx
atr_ma = pd.Series(atr).rolling(85).mean().to_numpy()
with np.errstate(invalid="ignore", divide="ignore"):
    atr_ratio = atr / atr_ma  # >1.28 ~ "expanded" per 0.28 expansion param (descriptive only)
bars["atr11"] = atr
bars["atr_ratio"] = atr_ratio

# session / DOW tagging (UTC, bar-open)
bars["utc_hour"] = bars["time"].dt.hour
bars["utc_dow"] = bars["time"].dt.dayofweek  # Mon=0
bars["utc_date"] = bars["time"].dt.date
in_session = bars["utc_hour"].isin([13, 14, 15, 16])      # 13:00-17:00 UTC bar-opens
eligible_dow = bars["utc_dow"].isin([0, 1])               # Mon, Tue
post_warmup = bars["utc_hour"].isin([13, 14, 15, 16]) & ~(
    (bars["utc_hour"] == 13) & (bars["time"].dt.minute < 45)
)  # warmup >3 bars => first eligible entry bar opens 13:45
bars["eligible_bar"] = in_session & eligible_dow

session_days = bars.loc[in_session, "utc_date"].nunique()
eligible_session_days = bars.loc[bars["eligible_bar"], "utc_date"].nunique()
mon_tue_dates = bars.loc[eligible_dow, "utc_date"].nunique()

stats["bar_data"] = {
    "n_bars": n_bars,
    "utc_first": str(t0),
    "utc_last": str(t1),
    "span_days": jround(span_days, 1),
    "modal_spacing_min": jround(modal_spacing, 1),
    "spacing_value_counts_min": {jround(k, 1): int(v) for k, v in gap_counts.items()},
    "n_gaps_gt_1h": int((dt_min > 60).sum()),
    "largest_gaps": largest_gaps,
    "index_first_close": jround(c[0], 1),
    "index_last_close": jround(c[-1], 1),
    "index_total_return_pct": jround((c[-1] / c[0] - 1) * 100, 2),
    "index_min_close": jround(c.min(), 1),
    "index_max_close": jround(c.max(), 1),
    "index_max_drawdown_pct": jround(max_idx_dd * 100, 2),
    "index_max_drawdown_at": max_idx_dd_at,
    "bar_logret_std_15m": jround(np.std(logret), 6),
    "bar_logret_ann_vol_pct": jround(np.std(logret) * np.sqrt(96 * 252) * 100, 1),
    "atr11_median": jround(np.nanmedian(atr), 2),
    "atr11_p10": jround(np.nanpercentile(atr, 10), 2),
    "atr11_p90": jround(np.nanpercentile(atr, 90), 2),
    "atr_ratio_median": jround(np.nanmedian(atr_ratio), 3),
    "frac_bars_atr_expanded_gt1.28": jround(np.nanmean(atr_ratio > 1.28), 4),
    "session_days_any_dow_in_13_17utc": int(session_days),
    "eligible_session_days_mon_tue_13_17utc": int(eligible_session_days),
    "mon_tue_calendar_days": int(mon_tue_dates),
    "n_in_session_bars": int(in_session.sum()),
    "n_eligible_bars_montue_session": int(bars["eligible_bar"].sum()),
}

# ── regime by quarter (index return, vol, atr) ──
bars["q"] = bars["time"].dt.to_period("Q").astype(str)
qg = []
for q, g in bars.groupby("q"):
    cc = g["close"].to_numpy()
    lr = np.diff(np.log(cc))
    rp = np.maximum.accumulate(cc)
    dd = ((cc - rp) / rp).min()
    qg.append({
        "quarter": q,
        "n_bars": len(g),
        "ret_pct": jround((cc[-1] / cc[0] - 1) * 100, 2),
        "ann_vol_pct": jround(np.std(lr) * np.sqrt(96 * 252) * 100, 1),
        "max_dd_pct": jround(dd * 100, 2),
        "atr11_median": jround(np.nanmedian(g["atr11"]), 1),
        "frac_atr_expanded": jround(np.nanmean(g["atr_ratio"] > 1.28), 3),
    })
stats["bar_regime_by_quarter"] = qg


# ───────────────────────── 2. TRADES ─────────────────────────
tr_raw = pd.read_csv(TRADES_CSV, encoding="utf-8-sig")
tr_raw.columns = [str(x).strip() for x in tr_raw.columns]
tid = "Trade number"
tr_raw[tid] = tr_raw[tid].astype(int)

entries = tr_raw[tr_raw["Type"].str.startswith("Entry")].copy()
exits = tr_raw[tr_raw["Type"].str.startswith("Exit")].copy()

# realized P&L lives on EXIT rows only (trade-csv-reconcile trap #3)
legs = entries[[tid, "Date and time", "Signal", "Price USD", "Size (qty)"]].rename(
    columns={"Date and time": "entry_dt", "Signal": "entry_signal",
             "Price USD": "entry_px", "Size (qty)": "qty"}
).merge(
    exits[[tid, "Date and time", "Signal", "Price USD",
           "Net PnL USD", "Net PnL %", "Favorable excursion USD", "Adverse excursion USD",
           "Cumulative PnL USD"]].rename(
        columns={"Date and time": "exit_dt", "Signal": "exit_signal", "Price USD": "exit_px",
                 "Net PnL USD": "pnl", "Net PnL %": "pnl_pct",
                 "Favorable excursion USD": "mfe", "Adverse excursion USD": "mae",
                 "Cumulative PnL USD": "cum_pnl"}),
    on=tid, how="inner",
).sort_values(tid).reset_index(drop=True)

legs["leg_type"] = np.where(legs["entry_signal"].str.contains("Add"), "pyramid_add", "base")
legs["entry_dt"] = pd.to_datetime(legs["entry_dt"])
legs["exit_dt"] = pd.to_datetime(legs["exit_dt"])

# resolve trade-CSV timezone EMPIRICALLY via bar close cross-check (don't assume ET vs UTC)
bar_by_time = bars.set_index("time")["close"]


def match_rate(hypothesis: str):
    hits, tot = 0, 0
    for _, r in legs.iterrows():
        naive = r["entry_dt"]
        if hypothesis == "ET":
            utc = naive.tz_localize(ET).tz_convert("UTC")
        else:  # naive-as-UTC
            utc = naive.tz_localize("UTC")
        utc = utc.floor("15min")
        tot += 1
        if utc in bar_by_time.index and abs(bar_by_time.loc[utc] - r["entry_px"]) <= max(1.0, r["entry_px"] * 1e-4):
            hits += 1
    return hits, tot


et_hits, tot = match_rate("ET")
utc_hits, _ = match_rate("UTC")
tz_used = "ET" if et_hits >= utc_hits else "UTC"

# attach bar context using resolved tz
ctx_rows = []
for _, r in legs.iterrows():
    naive = r["entry_dt"]
    utc = (naive.tz_localize(ET).tz_convert("UTC") if tz_used == "ET" else naive.tz_localize("UTC")).floor("15min")
    row = {"matched": False, "bar_utc": None, "bar_close": None, "atr11": None,
           "atr_ratio": None, "utc_hour": None, "utc_dow": None, "ret_20bar_pct": None}
    if utc in bar_by_time.index:
        bi = bars.index[bars["time"] == utc]
        if len(bi):
            i = int(bi[0])
            close_ok = abs(bars["close"].iloc[i] - r["entry_px"]) <= max(1.0, r["entry_px"] * 1e-4)
            row.update({
                "matched": bool(close_ok),
                "bar_utc": str(utc),
                "bar_close": jround(bars["close"].iloc[i], 1),
                "atr11": jround(bars["atr11"].iloc[i], 1),
                "atr_ratio": jround(bars["atr_ratio"].iloc[i], 3),
                "utc_hour": int(bars["utc_hour"].iloc[i]),
                "utc_dow": int(bars["utc_dow"].iloc[i]),
                "ret_20bar_pct": jround((bars["close"].iloc[i] / bars["close"].iloc[max(0, i - 20)] - 1) * 100, 2),
            })
    ctx_rows.append(row)
ctx = pd.DataFrame(ctx_rows)
legs = pd.concat([legs, ctx], axis=1)
legs.to_csv(OUT / "nas100_trades_paired.csv", index=False)

base = legs[legs["leg_type"] == "base"]
add = legs[legs["leg_type"] == "pyramid_add"]

# headline metrics (legs)
net = legs["pnl"].sum()
wins = legs[legs["pnl"] > 0]
losses = legs[legs["pnl"] <= 0]
gw, gl = wins["pnl"].sum(), losses["pnl"].sum()
pf = gw / abs(gl) if gl != 0 else None

# equity DD on cumulative (trade-close), static $200k base
eq = ACCOUNT + legs["pnl"].cumsum().to_numpy()
peak = np.maximum.accumulate(eq)
dd = (eq - peak) / peak
maxdd_pct = dd.min() * 100
maxdd_usd = (eq - peak).min()

# 1R: full-stop cohort mean (striker_nas archetype)
fullstops = legs[legs["pnl"] <= -FULLSTOP_THRESH]
n_fs = len(fullstops)
if n_fs == 0:
    r1 = abs(legs[legs["pnl"] < 0]["pnl"].median())
    r1_basis = "median_loss_fallback (n_fullstop=0)"
else:
    r1 = abs(fullstops["pnl"].mean())
    r1_basis = f"fullstop_cohort_mean (n={n_fs})"
cohort_warning = 1 <= n_fs < 5

# pyramid share
pyr_share = add["pnl"].sum() / net if net != 0 else None

# exit-type breakdown
exit_break = {}
for sig, g in legs.groupby("exit_signal"):
    exit_break[sig] = {"n": int(len(g)), "pnl": jround(g["pnl"].sum(), 2), "wr": jround((g["pnl"] > 0).mean() * 100, 1)}

# entry DOW / hour (resolved tz -> bar utc)
matched = legs[legs["matched"]]
dow_names = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
entry_dow = matched["utc_dow"].map(dow_names).value_counts().to_dict()
entry_hour_utc = matched["utc_hour"].value_counts().sort_index().to_dict()

stats["trades"] = {
    "n_legs": int(len(legs)),
    "n_base": int(len(base)),
    "n_pyramid_add": int(len(add)),
    "tz_resolution": {"et_match": f"{et_hits}/{tot}", "utc_match": f"{utc_hits}/{tot}", "used": tz_used},
    "bar_match_rate": f"{int(matched.shape[0])}/{len(legs)}",
    "net_usd": jround(net, 2),
    "net_pct_on_200k": jround(net / ACCOUNT * 100, 2),
    "final_cum_pnl_in_file": jround(legs["cum_pnl"].iloc[-1], 2),
    "wr_legs_pct": jround((legs["pnl"] > 0).mean() * 100, 2),
    "pf_legs": jround(pf, 3),
    "gross_win": jround(gw, 2),
    "gross_loss": jround(gl, 2),
    "avg_win": jround(wins["pnl"].mean(), 2),
    "avg_loss": jround(losses["pnl"].mean(), 2),
    "max_dd_pct_trade_close": jround(maxdd_pct, 2),
    "max_dd_usd": jround(maxdd_usd, 2),
    "rf": jround(net / abs(maxdd_usd), 2) if maxdd_usd else None,
    "r1_dollars": jround(r1, 2),
    "r1_basis": r1_basis,
    "cohort_warning": bool(cohort_warning),
    "n_fullstops": int(n_fs),
    "pyramid_pnl_share": jround(pyr_share, 4),
    "exit_type_breakdown": exit_break,
    "entry_dow_utc": entry_dow,
    "entry_hour_utc": {int(k): int(v) for k, v in entry_hour_utc.items()},
    "base_wr_pct": jround((base["pnl"] > 0).mean() * 100, 1),
    "base_net": jround(base["pnl"].sum(), 2),
    "add_wr_pct": jround((add["pnl"] > 0).mean() * 100, 1),
    "add_net": jround(add["pnl"].sum(), 2),
}

# trades per quarter + win/PF by quarter
legs["q"] = legs["exit_dt"].dt.to_period("Q").astype(str)
tq = []
for q, g in legs.groupby("q"):
    glw, gll = g[g["pnl"] > 0]["pnl"].sum(), g[g["pnl"] <= 0]["pnl"].sum()
    tq.append({
        "quarter": q, "n_legs": int(len(g)), "net": jround(g["pnl"].sum(), 2),
        "wr_pct": jround((g["pnl"] > 0).mean() * 100, 1),
        "pf": jround(glw / abs(gll), 2) if gll != 0 else None,
    })
stats["trades_by_quarter"] = tq

# ── JUXTAPOSITION: capture / opportunity ──
# eligible Mon/Tue session-days in bars vs days a base trade fired
base_matched = base[base["matched"]]
traded_dates = set(pd.to_datetime(base_matched["bar_utc"]).dt.date)
eligible_dates = set(bars.loc[bars["eligible_bar"], "utc_date"])
stats["juxtaposition"] = {
    "eligible_mon_tue_session_days": len(eligible_dates),
    "days_with_a_base_trade": len(traded_dates & eligible_dates),
    "signal_density_pct": jround(len(traded_dates & eligible_dates) / max(1, len(eligible_dates)) * 100, 1),
    "base_entries_in_session_13_17utc": int(base_matched["utc_hour"].isin([13, 14, 15, 16]).sum()),
    "base_entries_on_mon_tue": int(base_matched["utc_dow"].isin([0, 1]).sum()),
    "atr_ratio_at_base_entry_median": jround(base_matched["atr_ratio"].median(), 3),
    "frac_base_entries_atr_expanded": jround((base_matched["atr_ratio"] > 1.28).mean(), 3),
    "mean_ret_20bar_before_base_entry_pct": jround(base_matched["ret_20bar_pct"].mean(), 2),
}

# win/PF of trades bucketed by index regime (trailing 20-bar return sign at entry) -- SURFACE only
b = base_matched.copy()
b["regime"] = np.where(b["ret_20bar_pct"] >= 0, "up_20bar", "down_20bar")
reg = {}
for rname, g in b.groupby("regime"):
    glw, gll = g[g["pnl"] > 0]["pnl"].sum(), g[g["pnl"] <= 0]["pnl"].sum()
    reg[rname] = {"n": int(len(g)), "net": jround(g["pnl"].sum(), 2),
                  "wr_pct": jround((g["pnl"] > 0).mean() * 100, 1),
                  "pf": jround(glw / abs(gll), 2) if gll != 0 else None}
stats["juxtaposition"]["base_outcome_by_index_regime"] = reg

with open(OUT / "nas100_identify_stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print(json.dumps(stats, indent=2))
print("\n=== wrote:", OUT)
