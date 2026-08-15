"""Permanent consistency guard for the historical-challenge fixture.

Historical MC / dd_protection challenge constants derive from
``core/historical_challenge.py`` (substrate Phase 4). The FXIFY
``FIRM_RULES`` row, ``ACTIVE_FIRM``, and ``BASELINE_BALANCE`` are deleted.

This test fails the moment any consumer's derived constant drifts from the
frozen fixture.
"""

import dd_protection
import firm_rules
import historical_challenge as hc
import portfolio_mc


def test_fxify_row_and_active_firm_removed():
    assert "FXIFY" not in firm_rules.FIRM_RULES
    assert not hasattr(firm_rules, "ACTIVE_FIRM")
    assert not hasattr(firm_rules, "BASELINE_BALANCE")


def test_live_c1_tier_still_in_firm_rules():
    assert "Tradeify_Select_100K" in firm_rules.FIRM_RULES


def test_portfolio_mc_constants_match_historical_fixture():
    assert portfolio_mc.STARTING_EQUITY == hc.STARTING_EQUITY
    assert portfolio_mc.PROFIT_TARGET == hc.PROFIT_TARGET_ABS
    assert portfolio_mc.DAILY_LOSS_PCT == hc.DAILY_LOSS_PCT_SIGNED
    assert portfolio_mc.STATIC_DD_PCT == hc.STATIC_DD_PCT_SIGNED
    assert portfolio_mc.MIN_TRADING_DAYS == hc.MIN_TRADING_DAYS
    assert portfolio_mc.INACTIVITY_LIMIT == hc.INACTIVITY_LIMIT


def test_dd_protection_constants_match_historical_fixture():
    assert dd_protection.STARTING_EQUITY == hc.STARTING_EQUITY
    assert dd_protection.PROFIT_TARGET == hc.PROFIT_TARGET_FRAC
    assert dd_protection.DAILY_LOSS_LIMIT == hc.DAILY_LOSS_LIMIT_FRAC
    assert dd_protection.STATIC_DD_LIMIT == hc.STATIC_DD_LIMIT_FRAC


def test_locked_allocations_agree_across_consumers():
    expected = firm_rules._BASE_RISK
    dd_allocations = {
        "guardian": dd_protection.BASE_RISK["Guardian"],
        "striker": dd_protection.BASE_RISK["Striker"],
        "aegis": dd_protection.BASE_RISK["Aegis"],
        "striker_nas100": dd_protection.BASE_RISK["Striker NAS100"],
    }

    assert portfolio_mc.ALLOCATIONS == expected == dd_allocations
    assert dd_protection.BASE_RISK == firm_rules.base_risk_display()
    assert portfolio_mc.PINE_SHRINK_ALLOCATIONS == expected


def test_sweep_reg_and_ga4_derive_from_lock_not_re_literalized():
    """Q-SWAP-3 REG is the lock; GA4_ALLOCATIONS is SWEEP GA-4 (no duplicate literals)."""
    sweep = dict(portfolio_mc.SWEEP_CONFIGS)
    assert sweep["REG"] == portfolio_mc.ALLOCATIONS == firm_rules._BASE_RISK
    assert portfolio_mc.GA4_ALLOCATIONS == sweep["GA-4"]
    # Unchanged legs on GA-4 still match the lock (only guardian is the variant).
    for leg in ("striker", "aegis", "striker_nas100"):
        assert sweep["GA-4"][leg] == firm_rules._BASE_RISK[leg]
    assert sweep["GA-4"]["guardian"] == 0.0024
