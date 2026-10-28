"""Bounded release controls; all fixtures synthetic, never qualification runs."""
from datetime import datetime, timedelta, timezone
import io
import json
import os
from pathlib import Path
import sys
import subprocess
import hashlib
import importlib.util

import pytest

from discovery.orb_solo_release import (
    BoundedText, PhaseJournal, ReleaseError, validate_plan, guarded_event,
    MAX_CAPTURE_BYTES, phase_command, validate_admission, atomic_json,
)


def test_bounded_stream_and_atomic_receipt_preflight(tmp_path):
    target = io.StringIO()
    out = BoundedText(target, limit=4)
    assert out.write('é') == 1
    assert out.write('ab') == 2
    with pytest.raises(ReleaseError):
        out.write('x')
    assert target.getvalue() == 'éab'
    with pytest.raises(ReleaseError):
        atomic_json(tmp_path/'oversize.json', {'x':'a'*32}, limit=8)
    assert not (tmp_path/'oversize.json').exists()
    atomic_json(tmp_path/'receipt.json', {'ok':True}, limit=64)
    with pytest.raises(FileExistsError):
        atomic_json(tmp_path/'receipt.json', {'ok':False}, limit=64)


@pytest.mark.parametrize('event,args',[
    ('socket.__new__',()),('socket.connect',()),('socket.getaddrinfo',()),
    ('subprocess.Popen',()),('os.system',()),('open',('x','w',os.O_CREAT)),
    ('open',('x','r+',os.O_RDWR)),('os.remove',('x',)),('os.rename',('a','b')),
    ('os.mkdir',('x',)),('os.symlink',('x','y')),('os.link',('x','y')),
])
def test_all_worker_writes_and_launches_refused(event,args):
    with pytest.raises(ReleaseError):
        guarded_event(event,args)


def test_hostname_and_file_reads_only():
    guarded_event('socket.gethostname',())
    guarded_event('open',('x','r',os.O_RDONLY))
    guarded_event('open',('x','rb',os.O_RDONLY))


def test_journal_full_phase_lifecycle_and_monotone_charge(tmp_path):
    now = datetime.now(timezone.utc)
    journal = PhaseJournal.create(tmp_path/'ledger.json', setup_charged=14.28,
                                  deadline=(now+timedelta(hours=24)).isoformat())
    journal.begin('candidate', 'a'*64, now=now)
    assert journal.read()['reserved_phase_cpu_hours'] == 9.5
    with pytest.raises(ReleaseError):
        PhaseJournal(journal.path).begin('reference','a'*64,now=now)
    journal.finish(cpu_seconds=120,complete=True,receipt_path=tmp_path/'candidate-receipt.json',receipt={'phase':'candidate'})
    state = journal.read()
    assert state['charges']['setup'] == 14.28
    assert state['charges']['candidate'] == pytest.approx((120+60)/3600)
    assert state['completed'] == ['candidate']
    with pytest.raises(ReleaseError):
        journal.begin('candidate','a'*64,now=now)
    journal.begin('reference','a'*64,now=now)
    journal.finish(cpu_seconds=1,complete=False)
    assert journal.read()['charges']['reference'] == 9.5
    assert journal.read()['status'] == 'unknown'
    with pytest.raises(ReleaseError):
        journal.begin('seal','a'*64,now=now)


def test_journal_lost_controller_deadline_and_no_reinitialization(tmp_path):
    now = datetime.now(timezone.utc)
    path = tmp_path/'ledger.json'
    journal = PhaseJournal.create(path,setup_charged=14.28,deadline=now.isoformat())
    with pytest.raises(FileExistsError):
        PhaseJournal.create(path,setup_charged=14.28,deadline=now.isoformat())
    with pytest.raises(ReleaseError,match='deadline'):
        journal.begin('candidate','a'*64,now=now)
    with pytest.raises(ReleaseError):
        PhaseJournal.create(tmp_path/'reset.json',setup_charged=0,deadline=now.isoformat())


def plan():
    return dict(schema='orb-s4-release/v1', study='ORB-MNQ-v7-solo-S4-2026-10',
                phase='candidate',tiers=['Bulenox_100K','Tradeify_Select_100K','MFFU_Rapid_100K','BluSky_Premium_100K'],
                depth=dict(groups_per_population=19,sims_per_seed=10000,seeds=[42,123,2026],horizon=1500),
                mode='NORMAL',protection='OFF',inactivity_off=True,
                source_pins={'x':'a'*64},binding_sha256='b'*64,rules_sha256='c'*64,
                input_sha256='d'*64,producer_sha256='e'*64,admission_sha256='f'*64,
                freeze_commit='1'*40,freeze_contract_sha256='2'*64,
                operator_release='3'*64)


