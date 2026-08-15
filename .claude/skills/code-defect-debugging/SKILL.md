---
name: code-defect-debugging
description: Use this skill whenever Joshua suspects a deterministic code defect in `first_passage` — Python or shell code returning wrong values, scripts crashing, output magnitudes implausible vs a defensible reference, or cross-platform output diverging, where re-runs with identical inputs reproduce the failure. Triggers on phrases like "this is broken", "the output is wrong", "why is this returning X", "this number is off", "script crashed", "MC results look implausible", "P&L looks inflated", "verification failed". Canonical anchor: TV <30-day JPY ~153× P&L inflation (code/feed defect, not methodology). Hand off to `inqhiori` for statistical anomalies (WR/PF drift, anchor trades, regime sensitivity), `ooda-loop` for tactical/tempo decisions, `pinescript-v6` for Pine source bugs, `prop-firm-challenge` for live-ops or Rule-0 facts. Not for "is this strategy edge real" — that is INQHIORI; this skill is "is the code returning what its inputs imply" only.
---

# Code-Defect Debugging

Narrow skill for deterministic code defects in the `first_passage` Python/shell stack. Sibling to `inqhiori` (structural / statistical investigation) and `ooda-loop` (tactical / recoverable / tempo). Filling a real gap: the existing methodology skills are wrong tools for "why is this function returning the wrong number" — they would treat a code bug as if it were a falsifiable hypothesis, demand a Pre-Q gate, and waste budget on investigation discipline that doesn't apply to deterministic code.

The 4-phase structure is adapted from `obra/superpowers:systematic-debugging`. The adaptation: Joshua's stack has no unit-test scaffold to run RED-GREEN-REFACTOR against, and code defects are validated against historical CSV ground truth + Monte Carlo invariants, not against assertions. Phases 1–3 transfer directly; Phase 4 is reshaped around his actual verification gates.

---

## 0. Skill selection — which loop is this?

The first decision before any phase. Misrouted work is the single largest cost in this domain — INQHIORI applied to a code bug burns hours; this skill applied to a methodology anomaly produces false confidence.

| Symptom | Skill | Why |
|---|---|---|
| Function returns a value inconsistent with its declared inputs | **this skill** | Deterministic code; root cause is in code |
| Script crashes / raises exception | **this skill** | Code defect by definition |
| Output magnitude implausible vs known reference (JPY ~153×, P&L 100× expected) | **this skill** | Almost always feed/encoding/units bug, not strategy edge |
| Cross-platform output differs (TV vs Pepperstone vs Python) for same logical input | **this skill** | Code or feed-handling defect |
| Strategy WR / PF deviates from baseline despite no parameter change | **inqhiori** | Statistical anomaly in unchanged code; investigation question |
| Regime sensitivity unexpected (anchor trades, tail behavior) | **inqhiori** | Methodology / hypothesis territory |
| Live trade decision under time pressure | **ooda-loop** | Tactical / recoverable / tempo |
| Pine source returns wrong value | **pinescript-v6** | Different language and runtime; that skill owns Pine |
| dd_protection live calibration vs theoretical | **prop-firm-challenge** | Live-ops domain |

**Tiebreaker:** if the output divergence persists across re-runs with identical inputs, it is a code defect (this skill). If re-runs produce different outputs from the same code+inputs, the variance is the question and that is INQHIORI territory.

**Tiebreaker 2:** if you can state "the function should return X given inputs Y and Z" without invoking statistical reasoning, this skill applies. If the expected output requires a falsifiable hypothesis to predict, INQHIORI applies.

---

## 1. Phase 1 — Evidence before fixes

**Blocking rule: no fix proposed before Phase 1 completes.** This is Rule 0 transposed to debugging. The 04-17 dd_protection cycle and the JPY ~153× P&L bug both share the same failure mode: a fix attempted before the failing input/output was actually observed and logged. Symptom-based fixes are the failure mode this skill exists to prevent.

Phase 1 outputs, in order:

**1.1 Reproduction.** A minimal command that triggers the bug deterministically. If the bug is intermittent, the intermittence itself is the question — log every variable input (data file timestamp, Python version, env vars, working directory) until reproduction is deterministic. Intermittent-claim-without-reproduction is a Phase 1 failure.

**1.2 Inputs and outputs at the failure boundary.** For the failing function or pipeline stage:
- What did it receive?
- What did it return?
- What was expected, and on what authority?

The "authority" matters. Expected values come from one of: (a) a reference implementation (Pine source, a prior version), (b) a closed-form calculation Joshua can sanity-check by hand, (c) a baseline output from a CSV reconcile that's already locked, or (d) a Monte Carlo invariant (e.g., bust attribution sums to 100%). Expected values from "it felt about right last time" are not authority and the bug investigation is degraded by accepting them.

