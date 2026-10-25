---
name: code-defect-debugging
description: Use this skill whenever Joshua suspects a deterministic code defect in `first_passage` — Python or shell code returning wrong values, scripts crashing, output magnitudes implausible vs a defensible reference, or cross-platform output diverging, where re-runs with identical inputs reproduce the failure. Triggers on phrases like "this is broken", "the output is wrong", "why is this returning X", "this number is off", "script crashed", "MC results look implausible", "P&L looks inflated", "verification failed". Canonical anchor: TV <30-day JPY ~153× P&L inflation (code/feed defect, not methodology). Hand off to `inqhiori` for statistical anomalies (WR/PF drift, anchor trades, regime sensitivity), `pinescript-v6` for Pine source bugs, `prop-firm-challenge` for firm-rule/MC/dd_protection facts, `c1-rail` for live-ops facts. Not for "is this strategy edge real" — that is INQHIORI; this skill is "is the code returning what its inputs imply" only. Also use at the moment any fix is written or reviewed — "fix this", "make the test pass", "green the CI", "add a retry", "just guard it", "wrap it in try/except", "widen the parser", a diff adding a None-check, default, retry, broad except or looser schema, or a script that handles an error by exiting 0 — and whenever the first visible error is a TypeError, None, KeyError, schema or parse error: §11 bans band-aids until the mechanism is named and requires a ROOT CAUSE / FIX / VERIFICATION block with before/after evidence (merged from root-cause-first 2026-10-24).
---

# Code-Defect Debugging

Narrow skill for deterministic code defects in the `first_passage` Python/shell stack. Sibling to `inqhiori` (structural / statistical investigation) (the `ooda-loop` skill was retired 2026-10-24; live execution decisions follow `c1-rail`). Filling a real gap: the existing methodology skills are wrong tools for "why is this function returning the wrong number" — they would treat a code bug as if it were a falsifiable hypothesis, demand a Pre-Q gate, and waste budget on investigation discipline that doesn't apply to deterministic code.

The 4-phase structure is adapted from `obra/superpowers:systematic-debugging`. The adaptation as first written (2026-04): the stack then had no unit-test scaffold to run RED-GREEN-REFACTOR against, so code defects were validated against historical CSV ground truth + Monte Carlo invariants. `tests/` has since grown a pytest suite (`make test`), so Phase 4 now also requires a regression test that reproduces the original failure (item 7). Phases 1–3 transfer directly; Phase 4 is reshaped around the actual verification gates.

---

## 0. Skill selection — which loop is this?

The first decision before any phase. Misrouted work is the single largest cost in this domain — INQHIORI applied to a code bug burns hours; this skill applied to a methodology anomaly produces false confidence.

| Symptom | Skill | Why |
|---|---|---|
| Function returns a value inconsistent with its declared inputs | **this skill** | Deterministic code; root cause is in code |
| Script crashes / raises exception | **this skill** | Code defect by definition |
| Output magnitude implausible vs known reference (JPY ~153×, P&L 100× expected) | **this skill** | Almost always feed/encoding/units bug, not strategy edge |
| Cross-platform output differs (TV vs Python) for same logical input | **this skill** | Code or feed-handling defect |
| Strategy WR / PF deviates from baseline despite no parameter change | **inqhiori** | Statistical anomaly in unchanged code; investigation question |
| Regime sensitivity unexpected (anchor trades, tail behavior) | **inqhiori** | Methodology / hypothesis territory |
| Live trade or rail decision under time pressure | **c1-rail** | Operational; follows AGENTS.md §Live-execution posture |
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

The load-bearing technique for wrong-value bugs. Adapted from `systematic-debugging`. For crash-shaped bugs (an exception raised deep in a call chain) and state-shaped bugs (a wrong value with no obvious writer), §11's backward call-chain trace and first-unintended-write hunt replace or precede this forward pass. The principle: instrument every component boundary in the suspect path, run once to gather evidence, then analyze the evidence to identify which component is failing.

**For the `first_passage` stack specifically, component boundaries are:**

- **Function call boundaries** — between `portfolio_mc.py` modules (data loader → bootstrap engine → bust-attribution aggregator). Log inputs entering and outputs exiting at each.
- **File-format boundaries** — CSV in, DataFrame out; DataFrame in, dict out; dict in, JSON file out. The serializer/deserializer pair is the highest-frequency source of subtle bugs (encoding drift, NaN handling, integer-vs-float, timezone parsing).
- **Feed boundaries** — CME futures TV export CSV in (`core/data/tv_exports/cme/`; Pepperstone retired 2026-08-02), Python in-memory representation out. The 2026-04 OANDA→Pepperstone transition history shows that feed-boundary bugs hide as "the methodology must be wrong"; they are not.
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

