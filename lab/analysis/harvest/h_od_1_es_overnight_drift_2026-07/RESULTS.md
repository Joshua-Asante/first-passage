**Theme:** harvest
**Status:** ACTIVE — SR917 overnight hour on ES IS — Stage-2/4 results
# H-OD-1 Stage-2/4 RESULTS — SR917 overnight hour on ES IS

**Campaign:** `h_od_1_es_overnight_drift`
**Pre-reg:** [`docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md`](../../../docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md) (frozen `9d5b2ec`; §8 GO 2026-07-16/JA)
**Manifest:** [`discovery_manifests/h_od_1_es_overnight_drift.json`](../../../discovery_manifests/h_od_1_es_overnight_drift.json) — **closed** 2026-07-16, K=1 banked (ES family bank → 2)
**Machine report:** [`stage2_4_report.json`](stage2_4_report.json) · edge series [`stage4_is_edges.csv`](stage4_is_edges.csv)
**Cost harness:** [`lab/discovery/cost_es.py`](../../discovery/cost_es.py) — FROZEN PASSIVE model (0.5 ES tick TOTAL RT + commissions). D5's `cost_mnq.py` crossing model was NOT used (handoff §5 guard held).

---

## Verdict — Stage-2 cost-law **KILL** (campaign FALSIFIED per pre-reg §6) — with a **gate-geometry defect finding**: the mechanism CONFIRMED in-sample; the frozen gate was structurally unreachable for it

| Metric | Value |
|---|---|
| IS sessions (both 02:00 + 03:00 bars) | **2,190** (2010-06-07 → 2018-12-31; 2 days dropped missing a bar) |
| Mean gross edge (long 02:00→03:00 ET) | **+1.444 bp** / session |
| Session σ / t-stat | 13.41 bp · **t ≈ 5.0** |
| Gross ann. Sharpe (diagnostic) | **1.709** · hit rate 0.502 |
| Per-year mean edge | **positive all 9 years** (0.46 – 2.75 bp) |
| 4× RT hurdle (frozen passive, IS median px 1942.1) | **5.046 bp** (RT $12.25 = $6.25 slip + $6.00 comm on $97.1K notional) |
| Margin | **−3.60 bp** (edge is ~3.5× below the hurdle) |

**PASS iff** mean gross edge ≥ 4× RT cost fraction. **Failed.** Stage-5+ not run (hard kill).
The realized edge matches the SR917 cohort declaration almost exactly (+1.444 vs +1.5 bp/day;
realized δ/σ 0.108 vs cohort 0.093) — **the transfer premise held; the economics did not.**

Per-year mean edge (bp): 2010 1.47 · 2011 1.88 · 2012 1.19 · 2013 1.24 · 2014 0.93 ·
2015 2.75 · 2016 1.72 · 2017 0.46 · 2018 1.33.

---

## Frozen construct (H1) as executed

| Piece | Pin |
|---|---|
| Clock | 02:00 → 03:00 America/New_York (DST-aware), unconditional LONG, one RT/session |
| Edge | `ln(open_0300 / open_0200)` on the exact 1-minute bars |
| Series | `ES.FUT` parent 1m → ET-day volume-lead stitch (D5/DISC-CAMP-0 pattern) |
| Cost | FROZEN passive: 0.5 ES tick **total** RT ($6.25) + $3.00/side commission; ES-parent notional ($50 × px) |
| Placebo / OOS / Stage-6 | **never reached** — Stage-2 killed on IS |

---

## Gate-geometry defect (the load-bearing finding)

The pre-reg §R.1 attested the Stage-2 gate REACHABLE via a cell (~1.16 bp hurdle < 1.5 bp
cohort edge) that does **not** reproduce under corrected arithmetic. Two process defects:

- **PD-1 — commission fraction mis-scaled ×10 in the frozen pre-reg.** §2/§R.1 called ES-parent
  commissions "≤ 0.03 bp, negligible"; the correct figure is **0.27 bp** RT at index 4400
  ($6.00 / $220K) and **0.62 bp** at the IS median ($6.00 / $97.1K) — same order as the slip itself.
- **PD-2 — price-basis mismatch.** §R.1 priced the hurdle at a *recent* index level (~4400) while
  Stage-2 adjudicates on the *IS panel* (median 1942), where the cost fraction is ~2.3× larger.

