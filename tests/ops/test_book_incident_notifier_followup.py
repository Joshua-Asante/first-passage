"""Notifier follow-up: bounded rounds, ingestion, progress and no-rebuild open.

Card: docs/briefs/handoffs/2026-10-03-notifier-round-job-cap-card-DRAFT.md (FROZEN 2026-10-04),
tests RC1-RC10 for NF1-NF8. Synthetic incident rows are fed through an injected
``read_incidents``; every channel is a ``FakeChannel`` that never leaves the process.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import re
import sqlite3
import time

import pytest

from c1_rail.book_incident_notifier import (
    ChannelSpec,
    FakeChannel,
    IncidentNotifier,
    NotifierConfig,
    NotifierConfigError,
    NotifierStoreError,
    PublishResult,
)


NOW = datetime(2026, 10, 4, 12, 0, tzinfo=timezone.utc)
ACCEPTED = PublishResult("accepted")
REJECTED = PublishResult("rejected")
DIGEST = "d" * 64


class Clock:
    def __init__(self, at=NOW):
        self.at = at

    def __call__(self):
        return self.at

    def advance(self, seconds):
        self.at += timedelta(seconds=seconds)


class Rows:
    """Injected ``read_incidents``: synthetic committed rows, one per generation."""

    def __init__(self, *generations):
        self.rows, self.calls, self.fail = [], 0, False
        self.add(*generations)

    def add(self, *generations):
        for generation in generations:
            self.rows.append({"incident_id": "incident:%d" % len(self.rows), "reason": "operator",
                              "at": NOW.isoformat(), "generation": generation})

    def add_malformed(self):
        self.rows.append({"incident_id": "incident:%d" % len(self.rows), "reason": "",
                          "at": NOW.isoformat(), "generation": 7})

    def __call__(self):
        self.calls += 1
        if self.fail:
            raise RuntimeError("owner read failed")
        return [dict(row) for row in self.rows]


class Always(FakeChannel):
    """Answers every publish with the same result."""

    def __init__(self, name, result=REJECTED):
        super().__init__(name)
        self.result = result

    def publish(self, idempotency_key, payload):
        self.calls.append((idempotency_key, dict(payload)))
        return self.result


def _config(*names, k=None, m=None):
    raw = {"channels": [{"name": name, "kind": "fake", "secret_ref": "env:" + name.upper() + "_REF"}
                        for name in names or ("primary",)],
           "publish_timeout_s": 1.0, "retry_initial_s": 5.0, "retry_max_s": 30.0}
    if k is not None:
        raw["max_jobs_per_round"] = k
    if m is not None:
        raw["max_retained_incidents"] = m
    return NotifierConfig.from_mapping(raw)


def _notifier(path, rows, *channels, clock, k=None, m=None, rebuild=None):
    channels = channels or (FakeChannel("primary"),)
    extra = {} if rebuild is None else {"rebuild": rebuild}
    return IncidentNotifier(path, read_incidents=rows,
                            channels={channel.name: channel for channel in channels},
                            config=_config(*(channel.name for channel in channels), k=k, m=m),
                            clock=clock, **extra)


def _seed(path, rowid, at=None, *, rounds=0, lost=0, state="pending"):
    with closing(sqlite3.connect(path, isolation_level=None)) as db:
        db.execute("UPDATE jobs SET state=?, rounds=?, channels_lost=?, "
                   "next_attempt_at=COALESCE(?, next_attempt_at) WHERE rowid=?",
                   (state, rounds, lost, None if at is None else
                    (at if isinstance(at, str) else at.isoformat()), rowid))


def _rowids(notifier, channel, start=0):
    """Rowids of the jobs ``channel`` published since call ``start``, in call order."""
    keys = [job["incident_key"] for job in notifier.jobs()]
    return [keys.index(key) + 1 for key, _payload in channel.calls[start:]]


def _deferred(notifier):
    return [row["detail"] for row in notifier.events() if row["kind"] == "cap_deferred"]


def _trace(notifier):
    """Wrap ``_journal``: one list of executed statements per transaction entered."""
    entries, original = [], notifier._journal

    @contextmanager
    def traced():
        with original() as db:
            entries.append([])
            db.set_trace_callback(entries[-1].append)
            yield db

    notifier._journal = traced
    return entries


def _job_inserts(entries):
    return sum(bool(re.search(r"INSERT\b.*\bINTO jobs\b", statement, re.I))
               for entry in entries for statement in entry)


def _listing(directory):
    return {path.relative_to(directory).as_posix(): path.read_bytes() if path.is_file() else None
            for path in directory.rglob("*")}


def _tables(path):
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        return {name for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}


# -- RC1: NF1, the cap -----------------------------------------------------------------------

def test_cap_admits_exactly_k(tmp_path):
    rows, channel = Rows(1, 2, 3, 4, 5), FakeChannel("primary")
    notifier = _notifier(tmp_path / "a.sqlite", rows, channel, clock=Clock(), k=2)
    seen = []
    for _ in range(3):
        start = len(channel.calls)
        notifier.run_once()
        seen.append(_rowids(notifier, channel, start))
    assert seen == [[1, 2], [3, 4], [5]]

    # (b) a nominated job closed before its admission keeps its slot (J2): not replaced.
    rows, box = Rows(1, 2, 3), []

    class Closing(FakeChannel):
        def publish(self, idempotency_key, payload):
            result = super().publish(idempotency_key, payload)
            keys = [job["incident_key"] for job in box[0].jobs()]
            if idempotency_key == keys[0]:
                box[0].record_delivery(keys[1], "primary", DIGEST)
            return result

    channel = Closing("primary")
    notifier = _notifier(tmp_path / "b.sqlite", rows, channel, clock=Clock(), k=2)
    box.append(notifier)
    notifier.poll()
    notifier.publish_due()
    keys = [job["incident_key"] for job in notifier.jobs()]
    assert _rowids(notifier, channel) == [1]
    assert [row["kind"] for row in notifier.events(keys[1])] == ["detected", "delivered"]
    assert [row["kind"] for row in notifier.events(keys[2])] == ["detected"]
    assert _deferred(notifier) == [{"unaccepted": 1, "accepted": 0}]


# -- RC2: NF2 and NF5, the order -------------------------------------------------------------

def test_nf2_order_representatives_then_class_u_then_class_a(tmp_path):
    # (a) Sequences SB {1,2}, SA {10,11,12}, SC {20,21}, SD {30,31}, SE {40}.
    t = NOW + timedelta(hours=1)
    path, channel = tmp_path / "a.sqlite", FakeChannel("primary")
    notifier = _notifier(path, Rows(1, 2, 10, 11, 12, 20, 21, 30, 31, 40), channel,
                         clock=Clock(t), k=8)
    notifier.poll()
    second = timedelta(seconds=1)
    _seed(path, 1, t - 55 * second, rounds=1)                  # SB: class A
    _seed(path, 2, t - 12 * second, rounds=1, lost=1)
    _seed(path, 3, t + 8 * second, rounds=1, lost=1)           # SA: first job, not due
    _seed(path, 4, t - 22 * second, rounds=1, lost=1)
    _seed(path, 5, t - 32 * second)
    _seed(path, 6, t - 2 * second, rounds=1, lost=1)           # SC: first job, due
    _seed(path, 7, t - 12 * second)
    _seed(path, 8, rounds=1, state="delivered")                # SD: delivered
    _seed(path, 9, t - 12 * second)
    _seed(path, 10, t - 12 * second)                           # SE
    notifier.publish_due()
    assert _rowids(notifier, channel) == [10, 6, 5, 4, 2, 7, 9, 1]
    assert _deferred(notifier) == []

    # (b) Generation runs: {5, 6}, {8}, {malformed}, {1}.
    rows, channel = Rows(5, 6, 8), FakeChannel("primary")
    rows.add_malformed()
    rows.add(1)
    notifier = _notifier(tmp_path / "b.sqlite", rows, channel, clock=Clock(), k=5)
    notifier.run_once()
    assert [job["generation"] for job in notifier.jobs()] == [5, 6, 8, 0, 1]
    assert _rowids(notifier, channel) == [1, 3, 4, 5, 2]

    # (c) Due times compare as instants, never as text.
    path, channel = tmp_path / "c.sqlite", FakeChannel("primary")
    notifier = _notifier(path, Rows(1, 5), channel, clock=Clock(), k=2)
    notifier.poll()
    late = (NOW - timedelta(minutes=30)).isoformat()
    early = (NOW - timedelta(minutes=60)).astimezone(timezone(timedelta(hours=2))).isoformat()
    assert late < early and datetime.fromisoformat(early) < datetime.fromisoformat(late)
    _seed(path, 1, late)
    _seed(path, 2, early)
    notifier.publish_due()
    assert _rowids(notifier, channel) == [2, 1]

    # (d) A new sequence's first job runs ahead of another sequence's later-job representative.
    path, channel, clock = tmp_path / "d.sqlite", Always("primary"), Clock()
    notifier = _notifier(path, Rows(1, 2, 5), channel, clock=clock, k=1)
    notifier.poll()
    _seed(path, 1, NOW + timedelta(seconds=10), rounds=1, lost=1)
    _seed(path, 2, NOW - timedelta(seconds=10))
    _seed(path, 3, NOW)
    notifier.run_once()
    assert _rowids(notifier, channel) == [3]
    assert _deferred(notifier) == [{"unaccepted": 1, "accepted": 0}]
    assert (notifier.progress(), notifier.liveness()) == (0, None)


# -- RC3: NF2, rotation ----------------------------------------------------------------------

def _passes(notifier, channel, clock, count, step=60):
    seen = []
    for _ in range(count):
        clock.advance(step)
        start = len(channel.calls)
        notifier.run_once()
        seen.append(_rowids(notifier, channel, start))
    return seen


def test_rotation_within_a_class_under_persistent_failure(tmp_path):
    # (a) Class U, one sequence: its first job runs every pass, the rest rotate.
    clock, channel = Clock(), Always("primary")
    notifier = _notifier(tmp_path / "a.sqlite", Rows(1, 2, 3, 4, 5), channel, clock=clock, k=2)
    assert [set(ids) for ids in _passes(notifier, channel, clock, 5)] == [
        {1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 2}]

    # (b) Class A rotates once there is no class-U load.
    clock, channel = Clock(), Always("primary", ACCEPTED)
    notifier = _notifier(tmp_path / "b.sqlite", Rows(1, 2, 3), channel, clock=clock, k=1)
    assert _passes(notifier, channel, clock, 9)[3:] == [[1], [2], [3], [1], [2], [3]]

    # (c) S1 (1-7, generation 1 class A) and S2 (20-21).
    path, clock, channel = tmp_path / "c.sqlite", Clock(), Always("primary")
    notifier = _notifier(path, Rows(1, 2, 3, 4, 5, 6, 7, 20, 21), channel, clock=clock, k=2)
    notifier.poll()
    _seed(path, 1, NOW - timedelta(seconds=100), rounds=1)
    for rowid, back in zip(range(2, 8), (60, 50, 40, 30, 20, 10)):
        _seed(path, rowid, NOW - timedelta(seconds=back))
    _seed(path, 8, NOW - timedelta(seconds=5))
    _seed(path, 9, NOW - timedelta(seconds=5))
    seen = _passes(notifier, channel, clock, 12)
    assert all(ids[0] == 8 and len(ids) == 2 for ids in seen)
    assert [ids[1] for ids in seen] == [2, 3, 4, 5, 6, 7, 9, 2, 3, 4, 5, 6]
    assert 1 not in {rowid for ids in seen for rowid in ids}


# -- RC4: NF2 and NF3 after a rebuild --------------------------------------------------------

@pytest.mark.parametrize("generation, first_pass", [(121, 13), (200, 2)])
def test_post_rebuild_backlog_is_loud_and_representatives_first(tmp_path, generation, first_pass):
    path = tmp_path / "journal.sqlite"
    path.write_bytes(b"not a notifier journal\n" * 64)
    rows, clock, channel = Rows(*range(1, 121)), Clock(), FakeChannel("primary")
    notifier = _notifier(path, rows, channel, clock=clock, k=10, rebuild=True)
    assert [row["kind"] for row in notifier.events()] == ["journal_rebuilt"]
    notifier.run_once()
    assert _rowids(notifier, channel) == list(range(1, 11))
    assert _deferred(notifier) == [{"unaccepted": 110, "accepted": 0}]
    assert (notifier.progress(), notifier.liveness()) == (0, None)
    rows.add(generation)
    attempted_in = None
    for number in range(2, 14):
        clock.advance(1)
        start = len(channel.calls)
        notifier.run_once()
        calls = _rowids(notifier, channel, start)
        if 121 in calls:
            attempted_in = attempted_in or number
            if number == 2:
                assert calls[0] == 121
        if number < 13:
            assert (notifier.progress(), notifier.liveness()) == (0, None)
    assert attempted_in == first_pass
    assert [detail["unaccepted"] for detail in _deferred(notifier)] == [110] + [
        101 - 10 * index for index in range(11)]
    assert {detail["accepted"] for detail in _deferred(notifier)} == {0}
    assert (notifier.progress(), notifier.liveness()) == (1, clock.at)


# -- RC5: NF3, loud deferral -----------------------------------------------------------------

def test_cap_deferred_once_per_pass_with_counts_and_loudness(tmp_path):
    t = NOW - timedelta(seconds=10)
    # (a) 3 due class U and 2 due class A, k = 2.
    path = tmp_path / "a.sqlite"
    notifier = _notifier(path, Rows(1, 2, 3, 4, 5), clock=Clock(), k=2)
    notifier.poll()
    for rowid in (1, 2):
        _seed(path, rowid, t, rounds=1)
    for rowid in (3, 4, 5):
        _seed(path, rowid, t)
    notifier.run_once()
    assert _deferred(notifier) == [{"unaccepted": 1, "accepted": 2}]
    assert (notifier.progress(), notifier.liveness()) == (0, None)

    # (b) Only class A deferred: recorded, not loud.
    path, clock = tmp_path / "b.sqlite", Clock()
    notifier = _notifier(path, Rows(1, 2, 3), clock=clock, k=2)
    notifier.poll()
    for rowid in (1, 2, 3):
        _seed(path, rowid, t, rounds=1)
    notifier.run_once()
    assert _deferred(notifier) == [{"unaccepted": 0, "accepted": 1}]
    assert (notifier.progress(), notifier.liveness()) == (1, clock.at)

    # (c) At most k due: nothing deferred.
    notifier = _notifier(tmp_path / "c.sqlite", Rows(1, 2), clock=Clock(), k=2)
    notifier.run_once()
    assert _deferred(notifier) == [] and notifier.progress() == 1


# -- RC6: NF4 and NF5, ingestion ----------------------------------------------------------------

def test_known_keys_and_retained_bound(tmp_path):
    # (a) Known keys are never re-inserted, by this or a fresh instance.
    path, rows = tmp_path / "a.sqlite", Rows(1, 2, 3)
    notifier = _notifier(path, rows, clock=Clock())
    assert len(notifier.poll()) == 3
    entries = _trace(notifier)
    assert notifier.poll() == () and _job_inserts(entries) == 0
    rows.add(4)
    assert len(notifier.poll()) == 1 and _job_inserts(entries) == 1
    fresh = _notifier(path, rows, clock=Clock())
    entries = _trace(fresh)
    assert fresh.poll() == () and _job_inserts(entries) == 0

    # (b) A failed poll transaction never marks its key known.
    rows = Rows(1)
    notifier = _notifier(tmp_path / "b.sqlite", rows, clock=Clock())
    original = notifier._event

    def failing(db, key, kind, *args, **detail):
        if kind == "detected":
            raise sqlite3.OperationalError("injected")
        return original(db, key, kind, *args, **detail)

    notifier._event = failing
    with pytest.raises(NotifierStoreError):
        notifier.poll()
    del notifier._event
    assert notifier.jobs() == ()
    entries = _trace(notifier)
    assert len(notifier.poll()) == 1 and _job_inserts(entries) == 1

    # (c) One event per crossing above M.
    rows = Rows(1, 2, 3, 4, 5)
    every = list(rows.rows)
    notifier = _notifier(tmp_path / "c.sqlite", rows, clock=Clock(), m=3)
    for count in (2, 4, 5, 3, 4):
        rows.rows = every[:count]
        notifier.poll()
    bound = [row for row in notifier.events() if row["kind"] == "retained_incidents_over_bound"]
    assert [row["detail"] for row in bound] == [{"count": 4}, {"count": 4}]
    assert len(notifier.jobs()) == 5

    # (d) No LIMIT M on the pending fetch.
    channel = FakeChannel("primary")
    notifier = _notifier(tmp_path / "d.sqlite", Rows(1, 2, 3, 4, 5), channel, clock=Clock(),
                         k=5, m=3)
    notifier.run_once()
    assert _rowids(notifier, channel) == [1, 2, 3, 4, 5]

    # (e) A failed COMMIT leaves no job, no event and no crossing.
    path, rows = tmp_path / "e.sqlite", Rows(1, 2, 3, 4)
    notifier = _notifier(path, rows, clock=Clock(), m=3)
    reader = sqlite3.connect(path, isolation_level=None)
    try:
        reader.execute("BEGIN")
        reader.execute("SELECT count(*) FROM jobs").fetchall()
        with pytest.raises(NotifierStoreError):
            notifier.poll()
    finally:
        reader.close()
    assert notifier.jobs() == () and notifier.events() == ()
    assert len(notifier.poll()) == 4
    assert [row["detail"] for row in notifier.events()
            if row["kind"] == "retained_incidents_over_bound"] == [{"count": 4}]


# -- RC7: NF6, progress ----------------------------------------------------------------------

def test_progress_counts_clean_non_loud_loops_only(tmp_path):
    path, rows, clock = tmp_path / "journal.sqlite", Rows(1), Clock()
    notifier = _notifier(path, rows, clock=clock, k=1)
    assert notifier.progress() == 0
    notifier.run_once()
    assert (notifier.progress(), notifier.liveness()) == (1, NOW)
    clock.advance(-3600)
    notifier.run_once()
    assert (notifier.progress(), notifier.liveness()) == (2, NOW - timedelta(hours=1))
    rows.fail = True
    with pytest.raises(RuntimeError):
        notifier.run_once()
    assert notifier.progress() == 2
    rows.fail = False
    rows.add(50, 60)
    notifier.run_once()  # two new sequences, k = 1: loud
    assert _deferred(notifier) == [{"unaccepted": 1, "accepted": 0}]
    assert (notifier.progress(), notifier.liveness()) == (2, NOW - timedelta(hours=1))
    path.unlink()
    path.mkdir()
    with pytest.raises(NotifierStoreError):
        notifier.run_once()
    assert notifier.progress() == 2


# -- RC8: NF7, the no-rebuild open --------------------------------------------------------------

def _foreign_schema(store):
    with closing(sqlite3.connect(store)) as db:
        db.execute("CREATE TABLE jobs (incident_key TEXT PRIMARY KEY)")
        db.commit()


def _null_reason(store):
    """The journal's own schema, holding a row that fails ``PRAGMA integrity_check``."""
    _notifier(store, Rows(), clock=Clock())
    with closing(sqlite3.connect(store, isolation_level=None)) as db:
        db.execute("PRAGMA writable_schema=ON")
        db.execute("UPDATE sqlite_master SET sql=replace(sql, 'reason TEXT NOT NULL', "
                   "'reason TEXT') WHERE name='jobs'")
    with closing(sqlite3.connect(store, isolation_level=None)) as db:
        db.execute("INSERT INTO jobs VALUES ('k', NULL, 'at', 0, 'd', 'pending', 'at', 0, 0)")
        db.execute("PRAGMA writable_schema=ON")
        db.execute("UPDATE sqlite_master SET sql=replace(sql, 'reason TEXT', "
                   "'reason TEXT NOT NULL') WHERE name='jobs'")


