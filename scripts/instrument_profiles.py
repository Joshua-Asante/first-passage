#!/usr/bin/env python3
"""instrument_profiles.py — mechanism x instrument verdict index (governance tier).

Ledgers (ops/instruments/<SYM>.md) are the SOURCE OF RECORD. Each carries an
authored `## PROFILE (machine-readable)` YAML block that INDEXES verdicts and
points at the prose rows owning the evidence — it never restates evidence.

This module:
  build  — regenerate the derived view (PROFILES.md + profiles.json)
  check  — P1 block schema / P2 mechanism-id / P3 generated-view staleness
  cell   — answer an (instrument, mechanism) consult at candidate intake

Design: docs/superpowers/specs/2026-07-25-instrument-profiles-design.md

Reads only committed text -> environment-independent (green on CI / clone).
Exit codes: 0 = clean; 1 = one or more HARD findings.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

_MECH_HEADER_RE = re.compile(r"^##\s+([a-z0-9-]+)\s*$")
_FINDING_RE = re.compile(r"^-\s+\*\*Class finding:\*\*\s*(.+)$")


@dataclass
class Mechanism:
    id: str
    definition: str
    findings: list[str] = field(default_factory=list)
    lineno: int = 0


def parse_mechanisms(path: Path) -> dict[str, Mechanism]:
    """Parse MECHANISMS.md into {id: Mechanism}.

    Definition = first non-blank *prose* line after the header. Finding-shaped
    lines (`- **Class finding:** ...`) are never promoted to definition — if an
    entry has only findings (or finding-before-prose with no later prose),
    `definition` stays empty and validate() emits a P1.
    """
    mechs: dict[str, Mechanism] = {}
    current: Mechanism | None = None
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        header = _MECH_HEADER_RE.match(line)
        if header:
            current = Mechanism(id=header.group(1), definition="", lineno=i)
            mechs[current.id] = current
            continue
        if current is None:
            continue
        finding = _FINDING_RE.match(line)
        if finding:
            current.findings.append(finding.group(1).strip())
            continue
        if line.strip() and not current.definition:
            current.definition = line.strip()
    return mechs


try:
    import yaml
except ImportError:  # pragma: no cover - environment error, never a silent skip
    sys.stderr.write(
        "FATAL: PyYAML not installed. This gate does not silently no-op "
        "(operational_rules.md 9).\n  pip install -r requirements-ops.lock\n"
    )
    raise SystemExit(2)

VERDICTS = {"DEAD", "AMBIGUOUS-PARKED", "CONTINGENT-FORWARD", "LIVE"}
BLOCKING_VERDICTS = {"DEAD", "AMBIGUOUS-PARKED", "CONTINGENT-FORWARD"}
REQUIRED_FIELDS = ("symbol", "asset_class", "venue_tradable", "k_bank_source")

_BLOCK_RE = re.compile(
    r"^##\s+PROFILE \(machine-readable\)\s*$\n+^```yaml\s*$\n(.*?)^```\s*$",
    re.M | re.S,
)
_NO_PROFILE_RE = re.compile(r"<!--\s*no-profile:.*?-->")


@dataclass
class Finding:
    path: str
    lineno: int
    code: str
    message: str
    severity: str = "HARD"

    def __str__(self) -> str:
        return f"{self.severity}: {self.path}:{self.lineno}: {self.code} {self.message}"


@dataclass
class Cell:
    mechanism: str
    verdict: str
    date: str
    source: str


@dataclass
class Profile:
    symbol: str
    asset_class: str
    family: list[str]
    venue_tradable: bool
    venue_note: str | None
    k_bank_source: str | None
    cost_hurdle: dict | None
    cells: list[Cell]
    bars: list[dict]
    structure: list[dict]
    path: Path
    lineno: int


def extract_block(text: str) -> tuple[str | None, int]:
    """Return (yaml_body, 1-indexed start line) or (None, 0)."""
    m = _BLOCK_RE.search(text)
    if not m:
        return None, 0
    return m.group(1), text[: m.start(1)].count("\n") + 1


def has_no_profile_marker(text: str) -> bool:
    return bool(_NO_PROFILE_RE.search(text))


def _rel(path: Path) -> str:
    """Repo-relative posix path for findings; falls back to the plain posix
    path when `path` is outside the repo (pytest tmp_path fixtures)."""
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_profiles(instruments_dir: Path) -> tuple[list[Profile], list[Finding]]:
    profiles: list[Profile] = []
    findings: list[Finding] = []
    for path in sorted(instruments_dir.glob("*.md")):
        if path.name in {"MECHANISMS.md", "PROFILES.md"}:
            continue
        rel = _rel(path)
        text = path.read_text(encoding="utf-8")
        body, lineno = extract_block(text)
        if body is None:
            if not has_no_profile_marker(text):
                findings.append(Finding(rel, 1, "P1", "no PROFILE block and no no-profile marker"))
            continue
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as exc:
            findings.append(Finding(rel, lineno, "P1", f"YAML does not parse: {exc.__class__.__name__}"))
            continue
        if not isinstance(data, dict):
            findings.append(Finding(rel, lineno, "P1", "PROFILE block is not a mapping"))
            continue
        missing = [f for f in REQUIRED_FIELDS if f not in data]
        if missing:
            findings.append(Finding(rel, lineno, "P1", f"missing required field(s): {', '.join(missing)}"))
            continue
        if not isinstance(data["venue_tradable"], bool):
            findings.append(
                Finding(
                    rel,
                    lineno,
                    "P1",
                    f"venue_tradable must be a bool, got {data['venue_tradable']!r}",
                )
            )
            continue
        if not isinstance(data["k_bank_source"], str) or not data["k_bank_source"].strip():
            findings.append(
                Finding(
                    rel,
                    lineno,
                    "P1",
                    f"k_bank_source must be a non-empty string, got {data['k_bank_source']!r}",
                )
            )
            continue
        cells: list[Cell] = []
        for raw in data.get("cells") or []:
            verdict = raw.get("verdict")
            if verdict not in VERDICTS:
                findings.append(
                    Finding(rel, lineno, "P1", f"verdict {verdict!r} not in {sorted(VERDICTS)}")
                )
                continue
            cells.append(
                Cell(
                    mechanism=raw.get("mechanism", ""),
                    verdict=verdict,
                    date=str(raw.get("date", "")),
                    source=raw.get("source", ""),
                )
            )
        profiles.append(
            Profile(
                symbol=data["symbol"],
                asset_class=data["asset_class"],
                family=list(data.get("family") or []),
                venue_tradable=data["venue_tradable"],
                venue_note=data.get("venue_note"),
                k_bank_source=data["k_bank_source"],
                cost_hurdle=data.get("cost_hurdle"),
                cells=cells,
                bars=list(data.get("bars") or []),
                structure=list(data.get("structure") or []),
                path=path,
                lineno=lineno,
            )
        )
    return profiles, findings


def _resolve(source: str, profile: Profile) -> bool:
    """True if a source pointer resolves. Anchor-only (#X) sources are in-file.

    Empty / missing source is NOT vacuously resolved — an unsourced claim must
    fail the gate (ADR forbidden-moves: blocks never carry an unsourced claim).
    """
    if not source:
        return False
    if source.startswith("#"):
        return True
    return (profile.path.parent / source.split("#")[0]).exists()


# Labelled verdict-date fields used by this repo's decision artifacts.
#
# Two shape details, each of which silently disarms the check if missed:
#   1. The colon sits INSIDE the bold (`**Closed:** 2026-07-21`). A pattern
#      expecting `**Closed**:` matches almost nothing.
#   2. The date is not always adjacent to the label — this repo also writes
#      `**Status:** CLOSED — FALSIFIED 2026-07-21`, a genuine self-dated verdict
#      with prose between the two. So the date is matched anywhere on the
#      label's own line (bounded, non-greedy, single-line).
# Widening to same-line was measured before landing: it converted 2 advisory
# NOTEs into fully-checked cells and fired ZERO new P4s across all 47 cells.
LABEL_RE = re.compile(
    r"\*\*(Closed|Closure date|Decision date|Lock date|Date|Run|Ratified|Accepted"
    r"|Status|Disposition|Verdict)\s*:?\s*\*\*[^\n]{0,120}?(\d{4}-\d{2}-\d{2})",
    re.I,
)


def _check_date_provenance(cell: Cell, prof: Profile, rel: str) -> list[Finding]:
    """A cell's `date` must be findable in that row's OWN cited source.

    Five defects of this class were caught by human review during the build --
    a date taken from a tool-deletion event, one from an unrelated venue
    closure, one whose cited source carried no date at all (ADR 2026-07-25
    execution note 1). Three tiers, deliberately scoped:

      P4 (HARD)  source declares EXACTLY ONE labelled verdict date and the
                 cell disagrees with it.
      P5 (HARD)  source declares NO labelled date and the cell's date does not
                 appear anywhere in it -- unverifiable from what it cites.
      NOTE       source declares no labelled verdict date at all. Advisory:
                 prefer a record that self-dates its verdict.

    A multi-entry registry (many labelled dates) gets the P5 fallback only,
    never P4: picking "the right" date out of it needs semantics, which is the
    exact mistake the status-consistency checker's C1 was dropped for (100%
    false-positive on real data). Anchor-only sources resolve to the ledger
    itself, get the P5 fallback, and are exempt from the NOTE -- a ledger row
    is not a decision artifact, so the note would fire on every one as noise.
    """
    source = cell.source
    if not source:
        return []  # already a P1 from _resolve; do not double-report
    anchor_only = source.startswith("#")
    target = prof.path if anchor_only else (prof.path.parent / source.split("#")[0])
    if not target.exists():
        return []  # already a P1 from _resolve
    text = normalize(target.read_text(encoding="utf-8", errors="replace"))
    declared = {m.group(2) for m in LABEL_RE.finditer(text)}

    if len(declared) == 1 and not anchor_only:
        only = next(iter(declared))
        if cell.date != only:
            return [Finding(
                rel, prof.lineno, "P4",
                f"cell {cell.mechanism!r} dated {cell.date} but its source declares "
                f"{only} ({source}) — the date must be the one that source states",
            )]
        return []

    out: list[Finding] = []
    if cell.date not in text:
        out.append(Finding(
            rel, prof.lineno, "P5",
            f"cell {cell.mechanism!r} dated {cell.date}, which does not appear in its "
            f"source ({source}) — unverifiable as cited; point at a record that "
            "self-dates its verdict",
        ))
    if not declared and not anchor_only:
        out.append(Finding(
            rel, prof.lineno, "P5-WEAK",
            f"source for {cell.mechanism!r} ({source}) declares no verdict date — "
            "prefer a closure/scoping/ADR record that self-dates its verdict over a "
            "RESULTS.md carrying only numbers",
            severity="NOTE",
        ))
    return out


def validate(
    profiles: list[Profile], mechanisms: dict[str, Mechanism], repo_root: Path
) -> list[Finding]:
    findings: list[Finding] = []
    mech_path = _rel(repo_root / "ops" / "instruments" / "MECHANISMS.md")
    for mid, mech in mechanisms.items():
        if not mech.definition.strip():
            findings.append(
                Finding(
                    mech_path,
                    mech.lineno,
                    "P1",
                    f"mechanism {mid!r} has no prose definition",
                )
            )
    known = sorted(mechanisms)
    for prof in profiles:
        rel = _rel(prof.path)
        seen: set[str] = set()
        for cell in prof.cells:
            # One verdict per (instrument, mechanism): the generated index keys on
            # that pair, so a second row would silently overwrite the first.
            if cell.mechanism in seen:
                findings.append(
                    Finding(rel, prof.lineno, "P1",
                            f"duplicate cell for mechanism {cell.mechanism!r} — one verdict "
                            "per (instrument, mechanism); record the terminal verdict and "
                            "link the closure covering the earlier study")
                )
            seen.add(cell.mechanism)
            if cell.mechanism not in mechanisms:
                near = difflib.get_close_matches(cell.mechanism, known, n=1, cutoff=0.6)
                hint = f" — nearest: {near[0]!r}" if near else " — declare it NEW in MECHANISMS.md"
                findings.append(
                    Finding(rel, prof.lineno, "P2", f"unknown mechanism {cell.mechanism!r}{hint}")
                )
            if not _resolve(cell.source, prof):
                findings.append(
                    Finding(rel, prof.lineno, "P1", f"source {cell.source!r} does not resolve")
                )
            else:
                findings.extend(_check_date_provenance(cell, prof, rel))
        for kind, extras in (("bars", prof.bars), ("structure", prof.structure)):
            for extra in extras:
                src = extra.get("source", "")
                if not (isinstance(src, str) and src.strip()):
                    findings.append(
                        Finding(
                            rel,
                            prof.lineno,
                            "P1",
                            f"{kind} entry missing non-empty source",
                        )
                    )
                elif not _resolve(src, prof):
                    findings.append(
                        Finding(rel, prof.lineno, "P1", f"source {src!r} does not resolve")
                    )
        if prof.cost_hurdle and not _resolve(prof.cost_hurdle.get("source", ""), prof):
            findings.append(
                Finding(rel, prof.lineno, "P1", "cost_hurdle.source does not resolve")
            )
    return findings


VERDICT_INITIAL = {"DEAD": "D", "AMBIGUOUS-PARKED": "A", "CONTINGENT-FORWARD": "F", "LIVE": "L"}

GENERATED_HEADER = """# INSTRUMENT PROFILES — mechanism x instrument verdict index

