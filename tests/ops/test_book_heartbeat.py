"""Missed-heartbeat monitor for the book runtime and notifier (D-MON-1 heartbeat card).

Card: docs/briefs/handoffs/2026-10-03-dmon-missed-heartbeat-monitor-card-DRAFT.md (FROZEN
2026-10-05), §6.1 H1-H12 and §6.2 HQ1-HQ10. Every send goes to a loopback fake receiver on
127.0.0.1 with the fixture token ``fake-token``; nothing leaves the host. Each receiver
expires after its T on a fake monotonic clock that the pinger shares. The evidence class is
*Synthetic / replay engineering*: HB-L1 and HB-L2 stay owed to Joshua (card §6.3).
"""
from __future__ import annotations

import ast
from datetime import timedelta
import functools
import http.server
import io
import logging
from pathlib import Path
import socket
import threading
import time

import pytest

from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner
from c1_rail.book_incident_notifier import (
    FakeChannel,
    IncidentNotifier,
    NotifierConfig,
    NotifierStoreError,
    PublishResult,
)
from c1_signal_daemon import book_heartbeat
from c1_signal_daemon import book_heartbeat_live_check
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from c1_signal_daemon.book_heartbeat import (
    HeartbeatConfigError,
    HeartbeatPinger,
    build_pingers,
    notifier_round_with_heartbeat,
    step_with_heartbeat,
)
from c1_signal_daemon.book_runtime import FourLegRuntime
from test_four_leg_runtime import LEGS, NOW, inert_adapters, owner


ROOT = Path(__file__).resolve().parents[2]
MODULES = (ROOT / "ops" / "c1_signal_daemon" / "book_heartbeat.py",
           ROOT / "ops" / "c1_signal_daemon" / "book_heartbeat_live_check.py")
PATH = "/integrations/v1/formatted_webhook/fake-token/heartbeat/"
TOKEN = "fake-token"
REF, REF_N = "env:FP_TEST_HEARTBEAT_URL", "env:FP_TEST_NOTIFIER_HEARTBEAT_URL"
SETTLE = 5.0  # wall-clock bound for one loopback send to finish


