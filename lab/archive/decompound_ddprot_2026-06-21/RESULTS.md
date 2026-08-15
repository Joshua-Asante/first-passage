# Decompound + dd_protection portfolio sim, and 5th-leg target spec (2026-06-21)

**Spawn of:** `CC-handoff_decompound-ddprot_5th-leg.md`. **Status: DONE_WITH_CONCERNS.**
**Scope:** research (`lab/`). Read-only on `core/`, canonical panels, the locked
anchor, `dd_protection` constants, and all manifests. No locked artifact modified.

This run reuses the LOCKED production primitives with **zero fork**:
`core/portfolio_mc.py` (`build_daily_panel` / `build_week_blocks` / `_run_seeds` /
`_simulate_path`), `core/dd_protection.py` (`DD_TRIGGER` / `DD_SCALE`), and the
existing decompounder `lab/analysis/decompound_remc_2026-06-07/decompound.py`
(`load_file` / `reconstruct_roe` / `rebank` / `run_mc`). Harness soundness gate:
`python -m pytest test_decompound.py -q` → **18 passed** incl. the REG byte-identity
gate that reproduces the locked **99.83 / 0.17 / 4.37** anchor.

---

## §0 — Rule 0: production values reported verbatim (from disk)

| item | value (disk) | source |
|---|---|---|
| `DD_TRIGGER` | **0.015** (1.5% from peak) | `core/dd_protection.py:52` |
| `DD_SCALE` | **0.40** | `core/dd_protection.py:53` |
| combine operator | **multiplicative** — `strat_pnls = path[day] * (0.40 if round(dd_from_peak,6) <= -0.015 else 1.0)`; **not** `min()` | `core/portfolio_mc.py` `_simulate_path` |
| MC termination | pass (`eq>=210k` & `trade_days>=5`) / bust_daily (`day_pnl<=-5%`) / bust_static (`eq-200k<=-5%`) / bust_inactivity (60 idle bdays) / horizon_cap (1500) | `core/portfolio_mc.py` `_simulate_path` |
| decompound transform | `roe_i = NetPnL_i / equity_before_i`, `equity_before_i = 200k + cum_USD_{i-1}`; **static** rebank = `roe × 200k` | `decompound.py` `reconstruct_roe` / `rebank` |
| allocations | guardian 0.0034 / striker 0.0070 / aegis 0.0150 / striker_nas100 0.0037 | `firm_rules._BASE_RISK` = `portfolio_mc.ALLOCATIONS` |

`dd_protection.py` git anchor: last touched in the 2026-06-06 firm_rules refactor /
housekeeping; constants unchanged since the 2026-05-08 C2 relock. The MVD spec-pin
in `_validate_protection_rule()` hard-asserts `DD_TRIGGER==0.015 and DD_SCALE==0.40`.

## §0.5 — ambiguities, all resolved from disk (no BLOCK)

1. **dd_protection config** — handoff said the skill cache claims 0.010; **disk and the
   current `fxify-challenge` skill both say 0.015 (C2)**. Used 0.015 / 0.40.
2. **CSV placement** — the four fresh exports are in `~/Downloads` (vendor-licensed,
   not committed); driver reads them directly. Full-history 2020-01 → 2026-06.
3. **Allocations** — `_BASE_RISK` matches the cited current lock; the stale
   `baselines.md` DJ30 1.00% / NAS 0.40% values were NOT used.
4. **Pyramid schema** — the new exports use the newer TV header (`Trade number` /
   `Net PnL USD` / `Cumulative PnL USD`) and represent pyramid adds as **separate
   Trade #s tagged "Add"** (e.g. DJ30 #14 `Long Add`, NAS #2/#4 `Long Add`).
   `_normalize_tv_columns` handles the header; `load_file` pairs one entry+exit per
   Trade #. Confirmed empirically.

**Discovery:** this exact decompounded full-history analysis was already executed on
**2026-06-07** (`lab/analysis/decompound_remc_2026-06-07/`, HOLD ADR
`docs/adr/2026-06-07-decompound-remc-hold.md`). The new exports are a 2-week-fresher
vintage of the same 2020-26 data and **reproduce it**, which both verifies provenance
and reframes the handoff's "compare to 99.83 ceiling" expectation.

