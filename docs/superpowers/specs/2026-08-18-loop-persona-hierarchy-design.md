# Persona Hierarchy for the GRAND/STRATEGIC Loop Tiers — Design Spec

**Date:** 2026-08-18
**Status:** Draft — pending Joshua's review of this file
**Author:** Claude Code, design collaboration with Joshua (brainstorming session, 2026-08-18)

## 1. Purpose

First Passage's loop-tier doctrine (GRAND/STRATEGIC/OUTER/INNER — see
`docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` and
`docs/adr/2026-06-12-three-loop-methodology-binding.md`) answers *who has the authority to decide
what*. It says nothing about *who argues which side before a decision gets made*. This spec adds a
persona layer on top: a stable roster of named roles, framed as a front/middle/back-office trading
firm, that get spawned as real subagents to review GRAND and STRATEGIC-tier decisions before Joshua
ratifies them — replacing a single-voice recommendation with independent, structurally-separated
review.

The motivating principle, grounded in real trading-firm practice (research below): **the person who
proposes a decision should never be the person who validates it.** Real firms enforce this through
reporting-line independence (SEC Rule 18f-4: a fund's risk manager "may not be a portfolio manager
of the fund"; Fed SR 11-7: model validation must be organizationally independent from model
development). The documented failure mode when this collapses — Barings/Leeson, Société
Générale/Kerviel, UBS/Adoboli — is one person holding both a front-office and a control-adjacent
role, supervising their own risk. This design borrows the mechanism, not just the vocabulary.

## 2. Scope boundary — what this does NOT change

This is an overlay. It does not touch:

- **The 4-tier loop doctrine** (GRAND/STRATEGIC/OUTER/INNER) or its authority rules — the D-user-gate
  (`docs/methodology/inqhiori-canon.md` L282: Claude proposes, Joshua authorizes), D2/D3 no-borrowing
  (`docs/adr/2026-06-12-three-loop-methodology-binding.md`). Personas are a *different axis*: how many
  named review seats exist and what they argue, not who is allowed to execute what.
- **The CC/Cursor surface-allocation ADR** (`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`) —
  orthogonal axis (execution surface vs. decision authority). Cursor's role in this design (§5.3) is
  exactly its existing role under `cursor-fleet`, not a new one.
- **c1 Q-XMEM-1** (the parked cross-surface memory sidecar pilot) — persona memory (§6.4) is a
  narrower, distinct mechanism (a plain per-persona markdown log read/written by this panel
  mechanism only). It is not a general cross-surface visibility system and does not revive that
  parked pursuit or its re-entry armor.
- **No AI persona gains independent authority to execute a GRAND Subtract or a STRATEGIC Delete.**
  Panels are advisory. Joshua decides, always — with one narrow exception (§6.3) that restates an
  existing non-negotiable, not a new grant of authority.

## 3. Architecture

**Three persona layers, not four** — deliberately decoupled from the loop-tier count:

| Persona layer | Loop-tier work it covers | Cardinality |
|---|---|---|
| **C-suite** | GRAND | 5 seats (§5.1) |
| **Senior Managers** | STRATEGIC | 6 seats, grouped front/middle/back office (§5.2) |
| **Staff** | OUTER + INNER | 8 permanent personas + Cursor's existing ephemeral worker pool (§5.3) — most OUTER/INNER work stays unnamed |

Real front/middle/back office structures have 2-3 levels of depth per office (C-suite →
department-head → staff/analyst) — three levels, not four (research citations in §9). Forcing 1:1
symmetry with the loop-tier count was an early draft mistake, corrected during this design session.

**Mechanism:** personas are literal subagents, spawned via the Workflow/Agent tooling, not
documentation labels or a prompting lens someone silently adopts. This extends the existing
`pre-ratification-adversarial-panel` skill — reviewer lenses become the named personas below instead
of generic adversarial framings — rather than building new parallel infrastructure.

## 4. Trigger and cadence

A panel convenes on:

1. **Every GRAND-tier ratification** — any Subtract / Park / Merge / Keep proposal reaching its
   Phase-3-style ratification point (the same shape as GSUB-1's own Phase 3).
2. **Strict-D2 STRATEGIC-tier Deletes only** — programme/track/instrument-tier kills, per the three-loop
   ADR's own D2 definition. **Explicitly not** every OUTER-tier campaign closure (TRAINKILL-,
   Q-EXPR-, Q-CONDVAL-style dispositions) — those are frequent (several per week on current
   evidence) and keep their existing, lighter adjudication path untouched. Conflating the two would
   multiply panel cost by roughly an order of magnitude for no rigor gained at the OUTER tier.

