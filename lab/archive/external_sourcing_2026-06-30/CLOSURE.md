# External-strategy sourcing — Closure (§2.N)

**Date:** 2026-06-30 · **Pass:** thesis-first narrow (chop / follow-through-deficit decorrelated leg) · **Spec:** [CC-HANDOFF-external-strategy-sourcing.md](../../../docs/ltm/briefs/rnd-pipeline/CC-HANDOFF-external-strategy-sourcing.md) · **Locks:** [PREREGISTRATION-0.5-locks.md](PREREGISTRATION-0.5-locks.md)

```
Status: DONE
Program closure: RESOLVED (gate ran clean; 0 candidates SAVED — a zero count is RESOLVED, §6)
Per-step gates: 2.1 [pass, merged PR #251] 2.2 [pass] 2.3 [pass] 2.4 [pass-by-exhaustion: 0 ADMIT]
                2.5 [skip: empty corpus] 2.6 [skip] 2.7 [skip] 2.N [this]
Funnel: harvested=69 (source-CONFIRMED=65, MISREPRESENTED=4) distinct_clusters=~12
        lane_A_survivors=0  lane_B_shortlist=4  admitted=0  frozen=0  oos_pass=0  saved=0
Diffs (uncommitted, awaiting go): lab/research/external_sourcing_2026-06-30/{PREREGISTRATION-0.5-locks,catalog,triage,CLOSURE}.md
Next action recommended: accept RESOLVED-zero; feed to the 2026-08-08 HOLD/regime review; do NOT pull the deferred maximal-harvest forward (Edit 3).
```

## Consolidated verdict

The thesis-first external-sourcing pass closes **RESOLVED with zero saved candidates.** This is the brief's
anticipated, correct outcome (§4/§6): taking external-strategy survivorship seriously yields a low-to-near-zero
first-pass hit-rate. It is **not** a failure or an AMBIGUOUS (under-powered) close — the survivors were
adequately assessed and their walls **cheaply falsified** (source-checked), not left undecided.

## What ran

