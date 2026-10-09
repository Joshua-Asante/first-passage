import json
import os
from pathlib import Path
import sys
import time
import pytest
from scripts.azure_jobs import guest


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job Object')
def test_guest_tree_measures_descendants_and_retains_output(tmp_path):
    script = tmp_path / 'work.py'
    script.write_text("import subprocess,sys; subprocess.run([sys.executable,'-c','sum(i*i for i in range(1000000)); print(42)'])")
    result = guest.run_tree([sys.executable, str(script)], tmp_path, tmp_path, deadline=time.time()+30)
    assert result['exit_code'] == 0
    assert result['cpu_seconds'] > 0
    assert result['wall_seconds'] > 0
    assert '42' in (tmp_path / 'stdout.log').read_text()


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job Object')
def test_cancel_interrupts_tree_and_keeps_partial_stdout(tmp_path):
    script = tmp_path / 'work.py'
    script.write_text("import time; print('partial',flush=True); time.sleep(60)")
    import threading
    trigger = threading.Timer(1, lambda: (tmp_path / 'cancel').write_text('cancel'))
    trigger.start()
    result = guest.run_tree([sys.executable, str(script)], tmp_path, tmp_path, deadline=time.time()+30)
    trigger.join()
    assert result['status'] == 'interrupted'
    assert result['exit_code'] != 0
    assert 'partial' in (tmp_path / 'stdout.log').read_text()


@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job Object')
def test_timeout_kills_before_long_sleep_finishes(tmp_path):
    result = guest.run_tree([sys.executable, '-c', 'import time; time.sleep(60)'], tmp_path, tmp_path, deadline=time.time()+1)
    assert result['status'] == 'interrupted'
    assert result['reason'] == 'timeout'
    assert result['wall_seconds'] < 10

@pytest.mark.skipif(os.name != 'nt', reason='real Windows Job Object')
def test_named_job_can_be_stopped_by_independent_watchdog(tmp_path):
    import threading
    from scripts.azure_jobs.watchdog import terminate_tree
    trigger = threading.Timer(1, lambda: terminate_tree('test-independent-stop'))
    trigger.start()
    result = guest.run_tree([sys.executable, '-c', 'import time; time.sleep(60)'], tmp_path, tmp_path, deadline=time.time()+30, job_name='test-independent-stop')
    trigger.join()
    assert result['exit_code'] != 0
    assert result['wall_seconds'] < 10


def test_cancel_before_spawn_does_not_execute(tmp_path):
    (tmp_path / 'cancel').write_text('cancel')
    result = guest.run_tree([sys.executable, '-c', "open('SHOULD_NOT_EXIST','w').write('bad')"], tmp_path, tmp_path, deadline=time.time()+30)
    assert result['status'] == 'interrupted'
    assert not (tmp_path / 'SHOULD_NOT_EXIST').exists()


def test_reentry_never_reexecutes_job(tmp_path, monkeypatch):
    spec=dict(job_id='once',commit='a'*40,command=['fake.py'],environment='research',max_wall_seconds=60,expected_outputs=['out'],authority='public test',private_inputs=[])
    job=tmp_path/'jobs/once'; job.mkdir(parents=True)
    (job/'record.json').write_text('{"status":"interrupted"}')
    monkeypatch.setattr(guest,'checkout',lambda *a: (_ for _ in ()).throw(AssertionError('replayed')))
    guest.execute({'guest_root':str(tmp_path)},spec)
    assert json.loads((job/'record.json').read_text())['status']=='interrupted'


