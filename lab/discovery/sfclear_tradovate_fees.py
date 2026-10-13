"""Closed Q-SFCLEAR-2 card C scoring snapshot; reference replay costs stay separate.

JSON uses ``schema: sfclear_tradovate_fees/v1`` and a ``rows`` list of objects
with ``instrument`` plus the four decimal-string components. Both expected
digests come from the caller's frozen record: ``expected_sha256`` identifies
the exact serialized bytes, ``expected_source_sha256`` the retained capture.
No private capture is opened here, and there is no runtime age limit.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, DecimalException


_INSTRUMENTS = frozenset({'6J', 'MYM', 'MGC', 'MNQ'})
_COMPONENTS = ('commission', 'exchange', 'clearing', 'NFA')
_FIELDS = {'schema', 'venue', 'plan', 'unit', 'captured_utc', 'source_sha256', 'rows'}
_DECIMAL = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z')


def _digest(value):
    if type(value) is not str or re.fullmatch(r'[0-9a-fA-F]{64}', value) is None:
        raise ValueError('expected 64-hex SHA256 digest')
    return value.lower()


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def _constant(value):
    raise ValueError('non-JSON number: ' + value)


def _rate(value):
    if type(value) is not str or _DECIMAL.fullmatch(value) is None:
        raise ValueError('fee must be a decimal string')
    try:
        decimal = Decimal(value)
        if not decimal.is_finite() or decimal < 0:
            raise ValueError('fee must be finite and nonnegative')
        rate = float(decimal)
    except (DecimalException, OverflowError) as exc:
        raise ValueError('fee cannot be represented for scoring') from exc
    if not math.isfinite(rate) or (decimal > 0 and rate == 0):
        raise ValueError('fee cannot be represented for scoring')
    return rate


@dataclass(frozen=True)
class FeeSnapshot:
    """Parsed identity and immutable per-side rates, with defensive lookups."""

    snapshot_sha256: str
    source_sha256: str
    captured_utc: datetime
    _rows: tuple[tuple[str, tuple[float, ...]], ...]

    def rates_for(self, instrument: str) -> dict[str, float]:
        """Return one leg's component mapping for ``daily_series``."""
        for symbol, rates in self._rows:
            if instrument == symbol:
                return dict(zip(_COMPONENTS, rates))
        raise ValueError('unsupported fee instrument')


def parse_snapshot(raw: bytes, *, expected_sha256: str,
                   expected_source_sha256: str) -> FeeSnapshot:
    """Refuse swapped bytes, open schemas, incomplete rows and invalid rates.

    Values already use USD per side per contract: conversion to float happens
    once here, with no division, instrument-specific rule or age test.
    """
    expected = _digest(expected_sha256)
    source = _digest(expected_source_sha256)
    if type(raw) is not bytes or hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('snapshot SHA256 mismatch')
    try:
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=_object,
                         parse_constant=_constant)
    except (ValueError, UnicodeError) as exc:
        raise ValueError('invalid snapshot JSON') from exc
    if type(doc) is not dict or set(doc) != _FIELDS:
        raise ValueError('closed snapshot fields required')
    if (doc['schema'] != 'sfclear_tradovate_fees/v1'
            or doc['venue'] != 'Tradovate' or doc['plan'] != 'Free'
            or doc['unit'] != 'USD_per_side_per_contract'):
        raise ValueError('unsupported schema, venue, plan or per-side unit')
    if _digest(doc['source_sha256']) != source:
        raise ValueError('source SHA256 mismatch')
    try:
        captured = datetime.fromisoformat(doc['captured_utc'])
    except (TypeError, ValueError) as exc:
        raise ValueError('captured_utc must be aware ISO datetime') from exc
    if captured.utcoffset() is None:
        raise ValueError('captured_utc must be aware ISO datetime')
    rows = doc['rows']
    if type(rows) is not list or len(rows) != len(_INSTRUMENTS):
        raise ValueError('exact four-instrument rows required')
    parsed = {}
    for row in rows:
        if type(row) is not dict or set(row) != {'instrument', *_COMPONENTS}:
            raise ValueError('closed instrument/component row required')
        instrument = row['instrument']
        if (type(instrument) is not str or instrument not in _INSTRUMENTS
                or instrument in parsed):
            raise ValueError('each supported instrument must occur exactly once')
        parsed[instrument] = tuple(_rate(row[key]) for key in _COMPONENTS)
    return FeeSnapshot(expected, source, captured, tuple(sorted(parsed.items())))
