"""Independent literals catch accounting/summary comparison errors."""
from decimal import Decimal
from hashlib import sha256
import json

import pytest

from research_utils.trade_reconciliation import calculate_accounting
from research_utils import tv_summary_reconciliation
from test_trade_reconciliation import _spec, _trades, _trade


@pytest.fixture
def api():
    return tv_summary_reconciliation


def anchor_payload():
    return {"claim_class": "EXPLORATORY", "coverage_status": "COMPLETE",
            "coverage_note": "Literal synthetic independent summary", "strategies": [{
                "strategy_id": "fixture", "export_sha256": "0" * 64,
                "source_note": "Synthetic operator panel", "missing_metrics": [],
                "metrics": {"trade_count": 2, "net_pnl_usd": "6.00", "win_rate_pct": "50.00",
                            "profit_factor": "2.50", "max_drawdown_usd": "4.00",
                            "total_commissions_usd": "3.64", "monthly_net_pnl_usd": {"2026-01": "6.00"}},
            }]}


def accounting():
    return calculate_accounting(_trades(
        _trade(1, "2026-01-05 10:00", "10.00", "1.82", cumulative="10.00"),
        _trade(2, "2026-01-06 10:00", "-4.00", "1.82", cumulative="6.00")))


def load(api, tmp_path, payload):
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return api.load_summary_anchors(path, [_spec()]), path


def d17_payload():
    """The operator policy deliberately retires stale panel values, not scalar requirements."""
    return {
        "claim_class": "EXPLORATORY",
        "coverage_status": "NEEDS_CONTEXT",
        "coverage_note": "Replacement-source Key-stats panels are still required.",
        "d17_policy": {
            "ruling_date": "2026-09-03",
            "ruling_ref": "campaign-state §6 D17",
            "monthly_totals": "RECONSTRUCTED",
            "commissions": "AMENDED_OUT",
            "reason": "Monthly values come from the canonical row ledger; no independent commission total exists.",
        },
        "strategies": [],
    }


def test_d17_policy_keeps_five_scalar_requirements_without_silent_waiver(api, tmp_path):
    """Removing D17's policy must not turn absent replacement panels into acceptable evidence."""
    inventory, _ = load(api, tmp_path, d17_payload())

    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)

    assert inventory.d17_policy["monthly_totals"] == "RECONSTRUCTED"
    assert inventory.d17_policy["commissions"] == "AMENDED_OUT"
    assert [row["metric"] for row in rows] == [
        "trade_count", "net_pnl_usd", "win_rate_pct", "profit_factor", "max_drawdown_usd",
    ]
    assert all(row["status"] == "MISSING_ANCHOR" for row in rows)
    assert not issues


@pytest.mark.parametrize("mutation", ["missing", "extra", "bad_monthly", "bad_commissions", "monthly_metric", "commission_metric", "retired_missing"])
def test_d17_policy_rejects_noncanonical_or_independent_retired_dimensions(api, tmp_path, mutation):
    """A permissive D17 schema could falsely compare an unanchored commission or monthly total."""
    payload = d17_payload()
    if mutation == "missing":
        payload["d17_policy"].pop("reason")
    elif mutation == "extra":
        payload["d17_policy"]["extra"] = True
    elif mutation == "bad_monthly":
        payload["d17_policy"]["monthly_totals"] = "MISSING_ANCHOR"
    elif mutation == "bad_commissions":
        payload["d17_policy"]["commissions"] = "RECONCILED"
    else:
        payload["strategies"] = [{
            "strategy_id": "fixture", "export_sha256": "0" * 64,
            "source_note": "A future independent panel", "missing_metrics": [],
            "metrics": {
                "trade_count": 2, "net_pnl_usd": "6.00", "win_rate_pct": "50.00",
                "profit_factor": "2.50", "max_drawdown_usd": "4.00",
            },
        }]
        if mutation == "retired_missing":
            payload["strategies"][0]["missing_metrics"] = ["total_commissions_usd"]
        else:
            retired = "monthly_net_pnl_usd" if mutation == "monthly_metric" else "total_commissions_usd"
            payload["strategies"][0]["metrics"][retired] = {} if retired.startswith("monthly") else "3.64"
    with pytest.raises(ValueError):
        load(api, tmp_path, payload)


