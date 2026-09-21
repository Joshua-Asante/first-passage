"""Harmless fixed installed resource probes; no input, draw or signing port."""
import argparse
import os
import time

RESUME_WAIT_SECONDS = 30

# Readiness token: written to /proc/self/comm after the bootstrap-level resume
# block is verified, so the guardian can send SIGUSR1 only after the payload
# itself declared it armed. The interpreter's own comm is 'python...' until
# then. At most 15 bytes (TASK_COMM_LEN minus the NUL).
READINESS_TOKEN = 'fpq-armed'


def block_resume_signal():
    """Verify the bootstrap-level resume block, then declare readiness.

    bootstrap.py installed the no-op SIGUSR1 handler and blocked the signal
    for the payload roles before any import that could spawn threads, so every
    later thread inherited the blocked mask and a resume can only sit pending
    for the main thread's sigtimedwait. Renaming this process to the fixed
    token is the declaration the guardian polls /proc/<pid>/comm for: no
    SIGUSR1 is sent until the token is read back. S3's real worker entrypoint
    reuses this and await_resume; keep them here, importable by worker.
    """
    import signal
    if signal.SIGUSR1 not in signal.pthread_sigmask(signal.SIG_BLOCK, set()):
        raise SystemExit('resume block absent before readiness declaration')
    # No newline: /proc/self/comm keeps the written bytes as the comm verbatim.
    with open('/proc/self/comm', 'w') as comm:
        comm.write(READINESS_TOKEN)


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
    block_resume_signal()  # The bootstrap block, verified; readiness declared to the guardian.
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
