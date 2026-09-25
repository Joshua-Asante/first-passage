"""S4 R3: checkpoint contents retain their version across launch and recovery."""

import json

import pytest
from test_campaign_n1 import snap, store
from test_campaign_n2 import (
    capture_checkpoint, committed_n1, committed_receipt, n2_plan, run_work,
    worker_payload,
)
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot


def captured_n2(tmp_path, monkeypatch):
    instance = committed_n1(tmp_path, monkeypatch)
    run_work(instance, 'n2work', 'n2_worker')
    payload = worker_payload(
        instance, plan=n2_plan(instance, committed_receipt(instance)),
        checkpoint='N2', work='n2work',
    )
    capture_checkpoint(instance, 'n2work', 'N2', payload)
    return instance


def test_v6_rejects_n2_checkpoint_contents(tmp_path, monkeypatch):
    instance = captured_n2(tmp_path, monkeypatch)
    state = snap(instance)
    assert state['schema'].endswith('/v7')
    state['schema'] = 'qualification_campaign_budget_snapshot/v6'
    with pytest.raises(ValueError, match='checkpoint.*version'):
        parse_campaign_budget_snapshot(encoded(state))


def test_v7_requires_n2_checkpoint_contents(tmp_path, monkeypatch):
    instance = committed_n1(tmp_path, monkeypatch)
    state = snap(instance)
    assert state['schema'].endswith('/v6')
    state['schema'] = 'qualification_campaign_budget_snapshot/v7'
    with pytest.raises(ValueError, match='checkpoint.*version'):
        parse_campaign_budget_snapshot(encoded(state))


@pytest.mark.parametrize('boundary', ['launch', 'recovery'])
def test_n2_snapshot_version_survives_control_boundary(tmp_path, monkeypatch, boundary):
    instance = captured_n2(tmp_path, monkeypatch)
    run_work(instance, 'n2g5', 'n2_g5')
    campaigns = store(instance)
    if boundary == 'launch':
        with campaigns.launch_gate(
            instance.attempt, 'n2g5', supervisor.observe_campaign_clock,
        ):
            pass
    else:
        campaigns.claim_supervision_control(
            instance.attempt, 'n2g5', 'RECOVERY_OWNER',
            supervisor.observe_campaign_clock(), recovery_owner_token=b'x' * 32,
        )
    state = json.loads(campaigns.budget_snapshot(instance.attempt))
    assert state['schema'] == 'qualification_campaign_budget_snapshot/v7'
    assert set(state['checkpoints']) == {'N1', 'N2'}