**Who gets spawned, per trigger:**

- *GRAND:* the office(s) the pursuit's domain touches (mandatory) **plus CRO on every single GRAND
  decision, with no exceptions** — risk review isn't skippable because a pursuit looks unrelated to
  risk on its face. This is how the GRAND ADR's own forbidden-move #1 ("relitigating a lower-tier
  risk-control constant") gets caught in practice, not just prohibited on paper.
- *STRATEGIC:* the proposing office (1st line, owns/operates) + at least one other office as
  independent challenge (2nd line) — Three Lines of Defense shape, documented challenge rather than a
  majority vote.

## 5. Roster

### 5.1 GRAND tier — C-suite

| Seat | Owner | Domain | Spawned as agent? |
|---|---|---|---|
| **CEO** | Joshua | Aim; sole GRAND ratification authority; sole owner-adjudication channel for STRATEGIC-tier Deletes (D2 channel c); sets the Survive bound; final word on every panel's synthesis | **Never — this is the literal human, not a persona.** |
| **CRO** | AI persona | `dd_protection` integrity, the lifecycle authorization axis, M1 monitoring maturity, regime-robustness gate, strategy-validation discipline, c1 rail `dry_run`/`armed_until` invariants. The CLAUDE.md "Safety invariants (non-negotiable)" section is this seat's charter. | Yes — highest-stakes seat; mandatory on every GRAND decision (§4). |
| **CIO** | AI persona | Front-office oversight: a3, a4, the strategy-generation side of a2. | Yes |
| **COO** | AI persona | Back-office oversight: a5, a6, the meta-belt (d1-d16), STATE/SESSIONS/CATALOG hygiene, retention discipline. | Yes |
| **CFO** | AI persona | Survive bound (≤5 queue cap — concurrency-denominated per `docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md`; **not itself a capital concept**, despite sitting in this seat's domain), subscription spend (d11-d16), capital-allocation rulings (F1), the weekly token-trade compliance obligation. | Yes |

### 5.2 STRATEGIC tier — Senior Managers (front / middle / back office)

Sized to real current standing work, not padded to a target count — see §8 for the rejected
alternative of forcing a fixed fan-out.

| Office | Seat | Owns | Real-world title basis |
|---|---|---|---|
| Front (CIO) | **Head of Research** | [a3 MNQ discovery pipeline](../../pursuits/a3-mnq-discovery-pipeline.md) + [a4 harvest/external-mechanism intake](../../pursuits/a4-harvest-external-mechanism-intake.md) | Head of Quantitative Research — close analogue (real senior title exists; industry scope is broader than just this intake-gate function) |
| Front (CIO) | **Head of Execution** | [a2 c1 rail + incumbent-eval operations](../../pursuits/a2-c1-rail-incumbent-eval-operations.md) | Head of Execution — direct match |
| Middle (CRO) | **Head of Risk & Sizing** | `dd_protection`, the lifecycle axis, DD tier | Head of Risk — direct match |
| Middle (CRO) | **Head of Validation** | M1 monitoring, regime-robustness gate, strategy-validation (Step-0, DSR, overfitting) | Head of Model Validation — close analogue (established in banking/asset management; title kept short per Joshua) |
| Back (COO) | **Head of Engineering** | [a5 R&D tooling lane](../../pursuits/a5-rd-tooling-lane.md) + [a6 Cursor-fleet capability](../../pursuits/a6-cursor-fleet-worker-capability.md); personally performs the AI-agent-orchestration function (decompose, freeze specs, own the claim manifest, review, integrate, adjudicate — per the `cursor-fleet` skill) | Head of Quantitative Engineering — direct match; orchestration function folded in rather than delegated to a separate staff seat |
| Back (COO) | **Head of Governance** | Cross-office inventory (`docs/pursuits/`), ADR discipline, retention/pruning | Mandate sharpened toward banking's "Head of Model Risk Governance" (firm-wide inventory + governance-transformation); **placement kept under COO, not CRO** — see §5.2.1 |

#### 5.2.1 Why Head of Governance stays under COO, not CRO

The banking analogue for this role sits inside Risk because its scope there is narrowly risk-model
inventory. Here, governance is cross-cutting — it owns the pursuit/decision inventory and audit
trail for *all three offices*, including whether Risk itself complies with its own documentation
obligations. That is structurally closer to a **3rd line of defense** (independent audit, reporting
outside both 1st-line business and 2nd-line risk) than to 2nd-line risk itself. Placing it under CRO
would have Risk auditing itself — the exact independence failure this whole hierarchy exists to
prevent.

### 5.3 Staff

Most OUTER/INNER-tier work stays unnamed and ephemeral — most investigations don't warrant a
standing identity. The exceptions are recurring, non-instance-bound *methodology gates* that fire
the same way across every campaign regardless of which specific Q-brief is running:

| Reports to | Staff persona | Function | Real-world title |
|---|---|---|---|
| Head of Research | Falsifier Analyst | Cheap-falsifier / pre-G0 kill discipline | In-house — no clean equivalent (bundled into "Quant Researcher" at real funds) |
| Head of Research | Pre-Registration Analyst | G0-freeze discipline before any test runs | In-house — imported from open-science practice, not a finance role |
| Head of Execution | TCA Analyst | Cost-law pre-screen — edge must survive realistic costs before further investment | **Transaction Cost Analysis Analyst — direct match** |
| Head of Risk & Sizing | Risk Analyst (Intraday) | DD-tier compliance checks on any live-risk-touching item | **Direct match — found verbatim at an actual prop firm (Topstep), down to "monitor accounts intraday for drawdowns"** |
| Head of Validation | Model Validation Analyst | Overfit / DSR screen | In-house — loose borrow from banking model-validation practice |
| Head of Validation | Robustness Analyst | Regime-robustness (both-halves) gate | In-house — no clean equivalent |
| Head of Governance | Documentation Analyst | Brief-compliance (`check_brief.py`-style) gate | In-house — nearest is technical-writer/IC-memo review, a different artifact class |
| Head of Governance | Research Registry Analyst | Dedup-first-before-new-work discipline | In-house — informally practiced at large funds, never a titled role |
| **Head of Engineering** | *(no named persona)* | Implementation work on frozen specs | **Staff here are the literal Cursor worker agents dispatched per packet** — ephemeral, frozen-spec implementers per the existing `cursor-fleet` skill. They never exercise independent judgment (they bounce `NEEDS_CONTEXT` rather than deciding), so they don't fit the persistent-persona-with-a-log pattern every other Staff seat uses. This row is governed entirely by existing `cursor-fleet` mechanics — nothing new is built for it. |

8 named, persistent Staff personas; Engineering's staff pool is the existing Cursor dispatch
mechanism, unmodified.

## 6. Mechanics — how a panel actually runs

### 6.1 Precondition

The proposal must exist as a **committed, frozen artifact** before any review persona is spawned —
mirroring how GSUB-1 itself worked (Phase 1-2 inventory committed, then Phase 3 ratification read it
fresh). No live back-and-forth ever leaks a proposer's reasoning into a reviewer's context; the
artifact *is* the interface boundary. If no frozen artifact exists yet, the panel does not run — this
is a hard precondition, not a best-effort skip.

### 6.2 Spawn pattern

Each relevant persona is spawned fresh via `agent()`:

- Reads only the frozen artifact path + that persona's own decision-log file (§6.4). Never the
  authoring session's transcript or live reasoning.
- Prompted to argue strictly from its office's mandate (e.g., CRO explicitly checks the item against
  the CLAUDE.md safety invariants).
