from dataclasses import replace
from datetime import date, datetime, timedelta, timezone

import pytest

from c1_signal_daemon.feed import Bar
from mc.simulation import EvaluationState
from c1_rail.qualification.model import LEG_IDS, EdgeState, ReplayResult, SessionRecord, SessionSchedule, SourceBar, SourceSession
from c1_rail.qualification.part_a import SyntheticPartARequest, run_synthetic_part_a
from c1_rail.qualification.runner import NeedsContext
from c1_rail.qualification.replay import ReplayDeadlineFailure


STATE = EvaluationState(100000, 100000, 100000, 0, 0)
ZERO = tuple((leg, 0) for leg in LEG_IDS)
EDGE = EdgeState(ZERO, ZERO, ZERO)


def source():
    result = []
    for month in range(1, 13):
        ts = datetime(2024, month, 1, 15, tzinfo=timezone.utc)
        end = ts.replace(hour=20)
        result.append(SourceSession(str(month), ts.date(), (SourceBar(ts, (('aegis_6j', Bar(ts, 1, 1, 1, 1)),)),),
                                    SessionSchedule(end-timedelta(minutes=15), end-timedelta(minutes=5), end)))
    return tuple(result)


def request(**changes):
    return replace(SyntheticPartARequest('n2', 6, 5, 2, 5, 2, 4, .05, 'linear', 1., .01, 'test-only', 100., date(2030, 1, 7)), **changes)


def run(req, *, pnl=1200., full=1., timer=lambda: 0., proof_calls=None, replay_calls=None, deadline_failure=False, internal_domain=None):
    count = 0
    def prove(panel):
        if proof_calls is not None:
            proof_calls.append(panel)
        return (EDGE,) * (len(panel)+1), (True,) * (len(panel)-1)
    def replay(path):
        nonlocal count
        count += 1
        if replay_calls is not None:
            replay_calls.append(path)
        if deadline_failure and (count > 1 or deadline_failure == 'pilot'):
            s = path[0]
            raise ReplayDeadlineFailure(ReplayResult((SessionRecord(s.occurrence, s.path_session_date, s.source.session_id,
                                                                    0., 0., 0, False, EDGE, EDGE),), ()))
        return ReplayResult(tuple(SessionRecord(s.occurrence, s.path_session_date, s.source.session_id,
                                               pnl, min(pnl, 0.), int(pnl != 0), True, EDGE, EDGE) for s in path), ())
    entry=run_synthetic_part_a
    kwargs={}
    if internal_domain is not None:
        from c1_rail.qualification.part_a import _run_part_a
        entry=_run_part_a
        kwargs['synthetic']=internal_domain
    return entry(req, source(), adjacent=(True,)*11, covered_until=date(2025, 1, 1),
                 proof_provider=prove, replay_provider=replay, initial_state=STATE, full_pass_rate=full, timer=timer,**kwargs)


def test_expansion_preserves_initial_panels_and_rebuilds_every_occurrence_panel():
    proofs, replays = [], []
    expanded = run(request(), proof_calls=proofs, replay_calls=replays)
    initial_only = run(request(max_panels=2))
    assert expanded.expanded and expanded.passed
    assert expanded.panels[:2] == initial_only.panels
    assert len(proofs) == 5  # independent pilot plus four rebuilt alternate panels
    assert len(replays) == 9  # pilot plus depth two per panel
    assert all(len(panel) == 12 for panel in proofs)
    assert all(panel.passes == 2 for panel in expanded.panels)


def test_unresolved_counts_as_failure_and_far_from_floor_never_expands():
    result = run(request(), pnl=0.)
    assert not result.passed and not result.expanded
    assert len(result.panels) == 2
    assert all(p.passes == 0 and p.failures == 2 for p in result.panels)
    assert all(o.status == 'UNRESOLVED' for p in result.panels for o in p.outcomes)


def test_sanity_rejects_p5_above_full_and_n3_is_refused():
    assert run(request(), full=.9).failure_reason == 'p5_above_full'
    with pytest.raises(ValueError):
        request(stage='n3')


def test_budget_rejects_before_any_designated_panel():
    proofs, replays = [], []
    ticks = iter((0., 1., 2., 3.))
    with pytest.raises(NeedsContext, match='budget'):
        run(request(budget_seconds=.1), timer=lambda: next(ticks), proof_calls=proofs, replay_calls=replays)
    assert len(proofs) == len(replays) == 1


def test_expansion_band_is_inclusive_and_percentile_method_explicit():
    assert run(request(floor=.99, within_pp=.01)).expanded
    assert not run(request(floor=.98, within_pp=.01)).expanded
    with pytest.raises(ValueError):
        request(percentile_method='unspecified')


def test_typed_deadline_failure_counts_partial_path_as_failure_not_exclusion():
    result = run(request(), deadline_failure=True)
    assert not result.passed
    assert all(o.failure_reason == 'own_flat_deadline' for p in result.panels for o in p.outcomes)


def test_partial_pilot_cannot_supply_full_path_budget_measurement():
    with pytest.raises(NeedsContext, match='partial'):
        run(request(), deadline_failure='pilot')


def test_percentile_methods_have_distinct_frozen_interpretations():
    from c1_rail.qualification.part_a import _percentile, SyntheticPanelResult
    from c1_rail.qualification.model import PathOutcome
    yes, no = PathOutcome('PASS', 5, None, ()), PathOutcome('UNRESOLVED', None, 'horizon_cap', ())
    panels = (SyntheticPanelResult(0, ('a',), (no,)), SyntheticPanelResult(1, ('b',), (yes,)))
    assert _percentile(panels, .25, 'linear') == .25
    assert _percentile(panels, .25, 'nearest') == 0.


def test_nearest_rank_fifth_differs_from_nearest_sixth_of_one_hundred():
    from types import SimpleNamespace
    from c1_rail.qualification.part_a import _percentile
    panels = tuple(SimpleNamespace(pass_rate=i/100) for i in range(100))
    assert _percentile(panels, .05, 'nearest_rank') == .04
    assert _percentile(panels, .05, 'nearest') == .05
    assert _percentile(panels, 0., 'nearest_rank') == 0.
    assert _percentile(panels, 1., 'nearest_rank') == .99
    assert request(percentile_method='nearest_rank').percentile_method == 'nearest_rank'


def test_internal_production_domain_does_not_reuse_synthetic_panels():
    synthetic=run(request(),internal_domain=True)
    production=run(request(),internal_domain=False)
    assert synthetic.synthetic is True and production.synthetic is False
    assert tuple(p.source_session_ids for p in synthetic.panels)!=tuple(p.source_session_ids for p in production.panels)


def test_deadline_exception_cannot_contain_rows_after_failed_session():
    count=0
    def replay(path):
        nonlocal count
        count+=1
        rows=tuple(SessionRecord(s.occurrence,s.path_session_date,s.source.session_id,
            0.,0.,0,i!=0,EDGE,EDGE) for i,s in enumerate(path))
        if count==1:
            return ReplayResult(tuple(replace(row,flat_before_deadline=True) for row in rows),())
        raise ReplayDeadlineFailure(ReplayResult(rows,()))
    with pytest.raises(ValueError,match='terminal'):
        run_synthetic_part_a(request(),source(),adjacent=(True,)*11,covered_until=date(2025,1,1),
            proof_provider=lambda panel:((EDGE,)*(len(panel)+1),(True,)*(len(panel)-1)),
            replay_provider=replay,initial_state=STATE,full_pass_rate=1.,timer=lambda:0.)
