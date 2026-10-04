#!/usr/bin/env python3
"""track_b_register.py — Track B status register: check, write, digest, table.

The register (`docs/governance/track_b_register.yml`) holds one row per Track B
item: a gate, packet, slice, checkpoint, drill or defect. Each row gives the
item's status now, the next permitted action and who takes it, and links the
record that set that status; the ledgers keep the reasoning and evidence.
`role: pilot` means the linked owners still govern and nothing is generated;
`role: owner` (the Rule 7 owner of item status) turns on the fixed mirrors in
GENERATED_TARGETS and is set by the change that wires them.

Subcommands:
  check   (default) exit 0 when every invariant below holds; exit 1 with one line
          per finding otherwise.
  write   regenerate the mirrors (role owner only), between
          `<!-- BEGIN generated: track-b-register ... -->` and its END marker.
  digest  plain-text summary for a session start: expiries, next actions by actor,
          blocked items. It validates first and reports itself unavailable on any
          status-affecting finding. --hook never fails: errors become one line, exit 0.
  table   print the Markdown table view.

Invariants (finding code; the proving tests are named in brackets):
  I1  R1  Shape: required keys only, types, status/actor/kind/role enums, id prefix =
          kind. Dates (`as_of`, `since`) are quoted YYYY-MM-DD strings and `expires`
          a quoted ISO datetime with an explicit zone; YAML-typed dates and
          timestamps are refused. `note` is one non-empty line [test_r1_*].
  I2  R1  Action coherence: `next` null <=> next_actor `none`; a terminal row has no
          `next` [test_r1_next_and_actor_agree_with_status].
  I3  R2  Identity: each id occurs once; ids and aliases unique (NFKC, casefold); the
          YAML has no repeated mapping key [test_r2_*, test_load_rejects_duplicate_mapping_keys].
  I4  R3  Graph: every `blocked_by` / `checkpoint` id exists; no self-reference or
          cycle [test_r3_*].
  I5  R4  Links: every link in LINK_FIELDS (row `owner`, row `evidence`) is
          repository-relative and names an existing file inside the checkout.
          Fragments are not parsed [test_r4_*].
  I6  R6  Revision: `as_of` is on or after every `since`; `reconciled_at` names a
          commit dated on or after every `since` whose tree holds every linked file
          (checked where git can read the commit; skipped in a shallow or non-git
          tree) [test_r6_*].
  I7  R7  No YAML value is cut by an unquoted ` #` [test_r7_*].
  I8  R8  Mirrors (role owner only): each fixed target holds exactly one block equal
          to `write`'s output; `write` keeps the file's line endings; every rendered
          row carries its note [test_r8_*, test_write_preserves_crlf, test_mirrors_carry_notes].
  I9  R9  Gate selection: the gates.yml `track-b-register` selector matches the
          register, this script, gates.yml, every linked file and (role owner) every
          mirror [test_r9_*].
  I10 --  Readiness and expiry (views): a row is offered as a next action only when it
          is open, has a next action, waits on nothing outside the register, and every
          `blocked_by` row is terminal and, given a clock, unexpired. Expiry applies
          whatever the status: a lapsed terminal row satisfies nothing and every
          expiring row is listed. `check` and the mirrors are clock-free; the digest
          applies the clock [test_waits_for_*, test_expiry_*, test_digest_*].

Coverage of new dated headings in owner documents is not checked here; it belongs
to the follow-up that makes the register the owner.
"""
from __future__ import annotations

import argparse
import datetime as dt
import posixpath
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # the SessionStart hook may run on a bare system Python
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTER = ROOT / "docs" / "governance" / "track_b_register.yml"
REGISTER_DIR = "docs/governance"

SCHEMA = "track_b_register/v1"
STATUSES = (
    "NOT_STARTED",
    "OPEN",
    "IN_PROGRESS",
    "AWAITING_OPERATOR",
    "BLOCKED",
    "ACCEPTED",
    "ACCEPTED_LIMITED",
    "CLOSED",
    "PARKED",
)
TERMINAL = frozenset({"ACCEPTED", "ACCEPTED_LIMITED", "CLOSED"})
ACTORS = ("operator", "coordinator", "worker", "none")
ROLES = ("pilot", "owner")
KINDS = ("packet", "slice", "gate", "work", "checkpoint", "drill", "defect", "t00", "adapter", "parked")
LINK_FIELDS = ("owner", "evidence")  # every field holding a document link (I5, I6, I9)
GENERATED_TARGETS = (  # fixed mirrors, active only under role owner (I8)
    ("STATE.md", "summary"),
    ("docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md", "table"),
)

