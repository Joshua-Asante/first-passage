**Theme:** regime
**Status:** ACTIVE — decompounded full-history MC breaches both lock gates
# Portfolio MC reevaluation — decompounded, full-history (2026-06-07)


**Question.** Re-evaluate the 4-strategy portfolio MC anchor (locked **99.83% pass /
0.17% bust / 4.37% p99 DD**, Pepperstone 2022–26 compounded) using (a) the full
available 2020-01 → 2026-06 Pepperstone BT-OFF + daily-cap exports and (b)
decompounding — withdraw every +5% profit and reset the base to $200K (Joshua's
"banded skim" model).

**Verdict.** Under both corrections the portfolio **breaches both lock gates**:
**97.08% / 2.92% / 5.93%** (banded, 2020–26). Bust > 1% and p99 DD > 5%.

This is a research artifact in `lab/`. It does **not** modify `core/`, the canonical
panels, the locked anchor, or any manifest. No relock is implied without a separate
approved ADR.

---

## Method

* **Decompounding (lossless).** Each export is an independent $200K run; cumulative
  P&L is off the $200K base. Per-trade return-on-equity `roe_i = NetPnL_i / (200K +
  cum_USD_{i-1})` is sizing-invariant (= risk% × R). Re-banking `roe` recovers the
  original NetPnL to **$0.000000** max error (round-trip test, all 4 strategies).
* **Re-bank modes.** `compounded` = original NetPnL; `static` = roe × 200K;
  `banded` = roe × running-equity, skim to $200K on touching $210K.
* **MC.** Reuses locked `portfolio_mc.build_daily_panel / build_week_blocks /
  _run_seeds / _simulate_path` with zero fork (DD_TRIGGER/SCALE = C2, SEEDS =
  (42,123,2026), 10k×3). Decompounded cells pin 1R = alloc × 200K (exact on clean
  data; avoids the `implied_1r` full-stop-cohort fallback that fires on decompounded
  DJ30 where |loss| ≈ 0.70% < the 1% full-stop floor).
* **Stitching.** Guardian = 2 files concatenated (clean 2020-07 seam). DJ30 = 2
  files, **3 overlapping 2022-03-15/18 trades deduped**. Aegis/NAS single file.
  Counts: Guardian 309 / DJ30 264 / Aegis 149 / NAS100 280.

### Harness fidelity (gate, passed before trusting any number)
* REG byte-identity: driver fed the **canonical** panels (adaptive 1R) reproduces
  `compute_default_config` exactly and the CLAUDE.md headline **99.83 / 0.17 / 4.37**.
* Export consistency: new export's Guardian **2022+** compounded = N=204 / WR 22.1% /
  PF 3.70 / Net $565,274 vs published baseline N=203 / WR 22.2% / PF 3.75 /
  Net $571,841 (within ~1%). The 309-vs-203 count gap is **purely the 2020–21
  window**, not a BT-mode population difference.

---

## MC cells

| cell | window | n_bd | n_blk | pass | bust | p99 DD | p95 DD | median |
|------|--------|------|-------|------|------|--------|--------|--------|
| **canonical** (locked) | 2022–26 | 1141 | 227 | 99.83% | 0.17% | 4.37% | 3.45% | 26 |
| C_2022 (compounded, adaptive) | 2022–26 | 1151 | 229 | 99.80% | 0.20% | 4.43% | 3.48% | 26 |
| C_2020 (compounded, adaptive) | 2020–26 | 1672 | 334 | 98.22% | 1.78% | 5.48% | 4.58% | 36 |
| S_2022 (decompounded static) | 2022–26 | 1151 | 229 | 99.16% | 0.84% | 5.00% | 4.17% | 22 |
| S_2020 (decompounded static) | 2020–26 | 1672 | 334 | 97.04% | 2.96% | 5.93% | 4.86% | 31 |
| **B_2020 (decompounded BANDED)** | 2020–26 | 1672 | 334 | **97.08%** | **2.92%** | **5.93%** | 4.87% | 31 |

`C_2020` shows that **just adding 2020–21 under the existing (compounded) methodology
already breaches both gates** (1.78% / 5.48%).

