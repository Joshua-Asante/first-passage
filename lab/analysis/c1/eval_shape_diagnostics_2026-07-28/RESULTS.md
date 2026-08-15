**Theme:** c1
**Status:** ACTIVE — eval-shape diagnostics under corrected Tradeify geometry
# Eval-shape diagnostics (2026-07-28)

**Status:** `COMPLETE` (diagnostic; no K consumed; no gated question)
**Date:** 2026-07-28
**Shared geometry / panel:** CORRECTED — `dd_lock_offset_usd → 1_000_000.0` applied **inside each joblib worker** (loky re-import trap) and attested in JSON. Panel / 1R identical to [`../c1_band_rescore_2026-07-24/band_rescore_report.json`](../c1_band_rescore_2026-07-24/band_rescore_report.json) (MYM `15d8b` sha256 `9acfa297…`; MNQ `beabf` sha256 `8884e6dd…`; risk_pct 0.007 / 0.0037). `core/` / `firm_rules.py` untouched (in-memory patch only).
**Parts in this dir:** (1) days-to-pass + 50K quantization · (2) 0.50× boot-95th + rider-tail attribution.

---

# Part A — days-to-pass + 50K quantization

**Runner:** [`run_days_to_pass.py`](run_days_to_pass.py) · report [`days_to_pass_report.json`](days_to_pass_report.json)
**Engine:** harness-level wrap of frozen `run_seed` / `firm_kwargs` / `summarize_outcomes` (same chain as `run_partition_mc` → `run_tier_remc`). Days-to-pass captured from `run_seed` return payloads — **not** surfaced by `summarize_outcomes`. 10K sims × seeds 42/123/2026, horizon 1500.
**Prior bust finding:** [`../tradeify_eval_lock_correction_2026-07-22/remc_eval_lock_fix_report.json`](../tradeify_eval_lock_correction_2026-07-22/remc_eval_lock_fix_report.json) — corrected 100K|1.00× Run-1 3.9833% → Run-2 4.7433% (+0.76pp).

## Reproduction pins

| Cell | Measured bust | Pin | Result |
|---|---|---|---|
| 100K \| 1.00× \| Run-2 | **4.7433%** | 4.7433% | **MATCH** |
| 50K \| 1.00× \| Run-2 | **1.06%** | 1.06% | **MATCH** |
| 100K \| 0.50× \| Run-2 | 0.1067% | 0.01% (±0.15pp) | **MATCH** |
| 50K \| 0.50× \| Run-2 | **0.01%** | 0.01% | **MATCH** |

## Headline — consistency time-cost

Per-cell **(Run-2 − Run-1) median days-to-pass** is the consistency gate's time cost. Dollarized at the standing **$49/mo** CrossTrade Pro run-rate ([`../q_rail_1_2026-07/PHASE4.md`](../q_rail_1_2026-07/PHASE4.md)), using 21 trading days/month.

| Tier | Arm | Run-1 med d | Run-2 med d | **Δ med d** | **$ at $49/mo** | Bust Δ (pp) |
|---|---|---|---|---|---|---|
| Tradeify_Select_100K | **1.00×** | 217 | 262 | **+45** | **+$105** | **+0.76** |
| Tradeify_Select_100K | 0.50× | 447 | 451 | +4 | +$9.33 | 0.00 |
| Tradeify_Select_50K | **1.00×** | 222 | 270 | **+48** | **+$112** | +0.14 |
| Tradeify_Select_50K | 0.50× | 447 | 451 | +4 | +$9.33 | 0.00 |

At the gating 1.00× / 100K basis the 40% consistency rule costs **~2.1 months of bridge run-rate (~$105)** on top of the already-known **+0.76pp bust** cost under corrected geometry. At 0.50× the same gate is nearly free in both time and bust (scale pushes paths far from the consistency binding region).

## Full cell table (PASS sims only for days)

| Cell | bust | pass | med | p25 | p75 |
|---|---|---|---|---|---|
| 100K \| 1.00× \| Run-1 | 3.9833% | 96.02% | 217 | 137 | 322 |
| 100K \| 1.00× \| Run-2 | 4.7433% | 95.25% | 262 | 175 | 377 |
| 100K \| 0.50× \| Run-1 | 0.1067% | 99.81% | 447 | 325 | 607 |
| 100K \| 0.50× \| Run-2 | 0.1067% | 99.80% | 451 | 330 | 611 |
| 50K \| 1.00× \| Run-1 | 0.9200% | 99.08% | 222 | 141 | 332 |
| 50K \| 1.00× \| Run-2 | 1.0600% | 98.93% | 270 | 177 | 392 |
| 50K \| 0.50× \| Run-1 | 0.0100% | 99.89% | 447 | 325 | 607 |
| 50K \| 0.50× \| Run-2 | 0.0100% | 99.89% | 451 | 330 | 611 |

