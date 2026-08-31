# Audit Note — MNQ overnight-window look-ahead defect in `data_lib.py::overnight_ohlc`

**Audit ID:** AUDIT-2026-08-31-mnq-overnight-lookahead
**Date:** 2026-08-31
**Triggered by:** external observation (Codex PR review) + independent re-verification
**Authors:** Joshua + claude.ai
**Scope:** brief family (`Q-RANGEXFER-1`, `Q-RANGECOND-1`) — MNQ-side hypotheses only
**Lives in:** `docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md`

---

## §0 — Source anchors

All paths below verified by direct read on 2026-08-31, same day as the fix.

- `lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py` — `overnight_ohlc()`, the
  defective function (fixed in this same commit, confirmed by direct read 2026-08-31).
- [PR #227](https://github.com/Joshua-Asante/first-passage/pull/227) — Codex's Pine-parity review,
  where the defect was first surfaced.
- [PR #228](https://github.com/Joshua-Asante/first-passage/pull/228) — the branch carrying both
  `Q-RANGEXFER-1` and `Q-RANGECOND-1`, and this correction.
- `docs/briefs/closures/Q-RANGECOND-1-closure-resolved.md` — the retracted closure that cited the
  contaminated result as `RESOLVED`.
- `docs/pursuits/b3-orb-mnq-payability-line.md` — the live operational pursuit document whose
  addendum cited the contaminated result as new payability evidence.
- `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/load_sessions.py` — MYM's own,
  independently-authored `overnight_ohlc`, read directly on 2026-08-31 and confirmed to never
  share this defect.

---

## §1 — Trigger (what prompted this audit)

On 2026-08-31, reviewing Codex's PR #227 (a Pine indicator port of the overnight-range
conditioner) for parity against the tested Python construct, Codex's own review flagged that the
Pine port's overnight-window handling diverged from what looked like the intended session
boundary. Re-checking the Python reference directly (not assuming the Pine port was the one at
fault) showed the divergence was not a porting error — the Python reference itself,
`data_lib.py::overnight_ohlc`, had been silently including bars from *after* the outcome it was
used to predict. This halted an otherwise-closed `RESOLVED` verdict (`Q-RANGECOND-1`) and required
re-derivation of every hypothesis sharing that function.

**Failure class:** Source-of-truth fracture (a stale docstring claimed a 17:00 ET session
boundary that the code never actually encoded) compounding a methodology failure (no check in
this research line re-derives a predictor from raw bars against an independently-sourced session
boundary — see §3).

---

## §2 — What actually happened

1. `data_lib.py::overnight_ohlc()` computed a trading day's "overnight range" from every
   `is_rth==False` bar sharing that day's `trading_day` label. Only `RTH_CLOSE_MIN=16:00` and
   `TRADING_DAY_CUTOVER_MIN=18:00` gated anything — so the function silently included bars from
   **[16:00, 18:00) ET on the same calendar date**, i.e. bars occurring strictly *after* that
   trading day's own RTH session had already closed, not before it.
2. The module's own docstring claimed the Globex day "closes 17:00 ET," but that boundary was
   never actually encoded — stale, aspirational prose that didn't match what the function did.
3. `RTH_range_d` (the outcome the conditioner is meant to predict) is fully determined by 16:00 ET
   on day `d`. `on_range_d`, as literally computed, was not fully determined until 18:00 ET on day
   `d` — two hours *after* the very outcome it was used to "predict." The frozen `bias_overnight_d`
   predictor therefore partly incorporated information from later that same day: a genuine
   look-ahead defect, not a cosmetic scope difference.
4. Quantified before any fix landed: the [16:00,18:00) ET window has bars on 1,495/1,559 trading
   days (populated almost every day); including it changed `on_range` on 1,096/1,559 days (70%),
   mean inflation 90.7 index points; the derived `bias_overnight` flag — the actual binary
   predictor driving every downstream hypothesis — flipped on 312/1,499 scored days (20.81%).
5. Scope check by direct import-source inspection (`grep "^from\|^import"` on every consuming
   script, not assumed from naming convention) confirmed MYM's independently-authored
   `load_sessions.py::overnight_ohlc` (which uses `minute <= OVERNIGHT_CLOSE_MIN`) never shared
   this defect — only MNQ-side hypotheses were contaminated.
6. Root cause fixed in `data_lib.py`; all affected constructs re-derived; every governance
   artifact citing the original figures corrected same-day (§5).

---

## §3 — Discipline checks that should have caught it

| Check | Should have caught | Actual behavior |
|---|---|---|
| §1 Rule 0 reads | Partial — Rule 0 requires reading production code before authoring, which was done, but reading the code is not the same as re-deriving its output from raw bars against an independent boundary definition | Missed — the code was read and appeared self-consistent (docstring and constants both present); the discrepancy between the docstring's *claimed* 17:00 boundary and the *actual* unenforced boundary was not mechanically checked |
| §2 Falsifiable hypothesis | N/A | — |
| §3 Forbidden moves | N/A — this is a data-pipeline defect, not a forbidden-move violation | — |
| §4 Gate criteria binary | No — the L1-L4 gates fired correctly on the (contaminated) data; the defect was upstream of the gate, not in it | Gates behaved exactly as designed; they cannot catch a corrupted input |
| §5 Question form | N/A | — |
| §6 Audit hooks runnable | Partial — the presence-battery adversarial workflow (2026-08-30) re-verified CI mechanics and restriction logic, but none of its checks re-derived `on_range` from raw bars against an independently-sourced session boundary | Missed — every check shared the same underlying `data_lib.py` computation |
| §7-10 CC handoff checks | N/A | — |

If a check that should have fired didn't, the audit's first repair target is that check: no
existing discipline check re-derives a load-bearing predictor from a second, independently-sourced
implementation before certifying it. See §5 structural repair.

---

## §4 — Root cause analysis

- **Immediate cause:** `data_lib.py::overnight_ohlc()`'s overnight mask (`~is_rth`) included the
  same trading day's own [16:00,18:00) ET post-RTH-close window, which the function's constants
  never explicitly excluded.
- **Contributing factor:** the module's docstring asserted a 17:00 ET Globex-day-close boundary
  that was never actually encoded in code — a source-of-truth fracture between comment and
  behavior that a code read alone does not surface, only a re-derivation against raw bars does.
- **Structural cause:** this research line's verification passes (in-chat adversarial Workflow
  review, presence-battery re-checks) all validated logic *given* `data_lib.py`'s output, never
  re-derived that output from a second, independently-sourced session-boundary implementation.
  MYM's `load_sessions.py` was exactly that independent implementation and existed the whole time
  — it was simply never used as a cross-check against MNQ's `data_lib.py`, despite both files
  computing the same conceptual quantity for sibling instruments in the same research campaign.