**1.3 The git anchor.** `git log --oneline -1 -- <file>` for every file in the suspect path. If the bug is new, the diff between the last-known-good commit and HEAD is the highest-leverage read. If the bug has always been there, the git anchor still goes in the Phase 1 log so future audits know what they're looking at.

**1.4 Phase 1 closes when:** reproduction is deterministic AND inputs/outputs at the boundary are logged AND expected values have authority cited. Until then, no fix.

---

## 2. Phase 2 — Component-boundary logging

The load-bearing technique. Adapted from `systematic-debugging`. The principle: instrument every component boundary in the suspect path, run once to gather evidence, then analyze the evidence to identify which component is failing.

**For the `first_passage` stack specifically, component boundaries are:**

- **Function call boundaries** — between `portfolio_mc.py` modules (data loader → bootstrap engine → bust-attribution aggregator). Log inputs entering and outputs exiting at each.
- **File-format boundaries** — CSV in, DataFrame out; DataFrame in, dict out; dict in, JSON file out. The serializer/deserializer pair is the highest-frequency source of subtle bugs (encoding drift, NaN handling, integer-vs-float, timezone parsing).
- **Feed boundaries** — Pepperstone CSV in, Python in-memory representation out. The 2026-04 OANDA→Pepperstone transition history shows that feed-boundary bugs hide as "the methodology must be wrong"; they are not.
- **Unit boundaries** — points-vs-pips, percentage-vs-decimal, contract-value-vs-notional, base-vs-quote. The JPY ~153× incident was a unit-boundary bug at the feed-to-P&L interface.
- **Session/timezone boundaries** — chart-TZ vs UTC, NY-close-anchored vs broker-day. Guardian's session filter timing was corrected on prior pass; the same class of bug can recur.

**Logging procedure:**

```
For each component boundary in the suspect path:
  Log (in this order):
    1. Type of input (DataFrame? dict? path string?)
    2. Shape / size / length
    3. First and last 3 rows (or first 3 keys)
    4. dtype / encoding / unit metadata if available
    5. Any field that should match an external invariant (timestamp range, expected sum, expected count)
  Then on exit:
    Same five logs for the output.
```

**Run once, then analyze.** Do not log + theorize + log + theorize. The discipline is one full evidence-gathering pass, then read the gathered evidence as a complete artifact. Theorizing mid-log produces selective evidence.

**The component that fails is the one whose output stops matching expectation.** If `data_loader` outputs a DataFrame with the right shape, dtypes, and timestamp range, but `bootstrap_engine` outputs a result with the wrong magnitude, the bug is at or downstream of the bootstrap entry. Working forward through the boundaries narrows the suspect range deterministically.

**Phase 2 closes when:** the failing component (the boundary at which expectation diverges from observation) is identified by name. Not "somewhere in the MC pipeline" — `portfolio_mc.bootstrap_engine.compute_panel_thirds`, line range, specific input value, specific wrong output.

---

## 3. Phase 3 — Hypothesis testing

Once the failing component is identified, form a hypothesis about WHY it fails. The hypothesis must be specific enough that a one-line test can falsify it.

**Forbidden hypothesis patterns:**

- "Maybe the function isn't handling edge case X correctly" — too vague. Sharpen to: "If input is `<specific value>`, function returns `<specific wrong value>` instead of `<specific right value>`, because `<specific line>` does `<specific operation>` when it should do `<specific other operation>`."
- "Floating-point rounding" — almost never the answer in this stack at the magnitudes involved. If proposed, falsify it first with a quick magnitude check before exploring.
- "Pandas weirdness" — same. Sharpen or discard.

**Permitted hypothesis patterns (anchored to past bugs in this stack):**

- Unit conversion missing or doubled
- Encoding/dtype mismatch at a deserialization boundary
- Off-by-one in window-slicing or panel indexing
- Implicit timezone conversion (system-local vs UTC vs chart-TZ)
- Reference-vs-copy mutation in a DataFrame operation
- Integer division where float was intended
- Default argument value that's not what the caller assumed
- Feed-side data quality issue masquerading as code (verify by re-running on the canonical CME futures TV export under `core/data/tv_exports/cme/`)

**Test the hypothesis with one minimal input that distinguishes it from alternatives.** Do not test by applying a fix — test by injecting the hypothesized input and observing the hypothesized wrong output. The test confirms "this is the cause"; the fix comes after.

---

## 4. Phase 4 — Fix and verification

