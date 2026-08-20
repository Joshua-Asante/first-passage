# Q-ORBCUSH-1 — CLOSURE: `FALSIFIED` (trailing mean-R does not explain the 2021-09-28 break; date-correlation clears 0 of 3 pre-registered windows)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-20
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-ORBCUSH-1-verdict-preregistration.md`](../pre-registration/Q-ORBCUSH-1-verdict-preregistration.md) — frozen at `b84544a`
**Spend / K:** $0.00 · K consumed: 0 (diagnostic/explanatory question about an already-real pattern, not a strategy-candidate proposal — same class as Q-GEOFIT-1)
**Live effect:** none — ORB-MNQ-1 stays `PARKED`; no `dd_protection`/allocation/Pine/rail surface touched; the 2026-08-03 re-`PARK` ADR is unaffected either way (§5, frozen)
**Artifacts:** [`run_meanr_regime_gate.py`](../../../lab/analysis/c1/q_orbcush_1_2026-08/run_meanr_regime_gate.py) · [`results_meanr_regime_gate.json`](../../../lab/analysis/c1/q_orbcush_1_2026-08/results_meanr_regime_gate.json) · [`RESULTS_meanr_regime_gate.md`](../../../lab/analysis/c1/q_orbcush_1_2026-08/RESULTS_meanr_regime_gate.md)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | date-correlation clears (≥75% higher-bucket / ≤40% lower-bucket) at ≥2 of 3 windows AND direction stable (no sign-flip) across all three | date-correlation clears **0 of 3** windows | — |
| `FALSIFIED` | date-correlation fails at ≥2 of 3 windows, OR any sign-flip in direction between any two windows | date-correlation fails at **3 of 3** windows (fires the OR-condition on this clause alone) | ✓ |
| `AMBIGUOUS-HOLD` | primary classifier structurally unreliable at n < 30 trades in a pre-registered window, and the cost-fraction fallback also unreliable | smallest bucket (W3 lower-edge) has 530 trades — 18× the floor; sparsity condition never approached | — |

Full per-window breakdown (higher-edge bucket needs ≥75% post-2021-09-28; lower-edge needs ≤40%):

| Window | Higher-bucket post-break | Lower-bucket post-break | Clears? |
|---|---|---|---|
| W1 = 20 trades | 69.02% (fails, 5.98pp short) | 65.33% (fails, 25.33pp over) | No |
| W2 = 63 trades | 74.96% (fails, 0.04pp short) | 58.93% (fails, 18.93pp over) | No |
| W3 = 126 trades | 80.55% (clears) | 51.38% (fails, 11.38pp over) | No |

The lower-edge bucket's ≤40% ceiling is the binding failure at every single window — it never gets closer than 11.38pp over. Direction was in fact stable (`HIGHER_CLEARS_LOWER_DOES_NOT` under the cushion-sizing gate at all three windows, no sign-flip) — irrelevant to the verdict since the date-correlation failure already fires the Reject clause independently on its own OR-branch.

## 2. What the pre-registration predicted vs what happened

The pre-registration named mean-R as the leading candidate specifically because Stage 1 of the prior probe found it moved the most across the break (+0.0076R pre → +0.0901R post) of anything measured, and it was explicitly distinguished from the already-refuted volatility classifier. The frozen falsification criteria (3 pre-registered windows, no post-hoc window selection, one sign-flip anywhere disqualifying) were carried over unchanged from the volatility round specifically so a repeat of that discipline would be trustworthy either way. No surprise in the *mechanism*: it failed on the same axis (date-correlation) the volatility classifier failed on, not a new failure mode. One thing the pre-registration did not anticipate: the volatility classifier's failure mode was a *sign-flip* across windows (20d inverted vs 63d/126d); mean-R's failure mode is different — direction was stable at every window, but the lower-edge bucket's date-composition simply never got clean enough. Two distinct ways to fail the same falsification bar, which is some evidence the bar itself is doing real discriminating work rather than being an artifact of one classifier's quirks.

## 3. What this closure does NOT license

- Does not resolve *why* the 2021-09-28 break exists — it eliminates one candidate explanation (mean-R regime), not the break itself, which stays real and triple-verified from the prior probe.
- Does not license the cost-to-range-fraction fallback as a substitute test under this same brief — §4's Ambiguous-hold clause only routes to that fallback when the primary classifier is structurally unreliable (sparsity), which never fired here; a cost-fraction test needs its own fresh pre-registration if anyone wants to run it, not a silent extension of this one.
- Does not reopen `Q-POLFRONT-1` or the 2026-08-03 re-`PARK` ADR — unaffected regardless of verdict, per §5.
- Does not cast doubt on the bust-elimination finding (mathematically derivable, regime-agnostic, independently verified across the prior probe's three rounds) — that finding does not depend on this Q's outcome.

## 4. Defects found in the frozen brief (recorded, not repaired)

None found. The build agent flagged one *documentation* ambiguity in the calling session's own restatement of the classifier spec (an expanding-mean vs. rolling-window reading) — resolved in favor of the frozen pre-registration file's literal text (rolling window + expanding causal median threshold), which is the authoritative source and was not itself ambiguous. No edit to the frozen pre-registration was needed or made.

## 5. Lesson candidates

Below the two-incident bar — watch: this is the second distinct classifier (volatility, now mean-R) independently refuted for the same regime break under the same falsification discipline. Two clean nulls on two economically-plausible candidates is itself informative — it raises, without yet confirming, the possibility that this break is driven by something the estate doesn't have a good trailing-classifier vocabulary for yet (a structural/era-bound shift rather than a smoothly-varying trailing statistic), or that two candidates is simply not enough to conclude that. Not yet load-bearing; flagged for whoever considers a third candidate.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** Neither of the two most economically-plausible trailing classifiers (volatility, mean-R) explains the 2021-09-28 break, under an identical, twice-proven-out falsification discipline (3 pre-registered windows, no post-hoc selection, independently re-derived via a separate implementation both times). The break itself is not in doubt — it is triple-verified real and non-boundary-luck from the prior probe. What's confirmed is narrower than hoped: this is a real historical pattern still without a tested causal story, not a pattern that any of the cheap, obvious explanations account for.
- **Next:** `STOP`
- **Routing:** n/a — no successor named. A future session naming a third candidate mechanism (not a re-tuned window on either already-refuted classifier) would open a fresh Q, not amend this one.
- **Entry packet:** n/a — STOP, not ITERATE.
- **Stop rule / re-proposal bar:** Re-opening this question needs a genuinely different candidate mechanism — a different economic story for what changed around late-Sept-2021, tested with a variable this closure and the prior vol-regime round haven't already tried — not a re-tuned window, a re-normalized threshold, or a cost-to-range-fraction re-run dressed up as new evidence. The break itself remains recorded as real, triple-verified, and mechanistically unexplained in `ops/instruments/MNQ.md` (finding N17, appended alongside this closure).
- **Board write:** `SESSIONS Open/next: none owed — Q-ORBCUSH-1 STOPPED; ops/instruments/MNQ.md N17 carries the standing record.` Owner: this closure · [RESULTS](../../../lab/analysis/c1/q_orbcush_1_2026-08/RESULTS_meanr_regime_gate.md)
- **Registry:** n/a — mechanism-search null on an already-real pattern, not a strategy-mechanism rejection (no `docs/rejected_candidates.md` row; same convention as Q-GEOFIT-1 and the prior vol-regime probe round)

## §10 audit-hook discharge

```bash
# Confirm §0 anchors still resolve
$ git log -1 --format='%h' -- lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py
a7c6f7b
$ git log -1 --format='%h' -- core/mc/simulation.py
027a729
$ git log -1 --format='%h' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md
027a729

# Confirm the probe harness this brief builds on is present and untouched
$ git log -1 --format='%h' -- lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
[unchanged since b84544a — imported, not modified, per Phase 1's own verification]

# Confirm the frozen gate this thread measures against
$ grep -n "bust.*3.0%\|P(pass).*50%" docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md
[confirmed present — same gate cited throughout the prior probe and this Q]

# Pre-registration commit predates Phase 1
$ git log --oneline -- docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md
b84544a feat(briefs): open Q-ORBCUSH-1 ...
[Phase 1 executed 2026-08-20, after this commit — ordering holds]
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Closure authored. Phase 1 (build + independent verify + mechanical verdict application) run same day as pre-registration, under operator GO. FALSIFIED recorded. | Claude Code (Sonnet 5), operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md
```
