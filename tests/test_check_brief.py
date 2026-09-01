"""Tests for scripts/check_brief.py — the brief well-formedness validator.

The validator encodes the *mechanical* subset of brief-authoring SKILL.md's
"six load-bearing discipline checks" + CC-handoff patterns 7-10:
  §0 cites a repo path, §1/§4/§5/§6/§10 present, §4 has H: + falsifier,
  §5 lists forbidden moves, §10 has a runnable fenced block; present-but-empty
  sections WARN (ceremonial-section trap #1).

These tests are TDD-style fixtures (inline strings + the two real ADRs):
  - a well-formed brief passes (HARD == 0)
  - a brief missing the §4 falsifier fails HARD
  - a brief missing §5 / §10 fails HARD
  - an empty-but-present section WARNs (exit 0)
  - the two committed ADRs are well-formed (regression / migration smoke test)
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_CB_PATH = Path(__file__).resolve().parent.parent / "scripts" / "check_brief.py"
_spec = importlib.util.spec_from_file_location("check_brief", _CB_PATH)
cb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cb)

REPO_ROOT = Path(__file__).resolve().parent.parent


# A minimal well-formed ADR/brief that satisfies every HARD mechanical check.
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


def _drop_section(text: str, heading_prefix: str) -> str:
    """Remove a whole section block (heading line through the line before the
    next `## ` heading). Used to synthesize 'missing section N' fixtures."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    skipping = False
    for line in lines:
        if line.startswith("## ") and heading_prefix in line:
            skipping = True
            continue
        if skipping and line.startswith("## "):
            skipping = False
        if not skipping:
            out.append(line)
    return "".join(out)


def _hard(violations) -> list:
    return [v for v in violations if v.severity == "HARD"]


def _warn(violations) -> list:
    return [v for v in violations if v.severity == "WARN"]


# ── well-formed path ───────────────────────────────────────────

def test_well_formed_passes():
    v = cb.check_brief(WELL_FORMED, "adr")
    assert _hard(v) == [], v
    assert _warn(v) == [], v


def test_main_well_formed_exits_0(tmp_path, capsys):
    p = tmp_path / "brief.md"
    p.write_text(WELL_FORMED, encoding="utf-8")
    rc = cb.main([str(p), "--type", "adr"])
    assert rc == 0
    assert "well-formed" in capsys.readouterr().out


# ── §4 falsifier missing → HARD ────────────────────────────────

def test_missing_falsifier_fails():
    # CONTRACT CHANGE 2026-08-09 (ADR 2026-08-09-rejection-register-topology…
    # sibling fix): §4 is now satisfied by ANY canonical framing — the literal
    # "H:"+"falsifi*" token pair, a "Revert trigger", an if/then, or a
    # reject/accept-if. SKILL.md:145 states the canonical form IS
    # "If [observation], then [conclusion]; otherwise [alternative]", so an
    # if/then alone is a falsifiable hypothesis by the canon's own definition.
    # The old version of this test replaced only the Falsifier line and left the
    # if/then H: line in place — under the corrected contract that text DOES
    # carry a falsifier, so asserting a violation encoded the very repo-vs-skill
    # divergence this change removes. To test the real thing, §4 must lack
    # BOTH.
    text = WELL_FORMED.replace(
        "**H:** If X holds, then Y; otherwise Z.\n"
        "**Falsifier:** if Y does not occur, the claim is falsified and we revert.",
        "We will look at more data later.",
    )
    v = cb.check_brief(text, "adr")
    hard = _hard(v)
    assert any(vi.section == "§4" and "falsifier" in vi.message.lower() for vi in hard), v
    # Adversarial guard: the assertion above must not pass vacuously on an empty
    # violation list.
    assert hard, "expected at least one HARD violation; empty list would pass vacuously"


def test_if_then_alone_satisfies_section4():
    """Canon form (SKILL.md:145) with no literal 'falsifi*' token anywhere."""
    text = WELL_FORMED.replace(
        "**H:** If X holds, then Y; otherwise Z.\n"
        "**Falsifier:** if Y does not occur, the claim is falsified and we revert.",
        "**H:** If the pass rate drops below 95%, then revert to C0; otherwise hold.",
    )
    # Body only — the §4 *heading* is "Falsifiable hypothesis", which would
    # match "falsifi" and make this guard vacuous. split_sections() strips the
    # heading line for exactly this reason, so mirror that here.
    body = text.split("## §4")[1].split("## §5")[0].split("\n", 1)[1]
    assert "falsifi" not in body.lower(), body
    assert not [vi for vi in _hard(cb.check_brief(text, "adr")) if vi.section == "§4"]


