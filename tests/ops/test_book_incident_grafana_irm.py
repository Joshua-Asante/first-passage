"""D-MON-1: the Grafana IRM binding of the book incident notifier, tests U1-U15 and Q1-Q6.

Card: docs/briefs/handoffs/2026-10-03-dmon-grafana-irm-binding-card-DRAFT.md (FROZEN 2026-10-04).
Every request goes to a loopback fake IRM on 127.0.0.1 with the fixture token ``fake-token``;
nothing here reaches a provider, pages anyone, arms, deploys or contacts a broker. The Q7 live
page is Joshua's attended act and is not run here. The evidence class is *Synthetic / replay
engineering*.
"""
from __future__ import annotations

import ast
from contextlib import closing
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import functools
import hashlib
import http.server
import inspect
import json
import logging
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import threading
import time
from types import SimpleNamespace

import pytest

from c1_rail import book_incident_notifier as notifier_module
from c1_rail.book_account_owner import BookAccountOwner, BrokerResult
from c1_rail.book_incident_notifier import (
    CHANNEL_KINDS,
    ChannelSpec,
    IncidentNotifier,
    LocalFileChannel,
    NotifierConfig,
    NotifierConfigError,
    NotifierStoreError,
    incident_key,
)
from c1_rail.book_policy import leg
from c1_rail_telemetry import assert_no_secrets
from test_attended_incident_rehearsal import (
    LEGS,
    _dispatch,
    _other_leg_entry,
    _rehearsal_owner,
)
from test_book_account_owner import NOW, SESSION, binding, intent
from test_book_incident_notifier import (
    _INCIDENTS,
    Clock,
    _foreign_schema,
    _null_reason,
    _operator,
    _owner_view,
    _unreadable,
)

try:  # absent at the base revision: each test then fails on its own (red first)
    from c1_rail import book_incident_grafana_irm as irm_module
    from c1_rail import book_incident_irm_live_page as driver_module
    from c1_rail import book_incident_operator_cli as cli_module
except ImportError:
    irm_module = driver_module = cli_module = None


URL_ENV = "FP_DMON_GRAFANA_IRM_URL"
REF = "env:" + URL_ENV
TOKEN = "fake-token"
WEBHOOK = "/integrations/v1/formatted_webhook/" + TOKEN + "/"
# Split so that no source line holds a provider host followed by a path (card §10 hook).
PROVIDER_HOST = "stack.grafana" + ".net"
RAIL_DIR = Path(notifier_module.__file__).resolve().parent
CLI = RAIL_DIR / "book_incident_operator_cli.py"
SAFE = "safe to resolve (rail side)"
NOT_SAFE = "not safe; wait and re-run"
ALREADY = "already delivered"
BODY_FIELDS = {"alert_uid", "title", "message", "state", "severity"}


# -- loopback fake IRM ---------------------------------------------------------------------------

class Hold:
    """Answer 202 only once ``release`` is set."""

    def __init__(self):
        self.release = threading.Event()


class Drip:
    """Answer 200 at once, then drip the body one byte at a time until ``release`` is set."""

    def __init__(self, interval=0.1):
        self.release, self.interval = threading.Event(), interval


HANG = "hang"


class FakeIRM:
    """Records every request; scripted answers; groups POSTs by ``alert_uid`` while a group is
    open (card §0.5 item 5): a resolved group accepts nothing, so a later POST opens a new one."""

    def __init__(self):
        self.requests, self.script, self.groups, self.open = [], [], [], {}
        self.lock, self.stop = threading.Lock(), threading.Event()
        fake = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                with fake.lock:
                    fake.requests.append((self.path, None))
                self._answer(200, b"")

            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                payload = json.loads(raw) if raw else None
                with fake.lock:
                    fake.requests.append((self.path, payload))
                    if isinstance(payload, dict) and "alert_uid" in payload:
                        uid = payload["alert_uid"]
                        if uid not in fake.open:
                            fake.open[uid] = len(fake.groups)
                            fake.groups.append([])
                        fake.groups[fake.open[uid]].append(payload)
                    action = fake.script.pop(0) if fake.script else 202
                try:
                    self._act(action)
                except OSError:  # the client gave up (timeout); nothing more to send
                    pass

            def _act(self, action):
                if action == HANG:
                    fake.stop.wait(15)
                    self._answer(200, b"late")
                elif isinstance(action, Hold):
                    action.release.wait(60)
                    self._answer(202, b'{"held":true}')
                elif isinstance(action, Drip):
                    total = 4096
                    self.send_response(200)
                    self.send_header("Content-Length", str(total))
                    self.end_headers()
                    sent = 0
                    while not action.release.is_set() and sent < total - 1:
                        self.wfile.write(b"x")
                        self.wfile.flush()
                        sent += 1
                        time.sleep(action.interval)
                    self.wfile.write(b"x" * (total - sent))
                    self.wfile.flush()
                else:
                    self._answer(action, b"" if action == 204 else b'{"status":"ok"}')

            def _answer(self, status, content):
                self.send_response(status)
                if 300 <= status < 400:
                    self.send_header("Location", "http://127.0.0.1:%d/second-path"
                                     % fake.server.server_port)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                if content:
                    self.wfile.write(content)

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.server.block_on_close = False
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    @property
    def url(self):
        return "http://127.0.0.1:%d%s" % (self.server.server_port, WEBHOOK)

    def posts(self):
        with self.lock:
            return [payload for path, payload in self.requests if path == WEBHOOK]

    def resolve(self, uid):
        with self.lock:
            self.open.pop(uid, None)

    def close(self):
        self.stop.set()
        for action in self.script:
            if isinstance(action, (Hold, Drip)):
                action.release.set()
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def fake(monkeypatch):
    server = FakeIRM()
    monkeypatch.setenv(URL_ENV, server.url)
    yield server
    server.close()


def _closed_port_url():
    with closing(socket.socket()) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    return "http://127.0.0.1:%d%s" % (port, WEBHOOK)


# -- notifier wiring -----------------------------------------------------------------------------

def _config(*, timeout=2.0, initial=5.0, maximum=30.0, local=True, extra=()):
    channels = [{"name": "irm", "kind": "grafana_irm", "secret_ref": REF}, *extra]
    if local:
        channels.append({"name": "local", "kind": "local_file"})
    return NotifierConfig.from_mapping({"channels": channels, "publish_timeout_s": timeout,
                                        "retry_initial_s": initial, "retry_max_s": maximum})


