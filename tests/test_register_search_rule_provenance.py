"""close_run --rule-provenance-file: optional candidate provenance pointers."""
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
        tool="catch22",
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
    )
    base.update(kw)
    return Namespace(**base)


def _open_blind(ledger):
    rs.open_run(_open_args())
    assert (ledger / "test_run.json").exists()


def test_rule_provenance_recorded_when_id_matches(ledger, tmp_path):
    _open_blind(ledger)
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\ncand_b,0.002\n", encoding="utf-8")
    mapping = tmp_path / "prov.json"
    mapping.write_text(
        json.dumps({"cand_a": "lab/analysis/x/rules.json"}),
        encoding="utf-8",
    )

    rs.close_run(
        _close_args(
            pvalues_file=str(pv),
            rule_provenance_file=str(mapping),
        )
    )

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in manifest["results"]["candidates"]}
    assert by_id["cand_a"]["rule_provenance_path"] == "lab/analysis/x/rules.json"
    assert "rule_provenance_path" not in by_id["cand_b"]


def test_rule_provenance_flag_omitted_no_new_key(ledger, tmp_path):
    _open_blind(ledger)
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")

    rs.close_run(_close_args(pvalues_file=str(pv)))

    manifest = json.loads((ledger / "test_run.json").read_text(encoding="utf-8"))
    for row in manifest["results"]["candidates"]:
        assert "rule_provenance_path" not in row


def test_rule_provenance_malformed_json_aborts_without_write(ledger, tmp_path):
    _open_blind(ledger)
    before = (ledger / "test_run.json").read_text(encoding="utf-8")
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        rs.close_run(
            _close_args(
                pvalues_file=str(pv),
                rule_provenance_file=str(bad),
            )
        )
    assert "ABORT" in str(excinfo.value)
    assert "not valid JSON" in str(excinfo.value)
    assert (ledger / "test_run.json").read_text(encoding="utf-8") == before


def test_rule_provenance_non_object_json_aborts(ledger, tmp_path):
    _open_blind(ledger)
    before = (ledger / "test_run.json").read_text(encoding="utf-8")
    pv = tmp_path / "pvals.csv"
    pv.write_text("cand_a,0.001\n", encoding="utf-8")
    bad = tmp_path / "list.json"
    bad.write_text("[]", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        rs.close_run(
            _close_args(
                pvalues_file=str(pv),
                rule_provenance_file=str(bad),
            )
        )
    msg = str(excinfo.value)
    assert "ABORT" in msg
    assert "flat JSON object" in msg
    assert (ledger / "test_run.json").read_text(encoding="utf-8") == before


def test_cli_parser_accepts_rule_provenance_file_flag():
    parser = rs.build_parser()
    ns = parser.parse_args(
        [
            "close",
            "--run-id",
            "r1",
            "--pvalues",
            "0.01",
            "--rule-provenance-file",
            "map.json",
        ]
    )
    assert ns.rule_provenance_file == "map.json"
