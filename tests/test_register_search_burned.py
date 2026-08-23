"""burned_segments wiring into register_search.open_run (GROW Boundary / B1).

Deep lane: overlap refuses with no manifest write. Unlisted windows open and
record consultation_count=0 + empty history — never a silent "clean" boolean.
§2.2(iv) disclosure is not a refuse.
"""
from __future__ import annotations

import json
from argparse import Namespace

import pytest

from discovery import register_search
from discovery.grammar import sha256_of_grammar


_REAL_PREREG = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
_SEED_WINDOW = "2025-09-01:2026-08-05"


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    d = tmp_path / "ledger"
    monkeypatch.setattr(register_search, "LEDGER", d)
    return d


def _grammar_file(tmp_path, generation_budget=10):
    p = tmp_path / "grammar.json"
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
        run_id="deep_burned",
        tool="grammar-refine",
        search_space_size=10,
        alpha=0.05,
        data_window="2010-01-01:2011-01-01",
        hypothesis="h",
        params="",
        params_file=None,
        lane="deep",
        instrument="MGC",
        reachability_attestation=None,
        profile_cell=None,
        profile_consult=None,
        admission_file=None,
        prereg=_REAL_PREREG,
        grammar_file=grammar_path,
        grammar_sha256=sha256_of_grammar(grammar_path),
        confirm_years=6.5,
        target_sr=1.83,
    )
    base.update(kw)
    return Namespace(**base)


def test_deep_open_refuses_seed_mnq_window_no_manifest(ledger, tmp_path):
    args = _deep_args(
        tmp_path,
        instrument="MNQ",
        data_window=_SEED_WINDOW,
    )
    with pytest.raises(SystemExit, match="burned"):
        register_search.open_run(args)
    assert not (ledger / "deep_burned.json").exists()


def test_deep_open_refuses_overlap_subwindow_no_manifest(ledger, tmp_path):
    args = _deep_args(
        tmp_path,
        instrument="MNQ",
        data_window="2025-10-01:2025-11-01",
    )
    with pytest.raises(SystemExit, match="burned"):
        register_search.open_run(args)
    assert not (ledger / "deep_burned.json").exists()


def test_deep_open_unlisted_window_discloses_zero_not_clean(ledger, tmp_path):
    args = _deep_args(tmp_path, instrument="MGC", data_window="2010-01-01:2011-01-01")
    register_search.open_run(args)
    manifest = json.loads((ledger / "deep_burned.json").read_text())
    block = manifest["burned_consultation"]
    assert block["instrument"] == "MGC"
    assert block["window_start"] == "2010-01-01"
    assert block["window_end"] == "2011-01-01"
    assert block["consultation_count"] == 0
    assert block["consultation_history"] == []
    assert "clean" not in block


def test_deep_open_requires_instrument_no_manifest(ledger, tmp_path):
    args = _deep_args(tmp_path, instrument=None)
    with pytest.raises(SystemExit, match="instrument"):
        register_search.open_run(args)
    assert not (ledger / "deep_burned.json").exists()


def test_blind_open_does_not_gain_burned_consultation_key(ledger, tmp_path):
    args = Namespace(
        run_id="blind_run",
        tool="stumpy",
        search_space_size=48000,
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
    )
    register_search.open_run(args)
    manifest = json.loads((ledger / "blind_run.json").read_text())
    assert "burned_consultation" not in manifest
    assert "lane" not in manifest
