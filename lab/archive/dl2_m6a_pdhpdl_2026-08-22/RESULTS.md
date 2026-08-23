# DL-2 (M6A-PDHPDL) -- TRAIN scoring RESULTS

**Status:** `AMBIGUOUS` -- ABANDONMENT (prereg roster mapping: confirm never read, nothing
was tested).

**Prereg:** [`docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md`](../../../docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)
**Charter:** [`docs/adr/2026-08-16-deep-iteration-lane-charter.md`](../../../docs/adr/2026-08-16-deep-iteration-lane-charter.md)
**Handoff:** [`docs/briefs/rnd-pipeline/2026-08-22-cc-handoff-dl2-m6a-step2-train-scoring.md`](../../../docs/briefs/rnd-pipeline/2026-08-22-cc-handoff-dl2-m6a-step2-train-scoring.md)

## Sec6 step 2 -- TRAIN + nomination

All 10 frozen variants (Sec2) scored on 6A.FUT TRAIN (2010-06-06 -> 2019-01-01, 2,200
Globex sessions, 2,815,486 stitched 1-minute bars; 35 UTC roll days -> 35 roll sessions
excluded from entries). All 10 net-negative on TRAIN.

| V | Lookback | Drift | Style | Target | n | net annSR | trades/wk | median stop (ticks) | cost-law ratio |
|---|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | 1 | unconditional | close_confirm | 2R | 1811 | -1.6100 | 4.050 | 82.0 | 12.62 |
| 2 | 1 | unconditional | close_confirm | 3R | 1811 | -1.6104 | 4.050 | 82.0 | 12.62 |
| 3 | 1 | aligned | close_confirm | 2R | 1364 | -1.6121 | 3.050 | 84.0 | 12.92 |
| 4 | 1 | aligned | close_confirm | 3R | 1364 | -1.6220 | 3.050 | 84.0 | 12.92 |
| 5 | 2 | unconditional | close_confirm | 2R | 1500 | -1.2596 | 3.355 | 116.0 | 17.85 |
| 6 | 2 | unconditional | close_confirm | 3R | 1500 | -1.2750 | 3.355 | 116.0 | 17.85 |
| 7 | 2 | aligned | close_confirm | 3R | 1179 | -1.3654 | 2.637 | 121.0 | 18.62 |
| 8 | 1 | aligned | retest_limit | 2R | 1327 | -0.8471 | 2.968 | 80.0 | 12.31 |
| 9 | 2 | aligned | retest_limit | 3R | **1144** | **-0.6840** | 2.558 | 118.0 | 18.15 |
| 10 | 1 | unconditional | retest_limit | 2R | 1752 | -0.7580 | 3.918 | 79.0 | 12.15 |

Nominee = **V9** (2-session lookback, drift-aligned, retest-limit, 3R target) -- argmax
train net annSR, no fallback, no walk-down, per Sec6. No argmax tie (checked).

| Gate | Result |
|---|---|
| 2a cost-law (net annSR > 0 AND ratio >= 4x at realized geometry) | **FAIL** -- net annSR -0.6840; ratio 18.15x (passes alone) |
| 2b SPA (Hansen, consistent p <= 0.10, full 10-variant universe, block=20, B=10000, seed=11) | **FAIL** -- p = 0.9755 |
| 2c N-ACT cadence (>= 1 trade/week) | PASS -- 2.558/wk |
| 2d M-16 (+1 tick/side additional slip, net annSR > 0) | **FAIL** -- net annSR -0.9185 |

