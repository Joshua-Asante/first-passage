"""Verified, durable-binding inputs for one exact-depth E1 attempt."""
from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Mapping

from .contract import (
    ApprovalRecord,
    TrustedApprovalKey,
    ValidatedFrozenContract,
    canonical_json_bytes,
    require_validated_frozen_contract,
    verify_detached_approval,
)
from .trust_domain import require_trusted_domain_key, require_validated_trust_domain


class PreflightError(ValueError):
    """The exact-depth approval or output reservation is unsafe."""


@dataclass(frozen=True)
class PreflightReceipt:
    attempt_id: str
    contract_sha256: str
    trust_domain_sha256: str
    exact_depth_subject_sha256: str
    exact_depth_approval: ApprovalRecord
    output_root: str


def exact_depth_subject(contract: ValidatedFrozenContract, *, attempt_id: str) -> bytes:
    try:
        contract = require_validated_frozen_contract(contract)
    except Exception as exc:
        raise PreflightError(f"validated frozen contract required: {exc}") from exc
    if not isinstance(attempt_id, str) or not attempt_id:
        raise PreflightError("attempt_id is required")
    stages = []
    for stage in contract.stage_specs.values():
        if stage.included_in_e1_seal:
            stages.append({
                "exact_depth": stage.exact_depth,
                "name": stage.name,
                "population_counts": {
                    name: list(values) for name, values in stage.population_counts.items()
                },
                "rng_namespace": stage.rng_namespace,
            })
    return canonical_json_bytes({
        "attempt_id": attempt_id,
        "budget": asdict(contract.replay.budget),
        "contract_sha256": contract.contract_sha256,
        "trust_domain_sha256": contract.trust_domain_sha256,
        "schema": "e1_exact_depth_subject/v1",
        "stages": stages,
    })


def preflight_binding_bytes(receipt: PreflightReceipt) -> bytes:
    if not isinstance(receipt, PreflightReceipt):
        raise PreflightError("typed preflight receipt is required")
    return canonical_json_bytes({
        "attempt_id": receipt.attempt_id,
        "contract_sha256": receipt.contract_sha256,
        "trust_domain_sha256": receipt.trust_domain_sha256,
        "exact_depth_approval_sha256": receipt.exact_depth_approval.approval_sha256,
        "exact_depth_subject_sha256": receipt.exact_depth_subject_sha256,
        "output_root": receipt.output_root,
        "schema": "e1_preflight_binding/v1",
    })


def _is_reparse_point(path: Path) -> bool:
    info = path.lstat()
    attributes = getattr(info, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return path.is_symlink() or bool(attributes & reparse_flag)


def validate_e1_preflight(
    contract: ValidatedFrozenContract,
    *, attempt_id: str, output_root: Path,
    exact_depth_approval_bytes: bytes,
    trusted_keys: Mapping[str, TrustedApprovalKey],
    now: datetime, trust_domain: object,
) -> PreflightReceipt:
    """Verify the second decision and atomically reserve a never-used root."""
    subject = exact_depth_subject(contract, attempt_id=attempt_id)
    try:
        domain = require_validated_trust_domain(trust_domain)
    except Exception as exc:
        raise PreflightError(f"validator-issued trust domain required: {exc}") from exc
    if contract.trust_domain is not domain or contract.trust_domain_sha256 != domain.sha256:
        raise PreflightError("preflight trust domain differs from frozen contract")
    subject_sha = hashlib.sha256(subject).hexdigest()
    approval = verify_detached_approval(
        exact_depth_approval_bytes,
        trusted_keys=trusted_keys,
        expected_scope="APPROVE_E1_EXACT_DEPTH",
        expected_subject_sha256=subject_sha,
        expected_contract_sha256=contract.contract_sha256,
        now=now,
        allow_test_authority=domain.authority_class == "TEST_ONLY",
    )
    key = trusted_keys.get(approval.key_id)
    try:
        if approval.key_id not in domain.freeze_key_ids or key is None:
            raise ValueError("exact-depth key is not enrolled for freeze authority")
        require_trusted_domain_key(domain, approval.key_id, key.public_key)
    except Exception as exc:
        raise PreflightError(f"exact-depth key differs from trust domain: {exc}") from exc
    requested = Path(output_root)
    if requested.exists():
        raise PreflightError("qualification output root must be new")
    parent = requested.parent.resolve(strict=True)
    if not parent.is_dir() or _is_reparse_point(parent):
        raise PreflightError("qualification output parent is unsafe")
    root = parent / requested.name
    try:
        root.mkdir(mode=0o700, exist_ok=False)
    except FileExistsError as exc:
        raise PreflightError("qualification output root was already reserved") from exc
    if _is_reparse_point(root):
        raise PreflightError("qualification output root is unsafe")
    receipt = PreflightReceipt(
        attempt_id, contract.contract_sha256, domain.sha256, subject_sha, approval, str(root),
    )
    # Force construction now so a malformed receipt cannot be reserved.
    preflight_binding_bytes(receipt)
    return receipt


def revalidate_e1_preflight(
    contract: ValidatedFrozenContract, receipt: PreflightReceipt, *,
    exact_depth_approval_bytes: bytes,
    trusted_keys: Mapping[str, TrustedApprovalKey], now: datetime,
    trust_domain: object,
) -> PreflightReceipt:
    """Reverify retained approval bytes without creating or changing the root."""
    if not isinstance(receipt, PreflightReceipt):
        raise PreflightError("typed preflight receipt is required")
    try:
        domain = require_validated_trust_domain(trust_domain)
    except Exception as exc:
        raise PreflightError(f"validator-issued trust domain required: {exc}") from exc
    if contract.trust_domain is not domain or receipt.trust_domain_sha256 != domain.sha256:
        raise PreflightError("preflight trust domain differs from frozen contract")
    subject = exact_depth_subject(contract, attempt_id=receipt.attempt_id)
    subject_sha = hashlib.sha256(subject).hexdigest()
    approval = verify_detached_approval(
        exact_depth_approval_bytes,
        trusted_keys=trusted_keys,
        expected_scope="APPROVE_E1_EXACT_DEPTH",
        expected_subject_sha256=subject_sha,
        expected_contract_sha256=contract.contract_sha256,
        now=now,
        allow_test_authority=domain.authority_class == "TEST_ONLY",
    )
    key = trusted_keys.get(approval.key_id)
    try:
        if approval.key_id not in domain.freeze_key_ids or key is None:
            raise ValueError("exact-depth key is not enrolled for freeze authority")
        require_trusted_domain_key(domain, approval.key_id, key.public_key)
    except Exception as exc:
        raise PreflightError(f"exact-depth key differs from trust domain: {exc}") from exc
    expected = PreflightReceipt(
        receipt.attempt_id, contract.contract_sha256, domain.sha256, subject_sha, approval,
        receipt.output_root,
    )
    if expected != receipt:
        raise PreflightError("preflight receipt differs from retained approval bytes")
    root = Path(receipt.output_root)
    if not root.is_dir() or _is_reparse_point(root):
        raise PreflightError("reserved qualification output root is missing or unsafe")
    return expected


__all__ = [
    "PreflightError", "PreflightReceipt", "exact_depth_subject",
    "preflight_binding_bytes", "revalidate_e1_preflight", "validate_e1_preflight",
]
