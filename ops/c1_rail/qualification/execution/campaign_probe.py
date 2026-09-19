"""Harmless fixed installed resource probes; no input, draw or signing port."""
import argparse
import os
import time

RESUME_WAIT_SECONDS = 30


def _await_resume():
    """Pause until the guardian has retained this process's alive-verified identity.

    A container init receives only the signals it blocks or handles, so SIGUSR1
    is blocked first: a resume sent from that point on is queued by the kernel,
    never dropped, and the guardian sends it only after reading the block from
    /proc. Without a resume the probe ends non-zero inside the bound; a work
    that was never observed alive is never credited, so skipping this wait
    would gain nothing.
    """
    import signal
    signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1})
    signal.signal(signal.SIGUSR1, lambda *_: None)
    if signal.sigtimedwait({signal.SIGUSR1}, RESUME_WAIT_SECONDS) is None:
        raise SystemExit('supervisor resume signal absent')


def _burn():
    end = time.process_time() + 90
    while time.process_time() < end:
        sum(range(10000))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', choices=('noop', 'cpu', 'descendants', 'memory', 'wall', 'intent'), required=True)
    probe = parser.parse_args().probe
    _await_resume()
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
