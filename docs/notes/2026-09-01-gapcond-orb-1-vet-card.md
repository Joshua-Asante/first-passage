# Vet card — `GAPCOND-ORB-1` (gap-magnitude-conditioned ORB-MNQ-1 day-selection)

**Date:** 2026-09-01 (v2 — re-verdict after Codex review, same day)
**Author:** Claude Code (Sonnet 5 draft · Fable 5 re-verdict)
**Status:** **`DROP`** — re-verdict 2026-09-01 after Codex's PR #249 review (7 findings, all
verified against sources, all confirmed). The original read was `PASS` (informal); two gates it
scored Clear were wrong on the merits (Shape rested on another sizing policy's bust figures;
Novelty missed a registered dead cell and a standing pre-reg prohibition), and three more were
scored Clear on unmeasured or miscalibrated inputs. This card is a Vet-speed read under
[`docs/superpowers/specs/2026-09-01-three-speed-alpha-research-design.md`](../superpowers/specs/2026-09-01-three-speed-alpha-research-design.md)
(`Proposed`); it authorizes nothing and never did.
**Operator decision:** `DROP` accepted 2026-09-01. The original false-`PASS` and this corrected
`DROP` are one named Phase-A calibration case; this accepts the candidate disposition and sample
membership only, not the proposed three-speed design as standing doctrine.
**Spend / K:** $0.00 · K=0 — every figure quoted from already-closed artifacts; no fresh
outcome-bearing comparison was computed for either the original read or this re-verdict.

---

## 0. What this is, honestly

This was the **first prospective use** of the Vet speed on a new candidate, run at the operator's
request — ahead of the spec's own Phase A (retrospective shadow-routing on closed candidates),
and disclosed as such from the start. The re-verdict makes it a better demonstration, not a
worse one: the point of a cheap front door is to kill candidates like this **before** a campaign
spends anything, and the kill arrived at $0/K=0, at review time, before any contract opened.
The accepted Phase-A pairing is recorded once in §4; it does not reopen this candidate.

**Root cause of the original miss (recorded for Phase A):** the Novelty consult searched
`docs/briefs/closures/`, `docs/rejected_candidates.md`, and the pursuit/ADR surfaces — and
trusted the source notice's own "Distinct from" line, which scopes only against the gap-fill
*fade* family and DEAD-list rows. The directly-matching prior experiment lives in
`lab/analysis/orb/orb_universe_2026-06-22/RESULTS_gap_followup3.md`, and the binding prohibition
lives in a forbidden-moves row of the unpark ADR — neither surface was swept. This is the
standing lesson verbatim: an empty grep on the surfaces you chose is not evidence of no prior
work.

**Prior-art correction (2026-09-01, pre-review):** this card originally flagged
[`2026-08-30-generate-evaluate-tensions.md`](2026-08-30-generate-evaluate-tensions.md) as an
*unreconciled alternative* design. Wrong — its recommendations were ratified 2026-08-30 as six
Accepted ADRs ([`candidate-contract`](../adr/2026-08-30-candidate-contract.md) ·
[`terminal-taxonomy`](../adr/2026-08-30-terminal-taxonomy.md) ·
[`evaluation-order`](../adr/2026-08-30-evaluation-order.md) ·
[`tradeable-reachable-gate`](../adr/2026-08-30-tradeable-reachable-gate.md) ·
[`operator-approvals-campaign-envelope`](../adr/2026-08-30-operator-approvals-campaign-envelope.md) ·
[`channel-liveness-gate`](../adr/2026-08-30-channel-liveness-gate.md)). Any future proceed
decision on any candidate runs under those ADRs (candidate contract, `TRADEABLE-REACHABLE`,
reservation-before-probe, campaign envelope, four-verdict confirm vocabulary).

---

## 1. Vet card (fields as corrected; strikethrough-worthy claims replaced, originals noted)

