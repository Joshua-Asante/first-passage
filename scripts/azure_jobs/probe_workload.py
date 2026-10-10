"""Explicit remote safety probe, excluded from normal test discovery.

Run only as a named authorized public build test through scripts/fp.py pytest.
Cancellation should retain the printed prefix and kill the sleeping descendant.
"""
import subprocess
import sys
import time


def test_detached_tree_probe():
    print("public safety probe started", flush=True)
    child = subprocess.Popen([sys.executable, "-c",
                              "import time; print('owned child started',flush=True); time.sleep(120)"])
    try:
        time.sleep(120)
        assert child.wait(timeout=10) == 0
    finally:
        if child.poll() is None:
            child.kill()
            child.wait(timeout=10)
