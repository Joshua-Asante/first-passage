#!/usr/bin/env python3
"""Append-only fire log for advisory/report-only tooling.

2026-08-15 governance-belt programme audit, action 2. Answers "which of these
report-only mechanisms has never fired" at the next quarterly audit, and
supplies dated instances for triggers like the dedup-first ADR's T2
("3 dated instances of a WARN dismissed as noise") and T3 ("recurrence rate
... measured at the next quarterly programme audit"), which are otherwise
unmeasurable -- nothing in the belt records that it ran.

Records only that a mechanism fired: tool name, a short context (query text,
file path, or similar), and counts. Never log Rule-7 owned values or locked
strategy parameters -- callers control what they pass; this module does not
inspect or redact content.

Fail-open: a logging failure must never break the caller. The log itself is
gitignored (``.cache/``) -- a local, regenerable record, not a Rule-7 owner.

Usage (as a library):
    from gate_fire_log import log_fire
    log_fire("repo_retrieve", query="foo bar", n_hits=3)

Usage (CLI):
    python scripts/gate_fire_log.py --tally
    python scripts/gate_fire_log.py --tally --since 2026-08-15
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOG_PATH = REPO / ".cache" / "gate_fires.jsonl"


def log_fire(tool: str, **fields: object) -> None:
    """Append one fire record. Never raises — a logging failure is not the caller's failure."""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "tool": tool,
            **fields,
        }
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
    except OSError:
        pass


def _read_records(log_path: Path | None = None) -> list[dict]:
    # log_path defaults to the module-level LOG_PATH, resolved at call time
    # (not baked into the signature) so a monkeypatched/reassigned LOG_PATH
    # is honored -- a mutable-default-arg bug here silently pinned every
    # caller to whatever LOG_PATH was at import time.
    path = log_path if log_path is not None else LOG_PATH
    if not path.is_file():
        return []
    records = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def tally(since: str | None = None, log_path: Path | None = None) -> dict[str, int]:
    records = _read_records(log_path)
    if since:
        records = [r for r in records if str(r.get("ts", "")) >= since]
    return dict(Counter(r.get("tool", "unknown") for r in records))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--tally", action="store_true")
    ap.add_argument(
        "--since", type=str, default=None,
        help="ISO-8601 lower bound on the ts field (e.g. 2026-08-15)",
    )
    args = ap.parse_args(argv)

    if not args.tally:
        print("gate_fire_log: pass --tally to summarize, or import log_fire() as a library",
              file=sys.stderr)
        return 2

    counts = tally(args.since)
    suffix = f" since {args.since}" if args.since else ""
    if not counts:
        print(f"gate_fire_log: no fires recorded{suffix}")
        return 0
    print(f"gate_fire_log: {sum(counts.values())} fire(s){suffix}")
    for tool, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {tool:<24} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
