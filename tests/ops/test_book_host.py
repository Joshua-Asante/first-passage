"""Synthetic host qualification: no provider, account or deployment activity."""
from dataclasses import replace
import math

import pytest

from c1_signal_daemon import book_host as host
from c1_rail.book_incident_notifier import ESCALATION_STEP_S, NotifierConfig


def test_frozen_binding_and_digest():
    binding = host.FROZEN_BINDING
    host.validate_binding(binding)
    assert binding.max_round_duration_s == pytest.approx(38.4)
    assert binding.poll_bound_s == pytest.approx(2.1)
    assert binding.max_notifier_loop_interval == pytest.approx(39.4)
    assert binding.max_step_interval == 11
    assert host.ESCALATION_STEP_S == ESCALATION_STEP_S
    assert host.K_FLOOR == 8
    assert NotifierConfig.__dataclass_fields__['max_jobs_per_round'].default >= 8
    assert host.binding_digest(binding) == host.binding_digest(replace(binding))
    assert host.binding_digest(binding) != host.binding_digest(replace(binding, step_interval_s=9))


@pytest.mark.parametrize('side', ['runtime', 'notifier'])
@pytest.mark.parametrize('constraint', ['a', 'b', 'c'])
def test_binding_validator_refuses_constraint_breaches(side, constraint):
    binding = host.FROZEN_BINDING
    ping = dict(getattr(binding, side + '_ping'))
    if constraint == 'a':
        ping['timeout_s'] = ping['period_s']
        binding = replace(binding, **{side + '_ping': ping})
    elif constraint == 'b':
        interval = binding.max_step_interval if side == 'runtime' else binding.max_notifier_loop_interval
        duration = binding.max_step_duration_s if side == 'runtime' else binding.max_round_duration_s
        binding = replace(binding, **{side + '_timeout_s': ping['period_s'] + interval + duration + ping['timeout_s']})
    else:
        binding = replace(binding, **{side + '_timeout_s': 900 - binding.ingestion_allowance_s - binding.chain_s})
    with pytest.raises(ValueError, match=side + '.*' + constraint):
        host.validate_binding(binding)


def test_binding_d_and_e_are_independent():
    binding = host.FROZEN_BINDING
    with pytest.raises(ValueError, match='notifier.*d'):
        host.validate_binding(replace(binding, retry_max_s=60-binding.max_notifier_loop_interval-binding.poll_bound_s))
    with pytest.raises(ValueError, match='notifier.*e'):
        host.validate_binding(replace(binding, max_jobs_per_round=7))
    host.validate_binding(replace(binding, max_jobs_per_round=8))


@pytest.mark.parametrize('value', [0, -1, math.nan, math.inf, True])
@pytest.mark.parametrize('field', ['step_interval_s', 'max_step_duration_s', 'publish_timeout_s', 'owner_read_s', 'journal_s', 'parse_s', 'epsilon_s', 'scheduler_slack_s', 'max_retained_incidents'])
def test_binding_refuses_invalid_numbers(field, value):
    with pytest.raises(ValueError):
        host.validate_binding(replace(host.FROZEN_BINDING, **{field: value}))


def test_binding_copies_mutable_ping_and_redacts_invalid_reference():
    raw = dict(host.FROZEN_BINDING.runtime_ping)
    binding = replace(host.FROZEN_BINDING, runtime_ping=raw)
    raw['period_s'] = 999
    assert binding.runtime_ping['period_s'] == 12
    with pytest.raises(TypeError):
        binding.runtime_ping['period_s'] = 999
    with pytest.raises(ValueError) as error:
        host.validate_binding(replace(binding, runtime_ping={**raw, 'secret_ref': 'https://private.invalid/token'}))
    assert 'private.invalid' not in str(error.value)

# Host composition uses the real loop, owner, notifier and build_pingers factory.
import ast
from datetime import timedelta
import functools
import json
from pathlib import Path
import subprocess
import sys
import threading
import time

from c1_rail.book_account_owner import BookAccountOwner
from c1_rail.book_incident_notifier import ChannelSpec, FakeChannel, IncidentNotifier, NotifierStoreError
from c1_signal_daemon.book_heartbeat import build_pingers
from c1_signal_daemon.book_runtime import FourLegRuntime
from test_book_loop_continuation import loop_for
from test_book_heartbeat import FakeClock, Receiver
from test_four_leg_runtime import NOW, inert_adapters, owner