> **GENERATED — do not hand-edit; source = ledger PROFILE blocks.**
> Regenerate: `python scripts/instrument_profiles.py build`
> Source of record is always `ops/instruments/<SYM>.md`.
"""


def _md_cell(value: object) -> str:
    """Make a value safe to interpolate into a markdown table cell.

    Escapes ``|`` so it cannot inject a spurious column, and collapses any
    newline sequence (``\\r\\n`` / ``\\n`` / ``\\r``) to a single space so it
    cannot inject arbitrary markdown lines (headings, new rows, etc.) into
    the generated file. `source` values in particular can be unconstrained
    free text — an anchor pointer (`#X`) bypasses the filesystem existence
    check entirely, so a YAML authoring slip can put anything into it.

    Backslashes must be escaped *before* pipes. CommonMark backslash-escapes
    pair left-to-right, so escaping ``|`` -> ``\\|`` without first doubling
    any pre-existing backslash lets a value ending in an odd run of
    backslashes (e.g. ``...sec\\|injected``) re-form a live, unescaped pipe
    once the naive replace runs (the backslash count becomes even) — the
    escape is defeated and the pipe still opens a spurious column.
    """
    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    return text


def inherited_bars(profile: Profile, by_symbol: dict[str, Profile]) -> list[dict]:
    """Bars declared on this profile's family parents, deduped by id, sorted."""
    seen: dict[str, dict] = {}
    for parent_symbol in profile.family:
        parent = by_symbol.get(parent_symbol)
        if parent is None:
            continue
        for bar in parent.bars:
            seen.setdefault(bar.get("id", ""), bar)
    return [seen[k] for k in sorted(seen)]