class FakeClock:
    """The pinger's monotonic clock; the receivers stamp arrivals with the same value."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


class Receiver:
    """Loopback heartbeat endpoint: records arrivals on the fake clock; expires after T."""

    def __init__(self, clock, *, mode="ok"):
        self.clock = clock
        self.mode = mode
        self.arrivals = []
        self.requests = []
        self.release = threading.Event()
        receiver = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):  # noqa: ARG002 - keep test output clean
                return

            def do_POST(self):  # noqa: N802 - http.server naming
                length = int(self.headers.get("Content-Length") or 0)
                self.rfile.read(length)
                receiver.requests.append((self.command, self.path))
                if receiver.mode == "hang":
                    receiver.release.wait(SETTLE)
                    return
                if receiver.mode == "drip_headers":  # headers trickle one byte per 50 ms
                    for byte in b"HTTP/1.1 200 OK\r\nX-Slow: " + b"x" * 1000:
                        if receiver.release.wait(0.05):
                            return
                        try:
                            self.wfile.write(bytes([byte]))
                            self.wfile.flush()
                        except OSError:
                            return
                    return
                if receiver.mode == "drip":  # a 200 that trickles one byte per 50 ms
                    self.send_response(200)
                    self.send_header("Content-Length", "1000")
                    self.end_headers()
                    for _ in range(1000):
                        if receiver.release.wait(0.05):
                            return
                        try:
                            self.wfile.write(b"x")
                            self.wfile.flush()
                        except OSError:
                            return
                    return
                if receiver.mode == "redirect":
                    self.send_response(302)
                    self.send_header("Location", "/elsewhere/heartbeat/")
                    self.end_headers()
                    return
                if isinstance(receiver.mode, int):
                    self.send_response(receiver.mode)
                    self.end_headers()
                    return
                if self.path == PATH:
                    receiver.arrivals.append(receiver.clock())
                self.send_response(200)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"ok")

            do_GET = do_POST

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = "http://127.0.0.1:%d%s" % (self.server.server_address[1], PATH)
        self.start = clock()

    def expired(self, ttl):
        last = self.arrivals[-1] if self.arrivals else self.start
        return self.clock() - last > ttl

    def close(self):
        self.release.set()
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def receivers(clock):
    made = []

    def make(**kwargs):
        receiver = Receiver(clock, **kwargs)
        made.append(receiver)
        return receiver

    yield make
    for receiver in made:
        receiver.close()


def _pinger(url, clock, *, ref=REF, period=50.0, timeout=1.0):
    return HeartbeatPinger(ref, period_s=period, timeout_s=timeout, clock=clock,
                           environ={ref.partition(":")[2]: url}, allow_loopback_http=True)


def _closed_port_url():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    return "http://127.0.0.1:%d%s" % (port, PATH)


class StubLoop:
    def __init__(self, calls, error=None):
        self.calls, self.error = calls, error

    def step(self, *, now):
        self.calls.append(("step", now))
        if self.error:
            raise self.error
        return ("dispatch", now)


def _real_loop(tmp_path):
    account = owner(tmp_path, [])

    class Source:
        def poll(self):
            return None

    loop = FourLegEvaluateLoop(sources={leg: Source() for leg in LEGS},
                               runtime=FourLegRuntime(account, inert_adapters()))
    return account, loop


def _owner_view(account):
    return account.status(), account.incidents


class NotifierClock:
    def __init__(self, at=NOW):
        self.at = at

    def __call__(self):
        return self.at

    def advance(self, seconds):
        self.at += timedelta(seconds=seconds)


def _notifier(tmp_path, read_incidents, channel=None, *, k=10, clock=None):
    channel = channel or FakeChannel("primary")
    config = NotifierConfig.from_mapping({
        "channels": [{"name": channel.name, "kind": "fake", "secret_ref": "env:PRIMARY_REF"}],
        "publish_timeout_s": 1.0, "retry_initial_s": 5.0, "retry_max_s": 30.0,
        "max_jobs_per_round": k})
    return IncidentNotifier(tmp_path / "journal.sqlite", read_incidents=read_incidents,
                            channels={channel.name: channel}, config=config,
                            clock=clock or NotifierClock())


def _runtime_step(loop, pinger, clock, account):
    return step_with_heartbeat(loop, pinger, now=NOW + timedelta(seconds=clock()),
                               read_status=account.status)


def _settle(*pingers):
    for pinger in pingers:
        assert pinger.drain(SETTLE)


# -- §6.1 unit tests ----------------------------------------------------------------------------

def test_ping_only_after_step_and_status_succeed(clock, receivers):  # H1
    receiver = receivers()
    pinger = _pinger(receiver.url, clock)
    calls = []

    def read_status():
        calls.append(("status", len(receiver.requests)))
        return {"authority": "NORMAL"}

    result = step_with_heartbeat(StubLoop(calls), pinger, now="t0", read_status=read_status)
    _settle(pinger)
    assert result == ("dispatch", "t0")
    assert calls == [("step", "t0"), ("status", 0)]
    assert receiver.requests == [("POST", PATH)]
    assert receiver.arrivals == [0.0]


@pytest.mark.parametrize("where", ["step", "status"])
def test_no_mark_when_step_or_status_raises(clock, receivers, where):  # H2
    receiver = receivers()
    pinger = _pinger(receiver.url, clock)
    error = AccountOwnerError("owner storage unavailable")
    calls = []

    def read_status():
        calls.append(("status",))
        raise error

    loop = StubLoop(calls, error if where == "step" else None)
    with pytest.raises(AccountOwnerError) as raised:
        step_with_heartbeat(loop, pinger, now="t0",
                            read_status=read_status if where == "status" else dict)
    assert raised.value is error
    _settle(pinger)
    assert receiver.requests == []
    assert pinger.stats()["sends_started"] == 0


@pytest.mark.parametrize("authority", ["HALTED", "INTERVENTION"])
def test_intervention_and_halted_still_mark_progress(tmp_path, clock, receivers, authority):  # H3
    receiver = receivers()
    pinger = _pinger(receiver.url, clock)
    account, loop = _real_loop(tmp_path)
    if authority == "INTERVENTION":
        clock.advance(3600)  # source silence beyond 2 * bar_period + 30 s halts the whole book
        loop.step(now=NOW + timedelta(seconds=clock()))
    else:
        account.halt("operator-stop:synthetic", "operator", now=NOW + timedelta(seconds=1))
    assert account.authority in ("HALTED", "INTERVENTION")
    clock.advance(1)
    _runtime_step(loop, pinger, clock, account)
    _settle(pinger)
    assert receiver.arrivals == [clock()]


def test_rate_limited_to_one_send_per_period(clock, receivers):  # H4
    receiver = receivers()
    pinger = _pinger(receiver.url, clock, period=50.0)
    for _ in range(201):
        pinger.mark_progress()
        _settle(pinger)
        clock.advance(1)
    assert receiver.arrivals == [0.0, 50.0, 100.0, 150.0, 200.0]
    hanging = receivers(mode="hang")
    stuck = _pinger(hanging.url, clock, period=1.0, timeout=0.5)
    for _ in range(20):
        stuck.mark_progress()
        clock.advance(5)
    assert len(hanging.requests) <= 1
    hanging.release.set()
    _settle(stuck)
    time.sleep(0.2)
    assert len(hanging.requests) == 1  # nothing was queued behind the in-flight send


def test_sends_stop_when_progress_stops(clock, receivers):  # H5
    receiver = receivers()
    pinger = _pinger(receiver.url, clock, period=20.0)
    for _ in range(11):
        pinger.mark_progress()
        _settle(pinger)
        clock.advance(10)
    last_mark = clock() - 10
    clock.advance(1000)
    time.sleep(0.3)
    assert receiver.arrivals[-1] <= last_mark
    assert all(at <= last_mark for at in receiver.arrivals)
    assert not any(thread.name.startswith("book-heartbeat") for thread in threading.enumerate())


@pytest.mark.parametrize("mode", ["hang", 302, 404, 500, "refused"])
def test_send_failure_never_blocks_or_raises(clock, receivers, caplog, mode):  # H6
    if mode == "refused":
        url = _closed_port_url()
    else:
        url = receivers(mode=mode).url
    pinger = _pinger(url, clock, period=1.0, timeout=0.3)
    caplog.set_level(logging.DEBUG)
    for _ in range(3):
        started = time.monotonic()
        pinger.mark_progress()
        assert time.monotonic() - started < 0.05
        _settle(pinger)
        clock.advance(2)
    stats = pinger.stats()
    assert stats["sends_failed"] == 3 and stats["sends_ok"] == 0
    assert stats["last_outcome"] and stats["last_outcome"].isidentifier()
    text = caplog.text
    assert "heartbeat send failed" in text
    assert TOKEN not in text and "127.0.0.1" not in text and PATH not in text


@pytest.mark.parametrize("mode", ["drip", "drip_headers"])
def test_send_deadline_covers_the_whole_operation(clock, receivers, mode):  # H6 (#701 P2)
    # A byte before every socket timeout, in the body or the headers, must still end at
    # timeout_s.
    receiver = receivers(mode=mode)
    pinger = _pinger(receiver.url, clock, period=0.4, timeout=0.2)
    started = time.monotonic()
    pinger.mark_progress()
    assert pinger.drain(1.0)
    assert time.monotonic() - started < 0.6
    stats = pinger.stats()
    assert stats["sends_failed"] == 1 and stats["sends_ok"] == 0 and not stats["in_flight"]
    clock.advance(0.5)
    pinger.mark_progress()  # the slot is free again: a second send starts
    assert pinger.stats()["sends_started"] == 2
    assert pinger.drain(1.0)


def test_secret_ref_resolution_and_url_never_exposed(clock, receivers, caplog):  # H7
    receiver = receivers()
    pinger = _pinger(receiver.url, clock)
    with pytest.raises(HeartbeatConfigError) as missing:
        HeartbeatPinger(REF, period_s=50, timeout_s=1, environ={})
    assert "env:FP_TEST_HEARTBEAT_URL" in str(missing.value)
    with pytest.raises(HeartbeatConfigError) as stored:
        HeartbeatPinger("secret:FP_HB", period_s=50, timeout_s=1, environ={"FP_HB": receiver.url})
    assert "secret:FP_HB" in str(stored.value) and TOKEN not in str(stored.value)
    with pytest.raises(HeartbeatConfigError):
        HeartbeatPinger(receiver.url, period_s=50, timeout_s=1)  # a value, not a reference
    caplog.set_level(logging.DEBUG)
    pinger.mark_progress()
    _settle(pinger)
    failing = _pinger(_closed_port_url(), clock, timeout=0.3)
    failing.mark_progress()
    _settle(failing)
    for exposed in (repr(pinger), str(pinger), repr(pinger.stats()), str(failing.stats()),
                    caplog.text, repr(failing)):
        assert TOKEN not in exposed and PATH not in exposed and "127.0.0.1" not in exposed
    assert receiver.arrivals == [0.0]
    with pytest.raises(HeartbeatConfigError) as bad:
        HeartbeatPinger(REF, period_s=50, timeout_s=1,
                        environ={"FP_TEST_HEARTBEAT_URL": "https://user:pw@host.example/x/heartbeat/"})
    assert "pw" not in str(bad.value) and "host.example" not in str(bad.value)


def _imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, "relative import in " + path.name
            names.add(node.module)
        elif isinstance(node, ast.Call) and getattr(node.func, "id", None) == "__import__":
            names.add("__import__")
    return names


def test_heartbeat_modules_import_allowlist():  # H8
    allowed = {"__future__", "argparse", "collections.abc", "datetime", "http.client", "logging",
               "math", "os", "pathlib", "re", "socket", "ssl", "sys", "threading", "time", "urllib.error",
               "urllib.parse", "urllib.request", "c1_signal_daemon.book_heartbeat"}
    for path in MODULES:
        names = _imports(path)
        assert names <= allowed, (path.name, sorted(names - allowed))
        text = path.read_text(encoding="utf-8")
        for forbidden in ("book_incident_notifier", "book_incident_grafana_irm", "sqlite3",
                          "book_account_owner", "c1_rail", "importlib", "subprocess"):
            assert forbidden not in text, (path.name, forbidden)
    assert _imports(MODULES[0]) <= allowed - {"c1_signal_daemon.book_heartbeat", "argparse"}


def test_no_arming_state_read():  # H9
    for path in MODULES:
        text = path.read_text(encoding="utf-8")
        for forbidden in ("dry_run", "armed_until", "c1_rail_arm", "write_volume_config",
                          "operator_keys", "fly.toml", "c1_rail_listener", "handle_book_action"):
            assert forbidden not in text, (path.name, forbidden)


@pytest.mark.parametrize("url, rule", [
    ("http://127.0.0.1:9/integrations/v1/formatted_webhook/fake-token/heartbeat/", "scheme"),
    ("https://user@stack." + "grafana" + ".net/integrations/v1/x/heartbeat/", "userinfo"),
    ("https://stack.example.com/integrations/v1/x/heartbeat/", "host"),
    ("https://stack." + "grafana" + ".net/integrations/v1/x/alerts/", "path"),
    ("https://stack." + "grafana" + ".net.evil.example/integrations/v1/x/heartbeat/", "host"),
])
def test_url_validation_and_no_redirect(url, rule, clock, receivers):  # H10
    with pytest.raises(HeartbeatConfigError) as refused:
        HeartbeatPinger(REF, period_s=50, timeout_s=1, environ={"FP_TEST_HEARTBEAT_URL": url})
    message = str(refused.value)
    assert rule in message and "stack" not in message and "fake-token" not in message
    accepted = HeartbeatPinger(REF, period_s=50, timeout_s=1, environ={
        "FP_TEST_HEARTBEAT_URL": "https://stack." + "grafana" + ".net/integrations/v1/x/heartbeat/"})
    assert accepted.stats()["sends_started"] == 0
    redirecting = receivers(mode="redirect")
    pinger = _pinger(redirecting.url, clock, timeout=0.5)
    pinger.mark_progress()
    _settle(pinger)
    assert redirecting.requests == [("POST", PATH)]  # the 302 target was never requested
    assert pinger.stats()["sends_failed"] == 1


def test_live_check_refuses_without_confirmation_or_reference(receivers, clock):  # H11
    receiver = receivers()
    env = {"FP_DMON_GRAFANA_IRM_HEARTBEAT_URL": receiver.url}
    argv = ["--side", "runtime", "--ping-seconds", "1", "--silent-seconds", "0",
            "--period-s", "0.5", "--timeout-s", "0.2", "--mark-interval-s", "0.1"]
    out = io.StringIO()
    assert book_heartbeat_live_check.main(argv, environ=env, out=out) != 0
    assert "--confirm-live-check" in out.getvalue()
    missing = io.StringIO()
    assert book_heartbeat_live_check.main(
        argv + ["--confirm-live-check"], environ={}, out=missing) != 0
    assert "env:FP_DMON_GRAFANA_IRM_HEARTBEAT_URL" in missing.getvalue()
    notifier_side = io.StringIO()
    assert book_heartbeat_live_check.main(
        ["--side", "notifier"] + argv[2:] + ["--confirm-live-check"], environ=env,
        out=notifier_side) != 0
    assert "env:FP_DMON_GRAFANA_IRM_NOTIFIER_HEARTBEAT_URL" in notifier_side.getvalue()
    time.sleep(0.2)
    assert receiver.requests == []
    for text in (out.getvalue(), missing.getvalue(), notifier_side.getvalue()):
        assert TOKEN not in text and "127.0.0.1" not in text


def test_build_pingers_refuses_shared_reference_or_url(receivers, clock):  # H12
    first, second = receivers(), receivers()
    runtime = {"secret_ref": REF, "period_s": 50, "timeout_s": 1}
    notifier = {"secret_ref": REF_N, "period_s": 50, "timeout_s": 1}
    env = {"FP_TEST_HEARTBEAT_URL": first.url, "FP_TEST_NOTIFIER_HEARTBEAT_URL": second.url}
    pair = build_pingers(runtime, notifier, environ=env, allow_loopback_http=True, clock=clock)
    assert len(pair) == 2 and pair[0] is not pair[1]
    with pytest.raises(HeartbeatConfigError) as same_ref:
        build_pingers(runtime, dict(notifier, secret_ref=REF), environ=env,
                      allow_loopback_http=True)
    assert "reference" in str(same_ref.value)
    shared = dict(env, FP_TEST_NOTIFIER_HEARTBEAT_URL=first.url)
    with pytest.raises(HeartbeatConfigError) as same_url:
        build_pingers(runtime, notifier, environ=shared, allow_loopback_http=True)
    assert "URL" in str(same_url.value)
    for error in (same_ref.value, same_url.value):
        assert TOKEN not in str(error) and "127.0.0.1" not in str(error)
    with pytest.raises(HeartbeatConfigError):
        build_pingers(dict(runtime, url=first.url), notifier, environ=env,
                      allow_loopback_http=True)  # an inline value is refused
    # Equivalent spellings of one endpoint are the same integration (#701 review P2).
    host = "example." + "grafana" + ".net"
    for left, right in [
            ("https://%s/fake-token/heartbeat/" % host,
             "https://%s:443/fake-token/heartbeat/" % host.upper()),
            ("https://%s/fake-token/heartbeat/" % host,
             "https://%s/fake%%2Dtoken/heartbeat/" % host),
            ("https://%s/fake-token/heartbeat/" % host,
             "https://%s//fake-token//heartbeat/" % host),
            (first.url, first.url.replace("/integrations/", "//integrations/"))]:
        with pytest.raises(HeartbeatConfigError) as same:
            build_pingers(runtime, notifier, allow_loopback_http=True, environ={
                "FP_TEST_HEARTBEAT_URL": left, "FP_TEST_NOTIFIER_HEARTBEAT_URL": right})
        assert "URL" in str(same.value) and "example" not in str(same.value)


# -- §6.2 synthetic silent-runtime and silent-notifier qualification ---------------------------

T, P, STEP = 60.0, 20.0, 10.0


def test_hq1_stopped_loop_expires_and_resume_restores(tmp_path, clock, receivers):
    receiver = receivers()
    pinger = _pinger(receiver.url, clock, period=P)
    account, loop = _real_loop(tmp_path)
    for _ in range(30):
        _runtime_step(loop, pinger, clock, account)
        _settle(pinger)
        assert not receiver.expired(T)
        clock.advance(STEP)
    before = _owner_view(account)
    clock.advance(T)
    assert receiver.expired(T)
    at_expiry = _owner_view(account)
    for _ in range(3):
        _runtime_step(loop, pinger, clock, account)
        _settle(pinger)
        clock.advance(STEP)
    assert not receiver.expired(T)
    assert at_expiry == before == _owner_view(account)


def test_hq2_hung_step_expires(tmp_path, clock, receivers):
    receiver = receivers()
    pinger = _pinger(receiver.url, clock, period=P)
    account, loop = _real_loop(tmp_path)
    _runtime_step(loop, pinger, clock, account)
    _settle(pinger)
    clock.advance(STEP)
    loop._step_lock.acquire()
    worker = threading.Thread(target=_runtime_step, args=(loop, pinger, clock, account),
                              daemon=True)
    try:
        worker.start()
        for _ in range(10):
            clock.advance(STEP)
            time.sleep(0.01)
        assert receiver.arrivals == [0.0]
        assert receiver.expired(T)
    finally:
        loop._step_lock.release()
        worker.join(SETTLE)


def test_hq3_owner_storage_failure_expires(tmp_path, clock, receivers):
    receiver = receivers()
    pinger = _pinger(receiver.url, clock, period=P)
    account, loop = _real_loop(tmp_path)
    _runtime_step(loop, pinger, clock, account)
    _settle(pinger)
    account.path.write_bytes(b"not a database" * 64)
    for _ in range(10):
        clock.advance(STEP)
        with pytest.raises(AccountOwnerError):
            _runtime_step(loop, pinger, clock, account)
    _settle(pinger)
    assert receiver.arrivals == [0.0]
    assert pinger.stats()["sends_started"] == 1
    assert receiver.expired(T)


@pytest.mark.parametrize("target", ["refused", "hang"])
def test_hq4_receiver_unreachable_leaves_loop_timing_unchanged(tmp_path, clock, receivers,
                                                               target):
    url = _closed_port_url() if target == "refused" else receivers(mode="hang").url
    pinger = _pinger(url, clock, period=1.0, timeout=0.5)
    account, loop = _real_loop(tmp_path)
    baseline, wrapped = [], []
    for _ in range(10):
        started = time.monotonic()
        loop.step(now=NOW + timedelta(seconds=clock()))
        account.status()
        baseline.append(time.monotonic() - started)
        clock.advance(2)
        started = time.monotonic()
        _runtime_step(loop, pinger, clock, account)
        wrapped.append(time.monotonic() - started)
        clock.advance(2)
    assert max(wrapped) < max(baseline) + 0.1
    _settle(pinger)
    assert pinger.stats()["sends_ok"] == 0 and pinger.stats()["sends_failed"] >= 1


def test_hq5_runtime_pinger_independent_of_notifier(tmp_path, clock, receivers):
    receiver, other = receivers(), receivers()
    runtime_pinger, notifier_pinger = build_pingers(
        {"secret_ref": REF, "period_s": P, "timeout_s": 1},
        {"secret_ref": REF_N, "period_s": P, "timeout_s": 1},
        environ={"FP_TEST_HEARTBEAT_URL": receiver.url,
                 "FP_TEST_NOTIFIER_HEARTBEAT_URL": other.url},
        allow_loopback_http=True, clock=clock)
    account, loop = _real_loop(tmp_path)
    for _ in range(6):  # no notifier exists at all
        _runtime_step(loop, runtime_pinger, clock, account)
        _settle(runtime_pinger)
        clock.advance(STEP)
    notifier = _notifier(tmp_path, functools.partial(BookAccountOwner.read_incidents,
                                                     account.path))
    journal = tmp_path / "journal.sqlite"
    journal.unlink()
    journal.mkdir()  # the notifier's journal is now unavailable
    for _ in range(12):
        with pytest.raises(NotifierStoreError):
            notifier_round_with_heartbeat(notifier, notifier_pinger)
        _runtime_step(loop, runtime_pinger, clock, account)
        _settle(runtime_pinger, notifier_pinger)
        assert not receiver.expired(T)
        clock.advance(STEP)
    assert other.arrivals == [] and other.expired(T)


def _pair(clock, receivers, *, period=P, period_n=P):
    runtime_receiver, notifier_receiver = receivers(), receivers()
    pingers = build_pingers(
        {"secret_ref": REF, "period_s": period, "timeout_s": 1},
        {"secret_ref": REF_N, "period_s": period_n, "timeout_s": 1},
        environ={"FP_TEST_HEARTBEAT_URL": runtime_receiver.url,
                 "FP_TEST_NOTIFIER_HEARTBEAT_URL": notifier_receiver.url},
        allow_loopback_http=True, clock=clock)
    return runtime_receiver, notifier_receiver, pingers


@pytest.mark.parametrize("stall", ["stopped", "blocked"])
def test_hq6_notifier_stalled_runtime_alive_pages_notifier_only(tmp_path, clock, receivers,
                                                                 stall):
    r, n, (runtime_pinger, notifier_pinger) = _pair(clock, receivers)
    account, loop = _real_loop(tmp_path)
    channel = FakeChannel("primary")
    notifier = _notifier(tmp_path, functools.partial(BookAccountOwner.read_incidents,
                                                     account.path), channel)
    for _ in range(6):
        _runtime_step(loop, runtime_pinger, clock, account)
        notifier_round_with_heartbeat(notifier, notifier_pinger)
        _settle(runtime_pinger, notifier_pinger)
        clock.advance(STEP)
    worker = None
    if stall == "blocked":
        notifier._round_lock.acquire()
        worker = threading.Thread(target=notifier_round_with_heartbeat,
                                  args=(notifier, notifier_pinger), daemon=True)
        worker.start()
    try:
        for _ in range(12):
            _runtime_step(loop, runtime_pinger, clock, account)
            _settle(runtime_pinger, notifier_pinger)
            assert not r.expired(T)
            clock.advance(STEP)
        assert n.expired(T)
    finally:
        if worker:
            notifier._round_lock.release()
            worker.join(SETTLE)


def test_hq7_runtime_stalled_notifier_alive_pages_runtime_only(tmp_path, clock, receivers):
    r, n, (runtime_pinger, notifier_pinger) = _pair(clock, receivers)
    account, loop = _real_loop(tmp_path)
    notifier = _notifier(tmp_path, functools.partial(BookAccountOwner.read_incidents,
                                                     account.path))
    for _ in range(6):
        _runtime_step(loop, runtime_pinger, clock, account)
        notifier_round_with_heartbeat(notifier, notifier_pinger)
        _settle(runtime_pinger, notifier_pinger)
        clock.advance(STEP)
    for _ in range(12):
        notifier_round_with_heartbeat(notifier, notifier_pinger)
        _settle(notifier_pinger)
        assert not n.expired(T)
        clock.advance(STEP)
    assert r.expired(T)


def test_hq8_both_alive_no_page(tmp_path, clock, receivers):
    # P = 50 s just above a multiple of the 30 s cadence: sends land 60 s apart, so the
    # constraint P + interval + duration + timeout < T needs T above 81 s.
    ttl = 90.0
    r, n, (runtime_pinger, notifier_pinger) = _pair(clock, receivers, period=50.0,
                                                     period_n=50.0)
    account, loop = _real_loop(tmp_path)
    notifier = _notifier(tmp_path, functools.partial(BookAccountOwner.read_incidents,
                                                     account.path))
    for _ in range(40):  # 20 minutes, over a dozen T
        _runtime_step(loop, runtime_pinger, clock, account)
        notifier_round_with_heartbeat(notifier, notifier_pinger)
        _settle(runtime_pinger, notifier_pinger)
        assert not r.expired(ttl) and not n.expired(ttl)
        clock.advance(30)
        assert not r.expired(ttl) and not n.expired(ttl)
    assert max(b - a for a, b in zip(r.arrivals, r.arrivals[1:])) == 60.0


def _rows(count):
    return [{"incident_id": "synthetic-%d" % index, "reason": "operator-stop:synthetic",
             "at": NOW.isoformat(), "generation": 0} for index in range(count)]


@pytest.mark.parametrize("loss", ["incidents_store", "journal", "loud_deferral"])
def test_hq9_incidents_store_lost_pages_notifier(tmp_path, clock, receivers, loss):
    r, n, (runtime_pinger, notifier_pinger) = _pair(clock, receivers)
    account, loop = _real_loop(tmp_path)
    store = {"rows": []}

    def read_incidents():
        if store["rows"] is None:
            raise OSError("incidents store lost")
        return list(store["rows"])

    notifier_clock = NotifierClock()
    channel = FakeChannel("primary", [PublishResult("rejected")] * 200)
    notifier = _notifier(tmp_path, read_incidents, channel, k=1, clock=notifier_clock)
    notifier_round_with_heartbeat(notifier, notifier_pinger)
    _settle(notifier_pinger)
    assert n.arrivals == [0.0]
    if loss == "incidents_store":
        store["rows"] = None
    elif loss == "journal":
        journal = tmp_path / "journal.sqlite"
        journal.unlink()
        journal.mkdir()
    else:
        store["rows"] = _rows(3)  # k = 1 defers a due class-U job on every pass (NF3)
    for _ in range(12):
        clock.advance(STEP)
        notifier_clock.advance(60)
        progress = notifier.progress()
        if loss == "loud_deferral":
            notifier_round_with_heartbeat(notifier, notifier_pinger)
            assert notifier.progress() == progress
        else:
            with pytest.raises((OSError, NotifierStoreError)):
                notifier_round_with_heartbeat(notifier, notifier_pinger)
        _runtime_step(loop, runtime_pinger, clock, account)
        _settle(runtime_pinger, notifier_pinger)
        assert not r.expired(T)
    assert n.arrivals == [0.0]
    assert n.expired(T)


def test_hq10_backward_wall_clock_does_not_suppress_notifier_marks(tmp_path, clock, receivers):
    _, n, (_, notifier_pinger) = _pair(clock, receivers)
    notifier_clock = NotifierClock()
    notifier = _notifier(tmp_path, lambda: [], clock=notifier_clock)
    notifier_round_with_heartbeat(notifier, notifier_pinger)
    _settle(notifier_pinger)
    previous = notifier.liveness()
    for _ in range(12):
        clock.advance(STEP)
        notifier_clock.advance(-(T + 30))  # the wall clock steps back by more than T_n
        progress = notifier.progress()
        notifier_round_with_heartbeat(notifier, notifier_pinger)
        _settle(notifier_pinger)
        assert notifier.liveness() < previous
        assert notifier.progress() == progress + 1
        previous = notifier.liveness()
        assert not n.expired(T)
    assert len(n.arrivals) >= 12 * STEP // P
