# `MNQPOOL-1` — pool-shield session-carry long on MNQ: frozen pre-registration

**Status:** `FROZEN` — committed before any event count, trade count, or outcome number exists
for this construct anywhere. The freeze commit for this file precedes the results commit
(house rule: pre-registration freeze is a separate, earlier commit).
**Date:** 2026-08-04 · **Operator authorization:** in-session direction *"run an in-house probe
on MNQ. Let's use the information we have collected previously to our advantage."*
**Route:** in-house discovery probe (`futures-anomaly-discovery` lane) — **NOT** a harvest seed.
The harvest §1 admission requirements (1a WHO-constraint etc.) govern externally-sourced
mechanisms and do not apply; the discovery route's own discipline (K bound before looking,
manifest, DSR floor) applies in full. Mining needs no mechanism story; deploying does.
**K_intrinsic = 1** — a single frozen construct, zero swept axes (§2 derives every constant
from a prior measurement or a standing convention; none is tuned). `K_banked(MNQ) = 2`
(re-read from `discovery_manifests/` this session: `d5_nq_intraday_mom` 1 + `st_eh_supertrend_grid`
executed-split 1; the open ORB manifest banks nothing) — **disclosure, not a gate**
(ADR 2026-08-04 family-K-bank; `K_eff = K_intrinsic = 1`).
**Cost:** $0.00 (panel on disk) · no new pull · no `core/`, lock, allocation, `dd_protection`,
lifecycle, Pine, rail, or `LEG_MAP` change. Deployment of anything found requires its own
Stage-0 pre-registration + operator GO — this probe licenses measurement only.

---

## §0 — Rule-0 reads (executed this session, before this file was authored)

| Source | What it pins |
|---|---|
| [`lab/archive/ict_cascade_2026-06-18/harness_d.py`](lab/archive/../../archive/ict_cascade_2026-06-18/harness_d.py) (read at the function level, not the docstring) | The N9 measurement's frozen definitions, inherited verbatim by §2: pools = **pivot lows/highs at `pvLen=3`, wick basis**, `t0` = the TRUE pivot bar; **sweep (SSL) = any later daily bar's `low <= px`** — touch-or-through at the exact level, no penetration threshold; horizon `drawK=10` daily bars; roll exclusion = object origins within **±4 calendar days of quarterly 3rd-Friday expiry** |
| [`lab/analysis/_inbox/ict_mnq_2026-08/RESULTS.md`](lab/archive/../ict_mnq_2026-08/RESULTS.md) §3, §5 | The N9 rates: MNQ SSL pool sweep **0.3397 vs base 0.6502** (156 blocks), NQ **0.3128 vs 0.6014** (211), US500 0.34 vs 0.61 — three instruments, radius-matched MC null ≥5000 draws/side. §5.1: a tradable expression *"needs a fresh, separate, K-bound proposal that pays its own K and re-runs reachability against the family bank at that time"* — **this document is that proposal** |
| [`ops/instruments/MECHANISMS.md`](lab/archive/../../../ops/instruments/MECHANISMS.md) `ict-liquidity` | Class carries the anti-attractor finding; the barred reading is *"price is drawn to old highs/lows"* — this construct keys on the **measured inverse** |
| `python scripts/instrument_profiles.py cell MNQ ict-liquidity` (executed; exit 1) | **BINDING BAR** `index-intraday-ohlcv-directional-timing-2026-07-21` — addressed in §3. Cell verdict otherwise: *"untested — no prior on this cell."* Cost hurdle N6 3.01 bp/session noted |
| [`docs/rejected_candidates.md`](lab/archive/../../../docs/rejected_candidates.md) L456-466 (read in full) | The bar's three OR'd admission routes; scope; the 2026-08-02 status update (session-confluence preservation discharged) |
| [`lab/analysis/c1/mnq_event_ceiling_2026-08-04/run_ceiling.py`](lab/analysis/c1/mnq_event_ceiling_2026-08-04/run_ceiling.py) + PREREG | Step-1 session conventions (18:00→16:00 ET cut) this probe reuses |
| [`lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md`](lab/analysis/c1/eval_slow_archetype_2026-08-04/RESULTS.md) | The corrected frontier this probe is aimed at: k=1 at ≥0.49R-class edge suffices (no venue time limit, verified); the ratified screen floor at K=1 = **annSR 0.650** |
| `lab/research_utils/deflated_sharpe.py` (production) | Verdict machinery: `deflated_sharpe(sr, n, skew, kurt, sr0)` with `sr0 = expected_max_sharpe(1, ·) = 0.0` at K=1 |
| Data: `~/.databento_cache/ohlcv-1m_continuous_dd7f7f1ad81d2b63.dbn` | `MNQ.v.0` ohlcv-1m, **2019-05-06 → 2026-08-04** (metadata read via `DBNStore`), sha256 `38e29862655152d09cf4395fc36b1b464887ed93e6f795dd96f0f2fea43074a9` — the Step-1 panel, on disk, $0 |

