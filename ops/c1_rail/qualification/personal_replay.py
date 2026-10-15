"""Verified, chronological Q-SFCLEAR-2 PR replay. No private-state inspection.

Manifest v1 carries independent expected digests in ``inputs`` (role -> path,
sha256) and four PR routes. The source bundle v1 carries dated sessions of
synchronous 15-minute bars (utc, legs -> contract month and OHLC), a retained
Striker risk-dollar input, and explicit missing-active-bar exclusions. Schedule
splits are forbidden. Reference friction v1 carries the four Instrument mappings.
Neither a callback nor adapter construction precedes complete input validation.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from bisect import bisect_right
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from types import MappingProxyType

from c1_rail.book_policy import PersonalP0Policy, account_micro_cap, validate_size_vector
from c1_signal_daemon.feed import Bar
from .contract import canonical_json_bytes
from .model import LEG_IDS, ET, SourceBar, SourceSession, SessionSchedule, PathBar, PathSession
from .bracket import BracketScheduleQuotes
from .production_source import _json
from .replay import BookReplay, Instrument, ReplayNeedsContext, RouteBroker

TUPLE_SHA256 = '62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f'
SCHEDULE_SHA256 = 'ab44fada0c059c0d286798239a87c82331d8500ef075bf4cb1180ed552d5d473'
ROLL_SHA256 = '72677d254045fd35ca3da7047c8b649f47d0ae283d3fc41a402467de8de4134c'
SYMBOLS = dict(zip(LEG_IDS, ('6J', 'MYM', 'MGC', 'MNQ')))
INPUT_ROLES = frozenset(('tuple', 'size_vector', 'source_bundle', 'schedule', 'roll_list',
                         'generator', 'calendar', 'reference_friction', 'e0'))
TRADE_FIELDS = frozenset(('leg', 'instrument', 'contract', 'entry_utc', 'exit_utc', 'side',
    'quantity', 'tranche_index', 'entry_price', 'initial_stop_level', 'delta_0', 'exit_price',
    'exit_kind', 'stop_fill_distance_b', 'net_pnl_usd', 'commission_usd', 'mae_usd', 'mfe_usd'))


def _closed(doc, fields, label):
    if type(doc) is not dict or set(doc) != set(fields):
        raise ValueError(label + ' requires exact fields')


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _digest(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        raise ValueError('invalid identity digest')
    return value


def _utc(value):
    if type(value) is not str:
        raise ValueError('UTC timestamp required')
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.utcoffset() != timedelta(0):
        raise ValueError('timezone-aware UTC timestamp required')
    return result.astimezone(timezone.utc)


def _finite(value, *, positive=False):
    if type(value) not in (int, float) or not math.isfinite(value) or (positive and value <= 0):
        raise ValueError('finite numeric value required')
    return value


def _tuple(raw, size_raw):
    doc = _json(raw)
    strings = ('study', 'rung', 'status', 'protection', 'lifecycle_tier', 'striker_risk_basis',
               'size_vector_hash_rule', 'size_vector_sha256', 'prescreen_SHA256SUMS_sha256', 'nonce')
    _closed(doc, ('schema', *strings, 'paper_initial_capital', 'book_legs', 'sizing',
                 'capital_anchor', 'cap_source', 'rule_max_contracts', 'derived_from', 'ruling'), 'tuple')
    if doc['schema'] != 'q-sfclear-1-sizing-tuple/v1' or any(type(doc[k]) is not str or not doc[k] for k in strings):
        raise ValueError('tuple schema/scalars')
    if doc['protection'] != 'P0' or doc['lifecycle_tier'] != 'AUTHORIZED' or doc['rung'] != 'R1':
        raise ValueError('tuple must bind R1/P0/AUTHORIZED')
    if type(doc['book_legs']) is not list or len(doc['book_legs']) != 4 or set(doc['book_legs']) != set(LEG_IDS):
        raise ValueError('tuple requires exactly four legs')
    if type(doc['paper_initial_capital']) is not int or doc['paper_initial_capital'] <= 0:
        raise ValueError('tuple paper capital')
    sizing = validate_size_vector(doc['sizing'])
    if any(sizing.leg(k).adds.value != 'OFF' for k in ('dj30_mym_p250', 'vanguard_mgc')) or sizing.leg('orb_mnq_v7').base != 0:
        raise ValueError('R1 requires adds OFF and ORB OFF')
    _digest(doc['size_vector_sha256'])
    if _sha(canonical_json_bytes(doc['sizing'])) != doc['size_vector_sha256'] or _sha(canonical_json_bytes(_json(size_raw))) != doc['size_vector_sha256']:
        raise ValueError('size vector identity differs')
    _closed(doc['capital_anchor'], ('file', 'file_sha256', 'symbol'), 'capital anchor')
    if any(type(v) is not str or not v for v in doc['capital_anchor'].values()):
        raise ValueError('capital anchor strings required')
    _digest(doc['capital_anchor']['file_sha256'])
    _closed(doc['cap_source'], ('code_source', 'ruling', 'shared_account_cap_micro_equivalents',
                              'request_cap_micro_equivalents_each_leg'), 'cap source')
    for key in ('shared_account_cap_micro_equivalents', 'request_cap_micro_equivalents_each_leg'):
        if type(doc['cap_source'][key]) is not int or doc['cap_source'][key] != account_micro_cap('Personal_Tradovate'):
            raise ValueError('resolved instance cap differs')
    _closed(doc['rule_max_contracts'], (*LEG_IDS, 'book_micro_equivalents'), 'rule max')
    if any(type(v) is not int or v < 0 for v in doc['rule_max_contracts'].values()):
        raise ValueError('rule max integer required')
    for key, keys in [('derived_from', ('R0_size_vector_sha256', 'change_from_R0', 'r3d_startup_policy_sha256')),
                      ('ruling', ('D4', 'date', 'source', 'text'))]:
        _closed(doc[key], keys, key)
        if any(type(v) is not str or not v for v in doc[key].values()):
            raise ValueError('tuple provenance strings required')
    return doc, sizing


def parse_historical_schedule(raw):
    doc = _json(raw)
    _closed(doc, ('header', 'sessions'), 'schedule')
    if doc['header']['schema'] != 'sfclear_historical_schedule/v1':
        raise ValueError('historical schedule schema')
    rows = {}
    for row in doc['sessions']:
        day = date.fromisoformat(row['account_date'])
        if day in rows:
            raise ValueError('duplicate schedule day')
        if row['permission'] == 'PERMITTED':
            keys = ('opens', 'risk_add_cutoff', 'flatten_start', 'own_flat_deadline')
            fields = {'account_date', 'permission', *(k+s for k in keys for s in ('_local', '_utc'))}
            if not fields <= set(row) <= fields | {'d19_status'}:
                raise ValueError('permitted row requires exact fields')
            values = [_utc(row[k+'_utc']) for k in keys]
            for instant, expected in zip(values[1:], (time(15,45), time(15,55), time(16))):
                if instant.astimezone(ET).date() != day or instant.astimezone(ET).time() != expected:
                    raise ValueError('historical schedule G0 boundary differs')
            schedule = SessionSchedule(*values[1:])
        elif row['permission'] == 'DENIED':
            # Frozen denial rows have no executable times. These inert clock
            # boundaries let adapters retain chronology while admission refuses.
            if not {'account_date', 'permission', 'denial_reason'} <= set(row) <= {'account_date', 'permission', 'denial_reason', 'd19_status'}:
                raise ValueError('denied row fields')
            schedule = SessionSchedule(*(datetime.combine(day, t, ET).astimezone(timezone.utc)
                                          for t in (time(15,45), time(15,55), time(16))))
        else:
            raise ValueError('unknown schedule permission')
        rows[day] = (row['permission'], schedule)
    if not rows or list(rows) != sorted(rows):
        raise ValueError('ordered nonempty schedule required')
    return rows


def parse_roll_dates(raw):
    doc = _json(raw)
    _closed(doc, ('header', 'contracts', 'seams'), 'roll list')
    if doc['header']['schema'] != 'sfclear_roll_dates/v1':
        raise ValueError('roll list schema')
    result = {}
    for row in doc['contracts']:
        required = {'product', 'contract_month', 'g4_start_open_utc', 'g4_start_open_local',
                    'g4_start_trade_date', 'last_trade', 'on_seam_cycle'}
        if not required <= set(row) <= required | {'first_notice'}:
            raise ValueError('roll contract fields')
        key = (row['product'], row['contract_month'])
        if key[0] not in ('6J', 'MGC') or key in result or re.fullmatch(r'\d{4}-\d{2}', key[1]) is None:
            raise ValueError('roll contract identity')
        result[key] = _utc(row['g4_start_open_utc'])
    for row in doc['seams']:
        key = (row['product'], row['to_month'])
        if key[0] in ('6J', 'MGC'):
            if type(key[1]) is not str or re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', key[1]) is None:
                raise ValueError('roll seam contract identity')
            result.setdefault(key, None)
    return result


@dataclass(frozen=True, repr=False)
class VerifiedInputs:
    """Internal receipt created only after verification; sensitive bytes never repr'd."""
    retained: object = field(repr=False)
    identities: object
    sizing: object
    initial_equity: float = field(repr=False)
    paper_capital: int = field(repr=False)
    request_cap: int
    schedules: object
    rolls: object
    instruments: object
    path: tuple
    contracts: object
    contract_index: object
    splits: object
    striker_risk: float = field(repr=False)

    def risk_refusal(self, leg, instant, *, contract=None):
        local = instant.astimezone(ET)
        day = local.date() + timedelta(days=int(local.hour >= 18))
        permission, schedule = self.schedules[day]
        if permission != 'PERMITTED':
            return 'DENIED schedule row'
        contract = self.contract_at(leg, instant) if contract is None else contract
        boundary = self.rolls.get((SYMBOLS[leg], contract))
        if boundary is not None and instant >= boundary:
            return 'G4 contract boundary'
        if instant >= schedule.cutoff:
            return 'scheduled entry cutoff'
        return None

    def contract_at(self, leg, instant):
        # Contract labels are retained facts, never inferred from price jumps.
        times, labels = self.contract_index.get(leg, ((), ()))
        index = bisect_right(times, instant) - 1
        if index < 0:
            raise ValueError('missing contract fact')
        return labels[index]


