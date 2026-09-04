"""Evidence must propagate into aggregate, human, and detailed results."""
from hashlib import sha256
import json

import pytest

from test_tradeify_phase1_runner import _five_source_fixture, run_phase1, synthetic_pin_manifest
from test_cme_calendar_evidence import calendar_fixture


def summaries(config, *, complete=True):
    p = json.loads(config.read_bytes())
    anchors = {"claim_class": "EXPLORATORY", "coverage_status": "COMPLETE" if complete else "NEEDS_CONTEXT",
               "coverage_note": "Synthetic independent panel evidence", "strategies": []}
    for s in p["strategies"]:
        anchors["strategies"].append({
            "strategy_id": s["strategy_id"], "export_sha256": s["export_sha256"],
            "source_note": "Literal synthetic operator panel, not runner output", "missing_metrics": [],
            "metrics": {"trade_count": 1, "net_pnl_usd": "0.18", "win_rate_pct": "100.00",
                        "profit_factor": None, "tv_panel_max_drawdown_usd": "1.00", "total_commissions_usd": "1.82",
                        "monthly_net_pnl_usd": {"2026-01": "0.18"}},
        })
    path = config.parent / "tv_summary_anchors.json"
    path.write_text(json.dumps(anchors), encoding="utf-8")
    return path, anchors


@pytest.mark.parametrize("mode", ["missing", "partial", "complete", "mismatch"])
def test_runner_propagates_independent_summary_evidence(tmp_path, mode):
    source_dir, config, ids = _five_source_fixture(tmp_path)
    expected_hash = None
    if mode != "missing":
        path, p = summaries(config, complete=mode != "partial")
        if mode == "partial":
            for a in p["strategies"]:
                a["missing_metrics"] = ["total_commissions_usd", "monthly_net_pnl_usd"]
                a["metrics"].update(total_commissions_usd=None, monthly_net_pnl_usd=None)
        if mode == "mismatch": p["strategies"][0]["metrics"]["tv_panel_max_drawdown_usd"] = "0.00"
        path.write_text(json.dumps(p), encoding="utf-8")
        expected_hash = sha256(path.read_bytes()).hexdigest()
    output = tmp_path / "out"
    result = run_phase1.run_campaign(config, source_dir, output)
    manifest = json.loads(result.manifest_bytes)
    report = result.report_bytes.decode()
    assert manifest["summary_reconciliation_status"] == ("COMPLETE" if mode in {"complete", "mismatch"} else "NEEDS_CONTEXT")
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"  # Calendar still missing.
    assert manifest["inputs"]["tv_summary_anchors_sha256"] == expected_hash
    assert manifest["tolerances"]["tv_summary"]["win_rate_percentage_points"] == "0.01"
    for record in manifest["strategies"]:
        detail = json.loads((output / "strategy_reports" / f"{record['strategy_id']}.json").read_bytes())
        assert detail["summary_comparisons"] == record["summary_comparisons"]
        assert detail["summary_source_note"] == record["summary_source_note"]
        assert len(record["summary_comparisons"]) == 6
        assert all("monthly_net_pnl" not in row["metric"] for row in record["summary_comparisons"])
        assert record["net_pnl_usd"] == "0.18"
        assert "monthly_net_pnl_usd" not in report
        if mode == "missing": assert all(r["status"] == "MISSING_ANCHOR" for r in record["summary_comparisons"])
        elif mode == "partial": assert any(r["status"] == "MISSING_ANCHOR" for r in record["summary_comparisons"])
        else: assert all(r["status"] != "MISSING_ANCHOR" for r in record["summary_comparisons"])
    if mode == "mismatch":
        assert manifest["strategies"][0]["issue_counts"]["TV_SUMMARY_MISMATCH"] == 1
        assert "TV_SUMMARY_MISMATCH" in report
        assert report.index("TV_SUMMARY_MISMATCH") < report.index("## Independent TradingView summary reconciliation")
        assert "panel drawdown is a separate anchor" in report
    if mode != "missing": assert "Literal synthetic operator panel" in report