**Dedup attestation (commands executed, output summarized honestly):** `rg --no-ignore -il
"support bounce|pool.{0,10}bounce|pivot low.{0,20}long|barrier|anti.?attractor"` over
`rejected_candidates.md`, `rejected_signals.md`, `docs/briefs`, `discovery_manifests` → 24 files,
**all incidental word matches** ("absorbing barrier" MC contexts, this campaign's own MNQBASE
artifacts) — **no registry entry rejects a pool-anchored long-shield construct**. Manifest status
listing pasted in session log. Named adjacencies that are NOT this construct, distinguished ex
ante: **Q-ICT-MNQ-1 1H premium/discount MR gate FALSIFIED** (that gated hourly direction on
range-position; this keys on a confirmed pivot-low *level object* with measured avoidance
dynamics); **VWAP/midday-fade anti-edge** (that is a fade *against* intraday direction; this is a
with-drift long carry); **H-OD-1 overnight drift cost-law kill** (that was an unconditional
overnight harvest seed at ~1.5bp/event; this is RTH-only, conditional, R-scale); **EOD-adversity
raised bar** (scopes mechanism *explanations* for the 15:30–16:00 block; this construct merely
exits at 16:00 per E1).

---

## §1 — Hypothesis, and its derivation from measured facts only

**The measured fact (N9):** a confirmed daily-pivot low on MNQ is touched-or-penetrated within 10
days only **34%** of the time, against **65%** for a radius-matched random walk. The measurement's
sweep definition is `low <= px` — price avoids even *reaching* old pivot lows, at roughly half the
null rate, replicated on three instruments.

**What that licenses (and what it does not):** it does NOT license "buy the touch" — a fill at the
pool means the shield has already partially failed, and the conditional after a touch is unmeasured.
It DOES bound the loss side of a long held *above* an active pool with its stop AT the pool level:
the probability the stop is reached is the probability of the sweep, which is the measured
anomalously-rare event. If the anomaly is a genuine dynamics distortion (downside excursions
truncated relative to the null) rather than a pivot-definition artifact, a long with a pool-anchored
stop and a time exit has positive expectancy against a symmetric-walk baseline. Whether that
expectancy survives (a) the near-zero unconditional RTH drift on MNQ (D5/N5: intraday momentum
absent; overnight owns index drift) and (b) the 1.41 pt round-trip cost basis is exactly what this
probe measures.

**H-MNQPOOL-1.** Sessions carrying an active, unswept, confirmed pivot-low pool below the RTH open
have positive net long expectancy from a 09:30 ET entry, pool-anchored stop, 16:00 ET time exit —
above costs, above the session base rate (placebo), in both regime halves.

---

## §2 — The frozen construct (every constant sourced; nothing tuned)

| # | Element | Frozen value | Source (why this is not a free axis) |
|---|---|---|---|
| S1 | Panel | `MNQ.v.0` 1m, 2019-05-06 → 2026-08-04, sha256 `38e29862…` | Step-1 panel, on disk |
| S2 | Session cut | 18:00 → 16:00 ET, session dated by its close side | Step-1 convention (`run_ceiling.py`) |
| S3 | Roll exclusion | drop sessions within ±4 calendar days of quarterly 3rd-Friday expiry — both as pool origins AND as trade sessions | harness_d LOCKED rule, transplanted whole |
| S4 | Session-daily bars | OHLC resampled from in-session 1m bars | mechanical |
| S5 | Pool | pivot low at `pvLen=3` on session-daily lows: `low[i] < low[i±1..3]` strict both sides; level `px = low[i]` (wick); `t0 = i` | harness_d LOCKED (`pvLen=3`, wick basis, true-pivot t0) |
| S6 | Confirmation | pool is knowable only from session `t0+3` | look-ahead-free by construction |
| S7 | Active window | sessions `d` with `t0+3 ≤ d ≤ t0+10`, pool unswept in `(t0, d)` (no completed session low ≤ px) | harness_d `drawK=10`; sweep rule verbatim |
| S8 | Pool choice | nearest eligible pool below the entry anchor (max px < anchor); no eligible pool → no trade | mechanical; no distance band introduced |
| S9 | Entry | long at the 09:30:00 ET 1m bar's open; session skipped if that bar is absent | RTH-open convention (house + Mesfin comparability); the 18:00-entry overnight variant is NOT run (named untested sibling, would be K=2) |
| S10 | Stop | intraday: first 1m bar (entry bar onward) with `low ≤ px` → exit at `min(px, bar_open)` | the sweep definition itself is the stop trigger; gap-through priced honestly |
| S11 | Time exit | last in-session bar with time < 16:00 ET → exit at close | E1 (portable flat-by-16:00) |
| S12 | Costs | 1.41 pt round trip flat ($0.91/side commission + 1 tick/side slippage) | standing Tradeify basis (MNQBASE T1, N6) |
| S13 | R unit | `R = entry − px` (points); **skip trade if R < 5 pt** (≈3.5× RT cost, degenerate-stop guard — the only guard, declared here) | cost-floor rationale; not swept |
| S14 | Net R | `(gross_pnl_pt − 1.41) / R` | mechanical |
| S15 | Frequency | max one trade/session; long-only; SSL pools only (no BSL/short limb — MNQ short-side measured adverse estate-wide) | K containment |

