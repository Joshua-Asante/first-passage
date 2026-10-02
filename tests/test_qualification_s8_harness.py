"""S8 harness extensions: E01-E12 registration, the coverage map and --s8 selection.

Report and argument fixtures only; real campaigns run on the disposable host.
"""
from contextlib import contextmanager
import json
from pathlib import Path

import pytest

from scripts import check_qualification_invariants as checker
from scripts import qualification_boundary_verification as boundary

CANONICAL = Path(__file__).parent / 'ops/qualification/invariant_manifest.json'
FULL = boundary.FULL_CAMPAIGN_CASE


def e_rows(nodes=None):
    identities = sorted(checker.E_CASE_IDS)
    nodes = nodes or {identity: [f'{FULL}::test_{identity.lower()}'] for identity in identities}
    return [{'id': identity, 'requirement': 'E-case observation', 'owner': 'S8',
             'producer': 'installed route', 'consumer': 'service stores',
             'test_nodeids': list(nodes[identity]), 'evidence_kind': 'Linux JUnit'}
            for identity in identities]


def registered(rows=None):
    extension = e_rows() if rows is None else rows
    return json.dumps(json.loads(CANONICAL.read_bytes()) + extension).encode()


def test_canonical_manifest_is_unchanged_and_unregistered():
    assert not checker.registered_e_cases(CANONICAL.read_bytes())


def test_complete_e_registration_extends_the_one_manifest():
    required = checker._manifest(registered())
    assert checker.registered_e_cases(registered())
    assert required[f'{FULL}::test_e01'] == {'E01'}
    assert checker._manifest(CANONICAL.read_bytes()).items() <= required.items()


@pytest.mark.parametrize('drop', ['E01', 'E12'])
def test_partial_e_registration_refuses(drop):
    rows = [row for row in e_rows() if row['id'] != drop]
    with pytest.raises(ValueError, match='partial E01-E12 registration'):
        checker._manifest(registered(rows))


def test_unknown_e_identity_refuses():
    rows = e_rows()
    rows[0]['id'] = 'E13'
    with pytest.raises(ValueError, match='unknown or duplicate'):
        checker._manifest(registered(rows))


def test_registered_e_node_is_critical_like_any_invariant(tmp_path):
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from test_qualification_invariant_manifest import case, report
    node = f'{FULL}::test_e01'
    classname = FULL[:-3].replace('/', '.')
    passing = [case(name=node.split('::')[1], classname=classname)]
    skipped = [case(name=node.split('::')[1], classname=classname, outcome='skipped')]
    for cases, passed in ((passing, True), (skipped, False)):
        result = checker.validate_manifest(registered(), collected_nodeids={node},
            junit_paths=(report(tmp_path, f'{passed}.xml', cases),), evidence_root=tmp_path,
            required_nodeids={node})
        assert result['passed'] is passed, result


def test_coverage_map_maps_each_e_case_to_one_row():
    owner = checker.validate_coverage_map(e_rows(), collected_nodeids={f'{FULL}::test_{i.lower()}'
                                                                       for i in checker.E_CASE_IDS})
    assert sorted(owner.values()) == sorted(checker.E_CASE_IDS)


@pytest.mark.parametrize('kind', ['missing', 'duplicate', 'shared_node', 'wildcard', 'extra_field',
                                  'uncollected', 'collection_list'])
def test_coverage_map_refuses_ambiguity(kind):
    rows = e_rows()
    collected = {node for row in rows for node in row['test_nodeids']}
    if kind == 'missing':
        rows.pop()
    if kind == 'duplicate':
        rows.append(dict(rows[0]))
    if kind == 'shared_node':
        rows[1]['test_nodeids'] = list(rows[0]['test_nodeids'])
    if kind == 'wildcard':
        rows[0]['test_nodeids'] = [f'{FULL}::test_*']
    if kind == 'extra_field':
        rows[0]['optional'] = True
    if kind == 'uncollected':
        collected.discard(rows[0]['test_nodeids'][0])
    if kind == 'collection_list':
        collected = sorted(collected)
    with pytest.raises(ValueError):
        checker.validate_coverage_map(rows, collected_nodeids=collected)


