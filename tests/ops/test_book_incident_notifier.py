"""Book-route incident notifier (card: docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md).

Every case runs against a real ``BookAccountOwner`` in a disposable ``tmp_path`` store with a
synthetic account, session and clock, and publishes only through ``FakeChannel`` or
``LocalFileChannel``. Nothing here arms, deploys, contacts a broker or provider, or notifies an
external party. The evidence class is *Synthetic / replay engineering*: real delivery,
acknowledgment and the external heartbeat stay owed to D-MON/T13 (card §8).
"""
from __future__ import annotations

import ast
from contextlib import closing, contextmanager
from dataclasses import replace
from datetime import datetime, timedelta
import functools
import hashlib
import inspect
import json
from pathlib import Path
import sqlite3
import threading
import time

import pytest

from c1_rail import book_incident_notifier as notifier_module
from c1_rail.book_account_owner import AccountOwnerError, BookAccountOwner, BrokerResult
from c1_rail.book_incident_notifier import (
    FakeChannel,
    IncidentNotifier,
    LocalFileChannel,
    NotifierConfig,
    NotifierConfigError,
    NotifierStoreError,
    PublishResult,
    incident_key,
)
from c1_rail.book_policy import leg
from c1_rail_telemetry import assert_no_secrets
from test_attended_incident_rehearsal import (
    LEGS,
    SOURCE_TIMEOUT,
    _ambiguous_protection,
    _complete_bar,
    _dispatch,
    _other_leg_entry,
    _rehearsal_owner,
)
from test_book_account_owner import NOW, SESSION, binding, intent


DELIVERED = PublishResult("accepted", delivered=True, evidence_digest="e" * 64)
ACCEPTED = PublishResult("accepted")
REJECTED = PublishResult("rejected")
UNKNOWN = PublishResult("unknown")


class Clock:
    def __init__(self, at=NOW):
        self.at = at

    def __call__(self):
        return self.at

    def advance(self, seconds):
        self.at += timedelta(seconds=seconds)


def _config(*names, timeout=1.0, initial=5.0, maximum=300.0):
    return NotifierConfig.from_mapping({
        "channels": [{"name": name, "kind": "fake", "secret_ref": "env:" + name.upper() + "_REF"}
                     for name in names or ("primary",)],
        "publish_timeout_s": timeout,
        "retry_initial_s": initial,
        "retry_max_s": maximum,
    })


def _notifier(tmp_path, account, *channels, clock=None, config=None, store="journal.sqlite"):
    channels = channels or (FakeChannel("primary"),)
    config = config or _config(*(channel.name for channel in channels))
    return IncidentNotifier(
        tmp_path / store,
        read_incidents=functools.partial(BookAccountOwner.read_incidents, account.path),
        channels={channel.name: channel for channel in channels},
        config=config,
        clock=clock or Clock(),
    )


def _kinds(notifier, key=None):
    return [(row["kind"], row["channel"]) for row in notifier.events(key)]


def _owner_view(account):
    return account.status(), account.incidents


# -- T1: every committed incident row yields exactly one job ---------------------------------

def _operator(tmp_path):
    account, _ = _rehearsal_owner(tmp_path, [])
    account.halt("operator-stop:synthetic", "operator", now=NOW + timedelta(seconds=5))
    return account


def _protection(tmp_path):
    return _ambiguous_protection(tmp_path, "identity").owner


def _feed_silence(tmp_path):
    account, _ = _rehearsal_owner(tmp_path, [BrokerResult("accepted")])
    _complete_bar(account, NOW)
    account.check_source_silence(now=NOW + SOURCE_TIMEOUT + timedelta(seconds=1),
                                 max_silence=SOURCE_TIMEOUT)
    return account


def _ordinary_unknown(tmp_path):
    account, _ = _rehearsal_owner(tmp_path, [BrokerResult("unknown")])
    assert _dispatch(account, intent(), "base", NOW).transport_state == "unknown"
    return account


def _barrier_expiry(tmp_path):
    account, _ = _rehearsal_owner(tmp_path, [])
    account.record_partial_bar(LEGS[0], NOW, {"close": 100, "leg": LEGS[0]}, acquired_at=NOW)
    assert account.expire_partial_barrier(NOW, now=NOW + timedelta(minutes=10))
    return account


