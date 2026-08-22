"""Cheap falsifier -- MSL-S4 `expiry-oi-strike-convergence` (MGC).

STAGE1.md Step 4 was disclosed as NOT AVAILABLE (the sourcing session's cloud
container had no DATABENTO_API_KEY). This runner fills that gap from a local
environment that has the key, using only $0 GLBX.MDP3 schemas (definition,
statistics, ohlcv-1d).

Deliberately generous/informal, NOT the pre-registered Explore-confirm
(PREREG_G0.md Sec4): no IS/CONFIRM partition reserved, business-day arithmetic
(no CME holiday calendar), monthly OG options only (weeklies excluded), no
significance test. See the paired _LOG.md for the frozen check geometry,
result, and disposition.

Two phases, run in sequence:
  1. find_cycles()   -- discover N completed OG (Gold monthly options) expiry
                        cycles directly from Databento definition snapshots
                        (free schema, exact real expiry timestamps).
  2. run_falsifier() -- for each cycle: highest-OI strike ~3 sessions before
                        expiry (statistics schema, stype_in=instrument_id --
                        narrow, cheap), then check whether GC (parent, proxy
                        for MGC -- see PREREG_G0.md Sec6) closes converge
                        toward that strike more in the 3-session pre-expiry
                        arm window than in a length-matched non-expiry control
                        window 10 sessions earlier.
"""
import os
import time
import numpy as np
import pandas as pd
import databento as db

client = db.Historical(os.environ["DATABENTO_API_KEY"])

ANCHOR_DATES = [
    "2026-08-20", "2026-07-21", "2026-06-19", "2026-05-20",
    "2026-04-20", "2026-03-20", "2026-02-18", "2026-01-19",
]


def _pull(schema, symbols, stype, start, end, retries=3):
    for attempt in range(retries):
        try:
            data = client.timeseries.get_range(
                dataset="GLBX.MDP3", symbols=symbols, schema=schema,
                stype_in=stype, start=start, end=end,
            )
            return data.to_df()
        except db.common.error.BentoServerError as exc:
            print(f"    retry {attempt} ({schema}) after: {exc}")
            time.sleep(3)
    raise RuntimeError(f"failed {schema} pull {symbols} {start}..{end}")


def find_cycles(anchor_dates=ANCHOR_DATES):
    """One-day OG.OPT definition snapshots ($0, free schema) -> the currently
    listed near-month standard monthly contract + its real expiration."""
    rows = []
    for day in anchor_dates:
        end = (pd.Timestamp(day) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        df = _pull("definition", ["OG.OPT"], "parent", day, end)
        tok0 = df["raw_symbol"].str.split(" ").str[0]
        root = tok0.str[:-2]
        og = df[root == "OG"].copy()
        og["contract_code"] = tok0[root == "OG"]
        near_exp = og["expiration"].min()
        near = og[og["expiration"] == near_exp]
        rows.append(dict(
            anchor=day,
            contract_code=near["contract_code"].iloc[0],
            expiration=str(near_exp),
        ))
    return pd.DataFrame(rows)


def _bday_offset(d, n):
    return str(np.busday_offset(np.datetime64(d, "D"), n, roll="backward"))


def run_falsifier(cycles):
    """cycles: list of (contract_code, expiry_date_str), completed (past) only."""
    results = []
    for contract_code, expiry in cycles:
        arm_start = _bday_offset(expiry, -3)
        arm_end = _bday_offset(expiry, 0)
        ctrl_start = _bday_offset(expiry, -13)
        ctrl_end = _bday_offset(expiry, -10)

        d_end = str(pd.Timestamp(arm_start) + pd.Timedelta(days=1))[:10]
        defs = _pull("definition", ["OG.OPT"], "parent", arm_start, d_end)
        tok0 = defs["raw_symbol"].str.split(" ").str[0]
        this = defs[tok0 == contract_code].copy()
        this = this[(this["strike_price"] >= 1500) & (this["strike_price"] <= 4500)]
        this = this[this["instrument_class"].isin(["C", "P"])]
        if this.empty:
            continue
        inst_ids = this["instrument_id"].astype(str).unique().tolist()
        strike_map = this.set_index(this["instrument_id"].astype(str))["strike_price"]

        stats = _pull("statistics", inst_ids, "instrument_id", arm_start, d_end)
        oi = stats[stats["stat_type"] == 9].copy()  # 9 = OpenInterest
        if oi.empty:
            continue
        oi["strike"] = oi["instrument_id"].astype(str).map(strike_map)
        oi_by_strike = oi.groupby("strike")["quantity"].sum().sort_values(ascending=False)
        strike_star = oi_by_strike.index[0]

        px_end = str(pd.Timestamp(arm_end) + pd.Timedelta(days=1))[:10]
        px = _pull("ohlcv-1d", ["GC.c.0"], "continuous", ctrl_start, px_end).sort_index()
        px.index = px.index.date.astype(str)

        def close_on_or_before(day):
            avail = px[px.index <= day]
            return None if avail.empty else avail["close"].iloc[-1]

        c = {k: close_on_or_before(v) for k, v in
             dict(arm_start=arm_start, arm_end=arm_end,
                  ctrl_start=ctrl_start, ctrl_end=ctrl_end).items()}
        if None in c.values():
            continue

        results.append(dict(
            contract=contract_code, expiry=expiry, strike_star=float(strike_star),
            arm_disp_start=abs(c["arm_start"] - strike_star),
            arm_disp_end=abs(c["arm_end"] - strike_star),
            ctrl_disp_start=abs(c["ctrl_start"] - strike_star),
            ctrl_disp_end=abs(c["ctrl_end"] - strike_star),
        ))
    out = pd.DataFrame(results)
    out["arm_converged"] = out["arm_disp_end"] < out["arm_disp_start"]
    out["ctrl_converged"] = out["ctrl_disp_end"] < out["ctrl_disp_start"]
    return out


if __name__ == "__main__":
    cyc = find_cycles()
    print(cyc)
    # exclude the still-open cycle (expiration in the future as of the run date)
    completed = [(r.contract_code, r.expiration[:10]) for r in cyc.itertuples()
                 if r.expiration[:10] < "2026-08-21"]
    res = run_falsifier(completed)
    print(res)
    print("arm converge rate: ", res["arm_converged"].mean(), res["arm_converged"].sum(), "/", len(res))
    print("ctrl converge rate:", res["ctrl_converged"].mean(), res["ctrl_converged"].sum(), "/", len(res))
