"""Invariant-derived sequence oracles for the narrowed v1 coordinator contract."""
import json
import time
from pathlib import Path
import pytest
from scripts.azure_jobs import control, runner, contract


def spec():
    return dict(job_id='job', commit='a'*40, environment='operations',
                command=['scripts/fp.py', 'test'], max_wall_seconds=60,
                authority='public synthetic verification', private_inputs=[],
                expected_outputs=['.cache/fp-verification'])


def setup(tmp_path, monkeypatch, *, active=True):
    cfg = {'state_dir': str(tmp_path), 'guest_root': 'C:/fp'}
    ledger = control.Ledger(tmp_path/'ledger.json', initial_seconds=0)
    if active:
        ledger.reserve('job', 3600, time.time())
        control.atomic(tmp_path/'jobs/job/session.json', {'job_id':'job', 'mode':'execute'})
    events = []
    class Azure:
        def __init__(self, config): pass
        def power(self):
            events.append('power')
            return 'VM deallocated'
        def deallocate(self): events.append('deallocate')
        def script(self, text): raise RuntimeError('guest unavailable')
    monkeypatch.setattr(runner, 'Azure', Azure)
    monkeypatch.setattr(runner, 'clean_source', lambda: 'b'*40)
    return cfg, ledger, events, Azure


def test_s1_research_rejected_before_admission(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch, active=False)
    value = spec(); value['environment'] = 'research'
    value['command'] = ['fake.py']
    monkeypatch.setattr(runner, 'launch_guardian', lambda *a: events.append('launch'))
    with pytest.raises(ValueError, match='operations'):
        runner.run(cfg, tmp_path/'config.json', value)
    assert ledger.read()['active'] is None
    assert 'launch' not in events


def test_s1_disk_recovery_not_admitted(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch, active=False)
    control.atomic(tmp_path/'jobs/job/session.json', {'job_id':'job'})
    monkeypatch.setattr(runner, 'launch_guardian', lambda *a: events.append('launch'))
    with pytest.raises(ValueError, match='deferred|unsupported|mode'):
        runner.run(cfg, tmp_path/'config.json', spec(), mode='republish')
    assert ledger.read()['active'] is None


def test_s2_cancel_marker_failure_still_deallocates(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch)
    def fail(*args): raise OSError('disk failed')
    monkeypatch.setattr(runner, 'atomic', fail)
    try:
        runner.cancel(cfg, 'job')
    except (OSError, RuntimeError):
        pass
    assert 'deallocate' in events
    assert ledger.read()['active'] is None


def test_s2_cancel_guest_transport_failure_still_deallocates(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch)
    control.atomic(tmp_path/'jobs/job/submitted.json', {'command':'fp-job-job'})
    try:
        runner.cancel(cfg, 'job')
    except RuntimeError:
        pass
    assert 'deallocate' in events
    assert ledger.read()['active'] is None


def test_s4_cleanup_debt_refuses_admission(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch, active=False)
    control.atomic(tmp_path/'pending-command-cleanup/fp-job-old.json', {'command':'fp-job-old'})
    monkeypatch.setattr(runner, 'launch_guardian', lambda *a: events.append('launch'))
    with pytest.raises(ValueError, match='cleanup'):
        runner.run(cfg, tmp_path/'config.json', spec())
    assert ledger.read()['active'] is None
    assert 'launch' not in events


def test_s5_failed_deallocate_call_still_observes_power(tmp_path, monkeypatch):
    cfg, ledger, events, Azure = setup(tmp_path, monkeypatch)
    class FailedCall(Azure):
        def deallocate(self):
            events.append('deallocate-failed')
            raise RuntimeError('timeout after request accepted')
    control.retire(FailedCall(cfg), ledger, attempts=1, sleep=lambda _:None)
    assert events == ['deallocate-failed', 'power']
    assert ledger.read()['active'] is None


