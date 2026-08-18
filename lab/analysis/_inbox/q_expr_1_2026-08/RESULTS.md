**Theme:** _inbox
**Status:** CLOSED — H1 horizon-mismatch 4/4 models the orphaning; H2 1/5 misses; H3 cannot fire
# Q-EXPR-1 — conversion-step census

**Verdict:** `RESOLVED` (H1 fires). H2 misses. H3 cannot fire.
**Date:** 2026-08-18
**Spend / K:** $0 / K=0
**Parent:** [`Q-EXPR-1-regularity-expression-conversion.md`](../../../../docs/briefs/Q-EXPR-1-regularity-expression-conversion.md)
**Prereg (hashed before TABLE.json was opened by the scorer):**
`27c366f4f7e7a924a8e91ba549c8ade25eadd2024add1e827d70a31828e6441a`

E1 here = venue **flat-by-16:00** envelope, not MSL "E1 HOLD".

Reproduce:

```bash
python lab/analysis/_inbox/q_expr_1_2026-08/score_expr.py
```

The runner prints the prereg sha256 **before** reading `TABLE.json`.

---

## Shares vs the frozen 0.50 bar

| H | k/n | share | Wins? |
|---|---|---|---|
| H1 horizon-mismatch | 4/4 | **1.00** | **yes** |
| H2 cost-quantization | 1/5 | 0.20 | no |
| H3 survivor-artifact | — | cannot fire | no (weekly + daily share first-measurement day 2026-06-19) |

`RESOLVED` because ≥1 H meets 0.50. Winning branch: **H1 only**.

---

## B1 — validated regularities

| id | native | first measured | H1-eligible | H1+ |
|---|---|---|---|---|
| R-W-STRUCT — ICT weekly structure | weekly | 2026-06-19 | yes | yes |
| R-D-FVG — SSL bear-FVG draw | daily | 2026-06-19 | yes | yes |
| R-D-POOLS — pools anti-attractor | daily | 2026-06-19 | yes | yes |
| R-CL-RANGE — CL range-state SIGNAL-GENERIC | daily | 2026-08-18 | yes | yes |
| M-DEADWEEKS — 82/312 dead weeks | operational | 2026-08-02 | no | — |
| M-REGIME-TIME — Q-REGIME-TIME-1 RESOLVED-LARGE | operational | 2026-06-09 | no | — |
| M-VVG — Mesfin/N12 descriptive regime findings | operational | 2026-08-04 | no | — |

One object, one row. W/D replications across US500/NQ/MNQ are notes, not extra rows.

H3 first-screened class is unidentified: the cascade close of **2026-06-19** is the earliest
H1-eligible stamp and lands **weekly and daily on the same calendar day**. Modal horizon is
daily (3/4) — disclosed, not a fire.

---

## B2 — conversion attempts (evidence; not H1/H3 denom)

| id | of | death stage | geometry / residual |
|---|---|---|---|
| A-WSTRUCT-COST | W | cost-hurdle | E1-forced 2–5 RTs/week; honest 2RT 0.87× FAIL |
| A-WLEGB | W | reachability | daily gateHit 53.77% vs placebo 53.82% |
| A-MNQPOOL | pools | reachability | stop at pool, median 572 pt below |
| A-MNQFVG | FVG | reachability | limit at near-edge, median 291 pt; 18% touch |
| A-CL-COND | CL | never-attempted | CONDVAL ΔE 0.034R vs bar 0.110R; no host built |
| A-TXG-NAS-MYM | locked book | cost-hurdle | mean_net_r 0.0129 < 0.06 |
| A-TXG-STR-MNQ | locked book | stop-geometry | cost PASS; N-SURV ~98% bust |
| A-TXG-GUAR-MGC | locked book | stop-geometry | N-SURV full bust 42.2% |
| A-TXG-AEGIS-6J | locked book | stop-geometry | J14 composed GEOMETRY-FAIL 10.96% vs 3.0% |

Q-TXG-1 is prior art + these four rows, not a rediscovery.

---

## B3 — H2 class (frozen at GO)

| cell | death | gross_edge_present | H2+ |
|---|---|---|---|
| Q-TNEC-CON-2 | cost-hurdle | **yes** (gross +0.90/+0.97 pt; short placebo p=0.027) | **yes** |
| Q-TNEC-CON-3 | cost-hurdle | no (gross +4.14 pt; placebo 0.165; CI straddles) | no |
| Q-TNEC-CON-4 | cost-hurdle | no (gross +1.50 pt; means ≈0; placebo ≥0.435) | no |
| Q-TNEC-CON-5 | cost-hurdle | no (gross +0.61 pt; both arms mean-negative; placebo ≥0.894) | no |
| Q-R2AGRUN-1 | magnitude / CI-power | no (association floor; not a hurdle kill) | no |

H2 does **not** re-read the four TNEC-CON cells as a class of hurdle-kills. CON-2 already
was one, on its own closure.

---

## What this does not license

- H2 admission-rule change (projected gross/(4×RT) screen) — H2 missed.
- Demoting "find more regularities" via H3 — H3 could not fire.
- Opening Q-TRAINKILL-1.
- Retracting any regularity. H1 says the *conversion* dies when native > session, not that
  the facts are false.
- Treating TXG walls as this Q's discovery.