Once the hypothesis is confirmed, the fix follows — through the §11 band-aid gate: a guard, default, retry, broad `except`, `check=False` or widened parser is not a fix until the mechanism is named in one sentence, and the report carries its `ROOT CAUSE:` / `FIX:` / `VERIFICATION:` block. Verification is structured around the existing gates plus the regression test in item 7.

**Fix discipline:**

1. **Smallest possible change.** The fix is the inverse of the falsified hypothesis. If `compute_panel_thirds` was using integer division, the fix is `/` → `/.` (or explicit float cast), nothing else. Refactoring "while we're in here" is forbidden — that is scope creep into a CC-handoff §3 forbidden move at the wrong layer.

2. **Reproduction now produces correct output.** Re-run the Phase 1.1 reproduction command. The output must match expectation. If not, the hypothesis was wrong; return to Phase 3.

3. **Phase 1 baseline still passes.** Any locked baseline (CSV reconcile baselines: G 201t / DJ30 224t / A 123t / NAS 200t) must still match. A fix that resolves the immediate bug but breaks a locked baseline is a structural change, not a code defect fix — escalate to INQHIORI.

4. **MC engine regression unchanged.** If the fix touches any code in the MC path (`portfolio_mc.py`, `core/data/tv_exports/cme/` consumers, dd_protection logic), re-run `python -m pytest tests/core/test_mc_synthetic_engine.py -q`. The 99.83/0.17/4.37 figures are historical record, not a live pin. Drift in the synthetic-engine pins means the fix changed structural behavior — escalate to INQHIORI for re-calibration.

5. **Diff scope check.** Diff the fix against HEAD. Files modified should match the fix's logical scope exactly. Any surprise file changes are forbidden-move leakage at the IDE level.

6. **Twin sweep.** A defect found at one site is presumed to recur wherever the construct was copied, until a search says otherwise. Name the exact wrong construct (the expression, not the symptom), `rg` the whole repo for it, and record verbatim in the report: `TWINS: searched <pattern> — found <N> other sites: <files|none>`. Fix them or list them; a completeness claim with no search behind it is verification theater. Grounding: the `daily_loss_pct: None` division TypeError lived at four sites (`dd_protection.py`, `core/mc/modes.py`, `core/mc/simulation.py`, `core/mc/preflight.py`) and was fixed as a class in PR #356 only because all four were swept. (Adopted 2026-07-15 from the fable-method port; port record is in the private archive.)

7. **Regression test pins the original failure.** A fix that lands in repository code lands with a test that reproduces the Phase 1.1 symptom, fails on the pre-fix code and passes after — not a test of the fix's new behaviour in isolation. Grounding: fleet Packet C (`docs/SESSIONS.md` 2026-09-04f) guarded `scripts/repo_hygiene.py`'s subprocess call and shipped no missing-`git` test, so `git` absent exited 0 with an empty report; the fix round removed the guard and `test_build_report_without_git_raises` in `tests/test_repo_hygiene.py` now pins the raise. A fix PR whose only test would also pass on the pre-fix code has not verified anything. When the confirmed defect lives in an unmodifiable external source (the JPY case in §7: TradingView's own calculation), the fix is a consumer-side rule and its verification is two artifacts instead: the captured failing evidence (the offending input and the observed wrong output, pinned where the rule is recorded) and a consumer-side test that fails when the rule is absent — the guard rejects the offending input class — plus the lesson capture in §6.6. A synthetic test that does not exercise the original failure is theater in either case.

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
| `c1-rail` | A code defect surfaced under live time pressure; the immediate operational decision follows the rail's safety invariants; the code fix is deferred to a later session under this skill |
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

---

## 11. Root-cause gate — before writing or reviewing any fix

Merged 2026-10-24 from the retired `root-cause-first` skill (operator ruling; [tombstone](../../../docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation)). It fires on any repair or review, not only on deterministic defects routed through §0.

Fix the mechanism, not the symptom. A guard, a default, a retry, a broader `except` or a wider
parser makes the failure disappear from the place you are looking and keeps it everywhere else,
now silent. This skill is the gate at the moment of repair or review: no band-aid until the
mechanism that makes the failure inevitable is written down in one sentence, then the smallest
fix at the source, then a regression test that reproduces the original symptom.

Dated repo burns this gate would have caught at the fix:

- **2026-09-04f** — fleet Packet C wrapped `scripts/repo_hygiene.py`'s `_run` in a guard (a §5
  forbidden move) and shipped no test for the missing-`git` case; with `git` absent, `--json`
  exited 0 with an empty report. FALSIFIED on the §6 criterion, fix round C1 owed. The fixed shape
  is the opposite of the guard: the subprocess call raises, and
  [`tests/test_repo_hygiene.py`](../../../tests/test_repo_hygiene.py)
  `test_build_report_without_git_raises` pins it.