## Appendix — Tradeify_Select_50K integer-quantization check

**Owed by** [`STATE.md`](../../../STATE.md) / band-rescore RESULTS item 4 (cap-exact 39.5/40 continuous estimate). Pure arithmetic — `ops/c1_rail/c1_sizing_host_reference.py` sizing law + [`../q_rail_1_2026-07/f2_floors.json`](../q_rail_1_2026-07/f2_floors.json) pins (100K MYM base 8 / add 60 at WATCH-1). No schedule policies run.

### Method

```
r_eff   = BASE_RISK × DD_SCALE(=1) × lifecycle(=arm)
qty_raw = floor(E_firm × r_eff / (SL_pts × $/pt))
reserve = floor(cap_alloc / (1 + pyr%/100))
base    = min(qty_raw, reserve)
add     = floor(base × pyr%/100)
```

- `E_firm = 50_000`, `cap_firm = 40`
- **Primary split:** proportional scale of the locked 69/11 alloc → **MYM 35 / MNQ 5** (MNQ floored, MYM takes remainder)
- SL sources: F2 `full_median` and `recent_90d` ATR vintages
- Arms: 1.00× (lifecycle 1.0) and 0.50× (WATCH-1)

100K WATCH-1 pin check (full_median, alloc 69/11): MYM base **8** / add **60**, MNQ base **1** / add **10** — matches `f2_floors.json`.

### Results (primary split 35/5)

| Vintage | Arm | MYM base/add | MNQ base/add | Aggregate | MNQ zero-floor? |
|---|---|---|---|---|---|
| full_median | 1.00× | 4 / 30 | **0 / 0** | 34 / 40 | **YES** |
| full_median | 0.50× | 4 / 30 | **0 / 0** | 34 / 40 | **YES** |
| recent_90d | 1.00× | 4 / 30 | **0 / 0** | 34 / 40 | **YES** |
| recent_90d | 0.50× | 4 / 30 | **0 / 0** | 34 / 40 | **YES** |

**Answers:**

1. **MNQ zero-floors at both arms** under the proportional 69/11→35/5 split. Cause is the **cap reserve**, not risk dollars: `floor(5 / 11) = 0`, so MNQ `reserve_cap = 0` and the book **degenerates to a 1-leg MYM book** even when `qty_raw ≥ 1`.
2. **Aggregate fits the 40-micro cap** (34/40) — but only because MNQ died. The band-rescore continuous estimate of **39.5/40** assumed divisible MNQ size; integer + pyramid-reserve semantics do **not** realize that near-cap book.

### Side note — MNQ-min-11 reallocation (29/11)

If MNQ is held at `cap_alloc = 11` (minimum for `reserve_cap ≥ 1`) and MYM takes the rest (29):

| Vintage | Arm | MYM | MNQ | Agg | MNQ zero? |
|---|---|---|---|---|---|
| full_median | 1.00× / 0.50× | 3/22 | 1/10 | 36/40 | no |
| recent_90d | 1.00× | 3/22 | 1/10 | 36/40 | no |
| recent_90d | 0.50× | 3/22 | **0/0** | 25/40 | **YES** (risk-dollar floor) |

A 29/11 reallocation rescues MNQ under full-median and recent_90d@1.00×, still fits the 40 cap, and is **not** the proportional read of the locked 100K split. Admitting a 50K host constants file would need its own cap_alloc decision; this check only measures the owed check.

## What Part A does not do

- No frozen-gate change; no §4 discharge claim; no candidate selection.
- No Q-EVALSEQ-1 / sizing-schedule policies (08-08-gated).
- No edit to `core/firm_rules.py` — in-memory worker patch only.
- Does not authorize acting on the Tradeify_Select_50K clearer — the quantization finding is a **blocker** for 2-leg deployment at that tier under a proportional cap split.

---

# Part B — 0.50× boot-95th + rider-tail attribution

**Owed by:** GO ADR Addendum 2026-07-24 ("remaining separable long pole") + band-rescore RESULTS (no prior leg/day/block decomposition of the rider FAIL).
**Runners:** [`run_rider_050x.py`](run_rider_050x.py) · [`run_rider_tail_attribution.py`](run_rider_tail_attribution.py) · shared [`_boot_attested.py`](_boot_attested.py)
**Reports:** [`rider_050x_report.json`](rider_050x_report.json) · [`rider_tail_attribution.json`](rider_tail_attribution.json)
**Method:** frozen regime-gate primitives (full + H1/H2 + 6mo-block bootstrap n=100, block=126bd, `BOOT_SEED=20260715`, seeds 42/123/2026, 10K sims/seed, horizon 1500). Worker-local geometry patch + attestation on every panel.