ID_RE = re.compile(r"^[a-z0-9]+(?:\.[A-Za-z0-9][A-Za-z0-9+-]*)+$")
ALIAS_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ./+-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXPIRES_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?(?:Z|[+-]\d{2}:\d{2})$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")

ROW_KEYS = {"id", "kind", "title", "status", "since", "owner", "next", "next_actor"}
ROW_OPTIONAL = {"aliases", "blocked_by", "waits_for", "checkpoint", "expires", "evidence", "refs", "note"}
TOP_KEYS = {"schema", "role", "as_of", "reconciled_at", "items"}
BEGIN_RE = re.compile(r"^<!-- BEGIN generated: track-b-register \((summary|table)\) -->$", re.M)
END_MARK = "<!-- END generated: track-b-register -->"
WRITE_CMD = "`python -I scripts/fp.py python scripts/track_b_register.py write`"


# ---------------------------------------------------------------- loading

class Finding(Exception):
    pass


def _strict_loader():
    """A SafeLoader that refuses a repeated mapping key (safe_load keeps the last)."""

    class Strict(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        keys = set()
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in keys:
                raise yaml.constructor.ConstructorError(
                    None, None, f"duplicate key {key!r}", key_node.start_mark
                )
            keys.add(key)
        return loader.construct_mapping(node, deep=deep)

    Strict.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    return Strict


def load(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise Finding("R1 PyYAML is not installed for this interpreter")
    try:
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=_strict_loader())
    except (OSError, yaml.YAMLError) as exc:
        raise Finding(f"R1 {path.name}: unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise Finding(f"R1 {path.name}: top level must be a mapping")
    return data


def _date(value: Any) -> dt.date | None:
    """A quoted YYYY-MM-DD string only; YAML-typed dates and timestamps are refused (I1)."""
    if not (isinstance(value, str) and DATE_RE.match(value)):
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def _expiry(value: Any) -> dt.datetime | None:
    """A quoted ISO datetime with an explicit zone, as UTC; anything else is None (I1)."""
    if not (isinstance(value, str) and EXPIRES_RE.match(value)):
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except ValueError:
        return None


def _links(row: dict[str, Any]) -> list[str]:
    """Every document link of a row, from the one enumerated LINK_FIELDS list."""
    out: list[str] = []
    for field in LINK_FIELDS:
        val = row.get(field)
        vals = val if isinstance(val, list) else [val]
        out.extend(v for v in vals if isinstance(v, str))
    return out


def _link_path(link: str) -> str:
    """Repository-relative posix path of a register link (fragment dropped)."""
    return posixpath.normpath(posixpath.join(REGISTER_DIR, link.partition("#")[0]))


def _targets(data: dict[str, Any], targets: tuple = GENERATED_TARGETS) -> tuple:
    """The mirrors in force: none under pilot; under owner, the code-fixed list (I8)."""
    for rel, view in targets:
        norm = posixpath.normpath(rel)
        if view not in ("summary", "table") or norm.startswith(("..", "/")) or ":" in norm:
            raise Finding(f"R8 mirror target {rel!r} must be a repository-relative path with a known view")
    return targets if data.get("role") == "owner" else ()


# ---------------------------------------------------------------- check

QUOTED_RE = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\']|\'\')*\'')


def lint(text: str) -> list[str]:
    """R7: a value line whose unquoted part holds ` #` lost text to a comment."""
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if re.search(r"\s#", QUOTED_RE.sub('""', line)):
            out.append(f"R7 line {n}: inline comment after a value; quote text that holds '#'")
    return out


def _row_findings(row: dict[str, Any], where: str) -> list[str]:
    out = []
    for key in sorted(ROW_KEYS - row.keys()):
        out.append(f"R1 {where}: missing {key!r}")
    for key in sorted(row.keys() - ROW_KEYS - ROW_OPTIONAL):
        out.append(f"R1 {where}: unknown key {key!r}")
    if not (isinstance(row.get("id"), str) and ID_RE.match(row["id"])):
        out.append(f"R1 {where}: id must be <kind>.<name>, e.g. slice.S5")
    elif row["id"].split(".", 1)[0] != row.get("kind"):
        out.append(f"R1 {where}: id prefix must equal kind {row.get('kind')!r}")
    if row.get("kind") not in KINDS:
        out.append(f"R1 {where}: kind must be one of {', '.join(KINDS)}")
    if row.get("status") not in STATUSES:
        out.append(f"R1 {where}: status must be one of {', '.join(STATUSES)}")
    if row.get("next_actor") not in ACTORS:
        out.append(f"R1 {where}: next_actor must be one of {', '.join(ACTORS)}")
    if _date(row.get("since")) is None:
        out.append(f"R1 {where}: since must be a quoted YYYY-MM-DD string")
    for key in ("title", "owner"):
        if not (isinstance(row.get(key), str) and row[key].strip()):
            out.append(f"R1 {where}: {key} must be a non-empty string")
    nxt = row.get("next")
    if nxt is not None and not (isinstance(nxt, str) and nxt.strip()):
        out.append(f"R1 {where}: next must be text or null")
    if nxt is None and row.get("next_actor") != "none":
        out.append(f"R1 {where}: a row with no next action takes next_actor 'none'")
    if nxt is not None and row.get("next_actor") == "none":
        out.append(f"R1 {where}: a next action needs an actor")
    if row.get("status") in TERMINAL and nxt is not None:
        out.append(f"R1 {where}: a terminal row has no next action")
    for key in ("aliases", "blocked_by", "waits_for", "evidence", "refs"):
        val = row.get(key)
        if val is not None and not (isinstance(val, list) and all(isinstance(v, str) for v in val)):
            out.append(f"R1 {where}: {key} must be a list of strings")
    for alias in row.get("aliases") or []:
        if isinstance(alias, str) and not ALIAS_RE.match(alias):
            out.append(f"R1 {where}: alias {alias!r} has disallowed characters")
    if "expires" in row and _expiry(row["expires"]) is None:
        out.append(f"R1 {where}: expires must be a quoted ISO datetime with a zone, e.g. \"2026-10-09T01:52:19Z\"")
    note = row.get("note")
    if "note" in row and not (isinstance(note, str) and note.strip() and not re.search(r"[\r\n]", note)):
        out.append(f"R1 {where}: note must be one non-empty line")
    return out


def check(
    data: dict[str, Any], root: Path = ROOT, text: str | None = None, targets: tuple = GENERATED_TARGETS
) -> list[str]:
    out: list[str] = lint(text) if text is not None else []

    # R1 / R6 top level
    if data.get("schema") != SCHEMA:
        out.append(f"R1 schema must be {SCHEMA!r}")
    for key in sorted(TOP_KEYS - data.keys()):
        out.append(f"R1 missing top-level key {key!r}")
    for key in sorted(data.keys() - TOP_KEYS):
        out.append(f"R1 unknown top-level key {key!r}")
    if data.get("role") not in ROLES:
        out.append(f"R1 role must be one of {', '.join(ROLES)}")
    as_of = _date(data.get("as_of"))
    if as_of is None:
        out.append("R1 as_of must be a quoted YYYY-MM-DD string")
    if not (isinstance(data.get("reconciled_at"), str) and SHA_RE.match(data["reconciled_at"])):
        out.append("R1 reconciled_at must be a commit sha (7-40 hex)")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        out.append("R1 items must be a non-empty list")
        return out

    # R1 rows
    rows: list[dict[str, Any]] = []
    for i, row in enumerate(items):
        if not isinstance(row, dict):
            out.append(f"R1 items[{i}]: must be a mapping")
            continue
        out.extend(_row_findings(row, str(row.get("id", f"items[{i}]"))))
        rows.append(row)

    # R2 identity
    names: dict[str, str] = {}
    ids = {r["id"] for r in rows if isinstance(r.get("id"), str)}
    for rid, n in Counter(r.get("id") for r in rows if isinstance(r.get("id"), str)).items():
        if n > 1:
            out.append(f"R2 {rid}: id appears in {n} rows")
    for row in rows:
        rid = row.get("id")
        for name in [rid, *(row.get("aliases") or [])]:
            if not isinstance(name, str):
                continue
            key = unicodedata.normalize("NFKC", name).casefold()
            if key in names and names[key] != rid:
                out.append(f"R2 {rid}: name {name!r} already used by {names[key]}")
            elif key in names and name != rid:
                out.append(f"R2 {rid}: alias {name!r} repeats its own id")
            names.setdefault(key, rid)

    # R3 references and cycles
    graph: dict[str, list[str]] = {}
    for row in rows:
        rid = row.get("id")
        deps = [d for d in row.get("blocked_by") or [] if isinstance(d, str)]
        for dep in deps:
            if dep == rid:
                out.append(f"R3 {rid}: blocked_by names itself")
            elif dep not in ids:
                out.append(f"R3 {rid}: blocked_by {dep!r} is not a register id")
        cp = row.get("checkpoint")
        if cp is not None and (cp not in ids or not str(cp).startswith("checkpoint.")):
            out.append(f"R3 {rid}: checkpoint {cp!r} is not a checkpoint.* id")
        if isinstance(rid, str):
            graph[rid] = [d for d in deps if d in ids and d != rid]
    state: dict[str, int] = {}

    def visit(node: str, trail: list[str]) -> None:
        state[node] = 1
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                cycle = trail[trail.index(nxt):] + [nxt] if nxt in trail else [node, nxt]
                out.append(f"R3 blocked_by cycle: {' -> '.join(cycle)}")
            elif state.get(nxt) is None:
                visit(nxt, trail + [nxt])
        state[node] = 2

    for node in sorted(graph):
        if state.get(node) is None:
            visit(node, [node])

    # R4 links: repository-relative, inside the checkout, existing file
    top = root.resolve()
    for row in rows:
        for link in _links(row):
            where = f"R4 {row.get('id')}: {link!r}"
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link) or link.startswith("/"):
                out.append(f"{where} must be repository-relative")
                continue
            path = (root / REGISTER_DIR / link.partition("#")[0]).resolve()
            if not path.is_relative_to(top):
                out.append(f"{where} leaves the repository")
            elif not path.is_file():
                out.append(f"{where}: file not found")

    # R6 revision
    if as_of is not None:
        for row in rows:
            since = _date(row.get("since"))
            if since is not None and since > as_of:
                out.append(f"R6 {row.get('id')}: since {since} is after as_of {as_of}; advance as_of")
    out.extend(_revision_ok(data, rows, root))

    # R9 gate selection
    out.extend(_gate_selects(data, rows, root, targets))

    # R8 mirrors
    if not any(f.startswith("R1") for f in out):
        for rel, view in _targets(data, targets):
            out.extend(_check_block(data, rel, view, root))
    return out


