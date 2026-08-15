"""Tests for the strategy authorization-lifecycle multiplier (Phase-2 code, items 1-2).

Anchors:
  docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md (Accepted, Call 2)
  docs/methodology/strategy_lifecycle.md (canonical owner; the ratified tier ladder)

Covers: the tier ladder + state loader (core/lifecycle.py) and its wiring into
dd_protection.calculate_protection as the risk_pct-layer haircut
`BASE_RISK x DD_SCALE x lifecycle`, with axis-separation (ADR section-4 trigger 3)
and behavior-neutrality (default 1.0x == pre-lifecycle behavior) pinned.
"""

import json

import pytest


class TestTierLadder:
    def test_ladder_pins_ratified_values(self):
        # The four ratified multipliers (strategy_lifecycle.md Call 2). A drift here
        # is a governance change, not a code tweak — it must fail loudly.
        from lifecycle import TIER_MULTIPLIER

        assert TIER_MULTIPLIER == {
            "AUTHORIZED": 1.00,
            "WATCH-1": 0.50,
            "WATCH-2": 0.25,
            "RETIRED": 0.00,
        }


class TestStateLoader:
    def test_defaults_to_authorized_when_no_state_file(self, tmp_path, monkeypatch):
        # No state file == the live reality today: every leg AUTHORIZED @ 1.0x.
        import lifecycle

        monkeypatch.setattr(lifecycle, "STATE_FILE", tmp_path / "nonexistent.json")
        keys = ["Guardian", "Striker", "Aegis", "Striker NAS100"]
        assert lifecycle.get_lifecycle_multipliers(keys) == {k: 1.0 for k in keys}

    def test_maps_declared_tier_and_defaults_the_rest(self, tmp_path, monkeypatch):
        import lifecycle

        sf = tmp_path / "lifecycle_state.json"
        sf.write_text(json.dumps({"Guardian": "WATCH-1"}))
        monkeypatch.setattr(lifecycle, "STATE_FILE", sf)
        mult = lifecycle.get_lifecycle_multipliers(["Guardian", "Aegis"])
        assert mult["Guardian"] == 0.50
        assert mult["Aegis"] == 1.00  # unlisted -> AUTHORIZED

    def test_unknown_tier_raises_no_silent_fallback(self, tmp_path, monkeypatch):
        # Repo philosophy: a bad tier string must hard-error, never silently size.
        import lifecycle

        sf = tmp_path / "lifecycle_state.json"
        sf.write_text(json.dumps({"Guardian": "SORTA-OK"}))
        monkeypatch.setattr(lifecycle, "STATE_FILE", sf)
        with pytest.raises(ValueError):
            lifecycle.get_lifecycle_multipliers(["Guardian"])


class TestDDProtectionIntegration:
    def test_default_lifecycle_behavior_neutral_no_dd(self):
        # Regression guard: no lifecycle arg + no DD => scaled_risk IS BASE_RISK
        # (x1.0 is exact in IEEE754, so byte-identical to pre-lifecycle behavior).
        from dd_protection import calculate_protection, BASE_RISK

        result = calculate_protection(equity=200_000.0, peak=200_000.0)
        assert result["scaled_risk"] == BASE_RISK

    def test_default_lifecycle_behavior_neutral_with_dd(self):
        # Regression guard: no lifecycle arg + DD triggered => BASE_RISK x DD_SCALE,
        # unchanged from the pre-lifecycle single-factor path.
        from dd_protection import calculate_protection, BASE_RISK, DD_SCALE

        equity = 200_000.0 * (1.0 - 0.020)  # 2% DD -> triggers
        result = calculate_protection(equity=equity, peak=200_000.0)
        assert result["dd_triggered"] is True
        assert result["scaled_risk"] == {k: v * DD_SCALE for k, v in BASE_RISK.items()}

    def test_lifecycle_haircut_applied_without_dd(self):
        from dd_protection import calculate_protection, BASE_RISK

        lifecycle = {k: 1.0 for k in BASE_RISK}
        lifecycle["Guardian"] = 0.50  # WATCH-1
        result = calculate_protection(equity=200_000.0, peak=200_000.0, lifecycle=lifecycle)
        assert result["scaled_risk"]["Guardian"] == pytest.approx(BASE_RISK["Guardian"] * 0.50)
        assert result["scaled_risk"]["Aegis"] == pytest.approx(BASE_RISK["Aegis"])

    def test_lifecycle_compounds_multiplicatively_with_dd_scale(self):
        # The ratified 0.20x: a WATCH-1 leg (0.50x) simultaneously in DD (0.40x).
        from dd_protection import calculate_protection, BASE_RISK

        equity = 200_000.0 * (1.0 - 0.020)  # DD triggered
        lifecycle = {k: 1.0 for k in BASE_RISK}
        lifecycle["Guardian"] = 0.50
        result = calculate_protection(equity=equity, peak=200_000.0, lifecycle=lifecycle)
        assert result["dd_triggered"] is True
        assert result["scaled_risk"]["Guardian"] == pytest.approx(BASE_RISK["Guardian"] * 0.20)

    def test_retired_tier_zeroes_risk(self):
        from dd_protection import calculate_protection, BASE_RISK

        lifecycle = {k: 1.0 for k in BASE_RISK}
        lifecycle["Guardian"] = 0.0  # RETIRED
        result = calculate_protection(equity=200_000.0, peak=200_000.0, lifecycle=lifecycle)
        assert result["scaled_risk"]["Guardian"] == 0.0


