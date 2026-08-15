# Rejected methodology signals

Standing registry of **methodology / programme-audit signal** candidates investigated
and rejected. This is the methodology-layer parallel to
[`docs/rejected_candidates.md`](../rejected_candidates.md) (which holds *portfolio /
strategy / instrument / parameter* rejections). One entry per signal.

A rejected signal is a proposed degeneration-signal, diagnostic, or audit heuristic
that was tested against history and did **not** earn its place. Re-proposal of any
entry requires a **dated incident** the existing machinery would have missed — not a
restatement of the plausibility argument.

**Intake bar (same as acceptance):** a signal earns a place only if it would have
fired on a dated, evidence-anchored incident that the existing signals/diagnostics
miss by construction. Plausibility is not sufficient — adding signals on plausibility
alone is itself programme-audit degeneration signal #2 (belt that only grows, never
prunes).

New entries link to the closure/disposition artifact authoritative for the rejection.

---

## Entries

### REJECTED — Starvation signal (within-stream resource starvation) — 2026-06-04

**Proposed:** a programme-audit degeneration signal for an individually-progressive
*strategy* being under-resourced because another strategy dominates capital/attention
flow *within the operational value stream*.

**Disposition source:** the 1-of-3 coordination-class signal test, 2026-06-04 (three
coordination-aggregate candidates run against history; one survived). Candidate 3
(cross-stream drain) was accepted as coordination-signal **#8** / diagnostic **C1** in
the programme-audit protocol. Candidate 2 (collision) was cross-referenced, not
duplicated. Candidate 1 (this entry) was rejected.

**Reason rejected (earns-its-place test failed):**

1. **No on-disk-confirmed dated incident.** No record exists of a *built,
   MC-validated* track being starved by within-stream flow domination. The incident
   originally proposed as the nearest candidate — a missed Aegis signal dated
   "2026-03-16, +$3,467" — **does not verify against the live-execution-journal
   record** (the on-disk execution-lessons registry anchors its nearest comparable
   incident at the 2026-04-07 Guardian macro-skip, +$3,752, which is a *behavioral*
   skip under E1, not flow-starvation; no Mar-16 Aegis +$3,467 incident is on disk).
   The absence of a verifiable dated incident is itself the disqualifier.

2. **The causal mechanism is structurally absent (load-bearing).** The mechanism that
   would produce within-stream starvation — *discretionary* capital allocation — does
   not exist in this operation. Allocation is set by MC pass-rate optimization, which
   hands capital in proportion to contribution. The mechanism that would cause the
   failure is replaced by the mechanism that prevents it. Even a verified incident
   would have to defeat this structural argument first.

**Re-proposal bar:** a **dated incident** of a built, MC-validated strategy starved by
another strategy's within-stream flow domination — *and* an account of how it occurred
despite MC-pass-rate allocation. A restatement of the plausibility argument, a new
incident that is actually build-sequencing (system not yet deployed) rather than
flow-starvation, or a cross-stream (operational ↔ development) example do **not** clear
the bar.

**Do not conflate with the accepted signal.** Cross-stream drain (operational ↔
development) is a *different* signal, accepted 2026-06-04 as coordination-signal #8.
Within-stream starvation (one strategy vs another, same stream) is what is rejected
here.

---

### REJECTED — Status-grammar state-machine gate (status vocabulary closure + transition legality) — 2026-07-29

**Proposed:** a governance-tier gate typing the repo's status vocabulary into a state
machine — *entity class → legal states → legal transitions → precondition pointer* —
extending [`scripts/check_status_consistency.py`](../../scripts/check_status_consistency.py)
so that an invented/typo'd status word and an illegal status transition are caught
mechanically rather than by curation. Provenance: an external methodology source
(F. Coyle, *Why Agentic Systems Need Ontologies*, AI Engineer 2026) supplied the
constraint class — an *enumerated range*, his "order status of `probably shipped`"
error. The proposal was that the repo's strong-but-prose status grammar should be
machine-enforced the way its import contract and manifests already are.

**Disposition source:** measurement run 2026-07-29 (this session) against the live
surfaces, before any spec was authored. Commands and outputs in reasons 1–2 below.

**Reason rejected (earns-its-place test failed):**

