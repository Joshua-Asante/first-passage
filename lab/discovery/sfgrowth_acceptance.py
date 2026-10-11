"""Pool-independent Q-SFGROWTH-1 primitives, exercised only on synthetic inputs.

Contract: PR #752 b02c173e, §§B–D and F2–F9. This is not a real-data runner:
no active pool, manifest, K registration, archive transport or scoring CLI is
provided. F8 reconciliation and F9 margin integration remain prerequisites.
"""
from __future__ import annotations

import csv
import hashlib
import io
import itertools
import json
import math
import re
import tempfile
from dataclasses import dataclass
from datetime import timedelta
from fractions import Fraction
from pathlib import Path

import numpy as np

from discovery.remc_series_builder import Trade, TradeListError, parse_trade_list_csv


class Void(ValueError):
    """Input integrity failure; must precede all payoff verdicts."""


MULTIPLIERS = (Fraction(0), Fraction(1, 8), Fraction(1, 4), Fraction(1, 2),
               Fraction(1), Fraction(2))
BINDINGS = ('pine_sha256', 'reference_evidence_sha256', 'classification_sha256',
            'preregistration_sha256')


def _finite(value):
    if isinstance(value, bool) or not isinstance(value, (int, float, np.number)):
        raise Void('expected finite number')
    if not math.isfinite(value):
        raise Void('nonfinite number')
    return float(value)


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _hex(value, length):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{%d}' % length, value) is not None