- **§2.1 machinery** — merged (PR [#251](https://github.com/Joshua-Asante/multi_firm_operations/pull/251), `8458a90`); the publication-date OOS gate (pre-d-only selection) is the gate the pass relied on (Rule-0 re-confirmed this session).
- **§2.2 harvest** — Workflow `wf_6a7fc6ff-c94` (13 mechanism-family deep searches → adversarial source-verify → synthesize). 69 verified rows, 65 source-CONFIRMED, 4 MISREPRESENTED-and-excluded. [catalog.md](catalog.md).
- **§2.3 triage** — [triage.md](triage.md). ~12 distinct mechanism clusters scored against the three walls + Edit-1/Edit-2. **0 Lane-A survivors** (the only codifiable cluster, Bollinger/z-score band-MR, is a thesis-mismatched 5th-Aegis — correlated with the book's existing MR leg, not decorrelating). **4 Lane-B shortlist** advanced to adversarial verification.
- **§2.4 adversarial verify** — Workflow `wf_a6ad0a88-823` (4 survivors × 2 skeptic lenses, burden-of-proof on the candidate). Mechanical dedup (`dedup_check` logic): no hard DUPLICATE; 3 NEAR_MATCH→human-review (instrument-overlap-driven). **0 of 4 survive to ADMIT.**

## Why each Lane-B survivor died (source-grounded)

| Candidate | Cluster | Decisive wall (source-checked) |
|---|---|---|
| **Gold/Silver ratio cointegration MR** | F (market-neutral spread) | **Wall-2:** "market-neutral" is *dollar*-neutral, **not regime-neutral** — the XAU/XAG ratio spiked to an **all-time high >126 in Mar-2020** (silver crash) → the spread draws down maximally *in* the book's H1 risk-off regime; silver is the high-beta risk leg → implicitly net-long-risk in chop. Cointegration regime-unstable post-2011; cherry-picked 2015-2025, no OOS. **Wall-3:** two-leg, non-codifiable. |
| **VIX-amplified market-closure reversal** (Della Corte-Kosowski, SSRN 2730304) | D (overnight reversal) | **Edit-2 / Wall-5:** the proposed returns-independent side-prediction is **explicitly falsified by the source** — "stock-market uncertainty *fails* to explain this overnight-intraday reversal" for 3 of 4 asset classes; VIX works only for equity-index futures; the real predictor is **cross-sectional dispersion** (non-tradeable single-account). **Wall-3/4:** cross-sectional long-short non-codifiable; the codifiable single-asset degenerate form = the already-FALSIFIED NOCT-SPX. |
| **Gold abnormal-day contrarian** (Caporale-Plastun 2020) | H | **Source contradicts the framing:** the gold abnormal-day effect is **intraday momentum** (price moves *with* the spike to close → co-moves with Guardian) + only a *next-day* contrarian; that next-day reversal **equals the strategy's own P&L** → no returns-independent side-prediction (**Edit-2 CULL**). ~50% post-publication decay. Non-codifiable (must SHORT; long-only codifier). |
| **IBS close-location MR** (Pagonidis 2013) | A | Side-prediction genuine (close-location bucket→next-bar monotonicity, price-only) — the *only* one that cleared Edit-2 — **but Wall-2:** long-only daily dip-buy on equity indices = **net-long the same factor as Striker DJ30/NAS100** → co-draws in H1 (Aegis-2022 failure shape). Documented post-2015 decay ("arbed away"). Non-codifiable. |

## Load-bearing findings

1. **External sourcing is exhausted-NULL for the chop-decorrelated-leg thesis (first pass).** The external direction — the one §1 named as "not yet worked" — surfaced ~30 distinct documented mechanisms, and **every structurally-serious one died on the same three walls that killed every internal chop-native search** (regime co-occurrence in H1; single-account non-codifiability; side-prediction that reduces to returns / is falsified by its source). This **corroborates the 2026-06-07 decompound HOLD from the external angle**: the chop-regime gap is **structural**, not a sourcing deficit. The relief lever is the same as the internal searches concluded — exogenous / paid data or a genuinely new venue, **not** a published retail strategy.

2. **"Market-neutral" ≠ "regime-neutral" (the gold/silver catch).** A dollar-neutral spread can still be net-long-risk in chop if one leg is the high-beta risk-sensitive instrument; its tail co-occurs with the book's H1 risk-off. Decorrelation must be tested in the H1 regime, not assumed from market-neutrality.

3. **Methodology sub-lesson — harvest-agent "independence=yes" side-prediction labels are unreliable; check Edit-2 against the SOURCE at verify, not the harvest self-label.** Two of four survivors' "returns-independent" side-predictions were contradicted by their own papers (VIX-amplification explicitly rejected for 3/4 asset classes; gold abnormal-day reversal reduces to the traded P&L). Only the adversarial **source-check** caught it. This is the Edit-2 / "do not confirm a mechanism with its own returns" discipline working — and it echoes the GEX-death pattern (a side-prediction that collapses to a proxy/the-edge on inspection).

## Discipline check (forbidden moves honored)

- No concept ADMITted on a story alone (Edit-2 enforced; 2 culled for non-independent side-predictions).
- No pre-`discovery_date` performance credited (all `claimed_performance` is source-stated, never primary-table-verified; zero evidential weight).
- No corpus frozen then pruned (empty corpus; nothing to peek).
- Corpus-FDR not invoked as the survivorship antidote (it never ran — there was nothing to test).
- Harvest coverage gaps logged, not silently capped (catalog.md / triage.md — SSRN 403, QuantifiedStrategies CAPTCHA, TV JS-gated, pervasive instrument/timeframe-transfer gap, under-searched channels enumerated).
- Deferred maximal-harvest **not** pulled forward (Edit 3) — remains for the 2026-08-08 HOLD disposition.

## Open / deferred (not this pass)

- **Coverage gaps** that a *future, deeper* pass could mine (logged in [catalog.md](catalog.md), not pursued here): auction/Market-Profile value-area fades; stochastic %K/%D fades; FX-microstructure intraday/day-of-week (USDJPY/USDCAD); OPEX-week & Treasury-auction index calendar; a DJ30↔NAS100 cointegration backtest; open-source GitHub MR repos; paid TradingView/QuantConnect equity curves. None changes the structural read above.
- **Optional override (Joshua's call):** a formal Lane-B mechanism-probe on **gold/silver ratio MR** (the one candidate with a genuine returns-independent cointegration side-prediction) — **not recommended**: the cheap regime falsifier already fired (the Mar-2020 ratio blow-out), so a formal probe would re-confirm a known Wall-2 fail at real cost.
