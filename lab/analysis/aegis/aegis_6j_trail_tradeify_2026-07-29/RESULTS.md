**Theme:** aegis
**Status:** ACTIVE — J4 re-run at true Tradeify Select 100K geometry (Aegis→6J v0.3)
# RESULTS — J4 re-run at TRUE Tradeify Select 100K geometry (Aegis→6J v0.3)

**Date:** 2026-07-29 · **Runner:** [`trail_survival_tradeify.py`](trail_survival_tradeify.py) (seed 20260705)
**Logs:** [`run_cap8.log`](run_cap8.log) · [`run_cap12.log`](run_cap12.log)
**Input:** v0.3 deep panel, n=129 intraday trade-days, sha256 `c3b34162…` (pin verified this run)
**Supersedes as the decision basis:** [`RESULTS_trail_mc.md`](../aegis_6j_transfer_2026-07-05/RESULTS_trail_mc.md)
(ledger **J4**, Bulenox Option-2 site-example figures, flagged PROVISIONAL). That harness is
**byte-untouched**; this is a parameterized re-implementation with a proven equivalence control.

**Classification: a re-run at corrected venue inputs.** Same candidate, same panel, same gate.
No fresh K, no discovery search, no pre-registration consumed.

---

## §1 — Reproduction control: 12/12 PASS (gate passed before any arm was read)

The parameterized walk reproduces **every** published J4 figure at the Bulenox basis — both
deterministic anchors to the cent and all ten stochastic rows to <5e-5:

| Check | Expected | Reproduced |
|---|---|---|
| Anchor, full size | breach 2022-11-23, $97,326.25 vs floor $97,440.90 | ✓ exact |
| Anchor, 0.5× | no breach; min headroom $842.70; pass 2023-09-11; post-freeze min $100,942.70 | ✓ exact |
| 10 stochastic rows (arms a/b × rotation/L6/L13/L26/no-freeze) | published table | ✓ all 10 exact |

**This is what licenses the arms below.** A re-implementation that reproduces the original to the
cent is proven equivalent rather than asserted — the divergence from here is the *rule change*,
not the rewrite.

## §2 — What actually differs between the two account bases

Read from [`core/firm_rules.py`](../../../core/firm_rules.py) `Tradeify_Select_100K`:

| Parameter | Bulenox Opt-2 (J4) | Tradeify Select 100K | Δ |
|---|---|---|---|
| starting balance | 100,000 | 100,000 | — |
| trailing DD | $3,000 | `max_dd_pct 3.0` = $3,000 | **SAME** |
| floor lock | start + $100 | `dd_lock_offset_usd 100` | **SAME** |
| eval target | 6% = $6,000 | `profit_target_pct 6.0` | **SAME** |
| daily loss limit | $2,200 (never bound) | none | n/a |
| min trading days | 0 | 3 | trivially met (129) |
| **consistency rule** | none | **40% (eval only)** | **NEW — modelled** |
| **contract cap** | **12** | **8** (inferred) | **binding** |
| **commission** | **$1.30/side** (placeholder) | **$3.10/side** | **binding** |

**FINDING 1 — the trailing geometry is numerically IDENTICAL.** Arm A (Tradeify geometry, cap 12,
$1.30) returns **10.85% / 11.63% / 88.37%** on the exhaustive rotation — digit-for-digit the
published J4 row. So J4's PROVISIONAL-basis caveat, though procedurally correct, **was never the
thing that mattered**. The account-geometry worry is closed: the two firms' eval trails coincide.
What differs is **cap and commission**, which J4 never varied.

## §3 — Arms (rotation = exhaustive ×129; L13/L26 = 10,000-path circular block bootstrap)

Per the parent's own guidance, **rotation and L≥13 are the trusted rows** (L=6 breaks the panel's
serial structure and runs hot); L=6 is omitted here as a known pessimistic bound.

### Cap 8 (inferred Tradeify limit for a full-size currency contract)

| Arm | Sizing | breach<freeze | **breach ever** | eval pass | consistency-OK @ pass |
|---|---|---:|---:|---:|---:|
| **A** geometry only (cap 12, $1.30) | full | 10.85% | **11.63%** | 88.37% | 42.11% |
| **B** + cap 8 ($1.30) | full | 3.88% | **3.88%** | 96.12% | 77.42% |
| **B** + cap 8 ($1.30) | 0.5× | 0.00% | **0.78%** | 99.22% | 96.09% |
| **C** VERIFIED (cap 8, $3.10) | full | 11.63% | **12.40%** | 87.60% | 85.84% |
| **C** VERIFIED (cap 8, $3.10) | **0.5×** | 0.00% | **3.88%** | 96.12% | 92.74% |

Arm C bootstrap rows — full: L13 **10.79%**, L26 **14.66%** · 0.5×: L13 **5.31%**, L26 **5.00%**.
Panel net by arm: $39,056 (A) → $27,402 (B) → **$23,701** (C).

### Cap 12 adverse sensitivity ($3.10/side)

