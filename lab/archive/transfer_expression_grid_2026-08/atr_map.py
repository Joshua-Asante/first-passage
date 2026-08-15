# lab/archive/transfer_expression_grid_2026-08/atr_map.py
"""Committed ATR-in-ticks sources for W-COST stop-cell mapping (PREREG F6).
Owner of medians: lab/analysis/c1/q_rail_1_2026-07/f2_floors.json recent_90d
(atr_median_pts). Owner of tick_size: lab/discovery/cost_model.INSTRUMENT_SPECS.
ATR length must match the mechanism (Striker family ATR 11 only).

Inputs extension (2026-08-12): inventory beyond MYM/MNQ + M6J venue probe.
Derivation convention for any NEW atr_median_pts row = f2_floors.atr_frame
(roll-seam-masked RMA ATR(11), recent_90d median, round 4 dp) on a present
core/data/bar_data/<SYM>_M15.csv whose sha matches SHA256SUMS — then divide by
INSTRUMENT_SPECS[sym].tick_size. Never invent; gitignored-absent = PENDING.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.abspath(os.path.join(_DIR, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab"))
sys.path.insert(0, os.path.join(_REPO_ROOT, "lab", "analysis", "c1",
                                "tnec_envelope_compile_2026-08"))

from discovery.cost_model import INSTRUMENT_SPECS  # noqa: E402
from envelope import LADDER_TICKS  # noqa: E402
from mechanisms import Mechanism  # noqa: E402

# Transcribed from f2_floors.json recent_90d.atr_median_pts (committed artifact).
_ATR_PTS_RECENT90_ATR11 = {"MYM": 50.6834, "MNQ": 45.5095}
ATR_TICKS_MYM_ATR11 = _ATR_PTS_RECENT90_ATR11["MYM"] / INSTRUMENT_SPECS["MYM"].tick_size
ATR_TICKS_MNQ_ATR11 = _ATR_PTS_RECENT90_ATR11["MNQ"] / INSTRUMENT_SPECS["MNQ"].tick_size

# ---------------------------------------------------------------------------
# Inputs extension — append-only status surface (no cell scoring / election).
# ---------------------------------------------------------------------------

ATR_LEN_STRIKER = 11  # only length this map can supply today

_BAR_DATA = Path(_REPO_ROOT) / "core" / "data" / "bar_data"
_SHA256SUMS = _BAR_DATA / "SHA256SUMS"

# Pins from SHA256SUMS @ HEAD (tracked). CSV bytes are gitignored — presence is
# per-checkout. Land commit for MGC pin: ecfdf59.
_BAR_PINS: dict[str, str] = {
    "6J": "6ab2f8ebb2a33d770df3c547c6bc3f2a0251e025842538654f463c7469fdc6e7",
    "MGC": "88da9f1597daca5c6a118fa4539a117aba5ea4255d81e7475fd7029987caf3f3",
    "MNQ": "6c86f41a17b7dfce05baa205a4147b7504f3ce1eb14a3b03b994aa090fa7e00a",
    "MYM": "24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58",
}

# ENV-1 pool + M6J probe. MES/M2K/MCL/M6A have no bar_data pin at all.
_GRID_PLUS_M6J = ("MES", "MGC", "M2K", "MCL", "M6A", "M6J")

# M6J: not on any AUTOMATION_FRIENDLY product card — venue check closes ATR /
# envelope work for this symbol (no envelope row added).
# Citations: core/firm_rules.py Tradeify cost block (article 10468222 —
# micro FX = M6A+M6E only; NO M6J); Bulenox Rates.pdf NO M6J row; MFFU NO M6J;
# ops/instruments/6J.md ACTIVE/OPEN ("no FRIENDLY firm offers M6J").
# Symbology side-note (not a venue grant): proxy-discipline.md — M6J.FUT does
# not resolve on GLBX.MDP3; live micro code is MJY.
M6J_VENUE_LEGAL = False
M6J_VENUE_NOTE = (
    "UNSCREENABLE-INPUT(venue): M6J absent from all AUTOMATION_FRIENDLY "
    "product sets (Tradeify micro FX = M6A+M6E only; Bulenox/MFFU no M6J row)"
)


def _bar_csv_path(symbol: str) -> Path:
    return _BAR_DATA / f"{symbol}_M15.csv"


def bar_bytes_present(symbol: str) -> bool:
    """True iff the gitignored panel CSV exists in this checkout."""
    return _bar_csv_path(symbol).is_file()


def atr11_input_status(symbol: str) -> str:
    """Named input status for ATR(11) stop-map eligibility (not a cell verdict)."""
    if symbol in _ATR_PTS_RECENT90_ATR11:
        return "COMMITTED(f2_floors.recent_90d)"
    if symbol == "M6J":
        return M6J_VENUE_NOTE
    if symbol in _BAR_PINS:
        if bar_bytes_present(symbol):
            # Present + pinned but no committed atr_median_pts row yet — caller
            # must derive under f2_floors convention and transcribe before use.
            return "PINNED_BYTES_PRESENT_ATR_UNCOMMITTED"
        return (
            f"PENDING: {_bar_csv_path(symbol).as_posix()} absent "
            f"(SHA256SUMS pin {_BAR_PINS[symbol][:12]}…)"
        )
    return (
        f"UNSCREENABLE-INPUT(atr): no core/data/bar_data/{symbol}_M15.csv "
        "pin in SHA256SUMS"
    )


# Frozen inventory for INPUTS_EXTENSION.md / H_A open-cell accounting.
ATR11_INPUT_STATUS: dict[str, str] = {
    "MYM": atr11_input_status("MYM"),
    "MNQ": atr11_input_status("MNQ"),
    **{sym: atr11_input_status(sym) for sym in _GRID_PLUS_M6J},
}


def atr_ticks(mech: Mechanism, symbol: str) -> float | None:
    if mech.atr_len != 11:
        return None
    if symbol not in _ATR_PTS_RECENT90_ATR11:
        return None
    return _ATR_PTS_RECENT90_ATR11[symbol] / INSTRUMENT_SPECS[symbol].tick_size


def stop_ticks(mech: Mechanism, symbol: str) -> float | None:
    at = atr_ticks(mech, symbol)
    if at is None:
        return None
    return mech.sl_atr_mult * at


def map_stop_ticks(stop_ticks_val: float) -> int:
    return min(LADDER_TICKS, key=lambda t: (abs(t - stop_ticks_val), -t))