Once the hypothesis is confirmed, the fix follows. Joshua's stack has no unit-test framework to RED-GREEN-REFACTOR against, so verification is structured around the existing gates instead.

**Fix discipline:**

1. **Smallest possible change.** The fix is the inverse of the falsified hypothesis. If `compute_panel_thirds` was using integer division, the fix is `/` → `/.` (or explicit float cast), nothing else. Refactoring "while we're in here" is forbidden — that is scope creep into a CC-handoff §3 forbidden move at the wrong layer.

2. **Reproduction now produces correct output.** Re-run the Phase 1.1 reproduction command. The output must match expectation. If not, the hypothesis was wrong; return to Phase 3.

3. **Phase 1 baseline still passes.** Any locked baseline (CSV reconcile baselines: G 201t / DJ30 224t / A 123t / NAS 200t) must still match. A fix that resolves the immediate bug but breaks a locked baseline is a structural change, not a code defect fix — escalate to INQHIORI.

4. **MC engine regression unchanged.** If the fix touches any code in the MC path (`portfolio_mc.py`, `core/data/tv_exports/cme/` consumers, dd_protection logic), re-run `python -m pytest tests/core/test_mc_synthetic_engine.py -q`. The 99.83/0.17/4.37 figures are historical record, not a live pin. Drift in the synthetic-engine pins means the fix changed structural behavior — escalate to INQHIORI for re-calibration.

5. **Diff scope check.** Diff the fix against HEAD. Files modified should match the fix's logical scope exactly. Any surprise file changes are forbidden-move leakage at the IDE level.

6. **Twin sweep.** A defect found at one site is presumed to recur wherever the construct was copied, until a search says otherwise. Name the exact wrong construct (the expression, not the symptom), `rg` the whole repo for it, and record verbatim in the report: `TWINS: searched <pattern> — found <N> other sites: <files|none>`. Fix them or list them; a completeness claim with no search behind it is verification theater. Grounding: the `daily_loss_pct: None` division TypeError lived at four sites (`dd_protection.py`, `core/mc/modes.py`, `core/mc/simulation.py`, `core/mc/preflight.py`) and was fixed as a class in PR #356 only because all four were swept. (Adopted 2026-07-15 from the fable-method port — see `docs/notes/2026-07-15-fable-skills-port.md`.)

---

## 5. Phase 4.5 — Architecture questioning (mandatory after 3 failed fixes)

If three fix attempts have failed (Phase 3 hypothesis confirmed, Phase 4 fix applied, Phase 1.1 reproduction still fails or a different test breaks), STOP. Do not author Hypothesis 4.

The pattern is: three good-faith fixes failing in sequence is not "I need a smarter hypothesis." It is "the architecture of the code in this region is wrong." The fix is at a different level than the bug.

**Convergence note.** This rule appears independently in `inqhiori` §6 (tail-methodology-exhaustion: 3 hypotheses falsified → question the question). Same invariant, different domain. The methodology version applies to investigation; the code version applies to debugging. Both say: when three serious attempts at the same level fail, the level is wrong.

**What 4.5 looks like for this skill:**

- Read the broader region of the failing code (the parent module, the calling code, the data the failing code consumes).
- Ask: is the function being asked to do something it cannot do correctly given its current shape? (The function may be correctly implementing a specification that itself is wrong.)
- Ask: is the bug actually a code defect, or has the reframe revealed it as a methodology question? (If yes, hand off to INQHIORI — the loop selection in §0 was wrong.)
- Document the architecture concern as an ADR candidate (via `brief-authoring`), then escalate.

**Do not skip 4.5 by trying a 4th hypothesis.** That is the failure mode this rule prevents.

---

## 6. Anti-patterns and traps

**6.1 Symptom fixes.** "The number is wrong, so I'll add a correction factor." Almost always wrong. Symptom fixes propagate the bug into a future incident with a different presentation. Same anti-pattern as overlay-on-physical-facts at the methodology layer (Iran-Hormuz). The fix that makes the immediate symptom go away while leaving the cause unresolved is failure even if the test passes.

**6.2 Defaulting to "Pandas weirdness" or "floating-point rounding."** These are real categories but extremely rarely the actual cause in this stack at the magnitudes involved. Treat them as last-resort hypotheses, not first-resort.

**6.3 Trying to fix without reproducing.** "I think the bug is in X, let me just patch it." This converts a Phase 1 failure into a guessing game. Reproduce first. Always.

**6.4 Conflating data quality with code defect.** A bug that looks like code is sometimes a feed quality issue. Verification: re-run the failing operation against the locked CME futures TV export from `core/data/tv_exports/cme/` (the current canonical feed; Pepperstone retired 2026-08-02). If the bug reproduces, it is code. If it disappears, the input data is the question and this skill is the wrong tool — handoff to `trade-csv-reconcile`.

