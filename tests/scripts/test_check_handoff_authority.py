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


# --- 2026-09-25 babysit repairs (Codex review of #503 at a230f8b, comment 4109427040) ---

FENCE = "`" * 3
DELEGATES_ARM = WORKER_OK.replace("pr.open]", "pr.open, rail.arm]")


def _indented(body: str, pad: str, close: str | None = None) -> str:
    """A card whose fence (and body) is indented by `pad`; the closing fence by `close`."""
    lines = "".join(f"{pad}{line}\n" for line in body.splitlines())
    closer = pad if close is None else close
    return f"# Card\n\n{pad}{FENCE}yaml authority\n{lines}{closer}{FENCE}\n"


@pytest.mark.parametrize("pad", [" ", "  ", "   "])
def test_fence_indented_up_to_three_spaces_is_checked(tmp_path, pad):
    # Fails if a CommonMark fence indented by 1-3 spaces is read as no block, so a card
    # that delegates an operator act is skipped as historical (Codex #503, 4109427040).
    (tmp_path / "umbrella.md").write_text("# Umbrella\n", encoding="utf-8")
    path = tmp_path / "card.md"
    path.write_text(_indented("parent: umbrella.md\n" + DELEGATES_ARM, pad), encoding="utf-8")
    assert any(e.startswith("A3") for e in _errs(path, tmp_path))
    clean = tmp_path / "clean.md"
    clean.write_text(_indented("parent: umbrella.md\n" + WORKER_OK, pad), encoding="utf-8")
    assert _errs(clean, tmp_path) == []
    assert len(cha.extract_blocks(clean.read_text(encoding="utf-8"))) == 1


def test_fence_indented_four_spaces_is_not_a_block_and_fails_closed(tmp_path):
    # Fails if a four-space-indented fence (CommonMark: an indented code block, not a
    # fence) is taken for an authority block, or if it is let through as no block at all
    # instead of being refused (Codex #503, 4109578926: fail closed).
    path = tmp_path / "card.md"
    path.write_text(_indented(DELEGATES_ARM, "    "), encoding="utf-8")
    assert cha.extract_blocks(path.read_text(encoding="utf-8")) == []
    assert _errs(path, tmp_path) == [
        "A1 authority block must be a top-level fence (found inside a container at line 3)"]


@pytest.mark.parametrize("close", ["", " ", "   "])
def test_closing_fence_may_be_indented_up_to_three_spaces(tmp_path, close):
    # Fails if an indented closing fence is not read as the close, so the fence line
    # lands in the YAML and a clean card is refused.
    (tmp_path / "umbrella.md").write_text("# Umbrella\n", encoding="utf-8")
    path = tmp_path / "card.md"
    path.write_text(_indented("parent: umbrella.md\n" + WORKER_OK, "", close=close),
                    encoding="utf-8")
    assert _errs(path, tmp_path) == []


def test_fence_line_with_an_info_string_does_not_close(tmp_path):
    # Fails if a fence line carrying an info string is read as the close (CommonMark: a
    # closing fence has nothing after it), so the rest of the block goes unchecked.
    path = tmp_path / "card.md"
    path.write_text(f"{FENCE}yaml authority\nseat: worker\n{FENCE}text\n"
                    f"capabilities: [rail.arm]\n{FENCE}\n", encoding="utf-8")
    assert cha.extract_blocks(path.read_text(encoding="utf-8")) == [
        f"seat: worker\n{FENCE}text\ncapabilities: [rail.arm]"]
    assert any(e.startswith("A1") for e in _errs(path, tmp_path))


# --- 2026-09-25 babysit repairs (Codex review of #503 at a80f819, comment 4109578926) ---

CONTAINED = "A1 authority block must be a top-level fence (found inside a container at line"


def _contained(prefix: str, fence: str = FENCE, cont: str | None = None) -> str:
    """A card whose authority fence sits behind a container `prefix` (continuation lines
    behind `cont`, default the same prefix)."""
    rest = prefix if cont is None else cont
    lines = "".join(f"{rest}{line}\n" for line in DELEGATES_ARM.splitlines())
    return f"# Card\n\n{prefix}{fence}yaml authority\n{lines}{rest}{fence}\n"


@pytest.mark.parametrize("prefix,cont", [
    ("> ", None), (">", None), ("- ", "  "), ("* ", "  "), ("+ ", "  "), ("1. ", "   "),
    ("1) ", "   "), ("> - ", ">   "), ("- > ", "  > "), ("  - ", "    "), ("> > ", None),
    ("    ", None), ("\t", None), ("      ", None),
])
def test_authority_fence_inside_a_container_is_refused(tmp_path, prefix, cont):
    # Fails if an authority fence inside a blockquote or list item (or indented 4+ spaces)
    # is read as no block, so a card delegating an operator act gets the historical
    # exemption (Codex #503, 4109578926).
    for fence in (FENCE, "~~~"):
        path = tmp_path / "card.md"
        path.write_text(_contained(prefix, fence, cont), encoding="utf-8")
        errs = _errs(path, tmp_path)
        assert errs == [f"{CONTAINED} 3)"], (prefix, fence, errs)


def test_contained_authority_fence_beside_a_top_level_block_is_refused(tmp_path):
    # Fails if a second, contained authority fence hides behind a clean top-level block.
    (tmp_path / "umbrella.md").write_text("# Umbrella\n", encoding="utf-8")
    path = tmp_path / "card.md"
    path.write_text(f"# Card\n\n{FENCE}yaml authority\nparent: umbrella.md\n{WORKER_OK}"
                    f"{FENCE}\n\n> {FENCE}yaml authority\n> seat: worker\n> {FENCE}\n",
                    encoding="utf-8")
    assert f"{CONTAINED} 12)" in _errs(path, tmp_path)


def test_card_without_an_authority_looking_fence_stays_exempt(tmp_path):
    # Fails if the container rule over-reaches to cards whose fences are not authority
    # fences (a quoted yaml fence, an authority fence named in prose).
    path = tmp_path / "card.md"
    path.write_text(f"# Card\n\n> {FENCE}yaml\n> seat: worker\n> {FENCE}\n\n"
                    f"Write a `{FENCE}yaml authority` block.\n- {FENCE}text\n", encoding="utf-8")
    assert _errs(path, tmp_path) == []