class TestAxisSeparation:
    """ADR section-4 trigger 3: a lifecycle tier change must NEVER mutate a LOCKED
    constant. The lifecycle factor multiplies against BASE_RISK/DD_SCALE/DD_TRIGGER;
    it never edits them."""

    def test_tier_change_leaves_locked_constants_byte_identical(self):
        import dd_protection
        from dd_protection import calculate_protection, BASE_RISK

        base_snapshot = dict(BASE_RISK)
        equity = 200_000.0 * (1.0 - 0.020)
        lifecycle = {k: 1.0 for k in BASE_RISK}
        lifecycle["Guardian"] = 0.25  # WATCH-2
        lifecycle["Aegis"] = 0.0      # RETIRED
        calculate_protection(equity=equity, peak=200_000.0, lifecycle=lifecycle)
        # Locked constants untouched by the tier change.
        assert dd_protection.BASE_RISK == base_snapshot
        assert dd_protection.DD_SCALE == 0.40
        assert dd_protection.DD_TRIGGER == 0.015

    def test_mvd_spec_pin_still_holds(self):
        # Wiring lifecycle in must not trip the dd_protection MVD self-check.
        import dd_protection

        dd_protection._validate_protection_rule()  # raises on drift; must be silent


class TestCall4BetaDeathControl:
    """Call 4 (ratified): 2-of-4 legs de-authorized -> soft flag; 3-of-4 -> portfolio
    de-risk 0.50x + operator GO/NO-GO. "De-authorized" = any tier below AUTHORIZED
    (multiplier < 1.0), so RETIRED counts. The 0.50x is a PORTFOLIO-level beta de-risk
    applied on top of per-leg lifecycle (Call 4 is the shared-beta-death defense)."""

    def test_constants_pinned(self):
        import lifecycle

        assert lifecycle.BETA_SOFT_FLAG_COUNT == 2
        assert lifecycle.BETA_DEATH_COUNT == 3
        assert lifecycle.BETA_DEATH_DERISK == 0.50

    def test_no_flag_with_one_leg_de_authorized(self):
        from lifecycle import beta_death_assessment

        a = beta_death_assessment({"A": 0.50, "B": 1.0, "C": 1.0, "D": 1.0})
        assert a["watch_count"] == 1
        assert a["soft_flag"] is False
        assert a["beta_death"] is False
        assert a["portfolio_multiplier"] == 1.0
        assert a["operator_go_nogo"] is False

    def test_soft_flag_at_two_de_authorized(self):
        from lifecycle import beta_death_assessment

        a = beta_death_assessment({"A": 0.50, "B": 0.25, "C": 1.0, "D": 1.0})
        assert a["watch_count"] == 2
        assert a["soft_flag"] is True
        assert a["beta_death"] is False
        assert a["portfolio_multiplier"] == 1.0  # soft flag does NOT auto de-risk
        assert a["operator_go_nogo"] is False

    def test_beta_death_at_three_de_authorized(self):
        from lifecycle import beta_death_assessment

        a = beta_death_assessment({"A": 0.50, "B": 0.50, "C": 0.25, "D": 1.0})
        assert a["watch_count"] == 3
        assert a["soft_flag"] is True
        assert a["beta_death"] is True
        assert a["portfolio_multiplier"] == 0.50  # autonomous portfolio de-risk
        assert a["operator_go_nogo"] is True       # GO/NO-GO on FULL shutdown (not auto)

    def test_retired_leg_counts_toward_beta_death(self):
        # A RETIRED (0.0) leg is maximally degraded -> counts as correlated-degradation evidence.
        from lifecycle import beta_death_assessment

        a = beta_death_assessment({"A": 0.0, "B": 0.50, "C": 0.25, "D": 1.0})
        assert a["watch_count"] == 3
        assert a["beta_death"] is True

    def test_effective_multipliers_fold_beta_derisk_when_3of4(self):
        # get_effective_multipliers = per-leg lifecycle x portfolio beta multiplier.
        # 3 legs de-authorized -> the whole book takes an extra 0.50x.
        import lifecycle

        state = {"Guardian": "WATCH-1", "Striker": "WATCH-1", "Aegis": "WATCH-2"}
        # (Striker NAS100 unlisted -> AUTHORIZED)
        eff = lifecycle.get_effective_multipliers(
            ["Guardian", "Striker", "Aegis", "Striker NAS100"],
            _state_override=state,
        )
        assert eff["Guardian"] == pytest.approx(0.50 * 0.50)          # WATCH-1 x beta
        assert eff["Aegis"] == pytest.approx(0.25 * 0.50)             # WATCH-2 x beta
        assert eff["Striker NAS100"] == pytest.approx(1.00 * 0.50)    # AUTHORIZED x beta

    def test_effective_multipliers_no_beta_below_three(self):
        import lifecycle

        state = {"Guardian": "WATCH-1", "Striker": "WATCH-2"}  # only 2 -> no beta de-risk
        eff = lifecycle.get_effective_multipliers(
            ["Guardian", "Striker", "Aegis", "Striker NAS100"],
            _state_override=state,
        )
        assert eff["Guardian"] == pytest.approx(0.50)
        assert eff["Striker"] == pytest.approx(0.25)
        assert eff["Aegis"] == pytest.approx(1.00)