**Outputs computed (closed list — nothing else is read):** trade count n, eligible-session census,
mean net R + week-block bootstrap 95% CI (trades grouped by ISO week, 10,000 resamples, seed
20260804), daily net-R series → annSR (`mean/std·√252` over ALL panel sessions, zeros on
non-trade sessions), DSR = `deflated_sharpe(sr_daily, n_days, skew, kurt, sr0=0)` (production
module, K=1), regime halves (H1 < 2023-01-01 ≤ H2) mean net R, placebo distribution (below), stop-hit
rate (for the N9-consistency check only). **No MFE/MAE surfaces, no per-cell tables, no bracket
diagnostics are emitted** — removing the material a post-hoc bracket could be tuned on.

**Placebo (frozen):** 1,000 reps, seed 20260804. Each rep draws n sessions uniformly without
replacement from all valid non-roll sessions with a 09:30 bar, permutes the real trades' R multiset
onto them, sets each synthetic stop at `anchor − R`, and runs the identical S10/S11 machinery.
Threshold: real mean net R must exceed the placebo's **p95**. This tests that *pool-eligible
sessions* beat *random sessions at identical stop geometry* — the WLEGB discipline (four of five
limbs passed there; only the base-rate-matched placebo caught the confound).

---

## §3 — The binding domain bar, addressed (not waved at)

`index-intraday-ohlcv-directional-timing-2026-07-21` (rejected_candidates.md L456): a new
single-instrument index-futures intraday OHLCV directional-timing candidate is not admitted unless
it clears one of three routes. **This probe claims route 1** — *"a mechanism outside the mapped
cost-ratio-lever set (price / instrument-selection / hold-time)"*:

1. The mapped-and-exhausted levers are cost-ratio levers. This candidate re-tunes none of them: it
   is not a price-basis change, not instrument-shopping, not a hold-time re-tune of an existing
   construct. It is a **conditioning-state mechanism** — trade only when a measured structural
   object (active unswept pivot-low pool) is present, with the stop anchored to that object.
2. The evidence behind it **postdates the bar**: N9 was measured 2026-08-03/04, twelve days after
   the 2026-07-21 domain audit; none of the four in-domain closures (D5, D5-RECOST, H-TSMOM-1,
   cross-index-RV) used pool-state conditioning. The registry's own repo-wide re-proposal doctrine
   is *"new mechanism evidence, not new parameters"* — a three-instrument-replicated,
   radius-matched-null anomaly is new mechanism evidence in exactly that sense.
3. Route 3 (beat the incumbent net-of-cost) is not claimed ex ante — but the RESOLVED disposition
   (§6) requires reporting the annSR against ORB-MNQ-1's benchmarks (+0.890 Bulenox / **+0.835
   Tradeify** basis) so the comparison is on the record either way. Noted honestly: at the Tradeify
   basis the incumbent itself FAILS its full-window Stage-6 limb (N1 rider), so a Tradeify-viable
   candidate at ≥0.650 would be doing something the incumbent measurably cannot at this venue.