@pytest.mark.parametrize('field,value',[
    ('mode','PROTECTED'),('protection','ON'),('phase','other'),
    ('tiers',['FXIFY_Futures_Flex_150K']),('source_pins',{}),('operator_release',None),
])
def test_plan_refuses_variants_or_missing_identity(field,value):
    fixture=plan(); fixture[field]=value
    with pytest.raises(ReleaseError):
        validate_plan(fixture)


def test_exact_depth_and_fixed_worker_command(tmp_path):
    fixture=plan(); validate_plan(fixture)
    cmd=phase_command(tmp_path/'plan.json','a'*64)
    assert cmd == [sys.executable,'-B','-m','discovery.orb_solo_worker',str((tmp_path/'plan.json').resolve()),'a'*64]
    fixture['depth']['sims_per_seed']=9999
    with pytest.raises(ReleaseError):
        validate_plan(fixture)


def test_admission_never_trusts_caller_booleans():
    with pytest.raises(ReleaseError):
        validate_admission({'g1':True,'g2':True},plan())


def test_source_derived_admission_recomputed_from_synthetic_lots():
    from discovery.orb_solo_release import derive_candidate_admission, digest
    from discovery.remc_series_builder import Trade
    from zoneinfo import ZoneInfo
    ny=ZoneInfo('America/New_York')
    entries=[Trade('orb_mnq_v7',i,datetime(2024,1,day,10,tzinfo=ny),
                   datetime(2024,1,day,11,tzinfo=ny),1,99.,1.,-20.)
             for i,day in enumerate((8,9),1)]
    fixture=plan()
    derived=derive_candidate_admission(entries,[100.,100.],fixture)
    fixture['admission_sha256']=digest(derived)
    assert validate_admission(derived,fixture,derived=derived)['g1']['r_deploy'] == 2
    changed={**derived,'g1':True}
    with pytest.raises(ReleaseError):
        validate_admission(changed,fixture,derived=derived)
    assert all(row['clock_cap']['admissible'] for row in derived['tiers'].values())


def test_reference_route_requires_explicit_frozen_interpretation():
    from discovery.orb_solo_release import validate_reference_route
    with pytest.raises(ReleaseError):
        validate_reference_route({'reference_route':'bypass'})


def test_global_configuration_and_operator_release_are_bound():
    from discovery.orb_solo_release import validate_release_authorization,digest
    configuration={'depth':DEPTH_FIXTURE,'source_pins':{'x':'a'*64}}
    release=dict(study='ORB-MNQ-v7-solo-S4-2026-10',phase='candidate',
                 configuration_sha256=digest(configuration),operator='Joshua',
                 authorized=True,expires_at='2026-10-19T00:07:02-04:00')
    validate_release_authorization(release,configuration,'candidate',now=datetime(2026,10,17,tzinfo=timezone.utc))
    with pytest.raises(ReleaseError):
        validate_release_authorization(release,{'depth':{}},'candidate',now=datetime(2026,10,17,tzinfo=timezone.utc))
    with pytest.raises(ReleaseError):
        validate_release_authorization(release,configuration,'reference',now=datetime(2026,10,17,tzinfo=timezone.utc))


DEPTH_FIXTURE=dict(groups_per_population=19,sims_per_seed=10000,seeds=[42,123,2026],horizon=1500)


def test_compact_receipt_does_not_grow_with_sampling():
    from discovery.orb_solo_release import SampleRing
    ring=SampleRing(capacity=3)
    for index in range(100):
        ring.append(dict(elapsed=index,cpu_seconds=index,memory_bytes=1,new_disk_bytes=0,active_processes=1))
    evidence=ring.evidence()
    assert evidence['observations'] == 100 and len(evidence['tail']) == 3
    assert evidence['first']['elapsed'] == 0 and evidence['last']['elapsed'] == 99
    assert evidence['cpu_seconds_max'] == 99


