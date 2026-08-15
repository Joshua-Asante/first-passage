# lab/archive/tnec_envelope_compile_2026-08/envelope.py
"""Q-TNEC-ENV-1 cell arithmetic. Pure functions; owners imported, never re-derived.
Kill predicates are PREREG F4 verbatim: K-QTY and K-COST only. Everything else reports.
Edge labels are HYPOTHETICAL per the 2026-08-08 edge-cohort correction.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab"))
sys.path.insert(0, _DIR)

from discovery.cost_model import COST_LAW_MULTIPLE, INSTRUMENT_SPECS, rt_cost_usd  # noqa: E402
from instruments import Inst  # noqa: E402

LADDER_TICKS = (8, 20, 40, 80, 160)                    # PREREG F2
COMMISSION_PER_SIDE = 0.95                             # TNEC-1 N-EDGE screen basis
MICRO_CAP = 80                                         # firm_rules Tradeify_Select_100K
BEST_ON_RECORD_R = 0.85                                # hypothetical-labeled reference (PREREG F4)
INVERSION_R = 0.40                                     # disclosure only (TNEC-1 re-typing)
FRONTIER_RISKS_USD = {"0.49R(hyp)": 250.0, "0.65R(hyp)": 275.0, "0.85R(hyp)": 325.0}


@dataclass(frozen=True)
class Cell:
    stop_ticks: int
    stop_pts: float | None
    r_usd: float
    rt_usd: float
    cost_tax_r: float
    req_delta_ticks: float          # Req-5: COST_LAW_MULTIPLE x RT, in ticks (stop-independent)
    delta_over_stop: float
    inversion_line_r: float         # 0.40 + cost_tax_r — disclosure only
    qty: dict = field(default_factory=dict)
    power_floor: float | None = None
    verdict: str = "OPEN"
    killed_by: str | None = None


def rt_usd(inst: Inst, slip_ticks: int) -> float:
    if inst.symbol in INSTRUMENT_SPECS:
        return rt_cost_usd(inst.symbol, commission_per_side=COMMISSION_PER_SIDE, slip_ticks=slip_ticks, slip_convention="total_rt")
    # MCL/M6A: same total_rt formula on the source-anchored tick_value (instruments.py).
    return 2.0 * COMMISSION_PER_SIDE + slip_ticks * inst.tick_value


def cell(inst: Inst, stop_ticks: int, slip_ticks: int = 1) -> Cell:
    r = stop_ticks * inst.tick_value
    rt = rt_usd(inst, slip_ticks)
    tax = rt / r
    req_delta_ticks = COST_LAW_MULTIPLE * rt / inst.tick_value
    qty = {label: min(int(risk // r), MICRO_CAP) for label, risk in FRONTIER_RISKS_USD.items()}
    power = 1.96 / math.sqrt(inst.panel_n) if inst.panel_n else None

    verdict, killed_by = "OPEN", None
    if max(qty.values()) < 1:
        verdict, killed_by = "DEAD", "qty"                                  # K-QTY
    elif (COST_LAW_MULTIPLE * rt) / r > BEST_ON_RECORD_R:
        verdict, killed_by = "DEAD", "cost"                                 # K-COST
    elif power is None:
        verdict = "OPEN-CONDITIONAL(power)"                                 # PREREG F5

    pts = stop_ticks * inst.tick_value / inst.point_value if inst.point_value else None
    return Cell(stop_ticks, pts, r, rt, tax, req_delta_ticks,
                req_delta_ticks / stop_ticks, INVERSION_R + tax, qty, power, verdict, killed_by)


def instrument_verdict(cells: list[Cell]) -> str:
    open_cells = [c for c in cells if c.verdict.startswith("OPEN")]
    if not open_cells:
        return "EMPTY"
    if all(c.verdict == "OPEN-CONDITIONAL(power)" for c in open_cells):
        return "NON-EMPTY-CONDITIONAL(power)"
    return "NON-EMPTY"


# --- DSR floors (owner: lab/archive/q_kbudget_1_2026-07/floor_scan.py) ---
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab", "archive", "q_kbudget_1_2026-07"))
from floor_scan import CAP, floor_at_k  # noqa: E402


def dsr_floors() -> dict[int, float]:
    return {k: floor_at_k(k) for k in (1, 2, 3)}


def self_check() -> None:
    assert floor_at_k(3) <= CAP < floor_at_k(4), "K wall moved — re-read catalogue_k_wall_2026-08-05"
    assert COST_LAW_MULTIPLE == 4.0, "Req-5 multiple moved — re-read strategy_harvest Req 5"
    assert round(1.96 / math.sqrt(484), 4) == 0.0891, "Clause-N arithmetic drifted"