- Instructed to flag dissent explicitly — never softened toward consensus.

Staff-tier reviews (where they exist — Falsifier Analyst, TCA Analyst, etc.) apply the same
independence principle at lower cost: one fresh agent call reading only the candidate/data artifact,
not the proposing session's framing or enthusiasm for the candidate. This is the direct
operationalization of SR 11-7's "validator independent of developer."

### 6.3 Synthesis and the one hard-block exception

A separate synthesis pass combines panel outputs into one memo for Joshua. Dissent is preserved
**verbatim**, never averaged away.

**Exception:** a CRO dissent that cites a non-negotiable safety invariant (the `dry_run`/M1/arming
set already written as non-negotiable in CLAUDE.md) is a **hard block, not a flag** — the panel does
not grant itself more authority to waive those invariants than the existing doctrine grants anyone,
including Joshua's own override. This restates existing doctrine; it does not create new AI
authority.

Everything else stays fully advisory. Joshua decides, always.

### 6.4 Persona memory

One markdown file per persona (`docs/personas/<role-slug>-log.md`), append-only — matching how
STATE.md/SESSIONS.md/closures already work in this repo (never edit history, always append or
supersede). Each entry: date, artifact reviewed, verdict, whether Joshua ratified as recommended or
overrode it.

Read as input the next time that persona is spawned; written after each run. First-ever run for a
persona treats an absent/empty log as normal, not an error — it says so explicitly rather than
fabricating history.

