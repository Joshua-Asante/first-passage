# ORB-MNQ-1 N-SURV magnitude-resampling probe (2026-08-20)

Not a pre-registered campaign — an informal $0.00 spend, zero-K probe. Answers notice
[`N-2026-08-15-nsurv-single-history-magnitude-blindspot`](../../../docs/notes/notice/N-2026-08-15-nsurv-single-history-magnitude-blindspot.md)'s
own open item §3-C ("only c1 has been tested") for a **second, independently-fitted book**
— ORB-MNQ-1's own cushion-sizing bust-elimination finding from
[`orbmnq1_cushion_sizing_probe_2026-08-20`](../orbmnq1_cushion_sizing_probe_2026-08-20/README.md).
**HOLD status of the parent notice is unchanged** — this probe supplies evidence toward
§4's routing decision, it does not itself rule on scope, re-open anything, or discharge
the notice.

**Driver:** [`run_nsurv_magnitude_probe.py`](run_nsurv_magnitude_probe.py) (pre-declaration
in its own module docstring, fixed before it ran) · data
[`nsurv_magnitude_probe_results.json`](nsurv_magnitude_probe_results.json) · log
[`run_probe.log`](run_probe.log)

## What ran

1. Reused `family_skewed_gamma.py`
   ([`geofit_skewed_family_construction_2026-08-15`](../geofit_skewed_family_construction_2026-08-15/family_skewed_gamma.py)),
   **unchanged**, fit to ORB-MNQ-1's own active-day daily P&L (not the 2-leg c1 book the
   notice's own `characterize.json` used).
2. Reused ORB-MNQ-1's own already-validated intraday-honest reconstruction
   (`orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py`), **unchanged**
   — Control B mirror check re-run here as this script's own precondition (`recon` vs
   `orb_lib.orb_backtest`, PASS, n=1846), not re-derived from raw bars.
3. Drew N=50 fresh synthetic realizations (seeds 20260820100–20260820149, matching the
   notice's own N=50) and ran the same cushion-sizing gate check
   (`day_loop_intraday`/`build_paths_orb`/`run_policy_orb`/`pol_cushion`, all imported
   unchanged, k=1, frozen gate bust≤3.0% ∧ pass≥50%) that tonight's cushion probe ran on
   the single real historical draw.

## 1 — Fit-quality check

| | real ORB-MNQ-1 book | fitted family draws (N=50) |
|---|---|---|
| worst single day | **−$783.82** | mean −$818.03, median −$786.94, range [−$1,093.33, −$673.26] |
| skew | **+2.0939** | mean +1.1956, median +1.1514, range [+0.8178, +1.9232] |

Fitted params: `p_win=0.4637 win_mean=211.34 win_sd=223.32 loss_mean=−164.78 loss_sd=119.77
k_win=0.8956 k_loss=1.8928` (n_active=1846).

**Worst-day tail: good match.** The real book's own worst day (−$783.82) sits inside the
synthetic range and close to the synthetic median (−$786.94) — the uncapped Gamma loss
tail is neither systematically milder nor systematically harsher than what actually
happened; some realizations drew a materially deeper single-day loss (−$1,093) than any
day ORB-MNQ-1 has ever had.

**Skew: partial match, real ORB-MNQ-1's own skew (+2.09) is at the extreme upper edge of
what the fit reproduces**, not the fit's own center. All 50 draws undershoot the real
value; the single closest draw (+1.9232) still falls short, and the mean/median sit
41–45% below it. This is a genuine, disclosed fidelity gap, not silently absorbed — it
runs in the **opposite direction** from the same family's construction on the 2-leg c1
book (`geofit_skewed_family_construction_2026-08-15/characterize.json`: real skew
+3.633, realized mean **+4.245**, i.e. *overshoot* there vs *undershoot* here). Opposite
signs across the two books argue against a systematic directional bias in the fitter and
toward what the parent notice's own §3-B already named as unresolved: method-of-moments
(mean, sd) fitting doesn't target the third moment directly, and skew estimates from
finite, heavy-tailed samples (n=1846 active days here, 350 there) carry real sampling
noise in the fit itself, not just in what a single realization draws from it. **Trust
level for anything downstream: adequate to answer this probe's own question (which turns
on the *tail*, matched well) — not evidence the family fully characterizes ORB-MNQ-1's
higher moments.**

## 2 — N=50 distribution under the frozen cushion-sizing gate (k=1, EOD-only — see scope note below)

| | bust% | pass% |
|---|---|---|
| mean | **0.0000%** | 50.69% |
| median | **0.0000%** | 49.05% |
| sd | 0.0000pp | 24.17pp |
| min / max | 0.0000% / 0.0000% | 6.00% / 96.40% |
| p10 / p25 / p50 / p75 / p90 | all 0.0000% | 15.70 / 33.27 / 49.05 / 68.88 / 80.12 |

- **50/50 (100%) of realizations show bust exactly 0.00%.** No exceptions, including the
  realizations that drew a worse single-day tail loss than ORB-MNQ-1's real history.
- **Only 25/50 (50.0%) clear the FULL frozen gate** (bust≤3.0% ∧ pass≥50%) — every
  failure is a pass-rate failure, never a bust failure. Pass% ranges from 6.0% to 96.4%,
  sd 24.17pp — an enormous spread relative to the 50% floor it's being tested against.

