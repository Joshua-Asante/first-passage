"""Real worker computation returns bytes without journal or signing access."""
import base64
import importlib
import json
import os
import shutil
import stat

import pytest
from bundle_fixture import build_bundle
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.execution.plan import derive_n1_plan
from c1_rail.qualification.execution.protocol import decode_frame, sha256


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


# ---- S5: the PART_A worker route (W1 staged custody, S5-D1 prefix artifacts) --


def _stage_bundle(case, mount):
    """``run_worker`` reads its retained bundle from <input>/bundle; a staged
    mount in its own directory sees byte-identical retained files."""
    shutil.copytree(case['root'], mount / 'bundle')


def _part_a_predecessor_documents(pa, context, payload):
    """Write the three staged N2 predecessor documents into a PART_A mount.

    The assessment is a minimal wrapper, not G5's real one: G5 builds the real
    committed assessment, and the worker's W1 checks bind only these facts to
    the staged bytes (the receipt's ``assessment_sha256`` and the assessment's
    capture digests, the payload digest among them).
    """
    assessment = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_assessment/v1',
            'checkpoint': 'N2',
            'decision': 'CONTINUE',
            'capture': {
                'result_sha256': '3' * 64,
                'payload_sha256': sha256(payload),
                'attestation_sha256': '4' * 64,
            },
        }
    )
    receipt = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_receipt/v1',
            'attempt_id': context.attempt_id,
            'checkpoint': 'N2',
            'work_id': 'n2g5',
            'campaign_id': 'c1',
            'assessment_sha256': sha256(assessment),
            'cutoff_sha256': '1' * 64,
            'decision': 'CONTINUE',
            'campaign_state': 'PART_A_READY',
            'signing_at_utc': '2026-09-22T02:00:00Z',
            'committed_at_utc': '2026-09-22T02:00:01Z',
            'intent_sha256': '2' * 64,
            'predecessor_receipt_sha256': '5' * 64,
            'stage_decisions': {'N2': 'PASS', 'PART_B': 'PASS'},
        }
    )
    (pa / 'predecessor-receipt.json').write_bytes(receipt)
    (pa / 'predecessor-assessment.json').write_bytes(assessment)
    (pa / 'predecessor-payload.json').write_bytes(payload)
    return assessment, receipt


def _write_part_a_plan(pa, context, receipt):
    from c1_rail.qualification.checkpoint_plan import derive_checkpoint_plan
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context

    plan = derive_checkpoint_plan(derive_campaign_plan_from_context(context), 'PART_A', receipt)
    (pa / 'plan.json').write_bytes(plan)
    return plan


def part_a_stage_input(tmp_path, case, monkeypatch):
    """A guardian-staged PART_A mount over a genuine committed N2 capture.

    The staged payload is a genuine N2 worker payload (SR-5): the real joint
    worker runs once on its own mount, and its framed result is exactly the
    capture the PART_A mount stages. Returns ``(context, pa, out, payload,
    assessment, receipt)``.
    """
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    n2 = tmp_path / 'n2'
    n2.mkdir()
    _stage_bundle(case, n2)
    context, _ = joint_stage_input(n2, case)
    payload = decode_frame(
        worker.run_worker(n2, execution_id='n2work', checkpoint='N2'),
        limit=context.profile.output_byte_limit,
    )
    pa = tmp_path / 'pa'
    pa.mkdir()
    stage_input(pa, case)
    _stage_bundle(case, pa)
    assessment, receipt = _part_a_predecessor_documents(pa, context, payload)
    _write_part_a_plan(pa, context, receipt)
    out = tmp_path / 'out'
    out.mkdir()
    return context, pa, out, payload, assessment, receipt


