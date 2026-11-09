"""Tests for scripts/check_order.py (The Order's mechanical gates)."""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import subprocess

import pytest

from scripts import check_order as co

D = dt.date.fromisoformat
REG_BYTES = b"H: one falsifiable sentence\n"
REG_SHA = hashlib.sha256(REG_BYTES).hexdigest()


def state(**kw):
    s = copy.deepcopy(co.EMPTY_STATE)
    s.update(kw)
    return s


def reg(started=None, sha=REG_SHA, rid="R1", path="research/R1.md"):
    return {"id": rid, "path": path, "sha256": sha, "started": started}


Q = {"start": "2026-12-01", "until": "2026-12-15"}


# ---------------------------------------------------------------- schema

def test_committed_state_file_is_valid():
    committed = json.loads((co.REPO_ROOT / co.STATE_PATH).read_text(encoding="utf-8"))
    assert co.validate_schema(committed) == []


@pytest.mark.parametrize("bad, fragment", [
    ({"mode": "solo"}, "mode"),
    ({"step": "build"}, "step"),
    ({"quarantine": {"start": "2026-12-01", "until": "2026-12-10"}}, "14 days"),
    ({"registrations": [reg(), reg()]}, "duplicate"),
    ({"registrations": [{"id": "R1"}]}, "must have"),
    ({"contract": {"path": "c.md"}}, "contract"),
])
def test_schema_rejects(bad, fragment):
    assert any(fragment in e for e in co.validate_schema(state(**bad)))


# ---------------------------------------------------------------- hashes

def test_hash_match_and_mismatch():
    s = state(registrations=[reg()])
    assert co.check_hashes(s, lambda p: REG_BYTES) == []
    assert "does not match" in co.check_hashes(s, lambda p: b"edited")[0]
    assert "does not exist" in co.check_hashes(s, lambda p: None)[0]


# ---------------------------------------------------------------- freeze

def test_unstarted_registration_may_change():
    base = state(registrations=[reg()])
    head = state(registrations=[reg(sha="0" * 64)])
    assert co.check_transition(base, head, D("2026-11-10")) == []


def test_started_registration_is_frozen():
    base = state(registrations=[reg(started="2026-11-10")])
    for head in (state(registrations=[reg(started="2026-11-10", sha="0" * 64)]),
                 state(registrations=[reg(started=None)]),
                 state(registrations=[])):
        assert co.check_transition(base, head, D("2026-11-11")), head


def test_starting_a_registration_is_allowed():
    base = state(registrations=[reg()])
    head = state(registrations=[reg(started="2026-11-10")])
    assert co.check_transition(base, head, D("2026-11-10")) == []


# ---------------------------------------------------------------- quarantine

def test_quarantine_window():
    s = state(quarantine=Q)
    assert not co.quarantine_active(s, D("2026-11-30"))
    assert co.quarantine_active(s, D("2026-12-01"))
    assert co.quarantine_active(s, D("2026-12-15"))
    assert not co.quarantine_active(s, D("2026-12-16"))


@pytest.mark.parametrize("head_q", [None, {"start": "2026-12-01", "until": "2026-12-10"},
                                    {"start": "2026-11-20", "until": "2026-12-15"}])
def test_active_quarantine_cannot_be_removed_shortened_or_moved(head_q):
    errs = co.check_transition(state(quarantine=Q), state(quarantine=head_q), D("2026-12-05"))
    assert any("may not be removed" in e for e in errs)


def test_quarantine_may_be_extended_and_lapses():
    longer = {"start": "2026-12-01", "until": "2026-12-31"}
    assert co.check_transition(state(quarantine=Q), state(quarantine=longer), D("2026-12-05")) == []
    assert co.check_transition(state(quarantine=Q), state(quarantine=None), D("2026-12-16")) == []


def test_no_new_registration_or_contract_change_in_quarantine():
    base = state(quarantine=Q)
    errs = co.check_transition(base, state(quarantine=Q, registrations=[reg()]), D("2026-12-05"))
    assert any("added, changed or started" in e for e in errs)
    contract = {"path": "c.md", "sha256": "0" * 64, "end_date": "2027-01-31"}
    errs = co.check_transition(base, state(quarantine=Q, contract=contract), D("2026-12-05"))
    assert any("contract may not change" in e for e in errs)


def test_commit_subjects_in_quarantine():
    base = state(quarantine=Q)
    assert co.check_commit_subjects(["closure: RESULTS"], base, D("2026-12-05")) == []
    assert co.check_commit_subjects(["feat: successor"], base, D("2026-12-05"))
    assert co.check_commit_subjects(["feat: anything"], base, D("2026-12-16")) == []


# ---------------------------------------------------------------- hooks

