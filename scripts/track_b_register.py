#!/usr/bin/env python3
"""track_b_register.py — Track B status register: check, write, digest, table.

The register (`docs/governance/track_b_register.yml`) holds one row per Track B
item: a gate, packet, slice, checkpoint, drill or defect. Each row gives the
item's status now, the next permitted action and who takes it. It cites the dated
ruling or acceptance that set that status. The ledgers keep the reasoning and
evidence; a row only routes to them. Under Rule 7 the register is the canonical
owner of each item's current status, next action, actor, blockers and expiry
(`role: owner`, operator ruling 2026-10-03); the rulings' text, reasoning and
evidence stay with the record each row cites. The row is written by whoever
records the ruling or acceptance, in the same change.

Subcommands:
  check   (default) exit 0 when the register is well formed and in step with its
          watched owner documents; exit 1 with one line per finding otherwise.
  write   regenerate every block listed under `generated` in place, between
          `<!-- BEGIN generated: track-b-register ... -->` and its END marker.
  digest  a short plain-text summary for a session start: next actions by actor,
          blocked items and approvals expiring within --days (default 7). With
          --hook it never fails: any error becomes one line and exit 0.
  table   print the Markdown table view of the open rows.

`check` is content-deterministic: it never compares against the clock, so the
required CI status cannot turn red on a date alone. Expiry appears only in
`digest`. Its findings:
  R1  schema: required keys, types, status enum, id/alias shape.
  R2  identity: ids and aliases unique across the register; no alias equals an id.
  R3  references: every `blocked_by` / `checkpoint` id exists; no self-reference;
      no cycle in `blocked_by`.
  R4  links: every `owner` / `evidence` link resolves to a tracked file and, when it
      carries a fragment, to a heading anchor in that file (GitHub slug rules).
  R5  coverage: every heading dated on or after `covers_from` in a `watch` file is
      cited by some row's `owner` or `evidence`, or listed under `noted`. A new
      ruling or acceptance therefore lands with its register row in the same change.
  R6  `reconciled_at` and `as_of` are present and well formed.
  R7  no inline comment after a value: YAML reads an unquoted ` #` as the start of a
      comment and silently cuts the value there (quote any text holding `#`).
  R8  every `generated` block exists exactly once in its file and equals what
      `write` would produce (run `write` after editing the register).

Owner of the rule: docs/operational_rules.md Rule 7 owner table.
"""
from __future__ import annotations

import argparse
import posixpath
import datetime as dt
import re
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
KINDS = ("packet", "slice", "gate", "work", "checkpoint", "drill", "defect", "t00", "adapter", "parked")

ID_RE = re.compile(r"^[a-z0-9]+(?:\.[A-Za-z0-9][A-Za-z0-9+-]*)+$")
ALIAS_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ./+-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})")
DATED_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
HTML_ANCHOR_RE = re.compile(r"""<a\s+(?:id|name)=["']([^"']+)["']""")

ROW_KEYS = {"id", "kind", "title", "status", "since", "owner", "next", "next_actor"}
ROW_OPTIONAL = {"aliases", "blocked_by", "waits_for", "checkpoint", "expires", "evidence", "refs", "note"}
TOP_KEYS = {"schema", "role", "as_of", "reconciled_at", "covers_from", "watch", "items"}
TOP_OPTIONAL = {"noted", "generated"}
VIEWS = ("summary", "table")
BEGIN_RE = re.compile(r"^<!-- BEGIN generated: track-b-register \((summary|table)\) -->$", re.M)
END_MARK = "<!-- END generated: track-b-register -->"


# ---------------------------------------------------------------- anchors

def slugify(heading: str) -> str:
    """GitHub's heading anchor for `heading` (before duplicate suffixes)."""
    text = MD_LINK_RE.sub(lambda m: m.group(1), heading)
    text = text.replace("`", "").replace("*", "")
    text = text.strip().lower()
    out = []
    for ch in text:
        cat = unicodedata.category(ch)
        if ch in (" ", "-") or cat[0] in ("L", "M", "N") or cat == "Pc":
            out.append("-" if ch == " " else ch)
    return "".join(out)


