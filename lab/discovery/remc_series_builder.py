"""Four-firm re-MC §8 step 2(b): daily P&L / intraday-low series builder.

Card: ``docs/briefs/handoffs/2026-10-05-four-firm-remc-series-builder-card.md``
(FROZEN for build, 2026-10-05). This module is the executable expression of that
card and nothing wider: it turns the six TradingView trade-list exports (#698 §7)
into the per-tier business-day series the survivor-scoring harness consumes.

Why a calendar of every weekday: ``prop_survivor_scoring.paired_blocks_from_daily``
takes consecutive business-day arrays and indexes them positionally against
``pd.bdate_range("2020-01-06", …)``, so a missing day would silently shift every
later block. The builder therefore emits one row per weekday inside its window,
zero-filled on no-trade days.

Rules implemented (card §0.5, frozen):
* **Inputs** — six ``LEG:MODE=PATH@SHA256`` tables. The SHA-256 of the file bytes
  is verified *before* any row is parsed; a mismatch raises.
* **Parsing** — TradingView's 17-column trade-list header (UTF-8 BOM tolerated);
  each trade number pairs one ``Entry …`` row with one ``Exit …`` row; an unpaired
  row raises. Trade-level ``Size (qty)``, ``Net PnL USD``, ``Commission USD`` and
  ``Adverse excursion USD`` are read from the Exit row, falling back to the Entry
  row only when the Exit cell is empty. Timestamps are naive wall times in the
  required ``export_tz`` (no default — a #616 freeze input) and are converted to
  America/New_York.
* **Session date** — the exit timestamp's NY date. A trade whose entry and exit
  fall on different NY dates raises, and so does any exit after 16:45 ET.
* **Quantities** — book quantities enter as data (``lab`` may not import ``ops``):
  Aegis is rescaled per contract to 8 (normal) / 3 (protected), Striker and ORB
  are used as exported, Vanguard protected is ``zero`` (no trades). A parity test
  under ``tests/`` asserts the spec against ``ops/c1_rail/book_policy.py``.
* **Window** — latest first session to the earliest last session across the six
  inputs; trades outside it are dropped.
* **Per day** — ``gross = Net PnL USD + Commission USD`` and ``sides = 2 x qty``
  per trade, summed over every leg in the mode; ``intraday_low`` is the
  conservative coincident sum ``-Σ|Adverse excursion USD| - day cost`` per tier.
* **Per tier** — ``pnl = gross - sides x FIRM_RULES[tier]["cost_per_side_usd"]``
  for the four frozen $100K tiers.
* **MFFU flag** — ``mffu_admissible`` is False when any in-window trade (either
  mode) exits at/after 16:10 ET, which is exactly the card's "interval
  ``(entry, exit]`` contains 16:10, or exit after 16:10" on a same-day trade.

Import contract: ``lab → core`` only (never ``ops``). Synthetic inputs only in
tests; the private exports are read at run time by the caller, never here.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Mapping, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import numpy as np

_REPO_ROOT = Path(__file__).resolve().parents[2]
# Direct-script bootstrap (the CLI is runnable as `python lab/discovery/…`);
# pytest already puts both roots on sys.path via [tool.pytest.ini_options].
for _bootstrap in (_REPO_ROOT, _REPO_ROOT / "core"):
    if str(_bootstrap) not in sys.path:
        sys.path.insert(0, str(_bootstrap))

try:  # dual-import: package path or flat PYTHONPATH=lab + core/
    from firm_rules import FIRM_RULES
except ImportError:  # pragma: no cover
    from core.firm_rules import FIRM_RULES

NY_TZ = ZoneInfo("America/New_York")

#: The four frozen $100K tiers (survivor-scoring pre-reg §3 cross-section).
TIERS: tuple[str, ...] = (
    "Bulenox_100K",
    "Tradeify_Select_100K",
    "MFFU_Rapid_100K",
    "BluSky_Premium_100K",
)
LEGS: tuple[str, ...] = ("aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7")
MODES: tuple[str, ...] = ("normal", "protected")

#: The (leg, mode) tables supplied as export files. The remaining two tables of
#: the 4x2 grid are derived: aegis protected from the aegis normal export at
#: target 3, and vanguard protected as ``zero`` (card §0.5 item 1).
FILE_TABLES: tuple[tuple[str, str], ...] = (
    ("aegis_6j", "normal"),
    ("dj30_mym_p250", "normal"),
    ("dj30_mym_p250", "protected"),
    ("vanguard_mgc", "normal"),
    ("orb_mnq_v7", "normal"),
    ("orb_mnq_v7", "protected"),
)
DERIVED_TABLES: tuple[tuple[str, str], ...] = tuple(
    (leg, mode) for leg in LEGS for mode in MODES if (leg, mode) not in FILE_TABLES
)

AS_EXPORTED = "as_exported"
ZERO = "zero"

#: Book quantities as data (card §0.5 item 1). Parity with
#: ``ops/c1_rail/book_policy.entry_quantities`` is asserted by
#: ``tests/test_remc_series_quantity_parity.py``; do not edit one without the other.
DEFAULT_QUANTITY_SPEC: dict[str, dict[str, object]] = {
    "aegis_6j": {"normal": 8, "protected": 3},
    "dj30_mym_p250": {"normal": AS_EXPORTED, "protected": AS_EXPORTED},
    "vanguard_mgc": {"normal": AS_EXPORTED, "protected": ZERO},
    "orb_mnq_v7": {"normal": AS_EXPORTED, "protected": AS_EXPORTED},
}

#: MFFU auto-liquidation (core/firm_rules.py MFFU row: 16:10 ET) and the venue
#: force-flat ceiling every leg is asserted against (card §0.5 item 2).
MFFU_LIQUIDATION_ET = time(16, 10)
LATE_EXIT_ET = time(16, 45)
#: CME trade dates roll at 18:00 ET, so adding six hours maps a NY time to its trade date.
CME_ROLL_OFFSET_HOURS = 6
#: Exits in [16:45, 18:00) ET are late; an exit at or after 18:00 opens the next trade date.
CME_REOPEN_ET = time(18, 0)

#: TradingView trade-list header, frozen by #698 §7 (17 columns, in order).
TRADE_LIST_COLUMNS: tuple[str, ...] = (
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
#: Trade-level columns read from the Exit row (Entry row is the empty-cell fallback).
TRADE_LEVEL_COLUMNS: tuple[str, ...] = (
    "Size (qty)",
    "Net PnL USD",
    "Commission USD",
    "Adverse excursion USD",
)
_TIMESTAMP_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}\Z")
_SHA256_RE = re.compile(r"[0-9a-fA-F]{64}\Z")

QuantityRule = object  # int/float target, or the strings AS_EXPORTED / ZERO


# ── errors ───────────────────────────────────────────────────────────────


class TradeListError(ValueError):
    """A trade-list export violates the frozen 17-column pairing schema."""


class InputIdentityError(ValueError):
    """An input file's bytes do not match the pinned SHA-256."""


