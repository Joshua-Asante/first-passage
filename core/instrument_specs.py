"""Shared instrument geometry; commission eligibility remains research-owned."""
from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentSpec:
    symbol: str
    multiplier: float
    tick_size: float
    tick_value: float


# Sourced to proxy-discipline.md (+ standard CME parent/energy specs for
# campaigns that score on those notionals). MYM tick_size = 1.00.
INSTRUMENT_SPECS: dict[str, InstrumentSpec] = {
    "MES": InstrumentSpec("MES", 5.0, 0.25, 1.25),
    "MNQ": InstrumentSpec("MNQ", 2.0, 0.25, 0.50),
    "MYM": InstrumentSpec("MYM", 0.50, 1.0, 0.50),
    "M2K": InstrumentSpec("M2K", 5.0, 0.10, 0.50),
    "MGC": InstrumentSpec("MGC", 10.0, 0.10, 1.00),
    "ES": InstrumentSpec("ES", 50.0, 0.25, 12.50),
    "NQ": InstrumentSpec("NQ", 20.0, 0.25, 5.00),
    "YM": InstrumentSpec("YM", 5.0, 1.0, 5.00),
    "RTY": InstrumentSpec("RTY", 50.0, 0.10, 5.00),
    "GC": InstrumentSpec("GC", 100.0, 0.10, 10.00),
    "NG": InstrumentSpec("NG", 10_000.0, 0.001, 10.00),
    "MNG": InstrumentSpec("MNG", 1_000.0, 0.001, 1.00),
}


