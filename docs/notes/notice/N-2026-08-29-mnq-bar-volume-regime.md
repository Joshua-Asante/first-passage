# Notice — MNQ M15 bar-volume regime predicts next-bar range (not direction), incremental beyond range's own persistence

**Notice ID:** N-2026-08-29-mnq-bar-volume-regime
**Observed:** 2026-08-29
**Author:** Claude Code
**Source:** own statistical computation this session, candidate 3 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `OPEN` — routing decision below is GRADUATE (range limb only); direction limb is DROP. **Re-verified 2026-08-30** against live `MNQ_M15.csv` — the ToD-indexing fix holds (figures shift up slightly, do not dissolve) and the within-stratum null-calibrated p is now computed (decisive, p=0.00025 both strata) — see the update below, superseding the "pending re-verification" caveat.

**Pre-Q:** [`Q-VOLREGIME-1`](../../briefs/Q-VOLREGIME-1-intraday-bar-volume-regime.md) (opened separately — see that brief's own Authored field), jointly with MYM's own independently-run same-day candidate.
**Lives in:** `docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md`

---

**⚠ Correction, 2026-08-30 (Codex review, PR #210) — the ToD-matched range-outcome
labeling in `candidate3_volume_regime.py` had an indexing bug; the headline
+18.1pp / CI [0.673, 0.695] range-lift figure below is UNVERIFIED pending a
re-run.** The script's `outcome_range_tod` compared the *next* bar's realized
range against the *trigger* bar's own time-of-day-conditioned threshold
(`rng_thresh_tod[:-1]`) instead of the next bar's own slot's threshold
(`rng_thresh_tod[1:]`) — since consecutive M15 bars are almost always in
different ToD slots with very different typical range levels, this reintroduces
exactly the deterministic intraday seasonality confound the ToD-matched design
exists to remove (see §2's own null-validity argument, which this bug silently
undermined). The code fix is committed in the same commit as this correction;
it was **not** re-run in this session's environment (no `MNQ_M15.csv` — see
`Q-VOLREGIME-1`'s own Phase 0.5, a vendor-data-dependent task). Until a fresh
run confirms whether the corrected labeling reproduces, matches direction but
differs in magnitude, or dissolves entirely, **this notice's GRADUATE routing
(§4) and every downstream citation of the +18.1pp/CI figure (MECHANISMS.md,
`Q-VOLREGIME-1`, MNQ.md) should be read as "pending re-verification," not
"confirmed."** The incremental-over-own-range stratification (+20.6pp/+25.6pp)
uses the SAME buggy `outcome_range_tod` variable and is equally unverified. The
direction-limb null (+0.01pp) does not use this variable and is unaffected.

---

## Update, 2026-08-30 — re-verified against live vendor bars; within-stratum null computed

Both open items this notice's own correction named are now resolved:

**Re-run of `candidate3_volume_regime.py` (post-fix) against `MNQ_M15.csv`:** the
corrected ToD-matched range-lift figure **shifts up, does not dissolve**: obs
0.695 vs base 0.504, lift **+19.1pp** (was the unverified +18.1pp), CI
**[0.684, 0.707]** (n_cond=70,545/n_scored=136,020). Direction limb unchanged
(+0.01pp, still null, as expected — it never used the buggy variable).

**New script** [`candidate3_stratified_rerun.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_stratified_rerun.py)
ports `circular_shift_null_p` (same within-stratum circular-shift construction
already used in `candidate24_joint_gate.py` and MYM's own `c3_stratified_rerun.py`,
Codex PR #207 P1/P2) onto MNQ's own bias_hist (trigger bar's own ToD-matched
range state) stratification. Results, on real bars:

- Stratum `bias_hist=0` (own range NOT elevated, n=12,853+54,564=67,417):
  P(y=1|volume=1)=0.4877 vs P(y=1|volume=0)=0.2645 — lift **+22.3pp**,
  circular-shift null-calibrated **p=0.00025**.
- Stratum `bias_hist=1` (own range elevated, n=57,692+10,911=68,603):
  P(y=1|volume=1)=0.7415 vs P(y=1|volume=0)=0.4675 — lift **+27.4pp**,
  circular-shift null-calibrated **p=0.00025**.
- Both figures shift up from the previously-unverified +20.6pp/+25.6pp (same
  direction as the marginal range-lift shift above) — the ToD-indexing fix
  strengthens this finding, it does not weaken or dissolve it.
- Composite (disjunctive, "either stratum") null p = max(per-stratum p's) =
  **0.00025** — both strata individually decisive, so (unlike MYM's gap-magnitude
  analogue, PR #211) the sharp-joint-null-vs-composite-null distinction does not
  change the verdict here: either statistic reads decisive.

**This clears `Q-VOLREGIME-1`'s own Phase 0.5 precondition for MNQ** — the
within-stratum null was the one thing MNQ's own H-VOLREGIME-MNQ was explicitly
gated on (that brief's §4). The range-limb GRADUATE routing below is now
**confirmed, not pending** — struck caveat left visible in the correction above
for the record, but superseded by this update.

---

## §0 — Source anchor

- **Source:** [`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py) → `candidate3_results.json`; consolidated in [`RESULTS.md`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/RESULTS.md) §Candidate 3.
- **Observed at:** 2026-08-29, this session, on `core/data/bar_data/MNQ_M15.csv` (all 141,541 M15 bars).
- **K:** [`discovery_manifests/mnq_dailygeom_notice_20260829.json`](../../../discovery_manifests/mnq_dailygeom_notice_20260829.json), `--lane blind`, K=5, closed p≈0.0005 for this cell (block-bootstrap on the ToD-matched range result, the smaller/survivor sub-test).
- **Prior art:** `python scripts/instrument_profiles.py cell MNQ opening-pressure` and `... order-flow-depth-imbalance` both confirmed `DEAD` on MNQ — neither is this construct (opening-pressure is opening-window-only; order-flow-depth-imbalance is tick-level MBP-10 book size, not plain OHLCV volume). No existing MECHANISMS.md class matches "plain-OHLCV bar-volume regime → next-bar conditioning."

---

## §1 — The observation

Tested two next-bar outcomes conditioned on the trigger bar's volume being above its own trailing-median (ToD-matched to remove the deterministic intraday volume-seasonality confound — see §2):

- **Directional continuation (does the next bar's close-open sign match the trigger bar's?): a clean null.** ToD-matched lift +0.01pp (n≈134,678 scored pairs) — no effect, naive or corrected.
- **Next-bar range elevation: real and large.** Naive pooled: obs 0.803 vs base 0.514, lift +28.9pp — but this is heavily confounded by intraday volume seasonality (see §2). ToD-matched: obs **0.684** vs base 0.503, lift **+18.1pp**, CI [0.673, 0.695] (block-bootstrap, block=96≈1 day, n_cond=70,545/n_scored=136,020).

A follow-up check not in the original framing, run because same-bar Spearman(volume, range)=0.88 raised the obvious question of whether "volume regime" is just relabeling range's own persistence: own-range→own-range persistence (ToD-matched) gives an almost identical point estimate (0.686) to volume→range. But stratifying the volume→range test on the trigger bar's own range state shows volume still adds **+20.6pp** (low-range stratum, n=12,430/54,167) and **+25.6pp** (high-range stratum, n=58,115/11,308) of incremental lift beyond what the trigger bar's own range already tells you.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** no prior test of plain-OHLCV volume regime as a range/direction conditioner exists on MNQ. The nearest DEAD cells (`opening-pressure`, `order-flow-depth-imbalance`) are both confirmed structurally distinct.
- **Delta / null-validity note (this candidate's own required fresh citation, per the futures-anomaly-discovery skill's "fresh batteries need the same check reuse gets" rule):** M15 volume carries a strong deterministic intraday seasonality (U-shape, an RTH-open step) — a naive pooled trailing-median comparison is confounded on both sides of the test, since the 09:30 ET bar is mechanically high-volume and the following 09:45 ET bar mechanically is too, for reasons unrelated to any genuine clustering mechanism. This is the identical confound class that `tod-baseline-range-trigger` (Q-TODVOL-1) was built to avoid on a different construct, and the same fix — a causal reference conditioned on the SAME time-of-day slot — is adopted here as the null-validity design, not borrowed as a battery. The naive-vs-ToD-matched comparison (28.9pp → 18.1pp) makes the seasonality artifact's size directly visible, rather than merely asserted.
- **Frequency check:** first test of this construct on MNQ.

---

## §3 — Candidate mechanisms (informal)

- **A — the same underlying activity/volatility-clustering phenomenon as candidate 1, at finer grain.** Volume clustering and volatility clustering are both well-established ARCH-type stylized facts and are known to co-move (Clark's mixture-of-distributions hypothesis, volume-volatility literature). This candidate may not be a distinct WHO from candidate 1's daily TR persistence — just the same regime-level phenomenon observed at M15 via a different proxy.
- **B — volume genuinely carries information beyond contemporaneous range**, e.g. order-arrival intensity anticipates the NEXT bar's range even when the current bar's own range doesn't fully reflect it (a partial-information story: volume reflects participation/urgency, range reflects realized outcome, and the two decorrelate enough at M15 to matter — supported by the +20-26pp incremental-lift finding).
- **C — could be noise from the specific 60-bar trailing window / P50 threshold choice** — untested at other window/threshold combinations this session (any such retune would be a fresh K-charged axis, not a free look).

---

## §4 — Routing decision

**Split decision by outcome.** Range limb: **GRADUATE to Pre-Q — pending re-verification, 2026-08-30.** Reason (as originally read): real, well-powered (n>130k), CI clearly excludes the base rate, survives both the ToD-seasonality control and the incremental-over-own-range stratification — a construct worth a proper falsifiable H, distinct enough from candidate 1 (finer grain, incremental over range) to justify its own line even though mechanism A above is a live possibility the Pre-Q should confront directly. **This routing rests on the buggy `outcome_range_tod` labeling disclosed above and is not withdrawn, but should not be treated as confirmed until the fixed script is re-run against real bars.** Direction limb: **DROP** (unaffected by the bug — uses a different, unaffected variable). Reason: clean null both naive and ToD-matched, no plausible mechanism surviving, nothing to carry forward.

**Route flag for the range limb (raised bar, `index-intraday-ohlcv-directional-timing-2026-07-21`):** conditioner-role, not entry-role (same framing as candidates 1/2) — does not by itself need to clear the raised bar; an entry construct built on it later would.

---

## §5 — If HOLD: re-check trigger

N/A — routed GRADUATE (range) / DROP (direction), not HOLD.

---

## §10 — Audit hooks

```bash
# Reproduce both outcomes, naive and ToD-matched, against live MNQ_M15.csv (2026-08-30 re-verification)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py
# Expected (CONFIRMED against the corrected code, live bars): dir lift ~0.0001 (ToD-matched);
# range lift ~0.191 (ToD-matched), CI [0.684, 0.707].

# Confirm the indexing fix landed (Codex review, PR #210)
grep -n "rng_bar\[1:\] > rng_thresh_tod\[1:\]" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_volume_regime.py
# Expected: one match (was rng_thresh_tod[:-1] before the fix)

# Reproduce the within-stratum null-calibrated p (2026-08-30, clears Q-VOLREGIME-1 Phase 0.5)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate3_stratified_rerun.py
# Expected: both strata lift +22.3pp/+27.4pp, circular-shift null p=0.00025 each

# Confirm the DEAD-cell distinctness claims this notice rests on
python scripts/instrument_profiles.py cell MNQ opening-pressure
python scripts/instrument_profiles.py cell MNQ order-flow-depth-imbalance
# Expected: both DEAD, both for reasons distinct from this construct (see §0)

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-29-mnq-bar-volume-regime" docs/briefs/Q-*.md
# Expected: Q-VOLREGIME-1-intraday-bar-volume-regime.md (opened 2026-08-30)
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-bar-volume-regime.md --type notice
```
