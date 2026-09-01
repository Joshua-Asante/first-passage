# Vet card — `GAPCOND-ORB-1` (gap-magnitude-conditioned ORB-MNQ-1 day-selection)

**Date:** 2026-09-01
**Author:** Claude Code (Sonnet 5)
**Status:** `PASS` (informal) — a Vet-speed read under [`docs/superpowers/specs/2026-09-01-three-speed-alpha-research-design.md`](../superpowers/specs/2026-09-01-three-speed-alpha-research-design.md) (`Proposed`, PR [#246](https://github.com/Joshua-Asante/first-passage/pull/246)/[#247](https://github.com/Joshua-Asante/first-passage/pull/247)). That spec authorizes **no campaign, data pull, K spend, status change, Pine build, lifecycle change, or deployment action** until ratified — this card records a read, not a GO.
**Spend / K:** $0.00 · K=0 for this card — every figure below is quoted from an already-closed artifact; no fresh outcome-bearing comparison was computed to produce this read.

---

## 0. What this is, honestly

This is the **first prospective use** of the Vet speed on a new candidate, run at the operator's request. It is **not** the design's own Phase A (retrospective shadow-routing on a frozen sample of *closed* candidates) — that step, named in the spec's §10 as the prerequisite before any live use, has not been run. This card is therefore informal evidence about whether Vet is useful, not a validated instance of it. Treat the `PASS` label accordingly: it means "six gates read clear on inspection," not "a ratified process certified this."

**Prior-art correction (2026-09-01, same day):** this card originally flagged
[`2026-08-30-generate-evaluate-tensions.md`](2026-08-30-generate-evaluate-tensions.md) as an
*unreconciled alternative* design. That was wrong in an important direction: the note's
recommendations had already been **ratified 2026-08-30 as six Accepted ADRs**
([`candidate-contract`](../adr/2026-08-30-candidate-contract.md) ·
[`terminal-taxonomy`](../adr/2026-08-30-terminal-taxonomy.md) ·
[`evaluation-order`](../adr/2026-08-30-evaluation-order.md) ·
[`tradeable-reachable-gate`](../adr/2026-08-30-tradeable-reachable-gate.md) ·
[`operator-approvals-campaign-envelope`](../adr/2026-08-30-operator-approvals-campaign-envelope.md) ·
[`channel-liveness-gate`](../adr/2026-08-30-channel-liveness-gate.md)) — standing doctrine, not a
competing proposal. This card's six-gate read is unaffected (it consumed only closed campaign
artifacts and venue facts), but any next step runs under those ADRs: a proceed decision opens a
**candidate contract** per `candidate-contract` §2 — with the `TRADEABLE-REACHABLE` pre-gate,
CONFIRM-reservation-before-probe ordering, campaign envelope, and the four-verdict confirm
vocabulary — not a freestanding "Generate charter." The three-speed spec (PR #250, v3) is now a
thin wrapper over those owners.

---

## 1. Vet card

| Field | Content |
|---|---|
| **Candidate ID** | `GAPCOND-ORB-1` v0.1 |
| **Observation / source** | [`N-2026-08-29-mnq-gap-magnitude-rth-range.md`](notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md) — `GRADUATE`, blind-lane K=5, closed p≈0.00225 on the D5 stage-1 falsifier (beats matched day-history control). No strength inflation: this is the *weaker* of the two GRADUATEd MNQ range predictors from the same batch. |
| **Decision bridge** | Trade/skip each of `ORB-MNQ-1`'s frozen entry days on pre-open gap magnitude (\|open_d − close_{d−1}\|, known at 09:30:00 ET, before the construct's own entry clock). A validated lift is the "new re-entry evidence" the b3 payability pursuit (estate queue priority #1, `docs/pursuits/b3-orb-mnq-payability-line.md`) is explicitly waiting on. |
| **Trade expression** | `ORB-MNQ-1`'s construct stays byte-frozen — entry, stop, exit untouched. The only new element is a frozen entry-day gate (top quintile / P80, the notice's own definition, no threshold search). |
| **Role** | Entry-day filter (conditioner) on an already-admitted directional construct — the funnel's §8 first named bridge type. |
| **Venue legality** | MNQ; occupancy released for non-Striker research (2026-08-12 ADR); intraday, flat by close; micro cap 80 ≫ any k this construct has ever sized at (k=1–2). |
| **Data route** | $0 — on-disk `MNQ_M15.csv`, reusing `Q-RANGECOND-1`'s harness with the bias series swapped from overnight-range to gap-magnitude. `data_lib.py::overnight_ohlc` (the source of both 2026-08-31 defects) isn't even implicated: gap magnitude uses no overnight window at all, so this candidate is structurally untouched by either the MNQ look-ahead or the MYM scope-gap defect. |
| **Cost reachability** | The filter only removes trade-days; the per-trade cost basis (Tradeify RT ≈1.41pt) is unchanged from the already-admitted construct. No new cost hurdle is introduced by this candidate. |
| **Payoff-shape reachability** | The venue's binding gate is the $3,000 rope, not the 40% consistency rule (`lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md` §7, cited at `core/firm_rules.py:404-405`). `Q-ORBSURV-1` measured bust at **0.00%** for both k=1 and k=2 — survival is not the open problem; win rate is (41.7% unconditioned vs. the ≥55% shape target `Q-RANGECOND-1`'s own L4 gate already used for this exact construct). |
| **Power / cadence** | Expected n_conditioned ≈ 300–350, by direct analogy to `Q-RANGECOND-1`'s corrected run (n=346 on the same-shape overnight-range gate). That run's corrected CI width was ≈±6.5pp on the WR-diff — comfortably powered to detect the ≈13pp lift the shape target requires, if it exists. |
| **Economic prior** | **Weak, disclosed — near-`UNATTRIBUTED`.** `Q-RANGECOND-1`'s corrected closure is direct negative evidence that "predicts RTH range magnitude" does not imply "lifts this specific breakout's win rate" — the *stronger* range predictor (overnight range, p≈0.00025) showed zero ORB lift once look-ahead was removed (WR diff +0.75pp, CI includes 0). For gap magnitude to succeed where overnight range failed, it must carry ORB-relevant information through a channel other than range prediction (e.g., overnight repricing intensity → next-session follow-through), which is a plausible story with zero direct evidence behind it. |
| **Prior-art consult** | [`Q-RANGECOND-1` closure (corrected, `FALSIFIED`)](../briefs/closures/Q-RANGECOND-1-closure-falsified.md) §3 explicitly scopes its kill to one pairing ("does not test other conditioners… or other base constructs"). `ORB-MNQ-1` stands `PARKED` (2026-08-03 ADR, unaffected). `Q-ORBSURV-1` `FALSIFIED` on full-panel k=2 pass-rate only (post-break sub-window clears both k=1/k=2). `Q-ORBCUSH-1` (regime-break mechanism) `STOP`ped — this card touches neither thread. Dense-1m/G=10 temporal-selectivity pause does not bind — `ORB-MNQ-1` is a 30-min opening-range construct (`docs/rejected_candidates.md:1398`), not a minute-scale θ-parameterised entry-geometry construct, and this card adds a daily-bar conditioner on top of it rather than a new entry geometry, so it isn't route-① reliance on the paused lane at all. |
| **Search declaration** | Proposed Generate: `K_intrinsic = 1` (one frozen threshold, one frozen pairing — same discipline `Q-RANGECOND-1` used). Confirm reserve: **open** — the current `MNQ_M15.csv` panel is ~300 days shorter than `ORB-MNQ-1`'s original G8 admission panel (disclosed in `STATE.md` row 75); a Generate charter must rule reserve-vs-full-panel before any score is read. |
| **Kill conditions** | Reuse `Q-RANGECOND-1`'s frozen gates verbatim: n≥30 · WR-diff CI excludes 0 · mean-win-diff CI excludes 0 · conditioned WR ≥55%. Any miss is dead, no threshold movement. Re-proposal bar: new mechanism evidence only, never a quintile retune. |