**Verdict:** nominee fails 3 of 4 nomination gates -> **ABANDONMENT** (dated, no strike
against the lane's 2-campaign falsification budget, per prereg Sec4 / charter Sec4(c)).
Confirm partition (M6A.FUT) never read, per Sec5 forbidden moves.

**This is DL-2's own abandonment, the 2nd consecutive after DL-1 -- charter Sec4(c)'s
audit-report duty has now tripped** (2 consecutive abandonments), owed at the next
quarterly programme audit.

**Diagnostic note (disclosed, not a code defect -- ruled out by direct inspection before
accepting this verdict).** All 10 variants show win rates in a sensible 42.6%-46.6% band,
balanced long/short splits (~50/50 every variant), and `net = gross - n * $2.60` reproduces
exactly for every variant checked -- no evidence of a sign/direction defect. The structural
driver of the uniform negativity: 85-90% of trades exit via `force_flat`, not stop or
target (e.g. nominee V9: 1091/1144 = 95.4% force-flat, only 53 stops, 0 targets). The
prior-session-derived stop/target geometry (median stop ~80-130 ticks, target 2-3x that) is
wide relative to how far price can travel in the remainder of a single Globex session
before the next day's 16:55 ET force-flat -- so almost no trade ever resolves to a real R
multiple; realized P&L is close to a small, cost-negative directional residual on the
un-resolved bars. This is a property of the frozen construction (1-session holding period
vs. a full-prior-session-range-derived stop), not a signal that the mechanism itself lacks
directional information -- disclosed per Sec2.4's own instruction ("that's a
`DONE_WITH_CONCERNS` flag for the operator, never a silent in-flight edit") rather than
silently patched.

Full per-variant table (all 10 variants' net annSR, cadence, cost-law ratio) and gate
detail: [`train_results.json`](train_results.json). Engine: `stitch.py` / `engine.py` /
`score.py` / `variants.py` / `run_train.py`; unit-tested against hand-constructed synthetic
slices ([`test_units_synthetic.py`](test_units_synthetic.py), all (a)-(e) gates pass,
including a known synthetic roll day correctly skip-back'd and a known synthetic
break-and-hold reproducing the exact hand-worked R multiple) before the full TRAIN run.

## Geometric feasibility diagnostic (2026-08-22, post-closure -- not a Sec6 step, no
confirm touched, no OUTER-investigation slot consumed; discharges the Iterate block's own
stop rule below)

Ran [`geometric_feasibility_diagnostic.py`](geometric_feasibility_diagnostic.py) per the
Iterate block's own stop rule (ox-alpha's Q3 proposal, reconciled). Two measures, both on
TRAIN data already read:

**(A) Full-session ratio, unconditional (no signal needed) -- R = a session's own achievable
range (open through the 16:55 ET force-flat bar) / the reference-window width its PDH/PDL
level would be derived from:**

| Lookback | n sessions | median R | mean R | % R<1.0 | % R<0.5 | % R>2.0 | % R>3.0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 session | 2163 | 1.000 | 1.159 | 49.8% | 8.5% | 7.8% | 1.8% |
| 2 sessions | 2162 | 0.687 | 0.779 | 77.4% | 24.8% | 1.3% | 0.2% |

**(B) Realized-trade MFE ratio, conditional on trades that actually fired** (an
already-favorably-selected subset -- these are the sessions where price broke out at all)
-- max favorable excursion from entry to force-flat, as a fraction of that trade's own risk
(stop distance):

| V | Lookback | Target | n | median MFE/R | mean MFE/R | % never reach 1R | % reach own target |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 2R | 1811 | 0.342 | 0.476 | 89.3% | 1.1% |
| 2 | 1 | 3R | 1811 | 0.342 | 0.476 | 89.3% | 0.3% |
| 3 | 1 | 2R | 1364 | 0.328 | 0.448 | 90.2% | 0.9% |
| 4 | 1 | 3R | 1364 | 0.328 | 0.448 | 90.2% | 0.1% |
| 5 | 2 | 2R | 1500 | 0.230 | 0.317 | 96.7% | 0.3% |
| 6 | 2 | 3R | 1500 | 0.230 | 0.317 | 96.7% | 0.0% |
| 7 | 2 | 3R | 1179 | 0.219 | 0.303 | 96.9% | 0.0% |
| 8 | 1 | 2R | 1327 | 0.380 | 0.527 | 87.0% | 2.0% |
| 9 | 2 | 3R | 1144 | 0.255 | 0.343 | 96.0% | 0.0% |
| 10 | 1 | 2R | 1752 | 0.397 | 0.564 | 85.6% | 2.2% |

**Verdict: the construction is confirmed geometrically infeasible on M6A at this holding
period -- not a marginal mismatch.** Even the median SESSION (lookback=1) barely retraces
its own reference width (R=1.0), which only clears the STOP distance, with essentially no
room left for a 2-3R target beyond it (only 7.8%/1.8% of sessions ever have that much room).
Lookback=2 is measurably worse (median R=0.687, wider reference window without a
proportionally wider achievable range). Among trades that actually fired -- already the
favorable subset, since a breakout had to occur for entry to trigger at all -- 85-97% never
even complete a full 1R favorable move, and essentially none (0-2.2%) ever reach their own
2R/3R target. This resolves the Iterate block's stop rule: **R << 1, construction retired
for M6A**, per the pre-committed rule -- not an ad hoc call made after seeing this result.

## Iterate -- loop exit (canon `docs/methodology/inqhiori-canon.md` Sec16; mandatory per
`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`; updated 2026-08-22 post-diagnostic,
append-only -- the original text stands above the "post-diagnostic update" callouts below)

