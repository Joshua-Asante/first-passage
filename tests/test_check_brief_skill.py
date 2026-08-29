"""Tests for the SKILL-SIDE canonical `check_brief.py`
(`.claude/skills/brief-authoring/scripts/check_brief.py`), authored under
docs/adr/2026-08-09-check-brief-canon-ruling.md.

This is a SEPARATE file from `scripts/check_brief.py` (the repo-side
mechanical subset, covered by tests/test_check_brief.py, NOT modified here).
The two checkers deliberately disagree on lock/notice/lesson/audit/light-tier
records: repo-side declines them (`RESULT: NOT CHECKED`); this skill-side
checker applies each type's OWN section contract, per the ADR's §Decision.

Global constraint (docs/superpowers/plans/2026-08-27-ssot-data-lineage-
remediation.md "Global Constraints"): every new/extended checker must be
mutation-tested — plant the exact bad condition it claims to catch and
confirm a HARD violation actually fires, not just that a well-formed fixture
passes. Every new per-type contract below (notice/audit/lesson/light/lock)
therefore has a paired PASS + adversarial-FAIL case, not just a happy path.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_CB_PATH = (
    Path(__file__).resolve().parent.parent
    / ".claude" / "skills" / "brief-authoring" / "scripts" / "check_brief.py"
)
_spec = importlib.util.spec_from_file_location("check_brief_skill", _CB_PATH)
cb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cb)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _hard(violations) -> list:
    return [v for v in violations if v.severity == "HARD"]


def _warn(violations) -> list:
    return [v for v in violations if v.severity == "WARN"]


def test_skill_side_file_exists_and_loads():
    assert _CB_PATH.exists(), "skill-side check_brief.py must exist in-repo (Task 1)"


# ── general contract (inquire/adr/cc_handoff) — same as repo-side, must ──
# ── keep working since this file is a from-scratch reimplementation ─────

WELL_FORMED = """\
# ADR — sample decision

## §0 — Rule 0: production reads
Read `dd_protection.py` (confirmed at commit abc1234 on 2026-06-04) and
`docs/adr/2026-06-04-lean-portfolio-meta-layer.md`.

## §1 — Context
Connects to standing doctrine: the dd_protection C2 lock.

## §4 — Falsifiable hypothesis
**H:** If X holds, then Y; otherwise Z.
**Falsifier:** if Y does not occur, the claim is falsified and we revert.

## §5 — Forbidden moves
1. Tempting move A, ruled out because reasons.
2. Tempting move B, ruled out.

## §6 — Gate / closure criteria
RESOLVED when the test passes; FALSIFIED if it fails; AMBIGUOUS otherwise.

## §10 — Audit hooks
```bash
grep -r "thing" docs/ && echo found || echo missing
```
"""


def test_general_well_formed_passes_adr():
    v = cb.check_brief(WELL_FORMED, "adr")
    assert _hard(v) == [], v


def test_general_well_formed_passes_inquire():
    v = cb.check_brief(WELL_FORMED, "inquire")
    assert _hard(v) == [], v


def test_general_missing_section10_fails():
    text = WELL_FORMED.split("## §10")[0]
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§10" for vi in _hard(v)), v


HANDOFF = WELL_FORMED.replace(
    "## §1 — Context",
    "## §0.5 — Clarifying questions\nHalt and ask before §2 if anything is ambiguous.\n\n## §1 — Context",
).replace(
    "RESOLVED when the test passes; FALSIFIED if it fails; AMBIGUOUS otherwise.",
    "Return one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.\n"
    "RESOLVED when accepted.",
)


def test_cc_handoff_well_formed_passes():
    v = cb.check_brief(HANDOFF, "cc_handoff")
    assert _hard(v) == [], v


def test_cc_handoff_missing_status_taxonomy_fails():
    text = HANDOFF.replace(
        "Return one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.\n",
        "Report success or failure.\n",
    )
    v = cb.check_brief(text, "cc_handoff")
    assert any(vi.section == "§6" and "taxonomy" in vi.message.lower() for vi in _hard(v)), v


# ── notice — numbered §N, own §0/§4 contract (NOT declined here) ────────

NOTICE_GOOD = """\
# Notice — sample

## §0 — Source anchor
- **Source:** a specific trade row in the June export
- **Observed at:** 2026-06-01

## §1 — The observation
Something specific happened.

