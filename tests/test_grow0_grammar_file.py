from pathlib import Path

from discovery.grammar import load_grammar_with_hash_check

GRAMMAR_PATH = Path(__file__).resolve().parents[1] / "discovery_manifests" / "grow0_grammar.json"

# Pinned literal, not derived from the file under test -- sha256_of_grammar(GRAMMAR_PATH) would
# make this test tautological (it could never observe a drift, since the "expected" value would
# always be recomputed from whatever the file currently contains). Verified this session as the
# grammar file's actual current SHA256.
_EXPECTED_SHA256 = "89383a593a3a5c80f6e1973c3c3cffdfa65a0d0c620fccd92c3a1f9c031f499f"


def test_grow0_grammar_matches_prereg_section_2():
    grammar = load_grammar_with_hash_check(GRAMMAR_PATH, expected_sha256=_EXPECTED_SHA256)
    assert grammar.generation_budget == 10
    assert set(grammar.families.keys()) == {"session_offset_min"}
    assert grammar.families["session_offset_min"] == [0, 15, 30, 45, 60, 75, 90, 105, 120, 135]
