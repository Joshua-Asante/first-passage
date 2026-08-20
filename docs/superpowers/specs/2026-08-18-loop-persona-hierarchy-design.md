# Persona Hierarchy for the GRAND/STRATEGIC Loop Tiers — Design Spec

**Date:** 2026-08-18
**Status:** Accepted — ratified by Joshua 2026-08-19, in-session direct instruction ("Accepted on the design" / "Accepting the proposal"); see Ratification note
**Author:** Claude Code, design collaboration with Joshua (brainstorming session, 2026-08-18)

## 1. Purpose

First Passage's loop-tier doctrine (GRAND/STRATEGIC/OUTER/INNER — see
`docs/adr/2026-08-09-grand-tier-quintessentials-binding.md` and
`docs/adr/2026-06-12-three-loop-methodology-binding.md`) answers *who has the authority to decide
what*. It says nothing about *who argues which side before a decision gets made*. This spec adds a
persona layer on top: a stable roster of named roles, framed as a front/middle/back-office trading
firm, that get spawned as real subagents to review GRAND and STRATEGIC-tier decisions before Joshua
ratifies them — replacing *generic* multi-lens review (the existing `pre-ratification-adversarial-panel`
already runs 6 lenses + 2 skeptics; this is not literally single-voice today) with review structured
around named, domain-specific, front/middle/back-office roles and the independence mechanic in §6.2.

The motivating principle, grounded in real trading-firm practice (research below): **the person who
proposes a decision should never be the person who validates it.** Real firms enforce this through
reporting-line independence (SEC Rule 18f-4: a fund's risk manager "may not be a portfolio manager
of the fund"; Fed SR 11-7: model validation must be organizationally independent from model
development). The documented failure mode when this collapses — Barings/Leeson, Société
Générale/Kerviel, UBS/Adoboli — is one person holding both a front-office and a control-adjacent
role, supervising their own risk. This design borrows the mechanism, not just the vocabulary.

**Grounding caveat** *(added 2026-08-19 — see change history)*: every motivating incident above is
external to First Passage. No in-repo near-miss or incident is cited as evidence this specific
mechanism was needed here — the case rests on borrowed industry practice and the pre-existing
generic panel's own track record (see `feedback_adversarial_review_before_ratification.md`: a
green mechanical checker missed 6 real BLOCKERs on a prior brief), not on a local failure this
design is a direct response to.

## 2. Scope boundary — what this does NOT change

This is an overlay. It does not touch:

- **The 4-tier loop doctrine** (GRAND/STRATEGIC/OUTER/INNER) or its authority rules — the D-user-gate
  (`docs/methodology/inqhiori-canon.md` L284: "Claude Code and web Claude both propose deletions; Joshua authorizes"), D2/D3 no-borrowing
  (`docs/adr/2026-06-12-three-loop-methodology-binding.md`). Personas are a *different axis*: how many
  named review seats exist and what they argue, not who is allowed to execute what.
- **The CC/Cursor surface-allocation ADR** (`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`) —
  orthogonal axis (execution surface vs. decision authority). Cursor's role in this design (§5.3) is
  exactly its existing role under `cursor-fleet`, not a new one.
- **c1 Q-XMEM-1** (the cross-surface memory sidecar pilot, ratified `SUBTRACT` 2026-08-19 via GSUB-2
  *(corrected 2026-08-19 — see change history; previously called "parked" here after its own
  disposition had already changed)* — `docs/pursuits/c1-q-xmem-1.md`) — persona memory (§6.4) is a
  narrower, distinct mechanism (a plain per-persona markdown log read/written by this panel
  mechanism only). It is not a general cross-surface visibility system and does not revive that
  pursuit or its re-entry armor.
- **No AI persona gains independent authority to execute a GRAND Subtract or a STRATEGIC Delete.**
  Panels are advisory. Joshua decides, always — with one narrow exception (§6.3) that restates an
  existing non-negotiable, not a new grant of authority.

### 2.1 Retention self-test (added 2026-08-19 — see change history)

This spec proposes 21 new permanent artifacts that exist at authoring time *(corrected 2026-08-19
— see change history; the prior "~20" headline didn't sum to its own listed components)*: 19
persona definition files on disk (18 spawnable AI personas plus a `ceo.md` kept for roster-index
completeness even though CEO is never spawned, §5.1), a roster index, and a checker script — plus
up to 18 more append-only log files that accrue only once a persona's first real run happens
(§6.4) and are explicitly excluded from this count. Applying CLAUDE.md's own retention test
directly to that proposal, rather than leaving it unexamined:

- **R1 (pipeline-consumed):** contingent, not yet true. Each persona file is *designed* to be read by
  its own spawn prompt (§6.2) once the mechanism is in real use — but as of this writing nothing has
  consumed them for a real (non-rehearsal) decision. The §10 falsifier is the mechanism that proves
  or disproves this in use, not on faith.
- **R2 (live-safety):** true for the CRO seat specifically — its hard-block exception (§6.3) is a
  live-safety-adjacent control. The other 18 files are not live-safety artifacts on their own.
- **R3 (re-proposal bar):** not directly applicable — personas aren't rejected candidates being
  re-proposed. §11's open follow-up on a future Staff-seat intake rule (reusing GRAND §2.5) is the
  nearest analogue.
- **R4 (reproducibility manifest):** N/A — no data/backtest artifacts here.
- **R5 (open fireable obligation):** true, indirectly — §10's falsifier *is* the fireable obligation.
  If it fires (3 consecutive real uses with zero decision-difference), retention is answered
  mechanically (demote), rather than left to accumulate the way GSUB-1's own retrospective found
  happening elsewhere in this repo.

Honestly stated: this spec does not pass R1/R5 cleanly today — it passes them *prospectively*,
contingent on real use. That is a real gap, named here rather than left implicit, and it is the same
gap §10 exists to close.

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
   multiply panel cost substantially — OUTER-tier closures run several times a week on current
   evidence, far more often than GRAND/STRATEGIC-tier events — for no rigor gained at the OUTER tier
   (no per-panel cost model is derived here; this is a qualitative, not a scored, comparison).

**Who gets spawned, per trigger:**

- *GRAND:* the office(s) the pursuit's domain touches (mandatory) **plus CRO on every single GRAND
  decision, with no exceptions** — risk review isn't skippable because a pursuit looks unrelated to
  risk on its face. This is how the GRAND ADR's own forbidden-move #1 (paraphrase of that ADR's §5:
  using the ADR to relitigate any lower-tier lock, allocation, pre-registration, or risk-control
  constant) gets caught in practice, not just prohibited on paper.
- *STRATEGIC:* the proposing office (1st line, owns/operates) + at least one other office as
  independent challenge (2nd line) — Three Lines of Defense shape, documented challenge rather than a
  majority vote.

## 5. Roster

### 5.1 GRAND tier — C-suite

