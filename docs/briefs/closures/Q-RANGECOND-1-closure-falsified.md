# Q-RANGECOND-1 — CLOSURE: `FALSIFIED` (corrects the retracted `RESOLVED` verdict)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-31 (supersedes [`Q-RANGECOND-1-closure-resolved.md`](Q-RANGECOND-1-closure-resolved.md), retracted same day)
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-RANGECOND-1-verdict-preregistration.md`](../pre-registration/Q-RANGECOND-1-verdict-preregistration.md) — frozen 2026-08-30, unchanged; the pre-registered gate itself was never wrong, only the input data feeding it
**Live effect:** none — conditioner-role/filter research only; no entry, sizing, or timing construct was ever licensed; no `core/`, Pine, allocation, `dd_protection`, or rail change
**Spend / K:** $0.00 · `K_intrinsic=1` (disclosure only, unchanged from the retracted closure) · Cap seat not claimed
**Artifacts:** [`rangecond_1_2026-08-30/RESULTS.md`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/RESULTS.md) (updated in place with the corrected numbers) · [`phase1_2_3_conditioned_orb.py`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py) · [`RESULTS.json`](../../lab/analysis/_inbox/rangecond_1_2026-08-30/RESULTS.json) · [defect audit note](../../notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md)

---

## 1. Verdict (§6 asserted against the corrected numbers)

| §6 route | Trigger | Actual (corrected) | Fired? |
|---|---|---|---|
| `RESOLVED` | L1 AND L2 AND L3 AND L4 | L1✓ (n=346≥30) · L2✗ (WR diff CI `[-5.91pp,+7.18pp]`, includes 0) · L3✗ (mean-win diff CI `[-0.300R,+0.204R]`, includes 0) · L4✗ (conditioned WR 47.98% < 55%) | — |
| `FALSIFIED` | Diffs indistinguishable from/worse than unconditioned, OR L4 fails while L2/L3 clear | Diffs indistinguishable (both L2 and L3 fail on their own CIs) — the disjunctive trigger's first clause fires | ✓ |
| `AMBIGUOUS-HOLD` | L1 fails (n<30) | n_conditioned=346 ≫ 30 — L1 passes | — |

Not a borderline call: WR diff (+0.75pp) is within noise of zero; mean-win diff (-0.058R) is
*negative*. Every limb beyond L1 fails decisively, not marginally.

## 2. What happened, and why this supersedes the retracted `RESOLVED` closure

The original closure ([`Q-RANGECOND-1-closure-resolved.md`](Q-RANGECOND-1-closure-resolved.md))
reported conditioned WR 66.47% vs. unconditioned 41.72% (+24.75pp), both CIs clearing zero
decisively. That result was computed against `data_lib.py::overnight_ohlc`'s buggy definition,
which silently included the [16:00,18:00) ET post-RTH-close window in each trading day's own
"overnight range" — bars occurring strictly *after* that day's RTH session had already closed,
two hours after the very outcome (`RTH_range_d`) the conditioner was meant to lead. Codex's PR
#227 review caught this while checking Pine/Python parity; independently re-verified and
quantified the same day (full account: the linked audit note) before this closure was written.
Under the corrected, genuinely-pre-RTH-only conditioner, the entire apparent effect vanishes —
see the audit note's own before/after table. **This is not a magnitude correction; the direction
of the finding itself was an artifact of look-ahead contamination.**

The pre-registration's own gate criteria (§C, `docs/briefs/pre-registration/Q-RANGECOND-1-verdict-preregistration.md`)
required no changes — the frozen thresholds (n≥30, CI excludes 0, WR≥55%) are exactly as
originally pre-registered, applied here to corrected input data. No threshold was moved to
produce this outcome (the opposite of Known Trap #12): the gate stayed fixed; the underlying
`bias_overnight` series changed because a defect in its computation was fixed.

## 3. What this closure does NOT license

- **No re-reading of `ORB-MNQ-1`'s standing PARK status as anything other than unchanged.** The
  addendum the retracted closure filed on `b3-orb-mnq-payability-line.md` is itself retracted
  there, same day — see that document's own dated correction.
- **No claim that the overnight-range conditioner is useless for ORB-shaped constructs in
  general.** This closure tests exactly one pairing (the frozen `H-RANGEXFER-1` conditioner ×
  `ORB-MNQ-1`'s own frozen construct, on the current canonical panel) and finds no signal. It
  does not test other conditioners, other thresholds, or other base constructs.
- **No claim that `Q-RANGEXFER-1`'s own closure verdict is wrong.** That brief's own presence
  battery (L1-L3) was independently re-run under the corrected conditioner and still passes for
  both affected hypotheses (`H-RANGEXFER-1`, `H-RANGEXFER-1.a`) — the underlying predictive
  relationship between overnight range and same-day RTH range still clears statistical
  significance, just at roughly half the originally-reported magnitude. `Q-RANGEXFER-1` gets its
  own separate, dated amendment (not a closure change, since its own verdict did not change) —
  see that brief's own §11.
- **No re-proposal of this exact pairing without new evidence.** See the re-proposal bar below.

## 4. Defects found in the frozen brief (recorded, not repaired)

None in `Q-RANGECOND-1`'s own brief or pre-registration text — both were adversarially reviewed
and are unchanged. The defect was in a shared upstream dependency
(`data_lib.py::overnight_ohlc`), corrected at its own root per the audit note; this closure
reuses the corrected function, unmodified further.

## 5. Lesson candidates

See the audit note's own lesson candidate (a genuinely independent, differently-sourced
reimplementation — the Pine port, reviewed by an independent reviewer — caught what every
in-repo verification pass sharing the same underlying computation could not). Not repeated here
to avoid the two homes for one lesson trap.

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `FALSIFIED`.
- **Model update:** The overnight-range conditioner, once genuinely restricted to pre-RTH-open
  information, shows no measurable relationship to `ORB-MNQ-1`'s own win rate or mean win. The
  presence-verified predictive relationship between overnight range and same-day RTH-range
  *magnitude* (`Q-RANGEXFER-1`) still holds under the correction — but that relationship, on its
  own, does not translate into a useful entry-day filter for this specific breakout construct.
  Predicting that a day's RTH range will be elevated is not the same as predicting that
  `ORB-MNQ-1` will win more often or win bigger on that day — the two are conflated in the
  original mechanism story (parent brief §1, already flagged there as "plausible but not uniquely
  predicted"), and this result is direct evidence the conflation doesn't hold in practice for
  this construct.
- **Next:** `STOP`
- **Routing:** `STOP` — no addendum stands on `b3-orb-mnq-payability-line.md` beyond the
  retraction of the original one; the parked pursuit's own standing (`PARK`, unchanged) is
  correct and this closure adds no new re-entry evidence.
- **Entry packet:** n/a — STOP.
- **Stop rule / re-proposal bar:** new mechanism evidence — a genuinely different conditioning
  variable, a genuinely different base construct, or new data — not a retuned threshold, a
  different panel, or a re-run of this exact pairing under the same (now-corrected) inputs. The
  correction here was to a defect in the DATA, not a design choice; there is nothing left to
  retune.
- **Board write:** `SESSIONS Open/next: Q-RANGECOND-1's RESOLVED verdict retracted and corrected
  to FALSIFIED 2026-08-31 -- a look-ahead defect in data_lib.py::overnight_ohlc (Codex PR #227
  review) inflated the original result; corrected, the conditioner shows no useful signal for
  ORB-MNQ-1's own payoff shape. b3-orb-mnq-payability-line.md's own addendum retracted same day.
  ORB-MNQ-1 stays PARKED with no new re-entry evidence. Q-RANGEXFER-1's own closure verdict is
  unaffected (numbers corrected via amendment, presence battery still passes both affected
  hypotheses).` Owner: this closure.
- **Registry:** `n/a — governance/data-defect correction, not a strategy-grounds kill on new
  evidence`.

## §10 audit-hook discharge

```text
$ python lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py
WR diff CI=[-0.0591,+0.0718] (includes 0), mean-win diff CI=[-0.2997,+0.2044] (includes 0),
VERDICT=FALSIFIED                                                                       OK

$ grep -n "et_minute < RTH_OPEN_MIN" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py
confirms the corrected overnight_ohlc restriction is in place                           OK
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-31 | Closure authored — corrects and supersedes `Q-RANGECOND-1-closure-resolved.md` after the `data_lib.py` look-ahead defect (Codex PR #227) was independently verified and fixed | Claude Code |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-RANGECOND-1-closure-falsified.md
```
