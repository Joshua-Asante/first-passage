"""Acceptance tests for scripts/check_handoff_authority.py.

Rule owner: docs/adr/2026-07-14-cc-cursor-surface-allocation.md §Decision, "Action
classes and the authority block" (2026-09-25 revision). Each test names the property it
must violate to fail; the registry under test is the committed scripts/seat_authority.yml,
so a registry edit that loosens a rule turns one of these red.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts" / "check_handoff_authority.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_handoff_authority", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod  # dataclasses resolve their module by name
    spec.loader.exec_module(mod)
    return mod


cha = _load()
REG = cha.load_registry()

WORKER_OK = """\
seat: worker
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
constraints: [no_main_write]
acceptance: [tests/scripts/test_x.py::test_y]
"""


def _card(tmp_path: Path, body: str, name: str = "card.md", prose: str = "# Card\n") -> Path:
    path = tmp_path / name
    path.write_text(f"{prose}\n```yaml authority\n{body}```\n", encoding="utf-8")
    return path


def _errs(path: Path, root: Path) -> list[str]:
    return cha.check_card(path, REG, root=root)


def test_clean_worker_card_passes(tmp_path):
    # Fails if a well-formed worker card, naming its parent, is rejected (over-blocks).
    _card(tmp_path, "seat: coordinator\nmax_risk: medium\n"
          "capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]\n"
          "constraints: [no_main_write]\n", name="umbrella.md")
    body = "parent: umbrella.md\n" + WORKER_OK
    assert _errs(_card(tmp_path, body), tmp_path) == []


def test_worker_card_must_name_its_parent(tmp_path):
    # Fails if a worker block that omits `parent` skips A7 and keeps the whole seat
    # grant (item 7 requires the block to name its parent; Codex #503 threads Dr5 / TGh).
    assert any(e.startswith("A7") and "parent" in e
               for e in _errs(_card(tmp_path, WORKER_OK), tmp_path))


def test_blockless_parent_bounds_only_the_seat(tmp_path):
    # Fails if a worker whose parent carries no authority block (a historical umbrella;
    # the ADR does not retrofit them) is refused, or if naming such a parent lifts the
    # seat checks. A block-less parent narrows nothing beyond the seat (verifier round on
    # fd126c3; requiring every parent to carry a block would be a new rule).
    (tmp_path / "umbrella.md").write_text("# Historical umbrella\n", encoding="utf-8")
    assert _errs(_card(tmp_path, "parent: umbrella.md\n" + WORKER_OK), tmp_path) == []
    wide = ("parent: umbrella.md\n" + WORKER_OK).replace("pr.open]", "pr.open, pr.review]")
    assert any(e.startswith("A5")
               for e in _errs(_card(tmp_path, wide, name="wide.md"), tmp_path))


@pytest.mark.parametrize("names", ['[""]', '["  "]', '[tests/x.py::test_y, ""]'])
def test_acceptance_names_must_be_nonempty(tmp_path, names):
    # Fails if `acceptance: [""]` stands in for named tests (Codex #503 thread TGw).
    body = WORKER_OK.replace("[tests/scripts/test_x.py::test_y]", names)
    assert any(e.startswith("A6") for e in _errs(_card(tmp_path, body), tmp_path))


def test_registry_rejects_unknown_seat_ceiling(tmp_path):
    # Fails if a mistyped seat `max_risk` loads silently and crashes the first card for
    # that seat instead of failing the registry gate (Codex #503 thread DsN).
    text = (REPO / "scripts" / "seat_authority.yml").read_text(encoding="utf-8")
    bad = tmp_path / "seat_authority.yml"
    bad.write_text(text.replace("  executive:\n    max_risk: medium",
                                "  executive:\n    max_risk: meduim")
                   .replace("  executive:\r\n    max_risk: medium",
                            "  executive:\r\n    max_risk: meduim"), encoding="utf-8")
    assert "meduim" in bad.read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="executive"):
        cha.load_registry(bad)


def test_card_without_block_is_not_checked(tmp_path):
    # Fails if historical cards with no block are forced to retrofit.
    path = tmp_path / "old.md"
    path.write_text("# Old card\n```yaml\nseat: nobody\n```\n", encoding="utf-8")
    assert _errs(path, tmp_path) == []


@pytest.mark.parametrize("cap", sorted(REG.forbidden))
def test_forbidden_capability_is_ungrantable(tmp_path, cap):
    # Fails if any forbidden capability (trade.submit, pr.auto_merge, ...) can be granted.
    body = WORKER_OK.replace("pr.open]", f"pr.open, {cap}]")
    assert any(e.startswith("A2") for e in _errs(_card(tmp_path, body), tmp_path))


def test_hook_denials_are_registered_forbidden():
    # Fails if the hook denies an act the registry does not list as forbidden, or asks
    # on one the registry does not class as an operator act (the registry is the one
    # canonical list; the hook must not carry its own). Derived from the hook's own
    # decision table, which every hit it emits is looked up in.
    import scripts.guard_operator_acts as hook
    assert set(hook.MESSAGES) == set(hook.DECISION)
    denied = {cap for cap, dec in hook.DECISION.items() if dec == "deny"}
    asked = {cap for cap, dec in hook.DECISION.items() if dec == "ask"}
    assert denied - {"pr.merge_unpinned"} <= REG.forbidden
    assert all(REG.capabilities.get(cap) == "high" for cap in asked)
    assert {cap for _, cap in hook._FALLBACK} <= set(hook.DECISION)


def test_trade_submit_is_in_the_forbidden_set():
    # Fails if the registry ever demotes trade placement to an approvable class.
    assert "trade.submit" in REG.forbidden
    assert "trade.submit" not in REG.capabilities


@pytest.mark.parametrize("cap", sorted(c for c, r in REG.capabilities.items() if r == "high"))
def test_operator_act_is_never_delegated(tmp_path, cap):
    # Fails if a card can delegate an operator act (merge, ratify, spend, deploy, arm),
    # even to the coordinator with max_risk high.
    body = (f"seat: coordinator\nmax_risk: high\ncapabilities: [repository.read, {cap}]\n"
            "constraints: []\n")
    errs = _errs(_card(tmp_path, body), tmp_path)
    assert any(e.startswith("A3") for e in errs)
    assert any(e.startswith("A4") and "ceiling" in e for e in errs)


def test_no_agent_seat_is_granted_a_high_capability():
    # Fails if the registry lists an operator act as grantable to any agent seat.
    high = {c for c, r in REG.capabilities.items() if r == "high"}
    for seat, (max_risk, grant) in REG.seats.items():
        assert max_risk != "high", seat
        assert not grant & high, seat


def test_capability_above_card_risk_is_rejected(tmp_path):
    # Fails if a low-risk card may carry a medium capability.
    body = WORKER_OK.replace("max_risk: medium", "max_risk: low")
    assert any(e.startswith("A4") for e in _errs(_card(tmp_path, body), tmp_path))


def test_capability_outside_seat_grant_is_rejected(tmp_path):
    # Fails if a worker can be granted governance authoring (routing test 1).
    body = WORKER_OK.replace("pr.open]", "pr.open, governance.author]")
    assert any(e.startswith("A5") for e in _errs(_card(tmp_path, body), tmp_path))


def test_worker_card_needs_named_acceptance_tests(tmp_path):
    # Fails if a worker card may omit its acceptance tests (handoff contract item 5).
    body = "\n".join(l for l in WORKER_OK.splitlines() if not l.startswith("acceptance")) + "\n"
    assert any(e.startswith("A6") for e in _errs(_card(tmp_path, body), tmp_path))


def _parent(tmp_path: Path) -> None:
    _card(tmp_path, "seat: coordinator\nmax_risk: medium\n"
          "capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]\n"
          "constraints: [no_main_write, reserved_files_untouched]\n", name="umbrella.md")


def test_child_within_parent_passes(tmp_path):
    # Fails if a correctly narrowed child is rejected.
    _parent(tmp_path)
    body = ("parent: umbrella.md\n" + WORKER_OK).replace(
        "[no_main_write]", "[no_main_write, reserved_files_untouched, extra]")
    assert _errs(_card(tmp_path, body), tmp_path) == []


def test_child_cannot_widen_parent(tmp_path):
    # Fails if a child may hold a capability its parent never had.
    _parent(tmp_path)
    body = ("parent: umbrella.md\n" + WORKER_OK).replace(
        "pr.open]", "pr.open, ci.dispatch]").replace(
        "[no_main_write]", "[no_main_write, reserved_files_untouched]")
    assert any("A7 widens" in e for e in _errs(_card(tmp_path, body), tmp_path))


def test_child_cannot_drop_parent_constraint(tmp_path):
    # Fails if an inherited constraint can be silently removed.
    _parent(tmp_path)
    body = "parent: umbrella.md\n" + WORKER_OK
    assert any("A7 drops" in e for e in _errs(_card(tmp_path, body), tmp_path))


def test_missing_parent_is_rejected(tmp_path):
    # Fails if a card may cite a parent that does not exist.
    body = "parent: nowhere.md\n" + WORKER_OK
    assert any("does not exist" in e for e in _errs(_card(tmp_path, body), tmp_path))


def test_two_blocks_are_rejected(tmp_path):
    # Fails if a card can carry two competing grants.
    path = _card(tmp_path, WORKER_OK)
    path.write_text(path.read_text() + f"\n```yaml authority\n{WORKER_OK}```\n")
    assert any("more than one" in e for e in _errs(path, tmp_path))


def test_cli_scans_repo_clean():
    # Fails if a committed card in docs/briefs/ violates its own authority block.
    out = subprocess.run([sys.executable, str(CHECKER), "--all"], cwd=REPO,
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr


def test_parent_outside_repository_is_rejected(tmp_path):
    # Fails if a child can cite a parent outside the repository, whose grant is never
    # checked (Astra finding 3, PR #503 at 72c435c).
    repo = tmp_path / "repo"
    repo.mkdir()
    _card(tmp_path, "seat: coordinator\nmax_risk: high\ncapabilities: [pr.merge]\n",
          name="outside.md")
    body = "parent: ../outside.md\n" + WORKER_OK
    assert any("outside the repository" in e for e in _errs(_card(repo, body), repo))


def test_parent_violations_propagate(tmp_path):
    # Fails if a child passes while its in-repo parent grants an operator act.
    _card(tmp_path, "seat: coordinator\nmax_risk: medium\n"
          "capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open,"
          " pr.merge]\nconstraints: [no_main_write]\n", name="bad_parent.md")
    body = "parent: bad_parent.md\n" + WORKER_OK
    errs = _errs(_card(tmp_path, body), tmp_path)
    assert any(e.startswith("A7 parent bad_parent.md: A3") for e in errs)


def test_mutual_parents_are_rejected(tmp_path):
    # Fails if two cards naming each other as parents both pass
    # (Astra finding 3, PR #503 at 72c435c).
    a = _card(tmp_path, "parent: b.md\n" + WORKER_OK, name="a.md")
    b = _card(tmp_path, "parent: a.md\n" + WORKER_OK, name="b.md")
    assert any("loops" in e for e in _errs(a, tmp_path))
    assert any("loops" in e for e in _errs(b, tmp_path))