full: rotation **13.18%**, L13 **18.67%**, L26 **14.42%** · 0.5×: rotation **9.30%**, L13 **14.23%**, L26 **11.66%**.

## §4 — Verdict against the 3.0% Part-A admission ceiling

**FAILS in every arm — but by far less than the pre-run estimate, and the margin is the story.**

- **Best cell in the entire matrix** (verified inputs, 0.5×-until-freeze, exhaustive rotation):
  **3.88% vs a 3.0% ceiling — 1.3× over**, not the ~4× that the un-corrected J4 headline implied.
- Its own bootstrap rows are **5.00–5.31%**, i.e. **1.7–1.8× over**.
- Full-size at verified inputs is **10.79–14.66%** — the ~4× regime, which is where the J4
  headline figure actually lives.
- The adverse cap-12 reading is **9.30–18.67%**.

**FINDING 2 — the two corrections very nearly cancel, and this is the load-bearing mechanic.**
Cap 8 alone cuts breach **11.63% → 3.88%** (smaller size against a *fixed* $3,000 trail). Restoring
the true $3.10/side commission pushes it back to **12.40%** at full size. Commission is a pure
per-contract subtraction that does not shrink with the trail, so at reduced size the edge falls
while the barrier does not — the account grinds toward the floor. **Reducing size to survive the
trail is partially self-defeating once real fees are charged.** Anyone re-deriving this with cap
corrected but commission left at the $1.30 placeholder would read 3.88% and conclude PASS-adjacent.

**FINDING 3 — the 40% consistency rule is a genuine new obstacle J4 could not see.** At cap 12 only
**42–47%** of passing paths satisfy it at first touch of +$6,000: the strategy's big days are large
relative to a $6,000 target, so most passes would be consistency-blocked and forced to keep trading
— *more exposure, more breach risk*, a coupling this sim reports but does not compound. At cap 8 it
relaxes to **77–86%** (and 92–96% at 0.5×). Cap 8 helps both barriers at once.

## §5 — Caveats (all load-bearing; none rescue the verdict)

1. ~~**Linear cap re-scale, not a native replay.** Precedent F2 validated linear re-capping to
   **within 2%** against a native TV run. A native cap-8 replay is operator-owed and would
   supersede.~~ **DISCHARGED 2026-07-29 (later) — the native replay already existed.**
   `baseline_fill1600_cap8_c310_2026-07-16_68f0e.csv` is a **native cap-8 / $3.10-per-side** export
   (n=130, +$22,258.00, 2022-01-12 → 2026-07-15, qty 6–8, Stage-0 `ENVELOPE-YES`). Re-measuring the
   same configuration on it: **1.04% L13 / 1.38% L26, net $11,129** vs the re-scaled
   **0.67% / 0.77%, net $11,851**. **The approximation was OPTIMISTIC — ~0.4pp low on breach and
   +6.5% high on net — so the F2 ±2% precedent understated the error.** The window verdict is
   unchanged (PASS on 2022+), but any future cap-8 work must use `68f0e`, not a re-scale.
   Lineage: [`PANEL_OF_RECORD.md` §4](../aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md) · ledger **J10**.
2. **Cap 8 is INFERRED**, from Tradeify publishing eval limits as mini/micro pairs (`8/80` here)
   with no third bucket for full-size currencies. Not verbatim. Cap 12 is run as the adverse case;
   **both fail.**
3. **Commission $3.10/side** is the ledger's 2026-07-13 primary-verified cross-firm figure;
   re-verify at any deployment fork.
4. **Standalone, not composed.** This measures 6J *alone*. The admission gate governs the **book**,
   and adding a leg adds variance — Q-COMPOSE-1 saw ORB take composed bust 2.65% → 38.75%. A
   candidate that already fails standalone **fails composed a fortiori**, so no composition run is
   owed to reach the verdict.
5. Single 4.5-yr panel; bootstrap reuses its marginals (no regime enrichment). Trade-day
   granularity, EOD-only floor checks (bounded by max AE $1,733 at cap 12).

## §6 — Disposition

**D2 (Aegis-6J) stays PARKED — now on a measured basis at the registered tier rather than on a
provisional one at a different firm.** The venue-legality objection is dead (mixing clause
rescinded), the data-thinness objection was wrong (full-stop cohort n=10, not n=1), and what
remains is a **1.3–1.8× overshoot of the survival ceiling at the best achievable sizing** —
narrower than previously believed, and still a fail.

**What would change the verdict** (none performed, none owed):
- a native cap-8 TV replay (removes caveat 1);
- a commission re-verify materially below $3.10/side;
- an operator decision to move the 3.0% Part-A ceiling — which is owned by its own ADR chain and
  was already re-derived once (Q-BUSTGATE-1) and left at 3.0%.

**Still unmeasured and independently blocking on the ratified third-leg screen:** **S2** (6J is not
a micro; M6J is not a Tradeify product) and **R1** (per-contract daily-$ std ≤ ~$125, never
measured for 6J).

No `core/`, allocation, `dd_protection`, Pine, rung, or rail byte touched. Nothing armed.
