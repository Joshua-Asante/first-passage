from c1_rail.qualification.model import PathOutcome
from c1_rail.qualification.runner import StageRun
from c1_rail.qualification.adjudication import DecisionRules,adjudicate_stage


RULES=DecisionRules(.05,.05,.5,200)


def stage(name,n,failures,fast):
    rows=(PathOutcome('PASS',100,None,()),)*fast
    rows+=(PathOutcome('PASS',300,None,()),)*(n-failures-fast)
    rows+=(PathOutcome('UNRESOLVED',None,'horizon_cap',()),)*failures
    return StageRun(name,tuple((pool,rows) for pool in ('FULL','H1','H2')),0.,0.)


def test_screen_inclusive_cutoff_certifies_nothing():
    assert adjudicate_stage(stage('n1',200,10,0),RULES).status=='CONTINUE'
    assert adjudicate_stage(stage('n1',200,11,0),RULES).status=='FAILURE'


def test_exact_confirm_counts_and_speed_reuses_full():
    result=adjudicate_stage(stage('n2',970,37,512),RULES)
    assert result.status=='PASS'
    assert result.speed_successes==512
    assert result.cutoffs==(('FULL',37),('H1',37),('H2',37),('SPEED',512))
    assert adjudicate_stage(stage('n2',970,38,512),RULES).status=='FAILURE'
    assert adjudicate_stage(stage('n3',970,37,511),RULES).status=='FAILURE'
