# Q-OBJCOHERE-1 — Do the operation's ratified decision instruments compose coherently?

**Status:** `CLOSED — FALSIFIED-COHERENT` (operator ratification 2026-07-30, chat: "I ratify OBJCOHERE-1. Proceed with it")
**Authored:** 2026-07-29
**Ratified:** 2026-07-30
**Closed:** 2026-07-30 — see [closure](closures/Q-OBJCOHERE-1-closure-falsified-coherent.md)
**Authors:** Joshua (trigger question) + Claude Code (authoring)
**Parent question:** N/A (derived from the 2026-07-29 comparative-advantage thesis, `docs/notes/2026-07-29-comparative-advantage-thesis.md` §4/§6)
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gates on the §6 table below; doc-layer audit only ($0, K=0, no data touched)
**Artifact path:** `docs/briefs/Q-OBJCOHERE-1-objective-coherence-audit.md`
**Queue note:** per the STATE.md standing rule (L25), this packet queues **behind** the operator
queue by default; the operator's 2026-07-30 ratification ("proceed with it") is the explicit queue-
placement decision the brief required, made in the same breath as ratification. It still rides
nothing on B7/M1 and does not touch, delay, or reorder queue items 1–4 (all doc-layer, $0, K=0).

---

## §0 — Rule 0 reads (production-source verification)

All reads performed 2026-07-29 at worktree HEAD `b99871f` (branch `claude/first-passage-edge-253b8c`),
via a six-reader evidence workflow (`wf_0b87bdcd-098`) with parent-side grep re-verification of every
line cited below (executed outputs recorded in the thesis §Verification, same date).

- `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md` — anchor: L17, L37–46, L55–57. The one
  ratified EV objective; scope clause verbatim: "the c1 book's rung selection only. Not candidate
  admission; not the locked strategies' parameters; not `dd_protection` constants; not any other
  firm/account" (L46). Convergence claim L39 is conditional on 1.00× failing the regime gate.
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — anchor: L119
  (Part A: bust ≤ 3.0% ∧ P(pass) ≥ 50%, frozen 2026-07-13).
- `docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md` — anchor: L3 (FROZEN,
  operator-signed 2026-07-27), L104–108 (D1–D5), L160–181 (§5 forbidden moves).
- `lab/archive/c1_capalloc_2026-07-27/RESULTS.md` — anchor: L3, L62–77, L230–269 (argmax failure;
  48/32 superseded; 51/29 thin margin; verdict `AMBIGUOUS (d)`).