**Explicitly distinct from c1 Q-XMEM-1** (§2) — this is a narrow, single-purpose artifact bound to
this panel mechanism only, not a general cross-surface memory system.

### 6.5 Permanent Staff trigger (independent of the panel)

Permanent Staff personas (§5.3) fire at their own natural gate, independent of any GRAND/STRATEGIC
panel — e.g., Falsifier Analyst runs whenever a candidate actually needs cheap-falsifier screening,
which is constant and unrelated to whether a GRAND/STRATEGIC decision is in flight. Their logs feed
*into* the relevant Senior Manager's review only when a STRATEGIC-tier decision actually touches
that domain.

## 7. Error handling

| Condition | Behavior |
|---|---|
| No frozen artifact exists yet | Panel does not run. Hard precondition, not a soft skip. |
| First-ever run for a given persona | Empty/absent log is normal; the persona states this explicitly rather than fabricating prior history. |
| Two personas' verdicts flatly contradict | Preserved as dissent in the synthesis; Joshua adjudicates — except the CRO safety-invariant case (§6.3), which hard-blocks regardless. |
| A persona is asked to review something outside its office's mandate | Declines rather than opining, keeping domain boundaries crisp (the same discipline the GRAND ADR's §2.4 domain-table guard already enforces one tier up). |

## 8. Alternatives considered

| Alternative | Why not chosen |
|---|---|
| **Same-session multi-voice** — one CC session sequentially writes each persona's take in shared context. Cheap, no new tooling. | Fails the independence principle this whole design is built on — the exact failure shape as Kerviel/Adoboli (one party holding both the proposing and reviewing role). Acceptable only for low-stakes OUTER-tier labeling, never for GRAND/STRATEGIC panel decisions. |
| **Full bespoke build** — new skill, new memory infrastructure from scratch, independent of `pre-ratification-adversarial-panel`. | Highest cost; duplicates most of what the existing skill and a plain markdown log already provide. Only worth revisiting if the lightweight design here proves insufficient in real use. |
| **Fixed 4-6 fan-out per tier, forced to a target org-chart shape** (the original proposal) | Real current STRATEGIC-tier inventory supports 2-3 stable domains per office (7-8 total), not 12-18. Pre-minting empty seats to hit a target count reproduces the "belt that only grows" failure mode GSUB-1's own retrospective flagged. Roster grows only when a genuine new standing domain opens. |
| **Manager layer between Senior Managers and Staff** (mirroring OUTER as its own persona tier) | The candidate "manager" functions (cheap-falsifier gating, cost-law screening, etc.) are staff-shaped work in real organizational terms — mechanical, checklist-driven, one-function-one-owner — not supervisory judgment over several such functions. Real front/middle/back offices also run 3 levels deep, not 4 (§9). |
| **Persona-per-current-pursuit instances** (1:1 with the 37 `docs/pursuits/` records) | Pursuits churn on a near-weekly cadence (8 PARKs alone converting by 2026-11-08); this roster would need constant re-minting and would go stale within days. Stable functional roles persist across whatever pursuits currently sit in their domain, matching how real orgs actually staff departments. |

## 9. Real-world grounding (research summary)

Full findings live in this session's research; key points repeated here since they're load-bearing:

- **SEC Rule 18f-4** (derivatives risk management): a fund's risk manager "may not be a portfolio
  manager of the fund" — literal role-independence language, borrowed directly for §6.2.
- **Fed SR 11-7** (model risk management): model validation must be organizationally independent from
  model development — the direct analogue for "the persona that evaluates a candidate cannot be the
  persona that generated it."
