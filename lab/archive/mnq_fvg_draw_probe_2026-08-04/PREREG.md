# `MNQFVG-1` — bear-FVG draw as a target-anchored long on MNQ: frozen pre-registration

**Status:** `FROZEN` — committed before any event count, trade count, or outcome number exists for
this construct anywhere. Freeze commit precedes the results commit (house rule).
**Date:** 2026-08-04 · **Operator authorization:** in-session direction *"run the bear-FVG draw
probe"* (following the MNQPOOL-1 report, which named this as the one measured positive still
unexpressed).
**Route:** in-house discovery probe — same lane, discipline, and gate machinery as
[`MNQPOOL-1`](lab/archive/mnq_pool_shield_probe_2026-08-04/PREREG.md) (frozen `9c87f83`, closed
`FALSIFIED` V2). Harvest §1 admission requirements do not apply (not an external seed); the
discovery lane's K discipline applies in full.
**K_intrinsic = 1** — a single frozen construct, zero swept axes. `K_banked(MNQ) = 3` after
MNQPOOL-1 (re-read from `discovery_manifests/`: `d5_nq_intraday_mom` 1 + `st_eh_supertrend_grid`
split 1 + `mnqpool_shield_probe` 1) — **disclosure, not a gate**.
**Cost:** $0.00 — `MNQ.v.0` 1m panel on disk (same pinned file as MNQPOOL-1). The Databento
subscription is NOT drawn on for this probe; its recent-window order-flow entitlements (MBP-10 /
TBBO) are noted as the domain bar's **route 2 modality for future probes**, cost-dry-run-gated.
No `core/`, lock, allocation, `dd_protection`, lifecycle, Pine, rail, or `LEG_MAP` change.

---

## §0 — Rule-0 reads (executed this session, function level, before this file)

| Source | What it pins |
|---|---|
| [`_ict_offline.py`](lab/archive/../../archive/ict_cascade_2026-06-18/_ict_offline.py) L66-135, L386 | **Imported unmodified, not transcribed.** Bear FVG at daily bar `i` (wick): `high[i] < low[i-2]`; bounds `top = low[i-2]` (FAR), **`bot = high[i]` (NEAR edge from below)**; displacement on the middle candle: `(high[i-1]-low[i-1]) > 1.5 × ATR14[i]`, Wilder RMA ATR with the TV first-bar TR fix |
| [`harness_d.py`](lab/archive/../../archive/ict_cascade_2026-06-18/harness_d.py) L249-274, `_build_fvgs` | Touch (draw hit) = `high[j] ≥ bot`, scan from **`t0+1`** (D-1 guard ON in the headline result); registration bar `t0 = i`; `drawK = 10`; `dispMlt = 1.5`, `atrLen = 14` all LOCKED |
| [`ict_mnq_2026-08/RESULTS.md`](lab/archive/../ict_mnq_2026-08/RESULTS.md) §3, §5 | The measured draw: **NQ bear-FVG 0.8630 vs base 0.7494 — RESOLVED, stationary (halves 0.838/0.889), the only RESOLVED cell in the D layer**; MNQ secondary **0.8269 vs 0.7806 AMBIGUOUS-HOLD** (h1 0.769 dips below base; scope limit 6: do not quote as confirmation). Naming note: `SSL.fvg` **is** the bear FVG — an **upward** draw |
| `python scripts/instrument_profiles.py cell MNQ ict-liquidity` (re-run this session) | Binding bar `index-intraday-ohlcv-directional-timing-2026-07-21` (§3 below). ⚠ The consult's *"untested — no prior on this cell"* is **stale**: `MNQPOOL-1` (same class, this instrument) closed `FALSIFIED` V2 earlier today — named and addressed in §3, and the profile cell is corrected in this branch |
| [`MNQPOOL-1 RESULTS`](lab/archive/mnq_pool_shield_probe_2026-08-04/RESULTS.md) | The prior this design answers: pool-shield died because the anomaly's object was **572 pt away** — avoidance pushes its objects out of reach. FVG zones are **recent 3-session structures**; their near edges should sit within intraday reach (measured in Step 0, C0) |
| Committed [`run_pool_probe.py`](lab/archive/mnq_pool_shield_probe_2026-08-04/run_pool_probe.py) | Session/roll/RTH/bootstrap machinery **imported by path, unmodified** (`assign_sessions`, `session_daily`, `build_rth`, `week_block_ci`, `roll_dates`, calendar) — zero transcription risk, already unit-tested |
| Data | Same pinned panel: `~/.databento_cache/ohlcv-1m_continuous_dd7f7f1ad81d2b63.dbn`, sha256 `38e29862…` (hash asserted at load), 2019-05-06 → 2026-08-04 |

