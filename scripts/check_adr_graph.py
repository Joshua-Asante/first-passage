#!/usr/bin/env python3
"""check_adr_graph.py — ADR lifecycle graph gate (governance tier).

Enforces header Status vocabulary, supersession edge integrity (Accepted
successors only), cold-store stub shape, derived INDEX sync, (when
enabled) age+graph prune, and A8 intra-ADR running-count consistency.
CI verifies only — never mutates ADR bodies.

Design: docs/superpowers/specs/2026-07-17-adr-lifecycle-graph-design.md
"""
from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

STATUS_TOKENS = frozenset(
    {"Proposed", "Accepted", "Superseded", "Withdrawn", "Retired"}
)
COLD_TOKENS = frozenset({"Superseded", "Withdrawn", "Retired"})
AGE_MONTHS = 6
STUB_MAX_LINES = 40
# INDEX notes column is a pointer, not a restatement of the ADR Status
# annotation. 40 words matches the W5 / STATE entry-class cap
# (docs/adr/2026-08-07-w5-governance-diet.md). Full annotation stays on
# the ADR. Display-only — A1/A2 still parse the unclipped header.
INDEX_NOTES_MAX_WORDS = 40
INDEX_NOTES_ELLIPSIS = " …"
DEFAULT_ENABLED_CHECKS: frozenset[str] = frozenset(
    {"A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"}
)
VALID_CHECKS: frozenset[str] = frozenset({"A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"})

HEADER_END_RE = re.compile(r"^(## |---\s*$)")
FIELD_RE = re.compile(r"^\*\*(Status|Decision date|Supersedes|Superseded-by|"
                      r"Superseded-in-part-by|Retain-until):\*\*\s*(.*)$")
STATUS_TICK_RE = re.compile(
    r"^`(?P<tok>[^`]+)`(?:\s*[—–-]\s*(?P<ann>.*))?$"
)
STATUS_BARE_RE = re.compile(
    r"^(?P<tok>[A-Za-z][\w/-]*)(?:\s*[—–-]\s*(?P<ann>.*)|\s+(?P<paren>\(.*)|$)"
)
ADR_FILE_RE = re.compile(
    r"^`(?P<file>\d{4}-\d{2}-\d{2}[a-z]?-[^`]+?\.md)`"
    r"(?:\s+(?P<scope>full|in part)(?:\s*[—–-]\s*(?P<clause>.*))?)?$"
)
EVENT_RE = re.compile(
    r"^`event:(?P<id>[A-Za-z0-9._-]+)`(?:\s*[—–-]\s*(?P<note>.*))?$"
)
# A Supersedes/Superseded-by/Superseded-in-part-by value written as a markdown
# link ([`file.md`](file.md) ...) instead of a bare code span (`file.md` ...).
# Both are valid citation style elsewhere in this corpus, but parse_edge_value
# only recognized the bare form -- the link form silently returned None and the
# edge was dropped with no finding, rather than being flagged unparseable.
# Real incident (2026-07-22): the withdrawal ADR's `Supersedes: [`...`](...) in
# part` line parsed to nothing, so A2 never required the four-firms ADR to carry
# the reciprocal Superseded-in-part-by -- the graph was silently blind to a real,
# declared supersession. check_adr_graph reported OK while STATE.md separately
# drifted on the same fact. Normalize to the bare-backtick form and fall through
# to the existing logic unchanged.
MD_LINK_PREFIX_RE = re.compile(
    r"^\[`(?P<file>\d{4}-\d{2}-\d{2}[a-z]?-[^`]+?\.md)`\]\([^)]*\)\s*(?P<rest>.*)$"
)
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})$")

# Canonical token aliases for M1 / bare Status lines
STATUS_ALIASES = {
    "accepted": "Accepted",
    "proposed": "Proposed",
    "superseded": "Superseded",
    "withdrawn": "Withdrawn",
    "retired": "Retired",
    "locked": "Accepted",  # LOCKED provenance → Accepted token
    "superseded-by-merge": "Accepted",  # pair with event: in migration
    "withdrawn/superseded": "Superseded",
}


@dataclass(frozen=True)
class EdgeTarget:
    kind: str          # "adr" | "event"
    target: str        # filename or event id
    scope: str | None  # "full" | "in_part" | None
    clause: str
    lineno: int


@dataclass(frozen=True)
class AdrHeader:
    path: str
    status: str
    status_annotation: str
    decision_date: date | None
    supersedes: tuple[EdgeTarget, ...]
    superseded_by: tuple[EdgeTarget, ...]
    superseded_in_part_by: tuple[EdgeTarget, ...]
    retain_until: date | None
    header_end_lineno: int
    raw_status_lineno: int
    missing_fields: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    surface: str
    lineno: int
    message: str


