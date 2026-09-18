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
