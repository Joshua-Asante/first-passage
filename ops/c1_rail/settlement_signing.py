"""Operator-side reply construction. No private keys, storage or runtime authority."""
from datetime import datetime, timezone

CHALLENGE_SCHEMA = "settlement_challenge/v2"


def signing_envelope(challenge: dict, *, signed_at: datetime) -> dict:
    """Add the signing instant immediately before signing the canonical returned bytes.

    The operator must review the challenge and hash-bound package first. Sign the
    complete returned mapping using Ed25519; submit it unchanged with the signature.
    """
    if not isinstance(signed_at, datetime) or signed_at.tzinfo is None or signed_at.utcoffset() is None:
        raise ValueError("signing time must be timezone-aware")
    if not isinstance(challenge, dict) or challenge.get("schema") != CHALLENGE_SCHEMA \
            or "operator_signed_utc" in challenge:
        raise ValueError("expected an unsigned v2 settlement challenge")
    return {**challenge, "operator_signed_utc": signed_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
