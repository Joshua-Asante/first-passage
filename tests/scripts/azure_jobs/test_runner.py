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
