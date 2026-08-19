# ADR 2026-08-19 — Persona hierarchy: a front/middle/back-office review panel over the GRAND/STRATEGIC loop tiers

**Status:** `Proposed`
**Decision date:** 2026-08-19
**Authors:** Joshua + Claude Code (design collaboration, 2026-08-18–19)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [three-loop binding](2026-06-12-three-loop-methodology-binding.md) (`Accepted` — extended one
tier of *scope*, not amended; same pattern the GRAND ADR itself used) ·
[GRAND tier](2026-08-09-grand-tier-quintessentials-binding.md) (`Accepted` — this ADR's panel reviews
GRAND-tier ratifications and strict-D2 STRATEGIC-tier Deletes, per that ADR's own §2.6/D2) ·
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

- Design spec — `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md` — anchor `ca01be3`
  2026-08-19 (post-ratification, all 4 confirmed BLOCKERs + 6 CONCERNs from its own adversarial review
  already fixed; Status `Accepted`).
- Three-loop binding ADR — `docs/adr/2026-06-12-three-loop-methodology-binding.md` — anchor `027a729`
  2026-08-14. D1 binds OODA=INNER / INQHIORI=OUTER / Algorithm=STRATEGIC; this ADR's panel sits above
  that binding, not inside it.
- GRAND tier ADR — `docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` — anchor `57d355e`
  2026-08-19. §2.6 cadence and D2's three Delete-execution channels are what this ADR's panel-trigger
  scope (§2 D1 below) is built against.
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
- `.claude/workflows/pre-ratification-adversarial-panel.js` — anchor `35b2a31` 2026-08-18. The
  existing mechanism this decision extends (persona-mode input branch already landed; lens/synthesis
  wiring not yet built — see design spec §11 and the panel-mechanics plan).
- `docs/personas/INDEX.md` — anchor `c0a30b8` 2026-08-19. The 19-file roster this ADR registers as
  doctrine already exists on disk.
- `docs/rule_0.md` — anchor `027a729` 2026-08-14.

**Provenance note.** The underlying design was substantively ratified in-session on 2026-08-19 (design
spec's own Ratification note — operator direct instruction, "Accepted on the design" / "Accepting the
proposal") and partially implemented (persona roster + ownership map shipped; panel-mechanics Task 1
shipped) *before* this ADR existed. That sequence is itself the gap this ADR corrects: the decision
was doctrine-shaped from the start (ceremony-tiering limb 4), but was ratified only on a
`docs/superpowers/specs/` surface, which CLAUDE.md's own standing-decision table never points to. This
ADR does not re-litigate anything already ratified — it registers that same decision on the surface
the repo's own tier test says it belonged on.

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
earlier in the review chain, not a new AI power to overrule the operator.

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

*(Restated compactly from design spec §10, which is the canonical, fuller version — kept in sync by
the audit hook in §10 below.)*

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
git log -1 -- docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md   # expect ca01be3 or later
git log -1 -- .claude/workflows/pre-ratification-adversarial-panel.js             # expect 35b2a31 or later

# CRO hard-block invariant text stays in sync between the design spec and CLAUDE.md
# (mirrors the LOCKED-strategy-table recall-guard pattern in ops/recall/guard.py)
grep -n "dry_run\|armed_until\|M1" CLAUDE.md docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md | grep -i "non-negotiable\|hard block"

# Ownership map has no remaining unconfirmed rows
grep -in "unconfirmed\|inferred by naming\|not yet run" docs/personas/ownership-map.md
# Expected: no hits (all closed as of 2026-08-19)
```

---

## Ratification note

*(Populated on operator ratification — not yet ratified as of authoring.)*

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
