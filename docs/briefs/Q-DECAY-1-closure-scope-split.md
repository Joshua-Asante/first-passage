# Q-DECAY-1 — closure: earliest decay detector vs. realized drawdown

**Loop:** OUTER (INQHIORI), fast-follow to Q-NEFF-1. **Domain:** data.
**Status:** CLOSED — **SCOPE-SPLIT**. **Return:** `DONE_WITH_CONCERNS`.
**Reversibility:** analysis only. No detector built; no `core/` / `dd_protection` / `ecr_rolling` / `firm_rules` change; no real leg retired. Harness + full record: [`lab/analysis/q_decay_1_2026-07-10/`](../../lab/analysis/q_decay_1_2026-07-10/RESULTS.md).
**Consumer:** the 2026-08-08 quarterly regime check and its `accept-beta` fork.

---

## H (falsifiable, per scope)

> The portfolio has no decay detector cheaper than realized drawdown at either scope — for (a) single-leg and (b) common-mode edge death, the earliest signal forcing a response is the drawdown the decay causes, not a pre-registered live-vs-backtest expectancy trigger that fires first.

**Verdict: SCOPE-SPLIT.**

| Scope | Verdict | Basis |
|---|---|---|
| Guardian per-leg | **FALSIFIED (narrowly)** | The Guardian decay-gate CUSUM is a pre-registered, cheaper-than-DD, PnL-computable-at-WATCH expectancy detector. Fires at ~0.2% portfolio DD vs dd_protection's 1.5%; its rate tracks decay (14%→75%→98% control/step/kill) while dd_protection stays decay-blind (40%→48%→63%, always at ~1.58% DD, no attribution). **But** it is Guardian-only, **dormant** (no live venue), and its terminal DECAYED verdict is **classifier-interlocked off** (DP-4 — no validated exogenous regime classifier exists). |
| DJ30 / NAS100 / Aegis per-leg | **CONFIRMED** | No decay detector exists. dd_protection fires on normal variance (~40% with zero decay) and never attributes to a leg. |
| Common-mode / family | **CONFIRMED** | No family-level (k-of-N / aggregate-expectancy) monitor exists. ECR is execution-fidelity (a ratio blind to edge magnitude, and dormant). Under genuine common-mode edge death, the earliest portfolio-DD signal arrives only after a **median max DD of ~11.7% — past the 5% firm bust line** (drawdown "detects" it only after the account has busted). Even Guardian's single-leg CUSUM is late for the family (~4.7% portfolio DD). |

## Premise verification (§0.5-A / confabulation guard)

- **ECR is NOT a live decay detector** (the brief's central worry). `journal_review`: `counterfactual_pnl = sig.pnl`, `ratio = realized/counterfactual` — a ratio that divides out edge magnitude; a decaying edge executed faithfully keeps ECR ≈ 1, and total edge death sends the denominator ≤ 0 → NOT-SCORED, never BREACH. It needs live DXTrade fills that no longer accrue. `PREREG-NAS-ECR-1` is PARKED/UNREACHABLE.
- **No family-level monitor exists** → the §0.5-A hard-stop did **not** trigger; proceeded and folded the real Guardian CUSUM into the harness as the candidate.
- **A per-leg detector (Guardian) does exist** → H's premise was not clean; reported and continued per §0.5-A.

## Drawdown-paid-before-detection (the cost input to `accept-beta`)

- **Guardian per-leg:** ~0.2% portfolio DD (CUSUM) vs ∞ for drawdown-only (dd_protection never carries decay information for one small leg — it never even engages on single-leg decay).
- **DJ30 / NAS100 / Aegis per-leg:** no cheaper-than-DD signal at all.
- **Common-mode:** no cheaper-than-DD family signal; drawdown-only, and unambiguous only at ≥ the 5% bust line. **Accepting the shared-mechanism (Q-MECH-1) family means accepting that common-mode edge death is invisible until it has already cost a bust-line drawdown.**

## Surfaced candidate — OPERATOR DECISION, NOT BUILT (§5)

The gap is real and the design to close it already exists but is unbuilt: extend the Guardian decay-gate five-element spine (Q-GUARDIAN-DECAY-1 §7) to DJ30 / NAS100 / Aegis (each needs its own per-trade-R envelope, favorable-regime classifier, and degradation alternative — none built), **plus** a family-level aggregate (e.g. a k-of-N "legs in WATCH" counter or a portfolio-expectancy CUSUM) to cover common-mode. Two standing blockers make this non-trivial and keep it a decision, not an action:
1. **No validated exogenous regime classifier** (VIX>20 falsified 2026-06-22; endogenous OHLC falsified) — the same DP-4 interlock that caps the Guardian gate at WATCH caps any extension.
2. **All four legs are off their live venues** (CFD retired; futures-prop demoted/BLOCKED) — every CUSUM accrues zero in-regime trades until a leg is live somewhere, so even a full build is **forward-armed and dormant** today.

This is an output for the operator + Cursor (human-in-loop monitoring change), consistent with the standing entry/retirement asymmetry Q-GUARDIAN-DECAY-1 opened. **CC does not implement it.**

## Concerns (DONE_WITH_CONCERNS)

1. Feasibility-limited harness — synthetic inputs (panels gitignored/absent in worktree, Rule 9); real calibration deferred to local `build_envelope.py`. Ordering/structure calibration-robust; sim-weeks illustrative.
2. Common-mode fire-order is shock-sensitive (at `kill` severity drawdown fires before the CUSUM) — does not flip the coverage verdict.
3. H premise not clean (existing Guardian detector).

## Re-check hook

**2026-08-08 quarterly regime check:** feed this closure into the `accept-beta` fork as the "does accepting a shared-mechanism family come with common-mode blindness, and at what drawdown cost" input. Answer: **yes — common-mode is UNCOVERED; the cost is a bust-line drawdown before any signal.** Re-arm condition for the whole detector question: a leg goes live on some venue (fills accrue) **and** a regime classifier passes its own robustness gate.

## Anchors
`dd_protection.py`@`6f5480b` · `firm_rules.py`@`57f491c` · `portfolio_mc.py`@`83e589f` · `ecr_rolling.py`@`a85e340` · `journal_review.py`@`2555b9f` · `operational_rules.md`@`6bcb034` (Rule 11) · `guardian_decay_gate_2026-06-25/`@`8212ff0` (README@`8ecf7be`) · `PREREG-NAS-ECR-1`@`73eeab6` · `time_to_pass.py`@`53f59f5`.