def test_s5_unconfirmed_shutdown_emits_alarm_even_if_disk_fails(tmp_path, monkeypatch, capsys):
    cfg, ledger, events, Azure = setup(tmp_path, monkeypatch)
    class Running(Azure):
        def power(self): return 'VM running'
    def fail(*args): raise OSError('disk failed')
    monkeypatch.setattr(control, 'atomic', fail)
    with pytest.raises(RuntimeError, match='unconfirmed'):
        control.retire(Running(cfg), ledger, attempts=1, sleep=lambda _:None)
    assert 'ALARM' in capsys.readouterr().err
    assert ledger.read()['active'] is not None


def test_s6_failed_session_write_reconciles_without_start(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch, active=False)
    def fail(*args): raise OSError('session disk failed')
    monkeypatch.setattr(runner, 'atomic', fail)
    monkeypatch.setattr(runner, 'launch_guardian', lambda *a: events.append('launch'))
    with pytest.raises(OSError):
        runner.run(cfg, tmp_path/'config.json', spec())
    assert ledger.read()['active'] is None
    assert 'launch' not in events


def test_s8_pending_start_cannot_close_on_old_deallocated_observation(tmp_path, monkeypatch):
    cfg, ledger, events, Azure = setup(tmp_path, monkeypatch)
    data = ledger.read(); data['active']['start_pending'] = True
    control.atomic(ledger.path, data)
    with pytest.raises(RuntimeError, match='pending|unconfirmed'):
        control.retire(Azure(cfg), ledger, attempts=1, sleep=lambda _:None)
    assert ledger.read()['active'] is not None


def test_s10_reservation_is_committed_before_guardian_can_start(tmp_path, monkeypatch):
    cfg, ledger, events, _ = setup(tmp_path, monkeypatch, active=False)
    def launch(*args):
        assert ledger.read()['active']['job_id'] == 'job'
        with pytest.raises(ValueError, match='active'):
            ledger.reserve('second', 10, time.time())
        events.append('launch')
    monkeypatch.setattr(runner, 'launch_guardian', launch)
    runner.run(cfg, tmp_path/'config.json', spec())
    assert events[-1] == 'launch'


@pytest.mark.parametrize('phase', ['preparing','running','publishing','cleanup'])
def test_s7_ceiling_stop_does_not_depend_on_workload_phase(phase):
    session = {'start': 100, 'deadline': 500, 'phase': phase}
    assert runner.reap_reason(session, 499, 500) == 'deadline'


def test_s3_controller_loss_triggers_stop():
    assert runner.reap_reason({'start':100,'deadline':5000},100,701) == 'controller lost'


def test_s2_cancel_retirement_keeps_admission_locked(tmp_path, monkeypatch):
    cfg, ledger, events, Azure = setup(tmp_path, monkeypatch)
    original=runner.retire
    def observing(*args, **kwargs):
        with pytest.raises(OSError):
            with control.locked(tmp_path/'admission.lock'):
                pass
        return original(*args, **kwargs)
    monkeypatch.setattr(runner, 'retire', observing)
    runner.cancel(cfg, 'job')
    assert ledger.read()['active'] is None


def test_s8_reconcile_cannot_clear_pending_start(tmp_path, monkeypatch):
    cfg, ledger, events, Azure = setup(tmp_path, monkeypatch)
    data=ledger.read(); data['active']['start_pending']=True
    control.atomic(ledger.path,data)
    with pytest.raises(ValueError, match='pending'):
        runner.reconcile(cfg)
    assert ledger.read()['active'] is not None


def test_s6_reservation_write_failure_never_starts(tmp_path, monkeypatch):
    cfg, ledger, events, Azure = setup(tmp_path, monkeypatch, active=False)
    def fail(*a): raise OSError('reserve failed')
    monkeypatch.setattr(control,'atomic',fail)
    monkeypatch.setattr(runner,'launch_guardian',lambda *a:pytest.fail('started'))
    with pytest.raises(OSError): runner.run(cfg,tmp_path/'config.json',spec())
    assert ledger.read()['active'] is None


