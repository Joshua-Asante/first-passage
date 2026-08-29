"""archive_lab_analysis.py — STM/LTM archive for lab/analysis studies.

Design: docs/superpowers/specs/2026-07-11-lab-analysis-stm-ltm-archive-design.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gate_fire_log import log_fire  # noqa: E402

FIELD_HEAD_LINES = 40
ANALYSIS_REL = "lab/analysis"
ARCHIVE_REL = "lab/archive"
CATALOG_REL = "lab/CATALOG.md"

_CATALOG_HEADER = """\
# Lab analysis catalog

Open this file first for lab decisions. Hot bodies live under
`lab/analysis/<theme>/<slug>/`; archived studies are stub-only under
`lab/analysis/<slug>/CARD.md` (body in `lab/archive/<slug>/`).

Do not glob `lab/analysis/` alone to infer what is live.

**Camp layout (pytest):** every candidate directory that carries `test_*.py`
must include an empty `__init__.py` at scaffold time (and keep it when
archived). Hyphenated slugs (`…_2026-08`) are **not** valid package names, so
the marker alone cannot uniquify shared basenames under prepend —
`validation-controls` therefore runs `pytest lab/ --import-mode=importlib`.
Sibling imports of camp-local modules (especially shared names like
`construct_lib`) must use
[`research_utils.camp_import.load_camp_sibling`](research_utils/camp_import.py).
Still ship the `__init__.py` marker: valid-identifier camps need it, and it
documents the camp boundary for humans/tools.
"""

_ARCHIVED_RE = re.compile(r"(?im)^\*\*Archived:\*\*\s*(\S+)")

# Archiveable → catalog status
_TOKEN_STATUS = [
    (re.compile(r"DONE_WITH_CONCERNS", re.I), "CLOSED"),
    (re.compile(r"NOT\s*CLEARED", re.I), "FALSIFIED"),
    (re.compile(r"FAIL-?COST", re.I), "FALSIFIED"),
    (re.compile(r"\bRETIRED\b", re.I), "RETIRED"),
    (re.compile(r"\bSHELVED\b", re.I), "CLOSED"),
    (re.compile(r"\bFALSIFIED\b", re.I), "FALSIFIED"),
    # Distinct terminal NULL verdict (STOP / NULL). Case-sensitive uppercase
    # only — prose "null"/"the null" must not hijack CLOSED or other tokens
    # into FALSIFIED (third firing: tnec_envelope_compile_2026-08).
    (re.compile(r"\bNULL\b"), "NULL"),
    (re.compile(r"\bREJECT(?:ED)?\b", re.I), "FALSIFIED"),
    (re.compile(r"\bCLOSED\b", re.I), "CLOSED"),
    (re.compile(r"\bDONE\b", re.I), "CLOSED"),
    # Terminal gate outcomes that are not FALSIFIED (e.g. Q-GEOFIT-1)
    (re.compile(r"\bAMBIGUOUS(?:-PARAMETERIZATION)?\b", re.I), "CLOSED"),
    (re.compile(r"\bHOLD\b", re.I), "HOLD"),
    (re.compile(r"\bACTIVE\b", re.I), "ACTIVE"),
    # Non-terminal study-state words used as Status tokens. Uppercase-only
    # and also listed in _NON_TERMINAL_DOMINANT so a clause EXPLORATORY /
    # MEASURED is not stolen by a later CLOSED/FALSIFIED in the narrative.
    # RESOLVED is deliberately absent: it is a Q-closure verdict, not a
    # CATALOG status. Mapping it to CLOSED would flip stay-hot Active rows
    # (house style is ``ACTIVE — … RESOLVED …``) and mark them archiveable.
    # Hyphenated forms (RESOLVED-QUANTIFIED, RESOLVED-BY-RETIREMENT) would
    # also collide. Same NULL/CLOSED prose-collision class.
    (re.compile(r"\bEXPLORATORY\b"), "ACTIVE"),
    (re.compile(r"\bMEASURED\b"), "ACTIVE"),
]

_ARCHIVEABLE = frozenset({"CLOSED", "FALSIFIED", "RETIRED", "NULL"})

# House style is "VERDICT — narrative". Everything after the first spaced dash
# is prose, and prose routinely names *other* statuses: q_kbudget_1_2026-07's
# verdict is `RESOLVED`, but its one-liner recounts "Historical path:
# AMBIGUOUS-HOLD → ... → ratified". Only the verdict clause may decide, or a
# study's own history re-opens it.
_VERDICT_CLAUSE_SPLIT = re.compile(r"\s+[—–]\s+|\s+--?\s+")

# Non-archiveable statuses DOMINATE within that clause. `AMBIGUOUS-HOLD` (and
# "AMBIGUOUS / operational HOLD") is a real non-terminal verdict in this repo's
# vocabulary — it is in the CC-handoff verdict enum, and Q-KBUDGET-1 passed
# through it before resolving — and it is distinct from the bare, terminal
# `AMBIGUOUS` that _TOKEN_STATUS maps to CLOSED. Searching the whole value in
# priority order let AMBIGUOUS win, stamping a held study archiveable.
#
# A pre-check rather than a reordering, because the error is asymmetric:
# reading HOLD as CLOSED marks a study the operator held as archive-owed, and
# `--slug` would then move it — silent and destructive. Reading CLOSED as HOLD
# only leaves an archive owed, which is visible and reversible. Ambiguity must
# resolve to the non-archiveable reading.
#
# Uppercase-only, deliberately: every status token in the corpus is written in
# caps, while lowercase "hold"/"active" appear in ordinary prose. Matching
# case-insensitively here would let prose hijack a genuine closure.
_NON_TERMINAL_DOMINANT = [
    (re.compile(r"\bHOLD\b"), "HOLD"),
    (re.compile(r"\bACTIVE\b"), "ACTIVE"),
    (re.compile(r"\bEXPLORATORY\b"), "ACTIVE"),
    (re.compile(r"\bMEASURED\b"), "ACTIVE"),
]

# Field line: Disposition|Status|Verdict (optional bold) then : then value
_FIELD_RE = re.compile(
    r"(?im)^(?:\*\*)?(Disposition|Status|Verdict)(?:\*\*)?\s*:\s*(?:\*\*)?(.+?)\s*$"
)
# Also: **Verdict: FALSIFIED.** (label+value inside one bold span)
_BOLD_COMBO_RE = re.compile(
    r"(?im)^\*\*(Disposition|Status|Verdict)\s*:\s*(.+?)\*\*"
)
# Inline: Date · **Disposition:** CLOSED — … · Scope
_INLINE_RE = re.compile(
    r"(?:\*\*)?(Disposition|Status|Verdict)(?:\*\*)?\s*:\s*(?:\*\*)?"
    r"(.+?)(?=\s*·|\s*$)",
    re.I,
)
_DECISIVE_RE = re.compile(r"decisive:\s*([A-Za-z0-9_.-]+)", re.I)

_MARKDOWN_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")

_OUTBOUND_SIBLING_RE = re.compile(r"\]\(\.\./([^)/]+)")

_LIVING_ROOTS = (
    "docs",
    "ops",
    ".claude/skills",
    "tests",
)

_LIVING_FILES = ("CLAUDE.md", "STATE.md")

_SKIP_LIVING_PREFIX = "docs/ltm/notes/archive/"

_TEXT_SUFFIXES = frozenset(
    {".md", ".py", ".txt", ".json", ".toml", ".yml", ".yaml", ".rst", ".ini"}
)


class ArchiveError(Exception):
    """Refused or failed archive operation."""


@dataclass(frozen=True)
class ArchiveReport:
    slug: str
    decisive_name: str
    archived_date: str
    dry_run: bool
    body_path: str
    stub_path: str


@dataclass(frozen=True)
class Disposition:
    raw_token: str
    status: str
    one_liner: str
    decisive_hint: str | None


THEME_ORDER: tuple[str, ...] = (
    "c1",
    "striker",
    "orb",
    "aegis",
    "regime",
    "harvest",
    "mc",
    "legacy",
    "deep_lane",
    "_inbox",
)
THEMES: frozenset[str] = frozenset(THEME_ORDER)

_THEME_DIR_ALT = "|".join(re.escape(t) for t in THEME_ORDER)
_LAB_SLUG_PATH_RE = re.compile(
    rf"lab[/\\]analysis(?:[/\\](?:{_THEME_DIR_ALT}))?[/\\]([A-Za-z0-9_.-]+)",
    re.I,
)
_SYS_PATH_SLUG_RE = re.compile(
    rf"sys\.path\.(?:insert|append)\s*\([^)]*"
    rf"lab[/\\]analysis(?:[/\\](?:{_THEME_DIR_ALT}))?[/\\]([A-Za-z0-9_.-]+)",
    re.I,
)

_THEME_LINE_RE = re.compile(
    r"(?im)^\s*(?:\*\*)?(?:Theme)(?:\*\*)?\s*:\s*(.+?)\s*$"
)


@dataclass(frozen=True)
class CatalogRow:
    slug: str
    theme: str
    status: str
    one_liner: str
    card: str
    body: str
    heavy: str
    closed: str
    hot: str = ""


def parse_theme(text: str) -> str:
    head = "\n".join(text.splitlines()[:FIELD_HEAD_LINES])
    for line in head.splitlines():
        m = _THEME_LINE_RE.match(line.strip())
        if not m:
            continue
        tokens = m.group(1).strip().strip("*").strip().split()
        if not tokens:
            return "_inbox"
        raw = tokens[0].lower()
        return raw if raw in THEMES else "_inbox"
    return "_inbox"


def is_archiveable(status: str) -> bool:
    return status in _ARCHIVEABLE


def _normalize_status(value: str) -> str | None:
    # Non-archiveable dominates, but only from the verdict clause — see
    # _NON_TERMINAL_DOMINANT for why both halves of that sentence are load-bearing.
    clause = _VERDICT_CLAUSE_SPLIT.split(value, maxsplit=1)[0]
    for rx, status in _NON_TERMINAL_DOMINANT:
        if rx.search(clause):
            return status
    for rx, status in _TOKEN_STATUS:
        if rx.search(value):
            return status
    return None


def _extract_field_and_value(line: str) -> tuple[str | None, str | None]:
    """Return (field_name, value) from a disposition field line, or (None, None)."""
    stripped = line.strip()
    m = _FIELD_RE.match(stripped) or _BOLD_COMBO_RE.match(stripped)
    if m:
        return m.group(1), m.group(2).strip().rstrip("*").strip()
    m = _INLINE_RE.search(stripped)
    if m:
        return m.group(1), m.group(2).strip().rstrip("*").strip()
    return None, None


def _extract_value_from_line(line: str) -> str | None:
    """Return disposition field value from a single line, or None."""
    _field, value = _extract_field_and_value(line)
    return value


def _raw_token_for_status(value: str, status: str) -> str:
    for rx, st in _TOKEN_STATUS:
        if st == status and rx.search(value):
            return rx.pattern
    return status


def _clean_one_liner(value: str, status: str) -> str:
    """Strip redundant status tokens from a disposition value for display."""
    s = value.strip().rstrip("*").strip()
    changed = True
    while changed and s:
        changed = False
        for rx, _st in _TOKEN_STATUS:
            m = re.match(
                rf"^(?:\*\*)?{rx.pattern}(?:\*\*)?\s*[—\-/|]+\s*",
                s,
                re.I,
            )
            if m:
                s = s[m.end() :].strip().lstrip("*").strip()
                changed = True
                break
        # Hand Status annotations (claim-alignment M11/M45): "ACTIVE (note) — rest".
        # Separator after the parenthetical is required so dated archive one-liners
        # like "FALSIFIED (2026-06-17)** — …" keep their historical prefix.
        m = re.match(
            rf"^(?:\*\*)?{re.escape(status)}(?:\*\*)?\s*\([^)]*\)\s*[—\-/|]+\s*",
            s,
            re.I,
        )
        if m:
            s = s[m.end() :].strip().lstrip("*").strip()
            changed = True
            continue
        bare = re.match(rf"^(?:\*\*)?{re.escape(status)}(?:\*\*)?\s*$", s, re.I)
        if bare:
            return ""
    return s


def parse_disposition(text: str) -> Disposition | None:
    """Resolve campaign disposition from a card head.

    When both a Verdict field and a Status/Disposition field are present as
    separate lines, Verdict wins (ADR 2026-08-22-catalog-hot-vs-disposition).
    Dominance *inside* a single value still uses ``_NON_TERMINAL_DOMINANT``
    on the verdict clause — HOLD in that clause still dominates.
    """
    head = "\n".join(text.splitlines()[:FIELD_HEAD_LINES])
    verdict_hit: Disposition | None = None
    other_hit: Disposition | None = None
    for line in head.splitlines():
        stripped = line.strip()
        # v1 stamp-first: blockquote-only VERDICT lines do not auto-qualify
        if stripped.startswith(">"):
            continue
        field, value = _extract_field_and_value(line)
        if value is None:
            continue
        status = _normalize_status(value)
        if status is None:
            continue
        hint = None
        hm = _DECISIVE_RE.search(value)
        if hm:
            hint = hm.group(1)
        one = _clean_one_liner(value, status) or value
        if len(one) > 120:
            one = one[:117] + "..."
        raw = _raw_token_for_status(value, status)
        hit = Disposition(
            raw_token=raw, status=status, one_liner=one, decisive_hint=hint
        )
        if field is not None and field.lower() == "verdict":
            if verdict_hit is None:
                verdict_hit = hit
        elif other_hit is None:
            other_hit = hit
        if verdict_hit is not None and other_hit is not None:
            break
    return verdict_hit if verdict_hit is not None else other_hit


def choose_source_card(slug_dir: Path) -> Path | None:
    """Pick decisive source card: RESULTS* > verdict.md > CLOSURE.md > README.md."""
    if not slug_dir.is_dir():
        return None
    results_md = slug_dir / "RESULTS.md"
    if results_md.is_file():
        return results_md
    results_variants = sorted(slug_dir.glob("RESULTS_*.md"))
    if results_variants:
        return results_variants[0]
    for name in ("verdict.md", "CLOSURE.md", "README.md"):
        candidate = slug_dir / name
        if candidate.is_file():
            return candidate
    return None


def is_theme_dir_name(name: str) -> bool:
    return name in THEMES


def _tracked_under_prefix(
    repo: Path,
    prefix: str,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None,
) -> frozenset[str]:
    """Return tracked paths under ``prefix`` (POSIX, trailing slash).

    ``tracked_override`` remains keyed by slug; when set, the override set is
    returned as-is (callers filter by prefix when needed).
    """
    if tracked_override is not None:
        return tracked_override.get(slug, frozenset())
    try:
        out = subprocess.check_output(
            ["git", "ls-files", "--", prefix],
            cwd=repo,
            encoding="utf-8",
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return frozenset()
    return frozenset(line.strip() for line in out.splitlines() if line.strip())


def _tracked_under_slug(
    repo: Path,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None,
) -> frozenset[str]:
    return _tracked_under_prefix(
        repo, f"{ANALYSIS_REL}/{slug}/", slug, tracked_override
    )


def is_stub_dir(
    slug_dir: Path,
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> bool:
    """True when tracked files under a flat ``analysis/<slug>/`` are exactly {CARD.md}.

    Stub detection stays flat-only; nested hot bodies are never stubs.
    """
    slug = slug_dir.name
    try:
        rel = slug_dir.relative_to(repo / ANALYSIS_REL).as_posix()
    except ValueError:
        rel = slug
    # Nested path (theme/slug) is never a flat stub.
    if "/" in rel:
        return False
    prefix = f"{ANALYSIS_REL}/{slug}/"
    tracked = _tracked_under_slug(repo, slug, tracked_override)
    expected = frozenset({f"{prefix}CARD.md"})
    if tracked:
        return tracked == expected
    card = slug_dir / "CARD.md"
    if not card.is_file():
        return False
    on_disk = sorted(
        p.relative_to(slug_dir).as_posix()
        for p in slug_dir.rglob("*")
        if p.is_file()
    )
    return on_disk == ["CARD.md"]


def iter_hot_bodies(repo: Path) -> list[tuple[str, str, Path]]:
    """Yield (dir_theme, slug, path) for nested and pre-Wave-2 flat hot bodies."""
    root = repo / ANALYSIS_REL
    out: list[tuple[str, str, Path]] = []
    if not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if is_theme_dir_name(child.name):
            for slug_dir in sorted(child.iterdir()):
                if slug_dir.is_dir() and slug_dir.name != "__pycache__":
                    out.append((child.name, slug_dir.name, slug_dir))
        elif not (child / "CARD.md").is_file() or any(
            p.is_file() and p.name != "CARD.md" for p in child.iterdir()
        ):
            # flat full dir (pre-Wave-2) or non-stub; skip loose-script names
            if child.name.endswith(".py"):
                continue
            out.append(("_inbox", child.name, child))
    return out


def resolve_hot_dir(repo: Path, slug: str) -> Path | None:
    """Return nested hot body path for ``slug``, or None if stub-only/missing/flat.

    Nested-only contract: the path must be ``analysis/<theme>/<slug>/`` (parent
    is a theme directory directly under ``lab/analysis/``). Flat pre-Wave-2 full
    dirs are emitted by ``iter_hot_bodies`` as ``("_inbox", slug, path)``; because
    ``_inbox ∈ THEMES``, a theme-name filter alone would incorrectly accept them.
    """
    analysis_root = (repo / ANALYSIS_REL).resolve()
    for _dir_theme, hot_slug, path in iter_hot_bodies(repo):
        if hot_slug != slug:
            continue
        try:
            parent = path.resolve().parent
        except OSError:
            continue
        # Two-level only: analysis/<theme>/<slug>/
        if parent.parent != analysis_root or not is_theme_dir_name(parent.name):
            continue
        if is_stub_dir(path, repo):
            continue
        return path
    return None


def theme_layout_active(repo: Path) -> bool:
    """True when any closed-set theme directory exists under ``lab/analysis/``."""
    analysis_root = repo / ANALYSIS_REL
    if not analysis_root.is_dir():
        return False
    return any(
        child.is_dir() and is_theme_dir_name(child.name)
        for child in analysis_root.iterdir()
    )


def resolve_body_dir(
    repo: Path,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> Path | None:
    """Return nested or flat hot body dir for ``slug``, or None if missing/stub-only."""
    nested = resolve_hot_dir(repo, slug)
    if nested is not None:
        return nested
    flat = repo / ANALYSIS_REL / slug
    if flat.is_dir() and not is_stub_dir(flat, repo, tracked_override):
        return flat
    return None


def _resolve_scan_theme(stamped: str, dir_theme: str) -> str:
    """Prefer stamped theme; fall back to directory theme when stamp is ``_inbox``."""
    if stamped != "_inbox" and stamped in THEMES:
        return stamped
    if dir_theme != "_inbox" and is_theme_dir_name(dir_theme):
        return dir_theme
    return stamped


# `heavy` column vocabulary. Single-sourced so the catalog-freshness tolerance
# (`_compare_catalog`) cannot drift from what `_heavy_note` actually emits.
_HEAVY_INPUTS = "inputs gitignored"
_HEAVY_PKL = "pkl gitignored"
_HEAVY_NONE = "—"
# Values `_heavy_note` emits ONLY when a gitignored heavy artifact is present on
# disk — i.e. the annotations a worktree/clone lacking those bytes cannot verify.
_HEAVY_GITIGNORED = frozenset({_HEAVY_INPUTS, _HEAVY_PKL})


def _heavy_note(path: Path) -> str:
    if path.is_dir():
        if (path / "inputs").is_dir():
            return _HEAVY_INPUTS
        if any(path.glob("*.pkl")):
            return _HEAVY_PKL
    return _HEAVY_NONE


def _closed_from_card(text: str) -> str:
    m = _ARCHIVED_RE.search(text)
    return m.group(1) if m else "—"


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _row_from_stub(
    repo: Path,
    slug: str,
    slug_dir: Path,
    archive_body: Path,
) -> CatalogRow | None:
    card_path = slug_dir / "CARD.md"
    if not card_path.is_file():
        return None
    text = card_path.read_text(encoding="utf-8")
    disp = parse_disposition(text)
    status = disp.status if disp else "ACTIVE"
    one_liner = disp.one_liner if disp else "—"
    return CatalogRow(
        slug=slug,
        theme="—",
        status=status,
        one_liner=one_liner,
        card=f"{ANALYSIS_REL}/{slug}/CARD.md",
        body=f"{ARCHIVE_REL}/{slug}/",
        heavy=_heavy_note(archive_body),
        closed=_closed_from_card(text),
        hot="no",
    )


def _row_from_full_dir(
    repo: Path, slug: str, slug_dir: Path, theme: str
) -> CatalogRow:
    source = choose_source_card(slug_dir)
    source_text = source.read_text(encoding="utf-8") if source is not None else ""
    disp = parse_disposition(source_text) if source is not None else None
    status = disp.status if disp else "ACTIVE"
    one_liner = disp.one_liner if disp else "—"
    # Terminal disposition may sit in a full STM dir (stay-hot pin). C2 joins
    # to `hot`, not disposition class — do not coerce to HOLD / "archive owed".
    # Unstubbed closes remain a --check finding; --slug is still two-part.
    rel = slug_dir.relative_to(repo).as_posix()
    card = f"{rel}/{source.name}" if source is not None else "—"
    return CatalogRow(
        slug=slug,
        theme=theme,
        status=status,
        one_liner=one_liner,
        card=card,
        body=f"{rel}/",
        heavy=_heavy_note(slug_dir),
        closed="—",
        hot="yes",
    )


def scan_lab(
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> list[CatalogRow]:
    """Scan lab/analysis/ and build catalog rows (no orphan archive bodies).

    Discovers (a) flat stub-only dirs → archived rows; (b) nested
    ``analysis/<theme>/<slug>/`` full dirs and pre-Wave-2 flat full dirs →
    active rows. Theme ``README.md`` and loose root scripts are ignored.
    """
    analysis_root = repo / ANALYSIS_REL
    if not analysis_root.is_dir():
        return []
    active_rows: list[CatalogRow] = []
    archived_rows: list[CatalogRow] = []

    # (a) flat stub-only dirs → archived
    for slug_dir in sorted(analysis_root.iterdir()):
        if not slug_dir.is_dir() or is_theme_dir_name(slug_dir.name):
            continue
        slug = slug_dir.name
        if not is_stub_dir(slug_dir, repo, tracked_override):
            continue
        archive_body = repo / ARCHIVE_REL / slug
        if not archive_body.is_dir():
            continue
        row = _row_from_stub(repo, slug, slug_dir, archive_body)
        if row is not None:
            archived_rows.append(row)

    # (b) nested + flat-full hot bodies → active
    for dir_theme, slug, slug_dir in iter_hot_bodies(repo):
        if is_stub_dir(slug_dir, repo, tracked_override):
            continue
        source = choose_source_card(slug_dir)
        source_text = (
            source.read_text(encoding="utf-8") if source is not None else ""
        )
        stamped = parse_theme(source_text) if source is not None else "_inbox"
        theme = _resolve_scan_theme(stamped, dir_theme)
        active_rows.append(_row_from_full_dir(repo, slug, slug_dir, theme))

    return active_rows + archived_rows


def _render_active_table(rows: list[CatalogRow]) -> str:
    lines = [
        "| slug | theme | status | hot | one-liner | body | heavy |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        hot = row.hot or "yes"
        lines.append(
            "| "
            + " | ".join(
                _escape_cell(v)
                for v in (
                    row.slug,
                    row.theme,
                    row.status,
                    hot,
                    row.one_liner,
                    row.body,
                    row.heavy,
                )
            )
            + " |"
        )
    return "\n".join(lines)


def _render_archived_table(rows: list[CatalogRow]) -> str:
    lines = [
        "| slug | status | one-liner | card | body | heavy | closed |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                _escape_cell(v)
                for v in (
                    row.slug,
                    row.status,
                    row.one_liner,
                    row.card,
                    row.body,
                    row.heavy,
                    row.closed,
                )
            )
            + " |"
        )
    return "\n".join(lines)


def render_catalog(rows: list[CatalogRow]) -> str:
    """Render lab/CATALOG.md from scan rows.

    Active rows are grouped under ``### <theme>`` subsections in ``THEME_ORDER``;
    empty themes are omitted. Archived stays a single flat table (no theme col).
    """
    active = [r for r in rows if r.body.startswith(f"{ANALYSIS_REL}/")]
    archived = [r for r in rows if r.body.startswith(f"{ARCHIVE_REL}/")]
    parts = [_CATALOG_HEADER.rstrip(), "", "## Active", ""]
    if not active:
        parts.append("_No active studies._")
    else:
        by_theme: dict[str, list[CatalogRow]] = {t: [] for t in THEME_ORDER}
        for row in active:
            theme = row.theme if row.theme in THEMES else "_inbox"
            by_theme[theme].append(row)
        theme_blocks: list[str] = []
        for theme in THEME_ORDER:
            theme_rows = by_theme[theme]
            if not theme_rows:
                continue
            theme_blocks.append(
                f"### {theme}\n\n{_render_active_table(theme_rows)}"
            )
        parts.append("\n\n".join(theme_blocks))
    parts.extend(["", "## Archived", ""])
    parts.append(
        _render_archived_table(archived) if archived else "_No archived studies._"
    )
    return "\n".join(parts) + "\n"


def write_catalog(repo: Path, text: str) -> None:
    path = repo / CATALOG_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _normalize_catalog_text(text: str) -> str:
    """Normalize catalog markdown for render-diff comparison."""
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip() + "\n"


def _one_liners_from_catalog(text: str) -> dict[str, str]:
    """Slug → one-liner from an on-disk CATALOG, header-name keyed."""
    out: dict[str, str] = {}
    one_i: int | None = None
    for raw in text.splitlines():
        if not raw.startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if not cells:
            continue
        lower = [c.lower() for c in cells]
        if "slug" in lower and "one-liner" in lower:
            one_i = lower.index("one-liner")
            continue
        if one_i is None or set(cells[0]) <= set("-: "):
            continue
        if one_i < len(cells):
            out[cells[0]] = cells[one_i]
    return out


def _preserve_authored_one_liners(
    rows: list[CatalogRow], existing: dict[str, str]
) -> list[CatalogRow]:
    """Keep committed CATALOG one-liners; drop the old HOLD-coerce 'archive owed' prefix."""
    out: list[CatalogRow] = []
    for row in rows:
        old = existing.get(row.slug)
        # Only keep committed prose when the scan cannot derive a one-liner
        # (same contract as --check). Non-empty scan text wins so freshness
        # stays green; "archive owed (…)" prefixes are never preserved.
        if (
            old
            and not _is_empty_one_liner(old)
            and (
                _is_empty_one_liner(row.one_liner)
                or _scan_one_liner_is_truncation(row.one_liner, old)
            )
            and not re.match(r"(?i)archive\s+owed\s*\(", old)
        ):
            out.append(replace(row, one_liner=old))
        else:
            out.append(row)
    return out


def regenerate_catalog(
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> str:
    existing: dict[str, str] = {}
    path = repo / CATALOG_REL
    if path.is_file():
        existing = _one_liners_from_catalog(path.read_text(encoding="utf-8"))
    rows = scan_lab(repo, tracked_override=tracked_override)
    if existing:
        rows = _preserve_authored_one_liners(rows, existing)
    text = render_catalog(rows)
    write_catalog(repo, text)
    return text


def rewrite_sibling_links(text: str, slug: str, repo: Path) -> str:
    """Rewrite ](../other_slug/...) to lab/analysis|archive/other_slug/..."""

    def repl(m: re.Match[str]) -> str:
        target = m.group(2)
        if not target.startswith("../"):
            return m.group(0)
        rest = target[3:]
        if rest == ".." or rest.startswith("../"):
            # Multi-hop relative link (e.g. ../../docs/...) - not a
            # sibling-slug reference. Treating the leftover ".." as a slug
            # name would splice ARCHIVE_REL onto an already-correct path.
            return m.group(0)
        other = rest.split("/", 1)[0]
        if other == slug:
            return m.group(0)
        if (repo / ARCHIVE_REL / other).is_dir():
            prefix = f"{ARCHIVE_REL}/{other}"
        else:
            hot = resolve_hot_dir(repo, other)
            if hot is not None:
                try:
                    prefix = hot.relative_to(repo).as_posix()
                except ValueError:
                    prefix = f"{ANALYSIS_REL}/{other}"
            else:
                prefix = f"{ANALYSIS_REL}/{other}"
        tail = rest[len(other) :].lstrip("/")
        new = f"{prefix}/{tail}" if tail else f"{prefix}/"
        return f"{m.group(1)}{new}{m.group(3)}"

    return _MARKDOWN_LINK_RE.sub(repl, text)


_CAMPAIGN_ID_IN_PROSE = re.compile(
    r"\b(?:Q|H|GSUB|MNQBASE|OPENPRESS|MYM|SLR|ST)-[A-Z0-9]+(?:-[A-Z0-9]+)*"
)


def _truncate_one_liner(one_liner: str, limit: int = 80) -> str:
    """Cap stub/catalog one-liners without slicing a campaign ID.

    Coverage joins CATALOG prose to ``docs/briefs/closures/<id>-closure-*.md``.
    Truncating ``Q-TNEC-ENV-1`` to ``Q-TNEC-ENV...`` invents a missing-closure
    claim for an ID that has no file.
    """
    if len(one_liner) <= limit:
        return one_liner
    cut = max(limit - 3, 0)
    for m in _CAMPAIGN_ID_IN_PROSE.finditer(one_liner):
        if m.start() < cut < m.end():
            cut = m.end()
    return one_liner[:cut] + "..."


def build_stub(
    slug: str,
    disp: Disposition,
    decisive_name: str,
    archived_date: str,
) -> str:
    """Build hot CARD.md stub per spec §2.2."""
    one_liner = _clean_one_liner(disp.one_liner, disp.status) or disp.one_liner
    if one_liner.upper() == disp.status.upper():
        one_liner = ""
    one_liner = _truncate_one_liner(one_liner)
    disposition_line = (
        f"**Disposition:** {disp.status} — {one_liner}\n"
        if one_liner
        else f"**Disposition:** {disp.status}\n"
    )
    return (
        f"# {slug}\n"
        f"\n"
        f"{disposition_line}"
        f"**Archived:** {archived_date}\n"
        f"**Body:** [`lab/archive/{slug}/`](../../archive/{slug}/)\n"
        f"**Source card:** [`{decisive_name}`](../../archive/{slug}/{decisive_name})\n"
        f"\n"
        f"> Open [`lab/CATALOG.md`](../../CATALOG.md) for the full registry.\n"
        f"> Re-run harness from the body path, not from this stub.\n"
    )


def _hot_sys_path_dependent(
    repo: Path,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> str | None:
    """Return consumer slug if a full analysis dir sys.path-imports this slug."""
    needle = slug.replace("\\", "/")
    for _dir_theme, other_slug, slug_dir in iter_hot_bodies(repo):
        if other_slug == slug:
            continue
        if is_stub_dir(slug_dir, repo, tracked_override):
            continue
        for py_file in slug_dir.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
            except OSError:
                continue
            for m in _SYS_PATH_SLUG_RE.finditer(text):
                captured = m.group(1).replace("\\", "/")
                if captured == slug or captured == needle:
                    return other_slug
    return None


def _is_living_surface_path(repo: Path, path: Path) -> bool:
    try:
        rel = path.relative_to(repo).as_posix()
    except ValueError:
        return False
    if rel.startswith(_SKIP_LIVING_PREFIX):
        return False
    if rel in _LIVING_FILES:
        return True
    for root in _LIVING_ROOTS:
        if rel == root or rel.startswith(f"{root}/"):
            return True
    return False


def _iter_living_surface_files(repo: Path):
    for name in _LIVING_FILES:
        path = repo / name
        if path.is_file():
            yield path
    for root_name in _LIVING_ROOTS:
        root = repo / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file() and _is_living_surface_path(repo, path):
                if path.suffix.lower() in _TEXT_SUFFIXES or path.suffix == "":
                    yield path


def _analysis_path_needles(slug: str) -> list[str]:
    """Flat and theme-nested citation forms for ``lab/analysis/.../<slug>``."""
    needles = [f"{ANALYSIS_REL}/{slug}", f"{ANALYSIS_REL}\\{slug}"]
    for theme in THEME_ORDER:
        needles.append(f"{ANALYSIS_REL}/{theme}/{slug}")
        needles.append(f"{ANALYSIS_REL}\\{theme}\\{slug}")
    return needles


def _scan_inbound_citations(repo: Path, slug: str) -> list[str]:
    needles = _analysis_path_needles(slug)
    canonical = f"{ANALYSIS_REL}/{slug}"
    hits: list[str] = []
    for path in _iter_living_surface_files(repo):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if any(needle in text for needle in needles):
            hits.append(
                f"{path.relative_to(repo).as_posix()}: {canonical}"
            )
    return sorted(hits)


def _scan_outbound_sibling_links(slug_dir: Path) -> list[str]:
    hits: list[str] = []
    if not slug_dir.is_dir():
        return hits
    for md_path in slug_dir.rglob("*.md"):
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in _OUTBOUND_SIBLING_RE.finditer(text):
            rel = md_path.relative_to(slug_dir).as_posix()
            hits.append(f"{rel}: ../{m.group(1)}")
    return sorted(hits)


def _scan_python_coupling(
    repo: Path,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> list[str]:
    hits: list[str] = []
    consumer = _hot_sys_path_dependent(repo, slug, tracked_override)
    if consumer is not None:
        hits.append(f"hot sys.path dependent: {consumer}")
    needle = slug.replace("\\", "/")
    for _dir_theme, _other_slug, slug_dir in iter_hot_bodies(repo):
        if is_stub_dir(slug_dir, repo, tracked_override):
            continue
        for py_file in slug_dir.rglob("*.py"):
            try:
                text = py_file.read_text(encoding="utf-8")
            except OSError:
                continue
            for m in _LAB_SLUG_PATH_RE.finditer(text):
                if m.group(1).replace("\\", "/") == needle:
                    rel = py_file.relative_to(repo).as_posix()
                    hits.append(f"{rel}: references lab/analysis/{slug}")
    return sorted(dict.fromkeys(hits))


def _scan_untracked_leftovers(
    repo: Path,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> list[str]:
    slug_dir = resolve_body_dir(repo, slug, tracked_override)
    if slug_dir is None or not slug_dir.is_dir():
        return []
    try:
        prefix = slug_dir.relative_to(repo).as_posix() + "/"
    except ValueError:
        prefix = f"{ANALYSIS_REL}/{slug}/"
    if tracked_override is not None:
        tracked = tracked_override.get(slug, frozenset())
    else:
        tracked = _tracked_under_prefix(repo, prefix, slug, None)
    tracked_names = {
        p[len(prefix) :] for p in tracked if p.startswith(prefix)
    }
    leftovers: list[str] = []
    for path in slug_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(slug_dir).as_posix()
        if rel not in tracked_names:
            leftovers.append(rel)
    return sorted(leftovers)


def dependency_report(
    repo: Path,
    slug: str,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> str:
    """Inbound citations, outbound ../ links, python paths, untracked leftovers."""
    slug_dir = resolve_body_dir(repo, slug, tracked_override) or (
        repo / ANALYSIS_REL / slug
    )
    sections: list[str] = [f"# Dependency report: {slug}", ""]

    inbound = _scan_inbound_citations(repo, slug)
    sections.extend(["## Inbound citations", ""])
    if inbound:
        sections.extend(f"- {hit}" for hit in inbound)
    else:
        sections.append("_none_")
    sections.append("")

    outbound = _scan_outbound_sibling_links(slug_dir)
    sections.extend(["## Outbound sibling links", ""])
    if outbound:
        sections.extend(f"- {hit}" for hit in outbound)
    else:
        sections.append("_none_")
    sections.append("")

    python_hits = _scan_python_coupling(repo, slug, tracked_override)
    sections.extend(["## Python path coupling", ""])
    if python_hits:
        sections.extend(f"- {hit}" for hit in python_hits)
    else:
        sections.append("_none_")
    sections.append("")

    leftovers = _scan_untracked_leftovers(repo, slug, tracked_override)
    sections.extend(["## Untracked leftovers", ""])
    if leftovers:
        sections.extend(f"- {name}" for name in leftovers)
    else:
        sections.append("_none_")
    sections.append("")

    return "\n".join(sections)


_CATALOG_STALE = "CATALOG.md stale vs scan"
_EMPTY_ONE_LINER_SENTINELS = frozenset({"", "—", "-", "–"})


@dataclass(frozen=True)
class InventoryRow:
    """Wave-0 inventory line — not a permanent third index."""

    slug: str
    cls: str  # archiveable | hold | active
    theme: str
    status: str
    one_liner: str


def _is_empty_one_liner(one_liner: str) -> bool:
    return (one_liner or "").strip() in _EMPTY_ONE_LINER_SENTINELS


def _scan_one_liner_is_truncation(scan: str, disk: str) -> bool:
    """True when ``scan`` is a mechanical truncation, so ``disk`` may keep
    untruncated Status prose *or* a complete hand-authored summary.

    ``parse_disposition`` caps one-liners at 120 (``text[:117] + '...'``).
    Stub CARD dispositions use ``_truncate_one_liner`` (default 80). Either
    cap is a fallback: treating a complete committed cell as stale would
    hard-fail every long Status line and fight hand-authored catalog
    summaries. ``--check --catalog-only`` stays green without
    ``--regenerate-catalog`` clobbering the committed cell.

    The 117-char cap itself is left in place. Raising it would make more
    Status lines fit entirely, after which a concise rewrite would look like
    ordinary one-liner drift and get fought. Complete authored cells that
    themselves still end in ``...`` are *not* tolerated — those are a second
    dangling cut, not a summary.
    """
    if not scan or not disk:
        return False
    if not scan.endswith("..."):
        return False
    # Untruncated Status prose (disk is a prefix-extension of the scan).
    prefix = scan[:-3]
    if prefix and len(disk) > len(prefix) and disk.startswith(prefix):
        return True
    # Complete hand-authored summary (not itself a dangling truncation).
    return not disk.rstrip().endswith("...") and not _is_empty_one_liner(disk)


def _inventory_class(status: str) -> str:
    if is_archiveable(status):
        return "archiveable"
    if status == "HOLD":
        return "hold"
    return "active"


def inventory_lab(
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> list[InventoryRow]:
    """Classify every hot full body as archiveable / hold / active (Wave 0)."""
    rows: list[InventoryRow] = []
    for dir_theme, slug, slug_dir in iter_hot_bodies(repo):
        if is_stub_dir(slug_dir, repo, tracked_override):
            continue
        source = choose_source_card(slug_dir)
        source_text = (
            source.read_text(encoding="utf-8") if source is not None else ""
        )
        stamped = parse_theme(source_text) if source is not None else "_inbox"
        theme = _resolve_scan_theme(stamped, dir_theme)
        disp = parse_disposition(source_text) if source is not None else None
        status = disp.status if disp else "ACTIVE"
        one_liner = disp.one_liner if disp else "—"
        if _is_empty_one_liner(one_liner):
            one_liner = "—"
        rows.append(
            InventoryRow(
                slug=slug,
                cls=_inventory_class(status),
                theme=theme,
                status=status,
                one_liner=one_liner,
            )
        )
    return rows


def render_inventory(rows: list[InventoryRow]) -> str:
    """TSV: slug, class, theme, status, one_liner."""
    lines = [
        f"{r.slug}\t{r.cls}\t{r.theme}\t{r.status}\t{r.one_liner}" for r in rows
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def _theme_mismatch_issue(dir_theme: str, stamped: str, slug: str) -> str | None:
    """Issue when directory theme and stamp are both real and disagree."""
    if (
        dir_theme in THEMES
        and dir_theme != "_inbox"
        and stamped in THEMES
        and stamped != "_inbox"
        and dir_theme != stamped
    ):
        return f"theme mismatch: {slug} dir={dir_theme} stamp={stamped}"
    return None

# Active (7-col): slug, theme, status, hot, one-liner, body, heavy.
# Archived (7-col): slug, status, one-liner, card, body, heavy, closed.
# Legacy Active (6-col, no `hot`) is still accepted by the splitter so a
# mid-transition --check can name the schema drift instead of dropping rows.
_ACTIVE_COLS = 7
_ACTIVE_COLS_LEGACY = 6
_ARCHIVED_COLS = 7


def _split_catalog_row(line: str) -> list[str] | None:
    """Split a machine-rendered catalog data row into its cells, else None.

    Accepts Active (7-col, or legacy 6-col) and Archived (7-col) schemas. Renderers join cells
    with ``" | "`` and wrap them in ``"| … |"``; ``_escape_cell`` only turns
    ``|`` into ``\\|`` (which carries no surrounding spaces), so the ``" | "``
    delimiter is unambiguous. The ``|---|`` separator (no spaces) and non-table
    lines return None; the header row parses as cells but is filtered by the
    caller via ``cells[0] == "slug"``.
    """
    s = line.strip()
    if len(s) < 2 or not s.startswith("|") or not s.endswith("|"):
        return None
    cells = [c.strip() for c in s[1:-1].split(" | ")]
    if len(cells) not in (_ACTIVE_COLS, _ACTIVE_COLS_LEGACY, _ARCHIVED_COLS):
        return None
    return cells


def _partition_catalog(
    text: str,
) -> tuple[list[str], dict[tuple[str, str], list[str]], list[tuple[str, str]]]:
    """Split a rendered catalog into (structural lines, rows, same-section dupes).

    Structural = everything that is not a data row: preamble, section headers,
    theme subsections, the table header + separator, empty-state sentinels.
    Data rows are keyed by ``(section, slug)`` where ``section`` is ``active`` or
    ``archived`` (from the nearest ``## Active`` / ``## Archived`` heading). A
    slug may appear once per section; same-section repeats are recorded in
    ``dupes``. Cross-section presence (Active+Archived) is NOT collapsed — the
    comparator sees both keys so a phantom Active row cannot be overwritten by
    the Archived twin (2026-08-13 MSL false-pass).
    """
    struct: list[str] = []
    rows: dict[tuple[str, str], list[str]] = {}
    dupes: list[tuple[str, str]] = []
    section: str | None = None
    for line in _normalize_catalog_text(text).splitlines():
        stripped = line.strip()
        if stripped == "## Active":
            section = "active"
            struct.append(line)
            continue
        if stripped == "## Archived":
            section = "archived"
            struct.append(line)
            continue
        cells = _split_catalog_row(line)
        if cells is not None and cells[0] != "slug":
            key = (section or "unknown", cells[0])
            if key in rows:
                dupes.append(key)
            rows[key] = cells
        else:
            struct.append(line)
    return struct, rows, dupes


def _status_cells_compatible(disk: str, exp: str) -> bool:
    """True when disk Status equals scan token, or is a hand parenthetical on it.

    Claim-alignment M11/M45 require hand-edited CATALOG Status cells such as
    ``ACTIVE (one headline RETRACTED …)`` while ``render_catalog`` still emits the
    normalized token ``ACTIVE``. Regenerating would clobber those flags (and the
    heavy column on bare worktrees), so freshness tolerates annotations that
    ``_normalize_status`` maps back to the expected token.
    """
    if disk == exp:
        return True
    norm = _normalize_status(disk)
    return norm is not None and norm == exp


def _compare_catalog(on_disk: str, expected: str) -> tuple[list[str], list[str]]:
    """Structured freshness compare tolerant of scanner-unverifiable cells.

    Returns ``(issues, warnings)``. ``issues == []`` means the catalog is fresh
    except (possibly) for (a) the `heavy` column when gitignored artifacts are
    absent here, and (b) a one-liner that the scan cannot derive because
    ``choose_source_card`` found no RESULTS*/README/verdict/CLOSURE (committed
    hand-authored prose retained). Those rows warn, mirroring the sibling
    ``check_pine_manifest`` / ``check_data_manifests`` public-clone soft-degrade.
    A scan one-liner that is a mechanical truncation (``parse_disposition``'s
    120-char cap, or a stub ``_truncate_one_liner`` cut) of the committed cell
    — or that the committed cell replaced with a complete hand-authored
    summary — is also tolerated (silent — the cap is mechanical).
    Hand parenthetical Status annotations that normalize to the scanned token are
    also tolerated (M11/M45). Any other drift (new/removed/renamed slug,
    phantom Active beside Archived, same-section duplicate slug, status/body/
    card/closed change, non-empty one-liner drift, structural edit, or a `heavy`
    change while the artifacts are present) hard-fails.
    """
    disk_struct, disk_rows, disk_dups = _partition_catalog(on_disk)
    exp_struct, exp_rows, exp_dups = _partition_catalog(expected)

    # Same-section duplicate slug: last-wins would hide the earlier row.
    if disk_dups or exp_dups:
        return ([_CATALOG_STALE], [])

    # Preamble / section headers / table header / empty-state must match exactly.
    if disk_struct != exp_struct:
        return ([_CATALOG_STALE], [])
    # A new / removed / renamed study — or a section move (Active↔Archived) — is
    # a (section, slug)-set delta: real drift, even on a bare worktree. Cross-
    # section phantom Active rows surface here instead of silently overwriting.
    if set(disk_rows) != set(exp_rows):
        return ([_CATALOG_STALE], [])

    warnings: list[str] = []
    for key in exp_rows:
        _section, slug = key
        disk_cells = disk_rows[key]
        exp_cells = exp_rows[key]
        if disk_cells == exp_cells:
            continue
        if len(disk_cells) != len(exp_cells):
            return ([_CATALOG_STALE], warnings)
        # Active 7-col: slug, theme, status, hot, one-liner, body, heavy.
        # Archived 7-col: slug, status, one-liner, card, body, heavy, closed.
        # Distinguish by section — both schemas are 7 cells.
        if _section == "active":
            status_i, one_liner_i, heavy_i = 2, 4, 6
        else:
            status_i, one_liner_i, heavy_i = 1, 2, 5
        for i in range(len(disk_cells)):
            if i == heavy_i:
                continue
            if disk_cells[i] == exp_cells[i]:
                continue
            if i == status_i:
                if not _status_cells_compatible(disk_cells[i], exp_cells[i]):
                    return ([_CATALOG_STALE], warnings)
                continue
            if i == one_liner_i:
                # Tolerate committed prose when the scan cannot derive a one-liner
                # (no choose_source_card hit -> empty). Opposite direction and
                # non-empty!=non-empty drift stay hard-fails.
                if _is_empty_one_liner(exp_cells[i]) and not _is_empty_one_liner(
                    disk_cells[i]
                ):
                    warnings.append(
                        f'{slug}: one-liner unverifiable from source card '
                        f'(committed prose retained; scan saw empty)'
                    )
                    continue
                # Mechanical cap: committed CATALOG may keep the untruncated
                # Status prose or a complete hand-authored summary.
                if _scan_one_liner_is_truncation(exp_cells[i], disk_cells[i]):
                    continue
                return ([_CATALOG_STALE], warnings)
            return ([_CATALOG_STALE], warnings)
        # Tolerate ONLY a heavy downgrade caused by the study's gitignored heavy
        # artifacts being absent here: committed (generated where the bytes exist)
        # annotated the column; the scan here sees "—" because they were never
        # checked out. ``exp == "—"`` IS the "absent in this environment" signal —
        # so committed "—" → scanned annotation (files added but catalog not
        # regenerated) is the opposite direction and stays a hard-fail.
        if disk_cells[heavy_i] == exp_cells[heavy_i]:
            continue
        if (
            disk_cells[heavy_i] in _HEAVY_GITIGNORED
            and exp_cells[heavy_i] == _HEAVY_NONE
        ):
            warnings.append(
                f"{slug}: heavy artifacts gitignored and absent from this "
                f"checkout (committed {disk_cells[heavy_i]!r}, not verified)"
            )
            continue
        return ([_CATALOG_STALE], warnings)

    return ([], warnings)


def check_catalog_stale(
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> list[str]:
    """Return ``[CATALOG.md stale vs scan]`` when on-disk catalog ≠ rescan.

    Tolerant of scanner-unverifiable cells a worktree / clone cannot avoid:
    ``heavy`` (gitignored artifacts absent) and hand-authored one-liners when
    ``choose_source_card`` finds no RESULTS*/README/verdict/CLOSURE (scan emits
    empty). Those rows warn (stderr) instead of hard-failing, mirroring
    ``check_pine_manifest`` / ``check_data_manifests``. All other drift still
    hard-fails. On the primary tree the fast path below is byte-identical to
    the prior behaviour.
    """
    catalog_path = repo / CATALOG_REL
    if not catalog_path.is_file():
        return [_CATALOG_STALE]
    expected = render_catalog(scan_lab(repo, tracked_override=tracked_override))
    try:
        on_disk = catalog_path.read_text(encoding="utf-8")
    except OSError:
        on_disk = ""
    if _normalize_catalog_text(on_disk) == _normalize_catalog_text(expected):
        return []
    issues, warnings = _compare_catalog(on_disk, expected)
    for w in warnings:
        kind = "one-liner" if "one-liner unverifiable" in w else "heavy-column"
        print(f"WARN lab/CATALOG {kind} unverified: {w}", file=sys.stderr)
    return issues


def warn_new_slug_same_theme_collisions(
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
) -> None:
    """Report-only WARN when an untracked hot body shares a CATALOG theme.

    Fires when a new, not-yet-committed ``lab/analysis/<theme>/<slug>/`` directory
    shares its theme with existing Active ``CATALOG.md`` rows. Fail-open: prints
    to stderr and never contributes to the issue list / exit code. Grounding:
    ADR 2026-08-13 §2 leg 3 / §5 (explicitly forbidden to harden into a block).
    """
    catalog_path = repo / CATALOG_REL
    if not catalog_path.is_file():
        return
    try:
        on_disk = catalog_path.read_text(encoding="utf-8")
    except OSError:
        return
    _, catalog_rows, _dupes = _partition_catalog(on_disk)
    catalogued_slugs = {slug for _section, slug in catalog_rows}
    by_theme: dict[str, list[tuple[str, str]]] = {}
    for (_section, slug), cells in catalog_rows.items():
        if _section != "active":
            continue
        if len(cells) not in {_ACTIVE_COLS, _ACTIVE_COLS_LEGACY}:
            continue
        theme = cells[1]
        one_liner = cells[4] if len(cells) == _ACTIVE_COLS else cells[3]
        by_theme.setdefault(theme, []).append((slug, one_liner))

    for dir_theme, slug, _slug_dir in iter_hot_bodies(repo):
        if not is_theme_dir_name(dir_theme):
            continue
        if slug in catalogued_slugs:
            # Already catalogued — checkout/gitignore gaps are not "new" work.
            continue
        prefix = f"{ANALYSIS_REL}/{dir_theme}/{slug}/"
        tracked = _tracked_under_prefix(repo, prefix, slug, tracked_override)
        if tracked:
            continue
        peers = [(s, ol) for s, ol in by_theme.get(dir_theme, []) if s != slug]
        if not peers:
            continue
        print(
            f"WARN new-slug same-theme collision: {prefix} is untracked under "
            f"theme {dir_theme!r}; existing CATALOG rows share this theme — "
            f"read before treating as new work:",
            file=sys.stderr,
        )
        for peer_slug, one_liner in peers:
            print(f"  - {peer_slug}: {one_liner}", file=sys.stderr)
        log_fire("archive_lab_analysis_theme_warn", slug=slug, theme=dir_theme, n_peers=len(peers))


def check_lab(
    repo: Path,
    tracked_override: dict[str, frozenset[str]] | None = None,
    *,
    catalog_only: bool = False,
    require_one_liners: bool = True,
) -> list[str]:
    """Return drift issue strings; empty list means OK.

    ``catalog_only=True`` checks only that ``lab/CATALOG.md`` matches a fresh
    scan (the always-on pre-commit / ``make check`` surface). Full mode also
    flags stub/archive shape drift and unstubbed archiveable closes — those stay
    operator-fired (archive via ``--slug``); do not HARD-gate them until the
    STM set is intentionally clean.

    ``require_one_liners`` (default True since Wave 3 / Task 10) hard-fails
    empty Active/HOLD one-liners on hot bodies. ``catalog_only`` ignores this
    gate (stale-catalog only). Flat full-dir remnants after theme dirs exist
    are WARN-only (stderr), not issues.

    Always emits the report-only new-slug / same-theme collision WARN (ADR
    2026-08-13) before returning — never folded into the returned issues list.
    """
    warn_new_slug_same_theme_collisions(repo, tracked_override)

    if catalog_only:
        return check_catalog_stale(repo, tracked_override)

    issues: list[str] = []
    analysis_root = repo / ANALYSIS_REL
    archive_root = repo / ARCHIVE_REL

    archive_slugs: set[str] = set()
    if archive_root.is_dir():
        archive_slugs = {
            d.name for d in archive_root.iterdir() if d.is_dir()
        }

    # Flat stub / dual-presence checks — skip closed-set theme directories.
    analysis_slugs: set[str] = set()
    if analysis_root.is_dir():
        for slug_dir in sorted(analysis_root.iterdir()):
            if not slug_dir.is_dir() or is_theme_dir_name(slug_dir.name):
                continue
            slug = slug_dir.name
            analysis_slugs.add(slug)
            prefix = f"{ANALYSIS_REL}/{slug}/"
            expected_tracked = frozenset({f"{prefix}CARD.md"})
            tracked = _tracked_under_slug(repo, slug, tracked_override)

            if (
                slug in archive_slugs
                and tracked
                and tracked != expected_tracked
                and f"{prefix}CARD.md" in tracked
            ):
                issues.append(
                    f"stub {slug}: tracked tree is not exactly CARD.md "
                    f"({sorted(tracked)})"
                )

            if is_stub_dir(slug_dir, repo, tracked_override):
                if tracked and tracked != expected_tracked:
                    issues.append(
                        f"stub {slug}: tracked tree is not exactly CARD.md "
                        f"({sorted(tracked)})"
                    )
                elif (
                    not tracked
                    and (slug_dir / "CARD.md").is_file()
                    and any(
                        p.is_file() and p.name != "CARD.md"
                        for p in slug_dir.iterdir()
                    )
                ):
                    extras = sorted(
                        p.name
                        for p in slug_dir.iterdir()
                        if p.is_file() and p.name != "CARD.md"
                    )
                    issues.append(
                        f"stub {slug}: on-disk tree is not exactly CARD.md "
                        f"(extra: {extras})"
                    )
                if slug not in archive_slugs:
                    issues.append(f"archived stub {slug}: missing archive body")
            elif slug in archive_slugs:
                issues.append(
                    f"{slug}: full analysis dir and archive body both present"
                )

    # Hot bodies (nested + flat): unstubbed closes, theme mismatch, one-liners.
    layout_active = theme_layout_active(repo)
    for dir_theme, slug, slug_dir in iter_hot_bodies(repo):
        if is_stub_dir(slug_dir, repo, tracked_override):
            continue
        if layout_active:
            try:
                if slug_dir.resolve().parent == analysis_root.resolve():
                    print(
                        f"WARN flat full dir remnant: {slug}",
                        file=sys.stderr,
                    )
            except OSError:
                pass

        source = choose_source_card(slug_dir)
        source_text = ""
        if source is not None:
            try:
                source_text = source.read_text(encoding="utf-8")
            except OSError:
                source_text = ""
        stamped = parse_theme(source_text) if source_text else "_inbox"
        mismatch = _theme_mismatch_issue(dir_theme, stamped, slug)
        if mismatch is not None:
            issues.append(mismatch)

        disp = parse_disposition(source_text) if source_text else None
        if disp is not None and is_archiveable(disp.status):
            issues.append(
                f"{slug}: archiveable disposition but still full dir "
                f"(unstubbed close)"
            )
        elif require_one_liners:
            one = disp.one_liner if disp is not None else "—"
            if _is_empty_one_liner(one):
                issues.append(f"empty one-liner: {slug}")

    for slug in sorted(archive_slugs):
        if slug not in analysis_slugs:
            issues.append(f"archive body {slug}: missing analysis stub dir")
            continue
        slug_dir = analysis_root / slug
        if not is_stub_dir(slug_dir, repo, tracked_override):
            issues.append(
                f"archive body {slug}: analysis dir is not stub-only"
            )

    issues.extend(check_catalog_stale(repo, tracked_override))
    return issues


def _rewrite_md_sibling_links(repo: Path, slug: str, body_dir: Path) -> int:
    count = 0
    for md_path in body_dir.rglob("*.md"):
        original = md_path.read_text(encoding="utf-8")
        rewritten = rewrite_sibling_links(original, slug, repo)
        if rewritten != original:
            md_path.write_text(rewritten, encoding="utf-8")
            count += 1
    return count


def _git_mv(repo: Path, src: Path, dst: Path) -> None:
    """``git mv`` with copy+rm fallback when rename hits EXDEV (overlay FS)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "mv", str(src), str(dst)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return
    err = f"{result.stderr or ''}{result.stdout or ''}"
    if "Invalid cross-device link" not in err:
        raise subprocess.CalledProcessError(
            result.returncode,
            result.args,
            output=result.stdout,
            stderr=result.stderr,
        )
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    rm = subprocess.run(
        ["git", "rm", "-r", str(src)],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if rm.returncode != 0:
        shutil.rmtree(src, ignore_errors=True)
    elif src.exists():
        shutil.rmtree(src, ignore_errors=True)
    subprocess.run(["git", "add", "-A", str(dst)], cwd=repo, check=True)


def _move_archive_to_analysis(
    repo: Path,
    slug: str,
    *,
    use_git: bool,
    dest: Path | None = None,
) -> None:
    src = repo / ARCHIVE_REL / slug
    dst = dest if dest is not None else repo / ANALYSIS_REL / slug
    dst.parent.mkdir(parents=True, exist_ok=True)
    if use_git:
        _git_mv(repo, src, dst)
    else:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))


