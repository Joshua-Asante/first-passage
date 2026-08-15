"""Parse per-strategy baseline PF from baselines.md — never hardcode the numbers."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    from lifecycle import STRATEGY_KEYS
except ImportError:  # pragma: no cover
    from core.lifecycle import STRATEGY_KEYS

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASELINES_PATH = (
    REPO_ROOT
    / ".claude"
    / "skills"
    / "trade-csv-reconcile"
    / "references"
    / "baselines.md"
)

# baselines.md section titles → core.lifecycle.STRATEGY_KEYS (§0.5(A)).
# Keys must stay identical to STRATEGY_KEYS; asserted at load time.
_SECTION_TO_STRATEGY: dict[str, str] = {
    "Guardian Gold": "Guardian",
    "Striker DJ30": "Striker",
    "Striker NAS100": "Striker NAS100",
    "Aegis-Reversion": "Aegis",
}

_SECTION_HEADER_RE = re.compile(
    r"^##\s+(Guardian Gold|Striker DJ30|Striker NAS100|Aegis-Reversion)\b",
    re.MULTILINE,
)
# Pepperstone row: | Pepperstone | N | PF | ...
_PEPPERSTONE_PF_RE = re.compile(
    r"^\|\s*Pepperstone\s*\|\s*\d+\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*\|",
    re.MULTILINE,
)
# Public-tree remediation marker (ADR 2026-08-14). Do not guess PF from this.
_REDACTED_MARKER = "redacted from the public tree"


class BaselineDataUnavailable(ValueError):
    """PF tables absent or redacted — callers should skip, not guess."""


@dataclass(frozen=True)
class BaselinePF:
    """One strategy's baseline PF with parse provenance."""

    strategy: str
    pf: float
    source_path: str
    section: str
    line_number: int  # 1-indexed line of the Pepperstone PF cell row


def load_baseline_pfs(path: Path | None = None) -> dict[str, BaselinePF]:
    """Parse Pepperstone PF from baselines.md, keyed by STRATEGY_KEYS.

    Raises ``ValueError`` on missing section, missing Pepperstone PF, or a
    keyset mismatch with ``core.lifecycle.STRATEGY_KEYS``.
    """
    src = Path(path) if path is not None else DEFAULT_BASELINES_PATH
    if not src.is_file():
        raise ValueError(f"baselines.md not found: {src}")

    text = src.read_text(encoding="utf-8")
    lines = text.splitlines()
    headers = list(_SECTION_HEADER_RE.finditer(text))
    if not headers:
        raise ValueError(f"no strategy section headers found in {src}")

    found: dict[str, BaselinePF] = {}
    for i, match in enumerate(headers):
        section = match.group(1)
        strategy = _SECTION_TO_STRATEGY[section]
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]
        pf_match = _PEPPERSTONE_PF_RE.search(block)
        if pf_match is None:
            if _REDACTED_MARKER in block or _REDACTED_MARKER in text:
                raise BaselineDataUnavailable(
                    f"baseline PF redacted under ## {section} in {src} "
                    "(public-tree placeholder; private archive holds the values)"
                )
            raise ValueError(
                f"refusing to guess: no Pepperstone PF row under ## {section} in {src}"
            )
        pf = float(pf_match.group(1))
        # Absolute char offset of the Pepperstone match → line number in full file.
        abs_pos = start + pf_match.start()
        line_number = text.count("\n", 0, abs_pos) + 1
        # Sanity: the line content should still look like the Pepperstone row.
        if line_number < 1 or line_number > len(lines):
            raise ValueError(f"internal line-map failure for {section} in {src}")
        found[strategy] = BaselinePF(
            strategy=strategy,
            pf=pf,
            source_path=str(src.resolve()),
            section=section,
            line_number=line_number,
        )

    expected = set(STRATEGY_KEYS)
    got = set(found)
    if got != expected:
        raise ValueError(
            f"baseline keyset {sorted(got)} != STRATEGY_KEYS {sorted(expected)}"
        )
    # Explicit ordered-key assertion (§0.5(A)): mapping keys == sorted STRATEGY_KEYS.
    if sorted(found) != sorted(STRATEGY_KEYS):
        raise ValueError(
            f"sorted baseline keys {sorted(found)} != sorted(STRATEGY_KEYS) "
            f"{sorted(STRATEGY_KEYS)}"
        )
    return found
