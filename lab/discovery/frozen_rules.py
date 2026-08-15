"""Load frozen IS-derived rules from Stage-3 artifacts with hash verification."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from discovery.motif_rules import FrozenRule


class FrozenRuleLoadError(ValueError):
    """Raised when a frozen rule fails integrity checks."""


def _shape_hash(shape: np.ndarray) -> str:
    raw = np.asarray(shape, dtype=np.float64).tobytes()
    return hashlib.sha256(raw).hexdigest()[:16]


def load_frozen_rules(path: Path | str) -> list[FrozenRule]:
    """Reconstruct ``FrozenRule`` objects; refuse on ``shape_hash`` mismatch."""
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    rules: list[FrozenRule] = []
    for row in rows:
        shape = np.asarray(row["shape"], dtype=float)
        expected = row["shape_hash"]
        actual = _shape_hash(shape)
        if actual != expected:
            raise FrozenRuleLoadError(
                f"shape_hash mismatch for {row.get('candidate_id')}: "
                f"expected {expected}, got {actual}"
            )
        rules.append(
            FrozenRule(
                candidate_id=row["candidate_id"],
                kind=row["kind"],
                m=int(row["m"]),
                shape=shape,
                trigger=float(row["trigger"]),
                direction=int(row["direction"]),
                horizon=int(row["horizon"]),
                shape_hash=expected,
                source_index=int(row["source_index"]),
            )
        )
    return rules
