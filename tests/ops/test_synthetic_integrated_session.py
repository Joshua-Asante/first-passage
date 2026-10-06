"""Synthetic integrated session: contract bar sources -> four-leg loop -> owner -> notifier.

One scripted session runs the EXISTING production components end to end against in-process
fakes only: four ``ContractBarSource`` instances over a scripted ``BarTransport``, the
``FourLegEvaluateLoop`` and ``FourLegRuntime``, the ``BookAccountOwner`` with the labeled
``SyntheticProtectionBroker`` (admission and observed protection), a mid-session missing-leg
incident that halts the book, the ``IncidentNotifier`` publishing through a real
``GrafanaIRMChannel`` whose transport is an injected fake, the ``record-delivery`` CLI logic
against the notifier journal ("safe to resolve"), and an attended resume attempt that the
owner refuses (incident ADR §A11.2: no same-session restart).

Evidence class: synthetic / replay engineering. Not strategy performance, not live shadow,
not feed or T00 qualification. Synthetic legs, bars and strategies only; no accepted port.

The guard is an audit hook (process-wide, so the notifier's publish thread is covered) that
records and refuses any socket, DNS, HTTP, urllib or child-process attempt while armed, plus
failing stand-ins for every order-route and HTTP-client constructor the rail can reach. The
``test_guard_*`` cases are strict xfails that prove the guard is live.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
import json
import socket
import subprocess
import sys
from types import SimpleNamespace
import urllib.request

import pytest

from c1_rail import book_incident_grafana_irm as irm_module
from c1_rail import book_incident_operator_cli as cli_module
from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerResult
from c1_rail.book_incident_notifier import IncidentNotifier, NotifierConfig, incident_key
from c1_rail.book_protection import ProtectionRead
from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
from c1_rail.c1_rail_listener import handle_book_fact
from c1_signal_daemon import listener_client
from c1_signal_daemon.bar_source_contract import (
    LEG_FEEDS, ContractBarSource, DeliveredBar, Lease, SymbolBinding, TransportPolicy,
)
from c1_signal_daemon.book_adapters import synthetic_adapter_registry
from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
from c1_signal_daemon.book_protocol import BAR_PERIOD, BAR_SLACK, Bracket
from c1_signal_daemon.book_runtime import LEG_ORDER, FourLegRuntime
import c1_rail_listener as listener_module
import crosstrade_payload
from test_four_leg_runtime import NOW, Adapter, binding, entry

URL_ENV = "FP_SYNTHETIC_SESSION_IRM_URL"
# Never resolved or contacted: ``_poster`` is replaced by the fake transport below.
SYNTHETIC_URL = "https://synthetic-session.grafana" + ".net/integrations/v1/formatted_webhook/fake/"
CONTRACTS = {"aegis_6j": "6JZ6", "dj30_mym_p250": "MYMZ6", "vanguard_mgc": "MGCZ6",
             "orb_mnq_v7": "MNQZ6"}
MISSING_LEG = "vanguard_mgc"  # its transport goes silent for the third bar
INELIGIBLE = "fresh bootstrap entitlement required"
_GUARDED = ("socket.connect", "socket.getaddrinfo", "socket.gethostbyname",
            "socket.gethostbyname_ex", "socket.gethostbyaddr", "socket.bind", "socket.sendto",
            "socket.sendmsg", "http.client.connect", "http.client.send", "urllib.Request",
            "subprocess.Popen", "os.system", "os.posix_spawn", "os.spawn", "os.exec",
            "os.fork", "os.forkpty", "os.startfile", "_winapi.CreateProcess")


class GuardViolation(RuntimeError):
    """A network, HTTP, order-route or child-process attempt while the guard is armed."""


_GUARD = {"armed": False, "hits": []}


def _audit(event, _args):
    if _GUARD["armed"] and event in _GUARDED:
        _GUARD["hits"].append(event)
        raise GuardViolation(event)


sys.addaudithook(_audit)  # audit hooks cannot be removed; the flag scopes it to guarded tests


@pytest.fixture
def guard(monkeypatch):
    """Arm the audit hook and replace every order-route / HTTP-client constructor with a failer."""
    def refuse(name):
        def fail(*_args, **_kwargs):
            _GUARD["hits"].append(name)
            raise GuardViolation(name)
        return fail

    for module, names in ((crosstrade_payload, ("send_to_crosstrade", "_urllib_sender",
                                                "build_crosstrade_payload")),
                          (listener_module, ("send_to_crosstrade", "build_crosstrade_payload")),
                          (listener_client, ("default_transport", "ListenerClient")),
                          (urllib.request, ("build_opener", "urlopen")),
                          (irm_module.ssl, ("create_default_context",))):
        for name in names:
            monkeypatch.setattr(module, name, refuse(module.__name__ + "." + name))
    _GUARD["hits"] = []
    _GUARD["armed"] = True
    try:
        yield _GUARD["hits"]
    finally:
        _GUARD["armed"] = False


class Clock:
    def __init__(self, now):
        self.now = now

    def __call__(self):
        return self.now

    def at(self, instant):
        assert instant >= self.now
        self.now = instant
        return instant


class ScriptedTransport:
    """In-process ``BarTransport``: releases each scripted bar once it is complete."""

    def __init__(self, clock, script):
        self.clock = clock
        self.script = sorted(script, key=lambda bar: bar.stamp)
        self.calls = []

    def authenticate(self):
        self.calls.append("authenticate")
        return Lease(self.clock() + timedelta(days=1))

    def renew(self, lease):  # noqa: ARG002
        self.calls.append("renew")
        return Lease(self.clock() + timedelta(days=1))

    def connect(self, lease):  # noqa: ARG002
        self.calls.append("connect")

    def receive(self):
        due = [bar for bar in self.script if bar.stamp + BAR_PERIOD <= self.clock()]
        self.script = [bar for bar in self.script if bar not in due]
        return due

    def close(self):
        self.calls.append("close")


def _delivered(code, ts, offset):
    price = 100.0 + offset
    return DeliveredBar(code, ts, price, price + 1, price - 1, price + 0.5, 10.0 + offset)


def _session_owner(tmp_path):
    bound = binding()
    bound.update(valid_until=NOW + timedelta(hours=2), max_evidence_age=timedelta(hours=2))
    broker = SyntheticProtectionBroker([BrokerResult("accepted")], account="synthetic-account",
                                       account_epoch="unbound", at=NOW)
    owner = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                  binding=bound, synthetic_broker=broker)
    broker.account_epoch = owner.make_occurrence("direct", "fixture-bind").account_epoch
    owner.activate_synthetic(now=NOW)
    return owner, broker


def _adapters(signal):
    return synthetic_adapter_registry({
        leg_id: Adapter(leg_id, [signal] if leg_id == signal.leg_id else ())
        for leg_id in LEG_ORDER})


def _sources(clock, session):
    window = SimpleNamespace(opens_at=session.opens_at, closes_at=session.closes_at)
    bars = (NOW, NOW + BAR_PERIOD, NOW + 2 * BAR_PERIOD)
    sources, transports = {}, {}
    for offset, leg_id in enumerate(LEG_ORDER):
        code = "SYN-" + CONTRACTS[leg_id]
        script = [_delivered(code, ts, offset) for ts in bars
                  if not (leg_id == MISSING_LEG and ts == bars[2])]
        transports[leg_id] = ScriptedTransport(clock, script)
        sources[leg_id] = ContractBarSource(
            transports[leg_id],
            binding=SymbolBinding(leg_id, LEG_FEEDS[leg_id][1], code, CONTRACTS[leg_id],
                                  NOW + timedelta(days=1), "open"),
            policy=TransportPolicy(backoff_initial_s=1.0, backoff_max_s=30.0, renew_margin_s=60.0),
            session_window=lambda ts: window if window.opens_at <= ts < window.closes_at else None,
            clock=clock)
    return sources, transports


def _notifier(tmp_path, owner_path, clock):
    raw = {"channels": [{"name": "irm", "kind": "grafana_irm", "secret_ref": "env:" + URL_ENV}],
           "publish_timeout_s": 5.0, "retry_initial_s": 5.0, "retry_max_s": 30.0}
    config = NotifierConfig.from_mapping(raw)
    config_path = tmp_path / "notifier-config.json"
    config_path.write_bytes(json.dumps(raw).encode("utf-8"))
    channel = irm_module.GrafanaIRMChannel("irm", "env:" + URL_ENV,
                                           publish_timeout_s=config.publish_timeout_s)
    notifier = IncidentNotifier(tmp_path / "notifier.sqlite",
                                read_incidents=lambda: BookAccountOwner.read_incidents(owner_path),
                                channels={"irm": channel}, config=config, clock=clock)
    return notifier, config_path


def test_synthetic_integrated_session(tmp_path, guard, monkeypatch, capsys):
    posts = []

    def fake_poster(url, timeout_s):
        assert url == SYNTHETIC_URL and 0 < timeout_s < 5.0

        def post(data):
            posts.append(json.loads(data))
            return 202, b'{"synthetic":"accepted"}'
        return post

    monkeypatch.setenv(URL_ENV, SYNTHETIC_URL)
    monkeypatch.setattr(irm_module, "_poster", fake_poster)
    clock = Clock(NOW)
    owner, broker = _session_owner(tmp_path)
    signal = replace(entry("orb_mnq_v7", 1), bracket=Bracket(stop=98))
    adapters = _adapters(signal)
    runtime = FourLegRuntime(owner, adapters)
    sources, transports = _sources(clock, owner.binding["session"])
    loop = FourLegEvaluateLoop(sources=sources, runtime=runtime)

    # Bar 1 (NOW): all four legs arrive once complete; the orb signal is admitted and sent.
    first = loop.step(now=clock.at(NOW + BAR_PERIOD))
    assert [(row.operation_id, row.transport_state) for row in first] == [
        ("entry:orb_mnq_v7", "accepted")]
    assert [(c.leg_id, c.kind) for c in broker.commands] == [("orb_mnq_v7", "entry")]

    # Fill and protection evidence arrive through the listener / runtime seams.
    fill_at = clock.at(NOW + BAR_PERIOD + timedelta(seconds=1))
    fact = broker.execute_entry("entry:orb_mnq_v7", fill_id="fill-orb", quantity=1, price=100.0,
                                at=fill_at)
    handle_book_fact(fact, owner, runtime, now=fill_at)
    read_at = clock.at(fill_at + timedelta(seconds=1))
    broker.advance(read_at)
    snapshot = broker.read_protection(ProtectionRead(
        owner.make_occurrence("direct", "session-read"), ("orb_mnq_v7",), fill_at))
    runtime.observe_protection(snapshot, now=read_at)
    [protection] = [row for row in owner.protection_owners if row.entry_fill_id == "fill-orb"]
    assert protection.observed is not None
    assert adapters["orb_mnq_v7"].events == [("fill", "entry:orb_mnq_v7", "fill-orb")]
    assert (owner.permission, owner.authority) == ("RUNNING", "NORMAL")

    # Bar 2 (NOW + 15 m): complete, no actions.
    assert loop.step(now=clock.at(NOW + 2 * BAR_PERIOD)) == ()
    assert len(broker.commands) == 1

    # Bar 3 (NOW + 30 m): the vanguard transport is silent; the partial barrier expires.
    third = NOW + 2 * BAR_PERIOD
    assert loop.step(now=clock.at(third + BAR_PERIOD)) is None
    assert len(owner.retained_partial_bars) == 3
    expired_at = clock.at(third + BAR_PERIOD + BAR_SLACK + timedelta(seconds=1))
    assert loop.step(now=expired_at) is None
    assert (owner.permission, owner.authority) == ("HALTED", "INTERVENTION")
    # One halt sequence, two committed incidents at the same instant: the source-silence
    # watch (2 x bar + 30 s since the last complete barrier) and the partial-barrier expiry.
    incidents = owner.incidents
    assert [(row["incident_id"], row["reason"], row["generation"]) for row in incidents] == [
        ("feed-silence:" + owner.binding["session"].session_id + ":"
         + (NOW + BAR_PERIOD).isoformat(), "feed", 1),
        ("barrier-expired:" + third.isoformat(), "barrier", 2)]
    halted = owner.status()

    # Notification: one page per incident through the grafana_irm channel's fake transport.
    clock.at(expired_at + timedelta(seconds=1))
    notifier, config_path = _notifier(tmp_path, owner.path, clock)
    notifier.run_once()
    keys = [incident_key(row["incident_id"]) for row in incidents]
    assert [post["alert_uid"] for post in posts] == keys
    assert {(post["severity"], post["state"]) for post in posts} == {("critical", "alerting")}
    sent = json.dumps(posts)
    assert not any(row["incident_id"] in sent for row in incidents)
    assert "synthetic-account" not in sent
    assert [(job["incident_key"], job["state"], job["reason"]) for job in notifier.jobs()] == [
        (keys[0], "pending", "feed"), (keys[1], "pending", "barrier")]
    assert owner.status() == halted  # the notifier never changes the halt

    # record-delivery (operator acknowledgment) -> "safe to resolve (rail side)".
    for key in keys:
        capsys.readouterr()
        assert cli_module.main(["record-delivery", "--journal", str(notifier.store_path),
                                "--config", str(config_path), "--channel", "irm", key]) == 0
        assert cli_module.SAFE in capsys.readouterr().out
    clock.at(clock.now + timedelta(seconds=60))
    notifier.run_once()  # a later loop, past every retry time, republishes nothing
    assert len(posts) == 2

    # Attended resume attempt in the same session: refused, in place and after a restart.
    resume_at = clock.at(expired_at + timedelta(minutes=2))
    broker.advance(resume_at)
    with pytest.raises(AccountOwnerError, match=INELIGIBLE):
        owner.activate_synthetic(now=resume_at)
    restarted = BookAccountOwner.boot(owner.path, "synthetic-account", binding=owner.binding,
                                      synthetic_broker=broker)
    with pytest.raises(AccountOwnerError, match=INELIGIBLE):
        restarted.activate_synthetic(now=resume_at)
    after = restarted.status()
    assert (after["permission"], after["authority"]) == ("HALTED", "INTERVENTION")
    assert after["generation"] == halted["generation"] + 1
    assert restarted.incidents == incidents
    with pytest.raises(AccountOwnerError, match="stale account owner boot"):
        owner.status()  # the pre-restart handle is fenced
    blocked = restarted.dispatch(replace(entry("aegis_6j", 1), bar_time=resume_at),
                                 occurrence=restarted.make_occurrence("direct", "resume-attempt"),
                                 now=resume_at)
    assert blocked.refusal_reason == "intervention_fence"

    # End state: journals and records agree; nothing else left the process.
    for key in keys:
        kinds = [row["kind"] for row in notifier.events(key)]
        assert kinds == ["detected", "attempt", "provider_accepted", "delivered"]
    assert [(job["state"], job["generation"]) for job in notifier.jobs()] == [
        ("delivered", row["generation"]) for row in incidents]
    assert [(row["bar_time"], row["completed"]) for row in restarted.retained_barriers] == [
        (NOW.isoformat(), True), ((NOW + BAR_PERIOD).isoformat(), True)]
    assert restarted.retained_partial_bars == ()
    assert [(c.leg_id, c.kind) for c in broker.commands] == [("orb_mnq_v7", "entry")]
    assert all(source.refusal is None for source in sources.values())
    assert all(t.calls[:2] == ["authenticate", "connect"] for t in transports.values())
    assert guard == []


@pytest.mark.xfail(raises=GuardViolation, strict=True, reason="guard liveness: must refuse")
@pytest.mark.parametrize("attempt", ["getaddrinfo", "connect", "urllib", "subprocess"])
def test_guard_refuses_deliberate_attempt(guard, attempt):  # noqa: ARG001
    if attempt == "getaddrinfo":
        socket.getaddrinfo("127.0.0.1", 9, flags=socket.AI_NUMERICHOST)
    elif attempt == "connect":
        with socket.socket() as probe:
            probe.connect(("127.0.0.1", 9))
    elif attempt == "urllib":
        urllib.request.OpenerDirector().open("http://127.0.0.1:9/")  # no handlers: no I/O
    else:
        subprocess.Popen(["synthetic-session-no-such-executable"])  # pylint: disable=consider-using-with
