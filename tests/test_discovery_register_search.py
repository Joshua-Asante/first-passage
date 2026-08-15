"""Ledger path + repo-root anchor + profile-consult gate for
lab/discovery/register_search.py.

The profile-consult gate (ADR 2026-07-25 instrument-profile-index) mirrors the
existing reachability-attestation HARD gate: a mechanism-first `open` must
declare the (instrument, mechanism) cell it occupies and carry the written
`instrument_profiles.py cell` output. It is a MECHANICAL check -- exists,
non-empty, names the declared cell -- and deliberately does not parse the
verdict; addressing a blocking prior is the pre-registration author's job.

The consult arrives as a FILE rather than by importing the profile module:
register_search lives in lab/, the module lives in scripts/, and
scripts/check_boundaries.py enforces that layer contract.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

from discovery import register_search
from research_utils.repo_root import repo_root


def test_repo_root_anchor_matches_worktree():
    root = repo_root()
    assert register_search._REPO_ROOT == root
    expected = Path(__file__).resolve().parents[1]
    assert root == expected


def test_default_ledger_under_repo_root_when_env_unset(monkeypatch):
    monkeypatch.delenv("DISCOVERY_LEDGER", raising=False)
    # Module-level LEDGER is fixed at import; recompute the contract explicitly.
    assert (repo_root() / "discovery_manifests" / "README.md").is_file()
    if "DISCOVERY_LEDGER" not in os.environ:
        assert register_search.LEDGER == repo_root() / "discovery_manifests"


# --------------------------------------------------------------------------
# Profile-consult gate (ADR 2026-07-25)
# --------------------------------------------------------------------------


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(register_search, "LEDGER", d)
    return d


@pytest.fixture
def attestation(tmp_path):
    p = tmp_path / "attestation.md"
    p.write_text("reachability attested at the panel basis", encoding="utf-8")
    return str(p)


def _admission_payload(catalogue_k=2, **overrides):
    row = {
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
    row.update(overrides)
    return row


def _admission_file(tmp_path, catalogue_k=2, name="admission.json", **overrides):
    p = tmp_path / name
    p.write_text(
        json.dumps(_admission_payload(catalogue_k=catalogue_k, **overrides)),
        encoding="utf-8",
    )
    return str(p)


def _open_args(**kw):
    base = dict(
        run_id="test_run", tool="catch22", search_space_size=100,
        alpha=0.05, data_window="2010-01-01:2020-01-01",
        hypothesis="h", params="", params_file=None,
        lane="blind", reachability_attestation=None,
        profile_cell=None, profile_consult=None,
        admission_file=None,
        # Blind default: no prereg (lane asymmetry, 11-key schema).
        prereg=None,
    )
    base.update(kw)
    return Namespace(**base)


def _consult_file(tmp_path, text, name="consult.txt"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


def test_blind_lane_manifest_keeps_the_frozen_eleven_key_schema(ledger):
    """Regression: the blind/legacy schema is frozen. Seven committed manifests
    depend on it, so the profile fields must never appear on this path."""
    register_search.open_run(_open_args())

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert len(manifest) == 11
    assert "profile_cell" not in manifest
    assert "profile_consult" not in manifest


def test_mechanism_first_open_requires_a_profile_cell(ledger, attestation):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation)
        )
    assert "--profile-cell" in str(exc.value)


def test_mechanism_first_open_rejects_a_malformed_profile_cell(ledger, attestation):
    """<SYMBOL>:<mechanism-id> is the declared shape; a bare symbol is not it."""
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell="MYM",
            )
        )
    assert "--profile-cell" in str(exc.value)


def test_mechanism_first_open_requires_the_written_consult(ledger, attestation):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell="MYM:opening-range-continuation",
            )
        )
    message = str(exc.value)
    assert "profile consult" in message.lower()
    # The abort must be actionable: it names the command that produces the file.
    assert "instrument_profiles.py cell MYM opening-range-continuation" in message


def test_profile_consult_file_must_exist(ledger, attestation, tmp_path):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell="MYM:opening-range-continuation",
                profile_consult=str(tmp_path / "absent.txt"),
            )
        )
    assert "not found" in str(exc.value)


def test_profile_consult_file_must_be_non_empty(ledger, attestation, tmp_path):
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell="MYM:opening-range-continuation",
                profile_consult=_consult_file(tmp_path, "   \n  "),
            )
        )
    assert "empty" in str(exc.value)


def test_profile_consult_must_name_the_declared_cell(ledger, attestation, tmp_path):
    """A consult for a DIFFERENT cell is not evidence for this one."""
    other = "=== ZB x opening-range-breakout ===\nverdict: DEAD (2026-07-20)\n"
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell="MYM:opening-range-continuation",
                profile_consult=_consult_file(tmp_path, other),
            )
        )
    assert "does not name" in str(exc.value)


def test_mechanism_first_open_records_the_cell_and_consult(ledger, attestation, tmp_path):
    consult = _consult_file(
        tmp_path,
        "=== MYM x opening-range-continuation ===\nverdict: DEAD (2026-07-16)\n",
    )
    register_search.open_run(
        _open_args(
            search_space_size=2,
            lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
            profile_cell="MYM:opening-range-continuation", profile_consult=consult,
            admission_file=_admission_file(tmp_path, catalogue_k=2),
        )
    )

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert manifest["lane"] == "mechanism-first"
    assert manifest["profile_cell"] == "MYM:opening-range-continuation"
    assert manifest["profile_consult"] == consult
    assert manifest["admission"]["decision"] == "ADMIT"


@pytest.mark.parametrize("cell", ["MYM:", ":opening-range-continuation", ":"])
def test_profile_cell_rejects_an_empty_half(ledger, attestation, tmp_path, cell):
    """"" is a substring of everything, so an empty half would vacuously satisfy
    the cell-naming check and silently disarm the gate."""
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell=cell,
                profile_consult=_consult_file(tmp_path, "unrelated content"),
            )
        )
    assert "--profile-cell" in str(exc.value)


def test_a_sibling_micro_consult_does_not_satisfy_its_parent(ledger, attestation, tmp_path):
    """Substring matching false-accepted here: "NQ" occurs inside "MNQ", so MNQ's
    consult satisfied a declared NQ cell. Parent-vs-micro is a distinction this
    programme treats as load-bearing, so the match is anchored on the header."""
    mnq_consult = _consult_file(
        tmp_path,
        "=== MNQ x opening-range-breakout ===\n"
        "ledger: ops/instruments/MNQ.md\nverdict: DEAD (2026-07-23)\n",
    )
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(
            _open_args(
                lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
                profile_cell="NQ:opening-range-breakout", profile_consult=mnq_consult,
            )
        )
    assert "does not name" in str(exc.value)


def test_gate_accepts_real_cmd_cell_output_and_does_not_parse_the_verdict(
    ledger, attestation, tmp_path
):
    """Cross-module contract test, and the reason the anchored match is safe.

    Runs the REAL `scripts/instrument_profiles.py cell` and feeds its actual
    output to the gate. This pins the header format the gate anchors on: if
    cmd_cell's output changes, this fails loudly here rather than silently
    disarming the gate in production. It also proves a DEAD cell stays openable
    -- the gate enforces that the author LOOKED, not what the verdict was.
    """
    script = repo_root() / "scripts" / "instrument_profiles.py"
    proc = subprocess.run(
        [sys.executable, str(script), "cell", "MYM", "opening-range-continuation"],
        capture_output=True, text=True, encoding="utf-8",
    )
    # MYM x opening-range-continuation is DEAD, so the consult itself exits 1.
    assert proc.returncode == 1, proc.stdout + proc.stderr
    consult = _consult_file(tmp_path, proc.stdout)

    register_search.open_run(
        _open_args(
            search_space_size=2,
            lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md", reachability_attestation=attestation,
            profile_cell="MYM:opening-range-continuation", profile_consult=consult,
            admission_file=_admission_file(tmp_path, catalogue_k=2),
        )
    )
    assert (ledger / "test_run.json").is_file()


# --------------------------------------------------------------------------
# Attestation completeness gate (ADR 2026-07-25 §2a field shape)
# --------------------------------------------------------------------------


def _json_attestation(tmp_path, payload, name="attestation.json"):
    p = tmp_path / name
    p.write_text(json.dumps(payload), encoding="utf-8")
    return str(p)


def _complete_clause(clause_id="Stage-2-cost-law", **overrides):
    row = {
        "clause": clause_id,
        "value": 6.57,
        "units": "bp/event",
        "basis": "4x Tradeify hurdle at panel-era median",
        "source": "#M6",
    }
    row.update(overrides)
    return row


def _mf_open(ledger, tmp_path, attestation_path, run_id="test_run", catalogue_k=2):
    """Mechanism-first open with valid profile consult + SPEC S6 admission."""
    consult = _consult_file(
        tmp_path,
        "=== MYM x opening-range-continuation ===\nverdict: DEAD (2026-07-16)\n",
    )
    register_search.open_run(
        _open_args(
            run_id=run_id,
            search_space_size=catalogue_k,
            lane="mechanism-first", prereg="docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md",
            reachability_attestation=attestation_path,
            profile_cell="MYM:opening-range-continuation",
            profile_consult=consult,
            admission_file=_admission_file(tmp_path, catalogue_k=catalogue_k),
        )
    )


def test_json_attestation_missing_units_aborts_naming_the_clause(ledger, tmp_path):
    """A JSON clause missing `units` is an incomplete declaration."""
    # units key absent — incomplete declaration
    payload = {"clauses": [{
        "clause": "Stage-2-cost-law",
        "value": 6.57,
        "basis": "4x Tradeify hurdle at panel-era median",
        "source": "#M6",
    }]}
    att = _json_attestation(tmp_path, payload)
    with pytest.raises(SystemExit) as exc:
        _mf_open(ledger, tmp_path, att)
    message = str(exc.value)
    assert "Stage-2-cost-law" in message
    assert "units" in message
    assert message.startswith("ABORT:")
    assert not (ledger / "test_run.json").exists()


def test_json_attestation_empty_units_aborts_naming_the_clause(ledger, tmp_path):
    att = _json_attestation(tmp_path, {"clauses": [_complete_clause(units="  ")]})
    with pytest.raises(SystemExit) as exc:
        _mf_open(ledger, tmp_path, att)
    message = str(exc.value)
    assert "Stage-2-cost-law" in message
    assert "units" in message
    assert not (ledger / "test_run.json").exists()


def test_json_attestation_complete_records_clause_table_on_manifest(ledger, tmp_path):
    clauses = [
        _complete_clause("Stage-2-cost-law"),
        _complete_clause(
            "Stage-6-confirm",
            value=0.65,
            units="annualized Sharpe",
            basis="OOS panel DSR floor at K_eff=1",
            source="§R.1",
        ),
    ]
    att = _json_attestation(tmp_path, {"clauses": clauses})
    _mf_open(ledger, tmp_path, att)

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert manifest["reachability_attestation"] == att
    assert manifest["reachability_clauses"] == clauses
    assert "lane" in manifest  # mechanism-first only


def test_prose_attestation_passes_with_warn_byte_identical_to_presence_only(
    ledger, attestation, tmp_path, capsys
):
    """Prose (non-JSON) keeps exists+non-empty behaviour; WARN names the ADR."""
    _mf_open(ledger, tmp_path, attestation)

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert manifest["lane"] == "mechanism-first"
    assert manifest["reachability_attestation"] == attestation
    # Prose path stores no clause table — presence-only, as today.
    assert "reachability_clauses" not in manifest

    err = capsys.readouterr().err
    assert "WARN:" in err
    assert "ADR 2026-07-25" in err


def test_blind_lane_open_keeps_exactly_eleven_legacy_keys(ledger):
    """Blind / legacy: the 11-key schema stays byte-identical."""
    register_search.open_run(_open_args(run_id="blind_legacy"))
    manifest = json.loads((ledger / "blind_legacy.json").read_text(encoding="utf-8"))
    assert len(manifest) == 11
    assert set(manifest.keys()) == {
        "run_id", "status", "opened_at", "tool", "K", "alpha",
        "data_window", "hypothesis", "params", "closed_at", "results",
    }
    assert "reachability_clauses" not in manifest
    assert "lane" not in manifest


def test_re_registering_an_existing_run_id_still_aborts(ledger):
    """Pre-registration immutability (register_search.py open_run guard)."""
    register_search.open_run(_open_args(run_id="frozen_once"))
    with pytest.raises(SystemExit) as exc:
        register_search.open_run(_open_args(run_id="frozen_once"))
    assert "already registered" in str(exc.value)
    assert "immutable" in str(exc.value).lower()


@pytest.mark.parametrize(
    "payload", [[], {"clauses": []}], ids=["bare_empty_array", "empty_clauses_key"]
)
def test_zero_clause_attestation_aborts(ledger, tmp_path, payload):
    """An attestation declaring ZERO clauses must not pass vacuously.

    A per-clause for-loop check is satisfied trivially by an empty list, so a
    JSON attestation of `[]` would clear the completeness gate while declaring
    nothing — which IS the D5 failure mode (clause never simulated) and exactly
    what harvest Req 5 exists to catch. Both accepted container shapes are
    covered because each reaches the loop by a different branch.
    """
    att = _json_attestation(tmp_path, payload)
    with pytest.raises(SystemExit) as exc:
        _mf_open(ledger, tmp_path, att)
    message = str(exc.value)
    assert message.startswith("ABORT:")
    assert "ZERO clauses" in message
    assert not (ledger / "test_run.json").exists()


def test_one_complete_clause_still_passes_after_the_empty_guard(ledger, tmp_path):
    """Guard against over-correction: the empty check must not reject n=1."""
    att = _json_attestation(tmp_path, {"clauses": [_complete_clause()]})
    _mf_open(ledger, tmp_path, att, run_id="single_clause")
    manifest = json.loads((ledger / "single_clause.json").read_text(encoding="utf-8"))
    assert len(manifest["reachability_clauses"]) == 1