def _irm(config=None, *, transport=None, **kwargs):
    config = config or _config()
    return irm_module.GrafanaIRMChannel("irm", REF, publish_timeout_s=config.publish_timeout_s,
                                        timeout_s=transport, allow_loopback_http=True, **kwargs)


def _notifier(directory, read_incidents, config, irm, *, clock=None, others=(), **kwargs):
    channels = {"irm": irm, **{channel.name: channel for channel in others}}
    if any(spec.name == "local" for spec in config.channels):
        channels["local"] = LocalFileChannel("local", Path(directory) / "alerts")
    return IncidentNotifier(Path(directory) / "journal.sqlite", read_incidents=read_incidents,
                            channels=channels, config=config, clock=clock or Clock(), **kwargs)


def _owner_reader(account):
    return functools.partial(BookAccountOwner.read_incidents, account.path)


def _rows(*ids, at=NOW):
    rows = tuple({"incident_id": incident, "reason": "operator", "at": at.isoformat(),
                  "generation": number} for number, incident in enumerate(ids, 1))
    return lambda: rows


def _real_clock():
    return datetime.now(timezone.utc)


def _write_config(directory, config):
    path = Path(directory) / "notifier-config.json"
    path.write_text(json.dumps(config.resolved()), encoding="utf-8")
    return path


def _ro(journal):
    return sqlite3.connect(Path(journal).resolve().as_uri() + "?mode=ro", uri=True, timeout=5,
                           isolation_level=None)


def _events(journal, key=None):
    with closing(_ro(journal)) as db:
        return [(sequence, kind, channel, json.loads(detail))
                for sequence, kind, channel, detail in db.execute(
                    "SELECT sequence, kind, channel, detail FROM events "
                    "WHERE ? IS NULL OR incident_key=? ORDER BY sequence", (key, key))]


def _kinds(journal, key=None):
    return [kind for _sequence, kind, _channel, _detail in _events(journal, key)]


