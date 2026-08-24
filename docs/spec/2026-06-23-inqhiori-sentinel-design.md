# Design spec — INQHIORI Sentinel (periodic methodology-hygiene + obligation-readiness loop)

**Status:** `DRAFT — pending operator review`
**Date:** 2026-06-23
**Authors:** Joshua (decision) + Claude Code (design, this session)
**Type:** design spec (operational tooling). No governance override; no strategy/lock/risk-constant change. The tool **proposes**, never acts.
**Validation provenance:** one live, faithful INQHIORI probe iteration run this session (workflow `wf_5cddecb4-3e6`, 4 parallel Identify streams → pre-Q D-S-A gate → 5 candidates → per-candidate adversarial filter). Two survivors (C1, C2) were re-verified parent-side against the on-disk files before this spec was written.

---

## §0 — Rule 0 reads (production-source verification, this session)

Files read before authoring (file:line cited where load-bearing):

- `CLAUDE.md:79-80` — the Protection-block MC anchor line: asserts *"p99 DD 0.63pp headroom"* with **no fixed-1R caveat** on that line (the regime caveat sits at line 62, gross-of-swap at line 54). This is the C1 skew target.
- `docs/mc_anchor_history.md:7` — the Q-SWAP-2 closure (2026-05-26): *"The 'Both lock gates clear (… p99 DD 0.63pp headroom)' qualitative claim in the §Protection block above is **provisionally retracted** on the p99 DD gate under fixed-1R modeling"* (margin → 0.45pp; lock still passes, 4.55% < 5%). The superseding record lives **only in the archive**, not on the canonical surface.
- `ops/reference/regime_calendar.md:5,14-15,22` — *"one verification pass on [M]/[L] cells is due **before the 2026-08-08 quarterly slate**."* Rows `2025 = [M]` and `2026 = [L]` are still unverified. C2 precondition target.
- `docs/notes/audits/rule-2-trip-log.md:15,23` — one baseline (non-trip) row; *"An empty table across ≥2 audit cycles falsifies the rule."* The 2026-08-08 audit will be data-starved on the Rule-2 graduation check. C2 precondition target.
- `lab/analysis/time_to_pass.py`, `lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py` — both exist; the 2026-08-08 slate's instruments are runnable.
- `docs/spec/2026-06-17-dukascopy-retirement-design.md` — the spec-format template this document follows.
- `ops/weekly_review_feeder/weekly_review_feeder/__main__.py`, `ops/live_journal/reconcile/__main__.py` — the `ops/` package layout (`python -m <pkg>`) this tool follows.
- `scripts/check_boundaries.py` (contract: `ops → {core, governance}` legal; `lab ↔ ops` forbidden) — placement constraint for the new tool.
- Live probe output `wf_5cddecb4-3e6` — the empirical basis in §2 (gate, survivors, killed, forbidden-D flags).

---

## §1 — Goal & non-goals

**Goal.** A periodic, low-cost routine that probes the repo for (a) doc/code skew, (b) dated obligations coming due or past, and (c) precondition-readiness for those obligations — emitting a **human-gated proposal queue** routed Closed / Action / Forward. It runs the INQHIORI loop's structure (Identify → Notice → pre-Q D-S-A gate → falsifiable candidates → adversarial filter) on a cadence, and **returns control at the decision point**: it never deletes corpus, never edits files, never executes Actions.

**Non-goals (explicit).**
1. **Not an alpha-discovery engine.** The live probe established that on this repo new-edge yield is ~0 — the registry/SNAG/regime machinery has already exhausted the OHLC space; new edges need *exogenous* data the repo lacks. The Sentinel routes OHLC-space re-proposals to **Closed** and does not manufacture directions. (A burst of "new directions" is a degeneration signal, not a win — §7.)
2. **No autonomous mutation.** It does not patch CLAUDE.md, edit ADRs, delete corpus items, or run lock-affecting commands. Human-gated D is preserved.
3. **No new strategy/lock/risk-constant logic.** It reads the locked surfaces; it never writes them.
4. **Not a telemetry subsystem.** One queue file + one gate-audit log, mirroring the `rule-2-trip-log.md` "one table, not a subsystem" doctrine.

