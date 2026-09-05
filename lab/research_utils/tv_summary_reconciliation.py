"""Independent operator TradingView summaries; never derive anchors from exports."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Mapping, Sequence

import pandas as pd

from research_utils.trade_reconciliation import AccountingMetrics
from research_utils.tv_trade_ledger import Issue, SourceSpec


TV_PANEL_DD_METRIC = "tv_panel_max_drawdown_usd"
MAX_DRAWDOWN_POLICY_STATUS = "OVERLAP_KEYED_D32"
METRICS = (
    "trade_count", "net_pnl_usd", "win_rate_pct", "profit_factor",
    TV_PANEL_DD_METRIC, "total_commissions_usd", "monthly_net_pnl_usd",
)
_D17_SCALAR_METRICS = METRICS[:5]
_D17_POLICY_KEYS = {
    "ruling_date", "ruling_ref", "monthly_totals", "commissions", "max_drawdown", "reason",
}
SUMMARY_TOLERANCES = {
    "currency_usd": "0.01",
    "win_rate_percentage_points": "0.01",
    "profit_factor": "0.01",
    "trade_count": "exact",
}


@dataclass(frozen=True)
class SummaryInventory:
    coverage_status: str
    coverage_note: str
    anchors: Mapping[str, dict]
    input_sha256: str | None
    d17_policy: Mapping[str, str | None] | None = None


def _decimal(value: object, metric: str) -> Decimal:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{metric} must be a finite decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{metric} must be a finite decimal string") from exc
    if not result.is_finite():
        raise ValueError(f"{metric} must be finite")
    if metric in {"win_rate_pct", "profit_factor", TV_PANEL_DD_METRIC, "total_commissions_usd"} and result < 0:
        raise ValueError(f"{metric} must be nonnegative")
    if metric == "win_rate_pct" and result > 100:
        raise ValueError("win_rate_pct must be in [0, 100]")
    return result


def _validate_metrics(metrics: object, missing: object, *, d17_policy: bool = False) -> None:
    metric_names = _D17_SCALAR_METRICS if d17_policy else METRICS
    if not isinstance(metrics, dict) or set(metrics) != set(metric_names):
        raise ValueError("summary metrics keys mismatch")
    if (
        not isinstance(missing, list)
        or any(not isinstance(m, str) or m not in metric_names for m in missing)
        or len(set(missing)) != len(missing)
    ):
        raise ValueError("missing_metrics must contain unique known metric names")
    for metric, value in metrics.items():
        if metric in missing:
            if value is not None:
                raise ValueError("missing metric must have null value")
            continue
        if metric == "trade_count":
            if type(value) is not int or value < 0:
                raise ValueError("trade_count must be a nonnegative integer")
        elif metric == "monthly_net_pnl_usd":
            if not isinstance(value, dict):
                raise ValueError("monthly_net_pnl_usd must be a monthly map")
            for month, amount in value.items():
                if not re.fullmatch(r"[0-9]{4}-(0[1-9]|1[0-2])", month) or month.startswith("0000"):
                    raise ValueError("monthly key must be canonical YYYY-MM")
                _decimal(amount, metric)
        elif value is None and metric == "profit_factor":
            continue  # Explicit semantic undefined, unlike a listed missing metric.
        elif value is None and metric == "win_rate_pct" and metrics["trade_count"] == 0:
            continue
        else:
            _decimal(value, metric)


def _validate_d17_policy(value: object) -> dict[str, str | None]:
    if not isinstance(value, dict) or set(value) != _D17_POLICY_KEYS:
        raise ValueError("d17_policy keys mismatch")
    for field in ("ruling_date", "ruling_ref", "reason"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ValueError(f"d17_policy.{field} must be a non-empty string")
    try:
        from datetime import date
        parsed = date.fromisoformat(value["ruling_date"])
    except ValueError as exc:
        raise ValueError("d17_policy.ruling_date must be a canonical ISO date") from exc
    if parsed.isoformat() != value["ruling_date"]:
        raise ValueError("d17_policy.ruling_date must be a canonical ISO date")
    if value["monthly_totals"] != "RECONSTRUCTED":
        raise ValueError("d17_policy.monthly_totals must be RECONSTRUCTED")
    if value["commissions"] != "AMENDED_OUT":
        raise ValueError("d17_policy.commissions must be AMENDED_OUT")
    if value["max_drawdown"] != "OVERLAP_KEYED":
        raise ValueError("d17_policy.max_drawdown must be OVERLAP_KEYED")
    return dict(value)


def load_summary_anchors(path: str | Path, specs: Sequence[SourceSpec]) -> SummaryInventory:
    """Validate independent evidence and bind it to active export hashes."""
    try:
        raw = Path(path).read_bytes()
    except FileNotFoundError:
        return SummaryInventory("NEEDS_CONTEXT", "Operator TradingView summaries have not been supplied; G1.4 is partial.", {}, None)
    except OSError as exc:
        raise ValueError("cannot read TradingView summary anchors") from exc
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("cannot load TradingView summary anchors JSON") from exc
    if not isinstance(payload, dict) or set(payload) not in (
        {"claim_class", "coverage_status", "coverage_note", "strategies"},
        {"claim_class", "coverage_status", "coverage_note", "d17_policy", "strategies"},
    ):
        raise ValueError("summary anchor inventory keys mismatch")
    if payload["claim_class"] != "EXPLORATORY" or payload["coverage_status"] not in ("COMPLETE", "NEEDS_CONTEXT"):
        raise ValueError("summary anchors require EXPLORATORY and valid coverage_status")
    if not isinstance(payload["coverage_note"], str) or not payload["coverage_note"].strip():
        raise ValueError("summary coverage_note must be nonempty")
    if not isinstance(payload["strategies"], list):
        raise ValueError("summary strategies must be an array")
    d17_policy = (
        _validate_d17_policy(payload["d17_policy"])
        if "d17_policy" in payload
        else None
    )
    active = {spec.strategy_id: spec.export_sha256 for spec in specs}
    anchors = {}
    for anchor in payload["strategies"]:
        if not isinstance(anchor, dict) or set(anchor) != {"strategy_id", "export_sha256", "source_note", "metrics", "missing_metrics"}:
            raise ValueError("strategy summary anchor keys mismatch")
        strategy_id = anchor["strategy_id"]
        if not isinstance(strategy_id, str) or strategy_id not in active or strategy_id in anchors:
            raise ValueError("summary strategy must be unique and active (not dropped)")
        if anchor["export_sha256"] != active[strategy_id]:
            raise ValueError("summary export_sha256 does not match active export")
        if not isinstance(anchor["source_note"], str) or not anchor["source_note"].strip():
            raise ValueError("summary source_note must be nonempty operator provenance")
        _validate_metrics(
            anchor["metrics"], anchor["missing_metrics"], d17_policy=d17_policy is not None,
        )
        anchors[strategy_id] = anchor
    complete = set(anchors) == set(active) and not any(a["missing_metrics"] for a in anchors.values())
    if payload["coverage_status"] == "COMPLETE" and not complete:
        raise ValueError("COMPLETE summary coverage requires every active strategy and metric")
    return SummaryInventory(
        payload["coverage_status"], payload["coverage_note"], anchors,
        sha256(raw).hexdigest(), d17_policy,
    )


def _comparison(
    metric: str,
    observed: object,
    anchor: object,
    *,
    missing: bool = False,
    missing_side: bool = False,
) -> dict:
    tolerance = Decimal("0") if metric == "trade_count" else Decimal("0.01")
    difference = None
    if observed is not None and anchor is not None:
        difference = Decimal(observed) - Decimal(anchor)
    matches = not missing_side and (
        (observed is None and anchor is None)
        or (difference is not None and abs(difference) <= tolerance)
    )
    return {
        "metric": metric,
        "observed": observed,
        "anchor": anchor,
        "difference": difference,
        "tolerance": tolerance,
        "status": "MISSING_ANCHOR" if missing else "MATCH" if matches else "MISMATCH",
    }


def _money_string(value: Decimal) -> str:
    return format(value.quantize(Decimal("0.01")), "f")


def reconstruct_d17_monthly(
    *, accounting: AccountingMetrics, trades: object, spec: SourceSpec,
) -> tuple[dict[str, object], tuple[Issue, ...]]:
    """Reconstruct D17's local-only exit-month ledger from canonical trade rows."""
    if not isinstance(trades, pd.DataFrame):
        raise ValueError("D17 monthly reconstruction requires canonical trades")
    if not isinstance(spec.source_timezone, str) or not spec.source_timezone.strip():
        raise ValueError("D17 monthly reconstruction requires an explicit source timezone")
    monthly: dict[str, Decimal] = {}
    month_spanning_trade_count = 0
    for _, trade in trades.iterrows():
        entry = pd.Timestamp(trade["entry_timestamp_naive"])
        exit_ = pd.Timestamp(trade["exit_timestamp_naive"])
        if entry.strftime("%Y-%m") != exit_.strftime("%Y-%m"):
            month_spanning_trade_count += 1
        month = exit_.strftime("%Y-%m")
        monthly[month] = monthly.get(month, Decimal("0")) + Decimal(trade["net_pnl_usd"])
    monthly = {month: value.quantize(Decimal("0.01")) for month, value in sorted(monthly.items())}
    accounting_monthly = {
        month: Decimal(value).quantize(Decimal("0.01"))
        for month, value in accounting.monthly_net_pnl.items()
    }
    monthly_residual = sum(
        (
            (
                monthly.get(month, Decimal("0"))
                - accounting_monthly.get(month, Decimal("0"))
            ).copy_abs()
            for month in set(monthly) | set(accounting_monthly)
        ),
        Decimal("0"),
    )
    reconstructed_total = sum(monthly.values(), Decimal("0")).quantize(Decimal("0.01"))
    aggregate_residual = reconstructed_total - accounting.net_pnl_usd
    source_residual = (
        None
        if accounting.final_source_cumulative_pnl_usd is None
        else reconstructed_total - accounting.final_source_cumulative_pnl_usd
    )
    tolerance = Decimal("0.01")
    mismatch = (
        monthly_residual > tolerance
        or aggregate_residual.copy_abs() > tolerance
        or (source_residual is not None and source_residual.copy_abs() > tolerance)
    )
    payload = {
        "schema": "tradeify_d17_monthly_reconciliation/v1",
        "strategy_id": spec.strategy_id,
        "export_sha256": spec.export_sha256,
        "month_basis": f"exit_timestamp_naive in {spec.source_timezone}",
        "bucket_count": len(monthly),
        "monthly_net_pnl_usd": {month: _money_string(amount) for month, amount in monthly.items()},
        "comparison_status": "MISMATCH" if mismatch else "RECONSTRUCTED",
        "accounting_monthly_residual_usd": _money_string(monthly_residual),
        "aggregate_residual_usd": _money_string(aggregate_residual),
        "source_cumulative_residual_usd": (
            None if source_residual is None else _money_string(source_residual)
        ),
        "tolerance_usd": "0.01",
        "month_spanning_trade_count": month_spanning_trade_count,
    }
    issues = () if not mismatch else (
        Issue(
            code="D17_MONTHLY_RECONSTRUCTION_MISMATCH",
            severity="BLOCKER",
            strategy_id=spec.strategy_id,
            detail={
                "month_basis": payload["month_basis"],
                "accounting_monthly_residual_usd": payload["accounting_monthly_residual_usd"],
                "aggregate_residual_usd": payload["aggregate_residual_usd"],
                "source_cumulative_residual_usd": payload["source_cumulative_residual_usd"],
                "tolerance_usd": payload["tolerance_usd"],
            },
        ),
    )
    return payload, issues