- **Three Lines of Defense** (IIA guidance): 1st line (business) owns/operates controls; 2nd line
  (risk/compliance) sets policy and provides independent challenge — not unilateral veto; 3rd line
  (audit) gives the board independent assurance on both. Maps to §4's spawn-selection rule and
  §5.2.1's Governance placement.
- **Historical grounding for why this matters**: Barings/Leeson (1995, ~$1.3B), Société
  Générale/Kerviel (2008, ~$7.1B), UBS/Adoboli (2011) — all three failures trace to one person holding
  both a front-office and a control-adjacent role, supervising their own risk.
- **Small-shop compression**: real solo-PM funds preserve independence not through headcount but
  through a structurally separate control function (an outsourced administrator, a designated
  non-PM principal) — the generalizable rule this design borrows: independence comes from the
  context/reporting boundary (§6.2's fresh-spawn-reads-only-the-artifact rule), not from having
  enough bodies to staff three offices.
- **Title grounding** *(corrected 2026-08-19 — see change history)*: this session's research
  characterized the roster's titles against real job postings and fund career pages, but no capture
  dates, source URLs, or per-role scoring table were retained or attached anywhere in this repo.
  **Treat this as a directional, unscored characterization, not a verified count.** Several Senior
  Manager titles (Head of Execution, Head of Risk, Head of Quantitative Engineering) read as
  close-to-exact matches to real industry titles; most Staff-tier functions have no clean real-world
  equivalent, plausibly because real funds bundle those functions into a generic "Quantitative
  Researcher" role rather than staffing them separately — but that plausibility judgment is
  unscored too. A specific claim of "direct match" or "verbatim" wording for any individual role
  (including the Risk Analyst (Intraday) row in §5.3, whose sourced quote did **not** survive
  independent adversarial re-check — see change history) should not be treated as confirmed unless a
  primary-source artifact (capture date, quote block) is attached to back it.

## 10. Testing — the built-in falsifier

Matching how every other doctrine artifact in this repo is written (see the GRAND ADR's own §4 test
on GSUB-1): **if, across the first several real GRAND/STRATEGIC uses, panel input never changes a
ratified outcome from what Joshua would have decided solo, that is the signal this is ceremonial
rather than load-bearing**, and the mechanism should be revisited rather than kept on faith. A
secondary, mechanically-checkable signal: dissent preserved in a persona's log should always appear
in the corresponding synthesis memo — a drift between the two (dissent logged but silently smoothed
in synthesis) is a defect in the mechanism, not a judgment call.

## 11. Open follow-ups (not decided by this spec)

- Whether this should also be ratified as a formal ADR once implemented, per the repo's existing
  brief-authoring convention — this spec is a pre-implementation design document, not itself a
  ratified decision.
- The exact `pre-ratification-adversarial-panel` skill edits needed to carry named personas instead
  of generic adversarial-reviewer framings — implementation detail for the plan, not this spec.
- Whether any additional Staff seats should be added later, and under what evidence bar (the same
  intake-rule discipline GRAND already applies to pursuits, §2.5 of the GRAND ADR, is the natural
  candidate to reuse rather than inventing a separate one).

## Change history

Corrections below were found by running `pre-ratification-adversarial-panel` against this spec as a
regression test for an unrelated Phase 2 code change (2026-08-19) — the panel's own doctrine and
structural-completeness lenses read this document adversarially and surfaced real defects, several
already propagated into shipped Phase 1/2 artifacts. Fixed as new commits, not by rewriting prior
history.

| Date | Change | By |
|---|---|---|
| 2026-08-19 | §5.1 CFO row corrected: Survive bound was mischaracterized as "capital-denominated," contradicting `docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md` (concurrency-denominated). Same fix applied to `docs/personas/cfo.md` and the Phase 1 plan's embedded copy. | Claude Code |
| 2026-08-19 | §9 title-grounding bullet softened: dropped unscored "direct match" / "roughly a third (5-6)" verdicts with no attached research artifact; flagged the Risk Analyst (Intraday) row's "verbatim" Topstep quote as not surviving independent adversarial re-check. Same fix applied to `docs/personas/risk-analyst-intraday.md` and the Phase 1 plan's embedded copy. | Claude Code |
