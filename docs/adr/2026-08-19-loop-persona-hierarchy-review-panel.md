# ADR 2026-08-19 — Persona hierarchy: a front/middle/back-office review panel over the GRAND/STRATEGIC loop tiers

> ⚠ **Fully superseded 2026-08-31.** The entire persona-hierarchy system this ADR stood up —
> including the Front-Office-only roster the 2026-08-21 partial-supersession below preserved — is
> retired. `docs/personas/` is deleted from the live tree; no persona is spawnable. See
> [`2026-08-31-persona-hierarchy-full-retirement.md`](2026-08-31-persona-hierarchy-full-retirement.md)
> for the decision and rationale. This ADR's text below is left unedited as the historical record
> of what was ratified 2026-08-19 — read it as history, not as a current description of anything
> live.

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-19, in-session direct instruction
("ratify the ADR"); see Ratification note
**Decision date:** 2026-08-19
**Authors:** Joshua + Claude Code (design collaboration, 2026-08-18–19)
**Supersedes:** none
**Superseded-by:** `2026-08-31-persona-hierarchy-full-retirement.md` — in full (this ADR's entire
remaining decision, including the 2026-08-21 partial supersession below, is retired)
**Superseded-in-part-by:** `2026-08-21-persona-hierarchy-front-office-only.md` — D1's spawnable
roster (narrowed to Front Office + CEO apex + cross-office CFO; the six Middle/Back-office
C-suite/Senior-Manager seats and their two Back-office Staff retired to mechanical gates) and D3's
*implementation* of the CRO safety-invariant hard-block (now a standalone deterministic scan, not
conditional on a spawned CRO persona). D2, D4's delegation mechanism, D5, and the GRAND/STRATEGIC
trigger scope are untouched — see the addendum below. Historical record only as of 2026-08-31 (see
the full-supersession notice above).
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

**Follow-up, same day: §6.6 has now separately cleared that bar.** After two rounds of adversarial
review (full panel `wf_88c21d8d-a7f`, `BLOCKED` then fixed; targeted recheck `wf_8d2086b0-27d`,
which found one fix inadequate and prompted a structural redesign) Joshua ratified §6.6 directly
("ratify now"), per its own Status line. D1's "§§3–7" pointer still means the 2026-08-19-at-`66410ed`
snapshot, unchanged — §6.6's ratification is a separate act, recorded on the design spec's own
Status line and Change History, not a retroactive widening of what D1 itself covers.

---

## Addendum 2026-08-19 (later) — self-review evidentiary status: the design spec's §6.6 claim, and D2

