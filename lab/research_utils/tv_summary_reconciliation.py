"""Independent operator TradingView summaries; never derive anchors from exports."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Mapping, Sequence

from research_utils.trade_reconciliation import AccountingMetrics
from research_utils.tv_trade_ledger import Issue, SourceSpec


METRICS = (
    "trade_count", "net_pnl_usd", "win_rate_pct", "profit_factor",
    "max_drawdown_usd", "total_commissions_usd", "monthly_net_pnl_usd",
)
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


def _decimal(value: object, metric: str) -> Decimal:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{metric} must be a finite decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"{metric} must be a finite decimal string") from exc
    if not result.is_finite():
        raise ValueError(f"{metric} must be finite")
    if metric in {"win_rate_pct", "profit_factor", "max_drawdown_usd", "total_commissions_usd"} and result < 0:
        raise ValueError(f"{metric} must be nonnegative")
    if metric == "win_rate_pct" and result > 100:
        raise ValueError("win_rate_pct must be in [0, 100]")
    return result


def _validate_metrics(metrics: object, missing: object) -> None:
    if not isinstance(metrics, dict) or set(metrics) != set(METRICS):
        raise ValueError("summary metrics keys mismatch")
    if (
        not isinstance(missing, list)
        or any(not isinstance(m, str) or m not in METRICS for m in missing)
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
    if not isinstance(payload, dict) or set(payload) != {"claim_class", "coverage_status", "coverage_note", "strategies"}:
        raise ValueError("summary anchor inventory keys mismatch")
    if payload["claim_class"] != "EXPLORATORY" or payload["coverage_status"] not in ("COMPLETE", "NEEDS_CONTEXT"):
        raise ValueError("summary anchors require EXPLORATORY and valid coverage_status")
    if not isinstance(payload["coverage_note"], str) or not payload["coverage_note"].strip():
        raise ValueError("summary coverage_note must be nonempty")
    if not isinstance(payload["strategies"], list):
        raise ValueError("summary strategies must be an array")
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
        _validate_metrics(anchor["metrics"], anchor["missing_metrics"])
        anchors[strategy_id] = anchor
    complete = set(anchors) == set(active) and not any(a["missing_metrics"] for a in anchors.values())
    if payload["coverage_status"] == "COMPLETE" and not complete:
        raise ValueError("COMPLETE summary coverage requires every active strategy and metric")
    return SummaryInventory(payload["coverage_status"], payload["coverage_note"], anchors, sha256(raw).hexdigest())


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


def reconcile_summary(
    accounting: AccountingMetrics,
    spec: SourceSpec,
    inventory: SummaryInventory,
) -> tuple[list[dict], tuple[Issue, ...]]:
    """Compare each metric without repairing accounting or filling evidence gaps."""
    observed = {
        "trade_count": accounting.trade_count, "net_pnl_usd": accounting.net_pnl_usd,
        "win_rate_pct": accounting.win_rate * 100 if accounting.win_rate is not None else None,
        "profit_factor": accounting.profit_factor, "max_drawdown_usd": accounting.max_drawdown_usd,
        "total_commissions_usd": accounting.commission_usd,
        "monthly_net_pnl_usd": dict(accounting.monthly_net_pnl),
    }
    source = inventory.anchors.get(spec.strategy_id)
    anchors = source["metrics"] if source else {}
    missing = set(source["missing_metrics"]) if source else set(METRICS)
    rows = []
    for metric in METRICS:
        value = anchors.get(metric)
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
                "measurement_basis": (
                    "observed drawdown is closed-trade exit equity; "
                    "TradingView panel equity drawdown may differ"
                ),
            },
        ),
    ) if mismatches else ()
    return rows, issues