def test_d17_rejects_a_stale_export_pin_before_accepting_scalar_anchors(api, tmp_path):
    """A stale old-source panel must not become independent evidence for a replacement body."""
    payload = d17_payload()
    payload["strategies"] = [{
        "strategy_id": "fixture", "export_sha256": "f" * 64,
        "source_note": "Stale panel", "missing_metrics": [],
        "metrics": {
            "trade_count": 2, "net_pnl_usd": "6.00", "win_rate_pct": "50.00",
            "profit_factor": "2.50", "max_drawdown_usd": "4.00",
        },
    }]

    with pytest.raises(ValueError, match="export_sha256"):
        load(api, tmp_path, payload)


def test_d17_monthly_reconstruction_uses_exit_month_and_retains_cross_month_trade(api):
    """Bucketing by entry month would misstate a trade held across a calendar boundary."""
    trades = _trades(
        _trade(1, "2026-02-01 00:05", "2.005", cumulative="2.005"),
        _trade(2, "2026-02-02 10:00", "-1.005", cumulative="1.000"),
    )
    trades.loc[0, "entry_timestamp_naive"] = trades.loc[0, "entry_timestamp_naive"].replace(month=1)

    payload, issues = api.reconstruct_d17_monthly(accounting=calculate_accounting(trades), trades=trades, spec=_spec())

    assert payload["monthly_net_pnl_usd"] == {"2026-02": "1.00"}
    assert payload["month_basis"] == "exit_timestamp_naive in America/New_York"
    assert payload["month_spanning_trade_count"] == 1
    assert payload["comparison_status"] == "RECONSTRUCTED"
    assert payload["aggregate_residual_usd"] == "0.00"
    assert not issues


def test_d17_monthly_reconstruction_flags_real_ledger_accounting_disagreement(api):
    """A changed canonical trade amount must block instead of comparing a value to itself."""
    trades = _trades(_trade(1, "2026-01-05 10:00", "2.00", cumulative="2.00"))
    accounting_snapshot = calculate_accounting(trades)
    trades.loc[0, "net_pnl_usd"] = Decimal("3.00")

    payload, issues = api.reconstruct_d17_monthly(accounting=accounting_snapshot, trades=trades, spec=_spec())

    assert payload["comparison_status"] == "MISMATCH"
    assert payload["accounting_monthly_residual_usd"] == "1.00"
    assert [(issue.code, issue.severity) for issue in issues] == [
        ("D17_MONTHLY_RECONSTRUCTION_MISMATCH", "BLOCKER"),
    ]


def test_d17_monthly_reconstruction_accepts_zero_trades(api):
    """A zero-trade export is an empty month series, not a missing monthly anchor."""
    payload, issues = api.reconstruct_d17_monthly(
        accounting=calculate_accounting(_trades()), trades=_trades(), spec=_spec(),
    )

    assert payload["monthly_net_pnl_usd"] == {}
    assert payload["bucket_count"] == 0
    assert payload["comparison_status"] == "RECONSTRUCTED"
    assert not issues


def test_independent_summary_matches_and_hashes_parsed_bytes(api, tmp_path):
    inventory, path = load(api, tmp_path, anchor_payload())
    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)
    assert inventory.input_sha256 == sha256(path.read_bytes()).hexdigest()
    assert inventory.coverage_status == "COMPLETE"
    assert len(rows) == 8
    assert all(row["status"] == "MATCH" for row in rows)
    assert next(row for row in rows if row["metric"] == "win_rate_pct")["observed"] == Decimal("50")
    assert not issues


