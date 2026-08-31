# Audit note — MYM overnight-window scope-gap defect in `load_sessions.py::overnight_ohlc`

**Audit ID:** AUDIT-2026-08-31-mym-overnight-scope-gap
**Date:** 2026-08-31
**Triggered by:** external observation (Codex PR review, second pass) + independent re-verification
**Authors:** Joshua + claude.ai
**Scope:** brief family (`Q-RANGEXFER-1`) — MYM-side hypotheses only
**Lives in:** `docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md`

**Companion:** [`2026-08-31-mnq-overnight-window-lookahead-defect.md`](2026-08-31-mnq-overnight-window-lookahead-defect.md)
— a related but distinct defect (look-ahead, not scope-gap) found the same day in MNQ's sibling
function. That audit's own §11 closure had stated MYM's implementation was "unaffected" — this
audit corrects that claim: MYM was affected, just by a different failure mode.

---

## §0 — Source anchors

All paths below verified by direct read on 2026-08-31, same day as the fix.

- `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/load_sessions.py` — `overnight_ohlc()`,
  the defective function (fixed in this same commit, confirmed by direct read 2026-08-31).
- `lab/archive/msl_c1_mym_2026-08/construct_lib.py` — the source of the borrowed, flawed
  construct, confirmed by direct read 2026-08-31 to carry its own `"DELETE sham"` docstring on the
  identical `[00:00, 09:29]` window.
