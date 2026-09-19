"""Harmless fixed installed resource probes; no input, draw or signing port."""
import argparse
import os
import time

RESUME_WAIT_SECONDS = 30


def block_resume_signal():
    """First act of any supervised payload entrypoint: block SIGUSR1 (and install a
    no-op handler so a stray post-resume signal cannot terminate the process).

    A container init (PID 1 in its namespace) holds a blocked signal pending
    regardless of disposition, so a resume the guardian sends after retaining the
    identity is consumed by the later wait and never lost. S3's real worker
    entrypoint reuses this and await_resume; keep them here, importable by worker.
    """
    import signal
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})
    signal.signal(signal.SIGUSR1, lambda *_: None)


def await_resume():
    """Pause until the guardian resumes this process; returns None on timeout.

    Skipping this wait gains nothing: a work that was never observed alive is
    never credited, and a probe that does not wait simply ends non-zero inside
    the bound.
    """
    import signal
    return signal.sigtimedwait({signal.SIGUSR1}, RESUME_WAIT_SECONDS)


def _burn():
    end = time.process_time() + 90
    while time.process_time() < end:
        sum(range(10000))


def main():
    block_resume_signal()  # First act: no resume the guardian sends can be dropped.
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', choices=('noop', 'cpu', 'descendants', 'memory', 'wall', 'intent'), required=True)
    probe = parser.parse_args().probe
    if await_resume() is None:
        raise SystemExit('supervisor resume signal absent')
    if probe in ('noop', 'intent'):
        pass  # Identity was retained before the resume; nothing else to do.
    elif probe == 'cpu':
        _burn()
    elif probe == 'descendants':
        children = []
        for _ in range(2):
            child = os.fork()
            if child == 0:
                _burn()
                os._exit(0)
            children.append(child)
        for child in children:
            os.waitpid(child, 0)
    elif probe == 'memory':
        held = []
        while True:
            block = bytearray(1024 * 1024)
            for index in range(0, len(block), 4096):
                block[index] = 1
            held.append(block)
    else:
        time.sleep(600)
