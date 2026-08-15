"""Harness-owned consecutive-breach counter (NOT lifecycle_state.json)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping

from .evaluate import WindowOutcome

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BREACH_STATE_PATH = (
    REPO_ROOT / "lab" / "discovery" / "lifecycle_call1" / "breach_state.json"
)


def load_breach_state(path: Path | None = None) -> dict[str, int]:
    """Load per-strategy consecutive-breach counts; absent file → {}."""
    src = Path(path) if path is not None else DEFAULT_BREACH_STATE_PATH
    if not src.is_file():
        return {}
    raw = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"breach state must be a JSON object: {src}")
    out: dict[str, int] = {}
    for key, value in raw.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(
                f"breach state values must be non-negative ints; got {key!r}: {value!r}"
            )
        out[str(key)] = value
    return out


def save_breach_state(state: Mapping[str, int], path: Path | None = None) -> Path:
    """Persist consecutive-breach counters to the harness-owned file."""
    dest = Path(path) if path is not None else DEFAULT_BREACH_STATE_PATH
    dest.parent.mkdir(parents=True, exist_ok=True)
    payload = {k: int(v) for k, v in sorted(state.items())}
    dest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return dest


def update_consecutive(
    state: Mapping[str, int],
    strategy: str,
    outcome: WindowOutcome,
) -> dict[str, int]:
    """Return a new state dict after applying one window outcome.

    Semantics (§0.5 / §2.4):
    - BREACH → increment by 1
    - CLEAR → reset to 0
    - AMBIGUOUS → leave unchanged (inert data-gap window)
    """
    out = dict(state)
    current = int(out.get(strategy, 0))
    if outcome == "BREACH":
        out[strategy] = current + 1
    elif outcome == "CLEAR":
        out[strategy] = 0
    elif outcome == "AMBIGUOUS":
        out[strategy] = current  # inert
    else:  # pragma: no cover
        raise ValueError(f"unknown window outcome: {outcome!r}")
    return out
