"""Explicit administrator cleanup; see host.py for the single implementation."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from host import main

if __name__ == '__main__':
    if '--manifest' not in sys.argv:
        raise SystemExit('--manifest <absolute private ownership manifest> is required')
    raise SystemExit(main())
