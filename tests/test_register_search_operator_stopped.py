#!/usr/bin/env python3
"""Guards on the operator-stopped closure path (ADR 2026-07-26 clause 2-C).

This path lets a campaign bank FEWER trials than it declared, so it is precisely the
code a future session could misuse to launder a search. Every guard 2-C names is
tested here as a refusal, plus the provenance the ledger must retain.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MODULE = REPO / "lab" / "discovery" / "register_search.py"


def _run(args, ledger):
    env = {"DISCOVERY_LEDGER": str(ledger)}
    import os
    e = os.environ.copy()
    e.update(env)
    return subprocess.run([sys.executable, str(MODULE)] + args,
                          capture_output=True, text=True, env=e)


@pytest.fixture
def ledger(tmp_path):
    d = tmp_path / "manifests"
    d.mkdir()
    return d


@pytest.fixture
def opened(ledger):
    # Explicit --lane blind: SPEC S6 default is mechanism-first (needs admission).
    r = _run(["open", "--run-id", "camp", "--tool", "t", "--search-space-size", "84",
              "--lane", "blind",
              "--data-window", "2010-01-01:2026-01-01", "--hypothesis", "H"], ledger)
    assert r.returncode == 0, r.stderr
    return ledger


def _manifest(ledger):
    return json.loads((ledger / "camp.json").read_text())


OK = ["close", "--run-id", "camp", "--operator-stopped", "--executed-k", "2",
      "--stop-reason", "operator halted 2026-07-26",
      "--executed-looks", "2 TV baseline panels examined by the parent session"]


def test_happy_path_banks_executed_and_retains_declared(opened):
    r = _run(OK, opened)
    assert r.returncode == 0, r.stderr
    m = _manifest(opened)
    assert m["status"] == "closed"
    assert m["K"] == 2                      # what the ledger banks
    assert m["declared_K"] == 84            # provenance, never lost
    assert m["closure_mode"] == "operator-stopped"
    assert m["results"]["n_submitted"] == 0
    assert "NO campaign verdict exists" in m["verdict"]


def test_refuses_when_pvalues_are_supplied(opened):
    """p-values imply reads executed — that campaign looked, so it banks declared K."""
    r = _run(OK + ["--pvalues", "0.01"], opened)
    assert r.returncode != 0
    assert "stopped BEFORE results" in r.stderr
    assert _manifest(opened)["status"] == "open"


def test_refuses_without_executed_k(opened):
    args = [a for a in OK if a not in ("--executed-k", "2")]
    r = _run(args, opened)
    assert r.returncode != 0
    assert "never inferred" in r.stderr


def test_refuses_to_raise_k_above_declared(opened):
    r = _run(["close", "--run-id", "camp", "--operator-stopped", "--executed-k", "85",
              "--stop-reason", "x", "--executed-looks", "y"], opened)
    assert r.returncode != 0
    assert "exceeds declared K" in r.stderr


def test_refuses_without_stop_reason(opened):
    r = _run(["close", "--run-id", "camp", "--operator-stopped", "--executed-k", "2",
              "--stop-reason", "   ", "--executed-looks", "y"], opened)
    assert r.returncode != 0
    assert "--stop-reason" in r.stderr


def test_refuses_without_enumerated_looks(opened):
    """2-C condition (iii): every executed look and its examiner, in writing."""
    r = _run(["close", "--run-id", "camp", "--operator-stopped", "--executed-k", "2",
              "--stop-reason", "x", "--executed-looks", ""], opened)
    assert r.returncode != 0
    assert "executed look" in r.stderr


def test_refuses_negative_executed_k(opened):
    r = _run(["close", "--run-id", "camp", "--operator-stopped", "--executed-k", "-1",
              "--stop-reason", "x", "--executed-looks", "y"], opened)
    assert r.returncode != 0


def test_zero_executed_k_is_allowed(opened):
    """A campaign stopped before ANY look banks zero — legitimate and must be expressible."""
    r = _run(["close", "--run-id", "camp", "--operator-stopped", "--executed-k", "0",
              "--stop-reason", "stopped at Stage-0", "--executed-looks", "none"], opened)
    assert r.returncode == 0, r.stderr
    assert _manifest(opened)["K"] == 0


def test_cannot_reclose(opened):
    assert _run(OK, opened).returncode == 0
    r = _run(OK, opened)
    assert r.returncode != 0
    assert "Cannot re-close" in r.stderr


def test_normal_pvalue_close_is_unaffected(opened):
    """The ratified 'abandoned campaigns bank their K' path must be byte-unchanged."""
    r = _run(["close", "--run-id", "camp", "--pvalues", "0.02,0.4"], opened)
    assert r.returncode == 0, r.stderr
    m = _manifest(opened)
    assert m["K"] == 84                     # declared K stands
    assert "declared_K" not in m
    assert "closure_mode" not in m
    assert m["results"]["n_submitted"] == 2