**Reachability recompute (plausible-true world = cohort +1.5 bp):**

| Basis | 4× hurdle | True world passes? |
|---|---|---|
| IS median 1942, full frozen cost | 5.05 bp | NO |
| Recent 4400, full frozen cost (PD-1 corrected) | 2.23 bp | NO |
| IS median, slip-only (zero commission) | 2.57 bp | NO |
| Recent 4400, slip-only (zero commission) | 1.14 bp | only cell that passes — requires BOTH defects |

**Under commissions-included arithmetic there is no price basis at which the true mechanism
passes the frozen Stage-2 gate.** RESOLVED was unreachable before data arrived, and the §R
simulation failed to flag it — the two conjuncts of the HARV lane ADR §4 falsifier
([`2026-07-13-harv-discovery-lane-ratification.md`](../../../docs/adr/2026-07-13-harv-discovery-lane-ratification.md)),
which therefore **FIRES on this closure**. Amending/superseding ADR (Proposed):
[`2026-07-16-harv-attestation-same-units-supersession.md`](../../../docs/adr/2026-07-16-harv-attestation-same-units-supersession.md).

### D5 recount under the same test

D5's Stage-2 gate was **also** unreachable at cohort magnitude: measured session σ 26.26 bp ×
cohort δ/σ 0.113 ⇒ plausible-true mean ≈ **2.97 bp** vs hurdle **11.06 bp** (~3.7× short). D5's
§R simulated only the Stage-6 Sharpe floor (0.65 vs gross 1.79) and never priced the Stage-2
clause in bp at instrument economics; its own RESULTS conceded "directional footprint survives;
tradeability does not," and its pre-reg §4/§6 falsifier lists did not include Stage-2 (the
closure called itself a "§6 *analogue*"). Same defect class, same-units failure.

### Governance disposition

- **Harvest-intake §4 doctrine falsifier count: 0-of-2** (corrects the prior STATE "1-of-2"
  line, whose reasoning cited the Stage-6 attestation to validate the Stage-2 gate). Neither
  campaign closed FALSIFIED *on its primary confirm clause under a correctly-reachable gate* —
  the ADR's parenthetical routes both, as gate-geometry failures, to the HARV lane §4 falsifier
  instead. H-OD-1's mechanism evidence (t≈5, 9/9 years) is, if anything, evidence FOR the
  transfer premise. Doctrine verdict remains **open** (not RESOLVED — no OOS confirm; not
  FALSIFIED — no counting closure). Next counting closure: H-TSMOM-1, under the corrected
  same-units attestation.
- **Campaign verdict stands: FALSIFIED at Stage-2** per this campaign's own §6 (Stage-2 kill is
  an explicit trigger in H-OD-1's frozen §4/§6, unlike D5's). Success-eligible close; **K=1
  banked; ES family bank → 2** (H-TSMOM-1 still fundable at K_eff=3, floor 0.98 ≤ Cap 1.0).
- **Methodology lesson:** M-20 (candidate) in
  [`methodology_lessons.md`](../../../docs/methodology/lessons/methodology_lessons.md) — §R must
  simulate every bundled gate **in that gate's own units at the panel-era price basis,
  commissions included**; Sharpe-space attestation of the confirm floor does not discharge a
  bp-space cost gate.

---

## Reproduce

```bash
# Stage-2/4 (research venv; reads the era-tagged IS cache)
.venv-research/Scripts/python.exe lab/analysis/h_od_1_es_overnight_drift_2026-07/run_stage2_es.py
# expect: mean_edge=1.444 bp, hurdle_4x=5.046 bp, VERDICT: KILL, n=2190

# Reachability recompute (pure arithmetic)
python -c "print('IS:',round(4*(6.25+6)/(1942.1*50)*1e4,2),'| 4400:',round(4*(6.25+6)/(4400*50)*1e4,2),'| sliponly-4400:',round(4*6.25/(4400*50)*1e4,2))"
# expect: IS: 5.05 | 4400: 2.23 | sliponly-4400: 1.14   (vs cohort edge 1.5 bp)

# D5 recount (numbers from lab/analysis/d5_nq_intraday_mom_2026-07/stage2_4_report.json)
python -c "print('D5 plausible-true mean bp:', round(0.113*26.260995,2), 'vs hurdle 11.06')"
```