### Attribution
| step | comparison | Δ bust | Δ p99 DD |
|------|-----------|--------|----------|
| export consistency | C_2022 vs canonical | +0.03pp | +0.06pp |
| **decompounding** (clean isolation) | S_fixed vs C_fixed, 2022+ | +0.63pp | +0.51pp |
| fixed-vs-adaptive (sub-effect) | C_fixed vs C_adaptive, 2022+ | +0.01pp | +0.06pp |
| **window** (clean: both static) | S_2020 vs S_2022 | +2.13pp | +0.93pp |
| banding premium | B_2020 vs S_2020 | −0.05pp | +0.00pp |
| **HEADLINE** | **B_2020 vs canonical** | **+2.75pp** | **+1.56pp** |

* **Window (2020–21) is the largest driver.** It adds genuinely bad COVID-era blocks
  *and* more tail diversity (334 vs 227 week-blocks).
* **Decompounding is a real secondary effect** (+0.51pp p99, not a normalization
  artifact — fixed-vs-adaptive is only +0.06pp). Compounding let early/low-equity
  trades ride at sub-target size, flattering the bootstrap.
* **Banded ≈ static in the bootstrap** (+0.00pp). The withdrawal model's bite is on
  the standalone equity-curve DD, not the risk-normalized MC. (Confirms the session
  pre-decision: banded vs pure-static is immaterial once 1R is normalized.)

### Bust attribution (headline B_2020)
guardian 30.9% / striker 28.9% / **striker_nas100 23.4%** / aegis 16.8%.
NAS100's bust share jumps from **2.0%** (canonical) to **23.4%** — decompounding +
full-history un-dilutes its 1000%-pyramid stack risk (worst legs −6.5R to −7.6R).

---

## Per-strategy (decompounded to $200K base, 2020–26)

| strat | N | WR | PF cmp→dec | Net cmp → dec | compounding × | DD flat / banded | worst trade |
|-------|---|----|-----------|----|----|----|----|
| guardian | 309 | 17.2% | 2.99 → 2.53 | $553,828 → **$269,651** | 2.05× | 9.58% / 9.58% | −1.3R |
| striker DJ30 | 264 | 70.8% | 3.00 → 2.61 | $441,428 → **$239,729** | 1.84× | 9.03% / 9.03% | −5.0R |
| aegis | 149 | 58.4% | 3.56 → 3.18 | $195,032 → **$139,565** | 1.40× | 6.12% / 6.54% | −1.1R |
| striker NAS100 | 280 | 54.6% | 3.11 → 2.90 | $423,063 → **$236,899** | 1.79× | 5.18% / 6.42% | −7.6R |

* **Compounding inflates headline Net 1.4–2.05×.** Guardian's "$571K" is ~$270K on a
  real $200K-base account that withdraws profit.
* **Per-strategy full-history DD on a flat $200K base is ~2× the compounded-curve
  DD** (Guardian 9.6% vs the published 5.01%). These are *long-run* stats, not
  single-challenge metrics (a challenge is a short sprint to ±5%), but they show how
  much compounded backtests understate the DD a real prop account experiences.
* **Withdrawal can *raise* DD** (NAS banded 6.42% > flat 5.18%): skimming the profit
  cushion leaves a later losing streak closer to the bust floor. Relevant to the
  funded phase, not the pass/bust MC (which resets at +5% anyway).

### Data cleanliness
Worst DJ30 trades (−5.0R) are pyramid-stack stop-outs clipped by the daily cap at
~−3.5% roe, recurring in 2023/24/25 (not a 2020 glitch). NAS worst (−6.5 to −7.6R)
are 1000%-pyramid unwinds across 2020/21/23. Worst portfolio single days (~−2.7%,
inside the −5% daily limit) are spread 2020/23/24/25 → busts are static-DD clusters,
not single-day events.

---

## Interpretation & recommended next steps (not executed)

1. **The locked 99.83/0.17/4.37 is correct for what it measures** (2022–26 compounded
   bootstrap) but **optimistic** as a forward risk estimate: it excludes 2020–21 and
   carries the compounding dilution.
2. **The 2022-vs-2020 window is a genuine judgment call** (regime representativeness)
   and is Joshua's to make. Including all available history is the more conservative /
   honest default and is what breaches the gates.