def _unreadable(store):
    store.write_bytes(b"not a notifier journal\n" * 64)


def _table_less(store):
    with closing(sqlite3.connect(store)) as db:
        db.execute("PRAGMA user_version=1")
        db.commit()


def _empty(store):
    store.write_bytes(b"")


def test_rebuild_false_refuses_missing_faulty_and_uninitialized_journals(tmp_path, monkeypatch):
    # (a) Missing path in a missing directory.
    before = _listing(tmp_path)
    with pytest.raises(NotifierStoreError):
        _notifier(tmp_path / "missing" / "journal.sqlite", Rows(1), clock=Clock(), rebuild=False)
    assert _listing(tmp_path) == before

    # (b) The is_file race: mode=rw refuses the missing file.
    with monkeypatch.context() as patch:
        patch.setattr(type(tmp_path), "is_file", lambda self: True)
        with pytest.raises(NotifierStoreError):
            _notifier(tmp_path / "absent.sqlite", Rows(1), clock=Clock(), rebuild=False)
    assert _listing(tmp_path) == before

    # (c) and (e): faulty or uninitialized journals are refused and left exactly as found.
    for name, damage, fault in (("unreadable", _unreadable, True), ("integrity", _null_reason, True),
                                ("schema", _foreign_schema, True), ("empty", _empty, False),
                                ("table-less", _table_less, False)):
        directory = tmp_path / name
        directory.mkdir()
        store = directory / "journal.sqlite"
        damage(store)
        before = _listing(directory)
        with pytest.raises(NotifierStoreError):
            _notifier(store, Rows(1), clock=Clock(), rebuild=False)
        assert _listing(directory) == before, name
        if not fault:
            assert _tables(store) == set(), name
        rebuilt = _notifier(store, Rows(1), clock=Clock(), rebuild=True)
        moved = [path for path in directory.iterdir() if ".corrupt-" in path.name]
        kinds = [row["kind"] for row in rebuilt.events()]
        assert (bool(moved), kinds) == ((True, ["journal_rebuilt"]) if fault else (False, [])), name
        assert {"jobs", "events"} <= _tables(store)

    # (d) A valid journal opens and record_delivery closes a job.
    store = tmp_path / "valid.sqlite"
    first = _notifier(store, Rows(1), clock=Clock())
    (key,) = first.poll()
    second = _notifier(store, Rows(1), clock=Clock(), rebuild=False)
    second.record_delivery(key, "primary", DIGEST)
    assert [job["state"] for job in second.jobs()] == ["delivered"]

    # (f) A table-less file re-created under a running notifier.
    directory = tmp_path / "running"
    directory.mkdir()
    store = directory / "journal.sqlite"
    running = _notifier(store, Rows(1, 2, 3), clock=Clock())
    assert len(running.poll()) == 3
    store.rename(directory / "away.sqlite")
    with pytest.raises(NotifierStoreError):
        running.run_once()
    assert store.is_file() and _tables(store) == set()
    with pytest.raises(NotifierStoreError):
        _notifier(store, Rows(1, 2, 3), clock=Clock(), rebuild=False)
    assert _tables(store) == set()
    with pytest.raises(NotifierStoreError):
        running.run_once()
    assert running.progress() == 0