def _git(root: Path, *args: str) -> str | None:
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8", timeout=30
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if done.returncode == 0 else None


def _revision_ok(data: dict[str, Any], rows: list[dict[str, Any]], root: Path) -> list[str]:
    """R6 (I6): reconciled_at is a commit no older than any status, holding every linked file."""
    sha = data.get("reconciled_at")
    if not (isinstance(sha, str) and SHA_RE.match(sha)):
        return []
    toplevel = (_git(root, "rev-parse", "--show-toplevel") or "").strip()
    if not toplevel or Path(toplevel).resolve() != root.resolve():
        return []  # not a git tree, or root is not its top (e.g. a temp dir inside one)
    if (_git(root, "rev-parse", "--is-shallow-repository") or "").strip() == "true":
        return []
    if _git(root, "cat-file", "-e", f"{sha}^{{commit}}") is None:
        return [f"R6 reconciled_at {sha} is not a commit in this repository"]
    out = []
    when = _date((_git(root, "show", "-s", "--format=%cs", sha) or "").strip())
    latest = max((d for d in (_date(r.get("since")) for r in rows) if d), default=None)
    if when and latest and when < latest:
        out.append(f"R6 reconciled_at {sha} ({when}) predates the newest status ({latest}); reconcile against a later commit")
    present: dict[str, bool] = {}
    for row in rows:
        for link in _links(row):
            rel = _link_path(link)
            if rel not in present:
                present[rel] = _git(root, "cat-file", "-e", f"{sha}:{rel}") is not None
            if not present[rel]:
                out.append(f"R6 {row.get('id')}: {rel} does not exist at reconciled_at {sha}")
    return out