3. **If 2020–26 + decompounding is accepted as canonical**, the portfolio needs
   **de-risking** (lower allocations and/or a tighter dd_protection) to restore
   bust < 1% / p99 DD < 5%. That is a **separate lock decision** — ADR + the
   superpowers/brief-authoring chain, per `test_lock_criteria` ("do NOT bypass this
   check by tweaking constants"). NAS100 (0.37%, pyramid 1000%) and DJ30 (0.70%,
   pyramid 750%) are the marginal contributors to target first.
4. Offered follow-up: a decompounded **allocation de-risk sweep** (reuse
   `mode_alloc_sweep` machinery on these streams) to find the gate-clearing frontier.

## De-risk sweep (Joshua accepted 2020-26 + decompounding as canonical, 2026-06-07)

Goal: restore bust < 1% AND p99 DD < 5% on the decompounded 2020-26 streams. Mechanics:
linear rescale via the stream's native 1R = LOCKED_alloc × 200K (banding premium ~0, so
the path-independent static streams are used — exact).

**Uniform de-risk** (scale all four allocations by k):

| k | G/DJ/A/N % | Σrisk | pass | bust | p99 DD | median | gate (p99 margin) |
|---|---|---|---|---|---|---|---|
| 1.00 locked | .34/.70/1.50/.37 | 2.91% | 97.04% | 2.96% | 5.93% | 31 | **fail** |
| 0.75 | .25/.53/1.12/.28 | 2.18% | 99.17% | 0.83% | 5.05% | 38 | fail |
| 0.70 | .24/.49/1.05/.26 | 2.04% | 99.41% | 0.59% | 4.94% | 41 | PASS (+0.06, thin) |
| 0.65 | .22/.46/.97/.24 | 1.89% | 99.63% | 0.37% | 4.83% | 42 | PASS (+0.17) |
| 0.60 | .20/.42/.90/.22 | 1.75% | 99.79% | 0.21% | 4.62% | 45 | PASS (+0.38) |
| **0.55** | .19/.39/.83/.20 | 1.60% | 99.87% | 0.13% | 4.33% | 47 | **PASS (+0.67)** |
| 0.50 | .17/.35/.75/.18 | 1.46% | 99.92% | 0.08% | 4.09% | 52 | PASS (+0.91) |

**Targeted** (keep Aegis ~full — PF 3.18, lowest bust share; cut fat-tail DJ30/NAS + low-PF Guardian):

| config | G/DJ/A/N % | Σrisk | pass | bust | p99 DD | median | p99 margin |
|---|---|---|---|---|---|---|---|
| TA aegis-keep | .20/.46/1.42/.20 | 2.28% | 99.55% | 0.45% | 4.91% | 41 | +0.09 |
| TB anti-spike | .19/.49/1.42/.18 | 2.28% | 99.56% | 0.44% | 4.92% | 42 | +0.08 |
| TC mild-target | .22/.49/1.50/.22 | 2.43% | 99.35% | 0.65% | 4.98% | 37 | +0.02 (noise) |
| TD pyramids-cut | .24/.42/1.42/.18 | 2.26% | 99.46% | 0.54% | 4.93% | 40 | +0.07 |

**Finding: targeting buys little.** Configs that keep more total risk (TC 2.43%, TA 2.28% vs
uniform k=0.65 1.89%) pass a few days faster but carry proportionally **thinner p99 margins**
(TC +0.02pp is inside MC noise). The binding constraint is **portfolio-level p99 DD — drawdown
clustering / co-movement across all four strategies**, which redistribution does not relieve
efficiently. Uniform de-risk is near-optimal and avoids the overfit/justification burden of a
bespoke allocation shape on a single 2020–26 sample.

### Recommendation (a frontier, NOT a relock)
* **Robust choice — uniform k≈0.55** (G 0.19 / DJ 0.39 / A 0.83 / N 0.20): 99.87 / 0.13 / 4.33,
  p99 headroom +0.67pp ≈ the original lock's +0.63pp. Median 47d.
* **Lighter de-risk — k=0.60–0.65** if a tighter margin is acceptable for faster pass (45/42d).
* **Cost of correctness:** median pass-time 26 (original locked basis) → 31 (corrected, at
  locked risk) → ~45–47 (de-risked). Slower challenges are the price of the honest risk picture.
