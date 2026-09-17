"""Build-time resolution from installed canonical owners; never retained code."""
from decimal import Decimal
import hashlib
from pathlib import Path

from c1_rail import book_policy, policy_fingerprint
import firm_rules

from .contract import canonical_json_bytes
from .policy import QualificationPolicy, _policy_document, parse_policy


def build_qualification_policy() -> bytes:
    tier = book_policy.TIER
    basis = Decimal(str(firm_rules.FIRM_RULES[tier]['starting_balance']))
    if not basis.is_finite() or basis <= 0:
        raise ValueError('INVALID_CANONICAL_PRODUCT_BASIS')
    owners = {name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
              for name, module in (('book_policy', book_policy), ('firm_rules', firm_rules),
                                   ('policy_fingerprint', policy_fingerprint))}
    raw = canonical_json_bytes(_policy_document(tier=tier, basis=format(basis, 'f'), owners=owners))
    parse_policy(raw)
    return raw


def require_installed_policy(policy: QualificationPolicy) -> None:
    """Build/installation check; active consumers compare approved release bytes."""
    if type(policy) is not QualificationPolicy or policy.canonical_bytes != build_qualification_policy():
        raise ValueError('INSTALLED_POLICY_MISMATCH')
    if parse_policy(policy.canonical_bytes) != policy:
        raise ValueError('POLICY_IDENTITY_MISMATCH')
