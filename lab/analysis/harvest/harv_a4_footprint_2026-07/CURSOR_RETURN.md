# CURSOR_RETURN — A4 month-end footprint diagnostic

**Handoff:** `docs/briefs/handoffs/2026-07-14-cursor-handoff-a4-crowd-vs-death-diagnostic.md` (v3)
**Branch:** `cursor/a4-footprint-diagnostic` @ `a762500` (worktree from `origin/main`)
**Interpreter:** `C:/Users/joshu/multi_firm_operations/.venv-research/Scripts/python.exe`

---

## HANDOFF-VERIFY

```
HANDOFF-VERIFY: PASS
toplevel: C:/Users/joshu/multi_firm_operations/.worktrees/a4-footprint-diagnostic
branch: cursor/a4-footprint-diagnostic @ a762500 (tracks origin/main; no commits ahead of main yet)
checked:
  - docs/briefs/handoffs/2026-07-14-cursor-handoff-a4-crowd-vs-death-diagnostic.md (present)
  - docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md (present)
  - lab/archive/harv_0_month_end_rebalance_es_2026-07/{build_panel,run_harv0,chunked_pull}.py (present)
  - docs/adr/2026-07-13-harv-discovery-lane-ratification.md (Accepted; HARD gate §2)
  - lab/analysis/harv_a4_footprint_2026-07/ absent before this run (premises not already executed)
proceed: Phase-0 read-report below, then §2 TDD build
```

---

## §0 — Phase 0 read-report

### A4 memo (`docs/briefs/programs/2026-07-14-a4-flow-data-fork-scoping.md`) — §4 + §8

**§4 (disposition map, memo-frozen):** price-only footprint + timing-migration on the in-hand `ohlcv-1d` panel.
- Footprint attenuation → **H-death → DROP** the successor.
- Footprint flat + reversion migrates earlier → **H-crowd → GO** on earlier-entry / alt-instrument successor.
- Ambiguous → leans NO-GO on era-decay alone.

**§8 (substance):** the closure's "price data cannot" was too strong — the *realized edge/spread* cannot distinguish crowd from death, but other price observables can (weakly): month-end **volume footprint**, conditioning **|R_spread| magnitude**, and **entry-timing migration**. Recorded in the memo, not edited into the closed Q-HARV-0 record.

**Narrowing assertion (this handoff v2/v3 vs memo §4):** this diagnostic **collapses the non-identifying GO branch into DEFER by design**. Surviving outputs are **DROP** (both primary channels co-move to attenuation) and **DEFER** (anything else). **No GO** output exists. Timing migration is retained **informational-only** and cannot drive a call. Asserted against handoff §4; building a GO path would be a defect.

### `build_panel.py` (archive; last touch `47cc3eb` 2026-07-12)

- **`load_symbol_frame` (L56–83):** parquet → ET settle_date → **drop weekend settle_dates** (`dayofweek <= 4`) → sort/dedupe → returns **`[["open","high","low","close"]]` only — DROPS `volume`**. §2.1 needs a volume-preserving variant that reuses the settle/weekend logic.
- **`signal_from_r_spread` (L107–113):** qualifying ≡ `signal != 0` ≡ **|R_spread| ≥ 100bp** (truncation floor). Magnitude among qualifying is NOT a clean primary (handoff A2 uses un-truncated count instead).
- **`build_monthly_panel` columns:** `year, month, month_id, n_trading_days, T_1..T_4, R_spread, R_spread_bp, window, C, G, placebo, reversal_T1_to_next_T3, signal, signed_window, signed_C, qualifying, quarter_end, micro_era` (+ optional `ym_*` / `gc_*`).
- **L149–151:** `R_spread` conditioning window **ends at `close[T-4]`**. T-4 is the **selection endpoint**; raw T-4→… returns inherit mechanical drift. Frozen — import/copy, never edit.

### `run_harv0.py` — `perm_test_signed` + `effect_on`

- **`perm_test_signed`:** label-permutation of signal across months; recomputes `mean(signal * window)` on `|signal|>0`; P(effect ≥ observed). Does **not** shuffle returns within months.
- **`effect_on`:** on qualifying rows, mean signed effect + σ + **1.96·SE CI** + `perm_test_signed` p + trade_rate. Timing leg reuses this signed-effect + permutation + CI pattern (informational only).