def hand_staged_part_a(tmp_path, case, monkeypatch):
    """The same PART_A mount without the N2 worker run, for the cheap refusals.

    The staged payload is a closed-shape stand-in: the W1 digest chain and the
    captured outcome-status parse are all these routes read, never the
    capture's genuineness (``part_a_stage_input`` owns SR-5).
    """
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    pa = tmp_path / 'pa'
    pa.mkdir()
    context = stage_input(pa, case)
    _stage_bundle(case, pa)
    depth = context.contract.stage_specs['N2'].exact_depth
    outcome = {'status': 'PASS', 'sessions_to_pass': 1, 'failure_reason': None, 'diagnostics': []}
    payload = encoded(
        {
            'schema': 'qualification_worker_result/v1',
            'execution_id': 'n2work',
            'plan_sha256': '0' * 64,
            'source_admission': {},
            'legality': {},
            'runtime_load_manifest': [],
            'populations': [
                dict(population='FULL', stage='N2', outcomes=[dict(outcome) for _ in range(depth)])
            ],
            'path_inventory': {},
            'observations': {},
        }
    )
    assessment, receipt = _part_a_predecessor_documents(pa, context, payload)
    _write_part_a_plan(pa, context, receipt)
    out = tmp_path / 'out'
    out.mkdir()
    return context, pa, out, payload, assessment, receipt


def test_worker_runs_part_a_with_both_prefix_artifacts(tmp_path, monkeypatch):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, payload, assessment, receipt = part_a_stage_input(tmp_path, case, monkeypatch)
    overrides = []
    original = worker.run_part_a_body

    def spying_body(*args, **kwargs):
        overrides.append(kwargs.get('measurement_override'))
        return original(*args, **kwargs)

    monkeypatch.setattr(worker, 'run_part_a_body', spying_body)
    frame = worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out)
    doc = json.loads(decode_frame(frame, limit=context.profile.output_byte_limit))
    part_a_worker_launch_count = len(overrides)
    initial_panel_bytes = (out / 'part-a-initial.jsonl').read_bytes()
    final_panel_bytes = (out / 'part-a-final.jsonl').read_bytes()
    part = context.contract.replay.part_a
    initial_panels = part.initial_panels
    expanded_panels = part.expanded_panels
    expansion_required = doc['part_a']['expansion_required']
    actual_panel_count = doc['part_a']['final_panels']
    assert final_panel_bytes[:len(initial_panel_bytes)] == initial_panel_bytes
    assert actual_panel_count == (expanded_panels if expansion_required else initial_panels)
    assert part_a_worker_launch_count == 1
    # No expansion on this fixture: the initial prefix is the whole final
    # artifact, and the panel vector is exactly the initial panel count.
    assert expansion_required is False
    assert actual_panel_count == initial_panels == len(doc['part_a']['panels'])
    assert doc['part_a']['initial_prefix_sha256'] == sha256(initial_panel_bytes)
    assert doc['part_a']['final_sha256'] == sha256(final_panel_bytes)
    # W5a: the panel-major occurrence inventory keys each panel by the digest
    # of the plan's outer seed for it (population REGIME, panel index kept
    # beside it), in the panel-major order the installed adjudicator reads.
    plan_document = json.loads((pa / 'plan.json').read_bytes())
    potential = plan_document['part_a']['potential_panels']
    records = doc['path_inventory']['records']
    depth = part.paths_per_population_per_panel
    assert len(records) == initial_panels * depth
    assert {row['stage'] for row in records} == {'PART_A'}
    assert {row['population'] for row in records} == {'REGIME'}
    identities = [sha256(encoded(panel['outer_seed'])) for panel in potential[:initial_panels]]
    assert len(set(identities)) == len(identities)
    for panel_index, identity in enumerate(identities):
        block = records[panel_index * depth:(panel_index + 1) * depth]
        assert [row['panel_index'] for row in block] == [panel_index] * depth
        assert [row['path_index'] for row in block] == list(range(depth))
        assert {row['panel_id'] for row in block} == {identity}
    # W5a: the probe identity (the plan's probe seed-input digests) and the
    # worker's own N2 FULL baseline, derived from the staged capture statuses.
    assert doc['part_a']['pilot'] == {
        'seed_input_sha256s': [sha256(encoded(seed)) for seed in plan_document['seed_inputs']]
    }
    staged_full = json.loads(payload)['populations'][0]['outcomes']
    assert doc['part_a']['n2_full_baseline'] == {
        'passes': sum(row['status'] == 'PASS' for row in staged_full),
        'paths': len(staged_full),
    }
    # SR-4 read-only by convention. Windows chmod carries only the read-only
    # attribute and os.stat synthesizes the mode bits there, so the 0o444
    # equality is asserted as the POSIX fact it is (not a pytest skip).
    if os.name != 'nt':
        for name in ('part-a-initial.jsonl', 'part-a-final.jsonl'):
            assert stat.S_IMODE((out / name).stat().st_mode) == 0o444
    # P-3: the route never passes a measurement override.
    assert overrides == [None]