- **2026-09-02d** — P&L booked on a non-session date was silently dropped by a `bdate_range`
  reindex: six trades of real losses omitted from committed grids. Round 1 only disclosed it;
  restoring the rows moved bust in most finalist cells.
- **2026-08-31a** — an MNQ-side `overnight_ohlc` used `~is_rth` as its overnight mask and
  silently included the same day's post-close window, bars from *after* the outcome the
  conditioner predicts; the MYM twin never had the bug.
- **M-23** ([index](../../../docs/methodology/LESSONS_INDEX.jsonl)) — a config *key* passed to a
  joblib worker let the worker silently re-resolve the defective on-disk config; detected four
  days later. The visible error was never at the site of the cause.
- The faithfulness-audit lesson in
  [`methodology_lessons.md`](../../../docs/methodology/lessons/methodology_lessons.md): "Do NOT
  let a faithfulness audit silently discard the source-of-truth artifact in favor of its own
  recompute on a mismatch; the mismatch is the signal." The weird input is the clue.

### When it fires

| Trigger | What you are about to do |
|---|---|
| "Fix", "make it pass", "green the CI", a red required check on a PR you own | Gate before the first edit. |
| The first error is `TypeError` / `None` / `KeyError` / `JSONDecodeError` / schema or parse failure | Treat it as a symptom; trace up to who produced the value. |
| "Flaky", "intermittent", "passes on re-run" | A race, an ordering dependence or an environment difference. A retry hides it; §1.1 says the intermittence *is* the question. Not this row: an *evidence-backed* infrastructure failure — a runner, service or network outage read from the job log — which `babysit` step 4 reruns with the reason recorded and no code change. "It passed the second time" is not that evidence. |
| Reviewing a diff (Codex round, `handoff-verify` post-execution judging, a fleet return) that adds a guard, default, retry, broad `except`, `check=False`, `errors="ignore"` or a looser schema | Ask for the named mechanism; without one the change is REFUTED on that ground. |
| A hook, startup path, boot-time cache, restore/migration, worker pool, background refresher or rewriter is anywhere in the suspect path | Run the first-unintended-write hunt below. |

### Banned until the mechanism is named

| Move | Why it is banned | Repo burn |
|---|---|---|
| **None / empty guard** — `if x is None: return`, `.get(k, default)` where `k` must exist, `or 0` | Hides the signal. Ask *why* it is None and fix that writer. | The `daily_loss_pct: None` TypeError lived at four sites; the class fix was the writer, not four guards (Phase 4 item 6). |
| **Catch-and-continue** — `except Exception: pass / return ""`, swallowing a non-zero exit | Turns a loud bug into a silent one. | 2026-09-04f Packet C `_run` guard: missing `git` → exit 0, empty report. |
| **Retry / timeout inflation / sleep** | Flaky means a real race or order dependence. Retry hides it. | — (calibration pending a dated firing) |
| **Parser / schema widening** — accept both shapes, coerce, `errors="ignore"`, `errors="replace"` where bytes matter | The weird input is the clue. Find who produced it. | Faithfulness-audit lesson: the mismatch is the signal. |
| **Default-on-error / silent drop** — an empty report on failure, a reindex that drops rows, a fallback value nobody sees | Synthetic success masks the failure from everyone downstream. | 2026-09-02d `bdate_range` reindex. |
| **Pin, baseline or test edit** to green a run | fable-method Step 4.6: never. | — |
| **Correction factor / overlay** on the output | §6.1: the bug returns with a different presentation. | JPY ~153× P&L inflation. |
| **Unexplained fix** — "it passes now" with no mechanism | Then it is not fixed. You moved the bug. | — |

**Designed fail-open is not a band-aid.** Two doctrines this repo holds on purpose: the rail
"may fail closed on risk-add, never fail closed on risk reduction" — `exit` / `flat` relay best
effort and raise a CRITICAL operator notification when evidence cannot be written
([M1 ADR](../../../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) item 6); and
edit-time hooks and report-only scanners fail open for the completed edit while *emitting a
finding* ([skill lifecycle](../../../scripts/README.md); the Sentinel `preregistration_scan` in
`ops/sentinel/scan.py`). The test that separates doctrine from band-aid keeps the *protected action* and the *diagnostic*
apart — all three required of a new or reviewed path:

