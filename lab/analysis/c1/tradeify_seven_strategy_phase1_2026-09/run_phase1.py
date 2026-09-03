"""Run strict, exploratory Phase 1 normalization for five retained exports."""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Mapping
from dataclasses import asdict
import csv
from datetime import date, datetime
from decimal import Decimal
from hashlib import sha256
from io import StringIO
import json
import os
from pathlib import Path
import sys
from typing import NamedTuple, Sequence
from uuid import uuid4

import pandas as pd


_REPO = Path(__file__).resolve().parents[4]
_CAMPAIGN_DIR = Path(__file__).resolve().parent
_LAB = _REPO / "lab"
_CORE = _REPO / "core"
for _import_root in (_REPO, _LAB, _CORE):
    if str(_import_root) not in sys.path:
        sys.path.insert(0, str(_import_root))

from research_utils.joint_trade_blocks import (  # noqa: E402
    build_joint_events,
    build_weekly_exit_blocks,
)
from research_utils.trade_reconciliation import (  # noqa: E402
    analyze_venue,
    calculate_accounting,
    load_early_close_calendar,
    reconstruct_trades,
)
from research_utils.tv_trade_ledger import (  # noqa: E402
    SourceIdentityError,
    TradeExportSchemaError,
    load_fee_schedule,
    load_source_inventory,
    load_source_specs,
    normalize_export,
    verify_source_pair,
)
from research_utils.tv_summary_reconciliation import (  # noqa: E402
    SUMMARY_TOLERANCES,
    load_summary_anchors,
    reconcile_summary,
)


_RUNNER_VERSION = "tradeify-phase1-normalization-v2"
_SEVERITY_ORDER = {"INFO": 0, "WARNING": 1, "BLOCKER": 2, "FATAL": 3}
_BASE_COMMIT = "ed181233afd01d8fc128bc76ac626e43c3761f87"
_FROZEN_STRATEGY_IDS = (
    "aegis_6j1",
    "orb_mnq_recon_v7",
    "striker_dj30_mym_pyramid_250",
    "striker_nas100_mnq_dow_wed_excluded",
    "vanguard_mgc_v04",
)
_FROZEN_DROPPED_SOURCE_IDS = (
    "striker_dj30_qtxg1_swap_body_on_mym",
    "striker_nas100_qtxg1_swap_body_on_mnq",
)


class CampaignResult(NamedTuple):
    status: str
    manifest_path: Path
    report_path: Path
    manifest_bytes: bytes
    report_bytes: bytes


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        with temporary.open("wb") as handle:
            handle.write(payload)
            handle.flush()
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _publish_payloads(payloads: dict[Path, bytes]) -> None:
    """Publish a complete campaign generation, restoring old bytes on replace failure."""
    token = uuid4().hex
    staged = {
        target: target.with_name(f".{target.name}.phase1-{token}.stage")
        for target in payloads
    }
    backups = {
        target: target.with_name(f".{target.name}.phase1-{token}.backup")
        for target in payloads
    }
    backed_up: set[Path] = set()
    published: set[Path] = set()
    publication_error: OSError | None = None
    recovery_failures: list[str] = []
    preserved_backups: list[Path] = []
    try:
        for target, payload in payloads.items():
            _atomic_write_bytes(staged[target], payload)
        for target in payloads:
            if target.exists():
                os.replace(target, backups[target])
                backed_up.add(target)
        for target in payloads:
            os.replace(staged[target], target)
            published.add(target)
    except OSError as exc:
        publication_error = exc
        for target in payloads:
            try:
                if target in backed_up:
                    # Replacement restores old bytes directly, even if new bytes exist.
                    os.replace(backups[target], target)
                elif target in published:
                    target.unlink(missing_ok=True)
            except OSError as recovery_error:
                recovery_failures.append(f"{target}: {recovery_error}")
                if target in backed_up:
                    preserved_backups.append(backups[target])
    finally:
        # A failed restoration leaves the backup as the only recoverable old copy.
        disposable = (*staged.values(), *(backups.values() if publication_error is None else ()))
        for temporary in disposable:
            try:
                temporary.unlink(missing_ok=True)
            except OSError as cleanup_error:
                recovery_failures.append(f"cleanup {temporary}: {cleanup_error}")
    if publication_error is not None:
        if recovery_failures:
            raise OSError(
                f"publication failed: {publication_error}; recovery incomplete: "
                f"{'; '.join(recovery_failures)}; preserved recovery backups: "
                f"{', '.join(map(str, preserved_backups)) or 'none'}"
            ) from publication_error
        raise publication_error
    if recovery_failures:
        raise OSError(f"publication completed but cleanup failed: {'; '.join(recovery_failures)}")


