"""Boundary wrapper must reject unsupported setups before running any tests."""
from contextlib import contextmanager
import hashlib
import importlib
import json
from pathlib import Path
import pytest
import sys


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


# --- R1: the H9 checkpoint combined selection (ruling 5's broaden-R1 order) ----

BOUNDARY_DIR = 'tests/integration/qualification_boundary/'
RESULT_SEAL_FILE = BOUNDARY_DIR + 'test_campaign_result_seal_linux.py'
CPRIME_FILE = BOUNDARY_DIR + 'test_runtime_identity_linux.py'
# The R1 file set spelled from the seven fixed paths (card §2) rather than read
# off the selector, so the R4 falsifier can build its fixture tree and assert
# against a base selector that has no R1_CASES at all: it fails there on the
# ignore assertion itself, and the closing equality pin keeps this spelling and
# the selector's own tuple in step on the branch head.
R1_FILES = (BOUNDARY_DIR + 'test_campaign_service_linux.py',
            BOUNDARY_DIR + 'test_campaign_n1_linux.py',
            BOUNDARY_DIR + 'test_campaign_n2_linux.py',
            BOUNDARY_DIR + 'test_campaign_part_a_linux.py',
            RESULT_SEAL_FILE, CPRIME_FILE,
            BOUNDARY_DIR + 'test_campaign_supervision_linux.py')


def invariant_manifest_document(nodes):
    """One closed, valid manifest whose only registered nodes are `nodes`."""
    sys.path.insert(0, str(Path(__file__).parent))
    from test_qualification_invariant_manifest import manifest
    return manifest(tuple(nodes))


def r1_tree(tmp_path, monkeypatch, *, present=None, rows=None, files=None):
    """Point the selector at a throwaway tree holding a complete R1 selection.

    Every file of `files` (the selector's R1_CASES by default) exists and
    contributes one registered node, so a full `--r1` passes its own
    prerequisite check; `present` drops files from the tree and `rows` drops
    their manifest rows, which is exactly how the two refusal limbs are forged.
    """
    module = runner()
    files = tuple(module.R1_CASES) if files is None else tuple(files)
    present = files if present is None else tuple(present)
    for case in dict.fromkeys((*files, *present)):
        path = tmp_path / case
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('# TEST_ONLY linux boundary file\n', encoding='utf-8')
    for case in files:
        if case not in present:
            (tmp_path / case).unlink()
    nodes = (rows if rows is not None
             else [case + '::test_case' for case in present])
    manifest_path = tmp_path / 'invariant_manifest.json'
    manifest_path.write_text(json.dumps(invariant_manifest_document(nodes)), encoding='utf-8')
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr(module, 'INVARIANT_MANIFEST', manifest_path)
    return module, set(nodes), manifest_path


