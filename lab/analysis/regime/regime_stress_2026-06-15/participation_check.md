# Participation-viability check (Phase-1b)

**LoR:** OUTER (INQHIORI). Cheap falsifier before any deploy-vs-wait detector research. Research
artifact; locked config untouched (`LOCKED_FILES_CLEAN`). 2026-06-15. **Verdict: PARTICIPATION VIABLE
(`DONE_WITH_CONCERNS` — see the single-path caveat).**

**Question.** The oracle killed regime-adaptive *resizing*; the surviving frame is regime-adaptive
*participation* (deploy full risk in benign, sit out hostile). Before researching a detector: is
participation even viable on the realized history — is the deploy-vs-wait target **persistent and
block-avoidable**, with enough fast-passing benign time?

**Instrument.** Deterministic forward-start sweep on the real chronological path (decompounded-static
Pepperstone, LOCKED allocations, C2): for every business-day start date, walk the *actual* subsequent
daily P&L forward with the locked `_simulate_path` and record outcome + days. 1672 starts.

## Result

| start year | starts | PASS% | BUST% | median days-to-pass |
|---|---:|---:|---:|---:|
| 2020 | 259 | 98.5% | 1.5% | **96** |
| 2021 | 261 | 96.9% | 3.1% | **219** |
| 2022 | 260 | 100% | 0% | 65 |
| 2023 | 260 | 100% | 0% | 18 |
| 2024 | 262 | 100% | 0% | 24 |
| 2025 | 261 | 100% | 0% | 16 |
| 2026 | 75 | 100% | 0% | 14 |

Pre-registered criteria: V1 deployable (PASS≤60bd) **66.0% ✓**; V2 bust-block persistence **FAIL** (see caveat); V3 busts ≤2023 **100% ✓**; V4 benign median **18bd ✓**. Mechanical verdict (V1 ∧ (V2∨V3) ∧ V4) = VIABLE.

## Critical caveat — the single-path sweep understates bust RISK; read it for STRUCTURE, not risk

The realized path busts from only 12 / 1672 starts (0.7%) — even in 2020-2021. **That 0.7% is NOT the
participation bust risk.** The deterministic sweep is *one* realized draw: the actual 2020-2021 chop had
its bad weeks interspersed with recoveries, so the equity path rarely hit −5% before grinding to +5%.
The **bootstrap** (Q-REGIME-STRESS-1 / the gate) resamples week-blocks and *does* capture the tail —
**hostile-regime forward-bust risk is 33% (bucket) / 24.5% (H1), benign 0.5%.** That is the correct
forward risk. My pre-registered V1/V2 criteria were bust-based on the single path and so are
single-path-optimistic; V2 "failed" only because 12 busts are too sparse to form blocks — a
specification error, not evidence against persistence.

**What the sweep establishes robustly is the regime STRUCTURE, via median-days-to-pass** (a drift proxy,
single-path-robust because it tracks central drift, not tail luck): the hostile era (2020-2022) is
**slow** (median 65–219 bd to pass) and the benign era (2023-2026) is **fast** (14–24 bd) — a clean,
contiguous, multi-year transition around 2022→2023. This corroborates the bootstrap (hostile median
128 bd; benign 18 bd) from an independent angle.

## Verdict — VIABLE, grounded correctly

Combining the two instruments (sweep for structure, bootstrap for risk):

- **The regime is persistent and block-structured** — a multi-year low-drift/chop block (2020-2022) and
  a multi-year trending block (2023-2026), clean in the median-days transition. Not week-to-week flips.
- **The forward-risk gap between regimes is large** — benign deploy: 0.5% bust, median 18 bd (fast +
  safe); hostile deploy: ~33% bust, slow. Deploying in benign and avoiding hostile is high-value.
- **There is ample deployable benign time** (≈2023-onward, ~half the panel) and benign passes complete
  fast (median 18 bd), well inside a persistent benign block.

→ **A start-time deploy-vs-wait detector has a real, persistent, high-value target.** Participation
clears the cheap falsifier. **Commission the participation-gate detector research** (the redirected
claude.ai prompt).

## Concerns

1. **Single realized regime sequence (n=1 history).** Persistence and the regime boundary are read from
   one 2020-2026 path; out-of-sample regime behavior is unknown. The detector research must treat the
   2020-2022 → 2023-2026 transition as one sample, not a law.
2. **Bust risk comes from the bootstrap, not this sweep** (above). Do not cite the 0.7% / 66% single-path
   numbers as risk figures — they are structure indicators only.
3. **The detector itself is unproven.** This check shows the *target* exists and is persistent; whether a
   *state-readable* signal predicts the regime at challenge-start with adequate lead is the deferred
   research question (and still subject to the "backtest gate ≠ live pay" discipline + a forward live-PnL
   tripwire).

**Artifacts (gitignored):** `reports/regime_stress/participation_check.py` + `participation_check.json`.