* **Untested cheaper lever:** tightening `dd_protection` (a *conditional* brake that only costs
  during drawdowns) may cut tail DD with less median-pass penalty than flat allocation cuts —
  worth a sweep before finalizing allocations.
* **Process:** a relock is an **ADR + the mandatory regime-robustness gate** (half-panel split +
  6-mo block bootstrap, per `docs/methodology/regime_robustness_gate.md`) + an OANDA cross-check.
  The p99 margins here are near the MC noise floor; do **not** pick a `k` off this table and edit
  constants directly (`test_lock_criteria`).

## dd_protection lever (the cheaper, conditional brake)

**Structural finding: 100% of busts are static-DD (cumulative grind-down clusters); daily
busts = 0.00% in every cell.** The failure mode is losing-streak drawdowns, not single −5%
days — so `dd_protection` (which throttles sizing once equity is DD_TRIGGER below peak) reaches
the *entire* failure mode. Sweep at LOCKED allocations on decompounded static 2020-26:

| ddp (trig/scale) | pass | bust (all static) | p99 DD | median | gate |
|---|---|---|---|---|---|
| 1.50% / 0.40 (locked C2) | 97.04% | 2.96% | 5.93% | 31 | fail |
| **1.50% / 0.20** | 99.55% | 0.45% | 4.89% | **38** | PASS (p+0.11) |
| 1.00% / 0.25 | 99.48% | 0.52% | 4.92% | 45 | PASS (p+0.08) |
| 1.00% / 0.20 | 99.79% | 0.21% | 4.58% | 50 | PASS (p+0.42) |
| 0.75% / 0.20 | 99.87% | 0.13% | 4.38% | 56 | PASS (p+0.62) |
| 0.50% / 0.20 | 99.91% | 0.09% | 4.19% | 65 | PASS (p+0.81) |

Combos (mild allocation trim + brake):
| config | pass | bust | p99 DD | median | gate |
|---|---|---|---|---|---|
| k=0.85 + 1.0%/0.25 | 99.81% | 0.19% | 4.46% | 49 | PASS (p+0.54) |
| **k=0.80 + 1.0%/0.25** | 99.89% | 0.11% | 4.24% | 52 | PASS (p+0.76) |
| k=0.85 + 1.5%/0.30 | 99.39% | 0.61% | 4.96% | 37 | PASS (p+0.04) |

### Efficient frontier (lowest median pass-time at each safety tier)
* **Light / just-clear (p99 ≈ 4.9):** `dd_protection` wins — **DD_SCALE 0.40→0.20 at the locked
  1.5% trigger clears at median 38**, no allocation change, beats uniform k=0.70 (median 41).
  My original hypothesis holds *here*: one constant, surgical, fastest.
* **Moderate (p99 ≈ 4.6):** roughly a tie — uniform k=0.60 (median 45) ≈ ddp 1.0%/0.20 (median 50).
* **Deep / locked-equivalent headroom (p99 ≈ 4.3, +0.6pp):** **uniform allocation k≈0.55 (median 47)
  beats ddp-only** (0.75%/0.20, median 56). Deep p99 reduction via ddp needs a twitchy low trigger
  that over-brakes noise dips → bigger median penalty. The combo **k=0.80 + 1.0%/0.25** (median 52,
  p+0.76) is the most-robust single config and keeps 80% of the risk budget.

### Revised recommendation
* **Minimal-change, fastest:** `DD_SCALE 0.40 → 0.20` only (median 38, modest +0.11 margin). One
  constant; reaches the all-static failure mode directly.
* **Deepest headroom:** uniform `k≈0.55` (median 47) **or** combo `k=0.80 + DD 1.0%/0.25`
  (median 52, +0.76 margin — keeps more allocation).
* **Caveat:** DD_SCALE 0.20 is 2× the locked brake strength; it heavily throttles drawdown
  recovery and reopens the dd_protection lock. C2's *trigger* already failed the regime-
  robustness gate once (Q-DDP-1, accepted on override). **Any of these needs the mandatory
  regime-robustness gate + an ADR before locking** — these p99 margins sit near the MC noise floor.

## Regime-robustness gate (mandatory) — both de-risk candidates REJECTED

