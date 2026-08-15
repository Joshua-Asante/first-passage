**Theme:** legacy
**Status:** ACTIVE — Guardian Silver v1.0 allocation frontier + regime stress
# Guardian Silver v1.0 — allocation frontier + regime stress (2026-06-10)

**Question.** If Guardian Silver v1.0 (XAGUSD trend-rider + break-even @ 4.8≈3R) is
admitted as a 5th strategy: (a) what risk allocation minimizes portfolio bust and
maximizes median-days-shaved on the canonical MC, and (b) does that optimum survive
the 2026-06-07 decompound + regime-robustness correction?


> **Salvage provenance (2026-06-11).** Authored 2026-06-10 in the `kind-beaver-e659c3`
> worktree (uncommitted); salvaged onto the PR #169 branch on 2026-06-11 with path
> repoints only: `1bacc` → the manifest-pinned `..._7c8c2_be4.8.csv` (verified
> trade-identical: 239 exits, identical exit timestamps, prices, and P&L), and `11d4b`
> (2020-start, the sign-flipping export) now manifest-pinned at
> `core/data/tv_exports/pepperstone/`. The Pine source also surfaced from `~/Downloads`
> → main-checkout `core/strategies/candidates/guardian_silver_v1_0.pine` (gitignored;
> unpinned-candidate per the GBPUSD precedent); its defaults confirm the §Admission
> framing — `useBreakeven=false`, `beTriggerAtr=3.0` — so the lock candidate is a
> two-input delta (`true` / 4.8). Read alongside
> [`../../archive/guardian_silver_be_2026-06-10/RESULTS.md`](../../archive/guardian_silver_be_2026-06-10/RESULTS.md):
> the parent-session "+50.7% RF" BE-merit claim is falsified there against the true
> no-BE baseline, and BE-on/off is portfolio-invariant at ≤0.34% (that probe
> independently reproduces this file's be4.8 cells) — a future lock brief must argue
> BE on DD-repair/regime grounds, not the RF headline.
> `silver_regime_gate_full_2026-06-10.py` (formal Part-A bootstrap gate @ 0.15%) was
> authored in that session but its results are not recorded here — treat as NOT RUN
> until executed.

**Status.** EXPLORATORY, **conditional on Silver clearing admission** (feed-robustness
Dukascopy validation + a lock-decision brief are still pending; Silver's own handoff
scopes portfolio MC *out* until then). **Not a lock.** Zero `core/` mutation; reuses
the locked `portfolio_mc` machinery (`build_daily_panel`/`build_week_blocks`/`run_seed`),
which is already N-strategy-generic, and the 2026-06-07 decompound harness with zero fork.

---

## Admission (rejected-candidate re-proposal bar)

Silver-on-XAGUSD is a **rejected portfolio candidate** ([`docs/rejected_candidates.md`](../../../docs/rejected_candidates.md),
Q-CORR-1, 2026-05-14): re-proposal requires **new mechanism evidence**, not new
parameters. Guardian Silver v1.0 adds a **break-even exit @ `beTriggerAtr`=4.8 (≈3R)**
that Guardian-Gold v5.5 does *not* have (pure trend-rider, no BE). That BE mechanism
specifically repairs the 2022-2023 regime drawdown that drove the original Q-CORR-1.1
rejection (DD 11.52% > 8% cap), and is critical-trade-verified (Aug-2023 runner). Adding
a BE exit *class* to a pure trend-rider is a mechanism change → **clears the re-proposal
bar in principle**. Admission is not yet complete (validation + lock brief pending).

**CSV reconciliation (1bacc / 11d4b, Pepperstone XAGUSD, 2026-06-10):**
* `1bacc` (2022-01-20→2026-05-13): N=239, PF 2.864, WR 23.01%, compounded DD 4.95%, 1R $655.
* `11d4b` (2020-01-08→2026-05-13): N=369; its **2022+ subset is byte-identical to 1bacc**
  on compounding-invariant metrics (N=239 / PF 2.864 / WR 23.01%) → same v1.0 config,
  extended back to 2020. Net differs ($202K vs $231K) purely by compounding (2020-21 lost
  equity → smaller 2022+ sizing).
* **Silver 2020-2021 standalone: N=128, Net −$24,553, PF 0.539, WR 12.50%** — net-negative
  in the chop regime. This is the load-bearing fact.

---

## Verdict

1. **Compounded canonical 2022-26 panel — Silver 0.15-0.20% is a clean Pareto win.**
   0.15% improves *all four* axes vs the 4-strat baseline (bust 0.170%→0.103%, p99
   4.37%→4.32%, median 26→22d, pass 99.83%→99.90%). 0.20% shaves 5d at bust-neutral.
   Optimum is **well below** Guardian-Gold's 0.34% — the MC pricing in Gold↔Silver
   correlation (Silver's bust-share climbs to ~49% by 0.40%).
2. **The win survives decompounding on the *full* panel but NOT in the hard regime.**
   On decompounded 2020-26, Silver's net-negative 2020-2021 cohort raises the H1
   (2020-2023) bust **24.54% → 29.82% (0.15%) → 32.06% (0.20%)**. Silver **amplifies**
   the portfolio's existing regime-dependence (the 2026-06-07 HOLD) rather than
   diversifying it: it *helps* the benign H2 (bust 0.54%→0.40%) and *hurts* the chop H1.
3. **The 2020 data flips the sign.** With Silver from 2022-only, 0.20% *helped* H1 (bust
   24.54→22.86, velocity). With real 2020-start data it *hurts* H1 (→32.06). Extrapolating
   from the short panel would have inverted the conclusion (on-disk-artefact-can-be-wrong).
4. **Recommendation if admitted: 0.15% as a benign-regime velocity enhancer (fair-weather
   risk)** — first leg to de-risk/pause when the quarterly regime trigger (next 2026-08-08)
   flags chop. **0.20%+ is not defended**: it tips the full 2020-26 p99 *over* the 4-strat
   baseline (6.03% vs 5.93%) and adds most to the hard-regime bust. Silver is not a
   portfolio-strengthening diversifier; it buys speed in good regimes at the cost of
   amplifying the (already-managed) bad-regime tail.

---

## Method

* **Compounded sweep** (`silver_alloc_sweep.py`). Silver enters as a 5th panel column scaled
  by median-loss 1R (Guardian-family basis, $655). Silver's CSV window sits inside the
  canonical panel, so the 227 week-blocks are preserved (asserted). Gate: the 4-strat
  baseline reproduces the pinned anchor **99.83 / 0.17 / 4.37** before any Silver row.
* **Decompounded regime gate** (`../decompound_remc_2026-06-07/silver_regime_2026-06-10.py`).
  Reuses 2026-06-07 `stitch`/`rebank('static')` (roe = NetPnL/equity_before; static =
  roe×200K; 1R = alloc×200K exact). Silver decompounded the same way (native risk 0.262%,
  1R $525). Floor per partition = the two lock gates (bust<1% AND p99<5%). Half-panel split
  at the bday midpoint, per [`docs/methodology/regime_robustness_gate.md`](../../../docs/methodology/regime_robustness_gate.md).
  Gates: 4-strat reproduces **S_2022 99.16/0.84/5.00** and **S_2020 97.04/2.96/5.93**.

---

## Cells

### A. Compounded canonical 2022-26 (locked anchor basis)

| Silver risk | pass % | bust % | p99 DD % | median d | Ag bust-share |
|---:|---:|---:|---:|---:|---:|
| 0.00 (baseline) | 99.83 | 0.170 | 4.37 | 26 | 0% |
| **0.15** | 99.90 | **0.103** | 4.32 | 22 | 6.5% |
| 0.20 | 99.83 | 0.167 | 4.43 | 21 | 20.0% |
| 0.25 | 99.75 | 0.247 | 4.58 | 20 | 28.4% |
| 0.30 | 99.68 | 0.323 | 4.73 | 19 | 35.1% |
| 0.34 | 99.58 | 0.423 | 4.84 | 19 | 39.4% |
| 0.40 | 99.37 | 0.630 | 4.94 | 18 | 49.2% |
| 0.50 | 98.91 | 1.093 | **5.18** ✗ | 18 | 48.2% |

Median-days knee: 26→21 over baseline→0.20%, then flat (21→18) to 0.50%. Almost the
entire velocity benefit is captured by 0.20%; the last 3 days cost a 6× bust increase.

### B. Decompounded 2022-26 (Silver-complete; floor bust<1% AND p99<5% per partition)

| Config | Full | H1 2022-01→2024-03 | H2 2024-03→2026-06 |
|---|---|---|---|
| baseline | 99.16 / 0.84 / 5.00 ✅ | 97.26 / 2.74 / 5.70 ❌ | 99.76 / 0.24 / 4.58 ✅ |
| + Silver 0.15% | 99.31 / 0.69 / 4.96 ✅ | 97.50 / 2.50 / 5.67 ❌ | 99.83 / 0.17 / 4.44 ✅ |
| + Silver 0.20% | 99.23 / 0.77 / 4.97 ✅ | 97.33 / 2.67 / 5.77 ❌ | 99.80 / 0.20 / 4.54 ✅ |
| + Silver 0.25% | 99.13 / 0.87 / 5.00 ❌ | 96.92 / 3.08 / 5.85 ❌ | 99.76 / 0.24 / 4.66 ✅ |

The 4-strat baseline already FAILS H1 (the 2022 chop). Silver 0.15% improves the *full*
panel; 0.25% breaches it. H1 is failed by the portfolio regardless of Silver.

### C. Decompounded 2020-26 (full-history; Silver now spans the hard regime)

| Config | Full | **H1 2020-01→2023-03** | H2 2023-03→2026-06 |
|---|---|---|---|
| baseline | 97.04 / 2.96 / 5.93 ❌ | 75.45 / **24.54** / 8.57 ❌ | 99.46 / 0.54 / 4.87 ✅ |
| + Silver 0.15% | 97.25 / 2.75 / 5.88 ❌ | 70.18 / **29.82** / 8.85 ❌ | 99.60 / 0.40 / 4.80 ✅ |
| + Silver 0.20% | 96.91 / 3.09 / 6.03 ❌ | 67.93 / **32.06** / 8.93 ❌ | 99.57 / 0.43 / 4.83 ✅ |

Sign-flip evidence: with Silver from **2022-only**, 0.20% gave H1 = 77.14 / 22.86 / 8.56
(*helped*). With **2020-start** data, H1 = 67.93 / 32.06 / 8.93 (*hurt*). The 2020-2021
losing cohort (PF 0.539) is the difference.

---

## Interpretation

* **Three lenses, converging story.** Compounded-benign: Silver looks like a free lunch.
  Decompounded-benign: still a full-panel win, H1 (2022 chop) unfixed. Decompounded-2020:
  Silver *amplifies* the hard regime. The full-panel averages hide the regime split — the
  partition gate is what exposes it (recurring "full-panel masks regime split" lesson).
* **Silver fails the regime-robustness gate — but so does the locked 4-strategy portfolio**
  ([2026-06-07 HOLD](../../../docs/adr/2026-06-07-decompound-remc-hold.md)). Failing the gate
  is therefore not disqualifying *per se*; the question is whether Silver worsens the
  accepted tail. **It does** — modestly at 0.15%, meaningfully at 0.20%+.
* **2020-2021 representativeness is Joshua's judgment call** (same caveat as the 2026-06-07
  decision). If COVID-era chop is considered representative of forward risk, Silver is a net
  liability in the tail; if not, 0.15% is a benign-regime velocity gain.

## Feed-robustness (Dukascopy §2.3 critical-trade falsifier — 2026-06-10)

The BE @ 4.8 finding rests on the Aug-2023 runner (handoff §2.3). The strategy is
deterministic on the bars, so feed-robustness reduces to: does Dukascopy XAGUSD
serve the same price path? Pulled via `core/lib/dukascopy.py`
(`dukascopy_runner_check.py`); **no strategy execution** (none is available — see
residual gap below).

| quantity | TV/Pepperstone | Dukascopy XAGUSD M15 | divergence |
|---|---|---|---|
| 2023-08-17 entry-day range | entry 22.656 | 22.392 – 23.019 (entry inside) | — |
| day-1 adverse low | shallow dip | **22.392 (−1.17%)** | same shallow magnitude |
| run-up peak (08-23) | → 24.127 exit | **24.371** | +1.01% |
| exit-level (08-24 close) | 24.127 | **24.137** | **+0.04%** |

**Verdict: the §4 falsifier does NOT fire.** The runner reproduces (exit within ~0.01,
far under the >2R falsification threshold), and the day-1 adverse excursion is the same
shallow −1.17% — so the BE-arming mechanism (high trigger survives the dip, low trigger
exits) behaves identically on Dukascopy. §2.5 class: **mechanical** (spread-level), not
signal. The most likely feed-artifact kill-path for the BE finding is **retired**.

**Multi-regime feed-equivalence (RF-run substitute, `dukascopy_feed_equiv.py`).** No
Guardian-family executor exists in-repo, so RF(4.8)/RF(baseline) can't be recomputed on
Dukascopy directly. But the strategy is deterministic on the bars: if Dukascopy serves
equivalent bars, the trades (and RF) transfer by construction. Test = do Silver's actual
Pepperstone trade prices (1bacc) fall inside the Dukascopy daily bar ranges, across regimes?

| window | regime | Silver legs | inside Duka daily range |
|---|---|---:|---:|
| 2022-01-10→02-05 | chop | 6 | **6/6** |
| 2025-03-01→03-25 | trend | 4 | **4/4** |
| 2023-08 runner | (above) | 1 trade | exit match 0.04% |
| **total** | 3 regimes | **10 legs** | **10/10 = 100%** |

Daily-range containment is robust to the EDT/UTC export-timestamp ambiguity (NY-session
trades are mid-day in both). **100% across 2022-chop / 2023 / 2025-trend → the feeds are
equivalent at the bar level across regimes → the BE @ 4.8 finding (and the whole strategy)
transfers.** This is as far as feed-robustness goes without an executor.

**Residual (narrowed):** a *bit-exact* full-panel RF recomputation would still need a
strategy run (executor or Joshua TV second-feed export) or a full 15m-exact OHLC
equivalence (needs Pepperstone XAGUSD bars, not on disk) per
[`docs/spec/feed_equivalence_discovery_test_LOCKED.md`](../../../docs/spec/feed_equivalence_discovery_test_LOCKED.md).
But the load-bearing falsifier passed and bar-equivalence holds across regimes, so the
feed-artifact risk is effectively retired; the residual is rigor, not a live threat.

## Recommended next steps (not executed)

1. Finish Silver admission: Dukascopy feed-robustness validation (its open handoff) → lock
   brief → formal 5-strategy re-MC. Only then is an allocation a lock, not decision-support.
2. If admitted, **0.15%** with an explicit regime-pause rule (de-risk first on the quarterly
   trigger). Re-run this gate as part of the lock with Part A (6-month block bootstrap n=100),
   not just the deterministic half-panel.
3. Consider whether Silver is better deployed only as a *regime-adaptive* leg — consistent
   with the 2026-06-07 "regime-adaptive sizing is the only viable structural fix" finding.

## Reproduce

```
# A — compounded allocation sweep (reproduces 99.83 baseline, then sweeps Silver)
python lab/analysis/silver_regime_2026-06-10/silver_alloc_sweep.py

# B/C — decompounded regime gate (reproduces S_2022 + S_2020, then Silver rows)
#   needs the 6 2020-start canonical exports in inputs/ (gitignored; from Downloads)
python lab/analysis/decompound_remc_2026-06-07/silver_regime_2026-06-10.py
```

Silver CSVs: the be4.8 export is pinned at `core/data/tv_exports/pepperstone/` as
`..._7c8c2_be4.8.csv` (trade-identical to the session's original `1bacc`); the
2020-start `..._11d4b.csv` is pinned alongside it. The decompound `inputs/` CSVs
stay gitignored (restore from Downloads / the kind-beaver worktree). Exploratory
`lab/` artifact — does not modify `core/`, the canonical panels, the locked anchor, or any
manifest.