@pytest.fixture
def rig(tmp_path):
    runtime_clock, notifier_clock = FakeClock(), FakeClock()
    receivers = [Receiver(runtime_clock), Receiver(notifier_clock)]
    binding = host.FROZEN_BINDING
    # build_pingers accepts one callable: dispatch by the two host thread names.
    def ping_clock():
        return (notifier_clock if threading.current_thread().name == 'book-host-notifier' else runtime_clock)()
    pingers = build_pingers(binding.runtime_ping, binding.notifier_ping,
        environ={binding.runtime_ping['secret_ref'][4:]: receivers[0].url,
                 binding.notifier_ping['secret_ref'][4:]: receivers[1].url},
        allow_loopback_http=True, clock=ping_clock)
    account = owner(tmp_path, [])
    loop = loop_for(FourLegRuntime(account, inert_adapters()))
    observer = host.NotifierClockObserver(lambda: NOW + timedelta(seconds=notifier_clock()), monotonic=notifier_clock)
    specs = (ChannelSpec('page', 'grafana_irm', 'env:FAKE_PAGE'), ChannelSpec('file', 'local_file'))
    channels = {spec.name: FakeChannel(spec.name) for spec in specs}
    for spec in specs:
        channels[spec.name].kind = spec.kind
    config = NotifierConfig(specs, publish_timeout_s=2, retry_max_s=10, max_jobs_per_round=8)
    notifier = IncidentNotifier(tmp_path / 'notifier.sqlite', read_incidents=functools.partial(BookAccountOwner.read_incidents, account.path),
                                channels=channels, config=config, clock=observer)
    book = host.BookHost(loop=loop, notifier=notifier, read_status=account.status,
                         runtime_pinger=pingers[0], notifier_pinger=pingers[1],
                         notifier_observer=observer, binding=binding,
                         wall_clock=lambda: NOW, runtime_monotonic=runtime_clock)
    yield book, loop, notifier, account, pingers, receivers, runtime_clock, notifier_clock
    book.stop(timeout_s=1)
    for receiver in receivers:
        receiver.close()


def run_rounds(book, clock, count, gaps=None):
    calls = 0
    def wait(seconds):
        nonlocal calls
        calls += 1
        if calls == count:
            book.stop_event.set()
        else:
            clock.advance(gaps[calls-1] if gaps else seconds)
    book.notifier_wait = wait
    book.run_notifier()


def test_first_pass_seeds_then_marks_after_wrapper_returns(rig, monkeypatch):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks, in_call = [], []
    original = notifier.run_once
    def call():
        in_call.append(True)
        original()
        in_call.pop()
    def mark():
        assert not in_call
        marks.append(clock())
    monkeypatch.setattr(notifier, 'run_once', call)
    monkeypatch.setattr(pingers[1], 'mark_progress', mark)
    run_rounds(book, clock, 3)
    assert marks == [10, 20]
    assert notifier.progress() == 3


@pytest.mark.parametrize('kind,value,want', [
    ('duration', 38.4, True), ('duration', 38.4001, False),
    ('poll', 2.1, True), ('poll', 2.1001, False),
    ('spacing', 41.5, True), ('spacing', 41.5001, False),
    ('poll', 20, False),
])
def test_notifier_three_gates_independently(rig, monkeypatch, kind, value, want):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks = []
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    original_reader, original_run = notifier._read_incidents, notifier.run_once
    rounds = 0
    def reader():
        if rounds == 2 and kind == 'poll':
            clock.advance(value)
        return original_reader()
    def run():
        nonlocal rounds
        rounds += 1
        original_run()
        if rounds == 2 and kind == 'duration':
            clock.advance(value)
    monkeypatch.setattr(notifier, '_read_incidents', reader)
    monkeypatch.setattr(notifier, 'run_once', run)
    run_rounds(book, clock, 2, gaps=[value if kind == 'spacing' else 0])
    assert bool(marks) is want
    assert notifier.progress() == 2  # a rejected host mark must not rewind NF6


def test_rejected_spacing_becomes_next_baseline(rig, monkeypatch):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks = []
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    run_rounds(book, clock, 3, gaps=[42, 10])
    assert marks == [52]
    assert notifier.progress() == 3


