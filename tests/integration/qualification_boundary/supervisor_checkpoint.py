"""Administrator-only TEST_ONLY process barrier; never supplies execution data."""
import json
import os
from pathlib import Path
import runpy
import signal
import sys
import threading

code, checkpoint, receipt = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
release = json.loads((code/'qualification-installation/release.json').read_bytes())
if release['authority_class'] != 'TEST_ONLY' or release['production_execution']:
    raise SystemExit('checkpoint driver requires synthetic TEST_ONLY installation')
modules = {
    'record_container': 'c1_rail.qualification.execution.store',
    'start_and_capture': 'concurrent.futures.thread',
    'archive_capture': 'c1_rail.qualification.execution.archive',
    'commit_authority': 'c1_rail.qualification.execution.service',
}
if checkpoint not in modules:
    raise SystemExit('unknown administrator checkpoint')
fired = False


def trace(frame, event, _argument):
    global fired
    # CPython 3.12 can write inspected frame locals back while tracing an
    # inlined comprehension. Never inspect unrelated frames or line events.
    if fired or event != 'call' or frame.f_globals.get('__name__') != modules[checkpoint]:
        return None
    matched = (frame.f_code.co_name == checkpoint
               and frame.f_globals.get('__name__') == modules[checkpoint])
    container = None
    if checkpoint == 'start_and_capture':
        if frame.f_code.co_name != 'submit':
            return None
        caller = frame.f_back
        if (caller is None or caller.f_code.co_name != '_execute'
                or caller.f_globals.get('__name__') != 'c1_rail.qualification.execution.service'):
            return None
        target = frame.f_locals.get('fn')
        # Stop the execution thread before it submits capture. Stopping inside
        # the capture thread can suspend an already pending docker inspect and
        # expire its unrelated subprocess deadline while the service is paused.
        matched = (frame.f_code.co_name == 'submit'
                   and frame.f_globals.get('__name__') == modules[checkpoint]
                   and getattr(target, '__module__', '') == 'c1_rail.qualification.execution.launcher'
                   and getattr(target, '__name__', '') == 'start_and_capture'
                   and caller is not None and caller.f_code.co_name == '_execute'
                   and caller.f_globals.get('__name__') == 'c1_rail.qualification.execution.service')
        if matched:
            container = frame.f_locals['args'][0]
    elif checkpoint == 'commit_authority':
        if frame.f_code.co_name != 'now':
            return None
        caller = frame.f_back
        if (caller is None or caller.f_code.co_name != '_commit'
                or caller.f_globals.get('__name__') != modules[checkpoint]):
            return None
        # The first _commit clock call precedes reconstruction. Only stop after
        # the real verifier has returned evidence and before selecting commit time.
        values = caller.f_locals
        if values.get('evidence') is None:
            return None
        matched = True
        container = values['status']['container_id']
    elif matched:
        container = frame.f_locals.get('container_id')
    if not fired and event == 'call' and matched:
        fired = True
        sys.settrace(None)
        threading.settrace(None)
        document = dict(checkpoint=checkpoint, pid=os.getpid(),
                        container_id=container)
        with receipt.open('x') as stream:
            json.dump(document, stream)
            stream.flush()
            os.fsync(stream.fileno())
        # A process-directed stop can reach another thread first and let this
        # callback return. Target the caller so its clock cannot advance first.
        signal.pthread_kill(threading.get_ident(), signal.SIGSTOP)
    return None


threading.settrace(trace)
sys.settrace(trace)
sys.argv = [str(code/'bootstrap.py'), 'supervisor']
runpy.run_path(sys.argv[0], run_name='__main__')
