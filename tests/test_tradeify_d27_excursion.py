"""D27 synthetic walk contracts, independent literals and real consumers."""
from decimal import Decimal
import json

import pytest

from research_utils.trade_reconciliation import calculate_accounting
from research_utils.tv_summary_reconciliation import load_summary_anchors, reconcile_summary
from test_trade_reconciliation import _trade, _trades, _spec
from test_tv_summary_reconciliation import anchor_payload, d17_payload
from test_tradeify_phase1_runner import _five_source_fixture, run_phase1, synthetic_pin_manifest


DD = "max_drawdown_excursion_bounded_usd"


def ledger(mae="-9"):
    return _trades(
        dict(_trade(1, net="10", cumulative="10"), mae_usd=Decimal("-1")),
        dict(_trade(2, net="-4", cumulative="6"), mae_usd=mae),
    )


@pytest.mark.parametrize("mae", ["-9", "9", Decimal("-9"), Decimal("9")])
def test_excursion_precedes_settlement_and_preserves_closed_metrics(mae):
    result = calculate_accounting(ledger(mae))
    assert getattr(result, DD, None) == Decimal("9.00")
    assert result.max_drawdown_usd == Decimal("4.00")
    assert result.max_drawdown_label == "LOWER BOUND for non-overlapping trades"
    assert result.max_drawdown_excursion_bounded_label == "excursion-bounded for non-overlapping trades"
    assert "for non-overlapping trades" in result.max_drawdown_excursion_bounded_measurement_basis
    assert "exit-order" in result.max_drawdown_excursion_bounded_measurement_basis
    assert "not guaranteed" in result.max_drawdown_excursion_bounded_measurement_basis
    assert "synchronized" in result.max_drawdown_excursion_bounded_measurement_basis
    assert "overlap" in result.max_drawdown_excursion_bounded_measurement_basis
    assert (result.net_pnl_usd, result.commission_usd, result.gross_pnl_usd) == (
        Decimal("6.00"), Decimal("3.64"), Decimal("9.64"))
    assert (result.wins, result.losses, result.flats) == (1, 1, 0)
    assert result.profit_factor == Decimal("2.5")
    assert result.win_rate == Decimal("0.5")
    assert dict(result.monthly_net_pnl) == {"2026-01": Decimal("6.00")}


def test_exit_loss_can_exceed_mae():
    result = calculate_accounting(ledger("-1"))
    assert getattr(result, DD, None) == Decimal("4.00")


def test_empty_ledger_has_both_labeled_zero_drawdowns():
    result = calculate_accounting(_trades())
    assert getattr(result, DD, None) == result.max_drawdown_usd == Decimal("0.00")
    assert result.max_drawdown_label == "LOWER BOUND for non-overlapping trades"
    assert result.max_drawdown_excursion_bounded_label == "excursion-bounded for non-overlapping trades"


@pytest.mark.parametrize("mae", [None, "", "garbage", "NaN", "sNaN", "Infinity", "-Infinity", float("nan")])
def test_missing_or_nonfinite_mae_is_rejected(mae):
    with pytest.raises(ValueError, match="mae_usd.*finite"):
        calculate_accounting(ledger(mae))


def test_missing_mae_column_is_explicitly_rejected():
    with pytest.raises(ValueError, match="mae_usd.*finite"):
        calculate_accounting(ledger().drop(columns="mae_usd"))


def test_exit_timestamp_then_source_row_order_is_stable():
    trades = ledger()
    # Same timestamp: row order, not current DataFrame order, chooses the path.
    assert getattr(calculate_accounting(trades.iloc[::-1]), DD, None) == Decimal("9.00")
    trades.loc[0, "exit_source_row"] = 6
    assert getattr(calculate_accounting(trades), DD, None) == Decimal("9.00")
    # Loss first leaves -4 before a later MAE of 9, hence a 13-unit low.
    trades.loc[0, "mae_usd"] = Decimal("9")
    assert getattr(calculate_accounting(trades), DD, None) == Decimal("13.00")
    trades.loc[0, "exit_source_row"] = 4
    assert getattr(calculate_accounting(trades), DD, None) == Decimal("9.00")


