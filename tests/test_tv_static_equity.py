"""Acceptance tests for research_utils.tv_static_equity (MSL P2 W-C)."""
from __future__ import annotations

from pathlib import Path

import pytest

from research_utils.tv_static_equity import (
    MNQ_COMMISSION_PER_SIDE,
    MNQ_POINT_VALUE_USD,
    static_equity_recompute,
)

FIXTURES = (
    Path(__file__).resolve().parents[1]
    / "lab"
    / "research_utils"
    / "fixtures"
    / "tv_static_equity"
)

# Hand-recomputed MNQ static nets for static_match_mnq.csv
_EXPECTED_NETS = (18.18, -23.64)


def test_hand_recomputed_known_export_matches():
    result = static_equity_recompute(
        FIXTURES / "static_match_mnq.csv",
        point_value_usd=MNQ_POINT_VALUE_USD,
        commission_per_side=MNQ_COMMISSION_PER_SIDE,
    )
    assert result["n_legs"] == 2
    assert result["ok_within_1usd"] is True
    assert result["compounded_divergent"] is False
    assert result["max_abs_delta"] < 1.0
    assert result["tv_net_sum"] == pytest.approx(sum(_EXPECTED_NETS))
    assert result["recompute_net_sum"] == pytest.approx(sum(_EXPECTED_NETS))
    legs = result["legs"]
    assert list(legs["recompute_net"]) == pytest.approx(list(_EXPECTED_NETS))
    assert list(legs["static_equity"]) == pytest.approx(
        [18.18, 18.18 + (-23.64)]
    )


def test_compounded_fixture_flagged_divergent():
    result = static_equity_recompute(
        FIXTURES / "compounded_divergent_mnq.csv",
        point_value_usd=MNQ_POINT_VALUE_USD,
        commission_per_side=MNQ_COMMISSION_PER_SIDE,
    )
    assert result["n_legs"] == 2
    assert result["compounded_divergent"] is True
    assert result["ok_within_1usd"] is False
    assert result["max_abs_delta"] >= 1.0
    # Static recompute still matches hand math; TV nets diverge.
    assert result["recompute_net_sum"] == pytest.approx(sum(_EXPECTED_NETS))
    assert result["tv_net_sum"] == pytest.approx(27.50 + (-31.00))


def test_point_value_and_commission_are_required():
    with pytest.raises(TypeError):
        static_equity_recompute(FIXTURES / "static_match_mnq.csv")  # type: ignore[call-arg]
