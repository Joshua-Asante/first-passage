"""Harmless fixed installed resource probes; no input, draw or signing port."""
import argparse
import os
import time


def _burn():
    end = time.process_time() + 90
    while time.process_time() < end:
        sum(range(10000))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--probe', choices=('noop', 'cpu', 'descendants', 'memory', 'wall', 'intent'), required=True)
    probe = parser.parse_args().probe
    if probe in ('noop', 'intent'):
        time.sleep(.2)  # Ensure the guardian can retain actual PID membership.
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