Five-whys stops here: the repairable layer is "cross-check sibling implementations of the same
predictor before certifying," not a deeper claim about pandas, session conventions, or CME data.

---

## §5 — Repair plan

### Immediate

- [x] `data_lib.py::overnight_ohlc()` corrected to restrict explicitly to
      `et_minute < RTH_OPEN_MIN OR et_minute >= TRADING_DAY_CUTOVER_MIN`.
- [x] `H-RANGEXFER-1` / `H-RANGEXFER-1.a` re-derived (presence battery + by-year L4); verdict
      routing unchanged, magnitudes/`n_valid` corrected via dated amendment on
      `Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md` and its closure.
- [x] `Q-RANGECOND-1` re-derived; verdict flips `RESOLVED` → `FALSIFIED`. Original closure marked
      `RETRACTED` (Trap #12: banner added, original text preserved); new closure
      `Q-RANGECOND-1-closure-falsified.md` filed with corrected Iterate block.
- [x] `b3-orb-mnq-payability-line.md` addendum retracted (the operationally live document —
      leaving stale "new payability evidence" language there would actively mislead).
- [x] `STATE.md`, `docs/SESSIONS.md`, `docs/briefs/INDEX.md`, `lab/CATALOG.md`,
      `ops/instruments/MECHANISMS.md` updated to reflect the corrected verdict.

### Structural

- [ ] No SKILL.md / template / validator change proposed yet — this is a single-incident finding
      (see §6); below the two-incident bar for a new standing mechanical check. If a second,
      independent instance of "sibling implementations diverge and only an external reviewer
      catches it" occurs, promote to a standing pre-registration requirement: any construct with a
      same-concept sibling implementation elsewhere in the repo must diff its raw output against
      that sibling before certification.
- [ ] No calendar/Todoist trigger added — the audit hook below (§10) is the mechanical detector,
      run on demand rather than scheduled, since the root cause is already fixed and this is a
      closed incident, not an ongoing risk surface.

If no further structural repair lands, the failure mode (a load-bearing predictor validated only
by checks sharing its own computation) can recur elsewhere in the repo. Accepted explicitly here
rather than over-engineered — see §6 promotion status.

---

## §6 — Lessons to capture

- **Candidate lesson 1:** An external, independently-sourced re-implementation of a load-bearing
  predictor is a stronger verification signal than any number of checks that all share the same
  underlying computation — a from-scratch reimplementation built against the same spec by a
  different author/reviewer will disagree where shared-computation checks cannot.
  - Anchor: this audit (2026-08-31).
  - Cost: a closed `RESOLVED` verdict + a live pursuit-document addendum, both wrong for
    approximately 24 hours; no live spend, no capital exposure (`Q-RANGECOND-1` never reached an
    entry-construct license).
  - Lesson registry destination: `references/verification_lessons.md` (or nearest equivalent).
  - Promotion status: Candidate (needs 1 more independent firing, or a structural-argument
    approval, before graduating to a standing check per Known Trap #9).
  - Already covered by (partial): `lesson_verify_source_not_label.md`,
    `lesson_offline_port_needs_real_source_anchor.md` — those cover borrowed/ported values from
    *external* sources; this is the narrower case of two *internal* sibling implementations of the
    same concept diverging. Related but not duplicate.

---

## §7 — Programme-audit signal check (cross-skill)

- [ ] Belt-patches without independent corroboration? — No; this fix was itself found via
      independent corroboration (Codex + MYM's independent implementation).
- [ ] Belt that only grows, never prunes? — N/A.
- [ ] Falsifier thresholds drifting toward "we'd never hit this"? — No; the L1-L4 gates fired
      correctly once given corrected input.
- [ ] Methodology invoked to rationalize a decision already made? — No.
- [ ] SNAG pattern (multiple null/ambiguous loops same domain)? — No; single defect, single
      correction pass.
- [ ] Cross-layer contamination (methodology citing portfolio evidence or vice versa)? — No.
- [ ] Negative heuristic crossed without repair? — No.

No box checked — this audit does not escalate to programme-audit. Closed here.

---

## §10 — Audit hooks (forward-looking)

```bash
# Confirm the fix is in place
grep -n "et_minute < RTH_OPEN_MIN) | (df\[.et_minute.\] >= TRADING_DAY_CUTOVER_MIN" \
  lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py

# Reproduce the corrected H-RANGEXFER-1 stage-1 lifts
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate2_overnight_rth_transfer.py
# Expected: stratum bias'=0 lift ~0.2632, stratum bias'=1 lift ~0.2684

# Reproduce the corrected Q-RANGECOND-1 verdict
python lab/analysis/_inbox/rangecond_1_2026-08-30/phase1_2_3_conditioned_orb.py
# Expected: WR diff CI includes 0, mean-win diff CI includes 0, VERDICT=FALSIFIED

# Recurrence check schedule
# No scheduled re-check — root cause fixed in place; this hook is for on-demand verification only.

# Cross-reference to spawned lesson entries
grep -rln "AUDIT-2026-08-31-mnq-overnight-lookahead" docs/methodology/lessons/*.md 2>/dev/null
# Expected (once promoted): matches the §6 candidate lesson if/when it graduates
```

---

## §11 — Closure

- **Status:** `Closed (immediate + structural complete)` — the only structural repair proposed
  (§5) is deferred-by-design pending a second firing, which is itself the structural decision, not
  an open item.
- **Immediate repair completed:** 2026-08-31.
- **Structural repair completed:** n/a — none required at this incident count (see §5, §6).
- **Lessons graduated to standing rule:** none yet (§6 candidate lesson still at Candidate status).
- **Follow-up audits triggered:** none.

---

## Verification

```bash
# Canonical skill-side checker (ADR 2026-08-09) — validates audit's real §0-§11 contract
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md --type audit
# Expected: RESULT: well-formed

# Repo-side (mechanical subset — audit is a declined type here, expected not a gap)
$ python scripts/check_brief.py \
    docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md --type audit
# Expected: RESULT: NOT CHECKED — see the skill-side result above for the gate that counts

# Confirm the root-cause fix
$ grep -n "TRADING_DAY_CUTOVER_MIN" lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py

# Confirm downstream re-derivation outputs (§10 hooks above)
```
