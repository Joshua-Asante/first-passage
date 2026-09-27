"""Acceptance tests for scripts/check_handoff_brief_form.py (the `handoff-brief-form` gate).

Rule owner: docs/adr/2026-07-14-cc-cursor-surface-allocation.md §Decision, handoff contract
item 1 ("A handoff brief under `docs/briefs/**` passing `check_brief.py`"), and its
Addendum 2026-09-27, which records the unenforced item and the operator's exemption of four
files. Each test names the property it must violate to fail.
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GATE = REPO / "scripts" / "check_handoff_brief_form.py"
CHECK_BRIEF = REPO / "scripts" / "check_brief.py"
ADR = REPO / "docs" / "adr" / "2026-07-14-cc-cursor-surface-allocation.md"
WELL_FORMED = REPO / "docs" / "briefs" / "handoffs" / "2026-09-23-guard-s2-runs-hardening.md"


def _load():
    spec = importlib.util.spec_from_file_location("check_handoff_brief_form", GATE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


gate = _load()

# The shape every 2026-09-27 card had before the ruling: prose sections, no numbered
# §0/§0.5/§4/§5/§6/§10. `check_brief.py` reports it MALFORMED.
MALFORMED = """\
# Example card

**Status:** DISPATCH-READY.

## Routing

Local.

## Forbidden

