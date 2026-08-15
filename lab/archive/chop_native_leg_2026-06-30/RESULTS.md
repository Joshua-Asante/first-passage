# Chop-native 5th-leg candidate search under the futures-prop venue — RESULTS

**Date:** 2026-06-30 · **Disposition:** CLOSED — no viable candidate · **Scope:** lab-only (no `core/` / lock / allocation / `dd_protection` / Pine change). Locked config HELD 99.83/0.17/4.37.

## 0. Question

"Identify the top candidate for a chop-native leg of the portfolio" — a leg **natively profitable in directionless/range markets**, held *concurrently* with the 4 long-biased trend legs so their 2020-2023 chop-starvation is offset without needing to *detect* the regime (detection is CLOSED — [`regime_signal_research_2026-06-25`](lab/analysis/regime_signal_research_2026-06-25/CLOSURE.md)).

**Why this re-opens a structurally-closed thread legitimately:** the 5th-leg programme closed on `regime-robust ⟂ tradeable-here-affordably`, but that wall was largely **FXIFY-DXTrade-specific** (BTC died only on the crypto-account rule; the MR crosses died on CFD spread cost geometry). The **2026-06-29 futures-prop pivot** ([[project_futures_prop_pivot]]) is genuine new-mechanism evidence — CME micros change the eligibility universe *and* the cost law (commission-per-contract, no swap, tight tick). This search re-answers the question against that new venue.

## 1. Target spec + the three kill-walls

From [`decompound_ddprot_2026-06-21/RESULTS.md`](lab/analysis/decompound_ddprot_2026-06-21/RESULTS.md): the leg must have **after-cost PF ≈ 2.0 whose edge persists through the 2020-2023 chop regime**, inserted **risk-neutrally** (edge dominates; ρ is second-order — a marginal-edge leg hurts even at ρ=−0.6). Every prior candidate died on exactly one of three walls:

1. **Cost geometry** — `cost_R = round_trip_cost / realized_stop < 0.05R` ([`scripts/cost_geometry_pregate.py`](../../scripts/cost_geometry_pregate.py)). **Venue-specific** (futures cost law differs from CFD).
2. **Era conditionality** — a post-2020-only edge (ORB pattern) is disqualified. **Venue-independent.**
3. **Selection envelope** — vol-orthogonal AND era-orthogonal AND wide-best-of-K. **Venue-independent.**

## 2. Eight-family scorecard (workflow `wf_021dbd44-64c`, 12 agents)

| Family | Score | passes walls | Where it dies |
|---|---:|:--:|---|
| Micro-rates / STIR MR (M10Y/2YY) | 26 | ✗ | era/tail — **see §3** (2022 trend → fade bleeds in H1) |
| Index stat-arb (MES–MNQ spread) | 22 | ✗ | cost: 2-leg doubled cost over few-tick stop ≈ 0.18–0.46R; edge decayed post-2009, revives only in crisis bears |
| Metals intraday MR (MGC) | 22 | ✗ | era: only positive cohort is ML-regime-filtered + post-2020; HIGH corr to Guardian (shared XAU) |
| FX-futures range MR (M6E/J/B) | 14 | ✗ | cost: micro tick = 1 full pip = $1.25 doesn't undercut CFD → ≈0.08–0.15R = same USDCAD 0.097R wall; direct registry collision |
| Commodity calendar / ag seasonality | 14 | ✗ | not chop-native (calendar clock); edge pre-2000; calendar spreads un-routable on TradersPost |
| Short-term index reversal | 11 | ✗ | reduces to overnight drift already falsified (NOCT-SPX); net-negative after futures spread |
| Short-vol / VRP (VX/VXM) | 9 | ✗ | venue: VX/VXM are Cboe **CFE**, not CME — no prop routing; + catastrophic co-occurring tail (XIV −97%/day) |
| Intraday range-fade / VWAP | 8 | ✗ | empirical **anti-edge** (US500 VWAP-reversion −0.33R, neg all 5 yrs) |

**0/8 pass all walls** → the adversarial-verify stage had nothing to escalate. The top survivor (micro-rates MR) clears cost+venue+novelty but is HELD pending the cheapest falsifier (§3). Full per-family cards: workflow output (session `a6e97c75` tasks dir).

## 3. Cheapest falsifier — micro-rates MR era-split → **FALSIFIED**

Pre-registered kill rule frozen *before* scoring (see [`rates_era_split.py`](rates_era_split.py) docstring). Daily proxy for a 15m fade — tests the **regime / tail-co-occurrence** mechanism (the disqualifier), not the precise intraday bp. Data: Yahoo `^TNX` (10Y), `^FVX` (5Y), daily 2010-2026 (FRED/Stooq egress-blocked in-env).

**Regime check (confirmed):** 2022 10Y **1.63% → 3.88%** (max 4.23%, **+2.25pp**); 5Y 1.37% → 4.00% (+2.63pp). A violent one-directional selloff, not a range.

