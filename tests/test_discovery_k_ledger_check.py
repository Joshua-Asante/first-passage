"""K-ledger backing check — verify_manifest_backing().

Does not re-derive K/Bonferroni/BH-FDR; only checks a declared run_id has a
CLOSED manifest with recorded results. Paired positive/negative fixtures.
"""
from __future__ import annotations

import json

from discovery.k_ledger_check import verify_manifest_backing


def _write_manifest(tmp_path, run_id, **fields):
    payload = {
        "run_id": run_id,
        "status": "closed",
        "K": 2,
        "results": {"n_submitted": 1},
    }
    payload.update(fields)
    (tmp_path / f"{run_id}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_missing_manifest_fails():
    result = verify_manifest_backing("nope", ledger_dir="/no/such/dir")
    assert not result.ok
    assert "no_manifest" in result.reasons
    assert result.manifest is None


def test_closed_manifest_with_results_ok(tmp_path):
    _write_manifest(tmp_path, "run_a")
    result = verify_manifest_backing("run_a", ledger_dir=tmp_path)
    assert result.ok
    assert result.reasons == ()
    assert result.manifest["K"] == 2


def test_open_manifest_not_closed_fails(tmp_path):
    _write_manifest(tmp_path, "run_b", status="open", results=None)
    result = verify_manifest_backing("run_b", ledger_dir=tmp_path)
    assert not result.ok
    assert "manifest_not_closed" in result.reasons
    assert "no_results" in result.reasons


def test_invalid_k_fails(tmp_path):
    _write_manifest(tmp_path, "run_c", K=0)
    result = verify_manifest_backing("run_c", ledger_dir=tmp_path)
    assert not result.ok
    assert "k_missing_or_invalid" in result.reasons


def test_operator_stopped_closure_with_valid_k_passes(tmp_path):
    """Operator-stopped closures (ADR 2026-07-26 clause 2-C) still close with a
    banked K and a results block -- this check does not re-litigate that path."""
    _write_manifest(
        tmp_path,
        "run_d",
        K=2,
        results={"n_submitted": 0, "executed_k": 2, "declared_k": 84, "candidates": []},
        closure_mode="operator-stopped",
    )
    result = verify_manifest_backing("run_d", ledger_dir=tmp_path)
    assert result.ok
