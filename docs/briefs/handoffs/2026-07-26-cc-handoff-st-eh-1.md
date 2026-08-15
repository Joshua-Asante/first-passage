# CC HANDOFF — ST-EH-1
## Supertrend harness: long-panel baseline + pre-registered sensitivity sweep (MNQ / MYM)

**Date authored:** 2026-07-25
**Author:** claude.ai advisor session (parent)
**Spawn type:** Claude Code execution session
**Campaign ID:** ST-EH-1 (log trial counts under this ID in the anomaly-discovery K-ledger)
**Template note:** `references/cc_handoff.md` was not readable from the authoring
environment; structure follows brief-authoring SKILL.md checks 1–10 directly.
Flag any drift from the canonical template on first read.

---

## §0 — Rule-0 production reads

### §0-A Parent-side reads (verified at authoring time, 2026-07-25)

| Artifact | Anchor | What was verified |
|---|---|---|
| `ST-EH_CME_MINI_MNQ1__2026-07-25_80e00.csv` | upload 2026-07-25; n=551 (550 closed + 1 open); span 2025-08-31 22:15 → 2026-07-24 16:45 | New-format TV export (`Trade number`, `Commission USD`, FE/AE, `Duration (bars)`); Commission sums to $0.00; Signal = `ST(10,3)` + one `Open` mark-to-market row; entry minutes all :00/:15/:30/:45 (15m confirmed); 23 distinct entry hours + Sunday entries (24h Globex, no session filter); long/short 275/276; flip-share 99.8% (flip-only confirmed) |
| `ST-EH_CBOT_MINI_MYM1__2026-07-25_c93ef.csv` | upload 2026-07-25; n=550; same span | Same structure; long/short 275/275; flip-share 99.8%; Commission $0.00 |
| `supertrend_edge_harness.pine` (ST-EH v0.1) | authored 2026-07-25, this session | Replication spec extracted verbatim into §2 Phase 2 below — the spawn does NOT need TradingView access |

### §0-B Spawn-side Phase-0 reads (MANDATORY before any §2 execution)

`cat` each file below and report a one-line content confirmation BEFORE proposing
or running anything. If a file is missing, return `NEEDS_CONTEXT` naming it —
do not reconstruct from memory.

1. `ops/instruments/MNQ.md` and `ops/instruments/MYM.md` — instrument ledgers
   (active concepts, dead lists, durable findings). Read before deriving.
2. `scripts/db_fetch.py` — cost-gated Databento puller (estimate + pull modes).
3. `scripts/step0_battery.py`, `scripts/selection_tests.py`,
   `scripts/plateau_tracker.py` — validation tooling.
4. The frozen futures cost-model doc (Bulenox/Tradeify/MFFU per-side constants,
   ORB-MNQ-1 vintage). If no standalone doc exists, use the constants in §3 and
   flag `DONE_WITH_CONCERNS`.
5. `DATABENTO_API_KEY` presence in env (`echo ${DATABENTO_API_KEY:+set}`) —
   never print the key.

---

## §0.5 — Clarifying questions (HALT and surface before §2; do not guess)

The spawn must surface these to the operator and receive answers before Phase 1.
Ambiguity-defaulting on any of them can waste the session.

1. **TV chart timezone** for the two exports — assumed `America/New_York`
   (Sunday 22:15/22:45 entries are consistent with ET Globex evening). Confirm.
2. **Back-adjustment on MNQ1!/MYM1!** — TV continuous defaults to NOT
   back-adjusted. Confirm the toggle state at export time. This changes how many
   roll-artifact flips the 1-yr panels contain (~4 quarterly rolls in span).
3. **Slippage setting** in the TV Properties tab — Commission verified $0.00
   from the CSV; slippage cannot be read from the export. Confirm zero.
4. **Canonical cost model for ST-EH-1** — §3 assumes Tradeify
   ($0.91/side + 1 tick/side). Confirm, or name Bulenox/MFFU instead.
