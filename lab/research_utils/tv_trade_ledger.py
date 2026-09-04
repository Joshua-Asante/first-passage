"""Frozen source identity and primary-fee boundaries for Tradeify Phase 1."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path, PurePosixPath
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
        "export_bytes",
        "pine_filename",
        "pine_sha256",
        "pine_input_overrides_sha256",
        "pine_bytes",
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
        "pine_pyramiding_pct",
        "pine_pin_status",
        "pin_ref",
        "pin_divergence",
        "contract_cap",
    }
)
_DROPPED_SOURCE_KEYS = frozenset(
    {
        "strategy_id_as_named_before",
        "export_filename",
        "export_sha256",
        "pine_filename",
        "pine_sha256",
        "pin_ref",
        "reason",
    }
)
_PINE_PIN_STATUSES = frozenset(
    {
        "NOT_IN_PORT_MANIFEST",
        "PINNED_RESEARCH_VARIANT",
        "PINNED_SWAP_PROTOTYPE",
        "UNPINNED_MODIFIED",
    }
)
_DROP_REASON = "SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN"
_PORT_MANIFEST_PREFIX = "core/strategies/PORT_MANIFEST.sha256:"
_PORT_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "core/strategies/PORT_MANIFEST.sha256"
_ROLL_OBLIGATIONS = (
    "Phase 3 pre-registration states back-adjustment seam risk as a limitation of every campaign claim: fills cannot be attributed to a contract month, and a seam crossing is indistinguishable from a price move.",
    "A Phase 6 seam-sensitivity check is pre-registered with its severity frozen alongside the other Phase 6 cutoffs.",
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
EVENT_COLUMNS = (
    "strategy_id",
    "encoded_instrument",
    "source_trade_id",
    "source_row_number",
    "source_row_sha256",
    "timestamp_raw",
    "timestamp_naive",
    "timestamp_utc",
    "exchange_session_date",
    "type_raw",
    "event_type",
    "direction",
    "signal",
    "price_usd",
    "quantity",
    "size_value_usd",
    "net_pnl_usd",
    "return_pct",
    "commission_usd",
    "favorable_excursion_usd",
    "favorable_excursion_pct",
    "adverse_excursion_usd",
    "adverse_excursion_pct",
    "cumulative_pnl_usd",
    "cumulative_pnl_pct",
    "duration_bars",
    "concurrent_timestamp",
)
_EMPTY_EVENT_DTYPES = {
    "strategy_id": "object",
    "encoded_instrument": "object",
    "source_trade_id": "int64",
    "source_row_number": "int64",
    "source_row_sha256": "object",
    "timestamp_raw": "object",
    "timestamp_naive": "datetime64[ns]",
    "timestamp_utc": "datetime64[ns, UTC]",
    "exchange_session_date": "object",
    "type_raw": "object",
    "event_type": "object",
    "direction": "object",
    "signal": "object",
    "price_usd": "object",
    "quantity": "int64",
    "size_value_usd": "object",
    "net_pnl_usd": "object",
    "return_pct": "object",
    "commission_usd": "object",
    "favorable_excursion_usd": "object",
    "favorable_excursion_pct": "object",
    "adverse_excursion_usd": "object",
    "adverse_excursion_pct": "object",
    "cumulative_pnl_usd": "object",
    "cumulative_pnl_pct": "object",
    "duration_bars": "object",
    "concurrent_timestamp": "bool",
}
COLUMN_ALIASES = {
    "Trade #": "Trade number",
    "Net P&L USD": "Net PnL USD",
}
_DECIMAL_RE = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)\Z")
_TIMESTAMP_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}\Z")


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
    pine_input_overrides_sha256: str
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
    pine_pyramiding_pct: Decimal
    pine_pin_status: Literal[
        "NOT_IN_PORT_MANIFEST",
        "PINNED_RESEARCH_VARIANT",
        "PINNED_SWAP_PROTOTYPE",
        "UNPINNED_MODIFIED",
    ]
    pin_divergence: str | None
    contract_cap: int
    export_bytes: int = 0
    pine_bytes: int = 0
    pin_ref: str | None = None


@dataclass(frozen=True)
class VerifiedSource:
    spec: SourceSpec
    export_path: Path
    pine_path: Path
    export_bytes: bytes


@dataclass(frozen=True)
class DroppedSource:
    """A validated provenance record which is intentionally never normalized."""

    strategy_id_as_named_before: str
    export_filename: str
    export_sha256: str
    pine_filename: str
    pine_sha256: str
    pin_ref: str
    reason: Literal["SWAP_PORT_BODY_POINT_VALUE_NOT_OVERRIDDEN"]


@dataclass(frozen=True)
class ContinuousContractRollPolicy:
    disposition: Literal["ACCEPTED_UNMODELED", "UNRESOLVED"]
    ruling_date: date
    ruling_ref: str
    obligations: tuple[str, ...]


@dataclass(frozen=True)
class SourceInventory:
    """One parsed configuration snapshot shared by active and dropped inventories."""

    specs: tuple[SourceSpec, ...]
    dropped_sources: tuple[DroppedSource, ...]
    config_sha256: str
    continuous_contract_roll_policy: ContinuousContractRollPolicy


@dataclass(frozen=True)
class FeeSchedule:
    source_url: str
    page_date: date
    observed_date: date
    totals_include: str
    round_trip_usd: Mapping[str, Decimal]
    per_side_usd: Mapping[str, Decimal]
    input_sha256: str


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


def _load_json_snapshot(path: Path) -> tuple[object, bytes]:
    """Read a configuration once so consumers share both values and its digest."""
    try:
        raw = path.read_bytes()
        return json.loads(raw.decode("utf-8")), raw
    except OSError as exc:
        raise ValueError(f"cannot read JSON configuration: {path}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
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


def _validate_byte_count(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a non-negative integer")
    return value


def _manifest_target(value: str) -> str:
    target = PurePosixPath(value)
    if (
        not value or not target.parts or value != value.strip() or target.is_absolute()
        or str(target) != value or any(part in {".", ".."} for part in target.parts)
        or "\\" in value or ":" in value or any(ord(char) < 32 for char in value)
    ):
        raise ValueError("pin target must be a safe normalized repo-relative path")
    return value


def _load_port_manifest(path: Path) -> Mapping[str, str]:
    try:
        lines = path.read_bytes().decode("utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError("cannot read PORT_MANIFEST.sha256") from exc
    pins: dict[str, str] = {}
    for line_number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
        if match is None:
            raise ValueError(f"invalid PORT_MANIFEST row {line_number}")
        digest, target = match.groups()
        target = _manifest_target(target)
        if target in pins:
            raise ValueError(f"duplicate PORT_MANIFEST path: {target}")
        pins[target] = digest
    return MappingProxyType(pins)


def _validate_pin_ref(
    value: object, field: str, *, required: bool, pins: Mapping[str, str],
    pine_filename: str, pine_sha256: str | None,
) -> str | None:
    if value is None and not required:
        return None
    reference = _require_nonempty_string(value, field)
    if not reference.startswith(_PORT_MANIFEST_PREFIX):
        raise ValueError(f"{field} must reference PORT_MANIFEST.sha256")
    target = _manifest_target(reference[len(_PORT_MANIFEST_PREFIX):])
    if target not in pins:
        raise ValueError(f"pin target not found in PORT_MANIFEST: {target}")
    if pine_sha256 is not None:
        if PurePosixPath(target).name != pine_filename:
            raise ValueError(f"pin basename mismatch: {target}")
        if pins[target] != pine_sha256:
            raise ValueError(f"pin hash mismatch: {target}")
    return reference


def _source_spec(value: object, pins: Mapping[str, str]) -> SourceSpec:
    record = _require_exact_keys(value, _SOURCE_KEYS, "strategy")
    strategy_id = _require_nonempty_string(record["strategy_id"], "strategy_id")
    export_hash = _require_nonempty_string(record["export_sha256"], "export_sha256")
    pine_hash = _require_nonempty_string(record["pine_sha256"], "pine_sha256")
    overrides_hash = _require_nonempty_string(
        record["pine_input_overrides_sha256"], "pine_input_overrides_sha256"
    )
    if not _HASH_RE.fullmatch(overrides_hash):
        raise ValueError(f"invalid pine_input_overrides_sha256 for {strategy_id}")
    if not _HASH_RE.fullmatch(export_hash):
        raise ValueError(f"invalid export_sha256 for {strategy_id}")
    if not _HASH_RE.fullmatch(pine_hash):
        raise ValueError(f"invalid pine_sha256 for {strategy_id}")
    pine_pin_status = _require_nonempty_string(
        record["pine_pin_status"], "pine_pin_status"
    )
    if pine_pin_status not in _PINE_PIN_STATUSES:
        raise ValueError(
            "pine_pin_status must be one of "
            f"{sorted(_PINE_PIN_STATUSES)!r}: {pine_pin_status}"
        )
    pin_ref = record["pin_ref"]
    pin_divergence = record["pin_divergence"]
    if pine_pin_status == "PINNED_RESEARCH_VARIANT":
        if not isinstance(pin_divergence, str) or not pin_divergence.strip():
            raise ValueError("PINNED_RESEARCH_VARIANT requires a non-empty pin_divergence")
        if pin_ref is None:
            raise ValueError("PINNED_RESEARCH_VARIANT requires a pin_ref")
    elif pine_pin_status == "NOT_IN_PORT_MANIFEST":
        if pin_ref is not None or pin_divergence is not None:
            raise ValueError("NOT_IN_PORT_MANIFEST requires null pin_ref and pin_divergence")
    elif pine_pin_status == "UNPINNED_MODIFIED":
        if not isinstance(pin_divergence, str) or not pin_divergence.strip():
            raise ValueError("UNPINNED_MODIFIED requires a non-empty pin_divergence")
    elif pin_divergence is not None:
        raise ValueError("pin_divergence must be null unless pine_pin_status is a modified body")
    pin_ref = _validate_pin_ref(
        pin_ref, "pin_ref", required=pine_pin_status != "NOT_IN_PORT_MANIFEST", pins=pins,
        pine_filename=_validate_filename(record["pine_filename"], "pine_filename"),
        pine_sha256=None if pine_pin_status == "UNPINNED_MODIFIED" else pine_hash,
    )
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
        export_bytes=_validate_byte_count(record["export_bytes"], "export_bytes"),
        pine_filename=_validate_filename(record["pine_filename"], "pine_filename"),
        pine_sha256=pine_hash,
        pine_input_overrides_sha256=overrides_hash,
        pine_bytes=_validate_byte_count(record["pine_bytes"], "pine_bytes"),
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
        pine_pyramiding_pct=_require_decimal(
            record["pine_pyramiding_pct"], "pine_pyramiding_pct", allow_zero=True
        ),
        pine_pin_status=pine_pin_status,
        pin_ref=pin_ref,
        pin_divergence=pin_divergence,
        contract_cap=record["contract_cap"],
    )


def _dropped_source(value: object, pins: Mapping[str, str]) -> DroppedSource:
    record = _require_exact_keys(value, _DROPPED_SOURCE_KEYS, "dropped source")
    strategy_id = _require_nonempty_string(
        record["strategy_id_as_named_before"], "strategy_id_as_named_before"
    )
    export_hash = _require_nonempty_string(record["export_sha256"], "export_sha256")
    pine_hash = _require_nonempty_string(record["pine_sha256"], "pine_sha256")
    if not _HASH_RE.fullmatch(export_hash) or not _HASH_RE.fullmatch(pine_hash):
        raise ValueError(f"invalid dropped source hash for {strategy_id}")
    pine_filename = _validate_filename(record["pine_filename"], "pine_filename")
    pin_ref = _validate_pin_ref(
        record["pin_ref"], "pin_ref", required=True, pins=pins,
        pine_filename=pine_filename, pine_sha256=pine_hash,
    )
    if record["reason"] != _DROP_REASON:
        raise ValueError(f"dropped source reason must be {_DROP_REASON}")
    return DroppedSource(
        strategy_id_as_named_before=strategy_id,
        export_filename=_validate_filename(record["export_filename"], "export_filename"),
        export_sha256=export_hash,
        pine_filename=pine_filename,
        pine_sha256=pine_hash,
        pin_ref=pin_ref,
        reason=record["reason"],
    )


def _roll_policy(value: object) -> ContinuousContractRollPolicy:
    record = _require_exact_keys(value, frozenset({"disposition", "ruling_date", "ruling_ref", "obligations"}), "continuous contract roll policy")
    disposition = _require_nonempty_string(record["disposition"], "roll disposition")
    if disposition not in {"ACCEPTED_UNMODELED", "UNRESOLVED"}:
        raise ValueError("invalid continuous contract roll disposition")
    date_text = _require_nonempty_string(record["ruling_date"], "roll ruling_date")
    ruling_date = date.fromisoformat(date_text)
    if ruling_date.isoformat() != date_text:
        raise ValueError("roll ruling_date must be an ISO calendar date")
    ruling_ref = _require_nonempty_string(record["ruling_ref"], "roll ruling_ref")
    obligations = record["obligations"]
    if not isinstance(obligations, list):
        raise ValueError("roll obligations must be an array")
    obligations = tuple(_require_nonempty_string(item, "roll obligation") for item in obligations)
    if len(set(obligations)) != len(obligations):
        raise ValueError("roll obligations must be distinct")
    if disposition == "ACCEPTED_UNMODELED" and set(obligations) != set(_ROLL_OBLIGATIONS):
        raise ValueError("accepted roll policy requires both frozen obligations")
    if disposition == "UNRESOLVED" and obligations:
        raise ValueError("unresolved roll policy must not claim accepted obligations")
    return ContinuousContractRollPolicy(disposition, ruling_date, ruling_ref, obligations)


def load_source_inventory(path: str | Path) -> SourceInventory:
    """Load one strict snapshot of active and dropped exploratory source identities."""
    payload_value, raw_config = _load_json_snapshot(Path(path))
    payload = _require_exact_keys(
        payload_value,
        frozenset({"claim_class", "platform", "strategies", "dropped_sources", "continuous_contract_roll_policy"}),
        "source configuration",
    )
    if payload["claim_class"] != "EXPLORATORY":
        raise ValueError("claim_class must be EXPLORATORY")
    _require_nonempty_string(payload["platform"], "platform")
    strategies = payload["strategies"]
    if not isinstance(strategies, list) or not strategies:
        raise ValueError("strategies must be a non-empty array")
    roll_policy = _roll_policy(payload["continuous_contract_roll_policy"])
    pins = _load_port_manifest(_PORT_MANIFEST_PATH)
    specs = tuple(_source_spec(strategy, pins) for strategy in strategies)
    dropped_records = payload["dropped_sources"]
    if not isinstance(dropped_records, list):
        raise ValueError("dropped_sources must be an array")
    dropped_sources = tuple(_dropped_source(source, pins) for source in dropped_records)
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
    for source in dropped_sources:
        if source.strategy_id_as_named_before in strategy_ids:
            raise ValueError(f"active and dropped identity collision: {source.strategy_id_as_named_before}")
        strategy_ids.add(source.strategy_id_as_named_before)
        for filename in (source.export_filename, source.pine_filename):
            if filename in basenames:
                raise ValueError(f"duplicate source basename: {filename}")
            basenames.add(filename)
    return SourceInventory(
        specs=specs,
        dropped_sources=dropped_sources,
        config_sha256=sha256(raw_config).hexdigest(),
        continuous_contract_roll_policy=roll_policy,
    )


def load_source_specs(path: str | Path) -> tuple[SourceSpec, ...]:
    """Load active specs while preserving the established narrow API."""
    return load_source_inventory(path).specs


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
    """Verify both source files match their frozen filenames, sizes, and hashes."""
    root = Path(source_dir)
    export_path = _resolved_child(root, spec.export_filename, "export")
    pine_path = _resolved_child(root, spec.pine_filename, "Pine")
    try:
        export_bytes = export_path.read_bytes()
    except OSError as exc:
        raise SourceIdentityError(f"cannot read export source: {export_path.name}") from exc
    if len(export_bytes) != spec.export_bytes:
        raise SourceIdentityError(
            f"{export_path.name} byte length mismatch: expected {spec.export_bytes}, "
            f"observed {len(export_bytes)}"
        )
    observed_export = sha256(export_bytes).hexdigest()
    if observed_export != spec.export_sha256:
        raise SourceIdentityError(
            f"{export_path.name} SHA-256 mismatch: expected {spec.export_sha256}, observed {observed_export}"
        )
    try:
        pine_bytes = pine_path.read_bytes()
    except OSError as exc:
        raise SourceIdentityError(f"cannot read Pine source: {pine_path.name}") from exc
    if len(pine_bytes) != spec.pine_bytes:
        raise SourceIdentityError(
            f"{pine_path.name} byte length mismatch: expected {spec.pine_bytes}, "
            f"observed {len(pine_bytes)}"
        )
    observed_pine = sha256(pine_bytes).hexdigest()
    if observed_pine != spec.pine_sha256:
        raise SourceIdentityError(
            f"{pine_path.name} SHA-256 mismatch: expected {spec.pine_sha256}, observed {observed_pine}"
        )
    return VerifiedSource(
        spec=spec,
        export_path=export_path,
        pine_path=pine_path,
        export_bytes=export_bytes,
    )


def load_fee_schedule(path: str | Path) -> FeeSchedule:
    """Load the compact, primary-source Tradeify fee capture."""
    keys = frozenset({"source_url", "page_date", "observed_date", "totals_include", "rows"})
    value, raw = _load_json_snapshot(Path(path))
    payload = _require_exact_keys(value, keys, "fee schedule")
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
    required_symbols = {"6J", "MNQ", "MYM", "MGC"}
    if set(round_trip) != required_symbols:
        missing = sorted(required_symbols - set(round_trip))
        unexpected = sorted(set(round_trip) - required_symbols)
        raise ValueError(
            "fee schedule symbols mismatch: "
            f"missing={missing}, unexpected={unexpected}"
        )
    return FeeSchedule(
        input_sha256=sha256(raw).hexdigest(),
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
    if not isinstance(value, str) or not _TIMESTAMP_RE.fullmatch(value):
        raise TradeExportSchemaError(
            "Date and time must match %Y-%m-%d %H:%M exactly: "
            f"{value!r}"
        )
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
    row: Mapping[str, object], source_row_number: int, source_row_bytes: bytes, spec: SourceSpec
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
        "encoded_instrument": spec.encoded_instrument,
        "source_trade_id": _parse_positive_integral(row["Trade number"], "Trade number"),
        "source_row_number": source_row_number,
        "source_row_sha256": sha256(source_row_bytes).hexdigest(),
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


def _raw_csv_records(payload: bytes) -> list[bytes]:
    """Split RFC-style CSV bytes without normalizing row terminators or quoted fields."""
    records: list[bytes] = []
    start = 0
    index = 0
    in_quotes = False
    at_field_start = True
    while index < len(payload):
        byte = payload[index]
        if byte == ord('"'):
            if in_quotes and index + 1 < len(payload) and payload[index + 1] == ord('"'):
                index += 2
                at_field_start = False
                continue
            if in_quotes:
                in_quotes = False
            elif at_field_start:
                in_quotes = True
            at_field_start = False
        elif not in_quotes and byte in (ord("\r"), ord("\n")):
            terminator_length = 2 if byte == ord("\r") and index + 1 < len(payload) and payload[index + 1] == ord("\n") else 1
            end = index + terminator_length
            records.append(payload[start:end])
            start = end
            index = end
            at_field_start = True
            continue
        elif not in_quotes and byte == ord(","):
            at_field_start = True
        else:
            at_field_start = False
        index += 1
    if start < len(payload):
        records.append(payload[start:])
    return records


def _parse_csv_record(record: bytes, *, header: bool) -> list[str]:
    encoding = "utf-8-sig" if header else "utf-8"
    text = record.decode(encoding)
    rows = list(csv.reader(StringIO(text, newline="")))
    if len(rows) != 1:
        raise TradeExportSchemaError("CSV record parsing did not yield exactly one record")
    return rows[0]


def normalize_export(source: VerifiedSource) -> NormalizationResult:
    """Parse a verified TradingView export into strictly typed, stable event rows."""
    try:
        records = _raw_csv_records(source.export_bytes)
        if not records:
            raise TradeExportSchemaError("CSV export has no header row")
        headers = _normalized_headers(_parse_csv_record(records[0], header=True))
        events: list[dict[str, object]] = []
        for source_row_number, raw_record in enumerate(records[1:], start=1):
            values = _parse_csv_record(raw_record, header=False)
            if len(values) != len(headers):
                raise TradeExportSchemaError(
                    f"source row {source_row_number} has {len(values)} fields; "
                    f"expected {len(headers)}"
                )
            raw = dict(zip(headers, values, strict=False))
            canonical_row = {
                COLUMN_ALIASES.get(header, header): value for header, value in raw.items()
            }
            events.append(
                _event_record(canonical_row, source_row_number, raw_record, source.spec)
            )
    except UnicodeDecodeError as exc:
        raise TradeExportSchemaError(
            f"TradingView export is not valid UTF-8: {source.export_path.name}"
        ) from exc
    events.sort(key=lambda event: (event["timestamp_naive"], event["source_row_number"]))
    timestamp_counts: dict[pd.Timestamp, int] = {}
    for event in events:
        timestamp = event["timestamp_naive"]
        timestamp_counts[timestamp] = timestamp_counts.get(timestamp, 0) + 1
    for event in events:
        event["concurrent_timestamp"] = timestamp_counts[event["timestamp_naive"]] > 1
    frame = (
        pd.DataFrame(events, columns=EVENT_COLUMNS)
        if events
        else pd.DataFrame(
            {
                column: pd.Series(dtype=_EMPTY_EVENT_DTYPES[column])
                for column in EVENT_COLUMNS
            }
        )
    )
    return NormalizationResult(events=frame, issues=())
