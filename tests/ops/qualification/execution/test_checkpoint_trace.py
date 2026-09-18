"""Driver callback safety only; these tests do not establish Linux execution."""
import ast
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest


def callback(checkpoint, **bindings):
    path = Path(__file__).resolve().parents[4] / 'tests/integration/qualification_boundary/supervisor_checkpoint.py'
    tree = ast.parse(path.read_text())
    mapping = next(node.value for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == 'modules' for target in node.targets))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'trace')
    scope = dict(checkpoint=checkpoint, modules=ast.literal_eval(mapping), fired=False, **bindings)
    # Load the actual callback without activating tracing or the installed bootstrap.
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), scope)
    return scope['trace'], scope


class UninspectableFrame(SimpleNamespace):
    @property
    def f_locals(self):
        raise AssertionError('unrelated frame locals must never be inspected')


@pytest.mark.parametrize('checkpoint', ['record_container', 'start_and_capture', 'archive_capture', 'commit_authority'])
@pytest.mark.parametrize('case', ['line', 'return', 'wrong_module', 'already_fired'])
def test_trace_never_inspects_unrelated_frame_locals(checkpoint, case):
    trace, scope = callback(checkpoint)
    name = {'start_and_capture': 'submit', 'commit_authority': 'now'}.get(checkpoint, checkpoint)
    frame = UninspectableFrame(f_code=SimpleNamespace(co_name=name),
        f_globals={'__name__': scope['modules'][checkpoint] if case != 'wrong_module' else 'ast'})
    if case == 'already_fired':
        scope['fired'] = True
    assert trace(frame, case if case in ('line', 'return') else 'call', None) is None


@pytest.mark.parametrize('case', ['wrong_function', 'absent_caller', 'wrong_caller_function', 'wrong_caller_module'])
def test_trace_ignores_other_executor_calls_before_reading_locals(case):
    trace, _ = callback('start_and_capture')
    caller = SimpleNamespace(f_code=SimpleNamespace(co_name='_execute'),
        f_globals={'__name__': 'c1_rail.qualification.execution.service'})
    if case == 'wrong_caller_function': caller.f_code.co_name = 'other'
    if case == 'wrong_caller_module': caller.f_globals['__name__'] = 'other'
    frame = UninspectableFrame(f_code=SimpleNamespace(co_name='other' if case == 'wrong_function' else 'submit'),
        f_globals={'__name__': 'concurrent.futures.thread'},
        f_back=None if case == 'absent_caller' else caller)
    assert trace(frame, 'call', None) is None


@pytest.mark.parametrize('checkpoint', ['record_container', 'start_and_capture', 'archive_capture', 'commit_authority'])
def test_trace_records_exact_container_and_triggers_once(tmp_path, checkpoint):
    calls = []
    receipt = tmp_path / 'receipt.json'
    trace, scope = callback(checkpoint, receipt=receipt, json=json,
        sys=SimpleNamespace(settrace=lambda value: calls.append(('sys', value))),
        threading=SimpleNamespace(settrace=lambda value: calls.append(('threading', value))),
        signal=SimpleNamespace(SIGSTOP=19),
        os=SimpleNamespace(getpid=lambda: 123, fsync=os.fsync,
            kill=lambda pid, sig: calls.append(('stop', pid, sig))))
    frame = SimpleNamespace(f_code=SimpleNamespace(co_name=checkpoint),
        f_globals={'__name__': scope['modules'][checkpoint]}, f_locals={'container_id': 'exact-container'})
    if checkpoint == 'start_and_capture':
        frame.f_code.co_name = 'submit'
        frame.f_back = SimpleNamespace(f_code=SimpleNamespace(co_name='_execute'),
            f_globals={'__name__': 'c1_rail.qualification.execution.service'})
        frame.f_locals = {'args': ('exact-container',), 'fn': SimpleNamespace(
            __name__='start_and_capture', __module__='c1_rail.qualification.execution.launcher')}
    if checkpoint == 'commit_authority':
        frame = UninspectableFrame(f_code=SimpleNamespace(co_name='now'),
            f_globals={'__name__': 'c1_rail.qualification.execution.service'},
            f_back=SimpleNamespace(f_code=SimpleNamespace(co_name='_commit'),
                f_globals={'__name__': 'c1_rail.qualification.execution.service'},
                f_locals={'evidence': object(), 'status': {'container_id': 'exact-container'}}))
    assert trace(frame, 'call', None) is None
    assert trace(frame, 'call', None) is None
    assert json.loads(receipt.read_bytes()) == dict(checkpoint=checkpoint, pid=123, container_id='exact-container')
    assert calls == [('sys', None), ('threading', None), ('stop', 123, 19)]

@pytest.mark.parametrize('case', ['wrong_function', 'absent_caller', 'wrong_caller_function', 'wrong_caller_module'])
def test_commit_checkpoint_checks_call_chain_before_reading_locals(case):
    trace, _ = callback('commit_authority')
    caller = UninspectableFrame(f_code=SimpleNamespace(co_name='_commit'),
        f_globals={'__name__': 'c1_rail.qualification.execution.service'})
    if case == 'wrong_caller_function': caller.f_code.co_name = 'other'
    if case == 'wrong_caller_module': caller.f_globals['__name__'] = 'other'
    frame = UninspectableFrame(f_code=SimpleNamespace(co_name='other' if case == 'wrong_function' else 'now'),
        f_globals={'__name__': 'c1_rail.qualification.execution.service'},
        f_back=None if case == 'absent_caller' else caller)
    assert trace(frame, 'call', None) is None


@pytest.mark.parametrize('present', [False, True])
def test_commit_checkpoint_waits_for_completed_reconstruction(present):
    trace, scope = callback('commit_authority')
    frame = UninspectableFrame(f_code=SimpleNamespace(co_name='now'),
        f_globals={'__name__': 'c1_rail.qualification.execution.service'},
        f_back=SimpleNamespace(f_code=SimpleNamespace(co_name='_commit'),
            f_globals={'__name__': 'c1_rail.qualification.execution.service'},
            f_locals={'evidence': None} if present else {}))
    assert trace(frame, 'call', None) is None
    assert scope['fired'] is False


def test_commit_transport_extends_only_initial_socket_deadline():
    import socket
    path = Path(__file__).resolve().parents[4] / 'tests/integration/qualification_boundary/test_boundary_lifecycle.py'
    tree = ast.parse(path.read_text())
    source = next(node.value for node in tree.body if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'COMMIT_WAIT_DRIVER' for target in node.targets))
    driver = ast.parse(ast.literal_eval(source))
    definition = next(node for node in driver.body if isinstance(node, ast.ClassDef) and node.name == 'CommitSocket')
    scope = dict(socket=socket, wait_seconds=90)
    exec(compile(ast.Module(body=[definition], type_ignores=[]), str(path), 'exec'), scope)
    with scope['CommitSocket']() as connection:
        connection.settimeout(10)
        assert connection.gettimeout() == 90
        connection.settimeout(4)
        assert connection.gettimeout() == 4
