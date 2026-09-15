---
name: root-cause-first
description: Use at the moment a fix is about to be written or reviewed — "fix this", "make the test pass", "green the CI", "it's flaky, add a retry", "just guard it", "wrap it in try/except", "widen the parser", a diff that adds a None-check, default, retry, broad except or looser schema, or a hook/daemon/script that "handles" an error by exiting 0 — and whenever the first visible error is a TypeError, None, KeyError, schema or parse error, which is a symptom until the upstream mechanism is named. Bans the band-aid moves until the root cause is stated in one sentence, prescribes the backward call-chain trace and the first-unintended-write hunt, and requires a ROOT CAUSE / FIX / VERIFICATION block with a regression test that reproduces the original failure (or, for an unmodifiable external source, captured evidence plus a consumer-side test). Encodes the repo's designed fail-open doctrines (risk-reduction exits on the rail, report-only hooks) so the ban never contradicts them. Gate layered on code-defect-debugging, which owns reproduction and boundary logging; sibling of verify-source and fable-method's INTENT line. Changes no strategy parameters, allocations, dd_protection constants, or MC calibration.
---

# root-cause-first — name the mechanism before you touch the code

## Overview

Fix the mechanism, not the symptom. A guard, a default, a retry, a broader `except` or a wider
parser makes the failure disappear from the place you are looking and keeps it everywhere else,
now silent. This skill is the gate at the moment of repair or review: no band-aid until the
mechanism that makes the failure inevitable is written down in one sentence, then the smallest
fix at the source, then a regression test that reproduces the original symptom.

Provenance: adapted 2026-09-15 from three external drafts — `cohen-liel/agent-skills`
root-cause-first (banned moves, seven-step workflow, answer shape), `obra/superpowers`
systematic-debugging's `root-cause-tracing.md` and `defense-in-depth.md` (backward call-chain
trace; layered validation *after* the cause) and `instructa/agent-skills` root-cause-finder (the
first error is a symptom; intent chain; first unintended write; canonical vs competing sources of
truth). Every imported rule has to justify itself on repo grounds; §Provenance lists what was
dropped.

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

## When it fires

| Trigger | What you are about to do |
|---|---|
| "Fix", "make it pass", "green the CI", a red required check on a PR you own | Gate before the first edit. |
| The first error is `TypeError` / `None` / `KeyError` / `JSONDecodeError` / schema or parse failure | Treat it as a symptom; trace up to who produced the value. |
| "Flaky", "intermittent", "passes on re-run" | A race, an ordering dependence or an environment difference. A retry hides it; code-defect-debugging 1.1 says the intermittence *is* the question. Not this row: an *evidence-backed* infrastructure failure — a runner, service or network outage read from the job log — which `babysit` step 4 reruns with the reason recorded and no code change. "It passed the second time" is not that evidence. |
| Reviewing a diff (Codex round, `fable-judge`, a fleet return) that adds a guard, default, retry, broad `except`, `check=False`, `errors="ignore"` or a looser schema | Ask for the named mechanism; without one the change is REFUTED on that ground. |
| A hook, startup path, boot-time cache, restore/migration, worker pool, background refresher or rewriter is anywhere in the suspect path | Run the first-unintended-write hunt below. |

## Banned until the mechanism is named

| Move | Why it is banned | Repo burn |
|---|---|---|
| **None / empty guard** — `if x is None: return`, `.get(k, default)` where `k` must exist, `or 0` | Hides the signal. Ask *why* it is None and fix that writer. | The `daily_loss_pct: None` TypeError lived at four sites; the class fix was the writer, not four guards (`code-defect-debugging` §4.6). |
| **Catch-and-continue** — `except Exception: pass / return ""`, swallowing a non-zero exit | Turns a loud bug into a silent one. | 2026-09-04f Packet C `_run` guard: missing `git` → exit 0, empty report. |
| **Retry / timeout inflation / sleep** | Flaky means a real race or order dependence. Retry hides it. | — (calibration pending a dated firing) |
| **Parser / schema widening** — accept both shapes, coerce, `errors="ignore"`, `errors="replace"` where bytes matter | The weird input is the clue. Find who produced it. | Faithfulness-audit lesson: the mismatch is the signal. |
| **Default-on-error / silent drop** — an empty report on failure, a reindex that drops rows, a fallback value nobody sees | Synthetic success masks the failure from everyone downstream. | 2026-09-02d `bdate_range` reindex. |
| **Pin, baseline or test edit** to green a run | fable-method Step 4.6: never. | — |
| **Correction factor / overlay** on the output | `code-defect-debugging` §6.1: the bug returns with a different presentation. | JPY ~153× P&L inflation. |
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

## Procedure

