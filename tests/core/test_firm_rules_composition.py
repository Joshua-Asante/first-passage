"""FIRM_RULES rows are composed from product defaults + tier overrides (2026-09-17).

The resolved configuration must stay value-identical to the literal rows it
replaced. The fixture is that literal record, captured from core/firm_rules.py
at 63ea701 before any composition edit; it is an independent expectation and is
never regenerated from the composed module. A changed venue fact is edited in
both places on purpose, with its provenance, or it is a defect.
"""
import json
from pathlib import Path

import firm_rules

FIXTURE = Path(__file__).parent / "fixtures" / "firm_rules_resolved.json"


def _typed(value):
    """(type name, value): 25_000 != 25000.0, True != 1, None != 0 in the compare."""
    if isinstance(value, dict):
        return {k: _typed(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_typed(v) for v in value]
    return (type(value).__name__, value)


def _record() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_resolved_rows_match_the_pre_composition_record():
    record = _record()
    assert list(firm_rules.FIRM_RULES) == list(record["FIRM_RULES"])
    for tier, row in record["FIRM_RULES"].items():
        assert _typed(firm_rules.FIRM_RULES[tier]) == _typed(row), tier
    assert _typed(firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS) == _typed(
        record["AUTOMATION_FRIENDLY_PROP_FIRMS"])


def test_tier_mutation_does_not_leak_to_siblings_or_defaults(monkeypatch):
    rows = list(firm_rules.FIRM_RULES.values())
    assert len({id(r) for r in rows}) == len(rows)
    monkeypatch.setitem(firm_rules.FIRM_RULES["Tradeify_Select_100K"], "dd_lock_offset_usd", 100.0)
    assert firm_rules.FIRM_RULES["Tradeify_Select_50K"]["dd_lock_offset_usd"] == 1_000_000.0
    assert firm_rules.FIRM_RULES["Tradeify_Growth_100K"]["dd_lock_offset_usd"] == 1_000_000.0
    assert firm_rules._TRADEIFY_SELECT_EVAL["dd_lock_offset_usd"] == 1_000_000.0
    assert firm_rules._TRADEIFY_EVAL["dd_lock_offset_usd"] == 1_000_000.0


def test_product_defaults_are_not_rows():
    for name in ("_BULENOX_OPTION1", "_TRADEIFY_EVAL", "_TRADEIFY_SELECT_EVAL",
                 "_MFFU_RAPID_EVAL", "_BLUSKY_PREMIUM_EVAL"):
        assert "starting_balance" not in getattr(firm_rules, name), name