def test_s6_reconciliation_failure_keeps_charge_and_alarms(tmp_path,monkeypatch,capsys):
    cfg,ledger,events,Azure=setup(tmp_path,monkeypatch)
    def fail(*a): raise OSError('reconcile failed')
    monkeypatch.setattr(ledger,'finish',fail)
    with pytest.raises(RuntimeError):
        control.retire(Azure(cfg),ledger,attempts=1,sleep=lambda _:None)
    assert ledger.read()['active'] is not None
    assert 'ALARM' in capsys.readouterr().err


def test_s7_reservation_over_ceiling_never_launches(tmp_path,monkeypatch):
    cfg,ledger,events,Azure=setup(tmp_path,monkeypatch,active=False)
    data=ledger.read(); data['seed']['seconds']=control.WEEKLY_SECONDS-1
    control.atomic(ledger.path,data)
    monkeypatch.setattr(runner,'launch_guardian',lambda *a:pytest.fail('started'))
    with pytest.raises(ValueError,match='ceiling'):
        runner.run(cfg,tmp_path/'config.json',spec())
    assert ledger.read()['active'] is None


def test_s6_corrupt_ledger_does_not_veto_known_session_shutdown(tmp_path,monkeypatch,capsys):
    cfg,ledger,events,Azure=setup(tmp_path,monkeypatch)
    ledger.path.write_text('{broken')
    with pytest.raises(RuntimeError):
        control.retire(Azure(cfg),ledger,expected_job='job',attempts=1,sleep=lambda _:None)
    assert 'deallocate' in events
    assert 'ALARM' in capsys.readouterr().err


@pytest.mark.parametrize('fault', [None, 'cleanup', 'start_timeout', 'observation_write'])
def test_s1_s4_s6_controller_sequence_through_cli_boundary(tmp_path,monkeypatch,fault,capsys):
    from types import SimpleNamespace
    cfg,ledger,events,_=setup(tmp_path,monkeypatch,active=False)
    cfg.update(az='az.cmd',subscription='synthetic',resource_group='synthetic',
               vm='synthetic',location='synthetic',repository='https://github.com/Joshua-Asante/first-passage.git')
    session=ledger.reserve('job',3600,time.time())
    session.update(spec=spec(),mode='execute',runner_commit='b'*40,
                   bootstrap_deadline=time.time()+1800)
    path=tmp_path/'jobs/job/session.json';control.atomic(path,session)
    running=[False]
    def execute(args,**kwargs):
        op=tuple(args[1:3]);events.append(op)
        if op==('vm','start'):
            assert ledger.read()['active']['start_pending'] is True
            running[0]=True
            if fault=='start_timeout': raise TimeoutError('start uncertain')
        elif op==('vm','deallocate'):
            running[0]=False
        elif op==('vm','get-instance-view'):
            return SimpleNamespace(returncode=0,stdout=json.dumps(['VM running' if running[0] else 'VM deallocated']),stderr='')
        elif op==('rest','--method'):
            assert ledger.read()['active']['start_pending'] is False
            assert control.cleanup_pending(tmp_path)
        elif op==('vm','run-command'):
            if args[3]=='show':
                return SimpleNamespace(returncode=0,stdout=json.dumps({'instanceView':{'executionState':'Succeeded','exitCode':0}}),stderr='')
            if args[3]=='delete' and fault=='cleanup':
                return SimpleNamespace(returncode=1,stdout='',stderr='synthetic cleanup failure')
        return SimpleNamespace(returncode=0,stdout='{}',stderr='')
    monkeypatch.setattr(runner,'Azure',lambda config:control.Azure(config,execute=execute))
    monkeypatch.setattr(runner,'launch_reaper',lambda *a:None)
    original_atomic=runner.atomic
    if fault=='observation_write':
        def write(target,value):
            if target.name=='observation.json': raise OSError('disk failed')
            original_atomic(target,value)
        monkeypatch.setattr(runner,'atomic',write)
    original_retire=runner.retire
    monkeypatch.setattr(runner,'retire',lambda *a,**kw:original_retire(*a,**kw,attempts=1,sleep=lambda _:None))
    if fault=='start_timeout':
        with pytest.raises(RuntimeError,match='unconfirmed'):
            runner.guardian(cfg,path,tmp_path/'config.json')
        assert ledger.read()['active']['start_pending']
        assert 'ALARM' in capsys.readouterr().err
    else:
        runner.guardian(cfg,path,tmp_path/'config.json')
        assert ledger.read()['active'] is None
        assert ledger.read()['sessions'][0]['end'] >= session['start']
    assert not running[0]
    assert ('vm','deallocate') in events
    if fault=='cleanup':
        assert control.cleanup_pending(tmp_path)
        assert 'ALARM' in capsys.readouterr().err
    if fault is None:
        assert events.index(('vm','start')) < events.index(('rest','--method')) < events.index(('vm','deallocate'))
        assert not control.cleanup_pending(tmp_path)


