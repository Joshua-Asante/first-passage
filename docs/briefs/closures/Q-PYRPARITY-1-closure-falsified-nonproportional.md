# Q-PYRPARITY-1 — CLOSURE: `FALSIFIED-NONPROPORTIONAL`

**Closed:** 2026-07-17
**Parent Pre-Q:** [`Q-PYRPARITY-1-watch1-pyramid-proportionality.md`](../Q-PYRPARITY-1-watch1-pyramid-proportionality.md) (now `CLOSED — FALSIFIED-NONPROPORTIONAL`)
**Pre-reg (FROZEN 2026-07-17, operator-ratified):** [`Q-PYRPARITY-1-verdict-preregistration.md`](../pre-registration/Q-PYRPARITY-1-verdict-preregistration.md)
**Phase 0:** [`lab/archive/q_pyrparity_1_2026-07/PHASE0.md`](../../../lab/archive/q_pyrparity_1_2026-07/PHASE0.md) — Branch B; structural proportionality CONFIRMED-IN-SOURCE (corroborating)
**Phase 2:** [`lab/archive/q_pyrparity_1_2026-07/RESULTS.md`](../../../lab/archive/q_pyrparity_1_2026-07/RESULTS.md) — Branch B harness + four cohort tables
**No criterion moved after data** (Trap #12 clean).

## Verdict (§6 asserted)

**`FALSIFIED-NONPROPORTIONAL`** — MYM base and add cohort medians (Branch B) sit at **0.8707** / **0.9164** against the frozen accept band 0.500 ± 0.005 (and outside the reject band 0.500 ± 0.02). MNQ alone would have been `AMBIGUOUS-HOLD` (list misalignment + base fill-frac); overall is dominated by MYM.

| Leg × cohort | paired n | Branch B median | frac in ±0.02 | §4 |
|---|---:|---:|---:|---|
| MYM base | 232 | **0.8707** | 0.082 | FAIL |
| MYM add | 35 | **0.9164** | 0.086 | FAIL |
| MNQ base | 228 | 0.4888 | 0.715 | fill-frac FAIL; median PASS |
| MNQ add | 47 | 0.4990 | 1.000 | PASS |

## Mechanism

Pine is linear in `riskPerTrade` (Phase 0). The falsifier is a **TV/symbol qty ceiling on MYM1! @ $200K**: base clips at **17**, add at **127** (= 17 × 7.5 floored). Below the ceiling, H-PYRPARITY-1 holds (MYM base n=22 below-cap median **0.502**; add n=5 below-cap median **0.496**). At the ceiling, halving risk cannot halve size — realized ratios collapse toward 1.0. MNQ has no analogous ceiling in-range; its add cohort is textbook-proportional; extra fills at half risk are consistent with dollar-fixed day-stop/halt gates binding less often (effective signal-path touch → AMBIGUOUS on that leg alone).

## Dispositions

- **`strategy_lifecycle.md:113`:** OPEN → **CONFIRMED-FALLBACK (2026-07-17)** — WATCH-1 haircut for the two pyramided legs is applied at the **account-multiplier layer**, not via TV risk%-input scaling.
- **Q-RAIL-1 F1:** **PASS-via-fallback** (2026-07-17). F1 no longer blocks on this brief; remaining F2–F5 + Phases 0–4 still open on Q-RAIL-1.
- **Multiplier-spine forward-relevance flag (STATE 08-08):** affirmed **in the affirmative** — the account-multiplier layer is load-bearing for c1 WATCH-1 realization on MYM/MNQ.
- **c1 / locked book:** no Pine edit; no `BASE_RISK` / lifecycle-constant change. The haircut re-MC's book-level ×0.5 remains the evidence; execution realizes it via lot-multiplier, not risk input.
- **K-accounting:** TV observation + mechanical verify — no discovery search; no K banked.

## Lesson candidate

Source-linear Pine + TV symbol ceiling = “proportional in code, non-proportional in fills.” The §0 OPEN item’s exact risk. Uncapped-slice evidence shows the *input* path is fine; the *runtime ceiling* is the falsifier. Sibling of the Phase-0 note that integer-contract rounding on CME charts is invisible in source.

## Audit hooks

```bash
grep -n "CONFIRMED-FALLBACK\|OPEN — Pine pyramid-parity" docs/methodology/strategy_lifecycle.md
grep -n "PASS-via-fallback\|F1" docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md
grep -n "Multiplier-spine\|Q-PYRPARITY-1" STATE.md
python lab/archive/q_pyrparity_1_2026-07/verify_phase2.py
```
