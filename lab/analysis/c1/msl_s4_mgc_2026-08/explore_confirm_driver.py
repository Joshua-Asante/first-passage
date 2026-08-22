"""MSL-S4 Explore-confirm -- pull-and-run driver.

Written under EXPLORE_GO.md (ISSUED 2026-08-21), per its own Promote rule step 3
("Write the driver script ... not yet written; this token authorizes writing
it"). Extends _cheap_falsifier_expiry_oi_strike_convergence_2026-08-21.py's
proven cycle-discovery / per-cycle OI pull pattern to:
  - both weekly (OG1/OG2/OG3/OG4 roots) and monthly (OG root) Gold-option cycles
  - the frozen IS window only (2024-01-01 .. 2025-03-31) -- CONFIRM
    (2025-04-01 .. 2025-09-29) is NEVER queried by this script. There is no
    code path here that can read it; the CONFIRM dates are not even
    constants in this file.

All statistics (IAAFT significance test, delete/flip, verdict gate) are
computed by explore_confirm_lib.py -- this file only pulls data and shapes it
into that library's Cycle/array inputs. See EXPLORE_GO.md for the frozen
geometry and the pilot-calibration requirement this driver's __main__
executes in order.
"""
import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
import databento as db

from research_utils.camp_import import load_camp_sibling

lib = load_camp_sibling("explore_confirm_lib", __file__)

client = db.Historical(os.environ["DATABENTO_API_KEY"])

HERE = Path(__file__).parent

# IS window -- mirrors explore_confirm_lib.IS_START/IS_END exactly (imported,
# not retyped, so a future edit to the library can't silently desync this
# driver from the frozen partition).
IS_START = str(lib.IS_START)[:10]
IS_END = str(lib.IS_END)[:10]
# GC price history pulled with lookback padding so the DELETE test's 60-session
# trailing median has 60 real sessions behind even the FIRST IS cycle's arm open.
PRICE_PULL_START = str(np.datetime64(IS_START) - np.timedelta64(130, "D"))[:10]

WEEKLY_ROOTS = ["OG1", "OG2", "OG3", "OG4"]
MONTHLY_ROOT = "OG"


def _pull(schema, symbols, stype, start, end, retries=4):
    for attempt in range(retries):
        try:
            data = client.timeseries.get_range(
                dataset="GLBX.MDP3", symbols=symbols, schema=schema,
                stype_in=stype, start=start, end=end,
            )
            return data.to_df()
        except db.common.error.BentoServerError as exc:
            print(f"    retry {attempt} ({schema}, {len(symbols) if isinstance(symbols, list) else 1} syms) after: {exc}")
            time.sleep(4)
    raise RuntimeError(f"failed {schema} pull {symbols} {start}..{end}")


def _bday_offset(d, n):
    return str(np.busday_offset(np.datetime64(d, "D"), n, roll="backward"))


# ============================================================================
# Phase 1 -- discovery (IS window only; CONFIRM is structurally unreachable --
# no function in this file accepts a date argument spanning past IS_END)
# ============================================================================

def discover_weekly_cycles():
    """One bulk definition pull across the full IS window for the four weekly
    roots (OG1..OG4). Cheap (~0.36GB measured via `estimate`, $0). Because each
    day's snapshot only shows ONE active expiration per root (rolling weekly
    labels), the full daily stream is the correct + simplest way to enumerate
    every distinct weekly cycle without guessing a sampling cadence.

    Returns a DataFrame of one row per (expiration, ts_recv date) with columns
    needed to pick the exact-strike snapshot nearest each cycle's own
    arm_start later -- NOT deduplicated to one row per cycle yet.
    """
    cache_path = HERE / "_explore_confirm_2026-08-21_weekly_defs_cache.parquet"
    if cache_path.exists():
        print(f"[discover] weekly OG1-4 definitions: local cache hit ({cache_path})")
        return pd.read_parquet(cache_path)
    print(f"[discover] weekly OG1-4 definitions {IS_START}..{IS_END} (one bulk pull)")
    df = _pull("definition", [r + ".OPT" for r in WEEKLY_ROOTS], "parent", IS_START, IS_END)
    tok0 = df["raw_symbol"].str.split(" ").str[0]
    root = tok0.str[:-2]
    mask = root.isin(WEEKLY_ROOTS)
    # .values (not index-aligned assignment): the definition schema's ts_recv
    # index has many duplicate timestamps (one per strike per day), so a
    # filtered-vs-unfiltered Series reindex raises "duplicate labels."
    df = df[mask].copy()
    df["contract_code"] = tok0[mask].values
    # ts_recv is the DBNStore.to_df() index, not a column.
    df["snap_date"] = df.index.date.astype(str)
    df["exp_date"] = df["expiration"].dt.date.astype(str)
    print(f"[discover] weekly: {len(df):,} definition rows, "
          f"{df['exp_date'].nunique()} distinct expirations in-window")
    keep_cols = ["contract_code", "snap_date", "exp_date", "instrument_class",
                 "strike_price", "instrument_id", "expiration"]
    df[keep_cols].reset_index(drop=True).to_parquet(cache_path)
    return df


