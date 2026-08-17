"""Cost-gated BATCH pull for MNQ-SIZEDIV-1 (DESIGN_FREEZE §2).

Batch (not streaming): the 12.7 GB confirm-year died streaming on the OFCHAN
precedent, and db_fetch's final to_df() cannot hold 265M rows. Phases, windows
and ceilings are FROZEN here — do not pass ad-hoc windows.

Usage: python pull_batch.py --phase confirm_year [--poll-seconds 30]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import databento as db
except ImportError:
    sys.exit("databento not installed (research venv required).")

DATASET = "GLBX.MDP3"
SYMBOL = "MNQ.v.0"
SCHEMA = "trades"
CACHE_ROOT = Path(os.environ.get("DATABENTO_CACHE", Path.home() / ".databento_cache")) / "mnq_sizediv_blind_2026-08"

# FROZEN with DESIGN_FREEZE.md — window edits require a fresh freeze.
PHASES = {
    "confirm_year": dict(start="2025-08-14", end="2026-08-14", max_cost=1.00),
    "train_sem": dict(start="2023-08-14", end="2024-02-14", max_cost=120.00),
    "train_full": dict(start="2024-02-14", end="2025-08-14", max_cost=400.00),
}


def _client() -> "db.Historical":
    key = os.environ.get("DATABENTO_API_KEY")
    if not key:
        sys.exit("DATABENTO_API_KEY is not set.")
    return db.Historical(key)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=sorted(PHASES))
    ap.add_argument("--poll-seconds", type=int, default=30)
    ap.add_argument("--timeout-minutes", type=int, default=180)
    args = ap.parse_args()

    spec = PHASES[args.phase]
    out_dir = CACHE_ROOT / args.phase
    out_dir.mkdir(parents=True, exist_ok=True)
    client = _client()

    kwargs = dict(dataset=DATASET, symbols=[SYMBOL], stype_in="continuous",
                  schema=SCHEMA, start=spec["start"], end=spec["end"])

    cost = float(client.metadata.get_cost(**kwargs))
    size = int(client.metadata.get_billable_size(**kwargs))
    print(f"[estimate] phase={args.phase} cost=${cost:,.4f} billable={size/1e9:.3f} GB", flush=True)
    if cost > spec["max_cost"]:
        sys.exit(f"ABORT: ${cost:,.4f} exceeds the FROZEN ceiling ${spec['max_cost']:,.2f} "
                 f"for phase {args.phase}. A ceiling change requires a fresh freeze + operator GO.")

    job = client.batch.submit_job(**kwargs, encoding="dbn", compression="zstd",
                                  split_duration="month")
    jid = job["id"] if isinstance(job, dict) else getattr(job, "id", None)
    if not jid:
        sys.exit(f"ABORT: no job id in submit response: {job!r}")
    print(f"[batch]    submitted job {jid}", flush=True)

    deadline = time.time() + args.timeout_minutes * 60
    state = None
    while time.time() < deadline:
        jobs = client.batch.list_jobs()
        mine = next((j for j in jobs if (j.get("id") if isinstance(j, dict) else getattr(j, "id", None)) == jid), None)
        state = (mine.get("state") if isinstance(mine, dict) else getattr(mine, "state", None)) if mine else None
        print(f"[batch]    {datetime.now(timezone.utc).isoformat(timespec='seconds')} state={state}", flush=True)
        if state == "done":
            break
        if state in ("expired", "error"):
            sys.exit(f"ABORT: job {jid} entered state {state}")
        time.sleep(args.poll_seconds)
    if state != "done":
        sys.exit(f"ABORT: job {jid} not done within {args.timeout_minutes} min (state={state})")

    files = client.batch.download(job_id=jid, output_dir=out_dir)
    n = len(files) if files is not None else "?"
    print(f"[batch]    downloaded {n} files -> {out_dir}", flush=True)

    log = CACHE_ROOT / "JOB_LOG.jsonl"
    with open(log, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(dict(ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                 phase=args.phase, job_id=jid, est_cost_usd=cost,
                                 billable_bytes=size, out_dir=str(out_dir))) + "\n")
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