def _index_contracts(contracts):
    """Build immutable per-leg chronology once, outside the replay hot path."""
    grouped = {leg: [] for leg in LEG_IDS}
    for (leg, instant), label in contracts.items():
        grouped[leg].append((instant, label))
    result = {}
    for leg, facts in grouped.items():
        facts.sort()
        result[leg] = (tuple(instant for instant, _ in facts), tuple(label for _, label in facts))
    return MappingProxyType(result)


def _freeze(value):
    if type(value) is dict:
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if type(value) is list:
        return tuple(_freeze(item) for item in value)
    return value


def verify_inputs(manifest):
    _closed(manifest, ('schema', 'routes', 'inputs'), 'run manifest')
    if manifest['schema'] != 'sfclear_replay_manifest/v1' or manifest['routes'] != dict.fromkeys(LEG_IDS, 'PR'):
        raise ValueError('all four routes must be PR')
    _closed(manifest['inputs'], INPUT_ROLES, 'input identities')
    retained, identities, paths = {}, {}, set()
    pins = {'tuple': TUPLE_SHA256, 'schedule': SCHEDULE_SHA256, 'roll_list': ROLL_SHA256}
    for role, row in manifest['inputs'].items():
        _closed(row, ('path', 'sha256'), 'input identity')
        expected = _digest(row['sha256'])
        if role in pins and expected != pins[role]:
            raise ValueError('frozen input identity differs')
        path = Path(row['path']).resolve()
        if path in paths:
            raise ValueError('input identity path alias')
        paths.add(path)
        try:
            raw = path.read_bytes()
        except OSError:
            raise ValueError('input identity unavailable') from None
        if _sha(raw) != expected:
            raise ValueError('input identity mismatch: '+role)
        retained[role], identities[role] = raw, expected
    return _verify_retained(retained, identities)