def test_s8_set_is_s5_plus_the_full_campaign_file_before_the_oom_case():
    assert boundary.S8_CASES == (*boundary.S5_CASES[:-1], FULL, boundary.S5_CASES[-1])
    assert set(boundary.S5_CASES) < set(boundary.S8_CASES)


def test_s8_acceptance_refuses_before_any_host_prerequisite_while_unregistered(capsys):
    assert boundary.main(['--s8']) == 2
    err = capsys.readouterr().err
    assert 'E01-E12 registered' in err and 'Linux' not in err and '--manifest' not in err


def run(tmp_path, monkeypatch, argv, manifest_bytes=None):
    seen = {}
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({'host_config_sha256': 'configured',
                                         'source': {'commit': 'candidate'}}))
    if manifest_bytes is not None:
        invariant = tmp_path / 'invariant_manifest.json'
        invariant.write_bytes(manifest_bytes)
        monkeypatch.setattr(boundary, 'INVARIANT_MANIFEST', invariant)

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}, 'metadata': {}}
            seen['record'] = self

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            pass

        def execute(self, command, **kwargs):
            seen.update(command=list(command), env=kwargs.get('env'))
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0,
                                         'skipped': 0}
            self.data['verification_exit_code'] = 0

    def invariants(*_args, required_nodeids, **_kwargs):
        seen['required'] = set(required_nodeids)
        return {'passed': True}

    @contextmanager
    def lock(_root):
        yield

    monkeypatch.setattr(boundary.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(boundary.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(boundary, 'protected', lambda path: path)
    monkeypatch.setattr(boundary, 'RunRecord', Record)
    monkeypatch.setattr(boundary, 'require_invariants', invariants)
    monkeypatch.setattr(boundary, 'ownership_lock', lock)
    monkeypatch.setattr(boundary, 'cleanup', lambda path: {'ok': True})
    monkeypatch.setattr(boundary, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(boundary, 'owned_command', lambda group, command, interpreter: command)
    seen['code'] = boundary.main([*argv, '--manifest', str(manifest_path)])
    return seen


def test_registered_s8_runs_the_s8_set_in_order_on_the_integrated_environment(tmp_path,
                                                                             monkeypatch):
    raw = registered()
    seen = run(tmp_path, monkeypatch, ['--s8'], raw)
    assert seen['code'] == 0
    command = seen['command']
    positions = [command.index(case) for case in boundary.S8_CASES]
    assert positions == sorted(positions) and command.index(boundary.S8_CASES[-1]) == max(positions)
    assert command.index(FULL) == command.index(boundary.S8_CASES[-1]) - 1
    assert not any(argument.startswith('--ignore=') for argument in command)
    for stage in ('S2', 'S3', 'S4', 'S5', 'S8'):
        assert seen['env']['FP_QUALIFICATION_' + stage] == '1', stage
    prefixes = tuple(case + '::' for case in boundary.S8_CASES)
    expected = {node for node in checker._manifest(raw) if node.startswith(prefixes)}
    assert seen['required'] == expected
    assert {f'{FULL}::test_{i.lower()}' for i in checker.E_CASE_IDS} <= seen['required']
    assert seen['record'].data['metadata']['acceptance_scope'] == 'S8_FULL_E1'


def test_s8_diagnostic_subset_needs_no_registration_and_is_never_acceptance(tmp_path, monkeypatch):
    seen = run(tmp_path, monkeypatch, ['--s8', '--cases', 'e01'])
    assert seen['code'] == 2
    assert seen['command'][3:5] == ['-k', 'e01'] and FULL in seen['command']
    assert seen['record'].data['metadata']['acceptance_scope'] == 'DIAGNOSTIC_SUBSET'


@pytest.mark.parametrize('mode', ['--test-only', '--s5'])
def test_earlier_modes_never_select_or_require_the_full_campaign_file(tmp_path, monkeypatch, mode):
    monkeypatch.setenv('FP_QUALIFICATION_S8', '1')
    raw = registered()
    seen = run(tmp_path, monkeypatch, [mode], raw)
    assert seen['code'] == 0 and 'FP_QUALIFICATION_S8' not in seen['env']
    assert not any(node.startswith(FULL + '::') for node in seen['required'])
    if mode == '--test-only':
        assert '--ignore=' + FULL in seen['command']
        assert all('--ignore=' + case in seen['command'] for case in boundary.S8_CASES)
    else:
        assert FULL not in seen['command']
