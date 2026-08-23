#!/usr/bin/env python3
"""Look up the Rule 7 owner for a path or token. Not a second owner table.

Reads docs/operational_rules.md §7 first. Falls back to the blast-radius
sweep checklist (labeled, not a second owner). Prints the matching row
and a pointer. Does not restate owned constants.

Exit 0 on a hit; exit 1 with "no owner" when nothing matches.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULE7 = REPO / "docs" / "operational_rules.md"
SURFACES = (
    REPO / ".claude" / "skills" / "blast-radius" / "references" / "owner-surfaces.md"
)

_TABLE_ROW = re.compile(r"^\| (?!Fact class)(?!---)(?P<klass>.+?) \| (?P<owner>.+?) \|$")
_MIRROR_BULLET = re.compile(r"^- `?(?P<token>[^`—]+)`? — (?P<note>.+)$")


def _norm(s: str) -> str:
    return re.sub(r"[`*_]", "", s).strip().casefold()


def _tokens(s: str) -> set[str]:
    text = _norm(s)
    out = {text}
    for part in re.split(r"[\s/,|]+", text):
        part = part.strip(" .;:")
        if part:
            out.add(part)
            out.add(Path(part).name)
    return {t for t in out if t}


def _query_keys(q: str) -> set[str]:
    q = q.strip().strip("`")
    keys = _tokens(q)
    keys.add(_norm(q))
    keys.add(_norm(Path(q).name))
    return {k for k in keys if k}


def _parse_table(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for raw in text.splitlines():
        m = _TABLE_ROW.match(raw.rstrip())
        if m:
            rows.append((m.group("klass").strip(), m.group("owner").strip()))
    return rows


def _rule7_section(text: str) -> str:
    m = re.search(
        r"^## 7\. One canonical owner.*?(?=^## |\Z)",
        text,
        re.M | re.S,
    )
    return m.group(0) if m else ""


def _surfaces_mirrors(text: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    section = None
    for raw in text.splitlines():
        if raw.startswith("## Must-not-restate"):
            section = "mirrors"
            continue
        if raw.startswith("## "):
            section = None
            continue
        if section != "mirrors":
            continue
        m = _MIRROR_BULLET.match(raw.strip())
        if m:
            rows.append((m.group("token").strip(), m.group("note").strip()))
    return rows


def _score(query_keys: set[str], klass: str, owner: str) -> int:
    hay = _tokens(klass) | _tokens(owner)
    score = 0
    for k in query_keys:
        if len(k) < 3:
            continue
        if k in hay:
            score += 3
            continue
        # Path-like containment only (avoid "a"/"no" substring hits).
        if len(k) >= 8:
            for h in hay:
                if len(h) >= 8 and (k in h or h in k):
                    score += 2
                    break
    return score


def lookup(query: str) -> tuple[str, str, str] | None:
    """Return (fact_class, owner, source_label) or None."""
    rule7 = RULE7.read_text(encoding="utf-8")
    keys = _query_keys(query)
    best: tuple[int, str, str, str] | None = None

    def consider(klass: str, owner: str, source: str, bonus: int = 0) -> None:
        nonlocal best
        raw = _score(keys, klass, owner)
        if raw <= 0:
            return
        s = raw + bonus
        if best is None or s > best[0]:
            best = (s, klass, owner, source)

    for klass, owner in _parse_table(_rule7_section(rule7)):
        consider(klass, owner, "docs/operational_rules.md §7", bonus=1)

    if SURFACES.is_file():
        surf = SURFACES.read_text(encoding="utf-8")
        for klass, owner in _parse_table(surf):
            consider(
                klass,
                owner,
                ".claude/skills/blast-radius/references/owner-surfaces.md "
                "(sweep checklist; §7 is the owner table)",
            )
        for token, note in _surfaces_mirrors(surf):
            consider(
                token,
                f"labeled mirror — {note}",
                ".claude/skills/blast-radius/references/owner-surfaces.md "
                "(must-not-restate; not a second owner)",
            )

    if best is None:
        return None
    return best[1], best[2], best[3]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("query", help="path or token (e.g. dd_protection, SESSIONS.md)")
    args = ap.parse_args(argv)
    hit = lookup(args.query)
    if hit is None:
        print("no owner")
        return 1
    klass, owner, source = hit
    print(f"class: {klass}")
    print(f"owner: {owner}")
    print(f"source: {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
