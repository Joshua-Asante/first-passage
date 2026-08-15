# Aegis→6J panel-of-record — decision table (prop-candidate pre-requisite)

**Date:** 2026-07-14 (Cursor handoff execution)  
**Parent:** [`docs/briefs/handoffs/2026-07-14-cursor-handoff-aegis-6j-panel-of-record.md`](../../../docs/briefs/handoffs/2026-07-14-cursor-handoff-aegis-6j-panel-of-record.md)  
**Scope:** prop-candidate pre-registration only — does **not** reopen [`ops/instruments/6J.md`](../../../ops/instruments/6J.md) J1 (self-funded lane panel of record).  
**Reproduce:** `python lab/analysis/aegis_6j_transfer_2026-07-05/_panel_inventory.py` (decompound @ $200K); `python lab/analysis/tradeify_futures3_bustcut_2026-07-11/_diag_aegis_1r.py` (ae744 vs 5274c 1R pin).

---

## §1 — Step 2.1 inventory + diff diagnosis

### Diff table (mechanical)

| Metric | **8e269 (J1 pinned)** | **ae744 (07-11)** | **5274c (07-11)** |
|---|---:|---:|---:|
| File | `…PROTOTYPE…_2026-07-05_8e269.csv` | `…BEPAD-TEST…_2026-07-11_ae744.csv` | `…BEPAD-TEST…_2026-07-11_5274c.csv` |
| SHA256 | `c3b34162…801946a6` | `e82a2c25…d148ca38` | `35ae75f2…ca60bed` |
| Span (exit dates) | 2022-01-12 → 2026-07-01 | 2020-02-24 → 2026-07-01 | 2020-02-24 → 2026-07-01 |
| N | 129 | 152 | 152 |
| WR | 35.66% | 34.87% | 34.87% |
| PF (raw @ export) | 2.318 | 2.042 | 2.212 |
| Net (raw @ $100K export) | +$39,056 | +$41,247 | +$27,413 |
| Net (decompound @ $200K) | +$67,394 | +$70,817 | +$49,122 |
| Exit qty mean | 11.35 | 11.36 | 7.29 |
| Exit qty median | 12 | 12 | 7 |
| Entry-set vs ae744 | — (different span) | — | **identical 152/152** |

### Loss cohort (decompound static $, \|loss\| buckets)

| Bucket | 8e269 | ae744 | 5274c |
|---|---:|---:|---:|
| scratch ≤ $50 | 10 | 11 | 26 |
| $50 – $500 | 45 | 53 | 49 |
| $500 – $2k | 21 | 24 | 24 |
| full-stop > $2k | **7** | **11** | **0** |

### 1R pin — `full_stop_mean` (metric-cohort binding)

| Panel | Basis | 1R ($) | n (full-stop cohort) | Median fallback fires? | Thin-cohort warn (1≤n<5)? |
|---|---|---:|---:|---|---|
| **8e269** | raw @ $100K export (J1 canonical) | **1,385.74** | **10** | no | no |
| **8e269** | decompound @ $200K (remc path) | 2,908.17 | 7 | no | no |
| **ae744** | decompound @ $200K (remc path) | **2,912.96** | **11** | no | no |
| **ae744** | raw @ $100K export | 1,422.72 | 14 | no | no |
| **5274c** | decompound @ $200K (remc path) | **166.56** | **0** | **YES** (zero full-stops → median) | n/a (fallback) |
| **5274c** | raw @ $100K export | 1,006.20 | 1 | no | **YES** (n=1) |

Reproduce 5274c fallback: `python lab/analysis/tradeify_futures3_bustcut_2026-07-11/_diag_aegis_1r.py` → `pin: method=median loss (FALLBACK — zero full stops) 1R=166.56 n=0 warn=True`.

### Bustcut reproduction gate

All four numbers in the bustcut `AEGIS INVENTORY` block reproduce from bytes (**PASS**):

