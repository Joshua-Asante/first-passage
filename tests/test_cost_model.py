"""Acceptance + contract tests for lab/discovery/cost_model.py (fleet packet A).

Falsifier H-A: one parameterized model reproduces every frozen per-campaign cost
figure from that campaign's own declared primitives, with no per-campaign branch.
"""
from __future__ import annotations

import pytest

from discovery import cost_model


# --------------------------------------------------------------------------
# §3 acceptance table — frozen published figures
# --------------------------------------------------------------------------


def test_acceptance_cost_mnq_d5_recost_bulenox():
    """cost_mnq / D5-RECOST: Bulenox_100K, px 14769.25, slip 1.0 per_side."""
    result = cost_model.bp_hurdle(
        "MNQ",
        14769.25,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
    )
    assert result.hurdle_4x_bp == pytest.approx(3.0062460856, rel=1e-9)
    assert result.ratio_convention == "edge_over_hurdle_4x"
    assert result.firm_key == "Bulenox_100K"
    assert result.commission_per_side_usd == pytest.approx(0.61)


def test_acceptance_cost_es_h_od_1_passive():
    """cost_es / H-OD-1: comm 3.00, px 1942.125, slip 0.5 total_rt."""
    result = cost_model.bp_hurdle(
        "ES",
        1942.125,
        firm_key="Bulenox_100K",
        slip_ticks=0.5,
        slip_convention="total_rt",
        commission_per_side=3.00,
    )
    assert result.hurdle_4x_bp == pytest.approx(5.046019180021883, rel=1e-9)
    assert result.ratio_convention == "edge_over_hurdle_4x"
    assert result.slip_convention == "total_rt"


def test_acceptance_cost_mgc_disc_camp_0():
    """cost_mgc / DISC-CAMP-0: comm 0.62, px 1355, slip 1.0 per_side (4dp approx)."""
    result = cost_model.bp_hurdle(
        "MGC",
        1355.0,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
        commission_per_side=0.62,
    )
    assert result.hurdle_4x_bp == pytest.approx(9.5638, rel=1e-4)


def test_acceptance_mym_3fps_tradeify_comm():
    """MYM-3FPS: comm 0.91, px 34312.0, slip 1.0 per_side."""
    result = cost_model.bp_hurdle(
        "MYM",
        34312.0,
        firm_key="Tradeify_Select_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
        commission_per_side=0.91,
    )
    assert result.hurdle_4x_bp == pytest.approx(6.57495919794824, rel=1e-9)
    # MYM tick_size is 1.00 — not MNQ's 0.25
    assert cost_model.INSTRUMENT_SPECS["MYM"].tick_size == 1.0
    assert cost_model.INSTRUMENT_SPECS["MYM"].tick_value == 0.50


def test_acceptance_ng_eia_1_declared_comm():
    """NG-EIA-1: comm 0.61, px 2.868, slip 1.0 per_side (campaign-declared)."""
    result = cost_model.bp_hurdle(
        "NG",
        2.868,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
        commission_per_side=0.61,
    )
    assert result.hurdle_4x_bp == pytest.approx(29.595536959553694, rel=1e-9)


def test_scale_invariance_ng_mng_slippage_term():
    """NG (mult 10000) and MNG (mult 1000) return the SAME slippage term (points)."""
    ng = cost_model.bp_hurdle(
        "NG",
        2.868,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
        commission_per_side=0.61,
    )
    mng = cost_model.bp_hurdle(
        "MNG",
        2.868,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
        commission_per_side=0.61,
    )
    assert ng.slip_rt_pt == pytest.approx(mng.slip_rt_pt, rel=1e-12)
    assert ng.slip_rt_pt == pytest.approx(0.002, rel=1e-12)


# --------------------------------------------------------------------------
# Contract: firm_key, slip_convention, instrument gaps, no cross-unit
# --------------------------------------------------------------------------


def test_firm_key_required_no_default():
    with pytest.raises(TypeError):
        cost_model.bp_hurdle(
            "MNQ",
            14769.25,
            slip_ticks=1.0,
            slip_convention="per_side",
        )


def test_unknown_firm_key_raises():
    with pytest.raises((KeyError, ValueError), match="NoSuchFirm|unknown|not in"):
        cost_model.bp_hurdle(
            "MNQ",
            14769.25,
            firm_key="NoSuchFirm_100K",
            slip_ticks=1.0,
            slip_convention="per_side",
        )


