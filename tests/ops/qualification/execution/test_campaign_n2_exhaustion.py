"""C2 repair R2c: E08's N2 half.

Budget exhaustion and watchdogs during N2 from N2_READY, and restart with the
N2 reservation open."""

import base64
import json

import pytest
from test_campaign_n1 import clock, schedule_document, settle, snap, store, transition
from test_campaign_n2 import committed_n1, run_work
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore


def trusted_observation(instance, work, *, cpu=20, t=None, oom=0, memory=50):
    """A settlement observation over the enrolled scopes, with the watchdog
    fields the restart scene needs (a fresh clock, an OOM count) as overrides."""
    scopes = supervisor.work_enrollment('host1', instance.attempt, work)
    profile = snap(instance)['profile']
    phase = next(w['phase'] for w in snap(instance)['works'] if w['work_id'] == work)
    moment = json.loads(supervisor.observe_campaign_clock()) if t is None else clock({'t': t})
    return encoded(
        {
            'schema': 'qualification_campaign_observation/v2',
            'attempt_id': instance.attempt,
            'work_id': work,
            'clock': moment,
            'campaign_scope_id': scopes['campaign_slice'],
            'work_scope_id': scopes['payload_slice'],
            'cpu_ns': cpu,
            'memory_peak_bytes': memory,
            'oom_events': oom,
            'termination_known': True,
            'orchestration_charge_cpu_ns': profile['orchestration_cpu_ns'][phase],
        }
    )


def refuse_fresh_n2_draw(instance, work='n2late'):
    """A new N2 reservation meets the terminal budget, exactly as the BOUND
    analog's redraw refusal does after its watchdog fires."""
    state = snap(instance)
    with pytest.raises(ValueError, match='terminal campaign budget'):
        store(instance).reserve_work(
            instance.attempt,
            work,
            'N2',
            encoded(
                {
                    'limits': state['profile']['phases']['N2'],
                    'clock': json.loads(supervisor.observe_campaign_clock()),
                    'input_sha256': '0' * 64,
                }
            ),
            expected_revision=state['authority_revision'],
        )


def test_n2_work_wall_overrun_from_n2_ready_ends_authority(tmp_path, monkeypatch):
    # Pre-change: the work-wall watchdog (_terminal) did nothing from N2_READY, so the
    # campaign stayed N2_READY and accepted the overrunning transition.
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    state = snap(instance)
    work = next(w for w in state['works'] if w['work_id'] == 'n2work')
    assert state['state'] == 'N2_READY' and work['state'] == 'RUNNING'
    # Past the N2 work wall but still inside the campaign deadline, so only the
    # work-wall reason record_work_transition produces can fire (BOUND analog:
    # test_phase_wall_checked_before_capture_authority).
    instance.clocks['t'] = state['start_clock']['boottime_ns'] + work['limits']['wall_ns']
    transition(
        instance,
        'n2work',
        'CAPTURED',
        {'capture_bytes_b64': base64.b64encode(b'n2-work-wall-overrun').decode('ascii')},
    )
    final = snap(instance)
    assert final['state'] == 'BUDGET_EXHAUSTED'
    overrun = next(w for w in final['works'] if w['work_id'] == 'n2work')
    assert overrun['state'] == 'RUNNING', 'the overrunning transition is not accepted'
    with pytest.raises(ValueError, match='terminal campaign budget'):
        store(instance).claim_supervision_control(
            instance.attempt, 'n2work', 'START_CLIENT', supervisor.observe_campaign_clock()
        )


def test_n2_clock_regression_from_n2_ready_ends_authority(tmp_path, monkeypatch):
    # Pre-change: _observe_clock's regression watchdog (_terminal) did nothing from
    # N2_READY, so the settlement left the campaign N2_READY.
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    instance.clocks['t'] = 5  # behind the campaign's last trusted clock (21)
    settle(instance, 'n2work')
    final = snap(instance)
    assert final['state'] == 'BUDGET_UNCERTAIN'
    reopened = CampaignStore(ExecutionStore(instance.store.path))
    assert json.loads(reopened.budget_snapshot(instance.attempt))['state'] == (
        'BUDGET_UNCERTAIN'
    )
    refuse_fresh_n2_draw(instance)


def test_n2_compute_overrun_settles_to_budget_exhausted(tmp_path, monkeypatch):
    # Settlement runs through _settlement_terminal, which already covered the progression
    # states, so this N2 compute half of E08 may pass on the pre-change code.
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    limit = next(
        w for w in snap(instance)['works'] if w['work_id'] == 'n2work'
    )['limits']['cpu_ns']
    settle(instance, 'n2work', cpu=limit + 1)
    final = snap(instance)
    assert final['state'] == 'BUDGET_EXHAUSTED'
    work = next(w for w in final['works'] if w['work_id'] == 'n2work')
    assert work['charge_cpu_ns'] > work['limits'][
        'cpu_ns'
    ], 'an overrun consumes the whole reservation'
    with pytest.raises(ValueError, match='terminal campaign budget'):
        transition(instance, 'n2work', 'COMPLETED')


def test_restart_with_the_n2_reservation_open_recovers_without_new_authority(
    tmp_path, monkeypatch
):
    # Pre-change: recover_work's resource watchdog (_observe_resources -> _terminal) did
    # nothing from N2_READY, so the restart left the campaign merely IN_DOUBT.
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    before = snap(instance)
    reopened = CampaignStore(ExecutionStore(instance.store.path))
    reopened.recover_work(
        instance.attempt, 'n2work', trusted_observation(instance, 'n2work', t=22, oom=1)
    )
    final = snap(instance)
    assert final['state'] == 'BUDGET_EXHAUSTED'
    work = next(w for w in final['works'] if w['work_id'] == 'n2work')
    assert work['state'] == 'IN_DOUBT' and work['observation_bytes_b64'] is not None
    assert final['reserved_cpu_ns'] == 0 < before['reserved_cpu_ns']
    # No allowance reset or new authority: the open reservation is released and
    # settled at its observed charge, and the campaign total is conserved.
    assert final['settled_cpu_ns'] == before['settled_cpu_ns'] + work['charge_cpu_ns']
    totals = ('settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns')
    assert sum(final[k] for k in totals) == sum(before[k] for k in totals)
    refuse_fresh_n2_draw(instance)
