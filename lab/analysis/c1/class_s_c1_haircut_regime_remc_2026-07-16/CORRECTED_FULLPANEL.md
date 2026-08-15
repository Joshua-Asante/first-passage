# Corrected-geometry haircut arms — full/half-panel reference (2026-07-24)

**Status:** `MEASURED — closes the c1 GO ADR §6 open B7 input`
**Authorization:** operator chat directive 2026-07-24 ("proceed with the two unmeasured arms").
**Runner:** [`run_corrected_haircut_fullpanel.py`](run_corrected_haircut_fullpanel.py) · report [`corrected_haircut_fullpanel_report.json`](corrected_haircut_fullpanel_report.json)
**Method:** frozen 2026-07-15 regime primitives (`full_panel_reference` / `part_b_half_panel`, Run-2 consistency-on, 10K sims × seeds 42/123/2026) + the 2026-07-22 correction idiom (`dd_lock_offset_usd → 1_000_000.0` on both `trailing_locking` tiers, restored after) + the frozen 2026-07-16 haircut injection (`daily_100k × mult`). **No bootstrap** — the separable long pole per the withdrawal RESULTS §5; this is the recommended pre-B7 close.
**Reproduction control:** corrected 1.00× matched every published pin — full-panel Bulenox 3.51% / Tradeify 4.74% / MFFU 4.25% / BluSky 4.44%; H1 Tradeify 6.78% / MFFU 6.28%. `reproduction_control.ok = true`.

## The number B7 was waiting on

**WATCH-1 0.50× under CORRECTED eval geometry, $100K basis:**

| Tier | Full-panel bust / pass | H1 (2020-23 chop) | H2 (2023-26 trend) | Floor |
|---|---|---|---|---|
| Tradeify_Select_100K | **0.11% / 99.80%** | **0.22%** PASS | 0.04% PASS | **PASS** |
| MFFU_Rapid_100K | **0.11% / 99.81%** | **0.22%** PASS | 0.04% PASS | **PASS** |
| Bulenox_100K | 0.08% / 99.82% | — | — | PASS |
| BluSky_Premium_100K | 0.08% / 99.80% | — | — | PASS |

**vs the defective-geometry §6 figures** (full 0.08% / H1 0.14%): the correction
costs **+0.03pp full-panel and +0.08pp H1** at the deployed rung. The GO ADR's
"known-optimistic by an unmeasured amount" is now measured: at 0.50× the amount
is negligible. The forbidden move (scaling the 1.00× +2.10pp delta down) is
also now empirically vindicated — the barrier interaction is strongly
non-linear (+2.10pp at 1.00× vs +0.03pp at 0.50×).

**Still unmeasured (declared, not implied):** the corrected 0.50×
bootstrap-95th (defective-geometry published 0.77% vs 3.0% ceiling; the
corrected H1 delta of +0.08pp makes a corrected boot-95th anywhere near the
ceiling implausible, but it is not measured here — it remains the separable
long pole and does not gate B7 per the withdrawal ADR's own recommendation).

## Dispositions

1. **The c1 GO ADR §6 open B7 input is CLOSED-BENIGN.** The WATCH-1 0.50× risk
   framing survives corrected geometry essentially intact. This was the
   "recommend closing before B7 arms" item — done, pre-arm.
2. At the deployed rung the corrected regime halves **both PASS** on both
   discharge tiers — consistent with the Q-BUSTGATE-1/fork-B record (regime
   gate PASSES 0.50×) now re-confirmed under corrected geometry.
3. The 1.00× arm remains FAIL everywhere (4.74%/4.25%/3.51%/4.44%) — nothing
   here re-opens the §4 withdrawal; the (separate, pre-registered) 50K band
   re-score is where corrected-geometry clearers were found
   ([`c1_band_rescore_2026-07-24/RESULTS.md`](../c1_band_rescore_2026-07-24/RESULTS.md)).

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-24 | Measured corrected 1.00×/0.50× full+half panels; reproduction controls all MATCH; §6 open B7 input closed benign | Joshua (directive) + Claude Code (Fable 5) |