_INCIDENTS = {
    "operator": (_operator, "operator"),
    "protection": (_protection, "protection"),
    "feed-silence": (_feed_silence, "feed"),
    "ordinary-unknown": (_ordinary_unknown, "execution"),
    "barrier-expiry": (_barrier_expiry, "barrier"),
}


def test_each_committed_incident_yields_one_job_keyed_by_incident_id(tmp_path):
    for name, (scenario, reason) in _INCIDENTS.items():
        account = scenario(tmp_path / name)
        incidents = account.incidents
        assert len(incidents) == 1 and incidents[0]["reason"] == reason, name
        notifier = _notifier(tmp_path / name, account)
        assert notifier.poll() == (incident_key(incidents[0]["incident_id"]),), name
        assert [(job["incident_key"], job["reason"], job["detected_at"], job["generation"])
                for job in notifier.jobs()] == [
            (incident_key(row["incident_id"]), row["reason"], row["at"], row["generation"])
            for row in incidents], name
        # Detection is the owner's own timestamp, copied rather than re-stamped.
        detected = [row for row in notifier.events() if row["kind"] == "detected"]
        assert [row["at"] for row in detected] == [incidents[0]["at"]], name
        assert notifier.poll() == (), name
        assert len(notifier.jobs()) == 1, name


# -- T2: refusals and the scheduled cutoff are not incidents -----------------------------------

def test_scheduled_cutoff_and_refusals_yield_no_job(tmp_path):
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
    assert len(account.retained_partial_bars) == 3
    cases["incomplete-barrier"] = account

    account, _ = _rehearsal_owner(tmp_path / "cutoff", [])
    account.advance_schedule(now=SESSION.risk_add_cutoff)
    assert (account.permission, account.authority) == ("HALTED", "SCHEDULED_EXIT")
    cases["cutoff"] = account

    for name, account in cases.items():
        assert account.incidents == (), name
        channel = FakeChannel("primary")
        notifier = _notifier(tmp_path / name, account, channel)
        notifier.run_once()
        assert notifier.jobs() == () and notifier.events() == () and channel.calls == [], name


# -- T3: the notifier never takes the owner's write lock ---------------------------------------

def test_halt_commits_while_notifier_reads(tmp_path):
    """Supplementary to the binding guard below; it does not pin the seam on its own.

    Review 2026-10-02 (P3): a reader mutated to hold a read transaction for 50 ms still
    passes this test. ``test_notifier_never_opens_owner_with_begin_immediate`` is the test
    that fails under that mutation; do not delete it as redundant with this one.
    """
    account, _ = _rehearsal_owner(tmp_path, [])
    notifier = _notifier(tmp_path, account)
    generation = account.status()["generation"]
    stop, errors, reads = threading.Event(), [], [0]

    def read_loop():
        while not stop.is_set():
            try:
                notifier.poll()
                reads[0] += 1
            except Exception as exc:  # noqa: BLE001 - the test records any reader failure
                errors.append(exc)

    reader = threading.Thread(target=read_loop)
    reader.start()
    try:
        deadline = time.monotonic() + 10
        while reads[0] == 0 and not errors and time.monotonic() < deadline:
            time.sleep(0.01)
        for number in range(20):
            account.halt("operator-stop:%d" % number, "operator",
                          now=NOW + timedelta(seconds=number))
    finally:
        stop.set()
        reader.join(10)
    assert not reader.is_alive() and errors == [] and reads[0] > 0
    assert account.status()["generation"] == generation + 20
    assert len(account.incidents) == 20
    notifier.poll()
    assert {job["incident_key"] for job in notifier.jobs()} == {
        incident_key(row["incident_id"]) for row in account.incidents}

    # Rollback journal: a reader's SHARED lock delays a halt's commit but does not fail it.
    # The accessor holds SHARED only for one SELECT, far inside the owner's 5 s busy timeout.
    held = sqlite3.connect(account.path.resolve().as_uri() + "?mode=ro", uri=True,
                           isolation_level=None)
    halt_errors = []
    try:
        held.execute("BEGIN")
        held.execute("SELECT * FROM incidents").fetchall()

        def halt():
            try:
                account.halt("operator-stop:held", "operator", now=NOW + timedelta(minutes=1))
            except Exception as exc:  # noqa: BLE001
                halt_errors.append(exc)

        writer = threading.Thread(target=halt)
        writer.start()
        time.sleep(0.3)
        assert writer.is_alive()  # waiting on the reader, not failed
        held.execute("COMMIT")
        writer.join(10)
    finally:
        held.close()
    assert halt_errors == []
    assert account.status()["generation"] == generation + 21