**Scope note on the gate check itself (read before trusting the table above):**
`family_skewed_gamma` fits/draws the EOD daily-P&L magnitude only — it has no mechanism
for a paired intraday-low companion, and the day-loop's bust test is driven by
`min(EOD pnl, intraday low)`. Fabricating a low-companion (e.g. bootstrapping the real
book's giveback/pnl ratio) was tried and rejected: that ratio is itself extremely
heavy-tailed and weakly anti-correlated with win size in the real book (mean 2.88×,
median 0.54×, max 468×, measured this session) — applying it to a resampled magnitude
manufactures a second, uncontrolled fabricated tail, exactly the kind of invented
mechanism this probe should not introduce. Instead, the N=50 runs use `use_intraday=False`
(EOD-only), an existing, unmodified parameter of `day_loop_intraday` — not a new code
path. **Load-bearing check for this substitution:** re-running the real single historical
draw both ways gives an **identical** result (bust 0.0000% / pass 52.2700%, intraday-honest
and EOD-only alike) — `pol_cushion`'s multiplier caps at 0.75× and shrinks toward 0 as
cushion shrinks toward the trailing floor, which dominates the intraday/EOD distinction
for this policy on this book. That equivalence is measured on the one draw where both are
checkable, not assumed to hold inside each of the 50 synthetic draws individually — flagged
as the residual scope caveat on every number in this section.

## 3 — Where the actual single-history result sits

Real ORB-MNQ-1 book, full k=1 panel, `pol_cushion`, both conventions: **bust 0.0000% / pass
52.2700%** — clears the frozen gate (`floor_ok=True`).

- **On the bust axis:** the real result (0.00%) is not just "typical" of the resampled
  distribution — it is what **every single one** of the 50 magnitude-resampled
  realizations also produced. Rank: 100th percentile in the trivial sense that 0.00% is
  the only value the distribution ever takes.
- **On the pass axis:** the real result (52.27%) sits almost exactly at the distribution's
  median (49.05%) — roughly the 52nd percentile by count (26/50 draws at or below it).
  Not a lucky draw; a thoroughly central one.
- **On the combined gate:** the real draw clears (`floor_ok=True`), same as 25/50 (50%) of
  the resampled family — squarely inside, not at an edge of, what the fitted family calls
  plausible.

## 4 — Honest read: robust or lucky-draw-flattered?

**The "0.00% bust" headline is robust, not a lucky draw — this is the strongest possible
result the magnitude-resampling axis could have produced for it.** Every one of 50
independently-fitted-and-drawn realizations, including several with a worse tail-loss day
than anything ORB-MNQ-1's real 6+ year history has ever produced, still bust at exactly
0.00% under `pol_cushion`. That is a property of the *mechanism* (a multiplier that caps
at 0.75× and shrinks toward zero as the trailing-DD cushion shrinks is close to
self-protecting by construction against a single-day blowout, at k=1 lot size on this
book's loss-magnitude scale) — not an artifact of which one history happened to occur.
This is exactly the opposite of what the c1 book's own characterization found (2-leg book:
mean bust 7.46%, only 30% cleared the gate on the bust axis alone) — the two books differ
qualitatively here, which is itself useful evidence for the parent notice's open §3-C
question (skew-heavy books do **not** uniformly show a wide bust-axis gap; the
sizing/cushion mechanism matters as much as the book's own shape).

**But the *combined* "bust-elimination finding clears the gate" framing is considerably
less robust than the 0.00%-bust number alone suggests**, because the frozen gate has a
second, independent requirement (pass≥50%) that this same magnitude resampling shows is
genuinely uncertain — 24.17pp of spread, only half the resampled family clears it, and the
real draw's 52.27% is a coin-flip-adjacent outcome, not a comfortable margin above the
floor. If tonight's cushion probe (or anything built on it) is read as "the gate clears,
full stop," that overstates the finding: read correctly, it is "the bust half of the gate
is essentially guaranteed by the mechanism; the pass half is roughly a 50/50 proposition
given what the underlying P&L-magnitude process can plausibly produce, and the one history
that actually happened landed almost exactly on the coin's own median." **Recommendation
for whoever routes this: cite the bust-axis result with confidence; do not cite the
combined pass+bust "gate cleared" framing as more certain than a 50% resampled clear-rate
supports.**

Caveat carried forward from §1/§2 above, not re-litigated here: the skew fidelity gap and
the EOD-only substitution both bound how far this evidence generalizes — this is a
second, informative case study per notice §3-C, not a closure of the notice.

## 5 — Rerun

```bash
python lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/run_nsurv_magnitude_probe.py
```

Reads the same cached `MNQ.v.0` 15m panel and pre-registration thresholds as the sibling
cushion probe; no network, no spend, no writes outside this directory. Wall time ≈340s
single-threaded (50 realizations × ~2 `run_policy_orb` calls each region, one real-book
anchor pair).

## Audit hooks

```bash
# Headline numbers, reproducible from the committed artifact
python -c "import json; d=json.load(open('lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json', encoding='utf-8')); print(d['distribution']['n_zero_bust'], '/', d['n_realizations'], 'zero-bust;', d['distribution']['n_floor_ok'], '/', d['n_realizations'], 'floor_ok;', d['real_single_history_cushion'])"
# expect: 50 / 50 zero-bust; 25 / 50 floor_ok; real book bust=0.0 pass=52.27 both conventions

# EOD-only == intraday-honest equivalence on the real draw (load-bearing for §2's scope note)
python -c "import json; d=json.load(open('lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json', encoding='utf-8')); print(d['real_single_history_cushion']['equivalence_ok'])"
# expect: True
```