def _gate_selects(data: dict[str, Any], rows: list[dict[str, Any]], root: Path, targets: tuple) -> list[str]:
    """R9 (I9): gates.yml's track-b-register staged_regex must match each dependency path."""
    gates = root / "scripts" / "gates.yml"
    if yaml is None or not gates.is_file():
        return []
    try:
        spec = next(g for g in yaml.safe_load(gates.read_text(encoding="utf-8"))["gates"]
                    if g.get("id") == "track-b-register")
        selector = re.compile(spec["when"]["staged_regex"])
    except (StopIteration, KeyError, TypeError, re.error, yaml.YAMLError):
        return ["R9 scripts/gates.yml: no track-b-register gate with a staged_regex"]
    paths = {_link_path(link) for row in rows for link in _links(row)}
    paths |= {rel for rel, _ in _targets(data, targets)}
    paths |= {"docs/governance/track_b_register.yml", "scripts/track_b_register.py", "scripts/gates.yml"}
    return [
        f"R9 scripts/gates.yml: track-b-register staged_regex does not select {p}"
        for p in sorted(p for p in paths if not p.startswith("..") and not selector.search(p))
    ]


def _split_block(text: str) -> tuple[str, str, str, str] | str:
    """(before, view, body, after) for the one block in text, or a reason."""
    begins = list(BEGIN_RE.finditer(text))
    ends = text.count(END_MARK)
    if len(begins) != 1 or ends != 1:
        return f"needs exactly one BEGIN/END track-b-register pair (found {len(begins)}/{ends})"
    b = begins[0]
    end = text.index(END_MARK)
    if end < b.end():
        return "END marker precedes BEGIN"
    return text[: b.end()], b.group(1), text[b.end():end], text[end:]


