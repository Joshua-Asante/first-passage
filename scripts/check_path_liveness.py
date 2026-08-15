#!/usr/bin/env python3
"""check_path_liveness.py — committed-path liveness gate (governance tier).

Asserts every COMMITTED parent directory declared in
`core/strategies/MANIFEST.sha256` resolves on disk.

It NEVER checks `.pine` bytes — those are gitignored, so their absence on CI /
a public clone is legitimate (not drift). Only committed directories are
checked, so this gate is environment-independent.

The former `params.toml` lock_md / strategy-dir leg was retired with the
derived mirror (ADR docs/adr/2026-08-03-params-toml-gate-retirement.md).
Pine membership/hash integrity remains `scripts/check_pine_manifest.py`.

Exit codes:
  0 — every declared committed path resolves
  1 — one or more committed paths missing (stale manifest)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PINE_MANIFEST = REPO_ROOT / "core" / "strategies" / "MANIFEST.sha256"


def check_pine_manifest(pine_manifest_path: Path, repo_root: Path) -> list[str]:
    """Missing parent dirs for each `.pine` entry in MANIFEST.sha256."""
    if not pine_manifest_path.exists():
        return [f"pine manifest missing: {pine_manifest_path}"]
    misses: list[str] = []
    for lineno, raw in enumerate(
        pine_manifest_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        pine_rel = parts[-1]
        parent = (repo_root / pine_rel).parent
        if not parent.exists():
            misses.append(
                f"MANIFEST.sha256:{lineno}: parent dir of pine entry does not "
                f"resolve: {Path(pine_rel).parent.as_posix()}")
    return misses


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--pine-manifest", type=Path, default=DEFAULT_PINE_MANIFEST,
        help="path to MANIFEST.sha256 (default: core/strategies/MANIFEST.sha256)",
    )
    parser.add_argument(
        "--repo-root", type=Path, default=REPO_ROOT,
        help="root path the declared paths are resolved against",
    )
    args = parser.parse_args()

    misses = check_pine_manifest(args.pine_manifest, args.repo_root)

    for m in misses:
        print(f"HARD: {m}")
    if misses:
        print(f"\ncheck_path_liveness: {len(misses)} missing committed path(s) — "
              "stale manifest. A missing COMMITTED target is drift, not an "
              "environment artifact; re-point the manifest, do not relax the gate.")
        return 1
    # Scope-honest success string (corrected 2026-08-08): this gate resolves path
    # literals declared in the Pine manifest's parent dirs, NOT every committed path
    # in the repo. The prior wording ("all declared committed paths resolve") read as
    # repo-wide assurance while frozen pre-registrations, docs/** fenced blocks and
    # lab/analysis/**/*.md cite non-resolving paths it never inspects.
    print("check_path_liveness: OK — all pine-manifest-scoped declared paths resolve "
          "(does NOT cover docs/**, lab/analysis/**, or pre-registration citations).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
