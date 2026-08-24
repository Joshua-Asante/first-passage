# T1's 2026-08-08 firing on the venue-binding axis is dispositioned as a bootstrap artifact, not a falsification — `venue-binding-axis-t1-disposition`

Filename: `docs/adr/2026-08-24-venue-binding-axis-t1-disposition.md`.

**Status:** `Proposed` — drafted at operator request ("author a superseding ADR for T1"); the ruling is Claude Code's, not yet operator-ratified. Flips to `Accepted` on operator GO (§7 Phase 0).
**Decision date:** 2026-08-24
**Supersedes:** `2026-08-05-strategy-venue-binding-axis.md` in part — §4 T1's disposition and prospective applicability window only. §2 (the three-level axis), §3, §5, §6, T2–T4, and the `Accepted` status token are untouched.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Claude Code (ruling + authoring, per operator direction to close the open T1 gap) — pending Joshua's ratification (§7 Phase 0).
**Related:** [`2026-08-05-strategy-venue-binding-axis.md`](2026-08-05-strategy-venue-binding-axis.md) (the ADR this partially supersedes) · [`.claude/skills/brief-authoring/references/adr.md`](../../.claude/skills/brief-authoring/references/adr.md) (Forbidden-move-2 pattern: "silent amendment of the revert trigger is `p`-hacking... author a fresh ADR that supersedes this one") · [`2026-08-08-adr-ceremony-tiering.md`](2026-08-08-adr-ceremony-tiering.md) (tier test — this is full-ceremony, limb 4: amends doctrine) · [`docs/superpowers/plans/2026-08-23-venue-binding-registry-implementation.md`](../superpowers/plans/2026-08-23-venue-binding-registry-implementation.md) (already-executed implementation plan this ruling does not disturb)
**Layer:** governance / ADR-graph discipline. **No `core/`, Pine, allocation, `dd_protection`, `LEG_MAP`, lifecycle-multiplier, or rail change.** No live behavior changes; this is a ruling on a falsifier disposition only.

---

## §0 — Rule 0 reads (production-source verification, all executed 2026-08-24)

| Source | Anchor (`git log -1`) | What it pins |
|---|---|---|
| `docs/adr/2026-08-05-strategy-venue-binding-axis.md` (full read, header + both addenda + change history) | `21302e9` 2026-08-23 | §4 T1's exact trigger text and threshold (L188-199); the "reachability, stated honestly" note naming F2 (due 2026-08-08) as T1's first test (L197); §7 Phase 0 ("operator ratifies Proposed → Accepted. Nothing below runs first") and Phase 1 (registry creation, gated on Phase 0); Addendum 2026-08-14 conceding "T1 likely fired" while Status stayed `Proposed`; Addendum 2026-08-22 flipping Status to `Accepted` via "fresh GO" while explicitly declining to claim T1 did not fire; header fields `Supersedes: none` / `Superseded-by: none` still current. |
| `.claude/skills/brief-authoring/references/adr.md` | `92e896e` 2026-08-23 | The three canonical revert-action options (supersede / revert to prior config / escalate to re-investigation); the `Supersedes: X in part — <clause>` mechanics (X stays hot/`Accepted`, gains `Superseded-in-part-by`); Verification block note that A2 (edge reverse-match) is skipped while the superseding ADR is `Proposed`. |
| `docs/adr/2026-08-08-adr-ceremony-tiering.md` | `01afc64` 2026-08-21 | Tier test limb 4 ("creates or amends doctrine: a rule, gate, falsifier threshold, or convention that binds future work") — this ADR amends a falsifier's disposition and applicability window, so full ceremony applies. |
| `scripts/check_adr_graph.py` | `d7a8a7f` 2026-08-22 | A1 (header fields), A2 (edge reverse-match, skipped while `Proposed`), A6 (INDEX sync) — confirms mechanics above by reading the checker directly, not assuming the template's prose. |
| `docs/superpowers/plans/2026-08-23-venue-binding-registry-implementation.md` | `353200d` 2026-08-23 | Confirms Task 4 ("Append one Change History row... T1 still acknowledged. Do not flip any other Status wording that would imply T1 un-fired") already executed — matches the Change History row already present on the target ADR; confirms S1 (the 2026-08-07 environment-ratification ADR) was never rewritten to retroactively claim an edition transition, which this ADR also does not do. |