@pytest.mark.parametrize("d17", [False, True])
@pytest.mark.parametrize("anchor,status", [("9", "MATCH"), ("4", "MISMATCH"), ("9.01", "MATCH"), ("8.99", "MATCH"), ("9.02", "MISMATCH")])
def test_summary_uses_excursion_not_closed_dd(tmp_path, d17, anchor, status):
    payload = anchor_payload()
    metrics = payload["strategies"][0]["metrics"]
    metrics.pop("max_drawdown_usd", None)
    metrics[DD] = anchor
    if d17:
        payload["d17_policy"] = d17_payload()["d17_policy"]
        metrics.pop("total_commissions_usd")
        metrics.pop("monthly_net_pnl_usd")
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload))
    inventory = load_summary_anchors(path, [_spec()])
    rows, issues = reconcile_summary(calculate_accounting(ledger()), _spec(), inventory)
    row = next(r for r in rows if r["metric"] == DD)
    assert row["observed"] == Decimal("9")
    assert row["status"] == status
    if status == "MISMATCH":
        assert [(i.code, i.severity) for i in issues] == [("TV_SUMMARY_MISMATCH", "BLOCKER")]
        assert "exit-order" in issues[0].detail["measurement_basis"]
        assert "not guaranteed" in issues[0].detail["measurement_basis"]
    else:
        assert not issues


@pytest.mark.parametrize("d17", [False, True])
@pytest.mark.parametrize("mutation", ["retired", "retired_missing", "negative"])
def test_schema_rejects_retired_dd_names_and_negative_new_dd(tmp_path, d17, mutation):
    payload = anchor_payload()
    metrics = payload["strategies"][0]["metrics"]
    metrics.pop("max_drawdown_usd", None)
    metrics[DD] = "9"
    if d17:
        payload["d17_policy"] = d17_payload()["d17_policy"]
        metrics.pop("total_commissions_usd")
        metrics.pop("monthly_net_pnl_usd")
    if mutation == "retired":
        metrics["max_drawdown_usd"] = metrics.pop(DD)
    elif mutation == "retired_missing":
        payload["strategies"][0]["missing_metrics"] = ["max_drawdown_usd"]
    else:
        metrics[DD] = "-1"
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError):
        load_summary_anchors(path, [_spec()])


def test_identical_extrema_do_not_identify_synchronized_equity():
    # Two overlapping trades, both end flat and have MAE 5/MFE 0.
    # Coincident lows give aggregate DD 10; disjoint lows give only 5.
    coincident = [(0, 0), (-5, -5), (0, 0)]
    disjoint = [(0, 0), (-5, 0), (0, -5), (0, 0)]
    assert [min(p[i] for p in coincident) for i in (0, 1)] == [-5, -5]
    assert [min(p[i] for p in disjoint) for i in (0, 1)] == [-5, -5]
    assert -min(sum(p) for p in coincident) == 10
    assert -min(sum(p) for p in disjoint) == 5
    trades = _trades(dict(_trade(1, net="0"), mae_usd=Decimal("-5")),
                     dict(_trade(2, net="0"), mae_usd=Decimal("-5")))
    result = calculate_accounting(trades)
    assert getattr(result, DD, None) == Decimal("5")
    assert "not guaranteed" in result.max_drawdown_excursion_bounded_measurement_basis


def test_real_loader_accounting_summary_runner_serializes_both_bases(tmp_path):
    source_dir, config, _ = _five_source_fixture(tmp_path)
    output = tmp_path / "out"
    result = run_phase1.run_campaign(config, source_dir, output)
    manifest = json.loads(result.manifest_bytes)
    report = result.report_bytes.decode()
    for record in manifest["strategies"]:
        detail = json.loads((output / "strategy_reports" / f"{record['strategy_id']}.json").read_bytes())
        for consumer in (record, detail):
            assert consumer.get(DD) == "1.00"
            assert consumer["max_drawdown_usd"] == "0.00"
            assert consumer["max_drawdown_label"] == "LOWER BOUND for non-overlapping trades"
            assert consumer["max_drawdown_excursion_bounded_label"] == "excursion-bounded for non-overlapping trades"
            assert "for non-overlapping trades" in consumer["max_drawdown_excursion_bounded_measurement_basis"]
            assert "overlap" in consumer["max_drawdown_excursion_bounded_measurement_basis"]
            assert next(r for r in consumer["summary_comparisons"] if r["metric"] == DD)["observed"] == "1.00"
    assert "LOWER BOUND for non-overlapping trades" in report
    assert "excursion-bounded for non-overlapping trades" in report
    assert "DD (LOWER BOUND)" not in report
    assert "exit-order" in report
    assert "not guaranteed" in report