def test_finalization_keeps_heartbeat_and_publishes_terminal_state(tmp_path, monkeypatch):
    spec=dict(job_id='heartbeat',commit='a'*40,command=['fake.py'],environment='research',max_wall_seconds=60,expected_outputs=['out'],authority='public test',private_inputs=[])
    def checkout(config,commit,repo):
        repo.mkdir(parents=True); (repo/'out').write_text('42'); (repo/'fake.py').write_text('pass')
    monkeypatch.setattr(guest,'checkout',checkout)
    monkeypatch.setattr(guest,'environment',lambda *a: (Path(sys.executable),tmp_path/'env','lock'))
    monkeypatch.setattr(guest,'bounded_snapshot',lambda *a,**k: {'commit':'a'*40,'status':''})
    monkeypatch.setattr(guest,'run_tree',lambda *a,**k: dict(status='completed',exit_code=0,cpu_seconds=1,wall_seconds=1,finished_at=time.time()))
    for key in ('PATH','VIRTUAL_ENV','PYTHONPATH','PYTHONHOME','FP_VERIFICATION_ID'):
        if key in os.environ:
            monkeypatch.setenv(key,os.environ[key])
        else:
            monkeypatch.delenv(key,raising=False)
    original_bundle=guest.bundle
    observed=[]
    def slow_bundle(job,repo,outputs,**kwargs):
        old=json.loads((job/'heartbeat.json').read_text())['time']
        time.sleep(2.5)
        assert json.loads((job/'heartbeat.json').read_text())['time'] > old
        return original_bundle(job,repo,outputs,**kwargs)
    monkeypatch.setattr(guest,'bundle',slow_bundle)
    monkeypatch.setattr(guest,'upload',lambda cfg,job,id: observed.append(json.loads((job/'state.json').read_text())['status']))
    guest.execute({'guest_root':str(tmp_path),'deadline':time.time()+60,'git':'git.exe'},spec)
    assert observed == ['completed']


@pytest.mark.skipif(os.name != 'nt', reason='Windows names')
def test_existing_named_job_is_not_adopted():
    from scripts.agent_handoff import WindowsJob
    first=WindowsJob.create(name='Local\\FP-Offline-collision-test')
    try:
        with pytest.raises(OSError,match='already exists'):
            WindowsJob.create(name='Local\\FP-Offline-collision-test')
    finally:
        first.close()


def test_expired_deadline_never_spawns(tmp_path, monkeypatch):
    monkeypatch.setattr(guest.WindowsJob, 'create', lambda **kw: pytest.fail('spawn after cutoff'))
    result = guest.run_tree(['unused'], tmp_path, tmp_path, deadline=time.time()-1)
    assert result['status'] == 'interrupted'
    assert result['reason'] == 'timeout'


def test_recovery_defers_to_live_finalizer(tmp_path, monkeypatch):
    from scripts.azure_jobs import watchdog
    from scripts.azure_jobs.control import locked, atomic
    job = tmp_path/'jobs/job'; job.mkdir(parents=True)
    atomic(job/'record.json', {'status':'not_started'})
    monkeypatch.setattr(watchdog, 'terminate_tree', lambda name: True)
    monkeypatch.setattr(watchdog.time, 'sleep', lambda seconds: None)
    monkeypatch.setattr(watchdog, 'upload', lambda *a: pytest.fail('concurrent publisher'))
    with locked(tmp_path/'guest.lock'):
        assert watchdog.recover({'guest_root':str(tmp_path)}, {'job_id':'job'}, 'cancelled') is False
        assert json.loads((job/'record.json').read_text())['status'] == 'not_started'


def test_upload_publishes_immutable_archive_before_descriptor(tmp_path, monkeypatch):
    from scripts.azure_jobs.control import atomic
    (tmp_path/'results.zip').write_bytes(b'zip')
    atomic(tmp_path/'archive.json', {'sha256':guest.sha256(tmp_path/'results.zip')})
    atomic(tmp_path/'state.json', {'status':'completed'})
    names=[]
    monkeypatch.setattr(guest,'checked',lambda args,**kw: names.append(args[args.index('--name')+1]))
    guest.upload({'az':'az','storage_account':'test','container':'test'},tmp_path,'job')
    assert names[0] == 'job/'+guest.sha256(tmp_path/'results.zip')+'.zip'
    assert names[-1] == 'job/archive.json'