---

## §2 — What the live probe proved (empirical basis)

The concept was tested before being specced. One faithful iteration (`wf_5cddecb4-3e6`):

- **4 Identify streams** read real files (Rule 0), surfaced ~20 observations across metrics, investigation-history, live-ops, structural.
- **Pre-Q gate** compressed to 5 anomaly clusters, proposed **only permitted-D** deletions (the non-anomalies: byte-identical anchors, allocation/metadata consistency), and **self-flagged two forbidden D-tests it was tempted by and refused them** (the "high signal-to-noise / fits my model" temptation on the Closed-routed items; the "known mechanism" temptation on the Q-SWAP-2 observation). This is the Iran-Hormuz guardrail firing autonomously — the safety property that makes unattended operation acceptable for this methodology.
- **Adversarial filter killed 3 of 5** candidates with cited reasons, and **caught a factual overclaim** in one (C5 asserted "4 powered nulls"; only 3 were actually run — Q-TOM-SPX-1 is open-draft).
- **2 survivors**, both re-verified by me parent-side:
  - **C1 (doc/code skew):** `CLAUDE.md:80` carries an unqualified "0.63pp headroom" claim that `mc_anchor_history.md:7` provisionally retracted to 0.45pp under fixed-1R (M-SWAP-1). Lock still passes; this is a *margin-characterization* skew the existing doc/code-skew trigger missed.
  - **C2 (obligation readiness):** the 2026-08-08 slate's instruments exist but its inputs don't — `regime_calendar` `[M]/[L]` cells unverified; `rule-2-trip-log` near-empty.

**Conclusion that shapes this design:** the loop's value is **hygiene + obligation readiness**, not discovery. Both proven findings were caught by *mechanical* pattern-matching (a skew diff and a date scan) — which is why v1 puts the cheap deterministic layer first and reserves the LLM for where it actually earned its keep (the gate's forbidden-D detection and the adversarial filter).

---

## §3 — Architecture (three cost-tiered layers)

```
repo files
  │
  ▼  TIER 1 · deterministic (no LLM, cheap)  ── runs weekly ──
  Identify-by-script:
    • skew scan        — canonical claim-lines (CLAUDE.md) ⟂ ADR/history/test-pins   [caught C1]
    • obligation scan  — every dated next:/trigger/review date  vs  today            [caught C2]
    • precondition scan — for each near/past obligation, do its named inputs exist & look populated?
  │  surfaced-set  (expected: usually empty)
  │
  ├─ if empty → write an empty-run line to the queue, stop.   (the common case)
  │
  ▼  TIER 2 · LLM gate          ── fires only when Tier 1 surfaces something, or on the quarterly full run ──
  pre-Q D-S-A:  permitted-D propose · FLAG forbidden-D → gate-audit log · frame falsifiable H · route C/A/F
  │  candidates
  ▼  TIER 3 · LLM adversarial   ── load-bearing; killed 3/5 + caught an overclaim in the test ──
  per-candidate skeptic: kill if known / rejected-registry / tail-exhausted / non-falsifiable / re-proposal-without-new-evidence
  │  survivors
  ▼
  PROPOSAL QUEUE  (committed markdown)  +  GATE-AUDIT LOG (forbidden-D flags)
  ── operator reads: Closed = log · Action = operator does it · Forward = operator schedules ──
```

**v1 implementation scope.** Build **Tier 1** as a tested `ops/` tool. **Tiers 2–3 are not new code** — they are the saved probe workflow (`inqhiori-probe-iteration-1-wf_*.js`), promoted to a named, reusable workflow and documented as the **quarterly full-run procedure**. This keeps v1 genuinely lean: the weekly value (skew + obligations) ships as deterministic, testable Python with zero token cost; the deep LLM pass stays an on-demand/quarterly operator-invoked workflow.

