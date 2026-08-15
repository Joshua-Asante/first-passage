# Pre-registration — Q-COSTGEO-2: measured execution-cost geometry of the live c1 book (price-anchored fill localization)

**Status:** `FROZEN` — operator signed §9 on 2026-07-23 (chat: *"consider it signed. run P0.1/P0.2"*). No item below changes after any number is seen (Known Trap #12); amendment = close this pre-registration, open a fresh one.
**Freeze semantics:** once signed, no item below changes after any number is seen (Known Trap #12). Amendment = close this pre-registration, open a fresh one.
**Predecessor:** [`Q-COSTGEO-1`](Q-COSTGEO-1-verdict-preregistration.md) (`FROZEN` `a51ce0a`) → [closure `AMBIGUOUS-ALIGNMENT`](../closures/Q-COSTGEO-1-closure-ambiguous.md). **Exactly one row changes** (§2 quote selection); every other frozen item is carried verbatim and is listed in §3 so the carry-over is auditable.
**Loop of record:** STRATEGIC (ops/risk measurement — **not** a discovery campaign; §7).
**Authored:** 2026-07-23 · Claude Code (Opus 4.8), operator-directed.
**Spend:** **$0.00** — `bbo-1s`. `mbp-10` ($115.36/instrument-month) explicitly **not** authorized.

---

## §0 — Rule-0 reads

**Carried verbatim from [`Q-COSTGEO-1` §0](Q-COSTGEO-1-verdict-preregistration.md)** (production anchors unchanged, re-verified 2026-07-23): `cost_mnq.py` @ `e1c51f0` (`SLIPPAGE_TICKS_PER_SIDE = 1.0`, 35–45% of the round trip, unmeasured) · `cost_es.py` (frozen **passive** model, 0.5 tick RT — **4× apart** from the MNQ crossing model, by explicit design: *"do NOT substitute D5's `cost_mnq.py` crossing model"*) · `cost_mgc.py` (crossing, 1.0/side) · **no `cost_mym.py` exists** · `core/firm_rules.py` (Tradeify `cost_per_side_usd = 0.91`) · `ops/c1_rail/c1_sizing_host_reference.py` (`pyr_pct` 750%/1000%; adds sized off **broker-confirmed** base; no slippage term anywhere) · `f2_floors.json` (live qty **MYM 9→67, MNQ 3→30**, `micro_cap` 80) · the two byte-pinned panel CSVs (sha256 verified; span 2020-01-06→2026-06-30; cohorts MYM 232 base/35 add, MNQ 237 base/47 add) · databento cost table (`bbo-1s` **$0.0000**, 144 MB/instrument-month; `mbp-10` **$115.36**).

### New in this pre-registration — banked P0.1 outputs from Q-COSTGEO-1 (measured, not assumed)

- **Timestamp semantics — RESOLVED.** The panel's `Date and time` field is **`America/New_York`, DST-aware**. Anchored against the UTC-stamped bar panel: MYM **96.2%** / MNQ **97.4%** of entry prices fall inside the containing bar's `[low, high]`. Alternatives decisively rejected — `UTC` 0.8/1.1%, `America/Chicago` 31.5/26.7%, fixed `UTC-4` 64.8/68.8%, fixed `UTC-5` 53.6/48.9%. **Pinned as an input here; not re-derived.**
- **Fill convention — RESOLVED, and it is why this pre-registration exists.** Entry prices equal the stamped bar's close **0.0%** of the time and its open **0.0%** of the time, while falling inside its range ~97%. **Entries are intrabar stop fills.** The stamped timestamp therefore denotes **the bar, not the fill instant** — which invalidated Q-COSTGEO-1's timestamp-anchored quote rule.

---

## §1 — Question and what is under test

**Question (symptom form):** every cost-law verdict in this program — and the live c1 rung's own bust calibration — is priced by a slippage constant that was declared, never measured, and which the repo carries at two values 4× apart.

**Under test:** exactly one thing — whether the modeled crossing assumption of **1.0 tick/side** sits **above or below the measured cost floor at the actual fill instant**, at live c1 order sizes, split base vs add, on both legs. Commissions, tick specs, the 4× multiple, allocations, and the live rung are inherited and **not** under test.

---

## §2 — Frozen measurement definition

| Item | Frozen value |
|---|---|
| Instruments | `MYM.v.0`, `MNQ.v.0`, `continuous`, GLBX.MDP3. Volume-lead = the TV `1!` analogue; **not** `.c.0` ([[lesson_roll_rule_changes_bar_existence]]). |
| Schema | **`bbo-1s`**. `mbp-10`/`mbo` out of scope (§5). |
| Span | The panel span exactly: **2020-01-06 → 2026-06-30**. |
| Events | All entry and exit rows of the two byte-pinned panel CSVs. No sub-sampling, no date filter, no outlier removal. |
| Timezone | **`America/New_York`, DST-aware** — banked from Q-COSTGEO-1 P0.1 (§0). Fixed-offset approximations are **forbidden** (§5). |
| Cohorts | **base** vs **add**, from the panel's `Signal` column (`Long`/`Exit Long` = base; `Long Add`/`Exit Long Add` = add). Frozen counts MYM 232/35, MNQ 237/47. |
| Order size | Live sizing from `f2_floors.json` full_median @ WATCH-1 0.50×/$100K: **MYM base 9, add 67; MNQ base 3, add 30.** The panel's own `Size (qty)` column (up to 531) is **not** used (§5). |
| Aggressing side | Long entry ⇒ lifts the **ask**; long exit ⇒ hits the **bid**. |
| **Quote selection** — **THE ONE CHANGED ROW** | **Price-anchored fill localization.** Within the stamped bar's 15-minute window `[t, t+15m)` in UTC, scan `bbo-1s` forward and take the **first** record whose **aggressing-side quote reaches the known fill price** (ask ≤ fill price for a buy; bid ≥ fill price for a sell), within a **±1 tick** tolerance. Measure D1/D2/D3 **at that record**. Rationale: the fill price is known exactly, so it localizes the fill to the second rather than to the quarter-hour. Events that never localize inside the window are recorded **`UNLOCALIZED`** — counted and reported, never silently dropped, and excluded from the medians. |

### Deliverables (per leg × cohort — four cells)

- **D1 — inside-sufficiency rate:** fraction of localized events where live qty ≤ size at the inside on the aggressing side.
- **D2 — half-spread:** in ticks at the localized record; median + p90.
- **D3 — measured cost floor:** ticks per side = D2, reported with D1 as its validity condition.
- **Reported alongside:** `UNLOCALIZED` count/rate per cell.

---

## §3 — Carried verbatim from Q-COSTGEO-1 (auditable carry-over)

Schema · span · event set · cohort definitions and counts · live order sizes · aggressing-side convention · the four-cell reporting structure · **§4 hypothesis, falsifier, and floor asymmetry** · **§5 forbidden moves** (plus two additions) · **§6 verdict table** (with `AMBIGUOUS-ALIGNMENT` replaced by `AMBIGUOUS-LOCALIZATION`) · §7 prior-look and K=0 · commissions, tick specs, `COST_LAW_MULTIPLE = 4.0`, `C1_ALLOCS`, pyramid percentages, the live 0.50× rung, the frozen survivor-scoring floor, and every closed candidate's verdict.

---

## §4 — Falsifiable hypothesis (H-COSTGEO-2)

**H-COSTGEO-2 — if** the measured cost floor (D3) is **below 1.0 tick/side in all four cells** (MYM/MNQ × base/add) with inside-sufficiency (D1) ≥ 90% in each, **then** the modeled crossing assumption is a genuine upper bound at live size, the live c1 bust calibration is conservative on the cost axis, and the margin between measured floor and 1.0 tick/side is the **implicit latency + adverse-selection allowance** the program has been carrying unknowingly.

**Falsifier — FALSIFIED if** the measured floor is **≥ 1.0 tick/side in any cell**. The model then sits at or below the true cost floor: it **understates** execution cost, the live book's bust probability is understated on that leg, and this is a **safety finding raised before B7 arms**.

**Pre-registered primary risk: the add cohort.** 67 (MYM) / 30 (MNQ) lots fire into momentum at 7.5–10× base against a size-invariant constant. Named here, before measurement, so a finding there cannot be presented as a surprise.

**AMBIGUOUS-NEEDS-DEPTH if** D1 < 90% in any cell — more than one order in ten walks past level 1, where `bbo-1s` is structurally blind, so D3 stops bounding cost for that cohort.
**AMBIGUOUS-LOCALIZATION if** the `UNLOCALIZED` rate ≥ 10% in any cell (§6).

### The floor asymmetry (unchanged, load-bearing)

`bbo-1s` measures the cost of crossing **at the prevailing quote assuming immediate fill**. Latency and adverse selection add to real slippage and are invisible to it. Therefore **measured ≥ modeled is directly actionable**; **measured < modeled is not evidence the model is too conservative and licenses no hurdle reduction.** This is why the verdict table contains no "loosen the hurdle" outcome.

---

## §5 — Forbidden moves

*(carried from Q-COSTGEO-1, plus the final two, new to this instrument)*

- **Reading `RESOLVED-CONSERVATIVE` as licence to cut `SLIPPAGE_TICKS_PER_SIDE`, the 4× multiple, or any hurdle.** Forbidden by the floor asymmetry. Lowering the constant requires **realized fills**, not book state.
- **Retro-applying any measured constant to re-open a closed candidate.** D5, D5-RECOST, H-OD-1, MYM-3FPS-1, ORB-ZB-1, F-A/F-B/F-C, NG-EIA-1, RATES-EV-ZF-1 are closed. D5-RECOST-1 already ran that route on the strongest of them: the hurdle fell 3.7× and the edge had decayed negative anyway. Forward-only.
- **Substituting `cost_es.py`'s passive model for `cost_mnq.py`'s crossing model (or vice versa)** to obtain a friendlier number — both are frozen by their own pre-registrations; this instrument **measures**, it does not re-select.
- **Using the panel's `Size (qty)` column** instead of the pinned live quantities.
- **Pulling `mbp-10` or `mbo`.** Escalation is a separate operator decision triggered only by `AMBIGUOUS-NEEDS-DEPTH`.
- **Treating this as a discovery campaign** — no `register_search open`, no K, no DSR floor (§7).
- **Letting any verdict gate or authorize B7.** A FALSIFIED result is a safety input; a RESOLVED result authorizes nothing.
- **Dropping `UNLOCALIZED` or `STALE` events silently** — counted and reported per cell.
- **NEW — using a fixed UTC offset instead of DST-aware `America/New_York`.** Q-COSTGEO-1 P0.1 measured fixed `UTC-4` at 64.8/68.8%: right often enough to pass a spot check, wrong on every DST boundary. The near-miss is more dangerous than the obvious miss.
- **NEW — widening the ±1 tick localization tolerance, or the 15-minute window, to raise the localization rate.** Both are frozen. A low localization rate is a **finding** (`AMBIGUOUS-LOCALIZATION`) indicating the panel's price basis and databento's book disagree — most likely a roll-alignment or feed-vintage difference that must be diagnosed, **not** tuned away.

---

## §6 — Frozen verdict table

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED-CONSERVATIVE` | D3 < 1.0 tick/side in **all four** cells, D1 ≥ 90% in all four, `UNLOCALIZED` < 10% in all four | Model is an upper bound at live size. Record the implicit latency/adverse-selection allowance per cell. **No hurdle change. No sizing change.** Feeds the Q-NAS-ECR-1 successor Pre-Q as its futures-venue cost-proxy band. |
| `FALSIFIED-UNDERSTATED` | D3 ≥ 1.0 tick/side in **any** cell (with D1 ≥ 90% and `UNLOCALIZED` < 10% in that cell) | Model understates cost on that cell. **Raise before B7.** Open an admitting decision to correct `cost_mnq` / author a `cost_mym` model, and re-examine the live bust calibration on the affected leg. Correction direction is **upward only** under this instrument. |
| `AMBIGUOUS-NEEDS-DEPTH` | D1 < 90% in any cell | `bbo-1s` structurally insufficient for that cohort. Escalation to `mbp-10` ($115.36/instrument-month) is a **separate priced operator decision**, not authorized here. |
| `AMBIGUOUS-LOCALIZATION` | `UNLOCALIZED` ≥ 10% in any cell | The panel's fill prices and databento's book disagree at a material rate — diagnose (roll alignment `.v.0` vs TV `1!`, feed vintage, tick rounding) before any cost verdict. **No tuning of tolerance or window.** |

Cells are adjudicated **independently** — a `FALSIFIED-UNDERSTATED` on the MYM add cohort stands on its own and is never averaged against three passing cells.

---

## §7 — Prior-look disclosure and K accounting

**No quote-level data has ever been pulled for MYM or MNQ**, at any schema, in this program — including under Q-COSTGEO-1, which closed at Phase 0 with zero data touched. Every prior databento pull has been `ohlcv-*`. The only pre-existing execution-cost observation is the B6 dry-fire's **−$[redacted]** (n=1, and confounded — it mixes commission, slippage, and market movement across an entry-then-flat holding interval; it is context, not a measurement).

The P0.1 results banked in §0 were derived from **committed/pinned artifacts only** (panel CSVs + bar panel), **not** from any quote series.

**K = 0; no manifest is opened.** This measures a liquidity property of two instruments already in the live book against a pre-declared constant. There is no candidate, no return hypothesis, and no selection over alternatives — therefore no DSR floor and no multiplicity correction ([[lesson_dsr_floor_k_governed]] does not bind). Recorded explicitly so a future audit does not mistake a $0 measurement for an unlogged trial.

---

## §8 — Run protocol (post-signature)

- **P0.1 — fetch-path confirm (BLOCKING).** Re-run the free estimate for `bbo-1s` on both instruments. **Abort if it no longer returns $0.0000** (ADR falsifier: un-estimated billing event ⇒ freeze). Confirm `db_fetch` cache keying separates the two instruments.
- **P0.2 — localization dry-run (BLOCKING).** Pull **one month** of `bbo-1s` (MNQ, most recent full month in span) and run the §2 localization against that month's events. **If the `UNLOCALIZED` rate ≥ 10% on that sample ⇒ `AMBIGUOUS-LOCALIZATION`, stop** — diagnose before spending the full pull. This is the cheap failure-first probe the predecessor lacked.
- **P1 — pull.** `bbo-1s`, both instruments, full span, ~22 GB, $0.00. Local cache; **no `SHA256SUMS` entry** (databento cache is not vendor-CSV estate).
- **P2 — measure.** Emit D1/D2/D3 per leg × cohort, plus `UNLOCALIZED` and `STALE` counts.
- **P3 — adjudicate** §6 per cell; land `RESULTS.md` under `lab/analysis/c1_cost_geometry_2026-07-<dd>/` citing this pre-registration by path.

---

## §9 — Operator signature (gates the pull; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-23 / JA
Authorized: Q-COSTGEO-2 bbo-1s execution-cost geometry measurement on MYM/MNQ,
c1 panel span, base-vs-add cohorts, live sizing from f2_floors.json.
Quote selection = price-anchored intrabar fill localization (the one row changed
from Q-COSTGEO-1); timezone pinned America/New_York DST-aware.
Schema fixed at bbo-1s ($0.00); mbp-10/mbo NOT authorized.
Two-sided: a measured floor >= 1.0 tick/side is a SAFETY finding raised before B7.
Measured-below-modeled licenses NO hurdle reduction (floor asymmetry, §4).
P0.2 one-month localization dry-run is BLOCKING before the full pull.
K=0, no manifest, no candidate. No pull runs before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature gate.
grep -n "SIGNED / FROZEN: ____" docs/briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md \
  && echo "STILL DRAFT — no pull" || echo "signed"

# 2. The one changed row. NOTE (Trap M-AHF): a bare file-wide grep for the predecessor's
#    phrase returns hits from THIS hook's own text — assert on the §2 table row, not the file.
grep -n '^| \*\*Quote selection\*\*' docs/briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md
#    expect: the row names "Price-anchored fill localization"
grep -n '^| Quote selection' docs/briefs/pre-registration/Q-COSTGEO-1-verdict-preregistration.md
#    expect: the predecessor row names the timestamp rule (retained unedited as the record)

# 3. The constant under test, and the 4x sibling that motivates the measurement.
grep -n "SLIPPAGE_TICKS_PER_SIDE" lab/discovery/cost_mnq.py lab/discovery/cost_mgc.py
grep -n "PASSIVE_SLIP_TICKS_RT\|do NOT substitute" lab/discovery/cost_es.py
ls lab/discovery/cost_mym.py 2>/dev/null || echo "no cost_mym.py (the live MYM leg has no model)"

# 4. Live quantities this measurement is pinned to (drift => stale brief).
python -c "import json;d=json.load(open('lab/analysis/c1/q_rail_1_2026-07/f2_floors.json'));\
print([(l['symbol'],l['full_median']['base_capped'],l['full_median']['add_qty']) for l in d['legs']])"
# expect [('MYM', 9, 67), ('MNQ', 3, 30)]

# 5. Schema cost boundary still holds — bbo-1s free, mbp-10 billed.
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema bbo-1s --start 2026-06-01 --end 2026-07-01 | grep cost

# 6. K=0 — no manifest opened by this instrument.
ls discovery_manifests/ | grep -i costgeo || echo "no manifest (correct — K=0)"

# 7. Freeze-before-result.
git log --oneline --reverse -- docs/briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md | head -1
git log --oneline --reverse -- lab/analysis/c1_cost_geometry_2026-07-* 2>/dev/null | head -1
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/Q-COSTGEO-2-verdict-preregistration.md --type inquire

git log -1 --format='%h %ci' -- lab/discovery/cost_mnq.py        # e1c51f0
git log -1 --format='%h %ci' -- lab/discovery/cost_es.py
git log -1 --format='%h %ci' -- ops/c1_rail/c1_sizing_host_reference.py
git log -1 --format='%h %ci' -- core/firm_rules.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | **Signed / FROZEN** (§9) — operator chat authorization *"consider it signed. run P0.1/P0.2"*. Phase 0 authorized. **No item above changed at signature.** | Joshua (JA) |
| 2026-07-23 | Drafted `DRAFT — awaiting operator signature`. Successor to Q-COSTGEO-1 (`AMBIGUOUS-ALIGNMENT`). **One row changed:** quote selection → price-anchored intrabar fill localization, ±1 tick, within the stamped bar window. Banked P0.1 outputs pinned as inputs (TZ `America/New_York` DST-aware; entries are intrabar stop fills). Added `AMBIGUOUS-LOCALIZATION` verdict, a blocking one-month localization dry-run (P0.2) before the full pull, and two forbidden moves (no fixed-offset TZ; no widening tolerance/window to raise the localization rate). All other frozen items carried verbatim per §3. | Joshua (direction) + Claude Code (Opus 4.8) |