def test_part_a_initial_artifact_is_fsynced_before_the_decision(tmp_path, monkeypatch):
    """S5-D1 custody ordering: the initial artifact's fsync precedes the first
    percentile (the expansion decision input), and the final artifact's fsync
    follows the last one."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    part_a = importlib.import_module('c1_rail.qualification.part_a')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, payload, assessment, receipt = hand_staged_part_a(tmp_path, case, monkeypatch)
    events = []
    real_fsync = os.fsync

    def recording_fsync(descriptor):
        events.append('fsync')
        return real_fsync(descriptor)

    real_percentile = part_a._percentile

    def recording_percentile(panels, probability, method):
        events.append('percentile')
        return real_percentile(panels, probability, method)

    monkeypatch.setattr(os, 'fsync', recording_fsync)
    monkeypatch.setattr(part_a, '_percentile', recording_percentile)
    worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out)
    fsyncs = [index for index, event in enumerate(events) if event == 'fsync']
    percentiles = [index for index, event in enumerate(events) if event == 'percentile']
    assert fsyncs and percentiles
    assert min(fsyncs) < min(percentiles)
    assert max(fsyncs) > max(percentiles)


@pytest.mark.parametrize('role,expected', [
    ('assessment', 'staged N2 assessment differs from the receipt binding'),
    ('payload', 'staged N2 capture payload differs from the assessment binding'),
    ('receipt', 'staged N2 assessment differs from the receipt binding'),
])
def test_part_a_refuses_tampered_staged_predecessors(tmp_path, monkeypatch, role, expected):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, payload, assessment, receipt = hand_staged_part_a(tmp_path, case, monkeypatch)
    if role == 'assessment':
        tampered = json.loads(assessment)
        tampered['capture']['payload_sha256'] = '7' * 64
        (pa / 'predecessor-assessment.json').write_bytes(encoded(tampered))
    elif role == 'payload':
        (pa / 'predecessor-payload.json').write_bytes(payload + b'\n')
    else:
        # The plan is re-derived from the tampered receipt, so the refusal is
        # the worker's own W1 custody check, not the plan equality check.
        tampered = json.loads(receipt)
        tampered['assessment_sha256'] = '6' * 64
        tampered_bytes = encoded(tampered)
        (pa / 'predecessor-receipt.json').write_bytes(tampered_bytes)
        _write_part_a_plan(pa, context, tampered_bytes)
    with pytest.raises(ValueError, match=expected):
        worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out)
    assert list(out.iterdir()) == []


def test_part_a_failing_initial_write_leaves_no_final_file(tmp_path, monkeypatch):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, payload, assessment, receipt = hand_staged_part_a(tmp_path, case, monkeypatch)

    class CustodyWriteRefused(RuntimeError):
        pass

    original = worker.write_part_a_artifact

    def refusing_writer(directory, name, raw):
        if name == 'part-a-initial.jsonl':
            raise CustodyWriteRefused('initial prefix artifact write failed')
        return original(directory, name, raw)

    monkeypatch.setattr(worker, 'write_part_a_artifact', refusing_writer)
    # The custody failure propagates: no final artifact and no frame follow it.
    with pytest.raises(CustodyWriteRefused):
        worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out)
    assert list(out.iterdir()) == []


def test_part_a_worker_requires_the_output_mount(tmp_path, monkeypatch):
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, payload, assessment, receipt = hand_staged_part_a(tmp_path, case, monkeypatch)
    with pytest.raises(ValueError, match='campaign output mount'):
        worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=None)
    assert list(out.iterdir()) == []
