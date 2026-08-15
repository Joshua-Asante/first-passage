"""Synthetic Appendix-A alert intents + expected CrossTrade payloads (P5 §2-E).

End-to-end sim firing is operator-owned; these fixtures hold source intent for
offline translation tests and future golden-path replay.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GoldenPathFixture:
    leg: str
    primitive: str
    appendix_a: dict[str, Any]
    account: str = "sim101"
    secret_key: str = "test-secret-key"
    # Post-translation intent (side / qty / price logic / flat-or-position)
    expected_side: str | None = None
    expected_qty: int | None = None
    expected_flat: bool | None = None


INSTRUMENTS = {
    "dj30_mym": "MYM1!",
    "nas_mnq": "MNQ1!",
    "aegis_6j": "6J1!",
    "guardian_mgc": "MGC1!",
}


def _entry(leg: str, instrument: str, qty: int, sl: float, tp: float) -> GoldenPathFixture:
    strategy = {"dj30_mym": "striker", "nas_mnq": "nas100", "aegis_6j": "aegis", "guardian_mgc": "guardian"}[leg]
    return GoldenPathFixture(
        leg=leg,
        primitive="base_entry",
        appendix_a={
            "strategy": strategy,
            "action": "buy",
            "symbol": instrument,
            "leg": "entry",
            "qty": qty,
            "sl": sl,
            "tp": tp,
            "id": f"{strategy}-entry-202607061500",
        },
        expected_side="buy",
        expected_qty=qty,
        expected_flat=False,
    )


def _pyramid_add(leg: str, instrument: str, qty: int, sl: float) -> GoldenPathFixture:
    strategy = "striker" if leg == "dj30_mym" else "nas100"
    return GoldenPathFixture(
        leg=leg,
        primitive="pyramid_add",
        appendix_a={
            "strategy": strategy,
            "action": "buy",
            "symbol": instrument,
            "leg": "add",
            "qty": qty,
            "sl": sl,
            "id": f"{strategy}-add-202607061530",
        },
        expected_side="buy",
        expected_qty=qty,
        expected_flat=False,
    )


def _exit_close(leg: str, instrument: str, qty: int) -> GoldenPathFixture:
    strategy = {
        "dj30_mym": "striker",
        "nas_mnq": "nas100",
        "aegis_6j": "aegis",
        "guardian_mgc": "guardian",
    }[leg]
    return GoldenPathFixture(
        leg=leg,
        primitive="session_end_flat",
        appendix_a={
            "strategy": strategy,
            "action": "close",
            "symbol": instrument,
            "leg": "exit",
            "qty": qty,
            "id": f"{strategy}-exit-202607061700",
        },
        expected_side="close",
        expected_qty=qty,
        expected_flat=True,
    )


ALL_FIXTURES: list[GoldenPathFixture] = [
    _entry("dj30_mym", INSTRUMENTS["dj30_mym"], 17, 42100.0, 42500.0),
    _pyramid_add("dj30_mym", INSTRUMENTS["dj30_mym"], 127, 42150.0),
    _entry("nas_mnq", INSTRUMENTS["nas_mnq"], 5, 18500.0, 18700.0),
    _pyramid_add("nas_mnq", INSTRUMENTS["nas_mnq"], 50, 18550.0),
    _entry("aegis_6j", INSTRUMENTS["aegis_6j"], 8, 0.00645, 0.00655),
    _entry("guardian_mgc", INSTRUMENTS["guardian_mgc"], 3, 2350.0, 2380.0),
    _exit_close("dj30_mym", INSTRUMENTS["dj30_mym"], 144),
    _exit_close("nas_mnq", INSTRUMENTS["nas_mnq"], 55),
    _exit_close("aegis_6j", INSTRUMENTS["aegis_6j"], 8),
    _exit_close("guardian_mgc", INSTRUMENTS["guardian_mgc"], 3),
]

# Primitives covered only via translator defaults (no distinct Appendix-A leg):
# fixed_stop, atr_trail_update, eod_flat, m6j_side_inversion — see matrix DEFAULTABLE-SAFE / N/A rows.
