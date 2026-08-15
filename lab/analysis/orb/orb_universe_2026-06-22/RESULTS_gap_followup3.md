# NAS100 short-ORB GAP-CONDITIONED entry — RESULTS (follow-up #3, 2026-06-22)

> **VERDICT: NOT-CONFIRMED — offline null at lock-grade.** A gap-conditioned short opening-range
> breakout does not survive the pre-registered, multiplicity-corrected validation battery. The
> overnight gap carries *some* real, leak-free conditional information on the short ORB (monotone
> dose-response; the tail-guard passes — it is **not** pure tail-selection), but the apparent edge
> sits **within the best-of-K multiplicity envelope** (family-wise fw-p = 0.122, confirmed by three
> independent methods) on a structurally-weak OR=3 base (within-day placebo p = 0.141), and the
> surviving gates are marginal/regime-fragile. **No Pine variant authored. No core/lock change.**
> Adversarially verified (workflow `wf_68cbd0d3`, 3 independent lenses all CONFIRMS_NULL + an inline
> false-negative robustness guard).

**Date:** 2026-06-22 · **Basis:** exit@close (faithful entry-ranking; the give-back exit is NOT
offline-simulable — N5) · **Feed:** canonical Pepperstone BAR_EXPORT 2020-2026 (n=994 finite-gap) ·
**Harness:** [`nas100_orb_gap.py`](nas100_orb_gap.py) (battery), [`nas100_orb_gap_probe.py`](nas100_orb_gap_probe.py)
(reproduction), [`nas100_orb_gap_robust.py`](nas100_orb_gap_robust.py) (false-negative guard),
[`nas100_orb_sweep.py`](nas100_orb_sweep.py) `build_orb` (gap extension), [`orb_lib.py`](orb_lib.py) (engine).

---

## §0 — Rule 0 reads (done before any code)

- [`ops/instruments/NAS100.md`](../../../ops/instruments/NAS100.md) N1–N5 + ACTIVE/OPEN — the live ledger; N5 = the 5th-leg **NO-GO** (give-back exit not offline-simulable), ACTIVE/OPEN item 4 = the gap hypothesis.
- [`docs/adr/2026-06-22-nas100-orb-5th-leg.md`](../../../docs/adr/2026-06-22-nas100-orb-5th-leg.md) §11 (WITHDRAWN) — bug #4: "the OR-range filter lever is substantially an overnight-gap proxy; corr(OR-range,|gap|)=+0.34"; listed "a gap-conditioned variant" as a future test. This closes that thread (offline).
- [`nas100_orb_sweep.py`](nas100_orb_sweep.py) — `build_orb` already had `min_or/max_or`; `session_panel` meta already carries `prev_close`+`rth_open`. Gap = `rth_open − prev_close` is directly computable.

The base engine was reproduced exactly before any new claim: base OR=3 short n=995 (994 finite-gap) / meanR +0.0292 / drop-top-5 −0.0062 (matches the published anchor; my gap edit is inert when off).

---

## §1 — The motivating evidence, reproduced ([`nas100_orb_gap_probe.py`](nas100_orb_gap_probe.py))

- **corr(OR-range, |gap pts|) = +0.335** ≈ the cited +0.34 → the OR-range filter is a gap proxy.
- **Full-set |gap%| terciles: low −0.022 / mid −0.024 / HIGH +0.134** — the entire weak base edge lives in the top gap tercile.
- **Sign:** gap-UP (+0.050, t1.0) > gap-DOWN (+0.004, t0.1). **Big gap-UP (|gap%|>0.69%, n=178): +0.170, t1.68, halves +0.126/+0.215.**

So the gap IS where the short-ORB action is. The question this follow-up answers: is a gap-conditioned
entry a *real, separable, lock-grade* edge, or a multiplicity/tail artifact of a regime-conditional base?

---

## §2 — Pre-registration (fixed before the run; seed 20260622; deterministic)

**Grid (= the multiplicity universe / best-of-K family):** sign ∈ {any, up, down} × |gap%| floor ∈
{none, p50, p67, p80} = 12 cells (11 conditioned + base). Thresholds = fixed percentiles of |gap%| on
the base set (p50 0.437% / p67 0.688% / p80 0.961%). **Primary** (a-priori mechanistic = fade the
gap-up): `up/p67`. **Magnitude in % (regime-stationary)** — raw points are not (NAS100 spans ~7k→31k).

A gap-conditioned entry **SURVIVES only if it clears ALL SIX** gates:

