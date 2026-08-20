# Q-ORBSURV-1 — CLOSURE: `FALSIFIED` (full-panel k=2 misses the pass floor; cushion sizing's gate-clear is k-dependent)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-20
**Lane:** `UNASSIGNED`
**Pre-registration:** [`Q-ORBSURV-1-verdict-preregistration.md`](../pre-registration/Q-ORBSURV-1-verdict-preregistration.md) — frozen at `97f301f`
**Spend / K:** $0.00 · K consumed: 0 (gate-configuration measurement on an already-validated construct, not a strategy-candidate proposal)
**Live effect:** none — ORB-MNQ-1 stays `PARKED`; the 2026-08-03 re-`PARK` ADR is unaffected either way; no `dd_protection`/allocation/Pine/rail surface touched
**Artifacts:** [`run_full_k2_and_postbreak_gate.py`](../../../lab/analysis/c1/orbmnq1_survivor_scoring_2026-08-20/run_full_k2_and_postbreak_gate.py) · [`full_k2_and_postbreak_results.json`](../../../lab/analysis/c1/orbmnq1_survivor_scoring_2026-08-20/full_k2_and_postbreak_results.json)

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | All three configurations (full-panel k=2; post-break-only k=1; post-break-only k=2) clear bust≤3.0% ∧ pass≥50% | Full-panel k=2 **missed** (see below) | — |
| `FALSIFIED` | Any configuration misses either limb | Full-panel k=2: bust 0.0000% (clears) / **pass 41.5067% (misses the 50% floor)** | ✓ |
| `AMBIGUOUS-HOLD` | Post-break sub-window has < 20 Mon-anchored 5-day blocks | Both post-break configurations had 249 blocks, far above the floor | — |

Full per-configuration breakdown:

| Configuration | n_blocks | bust% | pass% | floor_ok |
|---|---:|---:|---:|:---:|
| Full-panel, k=2 | 375 | 0.0000 | **41.5067** | **False** |
| Post-break-only, k=1 | 249 | 0.0000 | 81.3467 | True |
| Post-break-only, k=2 | 249 | 0.0000 | 64.1133 | True |
| Full-panel, k=1 (reused reference, not re-derived) | — | 0.0000 | 52.2700 | True |

## 2. What the pre-registration predicted vs what happened

