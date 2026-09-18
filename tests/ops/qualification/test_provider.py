from datetime import date,timedelta
from c1_rail.qualification.benchmark import synthetic_source,synthetic_replay
from c1_rail.qualification.provider import SyntheticReplayProvider
from dataclasses import replace
import pytest
from c1_rail.qualification.replay import ReplayDeadlineFailure
from c1_rail.qualification.runner import NeedsContext


def test_provider_uses_ceil_partition_rebuilds_proofs_and_fresh_paths():
    sessions=tuple(synthetic_source(date(2020,1,6)+timedelta(days=i)) for i in range(5))
    calls=[]
    def replay(path):
        calls.append(tuple(s.source.session_id for s in path))
        return synthetic_replay(path)
    provider=SyntheticReplayProvider(sessions,(True,)*4,block_sessions=1,
                                    path_start_date=date(2020,2,3),replay=replay)
    assert tuple(map(len,provider.populations.values()))==(5,3,2)
    result=provider(stage='n1',population='H2',path_index=0,seed=91232,horizon_sessions=3)
    assert len(calls)==4  # each pool proved once; one freshly sampled path
    assert len(result.sessions)==3
    assert set(calls[-1])<=set(s.session_id for s in sessions[3:])


def test_source_proof_deadline_failure_is_missing_prerequisite():
    sessions=tuple(synthetic_source(date(2020,1,6)+timedelta(days=i)) for i in range(2))
    def replay(path):
        result=synthetic_replay(path)
        raise ReplayDeadlineFailure(replace(result,sessions=(replace(result.sessions[0],flat_before_deadline=False),)))
    with pytest.raises(NeedsContext,match='source proof'):
        SyntheticReplayProvider(sessions,(True,),block_sessions=1,path_start_date=date(2020,2,3),replay=replay)


@pytest.mark.parametrize('mismatch', ['source','not_failed','earlier_failure'])
def test_trial_deadline_exception_requires_designated_terminal_prefix(mismatch):
    sessions=tuple(synthetic_source(date(2020,1,6)+timedelta(days=i)) for i in range(2))
    provider=SyntheticReplayProvider(sessions,(True,),block_sessions=1,
        path_start_date=date(2020,2,3),replay=synthetic_replay)
    def replay(path):
        result=synthetic_replay(path)
        rows=list(result.sessions)
        rows[-1]=replace(rows[-1],flat_before_deadline=False)
        if mismatch=='source':
            rows[0]=replace(rows[0],source_session_id='WRONG_SOURCE')
        elif mismatch=='not_failed':
            rows[-1]=replace(rows[-1],flat_before_deadline=True)
        else:
            rows[0]=replace(rows[0],flat_before_deadline=False)
        raise ReplayDeadlineFailure(replace(result,sessions=tuple(rows)))
    provider.replay=replay
    with pytest.raises(ValueError):
        provider(stage='n1',population='FULL',path_index=0,seed=18,horizon_sessions=2)


def test_valid_deadline_prefix_propagates_as_designated_trial_failure():
    sessions=tuple(synthetic_source(date(2020,1,6)+timedelta(days=i)) for i in range(2))
    provider=SyntheticReplayProvider(sessions,(True,),block_sessions=1,
        path_start_date=date(2020,2,3),replay=synthetic_replay)
    def replay(path):
        result=synthetic_replay(path)
        raise ReplayDeadlineFailure(replace(result,sessions=(replace(result.sessions[0],flat_before_deadline=False),)))
    provider.replay=replay
    with pytest.raises(ReplayDeadlineFailure):
        provider(stage='n1',population='FULL',path_index=0,seed=18,horizon_sessions=2)