def test_worker_read_allowlist(tmp_path):
    from discovery.orb_solo_release import WorkerPolicy
    source=tmp_path/'source.py'; source.write_text('x=1')
    policy=WorkerPolicy([source],runtime_roots=[])
    policy('open',(str(source),'r',os.O_RDONLY))
    with pytest.raises(ReleaseError):
        policy('open',(str(tmp_path/'other.txt'),'r',os.O_RDONLY))
    with pytest.raises(ReleaseError):
        policy('open',(str(source),'w',os.O_WRONLY))


@pytest.mark.skipif(os.name != 'nt',reason='actual Windows controller memory capability')
def test_native_controller_and_descendant_aggregate_memory(tmp_path):
    root=Path(__file__).resolve().parents[1]
    code=(f"import sys; sys.path[:0]=[{str(root)!r},{str(root/'lab')!r},{str(root/'core')!r}]; "
          "from discovery.orb_solo_release import ControllerMemoryJob; "
          "bound=ControllerMemoryJob(64*1024**2); "
          "exec('try:\\n payload=bytearray(128*1024**2)\\nexcept MemoryError:\\n print(\"HARD_MEMORY_REFUSED\")')")
    # A fresh process owns its bound; never constrain the pytest/controller host.
    result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
    assert result.returncode == 0,result.stderr
    assert 'HARD_MEMORY_REFUSED' in result.stdout


def test_fixed_worker_module_exists():
    assert importlib.util.find_spec('discovery.orb_solo_worker') is not None


def test_nonfinite_diagnostic_is_preserved_without_fake_zero():
    from discovery.orb_solo_release import json_ready
    assert json_ready({'median':float('inf'),'ratio':float('nan')}) == {
        'median':{'nonfinite':'inf'},'ratio':{'nonfinite':'nan'}}


def test_dispatch_refuses_before_launch_without_bound_configuration(tmp_path,monkeypatch):
    import discovery.orb_solo_release as api
    def forbidden(*args,**kwargs):
        pytest.fail('no process may launch without all release dependencies')
    monkeypatch.setattr(api,'_launch_fixed_worker',forbidden)
    path=tmp_path/'plan.json'; path.write_text(json.dumps(plan()))
    with pytest.raises(ReleaseError):
        api.execute_phase(path,hashlib.sha256(path.read_bytes()).hexdigest(),
                          journal_path=tmp_path/'journal.json',output=tmp_path/'run')


@pytest.mark.skipif(os.name != 'nt',reason='actual accepted Windows metadata/import context')
def test_fixed_worker_controls_without_any_mc(tmp_path):
    result=subprocess.run([sys.executable,'-B','-m','discovery.orb_solo_worker','--verify-controls'],
                          capture_output=True,text=True,timeout=15)
    assert result.returncode == 0,result.stderr
    value=json.loads(result.stdout)
    assert value['qualification_groups'] == 0 and value['imports_ok']
    assert value['denials_verified'] >= 4


def test_zero_edge_admission_retains_nonfinite_diagnostic():
    from discovery.orb_solo_release import derive_candidate_admission,canonical
    from discovery.remc_series_builder import Trade
    from zoneinfo import ZoneInfo
    ny=ZoneInfo('America/New_York')
    lot=Trade('orb_mnq_v7',1,datetime(2024,1,8,10,tzinfo=ny),datetime(2024,1,8,11,tzinfo=ny),1,-1.,1.,-2.)
    evidence=derive_candidate_admission([lot],[0.],plan())
    assert evidence['g1']['halted']
    assert evidence['g1']['expectancy_ratio']=={'nonfinite':'nan'}
    assert canonical(evidence)


def test_depth_validation_without_simulation():
    from discovery.orb_solo_worker import check_depth
    from types import SimpleNamespace
    tiers=plan()['tiers']
    report=SimpleNamespace(tiers={key:SimpleNamespace(g3_ok=True) for key in tiers})
    sidecar={key:dict(guard_arms={arm:dict(sims_per_seed=10000,n_seeds=3) for arm in ('eod','zeros','real')},
                days_to_pass={run:{'n':30000} for run in ('run1','run2')}) for key in tiers}
    assert check_depth(report,sidecar)==19
    sidecar[tiers[1]]['days_to_pass']['run2']['n']=29999
    with pytest.raises(ReleaseError):
        check_depth(report,sidecar)


