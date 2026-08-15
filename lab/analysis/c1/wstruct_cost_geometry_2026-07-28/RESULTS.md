**Theme:** c1
# WSTRUCT-M2K-1 cost geometry — measured M2K weekly scales and the deployable cost law

**Status:** **ACTIVE** -- corrects WSTRUCT-M2K-1 §2.2 on cost; asymmetric-payoff frontier is OPEN but harvest returns 0 seeds (modality-barred)

**Verdict:** `COST-LAW FAIL at every E1-compliant round-trip count on the directionally honest scale.`

**What this is.** Instrument characterization: M2K's measured weekly range/move geometry and the
`hurdle_4x` cost law recomputed at the panel-era median price. It replaces the *illustrative*
figures in [`WSTRUCT-M2K-1`](../../../docs/briefs/rnd-pipeline/WSTRUCT-M2K-1-weekly-structure-component-confirm-scoping.md)
§2.2 with measured ones, as that brief's own M-20 note requires.

**What this is NOT.** It does **not** test the W structure on M2K. No hit-rate is measured here,
no edge is scored, **no K is consumed and no manifest is opened** — measuring a price-range
distribution is not a selection-shaped look at edge. The 2024+ reserved holdout is untouched
(panel ends 2023-12-29).

Reproduce: `python lab/analysis/wstruct_cost_geometry_2026-07-28/wstruct_cost_geometry.py`
(research venv; reads the cached `C1-3LEG-MAP` chunks, no pull).

---

## §1 — Two errors in WSTRUCT-M2K-1 §2.2, compounding in the same direction

§2.2 concluded *"the cost wall ... is **not binding** at weekly frequency"* from
`~10 bp hurdle vs 100-300 bp weekly range = 10-30x margin`. Both halves are wrong:

**(a) It compares the hurdle to the price RANGE, not to the EDGE.** Under the brief's own model
(§2.4: hit-rate 0.5571, symmetric payoff) the expected edge is `(2p-1) x move = 0.1142 x move`
— **11.4%** of the scale, not the scale. That alone overstates margin ~8.8x. §2.4 does the
Sharpe-space arithmetic correctly (per-trade 0.114) but never converts to bp and compares it
against the hurdle.

**(b) It costs the RESEARCH expression, not the deployable one.** `ops/prop_envelope_default.md`
§2 item 1 requires, verbatim, *"cost hurdle computed at the deployable expression's round-trip
count."* E1 forbids overnight **and** weekend holds, so a weekly thesis decomposes into
per-session round trips — 5/week, or 2/week if restricted to Wed+Thu — never 1.

This is the failure mode the harvest doctrine names as **Requirement 5 / the same-units
attestation rule** (ADR 2026-07-16), recorded there as having already killed **D5** and
**H-OD-1** at Stage-2 cost-law: *"§R argued Sharpe-space against the Stage-6 floor instead of
simulating the bp-space cost gate."*

## §2 — Measured M2K geometry (2019-05-06 -> 2024-01-01, 243 weeks, 1,540,356 1m bars)

| scale | p25 | median | p75 |
|---|---:|---:|---:|
| weekly RANGE (hi-lo) | 313.4 | **425.7** | 589.7 bp |
| weekly \|MOVE\| (open->close) | 83.8 | **181.9** | 314.0 bp |
| Wed+Thu sum of \|intraday move\| | 93.7 | **157.3** | 259.5 bp |

Wed+Thu reachable / weekly range, median ratio: **0.382**.

**Panel-era median price 1,897.20** -> `hurdle_4x` = **11.89 bp per round trip**
(Tradeify $0.91/side, 1 tick/side). The brief's illustrative 9.81 bp was ~17% low.

Note the range correction cuts **for** the brief: M2K's real weekly range (425.7 bp) is well
above the illustrative 100-300 bp. But range is not the scale a directional bet captures.

## §3 — Cost law at the deployable round-trip count

`E[edge] = 0.1142 x scale`, compared against `n x hurdle_4x`. Ratio >= 1.00 clears
(the 4x multiple is already inside `hurdle_4x`).

| scale used | E[edge] | 1 RT *(weekly hold -- E1 FORBIDS)* | **2 RT (Wed/Thu)** | 5 RT (E1 daily) |
|---|---:|---|---|---|
| weekly RANGE, median | 48.6 bp | 4.09x PASS | 2.04x PASS | 0.82x **FAIL** |
| weekly RANGE, p75 | 67.3 bp | 5.66x PASS | 2.83x PASS | 1.13x PASS |
| weekly \|MOVE\|, median | 20.8 bp | 1.75x PASS | **0.87x FAIL** | 0.35x **FAIL** |
| Wed+Thu reachable, median | 18.0 bp | 1.51x PASS | **0.76x FAIL** | 0.30x **FAIL** |
| Wed+Thu reachable, p75 | 29.6 bp | 2.49x PASS | 1.25x PASS | 0.50x **FAIL** |