def _verify_retained(retained, identities):
    """Pure replay of validation from the same immutable bytes; never reopen."""
    _closed(retained, INPUT_ROLES, 'retained inputs')
    _closed(identities, INPUT_ROLES, 'retained identities')
    pins = {'tuple': TUPLE_SHA256, 'schedule': SCHEDULE_SHA256, 'roll_list': ROLL_SHA256}
    for role, raw in retained.items():
        expected = _digest(identities[role])
        if type(raw) is not bytes or _sha(raw) != expected or (role in pins and expected != pins[role]):
            raise ValueError('retained input identity differs')
    doc, sizing = _tuple(retained['tuple'], retained['size_vector'])
    if identities['e0'] != doc['capital_anchor']['file_sha256']:
        raise ValueError('E_0 identity differs from verified tuple')
    raw = retained['e0']
    if re.fullmatch(rb'[0-9]+\n', raw) is None:
        raise ValueError('invalid E_0 encoding')
    try:
        number = int(raw)
        equity = float(number)
    except (ValueError, OverflowError):
        raise ValueError('invalid E_0 value') from None
    if not math.isfinite(equity) or equity <= 0:
        raise ValueError('invalid E_0 value')
    if int(equity) != number:
        raise ValueError('E_0 cannot be represented exactly by the replay')
    schedules = parse_historical_schedule(retained['schedule'])
    rolls = parse_roll_dates(retained['roll_list'])
    friction = _json(retained['reference_friction'])
    _closed(friction, ('schema', 'instruments'), 'reference friction')
    if friction['schema'] != 'sfclear_reference_friction/v1':
        raise ValueError('reference friction schema')
    _closed(friction['instruments'], LEG_IDS, 'friction legs')
    instruments = {leg: Instrument(**row) for leg, row in friction['instruments'].items()}
    source = _json(retained['source_bundle'])
    _closed(source, ('schema', 'sessions', 'striker_risk_dollars', 'splits', 'data_exclusions'), 'source bundle')
    if source['schema'] != 'sfclear_source_bundle/v1':
        raise ValueError('source bundle schema')
    risk = _finite(source['striker_risk_dollars'], positive=True)
    if source['splits'] != []:
        raise ValueError('source splits must be empty for R1 bracket placement')
    splits = {}
    if type(source['data_exclusions']) is not list:
        raise ValueError('data exclusions must be a list')
    exclusions = set()
    for row in source['data_exclusions']:
        _closed(row, ('account_date', 'leg', 'reason'), 'data exclusion')
        day = date.fromisoformat(row['account_date'])
        key = (day, row['leg'])
        if (row['leg'] not in LEG_IDS or row['reason'] != 'missing_active_bar'
                or key in exclusions or day not in schedules or schedules[day][0] != 'PERMITTED'):
            raise ValueError('invalid data exclusion')
        exclusions.add(key)
    excluded_days = {day for day, _ in exclusions}
    path, contracts, days = [], {}, []
    for row in source['sessions']:
        _closed(row, ('account_date', 'bars'), 'source session')
        day = date.fromisoformat(row['account_date'])
        days.append(day)
        if day not in schedules:
            raise ValueError('source day absent from frozen schedule')
        empty = row['bars'] == []
        if day in excluded_days and not empty:
            raise ValueError('excluded day must have no bars')
        if empty and schedules[day][0] == 'PERMITTED' and day not in excluded_days:
            raise ValueError('unlisted empty PERMITTED day')
        if empty:
            continue
        bars = []
        for item in row['bars']:
            _closed(item, ('utc', 'legs'), 'source bar')
            ts = _utc(item['utc'])
            _closed(item['legs'], LEG_IDS, 'source legs')
            legs = []
            for leg in LEG_IDS:
                value = item['legs'][leg]
                _closed(value, ('contract', 'ohlc'), 'contract bar')
                if type(value['contract']) is not str or not value['contract']:
                    raise ValueError('contract required')
                if SYMBOLS[leg] in ('6J', 'MGC') and (SYMBOLS[leg], value['contract']) not in rolls:
                    raise ValueError('contract missing from frozen roll list')
                boundary = rolls.get((SYMBOLS[leg], value['contract']))
                if boundary is not None and ts < boundary < ts + timedelta(minutes=15):
                    raise ValueError('G4 boundary requires finer chronology')
                if type(value['ohlc']) is not list or len(value['ohlc']) != 4:
                    raise ValueError('OHLC fields')
                legs.append((leg, Bar(ts, *value['ohlc'])))
                contracts[(leg, ts)] = value['contract']
            bars.append(SourceBar(ts, tuple(legs)))
        if any(b.source_bar_time-a.source_bar_time != timedelta(minutes=15) for a,b in zip(bars,bars[1:])):
            raise ValueError('missing source chronology')
        if len(days) > 1:
            opening = datetime.combine(day-timedelta(days=1), time(18), ET).astimezone(timezone.utc)
            if not bars or bars[0].source_bar_time != opening:
                raise ValueError('missing session opening chronology')
        schedule = schedules[day][1]
        session = SourceSession(day.isoformat(), day, tuple(bars), schedule)
        for edge in (schedule.cutoff, schedule.flatten_start, schedule.own_flat_deadline):
            if not any(b.source_bar_time <= edge <= b.source_bar_time+timedelta(minutes=15) for b in bars):
                raise ValueError('missing schedule chronology')
        mapped = tuple(PathBar(b.source_bar_time, b.source_bar_time, day, b.source_bar_time.astimezone(ET), b.bars) for b in bars)
        path.append(PathSession(len(path), day, session, mapped, True, True))
    if days != list(schedules) or not excluded_days <= set(days):
        raise ValueError('source must retain every frozen schedule day')
    envelope = VerifiedInputs(MappingProxyType(retained), MappingProxyType(identities), sizing,
        equity, doc['paper_initial_capital'], doc['cap_source']['request_cap_micro_equivalents_each_leg'],
        MappingProxyType(schedules), MappingProxyType(rolls), MappingProxyType(instruments), tuple(path),
        MappingProxyType(contracts), _index_contracts(contracts), _freeze(splits), risk)
    return envelope