1. **Both status surfaces are already gated, and both are green.**
   `python scripts/check_adr_graph.py` → `OK (enabled=['A1','A2','A3','A4','A6'])`; its
   docstring states it "Enforces header Status vocabulary" for ADRs.
   `python scripts/check_status_consistency.py` → `OK — no status contradictions
   (0 advisory note(s))`. There is no ungoverned status surface for the gate to occupy.

2. **The vocabulary-closure limb has zero manifest findings.** A census of every
   `lab/CATALOG.md` row via the gate's own parser: **106/106 rows** carry one of the five
   declared words (`ACTIVE` 46, `FALSIFIED` 21, `HOLD` 20, `CLOSED` 16, `RETIRED` 3);
   **0 rows** escape the class-check. The silent-escape path is real in code but exists
   *by deliberate design* — the gate class-checks only known words "so an unrecognised
   status word never false-positives" — and it has never fired. Closing it would add a
   gate against a hazard with no instance.

3. **The transition/cross-surface limb is a re-derivation of two already-rejected
   designs.** `check_status_consistency.py`'s docstring records both: **C1** (status-
   contradiction join across surfaces) was DROPPED after its first real run because
   rejection contexts legitimately link the *parent/apparatus* study, so the slug-join
   yielded only false positives; **C4** (intra-`STATE.md`) was DROPPED 2026-07-25 after
   two designs were built and measured against the actual pre-incident file — there is
   no shared anchor to join on (the pointer-log bullet recording the discharge cites 32
   repo paths, **none** of them the ADR whose falsifier it discharged). The recorded
   verdict is that separating signal from noise "needs semantic knowledge of which ADR a
   given status belongs to, which is the C1 mistake in new clothing," and that the
   reachable fix for the class is **a writing convention enforced at authoring time, not
   a gate**.

4. **No dated incident clears the intake bar.** The only candidate — the 2026-07-24
   `STATE.md` self-contradiction (pointer log recorded the prop §4 falsifier discharged
   while the forward board 180 lines below still restated it as open) — *is* the C4
   motivating incident, already measured as unreachable by a gate. **Method note worth
   keeping:** a first census of ADR status headers appeared to show a messy vocabulary
   (`'Accepted - ratified'`, `'ACCEPTED'`, 33 with no value) and looked like a live gap;
   running the actual gate returned green. The census was measuring an ad-hoc regex
   against prose, not a defect. The apparent gap was in the measuring instrument —
   *verify the source, not the label*.

**Re-proposal bar:** a **dated incident** in which (i) a status word outside the declared
vocabulary, or (ii) an illegal status transition on a single authoritative surface,
reached a decision surface **while the existing gates passed green through it**. For any
cross-surface limb additionally: a **joinable shared anchor** that does not require
semantic knowledge of which ADR a given status belongs to — absent that, the proposal is
C1/C4 in new clothing and is rejected on sight. A restated plausibility argument that
"prose grammar could drift" does not clear the bar.

**Do not conflate — two distinct things came from the same external source.** The
*methodology-layer* status-grammar gate is rejected here. The *rail-layer* constraint
from the same source — a **functional property** (one strategy intent → at most one
accepted venue order) — is **admissible and pre-registered separately** at
[`docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md`](../spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md).
It clears the bar this entry fails: a dated incident (2026-07-27, an unintended 8-lot
live fill from a re-POSTed payload), an unguarded surface (no join by `order_id` exists
anywhere in `ops/`), and a falsifier that was run and passed before authoring. Rejecting
the diagnostic is not rejecting the constraint class.

---

## Audit hooks

```bash
# Status-grammar rejection basis: BOTH gates must still exist and pass. If either goes
# red or is deleted, the 2026-07-29 rejection's reason 1 no longer holds — re-open it.
python scripts/check_adr_graph.py && python scripts/check_status_consistency.py

# Closure-pointer integrity: every rejected signal names its disposition source
grep -n "Disposition source" docs/methodology/rejected_signals.md

# Re-proposal-bar discipline: every entry states a dated-incident re-proposal bar
grep -n "Re-proposal bar" docs/methodology/rejected_signals.md

# Conflation guard: within-stream (rejected) must stay distinct from cross-stream #8 (accepted)
grep -n "Cross-stream drain\|within-stream" docs/methodology/rejected_signals.md
```
