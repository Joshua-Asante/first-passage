"""One DYN-SURVEY-1 run from the private freeze record. Usage, from the repo root:

    python -I scripts/fp.py python lab/analysis/_inbox/dyn_survey_2026_11/run.py <freeze.json>

Refuses unless HEAD is the frozen SHA, tracked files are clean, both output paths are private and
no run has started. Writes only to the record's private ``out`` directory and exposure log.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "lab"), str(ROOT / "core")]

import pandas as pd  # noqa: E402

from builder import data  # noqa: E402
from builder.gates import Costs  # noqa: E402
from builder.instruments import minutes  # noqa: E402
from discovery.cost_model import resolve_commission  # noqa: E402
from discovery.remc_series_builder import OutputPathError, assert_out_dir_allowed  # noqa: E402
from research_utils.camp_import import load_camp_sibling  # noqa: E402

S = load_camp_sibling("survey", __file__)

SYMBOLS = ("MNQ", "MYM", "M2K", "MGC", "MCL")
FIRMS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")
MARKER = "run.started"
ONE_RUN = "one run; a rerun needs a recorded defect and an addendum"


class Refused(RuntimeError):
    pass


def check_head(frozen_sha: str) -> None:
    def git(*args: str) -> str:
        return subprocess.run(("git", *args), cwd=ROOT, check=True, capture_output=True, text=True).stdout
    head = git("rev-parse", "HEAD").strip()
    if head != frozen_sha:
        raise Refused(f"HEAD {head} is not the frozen SHA {frozen_sha}")
    if git("status", "--porcelain", "--untracked-files=no").strip():
        raise Refused("tracked files differ from the frozen SHA")


def check_private(path: Path) -> None:
    """Refuse an output path that git tracks or that sits unignored in the repository."""
    try:
        assert_out_dir_allowed(path, repo_root=ROOT)
    except OutputPathError as e:
        raise Refused(str(e)) from e


def claim_run(out: Path, frozen_sha: str) -> Path:
    """Create the run marker atomically before any input is read. It is never removed."""
    marker = out / MARKER
    try:
        with open(marker, "x", encoding="utf-8") as fh:
            json.dump({"frozen_sha": frozen_sha, "started": datetime.now(timezone.utc).isoformat()}, fh)
    except FileExistsError:
        raise Refused(f"{marker} exists: {ONE_RUN}") from None
    return marker


def commission_row(firm: str, symbol: str) -> dict:
    """The report's commission entry; a missing row is recorded, not raised."""
    try:
        return {"commission": resolve_commission(firm, symbol), "missing": None}
    except (KeyError, ValueError) as e:
        return {"commission": None, "missing": str(e)}


def commission_gap(symbol: str, quotes: dict | None) -> str | None:
    """Why the symbol drops under protocol 7.2, or None when both firms' quotes match."""
    for firm in FIRMS:
        quote = (quotes or {}).get(firm)
        if quote is None:
            return f"no fee quote at {firm}"
        try:
            have = resolve_commission(firm, symbol)
        except (KeyError, ValueError) as e:
            return f"no commission row at {firm}: {e}"
        if abs(have - quote) > 1e-9:
            return f"quote {quote} does not match resolve_commission {have} at {firm}"
    return None


def log_read(log: Path, symbol: str, entry: dict) -> None:
    """One exposure-log row per instrument, before its bars are read."""
    row = (date.today().isoformat(), "DYN-SURVEY-1 run.py", symbol, f"pinned export {entry['sha256'][:8]}, full span",
           "timestamps, volumes, prices, cell outcomes", "planned", "DYN-SURVEY-1 development run")
    with open(log, "a", encoding="utf-8", newline="\n") as fh:
        fh.write("| " + " | ".join(row) + " |\n")