@pytest.mark.parametrize('failure', ['raise', 'extra', 'missing', 'backward', 'nan'])
def test_bad_observation_resets_first_pass_rule(rig, monkeypatch, failure):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks, rounds = [], 0
    original = notifier.run_once
    def run():
        nonlocal rounds
        rounds += 1
        if rounds == 2 and failure == 'raise':
            raise RuntimeError('https://must-not-appear.invalid')
        if rounds == 2 and failure == 'missing':
            return
        original()
        if rounds == 2:
            if failure == 'extra':
                notifier._clock()
            elif failure == 'backward':
                clock.advance(-1)
            elif failure == 'nan':
                clock.t = math.nan
    def wait(seconds):
        clock.t = rounds * 10
        if rounds == 4:
            book.stop_event.set()
    book.notifier_wait = wait
    monkeypatch.setattr(notifier, 'run_once', run)
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    book.run_notifier()
    assert marks == [30]
    assert 'must-not-appear' not in repr(book.stats)


def test_backward_wall_clock_and_outside_reads_do_not_gate(rig, monkeypatch):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks = []
    book.notifier_observer.wall_clock = lambda: NOW - timedelta(seconds=clock())
    notifier._clock()  # out of invocation reads do not select an ordinal
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    run_rounds(book, clock, 3)
    assert marks == [10, 20]
    assert notifier.liveness() == NOW - timedelta(seconds=20)


@pytest.mark.parametrize('field,value', [('max_jobs_per_round', 9), ('retry_max_s', 11), ('publish_timeout_s', 3), ('max_retained_incidents', 999)])
def test_host_refuses_notifier_config_mismatch(rig, field, value):
    book, loop, notifier, account, pingers, *_ = rig
    notifier.config = replace(notifier.config, **{field: value})
    with pytest.raises(ValueError, match='notifier'):
        host.BookHost(loop=loop, notifier=notifier, read_status=account.status, runtime_pinger=pingers[0],
                      notifier_pinger=pingers[1], notifier_observer=book.notifier_observer)


def test_host_refuses_unrelated_observer(rig):
    book, loop, notifier, account, pingers, *_ = rig
    with pytest.raises(ValueError, match='observer'):
        host.BookHost(loop=loop, notifier=notifier, read_status=account.status, runtime_pinger=pingers[0],
                      notifier_pinger=pingers[1], notifier_observer=host.NotifierClockObserver(lambda: NOW))


@pytest.mark.parametrize('duration,want', [(10, True), (10.001, False)])
def test_runtime_mark_waits_for_complete_step_and_status(rig, monkeypatch, duration, want):
    book, loop, _, account, pingers, _, clock, _ = rig
    marks = []
    original = account.status
    def status():
        clock.advance(duration)
        assert marks == []
        return original()
    book.read_status = status
    book.runtime_wait = lambda _: book.stop_event.set()
    monkeypatch.setattr(pingers[0], 'mark_progress', lambda: marks.append(clock()))
    book.run_runtime()
    assert bool(marks) is want


def test_host_import_and_scope_boundary():
    root = Path(__file__).resolve().parents[2]
    path = root / 'ops/c1_signal_daemon/book_host.py'
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    allowed = {'c1_signal_daemon', 'c1_rail.book_protection_owner'}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.module in allowed or node.module.split('.')[0] in sys.stdlib_module_names
        if isinstance(node, ast.Import):
            assert all(n.name.split('.')[0] in sys.stdlib_module_names for n in node.names)
        if isinstance(node, ast.Name):
            assert node.id not in {'dry_run', 'armed_until'}
    forbidden = ['c1_signal_daemon.daemon', 'c1_signal_daemon.__main__', 'c1_signal_daemon.listener_client',
                 'c1_rail.book_incident_notifier', 'c1_rail.book_incident_grafana_irm', 'c1_rail.c1_rail_arm',
                 'c1_rail.write_volume_config', 'c1_rail.c1_rail_listener', 'c1_rail.c1_rail_http_server', 'c1_rail.crosstrade_payload']
    code = 'import sys,json;sys.path.insert(0,' + repr(str(root/'ops')) + ');import c1_signal_daemon.book_host;print(json.dumps(sorted(sys.modules)))'
    result = subprocess.run([sys.executable, '-I', '-c', code], capture_output=True, text=True, check=True)
    assert not set(forbidden).intersection(json.loads(result.stdout))
    for name in ['ops/c1_signal_daemon/daemon.py', 'ops/c1_signal_daemon/__main__.py', 'tests/ops/test_c1_signal_daemon_image_manifest.py']:
        assert 'book_host' not in (root / name).read_text()


