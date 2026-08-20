"""Unit tests for scripts/check_instrument_ledger_coverage.py -- mechanical
pre-flight for ops/instruments/<SYM>.md coverage (docs/operational_rules.md
§8, added after the 2026-08-19 D5/MNQ near-miss)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_PATH = REPO_ROOT / "scripts" / "check_instrument_ledger_coverage.py"
_spec = importlib.util.spec_from_file_location("check_instrument_ledger_coverage", _PATH)
cilc = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = cilc
_spec.loader.exec_module(cilc)


def _make_instruments_dir(tmp_path: Path) -> Path:
    d = tmp_path / "ops" / "instruments"
    d.mkdir(parents=True)
    for name in ("MNQ.md", "MYM.md", "6J.md", "MECHANISMS.md", "PROFILES.md"):
        (d / name).write_text(f"# {name}\n", encoding="utf-8")
    return d


def test_known_symbols_excludes_non_symbol_files(tmp_path: Path):
    d = _make_instruments_dir(tmp_path)
    symbols = cilc.known_symbols(d)
    assert set(symbols) == {"MNQ", "MYM", "6J"}
    assert "MECHANISMS" not in symbols
    assert "PROFILES" not in symbols


def test_known_symbols_empty_dir_returns_empty():
    assert cilc.known_symbols(Path("/does/not/exist")) == []


def test_find_mentioned_symbols_is_whole_word_only():
    symbols = ["ES", "NQ"]
    # NQFLOW-1 must NOT count as a match for bare "NQ" -- \b requires a real
    # word boundary, and "NQF..." has none between Q and F.
    mentioned = cilc.find_mentioned_symbols("This mentions ES directly; NQFLOW-1 is a different token.", symbols)
    assert mentioned == ["ES"]
    # A real whole-word "NQ" elsewhere in the same text is expected to match.
    mentioned_both = cilc.find_mentioned_symbols("ES and NQ both appear here, plus NQFLOW-1.", symbols)
    assert mentioned_both == ["ES", "NQ"]


def test_cites_ledger_detects_relative_path_variants():
    text_a = "See [MNQ ledger](../../ops/instruments/MNQ.md) for details."
    text_b = "cite: `ops/instruments/MNQ.md`"
    text_c = "no mention of the ledger here at all"
    assert cilc.cites_ledger(text_a, "MNQ") is True
    assert cilc.cites_ledger(text_b, "MNQ") is True
    assert cilc.cites_ledger(text_c, "MNQ") is False


def test_rejected_candidates_hits_counts_whole_word_only():
    text = "MNQ appears here. MNQFLOW-1 should not inflate the MNQ count."
    assert cilc.rejected_candidates_hits("MNQ", text) == 2  # the two real "MNQ" whole-word tokens


def _setup_repo(tmp_path: Path) -> Path:
    _make_instruments_dir(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "rejected_candidates.md").write_text(
        "# Rejected\n\nMNQ mentioned once here.\n", encoding="utf-8")
    return tmp_path


def test_main_warns_when_symbol_mentioned_without_ledger_citation(tmp_path: Path, capsys):
    repo = _setup_repo(tmp_path)
    target = tmp_path / "draft.md"
    target.write_text("The D5 axis on MNQ is genuinely unspent.\n", encoding="utf-8")
    rc = cilc.main([str(target), "--repo-root", str(repo)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "WARN" in out
    assert "MNQ" in out
    assert "instruments/MNQ.md" in out


def test_main_ok_when_ledger_is_cited(tmp_path: Path, capsys):
    repo = _setup_repo(tmp_path)
    target = tmp_path / "draft.md"
    target.write_text(
        "The D5 axis on MNQ was already killed twice -- see `ops/instruments/MNQ.md` finding N5.\n",
        encoding="utf-8")
    rc = cilc.main([str(target), "--repo-root", str(repo)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "WARN" not in out
    assert "OK: every mentioned instrument symbol" in out


def test_main_nothing_to_check_when_no_symbols_mentioned(tmp_path: Path, capsys):
    repo = _setup_repo(tmp_path)
    target = tmp_path / "draft.md"
    target.write_text("This artifact never names a known instrument symbol.\n", encoding="utf-8")
    rc = cilc.main([str(target), "--repo-root", str(repo)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "no known instrument symbols mentioned" in out


def test_main_exits_two_on_missing_target():
    rc = cilc.main(["/does/not/exist.md"])
    assert rc == 2


def test_main_exits_zero_when_no_instrument_ledgers_exist(tmp_path: Path, capsys):
    empty_repo = tmp_path / "empty_repo"
    empty_repo.mkdir()
    target = tmp_path / "draft.md"
    target.write_text("MNQ mentioned but no ledger directory exists.\n", encoding="utf-8")
    rc = cilc.main([str(target), "--repo-root", str(empty_repo)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "nothing to check" in out