def test_notifier_never_opens_owner_with_begin_immediate(tmp_path, monkeypatch):
    """BINDING guard for the C-1 seam (card §6 T3, §10): every owner connection is
    ``?mode=ro`` and issues no BEGIN or write; the accessor source names no BEGIN."""
    account = _operator(tmp_path)
    opened, statements = [], []
    real_connect = sqlite3.connect

    def recording_connect(database, *args, **kwargs):
        connection = real_connect(database, *args, **kwargs)
        if "owner.sqlite" in str(database):
            opened.append(str(database))
            connection.set_trace_callback(statements.append)
        return connection

    monkeypatch.setattr(sqlite3, "connect", recording_connect)
    notifier = _notifier(tmp_path, account)
    notifier.run_once()
    monkeypatch.undo()

    assert opened and all(uri.endswith("?mode=ro") for uri in opened)
    assert statements
    assert not [sql for sql in statements
                if any(word in sql.upper() for word in ("BEGIN", "INSERT", "UPDATE", "DELETE"))]
    # The notifier's own journal is a durable store with immediate transactions; the owner
    # accessor it reads through takes none, and the notifier never names the owner's lock paths.
    accessor = inspect.getsource(BookAccountOwner.read_incidents)
    assert "BEGIN" not in accessor and "?mode=ro" in accessor
    source = Path(notifier_module.__file__).read_text(encoding="utf-8")
    assert not [name for name in ("._transaction(", ".serializer", "_halt_db", "BookAccountOwner(")
                if name in source]
    assert len(notifier.jobs()) == 1


# -- T4: channel failure never changes the owner ----------------------------------------------

def test_channel_failure_leaves_owner_status_and_incidents_equal(tmp_path):
    account = _operator(tmp_path)
    before = _owner_view(account)
    failures = {
        "raise": RuntimeError("synthetic provider outage"),
        "timeout": FakeChannel.HANG,
        "reject": REJECTED,
        "unknown": UNKNOWN,
    }
    expected = {"raise": "RuntimeError", "timeout": "timeout", "reject": "rejected",
                "unknown": "unknown"}
    for name, outcome in failures.items():
        channel = FakeChannel("primary", [outcome])
        notifier = _notifier(tmp_path, account, channel, store=name + ".sqlite",
                             config=_config("primary", timeout=0.05))
        try:
            notifier.run_once()
        finally:
            channel.release()
        assert _owner_view(account) == before, name
        assert notifier.jobs()[0]["state"] == "pending", name
        failed = [row for row in notifier.events() if row["kind"] == "delivery_failed"]
        assert [row["detail"]["outcome"] for row in failed] == [expected[name]], name
    assert _owner_view(account) == before


# -- T5: a duplicate incident report yields no second job --------------------------------------

def test_duplicate_incident_report_yields_no_second_job(tmp_path):
    account = _operator(tmp_path)
    notifier = _notifier(tmp_path, account)
    assert len(notifier.poll()) == 1
    account.halt("operator-stop:synthetic", "operator", now=NOW + timedelta(seconds=5))
    assert len(account.incidents) == 1
    assert notifier.poll() == ()
    assert len(notifier.jobs()) == 1
    assert [row["kind"] for row in notifier.events()].count("detected") == 1


# -- T6: retries keep one identity and never stop before delivery ------------------------------

