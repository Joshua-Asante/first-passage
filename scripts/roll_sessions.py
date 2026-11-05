#!/usr/bin/env python3
"""Retired 2026-11 with docs/SESSIONS.md (governance cut; history at main b7eaff7).

Kept only so git hooks installed before the cut, which still call it, exit 0
instead of blocking merges. Rerun scripts/install_hooks.sh (or .bat) to drop
them, then delete this file.
"""
import sys

if __name__ == "__main__":
    sys.exit(0)