def _paced_threads(book, pingers, clocks, target=55):
    """Advance independent virtual clocks, but settle real loopback transport first."""
    ready = [threading.Event(), threading.Event()]
    release = threading.Event()
    counts = [0, 0]
    def make_wait(side):
        def wait(seconds):
            assert pingers[side]._idle.wait(3)
            counts[side] += 1
            if counts[side] >= target:
                ready[side].set()
                release.wait(8)
            else:
                clocks[side].advance(seconds)
                time.sleep(0)  # yield the GIL, not a fake clock increment
        return wait
    book.runtime_wait, book.notifier_wait = make_wait(0), make_wait(1)
    return ready, release


def test_step_and_notifier_run_on_separate_threads(rig, monkeypatch):
    book, loop, notifier, _, pingers, receivers, rc, nc = rig
    ids = [set(), set()]
    step, run = loop.step, notifier.run_once
    def runtime(**kwargs):
        ids[0].add(threading.get_ident())
        return step(**kwargs)
    def notify():
        ids[1].add(threading.get_ident())
        return run()
    monkeypatch.setattr(loop, 'step', runtime)
    monkeypatch.setattr(notifier, 'run_once', notify)
    ready, release = _paced_threads(book, pingers, (rc, nc))
    try:
        book.start()
        assert all(event.wait(8) for event in ready)
        assert len(ids[0]) == len(ids[1]) == 1
        assert ids[0].isdisjoint(ids[1])
        assert not receivers[0].expired(60)
        assert not receivers[1].expired(120)
    finally:
        release.set()
        assert book.stop(timeout_s=2) == ()


@pytest.mark.parametrize('source', ['run_once', 'reader'])
def test_raising_notifier_leaves_step_cadence_bounded(rig, monkeypatch, source, caplog):
    book, _, notifier, account, pingers, receivers, rc, nc = rig
    def fail():
        raise NotifierStoreError('https://sensitive.invalid/never-log')
    monkeypatch.setattr(notifier, 'run_once' if source == 'run_once' else '_read_incidents', fail)
    ready, release = _paced_threads(book, pingers, (rc, nc))
    began = time.monotonic()
    try:
        book.start()
        assert all(event.wait(8) for event in ready)
        assert time.monotonic() - began < 10
        assert book.stats['runtime']['calls_started'] >= 50
        assert book.stats['runtime']['max_start_gap_s'] <= 11
        assert book.stats['notifier']['raises']['NotifierStoreError'] >= 50
        assert not receivers[0].expired(60)
        assert receivers[1].expired(120)
        assert 'sensitive.invalid' not in caplog.text + repr(book.stats)
        account.status()  # independent owner store remains readable
    finally:
        release.set()
        book.stop(timeout_s=2)


def test_hung_notifier_leaves_step_cadence_bounded(rig, monkeypatch):
    book, _, notifier, _, pingers, receivers, rc, nc = rig
    held, entered = threading.Event(), threading.Event()
    original = notifier.run_once
    def hang():
        entered.set()
        assert held.wait(8)
        original()
    monkeypatch.setattr(notifier, 'run_once', hang)
    ready, release = _paced_threads(book, pingers, (rc, nc))
    try:
        began = time.monotonic()
        book.start()
        assert entered.wait(2) and ready[0].wait(8)
        assert time.monotonic() - began < 10
        nc.advance(121)
        assert receivers[1].expired(120) and not receivers[0].expired(60)
        assert book.stats['runtime']['calls_started'] >= 50
        assert book.stats['runtime']['max_start_gap_s'] <= 11
        release.set()
        stop_start = time.monotonic()
        assert 'book-host-notifier' in book.stop(timeout_s=.05)
        assert time.monotonic() - stop_start < .5
        assert book.stats['notifier']['marks_forwarded'] == 0
    finally:
        held.set()
        release.set()
        assert book.stop(timeout_s=2) == ()
    assert book.stats['notifier']['marks_forwarded'] == 0  # no late mark
    assert book.stats['notifier']['calls_started'] == 1


