"""Quantity-spec parity: the builder's data-only spec equals the book's sizing law.

Card §0.5 item 1 (FROZEN 2026-10-05): the series builder takes the book quantities as
a spec argument (``discovery.remc_series_builder.DEFAULT_QUANTITY_SPEC``). The law it
was built against is frozen below as a fixture, at AUTHORIZED, so this test needs no
``ops`` import. Editing the spec or the fixture alone must fail here.
"""
from __future__ import annotations

import math
from fractions import Fraction

from discovery.remc_series_builder import (
    AS_EXPORTED,
    DEFAULT_QUANTITY_SPEC,
    ZERO,
)

PROTECTED_SCALE = Fraction(2, 5)
ACCOUNT_MICRO_CAP = 80
STRIKER_ADD_PCT = 250


def _scale(mode: str) -> Fraction:
    return PROTECTED_SCALE if mode == "protected" else Fraction(1)


def aegis_base(mode: str) -> int:
    return math.floor(8 * _scale(mode))


def vanguard_base(normal_base: int, mode: str) -> int:
    return math.floor(normal_base * _scale(mode))


def orb_base(mode: str) -> int:
    return 1  # The base is never scaled; protected refuses adds instead.


def striker_base(mode: str, *, risk_dollars: int, per_contract_risk: int) -> int:
    risk_term = Fraction(risk_dollars) * _scale(mode) / per_contract_risk
    cap_term = Fraction(ACCOUNT_MICRO_CAP) / (1 + Fraction(STRIKER_ADD_PCT, 100))
    return min(math.floor(risk_term), math.floor(cap_term))


def test_spec_matches_frozen_quantity_law():
    # Aegis: fixed base 8 normal, floor(8 x 0.40) = 3 protected (TB-S1 (F)).
    assert aegis_base("normal") == 8 and aegis_base("protected") == 3
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"]["normal"] == aegis_base("normal")
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"]["protected"] == aegis_base("protected")
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"] == {"normal": 8, "protected": 3}

    # Vanguard: base 1 or 2, protected floor(b x 0.40) = 0 at either base, so the
    # protected channel takes no entries at all — that is exactly the "zero" rule.
    for base in (1, 2):
        assert vanguard_base(base, "protected") == 0
    assert DEFAULT_QUANTITY_SPEC["vanguard_mgc"] == {
        "normal": AS_EXPORTED,
        "protected": ZERO,
    }

    # Striker (risk-scaled; S-P is the protected capture) and ORB (base 1, protected
    # keeps the base and refuses adds) are both used at their exported quantities.
    assert DEFAULT_QUANTITY_SPEC["dj30_mym_p250"] == {
        "normal": AS_EXPORTED,
        "protected": AS_EXPORTED,
    }
    assert DEFAULT_QUANTITY_SPEC["orb_mnq_v7"] == {
        "normal": AS_EXPORTED,
        "protected": AS_EXPORTED,
    }
    assert orb_base("protected") == orb_base("normal") == 1  # O-P keeps the base
    # Striker's protected size is risk-scaled, not a fixed multiple of one number,
    # which is precisely why the spec reads "as_exported" for the S-P capture.
    assert striker_base("protected", risk_dollars=700, per_contract_risk=100) == 2
    assert striker_base("normal", risk_dollars=700, per_contract_risk=100) == 7