**Gitignore pre-flight.** `**/*.pine` is ignored; not read or cited here — this decision sits entirely at the governance layer.

---

## §1 — Context

The 2026-08-05 venue-binding-axis ADR (`2026-08-05-strategy-venue-binding-axis.md`) writes a strict, binary falsifier for its own hypothesis: "H is FALSIFIED — and this ADR is reverted by a superseding ADR — if any trigger fires" (§4, L188), with T1's threshold at "any 1 occurrence" (L192) and exactly one named revert action: "author a superseding ADR. Never edit this §2 in place" (L199).

T1 fired. The F2/F3 venue-scope decision (recorded via `2026-08-07-loop-s1-environment-ratification.md`) resolved in prose, with no edition-state transition, because the registry T1 needs did not exist — the ADR itself was still `Proposed`, unratified, until 2026-08-22. Two addenda concede this in writing: 2026-08-14 ("T1 likely fired... This ADR was never ratified; `ops/venue_editions/` was never created") and 2026-08-22 ("T1... is acknowledged as already fired... it does not claim T1 did not fire and does not rewrite S1"). Neither addendum executes §4's named revert action. Instead, the response was a Rule-14 status-framing addendum plus an operator GO that flips `Proposed → Accepted` directly — a fourth path outside the three the ADR template names (supersede / revert to prior config / escalate to re-investigation). The target ADR's own header still reads `Supersedes: none` / `Superseded-by: none`; no supersession has ever been authored for this trigger.

**The bootstrap defect, named precisely.** The ADR's own §4 "reachability, stated honestly" note states: "T1 is reachable *this week* — F2 falls due 2026-08-08 and is exactly the shape of decision that must produce an edition transition" (L197) — written 2026-08-05, three days before F2's due date. But the same ADR's §7 sequences Phase 0 (operator acceptance) strictly before Phase 1 (registry creation): "Phase 0 — acceptance. Operator ratifies `Proposed → Accepted`. Nothing below runs first" (L254). Acceptance did not happen until 2026-08-22, fourteen days after F2's due date, and the registry (Phase 1) did not land until 2026-08-23. T1's own reachability window opens on a date that necessarily precedes the earliest date the axis it tests could possibly have existed to be consulted. This is not an edge case discovered in hindsight — it is derivable from the ADR's own text at the moment of authoring, and it means T1's "any 1 occurrence" firing on 2026-08-08 tests whether an *unaccepted, unbuilt* axis was consulted, which is a different question from whether the axis — once live — fails to prevent the premise-dead-propagation class of defect it was built for.

**Decision driver (one sentence):** the target ADR names one specific, unexecuted revert action for a falsifier its own text concedes has fired twice in writing; leaving that unexecuted treats every other ADR's identically-structured "H is FALSIFIED... revert action: author a superseding ADR" clause as advisory rather than binding, which this ADR closes out for this one instance rather than leaving as precedent.

---

## §2 — Decision

**Decision:** T1's 2026-08-08 firing (recorded via the F2/F3 decision in `2026-08-07-loop-s1-environment-ratification.md`) is dispositioned as **INAPPLICABLE, not FALSIFYING**. T1's trigger condition presupposes a live, consultable axis; the axis was not `Accepted` (§7 Phase 0) — let alone had its registry built (§7 Phase 1) — until 2026-08-22/23, after the decision T1's own reachability note named as its first test. An ADR that is not yet accepted cannot be "not consulted" in any sense that falsifies its own hypothesis H. This disposition applies to the 2026-08-08 occurrence only.

**T1's applicability window is amended prospectively:** T1 (§4, `2026-08-05-strategy-venue-binding-axis.md`) now reads, for all decisions from this ADR's effective date forward, "applies to venue-scope decisions recorded **on or after 2026-08-22** (the target ADR's Phase 0 acceptance date) without an edition-state transition." Threshold (any 1 occurrence), check point (at the decision), and every other trigger (T2, T3, T4) are **untouched** — T1 is exactly as strict for any decision from 2026-08-22 onward as it was written to be for any decision at all. Only the pre-acceptance bootstrap window is excused, and only for the one occurrence that fell inside it.