def test_candidate_adapter_on_synthetic_export_only(tmp_path):
    import csv
    from discovery.remc_series_builder import TRADE_LIST_COLUMNS
    from discovery.orb_solo_worker import candidate_context
    source=tmp_path/'synthetic.csv'
    with source.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=TRADE_LIST_COLUMNS);writer.writeheader()
        for number,day in enumerate(('2024-01-08','2024-01-12'),1):
            for side,hour in (('Entry','10:00'),('Exit','11:00')):
                row=dict.fromkeys(TRADE_LIST_COLUMNS,'0')
                row.update({'Trade number':number,'Type':side+' long','Date and time':day+' '+hour,
                    'Size (qty)':1,'Net PnL USD':99,'Commission USD':1,'Adverse excursion USD':-20})
                writer.writerow(row)
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    binding=tmp_path/'binding.json'
    binding.write_text(json.dumps(dict(mode='NORMAL',protection='OFF',qty_scale=1,
        source_export_sha256=sha,source_export_timezone='America/New_York',
        resolved_port_parameters={'qty':1},capture_emulator_overrides={'commission_per_side':.5},
        proposed_complete_week_window=['2024-01-08','2024-01-12'])))
    fixture=plan();fixture['input_sha256']=sha
    configuration={'inputs':{'candidate':{'path':str(source),'sha256':sha},'binding':{'path':str(binding)}}}
    trades,bundle,daily,evidence=candidate_context(fixture,configuration)
    assert len(trades)==2 and len(bundle.dates)==5
    assert sum(daily)==200 and evidence['g1']['r_deploy']==2


@pytest.mark.parametrize('failpoint',['before_receipt','after_receipt'])
def test_phase_cannot_advance_across_failed_publication(tmp_path,monkeypatch,failpoint):
    import discovery.orb_solo_release as api
    now=datetime.now(timezone.utc)
    journal=PhaseJournal.create(tmp_path/'journal.json',setup_charged=14.28,deadline=(now+timedelta(hours=1)).isoformat())
    journal.begin('candidate','a'*64,now=now)
    target=tmp_path/'candidate-receipt.json'
    original=api.atomic_json
    original_write=journal._write
    if failpoint=='before_receipt':
        def fail(path,value,**kwargs):
            if Path(path)==target:
                raise OSError('simulated publication failure')
            return original(path,value,**kwargs)
        monkeypatch.setattr(api,'atomic_json',fail)
    else:
        def fail(state):
            if state['status']=='idle':
                raise OSError('simulated crash after receipt before commit')
            return original_write(state)
        monkeypatch.setattr(journal,'_write',fail)
    with pytest.raises(OSError):
        journal.finish(cpu_seconds=1,complete=True,receipt_path=target,receipt={'phase':'candidate'})
    assert journal.read()['status']=='sealing'
    assert journal.read()['charges']['candidate']==9.5
    assert journal.read()['completed']==[]
    with pytest.raises(ReleaseError):
        PhaseJournal(journal.path).begin('reference','a'*64,now=now)


def test_reference_requires_every_tier_and_no_false_g3():
    from discovery.orb_solo_worker import check_depth
    from types import SimpleNamespace
    for tiers in ({},{'Bulenox_100K':SimpleNamespace(g3_ok=False)}):
        with pytest.raises(ReleaseError):
            check_depth(SimpleNamespace(tiers=tiers),{},phase='reference')


def test_candidate_only_source_proved_kills_reduce_depth():
    from discovery.orb_solo_worker import check_depth
    from types import SimpleNamespace
    tiers=plan()['tiers']
    report=SimpleNamespace(tiers={key:SimpleNamespace(g3_ok=(key==tiers[0]),gated_on='g2_killed') for key in tiers},
                           g1=SimpleNamespace(halted=False))
    admission={'g1':{'halted':False},'tiers':{key:{'g2':{'passed':False}} for key in tiers}}
    admission['tiers'][tiers[0]]['g2']['passed']=True
    sidecar={tiers[0]:dict(guard_arms={arm:dict(sims_per_seed=10000,n_seeds=3) for arm in ('eod','zeros','real')},
                          days_to_pass={run:{'n':30000} for run in ('run1','run2')})}
    assert check_depth(report,sidecar,phase='candidate',admission=admission)==4
    admission['tiers'][tiers[1]]['g2']['passed']=True
    with pytest.raises(ReleaseError):
        check_depth(report,sidecar,phase='candidate',admission=admission)