- **Verdict used:** `AMBIGUOUS` -- ABANDONMENT (prereg roster mapping; confirm never read,
  nothing tested).
- **Model update:** Cross-checked against a sanitized ox-alpha second opinion
  (2026-08-22, per `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`) that hypothesized
  DL-1's and DL-2's failures might be "one disease at two stages." Reconciled by re-running
  DL-1's own archived harness and computing its exit-reason mix: DL-1 resolves 40-70% of
  trades to genuine stop/target (an adverse hit-rate-ratio, candidate-level failure), sharply
  unlike DL-2's 85-95% force-flat non-resolution. **The hypothesis does not survive contact
  with the data** -- these are two structurally different failures, not one shared lane-wide
  construction defect. What DOES generalize from DL-2 specifically: a stop/target derived from
  a reference window materially wider than what price can traverse within the allowed holding
  period before force-flat is a live, disclosed, untested-for-generality risk in this
  construction family (1-2 session lookback -> opposite-extreme stop -> fixed-R target ->
  single-session force-flat), independent of DL-1's own unrelated candidate-level failure.
- **Next:** `ITERATE`
- **Routing:** dated packet / operator decision item -- not a fresh Q/H reframe yet, not a
  new Identify thread. The lane's next campaign (if any) is gated on an operator decision
  informed by a cheap diagnostic, not an automatic successor.
- **Entry packet:** A successor reusing this construction (reference-window-derived
  stop/target + single-session force-flat hold), on any instrument or mechanism id, must
  carry into its own prereg Sec0 Rule-0 reads: (1) the geometric-feasibility-ratio diagnostic
  below, computed and disclosed for its own target instrument -- not assumed healthy; (2) the
  roll-day-derivation-from-1m-cache technique (Sec3/stitch.py, proven byte-equivalent to a
  native `ohlcv-1d` pull against DL-1's own cache pair, 0/83,165 mismatches) as a reusable,
  already-validated positive carry-forward, needing no re-validation; (3) explicit
  acknowledgment that DL-1's own abandonment is NOT corroborating evidence for a shared
  construction defect (Model update above) -- citing it as such would be a fresh error, not
  inherited from this one.
- **Stop rule / re-proposal bar:** No successor may freeze a prereg reusing this stop/target/
  hold construction without first running and disclosing the **geometric-feasibility-ratio**
  diagnostic (ox-alpha's Q3 proposal, reconciled as sound): R = (distribution of price
  movement reachable within one holding period, from market data alone) / (reference-window-
  derived stop/target width), for the target instrument. If R is healthy (reachable move
  comparable to or exceeding the reference width), the construction is cleared for that
  instrument and a fresh campaign may proceed, K-accounted separately, on its own merits. If R
  replicates DL-2's pathology (R << 1, i.e. cutoff-forced exits would dominate), this
  construction is retired for that instrument class without burning a further OUTER-
  investigation slot on it.
  **>> RESOLVED 2026-08-22 (post-diagnostic update, append-only — see the section above):**
  R replicates the pathology, decisively (median R=1.0 at lookback=1 with essentially no
  target-reaching room; 0.687 at lookback=2; 85-97% of realized trades never complete a
  full 1R move). **This construction (opposite-prior-extreme stop/target derived from a
  1-2 session lookback, single-session force-flat hold) is retired for M6A**, per the
  pre-committed rule. It remains untested for generality on other instruments -- the entry
  packet's own requirement (any successor must run this same diagnostic for its own target
  instrument, not assume the M6A result transfers) is unaffected by this resolution.
- **Board write:** [`STATE.md` Scheduled forward triggers, No fixed date / gated section
  ("Deep-iteration lane -- geometric-feasibility-ratio audit RESOLVED: construction retired
  for M6A")](../../../STATE.md).

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | RESULTS.md authored; Sec6 step 2 closed ABANDONMENT | Claude Code (train-scoring session) |
| 2026-08-22 | Iterate block added (canon Sec16); ox-alpha sanitized second opinion sought and reconciled against a re-run of DL-1's own archived harness | Claude Code (same session) |
| 2026-08-22 | Geometric-feasibility-ratio diagnostic run per the Iterate block's own stop rule (`geometric_feasibility_diagnostic.py`) -- construction confirmed geometrically infeasible on M6A (median R=1.0 at lookback=1, 0.687 at lookback=2; 85-97% of realized trades never complete a 1R move). Retired for M6A per the pre-committed rule; Iterate block's Stop-rule field updated in place (append-only) with the resolution. | Claude Code (same session) |
