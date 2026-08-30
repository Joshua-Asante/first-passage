# TRADEABLE-REACHABLE — one pre-explore economic orchestrator delegating to existing cost/latency/geometry/shape authorities, never forking a new one — `tradeable-reachable-gate`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-30; see Ratification note.
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Amends-in-part:** `2026-08-30-candidate-contract.md` — adds payoff-shape-prior fields, the CONFIRM-window early-reservation commit, and the pinned cost-authority identifier to the contract schema this ADR's founding freeze already requires; edits land on ratification, not before.
**Layer:** methodology (pre-explore economic gate orchestration only). No `dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue action; no spend beyond the bounded, operator-approved probe envelope this ADR itself requires.
**Tier:** full — Limb 4 fires (creates standing doctrine binding every candidate contract's pre-explore gate).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, this session (2026-08-30):

- `docs/notes/2026-08-30-generate-evaluate-tensions.md` — anchor `419433a` (2026-08-30). Table row "Merge early economic gates": `TRADEABLE-REACHABLE` delegates each limb to its existing authority, pinned at freeze; cost delegates to whichever authority EM1 points at; `cost_geometry_pregate.py` stays additive; payoff-shape sources contract-frozen priors or a pre-freeze extraction probe under its own approved envelope; the CONFIRM window is reserved before the probe reads data; the all-clause reachability attestation (HARV-lane) is strengthened to same-units-per-gate and now enumerates latency/firm-geometry alongside cost-law/confirm/placebo/shape; a pre-explore `TRADEABLE-REACHABLE` failure appends a typed, taxonomy-routed verdict to the contract.
- `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` — anchor `340722c` (2026-08-24). §3a: "EM1 defines no cost formula. It consumes whichever authority the estate names, and it must not become a third one... EM1 points at Requirement 5 because this screen composes with harvest Req 1–5 — but if 08-08 rules the other way, or keeps both with a stated scope split, EM1 re-points in the same change and does not fork." §7: "the envelope E1-E7 and third-leg S1-S7 are ratified, non-overlapping, and composed with — not superseded. Any proposal to fold them into this spec is a different decision needing its own ADR" — this ADR does not fold E1-E7/S1-S7 into anything; it orchestrates cost/latency/geometry/shape as an external delegator, leaving every owning spec untouched.
- `docs/methodology/strategy_harvest.md` — anchor `936eb0f` (2026-08-29). Requirement 5 (cost reachability, self-declared "the sole authority" for cost-sensitive rejections since 2026-07-21) and Requirement 2's δ-extraction-probe relief valve ("no citable δ ⇒ UNSCREENABLE → route to a δ-extraction probe or drop; never invent a number") — the exact pattern this ADR's payoff-shape probe reuses.
- `scripts/cost_geometry_pregate.py` + `docs/adr/2026-06-22-cost-geometry-pregate.md` — anchor `e11fd39` / `e11fd39`. §2: the Phase-0 realized-stop-geometry pre-gate (`cost_R = RT / (stop_atr · median ATR15m)`, PASS < 0.05R) is explicitly additive — "extends Rule 10" — and computes a *different quantity* (realized-stop geometry ratio) than Requirement 5 (cohort-δ-vs-4×-RT-hurdle). The two are compatible necessary conditions, not competing authorities; the fracture named in `eval-mechanism-shape-screen.md` §3a is about which one EM1 defers to for its own limb, not a logical contradiction between them.
- `docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md` — anchor `e11fd39`. N-EDGE (net expectancy, CI, DSR) and N-SIZE (the candidate's own edge-indexed frontier, EM2 principle) are **measured** limbs — they cannot be simulated for reachability from priors alone; they are scored only once their declared data source exists, never claimed complete pre-data.
- `docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md` D2 (`Accepted` 2026-08-24). "Cost-law: two owners, correctly separated, not one" — Requirement 5 stays sole canonical owner of the per-event bp-of-panel-price form (admission/harvest time, unedited); `cost_geometry_pregate.py` becomes canonical owner of the per-trade stop-distance-R form (pre-build design-time check). This **is** the "stated scope split" outcome `eval-mechanism-shape-screen.md` §3a's own text names as one of G3's two possible resolutions ("EM1 re-points in the same change and does not fork") — **G3 is resolved**, six days before this ADR's authoring, even though §3a's own prose (RATIFIED 2026-08-06, unedited since) still reads "open fracture, deliberately not resolved here." Found via this ADR's own Phase-2 sweep (§7/§10), not by predecessor citation — the validation-battery ADR does not itself cite the G3 board item or this spec. Documentation lag between two independently-correct sources, not a live contradiction; corrected throughout this ADR's text below, and flagged as a downstream artifact (§6).
- `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — anchor `151cb18` (2026-08-29). §2: the all-clause reachability attestation HARD gate is scoped to "campaigns that claim a named economic mechanism (the HARV / Q-MECH-1 shape)" — mechanism-first candidates only, not every candidate contract.
- `docs/adr/2026-07-16-harv-attestation-same-units-supersession.md` — anchor `e11fd39` (2026-08-24). §2: strengthens the attestation to "simulate every gate the campaign can die at... in that gate's own units," with the mandatory cost-law inequality (`cohort δ ≥ 4 × RT_frac` at the adjudication-panel basis, commissions included) — the D5/H-OD-1 failure class this ADR's own attestation enumeration must not reproduce for latency/geometry/shape.
- `docs/adr/2026-08-05-strategy-venue-binding-axis.md` — anchor `e2d21b9` (2026-08-24). Confirms venue-edition state is a distinct axis from candidate-lifecycle evidence — relevant to how this ADR's pre-explore failures must be classified (§2) without conflating a contract-level kill with a later venue-placement kill (that distinction is `2026-08-30-terminal-taxonomy.md`'s decision, not this one).
- `docs/adr/2026-06-14-rejected-candidate-patterns.md` — anchor `0395f56` (2026-08-29). §A's venue/cost-constraint class and its add-back condition; this ADR's pre-explore failures route into that class, but the routing rule itself belongs to the terminal-taxonomy ADR, cited not re-decided here.
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` — anchor `e11fd39`. §2 item 5: "Cost-law reachability (Req 5's ≥4× round-trip inequality), with the candidate's own confirm-partition measured effect substituted for cohort δ — the schema already permits this (`delta_citation: null`)." Found via this ADR's own Phase-2 sweep (§7), not in the first draft: for this channel specifically, Requirement 5's cost input is, by the channel's own already-ratified design, the confirm partition's own measured result — structurally unavailable before Confirm, not merely uncalculated. A universal pre-Explore cost limb cannot be applied to this channel without either inventing a prior this channel's design deliberately declines to require, or reading confirm data early. Ruled on in §2 below as a named, cited exception — not a gap.

**Amendment-first / dedup (Rule 8 sub-rule 10), run at ratification:**

```
$ python scripts/check_advisor_dedup.py --keywords "TRADEABLE-REACHABLE pre-explore economic gate orchestrator cost latency geometry payoff shape delegating"
```

218 candidates surfaced, all keyword-overlap noise from instrument ledgers/mechanism vocabularies and unrelated audit notes — none proposes a single delegating pre-Explore economic orchestrator. No existing ADR or brief performs this ADR's decision.

---

## §1 — Context

Cost reachability, payoff-shape screening, latency, and firm-geometry
checks run today as separate stops, several with no formal reachability
guarantee before a candidate contract freezes. Cost specifically is split
across two artifacts (Requirement 5, `cost_geometry_pregate.py`) whose
relationship was an open, named fracture (`eval-mechanism-shape-screen.md`
§3a, "G3") — **resolved 2026-08-24** as two correctly-separated owners of
two distinct quantities (`2026-08-24-validation-battery-k-tiering-and-
gate-retirement.md` D2; §0), though the spec's own prose has not been
updated to say so. Meanwhile no requirement exists today for a candidate to
carry citable payoff-shape priors before its contract freezes: a HARV-lane
candidate could, absent this ADR, freeze with an unscored shape limb and
only discover the kill after the fact — the same shape of defect the
2026-07-16 supersession ADR diagnosed for the cost-law gate (D5/H-OD-1,
frozen on an unreachable Stage-2 gate the attestation never simulated).

**Decision driver (one sentence):** the estate has one economic pre-gate
concept scattered across separately-run checks — cost's own two-formula
split is now correctly resolved, but its spec-level record still reads
stale — and no requirement that a candidate's payoff shape be scoreable
before its contract freezes.

---

## §2 — Decision

**Decision:** Every candidate contract (`2026-08-30-candidate-contract.md`)
runs one **`TRADEABLE-REACHABLE`** pre-gate before Explore, covering
cost, latency, firm-geometry, and payoff-shape. `TRADEABLE-REACHABLE` is a
pure **orchestrator**: it delegates every limb to its existing named
authority and derives no arithmetic of its own.

- **Cost** delegates to `strategy_harvest.md` Requirement 5 — the
  per-event bp-of-panel-price form, sole canonical owner for
  admission/harvest-time cost per the eval-mechanism-shape screen's EM1
  pointer, now also confirmed by the resolved G3 split (§0).
  `cost_geometry_pregate.py`'s per-trade stop-distance-R form stays a
  separate, additive Phase-0 design-time check under its own canonical
  ownership — a different quantity, not a competing one, and (per the
  2026-08-24 resolution) not provisional either: both owners are now
  independently settled. The contract records which authority + revision
  was pinned at freeze; should a future superseding decision revise either
  owner's scope, an already-frozen campaign is **voided and refrozen**
  under the new authority rather than silently re-scored under a formula
  its attestation never simulated. `TRADEABLE-REACHABLE` must never fork a
  third cost formula.
  **Named exception — the no-counterparty-statistical/geometric channel
  (§0).** That channel's own already-ratified design substitutes the
  candidate's own confirm-partition measured effect for cohort δ, making
  Requirement 5's cost input structurally unavailable before Confirm for
  that channel — not a gap this ADR can close without either inventing a
  prior the channel's own design deliberately declines to require, or
  reading confirm data early (breaking the holdout this whole series
  protects). For candidates on this channel only, `TRADEABLE-REACHABLE`'s
  cost limb is satisfied by citing the channel's own already-ratified
  deferred order rather than blocked or forced to invent a number; that
  channel's existing post-confirm cost-law check (unedited by this ADR)
  remains the operative cost-reachability discipline for that limb. Every
  other channel's cost limb runs pre-Explore as described above; this
  exception does not generalize without its own citing exception, named at
  declaration for any future channel that shares the same structural
  shape.
- **Latency and firm-geometry** delegate to their existing owning checks
  (whichever the candidate's channel/venue binding names); this ADR adds
  no new latency or geometry arithmetic.
- **Payoff-shape** sources prior win-rate/mean-win/mean-loss estimates the
  contract's founding freeze must carry, under the same discipline harvest
  Requirement 2 applies to δ/σ — conservative central reading,
  publication-decay haircut, never an invented number. This requirement
  binds **every** candidate contract facing `TRADEABLE-REACHABLE`,
  regardless of lane, even though the all-clause attestation below stays
  HARV-scoped. A candidate with no citable shape priors is UNSCREENABLE on
  that limb and routes to a **pre-freeze shape-extraction probe** — the
  same funded route as Requirement 2's δ-extraction probe: declared on
  the draft contract (instrument, window, exactly which statistics), run
  only under its **own operator-approved probe envelope** (spend ceiling,
  schema, window, K ceiling frozen at declaration, approved *before* any
  data access — the campaign envelope itself is not recorded until the
  contract's own freeze, so an unapproved pre-freeze pull would be
  unbudgeted spend), and licensed only **outside** the candidate's
  CONFIRM window. The CONFIRM window is reserved by an append-only
  commitment on the draft contract *before* the probe reads any data — not
  at the contract's later freeze — because reserving it only afterward
  would let a probe run before the window existed and influence which
  interval gets designated the holdout. No contract freezes with the
  shape limb unscored.
- **All-clause reachability attestation.** For mechanism-first (HARV-lane)
  candidates, per `2026-07-13-harv-discovery-lane-ratification.md` §2 as
  strengthened by `2026-07-16-harv-attestation-same-units-supersession.md`
  §2: simulate every gate the draft contract can die at — Stage-2
  cost-law, Stage-6 confirm, placebo, the payoff-shape limb (now carrying
  real priors), the latency and firm-geometry limbs `TRADEABLE-REACHABLE`
  will score, and any bundled temporal battery — each in that gate's own
  units, before the contract freezes. The enumeration is closed over
  `TRADEABLE-REACHABLE`'s own limb set by construction: any limb the gate
  can kill on is a gate this attestation must have simulated first. A
  candidate outside the HARV/mechanism-first lane is not bound by this
  HARD gate absent a separate ratifying decision.
- **Measured limbs stay deferred, not claimed.** N-EDGE and N-SIZE/the
  EM2 frontier (`2026-08-08-tradeify-necessary-conditions-target-spec.md`)
  cannot score before their declared data source exists; `TRADEABLE-
  REACHABLE` never claims them reachable pre-data, and the attestation
  above does not enumerate them as pre-freeze-simulable.
- **Auditable pre-explore failure.** Because the contract has already
  frozen by the time `TRADEABLE-REACHABLE` runs, every limb is scorable by
  construction — except the named cost-limb exception above, which is
  satisfied by citation rather than scored, for the one channel whose own
  design makes a pre-Explore cost score structurally unavailable. A
  failure on any limb stops before Explore and appends a
  typed verdict (which limb, at what value) to the already-frozen
  contract — never silent, never leaving a candidate with no recorded
  disposition. Which terminal class that typed verdict routes into is
  `2026-08-30-terminal-taxonomy.md`'s decision, cited here, not re-decided.

**Effective:** immediately upon acceptance, for any candidate contract
frozen after this date.
**Scope:** every candidate contract's pre-explore economic gate, across
all five live channels (§0; GROW is tooling inside deep-iteration, not a
sixth channel — matching `2026-08-30-channel-liveness-gate.md`'s own
derivation), with the one deferred-cost-limb exception the no-counterparty-
statistical/geometric channel's own already-ratified design requires
(above). Does not alter Requirement 5, `cost_geometry_
pregate.py`, EM0–EM5, E1–E7, or S1–S7's own thresholds or ownership — it
orchestrates them, per §7's spec.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Re-adjudicate the Requirement-5-vs-`cost_geometry_pregate.py` split inside this ADR | Already resolved by a separate, already-Accepted ADR (`2026-08-24-validation-battery-k-tiering-and-gate-retirement.md` D2 — two owners, correctly separated), discovered via this ADR's own Phase-2 sweep (§0/§7). Re-deciding a closed question here would duplicate that ADR's authority; this ADR instead delegates to the settled owner for each quantity and cites the resolution. |
| Let `TRADEABLE-REACHABLE` compute its own cost/latency/geometry arithmetic, folding E1–E7/S1–S7/Requirement 5 into one formula | Directly forbidden by `eval-mechanism-shape-screen.md` §7 ("any proposal to fold them into this spec is a different decision needing its own ADR") and §3a ("must not become a third [authority]"). A pure delegator avoids becoming that third authority. |
| Require payoff-shape priors only for HARV-lane candidates, matching the all-clause attestation's scope | The gate that *consumes* the priors (`TRADEABLE-REACHABLE`) is universal by design — every candidate contract faces it before Explore, regardless of lane. Scoping the input requirement narrower than the gate that needs it would leave non-HARV contracts freezing with an unscored shape limb, reproducing this ADR's own target defect for those lanes. |
| Defer the CONFIRM-window reservation to the contract's later freeze (§2 of `candidate-contract.md`), rather than reserving it before the probe runs | A probe run before the window exists could influence which interval later gets designated the holdout — the reservation must happen first, or "the probe never touches the reserved window" is aspirational rather than enforced. |
| Silently re-score an already-frozen contract if EM1's cost authority re-points mid-campaign | The contract's reachability attestation and frozen cost fields were computed against the *prior* authority; re-scoring under a new one without a fresh attestation would evaluate the candidate against a formula it was never checked against. Void-and-refreeze preserves the attestation's meaning. |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** a single delegating `TRADEABLE-REACHABLE` orchestrator,
fed by contract-frozen payoff-shape priors (or a bounded extraction probe)
and a pre-freeze all-clause attestation, catches an unreachable economic
gate before it wastes a confirm holdout, without becoming a competing cost
authority itself.

**Revert trigger:** if, by the next scheduled quarterly programme audit
after this ADR's acceptance, either (a) `TRADEABLE-REACHABLE`'s
implementation is found to have derived its own cost, latency, or geometry
arithmetic rather than delegating (reproducing exactly the "third
authority" failure §0/§3 rule out), or (b) a candidate contract is found to
have frozen with an unscored payoff-shape limb (neither citable priors nor
a completed extraction probe on record) — this ADR is revoked.

**Revert action:** author a superseding ADR that either re-specifies the
delegation boundary more strictly (e.g. a mechanical lint checking no new
arithmetic constant appears in the orchestrator's own code) or tightens
the shape-limb freeze precondition. Never silently edit this ADR's decision
text.

**Trigger check schedule:** every quarterly programme audit (next:
2026-11-08); also immediately if a future superseding decision revises
either cost-law owner named in §2 (the 2026-08-24 split itself, or
Requirement 5's / `cost_geometry_pregate.py`'s own ownership).

---

## §5 — Forbidden moves (under this ADR)

- **Letting `TRADEABLE-REACHABLE` grow its own cost, latency, or geometry
  formula "for convenience," rather than delegating.** Directly forbidden
  by `eval-mechanism-shape-screen.md` §3a's own naming of this exact
  temptation ("does not become the third entry in an already-fractured
  stack"). If a limb's existing authority is inconvenient to call, that is
  a reason to fix the calling convention, never to re-derive the limb.
- **Silently extending the no-counterparty-statistical/geometric channel's
  deferred-cost-limb exception (§2) to any other channel**, or inventing a
  pre-Explore cost prior for that channel to avoid naming the exception.
  Ruled out in §2 — the exception is cited, narrow, and channel-specific;
  a future channel sharing the same structural shape (cost input
  substituted from the confirm partition itself) needs its own named,
  cited exception at declaration, never an inferred extension of this
  one.
- **Re-adjudicating the Requirement-5/`cost_geometry_pregate.py` split
  inside this ADR**, or silently treating it as still-open. Ruled out in
  §3 — it is already resolved by a separate Accepted ADR (2026-08-24);
  this ADR cites that resolution rather than re-deciding or re-opening
  it.
- **Scoping the payoff-shape-prior requirement to HARV-lane only**, to
  match the all-clause attestation's own scope. Ruled out in §2/§3 — the
  gate that consumes the priors is universal; narrowing the requirement
  below the gate's own scope reproduces the target defect.
- **Silently re-scoring an already-frozen contract when the cost authority
  re-points**, rather than void-and-refreeze. Ruled out in §2/§3 — the
  attestation's meaning depends on having simulated the *actual* authority
  the gate later scores under.
- **Inventing a default shape-extraction-probe budget inside this ADR** to
  make the mechanism look complete. Each probe declares and gets its own
  operator-approved envelope at declaration time (§2); no blanket default
  is set here.

---

## §6 — Consequences

**Positive consequences:**
- Collapses several separately-run economic checks — one of which (cost)
  was fractured until a separate, already-Accepted ADR settled it
  2026-08-24 — into one delegating orchestrator, without re-adjudicating
  that settled question.
- Gives payoff-shape priors a real, funded acquisition path
  (extraction probe) instead of leaving the limb permanently unscored for
  candidates with no citable prior literature.
- Closes the exact D5/H-OD-1 failure class (an unreachable pre-freeze gate
  the attestation never simulated) for latency, geometry, and shape, not
  only cost-law.
- Every pre-explore kill is now auditable — appended to the contract —
  rather than silently discarding a candidate with no recorded reason.

**Negative consequences (real cost, not theatrical):**
- A candidate with no citable shape priors now requires an extra,
  operator-approved probe step before its contract can freeze — real
  authoring and approval overhead versus today's silent-unscored-limb
  status quo.
- The void-and-refreeze rule (§2) means a G3 re-point mid-campaign costs a
  candidate its attestation work to date, rather than a cheap silent
  re-score.

**Risks (probabilistic, distinct from costs):**
- The cost-law split's spec-level record (`eval-mechanism-shape-screen.md`
  §3a) still reads "open," six days stale relative to its own actual
  2026-08-24 resolution; a future author reading only the spec (not the
  resolving ADR) could reintroduce the re-pointing language this ADR now
  retires. Mitigated by flagging the stale spec text as a downstream
  artifact below — not itself a new risk this ADR introduces.

**Downstream artifacts:**
- `2026-08-30-candidate-contract.md` — **landed at ratification** (this
  commit): payoff-shape-prior fields, CONFIRM-window reservation, pinned
  cost-authority identifier added to the founding-freeze field list.
- `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` §3a — owed a
  pointer-note correction now (found by this ADR's Phase-2 sweep, §7/§10):
  its prose still reads "open fracture, deliberately not resolved here,"
  but `2026-08-24-validation-battery-k-tiering-and-gate-retirement.md` D2
  already resolved G3 via the exact "stated scope split" outcome the
  spec's own text names. Correcting §3a's prose is not this ADR's own edit
  authority (a RATIFIED spec, out of scope here) — flagged for a separate,
  minimal doc-only correction.
- `STATE.md` — new forward-board row: `TRADEABLE-REACHABLE` orchestrator
  implementation owed as a separate handoff (§7); G3 resolution remains
  its own pre-existing board item, unblocked but not resolved by this ADR.

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time; in
  particular re-check whether the cost-law split (§0, G3) has been
  revised again since this ADR's own authoring — it was already found
  resolved (2026-08-24, six days before this ADR's authoring) during
  drafting, not at apply-time; this phase only guards against a further
  change after that.
- **Phase 1** — this ADR's own body is the complete policy deliverable;
  the `Amends-in-part` edge to `2026-08-30-candidate-contract.md` **landed
  at ratification** (this commit), as a new §2 subsection on that ADR.
- **Phase 2** — grep-sweep (Known Trap #7), executed at authoring time:
  **(i)** no predecessor to check (`Supersedes: none`); **(ii)** `grep -rl
  "cost_geometry_pregate\|Requirement 5\|payoff.shape" docs/adr/ docs/spec/
  docs/methodology/` returned 12 files. Beyond the 8 already cited in §0,
  4 new hits, each disposed:
  - `docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md`
    — the G3-resolving ADR itself; folded into §0/§1/§2 above (this ADR's
    single most load-bearing sweep finding).
  - `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md`
    L109 — consumes Requirement 5's arithmetic for a specific candidate
    grading call; no competing ownership claim.
  - `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md` — uses
    "payoff-shape" informally (a payoff-shape *problem*, not this ADR's
    shape-limb definition); no conflict.
  - `docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md`
    L189 — "Cost authority: EM1's — Requirement 5" — consumes the same
    settled pointer this ADR uses; consistent, no conflict.
  - `docs/methodology/lessons/methodology_lessons.md` M-20 — already
    rewritten as a labeled derived mirror of Requirement 5 (D2's own
    directive, confirmed executed by direct read); `docs/methodology/
    LESSONS_INDEX.jsonl`'s M-20 entry is an index pointer only, no formula
    content. Neither conflicts.
  No document claims to be "the" combined economic gate; the only
  substantive finding beyond the G3 resolution is the already-folded G3
  finding above.

  **Post-review correction (found by a Codex review pass on this PR, not
  by the sweep above):** the sweep's pattern used "Requirement 5" literally
  and missed `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-
  channel.md`, whose own §2 item 5 abbreviates it "Req 5's" — a real
  near-miss from abbreviation variance, not a sweep-execution failure. That
  file's own text substitutes the candidate's confirm-partition measured
  effect for cohort δ, making the cost limb structurally post-confirm for
  that one channel — a genuine gap in this ADR's original universal
  pre-Explore cost requirement, not just a missed citation. Fixed by the
  named, cited exception added to §0/§2/§5 above, rather than by silently
  forcing that channel to invent a pre-Explore prior its own design
  deliberately declines to require.
- **Phase 3** — verification block executes; status → `Accepted`.

Mechanical `TRADEABLE-REACHABLE` orchestrator code (the actual delegating
call sequence) is a **separate implementation handoff** — doctrine binds
now; code may lag, per the HARV-lane precedent
(`2026-08-30-candidate-contract.md` §0).

---

## §10 — Audit hooks (runnable)

```bash
# Cost-law split still resolved as of 2026-08-24 D2? (re-check before
# assuming Requirement 5 / cost_geometry_pregate.py ownership is unchanged)
grep -n "two owners, correctly separated" docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md

