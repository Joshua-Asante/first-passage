"""--lane deep wiring on register_search.open_run (charter §7 step 2 / GROW
spec v2 Part A). Mirrors the fixture shape of test_discovery_register_search.py.

Deep lane requires: --prereg (like mechanism-first), --grammar-file +
--grammar-sha256 (drift-checked), --confirm-years, --target-sr. It does NOT
require the HARV reachability-attestation JSON (that machinery belongs to
S6/TNEC-1's mechanism-first corridor, a different admission predicate at a
different threshold -- charter §2.2 is the deep-lane's own gate).
"""
from __future__ import annotations

import json
from argparse import Namespace
from pathlib import Path

import pytest

from discovery import register_search
from discovery.grammar import sha256_of_grammar
from research_utils.repo_root import repo_root


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "ledger"
    monkeypatch.setattr(register_search, "LEDGER", d)
    return d


_REAL_PREREG = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"


def _prereg_file(tmp_path, name="prereg.md"):
    # _require_prereg resolves the path relative to repo root -- a tmp_path
    # file is outside the repo, so this test suite reuses a real committed
    # prereg's path, matching test_discovery_register_search.py's own
    # pattern rather than re-deriving a workaround.
    return _REAL_PREREG


def _grammar_file(tmp_path, generation_budget=10, name="grammar.json"):
    p = tmp_path / name
    p.write_text(
        json.dumps(
            {
                "generation_budget": generation_budget,
                "families": {"sizing_policy": ["flat", "cushion_proportional"]},
            }
        ),
        encoding="utf-8",
    )
    return str(p)


def _deep_args(tmp_path, **kw):
    grammar_path = kw.pop("grammar_file", None) or _grammar_file(tmp_path)
    base = dict(
        run_id="deep_run", tool="grammar-refine", search_space_size=10,
        alpha=0.05, data_window="2010-01-01:2020-01-01",
        hypothesis="h", params="", params_file=None,
        lane="deep", instrument="MGC",
        reachability_attestation=None,
        profile_cell=None, profile_consult=None,
        admission_file=None,
        prereg=_prereg_file(tmp_path),
        grammar_file=grammar_path,
        grammar_sha256=sha256_of_grammar(grammar_path),
        confirm_years=6.5,
        target_sr=1.83,
    )
    base.update(kw)
    return Namespace(**base)


def test_deep_lane_admits_and_writes_manifest(ledger, tmp_path):
    args = _deep_args(tmp_path)
    register_search.open_run(args)
    manifest = json.loads((ledger / "deep_run.json").read_text())
    assert manifest["lane"] == "deep"
    assert manifest["K"] == 10
    assert manifest["deep_admission"]["decision"] == "ADMIT"
    assert manifest["grammar_sha256"] == args.grammar_sha256


def test_deep_lane_requires_prereg(ledger, tmp_path):
    args = _deep_args(tmp_path, prereg=None)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    assert not (ledger / "deep_run.json").exists()


def test_deep_lane_requires_grammar_file(ledger, tmp_path):
    args = _deep_args(tmp_path, grammar_file=None, grammar_sha256=None)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    assert not (ledger / "deep_run.json").exists()


def test_deep_lane_refuses_on_grammar_hash_drift(ledger, tmp_path):
    args = _deep_args(tmp_path, grammar_sha256="0" * 64)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    assert not (ledger / "deep_run.json").exists()


def test_deep_lane_refuses_when_search_space_size_mismatches_grammar_budget(
    ledger, tmp_path
):
    args = _deep_args(tmp_path, search_space_size=999)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    assert not (ledger / "deep_run.json").exists()


def test_deep_lane_refuses_k_above_33_no_manifest_written(ledger, tmp_path):
    args = _deep_args(
        tmp_path,
        search_space_size=40,
        grammar_file=_grammar_file(tmp_path, generation_budget=40),
    )
    args.grammar_sha256 = sha256_of_grammar(args.grammar_file)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    assert not (ledger / "deep_run.json").exists()


def test_deep_lane_refuses_underpowered_target_no_manifest_written(ledger, tmp_path):
    args = _deep_args(tmp_path, target_sr=0.1)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    assert not (ledger / "deep_run.json").exists()


def test_deep_lane_requires_confirm_years_and_target_sr(ledger, tmp_path):
    args = _deep_args(tmp_path, confirm_years=None)
    with pytest.raises(SystemExit):
        register_search.open_run(args)
    args2 = _deep_args(tmp_path, target_sr=None)
    with pytest.raises(SystemExit):
        register_search.open_run(args2)


def test_deep_lane_does_not_require_harv_reachability_attestation(ledger, tmp_path):
    """Deep lane's admission is charter §2.2, not S6/TNEC-1's mechanism-first
    corridor -- it must NOT demand the HARV attestation JSON mechanism-first
    requires; conflating the two lanes' doctrines is exactly what the
    2026-08-22 dual-panel review flagged (finding B3) in GROW spec v1."""
    args = _deep_args(tmp_path)
    assert args.reachability_attestation is None
    register_search.open_run(args)  # must not raise
    assert (ledger / "deep_run.json").exists()


def test_blind_lane_unaffected_by_deep_lane_wiring(ledger, tmp_path):
    args = Namespace(
        run_id="blind_run", tool="stumpy", search_space_size=48000,
        alpha=0.05, data_window="2010-01-01:2020-01-01",
        hypothesis="h", params="", params_file=None,
        lane="blind", reachability_attestation=None,
        profile_cell=None, profile_consult=None, admission_file=None,
        prereg=None,
    )
    register_search.open_run(args)
    manifest = json.loads((ledger / "blind_run.json").read_text())
    assert "lane" not in manifest
    assert "grammar_sha256" not in manifest
    assert "deep_admission" not in manifest
