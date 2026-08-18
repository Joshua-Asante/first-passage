"""Q-EXPR-1 -- share arithmetic on the frozen conversion census.

Freeze-before-table: sha256 the prereg bytes BEFORE opening TABLE.json.
Stdlib only. $0 / K=0. Does not read vendor bars.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PREREG = REPO / "docs" / "briefs" / "pre-registration" / "Q-EXPR-1-verdict-preregistration.md"
TABLE = HERE / "TABLE.json"

SHARE_BAR = 0.50
H1_POSITIVE_HORIZONS = frozenset({"weekly", "daily"})
H2_DEATH = frozenset({"cost-hurdle", "stop-geometry"})
RANKED = frozenset({"weekly", "daily", "session", "intradaily-1m"})


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_day(s: str) -> date:
    y, m, d = (int(p) for p in s.split("-"))
    return date(y, m, d)


def main() -> dict:
    if not PREREG.is_file():
        raise SystemExit(f"ABORT: prereg missing: {PREREG}")
    prereg_sha = sha256_file(PREREG)
    print(f"prereg_sha256 {prereg_sha}")
    print(f"prereg_path   {PREREG.relative_to(REPO).as_posix()}")

    table = json.loads(TABLE.read_text(encoding="utf-8"))

    h1_rows = [r for r in table["regularities"] if r["h1_eligible"]]
    if any(r["native_horizon"] not in RANKED for r in h1_rows):
        raise SystemExit("ABORT: H1-eligible row missing a ranked horizon")
    h1_pos = [r for r in h1_rows if r["native_horizon"] in H1_POSITIVE_HORIZONS]
    h1_n = len(h1_rows)
    h1_k = len(h1_pos)
    h1_share = h1_k / h1_n if h1_n else 0.0
    h1_wins = h1_share >= SHARE_BAR

    h2_rows = table["h2_class"]
    h2_flags = []
    for row in h2_rows:
        placebo = row["placebo_p"]
        placebo_fire = placebo is not None and placebo < 0.05
        gross_present = bool(row["mean_signed_gross_positive"]) and (
            placebo_fire or bool(row["ci_excludes_zero"])
        )
        positive = row["death_stage"] in H2_DEATH and gross_present
        h2_flags.append(
            {
                "id": row["id"],
                "death_stage": row["death_stage"],
                "gross_edge_present": gross_present,
                "h2_positive": positive,
            }
        )
    h2_n = len(h2_rows)
    h2_k = sum(1 for f in h2_flags if f["h2_positive"])
    h2_share = h2_k / h2_n if h2_n else 0.0
    h2_wins = h2_share >= SHARE_BAR

    first_date = min(parse_day(r["first_measured"]) for r in h1_rows)
    first_classes = sorted(
        {
            r["native_horizon"]
            for r in h1_rows
            if parse_day(r["first_measured"]) == first_date
        }
    )
    h3_cannot_fire = len(first_classes) != 1
    counts = Counter(r["native_horizon"] for r in h1_rows)
    mode_h, mode_n = counts.most_common(1)[0]
    mode_share = mode_n / h1_n
    h3_wins = (not h3_cannot_fire) and mode_h == first_classes[0] and mode_share >= SHARE_BAR

    if h1_wins or h2_wins or h3_wins:
        verdict = "RESOLVED"
    else:
        verdict = "FALSIFIED"

    payload = {
        "prereg_sha256": prereg_sha,
        "share_bar": SHARE_BAR,
        "H1": {
            "k": h1_k,
            "n": h1_n,
            "share": round(h1_share, 6),
            "wins": h1_wins,
            "positive_ids": [r["id"] for r in h1_pos],
        },
        "H2": {
            "k": h2_k,
            "n": h2_n,
            "share": round(h2_share, 6),
            "wins": h2_wins,
            "cells": h2_flags,
        },
        "H3": {
            "first_measured": first_date.isoformat(),
            "first_classes": first_classes,
            "cannot_fire": h3_cannot_fire,
            "mode": mode_h,
            "mode_share": round(mode_share, 6),
            "wins": h3_wins,
        },
        "verdict": verdict,
        "winning_branches": [n for n, w in (("H1", h1_wins), ("H2", h2_wins), ("H3", h3_wins)) if w],
    }
    (HERE / "RESULTS.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"H1 {h1_k}/{h1_n} = {h1_share:.4f}  wins={h1_wins}")
    print(f"H2 {h2_k}/{h2_n} = {h2_share:.4f}  wins={h2_wins}")
    print(
        f"H3 mode={mode_h} {mode_share:.4f}  first={first_classes}@{first_date}  "
        f"cannot_fire={h3_cannot_fire}  wins={h3_wins}"
    )
    print(f"verdict {verdict}")
    return payload


if __name__ == "__main__":
    main()
