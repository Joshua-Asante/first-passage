"""Cross-consumer contracts; expected results do not come from policies."""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_root_nested_contract_and_git_unavailable(tmp_path, monkeypatch):
    root, nested = load("check_root_doc_liveness"), load("check_md_relative_links")
    (tmp_path / "sub").mkdir()
    (tmp_path / "live.md").touch()
    doc = tmp_path / "sub/a.md"
    doc.write_text('[live](live.md "title")\n[x](missing.md#anchor)\n'
                   '[token](r0)\n[x](lost.md) git show old\n'
                   '[url](https://example.org) [anchor](#here)\n', encoding="utf-8")
    def unavailable(*args, **kwargs):
        raise FileNotFoundError("git unavailable")
    monkeypatch.setattr(subprocess, "run", unavailable)
    assert root.check_doc(doc, tmp_path) == [
        "a.md:2: dead link -> missing.md#anchor", "a.md:3: dead link -> r0"]
    assert nested.check_file(doc, tmp_path) == [
        "sub/a.md:1: dead link -> live.md", "sub/a.md:2: dead link -> missing.md#anchor"]


def test_root_cli_from_outside_checkout(tmp_path):
    (tmp_path / "README.md").write_text("[missing](absent.md)", encoding="utf-8")
    result = subprocess.run([sys.executable, "-I", str(SCRIPTS / "check_root_doc_liveness.py"),
                             "--repo-root", str(tmp_path), "--docs", "README.md"],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 1
    assert "HARD: README.md:1: dead link -> absent.md" in result.stdout


def test_link_policy_resolution_rejects_unknown(tmp_path):
    assert (SCRIPTS / "link_policy.py").is_file(), "shared policy owner missing"
    policy = load("link_policy")
    with pytest.raises(ValueError):
        policy.link_target(tmp_path / "a.md", tmp_path, "b.md", "unknown")
    assert policy.link_target(tmp_path / "sub/a.md", tmp_path, "b.md", "repo") == tmp_path / "b.md"
