# ADR 2026-07-14 — Prop-portfolio candidate class widened: pre-registered existing-strategy book candidates admitted to the frozen survivor gate

**Status:** Accepted (operator executive decision 2026-07-15 — Day-0 of the quad-track plan; drafting had been authorized 2026-07-14)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - the "ACTIVE_FIRM stays FXIFY" clause only (ACTIVE_FIRM was deleted outright in Phase 4, merged 2026-07-30 PR #572 — not repointed; live firm selection is now always an explicit FIRM_RULES key).
**Superseded-in-part-by:** `docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md` - the "survivor-scoring pre-registration... ceiling... untouched" clause only (Part A bust ceiling moved 3.0% → 5.0%, operator risk-tolerance override, 2026-08-26).
**Retain-until:** none
**Decision date:** 2026-07-14
**Authors:** Joshua (direction) + Claude Code (Fable 5, recorder)
**Supersedes:** `2026-07-12-prop-portfolio-four-friendly-firms.md` in part - its candidate-class scoping only (Section 2 "R6 boundary" second sentence and Section 5 bullet 2). Its firm set, registry, gating, Section 4 falsifier, and every other clause stand.
**Related:** Q-KBUDGET-1 ([closure: AMBIGUOUS-HOLD](../briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md)) — the motivating verdict; [`2026-07-13-prop-survivor-scoring-prereg`](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) (the unchanged gate); [`2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md) (falsifiers preserved); [`2026-07-13-dd-protection-concept-not-constant.md`](2026-07-13-dd-protection-concept-not-constant.md) (per-tier sizing variables); Q-KBUDGET-1 Phase-1 inventory Class S ([`Q-KBUDGET-1-phase1-inventory.md`](../briefs/Q-KBUDGET-1-phase1-inventory.md) §3–§4).
**Layer:** portfolio operations — **not** locked-parameter. No change to Pine, locked SL/TP/ATR, locked CFD allocations, `dd_protection` constants, `ACTIVE_FIRM`, or the FXIFY MC pins.

---

## §0 — Rule 0 reads (production-source verification, this session 2026-07-14)

- [`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](2026-07-12-prop-portfolio-four-friendly-firms.md) — anchor `fad8984` (content `0e26a7b`), read in full. The two clauses amended are quoted verbatim in §2 below.
- [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — anchor `be6dda6`, FROZEN. Part A bust ≤ 3.0% + P(pass) ≥ 50%, Run-2, frozen $100K×4 tiers, discharge ≥2 firms incl. ≥1 `trailing_locking`. **Unchanged by this ADR.**
- [`lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md`](../../lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md) + [`…bustcut…/RESULTS.md`](../../lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md) — anchor `eba5030`. Prior looks: 3-leg full-Aegis 100K bust 17.70%; 50K variants — 2-leg 0.76%, Aegis@0.75% 2.02%/1.28%; ae744↔5274c inventory delta; 1R pin-fallback artifact.
- [`ops/instruments/6J.md`](../../ops/instruments/6J.md) — anchor `fad8984`. J1 panel of record; J5 sizing reality; M6J absent at all FRIENDLY firms; verified 6J commissions.
- [`docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md`](../briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md) — this session (`b387ce1`). The AMBIGUOUS-HOLD verdict this ADR responds to.
- [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md) — cited-in-force; R5/P2 falsifiers preserved (§2 constraint 1).

---

## §1 — Context

Q-KBUDGET-1 (2026-07-14) screened the operator-ratified discovery-axis inventory under the frozen reachability screen and returned **AMBIGUOUS-HOLD**: 5/5 screenable discovery axes FAIL a-priori, and the two survivors are unsupplied-input questions, not ready axes. Newly-started discovery therefore cannot currently be shown reachable for the four-firms ADR §4 primary falsifier (hard date **2026-11-08**; demotion to research-only if no candidate clears). The four-firms ADR's candidate class is, as written, Gen-2 discovery survivors only — a class that is empty and, on today's evidence, likely to stay empty through the runway. Meanwhile the existing locked legs' **native-futures book expressions** carry measured prior looks *inside* the frozen ceiling (bustcut 2026-07-11: 2-leg 0.76%, Aegis@0.75% 2.02% at Tradeify 50K geometry-only) on a gate surface (the frozen $100K×4 cross-section) that has never been run. Operator directive 2026-07-14: "use existing strategies as a survivor path."

**Decision driver (one sentence):** the 11-08 falsifier's only currently-evidenced route runs through a candidate class the program ADR excludes, and the exclusion's stated reason (edge-transfer falsification) does not apply to the claim this class would actually make.

---

## §2 — Decision

**The prop-portfolio program's candidate class is widened to also admit *pre-registered existing-strategy book candidates*: books composed of the locked legs' native-futures expressions (currently MYM / MNQ / 6J prototypes), with per-tier allocation weights and sizing treated as venue variables, scored through the unchanged frozen survivor-scoring gate on equal terms with discovery survivors.**

Amended clauses (verbatim → amended):

1. Four-firms ADR §2 R6-boundary sentence — *"This program builds **new** prop-envelope portfolios; it does not re-open R5/P2 edge-transfer on the locked parameters."* → The program builds prop-envelope portfolios from **either** Gen-2 discovery survivors **or** pre-registered existing-strategy books. It **still does not re-open R5/P2**: an existing-strategy candidate's claim is **native-book bust-geometry at firm tiers** (panels as measured on the futures venue, costs included) — never CFD-edge preservation. R5/P2 remain FALSIFIED and citing this ADR to relitigate them is forbidden (§5).
2. Four-firms ADR §5 bullet — *"Deploying the locked four-strategy portfolio to prop firms under this ADR — different program, different portfolios; locked parameters stay immutable."* → Narrowed, not deleted: deploying the locked book **at its locked CFD allocations, or on any claim of CFD-edge transfer,** stays forbidden. A pre-registered book of locked-leg futures expressions with per-tier weights is admissible **as a candidate for scoring**; locked parameters (Pine/SL/TP/ATR and the CFD allocation lock) stay immutable — per-tier weights are `(portfolio, firm-tier)` variables in the sense of the dd-geometry concept-not-constant ADR.

**Constraints preserved (unchanged, restated for the reader):** the survivor-scoring pre-registration is untouched (ceiling, tiers, G0–G8, discharge rule, F1/F2 handling); rail build + account registration stay gated; `ACTIVE_FIRM` stays FXIFY; every candidate needs its **own pre-registration before any frozen-$100K-tier G4 run**, fixing the variant set and **disclosing all prior looks** (the 2026-07-10/11 Tradeify runs); the Aegis input defect (BEPAD-TEST CSV, ae744↔5274c delta, 1R pin basis) must be resolved before an Aegis-bearing candidate pre-registers (Cursor handoff ordered 2026-07-14).

**Effective:** upon operator acceptance (status flip to `Accepted`).
**Scope:** candidate-class definition for the four-firms prop-portfolio program only. No effect on the self-funded Aegis→M6J lane, the locked CFD book, or any discovery-side gate.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — discovery-only candidate class** | Q-KBUDGET-1: that class is empty a-priori on current inputs; holding it sole-source makes the 11-08 demotion near-certain by construction rather than by evidence. |
| **Rescind the four-firms program (accept demotion now)** | Premature — an evidenced candidate route exists (bustcut priors inside the frozen ceiling on an unrun surface); demotion without running the frozen gate once would decide on no new evidence. |
| **Reopen R5/P2 edge-transfer for the locked book** | The falsifiers are operator-accepted closures (DJ30→MYM 0.559 < 0.8×; NAS100 dead on micros); nothing new refutes them. This ADR deliberately does not need them reopened — bust-geometry at a firm tier is a different claim from CFD-edge preservation. |
| **Route existing-strategy books through Q-KBUDGET-1's screen instead** | Ratified against (inventory §6 ask 2): they are not newly-started discovery; Clause K's DSR floor is a category mismatch for candidates whose gate has no DSR clause. Screening them literally (honest K≈8 → FAIL) would kill the route inside an instrument built for a different question. |
| **Amend the survivor-scoring ceiling to fit the book (e.g. relax 3.0%)** | Trap-12 / forbidden by the pre-reg's own §5; the ceiling stays frozen — the book must clear it as-is or the route dies honestly. |

---

## §4 — Falsifier (revert trigger)

**H (amendment adds value):** at least one pre-registered existing-strategy book candidate clears the frozen Part A (bust ≤ 3.0% + P(pass) ≥ 50%, Run-2, $100K band) on ≥2 distinct FRIENDLY firms incl. ≥1 `trailing_locking`, by **2026-11-08**.

**Revert trigger (binary):** by 2026-11-08, no existing-strategy book candidate clears Part A on **any** frozen tier in a dated, pre-registered G4 re-MC → **H is falsified** and this amendment expires with the parent §4 demotion (prop program → research-only); the widened candidate class conferred nothing and is retired with it. The falsifier is deliberately the parent's own, inherited — no separate ceiling, date, or denominator is introduced. **Early-fail branch:** if the *first* pre-registered existing-strategy candidate fails Part A on **all four** frozen tiers, any second candidate requires fresh operator authorization (no variant-grinding through the gate — each candidate consumes an explicit operator decision).

**Revert action:** none needed beyond the parent's (the parent ADR §4 demotion covers it); never edit this §2 in place — supersede.

**Trigger check schedule:** rides the parent's — 2026-08-08 progress check, 2026-11-08 hard date.

---

## §5 — Forbidden moves (under this ADR; each genuinely tempting)

- **Citing MYM/MNQ absolute PF (~2) as evidence that P2 edge-transfer was wrong** — the temptation the moment a candidate clears. P2 measured *ratio-to-CFD*, and it stays FALSIFIED; this program's claim is bust-geometry on native panels, full stop.
- **Running the frozen $100K×4 tiers before the candidate pre-registration is committed** — the 50K priors are already visible; only a pre-committed variant set with prior-look disclosure keeps the gate honest (best-of-K at the book-composition layer is the live risk — ~7 variants have already been examined).
- **Tuning book weights after seeing per-tier results** — same trap, gate layer; the pre-registration fixes weights; a failed candidate closes, it does not iterate in place.
- **Reading the amendment as any easing of rail/account/go-live gating** — execution stays gated exactly as the parent ADR left it; a cleared candidate produces §4-falsifier evidence and a lifecycle CANDIDATE intake, nothing more.
- **Treating per-tier weight freedom as license to touch the locked CFD allocations or Pine** — the parameter axis is immutable; per-tier weights live beside `dd_geometry`'s per-(portfolio, firm-tier) variables, never in the locked constants.
- **Skipping the Aegis panel-of-record resolution because 2-leg (S2) doesn't need it** — tempting sequencing shortcut; admissible only if the pre-registered candidate genuinely contains no Aegis leg, and the pre-registration must say so explicitly.

---

## §6 — Consequences

**Positive:**
- The 11-08 falsifier gets a currently-evidenced route; the program's fate rests on a run of the frozen gate rather than on an empty candidate class.
- Zero new gate machinery — reuses the frozen pre-registration, the G0–G8 harness (`lab/discovery/prop_survivor_scoring.py`), and `core/mc/preflight.py` as-is.

**Negative (real cost):**
- The clean "greenfield-only" program identity is diluted; future readers must hold "R5/P2 falsified" and "locked-leg books admissible" simultaneously — the §2 claim-separation carries that load and will be misread by default (mitigation: §5 bullet 1).
- Prior-look contamination is real: the candidate class arrives with ~7 examined variants; the pre-registration discipline (disclosure + fixed variant set) bounds but does not erase it.

**Risks:**
- The 50K→100K geometry deterioration (10.33%→17.70% for the full book) may put every re-weighted variant above 3.0% at the frozen band — the route dies at first scoring (handled: that is the honest outcome; early-fail branch in §4).
- Aegis input ambiguity (ae744 vs 5274c vs pinned J1) could silently change a candidate's bust by percentage points (handled: pre-registration blocked on the Cursor mechanicals).

**Downstream artifacts to update at acceptance (not before):**
- Parent ADR: add a "Superseded in part by 2026-07-14-prop-portfolio-existing-strategy-candidates" line to its header + §5 bullet 2 annotation.
- `STATE.md` four-firms forward-board line: candidate class widened; first-candidate pre-registration owed.
- 08-08 packet: C7 status note gains the Class-S route.

---

## §7 — Implementation plan

- **Phase 0** — operator reads + accepts/rejects this ADR (separate act; drafting alone changes nothing).
- **Phase 1 (at acceptance)** — parent-ADR header/§5 annotation + STATE line (§6 downstream list); grep-sweep for "does not re-open R5/P2" restatements that need the amended reading cross-referenced.
- **Phase 2** — Aegis panel-of-record mechanicals land (Cursor handoff, already ordered); THEN the first candidate pre-registration is authored (fixed variant set, prior-look disclosure, DEPLOYABLE-DEFAULT-ENVELOPE declaration per envelope §2). **Done 2026-07-15:** operator pinned **ae744** + decompound `full_stop_mean` 1R **$2,912.96 (n=11)** — [`PANEL_OF_RECORD.md`](../../lab/analysis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md). First Class-S candidate pre-reg is now the open step.
- **Phase 3** — G0–G8 scoring run on the frozen $100K×4 tiers; result feeds the §4 falsifier either way.

---

## §10 — Audit hooks (runnable)

```bash
# Status honesty: this ADR confers nothing while Proposed
grep -n "^\*\*Status:\*\*" docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md

# Bidirectional supersede chain (must exist once Accepted; absent while Proposed)
grep -n "Superseded in part" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md

# The frozen gate was not touched by this amendment (byte-stability of the ceiling numbers)
grep -n "bust ≤ 3.0%\|≥ 50%" docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md

# No candidate scored before its own pre-registration exists
ls docs/briefs/pre-registration/ | grep -i "existing-strategy\|book-candidate" || echo "no candidate pre-reg yet (expected while Proposed)"

# R5/P2 falsifiers still in force (this ADR must never be cited against them)
grep -n "FALSIFIED" docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md | head -3
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md --type adr
# §0 anchors
git log -1 --format='%h %ci' -- docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md            # fad8984
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md  # be6dda6
git log -1 --format='%h %ci' -- lab/analysis/c1/tradeify_futures3_bustcut_2026-07-11/RESULTS.md          # eba5030
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-14 | Drafted (`Proposed`) per operator authorization — Q-KBUDGET-1 inventory §6 ask 3 | Joshua + Claude Code (Fable 5) |
| 2026-07-15 | Accepted — operator directed Day-0 of the Class-S / D5 / SFRISK quad-track plan; §6 downstream annotations landed same session | Joshua + Cursor |
| 2026-07-15 | Aegis prop panel pick — ae744 + decompound 1R $2,912.96 (n=11); Phase 2 Aegis gate cleared | Joshua + Cursor |
