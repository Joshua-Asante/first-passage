**Theme:** c1
# Sub-100K band integer-quantization sweep — RESULTS

**Status:** ACTIVE — MNQ zero-floors at every FRIENDLY tier below 100K under the locked-proportional split; the two published 50K clearers describe a book the integer rail cannot instantiate

**Verdict class:** `MEASURED` — arithmetic only, no MC, no gate scored, **no verdict claimed**
**Date:** 2026-08-02
**Trigger:** operator directive to run the 50K-band measurement bundle. This is the bundle's
arithmetic limb; the bust-scoring limb is **not** run here and needs its own pre-registration (§5).
**Cost:** $0 · no K · no manifest · no pull · nothing armed · no locked surface touched.

---

## §0 — Method and controls

**The law, verbatim from production** ([`ops/c1_rail/c1_sizing_host_reference.py:295`](../../../ops/c1_rail/c1_sizing_host_reference.py)):

```python
reserve_cap = math.floor(cap_alloc / (1 + pyr_pct / 100))
```

with locked Pine pyramids **MYM 750%** / **MNQ 1000%**, and the locked 100K split
**MYM `cap_alloc` 69 / MNQ 11** against `micro_contract_cap` 80. A leg with `reserve_cap = 0`
never sends (base floors to zero), i.e. **the leg is dead at that tier**.

**Two controls, both MATCH — the arithmetic is not novel, it is the production law re-applied:**

| Control | Expected | Got | |
|---|---|---|---|
| Sizing host's own pinned comment (`:76-79`) — *"MYM base 8 + add 60 = 68, MNQ base 1 + add 10 = 11, combined 79 ≤ 80"* | 8+60=68 · 1+10=11 · 79 | 8+60=68 · 1+10=11 · 79 | **MATCH** |
| Published T-50K quantization result ([`eval_shape_diagnostics_2026-07-28`](../eval_shape_diagnostics_2026-07-28/RESULTS.md) Part A appendix) — *"MNQ zero-floors `floor(5/11)=0` → 1-leg MYM book, aggregate 34/40"* | MNQ dead; MYM realized 34/40 | MNQ `floor(5/11)=0`; MYM base 4 + add 30 = **34**/40 | **MATCH** |

---

## §1 — Finding 1: under the LOCKED-PROPORTIONAL split, MNQ dies at every tier below 100K

Scaling the locked 69/11 proportionally (`cap_alloc = floor(share × cap_firm / 80)`):

| Tier | cap | MYM alloc → reserve | MNQ alloc → reserve | Realized book |
|---|---:|---|---|---|
| `Tradeify_Select_100K` | 80 | 69 → **8** | 11 → **1** | **2-leg**, 79/80 |
| `Tradeify_Select_50K` | 40 | 34 → 4 | 5 → **0 DEAD** | **1-leg MYM**, 34/40 |
| `MFFU_Rapid_50K` | 50 | 43 → 5 | 6 → **0 DEAD** | **1-leg MYM** |
| `BluSky_Premium_50K` | 50 | 43 → 5 | 6 → **0 DEAD** | **1-leg MYM** |
| `Bulenox_50K` | 70 | 60 → 7 | 9 → **0 DEAD** | **1-leg MYM** |
| `Bulenox_25K` | 30 | 25 → 2 | 4 → **0 DEAD** | **1-leg MYM** |
| `Tradeify_Select_25K` | 10 | 8 → **0 DEAD** | 1 → **0 DEAD** | **nothing trades** |

**Mechanism:** MNQ's 1000% pyramid makes `reserve_cap = floor(cap_alloc/11)`, so MNQ needs
`cap_alloc ≥ 11`; the proportional rule supplies `floor(11 × cap/80)`, which reaches 11 only at
`cap ≥ 80`. **This extends the published T-50K result — previously read as a T-50K quirk — to the
entire sub-100K band at every FRIENDLY firm.**

**Load-bearing consequence.** `Tradeify_Select_50K` **1.06%** and `MFFU_Rapid_50K` **0.96%** are the
estate's *only* mechanical Part A clearers and the sole basis on which the 2026-11-08 demotion clause
is defeated. Both were measured on a **continuously-sized 2-leg book that the integer rail cannot
realize at those tiers.** The realizable proportional book there is 1-leg MYM, whose bust
**has never been measured** (verified this session by `rg --no-ignore` over `lab/`, `lab/archive/`,
`docs/`, `docs/ltm/` — no MYM-only sub-100K MC exists).

---

## §2 — Finding 2 (and a correction to §1's first reading): re-allocation DOES rescue MNQ