| Gate | Definition |
|---|---|
| G1 improvement | meanR ≫ base (+0.029) AND bootstrap P(meanR≤0) < 0.05 |
| G2 structure | both-sides OR=3 within-day placebo p < 0.05 (opening range carries info) |
| G3 gap-info | per-cut gap-label permutation p < 0.05 (gap informative beyond random subsetting) |
| **G4 best-of-K** | **family-wise** p < 0.05 = P(max-t over 11 cells under gap permutation ≥ obs) |
| G5 tail-guard | within-subset drop-top-5 > 0 AND > base (−0.006) — NOT tail-selection relabeled |
| G6 regime | 2024-26 meanR > 0 AND halves same sign (base is neg pre-2020 (N2) and 2026 (N5)) |

**Forbidden:** re-tuning thresholds/OR off the result to lift a cell; nesting the gap cut inside the
OR-range "keep mid" filter (double-selection); reading native give-back numbers as decision evidence;
declaring SURVIVE on G1+G3 while G4/G5/G6 fail.

---

## §3 — Battery results ([`nas100_orb_gap_OUTPUT.txt`](nas100_orb_gap_OUTPUT.txt))

**[A] Cut grid (exit@close), meanR / t / n / drop-top-5 / 2024-26 / halves:**

| cell | meanR | t | n | d5 | 2024-26 | h1/h2 |
|---|---|---|---|---|---|---|
| any/none (base) | +0.029 | +0.83 | 994 | −0.006 | +0.042 | +0.054/+0.005 |
| any/p67 (**best cell**) | +0.134 | **+2.04** | 328 | +0.056 | +0.247 | +0.108/+0.160 |
| any/p80 | +0.193 | +2.03 | 199 | +0.064 | +0.372 | +0.122/+0.264 |
| **up/p67 (PRIMARY)** | +0.170 | +1.68 | 178 | +0.025 | +0.326 | +0.126/+0.215 |
| up/p80 | +0.257 | +1.68 | 105 | +0.010 | +0.504 | +0.133/+0.378 |
| down/p67 | +0.092 | +1.15 | 150 | +0.001 | +0.111 | +0.132/+0.051 |
| up/none | +0.050 | +1.00 | 558 | −0.008 | +0.066 | +0.064/+0.035 |

**[B–F] Gate verdicts for the headline cuts:**

| Cut | G1 | G2 | G3 (per-cut perm) | G4 (family-wise) | G5 (tail) | G6 (regime) |
|---|---|---|---|---|---|---|
| **up/p67 (PRIMARY)** | ✓ (boot P≤0 = 0.018) | ✗ **0.141** | ✓ 0.035 | ✗ **0.122** | ✓ +0.025 | ✓ but 2021/2023 neg, 2026 flat |
| any/p67 (best) | ✓ | ✗ 0.141 | ✓ 0.023 | ✗ **0.122** | ✓ +0.056 | ✓ but 2021/2023 neg |
| down/p67 | – | ✗ | ✗ 0.232 | ✗ | ✓ +0.001 | ✓ |
| up/none | – | ✗ | ✗ 0.257 | ✗ | ✗ −0.008 | ✓ |

