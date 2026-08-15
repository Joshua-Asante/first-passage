# Pre-registration — Q-COSTGEO-3: does the live 67-lot MYM add clear the book? (single cell, event-day `tbbo`)

**Status:** `CLOSED — AMBIGUOUS-NEEDS-DEPTH` (2026-07-24). Ran end-to-end at **$3.5767** (budget gate passed): 61/63 localized, **D1 = 0.0%** — the 67-lot MYM add never clears the inside (max displayed depth 30, median 5), so level-1 is structurally too shallow to price it. Substantive finding: the add is ~13× median displayed depth ⇒ the modeled 1.0 tick/side is near-certainly **optimistic** on the add cohort (a pre-B7 safety flag), magnitude unresolved by level-1. `mbp-10` escalation priced at $19.91 (separate decision, not taken). Closure: [`Q-COSTGEO-3-closure-ambiguous-needs-depth.md`](../closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md). Signed §9 `4aa9971` (retained unedited below). — *(original frozen header:)* operator signed §9 2026-07-23, `tbbo` $3.5767 basis, $4.00 ceiling.
**Freeze semantics:** once signed, no item below changes after any number is seen (Known Trap #12). Amendment = close this pre-registration, open a fresh one.
**Predecessors:** [`Q-COSTGEO-1`](Q-COSTGEO-1-verdict-preregistration.md) → [`AMBIGUOUS-ALIGNMENT`](../closures/Q-COSTGEO-1-closure-ambiguous.md) · [`Q-COSTGEO-2`](Q-COSTGEO-2-verdict-preregistration.md) → [`ABORTED at P0.1`](../closures/Q-COSTGEO-2-closure-aborted.md)
**Loop of record:** STRATEGIC (ops/risk measurement — **not** a discovery campaign; §7).
**Authored:** 2026-07-23 · Claude Code (Opus 4.8), operator-directed.
**Budget:** **$3.5767 verified** (day-by-day, §0). Hard ceiling **$4.00** enforced by `--max-cost`; `--force` forbidden (§5).

> **⚠ Spend delta requiring explicit confirmation at §9.** The operator accepted **$3.17** (an *extrapolated* figure for `bbo-1s`). The verified numbers are **`bbo-1s` $2.3370** and **`tbbo` $3.5767**. This pre-registration selects **`tbbo`** on methodological grounds (§2 rationale) at **+$0.41 above the accepted figure**. Signing §9 confirms the $3.5767/ceiling-$4.00 basis. To hold the accepted number instead, decline and re-issue on `bbo-1s` at $2.3370 — accepting the sub-second blind spot in §2.

---

## §0 — Rule-0 reads, with the verification that established each claim

Applying the [Q-COSTGEO-2 closure §5](../closures/Q-COSTGEO-2-closure-aborted.md) rule: **every quantitative or structural claim states how it was verified.** Three prior instruments halted on §0 claims asserted without their one-command check.

| # | Claim | Verified how | Result |
|---|---|---|---|
| 1 | MYM add cohort = **35 entries + 28 exits = 63 rows**, on **34 distinct UTC days** (2020-08-21 → 2026-02-06) | direct parse of the byte-pinned panel, `Signal` column | ✓ |
| 2 | Live MYM add order = **67 contracts** (base 9 × `pyr_pct` 750%) | read [`f2_floors.json`](../../../lab/analysis/c1/q_rail_1_2026-07/f2_floors.json) `full_median`; `pyr_pct` from [`ops/c1_rail/c1_sizing_host_reference.py`](../../../ops/c1_rail/c1_sizing_host_reference.py) L57-60 | ✓ MYM base_capped 9, add_qty 67, total 76, `micro_cap` 80 |
| 3 | MYM tick = **1.0 index pt = $0.50**; $0.50/pt | [`proxy-discipline.md`](../../../.claude/skills/databento-data/reference/proxy-discipline.md) L40 | ✓ `MYM \| $0.50 × index \| 1.0 \| $0.50 \| YM \| $5.00` |
| 4 | **`tbbo` on these 34 days = $3.5767** | `metadata.get_cost` per day, all 34 days summed (28 billed, 6 free from 2025-10-14) | ✓ measured, not extrapolated |
| 5 | **`bbo-1s` on these 34 days = $2.3370** | same, two independent code paths agreeing to the cent ($2.3370 / $2.3371) | ✓ |
| 6 | `tbbo` records carry trade **and** prevailing quote **with sizes** | offline introspection of `databento_dbn.MBP1Msg` | ✓ `price size side action` + `bid_px_00 ask_px_00 bid_sz_00 ask_sz_00 bid_ct_00 ask_ct_00` |
| 7 | `--max-cost` is a **hard abort**, not a warning | read [`db_fetch.py`](../../../lab/databento_fetch/db_fetch.py) L186-192 | ✓ `sys.exit("ABORT: estimated $… exceeds --max-cost …")`; note the `--force` bypass exists → forbidden in §5 |
| 8 | Billing granularity is **per-day** | 15-min vs 1-day estimate byte-identical (2,556,720 B / 31,959 rec) | ✓ sub-day windowing buys nothing |
| 9 | Panel timestamps are **`America/New_York`, DST-aware** | Q-COSTGEO-1 P0.1: MYM 96.2% / MNQ 97.4% of entry prices inside the containing bar; `UTC` 0.8/1.1%, fixed `UTC-4` 64.8/68.8% | ✓ banked |
| 10 | Entries are **intrabar stop fills** — the stamp denotes the bar, not the fill | Q-COSTGEO-1 P0.1: price == bar close **0.0%**, == bar open **0.0%**, ∈ [low,high] ~97% | ✓ banked; this is why §2 is price-anchored |
| 11 | The constant under test: `SLIPPAGE_TICKS_PER_SIDE = 1.0`, and **no `cost_mym.py` exists** | [`cost_mnq.py`](../../../lab/discovery/cost_mnq.py) L24 @ `e1c51f0`; `ls lab/discovery/` | ✓ MYM leg has no committed cost model at all |
| 12 | Tradeify commission **$0.91/side** (index micros) | [`core/firm_rules.py`](../../../core/firm_rules.py) L213 | ✓ not under test |

**Sibling context (not under test):** [`cost_es.py`](../../../lab/discovery/cost_es.py) is a frozen **passive** model at 0.5 tick round-trip — **4× apart** from `cost_mnq`'s crossing model, by explicit design (*"do NOT substitute D5's `cost_mnq.py` crossing model"*). The passive-vs-crossing choice is worth 4× on every cost-law gate and has never been measured on either side. This instrument measures the crossing side on one leg.

---

## §1 — Question and what is under test

**Question (symptom form):** the largest order the live c1 system sends — a 67-lot MYM add fired into a breakout — is priced by a size-invariant slippage constant that was declared, never measured, and for which this leg has no committed cost model at all.

**Under test:** exactly one cell — **MYM × add cohort**. Does 67 contracts clear the inside at the fill instant, and is the measured cost floor above or below the modeled 1.0 tick/side? Commissions, tick specs, the 4× multiple, allocations, the live rung, and all other cells are inherited and **not** under test.

---

## §2 — Frozen measurement definition

| Item | Frozen value |
|---|---|
| Instrument | `MYM.v.0`, `continuous`, GLBX.MDP3 (volume-lead = TV `1!` analogue; **not** `.c.0`). |
| Schema | **`tbbo`.** Chosen over `bbo-1s` (+$1.24) because a stop fill on a breakout is exactly the sub-second event a 1-second subsample can miss: `bbo-1s` could show no snapshot at the fill price, inflating `UNLOCALIZED`. `tbbo` carries the **trade print with the BBO in force at trade time** — the reference's named use for "execution-price studies" — making localization exact rather than approximate. |
| Pull shape | **34 individual event-day pulls** (one per UTC day in the frozen day list), **not** a continuous span. Verified equivalent coverage at ~1.5% of the continuous-span cost. |
| Cohort | **MYM add rows only** — `Signal` ∈ {`Long Add`, `Exit Long Add`}: 35 entries + 28 exits = **63 rows**. |
| Order size | **67 contracts** (live, `f2_floors.json`). The panel's own `Size (qty)` column is **not** used (§5). |
| Timezone | **`America/New_York`, DST-aware.** Fixed offsets forbidden (§5). |
| Aggressing side | `Long Add` ⇒ lifts the **ask** (measure `ask_px_00`, `ask_sz_00`); `Exit Long Add` ⇒ hits the **bid** (`bid_px_00`, `bid_sz_00`). |
| Fill localization | Within the stamped bar's window `[t, t+15m)` UTC, take the **first `tbbo` record whose trade `price` equals the panel's fill price within ±1 tick**. Measure D1/D2/D3 at that record's prevailing quote. Events with no matching print in-window are **`UNLOCALIZED`** — counted and reported, excluded from medians, never silently dropped. |
| Budget | Hard ceiling **`--max-cost 4.00`** per pull invocation. Verified total $3.5767. Any day estimating above ceiling **aborts the run** (§6). |

### Deliverables (single cell)

- **D1 — inside-sufficiency:** fraction of localized events where **67 ≤ size at the inside** on the aggressing side.
- **D2 — half-spread** at the localized record, in MYM ticks; median + p90.
- **D3 — measured cost floor** = D2, in ticks/side, reported with D1 as its validity condition.
- **Reported alongside:** `UNLOCALIZED` count/rate; and, for context only, the distribution of `ask_sz_00` at add moments.

### Honest scope limits (pre-registered, not caveats added later)

- **n = 35 entries over 6.5 years.** This is a **descriptive** measurement of the book at 35 specific historical moments, not an inferential estimate of future add-fill cost. It cannot support a distributional claim about adds in general.
- **Exit coverage is partial.** Some add positions exit via `EOD Flat` (14 MYM rows), which is not distinguishable as add-vs-base from the `Signal` column. The 28 `Exit Long Add` rows are therefore a **subset** of add exits, not all of them. Entries (35) are complete and are the load-bearing side.
- **`tbbo` shows the book as of the trade print**, so D3 remains a **floor** — see the asymmetry below.

---

## §3 — Carried verbatim from Q-COSTGEO-2

The falsifier structure and floor asymmetry (§4) · forbidden-move set (§5, minus the four-cell items, plus three new) · prior-look and K=0 (§7) · commissions, tick specs, `COST_LAW_MULTIPLE = 4.0`, `C1_ALLOCS`, pyramid percentages, the live WATCH-1 0.50× rung, the frozen survivor-scoring floor, and every closed candidate's verdict.

---

## §4 — Falsifiable hypothesis (H-COSTGEO-3)

**H-COSTGEO-3 — if** the measured cost floor (D3) for the MYM add cell is **below 1.0 tick/side** with inside-sufficiency (D1) **≥ 90%**, **then** the modeled crossing assumption is an upper bound for the largest order the live system sends, the live c1 bust calibration is conservative on the cost axis for this leg, and the gap between D3 and 1.0 tick/side is the **implicit latency + adverse-selection allowance** carried unknowingly.

**Falsifier — FALSIFIED if D3 ≥ 1.0 tick/side.** The model then sits at or below the true cost floor on the leg's largest order: it **understates** execution cost, the live book's bust probability is understated, and this is a **safety finding raised before B7 arms**.

**AMBIGUOUS-NEEDS-DEPTH if D1 < 90%** — 67 lots fail to clear the inside on more than one add in ten, so level-1 data stops bounding cost and the true figure requires depth.
**AMBIGUOUS-LOCALIZATION if `UNLOCALIZED` ≥ 10%** — panel fill prices and the GLBX book disagree materially; diagnose before any cost verdict.

### The floor asymmetry (unchanged, load-bearing)

`tbbo` shows the book **at the trade print**. Latency and adverse selection add to real slippage and remain invisible. Therefore **D3 ≥ modeled is directly actionable**; **D3 < modeled is not evidence the model is too conservative and licenses no hurdle reduction.** This is why the verdict table contains no "loosen the hurdle" outcome, and why a benign result changes nothing operationally.

---

## §5 — Forbidden moves

- **Reading `RESOLVED-CONSERVATIVE` as licence to cut `SLIPPAGE_TICKS_PER_SIDE`, the 4× multiple, or any hurdle** — forbidden by the floor asymmetry; lowering the constant requires realized fills.
- **Retro-applying any measured constant to re-open a closed candidate** — D5, D5-RECOST, H-OD-1, MYM-3FPS-1, ORB-ZB-1, F-A/B/C, NG-EIA-1, RATES-EV-ZF-1 are closed. Forward-only.
- **Substituting `cost_es.py`'s passive model for the crossing model** to obtain a friendlier number — this instrument measures; it does not re-select between frozen models.
- **Using the panel's `Size (qty)` column** instead of the pinned 67.
- **Using a fixed UTC offset** instead of DST-aware `America/New_York` — measured at 64.8% for MYM; the near-miss is more dangerous than the obvious miss.
- **Widening the ±1 tick localization tolerance or the 15-minute window** to raise the localization rate — both frozen; a low rate is a **finding**, not a tuning target.
- **Pulling `mbp-10`/`mbo`, or any instrument other than MYM, or any cohort other than add** — escalation is a separate priced operator decision triggered only by §6.
- **Passing `--force` to `db_fetch pull`** — it bypasses the `--max-cost` abort (verified §0 #7). The ceiling is the budget control; `--force` voids this pre-registration.
- **Treating this as a discovery campaign** — no `register_search open`, no K, no DSR floor (§7).
- **Letting any verdict gate or authorize B7** — a FALSIFIED result is a safety input; a RESOLVED result authorizes nothing.
- **NEW — inferring the MNQ add cell, or either base cell, from this result.** No *a fortiori* rule is pre-registered. It is *plausible* that MNQ's 30-lot add on a heavier-traded contract clears if MYM's 67-lot add does, but **relative depth between MYM and MNQ has not been measured**, and baking an unmeasured ordering into a decision rule is the exact error class that halted three prior instruments. Whether the other cells are worth their cost is a fresh decision after a real number exists.
- **NEW — generalizing n=35 into a distributional claim** about future add-fill cost (§2 scope limits).

---

## §6 — Frozen verdict table

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED-CONSERVATIVE` | D3 < 1.0 tick/side **and** D1 ≥ 90% **and** `UNLOCALIZED` < 10% | The modeled constant bounds the largest live order on this leg. Record the implicit latency/adverse-selection allowance. **No hurdle change, no sizing change, no rung change.** Feeds the Q-NAS-ECR-1 successor Pre-Q as its futures-venue cost-proxy band. Whether to buy the remaining three cells becomes a fresh decision. |
| `FALSIFIED-UNDERSTATED` | D3 ≥ 1.0 tick/side (D1 ≥ 90%, `UNLOCALIZED` < 10%) | Model understates cost on the live book's largest order. **Raise before B7.** Open an admitting decision to author `cost_mym.py` and re-examine the MYM leg's bust calibration. Correction direction **upward only** under this instrument. |
| `AMBIGUOUS-NEEDS-DEPTH` | D1 < 90% | 67 lots walk past level 1 on >1 add in 10. `tbbo` structurally insufficient. Escalation to `mbp-10` is a **separate priced operator decision** — and note the same-day `mbp-10` rate is ~100× this instrument's per-day cost. |
| `AMBIGUOUS-LOCALIZATION` | `UNLOCALIZED` ≥ 10% | Panel fill prices vs GLBX book disagree materially — diagnose roll alignment (`.v.0` vs TV `1!`), feed vintage, or tick rounding. **No tolerance/window tuning.** |
| `ABORTED-BUDGET` | Any day's estimate pushes the run above the `--max-cost 4.00` ceiling | Stop. Re-price and return to the operator. **No `--force`.** |

---

## §7 — Prior-look disclosure and K accounting

**No quote- or trade-level data has ever been pulled for MYM or MNQ**, at any schema, in this program — including under Q-COSTGEO-1 and Q-COSTGEO-2, both of which closed at Phase 0 with zero data touched. Every prior databento pull has been `ohlcv-*`. The only pre-existing execution-cost observation is the B6 dry-fire's **−$[redacted]** (n=1, confounded: it mixes commission, slippage, and market movement across an entry-then-flat holding interval).

All §0 figures derive from committed/pinned artifacts, offline package introspection, and **free metadata endpoints** — **no price or trade series has been retrieved, inspected, or analysed.**

**K = 0; no manifest opened.** This measures a liquidity property of an instrument already in the live book against a pre-declared constant. No candidate, no return hypothesis, no selection over alternatives ⇒ no DSR floor, no multiplicity correction. Recorded explicitly so a future audit does not mistake a paid measurement for an unlogged trial.

---

## §8 — Run protocol (post-signature)

- **P0 — re-estimate the frozen day list (BLOCKING).** Re-run `metadata.get_cost` for all 34 days at `tbbo`. **Abort if the total exceeds $4.00.** (This is the Q-COSTGEO-2 guard, now with a verified number behind it rather than an extrapolation.)
- **P1 — pull.** 34 event-day `tbbo` pulls via `db_fetch pull --max-cost 4.00`, MYM.v.0. No `--force`. Local DBN cache; **no `SHA256SUMS` entry** (databento cache is not vendor-CSV estate).
- **P2 — localize.** Apply §2 fill localization to all 63 add rows; emit the localized-record table and `UNLOCALIZED` list.
- **P3 — measure.** Emit D1, D2, D3 + the `ask_sz_00` distribution at add moments.
- **P4 — adjudicate** §6; land `RESULTS.md` under `lab/analysis/c1_cost_geometry_mym_add_2026-07-<dd>/` citing this pre-registration by path; record actual spend against the $3.5767 estimate.

---

## §9 — Operator signature (gates the pull; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-23 / JA
Authorized: Q-COSTGEO-3 — MYM add cohort only, 34 event-days, schema tbbo.
CONFIRMS the $3.5767 verified basis and the $4.00 --max-cost ceiling, which is
$0.41 ABOVE the previously accepted $3.17 (that figure was an extrapolation for
bbo-1s; tbbo is chosen for exact fill localization, §2).
Single cell: MYM x add @ 67 contracts. No MNQ, no base cells, no mbp-10, no --force.
Two-sided: D3 >= 1.0 tick/side is a SAFETY finding raised before B7.
D3 < modeled licenses NO hurdle reduction (floor asymmetry, §4).
K=0, no manifest. No pull runs before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature gate.
grep -n "SIGNED / FROZEN: ____" docs/briefs/pre-registration/Q-COSTGEO-3-verdict-preregistration.md \
  && echo "STILL DRAFT — no pull" || echo "signed"

# 2. Budget ceiling is a hard abort and --force is available (hence forbidden in §5).
grep -n "exceeds --max-cost" lab/databento_fetch/db_fetch.py

# 3. The constant under test; and the missing MYM model that motivates the cell choice.
grep -n "SLIPPAGE_TICKS_PER_SIDE" lab/discovery/cost_mnq.py
ls lab/discovery/cost_mym.py 2>/dev/null || echo "no cost_mym.py — the live MYM leg has no model"

# 4. Live order size this measurement is pinned to (drift => stale brief).
python -c "import json;d=json.load(open('lab/analysis/c1/q_rail_1_2026-07/f2_floors.json'));\
print([(l['symbol'],l['full_median']['base_capped'],l['full_median']['add_qty']) for l in d['legs']])"
# expect [('MYM', 9, 67), ('MNQ', 3, 30)]

# 5. Cohort counts from the byte-pinned panel (primary checkout; gitignored).
grep -c "Long Add" "core/data/tv_exports/cme/Striker_DJ30_v4.5_MYM_CBOT_MINI_MYM1!_2026-07-11_15d8b.csv"
# expect 63 (35 'Long Add' entries + 28 'Exit Long Add')

# 6. Budget still holds at run time (must be <= $4.00 across the 34 frozen days).
#    Re-run the P0 day-list re-estimate; verified 2026-07-23 at $3.5767.

# 7. K=0 — no manifest opened.
ls discovery_manifests/ | grep -i costgeo || echo "no manifest (correct — K=0)"

# 8. Freeze-before-result.
git log --oneline --reverse -- docs/briefs/pre-registration/Q-COSTGEO-3-verdict-preregistration.md | head -1
git log --oneline --reverse -- lab/analysis/c1_cost_geometry_mym_add_* 2>/dev/null | head -1
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/Q-COSTGEO-3-verdict-preregistration.md --type inquire

git log -1 --format='%h %ci' -- lab/discovery/cost_mnq.py            # e1c51f0
git log -1 --format='%h %ci' -- lab/databento_fetch/db_fetch.py
git log -1 --format='%h %ci' -- ops/c1_rail/c1_sizing_host_reference.py
git log -1 --format='%h %ci' -- core/firm_rules.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | **Signed / FROZEN** (§9) — operator chat *"tbbo, sign §9 accordingly and run it."*, confirming the `tbbo` $3.5767 basis + $4.00 ceiling (the acknowledged +$0.41 over the earlier-accepted extrapolated $3.17). Phase 0 authorized. **No item above changed at signature.** | Joshua (JA) |
| 2026-07-23 | Drafted `DRAFT — awaiting operator signature`. Third successor in the cost-geometry line. Scope cut from four cells to **one** (MYM × add @ 67 lots) — the only cell with real prior uncertainty. Pull shape changed from continuous span to **34 event-days**. Schema changed to **`tbbo`** for exact trade-anchored fill localization. **Every §0 claim carries its verification** (12-row table) per the Q-COSTGEO-2 closure lesson; cost is measured day-by-day ($3.5767), not extrapolated. Hard `--max-cost 4.00` ceiling with `--force` forbidden. Added `ABORTED-BUDGET` verdict, explicit n=35 descriptive-not-inferential scope limit, partial-exit-coverage disclosure, and a forbidden move against inferring the unmeasured cells. | Joshua (direction) + Claude Code (Opus 4.8) |