def _csv_bytes(frame: pd.DataFrame) -> bytes:
    stream = StringIO(newline="")
    frame.to_csv(
        stream,
        index=False,
        lineterminator="\n",
        na_rep="",
        quoting=csv.QUOTE_MINIMAL,
    )
    return stream.getvalue().encode("utf-8")


def _json_default(value: object) -> object:
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, tuple):
        return list(value)
    raise TypeError(f"cannot serialize {type(value).__name__}")


def _json_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            default=_json_default,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def _plain_evidence(value: object) -> object:
    """Copy immutable calendar provenance into the published JSON domain."""
    if isinstance(value, Mapping):
        return {str(key): _plain_evidence(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain_evidence(item) for item in value]
    return value


def _digest(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _validate_strategy_roster(specs: Sequence[object]) -> None:
    observed = tuple(spec.strategy_id for spec in specs)
    if observed != _FROZEN_STRATEGY_IDS:
        raise ValueError(
            "frozen strategy roster mismatch: "
            f"expected={list(_FROZEN_STRATEGY_IDS)!r}, observed={list(observed)!r}"
        )


def _validate_dropped_source_roster(dropped_sources: Sequence[object]) -> None:
    observed = tuple(source.strategy_id_as_named_before for source in dropped_sources)
    if observed != _FROZEN_DROPPED_SOURCE_IDS:
        raise ValueError(
            "frozen dropped source roster mismatch: "
            f"expected={list(_FROZEN_DROPPED_SOURCE_IDS)!r}, observed={list(observed)!r}"
        )


def _validate_output_dir(output_dir: Path) -> None:
    try:
        output_dir.relative_to(_REPO)
    except ValueError:
        return
    allowed_root = (_CAMPAIGN_DIR / "local_artifacts").resolve()
    if output_dir != allowed_root and not output_dir.is_relative_to(allowed_root):
        raise ValueError(
            "output directory inside the repository must be campaign-local "
            f"local_artifacts: {allowed_root}"
        )


def _validate_calendar_coverage(
    events_by_strategy: dict[str, pd.DataFrame],
    early_close_calendar: object,
) -> None:
    if early_close_calendar.coverage_status != "COMPLETE":
        return
    timestamps = pd.concat(
        [frame["timestamp_naive"] for frame in events_by_strategy.values()],
        ignore_index=True,
    )
    if timestamps.empty:
        return
    observed_start = pd.Timestamp(timestamps.min()).date()
    observed_end = pd.Timestamp(timestamps.max()).date()
    if (
        observed_start < early_close_calendar.coverage_start
        or observed_end > early_close_calendar.coverage_end
    ):
        raise ValueError(
            "COMPLETE CME early-close calendar does not cover observed source span: "
            f"calendar={early_close_calendar.coverage_start.isoformat()}.."
            f"{early_close_calendar.coverage_end.isoformat()}, "
            f"observed={observed_start.isoformat()}..{observed_end.isoformat()}"
        )


def _detailed_issue_rows(issues: Sequence[object]) -> list[dict[str, object]]:
    ordered = sorted(
        issues,
        key=lambda issue: (
            -_SEVERITY_ORDER[issue.severity],
            issue.code,
            -1 if issue.trade_id is None else issue.trade_id,
            issue.source_rows,
        ),
    )
    return [
        {
            "code": issue.code,
            "severity": issue.severity,
            "trade_id": issue.trade_id,
            "source_rows": issue.source_rows,
            "detail": dict(issue.detail),
        }
        for issue in ordered
    ]


def _issue_summary(issues: Sequence[object]) -> tuple[dict[str, int], list[dict[str, object]]]:
    counts = Counter(issue.code for issue in issues)
    grouped = Counter((issue.severity, issue.code) for issue in issues)
    rows = [
        {"severity": severity, "code": code, "count": count}
        for (severity, code), count in sorted(
            grouped.items(),
            key=lambda item: (
                -_SEVERITY_ORDER[item[0][0]],
                item[0][1],
            ),
        )
    ]
    return dict(sorted(counts.items())), rows


def _strategy_record(
    spec: object,
    events: pd.DataFrame,
    trades: pd.DataFrame,
    accounting: object,
    venue: object,
    issues: Sequence[object],
) -> dict[str, object]:
    blocker = any(issue.severity in {"BLOCKER", "FATAL"} for issue in issues)
    issue_counts, issue_summary = _issue_summary(issues)
    return {
        "strategy_id": spec.strategy_id,
        "status": "BLOCKED_EXPLORATORY" if blocker else "RECONCILED_EXPLORATORY",
        "claim_class": "EXPLORATORY",
        "intended_instrument": spec.intended_instrument,
        "encoded_instrument": spec.encoded_instrument,
        "source_row_count": len(events),
        "trade_count": accounting.trade_count,
        "first_entry_timestamp": accounting.first_entry_timestamp,
        "last_exit_timestamp": accounting.last_exit_timestamp,
        "net_pnl_usd": accounting.net_pnl_usd,
        "commission_usd": accounting.commission_usd,
        "gross_pnl_usd": accounting.gross_pnl_usd,
        "wins": accounting.wins,
        "losses": accounting.losses,
        "flats": accounting.flats,
        "win_rate": accounting.win_rate,
        "profit_factor": accounting.profit_factor,
        "max_drawdown_usd": accounting.max_drawdown_usd,
        "monthly_net_pnl": dict(accounting.monthly_net_pnl),
        "final_source_cumulative_pnl_usd": accounting.final_source_cumulative_pnl_usd,
        "pine_pyramiding_pct": spec.pine_pyramiding_pct,
        "pine_pin_status": spec.pine_pin_status,
        "pin_ref": spec.pin_ref,
        "pin_divergence": spec.pin_divergence,
        "export_bytes": spec.export_bytes,
        "pine_bytes": spec.pine_bytes,
        "micro_equivalent_multiplier": venue.micro_equivalent_multiplier,
        "peak_open_micro_equivalent_quantity_min": (
            venue.peak_open_micro_equivalent_quantity_min
        ),
        "peak_open_micro_equivalent_quantity_max": (
            venue.peak_open_micro_equivalent_quantity_max
        ),
        "micro_equivalent_contract_cap": venue.micro_equivalent_contract_cap,
        "cross_date_holds": venue.cross_date_holds,
        "overnight_holds": venue.overnight_holds,
        "friday_to_sunday_holds": venue.friday_to_sunday_holds,
        "holiday_short_deadline_status": venue.holiday_short_deadline_status,
        "venue_commission_per_side_usd": venue.venue_commission_per_side_usd,
        "pine_commission_per_side_usd": venue.pine_commission_per_side_usd,
        "export_implied_commission_per_side_usd": (
            venue.export_implied_commission_per_side_usd
        ),
        "contract_month_attribution_status": venue.contract_month_attribution_status,
        "roll_seam_attribution_status": venue.roll_seam_attribution_status,
        "bid_ask_spread_status": venue.bid_ask_spread_status,
        "issue_counts": issue_counts,
        "issues": issue_summary,
        "source_identity": {
            "export_filename": spec.export_filename,
            "export_sha256": spec.export_sha256,
            "export_bytes": spec.export_bytes,
            "pine_filename": spec.pine_filename,
            "pine_sha256": spec.pine_sha256,
            "pine_bytes": spec.pine_bytes,
            "pine_pin_status": spec.pine_pin_status,
            "pin_ref": spec.pin_ref,
            "pin_divergence": spec.pin_divergence,
        },
    }


def _render_legacy_report(manifest: dict[str, object]) -> bytes:
    """Keep the checked-in pre-R4 artifact acceptance test deterministic."""
    coverage_note = manifest.get("cme_early_close_coverage_note")
    calendar_boundary = (
        "- CME holiday-short coverage is `COMPLETE` for the observed source span; "
        "the captured early-close rows drive 12:59 ET deadlines."
        if manifest["phase1_verdict_cap"] == "COMPLETE"
        else f"- CME holiday-short coverage is `{manifest['phase1_verdict_cap']}`; no historical early-close date was inferred."
    )
    lines = [
        "# Tradeify seven-strategy Phase 1 reconciliation", "", "**Theme:** c1", "",
        "**In-flight:** yes", "",
        "**Status:** ACTIVE — strict seven-strategy Tradeify source, accounting, deadline, cap, and provenance normalization", "",
        "> **EXPLORATORY — Phase 0 was skipped.** All supplied history is development data; this report is not confirmatory, qualified, admitted, or deployable.", "",
        f"Campaign status: `{manifest['campaign_status']}`", "",
        f"Holiday-short verdict cap: `{manifest['phase1_verdict_cap']}`", "",
        "## Strategy inventory", "",
        "| Strategy | Status | Rows | Trades | Net P&L | Daily-deadline holds | Fri→Sun sub-count |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in manifest["strategies"]:
        lines.append("| {strategy_id} | {status} | {source_row_count} | {trade_count} | ${net_pnl_usd} | {overnight_holds} | {friday_to_sunday_holds} |".format(**row))
    lines.extend([
        "", "## Evidence boundaries", "",
        "- The source CSV/Pine bytes, row-level event/trade/weekly ledgers, and seven detailed issue reports remain local and gitignored.",
        "- No source row was repaired, dropped for an outcome, re-ranked, composed, simulated, or rerun in Pine.",
        "- Scalar MAE/MFE values are inventory-only excursion bounds, not timestamped paths.",
        "- Per-strategy caps are measured against 80 micro-equivalents; the joint book-cap verdict is deferred to Phase 4.",
        calendar_boundary,
        *([f"- CME early-close coverage note: {coverage_note}"] if coverage_note else []),
        "", "## Frozen hashes", "",
        f"- Config: `{manifest['inputs']['config_sha256']}`",
        f"- CME calendar capture: `{manifest['inputs']['cme_early_close_calendar_sha256']}`",
        f"- Canonical events: `{manifest['ledgers']['canonical_events_sha256']}`",
        f"- Canonical trades: `{manifest['ledgers']['canonical_trades_sha256']}`",
        f"- Weekly exit blocks: `{manifest['ledgers']['weekly_exit_blocks_sha256']}`",
        "", "## Issues by strategy", "",
    ])
    for row in manifest["strategies"]:
        lines.extend([f"### {row['strategy_id']}", ""])
        lines.extend(
            [f"- `{issue['severity']}` `{issue['code']}` × {issue['count']}" for issue in row["issues"]]
            if row["issues"] else ["- No issues."]
        )
        lines.append("")
    lines.extend([
        "## Reproduce", "",
        "Provide the frozen source directory at runtime and run `python run_phase1.py --config phase1_config.json --source-dir <source-dir> --output-dir local_artifacts`.", "",
    ])
    return "\n".join(lines).encode("utf-8")


def _render_report(manifest: dict[str, object]) -> bytes:
    if "dropped_sources" not in manifest:
        return _render_legacy_report(manifest)
    # Render the published JSON domain, not Python-only Decimal/map representations.
    manifest = json.loads(_json_bytes(manifest))
    coverage_note = manifest.get("cme_early_close_coverage_note")
    calendar_status = manifest.get("cme_early_close_calendar", {}).get("coverage_status", manifest["phase1_verdict_cap"])
    calendar = manifest.get("cme_early_close_calendar", {})
    evidence_kind = calendar.get("evidence_kind", "PRIMARY")
    secondary_metadata = calendar.get("evidence_metadata", {})
    if evidence_kind == "SECONDARY":
        full_closures = secondary_metadata["full_closure_dates"]
        sub_deadlines = secondary_metadata["sub_deadline_close_dates"]
        full_closure_inventory = ", ".join(full_closures["dates"]) or "none"
        sub_deadline_inventory = [
            f"{item['date']} {item['holiday']} — "
            + ", ".join(
                f"{group}={close}"
                for group, close in sorted(item["closes_et"].items())
            )
            for item in sub_deadlines["dates"]
        ]
        sub_deadline_rows = [f"  - {detail}" for detail in sub_deadline_inventory] or ["  - none"]
        calendar_boundary = (
            f"- CME holiday-short coverage is `{calendar_status}` with populated SECONDARY rows; "
            "the exact account-level EARLY_CLOSE union drives 12:59 ET deadlines but cannot lift the context cap."
        )
        secondary_limitations = [
            "- Secondary provenance is retained without a primary-CME upgrade: "
            f"`{secondary_metadata['source_calendar']['repo_path']}` SHA-256 "
            f"`{secondary_metadata['source_calendar']['sha256']}` under `{secondary_metadata['schema']}`.",
            f"- Secondary provenance note: {secondary_metadata['provenance_note']}",
            f"- Day basis: `{secondary_metadata['day_basis']['basis']}` — {secondary_metadata['day_basis']['note']}",
            "- CME trade-date full-closure inventory is not converted into wall-date deadlines: "
            f"{full_closures['rule']}",
            f"- Secondary full-closure inventory ({full_closures['count']}): {full_closure_inventory}",
            "- Pre-12:59 market closes remain limitations, never modeled closure/no-trade rules: "
            f"{sub_deadlines['rule']}",
            f"- Sub-deadline inventory ({sub_deadlines['count']}):",
            *sub_deadline_rows,
            *[f"- Secondary source URL (inert provenance): {url}" for url in secondary_metadata["source_urls"]],
            *[
                f"- Secondary unresolved {item['date']}: {item['issue']}"
                for item in secondary_metadata["unresolved"]
            ],
            "- Secondary source revisions remain provenance limits, not captured-byte proof: "
            f"{secondary_metadata['source_revisions']['note']}",
        ]
    elif calendar_status == "COMPLETE":
        calendar_boundary = (
            "- CME holiday-short coverage is `COMPLETE` for the observed source span; "
            "the captured early-close rows drive 12:59 ET deadlines."
        )
        secondary_limitations = []
    else:
        calendar_boundary = (
            f"- CME holiday-short coverage is `{calendar_status}`; "
            "no historical early-close date was inferred."
        )
        secondary_limitations = []
    lines = [
        "# Tradeify five-active-source Phase 1 reconciliation",
        "",
        "**Theme:** c1",
        "",
        "**In-flight:** yes",
        "",
        "**Status:** ACTIVE — strict five-source Tradeify source, accounting, deadline, cap, and provenance normalization",
        "",
        "> **EXPLORATORY — Phase 0 was skipped.** All supplied history is development data; this report is not confirmatory, qualified, admitted, or deployable.",
        "",
        f"Campaign status: `{manifest['campaign_status']}`",
        "",
        f"Phase 1 evidence verdict cap: `{manifest['phase1_verdict_cap']}`",
        "",
        f"Runner generation: `{manifest['runner_version']}`",
        "",
        "## Continuous-contract roll disposition",
        "",
        f"D13: `{manifest['continuous_contract_roll_policy']['disposition']}` — contract-month and seam attribution remain unavailable, not modeled or resolved.",
        "",
        manifest["continuous_contract_roll_policy"]["ruling_ref"],
        "",
        *[f"- {obligation}" for obligation in manifest["continuous_contract_roll_policy"]["obligations"]],
        "",
        "## Strategy inventory",
        "",
        "| Strategy | Status | Pine pin status | Pin ref | Divergence | Export bytes | Pine bytes | Rows | Trades | Net P&L | Daily-deadline holds | Fri→Sun sub-count |",
        "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in manifest["strategies"]:
        lines.append(
            "| {strategy_id} | {status} | {pine_pin_status} | {pin_ref} | {pin_divergence} | "
            "{export_bytes} | {pine_bytes} | {source_row_count} | {trade_count} | "
            "${net_pnl_usd} | {overnight_holds} | {friday_to_sunday_holds} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Dropped source inventory",
            "",
            "These exports are provenance only and are never normalized, counted, or used in ledgers or weekly results.",
            "",
            "| Previous strategy ID | Export | Export SHA-256 | Pine | Pine SHA-256 | Pin ref | Reason |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for source in manifest["dropped_sources"]:
        lines.append(
            "| {strategy_id_as_named_before} | {export_filename} | {export_sha256} | "
            "{pine_filename} | {pine_sha256} | {pin_ref} | {reason} |".format(**source)
        )
    lines.extend(
        [
            "",
            "## Evidence boundaries",
            "",
            "- The source CSV/Pine bytes, row-level event/trade/weekly ledgers, and five detailed issue reports remain local and gitignored.",
            "- No source row was repaired, dropped for an outcome, re-ranked, composed, simulated, or rerun in Pine.",
            "- Scalar MAE/MFE values are inventory-only excursion bounds, not timestamped paths.",
            "- Per-strategy caps are measured against 80 micro-equivalents; the joint book-cap verdict is deferred to Phase 4.",
            calendar_boundary,
            *(
                [f"- CME early-close coverage note: {coverage_note}"]
                if coverage_note
                else []
            ),
            *secondary_limitations,
            "",
            "## Frozen hashes",
            "",
            f"- Config: `{manifest['inputs']['config_sha256']}`",
            f"- Tradeify fee capture: `{manifest['inputs']['tradeify_commission_schedule_sha256']}`",
            f"- CME calendar capture: `{manifest['inputs']['cme_early_close_calendar_sha256']}`",
            f"- Independent TradingView anchors: `{manifest['inputs']['tv_summary_anchors_sha256']}`",
            f"- Canonical events: `{manifest['ledgers']['canonical_events_sha256']}`",
            f"- Canonical trades: `{manifest['ledgers']['canonical_trades_sha256']}`",
            f"- Weekly exit blocks: `{manifest['ledgers']['weekly_exit_blocks_sha256']}`",
            *[
                f"- Detail report {strategy_id}: `{digest}`"
                for strategy_id, digest in sorted(manifest["local_strategy_report_sha256"].items())
            ],
            "",
            "## Issues by strategy",
            "",
        ]
    )
    for row in manifest["strategies"]:
        lines.append(f"### {row['strategy_id']}")
        lines.append("")
        if row["issues"]:
            for issue in row["issues"]:
                lines.append(
                    f"- `{issue['severity']}` `{issue['code']}` × {issue['count']}"
                )
        else:
            lines.append("- No issues.")
        lines.append("")
    lines.extend([
        "## Independent TradingView summary reconciliation", "",
        f"G1.4 coverage: `{manifest['summary_reconciliation_status']}`. {manifest['summary_coverage_note']}", "",
        "Observed max drawdown uses closed-trade exit equity; TradingView panel equity drawdown may differ. Discrepancies remain blockers; no series is repaired.", "",
    ])
    for row in manifest["strategies"]:
        lines.extend([f"### {row['strategy_id']}", "", row["summary_source_note"] or "No independent operator summary supplied.", "",
                      "| Metric | Observed | Anchor | Difference | Tolerance | Status |",
                      "|---|---|---|---|---|---|",
                      *["| {metric} | {observed} | {anchor} | {difference} | {tolerance} | {status} |".format(**comparison)
                        for comparison in row["summary_comparisons"]], ""])
    lines.extend(
        [
            "## Reproduce",
            "",
            "Provide the frozen source directory at runtime and run `python run_phase1.py --config phase1_config.json --source-dir <source-dir> --output-dir local_artifacts`.",
            "",
        ]
    )
    return "\n".join(lines).encode("utf-8")


def run_campaign(
    config_path: str | Path,
    source_dir: str | Path,
    output_dir: str | Path,
) -> CampaignResult:
    """Verify every source first, then normalize and publish deterministic outputs."""
    config_path = Path(config_path).resolve()
    source_dir = Path(source_dir).resolve()
    output_dir = Path(output_dir).resolve()
    campaign_dir = config_path.parent
    fee_path = campaign_dir / "tradeify_commission_schedule.json"
    calendar_path = campaign_dir / "cme_early_close_calendar.json"

    _validate_output_dir(output_dir)
    inventory = load_source_inventory(config_path)
    roll_policy = inventory.continuous_contract_roll_policy
    roll_policy_record = asdict(roll_policy)
    specs = inventory.specs
    _validate_strategy_roster(specs)
    _validate_dropped_source_roster(inventory.dropped_sources)
    fee_schedule = load_fee_schedule(fee_path)
    early_close_calendar = load_early_close_calendar(calendar_path)
    summary_inventory = load_summary_anchors(campaign_dir / "tv_summary_anchors.json", specs)
    verified = [verify_source_pair(source_dir, spec) for spec in specs]

    normalized_by_strategy = {
        source.spec.strategy_id: normalize_export(source) for source in verified
    }
    events_by_strategy = {
        strategy_id: normalized.events
        for strategy_id, normalized in normalized_by_strategy.items()
    }
    _validate_calendar_coverage(events_by_strategy, early_close_calendar)

    trades_by_strategy: dict[str, pd.DataFrame] = {}
    issues_by_strategy: dict[str, tuple[object, ...]] = {}
    strategy_records: list[dict[str, object]] = []
    summaries_by_strategy: dict[str, dict[str, object]] = {}
    for source in verified:
        normalized = normalized_by_strategy[source.spec.strategy_id]
        reconstruction = reconstruct_trades(normalized.events, source.spec)
        accounting = calculate_accounting(reconstruction.trades)
        venue = analyze_venue(
            reconstruction.trades,
            source.spec,
            fee_schedule,
            early_close_calendar=early_close_calendar,
            continuous_contract_roll_policy=roll_policy,
        )
        comparisons, summary_issues = reconcile_summary(accounting, source.spec, summary_inventory)
        anchor = summary_inventory.anchors.get(source.spec.strategy_id)
        summary_record = {
            "continuous_contract_roll_policy": roll_policy_record,
            "summary_source_note": anchor["source_note"] if anchor else None,
            "summary_comparisons": comparisons,
        }
        summaries_by_strategy[source.spec.strategy_id] = summary_record
        issues = (*normalized.issues, *reconstruction.issues, *accounting.issues, *venue.issues, *summary_issues)
        trades_by_strategy[source.spec.strategy_id] = reconstruction.trades
        issues_by_strategy[source.spec.strategy_id] = issues
        strategy_records.append(
            _strategy_record(
                source.spec,
                normalized.events,
                reconstruction.trades,
                accounting,
                venue,
                issues,
            ) | summary_record
        )

    joint_events = build_joint_events(
        events_by_strategy,
        encoded_instruments_by_strategy={
            spec.strategy_id: spec.encoded_instrument for spec in specs
        },
    )
    canonical_trades = pd.concat(
        [trades_by_strategy[spec.strategy_id] for spec in specs],
        ignore_index=True,
        sort=False,
    )
    weekly_blocks = build_weekly_exit_blocks(trades_by_strategy)
    event_bytes = _csv_bytes(joint_events)
    trade_bytes = _csv_bytes(canonical_trades)
    weekly_bytes = _csv_bytes(weekly_blocks)
    detail_payloads: dict[Path, bytes] = {}
    local_strategy_report_sha256: dict[str, str] = {}
    for spec in specs:
        strategy_id = spec.strategy_id
        detail_bytes = _json_bytes(
            {
                "claim_class": "EXPLORATORY",
                "strategy_id": strategy_id,
                "source_identity": {
                    "export_filename": spec.export_filename,
                    "export_sha256": spec.export_sha256,
                    "export_bytes": spec.export_bytes,
                    "pine_filename": spec.pine_filename,
                    "pine_sha256": spec.pine_sha256,
                    "pine_bytes": spec.pine_bytes,
                    "pine_pin_status": spec.pine_pin_status,
                    "pin_ref": spec.pin_ref,
                    "pin_divergence": spec.pin_divergence,
                },
                "issues": _detailed_issue_rows(issues_by_strategy[strategy_id]),
                **summaries_by_strategy[strategy_id],
            }
        )
        detail_payloads[
            output_dir / "strategy_reports" / f"{strategy_id}.json"
        ] = detail_bytes
        local_strategy_report_sha256[strategy_id] = _digest(detail_bytes)

    campaign_status = (
        "BLOCKED_EXPLORATORY"
        if any(row["status"] == "BLOCKED_EXPLORATORY" for row in strategy_records)
        else "RECONCILED_EXPLORATORY"
    )
    manifest: dict[str, object] = {
        "claim_class": "EXPLORATORY",
        "phase0_status": "SKIPPED_BY_OPERATOR",
        "campaign_status": campaign_status,
        "phase1_verdict_cap": (
            "COMPLETE" if early_close_calendar.coverage_status == summary_inventory.coverage_status == "COMPLETE"
            else "NEEDS_CONTEXT"
        ),
        "summary_reconciliation_status": summary_inventory.coverage_status,
        "summary_coverage_note": summary_inventory.coverage_note,
        "cme_early_close_calendar": {
            "source_url": early_close_calendar.source_url,
            "page_date": early_close_calendar.page_date,
            "observed_date": early_close_calendar.observed_date,
            "coverage_start": early_close_calendar.coverage_start,
            "coverage_end": early_close_calendar.coverage_end,
            "coverage_status": early_close_calendar.coverage_status,
            "coverage_note": early_close_calendar.coverage_note,
            "sources": [dict(source) for source in early_close_calendar.sources],
            "observed_row_count": len(early_close_calendar.early_close_dates),
            "evidence_kind": early_close_calendar.evidence_kind,
            "source_calendar_sha256": early_close_calendar.source_calendar_sha256,
            "evidence_metadata": _plain_evidence(early_close_calendar.evidence_metadata),
        },
        "cme_early_close_coverage_note": early_close_calendar.coverage_note,
        "runner_version": _RUNNER_VERSION,
        "continuous_contract_roll_policy": roll_policy_record,
        "git_base_commit": _BASE_COMMIT,
        "inputs": {
            "config_sha256": inventory.config_sha256,
            "tradeify_commission_schedule_sha256": fee_schedule.input_sha256,
            "cme_early_close_calendar_sha256": early_close_calendar.input_sha256,
            "tv_summary_anchors_sha256": summary_inventory.input_sha256,
        },
        "ledgers": {
            "timestamp_domain": (
                joint_events["timestamp_domain"].iloc[0]
                if not joint_events.empty
                else "UTC"
            ),
            "canonical_events_sha256": _digest(event_bytes),
            "source_row_sha256": {
                "algorithm": "SHA-256",
                "input": "exact raw CSV record bytes including original record terminator when present",
            },
            "canonical_trades_sha256": _digest(trade_bytes),
            "weekly_exit_blocks_sha256": _digest(weekly_bytes),
        },
        "local_strategy_report_sha256": local_strategy_report_sha256,
        "tolerances": {
            "aggregate_money_usd": "0.01",
            "tick_grid_ticks": "1e-9",
            "duplicated_source_fee_and_identity": "exact",
            "tv_summary": SUMMARY_TOLERANCES,
        },
        "strategies": strategy_records,
        "dropped_sources": [
            {
                "strategy_id_as_named_before": source.strategy_id_as_named_before,
                "export_filename": source.export_filename,
                "export_sha256": source.export_sha256,
                "pine_filename": source.pine_filename,
                "pine_sha256": source.pine_sha256,
                "pin_ref": source.pin_ref,
                "reason": source.reason,
            }
            for source in inventory.dropped_sources
        ],
    }
    manifest_bytes = _json_bytes(manifest)
    report_bytes = _render_report(manifest)
    manifest_path = campaign_dir / "reconciliation_manifest.json"
    report_path = campaign_dir / "RESULTS.md"
    _publish_payloads(
        {
            output_dir / "canonical_events.csv": event_bytes,
            output_dir / "canonical_trades.csv": trade_bytes,
            output_dir / "weekly_exit_blocks.csv": weekly_bytes,
            **detail_payloads,
            manifest_path: manifest_bytes,
            report_path: report_bytes,
        }
    )
    return CampaignResult(
        status=campaign_status,
        manifest_path=manifest_path,
        report_path=report_path,
        manifest_bytes=manifest_bytes,
        report_bytes=report_bytes,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)
    config = Path(args.config)
    output = Path(args.output_dir) if args.output_dir else config.parent / "local_artifacts"
    try:
        run_campaign(config, args.source_dir, output)
    except (SourceIdentityError, TradeExportSchemaError) as exc:
        print(f"intake failure: {exc}", file=sys.stderr)
        return 3
    except ValueError as exc:
        print(f"configuration failure: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"output failure: {exc}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