def build_view(profiles: list[Profile], mechanisms: dict[str, Mechanism]) -> tuple[str, str]:
    profs = sorted(profiles, key=lambda p: p.symbol)
    by_symbol = {p.symbol: p for p in profs}
    symbols = [p.symbol for p in profs]

    index: dict[str, dict[str, Cell]] = {}
    for prof in profs:
        for cell in prof.cells:
            index.setdefault(prof.symbol, {})[cell.mechanism] = cell

    lines = [GENERATED_HEADER, "\n## Matrix\n"]
    lines.append("| Mechanism | " + " | ".join(_md_cell(s) for s in symbols) + " |")
    lines.append("|---" * (len(symbols) + 1) + "|")
    for mech_id in sorted(mechanisms):
        row = []
        for symbol in symbols:
            cell = index.get(symbol, {}).get(mech_id)
            row.append(VERDICT_INITIAL[cell.verdict] if cell else ".")
        lines.append(f"| {_md_cell(mech_id)} | " + " | ".join(row) + " |")
    lines.append("\nLegend: D=DEAD · A=AMBIGUOUS-PARKED · F=CONTINGENT-FORWARD · L=LIVE · `.`=untested\n")

    for mech_id in sorted(mechanisms):
        mech = mechanisms[mech_id]
        lines.append(f"\n## {mech_id}\n")
        lines.append(mech.definition or "_no definition_")
        for finding in mech.findings:
            lines.append(f"\n- **Class finding:** {finding}")
        rows = [(s, index[s][mech_id]) for s in symbols if mech_id in index.get(s, {})]
        if rows:
            lines.append("\n| Instrument | Verdict | Date | Source |")
            lines.append("|---|---|---|---|")
            for symbol, cell in rows:
                lines.append(
                    f"| {_md_cell(symbol)} | {_md_cell(cell.verdict)} | {_md_cell(cell.date)} "
                    f"| {_md_cell(cell.source)} |"
                )
        else:
            lines.append("\n_No instrument has a recorded verdict on this mechanism._")
        lines.append("")

    # Cells whose mechanism is absent from MECHANISMS.md never appear above —
    # the matrix and per-mechanism sections are driven by the registered
    # vocabulary (`sorted(mechanisms)`), not by what ledgers actually declare.
    # Surface them explicitly instead of silently dropping them from the
    # human-facing view while they still appear in the JSON `cells` payload.
    unrecognized = sorted(
        (
            (prof.symbol, cell)
            for prof in profs
            for cell in prof.cells
            if cell.mechanism not in mechanisms
        ),
        key=lambda t: (t[0], t[1].mechanism),
    )
    if unrecognized:
        lines.append("\n## Unrecognized mechanisms\n")
        lines.append(
            "These cells reference a `mechanism` id that is absent from `MECHANISMS.md`. "
            "They are excluded from the matrix and per-mechanism sections above (which are "
            "driven by the registered vocabulary), but they still appear in `profiles.json`. "
            "`check` reports each of these as a P2 finding."
        )
        lines.append("\n| Instrument | Mechanism | Verdict | Date | Source |")
        lines.append("|---|---|---|---|---|")
        for symbol, cell in unrecognized:
            lines.append(
                f"| {_md_cell(symbol)} | {_md_cell(cell.mechanism)} | {_md_cell(cell.verdict)} "
                f"| {_md_cell(cell.date)} | {_md_cell(cell.source)} |"
            )
        lines.append("")

    payload = {
        "generated_by": "scripts/instrument_profiles.py",
        "mechanisms": {
            m: {"definition": mechanisms[m].definition, "findings": mechanisms[m].findings}
            for m in sorted(mechanisms)
        },
        "instruments": {
            p.symbol: {
                "asset_class": p.asset_class,
                "family": sorted(p.family),
                "venue_tradable": p.venue_tradable,
                "venue_note": p.venue_note,
                "k_bank_source": p.k_bank_source,
                "cost_hurdle": p.cost_hurdle,
                "bars": sorted(p.bars, key=lambda b: b.get("id", "")),
                "inherited_bars": inherited_bars(p, by_symbol),
                "structure": p.structure,
                "ledger": _rel(p.path),
            }
            for p in profs
        },
        "cells": {
            p.symbol: {
                c.mechanism: {"verdict": c.verdict, "date": c.date, "source": c.source}
                for c in sorted(p.cells, key=lambda c: c.mechanism)
            }
            for p in profs
        },
    }
    return "\n".join(lines).rstrip("\n") + "\n", json.dumps(payload, indent=2, sort_keys=True) + "\n"