**Dedup (executed):** `rg --no-ignore -il "fvg"` over `rejected_candidates.md`,
`rejected_signals.md`, `discovery_manifests/` → **zero hits**. Named adjacencies, distinguished ex
ante: **`pharos_us500_sweepfvg`** FALSIFIED on robustness (drop-top-3 −0.152R) and **`Q-ICTEXP-1`**
AMBIGUOUS-null — both used structures as **entry context and targeted pools or range extremes**,
i.e. they targeted objects this estate has since measured as **anti-attractors**. This construct
inverts that: it **targets the FVG itself** — the one object in the class with a measured,
RESOLVED, stationary positive draw. The estate's own decomposition explains the prior deaths and
this design's difference. **`MNQPOOL-1`** (same class, today) died on object *distance*; §1
states why the same failure mode is not expected here and §4 prices the possibility that it is.

---

## §1 — Hypothesis, derivation, and the honest evidence split

**Measured fact:** after a displacement down-gap on daily bars, price is drawn back up to touch the
gap's near edge within 10 days at **0.86 vs 0.75** for a radius-matched null — RESOLVED and
stationary on NQ (primary); directionally consistent on MNQ (0.83 vs 0.78, AMBIGUOUS-HOLD on the
stationarity limb of a shorter panel). The traded instrument is MNQ (the venue micro, 1/10 NQ,
same underlying tape); **the premise rests on NQ-primary evidence and the probe itself is the MNQ
test.** A null here does not impeach the NQ rate; a positive is not a "confirmation" of MNQ's
D-layer cell (scope limit 6 both ways).

**What the draw licenses:** the measured event is a **target touch** — price reaching `bot` from
below. The natural expression anchors the **win side** to the anomaly (mirror-image of MNQPOOL-1,
which anchored the loss side): long toward the near edge, exit at the touch. The loss side has no
anomaly to anchor a stop to, so the construct is **stop-free with a time exit** — the `Q-ICTEXP-1`
precedent (stop-free tiers accepted when no stop rule is derivable; removes the one
unreconstructable constant instead of inventing it).

**Why MNQPOOL-1's failure mode should not repeat (falsifiably):** pool-shield died because
*surviving* pools recede (median 572 pt). FVG zones are the opposite kind of object — born from
the last three sessions' bars, near price by construction, and *consumed* (touched) rather than
*avoided*, so the eligible set is fresh and close. Step 0 measures the actual G distribution; if
median G is far (the MNQPOOL shape), §4's expectation names dilution as the live kill.

**H-MNQFVG-1.** Sessions carrying an active, untouched, displacement bear-FVG near edge above the
RTH open have positive net long expectancy from a 09:30 ET entry with a limit exit at the near
edge and a 16:00 ET time exit otherwise — above costs, above a base-rate-matched session placebo,
in both regime halves.

---

## §2 — The frozen construct (every constant sourced; nothing tuned)

| # | Element | Frozen value | Source |
|---|---|---|---|
| S1 | Panel / sessions / roll rule / session-daily bars | identical to MNQPOOL-1 S1–S4, machinery imported from the committed harness | MNQPOOL-1 (frozen `9c87f83`) |
| S2 | FVG registry | bear FVGs on session-daily bars via **imported** `_ict_offline` functions: `displacement(i, ATR14[i], 1.5, wick)` AND `bear_fvg(i, wick)` → `bot = high[i]`, `t0 = i`; origins in a roll window discarded | harness_d `_build_fvgs`, LOCKED constants |
| S3 | Active window | sessions `d` with `t0+1 ≤ d ≤ t0+10` (registration knowable at `t0` close; touch scan starts `t0+1` per the D-1 guard), zone untouched: no session `j` in `[t0+1, d-1]` with `high[j] ≥ bot` | harness_d scan semantics, verbatim |
| S4 | Target choice | nearest eligible near-edge **above** the anchor (min `bot > anchor`); none → no trade | mechanical, mirror of MNQPOOL S8 |
| S5 | Entry | long at the 09:30:00 ET 1m bar's open; session skipped if absent, roll-flagged sessions skipped | MNQPOOL S9 |
| S6 | Win exit | first 1m bar (entry bar onward, < 16:00) with `high ≥ bot` → limit fill **at `bot`** (no favorable slippage assumed) | the measured draw event, priced conservatively |
| S7 | Time exit | no touch → close of last in-session bar < 16:00 ET | E1; stop-free (Q-ICTEXP precedent) |
| S8 | Costs | flat **1.41 pt** round trip | standing Tradeify basis |
| S9 | Units | net points = `gross − 1.41`; `G = bot − anchor`; **skip if `G < 5 pt`** (the single declared guard, ≈3.5× RT) | MNQPOOL S13 rationale |
| S10 | Frequency | max one trade/session; long only; bear FVGs only (the RESOLVED side — the bull-FVG arm is BSL, AMBIGUOUS/FALSIFIED, not expressed) | K containment |

