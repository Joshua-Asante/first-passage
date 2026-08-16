# Q-EVALSEQ-1 — RESULTS (frozen K=4 within-eval schedule family)

**Run:** 2026-08-16 · instrument = recovered book-comp harness (tag `pre-prune-2026-08-08`,
anchor-verified; see [OPERATIONALIZATION.md](OPERATIONALIZATION.md) incl. the gate-v2
amendment recorded before any policy read) · 10K sims × seeds (11,12,13) × h=520 ·
Mon-anchored week-block bootstrap · EOD clock · risk_pct-layer multipliers on the 2-leg panel.
**Pre-registration:** [frozen 2026-07-24](../../../../docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md), §0–§10 byte-unedited; un-dormed scoring-only 2026-08-16 (P2 mark).
**Verdict:** `FALSIFIED` — schedule lever spent for eval-pass lift (best −1.06pt vs +5pt bar); flat WATCH-1 stands; surviving: cushion-proportional sizing zeroes bust → Q-POLFRONT-1
**Machine row:** `pass_pct_best 73.95 | lift −1.06pt < +5.0 | bust_best 0.00 ≤ 20.18 | halves lift −6.54/+6.01 | FALSIFIED`
**Spend / K:** $0 · K_intrinsic = 3 (the prereg's banked non-control policies) consumed by this read · no Pine / TV / arming.

## Fidelity gates (both passed before any policy read)

| Gate | Expected | Measured | Result |
|---|---|---|---|
| Stage-1 rebuild vs de-scope ADR | ≥$200 winning-day 22.2% | 22.2% | PASS |
| `assert_anchors.py` | p2 mean/mo ≈ 1751, q3 max ≈ 126 | 1751.04 / 126 | PASS |
| v1: port m=1.0 vs recorded 37.78 | 37.78 ±0.005 | 38.17 | **FIRED** → diagnosed |
| v2: port m=1.0 vs recovered ORIGINAL on this env | 38.2 ±0.1 | 38.17 (original prints 38.2±0.2; chain $315 vs recorded $318.20) | PASS |
| Control 0.50× vs original's own sweep row | 75.0 / 20.2 | 75.01 / 20.18 | PASS |

Vintage drift (recorded env → this env: +0.39pp pass at m=1.0, ~−1% chain) is an
environment/panel-rebuild effect, not a port defect; the policy-vs-control comparison is
same-instrument, same-environment throughout.

## Results (full panel)

| Arm | Eval pass % | Lift vs control (pt) | Bust % | Bust Δ (pt) | Median pass (bd) |
|---|---|---|---|---|---|
| (a) flat 0.50× — control | 75.01 | — | 20.18 | — | 197 |
| (b) linear decay 0.75→0.25 (T_b=197bd) | 66.55 | −8.47 | 15.38 | −4.80 | — |
| (c) floor-distance-proportional, cap 0.75× | **73.95** | **−1.06** | **0.00** | **−20.18** | — |
| (d) step-down-at-cushion ($1,500 latch) | 70.50 | −4.52 | 19.63 | −0.55 | — |

**Frozen §6 read:** best-of-3 = (c); lift −1.06pt fails the +5.0pt limb ⇒ `FALSIFIED`
(the bust limb, which (c) passes overwhelmingly, cannot rescue a failed lift limb — the
prereg's H was pass-probability-shaped). Halves (selection on full panel only): H1 lift
−6.54pt / H2 +6.01pt — moot for the verdict, recorded for completeness; (c)'s bust is 0.00%
in **both** halves (control 15.59 / 23.38). Placebo (frozen design): 60 state-destroyed shams,
mean lift −8.84pt, p_placebo = 0.000, max-of-3 p95 = −6.48pt vs winner −1.06pt — the
state-dependence is doing real work; also moot for the FALSIFIED headline.

## Surviving finding (NOT killed by this closure — the prereg falsified a pass-prob H)

**Cushion-proportional sizing eliminated trailing-DD bust on this instrument: 20.18% → 0.00%
(H1 15.59 → 0.00; H2 23.38 → 0.00) at a cost of 1.06pt of pass probability.** Mechanism:
m_t = 0.75·min(1, cushion/3000) makes the largest panel loss-day (−$1,991 at 1.00×) unable to
cross the remaining cushion at any state — sizing decays toward zero as the floor approaches,
and the EOD trail does not ratchet while P&L is near-flat. Three honest bounds on this zero:

1. **EOD clock** — venue enforces intraday; an intraday excursion deeper than the day's close
   can breach where this engine does not (standing lesson: bust figures are lower bounds).
2. **risk_pct abstraction** — integer-contract floors (1 micro) break the asymptotic-zero
   property below ~1-contract sizing; the real-world analogue near the floor is participation
   (stand down), which preserves the effect's direction but not its arithmetic purity.
3. **In-panel tails only** — the block bootstrap cannot draw a loss-day worse than the panel's
   worst; the zero is a statement about panel-supported states.

Route: this is exactly [Q-POLFRONT-1](../../../../docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md)'s
primary axis — reframed by this result from "does a schedule lift pass-prob" to **"how much
base-R headroom does cushion-proportional sizing buy at a fixed bust ceiling"** (N-SURV
admissible-region widening for candidates). Owed brief, not opened here.

## Files

`run_evalseq.py` (policy-capable port; fidelity-gated) · `out/evalseq_results.json` (full
per-seed numbers) · harness recovered working-only (not re-committed; the Great Prune stands).