### `chunked_pull.py` — symbols / schema / range

- Parents: `ES.c.0 YM.c.0 ZN.c.0 GC.c.0`; micros: `MES.c.0 MYM.c.0`.
- Schema: **`ohlcv-1d`**, `--stype continuous`, range **2010-06-06 → 2026-07-01**.
- **Volume:** Vendor `ohlcv-*` bar aggregates carry `volume`. Archived `load_symbol_frame` drops it; footprint premise depends on keeping it. Pre-run gate must refuse if the column is absent.

### ADR `2026-07-13-harv-discovery-lane-ratification.md` §2

- Mechanism-first lane ratified; **HARD gate:** every bundled clause needs a written **reachability attestation** under a plausible-true world before `K-budget search open`.
- Spirit binds this diagnostic: both **DROP** and **DEFER** must be reachable from the real ~163-event panel (and from synthetic fixtures offline), not only from crafted impossibilities.

### §0.5 defaults — applied as parent-confirmed (no contradiction from Phase-0 reads)

| ID | Default | Phase-0 check |
|----|---------|---------------|
| A | Primary = ES ex-QE volume-bump + qualifying-count rate (era-split) | Consistent; count is un-truncated |
| B | Eras 2010–2017 vs 2018–2026 on `T_1.year` | Matches Q-HARV-0 decay split |
| C | Timing informational only; T-4 caveat required | Required — selection endpoint at L149–151 |
| D | ZN / all-months / \|R_spread\| median = corroboration only | OK |
| E | Roll-harden baseline (exclude months whose trailing-21 ending T-4 overlaps roll week); ex-QE filters event | Matches NOTES (mid-month quarterly roll) |
| F | DROP iff both primaries shrink with non-overlapping CIs; else DEFER | Reachability-preserving; no GO |
| G | Report MDE (bootstrap CI half-width) | OK |

**No §0.5 ambiguities.** Proceeding to §2.

---

## Implementation progress

See status block at end of this file after offline suite completes.

---

## §6 — Status return

```
Status: DONE
Per-step gates: 2.1 [PASS] 2.2 [PASS] 2.3 [informational PASS] 2.4 [PASS] 2.5 [PASS] 2.6 [refusal-only PASS]
§0.5 resolutions applied: A=ES ex-QE volume-bump + qualifying-count rate B=2010-2017 vs 2018-2026 on T_1.year C=timing informational D=ZN/all-months/|R_spread| corroboration only E=roll-harden both windows (ex-QE event + baseline roll-week drop) F=co-movement non-overlapping CIs G=MDE bootstrap CI half-width reported
Diffs (files touched): lab/analysis/harv_a4_footprint_2026-07/* only (a4_footprint.py, test_a4_footprint.py, CURSOR_RETURN.md)
Concerns surfaced: (1) git diff vs fcf8f32 on archive/core/CLAUDE is non-empty due to later main commits after fcf8f32 — working tree does not modify those paths (git diff HEAD -- those paths is empty). (2) DEFER destination is the v3 Q-KBUDGET-1 inventory / new-axis requirement (Q-HARV-1 declined); encoded in data-reachability paragraph.
Next action recommended: operator runs the pull (skill Rule 1) then 2.6 real pass
```

## §10 — Audit hook outputs (offline)

### No data acquisition in new code
```
(empty — good)
```

### No GO output / no build-authorization
```
(empty after excluding never/defer lines — good; argparse help uses 'Operator flag')
```

### No pre-T-4 entry computed
```
no pre-T-4 entry computed — good
```

### Archived study + locked core untouched (vs HEAD)
```
git diff HEAD -- lab/archive/harv_0_month_end_rebalance_es_2026-07/ core/ CLAUDE.md
(empty)
```

### Offline suite
```
................                                                         [100%]
16 passed in 12.98s

```

### Boundaries
```
check_boundaries: OK — 21 first-party modules, no illegal edges, no name collisions.

```

### Files produced
- `lab/analysis/harv_a4_footprint_2026-07/a4_footprint.py`
- `lab/analysis/harv_a4_footprint_2026-07/test_a4_footprint.py`
- `lab/analysis/harv_a4_footprint_2026-07/CURSOR_RETURN.md`

**Not committed / not pushed** per dispatch instructions.
