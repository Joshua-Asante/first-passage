"""Injected book host; synthetic-qualified composition, without registration.

Timing inputs describe a healthy-host envelope. Post-return mark gates do not
cancel calls, bound SQLite/IO, supervise the process, or qualify a live monitor.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields
import hashlib
import json
import math
import re
from types import MappingProxyType

from c1_signal_daemon import book_heartbeat
from c1_rail.book_protection_owner import PROTECTION_PERIOD

ESCALATION_STEP_S = 60.0
K_FLOOR = 8


def _ping(reference):
    return {'secret_ref': reference, 'period_s': 12.0, 'timeout_s': 5.0}


@dataclass(frozen=True)
class BookHostBinding:
    """Canonical inputs; round and poll bounds are derived, never independent overrides."""

    step_interval_s: float = 10.0
    max_step_duration_s: float = 10.0
    notifier_interval_s: float = 10.0
    max_jobs_per_round: int = 8
    retry_max_s: float = 10.0
    scheduler_slack_s: float = 1.0
    runtime_timeout_s: float = 60.0
    notifier_timeout_s: float = 120.0
    ingestion_allowance_s: float = 30.0
    chain_s: float = 90.0
    publish_timeout_s: float = 2.0
    max_retained_incidents: int = 1000
    channel_kinds: tuple[str, ...] = ('grafana_irm', 'local_file')
    owner_read_s: float = 1.0
    journal_s: float = 0.1
    parse_s: float = 1.0
    epsilon_s: float = 1.0
    runtime_ping: Mapping = field(default_factory=lambda: _ping('env:FP_DMON_GRAFANA_IRM_HEARTBEAT_URL'), repr=False)
    notifier_ping: Mapping = field(default_factory=lambda: _ping('env:FP_DMON_GRAFANA_IRM_NOTIFIER_HEARTBEAT_URL'), repr=False)

    def __post_init__(self):
        for side in ('runtime', 'notifier'):
            name = side + '_ping'
            raw = getattr(self, name)
            if not isinstance(raw, Mapping):
                raise ValueError(side + ' ping binding requires a mapping')
            object.__setattr__(self, name, MappingProxyType(dict(raw)))
        object.__setattr__(self, 'channel_kinds', tuple(self.channel_kinds))

    @property
    def max_round_duration_s(self):
        jobs_channels = self.max_jobs_per_round * len(self.channel_kinds)
        return (self.owner_read_s + self.parse_s + (2 + 2 * jobs_channels) * self.journal_s
                + jobs_channels * self.publish_timeout_s + self.epsilon_s)

    @property
    def poll_bound_s(self):
        return self.owner_read_s + self.parse_s + self.journal_s

    @property
    def max_step_interval(self):
        return max(self.step_interval_s, self.max_step_duration_s) + self.scheduler_slack_s

    @property
    def max_notifier_loop_interval(self):
        return max(self.notifier_interval_s, self.max_round_duration_s) + self.scheduler_slack_s


def _positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError(name + ' must be finite and positive')


def validate_binding(binding):
    """Refuse arithmetic breaches at the consumption boundary; no environment access."""
    if not isinstance(binding, BookHostBinding):
        raise ValueError('BookHostBinding required')
    for item in fields(binding):
        if item.name not in ('runtime_ping', 'notifier_ping', 'channel_kinds'):
            _positive(getattr(binding, item.name), item.name)
    for name in ('max_jobs_per_round', 'max_retained_incidents'):
        if not isinstance(getattr(binding, name), int):
            raise ValueError('notifier ' + name + ' requires an integer')
    if sorted(binding.channel_kinds) != ['grafana_irm', 'local_file']:
        raise ValueError('notifier channel kinds/count mismatch')
    for side, duration, interval in (
        ('runtime', binding.max_step_duration_s, binding.max_step_interval),
        ('notifier', binding.max_round_duration_s, binding.max_notifier_loop_interval),
    ):
        ping = getattr(binding, side + '_ping')
        if set(ping) != {'secret_ref', 'period_s', 'timeout_s'}:
            raise ValueError(side + ' ping binding keys invalid')
        reference = ping['secret_ref']
        if not isinstance(reference, str) or not re.fullmatch(r'env:[A-Za-z_][A-Za-z0-9_]*', reference):
            raise ValueError(side + ' ping requires an environment reference')
        for name in ('period_s', 'timeout_s'):
            _positive(ping[name], side + ' ping ' + name)
        timeout = getattr(binding, side + '_timeout_s')
        for constraint, left, right in (
            ('a', ping['timeout_s'], ping['period_s']),
            ('b', ping['period_s'] + interval + duration + ping['timeout_s'], timeout),
            ('c', timeout + binding.ingestion_allowance_s + binding.chain_s, PROTECTION_PERIOD.total_seconds()),
        ):
            if not left < right:
                raise ValueError(side + ' constraint (' + constraint + ') breached')
    if binding.runtime_ping['secret_ref'] == binding.notifier_ping['secret_ref']:
        raise ValueError('runtime and notifier require separate references')
    if not binding.retry_max_s + binding.max_notifier_loop_interval + binding.poll_bound_s < ESCALATION_STEP_S:
        raise ValueError('notifier constraint (d) breached')
    if binding.max_jobs_per_round < K_FLOOR:
        raise ValueError("notifier constraint (e') breached")


def binding_digest(binding):
    validate_binding(binding)
    resolved = {item.name: getattr(binding, item.name) for item in fields(binding)}
    for side in ('runtime', 'notifier'):
        resolved[side + '_ping'] = dict(resolved[side + '_ping'])
    return hashlib.sha256(json.dumps(resolved, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


FROZEN_BINDING = BookHostBinding()

# The two schedulers share only the stop event. Each owns its observations/state.
from collections import Counter
from datetime import datetime, timezone
import threading
import time


class NotifierClockObserver:
    """Pass through the notifier wall clock; capture only this invocation/thread.

    Pinned notifier order: poll, publish_due (inside its lock), completion.
    Two reads with no progress is a normal loud pass. Other shapes fail closed.
    """

    def __init__(self, wall_clock, *, monotonic=time.monotonic):
        self.wall_clock = wall_clock
        self.monotonic = monotonic
        self._local = threading.local()

    def begin(self):
        if getattr(self._local, 'scope', None) is not None:
            raise ValueError('notifier observer scope already active')
        self._local.scope = {'reads': [], 'calling': False, 'fault': False}

    def end(self):
        scope = self._local.scope
        self._local.scope = None
        return tuple(scope['reads']), scope['fault']

    def __call__(self):
        scope = getattr(self._local, 'scope', None)
        if scope is None:
            return self.wall_clock()
        if scope['calling']:
            scope['fault'] = True
            return self.wall_clock()
        scope['calling'] = True
        try:
            value = self.wall_clock()
            observed = self.monotonic()
            if len(scope['reads']) < 4:
                scope['reads'].append(observed)
            else:
                scope['fault'] = True
            return value
        except Exception:
            scope['fault'] = True
            raise
        finally:
            scope['calling'] = False


class _DeferredMark:
    """Keep NF6 observations in the real pinger, defer only its mark side effect."""

    def __init__(self, pinger):
        self.pinger = pinger
        self.requested = False

    @property
    def has_count(self):
        return self.pinger.has_count

    def observe_count(self, count):
        return self.pinger.observe_count(count)

    def mark_progress(self):
        self.requested = True


def _interval(start, end):
    return (isinstance(start, (int, float)) and isinstance(end, (int, float))
            and math.isfinite(start) and math.isfinite(end) and end >= start)


def _stats():
    return {'calls_started': 0, 'raises': Counter(), 'max_duration_s': 0.0,
            'max_start_gap_s': 0.0, 'max_poll_s': 0.0, 'max_publish_gap_s': 0.0,
            'marks_forwarded': 0, 'marks_suppressed': 0, 'observation_faults': 0}


def _schedule(call, *, interval, monotonic, wait, stop_event, stats, stop_on_raise):
    previous = None
    while not stop_event.is_set():
        start = monotonic()
        if previous is not None:
            if _interval(previous, start):
                stats['max_start_gap_s'] = max(stats['max_start_gap_s'], start - previous)
            else:
                stats['observation_faults'] += 1
        previous = start
        stats['calls_started'] += 1
        try:
            call(start)
        except Exception as exc:  # messages may contain private data; retain class only
            stats['raises'][type(exc).__name__] += 1
            if stop_on_raise:
                return
        end = monotonic()
        # Reset from the latest start: never replay missed slots after an overrun.
        delay = max(0.0, start + interval - end) if _interval(start, end) else interval
        if not stop_event.is_set():
            wait(delay)


def _notifier_loop(notifier, pinger, *, binding, observer, wait, stop_event, stats):
    """Self-contained notifier scheduler; no dependency on the runtime side."""
    monotonic = observer.monotonic
    facade = _DeferredMark(pinger)
    prior = None

    def call(start):
        nonlocal prior
        facade.requested = False
        observer.begin()
        try:
            book_heartbeat.notifier_round_with_heartbeat(notifier, facade)
        except Exception:
            prior = None
            raise
        finally:
            reads, fault = observer.end()
            end = monotonic()
            if _interval(start, end):
                stats['max_duration_s'] = max(stats['max_duration_s'], end - start)
        shape = len(reads) == (3 if facade.requested else 2)
        sequence = (start, *reads, end)
        if fault or not shape or not all(_interval(a, b) for a, b in zip(sequence, sequence[1:])):
            prior = None
            stats['observation_faults'] += 1
            stats['marks_suppressed'] += 1
            return
        publish = reads[1]
        poll = publish - start
        stats['max_poll_s'] = max(stats['max_poll_s'], poll)
        duration_ok = end - start <= binding.max_round_duration_s
        poll_ok = poll <= binding.poll_bound_s
        previous = prior
        if previous is not None:
            # Rejected/loud passes replace the baseline; never measure only from last mark.
            prior = publish
            if not _interval(previous, publish):
                prior = None
                stats['observation_faults'] += 1
                spacing_ok = False
            else:
                gap = publish - previous
                stats['max_publish_gap_s'] = max(stats['max_publish_gap_s'], gap)
                spacing_ok = gap <= binding.max_notifier_loop_interval + binding.poll_bound_s
        else:
            spacing_ok = False
            if facade.requested and duration_ok and poll_ok:
                prior = publish
        if facade.requested and duration_ok and poll_ok and spacing_ok:
            facade.pinger.mark_progress()
            stats['marks_forwarded'] += 1
        else:
            stats['marks_suppressed'] += 1

    _schedule(call, interval=binding.notifier_interval_s, monotonic=monotonic,
              wait=wait, stop_event=stop_event, stats=stats, stop_on_raise=False)


class BookHost:
    """Run injected components independently. Construction starts no work."""

    def __init__(self, *, loop, notifier, read_status, runtime_pinger, notifier_pinger,
                 notifier_observer, binding=FROZEN_BINDING,
                 wall_clock=lambda: datetime.now(timezone.utc),
                 runtime_monotonic=time.monotonic, runtime_wait=None, notifier_wait=None):
        validate_binding(binding)
        config = notifier.config
        for name in ('max_jobs_per_round', 'retry_max_s', 'publish_timeout_s', 'max_retained_incidents'):
            if getattr(config, name, None) != getattr(binding, name):
                raise ValueError('notifier config mismatch: ' + name)
        if sorted(spec.kind for spec in config.channels) != sorted(binding.channel_kinds):
            raise ValueError('notifier channel kinds/count mismatch')
        if not isinstance(notifier_observer, NotifierClockObserver) or getattr(notifier, '_clock', None) is not notifier_observer:
            raise ValueError('notifier observer identity mismatch')
        if runtime_pinger is notifier_pinger or runtime_pinger._same_target(notifier_pinger):
            raise ValueError('runtime and notifier require independent pingers')
        for side, pinger in (('runtime', runtime_pinger), ('notifier', notifier_pinger)):
            expected = getattr(binding, side + '_ping')
            if any(getattr(pinger, name, None) != expected[name] for name in expected):
                raise ValueError(side + ' pinger binding mismatch')
        self.binding = binding
        self.loop, self.notifier, self.read_status = loop, notifier, read_status
        self.runtime_pinger, self.notifier_pinger = runtime_pinger, notifier_pinger
        self.notifier_observer = notifier_observer
        self.wall_clock, self.runtime_monotonic = wall_clock, runtime_monotonic
        self.stop_event = threading.Event()
        self.runtime_wait = runtime_wait or self.stop_event.wait
        self.notifier_wait = notifier_wait or self.stop_event.wait
        self.stats = {'runtime': _stats(), 'notifier': _stats()}
        self._threads = ()

    def run_runtime(self):
        facade = _DeferredMark(self.runtime_pinger)
        stats = self.stats['runtime']
        def call(start):
            facade.requested = False
            try:
                book_heartbeat.step_with_heartbeat(self.loop, facade, now=self.wall_clock(), read_status=self.read_status)
            finally:
                end = self.runtime_monotonic()
                if _interval(start, end):
                    stats['max_duration_s'] = max(stats['max_duration_s'], end - start)
            if facade.requested and _interval(start, end) and end - start <= self.binding.max_step_duration_s:
                facade.pinger.mark_progress()
                stats['marks_forwarded'] += 1
            else:
                stats['marks_suppressed'] += 1
                if not _interval(start, end):
                    stats['observation_faults'] += 1
        _schedule(call, interval=self.binding.step_interval_s, monotonic=self.runtime_monotonic,
                  wait=self.runtime_wait, stop_event=self.stop_event, stats=stats, stop_on_raise=True)

    def run_notifier(self):
        _notifier_loop(self.notifier, self.notifier_pinger, binding=self.binding,
                       observer=self.notifier_observer, wait=self.notifier_wait,
                       stop_event=self.stop_event, stats=self.stats['notifier'])

    def start(self):
        if self._threads or self.stop_event.is_set():
            raise ValueError('host cannot restart')
        self._threads = tuple(threading.Thread(target=target, name='book-host-' + side, daemon=True)
                              for side, target in (('runtime', self.run_runtime), ('notifier', self.run_notifier)))
        for thread in self._threads:
            thread.start()

    def stop(self, *, timeout_s=1.0):
        """Set stop; spend at most one total join budget and return unfinished sides."""
        _positive(timeout_s, 'join timeout')
        self.stop_event.set()
        deadline = time.monotonic() + timeout_s
        for thread in self._threads:
            if thread.ident is not None and thread is not threading.current_thread():
                thread.join(max(0.0, deadline - time.monotonic()))
        return tuple(thread.name for thread in self._threads if thread.is_alive())
