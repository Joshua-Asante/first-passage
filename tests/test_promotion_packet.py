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


def _backed_packet_at_k(tmp_path, monkeypatch, k: int) -> dict:
    monkeypatch.setenv("DISCOVERY_LEDGER", str(tmp_path))
    run_id = f"backing_run_k{k}"
    (tmp_path / f"{run_id}.json").write_text(
        json.dumps({"run_id": run_id, "status": "closed", "K": k,
                    "results": {"n_submitted": 1}}),
        encoding="utf-8",
    )
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["discovery_run_id"] = run_id
    return packet


def test_k_within_reachable_band_needs_no_dsr_floor_attestation(tmp_path, monkeypatch):
    """K=2 -> floor_at_k(2) <= CAP; unchanged status quo, no new requirement."""
    packet = _backed_packet_at_k(tmp_path, monkeypatch, k=2)
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.ok, result.reasons


def test_k_above_reachable_band_without_dsr_floor_attestation_fails(tmp_path, monkeypatch):
    """K=5 -> floor_at_k(5) > CAP; no dsr_floor attestation at all -> refuse."""
    packet = _backed_packet_at_k(tmp_path, monkeypatch, k=5)
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any(r.startswith("discovery_run_id_k_conditional_floor_missing:") for r in result.reasons)


def test_k_above_reachable_band_with_understated_hurdle_fails(tmp_path, monkeypatch):
    """A dsr_floor attestation is present but its hurdle is a stale/lower-K value."""
    packet = _backed_packet_at_k(tmp_path, monkeypatch, k=5)
    packet["gate_attestations"].append({
        "gate_id": "dsr_floor",
        "units": "annualized_sharpe",
        "measured_value": 1.10,
        "hurdle_value": 0.95,  # stale K<=3-era hurdle, not floor_at_k(5)
        "basis": "is_panel",
        "artifact_path": "tests/fixtures/promotion/artifacts/gate_stage2.json",
    })
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any(r.startswith("discovery_run_id_k_conditional_floor_understated:") for r in result.reasons)


def test_k_above_reachable_band_with_correct_dsr_floor_attestation_passes(tmp_path, monkeypatch):
    from research_utils.axis_screen import floor_at_k

    packet = _backed_packet_at_k(tmp_path, monkeypatch, k=5)
    packet["gate_attestations"].append({
        "gate_id": "dsr_floor",
        "units": "annualized_sharpe",
        "measured_value": floor_at_k(5) + 0.05,
        "hurdle_value": floor_at_k(5),
        "basis": "is_panel",
        "artifact_path": "tests/fixtures/promotion/artifacts/gate_stage2.json",
    })
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.ok, result.reasons


def test_k_above_reachable_band_with_nan_hurdle_fails(tmp_path, monkeypatch):
    """NaN passes isinstance(x, (int, float)) and `NaN < anything` is False --
    would otherwise silently satisfy the mandatory floor without declaring a
    real hurdle (Codex review, PR #218)."""
    packet = _backed_packet_at_k(tmp_path, monkeypatch, k=5)
    packet["gate_attestations"].append({
        "gate_id": "dsr_floor",
        "units": "annualized_sharpe",
        "measured_value": 1.10,
        "hurdle_value": float("nan"),
        "basis": "is_panel",
        "artifact_path": "tests/fixtures/promotion/artifacts/gate_stage2.json",
    })
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any(r.startswith("discovery_run_id_k_conditional_floor_understated:") for r in result.reasons)


def test_k_above_reachable_band_with_inf_hurdle_fails(tmp_path, monkeypatch):
    """+inf is also a float that would otherwise trivially clear any floor."""
    packet = _backed_packet_at_k(tmp_path, monkeypatch, k=5)
    packet["gate_attestations"].append({
        "gate_id": "dsr_floor",
        "units": "annualized_sharpe",
        "measured_value": 1.10,
        "hurdle_value": float("inf"),
        "basis": "is_panel",
        "artifact_path": "tests/fixtures/promotion/artifacts/gate_stage2.json",
    })
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any(r.startswith("discovery_run_id_k_conditional_floor_understated:") for r in result.reasons)


def _backed_packet_deep_lane(tmp_path, monkeypatch, k: int, confirm_years: float) -> dict:
    from research_utils.axis_screen import floor_at_k

    monkeypatch.setenv("DISCOVERY_LEDGER", str(tmp_path))
    run_id = f"backing_deep_k{k}"
    deep_floor = floor_at_k(k, years=confirm_years)
    (tmp_path / f"{run_id}.json").write_text(
        json.dumps({
            "run_id": run_id, "status": "closed", "K": k,
            "results": {"n_submitted": 1},
            "lane": "deep",
            "confirm_years": confirm_years,
            "deep_admission": {"decision": "ADMIT", "floor_at_k": deep_floor},
        }),
        encoding="utf-8",
    )
    packet = json.loads(CLEAN.read_text(encoding="utf-8"))
    packet["discovery_run_id"] = run_id
    return packet


def test_deep_lane_short_confirm_horizon_hurdle_between_default_and_true_floor_fails(
    tmp_path, monkeypatch
):
    """K=10, confirm_years=3.25 -> true floor 1.79; the module's default-years
    floor would be 1.265. A hurdle of 1.30 clears the wrong (default-years)
    floor but not the campaign's own recorded one (Codex review, PR #218)."""
    from research_utils.axis_screen import floor_at_k

    packet = _backed_packet_deep_lane(tmp_path, monkeypatch, k=10, confirm_years=3.25)
    assert floor_at_k(10) == 1.265  # the wrong floor this fix must not use
    assert floor_at_k(10, years=3.25) == 1.79  # the campaign's true floor
    packet["gate_attestations"].append({
        "gate_id": "dsr_floor",
        "units": "annualized_sharpe",
        "measured_value": 1.35,
        "hurdle_value": 1.30,
        "basis": "is_panel",
        "artifact_path": "tests/fixtures/promotion/artifacts/gate_stage2.json",
    })
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.decision == "Fail"
    assert any(
        r.startswith("discovery_run_id_k_conditional_floor_understated:")
        for r in result.reasons
    )


def test_deep_lane_hurdle_meeting_true_confirm_years_floor_passes(tmp_path, monkeypatch):
    from research_utils.axis_screen import floor_at_k

    packet = _backed_packet_deep_lane(tmp_path, monkeypatch, k=10, confirm_years=3.25)
    true_floor = floor_at_k(10, years=3.25)
    packet["gate_attestations"].append({
        "gate_id": "dsr_floor",
        "units": "annualized_sharpe",
        "measured_value": true_floor + 0.05,
        "hurdle_value": true_floor,
        "basis": "is_panel",
        "artifact_path": "tests/fixtures/promotion/artifacts/gate_stage2.json",
    })
    result = validate_promotion_packet(packet, repo_root=REPO_ROOT)
    assert result.ok, result.reasons
