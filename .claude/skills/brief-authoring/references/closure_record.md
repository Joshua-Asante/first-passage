# [Q-X] — CLOSURE: `[VERDICT]` ([one-line qualifier])

Filename: `docs/briefs/closures/Q-X-closure-<verdict-slug>.md` — the verdict lives in the
filename and the H1 title (house convention; `handoff-verify` treats the filename as the
closure vocabulary). This template distills the observed strong closures (Q-GEOFIT-1,
Q-COSTGEO-2, Q-HARV-0, Q-CAPALLOC-2) plus the mandatory Iterate block ratified by
`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`.

**Verdict:** `[as filed — RESOLVED / FALSIFIED / AMBIGUOUS[-qualifier] / VOID / MOOT / ABORT / operator-stopped / screen-fail / …]`
**Closed:** YYYY-MM-DD
**Lane:** `<preregistered-question lane slug from Q-SCORE-1 PREREG F2 | UNASSIGNED>`
**Pre-registration:** [`Q-X-verdict-preregistration.md`](../pre-registration/Q-X-verdict-preregistration.md) — frozen at `<commit>`
**Successor:** [named pre-reg link, iff one is authored — naming ≠ opening] or omit the line
**Spend / K:** $X.XX · K consumed: N
**Live effect:** [none / the state-flip this closure performs]
**Artifacts:** [paths]

---

## 1. Verdict (§6 asserted against actual numbers)

The Observe half — numbers vs the frozen §6 gate only; no winner language beyond what the
gate mechanically fires. Walk **every** pre-registered verdict route, not just the one that
fired (Q-C1PANEL lesson: a §5 void clause is a verdict route; enumerate it). If the verdict
was never reached (operator-stopped), say so and state that §6 verdicts may not be quoted.

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | [frozen condition] | [measured] | — |
| `FALSIFIED` | [frozen condition] | [measured] | ✓ |

## 2. What the pre-registration predicted vs what happened

[Required by §9 of the Pre-Q template. Surprises flagged; thin cohorts named.]

## 3. What this closure does NOT license

[Negative scope — the anti-overclaim section (Q-CAPALLOC-2 pattern). What readings of the
verdict are not authorized. Omit only if genuinely empty — rare.]

## 4. Defects found in the frozen brief (recorded, not repaired)

[Iff any. Per Trap #12 the frozen artifact is never edited; defects are recorded here and
become entry-packet inputs if Next = ITERATE. "None found" is a legal body.]

## 5. Lesson candidates

[Dated anchor + dollar/counterfactual cost, or "below the two-incident bar — watch" (Known
Trap #9). "No new lesson" is a legal body.]

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** [as filed above]
- **Model update:** [1–3 lines: what the prior framing got wrong or confirmed — beyond
  restating the §6 numbers. This is the Reflect residue.]
- **Next:** INTEGRATE | ITERATE | STOP  *(exactly one)*
- **Routing:**
  [INTEGRATE → the commit: ADR / state-flip / doctrine edit / wiring, + its re-validation]
  [ITERATE → return to: Q (reframe) | H (§4 rewrite) | Investigate (tighter test) |
   Identify (new thread) | dated packet / operator decision item]
  [STOP → why the thread dies here]
- **Entry packet:** *(required iff Next = ITERATE; else "n/a")* — what a successor must
  carry: frozen constraints AND positive carry-forwards (verified numbers, passing
  controls, H + prior verbatim), forbidden re-opens, K/$ budget. Naming a successor does
  NOT open it — operator GO is a fresh decision (parent-Q convention: named, not opened).
- **Stop rule / re-proposal bar:** *(required for ITERATE and STOP; "n/a — integrated"
  legal for INTEGRATE)* — what evidence reopens this thread, or when it dies for good.
  Re-proposal bars demand new *mechanism* evidence, not new parameters.
- **Board write:** [the STATE forward-board row or SESSIONS Open/next line this closure
  adds, quoted verbatim — or `none — STOP, nothing owed`. One-line pointer + owner link
  only (Rule 7); detail stays in this file.]
- **Registry:** `rejected_candidates.md — ### <heading>` **or** `n/a — <reason>`
  (RESOLVED / governance / not a strategy-grounds kill). Token-gated; see
  [`docs/operational_rules.md`](../../../../docs/operational_rules.md) Rule 8
  sub-rule 9. Do not skip on FALSIFIED/DEAD/STOP.

## §10 audit-hook discharge

[Run the parent brief's §10 hooks this session; paste outputs. Defective hooks are
corrected here with the reason recorded (M-AHF), never silently passed.]

## Change history

| Date | Change | By |
|---|---|---|
| YYYY-MM-DD | Closure authored | — |

---

## Verification

```bash
# Iterate-block tokens present (gate 14's authoring-time form)
python scripts/check_closure_disposition.py docs/briefs/closures/Q-X-closure-<slug>.md

# Verdict routing covers every §6 route
grep -c "Fired?" <this-file>   # the routing table exists
```

Authoring notes (not part of the artifact):
- **Header `Closed:` / `Lane:` are machine-readable (PREREG F3 / N-2026-08-11).** Use `**Closed:** YYYY-MM-DD` (aliases `Closed (explore record):` and `Date:` are non-compliant). `**Lane:**` is a forward-only F2 slug or `UNASSIGNED` — do not invent mid-flight lane names; do not retro-edit undated closures to satisfy coverage.
- **The Iterate block REPLACES the ad hoc sections.** Pre-ADR closures wrote
  "Dispositions" / "Forward — what a successor must carry" / "Re-proposal:" sections;
  the block is where that content now lives, written once. Do not write both.
- **The pre-registered §6 branch is the default, not a cage.** Discharging a different
  branch is closure-time judgment, not a Trap-#12 amendment — quote the frozen §6 row
  and state why the other branch fired.
- **Verdict asymmetry is by design.** RESOLVED-and-fully-integrated closures owe no
  re-proposal bar; FALSIFIED/AMBIGUOUS/VOID/STOPPED closures owe one. Do not manufacture
  stop rules to fill the field — "n/a — integrated" is the honest value.
- **Only the tokens are mechanical.** Gate 14 checks heading + `Next:` + `Board write:`
  presence; everything else is judgment, audited at the quarterly methodology cadence
  (ceremony limb of the owning ADR's §4).
- Section numbering (numbered vs `§N`) follows your file; the Iterate block heading must
  contain the word "Iterate".
