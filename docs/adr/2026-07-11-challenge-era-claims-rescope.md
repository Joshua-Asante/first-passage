# ADR 2026-07-11 — Challenge-era claims re-scoped to historical record; venue-agnostic substrate retained; successor risk questions routed to a fresh Pre-Q

**Status:** Accepted (operator executive decision 2026-07-11 — "retire, but do not over-retire: things we no longer need can be retired, anything still materially useful to the operation stays" — recorded)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - Pepperstone-anchor, FXIFY-fixture, and challenge-diagnostic retention clauses only. The historical-record re-scope itself, the byte-unchanged numbers, and D1 stand. (See also this ADR's own 2026-07-22 addendum resolving D2.)
**Retain-until:** none
**Decision date:** 2026-07-11
**Authors:** Joshua (decision) + Claude Code (recorder)
**Supersedes:** none in-place. **Re-scopes** the *claim status* of: the CLAUDE.md MC-anchor framing ("current canonical" → historical challenge-era calibration), the lock-gate framing (bust <1% / p99 DD <5% as live acceptance criteria), the C2→C0 quarterly revert-criterion *semantics*, and the repo §Purpose statement. No ADR is superseded: 2026-05-23 (allocation), 2026-05-08 (C2), 2026-06-07 (decompound HOLD), 2026-07-10 (R6 NO-GO) all stand — this ADR changes what their headline numbers are *claims about*, not the numbers, constants, or decisions.
**Related:** AUDIT-2026-07-11-core-fxify-anchoring ([`docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md`](../notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md) — the motivating audit; this ADR executes its §5.1 + §5.3 + §5.5); [`2026-06-30-no-manual-trading-cfd-retirement.md`](2026-06-30-no-manual-trading-cfd-retirement.md) (+07-10 Addendum, FXIFY formally closed); [`2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md); [`2026-07-10-strategies-never-locked-lifecycle-governance.md`](2026-07-10-strategies-never-locked-lifecycle-governance.md) (the axis separation this ADR leans on).
**Layer:** portfolio / governance (claim scope + documentation + provenance labels) — **no** locked parameter, allocation, `dd_protection` constant, test pin, or Pine byte is touched.

---

## §0 — Rule 0 reads (production-source verification)

All read on-disk this session (worktree `core-parameter-evaluation-7f4f3a`, branch `claude/core-parameter-evaluation-7f4f3a`), full-file or section reads with surrounding context per the context-scope sub-rules. Anchors are `git log -1 --format='%h %ci' -- <path>` outputs verified 2026-07-11:

- `core/firm_rules.py` — anchor `4777d9f` (2026-07-10). 10 firm configs (FXIFY / Bulenox ×5 / Tradeify ×4), all referencing closed or falsified programs; `ACTIVE_FIRM = "FXIFY"` (:206); `BASELINE_BALANCE = 200_000` (:229); `_BASE_RISK` 0.0034/0.0070/0.0150/0.0037 (:225) byte-stable.
- `core/dd_protection.py` — anchor `4441c72` (2026-07-11, fail-closed hardening; FXIFY semantics unchanged). `_F = FIRM_RULES[ACTIVE_FIRM]` (:47); `DAILY_LOSS_LIMIT = _F["daily_loss_pct"] / 100` (:52) — `TypeError` for all 9 non-FXIFY configs (`daily_loss_pct: None`); DD_TRIGGER 0.015 / DD_SCALE 0.40 (:58-59) + MVD spec pins (:255-264) intact; `starting_equity` hard-locked to 200,000 in state validation.
- `core/mc/modes.py` — anchor `f2be990` (2026-07-11, facade refactor; semantics unchanged). Docstring: "challenge-outcome simulator" (:2); `PROFIT_TARGET = BASELINE_BALANCE * 1.05` = $210K (:52), ±5% daily/static barriers (:53-54), `MIN_TRADING_DAYS 5` (:55), `INACTIVITY_LIMIT 60` FXIFY-correct timeout (:56-64). Same `None/100` pattern at :53.
- `core/config/params.toml` — anchor `784a9ab` (2026-06-24). `[mc_anchor_pepperstone]` 99.83/0.17/4.37, median 26, anchor_date 2026-05-24.
- `tests/core/test_mc_anchors.py` — anchor `f2be990` (2026-07-11). Pins 0.9983/0.0017/0.0437 (abs 1e-4, :81-83); lock-criteria test "bust <1%, p99 DD <5%" (:121-130).
- `scripts/verify_lock_anchors.py` — anchor `f2be990` (2026-07-11). Read in full before the CLAUDE.md edits below: the parser requires the bold `**X% pass / Y% bust …**` + same-sentence `p99 DD Z%` pattern in every retained CLAUDE.md copy (all copies must agree with params.toml + test pins) and finds the median integer within 100 chars after each headline. The §7 edits preserve these tokens. `python scripts/verify_lock_anchors.py` → **ROUTING: Closed** both before and after the edits (verification block).
- `scripts/validate_params.py` — CLAUDE.md coupling read (:497-560): requires the "Strategy Reference" markdown table with name/risk/version/contractValue cells. The §7 edits do not touch table rows.
- `core/csv_parser.py` — anchor `4441c72` (2026-07-11). DXTrade (Alchemy/FXIFY) parser; emitting venue closed.
- `lab/archive/tradeify_selectflex_remc_2026-07-10/RESULTS_tradeify_remc_2026-07-10.md` — every tier × config row FAIL (best bust 3.03% ≥ 1%); grounds the "no live target exists among the 10 configs" premise.
- `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` §2.1 — Bulenox/Tradeify configs retained "for provenance … not as live targets".
- CLAUDE.md — anchor `04fee2e` (2026-07-11). §Purpose, §Multiplier System, §Strategy Reference MC-anchor bullets, §Protection revert trigger, §Firm Expansion — the surfaces §7 edits.

---

## §1 — Context

FXIFY formally closed 2026-07-10; the futures-prop path closed NO-GO the same day; the surviving scale path is self-funded (Aegis→M6J active, go-live separately gated). AUDIT-2026-07-11-core-fxify-anchoring then established, from production reads: the MC engine is by construction a *challenge-outcome simulator* — its headline anchor 99.83/0.17/4.37 is P(pass an FXIFY $200K challenge), its lock gates are challenge-survival criteria, the C2 calibration was partly justified on a days-to-**pass** objective, and the quarterly C2→C0 revert criterion is denominated in challenge pass-rate. None of these numbers drifted; the *questions they answer* were retired. Left labeled "current canonical," they become unfalsifiable-by-construction — the degradation the 2026-07-01 portfolio audit warned "starts without any of the seven signals firing."

**Decision driver (one sentence):** the operator has ratified the audit's retire/keep principle ("retire, but do not over-retire"), and the 2026-08-08 quarterly slate will otherwise execute mechanically on retired challenge semantics — the re-scope must land before it.

---

## §2 — Decision

**Challenge-era claims are re-scoped to historical record; the venue-agnostic substrate is retained unchanged; successor risk questions are owned by a fresh pre-registered Pre-Q, not by in-place edits.** Concretely, four coupled re-scopes (one decision — what the challenge-era numbers are claims about — applied to its four surfaces):

1. **MC anchor (R1, R2, R8):** 99.83/0.17/4.37 + median-26 is re-labeled **historical challenge-era calibration and engine regression pin** everywhere it is headlined. The numbers, `[mc_anchor_pepperstone]`, and the test pins are byte-unchanged — they now pin *engine reproducibility and panel integrity*, not a live pass-probability. The lock gates (bust <1% / p99 DD <5%) are likewise re-labeled historical lock criteria; the test asserting them is retained as a regression pin. "AUTHORIZED @ 1.00×" is read as *eligibility* — any venue must still pass its own transfer/go-live gates.
2. **Quarterly trigger semantics (R3, R4):** the C2→C0 revert check still runs on schedule (2026-08-08 →) but executes as a **historical-semantics diagnostic** — a fixed-benchmark health read of the panel through the frozen challenge lens — until the successor criterion lands via the D2 re-derivation at the 08-08 review. `dd_protection` constants are untouched; the C2 relock ADR stands as the record of a decision whose pass-time grounds are now void (noted, not edited).
3. **Operational-purpose restatement (R5, R6):** CLAUDE.md §Purpose is restated — the repo is the operational + research layer for the locked four-strategy book on the self-funded futures path; the multi-firm prop multiplier tooling (`accounts.py`, `cli.py lots/challenge`, `fxify_rule_validator.py`) is **dormant-historical, retained**. `ACTIVE_FIRM="FXIFY"` is relabeled the **historical anchor fixture** it is (anchor byte-reproducibility depends on it); the "add a firm and everything downstream adapts automatically" doctrine is retired — production falsifies it (`daily_loss_pct=None` → `TypeError` at `dd_protection.py:52` / `mc/modes.py:53` for 9/10 configs) — replaced by "firm onboarding requires an engine-support pre-flight." (Forward-looking citations are symbol-based — `DAILY_LOSS_LIMIT` / `DAILY_LOSS_PCT` — since this ADR's own Phase-2 docstring edits shift line numbers; the §0 line anchors describe the files as-read at their cited commits.)
4. **Archival labels (R7):** `csv_parser.py` (DXTrade) and DXTrade operational lore are labeled archival — retained for historical reconciliation, no live consumer.

**Kept, explicitly (the do-not-over-retire half, audit K1–K7):** parameter-axis locks + Pine + manifests; the `dd_protection` *mechanism* + MVD pins; `lifecycle.py` + beta-death controls; the MC engine substrate (week-block bootstrap, ingestion, MVD gates — already reused by the discovery campaigns); TV/Pepperstone panels + loaders + manifest gates; the regime findings and decompound/withdrawal machinery (the closest existing instrument for the self-funded successor question); the venue-falsification corpus and every rejection-registry bar.

**Effective:** immediately upon acceptance (2026-07-11).
**Scope:** claim status, documentation, and provenance labels only. Zero behavior change: no constant, allocation, test pin, Pine byte, or executable statement is modified.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Delete the dead surfaces** (firm configs, `fxify_rule_validator.py`, `challenge` CLI, `csv_parser.py`) | Over-retirement. R6 ADR §2.1 explicitly retains the configs for provenance + §4 re-open; anchor byte-reproducibility depends on the FXIFY fixture; the parser is the only reader of the historical fill record. Deletion buys nothing operational and costs provenance. Precedent exists for deletion (Dukascopy −760, OANDA −561 lines) but those had zero remaining consumers *and* a replacement; here the historical record is the consumer. |
| **Re-MC now under self-funded semantics and re-pin a new anchor** | Premature — the successor question (what replaces P(pass): max-DD line, time-under-water, withdrawal model) is not yet pre-registered, and running numbers before the question is frozen is the SNAG/best-of-K failure mode. D1 Pre-Q first. |
| **Fix the `None/100` latent crash now** | Speculative engine work with no live target firm; a "fix" without a named onboarding firm can't be validated against real rules. Documented at the call sites instead; fires as a pre-flight requirement on any future onboarding ADR. |
| **Leave everything as-is until a new venue exists** | The 2026-08-08 slate then executes on retired semantics and the headline claims sit unfalsifiable — the audit's named path to a DEGENERATING verdict at next cycle. |
| **Retire the decompound/regime machinery too ("it's challenge-era analysis")** | Over-retirement, explicitly guarded: the decompounded withdrawal-model re-MC is the *closest existing instrument* to self-funded reality (and both old gates breach on it — the successor framing tightens, not loosens). |

---

## §4 — Falsifier (revert trigger)

**H (falsifiable):** re-scoping the challenge-era claims to historical record preserves the full engine/panel regression value while eliminating the unfalsifiable-live-claim exposure — at zero behavior change. Verdict at each quarterly check: **RESOLVED** if the validators stay green (`verify_lock_anchors.py` Closed, `validate_params.py` 0 HARD) AND no challenge-era number is quoted as a live claim in any new ratified artifact; **FALSIFIED** if the historical label proves insufficient (a live-claim quotation of the anchor recurs in a ratified artifact, or a validator breaks because of the re-labeling); **AMBIGUOUS** if no new artifact touches the claim set before 2026-11-08 — then re-test at the following quarterly.

**Revert trigger (binary, event-driven):** if a live challenge-class venue re-enters the operation — either the R6 ADR's §4 new-mechanism trigger fires (futures-prop re-opens on a dated, pre-registered ≥0.8× edge-preservation result) or a fresh firm-onboarding ADR lands with a registered account — then the challenge-outcome MC question re-arms as a **live** claim class, and the re-arming ADR must commission a fresh re-MC under *that venue's* rules (never a revival of 99.83/0.17/4.37 as a live number — it stays historical regardless).

**Completion falsifier (this ADR's own success bar):** if by **2026-11-08** (second quarterly) no successor risk-framework Pre-Q has been pre-registered (audit §5.2 / D1), the re-scope is judged **incomplete** — the historical label without a successor question is just a renamed vacuum — and D1 escalates to a mandatory blocker on any Aegis→M6J go-live decision.

**Revert action:** supersede with a fresh ADR citing the re-arming event; never edit §2 in place.

**Trigger check schedule:** event-driven; reviewed at each quarterly audit/regime date — next **2026-08-08**, then 2026-11-08, 2027-02-08, 2027-05-08.

---

## §5 — Forbidden moves (under this ADR)

- **Editing `dd_protection` constants, the display banner, or any executable line "while we're here."** Genuinely tempting (the FXIFY banner is now anachronistic; C2's grounds are void) — but constants are frozen re-MC-gated, and the zero-behavior-change scope is what makes this ADR safe to accept without a re-MC. D2 owns the calibration question at 08-08.
- **Deleting or weakening the anchor test pins / lock-criteria test.** They are re-scoped to engine regression pins, not removed — deleting them severs byte-reproducibility of the engine against its only validated benchmark.
- **Treating the re-scope as license to re-open rejected candidates or re-optimize.** Venue retirement is not new mechanism evidence; every `docs/rejected_candidates.md` bar stands (audit K7).
- **Switching `ACTIVE_FIRM` or patching the `None/100` crash without an onboarding ADR.** The fixture is load-bearing for anchor reproduction; a speculative fix has no validation target.
- **Running successor-semantics MC numbers before the D1 Pre-Q freeze.** Numbers-before-question is the family's own pre-registration violation; the first self-funded MC result must land against a frozen question set.
- **Letting the 08-08 diagnostic output be quoted as a live pass-claim.** The run is a fixed-benchmark health read; quoting its pass-rate as a live probability re-creates exactly the unfalsifiable claim this ADR retires.

---

## §6 — Consequences

**Positive consequences:**
- The headline claim set becomes honest: every number in CLAUDE.md is either a live claim with a live referent or an explicitly historical calibration record. The audit's DEGENERATING-at-next-cycle condition is discharged.
- The 2026-08-08 slate runs with declared semantics instead of silently simulating a ghost venue.
- The keep-list is now explicit — the substrate (engine, panels, lifecycle, decompound machinery) is protected from over-retirement by name.
- Zero behavior change, zero re-MC needed, all validators stay green.

**Negative consequences (real cost):**
- The operation carries **no live risk claim at all** until the D1 successor framework lands — "historical calibration only" is an honest but uncomfortable posture for a book whose legs are all AUTHORIZED.
- Documentation surface area grows (historical labels, semantics notes) without any new capability.

**Risks (probabilistic):**
- The historical label could decay into background noise and the D1 Pre-Q never lands — mitigated by the §4 completion falsifier (2026-11-08 hard date) and the go-live blocker escalation.
- Future sessions may read "historical" as "safe to delete" — mitigated by the explicit keep-list in §2 and the §5 deletion prohibition.

**Downstream artifacts updated (this session, §7):**
- `CLAUDE.md` — §Purpose restated; MC-anchor bullets + §Protection re-labeled historical (verifier-token-preserving); §Firm Expansion doctrine corrected; posture pointer added.
- `core/firm_rules.py` — header + `ACTIVE_FIRM` provenance comments.
- `core/dd_protection.py` — docstring historical-fixture note (comment-only).
- `core/csv_parser.py` — docstring archival note.
- `STATE.md` — 08-08 trigger semantics note + D1 obligation.
- `docs/SESSIONS.md` — session entry updated.
- Audit note — §5.1/§5.3/§5.5 marked executed by this ADR.
- Memory — `project_core_fxify_anchoring_audit` updated.

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified this session (incl. today's `4441c72`/`f2be990` hardening commits — FXIFY semantics unchanged by them).
- **Phase 1** — this ADR; CLAUDE.md edits (token-preserving per the `verify_lock_anchors.py` / `validate_params.py` parsing contracts read in §0).
- **Phase 2** — comment/docstring provenance labels in `firm_rules.py`, `dd_protection.py`, `csv_parser.py` (no executable change).
- **Phase 3** — verification block executes (`validate_params.py` 0 HARD, `verify_lock_anchors.py` Closed, `check_brief.py --type adr`, dd_protection import self-check); STATE.md/SESSIONS.md/audit-note/memory sweep; status `Accepted`.
- **Deferred (owned elsewhere):** D2 calibration re-derivation (2026-08-08 review).
  **Update 2026-07-15:** D1 discharged — see the §4 completion-falsifier Addendum below (Q-SFRISK-1 `RESOLVED`, admitting ADR `Accepted`). §5.4 gate-denominated-closure annotation sweep **DONE** — [`docs/notes/audits/programme-audit/2026-07-15-gate-denominated-closure-annotation-sweep.md`](../notes/audits/programme-audit/2026-07-15-gate-denominated-closure-annotation-sweep.md) (6 closures annotated; rejection registry zero re-opens).

---

## §10 — Audit hooks (runnable)

```bash
# Discipline check
python scripts/check_brief.py docs/adr/2026-07-11-challenge-era-claims-rescope.md --type adr

# Historical re-labeling landed (CLAUDE.md)
grep -n "historical challenge-era" CLAUDE.md
# Expected: >=1 hit at each MC-anchor headline site

# Verifier still parses the re-labeled headlines; no drift introduced
python scripts/verify_lock_anchors.py   # Expected: ROUTING: Closed (exit 0)
python scripts/validate_params.py       # Expected: 0 HARD

# Provenance labels landed at the code sites
grep -n "historical anchor fixture" core/firm_rules.py
grep -n "2026-07-11" core/dd_protection.py core/csv_parser.py

# Nothing executable changed in core risk sources (docs/comments only)
git diff HEAD --stat -- core/ | grep -v "\.md"
# Expected: firm_rules.py / dd_protection.py / csv_parser.py comment-line deltas only

# §4 completion falsifier — successor Pre-Q exists by 2026-11-08?
ls docs/briefs/ docs/briefs/pre-registration/ 2>/dev/null | grep -i "selffunded\|self-funded\|successor" || echo "NOT YET (hard date 2026-11-08)"

# 08-08 diagnostic ran with declared semantics (check after the date)
grep -n "historical-semantics diagnostic" STATE.md CLAUDE.md
```

---

## Verification

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-07-11-challenge-era-claims-rescope.md --type adr
# Expected: all checks PASS

# Production-source verification (§0 anchors)
git log -1 --format='%h %ci' -- core/firm_rules.py        # 4777d9f 2026-07-10
git log -1 --format='%h %ci' -- core/dd_protection.py     # 4441c72 2026-07-11
git log -1 --format='%h %ci' -- core/config/params.toml   # 784a9ab 2026-06-24

# Gates green after all edits
python scripts/validate_params.py        # 0 HARD
python scripts/verify_lock_anchors.py    # ROUTING: Closed
python -c "import sys; sys.path.insert(0, 'core'); import dd_protection; print('dd_protection import self-check OK')"
```

---

## Addendum — 2026-07-15: §4 D1 completion falsifier discharged (Q-SFRISK-1 RESOLVED)

**D1 completion falsifier discharged in full**, well inside its 2026-11-08 hard date. [`Q-SFRISK-1`](../briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md) — the successor risk-framework Pre-Q this §4 clause required — was pre-registered (architecture 2026-07-14), numerically frozen (single triple T1, operator-confirmed "confirm T1," 2026-07-14), run against the decompound instrument (Phase 1, merged `936a9e0`, 2026-07-15), and adjudicated `RESOLVED` per its own §6/§9 gate ([`docs/briefs/closures/Q-SFRISK-1-closure-resolved.md`](../briefs/Q-SFRISK-1-closure-resolved.md)). The admitting ADR — [`docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md`](2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md) (`Accepted`, ratified 2026-07-15) — replaces this ADR's "historical calibration only" posture with a live, falsifiable self-funded successor claim (T1), while leaving every number, constant, and label this ADR re-scoped untouched (zero `core/` change either way).

This addendum does not edit §2/§4 in place — the historical-record re-scope of the challenge-era numbers stands exactly as decided 2026-07-11. It records that the completion condition §4 named has now been met, which was the open half of this ADR's own success bar.

---

## Addendum — 2026-07-22: §D2 resolved — Pepperstone panel released; quarterly C2→C0 revert check RETIRED

**D2 is resolved by retirement, not re-derivation.** This ADR deferred "D2
calibration re-derivation (2026-08-08 review)" and, pending it, kept the
quarterly C2→C0 revert check running as a **historical-semantics diagnostic** on
the frozen Pepperstone panel. The operator resolved D2 on 2026-07-22: the
Pepperstone panel is **released from successor-diagnostic duty**, and the
quarterly check is **retired outright** rather than re-pointed at a successor
input.

**Grounds.** The trigger's criterion is challenge-denominated — "rolling 6-month
MC *pass-rate* … falls below 95% for two consecutive windows" — and its own
harness notes it "is meaningful only as the panel live-extends." With the FXIFY
venue closed there is no challenge for a pass-rate to denominate, which is
exactly why this ADR §2.2 already ruled its output "must not be quoted as a live
pass-probability" and recorded that C2's median-days-to-pass grounds are "void
with the venue." A criterion that cannot be interpreted is not made safer by
continuing to run it on schedule; D2 existed to decide whether to re-derive it or
drop it, and the decision is to drop it.

**What this changes.** `python lab/analysis/time_to_pass.py --regime-check` is no
longer a standing quarterly obligation, and the 2026-08-08 / 11-08 / 2027-02-08 /
2027-05-08 dates carry no revert-check duty. The harness is not deleted here.

**What this does NOT change.** `DD_TRIGGER = 0.015` and `DD_SCALE = 0.40` are
**untouched, in force, and consumed by c1 sizing** (baselined 2026-07-22: the
boundary is exact at equity 98,500 against a 100,000 peak). Retiring the trigger
removes a *scheduled review*, not the control itself. Nor does it retire the
separate quarterly obligations that rode the same date — the per-strategy decay
review and Call-4 beta-death review remain on the `STATE.md` forward board.

**Change-control after this.** With no calendar trigger, `dd_protection`'s
`(trigger, scale, reference_mode)` are governed solely by the standing chain in
[`2026-07-13-dd-protection-concept-not-constant.md`](2026-07-13-dd-protection-concept-not-constant.md):
pre-registration → re-MC → **both-halves** regime-robustness gate → admitting
ADR. That chain is strictly stronger than the retired trigger, which could only
fire a revert to a single pre-named alternative (C0).

**Downstream.** This release satisfies **condition 3** of the pre-acceptance gate
in [`2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md)
§4, taking that ADR's Phase 0 to `RESOLVED`. Acceptance of the retirement ADR is
a **separate operator action** and is not performed by this addendum.

No `core/` file, constant, locked parameter, allocation, lifecycle tier, or c1
behaviour changes here. This is a governance-scope decision recorded in prose.

### Addendum-to-the-addendum — 2026-08-02: Rule 11 back-propagation that was owed and not done

The 2026-07-22 retirement above **darkened a standing falsifier limb on another in-force
ADR and did not record it**, which Rule 11 requires of the retiring decision.

Retiring the quarterly `time_to_pass.py --regime-check` duty extinguished **limb 1 of
[`2026-05-23-allocation-refresh-2.md`](2026-05-23-allocation-refresh-2.md)'s §Falsifier**.
That ADR's own 2026-07-01 addendum had named the quarterly check as the *sole surviving*
retroactive catch-path after its live edge-captured limbs went dark, and its §5 lists
*"Skipping the next four quarterly `time_to_pass.py --regime-check` runs"* as a forbidden
move. With limb 1 gone, that ADR has **zero live catch-paths**, and the §Override that
skipped its regime-robustness gate is uncovered.

The §Downstream note above swept only the substrate-retirement ADR. The allocation ADR was
named in this ADR's `**Supersedes:**` line as one that "stands" — correct as to its
*decision*, but its *coverage* changed and that was not recorded.

Dormancy, grounds, re-arm condition, and the operator options are recorded in
[`2026-05-23-allocation-refresh-2.md`](2026-05-23-allocation-refresh-2.md) §Addendum
2026-08-02. Nothing in the 2026-07-22 decision is reversed or weakened here — the retirement
stands on its stated grounds; only the owed sweep is completed.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial authoring + acceptance (operator directive: retire but do not over-retire; executes audit §5.1 + §5.3 + §5.5) | Joshua + Claude Code |
| 2026-07-15 | Addendum: §4 D1 completion falsifier discharged — Q-SFRISK-1 RESOLVED, admitting ADR drafted (`Proposed`). No §2/§4 edit; no core/ change. | Joshua + Claude Code |
| 2026-07-15 | Audit §5.4 DONE — gate-denominated closure annotation sweep (6 closures + rejection-registry standfast). No §2/§4 edit; no core/ change. | Cursor Cloud Agent |
| 2026-07-22 | Addendum: §D2 resolved by **retirement** — Pepperstone panel released from successor-diagnostic duty; quarterly C2→C0 revert check retired (challenge-denominated criterion, closed venue). `DD_TRIGGER`/`DD_SCALE` untouched; change-control falls back to the concept-not-constant pre-reg → re-MC → both-halves gate → ADR chain. Satisfies substrate-retirement §4 condition 3. | Joshua (decision) + Claude Code (recording) |
