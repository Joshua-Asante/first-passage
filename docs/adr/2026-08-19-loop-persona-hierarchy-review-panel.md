# ADR 2026-08-19 — Persona hierarchy: a front/middle/back-office review panel over the GRAND/STRATEGIC loop tiers

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-19, in-session direct instruction
("ratify the ADR"); see Ratification note
**Decision date:** 2026-08-19
**Authors:** Joshua + Claude Code (design collaboration, 2026-08-18–19)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [three-loop binding](2026-06-12-three-loop-methodology-binding.md) (`Accepted` — extended one
tier of *scope*, not amended; same pattern the GRAND ADR itself used; also the ADR whose own D2 defines
the three Delete-execution channels this ADR's "strict-D2 STRATEGIC-tier Deletes" trigger scope refers
to) ·
[GRAND tier](2026-08-09-grand-tier-quintessentials-binding.md) (`Accepted` — this ADR's panel reviews
GRAND-tier ratifications, per that ADR's own §2.6 cadence) ·
[ceremony tiering](2026-08-08-adr-ceremony-tiering.md) (limb-4 fires — see §0; this ADR's own tier
justification) · [design spec](../superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md) (the
content of record — this ADR is a pointer-tier registration, not a retelling, per CLAUDE.md's own
"ADRs carry pointers only, never a retelling")
**Layer:** meta-process (review mechanism over the loop tiers — governance-of-what-governs, same class
as the three-loop ADR's own declaration). **$0 / K=0.**
**Loop-of-Record:** STRATEGIC — binding a review mechanism to the GRAND/STRATEGIC tiers is
governance-of-what-governs, the same LoR class as the three-loop binding ADR's own declaration.

---

## §0 — Rule 0 reads (this worktree, 2026-08-19)

- Design spec — `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md` — anchor `47e3421`
  2026-08-19 (post-ratification, all 4 confirmed BLOCKERs + 6 CONCERNs from its own adversarial review
  already fixed; Status `Accepted`; §12/§13 added and the §13 rehearsal-count corrected during this
  ADR's own adversarial review).
- Three-loop binding ADR — `docs/adr/2026-06-12-three-loop-methodology-binding.md` — anchor `027a729`
  2026-08-14. D1 binds OODA=INNER / INQHIORI=OUTER / Algorithm=STRATEGIC; D2 defines the three
  Delete-execution channels (programme-audit cadence / fired stopping rule / explicit owner
  adjudication) that this ADR's "strict-D2 STRATEGIC-tier Deletes" trigger scope refers to; this ADR's
  panel sits above that binding, not inside it.
- GRAND tier ADR — `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` — anchor `57d355e`
  2026-08-19. §2.6's cadence (binds GRAND review to the existing quarterly programme-audit gate) is
  what this ADR's panel-trigger scope (§2 D1 below) additionally builds against for the GRAND-tier half
  of that scope.
- Ceremony-tiering ADR — `docs/adr/2026-08-08-adr-ceremony-tiering.md` — anchor `91e6caa` 2026-08-15.
  **Tier test applied directly:** limb 1 (spends K/money) — no, $0/K=0. Limb 2 (touches a live-risk
  surface) — arguable but not decisive: the CRO hard-block (design spec §6.3) references but does not
  modify `dry_run`/M1/arming invariants. Limb 3 (alters a LOCKED surface) — no, explicitly out of scope
  (design spec §2). **Limb 4 (creates or amends doctrine: a rule, gate, falsifier threshold, or
  convention that binds future work) — fires unambiguously**: this decision creates a new review gate
  for GRAND/STRATEGIC decisions, a new CRO hard-block rule, and a new falsifier threshold (design spec
  §10, N=3) that bind all future work at those tiers. One limb firing is sufficient; per the
  ceremony-tiering ADR's own escalation rule ("ambiguous tier → FULL"), this is unambiguously
  **full-tier**, not light.
- CLAUDE.md — anchor `d88e5f2` 2026-08-15. §Standing decision table has no row for this decision as of
  this anchor — the gap this ADR closes.
- `.claude/workflows/pre-ratification-adversarial-panel.js` — anchor `84a941a` 2026-08-19. The
  existing mechanism this decision extends. Persona-mode input branch, persona-driven lens list, the
  CRO safety-invariant hard block, and the frozen-artifact precondition gate are all now built and
  wired into run/synthesis/return (panel-mechanics plan, all 3 tasks); a live GRAND-tier rehearsal has
  already run against the closed GSUB-1 inventory (design spec §13) and this ADR's own adversarial
  review (§0 note below) found and fixed a real fail-open defect in the CRO hard-block before merge.
- `docs/personas/INDEX.md` — anchor `c0a30b8` 2026-08-19. The 19-file roster this ADR registers as
  doctrine already exists on disk.
- `docs/rule_0.md` — anchor `027a729` 2026-08-14.

**Amendment-first / dedup (executed this session, backfilled 2026-08-19 — Rule 8 sub-rule 10 was in force as of 2026-08-15 and was omitted at original authoring):**

```
$ python scripts/check_advisor_dedup.py --keywords "persona hierarchy review panel front middle back office"
check_advisor_dedup: keywords: 'persona hierarchy review panel front middle back office'
  slugs found:    (none)
  keywords found: 8 significant terms

POSSIBLE PRIOR ART — review before treating the keywords as new work (top 8 of 51 candidate(s)):

  [  6] docs/briefs/closures/GSUB-2-closure-resolved-loadbearing.md — GSUB-2 — CLOSURE: `RESOLVED-LOADBEARING` (2 ratified dispositions differ from PARK)
        shared terms: ['front', 'hierarchy', 'office', 'panel', 'persona', 'review']

  [  3] docs/notes/audits/2026-07-12-08-08-classA-reachability-audit.md — Audit — gate reachability of the ratified 08-08 Class-A slate
        shared terms: ['back', 'panel', 'review']

  [  3] docs/notes/audits/2026-08-08-conventions-delete-phase-gap-audit.md — Conventions friction — Delete-phase gap audit — 2026-08-08
        shared terms: ['back', 'panel', 'review']

  [  3] docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md — Audit Note — Strategy-generation pipeline assumptions sweep
        shared terms: ['back', 'panel', 'review']

  [  3] docs/notes/audits/programme-audit/2026-07-01-cross-layer-synthesis.md — Cross-layer synthesis — 5-week programme audit (2026-05-27 → 2026-07-01)
        shared terms: ['back', 'panel', 'review']

  [  3] docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md — Audit Note — Object-layer audit: `core/` conclusions vs the retired FXIFY/CFD ground truth
        shared terms: ['back', 'panel', 'review']

  [  3] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/03-agent-facing.md — §3 — Agent-facing findings (round 2)
        shared terms: ['hierarchy', 'panel', 'review']

  [  3] docs/notes/audits/programme-audit/2026-08-05-claim-alignment/04-misleading.md — §4 — MISLEADING (not agent-facing)
        shared terms: ['front', 'panel', 'review']
```

Catalog-surface grep (sub-rule 8/10 attestation surfaces; `check_advisor_dedup.py` does not search `docs/adr/` or `docs/superpowers/`):

```
$ rg -n -i "persona hierarchy|persona-hierarchy|review panel" lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
(no matches)
```

**Judgment:** no prior owner exists on the three sub-rule 8/10 surfaces (`lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/rejected_candidates.md`). The `[6]` GSUB-2 closure hit is a same-day *downstream consumer* of this ADR (it used the panel this ADR registers), not an existing owner that should have taken an addendum. The remaining score-3 hits share generic tokens (`back`/`panel`/`review`) with unrelated audits. The existing owners are this ADR itself (amend-in-place) and the design spec it registers (`docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`). Nothing is re-derived.

**Provenance note.** The underlying design was substantively ratified in-session on 2026-08-19 (design
spec's own Ratification note — operator direct instruction, "Accepted on the design" / "Accepting the
proposal") and partially implemented (persona roster + ownership map shipped; panel-mechanics Task 1
shipped) *before* this ADR existed. That sequence is itself the gap this ADR corrects: the decision
was doctrine-shaped from the start (ceremony-tiering limb 4), but was ratified only on a
`docs/superpowers/specs/` surface, which CLAUDE.md's own standing-decision table never points to. This
ADR does not re-litigate anything already ratified — it registers that same decision on the surface
the repo's own tier test says it belonged on.

**Self-review note.** Before ratification, this ADR (and the code/docs it registers) went through a
4-dimension adversarial review (JS-logic, ADR-citation-accuracy, checker-logic,
ground-truth-consistency reviewers, each independently skeptic-verified). Agent count was reported as
32; that figure is as-reported — no workflow run ID or journal path was preserved in-tree (searched
the authoring commit `5d11cf8`, PR #56 body, persona logs, and `docs/SESSIONS.md`; none carry a
`wf_*` id for this review, unlike the sibling convention at
[`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`](../notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md)
§0). It found and fixed: a real fail-open defect in the CRO hard-block (fires:false when CRO's own
review agent failed, indistinguishable from a genuinely clean review), a misattributed ADR citation
(D2 belongs to the three-loop-binding ADR, not the GRAND-tier ADR — corrected above), a §10 audit
hook that could structurally never match CLAUDE.md, and several smaller staleness/accuracy gaps in
this file and the design spec. None of the underlying decisions (D1–D5) changed; only citation
accuracy and code robustness.

---

## §1 — Context

The loop-tier doctrine (three-loop binding + GRAND tier ADRs) answers *who has authority to decide
what*. It says nothing about *who argues which side before a decision gets made* — GRAND and
STRATEGIC-tier verdicts have historically been single-session, single-voice recommendations (or, for
generic doc/ADR ratification, the existing `pre-ratification-adversarial-panel`'s 6 generic lenses).
The design spec (§1) proposes a stable, front/middle/back-office-framed persona roster, spawned as
literal subagents with SEC-18f-4/SR-11-7-style independence, to review GRAND ratifications and
strict-D2 STRATEGIC-tier Deletes specifically.

---

## §2 — Decision

**D1 — Adopt the persona hierarchy as the review mechanism for GRAND ratifications and strict-D2
STRATEGIC-tier Deletes.** Three persona layers (C-suite / Senior Managers / Staff), deliberately
decoupled from the 4-tier loop-count — full roster, independence mechanics, and trigger scope live at
the design spec §§3–7; the 19-file roster is already built at `docs/personas/`. **Not** triggered by
the frequent OUTER-tier campaign closures (design spec §4) — panel cost stays proportionate to stakes.

**D2 — Extend, not replace.** The panel is an opt-in mode on the existing
`pre-ratification-adversarial-panel` workflow (persona-mode input branch already landed,
`.claude/workflows/pre-ratification-adversarial-panel.js`), not new parallel infrastructure. Every
existing non-persona-mode caller is unaffected (verified via a live regression run, 2026-08-19).

**D3 — The CRO safety-invariant hard-block restates existing doctrine; it grants no new authority.** A
CRO dissent citing a CLAUDE.md non-negotiable (`dry_run`/M1/`armed_until`) is a hard block on panel
synthesis (design spec §6.3) — this is the existing non-negotiable set, mechanically enforced one layer
earlier in the review chain, not a new AI power to overrule the operator. Two distinct claims, not one:
the *procedural gate* (checking for this citation before synthesis, in code) is novel — this is exactly
what §0's limb-4 firing is about — while the *underlying safety invariant it enforces* is not novel and
grants no new authority. A new gate over an old rule is still governance-of-what-governs, not new
substantive power.

**D4 — The repo's contents are divided among the roster.** `docs/personas/ownership-map.md`
(directory skeleton + all 38 `docs/pursuits/` records classified) gives every future decision or new
artifact a first-line owner without re-deriving one. Ownership means first-line reviewer/delegate, not
modification authority — locked-parameter authority is untouched (design spec §2, ownership map's own
opening line).

**D5 — Joshua decides, always.** No AI persona gains independent authority to execute a GRAND Subtract
or a STRATEGIC Delete (design spec §2). The D-user-gate (`inqhiori-canon.md` L284) is unchanged; panels
produce advisory synthesis for the CEO seat, which is never spawned.

---

## §3 — Alternatives considered

Full treatment at design spec §8 (same-session multi-voice, full bespoke build, fixed fan-out to a
target org-chart shape, a Manager persona layer, persona-per-pursuit instances) — not retold here per
CLAUDE.md's pointer-only instruction. Summary: every alternative was rejected either for failing the
independence principle this design is built on, or for reproducing the "belt that only grows" pattern
GSUB-1's own retrospective flagged.

---

## §4 — Falsifiable hypothesis

**H:** Across the first 3 real (non-rehearsal) GRAND or STRATEGIC panel uses, at least one panel run
changes what Joshua would have ratified without it — a confirmed BLOCKER, a CRO hard-block, or a
preserved dissent that alters the disposition.

**Falsifier:** 3 consecutive real panel uses that each produce zero decision-difference falsifies the
panel as load-bearing. Disposition on falsification: demote to a lighter, non-panel review path via a
superseding record — never silent retention.

**Trigger check schedule:** at the 3rd real panel use, or the next quarterly programme-audit gate
(2026-11-08), whichever comes first — same cadence the GRAND ADR's own §4 re-read uses, not a new one.

*(Restated compactly from design spec §10, which is the canonical, fuller version — manually kept in
sync at authoring time; re-check both on any future edit to either document's falsifier terms.)*

---

## §5 — Forbidden moves (genuinely tempting)

- **Using this ADR to relitigate any locked parameter, allocation, `dd_protection` constant, MC
  calibration, or campaign pre-registration** — the panel's downward interface is scoping/review
  authority only (design spec §2), same guard the GRAND ADR's own §2.4 domain table already enforces
  one tier down.
- **Reading the CRO hard-block (D3) as a new grant of AI authority** — it is a restatement of an
  existing non-negotiable, enforced deterministically in code (panel-mechanics plan Task 2), not a new
  power.
- **Letting a persona panel's synthesis substitute for the D-user-gate** — panels are advisory without
  exception; skipping operator ratification because "the panel already reviewed it" is exactly the
  failure this forbidden move exists to name before it happens.
- **Skipping the frozen-artifact precondition (design spec §6.1)** to save a round-trip — a
  live-back-and-forth review is the exact independence failure (Kerviel/Adoboli-shaped) this whole
  design exists to prevent.
- **Treating this ADR's registration as re-opening ratification** of anything already decided — the
  design, the roster, and the ownership map stay exactly as already accepted; this ADR moves them onto
  the correct doctrine-tier surface, it does not re-litigate their content.

---

## §6 — Gate (binary)

- **PROPOSED → ACCEPTED** requires: §0 populated with anchors (done, this commit) · operator
  ratification of *this ADR specifically* (distinct from the design spec's own prior informal
  acceptance — the ceremony-tiering ADR's full-tier apparatus gets its own explicit ratification, not
  an inherited one) · `python scripts/check_brief.py <this file> --type adr` passing · `python
  scripts/check_adr_graph.py` passing.
- **ACCEPTED same-commit downstream updates:** `CLAUDE.md` §Standing decision table gains a pointer
  row · `docs/adr/INDEX.md` regenerated via `check_adr_graph.py --regenerate-index` (never hand-edited,
  per that file's own header) · design spec gains a one-line cross-reference addendum in its own Change
  History section pointing at this ADR (not a rewrite of any ratified content).
- **REJECTED / AMBIGUOUS:** named defect, returns for re-authoring. No silent amendment mid-review.

---

## §10 — Audit hooks (runnable)

```bash
# Discipline checks
python scripts/check_brief.py docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md --type adr
python scripts/check_adr_graph.py

# Rule-0 anchor spot-check
git log -1 -- docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md   # expect 47e3421 or later
git log -1 -- .claude/workflows/pre-ratification-adversarial-panel.js             # expect 84a941a or later

# CRO hard-block invariant text stays in sync between CLAUDE.md and the design spec --
# two independent checks (a single-line grep pipeline can't span CLAUDE.md's own
# heading-to-bullet structure, since the two required patterns land on different lines there;
# mirrors the LOCKED-strategy-table recall-guard pattern in ops/recall/guard.py in spirit)
grep -A5 "Safety invariants (non-negotiable)" CLAUDE.md | grep -q "dry_run\|armed_until\|M1" && echo "CLAUDE.md: safety invariants present"
grep -A3 "non-negotiable" docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md | grep -q "dry_run\|armed_until\|M1" && echo "design spec §6.3: safety invariants cited"

# Ownership map has no remaining unconfirmed rows
grep -in "unconfirmed\|inferred by naming\|not yet run" docs/personas/ownership-map.md
# Expected: no hits (all closed as of 2026-08-19)
```

---

## Ratification note

**Ratified by:** Joshua, in-session direct instruction — *"ratify the ADR"* (2026-08-19). Authority
channel: explicit owner adjudication.

**§6 preconditions at ratification:** §0 populated with anchors (done, authoring commit) ✓ · operator
ratification of this ADR specifically (this note — distinct from the design spec's own prior informal
acceptance, per §6's own instruction) ✓ · `python scripts/check_brief.py
docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md --type adr` → `RESULT: well-formed` (0 HARD,
0 WARN) ✓ · `python scripts/check_adr_graph.py` → `OK` ✓.

**§6 ACCEPTED same-commit downstream updates (this commit):** `CLAUDE.md` §Standing decision table
gains a pointer row · `docs/adr/INDEX.md` regenerated via `check_adr_graph.py --regenerate-index` ·
design spec (`docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`) gains a one-line
cross-reference addendum in its own Change History pointing at this ADR.

**Not licensed by this ratification:** anything §5's forbidden moves already exclude — this ratifies
the *registration* of the persona-hierarchy panel as GRAND/STRATEGIC-tier doctrine; it does not itself
convene a panel or dispose of any pursuit. The first real (non-rehearsal) panel use is a separate,
subsequent act, per design spec §13's own distinction between rehearsal and real data points toward
§4's falsifier.

---

## Addendum 2026-08-19 (same day, later) — D1's design-spec pointer is a snapshot, not a live range

**Does not amend §2.** Citation-scope clarification only, found by the §6.6 pre-ratification
adversarial panel (see the design spec's own §6.6 Status line for the full finding).

D1 says the design spec's "§§3–7" carries "full roster, independence mechanics, and trigger scope."
Read unqualified, that range would sweep in any section added later under the same numbers — but
this ADR ratifies the design spec **as it stood at the ratification commit (`66410ed`)**, not as a
live-updating range. A section added to the design spec after that commit under a §-number inside
3–7 (e.g. `§6.6`, drafted afterward at `2dd34ae`) is **not** ratified by D1 and needs its own
separate ratification before it governs anything — the same rule the design spec's §11 applied to
whether *this* decision needed a formal ADR (now closed; this ADR is that resolution). This is a standing
reading rule for this ADR going forward, not a one-time fix: **the "§§3–7" pointer in D1 means the
2026-08-19 ratified content of those sections, not whatever they contain when a reader looks later.**

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md --type adr
python scripts/check_adr_graph.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-19 | Initial authoring — registers the already-ratified persona-hierarchy decision on the doctrine-tier surface the ceremony-tiering ADR's own limb-4 test says it belongs on | Claude Code (drafted at operator request, judged beneficial per the ceremony-tiering tier test — see §0) |
| 2026-08-19 | Self-review pass (32-agent, 4-dimension adversarial review, see §0 Self-review note): corrected D2's misattribution (three-loop-binding ADR, not GRAND ADR), fixed the §10 CRO-invariant grep that could never match CLAUDE.md, softened §4's unsupported "kept in sync by audit hook" claim, refreshed §0's design-spec and workflow-JS anchors past their own initial staleness, clarified D3's new-gate-vs-no-new-authority distinction. Same review also fixed a real fail-open CRO hard-block defect in the workflow JS itself (commit 84a941a) and a BLOCKER-undercount in the design spec's §13 (commit 47e3421) — logged there, not here, since neither is this ADR's own content. | Claude Code |
| 2026-08-19 | Ratified `Proposed` → `Accepted` (operator in-session instruction, "ratify the ADR"; Ratification note populated). §6 ACCEPTED downstream updates landed same commit: `CLAUDE.md` standing-decision pointer row, `docs/adr/INDEX.md` regenerated, design spec cross-reference addendum. | Joshua + Claude Code |
| 2026-08-19 | Addendum added — D1's "§§3–7" design-spec pointer clarified as a snapshot at ratification, not a live range, so a later same-numbered addition (§6.6) isn't read as already-ratified. Found by the §6.6 pre-ratification adversarial panel (44 agents, 6 lenses, workflow run `wf_88c21d8d-a7f`). | Claude Code |
| 2026-08-19 | Backfilled Rule 8 sub-rule 10 dedup-first attestation into §0 (omitted at original authoring; in force since 2026-08-15). Marked the Self-review "32 agents" figure as-reported — run artifacts were not preserved. Found by the 2026-08-19 §6.6 adversarial panel (`wf_88c21d8d-a7f`) as a pre-existing regression, not caused by §6.6. | Claude Code |
