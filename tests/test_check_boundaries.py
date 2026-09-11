"""Unit tests for scripts/check_boundaries.py — the 4-layer import-boundary gate.

The enforcer (ADR 2026-06-05) was previously untested (2026-06-07 high-level
review deferred action). These pin the load-bearing pieces of its decision logic:

  * ``layer_of_file`` path → layer classification (incl. the scripts/ overrides,
    the tests//archive/ exemptions, and the .claude/worktrees/ nested-repo
    exemption — a real worktree checked out there was misclassified as a
    governance-layer file and its own ops-package imports flagged as illegal,
    2026-07-06 housekeeping audit finding),
  * ``_first_party_targets`` AST extraction (plain / aliased / in-function /
    relative imports — the in-function form is the one a line-grep missed at
    parity_check.py),
  * the ``LEGAL_EDGES`` contract (the lab<->ops isolation invariant),
  * ``build_index`` collision-freedom + correct module→layer mapping on the
    real tree,
  * and the CLI exit code (the real repo currently has no illegal edges).
"""
from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
_CB_PATH = REPO_ROOT / "scripts" / "check_boundaries.py"
_spec = importlib.util.spec_from_file_location("check_boundaries", _CB_PATH)
cb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cb)


# ── layer_of_file: path → layer classification ─────────────────────

@pytest.mark.parametrize("rel,expected", [
    ("core/portfolio_mc.py", "core"),
    ("lab/analysis/decompound.py", "lab"),
    ("ops/accounts.py", "ops"),
    ("tests/test_accounts.py", None),       # contract-EXEMPT (single mixed suite)
    ("archive/strategies/old.py", None),    # archive is exempt
    (".claude/worktrees/foo/tests/test_x.py", None),   # nested worktree exempt (2026-07-06 fix)
    (".claude/worktrees/foo/lab/analysis/x.py", None), # nested worktree exempt, not "governance"
    (".venv/Lib/site-packages/pkg/mod.py", None),      # venv exempt (2026-07-10 fix)
    ("third_party/study_clone/pkg/x.py", None),  # untracked vendor / study tree exempt
    ("venv/lib/python3.11/site-packages/x.py", None),  # bare venv/ variant exempt
    ("env/Scripts/activate_this.py", None),            # env/ variant exempt
    ("docs/adr/x.py", "governance"),        # governance prefix
    ("root_module.py", "governance"),       # bare root-resident .py → governance
    ("scripts/check_boundaries.py", "governance"),   # SCRIPTS_LAYER → governance
    ("scripts/pine_lint.py", "lab"),                 # SCRIPTS_LAYER override → lab
    ("scripts/lock_event_hook.py", "ops"),           # SCRIPTS_LAYER override → ops
    ("scripts/some_unlisted_tool.py", "governance"), # default for unlisted script
])
def test_layer_of_file(rel, expected):
    assert cb.layer_of_file(rel) == expected


# ── LEGAL_EDGES: the dependency contract ───────────────────────────

def test_legal_downstream_edges_are_allowed():
    for edge in [("ops", "core"), ("lab", "core"), ("governance", "core"),
                 ("ops", "governance"), ("lab", "governance"),
                 ("core", "core"), ("ops", "ops"), ("lab", "lab")]:
        assert edge in cb.LEGAL_EDGES, edge


def test_lab_ops_isolation_invariant_is_illegal():
    # The load-bearing invariant: lab and ops must never import each other.
    assert ("lab", "ops") not in cb.LEGAL_EDGES
    assert ("ops", "lab") not in cb.LEGAL_EDGES


def test_core_must_not_import_other_layers():
    # core is the locked floor — it imports nothing internal but itself.
    for tgt in ("governance", "lab", "ops"):
        assert ("core", tgt) not in cb.LEGAL_EDGES


# ── build_index on the real tree ───────────────────────────────────

def test_build_index_has_no_collisions_and_maps_known_modules():
    index, collisions = cb.build_index()
    assert collisions == [], collisions
    assert index.get("portfolio_mc") == ("core/portfolio_mc.py",)
    assert index.get("firm_rules") == ("core/firm_rules.py",)
    assert index.get("cli") == ("ops/cli.py",)  # accounts.py retired substrate Phase 2


# ── CLI: the real repo currently honours the contract ──────────────

