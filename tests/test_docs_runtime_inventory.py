"""P3 docs-runtime inventory — quoted-path + pathlib-join, report-only --check."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check_docs_runtime_inventory.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_docs_runtime_inventory", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_tmp_tree_quoted_claude_and_pathlib_docs_join(tmp_path):
    inv = _load()
    (tmp_path / "ops" / "recall").mkdir(parents=True)
    (tmp_path / "ops" / "c1_rail").mkdir(parents=True)
    (tmp_path / "ops" / "recall" / "guard.py").write_text(
        "claude_md = repo_root / \"CLAUDE.md\"\n",
        encoding="utf-8",
    )
    (tmp_path / "ops" / "c1_rail" / "c1_rail_arm.py").write_text(
        'DEFAULT = _REPO_ROOT / "docs" / "notes" / "x.json"\n',
        encoding="utf-8",
    )
    hits = inv.scan_tree(tmp_path)
    cited = {h.cited for h in hits}
    assert "CLAUDE.md" in cited
    assert any(c == "docs/notes/x.json" or c.startswith("docs/notes/") for c in cited)


def test_real_repo_known_runtime_reads():
    inv = _load()
    hits = inv.scan_tree(REPO)
    pairs = {(h.source.replace("\\", "/"), h.cited.replace("\\", "/")) for h in hits}
    assert any(
        src.endswith("ops/recall/guard.py") and cited == "CLAUDE.md"
        for src, cited in pairs
    )
    assert any(
        src.endswith("ops/c1_rail/c1_rail_arm.py")
        and "M1_MONITORING_ACCEPTANCE.json" in cited
        for src, cited in pairs
    )
    assert any(
        src.endswith("lab/discovery/register_search.py") and cited.startswith("docs/")
        for src, cited in pairs
    )


def test_check_missing_row_warns_and_exits_zero(tmp_path):
    inv = _load()
    (tmp_path / "ops").mkdir()
    (tmp_path / "ops" / "hit.py").write_text(
        'p = root / "CLAUDE.md"\n',
        encoding="utf-8",
    )
    report = tmp_path / "docs" / "notes" / "audits" / "docs-runtime-inventory.md"
    report.parent.mkdir(parents=True)
    report.write_text("# stale\n\nNo CLAUDE.md row.\n", encoding="utf-8")
    rc = inv.main(["--check", "--root", str(tmp_path), "--report", str(report)])
    assert rc == 0


def test_check_matching_is_clean(tmp_path):
    inv = _load()
    (tmp_path / "ops").mkdir()
    (tmp_path / "ops" / "hit.py").write_text(
        'p = root / "CLAUDE.md"\n',
        encoding="utf-8",
    )
    report = tmp_path / "inv.md"
    assert inv.main(["--write", "--root", str(tmp_path), "--report", str(report)]) == 0
    captured = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--check",
            "--root",
            str(tmp_path),
            "--report",
            str(report),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert captured.returncode == 0
    assert "CLEAN" in captured.stdout
