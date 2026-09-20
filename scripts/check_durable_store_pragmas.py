#!/usr/bin/env python3
"""check_durable_store_pragmas.py — durability invariant for operational SQLite stores.

The rail's durable state lives in per-service SQLite databases on each Fly
machine's own volume (`deploy/c1_rail/fly.toml`, `deploy/c1_signal_daemon/fly.toml`
— single machine, single writer, local volume). Every one of those stores already
opens its write path with `PRAGMA synchronous=FULL` and serializes it with
`BEGIN IMMEDIATE`. Nothing enforced that, so a new store — or a new connection in
an existing one — could silently ship with SQLite's default `synchronous=NORMAL`
and a deferred transaction. On the risk path that is a durability downgrade that
no test would notice: the store still works, it just stops surviving a power loss
the same way.

This scanner pins the invariant that holds today. It changes no runtime behavior.

Contract
--------
1. Every module under `ops/` containing a `sqlite3.connect(...)` call site must be
   registered below — either in ``DURABLE_STORES`` (subject to the pragma rules)
   or in ``EXCLUDED`` with a reason. An unregistered connect site is an error, so
   a new store fails closed until someone classifies it.
2. In a durable store, every connect site must either
   - execute `PRAGMA synchronous=FULL` in the same function, or
   - be statically non-writing: a `:memory:` literal, or a URI carrying `mode=ro`.
3. Every durable store must issue `BEGIN IMMEDIATE` somewhere in the module.
   This is module-scoped, not function-scoped, on purpose: `execution/store.py`
   connects in `_connect` and begins in `transaction`, which is legitimate.

What this does NOT check
------------------------
`journal_mode`. `qualification/execution/store.py` creates its journal with WAL;
every other store runs SQLite's default rollback journal. That inconsistency is
real but unadjudicated — changing either one alters recovery and backup semantics
for a live store, which is not a scanner's call to make. The scanner pins what is
already uniform and stays silent on what is not.

`foreign_keys=ON` is likewise not required: the book schema declares no
`REFERENCES` constraints (`book_migration_schema.SOURCE_MANIFESTS`), so the pragma
is a no-op wherever it appears today. Requiring it would be cargo cult.
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Durable operational stores: authoritative state on a service's own volume.
DURABLE_STORES: tuple[str, ...] = (
    "ops/c1_rail/book_account_owner.py",
    "ops/c1_rail/book_halt.py",
    "ops/c1_rail/book_migration.py",
    "ops/c1_rail/book_settlement.py",
    "ops/c1_rail/qualification/attempt.py",
    "ops/c1_rail/qualification/execution/store.py",
)

# Connect sites that are deliberately not durable operational state.
EXCLUDED: dict[str, str] = {
    "ops/recall/index.py":
        "derived recall index; rebuildable from the corpus, not authoritative state",
}


def _normalized(text: str) -> str:
    """Collapse whitespace and case so pragma spelling variants compare equal."""
    return "".join(text.split()).upper()


def _string_constants(node: ast.AST) -> list[str]:
    return [n.value for n in ast.walk(node)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _executed_sql(node: ast.AST) -> str:
    """Normalized text of every string handed to an `.execute*` call.

    Scoped to executed statements on purpose: a docstring or comment that merely
    mentions `BEGIN IMMEDIATE` must not satisfy the contract.
    """
    statements: list[str] = []
    for call in ast.walk(node):
        if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                and call.func.attr.startswith("execute")):
            for argument in call.args:
                statements.extend(_string_constants(argument))
    return _normalized(" ".join(statements))


def _non_writing(call: ast.Call) -> bool:
    """True when the connection target is statically in-memory or read-only."""
    if not call.args:
        return False
    literals = _string_constants(call.args[0])
    return any(value == ":memory:" or "mode=ro" in value for value in literals)


def _enclosing_functions(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    parents: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    return parents


def _owner(node: ast.AST, parents: dict[ast.AST, ast.AST]):
    current = parents.get(node)
    while current is not None and not isinstance(
            current, (ast.FunctionDef, ast.AsyncFunctionDef)):
        current = parents.get(current)
    return current


def _connect_calls(tree: ast.AST) -> list[ast.Call]:
    return [node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "connect"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "sqlite3"]


def scan_source(relative: str, source: str) -> list[str]:
    """Apply the pragma contract to one durable store's source text."""
    tree = ast.parse(source)
    parents = _enclosing_functions(tree)
    findings: list[str] = []

    if "BEGINIMMEDIATE" not in _executed_sql(tree):
        findings.append(f"{relative}: durable store never issues BEGIN IMMEDIATE")

    for call in _connect_calls(tree):
        if _non_writing(call):
            continue
        function = _owner(call, parents)
        if function is None:
            findings.append(
                f"{relative}:{call.lineno}: module-level sqlite3.connect cannot be "
                "verified; move it into a function that sets PRAGMA synchronous=FULL")
            continue
        if "PRAGMASYNCHRONOUS=FULL" not in _executed_sql(function):
            findings.append(
                f"{relative}:{call.lineno}: writable sqlite3.connect in "
                f"{function.name}() without PRAGMA synchronous=FULL "
                "(add the pragma, or open the connection with mode=ro)")
    return findings


def _scan_store(relative: str) -> list[str]:
    path = REPO / relative
    if not path.exists():
        return [f"{relative}: registered durable store is missing; "
                f"update DURABLE_STORES in {Path(__file__).name}"]
    return scan_source(relative, path.read_text(encoding="utf-8"))


def _scan_registry() -> list[str]:
    """Every connect site under ops/ must be classified."""
    known = set(DURABLE_STORES) | set(EXCLUDED)
    findings: list[str] = []
    for path in sorted((REPO / "ops").rglob("*.py")):
        relative = path.relative_to(REPO).as_posix()
        if relative in known:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError) as exc:
            findings.append(f"{relative}: unreadable ({exc})")
            continue
        if _connect_calls(tree):
            findings.append(
                f"{relative}: unregistered sqlite3.connect call site; add it to "
                f"DURABLE_STORES or EXCLUDED in {Path(__file__).name}")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args(argv)

    findings = _scan_registry()
    for relative in DURABLE_STORES:
        findings.extend(_scan_store(relative))

    if findings:
        print("durable-store pragma invariant violated:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1
    print(f"durable-store pragmas OK ({len(DURABLE_STORES)} stores, "
          f"{len(EXCLUDED)} excluded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