class SessionBoundaryError(ValueError):
    """A trade spans two NY sessions or exits after the 16:45 ET cut."""


class QuantitySpecError(ValueError):
    """The per-leg quantity spec is not one of the frozen rule forms."""


class OutputPathError(RuntimeError):
    """The requested output directory is git-tracked or unignored inside the repo."""


#: Backwards-friendly alias — the card calls this a refusal, not an error string.
RefusedOutputPath = OutputPathError


# ── data model ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Trade:  # pylint: disable=too-many-instance-attributes
    """One paired trade, already converted to America/New_York."""

    leg: str
    trade_number: int
    entry_ny: datetime
    exit_ny: datetime
    qty: float
    net_usd: float
    commission_usd: float
    adverse_excursion_usd: float

    @property
    def session_date(self) -> date:
        """CME trade date of the exit: NY wall time rolled at 18:00 ET (card §0.5 item 3)."""
        return cme_trade_date(self.exit_ny)

    @property
    def gross_usd(self) -> float:
        """Net P&L plus commission (the pre-cost P&L the tier netting starts from)."""
        return self.net_usd + self.commission_usd

    @property
    def sides(self) -> float:
        """Traded sides: one entry and one exit per contract."""
        return 2.0 * self.qty

    def flags_mffu(self) -> bool:
        """The card's I-24 test, reduced for same-day trades to exit >= 16:10 ET.

        ``(entry, exit]`` contains 16:10 only when ``exit >= 16:10 > entry``; the
        second card clause catches every later exit regardless of entry, so the
        union is exactly ``exit >= 16:10``.
        """
        return MFFU_LIQUIDATION_ET <= self.exit_ny.time() < CME_REOPEN_ET