1. **State the observed failure concretely.** Exact error text, assertion or log line; the
   command that produced it; the commit. A deterministic defect in this repo's Python or shell
   code — a wrong value *or* a crash — runs `code-defect-debugging` Phase 1 first (deterministic
   reproduction, expected-value authority, git anchors; its §0 routes script crashes to itself)
   and comes back here for the trace and the fix gate. A Pine defect never enters that Phase 1:
   `code-defect-debugging` §0 routes Pine to `pinescript-v6`, which runs this gate in its own
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
     **once**, read the whole capture, then reason (code-defect-debugging Phase 2's run-once
     rule). Never log an env var's value: a token, password, DSN or API key written to a test
     or CI log is a leak (fable-method Step 4.6, CLAUDE.md: never touch secrets). When two
     candidate values must be told apart, log a fingerprint (length plus a hash prefix), never
     the bytes.
   - **First-unintended-write hunt** — state-shaped bugs, a wrong value present and nobody
     obviously wrote it. Ask whether the write, mutation or request should have happened at all.
     List the canonical source of truth and every competing one (Rule 7;
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
7. **Verify against the original failure.** For a fix that lands in repository code: a
   regression test that reproduces the original symptom, fails on the pre-fix code and passes
   after. For a defect in an unmodifiable external source (the TradingView JPY case,
   `code-defect-debugging` §7): no repository test can reproduce the upstream symptom, so the
   verification is the captured failing evidence — the offending input and the observed wrong
   output, pinned where the consumer-side rule is recorded — plus a consumer-side test that fails
   when the rule is absent (`code-defect-debugging` Phase 4 item 7). Then the surrounding gates
   (fable-method Step 5b); then the `TWINS:` sweep, extended per M-24 to independent
   re-encodings that share no identifier with the fixed site.
8. **Defense after the cause, never instead of it.** With the mechanism fixed, layered validation
   at the boundaries the bad value crossed is welcome, and it fails *closed*: the layer-boundaries
   ADR's "unresolved first-party imports fail closed"
  ([ADR](../../../docs/adr/2026-06-05-monorepo-layer-boundaries.md)), the arming interlock in
   `ops/c1_rail/c1_rail_arm.py`. The same layer added *before* step 4 is row one or two of the
   banned table.

## Answer shape

In the fix report and the PR description, beside fable-method's `INTENT:` and `TWINS:` lines:

```
ROOT CAUSE: <one mechanism — input or state, site, operation, consequence>
FIX: <what changed, where, at which layer; the band-aids rejected and why>
VERIFICATION: <regression test node that reproduced the symptom; gates run; remaining risk>
```

A fix report without the first line is a symptom fix by definition. A `VERIFICATION:` line that
names neither a test failing on the pre-fix code nor, for an external-source defect, the
captured evidence and the consumer-side test, is verification theater (fable-method failure
mode 14).

## Rationalizations — STOP if you think one

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

## Red flags

- A diff whose only change is a guard, default, retry, broader `except`, `check=False`,
  `errors="ignore"` or a wider schema, landing in the same PR as the failure it makes disappear.
- A fix commit message or PR description with no mechanism in it.
- The first error named as the cause: "KeyError on X — fixed with `.get`".
- "Flaky" in a PR description with no infrastructure evidence behind it.
- A regression test that would also pass on the pre-fix code, or a test pin edited in a fix PR.
- A script or hook that "handles" a missing executable, file or credential by exiting 0.
- A fallback path with no owner and no finding.

## Relationship to other skills

| Skill or rule | Boundary with this one |
|---|---|
| `code-defect-debugging` | Owns the evidence engine: Phase 1 reproduction, Phase 2 forward boundary logging, Phase 4.5 three strikes. This skill is the gate at the fix; its backward trace and hidden-write hunt are Phase 2 alternatives for crash- and state-shaped bugs. |
| `fable-method` | Step 2.6 / 4.1 `INTENT` is the contract reconstruction; 4.6 forbids weakening checks; 5(c) `TWINS`. This skill's three lines join those in the report. |
| `verify-source` / `rule-0` | The contract must come from the read source, the right vintage, not memory. |
| `blast-radius` | After the fix: sweep the owners and mirrors that still restate the pre-fix behaviour. |
| Rule 7, firm-constants single-source ADR, M-24 | The in-repo single-source-of-truth owners. When the mechanism is duplicated truth, consolidate to the owner, then return here for the regression check. |
| `fable-judge` | Review-time use: a returned fix with no named mechanism is REFUTED on that ground, whatever its tests say. |
| `pinescript-v6` | Owns Pine defects end to end (`code-defect-debugging` §0 routes them there, never to its own Phase 1); it runs this gate in its own runtime. |
| `babysit` | CI repair: its step 4 reruns an infrastructure-only failure with the outage evidence recorded and no code change; every other failing check reaches this gate before an edit. |
| `brief-authoring` lesson capture | A class-failure graduates to a lesson (code-defect-debugging §6.6). |

## Provenance — what was imported, what was dropped

| Source rule | Disposition here |
|---|---|
| root-cause-first banned moves (optional chaining, catch-and-continue, retry/timeout inflation, parser widening, default-on-error, unexplained fix) | Imported; JavaScript idioms mapped to their Python shapes; two repo-native rows added (pin edits, correction factors) |
| root-cause-first seven-step workflow and `Root cause / Fix / Verification` answer shape | Imported; the shape sits beside fable-method's existing artifact lines |
| root-cause-tracing five-step backward trace and instrumentation | Imported; `console.error` becomes a value-plus-stack capture read once |
| defense-in-depth layered validation | Imported as step 8, with the repo's fail-closed framing and the explicit "after, never instead" ordering |
| root-cause-finder intent chain, first-unintended-write, hidden-write audit, "do not widen the contract" | Imported; its fifteen-field output format compressed to the three-line block plus the contract's three sentences |
| ssot-enforcer (paired with root-cause-first upstream) | **Not imported** — Rule 7, the firm-constants ADR, `blast-radius` and lesson M-24 already own single-source-of-truth here |
| A blanket "no fallback, ever" reading | **Transformed** — the rail's risk-reduction fail-open and report-only hooks are doctrine; the three-part designed-fail-open test carries them |
| External frontmatter (`model:`, `allowed-tools:`, `version:`) | **Dropped** — not this repo's skill contract |
