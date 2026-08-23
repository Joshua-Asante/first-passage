#!/usr/bin/env python3
"""Clone the pinned NeMo Guardrails tag into third_party/ (gitignored).

Study clone only. Does not install the package or start a rails server.
Pin owner: docs/agent_rails/rails.yml ``nemo_pin``.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_agent_rails import DEFAULT_INVENTORY, load_inventory  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO / "third_party" / "nemo-guardrails"


def fetch(dest: Path, inventory_path: Path, *, force: bool = False) -> int:
    inventory = load_inventory(inventory_path)
    pin = inventory["nemo_pin"]
    repo_url = pin["repo"]
    tag = pin["tag"]
    expected = pin["commit"]
    if dest.exists():
        if not force:
            existing = subprocess.run(
                ["git", "-C", str(dest), "rev-parse", "HEAD"],
                check=False, capture_output=True, text=True,
            )
            if existing.returncode == 0 and existing.stdout.strip() == expected:
                print(f"nemo-fetch: already at {expected} ({dest})")
                return 0
            print(
                f"nemo-fetch: {dest} exists and is not {expected}; "
                "pass --force to replace",
                file=sys.stderr,
            )
            return 1
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    clone = subprocess.run(
        [
            "git", "clone", "--depth", "1", "--branch", str(tag),
            str(repo_url), str(dest),
        ],
        check=False, capture_output=True, text=True,
    )
    if clone.returncode != 0:
        print(clone.stderr or clone.stdout, file=sys.stderr)
        return clone.returncode
    got = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if got != expected:
        print(
            f"nemo-fetch: FAIL — HEAD {got} != pinned {expected}",
            file=sys.stderr,
        )
        return 1
    print(f"nemo-fetch: {tag} @ {got} -> {dest}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    try:
        return fetch(args.dest, args.inventory, force=args.force)
    except (OSError, KeyError, ValueError, RuntimeError) as exc:
        print(f"nemo-fetch: FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