H-ORBSURV-1 named two possible outcomes: either all three new configurations clear (evidentiary floor met) or any one misses (configuration-dependent gate-clear, negative finding). The second branch fired. The surprise is *where*: the post-break-only sub-window clears comfortably at **both** k=1 (81.35% pass) and k=2 (64.11% pass) — the mechanism's strength in the well-behaved regime is not in doubt. What breaks the full-panel k=2 result is the interaction between the larger contract count and the unexplained pre-2021-09-28 failure period the full-panel window still includes: bust stays perfectly protected (0.0000%, matching every other configuration measured today and in the prior informal probes — `pol_cushion`'s shrink-to-floor property held at every scale tested so far), but pass-rate degrades enough at k=2 to drop **8.76pp below the 50% floor**, whereas at k=1 the same full panel cleared by only 2.27pp (52.27% vs 50%) — confirming, in hindsight, that the k=1 full-panel clear measured earlier today was itself close to the edge rather than a comfortable margin. This closure does not attempt to explain *why* pass-rate degrades with k (that would be a new mechanism candidate, forbidden by §5 — `Q-ORBCUSH-1`'s own thread is `STOP`ped on exactly this kind of question).

## 3. What this closure does NOT license

- Does not license unpark, a re-entry ADR, or GSUB-1 `b3` renewal — moot given the `FALSIFIED` verdict, but recorded per §5 regardless.
- Does not invalidate the full-panel k=1 result (bust 0%, pass 52.27%, `floor_ok=True`) or the informal probes' thirds-split findings — those stand on their own, unchanged. This closure narrows what can be *concluded from them* (not a robust, k-independent property) without disturbing the numbers themselves.
- Does not reopen `Q-ORBCUSH-1` (regime-break mechanism, `STOP`ped) — the pre-break failure period is treated here exactly as that closure left it: real, unexplained, and not re-investigated.
- Does not establish that cushion sizing is a *bad* mechanism generally — only that its gate-clear is configuration-dependent within the range tested (k=1 vs k=2), which is itself useful, bounded information.

## 4. Defects found in the frozen brief (recorded, not repaired)

None found in this Q's own pre-registration. (The sibling `Q-NSURV-2` pre-registration had a pre-Phase-1 correction, recorded there — unrelated to this closure.)

## 5. Lesson candidates

Below the two-incident bar — watch: a single-configuration gate-clear (here, full-panel k=1) sitting close to its own threshold (2.27pp margin) did not generalize to an adjacent, untested configuration (k=2, same full panel) — the margin, not just the pass/fail label, was the informative signal, and it was available before this Q ran. This pairs conceptually with the N-SURV single-history-vs-magnitude-resampled family of findings (`Q-NSURV-1`) — both are instances of "a point estimate close to its own threshold deserves more scrutiny before being cited as a clear," though via different mechanisms (configuration sensitivity here, sampling uncertainty there). Not yet load-bearing; flagged for whoever next cites a near-threshold gate-clear as settled.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** Cushion-proportional sizing's bust-elimination property is robust across every configuration measured to date (k=1, k=2, full-panel, both split halves, thirds, and now the isolated post-break sub-window) — that part of the prior informal probes' finding is reconfirmed and strengthened. What is **not** robust is the combined-gate clear: it holds at k=1/full-panel by a narrow 2.27pp margin and fails at k=2/full-panel by 8.76pp. The mechanism is not a generically "the gate clears" result; it is configuration-specific, and the specific configuration that clears (k=1) was also the only one the informal probes happened to check against the full-panel gate before today.
- **Next:** `STOP`
- **Routing:** n/a — no successor named. A future session naming a genuinely different sizing mechanism (not a re-tuned ceiling, not a re-picked k) or an explanation for the k-dependence itself would open a fresh Q, not amend this one.
- **Entry packet:** n/a — `STOP`, not `ITERATE`.
- **Stop rule / re-proposal bar:** Re-opening this question needs either (a) a genuinely different sizing mechanism tested against the same three configurations, or (b) a mechanistic explanation for why pass-rate degrades with contract count at this construct — not a re-run at a cherry-picked k dressed up as new evidence. The full-panel k=1 clear and the post-break-only clears at both k stay recorded as real, narrow-margin findings in `ops/instruments/MNQ.md` alongside this closure.
- **Board write:** `STATE.md` decision index (2026-08-20 entry) + `docs/briefs/INDEX.md` — this Q moves from Open to Recently closed. Owner: this closure.
- **Registry:** no `docs/rejected_candidates.md` row — this falsifies a *configuration set*, not a mechanism or a deployment target (the target itself is already recorded FALSIFIED, separately, under the 2026-08-03 re-PARK ADR).

## §10 audit-hook discharge

```bash
$ python -c "import json; d=json.load(open('lab/analysis/c1/orbmnq1_survivor_scoring_2026-08-20/full_k2_and_postbreak_results.json', encoding='utf-8')); print(d['verdict'], d['full_panel_k2']['floor_ok'], d['full_panel_k2']['pass_pct'])"
FALSIFIED False 41.50666666666667

$ git log -1 --format='%h' -- docs/briefs/pre-registration/Q-ORBSURV-1-verdict-preregistration.md
97f301f

$ git log -1 --format='%h' -- lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
b84544a  # unchanged by this Q's own execution script, per Forbidden Moves
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Closure authored. Phase 1/2 executed same day as pre-registration, under operator GO ("execute them now"). `FALSIFIED` recorded. | Claude Code (Sonnet 5), operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-ORBSURV-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-ORBSURV-1-closure-falsified.md
```
