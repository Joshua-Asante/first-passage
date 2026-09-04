"""Synthetic independent paths distinguish lower bounds from panel anchors."""
from dataclasses import replace
from decimal import Decimal
import json

import pandas as pd
import pytest

from research_utils.trade_reconciliation import calculate_accounting
from research_utils import tv_summary_reconciliation as summary
from test_trade_reconciliation import _spec, _trade, _trades
from test_tv_summary_reconciliation import anchor_payload, d17_payload
from test_tradeify_phase1_runner import _five_source_fixture, run_phase1, synthetic_pin_manifest
from test_tradeify_phase1_evidence_integration import summaries


PANEL = "tv_panel_max_drawdown_usd"
WALK = "max_drawdown_excursion_bounded_usd"


def trades(second_entry="2026-01-05 10:01"):
    frame = _trades(
        dict(_trade(1, net="10", cumulative="10"), mae_usd=Decimal("0")),
        dict(_trade(2, "2026-01-05 10:30", net="-4", cumulative="6"), mae_usd=Decimal("-9")),
    )
    frame.loc[1, "entry_timestamp_naive"] = pd.Timestamp(second_entry)
    return frame


@pytest.mark.parametrize("entry,overlap", [
    ("2026-01-05 09:59", True), ("2026-01-05 10:00", True), ("2026-01-05 10:01", False),
])
def test_closed_interval_overlap_comes_from_ledger_times(entry, overlap):
    for frame in (trades(entry), trades(entry).iloc[::-1]):
        result = calculate_accounting(frame)
        assert getattr(result, "has_overlap_or_tie", None) is overlap


def test_nested_and_zero_duration_intervals_are_not_lost():
    frame = trades("2026-01-05 09:59")
    frame.loc[0, "exit_timestamp_naive"] = pd.Timestamp("2026-01-05 11:00")
    frame.loc[1, "exit_timestamp_naive"] = frame.loc[1, "entry_timestamp_naive"]
    assert getattr(calculate_accounting(frame), "has_overlap_or_tie", None) is True
    assert getattr(calculate_accounting(_trades()), "has_overlap_or_tie", None) is False


def test_walk_misses_drawdown_from_intratrade_peak_without_overlap():
    # Independent synthetic path: no adverse excursion, but a peak-to-exit loss.
    true_path = [Decimal("0"), Decimal("100"), Decimal("10")]
    frame = _trades(dict(_trade(1, net="10", cumulative="10"),
                         mae_usd=Decimal("0"), mfe_usd=Decimal("100")))
    result = calculate_accounting(frame)
    assert result.max_drawdown_usd == getattr(result, WALK) == Decimal("0")
    assert max(true_path) - true_path[-1] == Decimal("90")
    assert result.max_drawdown_excursion_bounded_label == (
        "LOWER BOUND (excursion-tightened) for non-overlapping trades"
    )
    basis = result.max_drawdown_excursion_bounded_measurement_basis
    assert "MFE" in basis and "never visits" in basis
    assert "closed <= walk <= true" in basis
    assert "neither" in basis and "overlap" in basis


def inventory(tmp_path, panel, d17):
    payload = anchor_payload()
    metrics = payload["strategies"][0]["metrics"]
    metrics.pop(WALK, None)
    metrics[PANEL] = panel
    if d17:
        payload["d17_policy"] = d17_payload()["d17_policy"] | {"max_drawdown": None}
        metrics.pop("total_commissions_usd")
        metrics.pop("monthly_net_pnl_usd")
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return summary.load_summary_anchors(path, [_spec()])