1. the open path is named in an owner — ADR, README, or the function's own docstring;
2. taking the open path emits a visible finding, notification or non-zero status somewhere a
   human reads, and the diagnostic's own status stays distinct from a clean result: "NOT CHECKED /
   could not run" is never reported as "checked, none found" (the SKIP-versus-PASS convention in
   `scripts/check_skill_deploy_sync.py`);
3. the protected action may proceed — an edit completes, a report-only scan does not block a
   commit, a risk-reducing exit relays — but a *fix* never converts the failure it was written for
   into a success exit code or an empty-but-valid artifact.

Under that reading the edit hook passes (owner: the skill-lifecycle README; validator failures go
to stderr; the edit proceeds). An existing documented path is grandfathered by its owner, not by
this test — where it conflates "could not run" with "none found", as the Sentinel's `no git → []`
in `ops/sentinel/scan.py` does, it is not a template for new code, and tightening it is its owner's
separate change, never a drive-by inside a fix PR. A `pass` that has no owner, no finding and turns
a failure into success is a band-aid whatever the comment above it says.

### Procedure

1. **State the observed failure concretely.** Exact error text, assertion or log line; the
   command that produced it; the commit. A deterministic defect in this repo's Python or shell
   code — a wrong value *or* a crash — runs Phase 1 first (deterministic
   reproduction, expected-value authority, git anchors; its §0 routes script crashes to itself)
   and comes back here for the trace and the fix gate. A Pine defect never enters that Phase 1:
   §0 routes Pine to `pinescript-v6`, which runs this gate in its own
   runtime. This step stands alone at review time, when Phase 1 has already run, or when the
   failing artifact is not code (a doc gate, a manifest, a hook payload).
2. **Reconstruct the intended contract.** Three sentences: the expected behaviour; the invariant
   it rests on; what definitely did *not* happen. The contract comes from the read source under
   fable-method's `INTENT` authority order (operator > ADR/LOCK > tests > current code), never
   from the failing code's own shape.
