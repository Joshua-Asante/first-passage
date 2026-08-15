"""Registry guard for the prop-portfolio program target firms (ADR 2026-07-12)."""

import firm_rules


def test_automation_friendly_prop_firms_has_four_families():
    assert len(firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS) == 4
    assert set(firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS) == {
        "bulenox",
        "tradeify",
        "myfundedfutures",
        "blusky",
    }


def test_all_target_tier_keys_exist_in_firm_rules():
    for family, tier_keys in firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS.items():
        assert tier_keys, family
        for key in tier_keys:
            assert key in firm_rules.FIRM_RULES, f"{family}: missing {key}"


def test_prop_tiers_carry_challenge_fields():
    required = {
        "dd_type",
        "starting_balance",
        "max_dd_pct",
        "profit_target_pct",
        "weekend_holds",
    }
    for tier_keys in firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS.values():
        for key in tier_keys:
            cfg = firm_rules.FIRM_RULES[key]
            missing = required - set(cfg)
            assert not missing, f"{key} missing {missing}"


def test_prop_tiers_carry_cost_per_side():
    """Every FRIENDLY tier must carry an all-in per-side commission.

    The survivor-scoring G2 cost-law kill gate (ratified recommendation §2.1)
    is structurally unrunnable without it — a tier missing this field would
    silently skip the cost pre-flight. All four firms primary-sourced
    2026-07-13 (prop_envelope v1.0 ratification ADR).
    """
    for tier_keys in firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS.values():
        for key in tier_keys:
            cfg = firm_rules.FIRM_RULES[key]
            cost = cfg.get("cost_per_side_usd")
            assert isinstance(cost, (int, float)) and 0 < cost < 5, (
                f"{key}: cost_per_side_usd missing or implausible ({cost!r})"
            )


def test_live_c1_tier_in_firm_rules():
    """c1 rail uses the explicit Tradeify Select 100K key (ACTIVE_FIRM deleted Phase 4)."""
    assert "Tradeify_Select_100K" in firm_rules.FIRM_RULES