@pytest.mark.parametrize('mode', ['hang', 'step_raise', 'status_raise', 'stop_steps'])
def test_hq7_through_host_runtime_stalled_notifier_alive(rig, monkeypatch, mode):
    book, loop, _, account, pingers, receivers, rc, nc = rig
    held, entered = threading.Event(), threading.Event()
    before = account.status(), account.incidents
    calls = 0
    original = loop.step
    def fail():
        raise RuntimeError('private failure text')
    def step(**kwargs):
        nonlocal calls
        calls += 1
        entered.set()
        if mode == 'step_raise':
            fail()
        if mode == 'hang':
            assert held.wait(8)
        return original(**kwargs)
    monkeypatch.setattr(loop, 'step', step)
    if mode == 'status_raise':
        book.read_status = fail
    ready, release = _paced_threads(book, pingers, (rc, nc))
    if mode == 'stop_steps':
        book.runtime_wait = lambda _: (entered.set(), release.wait(8))
    try:
        book.start()
        assert entered.wait(2) and ready[1].wait(8)
        assert pingers[0]._idle.wait(2)
        rc.advance(61)
        assert receivers[0].expired(60)
        assert not receivers[1].expired(120)
        assert (account.status(), account.incidents) == before
        assert calls == 1
        if mode != 'stop_steps':
            assert book.stats['runtime']['marks_forwarded'] == 0
    finally:
        held.set()
        release.set()
        assert book.stop(timeout_s=2) == ()
    if mode == 'hang':
        assert book.stats['runtime']['marks_forwarded'] == 0


def test_late_clock_return_and_round_lock_delay_are_in_poll_gate(rig, monkeypatch):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks, reads = [], 0
    original_clock = book.notifier_observer.wall_clock
    def wall():
        nonlocal reads
        reads += 1
        if reads == 5:  # second clock of second run: delay inside the wall clock
            clock.advance(2.101)
        return original_clock()
    book.notifier_observer.wall_clock = wall
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    run_rounds(book, clock, 3)
    assert marks == [20]
    assert book.stats['notifier']['max_poll_s'] == pytest.approx(2.101)


def test_round_lock_wait_is_before_second_observation(rig, monkeypatch):
    book, _, notifier, _, pingers, _, _, clock = rig
    marks, entered = [], threading.Event()
    original_poll = notifier.poll
    def poll():
        result = original_poll()
        entered.set()
        return result
    monkeypatch.setattr(notifier, 'poll', poll)
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    notifier._round_lock.acquire()
    worker = threading.Thread(target=lambda: run_rounds(book, clock, 1))
    try:
        worker.start()
        assert entered.wait(2)
        clock.advance(20)
    finally:
        notifier._round_lock.release()
        worker.join(3)
    assert not worker.is_alive()
    assert marks == []
    assert book.stats['notifier']['max_poll_s'] == 20


def test_reentrant_same_thread_read_is_a_contract_fault(rig, monkeypatch):
    book, _, notifier, _, pingers, _, _, clock = rig
    original, reentered, marks = book.notifier_observer.wall_clock, False, []
    def wall():
        nonlocal reentered
        if not reentered:
            reentered = True
            notifier._clock()
        return original()
    book.notifier_observer.wall_clock = wall
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    run_rounds(book, clock, 3)
    assert marks == [20]  # faulty first pass, clean seed, then a mark
    assert book.stats['notifier']['observation_faults'] == 1


def test_loud_pass_replaces_baseline_without_mark(rig, monkeypatch):
    book, _, notifier, account, pingers, _, _, clock = rig
    marks, round_number = [], 0
    original = notifier.run_once
    def run():
        nonlocal round_number
        round_number += 1
        if round_number == 2:
            # Nine independently halted sequences exceed k=8: real NF3 loud pass.
            for i in range(9):
                account.halt('host-loud-' + str(i), 'operator', now=NOW)
        original()
    monkeypatch.setattr(notifier, 'run_once', run)
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    run_rounds(book, clock, 4, gaps=[42, 10, 10])
    assert marks == [52, 62]
    assert notifier.progress() == 3
    assert any(event['kind'] == 'cap_deferred' for event in notifier.events())