## §2 — Why it stands out
- **Baseline:** expected pattern X
- **Delta:** departs by Y

## §3 — Candidate mechanisms
- Mechanism A

## §4 — Routing decision
Decision: DROP
Reason: too small to matter.

## §10 — Audit hooks
```bash
echo check
```
"""


def test_notice_well_formed_passes():
    v = cb.check_brief(NOTICE_GOOD, "notice")
    assert _hard(v) == [], v


def test_notice_no_repo_path_requirement_in_section0():
    """notice_log.md:14 — §0 is 'one line, not a verified-commit list'; the
    general §0 path+anchor contract must NOT apply here (mutation: strip the
    only path-shaped token from §0 and confirm it still passes)."""
    text = NOTICE_GOOD.replace(
        "- **Source:** a specific trade row in the June export",
        "- **Source:** a conversation with Joshua at standup",
    )
    v = cb.check_brief(text, "notice")
    assert not any(vi.section == "§0" for vi in _hard(v)), v


def test_notice_missing_routing_decision_fails():
    """Adversarial: §4 present but with no GRADUATE/DROP/HOLD keyword."""
    text = NOTICE_GOOD.replace(
        "Decision: DROP\nReason: too small to matter.",
        "We will look at this more at some point.",
    )
    v = cb.check_brief(text, "notice")
    hard = _hard(v)
    assert any(vi.section == "§4" and "routing" in vi.message.lower() for vi in hard), v
    assert hard, "expected at least one HARD violation; empty list would pass vacuously"


def test_notice_hold_requires_section5():
    text = NOTICE_GOOD.replace("Decision: DROP\nReason: too small to matter.",
                               "Decision: HOLD\nReason: need more data.")
    v = cb.check_brief(text, "notice")
    assert any(vi.section == "§5" and "missing" in vi.message.lower() for vi in _hard(v)), v


def test_notice_drop_does_not_require_section5():
    v = cb.check_brief(NOTICE_GOOD, "notice")
    assert not any(vi.section == "§5" for vi in v), v


# ── audit — numbered §N, §0 DOES get the path+anchor contract ───────────

AUDIT_GOOD = """\
# Audit Note — sample

## §0 — Source anchors
- `docs/briefs/Q-X-name.md` — commit `abc1234` (the brief being audited)
- `<chat URL>` — the session where the failure surfaced

## §1 — Trigger
On 2026-06-01 something happened.

## §2 — What actually happened
1. Event one.
2. Event two.

## §3 — Discipline checks that should have caught it
| Check | Should have caught | Actual behavior |
|---|---|---|
| §1 Rule 0 | yes | missed |

## §4 — Root cause analysis
- **Immediate cause:** X
- **Structural cause:** Y

## §5 — Repair plan
- [ ] Fix the thing

## §6 — Lessons to capture
- **Candidate lesson 1:** pattern statement

## §7 — Programme-audit signal check
- [ ] Belt-patches without independent corroboration?

## §10 — Audit hooks
```bash
grep -rn "thing" docs/
```

## §11 — Closure
**Status:** Open
"""


def test_audit_well_formed_passes():
    v = cb.check_brief(AUDIT_GOOD, "audit")
    assert _hard(v) == [], v


def test_audit_section0_gets_repo_path_contract():
    """Adversarial: unlike notice, audit's §0 IS supposed to cite a real repo
    path — strip it and confirm the general §0 check fires."""
    text = AUDIT_GOOD.replace(
        "- `docs/briefs/Q-X-name.md` — commit `abc1234` (the brief being audited)\n",
        "",
    )
    v = cb.check_brief(text, "audit")
    assert any(vi.section == "§0" for vi in _hard(v)), v


def test_audit_missing_section11_fails():
    text = AUDIT_GOOD.split("## §11")[0]
    v = cb.check_brief(text, "audit")
    assert any(vi.section == "§11" and "missing" in vi.message.lower() for vi in _hard(v)), v


def test_audit_no_falsifier_check_applied():
    """audit's §4 is root-cause analysis, not a falsifiable hypothesis — a
    §4 with neither H:/falsifier tokens nor canonical framing must NOT fail
    under the audit contract (it would under the general contract)."""
    text = AUDIT_GOOD.replace(
        "- **Immediate cause:** X\n- **Structural cause:** Y",
        "Just some root-cause prose with no H: or falsifier token anywhere.",
    )
    v = cb.check_brief(text, "audit")
    assert not any(vi.section == "§4" for vi in _hard(v)), v


# ── lesson — named headings, not numbered sections ───────────────────────

LESSON_GOOD = """\
# Lesson E-1 — sample

