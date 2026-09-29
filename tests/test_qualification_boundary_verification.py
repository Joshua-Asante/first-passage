"""Boundary wrapper must reject unsupported setups before running any tests."""
from contextlib import contextmanager
import importlib
import json
from pathlib import Path
import pytest


def runner():
    name = 'scripts.qualification_boundary_verification'
    assert importlib.util.find_spec(name), 'boundary verification wrapper is missing'
    return importlib.import_module(name)


def test_empty_or_skipped_acceptance_is_not_success():
    module = runner()
    for counts in ({'collected': 0, 'failed': 0, 'errors': 0, 'skipped': 0},
                   {'collected': 10, 'failed': 0, 'errors': 0, 'skipped': 1}):
        with pytest.raises(ValueError):
            module.require_tests(counts)


def test_partial_or_failed_report_is_rejected():
    module = runner()
    for counts in (None, {}, {'collected': 3, 'passed': 2, 'failed': 1, 'errors': 0, 'skipped': 0}):
        with pytest.raises(ValueError):
            module.require_tests(counts)


def test_nonlinux_entry_point_fails_without_provisioning(monkeypatch):
    module = runner()
    monkeypatch.setattr(module.platform, 'system', lambda: 'Windows')
    assert module.main(['--test-only']) != 0


@pytest.mark.parametrize('mode',['--host-only','--test-only','--s2'])
def test_host_cleanup_runs_after_ownership_lock_is_released(tmp_path, monkeypatch,mode):
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({
        'host_config_sha256': 'configured',
        'source': {'commit': 'candidate'},
    }))
    events = []

    @contextmanager
    def observed_lock(root):
        assert root == manifest_path.parent
        events.append('lock-enter')
        try:
            yield
        finally:
            events.append('lock-exit')

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            events.append('begin')

        def execute(self, command, **_kwargs):
            if mode=='--s2':
                # Every S2 file, in S2_CASES order (the last supervision case contaminates the host).
                positions=[command.index(case) for case in module.S2_CASES]
                assert positions==sorted(positions) and len(module.S2_CASES)>1
                assert not any(argument.startswith('--ignore=') for argument in command)
            else:
                selection='tests/integration/qualification_host' if mode=='--host-only' else 'tests/integration/qualification_boundary'
                assert selection in command
                if mode=='--test-only':
                    # The whole S5 file set (S4, S3 and S2 files included) stays out of N1_ONLY.
                    assert all('--ignore='+case in command for case in module.S5_CASES)
            if mode=='--test-only':
                assert self.data['metadata']['qualification_acceptance']=='coordinator_review_required'
            self.data['test_summary'] = {
                'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0,
            }
            self.data['verification_exit_code'] = 0

    def observed_cleanup(path):
        assert path == manifest_path
        events.append('cleanup')
        return {'ok': True}

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', lambda *args, **kwargs: {'passed': True})
    monkeypatch.setattr(module, 'ownership_lock', observed_lock)
    monkeypatch.setattr(module, 'cleanup', observed_cleanup)
    monkeypatch.setattr(module,'create_process_group',lambda root:root/'group')
    monkeypatch.setattr(module,'owned_command',lambda group,command,interpreter:command)

    assert module.main([mode, '--manifest', str(manifest_path)]) == 0
    assert events == ['lock-enter', 'begin', 'lock-exit', 'cleanup']


def test_invariant_gate_requires_actual_reports(tmp_path):
    from scripts.qualification_boundary_verification import require_invariants
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from test_qualification_invariant_manifest import manifest, NODE
    raw = json.dumps(manifest()).encode()
    collection = tmp_path / 'collected.json'
    collection.write_text(json.dumps([NODE]))
    with pytest.raises(ValueError, match='Qualification invariants'):
        require_invariants(raw, collection, tmp_path / 'missing.xml', tmp_path)
    diagnostics = json.loads((tmp_path / 'invariants.json').read_bytes())
    assert not diagnostics['passed']


@pytest.mark.parametrize('counts', [{'ok': False}, {}, {'ok': 1}])
def test_cleanup_must_be_explicitly_successful(counts):
    with pytest.raises(ValueError, match='cleanup'):
        runner().require_cleanup(counts)