def linux_harness(module, tmp_path, monkeypatch):
    """Patch every host seam; return the dict the run fills in."""
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir(exist_ok=True)
    manifest_path.write_text(json.dumps(
        {'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
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

        def execute(self, command, **kwargs):
            seen['command'] = list(command)
            seen['env'] = kwargs.get('env')
            self.data['test_summary'] = {'collected': 1, 'passed': 1, 'failed': 0,
                                         'errors': 0, 'skipped': 0}
            self.data['verification_exit_code'] = 0

    def observed_invariants(*_args, required_nodeids=None, **_kwargs):
        seen['required'] = set(required_nodeids or ())
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
    return seen


def test_r1_is_a_mode_that_reaches_the_host_prerequisite(tmp_path, monkeypatch, capsys):
    """R1 (falsifier-first): `--r1` is a real mode whose own prerequisite passes
    on a complete tree, so the host prerequisite is what stops it. On the base
    commit argparse refuses `--r1` (unrecognized argument, exit 2), which is the
    falsifier; the tree is spelled (R1_FILES) so the base failure is that."""
    module, _registered, _manifest = r1_tree(tmp_path, monkeypatch, files=R1_FILES)
    monkeypatch.setattr(module.platform, 'system', lambda: 'Windows')
    assert module.main(['--r1']) == 2
    err = capsys.readouterr().err
    assert 'usage:' not in err and 'unrecognized arguments' not in err
    assert 'Linux administrator' in err


def test_r1_cases_is_the_seven_file_set_supervision_last():
    """G1: the card §2 order -- service, N1, N2, Part A, result/seal, C', then
    supervision last (D1 places C' immediately before it), a strict superset of
    the S5 set that preserves S5's own order."""
    module = runner()
    boundary = 'tests/integration/qualification_boundary/'
    assert module.RESULT_SEAL_CASE == boundary + 'test_campaign_result_seal_linux.py'
    assert module.CPRIME_CASE == boundary + 'test_runtime_identity_linux.py'
    assert module.R1_CASES == (*module.S5_CASES[:-1], module.RESULT_SEAL_CASE,
                               module.CPRIME_CASE, module.S5_CASES[-1])
    assert module.R1_CASES == (boundary + 'test_campaign_service_linux.py',
                               boundary + 'test_campaign_n1_linux.py',
                               boundary + 'test_campaign_n2_linux.py',
                               module.PART_A_CASE,
                               module.RESULT_SEAL_CASE,
                               module.CPRIME_CASE,
                               boundary + 'test_campaign_supervision_linux.py')
    # A strict superset of the S5 set, preserving S5's order, supervision last.
    assert len(set(module.R1_CASES)) == len(module.R1_CASES) == len(module.S5_CASES) + 2
    assert set(module.S5_CASES) < set(module.R1_CASES)
    assert tuple(case for case in module.R1_CASES if case in module.S5_CASES) == module.S5_CASES
    assert module.R1_CASES[-1] == module.S5_CASES[-1] == module.S4_CASES[-1] == module.S2_CASES[-1]
    # No node ID is hard-coded anywhere near the tuple.
    assert not any('::' in case for case in module.R1_CASES)


def test_r1_requires_exactly_the_registered_nodes_inside_r1_cases(tmp_path, monkeypatch):
    """G2: `--r1` requires the registered nodes of R1_CASES and no other, and
    records the R1 scope with the same acceptance framing as --s5."""
    module, registered, manifest_path = r1_tree(tmp_path, monkeypatch)
    seen = linux_harness(module, tmp_path, monkeypatch)
    assert module.main(['--r1', '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 0
    r1 = tuple(case + '::' for case in module.R1_CASES)
    assert seen['required'] == {node for node in registered if node.startswith(r1)}
    assert len(seen['required']) == len(module.R1_CASES)
    metadata = seen['record'].data['metadata']
    assert metadata['acceptance_scope'] == 'T05_R1_COMBINED'
    assert metadata['qualification_acceptance'] == 'coordinator_review_required'
    assert metadata['invariant_manifest_sha256'] == hashlib.sha256(
        manifest_path.read_bytes()).hexdigest()


def test_r1_runs_the_r1_files_in_order_supervision_last(tmp_path, monkeypatch):
    """G2: the selection runs every R1 file in R1_CASES order, so result/seal
    and C' sit immediately before the supervision file whose OOM case runs
    last, and nothing is ignored."""
    module, _registered, _manifest = r1_tree(tmp_path, monkeypatch)
    seen = linux_harness(module, tmp_path, monkeypatch)
    assert module.main(['--r1', '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 0
    command = seen['command']
    positions = [command.index(case) for case in module.R1_CASES]
    assert positions == sorted(positions) and len(module.R1_CASES) > 1
    assert command.index(module.CPRIME_CASE) == command.index(module.R1_CASES[-1]) - 1
    assert command.index(module.RESULT_SEAL_CASE) == command.index(module.CPRIME_CASE) - 1
    assert command.index(module.R1_CASES[-1]) == max(positions)
    assert not any(argument.startswith('--ignore=') for argument in command)
    assert '-k' not in command


@pytest.mark.parametrize('mode,r1', [
    ('--test-only', False), ('--s2', False), ('--s3', False), ('--s4', False),
    ('--s5', False), ('--r1', True),
])
def test_only_r1_sets_the_r1_installation_variable(tmp_path, monkeypatch, mode, r1):
    """G2: `--r1` hands pytest the whole --s5 environment (S2, S3, S4 and S5
    set) plus FP_QUALIFICATION_R1, the seam H9's fixture reads; every other
    mode pops the R1 variable rather than trusting the caller."""
    module, _registered, _manifest = r1_tree(tmp_path, monkeypatch)
    seen = linux_harness(module, tmp_path, monkeypatch)
    monkeypatch.setenv('FP_QUALIFICATION_R1', '1')
    assert module.main([mode, '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 0
    env = seen['env']
    if r1:
        assert env['FP_QUALIFICATION_R1'] == '1'
        for name in ('FP_QUALIFICATION_S2', 'FP_QUALIFICATION_S3',
                     'FP_QUALIFICATION_S4', 'FP_QUALIFICATION_S5'):
            assert env[name] == '1', name
    else:
        assert 'FP_QUALIFICATION_R1' not in env


def test_r1_accepts_cases_as_a_diagnostic_subset_that_can_never_be_evidence(
        tmp_path, monkeypatch):
    """G3: `--cases` is accepted with `--r1`; the record is scoped
    DIAGNOSTIC_SUBSET and the run exits non-zero."""
    module, _registered, _manifest = r1_tree(tmp_path, monkeypatch)
    seen = linux_harness(module, tmp_path, monkeypatch)
    assert module.main(['--r1', '--cases=downtime',
                        '--manifest', str(tmp_path / 'run' / 'ownership.json')]) != 0
    metadata = seen['record'].data['metadata']
    assert metadata['acceptance_scope'] == 'DIAGNOSTIC_SUBSET'
    assert metadata['diagnostic_expression'] == 'downtime'


def test_a_full_r1_refuses_in_seconds_when_an_r1_file_is_absent(tmp_path, monkeypatch, capsys):
    """G4: the refusal runs before the Linux/root check, so it costs nothing and
    works from Windows; the message names the missing file."""
    module, _registered, _manifest = r1_tree(
        tmp_path, monkeypatch,
        present=[case for case in runner().R1_CASES if case != runner().RESULT_SEAL_CASE])
    assert module.main(['--r1', '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 2
    err = capsys.readouterr().err
    assert 'Failed prerequisite' in err
    assert module.RESULT_SEAL_CASE in err and 'absent from the tree' in err
    assert 'Linux administrator' not in err and 'Failed setup' not in err


def test_a_full_r1_refuses_when_an_r1_file_has_no_registered_node(
        tmp_path, monkeypatch, capsys):
    """G4: a present file with zero manifest rows is as incomplete as a missing
    one, and both are named."""
    module = runner()
    rows = [case + '::test_case' for case in module.R1_CASES if case != module.CPRIME_CASE]
    module, _registered, _manifest = r1_tree(tmp_path, monkeypatch, rows=rows)
    assert module.main(['--r1', '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 2
    err = capsys.readouterr().err
    assert 'Failed prerequisite' in err
    assert module.CPRIME_CASE in err and 'no registered node' in err
    # File 5 exists on this tree and carries a row, so it is not named at all.
    assert module.RESULT_SEAL_CASE not in err
    assert 'absent from the tree' not in err


def test_a_full_r1_refuses_naming_every_incomplete_file_at_once(tmp_path, monkeypatch, capsys):
    module = runner()
    module, _registered, _manifest = r1_tree(
        tmp_path, monkeypatch,
        present=[module.R1_CASES[0]],
        rows=[module.R1_CASES[0] + '::test_case'])
    assert module.main(['--r1', '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 2
    err = capsys.readouterr().err
    for case in module.R1_CASES[1:]:
        assert case in err, case
    assert err.count('absent from the tree') == len(module.R1_CASES) - 1


def test_a_full_r1_on_the_real_tree_refuses_naming_files_5_and_6(capsys):
    """G4: on the base tree neither the result/seal file (H9) nor the C' file is
    present, so a full `--r1` refuses in seconds naming both."""
    module = runner()
    assert module.main(['--r1', '--manifest', 'unused']) == 2
    err = capsys.readouterr().err
    assert 'Failed prerequisite' in err
    assert module.RESULT_SEAL_CASE in err and module.CPRIME_CASE in err
    assert err.count('absent from the tree') == 2


def test_every_other_mode_leaves_the_r1_prerequisite_alone(tmp_path, monkeypatch, capsys):
    """G4: `r1_refusal` is scoped to `--r1`; the other modes never consult the
    R1 file set, and a tree without file 5 does not disturb them."""
    module = runner()
    manifest_path = tmp_path / 'run' / 'ownership.json'
    manifest_path.parent.mkdir(exist_ok=True)
    manifest_path.write_text(json.dumps(
        {'host_config_sha256': 'configured', 'source': {'commit': 'candidate'}}))
    monkeypatch.setattr(module.platform, 'system', lambda: 'Windows')
    for mode in ('--test-only', '--s2', '--s3', '--s4', '--s5'):
        assert module.main([mode, '--manifest', str(manifest_path)]) == 2
        err = capsys.readouterr().err
        assert 'Linux administrator' in err
        assert module.RESULT_SEAL_CASE not in err and 'R1 selection' not in err


def test_test_only_ignores_every_r1_file_including_files_5_and_6(tmp_path, monkeypatch):
    """G5 (falsifier-first R4): N1_ONLY must stay green once H9 lands file 5 and
    the C' build lands file 6, so `--test-only` excludes the whole R1 file set —
    a strict superset of the S5 set it excluded before. The tree and the
    assertions spell the file set out (R1_FILES), so on the base commit the
    failure is the falsifier itself: file 5 sits in the tree and is run."""
    module, _registered, _manifest = r1_tree(tmp_path, monkeypatch, files=R1_FILES)
    seen = linux_harness(module, tmp_path, monkeypatch)
    assert module.main(['--test-only',
                        '--manifest', str(tmp_path / 'run' / 'ownership.json')]) == 0
    ignored = [argument for argument in seen['command'] if argument.startswith('--ignore=')]
    for case in R1_FILES:
        assert '--ignore=' + case in ignored, case
    assert '--ignore=' + RESULT_SEAL_FILE in ignored
    assert '--ignore=' + CPRIME_FILE in ignored
    assert not any(node.startswith(case + '::') for case in R1_FILES
                   for node in seen['required'])
    # The spelled set the fixture used is exactly the selector's own tuple.
    assert module.R1_CASES == R1_FILES