**Decisive failures: G4 (multiplicity) and G2 (structure).** The individually-significant per-cut
perm-p's (0.035, 0.023) are exactly the best-of-K trap: once the post-hoc selection over 11 correlated
tail-carried cells is corrected, the best cell (any/p67, t2.04) is reached by chance in **12.2%** of
gap-permutations. G2 adds that the OR=3 opening range itself fails its structural placebo (p=0.141;
N1's 0.014 was for OR=2). **G5 passing is the one genuine positive — the effect is not *pure*
tail-selection** — but a real-but-uncorrectable selection effect is still a null.

---

## §4 — Adversarial verification (workflow `wf_68cbd0d3`, 4 lenses; + inline robustness)

| Lens | Independent check | Verdict |
|---|---|---|
| **Multiplicity** (decisive) | 3 independent methods: independent gap-perm (20k) fw-p **0.113**; Holm across 11 cells rejects nothing (smallest adj **0.137**); demeaned block-bootstrap fw-p **0.503**. | **CONFIRMS_NULL** (high) |
| **Leak / faithfulness** | prev_close = strictly prior session (shift 1, NaN day-1); OR/breakout/exit forward-time only; the 1.9% both-touch bars are forced to −1R (**pessimistic → deflates, never inflates**). The +0.170 is **real**, not a look-ahead artifact. | **CONFIRMS_NULL** (high) |
| **Steelman** | Dose-response + per-cut G3 seed-robust (8 seeds), G1 boot P≤0=0.018 — real signal; but `up/p67` is **not** the best cell (sign-agnostic any/p67 is → "fade-gap-up" mechanism is post-hoc), G4 fails across all 8 seeds (0.110–0.122), G2 fails, regime-fragile. | **CONFIRMS_NULL** (high) |
| **Threshold-robustness** (false-negative guard) | family-wise fw-p across OR∈{2,3} × normalization∈{|gap%|, |gap|/OR}: see table below. | _(see §4.1)_ |

### §4.1 — False-negative guard: is the null knife-edge or robust?

Family-wise fw-p (the decisive gate) for the best cell, across OR-window × gap-normalization
([`nas100_orb_gap_robust_OUTPUT.txt`](nas100_orb_gap_robust_OUTPUT.txt)):

| OR | norm | best cell | t | meanR | n | **G4 fw-p** | G2 placebo |
|---|---|---|---|---|---|---|---|
| 2 | \|gap%\| | any/p67 | +2.09 | +0.150 | 363 | **0.148 FAIL** | 0.014 **PASS** |
| 2 | \|gap\|/OR | any/p67 | +2.04 | +0.158 | 363 | **0.164 FAIL** | 0.014 **PASS** |
| 3 | \|gap%\| | any/p67 | +2.04 | +0.134 | 328 | **0.123 FAIL** | 0.141 FAIL |
| 3 | \|gap\|/OR | any/p67 | +1.60 | +0.110 | 328 | **0.348 FAIL** | 0.141 FAIL |

**The null is ROBUST, not knife-edge.** Every OR-window × normalization fails the family-wise best-of-K.
The sharp finding: **even at OR=2, where the opening-range structure passes its placebo (G2 0.014), the
gap-conditioned best-of-K still fails (fw-p 0.148).** So the barrier is the **multiplicity of searching
gap-cuts**, not merely the weak OR=3 structure — fixing the structure does not rescue the edge. Verdict
holds. **CONFIRMS_NULL** (the false-negative guard found no nearby spec that flips it).

---

## §5 — What is real vs not (honest record)

**Real (leak-free, reproduced, seed-robust):**
- The overnight gap carries conditional directional information on the short ORB: monotone dose-response
  (any: +0.029 → +0.074 → +0.134 → +0.193 across none/p50/p67/p80) and the **drop-top-5 tail-guard
  passes** — conditioning genuinely shifts the distribution, it is not just grabbing the top trades.
- Recent-window strength is large (2024 +0.46, 2025 +0.35) and the native give-back cross-check on
  big-gap-up days points the same way (+0.142 vs +0.075 all-shorts — *context only, not a gate*).

**Not established (why it is a null at lock-grade):**
- **Multiplicity (G4):** the best gap-cut does not beat what searching 11 correlated cuts of a
  tail-carried base produces by chance (fw-p 0.11–0.50 across methods).
- **Structure (G2):** the OR=3 base fails its within-day placebo (p 0.141).
- **Mechanism is post-hoc:** the strongest cell is sign-agnostic (big |gap|), contradicting the a-priori
  "fade the gap-up" story that named `up/p67`.
- **Regime-fragile (G6):** 2021 & 2023 negative, 2026 ~flat (n=12) — consistent with N2 (post-2020-only)
  and N5 (2026 negative).

---

## §6 — Disposition

- **No gap-conditioned Pine variant authored.** The entry effect does not earn the cost of a native-TV
  export round. This is consistent with N5 (the whole NAS100-ORB give-back leg is NO-GO) and N2 (the base
  is regime-conditional). The deployed give-back exit remains not-offline-validatable regardless.
- **No `firm_rules` / `dd_protection` / `portfolio_mc` / Pine / LOCK change.** Operational layer untouched.
- **Revival path (recorded, not acted on):** the only way past the barrier is to **remove the
  multiplicity**, not search harder. A *fresh* pre-registration would name the **sign-agnostic big-|gap|
  cut (any/p67)** as the **single** a-priori hypothesis (no grid → no best-of-K penalty; the directional
  framing is what made `up/p67` post-hoc), tested on an **independent sample** (true OOS or a native TV
  export) so the in-sample selection is not re-paid. Note §4.1: **OR=2 fixes the structure (G2) but NOT
  the multiplicity (G4 0.148)** — moving to OR=2 alone does not rescue it. And the give-back exit cannot be
  locked offline regardless (N5). Re-proposal requires that fresh single-hypothesis pre-reg on independent
  data, not a parameter nudge.
- **2026 softness** flagged for the 2026-08-08 quarterly regime review (NAS100 ORB family).

---

## §7 — Audit hooks (runnable)

```bash
cd lab/analysis/orb_universe_2026-06-22
python nas100_orb_gap_probe.py     # reproduce base (n=995/+0.0281) + corr(+0.335) + gap terciles
python nas100_orb_gap.py all       # the 6-gate battery (G4 fw-p 0.122 FAIL, G2 0.141 FAIL)
python nas100_orb_gap_robust.py    # false-negative guard: family-wise fw-p over OR x normalization
python verify_multiplicity.py      # workflow scratch: 3 independent multiplicity methods (G4 robust)
# no-drift check: gap work is lab-only
git diff --stat -- core/ | grep -E "firm_rules|dd_protection|portfolio_mc" || echo "no core change (expected)"
```
