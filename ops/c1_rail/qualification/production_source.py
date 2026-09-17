"""Concrete retained-input decoding and explicit production producer gaps.

Historical receipts remain scoped to their admitted generation. Additional
proposed source-clock, initialization and source-instant execution formats are
consumed only when their exact bytes and review companions are bound by G1.
No missing production fact is supplied by the synthetic implementation.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, fields, is_dataclass
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
from enum import Enum
import hashlib
import io
import json
from pathlib import Path
from types import MappingProxyType
from math import isfinite
import weakref

from c1_signal_daemon.book_adapters import ADAPTERS, _qualification_snapshots
from c1_signal_daemon.feed import Bar
from .model import ET, LEG_IDS, SessionSchedule, SourceBar, aware
from .clock import AccountClock, SourceDayDisposition, SourceDayStatus
from .runner import NeedsContext


@dataclass(frozen=True)
class ProducerGap:
    code: str
    producer: str
    artifact_role: str
    reason: str


PRODUCER_GAPS = (
    ProducerGap('SOURCE_CALENDAR_CAPABILITY_MISSING', 'historical source calendar producer', 'source_calendar',
                'Deployment permission/calendar membership does not provide historical venue deadlines, complete expected source dates or tail coverage.'),
    ProducerGap('SCHEDULE_INTRABAR_CAPABILITY_MISSING', 'source-instant execution evidence producer', 'schedule_execution_evidence',
                'M15 OHLC bars do not prove source-instant flatten prices or before/after OHLC segments at non-bar schedule instants.'),
    ProducerGap('STARTUP_POLICY_BINDING_MISSING', 'F1 startup/configuration owner', 'source_startup_policy',
                'Fresh-once initialization, per-port paper capital, AUTHORIZED lifecycle and micro-equivalent cap80 must be explicit reviewed frozen bytes; no defaults.'),
)


class ProductionSourceNeedsContext(NeedsContext):
    def __init__(self, gaps=PRODUCER_GAPS, *, prepared=None):
        self.gaps = tuple(gaps)
        self.prepared = prepared
        super().__init__('concrete production source capabilities missing: ' + '; '.join(g.code for g in self.gaps))


def port_active_window(leg, instant, params):
    """RC7 session windows from the accepted corrected ports, not entry signals."""
    aware(instant)
    if leg not in LEG_IDS:
        raise ValueError('unknown accepted leg')
    if leg == 'dj30_mym_p250':
        return 13 <= instant.astimezone(timezone.utc).hour < 17 if params.use_session else True
    local = instant.astimezone(ET)
    minutes = local.hour*60+local.minute
    active = params.sess_start_min <= minutes < params.sess_end_min
    if leg == 'vanguard_mgc':
        return active and local.weekday() < 5 if params.use_session else True
    return active


def request_sizing_inputs(leg, action, params, *, lifecycle_tier, cap_alloc):
    """Supply original risk before shared book_policy scaling; never round twice."""
    if lifecycle_tier not in ('AUTHORIZED', 'WATCH-1', 'WATCH-2', 'RETIRED') or type(cap_alloc) is not int or cap_alloc <= 0:
        raise ValueError('explicit lifecycle tier and positive micro-equivalent allocation required')
    result = {'lifecycle_tier': lifecycle_tier}
    if leg not in LEG_IDS:
        raise ValueError('unknown accepted leg')
    if getattr(action, 'kind', 'entry') == 'add':
        return result
    if leg == 'dj30_mym_p250':
        risk = Decimal(str(params.account_size))*Decimal(str(params.risk_per_trade_pct))/100
        per_contract = Decimal(str(action.stop_dist_pts))*Decimal(str(params.point_value))
        if not risk.is_finite() or not per_contract.is_finite() or risk <= 0 or per_contract <= 0:
            raise ValueError('positive unrounded risk/stop inputs required')
        result.update(risk_dollars=risk, per_contract_risk=per_contract, cap_alloc=cap_alloc)
    elif leg == 'vanguard_mgc':
        result['normal_base'] = action.qty
    elif leg not in ('aegis_6j', 'orb_mnq_v7'):
        raise ValueError('unknown accepted leg')
    return result


def _json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate retained JSON key')
            result[key] = value
        return result
    def reject(value):
        raise ValueError('nonfinite retained JSON value')
    return json.loads(raw.decode('utf-8-sig'), object_pairs_hook=unique, parse_constant=reject)


@dataclass(frozen=True)
class StartupPolicy:
    path_start_date: date
    paper_initial_capitals: tuple[tuple[str, Decimal], ...]
    lifecycle_tiers: tuple[tuple[str, str], ...]
    request_caps_micro_equivalents: tuple[tuple[str, int], ...]
    shared_account_cap_micro_equivalents: int


def parse_startup_policy(raw):
    """Proposed serialized F1 choice; parsing supplies no approval by itself."""
    doc = _json(raw)
    if set(doc) != {'schema', 'initialization', 'positions', 'working_orders', 'splice_behavior',
                    'path_start_date', 'shared_account_cap_micro_equivalents', 'legs'}:
        raise ValueError('complete explicit startup policy fields required')
    if (doc['schema'] != 'qualification-source-startup/v1' or doc['initialization'] != 'FRESH_ONCE_CONTINUOUS'
            or doc['positions'] != 'ZERO' or doc['working_orders'] != 'ZERO'
            or doc['splice_behavior'] != 'CARRY_ALL_STATE'):
        raise ValueError('startup requires fresh-once construction and no state resets at splices')
    if type(doc['shared_account_cap_micro_equivalents']) is not int or doc['shared_account_cap_micro_equivalents'] != 80:
        raise ValueError('shared account cap must bind the accepted 80 micro-equivalent law')
    start = date.fromisoformat(doc['path_start_date'])
    if start.weekday() >= 5 or set(doc['legs']) != set(LEG_IDS):
        raise ValueError('weekday path origin and exact four-leg startup rows required')
    capitals, tiers, caps = [], [], []
    for leg in LEG_IDS:
        row = doc['legs'][leg]
        if set(row) != {'paper_initial_capital', 'lifecycle_tier', 'request_cap_micro_equivalents'}:
            raise ValueError('complete explicit per-leg startup row required')
        if type(row['paper_initial_capital']) is not str:
            raise ValueError('paper capital must be an explicit decimal string')
        capital = Decimal(row['paper_initial_capital'])
        if not capital.is_finite() or capital <= 0:
            raise ValueError('positive finite paper initial capital required')
        if row['lifecycle_tier'] != 'AUTHORIZED':
            raise ValueError('decision-bearing startup proposal is AUTHORIZED only')
        if type(row['request_cap_micro_equivalents']) is not int or row['request_cap_micro_equivalents'] != 80:
            raise ValueError('per-request cap must be explicit 80 micro-equivalents, not chart contract units')
        capitals.append((leg, capital)); tiers.append((leg, row['lifecycle_tier'])); caps.append((leg, row['request_cap_micro_equivalents']))
    return StartupPolicy(start, tuple(capitals), tuple(tiers), tuple(caps), 80)


def _instant(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    aware(result)
    return result


def _fact(reference, artifact_digests):
    if (type(reference) is not dict or set(reference) != {'role', 'sha256'}
            or type(reference['role']) is not str or not reference['role']
            or reference['role'] not in artifact_digests
            or type(reference['sha256']) is not str or len(reference['sha256']) != 64
            or any(c not in '0123456789abcdef' for c in reference['sha256'])
            or artifact_digests[reference['role']] != reference['sha256']):
        raise ValueError('source fact must bind an exact retained artifact role/digest')


def parse_source_calendar(raw, *, artifact_digests):
    """Proposed typed source rows; source fact authority comes from frozen G1."""
    doc = _json(raw)
    if set(doc) != {'schema', 'coverage_start', 'coverage_end', 'tail_covered', 'sessions'} or doc['schema'] != 'qualification-source-calendar/v1':
        raise ValueError('explicit qualification source-calendar schema required; deployment calendar is not a substitute')
    if type(doc['tail_covered']) is not bool or not doc['sessions']:
        raise ValueError('source calendar must declare tail coverage and rows')
    rows = []
    for row in doc['sessions']:
        if set(row) != {'date', 'status', 'reason', 'facts', 'venue_deadlines'} or not row['reason'] or not row['facts']:
            raise ValueError('source date requires explicit disposition, reason and source facts')
        day = date.fromisoformat(row['date'])
        for fact in row['facts']:
            _fact(fact, artifact_digests)
        if row['status'] == 'OPEN':
            if set(row['venue_deadlines']) != set(LEG_IDS):
                raise ValueError('earliest venue deadline requires all four leg facts')
            deadlines = []
            for leg in LEG_IDS:
                item = row['venue_deadlines'][leg]
                if set(item) != {'instant', 'fact'}:
                    raise ValueError('source deadline requires instant and fact')
                _fact(item['fact'], artifact_digests)
                value = _instant(item['instant'])
                if value.astimezone(ET).date() != day:
                    raise ValueError('venue deadline differs from source date')
                deadlines.append(value)
            own = min(datetime.combine(day, time(16), ET), min(deadlines)-timedelta(minutes=15))
            own = own.astimezone(timezone.utc)
            schedule = SessionSchedule(own-timedelta(minutes=15), own-timedelta(minutes=5), own)
        else:
            if row['venue_deadlines']:
                raise ValueError('non-open source disposition cannot carry executable deadlines')
            schedule = SourceDayDisposition(SourceDayStatus(row['status']), row['reason'])
        rows.append((day, schedule))
    clock = AccountClock(tuple(rows), date.fromisoformat(doc['coverage_start']), date.fromisoformat(doc['coverage_end']), hashlib.sha256(raw).hexdigest())
    return clock, doc['tail_covered']


@dataclass(frozen=True)
class SourcePopulationIndex:
    expected_source_dates: tuple[date, ...]
    expected_source_slots: tuple[tuple[date, tuple[datetime, ...]], ...]
    populations: tuple[tuple[str, tuple[str, ...]], ...]
    expected_exclusions: tuple[tuple[date, str, str], ...]
    source_binding_bytes: bytes
    slot_provenance: tuple[tuple[date, datetime, str, tuple[str, ...]], ...]

    def validate_calendar(self, clock):
        if tuple(day for day, _ in clock.schedules) != self.expected_source_dates:
            raise ValueError('source calendar rows differ from independent expected-date index')
        slots = dict(self.expected_source_slots)
        whole_missing = {day for day, reason, _ in self.expected_exclusions if reason == 'missing_entire_session'}
        for day, row in clock.schedules:
            if isinstance(row, SessionSchedule) and not slots[day] and day not in whole_missing:
                raise ValueError('empty open-date slot index requires an explicit frozen whole-session absence disposition')

    def validate_provider_generation(self, panels, *, expected_binding):
        from .panel import source_session_date
        if json.loads(self.source_binding_bytes) != expected_binding:
            raise ValueError('population index source/provider generation binding differs from retained inputs')
        lookup = {leg:{bar.ts for bar in bars} for leg, bars in panels}
        if set(lookup) != set(LEG_IDS):
            raise ValueError('exact four retained provider panels required')
        claimed_present = set()
        for day, instant, state, claimed in self.slot_provenance:
            actual = tuple(leg for leg in LEG_IDS if instant in lookup[leg])
            if actual != claimed or (state == 'PROVIDER_PRESENT') != bool(actual):
                raise ValueError('provider slot provenance contradicts the admitted retained generation')
            if actual:
                claimed_present.add((day, instant))
        observed = {(source_session_date(instant), instant) for values in lookup.values() for instant in values}
        if claimed_present != observed:
            raise ValueError('provider-present index must match the complete retained four-panel union')

    def validate_coverage(self, sessions, exclusions):
        observed = tuple((e.session_date, e.reason, e.detail) for e in exclusions)
        if observed != self.expected_exclusions:
            raise ValueError('source exclusions differ from independently frozen coverage index')
        if tuple(s.session_id for s in sessions) != dict(self.populations)['FULL']:
            raise ValueError('covered FULL population differs from independent index')
        accepted_dates = tuple(s.source_session_date for s in sessions)
        denied_dates = tuple(e.session_date for e in exclusions)
        if (len(set(accepted_dates)) != len(accepted_dates) or set(accepted_dates) & set(denied_dates)
                or tuple(sorted((*accepted_dates, *denied_dates))) != self.expected_source_dates):
            raise ValueError('accepted sessions and exclusions do not reconstruct expected source dates')


def parse_population_index(raw, *, populations):
    """Independent pre-coverage dates/slots and exact frozen pool/exclusion plan."""
    from .panel import source_session_date
    doc = _json(raw)
    if (set(doc) != {'schema', 'expected_source_dates', 'expected_source_slots', 'populations', 'expected_exclusions', 'source_binding', 'slot_provenance'}
            or doc['schema'] != 'qualification-population-index/v1'):
        raise ValueError('complete explicit source population index required')
    dates = tuple(date.fromisoformat(value) for value in doc['expected_source_dates'])
    if not dates or dates != tuple(sorted(set(dates))):
        raise ValueError('expected source dates must be unique and ordered')
    if set(doc['expected_source_slots']) != {day.isoformat() for day in dates}:
        raise ValueError('expected M15 source slots must enumerate every indexed date')
    if set(doc['slot_provenance']) != {day.isoformat() for day in dates}:
        raise ValueError('slot provenance must enumerate every indexed source date')
    binding = doc['source_binding']
    if (set(binding) != {'panel_sha256', 'port_sha256', 'effective_settings_sha256', 'source_calendar_sha256', 'slot_presence_rule'}
            or binding['slot_presence_rule'] != 'QUALIFIED_GENERATION_UNION'
            or set(binding['panel_sha256']) != set(LEG_IDS) or set(binding['port_sha256']) != set(LEG_IDS)):
        raise ValueError('source index must bind admitted provider generation, ports, settings and calendar')
    digests = (*binding['panel_sha256'].values(), *binding['port_sha256'].values(), binding['effective_settings_sha256'], binding['source_calendar_sha256'])
    if any(type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value) for value in digests):
        raise ValueError('source binding requires exact SHA256 identities')
    slot_rows = []
    provenance = []
    for day in dates:
        slots = tuple(_instant(value) for value in doc['expected_source_slots'][day.isoformat()])
        if slots != tuple(sorted(set(slots))) or any(ts.minute % 15 or ts.second or ts.microsecond
                                                   or source_session_date(ts) != day for ts in slots):
            raise ValueError('expected source slots must be unique ordered M15 instants bound to source date')
        slot_rows.append((day, slots))
        previous = None
        present = []
        for row in doc['slot_provenance'][day.isoformat()]:
            if set(row) != {'instant','state','present_legs'} or row['state'] not in ('PROVIDER_PRESENT','PROVIDER_SHARED_ABSENCE'):
                raise ValueError('explicit qualified-provider slot state required')
            instant = _instant(row['instant'])
            legs = tuple(row['present_legs'])
            if (instant.minute % 15 or instant.second or instant.microsecond or source_session_date(instant) != day
                    or (previous is not None and instant <= previous)
                    or legs != tuple(leg for leg in LEG_IDS if leg in legs)
                    or (row['state'] == 'PROVIDER_PRESENT') != bool(legs)):
                raise ValueError('slot provenance time/leg/state binding is invalid')
            previous = instant
            provenance.append((day, instant, row['state'], legs))
            if legs:
                present.append(instant)
        if slots != tuple(present):
            raise ValueError('expected source slots must be only the qualified-provider PRESENT union; shared absence is diagnostic')
    pools = {name:tuple(values) for name, values in doc['populations'].items()}
    if (set(pools) != {'FULL','H1','H2'} or pools != {name:tuple(values) for name, values in populations.items()}
            or any(type(value) is not str or not value for values in pools.values() for value in values)):
        raise ValueError('source population index must match exact frozen FULL/H1/H2')
    full = pools['FULL']; middle = (len(full)+1)//2
    if not full or len(set(full)) != len(full) or pools['H1'] != full[:middle] or pools['H2'] != full[middle:]:
        raise ValueError('source population halves must be the disjoint chronological ceil partition')
    exclusions = []
    allowed = {'missing_active_bar','missing_entire_session','exchange_closed','policy_denied'}
    for row in doc['expected_exclusions']:
        if set(row) != {'source_date','reason','detail'} or row['reason'] not in allowed or type(row['detail']) is not str or not row['detail']:
            raise ValueError('explicit supported source exclusion required; deadline failure is not an exclusion')
        exclusions.append((date.fromisoformat(row['source_date']), row['reason'], row['detail']))
    excluded_dates = tuple(day for day, _, _ in exclusions)
    if excluded_dates != tuple(sorted(set(excluded_dates))) or not set(excluded_dates) <= set(dates):
        raise ValueError('source exclusion dates must be unique ordered members of expected index')
    binding_bytes = json.dumps(binding, sort_keys=True, separators=(',',':')).encode()
    return SourcePopulationIndex(dates, tuple(slot_rows), tuple((name,pools[name]) for name in ('FULL','H1','H2')), tuple(exclusions), binding_bytes, tuple(provenance))


@dataclass(frozen=True)
class ScheduleExecutionEvidence:
    quotes: object
    splits: object
    source_rows: tuple

    @property
    def schedule_quotes(self):
        return self

    def __call__(self, session, instant, leg):
        from .replay import ReplayNeedsContext
        try:
            return self.quotes[(session.source.source_session_date, leg, instant)]
        except KeyError as exc:
            raise ReplayNeedsContext('missing reviewed source-instant schedule price') from exc

    def split_bar(self, session, pb, instant, leg):
        return self._split_at(session, pb, pb.source_bar_time, instant, leg)

    def split_interval(self, session, pb, original, instant, leg):
        return self._split_at(session, pb, original.ts, instant, leg)

    def _split_at(self, session, pb, start, instant, leg):
        from .replay import ReplayNeedsContext
        try:
            return self.splits[(session.source.source_session_date, leg, pb.source_bar_time, start, instant)]
        except KeyError as exc:
            raise ReplayNeedsContext('missing reviewed source interval split evidence') from exc

    def validate_split(self, session, pb, bars, instant):
        from .replay import BookReplay
        # The exact engine validator owns OHLC aggregation and TV path law.
        return BookReplay._split(self, session, pb, bars, instant)

    def validate_supplied(self, panels):
        """Check supplied claims against retained bars without requiring claims.

        Missing evidence is meaningful only at a consuming replay event. A
        supplied later subinterval must be anchored by an earlier validated
        suffix; that dependency validates the claim, not hypothetical exposure.
        """
        from types import SimpleNamespace
        from .panel import source_session_date
        source = {(source_session_date(bar.ts), leg, bar.ts): bar
                  for leg, bars in panels for bar in bars}
        suffixes = {}
        for day, leg, bar_time, start, instant in sorted(self.source_rows):
            original = source.get((day, leg, bar_time))
            if original is None:
                raise ValueError('schedule evidence has no matching retained source bar')
            key = (day, leg, bar_time, start, instant)
            if key not in self.splits:
                expected = original.open if instant == bar_time else original.close
                if self.quotes[(day, leg, instant)] != expected:
                    raise ValueError('grid-boundary quote contradicts retained source bar')
                continue
            anchor = original if start == bar_time else suffixes.get((day, leg, bar_time, start))
            if anchor is None:
                raise ValueError('source subinterval split has no validated prefix anchor')
            session = SimpleNamespace(source=SimpleNamespace(source_session_date=day))
            pb = SimpleNamespace(source_bar_time=bar_time)
            _, right = self.validate_split(session, pb, {leg: anchor}, instant)
            suffix_key = (day, leg, bar_time, instant)
            if suffix_key in suffixes and suffixes[suffix_key] != right[leg]:
                raise ValueError('conflicting retained source subinterval evidence')
            suffixes[suffix_key] = right[leg]


def parse_schedule_execution_evidence(raw):
    doc = _json(raw)
    if set(doc) != {'schema', 'rows'} or doc['schema'] != 'qualification-schedule-execution/v1':
        raise ValueError('explicit source execution-evidence schema required')
    quotes, splits, source_rows = {}, {}, []
    if type(doc['rows']) is not list:
        raise ValueError('execution evidence rows must be a list')
    for row in doc['rows']:
        if set(row) != {'source_session_date', 'leg_id', 'source_bar_time', 'interval_start', 'instant', 'price', 'prefix', 'suffix'}:
            raise ValueError('complete source execution evidence row required')
        day, leg = date.fromisoformat(row['source_session_date']), row['leg_id']
        if leg not in LEG_IDS:
            raise ValueError('unknown schedule evidence leg')
        bar_time, start, instant = (_instant(row[key]) for key in ('source_bar_time', 'interval_start', 'instant'))
        from .panel import source_session_date
        if source_session_date(bar_time) != day or not bar_time <= start <= instant <= bar_time+timedelta(minutes=15):
            raise ValueError('schedule evidence interval/source date mismatch')
        price = row['price']
        if type(price) not in (int, float) or not isfinite(price) or price <= 0:
            raise ValueError('finite positive source-instant price required')
        qkey = (day, leg, instant)
        if qkey in quotes and quotes[qkey] != price:
            raise ValueError('conflicting source-instant quotes')
        quotes[qkey] = float(price)
        source_rows.append((day, leg, bar_time, start, instant))
        # A grid-boundary quote can omit split segments; intrabar boundaries
        # require both. Split semantics are checked against the original panel.
        if row['prefix'] is None and row['suffix'] is None:
            if instant not in (bar_time, bar_time+timedelta(minutes=15)):
                raise ValueError('intrabar source instant requires split segments')
            continue
        if not bar_time <= start < instant < bar_time+timedelta(minutes=15):
            raise ValueError('split evidence requires a strict intrabar interval')
        values = []
        for key, ts in (('prefix', start), ('suffix', instant)):
            segment = row[key]
            if type(segment) is not dict or set(segment) != {'open', 'high', 'low', 'close', 'volume'}:
                raise ValueError('complete prefix/suffix OHLCV required')
            if any(type(x) not in (int, float) or not isfinite(x) for x in segment.values()):
                raise ValueError('finite numeric segment values required')
            values.append(Bar(ts, **segment))
        key = (day, leg, bar_time, start, instant)
        if key in splits:
            raise ValueError('duplicate source interval evidence')
        splits[key] = tuple(values)
    return ScheduleExecutionEvidence(MappingProxyType(quotes), MappingProxyType(splits), tuple(source_rows))


@dataclass(frozen=True)
class HistoricalAdmission:
    interval_start: datetime
    interval_end: datetime
    panels: tuple[tuple[str, str], ...]
    ports: tuple[tuple[str, str], ...]


def parse_historical_admission(admission_bytes, acceptance_bytes):
    """Decode actual Step 3 formats; external G1 pins supply authority.

    The proposal's PENDING label is preserved: a separate accepted receipt binds
    its exact bytes. This parser alone never grants historical or new approval.
    """
    doc, review = _json(admission_bytes), _json(acceptance_bytes)
    if doc.get('schema') != 'packet1-step3-evidence-admission-v1':
        raise ValueError('unsupported historical admission format')
    if (review.get('schema') != 'packet1-step3-review-approval-v1' or review.get('decision') != 'ACCEPTED'
            or review.get('accepted_contract_sha256') != hashlib.sha256(admission_bytes).hexdigest()
            or review.get('evidence_index_v4_sha256') != doc.get('evidence_index_sha256')):
        raise ValueError('separate historical review does not accept these exact bytes')
    start, end = (datetime.fromisoformat(value.replace('Z', '+00:00')) for value in doc['interval_utc'])
    aware(start); aware(end)
    if start >= end:
        raise ValueError('historical source interval order')
    aliases = {'aegis_6j': ('aegis_6j',), 'dj30_mym_p250': ('S-P', 'S-W1', 'S-W1P', 'S-W2', 'S-W2P'),
               'vanguard_mgc': ('vanguard_mgc',), 'orb_mnq_v7': ('O-N', 'O-P')}
    panels, ports = [], []
    for leg in LEG_IDS:
        rows = [doc['cases'][case] for case in aliases[leg]]
        for field, target in (('panel_sha256', panels), ('port_sha256', ports)):
            values = {row[field] for row in rows}
            if len(values) != 1:
                raise ValueError('historical cases disagree on source or corrected runtime')
            digest = values.pop()
            if type(digest) is not str or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
                raise ValueError('historical digest malformed')
            target.append((leg, digest))
    return HistoricalAdmission(start, end, tuple(panels), tuple(ports))


def decode_admitted_csv(raw: bytes, expected_sha256: str):
    """Actual accepted ISO-time OHLCV format, parsed from one verified buffer."""
    if type(raw) is not bytes or hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError('admitted CSV digest mismatch')
    reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig')))
    if reader.fieldnames != ['time', 'open', 'high', 'low', 'close', 'volume']:
        raise ValueError('unsupported admitted CSV column format')
    result = []
    for row in reader:
        if set(row) != set(reader.fieldnames) or any(value is None for value in row.values()):
            raise ValueError('malformed admitted CSV row')
        ts = datetime.fromisoformat(row['time'].replace('Z', '+00:00'))
        aware(ts)
        bar = Bar(ts, *(float(row[key]) for key in ('open', 'high', 'low', 'close', 'volume')))
        SourceBar(ts, ((LEG_IDS[0], bar),))
        if result and result[-1].ts >= ts:
            raise ValueError('duplicate or unordered admitted CSV time')
        result.append(bar)
    if not result:
        raise ValueError('empty admitted CSV')
    return tuple(result)


@dataclass(frozen=True)
class PreparedProductionInputs:
    """Private retained data only: no source-ready or qualification assertion."""
    contract_sha256: str
    retained_bytes: tuple[tuple[str, bytes], ...]
    load_trace: tuple[tuple[str, str, str], ...]
    historical_admission: HistoricalAdmission
    panels: tuple[tuple[str, tuple[Bar, ...]], ...]
    startup: StartupPolicy | None = None
    gaps: tuple[ProducerGap, ...] = PRODUCER_GAPS


def _read_retained_artifacts(artifacts, artifact_root):
    root = Path(artifact_root).resolve()
    retained, resolved = {}, set()
    for row in artifacts:
        path = (root / row.path).resolve()
        if not path.is_relative_to(root) or path in resolved:
            raise ValueError('retained artifact escapes root or aliases another artifact')
        resolved.add(path)
        try:
            retained[row.path] = path.read_bytes()
        except FileNotFoundError as exc:
            raise ProductionSourceNeedsContext((ProducerGap('RETAINED_ARTIFACT_MISSING', 'frozen artifact custodian', row.role,
                                                           'The exact artifact path bound by the contract is not available.'),)) from exc
    return retained


def prepare_production_inputs(contract, *, artifact_root):
    from c1_signal_daemon.book_adapters import _qualification_domain
    domain = _qualification_domain(contract)
    if domain.authority_class != 'OPERATOR' or domain.permits_synthetic:
        raise ValueError('exact production G1-validated contract required')
    return _prepare_domain_inputs(contract, artifact_root=artifact_root, domain=domain)


def _prepare_domain_inputs(contract, *, artifact_root, domain):
    from c1_signal_daemon.book_adapters import _qualification_domain
    if _qualification_domain(contract) is not domain:
        raise ValueError('source preparation domain differs from exact contract domain')
    retained = _read_retained_artifacts(contract.artifacts, artifact_root)
    snapshots, _, trace = _qualification_snapshots(contract, retained)
    by_role = {row.role: row for row in contract.artifacts}
    for role, digest in domain.accepted_historical_pins.items():
        if role not in by_role or by_role[role].sha256 != digest:
            raise ValueError('historical admission role differs from accepted pin')
    admission = parse_historical_admission(snapshots['step3_admission_contract'], snapshots['step3_independent_acceptance'])
    step6 = _json(snapshots['step6_admission_contract'])
    if step6.get('schema') != 'book-bundle-admissions-v1' or set(step6.get('bundles', {})) != {
            'O-N', 'O-P', 'S-P', 'S-W1', 'S-W1P', 'S-W2', 'S-W2P'}:
        raise ValueError('unsupported seven-bundle historical admission format')
    if dict(admission.ports) != {leg: pin.runtime_sha256 for leg, pin in domain.port_runtime_pins.items()}:
        raise ValueError('historical admission does not retain corrected Striker/four-leg ports')
    panels = []
    for leg, digest in admission.panels:
        matches = [row for row in contract.artifacts if row.sha256 == digest]
        if len(matches) != 1:
            raise ProductionSourceNeedsContext((ProducerGap('ADMITTED_PANEL_ARTIFACT_MISSING', 'retained panel producer', leg,
                                                           'Exactly one contract artifact must retain the admitted panel digest, including attested Aegis prefix.'),))
        bars = decode_admitted_csv(retained[matches[0].path], digest)
        if bars[0].ts < admission.interval_start or bars[-1].ts > admission.interval_end:
            raise ValueError('admitted CSV outside retained source interval')
        if leg == 'aegis_6j' and bars[0].ts != admission.interval_start:
            raise ValueError('Aegis attested full-origin prefix is missing')
        panels.append((leg, bars))
    startup = parse_startup_policy(snapshots['source_startup_policy']) if 'source_startup_policy' in snapshots else None
    gaps = tuple(gap for gap in PRODUCER_GAPS if not (startup is not None and gap.code == 'STARTUP_POLICY_BINDING_MISSING'))
    return PreparedProductionInputs(contract.contract_sha256, tuple(retained.items()), trace, admission, tuple(panels), startup, gaps)


def _review(raw, *, role, digest, scope, source_binding_sha256=None):
    doc = _json(raw)
    expected = {'schema': 'qualification-source-review/v1', 'artifact_role': role,
                'artifact_sha256': digest, 'scope': scope, 'decision': 'ACCEPTED'}
    if source_binding_sha256 is not None:
        expected['source_binding_sha256'] = source_binding_sha256
    if doc != expected:
        raise ValueError('review companion does not bind exact source artifact/scope')


_SOURCE_TOKEN = object()
_SOURCE_ISSUED = {}


def _execution_snapshot(value):
    """Stream a type/length-framed digest, retaining no mutable field values.

    Each verification traverses the full source graph: O(source size) time and
    O(nesting depth) traversal space. Only a 32-byte derived-state digest is
    retained per issued source. Shared bars may be visited more than once; no
    source rebuild or large expanded copy is hidden in verification.
    """
    digest, visiting = hashlib.sha256(), set()
    def frame(raw):
        digest.update(len(raw).to_bytes(8, 'big'))
        digest.update(raw)
    def kind_tag(kind):
        # Type identity is stable within this issuance lifetime. The qualified
        # name is diagnostic framing, never a substitute for exact identity.
        frame(str(id(kind)).encode('ascii'))
        frame((kind.__module__+'.'+kind.__qualname__).encode('utf-8'))
    def capture(item):
        kind = type(item)
        kind_tag(kind)
        if item is None:
            return
        if kind is bool:
            frame(b'1' if item else b'0'); return
        if kind is int:
            frame(str(item).encode('ascii')); return
        if kind is str:
            frame(item.encode('utf-8')); return
        if kind is bytes:
            frame(item); return
        if kind is float:
            frame(item.hex().encode('ascii')); return
        if kind is Decimal:
            capture(tuple(item.as_tuple())); return
        if kind is datetime:
            capture(item.isoformat()); capture(item.fold)
            kind_tag(type(item.tzinfo))
            capture(getattr(item.tzinfo, 'key', None)); capture(item.tzname())
            return
        if kind is date:
            frame(item.isoformat().encode('ascii')); return
        if kind is timedelta:
            capture((item.days, item.seconds, item.microseconds)); return
        if isinstance(item, Enum):
            capture(item.name); capture(item.value); return
        identity = id(item)
        if identity in visiting:
            raise ValueError('source integrity snapshot contains a cycle')
        visiting.add(identity)
        if kind in (tuple, list):
            frame(str(len(item)).encode('ascii'))
            for part in item: capture(part)
        elif kind in (dict, MappingProxyType):
            frame(str(len(item)).encode('ascii'))
            for key, part in item.items(): capture(key); capture(part)
        elif is_dataclass(item) and not isinstance(item, type):
            declared = fields(item)
            frame(str(len(declared)).encode('ascii'))
            for field in declared: capture(field.name); capture(getattr(item, field.name))
            # Frozen dict-backed nested records can still acquire instance
            # attributes through object.__setattr__, including method shadows.
            names = {field.name for field in declared}
            extras = tuple((key, part) for key, part in getattr(item, '__dict__', {}).items()
                           if key not in names)
            capture(extras)
        else:
            raise ValueError('unsupported source integrity field type: '+kind.__name__)
        visiting.remove(identity)
    capture(value)
    return digest.digest()


def _source_execution_snapshot(source):
    # Authority objects have their own issuance/reconstruction guards. Retain
    # their exact identity here rather than copying their large signed trees.
    references = {'contract', '_domain', '_token'}
    derived = tuple((field.name, getattr(source, field.name)) for field in fields(source)
                    if field.name not in references)
    return (type(source), id(source.contract), id(source._domain), id(source._token),
            _execution_snapshot(derived))


@dataclass(frozen=True, init=False, slots=True, weakref_slot=True)
class ProductionSource:
    """Concrete factory; one freshly loaded four-port engine per whole path.

    Only ``build`` creates objects. Its inputs are frozen artifact bytes, never
    caller-supplied replay/quote/window callbacks. Proposed JSON formats are
    capabilities, not approvals; missing source facts fail before any replay.
    """
    contract: object
    prepared: PreparedProductionInputs
    sessions: tuple
    adjacent: tuple
    clock: AccountClock
    covered_until: date
    tail_covered: bool
    path_start_date: date
    exclusions: tuple
    shared_provider_gaps: tuple
    _quotes: ScheduleExecutionEvidence
    _instruments: tuple
    _token: object
    _domain: object

    def __new__(cls, *args, **kwargs):
        raise ProductionSourceNeedsContext()

    @classmethod
    def build(cls, contract, *, artifact_root):
        from c1_signal_daemon.book_adapters import _qualification_domain
        domain = _qualification_domain(contract)
        if domain.authority_class != 'OPERATOR' or domain.permits_synthetic:
            raise ValueError('exact production OPERATOR contract required')
        return cls._build_domain(contract, artifact_root=artifact_root, domain=domain)

    @classmethod
    def _build_composition(cls, contract, *, artifact_root):
        from c1_signal_daemon.book_adapters import _qualification_domain
        domain = _qualification_domain(contract)
        if domain.authority_class != 'TEST_ONLY' or not domain.permits_synthetic:
            raise ValueError('TEST_ONLY composition contract domain required')
        return cls._build_domain(contract, artifact_root=artifact_root, domain=domain)

    @classmethod
    def _build_domain(cls, contract, *, artifact_root, domain):
        from c1_signal_daemon.book_adapters import _load_domain_adapters
        from .panel import build_panel, CoverageReport, Exclusion
        from .replay import Instrument
        prepared = _prepare_domain_inputs(contract, artifact_root=artifact_root, domain=domain)
        retained = dict(prepared.retained_bytes)
        snapshots = {role: retained[path] for role, path, _ in prepared.load_trace}
        digests = {role: digest for role, _, digest in prepared.load_trace}
        required = {'source_startup_policy', 'source_calendar', 'source_calendar_review', 'population_index', 'population_index_review',
                    'schedule_execution_evidence', 'schedule_execution_evidence_review', 'cost_model'}
        missing = required-set(snapshots)
        if missing:
            gaps = tuple(ProducerGap('REVIEWED_SOURCE_ARTIFACT_MISSING', 'F1 source evidence producer', role,
                                    'Concrete source capability and review bytes must be retained in the signed closed artifact inventory.')
                         for role in sorted(missing))
            raise ProductionSourceNeedsContext(gaps, prepared=prepared)
        for role, scope in (('source_calendar', 'SOURCE_CALENDAR'), ('schedule_execution_evidence', 'SCHEDULE_EXECUTION')):
            _review(snapshots[role+'_review'], role=role, digest=digests[role], scope=scope)
        startup = parse_startup_policy(snapshots['source_startup_policy'])
        clock, tail = parse_source_calendar(snapshots['source_calendar'], artifact_digests=digests)
        population_index = parse_population_index(snapshots['population_index'], populations=contract.populations)
        _review(snapshots['population_index_review'], role='population_index', digest=digests['population_index'], scope='SOURCE_POPULATION_INDEX',
                source_binding_sha256=hashlib.sha256(population_index.source_binding_bytes).hexdigest())
        population_index.validate_calendar(clock)
        population_index.validate_provider_generation(prepared.panels, expected_binding={
            'panel_sha256':dict(prepared.historical_admission.panels), 'port_sha256':dict(prepared.historical_admission.ports),
            'effective_settings_sha256':contract.effective_settings_sha256, 'source_calendar_sha256':digests['source_calendar'],
            'slot_presence_rule':'QUALIFIED_GENERATION_UNION'})
        unknown = [(day, row.reason) for day, row in clock.schedules
                   if isinstance(row, SourceDayDisposition) and row.status is SourceDayStatus.UNKNOWN]
        if unknown:
            raise ProductionSourceNeedsContext(tuple(ProducerGap('UNKNOWN_SOURCE_DATE', 'historical source evidence producer', 'source_calendar',
                                                                f'{day.isoformat()}: {reason}') for day, reason in unknown), prepared=prepared)
        loaded = _load_domain_adapters(contract, retained_bytes=retained, domain=domain)
        settings = _json(snapshots['effective_settings_successor'])
        for leg, adapter in loaded.registry.items():
            p = adapter.params
            if getattr(adapter, 'quantity_rule', None) is not None:
                raise ValueError('accepted normal adapter quantity must reach shared sizing without an injected pre-scaling rule')
            captured = getattr(p, 'initial_capital', getattr(p, 'account_size', None))
            if captured is not None and Decimal(str(captured)) != dict(startup.paper_initial_capitals)[leg]:
                raise ValueError('startup paper capital differs from approved adapter constructor')
        schedules = dict(clock.schedules)
        denied = tuple(day for day, row in clock.schedules if isinstance(row, SourceDayDisposition))
        coverage = build_panel(dict(prepared.panels), schedules=schedules,
                               expected_dates=population_index.expected_source_dates, excluded_dates=denied,
                               active=lambda leg, instant: port_active_window(leg, instant, loaded.registry[leg].params))
        # Preserve the typed reason; build_panel's historical generic exclusion
        # label must not turn a policy restriction into an exchange closure.
        exclusions = tuple(Exclusion(e.session_date, schedules[e.session_date].status.value, schedules[e.session_date].reason)
                           if e.session_date in denied else e for e in coverage.exclusions)
        sessions = coverage.sessions
        population_index.validate_coverage(sessions, exclusions)
        if not sessions or tuple(s.session_id for s in sessions) != tuple(contract.populations['FULL']):
            raise ValueError('covered production source population differs from frozen FULL index')
        quotes = parse_schedule_execution_evidence(snapshots['schedule_execution_evidence'])
        quotes.validate_supplied(prepared.panels)
        costs = _json(snapshots['cost_model'])
        cost_rows = costs.get('rows', [])
        by_symbol = {row['symbol']: Decimal(row['round_trip_usd'])/2 for row in cost_rows}
        if len(cost_rows) != 4 or set(by_symbol) != {spec.symbol for spec in ADAPTERS} or any(not value.is_finite() or value < 0 for value in by_symbol.values()):
            raise ValueError('exact four-symbol finite venue commission schedule required')
        instruments = []
        for spec in ADAPTERS:
            emulator = settings[spec.leg_id]['emulator']
            if 'slippage_ticks' not in emulator or type(emulator.get('orders_on_close')) is not bool:
                raise ValueError('explicit approved emulator slippage and close timing required')
            instruments.append((spec.leg_id, Instrument(spec.mintick, spec.pointvalue, emulator['slippage_ticks'],
                                                       float(by_symbol[spec.symbol]), emulator['orders_on_close'])))
        result = object.__new__(cls)
        fields = dict(contract=contract, prepared=prepared, sessions=sessions, adjacent=coverage.adjacent, clock=clock,
                      covered_until=clock.coverage_end+timedelta(days=1), tail_covered=tail,
                      path_start_date=startup.path_start_date, exclusions=exclusions, _quotes=quotes,
                      shared_provider_gaps=tuple((day,instant) for day,instant,state,_ in population_index.slot_provenance
                                                 if state=='PROVIDER_SHARED_ABSENCE'),
                      _instruments=tuple(instruments), _token=_SOURCE_TOKEN, _domain=domain)
        for name, value in fields.items():
            object.__setattr__(result, name, value)
        identity = id(result)
        _SOURCE_ISSUED[identity] = (weakref.ref(result, lambda ref: _SOURCE_ISSUED.pop(identity, None)),
                                    _source_execution_snapshot(result))
        return result

    def verify_for(self, contract):
        from c1_signal_daemon.book_adapters import _qualification_domain
        issued = _SOURCE_ISSUED.get(id(self))
        if issued is None or issued[0]() is not self:
            raise ValueError('factory-issued source object required')
        if _source_execution_snapshot(self) != issued[1]:
            raise ValueError('issued source execution state changed')
        if (type(self) is not ProductionSource or self._token is not _SOURCE_TOKEN or self.contract is not contract
                or _qualification_domain(contract) is not self._domain
                or self.prepared.contract_sha256 != contract.contract_sha256):
            raise ValueError('source factory identity does not bind the exact production G1 contract')
        _qualification_snapshots(contract, dict(self.prepared.retained_bytes))

    def replay(self, path):
        from c1_signal_daemon.book_adapters import _load_domain_adapters
        from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
        from c1_rail.book_policy import candidate_book_protection_policy
        from mc.simulation import EvaluationState
        from .replay import BookReplay
        self.verify_for(self.contract)
        by_id = {s.session_id: s for s in self.sessions}
        if not path or any(by_id.get(s.source.session_id) != s.source for s in path):
            raise ValueError('path contains a source session outside retained covered panel')
        loaded = _load_domain_adapters(self.contract, retained_bytes=dict(self.prepared.retained_bytes), domain=self._domain)
        startup = self.prepared.startup
        if startup is None:
            raise ProductionSourceNeedsContext((PRODUCER_GAPS[-1],))
        tiers, caps, capitals = dict(startup.lifecycle_tiers), dict(startup.request_caps_micro_equivalents), dict(startup.paper_initial_capitals)
        def sizing(leg, action, pb):
            return request_sizing_inputs(leg, action, loaded.registry[leg].params,
                                         lifecycle_tier=tiers[leg], cap_alloc=caps[leg])
        def brokers(leg, *args, **kwargs):
            # RC1/O-7 deliberately exclude the TradingView margin branch. The
            # historical ORB margin100 input remains retained provenance;
            # BookReplay passes margin_pct=0 for this qualification model.
            return TVBrokerEmulator(leg, *args, initial_capital=float(capitals[leg]), **kwargs)
        state = self.contract.initial_state
        initial = EvaluationState(float(state.original_basis), float(state.current_equity), float(state.historical_eod_peak),
                                  state.prior_trade_days, float(state.prior_max_day_profit))
        engine = BookReplay(loaded.registry, dict(self._instruments), policy=candidate_book_protection_policy(),
                            initial_state=initial, sizing_inputs=sizing, schedule_quotes=self._quotes, broker_factory=brokers)
        return engine.run(path)

    def proof(self, panel):
        from .paths import PathAssembler
        path = PathAssembler(self.path_start_date).assemble(tuple((s,) for s in panel), horizon_sessions=len(panel))
        result = self.replay(path)
        rows = result.sessions
        if len(rows) != len(panel) or any(a.end_edge != b.start_edge for a, b in zip(rows, rows[1:])):
            raise ValueError('continuous proof replay has incomplete or discontinuous ledger edges')
        edges = (rows[0].start_edge,)+tuple(row.end_edge for row in rows)
        source_index = {s.session_id:i for i, s in enumerate(self.sessions)}
        joins = []
        for left, right in zip(panel, panel[1:]):
            a, b = source_index[left.session_id], source_index[right.session_id]
            joins.append(self.adjacent[a] if b == a+1 else True)
        return edges, tuple(joins)
