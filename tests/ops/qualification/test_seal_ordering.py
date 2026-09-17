"""Actual SQLite ordering; no mocked journal commits or execution claims."""
from concurrent.futures import ThreadPoolExecutor
from threading import Event
from contextlib import contextmanager
import pytest
import test_attempt as t
from c1_rail.qualification.attempt import AttemptStore, TransitionError, AttemptConflict

@pytest.fixture
def committed(tmp_path):
    store=t.open_store(tmp_path)
    t.reserve_and_start(store)
    manifest=t.canonical({'result':'PASS'})
    t.validated_commit(store,'TB_E1',manifest,outcome='PASS',now=t.NOW)
    return store,manifest

def seal(store,manifest):
    return store._commit_e1_seal(t.canonical({'sealed':'PASS'}),manifest_bytes=manifest,
        authentication_sha256='c'*64,now=t.NOW)

def reopen(store):
    return AttemptStore.open(store.path,campaign_id=store.campaign_id,
        contract_digest=store.contract_digest,trust_domain_sha256=store.trust_domain_sha256,
        boot_id='restarted',now=t.NOW)

def test_void_before_seal_survives_restart(committed):
    store,manifest=committed
    store.void('invalid',now=t.NOW)
    for restarted in (False,True):
        current=reopen(store) if restarted else store
        with pytest.raises(TransitionError,match='VOID'):seal(current,manifest)
        assert current.result('TB_E1')['manifest_bytes']==manifest
        assert not any(e['kind']=='E1_SEALED' for e in current.events())

def test_seal_retry_and_history_survive_restart_and_void(committed):
    store,manifest=committed
    first=seal(store,manifest)
    store=reopen(store)
    assert seal(store,manifest)==first
    assert len([e for e in store.events() if e['kind']=='E1_SEALED'])==1
    store.void('invalid',now=t.NOW)
    with pytest.raises(TransitionError,match='VOID'):seal(store,manifest)
    assert len([e for e in store.events() if e['kind']=='E1_SEALED'])==1

@pytest.mark.parametrize('first',['E1_SEALED','ATTEMPT_VOIDED'])
def test_concurrent_seal_void_order_is_atomic(committed,monkeypatch,first):
    store,manifest=committed
    locked=Event();release=Event();second_started=Event()
    connect=AttemptStore._connection
    @contextmanager
    def observed_connection(self):
        with connect(self) as db:
            def trace(statement):
                if statement=='BEGIN IMMEDIATE' and locked.is_set():second_started.set()
            db.set_trace_callback(trace)
            yield db
    monkeypatch.setattr(AttemptStore,'_connection',observed_connection)
    original=AttemptStore._append_event
    def hold(self,db,kind,body,instant):
        value=original(self,db,kind,body,instant)
        if kind==first:
            locked.set()
            assert release.wait(10)
        return value
    monkeypatch.setattr(AttemptStore,'_append_event',hold)
    def do_seal():return seal(store,manifest)
    def do_void():return store.void('invalid',now=t.NOW)
    leading,trailing=(do_seal,do_void) if first=='E1_SEALED' else (do_void,do_seal)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a=pool.submit(leading)
        assert locked.wait(10)
        b=pool.submit(trailing)
        assert second_started.wait(10)
        assert not b.done()
        release.set();a.result(timeout=10)
        if first=='ATTEMPT_VOIDED':
            with pytest.raises(TransitionError,match='VOID'):b.result(timeout=10)
        else:b.result(timeout=10)
    kinds=[e['kind'] for e in reopen(store).events() if e['kind'] in ('E1_SEALED','ATTEMPT_VOIDED')]
    assert kinds==(['E1_SEALED','ATTEMPT_VOIDED'] if first=='E1_SEALED' else ['ATTEMPT_VOIDED'])


def test_distinct_verified_seals_are_retained_while_valid(committed):
    store,manifest=committed
    seal(store,manifest)
    newer=t.canonical({'sealed':'later externally verified seal'})
    assert store._commit_e1_seal(newer,manifest_bytes=manifest,
        authentication_sha256='c'*64,now=t.NOW)==newer
    assert len([e for e in store.events() if e['kind']=='E1_SEALED'])==2


@pytest.mark.parametrize('field',['manifest','authentication'])
def test_seal_transition_rechecks_committed_identity(committed,field):
    store,manifest=committed
    with pytest.raises(AttemptConflict):
        store._commit_e1_seal(t.canonical({'sealed':'PASS'}),
            manifest_bytes=t.canonical({'other':'result'}) if field=='manifest' else manifest,
            authentication_sha256='d'*64 if field=='authentication' else 'c'*64,now=t.NOW)
    assert not any(e['kind']=='E1_SEALED' for e in store.events())


def test_failed_seal_transaction_leaves_no_seal_after_restart(committed):
    import sqlite3
    store,manifest=committed
    with sqlite3.connect(store.path) as db:
        db.execute("CREATE TRIGGER fail_seal BEFORE INSERT ON events WHEN NEW.kind='E1_SEALED' "
                   "BEGIN SELECT RAISE(ABORT,'injected durable write failure'); END")
    with pytest.raises(sqlite3.IntegrityError):seal(store,manifest)
    store=reopen(store)
    assert not any(e['kind']=='E1_SEALED' for e in store.events())
    assert store.result('TB_E1')['manifest_bytes']==manifest