5. **Repo root / branch** for deliverables (assumed `research/st_eh/` under the
   discovery-stack repo).
6. **Grid axes confirmation** — §2 Phase 5 pre-registers ATR period × multiplier
   only, on 15m. Timeframe is explicitly OUT of this campaign (any TF axis is a
   new pre-reg). Confirm before run 1.

---

## §1 — Context

**Doctrine links.** ST-EH-1 sits inside the instrument-first research direction
(MNQ/MYM per-instrument profiling, raised 2026-07-23). The harness (ST-EH v0.1)
was built 2026-07-25 to convert signal-emitting TV indicators into exportable
strategy panels. ORB-MNQ-1 pre-reg §5 precedent applies: better-looking slices
observed mid-campaign do not authorize amendment. Prior is LOW — raw Supertrend
on liquid index futures is among the most publicly mined constructs in
existence; a cheap kill is an acceptable and likely outcome, and the harness
generalizes regardless.

**What the 1-yr panels show (baseline config: ST(10,3), hl2, RMA ATR,
flip-only, no filters, 1 contract, ZERO costs):**

| | MNQ | MYM |
|---|---|---|
| N (closed) | 550 | 549 |
| WR | 36.8% | 37.8% |
| PF | 1.026 | 1.049 |
| Net (zero-cost) | +$2,076 | +$1,201 |
| Avg/trade (zero-cost) | +$3.77 | +$2.18 |
| Bootstrap 90% CI on avg/trade | [−$26.12, +$32.95] | [−$7.07, +$11.96] |
| P(expectancy ≤ 0), zero-cost | 0.42 | 0.35 |
| Costed @ $2.82/RT: avg/trade | +$0.95 | −$0.64 |
| P(expectancy ≤ 0), costed | 0.49 | 0.56 |
| Max DD ($, 1 contract) | $12,877 | $2,436 |

**The load-bearing read:** at the Tradeify cost model the round-trip hurdle is
$2.82 and the ≥4× convention requires ~$11.28/trade. MYM is negative net of
costs at 1×; MNQ clears 1× but sits at ~1.3× — both are coin flips
(P(≤0) ≈ 0.5 costed) and neither is anywhere near 4×. MNQ additionally gave
back its entire accumulated P&L intra-panel (DD $12,877 vs peak P&L $12,790).

**Therefore:** the question this campaign answers is NOT "is PF 1.03–1.05
stable over more years." It is (a) whether the 1-yr result is representative of
a regime-diverse 16-yr panel, and (b) whether ANY cell of a pre-registered
(period × multiplier) grid clears the costed hurdle with selection effects
priced. The sweep runs as characterization; promotion of any cell is gated
(§2 Phase 6). A green cell in a dead-baseline grid is selection until proven
otherwise.

**Why TradingView cannot answer this:** TV bar history caps the 15m panel at
~11 months (observed span). Longer panels require the Databento/Python
replication path — which is also the only way to run the grid on one engine and
one feed (same-feed baseline rule).

---

## §2 — Execution plan

Run phases in order. Each phase has a binary gate; do not start phase N+1 with
phase N unresolved.

### Phase 0 — Rule-0 reads
Per §0-B. Report contents. Gate: all present → proceed; any missing →
`NEEDS_CONTEXT`.

### Phase 1 — Data acquisition (databento discipline, Rules 1–4)

1. **Estimate first, every pull** (`db_fetch.py estimate`, free). Never a bare
   `get_range`.
2. Pulls (schema `ohlcv-1m`, GLBX.MDP3, cost-gated `--max-cost 5.00` each,
   total ceiling $20; if any estimate exceeds its ceiling → report and
   `NEEDS_CONTEXT`):
   - `NQ` continuous, 2010-06-06 → present (parent, discovery panel)
   - `YM` continuous, 2010-06-06 → present (parent, discovery panel)
   - `MNQ` continuous, 2019-05-06 → present (native micro, OOS gate)
   - `MYM` continuous, 2019-05-06 → present (native micro, OOS gate)
