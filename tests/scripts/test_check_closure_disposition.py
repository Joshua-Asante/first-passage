"""Adversarial tests for scripts/check_closure_disposition.py (pre-commit gate 14).

Discipline guards need adversarial tests — a checker that passes on an empty
directory or a vacuous fixture is assurance theater. Every REQUIRED failure
mode below has a fixture that must FAIL, and the compliant fixture must PASS.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_SPEC = importlib.util.spec_from_file_location(
    "check_closure_disposition", REPO / "scripts" / "check_closure_disposition.py"
)
ccd = importlib.util.module_from_spec(_SPEC)
# Dataclass (and similar) looks up sys.modules[cls.__module__] at class-body
# time — register before exec_module or frozen dataclasses crash on 3.14.
sys.modules[_SPEC.name] = ccd
_SPEC.loader.exec_module(ccd)


def _load_checker(module_name: str):
    spec = importlib.util.spec_from_file_location(
        module_name, REPO / "scripts" / "check_closure_disposition.py"
    )
    checker = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = checker
    spec.loader.exec_module(checker)
    return checker


COMPLIANT = """# Q-TEST-1 — CLOSURE: `FALSIFIED` (fixture)

**Verdict:** `FALSIFIED`

## 1. Verdict (§6 asserted against actual numbers)

Numbers here.

## Iterate — loop exit

- **Verdict used:** FALSIFIED
- **Model update:** the prior framing assumed X; the panel showed Y.
- **Next:** STOP
- **Routing:** STOP — mechanism dead at every admissible k.
- **Entry packet:** n/a
- **Stop rule / re-proposal bar:** new mechanism evidence, not new parameters.
- **Board write:** none — STOP, nothing owed
- **Registry:** n/a — fixture / not a strategy-grounds kill
"""

MISSING_BLOCK = """# Q-TEST-2 — CLOSURE: `RESOLVED` (fixture)

**Verdict:** `RESOLVED`

## Verdict

Numbers here; ends with no forward disposition at all.
"""

UNFILLED_PLACEHOLDER = """# Q-TEST-3 — CLOSURE: `AMBIGUOUS` (fixture)

## Iterate — loop exit

- **Next:** INTEGRATE | ITERATE | STOP
- **Board write:** none — STOP, nothing owed
"""

MISSING_BOARD_WRITE = """# Q-TEST-4 — CLOSURE: `AMBIGUOUS` (fixture)

## Iterate — loop exit

- **Model update:** framing survived.
- **Next:** ITERATE
- **Entry packet:** carry the verified $3.58 number; no a-fortiori re-opens.
"""

ALL_IN_FENCE = """# Q-TEST-7 — CLOSURE: `RESOLVED` (fixture)

For reference, the template we should have used:

```markdown
## Iterate — loop exit

- **Next:** STOP
- **Board write:** none — STOP, nothing owed
```

But no real block exists.
"""

PROSE_NEXT_ONLY = """# Q-TEST-8 — CLOSURE: `RESOLVED` (fixture)

## Iterate history of this question

Next steps: ITERATE on the sizing question when data lands.
Board write pending.
"""

DECOY_THEN_PLACEHOLDER = """# Q-TEST-9 — CLOSURE: `AMBIGUOUS` (fixture)

## Verdict

Next: STOP chasing this — see below.

## Iterate — loop exit

- **Next:** INTEGRATE | ITERATE | STOP
- **Board write:** none — STOP, nothing owed
"""

PROSE_SECOND_TOKEN = """# Q-TEST-10 — CLOSURE: `FALSIFIED` (fixture)

## Iterate — loop exit

- **Model update:** the mechanism is dead at every admissible k.
- **Next:** STOP — do not ITERATE without new mechanism evidence.
- **Board write:** none — STOP, nothing owed
"""

HYPHENATED_BOARD = """# Q-TEST-11 — CLOSURE: `RESOLVED` (fixture)

## Iterate — loop exit

