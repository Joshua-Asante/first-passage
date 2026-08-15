"""Tests for lab/research_utils/axis_screen.py (harvest-intake standing screen).

Regression pins reproduce the historical Q-KBUDGET-1 table from a JSON fixture
alone — lab/analysis/q_kbudget_1_2026-07/ is not touched.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import research_utils.axis_screen as ax

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "qkbudget_2026_07_axes.json"


# ---------------------------------------------------------------- constants

def test_constants_match_frozen_prereg():
    """CAP / DSR_MIN / POWER_MIN / Z match Q-KBUDGET-1-screen-preregistration §B."""
    assert ax.CAP == 1.0
    assert ax.DSR_MIN == 0.95
    assert ax.POWER_MIN == 0.50
    assert ax.Z == 1.96
    assert ax.YEARS == 6.5
    assert ax.FREQS == (0.5, 1.0, 2.0, 4.0)


# ---------------------------------------------------------------- floor pins

@pytest.mark.parametrize(
    "k,expected",
    [
        (1, 0.65),
        (2, 0.85),
        (3, 0.98),
        (4, 1.06),
        (450, 1.835),
        (3178, 2.05),
    ],
)
def test_floor_at_k_regression(k, expected):
    assert ax.floor_at_k(k) == expected


# ---------------------------------------------------------------- power pins

def test_clause_n_power_d5():
    assert round(ax.clause_n_power(1000, 0.113), 3) == 0.947


def test_clause_n_power_d7():
    # HARV class-analogue δ/σ = 13bp / 90bp
    p = ax.clause_n_power(100, 0.0013 / 0.0090)
    assert abs(p - 0.303) < 0.001


# ---------------------------------------------------------------- schema

def test_schema_rejects_unknown_key():
    rows = json.loads(_FIXTURE.read_text())
    rows[0]["extra_field"] = "nope"
    with pytest.raises(ValueError, match="unknown keys"):
        ax._validate_row(rows[0], 0)


def test_schema_rejects_missing_key():
    row = {
        "axis": "x",
        "family": "y",
        "k_banked": 0,
        "k_intrinsic": [1, 1],
        "n_events": 10,
        "delta_over_sigma": 0.2,
        "delta_citation": "c",
        # unscreenable_reason missing
    }
    with pytest.raises(ValueError, match="missing keys"):
        ax._validate_row(row, 0)


def test_unscreenable_without_reason_hard_error():
    row = {
        "axis": "x",
        "family": "y",
        "k_banked": 0,
        "k_intrinsic": [1, 1],
        "n_events": None,
        "delta_over_sigma": None,
        "delta_citation": None,
        "unscreenable_reason": None,
    }
    with pytest.raises(ValueError, match="unscreenable_reason is mandatory"):
        ax._validate_row(row, 0)


def test_load_manifest_rejects_non_array(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text('{"axis": "x"}\n')
    with pytest.raises(ValueError, match="JSON array"):
        ax.load_manifest(p)


# ---------------------------------------------------------------- verdict branching

def test_verdict_clause_k_fail():
    rows = [{
        "axis": "wide",
        "family": "ES",
        "k_banked": 0,
        "k_intrinsic": [450, 450],
        "n_events": None,
        "delta_over_sigma": None,
        "delta_citation": None,
        "unscreenable_reason": "K kills",
    }]
    out = ax.screen_rows(rows)
    assert out[0]["verdict"] == "FAIL (Clause K)"
    assert out[0]["clause_k"] == "FAIL"


def test_verdict_inherited_clause_n():
    rows = [{
        "axis": "harv",
        "family": "ES",
        "k_banked": 1,
        "k_intrinsic": [1, 2],
        "n_events": None,
        "delta_over_sigma": None,
        "delta_citation": None,
        "unscreenable_reason": "inherited",
        "clause_n_inherited": {"verdict": "FAIL", "citation": "prior FAIL cite"},
    }]
    out = ax.screen_rows(rows)
    assert out[0]["verdict"] == "FAIL (Clause N, inherited)"
    assert out[0]["clause_k"] == "PASS"


def test_verdict_unscreenable():
    rows = [{
        "axis": "no-delta",
        "family": "NQ",
        "k_banked": 0,
        "k_intrinsic": [1, 1],
        "n_events": None,
        "delta_over_sigma": None,
        "delta_citation": None,
        "unscreenable_reason": "no citable prior",
    }]
    out = ax.screen_rows(rows)
    assert out[0]["verdict"] == "UNSCREENABLE"
    assert out[0]["clause_n"] == "no citable prior"


def test_verdict_clause_n_fail_computed():
    rows = [{
        "axis": "weak",
        "family": "6J",
        "k_banked": 0,
        "k_intrinsic": [1, 3],
        "n_events": 100,
        "delta_over_sigma": 0.14444444444444443,
        "delta_citation": "analogue",
        "unscreenable_reason": None,
    }]
    out = ax.screen_rows(rows)
    assert out[0]["verdict"] == "FAIL (Clause N)"
    assert out[0]["power"] is not None
    assert out[0]["power"] < ax.POWER_MIN


def test_verdict_pass_best_end_k():
    """Row PASSES Clause K only if its BEST (lowest-K) end passes."""
    rows = [{
        "axis": "d5-like",
        "family": "MYM/MNQ",
        "k_banked": 0,
        "k_intrinsic": [1, 3],
        "n_events": 1000,
        "delta_over_sigma": 0.113,
        "delta_citation": "Baltussen",
        "unscreenable_reason": None,
    }]
    out = ax.screen_rows(rows)
    assert out[0]["clause_k"] == "PASS"
    assert out[0]["verdict"] == "PASS"
    assert round(out[0]["power"], 3) == 0.947


def test_range_hi_end_above_cap_still_pass_on_best():
    """K_eff hi may exceed Cap; best (lo) end still gates PASS on Clause K."""
    # k_intrinsic 1..4 → k_eff 1..4; floor(1)=0.65 PASS, floor(4)=1.06 FAIL —
    # best-end semantics → Clause K PASS.
    rows = [{
        "axis": "range",
        "family": "NQ",
        "k_banked": 0,
        "k_intrinsic": [1, 4],
        "n_events": 1000,
        "delta_over_sigma": 0.2,
        "delta_citation": "synthetic",
        "unscreenable_reason": None,
    }]
    out = ax.screen_rows(rows)
    assert out[0]["floor"][0] == 0.65
    assert out[0]["floor"][1] == 1.06
    assert out[0]["clause_k"] == "PASS"


# ---------------------------------------------------------------- full fixture

def test_qkbudget_fixture_reproduces_resolved_table():
    rows = ax.load_manifest(_FIXTURE)
    screened = ax.screen_rows(rows)
    assert len(screened) == 7

    # AMENDED 2026-08-04 by ADR 2026-08-04-family-k-bank-disclosure-not-gate
    # (Accepted). K_eff now counts within-search selection only; k_banked is a
    # disclosure. The superseded expectations were:
    #   D1 FAIL (Clause K) floor [2.05, 2.05]   <- killed by GC/MGC bank 3,177
    #   D4 FAIL (Clause K)                      <- same bank
    #   passing 1 / failing 6 / unscreenable 0
    # D1 and D4 are no longer K-killed. They now fall through to UNSCREENABLE on
    # their own merits (neither has a citable delta) -- which is the honest verdict:
    # "we cannot screen this", not "the ledger forbids it".
    by_axis = {r["axis"][:2]: r for r in screened}
    assert by_axis["D1"]["verdict"] == "UNSCREENABLE"
    assert by_axis["D1"]["k_banked"] == 3177          # disclosure survives...
    assert by_axis["D1"]["k_eff"] == [1, 1]           # ...but does not enter k_eff
    assert by_axis["D1"]["floor"] == [0.65, 0.65]
    assert by_axis["D1"]["clause_k"] == "PASS"
    assert by_axis["D3"]["verdict"] == "FAIL (Clause N, inherited)"
    assert by_axis["D4"]["verdict"] == "UNSCREENABLE"
    assert by_axis["D5"]["verdict"] == "PASS"
    assert by_axis["D5"]["floor"] == [0.65, 0.98]
    assert round(by_axis["D5"]["power"], 3) == 0.947
    assert by_axis["D7"]["verdict"] == "FAIL (Clause N)"
    assert abs(by_axis["D7"]["power"] - 0.303) < 0.001

    # UNCHANGED, and load-bearing: a genuine WIDE SEARCH still dies on Clause K.
    # D2 declares k_intrinsic 1000-10000, D6 declares 450. If either of these ever
    # flips to PASS, the amendment has been mis-implemented as "K no longer gates".
    assert by_axis["D2"]["verdict"] == "FAIL (Clause K)"
    assert by_axis["D2"]["k_eff"] == [1000, 10000]
    assert by_axis["D6"]["verdict"] == "FAIL (Clause K)"
    assert by_axis["D6"]["floor"] == [1.835, 1.835]

    passing = [r for r in screened if r["verdict"] == "PASS"]
    failing = [r for r in screened if r["verdict"].startswith("FAIL")]
    unscreenable = [r for r in screened if r["verdict"] == "UNSCREENABLE"]
    assert len(passing) == 1
    assert len(failing) == 4
    assert len(unscreenable) == 2
    assert ax.aggregate_verdict(screened).startswith("RESOLVED")


# ------------------------------------------------- ADR 2026-08-04 regressions

def _row(**kw):
    """Minimal screenable row; caller overrides k_banked / k_intrinsic."""
    base = {
        "axis": "T1 test axis", "family": "TEST",
        "k_banked": 0, "k_intrinsic": [1, 1],
        "n_events": 1000, "delta_over_sigma": 0.113,
        "delta_citation": "synthetic fixture", "unscreenable_reason": None,
    }
    base.update(kw)
    return base


def test_huge_family_bank_no_longer_fails_clause_k_but_is_still_reported():
    """The ADR's core change. A family bank of 3,177 -- historically an instant
    kill at floor 2.05 -- must now PASS Clause K at k_intrinsic=1, while the bank
    remains visible in both the row and the rendered table (mandatory disclosure)."""
    [r] = ax.screen_rows([_row(k_banked=3177, k_intrinsic=[1, 1])])
    assert r["clause_k"] == "PASS"
    assert r["k_eff"] == [1, 1]
    assert r["floor"] == [0.65, 0.65]
    assert r["k_banked"] == 3177
    assert "3177" in ax.format_table([r]), "disclosure must survive in the table"


def test_a_genuine_wide_search_still_fails_clause_k():
    """ADVERSARIAL. The amendment must not read as 'K no longer gates'. A design
    that actually searches 5 variants still fails -- k_intrinsic is now the ONLY
    brake, so this test is the one that catches the change being over-applied."""
    [r] = ax.screen_rows([_row(k_banked=0, k_intrinsic=[5, 5])])
    assert r["clause_k"] == "FAIL"
    assert r["verdict"] == "FAIL (Clause K)"
    assert r["floor"][0] > ax.CAP


def test_clause_k_boundary_is_unmoved_at_k_eff_three_and_four():
    """The Cap and the floor ladder are explicitly NOT touched by the ADR."""
    [ok] = ax.screen_rows([_row(k_intrinsic=[3, 3])])
    [bad] = ax.screen_rows([_row(k_intrinsic=[4, 4])])
    assert ok["clause_k"] == "PASS" and ok["floor"] == [0.98, 0.98]
    assert bad["clause_k"] == "FAIL" and bad["floor"] == [1.06, 1.06]


def test_k_banked_is_still_a_required_key():
    """Disclosure decay is ADR section-4 trigger 2. Dropping the key must still error."""
    bad = _row()
    del bad["k_banked"]
    with pytest.raises((ValueError, KeyError)):
        ax.screen_rows([bad])


def test_cli_smoke(tmp_path):
    out = tmp_path / "results.json"
    rc = ax.main([str(_FIXTURE), "--out", str(out)])
    assert rc == 0
    payload = json.loads(out.read_text())
    assert payload["verdict"].startswith("RESOLVED")
    assert payload["cap"] == 1.0
    assert len(payload["rows"]) == 7