3. **Trace the real path** with whichever technique fits the bug's shape. Prefer logs, tests and
   traces over inference.
   - **Backward call-chain trace** — crash-shaped bugs, an exception deep in a chain. Symptom
     site → the line that threw → who called it → what value was passed at each level → where the
     bad value originated → what changed there (`git log -1 -- <file>`, `git log -S<token>`, the
     last-known-good diff). When you cannot read it, instrument: at the site log the value, the
     cwd, the *name* and presence of the relevant env var and `traceback.format_stack()`; run
     **once**, read the whole capture, then reason (Phase 2's run-once
     rule). Never log an env var's value: a token, password, DSN or API key written to a test
     or CI log is a leak (fable-method Step 4.6, AGENTS.md: never touch secrets). When two
     candidate values must be told apart, log a fingerprint (length plus a hash prefix), never
     the bytes.
   - **First-unintended-write hunt** — state-shaped bugs, a wrong value present and nobody
     obviously wrote it. Ask whether the write, mutation or request should have happened at all.
     List the canonical source of truth and every competing one (operational_rules §7;
     [firm-constants single source](../../../docs/adr/2026-06-06-firm-constants-single-source.md);
     M-24's independent re-encodings). Audit the hidden writers: `SessionStart` / `PostToolUse`
     hooks, startup code, boot-time caching, restore and migration paths, worker pools that
     re-import config, background refreshers, retries, rewriters. Non-explicit writes are suspects
     until proven intentional. The root cause is the *first* unintended side effect, not the last
     error.
4. **Name the mechanism** in one sentence that makes the failure inevitable: "given `<input or
   state>`, `<site>` does `<operation>`, so `<wrong output>`." Cannot → you are at a symptom; go
   up one level.
5. **Reject band-aids explicitly.** For each banned move you were tempted by, write why the
   mechanism makes it wrong. In the rare case the mechanism *proves* a fallback correct, it is now
   designed fail-open: give it an owner and a finding per the three-part test above.
6. **Fix at the source of the bad state**, smallest change, correct layer first: upstream logic
   over a downstream contract; never make a contract more permissive unless the observed payload
   is proven intended in the final design. An architectural concern found on the way goes to a
   Notice log or ADR candidate, not into the fix.
7. **Verify against the original failure.** One rule for every artifact step 1 admits: evidence
   that the original symptom reproduces *before* the fix and is absent *after* it, in the
   strongest form the artifact admits — never a synthetic check that would also pass on the
   pre-fix state. The form follows from where the defect lives, not from a list of cases:

   | Defect lives in | Strongest form the artifact admits |
   |---|---|
   | Repository code (Python, shell) | A regression test that reproduces the original symptom, fails on the pre-fix code and passes after. |
   | An unmodifiable external source (the TradingView JPY case, §7) | No repository test can reproduce the upstream symptom: the captured failing evidence — the offending input and the observed wrong output, pinned where the consumer-side rule is recorded — plus a consumer-side test that fails when the rule is absent (Phase 4 item 7). |
   | A repository artifact that is not code — a doc a gate reads, a manifest, a hook payload, a ledger row | The checker that consumes the artifact, run before (flagging the defect) and after (clean), both outputs captured. Where no checker consumes it: the before/after excerpt of the artifact beside the reader it misled, plus the gate that now covers it if one was added. A fix with neither is a claim, not a verification. |

   Then the surrounding gates (fable-method Step 5b); then the `TWINS:` sweep, extended per
   M-24 to independent re-encodings that share no identifier with the fixed site.
8. **Defense after the cause, never instead of it.** With the mechanism fixed, layered validation
   at the boundaries the bad value crossed is welcome. Its failure mode is the owning path's
   documented policy, not a blanket rule. On a fail-closed path the added layer fails closed —
   the layer-boundaries ADR's "unresolved first-party imports fail closed"
   ([ADR](../../../docs/adr/2026-06-05-monorepo-layer-boundaries.md)), the arming interlock in
   `ops/c1_rail/c1_rail_arm.py`, any risk-add on the rail. On a designed fail-open path that
   passes the three-part test above — a risk-reducing exit, an edit-time hook, a report-only
   scanner — the added layer keeps that path's shape: it emits its finding with a status distinct
   from clean and lets the protected action proceed; a validation that blocks the completed edit
   or the relaying exit has changed the owner's policy, which is the owner's separate change, not
   part of the fix. A new layer with no owner naming it fail-open fails closed. The same layer
   added *before* step 4 is row one or two of the banned table.

### Answer shape

In the fix report and the PR description, beside fable-method's `INTENT:` and `TWINS:` lines:

```
ROOT CAUSE: <one mechanism — input or state, site, operation, consequence>
FIX: <what changed, where, at which layer; the band-aids rejected and why>
VERIFICATION: <before/after evidence in step 7's form for the artifact — test node, captured evidence, or checker run; gates run; remaining risk>
```

A fix report without the first line is a symptom fix by definition. A `VERIFICATION:` line that
names no before/after evidence in the form step 7 gives for the artifact — a test failing on the
pre-fix code, captured external evidence plus a consumer-side test, or a checker's
failing-then-clean run — is verification theater (fable-method failure mode 14).

### Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "It's just a None check, it's defensive." | Defensive against what? If you cannot name the writer of the None, you are hiding it. |
| "The retry made it pass." | A race passed once. It is still there. |
| "The log is noisy, swallow it." | Loud is the feature. Emit a finding or raise. |
| "The parser should be lenient." | A lenient parser accepts the wrong artifact silently. The mismatch is the signal. |
| "I'll fix the symptom now and root-cause later." | The guard erases the evidence later would need. Packet C. |
| "Exit 0 on a missing dependency is friendlier." | It reported an empty result as success. |
| "Hooks fail open, so mine can." | Hooks are documented and emit a finding. Yours does neither. |
| "Root-causing is overkill for a one-liner." | The one-liner is where M-23 hid for four days. |
| "The test is flaky, mark it." | fable-method 4.6: a deterministic failure is never labelled flaky without investigation. `babysit` step 4 reruns only an infrastructure-only failure with the outage evidence recorded; "passes on re-run" is a race, not an outage. |

### Red flags

- A diff whose only change is a guard, default, retry, broader `except`, `check=False`,
  `errors="ignore"` or a wider schema, landing in the same PR as the failure it makes disappear.
- A fix commit message or PR description with no mechanism in it.
- The first error named as the cause: "KeyError on X — fixed with `.get`".
- "Flaky" in a PR description with no infrastructure evidence behind it.
- A regression test that would also pass on the pre-fix code, or a test pin edited in a fix PR.
- A script or hook that "handles" a missing executable, file or credential by exiting 0.
- A fallback path with no owner and no finding.
