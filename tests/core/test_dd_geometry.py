"""Tests for dd_geometry — the concept-not-constant protection registry.

Anchor: docs/adr/2026-07-13-dd-protection-concept-not-constant.md
Ratified recommendation:
docs/briefs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md §3.
FXIFY-C2 seed retirement: docs/adr/2026-07-22-challenge-era-substrate-retirement.md
Phase 1.

Load-bearing invariants pinned here:
  1. No FXIFY-C2 seed — registry starts empty; no import-time pin to
     dd_protection (substrate Phase 1).
  2. Registry isolation — adding a prop instance row cannot move
     dd_protection module constants.
  3. No silent defaults — unknown instance keys and unknown dd_types raise;
     nothing invents a default policy.
  4. dd_type coverage — every dd_type in FIRM_RULES maps to a reference_mode
     (a new firm class cannot land without a geometry decision).
"""

import pytest

import dd_geometry
import dd_protection
from dd_geometry import (
    POLICY_REGISTRY,
    ProtectionPolicy,
    protection_policy,
    reference_mode_for_dd_type,
)
from firm_rules import FIRM_RULES


class TestSeedRetirement:
    def test_module_imports_cleanly(self):
        assert isinstance(POLICY_REGISTRY, dict)

    def test_fxify_c2_seed_absent(self):
        assert "FXIFY-C2" not in POLICY_REGISTRY
        assert POLICY_REGISTRY == {}

    def test_dd_geometry_does_not_import_dd_protection(self):
        # Seed retirement removed the one-way pin import; keep the edge gone
        # so the registry never re-couples to the historical fixture.
        from pathlib import Path

        src = Path(dd_geometry.__file__).read_text(encoding="utf-8")
        for line in src.splitlines():
            code = line.split("#", 1)[0]
            assert "import dd_protection" not in code, (
                "dd_geometry must not import dd_protection after FXIFY-C2 "
                "seed retirement (ADR 2026-07-22 Phase 1)"
            )

    def test_dd_protection_does_not_import_dd_geometry(self):
        # Anchor path stays byte-identical without this module.
        from pathlib import Path

        src = Path(dd_protection.__file__).read_text(encoding="utf-8")
        for line in src.splitlines():
            code = line.split("#", 1)[0]
            assert "import dd_geometry" not in code, (
                "dd_protection must never import dd_geometry "
                "(anchor path stays byte-identical without this module)"
            )


class TestRegistryIsolation:
    def test_adding_prop_instance_leaves_constants_untouched(self):
        dummy = ProtectionPolicy(
            reference_mode="locking",
            trigger=0.009,
            scale=0.40,
            provenance="TEST-ONLY dummy — never a real admission",
        )
        POLICY_REGISTRY["DUMMY@Tradeify_Select_100K"] = dummy
        try:
            assert protection_policy("DUMMY@Tradeify_Select_100K") is dummy
            assert dd_protection.DD_TRIGGER == 0.015
            assert dd_protection.DD_SCALE == 0.40
        finally:
            del POLICY_REGISTRY["DUMMY@Tradeify_Select_100K"]

    def test_policy_rows_are_frozen(self):
        row = ProtectionPolicy(
            reference_mode="static",
            trigger=0.015,
            scale=0.40,
            provenance="TEST-ONLY frozen-row check",
        )
        POLICY_REGISTRY["TEMP@frozen"] = row
        try:
            with pytest.raises(Exception):  # dataclasses.FrozenInstanceError
                POLICY_REGISTRY["TEMP@frozen"].trigger = 0.02
        finally:
            del POLICY_REGISTRY["TEMP@frozen"]

    def test_policy_validation_rejects_bad_values(self):
        with pytest.raises(ValueError):
            ProtectionPolicy("static", 1.5, 0.40, "trigger not a fraction")
        with pytest.raises(ValueError):
            ProtectionPolicy("static", 0.015, 1.4, "scale > 1")
        with pytest.raises(ValueError):
            ProtectionPolicy("intraday", 0.015, 0.40, "unknown reference_mode")


class TestNoSilentDefaults:
    def test_unknown_instance_raises_not_defaults(self):
        with pytest.raises(KeyError, match="never invent a default"):
            protection_policy("NEWPORT@Bulenox_100K")

    def test_unknown_dd_type_raises_not_static(self):
        with pytest.raises(KeyError, match="Unknown dd_type"):
            reference_mode_for_dd_type("intraday_trailing_fixed_usd")


class TestDdTypeCoverage:
    def test_every_firm_rules_dd_type_maps(self):
        # A new firm class (new dd_type) must not land without a geometry
        # decision here — this is the guard that makes that structural.
        for tier, cfg in FIRM_RULES.items():
            mode = reference_mode_for_dd_type(cfg["dd_type"])
            assert mode in dd_geometry.REFERENCE_MODES, tier

    def test_known_mappings(self):
        assert reference_mode_for_dd_type("static") == "static"
        assert reference_mode_for_dd_type("trailing") == "trailing"
        assert reference_mode_for_dd_type("trailing_locking") == "locking"