---

## §4 — Components

### 4.1 `ops/sentinel/` — the Tier-1 scanner (v1 deliverable)
Runnable as `python -m sentinel` (layout per the plan; `ops/` is on pythonpath). Three pure functions over file contents, no first-party `core`/`lab` imports beyond reading paths (boundary-clean):

- **`skew_scan()`** — for a registry of *canonical claim assertions* (start with the MC-anchor pass/bust/p99/headroom values and strategy versions in `CLAUDE.md`), compare the stated value against its source-of-truth (`tests/core/test_mc_anchors.py` pins, `docs/mc_anchor_history.md`, `core/dd_protection.py` / `core/firm_rules.py`). Emit a finding when a canonical line asserts a value or qualitative margin that its source has superseded or retracted. **C1 is the first regression fixture.**
- **`obligation_scan()`** — parse dated obligations (`next:`/`trigger`/`review`/`due before` patterns) across `CLAUDE.md`, `docs/adr/*`, `ops/reference/regime_calendar.md`, `docs/notes/audits/*`, `docs/SESSIONS.md`. Flag any within a configurable horizon (default 60d) or past `today`. **The 2026-08-08 slate is the first fixture.** ⚠ **As-built scope, corrected 2026-08-03:** the implementation plan (`2026-06-23-inqhiori-sentinel-plan.md` Step 3) silently narrowed this to `CLAUDE.md` + `ops/reference/regime_calendar.md` (superseded in practice by `ops/instruments/USDCAD.md`'s Regime calendar section, since the named path never existed) + one `docs/notes/audits/` file — `docs/adr/*` and `docs/SESSIONS.md` were dropped without documented rationale. `docs/adr/*` landed 2026-08-03 (gate-stack audit X2/X3, `ops/sentinel/scan.py` `_adr_trigger_dates`), restricted to the ADR template's `**Trigger check schedule:**` field and aggregated by date (not per-file) to avoid the ADR-date noise a naive whole-file scan would reproduce — 34 of 100 ADRs currently name 2026-08-08 there. `docs/SESSIONS.md` and the rest of `docs/notes/audits/*` remain out of scope: `docs/SESSIONS.md` is already covered by the purpose-built `sessions_scan()` (roll-off hygiene, a different question than forward obligations) and widening `docs/notes/audits/*` beyond `rule-2-trip-log.md` was not re-examined this pass.
- **`precondition_scan()`** — for each surfaced obligation, check its named inputs exist and look non-empty (e.g. `regime_calendar` `[M]/[L]` cells verified? `rule-2-trip-log` has ≥1 row per active loop class?). **C2 is the first fixture.** Generalized 2026-08-03 beyond the single hardcoded `SLATE_DATE`: for every date `obligation_scan`'s ADR-trigger surface finds, checks whether STATE.md's matching `### {date}` section actually links the contributing ADRs (`_board_sync_findings`) — the gap X3 named ("STATE.md books none of them") is now a mechanical, re-runnable finding rather than a hand-grep. Deliberately does not attempt vehicle-name normalization (X3's "7 different names" for the convening event) — cross-checking by source FILE reference sidesteps needing to know whether "quarterly programme audit" and "quarterly regime check" denote the same mechanism, which several ADRs explicitly treat as distinct, merely co-scheduled cadences.

`today` is injected (never `Date.now()`-style implicit) so runs are deterministic and testable.

### 4.2 Proposal queue + gate-audit log (committed markdown)
- **Queue:** `docs/notes/sentinel/queue.md` (rolling, reverse-chron) + optional per-run detail under `docs/notes/sentinel/runs/<date>.md`. Each row: date, finding, routing (C/A/F), source path:line, cheapest next step. An empty run writes a single "no findings" baseline line (no empty-theater).
- **Gate-audit log:** `docs/notes/audits/sentinel-gate-audit.md` (mirrors `rule-2-trip-log.md` format) — every forbidden-D-test the Tier-2 gate flags is appended here. This is the safety audit trail; it must be non-empty whenever the LLM tiers run and route anything Closed.

### 4.3 Quarterly full-run procedure (reuse, not new code)
The saved probe workflow, promoted to a named workflow, invoked by the operator quarterly (co-scheduled with the 2026-08-08 regime slate). Documented in §6; produces the same queue + gate-audit artifacts as Tier-1, with the deeper LLM Identify/gate/adversarial passes.

---

## §5 — Data flow & the human-gated boundary

`repo files → Tier 1 (always) → [surfaced-set] → Tier 2 gate → Tier 3 adversarial → survivors → queue + gate-audit`.

The boundary is hard: **everything downstream of the queue is the operator.** `Closed` = the operator (or a later run) confirms it's logged. `Action` = the operator performs it. `Forward` = the operator schedules it. The Sentinel writes only to `docs/notes/sentinel/` and `docs/notes/audits/sentinel-gate-audit.md`; it touches no locked surface, runs no lock-affecting command, deletes nothing.

---

## §6 — Cadence & wiring

- **Weekly (Tier-1 only):** `make sentinel` (new Makefile target → `python -m sentinel --asof <date>`). Near-zero cost; catches C1/C2-class items fast. Optionally scheduled via `/schedule` or a cron cloud agent once the tool is stable (report-only).
- **Quarterly (full LLM run):** operator-invoked workflow, co-scheduled with the standing regime trigger (next **2026-08-08**, then 11-08, 02-08, 05-08).
- **Layer placement:** `ops/` (operational; reads `core`/docs, emits proposals; imports nothing from `lab`). `scripts/check_boundaries.py` must stay green.
- **No manifest/Pine/params interaction** (the tool writes only under `docs/notes/`), so the pre-commit data/Pine/params gates are unaffected.

---

## §7 — Guardrails (baked in)

1. **Human-gated D** — proposal queue only; never deletes/edits/acts.
2. **Forbidden-D audit trail** — every flagged forbidden-D-test logged to `sentinel-gate-audit.md` each LLM run.
3. **Degeneration tripwire** (programme-audit hook) — steady-state is a near-empty Forward queue. A burst of Forward "new directions" → inspect the registry/SNAG check for rot; treat as a smell, not a discovery. The Sentinel's *job is to mostly say nothing.*
4. **Not-an-alpha-engine** — OHLC-space re-proposals route Closed against `docs/rejected_candidates.md` + SNAG/exhaustion rules; revival bars (exogenous evidence) are enforced by the adversarial filter.
5. **Token budget** — Tier-1 is free; the quarterly full run is operator-invoked and budget-capped (the test ran ~728K tokens — acceptable quarterly, not weekly, which is exactly why Tier-1 is deterministic).

---

## §8 — Testing

Tier-1 is pure-function and unit-testable; the verified findings become regression fixtures:

- **`test_skew_scan`** — fixture reproducing the `CLAUDE.md:80` ⟂ `mc_anchor_history.md:7` Q-SWAP-2 case must be **detected** (until C1 is remediated, then a fixed copy must be **clean**). Plus a negative control (a correctly-caveated line must not fire).
- **`test_obligation_scan`** — fixture with the 2026-08-08 slate at a pinned `asof` must surface it inside the horizon; a far-future date must not.
- **`test_precondition_scan`** — fixture with an unverified `[L]` cell / empty trip-log must flag; a populated one must pass.
- **Determinism** — same inputs + same `asof` → byte-identical queue output.

Tests live in `tests/` (collected by the main pytest matrix) or skip-clean if a fixture file is absent, per repo convention.

---

## §9 — Open questions for the implementation plan

1. Exact package layout (`ops/sentinel/sentinel/__main__.py` vs flat) — match whichever sibling convention the plan confirms.
2. The canonical-claim registry format for `skew_scan()` — inline constants in v1, or a small `claims.toml`? (Lean v1: inline, ≤6 claims — the MC anchor quad + headroom + the four strategy versions.)
3. Whether the weekly run is operator-manual (`make sentinel`) only, or auto-scheduled from the start. (Recommend manual until one month of clean runs, then `/schedule`.)

---

## §10 — v1 acceptance criteria

- `python -m sentinel --asof 2026-06-23` runs, reads real files, and **surfaces C1 and C2** (the two verified findings) into `docs/notes/sentinel/queue.md`, routed Action.
- An `--asof` far past both obligations and after a (hypothetical) C1 fix produces a clean "no findings" run.
- Unit tests in §8 pass; `check_boundaries.py` green; no manifest/params/Pine gate touched.
- The quarterly full-run workflow is documented and invokable, producing queue + gate-audit artifacts.
- Nothing in the tool writes outside `docs/notes/`.

---

## Addendum — 2026-08-24: `_changed_files` detects renames; `asof` bounds the window at both ends

Two defects in the same helper layer, both surfaced by the 2026-08-24 weekly run. Neither
changes what the convention forbids; both change which commits the scan can see correctly.

### A. Archival moves read as freeze violations (rename detection)

`_changed_files` ran `diff-tree --name-status` with **no `-M`**, so git reported a MOVE as
delete-old + add-new — and `A` is exactly what "introduced here" keys on. Archiving a closed
camp (`lab/analysis/<slug>/` → `lab/archive/<slug>/`) relocates `PREREG` and `RESULTS`
*together by construction*, so every `--slug` archival commit read as a same-commit freeze.

- **How it surfaced.** The 2026-08-24 run emitted 20 `prereg` findings, of which two —
  `PREREG-SAMECOMMIT-1e40b11` (*"archive dstruct_mnq via --slug"*) and
  `PREREG-SAMECOMMIT-f2cbb7b` (*"archive closed CATALOG camps via --slug"*) — were pure
  relocations. `git show --stat -M` shows both files at 0 changed lines. Worse than noise:
  `1e40b11` double-counted the *same* dstruct artifact already flagged at its real
  `_inbox` origin (`4062562`), so one violation was reported twice under two IDs.
- **The rule.** `-M` is now passed. A rename status `R100` (pure move) contributes nothing —
  the artifact's freeze history lives at the **old** path, which artifact-pairing cannot
  adjudicate. A rename with a similarity score below 100 carries through as `M`: the commit
  moved frozen text, which is the `PREREG-RUNEDIT` claim, not the `SAMECOMMIT` one.
- **What is deliberately NOT suppressed.** A results artifact genuinely added alongside its
  prereg still flags; `4062562` (the real `_inbox` violation) is retained. Verified against
  live history, not fixtures alone: the 2026-08-24 window drops 20 → 18, and every dropped
  finding is a relocation.
- **Residual (documented, no silent cap).** A prereg moved *and* materially edited by a run
  commit is reported as `PREREG-RUNEDIT` via the `R<100` branch, but
  `_prereg_edit_is_status_stamp_only` reads the new path without rename detection, so it
  sees the whole file as added and cannot grant the status-stamp exemption. That errs
  toward flagging, which is the safe direction for a report-only tool.

### B. A past `--asof` swept every commit up to HEAD (window upper bound)

`_window_commits` passed `--since` only. The window was therefore open at the top: `asof`
set the floor and HEAD set the ceiling, so **every** historical `--asof` returned the same
answer. Correct in the weekly case (`asof == today == HEAD`) and wrong for every re-run of a
past window.

- **Why it matters beyond tidiness.** §4.1 makes `today` injected *"so runs are deterministic
  and testable"* and §8 requires *"same inputs + same `asof` → byte-identical queue output."*
  Neither held for the git-based scanner. The earlier addenda's own
  *"verified against live history"* checks were valid when written (HEAD was then) but are
  not reproducible now — they cannot be re-derived by re-running with a past `--asof`.
- **The rule.** `--until {asof} 23:59:59` is now passed alongside `--since`.
- **Verified.** Re-running `asof=2026-08-17` now reproduces exactly the two findings that run
  actually emitted (`PREREG-RUNEDIT-3c7ca2f`, `PREREG-SAMECOMMIT-ab303d0`); before the fix it
  returned the full 08-24 set. Pre-2026-08-14 anchors (`7f60dad`, `efeda82`, `c050965`) are
  **not** re-verifiable in this tree at all — the public repo's history begins at
  `027a729` *"Initial public release"* (2026-08-14); those anchors live in
  `first-passage-archive`. Recorded here so a future reader does not mistake an empty
  historical window for a regression.

### Tests

`tests/governance/test_sentinel.py` — `test_preregistration_scan_ignores_archival_move`
(freeze → run → `git mv` to `lab/archive/`, clean throughout),
`test_changed_files_skips_pure_move_but_keeps_edited_move` (the `R100` vs `R<100` boundary),
and `test_preregistration_scan_excludes_commits_after_asof`. All three were confirmed to
**fail against the pre-fix module** before being accepted — a guard that passes either way
guards nothing.

## Addendum — 2026-08-03: `_is_prereg_artifact` name-matching is documents-only

The name-based branch matched `"PREREG"`/`"FREEZE"` anywhere in a basename, on **any**
extension. A *runner script* whose filename described what it does therefore classified
as a pre-registration — and §4's scaffold-safe rule (runner `.py`, `panel.csv`,
`coverage.json` alongside a prereg is clean) never got the chance to apply, because the
scaffold *was* the thing being read as the prereg.

- **How it surfaced.** The 2026-08-03 weekly run emitted `PREREG-SAMECOMMIT-c050965`
  against [`lab/analysis/harvest/driftex_2026-08/RESULTS.md`](lab/analysis/harvest/driftex_2026-08/RESULTS.md),
  naming `run_phase123_freeze_tstar.py` as Q-DRIFTEX-1's pre-registration. It is a
  Phase-1–3 runner. The real prereg —
  [`2026-08-01-drift-exhaustion-mechanism-preregistration.md`](docs/briefs/pre-registration/2026-08-01-drift-exhaustion-mechanism-preregistration.md)
  — was frozen in `26cad59` (*"FREEZE Q-DRIFTEX-1 pre-registration"*), verified a **proper
  ancestor** of the results commit. That is the gold-standard shape reported as a violation:
  the check inverted its own verdict on the one commit in the window that complied.
- **The rule.** The name-based branch now requires `.md`. The `_PREREG_DIR` prefix branch
  is untouched — that directory is authoritative by placement, not by filename.
- **Why `.md` is the right line, on evidence.** Across all history, every genuine
  name-matched prereg outside the prereg directory is markdown (13/13), and the prereg
  directory itself is 75/75 markdown. The only two non-markdown matches in the entire
  repo are false: this runner and `lab/research_utils/prereg_paths.py`.
- **What is deliberately NOT suppressed.** A prereg *document* added alongside its results
  still flags (negative control in tests). Verified against live history rather than
  fixtures alone: the 07-27 window still emits exactly `PREREG-SAMECOMMIT-7f60dad`, and the
  `efeda82` anchor violation is still caught. The 2026-08-03 window drops 1 → 0.
- **Residual.** A pre-registration recorded in a non-markdown document (`.txt`, `.rst`) and
  placed outside `_PREREG_DIR` would now be missed. No such artifact exists in the repo;
  recorded here rather than left as a silent cap.
- **Tests.** `tests/governance/test_sentinel.py` — `test_prereg_name_match_is_documents_only`
  (the runner, the helper module, a `.json` freeze output; document forms still classify)
  and `test_pair_violations_ignores_freeze_named_runner_with_results` (the real `c050965`
  file set), plus `test_pair_violations_still_flags_real_same_commit_prereg_doc` as the
  negative control.
- **Why it mattered enough to fix.** Same argument as the 07-27 split, one step worse:
  §7.3 makes near-silence the design goal, and this finding was not merely mislabelled —
  it accused the compliant case. Two consecutive weeks of a wrong `prereg` finding is how
  the category stops being read.

## Addendum — 2026-07-27: `precondition_scan` honours a discharged verification pass

The C2 calendar check flagged **any** `[M]`/`[L]` year-row Tag cell. That reads the
precondition as *"is every cell `[H]`?"* when §4.1's actual input is *"is the pre-slate
verification pass outstanding?"* — the two diverge whenever a pass runs and
**deliberately keeps** a soft tag.

- **The divergence, observed.** The calendar moved into `ops/instruments/USDCAD.md`
  (inlined by `abb12ae`; the scanner followed the move correctly). Its
  2026-08-08 verification was **DISCHARGED 2026-07-02** (programme-audit R6), upgrading
  2025 `[M]→[H]` and 2026 YTD `[L]→[M]` — YTD held at `[M]` on purpose, a partial-year
  label pending the year-end full-year append. The cell-only check re-flagged that
  deliberate cell on the 2026-07-27 weekly run, and would have re-flagged it every week
  through year-end. Report-only, so it cost attention, not correctness — but a scanner
  whose job is *to mostly say nothing* (§7.3) cannot afford a standing false positive.
- **The rule.** Suppress when the regime-calendar section itself carries a line naming
  **this slate's date** alongside `DISCHARGED`. Scoped to the section (not the whole
  ledger) and to the slate date, so a discharge for a *different* slate does not
  suppress — that negative control is a test, not a comment.
