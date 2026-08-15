# Sovereign (CONCEPT-USDCAD-RDM-001) — F1 verdict

**Date:** 2026-06-12 · **Gate:** [`gate.py`](gate.py) · **Result:** [`gate_result.json`](gate_result.json)
**Brief:** [`CC-HANDOFF-USDCAD-RDM-001-stage1-f1.md`](../../docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-USDCAD-RDM-001-stage1-f1.md)

## VERDICT: **PASS** — §6 return: `DONE_WITH_CONCERNS`

All three §3 pre-registered criteria clear (thresholds verbatim, no mid-run
amendment). Concerns listed below are reporting, not threshold renegotiation.

| §3 criterion | threshold (pre-registered) | observed | state |
|---|---|---|---|
| 1. F1(b) spread loading, 5d primary | perm p ≥ 0.05 or beta < 0 ⇒ FAIL | beta **+0.0338**, r +0.283, **perm p < 0.0005** (0/2000), n=433 | clear |
| 2. F1(a) conditional correlation | corr ≥ 0 ⇒ FAIL | **−0.0167** (830 widening days) | clear |
| 3. F1(c) incremental loading after trend+WTI | perm p ≥ 0.05 or beta < 0 ⇒ FAIL | beta **+0.0333**, **perm p < 0.0005** | clear |

Supporting (non-gating): 10d secondary beta +0.0458 / r +0.358 / perm p < 0.0005;
**1d secondary FIRES** (perm p = 0.0515) — the loading is a multi-day phenomenon,
consistent with the swing/H4+D1 concept shape, reported per §3. Channel
separation: widening windows mean **+0.227%**/5d vs narrowing **−0.148%**/5d,
separation perm p < 0.0005 (REUSED `label_permutation_test`, n_perm=2000).
Episode loading (descriptive): 2018 cycle beta +0.0258 (n=51), 2022 cycle
+0.0329 (n=90), 2026 episode +0.0179 (n=18) — positive in all three
pre-registered episodes; the §4 multi-episode requirement is met, the
hypothesis-generating 2026 window is the *weakest* of the three (no §5-FM#3
selection artifact).

## Inputs and provenance (TV-CSV feed policy, ADR 2026-06-12 / PR #175)

* USDCAD D1 2018-01-01→2026-06-10: operator TV export
  `BAR_EXPORT_v0.1_FX_USDCAD_2026-06-12_ef452.csv` (FX:USDCAD), 2,190 closes
  decoded from the Signal-encoded trade list (0 unparseable).
* WTI control: `BAR_EXPORT_v0.1_TVC_USOIL_2026-06-12_e5806.csv` (TVC:USOIL),
  2,122 closes.
* US 2yr: treasury.gov daily par yield (2,111 rows); CA 2yr: BoC Valet
  BD.CDN.2YR.DQ.YLD (2,125 rows); joint spread days 2,066. Official series,
  not bar feeds.
* Constellation composite: six 2020-01→2026-06 decompound TV exports via
  `decompound.py` stitch + static rebank (trade counts 309/264/149/280 ==
  inventory), 668 active days, zero-filled to 1,661 panel days.
* **Cross-check:** TV USDCAD close vs BoC official FXUSDCAD — the TV daily bar
  labeled *t* closes 17:00 ET on *t+1*; aligned on that convention the series
  agree at mean |diff| 0.122% / p99 0.522% / max 0.906% (n=1,726), consistent
  with the 30-min fixing gap. The labeling convention makes the pre-registered
  ≤ *t−1* as-of join MORE conservative (state prints before the bar opens).
* As-of join drops: spread 3 days (2 no-prior, 1 stale>5d), WTI 1 day; panel
  2,190 → 2,187 complete rows. Counts reported, never silent.

## Concerns (each named, none threshold-bearing)

1. **The diversification leg is weakly evidenced.** §2.3(a) expected
   "materially negative" conditional correlation; observed −0.0167
   (full-window −0.0241, active-days-only −0.0409) is statistically negative
   but economically ≈ 0 — Sovereign is currently evidenced as
   *uncorrelated-with*, not *insurance-against*, the Constellation book. The
   §3.2 binary bar clears; the anti-Constellation *pitch* does not yet. The
   codify→sweep→validate harness optimizes challenge-window pass-rate
   directly, which is the correct instrument to adjudicate whether
   ~zero-correlation at this loading is worth a book slot.
2. **1d secondary fired** (perm p = 0.0515) — no intraday/overnight edge
   claim survives; any codification must stay swing-horizon.
3. **F1(a) coverage is 2020-06→2026-06 only** (composite availability); the
   2018 episode is untested for anti-correlation (it IS tested for loading).
4. **Composite alignment attenuation:** exit-date stamps (EDT) vs TV bar
   labels can misalign ±1 day; with 60% zero-fill days this attenuates |corr|
   toward 0 — direction is conservative for criterion 2's sign test, but it
   means the true magnitude is somewhat above the observed one, unknown by
   how much.
5. **2018 episode lost January** to the 20-day trend warm-up (export starts
   2018-01-01, not the requested 2017-12-01); n=51 windows remain.

## Dedup adjudication record (§10 hook)

Intake gate 2026-06-11: **ADMIT 7/7, dedup CLEAR** (verbatim:
"RESULT: ADMIT (7/7 PASS, 0 WARN for human review)"). The brief-anticipated
NEAR_MATCH vs **Sentinel** USDCHF did **not** fire — no operator adjudication
was required; the mechanism-differentiation argument (rate-expectation-
conditioned vs unconditional price trend) is recorded in the concept YAML's
dedup-neighbors header and was never needed.

## Disposition

PASS → CONCEPT-USDCAD-RDM-001 **earns a codify→sweep→validate pass** (R&D
pipeline stage 2+). No registry append (that is the FAIL path). No strategy
build in this probe (§5 FM#1). Codification, when picked up, must carry
concerns 1 and 2 into its portfolio-fit evaluation.