3. **Roll rule:** confirm the continuous roll-rule letter and price-adjustment
   behavior against the symbology docs BEFORE the deep pull — do not assume.
   Requirement for signal generation: a back-adjusted (gap-free) series,
   because Supertrend bands are price-level recursions and unadjusted roll gaps
   manufacture flips. If Databento continuous is not price-adjusted, stitch raw
   expiries locally with a documented calendar-roll rule and back-adjust;
   record the rule in the session record.
4. **Resample 1m → 15m** anchored to :00/:15/:30/:45 `America/New_York`,
   bar timestamp = bar open, 24h Globex calendar with the 17:00–18:00 ET
   maintenance halt excluded (no synthetic bars in the halt). Document the
   resample convention.
5. Cache DBN + parquet under `data/cache/glbx/`; re-pulls must hit cache.

### Phase 2 — Engine + replication fidelity gate (MANDATORY before any long-panel claim)

Implement the Supertrend engine exactly as the harness computes it:

```
src   = hl2
atr   = RMA(true_range, 10)            # harness default useRmaAtr = true
up    = src - mult*atr
up    = max(up, up_prev)  if close[1] > up_prev  else up
dn    = src + mult*atr
dn    = min(dn, dn_prev)  if close[1] < dn_prev  else dn
trend = +1 start; -1→+1 when close > dn_prev; +1→-1 when close < up_prev
        (up_prev / dn_prev = prior bar FINAL adjusted values, nz-seeded)
signal evaluated on bar close; fill at NEXT bar open; always-in-market
stop-and-reverse; no costs at signal layer (costs applied in analysis)
```

Warm up the recursion from ≥ 2025-06-01 so RMA converges before the fidelity
window. Then run 2025-08-31 → 2026-07-24 on native MNQ and MYM 15m series and
reconcile against the two uploaded CSVs (closed trades only; drop the open
mark-to-market row):

| Check | Tolerance | On fail |
|---|---|---|
| Closed-trade count | ±2% | HALT → `NEEDS_CONTEXT` |
| Entry-timestamp Jaccard | ≥ 0.95 | HALT → `NEEDS_CONTEXT` |
| Gross profit / gross loss | each ±5% | HALT → `NEEDS_CONTEXT` |
| Direction agreement on matched entries | ≥ 98% | HALT → `NEEDS_CONTEXT` |

Note: HIGH Jaccard is the goal here (replication fidelity). This is the
opposite use from the §6 path-independence clause in pre-reg doctrine, where
high cross-feed Jaccard means "same path, not independent evidence." Do not
confuse the two.

Report trades whose holding period spans a roll (count per symbol) — these are
the expected residual mismatch source.

### Phase 3 — Panel integrity (Step-0 equivalent)
Run the Step-0 battery logic on every generated panel: entry-minute census vs
15m, session/hour coverage, DOW census, duplicate detection, n-bounds vs prior
runs. Machine-check, not eyeball.

### Phase 4 — Long-panel baseline (the primary deliverable)

On NQ and YM parents, 2010-06-06 → present, ST(10,3) baseline:
- Report zero-cost AND costed (per §3) per-trade expectancy, PF, WR, N,
  max DD, in both native points and micro-scaled dollars (×0.1 parent→micro
  economics; parent dollars are NOT micro dollars).
- Bootstrap 10K: 90% CI on costed expectancy, P(≤0), P(≥ 4× hurdle).
- Pre-registered slices (calendar years only — no post-hoc slicing):
  per-year costed expectancy table, plus halves and thirds stationarity.
- Native micro era (MNQ/MYM 2019-05-06 → present) reported separately as the
  OOS/regime-consistency gate. Parent-era results are discovery-only until the
  micro-era gate is checked (proxy discipline).

### Phase 5 — Pre-registered sensitivity sweep (characterization, all cells reported)

