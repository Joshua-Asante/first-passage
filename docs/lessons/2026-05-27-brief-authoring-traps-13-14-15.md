# Lesson Capture — Brief-Authoring Traps #13 / #14 / #15

**Lesson ID:** `2026-05-27-brief-authoring-traps-13-14-15`
**Status:** **CANDIDATE** (not yet load-bearing; promotion criteria below)
**Dated anchor:** 2026-05-27 brief sequence — Q-JOINT-TAIL-1 (revs 1–3 + Phase 0 BLOCKED-RETIRED)
**Authored by:** claude.ai (Tech Advisor)
**Domain:** brief-authoring meta-methodology
**Related skill:** `brief-authoring` SKILL.md (`/mnt/skills/user/brief-authoring/SKILL.md`)

---

## §1 The three traps

Three failure modes in brief authoring surfaced sequentially across one brief sequence (Q-JOINT-TAIL-1 revs 1→2→3→Phase 0 BLOCKED) on 2026-05-27. Each was caught by CC's Rule 0 audit at the next downstream phase. The traps are distinct in mechanism but share a single root principle.

### Trap #13 candidate — Precision exceeds grounding

**Pattern:** Brief states load-bearing numerics at full precision (allocation percentages, MC anchor values, file paths) against state the author did not re-verify at authoring time. The numerics are sourced from memory or from a recent prior brief; the actual canonical state has since shifted.

**Mechanism:** Author writes "the locked MC anchor is 99.88/0.12/4.21" with confidence, because that was true a week ago. The 2026-05-23 allocation-refresh-2 ADR superseded that anchor (now 99.83/0.17/4.37) but the author's memory was anchored at the 2026-05-15 lock. The precision is technically correct *as of some past time*; the brief's grounding is implicitly that past time, not now.

**Observable signal:** specific numerics in §1 / §3 that match a prior brief's numerics but not the current `CLAUDE.md` or canonical ADR. Hash-anchored §0 reads would catch this if the §0 hashes were populated against current canonical (the brief had `<populate>` placeholders, deferring the verification).

**2026-05-27 firing:** Q-JOINT-TAIL-1 rev 1. CC revision note caught:
- `config/params.yaml` vs. canonical `config/params.toml` (extension wrong)
- ADR filename verb-order swap
- DJ30 0.75% pyr500% vs. canonical 0.70% pyr750%
- NAS100 0.45% vs. canonical 0.37% pyr1000%
- MC anchor 99.88/0.12/4.21 vs. canonical 99.83/0.17/4.37

**Procedural fix (applied at brief-authoring time, not Phase 0 time):** Before drafting §1 / §3 of any brief that references locked state, the author MUST consult the current canonical state document (`CLAUDE.md` §Strategy Reference + §Protection blocks for this codebase) and quote numerics from there, not from memory or from a prior brief.

### Trap #14 candidate — Claim-to-test exceeds methodology-can-test

**Pattern:** Brief claims to test a specific assumption or property that the methodology, as specified, does not actually deliver on. The brief reads as load-bearing; the audit reveals the headline claim is unsupported by the analysis plan.

**Mechanism:** Author frames the question imprecisely at the §1 level ("tests MC's independence assumption"). The §2 methodology, when audited, does something related but not equivalent — testing a different statistic or a different layer. The conflation is invisible at the framing level; it requires reading production code to see which independence assumption MC actually encodes vs. what the brief tests.

