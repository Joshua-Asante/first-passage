"""Rule-7 reject-list for the recall sidecar's write path.

The Delete route for Q-XMEM-1 replaces an extraction LLM with deterministic
retrieval, which lets the Rule-7 denylist degrade from a human review
obligation into a mechanical reject-list (parent brief Phase A2). This module
is that reject-list.

Denylisted values are SOURCED AT RUNTIME from the canonical production files,
never transcribed here — transcription is exactly how a mirror drifts from the
thing it mirrors, and a stale denylist silently stops guarding.

Rejection rule, and why it is a conjunction:

  reject if  (denylisted value)  AND  (context term)   co-occur
  reject if  a 32+ hex run appears                     (LOCK hashes)
  reject if  a cold-store path appears                 (docs/ltm, lab/archive)

The Rule-7 hazard is a locked constant asserted AS AUTHORITY, not the digits
themselves. An unconditional numeric denylist would reject "recall floor was
0.70" — including this sidecar's own falsifier result — and a guard that cries
wolf gets switched off. The conjunction keeps it precise.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# Numbers below this many characters are too common to denylist on their own
# (contract_value 1 / 10 / 100 would match half the corpus).
_MIN_VALUE_LEN = 4

_HEX_RUN = re.compile(r"\b[0-9a-f]{32,}\b", re.I)
_COLD_STORE = re.compile(r"(docs/ltm/|lab/archive/)", re.I)

# Terms that turn a bare number into an assertion about a governed constant.
_CONTEXT_TERMS = (
    "risk", "pyramid", "base_risk", "dd_trigger", "dd_scale", "dd protection",
    "allocation", "anchor", "bust", "p99", "pass rate", "pass/", "lock",
    "multiplier", "lifecycle", "active_firm", "firm", "contract_value",
    "sl", "tp", "atr", "session", "trail", "proximity", "drawdown",
)


@dataclass
class Denylist:
    values: set[str] = field(default_factory=set)
    sources: list[str] = field(default_factory=list)


@dataclass
class Verdict:
    ok: bool
    reason: str = ""


def _distinctive(raw: str) -> str | None:
    """Keep a numeric literal only if it is distinctive enough to denylist."""
    tok = raw.strip().rstrip(".")
    if not tok or len(tok) < _MIN_VALUE_LEN:
        return None
    if "." not in tok:                      # bare integers are too common
        return None
    return tok


def load_denylist(repo_root: Path) -> Denylist:
    """Read governed constants out of their canonical files."""
    dl = Denylist()

    ddp = repo_root / "core" / "dd_protection.py"
    if ddp.exists():
        text = ddp.read_text(encoding="utf-8")
        for m in re.finditer(r"^(DD_TRIGGER|DD_SCALE)\s*=\s*([0-9.]+)", text, re.M):
            if v := _distinctive(m.group(2)):
                dl.values.add(v)
        dl.sources.append(str(ddp.relative_to(repo_root)))

    firms = repo_root / "core" / "firm_rules.py"
    if firms.exists():
        text = firms.read_text(encoding="utf-8")
        if m := re.search(r"^_BASE_RISK\s*=\s*\{(.+?)\}", text, re.M | re.S):
            for num in re.findall(r"([0-9]*\.[0-9]+)", m.group(1)):
                if v := _distinctive(num):
                    dl.values.add(v)
                # %-form (0.0034 → 0.34) — notes cite risk as percent, not fraction.
                try:
                    pct = float(num) * 100.0
                except ValueError:
                    continue
                for form in (f"{pct}", f"{pct:.2f}"):
                    if v := _distinctive(form):
                        dl.values.add(v)
        dl.sources.append(str(firms.relative_to(repo_root)))

    # Phase C: CFD percents left living _BASE_RISK. Still locked — source the
    # historical 4-leg book so 0.34 / 1.50 stay denylisted as authority.
    hist = repo_root / "core" / "historical_challenge.py"
    if hist.exists():
        text = hist.read_text(encoding="utf-8")
        if m := re.search(
            r"^HISTORICAL_CHALLENGE_BASE_RISK\s*=\s*\{(.+?)\}",
            text,
            re.M | re.S,
        ):
            for num in re.findall(r"([0-9]*\.[0-9]+)", m.group(1)):
                if v := _distinctive(num):
                    dl.values.add(v)
                try:
                    pct = float(num) * 100.0
                except ValueError:
                    continue
                for form in (f"{pct}", f"{pct:.2f}"):
                    if v := _distinctive(form):
                        dl.values.add(v)
        dl.sources.append(str(hist.relative_to(repo_root)))

    # MC anchor triple — the historical calibration, denylisted as authority.
    claude_md = repo_root / "CLAUDE.md"
    if claude_md.exists():
        text = claude_md.read_text(encoding="utf-8")
        if m := re.search(r"(\d{2}\.\d{2})% pass / (\d\.\d{2})% bust", text):
            dl.values.update(m.groups())
        if m := re.search(r"p99 DD (\d\.\d{2})%", text):
            dl.values.add(m.group(1))
        dl.sources.append("CLAUDE.md")

    return dl


def check(note: str, denylist: Denylist) -> Verdict:
    """Fail-closed gate for a staged note."""
    if not note or not note.strip():
        return Verdict(False, "empty note")

    if _HEX_RUN.search(note):
        return Verdict(False, "contains a 32+ char hex run (LOCK hash)")

    if m := _COLD_STORE.search(note):
        return Verdict(False, f"cold-store ingest denylisted: {m.group(1)}")

    low = note.lower()
    context = [t for t in _CONTEXT_TERMS if re.search(rf"\b{re.escape(t)}", low)]
    if not context:
        return Verdict(True)

    hits = [v for v in denylist.values if re.search(rf"(?<![\d.]){re.escape(v)}(?![\d])", note)]
    if hits:
        return Verdict(
            False,
            f"governed constant {sorted(hits)} asserted alongside "
            f"context {sorted(context)[:3]} — Rule-7 owns these values",
        )
    return Verdict(True)