Grid, frozen before run 1: **ATR period ∈ {7, 10, 14, 21} × multiplier ∈
{2.0, 2.5, 3.0, 3.5, 4.0}** = 20 cells per symbol, 15m, hl2, RMA ATR,
flip-only, same engine, same feed, same span as Phase 4. K = 40 grid trials +
4 baselines (2 × 1-yr TV already run, 2 × long-panel) — log K=44 under
ST-EH-1 in the anomaly-discovery ledger.

Output: every cell's costed expectancy, CI, PF, N, max DD — the full 20-cell
table per symbol. No cell is omitted for any reason.

### Phase 6 — Selection accounting + promotion rule (pre-registered)

A cell is promotable to CANDIDATE only if ALL of:
1. Costed bootstrap 90% CI lower bound > 0 on the 2010→present parent panel;
2. Costed point expectancy ≥ 4× RT hurdle on the same panel;
3. Native micro-era (2019-05→present) costed expectancy > 0;
4. Grid-adjacent neighbors: ≥ 6 of available adjacent cells costed-positive,
   dome shape not cliff (plateau read);
5. Best-of-20 demeaned null (selection_tests best-of-K): P(best ≥ observed
   | zero-edge grid) < 0.05, per symbol.

Zero promotable cells → the grid closes dead with K logged; that is a clean,
useful result. Session record must include the "which nulls remain alive"
ledger (what each passed test killed, what it did not — e.g., permutation
kills random-labeling, not path-overfit).

### Phase 7 — Deliverables

- `research/st_eh/engine.py` (+ tests reproducing the Phase 2 gate)
- `research/st_eh/results/replication_gate.md`
- `research/st_eh/results/baseline_longpanel.csv`
- `research/st_eh/results/grid_results.csv` (40 rows, one per symbol-cell)
- `research/st_eh/results/SESSION-RECORD-ST-EH-1.md` (verdict, nulls-alive
  ledger, roll-rule documentation, K entry)
- Cached parquet panels under `data/cache/glbx/`

---

## §3 — Cost model (frozen for this campaign, pending §0.5 Q4)

Tradeify: $0.91/side commission + 1 tick/side slippage.
- MNQ: tick 0.25 pt × $2.00/pt = $0.50/tick → RT = 2×0.91 + 2×0.50 = **$2.82**
- MYM: tick 1.00 pt × $0.50/pt = $0.50/tick → RT = 2×0.91 + 2×0.50 = **$2.82**
- 4× hurdle: **$11.28 per trade**, both symbols.
Parent-panel analysis applies MICRO costs to micro-scaled P&L (never parent
commission structure). Bulenox ($0.61/side) and MFFU ($0.95/side) reported as
sensitivity columns only.

---

## §4 — Falsifiable hypotheses

**H1 (baseline representativeness):** ST(10,3) flip-only on 15m clears the
costed bar on the 2010→present parent panel — costed expectancy ≥ 4× RT hurdle
AND bootstrap 90% CI lower bound > 0 — for NQ and/or YM.
*If both symbols fail → H1 FALSIFIED (expected outcome given §1 evidence).*

**H2 (grid layer):** at least one grid cell satisfies ALL five §2-Phase-6
promotion criteria on at least one symbol.
*If no cell qualifies → H2 FALSIFIED, grid closed dead, K=44 logged.*

Either verdict is a resolution. "Needs more data" is not an available verdict —
the panel is 16 years.

---

## §5 — Forbidden moves (each was genuinely tempting at authoring time)

1. **Adding any filter mid-campaign** (session, DOW, EOM, min-ATR, hour-block)
   because a slice looks good in the long panel. Filters are a separate future
   pre-reg. ORB-MNQ-1 §5 precedent binds.
2. **Sweeping a dead baseline into a green cell and believing it** without the
   full Phase-6 battery. The grid may run (characterization); promotion may not
   skip a single criterion.
3. **Widening the grid after seeing results** ("try mult 5.0"). Any extension
   is a new pre-reg with an explicit K increment.
4. **Adding a timeframe axis.** Out of scope; new pre-reg required.
5. **Mixing engines or feeds** — no TV-derived numbers may enter the long-panel
   comparison; Phase 2 fidelity is what licenses the Python engine, and after
   that TV panels are historical context only.