**Observable signal:** Pre-Q gate question (brief-authoring SKILL.md check #5: "name a symptom, not a fix") passes superficially but the symptom-name is itself imprecise. The audit signal is: "if I read the methodology and the framing side-by-side, do they describe the same test?"

**2026-05-27 firing:** Q-JOINT-TAIL-1 rev 2. CC Phase 0 §0.5 Q5 read `portfolio_mc.py:386-466` and found:
- Brief framed as testing "MC's independence assumption"
- MC has TWO distinct independence assumptions: I1 (temporal across week-blocks; tested by 2026-04-25 panel analysis) and I2 (cross-strategy within blocks; preserved by block bootstrap, not assumed)
- The brief's daily-decile co-failure test tests *neither* directly — it tests a cross-strategy property of the input panel, which MC then propagates rather than assumes

**Procedural fix:** At §1 framing, the author must explicitly enumerate what the methodology *does* test and what it *does not* test. If the framing claim is "tests X assumption," the author should write a one-sentence proof that the §2 methodology tests X — and if that proof requires reading production code to confirm, the audit must happen at authoring time, not at Phase 0.

### Trap #15 candidate — Verdict-subset existence not verified

**Pattern:** Brief defines verdict thresholds (e.g., mean ≥ 3.0 on a specific subset) without verifying at authoring time that the verdict subset is non-trivially sized. The fallback logic exists in case primary fails, but the underlying assumption (that the data permits the test at all) was never surfaced as a load-bearing assumption to check.

**Mechanism:** Author defines a verdict subset (e.g., "bottom decile of portfolio days where all 4 strategies are active") and locks thresholds against it. The data must support the subset being non-empty (and ideally N ≥ 30) for the verdict to be producible. The brief's sample-size floor catches this at Phase 0, but only after substantial structural authoring work has been committed.

**Observable signal:** verdict subset specified in §3 with no panel-shape sanity check at authoring time. The audit signal: "could a 30-line script run at authoring time tell me whether the subset is empty?"

**2026-05-27 firing:** Q-JOINT-TAIL-1 rev 3. CC Phase 0 loaded data via MC-matched aggregation and found:
- 1 of 1141 bdays had `n_active = 4` (all strategies active)
- 0 of 115 bottom-decile days had `n_active = 4`
- 3 of 115 bottom-decile days had `n_active ≥ 3` (still below N≥30 floor)
- Structural cause: day-of-week scheduling (Tuesday is the only weekday all four strategies are eligible to trade)

**Procedural fix:** For any brief whose verdict depends on a subset of data (filtered, conditioned, or stratified), the author MUST execute a panel-shape sanity check before threshold-locking. The check is cheap — a Python script reading the input data and printing the subset sizes. The output gates threshold-locking: if the subset is empty or below the floor, the brief returns to Pre-Q stage before CC handoff authoring. **This fix is applied in `2026-05-27-q-joint-tail-weekly-pre-q.md` §9.**

---

## §2 The shared root principle

The three traps share a single principle:

> **Briefs encode implicit assumptions about reality. Those assumptions need explicit verification at authoring time — not at Phase 0, not during execution, not at parent-review.**

Each trap is a layer of the same discipline:

- **Trap #13** — implicit assumption about the *current state* of canonical reference documents (allocations, anchors, paths)
- **Trap #14** — implicit assumption about the *semantics* of the methodology vs. the claim (does the test test what the framing says?)
- **Trap #15** — implicit assumption about the *shape of the data* the methodology operates on (will the verdict subset exist?)

The brief-authoring SKILL.md's existing Rule 0 (production reads before authoring) is the prototype of this discipline. Rule 0 addresses one layer (assumed semantics of production code). Traps #13/#14/#15 are three additional layers where the same principle applies.

**Generalized authoring-time discipline (candidate; not yet promoted to SKILL.md):**

> Before locking §1 framing or §3/§4 thresholds in any brief, the author must explicitly enumerate the brief's implicit assumptions about (a) current canonical state, (b) methodology-claim alignment, and (c) data shape supporting the verdict. Each enumerated assumption requires explicit verification at authoring time, sourced from current canonical state (not from memory or prior briefs).

---

## §3 Why CANDIDATE status, not load-bearing

Per `brief-authoring` SKILL.md Lesson #9 promotion criteria:

> Lessons captured without dollar anchor. Methodology lesson entries that name a pattern but no measurable cost or counterfactual. These do not graduate to load-bearing. Repair: name the dated incident AND the dollar figure (or counterfactual). Below the threshold (E1/E2 standard: single-incident >$3K, OR three firings across separate windows), the lesson stays candidate-status.

This lesson does not yet meet either bar:

- **E1 (single-incident >$3K):** Brief-authoring costs are claude.ai + CC cycles, not dollars. No direct strategy-PnL impact. Counterfactual: ~4 cycles saved had the procedural fix been in place (3 claude.ai revisions + 1 CC Phase 0 cycle). At cycle costs this is well below the dollar threshold.
- **E2 (three firings across separate windows):** Three traps fired across *one* conversation window on 2026-05-27. Not three windows. The promotion criterion requires the trap pattern recurring in independent brief sequences.

**Status today:** candidate-status. Lesson registered. Procedural fixes applied in the next brief sequence (Q-JOINT-TAIL-WEEKLY Pre-Q §9).

**Promotion path:**

- **Promote to load-bearing** if one or more of:
  - Any of Traps #13/#14/#15 fire in two additional brief sequences (total 3 separate windows = E2 met)
  - A single brief-authoring incident produces a dollar-cost event ≥ $3K (e.g., a Trap #14 firing causes an analysis to be run against the wrong methodology, producing a decision that incurs trading loss)
  - Three separate brief-authoring sessions independently apply the §2 root principle and find it improves time-to-handoff measurably (qualitative E2-equivalent)

- **Retire candidate** if:
  - Two quarters pass with no Trap #13/#14/#15 firings AND no application of the procedural fix is recorded → the discipline did not earn its keep
  - Underlying SKILL.md is restructured to fold these traps into existing #1-12 (then the candidate is absorbed, not retired)

---

## §4 Procedural fixes (applied immediately, not waiting for promotion)

These three fixes are applied immediately to the active brief sequence (Q-JOINT-TAIL-WEEKLY) even though the lesson is candidate-status. The fixes are independently justifiable; the candidate status only affects whether they become canonical brief-authoring requirements.

### Fix for Trap #13

**At authoring time, before drafting §1 / §3:** the author reads `CLAUDE.md` §Strategy Reference + §Protection blocks (or equivalent canonical state document in other codebases) and sources all locked-state numerics from there. Memory and prior briefs are *not* canonical sources. The §0 hashes are populated against current canonical at authoring, not deferred to handoff.

### Fix for Trap #14

**At §1 framing time:** the author writes a one-sentence proof of the framing claim against the methodology. "This brief tests X by computing Y on dataset Z; here is why Y on Z is a test of X." If the proof requires reading production code, the read happens at authoring, and the relevant code section is added to §0 with line ranges.

### Fix for Trap #15

**Before threshold-locking §3 / §4:** the author executes a panel-shape sanity check on the data the brief operates on. The check is a cheap script (≤30 lines, ≤30 minutes) printing subset sizes, distributions, and verdict-eligible N. If the subset is below the floor, the brief returns to Pre-Q stage before CC handoff authoring. **Embedded in Q-JOINT-TAIL-WEEKLY Pre-Q §9 as a structural requirement for this brief.**

---

## §5 Cross-references and audit hooks

### Brief sequence anchoring this lesson

- Q-JOINT-TAIL-1 rev 1 (Trap #13 firing): `archive/docs/briefs/2026-05-27-q-joint-tail-1-cc-handoff.md` (rev 1 in git history, NEEDS_CONTEXT)
- Q-JOINT-TAIL-1 rev 2 (Trap #14 firing): same brief, rev 2 in git history, NEEDS_CONTEXT
- Q-JOINT-TAIL-1 rev 3 (Trap #15 firing): same brief at archive path, rev 3, BLOCKED — scope-problem
- CC revision note (rev-1 audit): `archive/docs/briefs/2026-05-27-q-joint-tail-1-revision-note.md`
- CC Phase 0 report: `archive/docs/briefs/2026-05-27-q-joint-tail-1-phase0.md`
- Q-JOINT-TAIL-1 closure: `archive/docs/briefs/Q-JOINT-TAIL-1-closure.md`
- Q-JOINT-TAIL-WEEKLY Pre-Q (first application of fixes): `docs/briefs/programs/2026-05-27-q-joint-tail-weekly-pre-q.md`

### Related SKILL.md trap registry

- Trap #3 (Reconstructed §0): related ancestor of Trap #13. Same root: pre-handoff verification deferred.
- Trap #5 (Vague gate criteria): related ancestor of Trap #15. Same root: gate criteria specified without checking they're achievable.
- Trap #12 (Briefs that change rules during investigation): adjacent. Distinct in that #12 is mid-investigation amendment; #13/#14/#15 are pre-investigation framing defects.

### Audit hooks (this lesson)

```bash
# 1. This lesson capture committed
ls docs/lessons/2026-05-27-brief-authoring-traps-13-14-15.md

# 2. Q-JOINT-TAIL-WEEKLY Pre-Q §9 references this lesson
grep -F "Trap #15" docs/briefs/programs/2026-05-27-q-joint-tail-weekly-pre-q.md

# 3. Quarterly check: scan briefs authored after 2026-05-27 for trap firings
# (manual review at quarterly cadence)
# - Count briefs that included an authoring-time panel-shape sanity check (Trap #15 fix applied proactively)
# - Count briefs that experienced a NEEDS_CONTEXT or BLOCKED return tracing to one of #13/#14/#15
# - If the proactive-application count exceeds the firing count by ≥3:1, fixes are working
# - If firing count holds or rises, the discipline is not landing; escalate to brief-authoring SKILL.md update

# 4. Promotion check (after sufficient firings)
# - Count brief sequences in which any of #13/#14/#15 fired
# - If ≥3 separate windows, promotion criterion E2 met; update this artifact + SKILL.md
```

---

## §6 Open questions (for future audit)

1. Is the root principle in §2 *general* enough that it should fold into brief-authoring SKILL.md's Rule 0 statement, or *distinct* enough that it warrants a separate "Rule 0.5" treatment? Defer pending E2 promotion.
2. Should the §9 panel-shape sanity check (Trap #15 fix) become a structural section in ALL Pre-Q briefs (mandatory), or remain context-dependent (only when the verdict depends on a subset)? Defer pending observation across 2-3 future Pre-Q briefs.
3. Does the procedural fix for Trap #13 (consult CLAUDE.md at authoring) generalize to environments without a CLAUDE.md equivalent? In skills that operate on personal/non-engineering domains, what plays the role of CLAUDE.md? Defer pending application in non-engineering contexts.

These remain open. The lesson stays candidate-status; the open questions reinforce the not-yet-canonical disposition.

---

## Discipline check

```
[x] Lesson ID + dated anchor present (2026-05-27 brief sequence)
[x] Status explicit (CANDIDATE, not load-bearing)
[x] Promotion criteria explicit (E1 dollar threshold OR E2 three-firings-across-windows)
[x] Procedural fixes named per trap, with applied-immediately disposition
[x] Cross-references to source brief sequence + SKILL.md trap registry
[x] Audit hooks runnable (4 hooks; #3 is manual quarterly review)
[x] Open questions named (3 questions deferred pending observation)
[x] No promotion to canonical without meeting standard (no SKILL.md edit recommended yet)
```

---

**End of lesson capture.**