def test_late_worker_and_record_delivery_reads_do_not_shift_observation(rig, monkeypatch):
    book, _, notifier, account, pingers, _, _, clock = rig
    channel = notifier._channels[0]
    channel.outcomes = [FakeChannel.HANG]
    account.halt('host-late', 'operator', now=NOW)
    marks, workers, original_late = [], [], notifier._record_late
    def late(*args, **kwargs):
        workers.append(threading.current_thread())
        return original_late(*args, **kwargs)
    monkeypatch.setattr(notifier, '_record_late', late)
    original_run = notifier.run_once
    rounds = 0
    def run():
        nonlocal rounds
        rounds += 1
        original_run()
        if rounds == 1:
            channel.release()
            deadline = time.monotonic() + 3
            while not workers and time.monotonic() < deadline:
                time.sleep(.001)
            assert workers
            workers[0].join(3)
            assert not workers[0].is_alive()
    monkeypatch.setattr(notifier, 'run_once', run)
    monkeypatch.setattr(pingers[1], 'mark_progress', lambda: marks.append(clock()))
    try:
        run_rounds(book, clock, 3)
        assert marks == [10, 20]
        assert book.stats['notifier']['observation_faults'] == 0
        assert all(worker.ident != threading.get_ident() for worker in workers)
        # This real public callback reads the clock outside the host invocation.
        key = notifier.jobs()[0]['incident_key']
        notifier.record_delivery(key, channel.name, 'e' * 64)
        assert book.stats['notifier']['observation_faults'] == 0
    finally:
        channel.release()


def test_measured_step_and_round_within_declared_bounds(rig, tmp_path, monkeypatch):
    """HH7: bounded synthetic history, 200 real-clock calls/side, >=20 saturated rounds."""
    from c1_rail.book_incident_notifier import PublishResult
    book, loop, _, account, _, receivers, *_ = rig
    binding = replace(host.FROZEN_BINDING, step_interval_s=.005, max_step_duration_s=.15,
                      notifier_interval_s=.005, scheduler_slack_s=.25, publish_timeout_s=.005,
                      owner_read_s=.3, parse_s=.3, journal_s=.1, epsilon_s=1,
                      retry_max_s=.01, max_retained_incidents=8,
                      runtime_timeout_s=5, notifier_timeout_s=15,
                      runtime_ping={**host.FROZEN_BINDING.runtime_ping, 'period_s': .5, 'timeout_s': .2},
                      notifier_ping={**host.FROZEN_BINDING.notifier_ping, 'period_s': .5, 'timeout_s': .2})
    pingers = build_pingers(binding.runtime_ping, binding.notifier_ping, allow_loopback_http=True,
                           environ={binding.runtime_ping['secret_ref'][4:]: receivers[0].url,
                                    binding.notifier_ping['secret_ref'][4:]: receivers[1].url})
    history_dir = tmp_path / 'history'
    history_dir.mkdir()
    history_owner = owner(history_dir, [])
    for i in range(binding.max_retained_incidents):
        history_owner.halt('host-measure-' + str(i), 'operator', now=NOW)
    assert len(BookAccountOwner.read_incidents(history_owner.path)) == 8
    wall = [NOW]
    observer = host.NotifierClockObserver(lambda: wall[0])
    class HeldChannel(FakeChannel):
        def publish(self, key, payload):
            self.calls.append((key, dict(payload)))
            time.sleep(binding.publish_timeout_s)
            return PublishResult('rejected')
    channels = [HeldChannel('page'), HeldChannel('file')]
    channels[0].kind, channels[1].kind = binding.channel_kinds
    config = NotifierConfig((ChannelSpec('page', 'grafana_irm', 'env:FAKE_PAGE'), ChannelSpec('file', 'local_file')),
                            publish_timeout_s=binding.publish_timeout_s, retry_initial_s=.01, retry_max_s=.01,
                            max_jobs_per_round=8, max_retained_incidents=8)
    notifier = IncidentNotifier(history_dir / 'notifier.sqlite',
        read_incidents=functools.partial(BookAccountOwner.read_incidents, history_owner.path),
        channels={c.name:c for c in channels}, config=config, clock=observer)
    notifier.poll()  # history is already retained before measurement begins
    assert len(notifier.jobs()) == binding.max_retained_incidents
    samples, starts, saturated = [[], []], [[], []], []
    original_step = host.book_heartbeat.step_with_heartbeat
    original_round = host.book_heartbeat.notifier_round_with_heartbeat
    def step(*args, **kwargs):
        start = time.monotonic()
        starts[0].append(start)
        try:
            return original_step(*args, **kwargs)
        finally:
            samples[0].append(time.monotonic() - start)
    def round_call(*args, **kwargs):
        start = time.monotonic()
        starts[1].append(start)
        before = [job['rounds'] for job in notifier.jobs()]
        try:
            return original_round(*args, **kwargs)
        finally:
            samples[1].append(time.monotonic() - start)
            after = [job['rounds'] for job in notifier.jobs()]
            saturated.append(sum(b > a for a, b in zip(before, after)))
    monkeypatch.setattr(host.book_heartbeat, 'step_with_heartbeat', step)
    monkeypatch.setattr(host.book_heartbeat, 'notifier_round_with_heartbeat', round_call)
    measured = host.BookHost(loop=loop, notifier=notifier, read_status=account.status,
        runtime_pinger=pingers[0], notifier_pinger=pingers[1], notifier_observer=observer,
        binding=binding, wall_clock=lambda: NOW)
    ready = [threading.Event(), threading.Event()]
    def wait(side, seconds):
        if side == 1 and len(samples[1]) <= 20:
            # Enough wall-clock advance to keep all eight rejected jobs due.
            wall[0] += timedelta(seconds=1)
        if len(samples[side]) >= 200:
            ready[side].set()
            measured.stop_event.wait(30)
        else:
            measured.stop_event.wait(seconds)
    measured.runtime_wait = lambda seconds: wait(0, seconds)
    measured.notifier_wait = lambda seconds: wait(1, seconds)
    try:
        measured.start()
        assert all(event.wait(30) for event in ready)
    finally:
        assert measured.stop(timeout_s=3) == ()
    report = {}
    for side, name in enumerate(('runtime', 'notifier')):
        ordered = sorted(samples[side])
        report[name] = {'count': len(ordered), 'maximum_s': max(ordered),
                        'p99_s': ordered[math.ceil(.99 * len(ordered))-1],
                        'maximum_start_gap_s': max(b-a for a,b in zip(starts[side], starts[side][1:]))}
        assert len(ordered) >= 200
        assert not measured.stats[name]['raises']
    report['saturated_rounds'] = sum(value == 8 for value in saturated)
    report['max_poll_s'] = measured.stats['notifier']['max_poll_s']
    report['max_publish_gap_s'] = measured.stats['notifier']['max_publish_gap_s']
    report['binding_digest'] = host.binding_digest(binding)
    print('HH7_MEASUREMENTS=' + json.dumps(report, sort_keys=True))
    assert report['saturated_rounds'] >= 20
    assert report['runtime']['maximum_s'] <= binding.max_step_duration_s
    assert measured.stats['runtime']['max_duration_s'] <= binding.max_step_duration_s
    assert report['runtime']['maximum_start_gap_s'] <= binding.max_step_interval
    assert report['notifier']['maximum_s'] <= binding.max_round_duration_s
    assert measured.stats['notifier']['max_duration_s'] <= binding.max_round_duration_s
    assert measured.stats['notifier']['max_start_gap_s'] <= binding.max_notifier_loop_interval
    assert report['max_poll_s'] <= binding.poll_bound_s
    assert report['max_publish_gap_s'] <= binding.max_notifier_loop_interval + binding.poll_bound_s