- [PR #227](https://github.com/Joshua-Asante/first-passage/pull/227) — Codex's second-pass Pine
  parity review, where this second defect was surfaced (the first pass, after the MNQ fix, was
  clean on MNQ but flagged the MYM mismatch).
- [PR #228](https://github.com/Joshua-Asante/first-passage/pull/228) — the branch carrying
  `Q-RANGEXFER-1` and this correction.
- `docs/briefs/closures/Q-RANGEXFER-1-closure-ambiguous-design.md` — the closure whose MYM rows
  carried the contaminated figures.
- `docs/notes/audits/2026-08-31-mnq-overnight-window-lookahead-defect.md` — the companion audit,
  whose own §11 "MYM unaffected" claim this audit corrects.

---

## §1 — Trigger (what prompted this audit)

On 2026-08-31, after landing the MNQ look-ahead fix (see the companion audit) and posting it to
Codex on PR #227, a fresh Codex review pass (triggered by an explicit `@codex review` comment)
found that the Pine indicator's single `inOvernight` window predicate — now an exact match for
the corrected MNQ definition — could not achieve parity with MYM's own frozen Python helper.
Direct read of `load_sessions.py::overnight_ohlc` confirmed: it filters bars to `minute <= 569`
(a raw ET-clock minute-of-day), which can never include the 18:00–23:59 ET evening-reopen segment
regardless of session bucketing. This defect had been present the entire time the MNQ correction
was in progress but was masked from view: the earlier audit and every governance artifact updated
that day assumed MYM was "the independent, correct implementation" solely because it lacked the
MNQ look-ahead bug — without independently re-deriving MYM's own output from raw bars.

**Failure class:** Source-of-truth fracture (a construct explicitly flagged `"DELETE sham"` in its
origin was copied forward without the flag being noticed or acted on) compounding the same
methodology gap named in the companion audit's §3/§4 (no check in this research line re-derives a
predictor from raw bars against an independently-sourced session boundary).

---

## §2 — What actually happened

1. `load_sessions.py::overnight_ohlc()` filtered bars with `bars["minute"] <= OVERNIGHT_CLOSE_MIN`
   (569, i.e. 9:29 AM), where `minute = hour*60+minute` is a raw ET-clock value, not
   session-relative. Combined with the module's own (correct) `session` bucketing — which assigns
   any bar with `hour >= 18` to the *next* calendar date's session — this filter can never select
   an evening-reopen bar for any session, no matter how it groups.
2. Net effect: for every session, `overnight_ohlc()` returned only the 00:00–09:29 ET
   early-morning tail. The prior evening's 18:00–23:59 ET Globex reopen — roughly 6 of the ~15.5
   overnight hours — was silently excluded entirely, on every single trading day.
3. Traced the origin: the constant name and filter pattern were copied from
   `lab/archive/msl_c1_mym_2026-08/construct_lib.py`, whose own `overnight_hl()` function carries
   the docstring `"DELETE sham -- same Globex-day overnight clock window [00:00, 09:29] ET."` —
   i.e., the *source* campaign had already identified this exact construct as a sham placeholder
   slated for deletion, not a validated definition of "overnight range." That flag did not travel
   with the copy into `load_sessions.py`.
4. `load_sessions.py`'s own module docstring describes the *intended* scope correctly: "overnight
   sub-window = same trading-day's bars strictly before 09:30 ET," for a session defined as
   `[D-1 18:00 ET, D 17:00 ET)`. Read literally, "same trading-day's bars strictly before 09:30 ET"
   necessarily includes the D-1 evening segment (it belongs to trading day D and is strictly before
   09:30 ET of day D) — the code just never implemented that.
5. Quantified before any fix landed: `on_range` changed on 817/1,304 days (63%), mean inflation
   +38.0 index points; the derived `bias_overnight` flag flipped on 113/1,304 scored days (8.67%).
   Smaller in magnitude than the MNQ look-ahead defect (20.81% flip rate) but material — one of the
   three MYM hypotheses (`H-RANGEXFER-1.a-MYM`) crossed a hard gate threshold as a direct result
   (see §2 corrected results below).
6. Root cause fixed in `load_sessions.py`; `H-RANGEXFER-1-MYM`, `H-RANGEXFER-1.a-MYM`,
   `H-RANGEXFER-1.b-MYM` re-derived; the closure and brief corrected same-day.

### Corrected results

| Hypothesis | Limb | Original (buggy) | Corrected |
|---|---|---|---|
| H-RANGEXFER-1-MYM | observed lift | +0.2170 | **+0.2234** |
| | L2 CI | `[+0.110,+0.310]` (excludes 0) | **`[+0.121,+0.307]`** (excludes 0 — unchanged) |
| | L4 `n_valid` | 3 | **3** (unchanged) |
| | Verdict | `AMBIGUOUS-DESIGN` | **`AMBIGUOUS-DESIGN`** (unchanged) |
| H-RANGEXFER-1.a-MYM | observed lift | +0.0848 | **+0.0110** (effect nearly vanishes) |
| | L1 (n-floor, `n_cond>=100`) | PASS (n_cond=124) | **FAIL** (n_cond=96) |
| | L2 CI | `[-0.008,+0.180]` (includes 0 — already FAIL) | **`[-0.093,+0.115]`** (includes 0 — still FAIL) |
| | L3 (both halves positive) | PASS (both halves positive) | **FAIL** (half2 = -0.038, negative) |
| | L4 `n_valid` | 4 | **3** |
| | Verdict | `FALSIFIED` (presence fails via L2) | **`FALSIFIED`** (presence fails via L1+L2+L3 — same route, wider margin) |
| H-RANGEXFER-1.b-MYM | observed lift | +0.1394 | **+0.1394** (byte-identical) |
| | L2 CI | `[+0.057,+0.219]` | **`[+0.057,+0.219]`** (byte-identical) |
| | L4 `n_valid` | 6 | **6** (unchanged) |
| | Verdict | `AMBIGUOUS-DESIGN` | **`AMBIGUOUS-DESIGN`** (unchanged) |

`H-RANGEXFER-1.b-MYM` is byte-identical because its predictor (`bias_gap`) and restriction
variable (`bias_dayhist`) never touch `on_range`/`bias_overnight` — confirmed structurally, not
coincidentally.

**Net: no `Q-RANGEXFER-1` §6 route changes.** The closure's overall `MIXED` verdict (4×
`AMBIGUOUS-DESIGN`, 1× `FALSIFIED` on `H-RANGEXFER-1.a-MYM`) is unaffected — `H-RANGEXFER-1.a-MYM`
was already the one FALSIFIED hypothesis and remains so, now failing on three limbs instead of one.
Corrected via dated amendment (Trap #12), not a re-open.

---

## §3 — Discipline checks that should have caught it

| Check | Should have caught | Actual behavior |
|---|---|---|
| §1 Rule 0 reads | Partial — `load_sessions.py` was read as part of the original MYM Notice authoring and again during the MNQ correction (to confirm "MYM is independent"), but never re-derived from raw bars against a second, independently-sourced boundary | Missed both times — the second read (during the MNQ correction, hours before this defect surfaced) explicitly concluded MYM was "correct" from code inspection alone, the exact failure mode the companion audit's §4 already names |
| §3 Forbidden moves | N/A | — |
| §4 Gate criteria binary | No — L1/L2/L4 fired correctly on the (contaminated) MYM data; the defect was upstream of the gates | Gates behaved as designed; cannot catch a corrupted input |
| §6 Audit hooks runnable | No — the presence-battery adversarial workflow (2026-08-30) verified bootstrap/restriction/L3 logic exhaustively but never re-derived `on_range` from raw MYM bars against an independent boundary | Missed — every check shared `load_sessions.py`'s own computation |
| §7-10 CC handoff checks | N/A | — |

Same structural gap as the companion audit, now confirmed on a second, independent instance: no
check in this research line diffs a load-bearing predictor's raw output against a second,
differently-sourced implementation before certifying it.

---

## §4 — Root cause analysis

- **Immediate cause:** `load_sessions.py::overnight_ohlc()`'s filter (`minute <= 569`, a raw
  ET-clock value) cannot select the 18:00–23:59 ET evening-reopen segment for any session.
