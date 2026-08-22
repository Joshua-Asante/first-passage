from pathlib import Path

from discovery.grammar import load_grammar_with_hash_check, sha256_of_grammar

GRAMMAR_PATH = Path(__file__).resolve().parents[1] / "discovery_manifests" / "grow0_grammar.json"


def test_grow0_grammar_matches_prereg_section_2():
    sha = sha256_of_grammar(GRAMMAR_PATH)
    grammar = load_grammar_with_hash_check(GRAMMAR_PATH, expected_sha256=sha)
    assert grammar.generation_budget == 10
    assert set(grammar.families.keys()) == {"session_offset_min"}
    assert grammar.families["session_offset_min"] == [0, 15, 30, 45, 60, 75, 90, 105, 120, 135]
