# ADR 2026-08-16 — AMBIGUOUS-HOLD counts toward null-run thresholds

**Status:** `Accepted` — governance-holes closing pass (operator direction: "close the governance holes that hide the drought"); drafted and Rule-0-verified by Claude Code, tightening-only, $0/K=0
**Decision date:** 2026-08-16
**Authors:** Joshua (direction, task start) + Claude Code (Rule-0 recon, drafting)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md) (the exposed lane, patched by this ADR) · [`2026-07-15-external-mechanism-harvest-intake.md`](2026-07-15-external-mechanism-harvest-intake.md) (§4 verdict-vocabulary gap, patched by this ADR) · [`2026-08-15-no-counterparty-statistical-sourcing-channel.md`](2026-08-15-no-counterparty-statistical-sourcing-channel.md) (sibling defect shape, already patched twice for pre-G0 kills / K-cap — this ADR closes the analogous AMBIGUOUS-HOLD gap) · [`docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md`](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) (the worked instance that surfaced this gap) · `docs/adr/2026-08-08-adr-ceremony-tiering.md` (tier test — this fires limb 4, new doctrine)
**Layer:** methodology (research rules of evidence / counting doctrine only). No strategy/risk-control parameter, allocation, `dd_protection` constant, or Pine source touched. **$0 / K=0.** **Tier:** FULL (ceremony-tiering limb 4 — creates a new counting convention binding future lane/channel specs).

---

## §0 — Rule 0 reads (production/methodology-source verification)

Files read in full before drafting (anchors as of 2026-08-16):

- `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` — `b2e3eec` (2026-08-13). Step 6: "**Lane stop-rule:** 3 consecutive FALSIFIED mechanisms on this universe → a lane-review packet to the operator (SNAG discipline), never a 4th campaign by default." Counts only the literal `FALSIFIED` disposition.
- `docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md` — `b2e3eec` (2026-08-13). Confirms by direct evidence that the stop-rule above did **not** fire across CON-2 → CON-5 (four consecutive `AMBIGUOUS-HOLD` closures, 2026-08-10 → 2026-08-12): "Lane FALSIFIED counter **unchanged at 1/3**." The operator instead cited an informal, unshipped tally ("8 consecutive zero-yield closes... against SNAG anchor 3") to elect a manual STOP.
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` — `5563cf4` (2026-08-10). §4 verdict vocabulary (L91): "**RESOLVED** if ≥1 of the first two [intake-class closures] confirms OOS; **FALSIFIED** per the revert trigger [both of the first two close FALSIFIED]; **AMBIGUOUS** if no intake-class campaign closes by 2026-11-08." No branch covers a seed closing `AMBIGUOUS-HOLD` (or any non-RESOLVED/non-FALSIFIED disposition) among the first two — a real, currently-dormant gap (only D5, RESOLVED, has closed to date).
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` — `a8dbadf` (2026-08-15). Both addenda (K-cap; pre-G0-kill-is-not-a-strike) are the direct precedent for this ADR's shape: each names an "absorb unbounded cheap deaths without reaching strike one" defect and closes it with a **tightening-only**, dated addendum, never a silent §2/§4 edit. The pre-G0 addendum explicitly declines to generalize its own fix ("this addendum deliberately does not invent that threshold") — this ADR is the generalization for the AMBIGUOUS-HOLD-specific instance of the same shape, not a re-litigation of the pre-G0 question (which stays open at `STATE.md` queue row 3, untouched here).
- `lab/archive/approach_scoreboard_2026-08/PREREG.md` — `b2e3eec` (2026-08-13). F4 ("Streak + yield rules," L97–106): "WATCH at consecutive zero-yield streak ≥ 3... LEVEL-CHANGE-RECOMMENDED at streak ≥ 6... A close resets the streak ONLY if it yielded an admitted candidate... `AMBIGUOUS-HOLD` counts as zero-yield (design §12 item 4 — held is not yielded). VOID / NULL / SCREEN-FAIL / INTAKE-DRY / OPERATOR-STOPPED / ABORT count as zero-yield." This is the exact definition this ADR promotes — drafted once, correctly, but never ratified as standing doctrine because its host investigation (Q-SCORE-1) closed FALSIFIED on an unrelated axis before the runner shipped.
- `docs/briefs/closures/Q-SCORE-1-closure-falsified.md` — `b2e3eec` (2026-08-13). Confirms F4 never went live: "Live effect: none — report-only; no lane closed; no runner shipped" (L8), and its own §3 disclaims licensing "closing any research lane by streak arithmetic" (L29) — i.e. F4's *definition* is sound and citable, but its *host investigation* conferred no authority to bind future lanes. This ADR supplies that authority directly, on F4's merits, rather than by inheritance from a failed campaign.
- `docs/rejected_candidates.md` — `50c3a1c` (2026-08-14). Scope line: admits entries only at closure "`FALSIFIED` on strategy grounds, or... `SNAG`-budget-exhaustion grounds" — confirmed to carry no `AMBIGUOUS-HOLD` token anywhere in the file. Named in §6 as a known adjacent gap this ADR does **not** close (out of scope — see Forbidden move 4).
- Repo-wide sweep for `"consecutive FALSIFIED"` / `"lane stop-rule"` / `"SNAG discipline"` (2026-08-16, this session) found exactly **one** currently-instantiated consecutive-counting stop-rule mechanism in the repo: the dense-1m lane spec above. No other lane/channel spec currently carries this shape, so §7's mechanical scope is complete as enumerated, not a partial sweep.