- **Contributing factor:** the filter pattern and constant were copied from
  `construct_lib.py::overnight_hl()`, whose own docstring flags the identical construct as a
  "sham" placeholder slated for deletion — that provenance signal did not travel with the copy,
  and nothing in this module's own authoring process checked the borrowed construct against the
  module's own (correct) prose description of intended scope.
- **Structural cause:** the same one named in the companion audit's §4 — this research line's
  verification passes validate logic *given* a helper's output, never re-derive that output from a
  second, independently-sourced implementation. This is now the SECOND instance of that exact
  structural gap firing in the same 24-hour window, on two different instruments, via two
  different specific bugs (look-ahead vs. scope-gap) — see §6 promotion.

Five-whys stops here, same repairable layer as the companion audit: cross-check sibling/borrowed
implementations of the same predictor before certifying, this time with the added specificity that
a source construct's own "DELETE"/"sham"/deprecation language must be checked before reuse, not
just its numeric output.

---

## §5 — Repair plan

### Immediate

- [x] `load_sessions.py::overnight_ohlc()` corrected to `(minute < RTH_OPEN_MIN) | (minute >=
      EVENING_REOPEN_MIN)`, combined with the existing (already-correct) `session` bucketing.
- [x] `H-RANGEXFER-1-MYM` / `H-RANGEXFER-1.a-MYM` / `H-RANGEXFER-1.b-MYM` re-derived (presence
      battery + by-year L4); no §6 route changed.
- [x] `Q-RANGEXFER-1-closure-ambiguous-design.md` corrected in place (dated note + row-level
      "(corrected; was X)" annotations) — no re-open, same pattern as the MNQ-side correction.
- [x] `Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md` §11 amendment log gets a second,
      separate dated row for this fix (distinct from the MNQ-fix row already there).
- [x] `rangexfer_presence_battery_2026-08-30/RESULTS.md` and
      `rangexfer_byyear_l4_2026-08-30/RESULTS.md` correction banners extended to cover both fixes.
- [x] The companion MNQ audit's own §11 "MYM rows are unaffected" claim is now known-superseded by
      this audit; not edited in place (Trap #12 — that audit accurately described the MNQ-defect
      scope as understood *at the time it was written*), but cross-linked from both directions.

### Structural

- [ ] Same deferred decision as the companion audit's §5: this is now a **second** firing of the
      identical structural gap (no cross-check against an independently-sourced sibling
      implementation) within 24 hours, on two different bugs. This crosses the two-incident bar
      named in the companion audit's §6 as the threshold for promotion. See §6 below — this audit
      promotes the lesson rather than leaving it at Candidate status.
- [ ] No calendar/Todoist trigger added — root cause is fixed in place; the audit hook below is
      for on-demand verification.

---

## §6 — Lessons to capture