def test_completed_archive_without_shutdown_is_not_job_completion(tmp_path,monkeypatch):
    from test_review_repairs import disk_job, retrieve
    from scripts.azure_jobs import guest
    job,repo,value,record=disk_job(tmp_path)
    guest.bundle(job,repo,['out'],partial=False)
    result=retrieve(tmp_path,monkeypatch,job)
    assert result['workload_verified'] is True
    assert result['verified'] is False


def test_s8_ledger_cannot_directly_finish_pending_start(tmp_path,monkeypatch):
    cfg,ledger,events,Azure=setup(tmp_path,monkeypatch)
    ledger.update_active('job',start_pending=True)
    with pytest.raises(ValueError,match='pending'):
        ledger.finish(time.time())
    assert ledger.read()['active'] is not None


@pytest.mark.parametrize('args', [
    ['--env','C:/other','test'], ['--env=C:/other','test'], ['--detach','test'],
    ['python','-c','print(1)'], ['python','untracked.py'], ['doctor'],
])
def test_v1_accepts_only_recorded_operations_launcher_tasks(args):
    value=spec();value['command']=['scripts/fp.py',*args]
    with pytest.raises(ValueError,match='launcher|recorded|operations'):
        contract.validate(value)


def test_s3_guest_watchdog_deallocation_failure_is_loud(tmp_path,monkeypatch,capsys):
    from scripts.azure_jobs import watchdog
    class Stop(BaseException): pass
    class Azure:
        def __init__(self,cfg): pass
        def deallocate(self): raise OSError('cloud unavailable')
    control.atomic(tmp_path/'config.json',{'guest_root':str(tmp_path)})
    monkeypatch.setattr(watchdog,'Azure',Azure)
    monkeypatch.setattr(watchdog,'cloud_lease',lambda:{'job_id':'job','deadline':0,'bootstrap_deadline':0})
    monkeypatch.setattr(watchdog,'terminate_tree',lambda name:True)
    monkeypatch.setattr(watchdog.time,'sleep',lambda _:(_ for _ in ()).throw(Stop()))
    with pytest.raises(Stop): watchdog.main(tmp_path/'config.json')
    assert 'ALARM' in capsys.readouterr().err


def test_s10_status_does_not_create_guest_command_for_unowned_vm(tmp_path,monkeypatch):
    cfg,ledger,events,Azure=setup(tmp_path,monkeypatch,active=False)
    class Running(Azure):
        def power(self): return 'VM running'
        def script(self,*a): pytest.fail('status mutated unowned VM')
    monkeypatch.setattr(runner,'Azure',Running)
    monkeypatch.setattr(runner,'blob',lambda *a:(_ for _ in ()).throw(RuntimeError('unpublished')))
    runner.status(cfg,'job')


def test_s10_status_serializes_guest_command_with_admission(tmp_path,monkeypatch):
    cfg,ledger,events,Azure=setup(tmp_path,monkeypatch)
    class Running(Azure):
        def power(self): return 'VM running'
        def script(self,*a):
            with pytest.raises(OSError):
                with control.locked(tmp_path/'admission.lock'): pass
            return json.dumps({'status':'running'})
    monkeypatch.setattr(runner,'Azure',Running)
    monkeypatch.setattr(runner,'blob',lambda *a:(_ for _ in ()).throw(RuntimeError('unpublished')))
    runner.status(cfg,'job')