# Has the stale eval-mechanism-shape-screen.md §3a prose been corrected
# to point at the 2026-08-24 resolution yet? (tracked downstream item, §6)
grep -n "open fracture, deliberately not resolved here" docs/spec/2026-08-05-eval-mechanism-shape-screen.md

# Has any document started claiming its own cost/latency/geometry formula
# inside a TRADEABLE-REACHABLE-labeled check? (should be zero -- pure delegation)
grep -rn "TRADEABLE-REACHABLE" docs/ scripts/ lab/ 2>/dev/null | grep -iv "candidate-contract.md\|tradeable-reachable-gate.md\|generate-evaluate-tensions.md"

# Candidate-contract amendment landed?
grep -n "tradeable-reachable-gate" docs/adr/2026-08-30-candidate-contract.md

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-30-tradeable-reachable-gate.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/spec/2026-08-05-eval-mechanism-shape-screen.md
$ git log -1 --format="%h %ci" -- docs/adr/2026-06-22-cost-geometry-pregate.md

# Downstream artifact update verification (post Amends-in-part landing)
$ grep -n "tradeable-reachable-gate" docs/adr/2026-08-30-candidate-contract.md
```

---

## Ratification note

**Ratified by:** Joshua, direct instruction ("ratify the six ADRs," 2026-08-30), following a
self-conducted adversarial re-read (the full 6-lens Workflow panel was declined for cost) that added
the missing amendment-first/dedup attestation (§0).

**§6-class preconditions at ratification:** mechanical checks clean (`check_brief.py` 0 HARD,
`check_adr_graph.py` OK) ✓ · amendment-first dedup run, no genuine prior art ✓ · the Codex review
round's finding on this file (the no-counterparty-statistical channel's structural cost-limb
conflict) verified already fixed via the named exception (§2) ✓ · the `Amends-in-part` edge to
`candidate-contract.md` confirmed landed (§10 hook) ✓.

**Not licensed by this ratification:** building the `TRADEABLE-REACHABLE` orchestrator's actual
delegating code (§7, separate implementation handoff) · resolving the pre-freeze shape-extraction
probe's tooling · any edit to `core/`, `ops/`, `dd_protection`, or allocations.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring | Joshua + Claude Code |
| 2026-08-30 | Ratified — status → `Accepted`; `Amends-in-part` edge to candidate-contract.md landed | Joshua (operator ratification) |
