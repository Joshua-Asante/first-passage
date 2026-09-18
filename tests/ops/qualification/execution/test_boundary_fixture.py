"""Actual signed fixture assembly, without any OS execution acceptance claim."""
from datetime import datetime,timezone
import importlib.util
from pathlib import Path
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.source_admission import admit_source
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from test_profile import document
import pytest

ROOT=Path(__file__).resolve().parents[4]


def test_real_fixture_binds_current_signed_policy_and_actual_role_closures(tmp_path):
    spec=importlib.util.spec_from_file_location('qualification_boundary_fixture',
        ROOT/'tests/integration/qualification_boundary/fixture_producer.py')
    fixture=importlib.util.module_from_spec(spec); spec.loader.exec_module(fixture)
    private,keys,_=fixture.fresh_keys(execution_seed=b'a'*32,result_seed=b'b'*32)
    release=encoded(fixture.release_document(ROOT,document(),'sha256:'+'c'*64,keys))
    bundle=fixture.build_real_bundle(tmp_path/'retained',repo=ROOT,release=release,private=private,keys=keys,
        attempt_id='fixture-current',idle=True)
    context=verify_bundle(bundle['root'],release,keys,datetime.now(timezone.utc))
    assert context.contract.policy_sha256==context.policy.sha256
    assert context.attempt_id=='fixture-current'
    assert context.release.document['runtime_manifests']['worker']!=context.release.document['runtime_manifests']['g5']
    admit_source(context.contract,artifact_root=context.bundle_dir,policy=context.policy)


@pytest.mark.parametrize('fault',['stop','exit_zero','cpu','memory','wall'])
def test_fault_fixture_is_signed_and_admitted_before_actual_worker_failure(tmp_path,fault):
    spec=importlib.util.spec_from_file_location('qualification_fault_fixture',
        ROOT/'tests/integration/qualification_boundary/fixture_producer.py')
    fixture=importlib.util.module_from_spec(spec); spec.loader.exec_module(fixture)
    private,keys,_=fixture.fresh_keys()
    release=encoded(fixture.release_document(ROOT,document(),'sha256:'+'c'*64,keys))
    bundle=fixture.build_real_bundle(tmp_path/'retained',repo=ROOT,release=release,private=private,keys=keys,
        attempt_id='fixture-fault',idle=True,fault=fault,depth_valid_seconds=90)
    context=verify_bundle(bundle['root'],release,keys,datetime.now(timezone.utc))
    assert context.attempt_id=='fixture-fault'
    assert (context.exact_depth_approval.expires_at-context.exact_depth_approval.issued_at).total_seconds()==390
    # Admission builds the real retained source, but never calls on_bar: the
    # destructive fault must remain dormant until the protected worker replays.
    admitted=admit_source(context.contract,artifact_root=context.bundle_dir,policy=context.policy)
    admitted.source.verify_for(context.contract)
