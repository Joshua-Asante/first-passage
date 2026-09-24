"""Tests for scripts/evidence_archive.py — the second copy of every pinned private file.

M-41 records three losses of private evidence whose only copy sat in a disposable
worktree or VM. These tests pin the archive's safety properties: `put` never
stages into anything but a first-passage-archive clone and verifies every copy;
`audit` tells pushed from unpushed from missing and never fails the run.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("evidence_archive", REPO / "scripts" / "evidence_archive.py")
ea = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = ea
_spec.loader.exec_module(ea)

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")


def git(cwd: Path, *args: str) -> None:
    env = dict(os.environ, GIT_AUTHOR_NAME="T", GIT_AUTHOR_EMAIL="t@example.com",
               GIT_COMMITTER_NAME="T", GIT_COMMITTER_EMAIL="t@example.com")
    subprocess.run(["git", *args], cwd=cwd, check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


PRIVATE = b"private evidence bytes\n"
LOST = sha(b"bytes nobody kept\n")
CRLF = b"a,b\r\nc,d\r\n"


@pytest.fixture
def public(tmp_path):
    """A checkout pinning one present file (manifest) and one lost file (registry)."""
    root = tmp_path / "public"
    (root / "data").mkdir(parents=True)
    git(root, "init", "-q", "-b", "main")
    (root / "data" / "a.csv").write_bytes(PRIVATE)
    (root / "data" / "SHA256SUMS").write_text(f"# comment\n{sha(PRIVATE)} *a.csv\n", encoding="utf-8")
    registry = root / ea.REGISTRY
    registry.parent.mkdir(parents=True)
    registry.write_text(f"# header\n\n{LOST}  somewhere/receipt.json\n", encoding="utf-8")
    git(root, "add", "data/SHA256SUMS", str(ea.REGISTRY))
    git(root, "commit", "-q", "-m", "seed")
    return root


def make_clone(tmp_path: Path, name: str) -> Path:
    bare = tmp_path / "remote" / f"{name}.git"
    bare.mkdir(parents=True)
    git(bare, "init", "-q", "--bare", "-b", "main")
    clone = tmp_path / f"{name}-clone"
    git(tmp_path, "clone", "-q", str(bare), str(clone))
    (clone / "README.md").write_text("archive\n", encoding="utf-8")
    git(clone, "add", "README.md")
    git(clone, "commit", "-q", "-m", "seed")
    git(clone, "push", "-q", "-u", "origin", "main")
    return clone


def run_audit(public, archive, **kw):
    out = io.StringIO()
    counts = ea.audit(public, archive, out=out, **kw)
    return counts, out.getvalue()


def test_collect_pins_reads_manifests_and_registry(public):
    pins = ea.collect_pins(public)
    assert {(p.digest, p.name, p.manifest) for p in pins} == {
        (sha(PRIVATE), "a.csv", "data/SHA256SUMS"),
        (LOST, "somewhere/receipt.json", ea.REGISTRY.as_posix()),
    }
    by_manifest = {p.manifest: p for p in pins}
    assert by_manifest["data/SHA256SUMS"].local_path(public) == public / "data" / "a.csv"
    assert by_manifest[ea.REGISTRY.as_posix()].local_path(public) == public / "somewhere" / "receipt.json"


def test_audit_without_an_archive_clone_is_unverified(public, tmp_path):
    counts, out = run_audit(public, tmp_path / "absent")
    assert out.startswith("UNVERIFIED") and "2 pinned digests unchecked" in out
    assert sum(counts.values()) == 0


def test_put_refuses_a_clone_that_is_not_the_archive(public, tmp_path):
    other = make_clone(tmp_path, "first-passage")
    assert ea.put([public / "data" / "a.csv"], other, public) == 2
    assert not (other / "evidence").exists()


def test_put_then_push_moves_a_pin_from_missing_to_archived(public, tmp_path):
    archive = make_clone(tmp_path, "first-passage-archive")
    counts, _ = run_audit(public, archive)
    assert counts["MISSING"] == 2

    assert ea.put([public / "data" / "a.csv"], archive, public, out=io.StringIO()) == 0
    blob = archive / ea.blob_path(sha(PRIVATE))
    assert blob.read_bytes() == PRIVATE
    row = (archive / ea.INDEX).read_text(encoding="utf-8").strip().split("\t")
    assert row[0] == sha(PRIVATE) and row[-1] == "data/a.csv"
    counts, out = run_audit(public, archive)
    assert (counts["UNPUSHED"], counts["MISSING"]) == (1, 1)
    assert "somewhere/receipt.json" in out

    git(archive, "add", "evidence")
    git(archive, "commit", "-q", "-m", "evidence")
    git(archive, "push", "-q")
    counts, out = run_audit(public, archive)
    assert (counts["ARCHIVED"], counts["MISSING"]) == (1, 1)
    assert "a.csv" not in out


def test_put_is_idempotent(public, tmp_path):
    archive = make_clone(tmp_path, "first-passage-archive")
    for _ in range(2):
        ea.put([public / "data" / "a.csv"], archive, public, out=io.StringIO())
    assert len((archive / ea.INDEX).read_text(encoding="utf-8").splitlines()) == 1


def test_put_skips_files_github_would_reject(public, tmp_path, monkeypatch):
    archive = make_clone(tmp_path, "first-passage-archive")
    monkeypatch.setattr(ea, "MAX_BYTES", 4)
    ea.put([public / "data" / "a.csv"], archive, public, out=io.StringIO())
    assert not (archive / ea.blob_path(sha(PRIVATE))).exists()


def test_verify_flags_bytes_that_do_not_match_their_address(public, tmp_path):
    archive = make_clone(tmp_path, "first-passage-archive")
    blob = archive / ea.blob_path(sha(PRIVATE))
    blob.parent.mkdir(parents=True)
    blob.write_bytes(b"tampered\n")
    assert run_audit(public, archive)[0]["UNPUSHED"] == 1
    assert run_audit(public, archive, verify=True)[0]["CORRUPT"] == 1


def test_main_audit_is_report_only(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("FP_EVIDENCE_ARCHIVE", str(tmp_path / "absent"))
    assert ea.main(["audit"]) == 0
    assert "UNVERIFIED" in capsys.readouterr().out


def test_registry_digests_are_well_formed_and_unique():
    pins = [p for p in ea.collect_pins(REPO) if p.manifest == ea.REGISTRY.as_posix()]
    assert pins, "the registry is read"
    digests = [p.digest for p in pins]
    assert len(digests) == len(set(digests))


def commit_crlf_under_autocrlf(public, tmp_path, *, attributes: bool):
    """Pin CRLF bytes in the public repo, put them into the archive, then commit
    with a hostile core.autocrlf=true. Returns (archive, digest, committed blob)."""
    digest = sha(CRLF)
    (public / "data" / "b.csv").write_bytes(CRLF)
    sums = public / "data" / "SHA256SUMS"
    sums.write_text(sums.read_text(encoding="utf-8") + f"{digest} *b.csv\n", encoding="utf-8")
    git(public, "add", "data")
    git(public, "commit", "-q", "-m", "pin b.csv")
    archive = make_clone(tmp_path, "first-passage-archive")
    ea.put([public / "data" / "b.csv"], archive, public, out=io.StringIO())
    if not attributes:
        (archive / "evidence" / ".gitattributes").unlink()
    git(archive, "-c", "core.autocrlf=true", "add", "evidence")
    git(archive, "commit", "-q", "-m", "evidence")
    git(archive, "push", "-q")
    blob = subprocess.run(["git", "cat-file", "blob", f"HEAD:{ea.blob_path(digest)}"],
                          cwd=archive, capture_output=True, check=True).stdout
    return archive, digest, blob


def test_put_writes_evidence_gitattributes(public, tmp_path):
    archive = make_clone(tmp_path, "first-passage-archive")
    ea.put([public / "data" / "a.csv"], archive, public, out=io.StringIO())
    assert (archive / "evidence" / ".gitattributes").read_bytes() == b"* -text\n"


def test_put_refuses_conflicting_gitattributes(public, tmp_path):
    archive = make_clone(tmp_path, "first-passage-archive")
    attributes = archive / "evidence" / ".gitattributes"
    attributes.parent.mkdir(parents=True)
    attributes.write_bytes(b"* text\n")
    assert ea.put([public / "data" / "a.csv"], archive, public, out=io.StringIO()) == 2
    assert not (archive / ea.blob_path(sha(PRIVATE))).exists()


def test_put_prints_autocrlf_safe_commands(public, tmp_path):
    archive = make_clone(tmp_path, "first-passage-archive")
    out = io.StringIO()
    ea.put([public / "data" / "a.csv"], archive, public, out=out)
    assert "-c core.autocrlf=false add evidence" in out.getvalue()
    assert "-c core.autocrlf=false commit" in out.getvalue()


def test_crlf_bytes_survive_commit_under_autocrlf(public, tmp_path):
    archive, digest, blob = commit_crlf_under_autocrlf(public, tmp_path, attributes=True)
    assert sha(blob) == digest
    assert run_audit(public, archive, verify=True)[0]["CORRUPT"] == 0


def test_control_without_attributes_autocrlf_corrupts(public, tmp_path):
    _, digest, blob = commit_crlf_under_autocrlf(public, tmp_path, attributes=False)
    if sha(blob) == digest:
        pytest.skip("git did not convert CRLF to LF on checkin here; the control cannot bite")
    assert sha(blob) != digest


def test_verify_hashes_committed_blob_not_working_tree(public, tmp_path):
    archive, digest, blob = commit_crlf_under_autocrlf(public, tmp_path, attributes=False)
    if sha(blob) == digest:
        pytest.skip("git did not convert CRLF to LF on checkin here; the control cannot bite")
    (archive / ea.blob_path(digest)).write_bytes(CRLF)
    assert run_audit(public, archive, verify=True)[0]["CORRUPT"] >= 1
    assert run_audit(public, archive, verify=False)[0]["ARCHIVED"] >= 1
