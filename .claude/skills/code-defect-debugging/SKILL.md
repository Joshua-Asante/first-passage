---
name: code-defect-debugging
description: Use this skill whenever Joshua suspects a deterministic code defect in `first_passage` — Python or shell code returning wrong values, scripts crashing, output magnitudes implausible vs a defensible reference, or cross-platform output diverging, where re-runs with identical inputs reproduce the failure. Triggers on phrases like "this is broken", "the output is wrong", "why is this returning X", "this number is off", "script crashed", "MC results look implausible", "P&L looks inflated", "verification failed". Canonical anchor: TV <30-day JPY ~153× P&L inflation (code/feed defect, not methodology). Hand off to `inqhiori` for statistical anomalies (WR/PF drift, anchor trades, regime sensitivity), `pinescript-v6` for Pine source bugs, `prop-firm-challenge` for firm-rule/MC/dd_protection facts, `c1-rail` for live-ops facts. Not for "is this strategy edge real" — that is INQHIORI; this skill is "is the code returning what its inputs imply" only. Also use at the moment any fix is written or reviewed — "fix this", "make the test pass", "green the CI", "add a retry", "just guard it", "wrap it in try/except", "widen the parser", a diff adding a None-check, default, retry, broad except or looser schema, or a script that handles an error by exiting 0 — and whenever the first visible error is a TypeError, None, KeyError, schema or parse error: §11 bans band-aids until the mechanism is named and requires a ROOT CAUSE / FIX / VERIFICATION block with before/after evidence (merged from root-cause-first 2026-10-24).
---

# Code-Defect Debugging

Deterministic code defects in the `first_passage` Python/shell stack. Sibling of `inqhiori`, which is the wrong tool here: it treats a code bug as a falsifiable hypothesis and demands a Pre-Q gate. Live execution decisions follow `c1-rail`. Phases adapted from `obra/superpowers:systematic-debugging`; verification runs against CSV ground truth, Monte Carlo invariants and a pytest regression test (Phase 4 item 7).

---

## 0. Skill selection — which loop is this?

Decide first. INQHIORI on a code bug burns hours; this skill on a methodology anomaly gives false confidence.

| Symptom | Skill |
|---|---|
| Function returns a value inconsistent with its declared inputs | **this skill** |
| Script crashes / raises exception | **this skill** |
| Output magnitude implausible vs known reference (JPY ~153×, P&L 100× expected) — almost always feed, encoding or units | **this skill** |
| Cross-platform output differs (TV vs Python) for same logical input | **this skill** |
| Strategy WR / PF deviates from baseline despite no parameter change | **inqhiori** |
| Regime sensitivity unexpected (anchor trades, tail behavior) | **inqhiori** |
| Live trade or rail decision under time pressure | Stop; AGENTS.md money controls apply, ask Joshua |
| Pine source returns wrong value | **pinescript-v6** |
| dd_protection live calibration vs theoretical | **prop-firm-challenge** |

**Tiebreaker:** divergence that persists across re-runs with identical inputs is a code defect (this skill). Different outputs from the same code and inputs: the variance is the question (INQHIORI).

**Tiebreaker 2:** if you can state "the function should return X given inputs Y and Z" without statistical reasoning, this skill applies. If predicting the output needs a falsifiable hypothesis, INQHIORI applies.

---

## 1. Phase 1 — Evidence before fixes

**Blocking rule: no fix proposed before Phase 1 completes**.

**1.1 Reproduction.** A minimal command that triggers the bug deterministically. If intermittent, the intermittence is the question: log every variable input (data file timestamp, Python version, env vars, working directory) until reproduction is deterministic. An intermittent claim without reproduction is a Phase 1 failure.

**1.2 Inputs and outputs at the failure boundary.** What did the failing function or stage receive, what did it return, what was expected, and on what authority? Authority is one of: (a) a reference implementation (Pine source, a prior version), (b) a closed-form calculation Joshua can check by hand, (c) a locked CSV-reconcile baseline, (d) a Monte Carlo invariant (e.g., bust attribution sums to 100%). "It felt about right last time" is not authority.