def test_revert_trigger_alone_satisfies_section4():
    """The canonical ADR template's own framing (references/adr.md §4)."""
    text = WELL_FORMED.replace(
        "**H:** If X holds, then Y; otherwise Z.\n"
        "**Falsifier:** if Y does not occur, the claim is falsified and we revert.",
        "**Revert trigger:** rolling 6-month pass rate <95% across 2 windows.",
    )
    assert not [vi for vi in _hard(cb.check_brief(text, "adr")) if vi.section == "§4"]


def test_section4_with_no_framing_at_all_still_fails():
    """Adversarial: the broadened acceptance must not accept everything."""
    text = WELL_FORMED.replace(
        "**H:** If X holds, then Y; otherwise Z.\n"
        "**Falsifier:** if Y does not occur, the claim is falsified and we revert.",
        "We will review this at some point once more data accumulates.",
    )
    hard = [vi for vi in _hard(cb.check_brief(text, "adr")) if vi.section == "§4"]
    assert hard, "a §4 with no hypothesis, no falsifier and no canonical framing must fail"


# ── unmodeled contracts: assert nothing rather than the wrong thing ──

def test_unmodeled_contract_types_return_no_violations():
    """lock/notice/lesson/audit have per-type contracts this subset does not
    model. Applying the `generic` contract to them reported the skill's own
    canonical templates as MALFORMED (measured 2026-08-09). We now decline."""
    # Deliberately malformed under the GENERAL contract: no §4, §5, §6, §10.
    text = "# Note\n\n## §0 — Source anchor\n- **Source:** a chat message\n"
    for t in ("lock", "notice", "lesson", "audit"):
        assert cb.check_brief(text, t) == [], f"{t} should assert nothing"
    # Guard against the frozenset being silently emptied.
    assert cb._UNMODELED_CONTRACT_TYPES, "unmodeled-type set must not be empty"
    # ...and against a modeled type being swept in by mistake.
    for t in ("adr", "brief", "handoff", "generic", "inquire", "cc_handoff"):
        assert t not in cb._UNMODELED_CONTRACT_TYPES, f"{t} must stay modeled"


def test_main_reports_not_checked_for_unmodeled_type(tmp_path, capsys):
    p = tmp_path / "note.md"
    p.write_text("# Note\n\n## §0 — Source anchor\n- **Source:** chat\n", encoding="utf-8")
    rc = cb.main([str(p), "--type", "audit"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "NOT CHECKED" in out
    # Must NOT claim a discipline pass.
    assert "well-formed" not in out


def test_missing_hypothesis_fails():
    text = WELL_FORMED.replace("**H:** If X holds, then Y; otherwise Z.", "Some prose.")
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§4" and "hypothesis" in vi.message.lower()
               for vi in _hard(v)), v


# ── §5 / §10 missing → HARD ────────────────────────────────────

def test_missing_section5_fails():
    text = _drop_section(WELL_FORMED, "§5")
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§5" and "missing" in vi.message.lower()
               for vi in _hard(v)), v


def test_missing_section10_fails():
    text = _drop_section(WELL_FORMED, "§10")
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§10" and "missing" in vi.message.lower()
               for vi in _hard(v)), v


def test_section5_no_list_fails():
    text = WELL_FORMED.replace(
        "1. Tempting move A, ruled out because reasons.\n"
        "2. Tempting move B, ruled out.",
        "We considered several things and ruled them out.",
    )
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§5" for vi in _hard(v)), v


def test_section10_no_fence_fails():
    text = WELL_FORMED.replace(
        '```bash\ngrep -r "thing" docs/ && echo found || echo missing\n```',
        "Review the docs quarterly.",
    )
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§10" for vi in _hard(v)), v


# ── §0 path-citation → HARD ────────────────────────────────────

def test_section0_no_repo_path_fails():
    text = WELL_FORMED.replace(
        "Read `dd_protection.py` (confirmed at commit abc1234 on 2026-06-04) and\n"
        "`docs/adr/2026-06-04-lean-portfolio-meta-layer.md`.",
        "We read the production code carefully before authoring.",
    )
    v = cb.check_brief(text, "adr")
    assert any(vi.section == "§0" for vi in _hard(v)), v


def test_section0_path_without_anchor_fails():
    """ADR 2026-08-20 Phase 1: path-only §0 is a new HARD (Known Trap #3)."""
    text = WELL_FORMED.replace(
        "Read `dd_protection.py` (confirmed at commit abc1234 on 2026-06-04) and\n"
        "`docs/adr/2026-06-04-lean-portfolio-meta-layer.md`.",
        "Read `core/dd_protection.py` before authoring.",
    )
    v = cb.check_brief(text, "adr")
    hard = _hard(v)
    assert any(vi.section == "§0" and "anchor" in vi.message.lower() for vi in hard), v
    assert hard, "expected at least one HARD violation; empty list would pass vacuously"


