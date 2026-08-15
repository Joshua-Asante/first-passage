# Cheap falsifier — MCL TAS δ-extraction **probe reachability** · `KILL-PENDING-σ` (magnitude wall)

**Date:** 2026-08-11 · **$0.00 · K=0 · no Q-ID spent · no G0 authored · no market data read**
**Trigger:** operator asked to scope the δ-extraction probe re-opened by the
[`Q-TNEC-ENV-1` closure](../../../docs/briefs/closures/Q-TNEC-ENV-1-closure.md) item (b) ruling
(*"the direction re-opens only through a completed δ-extraction probe"*). Standing lesson
`lesson_run_cheap_falsifier_before_authoring` — run the falsifier BEFORE the brief, parent-side,
designed generous so a failure is conclusive.

**What is being falsified:** not the mechanism — the **probe**. Is the δ this probe would have to
find even in the range of any causal-public δ this estate has ever admitted? If not, the probe is
unfundable before it is designed, and the cheapest correct act is to say so.

## Frozen before running (all constants imported, nothing re-derived)

| Input | Value | Owner |
|---|---|---|
| `COST_LAW_MULTIPLE` | 4.0 | harvest Req 5 · operator-frozen `COST-MULT-4X` |
| `RT` (MCL) | $2.90 | envelope [PREREG F3](tnec_envelope_compile_2026-08/PREREG.md) — $0.95/side + 1 tick `total_rt` **PRIMARY** |
| `tick_value` | $1.00 | MCL = $0.01/bbl × 100 bbl |
| `stop_ticks` | 20 | [entry JSON](tnec_envelope_compile_2026-08/entries/mcl-tas-settlement-window-replication.json) — shallowest OPEN rung |
| committed `N` | 251 | envelope PREREG F5 (MCL Stage-1 own-panel) |
| comparison cohort | causal-**public** δ only | informed-flow components already stripped, per [R8](../harvest/tnec_l2_sourcing_2026-08-10/DELTA_EXTRACTION_R8.md) |

**KILL iff** the required δ exceeds the largest causal-public δ ever admitted in this estate,
**at the most generous price basis**, and survives the killing-constants ablation.

## Result — the magnitude wall fires at every basis

Req-5 hurdle = 4.0 × $2.90 ÷ $1.00 = **11.60 ticks/event** = $11.60/contract = **$0.1160/bbl**
= **0.580R** of the cell's own 20-tick stop.

| Panel-era price basis | Required δ | vs estate causal-public ceiling (3.21 bp) |
|---|---|---|
| $70/bbl (conservative low) | **16.57 bp** | 5.16× |
| **$78/bbl (2023 MCL cache era)** | **14.87 bp** | **4.63×** |
| $95/bbl (2022 elevated) | 12.21 bp | 3.80× |
| $120/bbl (implausible high — stresses the hurdle *down*) | 9.67 bp | **3.01×** |

Estate causal-public δ record, for the comparison: gold PM-fix **+3.21 bp** (R8 generous top,
includes the untimeable end-block) · D5 intraday momentum **+2.97 bp** · H-OD-1 **+1.50 bp** ·
gold PM-fix conservative **+1.32 bp** · **H-FBEIA-1 CL-EIA −1.16 bp** (same instrument family,
wrong-signed).

**Killing-constants ablation** (2026-08-10b pattern — does relaxing the frozen basis rescue it?):

| Basis | Hurdle | Required δ @ $78 | vs ceiling |
|---|---|---|---|
| PRIMARY, F3 as frozen ($0.95/side + 1 tick) | 11.60 ticks | 14.87 bp | 4.63× |
| DISCLOSURE, bare commission $1.90 RT — **forbidden as a hurdle** by F3 | 7.60 ticks | 9.74 bp | **3.04×** |

The kill survives the most generous admissible basis *and* the forbidden one. It rests on the 4×
multiple and MCL's tick geometry, **not** on the slip election.

**Power limb is not the wall.** F5 min detectable δ/σ at N=251 = 1.96/√251 = **0.1237**. A δ *at*
the cost hurdle clears power for any per-event σ ≤ 93.8 ticks ($0.938/bbl); a 2-minute CL window σ
is order 10–20 ticks. **Power is slack conditional on cost clearing — cost is the sole binding wall.**
(The σ magnitude is an order-of-magnitude sanity note, **not** a measurement.)

## Why the verdict is `KILL-PENDING-σ` and not `KILL`

**The honest counter, stated because it is the strongest one available.** The table compares a δ
required on **oil** against a ceiling measured on **gold and equity indices**, in **bp**. Oil's
per-minute σ is materially larger, so bp-space is not cohort-neutral — this is
`lesson_metric_cohort_provenance_binding` firing on my own comparison. The cohort-correct space is
**δ/σ**, and rough scaling (CL 2-min σ ≈ 15 ticks vs GC fix-window ≈ 8 bp) narrows the gap from
~4.6× to roughly **~2.4×**. It **narrows but does not close**, and the narrowing figure is
hand-scaled, not measured.

**Consequence:** the falsifier is conclusive on the *shape* of the answer and provisional on its
*size*. Pinning MCL's own 14:28–14:30 ET window σ on the **already-committed 2023 cache** is a
**$0 / K=0** measurement (σ is a dispersion statistic, not an edge read — no PnL, no direction,
no selection) and converts this to a cohort-bound verdict. That is the first thing the probe
scoping should buy, and it is free.

## The second wall the arithmetic does not reach — the sign source

Independent of magnitude: the mandate obliges the counterparty to **transact in the window**; it
does not entail a **sign**. Reading the sign off the window's own price action is BE1's kill
verbatim (*"constraint carries neither sign nor level; direction laundered from price"*).

The closure's recorded route — *"free CME TAS volumes, non-circular"* — establishes non-circularity
for the **volume/decay observables** (Req 1a(iv)). It does **not** name a free, **signed**,
**exogenous** imbalance source, and published TAS volume is a total, not a net. **Whether such a
source exists is unverified and is the load-bearing unknown**; if it does not, the probe is
circular in exactly the way F1/MOC was ruled circular, at zero further cost.

**Mechanism-level prior, and it is adverse:** TAS exists *so that* mandated flow can lock the
settlement print without revealing direction to the outright book. The public residue in the
outright book is therefore small **by construction** — which is precisely R8's measured structure
(large informed δ, near-zero unconditional public residue). The informed-flow signature has now
fired **three times** (H-FBEIA-1 CL-EIA, NG-EIA-1, R8), and **CL is the instrument where it was
first confirmed**.

## Verdict

`KILL-PENDING-σ` — **conclusive that no probe should be funded on the current record**; provisional
pending one free σ measurement that either confirms the kill in cohort-bound units or reopens it.
**Licenses nothing.** No Q-ID spent, no G0, no data pull, no K.

Routing: [`Q-MCLTAS-1`](../../../docs/briefs/Q-MCLTAS-1-tas-settlement-delta-extraction-probe-scoping.md)
carries the staged design and the operator decision.

## Reproduce

```bash
python lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_mcl_tas_probe_2026-08-11.py
# Expected: FALSIFIER FIRES; 4.63x at the 2023 basis, 3.01x at the most generous
```