---

## 2. Six-gate read

| Gate | Read | Basis |
|---|---|---|
| Decision | **Clear** | Named bridge: trade/skip a specific frozen construct's entry days. |
| Structural | **Clear** | MNQ legal, occupancy released, no session/latency/product conflict. |
| Cost | **Clear** | Filter-only; inherits the already-admitted construct's cost basis unchanged. |
| Shape | **Clear** | Bust is not the binding constraint (`Q-ORBSURV-1`, 0.00% both k); WR is, and that is exactly what this filter targets. |
| Power | **Clear** | n≈300–350 expected, by direct analogy to a same-shape, already-run test. |
| Novelty | **Clear** | Not a relabeled dead cell — `Q-RANGECOND-1` tested a *different* conditioner (overnight range) on the same construct; its own closure disclaims testing this one. |

**Read: `PASS` (informal).** Cheap to test ($0, K=1, reuses an existing harness) and docks directly onto the estate's top-priority pursuit — the expected value of testing clears easily even with a low prior.

---

## 3. Runner-ups considered, not carried forward

- **Unconditioned ORB re-scope** — blocked; the post-break-only window that clears `Q-ORBSURV-1`'s pass floor is itself a seen-result window, and `Q-ORBCUSH-1` (the regime-break mechanism question) is `STOP`ped.
- **MYM twin candidates** (`N-2026-08-29-mym-*`) — post-dated by the 2026-08-31 MYM scope-gap defect; no parked survivor construct exists on MYM to bridge onto the way `ORB-MNQ-1` exists on MNQ.
- **Fresh literature harvest** — no measurement cost, but the raised admission bar and the rope's specific shape (survival is solved, WR is not) point more directly at an existing GRADUATEd in-house finding than an unscoped external search.

---

## 4. If the operator wants to proceed

The next artifact is a **candidate contract** per
[`2026-08-30-candidate-contract.md`](../adr/2026-08-30-candidate-contract.md) §2, opened under the
ratified [`evaluation-order`](../adr/2026-08-30-evaluation-order.md) pipeline: reserve the Confirm
window on the draft contract first (the panel-vintage question above must be ruled at that step),
freeze the promotion statistic (reuse `Q-RANGECOND-1`'s four gates) and the mechanism
discriminator's adjudication rule, then one operator GO on the campaign envelope covers the $0
exploration run. Nothing above authorizes that run on its own.