def test_section0_paths_direct_hook_missing_anchor():
    """ADR 2026-08-20 §10 hook: path present, no hash/date → HARD."""
    v = cb._check_section0_paths(
        {"0": "Read core/dd_protection.py before authoring."}
    )
    assert any(vi.severity == "HARD" and "anchor" in vi.message.lower() for vi in v), v


# ── WARN path: present-but-empty section ───────────────────────

def test_empty_section_warns_not_fails():
    # §1 present but empty → WARN, and because all HARD checks still pass the
    # overall result is exit 0.
    text = WELL_FORMED.replace(
        "## §1 — Context\nConnects to standing doctrine: the dd_protection C2 lock.",
        "## §1 — Context\n",
    )
    v = cb.check_brief(text, "adr")
    assert _hard(v) == [], v
    assert any(vi.section == "§1" and vi.severity == "WARN" for vi in v), v


def test_main_warn_only_exits_0(tmp_path, capsys):
    text = WELL_FORMED.replace(
        "## §1 — Context\nConnects to standing doctrine: the dd_protection C2 lock.",
        "## §1 — Context\n",
    )
    p = tmp_path / "brief.md"
    p.write_text(text, encoding="utf-8")
    rc = cb.main([str(p), "--type", "adr"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "WARN" in out


# ── §6 binary-verdict soft nudge → WARN ────────────────────────

def test_vague_gate_warns():
    text = WELL_FORMED.replace(
        "RESOLVED when the test passes; FALSIFIED if it fails; AMBIGUOUS otherwise.",
        "We will close this out when we have learned enough.",
    )
    v = cb.check_brief(text, "adr")
    assert _hard(v) == [], v
    assert any(vi.section == "§6" and vi.severity == "WARN" for vi in v), v


# ── CC-handoff extras ──────────────────────────────────────────

HANDOFF = WELL_FORMED.replace(
    "## §1 — Context",
    "## §0.5 — Clarifying questions\nHalt and ask before §2 if anything is ambiguous.\n\n## §1 — Context",
).replace(
    "RESOLVED when the test passes; FALSIFIED if it fails; AMBIGUOUS otherwise.",
    "Return one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.\n"
    "RESOLVED when accepted.",
)


def test_handoff_well_formed_passes():
    v = cb.check_brief(HANDOFF, "handoff")
    assert _hard(v) == [], v


def test_handoff_missing_status_taxonomy_fails():
    text = HANDOFF.replace(
        "Return one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.\n",
        "Report success or failure.\n",
    )
    v = cb.check_brief(text, "handoff")
    assert any(vi.section == "§6" and "taxonomy" in vi.message.lower()
               for vi in _hard(v)), v


def test_handoff_missing_clarifying_section_fails():
    text = _drop_section(HANDOFF, "§0.5")
    v = cb.check_brief(text, "handoff")
    assert any(vi.section == "§0.5" and "missing" in vi.message.lower()
               for vi in _hard(v)), v


# ── type inference ─────────────────────────────────────────────

def test_infer_handoff_from_status_tokens(tmp_path):
    p = tmp_path / "anything.md"
    assert cb.infer_type(p, HANDOFF) == "handoff"


def test_infer_adr_from_filename(tmp_path):
    p = tmp_path / "adr-2026-foo.md"
    assert cb.infer_type(p, WELL_FORMED) == "adr"


# GSUB-2 shape: Inquire-style header + §0.5 Ambiguity halt, WITHOUT the
# four-state spawn taxonomy. Pre-fix, `"0.5" in split_sections` classified
# this as handoff and HARD-failed the missing DONE/DONE_WITH_CONCERNS/…
# tokens — the Form Check false-positive on
# docs/briefs/programs/GSUB-2-park-cohort-early-review.md (2026-08-19 panel).
INQUIRE_WITH_SECTION_05 = WELL_FORMED.replace(
    "# ADR — sample decision",
    "# GSUB-2 — park-cohort early review\n\n"
    "**Loop:** Inquire-style brief, GRAND-tier",
).replace(
    "## §1 — Context",
    "## §0.5 — Ambiguity halt\n"
    "Halt for operator ratification rather than defaulting. Do not spawn.\n\n"
    "## §1 — Context",
)


def test_infer_inquire_header_beats_section_05(tmp_path):
    """Header Loop: Inquire-style wins over a copied §0.5 Ambiguity halt."""
    p = tmp_path / "GSUB-2-park-cohort-early-review.md"
    assert cb.infer_type(p, INQUIRE_WITH_SECTION_05) == "brief"
    # And the brief must not be scored as a malformed handoff.
    assert _hard(cb.check_brief(INQUIRE_WITH_SECTION_05, "brief")) == []


def test_main_inquire_autodetect_exits_0(tmp_path, capsys):
    p = tmp_path / "GSUB-2-park-cohort-early-review.md"
    p.write_text(INQUIRE_WITH_SECTION_05, encoding="utf-8")
    rc = cb.main([str(p)])  # no --type
    out = capsys.readouterr().out
    assert rc == 0
    assert "type=brief" in out
    assert "type=handoff" not in out
    assert "well-formed" in out
    assert "MALFORMED" not in out


def test_infer_handoff_ready_suffix_is_still_inquire(tmp_path):
    """`Loop: …brief, CC-handoff-ready` is an Inquire brief, not a handoff."""
    text = INQUIRE_WITH_SECTION_05.replace(
        "**Loop:** Inquire-style brief, GRAND-tier",
        "**Loop:** Inquire-style brief, CC-handoff-ready — closure gated on §4",
    )
    p = tmp_path / "GSUB-1-first-grand-subtract-pass.md"
    assert cb.infer_type(p, text) == "brief"


def test_infer_body_handoff_prose_does_not_override_inquire_header(tmp_path):
    """Spawn-taxonomy tokens in the body must not beat an Inquire Loop line."""
    text = INQUIRE_WITH_SECTION_05.replace(
        "RESOLVED when the test passes; FALSIFIED if it fails; AMBIGUOUS otherwise.",
        "Return one of DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED.\n"
        "RESOLVED when accepted.",
    )
    p = tmp_path / "anything.md"
    assert cb.infer_type(p, text) == "brief"


def test_infer_loop_na_before_inquire_phase_is_not_inquire(tmp_path):
    """`Loop: N/A — blocked before the Inquire-phase` is not a self-declaration."""
    text = WELL_FORMED.replace(
        "# ADR — sample decision",
        "# Q-MSCHAN-1\n\n**Loop:** N/A — blocked before the Inquire-phase Pre-Q could gate anything",
    )
    p = tmp_path / "Q-MSCHAN-1-microstructure-sourcing-channel-scoping.md"
    assert cb.infer_type(p, text) != "brief"


def test_infer_handoff_from_brief_type_header(tmp_path):
    """`**Brief type:** CC handoff` is enough even without §0.5 or a handoff filename."""
    text = WELL_FORMED.replace(
        "# ADR — sample decision",
        "# CC Handoff — sample\n\n**Brief type:** CC handoff (single-step)",
    )
    p = tmp_path / "notes.md"
    assert cb.infer_type(p, text) == "handoff"


def test_infer_real_gsub1_is_brief_not_handoff():
    path = REPO_ROOT / "docs/briefs/programs/GSUB-1-first-grand-subtract-pass.md"
    assert path.exists(), "GSUB-1 is the live Inquire-style + §0.5 fixture"
    text = path.read_text(encoding="utf-8")
    assert cb.infer_type(path, text) == "brief"


def test_infer_real_gsub2_is_brief_not_handoff():
    path = REPO_ROOT / "docs/briefs/programs/GSUB-2-park-cohort-early-review.md"
    if not path.exists():
        return  # not on this checkout; INQUIRE_WITH_SECTION_05 covers the shape
    text = path.read_text(encoding="utf-8")
    assert cb.infer_type(path, text) == "brief"
    v = cb.check_brief(text, cb.infer_type(path, text))
    assert _hard(v) == [], [str(x) for x in _hard(v)]


def test_infer_real_cc_handoff_still_handoff():
    path = REPO_ROOT / "docs/briefs/handoffs/2026-07-24-cc-handoff-core-dead-code-prune.md"
    assert path.exists(), "canonical CC-handoff fixture missing"
    text = path.read_text(encoding="utf-8")
    assert cb.infer_type(path, text) == "handoff"


# ── regression: the two real ADRs are well-formed ──────────────

def test_real_adrs_well_formed():
    for name in (
        "docs/adr/2026-06-04-methodology-skills-under-vc.md",
        "docs/adr/2026-06-04-lean-portfolio-meta-layer.md",
    ):
        path = REPO_ROOT / name
        if not path.exists():
            continue  # tolerate absence on a partial checkout
        text = path.read_text(encoding="utf-8")
        v = cb.check_brief(text, "adr")
        assert _hard(v) == [], f"{name}: {[str(x) for x in _hard(v)]}"


def test_file_not_found_exits_2(tmp_path, capsys):
    rc = cb.main([str(tmp_path / "nope.md")])
    assert rc == 2
    assert "not found" in capsys.readouterr().err


# ── skill-side type-name reconciliation ────────────────────────

def test_normalize_type_mapping():
    # skill-side names map to the closest internal type
    assert cb._normalize_type("cc_handoff") == "handoff"
    assert cb._normalize_type("inquire") == "brief"
    assert cb._normalize_type("lock") == "brief"
    assert cb._normalize_type("notice") == "generic"
    assert cb._normalize_type("lesson") == "generic"
    assert cb._normalize_type("audit") == "generic"
    # internal types pass through unchanged
    for t in ("adr", "brief", "handoff", "generic"):
        assert cb._normalize_type(t) == t
    # unknown falls back to generic
    assert cb._normalize_type("nonsense") == "generic"


def test_cc_handoff_alias_equals_handoff():
    # The skill-side 'cc_handoff' name yields the same result as 'handoff'.
    assert cb.check_brief(HANDOFF, "cc_handoff") == cb.check_brief(HANDOFF, "handoff")


def test_skill_only_types_accepted_run_general_checks():
    # inquire/lock map to the general (brief) check set — a well-formed brief
    # passes HARD under them without argparse-dying or crashing.
    for t in ("inquire", "lock", "notice", "lesson", "audit"):
        v = cb.check_brief(WELL_FORMED, t)
        assert _hard(v) == [], f"{t}: {[str(x) for x in _hard(v)]}"


def test_main_cc_handoff_accepted_and_notes(tmp_path, capsys):
    p = tmp_path / "handoff.md"
    p.write_text(HANDOFF, encoding="utf-8")
    rc = cb.main([str(p), "--type", "cc_handoff"])
    assert rc == 0
    err = capsys.readouterr().err
    assert "skill-side" in err  # the partial-coverage note fired


def test_main_internal_type_no_skill_note(tmp_path, capsys):
    p = tmp_path / "handoff.md"
    p.write_text(HANDOFF, encoding="utf-8")
    rc = cb.main([str(p), "--type", "handoff"])
    assert rc == 0
    assert "skill-side" not in capsys.readouterr().err


# ── light-tier records (ADR 2026-08-08-adr-ceremony-tiering) ──

LIGHT_RECORD = """\
# ADR 2026-08-09 — a light decision

**Status:** `Accepted`
**Decision date:** 2026-08-09
**Tier:** light

## Decision
We do the thing.

## Grounds
Because of `docs/adr/whatever.md`.

## Gate
RESOLVED when it lands.

## Boundary
Do not widen this.
"""


def test_light_tier_record_is_not_checked():
    """A correctly-formed light record carries NO numbered sections. Applying
    the §0-§10 ADR contract reported 6 HARD violations on a valid record."""
    assert cb.is_light_tier(LIGHT_RECORD)
    assert cb.check_brief(LIGHT_RECORD, "adr") == []


def test_light_tier_detection_is_header_scoped():
    """An ADR *about* the tiering convention that quotes `**Tier:** light` in
    its body must NOT be treated as declaring itself light."""
    text = WELL_FORMED.replace(
        "## §1 — Context",
        "## §1 — Context\nThe convention requires `**Tier:** light` in the header.",
    )
    assert not cb.is_light_tier(text)
    # ...and it therefore still gets the real contract.
    assert cb.check_brief(text, "adr") == cb.check_brief(WELL_FORMED, "adr")


def test_full_tier_adr_still_checked():
    """Adversarial: light-tier bypass must not swallow ordinary ADRs."""
    broken = WELL_FORMED.replace("## §5 — Forbidden moves", "## §99 — Nothing")
    assert not cb.is_light_tier(broken)
    assert _hard(cb.check_brief(broken, "adr")), "a malformed full-tier ADR must still fail"


def test_type_closure_delegates_and_does_not_apply_general_contract(tmp_path, capsys):
    """`--type closure` must not argparse-die and must not run §0–§10."""
    p = tmp_path / "Q-X-closure-resolved.md"
    p.write_text("# Q-X — CLOSURE: `RESOLVED` (test)\n\n## Iterate\n- **Next:** INTEGRATE\n",
                 encoding="utf-8")
    rc = cb.main([str(p), "--type", "closure"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "DELEGATED" in out
    assert "check_closure_disposition.py" in out
    assert "well-formed" not in out
    assert cb.check_brief(p.read_text(encoding="utf-8"), "closure") == []