- account access.
"""

AUTHORITY_BLOCK = """
```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
max_risk: medium
capabilities: [repository.read]
constraints: [no_main_write]
acceptance: [tests/scripts/test_x.py::test_y]
```
"""


def _tree(tmp_path: Path, files: dict[str, str]) -> Path:
    for rel, text in files.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def _run(root: Path, exempt=frozenset(), grandfathered=frozenset()):
    return gate.scan(root, exempt=exempt, grandfathered=grandfathered)


def test_well_formed_card_on_or_after_cutoff_passes(tmp_path):
    """Violated if a card `check_brief.py` reports well-formed is refused."""
    root = _tree(tmp_path, {
        "docs/briefs/handoffs/2026-09-28-example.md": WELL_FORMED.read_text(encoding="utf-8"),
    })
    result = _run(root)
    assert result.failures == []
    assert result.checked == 1


@pytest.mark.parametrize("name", ["2026-09-27-example.md", "2026-10-01-example.md"])
def test_malformed_card_on_or_after_cutoff_fails(tmp_path, name):
    """Violated if a malformed card dated on or after the cutoff passes the gate."""
    rel = f"docs/briefs/handoffs/{name}"
    root = _tree(tmp_path, {rel: MALFORMED})
    result = _run(root)
    assert [f.path for f in result.failures] == [rel]
    assert "RESULT: MALFORMED" in result.failures[0].report


def test_grandfathered_historical_card_is_not_checked(tmp_path):
    """Violated if the gate retrofits a historical card on the grandfathered list
    (item 7's precedent)."""
    root = _tree(tmp_path, {"docs/briefs/handoffs/2026-09-26-example.md": MALFORMED})
    result = _run(root, grandfathered=frozenset({"2026-09-26-example.md"}))
    assert result.failures == []
    assert result.checked == 0


def test_new_card_with_a_backdated_name_is_checked(tmp_path):
    """Violated if a new card escapes the gate by carrying a pre-cutoff date in its name
    (Codex P2 on #532): only listed historical cards are grandfathered."""
    rel = "docs/briefs/handoffs/2026-09-26-new.md"
    root = _tree(tmp_path, {rel: MALFORMED})
    result = _run(root, grandfathered=frozenset({"2026-09-26-other.md"}))
    assert [f.path for f in result.failures] == [rel]


def test_not_checked_outcome_fails(tmp_path):
    """Violated if a card that check_brief.py reports NOT CHECKED (exit 0) passes the gate
    (Codex P1 on #532): only RESULT: well-formed passes."""
    rel = "docs/briefs/handoffs/2026-09-28-example.md"
    root = _tree(tmp_path, {rel: MALFORMED.replace("**Status:**", "**Tier:** light\n**Status:**")})
    result = _run(root)
    assert [f.path for f in result.failures] == [rel]
    assert "NOT CHECKED" in result.failures[0].report


def test_partially_staged_card_fails(tmp_path):
    """Violated if a card whose staged copy differs from its working copy passes: the
    commit records the staged bytes, not the ones checked (Codex P2 on #532)."""
    rel = "docs/briefs/handoffs/2026-09-28-example.md"
    root = _tree(tmp_path, {rel: MALFORMED})
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", rel], check=True)
    (root / rel).write_text(WELL_FORMED.read_text(encoding="utf-8"), encoding="utf-8")
    result = _run(root)
    assert [f.path for f in result.failures] == [rel]
    assert "staged and unstaged" in result.failures[0].report
    subprocess.run(["git", "-C", str(root), "add", rel], check=True)
    assert _run(root).failures == []


def test_grandfathered_list_holds_only_historical_cards():
    """Violated if the list names a card dated on or after the cutoff, or grows past the
    74 historical cards on main when the gate landed."""
    names = gate.load_grandfathered()
    assert 0 < len(names) <= 74
    assert all(name < gate.CUTOFF for name in names)


def test_undated_card_is_checked_but_readme_is_not(tmp_path):
    """Violated if an undated name escapes the gate, or the directory README is gated."""
    root = _tree(tmp_path, {
        "docs/briefs/handoffs/example-card.md": MALFORMED,
        "docs/briefs/handoffs/README.md": MALFORMED,
    })
    result = _run(root)
    assert [f.path for f in result.failures] == ["docs/briefs/handoffs/example-card.md"]


def test_authority_block_card_is_checked_anywhere_under_briefs(tmp_path):
    """Violated if a worker card with an authority block escapes the gate by its
    directory or its date."""
    rel = "docs/briefs/programs/2026-01-01-example-card.md"
    root = _tree(tmp_path, {rel: MALFORMED + AUTHORITY_BLOCK})
    result = _run(root)
    assert [f.path for f in result.failures] == [rel]


def test_brief_without_block_outside_handoffs_is_not_checked(tmp_path):
    """Violated if the gate sweeps non-card briefs outside `docs/briefs/handoffs/`."""
    root = _tree(tmp_path, {"docs/briefs/programs/2026-10-01-state.md": MALFORMED})
    assert _run(root).checked == 0


def test_exempt_card_is_not_checked(tmp_path):
    """Violated if a file the ruling exempts is still refused."""
    rel = "docs/briefs/handoffs/2026-09-27-example.md"
    root = _tree(tmp_path, {rel: MALFORMED})
    result = _run(root, exempt=frozenset({rel}))
    assert result.failures == []
    assert result.exempted == 1


def test_missing_exempt_path_fails_closed(tmp_path):
    """Violated if an exemption naming no file passes silently: a stale exemption list
    is configuration drift, and a renamed exempt card must not keep its exemption."""
    rel = "docs/briefs/handoffs/2026-09-27-gone.md"
    root = _tree(tmp_path, {"docs/briefs/handoffs/README.md": "# Handoffs\n"})
    result = _run(root, exempt=frozenset({rel}))
    assert [f.path for f in result.failures] == [rel]
    assert "exempt path not found" in result.failures[0].report


def test_verdict_is_check_brief_cli_verdict(tmp_path):
    """Violated if the gate's pass/fail differs from `python scripts/check_brief.py <card>`
    for an in-scope card: the gate adds scope, never rules."""
    good = tmp_path / "docs/briefs/handoffs/2026-09-28-good.md"
    bad = tmp_path / "docs/briefs/handoffs/2026-09-28-bad.md"
    _tree(tmp_path, {
        "docs/briefs/handoffs/2026-09-28-good.md": WELL_FORMED.read_text(encoding="utf-8"),
        "docs/briefs/handoffs/2026-09-28-bad.md": MALFORMED,
    })
    failing = {f.path for f in _run(tmp_path).failures}
    for card in (good, bad):
        cli = subprocess.run([sys.executable, str(CHECK_BRIEF), str(card)],
                             capture_output=True, text=True, check=False)
        rel = card.relative_to(tmp_path).as_posix()
        assert (cli.returncode != 0) == (rel in failing)


def test_exempt_set_is_exactly_the_rulings_exempt_rows():
    """Violated if the script's exemptions drift from the operator's dated ruling
    (ADR Addendum 2026-09-27), in either direction."""
    text = ADR.read_text(encoding="utf-8")
    start = text.index('<a id="addendum-2026-09-27"></a>')
    end = text.index("\n## ", text.index("\n## ", start) + 1)
    section = text[start:end]
    rows = re.findall(r"^\| `([^`]+\.md)` \|.*\| \*\*Exempt\b[^|]*\|\s*$", section, re.M)
    assert rows, "the ruling's table was not found"
    assert gate.EXEMPT == frozenset(f"docs/briefs/handoffs/{name}" for name in rows)


def test_repository_tree_is_clean():
    """Violated if a card in scope on this tree fails, or an exemption is stale."""
    proc = subprocess.run([sys.executable, str(GATE)], cwd=REPO,
                          capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 failing" in proc.stdout