def normalize(text: str) -> str:
    """CRLF-insensitive compare — this repo checks out CRLF on Windows."""
    return text.replace("\r\n", "\n")


def _paths(repo_root: Path) -> tuple[Path, Path, Path, Path]:
    inst = repo_root / "ops" / "instruments"
    return inst, inst / "MECHANISMS.md", inst / "PROFILES.md", inst / "profiles.json"


def _write(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def cmd_build(repo_root: Path) -> int:
    inst, mech_path, md_path, json_path = _paths(repo_root)
    if not mech_path.exists():
        # parse_mechanisms() does path.read_text() unconditionally -- guard
        # here rather than let a missing controlled-vocabulary file surface
        # as an uncaught FileNotFoundError traceback. Report it through the
        # same Finding path every other defect uses, and stop: falling back
        # to an empty vocabulary would make every mechanism id look
        # unregistered and cascade into a pile of misleading P2 findings.
        finding = Finding(_rel(mech_path), 1, "P1",
                           f"vocabulary file not found: {mech_path.as_posix()} — "
                           "MECHANISMS.md is required to build/check")
        print(finding)
        print("\nBuild aborted: 1 finding(s). Fix them, then rebuild.")
        return 1
    mechanisms = parse_mechanisms(mech_path)
    profiles, findings = load_profiles(inst)
    # Deviation from the brief: `load_profiles` only surfaces P1 block-schema
    # findings. Without also running `validate()` here, `build` would happily
    # generate a view from a ledger referencing a mechanism id absent from
    # MECHANISMS.md (P2) or a dangling source pointer (P1) — a build that
    # "succeeds" but whose output a subsequent `check` immediately flags.
    # The invariant this CLI owns: a build that returns 0 is always a build
    # whose inputs would pass `check`.
    findings += validate(profiles, mechanisms, repo_root)
    # NOTEs are advisory: they are printed but never abort a build, exactly as
    # in cmd_check. Letting one block here would make the whole tier a hard
    # gate by the back door.
    notes = [f for f in findings if f.severity == "NOTE"]
    findings = [f for f in findings if f.severity != "NOTE"]
    for note in notes:
        print(note)
    if findings:
        for finding in findings:
            print(finding)
        print(f"\nBuild aborted: {len(findings)} finding(s). Fix them, then rebuild.")
        return 1
    md, js = build_view(profiles, mechanisms)
    _write(md_path, md)
    _write(json_path, js)
    print(f"instrument_profiles: wrote {md_path.as_posix()} + {json_path.as_posix()} "
          f"({len(profiles)} ledger(s))")
    return 0


def cmd_check(repo_root: Path) -> int:
    inst, mech_path, md_path, json_path = _paths(repo_root)
    if not mech_path.exists():
        # Same guard as cmd_build (see its comment): fail clean through the
        # ordinary Finding-reporting path instead of an uncaught
        # FileNotFoundError, and stop before load_profiles/validate can
        # cascade unregistered-mechanism P2 findings off an empty vocabulary.
        finding = Finding(_rel(mech_path), 1, "P1",
                           f"vocabulary file not found: {mech_path.as_posix()} — "
                           "MECHANISMS.md is required to build/check")
        print(finding)
        print("\ninstrument_profiles: 1 HARD finding(s).")
        return 1
    mechanisms = parse_mechanisms(mech_path)
    profiles, findings = load_profiles(inst)
    findings += validate(profiles, mechanisms, repo_root)

    # NOTEs are advisory and never gate a commit — a check that cries wolf stops
    # being read. They also must not suppress the P3 comparison below.
    notes = [f for f in findings if f.severity == "NOTE"]
    findings = [f for f in findings if f.severity != "NOTE"]

    if not findings:
        # Only reach the P3 comparison once P1/P2 are clean — comparing
        # against a view built from invalid input would produce a
        # confusing cascade (a stale-view finding on top of the real defect).
        md, js = build_view(profiles, mechanisms)
        for path, expected in ((md_path, md), (json_path, js)):
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            if normalize(actual) != normalize(expected):
                findings.append(
                    Finding(path.as_posix(), 1, "P3",
                            "generated view is stale — run: python scripts/instrument_profiles.py build")
                )
    for finding in findings:
        print(finding)
    for note in notes:
        print(note)
    if findings:
        print(f"\ninstrument_profiles: {len(findings)} HARD finding(s), {len(notes)} note(s).")
        return 1
    print(f"instrument_profiles: OK - {len(profiles)} ledger(s), "
          f"{sum(len(p.cells) for p in profiles)} cell(s), view current.")
    return 0


CONSULT_NOTE = {
    "DEAD": "BLOCKING — the re-proposal bar below must be met and addressed in the pre-registration.",
    "AMBIGUOUS-PARKED": "BLOCKING — a parked concept holds this cell and shares the instrument's "
                        "anti-SNAG budget; address it (and any decision date) in the pre-registration.",
    "CONTINGENT-FORWARD": "BLOCKING — a frozen forward test is running on this cell; a second "
                          "candidate here is the FM#3 collision class.",
    "LIVE": "NOTE — an authorized leg occupies this cell; if a live book exists, new work must clear the book-correlation gate — check `venue_note` first, as an authorized leg may have no venue",
}


def cmd_cell(repo_root: Path, symbol: str, mechanism: str) -> int:
    _, _, _, json_path = _paths(repo_root)
    if not json_path.exists():
        print(f"FATAL: {json_path.as_posix()} missing — run: python scripts/instrument_profiles.py build")
        return 2
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if symbol not in data["instruments"]:
        print(f"FATAL: no ledger for {symbol!r}. Known: {', '.join(sorted(data['instruments']))}")
        return 2
    if mechanism not in data["mechanisms"]:
        near = difflib.get_close_matches(mechanism, sorted(data["mechanisms"]), n=1, cutoff=0.6)
        hint = f" Nearest: {near[0]!r}." if near else ""
        print(f"FATAL: unknown mechanism {mechanism!r}.{hint} Declare it NEW in MECHANISMS.md.")
        return 2

    inst = data["instruments"][symbol]
    cell = data["cells"].get(symbol, {}).get(mechanism)
    print(f"=== {symbol} x {mechanism} ===")
    print(f"ledger: {inst['ledger']}")
    if not inst["venue_tradable"]:
        print(f"venue: NOT TRADABLE at the live firm — {inst.get('venue_note') or 'see ledger'}")
    if cell:
        print(f"verdict: {cell['verdict']} ({cell['date']})\n  source: {cell['source']}")
        print(f"  {CONSULT_NOTE[cell['verdict']]}")
    else:
        print("verdict: untested — no prior on this cell.")
    for finding in data["mechanisms"][mechanism]["findings"]:
        print(f"class finding (mechanism-wide, not specific to {symbol}): {finding}")
    for bar in inst["bars"] + inst["inherited_bars"]:
        print(f"BINDING BAR: {bar.get('id')} -> {bar.get('source')}")
    if inst.get("cost_hurdle"):
        hurdle = inst["cost_hurdle"]
        print(f"cost hurdle: {hurdle.get('value')} {hurdle.get('units')} "
              f"({hurdle.get('basis')}) — VERIFY at {hurdle.get('source')}")
    print(f"K bank: read {inst.get('k_bank_source')} — never trust a snapshot.")
    for item in inst["structure"]:
        print(f"prior: {item.get('claim')} [{item.get('source')}]")

    blocking = bool(cell and cell["verdict"] in BLOCKING_VERDICTS) or bool(
        inst["bars"] + inst["inherited_bars"]
    )
    return 1 if blocking else 0


def main(argv: list[str] | None = None) -> int:
    # `cell` prints ledger/MECHANISMS.md prose verbatim (em dashes, minus
    # signs, arrows, etc.). Windows consoles/pipes default stdout/stderr to
    # the ANSI code page (cp1252 here), which cannot encode that text and
    # raises UnicodeEncodeError mid-print -- discovered via the real-data
    # verification run (`cell MYM opening-range-continuation`), not a
    # fixture, since the synthetic test prose is pure ASCII. Force UTF-8 with
    # a non-fatal fallback so a consult command never crashes on the exact
    # ledger content it exists to surface.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("build", "check", "cell"))
    parser.add_argument("args", nargs="*", help="for 'cell': <SYMBOL> <mechanism-id>")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args(argv)
    if args.command == "cell":
        if len(args.args) != 2:
            parser.error("cell requires: <SYMBOL> <mechanism-id>")
        return cmd_cell(args.repo_root, args.args[0], args.args[1])
    return {"build": cmd_build, "check": cmd_check}[args.command](args.repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
