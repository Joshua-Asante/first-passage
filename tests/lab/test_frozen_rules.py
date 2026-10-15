"""Frozen-rule load integrity for lab/discovery/frozen_rules.py.

Moved from tests/test_stage4_7_drivers.py when that DISC-CAMP-0 driver suite was
retired (its campaign glue under lab/analysis/disccamp0_gc_2010_18/ no longer
exists). These two cases exercise only the live discovery modules.
"""
from __future__ import annotations

import json

import pytest

from discovery.frozen_rules import FrozenRuleLoadError, load_frozen_rules
from discovery.motif_rules import freeze_rule_from_spec
from discovery.synthetic_bars import default_motif_shape


def _payload(seed: int, candidate_id: str):
    shape = default_motif_shape(10, seed=seed)
    rule = freeze_rule_from_spec(
        shape, direction=1, horizon=3, trigger=0.5, candidate_id=candidate_id
    )
    return rule, [{**rule.as_provenance(), "shape": [float(v) for v in rule.shape]}]


def test_load_frozen_rules_roundtrip(tmp_path):
    rule, payload = _payload(1, "test_rule")
    p = tmp_path / "rules.json"
    p.write_text(json.dumps(payload))
    loaded = load_frozen_rules(p)
    assert len(loaded) == 1
    assert loaded[0].candidate_id == "test_rule"
    assert loaded[0].shape_hash == rule.shape_hash


def test_load_frozen_rules_tamper_fails(tmp_path):
    _, payload = _payload(2, "tamper")
    payload[0]["shape"][0] += 0.01  # corrupt bytes, keep stale hash
    p = tmp_path / "rules.json"
    p.write_text(json.dumps(payload))
    with pytest.raises(FrozenRuleLoadError):
        load_frozen_rules(p)