def test_session_start_reports_state():
    text = co.status_text(state(quarantine=Q, registrations=[reg(started="2026-11-10")]), D("2026-12-05"))
    assert "QUARANTINE until 2026-12-15" in text
    assert "FROZEN since 2026-11-10" in text
    assert "Contract: none" in text


def test_pre_tool_use_denies_frozen_registration(tmp_path, monkeypatch, capsys):
    (tmp_path / "docs/framework").mkdir(parents=True)
    (tmp_path / co.STATE_PATH).write_text(json.dumps(state(registrations=[reg(started="2026-11-10")])))
    monkeypatch.setattr(co, "REPO_ROOT", tmp_path)
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    co.run_pre_tool_use(json.dumps({"tool_input": {"file_path": str(tmp_path / "research/R1.md")}}))
    assert json.loads(capsys.readouterr().out)["hookSpecificOutput"]["permissionDecision"] == "deny"
    co.run_pre_tool_use(json.dumps({"tool_input": {"file_path": "research/other.md"}}))
    assert capsys.readouterr().out == ""


# ---------------------------------------------------------------- gate end to end

def _git(repo, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
                   cwd=repo, check=True, capture_output=True)


def test_gate_on_pull_request_range(tmp_path, monkeypatch):
    repo = tmp_path
    _git(repo, "init", "-q", "-b", "main")
    (repo / "docs/framework").mkdir(parents=True)
    (repo / "research").mkdir()
    (repo / "research/R1.md").write_bytes(REG_BYTES)
    (repo / co.STATE_PATH).write_text(json.dumps(state(registrations=[reg(started="2026-11-10")])))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "register R1")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    monkeypatch.setattr(co, "REPO_ROOT", repo)
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request")
    monkeypatch.setenv("GITHUB_BASE_REF", "main")
    monkeypatch.setenv("ORDER_TODAY", "2026-11-12")
    assert co.run_gate() == 0

    (repo / "research/R1.md").write_bytes(b"H: moved the threshold\n")
    _git(repo, "commit", "-qam", "tweak R1")
    assert co.run_gate() == 1


# ---------------------------------------------------------------- Codex round 1 regressions

def test_compact_dates_rejected_and_shortening_compares_dates():
    assert any("YYYY-MM-DD" in e for e in co.validate_schema(
        state(quarantine={"start": "2026-12-01", "until": "20261231"})))
    base = state(quarantine={"start": "2026-12-01", "until": "2026-12-31"})
    head = state(quarantine={"start": "2026-12-01", "until": "20261215"})
    assert co.check_transition(base, head, D("2026-12-05"))


def _repo(tmp_path, monkeypatch, registrations, quarantine=None):
    repo = tmp_path
    _git(repo, "init", "-q", "-b", "main")
    (repo / "docs/framework").mkdir(parents=True)
    (repo / "research").mkdir()
    (repo / "research/R1.md").write_bytes(REG_BYTES)
    (repo / co.STATE_PATH).write_text(json.dumps(state(registrations=registrations, quarantine=quarantine), indent=2))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    _git(repo, "checkout", "-qb", "pr")
    monkeypatch.setattr(co, "REPO_ROOT", repo)
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request")
    monkeypatch.setenv("GITHUB_BASE_REF", "main")
    monkeypatch.setenv("ORDER_TODAY", "2026-12-05")
    return repo


def _synthetic_checkout(repo, monkeypatch, tmp_path):
    """What actions/checkout gives a pull_request run: a merge of the PR head into base."""
    head = subprocess.run(["git", "rev-parse", "pr"], cwd=repo, capture_output=True, text=True).stdout.strip()
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"head": {"sha": head}}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    _git(repo, "checkout", "-q", "--detach", "main")
    _git(repo, "merge", "-q", "--no-ff", "-m", "Merge pr into main", head)


def _write_state(repo, **kw):
    (repo / co.STATE_PATH).write_text(json.dumps(state(**kw), indent=2))


