import hashlib
import json
from types import SimpleNamespace

import pytest

from c1_signal_daemon.book_adapters import _qualification_snapshots


def fixture():
    settings = {'_note': 'synthetic fixture'}
    legs = ('aegis_6j', 'dj30_mym_p250', 'vanguard_mgc', 'orb_mnq_v7')
    for leg in legs:
        settings[leg] = {'adapter': {'qty': 1} if leg == 'orb_mnq_v7' else {}, 'emulator': {}, 'qty_scale': 1}
    raw = json.dumps(settings).encode()
    digest = hashlib.sha256(raw).hexdigest()
    row = SimpleNamespace(role='effective_settings_successor', path='inputs/settings.json', sha256=digest)
    contract = SimpleNamespace(artifacts=(row,), runtime_load_sha256={row.role: digest}, effective_settings_sha256=digest)
    return contract, {row.path: raw}


def test_verified_settings_snapshot_is_parsed_without_a_second_file_read():
    contract, retained = fixture()
    snapshots, settings, trace = _qualification_snapshots(contract, retained)
    assert settings['orb_mnq_v7']['adapter']['qty'] == 1
    assert snapshots['effective_settings_successor'] is retained['inputs/settings.json']
    assert trace == (('effective_settings_successor', 'inputs/settings.json', contract.effective_settings_sha256),)


def test_wrong_digest_extra_inventory_or_legacy_orb_qty_refuses():
    contract, retained = fixture()
    with pytest.raises(ValueError, match='digest'):
        _qualification_snapshots(contract, {'inputs/settings.json': b'changed'})
    with pytest.raises(ValueError, match='inventory'):
        _qualification_snapshots(contract, retained | {'extra': b''})
    data = json.loads(retained['inputs/settings.json'])
    data['orb_mnq_v7']['adapter']['qty'] = 2
    raw = json.dumps(data).encode()
    digest = hashlib.sha256(raw).hexdigest()
    contract.artifacts[0].sha256 = digest
    contract.runtime_load_sha256['effective_settings_successor'] = digest
    contract.effective_settings_sha256 = digest
    with pytest.raises(ValueError, match='ORB'):
        _qualification_snapshots(contract, {'inputs/settings.json': raw})


def test_duplicate_json_settings_keys_refuse_even_with_matching_digest():
    contract, retained = fixture()
    raw = retained['inputs/settings.json'].replace(b'"qty": 1', b'"qty": 2, "qty": 1')
    digest = hashlib.sha256(raw).hexdigest()
    contract.artifacts[0].sha256 = digest
    contract.runtime_load_sha256['effective_settings_successor'] = digest
    contract.effective_settings_sha256 = digest
    with pytest.raises(ValueError, match='duplicate'):
        _qualification_snapshots(contract, {'inputs/settings.json': raw})


def test_public_loader_requires_exact_g1_type_and_refuses_before_port_execution(tmp_path):
    from c1_signal_daemon.book_adapters import load_qualification_adapters
    contract, retained = fixture()
    with pytest.raises(ValueError, match='G1'):
        load_qualification_adapters(contract, retained_bytes=retained)


def test_qualification_loader_compiles_verified_snapshots_not_disk_or_pyc(tmp_path):
    from composition_fixture import build_verified_composition, PORT_ROLES
    from c1_signal_daemon.book_adapters import _load_composition_adapters
    verified=build_verified_composition(tmp_path)
    retained=dict(verified.source.prepared.retained_bytes)
    for role in PORT_ROLES.values():
        (tmp_path/verified.fixture.paths[role]).write_text("raise AssertionError('disk bytes executed')")
    loaded=_load_composition_adapters(verified.contract,retained_bytes=retained)
    assert loaded.registry.kind=='synthetic'
    assert set(loaded.registry)==set(PORT_ROLES)
    assert loaded.registry['orb_mnq_v7'].params.qty==1
    role=PORT_ROLES['orb_mnq_v7']
    changed=retained|{verified.fixture.paths[role]:b"raise AssertionError('unverified executed')"}
    with pytest.raises(ValueError,match='digest'):
        _load_composition_adapters(verified.contract,retained_bytes=changed)
