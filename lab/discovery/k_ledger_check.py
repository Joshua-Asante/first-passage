#!/usr/bin/env python3
"""k_ledger_check.py — verify a candidate has a valid, closed backing K-ledger manifest.

Rule-0 finding (2026-08-19): nothing in scorer.py or promotion_packet.py
verifies that a candidate reaching scoring or promotion has a matching
register_search open/close manifest behind it. This closes that one gap only
-- it does not re-derive K, the Bonferroni floor, or BH-FDR survivorship;
register_search.py's close_run() already computed and froze those, and stays
the sole authority for that arithmetic. This module only checks that a
declared run_id exists in the ledger and was properly closed.

Usage:
  python -m discovery.k_ledger_check <run_id> [--ledger-dir PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from research_utils.repo_root import repo_root

_REPO_ROOT = repo_root()


@dataclass(frozen=True)
class ManifestCheckResult:
    ok: bool
    reasons: tuple[str, ...]
    manifest: Optional[dict[str, Any]]


def _ledger_dir(ledger_dir: str | Path | None) -> Path:
    if ledger_dir is not None:
        return Path(ledger_dir)
    return Path(os.environ.get("DISCOVERY_LEDGER", str(_REPO_ROOT / "discovery_manifests")))


def verify_manifest_backing(
    run_id: str, *, ledger_dir: str | Path | None = None
) -> ManifestCheckResult:
    """A candidate may be scored/promoted only if its declared run_id has a
    CLOSED manifest in the K-ledger, with a K value and recorded results.
    """
    path = _ledger_dir(ledger_dir) / f"{run_id}.json"
    if not path.is_file():
        return ManifestCheckResult(ok=False, reasons=("no_manifest",), manifest=None)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    reasons: list[str] = []
    if manifest.get("status") != "closed":
        reasons.append("manifest_not_closed")
    k = manifest.get("K")
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        reasons.append("k_missing_or_invalid")
    if manifest.get("results") is None:
        reasons.append("no_results")
    return ManifestCheckResult(ok=not reasons, reasons=tuple(reasons), manifest=manifest)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    p.add_argument("run_id")
    p.add_argument("--ledger-dir", default=None)
    args = p.parse_args(argv)
    result = verify_manifest_backing(args.run_id, ledger_dir=args.ledger_dir)
    if not result.ok:
        print(
            f"[refuse] run_id={args.run_id!r} reasons={','.join(result.reasons)}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"[ok]     run_id={args.run_id!r} K={result.manifest['K']} status=closed")


if __name__ == "__main__":
    main()