def _wait_for(predicate, timeout=30.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            if predicate():
                return
        except sqlite3.Error:
            pass
        time.sleep(0.02)
    raise AssertionError("condition not reached within %.0f s" % timeout)


def _corrupt_files(directory):
    return [path for path in Path(directory).rglob("*") if ".corrupt-" in path.name]


def _cli(*args):
    return cli_module.main(["record-delivery", *map(str, args)])


def _cli_process(out, journal, config_path, key, *, wait_s=60):
    env = {name: value for name, value in os.environ.items() if name != URL_ENV}
    with open(out, "w", encoding="utf-8") as handle:
        return subprocess.Popen(
            [sys.executable, str(CLI), "record-delivery", "--journal", str(journal),
             "--config", str(config_path), "--wait-s", str(wait_s), key],
            stdout=handle, stderr=subprocess.STDOUT, env=env)


def _published(tmp_path, fake, *, config=None, answer=202):
    """A journal holding one job whose IRM publish was answered ``answer``."""
    config = config or _config()
    fake.script.append(answer)
    notifier = _notifier(tmp_path, _rows("synthetic:1"), config, _irm(config))
    notifier.run_once()
    key = notifier.jobs()[0]["incident_key"]
    return notifier, key, _write_config(tmp_path, config)


# -- U1-U11: the channel -------------------------------------------------------------------------

def test_body_is_formatted_webhook_with_incident_key_as_alert_uid(tmp_path, fake):
    """U1."""
    account = _operator(tmp_path)
    row = account.incidents[0]
    notifier = _notifier(tmp_path, _owner_reader(account), _config(), _irm())
    notifier.run_once()
    [body] = fake.posts()
    key = incident_key(row["incident_id"])
    assert set(body) == BODY_FIELDS
    assert body["alert_uid"] == key
    assert body["state"] == "alerting" and body["severity"] == "critical"
    assert body["title"] == "First Passage book incident: operator"
    assert row["at"] in body["message"] and key[:12] in body["message"]
    text = json.dumps(body)
    assert row["incident_id"] not in text and account.account not in text
    assert TOKEN not in text and "127.0.0.1" not in text
    assert_no_secrets(body)


def test_every_publish_carries_the_important_marker(tmp_path, fake):
    """U2."""
    clock = Clock()
    fake.script.extend([500, 500, 202])
    rows = (lambda: ({"incident_id": "synthetic:1", "reason": "operator", "at": NOW.isoformat(),
                      "generation": 1},
                     {"incident_id": "synthetic:2", "reason": None, "at": "bad",
                      "generation": "x"}))
    notifier = _notifier(tmp_path, rows, _config(), _irm(qualification_test=True), clock=clock)
    for delay in (0, 5, 10):
        clock.advance(delay)
        notifier.run_once()
    posts = fake.posts()
    assert len(posts) >= 4 and {post["alert_uid"] for post in posts} == {
        job["incident_key"] for job in notifier.jobs()}
    assert any(post["title"].endswith("malformed") for post in posts)
    assert all(post["severity"] == "critical" and post["state"] == "alerting" for post in posts)
    assert irm_module.SEVERITY == "critical"
    parameters = set(inspect.signature(irm_module.GrafanaIRMChannel).parameters)
    assert not {"severity", "state", "body"} & parameters
    with pytest.raises(NotifierConfigError):
        NotifierConfig.from_mapping({"channels": [
            {"name": "irm", "kind": "grafana_irm", "secret_ref": REF, "severity": "info"}]})


@pytest.mark.parametrize("status,expected", [
    (200, "accepted"), (201, "accepted"), (202, "accepted"), (204, "accepted"),
    (301, "rejected"), (302, "rejected"), (307, "rejected"),
    (400, "rejected"), (401, "rejected"), (403, "rejected"), (404, "rejected"),
    (405, "rejected"), (410, "rejected"), (413, "rejected"), (418, "rejected"), (422, "rejected"),
    (408, "unknown"), (429, "unknown"), (500, "unknown"), (502, "unknown"), (503, "unknown"),
])
def test_response_mapping(fake, status, expected):
    """U3."""
    fake.script.append(status)
    result = _irm().publish("a" * 64, {"reason": "operator", "detected_at": NOW.isoformat()})
    assert result.state == expected and result.delivered is False
    if expected == "accepted":
        content = b"" if status == 204 else b'{"status":"ok"}'
        assert result.evidence_digest == hashlib.sha256(b"%d\x00" % status + content).hexdigest()
    else:
        assert result.evidence_digest is None


def test_response_mapping_transport_failure_raises_without_text(monkeypatch):
    """U3, transport row: connection refused raises a bare GrafanaIRMTransportError."""
    monkeypatch.setenv(URL_ENV, _closed_port_url())
    with pytest.raises(irm_module.GrafanaIRMTransportError) as caught:
        _irm().publish("a" * 64, {"reason": "operator", "detected_at": NOW.isoformat()})
    assert caught.value.args == () and str(caught.value) == ""
    assert caught.value.__context__ is None and caught.value.__cause__ is None


def test_redirect_is_never_followed(fake):
    """U4."""
    fake.script.append(302)
    result = _irm().publish("a" * 64, {"reason": "operator", "detected_at": NOW.isoformat()})
    assert result.state == "rejected"
    assert [path for path, _ in fake.requests] == [WEBHOOK]


def test_timeout_bounded_below_publish_timeout(tmp_path, fake):
    """U5."""
    config = _config(timeout=2.0)
    for bad in (2.0, 3.0, 0, -1, float("nan"), True):
        with pytest.raises(NotifierConfigError):
            _irm(config, transport=bad)
    fake.script.append(HANG)
    channel = _irm(config, transport=0.5)
    started = time.monotonic()
    with pytest.raises(irm_module.GrafanaIRMTransportError):
        channel.publish("a" * 64, {"reason": "operator", "detected_at": NOW.isoformat()})
    assert time.monotonic() - started < 1.5
    fake.script.append(HANG)
    notifier = _notifier(tmp_path, _rows("synthetic:1"), config, _irm(config, transport=0.5))
    started = time.monotonic()
    notifier.run_once()
    assert time.monotonic() - started < config.publish_timeout_s
    failed = [detail for _, kind, channel_name, detail in _events(notifier.store_path)
              if kind == "delivery_failed" and channel_name == "irm"]
    assert failed == [{"outcome": "GrafanaIRMTransportError"}]


def test_secret_ref_resolution_and_url_never_exposed(tmp_path, fake, monkeypatch, caplog):
    """U6."""
    caplog.set_level(logging.DEBUG)
    config = _config()
    channel = _irm(config)
    fake.script.extend([500, 202])
    clock = Clock()
    notifier = _notifier(tmp_path, _rows("synthetic:1"), config, channel, clock=clock)
    notifier.run_once()
    clock.advance(5)
    notifier.run_once()
    surfaces = [repr(channel), str(channel), json.dumps(config.resolved()), config.digest,
                json.dumps(notifier.events()), json.dumps(notifier.jobs()),
                notifier.store_path.read_bytes().decode("latin-1"), caplog.text]
    monkeypatch.delenv(URL_ENV)
    with pytest.raises(NotifierConfigError) as missing:
        _irm(config)
    assert REF in str(missing.value)
    with pytest.raises(NotifierConfigError) as stored:
        irm_module.GrafanaIRMChannel("irm", "secret:" + URL_ENV, publish_timeout_s=2.0)
    monkeypatch.setenv(URL_ENV, _closed_port_url())
    with pytest.raises(irm_module.GrafanaIRMTransportError) as transport:
        _irm(config).publish("a" * 64, {"reason": "operator", "detected_at": NOW.isoformat()})
    surfaces += [str(missing.value), str(stored.value), repr(transport.value)]
    for surface in surfaces:
        assert TOKEN not in surface and fake.url not in surface and "127.0.0.1:" not in surface


@pytest.mark.parametrize("url,rule", [
    ("http://127.0.0.1:9" + WEBHOOK, "scheme"),
    ("http://" + PROVIDER_HOST + WEBHOOK, "scheme"),
    ("https://alice:pw9@" + PROVIDER_HOST + WEBHOOK, "userinfo"),
    ("https://example.com" + WEBHOOK, "host"),
    ("https://" + PROVIDER_HOST + "/integrations/v1/webhook/" + TOKEN + "/", "path"),
    ("https://" + PROVIDER_HOST + ":bad" + WEBHOOK, "unparseable"),
])
def test_url_validation_refuses_without_echo(monkeypatch, url, rule):
    """U7: without the loopback flag, every rule refuses and names itself, never the URL."""
    monkeypatch.setenv(URL_ENV, url)
    with pytest.raises(NotifierConfigError) as refused:
        irm_module.GrafanaIRMChannel("irm", REF, publish_timeout_s=2.0)
    message = str(refused.value)
    assert rule in message
    for part in (TOKEN, "alice", "pw9", "example.com", "stack.", "127.0.0.1", ":bad"):
        assert part not in message


def test_url_validation_accepts_the_provider_shape_and_keeps_loopback_off_config(monkeypatch):
    """U7: the valid shape constructs without a request; the loopback flag is not config."""
    monkeypatch.setenv(URL_ENV, "https://" + PROVIDER_HOST + WEBHOOK)
    assert irm_module.GrafanaIRMChannel("irm", REF, publish_timeout_s=2.0).last_status is None
    with pytest.raises(NotifierConfigError):
        NotifierConfig.from_mapping({"channels": [{"name": "irm", "kind": "grafana_irm",
                                                   "secret_ref": REF,
                                                   "allow_loopback_http": True}]})


def _imports(module):
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.setdefault(alias.name, set())
        elif isinstance(node, ast.ImportFrom):
            names.setdefault(node.module or "", set()).update(alias.name for alias in node.names)
    internal = {name.removeprefix("c1_rail."): imported for name, imported in names.items()
                if name.split(".")[0] not in sys.stdlib_module_names}
    return internal, tree


def _loaded_modules(module_name):
    code = ("import sys; sys.path[:0] = %r; import %s; print('\\n'.join(sorted(sys.modules)))"
            % (sys.path, module_name))
    return set(subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                              check=True, timeout=120).stdout.split())


_FORBIDDEN = {"book_account_owner", "c1_rail_arm", "write_volume_config", "c1_rail_listener",
              "c1_rail_http_server", "book_runtime", "book_halt"}


