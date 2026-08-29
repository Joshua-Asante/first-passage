# Notice — MYM overnight-session range → RTH-range transfer (S2 cheap-falsifier only)

**Notice ID:** N-2026-08-29-mym-overnight-rth-range-transfer
**Observed:** 2026-08-29
**Author:** Joshua | claude.ai
**Source:** backtest CSV (bar panel) — atheoretical mechanism harvest, MYM Phase 2
**Status:** `HELD until 2027-03-01`
**Lives in:** `docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md`

---

## §0 — Source anchor

- **Source:** `core/data/bar_data/MYM_M15.csv` (sha256
  `24e169528f7ea6693b75c71c3195edf6a04f3a26c6b6dff0f2e9c623fd597a58`), split into
  overnight (`[00:00, 09:29]` ET, same trading day) and RTH (`[09:30, 15:59]` ET)
  sub-sessions using the session-boundary convention already pinned on this exact panel
  by `lab/archive/msl_c1_mym_2026-08/construct_lib.py`
  (`RTH_OPEN_MIN`/`RTH_CLOSE_MIN`/`OVERNIGHT_CLOSE_MIN`), not invented here — four MSL
  campaigns (C1, C2, C3, S2B) already use this convention on MYM. Script:
  `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py`.
  Results: `.../c2_c4_results.json` key `candidate2_overnight_range`.
- **Observed at:** 2026-08-29 (this session).

---

## §1 — The observation

**Constraint-audit catch, before running anything (load-bearing to this notice):** the
originating brief framed this candidate as reusable "verbatim" from the corrected
magnitude-persistence battery, the way candidate 1 (session-TR self-persistence) is. On
reading the battery's own frozen spec
(`docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` §4 D5), this
candidate is actually the **PAUSED "S2" construct**, not the un-paused "S1" one:
overnight range and RTH range are *different series measured the same day*, sharing a
slow common volatility-regime state — independent-series IAAFT surrogation (candidate
1's legitimate tool, same series next-period) does **not** delete that confound; only
joint surrogation would, and the spec marks the joint-surrogate design
"UNRESOLVED-NEEDS-DESIGN" (O1). Building that design is out of scope for a Notice-phase
screen, so no full battery was run.

Instead, per the spec's own un-pause precondition (2) — *"S2 reframed INCREMENTAL with a
stage-1 $0 cheap falsifier first — does overnight-state conditioning beat matched
day-session-history conditioning (`bias' = 1{DS_{d-1} ≥ P80 trailing}`) on the same
days? No increment → S2 dies for $0"* — a real-data-only head-to-head was run: does
today's own overnight-range state (top-quintile, strict-prior 60 sessions) predict an
elevated RTH range *better than* yesterday's own RTH-range state already does (the
mundane same-series autocorrelation baseline)? Result: overnight-conditioned
0.7604 (n=313) vs. day-history-conditioned 0.7306 (n=297) on n_common=1,307 matched
sessions — diff **+0.0297**, 95% block-bootstrap CI **[−0.0325, +0.0988]**, p≈0.372.

## §2 — Why it stands out (the N signal)

- **Baseline:** the spec's own precommitted decision rule — no increment beyond the
  mundane comparator kills S2 for $0.
- **Delta:** the observed increment is positive but the CI straddles zero — neither a
  clean pass nor a clean kill under that rule.
- **Frequency check:** first instance; MYM has never been scored on this construct
  (nor has any instrument, per the class's PAUSED status — this is the first time the
  precondition-2 falsifier itself has been run on any instrument for this class).

## §3 — Candidate mechanisms (informal)

- Genuine overnight→RTH information transfer (news/positioning carried into the open)
  distinct from ordinary day-to-day vol persistence — would require the CI to clear 0
  with more data or a tighter design.
- Pure noise around a null increment — equally consistent with the current CI.
- Could also be confounded by the same common-regime state the cheap falsifier is
  specifically designed to screen for, even in this simplified form (the day-history
  comparator only controls for ONE lag of same-series persistence, not the full
  common-state structure a joint surrogate would).

## §4 — Routing decision

**HOLD until 2027-03-01.**

Reason: not a clean kill (per §1's precommitted rule, "no increment" is the only
condition that dies at $0 — an AMBIGUOUS CI is a weaker read than that) but also not a
demonstrated increment worth building the heavier joint-surrogate design for today.
Escalating past this point needs a design (spec condition 3: a joint-surrogate null
passing its own adversarial review) that a Notice-phase screen has no license to
originate, **plus the slate's own operator GO** (condition 4) — neither of which this
session can self-issue. Re-checking after the panel grows narrows the CI's width without
any new design work.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** 2027-03-01 (~6 months / ~125 more sessions of panel growth).
- **Trigger condition:** re-run the identical $0 cheap falsifier on the grown panel; if
  the CI clears 0 (lower bound > 0), candidate 2 GRADUATEs to a Pre-Q scoping the joint-
  surrogate design (condition 3) and routes to the operator for condition-4 GO. Also
  graduates immediately, without waiting for the date, if the operator elects to
  authorize the joint-surrogate design directly (independent of this falsifier's
  outcome).
- **Drop trigger:** CI on the grown panel still straddles 0, or flips to a clean
  NO-INCREMENT (upper bound < 0) — the latter closes S2 on MYM for $0 per the spec's own
  rule.
- **Calendar entry:** none set (no Todoist/Calendar integration invoked this session);
  operator to set if desired.

---

## §10 — Audit hooks

```bash
python lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/c2_c4_increment_falsifiers.py
# Expected: [candidate2_overnight_range] diff=+0.0297  95% CI=[-0.0325,+0.0988]  VERDICT=AMBIGUOUS

# Re-check due: 2027-03-01 -- verify in Calendar / Todoist if the operator sets one
```

---

## Verification

```bash
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/notice/N-2026-08-29-mym-overnight-rth-range-transfer.md --type notice
# Expected: RESULT: well-formed
```