| File | N | PF | net@200K | qty mean |
|---|---:|---:|---:|---:|
| ae744 (measured) | 152 | 2.042 | 70,817 | 11.36 |
| ae744 (bustcut) | 152 | 2.042 | 70,817 | 11.36 |
| 5274c (measured) | 152 | 2.212 | 49,122 | 7.29 |
| 5274c (bustcut) | 152 | 2.212 | 49,122 | 7.29 |

### Per-file classification (provenance / Pine-config)

**8e269 — KNOWN (HIGH confidence).** v0.3 PROTOTYPE Pine (`aegis_jpy_futures_v0_3_prototype.pine`, sha `30d35028…`), Deep Backtest CME:6J1! 15m, $100K initial, max_contracts=12, $1.30/side placeholder, 1-tick slip, window 2022-01-12 → 2026-07-01. Canonical self-funded lane panel — [`6J.md` J1](../../../ops/instruments/6J.md), [`NOTES.md`](NOTES.md) artifact table.

**ae744 — PARTIALLY UNKNOWN.** Filename carries `BEPAD-TEST` (the CLOSED-FALSIFIED Q-AEGIS-6J-BEPAD-1 experiment family), but CSV headers contain no Pine input metadata (standard TV List-of-Trades schema only). Observable: same 152 entry timestamps as 5274c, WR identical, exit-qty mean 11.36 ≈ v0.3 deep panel (11.35). **Plausible:** v0.3-class sizing (cap 12, $100K) on the extended 2020-start window — **not mechanically verified**; BE-pad k / account size / max_contracts cannot be determined from bytes alone (§0.5 → operator classification).

**5274c — PARTIALLY UNKNOWN (sizing delta confirmed).** Same Pine signal set as ae744 (entry-set byte-identical, N=152, WR=34.87%). Median raw P&L ratio 5274c/ae744 = **0.583** across all 152 trades. Zero full-stops after decompound → remc `pin_r_basis` median fallback (1R $166.56, ~9× spurious scale in bustcut Test 2). **Plausible:** reduced max_contracts or lower effective risk basis — **not mechanically verified** from headers; operator must confirm which TV input differed.

### Sizing-vs-signal hypothesis (Step 2.1 sub-claim)

**CONFIRMED (mechanical):** ae744 ↔ 5274c delta is **sizing-borne, not signal-borne**. Evidence: identical entry timestamp set (152/152 intersection, 0-only-a / 0-only-b), identical N and WR, proportional P&L scaling (median ratio 0.58 ≈ qty ratio 7.29/11.36 = 0.64).

---

## §2 — Step 2.3 decision table

| Row | Provenance / Pine-config | N / PF / net | 1R (`full_stop_mean`, remc @ $200K) | Suitability caveats |
|---|---|---|---|---|
| **8e269 (J1 pinned)** | v0.3 PROTOTYPE — **KNOWN** ($100K, cap 12, 2022-start deep panel) | 129 / 2.318 / +$39,056 raw | **$1,385.74** (n=10, raw @ $100K); decompound n=7 | Self-funded lane panel of record; **shorter span** (no 2020–2021); not the 07-11 Tradeify 3-leg book window; J1 explicitly not reopened here |
| **ae744** | BEPAD-TEST filename — **UNKNOWN** exact Pine inputs; sizing ≈ v0.3-class | 152 / 2.042 / +$70,817 decomp | **$2,912.96** (n=11); fallback **no** | Extended span (2020+); valid full-stop cohort on remc path; prior remc/bustcut baseline file; BEPAD-TEST label vs CLOSED-FALSIFIED BEPAD experiment needs operator disambiguation |
| **5274c** | BEPAD-TEST filename — **UNKNOWN** exact Pine inputs; ~64% sized vs ae744 | 152 / 2.212 / +$49,122 decomp | **$166.56** (n=0); fallback **YES** | **Disqualified on remc 1R path** — zero full-stops after decompound triggers median fallback → spurious ~9× scale (bustcut SENSITIVITY block); same signals as ae744 but wrong sizing basis for prop scoring |

### Recommendation (non-binding)

For a **prop-candidate** panel cited by future Class-S pre-registration using the Tradeify remc scaling method (`decompound @ $200K` + `pin_r_basis(full_stop_mean)`):

