---
name: refine-question
description: Use when the user's question leaves a load-bearing dimension unresolved — "best"/"good"/"worth it" with no stated metric, an unstated candidate pool or venue/tier/clock, an unclear decision the answer feeds, or an unspecified evidence standard (synthesize existing results vs spend fresh runs/K) — and different resolutions would change the answer or the work. Also fires on "refine my question", "improve my question", "sharpen this question". Skip when the question is already sharp on all four dimensions. Methodology/UX layer; changes no repo state.
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