@pytest.mark.parametrize('mode',['--test-only','--s2','--s3','--s4','--s5'])
def test_required_nodes_match_the_selected_file_set(tmp_path, monkeypatch, mode):
    """--test-only must never require a node of the S5 file set: those nodes skip
    there by design and are ignored by the selection, so requiring them fails the
    required boundary jobs (PR #455, aaf9646)."""
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
    seen = {}

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}, 'metadata': {}}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            pass

        def execute(self, command, **_kwargs):
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0}
            self.data['verification_exit_code'] = 0

    def observed_invariants(*_args, required_nodeids, **_kwargs):
        seen['required'] = set(required_nodeids)
        return {'passed': True}

    @contextmanager
    def lock(_root):
        yield

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', observed_invariants)
    monkeypatch.setattr(module, 'ownership_lock', lock)
    monkeypatch.setattr(module, 'cleanup', lambda path: {'ok': True})
    monkeypatch.setattr(module, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(module, 'owned_command', lambda group, command, interpreter: command)

    assert module.main([mode, '--manifest', str(manifest_path)]) == 0
    registered = module._manifest(module.INVARIANT_MANIFEST.read_bytes())
    s2 = tuple(case + '::' for case in module.S2_CASES)
    s3 = tuple(case + '::' for case in module.S3_CASES)
    s4 = tuple(case + '::' for case in module.S4_CASES)
    s5 = tuple(case + '::' for case in module.S5_CASES)
    n2 = 'tests/integration/qualification_boundary/test_campaign_n2_linux.py::'
    expected = {'--test-only': {node for node in registered if not node.startswith(s5)},
                '--s2': {node for node in registered if node.startswith(s2)},
                '--s3': {node for node in registered if node.startswith(s3)},
                '--s4': {node for node in registered if node.startswith(s4)},
                '--s5': {node for node in registered if node.startswith(s5)}}[mode]
    assert seen['required'] == expected and expected
    if mode == '--test-only':
        assert not any(node.startswith(s5) for node in seen['required'])
    if mode == '--s3':
        # --s3 keeps S3's accepted meaning on the v5 installation: no N2 node.
        assert not any(node.startswith(n2) for node in seen['required'])
    if mode == '--s4':
        # --s4 is strictly larger: at least one N2 node, and every S3 node too.
        assert any(node.startswith(n2) for node in seen['required'])
        assert all(node in seen['required'] for node in registered if node.startswith(s3))
    if mode == '--s5':
        # --s5 is strictly larger again: at least one N2 node, and every S4 node
        # too. It asserts nothing about Part A nodes: the Part A Linux file has no
        # registered nodes yet, so this stays true whether or not it exists.
        assert any(node.startswith(n2) for node in seen['required'])
        assert all(node in seen['required'] for node in registered if node.startswith(s4))


@pytest.mark.parametrize('mode',['--s3','--s4','--s5'])
def test_cases_refuses_when_the_expression_parser_is_unavailable(monkeypatch, capsys, mode):
    """G5: without pytest's -k parser the subset cannot be validated, so it is refused early."""
    import sys
    module = runner()
    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setitem(sys.modules, '_pytest.mark.expression', None)
    assert module.main([mode, '--cases', 'downtime']) == 2
    err = capsys.readouterr().err
    assert '--cases' in err and '--manifest' not in err


@pytest.mark.parametrize('mode,joint',[('--s3',False),('--s4',True)])
def test_the_executed_environment_selects_the_joint_installation_only_for_s4(
        tmp_path, monkeypatch, mode, joint):
    """--s3 must keep the v5 installation; only --s4 hands pytest the joint v6 one."""
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
    seen = {}

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}, 'metadata': {}}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            pass

        def execute(self, _command, **kwargs):
            seen['env'] = kwargs.get('env')
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0}
            self.data['verification_exit_code'] = 0

    @contextmanager
    def lock(_root):
        yield

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', lambda *args, **kwargs: {'passed': True})
    monkeypatch.setattr(module, 'ownership_lock', lock)
    monkeypatch.setattr(module, 'cleanup', lambda path: {'ok': True})
    monkeypatch.setattr(module, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(module, 'owned_command', lambda group, command, interpreter: command)
    # An inherited S4 variable must not survive a --s3 run: it selects the v6
    # installation, so the wrapper pops it rather than trusting the caller.
    monkeypatch.setenv('FP_QUALIFICATION_S4', '1')

    assert module.main([mode, '--manifest', str(manifest_path)]) == 0
    assert seen['env']['FP_QUALIFICATION_S2'] == '1' and seen['env']['FP_QUALIFICATION_S3'] == '1'
    if joint:
        assert seen['env']['FP_QUALIFICATION_S4'] == '1'
    else:
        assert 'FP_QUALIFICATION_S4' not in seen['env']


@pytest.mark.parametrize('mode,s2,s3,s4,s5', [
    ('--test-only', False, False, False, False),
    ('--s2', True, False, False, False),
    ('--s3', True, True, False, False),
    ('--s4', True, True, True, False),
    ('--s5', True, True, True, True),
])
def test_the_executed_environment_selects_the_part_a_installation_only_for_s5(
        tmp_path, monkeypatch, mode, s2, s3, s4, s5):
    """Coordinator ruling E1: --s5 hands pytest --s4's environment (S2, S3 and
    S4 set) plus FP_QUALIFICATION_S5=1, which selects the Part A /v7
    installation; every other mode pops the S5 variable rather than trusting
    the caller, exactly as --s3 pops an inherited S4."""
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
    seen = {}

    class Record:
        def __init__(self, *_args):
            self.data = {'before': {'commit': 'candidate'}, 'metadata': {}}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def begin(self):
            pass

        def execute(self, _command, **kwargs):
            seen['env'] = kwargs.get('env')
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0}
            self.data['verification_exit_code'] = 0

    @contextmanager
    def lock(_root):
        yield

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', lambda *args, **kwargs: {'passed': True})
    monkeypatch.setattr(module, 'ownership_lock', lock)
    monkeypatch.setattr(module, 'cleanup', lambda path: {'ok': True})
    monkeypatch.setattr(module, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(module, 'owned_command', lambda group, command, interpreter: command)
    # Inherited S4 and S5 variables must not survive a mode that does not
    # select those installations: the wrapper pops them.
    monkeypatch.setenv('FP_QUALIFICATION_S4', '1')
    monkeypatch.setenv('FP_QUALIFICATION_S5', '1')

    assert module.main([mode, '--manifest', str(manifest_path)]) == 0
    env = seen['env']
    for name, expected in (('FP_QUALIFICATION_S2', s2), ('FP_QUALIFICATION_S3', s3),
                           ('FP_QUALIFICATION_S4', s4), ('FP_QUALIFICATION_S5', s5)):
        if expected:
            assert env[name] == '1', (mode, name)
        else:
            assert name not in env, (mode, name)


def test_s5_selection_places_the_part_a_file_immediately_before_the_oom_case(
        tmp_path, monkeypatch):
    """--s5 runs the S5 file set in S5_CASES order, so the Part A file sits
    immediately before the supervision file whose OOM case still runs last, and
    the record is scoped S5_PART_A rather than any S4 acceptance scope."""
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir()
    manifest_path.write_text(json.dumps({'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
    seen = {}

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

        def execute(self, command, **_kwargs):
            seen['command'] = list(command)
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0, 'errors': 0, 'skipped': 0}
            self.data['verification_exit_code'] = 0

    @contextmanager
    def lock(_root):
        yield

    monkeypatch.setattr(module.platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(module.os, 'geteuid', lambda: 0, raising=False)
    monkeypatch.setattr(module, 'protected', lambda path: path)
    monkeypatch.setattr(module, 'RunRecord', Record)
    monkeypatch.setattr(module, 'require_invariants', lambda *args, **kwargs: {'passed': True})
    monkeypatch.setattr(module, 'ownership_lock', lock)
    monkeypatch.setattr(module, 'cleanup', lambda path: {'ok': True})
    monkeypatch.setattr(module, 'create_process_group', lambda root: root / 'group')
    monkeypatch.setattr(module, 'owned_command', lambda group, command, interpreter: command)

    assert module.main(['--s5', '--manifest', str(manifest_path)]) == 0
    command = seen['command']
    part_a = 'tests/integration/qualification_boundary/test_campaign_part_a_linux.py'
    # The S5 set is the S4 set with the Part A file inserted immediately before
    # its last (supervision/OOM) file, exactly as s2_run_evidence.py builds it.
    assert module.S5_CASES == (*module.S4_CASES[:-1], part_a, module.S4_CASES[-1])
    positions = [command.index(case) for case in module.S5_CASES]
    assert positions == sorted(positions) and len(module.S5_CASES) > 1
    assert command.index(part_a) == command.index(module.S4_CASES[-1]) - 1
    assert command.index(module.S4_CASES[-1]) == max(positions)
    assert not any(argument.startswith('--ignore=') for argument in command)
    metadata = seen['record'].data['metadata']
    assert metadata['acceptance_scope'] == 'S5_PART_A'
    assert metadata['qualification_acceptance'] == 'coordinator_review_required'