@dataclass
class SeriesBundle:
    """The built per-tier series plus everything the manifest records."""

    dates: list[date]
    window: tuple[date, date]
    #: tier -> {"normal_pnl" | "normal_low" | "protected_pnl" | "protected_low"}
    tiers: dict[str, dict[str, np.ndarray]] = field(default_factory=dict)
    #: mode -> {"gross" | "sides" | "adverse_excursion"} (cost-netting inputs)
    daily: dict[str, dict[str, np.ndarray]] = field(default_factory=dict)
    mffu_admissible: bool = True
    mffu_flagged_days: int = 0
    manifest: dict = field(default_factory=dict)


# ── scalar parsing ───────────────────────────────────────────────────────


def _number(raw: object, label: str) -> float:
    """Parse a trade-list cell as a finite float (accounting negatives allowed)."""
    if not isinstance(raw, str):
        raise TradeListError(f"{label} must be a string cell, got {raw!r}")
    text = raw.strip()
    if text.startswith("(") and text.endswith(")"):
        text = "-" + text[1:-1].strip()
    try:
        value = float(text)
    except ValueError as exc:
        raise TradeListError(f"{label} is not a number: {raw!r}") from exc
    if not math.isfinite(value):
        raise TradeListError(f"{label} must be finite, got {raw!r}")
    return value


def _positive_int(raw: object, label: str) -> int:
    value = _number(raw, label)
    if value <= 0 or value != int(value):
        raise TradeListError(f"{label} must be a positive integer, got {raw!r}")
    return int(value)


def _localize_unambiguous(naive: datetime, zone: ZoneInfo) -> datetime:
    """Attach ``zone`` only when the wall time names exactly one instant."""
    instants: dict[datetime, datetime] = {}
    for fold in (0, 1):
        localized = naive.replace(tzinfo=zone, fold=fold)
        round_trip = localized.astimezone(timezone.utc).astimezone(zone)
        if round_trip.replace(tzinfo=None) == naive:
            instants[localized.astimezone(timezone.utc)] = localized
    if len(instants) != 1:
        raise TradeListError(
            "Date and time is ambiguous or nonexistent in the export timezone: "
            f"{naive.strftime('%Y-%m-%d %H:%M')}"
        )
    return next(iter(instants.values()))


def _parse_timestamp(raw: object, label: str, zone: ZoneInfo) -> datetime:
    if not isinstance(raw, str) or not _TIMESTAMP_RE.fullmatch(raw.strip()):
        raise TradeListError(
            f"{label} must match %Y-%m-%d %H:%M exactly (TV trade list), got {raw!r}"
        )
    naive = datetime.strptime(raw.strip(), "%Y-%m-%d %H:%M")
    return _localize_unambiguous(naive, zone).astimezone(NY_TZ)


def _as_zone(export_tz: str) -> ZoneInfo:
    try:
        return ZoneInfo(export_tz)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"export_tz is not a valid IANA timezone: {export_tz!r}") from exc


def _event_kind(raw: object) -> str:
    if not isinstance(raw, str):
        raise TradeListError(f"Type must be a string, got {raw!r}")
    normalized = " ".join(raw.strip().lower().split())
    if normalized.startswith("entry"):
        return "entry"
    if normalized.startswith("exit"):
        return "exit"
    raise TradeListError(f"Type must start with 'Entry' or 'Exit', got {raw!r}")


# ── input identity ───────────────────────────────────────────────────────


