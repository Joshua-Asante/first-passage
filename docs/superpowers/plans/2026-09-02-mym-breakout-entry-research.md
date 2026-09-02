# MYM Breakout Entry Research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and run a reproducible, costed, chronological study of a small catalogue of MYM opening-range breakout entry families.

**Architecture:** Keep vendor data in ignored local workspace directories and use the canonical BAR EXPORT v0.2 loader. Put the pure causal simulator and metrics in one focused research module, the frozen catalogue/config in JSON, and generated machine-readable outputs plus a concise report in a dated `lab/analysis` study directory.

**Tech Stack:** Python 3, pandas, numpy, pytest, repository BAR EXPORT v0.2 loader

**Spec:** User brief attached 2026-09-02; frozen choices are recorded below because no separate repository design spec governs this one-off study.

## Global Constraints

- Input is the canonical parsed MYM v0.2 export, never an ad hoc CSV interpretation.
- Instrument constants are `mintick=1.0` and `pointvalue=0.5`, verified against the v0.2 sidecar and `ops/instruments/MYM.md`.
- Baseline setup is a 30-minute 08:30–09:00 America/Chicago opening range, entries through 15:00, force-flat by the final eligible RTH bar, one trade per session, one MYM contract.
- Initial price risk is 300 points = $150; target is 300 points = 1R.
- Headline costs are $0.91 commission/fees per side plus one tick adverse execution per side; sensitivities use 0, 2, and 4 adverse ticks per side.
- Intrabar target/stop ties resolve to the stop; same-bar long/short entry ambiguity produces no fill; gap-through stops use the worse bar-open/stop price.
- Entry decisions use only completed or current-bar information available at the modeled decision time.
- Frozen families are immediate stop, close-confirmed, 10-point buffered stop, first 25-point retest, and two-close momentum confirmation.
- Chronological periods are development 2019-05-05–2022-12-31, validation 2023-01-01–2024-12-31, and untouched holdout 2025-01-01–2026-07-31.
- Raw vendor CSVs and local parsed outputs are never committed.

---

### Task 1: Causal simulator and accounting

**Files:**
- Create: `lab/analysis/mym_breakout_entry_2026-09/run_research.py`
- Test: `tests/lab/test_mym_breakout_entry.py`

**Interfaces:**
- Consumes: canonical `time,open,high,low,close,volume` bars plus sidecar metadata.
- Produces: `build_sessions`, `simulate_family`, `summarize_trades`, and `run_catalogue` pure functions.

- [ ] **Step 1: Write failing tests** for stop-first ties, gap-through stop fills, per-side cost accounting, entry timing/leakage, metric arithmetic, long/short separation, and chronological period labels using hand-derived fixtures.
- [ ] **Step 2: Run tests to verify RED** with `python -m pytest tests/lab/test_mym_breakout_entry.py -q` and confirm failures are missing-module or missing-behavior failures.
- [ ] **Step 3: Implement minimal simulator** with causal session construction, the five frozen entry rules, conservative fills, one-contract $/R accounting, and deterministic metrics.
- [ ] **Step 4: Run tests to verify GREEN** with the same command, then run the full focused test file after refactoring.

### Task 2: Frozen configuration and data audit

**Files:**
- Create: `lab/analysis/mym_breakout_entry_2026-09/config.json`
- Create: `lab/analysis/mym_breakout_entry_2026-09/data_audit.json`
- Modify: `lab/analysis/mym_breakout_entry_2026-09/run_research.py`

**Interfaces:**
- Consumes: parsed bar CSV and v0.2 metadata sidecar.
- Produces: validated audit fields, configuration hash, complete declared trial ledger, and nonzero exit on schema/metadata/order defects.

- [ ] **Step 1: Add failing validation tests** for wrong symbol, tick/point value, unsorted timestamps, duplicates, invalid OHLC, and missing required configuration fields.
- [ ] **Step 2: Run the validation tests to verify RED.**
- [ ] **Step 3: Add minimal audit/config validation**, including date range, gap distributions, session coverage, bar interval, metadata, duplicate count, and limitations.
- [ ] **Step 4: Run focused tests to verify GREEN.**

### Task 3: Chronological study, robustness, and uncertainty

**Files:**
- Modify: `lab/analysis/mym_breakout_entry_2026-09/run_research.py`
- Create: `lab/analysis/mym_breakout_entry_2026-09/results.json`
- Create: `lab/analysis/mym_breakout_entry_2026-09/trades.csv`

**Interfaces:**
- Consumes: Tasks 1–2 simulator/config and canonical local bars.
- Produces: complete family/period/side comparison, cost sensitivity, stop-risk distribution, 250/300/350-point neighborhood checks, deterministic session-bootstrap confidence intervals, and final holdout adjudication.

- [ ] **Step 1: Add failing tests** for bootstrap determinism, max drawdown, profit factor edge cases, and neighborhood/cost result cardinality.
- [ ] **Step 2: Run tests to verify RED.**
- [ ] **Step 3: Implement and run development plus validation**, select the simplest candidate only by frozen thresholds and adequate sample size, then access holdout once.
- [ ] **Step 4: Save every declared cell and trade**, including failures, with config/input hashes and exploratory versus holdout labels.
- [ ] **Step 5: Run focused tests and reproduce `results.json` byte-for-byte.**

### Task 4: Report and repository integration

**Files:**
- Create: `lab/analysis/mym_breakout_entry_2026-09/RESULTS.md`
- Modify: `lab/CATALOG.md`
- Modify: `ops/instruments/MYM.md`

**Interfaces:**
- Consumes: machine-readable audit/results from Task 3.
- Produces: concise data audit, hypothesis catalogue, methodology, baseline/candidate comparison, chronological and side results, sensitivity/robustness, limitations, conclusion, and next step.

- [ ] **Step 1: Generate the report from results**, explicitly stating whether thresholds are robustly met and flagging inadequate sample sizes.
- [ ] **Step 2: Add the retained study pointer and a dated MYM ledger disposition** without altering prior findings.
- [ ] **Step 3: Run report link/format checks and the relevant repository gates.**

### Task 5: Final verification and delivery

**Files:**
- Review all files above and repository status.

**Interfaces:**
- Consumes: completed study.
- Produces: clean scoped commit and pull request.

- [ ] **Step 1: Run focused tests, full relevant tests, boundaries, and manifest dry-run.**
- [ ] **Step 2: Re-run the research command and verify hashes/results.**
- [ ] **Step 3: Review `git diff`, confirm raw/proprietary/temp/unrelated files are excluded, and preserve all pre-existing changes.**
- [ ] **Step 4: Commit only scoped files on the current branch.**
- [ ] **Step 5: Push and create a pull request; if credentials/network block this, report the exact limitation and preserve the local commit.**

## Execution deviation recorded 2026-09-02

The first implementation computed all intended-holdout cells even though validation selected no
candidate. That access cannot be undone. Final artifacts label the period
`consumed_exploratory_not_confirmatory`, make no holdout-confirmed claim, and require genuinely new
forward data for any future Confirm attempt. The complete 60-cell trade ledger is local-only because
it contains vendor-derived prices/timestamps; `results.json` records its row count and SHA-256.
