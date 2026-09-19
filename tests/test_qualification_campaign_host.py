"""S2 campaign-host enrollment: manager call carries real properties only; oom.group is pinned on the realized slice.

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


def test_enrollment_uses_only_manager_properties_and_pins_group_oom_on_the_slice(tmp_path, monkeypatch):
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
    assert (group / 'memory.oom.group').read_text() == '1'
    assert saved == {str(campaign_host.enrollment_path(root)): enrollment}
    assert campaign_host.enrollment_path(root) == root / 'code' / 'qualification-installation' / 'campaign-host.json'
    assert enrollment['memory_bytes'] == 256000000 and enrollment['scope'].endswith('.slice')
    assert (tmp_path / 'rules.d' / ('49-' + enrollment['scope'][:-6] + '.rules')).read_bytes().startswith(b'polkit.addRule')


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


def test_foreign_run_identity_is_refused_before_any_side_effect(tmp_path, monkeypatch):
    calls = []
    saved, root = _fake_host(monkeypatch, tmp_path, _realizing_manager(tmp_path, calls))
    with pytest.raises(ValueError, match='identity differs'):
        campaign_host.install(root, {'run_id': 'b' * 32}, json.dumps({'memory_bytes': 1}).encode())
    assert calls == [] and saved == {}