def sha256_file(path: str | Path) -> str:
    """Byte-stream SHA-256 of a file."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sha256(path: str | Path, expected_sha256: str) -> str:
    """Raise before any parsing when the file bytes do not match the pin."""
    observed = sha256_file(path)
    if observed != expected_sha256.strip().lower():
        raise InputIdentityError(
            f"{Path(path).name}: SHA-256 mismatch — expected {expected_sha256}, "
            f"observed {observed}"
        )
    return observed


# ── trade-list parsing ───────────────────────────────────────────────────


def parse_trade_list_csv(
    path: str | Path, *, leg: str, export_tz: str
) -> list[Trade]:
    """Parse one TradingView trade-list export into paired NY-localized trades.

    Raises ``TradeListError`` for a foreign header, a short row, an unpaired
    trade number or a duplicated Entry/Exit row, and ``SessionBoundaryError`` for
    a trade that spans two NY sessions or exits after 16:45 ET.
    """
    source = Path(path)
    zone = _as_zone(export_tz)
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.reader(handle) if row]
    if not rows:
        raise TradeListError(f"{source.name}: trade list has no header row")
    header = [cell.strip() for cell in rows[0]]
    if tuple(header) != TRADE_LIST_COLUMNS:
        missing = [c for c in TRADE_LIST_COLUMNS if c not in header]
        raise TradeListError(
            f"{source.name}: header is not the frozen 17-column TV trade list"
            + (f" (missing {missing})" if missing else "")
            + f"; got {header}"
        )

    paired: dict[int, dict[str, dict[str, str]]] = {}
    for line_number, row in enumerate(rows[1:], start=2):
        if not any(cell.strip() for cell in row):
            continue
        if len(row) != len(TRADE_LIST_COLUMNS):
            raise TradeListError(
                f"{source.name} line {line_number}: {len(row)} fields, "
                f"expected {len(TRADE_LIST_COLUMNS)}"
            )
        values = dict(zip(TRADE_LIST_COLUMNS, row))
        number = _positive_int(values["Trade number"], f"{source.name} Trade number")
        kind = _event_kind(values["Type"])
        slot = paired.setdefault(number, {})
        if kind in slot:
            raise TradeListError(
                f"{source.name}: trade {number} has more than one {kind.title()} row"
            )
        slot[kind] = values

    trades: list[Trade] = []
    for number in sorted(paired):
        slot = paired[number]
        absent = [kind for kind in ("entry", "exit") if kind not in slot]
        if absent:
            raise TradeListError(
                f"{source.name}: trade {number} has no {'/'.join(absent)} row"
            )
        trades.append(_trade_from_pair(leg, number, slot["entry"], slot["exit"], zone))
    return trades


def _cell(exit_row: Mapping[str, str], entry_row: Mapping[str, str], column: str) -> str:
    """Trade-level values live on the Exit row; empty cells fall back to Entry."""
    raw = (exit_row.get(column) or "").strip()
    if raw:
        return raw
    return (entry_row.get(column) or "").strip()


def _trade_from_pair(
    leg: str,
    number: int,
    entry_row: Mapping[str, str],
    exit_row: Mapping[str, str],
    zone: ZoneInfo,
) -> Trade:
    entry_ny = _parse_timestamp(entry_row["Date and time"], "Entry Date and time", zone)
    exit_ny = _parse_timestamp(exit_row["Date and time"], "Exit Date and time", zone)
    qty = _number(_cell(exit_row, entry_row, "Size (qty)"), f"trade {number} Size (qty)")
    net = _number(_cell(exit_row, entry_row, "Net PnL USD"), f"trade {number} Net PnL USD")
    commission = _number(
        _cell(exit_row, entry_row, "Commission USD"), f"trade {number} Commission USD"
    )
    adverse = _number(
        _cell(exit_row, entry_row, "Adverse excursion USD"),
        f"trade {number} Adverse excursion USD",
    )
    if qty <= 0:
        raise TradeListError(f"trade {number}: Size (qty) must be positive, got {qty!r}")
    trade = Trade(
        leg=leg,
        trade_number=number,
        entry_ny=entry_ny,
        exit_ny=exit_ny,
        qty=qty,
        net_usd=net,
        commission_usd=commission,
        adverse_excursion_usd=adverse,
    )
    _assert_session_containment(trade)
    return trade


def cme_trade_date(moment_ny: datetime) -> date:
    """CME Globex trade date: a NY time at or after 18:00 belongs to the next day."""
    return (moment_ny + timedelta(hours=CME_ROLL_OFFSET_HOURS)).date()


def _assert_session_containment(trade: Trade) -> None:
    if cme_trade_date(trade.entry_ny) != cme_trade_date(trade.exit_ny):
        raise SessionBoundaryError(
            f"{trade.leg} trade {trade.trade_number}: entry {trade.entry_ny.isoformat()} "
            f"and exit {trade.exit_ny.isoformat()} fall on different CME trade dates "
            "(18:00 ET roll); the venue-bound editions are flat each session"
        )
    if LATE_EXIT_ET <= trade.exit_ny.time() < CME_REOPEN_ET:
        raise SessionBoundaryError(
            f"{trade.leg} trade {trade.trade_number}: exit {trade.exit_ny.isoformat()} "
            f"is after {LATE_EXIT_ET.strftime('%H:%M')} ET — the export does not match "
            "the venue-bound editions (INSUFFICIENT per card §0.5 item 2)"
        )


def load_trade_table(
    path: str | Path, expected_sha256: str, *, leg: str, export_tz: str
) -> list[Trade]:
    """Verify the pinned SHA-256 first, then parse the trade list."""
    verify_sha256(path, expected_sha256)
    return parse_trade_list_csv(path, leg=leg, export_tz=export_tz)


# ── quantity spec ────────────────────────────────────────────────────────


def normalize_quantity_spec(spec: object) -> dict[str, dict[str, object]]:
    """Validate the per-leg quantity spec; returns a JSON-safe copy."""
    if not isinstance(spec, Mapping):
        raise QuantitySpecError("quantity spec must be a JSON object keyed by leg")
    unexpected = sorted(set(spec) - set(LEGS))
    if unexpected:
        raise QuantitySpecError(f"quantity spec has unknown legs: {unexpected}")
    normalized: dict[str, dict[str, object]] = {}
    for leg in LEGS:
        row = spec.get(leg)
        if not isinstance(row, Mapping):
            raise QuantitySpecError(f"quantity spec leg {leg!r} must be an object")
        normalized[leg] = {}
        for mode in MODES:
            if mode not in row:
                raise QuantitySpecError(
                    f"quantity spec leg {leg!r} is missing mode {mode!r}"
                )
            rule = row[mode]
            if isinstance(rule, bool):
                raise QuantitySpecError(f"{leg}.{mode}: booleans are not a quantity rule")
            if isinstance(rule, str):
                if rule not in (AS_EXPORTED, ZERO):
                    raise QuantitySpecError(
                        f"{leg}.{mode}: unknown string rule {rule!r}; "
                        f"expected {AS_EXPORTED!r} or {ZERO!r}"
                    )
            elif isinstance(rule, (int, float)):
                if not math.isfinite(float(rule)) or float(rule) <= 0:
                    raise QuantitySpecError(
                        f"{leg}.{mode}: a rescale target must be positive and finite"
                    )
            else:
                raise QuantitySpecError(
                    f"{leg}.{mode}: rule must be a number, {AS_EXPORTED!r} or {ZERO!r}"
                )
            normalized[leg][mode] = rule
    return normalized


def load_quantity_spec(path: str | Path) -> dict[str, dict[str, object]]:
    """Load and validate a quantity-spec JSON file."""
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except OSError as exc:
        raise QuantitySpecError(f"cannot read quantity spec: {source}") from exc
    except json.JSONDecodeError as exc:
        raise QuantitySpecError(f"quantity spec is not valid JSON: {source}") from exc
    return normalize_quantity_spec(payload)


def rescale_per_contract(trade: Trade, target: float) -> Trade:
    """Rescale one trade's money columns per contract to ``target`` contracts."""
    if trade.qty <= 0:
        raise QuantitySpecError(
            f"{trade.leg} trade {trade.trade_number}: cannot rescale a non-positive "
            f"quantity {trade.qty!r}"
        )
    factor = float(target) / trade.qty
    return Trade(
        leg=trade.leg,
        trade_number=trade.trade_number,
        entry_ny=trade.entry_ny,
        exit_ny=trade.exit_ny,
        qty=float(target),
        net_usd=trade.net_usd * factor,
        commission_usd=trade.commission_usd * factor,
        adverse_excursion_usd=trade.adverse_excursion_usd * factor,
    )