**Effective:** immediately upon acceptance (§7 Phase 0 below).
**Scope:** `2026-08-05-strategy-venue-binding-axis.md` §4 T1 only. Does not touch §2 (the three-level axis itself), §3, §5, §6, §7, T2–T4, or the `Accepted` status token, which all stand as ratified 2026-08-22.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Revert the axis entirely** (T1's literal §4 default: "H is FALSIFIED... reverted by a superseding ADR"). | Substantively contradicted by everything that happened since acceptance: §7 Phase 1–3 landed 2026-08-23 (the registry exists and is non-trivially referenced by `CLAUDE.md`, `docs/methodology/strategy_lifecycle.md`, the third-leg spec, and the live viable-strategy generation pipeline). Reverting now would orphan real, in-use structure over a bootstrap-timing technicality the ADR's own 2026-08-14 addendum already conceded does not impugn "the underlying B3 layer-leak analysis." A literalist revert here repeats, in destructive form, the exact "gate nobody agreed to maintain" failure mode this programme's audits already flag — except backwards, discarding working structure instead of accreting unmaintained structure. |
| **Leave as-is** (the 2026-08-22 addendum's "acknowledged, not reopened" framing, no further action). | This is the status quo the operator asked to close. §4 names one specific revert action; not executing it, twice, sets a precedent that an ADR's own falsifier can be waived by a status-flip addendum — which would make the identical "H is FALSIFIED... revert action: author a superseding ADR" clause on every other ADR in the corpus read as decorative rather than binding. |
| **Silently narrow T1's threshold or reachability language in place.** | Forbidden by the target ADR's own §5 and by Known Trap #12: "silent amendment of the revert trigger is `p`-hacking at the methodology layer... author a fresh ADR that supersedes this one; never edit this ADR's header or body in place." This ADR is exactly that fresh ADR — the alternative is the thing the rule exists to prevent. |
| **Escalate to full re-investigation** (the third canonical revert-action option). | Considered and ruled out as disproportionate: the defect is a self-contained sequencing contradiction fully derivable from the target ADR's own §4 and §7 text (no new data, measurement, or campaign needed). A re-investigation would spend cycles re-deriving a conclusion already available on the page. |

---

## §4 — Falsifier (revert trigger)

**Hypothesis (H2, binary):** *T1's 2026-08-08 firing was a bootstrap-timing artifact — a consequence of the decision predating the axis's own acceptance and registry — and not evidence that the venue-binding axis, once live, fails to prevent the premise-dead-propagation and layer-leak defects it names in its own §1.*

**H2 is FALSIFIED — and this ADR is reverted by a superseding ADR — if any trigger fires:**

| # | Trigger | Threshold | Check |
|---|---|---|---|
| **T1'** | A venue-scope decision recorded **on or after 2026-08-22** (post-acceptance) is again recorded without an edition-state transition, having to fall back to prose. This is the *original* T1 condition, now unambiguously live. | Any 1 occurrence | At the decision |
| **T2'** | The bootstrap-window carve-out is invoked for a decision that in fact postdates 2026-08-22, i.e. used to launder a genuine post-acceptance non-consultation as "historical." | Any 1 occurrence | At the disposition |

**Revert action:** author a superseding ADR. Never edit this §2, or `2026-08-05-strategy-venue-binding-axis.md` §2/§4/§5, in place.

**Trigger check schedule:** T1' at the next venue-scope decision (F3 successor-venue election, or any future venue withdrawal/de-scope) and at the original ADR's own 2026-11-08 quarterly audit. T2' is checked at the time any bootstrap-window disposition is claimed — the bright line is the target ADR's own Phase-0-acceptance date (2026-08-22, machine-readable from its Change History table), not a judgment call made fresh each time.

---

## §5 — Forbidden moves (under this ADR)

- **Rewriting `2026-08-07-loop-s1-environment-ratification.md` (S1) to retroactively claim it performed an edition transition.** Already named as forbidden in `docs/superpowers/plans/2026-08-23-venue-binding-registry-implementation.md` ("Do not rewrite S1 as an edition transition to 'fix' T1") and repeated here for the same reason: that would falsify the historical record rather than correctly disposition it. This ADR closes the gap by ruling on T1's *applicability*, not by rewriting what S1 said.
- **Treating this disposition as license to relax T1 going forward.** T1' is exactly as strict as the original T1 — any 1 occurrence, at the decision — for every venue-scope decision from 2026-08-22 onward. Only the pre-acceptance window is excused, and it is excused exactly once, for the one occurrence that fell inside it.
- **Reopening or editing §2 (the three-level axis), §3, §5, §6, or §7 of `2026-08-05-strategy-venue-binding-axis.md`.** This ADR's scope is the §4 T1 disposition only. The axis itself, its registry, and its `Accepted` status are ratified and untouched.
- **Treating an operator-GO status flip as a standing substitute for a named §4 revert action on any other ADR's fired falsifier.** This ADR closes this one instance under its own reasoning (a diagnosable bootstrap-timing defect, argued in §1–§2); it does not establish "operator GO overrides §4" as a repo-wide convention, and citing it as precedent for skipping another ADR's revert action without the same kind of diagnosis is out of scope.

---

## §6 — Consequences

**Positive consequences:**
- Closes the outstanding gap: T1 fired, was conceded twice in writing, and now has an actual ruling instead of an unresolved acknowledgment.
- Restores the "H FALSIFIED → superseding ADR" mechanism's credibility as a binding commitment rather than one skippable by a status-flip addendum — relevant to every other ADR in the corpus carrying the identical clause.
- Gives T1 an unambiguous, machine-checkable live date (2026-08-22) instead of an open-ended "acknowledged, not reopened" state that a future reader could misread either as "still open" or "fully resolved."

**Negative consequences (real cost, not theatrical):**
- One more ADR in the corpus tracking a single-trigger disposition; the target ADR's header now carries a forward pointer (`Superseded-in-part-by`) indefinitely.
- A reader of `2026-08-05-strategy-venue-binding-axis.md` alone (without following the pointer) still sees the unresolved 2026-08-14/2026-08-22 addenda language ("acknowledged as already fired... does not claim T1 did not fire") — the header pointer is load-bearing for finding the actual disposition.

**Risks (probabilistic, distinct from costs):**
- **Laundering risk:** a future non-consultation could be misclassified as "before acceptance" when it postdates 2026-08-22. Mitigated by T2' above and by anchoring the carve-out to a single, already-recorded date rather than a re-litigated judgment call each time.

**Downstream artifacts that need updating (Phase-2 sweep, derived not recalled — raw output in §10):**
- `docs/adr/2026-08-05-strategy-venue-binding-axis.md` header — gains `Superseded-in-part-by` line; Change History gains one row. **§2/§4/§5 body byte-unchanged** (Trap #12). Executed only on this ADR's acceptance (§7 Phase 1), not before — while this ADR is `Proposed`, the reverse edge is not mandatory (per `check_adr_graph.py` A2 skip rule).
- `docs/adr/INDEX.md` — regenerated via `python scripts/check_adr_graph.py --regenerate-index` (machine-owned; never hand-edited) once this ADR lands, to pick up both the new row and the target ADR's `Superseded-in-part-by` note.

**Explicitly ruled unaffected (with reason):**
- `CLAUDE.md:129-130` — cites the axis as `Accepted`; unaffected, `Accepted` status is unchanged by an in-part supersession.
- `ops/venue_editions/Tradeify_Select_100K.md:5` — cites the ADR as owner of §2.6/§7 Phase 1; unaffected, Phase 1 registry status is unchanged.
- `docs/methodology/strategy_lifecycle.md:24` — cites "Accepted 2026-08-22" + registry; unaffected.
- `docs/spec/2026-07-27-third-leg-target-spec.md:9-11,357` — cites §2.5 ownership; its own line-357 "T1" is that spec's *own*, unrelated falsifier-table entry (cost-law hurdle), not this ADR's T1; unaffected.
- `docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md:13,104-153` — generic citation of the venue-binding ADR; its own T1/T4/T5 (L104-153) are that ADR's own, unrelated falsifier table (eval-activity limb, cadence instrument); unaffected.
- `docs/adr/2026-08-23-strategy-coldstore-phase-b.md:10,85-108` — generic citation; its own T1 (L85, "silent sizing / rail bleed") is that ADR's own, unrelated falsifier table; unaffected.
- `docs/superpowers/plans/2026-08-23-venue-binding-registry-implementation.md` — already executed (Phase 1-3 landed, Task 4's change-history row already present on the target ADR); consistent with this ruling since it never rewrote S1; no edit needed.
- `docs/adr/2026-08-14-repo-public-visibility-transition.md:207` — a one-time, already-executed scrub-account-ID instruction; unaffected.
- `docs/notes/audits/programme-audit/2026-08-05-claim-alignment/{README,01-diagnostics,02-blockers,04-misleading,05-cosmetic,06-operator-judgement,07-followups,08-hooks}.md` — dated, point-in-time audit records; not edited per standing repo convention (audits are historical snapshots, not living documents).
- `docs/ltm/notes/archive/sessions/SESSIONS-2026-Q3.md`, `docs/ltm/notes/archive/state/STATE-decision-index-pre-2026-08-23.md` — cold archive; not edited per the Great Prune retention convention (retrievable via `git show`, never rewritten).

---

## §7 — Implementation plan

- **Phase 0** — operator ratifies `Proposed → Accepted`. Nothing below runs first.
- **Phase 1** — on acceptance: append `Superseded-in-part-by` header line to `docs/adr/2026-08-05-strategy-venue-binding-axis.md` (immediately below its existing `Superseded-by: none` line) and one Change History row. No edit to that ADR's §2/§4/§5 body text.
- **Phase 2** — grep-sweep already executed at authoring time (§10); disposition table in §6 stands as the record. Re-run at Phase 0 to confirm no new hits landed between authoring and acceptance.
- **Phase 3** — run `python scripts/check_adr_graph.py --regenerate-index`; run `python scripts/check_brief.py <this file> --type adr`; both must pass before this ADR's Status is considered live.

Policy-only otherwise — no mechanical edits beyond the two header/index touches above.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Phase-2 sweep, re-run (should match authoring-time output above)
grep -rln "2026-08-05-strategy-venue-binding-axis" --include="*.md" . 2>/dev/null | grep -v "^\./docs/adr/2026-08-05-strategy-venue-binding-axis.md$"
grep -rln "T1 fired\|T1 already fired\|T1 acknowledged\|T1 remains acknowledged" --include="*.md" . 2>/dev/null | grep -v "^\./docs/adr/2026-08-05-strategy-venue-binding-axis.md$"

# 2. Reverse edge lands correctly once Accepted (expect a match after Phase 1)
grep -n "Superseded-in-part-by" docs/adr/2026-08-05-strategy-venue-binding-axis.md

# 3. T2' — bright-line acceptance date is still what this ADR cites (expect 2026-08-22 present)
grep -n "2026-08-22" docs/adr/2026-08-05-strategy-venue-binding-axis.md | head -3

# 4. S1 was not rewritten to claim an edition transition (expect no "edition" hit inside S1's own body)
grep -n "edition\|EDITION" docs/adr/2026-08-07-loop-s1-environment-ratification.md

# 5. T1' reachability — next venue-scope decision after 2026-08-22 produces an edition transition or fires T1'
grep -n "edition\|EDITION" STATE.md | head

# 6. Graph + INDEX integrity
python scripts/check_adr_graph.py
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-24-venue-binding-axis-t1-disposition.md --type adr
# Expected: RESULT: well-formed

# ADR lifecycle graph
$ python scripts/check_adr_graph.py
# Expected: exit 0; A2 skipped while this ADR is Proposed

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/adr/2026-08-05-strategy-venue-binding-axis.md
$ git log -1 --format="%h %ci" -- docs/adr/2026-08-08-adr-ceremony-tiering.md
$ git log -1 --format="%h %ci" -- .claude/skills/brief-authoring/references/adr.md
$ git log -1 --format="%h %ci" -- scripts/check_adr_graph.py

# Supersede chain integrity (in-part; reverse edge mandatory only once Accepted)
$ grep -A1 "Supersedes" docs/adr/2026-08-24-venue-binding-axis-t1-disposition.md
$ grep -n "Superseded-in-part-by" docs/adr/2026-08-05-strategy-venue-binding-axis.md
# Expected while Proposed: no reverse edge yet (A2 skip). Expected after Phase 1: bidirectional match.
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring (Claude Code, at operator request to close the open T1 gap). Status `Proposed` pending operator ratification. | Claude Code |