def test_retry_reuses_dedup_key_and_appends_attempt(tmp_path):
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    clock = Clock()
    channel = FakeChannel("primary", [REJECTED, UNKNOWN, DELIVERED])
    notifier = _notifier(tmp_path, account, channel, clock=clock,
                         config=_config("primary", initial=5, maximum=300))
    notifier.run_once()
    notifier.run_once()  # not yet due: no new attempt
    assert len(channel.calls) == 1
    clock.advance(5)
    notifier.run_once()
    clock.advance(9)
    notifier.run_once()  # second backoff is 10 s: still not due
    clock.advance(1)
    notifier.run_once()
    assert [call_key for call_key, _payload in channel.calls] == [key] * 3
    assert [kind for kind, _ in _kinds(notifier, key)].count("attempt") == 3
    assert notifier.jobs()[0]["state"] == "delivered"

    # No retry cap: a channel that never delivers keeps being retried with capped backoff.
    account = _operator(tmp_path / "uncapped")
    clock = Clock()
    channel = FakeChannel("primary", [REJECTED] * 12)
    notifier = _notifier(tmp_path / "uncapped", account, channel, clock=clock,
                         config=_config("primary", initial=1, maximum=4))
    notifier.poll()
    gaps, last = [], None
    for _ in range(10):
        clock.at = datetime.fromisoformat(notifier.jobs()[0]["next_attempt_at"])
        if last is not None:
            gaps.append((clock.at - last).total_seconds())
        last = clock.at
        notifier.run_once()
    assert len(channel.calls) == 10 and notifier.jobs()[0]["state"] == "pending"
    assert gaps == [1, 2, 4, 4, 4, 4, 4, 4, 4]


# -- T7: attempt, provider acceptance and delivery are separate records ------------------------

def test_attempt_acceptance_delivery_recorded_as_separate_events(tmp_path):
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    clock = Clock()
    channel = FakeChannel("primary", [ACCEPTED])
    notifier = _notifier(tmp_path, account, channel, clock=clock)
    notifier.run_once()
    assert _kinds(notifier, key) == [("detected", None), ("attempt", "primary"),
                                     ("provider_accepted", "primary")]
    assert notifier.jobs()[0]["state"] == "pending"  # acceptance is not delivery

    clock.advance(1)
    notifier.record_delivery(key, "primary", "f" * 64)
    assert _kinds(notifier, key)[-1] == ("delivered", "primary")
    assert notifier.events(key)[-1]["detail"] == {"evidence_digest": "f" * 64}
    assert notifier.jobs()[0]["state"] == "delivered"
    clock.advance(3600)
    notifier.run_once()
    assert len(channel.calls) == 1  # delivered jobs are never republished

    account = _operator(tmp_path / "sync")
    key = incident_key(account.incidents[0]["incident_id"])
    notifier = _notifier(tmp_path / "sync", account, FakeChannel("primary", [DELIVERED]))
    notifier.run_once()
    assert _kinds(notifier, key) == [("detected", None), ("attempt", "primary"),
                                     ("provider_accepted", "primary"), ("delivered", "primary")]
    assert len({row["sequence"] for row in notifier.events(key)}) == 4


# -- T8: delivery failure routes on at once; losing every channel is recorded only -------------

def test_primary_delivery_failure_routes_to_next_channel_at_once(tmp_path):
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    primary = FakeChannel("primary", [REJECTED])
    secondary = FakeChannel("secondary", [DELIVERED])
    clock = Clock()
    notifier = _notifier(tmp_path, account, primary, secondary, clock=clock)
    notifier.run_once()
    assert [call[0] for call in primary.calls] == [key]
    assert [call[0] for call in secondary.calls] == [key]
    assert _kinds(notifier, key) == [
        ("detected", None), ("attempt", "primary"), ("delivery_failed", "primary"),
        ("attempt", "secondary"), ("provider_accepted", "secondary"), ("delivered", "secondary")]
    assert {row["at"] for row in notifier.events(key)[1:]} == {clock().isoformat()}


def test_all_channels_failing_records_all_channels_lost(tmp_path):
    account = _operator(tmp_path)
    before = _owner_view(account)
    key = incident_key(account.incidents[0]["incident_id"])
    clock = Clock()
    primary = FakeChannel("primary", [REJECTED, REJECTED, DELIVERED])
    secondary = FakeChannel("secondary", [RuntimeError("down"), UNKNOWN])
    notifier = _notifier(tmp_path, account, primary, secondary, clock=clock,
                         config=_config("primary", "secondary", initial=5))
    notifier.run_once()
    assert notifier.channels_lost() == (key,)
    clock.advance(5)
    notifier.run_once()
    assert [kind for kind, _ in _kinds(notifier, key)].count("all_channels_lost") == 1
    clock.advance(10)
    notifier.run_once()
    assert notifier.channels_lost() == ()
    assert _kinds(notifier, key)[-1] == ("channels_restored", None)
    assert notifier.jobs()[0]["state"] == "delivered"
    assert _owner_view(account) == before  # recorded only: no rail action


