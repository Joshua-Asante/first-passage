# lab/archive/transfer_expression_grid_2026-08/run_grid_compile.py
"""Q-TXG-1 Block-1 runner. $0 - K=0 - no network - no PnL reads - deterministic.
Modes: --self-check | --compile
Reproduce: python -X utf8 lab/archive/transfer_expression_grid_2026-08/run_grid_compile.py --compile
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
_ENV1 = os.path.join(_REPO_ROOT, "lab", "analysis", "c1", "tnec_envelope_compile_2026-08")
_FLOOR = os.path.join(_REPO_ROOT, "lab", "archive", "q_kbudget_1_2026-07")
sys.path.insert(0, _REPO_ROOT)
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab"))
sys.path.insert(0, _ENV1)
sys.path.insert(0, _FLOOR)
sys.path.insert(0, _DIR)

from core.firm_rules import _BASE_RISK  # noqa: E402
from discovery.cost_model import COST_LAW_MULTIPLE  # noqa: E402
from floor_scan import CAP, floor_at_k  # noqa: E402

import atr_map  # noqa: E402
import walls  # noqa: E402

BASIS = (
    "Q-TXG-1 Block 1 — Tradeify_Select_100K eval — 4 mechanisms × ENV-1 7-micro pool — "
    "walls W-DEDUP/W-VENUE/W-CAP/W-COST (W-CADENCE/W-REGIME/S7 disclosure) — "
    "envelope.py owner for cell arithmetic — $0/K=0/no PnL reads"
)


def self_check() -> None:
    assert _BASE_RISK == {"guardian": 0.0034, "striker": 0.0070,
                          "aegis": 0.0150, "striker_nas100": 0.0037}, \
        "BASE_RISK moved — re-read firm_rules + allocation-refresh-2 ADR"
    assert floor_at_k(3) <= CAP < floor_at_k(4), "K wall moved — re-read catalogue_k_wall"
    assert COST_LAW_MULTIPLE == 4.0, "Req-5 multiple moved"
    assert abs(atr_map.ATR_TICKS_MYM_ATR11 - 50.6834) < 1e-6
    assert abs(atr_map.ATR_TICKS_MNQ_ATR11 - 182.038) < 1e-3
    # ENV-1 import still resolves
    import envelope as _e  # noqa: F401
    assert os.path.isfile(os.path.join(_ENV1, "envelope.py"))


def compile_all() -> dict:
    self_check()
    cells = walls.evaluate_all()
    open_cells = [c for c in cells if c.verdict == "OPEN"]
    return {
        "basis": BASIS,
        "dsr_floors": {str(k): round(floor_at_k(k), 3) for k in (1, 2, 3)},
        "cells": [dataclasses.asdict(c) for c in cells],
        "h_a": "OPEN" if open_cells else "EMPTY",
        "open_cells": [
            {"mech": c.mech_id, "symbol": c.symbol, "transfer_type": c.transfer_type,
             "port_must_beat": c.port_must_beat}
            for c in open_cells
        ],
    }


def render_markdown(result: dict) -> str:
    lines = [f"**Basis:** {result['basis']}", "",
             f"**DSR floors (K=1/2/3):** "
             f"{result['dsr_floors']['1']} / {result['dsr_floors']['2']} / "
             f"{result['dsr_floors']['3']}", "",
             "| mech | sym | transfer | stop_raw | stop_map | cost_tax | qty | verdict |",
             "|---|---|---|---:|---:|---:|---:|---|"]
    for c in result["cells"]:
        raw = f"{c['stop_ticks_raw']:.2f}" if c["stop_ticks_raw"] is not None else "—"
        mp = str(c["stop_ticks_mapped"]) if c["stop_ticks_mapped"] is not None else "UNSCR"
        tax = f"{c['cost_tax_r']:.3f}R" if c["cost_tax_r"] is not None else "—"
        qty = str(c["qty"]) if c["qty"] is not None else "—"
        lines.append(
            f"| {c['mech_id']} | {c['symbol']} | {c['transfer_type']} | {raw} | {mp} | "
            f"{tax} | {qty} | {c['verdict']} |"
        )
    lines += ["", f"**H_A: {result['h_a']}**  ({len(result['open_cells'])} OPEN cells)"]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--self-check", action="store_true")
    mode.add_argument("--compile", action="store_true", dest="do_compile")
    args = ap.parse_args()
    if args.self_check:
        self_check()
        print("self-check OK — BASE_RISK, K-wall, Req-5, ATR ticks, ENV-1 import")
        return
    result = compile_all()
    with open(os.path.join(_DIR, "GRID_RESULTS.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, sort_keys=True)
    print(render_markdown(result))
    print(f"\nH_A: {result['h_a']}  (GRID_RESULTS.json written)")


if __name__ == "__main__":
    main()