def strict_object(raw):
    """Exact UTF-8 object; no BOM, duplicate keys or non-JSON numbers."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Void('duplicate JSON key')
            result[key] = value
        return result
    def invalid_constant(value):
        raise Void('non-JSON constant: ' + value)
    try:
        result = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                            parse_constant=invalid_constant)
    except (ValueError, UnicodeError, AttributeError) as exc:
        raise Void('invalid JSON object') from exc
    if not isinstance(result, dict):
        raise Void('expected JSON object')
    return result


def resolve_manifest(raw_reference, retrieve, *, local_bytes=None):
    """Resolve immutable F6 identity through an injected archive transport.

    The transport must retrieve the exact (repository, commit, path), raising
    OSError/KeyError for unavailable evidence. Tests use an in-memory archive.
    """
    ref = strict_object(raw_reference)
    keys = {'schema_version', 'archive_repository', 'archive_commit',
            'archive_path', 'manifest_sha256'}
    if set(ref) != keys or type(ref['schema_version']) is not int or ref['schema_version'] != 1:
        raise Void('reference schema')
    sha = ref['manifest_sha256']
    if (ref['archive_repository'] != 'Joshua-Asante/first-passage-archive'
            or not _hex(ref['archive_commit'], 40) or not _hex(sha, 64)
            or ref['archive_path'] != f'evidence/sha256/{sha[:2]}/{sha}'):
        raise Void('reference identity')
    try:
        blob = retrieve(ref['archive_repository'], ref['archive_commit'], ref['archive_path'])
    except (OSError, KeyError) as exc:
        raise Void('archive unavailable') from exc
    if not isinstance(blob, bytes) or _digest(blob) != sha:
        raise Void('archive hash mismatch')
    if local_bytes is not None and local_bytes != blob:
        raise Void('local manifest differs from committed blob')
    return blob


def _slot(value):
    """A slot is a non-empty JSON array (or tuple) of strings and non-boolean integers."""
    if (not isinstance(value, (list, tuple)) or not value
            or any(isinstance(item, bool) or not isinstance(item, (str, int)) for item in value)):
        raise Void('slot container')
    return tuple(value)


def validate_slots(rows, expected, retrieve):
    """Check exact inventory/bytes against independently admitted slot bindings.

    Does not admit a pool or certify the contents of an export/zero artifact.
    The caller must then validate each artifact's type-specific contents.
    """
    if not isinstance(rows, (list, tuple)):
        raise Void('slot rows')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'slot', 'kind', 'sha256', *BINDINGS}:
            raise Void('slot schema')
        slot = _slot(row['slot'])
        if slot in seen or slot not in expected:
            raise Void('duplicate or unadmitted slot')
        seen.add(slot)
        binding = expected[slot]
        if set(binding) != {'kind', *BINDINGS}:
            raise Void('admitted binding schema')
        if any(not _hex(binding[key], 64) for key in BINDINGS):
            raise Void('admitted source digest')
        if any(row[key] != value for key, value in binding.items()):
            raise Void('source, freeze or kind mismatch')
        try:
            raw = retrieve(slot)
        except (OSError, KeyError) as exc:
            raise Void('artifact unavailable') from exc
        if not isinstance(raw, bytes) or not _hex(row['sha256'], 64) or _digest(raw) != row['sha256']:
            raise Void('artifact hash mismatch')
    if seen != set(expected):
        raise Void('incomplete slot inventory')


@dataclass(frozen=True)
class ExportTrade:
    """Paired parser trade plus captured favorable excursion (not regenerated)."""
    trade: Trade
    favorable: float


def read_export(path, *, expected_sha256, leg, export_tz, baseline):
    """Reuse the pinned CSV parser, supplementing its missing favorable channel.

    Both reads use the one hashed byte snapshot, never ``path`` again: the
    path-only parser gets a private temporary copy of those bytes.
    """
    try:
        raw = path.read_bytes()
        if _digest(raw) != expected_sha256:
            raise Void('export hash mismatch')
        with tempfile.TemporaryDirectory() as private:
            snapshot = Path(private) / path.name
            snapshot.write_bytes(raw)
            trades = parse_trade_list_csv(snapshot, leg=leg, export_tz=export_tz)
        rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline='')))
        favorable = {}
        for row in rows:
            if row['Type'].strip().lower().startswith('exit'):
                value = float(row['Favorable excursion USD'])
                favorable[int(row['Trade number'])] = abs(_finite(value))
        if baseline and not trades:
            raise Void('empty baseline export')
        return tuple(ExportTrade(trade, favorable[trade.trade_number]) for trade in trades)
    except (OSError, ValueError, KeyError, TypeError, TradeListError) as exc:
        raise Void('invalid export') from exc


def validate_settings(reference, actual):
    """Match captured non-sizing settings; no defaults or cosmetic exemptions.

    Both mappings contain only non-sizing settings. Source/admission provenance
    is checked separately by validate_slots; F8 must bind the final inventory.
    """
    required = {'Pyramiding', 'commission', 'slippage'}
    if not required <= set(reference) or set(reference) != set(actual):
        raise Void('missing or unexpected captured setting')
    if any(value is None for value in reference.values()):
        raise Void('unknown required reference')
    if any(type(value) is not type(actual[key]) or value != actual[key]
           for key, value in reference.items()):
        raise Void('unauthorized non-sizing setting change')


def daily_series(trades, calendar, fees, cost):
    """F9 fee-only accounting; parser.gross_usd already adds commission once."""
    if set(fees) != {'commission', 'exchange', 'clearing', 'NFA'}:
        raise Void('incomplete all-in fee')
    rates = [_finite(value) for value in fees.values()]
    if any(value < 0 for value in rates) or cost not in (1, 1.5):
        raise Void('invalid fee or cost multiple')
    rate = sum(rates)
    result = np.zeros((len(calendar), 3))
    positions = {day: i for i, day in enumerate(calendar)}
    for captured in trades:
        trade = captured.trade
        if trade.session_date not in positions:
            continue
        fee = cost * trade.sides * rate
        result[positions[trade.session_date]] += (
            trade.gross_usd - fee, -abs(trade.adverse_excursion_usd) - fee,
            abs(captured.favorable))
    return result


def explore_quantity(trades, calendar):
    days = set(calendar)
    return sum(item.trade.qty for item in trades if item.trade.session_date in days)


def common_calendar(baseline_ranges):
    if not baseline_ranges or any(not pair or len(pair) != 2 for pair in baseline_ranges):
        raise Void('missing baseline endpoints')
    start = max(pair[0] for pair in baseline_ranges)
    end = min(pair[1] for pair in baseline_ranges)
    if start > end:
        raise Void('empty common calendar')
    return tuple(start + timedelta(days=i) for i in range((end-start).days + 1)
                 if (start + timedelta(days=i)).weekday() < 5)


def split_calendar(calendar):
    cut = 2 * len(calendar) // 3
    if min(cut, len(calendar) - cut) < 20:
        raise Void('window shorter than 20 weekdays')
    return calendar[:cut], calendar[cut:]


def bootstrap_indices(window_length):
    if type(window_length) is not int or window_length < 20:
        raise Void('window shorter than 20 weekdays')
    draws = []
    for seed in (42, 123, 2026):
        starts = np.random.default_rng(seed).integers(0, window_length - 20 + 1,
                                                    size=(10000, 13))
        draws.append((starts[:, :, None] + np.arange(20)).reshape(10000, 260)[:, :252])
    result = np.array(draws)
    result.flags.writeable = False
    return result


# §C money is fixed-point at 1e-6 USD: each input is rounded half-even onto that
# grid once, so path arithmetic is exact integer arithmetic and the inclusive halt
# (peak − trough)/peak ≥ 0.15 is tested exactly as 20·(peak − trough) ≥ 3·peak.
MICROS = 10**6
MAX_USD = 10**8  # per input; keeps 252-day sums ×20 inside int64


def _micros(values):
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all() or np.any(np.abs(values) >= MAX_USD):
        raise Void('money outside fixed-point range')
    return np.rint(values * MICROS).astype(np.int64)


def _initial_micros(initial_equity):
    equity = int(_micros(_finite(initial_equity)))
    if equity <= 0:
        raise Void('nonpositive initial equity')
    return equity


def _halted(peak, trough):
    return 20 * (peak - trough) >= 3 * peak


def path_terminal(days, initial_equity):
    equity = peak = _initial_micros(initial_equity)
    for d, low, high in _micros(days).tolist():
        peak = max(peak, equity + high)
        trough = equity + low
        if _halted(peak, trough):
            return trough / MICROS, True
        equity += d
        peak = max(peak, equity)
    return equity / MICROS, False


@dataclass(frozen=True)
class Summary:
    growth: float
    hits: tuple[int, int, int]

    @property
    def clears(self):
        return all(hit <= 100 for hit in self.hits)


def summarize(terminals, hits):
    terminals, hits = np.asarray(terminals), np.asarray(hits)
    if terminals.shape != (3, 10000) or hits.shape != (3, 10000):
        raise Void('expected three seeds of 10000 paths')
    if not np.isfinite(terminals).all() or hits.dtype != bool:
        raise Void('invalid path outcomes')
    return Summary(float(np.median(terminals)), tuple(int(n) for n in hits.sum(axis=1)))


def score(days, initial_equity, draws):
    """Score synthetic arrays using caller-shared immutable bootstrap draws."""
    days = np.asarray(days, dtype=float)
    if days.ndim != 2 or days.shape[1] != 3 or not np.isfinite(days).all():
        raise Void('invalid daily channels')
    if np.any(days[:, 1] > 0) or np.any(days[:, 2] < 0):
        raise Void('invalid excursion signs')
    if (draws.shape != (3, 10000, 252) or not np.issubdtype(draws.dtype, np.integer)
            or draws.min() < 0 or draws.max() >= len(days)):
        raise Void('invalid shared draws')
    days = _micros(days)
    equity = np.full((3, 10000), _initial_micros(initial_equity), dtype=np.int64)
    peak = equity.copy()
    hits = np.zeros((3, 10000), dtype=bool)
    for t in range(252):
        d, low, high = np.moveaxis(days[draws[:, :, t]], -1, 0)
        active = ~hits
        intraday_peak = np.maximum(peak, equity + high)
        trough = equity + low
        hit = active & _halted(intraday_peak, trough)
        equity = np.where(hit, trough, np.where(active, equity + d, equity))
        peak = np.where(active, np.maximum(intraday_peak, equity), peak)
        hits |= hit
    return summarize(equity / MICROS, hits)


@dataclass(frozen=True)
class Candidate:
    vector: tuple
    result: Summary
    quantity: float
    excluded: bool = False


def nominal_grid(legs, *, forbidden_pairs):
    if not legs or len(set(legs)) != len(legs):
        raise Void('invalid nominal dimensions')
    try:
        pairs = [(legs.index(a), legs.index(b)) for a, b in forbidden_pairs]
    except ValueError as exc:
        raise Void('unknown excluded dimension') from exc
    return tuple(vector for vector in itertools.product(MULTIPLIERS, repeat=len(legs))
                 if any(vector) and not any(vector[a] and vector[b] for a, b in pairs))


def rank(candidates, initial_equity):
    eligible = [c for c in candidates if not c.excluded and c.result.clears
                and c.result.growth > initial_equity]
    return sorted(eligible, key=lambda c: (-c.result.growth, sum(c.result.hits),
                                          c.quantity, c.vector))


def verdict(candidates, initial_equity, confirm, *, input_error=None):
    """VOID first; Confirm callback sees only the top nominal Explore vector."""
    if input_error is not None:
        return 'VOID'
    ranked = rank(candidates, initial_equity)
    if not ranked:
        return 'FALSIFIED'
    top = ranked[0].vector
    try:
        base = confirm(top, 1, False)
        stress = confirm(top, 1.5, False)
        seam = confirm(top, 1, True)
    except Void:
        return 'VOID'
    if (base.clears and stress.clears and seam.clears
            and base.growth > initial_equity and stress.growth > initial_equity):
        return 'RESOLVED'
    return 'AMBIGUOUS-HOLD'


def outside_roll_seams(dates, roll_dates):
    excluded = set()
    for roll in roll_dates:
        if roll.weekday() >= 5:
            raise Void('roll date is not a weekday')
        excluded.add(roll)
        for direction in (-1, 1):
            day = roll
            count = 0
            while count < 10:
                day += timedelta(days=direction)
                if day.weekday() < 5:
                    excluded.add(day)
                    count += 1
    return tuple(day for day in dates if day not in excluded)


def validate_evidence(expected_hashes, retrieve):
    """Recheck every required source against independently frozen hashes."""
    for name, sha in expected_hashes.items():
        try:
            raw = retrieve(name)
        except (OSError, KeyError) as exc:
            raise Void('required evidence unavailable') from exc
        if not _hex(sha, 64) or not isinstance(raw, bytes) or _digest(raw) != sha:
            raise Void('source/freeze evidence mismatch')


def validate_zero_schema(raw):
    """Inspect the historical F2 schema, without admitting it to any pool.

    F8 excludes every historical eligible slot. This routine intentionally grants
    no eligibility and produces no daily contribution or replacement export.
    """
    obj = strict_object(raw)
    keys = {'schema_version', 'artifact_type', 'leg', 'multiplier', 'input_id',
            'reason', *BINDINGS}
    if set(obj) != keys:
        raise Void('zero artifact keys')
    if (type(obj['schema_version']) is not int or obj['schema_version'] != 1
            or obj['artifact_type'] != 'ZERO_BY_INTEGER_SIZING'
            or type(obj['leg']) is not int
            or obj['reason'] != 'FLOORED_COUNT_BELOW_INPUT_MIN'
            or any(not _hex(obj[key], 64) for key in BINDINGS)):
        raise Void('zero artifact schema')
    historical = {(3, '1/8', 'maxContracts'), (3, '1/4', 'maxContracts'),
                  (4, '1/8', 'qty'), (4, '1/4', 'qty'), (4, '1/2', 'qty')}
    if any(not isinstance(obj[key], str) for key in ('multiplier', 'input_id')):
        raise Void('zero artifact slot types')
    if (obj['leg'], obj['multiplier'], obj['input_id']) not in historical:
        raise Void('not a historical F2 slot')
    return obj


def require_zero_slot(obj, *, eligible_slots):
    """Separate frozen eligibility check; schema validity is never admission."""
    if (obj['leg'], obj['multiplier']) not in eligible_slots:
        raise Void('zero slot not admitted')
