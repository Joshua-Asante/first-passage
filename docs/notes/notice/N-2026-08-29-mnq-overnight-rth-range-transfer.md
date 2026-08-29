# Notice — MNQ overnight-range → same-day RTH-range transfer clears the D5 stage-1 $0 falsifier decisively

**Notice ID:** N-2026-08-29-mnq-overnight-rth-range-transfer
**Observed:** 2026-08-29
**Author:** Claude Code
**Source:** own statistical computation this session, candidate 2 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `OPEN` — routing decision below is GRADUATE; no `Q-*` file opened yet (owed to the next session's D-S-A pre-Q gate, per this session's scope)
**Lives in:** `docs/notes/notice/N-2026-08-29-mnq-overnight-rth-range-transfer.md`

---

## §0 — Source anchor

- **Source:** [`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py) → `candidate2_results.json`; consolidated in [`RESULTS.md`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/RESULTS.md) §Candidate 2.
- **Observed at:** 2026-08-29, this session, on `core/data/bar_data/MNQ_M15.csv`.
- **K:** [`discovery_manifests/mnq_dailygeom_notice_20260829.json`](../../../discovery_manifests/mnq_dailygeom_notice_20260829.json), `--lane blind`, K=5, closed p≈0.00025 for this cell (block-bootstrap, see §1).
- **Governing spec, read in full before running anything:** `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4 (D5).

---

## §1 — The observation

**This is not the candidate the handoff framed it as, and that distinction is the load-bearing finding.** The handoff described this as reusing "the same corrected-battery null as #1" (candidate 1, daily TR self-persistence). It does not. Overnight range and RTH range are two *different* series measured on the *same* trading day — structurally identical to the shape the frozen battery spec's own §4 (D5) names **"S2 (overnight→day-session transmission)"** and explicitly pauses: *"the S1 null does NOT port — bias and outcome are different series sharing a slow common vol state; joint surrogation preserves the effect under test, independent surrogation deletes the mundane common-state confound."* D5 requires a stage-1 **$0 cheap falsifier** before any battery: *does overnight-state conditioning beat matched day-session-history conditioning (bias′ = 1{DS_{d−1} ≥ P80 trailing}) on the same days? No increment → S2 dies for $0.*

Ran exactly that. RTH range's own trailing-median outcome, conditioned on overnight range (bias) vs. yesterday's own RTH range (bias′, matched day-history), stratified on bias′:

| bias′ stratum | P(y=1 \| overnight-bias=1) | P(y=1 \| overnight-bias=0) | incremental lift |
|---|---|---|---|
| bias′=0 (n=213/940) | 0.9296 | 0.3521 | **+57.7pp** |
| bias′=1 (n=126/208) | 0.9206 | 0.5337 | **+38.7pp** |

Naive marginals: P(y=1\|overnight-bias=1)=0.9263 (n=339) vs. unconditional base rate 0.5087. Block-bootstrap (day-blocks, block=20, 4000 draws) on the minimum stratified lift: mean 0.386, CI [0.300, 0.473], p(lift≤0) < 0.00025. Same-day raw Spearman correlation between overnight range and RTH range is 0.77 — high, as expected for two magnitude series sharing a vol regime — but the stratified design shows overnight range carries **large incremental** information beyond what yesterday's own RTH-range level already tells you, which is exactly the D5 "increment" test.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** D5's own predicted failure mode for this class is "no increment → dies for $0" (the spec explicitly frames the un-pause as a likely dead end, matching S1's own predicted-NULL pattern for GC/CL under the corrected battery). No prior test of this exact class exists anywhere in this repo — MECHANISMS.md has no `overnight-range-transfer` class entry and MNQ.md's DEAD list has nothing matching it (the nearest neighbor, `overnight-range-failed-extension-fade`, is an entry-role fade construct on M2K, unrelated).
- **Delta:** the incremental lift (+39 to +58pp) is an order of magnitude larger than the ~2pp threshold this session used to define "increment exists," and larger in absolute terms than any of the other four candidates' effects this session. It clears D5's stage-1 bar with enormous margin, not marginally.
- **Frequency check:** first instance — this specific class has never been tested on MNQ or any other instrument in this repo.

---

## §3 — Candidate mechanisms (informal)

- **A — genuine same-day volatility-regime persistence, tradeable because overnight resolves before RTH opens.** Whatever drives a session's overall vol level (macro news flow, positioning, an overnight risk event) is often already visible in the overnight segment before the RTH open, making this a legitimately forward-usable conditioner regardless of deeper causal story.
- **B — mechanical/definitional overlap, not a distinct "transfer" mechanism.** Overnight range and RTH range on the same calendar day are both symptoms of the day's realized volatility level — this could be relabeled generic same-day volatility clustering (the same ARCH/GARCH canon grounding as candidate 1) rather than anything specific to the overnight→RTH boundary. The stage-2 joint-surrogation design D5 calls for exists precisely to separate "real, specific transmission" from "both series inherit the same regime."
- **C — could be partly mechanical through the shared reference price at 09:30 ET** (RTH open is priced off wherever overnight left the market) rather than a volatility-transfer claim per se — untested this session.

---

## §4 — Routing decision

**GRADUATE to Pre-Q.** Reason: the D5 stage-1 $0 falsifier this exact spec names as the precondition for proceeding has now run, on real MNQ data, and clears decisively (not a close call — the incremental lift is large in both strata, well-powered, and bootstrap-robust). Per D5 condition (2), an increment exists, which licenses moving to D5 condition (3): a stage-2 joint-surrogation null design, adversarial review, and the slate's operator GO — none of which this Notice-phase session ran or is scoped to run. **Route-1 flag for the next session (raised bar, `index-intraday-ohlcv-directional-timing-2026-07-21`):** this is a **conditioner-role, not entry-role** claim (mirrors candidate 1's own framing) that uses a same-day pre-open informational lever untouched by the mapped price/hold-time/cross-instrument-selection levers — if a future entry construct is built on it, that construct would need its own Route 1/2/3 argument at that time; this notice's own D5-shaped conditioner claim does not by itself need to clear the raised bar.

---

## §5 — If HOLD: re-check trigger

N/A — routed GRADUATE, not HOLD.

---

## §10 — Audit hooks

```bash
# Reproduce the stage-1 $0 falsifier (deterministic, <10s)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py
# Expected: stratum bias'=0 lift ~0.577, stratum bias'=1 lift ~0.387, increment_exists=True

# Confirm the governing D5 text this notice's re-framing rests on
grep -n "S2 (overnight" docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
# Expected: the "S1 null does NOT port" clause and the three un-pause conditions

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-29-mnq-overnight-rth-range-transfer" docs/briefs/Q-*.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-overnight-rth-range-transfer.md --type notice
```