def test_irm_modules_have_no_broker_or_owner_mutation_path():
    """U8."""
    channel, _ = _imports(irm_module)
    assert set(channel) <= {"book_incident_notifier", "c1_rail_telemetry"}, channel
    assert channel.get("c1_rail_telemetry", set()) <= {"assert_no_secrets"}
    cli, _ = _imports(cli_module)
    assert set(cli) == {"book_incident_notifier"}, cli
    driver, tree = _imports(driver_module)
    admitted = {"book_account_owner", "book_incident_grafana_irm", "book_incident_notifier",
                "book_policy", "book_sizing_context"}
    assert set(driver) <= admitted, set(driver) - admitted
    for imports in (channel, cli, driver):
        assert not (set(imports) - {"book_account_owner"}) & _FORBIDDEN
    # Transitive closure: the channel and the CLI never load an owner, broker or arm module.
    for name in ("c1_rail.book_incident_grafana_irm", "c1_rail.book_incident_operator_cli"):
        loaded = {module.split(".")[-1] for module in _loaded_modules(name)}
        assert not loaded & _FORBIDDEN, (name, loaded & _FORBIDDEN)
        assert not [module for module in loaded if "broker" in module or "dispatch" in module]
    # The driver's only owner calls: BookAccountOwner.boot(synthetic_broker=None), then halt.
    owner_attributes, instance_attributes, boots = set(), [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "BookAccountOwner":
                owner_attributes.add(node.attr)
            elif node.value.id == "owner":
                instance_attributes.append(node.attr)
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "boot"):
            boots.append({keyword.arg: keyword.value for keyword in node.keywords})
        assert not (isinstance(node, ast.Attribute) and node.attr == "dispatch")
    assert owner_attributes == {"boot", "read_incidents"}
    assert sorted(instance_attributes) == ["halt", "path"]
    assert len(boots) == 1 and isinstance(boots[0]["synthetic_broker"], ast.Constant)
    assert boots[0]["synthetic_broker"].value is None


def test_grafana_irm_kind_needs_secret_ref_and_delivers():
    """U9."""
    assert CHANNEL_KINDS["grafana_irm"] == (True, True)
    with pytest.raises(NotifierConfigError):
        ChannelSpec("irm", "grafana_irm")
    with pytest.raises(NotifierConfigError):
        NotifierConfig.from_mapping({"channels": [{"name": "irm", "kind": "grafana_irm"}]})
    assert ChannelSpec("irm", "grafana_irm", REF).secret_ref == REF


def test_live_page_driver_refuses_without_confirmation_or_reference(tmp_path, fake, monkeypatch,
                                                                    capsys):
    """U10: no confirmation, a missing reference, or a non-provider URL: exit 2, no request."""
    assert driver_module.main(["--dir", str(tmp_path / "a")]) == 2
    monkeypatch.delenv(URL_ENV)
    assert driver_module.main(["--dir", str(tmp_path / "b"), "--confirm-live-page"]) == 2
    monkeypatch.setenv(URL_ENV, fake.url)  # plain-http loopback: the driver has no test flag
    assert driver_module.main(["--dir", str(tmp_path / "c"), "--confirm-live-page"]) == 2
    output = capsys.readouterr()
    assert fake.requests == []
    assert REF in output.err
    for stream in (output.out, output.err):
        assert TOKEN not in stream and fake.url not in stream
    assert not any((tmp_path / name).exists() for name in ("a", "b", "c"))


def test_live_page_driver_runs_the_q7_sequence_against_loopback(tmp_path, fake, monkeypatch,
                                                                capsys):
    """The §3.5 driver end to end, with the channel's loopback flag injected by the test only:
    one publish, one republish under the same key, one group; then §3.7 on its files."""
    monkeypatch.setattr(driver_module, "GrafanaIRMChannel", functools.partial(
        irm_module.GrafanaIRMChannel, allow_loopback_http=True))
    directory = tmp_path / "q7"
    assert driver_module.main(["--dir", str(directory), "--confirm-live-page",
                               "--republish-after-s", "5.2"]) == 0
    printed = capsys.readouterr().out
    posts = fake.posts()
    assert len(posts) == 2 and len(fake.groups) == 1
    key = posts[0]["alert_uid"]
    assert posts[1]["alert_uid"] == key and "incident key (alert_uid): " + key in printed
    assert posts[0]["title"].startswith("[QUALIFICATION TEST] ")
    assert TOKEN not in printed and fake.url not in printed
    config = json.loads((directory / "notifier-config.json").read_text(encoding="utf-8"))
    assert NotifierConfig.from_mapping(config).resolved() == config
    assert REF in json.dumps(config) and TOKEN not in json.dumps(config)
    owner = BookAccountOwner.read_incidents(directory / "qualification-owner.sqlite")
    assert [row["reason"] for row in owner] == ["operator"]
    assert _cli("--journal", directory / "notifier-journal.sqlite",
                "--config", directory / "notifier-config.json", key) == 0
    assert SAFE in capsys.readouterr().out


def test_one_webhook_per_round_fan_out_is_grafana_side(tmp_path, fake):
    """U11."""
    clock, config = Clock(), _config()
    notifier = _notifier(tmp_path, _rows("synthetic:1"), config, _irm(config), clock=clock)
    counts = []
    for delay in (0, 5, 10):
        clock.advance(delay)
        notifier.run_once()
        counts.append(len(fake.posts()))
    restarted = _notifier(tmp_path, _rows("synthetic:1"), config, _irm(config), clock=clock)
    clock.advance(20)
    restarted.run_once()
    counts.append(len(fake.posts()))
    assert counts == [1, 2, 3, 4]
    assert len(fake.groups) == 1
    for post in fake.posts():
        assert set(post) == BODY_FIELDS
    text = (json.dumps(fake.posts()) + json.dumps(config.resolved())).lower()
    for target in ("sms", "phone", "push", "mobile"):
        assert target not in text


# -- U12-U15: the record-delivery CLI ------------------------------------------------------------

class _Environ(dict):
    """An environ guard: reading the integration URL reference trips it."""

    def __init__(self, base, trips):
        super().__init__(base)
        self.trips = trips

    def _check(self, name):
        if name == URL_ENV:
            self.trips.append(name)
            raise AssertionError("record-delivery read the integration URL reference")

    def __getitem__(self, name):
        self._check(name)
        return super().__getitem__(name)

    def get(self, name, default=None):
        self._check(name)
        return super().get(name, default)

    def __contains__(self, name):
        self._check(name)
        return super().__contains__(name)


