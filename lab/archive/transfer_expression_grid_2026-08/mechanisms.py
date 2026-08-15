"""Q-TXG-1 mechanism axis. Constants via citation-chain (PREREG §0) — Pine not read.
Risk% is a live import from firm_rules._BASE_RISK (owner); never transcribed as a literal
used in arithmetic.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from core.firm_rules import _BASE_RISK  # noqa: E402


@dataclass(frozen=True)
class Mechanism:
    mech_id: str
    version: str
    risk_key: str
    sl_atr_mult: float
    atr_len: int
    session_note: str
    dow: str
    same_underlying_syms: frozenset
    source: str


MECHANISMS: dict[str, Mechanism] = {
    "guardian": Mechanism(
        "guardian", "v5.5", "guardian", 1.55, 14,
        "0800-1600 UTC", "Mon/Tue/Thu", frozenset({"MGC"}),
        source="core/strategies/_archive/guardian/LOCK.md locked config (v5.5)",
    ),
    "striker": Mechanism(
        "striker", "v4.5", "striker", 1.20, 11,
        "13-17 UTC", "Tue/Fri", frozenset({"MYM"}),
        source="core/strategies/_archive/striker/LOCK.md locked config (v4.5)",
    ),
    "striker_nas100": Mechanism(
        "striker_nas100", "v1", "striker_nas100", 1.20, 11,
        "13-17 UTC", "Mon/Tue", frozenset({"MNQ"}),
        source="core/strategies/_archive/nas/LOCK.md locked config (v1)",
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
