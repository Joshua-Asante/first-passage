"""Adversarial tests for scripts/check_closure_disposition.py (pre-commit gate 14).

Discipline guards need adversarial tests — a checker that passes on an empty
directory or a vacuous fixture is assurance theater. Every REQUIRED failure
mode below has a fixture that must FAIL, and the compliant fixture must PASS.
"""
from __future__ import annotations

import importlib.util
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
    # Every grandfathered name must exist on disk (a typo'd entry silently
    # un-grandfathers the real file), and no non-grandfathered pre-ADR file
    # may exist without a block once the ADR is Accepted — the second half is
    # exactly what the live scan asserts, so run it.
    for name in ccd.GRANDFATHERED:
        assert (ccd.CLOSURES_DIR / name).is_file(), f"grandfathered but absent: {name}"


# ── severity: self-arming on ADR ratification ──────────────────

def test_adr_status_parses_header_token_only(tmp_path):
    adr = tmp_path / "adr.md"
    adr.write_text(
        "# T\n\n**Status:** `Proposed` — note\n\n---\n\n## Addendum\n"
        "**Status:** `Accepted`\n",  # below the header boundary: ignored
        encoding="utf-8",
    )
    assert ccd.adr_status(adr) == "Proposed"


def test_adr_status_missing_file_degrades(tmp_path):
    assert ccd.adr_status(tmp_path / "nope.md") == "MISSING"


def test_adr_status_survives_frontmatter_and_bare_token(tmp_path):
    adr = tmp_path / "adr.md"
    adr.write_text(
        "---\ntitle: x\n---\n# T\n\n**Status:** Accepted — ratified\n",
        encoding="utf-8",
    )
    assert ccd.adr_status(adr) == "Accepted"


def test_explicit_path_skips_grandfathered_in_closures_dir():
    # Naming a grandfathered closure must SKIP, not hard-fail — hard-failing
    # invites the retro-editing the ADR's §5 forbids.
    legacy = ccd.CLOSURES_DIR / "Q-RAIL-1-closure-resolved.md"
    assert ccd.main([str(legacy)]) == 0


def test_live_scan_is_warn_tier_while_proposed(capsys):
    # The owning ADR ships Proposed; the live corpus scan must exit 0 today
    # regardless of violations, and hard-fail only after ratification.
    if ccd.adr_status() == "Accepted":
        pytest.skip("ADR ratified — WARN-tier branch no longer reachable")
    assert ccd.main([]) == 0


# ── explicit-path mode: authoring-time hard answer ─────────────

def test_explicit_path_mode_is_always_hard(tmp_path):
    bad = _write(tmp_path, "Q-TEST-5-closure-void.md", MISSING_BLOCK)
    good = _write(tmp_path, "Q-TEST-6-closure-resolved.md", COMPLIANT)
    assert ccd.main([str(bad)]) == 1
    assert ccd.main([str(good)]) == 0


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


def test_coverage_limb_is_advisory_while_proposed(tmp_path, capsys):
    # While the coverage ADR is Proposed (or hard=False), missing closures
    # must not flip the exit code — belt-churn / unrelated-work concern.
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    findings = ccd.missing_closure_campaigns(repo)
    assert findings  # precondition: something to warn about
    code = ccd.report_missing_closure_coverage(findings, hard=False)
    assert code == 0
    out = capsys.readouterr().out
    assert out.startswith("WARN ")
    assert "Q-OFCHAN-1" in out
    assert not any(ln.startswith("HARD ") for ln in out.splitlines())


def test_coverage_limb_hard_when_armed(tmp_path, capsys):
    # Adversarial: a fixture that actually violates coverage must fire HARD
    # once the coverage ADR is Accepted (lesson_discipline_guards_need_adversarial_tests).
    repo = _coverage_repo(tmp_path, with_ofchan_closure=False)
    findings = ccd.missing_closure_campaigns(repo)
    assert findings  # precondition: real violation fixture
    code = ccd.report_missing_closure_coverage(findings, hard=True)
    assert code == 1
    out = capsys.readouterr().out
    assert out.startswith("HARD ")
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


def test_coverage_owning_adr_is_accepted_and_armed(capsys):
    # After Accept, coverage limb is HARD-armed; live exit 0 requires backlog clear.
    assert ccd.COVERAGE_OWNING_ADR.is_file(), (
        "coverage owning ADR missing — COVERAGE_OWNING_ADR path drift"
    )
    assert ccd.adr_status(ccd.COVERAGE_OWNING_ADR) == "Accepted"
    missing = ccd.missing_closure_campaigns()
    ltm_briefs = Path(__file__).resolve().parents[2] / "docs" / "ltm" / "briefs"
    if missing and not ltm_briefs.is_dir():
        pytest.skip(
            "closure bodies live under docs/ltm/briefs/ "
            "(excluded from the public seed)"
        )
    assert missing == []
    assert ccd.main([]) == 0
    out = capsys.readouterr().out
    assert "HARD closure-disposition coverage:" not in out


def test_coverage_main_hard_exit_when_adr_accepted(tmp_path, monkeypatch, capsys):
    # Simulated Accepted: coverage violation ⇒ HARD + exit 1.
    adr = tmp_path / "coverage-adr.md"
    adr.write_text(
        "# T\n\n**Status:** `Accepted` — simulated ratification\n\n---\n\n## X\n",
        encoding="utf-8",
    )
    repo = _coverage_repo(tmp_path / "repo", with_ofchan_closure=False)
    findings = ccd.missing_closure_campaigns(repo)
    assert findings  # precondition: violating fixture
    monkeypatch.setattr(ccd, "COVERAGE_OWNING_ADR", adr)
    # Keep Iterate limb green so coverage alone drives the exit code.
    monkeypatch.setattr(ccd, "in_scope", lambda: [])
    monkeypatch.setattr(ccd, "missing_closure_campaigns", lambda: findings)
    assert ccd.main([]) == 1
    out = capsys.readouterr().out
    assert "HARD closure-disposition coverage:" in out
    assert "Q-OFCHAN-1" in out


def test_coverage_main_warn_exit_when_adr_proposed(tmp_path, monkeypatch, capsys):
    # Simulated Proposed with a real coverage gap ⇒ WARN + exit 0.
    adr = tmp_path / "coverage-adr.md"
    adr.write_text(
        "# T\n\n**Status:** `Proposed` — not yet ratified\n\n---\n\n## X\n",
        encoding="utf-8",
    )
    repo = _coverage_repo(tmp_path / "repo", with_ofchan_closure=False)
    findings = ccd.missing_closure_campaigns(repo)
    assert findings
    monkeypatch.setattr(ccd, "COVERAGE_OWNING_ADR", adr)
    monkeypatch.setattr(ccd, "in_scope", lambda: [])
    monkeypatch.setattr(ccd, "missing_closure_campaigns", lambda: findings)
    assert ccd.main([]) == 0
    out = capsys.readouterr().out
    assert "WARN closure-disposition coverage:" in out
    assert "Q-OFCHAN-1" in out
    assert "HARD closure-disposition coverage:" not in out
