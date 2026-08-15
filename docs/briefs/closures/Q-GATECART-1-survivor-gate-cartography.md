# Closure — Q-GATECART-1 survivor-gate cartography

**Brief:** [`docs/briefs/Q-GATECART-1-survivor-gate-cartography.md`](../Q-GATECART-1-survivor-gate-cartography.md)
**Pre-registration (frozen formula):** [`docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md`](../pre-registration/Q-GATECART-1-verdict-preregistration.md) (freeze commit `453148a`)
**Closed:** 2026-07-14 — at **Phase 0.5**, ahead of the cartography grid (the grid was never run; the realism-band anchors settled it).

---

## Verdict (exactly one)

**FALSIFIED — at the banked K = 3,177** (verdict is K-conditional; see §K-scope).

The realistic-and-demonstrable band **[S_floor, Cap] is empty**: the DSR demonstrability floor sits *above* the plausible-edge ceiling under every admissible Cap. H-CART's "otherwise" branch fired — the survivor-gate feasible region is empty for realistic candidates at the banked K — and it was reached by the realism-band anchors (A+B+C), so the Phase-1 grid became unnecessary (moot at this K).

## The numbers (frozen formula, §B byte-stable since the freeze)

| Anchor | Meaning | Value |
|---|---|---|
| **S_A** | best single edge the programme has validated (max of 4 locked legs; Pepperstone panel, gross/friendlier-venue upper bound) | **1.83** (Aegis; Guardian 1.48, NAS100 1.45, DJ30 1.11) |
| **S_B** | published top-decile net single-strategy annualized Sharpe (corrected literature; live-realized CTA weighted) | **0.85** (range 0.6–1.05; median single-strategy ~0.3–0.5) |
| **S_floor** | DSR demonstrability floor: min annualized Sharpe clearing DSR ≥ 0.95 at K=3,177, V=1/n | **2.05** (robust across trade-frequency — set by K, not n) |

**Divergence branch fired** (|S_A − S_B| = 0.98 > 0.5): S_A ≈ 2× S_B, the direction §B anticipated (S_A is gross/friendlier-venue, S_B net/corrected; the ~2× ratio is the expected haircut, confirming S_A as an upper bound). Per the frozen rule the Cap is operator-adjudicated, **but the verdict is invariant** — every admissible Cap ∈ [1.0, 2.0] is below S_floor 2.05, so the band is empty however the Cap resolves.

## Which trigger fired

H-CART "otherwise" — there are **zero realism-band-compliant grid points** (the band itself is empty), so vacuously zero clear. This is a **band-vacuity** finding, not a grid failure: the survivor bust/pass geometry was never the binding constraint.

## The operative finding (dominates the verdict) → M-19

The binding reachability constraint is the **DSR selection floor, not the survivor bust/pass gate**, and it is **governed by K, not sample size** (the floor barely moved across trade-frequency 0.5–4/day). K-sweep from the production `deflated_sharpe`:

| target floor | quality benchmark | requires |
|---|---|---|
| ≤ 1.83 | Aegis (best in-house) | K ≤ 441 |
| ≤ 1.48 | Guardian | K ≤ 33 |
| ≤ 1.00 | typical corrected anomaly | K ≤ 3 |
| = 2.05 | — | K = 3,177 (DISC-CAMP-0 blind matrix-profile) |

At the banked blind-mining K, a candidate must be *better than Aegis* just to clear DSR admission — while the corrected literature puts a realistic top-decile single strategy at *half* that. Blind, high-K mining is structurally dead at the DSR gate regardless of the downstream survivor geometry. Captured as methodology lesson **M-19**.

## K-scope (why the verdict is conditional, and the escape hatch)

FALSIFIED holds **at K = 3,177** (the blind matrix-profile regime DISC-CAMP-0 established). At **K ≤ 441 the band re-opens** (floor drops to/below S_A). The lever is search size: only **low-K, mechanism-first** axes — a handful of pre-committed hypotheses (the HARV lane, [`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md)) — bring the DSR floor below plausible edge quality. Wide feature mining cannot.

**Consequence for the 08-08 axis-selection work:** weight *intrinsic K* first. A genuinely-new axis worth funding toward the 11-08 prop-portfolio falsifier must be expressible as a few pre-committed mechanisms, not wide mining. The "K-budget as an a-priori axis-selection gate" question is a **new fork** (registered on the STATE forward board), not part of this brief.

## Deployability annotation

N/A — no candidate was scored. This is a program-level *reachability* finding, upstream of any deployment fork.

## Lesson candidates

- **M-19** — the DSR floor (not the bust/pass gate) is a discovery axis's binding reachability constraint, and it is K-governed; screen it against the best in-house edge + corrected literature before committing an axis. Dated anchor: 2026-07-14, Q-GATECART-1; quantified counterfactual: floor 2.05 vs best-validated 1.83 at K=3,177.
- Methodological win recorded: freezing the realism ceiling as a *formula over external data* before measuring surfaced the floor > ceiling inversion that the initial felt cap (SR ≤ 2.0) would have masked (2.0 sat exactly between S_A and S_floor).

## Forbidden moves carried out of closure (H-CART §5)

- Do **not** amend the frozen survivor-scoring ceilings (3.0% / 50% / 1.0%) in response to this — that gate's only amendment route is its own close-and-reopen.
- Do **not** read the empty band as license to touch the survivor gate or the DSR K/V rule — the finding is an operator-level reachability fact, not a parameter change.

## Reproduction

```bash
# Anchors A + C (post-freeze); N_eff self-test gates the panel load before Sharpe is trusted.
PYTHONPATH=lab python .claude/skills/strategy-validation/scripts/breadth.py --self-test   # PASS 3.98/3.09
# S_A per-leg + S_floor scan reproduce from breadth.load_baseline_panel + research_utils.deflated_sharpe
# (method frozen in the pre-registration §B; freeze commit 453148a).
git diff 453148a -- docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md   # §B unchanged; only §F annex filled
```