def test_slip_convention_required_no_default():
    with pytest.raises(TypeError):
        cost_model.bp_hurdle(
            "MNQ",
            14769.25,
            firm_key="Bulenox_100K",
            slip_ticks=1.0,
        )


def test_invalid_slip_convention_raises():
    with pytest.raises(ValueError, match="slip_convention"):
        cost_model.bp_hurdle(
            "MNQ",
            14769.25,
            firm_key="Bulenox_100K",
            slip_ticks=1.0,
            slip_convention="per_round_trip",
        )


@pytest.mark.parametrize("instrument", ["ZN", "ZB", "ZF", "CL", "NG", "6E"])
def test_no_commission_row_instruments_raise_naming_gap(instrument):
    with pytest.raises(ValueError, match=instrument):
        cost_model.resolve_commission("Bulenox_100K", instrument)


def test_ng_lookup_does_not_substitute_index_micro_rate():
    """Lookup path must refuse NG — never silently apply 0.61 index-micro."""
    with pytest.raises(ValueError, match="NG"):
        cost_model.bp_hurdle(
            "NG",
            2.868,
            firm_key="Bulenox_100K",
            slip_ticks=1.0,
            slip_convention="per_side",
        )


def test_mym_tradeify_firm_lookup_matches_declared_0_91():
    """Tradeify index-micro row is 0.91 — MYM lookup must not need an override."""
    result = cost_model.bp_hurdle(
        "MYM",
        34312.0,
        firm_key="Tradeify_Select_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
    )
    assert result.commission_per_side_usd == pytest.approx(0.91)
    assert result.hurdle_4x_bp == pytest.approx(6.57495919794824, rel=1e-9)


def test_r_hurdle_is_mean_of_ratios_not_rt_over_median():
    """mean(rt_pt / range_i), not rt_pt / median(range)."""
    ranges = [10.0, 20.0, 30.0]  # median 20; mean-of-ratios != rt/median
    result = cost_model.r_hurdle(
        "MNQ",
        ranges,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
    )
    rt_pt = result.rt_pt
    mean_of_ratios = sum(rt_pt / r for r in ranges) / len(ranges)
    wrong_form = rt_pt / 20.0
    assert result.mean_cost_R == pytest.approx(mean_of_ratios, rel=1e-12)
    assert result.mean_cost_R != pytest.approx(wrong_form, rel=1e-6)
    assert result.ratio_convention == "edge_over_mean_cost_R"
    assert wrong_form < mean_of_ratios


def test_no_r_bp_conversion():
    with pytest.raises(ValueError, match=r"R.*bp|bp.*R|cross-unit|No .*conversion"):
        cost_model.convert_r_to_bp(0.01, price=15000.0, instrument="MNQ")


def test_per_side_vs_total_rt_differ_by_four_on_same_slip_number():
    """Conflating conventions is a 4x slip error — model must keep them distinct."""
    per_side = cost_model.bp_hurdle(
        "MNQ",
        14769.25,
        firm_key="Bulenox_100K",
        slip_ticks=1.0,
        slip_convention="per_side",
    )
    assert per_side.slip_rt_usd == pytest.approx(2.0 * 1.0 * 0.50)  # $1.00 RT
    total = cost_model.rt_cost_usd(
        "MNQ",
        commission_per_side=0.61,
        slip_ticks=1.0,
        slip_convention="total_rt",
    )
    assert total == pytest.approx(2 * 0.61 + 1.0 * 0.50)


def test_mym_tick_size_is_not_mnq_copy():
    assert cost_model.INSTRUMENT_SPECS["MYM"].tick_size != cost_model.INSTRUMENT_SPECS["MNQ"].tick_size
    assert cost_model.INSTRUMENT_SPECS["MYM"].tick_size == 1.0
    assert cost_model.INSTRUMENT_SPECS["MNQ"].tick_size == 0.25


@pytest.mark.parametrize("symbol", sorted(cost_model.INSTRUMENT_SPECS))
def test_tick_value_invariant_holds_for_every_spec(symbol):
    """`tick_value` is stored but derivable as multiplier * tick_size.

    A redundant field with no invariant guard desyncs silently on a future spec
    edit, and every hurdle here is linear in tick_value — so a desync would move
    figures without failing any acceptance test, since those pin one instrument
    each. Guard the whole table, not a spot-check.
    """
    spec = cost_model.INSTRUMENT_SPECS[symbol]
    assert spec.tick_value == pytest.approx(
        spec.multiplier * spec.tick_size, rel=1e-12
    ), f"{symbol}: tick_value {spec.tick_value} != {spec.multiplier} * {spec.tick_size}"
