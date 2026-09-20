"""Durable-store pragma scanner — the invariant holds, and the gate can fail.

A scanner that cannot fail is not a gate (scripts/gates.yml preamble). These
tests pin both directions: the six registered stores comply today, and each
way of breaking the contract is actually caught.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_durable_store_pragmas.py"
_SPEC = importlib.util.spec_from_file_location("check_durable_store_pragmas", SCRIPT)
mod = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = mod
_SPEC.loader.exec_module(mod)


COMPLIANT = '''
import sqlite3

class Store:
    def _transaction(self):
        db = sqlite3.connect(self.uri, uri=True, timeout=5, isolation_level=None)
        db.execute("PRAGMA synchronous=FULL")
        db.execute("BEGIN IMMEDIATE")
        return db
'''


def test_registered_stores_comply_today():
    """The six durable stores already satisfy the contract; this pins it."""
    findings = []
    for relative in mod.DURABLE_STORES:
        findings.extend(mod._scan_store(relative))
    assert findings == []


def test_every_ops_connect_site_is_classified():
    assert mod._scan_registry() == []


def test_registry_entries_exist_and_are_disjoint():
    assert not set(mod.DURABLE_STORES) & set(mod.EXCLUDED)
    for relative in (*mod.DURABLE_STORES, *mod.EXCLUDED):
        assert (REPO / relative).exists(), relative
    for reason in mod.EXCLUDED.values():
        assert reason.strip(), "an exclusion must carry a reason"


def test_main_passes_on_current_tree():
    assert mod.main([]) == 0


def test_compliant_source_has_no_findings():
    assert mod.scan_source("fake.py", COMPLIANT) == []


def test_writable_connect_without_full_is_caught():
    source = COMPLIANT.replace('        db.execute("PRAGMA synchronous=FULL")\n', "")
    findings = mod.scan_source("fake.py", source)
    assert len(findings) == 1
    assert "without PRAGMA synchronous=FULL" in findings[0]


def test_missing_begin_immediate_is_caught():
    source = COMPLIANT.replace('        db.execute("BEGIN IMMEDIATE")\n', "")
    findings = mod.scan_source("fake.py", source)
    assert any("never issues BEGIN IMMEDIATE" in f for f in findings)


def test_read_only_connect_needs_no_full():
    """attempt.inspect() opens ?mode=ro and legitimately skips the pragma."""
    source = '''
import sqlite3

def begin():
    other.execute("BEGIN IMMEDIATE")

def inspect(path):
    return sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
'''
    assert mod.scan_source("fake.py", source) == []


def test_in_memory_connect_needs_no_full():
    """execution/store.py builds :memory: reference schemas to diff layouts."""
    source = '''
import sqlite3

def begin():
    other.execute("BEGIN IMMEDIATE")

def validate_layout():
    return sqlite3.connect(":memory:")
'''
    assert mod.scan_source("fake.py", source) == []


def test_module_level_connect_is_caught():
    source = '''
import sqlite3

other.execute("BEGIN IMMEDIATE")
DB = sqlite3.connect("/data/book.sqlite")
'''
    findings = mod.scan_source("fake.py", source)
    assert any("module-level sqlite3.connect" in f for f in findings)


def test_pragma_spelling_variants_are_accepted():
    """Whitespace and case must not decide compliance."""
    source = COMPLIANT.replace(
        '"PRAGMA synchronous=FULL"', "'pragma  synchronous = full'")
    assert mod.scan_source("fake.py", source) == []


def test_docstring_mention_does_not_satisfy_the_contract():
    """Only executed statements count — prose naming the pragma must not pass."""
    source = '''
"""This store uses PRAGMA synchronous=FULL and BEGIN IMMEDIATE throughout."""
import sqlite3

def _transaction(self):
    return sqlite3.connect(self.uri, uri=True)
'''
    findings = mod.scan_source("fake.py", source)
    assert any("never issues BEGIN IMMEDIATE" in f for f in findings)
    assert any("without PRAGMA synchronous=FULL" in f for f in findings)


def test_executescript_counts_as_executed_sql():
    """execution/store.py opens its creating transaction via executescript()."""
    source = '''
import sqlite3

def _connect(self):
    db = sqlite3.connect(self.path, isolation_level=None, timeout=30)
    db.execute("PRAGMA synchronous=FULL")
    return db

def create(self, db):
    db.executescript("BEGIN IMMEDIATE;\\n" + SCHEMA + "\\nCOMMIT;")
'''
    assert mod.scan_source("fake.py", source) == []