def test_complete_calendar_still_capped_without_summary_and_snapshot_is_frozen(tmp_path, monkeypatch):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    path, calendar, _ = calendar_fixture(config.parent)
    calendar_path = config.parent / "cme_early_close_calendar.json"
    calendar_path.write_bytes(path.read_bytes())
    digest = sha256(calendar_path.read_bytes()).hexdigest()
    real_load = run_phase1.load_early_close_calendar
    def load_then_change_file(path):
        loaded = real_load(path)
        path.write_bytes(b"changed after load")
        return loaded
    monkeypatch.setattr(run_phase1, "load_early_close_calendar", load_then_change_file)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    manifest = json.loads(result.manifest_bytes)
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
    assert manifest["cme_early_close_calendar"]["coverage_status"] == "COMPLETE"
    assert manifest["cme_early_close_calendar"]["sources"] == calendar["sources"]
    assert manifest["inputs"]["cme_early_close_calendar_sha256"] == digest
    assert "CME holiday-short coverage is `COMPLETE`" in result.report_bytes.decode()


def test_both_complete_evidence_inventories_lift_only_context_cap(tmp_path):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    path, _, _ = calendar_fixture(config.parent)
    (config.parent / "cme_early_close_calendar.json").write_bytes(path.read_bytes())
    summaries(config)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    manifest = json.loads(result.manifest_bytes)
    assert manifest["phase1_verdict_cap"] == "COMPLETE"
    assert manifest["claim_class"] == "EXPLORATORY"
    assert manifest["campaign_status"] == "BLOCKED_EXPLORATORY"  # Continuous-roll blocker remains.


@pytest.mark.parametrize("name", ["phase1_config.json", "tradeify_commission_schedule.json", "cme_early_close_calendar.json", "tv_summary_anchors.json"])
def test_malformed_configuration_utf8_returns_two(tmp_path, capsys, name):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    (config.parent / name).write_bytes(b"\xff")
    assert run_phase1.main(["--config", str(config), "--source-dir", str(source_dir)]) == 2
    assert "configuration failure:" in capsys.readouterr().err


def test_summary_snapshot_hash_survives_later_file_change(tmp_path, monkeypatch):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    path, _ = summaries(config)
    digest = sha256(path.read_bytes()).hexdigest()
    real_load = run_phase1.load_summary_anchors
    def load_then_change_file(path, specs):
        loaded = real_load(path, specs)
        path.write_bytes(b"changed after load")
        return loaded
    monkeypatch.setattr(run_phase1, "load_summary_anchors", load_then_change_file)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    assert json.loads(result.manifest_bytes)["inputs"]["tv_summary_anchors_sha256"] == digest