def apply_quantity_rule(
    trades: Sequence[Trade], rule: object, *, leg: str, mode: str
) -> list[Trade]:
    """Apply one spec cell: ``zero`` drops every trade, a number rescales, else as-is."""
    if rule == ZERO:
        return []
    if rule == AS_EXPORTED:
        return list(trades)
    if isinstance(rule, bool) or not isinstance(rule, (int, float)):
        raise QuantitySpecError(
            f"{leg}.{mode}: rule must be a number, {AS_EXPORTED!r} or {ZERO!r}; got {rule!r}"
        )
    target = float(rule)
    if not math.isfinite(target) or target <= 0:
        raise QuantitySpecError(f"{leg}.{mode}: rescale target must be positive")
    return [rescale_per_contract(trade, target) for trade in trades]


# ── series construction ──────────────────────────────────────────────────


def _weekday_calendar(start: date, end: date) -> list[date]:
    """Every Monday–Friday date in [start, end] inclusive (positional calendar)."""
    if start > end:
        raise ValueError(f"empty window: first session {start} is after last session {end}")
    days: list[date] = []
    current = start
    while current <= end:
        if current.weekday() < 5:
            days.append(current)
        current += timedelta(days=1)
    return days


def _window(tables: Mapping[tuple[str, str], Sequence[Trade]]) -> tuple[date, date]:
    """Latest first session to the earliest last session across the input tables."""
    firsts: list[date] = []
    lasts: list[date] = []
    for (leg, mode), trades in tables.items():
        if not trades:
            continue
        firsts.append(min(t.session_date for t in trades))
        lasts.append(max(t.session_date for t in trades))
    if not firsts:
        raise ValueError("no input table has a trade; the window is undefined")
    start, end = max(firsts), min(lasts)
    if start > end:
        raise ValueError(
            f"input tables do not overlap: latest first session {start} is after the "
            f"earliest last session {end}"
        )
    return start, end


