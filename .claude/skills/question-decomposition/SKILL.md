---
name: question-decomposition
description: Use when a review question, ADR draft, pre-registration brief, or falsifier/kill-rule interpretation feels like a single hard yes/no but arguing it directly produces a standoff — a "does X count toward Y" dispute, a governance ruling on an ambiguous edge case, a demotion/retirement-clause reading, a Notice/Inquire framing that "could go either way," or any single verdict that would simultaneously drive reporting, escalation, and precedent. Also fires when two people share the same facts but reach opposite conclusions, or when a proposed rule change is motivated by a "gap" or "conflict" that might just be an unsearched composition of existing rules. Reasoning-structure layer only — produces a decomposition and a recombination map, not a verdict; does not replace rule-0, verify-source, fable-judge, or pre-ratification-adversarial-panel.
---

# question-decomposition — decompose before you resolve

## Overview

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

## When to use

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

## The check (cheap — run before writing the analysis)

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

## Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "It's basically one question, I'm just being thorough." | If two people share the facts and still disagree, or your intuition flips when you vary something "irrelevant," it's already two questions. |
| "The prior finding settles this." | A prior finding settles *warrant-then*, not *status-now* — and it may not even settle warrant if the weight it carries was never stated. |
| "There's no rule for this edge case, so we need a new one." | Check composition first. Most "gaps" are two existing clauses nobody tried combining. |
| "Splitting this is overkill for a small question." | Test: does the split change any downstream output or standard of proof? If not, merge back. If yes, the split was owed. |
| "I'll note my read and move on to the verdict." | A verdict on the bundled sentence still smuggles in every sub-claim the loudest side assumed. Decompose first, even briefly. |
| "Decomposing is just a way to avoid deciding." | The method terminates in a recombination map and a verdict, not infinite forking. If you're not converging, you're doing something else. |

## Red flags

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

## Worked example

**Scenario (illustrative — not a claim about any real repo document).** A pre-registered
falsifier for a candidate strategy reads: *"Retire if p99 drawdown exceeds 6% in ≥2 of 3
regime-split windows."* The candidate is sitting at `CANDIDATE` tier. Months later, someone
re-runs the regime split on a newer data vintage — one that wasn't available when the falsifier
was pre-registered — and finds 2 of 3 windows now exceed 6%. Someone opens a thread: **"Did the
candidate breach its falsifier — retire it?"**

**Why the bundled framing stalls.** One camp says "the falsifier fired, retire it now." The other
says "the falsifier was written against the original data vintage, this is a different dataset,
it hasn't fired." Both sides are citing facts — the same recomputed p99 numbers — and reaching
opposite verdicts, which is the "agreement without convergence" tell: an unnamed axis (which
vintage the falsifier's language actually scopes to) is doing the real work.

**The decomposition:**

| Axis | Question | Finding |
|---|---|---|
| Q1 — Empirical | Does p99 DD exceed 6% in ≥2 of 3 windows, computed on the *new* vintage? | Yes, measured. |
| Q2 — Semantic/scope | Does the falsifier's language bind to the pre-registered data vintage only, or to "the regime split" generically, re-evaluated on whatever data exists later? | The falsifier text is silent on vintage — under this repo's own standing rule that source silence on scope means broad, not narrow, it reads as generically re-evaluable, not vintage-locked. |
| Q3 — Clock | As of when does a breach "count" — first detection, or the pre-registration date? | First detection (today) — there is no retroactive clock; the candidate wasn't in breach before this vintage existed to measure it. |

**Recombination.** Retirement depends on Q2 alone, given Q1 is already established: if the
falsifier is read as vintage-locked, the new-vintage result is a *new pre-registration* input, not
an automatic trigger — it would need its own admitting decision. If read as generic (the finding
here), the falsifier fires now, dated to today (Q3), not backdated to the original pre-reg date.
Either way, the dispute was never "did it breach" — both camps already agreed on Q1. It was a
silent disagreement about Q2 that the bundled framing let masquerade as a factual dispute.

**What the bundled framing would have gotten wrong.** Forcing one verdict on "did it breach"
would have let whichever side won carry an unstated, unexamined scope ruling into the closure
doc — future re-readers would cite "the falsifier fired" or "it didn't" with no record of *why*,
and the actual load-bearing question (does this falsifier's language scope to a data vintage)
would never get its own decision.

## Relationship to other skills

- **`inqhiori`** — owns the methodology/when-to-investigate framing (Notice→Inquire, the pre-Q
  gate, D-S-A). Use this skill to unbundle a question *before* it enters that gate, or when an
  Inquire-phase question "could go either way" and needs its axes named before a falsifiable H
  is written.
- **`brief-authoring`** — where a completed decomposition lands as a written artifact. The
  recombination map is the natural skeleton for an ADR's or Pre-Q brief's findings section — this
  skill structures the reasoning; brief-authoring structures the document.
- **`rule-0`** and **`verify-source`** — this skill assumes both disciplines are already running.
  Rule-0 gets you reading the actual rule text and production constants instead of memory;
  verify-source gets you the right vintage/state of each fact. Decomposition then organizes what
  those disciplines surface — it doesn't replace either one, and a beautifully decomposed
  analysis built on an unverified or stale source is still wrong.
- **`fable-judge`** and **`pre-ratification-adversarial-panel`** — a decomposition is useful
  *input* to those reviews (it hands them named axes to attack instead of one fused verdict), but
  it is never a substitute for them. This skill structures an analysis; it does not verify one,
  and it renders no ratification verdict itself.
