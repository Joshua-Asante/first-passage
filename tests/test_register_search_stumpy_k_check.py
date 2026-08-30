"""Optional STUMPY/matrix-profile K cross-check at register_search open
(root-cause finding 2026-08-29: --search-space-size was a hand-typed integer
even for the one tool whose K has a closed form -- discovery.k_count already
computes it, nothing called it here).

Opt-in, mirrors test_register_search_cost_law.py's house style: paired
positive/negative fixtures, a Namespace helper with sane defaults, a `ledger`
fixture that redirects register_search.LEDGER to tmp_path.
"""
from __future__ import annotations

import json
from argparse import Namespace

import pytest

from discovery import register_search
from discovery.k_count import DEFAULT_WINDOWS, compute_k_bracket


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(register_search, "LEDGER", d)
    return d


def _attestation(tmp_path, text="reachability attested at the panel basis"):
    p = tmp_path / "attestation.md"
    p.write_text(text, encoding="utf-8")
    return str(p)


def _consult_file(tmp_path):
    p = tmp_path / "consult.txt"
    p.write_text(
        "=== MNQ x opening-range-continuation ===\nverdict: PASS (2026-08-19)\n",
        encoding="utf-8",
    )
    return str(p)


def _admission_file(tmp_path, catalogue_k=2):
    p = tmp_path / "admission.json"
    p.write_text(
        json.dumps(
            {
                "catalogue_k": catalogue_k,
                "em1_edge_r": 0.65,
                "em2_risk_usd": 275.0,
                "em2_measured_edge_r": 0.65,
                "em3_independence_and_stops": True,
                "em4_weekly_cadence": True,
                "em5_session_slot_legal": True,
                "n_events": 1000,
                "delta_over_sigma": 0.113,
            }
        ),
        encoding="utf-8",
    )
    return str(p)


def _open_args(**kw):
    base = dict(
        run_id="test_run",
        tool="catch22",
        search_space_size=2,
        alpha=0.05,
        data_window="2010-01-01:2020-01-01",
        hypothesis="h",
        params="",
        params_file=None,
        lane="mechanism-first",
        reachability_attestation=None,
        profile_cell="MNQ:opening-range-continuation",
        profile_consult=None,
        admission_file=None,
        prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
        cost_law_instrument=None,
        cost_law_firm_key=None,
        cost_law_panel_price=None,
        cost_law_cohort_delta_bp=None,
        cost_law_slip_ticks=None,
        cost_law_slip_convention=None,
    )
    base.update(kw)
    return Namespace(**base)


def _mf_ready(tmp_path, **overrides):
    base = dict(
        lane="mechanism-first",
        reachability_attestation=_attestation(tmp_path),
        profile_cell="MNQ:opening-range-continuation",
        profile_consult=_consult_file(tmp_path),
        admission_file=_admission_file(tmp_path),
    )
    base.update(overrides)
    return base


_T = 10_000
_EXPECTED_K = compute_k_bracket(_T, DEFAULT_WINDOWS).k_dsr


def test_non_stumpy_tool_is_a_noop():
    """A T field in params is irrelevant for any tool other than stumpy."""
    result = register_search._require_stumpy_k_check(
        _open_args(tool="catch22", search_space_size=999),
        json.dumps({"T": _T}),
    )
    assert result is None


def test_stumpy_without_t_in_params_is_a_noop():
    """Status quo for stumpy campaigns that haven't adopted the T field."""
    result = register_search._require_stumpy_k_check(
        _open_args(tool="stumpy", search_space_size=999), ""
    )
    assert result is None


def test_stumpy_matching_k_admits():
    result = register_search._require_stumpy_k_check(
        _open_args(tool="stumpy", search_space_size=_EXPECTED_K),
        json.dumps({"T": _T}),
    )
    assert result is not None
    assert result["k_dsr"] == _EXPECTED_K


def test_stumpy_mismatched_k_aborts():
    with pytest.raises(SystemExit) as exc:
        register_search._require_stumpy_k_check(
            _open_args(tool="stumpy", search_space_size=_EXPECTED_K + 1),
            json.dumps({"T": _T}),
        )
    assert "does not match" in str(exc.value)
    assert str(_EXPECTED_K) in str(exc.value)


def test_stumpy_fractional_t_rejected_not_truncated():
    """int(10000.5) == 10000 silently -- params.T=10000.5 must abort, not
    silently validate K against the truncated 10000 (Codex review, PR #218)."""
    with pytest.raises(SystemExit) as exc:
        register_search._require_stumpy_k_check(
            _open_args(tool="stumpy", search_space_size=_EXPECTED_K),
            json.dumps({"T": _T + 0.5}),
        )
    assert "must be an integer" in str(exc.value)
    assert "not truncating" in str(exc.value)


def test_stumpy_fractional_window_rejected_not_truncated():
    with pytest.raises(SystemExit) as exc:
        register_search._require_stumpy_k_check(
            _open_args(tool="stumpy", search_space_size=_EXPECTED_K),
            json.dumps({"T": _T, "windows": [30.5, 60, 90]}),
        )
    assert "must be an integer" in str(exc.value)
    assert "not truncating" in str(exc.value)


def test_stumpy_integer_valued_float_t_accepted():
    """10000.0 is integer-valued -- not fractional -- so it's still accepted."""
    result = register_search._require_stumpy_k_check(
        _open_args(tool="stumpy", search_space_size=_EXPECTED_K),
        json.dumps({"T": float(_T)}),
    )
    assert result is not None
    assert result["k_dsr"] == _EXPECTED_K


def test_stumpy_custom_windows_respected():
    windows = (15, 45)
    expected = compute_k_bracket(_T, windows).k_dsr
    result = register_search._require_stumpy_k_check(
        _open_args(tool="stumpy", search_space_size=expected),
        json.dumps({"T": _T, "windows": list(windows)}),
    )
    assert result is not None
    assert result["k_dsr"] == expected


# STUMPY's K_dsr base cost alone is 22+1=23 -- always above mechanism-first's
# CAP=1.0-implied K<=3 ceiling (docs/adr/2026-08-04-family-k-bank-disclosure-
# not-gate.md's "wide mining is structurally unfundable" finding, confirmed
# directly: floor_at_k(23) already exceeds CAP). Every real STUMPY campaign in
# this repo runs --lane blind, never mechanism-first -- so the open_run
# integration tests below use blind, matching actual usage, not a fixture of
# convenience.
def _blind_open_args(**kw):
    base = dict(lane="blind", reachability_attestation=None, profile_cell=None,
                profile_consult=None, admission_file=None, prereg=None)
    base.update(kw)
    return _open_args(**base)


def test_positive_open_records_stumpy_k_check_on_manifest(ledger, tmp_path):
    register_search.open_run(
        _blind_open_args(
            tool="stumpy",
            search_space_size=_EXPECTED_K,
            params=json.dumps({"T": _T}),
        )
    )
    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert "stumpy_k_check" in manifest
    assert manifest["stumpy_k_check"]["k_dsr"] == _EXPECTED_K


def test_negative_open_mismatched_k_no_manifest_written(ledger, tmp_path):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _blind_open_args(
                tool="stumpy",
                search_space_size=_EXPECTED_K + 1,
                params=json.dumps({"T": _T}),
            )
        )
    assert "does not match" in str(exc.value)
    assert not (ledger / "test_run.json").exists()


def test_open_stumpy_without_t_field_unaffected(ledger, tmp_path):
    """Omitting params.T entirely does not change existing behavior."""
    register_search.open_run(
        _blind_open_args(tool="stumpy", search_space_size=5)
    )
    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert "stumpy_k_check" not in manifest