---

## §1 — Context

The 2026-08-16 governance-holes diagnostic found that `AMBIGUOUS-HOLD` closures — an investigation reaching a non-promotable, inconclusive disposition rather than an outright falsification — are invisible to every named consecutive/counting falsifier mechanism in the repo except one drafted-and-abandoned design (F4, above). This is not hypothetical: the dense-1m entry-mechanism lane's own stop-rule (step 6 of its spec) exists specifically to stop indefinite iteration on a dry domain, and **four consecutive `AMBIGUOUS-HOLD` closures (Q-TNEC-CON-2 through CON-5, 2026-08-10 → 2026-08-12) ran past it without moving the counter at all** — the closure record for CON-5 states the FALSIFIED counter stood at 1/3 throughout. The lane only stopped because an operator, in-session, manually noticed the pattern and cited an informal tally that is not itself a binding gate.

This is the same defect shape this repo has already named and patched twice, in the adjacent no-counterparty channel ADR: an "absorb unbounded cheap deaths without reaching strike one" hole, first for battery-closure (closed by defining death at *any* named stage as a strike) and again for pre-G0 kills (closed by mandatory count-and-disclose, tightening-only). Both of those fixes required the death to be FALSIFIED-adjacent. Neither reaches a candidate or campaign that closes `AMBIGUOUS-HOLD` — inconclusive, not falsified — even though the dense-1m lane's own record shows this is the *dominant* closure shape in practice (four of the five `AMBIGUOUS-HOLD` closures on record, across every lane in the repo, sit in this one lane).

**Decision driver (one sentence):** a mechanical fix already exists, drafted correctly once (F4) but stranded inside a failed, unrelated investigation with no authority to bind anything — ratifying it directly, on its own merits, closes an already-materialized gap rather than a theoretical one.

---

## §2 — Decision

**Decision:** every named consecutive-closure / streak-counting falsifier or stop-rule mechanism in this repo (a "counting mechanism") counts a closure disposition of `AMBIGUOUS-HOLD` — and, following F4's frozen definition verbatim, the broader **zero-yield disposition class** (`AMBIGUOUS-HOLD`, `VOID`, `NULL`, `SCREEN-FAIL`, `INTAKE-DRY`, `OPERATOR-STOPPED`, `ABORT`, and a capability-only `RESOLVED` that yields no candidate) — **identically to a `FALSIFIED` closure**, for the sole purpose of advancing that counting mechanism's streak. A closure resets the streak only if it yields an admitted candidate; a capability-only `RESOLVED` does not reset it. This applies **unless a specific ADR names an explicit carve-out for that mechanism** — silence in an existing mechanism's own text is not such a carve-out, and is not a reason to treat it as excluding zero-yield dispositions by design.