def read_volume(path: Path, index: pd.DatetimeIndex) -> pd.Series:
    """Bar volume by bar open; the builder's reader drops this field."""
    by_epoch = {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["Type"].startswith("Entry"):
                m = data.SIGNAL.match(r["Signal"])
                by_epoch[int(m["epoch"])] = int(m["v"])
    return pd.Series([by_epoch[int(e)] for e in index.tz_convert("UTC").as_unit("ms").asi8], index=index)


def not_evaluated(symbol: str, reason: str) -> list[dict]:
    return [{"id": S.cell_id(symbol, c, d), "status": "NOT EVALUATED", "reason": reason}
            for c in S.CELLS for d in S.DIRECTIONS]


def survey_instrument(symbol: str, entry: dict, calendar, book: dict, log: Path) -> tuple[list[dict], dict]:
    gap = commission_gap(symbol, entry.get("quoted_commission"))
    if gap:
        return not_evaluated(symbol, gap), {}
    log_read(log, symbol, entry)
    try:
        bars, summary = data.load_bars(Path(entry["path"]), symbol, entry["sha256"])
        sessions = data.session_dates(bars, symbol)
        dev = [d for d in sessions if d >= S.DEV_START]
        if not dev:
            raise data.DataError("no development sessions")
        calendar.check_covers(dev, symbol)
    except data.DataError as e:
        return not_evaluated(symbol, f"data refused: {e}"), {}
    h_start = entry.get("h_start")
    if h_start is not None and dev[-1] >= h_start:
        raise Refused(f"{symbol}: export reaches its holdout interval ({dev[-1]} >= {h_start})")
    s = minutes(entry["settlement"]) if entry.get("settlement") else None
    commission = resolve_commission(FIRMS[0], symbol)
    days = S.session_days(bars)
    rows = [S.evaluate_cell(c, d, symbol, sessions, dev, days, calendar.closed, s, commission, book)
            for c in S.CELLS for d in S.DIRECTIONS]
    cost = Costs(commission, S.BASE_TICKS).per_trade(symbol)
    table = S.quality(bars, read_volume(Path(entry["path"]), bars.index), dev, symbol, cost)
    return rows, {"summary": summary, "development": [dev[0], dev[-1], len(dev)], "quality": table}


def main(record_path: Path) -> dict:
    record = json.loads(record_path.read_text(encoding="utf-8"))
    check_head(record["frozen_sha"])
    out = Path(record["out"])
    log = Path(record["exposure_log"])
    check_private(out)
    check_private(log)
    report_path = out / "report.json"
    if report_path.exists():
        raise Refused(f"{report_path} exists: {ONE_RUN}")
    if set(record["instruments"]) != set(SYMBOLS):
        raise Refused(f"the record must list exactly {SYMBOLS}")
    if not log.is_file():
        raise Refused(f"{log}: the exposure log is seeded at freeze")
    out.mkdir(parents=True, exist_ok=True)
    claim_run(out, record["frozen_sha"])
    calendar = data.load_calendar(Path(record["calendar"]["path"]), record["calendar"]["sha256"])
    book = data.load_book(Path(record["book"]["path"]), record["book"]["sha256"])
    rows, detail = [], {}
    for symbol in SYMBOLS:
        got, detail[symbol] = survey_instrument(symbol, record["instruments"][symbol], calendar, book, log)
        rows += got
    if len(rows) != S.K:
        raise Refused(f"{len(rows)} cells, K is {S.K}")
    chosen = S.select(rows)
    report = {"survey": "DYN-SURVEY-1", "k": S.K, "frozen_sha": record["frozen_sha"],
              "freeze_record_sha256": hashlib.sha256(record_path.read_bytes()).hexdigest(),
              "exposure_log_sha256": data.file_sha256(log), "outcome": S.outcome(rows, chosen),
              "advanced": chosen["id"] if chosen else None,
              "eligible_rises": {r["id"]: r["rise"] for r in rows if r["status"] == "ELIGIBLE"},
              "commissions": {f: {s: commission_row(f, s) for s in SYMBOLS} for f in FIRMS},
              "cells": rows, "instruments": detail}
    report_path.write_text(json.dumps(report, indent=1, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("record", type=Path)
    result = main(ap.parse_args().record)
    print(result["outcome"], result["advanced"])
