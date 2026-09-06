#!/usr/bin/env python3
"""Opt-in strict validator for BAR EXPORT v0.2 List-of-Trades pages.

Read-only evidence check: detects malformed Entry rows, float-precision loss,
and conflicting cross-page overlap before a caller accepts raw bytes. Does not
replace the permissive producer in ``core/bar_export_loader.py``.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "core"))

from bar_export_loader import SIGNAL_PIPE_V2_RE  # noqa: E402
from lib.atomic_io import atomic_write_text  # noqa: E402

SCHEMA = "bar_export_v2_validation_v1"
STATUS_PASS = "PASS"
META_KEYS = (
    "ticker",
    "type",
    "quote_currency",
    "base_currency",
    "mintick",
    "pointvalue",
    "timezone",
    "timeframe",
)


@dataclass(frozen=True)
class ExpectedBarExportV2:
    price_column: str
    ticker: str
    instrument_type: str
    quote_currency: str
    base_currency: str
    mintick: Decimal
    pointvalue: Decimal
    timezone: str
    timeframe_minutes: int
    expected_unique_bars: int
    expected_first_open_utc: datetime
    expected_last_open_utc: datetime


@dataclass(frozen=True)
class BarExportValidationReceipt:
    schema: str
    status: str
    page_count: int
    input_sha256: tuple[str, ...]
    entry_row_count: int
    unique_bar_count: int
    identical_cross_page_overlap_count: int
    first_open_utc: datetime
    last_open_utc: datetime
    metadata: Mapping[str, str]


@dataclass(frozen=True)
class _DecodedEntry:
    trade_id: int
    epoch_ms: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    time_close_ms: int
    dow: str
    session: str
    ticker: str
    instrument_type: str
    quote_currency: str
    base_currency: str
    mintick: Decimal
    pointvalue: Decimal
    mintick_raw: str
    pointvalue_raw: str
    timezone: str
    timeframe_raw: str
    entry_price: Decimal
    page_index: int
    row_number: int


def _fail(page: int | None, row: int | None, field: str, reason: str) -> None:
    parts: list[str] = []
    if page is not None:
        parts.append(f"page={page}")
    if row is not None:
        parts.append(f"row={row}")
    parts.append(f"field={field}")
    raise ValueError(f"{' '.join(parts)}: {reason}")


def _require_positive_decimal(
    value: Decimal, *, page: int | None, row: int | None, field: str
) -> Decimal:
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        _fail(page, row, field, "must be a finite positive Decimal")
    return value


def _require_nonbool_positive_int(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"field={field}: must be a positive non-boolean int")
    return value


def _require_utc(dt: datetime, *, field: str) -> datetime:
    if not isinstance(dt, datetime) or dt.tzinfo is None:
        raise ValueError(f"field={field}: must be timezone-aware UTC")
    offset = dt.utcoffset()
    if offset is None or offset != timedelta(0):
        raise ValueError(f"field={field}: must have zero UTC offset")
    return dt


def _validate_expected(expected: ExpectedBarExportV2) -> None:
    for field in ("price_column", "ticker", "instrument_type", "quote_currency", "timezone"):
        val = getattr(expected, field)
        if not isinstance(val, str) or val == "":
            raise ValueError(f"field={field}: must be a nonempty string")
    if not isinstance(expected.base_currency, str):
        raise ValueError("field=base_currency: must be a string")
    _require_positive_decimal(expected.mintick, page=None, row=None, field="mintick")
    _require_positive_decimal(expected.pointvalue, page=None, row=None, field="pointvalue")
    _require_nonbool_positive_int(expected.timeframe_minutes, field="timeframe_minutes")
    _require_nonbool_positive_int(expected.expected_unique_bars, field="expected_unique_bars")
    first = _require_utc(expected.expected_first_open_utc, field="expected_first_open_utc")
    last = _require_utc(expected.expected_last_open_utc, field="expected_last_open_utc")
    if first > last:
        raise ValueError("field=expected_first_open_utc: must be <= expected_last_open_utc")


def _canonical_timeframe(minutes: int) -> str:
    return format(Decimal(minutes), "f")


def _file_identity(path: Path) -> tuple[int, int]:
    st = path.stat()
    return (st.st_dev, st.st_ino)


def _paths_alias(a: Path, b: Path) -> bool:
    try:
        return a.exists() and b.exists() and a.samefile(b)
    except OSError:
        return False


def _parse_decimal(raw: str, *, page: int, row: int, field: str) -> Decimal:
    try:
        value = Decimal(raw)
    except (InvalidOperation, ValueError):
        _fail(page, row, field, f"invalid decimal {raw!r}")
    if not value.is_finite():
        _fail(page, row, field, "non-finite decimal")
    return value


def _parse_int(raw: str, *, page: int, row: int, field: str) -> int:
    try:
        return int(raw)
    except ValueError:
        _fail(page, row, field, f"invalid integer {raw!r}")
        raise AssertionError


def _ohlc_ok(o: Decimal, h: Decimal, low: Decimal, c: Decimal) -> bool:
    return h >= low and h >= o and h >= c and low <= o and low <= c


def _choose_trade_header(headers: list[str], *, page: int) -> str:
    if "Trade #" in headers:
        return "Trade #"
    if "Trade number" in headers:
        return "Trade number"
    _fail(page, None, "Trade #", "missing Trade # / Trade number column")
    raise AssertionError


def _choose_signal_header(headers: list[str], *, page: int) -> str:
    if "Signal" in headers:
        return "Signal"
    if "Comment" in headers:
        return "Comment"
    _fail(page, None, "Signal", "missing Signal / Comment column")
    raise AssertionError


def _decode_page(
    page_index: int,
    path: Path,
    raw: bytes,
    *,
    price_column: str,
) -> tuple[str, list[_DecodedEntry]]:
    digest = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        _fail(page_index, None, "encoding", f"UTF-8 decode failed: {exc}")

    reader = csv.reader(io.StringIO(text))
    try:
        headers = next(reader)
    except StopIteration:
        _fail(page_index, None, "header", "empty page")

    headers = [h.strip() for h in headers]
    if len(headers) != len(set(headers)):
        _fail(page_index, None, "header", "duplicate headers")
    required = {"Type", "Date and time", price_column}
    missing = sorted(required - set(headers))
    if missing:
        _fail(page_index, None, "header", f"missing columns {missing}")

    trade_header = _choose_trade_header(headers, page=page_index)
    signal_header = _choose_signal_header(headers, page=page_index)
    width = len(headers)
    entries: list[_DecodedEntry] = []
    seen_trade_ids: set[int] = set()

    for row_number, cells in enumerate(reader, start=2):
        if len(cells) == 0 or all(c.strip() == "" for c in cells):
            continue
        if len(cells) != width:
            _fail(page_index, row_number, "width", f"expected {width} fields, got {len(cells)}")
        row = {headers[i]: cells[i] for i in range(width)}
        typ = row["Type"].strip()
        if not typ.startswith("Entry"):
            continue

        trade_raw = row[trade_header].strip()
        trade_id = _parse_int(trade_raw, page=page_index, row=row_number, field="Trade #")
        if trade_id <= 0:
            _fail(page_index, row_number, "Trade #", "must be a positive integer")
        if trade_id in seen_trade_ids:
            _fail(page_index, row_number, "Trade #", f"duplicate trade id {trade_id}")
        seen_trade_ids.add(trade_id)

        signal_text = row[signal_header].strip()
        match = SIGNAL_PIPE_V2_RE.fullmatch(signal_text)
        if match is None:
            _fail(
                page_index,
                row_number,
                signal_header,
                "Entry Signal must full-match v0.2 grammar",
            )

        epoch_ms = _parse_int(match.group("epoch"), page=page_index, row=row_number, field="epoch")
        time_close_ms = _parse_int(
            match.group("time_close"), page=page_index, row=row_number, field="time_close"
        )
        volume = _parse_int(match.group("v"), page=page_index, row=row_number, field="volume")
        if volume < 0:
            _fail(page_index, row_number, "volume", "must be nonnegative")

        o = _parse_decimal(match.group("o"), page=page_index, row=row_number, field="open")
        h = _parse_decimal(match.group("h"), page=page_index, row=row_number, field="high")
        low = _parse_decimal(match.group("l"), page=page_index, row=row_number, field="low")
        c = _parse_decimal(match.group("c"), page=page_index, row=row_number, field="close")
        for name, val in (("open", o), ("high", h), ("low", low), ("close", c)):
            if val <= 0:
                _fail(page_index, row_number, name, "must be finite and positive")
        if not _ohlc_ok(o, h, low, c):
            _fail(page_index, row_number, "OHLC", "invalid geometry")

        entry_price = _parse_decimal(
            row[price_column].strip(), page=page_index, row=row_number, field=price_column
        )
        if entry_price <= 0:
            _fail(page_index, row_number, price_column, "must be finite and positive")
        if entry_price != c:
            _fail(page_index, row_number, price_column, "Entry price must equal encoded close")

        mintick_raw = match.group("mintick")
        pointvalue_raw = match.group("pointvalue")
        mintick = _parse_decimal(mintick_raw, page=page_index, row=row_number, field="mintick")
        pointvalue = _parse_decimal(
            pointvalue_raw, page=page_index, row=row_number, field="pointvalue"
        )
        _require_positive_decimal(mintick, page=page_index, row=row_number, field="mintick")
        _require_positive_decimal(pointvalue, page=page_index, row=row_number, field="pointvalue")

        ticker = match.group("ticker")
        instrument_type = match.group("type")
        quote_currency = match.group("quote_ccy")
        base_currency = match.group("base_ccy")
        tz = match.group("tz")
        timeframe_raw = match.group("tf")
        for field, val, allow_empty in (
            ("ticker", ticker, False),
            ("type", instrument_type, False),
            ("quote_currency", quote_currency, False),
            ("base_currency", base_currency, True),
            ("timezone", tz, False),
            ("timeframe", timeframe_raw, False),
        ):
            if not allow_empty and val == "":
                _fail(page_index, row_number, field, "must be nonempty")

        entries.append(
            _DecodedEntry(
                trade_id=trade_id,
                epoch_ms=epoch_ms,
                open=o,
                high=h,
                low=low,
                close=c,
                volume=volume,
                time_close_ms=time_close_ms,
                dow=match.group("dow"),
                session=match.group("sess"),
                ticker=ticker,
                instrument_type=instrument_type,
                quote_currency=quote_currency,
                base_currency=base_currency,
                mintick=mintick,
                pointvalue=pointvalue,
                mintick_raw=mintick_raw,
                pointvalue_raw=pointvalue_raw,
                timezone=tz,
                timeframe_raw=timeframe_raw,
                entry_price=entry_price,
                page_index=page_index,
                row_number=row_number,
            )
        )

    if not entries:
        _fail(page_index, None, "Entry", "page has no Entry rows")

    entries_sorted = sorted(entries, key=lambda e: e.trade_id)
    prev_epoch: int | None = None
    for entry in entries_sorted:
        if prev_epoch is not None and entry.epoch_ms <= prev_epoch:
            _fail(
                page_index,
                entry.row_number,
                "epoch",
                "opens must strictly increase in numeric Trade # order",
            )
        prev_epoch = entry.epoch_ms

    epochs = [e.epoch_ms for e in entries_sorted]
    if len(epochs) != len(set(epochs)):
        _fail(page_index, None, "epoch", "duplicate timestamp within page")

    return digest, entries_sorted


def _payload_key(entry: _DecodedEntry) -> tuple:
    return (
        entry.epoch_ms,
        entry.open,
        entry.high,
        entry.low,
        entry.close,
        entry.volume,
        entry.time_close_ms,
        entry.dow,
        entry.session,
        entry.ticker,
        entry.instrument_type,
        entry.quote_currency,
        entry.base_currency,
        entry.mintick,
        entry.pointvalue,
        entry.timezone,
        entry.timeframe_raw,
        entry.entry_price,
    )


def _meta_from_entry(entry: _DecodedEntry) -> dict[str, str]:
    return {
        "ticker": entry.ticker,
        "type": entry.instrument_type,
        "quote_currency": entry.quote_currency,
        "base_currency": entry.base_currency,
        "mintick": entry.mintick_raw,
        "pointvalue": entry.pointvalue_raw,
        "timezone": entry.timezone,
        "timeframe": entry.timeframe_raw,
    }


def _meta_equal(a: dict[str, str], b: dict[str, str]) -> bool:
    if a.keys() != b.keys():
        return False
    for key in a:
        if key in ("mintick", "pointvalue"):
            if Decimal(a[key]) != Decimal(b[key]):
                return False
        elif a[key] != b[key]:
            return False
    return True


def validate_bar_export_v2(
    paths: Sequence[Path],
    *,
    expected: ExpectedBarExportV2,
) -> BarExportValidationReceipt:
    _validate_expected(expected)
    if not paths:
        raise ValueError("field=paths: at least one page is required")

    path_list = [Path(p) for p in paths]
    identities: list[tuple[int, int]] = []
    digests: list[str] = []
    all_entries: list[_DecodedEntry] = []

    for page_index, path in enumerate(path_list, start=1):
        raw = path.read_bytes()
        identity = _file_identity(path)
        if identity in identities:
            raise ValueError(f"field=paths: duplicate underlying input file at page={page_index}")
        identities.append(identity)
        digest, entries = _decode_page(
            page_index, path, raw, price_column=expected.price_column
        )
        digests.append(digest)
        all_entries.extend(entries)

    tf_ms = expected.timeframe_minutes * 60_000
    canonical_tf = _canonical_timeframe(expected.timeframe_minutes)
    first_meta: dict[str, str] | None = None

    for entry in all_entries:
        if not (entry.epoch_ms < entry.time_close_ms <= entry.epoch_ms + tf_ms):
            _fail(
                entry.page_index,
                entry.row_number,
                "time_close",
                "must satisfy epoch_ms < time_close_ms <= epoch_ms + timeframe",
            )
        meta = _meta_from_entry(entry)
        if first_meta is None:
            first_meta = meta
        elif not _meta_equal(first_meta, meta):
            _fail(entry.page_index, entry.row_number, "metadata", "metadata drift across entries")

    assert first_meta is not None

    exact_checks = [
        ("ticker", first_meta["ticker"], expected.ticker),
        ("type", first_meta["type"], expected.instrument_type),
        ("quote_currency", first_meta["quote_currency"], expected.quote_currency),
        ("base_currency", first_meta["base_currency"], expected.base_currency),
        ("timezone", first_meta["timezone"], expected.timezone),
        ("timeframe", first_meta["timeframe"], canonical_tf),
    ]
    for field, got, want in exact_checks:
        if got != want:
            raise ValueError(f"field={field}: expected {want!r}, got {got!r}")
    if Decimal(first_meta["mintick"]) != expected.mintick:
        raise ValueError(
            f"field=mintick: expected {expected.mintick!r}, got {first_meta['mintick']!r}"
        )
    if Decimal(first_meta["pointvalue"]) != expected.pointvalue:
        raise ValueError(
            f"field=pointvalue: expected {expected.pointvalue!r}, got {first_meta['pointvalue']!r}"
        )

    by_epoch: dict[int, list[_DecodedEntry]] = {}
    for entry in all_entries:
        by_epoch.setdefault(entry.epoch_ms, []).append(entry)

    for epoch, group in by_epoch.items():
        if len(group) > 1:
            first = group[0]
            first_payload = _payload_key(first)
            for other in group[1:]:
                if _payload_key(other) != first_payload:
                    _fail(
                        other.page_index,
                        other.row_number,
                        "overlap",
                        f"conflicting overlap at epoch={epoch}",
                    )

    unique_epochs = sorted(by_epoch.keys())
    unique_count = len(unique_epochs)
    entry_count = len(all_entries)
    overlap_count = entry_count - unique_count

    if unique_count != expected.expected_unique_bars:
        raise ValueError(
            f"field=expected_unique_bars: expected {expected.expected_unique_bars}, got {unique_count}"
        )
    first_open = datetime.fromtimestamp(unique_epochs[0] / 1000, tz=timezone.utc)
    last_open = datetime.fromtimestamp(unique_epochs[-1] / 1000, tz=timezone.utc)
    if first_open != expected.expected_first_open_utc:
        raise ValueError(
            "field=expected_first_open_utc: "
            f"expected {expected.expected_first_open_utc.isoformat()}, got {first_open.isoformat()}"
        )
    if last_open != expected.expected_last_open_utc:
        raise ValueError(
            "field=expected_last_open_utc: "
            f"expected {expected.expected_last_open_utc.isoformat()}, got {last_open.isoformat()}"
        )

    metadata = MappingProxyType({k: first_meta[k] for k in META_KEYS})
    return BarExportValidationReceipt(
        schema=SCHEMA,
        status=STATUS_PASS,
        page_count=len(path_list),
        input_sha256=tuple(digests),
        entry_row_count=entry_count,
        unique_bar_count=unique_count,
        identical_cross_page_overlap_count=overlap_count,
        first_open_utc=first_open,
        last_open_utc=last_open,
        metadata=metadata,
    )


def _dt_to_iso(dt: datetime) -> str:
    ms = int(dt.timestamp() * 1000)
    whole = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    frac = ms % 1000
    if frac:
        return whole.strftime("%Y-%m-%dT%H:%M:%S.") + f"{frac:03d}Z"
    return whole.strftime("%Y-%m-%dT%H:%M:%SZ")


def receipt_to_json_bytes(receipt: BarExportValidationReceipt) -> bytes:
    payload = {
        "entry_row_count": receipt.entry_row_count,
        "first_open_utc": _dt_to_iso(receipt.first_open_utc),
        "identical_cross_page_overlap_count": receipt.identical_cross_page_overlap_count,
        "input_sha256": list(receipt.input_sha256),
        "last_open_utc": _dt_to_iso(receipt.last_open_utc),
        "metadata": {k: receipt.metadata[k] for k in META_KEYS},
        "page_count": receipt.page_count,
        "schema": receipt.schema,
        "status": receipt.status,
        "unique_bar_count": receipt.unique_bar_count,
    }
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _parse_iso_utc(text: str) -> datetime:
    raw = text.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"invalid ISO UTC datetime: {text!r}") from exc
    return _require_utc(dt, field="datetime")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Strict opt-in BAR EXPORT v0.2 validator")
    p.add_argument("--in", dest="inputs", nargs="+", required=True, help="Raw v0.2 page CSV(s)")
    p.add_argument("--price-column", required=True)
    p.add_argument("--expected-ticker", required=True)
    p.add_argument("--expected-type", required=True)
    p.add_argument("--expected-quote-currency", required=True)
    p.add_argument("--expected-base-currency", required=True)
    p.add_argument("--expected-mintick", required=True)
    p.add_argument("--expected-pointvalue", required=True)
    p.add_argument("--expected-timeframe-minutes", required=True, type=int)
    p.add_argument("--expected-timezone", required=True)
    p.add_argument("--expected-unique-bars", required=True, type=int)
    p.add_argument("--expected-first-open-utc", required=True)
    p.add_argument("--expected-last-open-utc", required=True)
    p.add_argument("--receipt", default=None, help="Optional atomic JSON receipt path")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return 2 if code not in (0, None) else 0

    try:
        if isinstance(args.expected_timeframe_minutes, bool) or args.expected_timeframe_minutes <= 0:
            raise ValueError("field=expected_timeframe_minutes: must be a positive non-boolean int")
        if isinstance(args.expected_unique_bars, bool) or args.expected_unique_bars <= 0:
            raise ValueError("field=expected_unique_bars: must be a positive non-boolean int")
        expected = ExpectedBarExportV2(
            price_column=args.price_column,
            ticker=args.expected_ticker,
            instrument_type=args.expected_type,
            quote_currency=args.expected_quote_currency,
            base_currency=args.expected_base_currency,
            mintick=Decimal(args.expected_mintick),
            pointvalue=Decimal(args.expected_pointvalue),
            timezone=args.expected_timezone,
            timeframe_minutes=args.expected_timeframe_minutes,
            expected_unique_bars=args.expected_unique_bars,
            expected_first_open_utc=_parse_iso_utc(args.expected_first_open_utc),
            expected_last_open_utc=_parse_iso_utc(args.expected_last_open_utc),
        )
        paths = [Path(p) for p in args.inputs]
        receipt = validate_bar_export_v2(paths, expected=expected)
        payload = receipt_to_json_bytes(receipt)

        if args.receipt is not None:
            out = Path(args.receipt)
            for inp in paths:
                if _paths_alias(out, inp) or out.resolve() == inp.resolve():
                    raise ValueError("field=receipt: refuses path that aliases an input")
            atomic_write_text(out, payload.decode("utf-8"))

        sys.stdout.buffer.write(payload)
        return 0
    except (ValueError, OSError, InvalidOperation) as exc:
        print(f"validate_bar_export_v2: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
