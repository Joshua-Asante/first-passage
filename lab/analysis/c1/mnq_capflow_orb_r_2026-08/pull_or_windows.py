#!/usr/bin/env python3
"""Q-CAPFLOW-1 — estimate / pull TBBO for S1 gap (pre-OFCHAN).

Prefer OFCHAN day-file reuse (2026-02-06+). This helper covers trigger session
days missing from that cache, inside parent S1 (2025-08-06->2026-08-04).

Protocol (databento-data skill): estimate before every pull; refuse > .
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "lab"))
from databento_fetch import db_fetch  # noqa: E402

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "mnq_orb_flow_substrate_2026-08-05"
EVENTS = PARENT / "events.parquet"
CACHE_OFCHAN = (
    Path.home()
    / ".databento_cache"
    / "q_ofchan_1_exploration_tbbo"
    / "GLBX-20260807-EHX5KUSF7K"
)
CACHE_GAP = Path.home() / ".databento_cache" / "q_capflow_1_or_tbbo_gap"
GAP_BLOB = CACHE_GAP / "gap_20250806_20260206.tbbo.dbn"
OFCHAN_START = date(2026, 2, 6)
S1_START = date(2025, 8, 6)
BUDGET = 50.0
SYMBOL = "MNQ.v.0"
STYPE = "continuous"
SCHEMA = "tbbo"
GAP_START = date(2025, 8, 6)
GAP_END_EXCL = date(2026, 2, 6)


def missing_trigger_days() -> list[date]:
    if not EVENTS.exists():
        raise SystemExit(f"ABORT: events missing at {EVENTS}")
    ev = pd.read_parquet(EVENTS)
    trig = ev[ev["kind"] == "trigger"]
    days = sorted({pd.Timestamp(d).date() for d in trig["date"]})
    if GAP_BLOB.exists():
        return []
    missing = []
    for d in days:
        name = f"glbx-mdp3-{d.strftime('%Y%m%d')}.tbbo.dbn.zst"
        if (CACHE_OFCHAN / name).exists() or (CACHE_GAP / name).exists():
            continue
        if (CACHE_OFCHAN / name.replace(".zst", "")).exists():
            continue
        if d < GAP_END_EXCL:
            missing.append(d)
    return missing


def estimate_range(d0: date, d1_excl: date) -> dict:
    client = db_fetch._client()
    start = pd.Timestamp(d0, tz="America/New_York").tz_convert("UTC")
    end = pd.Timestamp(d1_excl, tz="America/New_York").tz_convert("UTC")
    cost = float(
        client.metadata.get_cost(
            dataset=db_fetch.DATASET,
            symbols=[SYMBOL],
            stype_in=STYPE,
            schema=SCHEMA,
            start=start.isoformat(),
            end=end.isoformat(),
        )
    )
    return {
        "start": str(d0),
        "end_excl": str(d1_excl),
        "schema": SCHEMA,
        "symbol": SYMBOL,
        "estimated_usd": cost,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--estimate-only", action="store_true")
    ap.add_argument("--pull", action="store_true")
    ap.add_argument("--max-cost", type=float, default=BUDGET)
    args = ap.parse_args()
    if not args.pull:
        args.estimate_only = True

    missing = missing_trigger_days()
    print(f"[gap] missing trigger session days: {len(missing)}")
    if not missing and GAP_BLOB.exists():
        out = dict(missing_days=0, estimated_usd=0.0, action="reuse_gap_blob", path=str(GAP_BLOB))
        (HERE / "ESTIMATE_gap.json").write_text(json.dumps(out, indent=2))
        print("[gap] gap blob already present — no pull")
        return 0
    if not missing:
        out = dict(missing_days=0, estimated_usd=0.0, action="none")
        (HERE / "ESTIMATE_gap.json").write_text(json.dumps(out, indent=2))
        print("[gap] nothing to pull")
        return 0

    est = estimate_range(GAP_START, GAP_END_EXCL)
    est["missing_days"] = len(missing)
    est["missing_first"] = str(missing[0])
    est["missing_last"] = str(missing[-1])
    est["budget_usd"] = args.max_cost
    est["within_budget"] = est["estimated_usd"] <= args.max_cost
    est["gap_blob"] = str(GAP_BLOB)
    (HERE / "ESTIMATE_gap.json").write_text(json.dumps(est, indent=2))
    print(json.dumps(est, indent=2))

    if args.estimate_only and not args.pull:
        print("[estimate-only] no pull; re-run with --pull if within budget + Cap-spend GO")
        return 0

    if not est["within_budget"]:
        raise SystemExit(
            f"ABORT: estimate  > budget "
        )

    CACHE_GAP.mkdir(parents=True, exist_ok=True)
    client = db_fetch._client()
    start = pd.Timestamp(GAP_START, tz="America/New_York").tz_convert("UTC")
    end = pd.Timestamp(GAP_END_EXCL, tz="America/New_York").tz_convert("UTC")
    print(f"[pull] {GAP_START} -> {GAP_END_EXCL} (excl) est=")
    store = client.timeseries.get_range(
        dataset=db_fetch.DATASET,
        symbols=[SYMBOL],
        stype_in=STYPE,
        schema=SCHEMA,
        start=start.isoformat(),
        end=end.isoformat(),
    )
    tmp = GAP_BLOB.with_suffix(".dbn.tmp")
    store.to_file(tmp)
    tmp.replace(GAP_BLOB)
    # Split into OFCHAN-shaped day files so the runner can multiprocess without
    # re-decoding the multi-month blob per day.
    print("[split] decoding gap blob -> per-day tbbo files …")
    import databento as db
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
    df = db.DBNStore.from_file(GAP_BLOB).to_df()
    ts = pd.to_datetime(df["ts_event"], utc=True).dt.tz_convert(ET)
    n_days = 0
    for d, g in df.groupby(ts.dt.date):
        out_day = CACHE_GAP / f"glbx-mdp3-{d.strftime('%Y%m%d')}.tbbo.dbn"
        # Re-pull single day would bill again; instead write a parquet sidecar for runner.
        # Runner accepts parquet day caches under CACHE_GAP as well.
        pq = CACHE_GAP / f"glbx-mdp3-{d.strftime('%Y%m%d')}.tbbo.parquet"
        g.to_parquet(pq)
        n_days += 1
    est["action"] = "pulled_and_split"
    est["pulled_usd_est"] = est["estimated_usd"]
    est["split_day_parquets"] = n_days
    (HERE / "ESTIMATE_gap.json").write_text(json.dumps(est, indent=2))
    print(f"[pull] wrote {GAP_BLOB} + {n_days} day parquets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
