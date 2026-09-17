"""Read-only/preflight CLI boundary for qualification control.

This module verifies inputs and inspects journals.  It intentionally has no
sign, freeze, execute, seal, admission, deployment, or activation command.
"""
from __future__ import annotations

import argparse
import base64
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence

from .qualification.attempt import AttemptStore
from .qualification.contract import (
    TrustedApprovalKey,
    parse_canonical_json,
)
from .qualification.preflight import (
    PreflightError,
    PreflightReceipt,
    exact_depth_subject,
    preflight_binding_bytes,
    revalidate_e1_preflight,
    validate_e1_preflight,
)


class QualificationCLIError(ValueError):
    """A CLI/preflight input is unsafe or incomplete."""


def load_trusted_approval_keys(
    registry_bytes: bytes, *, allow_test_authority: bool = False,
) -> Mapping[str, TrustedApprovalKey]:
    doc = parse_canonical_json(registry_bytes, label="qualification key registry")
    if not isinstance(doc, dict) or set(doc) != {"schema", "keys"}:
        raise QualificationCLIError("qualification key registry fields differ")
    if doc["schema"] != "qualification_trusted_keys/v1" or not isinstance(doc["keys"], list):
        raise QualificationCLIError("qualification key registry schema differs")
    keys: dict[str, TrustedApprovalKey] = {}
    for row in doc["keys"]:
        if not isinstance(row, dict) or set(row) != {
                "key_id", "public_key_b64", "authority_class", "revoked_at"}:
            raise QualificationCLIError("qualification key fields differ")
        authority = row["authority_class"]
        if authority == "TEST_ONLY" and not allow_test_authority:
            raise QualificationCLIError("TEST_ONLY keys are forbidden in production mode")
        if authority not in ("OPERATOR", "TEST_ONLY"):
            raise QualificationCLIError("qualification key authority is unsupported")
        key_id = row["key_id"]
        if not isinstance(key_id, str) or not key_id or key_id in keys:
            raise QualificationCLIError("qualification key identity is invalid or duplicate")
        try:
            public = base64.b64decode(row["public_key_b64"], validate=True)
        except (ValueError, TypeError) as exc:
            raise QualificationCLIError("qualification public key encoding is invalid") from exc
        revoked = row["revoked_at"]
        revoked_at = None
        if revoked is not None:
            try:
                revoked_at = datetime.fromisoformat(revoked.replace("Z", "+00:00"))
            except (AttributeError, ValueError) as exc:
                raise QualificationCLIError("qualification key revocation time is invalid") from exc
            if revoked_at.tzinfo is None or revoked_at.utcoffset() is None:
                raise QualificationCLIError("qualification key revocation time must be aware")
        keys[key_id] = TrustedApprovalKey(key_id, public, authority, revoked_at)
    return keys


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    status = subparsers.add_parser("status", help="inspect a journal without claiming its boot")
    status.add_argument("journal", type=Path)
    args = parser.parse_args(argv)
    if args.command == "status":
        print(json.dumps(AttemptStore.inspect(args.journal), default=str,
                         sort_keys=True, separators=(",", ":")))
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