**1.3 The git anchor.** `git log --oneline -1 -- <file>` for every file in the suspect path. If the bug is new, read the diff between last-known-good and HEAD first. If it has always been there, log the anchor anyway.

**1.4 Phase 1 closes when** reproduction is deterministic AND boundary inputs/outputs are logged AND expected values have authority cited.

---

## 2. Phase 2 — Component-boundary logging

For wrong-value bugs. For crash-shaped bugs (an exception deep in a call chain) and state-shaped bugs (a wrong value with no obvious writer), §11's backward call-chain trace and first-unintended-write hunt replace or precede this forward pass. Instrument every component boundary in the suspect path, run once, then analyze.

**Component boundaries in this stack:**

- **Function call** — between `portfolio_mc.py` modules (data loader → bootstrap engine → bust-attribution aggregator).
- **File format** — CSV → DataFrame → dict → JSON. Serializer/deserializer pairs are the highest-frequency source of subtle bugs (encoding drift, NaN handling, integer-vs-float, timezone parsing).
- **Feed** — CME futures TV export CSV (`core/data/tv_exports/cme/`) to in-memory representation. Feed bugs hide as "the methodology must be wrong"; they are not.
- **Unit** — points-vs-pips, percentage-vs-decimal, contract-value-vs-notional, base-vs-quote.
- **Session/timezone** — chart-TZ vs UTC, NY-close-anchored vs broker-day.

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

**Run once, then analyze.** One full evidence pass, read as a complete artifact. No log-theorize-log cycles: theorizing mid-log selects evidence.

**The failing component is the one whose output stops matching expectation.** Work forward through the boundaries.

**Phase 2 closes when** the failing component is named: not "somewhere in the MC pipeline" but `portfolio_mc.bootstrap_engine.compute_panel_thirds`, line range, specific input value, specific wrong output.

---

## 3. Phase 3 — Hypothesis testing

The hypothesis must be specific enough that a one-line test can falsify it.

**Forbidden patterns:**

- "Maybe the function isn't handling edge case X correctly." Sharpen to: "If input is `<specific value>`, function returns `<specific wrong value>` instead of `<specific right value>`, because `<specific line>` does `<specific operation>` when it should do `<specific other operation>`."
- "Floating-point rounding": almost never the answer at this stack's magnitudes. Last resort; falsify first with a quick magnitude check.
- "Pandas weirdness": same. Sharpen or discard.

**Permitted patterns (from past bugs here):** unit conversion missing or doubled; encoding/dtype mismatch at a deserialization boundary; off-by-one in window-slicing or panel indexing; implicit timezone conversion (system-local vs UTC vs chart-TZ); reference-vs-copy mutation in a DataFrame operation; integer division where float was intended; a default argument the caller did not assume; a feed-side data issue masquerading as code (verify per §6.4).

**Test with one minimal input that distinguishes the hypothesis from alternatives.** Inject the hypothesized input and observe the hypothesized wrong output. Do not test by applying a fix.

---

## 4. Phase 4 — Fix and verification

The fix passes through the §11 band-aid gate: a guard, default, retry, broad `except`, `check=False` or widened parser is not a fix until the mechanism is named in one sentence, and the report carries its `ROOT CAUSE:` / `FIX:` / `VERIFICATION:` block.