# -- RC9: NF8, the whole-invocation counts ------------------------------------------------------

def test_run_once_stays_within_nf8_counts(tmp_path):
    path, rows, k, channels = tmp_path / "journal.sqlite", Rows(*range(1, 51)), 2, (
        Always("primary"), Always("secondary"))
    notifier = _notifier(path, rows, *channels, clock=Clock(), k=k, m=50)
    notifier.poll()
    for rowid in range(1, 46):
        _seed(path, rowid, rounds=1, state="delivered")
    started = time.perf_counter()
    for row in rows():
        IncidentNotifier._parse(row)
    print("parse time for M = 50 rows: %.6f s" % (time.perf_counter() - started))
    rows.calls = 0
    entries = _trace(notifier)
    publishes, bounded = [], notifier._bounded_publish

    def counted(*args):
        publishes.append(args[:2])
        return bounded(*args)

    notifier._bounded_publish = counted
    notifier.run_once()
    c = len(channels)
    assert rows.calls == 1
    assert _job_inserts(entries) == 0
    assert len(entries) == 2 + 2 * k * c
    assert any("cap_deferred" in statement for statement in entries[1])
    assert sum("cap_deferred" in statement for entry in entries for statement in entry) == 1
    assert len(publishes) == k * c


# -- RC10: NF1 and NF4, the configuration -------------------------------------------------------

@pytest.mark.parametrize("field, default, other",
                         [("max_jobs_per_round", 10, 3), ("max_retained_incidents", 1000, 7)])
def test_new_fields_validated_and_round_trip(field, default, other):
    spec = ChannelSpec("primary", "fake", "env:PRIMARY_REF")
    raw = {"channels": [{"name": "primary", "kind": "fake", "secret_ref": "env:PRIMARY_REF"}]}
    for bad in (0, -1, True, False, 1.0, 2.5, "2", None):
        with pytest.raises(NotifierConfigError, match=field):
            NotifierConfig((spec,), **{field: bad})
        with pytest.raises(NotifierConfigError, match=field):
            NotifierConfig.from_mapping({**raw, field: bad})
    config = NotifierConfig((spec,))
    assert config.resolved()[field] == default
    for case in (config, NotifierConfig((spec,), max_jobs_per_round=3, max_retained_incidents=7)):
        again = NotifierConfig.from_mapping(case.resolved())
        assert again == case and again.digest == case.digest
    assert replace(config, **{field: other}).digest != config.digest