def _check_block(data: dict[str, Any], rel: str, view: str, root: Path) -> list[str]:
    try:
        text = (root / rel).read_text(encoding="utf-8")
    except OSError:
        return [f"R8 {rel}: file not found"]
    parts = _split_block(text)
    if isinstance(parts, str):
        return [f"R8 {rel}: {parts}"]
    _, found, body, _ = parts
    if found != view:
        return [f"R8 {rel}: block view is {found!r}, expected {view!r}"]
    if body != "\n" + render(data, view, rel) + "\n":
        return [f"R8 {rel}: generated block is stale; run {WRITE_CMD}"]
    return []


def write(data: dict[str, Any], root: Path = ROOT, targets: tuple = GENERATED_TARGETS) -> list[str]:
    """Regenerate each mirror's block in place (role owner only); returns the paths rewritten."""
    changed = []
    for rel, view in _targets(data, targets):
        path = root / rel
        raw = path.read_bytes().decode("utf-8")
        eol = "\r\n" if "\r\n" in raw else "\n"
        text = raw.replace("\r\n", "\n")
        parts = _split_block(text)
        if isinstance(parts, str):
            raise Finding(f"R8 {rel}: {parts}")
        before, _, _, after = parts
        before = BEGIN_RE.sub(f"<!-- BEGIN generated: track-b-register ({view}) -->", before)
        new = before + "\n" + render(data, view, rel) + "\n" + after
        if new != text:
            path.write_bytes(new.replace("\n", eol).encode("utf-8"))
            changed.append(rel)
    return changed


# ---------------------------------------------------------------- views

def _open(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r.get("status") not in TERMINAL and r.get("status") != "PARKED"]


