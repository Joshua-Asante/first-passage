# MNQSR-1 RESULTS — Phase-1 MNQ S/R structure screen

**Status:** CLOSED — 0/14 BH-FDR survivors; Phase B/C not licensed. (Catalog stamp CLOSED = archive-owed HOLD.)  
**Run id:** `mnqsr1_structure_20260806b` (seed-fixed RESULTS pin; see also closed `mnqsr1_structure_20260806`)  
**Window:** 2025-08-06 → 2026-08-04 (ET)  
**Seed:** 20260806  
**K:** 14 primary cells (BH-FDR α=0.05)

## Coverage

```json
{
  "window": ["2025-08-06", "2026-08-04"],
  "n_rth_sessions": 257,
  "n_event_rows": 12697,
  "n_primary_hits": 701,
  "n_vwap_days": 257,
  "vwap_hit_rate": 1.0,
  "run_id": "mnqsr1_structure_20260806b",
  "seed": 20260806,
  "note": "vwap_hit_rate=1.0 is a construct disclosure (expanding-sigma early |z|); see Caveats"
}
```

## Primary cell table

| family | limb | n | delta | CI 95% | p | verdict |
|---|---|---:|---:|---|---:|---|
| prior_rth | attraction | 256 | 0.0137 | [-0.0273, 0.0547] | 0.5380 | **FAIL** |
| prior_rth | reaction | 82 | -0.0366 | [-0.1220, 0.0610] | 0.5146 | **FAIL** |
| overnight | attraction | 256 | -0.0039 | [-0.0449, 0.0371] | 0.8874 | **FAIL** |
| overnight | reaction | 106 | 0.0283 | [-0.0566, 0.1132] | 0.5574 | **FAIL** |
| std_pivot | attraction | 256 | -0.0176 | [-0.0527, 0.0195] | 0.3706 | **FAIL** |
| std_pivot | reaction | 63 | 0.0159 | [-0.0794, 0.1111] | 0.8512 | **FAIL** |
| fib_pivot | attraction | 256 | 0.0547 | [0.0156, 0.0938] | 0.0086 | **FAIL** |
| fib_pivot | reaction | 85 | 0.0235 | [-0.0588, 0.1059] | 0.6586 | **FAIL** |
| camarilla | attraction | 256 | -0.0059 | [-0.0527, 0.0410] | 0.8360 | **FAIL** |
| camarilla | reaction | 92 | 0.0217 | [-0.0652, 0.1087] | 0.7136 | **FAIL** |
| atr | attraction | 243 | 0.0000 | [0.0000, 0.0000] | 1.0000 | **FAIL** |
| atr | reaction | 16 | 0.0625 | [-0.1250, 0.2500] | 0.7762 | **VOID-POWER** |
| vwap | attraction | 257 | 0.0000 | [0.0000, 0.0000] | 1.0000 | **FAIL** |
| vwap | reaction | 257 | -0.0233 | [-0.0817, 0.0350] | 0.4880 | **FAIL** |

## ToD diagnostics (primary touches)

| family | n | tod_med | IQR |
|---|---:|---:|---|
| prior_rth | 82 | 682 | [636, 766] |
| overnight | 106 | 689 | [624, 786] |
| std_pivot | 63 | 696 | [648, 799] |
| fib_pivot | 85 | 672 | [605, 770] |
| camarilla | 92 | 710 | [641, 800] |
| atr | 16 | 760 | [693, 822] |
| vwap | 257 | 574 | [573, 577] |

## Phase-2 gate

- **Rule:** B requires reaction PASS; C requires attraction PASS and reaction PASS
- **Phase B (candle confirmation) licensed:** *(none)*
- **Phase C (VP / L2) licensed:** *(none)*

## Caveats

1. **No BH-FDR survivor at K=14.** Closest naive hit: `fib_pivot:attraction` p=0.0086 (still above BH rank-1 floor α/K ≈ 0.00357).
2. **VWAP construct:** expanding session σ makes |z|≥2 nearly immediate (ToD ~09:34; hit_rate=1.0). Attraction Δ vs shuffle is zero under that pathology. A min-bars-before-z gate is a **new** cell (PREREG §5).
3. **ATR reaction VOID-POWER** (n=16 < 50). Not interpreted.
4. Seed-fixed RESULTS pin is `mnqsr1_structure_20260806b` (deterministic `_FAMILY_SEED`; never `hash(family)`).

## Disposition

Phase-1 screen **CLOSED** under this freeze: no family licenses Phase B (candles) or Phase C (VP/L2). Notice-phase only — no trade entry.
