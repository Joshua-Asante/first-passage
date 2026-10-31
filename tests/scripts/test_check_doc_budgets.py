"""Behavioral contracts for the orientation-document byte budgets."""
import importlib.util
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/check_doc_budgets.py"


@pytest.fixture
def checker():
    spec = importlib.util.spec_from_file_location("check_doc_budgets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    for name, body in {"A.md": b"x" * 10, "S.md": b"y" * 20, "P.md": b"z" * 5}.items():
        (tmp_path / name).write_bytes(body)
    subprocess.run(["git", "add", "--", "A.md", "S.md", "P.md"], cwd=tmp_path, check=True)
    return tmp_path


CONFIG = """version: 1
files:
  A.md: {a}
  S.md: 20
  P.md: 5
t0:
  files: [A.md, S.md]
  cap: {t0}
"""


def run(checker, repo, capsys, text):
    config = repo / "scripts/doc_budgets.yml"
    config.parent.mkdir(exist_ok=True)
    config.write_text(text, encoding="utf-8")
    code = checker.main([], repo_root=repo)
    out = capsys.readouterr()
    return code, out.out, out.err


def test_at_cap_passes_and_reports_headroom(checker, repo, capsys):
    code, out, _ = run(checker, repo, capsys, CONFIG.format(a=10, t0=31))
    assert code == 0
    assert "ok A.md: 10 / 10 B (headroom 0)" in out
    assert "ok t0 (A.md + S.md + hook): 30 / 31 B (headroom 1)" in out


def test_file_over_cap_fails(checker, repo, capsys):
    code, out, _ = run(checker, repo, capsys, CONFIG.format(a=9, t0=31))
    assert code == 1
    assert "OVER A.md: 10 / 9 B (headroom -1)" in out


def test_t0_over_cap_fails(checker, repo, capsys):
    code, out, _ = run(checker, repo, capsys, CONFIG.format(a=10, t0=29))
    assert code == 1
    assert "OVER t0" in out


@pytest.mark.parametrize("ending", [b"\r\n", b"\r"])
def test_line_endings_are_measured_lf_normalised(checker, repo, capsys, ending):
    (repo / "A.md").write_bytes(b"abcd" + ending + b"efgh" + ending)  # 10 bytes as LF
    code, out, _ = run(checker, repo, capsys, CONFIG.format(a=10, t0=30))
    assert code == 0, out
    assert "ok A.md: 10 / 10 B" in out


@pytest.mark.parametrize("name, setup", [
    ("missing.md", None),
    ("untracked.md", b"tiny"),
])
def test_missing_or_untracked_path_fails_closed(checker, repo, capsys, name, setup):
    if setup is not None:
        (repo / name).write_bytes(setup)
    text = CONFIG.format(a=10, t0=31).replace("  P.md: 5\n", f"  P.md: 5\n  {name}: 100\n")
    code, _, err = run(checker, repo, capsys, text)
    assert code == 2
    assert f"{name}: not a tracked file" in err


@pytest.mark.parametrize("text, message", [
    ("", "empty or not a mapping"),
    ("version: 1\n", "keys must be"),
    ("- a\n- b\n", "empty or not a mapping"),
    ("version: 1\nfiles: {A.md: 10}\nt0: {files: [A.md], cap: 99}\nextra: 1\n", "keys must be"),
    ("version: 2\nfiles: {A.md: 10}\nt0: {files: [A.md], cap: 99}\n", "unsupported version"),
    ("version: 1\nfiles: {}\nt0: {files: [A.md], cap: 99}\n", "non-empty mapping"),
    ("version: 1\nfiles: {A.md: 0}\nt0: {files: [A.md], cap: 99}\n", "positive integer"),
    ("version: 1\nfiles: {A.md: '10'}\nt0: {files: [A.md], cap: 99}\n", "positive integer"),
    ("version: 1\nfiles: {A.md: true}\nt0: {files: [A.md], cap: 99}\n", "positive integer"),
    ("version: 1\nfiles: {A.md: 10}\nt0: {files: [], cap: 99}\n", "non-empty list"),
    ("version: 1\nfiles: {A.md: 10}\nt0: {files: [A.md, A.md], cap: 99}\n", "without repeats"),
    ("version: 1\nfiles: {A.md: 10}\nt0: {files: [A.md]}\n", "exactly files and cap"),
    ("version: 1\nfiles: {A.md: 10\n", "check_doc_budgets:"),
])
def test_malformed_config_fails_closed(checker, repo, capsys, text, message):
    code, out, err = run(checker, repo, capsys, text)
    assert code == 2
    assert message in err
    assert out == ""


def test_missing_config_fails_closed(checker, repo, capsys):
    assert checker.main([], repo_root=repo) == 2
    assert "missing" in capsys.readouterr().err
