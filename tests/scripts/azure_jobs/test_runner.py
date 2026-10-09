import json
from pathlib import Path
import pytest
from scripts.azure_jobs import runner, watchdog
from scripts.azure_jobs.control import Ledger


def test_expired_guest_lease_always_requests_deallocation():
    assert watchdog.stop_reason({'deadline':100, 'job_id':'a'}, None, 101) == 'deadline'


def test_old_job_idle_marker_does_not_stop_current_job():
    assert watchdog.stop_reason({'deadline':200, 'job_id':'b'}, {'job_id':'a'}, 100) is None


def test_matching_idle_marker_requests_shutdown():
    assert watchdog.stop_reason({'deadline':200, 'job_id':'b'}, {'job_id':'b'}, 100) == 'idle'


def test_missing_lease_fails_closed():
    assert watchdog.stop_reason(None, None, 100) == 'missing lease'


def test_results_refuse_archive_traversal(tmp_path):
    import zipfile
    path = tmp_path / 'bad.zip'
    with zipfile.ZipFile(path, 'w') as out:
        out.writestr('../escape', 'bad')
    with pytest.raises(ValueError):
        runner.unpack(path, tmp_path / 'out')
    assert not (tmp_path / 'escape').exists()


def test_results_refuse_unmanifested_extra_file(tmp_path):
    import zipfile
    path = tmp_path / 'bad.zip'
    with zipfile.ZipFile(path, 'w') as out:
        out.writestr('manifest.json', '{}')
        out.writestr('extra', 'bad')
    with pytest.raises(ValueError, match='inventory'):
        runner.unpack(path, tmp_path / 'out')

@pytest.mark.parametrize('heartbeat,now,expected', [(100,150,None),(100,701,'controller lost'),(None,701,'controller lost'),(399,501,'deadline')])
def test_reaper_bounds_controller_failure(heartbeat,now,expected):
    assert runner.reap_reason({'start':100,'deadline':500 if expected == 'deadline' else 2000},heartbeat,now) == expected


def test_cpu_report_accounts_retrieved_jobs_and_marks_unknown(tmp_path):
    from datetime import datetime, timezone
    now = datetime(2026,10,9,tzinfo=timezone.utc).timestamp()
    result = tmp_path / 'results' / 'a' / 'files' / 'runner'
    result.mkdir(parents=True)
    (result / 'record.json').write_text(json.dumps(dict(cpu_seconds=7200,finished_at=now,wall_seconds=400)))
    report = runner.cpu_report({'state_dir':str(tmp_path)}, now=now)
    assert report['week_process_cpu_hours'] == 2
    assert report['month_process_cpu_hours'] == 2
    assert report['monthly_planning_allowance_cpu_hours'] == 5000



def test_status_reads_durable_guest_state_while_running(tmp_path, monkeypatch):
    calls=[]
    class Fake:
        def __init__(self,cfg): pass
        def power(self): return 'VM running'
        def script(self,script):
            calls.append(script)
            return json.dumps({'status':'running','phase':'executing'})
    monkeypatch.setattr(runner,'Azure',Fake)
    monkeypatch.setattr(runner,'blob',lambda *a: (_ for _ in ()).throw(RuntimeError('not published')))
    Ledger(tmp_path/'ledger.json',initial_seconds=0)
    result=runner.status({'state_dir':str(tmp_path),'guest_root':'C:/runner'},'job')
    assert result['status']=='running'
    assert 'state.json' in calls[0]

def test_status_does_not_consume_submission_identity(tmp_path, monkeypatch):
    class Fake:
        def __init__(self,cfg): pass
        def power(self): return "VM deallocated"
    monkeypatch.setattr(runner,"Azure",Fake)
    monkeypatch.setattr(runner,"blob",lambda *args: (_ for _ in ()).throw(RuntimeError()))
    Ledger(tmp_path/"ledger.json",initial_seconds=0)
    runner.status({"state_dir":str(tmp_path)},"new-job")
    assert not (tmp_path/"jobs/new-job").exists()