## (a) Headline — WATCH-1 0.50× boot-95th vs 3.0%

`Tradeify_Select_100K` @ deployed 0.50×, corrected geometry:

| Partition | bust | Floor (≤3.0% ∧ pass≥50%) |
|---|---|---|
| Full-panel | **0.11%** | PASS |
| H1 | **0.22%** | PASS |
| H2 | **0.04%** | PASS |
| **Bootstrap-95th (n=100)** | **1.20%** | **PASS** |
| Bootstrap pass-5th | 95.5% | PASS |

Reproduction vs published corrected full/half pins (GO Addendum 2026-07-24 / `corrected_haircut_fullpanel_report.json`): full / H1 / H2 all **MATCH**. Geometry attestation: all 100 panels report `dd_lock_offset_usd = 1e6`.

**Verdict:** the declared remaining separable long pole **clears** the frozen 3.0% ceiling under corrected geometry (1.20% << 3.0%). Context: defective-geometry historical boot-95th at 0.50× was 0.77% (GO §6); corrected is higher, as expected, and still PASS. Not a B7 gate — diagnostic closure of the open measurement only.

## (b) Headline — top-decile rider-tail attribution

1.00× block-logged bootstrap on the RIDER-FAIL cell + the 100K reference. Headline pins first:

| Tier | Headline | Pin | Boot-95th (this run) | Prior pin |
|---|---|---|---|---|
| Tradeify_Select_50K | **1.06%** | 1.06% **MATCH** | **6.69%** | 4.54% **MISMATCH** |
| Tradeify_Select_100K | **4.7433%** | 4.7433% **MATCH** | **17.79%** | (none published corrected) |

The 50K boot-95th MISMATCH vs the prior band-rider 4.54% is **informative, not a harness defect**: that prior rider patched geometry in the parent only under `joblib` process pools, so workers silently re-imported the defective `dd_lock_offset_usd=100`. Worker-attested corrected geometry is the trustworthy number; headline MATCH confirms the panel/MC path.

### Fragility shape: **CONCENTRATED** (both tiers) — but not via H1 / leg / Tuesday

Top-decile-bust resamples vs the rest:

| Signal | 50K Δ (top−rest) | 100K Δ (top−rest) |
|---|---|---|
| H1 block-share | −0.009 | −0.013 |
| MYM loss-share | −0.016 | −0.022 |
| Tuesday co-fire density | −0.003 | −0.003 |
| Mean block loss-sum ($) | −75 | −142 |
| **Top-5 block-start mass within top** | **0.50** | **0.45** |

H1-vs-H2 share, per-leg loss share, and Tuesday co-fire density do **not** separate the tail (near-zero deltas). What concentrates: a **small set of recurring 6mo block starts** inside the top-decile cohort (top-5 mass ≥0.45 on both tiers). Blocks starting near indices **487** and **470** appear in both tiers' top-5 lists — identifiable chop windows on the daily panel, not a one-leg or co-fire story.

**Label correction 2026-07-28 (post-merge):** the JSON's `fragility_shape` field carried a *static* string ("block / leg / co-fire structure") emitted regardless of which limb of the `concentrated` OR actually fired — contradicting this section's own prose. Only the **block** limb fired (top-5 mass 0.50 / 0.45 vs threshold 0.45); H1-share, per-leg loss share and Tuesday co-fire were all an order of magnitude below theirs. `run_rider_tail_attribution.py` now reports the firing limbs, and the stored labels were **re-derived from the already-recorded deltas** (a pure function of them — no MC re-run). New field: `fragility_limbs_fired`.

**Answer to the brief's question:** fragility is **concentrated in identifiable blocks**, not diffuse across the panel — and **not** explained by H1-half dominance, MYM-vs-MNQ loss share, or Tuesday co-fire density.

## What Part B does not do

- No frozen-gate change; no §4 discharge; no new candidate selection; no sizing-schedule policies (Q-EVALSEQ-1 stays 08-08-gated).
- Does not re-open B7 on the 0.50× bust geometry (already closed benign on full/half; boot-95th was explicitly non-gating).
- Does not retract the 50K Part A clearer — rider FAIL caveat stands, now with a corrected (higher) boot-95th and a block-level attribution.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-28 | Days-to-pass matrix + 50K quantization check executed; all four reproduction pins MATCH | Cursor agent (PRIMARY tree) |
| 2026-07-28 | Part B: 0.50× boot-95th **1.20% PASS**; rider-tail attribution **CONCENTRATED** (block-start mass, not H1/leg/Tue); 50K corrected boot-95th 6.69% (prior 4.54% parent-only-patch MISMATCH) | Cursor agent (PRIMARY tree) |