def discover_monthly_cycles():
    """One small single-day definition snapshot near IS_START. Monthly Gold
    options list many months/years ahead (confirmed empirically: a single
    2026-08-20 snapshot showed contracts through 2032), so one snapshot at or
    just after IS_START reveals every monthly cycle whose expiry falls in or
    after the IS window -- none of them can have already expired relative to
    IS_START by construction of the window."""
    print(f"[discover] monthly OG definitions, single snapshot at {IS_START}")
    end = str(np.datetime64(IS_START) + np.timedelta64(1, "D"))[:10]
    df = _pull("definition", ["OG.OPT"], "parent", IS_START, end)
    tok0 = df["raw_symbol"].str.split(" ").str[0]
    root = tok0.str[:-2]
    mask = root == MONTHLY_ROOT
    df = df[mask].copy()
    df["contract_code"] = tok0[mask].values
    cycles = (df.groupby("contract_code")["expiration"].first()
                .reset_index().sort_values("expiration"))
    cycles["exp_date"] = cycles["expiration"].dt.date.astype(str)
    in_window = cycles[(cycles["exp_date"] >= IS_START) & (cycles["exp_date"] <= IS_END)]
    print(f"[discover] monthly: {len(cycles)} contracts visible, "
          f"{len(in_window)} with expiry inside IS window")
    return in_window[["contract_code", "exp_date"]].to_dict("records")


# ============================================================================
# Phase 2 -- per-cycle strikes + open interest
# ============================================================================

def weekly_cycle_strikes_and_oi(weekly_defs, exp_date):
    """For one weekly expiration date, pick the definition snapshot on the
    trading day at/before arm_start (3 sessions before expiry) from the
    already-pulled bulk weekly definitions (no extra definition pull needed),
    then a small instrument_id-scoped statistics pull for OI-by-strike."""
    arm_start = _bday_offset(exp_date, -3)
    day_rows = weekly_defs[weekly_defs["exp_date"] == exp_date]
    day_rows = day_rows[day_rows["snap_date"] <= arm_start]
    if day_rows.empty:
        return None
    snap_date = day_rows["snap_date"].max()
    this = day_rows[day_rows["snap_date"] == snap_date]
    this = this[this["instrument_class"].isin(["C", "P"])]
    this = this[this["strike_price"].notna()]
    if this.empty:
        return None
    return _score_strikes(this, arm_start, snap_date)


def monthly_cycle_strikes_and_oi(contract_code, exp_date):
    """Per-cycle re-pull (proven cheap-falsifier pattern): a fresh definition
    snapshot AT the cycle's own arm_start date, scoped to this one contract
    code, so strikes reflect what was actually listed at scoring time (not
    assumed static from the IS_START discovery snapshot)."""
    arm_start = _bday_offset(exp_date, -3)
    d_end = str(pd.Timestamp(arm_start) + pd.Timedelta(days=1))[:10]
    defs = _pull("definition", ["OG.OPT"], "parent", arm_start, d_end)
    tok0 = defs["raw_symbol"].str.split(" ").str[0]
    this = defs[tok0 == contract_code].copy()
    this = this[this["instrument_class"].isin(["C", "P"])]
    this = this[this["strike_price"].notna()]
    if this.empty:
        return None
    return _score_strikes(this, arm_start, arm_start)


