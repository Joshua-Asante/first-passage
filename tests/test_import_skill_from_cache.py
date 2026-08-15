"""Tests for scripts/import_skill_from_cache.py — one-time deployed -> repo seed."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_IS_PATH = Path(__file__).resolve().parent.parent / "scripts" / "import_skill_from_cache.py"
_spec = importlib.util.spec_from_file_location("import_skill_from_cache", _IS_PATH)
isc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(isc)


def _mk_skill(root: Path, skill: str, files: dict[str, str]) -> Path:
    d = root / skill
    for rel, content in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return d


def test_import_copies_all_files(tmp_path):
    bundle = tmp_path / "bundle"
    repo = tmp_path / "repo_skills"
    _mk_skill(bundle, "alpha", {
        "SKILL.md": "# alpha\n",
        "scripts/step0.py": "print('x')\n",
        "references/notes.md": "notes\n",
    })
    rc, msg = isc.import_skill(bundle / "alpha", repo / "alpha")
    assert rc == 0, msg
    assert (repo / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "# alpha\n"
    assert (repo / "alpha" / "scripts" / "step0.py").exists()
    assert (repo / "alpha" / "references" / "notes.md").exists()
    assert "3 file(s)" in msg


def test_refuses_when_repo_copy_exists(tmp_path):
    bundle = tmp_path / "bundle"
    repo = tmp_path / "repo_skills"
    _mk_skill(bundle, "alpha", {"SKILL.md": "bundle version\n"})
    _mk_skill(repo, "alpha", {"SKILL.md": "repo version\n"})
    rc, msg = isc.import_skill(bundle / "alpha", repo / "alpha")
    assert rc == 1
    assert "REFUSED" in msg
    # Repo copy untouched.
    assert (repo / "alpha" / "SKILL.md").read_text(encoding="utf-8") == "repo version\n"


def test_errors_when_source_missing(tmp_path):
    rc, msg = isc.import_skill(tmp_path / "bundle" / "ghost", tmp_path / "repo" / "ghost")
    assert rc == 2
    assert not (tmp_path / "repo" / "ghost").exists()


def test_errors_when_source_lacks_skill_md(tmp_path):
    bundle = tmp_path / "bundle"
    (bundle / "alpha").mkdir(parents=True)
    (bundle / "alpha" / "readme.txt").write_text("not a skill\n", encoding="utf-8")
    rc, msg = isc.import_skill(bundle / "alpha", tmp_path / "repo" / "alpha")
    assert rc == 2
    assert "SKILL.md" in msg
    assert not (tmp_path / "repo" / "alpha").exists()


def test_main_exit_codes_and_source_flag(tmp_path):
    bundle = tmp_path / "bundle"
    repo = tmp_path / "repo_skills"
    _mk_skill(bundle, "alpha", {"SKILL.md": "x\n"})
    rc = isc.main(["alpha", "--source", str(bundle), "--repo-skills", str(repo)])
    assert rc == 0
    assert (repo / "alpha" / "SKILL.md").exists()
    # Second run refuses — the seed is one-time.
    rc = isc.main(["alpha", "--source", str(bundle), "--repo-skills", str(repo)])
    assert rc == 1
