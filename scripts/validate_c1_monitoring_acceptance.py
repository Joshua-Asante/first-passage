#!/usr/bin/env python3
"""Validate the M1 monitoring acceptance artifact (secret-free).

Per docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md §4 / §10.

A PENDING/CODE_LANDED artifact is structurally valid and documents that
operator SIM drills remain owed. Only status=RESOLVED (with all required
drill fields) may unlock the next dry_run=false entry/add send.

Usage:
  python scripts/validate_c1_monitoring_acceptance.py \\
    docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json
  python scripts/validate_c1_monitoring_acceptance.py \\
    docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json --require-resolved
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SECRET_KEYS = frozenset({
    "secret_key", "webhook_secret", "path_token", "webhook_id",
    "crosstrade_api_token", "bearer", "authorization", "password", "api_token",
})
SECRET_HINT = re.compile(r"(?i)(secret|token|bearer|password|authorization)\s*[:=]")

VALID_STATUSES = frozenset({"PENDING", "CODE_LANDED", "AMBIGUOUS", "RESOLVED", "FALSIFIED"})

REQUIRED_TOP = (
    "schema_version", "status", "adr", "code_commit_or_branch",
    "offline_tests_note", "secrets_present",
)

RESOLVED_REQUIRED = (
    "fixture_hashes",
    "dry_run_strategy_signal_event_id",
    "sim_chain_ok_event_id",
    "reconcile_verdict",
    "notification_alert_id",
    "notification_acked",
    "drills",
    "operator_signoff",
)

REQUIRED_DRILLS = frozenset({
    "transport_unknown",
    "partial_fill_confirmed_base",
    "rejected_entry_no_add",
    "exit_on_equity_failure",
    "restart_confirmed_base",
    "b6_wrong_secret_shape",
})


def _walk_secrets(obj, path="$"):
    findings = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            kl = str(k).lower()
            if kl in SECRET_KEYS or any(
                bad in kl for bad in ("secret", "token", "password", "bearer")
            ):
                # Allow boolean secrets_present / notification_acked style flags.
                if not (isinstance(v, bool) or v is None):
                    findings.append(f"denylist key {k!r} at {path}")
            findings.extend(_walk_secrets(v, f"{path}.{k}"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            findings.extend(_walk_secrets(item, f"{path}[{i}]"))
    elif isinstance(obj, str) and SECRET_HINT.search(obj):
        findings.append(f"secret-shaped string at {path}")
    return findings


def validate(path: Path, *, require_resolved: bool) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"unreadable JSON: {exc}"]

    if not isinstance(data, dict):
        return ["root must be a JSON object"]

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing required field {key!r}")

    status = data.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"invalid status {status!r}; valid={sorted(VALID_STATUSES)}")

    if data.get("secrets_present") is not False:
        errors.append("secrets_present must be false (secret-free artifact)")

    errors.extend(_walk_secrets(data))

    if data.get("adr") != "2026-07-22-c1-venue-native-monitoring-maturity.md":
        errors.append("adr must point at the monitoring maturity ADR filename")

    if require_resolved or status == "RESOLVED":
        if status != "RESOLVED":
            errors.append(
                f"--require-resolved set but status={status!r} (need RESOLVED)")
        for key in RESOLVED_REQUIRED:
            if key not in data:
                errors.append(f"RESOLVED requires field {key!r}")
        if data.get("reconcile_verdict") != "CHAIN_OK":
            errors.append("RESOLVED requires reconcile_verdict=CHAIN_OK")
        if data.get("notification_acked") is not True:
            errors.append("RESOLVED requires notification_acked=true")
        drills = data.get("drills") or {}
        if not isinstance(drills, dict):
            errors.append("drills must be an object")
        else:
            missing = REQUIRED_DRILLS - set(drills)
            if missing:
                errors.append(f"RESOLVED missing drills: {sorted(missing)}")
            for name, ok in drills.items():
                if ok is not True:
                    errors.append(f"drill {name!r} is not true")
        signoff = data.get("operator_signoff") or {}
        if not isinstance(signoff, dict) or not signoff.get("operator"):
            errors.append("operator_signoff.operator required for RESOLVED")

    return errors


def tree_skew(path: Path, root: Path | None = None) -> list[tuple[str, str, str]]:
    """Compare `fixture_hashes` against the working tree.

    `fixture_hashes` records the bytes ACTUALLY RUNNING ON THE HOST, read
    in-container by sha256 — not the tree. So a mismatch is NOT an error: main
    legitimately moves ahead of the deployed build between deploys, and the pin
    must keep describing the deployed build until a real deploy replaces it.
    Rewriting it from local bytes would make the artifact assert a deploy that
    never happened.

    What IS worth catching is the skew going UNRECORDED, which is exactly what
    happened on 2026-07-31: commit 28ab8a6 moved two of the six pinned files and
    nothing noticed, because this validator only ever checked that the field was
    present. The skew surfaced by hand, during an incident. Returns
    (relpath, pinned, on_tree) per divergence; hashing mirrors the repo's
    working-tree-bytes convention (CLAUDE.md), so CRLF checkouts hash as CRLF.
    """
    root = root or REPO_ROOT
    data = json.loads(path.read_text(encoding="utf-8"))
    out: list[tuple[str, str, str]] = []
    for rel, pinned in sorted((data.get("fixture_hashes") or {}).items()):
        target = root / rel
        if not target.is_file():
            out.append((rel, pinned, "MISSING"))
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != pinned:
            out.append((rel, pinned, actual))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    ap.add_argument(
        "--require-resolved", action="store_true",
        help="fail unless status=RESOLVED with all §4 drill fields",
    )
    ap.add_argument(
        "--check-tree-skew", action="store_true",
        help="report where fixture_hashes (the DEPLOYED build) differs from this tree",
    )
    ap.add_argument(
        "--require-tree-current", action="store_true",
        help=("exit 1 on any such divergence. For pre-deploy / pre-arm use only — "
              "skew between deploys is normal, so this is never a commit gate"),
    )
    ap.add_argument(
        "--root", type=Path, default=None,
        help="tree to hash the pinned files against (default: this repo)",
    )
    args = ap.parse_args(argv)
    errors = validate(args.path, require_resolved=args.require_resolved)
    if errors:
        print(f"FAIL {args.path} ({len(errors)} error(s)):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    data = json.loads(args.path.read_text(encoding="utf-8"))
    print(f"OK status={data.get('status')} path={args.path}")
    if data.get("status") != "RESOLVED":
        print(
            "NOTE: M1 is not RESOLVED — next dry_run=false entry/add send "
            "remains gated.",
        )
    if args.check_tree_skew or args.require_tree_current:
        skew = tree_skew(args.path, root=args.root)
        pin_count = len(data.get("fixture_hashes") or {})
        if not skew and pin_count == 0:
            # Vacuous-assurance guard (added 2026-08-08). tree_skew() iterates
            # fixture_hashes, so an EMPTY pin set yields zero divergences and the
            # all-clear below would announce maximum confidence over a comparison
            # that never happened — including under --require-tree-current, the
            # mode reserved for pre-deploy / pre-arm use. Say nothing was checked.
            print("tree skew: NOT CHECKED — fixture_hashes is empty, so no pinned "
                  "file was compared. This is not a pass; re-pin from in-container "
                  "hashes at the next deploy.")
            return 1 if args.require_tree_current else 0
        if not skew:
            print(f"tree skew: none — all {pin_count} pinned file(s) match this tree, "
                  "so a redeploy from here would reproduce the pinned build.")
            return 0
        print(f"tree skew: {len(skew)} of "
              f"{len(data.get('fixture_hashes') or {})} pinned file(s) differ "
              f"from this tree (deployed pin -> tree):")
        for rel, pinned, actual in skew:
            print(f"  - {rel}\n      deployed {pinned[:8]}…  tree {actual[:8]}…")
        print("This is drift, not corruption: fixture_hashes describes the "
              "DEPLOYED build and stays authoritative until a real deploy.\n"
              "A redeploy MUST refresh the pin in the same motion, from hashes "
              "read in-container — never from these tree bytes.")
        return 1 if args.require_tree_current else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