# -- T9: no broker, dispatch, arm, config-write or owner-mutation path -------------------------

_ALLOWED_IMPORTS = {
    "__future__", "collections.abc", "contextlib", "dataclasses", "datetime", "hashlib", "json", "math",
    "os", "pathlib", "re", "sqlite3", "threading", "typing", "c1_rail_telemetry",
}
_MUTATORS = ("halt", "dispatch", "boot", "activate", "record_input_incident", "observe")


def _reachable(root):
    """Objects reachable from ``root`` through state, containers, partials and methods.

    Function globals are not followed: a plain function is reachable code, not a reference
    to an owner instance.
    """
    seen, stack = set(), [root]
    while stack:
        item = stack.pop()
        if id(item) in seen or isinstance(item, (str, bytes, int, float, bool, type(None))):
            continue
        seen.add(id(item))
        yield item
        if isinstance(item, dict):
            stack.extend(item.keys())
            stack.extend(item.values())
        elif isinstance(item, (list, tuple, set, frozenset)):
            stack.extend(item)
        elif isinstance(item, functools.partial):
            stack.extend((item.func, item.args, item.keywords))
        elif inspect.ismethod(item):
            stack.extend((item.__self__, item.__func__))
        elif inspect.isfunction(item):
            stack.extend(cell.cell_contents for cell in item.__closure__ or ())
        elif not isinstance(item, type) and hasattr(item, "__dict__"):
            stack.append(vars(item))


