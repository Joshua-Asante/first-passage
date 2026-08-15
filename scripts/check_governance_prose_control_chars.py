#!/usr/bin/env python3
"""check_governance_prose_control_chars.py — reject stray C0 controls in governance prose.

THE FAILURE MODE (dated, not hypothetical — 2026-08-11):

  docs/SESSIONS.md carried a literal form-feed (U+000C) in the "2026-08-11o —
  MCL ledger" entry, inherited via an earlier union merge. The post-merge
  SESSIONS repair hook treats form-feed as a line break and rewrites that line
  into a broken two-line form with a trailing space. Fired twice on 2026-08-11
  (fast-forward of claude/strategy-candidate-generation-3dc0dc; origin/main
  merge into claude/approach-scoreboard-4f1a2c). Cause removed in faccf75
  (PR #743). No prior gate caught it — verified against scripts/gates.yml.

THE MECHANICAL RULE:

  In scoped markdown, forbid C0 controls other than TAB / LF / CR, and forbid
  DEL (U+007F). CR is allowed because Windows checkouts with autocrlf produce
  CRLF; rejecting it would brick the gate on an otherwise clean tree. Form-feed
  (U+000C) and vertical tab (U+000B) are the load-bearing rejects.

SCOPE (union-merge-prone + high-traffic prose; extend here, not via a flag):

  - docs/SESSIONS.md, docs/rejected_candidates.md, docs/mc_anchor_history.md
    (merge=union in .gitattributes — debris accumulates silently)
  - STATE.md (root orientation / board)
  - docs/adr/**/*.md, docs/briefs/**/*.md (decision + brief surfaces)
  - docs/notes/**/*.md (same class of hand-edited governance prose; sweep on
    2026-08-11 found a BEL from a mangled ``\\a`` escape there)

Exit 0 clean, 1 on any hit. Report file:line:column and the codepoint.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Allowed ASCII controls in prose. CR stays: CRLF checkouts are real here.
_ALLOWED_CONTROLS = frozenset({0x09, 0x0A, 0x0D})  # TAB, LF, CR

_C0_NAMES = {
    0x00: "NUL",
    0x01: "SOH",
    0x02: "STX",
    0x03: "ETX",
    0x04: "EOT",
    0x05: "ENQ",
    0x06: "ACK",
    0x07: "BEL",
    0x08: "BS",
    0x0B: "VT",
    0x0C: "FF",
    0x0E: "SO",
    0x0F: "SI",
    0x10: "DLE",
    0x11: "DC1",
    0x12: "DC2",
    0x13: "DC3",
    0x14: "DC4",
    0x15: "NAK",
    0x16: "SYN",
    0x17: "ETB",
    0x18: "CAN",
    0x19: "EM",
    0x1A: "SUB",
    0x1B: "ESC",
    0x1C: "FS",
    0x1D: "GS",
    0x1E: "RS",
    0x1F: "US",
    0x7F: "DEL",
}


def _is_forbidden(cp: int) -> bool:
    if cp in _ALLOWED_CONTROLS:
        return False
    return cp < 0x20 or cp == 0x7F


def _codepoint_label(cp: int) -> str:
    name = _C0_NAMES.get(cp, "CTRL")
    return f"U+{cp:04X} {name}"


def find_control_chars(text: str) -> list[tuple[int, int, int]]:
    """Return (line, column, codepoint) for each forbidden control (1-based)."""
    hits: list[tuple[int, int, int]] = []
    line = 1
    col = 1
    for ch in text:
        cp = ord(ch)
        if _is_forbidden(cp):
            hits.append((line, col, cp))
        if ch == "\n":
            line += 1
            col = 1
        else:
            col += 1
    return hits


def scan_file(path: Path) -> list[str]:
    """Return violation messages for one file (empty == clean)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"WARN governance-prose-control-chars: cannot read {path}: {exc}")
        return []
    except UnicodeDecodeError as exc:
        try:
            shown = path.relative_to(REPO)
        except ValueError:
            shown = path
        return [f"{shown}: not valid UTF-8 ({exc}) — refuse to scan"]

    try:
        shown = path.relative_to(REPO)
    except ValueError:
        shown = path

    msgs: list[str] = []
    for line, col, cp in find_control_chars(text):
        msgs.append(
            f"{shown}:{line}:{col}: stray control character {_codepoint_label(cp)} "
            f"— remove it (union-merge debris / escape mangling; do not rely on "
            f"SESSIONS repair to 'fix' form-feed)"
        )
    return msgs


def in_scope(repo: Path) -> list[Path]:
    files: list[Path] = []
    for rel in (
        "docs/SESSIONS.md",
        "docs/rejected_candidates.md",
        "docs/mc_anchor_history.md",
        "STATE.md",
    ):
        p = repo / rel
        if p.is_file():
            files.append(p)
    for sub in ("docs/adr", "docs/briefs", "docs/notes"):
        d = repo / sub
        if d.is_dir():
            files.extend(sorted(d.rglob("*.md")))
    # Stable, de-duped order
    return sorted({p.resolve(): p for p in files}.values(), key=lambda p: str(p))


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:
        paths = [Path(a) for a in argv]
    else:
        paths = in_scope(REPO)

    all_msgs: list[str] = []
    for path in paths:
        all_msgs.extend(scan_file(path))

    if all_msgs:
        print("FAIL governance-prose-control-chars:", file=sys.stderr)
        for msg in all_msgs:
            print(f"  {msg}", file=sys.stderr)
        return 1
    print(f"check_governance_prose_control_chars: OK — {len(paths)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