class TestCall1DecaySignal:
    """Call 1 (ratified): rolling live PF < [baseline PF - 1.0*sigma] for 2 consecutive
    windows -> demote one tier. Autonomous demotion caps at WATCH-2 (WATCH-2 -> RETIRED
    is operator-gated, Call 5)."""

    def test_breach_when_below_floor(self):
        from lifecycle import decay_breach

        # baseline 3.0, sigma 0.5, k=1.0 -> floor 2.5; PF 2.4 is below.
        assert decay_breach(rolling_pf=2.4, baseline_pf=3.0, pf_sigma=0.5) is True

    def test_no_breach_at_floor_boundary(self):
        from lifecycle import decay_breach

        # PF exactly at floor (2.5) is NOT "below" -> no breach (strict <).
        assert decay_breach(rolling_pf=2.5, baseline_pf=3.0, pf_sigma=0.5) is False

    def test_no_breach_when_healthy(self):
        from lifecycle import decay_breach

        assert decay_breach(rolling_pf=3.1, baseline_pf=3.0, pf_sigma=0.5) is False

    def test_k_sigma_is_tunable(self):
        from lifecycle import decay_breach

        # k=1.0 floor 2.5 -> 2.6 not a breach; a laxer k would move the floor.
        assert decay_breach(2.6, 3.0, 0.5, k_sigma=1.0) is False
        assert decay_breach(2.6, 3.0, 0.5, k_sigma=0.5) is True  # floor 2.75

    def test_next_tier_down_full_ladder(self):
        from lifecycle import next_tier_down

        assert next_tier_down("AUTHORIZED") == "WATCH-1"
        assert next_tier_down("WATCH-1") == "WATCH-2"
        assert next_tier_down("WATCH-2") == "RETIRED"
        assert next_tier_down("RETIRED") == "RETIRED"  # floor

    def test_autonomous_demote_caps_at_watch2(self):
        # Call 5: WATCH-2 -> RETIRED is operator-gated; automation may never auto-RETIRE.
        from lifecycle import autonomous_demote

        assert autonomous_demote("AUTHORIZED") == "WATCH-1"
        assert autonomous_demote("WATCH-1") == "WATCH-2"
        assert autonomous_demote("WATCH-2") == "WATCH-2"  # no autonomous RETIRE