**The 2-RT decomposition shrinks the edge, not just the cost.** A Wed/Thu-only expression can
only reach the Wed+Thu portion of the weekly move (38.2% of range at the median) — so halving
the round trips does not halve the problem.

## §4 — Verdict

**No robust 1-2 RT/week expression exists.**

- **1 RT/week** clears on every scale (1.51x-5.66x) — and is exactly the weekly hold **E1
  forbids**. It is not a deployable expression at any FRIENDLY firm.
- **2 RT/week (Wed+Thu)** fails at the median week on both directionally honest scales
  (`|move|` 0.87x, Wed+Thu-reachable 0.76x). It clears only at p75 (1.25x) — i.e. only in
  above-median weeks, which cannot be selected ex ante. A gate that passes only on the good half
  of the sample is not a gate.
- **5 RT/week** fails everywhere except the range-p75 cell, which is the least honest scale.

**Consequence for WSTRUCT-M2K-1:** §2.2's "cost is not binding" is withdrawn. The candidate does
not have a deployable expression that clears the 4x cost law, so a pre-registration should not be
authored against it as written. **M2K's K bank (0, floor 0.650, the widest in the repo) is
NOT spent** — this closed at $0.00 and zero K, before any `register_search open`.

**What would reopen it:** an expression whose captured edge is a materially larger fraction of
the move than `(2p-1)` implies — i.e. asymmetric payoff (structure predicts *direction* and the
exit captures more than it risks), not a re-tune of the round-trip count, the day set, or the
instrument. That is a **new mechanism claim** requiring its own warrant, not a rescue of this one.

## §5 — Scope honesty

- The `(2p-1)` edge model is **WSTRUCT-M2K-1's own** (§2.4, symmetric payoff); it reproduces that
  brief's stated per-trade Sharpe of 0.114, so it is not a stricter model imposed from outside.
- The 0.5571 hit-rate is the **US500** figure. Whether it transfers to M2K is exactly what the
  proposed campaign would have tested and is **not** established here. This analysis shows the
  campaign fails on cost *even granting the borrowed hit-rate in full* — which is the cheaper
  falsifier, and the reason it runs first.
- Wed+Thu "reachable" is the sum of two sessions' `|open->close|` moves — an **upper bound** on
  what a 2-RT decomposition could capture, so 0.76x is already generous.

---

## §6 — Asymmetric-payoff frontier (added 2026-07-28)

§4 named the one reopening route: an expression whose captured edge exceeds what `(2p-1)`
implies — i.e. **asymmetric payoff** (stop `L`, target `R x L`, hit-rate `p`). Then
`E = L x (p*R - (1-p))`, and the cost law needs `E >= n x hurdle_4x`.

Required payoff ratio `R`, at `hurdle_4x` = 11.89 bp (measured median price 1,897.20):

| stop `L` | risk/contract | **1 RT/session** p=0.30 / 0.35 / 0.40 / 0.50 | **2 RT/session** p=0.30 / 0.35 / 0.40 / 0.50 |
|---|---:|---|---|
| 25 bp | $24 | 3.92 / 3.22 / 2.69 / 1.95 | 5.50 / 4.58 / 3.88 / 2.90 |
| 50 bp | $47 | **3.13 / 2.54 / 2.09 / 1.48** | 3.92 / 3.22 / 2.69 / 1.95 |
| 75 bp | $71 | 2.86 / 2.31 / 1.90 / 1.32 | 3.39 / 2.76 / 2.29 / 1.63 |
| 100 bp | $95 | 2.73 / 2.20 / 1.80 / 1.24 | 3.13 / 2.54 / 2.09 / 1.48 |

**The arithmetic is OPEN.** At 1 RT/session with a 50 bp stop, `R >= 2.09` at `p = 0.40` or
`R >= 3.13` at `p = 0.30` — ordinary breakout/trend profiles (the locked Guardian leg runs
WR 22.17% at PF 3.750). **Cost is not the wall for an asymmetric expression**, unlike the
symmetric case in §3.

**R1 is not the wall either.** A 50 bp stop risks **$47/contract**; the Stage-2 measured
1-contract sigma ceiling is $125/day, so stop geometry sits well inside R1.