**6.5 Treating a methodology anomaly as a code defect.** The mirror of 6.4. If a strategy's WR or PF has shifted unexpectedly with no code change, the code is doing what it has always done and the question is statistical. Hand off to `inqhiori`. The signal: was there a recent change to the relevant code? If no, this skill does not apply.

**6.6 Not capturing the lesson.** A code defect that consumed >2 hours of debugging and identified a class of failure (not a one-off typo) graduates to a methodology lesson via `brief-authoring` lesson-capture. The JPY ~153× P&L bug is in the registry because of this discipline; future class-failures should follow the same path.

---

## 7. Worked example — the JPY ~153× P&L bug (retrospective)

The TradingView <30-day backtest P&L inflation bug is the canonical case for this skill.

| Phase | What happened | What this skill would have prescribed |
|---|---|---|
| 0 — selection | Initially treated as "is the strategy actually this profitable?" — a methodology question | Selection rule should have routed to this skill: output magnitude implausible vs reference (the matching CSV-export run showed ~1×, not ~153×) |
| 1 — evidence | Reproduction found: TradingView ≤29-day backtests produced wildly inflated JPY-pair P&L | Phase 1 closes here; bug is deterministic, inputs are TV time window + JPY pair |
| 2 — boundary | Boundary identified: TV's pip-value calculation for JPY pairs differs by a factor in short windows | Component-boundary logging would have surfaced this as: "P&L per pip × pip count" — pip value 100× off |
| 3 — hypothesis | "TV uses a different pip-value normalization for short windows on JPY pairs" — confirmed | Hypothesis is testable: same backtest at 31 days produces sane numbers |
| 4 — fix | "Don't use TV <30-day backtests for P&L" — encoded as a standing rule | Fix is at the consumer (the user) since the source (TV) is not modifiable |
| Lesson | Captured: "TV <30-day JPY backtests unreliable (~153× P&L inflation)" | Lesson capture is correct; this is the canonical class-failure for this skill |

The bug took longer than it should have because it was initially routed as a methodology question. With this skill in place, the routing decision in §0 ("magnitude implausible vs reference, deterministic across re-runs → this skill") would have shortcut the methodology investigation and gone straight to component-boundary logging at the TV-output layer.

---

## 8. Hand-off rules

When this skill exits — either because the bug is fixed, or because §0 selection was wrong and a different skill applies:

| Hand off to | When |
|---|---|
| `inqhiori` | Phase 4.5 reveals the "code defect" was actually a methodology question; or the fix produces a structural change that needs full INQHIORI discipline |
| `ooda-loop` | A code defect surfaced under live time pressure; the immediate decision is tactical (skip this trade, halt this strategy); the code fix is deferred to a later session under this skill |
| `pinescript-v6` | The bug is in Pine source, not Python |
| `prop-firm-challenge` | The "bug" is actually a live-ops or Rule-0 fact (the dd_protection rule is doing what it's supposed to do; the user's expectation was wrong) |
| `brief-authoring` lesson capture | A class-failure (>2 hours, identifies a category of bug not a one-off) graduates to the lessons registry |
| `brief-authoring` ADR | Phase 4.5 architecture concern that warrants a structural decision artifact |
| `trade-csv-reconcile` | The bug turns out to be data-quality, not code |

---

## 9. What this skill does not change

- Strategy parameters (Guardian / Striker / Aegis / NAS locks remain).
- Allocations or dd_protection calibration (those are `prop-firm-challenge` / INQHIORI).
- Methodology framework rules (those are `inqhiori`).
- Pine source (that is `pinescript-v6`).

This skill governs how code defects get diagnosed and fixed. It does not modify what production code is supposed to do — that is governed at the layer above.

---

## 10. Audit hooks

Quarterly review questions for this skill's effectiveness:

- How many code defects in `first_passage` were diagnosed in the period? (rough cadence — `git log --oneline | grep -i 'fix\|bug'`)
- Of those, how many followed Phase 1 evidence-first discipline vs symptom-fixed? (read commit messages and PR-equivalent notes)
- How many were initially mis-routed to INQHIORI before landing here? (signal: skill is undertriggering or its description is unclear)
- How many graduated to lesson captures? (signal: are class-failures being recognized as such)
- How many invoked Phase 4.5? (signal: is the architecture-questioning rule firing when it should)

If this skill's routing is being missed (mis-routes >1× per quarter), revise the description per `skill-creator`'s undertriggering guidance.
