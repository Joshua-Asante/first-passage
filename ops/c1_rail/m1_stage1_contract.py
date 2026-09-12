"""Operator-approved M1 proof identity. NEVER a live venue authorization.

2026-09-10: one native MYM tick (c1_rail_slippage.py) is the smallest stop.
For E=100000 and DD=.4 the minimum binary64 risk passing the actual host
formula is .0000125: E*(r*.4)/(.5*1)=1; nextafter(r,0) floors to zero.
Normal raw qty=2; a dedicated one-micro cap bounds both outputs to one.
No production risk registry is extended. Default generated allocation is 0.
"""
from __future__ import annotations

import hashlib
import json
import math

LEG_ID = "m1_stage1_test"
LEG_KEY = "M1 Stage1 Test"
SYMBOL = "MYM1!"
TIER = "Tradeify_Select_100K"
BASE_RISK = .0000125
STOP_DIST_PTS = 1.0
DOLLARS_PER_PT = .50
CAP_ALLOC = 1
PYR_PCT = 0.0
# The offline marker is retained for synthetic test harnesses only.
OFFLINE_SOURCE = {"kind": "offline_fixture", "schema": "ohlcv-1m", "symbol": SYMBOL}
OPERATOR_INPUT_SOURCE = {"kind": "operator_attended_input", "schema": "ohlcv-1m", "symbol": SYMBOL}


def constants_row(*, enabled: bool = False) -> dict:
    """A dedicated row; never borrow a withdrawn leg's risk or allocation."""
    return {"leg_key": LEG_KEY, "base_risk": BASE_RISK, "pyr_pct": PYR_PCT,
            "dollars_per_pt": DOLLARS_PER_PT, "cap_alloc": CAP_ALLOC if enabled else 0}


def contract_sha256() -> str:
    contract = {"version": 1, "leg_id": LEG_ID, "symbol": SYMBOL, "tier": TIER,
                "stop_dist_pts": STOP_DIST_PTS, "row": constants_row(enabled=True),
                "entry_only": True, "permanently_dry_run_only": True}
    return hashlib.sha256(json.dumps(contract, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def rejection_reason(payload: dict, config: dict) -> str | None:
    """Primary listener policy: no mutable state can opt this identity live."""
    if payload.get("leg_id") != LEG_ID:
        return None
    if config.get("dry_run") is not True:
        return "m1_test_requires_explicit_dry_run"
    if payload.get("signal_type") != "entry":
        return "m1_test_entry_only"
    return None


def finite_number(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def validate_sizing_inputs(constants: dict, payload: dict, equity: float,
                           *, expected_equity: float, expected_cap: int) -> None:
    """Validate this proof's inputs only; production sizing behavior is unchanged."""
    if constants.get("tier") != TIER:
        raise ValueError("m1_test_wrong_tier")
    for field, expected in (("E_firm", expected_equity), ("cap_firm", expected_cap)):
        value = constants.get(field)
        if not finite_number(value) or value != expected:
            raise ValueError("m1_test_firm_constants_mismatch")
    rows = constants.get("leg_map")
    if not isinstance(rows, dict):
        raise ValueError("m1_test_invalid_leg_map")
    row = rows.get(LEG_ID)
    if not isinstance(row, dict):
        raise ValueError("m1_test_missing_constants")
    expected = constants_row()
    if set(row) != set(expected) or row.get("leg_key") != LEG_KEY:
        raise ValueError("m1_test_constants_mismatch")
    for field in ("base_risk", "pyr_pct", "dollars_per_pt"):
        if not finite_number(row[field]) or row[field] != expected[field]:
            raise ValueError("m1_test_constants_mismatch")
    if type(row["cap_alloc"]) is not int or row["cap_alloc"] not in (0, CAP_ALLOC):
        raise ValueError("m1_test_invalid_cap")
    total = 0
    for reservation in rows.values():
        if not isinstance(reservation, dict):
            raise ValueError("m1_test_invalid_reservation")
        cap = reservation.get("cap_alloc")
        if not finite_number(cap) or cap < 0 or int(cap) != cap:
            raise ValueError("m1_test_invalid_reservation")
        total += cap
    if total > expected_cap:
        raise ValueError("m1_test_account_cap_exhausted")
    if not finite_number(equity) or equity <= 0:
        raise ValueError("m1_test_invalid_equity")
    if (not finite_number(payload.get("stop_dist_pts"))
            or payload["stop_dist_pts"] != STOP_DIST_PTS):
        raise ValueError("m1_test_stop_mismatch")
    if not finite_number(payload.get("close")) or payload["close"] <= STOP_DIST_PTS:
        raise ValueError("m1_test_invalid_close")
