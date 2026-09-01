# Scoping — 08-08 A4 flow-data fork: can positioning data adjudicate crowd-vs-death for the HARV month-end harvest?

**Status:** SCOPING COMPLETE — recommendation stands for the 2026-08-08 A4 decision (operator GO/NO-GO at the gate). Pre-assembles the Class-A **A4** evidence the ratified pre-triage asks to pre-stage.
**Date:** 2026-07-14
**Loop of record:** OUTER (research-data disposition, upstream of the HARV successor go/no-go)
**Related:** [`docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md`](2026-07-12-08-08-packet-pretriage.md) §2 A4; [`docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md`](../closures/Q-HARV-0-month-end-rebalance-ES.md); [`lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md); [`STATE.md`](../../STATE.md) Q-HARV-0 board line. Memory: `lesson_gate_reachability_preregistration`, `lesson_run_cheap_falsifier_before_authoring`.
**Method:** 3-lens research workflow (adjudication-logic / data-source-landscape-with-web-verification / resolution-adversarial), 2026-07-14; all three converge on the recommendation below.

---

## §1 — The fork

Q-HARV-0 (fade the intra-month ES-vs-ZN outperformer over T-3→T-1 into month-end) closed **AMBIGUOUS** with a real primary (+19.2 bp, p=0.013, 4× cost hurdle cleared, GC control clean, MES same-signed) but **era decay**: **2010-17 +26.3 bp (p=0.015)** → **2018-26 +13.4 bp (p=0.10, not significant)** — dead-to-insignificance exactly where deployment would live. Two rival explanations that the **realized spread cannot separate** (both lower it):

- **H-crowd** — the real-money rebalance flow is intact but more speculators front-run it. Mechanism **alive**; an earlier-entry / alt-instrument expression may still harvest.
- **H-death** — the underlying rebalance flow itself shrank. Mechanism **dead**; drop the candidate.

The A4 fork was framed (closure + STATE) as *"flow data adjudicates crowded-expression vs mechanism-death, which price data cannot."* This scoping tests that premise before any K or $ is committed to procuring flow data or to a HARV successor.

## §2 — Finding: flow data cannot cleanly adjudicate this fork

**Verdict: MARGINAL, leaning NO.** Only one channel even carries identifying information — the **CFTC TFF signed divergence between Asset-Manager (real-money rebalancer proxy) and Leveraged-Funds (speculator proxy)** net positioning around month-end. Net/aggregate positioning is **fully confounded** (a shrinking swing is equally consistent with fewer rebalancers *or* speculators pre-absorbing the flow). Four structural degradations then block a clean read even from the category split:

1. **Cadence** — TFF is a weekly Tuesday snapshot; the harvest is a 3-day T-3→T-1 flow month-end rarely lands on. Weekly can only see the end-of-month *week*, not the window.
2. **Off-futures expression** — real-money month-end rebalancing runs heavily through total-return swaps, cash/ETF, and the dealer book. A genuine H-death flow decline **may simply not appear** in the Asset-Manager futures line ⇒ absence of a positioning signal is **not** evidence against H-death.
3. **Impure mapping** — Asset Manager ≠ only rebalancers; Leveraged Funds ≠ only front-runners.
4. **Net-of-gross masking** — the small mechanical rebalance ΔNet is buried in large category gross positions.

**The load-bearing trap (why this is not just "weak"):** because weekly data cannot resolve the window, **any flow-data null reads as "effect present but unseeable" — the H-death branch is unreachable-by-construction.** Pre-registering a flow-data adjudication would re-commit the *exact* structural failure that sank Q-HARV-0's own placebo (`lesson_gate_reachability_preregistration`). Databento MBO/L3 tick has the right cadence but sees **net imbalance only** (can't split categories), so it cannot resolve the confound either — and its history starts ~2010, truncating the strong era. The confound is **structural, not a resolution problem** → higher-resolution data does not fix it.

## §3 — The fork is near-moot for the go/no-go

The decision A4 feeds is not "why did it decay" — it is **"is there a harvestable expression in the 2018+ deployment era."** That is answered **directly and more cheaply by the HARV successor's own price test** (earlier-entry, mechanism-first, 2018+ pre-registration, disjoint placebo, fresh K):

- earlier-entry variant clears cost in-era → H-crowd is effectively confirmed **and you already hold a deployable**;
- nothing harvests it in-era → the **operational equivalent of H-death regardless of cause** → drop.

Flow data cannot pre-empt that test more cheaply or more decisively, because it cannot cleanly resolve the fork.

## §4 — Recommended cheap first move (zero new data, ~$0)

Before any procurement, run a **price-only footprint + timing-migration test on the Databento GLBX `ohlcv-1d` panel already in hand** (the Q-HARV-0 harness: 192 months 2010-07→2026-06, 163 qualifying events). Two price observables that *do* carry differential signal (this sharpens the closure's "price data cannot" — see §8):

- **Footprint attenuation (H-death signature):** does the month-end volume bump (T-3→T-1 volume ÷ trailing baseline) **and** the conditioning |R_spread| magnitude shrink era-over-era (2010-17 vs 2018-26)?
- **Timing migration (H-crowd signature):** scanning entry days T-5…T-1, does the profitable reversion **migrate earlier** across eras while the footprint stays flat?

**Disposition map:** clear footprint attenuation → **H-death → DROP the successor** (do not burn K); footprint flat + reversion migrates earlier → **H-crowd → GO on an earlier-entry / alt-instrument successor**; genuinely ambiguous → the era-decay-to-insignificance already **leans NO-GO** on its own.

**Power caveat (honest):** 163 events split by era (×entry-day for the migration test) = thin cells; the price-only test can itself return ambiguous. It is still the strict first move because it is free, directly measures the mechanism's own footprint, and — unlike weekly flow data — its H-death branch **is** reachable.

## §5 — Data-source landscape (so nobody re-derives it)

| Source | Granularity | Coverage (ES+ZN) | Cost | Fit for the fork |
|---|---|---|---|---|
| **Price-only footprint/timing test** (existing Databento bars) | daily; event-study by era | 2010-07→ (matches panel) | **~$0** | **Best** — direct, free, H-death branch reachable. Run first. |
| **CFTC TFF** (Traders in Financial Futures) | weekly, Tue snapshot / Fri 3:30pm ET | to **2006-06-13** | **free** (cftc.gov CSV / Socrata) | The *only* positioning report with the real-money-vs-spec split; but weekly cadence + off-futures + net-masking ⇒ **prior-mover, not decider**. Non-blocking corroborant only. ES/ZN are **TFF, not Disaggregated**. |
| CFTC Legacy COT | weekly | ES ~1997 / ZN 1990s | free | Coarser (commercial/non-commercial ≠ rebalancer/front-runner). Cross-check only. |
| Databento GLBX MBO/L3 tick | tick/intraday | ~2010+ | **expensive, cost-gated** | Right cadence but **net imbalance only** (can't split categories) → non-identifying. **Never procure for this fork.** |
| Balanced/target-date AUM (ICI) | monthly/quarterly | decades | free/low | Weak prior *against* H-death (rebalance AUM grew 2010→26), but migrated to internal-cashflow rebalancing → loose proxy. |
| Vendor crowding proxies (OFR/Barchart/Nasdaq) | weekly | 2006+ | free–cheap | Just repackaged CFTC COT — no independent signal. Genuine real-money estimates are sell-side desk notes, not procurable as a clean series. |

## §6 — Recommendation

**DEFER flow-data procurement. DROP the tick-history path entirely. Do not gate the HARV successor on a flow-data adjudication.**

1. Run the §4 **price-only test** on data in hand (~$0) as the real adjudicator / go-no-go input.
2. Optionally pair with the **free CFTC TFF** era-decomposition (AM-vs-LF month-end divergence) **only as a weak, non-blocking prior** — and **do not** pre-register any flow-data test whose H-death branch is unreachable.
3. **Escalate to paid tick procurement: never** for this fork (structural confound, snoop-prone, research-only, no live-signal payoff).
4. Let the **successor's own 2018+ earlier-entry price test** carry the mechanism adjudication.

## §7 — Boundary (unchanged)

Flow/positioning data here is a **research adjudication tool only** — not proposed as a live tradable signal/feature (the discovery pipeline and the four-firms prop program trade on price/volume; flow data has latency/venue/snooping problems as a live input). This scoping does not touch that boundary, any locked parameter, allocation, `dd_protection`, `ACTIVE_FIRM`, or Pine.

## §8 — Refinement to the closure's A4 framing (flag for the 08-08 owner)

The Q-HARV-0 closure + STATE carry *"flow data adjudicates … which price data cannot."* Precise correction: the **realized edge/spread** cannot distinguish crowd from death (both lower it) — but **other price observables can** (weakly): the month-end **volume footprint**, the conditioning **|R_spread| magnitude**, and the **entry-timing migration**. So "price data cannot" was too strong; it should read "the realized spread cannot, but its footprint/timing signatures can — and they dominate flow-data procurement on cost, directness, and null-reachability." Recorded here, **not** edited into the closed record; the 08-08 A4 owner should read A4 through this refinement.

## §10 — Audit hooks (runnable)

```bash
# This scoping exists and is linked from the 08-08 packet's A4 evidence line
test -f docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md && echo present
grep -n "A4" docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md   # A4 is the fork this pre-assembles

# The cheap first move is a re-analysis of data in hand — no new pull, no register_search
ls lab/analysis/harv_0_month_end_rebalance_es_2026-07/ 2>/dev/null || echo "(archived — see lab/archive/ or git)"

# If a flow-data test is ever pre-registered for this fork, its H-death branch MUST be reachable
#   (else it repeats the Q-HARV-0 placebo trap). Guard:
grep -rn "TFF\|flow.data\|positioning" docs/briefs/pre-registration/ 2>/dev/null | grep -i harv \
  && echo "CHECK: a flow-data HARV pre-reg exists — verify its H-death branch is reachable" \
  || echo "no flow-data HARV pre-reg (expected — DEFER stands)"
```