def header_region(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    end = 0
    for i, line in enumerate(lines, start=1):
        if i > 1 and HEADER_END_RE.match(line):
            break
        out.append(line)
        end = i
    return "\n".join(out), end


def parse_status_token(value: str) -> tuple[str | None, str]:
    value = value.strip()
    m = STATUS_TICK_RE.match(value)
    if m:
        raw = m.group("tok").strip()
        ann = (m.group("ann") or "").strip()
    else:
        m2 = STATUS_BARE_RE.match(value)
        if not m2:
            return None, ""
        raw = m2.group("tok").strip()
        ann = (m2.group("ann") or m2.group("paren") or "").strip()
    # Strip trailing annotation glued without dash: "Accepted (foo)"
    if "(" in raw and raw.endswith(")"):
        raw, _, rest = raw.partition(" ")
        if rest:
            ann = (rest + (" " + ann if ann else "")).strip()
    key = raw.lower().replace(" ", "")
    # Handle "Withdrawn/Superseded" and "SUPERSEDED-BY-MERGE"
    if key.startswith("superseded-by-merge") or key.startswith("supersededbymerge"):
        return "Accepted", ann or raw
    if "withdrawn/superseded" in key or key == "withdrawn/superseded":
        return "Superseded", ann or raw
    if key.startswith("superseded"):
        # "SUPERSEDED-BY: file" → token Superseded; file belongs in field migration
        return "Superseded", ann or raw
    if key.startswith("retired"):
        return "Retired", ann or raw
    if key.startswith("withdrawn"):
        return "Withdrawn", ann or raw
    if key.startswith("proposed"):
        return "Proposed", ann or raw
    if key.startswith("locked"):
        return "Accepted", ann or raw
    if key.startswith("accepted"):
        return "Accepted", ann or raw
    tok = STATUS_ALIASES.get(raw.lower())
    return tok, ann


def parse_edge_value(field: str, value: str, lineno: int) -> EdgeTarget | None:
    value = value.strip()
    if value.lower() == "none" or value == "":
        return None
    md_link = MD_LINK_PREFIX_RE.match(value)
    if md_link:
        rest = md_link.group("rest").strip()
        value = f"`{md_link.group('file')}`" + (f" {rest}" if rest else "")
    if field == "Superseded-in-part-by":
        em = EVENT_RE.match(value)
        if em:
            return EdgeTarget("event", em.group("id"), "in_part",
                              (em.group("note") or "").strip(), lineno)
    m = ADR_FILE_RE.match(value)
    if not m:
        # bare filename without scope for Superseded-by / in-part-by + clause
        m2 = re.match(
            r"^`(?P<file>\d{4}-\d{2}-\d{2}[a-z]?-[^`]+?\.md)`"
            r"(?:\s*(?:[-\u2014]\s*(?P<clause>.*))?)?\s*$",
            value,
        )
        if m2 and field in {"Superseded-by", "Superseded-in-part-by"}:
            scope = "in_part" if field == "Superseded-in-part-by" else None
            return EdgeTarget(
                "adr", m2.group("file"), scope,
                (m2.group("clause") or "").strip(), lineno)
        return None
    scope_raw = m.group("scope")
    scope = None
    if scope_raw == "full":
        scope = "full"
    elif scope_raw == "in part":
        scope = "in_part"
    elif field == "Supersedes":
        return None  # Supersedes requires explicit scope
    elif field == "Superseded-in-part-by":
        scope = "in_part"
    return EdgeTarget("adr", m.group("file"), scope,
                      (m.group("clause") or "").strip(), lineno)


def _parse_date(value: str) -> date | None:
    value = value.strip()
    if value.lower() == "none" or not value:
        return None
    m = DATE_RE.match(value)
    if not m:
        return None
    return date.fromisoformat(m.group(1))


def parse_adr_header(path: str, text: str) -> AdrHeader:
    region, end = header_region(text)
    status = ""
    status_ann = ""
    status_lineno = 1
    decision_date: date | None = None
    retain_until: date | None = None
    supersedes: list[EdgeTarget] = []
    superseded_by: list[EdgeTarget] = []
    in_part: list[EdgeTarget] = []
    saw = {k: False for k in (
        "Status", "Decision date", "Supersedes", "Superseded-by",
        "Superseded-in-part-by", "Retain-until")}

    for i, line in enumerate(region.splitlines(), start=1):
        m = FIELD_RE.match(line)
        if not m:
            continue
        field, val = m.group(1), m.group(2).strip()
        saw[field] = True
        if field == "Status":
            tok, ann = parse_status_token(val)
            status = tok or ""
            status_ann = ann
            status_lineno = i
        elif field == "Decision date":
            decision_date = _parse_date(val)
        elif field == "Retain-until":
            retain_until = _parse_date(val)
        elif field == "Supersedes":
            if val.lower() != "none":
                e = parse_edge_value(field, val, i)
                if e:
                    supersedes.append(e)
        elif field == "Superseded-by":
            if val.lower() != "none":
                e = parse_edge_value(field, val, i)
                if e:
                    superseded_by.append(e)
        elif field == "Superseded-in-part-by":
            if val.lower() != "none":
                e = parse_edge_value(field, val, i)
                if e:
                    in_part.append(e)

    missing_fields = tuple(k for k, v in saw.items() if not v)

    return AdrHeader(
        path=path,
        status=status,
        status_annotation=status_ann,
        decision_date=decision_date,
        supersedes=tuple(supersedes),
        superseded_by=tuple(superseded_by),
        superseded_in_part_by=tuple(in_part),
        retain_until=retain_until,
        header_end_lineno=end,
        raw_status_lineno=status_lineno,
        missing_fields=missing_fields,
    )


def load_adr_headers(adr_dir: Path) -> dict[str, AdrHeader]:
    out: dict[str, AdrHeader] = {}
    if not adr_dir.is_dir():
        return out
    for fp in sorted(adr_dir.glob("*.md")):
        if fp.name.upper() in ("INDEX.MD", "TOMBSTONES.MD", "README.MD"):
            # Derived / pointer surfaces, not ADRs: INDEX is regenerated;
            # TOMBSTONES is the one-line-per-pruned-ADR index (ADR
            # 2026-08-08-great-prune §3 class 4); README is the directory hop.
            continue
        body = fp.read_text(encoding="utf-8", errors="replace")
        rel = f"docs/adr/{fp.name}"
        out[fp.name] = parse_adr_header(rel, body)
    return out


def load_tombstoned_names(adr_dir: Path) -> frozenset[str]:
    """Filenames of pruned ADRs recorded in TOMBSTONES.md. A supersession edge
    pointing at a tombstoned ADR is resolved (the decision record survives as a
    tombstone line + the pre-prune tag), while a typo'd target still fails A2."""
    fp = adr_dir / "TOMBSTONES.md"
    if not fp.is_file():
        return frozenset()
    text = fp.read_text(encoding="utf-8", errors="replace")
    return frozenset(m.group(0) for m in re.finditer(
        r"\d{4}-\d{2}-\d{2}[a-z]?-[a-z0-9-]+\.md", text))


def check_a1(headers: dict[str, AdrHeader]) -> list[Finding]:
    findings: list[Finding] = []
    for h in headers.values():
        if h.missing_fields:
            findings.append(Finding(
                "HARD", "A1", h.path, h.raw_status_lineno,
                "missing header fields: " + ", ".join(h.missing_fields)))
        if h.status not in STATUS_TOKENS:
            findings.append(Finding(
                "HARD", "A1", h.path, h.raw_status_lineno,
                f"Status token {h.status!r} not in closed vocabulary"))
        if h.decision_date is None:
            findings.append(Finding(
                "HARD", "A1", h.path, h.raw_status_lineno,
                "Decision date missing or unparseable"))
    return findings


def check_a2(headers: dict[str, AdrHeader],
             tombstoned: frozenset[str] = frozenset()) -> list[Finding]:
    findings: list[Finding] = []
    for name, y in headers.items():
        if y.status != "Accepted":
            continue  # Proposed edges are pending
        for e in y.supersedes:
            if e.kind != "adr":
                findings.append(Finding(
                    "HARD", "A2", y.path, e.lineno,
                    "Supersedes target must be an ADR path, not event:*"))
                continue
            if e.target in tombstoned:
                continue  # pruned target: tombstone line + tag carry the record
            if e.target not in headers:
                findings.append(Finding(
                    "HARD", "A2", y.path, e.lineno,
                    f"Supersedes target missing: {e.target}"))
                continue
            x = headers[e.target]
            if e.scope == "full":
                if x.status != "Superseded":
                    findings.append(Finding(
                        "HARD", "A2", y.path, e.lineno,
                        f"full supersede of {e.target} but its Status is {x.status}"))
                if not any(b.kind == "adr" and b.target == name
                           for b in x.superseded_by):
                    findings.append(Finding(
                        "HARD", "A2", y.path, e.lineno,
                        f"{e.target} missing Superseded-by: `{name}`"))
            elif e.scope == "in_part":
                if x.status != "Accepted":
                    findings.append(Finding(
                        "HARD", "A2", y.path, e.lineno,
                        f"in-part supersede of {e.target} requires Status Accepted"))
                if not any(b.kind == "adr" and b.target == name
                           for b in x.superseded_in_part_by):
                    findings.append(Finding(
                        "HARD", "A2", y.path, e.lineno,
                        f"{e.target} missing Superseded-in-part-by: `{name}`"))
            else:
                findings.append(Finding(
                    "HARD", "A2", y.path, e.lineno,
                    "Supersedes edge missing scope (full|in part)"))
    return findings

BODY_LINK_RE = re.compile(
    r"\*\*Body:\*\*\s*`?docs/ltm/adr/(?P<file>[^`\s]+)`?"
)
H2_RE = re.compile(r"^## ", re.M)


def is_stub(text: str, slug_stem: str) -> bool:
    if text.count("\n") + 1 > STUB_MAX_LINES:
        return False
    if H2_RE.search(text):
        return False
    m = BODY_LINK_RE.search(text)
    return bool(m and m.group("file") == slug_stem)


def check_a3(
    headers: dict[str, AdrHeader],
    adr_dir: Path,
    ltm_dir: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    for name, h in headers.items():
        if h.status not in COLD_TOKENS:
            continue
        text = (adr_dir / name).read_text(encoding="utf-8", errors="replace")
        surface = f"docs/adr/{name}"
        if not is_stub(text, name):
            findings.append(Finding(
                "HARD", "A3", surface, h.raw_status_lineno,
                "cold Status but hot file is not stub-shaped"))
        ltm_path = ltm_dir / name
        if not ltm_path.is_file():
            if not ltm_dir.is_dir():
                # Public seed excludes docs/ltm/** (2026-08-14 transition ADR).
                continue
            findings.append(Finding(
                "HARD", "A3", surface, h.raw_status_lineno,
                f"missing LTM body docs/ltm/adr/{name}"))
            continue
        ltm_h = parse_adr_header(
            f"docs/ltm/adr/{name}",
            ltm_path.read_text(encoding="utf-8", errors="replace"),
        )
        if ltm_h.status != h.status:
            findings.append(Finding(
                "HARD", "A3", surface, h.raw_status_lineno,
                f"stub Status {h.status} != LTM Status {ltm_h.status}"))
    return findings


def check_a4(
    headers: dict[str, AdrHeader],
    adr_dir: Path,
    ltm_dir: Path,
) -> list[Finding]:
    findings: list[Finding] = []
    for name, h in headers.items():
        if h.status not in {"Proposed", "Accepted"}:
            continue
        text = (adr_dir / name).read_text(encoding="utf-8", errors="replace")
        surface = f"docs/adr/{name}"
        if is_stub(text, name):
            findings.append(Finding(
                "HARD", "A4", surface, h.raw_status_lineno,
                "Proposed/Accepted must keep full hot body"))
    return findings
INDEX_HEADER = """\
# ADR index (derived)

> Generated by `python scripts/check_adr_graph.py --regenerate-index`.
> Do not hand-edit. Source of truth = ADR header fields.
> Notes cells cap at 40 words (W5); the full Status annotation lives on the ADR.
"""


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _index_notes(annotation: str, *, max_words: int = INDEX_NOTES_MAX_WORDS) -> str:
    """Clip a Status annotation for the INDEX notes cell.

    The ADR header is unchanged. Incomplete trailing markdown links are
    dropped so a mid-link word cut cannot leave a broken ``[text](`` cell.
    """
    text = (annotation or "").strip()
    if not text:
        return ""
    words = text.split()
    if len(words) <= max_words:
        return text
    clipped = " ".join(words[:max_words])
    if clipped.count("[") > clipped.count("]") or clipped.rstrip().endswith("("):
        clipped = clipped.rsplit("[", 1)[0].rstrip()
    return clipped + INDEX_NOTES_ELLIPSIS


def _format_supersedes(edges: tuple[EdgeTarget, ...]) -> str:
    if not edges:
        return "none"
    parts: list[str] = []
    for e in edges:
        if e.kind == "adr":
            if e.scope == "full":
                parts.append(f"`{e.target}` full")
            elif e.scope == "in_part":
                clause = f" — {e.clause}" if e.clause else ""
                parts.append(f"`{e.target}` in part{clause}")
            else:
                parts.append(f"`{e.target}`")
        else:
            note = f" — {e.clause}" if e.clause else ""
            parts.append(f"`event:{e.target}`{note}")
    return "; ".join(parts)


def _index_bucket(h: AdrHeader) -> str | None:
    if h.status in COLD_TOKENS:
        return "cold"
    if h.status == "Accepted" and h.superseded_in_part_by:
        return "partial"
    if h.status in {"Proposed", "Accepted"} and not h.superseded_in_part_by:
        return "live"
    return None


def _render_index_table(rows: list[AdrHeader]) -> str:
    lines = [
        "| file | status | decision date | supersedes | notes |",
        "|---|---|---|---|---|",
    ]
    for h in rows:
        d = h.decision_date.isoformat() if h.decision_date else ""
        notes = _index_notes(h.status_annotation)
        lines.append(
            "| "
            + " | ".join(
                _escape_cell(v)
                for v in (
                    h.path.rsplit("/", 1)[-1],
                    h.status,
                    d,
                    _format_supersedes(h.supersedes),
                    notes,
                )
            )
            + " |"
        )
    return "\n".join(lines)


def render_index(headers: dict[str, AdrHeader]) -> str:
    live: list[AdrHeader] = []
    partial: list[AdrHeader] = []
    cold: list[AdrHeader] = []
    for name in sorted(headers):
        h = headers[name]
        bucket = _index_bucket(h)
        if bucket == "live":
            live.append(h)
        elif bucket == "partial":
            partial.append(h)
        elif bucket == "cold":
            cold.append(h)
    parts = [INDEX_HEADER.rstrip(), "", "## Live", ""]
    parts.append(_render_index_table(live) if live else "_No live ADRs._")
    parts.extend(["", "## Partially superseded", ""])
    parts.append(_render_index_table(partial) if partial else "_None._")
    parts.extend(["", "## Cold", ""])
    parts.append(_render_index_table(cold) if cold else "_No cold ADRs._")
    return "\n".join(parts) + "\n"


def _normalize_index_text(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip() + "\n"


def check_a6(headers: dict[str, AdrHeader], index_text: str) -> list[Finding]:
    expected = render_index(headers)
    if _normalize_index_text(index_text) == _normalize_index_text(expected):
        return []
    return [Finding(
        "HARD", "A6", "docs/adr/INDEX.md", 1,
        "INDEX.md drift — run check_adr_graph.py --regenerate-index")]


def is_older_than_months(decision: date, today: date, months: int) -> bool:
    age = (today.year - decision.year) * 12 + (today.month - decision.month)
    if today.day < decision.day:
        age -= 1
    return age >= months


_ROOT_DOCS = (
    "CLAUDE.md",
    "STATE.md",
    "REPO_MAP.md",
    "README.md",
    "PIPELINES.md",
)


def iter_a5_surfaces(repo_root: Path) -> Iterable[Path]:
    docs = repo_root / "docs"
    if docs.is_dir():
        for fp in sorted(docs.rglob("*.md")):
            rel = fp.relative_to(docs)
            if rel.parts and rel.parts[0] == "ltm":
                continue
            yield fp
    for name in _ROOT_DOCS:
        fp = repo_root / name
        if fp.is_file():
            yield fp
    strategies = repo_root / "core" / "strategies"
    if strategies.is_dir():
        # LOCK.md files live under _archive/<family>/, not strategies/<family>/.
        for fp in sorted(strategies.glob("_archive/*/LOCK.md")):
            yield fp
    skills = repo_root / ".claude" / "skills"
    if skills.is_dir():
        for fp in sorted(skills.rglob("*.md")):
            yield fp


def _inbound_ref_pattern(slug_file: str) -> re.Pattern[str]:
    esc = re.escape(slug_file)
    return re.compile(
        rf"(?:docs/adr/{esc}|`{esc}`|\({esc}\)|\]\([^\)]*{esc})"
    )


def has_inbound_ref(
    slug_file: str,
    surfaces: Iterable[Path],
    self_path: Path,
) -> bool:
    pat = _inbound_ref_pattern(slug_file)
    self_resolved = self_path.resolve()
    for fp in surfaces:
        if not fp.is_file():
            continue
        if fp.resolve() == self_resolved:
            continue
        if fp.name.upper() == "INDEX.MD" and fp.parent.name == "adr":
            continue
        if pat.search(fp.read_text(encoding="utf-8", errors="replace")):
            return True
    return False


def _a5_scan_surfaces(
    repo_root: Path,
    headers: dict[str, AdrHeader],
) -> list[Path]:
    cold = {
        name for name, h in headers.items() if h.status in COLD_TOKENS
    }
    out: list[Path] = []
    for fp in iter_a5_surfaces(repo_root):
        if fp.name.upper() == "INDEX.MD" and fp.parent.name == "adr":
            continue
        if (
            fp.parent.name == "adr"
            and fp.parent.parent.name == "docs"
            and fp.name in cold
        ):
            continue
        out.append(fp)
    return out


def check_a5(
    headers: dict[str, AdrHeader],
    repo_root: Path,
    today: date | None = None,
) -> list[Finding]:
    today = today or date.today()
    findings: list[Finding] = []
    surfaces = _a5_scan_surfaces(repo_root, headers)
    for name, h in headers.items():
        if h.status != "Accepted":
            continue
        if h.superseded_in_part_by:
            continue
        if h.decision_date is None:
            continue
        if not is_older_than_months(h.decision_date, today, AGE_MONTHS):
            continue
        if h.retain_until is not None and h.retain_until > today:
            continue
        self_path = repo_root / "docs" / "adr" / name
        if has_inbound_ref(name, surfaces, self_path):
            continue
        findings.append(Finding(
            "HARD", "A5", h.path, h.raw_status_lineno,
            f"Accepted ADR older than {AGE_MONTHS} months with no inbound refs; "
            "retire or set Retain-until",
        ))
    return findings


FORWARD_TRIGGERS_HEADER_RE = re.compile(
    r"^##\s+Scheduled forward triggers", re.IGNORECASE)
STATE_ADR_CITE_RE = re.compile(
    r"docs/adr/([0-9]{4}-[0-9]{2}-[0-9]{2}-[^`)\]\s]+\.md)")


def _state_forward_bullets(text: str) -> list[tuple[int, str]]:
    """Group STATE.md's '## Scheduled forward triggers' section into
    (first_lineno, joined_text) per top-level `- ` bullet. Multi-line markdown
    list items are the norm in this file; a line-scoped rule would match
    nothing (the same defect that sank check_status_consistency's first C4
    attempt)."""
    out: list[tuple[int, str]] = []
    in_section = False
    cur_no: int | None = None
    buf: list[str] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            if in_section and cur_no is not None:
                out.append((cur_no, chr(10).join(buf)))
            in_section = bool(FORWARD_TRIGGERS_HEADER_RE.match(line))
            cur_no, buf = None, []
            continue
        if not in_section:
            continue
        if re.match(r"^- ", line):
            if cur_no is not None:
                out.append((cur_no, chr(10).join(buf)))
            cur_no, buf = i, [line]
        elif cur_no is not None:
            buf.append(line)
    if in_section and cur_no is not None:
        out.append((cur_no, chr(10).join(buf)))
    return out


def check_a7(headers: dict[str, AdrHeader], state_text: str, state_surface: str) -> list[Finding]:
    """A7 -- a STATE.md forward-trigger bullet cites an ADR the graph shows has
    been superseded (full or in part), without the bullet also naming at least
    one of the superseding ADRs. In DEFAULT_ENABLED_CHECKS as of 2026-08-26 --
    the corpus was clean under both A5 and A7 at flip time (6 findings existed
    and were fixed by hand first, PR #170); same posture as A5.

    Deliberately NOT the C4 join check_status_consistency.py tried and dropped.
    That attempt joined STATE.md's forward board against STATE.md's OWN pointer
    log by shared textual anchor -- and there is none: the 2026-07-24 incident's
    discharge bullet cited 32 repo paths and not one was the ADR it discharged.
    This joins on a DIFFERENT, reliable anchor instead: the ADR filename, which
    is how every STATE.md bullet already cites its owning decision, checked
    against the ADR graph's own structured Supersedes/Superseded-by/
    Superseded-in-part-by edges -- the same edges A2 already keeps internally
    consistent. Nothing semantic is guessed; a citation is a citation.

    MEASURED PRECISION, first production run (2026-07-25): 4 findings, 1 true
    positive / 3 false positives. The true positive was real and had been live
    for 13 days: the four-firms ADR's own §4 forward-board bullet still read
    "quarterly check 2026-08-08; HARD DATE 2026-11-08" with zero mention that
    the discharge it was tracking had been WITHDRAWN 2026-07-22 -- unchanged
    since 2026-07-12 (git blame), surviving even a same-week hygiene pass whose
    attention was on reverting a WRONG discharge claim rather than completing
    the right one. Fixed in the same commit as this check.

    The 3 false positives share one root cause: WHOLE-ADR join granularity.
    An ADR can be partially superseded on a clause with nothing to do with what
    a given STATE.md bullet is discussing (e.g. the D2 dd_protection-revert
    bullet cites an ADR that was separately, unrelated-ly, partially superseded
    on an ACTIVE_FIRM-retention clause three sections away). The check cannot
    tell "this ADR has SOME incoming edge" from "this ADR has an incoming edge
    ON THE CLAUSE THIS BULLET IS ABOUT" without clause-level semantic matching
    -- which is the C1 mistake in new clothing. Each of the 3 was fixed with a
    one-line "(Unrelated: ...)" pointer rather than silenced, since the
    underlying fact (a partial supersede exists) is true and worth one line
    regardless of A7. The corpus is clean as of this commit, but a FUTURE
    unrelated partial-supersede on any currently-cited ADR will retrigger this
    same false-positive class -- this is a periodic-review tool, not a gate,
    and should stay opt-in for that reason even at 0 current findings.
    """
    findings: list[Finding] = []
    for lineno, body in _state_forward_bullets(state_text):
        cited = STATE_ADR_CITE_RE.findall(body)
        if not cited:
            continue
        cited_set = set(cited)
        seen: set[str] = set()
        for adr in cited:
            if adr in seen:
                continue
            h = headers.get(adr)
            if h is None:
                continue
            supersede_targets = {
                e.target for e in (*h.superseded_by, *h.superseded_in_part_by)
                if e.kind == "adr"
            }
            if not supersede_targets or (supersede_targets & cited_set):
                continue
            seen.add(adr)
            findings.append(Finding(
                "HARD", "A7", state_surface, lineno,
                f"cites {adr}, which the ADR graph shows superseded by "
                f"{sorted(supersede_targets)} -- bullet does not name the "
                "superseding ADR"))
    return findings


# A8 — intra-ADR running-count consistency. Discovers ADRs by the counting-
# machinery "(a) Authoritative surface" sentence. Does NOT join STATE.md or
# ops/instruments/*.md (closed-row deletion is legal). Owner:
# docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md 2026-08-29 addendum.
AUTHORITATIVE_SURFACE_RE = re.compile(
    r"\(a\)\s+Authoritative surface\.\s*.{0,240}running-count line",
    re.IGNORECASE | re.DOTALL,
)
TABLE_CANONICAL_RE = re.compile(
    r"\*\*Running(?:\s+consecutive\s+[^*]+)?\s+count\s+\(canonical\):"
    r"(?:\*\*)?\s*(\d+)\s*/\s*(\d+)",
    re.IGNORECASE,
)
DEEP_LANE_HEAD_RE = re.compile(
    r"\*\*Running counts \(canonical, this ADR\):\*\*",
    re.IGNORECASE,
)
DEEP_LANE_FIELDS_RE = re.compile(
    r"campaigns completed \*\*(\d+)\*\*"
    r".*?survivors falsified \*\*(\d+)\s*/\s*(\d+)\*\*"
    r".*?campaigns abandoned \*\*(\d+)\*\*",
    re.IGNORECASE | re.DOTALL,
)
DEEP_LANE_PREREG_RE = re.compile(
    r"(?:[\w./-]+/)?[\w.-]*deep-lane[\w.-]*prereg[\w.-]*\.md",
    re.IGNORECASE,
)
_SKIP_ADR_NAMES = frozenset({"INDEX.MD", "TOMBSTONES.MD", "README.MD"})


def _cell_plain(cell: str) -> str:
    s = cell.strip()
    while s.startswith("*"):
        s = s[1:]
    return s.strip().lower()


def _yes_increment_count(text: str) -> int | None:
    """Count increment-table rows whose Increments? cell starts with 'yes'.

    Returns None if no such table exists.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "Increments?" not in line or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        try:
            idx = next(j for j, c in enumerate(cells) if "Increments?" in c)
        except StopIteration:
            continue
        yes = 0
        for row in lines[i + 1:]:
            stripped = row.strip()
            if not stripped.startswith("|"):
                break
            body = stripped.strip("|")
            if set(body.replace("|", "").replace(":", "").replace("-", "").strip()) == set():
                continue
            rcells = [c.strip() for c in body.split("|")]
            if idx >= len(rcells):
                continue
            if _cell_plain(rcells[idx]).startswith("yes"):
                yes += 1
        return yes
    return None


def _deep_lane_paragraph(text: str) -> tuple[str, int] | None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if DEEP_LANE_HEAD_RE.search(line):
            buf = [line]
            for nxt in lines[i + 1:]:
                if nxt.strip() == "" or nxt.startswith("##"):
                    break
                buf.append(nxt)
            return "\n".join(buf), i + 1
    return None


def _deep_lane_prereg_names(paragraph: str) -> frozenset[str]:
    return frozenset(
        Path(p).name.lower() for p in DEEP_LANE_PREREG_RE.findall(paragraph)
    )


def check_a8(adr_dir: Path) -> list[Finding]:
    """A8 -- a counting-machinery ADR's canonical n disagrees with its own
    increment evidence (table yes-rows, or deep-lane *deep-lane* prereg cites).

    Discovers files by the existing '(a) Authoritative surface' sentence.
    Table-backed ADRs compare N on 'Running … count (canonical): N / D' to
    the Increments? yes-count. Deep-lane (no table) compares
    'campaigns abandoned **A**' to unique *deep-lane*.md paths in that
    paragraph. STATE.md / instrument-profile mirrors are deliberately
    not joined — those ADRs authorize deleting closed STATE rows.
    """
    findings: list[Finding] = []
    if not adr_dir.is_dir():
        return findings
    for fp in sorted(adr_dir.glob("*.md")):
        if fp.name.upper() in _SKIP_ADR_NAMES:
            continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        if not AUTHORITATIVE_SURFACE_RE.search(text):
            continue
        surface = f"docs/adr/{fp.name}"
        table_m = TABLE_CANONICAL_RE.search(text)
        deep = _deep_lane_paragraph(text)
        if table_m:
            declared_n = int(table_m.group(1))
            yes_n = _yes_increment_count(text)
            lineno = text[: table_m.start()].count("\n") + 1
            if yes_n is None:
                findings.append(Finding(
                    "HARD", "A8", surface, lineno,
                    "canonical running-count line has no Increments? table",
                ))
                continue
            if declared_n != yes_n:
                findings.append(Finding(
                    "HARD", "A8", surface, lineno,
                    f"canonical running-count N={declared_n} disagrees with "
                    f"Increments? yes-count {yes_n}",
                ))
            continue
        if deep:
            paragraph, lineno = deep
            fields = DEEP_LANE_FIELDS_RE.search(paragraph)
            if fields is None:
                findings.append(Finding(
                    "HARD", "A8", surface, lineno,
                    "Running counts (canonical, this ADR) line is unparseable "
                    "(need campaigns completed / survivors falsified / "
                    "campaigns abandoned)",
                ))
                continue
            abandoned = int(fields.group(4))
            cited = _deep_lane_prereg_names(paragraph)
            if abandoned != len(cited):
                findings.append(Finding(
                    "HARD", "A8", surface, lineno,
                    f"campaigns abandoned **{abandoned}** disagrees with "
                    f"{len(cited)} *deep-lane* prereg path(s) cited in the "
                    "same paragraph",
                ))
            continue
        findings.append(Finding(
            "HARD", "A8", surface, 1,
            "has (a) Authoritative surface counting machinery but no "
            "parseable Running count (canonical) line or Running counts "
            "(canonical, this ADR) paragraph",
        ))
    return findings


def collect_findings(
    repo_root: Path,
    enabled: frozenset[str],
    today: date | None = None,
) -> list[Finding]:
    adr_dir = repo_root / "docs" / "adr"
    ltm_dir = repo_root / "docs" / "ltm" / "adr"
    headers = load_adr_headers(adr_dir)
    findings: list[Finding] = []
    if "A1" in enabled:
        findings += check_a1(headers)
    if "A2" in enabled:
        findings += check_a2(headers, load_tombstoned_names(adr_dir))
    if "A3" in enabled:
        findings += check_a3(headers, adr_dir, ltm_dir)
    if "A4" in enabled:
        findings += check_a4(headers, adr_dir, ltm_dir)
    if "A5" in enabled:
        findings += check_a5(headers, repo_root, today=today)
    if "A6" in enabled:
        idx_path = adr_dir / "INDEX.md"
        text = idx_path.read_text(encoding="utf-8") if idx_path.is_file() else ""
        findings += check_a6(headers, text)
    if "A7" in enabled:
        state_path = repo_root / "STATE.md"
        if state_path.is_file():
            findings += check_a7(
                headers, state_path.read_text(encoding="utf-8"), "STATE.md")
    if "A8" in enabled:
        findings += check_a8(adr_dir)
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--regenerate-index", action="store_true")
    ap.add_argument(
        "--enable", default="",
        help="comma list overriding DEFAULT_ENABLED_CHECKS for one run",
    )
    ap.add_argument(
        "--today", default="",
        help="YYYY-MM-DD override for A5 age check (tests / M4)",
    )
    args = ap.parse_args(argv)
    root = args.repo_root
    adr_dir = root / "docs" / "adr"
    headers = load_adr_headers(adr_dir)
    if args.regenerate_index:
        (adr_dir / "INDEX.md").write_text(render_index(headers), encoding="utf-8")
        print(f"wrote {adr_dir / 'INDEX.md'}")
        return 0
    enabled = (
        frozenset(x.strip() for x in args.enable.split(",") if x.strip())
        or DEFAULT_ENABLED_CHECKS
    )
    unknown = enabled - VALID_CHECKS
    if unknown:
        print(
            f"check_adr_graph: unknown check(s): {sorted(unknown)}; "
            f"valid={sorted(VALID_CHECKS)}",
            file=sys.stderr,
        )
        return 2
    today: date | None = None
    if args.today:
        today = date.fromisoformat(args.today)
    findings = collect_findings(root, enabled, today=today)
    hard = [f for f in findings if f.severity == "HARD"]
    for f in hard:
        print(f"HARD: {f.surface}:{f.lineno}: {f.code} {f.message}")
    if hard:
        print(f"\ncheck_adr_graph: {len(hard)} finding(s).")
        return 1
    print(f"check_adr_graph: OK (enabled={sorted(enabled)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