@pytest.mark.parametrize("d17", [False, True])
@pytest.mark.parametrize("panel,status,issue", [
    ("8.989999", "MISMATCH", "TV_SUMMARY_MISMATCH"),
    ("8.99", "WITHIN_BOUND", None),
    ("10", "WITHIN_BOUND", None),
    ("9", "COINCIDENT", "TV_DRAWDOWN_COINCIDENT"),
])
def test_nonoverlap_dd_is_one_sided_never_a_match(tmp_path, d17, panel, status, issue):
    data = inventory(tmp_path, panel, d17)
    # Declared pyramiding does not choose the measured branch.
    spec = replace(_spec(), pine_pyramiding_pct=Decimal("100"))
    rows, issues = summary.reconcile_summary(calculate_accounting(trades()), spec, data)
    row = next(row for row in rows if row["metric"] == PANEL)
    assert row["status"] == status
    assert row["observed"] is None  # Never route the panel anchor to the computed walk field.
    assert row["anchor"] == panel
    assert row["walk_usd"] == Decimal("9")
    assert row["difference"] == Decimal("9") - Decimal(panel)
    assert row["tolerance"] == Decimal("0.01")
    assert WALK not in summary.METRICS
    assert not any(r["metric"] == WALK for r in rows)
    assert [(i.code, i.severity) for i in issues] == (
        [] if issue is None else [(issue, "BLOCKER" if status == "MISMATCH" else "INFO")]
    )
    if issue:
        assert "MFE" in issues[0].detail["measurement_basis"]


@pytest.mark.parametrize("d17", [False, True])
@pytest.mark.parametrize("entry", ["2026-01-05 09:59", "2026-01-05 10:00"])
@pytest.mark.parametrize("panel", ["1", "9", "20"])
def test_overlap_and_tie_only_record_difference(tmp_path, d17, entry, panel):
    data = inventory(tmp_path, panel, d17)
    spec = replace(_spec(), pine_pyramiding_pct=Decimal("0"))
    rows, issues = summary.reconcile_summary(calculate_accounting(trades(entry)), spec, data)
    row = next(row for row in rows if row["metric"] == PANEL)
    assert row["status"] == "RECORDED"
    assert row["has_overlap_or_tie"] is True
    assert row["difference"] == Decimal("9") - Decimal(panel)
    assert [(i.code, i.severity) for i in issues] == [("TV_DRAWDOWN_RECORDED", "INFO")]
    assert issues[0].detail["comparison"] == ("coincident" if panel == "9" else "differs")


@pytest.mark.parametrize("retired", ["max_drawdown_usd", WALK])
def test_retired_anchor_names_are_rejected(tmp_path, retired):
    payload = anchor_payload()
    metrics = payload["strategies"][0]["metrics"]
    metrics.pop(PANEL, None)
    metrics.pop(WALK, None)
    metrics[retired] = "9"
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="summary metrics keys mismatch"):
        summary.load_summary_anchors(path, [_spec()])


@pytest.mark.parametrize("value", ["RECORDED", "ACCEPTED", "", False, {}])
def test_d32_placeholder_cannot_claim_an_operator_ruling(tmp_path, value):
    payload = d17_payload()
    payload["d17_policy"]["max_drawdown"] = value
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="max_drawdown.*D32"):
        summary.load_summary_anchors(path, [_spec()])


def test_missing_d32_slot_fails_closed(tmp_path):
    payload = d17_payload()
    payload["d17_policy"].pop("max_drawdown", None)
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="d17_policy keys mismatch"):
        summary.load_summary_anchors(path, [_spec()])


def test_runner_reports_three_distinct_drawdowns_on_every_leg(tmp_path):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    path, anchors = summaries(config)
    for row in anchors["strategies"]:
        row["metrics"].pop(WALK, None)
        row["metrics"][PANEL] = "3.00"
    path.write_text(json.dumps(anchors), encoding="utf-8")
    output = tmp_path / "out"
    result = run_phase1.run_campaign(config, source_dir, output)
    manifest = json.loads(result.manifest_bytes)
    report = result.report_bytes.decode()
    for row in manifest["strategies"]:
        detail = json.loads((output / "strategy_reports" / f"{row['strategy_id']}.json").read_bytes())
        for consumer in (row, detail):
            assert consumer["max_drawdown_usd"] == "0.00"
            assert consumer[WALK] == "1.00"
            assert consumer[PANEL] == "3.00"
            assert consumer["has_overlap_or_tie"] is False
            assert consumer["max_drawdown_policy_status"] == "PENDING_D32"
        assert f"| {row['strategy_id']} | $0.00 | $1.00 | $3.00 |" in report
    assert "TV panel DD (separate anchor)" in report
    assert "LOWER BOUND (excursion-tightened) for non-overlapping trades" in report
    assert "PENDING_D32" in report
