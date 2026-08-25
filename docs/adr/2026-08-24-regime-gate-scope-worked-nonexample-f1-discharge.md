# ADR 2026-08-24 — Regime-robustness gate: worked non-example and F1 discharge

**Status:** `Accepted` — ratified via operator in-session instruction to execute the
validation-phase-cuts plan (2026-08-24); see Ratification note.
**Decision date:** 2026-08-24
**Authors:** Joshua Asante (+ Claude Code, drafter)
**Supersedes:** nothing. `docs/methodology/regime_robustness_gate.md`'s existing scope text
(lines 20–36, landed by `cd8b617` 2026-08-02) is strengthened, not superseded — the "Not
required" list is unedited in substance; this ADR adds a worked non-example and a forward rule.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [gate-stack programme audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)
(action item F1, discharged by this ADR) · [regime_robustness_gate.md](../methodology/regime_robustness_gate.md)
(owning doc, edited alongside this ADR) · [three-loop methodology binding](2026-06-12-three-loop-methodology-binding.md)
(`Accepted` — D2 STRATEGIC-Delete channel, cited below and ruled inapplicable to this ADR) ·
[G1 — prop-survivor-scoring prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
(`FROZEN` — §7 item 7 stays byte-unedited, Trap #12) ·
[candidate-1 prereg](../briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md)
(`FROZEN` — the importing document, byte-unedited)
**Layer:** methodology governance — no live-risk surface; no locked parameter; no allocation; no
arming; no production code touched. **$0 / K=0.**
**Loop-of-Record:** STRATEGIC — a methodology-doc scope-and-precedent decision governing how
future candidate pre-registrations may cite the regime gate, at the same meta-process layer the
gate itself was authored at (`docs/methodology/regime_robustness_gate.md`'s own header: "D-S-A
domain at authoring: meta-process"). Not a programme/track/instrument Delete — D2's STRATEGIC-Delete
channel (see §2 D3 below) does not govern this ADR; it is cited only to rule it out.

---

## §0 — Rule 0 reads (this worktree, 2026-08-24)

- `docs/methodology/regime_robustness_gate.md` — anchor `1a07c35` (2026-08-21). Read in full.
  Scope section ("## When this gate fires", lines 20–36) already states "Not required for: …
  Adding / removing strategies (full re-MC at locked `dd_protection` — no Pareto sweep)" — the
  gate's own text is correctly scoped. This ADR strengthens that section with a worked
  non-example; it does not repair broken scope text.
- `docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md` — anchor `1a07c35`
  (2026-08-21). Read in full. §3.1 names the finding as **G4 — "a bindingness gap in the
  importing brief, not a hard-core violation"** and §5.1 records **F1**, a **Required** follow-up
  with due date **2026-08-08** (now 16 days overdue): *"Ratify or revert the 2026-08-02 scope
  narrowing. Author an ADR … that records the ORB-MNQ/venue-native exemption, the LOCK-CANDIDATE
  conditioning, and the deleted cheapness rationale as a decision with grounds — or revert
  `cd8b617`'s three narrowings … A methodology-doc scope change may not stand on a `chore:`
  commit with no artifact."* This ADR is that artifact.
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` (**G1** in the
  audit's own shorthand) — anchor `1a07c35`. Read §7 "Freeze list" in full. **`FROZEN`**
  (operator-signed). Item 7 (line 210–211): *"Regime-robustness caveat — run the regime gate on
  the deployable expression before trusting the ceiling result (panels inherit benign-regime
  provenance)."* Stays byte-unedited by this ADR — Trap #12.
- `docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md` — anchor
  `1a07c35`. Read in full. **`FROZEN`** (operator-signed 2026-07-15; "Known Trap #12"). Lines
  213–217 import G1 item 7 as a "Regime-robustness rider (gate §7(7))" and pre-declare its
  consequence **before the gate ran**: *"a both-halves FAIL does not overturn the mechanical Part
  A read but is reported alongside it and rides into the G8 intake as a standing caveat."* Stays
  byte-unedited by this ADR — Trap #12.
- `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/{RESULTS.md,REGIME_GATE.md,G8_INTAKE.md}`
  — read in full. The rider fired: `Overall gate pass: False` (both discharge tiers, H1 bust
  ≈4.37%, bootstrap bust 95th ≈10.4%), yet `discharges_falsifier: true` was recorded and the
  candidate admitted to G8 "CANDIDATE @ 1.00× with standing regime-fragile caveat" per the
  pre-declared non-blocking posture. `RESULTS.md`'s `discharges_falsifier=True` was later
  superseded 2026-07-22 on an **unrelated** drawdown-locking-cushion defect — that withdrawal does
  not touch the bindingness/non-blocking-rider pattern this ADR documents.
- `docs/adr/2026-06-12-three-loop-methodology-binding.md` — anchor `1a07c35`. Read D2 (line 57)
  in full: STRATEGIC-Delete authority governs "Delete verdicts at programme, track, or instrument
  tier" only — see §2 D3 below for why this ADR does not need that channel.

**Amendment-first / dedup (Rule 8 sub-rule 10):**

```
$ python scripts/check_advisor_dedup.py --keywords "regime robustness gate scope ORB-MNQ candidate-1 rider bindingness"
```
Corpus hit: the gate-stack programme audit itself (F1, quoted above) — that is the existing
owner this ADR amends-into-existence-as-artifact, not a duplicate to avoid. No `docs/adr/` or
`docs/briefs/` file already performs F1's action.

**Judgment:** the true prior "owner" of this fact is the audit's own F1 row — an open, dated,
unfired action item, not a fresh proposal. This ADR is the belated F1 deliverable.

**Correction to the originating plan.** The conversation that proposed this work named the
anti-pattern's source as the **ORB-MNQ-1** pre-registration. A direct read of
`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md` (451
lines) found no reference to G1, item 7, bindingness, or `discharges_falsifier` anywhere in it —
ORB-MNQ-1 does not carry this pattern. The actual source is the unrelated Class-S
existing-strategy-book candidate-1 chain cited above, which the 2026-08-03 audit had already
independently identified and named G4. The rule this ADR states (§2 D2) is unaffected by which
campaign the worked example is drawn from; only the citation changes.

---

## §1 — Context

`docs/methodology/regime_robustness_gate.md` scopes itself ("When this gate fires") to
risk-constant Pareto-relaxation decisions — never to strategy or book additions. That scoping
text was landed 2026-08-02 (`cd8b617`) on a `chore:`-subject commit with no governing ADR — a
methodology-doc scope narrowing that the 2026-08-03 gate-stack audit found procedurally
unsupported (§3.4 item 2: "no decision artifact… `git show --stat cd8b617` touches two ADRs;
neither mentions the regime gate") even though the audit's own theory-comparison pass (§3.6)
later found the narrowing was *substantively* correct: the candidate-1 rider's criteria were
**stricter** than the canonical gate's while its **consequence** was relaxed to non-blocking —
"the counterfactual is not established… the bootstrap limb was `nan`."

Separately, one day *before* that narrowing landed, the candidate-1 pre-registration (frozen
2026-07-15) had already imported G1 item 7 — a caveat clause inside a `FROZEN` prereg whose own
scope (prop-tier book scoring, not a `dd_protection` Pareto sweep) sits squarely inside the
gate's "Not required" list — as a per-candidate rider, with its bindingness fixed at zero **in
advance of the gate ever running**. When the gate then failed on both discharge tiers, the
pre-declared non-blocking posture meant the FAIL rode into G8 as a caveat rather than as a
falsifier, and the candidate was recorded `discharges_falsifier: true`.

Neither defect is a hard-core violation — the gate's acceptance criteria were computed honestly,
and the audit's own G4 finding says so explicitly. The defect is bindingness theater: importing
an out-of-scope gate as if it were a blocking requirement, while quietly fixing in advance that a
FAIL will not block anything. Left undocumented, this is a template a future candidate
pre-registration could repeat without anyone noticing the gap between "the gate ran" and "the
gate's verdict could have changed the outcome."

**Decision driver:** close F1 (16 days overdue), and make the anti-pattern citable so a future
prereg author sees it before repeating the shape.

---

## §2 — Decision

**D1 — Ratify the 2026-08-02 scope narrowing as correct, on the grounds the audit itself
supplied.** The "Not required" list in `docs/methodology/regime_robustness_gate.md` (ORB-MNQ /
venue-native research exemption; the "risk-constant LOCK CANDIDATE is in play" conditioning on
the default-to-run rule; the removed "gate is cheap" cheapness rationale) reflects the gate's
actual jurisdiction: **"G4's hard core governs risk-constant LOCK CANDIDATE recommendations, not
strategy-book additions"** (gate-stack audit §3.1, verbatim). This satisfies F1's "ratify" branch
— no revert of `cd8b617` is warranted. **This ADR is the missing decision artifact.**

**D2 — Add a worked non-example to the gate doc, and state the forward rule.** A new
`## Worked non-example` section is added to `docs/methodology/regime_robustness_gate.md`
(alongside the existing `## Worked example: Q-DDP-1`) documenting the candidate-1 rider chain:
what was imported, how bindingness was pre-declared zero, and what the FAIL-yet-discharged
outcome looked like. **Forward rule:** a future candidate pre-registration may cite the regime
gate as informational context, but may **not** import it as a per-candidate rider whose
consequence is fixed before the gate runs. If a candidate pre-registration wants the gate to be
load-bearing, it must be run within the gate's own declared scope (§ "When this gate fires") with
its FAIL treated as a real falsifier — not imported out-of-scope with the outcome pre-negotiated
to non-blocking. A caveat that cannot change the verdict should be labeled a caveat, not scored
in a `discharges_falsifier` field.

**D3 — D2's STRATEGIC-Delete channel does not govern this ADR.** `2026-06-12-three-loop-methodology-binding.md`
D2 requires programme/track/instrument-tier *Delete* verdicts to run through programme-audit
cadence, a fired stopping rule, or explicit owner adjudication. This ADR deletes nothing — G1
item 7 and the candidate-1 rider both stay byte-unedited (Trap #12); the gate doc's own scope
text is unedited in substance. The applicable authority is F1's own action-item structure
(Owner: "Operator (ruling) + CC (ADR)"), which this ADR's ratification (operator in-session
instruction to execute the validation-phase-cuts plan) satisfies directly.

**Effective:** immediately upon Accept (2026-08-24). **$0 / K=0** — no code, no risk constant, no
allocation, no lifecycle authorization touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Revert `cd8b617`'s three narrowings (F1's other branch) | The audit's own theory-comparison (§3.6) found the narrowed scope substantively correct; reverting would re-widen the gate to cover strategy-book additions it was never meant to govern, re-introducing the ambiguity that let the candidate-1 rider be imported in the first place. |
| Edit the candidate-1 prereg or G1 item 7 in place to "fix" the anti-pattern retroactively | Both are `FROZEN`, Trap #12 (Rule 14 class 1). The record stays byte-unedited; correction is an addendum/worked-example, not an edit. |
| Do nothing (treat G4 as fully closed by the audit's own narrowed verdict) | F1 is explicitly a **Required** follow-up with its own due date, not a finding that self-closes. An audit finding is diagnosis; F1 asks for the prescriptive artifact this ADR supplies. |
| Author the worked non-example citing ORB-MNQ-1 (as originally proposed) | Verified false — see §0 Correction. Citing the wrong campaign would plant a second inaccuracy for a future reader to untangle. |

---

## §4 — Falsifier (revert trigger)

**H / Revert trigger:** a future candidate pre-registration imports the regime gate as a
per-candidate rider with pre-declared non-blocking consequence, and this ADR's D2 forward rule
fails to prevent it (i.e., the rule existed and was still not read/applied).

**Revert action:** if that recurs, author a new ADR superseding D2 in part — the forward rule as
stated (prose in a methodology doc) was insufficient; escalate to a mechanical check (a
`register_search.py`-style hard-fail on any prereg that imports `regime_robustness_gate.md`
outside its own declared scope) rather than a documentation-only fix.

**Trigger check schedule:** the next quarterly programme-audit cadence (this repo's own gate-stack
audit lineage), or the next candidate pre-registration that cites the regime gate as a rider,
whichever comes first.

---

## §5 — Forbidden moves (genuinely tempting)

- **Editing G1 item 7 or the candidate-1 prereg "to make them consistent" with this ADR** —
  both are `FROZEN`; Trap #12 forbids in-place edits to signed pre-registrations regardless of
  how clearly a later reader would benefit. The correction lives here and in the gate doc's new
  worked-non-example section, upstream of where a future reader encounters the pattern (Rule 14).
- **Widening this ADR into a general re-litigation of the gate-stack audit's other findings**
  (G1 stale labelling, G8 unfired consult, G9 dangling reference, etc.) — those are separate F-items
  with their own owners and dates in the audit's §5; this ADR closes only F1.
- **Treating the audit's G4 "narrowed on verification" language as license to soften the forward
  rule** — the audit narrowed the *severity* of the finding (bindingness gap, not hard-core
  violation), not the *prescription*. F1 still asks for a decision artifact, and D2's forward rule
  is that artifact's substance.

---

## §6 — Consequences

**Gate verdict (binary, ties to §4):** RESOLVED — the worked non-example lands, the forward rule
is stated, F1 is discharged. AMBIGUOUS/FALSIFIED conditions are covered by §4 above.

**Positive consequences:**
- Closes a 16-day-overdue Required audit follow-up (F1) with the artifact it explicitly asked for.
- Gives a future prereg author a citable, worked, non-hypothetical example of the exact shape to
  avoid, at the place they'll actually read it (the gate doc itself, not a buried audit line).
- Corrects a wrong campaign attribution (ORB-MNQ-1 → candidate-1 chain) before it could propagate
  into a permanent, git-committed record.

**Negative consequences (real cost, not theatrical):**
- One more ADR in a corpus the 2026-08-08 great-prune already flagged as growing 48→121 in 38
  days — mitigated by this ADR closing a *pre-existing* open obligation rather than opening a new
  one, and by carrying $0/K=0.

**Downstream artifacts updated (this commit):**
- `docs/methodology/regime_robustness_gate.md` — worked-non-example section added; scope section
  strengthened with a cross-reference; no numeric/procedural content changed.
- The Generate–Evaluate Throughline artifact (published, out-of-repo) — Phase "Regime-Robustness
  Gate" un-drawn as a mandatory linear step; `REGIME-FRAGILE-REJECT` terminal-state mapping
  corrected. Tracked in the companion ADR-B commit note, not duplicated here (Rule 7).

**Downstream artifacts NOT changed:**
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` (G1) — byte-unedited.
- `docs/briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md` — byte-unedited.
- `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/*` — byte-unedited (already carries its
  own 2026-07-22 supersession banner for the unrelated defect).
- Any `core/` or `ops/` code, any risk constant, any lifecycle/authorization state.

---

## §10 — Audit hooks (runnable)

```bash
python scripts/check_brief.py docs/adr/2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md --type adr
python scripts/check_adr_graph.py --regenerate-index

# F1's own audit hooks still hold (unchanged frozen thresholds — expect all 4 tiers, expect the ceiling numbers).
grep -n "Bulenox_100K\|Tradeify_Select_100K\|MFFU_Rapid_100K\|BluSky_Premium_100K" \
  docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md   # expect all 4

# The gate's scope text is unedited in substance — only strengthened.
grep -n "Adding / removing strategies" docs/methodology/regime_robustness_gate.md   # expect 1 hit, unchanged

# The worked non-example section exists and cites the correct campaign, not ORB-MNQ-1.
grep -n "Worked non-example" docs/methodology/regime_robustness_gate.md   # expect 1 hit
grep -n "ORB-MNQ-1" docs/methodology/regime_robustness_gate.md   # expect 0 hits in the new section
```

---

## Ratification note

**Ratified by:** Joshua Asante, in-session direct instruction to execute the validation-phase-cuts
plan carried forward from a prior conversation (2026-08-24).

**§6-class preconditions at ratification:** §0 populated with anchors and the wrong-campaign
correction (done, this commit) ✓ · F1's own action item quoted verbatim and satisfied ✓ · both
`FROZEN` source documents confirmed byte-unedited ✓

**Not licensed by this ratification:** any edit to `core/`, `ops/`, `dd_protection`, allocations,
or any `FROZEN` pre-registration; any re-opening of the candidate-1 chain's own 2026-07-22
supersession; any claim that the regime gate is now mandatory (or now-more-optional) for any
decision class beyond what its own "When this gate fires" section already stated before this ADR.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Initial authoring and ratification — F1 discharge, worked non-example, wrong-campaign correction (ORB-MNQ-1 → candidate-1 chain). | Claude Code, operator-directed |