| Seat | Owner | Domain | Spawned as agent? |
|---|---|---|---|
| **CEO** | Joshua | Aim; sole GRAND ratification authority; sole owner-adjudication channel for STRATEGIC-tier Deletes (D2 channel c); sets the Survive bound; final word on every panel's synthesis | **Never — this is the literal human, not a persona.** |
| **CRO** | AI persona | `dd_protection` integrity, the lifecycle authorization axis, M1 monitoring maturity, regime-robustness gate, strategy-validation discipline, c1 rail `dry_run`/`armed_until` invariants. The CLAUDE.md "Safety invariants (non-negotiable)" section is this seat's charter. | Yes — highest-stakes seat; mandatory on every GRAND decision (§4). |
| **CIO** | AI persona | Front-office oversight: a3, a4, and a2 (a2 is owned wholesale by Head of Execution per §5.2 — it has no separate strategy-generation component; its own pursuit record's Aim is deploy-and-operate-safely on the incumbent eval, not signal generation). | Yes |
| **COO** | AI persona | Back-office oversight: a5, a6, the meta-belt (d1-d16), STATE/SESSIONS/CATALOG hygiene, retention discipline. | Yes |
| **CFO** | AI persona | Survive bound (≤5 queue cap — concurrency-denominated per `docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md`; **not itself a capital concept**, despite sitting in this seat's domain), subscription spend (d11-d16), capital-allocation rulings (F1), the weekly token-trade compliance obligation. | Yes |

### 5.2 STRATEGIC tier — Senior Managers (front / middle / back office)

Sized to real current standing work, not padded to a target count — see §8 for the rejected
alternative of forcing a fixed fan-out.

| Office | Seat | Owns | Real-world title basis |
|---|---|---|---|
| Front (CIO) | **Head of Research** | [a3 MNQ discovery pipeline](../../pursuits/a3-mnq-discovery-pipeline.md) + [a4 harvest/external-mechanism intake](../../pursuits/a4-harvest-external-mechanism-intake.md) | Head of Quantitative Research — close analogue (real senior title exists; industry scope is broader than just this intake-gate function) |
| Front (CIO) | **Head of Execution** | [a2 c1 rail + incumbent-eval operations](../../pursuits/a2-c1-rail-incumbent-eval-operations.md) | Head of Execution — close-to-exact match (unscored characterization; see §9) |
| Middle (CRO) | **Head of Risk & Sizing** | `dd_protection`, the lifecycle axis, DD tier | Head of Risk — close-to-exact match (unscored characterization; see §9) |
| Middle (CRO) | **Head of Validation** | M1 monitoring, regime-robustness gate, strategy-validation (Step-0, DSR, overfitting) | Head of Model Validation — close analogue (established in banking/asset management; title kept short per Joshua) |
| Back (COO) | **Head of Engineering** | [a5 R&D tooling lane](../../pursuits/a5-rd-tooling-lane.md) + [a6 Cursor-fleet capability](../../pursuits/a6-cursor-fleet-worker-capability.md); personally performs the AI-agent-orchestration function (decompose, freeze specs, own the claim manifest, review, integrate, adjudicate — per the `cursor-fleet` skill) | Head of Quantitative Engineering — close-to-exact match (unscored characterization; see §9); orchestration function folded in rather than delegated to a separate staff seat |
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
| Head of Research | Research Analyst | General research support for a3/a4; inaugural project (added 2026-08-19): decompose active/archived research into atomic, statistically-important facts assembled into per-instrument profiles, starting with MNQ (a3) | In-house — the first *producer*-type Staff seat on this roster (see note below); no clean real-world title, closest analogue is a buy-side "Research Associate" doing thematic/cross-desk synthesis rather than gate review |
| Head of Execution | TCA Analyst | Cost-law pre-screen — edge must survive realistic costs before further investment | **Transaction Cost Analysis Analyst — direct match** |
| Head of Governance | Documentation Analyst | Brief-compliance (`check_brief.py`-style) gate | In-house — nearest is technical-writer/IC-memo review, a different artifact class |
| Head of Governance | Research Registry Analyst | Dedup-first-before-new-work discipline | In-house — informally practiced at large funds, never a titled role |
| **Head of Engineering** | *(no named persona)* | Implementation work on frozen specs | **Staff here are the literal Cursor worker agents dispatched per packet** — ephemeral, frozen-spec implementers per the existing `cursor-fleet` skill. They never exercise independent judgment (they bounce `NEEDS_CONTEXT` rather than deciding), so they don't fit the persistent-persona-with-a-log pattern every other Staff seat uses. This row is governed entirely by existing `cursor-fleet` mechanics — nothing new is built for it. |

**Archived 2026-08-19, briefly, then partly restored same day (see Change History).** All 5
Middle/Back-office analysts (above the Head of Engineering row: Risk Analyst Intraday, Model
Validation Analyst, Robustness Analyst originally alongside Documentation Analyst and Research
Registry Analyst) were archived same-day as never-spawned. After operator pushback, all 5 were
retroactively tested against real repo artifacts. Documentation Analyst and Research Registry
Analyst each found a genuine, previously-uncaught defect in a real artifact on first spawn — see
`docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md` — and are restored above.
**Still archived, tested-but-inconclusive** (came back clean against a target outside their
domains, not shown to add no value): Risk Analyst (Intraday) (Head of Risk & Sizing), Model
Validation Analyst (Head of Validation), Robustness Analyst (Head of Validation) — full charters
preserved at [`docs/personas/archive/`](../../personas/archive/); retirement procedure per §6.7.
Front-office Staff (above) are unaffected and in active use throughout.

5 active, persistent Staff personas from this archive/restore cycle (down from 8 built same-day,
up from the initial 3-personas cut), plus Research Analyst — spawned same day on a parallel
branch, unaffected by the archive/restore cycle, merged in 2026-08-20 — for 6 total named Staff
seats (Falsifier Analyst, Pre-Registration Analyst, Research Analyst, TCA Analyst, Documentation
Analyst, Research Registry Analyst); Engineering's staff pool is the existing Cursor dispatch
mechanism, unmodified.

**Architectural note (added 2026-08-19):** every Staff seat above Research Analyst is a recurring
*review/gate* function — the class this section's own opening paragraph licenses a standing identity
for (SR-11-7-style evaluator independence). Research Analyst is the first *producer* seat: it
generates research synthesis rather than gating someone else's, so the independence property doesn't
apply to its own output the way it does the other eight. Its charter (`docs/personas/research-analyst.md`)
routes anything it produces that reaches a G0/pre-registration point or a STRATEGIC-tier decision
through the existing gates (Falsifier Analyst, Pre-Registration Analyst, Head of Research's own
review) rather than granting the new seat any self-certifying authority. Flagged explicitly here so
this departure from precedent isn't silently blended into the table above.

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
operationalization of SR 11-7's principle that a validator must be organizationally independent of
the developer *(reworded 2026-08-19 — see change history; not the letter's literal wording, an
accurate paraphrase)*.

This mechanic addresses *contextual* contamination only — see §9's "Architectural correlation"
bullet for the distinct, unaddressed risk of same-model-family correlated bias across personas.

### 6.3 Synthesis and the one hard-block exception

A separate synthesis pass combines panel outputs into one memo for Joshua. Dissent is preserved
**verbatim**, never averaged away.

**Exception:** a CRO dissent that cites a non-negotiable safety invariant (the `dry_run`/M1/arming
set already written as non-negotiable in CLAUDE.md) is a **hard block, not a flag** — the panel does
not grant itself more authority to waive those invariants than the existing doctrine grants anyone,
including Joshua's own override. This restates existing doctrine; it does not create new AI
authority.

Everything else stays fully advisory. Joshua decides, always.

**Citation-diff / independent-dissent flag — ARCHIVED 2026-08-19 (operator-authorized cut; see
Change History).** Was drafted-not-wired-in, held until N=3 real data (was 1/3 banked). Full text
preserved at
[`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`](archive/2026-08-19-persona-hierarchy-archived-sections.md#63-addendum--citation-diff--independent-dissent-flag-drafted-not-wired-in).
Re-propose once its own hold condition clears.

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

#### 6.4.1 Charter versioning and bounded self-refinement — ARCHIVED 2026-08-19

Operator-authorized cut (see Change History). Trigger required 2 consecutive divergent
ratifications; the only real review to date (GSUB-2) produced zero divergence — outside current
temporal scope. Full text preserved at
[`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`](archive/2026-08-19-persona-hierarchy-archived-sections.md#641--charter-versioning-and-bounded-self-refinement-added-2026-08-19).
Re-propose when a second divergence looks imminent, not before the first.

### 6.5 Permanent Staff trigger (independent of the panel)

Permanent Staff personas (§5.3) fire at their own natural gate, independent of any GRAND/STRATEGIC
panel — e.g., Falsifier Analyst runs whenever a candidate actually needs cheap-falsifier screening,
which is constant and unrelated to whether a GRAND/STRATEGIC decision is in flight. Their logs feed
*into* the relevant Senior Manager's review only when a STRATEGIC-tier decision actually touches
that domain.

### 6.6 Cross-examination round — ARCHIVED 2026-08-19

Was `ACCEPTED` (ratified 2026-08-19) but never implemented — zero code, zero executions, no
`<slug>-cross-exam-log.md` file ever created. Consumed two full adversarial-review cycles (one
`BLOCKED` with 6 confirmed BLOCKERs, a recheck that found the fix "visibility-only" and forced a
redesign) reviewing a feature that was never built. Operator-authorized cut (see Change History).
Full text — trigger, ownership precondition, CRO carve-out, mechanics, falsifier — preserved at
[`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`](archive/2026-08-19-persona-hierarchy-archived-sections.md#66--cross-examination-round-interactive-opt-in--added-2026-08-19).
Re-propose alongside the first real disputed Stage-1 finding that actually needs it.

### 6.7 Persona retirement procedure (individual seat — added 2026-08-19)

Distinct from §10's falsifier disposition, which demotes the *whole panel mechanism* if it fires
("demote to a lighter, non-panel review path"). Retiring one named persona is a separate, narrower,
human-initiated event with its own evidence — this subsection is the previously-missing procedure
for that case, modeled on this repo's own Great Prune precedent
(`docs/adr/2026-08-08-great-prune.md`): PR-merge is the ratification, and dead-weight has to be
proven, not assumed. Great Prune's own adversarial "prove each file is dead" review rescued 66 of
69 candidate deletions (4.3% classifier precision) before its own PR merged — persona retirement
carries the same proof burden, scaled down.

**Trigger.** Operator-decided only, never automatic — e.g. N consecutive reviews with zero
findings, or a direct Joshua call. Never inferred solely from the §10 falsifier firing on the whole
panel, which is a distinct, broader event.

**Procedure.**
1. **Freeze intake** — stop assigning new `docs/personas/ownership-map.md` rows to the persona.
2. **Reassign** — move every existing ownership-map row (primary or secondary) to the covering
   persona, per the existing reporting line (a retired Staff seat's rows go to its Head; a retired
   Senior Manager's rows go to its GRAND-tier officer).
3. **Archive, don't delete** — the persona's log file (`docs/personas/<slug>-log.md`) stops
   receiving new entries; git history is the archive, matching how Great Prune treats every
   deleted byte (`git show pre-prune-2026-08-08:<path>`).
4. **Update the index** — mark the row RETIRED in `docs/personas/INDEX.md` with a pointer, the same
   tombstone convention `docs/adr/TOMBSTONES.md` already uses elsewhere in this repo.
5. **Ratify before merge** — the whole diff (ownership-map reassignment + INDEX update + a short
   retirement note stating the trigger and evidence) goes to Joshua as one PR, never auto-executed
   — the same D5 discipline every other structural change in this design already carries.

Explicitly not part of this procedure: disabling "endpoints or credentials" — personas are fresh
per-review spawns with no standing credentials to revoke; step 4 above already covers what that
instinct is reaching for.

## 7. Error handling

| Condition | Behavior |
|---|---|
| No frozen artifact exists yet | Panel does not run. Hard precondition, not a soft skip. |
| First-ever run for a given persona | Empty/absent log is normal; the persona states this explicitly rather than fabricating prior history. |
| Two personas' verdicts flatly contradict | Preserved as dissent in the synthesis; Joshua adjudicates — except the CRO safety-invariant case (§6.3), which hard-blocks regardless. |
| A persona is asked to review something outside its office's mandate | Declines rather than opining, keeping domain boundaries crisp (the same discipline the GRAND ADR's §2.4 domain-table guard already enforces one tier up). |
| A cross-examination round (§6.6, ARCHIVED 2026-08-19 — never built) is requested | Does not run — the mechanism doesn't exist; see §6.6 for the archive pointer. |

## 8. Alternatives considered

| Alternative | Why not chosen |
|---|---|
| **Same-session multi-voice** — one CC session sequentially writes each persona's take in shared context. Cheap, no new tooling. | Fails the independence principle this whole design is built on — the exact failure shape as Kerviel/Adoboli (one party holding both the proposing and reviewing role). Acceptable only for low-stakes OUTER-tier labeling, never for GRAND/STRATEGIC panel decisions. |
| **Full bespoke build** — new skill, new memory infrastructure from scratch, independent of `pre-ratification-adversarial-panel`. | Highest cost; duplicates most of what the existing skill and a plain markdown log already provide. Only worth revisiting if the lightweight design here proves insufficient in real use. |
| **Fixed 4-6 fan-out per tier, forced to a target org-chart shape** (the original proposal) | Real current STRATEGIC-tier inventory supports 2-3 stable domains per office (7-8 total), not 12-18. Pre-minting empty seats to hit a target count reproduces the volume/bloat failure shape the GRAND ADR's own motivating language names "a belt that only grows" *(corrected 2026-08-19 — see change history; a related but distinct symptom from what GSUB-1's own retrospective actually found — ownerless, un-expiring drift, not raw volume)*. Roster grows only when a genuine new standing domain opens. |
| **Manager layer between Senior Managers and Staff** (mirroring OUTER as its own persona tier) | The candidate "manager" functions (cheap-falsifier gating, cost-law screening, etc.) are staff-shaped work in real organizational terms — mechanical, checklist-driven, one-function-one-owner — not supervisory judgment over several such functions. Real front/middle/back offices also run 3 levels deep, not 4 (§9). |
| **Persona-per-current-pursuit instances** (1:1 with the 38 `docs/pursuits/` records) | Pursuits churn on a near-weekly cadence — of the original 8 GSUB-1 PARKs, only 5 (b1, b3, b6, b7, c3) still ride to the 2026-11-08 default *(corrected 2026-08-19 — see change history; previously stated "7," undercounting two further same-day dispositions)*: b5 was renewed to 2027-02-08 on 2026-08-16, and b2/c1 were separately ratified `SUBTRACT` via GSUB-2 on 2026-08-19 — itself evidence of the churn this row describes. This roster would need constant re-minting and would go stale within days. Stable functional roles persist across whatever pursuits currently sit in their domain, matching how real orgs actually staff departments. |

## 9. Real-world grounding (research summary)

Full findings live in this session's research; key points repeated here since they're load-bearing:

- **Organizational depth** *(added 2026-08-19 — see change history; this is the source for §3's "three
  levels, not four" and §8's Manager-layer rejection, both of which cited this section before it
  actually carried the finding)*: this session's front/middle/back-office research characterized real
  trading-firm hierarchies as running a realistic 2-3 levels of depth per office — C-suite →
  department-head/senior-manager → staff/analyst — not four. Like the title-grounding bullet below,
  this is an unarchived, directional research characterization (no capture dates or scoring table
  retained), not a formally scored count.
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
- **Architectural correlation — an open risk, not solved by this design** *(added 2026-08-19)*:
  fresh-context spawning (§6.2) prevents *contextual* contamination — a reviewer never sees the
  proposer's live reasoning, or any other reviewer's draft opinion. It does nothing about
  *architectural* correlation: CRO/CIO/COO/CFO personas likely share one underlying model family's
  blind spots and its pull toward "the artifact looks complete, therefore approve." 2025-2026
  literature on LLM-judge/evaluator collusion documents this as a real, unsolved failure mode for
  nominally independent AI reviewers. No mitigation is proposed here — this bullet exists so "fresh
  subagents" is never silently read as having solved a risk it only partially addresses.
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

*(Restructured 2026-08-19 with explicit H:/Falsifier:/Trigger-check-schedule tokens — see change
history. The original prose claimed parity with the GRAND ADR's own §4 discipline without actually
reproducing its structure.)*

**H:** Across the first 3 real (non-rehearsal) GRAND or STRATEGIC panel uses, at least one panel run
changes what Joshua would have ratified without it — a confirmed BLOCKER, a CRO hard-block, or a
preserved dissent that alters the disposition from what a single-voice recommendation would have
produced.

**Falsifier:** 3 consecutive real panel uses that each produce zero decision-difference (the
synthesis's disposition matches what Joshua's own unassisted read would have concluded) falsifies
the panel as load-bearing. Disposition on falsification: demote to a lighter, non-panel review path
via a superseding record — never silent retention on faith.

**Trigger check schedule:** at the 3rd real panel use, or the next quarterly programme-audit gate
(2026-11-08), whichever comes first — matching how the GRAND ADR's own §4 test on GSUB-1 is read at
the same cadence, rather than inventing a new one.

A secondary, mechanically-checkable signal, independent of the H/Falsifier above: dissent preserved
in a persona's log should always appear in the corresponding synthesis memo — a drift between the
two (dissent logged but silently smoothed in synthesis) is a defect in the mechanism, not a judgment
call, and should be treated as a bug report regardless of where the H/Falsifier trajectory stands.

**A limitation this falsifier cannot see (added 2026-08-19 — see §9's "Architectural correlation"
bullet).** The H/Falsifier above measures divergence from what Joshua would have concluded
unassisted. A panel that is correlated-but-wrong — sharing the same underlying-model blind spot
Joshua himself might share, per §9 — looks identical, on this measure, to a panel that is genuinely
unnecessary: both produce zero decision-difference. This falsifier can detect "the panel added
nothing"; it cannot distinguish *why* — redundant panel vs. panel-and-operator sharing one blind
spot together. No fix is proposed here, consistent with §9's own stance on the underlying risk —
named as an open limitation of the measurement itself, not left implicit.

### 10.1 Preference-anchoring companion check — ARCHIVED 2026-08-19

Trigger was a persona's 5th real log entry; deepest log at archival (CRO) has 3. Structurally
unreachable at current usage. Operator-authorized cut (see Change History). Full text preserved at
[`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`](archive/2026-08-19-persona-hierarchy-archived-sections.md#101--preference-anchoring-companion-check-added-2026-08-19).
Re-propose once any persona's log approaches 5 real entries.

### 10.2 Self-consistency companion checkpoint — ARCHIVED 2026-08-19

Trigger ("first 1-2 real GRAND-tier reviews") already fired at GSUB-2 and was never executed — a
grep for "Self-consistency checkpoint" across every real log file returns zero hits. Operator-
authorized cut (see Change History). Full text preserved at
[`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`](archive/2026-08-19-persona-hierarchy-archived-sections.md#102--self-consistency-companion-checkpoint-added-2026-08-19).
Re-propose fresh at the next real GRAND-tier review if still wanted.

## 11. Open follow-ups (not decided by this spec)

- **Formal ADR — closed 2026-08-19.** Disputed finding B (whether a separate ADR should follow, to
  give the decision doctrine-tier status rather than living only as an accepted
  `docs/superpowers/specs/` document) is resolved by
  [`docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`](../../adr/2026-08-19-loop-persona-hierarchy-review-panel.md)
  (`Accepted` same day). That ADR *is* the resolution — a pointer-tier registration of the decision
  this spec already carries. This bullet is left in place as a record that the question was once
  open, not because it still is. See Change History.
- The exact `pre-ratification-adversarial-panel` skill edits needed to carry named personas instead
  of generic adversarial-reviewer framings — implementation detail for the plan, not this spec.
- Whether any additional Staff seats should be added later, and under what evidence bar (the same
  intake-rule discipline GRAND already applies to pursuits, §2.5 of the GRAND ADR, is the natural
  candidate to reuse rather than inventing a separate one).

## Ratification note (2026-08-19)

**Ratified by:** Joshua, in-session direct instruction — *"Accepted on the design" / "Accepting the
proposal"* (2026-08-19, mid-PR-creation flow on branch `claude/grand-strategy-review-5d9eae`).
Authority channel: explicit owner adjudication.

This closes **disputed finding A** from the 2026-08-19 adversarial review (the "pending review"
framing vs. same-evening implementation, §1/§11's prior wording) — the spec is no longer pending; it
is reviewed and accepted, with all 4 confirmed BLOCKERs and 6 confirmed CONCERNs from that same
review already fixed as prior commits on this branch (see Change history below).

**Disputed finding B** (whether this spec needs a separate, formal ADR for its own Draft→Accepted
transition) is **resolved same day** by
[`docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`](../../adr/2026-08-19-loop-persona-hierarchy-review-panel.md)
(`Accepted` 2026-08-19). The operator originally accepted the design in its
`docs/superpowers/specs/` genre; the ADR is the subsequent pointer-tier registration on the
doctrine surface *(clarified 2026-08-19 — see change history; this note is left as originally
written, not backdated, so the sequence of events stays honest)*. See §11 and Change History.

**Not licensed by this acceptance:** anything the design's own §2 Scope boundary already excludes —
the loop-tier doctrine, the CC/Cursor surface-allocation ADR, and c1 Q-XMEM-1 stay untouched. This
ratifies the *design*; it does not itself authorize skipping Phase 2's remaining tasks or Phase 3's
validation — those still execute per the existing three-phase plan.

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
| 2026-08-19 | §9 gained an "Organizational depth" bullet. §3 and §8 both cited "(§9)" as the source for the "three levels, not four" architectural decision, but §9 never actually carried that research — the citation pointer resolved to an empty set. | Claude Code |
| 2026-08-19 | §10 restructured with explicit `H:`/`Falsifier:`/`Trigger check schedule:` tokens (N=3, dated to the 2026-11-08 quarterly gate). The prior prose claimed to match the GRAND ADR's own §4 discipline without reproducing its structure. | Claude Code |
| 2026-08-19 | This decision was registered as a formal ADR — [`docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`](../../adr/2026-08-19-loop-persona-hierarchy-review-panel.md), ratified same day — resolving §11's open "disputed finding B" (whether a separate ADR should follow). No content in this spec changed; the ADR is a pointer-tier registration of the decision this spec already carries. | Claude Code |
| 2026-08-19 | §6.6 added — cross-examination round, a strictly-additive, post-synthesis, opt-in extension letting Joshua route one persona's already-locked Stage-1 position to a co-owning persona for direct response. Motivated by operator question, same day, about whether personas could see/react to each other's work interactively — answer: not during Stage 1 (that would reopen the SEC 18f-4 / SR 11-7 independence property §1 is built on), but yes as a bounded debate round after independent judgment is already on record, same shape real risk committees use. §7 error-handling table gained a matching fail-closed row (ownership mismatch declines the round). **PROPOSED — not yet ratified; §6.1–§6.5 and the persona-hierarchy ADR are unaffected either way.** | Claude Code (drafted at operator request) |
| 2026-08-19 | §6.6 self-reviewed via its own pre-ratification adversarial panel (44 agents, 6 lenses + double-skeptic verify, workflow run `wf_88c21d8d-a7f`) before ratification was even asked for — disposition `BLOCKED`, 6 confirmed BLOCKERs. Fixed same day: explicit "Status: PROPOSED, no implementing code" line added at §6.6's own top (was previously only in Change History); §7's row hedged to match; ownership gate gained a mandatory CRO carve-out (was 1/38-eligible without it); mechanics gained point 6, a `**Cross-exam (operator-framed):** yes` provenance tag, closing a durable-log contamination path into unrelated future Stage-1 reviews; the CRO hard-block paragraph gained explicit coverage for a safety-invariant citation surfacing for the first time *during* cross-examination, not only at Stage-1; Falsifier clause gained a third branch (`not yet tested`) so a low-opportunity-count checkpoint isn't misread either way. Also fixed in passing, same commit, since found by the same panel run in the same file: §5.3's unhedged fabricated Topstep "verbatim" quote (contradicted the document's own §9 correction, which had touched everything *except* its origin point) and §13's stale "first real data point... can only come from a genuine future" claim (GSUB-2 had already supplied it, same day, before this file's own prior edit). Remaining CONCERNS/NITs from the same run (stale §5.2 labels, a wrong `inqhiori-canon.md` line citation, §11's stale "remains open," unbacked agent-count metadata, sibling ADR's missing dedup-first attestation) are pre-existing and out of §6.6's own scope — spun off as a separate follow-up rather than bundled here. | Claude Code |
| 2026-08-19 | Pre-existing staleness caught in passing by the §6.6 adversarial panel (`wf_88c21d8d-a7f`; confirmed, double-skeptic-verified; does not block §6.6's own ratification). Softened §5.2 "direct match" labels to "close-to-exact match (unscored characterization; see §9)" so they no longer contradict §9; same wording applied to the three Senior Manager persona files and the Phase 1 plan's embedded copies (labeled mirrors of §5.2). Corrected §2 D-user-gate citation L282 → L284 (L282 is an unrelated brief-header bullet; L284 carries the quoted text). Closed §11 / Ratification-note disputed finding B as resolved by the Accepted persona-hierarchy ADR. Dropped quotation marks around the GRAND ADR §5 forbidden-move #1 paraphrase. Marked §13's "19 agents, ~10.6 minutes" as-reported — run artifacts were not preserved. Same regression-check pattern as the rows above. Discharges the follow-up named in the row above. | Claude Code |
| 2026-08-19 | **Correction to the row above.** The row's characterization of the previous fix — "a `Cross-exam (operator-framed): yes` provenance tag, closing a durable-log contamination path" — overclaimed. A targeted, operator-requested re-check (workflow `wf_8d2086b0-27d`: one steelman-the-kill lens re-run against the fixed text, double-skeptic-verified) confirmed unanimously that the tag was visibility-only: nothing in §6.2/§6.4 told a future Stage-1 spawn to treat a tagged entry any differently, so the influence pathway the original BLOCKER named stayed fully open, just human-auditable. The same re-check confirmed fixes 1, 4, 5 (the Status line, CRO hard-block extension, Falsifier third branch) genuinely closed their BLOCKERs, and flagged (disputed 1-1, non-gating per its own synthesis) that the CRO carve-out expands cross-exam eligibility from 1/38 to 38/38 GRAND items, compounding the tag's gap specifically for the panel's highest-stakes seat. **Redesigned, not re-patched:** mechanics point 5 now routes a cross-examination round's written record to a separate file (`docs/personas/<slug>-cross-exam-log.md`) that §6.2's Stage-1 spawn never reads, closing the pathway structurally rather than by label — and, as a side effect, substantially moots the CRO-exposure CONCERN, since no cross-exam content reaches any persona's Stage-1 read path regardless of how many items that persona is eligible for. The CRO hard-block extension was also re-scoped to CRO-authored citations specifically, matching §6.3's literal wording and the underlying `croHardBlockFires` code (keys off the `cro` lens result only), closing the NIT the same re-check raised about unscoped hard-block-triggering authority. Still `PROPOSED` — this redesign has not itself been re-verified by a fresh check. | Claude Code |
| 2026-08-19 | §6.6 ratified `PROPOSED` → `Accepted` (operator in-session instruction, "ratify now"). The redesigned mechanics point 5 (§6.6-cross-exam-log.md file separation, ratified without a third review round — operator judgment call) is now the entirety of what this subsection describes. Status line, §7's row, and this Change History updated to match; §5.1's own mandatory-CRO-participation framing and §6.3's hard-block scoping were re-read at ratification and found unaffected by anything in §6.6. | Joshua + Claude Code |
| 2026-08-19 | §1 reworded: dropped the inaccurate "replacing a single-voice recommendation" framing (the existing panel already runs 6 lenses + 2 skeptics) and added a grounding caveat that every motivating incident is external, not First-Passage-specific. Added §2.1 applying CLAUDE.md's own retention test (R1-R5) to this spec's ~20 proposed new artifacts, honestly stating it passes R1/R5 prospectively, not today. Softened §4's unsupported "order of magnitude" panel-cost claim. §5.1 CIO row and `docs/personas/cio.md` corrected: a2 has no "strategy-generation side" (contradicted both its own pursuit record and §5.2's wholesale Head-of-Execution assignment). §8's alternatives table corrected: 37 pursuits -> 38 (actual count); 8 PARKs -> 7 (b5 was renewed to 2027-02-08 on 2026-08-16, before this spec's own 2026-08-18 date). All found by the same 2026-08-19 adversarial review as the BLOCKERs above (confirmed CONCERNs, not blocking on their own). | Claude Code |
| 2026-08-19 | §12's log-append template gained two fields, `Evidence-Cited` and `Deviation-from-Precedent`, filled from data the synthesis pass and the prior-log read already produce -- not new data collection. Sourced from a landscape survey of 2025-2026 multi-agent memory practice (arXiv:2508.08997, "Intrinsic Memory Agents": uniform structured per-role templates beat free-text logs on both role-adherence and token efficiency); the survey found the three other fields the source proposed (Artifact-Reviewed, Verdict, Ratified-or-Overridden) were already covered by this template's existing minimum contract. Record-keeping only, explicitly non-gating (new §12 closing paragraph) -- existing entries are unaffected, no synthesis is blocked for an incomplete log. Dispatch-eligibility checked against `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §2 routing test 1 ("does the task author doctrine... -> CC, full stop") before authoring: this file is the content-of-record for an `Accepted` ADR, so the edit stayed on this surface rather than routing to Cursor. | Claude Code |
| 2026-08-19 | §10.1 added -- preference-anchoring companion check, a distinct H′ from the main §10 falsifier. Sourced from 2026 research on stateful personal agents (durable-memory agreement-bias/failure-rate escalation on repeated retrieval) applied to the fact that persona memory (§6.4) is exactly the durable, read-before-every-spawn condition that research names as the trigger. Check: at every 5th real log entry, watch for agreement-rate-rising AND findings-count-falling *together*, not agreement alone. Manual/periodic, not automated tooling; non-counting, tagged the same way §13's rehearsal entries already are. Dispatch-eligibility checked against the surface-allocation ADR before authoring, same test as the row above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | §14 added -- a one-time MAST pre-mortem procedure (arXiv:2503.13657, Cemri et al., NeurIPS 2025), checking the panel's own review PROCESS rather than §10's outcome-only measure. Read the full 14-mode taxonomy (previously only the 3-category summary was known); scoped down to the 9 modes actually reachable given this panel's fan-out, single-shot-call architecture (never a conversing multi-agent system), naming and excluding the other 4 (loss of conversation history, unaware of termination conditions, conversation reset, fail to ask for clarification) as architecturally inapplicable rather than silently dropping them. Run once per real panel use (not rehearsal-inclusive, not a standing recurring gate) against `journal.jsonl`; no new persona minted, extends Head of Governance's existing mandate if a standing owner is ever needed. Dispatch-eligibility checked, same test as the rows above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | §9 gained an "Architectural correlation" bullet, and §6.2 gained a one-line cross-reference to it: fresh-context spawning (already built) prevents contextual contamination but not architectural correlation between personas that likely share one model family's blind spots and sycophancy pull, per 2025-2026 LLM-judge-collusion literature. No mitigation proposed -- documentation only, so "fresh subagents" is never silently read as having solved a risk it only partially addresses. Smallest item on the docket: no code, no new structure, no forward obligation. Dispatch-eligibility checked, same test as the rows above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | §6.3 gained a drafted-not-wired-in extension: a deterministic `flagIndependentDissent`-shaped mechanic (diverging severity + non-matching `location` between two personas' findings) sketched as the frozen spec for a future synthesis-prompt addition, explicitly held until §10's N=3 falsifier clears (currently 1/3 -- GSUB-2). No code touched `.claude/workflows/pre-ratification-adversarial-panel.js` in this commit; the paragraph is the spec, not the patch. Narrowed from an earlier trained-classifier proposal to this purely syntactic, deterministic form specifically so it doesn't reopen the CRO hard-block's status as the sole non-advisory dissent case. Dispatch-eligibility checked, same test as the rows above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | §10.2 added -- self-consistency companion checkpoint, a distinct H′ from the main §10 falsifier. Sourced from a 2026 benchmark finding automatically-designed multi-agent systems can underperform a single agent's Chain-of-Thought self-consistency at a fraction of the cost. Check: on the first 1-2 real GRAND reviews, spawn 3 extra same-persona CRO samples alongside the real run and compare majority-vote agreement -- an AI-vs-AI measurement, explicitly distinct from and not a substitute for the human-ground-truth §10 falsifier. No workflow-file code change; runs as an ad hoc side call. Non-counting, tagged the same way §13's rehearsal entries already are. Dispatch-eligibility checked, same test as the rows above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | §6.7 added -- persona retirement procedure for an individual seat, distinct from §10's whole-panel demotion disposition. Modeled on this repo's own Great Prune precedent (66/69 candidate deletions rescued on adversarial review before that PR merged): operator-decided trigger only, 5-step freeze/reassign/archive/index/ratify-before-merge sequence routing through PR review the same way Great Prune itself was ratified, never auto-executed. Dropped the source proposal's "disable endpoints/credentials" step -- no literal referent, since personas are fresh per-review spawns with no standing credentials; step 4 (index update) already covers the intent. Dispatch-eligibility checked, same test as the rows above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | §6.4.1 added -- charter versioning (§12 template gains a third field, `Charter-Commit`, the short SHA of the persona's own `.md` file at spawn time -- no code change, filled at log-append time) and a bounded, Governance-gated self-refinement procedure: a persona may propose (never silently apply) a charter edit on a pre-registered trigger (2 consecutive real entries where Joshua's ratification diverges from the persona's own recommendation, same root cause), but for control-layer personas (CRO, Head of Risk & Sizing, Model Validation Analyst, Head of Governance itself) the proposal must clear an independent Head of Governance read before Joshua ever sees it -- otherwise a control-layer persona would be auditing its own proposed redefinition, the exact failure §5.2.1 already reasoned through once for Governance's own placement. Closes this docket's last open item; final item in the sequence. Dispatch-eligibility checked, same test as the rows above -- stayed off Cursor. | Claude Code |
| 2026-08-19 | **Packet-wide adversarial review (46 agents, 6 lenses + double-skeptic verify, run against the full document post the 8-item sequence above) -- disposition `BLOCKED`, 14 confirmed findings + 1 disputed.** Two are genuinely defects in this pass's own §14 addition, fixed here: the MAST framework-count citation (150-trace/κ=0.88 set is 5 frameworks, not 7 -- that figure belongs to a separate 1,600+-trace corpus), and §14's mode-count arithmetic (4 excluded + 9 listed = 13, one short of the stated 14 -- the published taxonomy's two "Disobey" modes were bundled into one row; now split into two, making a true 10-row table). The rest were pre-existing, found in passing in the same file by the same run (matching this document's own established convention, see the §6.6 fix-in-passing rows above): §2/Ratification-note's "c1 Q-XMEM-1... parked" (SUBTRACTed via GSUB-2 same day, never updated); §2.1's "~20 new permanent artifacts" not summing to its own listed components (corrected to 21 existing-at-authoring-time + up to 18 accruing later, explicitly separated; also fixed the adjacent 18-vs-19-persona-file undercount, `ceo.md` exists on disk); §8's stale "7 of 8" PARK count (5 remain once GSUB-2's same-day b2/c1 SUBTRACTs are counted, not just b5's renewal) and its misattribution of "belt that only grows" to GSUB-1's retrospective (the phrase originates in the GRAND ADR; GSUB-1's own retrospective found a different failure shape -- ownerless drift, not volume); §6.6's CRO carve-out citing "the ADR's own §4" for a rule that only exists in this spec's own §4; §2's D-user-gate line citation (L282 -> L284); §6.2's SR-11-7 phrase de-quoted as an acknowledged paraphrase, not the letter's literal wording. Also added, from the run's Steelman and structural-completeness lenses: a named limitation connecting §9's architectural-correlation risk to §10's own falsifier (it cannot distinguish a redundant panel from a panel sharing the operator's blind spot), and a new §15 Watch-items index consolidating every "held/not-yet-active/named-risk" item into one place. **Not fixed here, flagged for a separate operator decision:** the run's #1 confirmed BLOCKER (the §6.6 self-review's own claimed run IDs/agent-counts and the ADR's D2 regression-run claim have no recoverable artifact anywhere in the repo) and the disputed dedup-first-attestation severity call -- both live partly or fully in `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`, an `Accepted` ADR whose ratified body this repo's convention keeps byte-unedited (amendments via addendum, not direct edit) -- out of scope for a same-surface doc-text fix and requiring an operator call on how to characterize unrecoverable prior-session evidence. | Claude Code |
| 2026-08-19 | **Resolves the row above's flagged BLOCKER/disputed item, discovered on `git push`.** A parallel session (PR #59, `cursor/persona-hierarchy-spec-staleness-1583`) had independently found and fixed an overlapping subset of the same §6.6 spun-off punch list this document's own Change History already named -- the D-user-gate line cite, §5.2's "direct match" labels, §11/Ratification-note staleness, the GRAND ADR §5 forbidden-move quote, §13's unbacked "19 agents" figure, *and* the ADR's dedup-first attestation + "32 agents" self-review claim -- landing on `main` before this branch pushed. A `git merge origin/main` produced real conflicts (not a silent bad merge) on the D-user-gate/§11/Ratification-note text, where origin's wording was kept (equivalent substance, more precise); PR #59's ADR-side fix was kept as-is rather than duplicated. The ADR's own addendum (drafted in response to the row above) was narrowed on merge to cover only what PR #59's fix did not reach -- see `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` Change History for the full account. | Claude Code |
| 2026-08-19 | §5.3 gained a ninth Staff seat, Research Analyst (reports to Head of Research) -- the first producer-type seat on this roster; every prior Staff persona is a review/gate function per this section's own SR-11-7 licensing test, so the departure is called out in a new architectural note directly under the table rather than blended silently into it. Inaugural standing project: decompose active/archived research into atomic, statistically-important facts assembled into per-instrument profiles, starting with MNQ (a3), ahead of a CIO + Head of Research meeting on the idea. `docs/personas/research-analyst.md` added, `docs/personas/INDEX.md` gained its row, and `scripts/check_personas.py`'s `EXPECTED_COUNT` moved 19 -> 20 in the same change (this session's own count, on a parallel branch -- see the merge-reconciliation row below for the number that actually survived). Ratified by Joshua, in-session direct instruction ("I want to create the research analyst persona ... our newest member of the research team"). | Joshua + Claude Code |
| 2026-08-19 | **Operator-authorized simplification pass, same day as ratification, per `docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md` (4-reader-agent audit + an independently-spawned Head of Governance review that flagged its own spawn as outside its literal strict-D2 trigger and marked itself `Rehearsal: yes`).** Archived to `docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md` (verbatim text preserved, not deleted): §6.3's citation-diff/dissent-flag addendum, §6.4.1 (charter versioning + self-refinement), §6.6 (cross-examination round), §10.1 (preference-anchoring check), §10.2 (self-consistency checkpoint), §12's extended log-append fields (Evidence-Cited/Deviation-from-Precedent/Charter-Commit), §14 (MAST pre-mortem). Every one of the seven had zero executions from ratification to archival; none is a "proven wrong" verdict, only "never used, archived rather than carried as live spec weight." §5.3's Staff table collapsed from 8 to 3 active personas -- the 5 Middle/Back-office analysts that were never spawned (Risk Analyst (Intraday), Model Validation Analyst, Robustness Analyst, Documentation Analyst, Research Registry Analyst) moved to `docs/personas/archive/` via `git mv`, retired per this document's own §6.7 procedure; the 3 Front-office Staff (Falsifier Analyst, Pre-Registration Analyst, TCA Analyst) were explicitly excluded from the cut at operator instruction (in active use in a parallel session) and are unaffected. `scripts/check_personas.py`'s `EXPECTED_COUNT` updated 19 -> 14 to match. §15's Watch-items index updated to point at the archive instead of listing these as held-pending-trigger. What was **not** cut: the CRO safety-invariant hard-block (§6.3's core exception), the GRAND tier, §6.1-6.2/6.4-6.5/6.7 base mechanics, the 3 Front-office Staff personas, and the ownership map -- all independently confirmed load-bearing by the audit (real logged output, or deterministic code wired into the pipeline that actually runs). Nothing here reopens the ratification (§1-§11, D1-D5) or the CRO hard-block's status. | Claude Code (operator-authorized) |
| 2026-08-19 | **Correction to the row above, same day, after operator pushback.** Operator pushed back on the archival pass before merge: "push back on archiving all of the spec extensions and STAFF personas, because they are brand new and haven't had a chance to be used yet... test them to see if they would earn their keep based on existing evidence we have in the repo." Re-tested every archived item against real, already-existing evidence (GSUB-2's preserved panel journal `wf_e016a5d9-3f6`; retroactive spawns against real repo artifacts) rather than leaving "never fired" unexamined. Result: §14 MAST **restored** (run for real, found 2 genuine findings the panel's own verify stage hadn't caught -- falsifies the original "duplicated by a higher-fidelity source" rationale). §10.2 self-consistency **discharged, not restored** (actually run: 3 blinded CRO resamples against the frozen GSUB-2 artifact, majority matched the real verdict; logged at `docs/personas/cro-log.md`; stays archived since it was always a bounded 1-2-use diagnostic, now used). §6.3 citation-diff **stays archived on stronger evidence** (the deterministic rule was run against GSUB-2's real findings and produced a false positive -- flagged two unrelated findings as "dissent" purely on severity+location mismatch; needs redesign, not just N=3 data). §6.6/§6.4.1/§10.1 **confirmed genuinely blocked on data** (checked real panel history directly for each trigger precondition; none has fired -- not the same claim as "unused"). Of the 5 archived Middle/Back-office Staff personas, 2 (Documentation Analyst, Research Registry Analyst) were spawned against real repo artifacts and each found a genuine, previously-uncaught defect in `docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md` itself on first use -- restored to `docs/personas/`, first log entries at `docs/personas/documentation-analyst-log.md` / `docs/personas/research-registry-analyst-log.md`. The other 3 (Risk Analyst Intraday, Model Validation Analyst, Robustness Analyst) came back clean against the one target tried (a CME data-panel ADR outside all three domains) -- inconclusive, not negative; stay archived pending a better-fitting target. `check_personas.py` `EXPECTED_COUNT` updated 14 → 16. Full account in `docs/notes/audits/2026-08-19-governance-friction-persona-panel-audit.md`'s Disposition section. | Claude Code (operator-authorized, after operator pushback) |
| 2026-08-20 | **Merge reconciliation.** `git merge origin/main` on the Research Analyst branch produced real conflicts on this table (not a silent bad merge) between the row above and the Research Analyst row two above it -- both are genuine, non-overlapping same-day history (Research Analyst on a parallel branch was unaffected by, and unaware of, the archive/restore cycle run in a different session). Both rows kept verbatim, in the order they're written above. `scripts/check_personas.py`'s `EXPECTED_COUNT` reconciled to the actual merged roster count: 16 (post-restore, this session) + 1 (Research Analyst, parallel branch) = 17, confirmed against `docs/personas/*.md` on disk. | Claude Code |

## 12. Post-workflow log-append procedure (added during Phase 2 implementation; template extended
2026-08-19 -- see Change History)

After a persona-mode `Workflow` call returns, for each slug in `result.personaSlugs`:

1. Read `docs/personas/<slug>-log.md` if it exists; treat as empty (first entry) if not.
2. Extract that persona's verdict from `result.synthesis` (the synthesis memo names each
   persona's confirmed/disputed findings by lens key).
3. Append (never edit prior entries) a new entry using this exact template, with today's date filled
   in by the calling session (never computed inside the Workflow script):

```markdown
## <YYYY-MM-DD> — <result.targetPath>

**Verdict:** <BLOCKED | CLEAR-WITH-CONCERNS | CLEAR, from result.synthesis for this persona>
**Confirmed findings:** <count, or "none">
**Ratified as recommended:** <Yes | No | Pending -- operator has not yet ratified>
```

4. If `result.croHardBlock` is true, every persona's log entry for this review additionally carries
   a line: `**CRO hard block fired:** yes -- disposition is BLOCKED regardless of this persona's own verdict.`

**ARCHIVED 2026-08-19 (operator-authorized cut; see Change History):** an extended template adding
`Evidence-Cited`, `Deviation-from-Precedent`, and `Charter-Commit` fields, plus §6.4.1's charter-
versioning mechanic that produced the third field. `check_personas.py`'s `LOG_REQUIRED_SUBFIELDS`
was never updated to enforce any of the three, and no real log entry ever used them. Full text
preserved at
[`docs/superpowers/specs/archive/2026-08-19-persona-hierarchy-archived-sections.md`](archive/2026-08-19-persona-hierarchy-archived-sections.md#12--extended-log-append-template-fields-evidence-cited-deviation-from-precedent-charter-commit).
Re-propose together with the code change that would make the fields load-bearing, not as prose
alone.

## 13. Rehearsal record (added during Phase 3 implementation)

**2026-08-19 — retroactive dry run, NOT a real falsifier data point.** Ran the persona-mode panel
(GRAND tier, personas `cio`/`coo`/`cfo` + auto-added `cro`, confirming the mandatory-GRAND-CRO rule
fires mechanically) against the already-closed GSUB-1 inventory
(`docs/briefs/GSUB-1-inventory-and-dispositions.md`) purely to prove the mechanism produces sensible
independent output and writes well-formed logs. Outcome: overall disposition **CLEAR-WITH-CONCERNS**
— one CONCERN confirmed unanimously by both independent skeptics (an unanchored §0 Rule-0 citation),
two BLOCKERs and three further CONCERNs raised and all unanimously refuted on independent re-read
(including a real case of a reviewer missing a same-day resolving ADR reachable from the very row it
cited — exactly the kind of miss the verify stage's independent skeptics exist to catch),
`croHardBlock: false`. 19 agents, ~10.6 minutes wall-clock *(as-reported; no workflow run ID or
journal path was preserved in-tree — searched commits `7032184` / `55012da`, PR #54/#56 bodies,
persona logs, and `docs/SESSIONS.md`; none carry a `wf_*` id for this rehearsal, unlike the sibling
convention at
[`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`](../../notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md)
§0)*. Because GSUB-1 was already ratified and
closed before this mechanism existed, this run **cannot** change a ratified outcome and therefore does
not count toward the §10 falsifier ("does panel input ever change a ratified outcome"). The first real
data point toward that falsifier can only come from a genuine future GRAND or strict-D2
STRATEGIC-tier decision reviewed *before* ratification. Every log entry this rehearsal wrote
(`docs/personas/{cio,coo,cfo,cro}-log.md`) carries an explicit `**Rehearsal:** yes` line for exactly
this reason -- so a future reader of `docs/personas/*-log.md` never mistakes rehearsal output for a
real review.

**Addendum 2026-08-19 (same day, later) — the "future" arrived: real data point 1/3.** Immediately
after this rehearsal, [`GSUB-2`](../../briefs/GSUB-2-park-cohort-early-review.md) ran the first
genuine pre-ratification GRAND-tier panel review (CIO/COO/CRO against a frozen SUBTRACT-candidate
proposal, verdict `CLEAR-WITH-CONCERNS`, one confirmed CONCERN fixed before ratification) and its
[closure](../../briefs/closures/GSUB-2-closure-resolved-loadbearing.md) states explicitly: "this is
real data point 1 of the needed 3." The persona-hierarchy ADR's own §4 tracker is the canonical
count, not this line — restated here only so this section stops reading as if that first real
review still lay entirely in the future, which it no longer does.

## 14. MAST pre-mortem procedure (added 2026-08-19; briefly archived and restored same day — see
Change History)

A one-time, read-only process check against the panel's own mechanism — distinct from §10's
falsifier, which measures OUTCOME only ("does panel input ever change a ratified disposition").
Sourced from Cemri, Pan, Yang et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv:2503.13657,
NeurIPS 2025 Datasets & Benchmarks) — MAST, an empirically-derived 14-mode taxonomy of multi-agent
failures, built from 150+ expert-annotated traces (κ=0.88 on the IAA subset) across 5 MAS
frameworks.

**Scope, narrowed to this panel's actual architecture.** MAST was built from systems where agents
converse (AutoGen, ChatDev, AppWorld). This panel is a fan-out of independent, schema-constrained,
single-shot `agent()` calls across three pipeline stages (Review → Verify → Synthesize) — never a
live back-and-forth dialogue. Four of the 14 modes assume a conversation that doesn't exist here
and are excluded by architecture, not oversight: loss of conversation history, unaware of
termination conditions, conversation reset, fail to ask for clarification.

The other ten modes map onto this panel's actual stages:

| Mode | Stage | Check |
|---|---|---|
| Disobey task specification | Review | Did the persona's finding stay inside the target artifact's actual subject matter, not a different task? |
| Disobey role specification | Review | Did the persona's finding stay inside its stated Domain (`docs/personas/<slug>.md`)? |
| Task derailment | Review | Does `notes`/`findings` actually address the target artifact? |
| Information withholding | Synthesize | Does every CONFIRMED/DISPUTED finding in `lensResults` surface in the synthesis memo? |
| Ignored other agent's input | Synthesize | Does the memo engage with a persona that said `clean:true` with a substantive rationale? |
| Reasoning-action mismatch | Review + Verify | Does a finding's `why_wrong` support its `severity`? Does a skeptic's `rationale` support its `refuted` call? |
| Premature termination | Review | Is a `clean:true` result backed by specific section/line engagement, not a generic one-liner? |
| No/incomplete verification | Review + Verify | Open every cited `location` and confirm it exists and says what's claimed. |
| Incorrect verification | Verify | Re-check a sample of the Verify stage's own `refuted` calls independently. |
| Step repetition | Verify (weak) | Do the two independent skeptic votes read as genuinely independent, or templated restatement of each other? |

**Cadence — one-time per real panel use, up to the first 3 (§10's own falsifier count), not
periodic.** No standing owner — Joshua or CC runs the checklist directly; extends Head of
Governance's 3rd-line mandate (§5.2.1) if one is ever needed.

**Findings — run 1/3, 2026-08-19, against GSUB-2's real panel journal (`wf_e016a5d9-3f6`,
preserved).** Two real hits, both worth carrying forward, neither BLOCKER-severity against GSUB-2
itself (already ratified, not reopened by this note):
- **Ignored other agent's input:** the GSUB-2 synthesis memo never engages with CRO's `clean:true`
  verdict — the most domain-comprehensive review of any lens in that run (checked all 8 rows
  against every named safety invariant) — at all. Recommendation: synthesis prompts should name
  and briefly credit at least one `clean:true` rationale per run, not only report confirmed/refuted
  findings.
- **Incomplete verification, self-corrected:** the original CIO-lens BLOCKER finding
  (`docs/briefs/GSUB-2-park-cohort-early-review.md` §7 Phase 2.5) quoted `cio.md` by trimming its
  leading "Front-office oversight:" qualifier before the narrower enumeration — a real, if minor,
  citation-integrity defect at the Review stage. Caught and refuted at the Verify stage by a
  skeptic who explicitly re-read the untrimmed source ("I re-read all the cited files directly, not
  the reviewer's paraphrase"). The two-stage architecture worked as designed; the defect it caught
  is itself the evidence this check adds value beyond what the existing verify stage already
  covers — the verify stage checks whether a *conclusion* survives re-reading the source, not
  whether a *citation was quoted in full*, and this is the distinction that let the trim slip
  through to the finding-authoring step in the first place.

This directly falsifies this section's own original archival rationale ("duplicated by a
higher-fidelity source already in the corpus") — see Change History.

## 15. Watch-items index (added 2026-08-19)

A pointer collection, not new content — every item below is already fully specified in its own
section; this just answers "what in this design is deliberately not-yet-active, or a named-but-
unmitigated risk" in one place. Closes a structural-completeness gap a same-day adversarial review
flagged: each item below was already individually labeled where it lives, just never indexed
together.

- **§6.3, drafted-not-wired-in dissent flag** — ARCHIVED 2026-08-19, and stays archived on
  stronger evidence than "unused": the deterministic rule was run against GSUB-2's real findings
  and produced a false positive (flagged CIO's BLOCKER and COO's unrelated CONCERN as
  "independently-sourced dissent" purely on severity+location mismatch, though the two findings
  aren't about the same question). Needs redesign — a same-item/same-nomination constraint, not
  just non-matching `location` strings — before re-proposing, not just N=3 data. See archive.
- **§6.4.1, charter versioning / self-refinement** — ARCHIVED 2026-08-19; checked 2026-08-19
  whether its trigger (2 consecutive divergent ratifications) has fired anywhere in real panel
  history — it hasn't (1 real review, 0 divergence). Genuinely blocked on data, not deprioritized.
  See archive.
- **§6.6, cross-examination round** — ARCHIVED 2026-08-19; checked 2026-08-19 whether its trigger
  (a disputed, non-unanimous Stage-1 finding) has fired anywhere in real panel history — it
  hasn't: GSUB-2's own synthesis states "No lens finding landed in a genuinely split... state."
  Genuinely blocked on data. See archive.
- **§9, architectural correlation** — a named, unmitigated risk in the independence mechanic; no
  fix proposed. Not archived — this is a live-standing caveat on the mechanism as built, not a
  not-yet-active extension.
- **§10, falsifier/architectural-correlation limitation** — the H/Falsifier cannot distinguish a
  redundant panel from a panel sharing the operator's own blind spot. Not archived, same reason.
- **§10.1, preference-anchoring companion check** — ARCHIVED 2026-08-19; checked 2026-08-19 against
  real log depth — deepest persona log (CRO) has 3 entries, trigger needs 5. Genuinely blocked on
  data. See archive.
- **§10.2, self-consistency companion checkpoint** — exercised retroactively 2026-08-19 against the
  frozen GSUB-2 artifact (3 fresh blinded CRO samples, majority `clean:true`, matched the real
  panel's CRO verdict) — result logged at `docs/personas/cro-log.md`. Discharged as the bounded
  1-2-use side experiment it was designed to be; not restored to live spec text since nothing about
  it is meant to be standing. See archive for the pre-exercise text.
- **§14, MAST pre-mortem procedure** — **restored to §14 above, 2026-08-19**, after being briefly
  archived then run for real against GSUB-2's preserved journal and surfacing two genuine findings.
  No longer archived.

Was: six watch-items archived as not-yet-active. After operator pushback ("test them against
existing evidence before archiving") and an actual test pass per item: 1 restored (§14, earned it),
1 discharged (§10.2, ran once, done), 3 confirmed genuinely blocked on data that doesn't exist yet
(§6.4.1, §6.6, §10.1 — not the same claim as "unused"), 1 stays archived on stronger evidence than
before (§6.3 — tested and found to produce a false positive, not just untested).