**Outputs (closed list):** n, census (eligible sessions, **G distribution median/p25/p75** — the
MNQPOOL diagnostic, now pre-declared), touch rate (vs the daily-scale 0.86/0.83 for qualitative
consistency only), mean net points + week-block bootstrap 95% CI (10,000, seed 20260804), daily
net-point series → annSR + DSR (production module, `sr0 = expected_max_sharpe(1,·) = 0`), halves
(H1 < 2023-01-01), placebo (below), mean net/G disclosure. **No MFE/MAE surfaces, no per-cell
tables** (FM-6).

**Placebo (frozen):** 1,000 reps, seed 20260804 — n random valid sessions without replacement,
real **G multiset permuted** onto them as limit-target distances (`target = anchor + G`), identical
S6/S7 machinery, mean net points per rep; real mean must exceed **p95**. Tests "FVG-eligible
sessions beat random sessions at identical target geometry."

---

## §3 — The binding domain bar, addressed at today's honest tail count

Same bar as MNQPOOL-1 (`index-intraday-ohlcv-directional-timing-2026-07-21`), which now carries
**five** in-domain closures including MNQPOOL-1 itself, closed hours ago. Claimed route: **route 1**
again — target-anchored FVG-draw conditioning is a mechanism outside the mapped cost-ratio lever
set (price / instrument-selection / hold-time), resting on the D-layer's **only RESOLVED cell**,
measured 2026-08-03 (post-bar). Two honesty additions beyond the MNQPOOL argument:

1. **The within-class prior is adverse and is named:** MNQPOOL-1 (same class, same instrument,
   same day) is FALSIFIED. The distinguishing fact is mechanistic, not hopeful: MNQPOOL targeted
   *avoided* objects at 572 pt; this targets *consumed* objects born three sessions ago. If the
   census shows the same distance shape, §4 expects the same death.
2. **Route 2 is now genuinely open for successors:** the Databento subscription's recent-window
   MBP-10/TBBO entitlements are the order-flow modality the bar names. Not drawn on here ($0
   probe); recorded so the next probe's route argument can be stronger than route 1.

**Flagged for operator veto at the freeze point**, as before. A second same-class falsification
would make route-1 arguments on this cell **presumptively exhausted** — that consequence is
accepted ex ante and recorded in §6's dispositions.

---

## §4 — Pre-registered expectation

**Most likely single branch: V2 (null).** Grounds: every prior tradable ICT expression died
(sweepfvg robustness, ICTEXP ≈0, MNQPOOL today); bear-FVG-active sessions follow down-displacement
— entering long into recent weakness with **no stop** exposes the E1 tail to trend-continuation
days; and the placebo (random sessions, same targets) inherits the same mild long drift that made
MNQPOOL's placebo positive. **But this is the least-null-expected probe of the family:** the target
is the one RESOLVED stationary object, G should be near (tens of points), the touch hazard
concentrates early in the window, and a 0.8-class touch rate at G ≈ 2-4× cost is arithmetically
capable of clearing V1. V1/V3 are genuinely live; V5 possible (FVG blocks ≈ 52 on the TV MNQ
panel → the session-expansion must reach n ≥ 150 for power). Dilution (median G ≫ 100 pt) would
reproduce the MNQPOOL death and is the named alternative kill.

---

## §5 — Forbidden moves

