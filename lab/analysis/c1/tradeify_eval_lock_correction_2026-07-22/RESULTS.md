**Theme:** c1
**Status:** ACTIVE — Tradeify/MFFU eval drawdown-lock correction re-MC
# Tradeify / MFFU eval-tier drawdown-locking correction — re-MC RESULTS

**Status:** `MEASURED — Part A flips PASS → FAIL on both trailing_locking tiers; G8 discharge WITHDRAWN`
**Date:** 2026-07-22
**Authorisation:** operator, chat 2026-07-22 — "I authorise the eval-tier re-MC for the locking fix."
**Layer:** research measurement + config-provenance. **No locked parameter, allocation, or `dd_protection` constant is touched by this run.**

---

## §0 — Rule-0 reads (production source, this session)

- `core/firm_rules.py` — `Tradeify_Select_{25K,50K,100K,150K}` and `MFFU_Rapid_{50K,100K}` all carry `dd_lock_offset_usd: 100` on rows whose other fields (`profit_target_pct` 6.0 = eval target, `min_trading_days` 3 = eval-only consistency, eval micro caps) model the **evaluation** phase.
- `core/mc/simulation.py:123-135` — the `trailing_locking` branch: `floor = min(peak - max_dd_usd, starting_equity + dd_lock_offset_usd)`. The `min()` is what caps the floor's ascent.
- `tests/core/test_trailing_locking_boundary.py` — establishes the engine's own idiom for "pure fixed-$ trail, no lock": `dd_lock_offset_usd=1_000_000.0` (unreachable). **Not `None`** — `None` makes the whole branch inert (no DD check at all), which would be a different and much larger error.
- `lab/analysis/class_s_candidate1_scoring_2026-07-15/RESULTS.md` — the published figures this run re-derives.
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` — frozen gate: `eval_bust_ceiling` 3.0%, `pass_floor` 50%, seeds (42, 123, 2026), 10k sims/seed, horizon 1500.

## §1 — The defect

Both firms apply drawdown **locking** only in the funded stage; the eval phase has none. Verbatim:

- **Tradeify** ([article 10495897](https://help.tradeify.co/en/articles/10495897-rules-trailing-max-drawdowns), article-dated 2026-06-18, read 2026-07-22): *"Q: Does drawdown lock on Evaluation accounts? A: No. Drawdown only locks on Sim Funded accounts. Evaluation accounts do not have drawdown locking."*
- **MFFU** ([article 13286542](https://help.myfundedfutures.com/en/articles/13286542), read 2026-07-22): the *"Rapid Plan Evaluation Stage Account Parameters"* table lists only `Maximum Loss Limit (EOD) $3,000` — **no lock**. *"Max Loss Lock at $100"* appears solely under *"1. Sim Funded Account Parameters."* The `firm_rules.py` comment above these rows **already said** the lock was a funded mechanism; the eval rows carried it anyway.

**Direction of the error is optimistic, and the magnitude is near-total over the decisive stretch.** At the 100K tier the lock engages at EOD **$103,100** while the eval passes at **$106,000** — so *every* simulated path crosses the lock region before passing. Over that stretch the modeled floor sits up to **$2,900 below** the real one, ≈97% of the entire $3,000 drawdown. The sim survives paths a real eval account busts.

## §2 — Method

Correction = keep `dd_type="trailing_locking"` (the fixed-$ trail is right) and make the lock **unreachable**, which is the engine's existing idiom for a pure fixed-$ trail. No engine change.

Both runs use the harness's own `score_candidate` path at the **$100K basis** (`book_daily_at_100k`), the frozen seeds/sims/horizon, and identical panel bytes. Baseline and corrected differ **only** in `dd_lock_offset_usd`.

**Reproduction control (load-bearing).** The baseline arm must reproduce the published 2026-07-15 figure before any delta is trusted — an artefact agreeing with its own pin is consistency, not correctness. It does: **2.64% vs published 2.65%** → `MATCH`.

> A first attempt produced a 15.83% baseline and was **discarded, not reported**: it summed the raw $200K panel instead of rescaling to $100K. The reproduction check is what caught it. Retained here because "the check that caught my own error" is the reason to keep running it.

## §3 — Result: Tradeify_Select_100K (the c1 account)

| | Run-1 bust | Run-1 pass | Run-2 bust | Run-2 pass | Part A (≤3.0%) |
|---|---|---|---|---|---|
| Baseline (lock @ $100, as published) | 2.64% | 97.36% | 2.65% | 97.34% | **PASS** |
| **Corrected** (eval: no locking) | 3.98% | 96.02% | **4.74%** | 95.25% | **FAIL** |
| delta | +1.34 pp | −1.34 pp | **+2.10 pp** | −2.09 pp | flips |

Part A had **0.35pp** of headroom under the frozen 3.0% ceiling; corrected, it misses by **1.74pp**.

## §4 — Result: G8 discharge, all four frozen tiers (corrected)

The published `discharges_falsifier = True` rested on exactly two Part A clearers — Tradeify and MFFU — which are precisely the two `trailing_locking` tiers, i.e. **the only two carrying this defect**. Bulenox and BluSky are `dd_type="trailing"`, carry no lock field, and are untouched controls.

| Tier | dd_type | Run-1 bust | Run-2 bust | Run-2 pass | Part A |
|---|---|---|---|---|---|
| Bulenox_100K | trailing | 3.51% | 3.51% | 96.49% | False *(control, unchanged)* |
| Tradeify_Select_100K | trailing_locking | 3.98% | **4.74%** | 95.25% | **False** *(was True)* |
| MFFU_Rapid_100K | trailing_locking | 3.98% | **4.25%** | 95.74% | **False** *(was True)* |
| BluSky_Premium_100K | trailing | 3.51% | 4.44% | 95.54% | False *(control, unchanged)* |

**Part A clearers: none. `discharges_falsifier = False`.**

G8 requires ≥2 firms clearing Part A including ≥1 `trailing_locking`. Corrected, there are zero clearers — the discharge does not merely weaken, it collapses. **The prop-portfolio program's §4 falsifier is therefore UNDISCHARGED** (hard date 2026-11-08). Decision record: `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`.

The two `trailing` controls returning unchanged values is the internal check that the correction touched only what it should.

## §5 — WATCH-1 (0.50×) corrected arm — **NOT MEASURED**

**Status: `UNMEASURED — open item`.** Launched via the authoritative pre-registered harness (`class_s_c1_haircut_regime_remc_2026-07-16/run_haircut_regime_remc.py`) under corrected geometry, then **stopped by the operator on runtime cost** (the n=100-panel bootstrap runs >70 min per arm-tier and had not reached the 0.50× arm). **No 0.50× figure is quoted, estimated, or inferred here.**

What the aborted run *did* establish: its **1.00× arm reproduced §3 exactly**, plus corrected 1.00× regime halves (Tradeify H1 6.78%, MFFU H1 6.28%, vs 4.37% published).

**The open risk, stated precisely.** The c1 GO ADR §6 frames live risk on the **WATCH-1 0.50×** figures — published full-panel bust **0.08%**, H1 **0.14%**, bootstrap-95th **0.77%**. Those were computed under the **defective** geometry, so they are **known-optimistic by an unmeasured amount**. Direction is certain (the correction only removes cushion); magnitude is not. The +2.10pp seen at 1.00× must **not** be scaled to 0.50× — halved risk interacts with the barrier non-linearly, which is exactly why it must be run.

**Cheapest path to close (≈3 min, not an hour):** the headline is the *full-panel reference*, which the harness computes **before** the expensive bootstrap. `--arms 0.50x` and read the full-panel line; the bootstrap-95th and regime rider are the long poles and are separable.

Until measured, treat the published 0.50× figures as an upper bound on quality, not as current.

## §6 — What is NOT changed by this run

- **`dd_lock_offset_usd` stays `100` in `core/firm_rules.py`.** The measurement is recorded; the constant is not hand-edited. Applying it is a separate change that moves published numbers across three consumers (`tradeify_futures3_remc_2026-07-11`, `tradeify_futures3_bustcut_2026-07-11`, `class_s_candidate1_scoring_2026-07-15`) and needs its own ADR + re-pin pass.
- **The c1 rail GO is not overturned.** It rests on Q-RAIL-1 execution fidelity and the WATCH-1 haircut re-MC — a different harness and a different gate. §5 is a real open input to B7, not a retraction of the GO.
- No locked Pine, allocation, or `dd_protection` constant is touched.

## §7 — Reproduce

```bash
python lab/analysis/tradeify_eval_lock_correction_2026-07-22/remc_eval_lock_fix.py
python lab/analysis/tradeify_eval_lock_correction_2026-07-22/remc_g8_discharge_check.py
```

Both print a `[reproduction]` / control line; the first hard-checks the baseline against the published 2.65% and prints `MATCH` or `MISMATCH — delta NOT trustworthy`. Requires the gitignored CME panel bytes under `core/data/tv_exports/cme/`. Reports: `remc_eval_lock_fix_report.json`, `remc_g8_discharge_corrected.json`.