def _drawdown_comparison(
    accounting: AccountingMetrics, panel: object, *, missing: bool,
) -> dict:
    """Record the panel separately; only a measured non-overlap lower bound is tested."""
    walk = accounting.max_drawdown_excursion_bounded_usd
    difference = None if missing else walk - Decimal(panel)
    if missing:
        status = "MISSING_ANCHOR"
    elif accounting.has_overlap_or_tie:
        status = "RECORDED"
    elif difference > Decimal("0.01"):
        status = "MISMATCH"
    elif difference == 0:
        status = "COINCIDENT"
    else:
        status = "WITHIN_BOUND"
    return {
        "metric": TV_PANEL_DD_METRIC,
        "observed": None,  # The computed walk is not an observation of the panel quantity.
        "anchor": panel,
        "walk_usd": walk,
        "difference": difference,
        "tolerance": Decimal("0.01"),
        "status": status,
        "has_overlap_or_tie": accounting.has_overlap_or_tie,
        "measurement_basis": accounting.max_drawdown_excursion_bounded_measurement_basis,
        "difference_basis": "walk minus separate TradingView panel anchor",
        "max_drawdown_policy_status": MAX_DRAWDOWN_POLICY_STATUS,
    }


def reconcile_summary(
    accounting: AccountingMetrics,
    spec: SourceSpec,
    inventory: SummaryInventory,
) -> tuple[list[dict], tuple[Issue, ...]]:
    """Compare each metric without repairing accounting or filling evidence gaps."""
    observed = {
        "trade_count": accounting.trade_count, "net_pnl_usd": accounting.net_pnl_usd,
        "win_rate_pct": accounting.win_rate * 100 if accounting.win_rate is not None else None,
        "profit_factor": accounting.profit_factor,
        "total_commissions_usd": accounting.commission_usd,
        "monthly_net_pnl_usd": dict(accounting.monthly_net_pnl),
    }
    source = inventory.anchors.get(spec.strategy_id)
    anchors = source["metrics"] if source else {}
    metric_names = _D17_SCALAR_METRICS if inventory.d17_policy is not None else METRICS
    missing = set(source["missing_metrics"]) if source else set(metric_names)
    rows = []
    for metric in metric_names:
        value = anchors.get(metric)
        if metric == TV_PANEL_DD_METRIC:
            rows.append(_drawdown_comparison(accounting, value, missing=metric in missing))
            continue
        if metric != "monthly_net_pnl_usd":
            rows.append(_comparison(metric, observed[metric], value, missing=metric in missing))
            continue
        monthly = value or {}
        details = [
            _comparison(
                f"{metric}.{month}", observed[metric].get(month), monthly.get(month),
                missing=metric in missing,
                missing_side=month not in monthly or month not in observed[metric],
            )
            for month in sorted(set(observed[metric]) | set(monthly))
        ]
        if metric in missing:
            status = "MISSING_ANCHOR"
        else:
            status = "MISMATCH" if any(r["status"] == "MISMATCH" for r in details) else "MATCH"
        rows.append({"metric": metric, "observed": observed[metric], "anchor": value,
                     "difference": None, "tolerance": Decimal("0.01"), "status": status})
        rows.extend(details)
    mismatches = [row["metric"] for row in rows if row["status"] == "MISMATCH"]
    issues = (
        Issue(
            code="TV_SUMMARY_MISMATCH",
            severity="BLOCKER",
            strategy_id=spec.strategy_id,
            detail={
                "metrics": mismatches,
                "measurement_basis": accounting.max_drawdown_excursion_bounded_measurement_basis,
            },
        ),
    ) if mismatches else ()
    for row in rows:
        if row["metric"] == TV_PANEL_DD_METRIC and row["status"] in {"COINCIDENT", "RECORDED"}:
            issues += (Issue(
                code="TV_DRAWDOWN_COINCIDENT" if row["status"] == "COINCIDENT" else "TV_DRAWDOWN_RECORDED",
                severity="INFO", strategy_id=spec.strategy_id,
                detail={
                    **row,
                    "comparison": "coincident" if row["difference"] == 0 else "differs",
                },
            ),)
    return rows, issues
