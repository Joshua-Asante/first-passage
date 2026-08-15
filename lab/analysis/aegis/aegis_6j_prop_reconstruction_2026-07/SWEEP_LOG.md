# SWEEP_LOG — Aegis→6J Wave-1 (c01–c12)

**Pre-reg:** [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md`](../../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md) (`FROZEN` §9 2026-07-16 / JA)  
**Closed:** 2026-07-16 — Stage-1 **FALSIFIED** (operator accepted)  
**Windows:** selection **2022-01-12 → 2024-12-31**; holdout **2025-01-01 → 2026-06-30**  
**Fill semantics:** Stage-0 (`≤ deadline` PASS; exits at deadline OK)  
**Pins:** [`WAVE1_SHA256SUMS`](WAVE1_SHA256SUMS) · [`wave1_metrics.json`](wave1_metrics.json)

---

## Operator-confirmed degeneracies (byte-identical CSVs)

| Pair | sha256 (12) | Operator note |
|---|---|---|
| **c02 ≡ c04** | `4EE81F2AD301` | cap8/0.25% matched cap5/0.25% on chart (natural size ≤5) |
| **c05 ≡ c06** | `ED91CD2D5D40` | risk field showed **0.55%**; export identical to 0.40% profile |
| **c11 ≡ c12** | `EA540276D101` | same on 15:45 half |

→ **9 unique panels** cover all 12 frozen labels.

---

## Cell table

| Cell | cap | risk% | fill | Pine trig | N | meanQ | maxQ | sel N | sel maxDD% | sel meanQ | sel net $ | ho net $ | a/a2/c/d/e | note |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| c01 | 3 | 0.25 | 16:00 | 15:45 | 129 | 1.92 | 3 | 73 | 0.49 | 1.79 | 2144 | 2768 | Y/Y/Y/**N**/Y | |
| c02 | 5 | 0.25 | 16:00 | 15:45 | 129 | 2.04 | 5 | 73 | 0.49 | 1.88 | 2132 | 2687 | Y/Y/Y/**N**/Y | ≡ c04 |
| c03 | 5 | 0.40 | 16:00 | 15:45 | 130 | 3.43 | 5 | 74 | 0.78 | 3.18 | 4381 | 5348 | Y/Y/Y/**N**/Y | |
| c04 | 8 | 0.25 | 16:00 | 15:45 | 129 | 2.04 | 5 | 73 | 0.49 | 1.88 | 2132 | 2687 | Y/Y/Y/**N**/Y | ≡ c02 |
| c05 | 8 | 0.40 | 16:00 | 15:45 | 130 | 5.15 | 8 | 74 | 1.24 | 4.68 | 6542 | 8015 | Y/Y/Y/**N**/Y | ≡ c06 |
| c06 | 8 | 0.55 | 16:00 | 15:45 | 130 | 5.15 | 8 | 74 | 1.24 | 4.68 | 6542 | 8015 | Y/Y/Y/**N**/Y | ≡ c05; 0.55 on screen |
| c07 | 3 | 0.25 | 15:45 | 15:30 | 129 | 1.92 | 3 | 73 | 0.49 | 1.79 | 1919 | 2612 | Y/Y/Y/**N**/Y | |
| c08 | 5 | 0.25 | 15:45 | 15:30 | 129 | 2.04 | 5 | 73 | 0.49 | 1.88 | 1888 | 2512 | Y/Y/Y/**N**/Y | |
| c09 | 5 | 0.40 | 15:45 | 15:30 | 130 | 3.43 | 5 | 74 | 0.78 | 3.18 | 3924 | 5098 | Y/Y/Y/**N**/Y | |
| c10 | 8 | 0.25 | 15:45 | 15:30 | 130 | 3.64 | 8 | 74 | 0.78 | 3.28 | 3962 | 5317 | Y/Y/Y/**N**/Y | distinct vs c08 |
| c11 | 8 | 0.40 | 15:45 | 15:30 | 130 | 5.12 | 8 | 74 | 1.24 | 4.65 | 5423 | 7528 | Y/Y/Y/**N**/Y | ≡ c12 |
| c12 | 8 | 0.55 | 15:45 | 15:30 | 130 | 5.12 | 8 | 74 | 1.24 | 4.65 | 5423 | 7528 | Y/Y/Y/**N**/Y | ≡ c11; 0.55 on screen |

---

## Hard-filter outcome (§2.6)

| Filter | Result |
|---|---|
| (a) overnight = 0 | **PASS** all 12 |
| (a2) fills ≤ cell deadline | **PASS** all 12 |
| (c) sel maxDD ≤ 6% | **PASS** all 12 (0.49–1.24%) |
| (d) sel N ≥ 80 | **FAIL** all 12 (73–74) |
| (e) holdout net ≥ 0 | **PASS** all 12 |

**Survivors:** **0 / 12**  
**Selection rule:** not reached (no survivors to rank by mean qty).

---

## Verdict

**H-SWEEP FALSIFIED** — zero cells clear (a)–(e). Binding fail = selection-window trade count under the frozen N≥80 bar. Operator accepted and closed 2026-07-16. Stage-2 H-SOLO **not authorized**. Fresh pre-reg required for any retry (Trap #12).
