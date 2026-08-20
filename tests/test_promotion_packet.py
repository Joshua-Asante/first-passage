"""SPEC S5 — promotion packet validator + refuter fixtures.

Gate: clean_packet.json must Pass; confabulated_packet.json must Fail.
"""
from __future__ import annotations

import json
from pathlib import Path

from discovery.promotion_packet import validate_promotion_packet
from discovery.promotion_refuter import refute_promotion_packet

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "promotion"
CLEAN = FIXTURES / "clean_packet.json"
CONFAB = FIXTURES / "confabulated_packet.json"


def test_clean_packet_passes_validator():
    result = validate_promotion_packet(CLEAN, repo_root=REPO_ROOT)
    assert result.decision == "Pass", result.reasons
    assert result.ok


def test_confabulated_packet_fails_validator():
    result = validate_promotion_packet(CONFAB, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert not result.ok
    # Must catch at least the confabulation limbs baked into the fixture.
    joined = " ".join(result.reasons)
    assert "freeze_commit_mismatch" in joined
    assert "prose_keys" in joined or "artifact_path_empty" in joined
    assert "units_mismatch" in joined or "basis_forbidden" in joined


def test_clean_packet_passes_refuter():
    result = refute_promotion_packet(CLEAN, repo_root=REPO_ROOT)
    assert result.decision == "Pass", result.reasons


def test_confabulated_packet_fails_refuter_precondition():
    result = refute_promotion_packet(CONFAB, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert "refuter:precondition_validate_fail" in result.reasons


def test_ceiling_cross_rejected():
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["sandbox"]["loss_budget_usd"] = 9999.0
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any(r.startswith("ceiling:") for r in result.reasons)


def test_missing_artifact_rejected_when_repo_root_set():
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["claims"][0]["artifact_path"] = "tests/fixtures/promotion/artifacts/nope.json"
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any("artifact_missing" in r for r in result.reasons)


def test_clean_packet_without_discovery_run_id_still_passes():
    """Optional field (2026-08-19 K-ledger check) -- absence is the status quo."""
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    assert "discovery_run_id" not in packet
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.ok, result.reasons


def test_discovery_run_id_backed_by_closed_manifest_passes(tmp_path, monkeypatch):
    monkeypatch.setenv("DISCOVERY_LEDGER", str(tmp_path))
    (tmp_path / "backing_run.json").write_text(
        json.dumps({"run_id": "backing_run", "status": "closed", "K": 2,
                    "results": {"n_submitted": 1}}),
        encoding="utf-8",
    )
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["discovery_run_id"] = "backing_run"
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.ok, result.reasons


def test_discovery_run_id_with_no_manifest_fails(tmp_path, monkeypatch):
    monkeypatch.setenv("DISCOVERY_LEDGER", str(tmp_path))
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["discovery_run_id"] = "no_such_run"
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any("discovery_run_id_unbacked:no_manifest" in r for r in result.reasons)


def test_discovery_run_id_pointing_at_open_manifest_fails(tmp_path, monkeypatch):
    monkeypatch.setenv("DISCOVERY_LEDGER", str(tmp_path))
    (tmp_path / "still_open.json").write_text(
        json.dumps({"run_id": "still_open", "status": "open", "K": 2, "results": None}),
        encoding="utf-8",
    )
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["discovery_run_id"] = "still_open"
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any("manifest_not_closed" in r for r in result.reasons)


def test_discovery_run_id_empty_string_fails():
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["discovery_run_id"] = "   "
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert "discovery_run_id_empty" in result.reasons