**Canonical fade (z=(y−SMA20)/SD20, fade |z|≥1, daily MR equity in bp):**

| Era | 10Y total | 10Y Sharpe | 5Y total | 5Y Sharpe |
|---|---:|---:|---:|---:|
| PRE 2010-2019 | +89 bp | **+0.22** | +118 bp | +0.31 |
| H1 2020→2023-03 | **−56 bp** | **−0.31** | **−91 bp** | **−0.47** |
| H2 2023+ | +15 bp | +0.10 | +197 bp | +1.10 |

**Worst year, both tenors = 2022** (10Y −124 bp / hit 44%; 5Y −116 bp / hit 43%).

- **K1 (tail co-occurrence) — FIRES.** The fade's worst year is 2022, squarely inside H1; H1 is net-negative on both tenors. The leg bleeds *exactly* when the trend book co-draws → it **deepens** the H1 co-drawdown rather than offsetting it (the Aegis-USDJPY-2022 bleed mode reproduced empirically on rates).
- **K2 (era-relabel) — does not fire** (PRE marginally positive), but no rescue: the PRE edge is Sharpe ≈ 0.22 (mean +0.067 bp/day) — economically **zero**, ≪ tradeable, let alone PF≈2.0.
- **Robustness:** H1/2022 negative across nearly the whole 3×3 grid; only `thr=1.5` (barely-trading, low-n noise) dodges 2022, and even there no cell delivers a meaningful PRE-positive AND H1-positive edge. No best-of-K rescue (and selecting that cell is the forbidden move).
- **Proxy caveat:** a daily proxy can't speak to a hypothetical pure-intraday edge that leaves no daily trace; but the disqualifier is regime-level (2022 trended at every timescale), so the kill transfers. A full intraday closure is data-gated (no rates 15m panel in-repo) but unwarranted given zero positive signal.

## 4. Last gap — dispersion / correlation-premium → **FALSIFIED** (venue + tail)

The one mechanistically-attractive chop-native family the 8 didn't score (sell index vol / buy single-name vol; harvest the implied-correlation premium that widens when constituents de-correlate). One-page venue falsifier (pre-registered: venue decisive, tail secondary):

- **Venue — INELIGIBLE (decisive), harder than short-vol.** Needs an *options book* (index + single-name). US futures-prop firms (Apex/Topstep/Bulenox) are **futures-only — no equity/single-stock options**. The only single-instrument proxy, **Cboe DSPX** (Sept-2023), is a benchmark index with **no listed tradable future/option**. Not a futures product at all.
- **Tail — WRONG-SIGN (mechanism-level).** Short-correlation harvest blows up when realized correlation spikes to ~1 in systemic risk-off (2008, Feb-2018, Mar-2020) = the same H1 risk-off window the book co-draws. (The "Assenagon did well in 2018/2020" cite is the *long*-vol hedged variant — opposite position.)

**Structural finding:** the entire **vol/correlation-risk-premium branch** (short-vol, dispersion, gamma-scalp, IV-calendar-spread) is uniformly venue-blocked because the **futures-prop venue is options-free** — and the CFE-accessible piece has the wrong-sign co-occurring tail anyway. The futures pivot opens the *cost* wall but specifically does **not** open the most-chop-native (vol-premium) branch.

## 5. Conclusion

Nine families considered (8 scored + dispersion), **0 viable** in the affordable universe (FXIFY CFD + futures-prop CME micros):

- **Vol/correlation-premium branch** (most chop-native): uniformly venue-blocked (options-free venue) + wrong-sign co-occurring tail.
- **Price-MR branch** (venue-eligible): each dies on cost (stat-arb, FX), anti-edge (intraday fade), era-relabel (metals), already-falsified (index reversal = NOCT-SPX), or era/tail co-occurrence (rates, §3).
- **Calendar/seasonal branch**: not chop-native by the generated-by-range definition + un-routable spreads / selection-envelope.

> **A regime-robust + orthogonal + affordable chop-native leg does not exist in this universe.** The futures pivot relaxed the cost wall but is options-free, so it did not open the vol-premium branch. Relief remains **exogenous/paid-data-procured** (the T1/T2 levers — paid dealer-gamma/options-flow, or more accrued co-drawdown episodes), **not idea-blocked**. Consistent with the standing 2026-06-07 HOLD; quarterly regime trigger **2026-08-08**.

## 6. Reproduce

```bash
cd lab/analysis/chop_native_leg_2026-06-30
python rates_era_split.py        # fetches ^TNX/^FVX from Yahoo if the JSON is absent (egress required)
```

Rejections recorded in [`docs/rejected_candidates.md`](../../docs/rejected_candidates.md): `rates-intraday-mean-reversion × Micro-10Y/2YY` and `index-dispersion-correlation-premium × SPX500`.