---

## §2.1 — Reconcile (provenance + sanity; no HALT)

| leg | N | WR% | PF | comp$ | static$ | cmp× | DD% | medR$ | fs-mean$ | base-R% | dev | gate |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| Guardian | 317 | 17.7 | 2.78 | 492,109 | 259,493 | 1.90 | 9.16 | 689 | – | 0.345 | +1.3% | ok |
| Striker DJ30 | 269 | 71.4 | 3.20 | 422,727 | 237,957 | 1.78 | 9.88 | 1,408 | 4,035 | 0.704 | +0.6% | ok |
| Aegis | 149 | 58.4 | 3.56 | 195,032 | 139,565 | 1.40 | 6.37 | 620 | 2,994 | 1.497 | −0.2% | ok |
| Striker NAS100 | 288 | 55.9 | 3.68 | 529,723 | 269,123 | 1.97 | 5.37 | 746 | 4,390 | 0.373 | +0.8% | ok |

Base-risk gate uses **median |loss|** for Guardian/DJ30/NAS (base-entry proxy) and
**full-stop mean** for Aegis (BE strategy; median is BE-clipped). All four reconcile to
locked `_BASE_RISK` within ±1.3% → **no HALT**. The pyramid legs' full-stop mean is
add-inclusive ~2% (DJ30 2.02%, NAS 2.20%) — **expected, not a flag** (handoff §2.1).
Filenames carry correct strategy/version/broker/symbol tokens (no symbol mislabel).

**Consistency vs the independently-computed 2026-06-07 run** (decisive provenance):
Aegis **matches to the dollar** (0.0% — no new Aegis trades since 2026-06-07; last
trade 2026-05-19); DJ30 −0.7%, Guardian −3.8%, NAS +13.6% — all explained by the
2-week-fresher window (+8 Guardian / +5 DJ30 / +0 Aegis / +8 NAS recent trades).

## §2.2 — Decompound to fixed $200K base (static)

`build_daily_panel` scale factors are **1.000** on all four legs (FIXED_1R = alloc×200K
pins exactly), confirming the static streams are sized at the locked allocations.
Daily panel: **2020-01-06 → 2026-06-17, 1683 bdays / 336 week-blocks.**

**Aegis decompound verdict (handoff §1 reconcile item):** compounded Net $195,032 →
static-decompounded $139,565 (×1.40) — net **shrinks** under decompounding ⇒ Aegis
**compounded**, decompounding is **coherent**. The ~flat early-vs-late full-stop $loss
is the BE-manufactured small-loss distribution (median loss $620 ≠ 1R full stop $2,994),
**not fixed-lot sizing**. Matches the 2026-06-07 ×1.40 exactly.

## §2.3 — Combined equity curve: raw vs dd_protection  (primary deliverable)

`equity_curves.png` + `equity_series.csv`. Live C2 semantics (0.40× when
`round(dd_from_peak,6) ≤ −0.015`).

| curve | final $ | net $ | maxDD $ | maxDD % | RF | Calmar | maxDD window |
|---|--:|--:|--:|--:|--:|--:|---|
| RAW (static, no protection) | 988,194 | 788,194 | 21,687 | **8.63%** | 36.34 | 7.09 | 2021-10-20 → 2022-01-19 |
| dd_protection (C2) | 888,666 | 688,666 | 11,997 | **2.60%** | 57.40 | 20.55 | 2024-03-19 → 2024-05-29 |

**DD reduction 8.63% → 2.60% (+6.03pp, 44.7% of $DD).** Brake active **42.5%** of days
(715/1683). Per-leg $ at the protected trough (sums to −maxDD$, assertion-checked):
Guardian −6,224 / DJ30 −4,539 / Aegis −624 / NAS −610. dd_protection costs ~$100K of
6.5-yr upside (it throttles drawdown recovery) but halves the drawdown — the
conditional-brake tradeoff. Drawdowns concentrate in **2020-2022** (chop/crisis);
2023-2026 is near-monotone (benign trend) — the regime split, visible in the curve.

