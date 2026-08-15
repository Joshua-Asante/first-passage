"""P5 §2-E golden-path fixtures — offline translation layer + sim placeholder."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parent.parent
_FIXTURES_DIR = _REPO / "tests" / "rail_crosstrade"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_fixtures = _load_module("rail_fixtures", _FIXTURES_DIR / "fixtures.py")
_translator = _load_module("rail_translator", _FIXTURES_DIR / "translator.py")

ALL_FIXTURES = _fixtures.ALL_FIXTURES
appendix_a_to_crosstrade = _translator.appendix_a_to_crosstrade
parse_crosstrade_payload = _translator.parse_crosstrade_payload


@pytest.mark.parametrize("fixture", ALL_FIXTURES, ids=lambda f: f"{f.leg}:{f.primitive}")
def test_golden_path_translation_matches_intent(fixture):
    """Diff translated CrossTrade payload against Appendix-A source intent."""
    ct = appendix_a_to_crosstrade(
        fixture.appendix_a,
        account=fixture.account,
        secret_key=fixture.secret_key,
    )
    parsed = parse_crosstrade_payload(ct)
    assert "traderspost" not in ct.lower()
    assert "tradovate" not in ct.lower()

    if fixture.primitive in ("base_entry", "pyramid_add"):
        assert parsed["command"] == "place"
        assert parsed["action"] == fixture.expected_side
        assert int(parsed["qty"]) == fixture.expected_qty
        assert parsed["instrument"] == fixture.appendix_a["symbol"]
        if fixture.primitive == "base_entry":
            assert "stop_loss" in parsed
            assert "take_profit" in parsed
    elif fixture.primitive == "session_end_flat":
        assert parsed["command"] == "closeposition"
        assert int(parsed["quantity"]) == fixture.expected_qty


@pytest.mark.skip(reason="requires operator CrossTrade+NT8 sim account — P5 §2-E e2e gate")
@pytest.mark.parametrize("fixture", ALL_FIXTURES, ids=lambda f: f"{f.leg}:{f.primitive}")
def test_golden_path_e2e_sim(fixture):
    """Fire through live rail on sim; diff fill echo vs source intent (operator wiring)."""
    raise NotImplementedError("operator-owned: CrossTrade webhook → NT8 sim101")


def test_matrix_verdict_tokens_present():
    matrix = _REPO / "docs" / "notes" / "2026-07-06-crosstrade-nt8-payload-sufficiency-matrix.md"
    if not matrix.is_file():
        pytest.skip(
            "payload-sufficiency matrix lives under docs/notes/ "
            "(excluded from the public seed)"
        )
    text = matrix.read_text(encoding="utf-8")
    for token in ("EXPRESSIBLE", "DEFAULTABLE-SAFE", "INEXPRESSIBLE"):
        assert token in text
