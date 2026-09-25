"""S2 campaign-host enrollment: manager call carries real properties only; slice limit/swap verified once realized.

The first real --s2 run (2026-09-19, Actions 35453843198) failed inside
StartTransientUnit because the call named MemoryOOMGroup, which systemd does
not define; the manager rejects the whole call. These tests are diagnostic
(fake manager, fake cgroup tree) and claim nothing about Linux enforcement.
"""
import json
import subprocess

import pytest

from tools.qualification_verification import campaign_host

ROOT_ID = 'a' * 32


def _fake_host(monkeypatch, tmp_path, run):
    saved = {}
    monkeypatch.setattr(campaign_host.host, 'administrator', lambda: None)
    monkeypatch.setattr(campaign_host.host, 'protected', lambda path: path)
    monkeypatch.setattr(campaign_host.host, 'save', lambda path, data, **kw: saved.setdefault(str(path), data))
    monkeypatch.setattr(campaign_host.host, 'run', run)
    (tmp_path / 'rules.d').mkdir()
    (tmp_path / 'cgroup').mkdir()
    monkeypatch.setattr(campaign_host, 'POLKIT_RULES', tmp_path / 'rules.d')
    monkeypatch.setattr(campaign_host, 'CGROUP_ROOT', tmp_path / 'cgroup')
    monkeypatch.setattr(campaign_host, 'SLICE_REALIZE_SECONDS', 0.2)
    root = tmp_path / ROOT_ID
    root.mkdir()
    return saved, root


def _realizing_manager(tmp_path, calls, *, memory_max='256000000'):
    def run(command):
        calls.append(command)
        scope = command[command.index('ssa(sv)a(sa(sv))') + 1]
        group = tmp_path / 'cgroup' / scope
        group.mkdir()
        (group / 'memory.max').write_text(memory_max + '\n')
        (group / 'memory.swap.max').write_text('0\n')
        (group / 'memory.oom.group').write_text('0\n')
        return 'o "/org/freedesktop/systemd1/job/1"'
    return run


def test_enrollment_uses_only_manager_properties_and_leaves_oom_group_to_the_manager(tmp_path, monkeypatch):
    calls = []
    saved, root = _fake_host(monkeypatch, tmp_path, _realizing_manager(tmp_path, calls))
    enrollment = campaign_host.install(root, {'run_id': ROOT_ID}, json.dumps({'memory_bytes': 256000000}).encode())
    [command] = calls
    assert command[:4] == ['/usr/bin/busctl', '--system', '--timeout=5s', 'call']
    body = command[command.index('fail') + 1:]
    count, triples, aux = int(body[0]), body[1:-1], body[-1]
    assert aux == '0' and len(triples) == 3 * count
    names = triples[0::3]
    assert 'MemoryOOMGroup' not in names
    assert names == ['MemoryMax', 'MemorySwapMax', 'MemoryAccounting', 'CPUAccounting']
    assert triples[triples.index('MemoryMax') + 2] == '256000000'
    group = tmp_path / 'cgroup' / enrollment['scope']
    # Untouched: the system manager owns memory.oom.group and would revert a write.
    assert (group / 'memory.oom.group').read_text() == '0\n'
    assert saved == {str(campaign_host.enrollment_path(root)): enrollment}
    assert campaign_host.enrollment_path(root) == root / 'code' / 'qualification-installation' / 'campaign-host.json'
    assert enrollment['memory_bytes'] == 256000000 and enrollment['scope'].endswith('.slice')
    rule = (tmp_path / 'rules.d' / ('49-' + enrollment['scope'][:-6] + '.rules')).read_text()
    assert rule.startswith('polkit.addRule')
    # StartTransientUnit carries no "unit" detail: the rule must not dereference it.
    assert 'unit === undefined' in rule and 'indexOf("' + enrollment['scope'][:-6] + '")' in rule
    assert 'subject.user != "qexec"' in rule and 'action.lookup("unit").indexOf' not in rule