def _cost_per_side(tier: str) -> float:
    try:
        raw = FIRM_RULES[tier]["cost_per_side_usd"]
    except KeyError as exc:
        raise ValueError(f"tier {tier!r} has no cost_per_side_usd in FIRM_RULES") from exc
    return float(raw)


def build_series(
    tables: Mapping[tuple[str, str], Sequence[Trade]],
    *,
    export_tz: str,
    quantity_spec: Mapping[str, Mapping[str, object]] | None = None,
    input_hashes: Mapping[tuple[str, str], str] | None = None,
) -> SeriesBundle:
    """Build the per-tier weekday series from the parsed (leg, mode) trade tables.

    ``tables`` holds the input tables keyed by ``(leg, mode)``. Every cell of the
    4x2 leg/mode grid must be resolvable: a supplied table is used directly, and a
    missing one is derived from that leg's ``normal`` table by applying its spec
    rule (which is how aegis protected and vanguard protected exist at all).
    """
    _as_zone(export_tz)  # fail fast on a bad tz string
    spec = normalize_quantity_spec(
        DEFAULT_QUANTITY_SPEC if quantity_spec is None else quantity_spec
    )
    for key in tables:
        leg, mode = key
        if leg not in LEGS or mode not in MODES:
            raise ValueError(f"unknown (leg, mode) table key: {leg}:{mode}")
    # Fail closed on the source set: exactly the six file-backed tables. Only the
    # designated DERIVED_TABLES are built from a normal table; nothing substitutes.
    missing = [":".join(key) for key in FILE_TABLES if key not in tables]
    if missing:
        raise ValueError(f"missing required input tables: {missing}")
    supplied_derived = [":".join(key) for key in DERIVED_TABLES if key in tables]
    if supplied_derived:
        raise ValueError(
            f"tables {supplied_derived} are derived by rule and must not be supplied"
        )

    start, end = _window(tables)
    dates = _weekday_calendar(start, end)
    index = {day: position for position, day in enumerate(dates)}

    resolved: dict[tuple[str, str], list[Trade]] = {}
    for leg in LEGS:
        for mode in MODES:
            key = (leg, mode)
            if key in tables:
                source = list(tables[key])
            else:  # a DERIVED_TABLES cell; its normal table is required above
                source = list(tables[(leg, "normal")])
            in_window = [
                trade for trade in source if start <= trade.session_date <= end
            ]
            resolved[key] = apply_quantity_rule(
                in_window, spec[leg][mode], leg=leg, mode=mode
            )

    daily: dict[str, dict[str, np.ndarray]] = {}
    for mode in MODES:
        gross = np.zeros(len(dates), dtype=float)
        sides = np.zeros(len(dates), dtype=float)
        adverse = np.zeros(len(dates), dtype=float)
        for leg in LEGS:
            for trade in resolved[(leg, mode)]:
                position = index[trade.session_date]
                gross[position] += trade.gross_usd
                sides[position] += trade.sides
                adverse[position] += abs(trade.adverse_excursion_usd)
        daily[mode] = {"gross": gross, "sides": sides, "adverse_excursion": adverse}

    tiers: dict[str, dict[str, np.ndarray]] = {}
    for tier in TIERS:
        cost_per_side = _cost_per_side(tier)
        channels: dict[str, np.ndarray] = {}
        for mode in MODES:
            cost = daily[mode]["sides"] * cost_per_side
            pnl = daily[mode]["gross"] - cost
            # 0.0 - x keeps a no-trade day at exactly +0.0 (never -0.0).
            low = 0.0 - daily[mode]["adverse_excursion"] - cost
            for label, series in ((f"{mode}_pnl", pnl), (f"{mode}_low", low)):
                if not np.isfinite(series).all():
                    raise ValueError(f"{tier} {label} is not finite")
            if np.any(low > 0.0):
                raise ValueError(
                    f"{tier} {mode}_low must be <= 0 (intraday excursion sign)"
                )
            channels[f"{mode}_pnl"] = pnl
            channels[f"{mode}_low"] = low
        tiers[tier] = channels

    flagged_days = {
        trade.session_date
        for mode in MODES
        for leg in LEGS
        for trade in resolved[(leg, mode)]
        if trade.flags_mffu()
    }
    pinned = dict(input_hashes or {})
    manifest = {
        "export_tz": str(export_tz),
        "window": {"start": start.isoformat(), "end": end.isoformat()},
        "n_days": len(dates),
        "quantity_spec": {leg: dict(spec[leg]) for leg in LEGS},
        "inputs": {
            f"{leg}:{mode}": {
                "sha256": pinned.get((leg, mode), pinned.get((leg, "normal"))),
                "derived": (leg, mode) not in tables,
                "trades": len(resolved[(leg, mode)]),
            }
            for leg in LEGS
            for mode in MODES
        },
        "tiers": {tier: {"cost_per_side_usd": _cost_per_side(tier)} for tier in TIERS},
        "mffu_admissible": not flagged_days,
        "mffu_flagged_days": len(flagged_days),
        "columns": {
            mode: {
                "gross": [float(v) for v in daily[mode]["gross"]],
                "sides": [float(v) for v in daily[mode]["sides"]],
                "adverse_excursion": [float(v) for v in daily[mode]["adverse_excursion"]],
            }
            for mode in MODES
        },
    }
    return SeriesBundle(
        dates=dates,
        window=(start, end),
        tiers=tiers,
        daily=daily,
        mffu_admissible=not flagged_days,
        mffu_flagged_days=len(flagged_days),
        manifest=manifest,
    )