⚠ **An earlier in-session statement of mine — *"MNQ survives only at cap ≥ 80"* — is too strong and
is corrected here.** It is true of the *proportional* split only. Exhaustive search over every
integer split `(MYM, MNQ)` with both `reserve_cap ≥ 1` and realized aggregate ≤ `cap_firm`:

| Tier | cap | Viable 2-leg splits | Max-MYM viable split | Realized |
|---|---:|---:|---|---|
| `Tradeify_Select_50K` | 40 | **21** | MYM 29 / MNQ 11 | 25 + 11 = 36/40 |
| `MFFU_Rapid_50K` | 50 | **31** | MYM 39 / MNQ 11 | 34 + 11 = 45/50 |
| `BluSky_Premium_50K` | 50 | **31** | MYM 39 / MNQ 11 | 34 + 11 = 45/50 |
| `Bulenox_50K` | 70 | **51** | MYM 59 / MNQ 11 | 51 + 11 = 62/70 |
| `Bulenox_25K` | 30 | **11** | MYM 19 / MNQ 11 | 17 + 11 = 28/30 |
| `Tradeify_Select_25K` | 10 | **0** | — | **no viable 2-leg split at any allocation** |

**Smallest `micro_contract_cap` admitting any 2-leg book: 20.** So only `Tradeify_Select_25K` is
structurally 1-leg; every other sub-100K tier is 1-leg *by allocation choice*, not by construction.

**This is a finding, not a recommendation.** Picking "max-MYM among 21 viable splits" is selection
over an allocation space — best-of-K one layer below the tier layer the frozen gate already fences
(survivor-scoring pre-reg §5 bars *"post-hoc tier substitution after seeing per-tier results"*). Any
split adopted for scoring must be fixed by a **pre-registered rule stated before the bust is seen**
(§5).

---

## §3 — What this does and does not establish

**Establishes:**
- The published sub-100K Part A figures describe books the integer rail does not realize at those
  tiers under the locked-proportional split.
- The realizable proportional expression is 1-leg MYM (or, at T-25K, nothing).
- A 2-leg expression exists at every sub-100K tier except T-25K, but only via re-allocation.

**Does NOT establish:**
- **Any bust rate.** No MC was run. The 1-leg MYM book and the re-allocated 2-leg books are
  **unmeasured**, and nothing here predicts them — dropping the low-variance MNQ leg changes the
  book's loss-side shape, which is the property Q-GEOFIT-1 showed governs trailing-DD survival.
- **That the 11-08 demotion clause is or is not still defeated.** The band re-score's clearers stand
  as *published*; whether an unrealizable-at-tier book can carry that clause is an adjudication, not
  an arithmetic result, and belongs to the operator.
- **Anything about the live 100K account.** `Tradeify_Select_100K` is unaffected — 69/11 realizes
  2-leg at 79/80, exactly as deployed. **No `LEG_MAP` change is implied or proposed**; Q-CAPALLOC-2
  closed `RESOLVED-FRAGILE` with the operator electing DECLINE, and that stands.

---

## §4 — Reproduction

```bash
python lab/analysis/band_quantization_2026-08-02/run_band_quantization.py
# Prints both controls, the proportional table (§1), and the exhaustive split search (§2).
```

---

## §5 — What is owed before any bust number

The bundle's remaining limbs score a **new book shape** against the frozen Part A gate, which is
gate-scoring with real best-of-K exposure (two book shapes × six tiers × an allocation space). Per the
survivor-scoring pre-registration's §5 and Known Trap #12 they require a **fresh, frozen
pre-registration** naming, before any result is seen: the tier set, the book shapes, the
allocation-selection rule, the partitions, the controls, and the verdict vocabulary.

**Not authored here.** Deliberately — authoring it in the same pass that produced the motivating
arithmetic is how a selection rule gets fitted to a number the author has already glimpsed.

**Also re-scoped by this result:** the MFFU-50K corrected-bootstrap repair (the impeached 4.49%
figure, never re-measured after M-23) now describes a **book that tier cannot realize** under the
proportional split. It remains an owed repair of a published figure, but its decision value has
dropped and it should queue behind the realizable-cell scoring, not ahead of it.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-02 | Initial. Two controls MATCH. §1 extends the published T-50K zero-floor to the whole sub-100K band; §2 corrects an in-session overreach of mine (*"MNQ survives only at cap ≥ 80"* — true of the proportional split only) and finds 11–51 viable re-allocated 2-leg splits per tier, T-25K excepted | Claude Code (Opus 5) |