def test_record_delivery_cli_refusals_idempotency_and_no_effect(tmp_path, fake, monkeypatch,
                                                                 capsys):
    """U12."""
    backup = {"name": "backup", "kind": "grafana_irm", "secret_ref": "env:FP_DMON_BACKUP_URL"}
    monkeypatch.setenv("FP_DMON_BACKUP_URL", fake.url)
    config = _config(extra=(backup,))
    fake.script.append(202)
    clock = Clock()
    notifier = _notifier(tmp_path, _rows("synthetic:1"), config, _irm(config), clock=clock,
                         others=(irm_module.GrafanaIRMChannel(
                             "backup", backup["secret_ref"], publish_timeout_s=2.0,
                             allow_loopback_http=True),))
    notifier.run_once()
    key = notifier.jobs()[0]["incident_key"]
    journal = notifier.store_path
    two = _write_config(tmp_path, config)
    garbage = tmp_path / "garbage.json"
    garbage.write_text("{not json", encoding="utf-8")
    capsys.readouterr()
    before = _events(journal)
    for argv, check in (
            (("--journal", journal, "--config", two, "--channel", "irm", "0" * 64), "key-unknown"),
            (("--journal", journal, "--config", two, "--channel", "irm", "not-a-key"),
             "key-unknown"),
            (("--journal", journal, "--config", two, "--channel", "local", key), "channel"),
            (("--journal", journal, "--config", two, "--channel", "nope", key), "channel"),
            (("--journal", journal, "--config", two, key), "channel"),
            (("--journal", journal, "--config", two, "--channel", "backup", key), "no-attempt"),
            (("--journal", journal, "--config", garbage, key), "config")):
        assert _cli(*argv) == 2, argv
        assert "record-delivery refused: " + check in capsys.readouterr().err, argv
        assert _events(journal) == before, argv

    trips, connects = [], []

    def refuse_connect(*_args):
        connects.append(True)
        raise AssertionError("record-delivery opened a socket")

    with monkeypatch.context() as guard:
        guard.setattr(socket.socket, "connect", refuse_connect)
        guard.setattr(socket.socket, "connect_ex", refuse_connect)
        guard.setattr(os, "environ", _Environ(os.environ, trips))
        assert _cli("--journal", journal, "--config", two, "--channel", "irm", key) == 0
        first = capsys.readouterr().out
        assert _cli("--journal", journal, "--config", two, "--channel", "irm", key) == 0
        second = capsys.readouterr().out
    assert trips == [] and connects == []
    added = _events(journal)[len(before):]
    assert [(kind, channel) for _, kind, channel, _ in added] == [("delivered", "irm")]
    assert SAFE in first and ALREADY not in first
    assert ALREADY in second and SAFE in second
    requests = len(fake.requests)
    clock.advance(60)
    notifier.run_once()
    assert len(fake.requests) == requests
    assert _events(journal)[len(before):] == added


def _notifier_loop(notifier, stop, errors):
    while not stop.is_set():
        try:
            notifier.run_once()
        except Exception as exc:  # noqa: BLE001 - the test asserts no loop failure
            errors.append(exc)
        time.sleep(0.05)


@pytest.mark.parametrize("run", range(3))
def test_record_delivery_cli_with_a_running_notifier(tmp_path, fake, run):
    """U13: at least 3/p runs with p ~ 1; the hold forces held attempt, delivered, its close."""
    config = _config(timeout=30.0, initial=1.0, maximum=2.0)
    hold = Hold()
    fake.script.append(hold)
    notifier = _notifier(tmp_path, _rows("synthetic:%d" % run), config,
                         _irm(config, transport=25.0), clock=_real_clock)
    config_path = _write_config(tmp_path, config)
    stop, errors = threading.Event(), []
    loop = threading.Thread(target=_notifier_loop, args=(notifier, stop, errors), daemon=True)
    loop.start()
    try:
        _wait_for(lambda: notifier.jobs() and "attempt" in _kinds(notifier.store_path))
        key = notifier.jobs()[0]["incident_key"]
        out = tmp_path / "cli.out"
        process = _cli_process(out, notifier.store_path, config_path, key)
        try:
            _wait_for(lambda: "delivered" in _kinds(notifier.store_path, key))
            time.sleep(0.5)  # several CLI polls with the held publish still open
            assert process.poll() is None and SAFE not in out.read_text(encoding="utf-8")
            assert "provider_accepted" not in _kinds(notifier.store_path, key)
            hold.release.set()
            assert process.wait(60) == 0
        finally:
            if process.poll() is None:
                process.kill()
    finally:
        hold.release.set()
        stop.set()
        loop.join(60)
    assert errors == [] and not loop.is_alive()
    assert SAFE in out.read_text(encoding="utf-8")
    events = [(sequence, kind) for sequence, kind, channel, _ in _events(notifier.store_path, key)
              if channel in ("irm", None) or kind == "delivered"]
    attempts = [sequence for sequence, kind in events if kind == "attempt"]
    [delivered] = [sequence for sequence, kind in events if kind == "delivered"]
    accepted = [sequence for sequence, kind in events if kind == "provider_accepted"]
    assert attempts == [attempts[0]] and attempts[0] < delivered < accepted[-1]
    assert not [sequence for sequence in attempts if sequence > delivered]
    assert _corrupt_files(tmp_path) == []


def _late_closed(journal, key):
    return "late_outcome" in _kinds(journal, key)