- **Next:** INTEGRATE
- **Board-write:** `- **X** — done. [owner](docs/x.md)` (STATE row added)
"""

DEFECTS = {
    "heading": ("## Iterate — loop exit", "## Exit", "no 'Iterate' heading"),
    "next": ("- **Next:** STOP\n", "", "no 'Next:'"),
    "board": ("- **Board write:** none — STOP, nothing owed\n", "", "Board write"),
    "registry": (
        "- **Registry:** n/a — fixture / not a strategy-grounds kill\n",
        "",
        "closure lacks a Registry line",
    ),
}

FORMER_ITERATE_OWNER = "2026-08-04-iterate-closure-exit-mandatory.md"
FORMER_COVERAGE_OWNER = "2026-08-12-closure-disposition-coverage-hard.md"


def _write(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


# ── scan_file: the four fixture verdicts ───────────────────────

def test_compliant_closure_passes(tmp_path):
    assert ccd.scan_file(_write(tmp_path, "Q-TEST-1-closure-falsified.md", COMPLIANT)) is None


def test_missing_block_fails(tmp_path):
    msg = ccd.scan_file(_write(tmp_path, "Q-TEST-2-closure-resolved.md", MISSING_BLOCK))
    assert msg is not None
    assert "no 'Iterate' heading" in msg
    assert "Next:" in msg
    assert "Board write" in msg


def test_unfilled_placeholder_fails(tmp_path):
    msg = ccd.scan_file(_write(tmp_path, "Q-TEST-3-closure-ambiguous.md", UNFILLED_PLACEHOLDER))
    assert msg is not None
    assert "branch tokens" in msg  # all three tokens = template not filled in


def test_missing_board_write_fails(tmp_path):
    msg = ccd.scan_file(_write(tmp_path, "Q-TEST-4-closure-ambiguous.md", MISSING_BOARD_WRITE))
    assert msg is not None
    assert "Board write" in msg
    assert "no 'Iterate' heading" not in msg  # heading + Next are fine here


# ── adversarial-review regressions (2026-08-04 pre-ratification pass) ──

def test_tokens_only_inside_fence_fail(tmp_path):
    # Fence-blindness false pass: a quoted template must not satisfy the gate.
    msg = ccd.scan_file(_write(tmp_path, "Q-TEST-7-closure-resolved.md", ALL_IN_FENCE))
    assert msg is not None
    assert "no 'Iterate' heading" in msg


def test_prose_next_steps_fails(tmp_path):
    # "Next steps: ITERATE ..." prose must not satisfy the typed-branch check.
    msg = ccd.scan_file(_write(tmp_path, "Q-TEST-8-closure-resolved.md", PROSE_NEXT_ONLY))
    assert msg is not None
    assert "no 'Next:'" in msg


def test_decoy_prose_cannot_shadow_placeholder(tmp_path):
    # A prose "Next: STOP" above the block must not mask the unfilled
    # placeholder inside the real block (search is scoped after the heading).
    msg = ccd.scan_file(
        _write(tmp_path, "Q-TEST-9-closure-ambiguous.md", DECOY_THEN_PLACEHOLDER)
    )
    assert msg is not None
    assert "placeholder" in msg


def test_reproposal_bar_prose_second_token_passes(tmp_path):
    # "STOP — do not ITERATE without new mechanism evidence" is house style,
    # not an unfilled placeholder; it must pass.
    assert ccd.scan_file(
        _write(tmp_path, "Q-TEST-10-closure-falsified.md", PROSE_SECOND_TOKEN)
    ) is None


def test_hyphenated_board_write_passes(tmp_path):
    assert ccd.scan_file(
        _write(tmp_path, "Q-TEST-11-closure-resolved.md", HYPHENATED_BOARD)
    ) is None


# ── grandfathering: forward-only boundary ──────────────────────

def test_grandfathered_names_are_skipped_in_scan(tmp_path):
    _write(tmp_path, "Q-RAIL-1-closure-resolved.md", MISSING_BLOCK)  # legacy name
    _write(tmp_path, "Q-NEW-1-closure-falsified.md", COMPLIANT)
    scoped = ccd.in_scope(tmp_path)
    assert [p.name for p in scoped] == ["Q-NEW-1-closure-falsified.md"]


def test_grandfather_list_matches_the_adr_boundary():
    # Every grandfathered name must exist on disk: a typo silently removes
    # the real file from the fixed forward-only boundary.
    for name in ccd.GRANDFATHERED:
        assert (ccd.CLOSURES_DIR / name).is_file(), f"grandfathered but absent: {name}"


def test_explicit_path_skips_grandfathered_in_closures_dir():
    # Naming a grandfathered closure must SKIP, not invite retro-editing.
    legacy = ccd.CLOSURES_DIR / "Q-RAIL-1-closure-resolved.md"
    assert ccd.main([str(legacy)]) == 0


# ── explicit-path mode: authoring-time hard answer ─────────────

def test_explicit_path_mode_is_always_hard(tmp_path):
    bad = _write(tmp_path, "Q-TEST-5-closure-void.md", MISSING_BLOCK)
    good = _write(tmp_path, "Q-TEST-6-closure-resolved.md", COMPLIANT)
    assert ccd.main([str(bad)]) == 1
    assert ccd.main([str(good)]) == 0


def test_explicit_path_registry_only_is_hard(tmp_path, capsys):
    old, new, reason = DEFECTS["registry"]
    bad = _write(
        tmp_path,
        "Q-TEST-12-closure-falsified.md",
        COMPLIANT.replace(old, new, 1),
    )
    assert ccd.main([str(bad)]) == 1
    out = capsys.readouterr().out
    assert out.startswith("HARD closure-disposition: ")
    assert reason in out


def test_explicit_path_same_grandfather_name_outside_closures_fails(
    tmp_path, capsys
):
    outside = _write(tmp_path, "Q-RAIL-1-closure-resolved.md", MISSING_BLOCK)
    assert ccd.main([str(outside)]) == 1
    out = capsys.readouterr().out
    assert "HARD closure-disposition:" in out
    assert "no 'Iterate' heading" in out


def test_explicit_path_and_list_debt_do_not_run_coverage(
    tmp_path, monkeypatch
):
    bad = _write(tmp_path, "Q-TEST-13-closure-void.md", MISSING_BLOCK)

    def fail_coverage():
        raise AssertionError("coverage must not run in this mode")

    monkeypatch.setattr(ccd, "missing_closure_campaigns", fail_coverage)
    assert ccd.main([str(bad)]) == 1
    assert ccd.main(["--list-debt"]) == 0


def test_scan_registry_requires_token_on_new_closure(tmp_path):
    body = COMPLIANT.replace(
        "- **Registry:** n/a — fixture / not a strategy-grounds kill\n", ""
    )
    path = _write(tmp_path, "Q-NEW-1-closure-falsified.md", body)
    msg = ccd.scan_registry(path)
    assert msg is not None
    assert "Registry" in msg


def test_scan_registry_accepts_na_reason(tmp_path):
    path = _write(tmp_path, "Q-NEW-2-closure-resolved.md", COMPLIANT)
    assert ccd.scan_registry(path) is None


def test_scan_registry_skips_grandfathered_name(tmp_path):
    # Filename match is enough — do not retro-edit the live grandfathered body.
    name = next(iter(ccd.REGISTRY_GRANDFATHERED))
    path = _write(tmp_path, name, "# no iterate\n")
    assert ccd.scan_registry(path) is None


def test_registry_grandfathered_split_is_exact_partition():
    """2026-08-15 governance-belt audit action 4: NA/DEBT must partition the
    union exactly — no overlap (a name can't be simultaneously "doesn't owe
    a row" and "owes a row"), and nothing dropped when the set was split."""
    assert ccd.REGISTRY_GRANDFATHERED_NA.isdisjoint(ccd.REGISTRY_DEBT_2026_08)
    assert (ccd.REGISTRY_GRANDFATHERED_NA | ccd.REGISTRY_DEBT_2026_08) == ccd.REGISTRY_GRANDFATHERED
    assert len(ccd.REGISTRY_GRANDFATHERED) == 66  # count at 2026-08-15 split; grows forward-only
    # 33 at split minus 3 reclassified DEBT → NA on 2026-08-24 (not discharged).
    assert len(ccd.REGISTRY_DEBT_2026_08) == 30
    assert len(ccd.REGISTRY_GRANDFATHERED_NA) == 36
    assert ccd._REGISTRY_RECLASSIFIED_TO_NA_2026_08_24 <= ccd.REGISTRY_GRANDFATHERED_NA
    assert ccd._REGISTRY_RECLASSIFIED_TO_NA_2026_08_24.isdisjoint(
        ccd.REGISTRY_DEBT_2026_08
    )


def test_scan_registry_skips_debt_name_too(tmp_path):
    # Debt-bucket names are still mechanically exempt -- the split is a
    # triage aid, not a change to gate behavior.
    name = next(iter(ccd.REGISTRY_DEBT_2026_08))
    path = _write(tmp_path, name, "# no iterate\n")
    assert ccd.scan_registry(path) is None


def test_unpaid_registry_debt_reports_missing_row(tmp_path):
    registry = tmp_path / "rejected_candidates.md"
    registry.write_text("# empty registry\n", encoding="utf-8")
    assert ccd.unpaid_registry_debt(
        debt_names=frozenset({"MSL-C1-closure-falsified.md"}),
        registry_path=registry,
    ) == ["MSL-C1-closure-falsified.md"]


def test_unpaid_registry_debt_clears_when_filename_lands(tmp_path):
    registry = tmp_path / "rejected_candidates.md"
    registry.write_text(
        "briefs/closures/MSL-C1-closure-falsified.md\n", encoding="utf-8"
    )
    assert ccd.unpaid_registry_debt(
        debt_names=frozenset({"MSL-C1-closure-falsified.md"}),
        registry_path=registry,
    ) == []


def test_unpaid_registry_debt_fails_closed_on_missing_registry(tmp_path):
    missing = tmp_path / "no-such-registry.md"
    names = frozenset({"MSL-C1-closure-falsified.md", "MSL-C2-closure-falsified.md"})
    assert ccd.unpaid_registry_debt(debt_names=names, registry_path=missing) == sorted(
        names
    )


def test_live_registry_clears_all_debt_snapshot_names():
    """2026-08-24 backfill landed a row for every remaining DEBT name."""
    assert ccd.unpaid_registry_debt() == []


def test_list_debt_cli_lists_unpaid_not_the_snapshot(capsys):
    rc = ccd.main(["--list-debt"])
    assert rc == 0
    out = capsys.readouterr().out
    unpaid = set(ccd.unpaid_registry_debt())
    for name in unpaid:
        assert name in out
    for name in ccd.REGISTRY_DEBT_2026_08 - unpaid:
        assert name not in out
    for name in ccd.REGISTRY_GRANDFATHERED_NA:
        assert name not in out
    assert f"{len(unpaid)} closure(s) owe" in out


# ── coverage limb: closed campaign with no closure file (lesson_green_gate) ──

_INDEX_FIXTURE = """# Open-Question Roster

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-OPEN-1** — still investigating | **`OPEN`** | [`x`](x.md) | keep going |
| **Q-OFCHAN-1** — Route B order-flow | **`CLOSED — Stage-G VOID-COVERAGE`** 2026-08-07 — empty candidates | [`Q-OFCHAN-1.md`](Q-OFCHAN-1.md) | Do **not** retune |
| **Q-TOM-SPX-1** — turn-of-month | Layer A **RESOLVED-ABSENT** on Pepperstone; formal DEAD close reserved | [`Q-TOM-SPX-1.md`](Q-TOM-SPX-1.md) | reserved close only |
| **Q-CAPRES-2** — Cap seat | **RESOLVED** — reservation GO; CapFLOW BLOCKED | [`Q-CAPRES-2.md`](Q-CAPRES-2.md) | join still owed |
| **Q-DRAFT-1** — not opened | **`DRAFT — gated`** on ADR ratification | [`d`](d.md) | wait |

## Dormant (no current session home; resurface before assuming dead)

| Q | Status | Home | Note |
|---|---|---|---|
| ~~**Q-FUNDPOL-1** — funded-phase~~ → **DORMANT 2026-08-04** | measurement | [`f`](f.md) | do not build |

## Recently closed (cross-reference; not open)

- **Q-HASCLOS-1** — some cell — **FALSIFIED 2026-08-01** — [`closure`](closures/Q-HASCLOS-1-closure-falsified.md).
- **Q-NOCLOS-1** — some cell — **FALSIFIED 2026-08-01** — no closure authored.
- **GSUB-1** — subtract pass — **`RESOLVED-LOADBEARING` 2026-08-09** — [`closure`](closures/GSUB-1-closure-resolved-loadbearing.md).
"""

_CATALOG_FIXTURE = """# Lab analysis catalog

## Active

| slug | theme | status | one-liner | body | heavy |
|---|---|---|---|---|---|
| mnq_ofchan_routeb_2026-08 | c1 | ACTIVE | Q-OFCHAN-1 VOID-COVERAGE | lab/analysis/c1/mnq_ofchan_routeb_2026-08/ | — |
| mnq_alive_2026-08 | c1 | ACTIVE | still running | lab/analysis/c1/mnq_alive_2026-08/ | — |
| mnq_r2vbuck_routeb_2026-08 | c1 | HOLD | archive owed (FALSIFIED): `FALSIFIED` — Q-R2VBUCK-1 empty candidates | lab/analysis/c1/mnq_r2vbuck_routeb_2026-08/ | — |

## Archived

| slug | theme | card | body | heavy |
|---|---|---|---|---|
| old_study_2026-06 | c1 | lab/analysis/old/CARD.md | lab/archive/old/ | — |
"""


def _coverage_repo(tmp_path: Path, *, with_ofchan_closure: bool = False) -> Path:
    """Minimal repo layout for the missing-closure coverage limb."""
    (tmp_path / "docs" / "briefs" / "closures").mkdir(parents=True)
    (tmp_path / "docs" / "ltm" / "briefs").mkdir(parents=True)
    (tmp_path / "lab").mkdir(parents=True)
    (tmp_path / "docs" / "briefs" / "INDEX.md").write_text(_INDEX_FIXTURE, encoding="utf-8")
    (tmp_path / "lab" / "CATALOG.md").write_text(_CATALOG_FIXTURE, encoding="utf-8")
    # Sentinel joinable LTM file so the fixture is a "full checkout" (corpus
    # present). Public-seed / template-only trees are covered by dedicated tests.
    (tmp_path / "docs" / "ltm" / "briefs" / "Q-LTMCORPUS-1-closure.md").write_text(
        COMPLIANT, encoding="utf-8"
    )
    # Present closure for the positive control
    (tmp_path / "docs" / "briefs" / "closures" / "Q-HASCLOS-1-closure-falsified.md").write_text(
        COMPLIANT, encoding="utf-8"
    )
    (tmp_path / "docs" / "briefs" / "closures" / "GSUB-1-closure-resolved-loadbearing.md").write_text(
        COMPLIANT, encoding="utf-8"
    )
    # Grandfathered name present (must not be required to have Iterate tokens,
    # but DOES count as a closure record for coverage).
    (tmp_path / "docs" / "briefs" / "closures" / "Q-RAIL-1-closure-resolved.md").write_text(
        MISSING_BLOCK, encoding="utf-8"
    )
    if with_ofchan_closure:
        (tmp_path / "docs" / "briefs" / "closures" / "Q-OFCHAN-1-closure-void-coverage.md").write_text(
            COMPLIANT, encoding="utf-8"
        )
    return tmp_path


def _clean_gate_repo(
    tmp_path,
    monkeypatch,
    checker=ccd,
    *,
    actual_scope=None,
    actual_missing=None,
):
    repo = _coverage_repo(tmp_path / "repo", with_ofchan_closure=True)
    closures = repo / "docs" / "briefs" / "closures"
    for name in (
        "Q-NOCLOS-1-closure-falsified.md",
        "Q-R2VBUCK-1-closure-falsified.md",
    ):
        _write(closures, name, COMPLIANT)
    scope_fn = checker.in_scope if actual_scope is None else actual_scope
    missing_fn = (
        checker.missing_closure_campaigns
        if actual_missing is None
        else actual_missing
    )
    monkeypatch.setattr(checker, "REPO", repo)
    monkeypatch.setattr(checker, "CLOSURES_DIR", closures)
    monkeypatch.setattr(checker, "in_scope", lambda: scope_fn(closures))
    monkeypatch.setattr(
        checker, "missing_closure_campaigns", lambda: missing_fn(repo)
    )
    assert missing_fn(repo) == []
    assert all(checker.scan_file(p) is None for p in scope_fn(closures))
    assert all(checker.scan_registry(p) is None for p in scope_fn(closures))
    return repo, closures / "Q-HASCLOS-1-closure-falsified.md"


def _owner_paths(repo: Path) -> dict[str, Path]:
    adr_dir = repo / "docs" / "adr"
    return {
        "iterate": adr_dir / FORMER_ITERATE_OWNER,
        "coverage": adr_dir / FORMER_COVERAGE_OWNER,
    }


def _selected_owner_limbs(owner_target: str) -> set[str]:
    if owner_target == "both":
        return {"iterate", "coverage"}
    return {owner_target}


def _owner_fixture(status: str) -> str:
    addendum_status = "Proposed" if status == "Accepted" else "Accepted"
    return (
        "# Historical owner fixture\n\n"
        f"**Status:** `{status}` — header token\n\n"
        "---\n\n## Addendum\n\n"
        f"**Status:** `{addendum_status}` — conflicting later prose\n"
    )


def _configure_former_owners(
    repo: Path,
    monkeypatch,
    *,
    owner_target: str,
    owner_variant: str,
    checker=ccd,
) -> None:
    paths = _owner_paths(repo)
    selected = _selected_owner_limbs(owner_target)
    for limb, path in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if limb in selected and owner_variant == "missing":
            continue
        if limb in selected and owner_variant == "malformed":
            body = "# Historical owner fixture\n\nNo Status token.\n"
        else:
            status = (
                owner_variant
                if limb in selected and owner_variant in {"Accepted", "Proposed"}
                else "Accepted"
            )
            body = _owner_fixture(status)
        path.write_text(body, encoding="utf-8")

    if hasattr(checker, "OWNING_ADR"):
        monkeypatch.setattr(checker, "OWNING_ADR", paths["iterate"])
    if hasattr(checker, "COVERAGE_OWNING_ADR"):
        monkeypatch.setattr(
            checker, "COVERAGE_OWNING_ADR", paths["coverage"]
        )

    if owner_variant == "unreadable":
        denied = {
            os.path.normcase(str(paths[limb].resolve()))
            for limb in selected
        }
        actual_open = Path.open

        def deny_selected_owner(path, *args, **kwargs):
            if os.path.normcase(str(path.resolve())) in denied:
                raise PermissionError(f"denied owner fixture: {path}")
            return actual_open(path, *args, **kwargs)

        monkeypatch.setattr(Path, "open", deny_selected_owner)


def _apply_defect(repo: Path, closure: Path, defect: str) -> str:
    if defect == "coverage":
        missing = (
            repo
            / "docs"
            / "briefs"
            / "closures"
            / "Q-NOCLOS-1-closure-falsified.md"
        )
        missing.unlink()
        return "Q-NOCLOS-1"
    old, new, reason = DEFECTS[defect]
    assert old in COMPLIANT
    closure.write_text(COMPLIANT.replace(old, new, 1), encoding="utf-8")
    return reason


def _hard_prefixes(output: str) -> set[str]:
    prefixes = set()
    for line in output.splitlines():
        if line.startswith("HARD closure-disposition registry:"):
            prefixes.add("registry")
        elif line.startswith("HARD closure-disposition coverage:"):
            prefixes.add("coverage")
        elif line.startswith("HARD closure-disposition:"):
            prefixes.add("iterate")
    return prefixes


def _assert_independent_hard_failure(
    defect: str, reason: str, output: str
) -> None:
    expected_limb = (
        "coverage"
        if defect == "coverage"
        else "registry"
        if defect == "registry"
        else "iterate"
    )
    assert _hard_prefixes(output) == {expected_limb}
    assert reason in output
    warn_prefix = {
        "iterate": "WARN closure-disposition:",
        "registry": "WARN closure-disposition registry:",
        "coverage": "WARN closure-disposition coverage:",
    }[expected_limb]
    assert not any(
        line.startswith(warn_prefix) for line in output.splitlines()
    )


def test_coverage_reports_closed_campaign_without_closure(tmp_path):
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    missing = ccd.missing_closure_campaigns(repo)
    ids = {m.campaign_id for m in missing}
    assert "Q-OFCHAN-1" in ids, "Open-table CLOSED row must be reported"
    assert "Q-NOCLOS-1" in ids, "Recently-closed bullet without a file must be reported"
    assert "Q-R2VBUCK-1" in ids, "CATALOG archive-owed FALSIFIED with Q-ID must be reported"


def test_coverage_silent_when_closure_exists(tmp_path):
    repo = _coverage_repo(tmp_path, with_ofchan_closure=True)
    missing = ccd.missing_closure_campaigns(repo)
    ids = {m.campaign_id for m in missing}
    assert "Q-OFCHAN-1" not in ids
    assert "Q-HASCLOS-1" not in ids
    assert "GSUB-1" not in ids


def test_coverage_skips_non_closure_bearing_statuses(tmp_path):
    repo = _coverage_repo(tmp_path)
    missing = ccd.missing_closure_campaigns(repo)
    ids = {m.campaign_id for m in missing}
    assert "Q-OPEN-1" not in ids
    assert "Q-TOM-SPX-1" not in ids, "RESOLVED-ABSENT / DEAD-close-reserved is not a filed close"
    assert "Q-CAPRES-2" not in ids, "bare RESOLVED in Open is not a filed close"
    assert "Q-DRAFT-1" not in ids
    assert "Q-FUNDPOL-1" not in ids, "Dormant section is not closure-bearing"


def test_claimed_closed_from_hot_bodies_heading():
    for heading in ("## Active", "## Hot bodies"):
        text = _CATALOG_FIXTURE.replace("## Active", heading)
        claimed = ccd.claimed_closed_campaigns_from_catalog(text)
        ids = {c.campaign_id for c in claimed}
        assert "Q-R2VBUCK-1" in ids


def test_coverage_id_extraction_matches_roster_stored_form():
    # M-AHF: bold + em-dash + backticks around CLOSED — extract from the real INDEX.
    text = (
        "## Open\n\n"
        "| Q | Status | Home | Next |\n"
        "|---|---|---|---|\n"
        "| **Q-OFCHAN-1** — Route B | **`CLOSED — Stage-G VOID-COVERAGE`** 2026-08-07 "
        "| [`Q-OFCHAN-1.md`](Q-OFCHAN-1.md) | x |\n"
    )
    claimed = ccd.claimed_closed_campaigns_from_index(text)
    assert any(c.campaign_id == "Q-OFCHAN-1" for c in claimed)


def test_coverage_accepts_nonstandard_closure_filename():
    # Q-KBUDGET-HARVEST-1-bounded-... has no '-closure-' token but is a closure record.
    assert ccd.campaign_id_from_closure_filename(
        "Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md"
    ) == "Q-KBUDGET-HARVEST-1"
    assert ccd.campaign_id_from_closure_filename(
        "Q-OFCHAN-1-closure-void-coverage.md"
    ) == "Q-OFCHAN-1"


def test_coverage_reporter_empty_findings_has_no_output(capsys):
    code = ccd.report_missing_closure_coverage([])
    assert code == 0
    assert capsys.readouterr().out == ""


def test_coverage_reporter_is_fixed_hard(tmp_path, capsys):
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    findings = ccd.missing_closure_campaigns(repo)
    assert findings  # precondition: real violation fixture
    code = ccd.report_missing_closure_coverage(findings)
    assert code == 1
    out = capsys.readouterr().out
    assert out.startswith("HARD closure-disposition coverage:")
    assert "Q-OFCHAN-1" in out
    assert "Q-NOCLOS-1" in out


def test_coverage_grandfathered_ids_excluded(tmp_path):
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    all_missing = ccd.missing_closure_campaigns(repo, grandfathered=frozenset())
    assert "Q-OFCHAN-1" in {m.campaign_id for m in all_missing}
    filtered = ccd.missing_closure_campaigns(
        repo, grandfathered=frozenset({"Q-OFCHAN-1", "Q-NOCLOS-1"})
    )
    ids = {m.campaign_id for m in filtered}
    assert "Q-OFCHAN-1" not in ids
    assert "Q-NOCLOS-1" not in ids
    assert "Q-R2VBUCK-1" in ids  # non-grandfathered still reported


def test_coverage_grandfathered_set_empty_at_promotion_baseline():
    # PR #745 cleared 9 → 0; the permanent set must stay empty unless a
    # superseding ADR adds IDs (never silent append to dodge).
    assert ccd.COVERAGE_GRANDFATHERED == frozenset()


def test_coverage_public_seed_missing_ltm_dir_is_silent(tmp_path):
    """docs/ltm/briefs/ is excluded from the public seed; a campaign whose
    closure lives only there is unverifiable, not missing (same posture as
    check_adr_graph.py's A3 check for docs/ltm/adr/)."""
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    ltm_dir = repo / "docs" / "ltm" / "briefs"
    for f in ltm_dir.iterdir():
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            for child in f.iterdir():
                child.unlink()
            f.rmdir()
    ltm_dir.rmdir()
    assert ccd.missing_closure_campaigns(repo) == []


def test_coverage_public_seed_ltm_dir_without_joinable_closures_is_silent(tmp_path):
    """A nested non-closure restore must not re-arm HARD coverage.

    Recreates the 2026-08-21 public-seed state: docs/ltm/briefs/ exists
    because rnd-pipeline/discovery-campaign-template.md was restored, but
    no joinable Q-* closure file is present.
    """
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    ltm_dir = repo / "docs" / "ltm" / "briefs"
    for f in ltm_dir.iterdir():
        if f.is_file():
            f.unlink()
    nested = ltm_dir / "rnd-pipeline"
    nested.mkdir()
    (nested / "discovery-campaign-template.md").write_text("# template\n", encoding="utf-8")
    assert ccd.ltm_closure_corpus_present(ltm_dir) is False
    assert ccd.missing_closure_campaigns(repo) == []


@pytest.mark.parametrize(
    "owner_variant",
    ["Accepted", "Proposed", "missing", "malformed", "unreadable"],
)
@pytest.mark.parametrize("owner_target", ["iterate", "coverage", "both"])
def test_clean_repo_ignores_former_owner_state(
    tmp_path,
    monkeypatch,
    capsys,
    owner_target,
    owner_variant,
):
    repo, _ = _clean_gate_repo(tmp_path, monkeypatch)
    _configure_former_owners(
        repo,
        monkeypatch,
        owner_target=owner_target,
        owner_variant=owner_variant,
    )
    assert ccd.main([]) == 0
    out = capsys.readouterr().out
    assert "owning ADR" not in out
    assert "coverage ADR" not in out
    assert not any(line.startswith("WARN ") for line in out.splitlines())


@pytest.mark.parametrize(
    "owner_variant",
    ["Accepted", "Proposed", "missing", "malformed", "unreadable"],
)
@pytest.mark.parametrize("owner_target", ["iterate", "coverage", "both"])
@pytest.mark.parametrize(
    "defect", ["heading", "next", "board", "registry", "coverage"]
)
def test_repo_mode_defects_are_hard_independent_of_former_owner_state(
    tmp_path,
    monkeypatch,
    capsys,
    owner_target,
    owner_variant,
    defect,
):
    repo, closure = _clean_gate_repo(tmp_path, monkeypatch)
    _configure_former_owners(
        repo,
        monkeypatch,
        owner_target=owner_target,
        owner_variant=owner_variant,
    )
    reason = _apply_defect(repo, closure, defect)
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    _assert_independent_hard_failure(defect, reason, out)


def test_main_iterate_only_is_hard_without_former_owner(
    tmp_path, monkeypatch, capsys
):
    repo, closure = _clean_gate_repo(tmp_path, monkeypatch)
    _configure_former_owners(
        repo,
        monkeypatch,
        owner_target="both",
        owner_variant="missing",
    )
    reason = _apply_defect(repo, closure, "heading")
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    _assert_independent_hard_failure("heading", reason, out)


def test_main_registry_only_is_hard_without_former_owner(
    tmp_path, monkeypatch, capsys
):
    repo, closure = _clean_gate_repo(tmp_path, monkeypatch)
    _configure_former_owners(
        repo,
        monkeypatch,
        owner_target="both",
        owner_variant="missing",
    )
    reason = _apply_defect(repo, closure, "registry")
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    _assert_independent_hard_failure("registry", reason, out)


def test_main_coverage_only_is_hard_without_former_owner(
    tmp_path, monkeypatch, capsys
):
    repo, closure = _clean_gate_repo(tmp_path, monkeypatch)
    _configure_former_owners(
        repo,
        monkeypatch,
        owner_target="both",
        owner_variant="missing",
    )
    reason = _apply_defect(repo, closure, "coverage")
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    _assert_independent_hard_failure("coverage", reason, out)


def test_repo_mode_reports_iterate_registry_and_coverage_together(
    tmp_path, monkeypatch, capsys
):
    repo, closure = _clean_gate_repo(tmp_path, monkeypatch)
    _configure_former_owners(
        repo,
        monkeypatch,
        owner_target="both",
        owner_variant="missing",
    )
    body = COMPLIANT
    for defect in ("next", "registry"):
        old, new, _ = DEFECTS[defect]
        body = body.replace(old, new, 1)
    closure.write_text(body, encoding="utf-8")
    _apply_defect(repo, closure, "coverage")
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    assert _hard_prefixes(out) == {"iterate", "registry", "coverage"}
    assert "no 'Next:'" in out
    assert "closure lacks a Registry line" in out
    assert "Q-NOCLOS-1" in out


def test_hot_gap_is_covered_by_ltm_then_hard_when_ltm_record_removed(
    tmp_path, monkeypatch, capsys
):
    repo, _ = _clean_gate_repo(tmp_path, monkeypatch)
    hot = (
        repo
        / "docs"
        / "briefs"
        / "closures"
        / "Q-NOCLOS-1-closure-falsified.md"
    )
    ltm = (
        repo
        / "docs"
        / "ltm"
        / "briefs"
        / "Q-NOCLOS-1-closure-falsified.md"
    )
    hot.unlink()
    ltm.write_text(COMPLIANT, encoding="utf-8")

    assert ccd.main([]) == 0
    assert "coverage:" not in capsys.readouterr().out

    ltm.unlink()
    assert (
        repo / "docs" / "ltm" / "briefs" / "Q-LTMCORPUS-1-closure.md"
    ).is_file()
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    assert "HARD closure-disposition coverage:" in out
    assert "Q-NOCLOS-1" in out


@pytest.mark.parametrize("ltm_layout", ["absent", "nested-template"])
@pytest.mark.parametrize("defect", ["next", "registry"])
def test_public_seed_waiver_does_not_mask_iterate_or_registry_failure(
    tmp_path, monkeypatch, capsys, ltm_layout, defect
):
    repo, closure = _clean_gate_repo(tmp_path, monkeypatch)
    ltm_dir = repo / "docs" / "ltm" / "briefs"
    (ltm_dir / "Q-LTMCORPUS-1-closure.md").unlink()
    if ltm_layout == "absent":
        ltm_dir.rmdir()
    else:
        nested = ltm_dir / "rnd-pipeline"
        nested.mkdir()
        (nested / "discovery-campaign-template.md").write_text(
            "# template\n", encoding="utf-8"
        )
    (
        repo
        / "docs"
        / "briefs"
        / "closures"
        / "Q-NOCLOS-1-closure-falsified.md"
    ).unlink()
    reason = _apply_defect(repo, closure, defect)

    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    _assert_independent_hard_failure(defect, reason, out)
    assert "Q-NOCLOS-1" not in out


@pytest.mark.parametrize(
    "denied_limbs",
    [("iterate",), ("coverage",), ("iterate", "coverage")],
)
def test_fresh_checker_never_reads_former_status_owners(
    tmp_path, monkeypatch, capsys, denied_limbs
):
    targets = _owner_paths(REPO)
    denied = {
        os.path.normcase(str(targets[limb].resolve()))
        for limb in denied_limbs
    }
    attempts: list[str] = []
    actual_open = Path.open

    def deny_historical_owner(path, *args, **kwargs):
        resolved = os.path.normcase(str(path.resolve()))
        if resolved in denied:
            attempts.append(resolved)
            raise PermissionError(f"denied historical owner: {path}")
        return actual_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_historical_owner)
    for limb in denied_limbs:
        with pytest.raises(PermissionError):
            targets[limb].open(encoding="utf-8")
    assert attempts == [
        os.path.normcase(str(targets[limb].resolve()))
        for limb in denied_limbs
    ]
    attempts.clear()

    module_name = "check_closure_disposition_denied_" + "_".join(
        denied_limbs
    )
    fresh = _load_checker(module_name)
    actual_scope = fresh.in_scope
    actual_missing = fresh.missing_closure_campaigns
    cases = ("clean", "iterate", "registry", "coverage")
    for case in cases:
        repo, closure = _clean_gate_repo(
            tmp_path / case,
            monkeypatch,
            checker=fresh,
            actual_scope=actual_scope,
            actual_missing=actual_missing,
        )
        if case != "clean":
            defect = "heading" if case == "iterate" else case
            reason = _apply_defect(repo, closure, defect)
        expected = 0 if case == "clean" else 1
        assert fresh.main([]) == expected
        out = capsys.readouterr().out
        if case == "clean":
            assert not any(
                line.startswith(("HARD ", "WARN ")) for line in out.splitlines()
            )
        else:
            _assert_independent_hard_failure(defect, reason, out)
    assert attempts == []