def _expiring(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every non-parked row carrying an expiry, terminal or not (I10)."""
    return [r for r in rows if _expiry(r.get("expires")) and r.get("status") != "PARKED"]


def _groups(
    rows: list[dict[str, Any]], now: dt.datetime | None = None
) -> tuple[dict[str, list], list]:
    """Unblocked next actions by actor, and blocked rows with what they wait on (I10).

    `waits_for` blocks like `blocked_by`. With `now`, expiry applies whatever the
    status: a lapsed row is not offered, and a lapsed terminal row satisfies nothing.
    """
    dupes = sorted(rid for rid, n in Counter(r["id"] for r in rows).items() if n > 1)
    if dupes:
        raise Finding(f"R2 duplicate row ids: {', '.join(dupes)}")
    by_id = {r["id"]: r for r in rows}

    def lapsed(r):
        exp = _expiry(r.get("expires"))
        return now is not None and exp is not None and exp <= now

    def waiting(r):
        deps = []
        for d in r.get("blocked_by") or []:
            dep = by_id.get(d, {})
            if dep.get("status") not in TERMINAL:
                deps.append(d)
            elif lapsed(dep):
                deps.append(f"{d} (expired)")
        return deps + list(r.get("waits_for") or [])

    nexts = {
        actor: [
            r for r in _open(rows)
            if r.get("next_actor") == actor and r.get("next") and not waiting(r) and not lapsed(r)
        ]
        for actor in ("operator", "coordinator", "worker")
    }
    blocked = [(r, waiting(r)) for r in _open(rows) if waiting(r)]
    return nexts, blocked


def _relink(link: str, target_rel: str) -> str:
    """A register link (relative to docs/governance) re-expressed from target_rel."""
    path_part, hash_, frag = link.partition("#")
    absolute = posixpath.normpath(posixpath.join(REGISTER_DIR, path_part))
    rel = posixpath.relpath(absolute, posixpath.dirname(target_rel) or ".")
    return rel + (hash_ + frag if hash_ else "")


def _note_md(r: dict[str, Any]) -> str:
    return f" _(Note: {r['note']})_" if r.get("note") else ""


def render(data: dict[str, Any], view: str, target_rel: str) -> str:
    register = _relink("track_b_register.yml", target_rel)
    governs = "the register owns item status" if data.get("role") == "owner" else "pilot view; the linked owners govern"
    head = (
        f"_Generated from the [Track B register]({register}) (as of {data['as_of']} @ "
        f"`{data['reconciled_at']}`); {governs}. Edit it, then run {WRITE_CMD}._"
    )
    if view == "table":
        return head + "\n\n" + table(data, target_rel)
    nexts, blocked = _groups(data["items"])
    lines = [head, ""]
    for r in sorted(_expiring(data["items"]), key=lambda r: _expiry(r["expires"])):
        lines.append(
            f"- **Expires {_expiry(r['expires']):%Y-%m-%dT%H:%MZ}:** `{r['id']}` ({r['status']}) — "
            f"{r['title']}{_note_md(r)}"
        )
    for actor, label in (("operator", "Operator"), ("coordinator", "Coordinator"), ("worker", "Worker")):
        if nexts[actor]:
            lines.append(f"- **Next — {label}:**")
            lines.extend(f"  - `{r['id']}` — {r['next']}{_note_md(r)}" for r in nexts[actor])
    if blocked:
        lines.append("- **Blocked:**")
        lines.extend(f"  - `{r['id']}` ← {', '.join(w)}{_note_md(r)}" for r, w in blocked)
    return "\n".join(lines)


def digest(data: dict[str, Any], today: dt.datetime, days: int) -> str:
    rows = data["items"]
    lines = [f"Track B register (role {data.get('role')}) as_of {data['as_of']} @ {data['reconciled_at']}"]
    horizon = today + dt.timedelta(days=days)
    expiring = []
    for r in _expiring(rows):
        exp = _expiry(r["expires"])
        if exp <= today:
            expiring.append(f"  EXPIRED {exp:%Y-%m-%dT%H:%MZ} {r['id']}: {r['title']}")
        elif exp <= horizon:
            hours = int((exp - today).total_seconds() // 3600)
            expiring.append(f"  {exp:%Y-%m-%dT%H:%MZ} (~{hours}h) {r['id']}: {r['title']}")
    if expiring:
        lines.append(f"Expiring within {days}d:")
        lines.extend(expiring)

    def noted(line, r):
        return [line] + ([f"    note: {r['note']}"] if r.get("note") else [])

    nexts, blocked = _groups(rows, today)
    for actor in ("operator", "coordinator", "worker"):
        if nexts[actor]:
            lines.append(f"Next ({actor}):")
            for r in nexts[actor]:
                lines.extend(noted(f"  {r['id']}: {r['next']}", r))
    if blocked:
        lines.append("Blocked:")
        for r, w in blocked:
            lines.extend(noted(f"  {r['id']} <- {', '.join(w)}", r))
    lines.append(f"Register: docs/governance/track_b_register.yml ({len(rows)} rows)")
    return "\n".join(lines)


def table(data: dict[str, Any], target_rel: str = "docs/governance/x") -> str:
    def cell(text: Any) -> str:
        return str(text or "—").replace("|", "\\|").replace("\n", " ")

    lines = [
        "| Item | Status | Next | Actor | Blocked by | Expires | Note | Owner |",
        "|---|---|---|---|---|---|---|---|",
    ]
    shown = _open(data["items"]) + [r for r in _expiring(data["items"]) if r.get("status") in TERMINAL]
    for r in shown:
        name = r["id"] + (f" ({', '.join(r['aliases'])})" if r.get("aliases") else "")
        exp = _expiry(r.get("expires"))
        waits = ", ".join([*(r.get("blocked_by") or []), *(r.get("waits_for") or [])])
        lines.append(
            f"| {cell(name)} | {r['status']} | {cell(r.get('next'))} | {r['next_actor']} | "
            f"{cell(waits)} | {cell(exp and f'{exp:%Y-%m-%dT%H:%MZ}')} | {cell(r.get('note'))} | "
            f"[owner]({_relink(r['owner'], target_rel)}) |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------- cli

def _status_affecting(findings: list[str]) -> list[str]:
    """Findings that can make the digest's status wrong (stale mirrors and the gate selector cannot)."""
    return [f for f in findings if not f.startswith(("R8", "R9"))]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "command", nargs="?", default="check", choices=("check", "write", "digest", "table")
    )
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument(
        "--hook", action="store_true", help="digest only: report any failure as one line, exit 0"
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):  # a cp1252 console must not kill the digest on "C′"
        sys.stdout.reconfigure(errors="replace")
    if args.hook:
        if args.command != "digest":
            parser.error("--hook applies to digest only")
        try:
            data = load(args.register)
            text = args.register.read_text(encoding="utf-8")
            bad = _status_affecting(check(data, text=text))
            if bad:
                print(f"track-b register digest unavailable: {len(bad)} finding(s), first: {bad[0]}"[:300])
            else:
                print(digest(data, dt.datetime.now(dt.timezone.utc), args.days))
        except Exception as exc:  # a session must start whatever the register's state
            print(f"track-b register digest unavailable: {type(exc).__name__}: {exc}"[:300])
        return 0
    try:
        data = load(args.register)
    except Finding as exc:
        print(exc)
        return 1
    text = args.register.read_text(encoding="utf-8")
    findings = check(data, text=text)
    if args.command == "check":
        for f in findings:
            print(f)
        if findings:
            print(f"track_b_register: {len(findings)} finding(s)")
            return 1
        print(f"track_b_register: OK ({len(data['items'])} rows)")
        return 0
    blocking = [f for f in findings if not f.startswith("R8")]
    if args.command == "write" and blocking:
        for f in blocking:
            print(f)
        print("track_b_register: fix the findings above before writing")
        return 1
    if args.command == "digest" and _status_affecting(findings):
        for f in _status_affecting(findings):
            print(f)
        print("track_b_register: digest unavailable until the findings above are fixed")
        return 1
    if any(f.startswith(("R1", "R2", "R7")) for f in findings):
        print("track_b_register: register is malformed; run `check`")
        return 1
    if args.command == "write":
        try:
            changed = write(data)
        except Finding as exc:
            print(exc)
            return 1
        print("track_b_register: wrote " + (", ".join(changed) if changed else "nothing (up to date)"))
    elif args.command == "digest":
        print(digest(data, dt.datetime.now(dt.timezone.utc), args.days))
    else:
        print(table(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
