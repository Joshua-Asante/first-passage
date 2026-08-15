"""Q-TNEC-ENV-1 instrument pool. Owners, never re-derived here:
- point/tick values: lab/discovery/cost_model.py INSTRUMENT_SPECS (live import, 5 symbols;
  multiplier field mapped to point_value via campaign-local _SpecAdapter).
- MCL/M6A tick_value: transcribed from the Stage-1 map RT-1t column with the
  connecting arithmetic shown (RT 1t $2.82 = 2 x $0.91 commission + $1.00 tick)
  -- c1_thirdleg_instrument_map_2026-07-27/RESULTS.md, table row MCL / M6A.
- panel Ns: Stage-1 "N (own panel)" and Stage-2 ex-FOMC counts (same campaign).
PREREG F1/F5 freeze the pool and the N sources; edit nothing here without a new freeze.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab"))

from discovery.cost_model import INSTRUMENT_SPECS, InstrumentSpec as _InstrumentSpec  # noqa: E402


# Adapter wrapper: map INSTRUMENT_SPECS multiplier to point_value
class _SpecAdapter:
    """Wraps InstrumentSpec to alias multiplier as point_value."""
    def __init__(self, spec: _InstrumentSpec):
        self._spec = spec

    @property
    def point_value(self) -> float:
        return self._spec.multiplier

    @property
    def tick_value(self) -> float:
        return self._spec.tick_value

    @property
    def symbol(self) -> str:
        return self._spec.symbol


SPECS = {sym: _SpecAdapter(spec) for sym, spec in INSTRUMENT_SPECS.items()}


@dataclass(frozen=True)
class Inst:
    symbol: str
    tick_value: float
    point_value: float | None   # None => no committed source; pts column renders UNSCREENABLE
    group: str
    long_only: bool             # S4-LONG-ONLY (Equity Index Product Group)
    panel_n: int | None         # Stage-1 "N (own panel)"; None => UNSCREENABLE-INPUT(panel_N)
    slot_n: int | None          # Stage-2 ex-FOMC slot-overlay N
    source: str


def _from_specs(sym: str, group: str, long_only: bool,
                panel_n: int | None, slot_n: int | None) -> Inst:
    s = SPECS[sym]
    return Inst(sym, s.tick_value, s.point_value, group, long_only, panel_n, slot_n,
                source="lab/discovery/cost_model.py INSTRUMENT_SPECS (live import via _SpecAdapter)")


_STAGE1 = "c1_thirdleg_instrument_map_2026-07-27/RESULTS.md (RT-1t arithmetic; N own-panel)"

POOL: dict[str, Inst] = {
    "MNQ": _from_specs("MNQ", "Equity Index", True, None, None),
    "MYM": _from_specs("MYM", "Equity Index", True, 484, 450),
    "MES": _from_specs("MES", "Equity Index", True, None, None),
    "MGC": _from_specs("MGC", "Metals", False, None, None),
    "M2K": _from_specs("M2K", "Equity Index", True, 484, 450),
    # RT 1t $2.82 = 2 x $0.91 + tick_value  =>  tick_value $1.00; point_value uncommitted.
    "MCL": Inst("MCL", 1.00, None, "Energy", False, 251, 233, source=_STAGE1),
    "M6A": Inst("M6A", 1.00, None, "Currencies", False, 484, 450, source=_STAGE1),
}
