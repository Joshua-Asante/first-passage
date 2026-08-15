# Candidate rows — radar Tier-A burst 2026-07-16

**Status:** **`H-TSMOM-6J` CLOSED Clause-N FAIL** (Default #1 pinned 2026-07-16). Carry stubs: Table-1 moments recovered; **timing Req-2 still UNSCREENABLE**. Month-end Tier B: no new brief (Q-HARV-1 §R already DECLINED) — see [`MONTH_END_ITEM3_DISPOSITION.md`](MONTH_END_ITEM3_DISPOSITION.md).  
**Screen:** do **not** append `floor_scan` for any of these rows.  
**K banks re-read 2026-07-16:** ES=2 (H-OD only; H-TSMOM-1 never opened) · MNQ=1 · GC/MGC=3177 · 6J=0 · 6E=0 · CL-family=0.

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
