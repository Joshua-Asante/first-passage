# ADR 2026-08-14 — MSL yield-falsifier survival limb (G0-to-survivor blind spot)

**Status:** `Accepted` — operator election 2026-08-14
**Decision date:** 2026-08-14
**Supersedes:** none — addition only. Amends [`docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md`](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) Gate line and [`docs/briefs/programs/2026-08-12-msl-program-plan.md`](../briefs/programs/2026-08-12-msl-program-plan.md) §7 by **addition only**; the existing `FALSIFIED(process)` and `FALSIFIED(yield)` clauses (6 consecutive pre-G0 deaths across ≥2 families / 12 calendar weeks zero G0) are unchanged and continue to apply independently. The charter/plan edit lands in the same commit as this acceptance.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** full (ceremony-tiering limb 4 fires — this creates a new falsifier threshold, binding doctrine)
**Authors:** Claude Code (drafting session, programme-audit dispatch 2026-08-14) — accepted by operator election 2026-08-14 (same-day, separate follow-on session)
**Related:** [MSL charter](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) · [MSL program plan §7](../briefs/programs/2026-08-12-msl-program-plan.md) · [this session's audit note](../notes/audits/programme-audit/2026-08-14-msl-methodology-audit.md) §3 Q1/Q7 (evidence base) · [MSL C3-K2 dual-axis revive ADR](2026-08-13-msl-c3-k2-dual-axis-revive.md) · [MSL slate-2 design-box ADR](2026-08-13-msl-slate-2-design-box.md) (header/structure template) · [ceremony tiering](2026-08-08-adr-ceremony-tiering.md)
**Layer:** meta (MSL methodology governance). $0 · K=0. No `core/`, Pine, allocation, `dd_protection`, rail, or K ledger touched; nothing armed; no candidate admitted or killed by this ADR itself.

## §0 — Reads (verified this session)

[MSL charter Gate line](../spec/2026-08-12-msl-manual-sourcing-loop-charter.md) @ `8290b89` 2026-08-13 (quoted verbatim in §2 below) · [plan §6 claim manifest + §7 stop rules](../briefs/programs/2026-08-12-msl-program-plan.md) @ `eb1f7c7` 2026-08-14 · all seven MSL closures (C2/C3/C3-K2/C1/S2A/S2B/S7) + both notices (slate-3, WHO-track) — full list and anchors in [this session's audit note](../notes/audits/programme-audit/2026-08-14-msl-methodology-audit.md) §0.

**The gap, restated from the audit's Q7 finding:** the charter's yield falsifier has two limbs — pre-G0 death count and calendar weeks since the last G0 freeze — and both are blind to what has actually happened to MSL to date: **4 of 4 G0 freezes (100%) have died at an under-specified "explore" IS-score stage** (charter-licensed by cross-reference via R-REQSCOPE's "G0/explore-confirm lane discipline," but not one of the charter's 8 numbered steps and carrying no gate criteria of its own) **, with zero Pine files ever authored and zero survivor-MC computations ever run.** The pre-G0 tally sits at 2/6 (C3, S2B — comfortably under the trigger); the weeks-since-G0 clock has never approached 12 because G0 froze four times in the first two days. A channel could run this exact pattern indefinitely — clear G0 often enough to keep the calendar clock cold, kill everything downstream, and never once trip the existing falsifier.

## §1 — Context

MSL's charter defines two kill classes: **pre-G0 kill** (a step 2–4 FAIL) and **scored kill** (a step 8 FAIL — i.e. after Pine is authored, TV-backtested, and survivor-MC'd). In observed practice, all six scored MSL cards to date died at neither of the charter's own named classes cleanly: they cleared Stage-1 and froze G0 (so they are not pre-G0 kills), but they died at an "explore" stage that precedes Pine (step 6) — meaning they are not step-8 scored kills either, since step 8 has never once executed. The charter's yield falsifier was written to catch two specific failure shapes — a channel that can't even clear its cheap pre-registration screens (pre-G0 death spiral), and a channel that has simply stopped generating cards at all (calendar-idle) — and it catches both of those correctly. It was not written to catch a **third** shape: a channel that generates cards, clears G0 cleanly and honestly (Stage-1 PASS, B4 GO paid, PREREG frozen — all real, all disclosed), and then reliably dies one stage later, never converting a single G0 into a Pine-authored, TV-tested, MC-scored candidate. That third shape is exactly MSL's observed history.

## §2 — Decision

**Add a third falsifier limb to the charter's Gate line — `FALSIFIED(yield-conversion)` — with a two-rung structure mirroring the existing plan §7 ladder (soft Board-review rung below a hard FALSIFIED rung, the same relationship the existing "3 Stage-1 deaths → Board review" rung already has to the existing yield clause):**

**Rung A — WATCH (soft, non-terminal):** if **6 consecutive G0 freezes** occur with **zero cards reaching step 6 (Pine authored)**, this fires a **mandatory Board review of the explore-stage screen calibration** — parallel in form and severity to the plan's existing "Three Stage-1 deaths without any G0 ⇒ Board review of the slate-generation method... not an automatic stop." The review's scope is specifically whether the "explore" IS-score gate (session-block bootstrap CI / DELETE-FLIP, computed pre-Pine on historical panel data) is calibrated correctly, or whether it is killing candidates that would have survived a full Pine/TV/MC pass. This rung does **not** close the channel; it forces an explicit look, the same way the 3-Stage-1-death rung does not itself stop MSL.

**Rung B — FALSIFIED (hard, terminal, same consequence as the existing yield clause — channel closes pending a superseding ADR):** fires on whichever comes first:
- **(i)** **10 consecutive G0 freezes** occur with **zero TNEC-1 survivors** (a candidate that reached step 8, cleared survivor MC, and entered TNEC-1 intake), or
- **(ii)** **8 calendar weeks** elapse from MSL's first G0 freeze (2026-08-12) with **zero TNEC-1 survivors**, **given at least 4 G0 freezes have occurred** in that window.

The `≥4 G0 freezes` guard on clause (ii) is deliberate: it prevents the calendar clause from firing on a channel that is simply WHO-starved (few G0s, the existing pre-G0/12-week yield clause already covers that failure mode) rather than one that is G0-rich but conversion-dead (many G0s, none converting) — the specific gap this ADR targets.

**Reachability check on the numbers (not arbitrary):** MSL's observed rate is 4 G0 freezes in 2 calendar days, currently 4/4 (100%) dying pre-Pine. Rung A's threshold of 6 is deliberately close to the *already-observed* 4 — a real test that could fire soon if the pattern holds even loosely, not a number set so high it can never bite. Rung B(i)'s threshold of 10 gives meaningful headroom above Rung A so the soft review has a chance to change something before the hard trigger; Rung B(ii)'s 8-week calendar clause lands at approximately 2026-10-07 — about four weeks before the TNEC-1 `FALSIFIED` hard clock (2026-11-08) — so the survival-limb has a chance to force a Board review and correction *before* the channel simply runs the TNEC clock out silently with a live-looking-but-actually-dead pipeline.

## §3 — Alternatives considered

| Alternative | Why not chosen |
|---|---|
| Hard FALSIFIED on the same threshold used for the existing pre-G0 clause (6 consecutive), no soft rung | Rejected — the failure mode here is more diagnostically ambiguous than pre-G0 death (could be a genuinely dead instrument-story space, cheap kills being "the win" per S6, *or* a miscalibrated explore-stage statistical test; an instant hard-close on the first plausible reading of a 6-count risks foreclosing the channel on a screen-calibration bug rather than a real absence of edge). A two-rung ladder mirrors the plan's own existing precedent (3-Stage-1-death soft rung under the 6-pre-G0 hard rung) and lets the Board correct course before closing. |
| Count only "Pine authored" as the survival bar (no MC/TNEC requirement) | Rejected — Pine-authored is a much lower, cheaper bar than a genuine survivor; using it as the *hard* FALSIFIED trigger would let a channel game the limb by authoring Pine for a candidate everyone already expects to fail TV, without ever producing anything TNEC-1 could use. Pine-authored is the right bar for the *soft* Rung A (it is diagnostic of the explore-stage question specifically), but the *hard* Rung B needs the real bar: a TNEC-1 survivor, matching the charter's own step-8 language ("Survivor MC is the verdict, not TV net/PF"). |
| No calendar clause, count-only | Rejected — mirrors a real gap the existing yield clause already avoids (it pairs a count limb with a calendar limb precisely so a channel cannot game either dimension alone). A pure count-only Rung B could in principle sit at 9/10 G0s-without-survivor for months without firing if G0s are generated slowly; the calendar clause closes that. |
| Set the calendar clause to land exactly at the TNEC-1 hard clock (2026-11-08) | Rejected — that would make this limb redundant with the TNEC-1 FALSIFIED clause itself (no early warning, no time for a Board correction before the channel closes anyway). Landing ~4 weeks earlier (8 weeks from first G0, ≈2026-10-07) preserves a genuine early-warning function. |

## §4 — Falsifier / revert (for this ADR's own claim)

**H:** after acceptance, Rung A and Rung B fire exactly as specified above — mechanically, on the stated counts/dates — and neither rung is reinterpreted after the fact to avoid firing (the same discipline this audit's Q7 found held for the existing yield clause).

**H is falsified — and this decision reverts (superseding ADR, never an in-place edit) — if any limb fires:**
- **Threshold-softening limb:** a future session reads "6 consecutive G0 freezes" as "6 consecutive G0 freezes in the same instrument family" or otherwise narrows the count without a superseding ADR.
- **Silent-non-fire limb:** Rung A or B's stated condition is mechanically true and no Board review / no channel closure follows within the same session that discovers it.
- **Double-count limb:** a G0 freeze that is later revived under the registry re-proposal bar (the C3→C3-K2 pattern) is counted twice toward Rung A/B without an explicit accounting note (each *card* — not each *G0 event* — should count once toward these limbs, matching how the existing Stage-1-deaths counter already treats C3-K2 as continuing C3's slot rather than adding a fresh count).

**Trigger check schedule:** at each MSL B7 weekly review and at every G0 freeze (the plan's existing counter-update discipline).

## §5 — Forbidden moves (under this ADR, if accepted)

- Reading Rung A's mandatory review as license to loosen the explore-stage statistical test (session-block CI / DELETE-FLIP) without independent justification — the review may conclude the test is miscalibrated, but that conclusion needs its own evidence, not just the fact that the review was triggered.
- Treating a Pine-authored-but-TV-rejected candidate as satisfying Rung B — Rung B requires a TNEC-1 survivor, not merely reaching step 6 or step 7.
- Resetting the Rung A/B counters by re-founding MSL under a new name — the counters track the *channel's* G0-to-survivor conversion history, not a particular card-naming scheme.
- Citing this ADR's Rung A review as itself a form of relief for a specific dying candidate — the review is about the *screen*, never about admitting the candidate that triggered it.
- Self-accepting this ADR in the same session that drafted it (the drafting session did not do so; acceptance came from a separate follow-on operator-election session, per Change history).

## §6 — Consequences

**Positive:** closes a live, evidence-confirmed blind spot (4/4 G0s dead at explore, 0 Pine ever authored) before the channel could in principle run indefinitely without ever tripping a falsifier; the soft/hard two-rung structure gives the Board a chance to fix a possibly-miscalibrated explore-stage test before the channel is forced to close; the reachability numbers are calibrated off MSL's own observed rate rather than picked arbitrarily.

**Negative:** a third standing counter to maintain alongside the existing Stage-1-deaths counter and the pre-G0/weeks-since-G0 yield counters — more bookkeeping per B7 review. A channel that is genuinely producing honest, well-calibrated cheap kills (which Q3 of the audit found MSL has been doing) could still trip Rung A on bad luck alone if the true edge rate in the remaining instrument-story space is simply low; Rung A's soft, review-only consequence is the deliberate mitigation for that risk, not a full protection against it.

**Risks:** Rung B(ii)'s 8-week clause could fire while a genuinely promising candidate is mid-TV-backtest, forcing a Board review at an awkward moment (mitigation: Rung B requires *zero* survivors, not zero candidates-in-flight — a card actively at step 7 is not itself a violation, and the Board review is not an automatic close, it is the trigger for `FALSIFIED(yield-conversion)`, which per §2 still requires a superseding ADR to actually close the channel, exactly as the existing `FALSIFIED(yield)` clause does).

## §7 — Implementation (owed on acceptance, not executed by this ADR)

Phase 0 — this ADR drafted and left `Proposed` (this session). Phase 1 (owed, on operator acceptance): edit `docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md` Gate line to add the `FALSIFIED(yield-conversion)` clause quoted in §2; edit `docs/briefs/programs/2026-08-12-msl-program-plan.md` §7 to add the Rung A/B stop rules alongside the existing bullets, and add a "G0-to-Pine conversion" tracking row to §6's claim manifest next to the existing Stage-1-deaths-counter row; regenerate `docs/adr/INDEX.md`; add a `docs/SESSIONS.md` entry. Phase 2 — grep sweep for any place that currently states or implies "MSL's yield falsifier only tracks pre-G0 deaths and calendar weeks" (this audit note is one such place, and should be updated to note the amendment landed, once it does).

## §10 — Audit hooks (runnable)

```bash
# Rung A: has a 6th consecutive G0-freeze-without-Pine occurred since acceptance?
# (count G0-freeze commits per closure; a Pine file under lab/analysis/c1/**/*.pine
#  tied to any MSL card resets the consecutive counter to 0)
git log --oneline --since=<acceptance-date> -- docs/briefs/closures 'docs/briefs/handoffs/*msl*' | grep -ci "G0 FROZEN\|G0 freeze"
find lab/analysis/c1 -iname "*.pine" -newer docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md 2>/dev/null

# Rung B(i): 10 consecutive G0 freezes, zero TNEC-1 survivors?
grep -rln "TNEC-1 intake\|TNEC-1 survivor" docs/briefs/closures/MSL-*-closure-*.md 2>/dev/null
# Expected until a survivor lands: no hits

# Rung B(ii): 8 calendar weeks from first G0 (2026-08-12) with <4 G0s => clause does not apply;
# with >=4 G0s and zero survivors => fires on 2026-10-07
date -d 2026-10-07 +%s 2>/dev/null || echo "manual date check: has 2026-10-07 passed?"

# §4 threshold-softening check: has any session narrowed "6 consecutive G0 freezes"
# to a sub-scope (e.g. "same instrument family") without a superseding ADR?
grep -rn "consecutive G0" docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md docs/briefs/programs/2026-08-12-msl-program-plan.md 2>/dev/null

# §4 double-count check: does a revived card (C3->C3-K2 pattern) count once or twice
# toward the Rung A/B tallies in the plan's §6 claim manifest?
grep -n "Stage-1 deaths\|G0-to-Pine\|G0 freeze" docs/briefs/programs/2026-08-12-msl-program-plan.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md --type adr
python scripts/check_adr_graph.py
# Confirm this ADR's acceptance status
grep -n "^\*\*Status:\*\*" docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md
# Expected: Accepted — operator election 2026-08-14
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-14 | Drafted as Proposed, per programme-audit dispatch; operator election owed | Claude Code |
| 2026-08-14 | Accepted — operator election, separate follow-on session; charter Gate line + plan §6/§7 amended in the same commit | Joshua |
