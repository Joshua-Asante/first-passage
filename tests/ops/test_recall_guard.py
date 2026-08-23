"""Controls for the recall sidecar's Rule-7 reject-list.

The parent brief (2026-07-27 Hermes adoption ruling, Phase A2) requires the
Rule-7 denylist be "a mechanical reject-list in the writer, not a review
obligation". These controls feed the guard denylisted content and assert it
REFUSES. A guard that admits a locked constant as authority is unusable.

Design tension the controls pin: the guard must reject locked constants
ASSERTED AS FACT without rejecting every note that happens to contain a
number. It therefore requires a denylisted value AND a context term to
co-occur — see test_bare_number_without_context_is_allowed.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ops.recall import guard  # noqa: E402


@pytest.fixture(scope="module")
def dl():
    return guard.load_denylist(_REPO_ROOT)


# --- denylist is SOURCED from production, never hardcoded ------------------

def test_denylist_sources_dd_protection_constants(dl):
    """DD_TRIGGER 0.015 / DD_SCALE 0.40 are read from core/dd_protection.py."""
    assert "0.015" in dl.values
    assert "0.40" in dl.values


def test_denylist_sources_locked_risk_pcts(dl):
    """risk %-forms from the historical 4-leg book (living is a subset)."""
    for v in ("0.34", "0.70", "1.50", "0.37"):
        assert v in dl.values, f"{v} missing from sourced denylist"


def test_denylist_excludes_low_cardinality_integers(dl):
    """contract_value 1 / 10 / 100 are useless as denylist entries."""
    for v in ("1", "10", "100"):
        assert v not in dl.values


# --- rejection --------------------------------------------------------------

def test_locked_risk_constant_with_context_is_rejected(dl):
    v = guard.check("DJ30 runs at 0.70% risk per trade", dl)
    assert not v.ok
    assert "0.70" in v.reason


def test_mc_anchor_with_context_is_rejected(dl):
    v = guard.check("the anchor is 99.83% pass / 0.17% bust", dl)
    assert not v.ok


def test_dd_trigger_asserted_as_authority_is_rejected(dl):
    v = guard.check("DD_TRIGGER = 0.015 is the live value", dl)
    assert not v.ok


def test_sha256_hash_is_rejected_unconditionally(dl):
    """LOCK hashes are denylisted with no context requirement."""
    v = guard.check("pin " + "a" * 64, dl)
    assert not v.ok
    assert "hash" in v.reason.lower()


def test_cold_store_ingest_is_rejected(dl):
    """docs/ltm/** and lab/archive/** ingest is denylisted by the pre-reg."""
    assert not guard.check("copied from docs/ltm/notes/foo.md: ...", dl).ok
    assert not guard.check("per lab/archive/orb_mnq_2026-07/RESULTS.md", dl).ok


def test_reason_names_what_matched(dl):
    v = guard.check("guardian risk is 0.34%", dl)
    assert not v.ok
    assert v.reason and "0.34" in v.reason


# --- no over-rejection ------------------------------------------------------

def test_clean_pointer_note_is_allowed(dl):
    v = guard.check("Q-XMEM-1 delete route: see the falsifier RESULTS", dl)
    assert v.ok, v.reason


def test_bare_number_without_context_is_allowed(dl):
    """A number alone is not a Rule-7 leak; the guard needs a context term.

    Without this the guard would reject its own falsifier result, which
    legitimately contains 0.70 as a recall floor.
    """
    v = guard.check("recall floor was 0.70 on that fixture", dl)
    assert v.ok, v.reason


def test_context_term_without_denylisted_value_is_allowed(dl):
    v = guard.check("the risk controls are documented in the ADR", dl)
    assert v.ok, v.reason


def test_empty_note_is_rejected_as_useless(dl):
    assert not guard.check("   ", dl).ok