1. **Smallest possible change**, the inverse of the confirmed hypothesis. No refactoring "while we're in here".
2. **Reproduction now produces correct output.** Re-run the Phase 1.1 command. If not, the hypothesis was wrong; return to Phase 3.
3. **Locked baselines still pass** (CSV reconcile baselines: G 201t / DJ30 224t / A 123t / NAS 200t). A fix that breaks one is a structural change, not a defect fix: escalate to INQHIORI.
4. **MC engine regression unchanged.** If the fix touches the MC path (`portfolio_mc.py`, `core/data/tv_exports/cme/` consumers, dd_protection logic), re-run `python -m pytest tests/core/test_mc_synthetic_engine.py -q`. The 99.83/0.17/4.37 figures are historical record, not a live pin. Drift in the synthetic-engine pins means structural change: escalate to INQHIORI for re-calibration.
5. **Diff scope check.** Files modified must match the fix's logical scope exactly. Surprise file changes are forbidden.
6. **Twin sweep.** A defect at one site is presumed to recur wherever the construct was copied until a search says otherwise. Name the exact wrong construct (the expression, not the symptom), `rg` the whole repo, and record verbatim: `TWINS: searched <pattern> — found <N> other sites: <files|none>`. Fix them or list them; a completeness claim with no search behind it is verification theater.
7. **Regression test pins the original failure.** A fix in repository code lands with a test that reproduces the Phase 1.1 symptom, fails on the pre-fix code and passes after; a test that would also pass pre-fix verifies nothing. When the defect lives in an unmodifiable external source (§7), the fix is a consumer-side rule and verification is: the captured failing evidence (offending input and observed wrong output, pinned where the rule is recorded), a consumer-side test that fails when the rule is absent, and the lesson capture in §6.6.

---

## 5. Phase 4.5 — Architecture questioning (mandatory after 2 failed fixes)

If two fix attempts have failed (hypothesis confirmed, fix applied, reproduction still fails or a different test breaks), STOP. Do not author Hypothesis 3, and do not try a third fix: the fix is at a different level than the bug. Sibling of `inqhiori` §6 (when serious attempts at one level keep failing, the level is wrong).

- Read the broader region: parent module, calling code, the data consumed.
- Ask: is the function being asked to do something it cannot do given its shape? (It may correctly implement a wrong specification.)
- Ask: has the reframe revealed a methodology question? If yes, hand off to INQHIORI; §0 selection was wrong.
- Document the architecture concern as an ADR candidate (via `brief-authoring`), then escalate.

---

## 6. Anti-patterns and traps

**6.1 Symptom fixes.** "The number is wrong, so I'll add a correction factor." A fix that clears the symptom and leaves the cause is failure even if the test passes.

**6.2 Defaulting to "Pandas weirdness" or "floating-point rounding."** Last-resort hypotheses, not first-resort.

**6.3 Fixing without reproducing.** Reproduce first. Always.

**6.4 Conflating data quality with code defect.** Re-run the failing operation against the locked CME futures TV export from `core/data/tv_exports/cme/` (the canonical feed). If the bug reproduces, it is code. If it disappears, the input data is the question: hand off to `trade-csv-reconcile`.

**6.5 Treating a methodology anomaly as a code defect.** If WR or PF shifted with no recent change to the relevant code, the question is statistical: hand off to `inqhiori`.

**6.6 Not capturing the lesson.** A defect that consumed >2 hours and identified a class of failure (not a one-off typo) graduates to a methodology lesson via `brief-authoring` lesson capture.

---

## 7. Canonical case — the JPY ~153× P&L bug

TradingView ≤29-day backtests inflated JPY-pair P&L (~153×) through TV's own pip-value calculation; the same run at 31 days was sane. It was first misrouted as a methodology question; §0 (magnitude implausible vs reference, deterministic across re-runs) routes it here. TV is not modifiable, so the fix is a consumer-side rule, "don't use TV <30-day backtests for P&L", plus the captured lesson.

---

## 8. Hand-off rules

| Hand off to | When |
|---|---|
| `inqhiori` | Phase 4.5 reveals a methodology question, or the fix produces a structural change that needs full INQHIORI discipline |
| `c1-rail` | A defect surfaced under live time pressure: the operational decision follows the rail's safety invariants; the code fix is deferred to a later session under this skill |
| `pinescript-v6` | The bug is in Pine source, not Python |
| `prop-firm-challenge` | The "bug" is a live-ops or Rule-0 fact (dd_protection is doing what it should; the expectation was wrong) |
| `brief-authoring` lesson capture | A class-failure (§6.6) |
| `brief-authoring` ADR | A Phase 4.5 architecture concern that warrants a structural decision artifact |
| `trade-csv-reconcile` | The bug turns out to be data quality, not code |

