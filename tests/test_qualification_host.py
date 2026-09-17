"""Host input/ownership validation must fail before making privileged changes."""
import hashlib
import importlib
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]


def host_module():
    name = 'tools.qualification_verification.host'
    assert importlib.util.find_spec(name), 'host provisioning is missing'
    return importlib.import_module(name)


def test_changed_lock_is_rejected_before_provisioning(tmp_path):
    host = host_module()
    (tmp_path / 'requirements-ops.lock').write_text('tampered')
    with pytest.raises(ValueError, match='lock'):
        host.validate_inputs(tmp_path, host.load_config())


def test_host_config_matches_committed_lock_bytes():
    host = host_module()
    host.validate_inputs(ROOT, host.load_config())


@pytest.mark.parametrize('relative', ['../outside', '/etc/passwd', 'data/../../outside', '.', ''])
def test_cleanup_manifest_cannot_name_escape_or_root(tmp_path, relative):
    host = host_module()
    with pytest.raises(ValueError):
        host.resource_path(tmp_path, relative)


def test_cleanup_manifest_rejects_unknown_resource_kind(tmp_path):
    host = host_module()
    with pytest.raises(ValueError, match='resource'):
        host.validate_resources({'resources': [{'kind': 'shell', 'command': 'anything'}]}, tmp_path)


def test_cleanup_manifest_rejects_duplicate_resources(tmp_path):
    host = host_module()
    with pytest.raises(ValueError, match='duplicate'):
        host.validate_resources({'resources': [
            {'kind': 'tree', 'path': 'data', 'uid': 61001},
            {'kind': 'tree', 'path': 'data', 'uid': 61001}]}, tmp_path)


def test_cleanup_tree_refuses_link_without_removing_target(tmp_path):
    host = host_module()
    target = tmp_path / 'sentinel'
    target.write_text('keep')
    tree = tmp_path / 'data'
    tree.mkdir()
    try:
        (tree / 'alias').symlink_to(target)
    except OSError:
        pytest.skip('symlink creation unavailable on this development host')
    with pytest.raises(ValueError, match='link'):
        host.inspect_tree(tree)
    assert target.read_text() == 'keep'


def test_public_observations_exclude_private_manifest_fields():
    host = host_module()
    manifest = {'run_id': 'a' * 32, 'host_config_sha256': 'b' * 64,
                'facts': {'python': '3.12.3', 'docker': {'Version': '28.0.4'}},
                'runtime': {'packages': [['cryptography', '50.0.1']]},
                'roles': {'qclient': 61000, 'qexec': 61001, 'qg5': 61002},
                'source': {'commit': 'c' * 40, 'fingerprint': 'd' * 64},
                'resources': [{'path': '/private/TEST_ONLY.key'}],
                'private_future_field': 'do not export'}
    assert hasattr(host, 'public_observations'), 'non-secret host inventory export is missing'
    report = host.public_observations(manifest)
    assert report['runtime']['packages'] == [['cryptography', '50.0.1']]
    assert report['facts']['docker']['Version'] == '28.0.4'
    assert 'resources' not in report and 'private_future_field' not in report


def test_cleanup_accepts_resolved_nondefault_identity_ids(tmp_path):
    host = host_module()
    config = {**host.load_config(), 'uid_start': 62000}
    manifest = {'host_config': config, 'roles': {'qclient': 62000, 'qexec': 62001, 'qg5': 62002},
                'resources': [{'kind': 'user', 'name': 'qexec', 'id': 62001},
                              {'kind': 'group', 'name': 'qexec', 'id': 62001}]}
    host.validate_resources(manifest, tmp_path)


def test_cleanup_rejects_role_id_swap_even_within_range(tmp_path):
    host = host_module()
    manifest = {'host_config': host.load_config(),
                'roles': {'qclient': 61000, 'qexec': 61001, 'qg5': 61002},
                'resources': [{'kind': 'user', 'name': 'qclient', 'id': 61001}]}
    with pytest.raises(ValueError, match='identity'):
        host.validate_resources(manifest, tmp_path)


def test_reservation_prevents_claiming_an_interrupted_runs_groups(tmp_path):
    host = host_module()
    assert hasattr(host, 'require_available_reservation'), 'shared durable reservation is missing'
    reservation = tmp_path / 'reservation.json'
    reservation.write_text(json.dumps({'schema': 'qualification_identity_reservation/v1',
                                       'owner': {'run_id': 'first', 'manifest': '/first/ownership.json'}}))
    with pytest.raises(ValueError, match='reserved'):
        host.require_available_reservation(reservation)


def test_old_manifest_cannot_retire_another_runs_identities(tmp_path):
    host = host_module()
    assert hasattr(host, 'require_reservation_owner'), 'reservation owner validation is missing'
    reservation = tmp_path / 'reservation.json'
    reservation.write_text(json.dumps({'schema': 'qualification_identity_reservation/v1',
                                       'owner': {'run_id': 'new', 'manifest': '/new/ownership.json'}}))
    with pytest.raises(ValueError, match='reservation owner'):
        host.require_reservation_owner(reservation, tmp_path / 'ownership.json',
                                       {'run_id': 'old', 'resources': [{'kind': 'group'}]})