class _PersonalReplay(BookReplay):
    """Deliver empty-session boundaries without submitting invented price bars."""

    def run(self, path):
        def chronological():
            sessions = iter(path)
            session = next(sessions, None)
            for day in self._personal_route.schedules:
                if session is not None and session.path_session_date == day:
                    yield session
                    session = next(sessions, None)
                elif self.bar_observer is not None:
                    for leg in LEG_IDS:
                        self.bar_observer(leg, None, self.adapters[leg])
            if session is not None:
                raise ValueError('path session outside verified calendar')
        return super().run(chronological())


def build_personal_replay(envelope, *, adapter_factory, bar_observer=None):
    if type(envelope) is not VerifiedInputs:
        raise ValueError('verified input receipt required')
    checked = _verify_retained(dict(envelope.retained), dict(envelope.identities))
    if envelope != checked:
        raise ValueError('verified input derived state differs')
    envelope = checked
    from mc.simulation import EvaluationState
    strategies = adapter_factory(envelope)
    def sizing(leg, action, pb):
        values = {'lifecycle_tier': 'AUTHORIZED'}
        if action.kind == 'entry':
            if leg == 'dj30_mym_p250':
                values.update(risk_dollars=envelope.striker_risk,
                    per_contract_risk=action.stop_dist_pts*envelope.instruments[leg].pointvalue,
                    cap_alloc=envelope.request_cap)
            elif leg == 'vanguard_mgc':
                values['normal_base'] = action.qty
        return values
    def broker(leg, *args, **kwargs):
        return RouteBroker(leg, *args, initial_capital=envelope.paper_capital,
                           contract_at=envelope.contract_at, symbol=SYMBOLS[leg], **kwargs)
    eq = envelope.initial_equity
    replay = _PersonalReplay(strategies, envelope.instruments, policy=PersonalP0Policy(),
        initial_state=EvaluationState(eq, eq, eq, 0, 0), sizing_inputs=sizing,
        schedule_quotes=BracketScheduleQuotes('R1'), broker_factory=broker,
        size_vector=envelope.sizing, bar_observer=bar_observer)
    replay._personal_route = envelope
    return replay


