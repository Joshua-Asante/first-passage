"""Frozen source identity and primary-fee boundaries for Tradeify Phase 1."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Literal, Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pandas as pd


_HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
_SOURCE_KEYS = frozenset(
    {
        "strategy_id",
        "intended_instrument",
        "encoded_instrument",
        "export_filename",
        "export_sha256",
        "pine_filename",
        "pine_sha256",
        "source_timezone",
        "session_timezone",
        "declared_bar_size_minutes",
        "declared_session",
        "direction_evidence",
        "quantity_convention",
        "continuous_symbol",
        "synchronized_intraday_path_available",
        "lineage_notes",
        "pine_commission_per_side_usd",
        "pine_slippage_ticks_per_side",
        "contract_cap",
    }
)
_FEE_URL = "https://help.tradeify.co/en/articles/10468315-trading-commission-fees"
_FEE_PAGE_DATE = "2026-04-28"
_FEE_OBSERVED_DATE = "2026-09-02"
_FEE_TOTALS_INCLUDE = "exchange, NFA, clearing, and commission"

REQUIRED_COLUMNS = (
    "Trade number",
    "Type",
    "Date and time",
    "Signal",
    "Price USD",
    "Size (qty)",
    "Size (value)",
    "Net PnL USD",
    "Return %",
    "Commission USD",
    "Favorable excursion USD",
    "Favorable excursion %",
    "Adverse excursion USD",
    "Adverse excursion %",
    "Cumulative PnL USD",
    "Cumulative PnL %",
    "Duration (bars)",
)
COLUMN_ALIASES = {
    "Trade #": "Trade number",
    "Net P&L USD": "Net PnL USD",
}
_DECIMAL_RE = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)\Z")


class SourceIdentityError(ValueError):
    """A configured source is absent, escapes its source directory, or changed."""


class TradeExportSchemaError(ValueError):
    """A TradingView trade-list export does not meet the frozen schema contract."""


@dataclass(frozen=True)
class Issue:
    code: str
    severity: Literal["INFO", "WARNING", "BLOCKER", "FATAL"]
    strategy_id: str
    detail: Mapping[str, object]
    trade_id: int | None = None
    source_rows: tuple[int, ...] = ()


@dataclass(frozen=True)
class SourceSpec:
    strategy_id: str
    intended_instrument: str
    encoded_instrument: str
    export_filename: str
    export_sha256: str
    pine_filename: str
    pine_sha256: str
    source_timezone: str | None
    session_timezone: str
    declared_bar_size_minutes: int
    declared_session: str
    direction_evidence: str
    quantity_convention: str
    continuous_symbol: bool
    synchronized_intraday_path_available: bool
    lineage_notes: tuple[str, ...]
    pine_commission_per_side_usd: Decimal
    pine_slippage_ticks_per_side: Decimal
    contract_cap: int


@dataclass(frozen=True)
class VerifiedSource:
    spec: SourceSpec
    export_path: Path
    pine_path: Path


@dataclass(frozen=True)
class FeeSchedule:
    source_url: str
    page_date: date
    observed_date: date
    totals_include: str
    round_trip_usd: Mapping[str, Decimal]
    per_side_usd: Mapping[str, Decimal]


@dataclass(frozen=True)
class NormalizationResult:
    events: pd.DataFrame
    issues: tuple[Issue, ...]


def _load_json(path: Path) -> object:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise ValueError(f"cannot read JSON configuration: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON configuration: {path}") from exc


def _require_exact_keys(value: object, keys: frozenset[str], context: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        unexpected = sorted(actual - keys)
        raise ValueError(f"{context} keys mismatch: missing={missing}, unexpected={unexpected}")
    return value


def _require_nonempty_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _require_decimal(value: object, field: str, *, allow_zero: bool) -> Decimal:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a decimal string")
    try:
        parsed = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a finite decimal") from exc
    if not parsed.is_finite() or (parsed < 0 if allow_zero else parsed <= 0):
        comparison = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{field} must be {comparison}")
    return parsed


def _validate_timezone(value: object, field: str, *, nullable: bool) -> str | None:
    if value is None and nullable:
        return None
    name = _require_nonempty_string(value, field)
    try:
        ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"{field} is not a valid IANA timezone: {name}") from exc
    return name


def _validate_filename(value: object, field: str) -> str:
    filename = _require_nonempty_string(value, field)
    if Path(filename).name != filename:
        raise ValueError(f"{field} must be a basename: {filename}")
    return filename


def _source_spec(value: object) -> SourceSpec:
    record = _require_exact_keys(value, _SOURCE_KEYS, "strategy")
    strategy_id = _require_nonempty_string(record["strategy_id"], "strategy_id")
    export_hash = _require_nonempty_string(record["export_sha256"], "export_sha256")
    pine_hash = _require_nonempty_string(record["pine_sha256"], "pine_sha256")
    if not _HASH_RE.fullmatch(export_hash):
        raise ValueError(f"invalid export_sha256 for {strategy_id}")
    if not _HASH_RE.fullmatch(pine_hash):
        raise ValueError(f"invalid pine_sha256 for {strategy_id}")
    for field in ("declared_bar_size_minutes", "contract_cap"):
        if type(record[field]) is not int or record[field] <= 0:
            raise ValueError(f"{field} must be a positive integer")
    for field in ("continuous_symbol", "synchronized_intraday_path_available"):
        if type(record[field]) is not bool:
            raise ValueError(f"{field} must be a boolean")
    if record["continuous_symbol"] is not True:
        raise ValueError("continuous_symbol must be true for this frozen source set")
    notes = record["lineage_notes"]
    if not isinstance(notes, list) or not notes:
        raise ValueError("lineage_notes must be a non-empty array")
    lineage_notes = tuple(_require_nonempty_string(note, "lineage_notes item") for note in notes)
    return SourceSpec(
        strategy_id=strategy_id,
        intended_instrument=_require_nonempty_string(record["intended_instrument"], "intended_instrument"),
        encoded_instrument=_require_nonempty_string(record["encoded_instrument"], "encoded_instrument"),
        export_filename=_validate_filename(record["export_filename"], "export_filename"),
        export_sha256=export_hash,
        pine_filename=_validate_filename(record["pine_filename"], "pine_filename"),
        pine_sha256=pine_hash,
        source_timezone=_validate_timezone(record["source_timezone"], "source_timezone", nullable=True),
        session_timezone=_validate_timezone(record["session_timezone"], "session_timezone", nullable=False),
        declared_bar_size_minutes=record["declared_bar_size_minutes"],
        declared_session=_require_nonempty_string(record["declared_session"], "declared_session"),
        direction_evidence=_require_nonempty_string(record["direction_evidence"], "direction_evidence"),
        quantity_convention=_require_nonempty_string(record["quantity_convention"], "quantity_convention"),
        continuous_symbol=record["continuous_symbol"],
        synchronized_intraday_path_available=record["synchronized_intraday_path_available"],
        lineage_notes=lineage_notes,
        pine_commission_per_side_usd=_require_decimal(
            record["pine_commission_per_side_usd"], "pine_commission_per_side_usd", allow_zero=True
        ),
        pine_slippage_ticks_per_side=_require_decimal(
            record["pine_slippage_ticks_per_side"], "pine_slippage_ticks_per_side", allow_zero=True
        ),
        contract_cap=record["contract_cap"],
    )


def load_source_specs(path: str | Path) -> tuple[SourceSpec, ...]:
    """Load and validate the immutable exploratory source inventory."""
    payload = _require_exact_keys(
        _load_json(Path(path)),
        frozenset({"claim_class", "platform", "strategies"}),
        "source configuration",
    )
    if payload["claim_class"] != "EXPLORATORY":
        raise ValueError("claim_class must be EXPLORATORY")
    _require_nonempty_string(payload["platform"], "platform")
    strategies = payload["strategies"]
    if not isinstance(strategies, list) or not strategies:
        raise ValueError("strategies must be a non-empty array")
    specs = tuple(_source_spec(strategy) for strategy in strategies)
    strategy_ids: set[str] = set()
    basenames: set[str] = set()
    for spec in specs:
        if spec.strategy_id in strategy_ids:
            raise ValueError(f"duplicate strategy_id: {spec.strategy_id}")
        strategy_ids.add(spec.strategy_id)
        for filename in (spec.export_filename, spec.pine_filename):
            if filename in basenames:
                raise ValueError(f"duplicate source basename: {filename}")
            basenames.add(filename)
    return specs


def sha256_file(path: str | Path) -> str:
    """Return a byte-stream SHA-256 digest without loading the source in memory."""
    digest = sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _resolved_child(source_dir: Path, filename: str, kind: str) -> Path:
    root = source_dir.resolve()
    if not root.is_dir():
        raise SourceIdentityError(f"source directory is not a directory: {root}")
    path = (root / filename).resolve()
    if path.parent != root or path.name != filename:
        raise SourceIdentityError(f"{kind} filename is not a resolved child of source directory: {filename}")
    if not path.is_file():
        raise SourceIdentityError(f"{kind} source is not a regular file: {filename}")
    return path


def verify_source_pair(source_dir: str | Path, spec: SourceSpec) -> VerifiedSource:
    """Verify both source files match their frozen filenames and byte hashes."""
    root = Path(source_dir)
    export_path = _resolved_child(root, spec.export_filename, "export")
    pine_path = _resolved_child(root, spec.pine_filename, "Pine")
    for path, expected in ((export_path, spec.export_sha256), (pine_path, spec.pine_sha256)):
        observed = sha256_file(path)
        if observed != expected:
            raise SourceIdentityError(
                f"{path.name} SHA-256 mismatch: expected {expected}, observed {observed}"
            )
    return VerifiedSource(spec=spec, export_path=export_path, pine_path=pine_path)


def load_fee_schedule(path: str | Path) -> FeeSchedule:
    """Load the compact, primary-source Tradeify fee capture."""
    keys = frozenset({"source_url", "page_date", "observed_date", "totals_include", "rows"})
    payload = _require_exact_keys(_load_json(Path(path)), keys, "fee schedule")
    if payload["source_url"] != _FEE_URL:
        raise ValueError("fee schedule source_url does not match the frozen primary source")
    if payload["page_date"] != _FEE_PAGE_DATE:
        raise ValueError("fee schedule page_date does not match the frozen source capture")
    if payload["observed_date"] != _FEE_OBSERVED_DATE:
        raise ValueError("fee schedule observed_date does not match the frozen observation")
    if payload["totals_include"] != _FEE_TOTALS_INCLUDE:
        raise ValueError("fee schedule totals_include does not match the primary-source statement")
    rows = payload["rows"]
    if not isinstance(rows, list) or not rows:
        raise ValueError("fee schedule rows must be a non-empty array")
    round_trip: dict[str, Decimal] = {}
    for row in rows:
        record = _require_exact_keys(row, frozenset({"symbol", "round_trip_usd"}), "fee row")
        symbol = _require_nonempty_string(record["symbol"], "fee symbol")
        if symbol in round_trip:
            raise ValueError(f"duplicate fee symbol: {symbol}")
        amount = _require_decimal(record["round_trip_usd"], "round_trip_usd", allow_zero=False)
        if amount.as_tuple().exponent != -2:
            raise ValueError("round_trip_usd must have exactly two decimal places")
        round_trip[symbol] = amount
    return FeeSchedule(
        source_url=payload["source_url"],
        page_date=date.fromisoformat(payload["page_date"]),
        observed_date=date.fromisoformat(payload["observed_date"]),
        totals_include=payload["totals_include"],
        round_trip_usd=MappingProxyType(round_trip),
        per_side_usd=MappingProxyType(
            {symbol: (amount / Decimal("2")).quantize(Decimal("0.01")) for symbol, amount in round_trip.items()}
        ),
    )


def _normalized_headers(headers: list[str] | None) -> list[str]:
    if headers is None:
        raise TradeExportSchemaError("CSV export has no header row")
    normalized: list[str] = []
    for index, header in enumerate(headers):
        if header is None:
            raise TradeExportSchemaError("CSV export contains an unnamed header")
        if index == 0:
            header = header.removeprefix("\ufeff")
        normalized.append(COLUMN_ALIASES.get(header, header))
    duplicates = sorted({header for header in normalized if normalized.count(header) > 1})
    if duplicates:
        raise TradeExportSchemaError(f"duplicate canonical columns: {duplicates}")
    required = set(REQUIRED_COLUMNS)
    actual = set(normalized)
    missing = sorted(required - actual)
    unexpected = sorted(actual - required)
    if missing:
        raise TradeExportSchemaError(f"missing required columns: {missing}")
    if unexpected:
        raise TradeExportSchemaError(f"unexpected columns: {unexpected}")
    return normalized


def _parse_decimal(value: object, field: str) -> Decimal:
    if not isinstance(value, str) or not value.strip():
        raise TradeExportSchemaError(f"{field} must be a non-blank finite decimal")
    text = value.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
        if text.startswith("$"):
            text = text[1:]
        text = f"-{text}"
    if not _DECIMAL_RE.fullmatch(text):
        raise TradeExportSchemaError(f"{field} must be a finite decimal")
    try:
        parsed = Decimal(text)
    except InvalidOperation as exc:
        raise TradeExportSchemaError(f"{field} must be a finite decimal") from exc
    if not parsed.is_finite():
        raise TradeExportSchemaError(f"{field} must be a finite decimal")
    return parsed


def _parse_positive_integral(value: object, field: str) -> int:
    parsed = _parse_decimal(value, field)
    if parsed <= 0 or parsed != parsed.to_integral_value():
        raise TradeExportSchemaError(f"{field} must be a positive integral Decimal")
    return int(parsed)


def _classify_type(value: str) -> tuple[str, str]:
    normalized = " ".join(value.strip().lower().split())
    match normalized.split():
        case ["entry", "long"]:
            return "ENTRY", "LONG"
        case ["entry", "short"]:
            return "ENTRY", "SHORT"
        case ["exit", "long"]:
            return "EXIT", "LONG"
        case ["exit", "short"]:
            return "EXIT", "SHORT"
        case _:
            raise TradeExportSchemaError(f"unknown Type value: {value!r}")


def _parse_timestamp(value: object) -> datetime:
    if not isinstance(value, str):
        raise TradeExportSchemaError("Date and time must be a string in %Y-%m-%d %H:%M format")
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise TradeExportSchemaError(
            f"Date and time must match %Y-%m-%d %H:%M exactly: {value!r}"
        ) from exc


def _localize_unambiguous(naive: datetime, zone: ZoneInfo) -> datetime:
    valid_instants: dict[datetime, datetime] = {}
    for fold in (0, 1):
        localized = naive.replace(tzinfo=zone, fold=fold)
        utc = localized.astimezone(timezone.utc)
        round_trip = utc.astimezone(zone).replace(tzinfo=None)
        if round_trip == naive:
            valid_instants[utc] = localized
    if len(valid_instants) != 1:
        raise TradeExportSchemaError(
            f"ambiguous or nonexistent DST wall time: {naive.strftime('%Y-%m-%d %H:%M')}"
        )
    return next(iter(valid_instants.values()))


def _event_record(
    row: Mapping[str, object], source_row_number: int, spec: SourceSpec
) -> dict[str, object]:
    timestamp_raw = row["Date and time"]
    naive_datetime = _parse_timestamp(timestamp_raw)
    type_raw = row["Type"]
    if not isinstance(type_raw, str):
        raise TradeExportSchemaError("Type must be a string")
    event_type, direction = _classify_type(type_raw)
    if not isinstance(row["Signal"], str):
        raise TradeExportSchemaError("Signal must be a string")
    event: dict[str, object] = {
        "strategy_id": spec.strategy_id,
        "source_trade_id": _parse_positive_integral(row["Trade number"], "Trade number"),
        "source_row_number": source_row_number,
        "timestamp_raw": timestamp_raw,
        "timestamp_naive": pd.Timestamp(naive_datetime),
        "timestamp_utc": pd.NaT,
        "exchange_session_date": None,
        "type_raw": type_raw,
        "event_type": event_type,
        "direction": direction,
        "signal": row["Signal"],
        "price_usd": _parse_decimal(row["Price USD"], "Price USD"),
        "quantity": _parse_positive_integral(row["Size (qty)"], "Size (qty)"),
        "size_value_usd": _parse_decimal(row["Size (value)"], "Size (value)"),
        "net_pnl_usd": _parse_decimal(row["Net PnL USD"], "Net PnL USD"),
        "return_pct": _parse_decimal(row["Return %"], "Return %"),
        "commission_usd": _parse_decimal(row["Commission USD"], "Commission USD"),
        "favorable_excursion_usd": _parse_decimal(
            row["Favorable excursion USD"], "Favorable excursion USD"
        ),
        "favorable_excursion_pct": _parse_decimal(
            row["Favorable excursion %"], "Favorable excursion %"
        ),
        "adverse_excursion_usd": _parse_decimal(
            row["Adverse excursion USD"], "Adverse excursion USD"
        ),
        "adverse_excursion_pct": _parse_decimal(
            row["Adverse excursion %"], "Adverse excursion %"
        ),
        "cumulative_pnl_usd": _parse_decimal(row["Cumulative PnL USD"], "Cumulative PnL USD"),
        "cumulative_pnl_pct": _parse_decimal(row["Cumulative PnL %"], "Cumulative PnL %"),
        "duration_bars": _parse_decimal(row["Duration (bars)"], "Duration (bars)"),
    }
    if spec.source_timezone is not None:
        localized = _localize_unambiguous(naive_datetime, ZoneInfo(spec.source_timezone))
        utc = localized.astimezone(timezone.utc)
        event["timestamp_utc"] = pd.Timestamp(utc)
        event["exchange_session_date"] = utc.astimezone(ZoneInfo(spec.session_timezone)).date()
    return event


def normalize_export(source: VerifiedSource) -> NormalizationResult:
    """Parse a verified TradingView export into strictly typed, stable event rows."""
    try:
        handle = source.export_path.open(encoding="utf-8-sig", newline="")
    except OSError as exc:
        raise TradeExportSchemaError(f"cannot read TradingView export: {source.export_path.name}") from exc
    with handle:
        reader = csv.DictReader(handle)
        _normalized_headers(reader.fieldnames)
        events: list[dict[str, object]] = []
        for source_row_number, raw in enumerate(reader, start=1):
            if None in raw:
                raise TradeExportSchemaError(
                    f"source row {source_row_number} has more fields than the header"
                )
            canonical_row = {
                COLUMN_ALIASES.get(header, header): value for header, value in raw.items()
            }
            events.append(_event_record(canonical_row, source_row_number, source.spec))
    events.sort(key=lambda event: (event["timestamp_naive"], event["source_row_number"]))
    timestamp_counts: dict[pd.Timestamp, int] = {}
    for event in events:
        timestamp = event["timestamp_naive"]
        timestamp_counts[timestamp] = timestamp_counts.get(timestamp, 0) + 1
    for event in events:
        event["concurrent_timestamp"] = timestamp_counts[event["timestamp_naive"]] > 1
    return NormalizationResult(events=pd.DataFrame(events), issues=())