def test_completed_phase_requires_unchanged_publication(tmp_path):
    now=datetime.now(timezone.utc)
    journal=PhaseJournal.create(tmp_path/'journal.json',setup_charged=14.28,deadline=(now+timedelta(hours=1)).isoformat())
    journal.begin('candidate','a'*64,now=now)
    receipt=tmp_path/'candidate.json'
    journal.finish(cpu_seconds=1,complete=True,receipt_path=receipt,receipt={'status':'completed'})
    receipt.write_text('{}')
    with pytest.raises(ReleaseError):
        PhaseJournal(journal.path).begin('reference','a'*64,now=now)


def test_reference_adapter_exact_shape_without_recosting(tmp_path,monkeypatch):
    import csv
    import discovery.orb_solo_worker as worker
    from discovery.orb_solo_release import validate_reference_route
    from datetime import date
    first,last=date(2020,1,6),date(2026,7,1)
    dates=[first+timedelta(days=i) for i in range((last-first).days+1) if (first+timedelta(days=i)).weekday()<5]
    source=tmp_path/'synthetic-reference.csv'
    with source.open('w',newline='',encoding='utf-8') as handle:
        writer=csv.writer(handle);writer.writerow(['date','striker','striker_nas100','aegis','intraday_low'])
        writer.writerows((str(day),1.,2.,3.,-8.) for day in dates)
    route=dict(kind='I20-bust-only',source='2026-10-06-executor-0.5-5',
        panel_sha256='a2e9192aec54dd081245232247f5f5306553910a2956f3601364c050f9aa50a2',
        cost_policy='already-net-no-additional-cost',g1_g2='documented-reference-only-bypass',explicit_in_frozen_contract=True)
    configuration=dict(reference_route=route,inputs={'reference':{'path':str(source),'sha256':route['panel_sha256']}})
    # Synthetic file represents the identity-admitted panel at this pure loader
    # boundary. No actual reference bytes, metrics or simulation are accessed.
    monkeypatch.setattr(worker,'file_digest',lambda _:route['panel_sha256'])
    pnl,low=worker.reference_context(configuration)
    assert len(pnl)==len(low)==1690
    assert (pnl==6).all() and (low==-8).all()


def test_reference_and_candidate_routes_use_source_shaped_reports(monkeypatch):
    import numpy as np
    import discovery.orb_solo_worker as worker
    import discovery.prop_survivor_scoring as scoring
    from types import SimpleNamespace
    from discovery.orb_solo_release import digest, required_source_paths, WorkerPolicy
    # Apply the real worker policy at each threshold-file read without installing
    # an irreversible process-wide audit hook in the pytest process.
    root=Path(__file__).resolve().parents[1]
    frozen_v2=root/'docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md'
    sources=required_source_paths(root)
    assert frozen_v2 in sources
    assert not set(scoring.DEFAULT_ADDENDA).intersection(sources)
    policy=WorkerPolicy(sources,runtime_roots=[])
    original_read_text=Path.read_text
    def pinned_read_text(path,*args,**kwargs):
        policy('open',(str(path),'r',os.O_RDONLY))
        return original_read_text(path,*args,**kwargs)
    monkeypatch.setattr(Path,'read_text',pinned_read_text)
    fixture=plan()
    configuration={}
    admission={'schema':'orb-s4-admission/v1','input_sha256':fixture['input_sha256'],
        'binding_sha256':fixture['binding_sha256'],'rules_sha256':fixture['rules_sha256'],
        'producer_sha256':fixture['producer_sha256'],
        'g1':{'halted':False,'deployable_default_envelope':'YES'},
        'tiers':{key:dict(g2={'passed':True},clock_cap={'admissible':True,'reason':'synthetic'}) for key in fixture['tiers']}}
    fixture['admission_sha256']=digest(admission)
    calls=[]
    def fake_score(**kwargs):
        calls.append(kwargs)
        assert kwargs['thresholds'].sims_per_seed==10000
        assert kwargs['thresholds'].cost_law_multiple==4.0
        assert kwargs['thresholds'].source_path==str(frozen_v2)
        assert kwargs['thresholds'].addenda==()
        report=scoring.ScoringReport('synthetic',scoring.G1Result(2,1.,'YES',False))
        for key in fixture['tiers']:
            report.tiers[key]=scoring.TierScore(key,'trailing_locking',None,True,{}, {},False,False,'run2')
            captured=kwargs['sidecar'][key]=dict(guard_arms={arm:{'sims_per_seed':10000,'n_seeds':3} for arm in ('eod','zeros','real')},
                  days_to_pass={'run1':{'n':30000},'run2':{'n':30000}})
            if key=='Bulenox_100K':
                captured['days_to_pass']['run2']=captured['days_to_pass']['run1']
        return report
    monkeypatch.setattr(scoring,'score_candidate',fake_score)
    bundle=SimpleNamespace(tiers={key:{'pnl':np.zeros(5),'low':-np.ones(5)} for key in fixture['tiers']})
    monkeypatch.setattr(worker,'candidate_context',lambda *a:([SimpleNamespace(gross_usd=2.)],bundle,np.array([2.,0.,0.,0.,0.]),admission))
    monkeypatch.setattr(worker,'read_json',lambda *a,**kw:admission)
    configuration['inputs']={'candidate_admission':{'path':'synthetic-only'}}
    result=worker.evaluate_phase(fixture,configuration)
    assert result['groups_completed']==19 and calls[-1]['tier_series']
    fixture['phase']='reference'
    monkeypatch.setattr(worker,'reference_context',lambda *a:(np.zeros(1690),-np.ones(1690)))
    result=worker.evaluate_phase(fixture,configuration)
    assert result['groups_completed']==19 and calls[-1]['full_res_trades']==[]
    assert calls[-1]['gross_edge_usd']==float('inf')