@pytest.mark.parametrize("order", ["timeout_first", "late_first", "wait_expires"])
def test_record_delivery_cli_waits_for_the_late_close(tmp_path, fake, monkeypatch, order):
    """U14: a drip-fed publish outlives publish_timeout_s; delivery_failed {timeout} is not a
    close, so ``safe`` waits for late_outcome. Both journal orders, plus a wait that expires."""
    config = _config(timeout=1.0, initial=30.0, maximum=30.0)
    drip = Drip(interval=0.1)
    fake.script.append(drip)
    notifier = _notifier(tmp_path, _rows("synthetic:1"), config, _irm(config, transport=0.5),
                         clock=_real_clock)
    journal, config_path = notifier.store_path, _write_config(tmp_path, config)
    key = incident_key("synthetic:1")
    abandoned = threading.Event()
    if order == "late_first":
        bounded = notifier._bounded_publish

        def close_after_late(channel, job_key, payload):
            result = bounded(channel, job_key, payload)
            if channel.name == "irm" and result == (None, "timeout"):
                abandoned.set()  # the round gave up; its close now waits for late_outcome
                _wait_for(lambda: _late_closed(journal, job_key), 60)
            return result

        monkeypatch.setattr(notifier, "_bounded_publish", close_after_late)
    errors = []
    round_thread = threading.Thread(
        target=lambda: errors.extend(_capture(notifier.run_once)), daemon=True)
    round_thread.start()
    out = tmp_path / "cli.out"
    try:
        _wait_for(lambda: "attempt" in _kinds(journal, key))
        process = _cli_process(out, journal, config_path, key,
                               wait_s=3 if order == "wait_expires" else 60)
        try:
            _wait_for(lambda: "delivered" in _kinds(journal, key))
            if order == "late_first":
                assert abandoned.wait(30)
                assert not any(kind == "delivery_failed" for _, kind, _, _ in _events(journal, key))
            else:
                _wait_for(lambda: any(kind == "delivery_failed" and detail == {"outcome": "timeout"}
                                      for _, kind, _, detail in _events(journal, key)))
                time.sleep(1.0)  # the CLI polls past the timeout row and must not call it safe
            if order == "wait_expires":
                assert process.wait(60) == 3
                text = out.read_text(encoding="utf-8")
                assert NOT_SAFE in text and SAFE not in text
                assert not _late_closed(journal, key)
            else:
                assert process.poll() is None, "the CLI ended before the drip completed"
                assert SAFE not in out.read_text(encoding="utf-8")
                assert not _late_closed(journal, key)
            drip.release.set()
            _wait_for(lambda: _late_closed(journal, key), 60)
            if order != "wait_expires":
                assert process.wait(60) == 0
                assert SAFE in out.read_text(encoding="utf-8")
        finally:
            if process.poll() is None:
                process.kill()
    finally:
        drip.release.set()
        round_thread.join(60)
    assert errors == [] and not round_thread.is_alive()
    irm_events = [(kind, detail) for _, kind, channel, detail in _events(journal, key)
                  if channel == "irm"]
    kinds = [kind for kind, _ in irm_events]
    timeout_row = kinds.index("delivery_failed")
    assert irm_events[timeout_row][1] == {"outcome": "timeout"}
    if order == "late_first":
        assert kinds.index("late_outcome") < timeout_row
    elif order == "timeout_first":
        assert timeout_row < kinds.index("late_outcome")
    if order == "wait_expires":
        rerun = tmp_path / "rerun.out"
        process = _cli_process(rerun, journal, config_path, key, wait_s=30)
        assert process.wait(60) == 0
        text = rerun.read_text(encoding="utf-8")
        assert ALREADY in text and SAFE in text
    assert kinds.count("delivered") == 1 and _corrupt_files(tmp_path) == []


def _capture(function):
    try:
        function()
    except Exception as exc:  # noqa: BLE001 - returned for the test to assert on
        return [exc]
    return []


def _hot_rollback_journal(store):
    """A valid journal left with a hot rollback journal by a writer that died mid-transaction."""
    code = ("import os, sqlite3, sys\n"
            "db = sqlite3.connect(sys.argv[1], isolation_level=None)\n"
            "db.execute('PRAGMA cache_size=1')\n"
            "db.execute('BEGIN IMMEDIATE')\n"
            "for number in range(400):\n"
            "    db.execute(\"INSERT INTO events(incident_key, kind, channel, at, detail) \"\n"
            "               \"VALUES (?, 'filler', NULL, 'at', ?)\", (str(number), 'y' * 2000))\n"
            "os._exit(1)\n")
    subprocess.run([sys.executable, "-c", code, str(store)], check=False, timeout=120)
    assert Path(str(store) + "-journal").is_file()


def _snapshot(directory):
    return {path.name: path.read_bytes() for path in Path(directory).iterdir() if path.is_file()}


def _inert(config):
    return {spec.name: SimpleNamespace(name=spec.name, kind=spec.kind) for spec in config.channels}


def test_record_delivery_cli_refuses_journal_states(tmp_path, fake, capsys):
    """U15."""
    config = _config()
    key = "b" * 64
    missing = tmp_path / "missing" / "journal.sqlite"
    config_path = _write_config(tmp_path, config)
    assert _cli("--journal", missing, "--config", config_path, key) == 2
    assert "record-delivery refused: journal-missing" in capsys.readouterr().err
    assert not missing.parent.exists()

    def fresh(name):
        directory = tmp_path / name
        directory.mkdir()
        return directory, directory / "journal.sqlite"

    def initialized(store):
        IncidentNotifier(store, read_incidents=_rows(), channels=_inert(config), config=config,
                         clock=Clock())

    cases = {
        "empty": lambda store: store.write_bytes(b""),
        "unreadable": _unreadable,
        "integrity": lambda store: (initialized(store), _null_reason(store)),
        "schema": _foreign_schema,
        "hot": lambda store: (initialized(store), _hot_rollback_journal(store)),
    }
    for name, damage in cases.items():
        directory, store = fresh(name)
        damage(store)
        before = _snapshot(directory)
        assert _cli("--journal", store, "--config", config_path, key) == 2, name
        assert "record-delivery refused: journal-faulty" in capsys.readouterr().err, name
        assert _snapshot(directory) == before, name
        if name != "hot":  # the hot journal is a pre-check refusal only (C3 item 3)
            with pytest.raises(NotifierStoreError):
                IncidentNotifier(store, read_incidents=_rows(), channels=_inert(config),
                                 config=config, clock=Clock(), rebuild=False)
            assert _snapshot(directory) == before, name
        assert _corrupt_files(directory) == [], name

    directory, _ = fresh("lock")
    notifier, key, locked_config = _published(directory, fake)
    journal = notifier.store_path
    before = _events(journal)
    holding, done = threading.Event(), threading.Event()

    def hold_lock():
        with closing(sqlite3.connect(journal, isolation_level=None)) as db:
            db.execute("BEGIN IMMEDIATE")
            holding.set()
            done.wait(8)
            db.execute("ROLLBACK")

    holder = threading.Thread(target=hold_lock, daemon=True)
    holder.start()
    assert holding.wait(10)
    started = time.monotonic()
    try:
        assert _cli("--journal", journal, "--config", locked_config, key) == 2
        elapsed = time.monotonic() - started
    finally:
        done.set()
        holder.join(20)
    assert "record-delivery refused: journal-lock" in capsys.readouterr().err
    assert elapsed >= 5
    assert _events(journal) == before and _corrupt_files(directory) == []
    assert _cli("--journal", journal, "--config", locked_config, key) == 0  # lock-free control
    assert SAFE in capsys.readouterr().out


# -- Q1-Q6: real owner, notifier, real channel, loopback fake IRM -----------------------------

