"""Quantity-spec parity: the builder's data-only spec equals the book's sizing law.

Card §0.5 item 1 (FROZEN 2026-10-05): ``lab`` may not import ``ops``, so the series
builder takes the book quantities as a spec argument
(``discovery.remc_series_builder.DEFAULT_QUANTITY_SPEC``). This test — which MAY
import both layers, because ``tests/`` is contract-exempt (ADR 2026-06-05 §8 Q-c) —
is the single seam that keeps the spec and ``ops/c1_rail/book_policy.py`` one
source of truth. Editing one without the other must fail here.
"""
from __future__ import annotations

from c1_rail.book_policy import candidate_book_protection_policy, entry_quantities
from c1_signal_daemon.book_protocol import Mode

from discovery.remc_series_builder import (
    AS_EXPORTED,
    DEFAULT_QUANTITY_SPEC,
    ZERO,
)

AUTHORIZED = "AUTHORIZED"


def test_spec_matches_book_policy():
    policy = candidate_book_protection_policy()

    # Aegis: fixed base 8 normal, floor(8 x 0.40) = 3 protected (TB-S1 (F)).
    aegis_normal = entry_quantities(
        "aegis_6j", mode=Mode.NORMAL, policy=policy, lifecycle_tier=AUTHORIZED
    )[0]
    aegis_protected = entry_quantities(
        "aegis_6j", mode=Mode.PROTECTED, policy=policy, lifecycle_tier=AUTHORIZED
    )[0]
    assert aegis_normal == 8 and aegis_protected == 3
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"]["normal"] == aegis_normal
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"]["protected"] == aegis_protected
    assert DEFAULT_QUANTITY_SPEC["aegis_6j"] == {"normal": 8, "protected": 3}

    # Vanguard: base 1 or 2, protected floor(b x 0.40) = 0 at either base, so the
    # protected channel takes no entries at all — that is exactly the "zero" rule.
    for base in (1, 2):
        assert (
            entry_quantities(
                "vanguard_mgc",
                normal_base=base,
                mode=Mode.PROTECTED,
                policy=policy,
                lifecycle_tier=AUTHORIZED,
            )[0]
            == 0
        )
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
    orb_protected = entry_quantities(
        "orb_mnq_v7", mode=Mode.PROTECTED, policy=policy, lifecycle_tier=AUTHORIZED
    )[0]
    orb_normal = entry_quantities(
        "orb_mnq_v7", mode=Mode.NORMAL, policy=policy, lifecycle_tier=AUTHORIZED
    )[0]
    assert orb_protected == orb_normal == 1  # O-P keeps the base
    # Striker's protected size is risk-scaled, not a fixed multiple of one number,
    # which is precisely why the spec reads "as_exported" for the S-P capture.
    assert (
        entry_quantities(
            "dj30_mym_p250",
            mode=Mode.PROTECTED,
            policy=policy,
            lifecycle_tier=AUTHORIZED,
            risk_dollars=700,
            per_contract_risk=100,
            cap_alloc=80,
        )[0]
        == 2
    )
    assert (
        entry_quantities(
            "dj30_mym_p250",
            mode=Mode.NORMAL,
            policy=policy,
            lifecycle_tier=AUTHORIZED,
            risk_dollars=700,
            per_contract_risk=100,
            cap_alloc=80,
        )[0]
        == 7
    )
