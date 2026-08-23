# Q-ORBPOS-1 — CLOSURE: `FALSIFIED` (trailing CFTC TFF Leveraged-Funds positioning-extremity does not explain the 2021-09-28 break; date-correlation clears 0 of 3 windows AND gate direction sign-flips)

**Verdict:** `FALSIFIED`
**Closed:** 2026-08-23
**Lane:** `UNASSIGNED`
**Pre-registration:** [`2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md`](../pre-registration/2026-08-22-orbcush-1-tff-positioning-mechanism-prereg.md) — new/uncommitted in this worktree at closure time (authored + GO both landed this session; no prior commit anchor exists yet — cite by path, not hash, until this closure's own commit lands)
**Spend / K:** $0.00 · K consumed: 0 (diagnostic/explanatory question about an already-real pattern, not a strategy-candidate proposal — same class as Q-GEOFIT-1 and its own parent Q-ORBCUSH-1, per §8)
**Live effect:** none — ORB-MNQ-1 stays `PARKED`; no `dd_protection`/allocation/Pine/rail surface touched; the 2026-08-03 re-`PARK` ADR is unaffected either way (§5, frozen)
**Artifacts:** [`RESULTS.md`](../../../lab/analysis/c1/q_orbpos_1_2026-08/RESULTS.md) (Phase 0–4, this closure's full evidentiary record) · [`run_orbpos_tff_probe.py`](../../../lab/analysis/c1/q_orbpos_1_2026-08/run_orbpos_tff_probe.py) · [`results_orbpos_tff_probe.json`](../../../lab/analysis/c1/q_orbpos_1_2026-08/results_orbpos_tff_probe.json) · [`run_log.txt`](../../../lab/analysis/c1/q_orbpos_1_2026-08/run_log.txt) · [`_imported_run_evalseq_orb_intraday.py`](../../../lab/analysis/c1/q_orbpos_1_2026-08/_imported_run_evalseq_orb_intraday.py) (unchanged harness copy) — Implementation B's own script/pull/JSON (the Phase 3 independent re-derivation) live only in a per-session scratchpad path that is **not recoverable from this worktree or committed anywhere in the repo**; its written report and reported numbers are the only surviving record and are quoted, cross-checked, and flagged as unverifiable-at-the-file-level in `RESULTS.md` Phase 3.

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | date-correlation clears (≥75% higher-bucket / ≤40% lower-bucket) at ≥2 of 3 windows AND direction stable (no sign-flip) across all three | date-correlation clears **0 of 3** windows | — |
| `FALSIFIED` | date-correlation fails at ≥2 of 3 windows, OR gate-clearance direction sign-flips between any two windows | **both** independent clauses fire: date-correlation fails at **3 of 3** windows, AND direction is not the same sign at every window (W2 breaks the W1/W3 pattern) | ✓ |
| `AMBIGUOUS-HOLD` | W1 sparsity (<4 pre-break prints) or degenerate threshold, OR MNQ-not-separately-reported with combined-line share <10%, OR primary+secondary both unreliable | 45–46 pre-break prints (≫ the 4-print floor); MNQ confirmed a standalone `209747` TFF line (Phase 0 + both Phase-3 builds); no degenerate threshold at any window | — |

Full per-window breakdown (higher-extremity bucket needs ≥75% post-2021-09-28; lower-extremity needs ≤40%; gate-clearance at k=1 cushion sizing against the frozen bust≤3.0%/pass≥50% gate):

| Window | Higher-bucket post-break | Lower-bucket post-break | Higher cushion pass % | Lower cushion pass % | Direction | Clears? |
|---|---|---|---|---|---|---|
| W1 = 4 TFF prints | 89.64% (clears ≥75%) | 74.44% (fails ≤40% by 34.44pp) | 23.05% (FAIL) | 99.24% (PASS) | `LOWER_CLEARS_HIGHER_DOES_NOT` | No |
| W2 = 13 TFF prints | 96.29% (clears) | 80.40% (fails by 40.40pp) | 62.98% (PASS) | 98.64% (PASS) | `BOTH_CLEAR` | No |
| W3 = 26 TFF prints | 99.26% (clears) | 85.74% (fails by 45.74pp) | 49.52% (FAIL — 0.48pp under floor) | 99.44% (PASS) | `LOWER_CLEARS_HIGHER_DOES_NOT` | No |

The lower-extremity bucket's ≤40% ceiling is the binding date-correlation failure at every window — it never gets closer than 34pp over, because the TFF-covered span (2020-08-04 onward) is itself disproportionately post-break (2021-09-28 falls only ~14 months into a 45–46-print pre-break history), so a roughly-50/50 causal-median split inherits a post-break majority in both buckets by base rate. **Independently and sufficiently on its own**, the gate-clearance direction is not stable: W1 and W3 both show `LOWER_CLEARS_HIGHER_DOES_NOT`, but W2 shows `BOTH_CLEAR` — the higher-extremity bucket clears the survivor gate at W2 (62.98% pass) when it fails at W1/W3 (23.05%/49.52%), which is disqualifying under §4's "same sign at every window, no exceptions" clause by itself, regardless of the date-correlation failure.

## 2. Two independent implementations — comparison (§7 Phase 3 requirement)

Per §7 Phase 3 ("independent, adversarial re-derivation of the classifier — a second, separate implementation, not a re-read"), two teams built the full classifier + gate-clearance pipeline from scratch. **They substantively agree on every qualitative call and on the final verdict**: identical contract line (`209747`, standalone since 2020-08-04), identical classifier formula and causal-lag treatment, identical Ambiguous-hold non-firing, identical 0/3 date-correlation result, and — critically — the **identical** per-window direction pattern (`LOWER_CLEARS_HIGHER_DOES_NOT`, `BOTH_CLEAR`, `LOWER_CLEARS_HIGHER_DOES_NOT`), including the exact same W2 sign-break that disqualifies on its own.

They diverge, materially and disclosed rather than papered over, on **exact magnitude**: post-break date fractions differ by 1–4pp (traced to a day-level vs. print-level fraction denominator between the two builds), and the higher-extremity bucket's cushion-sizing pass rate differs by **5–14pp at every window** (23.05% vs 36.62% at W1; 62.98% vs 52.91% at W2; 49.52% vs 44.61% at W3) — traced to each team independently writing its own per-bucket Monte-Carlo block-selection algorithm (the pre-registration fixes the classifier and the windows, not the block-construction method for a non-contiguous bucket mask), which the smaller, boundary-adjacent higher-extremity bucket is far more sensitive to than the larger, more homogeneous lower-extremity bucket (≤0.80pp gap there at every window). Full comparison table and reasoning: `RESULTS.md` Phase 3.

**This divergence does not create verdict uncertainty.** H-ORBPOS's Reject condition fires on two independent clauses, and both fire under **either** implementation's numbers standing alone — swapping Implementation B's figures in for Implementation A's throughout changes zero Accept/Reject/Ambiguous-hold routing decisions. It is, however, a real, open construction-method ambiguity (how to build MC blocks from a scattered/non-contiguous bucket mask) that a future brief needing a precise higher-extremity-bucket pass-rate number should not paper over by picking whichever implementation's number is more convenient.

## 3. What the pre-registration predicted vs what happened

The pre-registration named Leveraged Funds %OI extremity as the leading candidate specifically because it is sign-agnostic (sidesteps the disputed Wang-1 large-speculator continuation/reversal sign question) and because a crowding extreme is more plausibly connected to an abrupt, date-localized break than a shift in patient real-money allocation. The frozen falsification criteria (3 pre-registered windows, no post-hoc window selection, sign-flip anywhere disqualifying) were carried over unchanged from both prior rounds specifically so a repeat of that discipline would be trustworthy either way. **No surprise in the mechanism**: like mean-R before it, positioning fails on date-correlation (the lower-extremity bucket's ceiling is never approached, missing by 34–46pp at every window — a wider miss than mean-R's own 11–25pp gap, itself already the wider of the two prior rounds' failure margins). **One new failure mode this round adds that neither prior round showed as decisively**: the gate-clearance direction *also* independently disqualifies (W2's sign-break), where volatility failed on a sign-flip alone and mean-R's direction was in fact stable. Positioning fails on **both** of §4's disqualifying axes at once — the least ambiguous of the three nulls.

One genuinely new fact Phase 0/1 surfaced, not anticipated in the pre-registration's own text: MNQ's standalone TFF line does not begin at the 2019-05-06 contract launch but 15 months later (2020-08-04) — the "young contract" caveat §2.2 flagged as a live risk did materialize, though it did not bind (45–46 pre-break prints still clears the sparsity floor 11× over).

## 4. What this closure does NOT license

- Does not resolve *why* the 2021-09-28 break exists — it eliminates a third candidate explanation, not the break itself, which stays real and triple-verified from the Q-ORBCUSH-1 probe.
- Does not license the Asset Manager secondary as a substitute test under this brief — the §4 Ambiguous-hold trigger that alone licenses that fallback never fired (LF was neither sparse nor structurally unreliable), so AM was correctly never run, per §5's forbidden-move on switching category early.
- Does not reopen `Q-POLFRONT-1` or the 2026-08-03 re-`PARK` ADR — unaffected regardless of verdict, per §5.
- Does not license procuring a live TFF/positioning feed, or treat the free-data / already-surviving-construct reasoning in §8 as extending to any other, recurring or live-signal purpose on MNQ or any other instrument (§5, §8).
- Does not cast doubt on the bust-elimination finding (mathematically derivable, regime-agnostic, independently verified across the Q-ORBCUSH-1 probe's three rounds) — that finding does not depend on this Q's outcome.
- Does not, by itself, mandate a fourth candidate-mechanism search. Per §5/§8, three clean nulls (volatility, mean-R, positioning) now sit on this break under an identical, twice-independently-verified falsification discipline; this closure raises, without deciding, an explicit operator review of whether continued search for *any* mechanism behind this specific break is worth further K, ever, before a fourth candidate is proposed.

## 5. Defects found in the frozen brief (recorded, not repaired)

None found in the pre-registration's own frozen text. One under-specification is surfaced by the two independent builds diverging on it (§2, above): §2.3/§4 fix the classifier and the three windows but do not fix a block-construction method for a bucket mask that is *not* a contiguous calendar slice (unlike the prior two rounds' halves/thirds splits, which were contiguous by construction). This is not an error in the frozen document — it was simply never load-bearing before this candidate, since neither volatility nor mean-R produced a scattered, weekly-relabeled bucket mask of this shape. Flagged as an entry-packet item for any future brief that needs a precise per-bucket MC pass rate from a non-contiguous mask (not needed here, since the verdict is robust to it).

## 6. Lesson candidates

**Third incident, same class — now load-bearing, not merely watch.** This is the third distinct classifier (volatility, mean-R, now positioning) independently refuted for the same regime break under an identical falsification discipline, and the third whose failure mode differs from its predecessors (volatility: sign-flip only; mean-R: date-correlation only, direction stable; positioning: both axes fail at once). Three clean nulls under a twice-independently-reproduced discipline is itself the strongest evidence yet that this break is not explained by any trailing-classifier vocabulary this program currently has — worth a named lesson candidate at the next methodology pass (working title: a regime break can be real, triple-verified, and durably resistant to every economically-plausible trailing-classifier explanation tried against it; absence of an explanation after N≥3 independently-falsified candidates is itself information the program should act on, per §8's own pre-committed operator-review trigger, not silently re-run at N=4).

**Second lesson candidate, new to this round specifically:** independently-written Monte-Carlo block-selection algorithms for a non-contiguous/scattered bucket mask can diverge by 5–14pp on the smaller bucket's pass rate even when every upstream input (classifier, threshold, windows, harness) is identical — a genuine implementation-choice sensitivity that neither prior round (contiguous halves/thirds) ever exposed. Below the two-incident bar on its own (this is the first time this specific construction question has come up) — watch for whether a second bucket-mask-shaped candidate reproduces it.

## Iterate — loop exit

- **Verdict used:** `FALSIFIED`
- **Model update:** None of the three most economically-plausible trailing classifiers tried against this break (volatility, mean-R, now CFTC TFF Leveraged-Funds positioning-extremity) explains it, under an identical, now-**thrice**-proven-out falsification discipline (3 pre-registered windows, no post-hoc selection, independently re-derived via a separate from-scratch implementation every time). The break itself is not in doubt — triple-verified real and non-boundary-luck from the Q-ORBCUSH-1 probe. What's newly confirmed: positioning fails more decisively than either prior candidate (both disqualifying axes fire at once, and the lower-extremity bucket's miss margin — 34-46pp — is the widest of the three rounds), and the two-implementation comparison shows the null is robust to a real, disclosed methodological sensitivity (block-construction choice for a non-contiguous mask) that moves the higher-bucket's exact pass rate by up to 14pp without moving the verdict at all.
- **Next:** `STOP`
- **Routing:** n/a — no successor named. Per §5/§8, a future session naming a **fourth**, genuinely different candidate mechanism (not a re-tuned window, category, or normalization on any of the three already-refuted classifiers) would open a fresh Q — and per §8's own pre-committed trigger, should first carry an explicit operator review of whether continued search value on this specific break justifies a fourth attempt, given three clean nulls under an identical discipline.
- **Entry packet:** n/a — STOP, not ITERATE.
- **Stop rule / re-proposal bar:** Re-opening this question needs a genuinely different fourth candidate mechanism — a different economic story for what changed around late-Sept-2021, tested with a variable none of the volatility, mean-R, or positioning rounds already tried — not a re-tuned window, a re-normalized threshold, a category swap (LF↔AM), or a different block-construction algorithm dressed up as new evidence. Per §8, any such fourth proposal should be preceded by an explicit operator review of continued search value, per this closure's own §4/§6 finding of three clean nulls. The break itself remains recorded as real, triple-verified, and mechanistically unexplained in `ops/instruments/MNQ.md` (finding N20, appended alongside this closure).
- **Board write:** `SESSIONS Open/next: none owed — Q-ORBPOS-1 STOPPED; ops/instruments/MNQ.md N20 carries the standing record (third clean null; operator-review-before-fourth-candidate trigger named, not yet exercised).` Owner: this closure · [`RESULTS.md`](../../../lab/analysis/c1/q_orbpos_1_2026-08/RESULTS.md)
- **Registry:** n/a — mechanism-search null on an already-real pattern, not a strategy-mechanism rejection (no `docs/rejected_candidates.md` row; same convention as Q-GEOFIT-1 and Q-ORBCUSH-1, per §8)

## §10 audit-hook discharge

```bash
# Confirm §0 anchors still resolve (re-run at closure time, 2026-08-23)
$ git log -1 --format='%h' -- docs/briefs/Q-ORBCUSH-1-regime-break-mechanism.md
b12689c
$ git log -1 --format='%h' -- docs/briefs/closures/Q-ORBCUSH-1-closure-falsified.md
bcef3e0
$ git log -1 --format='%h' -- docs/briefs/pre-registration/Q-ORBCUSH-1-verdict-preregistration.md
b84544a
$ git log -1 --format='%h' -- ops/instruments/MNQ.md
1e40b11
$ git log -1 --format='%h' -- docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md
027a729
$ git log -1 --format='%h' -- lab/analysis/c1/orbmnq1_cushion_sizing_probe_2026-08-20/run_evalseq_orb_intraday.py
b84544a

# Freeze-before-run check — no longer applicable at closure time (results now exist by design);
# recorded for the record that the pre-registration predated Phase 0 by inspection of its own
# Change History (authored 2026-08-22, GO + all execution 2026-08-23)

# No docs/rejected_candidates.md row exists for this candidate (expected, per §8's no-registry convention)
$ grep -i "orbpos" docs/rejected_candidates.md
[no output — OK, none, as expected]

# ops/instruments/MNQ.md next open slot re-verified at closure time, not trusted from the pre-reg's draft-time guess
$ grep -noE "N[0-9]+" ops/instruments/MNQ.md | sort -t N -k2 -n -u | tail -3
109:N17
110:N18
111:N19
[confirms N19 is the current tail as of 2026-08-23 — N20 is the correct next slot, matching the
 pre-registration's own draft-time guess, re-verified rather than trusted per §9's instruction]
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure authored. Phase 1–4 (pull, build, independent second implementation, cross-implementation comparison, verdict assertion) run same session as the pre-registration and its operator GO, under §8's K=0/$0 no-separate-spend-gate posture. `FALSIFIED` recorded — third distinct candidate mechanism refuted against the 2021-09-28 break. `ops/instruments/MNQ.md` N20 append drafted here and in `RESULTS.md`; **not yet applied to the ledger file — left as a separate, reviewable step**, per this task's own instruction (same posture as MNQTAPE-1's unapplied closing bookkeeping). | Claude Code (Sonnet 5), operator GO |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md
grep -c "Fired?" docs/briefs/closures/Q-ORBPOS-1-closure-falsified.md
```