1. **5274c** should not be selected — median fallback is load-bearing and already falsified Test 2 in bustcut.
2. **ae744** is the only 07-11 export with a valid remc 1R cohort (n=11) and matches the prior remc baseline; operator must confirm whether the `BEPAD-TEST` label reflects intended Pine inputs.
3. **8e269** remains the self-funded J1 panel; its shorter span and different remc 1R basis (decompound n=7 vs ae744 n=11) make it a weaker direct match for the 2020-start 3-leg Tradeify book unless operator explicitly wants J1 continuity over span alignment.

**Operator pick (2026-07-15):**

```
PICK: ae744
1R basis pinned: decompound @ $200K — full_stop_mean $2,912.96 (n=11)
Date / initials: 2026-07-15 / JA (operator approve — remc prop-candidate path)
```

**Notes on the pick:** 5274c remains disqualified (median-fallback 1R). 8e269 stays the self-funded J1 panel (`ops/instruments/6J.md`) and is **not** reopened by this pick. Operator accepted ae744 despite PARTIALLY UNKNOWN exact Pine inputs (BEPAD-TEST filename; sizing ≈ v0.3-class from observables). Class-S Aegis-bearing pre-reg may cite this panel + pin; prior looks on the 07-11 Tradeify remc/bustcut runs must still be disclosed in the candidate pre-reg.

---

## §3 — Step 2.4 guard proposal (REPORT-ONLY — not landed)

### Call chain as implemented (read from code)

**Upstream scaling (where the trap fires today):**

1. Tradeify remc / bustcut path — `lab/analysis/tradeify_futures3_remc_2026-07-11/run_tradeify_futures3_remc.py:137-139` calls `pin_r_basis(pd.Series(t["pnl_static"]), R_BASIS_DEFAULT, ACCOUNT)` after decompound reconstruct; scale = `target_1r / r_dollars`.
2. `pin_r_basis` — `.claude/skills/trade-csv-reconcile/scripts/reconcile.py:350-394`:
   - `full_stop_mean`: cohort = losses where `|loss| > 1% × account` (line 375-376)
   - **`n_fs == 0` → silent fallback to median** (lines 379-384), sets `warn=True`
   - `1 <= n_fs < 5` → thin-cohort warning only, still proceeds (lines 386-393)
