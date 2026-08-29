# Notice — MNQ unsigned gap magnitude → RTH-range conditioning clears the D5 stage-1 $0 falsifier (smaller than candidate 2)

**Notice ID:** N-2026-08-29-mnq-gap-magnitude-rth-range
**Observed:** 2026-08-29
**Author:** Claude Code
**Source:** own statistical computation this session, candidate 4 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `OPEN` — routing decision below is GRADUATE
**Lives in:** `docs/notes/notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md`

---

## §0 — Source anchor

- **Source:** [`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate4_gap_magnitude.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate4_gap_magnitude.py) → `candidate4_results.json`; consolidated in [`RESULTS.md`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/RESULTS.md) §Candidate 4.
- **Observed at:** 2026-08-29, this session, on `core/data/bar_data/MNQ_M15.csv`.
- **K:** [`discovery_manifests/mnq_dailygeom_notice_20260829.json`](../../../discovery_manifests/mnq_dailygeom_notice_20260829.json), `--lane blind`, K=5, closed p≈0.00225 for this cell (block-bootstrap on the minimum stratified lift).
- **Distinct from:** the already-corroborated-dead gap-fill *fade* direction (Mesfin 2026, T=−0.44…−0.59; also this repo's own `MNQ-SIZEDIV-1` and other DEAD-list rows never touched gap magnitude specifically). This candidate makes no fill/fade claim at all — it is sign-agnostic magnitude only.

---

## §1 — The observation

**Same re-framing this session applied to candidate 2 applies here, and for the identical reason.** Gap magnitude (|RTH open_d − RTH close_{d−1}|) and RTH range are two *different* series on the same trading day, not one series lagged against itself — structurally the same "S2" shape the frozen battery spec's §4 (D5) pauses pending a stage-1 $0 cheap falsifier, not a straightforward reuse of candidate 1's single-series null. The handoff's framing ("same corrected-battery family as #1/#2") is imprecise on this point: it is family-adjacent (a magnitude-conditioning claim) but structurally like #2, not #1.

Ran the identical D5 stage-1 design (bias = elevated gap magnitude; bias′ = matched day-history, yesterday's own RTH range; outcome = today's RTH range elevated vs its own trailing median), stratified on bias′:

| bias′ stratum | P(y=1 \| gap-bias=1) | P(y=1 \| gap-bias=0) | incremental lift |
|---|---|---|---|
| bias′=0 (n=209/944) | 0.5981 | 0.4280 | **+17.0pp** |
| bias′=1 (n=118/216) | 0.7797 | 0.6250 | **+15.5pp** |

Naive marginals look unremarkable on their own (P(y=1\|gap-bias=1)=0.6636 vs P(y=1\|dayhist-bias=1)=0.6796 — gap even looks slightly *worse* than day-history in the pooled comparison) — the stratified design is what surfaces the real, positive, consistent incremental effect the naive comparison masks. Block-bootstrap (day-blocks, block=20, 4000 draws) on the minimum stratified lift: mean 0.137, CI [0.054, 0.212], p(lift≤0) ≈ 0.00225.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** D5's own predicted failure mode is "no increment → dies for $0." The naive marginal comparison alone would have supported that prediction (gap ≈ day-history, no obvious lift) — it is only the stratified design that reveals the naive comparison was itself confounded by bias′ correlating with bias in a way that canceled out in the pooled read.
- **Delta:** +15-17pp incremental lift, smaller than candidate 2's overnight-range effect (+39 to +58pp) but still well above the noise floor (bootstrap CI excludes 0 with real margin) and above the ~2pp threshold used to define "increment exists" this session.
- **Frequency check:** first test of gap MAGNITUDE (as opposed to fill/fade direction) as an RTH-range conditioner on MNQ or any instrument in this repo.

---

## §3 — Candidate mechanisms (informal)

- **A — genuine information content in the size of the overnight jump**, independent of its direction: a large gap (of either sign) reveals something happened overnight that plausibly continues to generate range during RTH.
- **B — gap magnitude is a noisier, single-point-in-time proxy for the same underlying quantity candidate 2 measures more directly** (the full overnight session's realized range). The smaller effect size here relative to candidate 2 is consistent with this — a single jump captures less of the overnight information set than the full overnight range does.
- **C — could still partly reflect the same shared same-day vol-regime confound D5 flags for candidate 2** — untested this session whether gap magnitude's incremental lift survives once candidate 2's overnight-range signal is also controlled for (the two candidates are likely correlated with each other, not just each with day-history).

---

## §4 — Routing decision

**GRADUATE to Pre-Q.** Reason: clears the D5 stage-1 $0 falsifier with real, bootstrap-robust margin — smaller effect than candidate 2, but real and worth a falsifiable H, especially since it may turn out to be either (a) redundant with candidate 2 once jointly tested (mechanism C) or (b) incrementally informative beyond it, which is itself worth knowing before either is built into anything. Per D5, proceeding requires the same stage-2 path as candidate 2: a joint-surrogation null design, adversarial review, and operator GO — not run this session. **Route flag (raised bar, `index-intraday-ohlcv-directional-timing-2026-07-21`):** conditioner-role, same framing as candidates 1/2/3 — does not by itself need to clear the raised bar.

**Suggested sequencing for the next session (not binding, flagged for judgment):** since candidates 2 and 4 are both S2-shaped and plausibly overlapping, consider scoping the D-S-A pre-Q gate to test them jointly (does gap magnitude add anything once overnight range is already in the conditioning set?) rather than as two fully independent Pre-Qs — this is a scoping suggestion, not a decision made here.

---

## §5 — If HOLD: re-check trigger

N/A — routed GRADUATE, not HOLD.

---

## §10 — Audit hooks

```bash
# Reproduce the stage-1 $0 falsifier (deterministic, <10s)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate4_gap_magnitude.py
# Expected: stratum bias'=0 lift ~0.170, stratum bias'=1 lift ~0.155, increment_exists=True

# Confirm this is distinct from the corroborated-dead gap-FADE direction
grep -n "gap-fill" docs/rejected_candidates.md | head -5
# Expected: fade/fill direction claims only, none about unsigned magnitude

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-29-mnq-gap-magnitude-rth-range" docs/briefs/Q-*.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-gap-magnitude-rth-range.md --type notice
```