6. **Treating parent-era P&L as micro P&L** without the ×0.1 economics rescale,
   or skipping the micro-era OOS gate.
7. **Escalating to tick/MBO data "for realism."** Bars only. Microstructure
   escalation requires a surviving candidate first.
8. **Any pull without a prior estimate**, or hand-written `get_range` outside
   `db_fetch.py`.

---

## §6 — Gates, reporting format, status taxonomy

Per-phase gates are stated inline in §2. Final campaign verdict is one of:
- `H1-VIABLE` (baseline clears — proceed to a follow-up pre-reg, not to live)
- `GRID-CANDIDATE(cells…)` (H1 failed, ≥1 cell passed all five criteria)
- `FALSIFIED-AT-COST` (H1 and H2 both falsified — expected)
- `AMBIGUOUS` (fidelity gate unresolvable or data defect; explain)

Status returns use the four-state taxonomy: `DONE` / `DONE_WITH_CONCERNS` /
`NEEDS_CONTEXT` / `BLOCKED`. `DONE_WITH_CONCERNS` requires naming the concern
(e.g., cost-model doc absent, roll-rule ambiguity, fidelity passed at tolerance
edge). `BLOCKED` must name its sub-case: context-problem (re-dispatch with
context) / capability-problem (stronger model or human) / scope-problem
(decompose) / plan-itself-wrong (escalate to parent — e.g., if Phase 2 fidelity
is unachievable because the TV feed diverges structurally from GLBX, the plan
premise is wrong; escalate, do not force tolerances).

---

## §7 — Parent-session review (on return)

Two passes, then a consolidated read:
1. **Spec compliance:** exactly §2 Phases 0–7, nothing missing, nothing added.
   Any "while I was in there" extra (an added filter test, an extra symbol, a
   widened grid) fails this pass even if methodologically sound.
2. **Quality:** engine math vs §2 Phase 2 spec; bootstrap and null
   implementations vs selection_tests conventions; slice discipline (calendar
   years only).
3. **Consolidated read** across all phases (this is a >1-step handoff):
   fidelity gate ↔ long-panel ↔ grid must tell one consistent story; per-phase
   correctness does not guarantee integration consistency.

---

## §10 — Audit hooks (runnable)

```bash
# Estimate-before-pull discipline: every pull preceded by an estimate
grep -c "estimate" logs/db_fetch.log; grep -c "pull" logs/db_fetch.log
# assert estimate_count >= pull_count

# Grid completeness: 40 rows, no cell dropped
python -c "import pandas as pd; df=pd.read_csv('research/st_eh/results/grid_results.csv'); assert len(df)==40, len(df); print('grid OK')"

# Replication gate artifact exists and passed
grep -E "Jaccard|count|VERDICT" research/st_eh/results/replication_gate.md

# K logged under campaign ID
grep "ST-EH-1" <anomaly-discovery-ledger-path> | grep "K=44"

# Roll rule documented
grep -i "roll" research/st_eh/results/SESSION-RECORD-ST-EH-1.md

# Forbidden-move tripwire: no filter logic entered the engine
grep -iE "session|dayofweek|eom|min_atr" research/st_eh/engine.py; # expect no matches

# Brief discipline (if checker present in repo)
python scripts/check_brief.py CC_HANDOFF_ST-EH-1.md --type cc_handoff
```

## Verification (author-side, run before spawning)

- Baseline table in §1 regenerated from the two uploaded CSVs this session
  (parser: utf-8-sig, Exit-rows-only P&L, pair by `Trade number`; new-format
  columns confirmed). ✔
- Commission $0.00 verified by column sum on both files. ✔
- Flip-only + 15m + 24h session verified by flip-share/minute/hour censuses. ✔
- Cost constants cross-checked against the ORB-MNQ-1 frozen cost model
  (Bulenox $0.61 / Tradeify $0.91 / MFFU $0.95 per side + 1 tick). ✔
