"""grammar.py — deep-lane mutation grammar: schema + SHA256 freeze/drift check.

GROW spec v2 Part A (docs/spec/2026-08-22-grow-lane-generate-refine-spec.md)
step 2: "K = G, fully counted" -- the campaign prereg freezes an operator
grammar (enumerated mutation-operator families over entry/filter conditions,
exit/stop geometry, and sizing policy) plus a generation budget G at G0.
This module owns two things only: schema validation, and the SHA256
freeze/drift check (audit repair G-D1-FREEZE) -- mirroring the
PORT_MANIFEST.sha256 pattern already used for locked-strategy ports (root
CLAUDE.md, Public-clone posture). It does not run the refine loop or score
anything.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class GrammarValidationError(ValueError):
    """Raised when a grammar.json fails schema validation."""


class GrammarDriftError(ValueError):
    """Raised when a loaded grammar's SHA256 does not match the pinned value."""


@dataclass(frozen=True)
class Grammar:
    generation_budget: int
    families: dict[str, Any]
    sha256: str
    source_path: str


def sha256_of_grammar(path: str | Path) -> str:
    """Hash the grammar file's raw bytes (not a re-serialization) -- matches
    what a human diffing the committed file on disk actually sees."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _validate(raw: Any) -> tuple[int, dict[str, Any]]:
    if not isinstance(raw, dict):
        raise GrammarValidationError("grammar must be a JSON object")

    budget = raw.get("generation_budget")
    if not isinstance(budget, int) or isinstance(budget, bool) or budget < 1:
        raise GrammarValidationError(
            "generation_budget must be a positive int (this is G in K=G)"
        )

    families = raw.get("families")
    if not isinstance(families, dict) or not families:
        raise GrammarValidationError(
            "families must be a non-empty object mapping family name -> "
            "parameter-range list (or dict of such lists)"
        )
    for name, spec in families.items():
        if isinstance(spec, list):
            if not spec:
                raise GrammarValidationError(f"family {name!r}: empty range list")
            continue
        if isinstance(spec, dict):
            if not spec:
                raise GrammarValidationError(f"family {name!r}: empty parameter dict")
            for param, values in spec.items():
                if not isinstance(values, list) or not values:
                    raise GrammarValidationError(
                        f"family {name!r} param {param!r}: must be a non-empty list"
                    )
            continue
        raise GrammarValidationError(
            f"family {name!r}: must be a list of values, or a dict of "
            f"param -> non-empty list (got {type(spec).__name__})"
        )

    return budget, families


def load_grammar(path: str | Path) -> Grammar:
    """Load + schema-validate a grammar.json. Does not check any pin."""
    p = Path(path)
    raw = json.loads(p.read_text(encoding="utf-8"))
    budget, families = _validate(raw)
    return Grammar(
        generation_budget=budget,
        families=families,
        sha256=sha256_of_grammar(p),
        source_path=str(p),
    )


def load_grammar_with_hash_check(path: str | Path, *, expected_sha256: str) -> Grammar:
    """Load + validate, then hard-fail on any drift from the PREREG-pinned hash.

    Raises GrammarDriftError (not a silent warning) -- a campaign prereg pins
    one grammar; a mid-campaign edit is a new campaign, never a live catalogue
    widening (Route B G0 hard rule, imported for this lane by GROW spec v2 D1).
    """
    grammar = load_grammar(path)
    if grammar.sha256 != expected_sha256:
        raise GrammarDriftError(
            f"grammar at {path} has sha256={grammar.sha256}, expected "
            f"{expected_sha256} -- the PREREG-pinned grammar has drifted. "
            "A grammar change is a new campaign, not an edit to this one."
        )
    return grammar