def test_current_cloud_lease_replaces_previous_disk_job():
    lease = watchdog.metadata_lease({"tagsList":[
        {"name":"FPOfflineJob","value":"new-job"},
        {"name":"FPOfflineDeadline","value":"500"}]})
    assert watchdog.stop_reason(lease,{"job_id":"old-job"},100) is None
    assert lease["job_id"] == "new-job"


def test_reaper_allows_two_maximum_cli_reads_and_poll_delay():
    assert runner.reap_reason({"start":100,"deadline":2000},100,475) is None


def test_reconcile_refuses_to_stop_healthy_job(tmp_path, monkeypatch):
    ledger=Ledger(tmp_path/'ledger.json',initial_seconds=0)
    import time
    ledger.reserve('healthy',100,time.time())
    class Fake:
        def __init__(self,cfg): pass
        def power(self): return 'VM running'
        def deallocate(self): pytest.fail('reconcile killed healthy work')
    monkeypatch.setattr(runner,'Azure',Fake)
    with pytest.raises(ValueError,match='cancel'):
        runner.reconcile({'state_dir':str(tmp_path)})
    assert ledger.read()['active']['job_id']=='healthy'


def test_recovery_admission_reserves_fresh_session_without_changing_job(tmp_path, monkeypatch):
    import time
    from scripts.azure_jobs.control import atomic, OVERHEAD_SECONDS
    spec=dict(job_id='original',commit='a'*40,command=['fake.py'],environment='research',max_wall_seconds=600,expected_outputs=['out'],authority='public test',private_inputs=[])
    original=tmp_path/'jobs/original'
    atomic(original/'session.json', {'job_id':'original'})
    atomic(original/'spec.json',spec)
    ledger=Ledger(tmp_path/'ledger.json',initial_seconds=0)
    class Fake:
        def __init__(self,cfg): pass
        def power(self): return 'VM deallocated'
    monkeypatch.setattr(runner,'Azure',Fake)
    monkeypatch.setattr(runner,'clean_source',lambda: 'b'*40)
    launched=[]
    monkeypatch.setattr(runner,'launch_guardian',lambda config,path: launched.append(runner.read(path)))
    result=runner.run({'state_dir':str(tmp_path)},tmp_path/'config.json',spec,mode='republish')
    assert result['session_id'] != spec['job_id']
    assert result['reserved_seconds'] == OVERHEAD_SECONDS
    assert launched[0]['mode'] == 'republish'
    assert launched[0]['spec'] == spec
    assert ledger.read()['active']['source_job_id']=='original'
    assert runner.read(original/'session.json') == {'job_id':'original'}


def test_retrieval_remains_consistent_when_descriptor_changes_mid_download(tmp_path, monkeypatch):
    import shutil
    from scripts.azure_jobs import guest
    from scripts.azure_jobs.control import atomic
    cloud=tmp_path/'cloud'; cloud.mkdir()
    job=tmp_path/'guest'; job.mkdir()
    repo=tmp_path/'repo'; repo.mkdir(); (repo/'out').write_text('first')
    record={'status':'completed','exit_code':0,'verification_exit_code':0,'source_stable':True,'capture_complete':True,'report_errors':[]}
    atomic(job/'record.json',record)
    atomic(job/'state.json',record)
    def upload(args,**kwargs):
        name=args[args.index('--name')+1]
        dest=cloud/name; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(args[args.index('--file')+1],dest)
    monkeypatch.setattr(guest,'checked',upload)
    cfg={'az':'az','storage_account':'test','container':'test','state_dir':str(tmp_path/'host')}
    def publish():
        atomic(job/'archive.json',guest.bundle(job,repo,['out'],partial=False))
        guest.upload(cfg,job,'job')
    publish()
    def download(config,action,name,destination):
        shutil.copyfile(cloud/name,destination)
        if name.endswith('/archive.json'):
            (repo/'out').write_text('second')
            publish()
    monkeypatch.setattr(runner,'blob',download)
    Ledger(Path(cfg['state_dir'])/'ledger.json',initial_seconds=0)
    result=runner.results(cfg,'job')
    assert result['verified']
    assert (Path(result['directory'])/'files/out').read_text()=='first'


