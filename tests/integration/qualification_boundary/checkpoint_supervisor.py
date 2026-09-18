"""Administrator TEST_ONLY timing harness; never installed in a worker/release.

Runs the measured, canonical bootstrap. Wrappers observe real SQLite operations
and pause processes; no transition, signature, result or clock is supplied here.
The root-owned control file is unavailable through the service protocol.
"""
import functools
import json
import os
from pathlib import Path
import runpy
import sys
import threading
import time


def main():
    root = Path(__file__).resolve().parents[3]
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(root / part) for part in ('ops', 'core', 'lab', 'governance', '')]
    from c1_rail.qualification.execution import service, signing
    from c1_rail.qualification.execution.runtime import protected_path, load_instance
    from c1_rail.qualification.execution.store import ExecutionStore

    control = Path(sys.argv[1])
    protected_path(control)
    config = load_instance(root / 'qualification-installation/supervisor.json')
    release = load_instance(root / 'qualification-installation/release.json')
    if (sys.platform != 'linux' or not sys.flags.isolated
            or os.geteuid() != config['service_uid']
            or release['authority_class'] != 'TEST_ONLY'):
        raise ValueError('protected TEST_ONLY supervisor harness required')
    rules = json.loads(control.read_bytes())
    directory = Path(rules['directory'])
    local = threading.local()
    original_handle = service.ExecutionService.handle_request

    def checkpoint(name):
        if name not in rules['observe']:
            return
        # One occurrence per run. Repeated status reads cannot overwrite evidence.
        marker = directory / (name + '.json')
        try:
            with marker.open('x') as stream:
                json.dump(dict(checkpoint=name, pid=os.getpid(), uid=os.geteuid(),
                               thread=threading.get_ident(), monotonic_ns=time.monotonic_ns()), stream)
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            return
        if name in rules['pause']:
            deadline = time.monotonic() + 180
            while not (directory / (name + '.release')).exists():
                if time.monotonic() > deadline:
                    raise TimeoutError('administrator checkpoint expired: ' + name)
                time.sleep(.01)

    def transaction_name():
        frame = sys._getframe(1)
        while frame:
            if frame.f_code is service.ExecutionService._commit.__code__:
                return 'COMMIT'
            if frame.f_code is signing.sign_captured.__code__:
                local.sign_transactions += 1
                return 'PUBLISH' if local.sign_transactions == 2 else 'CAPTURE_READ'
            if frame.f_code is original_handle.__code__:
                operation = frame.f_locals.get('operation')
                if operation == 'VOID':
                    return 'VOID' if 'status' in frame.f_locals else 'VOID_STATUS'
                if operation == 'COMMIT_N1_RESULT':
                    return 'COMMIT_STATUS'
                return operation or 'OTHER'
            frame = frame.f_back
        return 'OTHER'

    original_connect = ExecutionStore._connect

    class ObservedConnection:
        def __init__(self, connection):
            self.connection = connection
            self.label = None
            connection.set_trace_callback(self.trace)

        def trace(self, statement):
            if statement == 'BEGIN IMMEDIATE':
                checkpoint(self.label + '.attempt')

        def execute(self, statement, *arguments):
            if statement == 'BEGIN IMMEDIATE':
                self.label = transaction_name()
                checkpoint(self.label + '.before')
            result = self.connection.execute(statement, *arguments)
            if statement == 'BEGIN IMMEDIATE':
                checkpoint(self.label + '.locked')
            if statement == 'COMMIT':
                pending = getattr(local, 'after_commit', [])
                local.after_commit = []
                for name in pending:
                    checkpoint(name)
                checkpoint(self.label + '.committed')
            if statement == 'ROLLBACK':
                local.after_commit = []
            return result

        def __getattr__(self, name):
            return getattr(self.connection, name)

    ExecutionStore._connect = lambda store: ObservedConnection(original_connect(store))

    def observe_method(method, name):
        @functools.wraps(method)
        def wrapped(store, *args, **kwargs):
            result = method(store, *args, **kwargs)
            if getattr(store._local, 'connection', None) is None:
                checkpoint(name)
            else:
                local.after_commit = [*getattr(local, 'after_commit', []), name]
            return result
        return wrapped

    for method, name in [('record_container', 'CONTAINER'), ('record_start_intent', 'START_INTENT'),
                         ('record_capture', 'CAPTURED')]:
        setattr(ExecutionStore, method, observe_method(getattr(ExecutionStore, method), name))
    original_sign = service.sign_captured

    def observed_sign(*args, **kwargs):
        local.sign_transactions = 0
        try:
            return original_sign(*args, **kwargs)
        finally:
            checkpoint('PUBLISH.finished')
    service.sign_captured = observed_sign

    submit_lock = threading.Lock()
    submissions = 0

    def observed_request(instance, peer_uid, raw):
        nonlocal submissions
        if json.loads(raw).get('operation') == 'SUBMIT_N1':
            with submit_lock:
                submissions += 1
                number = submissions
            checkpoint('SUBMIT_ENTERED.' + str(number))
        return original_handle(instance, peer_uid, raw)
    service.ExecutionService.handle_request = observed_request

    sys.argv = [str(root / 'bootstrap.py'), 'supervisor']
    runpy.run_path(sys.argv[0], run_name='__main__')


if __name__ == '__main__':
    main()
