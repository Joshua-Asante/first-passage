"""Real worker computation returns bytes without journal or signing access."""
import base64
import importlib
import json

import pytest
from bundle_fixture import build_bundle
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.execution.plan import derive_n1_plan
from c1_rail.qualification.execution.protocol import decode_frame


def stage_input(root, case):
    installation = root / 'installation'
    installation.mkdir()
    (installation / 'release.json').write_bytes(case['release'])
    (installation / 'keys.json').write_bytes(encoded(dict(schema='qualification_trusted_keys/v1',
        keys=[dict(key_id=key.key_id, public_key_b64=base64.b64encode(key.public_key).decode(),
                   authority_class=key.authority_class, revoked_at=None) for key in case['keys'].values()])))
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    plan = derive_n1_plan(context.contract, attempt_id=context.attempt_id,
                          exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
    (root / 'plan.json').write_bytes(plan)
    return context


@pytest.mark.parametrize('idle', [False, True])
def test_worker_serializes_actual_paths_and_admission_without_verdict(tmp_path, monkeypatch, idle):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    case = build_bundle(tmp_path / 'bundle', idle=idle)
    context = stage_input(tmp_path, case)
    raw = worker.run_worker(tmp_path, execution_id='worker-fixture')
    doc = json.loads(decode_frame(raw, limit=context.profile.output_byte_limit))
    assert doc['legality']['status'] == 'PASS'
    assert doc['source_admission']['schema'] == 'qualification_source_admission/v1'
    from c1_rail.qualification.execution.protocol import sha256
    assert doc['legality']['source_admission_sha256'] == sha256(encoded(doc['source_admission']))
    assert doc['source_admission']['policy_sha256'] == context.policy.sha256
    assert doc['runtime_load_manifest'] == [dict(role=role,sha256=digest) for role,digest in sorted(context.contract.runtime_load_sha256.items())]
    assert len(doc['path_inventory']['records']) == 6
    assert [row['population'] for row in doc['populations']] == ['FULL', 'H1', 'H2']
    assert all(outcome['status'] == ('UNRESOLVED' if idle else 'PASS')
               for population in doc['populations'] for outcome in population['outcomes'])
    assert 'verdict' not in doc


def test_worker_rejects_caller_seed_plan_before_computation(tmp_path, monkeypatch):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    case = build_bundle(tmp_path / 'bundle')
    stage_input(tmp_path, case)
    plan = json.loads((tmp_path / 'plan.json').read_bytes())
    plan['seed_inputs'][0]['seed'] += 1
    (tmp_path / 'plan.json').write_bytes(encoded(plan))
    with pytest.raises(ValueError, match='derived plan'):
        worker.run_worker(tmp_path, execution_id='worker-fixture')


def test_capture_parser_rejects_boolean_path_indices(tmp_path,monkeypatch):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    from c1_rail.qualification.execution.evidence import parse_worker_result
    monkeypatch.setattr(worker,'utc_now',lambda:NOW)
    case = build_bundle(tmp_path/'bundle',idle=True)
    context = stage_input(tmp_path,case)
    plan = (tmp_path/'plan.json').read_bytes()
    doc = json.loads(decode_frame(worker.run_worker(tmp_path,execution_id='worker-fixture'),limit=context.profile.output_byte_limit))
    parse_worker_result(encoded(doc),context=context,execution_id='worker-fixture',plan_bytes=plan)
    for index in (0,1):
        doc['path_inventory']['records'][index]['path_index'] = bool(index)
        with pytest.raises(ValueError,match='path inventory'):
            parse_worker_result(encoded(doc),context=context,execution_id='worker-fixture',plan_bytes=plan)
        doc['path_inventory']['records'][index]['path_index'] = index


@pytest.mark.parametrize('phase', ['encode_worker_result','parse_worker_result','encode_frame'])
def test_retained_observations_include_completed_payload_work(tmp_path,monkeypatch,phase):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    budget = importlib.import_module('c1_rail.qualification.execution.budget')
    monkeypatch.setattr(worker,'utc_now',lambda:NOW)
    case = build_bundle(tmp_path/'bundle',idle=True)
    context = stage_input(tmp_path,case)
    meter = dict(wall=0,cpu=0,memory=1024)
    monkeypatch.setattr(budget,'perf_counter_ns',lambda:meter['wall'])
    monkeypatch.setattr(budget,'process_time_ns',lambda:meter['cpu'])
    monkeypatch.setattr(budget,'peak_memory_bytes',lambda:meter['memory'])
    original = getattr(worker,phase)
    def measured_payload_work(*args,**kwargs):
        result = original(*args,**kwargs)
        meter.update(wall=123456,cpu=654321,memory=32768)
        return result
    monkeypatch.setattr(worker,phase,measured_payload_work)
    raw = decode_frame(worker.run_worker(tmp_path,execution_id='worker-fixture'),limit=context.profile.output_byte_limit)
    assert json.loads(raw)['observations'] == dict(worker_compute_wall_ns=123456,
        worker_cpu_ns=654321,worker_peak_memory_bytes=32768)


@pytest.mark.parametrize('metric', ['wall','cpu','memory'])
def test_final_observation_serialization_overrun_cannot_return_result(tmp_path,monkeypatch,metric):
    from c1_rail.qualification.runner import NeedsContext
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    budget = importlib.import_module('c1_rail.qualification.execution.budget')
    monkeypatch.setattr(worker,'utc_now',lambda:NOW)
    case = build_bundle(tmp_path/'bundle',idle=True)
    context = stage_input(tmp_path,case)
    meter = dict(wall=0,cpu=0,memory=1024)
    monkeypatch.setattr(budget,'perf_counter_ns',lambda:meter['wall'])
    monkeypatch.setattr(budget,'process_time_ns',lambda:meter['cpu'])
    monkeypatch.setattr(budget,'peak_memory_bytes',lambda:meter['memory'])
    limits = dict(wall=context.contract.replay.budget.maximum_wall_seconds*1000000000,
        cpu=context.contract.replay.budget.maximum_cpu_seconds*1000000000,
        memory=context.contract.replay.budget.maximum_memory_bytes)
    original = worker.encode_frame
    calls = 0
    def late_overrun(*args,**kwargs):
        nonlocal calls
        result = original(*args,**kwargs)
        calls += 1
        if calls == 2:
            meter[metric] = limits[metric]+1
        return result
    monkeypatch.setattr(worker,'encode_frame',late_overrun)
    with pytest.raises(NeedsContext,match='budget'):
        worker.run_worker(tmp_path,execution_id='worker-fixture')


# ---- S4: the joint N2 worker path (one batch, staged plan + receipt) ---------


def joint_stage_input(root, case):
    from c1_rail.qualification.checkpoint_plan import derive_checkpoint_plan
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context

    context = stage_input(root, case)
    receipt = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_receipt/v1',
            'attempt_id': context.attempt_id,
            'checkpoint': 'N1',
            'work_id': 'g5work',
            'campaign_id': 'c1',
            'assessment_sha256': '0' * 64,
            'cutoff_sha256': '1' * 64,
            'decision': 'CONTINUE',
            'campaign_state': 'N2_READY',
            'signing_at_utc': '2026-09-22T00:00:00Z',
            'committed_at_utc': '2026-09-22T00:00:01Z',
            'intent_sha256': '2' * 64,
        }
    )
    (root / 'predecessor-receipt.json').write_bytes(receipt)
    plan = derive_checkpoint_plan(
        derive_campaign_plan_from_context(context), 'N2', receipt
    )
    (root / 'plan.json').write_bytes(plan)
    return context, plan


