"""Q-TXG-1 mechanism axis. Constants via citation-chain (PREREG §0) — Pine not read.
Risk% is a live import from firm_rules._BASE_RISK (owner); never transcribed as a literal
used in arithmetic.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from core.firm_rules import _BASE_RISK  # noqa: E402

# Striker-family stop multiple, ATR length, session and day-of-week are Pine-only
# (core/strategies/CATALOG.md §Locked parameter record). Redacted from the public copy
# 2026-10-09 (operator decision, option 2); original preserved in first-passage-archive
# archive/preserve-exposure-2026-10-09 7df79240c146ec8a3e9799bb882431c5ab13b9a7. They load from
# this gitignored input ({mech_id: {sl_atr_mult, atr_len, session_note, dow}}); when it is
# absent the fields are None and atr_map returns None for those cells (skip).
_PRIVATE_PARAMS = os.path.join(_DIR, "locked_params.private.json")


def _private(mech_id: str) -> dict:
    try:
        with open(_PRIVATE_PARAMS, encoding="utf-8") as fh:
            return json.load(fh).get(mech_id, {})
    except FileNotFoundError:
        return {}


@dataclass(frozen=True)
class Mechanism:
    mech_id: str
    version: str
    risk_key: str
    sl_atr_mult: float | None
    atr_len: int | None
    session_note: str | None
    dow: str | None
    same_underlying_syms: frozenset
    source: str


def _striker_family(mech_id: str, version: str, syms: frozenset, source: str) -> Mechanism:
    p = _private(mech_id)
    return Mechanism(mech_id, version, mech_id, p.get("sl_atr_mult"), p.get("atr_len"),
                     p.get("session_note"), p.get("dow"), syms, source=source)


MECHANISMS: dict[str, Mechanism] = {
    "guardian": Mechanism(
        "guardian", "v5.5", "guardian", 1.55, 14,
        "0800-1600 UTC", "Mon/Tue/Thu", frozenset({"MGC"}),
        source="core/strategies/_archive/guardian/LOCK.md locked config (v5.5)",
    ),
    "striker": _striker_family(
        "striker", "v4.5", frozenset({"MYM"}),
        "core/strategies/_archive/striker/LOCK.md locked config (v4.5)",
    ),
    "striker_nas100": _striker_family(
        "striker_nas100", "v1", frozenset({"MNQ"}),
        "core/strategies/_archive/nas/LOCK.md locked config (v1)",
    ),
    "aegis": Mechanism(
        "aegis", "v4.3", "aegis", 1.42, 19,
        "1000-1345 chart TZ", "Mon/Tue/Wed", frozenset(),
        source="core/strategies/_archive/aegis/LOCK.md locked config (v4.3)",
    ),
}


def risk_pct(m: Mechanism) -> float:
    return _BASE_RISK[m.risk_key]


def transfer_type(m: Mechanism, symbol: str) -> str:
    return "same-underlying" if symbol in m.same_underlying_syms else "cross-underlying"