def test_republish_keeps_terminal_record_and_never_executes(tmp_path, monkeypatch):
    from scripts.azure_jobs.control import atomic
    spec=dict(job_id='original',commit='a'*40,command=['fake.py'],environment='research',max_wall_seconds=60,expected_outputs=['out'],authority='public test',private_inputs=[])
    job=tmp_path/'jobs/original'; job.mkdir(parents=True)
    repo=tmp_path/'repos/original'; repo.mkdir(parents=True); (repo/'out').write_text('result')
    record={'status':'completed','exit_code':0,'source_stable':True}
    atomic(job/'record.json',record)
    for forbidden in ('checkout','environment','run_tree'):
        monkeypatch.setattr(guest,forbidden,lambda *a,**kw: pytest.fail('replayed job'))
    observed=[]
    monkeypatch.setattr(guest,'upload',lambda *a: observed.append(a[2]))
    guest.republish({'guest_root':str(tmp_path),'session_id':'recovery'},spec)
    assert json.loads((job/'record.json').read_text()) == record
    assert json.loads((tmp_path/'idle.json').read_text())['job_id']=='recovery'
    assert observed==['original']


def test_stale_heartbeat_does_not_kill_a_live_lock_owner(tmp_path,monkeypatch):
    from scripts.azure_jobs import watchdog
    from scripts.azure_jobs.control import locked
    monkeypatch.setattr(watchdog,'terminate_tree',lambda *a: pytest.fail('killed live supervisor'))
    with locked(tmp_path/'guest.lock'):
        assert watchdog.recover({'guest_root':str(tmp_path)},{'job_id':'job'},'guest supervisor lost') is False
    assert not (tmp_path/'jobs/job/cancel').exists()


def test_reentry_marks_idle_without_replaying(tmp_path,monkeypatch):
    from scripts.azure_jobs.control import atomic
    spec=dict(job_id='once',commit='a'*40,command=['fake.py'],environment='research',max_wall_seconds=60,expected_outputs=['out'],authority='public test',private_inputs=[])
    atomic(tmp_path/'jobs/once/record.json',{'status':'completed'})
    monkeypatch.setattr(guest,'checkout',lambda *a: pytest.fail('replayed'))
    guest.execute({'guest_root':str(tmp_path)},spec)
    assert json.loads((tmp_path/'idle.json').read_text())['job_id']=='once'


@pytest.mark.skipif(os.name != 'nt', reason='Windows process ownership')
def test_bounded_source_snapshot_reads_clean_git_revision(tmp_path):
    import subprocess
    repo=tmp_path/'repo'; repo.mkdir()
    subprocess.run(['git','init',str(repo)],check=True,capture_output=True)
    subprocess.run(['git','-C',str(repo),'-c','user.name=Runner test','-c','user.email=runner@example.invalid','commit','--allow-empty','-m','fixture'],check=True,capture_output=True)
    result=guest.bounded_snapshot(repo,tmp_path/'snapshot',time.time()+30)
    assert len(result['commit'])==40
    assert result['status']==''
    with pytest.raises(TimeoutError):
        guest.bounded_snapshot(repo,tmp_path/'expired',time.time()-1)


def test_heartbeat_recovers_after_a_failed_tick(tmp_path, monkeypatch):
    class Stop:
        stopped = False
        waits = []
        def is_set(self): return self.stopped
        def wait(self, seconds): self.waits.append(seconds)
    stop = Stop()
    calls = []
    original = guest.atomic
    def flaky(path, value):
        calls.append(path)
        if len(calls) == 1:
            raise PermissionError("reader outlasted retry window")
        original(path, value)
        stop.stopped = True
    monkeypatch.setattr(guest, "atomic", flaky)
    guest.keep_heartbeat(tmp_path, stop)
    assert len(calls) == 2
    assert stop.waits == [2, 2]
    assert json.loads((tmp_path / "heartbeat.json").read_text())["time"] > 0