def test_running_lease_after_controller_loss_cannot_be_reused(tmp_path):
    now=datetime.now(timezone.utc)
    journal=PhaseJournal.create(tmp_path/'journal.json',setup_charged=14.28,deadline=(now+timedelta(hours=1)).isoformat())
    journal.begin('candidate','a'*64,now=now)
    replacement=PhaseJournal(journal.path)
    assert replacement.read()['reserved_phase_cpu_hours']==9.5
    with pytest.raises(ReleaseError):
        replacement.begin('candidate','a'*64,now=now)
    with pytest.raises(ReleaseError):
        replacement.begin('reference','a'*64,now=now)


@pytest.mark.skipif(os.name != 'nt',reason='real nested controller/worker Job boundary')
def test_native_controller_memory_job_composes_with_worker_shutdown(tmp_path):
    root=Path(__file__).resolve().parents[1]
    source=Path(__file__).resolve()
    code=(f"import sys; sys.path[:0]=[{str(root)!r},{str(root/'lab')!r},{str(root/'core')!r}]; "
        "from discovery.orb_solo_release import ControllerMemoryJob; "
        "from discovery.orb_solo_executor import run_owned; "
        "bound=ControllerMemoryJob(256*1024**2); "
        f"r=run_owned([[sys.executable,'-c','pass']],cwd={str(tmp_path)!r},output={str(tmp_path/'owned')!r},"
        f"pins={{{str(source)!r}:{hashlib.sha256(source.read_bytes()).hexdigest()!r}}}); "
        "assert r['status']=='completed' and r['active_processes']==0; print('NESTED_BOUNDARY_OK')")
    result=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,text=True,timeout=10)
    assert result.returncode==0,result.stderr
    assert 'NESTED_BOUNDARY_OK' in result.stdout


@pytest.mark.skipif(os.name != 'nt',reason='real independent native deadline stop')
def test_watchdog_stops_blocked_controller_and_preserves_reservation(tmp_path):
    root=Path(__file__).resolve().parents[1]
    journal_path=tmp_path/'journal.json'
    body=(f"import sys,time; sys.path[:0]=[{str(root)!r},{str(root/'lab')!r},{str(root/'core')!r}]; "
        "from datetime import datetime,timedelta,timezone; "
        "from discovery.orb_solo_release import ControllerMemoryJob,PhaseJournal,PhaseWatchdog; "
        f"journal=PhaseJournal.create({str(journal_path)!r},setup_charged=14.28,deadline=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()); "
        "bound=ControllerMemoryJob(256*1024**2); journal.begin('candidate','a'*64); "
        "watch=PhaseWatchdog(bound.job,cpu_ceiling=1000,initialization_allowance=1,wall_deadline=time.monotonic()+.2); "
        "watch.start(); time.sleep(30)")
    result=subprocess.run([sys.executable,'-B','-c',body],capture_output=True,text=True,timeout=5)
    assert result.returncode!=0
    state=PhaseJournal(journal_path).read()
    assert state['status']=='running' and state['reserved_phase_cpu_hours']==9.5
    with pytest.raises(ReleaseError):
        PhaseJournal(journal_path).begin('reference','a'*64)
