"""Personal Tradovate tier (ADR 2026-10-09 owed item 2): public row, private balance."""
import json

import pytest

import firm_rules
from mc import preflight

TIER = "Personal_Tradovate"
FIXTURE_BALANCE = 12_345.0  # test fixture value, not the account's capital


def test_public_row_carries_no_balance_literal():
    row = firm_rules.FIRM_RULES[TIER]
    assert row["starting_balance"] is None
    assert row["starting_balance_source"] == "private"
    assert row["dd_type"] == "trailing" and row["max_dd_pct"] == 15.0
    assert row["profit_target_pct"] is None
    assert TIER not in {k for keys in firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS.values() for k in keys}


def _write(tmp_path, monkeypatch, payload):
    path = tmp_path / "firm_rules.private.json"
    path.write_text(payload if isinstance(payload, str) else json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(firm_rules, "PRIVATE_RULES_PATH", path)


def test_loader_reads_private_value(tmp_path, monkeypatch):
    _write(tmp_path, monkeypatch, {TIER: {"starting_balance": FIXTURE_BALANCE}})
    assert firm_rules.private_starting_balance(TIER) == FIXTURE_BALANCE


def test_loader_refuses_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(firm_rules, "PRIVATE_RULES_PATH", tmp_path / "absent.json")
    with pytest.raises(firm_rules.PrivateRuleError, match="absent"):
        firm_rules.private_starting_balance(TIER)


@pytest.mark.parametrize("payload", [
    "{not json", [], {}, {TIER: {}}, {TIER: {"starting_balance": None}},
    {TIER: {"starting_balance": True}}, {TIER: {"starting_balance": "5000"}},
    {TIER: {"starting_balance": 0}}, {TIER: {"starting_balance": -1}},
    '{"%s": {"starting_balance": Infinity}}' % TIER,
])
def test_loader_refuses_invalid(tmp_path, monkeypatch, payload):
    _write(tmp_path, monkeypatch, payload)
    with pytest.raises(firm_rules.PrivateRuleError):
        firm_rules.private_starting_balance(TIER)


def test_loader_refuses_public_tier():
    with pytest.raises(firm_rules.PrivateRuleError, match="not privately sourced"):
        firm_rules.private_starting_balance("Tradeify_Select_100K")


def test_preflight_refuses_tier_with_no_profit_target(tmp_path, monkeypatch):
    # Pre-flight finding: simulate_path is pass/bust shaped; the growth statistic
    # needs the Q-SFGROWTH-1 harness. Refused with or without a basis.
    _write(tmp_path, monkeypatch, {TIER: {"starting_balance": FIXTURE_BALANCE}})
    for kwargs in ({}, {"account": FIXTURE_BALANCE}):
        with pytest.raises(preflight.EngineUnsupported, match="profit target"):
            preflight.firm_kwargs(TIER, **kwargs)
    with pytest.raises(preflight.EngineUnsupported):
        preflight.assert_engine_ready(TIER)


def test_prop_tiers_unchanged_through_preflight():
    kw = preflight.firm_kwargs("Tradeify_Select_100K")
    assert kw["starting_equity"] == 100_000.0 and kw["dd_type"] == "trailing_locking"