def test_manager_refusal_surfaces_busctl_stderr(tmp_path, monkeypatch):
    def refusing(command):
        raise subprocess.CalledProcessError(1, command, output='',
            stderr='Cannot set property MemoryOOMGroup, or unknown property.')
    _, root = _fake_host(monkeypatch, tmp_path, refusing)
    with pytest.raises(ValueError, match='enrollment failed: .*unknown property'):
        campaign_host.install(root, {'run_id': ROOT_ID}, json.dumps({'memory_bytes': 1}).encode())


def test_unrealized_slice_is_refused_after_the_bounded_wait(tmp_path, monkeypatch):
    _, root = _fake_host(monkeypatch, tmp_path, lambda command: 'o "/org/freedesktop/systemd1/job/2"')
    with pytest.raises(ValueError, match='not realized'):
        campaign_host.install(root, {'run_id': ROOT_ID}, json.dumps({'memory_bytes': 1}).encode())


def test_divergent_slice_attributes_are_refused(tmp_path, monkeypatch):
    calls = []
    _, root = _fake_host(monkeypatch, tmp_path, _realizing_manager(tmp_path, calls, memory_max='max'))
    with pytest.raises(ValueError, match='attributes differ'):
        campaign_host.install(root, {'run_id': ROOT_ID}, json.dumps({'memory_bytes': 256000000}).encode())


def test_slice_limits_written_after_the_directory_appears_are_awaited(tmp_path, monkeypatch):
    clock = [0.0]
    polls = []
    group = None

    def run(command):
        nonlocal group
        scope = command[command.index('ssa(sv)a(sa(sv))') + 1]
        group = tmp_path / 'cgroup' / scope
        group.mkdir()
        (group / 'memory.max').write_text('max\n')
        (group / 'memory.swap.max').write_text('max\n')
        return 'o "/org/freedesktop/systemd1/job/3"'

    def advance(seconds):
        polls.append(seconds)
        clock[0] += seconds
        # Only a retry can publish the manager's limits. The old one-shot
        # implementation necessarily sees max/max and fails before this call.
        (group / 'memory.max').write_text('256000000\n')
        (group / 'memory.swap.max').write_text('0\n')

    _, root = _fake_host(monkeypatch, tmp_path, run)
    monkeypatch.setattr(campaign_host.time, 'monotonic', lambda: clock[0])
    monkeypatch.setattr(campaign_host.time, 'sleep', advance)
    enrollment = campaign_host.install(root, {'run_id': ROOT_ID}, json.dumps({'memory_bytes': 256000000}).encode())
    assert polls == [0.05]
    assert campaign_host._realize_common_slice(enrollment['scope'], 256000000) == {
        'memory.max': '256000000', 'memory.swap.max': '0'}

def test_foreign_run_identity_is_refused_before_any_side_effect(tmp_path, monkeypatch):
    calls = []
    saved, root = _fake_host(monkeypatch, tmp_path, _realizing_manager(tmp_path, calls))
    with pytest.raises(ValueError, match='identity differs'):
        campaign_host.install(root, {'run_id': 'b' * 32}, json.dumps({'memory_bytes': 1}).encode())
    assert calls == [] and saved == {}


def test_guardian_start_command_ends_option_parsing_before_dash_prefixed_values():
    """busctl permutes options: '--' must precede 'call' or ExecStart's '-I'/'--attempt' are read as busctl flags."""
    from tools.qualification_verification.container_ownership import CAMPAIGN_BUS_START, campaign_scopes
    from c1_rail.qualification.execution.campaign_supervisor import guardian_unit_spec, manager_start_arguments
    assert CAMPAIGN_BUS_START.index('--') < CAMPAIGN_BUS_START.index('call')
    assert all(not item.startswith('-') for item in CAMPAIGN_BUS_START[CAMPAIGN_BUS_START.index('--') + 1:])
    scopes = campaign_scopes('host1', 'attempt-1', 'work-1')
    spec = guardian_unit_spec(scopes, attempt_id='attempt-1', work_id='work-1', code_root='/opt/qualification',
        interpreter='/opt/ops/bin/python', uid=61001, orchestration_cpu_ns=20_000_000_000, remaining_wall_ns=20_000_000_000,
        cpu_ns=120_000_000_000, deadline_boottime_ns=1_000_000_000_000)
    arguments = manager_start_arguments(scopes, spec)
    assert {'-I', '--attempt', '--work'} <= set(arguments)
