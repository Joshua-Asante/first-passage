---
name: refine-question
description: Use when the user's question leaves a load-bearing dimension unresolved — "best"/"good"/"worth it" with no stated metric, an unstated candidate pool or venue/tier/clock, an unclear decision the answer feeds, or an unspecified evidence standard (synthesize existing results vs spend fresh runs/K) — and different resolutions would change the answer or the work. Also fires on "refine my question", "improve my question", "sharpen this question". Skip when the question is already sharp on all four dimensions. Also use when a review question, ADR draft, pre-registration brief or falsifier/kill-rule reading feels like one hard yes/no but arguing it directly stalls — a "does X count toward Y" dispute, an ambiguous-edge governance ruling, two people sharing the facts but reaching opposite verdicts, or a proposed rule motivated by a "gap" that may be an unsearched composition of existing rules: decompose into separable axes and a recombination map before resolving (merged from question-decomposition 2026-10-24). Methodology/UX layer; changes no repo state.
---

# refine-question — pick the sharp question before spending the answer

## Overview

An ambiguous question silently answered is a reading **chosen for** the user. This skill makes
the choice explicit: diagnose the ambiguity, present genuinely different sharpened readings as
select-box options (`AskUserQuestion`), let the user pick, then answer the picked question.
Refinement costs one click; an answer to the wrong question costs the whole answer.

## Fire test

Fire when ≥1 dimension below is unresolved **and** different resolutions change the answer or
the work. Otherwise pass through silently — no "your question was fine" ceremony.

1. **Decision link** — what decision does the answer feed?
2. **Success criterion** — "best/good/worth it" by what metric (e.g. 1−P(bust), post-funding
   expectancy, p99 DD, time-to-pass)?
3. **Cohort/scope** — which candidate pool, venue/tier key, clock (EOD vs intraday-honest),
   window?
4. **Evidence standard** — synthesize existing RESULTS, or spend fresh runs/K?

## The move (one AskUserQuestion call)

1. Identify the dominant ambiguity. Resolve what standing decisions already foreclose — a
   reading barred by an ADR is flagged as barred in its description, never offered as live.
2. Present 2–4 **candidate refined questions**, each committing to a different resolution.
   Recommended reading first, labeled "(Recommended)". Each description states what the option
   assumes/commits to.
3. Orthogonal unknowns (rare) ride along as a second question in the same call.
   `multiSelect: true` only when readings are complementary ("answer both"), not exclusive.
4. The selection is the confirmation: restate the refined question in one line, then route to
   the owning domain skill and answer. No second confirmation pass.

## Option quality bar

Each option is a different **resolution**, never a paraphrase. Test: would two options produce
materially different answers or work? If not, merge them. Max 4. "Other" free-text is the
built-in escape hatch — don't add an "Other" option.

## Rationalizations

| Excuse | Reality |
|---|---|
| "Context makes the intent clear enough" | Then the fire test fails and you pass through. If you're choosing among readings, it wasn't clear. |
| "I'll note my interpretation and answer" | A stated assumption still spends the full answer on an unpicked reading. The select box costs one click. |
| "More options = more helpful" | >4 or paraphrase variants push the real choice into noise. Different resolutions only. |
| "The user can correct me after" | The correction costs a full re-answer. Refinement is the cheap path. |

## Red flags

- About to answer a question containing "best", "good", "worth it", or "should we" with no
  stated metric.
- Writing "assuming you mean…" in an answer instead of asking.
- Options that differ in wording but would produce the same answer.
- Offering as live an option a standing ADR already bars.

## Related skills

- **`inqhiori`** — owns full Inquire-phase question formulation (pre-Q gate, D-S-A); this skill
  is the lightweight conversational front door. If refinement reveals a gated investigation,
  hand off there.
- **`brief-authoring`** — if the refined question is really a Pre-Q brief in disguise, hand off.
- **`verify-source`** — factual premises embedded in the question get source-state checks before
  the options are built.

## Decompose a contested question before resolving it

Merged 2026-10-24 from the retired `question-decomposition` skill ([tombstone](../../../docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation)). Use it when the question is clear to the asker but contested on the merits; the select-box move above handles questions the asker left ambiguous. Produces a decomposition and a recombination map, not a verdict; it does not replace Rule 0, `verify-source`, `handoff-verify` or `pre-ratification-adversarial-panel`. A bundled question inside an oversize brief comes here before `work-decomposition` cuts the work.

A question that "could go either way" is usually not one hard question — it's two to four
separable questions wearing one sentence. Arguing the bundled sentence directly produces
positional standoffs where both sides are technically right about different sub-claims. Arguing
the parts produces convergent, auditable findings, because each part gets the evidentiary
standard it actually earns instead of borrowing the standard of whichever sub-claim is loudest.

**The discipline: treat every felt paradox as a hypothesis that it contains multiple axes.
Extract candidate axes, check that each can flip independently of the others, answer each under
its own standard, then write down explicitly which final calls depend on which sub-answers.**
(This framing was sharpened against an external draft on the general technique; the method has
to justify itself here on repo grounds, not on that provenance.)

Two sub-questions are separable if either can flip without forcing the other to flip. A genuine
coupling is never eliminated by decomposing — it's named and carried into the recombination map.

### When to use

