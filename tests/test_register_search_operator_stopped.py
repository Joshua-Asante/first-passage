#!/usr/bin/env python3
"""Guards on the operator-stopped closure path (ADR 2026-07-26 clause 2-C).

This path lets a campaign bank FEWER trials than it declared, so it is precisely the
code a future session could misuse to launder a search. The tool must enforce 2-C's
conditions, not assert them: (i) no results artifact names the campaign, (iii) an
enumerated look/examiner list whose length is the bank, (ii) and (iv) recorded as
required attestations, and a verdict written from those inputs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MODULE = REPO / "lab" / "discovery" / "register_search.py"

TWO_LOOKS = [
    {"look": "MNQ 1-yr TV baseline panel", "examiner": "parent advisor session"},
    {"look": "MYM 1-yr TV baseline panel", "examiner": "parent advisor session"},
]


@pytest.fixture
def results_root(tmp_path):
    d = tmp_path / "lab"
    (d / "analysis" / "other_camp").mkdir(parents=True)
    # An unrelated RESULTS file: must be scanned and must not match.
    (d / "analysis" / "other_camp" / "RESULTS.md").write_text(
        "**Campaign:** `camp_two` -- not this one\n", encoding="utf-8")
    return d


@pytest.fixture
def ledger(tmp_path):
    d = tmp_path / "manifests"
    d.mkdir()
    return d


def _run(args, ledger, results_root):
    e = os.environ.copy()
    e.update({"DISCOVERY_LEDGER": str(ledger), "DISCOVERY_RESULTS_ROOTS": str(results_root)})
    return subprocess.run([sys.executable, str(MODULE)] + args,
                          capture_output=True, text=True, env=e)


@pytest.fixture
def opened(ledger, results_root):
    # Explicit --lane blind: SPEC S6 default is mechanism-first (needs admission).
    r = _run(["open", "--run-id", "camp", "--tool", "t", "--search-space-size", "84",
              "--lane", "blind",
              "--data-window", "2010-01-01:2026-01-01", "--hypothesis", "H"],
             ledger, results_root)
    assert r.returncode == 0, r.stderr
    return ledger


def _looks_file(tmp_path, looks, name="looks.json"):
    p = tmp_path / name
    p.write_text(json.dumps(looks), encoding="utf-8")
    return str(p)


def _close(tmp_path, executed_k=2, looks=TWO_LOOKS, **override):
    flags = {
        "--executed-k": str(executed_k),
        "--stop-reason": "operator halted 2026-07-26",
        "--executed-looks-file": _looks_file(tmp_path, looks),
        "--non-execution-evidence": "run_campaign.py never invoked; no outputs under lab/",
        "--operator-signoff": "'Supertrend is closed.' -- operator, 2026-07-26",
    }
    flags.update(override)
    args = ["close", "--run-id", "camp", "--operator-stopped"]
    for k, v in flags.items():
        if v is not None:
            args += [k, v]
    return args


def _manifest(ledger):
    return json.loads((ledger / "camp.json").read_text())


def test_happy_path_banks_enumerated_looks_and_retains_declared(opened, results_root, tmp_path):
    r = _run(_close(tmp_path), opened, results_root)
    assert r.returncode == 0, r.stderr
    m = _manifest(opened)
    assert m["status"] == "closed"
    assert m["K"] == 2                      # what the ledger banks
    assert m["declared_K"] == 84            # provenance, never lost
    assert m["closure_mode"] == "operator-stopped"
    assert m["results"]["n_submitted"] == 0
    assert m["executed_looks"] == TWO_LOOKS
    assert m["operator_signoff"].startswith("'Supertrend is closed.'")
    assert m["non_execution_evidence"]
    check = m["results_artifact_check"]
    assert check["matches"] == [] and check["files_scanned"] == 1
    assert check["scope"] == "checkout"


def test_verdict_is_written_from_inputs_not_boilerplate(opened, results_root, tmp_path):
    """Regression for the fixed 'before declared reads executed' text, which was
    written whatever the closure note said (2-C enumeration check, 2026-11-08)."""
    assert _run(_close(tmp_path), opened, results_root).returncode == 0
    v = _manifest(opened)["verdict"]
    assert "before declared reads executed" not in v
    assert v.startswith("OPERATOR-STOPPED")
    assert "2 enumerated executed look(s)" in v
    for look in TWO_LOOKS:
        assert look["look"] in v and look["examiner"] in v
    assert "1 scanned" in v
    assert "not verified by this tool" in v


def test_refuses_when_a_results_artifact_names_the_campaign(opened, results_root, tmp_path):
    """2-C condition (i): a RESULTS file attributing itself to the campaign means it
    examined results -- the orb_mnq_intraday_breakout failure shape."""
    stage = results_root / "analysis" / "camp_2026-07"
    stage.mkdir()
    (stage / "RESULTS_stage6.md").write_text("**Campaign:** `camp`\n", encoding="utf-8")
    r = _run(_close(tmp_path), opened, results_root)
    assert r.returncode != 0
    assert "condition (i)" in r.stderr
    assert "RESULTS_stage6.md" in r.stderr
    assert _manifest(opened)["status"] == "open"


def test_results_match_is_whole_token(opened, results_root, tmp_path):
    """`camp` must not match `camp_two` or `pre-camp`; only the run id itself."""
    (results_root / "analysis" / "other_camp" / "RESULTS_b.md").write_text(
        "pre-camp and camp_two and camps\n", encoding="utf-8")
    r = _run(_close(tmp_path), opened, results_root)
    assert r.returncode == 0, r.stderr


def test_refuses_when_results_root_is_missing(opened, tmp_path):
    r = _run(_close(tmp_path), opened, tmp_path / "no_such_root")
    assert r.returncode != 0
    assert "cannot be checked" in r.stderr
    assert _manifest(opened)["status"] == "open"


def test_refuses_when_executed_k_disagrees_with_enumeration(opened, results_root, tmp_path):
    """The bank is the enumeration's length -- 'none' with K>0, or looks with K=0,
    are both incoherent (the q_txg1 / ORB failure shapes)."""
    r = _run(_close(tmp_path, executed_k=0), opened, results_root)
    assert r.returncode != 0
    assert "enumerated looks" in r.stderr
    r = _run(_close(tmp_path, executed_k=1, looks=[]), opened, results_root)
    assert r.returncode != 0
    assert "enumerated looks" in r.stderr
    assert _manifest(opened)["status"] == "open"


def test_refuses_without_looks_file(opened, results_root, tmp_path):
    """2-C condition (iii): every executed look and its examiner, in writing."""
    r = _run(_close(tmp_path, **{"--executed-looks-file": None}), opened, results_root)
    assert r.returncode != 0
    assert "executed look" in r.stderr


def test_old_free_text_looks_flag_is_gone(opened, results_root, tmp_path):
    r = _run(_close(tmp_path) + ["--executed-looks", "none"], opened, results_root)
    assert r.returncode != 0
    assert _manifest(opened)["status"] == "open"


@pytest.mark.parametrize("bad", [
    "not json",
    json.dumps({"look": "x", "examiner": "y"}),               # not a list
    json.dumps([{"look": "x"}]),                              # examiner missing
    json.dumps([{"look": "x", "examiner": "  "}]),            # blank examiner
    json.dumps([{"look": "x", "examiner": "y", "pf": 1.2}]),  # extra key
    json.dumps(["MNQ panel"]),                                # bare string
])
def test_refuses_malformed_looks(opened, results_root, tmp_path, bad):
    p = tmp_path / "bad.json"
    p.write_text(bad, encoding="utf-8")
    r = _run(_close(tmp_path, executed_k=1, **{"--executed-looks-file": str(p)}),
             opened, results_root)
    assert r.returncode != 0
    assert _manifest(opened)["status"] == "open"


@pytest.mark.parametrize("flag,needle", [
    ("--non-execution-evidence", "condition ii"),
    ("--operator-signoff", "condition iv"),
    ("--stop-reason", "--stop-reason"),
])
def test_refuses_without_attestation(opened, results_root, tmp_path, flag, needle):
    r = _run(_close(tmp_path, **{flag: "   "}), opened, results_root)
    assert r.returncode != 0
    assert needle in r.stderr
    assert _manifest(opened)["status"] == "open"


def test_refuses_when_pvalues_are_supplied(opened, results_root, tmp_path):
    """p-values imply reads executed — that campaign looked, so it banks declared K."""
    r = _run(_close(tmp_path) + ["--pvalues", "0.01"], opened, results_root)
    assert r.returncode != 0
    assert "stopped BEFORE results" in r.stderr
    assert _manifest(opened)["status"] == "open"


def test_refuses_without_executed_k(opened, results_root, tmp_path):
    r = _run(_close(tmp_path, **{"--executed-k": None}), opened, results_root)
    assert r.returncode != 0
    assert "never inferred" in r.stderr


def test_refuses_to_raise_k_above_declared(opened, results_root, tmp_path):
    r = _run(_close(tmp_path, executed_k=85), opened, results_root)
    assert r.returncode != 0
    assert "exceeds declared K" in r.stderr


def test_refuses_negative_executed_k(opened, results_root, tmp_path):
    r = _run(_close(tmp_path, executed_k=-1), opened, results_root)
    assert r.returncode != 0


def test_zero_executed_k_is_allowed(opened, results_root, tmp_path):
    """A campaign stopped before ANY look banks zero — legitimate and must be expressible."""
    r = _run(_close(tmp_path, executed_k=0, looks=[]), opened, results_root)
    assert r.returncode == 0, r.stderr
    m = _manifest(opened)
    assert m["K"] == 0
    assert m["executed_looks"] == []
    assert "0 enumerated executed looks" in m["verdict"]


def test_cannot_reclose(opened, results_root, tmp_path):
    assert _run(_close(tmp_path), opened, results_root).returncode == 0
    r = _run(_close(tmp_path), opened, results_root)
    assert r.returncode != 0
    assert "Cannot re-close" in r.stderr


def test_normal_pvalue_close_is_unaffected(opened, results_root):
    """The ratified 'abandoned campaigns bank their K' path must be unchanged,
    including when a results artifact names the campaign."""
    stage = results_root / "analysis" / "camp_2026-07"
    stage.mkdir()
    (stage / "RESULTS.md").write_text("**Campaign:** `camp`\n", encoding="utf-8")
    r = _run(["close", "--run-id", "camp", "--pvalues", "0.02,0.4"], opened, results_root)
    assert r.returncode == 0, r.stderr
    m = _manifest(opened)
    assert m["K"] == 84                     # declared K stands
    assert "declared_K" not in m
    assert "closure_mode" not in m
    assert "results_artifact_check" not in m
    assert m["results"]["n_submitted"] == 2
