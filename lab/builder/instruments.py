"""Instruments the builder trades. Geometry comes from ``core/instrument_specs`` (the single
source); this module adds only the exported ticker and timezone, and the US day-session open in
America/New_York, where a card's range starts. ``data.read_bar_export`` checks every exported
row against them."""
from __future__ import annotations

from dataclasses import dataclass

from instrument_specs import INSTRUMENT_SPECS

# On the quarter-hour M15 grid. MGC's 08:20 COMEX day open has no bar boundary, so its range
# starts with the first whole bar after it, 08:30.
SESSION_OPEN = {"MCL": "09:00", "MGC": "08:30", "M2K": "09:30", "MYM": "09:30", "MNQ": "09:30"}
# CME Globex halts every product here 17:00-18:00 ET; the trading day the engine reads ends at 17:00.
DAY_END = "17:00"
EXPORT_TZ = "America/New_York"
if any(int(o[3:]) % 15 for o in SESSION_OPEN.values()):
    raise ValueError("session opens must sit on the 15m grid")


@dataclass(frozen=True)
class Instrument:
    ticker: str
    tick: float
    point_value: float
    session_open: str  # HH:MM America/New_York


INSTRUMENTS = {s: Instrument(f"{s}1!", INSTRUMENT_SPECS[s].tick_size, INSTRUMENT_SPECS[s].multiplier, o)
               for s, o in SESSION_OPEN.items()}


def minutes(hhmm: str) -> int:
    return int(hhmm[:2]) * 60 + int(hhmm[3:])
