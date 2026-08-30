"""close_run --search-log: optional actual-search-trace artifact for tools
whose K has no closed form (root-cause finding 2026-08-29). Presence-only
check (mirrors --reachability-attestation's non-empty-file gate); records
path + entry count (when JSON-list-shaped) on the manifest so a later
regret-audit has something to open. Opt-in -- omitting it changes nothing.
"""
from __future__ import annotations

import json
from argparse import Namespace

import pytest

from discovery import register_search as rs


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "discovery_manifests"
    monkeypatch.setattr(rs, "LEDGER", d)
    return d


def _open_args(**kw):
    base = dict(
        run_id="test_run",
        tool="pysr",
        search_space_size=100,
        alpha=0.05,
        data_window="2010-01-01:2020-01-01",
        hypothesis="h",
        params="",
        params_file=None,
        lane="blind",
        reachability_attestation=None,
        profile_cell=None,
        profile_consult=None,
        admission_file=None,
        prereg=None,
        cost_law_instrument=None,
        cost_law_firm_key=None,
        cost_law_panel_price=None,
        cost_law_cohort_delta_bp=None,
        cost_law_slip_ticks=None,
        cost_law_slip_convention=None,
    )
    base.update(kw)
    return Namespace(**base)


def _close_args(**kw):
    base = dict(
        run_id="test_run",
        pvalues=None,
        pvalues_file=None,
        operator_stopped=False,
        executed_k=None,
        stop_reason=None,
        executed_looks=None,
        rule_provenance_file=None,
        search_log=None,
    )
    base.update(kw)
    return Namespace(**base)


def _open_blind(ledger):
    rs.open_run(_open_args())
    assert (ledger / "test_run.json").exists()


def test_omitted_search_log_is_a_noop(ledger, tmp_path):
    _open_blind(ledger)
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")

    rs.close_run(_close_args(pvalues_file=str(pv)))

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert "search_log" not in manifest


def test_search_log_missing_file_aborts_without_write(ledger, tmp_path):
    _open_blind(ledger)
    before = (ledger / "test_run.json").read_text(encoding="utf-8")
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        rs.close_run(
            _close_args(pvalues_file=str(pv), search_log=str(tmp_path / "nope.json"))
        )
    assert "file not found" in str(exc.value)
    assert (ledger / "test_run.json").read_text(encoding="utf-8") == before


def test_search_log_empty_file_aborts_without_write(ledger, tmp_path):
    _open_blind(ledger)
    before = (ledger / "test_run.json").read_text(encoding="utf-8")
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")
    empty = tmp_path / "empty.json"
    empty.write_text("   ", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        rs.close_run(_close_args(pvalues_file=str(pv), search_log=str(empty)))
    assert "file is empty" in str(exc.value)
    assert (ledger / "test_run.json").read_text(encoding="utf-8") == before


def test_search_log_json_list_records_path_and_entry_count(ledger, tmp_path):
    _open_blind(ledger)
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")
    log = tmp_path / "restarts.json"
    log.write_text(json.dumps([{"seed": 1}, {"seed": 2}, {"seed": 3}]), encoding="utf-8")

    rs.close_run(_close_args(pvalues_file=str(pv), search_log=str(log)))

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert manifest["search_log"]["path"] == str(log)
    assert manifest["search_log"]["entry_count"] == 3


def test_search_log_non_json_prose_records_path_with_no_entry_count(ledger, tmp_path):
    _open_blind(ledger)
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")
    log = tmp_path / "restarts.txt"
    log.write_text("seed=1 attempt=1\nseed=2 attempt=1\n", encoding="utf-8")

    rs.close_run(_close_args(pvalues_file=str(pv), search_log=str(log)))

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert manifest["search_log"]["path"] == str(log)
    assert manifest["search_log"]["entry_count"] is None


def test_search_log_recorded_on_operator_stopped_closure(ledger, tmp_path):
    _open_blind(ledger)
    log = tmp_path / "restarts.json"
    log.write_text(json.dumps([{"seed": 1}]), encoding="utf-8")

    rs.close_run(
        _close_args(
            operator_stopped=True,
            executed_k=1,
            stop_reason="ran out of budget",
            executed_looks="1 look, examiner: operator",
            search_log=str(log),
        )
    )

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    assert manifest["search_log"]["entry_count"] == 1


def test_cli_parser_accepts_search_log_flag():
    parser = rs.build_parser()
    ns = parser.parse_args(
        ["close", "--run-id", "r1", "--pvalues", "0.01", "--search-log", "log.json"]
    )
    assert ns.search_log == "log.json"


def test_cli_parser_search_log_defaults_none():
    parser = rs.build_parser()
    ns = parser.parse_args(["close", "--run-id", "r1", "--pvalues", "0.01"])
    assert ns.search_log is None
