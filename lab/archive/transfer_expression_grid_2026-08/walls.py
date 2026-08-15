# lab/archive/transfer_expression_grid_2026-08/walls.py
"""Q-TXG-1 Phase-A wall battery. Kill order: DEDUP → VENUE → CAP → COST.
Disclosure walls (CADENCE, REGIME, S7) never kill. Owners imported, never re-derived.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
_ENV1 = os.path.join(_REPO_ROOT, "lab", "analysis", "c1", "tnec_envelope_compile_2026-08")
sys.path.insert(0, _REPO_ROOT)
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab"))
sys.path.insert(0, _ENV1)
sys.path.insert(0, _DIR)

from core.firm_rules import FIRM_RULES, _BASE_RISK  # noqa: E402
import envelope  # noqa: E402
import instruments as env1_instruments  # noqa: E402
from envelope import LADDER_TICKS, MICRO_CAP  # noqa: E402

import atr_map  # noqa: E402
import mechanisms  # noqa: E402

POOL_ORDER = ("MNQ", "MYM", "MES", "MGC", "M2K", "MCL", "M6A")
LIFECYCLE = 1.00  # AUTHORIZED · MECHANISM — disclosure; live import not required for constant 1.0
BALANCE = FIRM_RULES["Tradeify_Select_100K"]["starting_balance"]
EQUITY_INDEX = frozenset({"MNQ", "MYM", "MES", "M2K"})

# PREREG F7 — frozen dispositions (mech_id, symbol) → verdict
DEDUP_MAP: dict[tuple[str, str], str] = {
    ("striker", "MYM"): "WITHDRAWN(F1)",
    ("striker_nas100", "MNQ"): "WITHDRAWN(F1)",
    ("guardian", "MGC"): "PARKED(b8)",
}

S7_OCCUPANCY_DISCLOSURE = (
    "S7 map (third-leg §7.1): MNQ Mon+Tue · MYM Tue+Fri; both c1 legs withdrawn "
    "(de-scope 2026-08-04); LEG_MAP retained-not-released — bindingness deferred to Block 2"
)


@dataclass(frozen=True)
class CellResult:
    mech_id: str
    symbol: str
    transfer_type: str
    verdict: str
    killed_by: str | None
    stop_ticks_raw: float | None
    stop_ticks_mapped: int | None
    cost_tax_r: float | None
    req_net_r: float | None
    qty: int | None
    disclosures: list = field(default_factory=list)
    port_must_beat: dict = field(default_factory=dict)


def _qty_at(risk_frac: float, stop_ticks: int, tick_value: float) -> int:
    r_usd = stop_ticks * tick_value
    if r_usd <= 0:
        return 0
    return min(int((BALANCE * risk_frac * LIFECYCLE) // r_usd), MICRO_CAP)


def evaluate_cell(mech_id: str, symbol: str) -> CellResult:
    m = mechanisms.MECHANISMS[mech_id]
    ttype = mechanisms.transfer_type(m, symbol)
    discs = [S7_OCCUPANCY_DISCLOSURE,
             "W-CADENCE: disclosure only (design §4)",
             "W-REGIME: disclosure only — H1-chop co-draw prior (design §4)"]
    if ttype == "cross-underlying":
        discs.append("transplant prior: cross-underlying record 0/2 (EURGBP, USDCAD dead)")

    # W-DEDUP
    if (mech_id, symbol) in DEDUP_MAP:
        v = DEDUP_MAP[(mech_id, symbol)]
        return CellResult(mech_id, symbol, ttype, v, "dedup", None, None, None, None, None,
                          discs, {})

    # W-VENUE — pool membership is the product-set proxy (ENV-1 F1); all four mechs long-only.
    if symbol not in POOL_ORDER:
        return CellResult(mech_id, symbol, ttype, "DEAD(venue)", "venue", None, None, None,
                          None, None, discs, {})
    if symbol in EQUITY_INDEX:
        discs.append("Equity Index Product Group: long-or-flat — mechanism is long-only (LOCK)")
    if mech_id.startswith("striker"):
        discs.append("de-scope amendment 2026-08-04: Striker-mechanism research on a different "
                     "instrument is not barred; redeploy of withdrawn legs is")

    inst = env1_instruments.POOL[symbol]
    risk = _BASE_RISK[m.risk_key]
    raw = atr_map.stop_ticks(m, symbol)
    mapped = atr_map.map_stop_ticks(raw) if raw is not None else None

    # W-CAP
    qty = None
    if mapped is not None:
        qty = _qty_at(risk, mapped, inst.tick_value)
        if qty < 1:
            return CellResult(mech_id, symbol, ttype, "DEAD(cap)", "cap", raw, mapped,
                              None, None, qty, discs, {})
    else:
        # stop unscreenable — try best OPEN-capable rung for qty feasibility
        discs.append("UNSCREENABLE-INPUT(stop_cell): no ATR(%d)-matched median for %s" %
                     (m.atr_len, symbol))
        best_q, best_t = 0, None
        for t in LADDER_TICKS:
            q = _qty_at(risk, t, inst.tick_value)
            if q >= 1 and (best_t is None or t * inst.tick_value > best_t * inst.tick_value):
                best_q, best_t = q, t
        if best_t is None:
            return CellResult(mech_id, symbol, ttype, "DEAD(cap)", "cap", None, None,
                              None, None, 0, discs, {})
        qty = best_q
        discs.append("stop_unscreenable_qty_at_best_open_rung=%dt qty=%d" % (best_t, best_q))

    # W-COST
    cost_tax = req = None
    pmb = {"nsurv_ceiling_pct": 3.0, "lifecycle": LIFECYCLE, "risk_pct": risk}
    if mapped is None:
        pmb["stop_cell"] = "UNSCREENABLE"
        return CellResult(mech_id, symbol, ttype, "OPEN", None, raw, None, None, None, qty,
                          discs, pmb)

    cell = envelope.cell(inst, mapped, slip_ticks=1)
    cost_tax = cell.cost_tax_r
    req = cost_tax
    pmb.update({"stop_ticks": mapped, "cost_tax_r": round(cost_tax, 4),
                "required_net_r": round(req, 4), "qty_at_locked_risk": qty,
                "env1_cell_verdict": cell.verdict})
    if cell.killed_by == "cost":
        return CellResult(mech_id, symbol, ttype, "DEAD(cost)", "cost", raw, mapped,
                          cost_tax, req, qty, discs, pmb)
    return CellResult(mech_id, symbol, ttype, "OPEN", None, raw, mapped, cost_tax, req, qty,
                      discs, pmb)


def evaluate_all() -> list[CellResult]:
    out = []
    for mech_id in mechanisms.MECHANISMS:
        for sym in POOL_ORDER:
            out.append(evaluate_cell(mech_id, sym))
    return out
