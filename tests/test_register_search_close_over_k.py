#!/usr/bin/env python3
"""A normal p-value close must refuse more submitted results than the registered K.

Submitted p-values are a subset of the K pre-registered tests. Closing with N > K
used to warn, compute Bonferroni/BH against the smaller K and save a closed manifest
(issue #1144). The close now aborts before any manifest mutation; the registration
stays open and byte-identical. N == K stays a valid close.
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


@pytest.fixture
def ledger(tmp_path):
    d = tmp_path / "manifests"
    d.mkdir()
    return d


def _run(args, ledger, tmp_path):
    e = os.environ.copy()
    e.update({"DISCOVERY_LEDGER": str(ledger), "DISCOVERY_RESULTS_ROOTS": str(tmp_path)})
    return subprocess.run([sys.executable, str(MODULE)] + args,
                          capture_output=True, text=True, env=e)


@pytest.fixture
def opened(ledger, tmp_path):
    r = _run(["open", "--run-id", "camp", "--tool", "t", "--search-space-size", "1",
              "--lane", "blind",
              "--data-window", "2010-01-01:2026-01-01", "--hypothesis", "H"],
             ledger, tmp_path)
    assert r.returncode == 0, r.stderr
    return ledger


def _manifest_path(ledger):
    return ledger / "camp.json"


def _assert_refused_unchanged(r, ledger, before):
    assert r.returncode != 0
    assert "ABORT:" in r.stderr
    assert "registered K=1" in r.stderr
    assert "[close]" not in r.stdout
    assert _manifest_path(ledger).read_bytes() == before   # no save
    m = json.loads(before)
    assert m["status"] == "open"
    assert m["results"] is None


def test_pvalues_above_k_abort_and_registration_stays_open(opened, tmp_path):
    before = _manifest_path(opened).read_bytes()
    r = _run(["close", "--run-id", "camp", "--pvalues", ".06,.06"], opened, tmp_path)
    _assert_refused_unchanged(r, opened, before)


def test_pvalues_file_above_k_aborts(opened, tmp_path):
    before = _manifest_path(opened).read_bytes()
    pfile = tmp_path / "pvals.csv"
    pfile.write_text("# id,p\ncand_a,0.06\ncand_b,0.06\n", encoding="utf-8")
    r = _run(["close", "--run-id", "camp", "--pvalues-file", str(pfile)], opened, tmp_path)
    _assert_refused_unchanged(r, opened, before)


def test_refused_registration_can_still_close_validly(opened, tmp_path):
    r = _run(["close", "--run-id", "camp", "--pvalues", ".06,.06"], opened, tmp_path)
    assert r.returncode != 0
    r = _run(["close", "--run-id", "camp", "--pvalues", ".06"], opened, tmp_path)
    assert r.returncode == 0, r.stderr
    assert json.loads(_manifest_path(opened).read_text())["status"] == "closed"


def test_pvalues_equal_to_k_close_normally(opened, tmp_path):
    r = _run(["close", "--run-id", "camp", "--pvalues", "0.02"], opened, tmp_path)
    assert r.returncode == 0, r.stderr
    m = json.loads(_manifest_path(opened).read_text())
    assert m["status"] == "closed"
    assert m["K"] == 1
    assert m["results"]["n_submitted"] == 1
    assert m["results"]["n_pass_bh"] == 1


def test_pvalues_file_equal_to_k_close_normally(opened, tmp_path):
    pfile = tmp_path / "pvals.csv"
    pfile.write_text("cand_a,0.2\n", encoding="utf-8")
    r = _run(["close", "--run-id", "camp", "--pvalues-file", str(pfile)], opened, tmp_path)
    assert r.returncode == 0, r.stderr
    m = json.loads(_manifest_path(opened).read_text())
    assert m["status"] == "closed"
    assert m["results"]["n_submitted"] == 1
    assert m["results"]["n_pass_bh"] == 0