---

## 9. What this skill does not change

Strategy parameters (Guardian / Striker / Aegis / NAS locks remain), allocations or dd_protection calibration (`prop-firm-challenge` / INQHIORI), methodology framework rules (`inqhiori`), Pine source (`pinescript-v6`). It governs how defects are diagnosed and fixed, not what production code is supposed to do.

---

## 10. Audit hooks

Quarterly: defects diagnosed (`git log --oneline | grep -i 'fix\|bug'`); how many followed Phase 1 vs symptom-fixed; how many were mis-routed to INQHIORI first; how many graduated to lessons; how many invoked Phase 4.5. If mis-routes exceed 1× per quarter, revise the description per `skill-creator`'s undertriggering guidance.

---

## 11. Root-cause gate — before writing or reviewing any fix

Merged 2026-10-24 from the retired `root-cause-first` skill ([tombstone](../../../docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation)). It fires on any repair or review, not only on defects routed through §0.

Fix the mechanism, not the symptom. A guard, default, retry, broader `except` or wider parser keeps the failure everywhere else, now silent. No band-aid until the mechanism that makes the failure inevitable is written in one sentence; then the smallest fix at the source; then a regression test that reproduces the original symptom. The visible error is rarely at the site of the cause, and a mismatch is the signal ([`methodology_lessons.md`](../../../docs/methodology/lessons/methodology_lessons.md); M-23 in the [index](../../../docs/methodology/LESSONS_INDEX.jsonl)): never let a faithfulness audit silently discard the source-of-truth artifact in favor of its own recompute.

### When it fires

| Trigger | What you are about to do |
|---|---|
| "Fix", "make it pass", "green the CI", a red required check on a PR you own | Gate before the first edit. |
| The first error is `TypeError` / `None` / `KeyError` / `JSONDecodeError` / schema or parse failure | Treat it as a symptom; trace up to who produced the value. |
| "Flaky", "intermittent", "passes on re-run" | A race, ordering dependence or environment difference; a retry hides it (§1.1). Not this row: an *evidence-backed* infrastructure failure (runner, service or network outage read from the job log), which is rerun with the reason recorded and no code change. "It passed the second time" is not that evidence. |
| Reviewing a diff (Codex round, `handoff-verify` post-execution judging, a fleet return) that adds a guard, default, retry, broad `except`, `check=False`, `errors="ignore"` or a looser schema | Ask for the named mechanism; without one the change is REFUTED on that ground. |
| A hook, startup path, boot-time cache, restore/migration, worker pool, background refresher or rewriter is in the suspect path | Run the first-unintended-write hunt below. |

### Banned until the mechanism is named

| Move | Why |
|---|---|
| **None / empty guard** — `if x is None: return`, `.get(k, default)` where `k` must exist, `or 0` | Hides the signal. Ask *why* it is None and fix that writer. |
| **Catch-and-continue** — `except Exception: pass / return ""`, swallowing a non-zero exit | Turns a loud bug into a silent one. |
| **Retry / timeout inflation / sleep** | Flaky means a real race or order dependence. |
| **Parser / schema widening** — accept both shapes, coerce, `errors="ignore"`, `errors="replace"` where bytes matter | The weird input is the clue. Find who produced it. |
| **Default-on-error / silent drop** — an empty report on failure, a reindex that drops rows, a fallback value nobody sees | Synthetic success masks the failure downstream. |
| **Pin, baseline or test edit** to green a run | fable-method Step 4.6: never. |
| **Correction factor / overlay** on the output | §6.1. |
| **Unexplained fix** — "it passes now" with no mechanism | Then it is not fixed. You moved the bug. |