**Status:** `Candidate`

## Pattern (one sentence)
The recurring failure mode.

## Anchor incidents
| Date | Incident | Cost / counterfactual | Source brief |
|---|---|---|---|
| 2026-06-01 | the firing | $500 | docs/briefs/Q-X.md |

## Repair / discipline rule
**Rule:** do the specific thing.

## Audit hooks
```bash
grep -rn "E-1" docs/
```
"""


def test_lesson_well_formed_passes():
    v = cb.check_brief(LESSON_GOOD, "lesson")
    assert _hard(v) == [], v


def test_lesson_missing_repair_section_fails():
    text = LESSON_GOOD.split("## Repair")[0] + "## Audit hooks\n```bash\ngrep -rn E-1 docs/\n```\n"
    v = cb.check_brief(text, "lesson")
    hard = _hard(v)
    assert any("Repair" in vi.section and "missing" in vi.message.lower() for vi in hard), v
    assert hard, "expected at least one HARD violation; empty list would pass vacuously"


def test_lesson_audit_hooks_needs_fence():
    text = LESSON_GOOD.replace(
        '```bash\ngrep -rn "E-1" docs/\n```',
        "Review this quarterly.",
    )
    v = cb.check_brief(text, "lesson")
    assert any(vi.section == "Audit Hooks" for vi in _hard(v)), v


def test_lesson_standing_rule_requires_promotion_record():
    text = LESSON_GOOD.replace("**Status:** `Candidate`", "**Status:** `Standing rule`")
    v = cb.check_brief(text, "lesson")
    assert any(vi.section == "Promotion Record" for vi in _hard(v)), v


def test_lesson_candidate_status_does_not_require_promotion_record():
    v = cb.check_brief(LESSON_GOOD, "lesson")
    assert not any(vi.section == "Promotion Record" for vi in v), v


def test_lesson_retired_requires_retirement_section():
    text = LESSON_GOOD.replace("**Status:** `Candidate`", "**Status:** `Retired (no longer applicable)`")
    v = cb.check_brief(text, "lesson")
    assert any(vi.section == "Retirement" for vi in _hard(v)), v


# ── light-tier ADR — named headings, Gate/Boundary may read literally ───
# ── "none" without that counting as ceremonial ───────────────────────────

LIGHT_GOOD = """\
# ADR 2026-08-09 — a light decision

**Status:** `Accepted`
**Decision date:** 2026-08-09
**Tier:** light

## Decision
We do the thing.

## Grounds
Because of `docs/adr/whatever.md`.

## Reads
`core/dd_protection.py` @ commit abc1234.

## Gate
none

