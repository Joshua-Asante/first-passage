"""Q-TNEC-ENV-1 runner. $0 - K=0 - no network - deterministic.
Modes: --self-check | --compile | --entry <entry.json> (Task 7).
Reproduce: python -X utf8 lab/archive/tnec_envelope_compile_2026-08/run_envelope_compile.py --compile
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)
# Add repo root for core/ and lab/ imports
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, '../../../../'))
sys.path.insert(0, _REPO_ROOT)

import envelope  # noqa: E402
import instruments  # noqa: E402
from envelope import LADDER_TICKS  # noqa: E402

BASIS = ("Tradeify_Select_100K eval - commission $0.95/side (TNEC-1 N-EDGE screen; actual $0.91) - "
         "slip 1 tick total_rt PRIMARY (Stage-1 map execution model), slip 0 DISCLOSURE - "
         "edge labels HYPOTHETICAL per 2026-08-08 edge-cohort correction")


def compile_all(slip_ticks: int = 1) -> dict:
    envelope.self_check()
    out = {"basis": BASIS, "dsr_floors": {str(k): round(v, 3) for k, v in envelope.dsr_floors().items()},
           "instruments": {}, "h_a": "EMPTY"}
    for sym, inst in instruments.POOL.items():
        cells = [envelope.cell(inst, t, slip_ticks) for t in LADDER_TICKS]
        verdict = envelope.instrument_verdict(cells)
        open_cells = [c for c in cells if c.verdict.startswith("OPEN")]
        g0 = {}
        if open_cells:
            g0 = {"req_delta_ticks": round(open_cells[0].req_delta_ticks, 2),
                  "open_stop_ticks": [c.stop_ticks for c in open_cells],
                  "power_floor": open_cells[0].power_floor,
                  "note": "the numbers a G0 freeze must defend (PREREG F4/F5)"}
        out["instruments"][sym] = {"cells": [dataclasses.asdict(c) for c in cells],
                                   "verdict": verdict, "g0_numbers": g0}
        if verdict.startswith("NON-EMPTY"):
            out["h_a"] = "NON-EMPTY"
    return out


def render_markdown(result: dict) -> str:
    lines = [f"**Basis:** {result['basis']}", "",
             f"**DSR floors (confirm-stage bar, K=1/2/3):** "
             f"{result['dsr_floors']['1']} / {result['dsr_floors']['2']} / {result['dsr_floors']['3']}", ""]
    for sym, block in result["instruments"].items():
        lines += [f"### {sym} — {block['verdict']}", "",
                  "| stop (ticks) | stop (pts) | R/ct | RT$ | cost tax | req δ (ticks) | δ/stop | "
                  "inv. line (disc.) | qty@250/275/325(hyp) | power floor | verdict |",
                  "|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|"]
        for c in block["cells"]:
            pts = f"{c['stop_pts']:.2f}" if c["stop_pts"] is not None else "UNSCR(pt_val)"
            pf = f"{c['power_floor']:.4f}" if c["power_floor"] is not None else "UNSCR(panel_N)"
            q = "/".join(str(c["qty"][k]) for k in ("0.49R(hyp)", "0.65R(hyp)", "0.85R(hyp)"))
            v = c["verdict"] if not c["killed_by"] else f"DEAD({c['killed_by']})"
            lines.append(f"| {c['stop_ticks']} | {pts} | ${c['r_usd']:.2f} | ${c['rt_usd']:.2f} | "
                         f"{c['cost_tax_r']:.3f}R | {c['req_delta_ticks']:.1f} | "
                         f"{c['delta_over_stop']:.2f} | {c['inversion_line_r']:.3f}R | {q} | {pf} | {v} |")
        lines.append("")
    lines.append(f"**H_A: {result['h_a']}**")
    return "\n".join(lines)


HORIZON_FLOOR_S = 5.0   # Route B precondition (rail latency)

_REQUIRED = ("name", "instrument", "stop_ticks", "delta_ticks_per_event", "delta_source",
             "events_per_year", "horizon_seconds", "taxonomy_class")


def score_entry(entry: dict) -> dict:
    missing = [k for k in _REQUIRED if k not in entry]
    if missing:
        return {"verdict": "UNSCREENABLE", "wall": f"missing fields: {missing}", "checks": []}
    if entry["instrument"] not in instruments.POOL:
        return {"verdict": "UNSCREENABLE", "wall": f"unknown instrument: {entry['instrument']}", "checks": []}
    try:
        stop_ticks = int(entry["stop_ticks"])
    except (TypeError, ValueError):
        return {"verdict": "UNSCREENABLE", "wall": f"stop_ticks not an integer: {entry['stop_ticks']!r}", "checks": []}
    inst = instruments.POOL[entry["instrument"]]
    c = envelope.cell(inst, stop_ticks)
    checks = []

    if entry["delta_ticks_per_event"] is None:
        return {"verdict": "UNSCREENABLE",
                "wall": "delta uncited — route: delta-extraction probe needed (harvest Req 2 relief valve)",
                "checks": checks}
    if entry["horizon_seconds"] < HORIZON_FLOOR_S:
        return {"verdict": "FAIL", "wall": "horizon", "checks": checks}
    if c.verdict == "DEAD":
        return {"verdict": "FAIL", "wall": "cell", "checks": [f"target cell DEAD({c.killed_by})"]}
    checks.append(f"cell {entry['stop_ticks']}t {c.verdict}")

    if float(entry["delta_ticks_per_event"]) < c.req_delta_ticks:
        return {"verdict": "FAIL", "wall": "cost",
                "checks": checks + [f"delta {entry['delta_ticks_per_event']} < req {c.req_delta_ticks:.1f} ticks"]}
    checks.append(f"delta clears 4x hurdle ({c.req_delta_ticks:.1f} ticks)")

    if c.power_floor is not None:
        import math as _m
        n = float(entry["events_per_year"]) * 2.0   # generous 2y OOS read; Req 4 is the real bar at admission
        checks.append(f"power note: min detectable delta/sigma {1.96 / _m.sqrt(n):.4f} at N={n:.0f} "
                      f"(instrument floor {c.power_floor:.4f}; harvest Req 4 binds at admission)")
    return {"verdict": "SEED-GRADE", "wall": None, "checks": checks}


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-check", action="store_true")
    mode.add_argument("--compile", action="store_true", dest="do_compile")
    mode.add_argument("--entry", metavar="ENTRY_JSON")
    args = ap.parse_args()

    if args.self_check:
        envelope.self_check()
        print("self-check OK — floor_scan 3/4 boundary, Req-5 multiple, Clause-N arithmetic")
        return
    if args.entry:
        with open(args.entry, encoding="utf-8") as f:
            entry = json.load(f)
        v = score_entry(entry)
        print(json.dumps({"name": entry.get("name"), **v}, indent=1))
        return

    result = compile_all()
    with open(os.path.join(_DIR, "RESULTS.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, sort_keys=True)
    print(render_markdown(result))
    print(f"\nH_A: {result['h_a']}  (RESULTS.json written)")


if __name__ == "__main__":
    main()