def _score_strikes(this, arm_start, stats_day):
    dedup = this.drop_duplicates("instrument_id").copy()
    dedup["instrument_id_str"] = dedup["instrument_id"].astype(str)
    inst_ids = dedup["instrument_id_str"].tolist()
    strike_map = dedup.set_index("instrument_id_str")["strike_price"]
    d_end = str(pd.Timestamp(stats_day) + pd.Timedelta(days=1))[:10]
    stats = _pull("statistics", inst_ids, "instrument_id", stats_day, d_end)
    if "stat_type" not in stats.columns or stats.empty:
        return None
    oi = stats[stats["stat_type"] == 9].copy()  # 9 = OpenInterest
    if oi.empty:
        return None
    oi["strike"] = oi["instrument_id"].astype(str).map(strike_map)
    oi_by_strike = oi.groupby("strike")["quantity"].sum().sort_values(ascending=False)
    if oi_by_strike.empty:
        return None
    return dict(
        arm_start=arm_start,
        strike_star=float(oi_by_strike.index[0]),
        oi_top=float(oi_by_strike.iloc[0]),
        oi_runner_up=float(oi_by_strike.iloc[1]) if len(oi_by_strike) > 1 else None,
        n_strikes=int(len(oi_by_strike)),
    )


# ============================================================================
# Phase 3 -- GC price series (real returns for IAAFT + real prices for scoring)
# ============================================================================

def pull_gc_price_series():
    print(f"[price] GC.c.0 daily {PRICE_PULL_START}..{IS_END}")
    px = _pull("ohlcv-1d", ["GC.c.0"], "continuous", PRICE_PULL_START, IS_END).sort_index()
    px["date"] = px.index.date.astype(str)
    px = px.reset_index(drop=True)
    print(f"[price] {len(px)} daily bars")
    return px


def date_to_idx(px, date_str):
    """Index of the last available trading day <= date_str."""
    avail = px[px["date"] <= date_str]
    if avail.empty:
        return None
    return int(avail.index[-1])


if __name__ == "__main__":
    OUT = HERE / "_explore_confirm_2026-08-21_RAW.json"
    print("=== Phase 1: discovery ===")
    weekly_defs = discover_weekly_cycles()
    weekly_exp_dates = sorted(
        d for d in weekly_defs["exp_date"].unique()
        if IS_START <= d <= IS_END
    )
    monthly_cycles = discover_monthly_cycles()
    print(f"[discover] {len(weekly_exp_dates)} weekly + {len(monthly_cycles)} monthly "
          f"= {len(weekly_exp_dates) + len(monthly_cycles)} candidate IS cycles")

    print("=== Phase 2: per-cycle strikes + OI ===")
    scored = []
    for exp_date in weekly_exp_dates:
        r = weekly_cycle_strikes_and_oi(weekly_defs, exp_date)
        if r is not None:
            r.update(kind="weekly", exp_date=exp_date)
            scored.append(r)
            print(f"  weekly {exp_date}: strike*={r['strike_star']} "
                  f"oi={r['oi_top']:.0f} n_strikes={r['n_strikes']}")
        else:
            print(f"  weekly {exp_date}: SKIP (no OI data)")
    for c in monthly_cycles:
        r = monthly_cycle_strikes_and_oi(c["contract_code"], c["exp_date"])
        if r is not None:
            r.update(kind="monthly", exp_date=c["exp_date"], contract_code=c["contract_code"])
            scored.append(r)
            print(f"  monthly {c['contract_code']} {c['exp_date']}: strike*={r['strike_star']} "
                  f"oi={r['oi_top']:.0f} n_strikes={r['n_strikes']}")
        else:
            print(f"  monthly {c['contract_code']} {c['exp_date']}: SKIP (no OI data)")

    print(f"[phase2] {len(scored)} cycles scored (of {len(weekly_exp_dates) + len(monthly_cycles)} candidates)")

    print("=== Phase 3: GC price series ===")
    px = pull_gc_price_series()

    with open(OUT, "w") as f:
        json.dump(dict(
            scored_cycles=scored,
            price_dates=px["date"].tolist(),
            price_close=px["close"].tolist(),
        ), f, indent=2)
    print(f"[done] wrote {OUT}")