**This is a counting rule, not a strike-severity rule.** It governs only mechanisms that already count *something* toward a review/pause trigger (lane stop-rules, seed-admission revert triggers). It does **not** make `AMBIGUOUS-HOLD` a `FALSIFIED`-equivalent for any programme-level, date-boxed hard falsifier (e.g. the prop-portfolio §4 "≥1 candidate clears bust ceiling by 2026-11-08" existence test, or the no-counterparty channel's own §4) — those are binary existence checks at a hard date, not streak counters, and adding intermediate AMBIGUOUS-HOLD accounting to them is out of scope (see Forbidden move 1 and §3).

**Immediate mechanical effect (§7 below), the two currently-instantiated mechanisms this repo sweep found:**
1. `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` step 6 — the lane stop-rule now counts `FALSIFIED`-or-zero-yield identically.
2. `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` §4 — the verdict vocabulary gains an explicit fourth branch covering a first-two-seeds closure that is neither RESOLVED, both-FALSIFIED, nor zero-closures.

**Effective:** immediately upon acceptance.
**Scope:** every counting mechanism in the repo, present and future, unless expressly carved out by its own governing ADR/spec.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — count only `FALSIFIED`.** | Already demonstrated to fail: four consecutive `AMBIGUOUS-HOLD` closures ran through the one live mechanical counter in the repo without moving it (§0/§1). The lane stop-rule's entire purpose — stopping indefinite iteration without depending on an operator's memory — is defeated if its counter is blind to the majority of that lane's own closure shapes. |
| **Make `AMBIGUOUS-HOLD` a full `FALSIFIED`-equivalent strike at every level, including programme-level hard falsifiers (§4-style existence checks).** | This is the mirror-image defect the no-counterparty channel ADR's pre-G0 addendum already named and rejected: firing a falsifier on evidence that does not actually bear on its hypothesis. An `AMBIGUOUS-HOLD` closure means "inconclusive," not "the hypothesis is false" — collapsing the two at the programme level would fire an existence-test falsifier on the wrong evidence class. Scoped out explicitly (§2, Forbidden move 1). |
| **Ratify F4 wholesale, including its narrative framing and its host investigation's apparatus (WATCH/LEVEL-CHANGE-RECOMMENDED verdict labels, the specific streak-≥6 second threshold).** | Over-scope. F4's *definition* of the zero-yield disposition set is sound and worth promoting on its own merits; its host investigation (Q-SCORE-1) closed FALSIFIED on an unrelated axis (closure-artifact assignability, 69.8% < 80% bar) and explicitly disclaims licensing any lane-closing authority. Inheriting the whole apparatus from a failed campaign would smuggle in unreviewed machinery under borrowed authority. This ADR extracts only the frozen zero-yield definition and reattaches it directly to the one mechanism that already exists and already needs it (the dense-1m lane's own stop-rule threshold, ≥3), leaving WATCH/LEVEL-CHANGE-RECOMMENDED as F4's own unadopted vocabulary. |
| **Do nothing further — rely on operator vigilance, as happened at CON-5.** | The vigilance already happened once, informally, and it worked — but a lane stop-rule exists specifically so that outcome does not depend on an operator happening to notice and hand-tally a narrative count every time. Formalizing what already had to be done manually is the cheaper, more reliable fix. |

---

## §4 — Falsifier (revert trigger)

**H:** treating the zero-yield disposition class as equivalent to `FALSIFIED` for streak-counting purposes correctly identifies lanes/channels that should pause for operator review, without triggering premature reviews on lanes that are still productively iterating.

**Revert trigger:** across the first 5 lane-review packets fired under this rule (counting the dense-1m lane's own retroactive read — see §6), if a **majority** (≥3 of 5) are, upon operator review, judged to have fired on a lane that was still worth continuing *as configured* (i.e. the operator's disposition is "continue, no change" rather than "STOP / redirect / re-scope"), the streak threshold (currently ≥3, inherited from F4) is miscalibrated for this counting rule specifically — not a reason to revert the counting *principle*.

**Revert action:** if the trigger fires, author a superseding ADR (`Supersedes: 2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md in part — streak threshold`) that widens the threshold (e.g. ≥4 or ≥5) rather than reverting to FALSIFIED-only counting. Reverting the counting principle itself would require separately demonstrating that zero-yield closures are *not* informative about lane dryness, which the worked CON-2→CON-5 instance already refutes on its face (four genuinely inconclusive closures in the same narrow domain is itself the signal a stop-rule exists to catch).

**Trigger check schedule:** at each quarterly programme audit (next: 2026-11-08), tally lane-review packets fired under this rule since the prior audit and their dispositions.

---

## §5 — Forbidden moves (under this ADR)

- **Treating `AMBIGUOUS-HOLD` as a `FALSIFIED`-equivalent strike for any programme-level, date-boxed existence falsifier** (prop-portfolio §4, the no-counterparty channel §4, or any future one shaped like them). Those are binary checks at a hard date, not streak counters; this ADR governs streak counters only. Ruled out in §3 as the mirror-image defect.
- **Silently loosening a stop-rule threshold to avoid triggering a review packet.** This ADR is tightening-only; any future widening of a threshold must cite the §4 revert trigger and land as a superseding ADR, never an in-place edit (Known Trap #12).
- **Reclassifying a genuine `AMBIGUOUS-HOLD` closure under a different disposition token specifically to dodge the counter.** Same-shape gaming as the no-counterparty ADR's own Forbidden move ("re-classifying a battery-stage death as pre-G0 to dodge a strike") — the boundary is the closure's own honest disposition, not a relabeling exercise.
- **Treating this ADR as also answering the still-open "consecutive pre-G0-kill threshold" question** (`STATE.md` queue row 3, the no-counterparty channel's own explicitly-flagged, deliberately-uncovered item). That is a different disposition class (pre-`register_search open` kills, which are not battery-closures at all) and stays open, untouched, exactly as that ADR left it.
- **Backdating this rule to reopen or re-litigate any closure that predates 2026-08-16** as if the rule had been binding at the time. It is forward-only; the CON-2→CON-5 sequence is cited as evidence for why the rule is needed, not reopened for a new disposition.

---

## §6 — Consequences

**Positive consequences:**
- Closes an already-materialized gap: a lane stop-rule that exists specifically to catch indefinite dry iteration now actually catches the dominant closure shape it was blind to.
- Reuses a definition the repo already drafted correctly (F4) instead of re-deriving one, and gives it standing authority on its own merits rather than by inheritance from a failed host investigation.
- Retroactive read (informational only, not a reopening): applied to the dense-1m lane's own history, this rule would have fired the lane-review packet after CON-4 (the third consecutive `AMBIGUOUS-HOLD`, following CON-1's FALSIFIED reset) — one candidate earlier than the operator's own manual CON-5 intervention. Named here as calibration evidence for §4, not as a claim that CON-5 was run in error.

**Negative consequences (real cost, not theatrical):**
- Lane-review packets will fire more often — a genuinely inconclusive but still-plausible research direction can now trigger a pause after 3 non-yields even if none was individually damning. This is the accepted tradeoff (§3); the §4 revert trigger exists to catch miscalibration if it proves too aggressive in practice.
- Authors must now track zero-yield streaks, not just FALSIFIED streaks, when working a lane — marginal bookkeeping overhead per closure.

**Risks (probabilistic, distinct from costs):**
- A lane-review packet is a pause for operator attention, not a kill — the risk is operator-attention cost, not lost research, if the threshold proves too sensitive. Mitigated by the §4 revert trigger and the quarterly check schedule.

**Downstream artifacts that need updating (§7 below):**
- `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` — reader-intercept banner added (matching the file's own established self-correction convention from 2026-08-10), not an in-place rewrite of step 6.
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` — dated addendum appended below the header region (matching the no-counterparty ADR's own precedent for tightening-only extensions), adding the missing §4 verdict branch.
- `STATE.md` — one decision-index line.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified current at implementation time (this session, 2026-08-16).
- **Phase 1** —
  - Add a reader-intercept banner to `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` (top of file, below the existing 2026-08-10 banner), stating the step-6 stop-rule now counts the zero-yield class identically to FALSIFIED, citing this ADR.
  - Append a dated addendum section to `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` (below its header region, alongside its existing Change-history table), adding the missing §4 verdict branch for a first-two-seeds closure that is neither RESOLVED, both-FALSIFIED, nor zero-closures.
- **Phase 2** — grep-sweep (Known Trap #7): (i) no predecessor is superseded, so no stale-reference sweep applies; (ii) repo-wide search for other consecutive-FALSIFIED-shaped counting mechanisms, executed in §0 above — found none beyond the two patched here. A future lane/channel spec that introduces a new consecutive-counting stop-rule inherits this ADR's rule by default (§2 scope), with no further mechanical edit owed here.
- **Phase 3** — verification block below executes; ADR status `Accepted` on landing (governance-hygiene, $0/K=0, operator direction already given via task start).

---

## §10 — Audit hooks (runnable)

```bash
# Confirm the dense1m lane banner landed and cites this ADR
grep -n "2026-08-16-ambiguous-hold-counts" docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md

# Confirm the harvest-intake addendum landed
grep -n "Addendum 2026-08-16" docs/adr/2026-07-15-external-mechanism-harvest-intake.md

# Retroactive-read check (§6): CON-4 is the 3rd consecutive AMBIGUOUS-HOLD after CON-1's FALSIFIED reset
grep -l "AMBIGUOUS-HOLD" docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md docs/briefs/closures/Q-TNEC-CON-3-closure-ambiguous-hold.md docs/briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md

# §4 trigger check — tally lane-review packets fired under this rule since acceptance (manual read at each quarterly audit)
grep -rln "lane-review packet" docs/notes/ docs/briefs/closures/ 2>/dev/null

# No scope creep into programme-level existence falsifiers (Forbidden move 1)
grep -n "AMBIGUOUS-HOLD" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md
# Expected: no edits to those files' own §4 text from this ADR

# Pre-G0-kill threshold (STATE.md queue row 3) stays untouched/open — Forbidden move 4
grep -n "consecutive-pre-G0-kill threshold" STATE.md
# Expected: still present, still UNCOVERED — this ADR does not discharge it

# Quarterly trigger reminder
# Next check due: 2026-11-08
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python "C:\Users\joshu\.claude\skills\brief-authoring\scripts\check_brief.py" docs/adr/2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md --type adr
# Expected: all 6 checks PASS

python scripts/check_adr_graph.py --regenerate-index
python scripts/check_adr_graph.py
# Expected: exit 0

# Production-source verification (§0 anchors)
git log -1 --format='%h %cs' -- docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md          # b2e3eec 2026-08-13
git log -1 --format='%h %cs' -- docs/adr/2026-07-15-external-mechanism-harvest-intake.md            # 5563cf4 2026-08-10
git log -1 --format='%h %cs' -- docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md # a8dbadf 2026-08-15

# Downstream artifact update verification
grep -n "2026-08-16-ambiguous-hold-counts" docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md docs/adr/2026-07-15-external-mechanism-harvest-intake.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-16 | Initial authoring — closes the AMBIGUOUS-HOLD falsifier-counting gap named in the 2026-08-16 governance-holes diagnostic; ratifies F4's frozen zero-yield definition as standing doctrine; patches the dense-1m lane stop-rule and the harvest-intake §4 verdict vocabulary | Joshua (direction, task start) + Claude Code (draft) |