def _remove_stub_dir(
    repo: Path,
    slug: str,
    *,
    use_git: bool,
) -> None:
    stub_dir = repo / ANALYSIS_REL / slug
    card = stub_dir / "CARD.md"
    if use_git:
        try:
            subprocess.run(
                ["git", "rm", "-f", str(card)],
                cwd=repo,
                check=True,
            )
        except subprocess.CalledProcessError:
            if card.is_file():
                card.unlink()
    elif card.is_file():
        card.unlink()
    if stub_dir.is_dir():
        for child in list(stub_dir.iterdir()):
            if child.is_file():
                child.unlink()
        try:
            stub_dir.rmdir()
        except OSError:
            pass


def _ensure_theme_stamp(body_dir: Path, theme: str) -> None:
    """Insert ``**Theme:**`` on the decisive card when the field is missing."""
    source = choose_source_card(body_dir)
    if source is None:
        return
    try:
        text = source.read_text(encoding="utf-8")
    except OSError:
        return
    head = "\n".join(text.splitlines()[:FIELD_HEAD_LINES])
    if _THEME_LINE_RE.search(head):
        return
    source.write_text(f"**Theme:** {theme}\n{text}", encoding="utf-8")


def unarchive_slug(
    repo: Path,
    slug: str,
    *,
    dry_run: bool = False,
    use_git: bool = True,
    tracked_override: dict[str, frozenset[str]] | None = None,
    theme: str | None = None,
) -> Path:
    """Move body from lab/archive/ back to lab/analysis/; remove stub.

    Returns the restore destination directory. When theme layout is active,
    ``theme`` is required and the body lands at ``analysis/<theme>/<slug>/``.
    Pre-nest trees (no theme dirs) restore flat unless ``theme`` is given.
    """
    archive_body = repo / ARCHIVE_REL / slug
    stub_dir = repo / ANALYSIS_REL / slug

    if not archive_body.is_dir():
        raise ArchiveError(f"missing archive body: {ARCHIVE_REL}/{slug}/")

    if not stub_dir.is_dir() or not is_stub_dir(
        stub_dir, repo, tracked_override
    ):
        raise ArchiveError(
            f"not archived (stub-only dir required): {ANALYSIS_REL}/{slug}/"
        )

    layout_active = theme_layout_active(repo)
    if layout_active and not theme:
        raise ArchiveError(
            "--theme required when theme layout is active under lab/analysis/"
        )
    if theme is not None and theme not in THEMES:
        raise ArchiveError(f"unknown theme: {theme}")

    if theme:
        dest = repo / ANALYSIS_REL / theme / slug
        dest_rel = f"{ANALYSIS_REL}/{theme}/{slug}/"
    else:
        dest = repo / ANALYSIS_REL / slug
        dest_rel = f"{ANALYSIS_REL}/{slug}/"

    if dry_run:
        print(
            f"[dry-run] would remove stub {ANALYSIS_REL}/{slug}/CARD.md"
        )
        print(
            f"[dry-run] would move {ARCHIVE_REL}/{slug}/ -> {dest_rel}"
        )
        print(f"[dry-run] would regenerate {CATALOG_REL}")
        return dest

    _remove_stub_dir(repo, slug, use_git=use_git)
    _move_archive_to_analysis(repo, slug, use_git=use_git, dest=dest)
    if theme:
        _ensure_theme_stamp(dest, theme)
    regenerate_catalog(repo)
    return dest


