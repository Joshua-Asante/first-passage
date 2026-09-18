from datetime import date, timedelta
import pytest
from mc.simulation import EvaluationState
from c1_rail.qualification.model import LEG_IDS,EdgeState,SessionRecord,ReplayResult,PathOutcome
from c1_rail.qualification.runner import evaluate_replay,run_synthetic_stage,SyntheticStageRequest,NeedsContext


def result(values,failed=None):
    zero=tuple((leg,0) for leg in LEG_IDS);edge=EdgeState(zero,zero,zero)
    return ReplayResult(tuple(SessionRecord(i,date(2020,1,6)+timedelta(days=(i//5)*7+i%5),str(i),v,min(v,0),int(v!=0),i!=failed,edge,edge) for i,v in enumerate(values)),())


STATE=EvaluationState(100000,100000,100000,0,0)


def test_kernel_uses_intraday_and_no_second_scaling():
    observed={}
    def kernel(path,dd_trigger,dd_scale,horizon,**kw):
        observed.update(scale=dd_scale,low=kw['intraday_low'],initial=kw['initial_state'],inactivity=kw['inactivity_limit'])
        return 'bust_trailing',1,.03,0
    outcome=evaluate_replay(result([-2000,0]),initial_state=STATE,kernel=kernel)
    assert outcome.status=='FAILURE' and outcome.sessions_to_pass is None
    assert observed['scale']==1. and list(observed['low'])==[-2000,0]
    assert observed['initial'] is STATE and observed['inactivity']>2


def test_deadline_failure_never_source_exclusion_and_initial_state_required():
    assert evaluate_replay(result([0,0],failed=0),initial_state=STATE).failure_reason=='own_flat_deadline'
    with pytest.raises(TypeError):
        evaluate_replay(result([0]),initial_state=None)
    assert evaluate_replay(result([0]),initial_state=STATE).status=='UNRESOLVED'


def test_budget_probe_happens_before_any_population_path():
    calls=[]
    req=SyntheticStageRequest('n1',(('FULL',2),('H1',2),('H2',2)),2,'synthetic-test',1.)
    times=iter((0.,2.))
    with pytest.raises(NeedsContext,match='budget'):
        run_synthetic_stage(req,lambda **kw:(calls.append(kw) or result([0,0])),initial_state=STATE,timer=lambda:next(times))
    assert len(calls)==1 and calls[0]['stage']=='probe'


def test_population_depth_independent_and_speed_reuses_full():
    calls=[]
    req=SyntheticStageRequest('n2',(('FULL',2),('H1',3),('H2',4)),2,'synthetic-test',100.)
    output=run_synthetic_stage(req,lambda **kw:(calls.append(kw) or result([0,0])),initial_state=STATE)
    assert tuple((name,len(outcomes)) for name,outcomes in output.populations)==(('FULL',2),('H1',3),('H2',4))
    assert len(calls)==10  # distinct probe plus exactly nine requested paths
    assert len({c['seed'] for c in calls})==10
    assert output.synthetic is True


def test_stage_requires_exact_depths_and_full_horizon_output():
    with pytest.raises(ValueError):
        SyntheticStageRequest('n1',(('FULL',1),),2,'test',1.)
    req=SyntheticStageRequest('n1',(('FULL',1),('H1',1),('H2',1)),2,'test',100.)
    with pytest.raises(ValueError,match='horizon'):
        run_synthetic_stage(req,lambda **kw:result([0]),initial_state=STATE)


def test_internal_stage_domain_is_explicit_and_public_synthetic_stays_separate():
    from c1_rail.qualification.runner import _run_stage
    from c1_rail.qualification.regime import domain_seed
    calls=[]
    req=SyntheticStageRequest('n1',(('FULL',1),('H1',1),('H2',1)),2,'domain-fixture',100.)
    output=_run_stage(req,lambda **kw:(calls.append(kw) or result([0,0])),
                      initial_state=STATE,synthetic=False)
    assert output.synthetic is False
    expected=domain_seed(root='domain-fixture',stage='n1',population='FULL',panel_index=None,path_index=0,synthetic=False)
    assert calls[1]['seed']==expected
    assert expected!=domain_seed(root='domain-fixture',stage='n1',population='FULL',panel_index=None,path_index=0,synthetic=True)
