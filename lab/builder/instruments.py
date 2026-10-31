"""Instruments the builder trades. Geometry comes from ``core/instrument_specs`` (the single
source); this module adds only the exported ticker and the US day-session open in
America/New_York, where a card's range starts. ``data.load_bars`` checks exported metadata
against both."""
from __future__ import annotations

from dataclasses import dataclass

from instrument_specs import INSTRUMENT_SPECS

SESSION_OPEN = {"MCL": "09:00", "MGC": "08:20", "M2K": "09:30", "MYM": "09:30", "MNQ": "09:30"}


@dataclass(frozen=True)
class Instrument:
    ticker: str
    tick: float
    point_value: float
    session_open: str  # HH:MM America/New_York


INSTRUMENTS = {s: Instrument(f"{s}1!", INSTRUMENT_SPECS[s].tick_size, INSTRUMENT_SPECS[s].multiplier, o)
               for s, o in SESSION_OPEN.items()}