- `docs/spec/2026-07-27-third-leg-target-spec.md` — anchor: L233 (H-3LEG), L328–332 (T1–T5 stack),
  L364 (Stage-8 negative control: "The single requirement ORB clears is exactly the written gate
  that let it through").
- `ops/prop_envelope_default.md` — anchor: L31 (Stage-8 admission limb), L75 (documented
  decorrelation-vs-hedging conflict: rewards "exactly what this rule forbids").
- `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` — anchor: L51 (per-instance
  objective template), L75 (numeric successor objective recorded as owed, self-funded lane — lane
  parked 2026-07-16).
- `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` — anchor: L39 (target statement),
  L76 (§4 program-success hypothesis, survival-denominated).
- `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` — anchor: L20–21, L32, L70
  (frozen gate unchanged; discharge withdrawn; anti-goalpost clause).
- `STATE.md` — anchor: L20 (queue premise), L25 (queue-behind rule), L196–202 (69/11 executed as
  "an unpriced de-risking trade, defensible but never measured"; premise "MYM carries the size"
  false on P&L).
- **Dedup attestation (executed, this session):** `rg --no-ignore -n -i "objective.map" docs/` →
  the 2026-05-11 Objective-Map ADR is `Retired` (INDEX.md L107); body read at
  `docs/ltm/adr/2026-05-11-objective-map-section-4-tighten-falsifier.md` L15–30. It was a **Notion
  goal-registry layer** (Y2-O2 Objective, Calibration Scores DB, quarterly close hooks Q7/Q8/Q12),
  retired 2026-07-12 because its registry was retired 2026-06-12 — hooks unfireable-by-construction.
  Its re-proposal bar ("a revived objective-map layer needs a fresh ADR with a live registry")
  governs *that tracking layer*; this brief proposes **no registry, no tracking layer, no revival**
  — it is a one-shot coherence audit of decision gates, a different mechanism family. Name-collision
  check: `rg --no-ignore -n -i "Q-OBJ" docs/ lab/ ops/` → no existing Q-OBJ* question.
- **Owed at Phase 0 (execution time), not yet read end-to-end:**
  `docs/briefs/closures/Q-BUSTGATE-1-closure-falsified.md` (full §D locational rule),
  `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` (composition-variance precedent), and
  the fork-B ADR's §7 revert triggers in full context (±20 lines). These sharpen T1's
  constructibility test; verdict may not be declared before they are read.

---

## §1 — Context & motivation

The 2026-07-29 comparative-advantage thesis (operator-triggered) found that the operation's
decision quantities are denominated in barrier-passage functionals across **five scoped ratified
instruments** — admission (bust ≤3.0% ∧ pass ≥50%), program success (four-firms §4), allocation
(D1–D5), protection (per-instance dd objective), rung selection (EV/dollar-day among regime-robust
rungs) — with **no operation-level composition**: no ratified text says which instrument wins when
two of them disagree about the same decision. Four dated exhibits suggest this is not hypothetical:

- **T1** — a rung passing both halves with bust ∈ (3.0%, 4.37%] would be EV-selected at the rung
  layer while an identical *new* candidate is refused admission at 3.0%; the fork-B ADR's
  "no tension" claim (L39) is conditional on 1.00× currently failing the regime gate.
- **T2** — ORB-MNQ-1 passed the written Stage-8 admission limb (+0.003) and took composed bust
  2.65%→38.75%; the third-leg spec's own negative control concludes the written gates do not
  encode the operative objective (spec L364).
- **T3** — the 2026-07-22 69/11 re-allocation was executed as "an unpriced de-risking trade,
  defensible but never measured" (STATE.md L196–202): a real allocation decision taken with no
  instrument to price survival-bought against net-sold, quantified only five days later by
  Q-CAPALLOC-1, which also falsified its stated premise.
- **T4** — the envelope documents its own conflict: the §2 item-6 decorrelation gate rewards
  "exactly what this rule forbids" (the §4a hedging rule) for same-Product-Group legs (L75).

Standing doctrine this bears on: Trap #12 (frozen gates are recorded, not edited), the
concept-not-constant ADR (objectives are per-instance, pre-registered), and the four-firms §4
falsifier (hard date 2026-11-08 — any charter output of this audit must not touch that gate).

---

## §2 — Prior art / lineage

- **Q-BUSTGATE-1** — `CLOSED-FALSIFIED` 2026-07-23: the 3.0% ceiling is a survival quantity, not
  an economic one; produced the operator fork that ratified the EV rung objective. This brief
  audits the *composition* that fork created; it does not re-open the fork.
- **Q-CAPALLOC-1** — `AMBIGUOUS (d)` (re-run 2026-07-29, verdict stands): supplies T3 and the
  measured demonstration that pooled-net and halves disagree; its (d)→RESOLVED conversion is a
  separate operator decision this brief does not touch.
- **Q-COMPOSE-1** — `CLOSED-FALSIFIED`: composition raised bust via variance dominance; precedent
  that composition behavior is not derivable from per-leg gates — the same class of gap at the
  objective layer is what this brief audits.
- **2026-05-11 Objective-Map ADR** — `Retired`. Different mechanism family (goal-tracking registry);
  see §0 dedup attestation. This brief must not recreate it.
- **Lessons:** M-18 (deadline-race vs barrier geometry — constrains any charter language), M-21
  (risk-breadth vs dependence-breadth admissibility — the repaired form of T2's gap),
  `lesson_full_panel_masks_regime_split` (why halves outrank pooled anywhere they conflict).
- **Concept-not-constant ADR** — records a numeric successor objective as *owed* for the (parked)
  self-funded lane (L75): direct evidence the estate itself considers the objective layer
  incomplete, scoped to a lane this brief does not resurrect.

---

## §3 — Question (Q-OBJCOHERE-1)

Symptom-only rephrase check: the question names a gap (instruments that may return contradictory
dispositions) and not a fix (a charter is one *possible output branch*, not the question).

**Q-OBJCOHERE-1:** Which single objective, if any, do the operation's ratified decision
instruments jointly imply — and is there any constructible decision, inside currently-admissible
parameter ranges, for which two live instruments return contradictory dispositions with no written
precedence rule deciding between them?

---

## §4 — Falsifiable hypothesis (H-OBJCOHERE-1)

**H-OBJCOHERE-1:** If the audit constructs **≥1 concrete decision object** (a candidate, rung,
allocation cell, or composition move, specified with actual numbers drawn from
currently-admissible ranges) for which **instrument A mandates disposition X and instrument B
mandates ¬X**, both instruments live and ratified, and **no ratified text assigns precedence**,
then the estate is objective-fragmented and the repair is a charter ADR draft (operator ratifies
or declines). Otherwise — every candidate tension, including T1–T4, resolves to an explicit
written precedence rule — the estate is coherent, the fragmentation clause of the thesis's H-EDGE
is **FALSIFIED**, and the correct output is the composition map alone (no charter).

- **Accept (RESOLVED-INCOHERENT) if:** ≥1 contradiction per the definition above survives the
  precedence sweep (the sweep must quote the precedence text it searched for and failed to find).
- **Reject — the hypothesis is FALSIFIED (verdict `FALSIFIED-COHERENT`) — if:** all of T1–T4 plus
  any audit-found pairs resolve to quoted precedence text in a ratified artifact.
- **Ambiguous-hold if:** a tension's constructibility cannot be decided on paper — i.e. deciding
  whether the contradictory case is reachable requires a new measurement or K>0. Record it,
  hold, and name the measurement; this brief licenses no run.

Definition notes (pre-committed): "live and ratified" = Accepted ADRs, RATIFIED specs, and FROZEN
operator-signed pre-registrations currently in force (the §0 list is the census; the audit may add
to it but not subtract). "Contradictory dispositions" excludes cases where one instrument is
explicitly scoped out of the decision class (e.g. fork-B L46 already cedes admission) — those are
precedence rules, and finding them is the point.

---

## §5 — Forbidden moves

- **Editing any threshold, gate, or frozen pre-registration in the course of the audit** — the
  audit reads; only a superseding ADR may move a number (Trap #12, withdrawal-ADR L70 precedent).
  Tempting because T1 makes the 3.0%-vs-EV band *look* like a bug to fix inline.
- **Re-opening closed verdicts as "evidence of incoherence."** Q-BUSTGATE-1's fork, the rung
  election, Q-CAPALLOC-1's (d), and the TERMINAL reconstruction tracks stay owned by their
  artifacts. Incoherence is about *live instruments disagreeing*, not about past decisions one
  might dislike.
- **Constructing T1's rung as a proposal.** The audit needs the hypothetical (a both-halves-passing
  rung with bust in (3.0%, 4.37%]) only to test whether written precedence exists; going and
  *looking for* such a rung is a sizing investigation this brief does not license.
- **Running anything.** $0, K=0, no MC, no data pull. If a tension needs a run to adjudicate, that
  is the AMBIGUOUS-HOLD branch by definition — tempting because T3's pricing question ("what did
  the 69/11 survival purchase cost?") is one Q-CAPALLOC harness invocation away.
- **Self-ratifying the charter branch.** RESOLVED-INCOHERENT produces a *draft* ADR; ratification,
  queue position, and even whether the charter is wanted at all are operator decisions.
- **Recreating the Objective-Map.** No registry, no tracked metrics, no recurring hooks. The
  output is one map + at most one draft ADR, both inert documents.
- **Scoring which objective is "better."** The question is whether the instruments compose, not
  whether survival should beat EV — preference questions route to the operator via the charter
  draft's options, never resolved inside the audit.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED-INCOHERENT` | ≥1 constructed decision object meets the §4 contradiction definition AND the precedence sweep for that pair comes back empty (sweep documented: artifacts searched, quotes absent) | Close; author charter-ADR **draft** enumerating the contradiction(s) + candidate precedence rules as operator options; thesis H-EDGE fragmentation clause CONFIRMED on the record |
| `FALSIFIED-COHERENT` | Zero constructible contradictions: T1–T4 and every audit-found pair each resolve to quoted precedence text in a ratified artifact — H-OBJCOHERE-1's fragmentation claim is falsified | Close; publish the composition map (instrument → decision class → precedence citations) as a standing reference doc; append falsification addendum to the thesis §4 |
| `AMBIGUOUS-HOLD` | Every unresolved tension lands in the "constructibility undecidable on paper" branch (needs measurement/K>0), and zero paper-decidable contradictions exist | Close AMBIGUOUS; record each blocked tension + the measurement that would decide it; re-test only if/when that measurement is separately authorized (no date — this brief creates no obligation) |

Pre-registered before execution per §8. Mixed outcomes resolve by precedence: any single
paper-decidable contradiction ⇒ `RESOLVED-INCOHERENT` regardless of how many others are blocked.

---

## §7 — Execution plan (self-executing, single session, agent-executable)

- **Phase 0 — Rule-0 reads.** The two owed closures + fork-B §7 in ±20-line context (§0 last
  bullet). Re-verify every §0 line anchor still resolves at execution HEAD (hooks in §10).
- **Phase 1 — Instrument inventory.** One table: instrument · owning artifact · decision class it
  governs · denomination (survival / expectancy / cost / structural) · every explicit scope or
  precedence clause, quoted verbatim with line numbers. Census starts from §0; sweep
  `docs/adr/*.md` (Accepted only) + `docs/spec/*.md` (RATIFIED only) + FROZEN pre-registrations
  for additions.
- **Phase 2 — Adjudicate T1–T4, then pairwise sweep.** For each tension: construct the concrete
  decision object with numbers, run the precedence sweep, classify per §4. Then sweep remaining
  instrument pairs sharing a decision class for additional candidates (bounded by the Phase-1
  table — no open-ended search).
- **Phase 3 — Verdict.** Apply §6 mechanically; produce the closure artifact per §9 + the map
  (both branches produce the map; only one produces a charter draft).

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

`docs/briefs/pre-registration/Q-OBJCOHERE-1-verdict-preregistration.md` — to contain the §6 table
plus the §4 contradiction definition verbatim, committed **before** Phase 1 begins. Not yet
authored: pre-registration is committed only after operator signature on this brief (no point
freezing a gate the operator may re-shape at signing).

Pre-registration commit hash: `<populated at pre-registration commit time>`
Pre-registration date: pending

---

## §9 — Closure record format

**SIGNED.** Operator ratification 2026-07-30 (chat: "I ratify OBJCOHERE-1. Proceed with it").
Queue placement: proceed now (operator election). On closure:

- `RESOLVED-INCOHERENT` → `docs/briefs/closures/Q-OBJCOHERE-1-closure-resolved-incoherent.md` +
  charter-ADR draft at `docs/adr/DRAFT-objective-composition-charter.md` (status `Proposed`).
- `FALSIFIED-COHERENT` → `docs/briefs/closures/Q-OBJCOHERE-1-closure-falsified-coherent.md` +
  composition map at `docs/methodology/objective_composition_map.md` + thesis §4 addendum.
- `AMBIGUOUS-HOLD` → `docs/briefs/closures/Q-OBJCOHERE-1-closure-ambiguous.md` with the blocked
  tensions + deciding measurements named.

Closure must include: verdict vs the pre-registered definition, the full precedence-sweep record
(what was searched, what was quoted or absent), and lesson candidates only if dated-anchored
(Trap #9).

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve at execution HEAD:
rg -n "the c1 book's rung selection only" docs/adr/2026-07-23-c1-rung-selection-ev-objective.md
rg -n "bust ≤ 3.0%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | head -1
rg -n "exactly what this rule forbids" ops/prop_envelope_default.md
rg -n "written gate that let it through" docs/spec/2026-07-27-third-leg-target-spec.md   # M-AHF: phrase wraps a line break in storage; matched on the shorter, wrap-safe substring
rg -n "unpriced de-risking trade" STATE.md

# The audit changed nothing (run after closure — all must return empty):
git diff --stat -- core/ ops/c1_rail/c1_sizing_host_reference.py ops/prop_envelope_default.md \
  docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md \
  docs/briefs/pre-registration/Q-CAPALLOC-1-verdict-preregistration.md

# No registry was recreated (Objective-Map forbidden move):
rg -rn --no-ignore -i "objective.map registry" docs/ --glob '!docs/ltm/**' ; echo "expect: no live registry"

# Pre-registration preceded Phase 1 (run at closure):
git log --oneline -- docs/briefs/pre-registration/Q-OBJCOHERE-1-verdict-preregistration.md

# Closure artifacts exist (post-closure — verdict was FALSIFIED-COHERENT):
test -f docs/briefs/closures/Q-OBJCOHERE-1-closure-falsified-coherent.md && echo OK
test -f docs/methodology/objective_composition_map.md && echo OK
rg -n "H-EDGE FALSIFIED" docs/notes/2026-07-29-comparative-advantage-thesis.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/Q-OBJCOHERE-1-objective-coherence-audit.md --type inquire

# Production-source verification (Rule 0) — executed 2026-07-29, outputs in the thesis §Verification:
#   D1 functional at prereg L104; EV objective at ADR title/L37; scope clause L46;
#   admission gate L119; envelope conflict L75; spec negative control L364;
#   owed successor objective L75; Objective-Map retired body read in LTM; no Q-OBJ* collision.
```

---

## Pre-Lock Checklist (DRAFT brief)

- [x] §0 paths read and anchored (worktree `b99871f`, 2026-07-29; two closure reads explicitly owed at Phase 0)
- [x] §3 question passes the symptom-only rephrase test (charter is an output branch, not the question)
- [x] §4 hypothesis binary; contradiction definition pre-committed
- [x] §5 forbidden moves are the genuinely tempting ones (inline fix of T1; running the T3 pricing; proposing the T1 rung)
- [x] §6 triggers specific; mixed-outcome precedence stated
- [x] §8 pre-registration committed (post-signature, pre-Phase-1 — see pre-reg commit hash)
- [x] §10 hooks runnable
- [x] Closed 2026-07-30: `FALSIFIED-COHERENT` — see [closure](closures/Q-OBJCOHERE-1-closure-falsified-coherent.md)
- [x] Operator signature (§9) — 2026-07-30, "I ratify OBJCOHERE-1. Proceed with it"