def test_d17_runner_publishes_only_hashed_local_monthly_ledgers(tmp_path):
    """Publishing a monthly map in a tracked result would turn derived ledger data into an anchor."""
    source_dir, config, ids = _five_source_fixture(tmp_path)
    anchors = {
        "claim_class": "EXPLORATORY",
        "coverage_status": "NEEDS_CONTEXT",
        "coverage_note": "Replacement Key-stats panels are required for all five sources.",
        "d17_policy": {
            "ruling_date": "2026-09-03", "ruling_ref": "campaign-state §6 D17",
            "monthly_totals": "RECONSTRUCTED", "commissions": "AMENDED_OUT",
            "max_drawdown": None,
            "reason": "Monthly totals are row-ledger reconstructions and commissions have no independent total.",
        },
        "strategies": [],
    }
    (config.parent / "tv_summary_anchors.json").write_text(json.dumps(anchors), encoding="utf-8")

    output = tmp_path / "out"
    result = run_phase1.run_campaign(config, source_dir, output)
    manifest = json.loads(result.manifest_bytes)
    report = result.report_bytes.decode("utf-8")

    assert manifest["runner_version"] == "tradeify-phase1-normalization-v4"
    assert manifest["d17_policy"] == anchors["d17_policy"]
    assert "monthly_net_pnl" not in json.dumps(manifest)
    assert "monthly_net_pnl" not in report
    assert "independently reconciled" not in report
    assert set(manifest["local_monthly_reconciliation_sha256"]) == set(ids)
    for strategy_id in ids:
        local_path = output / "monthly_reconciliation" / f"{strategy_id}.json"
        local = json.loads(local_path.read_bytes())
        record = next(row for row in manifest["strategies"] if row["strategy_id"] == strategy_id)
        assert sha256(local_path.read_bytes()).hexdigest() == manifest["local_monthly_reconciliation_sha256"][strategy_id]
        assert (
            f"- Local monthly reconciliation {strategy_id}: "
            f"`{manifest['local_monthly_reconciliation_sha256'][strategy_id]}`"
        ) in report
        assert record["monthly_reconciliation"]["bucket_count"] == local["bucket_count"]
        assert record["monthly_reconciliation"]["comparison_status"] == "RECONSTRUCTED"
        assert all(comparison["metric"] not in {"total_commissions_usd", "monthly_net_pnl_usd"}
                   for comparison in record["summary_comparisons"])


def test_fee_snapshot_hash_survives_later_file_change(tmp_path, monkeypatch):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    fee_path = config.parent / "tradeify_commission_schedule.json"
    digest = sha256(fee_path.read_bytes()).hexdigest()
    real_load = run_phase1.load_fee_schedule

    def load_then_change_file(path):
        loaded = real_load(path)
        path.write_bytes(b"changed after load")
        return loaded

    monkeypatch.setattr(run_phase1, "load_fee_schedule", load_then_change_file)
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    manifest = json.loads(result.manifest_bytes)
    assert manifest["inputs"]["tradeify_commission_schedule_sha256"] == digest
    assert all(row["venue_commission_per_side_usd"] == "0.91" for row in manifest["strategies"])


def test_runner_v4_echoes_explicit_accepted_roll_policy(tmp_path):
    from test_tradeify_phase1_identity_policy import accepted_policy, OBLIGATIONS
    source_dir, config, _ = _five_source_fixture(tmp_path)
    payload = json.loads(config.read_bytes())
    payload["continuous_contract_roll_policy"] = accepted_policy()
    config.write_text(json.dumps(payload), encoding="utf-8")
    result = run_phase1.run_campaign(config, source_dir, tmp_path / "out")
    manifest = json.loads(result.manifest_bytes)
    assert manifest["runner_version"] == "tradeify-phase1-normalization-v4"
    assert manifest["continuous_contract_roll_policy"] == accepted_policy()
    assert "tradeify-phase1-normalization-v4" in result.report_bytes.decode()
    assert "ACCEPTED_UNMODELED" in result.report_bytes.decode()
    for obligation in OBLIGATIONS:
        assert obligation in result.report_bytes.decode()
    for row in manifest["strategies"]:
        assert row["continuous_contract_roll_policy"] == accepted_policy()
        assert row["status"] == "RECONCILED_EXPLORATORY"
        assert row["contract_month_attribution_status"] == "UNAVAILABLE"
        detail = json.loads((tmp_path / "out" / "strategy_reports" / f"{row['strategy_id']}.json").read_bytes())
        assert detail["continuous_contract_roll_policy"] == accepted_policy()
        roll = next(issue for issue in detail["issues"] if issue["code"] == "CONTINUOUS_CONTRACT_ROLL_UNRESOLVED")
        assert roll["severity"] == "WARNING"
        assert roll["detail"]["obligations"] == OBLIGATIONS
    assert manifest["phase1_verdict_cap"] == "NEEDS_CONTEXT"