def test_q1_each_incident_class_pages_once_as_important(tmp_path, fake):
    """Q1."""
    for name, (scenario, reason) in _INCIDENTS.items():
        account = scenario(tmp_path / name)
        [row] = account.incidents
        start = len(fake.posts())
        notifier = _notifier(tmp_path / name, _owner_reader(account), _config(), _irm())
        notifier.run_once()
        posts = fake.posts()[start:]
        assert len(posts) == 1, name
        assert posts[0]["alert_uid"] == incident_key(row["incident_id"]), name
        assert (posts[0]["severity"], posts[0]["state"]) == ("critical", "alerting"), name
        assert posts[0]["title"].endswith(": " + reason), name


def test_q2_cutoff_and_refusals_page_nothing(tmp_path, fake):
    """Q2 (the #628 T2 cases, through the IRM channel)."""
    cases = {}
    settled = replace(binding()["settlement"], equity=100_000.0)
    account, _ = _rehearsal_owner(tmp_path / "capacity", [BrokerResult("accepted")] * 2,
                                  settlement=settled)
    aegis = replace(intent("aegis"), leg_id="aegis_6j", qty=8, side=leg("aegis_6j").entry_side)
    assert _dispatch(account, aegis, "aegis", NOW).transport_state == "accepted"
    assert _dispatch(account, _other_leg_entry("orb", NOW), "orb",
                     NOW).refusal_reason == "insufficient_observed_capacity"
    cases["capacity"] = account
    account, _ = _rehearsal_owner(tmp_path / "zero-size", [BrokerResult("accepted")])
    assert _dispatch(account, replace(intent("too-wide"), stop_dist_pts=10**6), "too-wide",
                     NOW).refusal_reason == "zero_size"
    cases["zero-size"] = account
    account, _ = _rehearsal_owner(tmp_path / "duplicate", [BrokerResult("accepted")] * 2)
    assert _dispatch(account, intent("signal"), "signal", NOW).transport_state == "accepted"
    assert _dispatch(account, intent("signal"), "signal-redelivered",
                     NOW).refusal_reason == "duplicate_operation"
    cases["duplicate"] = account
    account, _ = _rehearsal_owner(tmp_path / "incomplete-barrier", [])
    for leg_id in LEGS[:3]:
        account.record_partial_bar(leg_id, NOW, {"close": 100, "leg": leg_id}, acquired_at=NOW)
    cases["incomplete-barrier"] = account
    account, _ = _rehearsal_owner(tmp_path / "cutoff", [])
    account.advance_schedule(now=SESSION.risk_add_cutoff)
    assert (account.permission, account.authority) == ("HALTED", "SCHEDULED_EXIT")
    cases["cutoff"] = account
    for name, account in cases.items():
        assert account.incidents == (), name
        notifier = _notifier(tmp_path / name, _owner_reader(account), _config(), _irm())
        notifier.run_once()
        assert notifier.jobs() == (), name
    assert fake.requests == []


def test_q3_retries_reuse_alert_uid_and_one_group(tmp_path, fake):
    """Q3: 503, then a hang past the transport timeout, then 200."""
    clock, config = Clock(), _config(timeout=2.0)
    account = _operator(tmp_path)
    fake.script.extend([503, HANG, 200])
    notifier = _notifier(tmp_path, _owner_reader(account), config, _irm(config, transport=0.5),
                         clock=clock)
    for delay in (0, 5, 10):
        clock.advance(delay)
        notifier.run_once()
    key = incident_key(account.incidents[0]["incident_id"])
    posts = fake.posts()
    assert len(posts) == 3 and {post["alert_uid"] for post in posts} == {key}
    assert len(fake.groups) == 1
    irm = [(kind, detail.get("outcome")) for _, kind, channel, detail
           in _events(notifier.store_path, key) if channel == "irm"]
    assert irm == [("attempt", None), ("delivery_failed", "unknown"),
                   ("attempt", None), ("delivery_failed", "GrafanaIRMTransportError"),
                   ("attempt", None), ("provider_accepted", None)]


def test_q4_acceptance_is_not_delivery(tmp_path, fake):
    """Q4."""
    clock, config = Clock(), _config()
    account = _operator(tmp_path)
    notifier = _notifier(tmp_path, _owner_reader(account), config, _irm(config), clock=clock)
    notifier.run_once()
    key = incident_key(account.incidents[0]["incident_id"])
    [accepted] = [detail for _, kind, _, detail in _events(notifier.store_path, key)
                  if kind == "provider_accepted"]
    assert len(accepted["evidence_digest"]) == 64
    assert "delivered" not in _kinds(notifier.store_path, key)
    assert notifier.jobs()[0]["state"] == "pending"
    clock.advance(5)
    notifier.run_once()
    assert [post["alert_uid"] for post in fake.posts()] == [key, key]


@pytest.mark.parametrize("failure", [403, 404, 429, 500, "refused", HANG])
def test_q5_provider_failure_isolated_and_channel_loss_recorded(tmp_path, fake, monkeypatch,
                                                                failure):
    """Q5: IRM is the only delivering channel; local_file evidence is still written."""
    clock, config = Clock(), _config(timeout=2.0)
    account = _operator(tmp_path)
    if failure == "refused":
        monkeypatch.setenv(URL_ENV, _closed_port_url())
    else:
        fake.script.extend([failure] * 4)
    notifier = _notifier(tmp_path, _owner_reader(account), config, _irm(config, transport=0.5),
                         clock=clock)
    before = _owner_view(account)
    errors = []
    round_thread = threading.Thread(target=lambda: errors.extend(_capture(notifier.run_once)))
    round_thread.start()
    account.halt("operator-stop:concurrent", "operator", now=NOW + timedelta(seconds=30))
    round_thread.join(30)
    assert errors == [] and not round_thread.is_alive()
    after = _owner_view(account)
    assert after[1][:1] == before[1] and len(after[1]) == 2  # only the concurrent halt landed
    key = incident_key(before[1][0]["incident_id"])
    clock.advance(5)
    view = _owner_view(account)
    notifier.publish_due()
    assert _owner_view(account) == view
    kinds = _kinds(notifier.store_path, key)
    assert kinds.count("all_channels_lost") == 1 and "provider_accepted" not in kinds
    assert kinds.count("local_evidence") == 2
    assert (tmp_path / "alerts" / (key + ".json")).is_file()
    assert key in notifier.channels_lost()