**Designed fail-open is not a band-aid.** Two doctrines held on purpose: the rail "may fail closed on risk-add, never fail closed on risk reduction" — `exit` / `flat` relay best effort and raise a CRITICAL operator notification when evidence cannot be written ([M1 ADR](../../../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) item 6); and edit-time hooks and report-only scanners fail open for the completed edit while *emitting a finding* ([skill lifecycle](../../../scripts/README.md); the Sentinel `preregistration_scan` in `ops/sentinel/scan.py`). A new or reviewed path must meet all three:

1. the open path is named in an owner: ADR, README, or the function's own docstring;
2. taking it emits a visible finding, notification or non-zero status where a human reads, and the diagnostic's status stays distinct from clean: "NOT CHECKED / could not run" is never "checked, none found" (the SKIP-versus-PASS convention in `scripts/check_skill_deploy_sync.py`);
3. the protected action may proceed (an edit completes, a report-only scan does not block a commit, a risk-reducing exit relays), but a *fix* never converts the failure it was written for into a success exit code or an empty-but-valid artifact.

An existing documented path is grandfathered by its owner, not by this test. Where it conflates "could not run" with "none found", as the Sentinel's `no git → []` in `ops/sentinel/scan.py` does, it is no template for new code, and tightening it is its owner's separate change, never a drive-by inside a fix PR. A `pass` with no owner and no finding that turns failure into success is a band-aid whatever its comment says.

### Procedure