Per `docs/methodology/regime_robustness_gate.md` (6-month block bootstrap n=100 + half-panel
split). Floor = this brief's headline criteria = the two lock gates (bust < 1% AND p99 DD < 5%),
applied in **each** partition (Phase-4-floor amendment — relaxing it defeats the gate). Candidates
on the decompounded static 2020-26 streams, fixed 1R:
* **C1 k=0.55** — uniform allocation cut, locked dd_protection (1.5%/0.40)
* **C2 DD_SCALE→0.20** — locked allocations, brake strengthened

**Half-panel split (deterministic; bday midpoint 2023-03-20):**

| candidate | H1 2020–2023 (bust / p99 / med) | H2 2023–2026 (bust / p99 / med) | verdict |
|---|---|---|---|
| C1 k=0.55 | **8.89% / 7.58% / 181d** ❌ | 0.00% / 3.30% / 27d ✅ | **GATE FAIL** |
| C2 DD_SCALE→0.20 | **13.50% / 7.37% / 149d** ❌ | 0.07% / 4.28% / 20d ✅ | **GATE FAIL** |

**Both Part A (6-month block bootstrap, n=100) and Part B (half-panel) fail — doubly decisive:**

| candidate | bootstrap 95th-pct p99 / bust (floor <5% / <1%) | Part B |
|---|---|---|
| C1 k=0.55 | **5.03%** ❌ / 0.64% ✅ | H1 fails |
| C2 DD_SCALE→0.20 | **5.25%** ❌ / **1.53%** ❌ | H1 fails |

(Bootstrap sanity per the gate doc holds — 5th-pct pass ≤ full-panel pass for both: stress is a
haircut, not a boost.) So the regime-fragility is not merely a temporal-half artifact — it is
independently present under alternate-history block resampling. **Both candidates fail, decisively
on H1.** The de-risk only clears the *full* panel because the benign H2 (2023-2026 trend regime)
dominates the average; the H1↔H2 asymmetry is enormous (bust 8.89% vs 0%, p99 7.58% vs 3.30% for
C1). Same shape as Q-DDP-1's rejected C2, far more severe.

### What would it take to clear the hard H1 regime?
| H1 config | Σrisk | bust | p99 DD | median |
|---|---|---|---|---|
| k=0.55 (C1) | 0.55 | 8.89% | 7.58% | 181d ❌ |
| k=0.40 | 0.40 | 3.43% | 6.57% | 254d ❌ |
| k=0.30 | 0.30 | 1.00% | 5.57% | 321d ❌ |
| **k=0.25** | 0.25 | 0.35% | 5.00% | **367d** ✅ |
| k=0.20 | 0.20 | 0.08% | 4.35% | **431d** ✅ |
| k=0.30 + DD 0.75/0.20 | 0.30 | 0.00% | 3.31% | **591d** ✅ |

The hard regime only clears at **~¼ of locked risk, where median pass-time is 367–591 days
(1–1.6 years)** — not a viable prop challenge.

### Verdict → HOLD
**No viable static sizing config (allocation or dd_protection) is regime-robust.** The portfolio
is regime-dependent: excellent in trending regimes (2023-2026), poor in choppy/crisis regimes
(2020-2023, esp. 2022), and sizing cannot fix the hard regime without crippling the challenge.
Decision: **HOLD** the locked config; adopt the regime-dependence as the canonical risk
characterization; manage the hard regime operationally + a quarterly regime trigger (next
2026-08-08); k=0.55 retained as a *documented mitigation only*; **regime-adaptive sizing** is the
only viable structural fix (future Pre-Q). Full decision: `docs/adr/2026-06-07-decompound-remc-hold.md`.

## Reproduce
```
cd lab/analysis/decompound_remc_2026-06-07
python -m pytest test_decompound.py -q     # 18 gates incl REG byte-identity
python decompound.py                       # stitch + round-trip self-check
python remc.py                             # MC cells + attribution
python findings.py                         # per-strategy + isolation
python sweep.py                            # uniform de-risk grid
python sweep.py --targeted                 # targeted allocation configs
python ddp_sweep.py                        # dd_protection tightening grid + combos
python regime_gate.py 100                  # regime-robustness gate (both candidates)
python h1_check.py                         # what de-risk clears the hard H1 regime
```