def test_notifier_has_no_broker_or_owner_mutation_path(tmp_path):
    tree = ast.parse(Path(notifier_module.__file__).read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add("." * node.level + (node.module or ""))
    imported = {name.lstrip(".") for name in imported}
    assert imported <= _ALLOWED_IMPORTS, imported - _ALLOWED_IMPORTS
    telemetry_names = {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
                       and (node.module or "").endswith("c1_rail_telemetry") for alias in node.names}
    assert telemetry_names == {"assert_no_secrets"}

    account = _operator(tmp_path)
    notifier = _notifier(tmp_path, account, FakeChannel("primary"),
                         LocalFileChannel("local", tmp_path / "alerts"),
                         config=NotifierConfig.from_mapping({"channels": [
                             {"name": "primary", "kind": "fake", "secret_ref": "env:PRIMARY_REF"},
                             {"name": "local", "kind": "local_file"}]}))
    notifier.run_once()
    for item in _reachable(notifier):
        assert not isinstance(item, BookAccountOwner)
        if not inspect.isfunction(item) and not isinstance(item, type):
            assert not [name for name in _MUTATORS if callable(getattr(item, name, None))], item


# -- T10: the payload is opaque and minimal ----------------------------------------------------

def test_payload_has_no_incident_id_text_account_or_secret(tmp_path):
    account = _ordinary_unknown(tmp_path)
    incident_id = account.incidents[0]["incident_id"]
    attempt_id = incident_id.split(":", 1)[1]
    channel = FakeChannel("primary", [ACCEPTED])
    local = LocalFileChannel("local", tmp_path / "alerts")
    config = NotifierConfig.from_mapping({"channels": [
        {"name": "primary", "kind": "fake", "secret_ref": "env:PRIMARY_REF"},
        {"name": "local", "kind": "local_file"}]})
    notifier = _notifier(tmp_path, account, channel, local, config=config)
    notifier.run_once()
    ((key, payload),) = channel.calls
    assert key == incident_key(incident_id)
    assert set(payload) == {"kind", "idempotency_key", "reason", "detected_at"}
    assert payload["idempotency_key"] == key and payload["reason"] == "execution"
    written = [path.read_text(encoding="utf-8") for path in (tmp_path / "alerts").iterdir()] \
        if (tmp_path / "alerts").exists() else []
    for text in [json.dumps(payload)] + written + [json.dumps(notifier.events())]:
        for private in (incident_id, attempt_id, account.account):
            assert private not in text
    assert_no_secrets(payload)

    local_first = _notifier(tmp_path / "local", account, local, FakeChannel("pager", [ACCEPTED]),
                            config=NotifierConfig.from_mapping({"channels": [
                                {"name": "local", "kind": "local_file"},
                                {"name": "pager", "kind": "fake", "secret_ref": "env:PAGER_REF"}]}))
    local_first.run_once()
    (record,) = (tmp_path / "alerts").iterdir()
    body = json.loads(record.read_text(encoding="utf-8"))
    assert body == payload and record.name == key + ".json"
    assert local_first.jobs()[0]["state"] == "pending"  # local evidence is not delivery


# -- T11: config as code -----------------------------------------------------------------------

@pytest.mark.parametrize("channel", [
    {"name": "pager", "kind": "fake"},                                       # ref missing
    {"name": "pager", "kind": "fake", "secret_ref": "hunter2-literal"},     # inline value
    {"name": "pager", "kind": "fake", "secret_ref": "env:lower_case"},      # not a ref name
    {"name": "pager", "kind": "fake", "secret_ref": "env:PAGER_REF", "token": "abc"},
    {"name": "pager", "kind": "fake", "secret_ref": "env:PAGER_REF", "url": "https://x.test"},
    {"name": "pager", "kind": "smtp", "secret_ref": "env:PAGER_REF"},       # unknown kind
    {"name": "local", "kind": "local_file", "secret_ref": "sk-inline"},     # inline value
])
def test_config_requires_secret_refs_and_rejects_inline_values(channel):
    with pytest.raises(NotifierConfigError):
        NotifierConfig.from_mapping({"channels": [channel]})


def test_config_rejects_bad_shared_settings():
    good = {"name": "pager", "kind": "fake", "secret_ref": "secret:PAGER_ROUTING_KEY"}
    NotifierConfig.from_mapping({"channels": [good]})
    for raw in ({"channels": []},
                {"channels": [good, dict(good)]},
                {"channels": [good], "publish_timeout_s": 0},
                {"channels": [good], "retry_initial_s": 10, "retry_max_s": 5},
                {"channels": [good], "api_key": "inline"}):
        with pytest.raises(NotifierConfigError):
            NotifierConfig.from_mapping(raw)


def test_job_records_resolved_config_digest(tmp_path):
    account = _operator(tmp_path)
    config = _config("primary", timeout=2.0)
    notifier = _notifier(tmp_path, account, config=config)
    notifier.poll()
    canonical = json.dumps(config.resolved(), sort_keys=True, separators=(",", ":"))
    assert config.digest == hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    assert notifier.jobs()[0]["config_digest"] == config.digest
    assert _config("primary", timeout=3.0).digest != config.digest
    assert "PRIMARY_REF" in canonical  # the reference, never a value, is what is digested


def test_channels_must_match_config(tmp_path):
    account = _operator(tmp_path)
    with pytest.raises(NotifierConfigError):
        _notifier(tmp_path, account, FakeChannel("primary"), config=_config("other"))
    with pytest.raises(NotifierConfigError):
        _notifier(tmp_path, account, LocalFileChannel("primary", tmp_path / "alerts"),
                  config=_config("primary"))


# -- T12: restart keeps pending jobs and their identity ----------------------------------------

def test_restart_resumes_pending_jobs_with_same_identity(tmp_path):
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    clock = Clock()
    first = _notifier(tmp_path, account, FakeChannel("primary", [REJECTED]), clock=clock)
    first.run_once()
    job = first.jobs()[0]
    assert job["state"] == "pending"

    clock.advance(5)
    channel = FakeChannel("primary", [DELIVERED])
    restarted = _notifier(tmp_path, account, channel, clock=clock)
    restarted.run_once()
    assert [call[0] for call in channel.calls] == [key]
    (resumed,) = restarted.jobs()
    assert {name: resumed[name] for name in ("incident_key", "reason", "detected_at",
                                               "generation", "config_digest")} == \
        {name: job[name] for name in ("incident_key", "reason", "detected_at",
                                      "generation", "config_digest")}
    assert resumed["state"] == "delivered"
    kinds = [kind for kind, _ in _kinds(restarted, key)]
    assert kinds.count("detected") == 1 and kinds.count("attempt") == 2


# -- T13: an unavailable journal never touches the owner ---------------------------------------

def test_notifier_store_unavailable_does_not_touch_owner(tmp_path):
    account, _ = _rehearsal_owner(tmp_path, [])
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("occupied", encoding="utf-8")
    before = _owner_view(account)
    with pytest.raises(NotifierStoreError):
        _notifier(tmp_path, account, store="not-a-directory/journal.sqlite")
    assert _owner_view(account) == before

    account.halt("operator-stop:synthetic", "operator", now=NOW + timedelta(seconds=5))
    assert (account.permission, account.authority) == ("HALTED", "INTERVENTION")
    assert len(account.incidents) == 1

    notifier = _notifier(tmp_path, account)
    (tmp_path / "journal.sqlite").unlink()
    (tmp_path / "journal.sqlite").mkdir()  # the journal disappears under a running notifier
    halted = _owner_view(account)
    with pytest.raises(NotifierStoreError):
        notifier.run_once()
    assert _owner_view(account) == halted


# -- Review folds 2026-10-02 (notifier-review P2-1, P2-2, P3-1) --------------------------------

def _crash_when_delivered_update_runs(monkeypatch, store):
    """Fail between the delivered event and the job update when they share a transaction."""
    real_connect = sqlite3.connect

    class Crashing:
        def __init__(self, db):
            self._db, self._delivered = db, False

        def __getattr__(self, name):
            return getattr(self._db, name)

        def execute(self, sql, *args):
            if sql.startswith("INSERT INTO events") and args and args[0][1] == "delivered":
                self._delivered = True
            if sql.startswith("UPDATE jobs") and self._delivered:
                raise SystemExit("crash between the delivered event and the job update")
            return self._db.execute(sql, *args)

    def connect(database, *args, **kwargs):
        db = real_connect(database, *args, **kwargs)
        return Crashing(db) if Path(str(database)) == store else db

    monkeypatch.setattr(sqlite3, "connect", connect)


def test_delivered_outcome_and_job_update_commit_together(tmp_path, monkeypatch):
    """P2-1: the outcome events and the job update are one transaction (review probe)."""
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    store = tmp_path / "journal.sqlite"
    channel = FakeChannel("primary", [DELIVERED, DELIVERED])
    first = _notifier(tmp_path, account, channel)
    journal = first._journal

    @contextmanager
    def crash_after_delivered_commit():
        with journal() as db:
            yield db
        with closing(sqlite3.connect(store)) as raw:
            if raw.execute("SELECT COUNT(*) FROM events WHERE kind='delivered'").fetchone()[0]:
                raise SystemExit("crash after the delivered transaction committed")

    first._journal = crash_after_delivered_commit
    with pytest.raises(SystemExit):
        first.run_once()
    restarted = _notifier(tmp_path, account, channel)
    restarted.run_once()
    assert len(channel.calls) == 1  # no duplicate publish after restart
    assert restarted.jobs()[0]["state"] == "delivered"
    assert [kind for kind, _ in _kinds(restarted, key)].count("delivered") == 1

    # A failure after the event write but before the job update rolls both back: the journal
    # never shows delivered on a pending job, and the restart's one republish (the inherent
    # at-least-once window) reuses the same idempotency key.
    account = _operator(tmp_path / "rollback")
    key = incident_key(account.incidents[0]["incident_id"])
    store = tmp_path / "rollback" / "journal.sqlite"
    channel = FakeChannel("primary", [DELIVERED, DELIVERED])
    crashing = _notifier(tmp_path / "rollback", account, channel)
    _crash_when_delivered_update_runs(monkeypatch, store)
    with pytest.raises(SystemExit):
        crashing.run_once()
    monkeypatch.undo()
    restarted = _notifier(tmp_path / "rollback", account, channel)
    assert restarted.jobs()[0]["state"] == "pending"
    assert _kinds(restarted, key) == [("detected", None), ("attempt", "primary")]
    restarted.run_once()
    assert [call[0] for call in channel.calls] == [key, key]
    assert restarted.jobs()[0]["state"] == "delivered"
    assert [kind for kind, _ in _kinds(restarted, key)].count("delivered") == 1


def _local_config(*entries):
    return NotifierConfig.from_mapping({"channels": [
        {"name": name, "kind": "local_file"} if name.startswith("local")
        else {"name": name, "kind": "fake", "secret_ref": "env:" + name.upper() + "_REF"}
        for name in entries]})


def test_local_file_first_does_not_starve_delivering_channel(tmp_path):
    """P2-2: local-file acceptance is evidence only; the round continues (review probe)."""
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    local = LocalFileChannel("local", tmp_path / "alerts")
    primary = FakeChannel("primary", [DELIVERED])
    notifier = _notifier(tmp_path, account, local, primary, config=_local_config("local", "primary"))
    notifier.run_once()
    assert [call[0] for call in primary.calls] == [key]
    assert _kinds(notifier, key) == [
        ("detected", None), ("attempt", "local"), ("local_evidence", "local"),
        ("attempt", "primary"), ("provider_accepted", "primary"), ("delivered", "primary")]
    assert notifier.jobs()[0]["state"] == "delivered"
    assert (tmp_path / "alerts" / (key + ".json")).exists()
    with pytest.raises(ValueError):
        notifier.record_delivery(key, "local", "f" * 64)  # local evidence is never delivery


def test_config_without_a_delivering_channel_is_refused():
    for names in (("local",), ("local", "local_b")):
        with pytest.raises(NotifierConfigError):
            _local_config(*names)
    _local_config("local", "primary")


def test_all_delivering_channels_failing_records_lost_with_local_channel(tmp_path):
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    primary = FakeChannel("primary", [REJECTED])
    secondary = FakeChannel("secondary", [RuntimeError("down")])
    notifier = _notifier(tmp_path, account, primary, LocalFileChannel("local", tmp_path / "alerts"),
                         secondary, config=_local_config("primary", "local", "secondary"))
    notifier.run_once()
    assert notifier.channels_lost() == (key,)
    assert _kinds(notifier, key) == [
        ("detected", None), ("attempt", "primary"), ("delivery_failed", "primary"),
        ("attempt", "local"), ("local_evidence", "local"),
        ("attempt", "secondary"), ("delivery_failed", "secondary"), ("all_channels_lost", None)]
    assert notifier.jobs()[0]["state"] == "pending"


def test_run_once_publishes_due_jobs_when_poll_fails(tmp_path):
    """P3-1: an unreadable owner store does not stop publishing; the error still surfaces."""
    account = _operator(tmp_path)
    key = incident_key(account.incidents[0]["incident_id"])
    owner_unreadable = [False]

    def read_incidents():
        if owner_unreadable[0]:
            raise AccountOwnerError("account owner state unavailable")
        return BookAccountOwner.read_incidents(account.path)

    clock = Clock()
    channel = FakeChannel("primary", [REJECTED, DELIVERED])
    notifier = IncidentNotifier(tmp_path / "journal.sqlite", read_incidents=read_incidents,
                                channels={"primary": channel}, config=_config("primary", initial=5),
                                clock=clock)
    notifier.run_once()
    owner_unreadable[0] = True
    clock.advance(5)
    with pytest.raises(AccountOwnerError):
        notifier.run_once()
    assert [call[0] for call in channel.calls] == [key, key]
    assert notifier.jobs()[0]["state"] == "delivered"


def test_malformed_incident_row_is_skipped_and_recorded(tmp_path):
    account = _operator(tmp_path)
    (good,) = BookAccountOwner.read_incidents(account.path)
    at = NOW.isoformat()
    bad = [{"incident_id": "bad:reason", "reason": "", "at": at, "generation": 1},
           {"incident_id": "bad:at", "reason": "operator", "at": "not-a-time", "generation": 1},
           {"incident_id": "bad:generation", "reason": "operator", "at": at, "generation": True},
           {"reason": "operator", "at": at, "generation": 1},
           {"incident_id": "", "reason": "operator", "at": at, "generation": 1},
           None]
    rows = bad[:3] + [good] + bad[3:]
    notifier = IncidentNotifier(tmp_path / "journal.sqlite", read_incidents=lambda: rows,
                                channels={"primary": FakeChannel("primary")},
                                config=_config("primary"), clock=Clock())
    assert notifier.poll() == (incident_key(good["incident_id"]),)
    assert notifier.poll() == ()
    assert [job["incident_key"] for job in notifier.jobs()] == [incident_key(good["incident_id"])]
    malformed = [row for row in notifier.events() if row["kind"] == "malformed_incident"]
    assert len(malformed) == len(bad)  # recorded once each, not once per poll
    assert len({row["incident_key"] for row in malformed}) == len(bad)
    assert malformed[0]["incident_key"] == incident_key("bad:reason")
    text = json.dumps(notifier.events())
    assert not [incident_id for incident_id in ("bad:reason", "bad:at", "bad:generation")
                if incident_id in text]