- **What is deliberately NOT suppressed.** An `[M]`/`[L]` cell with no discharge record
  still flags; the sibling `PRECOND-rule2-triplog-starved` is untouched and still fires
  against the live tree. The fix narrows one predicate; it does not soften the gate.
- **Tests.** `tests/governance/test_sentinel.py` — the discharge-clean case and the
  other-slate negative control, alongside the retained cell-only detection fixture.
- **Residual (documented, no silent cap).** `SLATE_DATE` remains the single hard-coded
  slate (spec §9 generalization is still future work), so the discharge match is only as
  current as that constant. When the slate rolls to 2026-11-08, the 07-02 discharge stops
  matching and the check re-arms — which is the intended behaviour, not a regression.

## Addendum — 2026-07-27: `preregistration_scan` splits added-prereg from edited-prereg

The 07-02 check treated a prereg that was **added** with the results and one merely
**modified** by the run commit as the same violation, under one ID and one message
("the freeze is self-attested, not git-verifiable"). For the modified case that message
is **false on the facts** — the freeze is often a named ancestor commit.

- **How it surfaced.** The 2026-07-27 weekly run emitted three `PREREG-SAMECOMMIT`
  findings. Investigation: **one real** (`7f60dad`, Q-INVENTORY-1 — prereg `A`dded
  alongside its closure *and* `RESULTS.md`; the parent brief was still
  `OPEN — DRAFT (operator ratification owed)` at its ancestor commit, so the
  DRAFT→FROZEN moment is attested only in the results commit). **Two mislabelled**
  (`b0189db` Q-COSTGEO-1, `6812146` Q-COSTGEO-3) — each the *gold-standard* shape
  (prereg added `de38fca`/`db9ce1f`, signed+FROZEN `a51ce0a`/`4aa9971`, all proper
  ancestors) plus a **one-line** `**Status:**` closure stamp in the run commit.
