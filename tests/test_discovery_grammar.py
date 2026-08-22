"""Deep-lane mutation grammar -- frozen operator families + SHA256 hash pin.

GROW spec v2 Part A step 2: "grammar.json committed at G0, SHA256 pinned in
the PREREG, hash recomputed at every run start, exits nonzero on mismatch,
stamps the hash into every emitted row" (audit repair G-D1-FREEZE, mirroring
the PORT_MANIFEST.sha256 pattern already used for locked-strategy ports).
"""
from __future__ import annotations

import json

import pytest

from discovery.grammar import (
    GrammarDriftError,
    GrammarValidationError,
    load_grammar,
    load_grammar_with_hash_check,
    sha256_of_grammar,
)

_VALID = {
    "generation_budget": 10,
    "families": {
        "entry_filter": {"threshold_sigma": [0.5, 1.0, 1.5]},
        "exit_geometry": {"rr_multiple": [1.5, 2.0, 3.0]},
        "sizing_policy": ["flat", "cushion_proportional"],
    },
}


def _write(tmp_path, payload=None):
    p = tmp_path / "grammar.json"
    p.write_text(json.dumps(payload if payload is not None else _VALID), encoding="utf-8")
    return p


def test_load_valid_grammar_roundtrips(tmp_path):
    p = _write(tmp_path)
    g = load_grammar(p)
    assert g.generation_budget == 10
    assert "sizing_policy" in g.families
    assert g.families["sizing_policy"] == ["flat", "cushion_proportional"]


def test_missing_generation_budget_rejected(tmp_path):
    payload = dict(_VALID)
    del payload["generation_budget"]
    p = _write(tmp_path, payload)
    with pytest.raises(GrammarValidationError):
        load_grammar(p)


def test_zero_generation_budget_rejected(tmp_path):
    payload = {**_VALID, "generation_budget": 0}
    p = _write(tmp_path, payload)
    with pytest.raises(GrammarValidationError):
        load_grammar(p)


def test_empty_families_rejected(tmp_path):
    payload = {**_VALID, "families": {}}
    p = _write(tmp_path, payload)
    with pytest.raises(GrammarValidationError):
        load_grammar(p)


def test_non_list_family_values_rejected(tmp_path):
    payload = {
        "generation_budget": 5,
        "families": {"entry_filter": "not-a-list-or-dict-of-lists"},
    }
    p = _write(tmp_path, payload)
    with pytest.raises(GrammarValidationError):
        load_grammar(p)


def test_sha256_is_stable_for_identical_content(tmp_path):
    p1 = _write(tmp_path)
    (tmp_path / "sub").mkdir()
    p2 = tmp_path / "sub" / "grammar2.json"
    p2.write_text(p1.read_text(encoding="utf-8"), encoding="utf-8")
    assert sha256_of_grammar(p1) == sha256_of_grammar(p2)


def test_sha256_changes_when_content_changes(tmp_path):
    p1 = _write(tmp_path)
    h1 = sha256_of_grammar(p1)
    payload = {**_VALID, "generation_budget": 11}
    p2 = _write(tmp_path, payload)
    assert sha256_of_grammar(p2) != h1


def test_hash_check_passes_on_match(tmp_path):
    p = _write(tmp_path)
    expected = sha256_of_grammar(p)
    g = load_grammar_with_hash_check(p, expected_sha256=expected)
    assert g.sha256 == expected


def test_hash_check_raises_on_drift(tmp_path):
    p = _write(tmp_path)
    with pytest.raises(GrammarDriftError):
        load_grammar_with_hash_check(p, expected_sha256="0" * 64)
