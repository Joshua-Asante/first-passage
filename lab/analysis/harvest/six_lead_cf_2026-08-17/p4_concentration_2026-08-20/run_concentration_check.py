"""P4 (L2) dealer-gamma — NQ.OPT trade-volume concentration by moneyness/tenor.

Answers the question P4_DRYRUN.md §3 left open: does NQ.OPT trade volume
concentrate in the near-the-money, near-dated slice a real delta-hedging-flow
proxy would actually use, or is the complex-wide thinness (367x fewer trades
than NQ.FUT) uniform across the chain?

Inputs (pulled this session, campaign P4-L2-GAMMA-conc, 2026-05-20->2026-08-20,
$0.00 billed):
  definition.parquet    - NQ.OPT instrument specs (strike, expiration, class)
  trades.parquet        - NQ.OPT trade prints (instrument_id, price, size, side)
  nq_fut_ohlcv1d.parquet - NQ.FUT daily bars, all expiries (for a front-month
                           underlying close to compute moneyness against)
"""
import json
import pandas as pd
import numpy as np

d = pd.read_parquet("definition.parquet")
t = pd.read_parquet("trades.parquet")
u = pd.read_parquet("nq_fut_ohlcv1d.parquet")

# --- front-month underlying daily close: highest-volume NQ.FUT contract per day ---
u = u.reset_index()
u["date"] = u["ts_event"].dt.date
front = u.sort_values("volume", ascending=False).drop_duplicates("date")[["date", "close", "symbol"]]
front = front.rename(columns={"close": "underlying_close", "symbol": "front_symbol"})

# --- definition: one row per instrument_id (dedupe on the latest record if revised) ---
d = d.reset_index()
def_cols = ["instrument_id", "strike_price", "expiration", "instrument_class", "raw_symbol"]
d_small = d[def_cols].drop_duplicates("instrument_id", keep="last")

# --- trades: join to definition, join to underlying close by trade date ---
t = t.reset_index()
t["date"] = t["ts_recv"].dt.date if "ts_recv" in t.columns else t["ts_event"].dt.date

merged = t.merge(d_small, on="instrument_id", how="left")
n_before = len(merged)
merged = merged.merge(front, on="date", how="left")
n_unmatched_def = merged["strike_price"].isna().sum()
n_unmatched_underlying = merged["underlying_close"].isna().sum()

merged = merged.dropna(subset=["strike_price", "expiration", "underlying_close"])

# --- moneyness: absolute distance from ATM, in percent of underlying ---
merged["moneyness_pct"] = (merged["strike_price"] - merged["underlying_close"]).abs() / merged["underlying_close"] * 100.0

# --- tenor: calendar days from trade date to expiration ---
merged["trade_date_ts"] = pd.to_datetime(merged["date"])
merged["expiration_date"] = pd.to_datetime(merged["expiration"]).dt.tz_localize(None)
merged["tenor_days"] = (merged["expiration_date"] - merged["trade_date_ts"]).dt.days

moneyness_bins = [-0.001, 2, 5, 10, 20, 1e9]
moneyness_labels = ["0-2%", "2-5%", "5-10%", "10-20%", ">20%"]
tenor_bins = [-1, 7, 30, 90, 1e9]
tenor_labels = ["0-7d", "8-30d", "31-90d", ">90d"]

merged["moneyness_bucket"] = pd.cut(merged["moneyness_pct"], bins=moneyness_bins, labels=moneyness_labels)
merged["tenor_bucket"] = pd.cut(merged["tenor_days"], bins=tenor_bins, labels=tenor_labels)

total_trades = len(merged)
total_size = merged["size"].sum()

by_moneyness = merged.groupby("moneyness_bucket", observed=True).agg(
    trades=("size", "count"), contracts=("size", "sum")
)
by_moneyness["trade_pct"] = (by_moneyness["trades"] / total_trades * 100).round(2)
by_moneyness["contract_pct"] = (by_moneyness["contracts"] / total_size * 100).round(2)

by_tenor = merged.groupby("tenor_bucket", observed=True).agg(
    trades=("size", "count"), contracts=("size", "sum")
)
by_tenor["trade_pct"] = (by_tenor["trades"] / total_trades * 100).round(2)
by_tenor["contract_pct"] = (by_tenor["contracts"] / total_size * 100).round(2)

cross = merged.groupby(["moneyness_bucket", "tenor_bucket"], observed=True).size().unstack(fill_value=0)
cross_pct = (cross / total_trades * 100).round(2)

# the "near-the-money, near-dated" slice the route memo's construction would actually use
near = merged[(merged["moneyness_pct"] <= 5) & (merged["tenor_days"] <= 30)]
near_trades = len(near)
near_pct_of_total = round(near_trades / total_trades * 100, 2)

# recompute trades/session for the near slice vs the complex-wide figure, same units as P4_DRYRUN.md §3
n_sessions = merged["date"].nunique()
near_per_session = round(near_trades / n_sessions, 1) if n_sessions else float("nan")
complex_per_session = round(total_trades / n_sessions, 1) if n_sessions else float("nan")

result = {
    "window": "2026-05-20 to 2026-08-20",
    "n_sessions": int(n_sessions),
    "trades_pulled_total": int(len(t)),
    "trades_matched_to_definition_and_underlying": int(total_trades),
    "trades_dropped_unmatched_definition": int(n_unmatched_def),
    "trades_dropped_unmatched_underlying": int(n_unmatched_underlying),
    "total_contracts_traded": int(total_size),
    "by_moneyness": by_moneyness.to_dict(orient="index"),
    "by_tenor": by_tenor.to_dict(orient="index"),
    "cross_moneyness_x_tenor_pct_of_trades": cross_pct.to_dict(orient="index"),
    "near_the_money_near_dated_slice": {
        "definition": "moneyness<=5% AND tenor<=30d",
        "trade_count": int(near_trades),
        "pct_of_all_matched_trades": near_pct_of_total,
        "trades_per_session_this_slice": near_per_session,
        "trades_per_session_complex_wide": complex_per_session,
        "trades_per_session_NQ_FUT_from_dryrun": 361389.5,
    },
}

with open("concentration_results.json", "w") as f:
    json.dump(result, f, indent=2, default=str)

print(json.dumps(result, indent=2, default=str))
