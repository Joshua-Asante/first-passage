"""PD-3 fix: `register_search.py open --params-file` bypasses shell quoting.

Caught live during DISC-CAMP-0's real Stage-3 `open` call (docs/briefs/
DISC-CAMP-0-closure-falsified.md, PD-3): passing a JSON --params string
through PowerShell/argparse round-tripped into a manifest field containing
literal backslash-escaped quotes -- human-readable, but not machine-parseable
as JSON. --params-file reads a JSON file directly, so the shell never
touches the JSON payload's quoting at all.

Pure offline tests: no network, stdlib only (register_search.py itself has
no non-stdlib deps).
"""
from __future__ import annotations

import json

import pytest

from discovery import register_search as rs


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(rs, "LEDGER", d)
    return d


def _open_args(**kw):
    base = dict(
        run_id="test_run", tool="catch22", search_space_size=100,
        alpha=0.05, data_window="2010-01-01:2020-01-01",
        hypothesis="h", params="", params_file=None,
        # Explicit blind: SPEC S6 flipped the CLI default to mechanism-first.
        lane="blind", reachability_attestation=None,
        profile_cell=None, profile_consult=None, admission_file=None,
        # Blind default: no prereg (lane asymmetry, 11-key schema).
        prereg=None,
    )
    base.update(kw)
    from argparse import Namespace
    return Namespace(**base)


def test_params_file_stores_valid_json_round_trip(ledger, tmp_path):
    payload = {"k_rule": "non-overlap floor", "T": 51659, "windows": [30, 60, 90]}
    pf = tmp_path / "params.json"
    pf.write_text(json.dumps(payload), encoding="utf-8")

    rs.open_run(_open_args(params_file=str(pf)))

    manifest = json.loads((ledger / "test_run.json").read_text())
    # The stored params string must itself parse as JSON, byte-identical to the input.
    assert json.loads(manifest["params"]) == payload


def test_params_file_invalid_json_aborts_before_writing_manifest(ledger, tmp_path):
    pf = tmp_path / "bad.json"
    pf.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(SystemExit):
        rs.open_run(_open_args(params_file=str(pf)))

    assert not (ledger / "test_run.json").exists()


def test_params_and_params_file_both_given_is_an_error(ledger, tmp_path):
    pf = tmp_path / "params.json"
    pf.write_text("{}", encoding="utf-8")

    with pytest.raises(SystemExit):
        rs.open_run(_open_args(params="inline", params_file=str(pf)))

    assert not (ledger / "test_run.json").exists()


def test_no_params_file_legacy_behavior_unchanged(ledger):
    """Omitting --params-file (the default, None) must be byte-identical to
    today's behavior: whatever --params text was given is stored as-is."""
    rs.open_run(_open_args(params="free text, not JSON", params_file=None))

    manifest = json.loads((ledger / "test_run.json").read_text())
    assert manifest["params"] == "free text, not JSON"


def test_cli_parser_accepts_params_file_flag():
    parser = rs.build_parser()
    ns = parser.parse_args([
        "open", "--tool", "catch22", "--search-space-size", "10",
        "--data-window", "2010-01-01:2020-01-01", "--hypothesis", "h",
        "--params-file", "some/path.json",
    ])
    assert ns.params_file == "some/path.json"
    assert ns.params == ""  # default unchanged


def test_cli_parser_lane_defaults_and_explicit_mechanism_first():
    parser = rs.build_parser()
    base = [
        "open", "--tool", "catch22", "--search-space-size", "10",
        "--data-window", "2010-01-01:2020-01-01", "--hypothesis", "h",
    ]
    ns_default = parser.parse_args(base)
    assert ns_default.lane == "mechanism-first"  # SPEC S6 default flip
    assert ns_default.reachability_attestation is None
    assert ns_default.admission_file is None

    ns_mf = parser.parse_args(base + [
        "--lane", "mechanism-first",
        "--reachability-attestation", "p.json",
        "--admission-file", "adm.json",
    ])
    assert ns_mf.lane == "mechanism-first"
    assert ns_mf.reachability_attestation == "p.json"
    assert ns_mf.admission_file == "adm.json"

    ns_blind = parser.parse_args(base + ["--lane", "blind"])
    assert ns_blind.lane == "blind"


# --- HARV ADR 2026-07-13 §2 HARD gate (reachability attestation) ---------------
# Mechanical existence + non-emptiness only; not per-clause semantic verification.

_BLIND_MANIFEST_KEYS = {
    "run_id", "status", "opened_at", "tool", "K", "alpha",
    "data_window", "hypothesis", "params", "closed_at", "results",
}


def test_mechanism_first_without_attestation_aborts(ledger):
    with pytest.raises(SystemExit):
        rs.open_run(_open_args(lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=None))
    assert not (ledger / "test_run.json").exists()


def test_mechanism_first_missing_attestation_path_aborts(ledger, tmp_path):
    with pytest.raises(SystemExit):
        rs.open_run(_open_args(
            lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
            reachability_attestation=str(tmp_path / "nope.md"),
        ))
    assert not (ledger / "test_run.json").exists()


@pytest.mark.parametrize("content", ["", "   \n"])
def test_mechanism_first_empty_attestation_aborts(ledger, tmp_path, content):
    pf = tmp_path / "empty.md"
    pf.write_text(content, encoding="utf-8")
    with pytest.raises(SystemExit):
        rs.open_run(_open_args(
            lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
            reachability_attestation=str(pf),
        ))
    assert not (ledger / "test_run.json").exists()


def test_mechanism_first_with_valid_attestation_records_lane(ledger, tmp_path):
    pf = tmp_path / "attestation.md"
    pf.write_text(
        "clause C1 reachable under plausible-true world: …",
        encoding="utf-8",
    )
    # ADR 2026-07-25 added a second mechanism-first HARD gate: the declared
    # (instrument, mechanism) cell + its written profile consult. This test
    # covers attestation recording, so it supplies a valid consult to get past
    # the new gate -- the profile gate has its own tests in
    # tests/test_discovery_register_search.py. SPEC S6 also requires admission.
    consult = tmp_path / "consult.txt"
    consult.write_text(
        "=== MYM x opening-range-continuation ===\nverdict: DEAD (2026-07-16)\n",
        encoding="utf-8",
    )
    adm = tmp_path / "admission.json"
    adm.write_text(json.dumps({
        "catalogue_k": 2,
        "em1_edge_r": 0.65,
        "em2_risk_usd": 275.0,
        "em2_measured_edge_r": 0.65,
        "em3_independence_and_stops": True,
        "em4_weekly_cadence": True,
        "em5_session_slot_legal": True,
        "n_events": 1000,
        "delta_over_sigma": 0.113,
    }), encoding="utf-8")
    rs.open_run(_open_args(
        search_space_size=2,
        lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
        reachability_attestation=str(pf),
        profile_cell="MYM:opening-range-continuation",
        profile_consult=str(consult),
        admission_file=str(adm),
    ))
    manifest = json.loads((ledger / "test_run.json").read_text())
    assert manifest["lane"] == "mechanism-first"
    assert manifest["reachability_attestation"] == str(pf)
    assert manifest["admission"]["decision"] == "ADMIT"


def test_blind_open_manifest_schema_unchanged(ledger):
    """Explicit --lane blind must stay byte-identical to the pre-HARV 11-key schema."""
    rs.open_run(_open_args(lane="blind"))
    manifest = json.loads((ledger / "test_run.json").read_text())
    assert set(manifest.keys()) == _BLIND_MANIFEST_KEYS
    assert "lane" not in manifest
    assert "reachability_attestation" not in manifest
