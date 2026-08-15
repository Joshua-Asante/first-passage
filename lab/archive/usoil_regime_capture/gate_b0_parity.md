# Gate B-0 — native-parity result (CONCEPT-USOIL-RGC-001 anchor)

**Date:** 2026-06-14 · **Verdict:** **NO-VERDICT (parity not cleared; not PASS, not FALSIFIED)** · **Anti-SNAG slots consumed: 0** (PREREG §10: un-cleared B-0 = NO-VERDICT, concept parks).
**Reproduces:** `gate_b0_parity.py` (Python pre-filter on the on-disk c35c1 panel) vs the operator's native TradingView Strategy-Tester export.
**Pre-reg:** `docs/ltm/briefs/pre-registration/PREREG-USOIL-RGC-GATEB-2026-06-14.md` (r2). **Authority:** Python tier has NO gate authority (sweep ADR 2026-06-05) — these are advisory.

## Native (canonical PEPPERSTONE:SPOTCRUDE, operator export, re-parsed in-session)
n=534 (309 long / 225 short) · Net **+$352.65** · PF **1.0029** · WR 35.02% · gross_win $121,247 ≈ gross_loss $120,894 · maxDD $16,109 (8.05% of $200K) · RF 0.022.

## Python pre-filter on c35c1 (anchor channelLen=384, stopAtr=3.0, trailAtr=3.5)
| exitAtrLength | n_trades | L / S | net | PF | count Δ vs 534 | PF frac-diff | parity |
|---|---|---|---|---|---|---|---|
| 22 (frozen) | 540 | 314/226 | $3,883 | 1.0294 | **+6 (+1.12%)** | 2.65% | ✗ |
| 14 (Pine default) | 532 | 313/219 | $14,776 | 1.1134 | **−2 (−0.37%)** | 11.01% | ✗ |

**Count-exact (the only robust leg) does NOT clear at either exitAtrLength.** The two split: 14 wins raw count (Δ2), 22 wins PF/net-magnitude/side-balance — weight of evidence **leans 22** (the frozen value), but neither resolves it.

## Why this is INDETERMINATE, not FAIL
- **Net-2% band is non-diagnostic at PF≈1:** 2% of native net $352.65 = **$7.05**; net is 0.29% of $121K gross turnover (statistical zero). A few hundred $ of execution-model difference detonates the band by 1000–4000%. The frozen 0.02 band was **not** tuned (forbidden). Reproduces the GBPUSD PF≈1 ill-conditioning lesson (2026-06-06).
- **The ±2/+6 deltas are tiny** and confounded by a **SPAN MISMATCH** (on-disk panel = 2020-01-01 23:00 → 2023-12-29 21:15; native export stated 2020-01-08 → 2024-01-01 — native right-edge ~3d past panel, left-edge ~7d offset) + un-reconciled execution-model micro-differences (entry-fill convention, STOP-FIRST straddle order, UTC-vs-chart-TZ daily-cap bucketing, channel[1] edges). PREREG §6 explicitly anticipates first-pass parity failure for this never-before-native-validated long-short+trailing model.
- **rank-ρ leg entirely un-run** (only the anchor cell exists; the 10-cell sample for ρ≥0.70 was not executed).

## Triangulation — PEPPERSTONE vs FX_USOIL (operator-supplied cross-feed)
1. **EXACT 10× contractValue divergence.** Implied contractValue = (Size(value)/qty)/price is a clean **1.0000** on PEPPERSTONE vs **10.0000** on FX_USOIL (zero variance both). Same shape as the DJ30 default-of-1-was-10×-wrong; **concretizes ledger W5** (USOIL DXTrade contractValue UNVERIFIED).
2. **FX_USOIL carries the negative-WTI corruption** (W1/D3): a $3.427 print @ 2020-04-20, 1 bar <$5. PEPPERSTONE bottoms cleanly at $12.458, 0 bars <$5.
3. **FX_USOIL's +$120,608 is an illusion.** One 2020-03-09 crash trade = +$103,644 ≈ **86% of the entire net** (same trade +$4,147 on PEPPERSTONE — 26× amplification from 10× leverage + corrupt tail). Static-$200K equity swings $549K peak → $255K trough = **147% maxDD** (account destroyed mid-run).
4. **No edge on either feed once sizing is removed** — both ≈ PF 1.0 breakeven on a risk-normalized basis (median per-trade return-on-notional −0.4561% PEPP vs −0.4575% FX). FX's higher headline PF (1.066) is a corruption+leverage artifact (PF rank-inversion: the corrupt feed shows the "better" PF).
5. **Selection mostly agrees:** >82% of entries align within 15min, day-level Jaccard 0.86 → same strategy, different fills + a ~15% genuinely-different-trigger tail from the corrupt bars. **Not a logic bug.**
6. **FX_USOIL is non-canonical / staging-only** (the corruption-bearing family). It corroborates the breakout fires on the same events and is a useful **W5 tripwire exhibit**, but sets/moves **no** B-0 verdict, anchor, or edge claim.

## Edge omen (SEPARATE from B-0; B-0 does not verdict the edge)
The canonical **anchor (grid centre) is dead: PF 1.0029, net +$352, RF 0.022.** A dead centre on a 36-cell grid + oil's random-walk priors (W2/F2: VR≈1, no persistence) is a **strong negative prior** for the full Gate B (B-1…B-6) and *raises* the DSR-at-honest-N / episode-breadth bars. It does **not** formally falsify the grid (edge could live off-centre), but hunting the one surviving off-centre cell after a dead centre is the textbook selection trap the deflation battery exists to punish.