def test_worker_runs_the_joint_batch_with_staged_stage_tags(tmp_path, monkeypatch):
    import json

    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', joint=True)
    context, plan = joint_stage_input(tmp_path, case)
    raw = worker.run_worker(
        tmp_path, execution_id='n2work', checkpoint='N2'
    )
    doc = json.loads(decode_frame(raw, limit=context.profile.output_byte_limit))
    assert [row['population'] for row in doc['populations']] == ['FULL', 'H1', 'H2']
    assert [row.get('stage') for row in doc['populations']] == ['N2', 'PART_B', 'PART_B']
    counts = {row['population']: len(row['outcomes']) for row in doc['populations']}
    spec = context.contract.stage_specs
    assert counts == {
        'FULL': spec['N2'].exact_depth,
        'H1': spec['PART_B'].exact_depth,
        'H2': spec['PART_B'].exact_depth,
    }
    records = doc['path_inventory']['records']
    assert {row['stage'] for row in records} == {'N2', 'PART_B'}
    assert len(records) == sum(counts.values())
    assert 'verdict' not in doc


def test_worker_refuses_a_tampered_predecessor_receipt(tmp_path, monkeypatch):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', joint=True)
    joint_stage_input(tmp_path, case)
    tampered = json.loads((tmp_path / 'predecessor-receipt.json').read_bytes())
    tampered['decision'] = 'FAILURE'
    tampered['campaign_state'] = 'N1_FAILED'
    (tmp_path / 'predecessor-receipt.json').write_bytes(encoded(tampered))
    with pytest.raises(ValueError, match='committed predecessor decision differs'):
        worker.run_worker(tmp_path, execution_id='n2work', checkpoint='N2')
