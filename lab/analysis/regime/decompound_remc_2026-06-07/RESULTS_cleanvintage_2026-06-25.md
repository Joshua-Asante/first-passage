# Scope-A decompound re-MC — CLEAN single-file vintage (2026-06-25)

**Verdict: HOLD-ROBUST** (the 2026-06-07 HOLD stands) **— but the breach severity was
materially inflated by the old stitch-seam artifact.**

**Question.** The HOLD ADR (`docs/adr/2026-06-07-decompound-remc-hold.md`) put the
portfolio on HOLD because the decompounded full-history (2020-26) re-MC breached both lock
gates (B_2020 = 97.08% / 2.92% / 5.93%). That re-MC stitched Guardian/DJ30 from 2 TV exports
each. Scope-B (`Q-INCUMBENT-REGIME-1`) surfaced a stitch-seam artifact: clean single-file
DJ30 standalone DD = 6.54% vs stitched 9.03%. Does the breach soften on clean data?

**Pre-registration:** `docs/ltm/briefs/pre-registration/2026-06-25-decompound-cleanvintage-remc-prereg.md`
(thresholds = the standing lock gates bust<1% AND p99<5%, frozen before this run).
**Driver:** `remc_cleanvintage.py` (sibling; zero fork of frozen `decompound.py`).
**Data:** clean single-file 2026-06-25 Pepperstone BT-OFF, N=317/271/150/281, n_bd=1687.

---

## Cells (locked C2 dd; SEEDS=(42,123,2026); 10k×3; fixed 1R on decompounded)

| cell | window | pass | bust | p99 DD | median | OLD (stitched) | gate |
|---|---|---:|---:|---:|---:|---|:--|
| C_2020 (compounded) | 2020-26 | 99.09% | 0.91% | 5.11% | 36 | 98.22/1.78/5.48 | breach (p99) |
| S_2022 (static) | 2022-26 | 99.58% | 0.42% | 4.78% | 22 | 99.16/0.84/5.00 | **CLEAR** |
| S_2020 (static) | 2020-26 | 98.46% | 1.54% | 5.31% | 31 | 97.04/2.96/5.93 | breach |
| **B_2020 (banded)** — HEADLINE | 2020-26 | **98.53%** | **1.47%** | **5.32%** | 31 | 97.08/2.92/5.93 | **breach** |

**Headline B_2020 vs HOLD anchor:** Δbust **−1.45pp** (2.92→1.47), Δp99 **−0.61pp** (5.93→5.32).
Both gates **still breach** (bust 1.47% ≥ 1%, p99 5.32% ≥ 5%) → **HOLD-ROBUST**. But the breach
is ~half as severe as the stitched vintage recorded — the artifact was real and non-trivial.

## Half-panel regime cut (Part B; floor bust<1% AND p99<5% per partition)

| config | H1 (2020-01→2023-03, 843bd) | H2 (2023-03→2026-06, 844bd) | verdict |
|---|---|---|:--|
| **LOCKED k=1.0** | pass 86.16% / **bust 13.84%** / p99 7.76% / med 62 | 99.79 / 0.21 / 4.53 / 20 | H1 **FAIL** |
| C1 k=0.55 | 96.93 / **2.81%** / 6.27% / 136 | 100.00 / 0.00 / 3.02 / 29 | H1 **FAIL** |
| C2 DDscale0.20 | 93.95 / **4.94%** / 6.31% / 122 | 99.99 / 0.01 / 3.87 / 21 | H1 **FAIL** |

- **Locked-config H1 isolated for the first time** (the original gate only tested the
  de-risk candidates): H1 bust **13.84%**, p99 **7.76%** — the regime-split that the HOLD
  characterizes is fully intact on clean data. The chop half is still the killer.
- **Both de-risk candidates still GATE FAIL on H1** (softer than stitched 8.89% / 13.50%,
  but neither clears bust<1% nor p99<5%). The "no viable static de-risk" conclusion survives.
- Bootstrap (Part A) not run: both candidates fail on H1, which fails the full gate
  (bootstrap AND H1 AND H2) regardless — the bootstrap can only matter when H1 passes.

## Disposition

1. **HOLD unchanged.** Locked config still breaches both gates on clean 2020-26 data; the
   regime-dependence characterization holds. No `core/` change; no ADR reversal.
2. **Severity correction (recorded as an ADR addendum):** the canonical breach figure on
   clean data is **98.53% / 1.47% / 5.32%**, not the stitched 97.08% / 2.92% / 5.93%. The
   ADR's headline overstated bust by ~1.45pp and p99 by ~0.61pp due to the Guardian/DJ30
   stitch-seam artifact. The HOLD's *direction* is robust; its *magnitude* was inflated.
3. **Follow-up for the 2026-08-08 regime trigger (flagged, not run):** because H1 is less
   severe on clean data (C1 k=0.55 H1 bust 2.81% vs stitched 8.89%), the regime-robust
   deep-de-risk frontier may now clear at a **more practical** risk/median than the ADR's
   "k≈0.25, 367-591d" conclusion. Re-run `h1_check.py` on the clean single-file vintage at
   the next trigger to re-quantify the cost-of-regime-robustness; if a practical regime-robust
   config emerges, it reopens the de-risk option the ADR closed. Does NOT change today's HOLD.

## Fidelity

No in-run anchor available (the canonical 99.83 cell + old stitched files are absent in this
worktree). Trust chain: (a) the single-file loader reproduced RESULTS.md Aegis/NAS full-panel
decompounded DD **exactly** (6.12 / 5.18) in `scope_b_regime_split.py` — and those two are
single-file in both vintages, so the loader is validated; (b) `run_mc` / `build_daily_panel`
are the `test_decompound.py`-pinned frozen machinery (REG byte-identity reproduces 99.83). All
four clean cells move in the same direction and magnitude vs their stitched counterparts
(bust roughly halved, p99 −0.4 to −0.6pp), consistent with a DD-inflating stitch artifact.

## Reproduce
```
cd lab/analysis/decompound_remc_2026-06-07
python remc_cleanvintage.py               # cells + locked/C1/C2 half-panels
python remc_cleanvintage.py --bootstrap 100   # + Part A block bootstrap (moot — H1 already fails)
```