## Recommended next (single best step) — DONE 2026-06-15, see UPDATE below
Operator: (1) confirm `exitAtrLength=22` was the native setting; (2) **re-run the native TV anchor with the date range forced to exactly the c35c1 panel span 2020-01-01 → 2023-12-29** (NOT 2024-01-01) to kill the span-mismatch confound on the only diagnostic leg; (3) export the native "List of Trades" CSV so a **trade-by-trade** reconciliation can attribute the residual ±N delta to a specific cause. Only after count-exact clears (or the residual is explained + bounded) → run the 10-cell rank sample (ρ≥0.70) → then B-1…B-6.

---

## UPDATE 2026-06-15 — trade-by-trade reconciliation (parity_check leg substantively RECONCILED)

Operator **confirmed exitAtrLength=22** and re-ran the native anchor on the panel span → new export `…2026-06-15_79c8c.csv`: **n=533** (309L/224S), net +$756.61, PF 1.0063, maxDD 8.05%, span 2020-01-08 → 2023-12-29 (right edge now panel-aligned; the prior 2024-01-01 trailing trade is gone). Reconciler: `reconcile_b0.py` (TZ-robust greedy match: same side, |Δt|≤30min, |Δprice|≤0.10). **Native is UTC** (532/533 matched at offset 0; ET interpretation matched 1/533 — rejected).

**Result: 532 of 533 native trades reproduce EXACTLY** (bar time + price + side) by the Python pre-filter at exitAtrLength=22. The Python excess (540 vs 533 = +7) is **fully attributed, none is logic divergence**:
- **4× left-edge warmup** (2020-01-01/03/06/07, all before native's first trade 2020-01-08): Python's panel starts 2020-01-01 with no pre-history, so its Donchian (`ta.highest/lowest` available-bars warmup) fires **phantom breakouts on a truncated channel**; native's chart carries full pre-2020 history, so those prices ($61–64) are not breakouts. **Panel-scope artifact, benign.**
- **1× right-edge** (2023-12-29 21:00, the panel's last bar).
- **1× fill-timing near-match** (Python 2020-05-01 ~$21.81 L vs native 2020-04-30 ~$21.23 L, 75 min apart, in the violent COVID-bottom window) — same breakout, just outside the 30-min tolerance; net 0.
- **2× genuine mid-sample extra Python longs** (2021-09-13, 2022-04-13) — position-sequencing cascade downstream of the 4 boundary phantoms (Python's equity/position timeline is shifted, so it is flat for 2 later breakouts native was still in a prior trade for).

**Disposition:** **parity_check leg substantively RECONCILED** — the Python tier replicates native to **99.8%** (532/533 exact). Literal trade-count-EXACT (533≠540) is not met, but the strict gate's *purpose* (detect different LOGIC, not rounding — parity.py docstring) is satisfied: the gap is panel-boundary warmup + 2-trade sequencing, **no logic divergence**. The Python pre-filter has earned rank-ordering authority for the N=36 sweep.

**Reusable finding (L-WARMUP-PHANTOM):** the codifier's Donchian numpy twin (`np_indicators.highest/lowest`, available-bars warmup) produces phantom breakouts when a panel starts mid-history (no pre-channel data) — inflating the left-edge trade count vs a native chart with full history. For literal count-exact, gate breakout entries until the channel is fully warmed (skip the first `channelLen` bars) OR supply a panel with ≥`channelLen` pre-roll bars. Candidate primitives hardening; does not affect the sweep's rank authority (the artifact is constant across grid cells).

**Remaining for full B-0:** the **rank-ρ ≥ 0.70 leg** (10-cell representative sample) is still un-run — parity_check (anchor) is reconciled, but the rank-correlation falsifier is the other B-0 requirement before B-1…B-6. No anti-SNAG slot consumed.

## Advisory N=36 grid preview (2026-06-15, `gate_b_grid_preview.py`) — REVISES the "dead centre" omen
The Python tier is parity-validated, so an **advisory** full-grid run (exitAtrLength=22; NO authority, NO verdict, NO slot) pre-screens whether the edge lives anywhere before the operator-manual rank cert. Result:
- **The anchor (384/3.0/3.5) is the 2nd-WORST of 36 cells (PF 1.0294)** — the "dead centre" was unrepresentative, not the grid.
- **20/36 cells PF>1.10 · 29/36 PF>1.05 · 0/36 losing.** PF dist: min 1.0026 / median **1.124** / max **1.328**. Best cell **576/2.5/3.5 → PF 1.328, net $45.8K, n=441**.
- **Monotonic in channelLen:** 576–960 (≈6–10 trading days) cluster at PF 1.20–1.33; 192–384 at PF 1.00–1.13. The candidate edge lives at the genuinely multi-week lookbacks.

**Caveat (load-bearing):** PF 1.10–1.33 on a no-persistence-prior instrument (W2/F2: VR≈1, Hurst≈0.5) is a **CANDIDATE, not an edge.** The longer-channel→higher-PF gradient is confounded by the cost-law (longer channel → fewer trades → less cost drag; n 192≈900 vs 960≈340) and by fat-tail concentration (2020 COVID / 2022 invasion). Net $ also carries the L-WARMUP-PHANTOM inflation + compounding. Whether this is real regime-capture or selection/cost/fat-tail survivorship is **exactly** the open question the deflation battery (B-3 DSR-at-honest-N=36 with √(2 ln 36)≈2.67 multiplicity penalty; B-4 episode-breadth + drop-top-episode; B-5 COVID/invasion-exclusion) is designed to adjudicate. The grid being structured (not dead) **justifies proceeding** to that battery; it does NOT pre-judge a PASS.