def test_command_retirement_retains_last_read_before_cleanup(tmp_path):
    events=[]
    class Fake:
        def command(self,name):
            events.append('read')
            return {'instanceView':{'executionState':'Succeeded','exitCode':0}}
        def cleanup(self,name):
            assert runner.read(tmp_path/'terminal-observation.json')['instanceView']['executionState']=='Succeeded'
            events.append('cleanup')
    runner.retain_and_cleanup(Fake(),tmp_path,'job')
    assert events==['read','cleanup']


def test_cancel_recovery_stops_session_without_changing_original_result(tmp_path,monkeypatch):
    from scripts.azure_jobs.control import atomic
    import time
    ledger=Ledger(tmp_path/'ledger.json',initial_seconds=0)
    ledger.reserve('recover-session',100,time.time(),source_job_id='original')
    atomic(tmp_path/'jobs/recover-session/session.json',{'mode':'republish'})
    calls=[]
    monkeypatch.setattr(runner,'Azure',lambda cfg: object())
    monkeypatch.setattr(runner,'retire',lambda *a,**kw: calls.append(kw['expected_job']))
    result=runner.cancel({'state_dir':str(tmp_path)},'original')
    assert calls==['recover-session']
    assert result['status']=='interrupted'
    assert runner.read(tmp_path/'jobs/recover-session/stop-request.json')['reason']=='cancelled'


def test_retirement_still_runs_if_diagnostic_storage_fails(tmp_path,monkeypatch):
    import time
    from scripts.azure_jobs.control import atomic
    ledger=Ledger(tmp_path/'ledger.json',initial_seconds=0)
    session=ledger.reserve('job',100,time.time())
    path=tmp_path/'jobs/job/session.json'; atomic(path,session)
    atomic(path.parent/'submitted.json',{'command':'fp-job-job'})
    monkeypatch.setattr(runner,'Azure',lambda cfg: object())
    monkeypatch.setattr(runner,'launch_reaper',lambda *a: (_ for _ in ()).throw(RuntimeError('setup failed')))
    monkeypatch.setattr(runner,'retain_and_cleanup',lambda *a: (_ for _ in ()).throw(OSError('disk full')))
    monkeypatch.setattr(runner,'retire',lambda *a,**kw: ledger.finish(time.time()))
    runner.guardian({'state_dir':str(tmp_path)},path,tmp_path/'config.json')
    assert ledger.read()['active'] is None


@pytest.mark.parametrize('submitted,force',[(False,False),(True,True)])
def test_cancel_can_stop_before_guest_or_force_stop(tmp_path,monkeypatch,submitted,force):
    import time
    from scripts.azure_jobs.control import atomic
    ledger=Ledger(tmp_path/'ledger.json',initial_seconds=0)
    ledger.reserve('job',100,time.time())
    directory=tmp_path/'jobs/job'
    atomic(directory/'session.json',{'mode':'execute'})
    if submitted: atomic(directory/'submitted.json',{'command':'fp-job-job'})
    monkeypatch.setattr(runner,'Azure',lambda cfg: object())
    stopped=[]
    monkeypatch.setattr(runner,'retire',lambda *a,**kw: stopped.append(kw['expected_job']))
    result=runner.cancel({'state_dir':str(tmp_path)},'job',force=force)
    assert result['status']=='interrupted'
    assert stopped==['job']
    assert runner.read(directory/'stop-request.json')['reason']=='cancelled'


def test_guest_bootstrap_deadline_is_separate_from_workload_deadline():
    lease={'job_id':'job','deadline':2000,'bootstrap_deadline':200}
    assert watchdog.job_stop_reason(lease,{}, {},False,201)=='bootstrap deadline'
    assert watchdog.job_stop_reason(lease,{'status':'running','phase':'executing'}, {'time':201},False,201) is None