## Boundary
none
"""


def test_light_tier_well_formed_with_literal_none_passes():
    assert cb.is_light_tier(LIGHT_GOOD)
    v = cb.check_brief(LIGHT_GOOD, "adr")
    assert _hard(v) == [], v
    assert _warn(v) == [], v  # literal "none" must NOT warn as ceremonial


def test_light_tier_missing_grounds_fails():
    text = LIGHT_GOOD.replace(
        "## Grounds\nBecause of `docs/adr/whatever.md`.\n\n", ""
    )
    v = cb.check_brief(text, "adr")
    hard = _hard(v)
    assert any(vi.section == "Grounds" and "missing" in vi.message.lower() for vi in hard), v
    assert hard, "expected at least one HARD violation; empty list would pass vacuously"


def test_light_tier_truly_blank_gate_warns_but_literal_none_does_not():
    blank = LIGHT_GOOD.replace("## Gate\nnone\n", "## Gate\n\n")
    v = cb.check_brief(blank, "adr")
    assert any(vi.section == "Gate" and vi.severity == "WARN" for vi in v), v
    # the original (literal "none") must not warn on Gate at all
    v_good = cb.check_brief(LIGHT_GOOD, "adr")
    assert not any(vi.section == "Gate" for vi in v_good), v_good


def test_light_tier_over_word_limit_warns_not_hard():
    padded = LIGHT_GOOD + ("\nextra filler word" * 350)
    v = cb.check_brief(padded, "adr")
    assert _hard(v) == [], "a false HARD on an over-length light record repeats the exact defect the ADR fixed"
    assert any(vi.section == "body" and vi.severity == "WARN" for vi in v), v


def test_light_tier_detection_beats_requested_type():
    """A light record still gets the light contract even if --type notice was
    (incorrectly) requested — light-tier detection wins, matching repo-side's
    documented precedence."""
    v_as_notice = cb.check_brief(LIGHT_GOOD, "notice")
    v_as_adr = cb.check_brief(LIGHT_GOOD, "adr")
    assert v_as_notice == v_as_adr


# ── lock — retired type, best-effort content-only check ──────────────────

def test_lock_with_trigger_table_passes():
    text = "# Lock decision — sample\n\n| Trigger | Threshold |\n|---|---|\n| PF drop | <1.0 |\n"
    v = cb.check_brief(text, "lock")
    assert _hard(v) == [], v


def test_lock_with_canonical_framing_passes():
    text = "# Lock decision — sample\n\n**Revert trigger:** rolling PF <1.0 across 2 windows.\n"
    v = cb.check_brief(text, "lock")
    assert _hard(v) == [], v


def test_lock_with_neither_fails():
    text = "# Lock decision — sample\n\nJust some prose with no table and no falsifier language at all.\n"
    v = cb.check_brief(text, "lock")
    hard = _hard(v)
    assert hard, "a lock record with no table and no canonical framing must fail"
    assert any(vi.section == "§4" for vi in hard), v


# ── closure — delegates, same as repo-side, kept for CLI parity ─────────

def test_closure_delegates_to_empty_violation_list():
    text = "# Q-X — CLOSURE: `RESOLVED` (test)\n\n## Iterate\n- **Next:** INTEGRATE\n"
    assert cb.check_brief(text, "closure") == []


def test_main_closure_delegates_and_does_not_apply_general_contract(tmp_path, capsys):
    p = tmp_path / "Q-X-closure-resolved.md"
    p.write_text("# Q-X — CLOSURE: `RESOLVED` (test)\n\n## Iterate\n- **Next:** INTEGRATE\n",
                 encoding="utf-8")
    rc = cb.main([str(p), "--type", "closure"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "DELEGATED" in out
    assert "well-formed" not in out


# ── type inference from template-native ID header fields ────────────────

def test_infer_audit_from_id_header():
    text = "# Audit Note — x\n\n**Audit ID:** AUDIT-2026-06-01-x\n"
    assert cb.infer_type(Path("anything.md"), text) == "audit"


def test_infer_notice_from_id_header():
    text = "# Notice — x\n\n**Notice ID:** N-2026-06-01-x\n"
    assert cb.infer_type(Path("anything.md"), text) == "notice"


def test_infer_lesson_from_id_header():
    text = "# Lesson E-1 — x\n\n**Lesson ID:** E-1\n"
    assert cb.infer_type(Path("anything.md"), text) == "lesson"


def test_infer_defaults_to_adr_when_no_signal():
    text = "# Something — x\n\nNo distinguishing header fields at all.\n"
    assert cb.infer_type(Path("anything.md"), text) == "adr"


# ── --self-test / --list-checks CLI surface ─────────────────────────────

def test_self_test_exits_0_no_section_detection_regressions():
    assert cb.run_self_test() == 0


def test_main_self_test_flag(capsys):
    rc = cb.main(["--self-test"])
    assert rc == 0
    assert "SELF-TEST" in capsys.readouterr().out


def test_main_list_checks_flag(capsys):
    rc = cb.main(["--list-checks"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "lesson" in out.lower()
    assert "light-tier" in out.lower() or "light" in out.lower()


def test_main_requires_brief_path_without_flags(capsys):
    # argparse's parser.error() raises SystemExit(2) directly (it never
    # returns), matching this script's usual "2 = usage error" convention.
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        cb.main([])
    assert exc_info.value.code == 2


# ── regression: the light-tier ADR this file itself implements is clean ──

def test_real_canon_ruling_adr_is_well_formed():
    path = REPO_ROOT / "docs" / "adr" / "2026-08-09-check-brief-canon-ruling.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert cb.is_light_tier(text)
    v = cb.check_brief(text, "adr")
    assert _hard(v) == [], [str(x) for x in _hard(v)]


def test_file_not_found_exits_2(tmp_path, capsys):
    rc = cb.main([str(tmp_path / "nope.md")])
    assert rc == 2
    assert "not found" in capsys.readouterr().err