def test_overrun_runs_once_immediately_then_resumes_fixed_rate(rig, monkeypatch):
    book, loop, _, _, pingers, _, clock, _ = rig
    starts, marks, waits = [], [], []
    original = loop.step
    def step(**kwargs):
        starts.append(clock())
        result = original(**kwargs)
        if len(starts) == 1:
            clock.advance(35)
        return result
    def wait(seconds):
        waits.append(seconds)
        if len(starts) == 3:
            book.stop_event.set()
        else:
            clock.advance(seconds)
    book.runtime_wait = wait
    monkeypatch.setattr(loop, 'step', step)
    monkeypatch.setattr(pingers[0], 'mark_progress', lambda: marks.append(clock()))
    book.run_runtime()
    assert starts == [0, 35, 45]
    assert marks == [35, 45]
    assert waits == [0, 10, 10]


@pytest.mark.parametrize('kinds', [('grafana_irm', 'grafana_irm'), ('grafana_irm',)])
def test_host_refuses_channel_kind_or_count_mismatch(rig, kinds):
    book, loop, notifier, account, pingers, *_ = rig
    notifier.config = replace(notifier.config, channels=tuple(
        ChannelSpec('c' + str(i), kind, 'env:FAKE_REF') for i,kind in enumerate(kinds)))
    with pytest.raises(ValueError, match='notifier channel'):
        host.BookHost(loop=loop, notifier=notifier, read_status=account.status,
                      runtime_pinger=pingers[0], notifier_pinger=pingers[1], notifier_observer=book.notifier_observer)