Fire when a question resists a clean verdict and shows one of these tells. The right-hand column
is the axis pair the pattern usually hides.

| Pattern | Tell — what the bundled question looks like | Separates into |
|---|---|---|
| **Semantics vs. consequences** | "Does this breach the rule?" — arguers are really disputing what happens *after* a finding (report/escalate/retire), not what the rule's text covers. | (a) does the rule's text reach this case, (b) given either finding, what's the prescribed disposition. |
| **Empirical vs. semantic vs. anchoring** | "Did the event count?" — factual doubt and interpretive doubt are being traded against each other, and a prior finding is treated as settling both at once. | (a) what actually happened, (b) does the rule's definition cover events of that kind, (c) how much weight does the prior finding retain — binding, presumptive, or merely informative. |
| **Status vs. warrant** | A closed finding is attacked with facts that postdate it, as if it had been unreasonable *when made* — or defended as "reasonable at the time" to protect its truth *now*. | (a) status — is the underlying condition true now, (b) warrant — was the finding justified on the evidence available at the time it was made. Warranted-then and false-now can both be true. |
| **Transparency vs. content** | "Was the disclosure/citation handled correctly?" — the review fixates on whether a source was described precisely while nobody checks what actually moved, or vice versa. | (a) was the description of sources/mechanism/limits accurate, (b) did the substantive thing actually happen (data moved, trade fired, threshold crossed). Either can fail alone. |
| **Exhaustiveness assumption** | "There's no clause for this case, so it's unresolvable / the rules conflict." | Drop the assumption that the rule set is exhaustive or that overlapping clauses must conflict; check whether two existing clauses already *compose* to decide it. |
| **Fact-time vs. judgment-time (clock)** | "Is it compliant?" with no stated instant — deadline disputes, "we didn't know then," retroactive-rule arguments. | Peg every predicate to a specific clock and information state: compliant *as of when*, *known by whom*, *under which vintage of the data*. |
| **Process vs. outcome** | Due process invoked against a substantively fine outcome, or a bad outcome excused by a clean process. | (a) was the procedure followed, (b) is the result correct/acceptable on the merits. They license different remedies (redo vs. accept-with-note). |
| **Case vs. rule** | Resistance to a sensible one-off outcome because "it sets a bad precedent," or a good general rule rejected for hardship in one instance. | Decide the instance under the rule as it stands; log the rule-level concern as a separate, explicitly flagged recommendation. |
| **Merits vs. burden** | "Is it true?" when the real dispute is who had to produce evidence and whether they did. | What the record shows on the merits vs. who bore the burden and whether it was met — a failed burden can decide the issue with no merits finding at all. |

Also fire on the generic signals: mixed argument registers (empirical evidence answering what is
really a definitional dispute), agreement on facts with disagreement on verdict, a missing time
or data-vintage index, or one verdict that would simultaneously feed a closure doc, a lifecycle
change, and a precedent citation.

### The check (cheap — run before writing the analysis)

- [ ] Rewrite the question as 2–4 sub-questions, each answerable by **one** evidence type
      (empirical / semantic / procedural-historical / normative).
- [ ] For each pair of sub-questions, ask: can A flip while B holds? Keep the flips; write down
      any pair that's genuinely coupled instead of forcing it apart.
- [ ] Time-index and vintage-index every predicate: as of when, under which data/rule vintage,
      known by whom.
- [ ] Test the exhaustiveness assumption: does dropping "the rulebook has no row for this" reveal
      a composition of existing clauses that already covers it?
- [ ] Run the live-question probe: "if I could learn exactly one more fact, which would most
      change the call?" If it isn't what the framed question asks about, re-anchor before writing.
- [ ] Draw the recombination map: which final outputs (retire / reopen / notify / no-op) depend on
      which sub-answers — before drafting the verdict prose.

### Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "It's basically one question, I'm just being thorough." | If two people share the facts and still disagree, or your intuition flips when you vary something "irrelevant," it's already two questions. |
| "The prior finding settles this." | A prior finding settles *warrant-then*, not *status-now* — and it may not even settle warrant if the weight it carries was never stated. |
| "There's no rule for this edge case, so we need a new one." | Check composition first. Most "gaps" are two existing clauses nobody tried combining. |
| "Splitting this is overkill for a small question." | Test: does the split change any downstream output or standard of proof? If not, merge back. If yes, the split was owed. |
| "I'll note my read and move on to the verdict." | A verdict on the bundled sentence still smuggles in every sub-claim the loudest side assumed. Decompose first, even briefly. |
| "Decomposing is just a way to avoid deciding." | The method terminates in a recombination map and a verdict, not infinite forking. If you're not converging, you're doing something else. |

### Red flags

- Two reviewers hold the same facts and the same rule text and still land on opposite verdicts.
- The debate keeps citing different *kinds* of reasons (a factual objection answered with a
  procedural one, or vice versa) without either side noticing the mismatch.
- A single yes/no is about to drive a closure doc, a lifecycle-tier change, and a precedent
  citation all at once, with no sub-finding written down for any of the three separately.
- "The rules conflict here" or "there's no clause for this" asserted without checking composition.
- A predicate in the draft ("is compliant," "counts," "breached") with no stated clock or data
  vintage attached.
- An old finding being retried against new facts as if it had been wrong when made, with no
  warranted-then / false-now split offered.
