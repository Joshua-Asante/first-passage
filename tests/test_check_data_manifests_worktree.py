"""Worktree / public-clone soft-degrade coverage for check_data_manifests.

Pins Algorithm brief #3 Step 2.3: per-directory absent-tree WARN+skip when
SHA256SUMS lists files but ZERO exist on disk; partial presence and hash
mismatch keep hard-fail; --regenerate is unaffected.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

_CDM_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_data_manifests.py"
_spec = importlib.util.spec_from_file_location("check_data_manifests", _CDM_PATH)
cdm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cdm)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_all_absent_dir_warns_and_exits_0(tmp_path, monkeypatch, capsys):
    d = tmp_path / "core/data/tv_exports/pepperstone"
    d.mkdir(parents=True)
    digest = _sha(b"ABSENT-PLACEHOLDER-a.csv")
    (d / "SHA256SUMS").write_text(f"{digest} *a.csv\n", encoding="utf-8")
    monkeypatch.setattr(cdm, "MANIFEST_DIRS", [d])
    monkeypatch.setattr(cdm, "REPO_ROOT", tmp_path)

    rc = cdm.check_all()
    assert rc == 0
    err = capsys.readouterr().err
    assert "WARN absent-tree skip" in err
    assert "pepperstone" in err


def test_partial_presence_hard_fails(tmp_path, monkeypatch, capsys):
    d = tmp_path / "core/data/bar_data"
    d.mkdir(parents=True)
    present = b"csv-bytes-1"
    digest_a = _sha(present)
    digest_b = _sha(b"ABSENT-PLACEHOLDER-b.csv")
    (d / "a.csv").write_bytes(present)
    (d / "SHA256SUMS").write_text(
        f"{digest_a} *a.csv\n{digest_b} *b.csv\n", encoding="utf-8",
    )
    monkeypatch.setattr(cdm, "MANIFEST_DIRS", [d])
    monkeypatch.setattr(cdm, "REPO_ROOT", tmp_path)

    rc = cdm.check_all()
    assert rc == 1
    err = capsys.readouterr().err
    assert "MISSING" in err
    assert "b.csv" in err
    assert "WARN absent-tree skip" not in err


def test_full_presence_hash_mismatch_hard_fails(tmp_path, monkeypatch, capsys):
    d = tmp_path / "core/data/external"
    d.mkdir(parents=True)
    (d / "a.csv").write_bytes(b"on-disk-content")
    wrong = _sha(b"different-content")
    (d / "SHA256SUMS").write_text(f"{wrong} *a.csv\n", encoding="utf-8")
    monkeypatch.setattr(cdm, "MANIFEST_DIRS", [d])
    monkeypatch.setattr(cdm, "REPO_ROOT", tmp_path)

    rc = cdm.check_all()
    assert rc == 1
    err = capsys.readouterr().err
    assert "MISMATCH" in err


def test_regenerate_unaffected_by_soft_degrade(tmp_path, monkeypatch):
    d = tmp_path / "core/data/tv_exports/cme"
    d.mkdir(parents=True)
    # Manifest lists a file that is absent — regenerate should rewrite from
    # on-disk CSVs (none) to an empty body, not soft-degrade.
    digest = _sha(b"ABSENT-PLACEHOLDER-old.csv")
    (d / "SHA256SUMS").write_text(f"{digest} *old.csv\n", encoding="utf-8")
    monkeypatch.setattr(cdm, "MANIFEST_DIRS", [d])
    monkeypatch.setattr(cdm, "REPO_ROOT", tmp_path)

    rc = cdm.regenerate_all(dry_run=False)
    assert rc == 0
    body = (d / "SHA256SUMS").read_text(encoding="utf-8")
    assert body == ""
    assert "old.csv" not in body
