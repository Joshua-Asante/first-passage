"""Adversarial tests for scripts/check_lab_path_relocation.py.

Relocation rot is a dead ``lab/…`` citation whose path *tail* still exists
elsewhere under ``lab/`` (theme-nest or archive move). Pruned-by-design
harnesses (Great Prune) have no live twin and must NOT flag — otherwise the
gate is noise from day one.

Every REQUIRED failure mode below has a fixture that must FAIL the checker's
predicate, and the live / pruned / compliant fixtures must PASS. Removing any
limb of the production classifier must turn at least one of these red.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "check_lab_path_relocation",
    REPO / "scripts" / "check_lab_path_relocation.py",
)
clr = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
sys.modules[_SPEC.name] = clr  # required before dataclass exec on 3.12+
_SPEC.loader.exec_module(clr)


def _lab_tree(root: Path) -> None:
    """Minimal lab index: one theme-nested study + one archive twin + decoy."""
    (root / "lab" / "analysis" / "regime" / "decompound_remc_2026-06-07").mkdir(
        parents=True
    )
    (
        root / "lab" / "analysis" / "regime" / "decompound_remc_2026-06-07" / "RESULTS.md"
    ).write_text("# results\n", encoding="utf-8")
    (root / "lab" / "archive" / "usoil_rdm").mkdir(parents=True)
    (root / "lab" / "archive" / "usoil_rdm" / "RESULTS.md").write_text(
        "# archived\n", encoding="utf-8"
    )
    # Ambiguous twin: same slug/file under two live locations.
    (root / "lab" / "analysis" / "orb" / "shared_slug").mkdir(parents=True)
    (root / "lab" / "analysis" / "c1" / "shared_slug").mkdir(parents=True)
    (root / "lab" / "analysis" / "orb" / "shared_slug" / "NOTES.md").write_text(
        "orb\n", encoding="utf-8"
    )
    (root / "lab" / "analysis" / "c1" / "shared_slug" / "NOTES.md").write_text(
        "c1\n", encoding="utf-8"
    )


def _docs(root: Path, name: str, body: str) -> Path:
    p = root / "docs" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


# ── classify_citation: four limbs ──────────────────────────────────


def test_relocated_path_flags(tmp_path: Path):
    _lab_tree(tmp_path)
    cited = "lab/analysis/decompound_remc_2026-06-07/RESULTS.md"
    kind, targets = clr.classify_citation(cited, tmp_path)
    assert kind == "relocated"
    assert targets == [
        "lab/analysis/regime/decompound_remc_2026-06-07/RESULTS.md"
    ]


def test_pruned_by_design_does_not_flag(tmp_path: Path):
    """Great-Prune harness: dead, no twin anywhere under lab/ → not relocation."""
    _lab_tree(tmp_path)
    cited = "lab/analysis/decompound_remc_2026-06-07/run_harness.py"
    kind, targets = clr.classify_citation(cited, tmp_path)
    assert kind is None
    assert targets == []


def test_ambiguous_multi_match_reports_not_rewrites(tmp_path: Path):
    _lab_tree(tmp_path)
    cited = "lab/analysis/shared_slug/NOTES.md"
    kind, targets = clr.classify_citation(cited, tmp_path)
    assert kind == "ambiguous"
    assert targets == [
        "lab/analysis/c1/shared_slug/NOTES.md",
        "lab/analysis/orb/shared_slug/NOTES.md",
    ]


def test_live_path_does_not_flag(tmp_path: Path):
    _lab_tree(tmp_path)
    cited = "lab/analysis/regime/decompound_remc_2026-06-07/RESULTS.md"
    kind, targets = clr.classify_citation(cited, tmp_path)
    assert kind is None
    assert targets == []


def test_archive_move_is_relocated(tmp_path: Path):
    _lab_tree(tmp_path)
    cited = "lab/analysis/usoil_rdm/RESULTS.md"
    kind, targets = clr.classify_citation(cited, tmp_path)
    assert kind == "relocated"
    assert targets == ["lab/archive/usoil_rdm/RESULTS.md"]


# ── scan_docs + CLI severity ───────────────────────────────────────


def test_scan_docs_flags_relocated_and_skips_pruned(tmp_path: Path):
    _lab_tree(tmp_path)
    _docs(
        tmp_path,
        "note.md",
        "See lab/analysis/decompound_remc_2026-06-07/RESULTS.md "
        "and the pruned lab/analysis/decompound_remc_2026-06-07/run_harness.py.\n",
    )
    findings = clr.scan_docs(tmp_path)
    kinds = {f.kind for f in findings}
    cited = {f.cited for f in findings}
    assert "relocated" in kinds
    assert "lab/analysis/decompound_remc_2026-06-07/RESULTS.md" in cited
    assert "lab/analysis/decompound_remc_2026-06-07/run_harness.py" not in cited


def test_scan_docs_reports_ambiguous(tmp_path: Path):
    _lab_tree(tmp_path)
    _docs(tmp_path, "ambig.md", "Pointer: lab/analysis/shared_slug/NOTES.md\n")
    findings = clr.scan_docs(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == "ambiguous"
    assert len(findings[0].targets) == 2


def test_intentional_evidence_docs_are_skipped(tmp_path: Path):
    """Audit artifacts that *document* the stale path must not keep the gate noisy."""
    _lab_tree(tmp_path)
    rel = (
        "notes/audits/programme-audit/2026-08-05-claim-alignment/05-cosmetic.md"
    )
    _docs(
        tmp_path,
        rel,
        "Finding cites lab/analysis/decompound_remc_2026-06-07/RESULTS.md as evidence.\n",
    )
    assert clr.scan_docs(tmp_path) == []


def test_subject_context_citation_is_skipped(tmp_path: Path):
    """'which no longer resolves' documents the stale path — do not flag."""
    _lab_tree(tmp_path)
    _docs(
        tmp_path,
        "note.md",
        "Path note: cites lab/analysis/decompound_remc_2026-06-07/RESULTS.md, "
        "which no longer resolves (study moved).\n",
    )
    assert clr.scan_docs(tmp_path) == []


def test_main_warn_tier_exits_zero_with_findings(tmp_path: Path, capsys):
    _lab_tree(tmp_path)
    _docs(
        tmp_path,
        "rot.md",
        "lab/analysis/decompound_remc_2026-06-07/RESULTS.md\n",
    )
    assert clr.main(["--repo-root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "relocated" in out.lower() or "WARN" in out


def test_main_strict_exits_one_with_findings(tmp_path: Path):
    _lab_tree(tmp_path)
    _docs(
        tmp_path,
        "rot.md",
        "lab/analysis/decompound_remc_2026-06-07/RESULTS.md\n",
    )
    assert clr.main(["--repo-root", str(tmp_path), "--strict"]) == 1


def test_main_clean_corpus_exits_zero(tmp_path: Path, capsys):
    _lab_tree(tmp_path)
    _docs(
        tmp_path,
        "ok.md",
        "Live: lab/analysis/regime/decompound_remc_2026-06-07/RESULTS.md\n",
    )
    assert clr.main(["--repo-root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "0 finding" in out or "OK" in out


# ── adversarial: rewrite helper refuses multi-match ────────────────


def test_unique_target_or_none_refuses_ambiguous(tmp_path: Path):
    _lab_tree(tmp_path)
    assert (
        clr.unique_target_or_none("lab/analysis/shared_slug/NOTES.md", tmp_path)
        is None
    )
    assert (
        clr.unique_target_or_none(
            "lab/analysis/decompound_remc_2026-06-07/RESULTS.md", tmp_path
        )
        == "lab/analysis/regime/decompound_remc_2026-06-07/RESULTS.md"
    )


def test_unique_target_or_none_refuses_pruned(tmp_path: Path):
    _lab_tree(tmp_path)
    assert (
        clr.unique_target_or_none(
            "lab/analysis/decompound_remc_2026-06-07/run_harness.py", tmp_path
        )
        is None
    )