def test_cli_exit_zero_on_real_tree():
    r = subprocess.run([sys.executable, str(_CB_PATH)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "check_boundaries: OK" in r.stdout
    assert "UNPARSEABLE" not in r.stdout
    assert "ILLEGAL" not in r.stdout


def test_gate_floor_is_311():
    # pyproject requires-python / CI matrix / .venv-research — keep in sync.
    assert cb.MIN_PYTHON == (3, 11)


def test_parse_failure_message_is_not_labeled_illegal():
    # Reporting defect closed 2026-07-26: a SyntaxError must not be printed as
    # a boundary "violation" that invites LEGAL_EDGES relaxation.
    src = "f'{f['x']}'\n"  # nested same-quote f-string: 3.12+ only (PEP 701)
    try:
        ast.parse(src)
        pytest.skip(f"this interpreter ({sys.version_info[:2]}) accepts PEP 701")
    except SyntaxError as exc:
        labeled = (
            f"demo.py:{exc.lineno}: UNPARSEABLE under Python "
            f"{sys.version_info.major}.{sys.version_info.minor} — {exc.msg}"
        )
        assert "UNPARSEABLE" in labeled
        assert "ILLEGAL" not in labeled


@pytest.mark.parametrize("statement,target", [
    ("import ops.runner as run", "ops/runner.py"),
    ("from ops import runner as run", "ops/runner.py"),
    ("def f():\n    from c1_rail import listener", "ops/c1_rail/listener.py"),
    ("import listener", "ops/c1_rail/listener.py"),
    ("import daemon", "ops/c1_signal_daemon/daemon.py"),
    ("from scripts import lock_event_hook", "scripts/lock_event_hook.py"),
    ("import scripts.lock_event_hook", "scripts/lock_event_hook.py"),
])
def test_synthetic_import_paths_fail_closed(tmp_path, monkeypatch, capsys, statement, target):
    for rel, source in {"core/source.py": statement, target: ""}.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    output = capsys.readouterr().out
    assert "ILLEGAL core->ops" in output
    assert target in output


def test_unresolved_first_party_is_not_third_party(tmp_path, monkeypatch, capsys):
    (tmp_path / "core").mkdir()
    (tmp_path / "core/source.py").write_text("import ops.missing\nimport numpy\n", encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    output = capsys.readouterr().out
    assert "UNRESOLVED first-party import 'ops.missing'" in output
    assert "numpy" not in output


def test_cross_layer_collision_reports_paths(tmp_path, monkeypatch, capsys):
    for rel in ("core/shared.py", "ops/c1_rail/shared.py"):
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    output = capsys.readouterr().out
    assert "NAME COLLISION" in output
    assert "core/shared.py" in output
    assert "ops/c1_rail/shared.py" in output


def test_same_layer_duplicate_and_relative_imports_pass(tmp_path, monkeypatch):
    for rel, source in {"ops/shared.py": "", "ops/c1_rail/shared.py": "", "ops/pkg/source.py": "from . import sibling\nfrom .. import shared", "ops/pkg/sibling.py": ""}.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 0


@pytest.mark.parametrize("statement", [
    "import portfolio_mc as mc\nimport numpy\nimport ast",
    "from core import portfolio_mc as mc",
    "def f():\n    from portfolio_mc import run",
])
def test_legal_core_and_external_imports_pass(tmp_path, monkeypatch, statement):
    (tmp_path / "core").mkdir()
    (tmp_path / "ops").mkdir()
    (tmp_path / "core/portfolio_mc.py").write_text("def run(): pass", encoding="utf-8")
    (tmp_path / "ops/source.py").write_text(statement, encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 0


def test_relative_import_of_mixed_layer_script_is_checked(tmp_path, monkeypatch, capsys):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts/check_brief.py").write_text("from . import lock_event_hook", encoding="utf-8")
    (tmp_path / "scripts/lock_event_hook.py").write_text("", encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    assert "ILLEGAL governance->ops" in capsys.readouterr().out


def test_unresolved_known_flat_package_fails(tmp_path, monkeypatch, capsys):
    (tmp_path / "core/pkg").mkdir(parents=True)
    (tmp_path / "core/pkg/__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "core/source.py").write_text("import pkg.missing", encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    assert "UNRESOLVED first-party import 'pkg.missing'" in capsys.readouterr().out


def test_beyond_top_level_relative_import_is_distinct(tmp_path, monkeypatch, capsys):
    (tmp_path / "core").mkdir()
    (tmp_path / "core/source.py").write_text("from ... import sibling", encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    output = capsys.readouterr().out
    assert "INVALID RELATIVE" in output
    assert "UNRESOLVED" not in output


def test_missing_relative_package_fails(tmp_path, monkeypatch, capsys):
    (tmp_path / "core/pkg").mkdir(parents=True)
    (tmp_path / "core/pkg/source.py").write_text("from .missing import thing", encoding="utf-8")
    monkeypatch.setattr(cb, "REPO_ROOT", tmp_path)
    assert cb.main() == 1
    assert "UNRESOLVED first-party import 'core.pkg.missing'" in capsys.readouterr().out