def headings(text: str) -> list[tuple[int, str]]:
    """(line number, heading text) for every ATX heading outside a code fence."""
    found: list[tuple[int, str]] = []
    fence: str | None = None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker[0] * len(marker)
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        h = HEADING_RE.match(line)
        if h:
            found.append((n, h.group(2)))
    return found


def anchors(text: str) -> dict[str, int]:
    """anchor -> line, with GitHub's -1, -2 suffixes for repeated slugs."""
    seen: dict[str, int] = {}
    result: dict[str, int] = {}
    for n, title in headings(text):
        base = slugify(title)
        count = seen.get(base, 0)
        seen[base] = count + 1
        result[base if count == 0 else f"{base}-{count}"] = n
    for n, line in enumerate(text.splitlines(), 1):
        for m in HTML_ANCHOR_RE.finditer(line):
            result.setdefault(m.group(1), n)
    return result


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
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and DATE_RE.match(value):
        return dt.date.fromisoformat(value)
    return None


def _expiry(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        return value.astimezone(dt.timezone.utc) if value.tzinfo else None
    if isinstance(value, str):
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed.astimezone(dt.timezone.utc) if parsed.tzinfo else None
    return None


def _links(row: dict[str, Any]) -> list[str]:
    links = [row["owner"]] if isinstance(row.get("owner"), str) else []
    evidence = row.get("evidence") or []
    if isinstance(evidence, list):
        links.extend(e for e in evidence if isinstance(e, str))
    return links


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


def check(
    data: dict[str, Any], root: Path = ROOT, text: str | None = None, production: bool = False
) -> list[str]:
    out: list[str] = lint(text) if text is not None else []

    # R1/R6 top level
    if data.get("schema") != SCHEMA:
        out.append(f"R1 schema must be {SCHEMA!r}")
    for key in sorted(TOP_KEYS - data.keys()):
        out.append(f"R1 missing top-level key {key!r}")
    for key in sorted(data.keys() - TOP_KEYS - TOP_OPTIONAL):
        out.append(f"R1 unknown top-level key {key!r}")
    if data.get("role") != "owner":
        out.append("R1 role must be 'owner' (Rule 7 owner of Track B item status)")
    as_of = _date(data.get("as_of"))
    if as_of is None:
        out.append("R6 as_of must be YYYY-MM-DD")
    if not (isinstance(data.get("reconciled_at"), str) and SHA_RE.match(data["reconciled_at"])):
        out.append("R6 reconciled_at must be a commit sha (7-40 hex)")
    covers_from = _date(data.get("covers_from"))
    if covers_from is None:
        out.append("R1 covers_from must be YYYY-MM-DD")
    watch = data.get("watch")
    if not (isinstance(watch, list) and all(isinstance(w, str) for w in watch)):
        out.append("R1 watch must be a list of repository paths")
        watch = []
    out.extend(_targets_ok(data))
    if production and not data.get("generated"):
        out.append("R1 the production register needs a non-empty generated list")
    if production and not watch:
        out.append("R1 the production register needs a non-empty watch list")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        out.append("R1 items must be a non-empty list")
        return out

    # R1 rows
    rows: list[dict[str, Any]] = []
    for i, row in enumerate(items):
        where = f"items[{i}]"
        if not isinstance(row, dict):
            out.append(f"R1 {where}: must be a mapping")
            continue
        where = f"{row.get('id', where)}"
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
            out.append(f"R1 {where}: since must be YYYY-MM-DD")
        for key in ("title", "owner"):
            if not (isinstance(row.get(key), str) and row[key].strip()):
                out.append(f"R1 {where}: {key} must be a non-empty string")
        nxt = row.get("next")
        if nxt is not None and not (isinstance(nxt, str) and nxt.strip()):
            out.append(f"R1 {where}: next must be text or null")
        if nxt is None and row.get("next_actor") != "none":
            out.append(f"R1 {where}: a row with no next action takes next_actor 'none'")
        if row.get("status") in TERMINAL and nxt is not None:
            out.append(f"R1 {where}: a terminal row has no next action")
        if nxt is not None and row.get("next_actor") == "none":
            out.append(f"R1 {where}: a next action needs an actor")
        for key in ("aliases", "blocked_by", "waits_for", "evidence", "refs"):
            val = row.get(key)
            if val is not None and not (isinstance(val, list) and all(isinstance(v, str) for v in val)):
                out.append(f"R1 {where}: {key} must be a list of strings")
        for alias in row.get("aliases") or []:
            if isinstance(alias, str) and not ALIAS_RE.match(alias):
                out.append(f"R1 {where}: alias {alias!r} has disallowed characters")
        if "expires" in row and _expiry(row["expires"]) is None:
            out.append(f"R1 {where}: expires must be an ISO datetime with a zone, e.g. 2026-10-09T01:52:19Z")
        rows.append(row)

    # R6 as_of covers every row's status date
    if as_of is not None:
        for row in rows:
            since = _date(row.get("since"))
            if since is not None and since > as_of:
                out.append(f"R6 {row.get('id')}: since {since} is after as_of {as_of}; advance as_of")

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

    # R4 links
    register_dir = root / "docs" / "governance"
    cache: dict[Path, dict[str, int] | None] = {}

    def resolve(link: str) -> tuple[Path, str]:
        path_part, _, frag = link.partition("#")
        return (register_dir / path_part).resolve(), frag

    def anchor_map(path: Path) -> dict[str, int] | None:
        if path not in cache:
            try:
                cache[path] = anchors(path.read_text(encoding="utf-8"))
            except OSError:
                cache[path] = None
        return cache[path]

    cited: set[tuple[Path, str]] = set()
    noted = data.get("noted") or []
    if not (isinstance(noted, list) and all(isinstance(n, dict) for n in noted)):
        out.append("R1 noted must be a list of {link, reason} mappings")
        noted = []
    link_owners = [(row.get("id"), link) for row in rows for link in _links(row)]
    for n in noted:
        if not (isinstance(n.get("link"), str) and isinstance(n.get("reason"), str) and n["reason"].strip()):
            out.append("R1 noted entries need a link and a non-empty reason")
            continue
        link_owners.append(("noted", n["link"]))
    for rid, link in link_owners:
        if re.match(r"^[a-z]+:", link):
            out.append(f"R4 {rid}: owner/evidence links must be repository-relative, not {link!r}")
            continue
        path, frag = resolve(link)
        try:
            path.relative_to(root.resolve())
        except ValueError:
            out.append(f"R4 {rid}: {link!r} leaves the repository")
            continue
        amap = anchor_map(path)
        if amap is None:
            out.append(f"R4 {rid}: {link!r}: file not found")
            continue
        if frag and frag not in amap:
            out.append(f"R4 {rid}: {link!r}: no heading with that anchor")
            continue
        cited.add((path, frag))

    # R5 coverage of dated headings in watched owners
    if covers_from is not None:
        for rel in watch:
            path = (root / rel).resolve()
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                out.append(f"R5 watch {rel!r}: file not found")
                continue
            seen: dict[str, int] = {}
            for n, title in headings(text):
                base = slugify(title)
                count = seen.get(base, 0)
                seen[base] = count + 1
                anchor = base if count == 0 else f"{base}-{count}"
                dates = []
                for m in DATED_RE.finditer(title):
                    try:
                        dates.append(dt.date.fromisoformat(m.group(1)))
                    except ValueError:
                        pass
                if not any(when >= covers_from for when in dates):
                    continue
                if (path, anchor) not in cited:
                    out.append(
                        f"R5 {rel}:{n}: dated heading not cited by any row or noted entry: "
                        f"#{anchor}"
                    )

    # R9 the track-b-register gate selects every file the register depends on
    out.extend(_gate_selects(data, rows, root))

    # R8 generated blocks
    if not any(f.startswith("R1") for f in out):
        for target in data.get("generated") or []:
            out.extend(_check_block(data, target, root))
    return out


def _gate_selects(data: dict[str, Any], rows: list[dict[str, Any]], root: Path) -> list[str]:
    """R9: gates.yml's track-b-register staged_regex must match each dependency path."""
    gates = root / "scripts" / "gates.yml"
    if yaml is None or not gates.is_file():
        return []
    try:
        spec = next(g for g in yaml.safe_load(gates.read_text(encoding="utf-8"))["gates"]
                    if g.get("id") == "track-b-register")
        selector = re.compile(spec["when"]["staged_regex"])
    except (StopIteration, KeyError, TypeError, re.error, yaml.YAMLError):
        return ["R9 scripts/gates.yml: no track-b-register gate with a staged_regex"]
    links = [link for row in rows for link in _links(row)]
    links += [n["link"] for n in data.get("noted") or [] if isinstance(n, dict) and isinstance(n.get("link"), str)]
    paths = {posixpath.normpath(posixpath.join("docs/governance", l.partition("#")[0])) for l in links}
    paths |= set(data.get("watch") or []) | {t.get("path") for t in data.get("generated") or [] if isinstance(t, dict)}
    paths |= {"docs/governance/track_b_register.yml", "scripts/track_b_register.py", "scripts/gates.yml"}
    return [
        f"R9 scripts/gates.yml: track-b-register staged_regex does not select {p}"
        for p in sorted(p for p in paths if isinstance(p, str) and not p.startswith("..") and not selector.search(p))
    ]


def _targets_ok(data: dict[str, Any]) -> list[str]:
    gen = data.get("generated")
    if gen is None:
        return []
    if not isinstance(gen, list):
        return ["R1 generated must be a list of {path, view} mappings"]
    out = []
    for g in gen:
        if not (isinstance(g, dict) and isinstance(g.get("path"), str) and g.get("view") in VIEWS):
            out.append(f"R1 generated entry {g!r} needs a path and a view in {VIEWS}")
    return out


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


def _check_block(data: dict[str, Any], target: dict[str, Any], root: Path) -> list[str]:
    rel = target["path"]
    try:
        text = (root / rel).read_text(encoding="utf-8")
    except OSError:
        return [f"R8 {rel}: file not found"]
    parts = _split_block(text)
    if isinstance(parts, str):
        return [f"R8 {rel}: {parts}"]
    _, view, body, _ = parts
    if view != target["view"]:
        return [f"R8 {rel}: block view is {view!r}, register says {target['view']!r}"]
    if body != "\n" + render(data, view, rel) + "\n":
        return [f"R8 {rel}: generated block is stale; run `python -I scripts/fp.py python scripts/track_b_register.py write`"]
    return []


def write(data: dict[str, Any], root: Path = ROOT) -> list[str]:
    """Regenerate each target's block in place; returns the paths rewritten."""
    changed = []
    for target in data.get("generated") or []:
        path = root / target["path"]
        raw = path.read_bytes().decode("utf-8")
        eol = "\r\n" if "\r\n" in raw else "\n"
        text = raw.replace("\r\n", "\n")
        parts = _split_block(text)
        if isinstance(parts, str):
            raise Finding(f"R8 {target['path']}: {parts}")
        before, _, _, after = parts
        before = BEGIN_RE.sub(
            f"<!-- BEGIN generated: track-b-register ({target['view']}) -->", before
        )
        new = before + "\n" + render(data, target["view"], target["path"]) + "\n" + after
        if new != text:
            path.write_bytes(new.replace("\n", eol).encode("utf-8"))
            changed.append(target["path"])
    return changed


# ---------------------------------------------------------------- views

def _open(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [r for r in rows if r.get("status") not in TERMINAL and r.get("status") != "PARKED"]


def _groups(
    rows: list[dict[str, Any]], now: dt.datetime | None = None
) -> tuple[dict[str, list], list]:
    """Unblocked next actions by actor, and blocked rows with what they wait on.

    `waits_for` (prerequisites outside the register) blocks like `blocked_by`. With
    `now`, a row whose `expires` has passed is not offered as a next action.
    """
    dupes = sorted(rid for rid, n in Counter(r["id"] for r in rows).items() if n > 1)
    if dupes:
        raise Finding(f"R2 duplicate row ids: {', '.join(dupes)}")
    by_id = {r["id"]: r for r in rows}

    def waiting(r):
        deps = [d for d in r.get("blocked_by") or [] if by_id.get(d, {}).get("status") not in TERMINAL]
        return deps + list(r.get("waits_for") or [])

    def lapsed(r):
        exp = _expiry(r.get("expires"))
        return now is not None and exp is not None and exp <= now

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
    absolute = posixpath.normpath(posixpath.join("docs/governance", path_part))
    rel = posixpath.relpath(absolute, posixpath.dirname(target_rel) or ".")
    return rel + (hash_ + frag if hash_ else "")


def render(data: dict[str, Any], view: str, target_rel: str) -> str:
    register = _relink("track_b_register.yml", target_rel)
    head = (
        f"_Generated from the [Track B register]({register}) (as of {data['as_of']} @ "
        f"`{data['reconciled_at']}`); the register owns item status. Edit it, then run "
        f"`python -I scripts/fp.py python scripts/track_b_register.py write`._"
    )
    if view == "table":
        return head + "\n\n" + table(data, target_rel)
    nexts, blocked = _groups(data["items"])
    lines = [head, ""]
    expiring = sorted(
        (r for r in _open(data["items"]) if _expiry(r.get("expires"))),
        key=lambda r: _expiry(r["expires"]),
    )
    for r in expiring:
        lines.append(
            f"- **Expires {_expiry(r['expires']):%Y-%m-%dT%H:%MZ}:** `{r['id']}` — {r['title']}"
        )
    for actor, label in (("operator", "Operator"), ("coordinator", "Coordinator"), ("worker", "Worker")):
        if nexts[actor]:
            lines.append(f"- **Next — {label}:**")
            lines.extend(
                f"  - `{r['id']}` — {r['next']}"
                for r in nexts[actor]
            )
    if blocked:
        lines.append("- **Blocked:** " + "; ".join(f"`{r['id']}` ← {', '.join(w)}" for r, w in blocked))
    return "\n".join(lines)


def digest(data: dict[str, Any], today: dt.datetime, days: int) -> str:
    rows = data["items"]
    lines = [
        f"Track B register (owner of item status) as_of {data['as_of']} "
        f"@ {data['reconciled_at']}"
    ]
    horizon = today + dt.timedelta(days=days)
    expiring = []
    for r in rows:
        exp = _expiry(r.get("expires"))
        if exp is None or r.get("status") in TERMINAL:
            continue
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

    lines = ["| Item | Status | Next | Actor | Blocked by | Owner |", "|---|---|---|---|---|---|"]
    for r in _open(data["items"]):
        name = r["id"] + (f" ({', '.join(r['aliases'])})" if r.get("aliases") else "")
        lines.append(
            f"| {cell(name)} | {r['status']} | {cell(r.get('next'))} | {r['next_actor']} | "
            f"{cell(', '.join([*(r.get('blocked_by') or []), *(r.get('waits_for') or [])]))} | [owner]({_relink(r['owner'], target_rel)}) |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------- cli

def _status_affecting(findings: list[str]) -> list[str]:
    """Findings that can make the digest's status wrong (stale views and the gate selector cannot)."""
    return [f for f in findings if not f.startswith(("R8", "R9"))]


def _is_production(register: Path) -> bool:
    return register.resolve() == DEFAULT_REGISTER.resolve()


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
    if args.hook:
        if args.command != "digest":
            parser.error("--hook applies to digest only")
        try:
            data = load(args.register)
            text = args.register.read_text(encoding="utf-8")
            bad = _status_affecting(check(data, text=text, production=_is_production(args.register)))
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
    findings = check(data, text=text, production=_is_production(args.register))
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