**Flagged for the operator:** route-1 clearance is this pre-registration's own argument, made under
the standing consult rule (*"the pre-registration must name and address it; it is not a permanent
bar"*). If the operator reads route 1 more strictly, this probe should be stopped before the
results commit — the freeze gives that veto a clean point of intervention.

---

## §4 — Pre-registered expectation (recorded so the outcome cannot be retrofitted)

**The single most likely outcome is V2 or V4 (null-after-costs / base-drift confound).** Grounds:
unconditional RTH-only drift on MNQ is ≈ 0 (D5-RECOST: OOS −0.327 bp; overnight owns index drift),
so the placebo should center near −costs, and the anomaly must supply the entire edge. The
anti-attractor is large in probability space but its dollar-space translation is unmeasured, and
"stop rarely hit" bounds only the loss side. **A positive result would NOT be suspicious** — the
construct aligns with drift, the shield is measured, and the hold (6.5h) sits in the class Mesfin's
own edge-ceiling explicitly exempts — but it is not the expected branch. The probe is worth K=1
because every branch is decision-grade: V1 lands directly on the corrected k=1 frontier; V2/V4
close the pool-shield expression at $0 and sharpen the domain map; V3 records a real conditioning
input without a strategy claim.

---

## §5 — Forbidden moves

- **FM-1 — Any second cell.** No bracket/target variant, no BSL/short limb, no pvLen/drawK/entry-time/guard sweep, no distance band, no overnight-entry sibling. Each is a new K-bound axis needing fresh authorization.
- **FM-2 — Reading the stop-hit rate as a tradability verdict.** It is emitted solely to check consistency with N9's 0.34; the verdict lives in §6's limbs only.
- **FM-3 — Adjusting any §6 threshold, the placebo design, the seed, or the CI method after data** (Trap #12).
- **FM-4 — Reframing V3 (real effect below floor) as a deployable edge** — it routes to disclosure only.
- **FM-5 — Any deployment implication from any branch.** Rail stays disarmed; M1 interlock stands; a V1 successor needs its own Stage-0 + operator GO.
- **FM-6 — Emitting or consulting excursion surfaces** that would let a future session tune a bracket on this panel "for free."

---

## §6 — Verdict gates (frozen; precedence order as listed)

| # | Condition | Verdict | Disposition (pre-registered) |
|---|---|---|---|
| V5 | n < 150 trades | `AMBIGUOUS-UNDERPOWERED` | Report census only; no re-cut of the panel to manufacture n |
| V2 | mean net R ≤ 0, OR week-block 95% CI includes 0 | `FALSIFIED` | **STOP.** K=1 banked to MNQ; the pool-shield *expression* dies; N9 (a rate fact) is untouched. Re-proposal bar: new mechanism evidence, not re-parameterization |
| V4 | CI > 0 but real mean ≤ placebo p95 | `AMBIGUOUS-CONFOUND` | **STOP.** The "edge" is session base drift, not the pool condition (WLEGB shape). Same bar as V2 |
| V3 | CI > 0, placebo beaten, but annSR < 0.650 or DSR < 0.95 | `AMBIGUOUS-EFFECT` | Record as a **conditioning-input candidate** (disclosure); no strategy claim; any follow-up probe needs fresh operator authorization |
| V1 | CI > 0 ∧ placebo beaten ∧ annSR ≥ 0.650 ∧ DSR ≥ 0.95 ∧ both halves mean ≥ 0 | `RESOLVED` | **ITERATE → names (does not open) a Stage-0 pre-registration** for the construct, reporting annSR vs the ORB benchmarks (§3.3) and the frontier row it lands on. Board write + operator decision item |

A V1 missing only the halves limb reports as `AMBIGUOUS-REGIME` with V3's disposition. **Board
write owed at closure in every branch.**

---

## §7 — Protocol order (violations void the run)

1. This file committed (freeze) — **before any event count exists**.
2. `register_search open` binds K_intrinsic=1 to run-id `mnqpool_shield_probe` (manifest).
3. Harness + hand-computed unit tests; **all tests pass before the runner reads a real bar**.
4. Single run. RESULTS.md discharges exactly one §6 branch. Manifest closed. Boards written.

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering: this file's commit precedes the RESULTS commit
git log --oneline -- lab/archive/mnq_pool_shield_probe_2026-08-04/PREREG.md | tail -1
git log --oneline -- lab/archive/mnq_pool_shield_probe_2026-08-04/RESULTS.md | tail -1

# The inherited sweep rule is touch-or-through (expect: low[j] <= px in harness_d)
grep -n "b.low\[j\] <= px" lab/archive/ict_cascade_2026-06-18/harness_d.py

# The domain bar this prereg claims route 1 against (expect the three-route list)
grep -n "not admitted for a full Pre-Q" docs/rejected_candidates.md

# K discipline: manifest exists, K=1, and the MNQ bank was disclosed not summed
python -c "import json;m=json.load(open('discovery_manifests/mnqpool_shield_probe.json'));print(m.get('K'),m.get('status'))"

# Data pin
python -c "import hashlib;print(hashlib.sha256(open(r'C:/Users/joshu/.databento_cache/ohlcv-1m_continuous_dd7f7f1ad81d2b63.dbn','rb').read()).hexdigest())"
# Expect 38e29862655152d09cf4395fc36b1b464887ed93e6f795dd96f0f2fea43074a9
```