def _move_slug_tree(
    repo: Path,
    slug: str,
    *,
    use_git: bool,
    src: Path | None = None,
) -> None:
    source = src if src is not None else repo / ANALYSIS_REL / slug
    dst = repo / ARCHIVE_REL / slug
    dst.parent.mkdir(parents=True, exist_ok=True)
    parent = source.parent
    if use_git:
        _git_mv(repo, source, dst)
    else:
        shutil.move(str(source), str(dst))
    # Drop empty theme parent left behind after nested archive.
    if (
        parent.is_dir()
        and is_theme_dir_name(parent.name)
        and not any(parent.iterdir())
    ):
        try:
            parent.rmdir()
        except OSError:
            pass


def archive_slug(
    repo: Path,
    slug: str,
    *,
    dry_run: bool = False,
    use_git: bool = True,
    tracked_override: dict[str, frozenset[str]] | None = None,
    archived_date: str | None = None,
) -> ArchiveReport:
    """Move study body to lab/archive/, write flat CARD stub, regenerate catalog."""
    archive_body = repo / ARCHIVE_REL / slug
    flat_dir = repo / ANALYSIS_REL / slug
    slug_dir = resolve_body_dir(repo, slug, tracked_override)

    if slug_dir is None:
        if flat_dir.is_dir() and is_stub_dir(
            flat_dir, repo, tracked_override
        ) and archive_body.is_dir():
            raise ArchiveError(f"already archived: {slug}")
        raise ArchiveError(
            f"missing analysis dir: {ANALYSIS_REL}/[theme/]{slug}/"
        )

    if (
        flat_dir.is_dir()
        and is_stub_dir(flat_dir, repo, tracked_override)
        and archive_body.is_dir()
    ):
        raise ArchiveError(f"already archived: {slug}")

    source = choose_source_card(slug_dir)
    if source is None:
        raise ArchiveError(
            f"no source card under {slug_dir.relative_to(repo).as_posix()}/"
        )

    disp = parse_disposition(source.read_text(encoding="utf-8"))
    if disp is None or not is_archiveable(disp.status):
        raise ArchiveError(
            f"no archiveable disposition in {source.relative_to(repo)}"
        )

    dependent = _hot_sys_path_dependent(repo, slug, tracked_override)
    if dependent is not None:
        raise ArchiveError(
            f"hot sys.path dependent {dependent} still imports {ANALYSIS_REL}/{slug}"
        )

    decisive_name = disp.decisive_hint or source.name
    closed = archived_date or dt.date.today().isoformat()
    body_path = f"{ARCHIVE_REL}/{slug}/"
    stub_path = f"{ANALYSIS_REL}/{slug}/CARD.md"
    try:
        src_rel = slug_dir.relative_to(repo).as_posix()
    except ValueError:
        src_rel = f"{ANALYSIS_REL}/{slug}"

    if archive_body.exists():
        raise ArchiveError(f"archive body already exists: {body_path}")

    if dry_run:
        print(f"[dry-run] would move {src_rel}/ -> {body_path}")
        print(f"[dry-run] would write {stub_path}")
        print(f"[dry-run] decisive: {decisive_name}; archived: {closed}")
        print()
        print(dependency_report(repo, slug, tracked_override))
        return ArchiveReport(
            slug=slug,
            decisive_name=decisive_name,
            archived_date=closed,
            dry_run=True,
            body_path=body_path,
            stub_path=stub_path,
        )

    leftovers_before = _scan_untracked_leftovers(
        repo, slug, tracked_override
    )
    _move_slug_tree(repo, slug, use_git=use_git, src=slug_dir)
    _rewrite_md_sibling_links(repo, slug, archive_body)

    stub_dir = repo / ANALYSIS_REL / slug
    stub_dir.mkdir(parents=True, exist_ok=True)
    stub_text = build_stub(slug, disp, decisive_name, closed)
    (stub_dir / "CARD.md").write_text(stub_text, encoding="utf-8")

    regenerate_catalog(repo)

    if leftovers_before:
        print(
            f"warning: untracked leftovers remain under {src_rel}/: "
            + ", ".join(leftovers_before),
            file=sys.stderr,
        )

    return ArchiveReport(
        slug=slug,
        decisive_name=decisive_name,
        archived_date=closed,
        dry_run=False,
        body_path=body_path,
        stub_path=stub_path,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=None, help="repo root (default: inferred)")
    ap.add_argument(
        "--regenerate-catalog",
        action="store_true",
        help="rescan lab/analysis + lab/archive; rebuild lab/CATALOG.md",
    )
    ap.add_argument("--slug", metavar="NAME", help="archive one study slug")
    ap.add_argument(
        "--unarchive",
        metavar="NAME",
        help="restore archived study body to lab/analysis/",
    )
    ap.add_argument(
        "--theme",
        metavar="NAME",
        help="theme dir for --unarchive restore "
        "(required when any theme dir exists under lab/analysis/)",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="report lab/archive drift; exit 1 if any issues",
    )
    ap.add_argument(
        "--catalog-only",
        action="store_true",
        help="with --check: only require lab/CATALOG.md match a fresh scan "
        "(always-on gate; ignores unstubbed closes / stub shape)",
    )
    ap.add_argument(
        "--require-one-liners",
        action="store_true",
        help="deprecated no-op: full --check always hard-fails empty "
        "Active/HOLD one-liners (Wave 3); catalog-only stays stale-only",
    )
    ap.add_argument(
        "--inventory",
        action="store_true",
        help="print Wave-0 TSV inventory "
        "(slug/class/theme/status/one_liner); no files written",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="with --slug/--unarchive: print planned moves; write nothing",
    )
    args = ap.parse_args(argv)

    root = args.root if args.root else Path(__file__).resolve().parents[1]
    if args.catalog_only and not args.check:
        print("--catalog-only requires --check", file=sys.stderr)
        return 1
    if args.require_one_liners and not args.check:
        print("--require-one-liners requires --check", file=sys.stderr)
        return 1
    if args.inventory:
        sys.stdout.write(render_inventory(inventory_lab(root)))
        return 0
    if args.check:
        issues = check_lab(
            root,
            catalog_only=args.catalog_only,
            # Wave 3: full --check always requires one-liners; catalog_only
            # returns early and never consults this flag.
            require_one_liners=not args.catalog_only,
        )
        if issues:
            for issue in issues:
                print(issue, file=sys.stderr)
            if args.catalog_only and issues == [_CATALOG_STALE]:
                print(
                    "hint: python scripts/archive_lab_analysis.py "
                    "--regenerate-catalog",
                    file=sys.stderr,
                )
            return 1
        label = (
            "lab/CATALOG check: OK"
            if args.catalog_only
            else "lab/archive check: OK"
        )
        print(label)
        return 0
    if args.regenerate_catalog:
        text = regenerate_catalog(root)
        n_rows = sum(
            1
            for line in text.splitlines()
            if line.startswith("|") and not line.startswith("| slug") and "|---" not in line
        )
        print(f"Wrote {CATALOG_REL} ({n_rows} rows)")
        return 0
    if args.theme and not args.unarchive:
        print("--theme requires --unarchive", file=sys.stderr)
        return 1
    if args.unarchive:
        try:
            dest = unarchive_slug(
                root,
                args.unarchive,
                dry_run=args.dry_run,
                theme=args.theme,
            )
        except ArchiveError as exc:
            print(f"unarchive refused: {exc}", file=sys.stderr)
            return 1
        try:
            dest_rel = dest.relative_to(root).as_posix()
        except ValueError:
            dest_rel = str(dest)
        if args.dry_run:
            print(f"[dry-run] unarchive plan for {args.unarchive}")
        else:
            print(f"Unarchived {args.unarchive} -> {dest_rel}/")
        return 0
    if args.slug:
        try:
            report = archive_slug(root, args.slug, dry_run=args.dry_run)
        except ArchiveError as exc:
            print(f"archive refused: {exc}", file=sys.stderr)
            return 1
        if report.dry_run:
            print(f"[dry-run] archive plan for {report.slug}")
        else:
            print(
                f"Archived {report.slug} -> {report.body_path} "
                f"(stub {report.stub_path})"
            )
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
