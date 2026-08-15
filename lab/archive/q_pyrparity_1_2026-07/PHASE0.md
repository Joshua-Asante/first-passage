# Q-PYRPARITY-1 — Phase 0 (Pine read): sizing basis + branch selection

**Executed:** 2026-07-17 · Claude Code (CC-reserved Pine read per surface-allocation ADR Test 1; Pine on local disk, sha-verified).
**Parent brief:** [`docs/briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md`](lab/archive/../../docs/briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md) §7 Phase 0.
**Pre-registration:** [`docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md`](lab/archive/../../docs/briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md) — §4 branch slot filled by this read.

---

## 0. Sha precondition (satisfied)

Both locked strategy sources hash-match `core/strategies/MANIFEST.sha256` exactly (verified 2026-07-17, `sha256sum`):

| File | Working-tree sha256 | MANIFEST |
|---|---|---|
| `core/strategies/striker/striker_dj30_v4.5.pine` | `716f8b43…61783` | `716f8b43…61783` ✓ |
| `core/strategies/nas/striker_nas100_v1.pine` | `f5a567b5…57258d` | `f5a567b5…57258d` ✓ |

Locked sources unchanged; the read is against the same bytes the panel-of-record exports were produced from.

---

## 1. Sizing basis → **Branch B** (rolling-equity / compounding)

Both files derive base size through an identical `calcSize`:

```pine
// striker_dj30_v4.5.pine:149-151   |   striker_nas100_v1.pine:202-204
calcSize(stopDist) =>
    risk = strategy.equity * (riskPerTrade / 100)
    stopDist > 0 ? risk / stopDist : 0
```

The sizing basis is **`strategy.equity`** (rolling equity), not `strategy.initial_capital`. NAS100 states it verbatim in-source (`:42` header "SIZING: rolling-equity (strategy.equity * 0.37%). Compounds." + the `riskPerTrade` tooltip `:64`). DJ30 is byte-identical in form.

**⇒ Branch B is selected.** The per-fill statistic is the equity-**normalized** qty ratio `[qty/equity](r0/2) / [qty/equity](r0)`, per the pre-registration §4. Raw qty ratios are *not* usable directly: because size feeds position→P&L→`strategy.equity`, the two runs' equity paths diverge after the first closed trade (the standing "TV CSV compounding artifact"), so a raw ratio drifts from 0.500 even under perfect proportionality. Branch B removes exactly that confound.

`default_qty_type=strategy.percent_of_equity, default_qty_value=100` in both `strategy(...)` headers is the *default* only; every entry passes an explicit computed `qty=`, so the default value is inert for the fills under test.

## 2. Pyramid-add derivation → structurally proportional (CORROBORATING, source-side)

Base entry captures the computed size, and the add is a fixed multiple of that captured value:

```pine
// base entry:  striker_dj30_v4.5.pine:228,239   |   striker_nas100_v1.pine:282,293
size        = calcSize(stopDist)
strategy.entry("Long", strategy.long, qty=size)
initialSize := size

// pyramid add: striker_dj30_v4.5.pine:275-276    |   striker_nas100_v1.pine:329-330
addSize = initialSize * (pyramidSize / 100)
strategy.entry("Long Add", strategy.long, qty=addSize)
```

Substituting: `size = strategy.equity · (riskPerTrade/100) / stopDist`, and `addSize = size · (pyramidSize/100)`. Both legs are **exactly linear in `riskPerTrade`**, and `pyramidSize` (350% DJ30 / 1000% NAS100) is a plain `input.float` in the PYRAMIDING group, independent of the risk input. There is **no `math.round`/`floor`/`ceil`, no `syminfo.mintick`/`pointvalue`, no min-qty clamp anywhere on the sizing path** in either file (grep-confirmed). Halving `riskPerTrade` halves the pre-rounding qty of **both** cohorts by construction.

**Load-bearing subtlety for Phase 2 normalization:** `addSize` is built from `initialSize`, which is captured at the **entry bar** (`initialSize := size`), *not* recomputed off equity at the (later) add bar. So the add cohort's equity basis is the **entry-bar equity**, and — pre-TV-rounding — the add-fill qty ratio *equals* the base-fill qty ratio for the same trade: `addSize(r0/2)/addSize(r0) = initialSize(r0/2)/initialSize(r0)`. Phase 2 must normalize the add fill on entry-bar equity, not add-bar equity, or it will manufacture a spurious deviation.

## 3. Why Phase 1 (the TV runs) is still required — the source proof is corroborating, not sufficient

The §0 item demands a TV *observation* precisely because two behaviors are invisible in Pine source and both live on the deployment surface:

1. **TV integer-contract rounding on MYM1!/MNQ1!** — on a CME futures symbol TV may quantize the computed `qty` to whole contracts at runtime. That quantization is non-linear and is applied to two *different* absolute sizes (base vs the 3.5×/10× larger add), so it is the one channel that could make the add cohort's realized ratio diverge from the base cohort's. This is exactly what the ±0.02 per-fill / ±0.005 median bands are sized to absorb-or-detect, and what the "clipped adds" reject clause guards.
2. **Compounding-path divergence** — handled by Branch B, but only observable in the exports.

Neither is a Pine-source property, so the structural finding here **corroborates** an expected `RESOLVED-PROPORTIONAL` outcome without pre-empting it. The four TV runs proceed as specified.

## 4. Outputs handed to the pre-registration

- **Branch selected: B** (equity-normalized ratio). Recorded in pre-reg §4.
- **Structural proportionality: CONFIRMED-IN-SOURCE (corroborating).** Base and add both exactly linear in `riskPerTrade`; no floor/cap/round/min-qty on the sizing path.
- **Phase-2 normalization rule:** normalize the `Long Add` fill on **entry-bar** equity (the bar its `initialSize` was captured), not add-bar equity.
- **No criterion moved.** The §4 bands and §6 gate are untouched; only the pre-registered "branch selected at Phase 0" slot is filled, exactly as §7 freeze-list item 4 provides.
