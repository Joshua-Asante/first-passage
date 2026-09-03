"""The Aegis drift conclusion must follow the control, not be asserted regardless of it.

`RESULTS.md` verdict item 4 concludes that the Aegis-ballast gain "is Aegis's positive
drift over 2022-2026, not diversification". That is a CONCLUSION FROM the shuffled-Aegis
control -- a derangement of its trade dates within each year, drift kept, co-movement
destroyed -- and it holds only when the control busts at or below the real book.

The renderer used to append it unconditionally. Two ways that went wrong: with
`controls.json` absent the prose said the control was "absent" and then reported its
finding as established anyway; and had a re-run put the shuffled book ABOVE the real one,
the same sentence would have contradicted the figures printed immediately beside it.
Raised by Codex on PR #271 (round 4).

Only one of the three orderings is exercised by the committed data (shuffled 8.27% <= real
8.63%), so the other two are unreachable through the artifact and would otherwise go
untested. That is exactly why the branch logic is a separate function.
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

_CAMPAIGN = (pathlib.Path(__file__).resolve().parents[2] / "lab" / "analysis" / "c1"
             / "tradeify_book_composition_2026-09")
_RENDER = _CAMPAIGN / "render_results.py"

_DRIFT = "not diversification"


@pytest.fixture(scope="module")
def rr():
    if not _RENDER.exists():
        pytest.skip(f"absent: {_RENDER}")
    spec = importlib.util.spec_from_file_location("render_results_under_test", _RENDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_control_below_real_supports_the_drift_reading(rr):
    """The committed ordering: shuffled 8.27 <= real 8.63."""
    head, txt = rr.drift_reading(8.27, 8.63, 5)
    assert _DRIFT in txt
    assert "for the wrong reason" in head
    assert "8.27" in txt and "8.63" in txt and "5 draws" in txt


def test_control_equal_to_real_still_supports_it(rr):
    _, txt = rr.drift_reading(8.63, 8.63, 5)
    assert _DRIFT in txt, "'matches or beats' must include the equality case"


def test_control_above_real_withholds_the_drift_reading(rr):
    """If destroying co-movement made things WORSE, the drift reading is not supported."""
    head, txt = rr.drift_reading(9.90, 8.63, 5)
    assert _DRIFT not in txt, "asserted the drift conclusion against its own control"
    assert "unresolved" in txt
    assert "WORSE" in txt
    assert "for the wrong reason" not in head
    assert "9.90" in txt and "8.63" in txt


def test_absent_control_withholds_the_drift_reading(rr):
    """With no control there is no evidence either way, so claim neither."""
    head, txt = rr.drift_reading(None, None, 0)
    assert _DRIFT not in txt, "reported an unavailable control's finding as established"
    assert "UNTESTED" in txt
    assert "for the wrong reason" not in head


def test_clause_reads_as_a_sentence_after_But(rr):
    """The caller renders 'But {clause}.' -- the clause must not carry its own terminator."""
    for args in ((8.27, 8.63, 5), (9.90, 8.63, 5), (None, None, 0)):
        _, txt = rr.drift_reading(*args)
        assert txt and not txt.endswith("."), f"clause should not end with a period: {txt[-40:]!r}"
        assert not txt[0].isupper() or txt.startswith("the"), txt[:40]