## §7 — Harvest verdict: 0 screenable seeds (2026-07-28)

With cost and R1 both open, the binding constraint is **modality**, and it closes every route
searched.

**M2K's own ledger carries a BINDING CLASS BAR.** `ops/instruments/M2K.md` **M1** —
`index-intraday-ohlcv-directional-timing-2026-07-21`.

> **⚠ RAISED-BAR TEXT CORRECTION 2026-07-29.** The paragraph that originally sat here quoted
> M1 as "origin OPENPRESS-1" with addback *"new modality / mechanism evidence — NOT an RV
> threshold…"* / *"instrument rescue on same OHLCV."* That text is the **OPENPRESS-1 candidate**
> re-proposal bar, miscopied onto the domain bar id (same defect as WSTRUCT-M2K-1 §3.4(a);
> SLR-MYM-1 §2.7.1 "Separate ledger defect"). Canonical owner:
> [`docs/rejected_candidates.md`](../../../docs/rejected_candidates.md) §RAISED BAR 2026-07-21 —
> three-route disjunction (mechanism outside {price, instrument-selection, hold-time} **OR**
> different modality/venue **OR** beats ORB-MNQ net-of-cost). Origin = 2026-07-21 programme
> audit, not OPENPRESS-1. M2K.md **M1** is corrected to match. The route table below was scored
> against the non-canonical paraphrase; its harvest verdict (0 seeds / modality wall) is
> **unchanged** because WSTRUCT itself already died on cost-law before any seed spend — but
> future M1 scoring must use the three-route test.

| route | verdict | why |
|---|---|---|
| OHLCV breakout / trend (the natural asymmetric profile) | **BARRED** | M1 (as then paraphrased: "instrument rescue on same OHLCV"). Independently corroborated below. Under the canonical three-route test this row is a *candidate for route-1/3 scoring*, not an automatic OPENPRESS-style rescue kill — preserved as scored-at-the-time. |
| Russell annual reconstitution | **FAIL Req 2 + Req 4** | Cohort is *stocks, cross-sectionally* (additions vs deletions), not an RTY-futures directional δ/σ — transplanting it is the forbidden move. And it is **annual**: N ≈ 5 over the panel, confirm-power ≈ 0. Evidence base 1996–2002 / 1979–2004, heavily decayed. |
| Options-derived (gamma / GEX) | **already FALSIFIED + procurement-blocked** | Q-ORB-GEX-1 on NAS100: indicator-t **−0.58** after partialling gap + OR-range ⇒ "GEX is a vol/gap proxy". Paid data also hits the no-buy-before-survivor rule. |
| Cross-index relative-volume selection (incl. RTY) | **already REJECTED** | `docs/rejected_candidates.md` 2026-07-21 — selection *dilutes* edge; strictly dominated by incumbent ORB-MNQ. |
| Overnight / session-boundary | **E1-forbidden** | No overnight or weekend holds at any FRIENDLY firm. |

**External corroboration of M1 (new, verified this session).** Mathias Mesfin, *"Structural
Limits of OHLCV-Based Intraday Signals in MNQ Futures: A Systematic Falsification Study"*
([arXiv:2605.04004](https://arxiv.org/abs/2605.04004), submitted 2026-05-05, revised
2026-07-13): **14 signal families**, 947 trading days of 5-minute data (2021–2025), walk-forward
OOS, |t| ≥ 2.0, ≥30 trades. Gross edge **0.07–1.50 points/trade**; a fixed **2-point round-trip**
eliminates it in every case. **None** of the fourteen satisfied all criteria — and **two positive
controls confirmed the methodology detects genuine edge**, so this is a real null, not a power
failure. An independent 2026 study reaching our own class bar's conclusion on the sibling
instrument. It does **not** cover RTY, so it cannot supply the Russell-specific δ/σ Requirement 2
demands — it corroborates the bar without lifting it.

**Verdict: `0 SCREENABLE SEEDS`.** No `register_search open`, no manifest, no K, no pull, $0.00.
**M2K's bank remains 0** (floor 0.650, the widest DSR headroom in the repo, still spendable
exactly once).

**What would constitute a seed:** a mechanism that is (a) **non-OHLCV in modality** or carries
genuinely new mechanism evidence, (b) **cohort-cited on Russell/RTY itself** — no transplant from
ES/SPX/NQ, (c) at **daily-or-finer event frequency** so confirm-power ≥ 0.50 is reachable at
N ≈ 450, and (d) asymmetric enough to clear §6's frontier. All four, not a subset. Nothing found
this pass meets even two.