def test_start_then_rewrite_within_one_pr_fails(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [reg()])
    _write_state(repo, registrations=[reg(started="2026-12-05")])
    _git(repo, "commit", "-qam", "start R1")
    assert co.run_gate() == 0
    new = b"H: moved the threshold\n"
    (repo / "research/R1.md").write_bytes(new)
    _write_state(repo, registrations=[reg(started="2026-12-05", sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "commit", "-qam", "rewrite R1")
    assert co.run_gate() == 1


def test_symlinked_registration_rejected(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [])
    (repo / "research/R2.md").symlink_to("R1.md")
    link_sha = hashlib.sha256(b"R1.md").hexdigest()
    _write_state(repo, registrations=[reg(rid="R2", path="research/R2.md", sha=link_sha)])
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "register via symlink")
    assert co.run_gate() == 1


def test_authored_merge_in_quarantine_needs_closure_prefix(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [], quarantine=Q)
    _git(repo, "checkout", "-qb", "side")
    (repo / "research/notes.md").write_text("results\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "closure: record results")
    _git(repo, "checkout", "-q", "pr")
    (repo / "research/impl.py").write_text("x = 1\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "closure: tidy")
    _git(repo, "merge", "-q", "--no-ff", "-m", "feat: continue programme", "side")
    _synthetic_checkout(repo, monkeypatch, tmp_path)
    assert co.run_gate() == 1


def test_synthetic_pr_merge_is_exempt(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [], quarantine=Q)
    (repo / "research/notes.md").write_text("results\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "closure: record results")
    _synthetic_checkout(repo, monkeypatch, tmp_path)
    assert co.run_gate() == 0


# ---------------------------------------------------------------- Codex round 2 regressions

def test_target_branch_freeze_after_fork_binds_the_merge(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [reg()])
    new = b"H: moved the threshold\n"
    (repo / "research/R1.md").write_bytes(new)
    _write_state(repo, registrations=[reg(sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "commit", "-qam", "edit unstarted R1")
    _git(repo, "checkout", "-q", "main")
    _write_state(repo, registrations=[reg(started="2026-12-04")])
    _git(repo, "commit", "-qam", "start R1 on main")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    head_sha = subprocess.run(["git", "rev-parse", "pr"], cwd=repo, capture_output=True, text=True).stdout.strip()
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"head": {"sha": head_sha}}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    _git(repo, "checkout", "-q", "--detach", "main")
    # Adjacent JSON lines conflict here; Codex's case merged cleanly. Record the same
    # merged result: main's start date with the PR's rewritten file and hash.
    subprocess.run(["git", "merge", "--no-ff", "--no-commit", head_sha], cwd=repo, capture_output=True)
    _write_state(repo, registrations=[reg(started="2026-12-04", sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "Merge pr into main")
    assert co.run_gate() == 1


def test_invalid_intermediate_state_is_rejected(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [])
    _write_state(repo, registrations=[reg(started="2026-12-05")])
    _git(repo, "commit", "-qam", "start R1")
    new = b"H: moved the threshold\n"
    (repo / "research/R1.md").write_bytes(new)
    _write_state(repo, version=2, registrations=[reg(started="2026-12-05", sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "commit", "-qam", "rewrite under an invalid state")
    _write_state(repo, registrations=[reg(started="2026-12-05", sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "commit", "-qam", "restore version")
    assert co.run_gate() == 1


def test_unstarted_registration_cannot_be_repurposed_in_quarantine():
    base = state(quarantine=Q, registrations=[reg()])
    head = state(quarantine=Q, registrations=[reg(path="research/successor.md", sha="0" * 64, started="2026-12-05")])
    errs = co.check_transition(base, head, D("2026-12-05"))
    assert any("added, changed or started" in e for e in errs)


# ---------------------------------------------------------------- Codex round 3 regression

def test_pr_head_freeze_binds_a_merge_with_rewritten_main(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [reg()])
    _write_state(repo, registrations=[reg(started="2026-12-05")])
    _git(repo, "commit", "-qam", "start R1")
    _git(repo, "checkout", "-q", "main")
    new = b"H: moved the threshold\n"
    (repo / "research/R1.md").write_bytes(new)
    _write_state(repo, registrations=[reg(sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "commit", "-qam", "rewrite unstarted R1 on main")
    _git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
    head_sha = subprocess.run(["git", "rev-parse", "pr"], cwd=repo, capture_output=True, text=True).stdout.strip()
    event = tmp_path / "event.json"
    event.write_text(json.dumps({"pull_request": {"head": {"sha": head_sha}}}))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event))
    _git(repo, "checkout", "-q", "--detach", "main")
    subprocess.run(["git", "merge", "--no-ff", "--no-commit", head_sha], cwd=repo, capture_output=True)
    # The merge Codex described: the PR's start date with main's rewritten document and hash.
    _write_state(repo, registrations=[reg(started="2026-12-05", sha=hashlib.sha256(new).hexdigest())])
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "Merge pr into main")
    assert co.run_gate() == 1


# ---------------------------------------------------------------- Codex round 4 regression

def test_symlinked_state_file_is_rejected(tmp_path, monkeypatch):
    repo = _repo(tmp_path, monkeypatch, [])
    # A target file name that is itself valid empty-state JSON would parse as the link's blob.
    name = json.dumps(co.EMPTY_STATE, separators=(",", ":"))
    real = repo / "docs/framework/real-state.json"
    real.write_text(json.dumps(state(registrations=[reg(started="2026-12-05")])))
    (repo / co.STATE_PATH).unlink()
    try:
        (repo / co.STATE_PATH).symlink_to(name)
    except OSError:
        pytest.skip("cannot create a symlink with that name here")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "link the state file")
    assert co.run_gate() == 1
    with pytest.raises(co.StateError):
        co._working_state()