def validate_route_output(doc):
    _closed(doc, ('schema', 'trades', 'refusals', 'days', 'input_identities', 'latch'), 'route output')
    if doc['schema'] != 'sfclear_route_output/v1':
        raise ValueError('route schema')
    _closed(doc['input_identities'], INPUT_ROLES, 'route identities')
    for value in doc['input_identities'].values():
        _digest(value)
    _closed(doc['refusals'], LEG_IDS, 'refusal legs')
    for rows in doc['refusals'].values():
        if type(rows) is not list:
            raise ValueError('refusal list required')
        for row in rows:
            _closed(row, ('utc', 'reason'), 'refusal')
            _utc(row['utc'])
            if type(row['reason']) is not str or not row['reason']:
                raise ValueError('refusal reason required')
    dates = []
    for row in doc['days']:
        _closed(row, ('account_date', 'net_pnl_usd', 'fills'), 'day')
        dates.append(date.fromisoformat(row['account_date']))
        _finite(row['net_pnl_usd'])
        if type(row['fills']) is not int or row['fills'] < 0:
            raise ValueError('day fill count')
    if not dates or dates != sorted(set(dates)):
        raise ValueError('ordered unique output days required')
    if doc['latch'] is not None:
        _closed(doc['latch'], ('utc', 'kind'), 'latch')
        _utc(doc['latch']['utc'])
        if doc['latch']['kind'] != 'personal_halt_latched':
            raise ValueError('unknown latch event')
    for trade in doc['trades']:
        _closed(trade, TRADE_FIELDS, 'trade')
        if trade['leg'] not in LEG_IDS or trade['instrument'] != SYMBOLS[trade['leg']]:
            raise ValueError('trade leg/instrument')
        if any(type(trade[k]) is not str or not trade[k] for k in ('contract', 'exit_kind')):
            raise ValueError('trade contract and exit kind required')
        if _utc(trade['entry_utc']) > _utc(trade['exit_utc']):
            raise ValueError('trade time order')
        if trade['side'] not in ('buy', 'sell') or type(trade['quantity']) is not int or trade['quantity'] <= 0:
            raise ValueError('trade side/quantity')
        if type(trade['tranche_index']) is not int or trade['tranche_index'] != 0:
            raise ValueError('R1 tranche must be zero')
        for name in ('entry_price', 'initial_stop_level', 'delta_0', 'exit_price', 'stop_fill_distance_b',
                     'net_pnl_usd', 'commission_usd', 'mae_usd', 'mfe_usd'):
            _finite(trade[name])
        if trade['mae_usd'] > 0 or trade['mfe_usd'] < 0 or trade['commission_usd'] < 0 or trade['delta_0'] < 0 or trade['stop_fill_distance_b'] < 0:
            raise ValueError('trade money/excursion signs')
        if trade['delta_0'] != abs(trade['entry_price'] - trade['initial_stop_level']):
            raise ValueError('initial stop distance differs')
    # Closed output construction below never serializes raw replay events,
    # retained bytes, paper capital, starting equity or account equity marks.
    return doc