def test_normal_cancel_preserves_publication_instead_of_retiring(tmp_path,monkeypatch):
    import time
    from scripts.azure_jobs.control import atomic
    ledger=Ledger(tmp_path/'ledger.json',initial_seconds=0)
    ledger.reserve('job',100,time.time())
    directory=tmp_path/'jobs/job'
    atomic(directory/'session.json',{'mode':'execute'})
    atomic(directory/'submitted.json',{'command':'fp-job-job'})
    scripts=[]
    class Fake:
        def __init__(self,cfg): pass
        def script(self,text): scripts.append(text)
    monkeypatch.setattr(runner,'Azure',Fake)
    monkeypatch.setattr(runner,'retire',lambda *a,**kw: pytest.fail('normal cancel retired before publication'))
    result=runner.cancel({'state_dir':str(tmp_path),'guest_root':'C:/runner'},'job')
    assert result['status']=='cancellation_requested'
    assert '/jobs/job/cancel' in scripts[0]
    assert not (directory/'stop-request.json').exists()


def test_watchdog_idle_deallocates_during_boot_grace(tmp_path,monkeypatch):
    from scripts.azure_jobs.control import atomic
    class Stopped(BaseException): pass
    class Fake:
        def __init__(self,cfg): pass
        def deallocate(self): raise Stopped()
    atomic(tmp_path/'config.json',{'guest_root':str(tmp_path)})
    atomic(tmp_path/'idle.json',{'job_id':'job'})
    monkeypatch.setattr(watchdog,'Azure',Fake)
    monkeypatch.setattr(watchdog,'cloud_lease',lambda: {'job_id':'job','deadline':5000,'bootstrap_deadline':1000})
    monkeypatch.setattr(watchdog.time,'time',lambda:100)
    monkeypatch.setattr(watchdog.time,'monotonic',lambda:100)
    monkeypatch.setattr(watchdog.time,'sleep',lambda seconds: pytest.fail('idle VM waited through boot grace'))
    with pytest.raises(Stopped): watchdog.main(tmp_path/'config.json')


@pytest.mark.parametrize('state',[None,{'status':'running','phase':'preparing','started_at':100}])
def test_watchdog_bootstrap_cutoff_deallocates_even_when_recovery_lock_busy(tmp_path,monkeypatch,state):
    from scripts.azure_jobs.control import atomic
    class Stopped(BaseException): pass
    class Fake:
        def __init__(self,cfg): pass
        def deallocate(self): raise Stopped()
    atomic(tmp_path/'config.json',{'guest_root':str(tmp_path)})
    if state: atomic(tmp_path/'jobs/job/state.json',state)
    monkeypatch.setattr(watchdog,'Azure',Fake)
    monkeypatch.setattr(watchdog,'cloud_lease',lambda: {'job_id':'job','deadline':5000,'bootstrap_deadline':200})
    monkeypatch.setattr(watchdog,'recover',lambda *a: False)
    monkeypatch.setattr(watchdog.time,'time',lambda:201)
    monkeypatch.setattr(watchdog.time,'monotonic',lambda:100)
    monkeypatch.setattr(watchdog.time,'sleep',lambda seconds: pytest.fail('bootstrap cutoff failed to deallocate'))
    with pytest.raises(Stopped): watchdog.main(tmp_path/'config.json')


def test_reaper_deallocates_even_when_stop_marker_cannot_be_written(tmp_path, monkeypatch):
    import time
    ledger = Ledger(tmp_path / "ledger.json", initial_seconds=0)
    session = ledger.reserve("job", 100, time.time())
    path = tmp_path / "jobs/job/session.json"
    original = runner.atomic
    original(path, session)
    def denied_marker(destination, value):
        if destination.name == "stop-request.json":
            raise PermissionError("state storage unavailable")
        original(destination, value)
    monkeypatch.setattr(runner, "atomic", denied_marker)
    monkeypatch.setattr(runner, "Azure", lambda cfg: object())
    retired = []
    def retire(azure, actual_ledger, **kwargs):
        retired.append(kwargs["expected_job"])
        actual_ledger.finish(time.time())
    monkeypatch.setattr(runner, "retire", retire)
    runner.reaper({"state_dir": str(tmp_path)}, path)
    assert retired == ["job"]
    assert ledger.read()["active"] is None
