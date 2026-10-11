"""Q-SFGROWTH-1 F9: conservative concurrent-contract margin accounting.

This pure lab primitive consumes a complete, already admitted fill ledger, starting
and ending flat over the full calendar. It does not parse exports or admit evidence.
Each entry/add has a distinct tranche ID; partial exits name their entry tranche.
A paired trade row becomes one entry and one exit, never two copies of the pair.
Disjoint closed portions of one entry may instead be separate tranches, provided
the adapter allocates each contract exactly once and retains its entry timestamp.

The independent expected-fill inventory must come from upstream reconciliation,
not be inferred from the possibly incomplete ledger passed here. Snapshot dates,
artifact hashes, pool admission, baseline nonemptiness and Properties provenance
remain the caller's admission obligations. Empty admitted nonbaseline legs are
explicit empty sequences (including their inventory), never missing values.
"""
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
from typing import Literal


Number = int | float | Decimal


@dataclass(frozen=True)
class MarginFill:
    """Unsigned contracts; timestamps must be timezone-aware, IDs leg-local."""

    fill_id: str
    tranche_id: str
    timestamp: datetime
    kind: Literal['entry', 'exit']
    quantity: Number


@dataclass(frozen=True)
class MarginResult:
    status: Literal['PASS', 'EXCLUDED', 'VOID']
    peak_quantity_by_leg: dict[str, int] | None
    required_margin: Fraction | None
    reason: str | None = None


def _positive_number(value: Number) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError('expected a finite positive number')
    # Exact decimal arithmetic prevents rounding a just-over-limit requirement down.
    result = Fraction(str(value))
    if result <= 0:
        raise ValueError('expected a finite positive number')
    return result


def _identity(value: str) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _sequence(value: object) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes))


def _leg_peak(rows: Sequence[MarginFill], expected: Sequence[str]) -> int:
    if not _sequence(rows) or not _sequence(expected):
        raise ValueError('missing or invalid fill ledger/inventory')
    if any(not _identity(identity) for identity in expected):
        raise ValueError('invalid expected fill ID')
    if len(set(expected)) != len(expected):
        raise ValueError('duplicate expected fill ID')
    seen: set[str] = set()
    events = []
    for row in rows:
        if not isinstance(row, MarginFill):
            raise ValueError('invalid fill')
        if not _identity(row.fill_id) or not _identity(row.tranche_id):
            raise ValueError('missing fill/tranche ID')
        if row.fill_id in seen:
            raise ValueError('duplicate fill ID')
        seen.add(row.fill_id)
        if row.kind not in ('entry', 'exit'):
            raise ValueError('invalid fill kind')
        stamp = row.timestamp
        if not isinstance(stamp, datetime) or stamp.utcoffset() is None:
            raise ValueError('missing/invalid timestamp or timezone')
        quantity = _positive_number(row.quantity)
        if quantity.denominator != 1:
            raise ValueError('noninteger contract quantity')
        events.append((stamp.astimezone(timezone.utc), row.kind != 'entry',
                       row.fill_id, row.tranche_id, int(quantity)))
    if seen != set(expected):
        raise ValueError('fill inventory mismatch (missing or unexpected fill)')

    balances: dict[str, int] = {}
    total = peak = 0
    # All entries precede all exits at the same instant, including zero-duration
    # tranches. Fill ID only stabilizes ordering within those two groups.
    for _, is_exit, _, tranche, quantity in sorted(events):
        if not is_exit:
            if tranche in balances:
                raise ValueError('repeated entry tranche; use a distinct ID for each add')
            balances[tranche] = quantity
            total += quantity
            peak = max(peak, total)
        else:
            if tranche not in balances or quantity > balances[tranche]:
                raise ValueError('exit before entry, unmatched exit or over-exit')
            balances[tranche] -= quantity
            total -= quantity
    if any(balances.values()):
        raise ValueError('incomplete accounting: unclosed tranche')
    return peak


def check_concurrent_margin(
    fills_by_leg: Mapping[str, Sequence[MarginFill]],
    *,
    initial_margin_by_leg: Mapping[str, Number],
    equity_limit: Number,
    expected_fill_ids_by_leg: Mapping[str, Sequence[str]],
) -> MarginResult:
    """Return PASS, EXCLUDED (> limit), or VOID, with no partial result on VOID.

    F9 uses SUM OF PER-LEG PEAKS times initial margins, even if different legs
    peak at different times. Long/short quantities are unsigned and never netted.
    Invalid/missing ledgers, identities, inventory, timestamps, quantities,
    pairing, margins or limit return VOID before any margin verdict. Each ledger
    must finish flat. Exact equality to the limit passes this margin check only.
    This function does not alter nominal vectors, K or ranking quantities.
    """
    try:
        mappings = (fills_by_leg, initial_margin_by_leg, expected_fill_ids_by_leg)
        if any(not isinstance(value, Mapping) for value in mappings):
            raise ValueError('missing/invalid leg mapping')
        if not fills_by_leg or any(not _identity(leg) for leg in fills_by_leg):
            raise ValueError('missing/invalid legs')
        if not (set(fills_by_leg) == set(initial_margin_by_leg) == set(expected_fill_ids_by_leg)):
            raise ValueError('ledger, inventory and margin leg sets must match')
        limit = _positive_number(equity_limit)
        peaks = {}
        required = Fraction(0)
        for leg, rows in fills_by_leg.items():
            margin = _positive_number(initial_margin_by_leg[leg])
            peaks[leg] = _leg_peak(rows, expected_fill_ids_by_leg[leg])
            required += peaks[leg] * margin
    except (ValueError, TypeError, OverflowError) as exc:
        return MarginResult('VOID', None, None, str(exc))
    return MarginResult('EXCLUDED' if required > limit else 'PASS', peaks, required)