@pytest.mark.parametrize("metric,value", [
    ("trade_count", 3), ("net_pnl_usd", "6.02"), ("win_rate_pct", "50.02"),
    ("profit_factor", "2.52"), ("max_drawdown_usd", "4.02"),
    ("total_commissions_usd", "3.66"), ("monthly_net_pnl_usd", {"2026-01": "6.02"}),
])
def test_each_independent_metric_mismatch_blocks(api, tmp_path, metric, value):
    p = anchor_payload()
    p["strategies"][0]["metrics"][metric] = value
    inventory, _ = load(api, tmp_path, p)
    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)
    assert any(r["metric"] == metric and r["status"] == "MISMATCH" for r in rows)
    assert [(i.code, i.severity) for i in issues] == [("TV_SUMMARY_MISMATCH", "BLOCKER")]


@pytest.mark.parametrize("metric,base", [("net_pnl_usd", "6"), ("win_rate_pct", "50"),
    ("profit_factor", "2.5"), ("max_drawdown_usd", "4"), ("total_commissions_usd", "3.64"),
    ("monthly_net_pnl_usd", "6")])
@pytest.mark.parametrize("delta,status", [("0.01", "MATCH"), ("-0.01", "MATCH"), ("0.010001", "MISMATCH"), ("-0.010001", "MISMATCH")])
def test_absolute_tolerances_are_inclusive(api, tmp_path, metric, base, delta, status):
    p = anchor_payload()
    value = str(Decimal(base) + Decimal(delta))
    p["strategies"][0]["metrics"][metric] = {"2026-01": value} if metric == "monthly_net_pnl_usd" else value
    inventory, _ = load(api, tmp_path, p)
    rows, _ = api.reconcile_summary(accounting(), _spec(), inventory)
    assert next(r for r in rows if r["metric"] == metric)["status"] == status


def test_month_union_does_not_zero_fill_missing_sides(api, tmp_path):
    p = anchor_payload()
    p["strategies"][0]["metrics"]["monthly_net_pnl_usd"] = {"2026-02": "0.00"}
    inventory, _ = load(api, tmp_path, p)
    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)
    monthly = {r["metric"]: r for r in rows if r["metric"].startswith("monthly_net_pnl_usd.")}
    assert monthly["monthly_net_pnl_usd.2026-01"]["anchor"] is None
    assert monthly["monthly_net_pnl_usd.2026-02"]["observed"] is None
    assert all(r["status"] == "MISMATCH" for r in monthly.values())
    assert issues[0].code == "TV_SUMMARY_MISMATCH"


def test_partial_metrics_are_missing_not_undefined_or_match(api, tmp_path):
    p = anchor_payload()
    p["coverage_status"] = "NEEDS_CONTEXT"
    p["strategies"][0]["missing_metrics"] = ["total_commissions_usd", "monthly_net_pnl_usd"]
    p["strategies"][0]["metrics"].update(total_commissions_usd=None, monthly_net_pnl_usd=None)
    inventory, _ = load(api, tmp_path, p)
    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)
    assert inventory.coverage_status == "NEEDS_CONTEXT"
    assert {r["metric"] for r in rows if r["status"] == "MISSING_ANCHOR"} >= {"total_commissions_usd", "monthly_net_pnl_usd"}
    assert not issues


@pytest.mark.parametrize("file_exists", [True, False])
def test_missing_evidence_never_self_certifies(api, tmp_path, file_exists):
    p = anchor_payload()
    p.update(coverage_status="NEEDS_CONTEXT", strategies=[])
    if file_exists:
        inventory, _ = load(api, tmp_path, p)
    else:
        inventory = api.load_summary_anchors(tmp_path / "absent.json", [_spec()])
    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)
    assert inventory.coverage_status == "NEEDS_CONTEXT"
    assert len(rows) >= 7
    assert all(r["status"] == "MISSING_ANCHOR" for r in rows)
    assert not issues