1. **State the observed failure concretely.** Exact error text, assertion or log line; the command; the commit. A deterministic defect in this repo's Python or shell code (wrong value *or* crash) runs Phase 1 first, then returns here for the trace and fix gate. A Pine defect never enters Phase 1: §0 routes it to `pinescript-v6`, which runs this gate in its own runtime. This step stands alone at review time, when Phase 1 has already run, or when the failing artifact is not code (a doc gate, a manifest, a hook payload).
2. **Reconstruct the intended contract.** Three sentences: the expected behaviour; the invariant it rests on; what definitely did *not* happen. It comes from the read source under fable-method's `INTENT` authority order (operator > ADR/LOCK > tests > current code), never from the failing code's own shape.
3. **Trace the real path** with the technique that fits. Prefer logs, tests and traces over inference.
   - **Backward call-chain trace** (crash-shaped). Symptom site → the line that threw → who called it → what value was passed at each level → where the bad value originated → what changed there (`git log -1 -- <file>`, `git log -S<token>`, the last-known-good diff). If you cannot read it, instrument: log the value, the cwd, the *name* and presence of the relevant env var and `traceback.format_stack()`; run **once**, read the whole capture, then reason. Never log an env var's value: a token, password, DSN or API key in a test or CI log is a leak (fable-method Step 4.6, AGENTS.md: never touch secrets). To tell two candidate values apart, log a fingerprint (length plus a hash prefix), never the bytes.
   - **First-unintended-write hunt** (state-shaped: a wrong value nobody obviously wrote). Ask whether the write, mutation or request should have happened at all. List the canonical source of truth and every competing one (operational_rules §7; [firm-constants single source](../../../docs/adr/2026-06-06-firm-constants-single-source.md); M-24's independent re-encodings). Audit hidden writers: `SessionStart` / `PostToolUse` hooks, startup code, boot-time caching, restore and migration paths, worker pools that re-import config, background refreshers, retries, rewriters. Non-explicit writes are suspects until proven intentional. The root cause is the *first* unintended side effect, not the last error.
4. **Name the mechanism** in one sentence that makes the failure inevitable: "given `<input or state>`, `<site>` does `<operation>`, so `<wrong output>`." Cannot → you are at a symptom; go up one level.
5. **Reject band-aids explicitly.** For each banned move you were tempted by, write why the mechanism makes it wrong. If the mechanism *proves* a fallback correct, it is designed fail-open: give it an owner and a finding per the three-part test.
6. **Fix at the source of the bad state**, smallest change, correct layer first: upstream logic over a downstream contract. Never make a contract more permissive unless the observed payload is proven intended in the final design. An architectural concern goes to a Notice log or ADR candidate, not into the fix.
7. **Verify against the original failure.** Evidence that the symptom reproduces *before* the fix and is absent *after*, in the strongest form the artifact admits, never a synthetic check that would also pass pre-fix:

   | Defect lives in | Strongest form |
   |---|---|
   | Repository code (Python, shell) | A regression test that reproduces the symptom, fails on pre-fix code, passes after. |
   | An unmodifiable external source (§7) | Captured failing evidence (offending input, observed wrong output) pinned where the consumer-side rule is recorded, plus a consumer-side test that fails when the rule is absent (Phase 4 item 7). |
   | A repository artifact that is not code — a doc a gate reads, a manifest, a hook payload, a ledger row | The consuming checker run before (flagging) and after (clean), both outputs captured. With no checker: the before/after excerpt beside the reader it misled, plus the gate that now covers it if one was added. A fix with neither is a claim, not a verification. |

   Then the surrounding gates (fable-method Step 5b); then the `TWINS:` sweep, extended per M-24 to independent re-encodings that share no identifier with the fixed site.
8. **Defense after the cause, never instead of it.** With the mechanism fixed, layered validation at the boundaries the bad value crossed is welcome, and its failure mode is the owning path's documented policy. On a fail-closed path it fails closed: the layer-boundaries ADR's "unresolved first-party imports fail closed" ([ADR](../../../docs/adr/2026-06-05-monorepo-layer-boundaries.md)), the arming interlock in `ops/c1_rail/c1_rail_arm.py`, any risk-add on the rail. On a designed fail-open path that passes the three-part test (a risk-reducing exit, an edit-time hook, a report-only scanner) it emits its finding with a status distinct from clean and lets the protected action proceed; blocking the edit or the exit changes the owner's policy, which is the owner's separate change. A new layer with no owner naming it fail-open fails closed. The same layer added *before* step 4 is a banned move.

### Answer shape

In the fix report and PR description, beside fable-method's `INTENT:` and `TWINS:` lines:

```
ROOT CAUSE: <one mechanism — input or state, site, operation, consequence>
FIX: <what changed, where, at which layer; the band-aids rejected and why>
VERIFICATION: <before/after evidence in step 7's form for the artifact — test node, captured evidence, or checker run; gates run; remaining risk>
```

A report without the first line is a symptom fix by definition. A `VERIFICATION:` line with no before/after evidence in step 7's form is verification theater (fable-method failure mode 14).

### Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "It's just a None check, it's defensive." | Defensive against what? If you cannot name the writer of the None, you are hiding it. |
| "The retry made it pass." | A race passed once. It is still there. |
| "The log is noisy, swallow it." | Loud is the feature. Emit a finding or raise. |
| "The parser should be lenient." | A lenient parser accepts the wrong artifact silently. |
| "I'll fix the symptom now and root-cause later." | The guard erases the evidence later would need. |
| "Exit 0 on a missing dependency is friendlier." | It reports an empty result as success. |
| "Hooks fail open, so mine can." | Hooks are documented and emit a finding. Yours does neither. |
| "Root-causing is overkill for a one-liner." | The one-liner is where M-23 hid for four days. |
| "The test is flaky, mark it." | fable-method 4.6: a deterministic failure is never labelled flaky without investigation. Only an infrastructure-only failure is rerun, with outage evidence recorded. |

### Red flags

- A diff whose only change is a guard, default, retry, broader `except`, `check=False`, `errors="ignore"` or a wider schema, in the same PR as the failure it makes disappear.
- A fix commit message or PR description with no mechanism in it.
- The first error named as the cause: "KeyError on X — fixed with `.get`".
- "Flaky" in a PR description with no infrastructure evidence behind it.
- A regression test that would also pass pre-fix, or a test pin edited in a fix PR.
- A script or hook that "handles" a missing executable, file or credential by exiting 0.
- A fallback path with no owner and no finding.
