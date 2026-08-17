# Candidate rows — radar Tier-A burst 2026-07-16

**Status:** **`H-TSMOM-6J` CLOSED Clause-N FAIL** (Default #1 pinned 2026-07-16). Carry stubs: Table-1 moments recovered; **timing Req-2 still UNSCREENABLE**. Month-end Tier B: no new brief (Q-HARV-1 §R already DECLINED) — see [`MONTH_END_ITEM3_DISPOSITION.md`](MONTH_END_ITEM3_DISPOSITION.md). **2026-08-16 addendum: `H-TSMOM-6A` CLOSED Clause-N FAIL; `H-COTREV-6A` UNSCREENABLE (Req 2)** — both sourced as part of the S3 WHO-drought-relief thread, targeting M6A (the one non-index micro with zero prior Tier-A work); both die pre-manifest.  
**Screen:** do **not** append `floor_scan` for any of these rows.  
**K banks re-read 2026-08-16:** ES=2 (H-OD only; H-TSMOM-1 never opened) · MNQ=1 · GC/MGC=3177 · 6J=0 · 6E=0 · 6A=0 · CL-family=0.

---

## H-TSMOM-6J — 12m/1m TSMOM confirm on JPY (6J) — **CLOSED — Clause-N FAIL**

| Field | Declaration |
|---|---|
| **Axis short name** | `H-TSMOM-6J` Moskowitz 12m/1m TSMOM confirm (JPY / 6J) |
| **Path 1a/1b** | **1b** — same evidence-robustness spine as H-TSMOM-1 (Phase-2 scored PASS); instrument change does not re-open Path 1b; Req-2 δ is JPY-native (below). |
| **Source + tier** | Moskowitz, Ooi & Pedersen 2012 *JFE* Fig.2 bar 12 + Hurst, Ooi & Pedersen 2013 *JOIM* Fig.2 labeled USD-JPY (label authority). **Tier 1.** Digitize: [`FIG2_DIGITIZATION.md`](FIG2_DIGITIZATION.md); recovery: [`CHEAP_RECOVERY_JPY.md`](CHEAP_RECOVERY_JPY.md). |
| **Instrument family → K_banked** | **6J → K_banked=0** (unchanged — never opened). Distinct from ES `H-TSMOM-1`. |
| **Design → K_intrinsic** | Frozen 12m lookback / 1m hold sign rule (vol-scaled). **K_intrinsic = 1**. |
| **OOS era → N** | **PINNED (c) Default #1** — statistical OOS 2019-05-06→present, **N≈86**. Disposition: [`H_TSMOM_6J_N_PIN.md`](H_TSMOM_6J_N_PIN.md). |
| **δ/σ (cohort-cited)** | **0.1415** from conservative central SR **0.49** (Moskowitz Fig.2 USD-JPY under Demystifying L→R map). `δ/σ = SR/√12`. Tolerance ±0.03 SR. |
| **Req-5 cost sniff** | **PASS (provisional)** — moot under Clause-N FAIL (campaign never reaches Stage-0). |
| **Dedup** | Not H-TSMOM-1 (different family). Not D7 (month-end). |
| **Clause K (informational)** | K_eff = 1 → floor **0.65** → **PASS(K)** — moot. |
| **Clause N** | power@N=86 ≈ **0.26** → **FAIL** (threshold 0.50; break-even N≈192). Demystifying SR 0.54 → power≈0.30 still FAIL. |
| **Disposition** | **CLOSED — Clause-N FAIL.** No Stage-0 / no pull / no K. Re-open only with N-extending evidence or stated §8 override. |

---

## H-CARRY-FX-1 — Currency carry (Koijen) → 6J/6E expression

| Field | Declaration |
|---|---|
| **Axis short name** | `H-CARRY-FX-1` Koijen currency carry confirm |
| **Path 1a/1b** | **1a** — high-interest currencies earn a risk premium paid by funding-currency borrowers / UIP failure; losers = constrained funding providers in crashes (Brunnermeier-class). |
| **Source + tier** | Koijen, Moskowitz, Pedersen & Vrugt, *Carry*, *JFE* 2018 Table 2 (currency carry1m SR **0.68**); Table 6 timing vs mean SR **0.53**. **Tier 1.** Table 1 moments: [`CARRY_DELTA_EXTRACTION.md`](CARRY_DELTA_EXTRACTION.md). |
| **Instrument family → K_banked** | Prefer **6J or 6E → K_banked=0**. Cross-sectional multi-currency book is a *different* design (not staged as K_intrinsic≤3 single-leg here). |
| **Design → K_intrinsic** | Intended confirm: time-series carry timing on one CME FX future (sign of own carry vs 0 or own history). **K_intrinsic = 1** once timing δ exists. |
| **OOS era → N** | Monthly; Default #1 N≈86 binds any future screen (H-TSMOM-6J precedent). |
| **δ/σ (cohort-cited)** | **`UNSCREENABLE:carry-timing-delta-not-published-per-instrument`**. Table 1 Japan/Euro **unconditional** moments recovered (Japan uncond monthly δ/σ=0.043 — **not** the timing design; do not plug). Class timing SR 0.53 remains an inadmissible transplant. |
| **Req-5 cost sniff** | **PASS (class-level)** — monthly carry moves dominate FX futures RT at SR~0.5–0.7; re-check per instrument at Stage-0 if ever screened. |
| **Dedup** | Distinct from TSMOM; Table 8 shows currency carry α survives TSMOM controls. |
| **Proposed posture** | Recovery path: named per-contract predictive δ (appendix/replication/AQR library) **or** δ-extraction probe Pre-Q **or** drop. |

---

## H-CARRY-CM-1 — Commodity carry / basis (Koijen) → CL expression

| Field | Declaration |
|---|---|
| **Axis short name** | `H-CARRY-CM-1` commodity basis/carry confirm (CL) |
| **Path 1a/1b** | **1a** — convenience yield / theory of storage; hedgers pay premium; carry ≡ basis in Koijen §2.3. |
| **Source + tier** | Koijen et al. 2018 Table 2 commodities carry SR **0.60** (= basis). **Tier 1.** Table 1 WTI moments: [`CARRY_DELTA_EXTRACTION.md`](CARRY_DELTA_EXTRACTION.md). |
| **Instrument family → K_banked** | **CL (WTI) → K_banked=0**. **Not GC/MGC** (FAIL-K bank 3,177). |
| **Design → K_intrinsic** | Sign of own front-curve basis/carry, monthly. **K_intrinsic = 1**. |
| **OOS era → N** | Monthly; Default #1 N≈86 binds. |
| **δ/σ (cohort-cited)** | **`UNSCREENABLE:carry-timing-delta-not-published-per-instrument`**. Table 1 WTI uncond monthly δ/σ=0.100 recovered — **not** timing δ; do not plug. Class timing SR 0.75 inadmissible transplant. |
| **Req-5 cost sniff** | **PASS (class-level)** at SR~0.6 monthly; Stage-0 must use CL panel-era median + commissions. |
| **Dedup** | Not GC. Not DISC-CAMP-0. |
| **Proposed posture** | Same three recovery paths as FX; prefer WTI/CL over Brent for CME. |

---

## H-TSMOM-6A — 12m/1m TSMOM confirm on AUD (6A/M6A) — **CLOSED — Clause-N FAIL** (2026-08-16)

| Field | Declaration |
|---|---|
| **Axis short name** | `H-TSMOM-6A` Moskowitz 12m/1m TSMOM confirm (AUD / 6A family, venue-legal edition M6A) |
| **Path 1a/1b** | **1b — spine inherited from H-TSMOM-1's Phase-2 scored PASS (standing record, unmodified here).** ⚠ **Open question flagged, NOT scored:** this session's single-pass literature read surfaced the Mar–May 2009 TSMOM crash/V-reversal + ~4yr post-crisis Sharpe degradation as a candidate 1b(iv) "known sign-reversal condition" concern. Re-scoring the class 1b spine would touch every TSMOM sibling and is an operator-ratified act — not executed on one agent's web read. Standing PASS governs until then; moot for this row's disposition (dies on Clause N regardless). |
| **Source + tier** | Moskowitz, Ooi & Pedersen 2012 *JFE* Fig.2 (currency-futures sleeve); Hurst, Ooi & Pedersen 2017 "A Century of Evidence" (AQR) for 1b(i)/(ii). **Tier 1.** No primary-source AUD-specific Sharpe was extractable this session (source PDFs returned unparseable encoded streams) — used a secondary summary reporting individual-instrument Sharpes clustered ~0.3–0.5 vs ~1.0 diversified-portfolio Sharpe; conservative-central reading takes the low end, **SR ≈ 0.3**, since no source suggests AUD sits above the currency-sleeve median. **Weaker sourcing grade than H-TSMOM-6J's direct Fig.2 digitization — flag before reuse.** |
| **Instrument family → K_banked** | **6A/M6A → K_banked=0** (never opened). Distinct from ES `H-TSMOM-1`, 6J `H-TSMOM-6J`. |
| **Design → K_intrinsic** | Same frozen 12m lookback / 1m hold sign rule (vol-scaled) as the two prior siblings. **K_intrinsic = 1**. |
| **OOS era → N** | Same Default #1 pin as H-TSMOM-1/6J (temporal-not-instrument OOS, campaign-defaults ADR 2026-07-11): **N≈86**. No new instrument-specific reason to deviate. |
| **δ/σ (cohort-cited)** | **0.0866** from conservative-central SR **0.3** (`δ/σ = SR/√12`). Upper-bound sensitivity at SR 0.5 → δ/σ 0.144. |
| **Clause N (power)** | At SR 0.3: power = Φ(√86×0.0866 − 1.96) = Φ(−1.15) ≈ **0.13 — FAIL**. At upper-bound SR 0.5: Φ(√86×0.144−1.96) = Φ(−0.62) ≈ **0.27 — still FAIL**. **Robustness to the sourcing weakness (load-bearing):** power ≥ 0.50 at N=86 requires δ/σ ≥ 1.96/√86 = 0.211 → **break-even SR ≈ 0.73** — 1.4× the best *digitized* currency-sleeve reading in this burst (6J at 0.49–0.54) and above the entire published individual-currency range. So the FAIL holds for **any defensible SR reading**, not just the secondary-summary 0.3 point estimate. Break-even N ≈ 250–450 depending on SR, i.e. materially longer than Default #1 permits. |
| **Higher-frequency rescue — checked and rejected.** | Weekly/daily TSMOM variants exist in the literature but are reported weaker, not stronger, at higher frequency (Quantpedia). Mechanically, under MOP's own vol-scaling, power ≈ Φ(√T_years·SR_ann − 1.96) is roughly frequency-invariant — a shorter lookback multiplies N but shrinks per-observation δ/σ by a matching √N factor, canceling the gain. No source found breaks that cancellation for AUD. This is a near-certain repeat of the ES/6J failure shape, not a hopeful reframe. |
| **Req-5 cost sniff** | M6A notional ≈ $6,500 (10,000 AUD × ~0.65 AUD/USD, **not** the $60–70K standard-6A notional). Tick ≈$1 ≈1.5bp; estimated RT (spread + commission) ≈ **4–8bp**. Monthly δ ≈ SR_month(0.087)×AUD monthly vol(~260bp) ≈ 20–25bp/event vs 4×-cost bar 16–32bp — **borderline, does not comfortably clear**, moot under Clause-N FAIL regardless. |
| **Dedup** | Not H-TSMOM-1 (ES) or H-TSMOM-6J (JPY) — different family. Both prior siblings independently confirm the Default #1/N≈86 monthly-TSMOM shape kills on power; this is now three-for-three. |
| **Pin inheritance** | Default #1 (c) applied by **standing class precedent** — [`H_TSMOM_6J_N_PIN.md`](H_TSMOM_6J_N_PIN.md): "H-TSMOM-1 operator pin (c) is the standing class precedent for monthly TSMOM confirms." Mechanical third-sibling application; operator veto in review reverses it at $0. |
| **Disposition** | **CLOSED — Clause-N FAIL.** No Stage-0 / no `register_search` / no pull / no K. FAIL is robust across the defensible SR range (break-even 0.73, above the published currency sleeve) — a primary-source digitization upgrade would sharpen the record but cannot plausibly flip the verdict. Re-open only with N-extending evidence or a §8 Default-#1 override with stated reason. |

---

## H-COTREV-6A — CFTC-COT positioning-extreme reversal on AUD — **UNSCREENABLE (Req 2)** (2026-08-16)

| Field | Declaration |
|---|---|
| **Axis short name** | `H-COTREV-6A` positioning-extreme reversal, AUD futures/crosses, sourced via CFTC COT/TFF |
| **Path 1a/1b** | Nominally 1a-shaped (constrained positioning unwind) or 1b-shaped depending on framing — moot, dies at Requirement 2 before the 1a/1b choice matters. |
| **Source + tier** | Wang, *Applied Financial Economics* 13(12) 2003 and *J. Banking & Finance* 28(5) 2004; Klitgaard & Weir (FRBNY 2004, six currencies incl. AUD, 1993–2003 weekly). **Tier 1**, but load-bearing caveat below. |
| **⚠ Sign-direction contradiction (flagged from a single-pass literature read — verify against the primary texts before any load-bearing use).** | Wang's reported result: large-**speculator** sentiment predicts **continuation**; it is large-**hedger** sentiment that predicts reversal. The commonly-practiced "extreme non-commercial/leveraged-fund positioning → mean-reversion" framing this candidate assumed runs **opposite** to that reading. Klitgaard & Weir separately document *contemporaneous continuation*, not reversal. Carried as a caution for any future COT-based candidate on any instrument — unverified beyond abstracts this session; the disposition below does not rest on it. |
| **δ/σ (cohort-cited)** | **`UNSCREENABLE:no-citable-AUD-reversal-delta`** — no rigorous, backtested AUD-specific (or defensible FX-cohort) effect size found for a reversal specification; only qualitative practitioner z-score sources (no backtest), which this repo's doctrine does not admit as a citation. |
| **OOS era → N / event frequency** | COT/TFF is weekly-published — already flagged in this repo's own prior burst as "power-marginal at weekly event frequency." Moot here since Req 2 fails before N/power can be computed. |
| **1b(i) decades** | Legacy COT (non-commercial/commercial) runs to 1986 (~40yr, nominally clears); the TFF leveraged-funds/asset-managers breakout most COT-reversal work actually uses only starts **September 2009** (~17yr) — **fails** (i) if that finer breakout is the one the mechanism needs. |
| **Req-5 cost sniff** | Not reached — Req 2 UNSCREENABLE blocks arithmetic. |
| **Dedup** | Not H-CARRY-FX-1/H-CARRY-CM-1 (different mechanism class — carry vs positioning). |
| **Disposition** | **UNSCREENABLE (Requirement 2)** — no manifest, no K, no Q-ID. Recovery path (per `strategy_harvest.md` §1 relief valve): a δ-extraction probe building the reversal-vs-continuation regression directly from public CFTC data **using the correct (hedger-sentiment, not speculator-extreme) specification** — a genuinely different construct from the one usually assumed, not a parameter retune. |

---

## Exclusions logged (not rows)

| ID | Reason |
|---|---|
| `H-TSMOM-GC` | Req 3 FAIL-K (GC/MGC bank 3,177) even if Fig.2 Gold SR is large |
| Hurst–Ooi–Pedersen 2017 | Path-1b support for existing TSMOM class — not a new 4-tuple |
| Basu–Miffre hedging-pressure XS | Cross-sectional commodity sort; no single-leg δ |
| Tier-C intraday / OD siblings | Graveyard-watch; D5 + H-OD-1 closed |
| Month-end ES successor brief | **Declined** — Q-HARV-1 §R FAIL; see [`MONTH_END_ITEM3_DISPOSITION.md`](MONTH_END_ITEM3_DISPOSITION.md) |

---

## Burst + recovery discharge (updated 2026-07-16 proceed 1–3)

| Metric | Value |
|---|---|
| Req-2 clears this burst | **1** (`H-TSMOM-6J`) — then **CLOSED Clause-N FAIL** under Default #1 |
| Carry Table-1 moments | **Recovered** (Japan / Euro / WTI) — timing Req-2 still UNSCREENABLE |
| Pulls / K | **0 / 0** |
| Default-#1 note | N≈86 kills monthly TSMOM at this δ; same fork as H-TSMOM-1 |

## 2026-08-16 addendum — M6A sourcing pass (S3 WHO-drought-relief thread)

| Metric | Value |
|---|---|
| Candidates sourced this pass | 2 (`H-TSMOM-6A`, `H-COTREV-6A`) — both against M6A, the one non-index micro with zero prior Tier-A history |
| Disposition | Both die pre-manifest: `H-TSMOM-6A` CLOSED Clause-N FAIL (power 0.13–0.27, robust — break-even SR 0.73 exceeds the published currency sleeve; now 3/3 monthly-TSMOM siblings dead on power) with a 1b(iv) concern flagged as an **open question only** (standing Phase-2 1b PASS unmodified); `H-COTREV-6A` UNSCREENABLE Req 2, with a sign-direction caution (single-pass read, unverified) carried for future COT-based candidates |
| Pulls / K | 0 / 0 |
| Reading for the WHO-drought thread | M6A being "virgin" (no prior attempt) is not the same as M6A being productive — the two most obvious Tier-A doors here were both dead on arrival by the repo's own pre-screen arithmetic, before any data pull. Recorded so a future session doesn't re-spend a sourcing pass re-deriving the same two dead ends. |
