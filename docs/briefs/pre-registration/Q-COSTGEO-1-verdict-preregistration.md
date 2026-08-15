# Pre-registration — Q-COSTGEO-1: measured execution-cost geometry of the live c1 book (MYM/MNQ, base vs add)

**Status:** `CLOSED — AMBIGUOUS-ALIGNMENT` (2026-07-23). Signed + FROZEN `a51ce0a`, then closed at Phase 0 **with zero data touched**: P0.1 resolved the timezone (`America/New_York`, DST-aware) and in doing so established that entries are **intrabar stop fills**, so the §2 quote-selection rule below — which assumes the stamped timestamp is the fill instant — would have sampled the book up to 15 min early and suppressed both non-benign verdicts. **Closed rather than amended** (Trap #12). Successor: [`Q-COSTGEO-2`](Q-COSTGEO-2-verdict-preregistration.md) (one row changed). Closure: [`Q-COSTGEO-1-closure-ambiguous.md`](../closures/Q-COSTGEO-1-closure-ambiguous.md). **This file is retained unedited below the status line as the record of what was authorized.**
**Freeze semantics:** once signed, no item below changes after any number is seen (Known Trap #12). Amendment = close this pre-registration, open a fresh one.
**Loop of record:** STRATEGIC (ops/risk measurement — **not** a discovery campaign; see §7).
**Authored:** 2026-07-23 · Claude Code (Opus 4.8), operator-directed.
**Spend:** **$0.00** — `bbo-1s` estimated free this session (§0). Any escalation to `mbp-10` is a **separate priced decision** (§6 `AMBIGUOUS-NEEDS-DEPTH`).

---

## §0 — Rule-0 reads (production source, verified 2026-07-23)

- **[`lab/discovery/cost_mnq.py`](../../../lab/discovery/cost_mnq.py) @ `e1c51f0`** — the constant under test. `SLIPPAGE_TICKS_PER_SIDE = 1.0` (L24); `MNQ_TICK_VALUE = $0.50` (L20); `COST_LAW_MULTIPLE = 4.0` (L25); `mnq_rt_cost_usd = 2 × (commission + 1.0 × $0.50)` (L50-51). A **crossing** model. At Bulenox `$0.61`/side the slippage term is **45% of the round trip**; at Tradeify `$0.91`/side, **35%**. Never measured.
- **[`lab/discovery/cost_es.py`](../../../lab/discovery/cost_es.py) @ read this session** — the **same program's other cost model**, and it is **4× apart**: `PASSIVE_SLIP_TICKS_RT = 0.5` — "HALF a tick for the WHOLE round trip (not per side)" (L26) — vs `cost_mnq`'s 1.0/side = 2.0 RT. Its docstring is explicit that this is deliberate and frozen: *"FROZEN model (do NOT substitute D5's `cost_mnq.py` crossing model)"* (L6). **Not a bug — but it means the passive-vs-crossing choice is worth a 4× swing in the gate and is currently made by authorial declaration per brief, never by measurement.**
- **[`lab/discovery/cost_mgc.py`](../../../lab/discovery/cost_mgc.py)** — `SLIPPAGE_TICKS_PER_SIDE = 1.0` (L16), same crossing form as MNQ. **No `cost_mym.py` exists** — the live book's MYM leg has no committed cost model in `lab/discovery/`.
- **[`core/firm_rules.py`](../../../core/firm_rules.py) @ read this session** — `cost_per_side_usd`: Bulenox `0.61` (L91, "all-in, MNQ/MYM; MGC=$0.76"), **Tradeify `0.91`** (L213, the live firm). Commissions are primary-sourced and **not** under test here.
- **[`ops/c1_rail/c1_sizing_host_reference.py`](../../../ops/c1_rail/c1_sizing_host_reference.py) @ read this session** — live sizing. `pyr_pct` **750% (MYM)** / **1000% (MNQ)** (L57-66); add qty = `floor(executed_base × pyr_pct/100)` (L269). **Adds are 7.5–10× the base and are sized off the broker-confirmed base**, not the intended base (L254). No slippage term anywhere in the sizing path.
- **[`lab/analysis/c1/q_rail_1_2026-07/f2_floors.json`](../../../lab/analysis/c1/q_rail_1_2026-07/f2_floors.json)** — the **live quantities at WATCH-1 0.50× / $100K** (full_median basis): **MYM base 9 → add 67 → total 76**; **MNQ base 3 → add 30 → total 33**; `micro_cap` 80.
- **Byte-pinned c1 panel** (read from the primary checkout; both sha256 verify) — `…MYM1!_2026-07-11_15d8b.csv` `9acfa297…` and `…MNQ1!_2026-07-11_beabf.csv` `8884e6dd…`; span **2020-01-06 → 2026-06-30**. Cohort counts from the `Signal` column: **MYM 267 entries (232 base / 35 add)**; **MNQ 284 entries (237 base / 47 add)**. Exit signals present (`Exit Long`, `Exit Long Add`, `EOD Flat`, `Max Hold`).
- **Databento cost + volume, measured 2026-07-23 (free metadata endpoints; no data pulled):** `MNQ.v.0` `bbo-1s` 1 month → **$0.0000**, 144 MB, 1.80M records. `tbbo` → $0.0000, 2.69 GB. `mbp-1` → $0.0000, 58.4 GB. **`mbp-10` → $115.36** (billing boundary). Full c1 span at `bbo-1s` ≈ **11 GB/instrument, ~22 GB both legs, $0.00**.
- **Only pre-existing execution-cost observation:** the B6 dry-fire realized **−$[redacted]** over a 4-order round trip ([`RUNBOOK.md` §B6](../../notes/rail_build/RUNBOOK.md)). **This is not a slippage measurement** — it conflates commission, slippage, and market movement across the holding interval of an entry-then-flat sequence, on n=1. It is cited as context, and as evidence that no usable measurement exists.

---

## §1 — Question and what is under test

**Question (symptom form):** every cost-law verdict in this program — and the live c1 rung's own bust calibration — is priced by a slippage constant that was declared, never measured, and which the repo itself carries at two values 4× apart.

**Under test:** exactly one thing — whether the **modeled crossing assumption of 1.0 tick/side is above or below the measured cost floor** at live c1 order sizes, split base vs add, on both legs. Commissions, tick specs, the 4× cost-law multiple, allocations, and the live rung are **all inherited and not under test**.

---

## §2 — Frozen measurement definition

| Item | Frozen value |
|---|---|
| Instruments | `MYM.v.0` and `MNQ.v.0`, `continuous` stype, GLBX.MDP3. Volume-lead (`.v.0`) is the TV `1!` analogue — **not** `.c.0` ([[lesson_roll_rule_changes_bar_existence]]). |
| Schema | **`bbo-1s`** (1-second top-of-book). Estimated $0.0000. **`mbp-10`/`mbo` are out of scope** and forbidden without a separate priced decision (§5). |
| Span | The c1 panel span exactly: **2020-01-06 → 2026-06-30**. No extension, no shortening. |
| Events | All entry and exit rows of the two byte-pinned panel CSVs (MYM 267 entries, MNQ 284 entries, plus paired exits). No sub-sampling, no date filtering, no outlier removal. |
| Cohorts | **base** vs **add**, assigned from the panel's own `Signal` column (`Long` / `Exit Long` = base; `Long Add` / `Exit Long Add` = add). Frozen counts: MYM 232/35, MNQ 237/47. |
| Order size | **Live sizing from `f2_floors.json` full_median @ WATCH-1 0.50× / $100K**: MYM base **9**, add **67**; MNQ base **3**, add **30**. **The panel's own `Size (qty)` column (up to 531) is NOT used** — it is a %-equity backtest artifact at scaled equity, not a live order size (§5). |
| Aggressing side | Long entry ⇒ lifts the **ask**; long exit ⇒ hits the **bid**. Half-spread measured on the aggressing side only. |
| Quote selection | The last `bbo-1s` record at or before the event's UTC timestamp. If the gap to the preceding quote exceeds **60 s**, the event is recorded `STALE` and excluded from the medians (count reported, never silently dropped). |

### Deliverables (per leg × cohort — four cells)

- **D1 — inside-sufficiency rate:** fraction of events where live qty ≤ size at the inside on the aggressing side.
- **D2 — half-spread distribution:** in ticks, median + p90.
- **D3 — measured cost floor:** ticks per side = half-spread (D2). Reported with D1 as its validity condition.

---

## §3 — Inherited unchanged (cited, not re-decided)

Commissions (`firm_rules.cost_per_side_usd`, primary-sourced 2026-07-13) · tick specs (MYM $0.50/pt, MNQ $2.00/pt) · `COST_LAW_MULTIPLE = 4.0` · `C1_ALLOCS` 0.70%/0.37% · pyramid 750%/1000% · the live WATCH-1 **0.50×** rung · the frozen survivor-scoring floor · every closed candidate's verdict.

---

## §4 — Falsifiable hypothesis (H-COSTGEO)

**H-COSTGEO — if** the measured cost floor (D3) is **below 1.0 tick/side in all four cells** (MYM/MNQ × base/add) with inside-sufficiency (D1) ≥ 90% in each, **then** the modeled crossing assumption is a genuine upper bound at live size, the live c1 bust calibration is conservative on the cost axis, and the margin between measured floor and 1.0 tick/side is the **implicit latency + adverse-selection allowance** the program has been carrying unknowingly.

**Falsifier — H-COSTGEO is FALSIFIED if** the measured floor is **≥ 1.0 tick/side in any cell**. Then the model is at or below the true cost floor, meaning it **understates** execution cost — the live book's bust probability is understated on the leg where it fires, and this is a **safety finding to be raised before B7 arms**.

**The falsifier is expected to be most at risk on the add cohort**, which fires 67 (MYM) / 30 (MNQ) lots into momentum — 7.5–10× base — against a size-invariant constant. Pre-registered as the primary risk, not discovered after the fact.

**AMBIGUOUS-NEEDS-DEPTH if** D1 < 90% in any cell: more than one order in ten walks past level 1, where `bbo-1s` is structurally blind, so D3 stops being a valid floor for that cohort. The 90% line is set because at that rate level-1 data systematically understates cost rather than bounding it.

### The floor asymmetry (load-bearing; see §5)

`bbo-1s` measures the **cost of crossing at the prevailing quote assuming immediate fill**. Latency and adverse selection add to real slippage and are **invisible** to it. Therefore:

- **measured ≥ modeled** is *directly actionable* — the model is definitely too optimistic.
- **measured < modeled** is **not** evidence the model is too conservative, and **licenses no hurdle reduction.** It only quantifies the implicit allowance.

This asymmetry is the reason the verdict table has no "loosen the hurdle" outcome.

---

## §5 — Forbidden moves

- **Reading `RESOLVED-CONSERVATIVE` as licence to cut `SLIPPAGE_TICKS_PER_SIDE`, the 4× multiple, or any hurdle.** The single most tempting move, and the one the floor asymmetry (§4) forbids outright. Lowering the constant requires **realized fills**, not book state. A measured floor of 0.4 ticks does **not** mean cost is 0.4 ticks.
- **Retro-applying any measured constant to re-open a closed candidate.** D5, D5-RECOST, H-OD-1, MYM-3FPS-1, ORB-ZB-1, F-A/F-B/F-C, NG-EIA-1, RATES-EV-ZF-1 are closed. D5-RECOST-1 already ran the cost-re-derivation route on the strongest of them: the hurdle fell 3.7× and the edge had decayed negative anyway. A cost measurement is **forward-only**.
- **Substituting `cost_es.py`'s passive model for `cost_mnq.py`'s crossing model (or vice versa) to obtain a friendlier number.** Both are frozen by their own pre-registrations; this instrument **measures**, it does not re-select between them.
- **Using the panel's `Size (qty)` column instead of the pinned live quantities.** Panel qty reaches 531 — a %-equity artifact at scaled backtest equity. Measuring book sufficiency against it would manufacture an insufficiency finding that has no live counterpart.
- **Pulling `mbp-10` or `mbo` under this pre-registration.** $115.36/instrument-month. Escalation is a separate operator decision triggered *only* by `AMBIGUOUS-NEEDS-DEPTH`, mirroring Rule 2's escalate-only-after-survival ladder.
- **Treating this as a discovery campaign** — no `register_search open`, no K, no DSR floor. It measures a liquidity property of instruments already in the live book, not a return hypothesis (§7).
- **Letting any verdict here gate or authorize B7.** A `FALSIFIED-UNDERSTATED` result is a safety input to the arm decision; a `RESOLVED-CONSERVATIVE` result authorizes nothing. B7 stays gated on M1 `RESOLVED` + its own operator GO.
- **Dropping `STALE` events silently** — they are counted and reported (§2), because a systematic quote gap at entry times would itself be a finding.

---

## §6 — Frozen verdict table

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED-CONSERVATIVE` | D3 < 1.0 tick/side in **all four** cells **and** D1 ≥ 90% in all four | Model is an upper bound at live size. Record the implicit latency/adverse-selection allowance per cell. **No hurdle change. No sizing change.** Feeds the Q-NAS-ECR-1 successor Pre-Q as its futures-venue cost-proxy band. |
| `FALSIFIED-UNDERSTATED` | D3 ≥ 1.0 tick/side in **any** cell (D1 ≥ 90% in that cell) | Model understates cost on that cell. **Raise before B7.** Open an admitting decision to correct `cost_mnq`/add a `cost_mym` model, and re-examine the live bust calibration on the affected leg. Correction direction is **upward only** under this instrument. |
| `AMBIGUOUS-NEEDS-DEPTH` | D1 < 90% in **any** cell | `bbo-1s` is structurally insufficient for that cohort. Report per-cell; escalation to `mbp-10` ($115.36/instrument-month) is a **separate priced operator decision**, not authorized here. |
| `AMBIGUOUS-ALIGNMENT` | P0.1 timestamp-alignment gate fails | Events cannot be located in quote time. **No pull proceeds**; no cost verdict. |

Cells are reported independently — a `FALSIFIED-UNDERSTATED` on the MYM add cohort stands on its own and is **not** averaged away against three passing cells.

---

## §7 — Prior-look disclosure and K accounting

**No quote-level data has ever been pulled for MYM or MNQ**, at any schema, in this program. Every prior databento pull has been `ohlcv-1m`/`ohlcv-1h`/`ohlcv-1d`. The only execution-cost observation in existence is the B6 dry-fire's −$[redacted] (n=1, confounded — §0). Cohort counts, live quantities, and the cost constants in §0 were read from committed/pinned artifacts, **not** from any quote series.

**K = 0, and no manifest is opened.** This measures a liquidity property of two instruments already in the live book against a pre-declared constant. There is **no candidate, no return hypothesis, no selection over alternatives, and therefore no DSR floor and no multiplicity correction** ([[lesson_dsr_floor_k_governed]] does not bind). Recording this explicitly so a future audit does not mistake a $0 measurement for an unlogged trial.

---

## §8 — Run protocol (post-signature)

- **P0.1 — timestamp alignment (BLOCKING).** Establish the mapping from the panel's `Date and time` field to UTC. **Anchor it against a real source**: match ≥20 known panel events to `core/data/bar_data/{MYM,MNQ}_M15.csv` (UTC-stamped) and confirm entry prices fall within the corresponding bar's high/low. **Fail ⇒ `AMBIGUOUS-ALIGNMENT`, stop — no pull.** ([[lesson_offline_port_needs_real_source_anchor]]; the panel is a TV export and TV display TZ is ET, so a naive UTC read would misalign every lookup by hours.)
- **P0.2 — fetch-path confirm.** Confirm `db_fetch` handles `bbo-1s` end-to-end (estimate already clears) and that cache keying separates the two instruments. Re-run the free estimate; **abort if it no longer returns $0.0000** (ADR falsifier: un-estimated billing event ⇒ freeze).
- **P1 — pull.** `bbo-1s`, both instruments, panel span, ~22 GB, $0.00. Cache locally; **no `SHA256SUMS` entry** (databento cache is not vendor-CSV estate).
- **P2 — measure.** Emit D1/D2/D3 per leg × cohort, plus `STALE` counts.
- **P3 — adjudicate** §6 per cell; land `RESULTS.md` under `lab/analysis/c1_cost_geometry_2026-07-<dd>/` citing this pre-registration by path.

---

## §9 — Operator signature (gates the pull; DRAFT until filled)

```
SIGNED / FROZEN: 2026-07-23 / JA
Authorized: Q-COSTGEO-1 bbo-1s execution-cost geometry measurement on MYM/MNQ,
c1 panel span, base-vs-add cohorts, live sizing from f2_floors.json.
Schema fixed at bbo-1s ($0.00); mbp-10/mbo NOT authorized.
Two-sided: a measured floor >= 1.0 tick/side is a SAFETY finding raised before B7.
Measured-below-modeled licenses NO hurdle reduction (floor asymmetry, §4).
K=0, no manifest, no candidate. No pull runs before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature gate.
grep -n "SIGNED / FROZEN: ____" docs/briefs/pre-registration/Q-COSTGEO-1-verdict-preregistration.md \
  && echo "STILL DRAFT — no pull" || echo "signed"

# 2. The constant under test, and the 4x sibling that motivates the measurement.
grep -n "SLIPPAGE_TICKS_PER_SIDE" lab/discovery/cost_mnq.py lab/discovery/cost_mgc.py
grep -n "PASSIVE_SLIP_TICKS_RT\|do NOT substitute" lab/discovery/cost_es.py

# 3. Live quantities this measurement is pinned to (drift => this brief is stale).
python -c "import json;d=json.load(open('lab/analysis/c1/q_rail_1_2026-07/f2_floors.json'));\
print([(l['symbol'],l['full_median']['base_capped'],l['full_median']['add_qty']) for l in d['legs']])"
# expect [('MYM', 9, 67), ('MNQ', 3, 30)]

# 4. Cohort counts from the byte-pinned panel (primary checkout; gitignored).
grep -c "Long Add" "core/data/tv_exports/cme/Striker_NAS100_v1_CME_MINI_MNQ1!_2026-07-11_beabf.csv"

# 5. Schema cost boundary still holds — bbo-1s free, mbp-10 billed.
PYTHONPATH=lab .venv-research/Scripts/python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema bbo-1s --start 2026-06-01 --end 2026-07-01 | grep cost

# 6. No discovery manifest was opened by this instrument (K=0).
ls discovery_manifests/ | grep -i "costgeo" || echo "no manifest (correct — K=0)"

# 7. Freeze-before-result: this file's commit predates any results artifact.
git log --oneline --reverse -- docs/briefs/pre-registration/Q-COSTGEO-1-verdict-preregistration.md | head -1
git log --oneline --reverse -- lab/analysis/c1_cost_geometry_2026-07-* 2>/dev/null | head -1
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/Q-COSTGEO-1-verdict-preregistration.md --type inquire

git log -1 --format='%h %ci' -- lab/discovery/cost_mnq.py        # e1c51f0
git log -1 --format='%h %ci' -- lab/discovery/cost_es.py
git log -1 --format='%h %ci' -- ops/c1_rail/c1_sizing_host_reference.py
git log -1 --format='%h %ci' -- core/firm_rules.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-23 | **Signed / FROZEN** (§9) — operator chat authorization *"apply my §9 signature"*. Phase 0 authorized. **No item above changed at signature**; the only edits in this commit are the §9 block, the status line, and this row. | Joshua (JA) |
| 2026-07-23 | Drafted `DRAFT — awaiting operator signature`. Schema fixed at free `bbo-1s`; cohorts base-vs-add from the panel's own `Signal` column; order size pinned to live `f2_floors.json` quantities (MYM 9/67, MNQ 3/30) rather than panel qty; falsifier two-sided with the **dangerous** direction (understated cost) as the action-firing one; floor asymmetry pre-registered so a low reading cannot be read as licence to cut the hurdle; `mbp-10` escalation ring-fenced as a separate priced decision; K=0 recorded explicitly. | Joshua (direction) + Claude Code (Opus 4.8) |
