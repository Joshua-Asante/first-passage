"""Deep-iteration-lane charter §2.2 three-conjunct admission predicate.

Charter (docs/adr/2026-08-16-deep-iteration-lane-charter.md) §2.2:
  (i)   K <= 33 (M-19 Guardian-quality crossing, hard literal)
  (ii)  floor_at_k(K, confirm_years) <= 2.0 (overfit-suspect-zone wall)
  (iii) power >= POWER_MIN (0.50) at the declared target_sr, Gaussian
        approx with se ~= 1/sqrt(years) -- charter's own worked examples:
        target=1.83, K=33, years=6.5 -> floor=1.475, power ~= 0.82 (admissible);
        target at-the-bar (target==floor) -> power == 0.50 (boundary-admissible).

This module does NOT reuse S6/admission_schema.py's mechanism-first predicate
(that one refuses K>=4 against CAP=1.0; a different threshold for a different
lane) -- it reuses only axis_screen.floor_at_k, verbatim, per the charter's own
Rule-0 citation.
"""
from __future__ import annotations

import math

import pytest

from discovery.deep_lane_admission import (
    K_CEILING,
    FLOOR_CEILING,
    DeepLaneAdmission,
    deep_lane_power,
    evaluate_deep_admission,
)
from research_utils.axis_screen import POWER_MIN, floor_at_k


def test_constants_match_charter_literals():
    assert K_CEILING == 33
    assert FLOOR_CEILING == 2.0
    assert POWER_MIN == 0.50


def test_power_at_the_bar_is_exactly_half():
    floor = floor_at_k(33, years=6.5)
    power = deep_lane_power(target_sr=floor, floor_sr=floor, years=6.5)
    assert power == pytest.approx(0.5, abs=1e-9)


def test_power_worked_example_matches_charter_082():
    # Charter §2.2(iii) worked example, verbatim: target 1.83, K=33, 6.5y confirm.
    floor = floor_at_k(33, years=6.5)
    assert floor == pytest.approx(1.475, abs=1e-3)
    power = deep_lane_power(target_sr=1.83, floor_sr=floor, years=6.5)
    assert power == pytest.approx(0.82, abs=0.01)


def test_power_below_floor_is_under_half():
    floor = floor_at_k(33, years=6.5)
    power = deep_lane_power(target_sr=floor - 0.5, floor_sr=floor, years=6.5)
    assert power < 0.5


def test_admits_ge10_k_within_defaults():
    # GO-2's first-campaign point: K~=10, 6.5y confirm, target 1.83 -> admissible.
    result = evaluate_deep_admission(
        DeepLaneAdmission(declared_k=10, confirm_years=6.5, target_sr=1.83)
    )
    assert result.admitted
    assert result.reasons == ()
    assert result.summary["floor_at_k"] == pytest.approx(floor_at_k(10, years=6.5))


def test_refuses_k_above_33_hard_literal():
    # floor_at_k(2000, 6.5y) == 2.0 -- the long-confirm back door the hard K
    # cap exists to block regardless of what floor-only accounting would admit.
    result = evaluate_deep_admission(
        DeepLaneAdmission(declared_k=2000, confirm_years=6.5, target_sr=2.5)
    )
    assert not result.admitted
    assert "K_ABOVE_CEILING" in result.reasons


def test_refuses_floor_above_two_on_short_confirm():
    # K=33 on a 3.25-year confirm -> floor 2.090 (charter's own example).
    result = evaluate_deep_admission(
        DeepLaneAdmission(declared_k=33, confirm_years=3.25, target_sr=3.0)
    )
    assert not result.admitted
    assert "FLOOR_ABOVE_CEILING" in result.reasons
    assert result.summary["floor_at_k"] == pytest.approx(2.090, abs=1e-3)


def test_refuses_underpowered_target():
    floor = floor_at_k(33, years=6.5)
    result = evaluate_deep_admission(
        DeepLaneAdmission(declared_k=33, confirm_years=6.5, target_sr=floor - 0.5)
    )
    assert not result.admitted
    assert "POWER_BELOW_MIN" in result.reasons


def test_boundary_admissible_at_exactly_power_min():
    floor = floor_at_k(33, years=6.5)
    result = evaluate_deep_admission(
        DeepLaneAdmission(declared_k=33, confirm_years=6.5, target_sr=floor)
    )
    assert result.admitted
    assert result.summary["power"] == pytest.approx(0.5, abs=1e-9)


def test_k_must_be_positive_int():
    with pytest.raises(ValueError):
        evaluate_deep_admission(
            DeepLaneAdmission(declared_k=0, confirm_years=6.5, target_sr=1.83)
        )
    with pytest.raises(ValueError):
        evaluate_deep_admission(
            DeepLaneAdmission(declared_k=True, confirm_years=6.5, target_sr=1.83)
        )


def test_confirm_years_must_be_positive():
    with pytest.raises(ValueError):
        evaluate_deep_admission(
            DeepLaneAdmission(declared_k=10, confirm_years=0.0, target_sr=1.83)
        )


def test_all_three_reasons_can_fire_together():
    result = evaluate_deep_admission(
        DeepLaneAdmission(declared_k=2000, confirm_years=0.5, target_sr=0.0)
    )
    assert not result.admitted
    assert set(result.reasons) == {
        "K_ABOVE_CEILING",
        "FLOOR_ABOVE_CEILING",
        "POWER_BELOW_MIN",
    }