- **The split.** `_pair_violations` now carries the prereg's git status, and the scan
  emits `PREREG-SAMECOMMIT` (added — unchanged message) or `PREREG-RUNEDIT` (modified
  beyond the status header — its own, weaker, accurate claim). `PREREG-RUNEDIT` is a
  cheap proxy for the `3935d2c` verdict-logic class the 07-02 addendum listed as a gap;
  it narrows that gap without pretending to close it (semantic diffing still isn't done).
- **Stamp exemption.** `_prereg_edit_is_status_stamp_only` reads the commit's diff for
  that file and exempts it when every touched line is the `**Status:**` header — the
  repo's closure convention (4 of 36 preregs carry such a stamp), now ratified in
  `operational_rules.md` Rule 8 sub-rule 7. Fail-open: an unreadable diff exempts,
  per this module's never-a-false-positive contract.
- **Verified against live history**, not just fixtures: the same window that emitted
  three findings now emits one — `PREREG-SAMECOMMIT-7f60dad`.
- **Tests.** `tests/governance/test_sentinel.py` — status-tagging units for both
  branches, plus git-integration tests for the exempt stamp and for a substantive
  edit (a moved gate threshold) that must flag as `PREREG-RUNEDIT`.
- **Why it mattered enough to fix.** §7.3 makes near-silence the design goal. A finding
  that is wrong on the facts two times in three is worse than a noisy one — it trains
  the operator to discount the whole category, including the one real hit.

## Addendum — 2026-07-02: `preregistration_scan` (freeze-before-results commit hygiene)

A fourth Tier-1 scanner, added from the **2026-07-01 programme audit (R4)** and
enforcing `operational_rules.md` Rule 8 sub-rule 7. It differs from the original
three in that it reads **git history**, not just working-tree file contents —
but keeps the same contract: report-only, fail-open, one `Finding` per hit,
routed via the existing vocabulary.

- **What it flags.** A commit that **introduces** a results/closure artifact
  (`docs/briefs/*closure*`, `lab/analysis/**/{RESULTS,FINDINGS}*`) and, in the
  **same commit**, adds-or-modifies a **corresponding** pre-registration (the
  adds-vs-modifies conflation was split into two findings on 2026-07-27 — see the
  addendum above; the paragraph below describes the check as originally shipped)
  (`docs/briefs/pre-registration/*`, `*PREREG*`, `*FREEZE*`, `docs/spec/PREREG-*`,
  `lab/analysis/<run>/preregistration.md`). Correspondence = shared question-ID
  stem (`Q-…-N`) or shared `lab/analysis/<run>/` directory. A freeze commit
  carrying a prereg **alongside scaffold** (runner `.py`, `panel.csv`,
  `coverage.json`) is clean — only prereg+results together trips. Routed
  **Action**, category `prereg`.
- **Why it's git-based.** The convention is *inherently* about commit boundaries
  ("frozen before the run" = a separate, earlier commit), so the anti-pattern is
  invisible to a working-tree scan. `--commit-lookback-days` (default 14) bounds
  the window from `asof`; merge commits are skipped.
- **Empirical basis.** Anchor violation `efeda82` (prereg + closure + clean-vintage
  RESULTS in one commit) is flagged; the gold standard `46f47d1` (freeze) →
  `913829b` (run) is clean; Q-ORB-FRIDAY-1 / `3935d2c` is correctly **not**
  flagged by artifact-pairing because its prereg (`711d499`) is a true ancestor —
  its violation was a post-freeze *verdict-code* edit, a documented v1 gap.
- **Shallow-clone safety.** In a shallow clone (this remote env, CI), graft-boundary
  commits have no reachable parent; their real delta is invisible, so they are
  **skipped**, never flagged on their whole tree. The audit is complete only
  against a full-history clone (operator local / pre-commit context); on a shallow
  clone it covers the recent window whose parents are present.
- **Tests.** `tests/test_sentinel.py` — classifier + pure-pairing units (incl. the
  scaffold-safe negative), a git-integration test (freeze→run clean, same-commit
  flagged), the parentless/graft-boundary skip regression, and non-git fail-open.
- **Not covered (v1, documented — no silent cap).** Post-freeze edits to *verdict
  code* in a run commit whose prereg markdown is a proper ancestor (the `3935d2c`
  class); cross-tree prereg↔results pairs sharing neither a Q-ID nor a directory
  (still caught whenever any one corresponding pair is present in the commit).