# ── outputs ──────────────────────────────────────────────────────────────

SERIES_COLUMNS = ("date", "normal_pnl", "normal_low", "protected_pnl", "protected_low")


def _format_value(value: float) -> str:
    return repr(float(value))


def write_bundle(bundle: SeriesBundle, out_dir: str | Path) -> Path:
    """Write one CSV per tier plus ``manifest.json`` (with output SHA-256s)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, dict[str, object]] = {}
    for tier, channels in bundle.tiers.items():
        target = out / f"{tier}.csv"
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(SERIES_COLUMNS)
            for position, day in enumerate(bundle.dates):
                writer.writerow(
                    [day.isoformat()]
                    + [
                        _format_value(channels[f"{mode}_{channel}"][position])
                        for mode in MODES
                        for channel in ("pnl", "low")
                    ]
                )
        outputs[target.name] = {"sha256": sha256_file(target)}
    manifest = dict(bundle.manifest)
    manifest["outputs"] = outputs
    manifest_path = out / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest_path


# ── output-path guard ────────────────────────────────────────────────────


def _git(args: Sequence[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False
    )


def assert_out_dir_allowed(out: str | Path, *, repo_root: Path | None = None) -> None:
    """Refuse an output directory that git tracks, or that sits unignored in the repo.

    Outside the repository anything goes; inside it the directory must be
    git-ignored (the private output root is), and never tracked.
    """
    root = (repo_root or _REPO_ROOT).resolve()
    top = _git(["rev-parse", "--show-toplevel"], root)
    if top.returncode != 0:
        return  # not a git work tree: nothing tracked to collide with
    toplevel = Path(top.stdout.strip()).resolve()
    target = Path(out).resolve()
    if target != toplevel and toplevel not in target.parents:
        return  # outside this repository
    tracked = _git(["ls-files", "--error-unmatch", str(target)], toplevel)
    if tracked.returncode == 0:
        raise OutputPathError(
            f"output directory {target} is tracked by git; the series builder writes "
            "only to an untracked, git-ignored output root"
        )
    ignored = _git(["check-ignore", "-q", str(target)], toplevel)
    if ignored.returncode != 0:
        raise OutputPathError(
            f"output directory {target} is inside the repository and not git-ignored; "
            "refusing (card §5: outputs go to a gitignored private root)"
        )


# ── CLI ──────────────────────────────────────────────────────────────────


def parse_input_token(token: str) -> tuple[str, str, Path, str]:
    """Split ``LEG:MODE=PATH@SHA256``; the path may hold a Windows drive colon."""
    leg_mode, separator, path_at_sha = token.partition("=")
    if not separator:
        raise ValueError(f"--input must be LEG:MODE=PATH@SHA256, got {token!r}")
    leg, separator, mode = leg_mode.partition(":")
    if not separator:
        raise ValueError(f"--input must be LEG:MODE=PATH@SHA256, got {token!r}")
    path_text, separator, sha = path_at_sha.rpartition("@")
    if not separator or not path_text:
        raise ValueError(f"--input must be LEG:MODE=PATH@SHA256, got {token!r}")
    if leg not in LEGS:
        raise ValueError(f"unknown leg {leg!r}; known: {list(LEGS)}")
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode!r}; known: {list(MODES)}")
    if not _SHA256_RE.fullmatch(sha):
        raise ValueError(f"--input SHA-256 must be 64 hex characters, got {sha!r}")
    return leg, mode, Path(path_text), sha.lower()


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: six pinned inputs in, per-tier weekday CSVs + manifest out."""
    parser = argparse.ArgumentParser(
        description=(
            "Four-firm re-MC daily series builder (card 2026-10-05). Reads the six "
            "pinned TradingView trade-list exports and writes one weekday series CSV "
            "per firm tier plus manifest.json. Synthetic or private inputs only."
        )
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        metavar="LEG:MODE=PATH@SHA256",
        help="one pinned trade-list export; repeat for the six file-backed tables",
    )
    parser.add_argument(
        "--quantity-spec",
        default=None,
        metavar="JSON",
        help="path to the per-leg quantity spec JSON (default: the frozen book spec)",
    )
    parser.add_argument(
        "--export-tz",
        required=True,
        metavar="IANA_TZ",
        help="timezone the export timestamps are naive wall times in (#616 freeze input)",
    )
    parser.add_argument("--out", required=True, metavar="DIR", help="output directory")
    args = parser.parse_args(list(argv) if argv is not None else None)

    out_dir = Path(args.out)
    # Refuse an unsafe destination before any input byte is read or hashed.
    assert_out_dir_allowed(out_dir)

    spec = (
        DEFAULT_QUANTITY_SPEC
        if args.quantity_spec is None
        else load_quantity_spec(args.quantity_spec)
    )
    tables: dict[tuple[str, str], list[Trade]] = {}
    hashes: dict[tuple[str, str], str] = {}
    for token in args.input:
        leg, mode, path, sha = parse_input_token(token)
        key = (leg, mode)
        if key in tables:
            raise ValueError(f"--input {leg}:{mode} supplied more than once")
        if key not in FILE_TABLES:
            raise ValueError(
                f"--input {leg}:{mode} is not one of the six file-backed tables "
                f"{[':'.join(k) for k in FILE_TABLES]}"
            )
        tables[key] = load_trade_table(path, sha, leg=leg, export_tz=args.export_tz)
        hashes[key] = sha

    missing = [":".join(key) for key in FILE_TABLES if key not in tables]
    if missing:
        raise ValueError(f"missing required input tables: {missing}")

    bundle = build_series(
        tables, export_tz=args.export_tz, quantity_spec=spec, input_hashes=hashes
    )
    manifest_path = write_bundle(bundle, out_dir)
    print(
        f"[remc-series-builder] window {bundle.window[0]}..{bundle.window[1]} "
        f"({len(bundle.dates)} weekdays) tiers={len(bundle.tiers)} "
        f"mffu_admissible={bundle.mffu_admissible} "
        f"mffu_flagged_days={bundle.mffu_flagged_days} -> {manifest_path}"
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    try:
        raise SystemExit(main())
    except OutputPathError as error:
        print(f"remc-series-builder: refused: {error}", file=sys.stderr)
        raise SystemExit(2) from None


__all__ = [
    "AS_EXPORTED",
    "DEFAULT_QUANTITY_SPEC",
    "DERIVED_TABLES",
    "FILE_TABLES",
    "InputIdentityError",
    "LEGS",
    "MODES",
    "MFFU_LIQUIDATION_ET",
    "LATE_EXIT_ET",
    "OutputPathError",
    "RefusedOutputPath",
    "SERIES_COLUMNS",
    "SeriesBundle",
    "TIERS",
    "TRADE_LIST_COLUMNS",
    "Trade",
    "TradeListError",
    "QuantitySpecError",
    "SessionBoundaryError",
    "apply_quantity_rule",
    "assert_out_dir_allowed",
    "build_series",
    "cme_trade_date",
    "load_quantity_spec",
    "load_trade_table",
    "main",
    "normalize_quantity_spec",
    "parse_input_token",
    "parse_trade_list_csv",
    "rescale_per_contract",
    "sha256_file",
    "verify_sha256",
    "write_bundle",
    "ZERO",
]