Supplement — banded withdrawal model (skim +5% to $200K, Joshua's real-life funded-phase
model): final $989,630, maxDD 8.38%. Banded ≈ static in the bootstrap once 1R is
normalized (confirms the 2026-06-07 "+0.00pp banding premium").

## §2.4 — Portfolio MC at the current lock (decompounded static streams)

| basis | pass | bust (daily/static) | p99 DD | median | gates |
|---|--:|--:|--:|--:|---|
| locked anchor (compounded 2022-26) | 99.83% | 0.17% (0.00/0.17) | 4.37% | 26 | **both clear** |
| 2026-06-07 S_2020 (decompound static) | 97.04% | 2.96% | 5.93% | 31 | both breach |
| **THIS run (decompound static 2020-26)** | **98.17%** | **1.83% (0.00/1.83)** | **5.50%** | **28** | **both breach** |

Bust attribution: guardian 30.3% / NAS 27.4% / striker 26.1% / aegis 16.2% (NAS
un-diluted from the locked anchor's 2.0% by full-history + decompounding, per
2026-06-07). **All busts are static-DD (grind-down clusters); 0.00% daily.** The
drift from the locked anchor is **expected and already characterized** by the
2026-06-07 HOLD ADR — driver order panel-length (5.5yr vs 52mo) > decompounding >
methodology. The slightly-better-than-S_2020 result is the 2-week-fresher benign window.
**Not re-baselined** (forbidden #3). Production MC block length is fixed at 5 (week-block)
— there is no native L parameter, so the §2.4-conditional L=8 variant is N/A without
forking the MC (declined per forbidden #1).

## §2.5 — Covariance, ENB, worst windows

**Correlations near zero** (all-day |ρ| ≤ 0.03; active-day-only up to −0.29 NAS/Aegis).
**ENB** (correlation form, bounded by 4): equal-weight **4.018**, locked-risk-weight
**2.848** (Aegis 1.50% concentration costs ~1.2 effective bets), as-traded div-ratio
**3.770**. Legs are already near-maximally diversified at the leg level — the smoothing
ceiling is set by weight/σ concentration, so a 5th **uncorrelated** leg raises the ceiling.

K=10 worst protected-curve drawdown windows (depth%, peak→trough):
the top 6 are all in **2020-2022** (2021-10→2022 4.94%; 2020-02→05 COVID 4.23%;
2021-01→07 4.02%; 2020-08→10 3.88%; 2022-08→12 3.13%; 2022-03→06 3.04%). These are
**risk-off / growth-scare** episodes in which the long-biased legs (long gold, long 2
equity indices, long USDJPY carry) **co-draw**. That co-movement — not any single leg —
is the binding portfolio-variance source.

## §2.6 — Synthetic 5th-leg target spec (NOT an instrument pick)

Parametric synthetic leg (clearly labelled; **no fabricated instrument CSV**), risk
**0.50% ADDED** (total 2.91% → 3.41%), ρ_stress = correlation to the 4-leg portfolio over
the 573 worst-window bdays. Controlled-Δ design (appending a column leaves n_blocks and
the per-seed block indices unchanged → identical resampled weeks, +5th leg only).

**Response surface — the dominant axis is standalone EDGE, not ρ_stress:**

Δp99 DD (pp; negative = better), avg over both active-day sets:

| PF tier ╲ ρ_stress | −0.6 | −0.3 | 0.0 | +0.3 |
|---|--:|--:|--:|--:|
| marginal (PF~1.1) | +0.77 | +0.28 | +0.27 | +0.32 |
| solid (PF~1.5) | +0.05 | +0.04 | +0.04 | +0.43 |
| strong (PF~2.0) | **−0.27** | −0.23 | −0.23 | −0.16 |

Δpass (pp):

| PF tier ╲ ρ_stress | −0.6 | −0.3 | 0.0 | +0.3 |
|---|--:|--:|--:|--:|
| marginal (PF~1.1) | −1.72 | −0.46 | −0.31 | −0.67 |
| solid (PF~1.5) | +0.18 | +0.26 | +0.19 | −0.75 |
| strong (PF~2.0) | **+0.74** | +0.85 | +0.80 | +0.60 |

* A **marginal-edge** leg HURTS even at ρ=−0.6 — the diversification benefit is swamped
  by the drag of adding capital-at-risk with weak edge.
* A **strong-edge** leg HELPS at every ρ (Δpass +0.6→+0.9pp, Δp99 −0.16→−0.33pp).
* **ρ_stress is a real but second-order effect** (~0.1–0.3pp), an order of magnitude
  smaller than the edge effect (~1pp marginal→strong).
* **0 / 24 cells restore both gates.** Best cells (strong edge) reach bust 0.89% (clears
  <1%) but p99 stays **5.17–5.19% (>5%, breached)**. 11/24 cap p99 below baseline 5.50%.
* **Risk-weight sensitivity** (ρ=−0.6/solid/ThuFri): 0.25%→p99 5.47 / 0.50%→5.71 /
  0.75%→6.02 — **more 5th-leg risk makes p99 WORSE** at the solid tier; only strong edge
  overcomes its own added capital-at-risk, and even then not below the 5% gate.

**Construction caveat (load-bearing):** the synthetic could not jointly realize *strong
edge* AND *strongly-negative ρ_stress* — the stress-forcing degraded realized PF, and
high-WR legs resisted the negative-correlation forcing (realized |ρ| < target for
high-edge cells). This is partly **inherent**: a leg that reliably prints green during
the portfolio's worst windows is, by that fact, earning return there (raising its PF),
so ρ_stress<0 and edge are **not independent knobs** for any real leg. The surface's
"edge dominates" finding partly reflects that the achievable (edge, ρ) region couples them.

**Minimum profile:** none at ≤0.75% risk restores both gates. The weakest helpful
profile (lifts pass, trims p99 below baseline) is **strong edge (PF~2.0), any ρ,
Thu/Fri fill** — but it leaves p99 > 5%.

**Copper-short mapping (memory's #1 candidate):** the worst windows are risk-off / growth
scares → a copper **short** prints green there → ρ_stress negative (−0.3..−0.6), and copper
trades the full week → can fill the thin **Thu/Fri** coverage. But the surface says a
negatively-correlated copper short only helps materially **if its standalone after-cost
PF is strong (~2.0)** — at marginal/solid edge it does not move p99 below the gate. That
after-cost PF≥~2.0 bar is what a real copper-short backtest must clear before it earns a
validation loop. Instrument selection remains a separate INQHIORI loop (forbidden #6).

## §2.6 regime-robustness (half-panel @ 2023-03-20) — best-case 5th leg

Profile: strong(PF~2.0)/Thu-Fri/ρ_stress −0.6 (the most-favourable cell; due to the
edge↔ρ coupling the forcing realized ρ −0.28 / PF 1.53). Gate per partition: bust<1% AND p99<5%.

| partition | config | pass | bust | p99 DD | median | gate |
|---|---|--:|--:|--:|--:|---|
| **H1 2020-2023** (chop/crisis) | 4-leg | 83.94% | 16.06% | 7.95% | 58 | FAIL |
| | + synth 5th | 85.31% | 14.69% | 8.00% | 53 | **FAIL** |
| **H2 2023-2026** (benign trend) | 4-leg | 99.67% | 0.33% | 4.76% | 18 | CLEAR |
| | + synth 5th | 99.65% | 0.35% | 4.80% | 16 | CLEAR |
| full 2020-2026 | 4-leg | 98.17% | 1.83% | 5.50% | 28 | fail |
| | + synth 5th | 98.30% | 1.70% | 5.52% | 26 | fail |

**The 5th leg does NOT clear the hard H1 regime.** It nudges H1 bust 16.06% → 14.69%
(−1.37pp) and pass +1.37pp and median 58→53d, but the **tail is untouched** — p99 even
ticks up (7.95 → 8.00) from the added capital-at-risk. The benefit is concentrated in the
average/median, not the tail. This is the **same failure shape** the 2026-06-07 ADR found
for static de-risk (k and dd_protection both failed H1) and Q-DDTRIG-1 found for the
dd-trigger lever (H1 bust 11.76%). The H1↔H2 asymmetry (bust 16% vs 0.33%, p99 7.95% vs
4.76%) is enormous: the portfolio is **regime-bound**, and a modest 5th leg is not a
regime-robust fix. Regime-adaptive sizing remains the only structural lever
(`docs/adr/2026-06-07-decompound-remc-hold.md` open Pre-Q).

---

## §2.6b — RISK-NEUTRAL insertion (constant total risk 2.91%) — follow-on to the ADD frame

The §2.6 ADD sweep raised total risk (2.91% → 3.41%), so the added capital-at-risk fought
the diversification (0/24 restored gates). Holding total risk **constant** — trim the four
legs by `k = (2.91% − w5)/2.91%`, slot the freed risk `w5` into the 5th leg (scaling a
static $-stream by k exactly models running the leg at k× its risk) — changes the picture.
Active days Thu/Fri; full / H1 / H2 partitions.

| config (total risk) | full pass/bust/p99 | full gate | H1 bust/p99 | H1 gate | median |
|---|---|---|---|---|--:|
| baseline 4-leg (2.91%) | 98.17 / 1.83 / 5.50 | breach | 16.06 / 7.95 | fail | 28 |
| de-risk-only k=0.828 (2.41%) | 99.20 / 0.80 / 4.99 | **CLEAR** | 11.24 / 7.70 | fail | 32 |
| de-risk-only k=0.656 (1.91%) | 99.79 / 0.21 / 4.54 | **CLEAR** | 6.28 / 7.06 | fail | 38 |
| insert strong-edge ρ0, w5=0.5% (2.91%) | 99.58 / 0.42 / 4.91 | **CLEAR** | 3.39 / 6.31 | fail | 27 |
| **insert strong-edge ρ0, w5=1.0% (2.91%)** | **99.71 / 0.29 / 4.82** | **CLEAR** | **1.50 / 5.85** | fail | **24** |
| insert solid-edge ρ−0.6, w5=1.0% (2.91%) | 96.72 / 3.28 / 6.46 | breach | 20.92 / 8.62 | fail (worse) | 35 |

1. **Risk-neutral insertion restores the full-panel gates** — 2/8 cells (both strong-edge,
   ~uncorrelated). The ADD frame got 0/24. **Constant total risk is what lets the leg help.**
2. **Marginal value over pure de-risk = pass SPEED.** De-risk-only also clears the full gates,
   but slowly (median 32–38d). The strong-edge insertion clears at the *same* safety with
   **median 24d** (w5=1.0%) — faster than even baseline's 28d. Redeploying freed risk into a
   profitable uncorrelated leg buys back the speed pure de-risking sacrifices. That cell
   **dominates baseline** (faster AND gates clear).
3. **H1 still unfixed by all 8 configs, but the strong-edge insertion is the closest approach
   in the entire investigation:** H1 bust **16.06% → 1.50%**, p99 7.95% → 5.85% (w5=1.0%
   strong-ρ0). It *beats* de-risk-only-k=0.656 on H1 (1.50% vs 6.28% bust) **despite carrying
   more total risk** — the leg's edge genuinely cushions the chop. Still misses (<1% / <5%).
4. **Edge is the binding requirement, again.** Forcing ρ=−0.6 collapses realized PF (the
   coupling) and backfires — w5=1.0% solid-ρ−0.6 makes H1 *worse* than baseline (bust 20.92%,
   realized PF 1.09). The winning profile is **strong edge + low (achievable) correlation**;
   ρ<0 is not separately purchasable.

**Caveat:** the winner assumes a 5th leg delivering **after-cost PF ≈ 2.0 with edge that
PERSISTS through the chop regime** — a high empirical bar (most legs' edge degrades in the
very regime that hurts the portfolio). That, not anti-correlation, is the real target for any
instrument search. Artifact: `fifth_leg_riskneutral.json`, `analyze_part4.py`.

---

## §4 — Falsifiable hypothesis: verdict

> §4 H: a 5th leg with ρ_stress ≤ −0.3, standalone PF ≥ ~1.5, Thu/Fri fill ⇒ portfolio
> p99 DD falls below the 4-leg value AND pass rises ≥ 0.10pp.

**NOT SUPPORTED as stated.** The exact specified cell (Thu/Fri, solid PF~1.5, ρ_target −0.3
→ realized ρ −0.38 / PF 1.32) gives Δpass −0.06pp (does not rise) and Δp99 +0.19pp (rises,
does not fall). More broadly, **ρ_stress is not the operative lever** — standalone edge is.
A strong-edge (PF~2.0) leg helps regardless of correlation; a weak-edge leg hurts regardless.
In the **ADD** frame no 5th leg restores the breached p99 gate (added capital-at-risk fights
the diversification). In the **RISK-NEUTRAL** frame (§2.6b, constant 2.91% risk) a **strong-edge,
low-correlation** 5th leg **does restore the full-panel gates AND buys pass-speed** (median
24d, dominating baseline) — so the slot *can* help, but via **edge at constant risk**, not via
ρ_stress. The binding open requirement is therefore an instrument delivering **after-cost
PF ≈ 2.0 with edge that persists through the chop regime** — a high empirical bar. The hard
H1 (2020-2023) tail is **not cleared by any static config** (ADD, de-risk, or risk-neutral
insertion); the strong-edge insertion only *approaches* it (H1 bust 16% → 1.5%). Regime-adaptive
sizing remains the only lever that could clear H1 outright (2026-06-07 ADR open Pre-Q).

## §6 — Status: **DONE_WITH_CONCERNS**

All of §2.1–§2.6 produced; combined curve (raw + protected) emitted with DD reduction;
MC reproduced within the documented decompound+window envelope of the 2026-06-07 anchor
(verified by the 18-gate REG byte-identity test); response surface + minimum-profile +
§4 verdict stated. **Concerns flagged:** (a) the §4 hypothesis is not supported and the
operative lever is edge, not ρ_stress; (b) the synthetic-leg construction cannot fully
decouple edge from ρ_stress (partly inherent), so the strong-negative-ρ region is
under-resolved; (c) the decompounded MC breaches both lock gates — consistent with the
2026-06-07 HOLD, **not a new finding and not a relock trigger**.

## §7 — self-review

* **Spec compliance:** §2.1–§2.6 all produced; no fabricated 5th-leg CSV (synthetic only);
  no parser/decompounder/MC re-derived (production reused, REG-verified); no locked anchor
  or constant edited; the banded curve + regime split are labelled supplements, not silent
  scope-creep.
* **Quality:** decompound transform = production static rebank; dd_protection semantics
  byte-match disk (`round(dd,6) ≤ −0.015 → ×0.40`); ENB corrected to the bounded
  correlation form; per-leg DD attribution assertion-checked to −maxDD$; MC reproduces the
  2026-06-07 decompounded basis.
* **Consolidated read (2.2→2.3→2.4→2.6):** the per-leg decompounded nets reconcile to the
  2026-06-07 table (Aegis exact); the protected-curve worst windows (§2.5) are the same
  risk-off episodes that drive the static-DD busts (§2.4); the §2.6 surface inherits the
  same panel — internally consistent.

## Reproduce
```
cd lab/analysis/decompound_ddprot_2026-06-21
python analyze_part1.py     # §2.1-§2.5 + equity_curves.png
python analyze_part2.py     # §2.6 synthetic 5th-leg sweep (joblib, 7 workers)
python analyze_part3.py -0.6 "strong(PF~2.0)" ThuFri 0.005   # regime split
# harness soundness:
cd ../decompound_remc_2026-06-07 && python -m pytest test_decompound.py -q
```
Inputs: the four 2026-06-21 Pepperstone exports in `~/Downloads` (vendor-licensed,
gitignored — not committed).