- **FM-1 — any second cell:** no bull-FVG arm, no stop variant, no mid-of-gap target (W3's 59% is
  a 1m-scale fact with **no null**, not a licensed target), no dispMlt/atrLen/drawK/entry-time/guard
  sweep, no NQ scored arm (evidence panel ≠ trade panel; an NQ arm is a new instrument cell).
- **FM-2 — reading the touch rate as the verdict** — it is qualitative consistency only; the
  verdict is §6's ladder.
- **FM-3 — adjusting any threshold, seed, placebo, or CI method after data** (Trap #12).
- **FM-4 — reframing V3 as deployable**, or any deployment implication from any branch (rail
  disarmed; M1 interlock; Stage-0 + operator GO required for anything further).
- **FM-5 — emitting excursion surfaces** a successor bracket could be tuned on (FM-6 inheritance).
- **FM-6 — a third same-class probe on this instrument without operator review** if this one
  falsifies — accepted ex ante per §3.

---

## §6 — Verdict gates (frozen; precedence as listed)

| # | Condition | Verdict | Disposition |
|---|---|---|---|
| V5 | n < 150 | `AMBIGUOUS-UNDERPOWERED` | Census only; no panel re-cut. Records that the daily-scale draw cannot power a session-scale probe → any expression needs multi-day holds, which T5 (flat-by-16:00) structurally complicates — an honest wall, not an invitation to re-cut |
| V2 | mean net ≤ 0 OR CI includes 0 | `FALSIFIED` | **STOP.** K banked (MNQ 3→4). With MNQPOOL-1, two same-day same-class kills ⇒ route-1 arguments on `MNQ × ict-liquidity` are **presumptively exhausted** (FM-6); the class continues only via route 2 (order-flow modality) or route 3, with operator review |
| V4 | CI > 0 but mean ≤ placebo p95 | `AMBIGUOUS-CONFOUND` | **STOP**, same consequences as V2 (the effect is drift, not the draw) |
| V3 | CI > 0, placebo beaten, annSR < 0.650 or DSR < 0.95 | `AMBIGUOUS-EFFECT` | Conditioning-input disclosure only; no strategy claim; follow-up needs fresh authorization |
| V1 | CI > 0 ∧ placebo beaten ∧ annSR ≥ 0.650 ∧ DSR ≥ 0.95 ∧ both halves ≥ 0 | `RESOLVED` | **ITERATE → names (does not open) a Stage-0 pre-registration**; reports vs ORB benchmarks (+0.890/+0.835) and the corrected k=1 frontier row; operator decision item |

V1 missing only halves → `AMBIGUOUS-REGIME`, V3's disposition. **Board write owed in every branch.**

---

## §7 — Protocol order (violations void the run)

1. This file committed (freeze) — before any event count exists.
2. `register_search open` binds K_intrinsic=1, run-id `mnqfvg_draw_probe`.
3. Harness + hand-computed unit tests; all pass before the runner reads a real bar.
4. Single run (census + verdict in one execution). RESULTS.md discharges exactly one branch.
   Manifest closed. Boards written (including the MNQ profile-cell correction from §0).

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering
git log --oneline -- lab/archive/mnq_fvg_draw_probe_2026-08-04/PREREG.md | tail -1
git log --oneline -- lab/archive/mnq_fvg_draw_probe_2026-08-04/RESULTS.md | tail -1

# The inherited touch rule and D-1 guard (expect: high[j] >= f.bot, start_off = 1)
grep -n "b.high\[j\] >= f.bot" lab/archive/ict_cascade_2026-06-18/harness_d.py
grep -n "start_off = 1 if guard else 0" lab/archive/ict_cascade_2026-06-18/harness_d.py

# Bear near-edge is bot = high[i] (expect the bear_bounds docstring lines)
grep -n "bot = high\[0\]" lab/archive/ict_cascade_2026-06-18/_ict_offline.py

# Manifest K=1 and the data pin
python -c "import json;m=json.load(open('discovery_manifests/mnqfvg_draw_probe.json'));print(m.get('K'),m.get('status'))"
python -c "import hashlib;print(hashlib.sha256(open(r'C:/Users/joshu/.databento_cache/ohlcv-1m_continuous_dd7f7f1ad81d2b63.dbn','rb').read()).hexdigest())"
# Expect 38e29862655152d09cf4395fc36b1b464887ed93e6f795dd96f0f2fea43074a9
```
