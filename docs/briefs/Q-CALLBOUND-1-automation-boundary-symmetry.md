# Q-CALLBOUND-1 — Are the lifecycle Call-system's automation-authority boundaries symmetric and complete in both directions?

**Status:** `OPEN — DRAFT (pre-lock)` — execution requires a separate operator GO (parent-Q convention: naming is not opening)
**Authored:** 2026-08-18
**Closed:** N/A
**Authors:** Joshua + Claude Code
**Parent question:** N/A — opened from the assumption-sweep audit note
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on a $0/K=0 grep-and-read sweep of `core/`, `docs/adr/`, `docs/methodology/`, `STATE.md` for reverse-path vocabulary, plus a vocabulary-overlap diff between the sizing host's floor-to-zero language and Call 5's sign-off language
**Artifact path:** docs/briefs/Q-CALLBOUND-1-automation-boundary-symmetry.md

---

## Section 0 — Rule 0 reads (production-source verification)

- `core/lifecycle.py:21-23` — module docstring: "Writing state (a Call-1 tier demotion) is item 3, not built here — a human hand-edits `lifecycle_state.json` in the interim." No reverse-path mention anywhere in the file.
- `core/lifecycle.py:149-155` — `next_tier_down()`: walks `_LADDER_ORDER` strictly downward, floor `RETIRED`.
- `core/lifecycle.py:158-166` — `autonomous_demote()`: "Call 5: automation may move authorization DOWN only and may NEVER auto-RETIRE... the autonomous floor is WATCH-2." No promote function exists in the module.
- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md:66` — "Because the response is graded, reversible sizing (Call 2), a false positive costs only *one size step*, not a killed edge... The terror of the binary dissolves once the action is cheap." (the decision driver behind σ = 1.0)
- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md:71` — "recommended σ = 1.0 (tighter than the 2σ a kill-trigger would use, *because* the action is reversible)."
- `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md:213` — forbidden-moves list: "No autonomous size-up, ever. Automation may move authorization down only. It may never promote a tier, re-enter a RETIRED strategy, or increase size beyond the authorized tier."
- `docs/methodology/strategy_lifecycle.md:86-94` (Call 5) — "The boundary is **reversibility**... Reversible de-risk → autonomous (rules-mandated): tier demotions... **Irreversible retirement → operator GO/NO-GO** against pre-registered criteria: WATCH-2→`RETIRED` (**capital to zero**) and full beta shutdown."
- `docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md:23` — production-read table: "`autonomous_demote` floors at WATCH-2; no promote path in code today."
- `docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md:55` — "Call 5's 'never promotes' gains only this sandbox admit. No autonomous path to full AUTHORIZED book size, no RETIRED re-entry, no re-optimization." (S5 scopes strictly to brand-new CANDIDATE packets, not to restoring a demoted incumbent — confirmed by re-read, not merely asserted.)
- `ops/c1_rail/c1_sizing_host_reference.py:280` — `r_eff = base_risk * dd_scale * lifecycle_m` (WATCH-1's 0.50× haircut lands here).
- `ops/c1_rail/c1_sizing_host_reference.py:286-300` — `qty_base_raw = math.floor(risk_dollars / per_contract)`; `qty_out = min(qty_base_raw, reserve_cap)`. Ordinary integer-floor arithmetic, no zero-guard, no distinct code path for "size floored to zero."
- `ops/instruments/MNQ.md:143` (re-verified 2026-08-18; the audit note's originating read cited `:118` earlier the same session — this file is an append-only session log that grew between reads, confirmed same content at the new line) — "**NOT-M8 expected zero-fill:** at 0.50× on the $100K basis the MNQ base rounds to **0 contracts** at stops ≥93 pts (≥38 pts with DD active) — that is the sizing law working, not a fault."
- `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` D3, D6 — the source findings this Q transcribes, each independently cited above.

---

## Section 1 — Context and motivation

Origin: the 2026-08-18 assumption-sweep audit note (`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`), Tier D findings **D3** and **D6**. Both interrogate the same standing doctrine from two directions: `docs/methodology/strategy_lifecycle.md` Call 5 draws the automation/operator-GO line at **reversibility**, and names capital-to-zero (`WATCH-2→RETIRED`) as the one step requiring sign-off because it is irreversible. D3 asks whether the *reversible* side of that line is actually reversible in practice (a demoted incumbent has no coded path back up). D6 asks whether the *irreversible* outcome the line was drawn to protect can be reached by a route the line never anticipated (integer-floor arithmetic zeroing a live leg's contract count without ever touching the `RETIRED` state machine). The audit note's own cross-cutting pattern (§6) names D6 as one of six findings where "the c1 rail's live-safety interlocks are consistently described in prose... with more rigor than they are wired in code" — this Q is the formal home for that observation as it applies to the Call-system boundary specifically.

---

## Section 2 — Prior art / lineage

- **Audit note** `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md` — source of both limbs (§4 D3, D6); §3 D-gate deletions checked and **none overlap** this Q's scope (the five deletions cover DD-multiplier firm-mismatch, CI wiring gaps, sentinel non-firing, and a slippage constant — none touch the Call-system's up/down asymmetry).
- **`docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md`** (`Proposed`, unaccepted) — proposes a *down-direction* ladder rung (WATCH-1H at 0.40×). Orthogonal: it adds resolution to the descent, it does not touch whether descent reverses. Not re-litigated here.
- **`docs/adr/2026-08-06-candidate-call1-action-on-breach.md`** — governs the `CANDIDATE`-tier breach path, a different rung than D3's already-`AUTHORIZED` incumbent. Not re-litigated here.
- **Q-CAPBAND-1** (`docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md`) — structural precedent for this brief's shape: one combined H over named limbs, a binary locational read of already-recorded facts, no new spend, no constant/code edited by the brief itself.

---

## Section 3 — Question (Q-CALLBOUND-1)

**Pre-Q gate test (symptom-only rephrase):** "the Call-system's automation/operator-GO boundary is drawn on reversibility, but it is unknown whether the reversible side actually has a working reverse path, and unknown whether the one outcome reserved for operator sign-off can be reached by a mechanical route that was never gated the same way." No fix baked in — the question does not mention building a promote function, adding a sign-off gate, or wiring a warning.

**Q-CALLBOUND-1:** Does the Call-system's automation-authority boundary hold **symmetrically** — a real, operator-executable reverse path for every autonomous down-step (limb D3), and **completely** — no non-Call mechanical path reaches the one outcome (capital-to-zero) Call 5 reserved for operator sign-off (limb D6) — or does it fail on one or both axes?

---

## Section 4 — Falsifiable hypothesis (H-CALLBOUND)

**H-CALLBOUND-D3 (symmetry):** No operator-executable, criteria-gated procedure anywhere in the corpus (code, ADR, or methodology doc) restores an autonomously demoted `AUTHORIZED` incumbent leg, short of an undocumented hand-edit of a gitignored state file or the ~6-month whole-ADR Type-I-dominance revert trigger.

**H-CALLBOUND-D6 (completeness):** No repo doc, ADR, code comment, or Q-roster entry anywhere connects the sizing host's routine integer-floor-to-zero outcome to Call 5's operator-GO/NO-GO boundary as requiring, or being exempt from, that same sign-off.

**Combined H-CALLBOUND:** the boundary holds as designed only if **both** limbs hold.

**Reject H-CALLBOUND** (boundary is broken on ≥1 axis) if: **either** (a) a reverse-path procedure for D3 is found beyond the two named exceptions, or (b) the D6 vocabulary diff (§7 Phase 1) surfaces any connection between floor-to-zero and Call-5 sign-off language.
**Accept H-CALLBOUND** (boundary holds as designed, both axes) if: D3's grep returns nothing beyond the down-only citations already in Section 0, **and** the D6 diff returns no overlap between the two vocabularies.
**Ambiguous-hold** if: either grep/diff surfaces language that is topically adjacent but not conclusively on-point (e.g., a generic "promote" hit in an unrelated S5/database/test-fixture context, or a zero-contract mention that doesn't reach Call-5 vocabulary) — routes to a human read, not an automated verdict.

---

## Section 5 — Forbidden moves

- **Reading "no promote path exists" as itself a defect requiring a fix.** D3's own finding names the *reasoning gap* (σ=1.0 was chosen because the response is "cheap," but "cheap" was never tested against a real reversal cost) — not "build a promote function." Proposing code under this brief would be solution-baking the exact move Section 3's symptom-only test forbids.
- **Treating S5's bounded sandbox-up lane as if it answers D3.** S5 is confirmed (§0, `loop-s5:55`) to admit only brand-new `CANDIDATE` packets under capped concurrency — not restoration of an already-`AUTHORIZED` incumbent that Call-1 demoted. Citing S5 as a reverse path for D3 would misread a scoped exception as a general one; this is the precise oversimplification named in the task brief and is explicitly ruled out.
- **Collapsing D6 into "the zero is numerically correct, so it's fine."** The audit note is explicit that the repo has only ever asked the numerical-correctness question (`NOT-M8`); this Q asks the orthogonal governance question (should reaching zero this way require the sign-off Call 5 reserves for reaching zero the other way). Answering the numerical question again would not touch H-CALLBOUND-D6.
- **Scoring this Q on the c1 book's live risk today.** No strategy is deployed and `dry_run=true`; nothing here changes arming posture. Reading a `FALSIFIED` verdict as urgent live-risk news would overclaim — it prices a governance gap, not an active exposure.

---

## Section 6 — Gate criteria (closure verdict)

| Verdict | Trigger condition | Disposition (typed) |
|---|---|---|
| `RESOLVED` | D3 grep returns nothing beyond Section 0's down-only citations **AND** D6 vocabulary diff returns zero overlap | `INTEGRATE` — record both gaps as **confirmed-and-costless-today** (no live leg has yet been demoted or floored to zero); discharge D3/D6 from the audit note's open-findings list; no constant or code moves. |
| `FALSIFIED` | Either grep/diff surfaces a genuine reverse-path procedure (D3) or a genuine floor-to-zero/Call-5 connection (D6) | `ITERATE` — the specific gap is priced with a citation; name (do not open) a successor decision packet scoped to the surfaced gap. No constant or code moves under this brief. |
| `AMBIGUOUS-HOLD` | Either check returns a topically-adjacent but inconclusive hit (per Section 4) | `ITERATE` — record as unresolved-by-grep; re-test only if a future session needs the reverse path (D3) or a leg is actually floored to zero live (D6). |

---

## Section 7 — Execution plan (self-executing, $0/K=0 — reuse the cheap-falsifier sketches supplied)

- **Phase 0 — Rule-0 reads.** Done (Section 0).
- **Phase 1 — D3 reverse-path grep.** `rg -i "promote|re-authoriz|reauthoriz|restore.tier|restore.authoriz|WATCH.to.AUTHORIZED" core/ docs/adr/ docs/methodology/ STATE.md` — read every hit; a hit is only load-bearing if it names a procedure to move an already-demoted incumbent *back up*, not a generic use of "promote" (S5 candidate admission, test fixtures, unrelated ADRs). If it returns nothing beyond the down-only citations already in Section 0, D3 is CONFIRMED.
- **Phase 2 — D6 vocabulary diff.** Search the whole tree for zero-contract/zero-fill/`NOT-M8`/`qty_base` language (find every place the floor-to-zero fact is stated); separately search `docs/adr/`, `docs/methodology/`, `docs/rejected_candidates.md`, `docs/briefs/INDEX.md`, `STATE.md` for operator-GO/sign-off/`RETIRED`/Call-5 language; diff the two file/line sets for overlap. A hit connecting the two vocabularies falsifies H-CALLBOUND-D6; a clean miss corroborates it.
- **Phase 3 — Verdict assertion.** Apply Section 6 mechanically. Produce the closure per Section 9.

---

## Section 8 — Verdict pre-registration

Owed at operator GO, committed before Phase 1 executes. Not yet authored (this Q is named, not opened).

---

## Section 9 — Closure record format

Per `references/closure_record.md`, with the mandatory typed `## Iterate` block. `RESOLVED` → `docs/briefs/closures/Q-CALLBOUND-1-closure-resolved.md`; `FALSIFIED` → `…-closure-falsified.md`; `AMBIGUOUS-HOLD` → `…-closure-ambiguous-hold.md` with the re-test trigger named per limb.

---

## Section 10 — Audit hooks (runnable)

```bash
# D3 — reverse-path vocabulary, whole corpus
rg -i "promote|re-authoriz|reauthoriz|restore.tier|restore.authoriz|WATCH.to.AUTHORIZED" core/ docs/adr/ docs/methodology/ STATE.md

# D3 — confirm the down-only functions are still the only lifecycle-state movers
rg -n "def next_tier_down|def autonomous_demote" core/lifecycle.py

# D6 — every place the floor-to-zero fact is stated
rg -in "zero.contract|zero.fill|NOT-M8|qty_base" --type py --type md

# D6 — every place operator-GO / Call-5 sign-off vocabulary is stated
rg -in "operator.GO|sign.off|RETIRED|Call.5" docs/adr/ docs/methodology/ docs/rejected_candidates.md docs/briefs/INDEX.md STATE.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/Q-CALLBOUND-1-automation-boundary-symmetry.md --type inquire

# Section 0 anchor spot-checks
sed -n '149,166p' core/lifecycle.py
sed -n '66p;71p;213p' docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md
sed -n '86,94p' docs/methodology/strategy_lifecycle.md
sed -n '23p;55p' docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md
sed -n '280p;286,300p' ops/c1_rail/c1_sizing_host_reference.py
grep -n "NOT-M8" ops/instruments/MNQ.md
```

---

## Pre-Lock Checklist (DRAFT briefs only)

- [x] Section 0 paths read with anchors
- [x] Section 3 passes the symptom-only rephrase
- [x] Section 4 hypothesis binary
- [x] Section 5 forbidden moves genuinely tempting
- [x] Section 6 triggers specific
- [x] Section 8 pre-registration owed at operator GO
- [x] Section 10 hooks runnable
- [ ] Operator GO owed before Phase 1 — this brief is named, not opened