3. Legacy MC ingest — `core/mc/ingest.py:135-145` `implied_1r()`: **`len(full_stops) < 5` → median fallback** with `fell_back=True` (different threshold than reconcile's zero-only fallback).

**Prop survivor-scoring path (downstream — no 1R guard today):**

4. `lab/discovery/prop_survivor_scoring.py` — **does not import** `pin_r_basis` or `implied_1r`. `score_candidate()` (lines 427-538) accepts pre-built `candidate_daily_pnl` and `full_res_trades`; scaling/normalization is caller responsibility.
5. CLI `main()` (lines 569-631) reads `--daily-pnl-csv` and `--trades-csv` as already-scaled numeric columns — no cohort check.

**Gap:** A future Class-S candidate adapter that scales TV exports → daily P&L before `score_candidate()` will inherit whichever upstream pin method is used. The 5274c defect shows `warn=True` is recorded in remc meta but **does not hard-fail** the run.

### Can the n<5 / zero-full-stop median fallback fire silently in prop scoring?

| Stage | Fallback possible? | Hard-fail today? |
|---|---|---|
| `pin_r_basis` (reconcile) | YES — n=0 full-stops → median | NO — returns `warn=True`, caller continues |
| `implied_1r` (mc/ingest) | YES — n<5 full-stops → median | NO — returns `fell_back=True`, `build_daily_panel` records flag but does not assert |
| `prop_survivor_scoring.score_candidate` | N/A (no 1R logic) | NO — trusts caller-supplied arrays |

### Proposed guard (diff-shaped suggestion — **do not land** without reviewed handoff)

At the candidate-scoring adapter boundary (future module wrapping `score_candidate`, **not** in `lab/discovery/prop_survivor_scoring.py` itself unless separately reviewed):

```python
# After pin_r_basis(pnl_static, "full_stop_mean", account):
method, r_dollars, r_n, warn = pin_r_basis(pnl_static, "full_stop_mean", account)
if r_n == 0 or "FALLBACK" in method:
    raise ValueError(
        f"1R pin fallback blocked for candidate scoring: method={method!r} n={r_n}. "
        f"Panel has zero full-stop cohort after decompound — fix export sizing or pin 1R explicitly."
    )
if warn:  # thin cohort 1 <= n < 5
    raise ValueError(
        f"1R thin-cohort blocked for candidate scoring: n={r_n} full-stops. "
        f"Require n>=5 or operator-pinned fixed 1R."
    )
```

Optionally mirror in `core/mc/ingest.py:build_daily_panel` (lines 160-168): assert `not fell_back` when `fixed_1r_reference is None` on candidate-scoring paths (historical MC anchor paths would remain exempt via explicit `fixed_1r_reference`).

---

## §4 — Manifest repair (Step 2.2)

Four 07-11 Downloads CSVs copied to `core/data/tv_exports/cme/` (naming unchanged):

| File | SHA256 | Bytes |
|---|---|---:|
| `Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_ae744.csv` | `e82a2c25…d148ca38` | 34,824 |
| `Aegis_JPY-Futures_v0.3_BEPAD-TEST_(MJY_6J)_CME_6J1!_2026-07-11_5274c.csv` | `35ae75f2…ca60bed` | 34,430 |
| `Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv` | `9acfa297…ce01b9e` | 59,820 |
| `Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv` | `8884e6dd…ddc6419` | 61,963 |

`core/data/tv_exports/cme/SHA256SUMS` regenerated (`python scripts/check_data_manifests.py --regenerate --dry-run` → `--regenerate`); `python scripts/check_data_manifests.py` exits clean. **Not committed** (per handoff authority).

Note: MYM 15d8b and MNQ beabf are byte-identical to the 07-08 vendor-tree copies already pinned — 07-11 filenames landed for provenance alignment with the remc harness paths.

---

## §5 — Artifacts

| Artifact | Path |
|---|---|
| Decision table (this file) | `lab/analysis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md` |
| Inventory script | `lab/analysis/aegis_6j_transfer_2026-07-05/_panel_inventory.py` |
| Vendor copies + manifest delta | `core/data/tv_exports/cme/*.csv`, `core/data/tv_exports/cme/SHA256SUMS` |

---

## §4 — Extension 2026-07-29: the three later exports + panel-of-record PER PURPOSE

**Why appended, not rewritten.** §1–§3 are the 2026-07-14 reconciliation and the 2026-07-15
operator PICK; they stand byte-unchanged (Trap #12). Three exports **postdate** them and were never
added, which is what made the lineage *look* unreconciled from downstream. Nothing here re-decides
the PICK.

### Full lineage (all figures byte-measured 2026-07-29)

| Export | n | net (raw @export) | span | qty | config |
|---|---:|---:|---|---|---|
| `…PROTOTYPE…07-05_8e269` | 129 | +$39,056.10 | **2022-01-12 → 2026-07-01** | 6–12 | **KNOWN** — cap 12, $1.30/side |
| `…BEPAD-TEST…07-11_ae744` | 152 | +$41,247.30 | **2020-02-24 → 2026-07-01** | 6–12 | PARTIALLY UNKNOWN |
| `…BEPAD-TEST…07-11_5274c` | 152 | +$27,412.95 | 2020-02-24 → 2026-07-01 | **3**–12 | sizing-borne delta vs ae744 |
| `baseline…07-16_3cd61` | 130 | +$31,385.85 | 2022-01-12 → 2026-07-15 | 6–12 | cap 12 — **superseded** |
| **`baseline…07-16_68f0e`** | 130 | **+$22,258.00** | 2022-01-12 → 2026-07-15 | **6–8** | **NATIVE cap 8 + $3.10/side** |
| `…BEPAD-TEST…07-23_6aa5d` | 143 | +$28,562.85 | 2020-07-27 → 2026-07-15 | 3–12 | book-composition input |

### Panel of record, by purpose (this is the thing that was missing)

| Purpose | Panel | Authority |
|---|---|---|
| Self-funded lane / transfer test | **`8e269`** | [`6J.md`](../../../ops/instruments/6J.md) **J1** |
| Prop-candidate remc scoring (decompound @$200K, `full_stop_mean`) | **`ae744`** | operator PICK 2026-07-15 / JA (§3); pinned by the frozen Class-S harness |
| Deployable-config survival work (cap 8, $3.10) | **`68f0e`** | Stage-0 `ENVELOPE-YES`, supersedes `3cd61` |
| Book composition | `6aa5d` | [`paths.py`](../../tradeify_book_composition_2026-07-23/paths.py) |
| — disqualified — | `5274c` | 0 full-stops ⇒ remc median fallback $166.56 (§2) |

**There is no single "panel of record" for 6J and there should not be one** — the purposes differ in
window and sizing basis. Citing "the 6J panel" without naming the purpose is what produced the
`n=1` / `n=10` / `n=11` contradictions downstream.

### Two measured consequences

1. **`68f0e` supersedes the 2026-07-29 linear cap re-scale.** A native cap-8/$3.10 export existed
   all along. Re-measuring the same configuration (constant 0.50×, Tradeify geometry):
   **native 1.04% L13 / 1.38% L26 (net $11,129)** vs **re-scaled 0.67% / 0.77% (net $11,851)** —
   the approximation was **optimistic by ~0.4pp breach and +6.5% net**, so the F2 ±2% precedent
   understated it. Window verdict unchanged (PASS); the caveat is **discharged**.
2. **The 2022-start family cannot serve a composed regime run.** H1 is the 2020–23 chop half and
   `8e269`/`3cd61`/`68f0e` zero-fill it. The H1-covering family (`ae744`/`5274c`/`6aa5d`) contains
   no KNOWN-config member.

### ~~Still open~~ CLOSED 2026-07-29 — `ae744` classified FROM BYTES (ledger J11)

§1 recorded BE-pad k / account size / `max_contracts` as "not determinable from bytes" and routed
the classification to the operator. **That is superseded: it IS determinable, by a test §1 did not
run — per-contract identity across the overlap.**

**`ae744` is the SAME Pine configuration as `8e269`** — v0.3 PROTOTYPE, BE-pad **k=0**, cap **12**,
**$100K**, **$1.30/side** — exported over a **2020-start** window. The `BEPAD-TEST` filename is a
**label carry-over** from the 07-05 experiment layout, not a config indicator.

1. **Decisive:** per-contract P&L is identical on **all 129** overlap days, and the **65 scratch
   (≤1-bar) trades** in that overlap differ in **neither per-contract P&L nor duration**. The BE-pad
   tick-floor acts precisely on the scratch cohort (§J3: scratch mean −225.71 → −210.37 → −181.62,
   wins 9 → 24), so a non-zero k cannot hide there.
2. All **7** differing overlap days differ by **exactly +1 contract** (qty ratio == P&L ratio to
   4 dp) — a TV percent-of-equity compounding artifact of the 23 extra earlier trades (+$1,759 of
   equity by 2022), not a config change.
3. `ae744` belongs to a **matched same-day 3-leg export set** (`…MYM…07-11_15d8b` 2020-01-14→,
   `…MNQ…07-11_beabf` 2020-01-06→) read from `Downloads\` by
   [`run_tradeify_futures3_remc.py`](../tradeify_futures3_remc_2026-07-11/run_tradeify_futures3_remc.py)
   L52-61 — purpose was the 3-leg book re-MC at a common ~2020 window.
4. The BEPAD A/B was three **07-05** replays, k=0 byte-identical to the **129**-trade panel;
   `ae744` is **152** trades dated **07-11** ⇒ not one of those replays.

**Consequence:** `ae744` is a **KNOWN-config, H1-covering** panel, so the "no export is both
KNOWN-config and H1-covering" blocker (Q-6JCOMPOSE-1 §3 P5) **dissolves**. It does *not* predict a
composed PASS — that pre-reg's §4 prior still expects FALSIFIED, and a cap 12→8 re-scale on `ae744`
inherits the known-optimistic bias recorded above.
