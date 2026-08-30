# Operator approvals — one campaign envelope up front, and the frozen multiplicity configuration that keeps confirm attempts from becoming a spend backdoor — `operator-approvals-campaign-envelope`

**Status:** `Proposed`
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Amends-in-part:** `2026-08-30-candidate-contract.md` — freezes the multiplicity-configuration field
(`α`, the confirm count `M`, and the named Bonferroni-or-Holm procedure identity) that ADR's own §3
named as deferred to "the ADR that actually needs it"; the campaign-envelope field itself is
**already** in that ADR's founding baseline list and is not re-added here — this ADR rules its
approval mechanics, not its existence.
**Layer:** methodology (operator-approval ceremony and confirm-attempt accounting only). No
`dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue
action; this ADR sets **how** spend gets approved, never a spend amount itself.
**Tier:** full — Limb 4 fires (creates standing doctrine binding every candidate contract's
approval and multiplicity-accounting mechanics).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, this session (2026-08-30):

- `docs/notes/2026-08-30-generate-evaluate-tensions.md` — anchor `419433a` (2026-08-30). "Simplify
  operator approvals" row: approve one campaign envelope up front (spend, schemas, windows, K);
  confirm attempts are not a separately spendable item — bound to the frozen multiplicity
  configuration set at contract freeze; any `VOID-*` result exhausts the attempt and requires a
  fresh campaign with a fresh holdout, never a retry inside the same envelope; another GO is
  required only to exceed the envelope or cross into sandbox/capital. Generate-phase step 3 (the
  pre-freeze shape-extraction probe's own operator-approved envelope, approved before any data
  access since the campaign envelope itself is not recorded until freeze) and step 5 (the
  Bonferroni-vs-Holm freeze mechanics: Bonferroni's fixed `α/M` per-candidate bar freezes now; Holm's
  per-candidate thresholds `α/(M−i+1)` attach only after observed confirm p-values are ordered, so
  what freezes is the algorithm identity, not pre-assigned numbers) supply this ADR's operative
  mechanics.
- `docs/adr/2026-08-30-candidate-contract.md` — anchor `7669664` (2026-08-30, this branch). §2's
  founding baseline already lists "the campaign envelope it opens under" as a contract field; §3
  explicitly names "the multiplicity configuration (α/M/procedure)" as a field deferred to a
  separate ADR, and rules that folding it into ADR-1 itself "would violate 'ADRs document ONE
  decision.'" This ADR is that separate decision.
- `docs/adr/2026-08-30-evaluation-order.md` — anchor `1c58ee1` (2026-08-30, this branch). Step 7
  (contract-integrity check) cites "the frozen multiplicity configuration (owned by
  `2026-08-30-operator-approvals-campaign-envelope.md`, cited not re-decided here)" — this ADR is
  that forward-cited decision, matching the filename that ADR already committed to.
- `docs/adr/2026-08-30-tradeable-reachable-gate.md` — anchor `a682b74` (2026-08-30, this branch).
  §2's payoff-shape bullet: the pre-freeze shape-extraction probe is "run only under its own
  operator-approved probe envelope (spend ceiling, schema, window, and K ceiling frozen at
  declaration, approved before any data access)... the step-5 campaign envelope then subsumes the
  probe tranche by citation" — asserted there but not reconciled in detail; this ADR's §2 rules the
  reconciliation mechanics (how a pre-freeze probe tranche composes with the main campaign envelope
  approved at freeze).
- `docs/adr/2026-08-30-terminal-taxonomy.md` — anchor `1c58ee1` (2026-08-30, this branch). §2:
  `EVIDENCE-VOID` exhausts a confirm attempt without a terminal registry destination — the exact
  disposition this ADR's "any `VOID-*` result... requires a fresh campaign" rule fires on.
- `docs/methodology/avenue_a_generate_confirm.md` — anchor (Route B checklist, `Superseded` in full
  by the 2026-08-24 channel retirement, §0 of `2026-08-30-channel-liveness-gate.md`). L88: "Confirm-
  budget M + multiplicity bar... If M > 1, the per-candidate confirm threshold is Bonferroni/Holm-
  adjusted for M" — a real precedent for this ADR's `α`/`M`/procedure naming, found via this ADR's
  own Phase-2 sweep (§7). This ADR **generalizes** that retired route's single-checklist-line
  convention into a standing, contract-frozen field for every channel, rather than inventing the
  `M`/Bonferroni/Holm vocabulary from nothing.
- `docs/adr/2026-06-16-rule-2-budget-before-acting.md` — anchor `e11fd39` (2026-08-24). §2 D1: an
  **iteration**-budget tripwire (INNER 3 / OUTER 8 / STRATEGIC 3 constituent investigations),
  scaled to reversibility, for research/investigation *work effort*. A different axis from this
  ADR's campaign envelope (data spend, K, schema, window ceilings) — the two compose (a campaign can
  blow its iteration budget without touching its dollar/K envelope, or vice versa) and neither
  supersedes the other; this ADR does not re-decide Rule 2's tripwire mechanics.
- `docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md` — anchor `e11fd39` (2026-08-24). The one
  ratified exception to down-only automation — cited by this ADR's "another GO... to cross into
  sandbox/capital" clause (§2) as the destination that clause points at; this ADR does not redefine
  S5's own bounds.

---

## §1 — Context

Today, exploration and confirmation each accumulate separate, informally-timed permission requests
— a spend ask here, a schema question there, an implicit re-ask whenever confirm data gets
consulted again after a `VOID` result. Nothing states that a single up-front envelope is the unit of
operator authorization, and nothing states that confirm attempts are *bound* to a frozen multiplicity
configuration rather than being a separately-negotiable resource each time. The risk this creates is
concrete: repeatedly re-consulting confirm data within one "approved" scope, each time under a fresh
informal ask, is exactly the multiplicity-inflation pathway the untouched-holdout discipline exists
to prevent — the approval process itself can silently become the leak.

A second, narrower gap: `2026-08-30-tradeable-reachable-gate.md` already requires a pre-freeze
shape-extraction probe to run "under its own operator-approved probe envelope," approved before any
data access because the campaign envelope itself doesn't exist until the contract freezes later —
but that ADR only asserts the probe tranche is "subsumed by citation" at freeze, without ruling what
happens if the probe's actual spend differs from what gets cited, or what a probe-then-no-campaign
outcome means for the ledger.

**Decision driver (one sentence):** the estate needs one operator-approval unit per campaign instead
of scattered re-asks, and a frozen multiplicity configuration that makes "confirm attempts are not a
separately spendable item" mechanically true rather than aspirational.

---

## §2 — Decision

**Decision:** Every candidate contract carries exactly one operator-approved **campaign envelope**,
approved up front, and one **frozen multiplicity configuration** set at contract freeze that binds
every confirm attempt inside that envelope.

**The campaign envelope.** Approved once, before Explore begins: maximum spend, data schemas,
exploration and confirm windows, and K. This is the sole standing authorization for the campaign's
data and compute costs. No separate approval is asked for a schema clarification, a window question,
or any action that stays inside the approved envelope — those are implementation detail, not new
spend.

**Confirm attempts are not a separately spendable envelope item.** They are bound to the multiplicity
configuration below, frozen at contract freeze (`2026-08-30-candidate-contract.md` §2), for the life
of the envelope. An `EVIDENCE-VOID` result (`2026-08-30-terminal-taxonomy.md` §2) exhausts that
attempt and requires a **fresh campaign with a fresh holdout** — never a retry inside the same
envelope, and never a fresh "ask" to re-consult the same confirm data. This is the mechanical form
of the anti-inflation requirement: an operator cannot informally re-approve another look at the same
holdout by treating it as a new permission request, because the envelope's own terms already forbid
it.

**The frozen multiplicity configuration.** Three fields, frozen at contract freeze, never revised
mid-campaign:
- **`α`** — the family-wise significance level for the confirm family.
- **`M`** — the confirm count: how many candidates the frozen exploration selection may advance to
  confirm (`2026-08-30-evaluation-order.md` step 6's selection freeze pins the actual selected set;
  `M` is its ceiling).
- **The named procedure** — either **Bonferroni**, whose fixed per-candidate bar `α/M` is a number
  frozen at contract freeze, or **Holm step-down**, whose per-candidate thresholds `α/(M−i+1)`
  cannot be pre-assigned by candidate (they attach only after the observed confirm p-values are
  ordered) — so what freezes under Holm is the **algorithm identity**, not a table of numbers. A
  contract must declare one procedure; a contract silent on procedure is integrity-invalid at
  `2026-08-30-evaluation-order.md` step 7 (contract-integrity check).
- A slot with no adjudicable statistic (forfeited `ROLE-BLOCKED`, voided `EVIDENCE-VOID`, or simply
  unfilled because Explore selected fewer than `M`) enters the step-down as the frozen conservative
  placeholder **`p = 1`**: the family stays size `M`, the ordering algorithm stays executable, and a
  missing test can only make every remaining rejection harder, never easier. This applies under both
  named procedures — Bonferroni's fixed bar needs no placeholder mechanics, but the family size `M`
  itself never shrinks to accommodate an unfilled or voided slot.

**Distinct from the K-ledger's own selection-under-K correction.** `register_search.py`'s
Bonferroni/BH-FDR triage at manifest `close` (`2026-08-15-no-counterparty-statistical-sourcing-
channel.md`, `2026-07-10-databento-research-stack.md`, §0) corrects for the **catalogue-selection**
question — how many cells were examined before a candidate was picked at all. This ADR's `α`/`M`/
procedure corrects a **later, separate** question — the family-wise error of the `M` candidates that
already survived selection and now face confirm. The two corrections are sequential and cumulative,
not alternatives; this ADR does not alter the K-ledger's own mechanism or ownership.

**Probe-tranche reconciliation.** A pre-freeze shape-extraction probe
(`2026-08-30-tradeable-reachable-gate.md` §2) is approved under its **own** operator-approved
envelope — spend ceiling, schema, window, K ceiling — declared and approved before any data access,
since the campaign envelope does not exist until freeze. At freeze, if the campaign proceeds, the
probe tranche's actual realized spend and K are cited into the campaign envelope's own record as an
already-spent sub-line — the campaign envelope's own ceiling is set inclusive of that citation, never
silently topped back up as if the probe tranche were free. If the candidate does not reach freeze
(the probe itself kills it, e.g. no citable shape emerges and no campaign is opened), the probe
tranche is never subsumed by anything — it stands alone as its own closed, already-approved spend,
attributed to the mechanism's own record, not orphaned or double-counted against a campaign that
never existed.

**Escalation.** Another operator GO is required only to (a) exceed the approved envelope (spend,
schema, window, or K), or (b) cross into the bounded sandbox-up promotion lane or any capital-facing
action (`2026-08-07-loop-s5-bounded-promotion-lane.md`, §0 — cited, not redefined here). Neither
escalation path is a routine step; both require a fresh, explicit operator decision, never inferred
from silence or from the campaign envelope's own approval.

**Composition with Rule 2.** The campaign envelope (this ADR) and Rule 2's iteration-budget tripwire
(`2026-06-16-rule-2-budget-before-acting.md`, §0) are different axes — one bounds data/compute spend
and confirm-attempt multiplicity, the other bounds research work-effort — and compose without
conflict: a campaign can be well inside its envelope while blowing its iteration budget (a STOP
signal on the effort axis alone), or vice versa. Neither this ADR nor Rule 2 is amended by the other.

**Effective:** immediately upon acceptance, for any candidate contract frozen after this date.
**Scope:** operator-approval ceremony and multiplicity-configuration freeze, across all six live
channels. Does not alter Rule 2's tripwire mechanics, S5's own bounds, or any cited ADR's own
thresholds — it rules the campaign envelope's approval unit and the multiplicity fields
`2026-08-30-candidate-contract.md` deferred here.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep separate permission points for exploration and confirmation, as today | This is the status quo the note's row diagnoses as the actual multiplicity-inflation risk — a re-ask each time confirm data is revisited is functionally a re-approval of the same holdout look, undetected as such. |
| Let a `VOID-*` result be retried inside the same envelope with fresh operator sign-off | Reintroduces exactly the informal-re-ask leak this ADR exists to close; a fresh campaign with a fresh holdout is the only way "the confirm attempt is exhausted" stays mechanically true rather than negotiable. |
| Fold the multiplicity configuration into `2026-08-30-evaluation-order.md` instead, since that ADR's step 7 checks it | `2026-08-30-candidate-contract.md` §3 already named this a separate decision from evaluation order, and `evaluation-order.md` §3 itself declined to claim the field for exactly this reason — duplicating ownership across two ADRs risks inconsistent definitions. |
| Treat the shape-extraction probe's spend as free once subsumed into the campaign envelope | Would let a probe-then-campaign pattern under-report real spend against the campaign's own ceiling — the reconciliation rule (§2) requires the ceiling be set inclusive of the cited probe spend, never topped back up. |
| Require a fresh operator GO for every escalation, including staying inside the approved envelope | Reintroduces the exact throughput-scheduler problem the note's row names ("the operator [becomes] the throughput scheduler rather than the risk owner") — the whole point of one up-front envelope is that in-envelope work needs no further asking. |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** one up-front campaign envelope plus a frozen multiplicity configuration correctly
prevents confirm-attempt/spend inflation via informal re-asks, without either starving a legitimate
campaign of needed flexibility or silently under-reporting probe-tranche spend.

**Revert trigger:** if, by the next scheduled quarterly programme audit after this ADR's acceptance,
either (a) a candidate contract is found to have retried a confirm attempt inside the same envelope
after an `EVIDENCE-VOID` result (rather than opening a fresh campaign with a fresh holdout), or (b) a
campaign envelope's recorded ceiling is found to exclude a probe tranche's realized spend that §2
requires it include — this ADR is revoked.

**Revert action:** author a superseding ADR that either tightens the reconciliation rule into a
mechanical check (a contract-integrity check refusing a campaign envelope whose declared ceiling is
less than its cited probe-tranche spend plus new spend) or revisits the fresh-holdout requirement if
it proves to block legitimate work more often than it prevents inflation. Never silently edit this
ADR's decision text.

**Trigger check schedule:** every quarterly programme audit (next: 2026-11-08).

---

## §5 — Forbidden moves (under this ADR)

- **Treating a `VOID-*` result as grounds for a fresh operator ask to retry inside the same
  envelope.** Ruled out in §2/§3 — the only legal path is a fresh campaign with a fresh holdout.
- **Silently topping the campaign envelope's ceiling back up to exclude an already-cited probe
  tranche's realized spend**, to make the campaign's own budget look larger than what was actually
  approved end to end. Ruled out in §2/§3 — the ceiling is set inclusive of the citation.
- **Revising `α`, `M`, or the named procedure mid-campaign** because an intermediate result suggests
  a different configuration would be more favorable. Ruled out in §2 — all three freeze at contract
  freeze; a mid-campaign revision is exactly the "silent multiplicity inflation" the note's row
  exists to prevent.
- **Requiring a fresh operator GO for routine in-envelope work** (a schema clarification, a window
  question). Ruled out in §2/§3 — defeats the entire purpose of approving one envelope up front.
- **Reading Rule 2's iteration-budget tripwire as satisfying or replacing this ADR's spend-envelope
  approval**, or vice versa. Ruled out in §2 — the two axes are independent and both must clear.

---

## §6 — Consequences

**Positive consequences:**
- Closes the specific multiplicity-inflation pathway the note's row diagnosed: a `VOID-*` result can
  no longer be informally re-asked into another look at the same holdout.
- Gives the pre-freeze shape-extraction probe (`2026-08-30-tradeable-reachable-gate.md`) a ruled
  reconciliation path instead of an unspecified "subsumed by citation" assertion.
- Reduces routine approval friction for in-envelope work, addressing the note's own diagnosis that
  scattered permission points make the operator a throughput scheduler rather than a risk owner.
- Discharges `2026-08-30-candidate-contract.md` §3's and `2026-08-30-evaluation-order.md`'s forward
  citations to this exact filename.

**Negative consequences (real cost, not theatrical):**
- A campaign that genuinely needs to exceed its declared envelope (a legitimate scope change, not
  inflation) now requires an explicit fresh GO rather than an informal adjustment — real friction,
  the cost side of closing the inflation leak.
- An `EVIDENCE-VOID` result now permanently forfeits that holdout's confirm attempt rather than
  allowing any retry — a candidate that voided on an infrastructure hiccup, not a genuine holdout
  problem, still pays the full fresh-campaign cost.

**Risks (probabilistic, distinct from costs):**
- The probe-tranche reconciliation rule (§2) depends on accurate citation at freeze time; if a
  future channel's tooling fails to carry the probe's realized spend forward correctly, the ceiling
  could under-report despite this ADR's rule — a build-time risk for the separate implementation
  handoff (§7), not a defect in the rule itself.

**Downstream artifacts that need updating:**
- `2026-08-30-candidate-contract.md` — Amends-in-part (this ADR's header): the multiplicity-
  configuration field (`α`/`M`/procedure) added to the founding-freeze field list, discharging that
  ADR's own §3 deferral.
- `2026-08-30-evaluation-order.md` §2 step 7 — its forward citation to this ADR's filename is now
  discharged; no edit needed to that ADR's text (Trap #12 — decisions stay byte-stable once landed,
  and that ADR is not yet `Accepted` in any case).
- `STATE.md` — new forward-board row: campaign-envelope + multiplicity-configuration mechanical
  enforcement owed as a separate handoff (§7).

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time.
- **Phase 1** — this ADR's own body is the complete policy deliverable; the `Amends-in-part` edge to
  `2026-08-30-candidate-contract.md` lands on ratification, not before.
- **Phase 2** — grep-sweep (Known Trap #7): **(i)** no predecessor to check (`Supersedes: none`);
  **(ii)** `grep -rl "campaign envelope\|multiplicity configuration\|Bonferroni\|Holm step-down"
  docs/adr/ docs/spec/ docs/methodology/` — executed at authoring time: 10 hits, each disposed:
  - `candidate-contract.md`, `tradeable-reachable-gate.md`, `evaluation-order.md` — this session's
    own prior work, already folded into §0/§1.
  - `docs/methodology/avenue_a_generate_confirm.md` — the real precedent this ADR generalizes,
    folded into §0 (not a competing definition; that route is retired).
  - `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` and
    `docs/adr/2026-07-10-databento-research-stack.md` — `register_search.py`'s own K-accounting
    Bonferroni/BH-FDR triage, a **different, earlier-stage** correction (catalogue selection-under-K,
    not confirm-family FWER); disposed in §2 as sequential-and-cumulative, not competing.
  - `docs/adr/2026-05-22-reality-check-harness.md` — a separate, narrower, already-locked pattern-
    mining harness's own MTC method choice (Bonferroni vs. Romano-Wolf vs. DSR for K-pattern
    enumeration scans); a different gate at a different layer, no conflict, no edit needed.
  - `docs/methodology/references/statistics-of-tradable-anomalies.md` — general background
    reference material explaining FWER methods generically; not a decision artifact, no conflict.
  - `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md` — a passing aside citing "frozen
    DSR/Bonferroni" as context for an unrelated proposal; no competing claim.
  No document claims ownership of the confirm-family `α`/`M`/procedure field this ADR freezes; the
  one genuine precedent (Route B's retired checklist line) is generalized, not duplicated.
- **Phase 3** — verification block executes; status → `Accepted`.

Mechanical enforcement (the contract-integrity check refusing a mismatched procedure declaration,
the probe-tranche citation bookkeeping) is a **separate implementation handoff** — doctrine binds
now; code may lag, per the HARV-lane precedent (`2026-08-30-candidate-contract.md` §0).

---

## §10 — Audit hooks (runnable)

```bash
# Multiplicity-configuration field discharges candidate-contract.md's own deferral.
grep -n "operator-approvals-campaign-envelope" docs/adr/2026-08-30-candidate-contract.md

# evaluation-order.md's forward citation resolves to this exact filename.
grep -n "operator-approvals-campaign-envelope" docs/adr/2026-08-30-evaluation-order.md

# No other document has quietly started defining a competing multiplicity-configuration owner.
grep -rn "multiplicity configuration" docs/ 2>/dev/null | grep -iv "operator-approvals-campaign-envelope.md\|candidate-contract.md\|evaluation-order.md\|generate-evaluate-tensions.md"

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-30-operator-approvals-campaign-envelope.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/adr/2026-06-16-rule-2-budget-before-acting.md
$ git log -1 --format="%h %ci" -- docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md

# Downstream artifact update verification (post Amends-in-part landing)
$ grep -n "operator-approvals-campaign-envelope" docs/adr/2026-08-30-candidate-contract.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring | Joshua + Claude Code |