| Field | Content |
|---|---|
| **Candidate ID** | `GAPCOND-ORB-1` v0.1 |
| **Observation / source** | [`N-2026-08-29-mnq-gap-magnitude-rth-range.md`](notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md) — `GRADUATE`, blind-lane K=5, p≈0.00225 on the D5 stage-1 falsifier. The notice's "Distinct from" line covers the gap-fill *fade* family only — it does not clear the gap-**conditioned-ORB** family, which has its own prior art (Novelty row below). |
| **Decision bridge** | Trade/skip `ORB-MNQ-1`'s frozen entry days on pre-open gap magnitude (\|open_d − close_{d−1}\|, known 09:30:00 ET). Intended as re-entry evidence for the b3 payability pursuit (`docs/pursuits/b3-orb-mnq-payability-line.md`). |
| **Trade expression** | `ORB-MNQ-1` byte-frozen; new element = a frozen P80 gap-magnitude entry-day gate. **This makes it a conditioning gate on ORB-MNQ — a move the reconstruction pre-reg's §5 forbids outright** (see Novelty). |
| **Role** | Entry-day filter (conditioner) on a parked directional construct. |
| **Venue legality** | MNQ legal; occupancy released (2026-08-12 ADR); intraday, flat by close; micro cap 80 ≫ k=1–2. **Activity caveat (review finding):** `Tradeify_Select_100K` requires ≥1 trade/week (`inactivity_max_idle_days: 5`, account-ending). A P80 day filter (~20% of sessions) can idle >5 consecutive sessions, so the *standalone* expression does not satisfy the venue's activity rule by construction — it would need an account-level activity source (companion book, or the operator-placed token trade, which is a manual practice and cannot be assumed into strategy results). |
| **Data route** | $0 — on-disk `MNQ_M15.csv`, `Q-RANGECOND-1`'s harness with the bias swapped. Gap magnitude uses no overnight window, so both 2026-08-31 `overnight_ohlc` defects are structurally irrelevant to it. (This row survives review unchanged.) |
| **Cost reachability** | **Corrected — original was too strong.** The unchanged dollar fee (RT ≈1.41pt) does not imply unchanged `cost_R`: ORB's cost gate is R-denominated (`cost_R = RT / OR-stop distance`), and a range-correlated day filter changes the retained trades' OR-width distribution. The notice establishes full-session RTH-range conditioning, not 30-min OR geometry. Conditioned `cost_R` is unmeasured; the gate cannot be scored Clear from the fee alone. |
| **Payoff-shape reachability** | **Corrected — original was wrong.** The 0.00%-bust figures cited from `Q-ORBSURV-1` belong to the **cushion-proportional `pol_cushion` sizing** configurations, not to the frozen fixed-k ORB expression. The unchanged fixed-k expression measured intraday-honest bust **67.67% (k=1) / 77.01% (k=2)** vs. the ceiling — the arithmetic that falsified the payability target ([unpark ADR](../adr/2026-07-31-orb-mnq-unpark-payability-target.md) · [re-park ADR](../adr/2026-08-03-orb-mnq-repark-payability-falsified.md)). Survival is very much the open problem for this expression; a day filter reduces exposure but its effect on the bust path is unmeasured, and cushion sizing as a rescue is its own separately-parked thread (`Q-ORBSURV-1` `FALSIFIED` full-panel k=2; `Q-ORBCUSH-1` `STOP`). Corrected WR baseline: unconditioned **47.22%** (corrected run, `rangecond_1_2026-08-30/RESULTS.md:119`), not the retracted 41.72% — required lift to the 55% floor ≈ **+7.8pp**, not 13pp. |
| **Power / cadence** | **Corrected — original was miscalibrated twice.** (i) The ±6.5pp CI half-width vs. a ≈7.8pp required lift is marginal, not comfortable. (ii) The n≈346 / CI figures come from scoring the **entire current panel**; under the funnel, power must hold on the reserved (post-partition) stages, each with substantially fewer conditioned observations. Unresolvable until a partition is frozen — cannot be scored Clear. |
| **Economic prior** | Weak, near-`UNATTRIBUTED` (unchanged from v1): `Q-RANGECOND-1`'s corrected closure is direct evidence that range prediction ≠ ORB lift for the *stronger* sibling conditioner. |
| **Prior-art consult** | **Corrected — the decisive miss.** [`RESULTS_gap_followup3.md`](../../lab/analysis/orb/orb_universe_2026-06-22/RESULTS_gap_followup3.md) (2026-06-22) already tested gap-conditioned ORB entry — a 12-cell grid including sign-agnostic **P80** cuts — and returned **NOT-CONFIRMED at lock grade** (family-wise p=0.122 by three methods; adversarially verified), with a recorded revival path: *"fresh single-hypothesis pre-reg on independent data, not a parameter nudge."* Separately and bindingly, the [unpark ADR](../adr/2026-07-31-orb-mnq-unpark-payability-target.md) forbidden-moves row: **"Re-adding conditioning gates to ORB-MNQ itself. Four attempts (overnight-path / gap / GEX / T10Y3M) and two selection cuts (Friday, DOW) are FALSIFIED and registered; pre-reg §5 forbids it outright, and any gate makes it a new candidate at floor 0.98."** The gap×ORB cell is not untested — it is tested, dead, and gate-re-adds are prohibited. `Q-RANGECOND-1`'s narrow closure scope (one pairing) is real but does not reopen what the pre-reg and registry already closed. |
| **Search declaration** | Moot under `DROP`. (v1 proposed K_intrinsic=1 with the Confirm reserve open — the review correctly noted the open reserve also invalidated the Power read.) |
| **Kill conditions** | **Corrected:** "reuse `Q-RANGECOND-1`'s gates verbatim" must include its L1 branch — `n_conditioned < 30` → `AMBIGUOUS-HOLD`, not dead. v1's "any miss is dead" contradicted the verbatim claim. Recorded for any future proposal in this family. |