- **Candidate lesson (PROMOTED — second independent firing within 24 hours):** An external,
  independently-sourced re-implementation of a load-bearing predictor is a stronger verification
  signal than any number of checks that all share the same underlying computation. First fired on
  the MNQ look-ahead defect (companion audit); fires again here on a structurally different bug
  (scope-gap, not look-ahead) in MYM's own, previously-trusted-by-default sibling implementation.
  Both instances were caught only by Codex's external, from-scratch Pine reimplementation
  disagreeing with the Python reference it was built against the same spec as — never by any
  in-repo check, however thorough, that shared the reference implementation's own computation.
  - Anchor: this audit (2026-08-31) + companion audit (2026-08-31), same day, two instruments.
  - Cost: three MYM hypothesis rows in a closed closure carried contaminated (though, per §2,
    verdict-preserving) figures for several hours; no live spend, no capital exposure.
  - Lesson registry destination: `references/verification_lessons.md` (or nearest equivalent).
  - Promotion status: **promoted to standing check** — before certifying any predictor that has a
    same-concept sibling implementation elsewhere in the repo (same research line, same or
    adjacent instrument), diff the sibling's raw output against the candidate before treating
    either as ground truth. Absence of a shared bug is not evidence of correctness on its own.
  - Already covered by (partial, per the companion audit): `lesson_verify_source_not_label.md`,
    `lesson_offline_port_needs_real_source_anchor.md`.

---

## §7 — Programme-audit signal check (cross-skill)

- [ ] Belt-patches without independent corroboration? — No; found via independent corroboration
      (Codex's second review pass).
- [ ] Belt that only grows, never prunes? — N/A.
- [ ] Falsifier thresholds drifting toward "we'd never hit this"? — No.
- [ ] Methodology invoked to rationalize a decision already made? — No.
- [ ] SNAG pattern (multiple null/ambiguous loops same domain)? — No; two related but distinct
      defects, both promptly fixed.
- [ ] Cross-layer contamination (methodology citing portfolio evidence or vice versa)? — No.
- [ ] Negative heuristic crossed without repair? — No.

No box checked — this audit does not escalate to programme-audit. Closed here.

---

## §10 — Audit hooks (forward-looking)

```bash
# Confirm the fix is in place
grep -n "EVENING_REOPEN_MIN\|RTH_OPEN_MIN) | (bars" \
  lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/load_sessions.py

# Reproduce the corrected presence-battery numbers
python lab/analysis/_inbox/rangexfer_presence_battery_2026-08-30/presence_l1_l3.py
# Expected: H-RANGEXFER-1.a-MYM L1_n_floor=False, L2 CI includes 0, presence_pass=False

# Reproduce the corrected by-year L4 counts
python lab/analysis/_inbox/rangexfer_byyear_l4_2026-08-30/byyear_l4.py
# Expected: H-RANGEXFER-1.a-MYM n_valid=3 (was 4)

# Cross-reference to the promoted lesson entry
grep -rln "AUDIT-2026-08-31-mym-overnight-scope-gap" docs/methodology/lessons/*.md 2>/dev/null
```

---

## §11 — Closure

- **Status:** `Closed (immediate + structural complete)` — the structural repair (§6) was promoted
  directly to a standing check rather than deferred, since this is the second firing within 24
  hours.
- **Immediate repair completed:** 2026-08-31.
- **Structural repair completed:** 2026-08-31 (lesson promoted; the standing check itself is a
  verification-discipline norm, not a new mechanical gate — no validator change required).
- **Lessons graduated to standing rule:** the cross-check-siblings-before-certifying lesson (§6),
  promoted this audit.
- **Follow-up audits triggered:** none.

---

## Verification

```bash
# Canonical skill-side checker (ADR 2026-08-09) — validates audit's real §0-§11 contract
$ python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
    docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md --type audit
# Expected: RESULT: well-formed

# Repo-side (mechanical subset — audit is a declined type here, expected not a gap)
$ python scripts/check_brief.py \
    docs/notes/audits/2026-08-31-mym-overnight-window-scope-gap-defect.md --type audit
# Expected: RESULT: NOT CHECKED — see the skill-side result above for the gate that counts

# Confirm the root-cause fix
$ grep -n "EVENING_REOPEN_MIN" lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/load_sessions.py

# Confirm downstream re-derivation outputs (§10 hooks above)
```
