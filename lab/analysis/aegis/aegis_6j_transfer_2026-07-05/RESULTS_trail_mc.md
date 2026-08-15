**Theme:** aegis
**Status:** ACTIVE — Bulenox Option-2 trail-survival MC sequence (Aegis→6J v0.3)
# RESULTS — Bulenox Option-2 trail-survival MC (Aegis→6J v0.3 sequence)

**Date:** 2026-07-05 · **Script:** [`trail_survival_mc.py`](trail_survival_mc.py) (seed 20260705) · **Parent:** `CC-HANDOFF-AEGIS-6J-2026-07-05` §2.5
**Input:** v0.3 deep-panel trade sequence (n=129 intraday trade-days, cap-12 dollar P&L, sha256 `c3b34162…` per `NOTES.md`)
**Account basis:** $100K Option-2 **site-example figures** — $3,000 EOD trailing / $2,200 DLL / cap 12 / floor freeze at start+$100 / eval target 6% = $6,000 (`firm_rules.py` `Bulenox_100K` `profit_target_pct`). **PROVISIONAL** — operator confirmed this basis 2026-07-05 pending account purchase; re-run on confirmation. NB `firm_rules.py` currently encodes **Option 1** tiers only; this sim implements Option-2 semantics standalone (the R1 track owes the engine-level fixed-$ trail).
**Scope guard:** this is fxify-challenge-layer *input*. The sizing-ramp decision (full vs 0.5×-until-freeze) is Joshua's, OODA-layer — explicitly NOT decided here (handoff §1).

## Deterministic anchors — GATE PASSED (pre-registered reproduction before any stochastic run)

| Anchor | Expected (parent session) | Reproduced |
|---|---|---|
| Full size, Jan-2022 start | breach **2022-11-23**, EOD equity **$97,326** vs floor **$97,441** | ✓ exact: $97,326.25 vs $97,440.90. Margin $114.65 — parent §3 prose said "by $135"; the equity/floor pins match to the dollar, the prose margin was off by ~$20. Flagged, not load-bearing. |
| 0.5× until freeze, same path | clears "by ≈$1.4K" | ✓ no breach. Margin at the full-size breach date = $1,442.67 (matches "≈$1.4K"); global path min headroom $842.70 (tighter point sits elsewhere). Eval passes 2023-09-11. Post-freeze min equity $100,942.70 — never below start; structural bound once frozen: account cannot finish below start+$100, max watermark→floor giveback $3,000. |

**DLL applicability:** never binds at cap-12 — worst realized day −$1,747.35, worst intraday adverse excursion −$1,733.05, both < $2,200. Reported, not simulated as a stop.

## Stochastic results

Methods stated per handoff: (A) **start-date rotation** — all 129 circular rotations, exhaustive, preserves full serial structure; (B) **circular block bootstrap on trades** — L ∈ {6, 13, 26} (~2.5 / 5.5 / 11 months at 29 trades/yr), 10,000 paths each, path length 129.

### Arm (a) — full cap-12

| Method | P(breach before freeze) | P(breach ever) | P(eval pass) |
|---|---:|---:|---:|
| Rotation ×129 | 10.85% | 11.63% | 88.37% |
| Bootstrap L=6 | 17.15% | 22.34% | 78.37% |
| Bootstrap L=13 | 10.60% | 12.00% | 88.06% |
| Bootstrap L=26 | 10.74% | 12.02% | 88.09% |
| Rotation, NO freeze (sens.) | — | 100.00% | 87.60% |

### Arm (b) — 0.5× until floor-freeze, then full

| Method | P(breach before freeze) | P(breach ever) | P(eval pass) |
|---|---:|---:|---:|
| Rotation ×129 | 0.00% | 4.65% | 95.35% |
| Bootstrap L=6 | 4.49% | 12.82% | 87.86% |
| Bootstrap L=13 | 0.55% | 7.82% | 92.37% |
| Bootstrap L=26 | 0.41% | 7.62% | 92.42% |
| Rotation, NO freeze (sens.) | 0.00% | 0.00% | 100.00% |

## Reads (pre-stated frame: measurement, no decision)

1. **The half-size ramp buys real tail protection.** Breach-ever drops ~11.6% → ~4.7% (rotation) / ~12% → ~7.8% (L=13); breach-before-freeze effectively vanishes (10.9% → 0–0.6%). Cost: slower pass (the anchor path passes 2023-09-11 at half size vs earlier at full).
2. **Block-length sensitivity is real and one-sided (CONCERN, per §6):** L=6 runs ~6–7pp hotter on breach than L=13/L=26, which agree with the exhaustive rotation. Short blocks break the panel's serial structure and re-cluster losses more often than the observed sequence does. Rotation + L≥13 are the trusted rows; L=6 is the pessimistic bound, not the headline.
3. **The freeze is load-bearing for survival, not for passing.** Without the ratchet-stop (qualification-account semantics per the Pine tooltip), a $3K trail over a 4.5-year full-size path breaches with certainty — but eval pass barely moves (88.4% → 87.6%) because passing races breaching and usually wins. Practical read: the trail's threat window is early, before +$3.1K watermark; after freeze the account is structurally safe (floor = start+$100).
4. **2022-H1 chop is the bust driver** (the deterministic breach is the 2022-01→11 stretch), consistent with the decompound-re-MC regime split — the 6J transfer does not escape the chop-regime tail.

## Caveats

- Trade-day granularity, EOD trail check only; intraday equity between watermark updates is not modeled (bounded by the AE check above — max AE $1,733 at cap-12).
- Dollar P&L embeds TV `strategy.equity` compounding, but sizing is cap-bound at 12 contracts on most trades, so compounding leakage is small; static-$100K re-scale not applied (consistent with the parent-session sim this reproduces).
- Sequence is the single observed 4.5-yr panel; bootstrap paths re-use its marginal distribution (no regime enrichment). The EOD-OFF counterfactual (`RUNSPEC_EOD_OFF.md`) will bound how conservative the ON-panel sequence is.