def run_personal_replay(manifest, *, adapter_factory, bar_observer=None):
    envelope = verify_inputs(manifest)
    replay = build_personal_replay(envelope, adapter_factory=adapter_factory, bar_observer=bar_observer)
    result = replay.run(envelope.path)
    refusals = {leg: [] for leg in LEG_IDS}
    latch = None
    for event in result.events:
        if event.kind == 'refused':
            refusals[event.leg_id].append({'utc': event.path_time.isoformat(), 'reason': event.detail})
        elif event.kind == 'personal_halt_latched':
            # Carry the occurrence of A's latch, excluding its private account figures.
            latch = {'utc': event.path_time.isoformat(), 'kind': event.kind}
    sessions = {s.path_session_date: s for s in result.sessions}
    doc = {'schema': 'sfclear_route_output/v1',
           'trades': sorted([t for broker in replay.brokers.values() for t in broker.route_trades],
                            key=lambda t: (t['exit_utc'], t['leg'], t['entry_utc'])),
           'refusals': refusals,
           'days': [{'account_date': day.isoformat(),
                     'net_pnl_usd': sessions[day].pnl if day in sessions else 0.0,
                     'fills': sessions[day].fills if day in sessions else 0}
                    for day in envelope.schedules],
           'input_identities': dict(envelope.identities, size_vector=
               _json(envelope.retained['tuple'])['size_vector_sha256']), 'latch': latch}
    return canonical_json_bytes(validate_route_output(doc))