---

## 2. Six-gate re-read

| Gate | v1 read | v2 read | Basis |
|---|---|---|---|
| Decision | Clear | **Clear** | The bridge is real and precisely stated — the one part of this candidate that was sound. |
| Structural | Clear | **Conditional fail** | Standalone expression violates the ≥1-trade/week venue rule by construction under a P80 filter; needs an account-level activity source not supplied by the expression. |
| Cost | Clear | **Unresolved** | Conditioned `cost_R` unmeasured; fee-invariance argument insufficient in R units. |
| Shape | Clear | **Fail** | Fixed-k bust is 67.67%/77.01% intraday-honest — the 0% figures belong to cushion sizing. Survival is unsolved for this expression; the filter's effect on the bust path is unmeasured. |
| Power | Clear | **Not clear** | ±6.5pp CI vs ≈7.8pp required lift, on the *full* panel; post-partition power necessarily worse and unknowable until a reserve is frozen. |
| Novelty | Clear | **Fail** | Registered dead cell (gap-conditioned ORB, incl. P80, nulled at lock grade) + standing pre-reg §5 prohibition on re-adding conditioning gates to ORB-MNQ. |

**Re-verdict: `DROP`.** Two hard gate failures (Shape, Novelty) plus a structural conditional
fail; the remaining unresolved gates are moot. Under the card's own output table this is a
binding impossibility as proposed, not a missing input.

**Re-proposal bar (recorded, composited from the owning sources — all three limbs required):**

1. `RESULTS_gap_followup3.md`'s recorded revival path: a **fresh single-hypothesis**
   pre-registration (sign-agnostic big-\|gap\| cut named a priori, no grid) on **independent
   data** — not a parameter nudge, and not satisfied by the range-prediction notice (a different
   hypothesis; and `Q-RANGECOND-1` showed range-prediction does not transfer to ORB lift);
2. the unpark ADR / pre-reg §5 route: any conditioning gate on ORB-MNQ is a **new candidate at
   DSR floor 0.98**, never a filter overlay feeding b3 re-entry evidence;
3. a survival story for the venue: evidence the expression (at its proposed sizing policy) can
   clear the intraday-honest bust ceiling — the 67.67%/77.01% fixed-k record stands until
   something measured replaces it.

---

## 3. Runner-ups considered at v1, unchanged

- **Unconditioned ORB re-scope** — blocked; the post-break-only window is a seen-result window;
  `Q-ORBCUSH-1` `STOP`ped.
- **MYM twin candidates** — post-dated by the 2026-08-31 MYM scope-gap defect; no parked survivor
  construct on MYM to bridge onto.
- **Fresh literature harvest** — no measurement cost, but the raised admission bar points at
  in-house evidence first. (v1's parenthetical "survival is solved" is retracted with the Shape
  correction above; the routing conclusion stands on the other grounds.)

With `GAPCOND-ORB-1` dropped, the honest current answer to "best available Tradeify candidate"
reverts to: **no candidate currently clears Vet** — consistent with the standing
channels-dry/bottleneck diagnostics. That is a valid Vet outcome, not a failure of the exercise.

---

## 4. Process notes

- The kill cost $0 and K=0, landed at review time, before any contract, pull, or campaign — the
  funnel's front door plus the standing Codex-review workflow doing exactly their job.
- Both card versions are in the spec's Phase-A shadow-routing sample as one named calibration
  case: v1 as a measured false-`PASS` (with its root cause recorded above), v2 as the corrected
  `DROP` routing. This sample entry changes neither version's historical evidence nor the proposed
  spec's ratification status.
