"""Provisional #867 plumbing, not acceptance of the venue's disputed rules.

Pin: 768b71bab112a79584d30592dad5e742b76ffdd1. C1's no-lock reading
and C3's intraday-equity breach reading remain assumptions pending Claude's
revision. These examples deliberately expose their effect before any re-MC.
The smoke preflight does not model the soft DLL, 30-calendar-day expiry,
news/price-limit/scalping filters, feed permissions, commissions or session close.
"""

import numpy as np
import pytest

from firm_rules import AUTOMATION_FRIENDLY_PROP_FIRMS, FIRM_RULES
from mc.preflight import EngineUnsupported, assert_engine_ready, firm_kwargs
from mc.simulation import simulate_path

TIER = "FXIFY_Futures_Flex_150K"


def _kwargs(**overrides):
    return firm_kwargs(TIER, allow_provisional_rules=True, **overrides)


def _run(pnls, *, kwargs=None, **overrides):
    return simulate_path(
        np.array(pnls, dtype=float).reshape(-1, 1),
        dd_trigger=1.0, dd_scale=1.0, horizon=len(pnls),
        **(_kwargs() if kwargs is None else kwargs), **overrides,
    )[0]


def test_distinct_futures_identity_and_reported_fields():
    row = FIRM_RULES[TIER]
    assert AUTOMATION_FRIENDLY_PROP_FIRMS["fxify_futures"] == [TIER]
    assert "FXIFY" not in FIRM_RULES
    assert row["rules_source_revision"] == "768b71bab112a79584d30592dad5e742b76ffdd1"
    assert row["starting_balance"] == 150_000
    assert row["micro_contract_cap"] == 100
    assert row["consistency_rule_pct"] == 50.0
    assert row["soft_daily_loss_pct"] == 2.0
    assert row["cost_per_side_usd"] is None
    assert row["weekend_holds"] is False
    assert row["news_trading"] is False  # C2 assumption, not an event filter


@pytest.mark.parametrize("builder", [firm_kwargs, assert_engine_ready])
def test_final_acceptance_held_without_explicit_provisional_opt_in(builder):
    with pytest.raises(ValueError, match="reconcile Claude's revision"):
        builder(TIER)


def test_provisional_smoke_and_original_basis():
    kw = assert_engine_ready(TIER, allow_provisional_rules=True)
    assert kw["starting_equity"] == 150_000.0
    assert kw["profit_target"] == 159_000.0
    assert kw["trailing_dd_pct"] == -0.03
    assert kw["dd_lock_offset_usd"] == 1_000_000.0
    assert kw["dd_type"] == "trailing_locking"
    assert kw["daily_loss_pct"] is None
    assert kw["min_trading_days"] == 2  # consistency-derived assumption
    assert kw["consistency_frac"] is None  # existing Run-1 API
    assert _kwargs(account=100_000)["profit_target"] == 106_000.0


def test_soft_dll_is_not_an_absorbing_daily_bust():
    assert _run([-3_000]) == "horizon_cap"
    assert _run([-4_500]) == "bust_trailing"  # initial floor, inclusive


def test_c1_lock_sensitivity_changes_the_outcome():
    # $156K EOD peak -> $151.5K no-lock floor; then equity falls to $151K.
    assert _run([6_000, -5_000]) == "bust_trailing"
    lock = {**_kwargs(), "dd_lock_offset_usd": 0.0}
    assert _run([6_000, -5_000], kwargs=lock) == "horizon_cap"


def test_fixed_dollar_trail_is_not_percent_of_new_peak():
    # At $154K peak, fixed-$ floor = $149.5K; %-peak floor = $149.38K.
    assert _run([4_000, -4_550]) == "bust_trailing"


def test_c3_intraday_breach_assumption_is_testable():
    assert _run([1_000]) == "horizon_cap"
    assert _run([1_000], intraday_low=np.array([-4_500.0])) == "bust_trailing"


def test_consistency_is_a_soft_pass_gate():
    kw = _kwargs(consistency=0.50)
    assert _run([6_000, 3_000], kwargs=kw) == "horizon_cap"
    assert _run([6_000, 3_000, 3_000], kwargs=kw) == "pass"
    assert _run([4_500, 4_500], kwargs=kw) == "pass"


@pytest.mark.parametrize("allow_unsourced", [False, True])
def test_calendar_inactivity_cannot_silently_become_business_days(allow_unsourced):
    with pytest.raises(EngineUnsupported, match="calendar-day rules and grace"):
        _kwargs(inactivity_off=False, allow_unsourced_inactivity=allow_unsourced)
