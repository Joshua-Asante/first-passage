#!/usr/bin/env python3
"""Estimate Databento cost for CapFLOW S1 gap (pre-OFCHAN day files) before any pull.

OFCHAN exploration TBBO day-files start 2026-02-06. CapFLOW event window is
2025-08-06 → 2026-08-04. This script reports:
  - n_triggers total / covered by OFCHAN days / in gap
  - billable estimate for gap TBBO (MNQ.v.0) if DATABENTO_API_KEY present
  - BLOCKED recommendation if estimate > $50 or key missing for gap

Does not pull.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "mnq_orb_flow_substrate_2026-08-05"
OFCHAN_TBBO = Path.home() / ".databento_cache" / "q_ofchan_1_exploration_tbbo"
BUDGET = 50.0
OFCHAN_START = pd.Timestamp("2026-02-06").date()


def ofchan_days() -> set:
    days = set()
    if not OFCHAN_TBBO.exists():
        return days
    for p in OFCHAN_TBBO.rglob("*.tbbo.dbn.zst"):
        # glbx-mdp3-YYYYMMDD.tbbo.dbn.zst
        name = p.name
        if "glbx-mdp3-" in name:
            ymd = name.split("glbx-mdp3-")[1][:8]
            try:
                days.add(pd.Timestamp(ymd).date())
            except Exception:
                pass
    return days


def main() -> int:
    ev_path = PARENT / "events.parquet"
    if not ev_path.exists():
        print("BLOCKED: parent events.parquet missing")
        return 2
    ev = pd.read_parquet(ev_path)
    trig = ev[ev["kind"] == "trigger"].copy()
    trig["d"] = pd.to_datetime(trig["date"]).dt.date
    n = len(trig)
    have = ofchan_days()
    covered = trig[trig["d"].isin(have)]
    gap = trig[~trig["d"].isin(have)]
    gap_dates = sorted(gap["d"].unique())
    out = {
        "n_triggers": int(n),
        "ofchan_days_on_disk": int(len(have)),
        "triggers_ofchan_overlap": int(len(covered)),
        "triggers_in_gap": int(len(gap)),
        "gap_unique_dates": int(len(gap_dates)),
        "gap_first": str(gap_dates[0]) if gap_dates else None,
        "gap_last": str(gap_dates[-1]) if gap_dates else None,
        "budget_usd": BUDGET,
        "estimate_usd": None,
        "status": None,
    }
    if not gap_dates:
        out["status"] = "READY_REUSE_ONLY"
        out["estimate_usd"] = 0.0
        print(json.dumps(out, indent=2))
        return 0

    key = os.environ.get("DATABENTO_API_KEY")
    if not key:
        out["status"] = "BLOCKED_NO_KEY_FOR_GAP_ESTIMATE"
        out["note"] = (
            f"Gap {gap_dates[0]}→{gap_dates[-1]} ({len(gap_dates)} sessions) needs "
            "tbbo estimate; DATABENTO_API_KEY unset. OFCHAN overlap alone is partial."
        )
        print(json.dumps(out, indent=2))
        (HERE / "ESTIMATE.json").write_text(json.dumps(out, indent=2))
        return 1

    try:
        from databento import Historical

        client = Historical(key=key)
        start = str(gap_dates[0])
        # exclusive end = last gap day + 1
        end = str(pd.Timestamp(gap_dates[-1]) + pd.Timedelta(days=1))[:10]
        cost = float(
            client.metadata.get_cost(
                dataset="GLBX.MDP3",
                symbols="MNQ.v.0",
                schema="tbbo",
                start=start,
                end=end,
                stype_in="continuous",
            )
        )
        out["estimate_usd"] = cost
        out["estimate_window"] = [start, end]
        if cost > BUDGET:
            out["status"] = "BLOCKED_OVER_BUDGET"
        else:
            out["status"] = "ESTIMATE_OK_AWAITING_PULL_GO"
    except Exception as e:
        out["status"] = "BLOCKED_ESTIMATE_FAILED"
        out["error"] = str(e)

    print(json.dumps(out, indent=2))
    (HERE / "ESTIMATE.json").write_text(json.dumps(out, indent=2))
    return 0 if out["status"] in ("READY_REUSE_ONLY", "ESTIMATE_OK_AWAITING_PULL_GO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