@pytest.mark.parametrize("mutation", ["hash", "unknown", "dropped", "duplicate", "float", "bool", "nan",
    "extra", "metric_extra", "missing_extra", "missing_nonnull", "missing_duplicate", "negative_dd",
    "bad_month", "month_float", "empty_note", "null_rate", "rate_range", "bool_count", "empty_complete", "partial_complete"])
def test_invalid_anchor_inventory_is_rejected(api, tmp_path, mutation):
    p = anchor_payload(); a = p["strategies"][0]; m = a["metrics"]
    if mutation == "hash": a["export_sha256"] = "1" * 64
    elif mutation == "unknown": a["strategy_id"] = "unknown"
    elif mutation == "dropped": a["strategy_id"] = "striker_dj30_qtxg1_swap_body_on_mym"
    elif mutation == "duplicate": p["strategies"].append(dict(a))
    elif mutation == "float": m["net_pnl_usd"] = 6.0
    elif mutation == "bool": m["profit_factor"] = True
    elif mutation == "nan": m["net_pnl_usd"] = "NaN"
    elif mutation == "extra": a["extra"] = 1
    elif mutation == "metric_extra": m["extra"] = 1
    elif mutation == "missing_extra": a["missing_metrics"] = ["extra"]
    elif mutation == "missing_nonnull": a["missing_metrics"] = ["net_pnl_usd"]
    elif mutation == "missing_duplicate": a["missing_metrics"] = ["profit_factor", "profit_factor"]; m["profit_factor"] = None
    elif mutation == "negative_dd": m["max_drawdown_usd"] = "-1"
    elif mutation == "bad_month": m["monthly_net_pnl_usd"] = {"2026-13": "1"}
    elif mutation == "month_float": m["monthly_net_pnl_usd"] = {"2026-01": 1.0}
    elif mutation == "empty_note": a["source_note"] = " "
    elif mutation == "null_rate": m["win_rate_pct"] = None
    elif mutation == "rate_range": m["win_rate_pct"] = "100.1"
    elif mutation == "bool_count": m["trade_count"] = True
    elif mutation == "empty_complete": p["strategies"] = []
    elif mutation == "partial_complete": a["missing_metrics"] = ["profit_factor"]; m["profit_factor"] = None
    with pytest.raises(ValueError): load(api, tmp_path, p)


def test_semantically_undefined_nulls_only_match_each_other(api, tmp_path):
    p = anchor_payload(); m = p["strategies"][0]["metrics"]
    m.update(trade_count=0, net_pnl_usd="0", win_rate_pct=None, profit_factor=None,
             max_drawdown_usd="0", total_commissions_usd="0", monthly_net_pnl_usd={})
    inventory, _ = load(api, tmp_path, p)
    rows, issues = api.reconcile_summary(calculate_accounting(_trades()), _spec(), inventory)
    assert all(r["status"] == "MATCH" for r in rows)
    assert not issues
    rows, issues = api.reconcile_summary(accounting(), _spec(), inventory)
    assert next(r for r in rows if r["metric"] == "profit_factor")["status"] == "MISMATCH"


def test_invalid_status_type_is_configuration_error(api, tmp_path):
    p = anchor_payload()
    p["coverage_status"] = []
    with pytest.raises(ValueError): load(api, tmp_path, p)


def test_checked_in_operator_anchors_reject_stale_panels_under_d17(api):
    from pathlib import Path
    from test_trade_reconciliation import _spec
    campaign = Path(__file__).parents[1] / "lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09"
    # Runtime validation uses a synthetic source, never upgrades historical config.
    specs = [_spec()]
    inventory = api.load_summary_anchors(campaign / "tv_summary_anchors.json", specs)
    assert inventory.coverage_status == "NEEDS_CONTEXT"
    assert inventory.anchors == {}
    assert inventory.d17_policy["monthly_totals"] == "RECONSTRUCTED"
    assert inventory.d17_policy["commissions"] == "AMENDED_OUT"
    assert "all five replacement sources" in inventory.coverage_note
    assert "+$287" in inventory.coverage_note
