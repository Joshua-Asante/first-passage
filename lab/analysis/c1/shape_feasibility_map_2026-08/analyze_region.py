"""Merge shard JSONL outputs, cross-check the validation subset, and print the
markdown summary tables consumed by RESULTS.md. Read-only over the sweep's own
output; does not call the MC engine.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import shape_generator as sg  # noqa: E402

FIRM_KEYS = ("Tradeify_Select_100K", "MFFU_Rapid_100K")


def load_jsonl(paths: List[Path]) -> List[dict]:
    rows: Dict[str, dict] = {}
    for p in paths:
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rows[rec["cell_id"]] = rec  # last-writer-wins; sharding guarantees no true dup
    return list(rows.values())


def cross_check(sweep_rows: List[dict], val_rows: List[dict]) -> List[dict]:
    """For every validation row, find the matching (same tuple+firm) sweep row
    and report whether the verdict agrees. Cross-check is by VERDICT class
    (FEASIBLE/MARGINAL/INFEASIBLE), not by exact bust/pass equality -- the two
    runs use different N by design.
    """
    sweep_by_key = {
        (r["win_rate"], r["shape"], r["cadence"], r["risk_usd"], r["firm"]): r
        for r in sweep_rows
    }
    out = []
    for v in val_rows:
        key = (v["win_rate"], v["shape"], v["cadence"], v["risk_usd"], v["firm"])
        s = sweep_by_key.get(key)
        out.append(
            {
                "cell_id": v["cell_id"],
                "validation_n": v["n_total_paths"],
                "validation_bust": v["bust"],
                "validation_pass": v["pass_rate"],
                "validation_verdict": v["verdict"],
                "sweep_n": s["n_total_paths"] if s else None,
                "sweep_bust": s["bust"] if s else None,
                "sweep_pass": s["pass_rate"] if s else None,
                "sweep_verdict": s["verdict"] if s else None,
                "agree": (s is not None and s["verdict"] == v["verdict"]),
            }
        )
    return out


def heatmap_table(rows: List[dict], *, shape: str, firm: str, risk: float) -> str:
    by_key = {(r["win_rate"], r["cadence"]): r for r in rows if r["shape"] == shape and r["firm"] == firm and r["risk_usd"] == risk}
    header = "| win rate \\ cadence(/wk) | " + " | ".join(str(c) for c in sg.CADENCES) + " |"
    sep = "|---" * (len(sg.CADENCES) + 1) + "|"
    lines = [header, sep]
    sym = {"FEASIBLE": "FEASIBLE", "MARGINAL": "MARGINAL", "INFEASIBLE": "infeasible"}
    for wr in sg.WIN_RATES:
        cells = []
        for cd in sg.CADENCES:
            r = by_key.get((wr, cd))
            if r is None:
                cells.append("?")
            else:
                cells.append(f"{sym[r['verdict']]} (bust {r['bust']*100:.1f}%, pass {r['pass_rate']*100:.1f}%)")
        lines.append(f"| {wr:.0%} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def verdict_counts(rows: List[dict]) -> Dict[str, Counter]:
    out: Dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        out[(r["shape"], r["firm"])][r["verdict"]] += 1
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards-dir", required=True)
    ap.add_argument("--out-merged", required=True)
    args = ap.parse_args(argv)

    shards_dir = Path(args.shards_dir)
    sweep_paths = sorted(shards_dir.glob("shard*.jsonl"))
    val_path = shards_dir / "validation.jsonl"

    sweep_rows = load_jsonl(sweep_paths)
    val_rows = load_jsonl([val_path]) if val_path.is_file() else []

    print(f"sweep rows: {len(sweep_rows)} / 630")
    print(f"validation rows: {len(val_rows)} / 8")

    expected = set()
    for t in sg.all_tuples():
        for firm in FIRM_KEYS:
            expected.add(sg.tuple_index(*t))
    missing_ids = set()
    have_ids = {r["cell_id"] for r in sweep_rows}
    for t in sg.all_tuples():
        for firm in FIRM_KEYS:
            wr, sh, cd, rk = t
            cid = f"wr{wr:.2f}_{sh}_cd{cd}_rk{int(rk)}_{firm}"
            if cid not in have_ids:
                missing_ids.add(cid)
    print(f"missing cells: {len(missing_ids)}")
    if missing_ids and len(missing_ids) <= 20:
        for m in sorted(missing_ids):
            print(f"  MISSING {m}")

    out_path = Path(args.out_merged)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        for r in sorted(sweep_rows, key=lambda r: r["cell_id"]):
            fh.write(json.dumps(r) + "\n")
    print(f"wrote merged {out_path}")

    if val_rows:
        print("\n=== validation cross-check ===")
        for row in cross_check(sweep_rows, val_rows):
            print(
                f"{row['cell_id']}: val(N={row['validation_n']}) bust={row['validation_bust']:.4f} "
                f"pass={row['validation_pass']:.4f} verdict={row['validation_verdict']} | "
                f"sweep(N={row['sweep_n']}) bust={row['sweep_bust']} pass={row['sweep_pass']} "
                f"verdict={row['sweep_verdict']} | agree={row['agree']}"
            )

    print("\n=== verdict counts by (shape, firm) ===")
    for (shape, firm), counts in sorted(verdict_counts(sweep_rows).items()):
        print(f"{shape:20s} {firm:24s} {dict(counts)}")

    if len(sweep_rows) == 630:
        print("\n=== heatmap tables (risk=$275) ===")
        for shape in sg.SHAPES:
            for firm in FIRM_KEYS:
                print(f"\n#### {shape} — {firm} (risk=$275)\n")
                print(heatmap_table(sweep_rows, shape=shape, firm=firm, risk=275.0))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