**Does not amend §0–§6, §10, D1–D5, or the Ratification note.** Originally drafted broader, from a
packet-wide adversarial review of the design spec (46 agents, 2026-08-19) that also covered this
ADR. **Narrowed on merge** with a parallel fix (PR #59, `cursor/persona-hierarchy-spec-staleness-
1583`) that landed on `main` first and already covers most of the same ground directly in §0 above:
a retroactive Rule 8 sub-rule 10 dedup-first attestation (executed via `check_advisor_dedup.py`,
more rigorous than this addendum's own manual grep would have been) and a softened "32 agents"
figure on this ADR's own ratification self-review. That fix is kept as-is rather than duplicated
here. What it did **not** reach — a *different* self-review event, and D2 — is what this addendum
still covers.

**The design spec's own §6.6 Change History claims a "44 agents, 6 lenses... workflow run
`wf_88c21d8d-a7f`," disposition `BLOCKED`, "6 confirmed BLOCKERs," and a "targeted recheck
(workflow `wf_8d2086b0-27d`)"** — a separate review, of the §6.6 subsection specifically, distinct
from this ADR's own "32 agents" ratification self-review that PR #59 already addressed. A
repo-wide search for both workflow IDs returns hits only inside the design spec's own prose — no
`journal.jsonl`, per-lens findings file, or persona-log entry anywhere records either run's actual
output. What *is* independently checkable: the specific content changes those claims describe
landed as real, inspectable commits — `eba0701` ("§6.6 panel found BLOCKED -- 6 confirmed
BLOCKERs, fixed"), `8e19126` ("targeted recheck confirmed fix 3 still open; redesign it"),
`bc8d828` ("§6.6 cross-examination round Proposed -> Accepted") — each with a real diff matching
its message, confirmed via `git log`. **Disposition: downgrade the framing from "a scored N-agent
panel verdict" to "an editorial self-review pass of unconfirmed scale/mechanism, whose resulting
content changes are independently verifiable in the commit history."** This does not reopen §6.6's
`Accepted` status (Joshua ratified it directly, "ratify now" — a separate, sufficient authority
channel under D5 that never depended on the self-review's scale claims being true) or retroactively
invalidate any of the content fixes the self-review produced (those stand on their own merits,
checkable in the diff, independent of how the review that found them is described).

**Same gap, same fix, for D2 above.** D2's "verified via a live regression run, 2026-08-19" claim
has the identical evidentiary shape — no test log or session record anywhere shows this run
happened. Partially mitigated, as the packet-wide review itself noted: `.claude/workflows/
pre-ratification-adversarial-panel.js` structurally gates persona-mode logic behind
`if (personaMode)` (confirmed by direct read), so a non-persona-mode caller plausibly does fall
through unchanged — but that is code-reading, not a shown run. Read D2's regression claim as
"structurally supported by code inspection," not as a scored test result.

---

## Addendum 2026-08-19 (later still) — roster/spec simplification pass; D1's counts now stale by design

**Does not amend §0–§7, §10, D1–D5, or the Ratification note.** D1's "the 19-file roster is already
built" (§2 above) and the design spec's own "18 spawnable personas" / "8 named, persistent Staff"
language are now stale **on purpose**, not by drift: an operator-authorized simplification pass, the
same day as ratification, per
[`docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md`](../notes/audits/2026-08-19-governance-friction-persona-panel-audit.md),
archived seven never-executed spec extensions (§6.3's dissent-flag addendum, §6.4.1, §6.6, §10.1,
§10.2, §12's extended log fields, §14) to
`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`, and moved 5 of
the 8 Staff-tier personas (the Middle/Back-office analysts — Risk Analyst (Intraday), Model
Validation Analyst, Robustness Analyst, Documentation Analyst, Research Registry Analyst; all zero
real log entries) to `docs/personas/archive/` per the design spec's own §6.7 retirement procedure.
The active roster was 14 files, not 19, immediately after this pass — **corrected same day, see the
addendum below: 16, after operator pushback restored 2 of the 5 archived Staff analysts on tested
evidence.** Front-office Staff (Falsifier Analyst, Pre-Registration Analyst, TCA Analyst) were
explicitly excluded from the cut throughout — in active use in a parallel session — and are
unaffected, as is the CRO hard-block and the GRAND tier.

**Independent check on the audit itself.** A fresh-spawned Head of Governance pass (first-ever spawn
for that seat — `docs/personas/head-of-governance-log.md` did not exist before this) independently
re-verified the audit's headline claims against the live repo (catching and correcting two small
figures) and confirmed all seven archival candidates' factual predicates. It also flagged, without
softening it for being its own seat's use, that this review was not itself triggered by a literal
strict-D2 STRATEGIC-tier pursuit Delete (this action touches no `docs/pursuits/` object) and marked
its own entry `Rehearsal: yes` for that reason.

**What this does not do.** No content in §0–§7, §10, or D1–D5 changed; nothing here reopens the
GRAND/STRATEGIC panel decision itself, the CRO hard-block, or any prior addendum's findings. This is
the same class of edit as the two addenda above — a correction/scope-clarification to what the
ratified decision's supporting artifacts now say, landed via addendum per this file's own
established convention, not a re-litigation of D1.

---

## Addendum 2026-08-19 (later still, again) — operator pushback; 2 archived items restored, 1 sharpened, rest confirmed blocked

**Does not amend §0–§7, §10, D1–D5, the Ratification note, or either addendum above.** Before this
branch merged, operator pushback on the simplification pass above: "push back on archiving all of
the spec extensions and STAFF personas, because they are brand new and haven't had a chance to be
used yet... test them to see if they would earn their keep based on existing evidence we have in the
repo." Re-tested every archived item against real repo evidence rather than leaving "never fired"
unexamined — full account in
[`docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md`](../notes/audits/2026-08-19-governance-friction-persona-panel-audit.md)'s
Disposition section. Net: §14 MAST restored (run for real against GSUB-2's preserved journal, found
2 genuine findings); §10.2 self-consistency discharged, not restored (run for real, logged);
§6.3's dissent flag stays archived on stronger evidence (tested, produced a false positive); §6.6,
§6.4.1, §10.1 confirmed genuinely blocked on data, not deprioritized. Of the 5 archived Staff
analysts, 2 (Documentation Analyst, Research Registry Analyst) each found a genuine,
previously-uncaught defect in the audit note itself on first spawn — restored. The other 3 came back
clean against a mismatched test target — inconclusive, stay archived. **Active roster is now 16
files**, not 14. `check_personas.py`'s `EXPECTED_COUNT` updated 14 → 16.

---

## Addendum 2026-08-21 — partially superseded: roster narrowed to Front Office

**Does not amend §1–§2's D2/D4/D5, §5, §6, §10, or the Ratification note.** Operator direct
instruction, in-session: First Passage is primarily a research entity, with deployment as a means of
validating that research; it does not need a standing Middle/Back-office persona roster with its own
reporting chains, only middle/back-office *services*. Recorded as a partial supersession, per
[`2026-08-21-persona-hierarchy-front-office-only.md`](2026-08-21-persona-hierarchy-front-office-only.md)
(see this file's own header `Superseded-in-part-by` line above for the exact clause scope).

**What changed:** D1's roster narrows from 19-file/16-file/17-file (this file's own count churned
same-day and again 2026-08-20 — see change history) to 9: Front Office (CIO, Head of Research, Head
of Execution, Falsifier Analyst, Pre-Registration Analyst, Research Analyst, TCA Analyst) plus the
CEO apex and cross-office CFO, both explicitly confirmed out of scope for this cut. The six retired
Middle/Back-office seats' functions continue running as mechanical gates (2026-08-21 ADR's §2 D2
table), not LLM spawns. D3's CRO hard-block is re-implemented as a standalone deterministic scan of
the target artifact's own text, unconditional on any persona spawn — its underlying claim (restates
existing doctrine, grants no new AI authority) is unchanged and not superseded.

**What did not change:** D2 (extend the existing panel workflow, never replace) · D4's ownership-map
delegation *mechanism* (rows reassigned to the mechanical gates per the new ADR, not the mechanism
itself abolished) · D5 (Joshua decides, always) · the GRAND/STRATEGIC panel trigger scope (GRAND
ratifications + strict-D2 STRATEGIC-tier Deletes) · this ADR's own §4 falsifier (the whole-panel
mechanism question) and its 2026-11-08/3rd-real-use trigger schedule, tracked independently of the
new ADR's own narrower §4.

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
| 2026-08-19 | Backfilled Rule 8 sub-rule 10 dedup-first attestation into §0 (omitted at original authoring; in force since 2026-08-15). Marked the Self-review "32 agents" figure as-reported — run artifacts were not preserved. Found by the 2026-08-19 §6.6 adversarial panel (`wf_88c21d8d-a7f`) as a pre-existing regression, not caused by §6.6. | Claude Code (PR #59, `cursor/persona-hierarchy-spec-staleness-1583`) |
| 2026-08-19 | Addendum added — self-review evidentiary status for the design spec's *separate* §6.6 self-review claim ("44 agents... workflow run `wf_88c21d8d-a7f`," "6 confirmed BLOCKERs") and D2's "live regression run" claim, both with no recoverable artifact anywhere in the repo — downgraded in framing to "editorial pass, unconfirmed scale" while leaving the underlying, independently-checkable content changes (real commits, verified via `git log`) untouched. Originally drafted broader, from a packet-wide adversarial review (46 agents) of the design spec that also covered this ADR; narrowed on merge with the parallel PR #59 fix above, which already covers this ADR's own dedup gap and ratification self-review — not duplicated here. Neither correction reopens §6.6's `Accepted` status or D1-D5. | Claude Code (drafted at operator request, following this file's own prior-addendum precedent — correction/clarification, no re-litigation, no fresh ratification act required) |
| 2026-08-19 | Addendum added — roster/spec simplification pass makes D1's "19-file roster" pointer stale by design: 7 never-executed spec extensions archived (not deleted) to `docs/superpowers/specs/archive/`, 5 of 8 Staff-tier personas (never spawned, zero log entries) retired to `docs/personas/archive/` per the design spec's own §6.7, active roster now 14 files. Driven by `docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md` plus an independently-spawned Head of Governance review that flagged its own use as outside its literal strict-D2 trigger. Front-office Staff and the CRO hard-block unaffected. | Claude Code (operator-authorized) |
| 2026-08-19 | Addendum added — operator pushback before merge, re-tested every archived item against real repo evidence. §14 MAST restored (2 genuine findings on real re-run); §10.2 discharged (run for real, not restored to spec text); §6.3 stays archived on stronger evidence (tested, produced a false positive); §6.6/§6.4.1/§10.1 confirmed genuinely blocked on data. 2 of 5 archived Staff analysts (Documentation Analyst, Research Registry Analyst) restored after each found a real, previously-uncaught defect in the governing audit note on first spawn. Active roster now 16 files, not 14. | Claude Code (operator-authorized, after operator pushback) |
| 2026-08-21 | Header field `Superseded-in-part-by` set + addendum added — operator direct instruction narrows D1's spawnable roster to Front Office (+ CEO apex, cross-office CFO), retiring six Middle/Back-office seats and their two Back-office Staff to mechanical gates; D3's CRO hard-block re-implemented as a standalone deterministic scan. See [`2026-08-21-persona-hierarchy-front-office-only.md`](2026-08-21-persona-hierarchy-front-office-only.md). D2, D4's mechanism, D5, and this ADR's own §4 falsifier/trigger schedule are unaffected. | Joshua + Claude Code |