def test_q6_restart_keeps_identity_and_hides_url(tmp_path, fake, caplog, capsys):
    """Q6."""
    caplog.set_level(logging.DEBUG)
    clock, config = Clock(), _config()
    account = _operator(tmp_path)
    fake.script.extend([500, 202])
    first = _notifier(tmp_path, _owner_reader(account), config, _irm(config), clock=clock)
    first.run_once()
    digest = first.jobs()[0]["config_digest"]
    del first
    restarted = _notifier(tmp_path, _owner_reader(account), _config(), _irm(), clock=clock)
    clock.advance(5)
    restarted.run_once()
    posts = fake.posts()
    assert len(posts) == 2 and posts[0]["alert_uid"] == posts[1]["alert_uid"]
    assert len(fake.groups) == 1
    assert [job["config_digest"] for job in restarted.jobs()] == [digest] == [config.digest]
    captured = capsys.readouterr()
    for surface in (restarted.store_path.read_bytes().decode("latin-1"),
                    json.dumps(restarted.events()), json.dumps(posts), caplog.text,
                    captured.out, captured.err, json.dumps(config.resolved())):
        assert TOKEN not in surface and "127.0.0.1:" not in surface


# -- review folds on #676 (Codex at 6b24df0) and #677 ------------------------------------------

def test_last_status_is_cleared_before_each_post(fake):
    """r4179168630: a transport failure after an HTTP answer reports no stale status."""
    config = _config(timeout=2.0)
    channel = _irm(config, transport=0.5)
    payload = {"reason": "operator", "detected_at": NOW.isoformat()}
    fake.script.extend([202, HANG])
    assert channel.publish("a" * 64, payload).state == "accepted"
    assert channel.last_status == 202  # twin: an answered post records its status
    with pytest.raises(irm_module.GrafanaIRMTransportError):
        channel.publish("a" * 64, payload)
    assert channel.last_status is None


@pytest.mark.parametrize("wait", ["nan", "inf", "-inf", "0", "-1"])
def test_record_delivery_refuses_a_non_finite_or_non_positive_wait(tmp_path, fake, capsys, wait):
    """r4179168633: --wait-s must be finite and positive; refused before any event."""
    notifier, key, config_path = _published(tmp_path, fake)
    before = _events(notifier.store_path)
    capsys.readouterr()
    assert _cli("--journal", notifier.store_path, "--config", config_path, "--wait-s=" + wait,
                key) == 2
    assert "record-delivery refused: wait-s" in capsys.readouterr().err
    assert _events(notifier.store_path) == before


def test_record_delivery_accepts_a_finite_positive_wait(tmp_path, fake, capsys):
    """Twin of the --wait-s refusal: a finite positive bound records and reports safe."""
    notifier, key, config_path = _published(tmp_path, fake)
    assert _cli("--journal", notifier.store_path, "--config", config_path, "--wait-s", "0.5",
                key) == 0
    assert SAFE in capsys.readouterr().out


def test_record_delivery_refuses_a_config_other_than_the_journaled_one(tmp_path, fake, capsys):
    """r4179168634: the supplied config's digest must equal the job's config_digest, so its
    channel roles are the ones the notifier ran with; the twin is the journal's own config."""
    notifier, key, config_path = _published(tmp_path, fake)
    other = tmp_path / "other.json"
    other.write_text(json.dumps(_config(timeout=3.0).resolved()), encoding="utf-8")
    before = _events(notifier.store_path)
    capsys.readouterr()
    assert _cli("--journal", notifier.store_path, "--config", other, key) == 2
    assert "record-delivery refused: config-mismatch" in capsys.readouterr().err
    assert _events(notifier.store_path) == before
    assert _cli("--journal", notifier.store_path, "--config", config_path, key) == 0
    assert SAFE in capsys.readouterr().out


def test_record_delivery_reports_a_concurrent_delivery_as_already_delivered(tmp_path, fake,
                                                                          monkeypatch, capsys):
    """r4179168638: a job delivered by another writer between the pre-check and the record
    gets no second event, and the CLI says so; the twin records and says recorded."""
    notifier, key, config_path = _published(tmp_path, fake)
    precheck = cli_module._precheck

    def deliver_concurrently(*args):
        state = precheck(*args)
        notifier.record_delivery(key, "irm", "c" * 64)
        return state

    monkeypatch.setattr(cli_module, "_precheck", deliver_concurrently)
    capsys.readouterr()
    assert _cli("--journal", notifier.store_path, "--config", config_path, key) == 0
    out = capsys.readouterr().out
    assert ALREADY in out and "recorded delivered" not in out and SAFE in out
    assert _kinds(notifier.store_path, key).count("delivered") == 1
    monkeypatch.setattr(cli_module, "_precheck", precheck)
    (tmp_path / "twin").mkdir()
    twin, twin_key, twin_config = _published(tmp_path / "twin", fake)
    assert _cli("--journal", twin.store_path, "--config", twin_config, twin_key) == 0
    out = capsys.readouterr().out
    assert "recorded delivered" in out and ALREADY not in out


def _writable_connects(source):
    """Every sqlite3 connect in ``source`` that is not a literal mode=ro URI with uri=True."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom) and node.module == "sqlite3":
            found.append(("from-import", node.lineno))
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "connect"):
            continue
        literals = [item.value for item in ast.walk(node.args[0]) if isinstance(item, ast.Constant)
                    and isinstance(item.value, str)] if node.args else []
        uri = [keyword.value for keyword in node.keywords if keyword.arg == "uri"]
        if not (any("mode=ro" in value for value in literals) and len(uri) == 1
                and isinstance(uri[0], ast.Constant) and uri[0].value is True):
            found.append(("connect", node.lineno))
    return found


def test_operator_cli_connects_are_read_only_uris():
    """#677 r4179166723: the gate's EXCLUDED entry skips this whole module, so this test pins
    every sqlite3 connect in it to a literal mode=ro URI with uri=True."""
    source = CLI.read_text(encoding="utf-8")
    assert "sqlite3.connect(" in source and _writable_connects(source) == []
    mutations = (
        source + "\n\ndef _writer(path):\n    return sqlite3.connect(path)\n",
        source.replace('"?mode=ro", uri=True', '"?mode=rw", uri=True'),
        source.replace('"?mode=ro", uri=True', '"?mode=ro", uri=False'),
        source + "\n\nfrom sqlite3 import connect as _open\n",
    )
    for mutated in mutations:
        assert mutated != source and _writable_connects(mutated), mutated[-80:]
