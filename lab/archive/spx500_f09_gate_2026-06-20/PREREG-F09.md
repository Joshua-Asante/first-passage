# Q-SPX-F09 — Is the SPX500 momentum/reversion regime state PREDICTIVELY observable with actionable lead?

**Status:** `CLOSED-FALSIFIED` (see [`CLOSURE-F09-falsified.md`](CLOSURE-F09-falsified.md))
**Authored:** 2026-06-20
**Closed:** 2026-06-20 — FALSIFIED, all 3 §6 triggers fired (Δ=−2.18bps / perm p=0.64 / halves flip); directional axis collapses
**Authors:** Joshua + Claude Code
**Parent question:** Q-SPX-IDENTIFY (INQHIORI Identify, 2026-06-20 — the 30-family feature-space catalog). F09 is the catalog's load-bearing gating family.
**Loop:** INQHIORI Notice/Investigate — closure gated on a pre-registered conditional-separation falsifier with permutation + stationarity + drop-top-k robustness.
**Artifact path:** `lab/analysis/spx500_f09_gate_2026-06-20/PREREG-F09.md`

---

## §0 — Rule 0 reads (production-source verification)

Read **before** authoring this pre-registration, this session:

- `core/bar_export_loader.py` — anchor `5cba8af` (verified `git log -1` 2026-06-20). BAR EXPORT v0.1 decode contract: `Signal = epoch_ms|o|h|l|c|v`; `epoch_ms` is bar-open **UTC** (authoritative over the chart-TZ `Date and time` column); Entry `Price` == encoded close cross-check is the format-drift detector.
- `core/tv_export_loader.py` — anchor `b294993` (verified 2026-06-20). `PRICE_COL_BY_INSTRUMENT` map; **US500/SPX500 not registered** → this harness decodes the Signal column directly and cross-checks against `Price USD` (the index-CFD price column) self-contained.
- `ops/instruments/SPX500.md` — anchor `aeee7a9` (verified 2026-06-20). Instrument ledger: 3-null/3-family SNAG; durable findings F1–F10, D1/D2, W1–W4; cost structure (1.0pt round-trip / asymmetric −140.27 long swap / tradeability floor `stop ≥ max(1pt,cost)`); canonical feed = TV/Pepperstone US500 (point_factor=1).
- Identify-phase corpus characterization (this session, deterministic): 5m = 385,370 bars 2021-01-03→2026-06-11 contiguous, **0 undecodable / 0 cross-check fails**; daily-resampled regime map (1695 trading days): daily AC1 **+0.012 (2024) vs −0.244 (2025)**, full-sample −0.094.

**Data provenance / fidelity caveat:** the 4 BAR_EXPORT pages are the canonical Pepperstone US500 chart feed packed into a TV List-of-Trades export. Prior BAR_EXPORT↔TV-chart parity was byte-identical on a 1H overlap (ledger session log 2026-06-19), but a 5m parity re-validation has NOT been run. **This is a staging-grade Identify/Notice result, not gate-bearing for any lock** (TV CSV canonical-feed policy 2026-06-12). No `core/`, lock, allocation, or dd_protection touch.

---

## §1 — Context & motivation

The Identify-phase catalog (2026-06-20) concluded that **every** plausible directional family on US500 5m/15m (F01 opening-range, F02 expansion, F06 ETH-ORB, F25 event-window, F32 post-large-move) is momentum-vs-reversion **regime-conditional**, and that the regime sign physically flips in-sample (2024 daily AC1 +0.012 → 2025 −0.244, a tariff-shock **discontinuity**, not a slow drift). The catalog named **F09 (trend-state conditioning)** the load-bearing gate: *if* the regime state cannot be observed predictively with enough lead to act before the flip, **all directional halves collapse together** into thin-drift (cost-dead under the ~2.3 bps floor) and only the direction-agnostic primitives (F07/F08/F34/F10) survive as risk tools, not alpha. Testing F09 first is the highest P(changes verdict)÷cost test in the catalog (strategy-validation §0).

---

## §2 — Prior art / lineage

- **Q-SPX-IDENTIFY catalog** (2026-06-20) — F09 = load-bearing gate; this brief is its first falsification.
- **D1 / NOCT-SPX-001** (FALSIFIED 2026-06-07) — a *conditional* channel that failed to separate from its unconditional baseline (sep t=0.34). F09 is the same *separation-must-beat-unconditional* logic at the regime-state level; D1's failure mode (conditioning that adds nothing) is the prior.
- **D2 / Q-ICT-SWEEPFVG-1** (FALSIFIED 2026-06-17) — died on **robustness** (drop-top-3 negative, thirds back-loaded) after a point estimate passed. F09's drop-top-k + halves robustness gates are pre-registered *because* of D2.
- **Decompound re-MC HOLD** (2026-06-07, [[project_decompound_remc_canonical_shift_2026_06_07]]) — portfolio risk is strongly regime-split (2020-23 chop vs 2023-26 trend); "regime state is load-bearing but hard to act on predictively" is an established cross-instrument prior. F09 is the SPX500 alpha-side analogue of that same lead-time problem.
- **Q-REGIME-1** (FALSIFIED 2026-05-26) — a specific 2024-04-30 regime break is a local-max, priors-shifting; supports treating regime sign as real but discontinuous.

This question is novel for SPX500 (no prior loop tested regime-state lead-time on the alpha side).

---

## §3 — Question (Q-SPX-F09)

**Pre-Q gate test (symptom-only rephrase):** the question names what is unknown (whether the regime state has predictive lead), not a fix (it does not bake in "use a 63-day AC1 filter" as the answer — that is merely the pre-registered instrument).

**Q-SPX-F09:** Does a trailing, strictly-causal estimate of the SPX500 daily momentum/reversion regime state carry **predictive** content for the *forward* sign of daily continuation — i.e., does conditioning on the trailing state separate forward momentum payoff with enough lead to beat the unconditional winner — or is the state only **descriptive** (it identifies the regime in hindsight but flips too late to act on)?

---

## §4 — Falsifiable hypothesis (H-F09)

**Instrument (frozen, single primary — no sweep):**
- Daily returns `r_t = ln(close_t / close_{t-1})`, `close` = last 5m close per ET calendar day (5m merged corpus, 2021-01-03→2026-06-11).
- Trailing regime state `S_t = sign( AC1( r over [t-L .. t-1] ) )`, lookback **L = 63 trading days (~1 quarter)**, computed using returns **through day t−1 only** (strictly causal; no `r_t`).
- 1-day time-series momentum payoff `m_t = sign(r_{t-1}) · r_t` (known-at-open position `sign(r_{t-1})`, realized on `r_t`). `E[m_t] > 0` ⇔ momentum regime; `< 0` ⇔ reversion regime.
- **Primary statistic — conditional separation:** `Δ = E[m_t | S_t = momentum] − E[m_t | S_t = reversion]`.

**H-F09:** *If* the regime state is predictively observable with lead, *then* on days the trailing estimator flags MOMENTUM the forward momentum payoff is positive and on REVERSION days it is negative, so `Δ > 0` and the separation survives a label-alignment-breaking permutation, is sign-stable across halves, and is not carried by a handful of days; *otherwise* the state is descriptive-only and the directional axis collapses.

**Reject H-F09 (FALSIFIED — gate closes, directional axis collapses) if ANY of:**
- `Δ ≤ 0`, OR
- `Δ > 0` but cyclic-rotation permutation `p ≥ 0.10` (separation indistinguishable from chance alignment), OR
- `Δ` sign-flips between the two time-halves (non-stationary — the estimator works in one era only).

**Accept H-F09 (RESOLVED — gate feasible, advance to test whether intraday triggers inherit it) if ALL of:**
- `Δ > 0` AND `E[m|mom] > 0` AND `E[m|rev] < 0` (both conditional means correctly signed), AND
- cyclic-rotation permutation `p < 0.10`, AND
- `Δ > 0` in **both** time-halves (sign-stable), AND
- `Δ > 0` after **drop-top-5** highest-`|m_t|` days (not few-day-carried).

**Ambiguous-hold if:** `Δ > 0` AND permutation `p < 0.10`, but it FAILS the stationarity OR drop-top-5 robustness (real but fragile — the D2 fate). Re-test trigger named in §6.

---

## §5 — Forbidden moves

- **Sweeping the lookback L and reporting the best.** L=63 is the single pre-registered primary. L∈{42,126} are computed as **descriptive robustness only** and CANNOT change the verdict. Tuning L to flip the verdict = the multiplicity trap (strategy-validation §5).
- **Swapping the estimator family to rescue a failure.** Primary = trailing-AC1-sign. Efficiency-ratio (Kaufman ER) sign is computed as **one** pre-registered robustness echo, not a verdict alternative. Trying AC1→ER→ADX→… until one passes is forbidden (Trap #12 p-hacking).
- **Any look-ahead in `S_t`.** Using `r_t` or later in the state, or ending the AC1 window at `t` instead of `t−1`, would make F09 spuriously PASS — this is the single highest-risk defect and the adversarial harness audit (§7 Phase 2) must HALT on any leakage (M-15 / [[feedback_pine_offset_port_faithfulness_anchor]]).
- **Deleting 2022 (bear) or 2025-Q2 (tariff shock) as "outliers."** Those ARE the regimes the gate must survive; outcome-conditional deletion is the forbidden §5 D-test.
- **Amending the §4 thresholds after seeing Δ.** Any post-data threshold move voids the run (Trap #12); close AMBIGUOUS and re-open with new criteria stated up front.
- **Substituting the intraday horizon to rescue a daily FALSIFIED without a fresh pre-registration.** A daily-state failure does not get silently re-scored intraday; that is a new Q with its own PREREG.

---

## §6 — Gate criteria (closure verdict)

Pre-registered before any scoring script runs (§8). `Δ` in daily-log-return units.

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | `Δ>0` AND `E[m\|mom]>0` AND `E[m\|rev]<0` AND perm `p<0.10` AND `Δ>0` in both halves AND `Δ>0` after drop-top-5 | Gate feasible → advance to the *inheritance* test (does an intraday trigger keep the edge net of ~2.3 bps?). Does NOT itself authorize a trade or consume a SNAG slot. |
| `FALSIFIED` | `Δ≤0` OR perm `p≥0.10` OR `Δ` sign-flips across halves | **Directional axis collapses.** Only primitives F07/F08/F34/F10 survive (as risk/sizing, not alpha). Close the directional families; capture the lesson. |
| `AMBIGUOUS-HOLD` | `Δ>0` AND perm `p<0.10` but fails stationarity OR drop-top-5 | Real-but-fragile (D2 fate). HOLD; re-test trigger: re-score when a 5m parity-validated panel or a fresh out-of-sample regime (post-2026-06) is available. |

**Cost note (secondary, not a gate):** if RESOLVED gross, report whether `Δ` clears the ~2.3 bps round-trip per position change. The gate is about predictive *lead* (gross separation); cost binds at the downstream intraday-inheritance step, not here.

---

## §7 — Execution plan (self-executing, single session)

- **Phase 0 — Rule-0 reads.** Done (§0). Data integrity already verified (0 undecodable / 0 cross-check fails).
- **Phase 1 — Build the harness** (`f09_gate.py`): daily resample (ET) → `r_t`, `m_t`; strictly-causal `S_t` (L=63, ending t−1); conditional means + `Δ`; cyclic-rotation permutation (10,000 rotations, preserves each series' autocorrelation, breaks S↔m alignment); halves; drop-top-5/10; per-year descriptive; the 2024→2025 transition slice; L∈{42,126} + ER-sign robustness echoes (descriptive only).
- **Phase 2 — Adversarial harness audit BEFORE scoring** (M-15 discipline; the ledger's twice-audited REVCON precedent). Parallel auditors hunt look-ahead leakage, lag/off-by-one in `S_t`, permutation-null correctness, drop-top-k basis. **HALT and fix on any verdict-corrupting defect before the verdict is read.**
- **Phase 3 — Score ONCE, assert §6 gate, write closure** (`CLOSURE-F09-*.md`), append dated disposition to `ops/instruments/SPX500.md`.

---

## §8 — Verdict pre-registration

This file IS the pre-registration. The §4/§6 thresholds are fixed as of authoring (2026-06-20), **before** `f09_gate.py` exists. Firewall caveat: the historical data is already in hand (no commit-before-data firewall is possible as with a future out-of-sample page), so the integrity rests on (a) the falsifier being fixed before the scoring logic is written, and (b) the §5 forbidden-move list (no L-sweep, no estimator-swap, no threshold move). The adversarial audit (§7 Phase 2) is the leakage backstop.

Pre-registration anchor: authored at HEAD `7a50011` (2026-06-20); `f09_gate.py` does not yet exist at authoring time.

---

## §9 — Closure record format

- **RESOLVED:** `CLOSURE-F09-resolved.md` — Δ, conditional means, perm p, halves, drop-top-k, transition slice; the inheritance-test it unlocks.
- **FALSIFIED:** `CLOSURE-F09-falsified.md` — which trigger fired; the directional-axis-collapse consequence (which catalog families die); lesson candidate.
- **AMBIGUOUS-HOLD:** `CLOSURE-F09-ambiguous.md` — the fragility that fired; re-test trigger + date.

All include: verdict vs each §6 threshold, what this PREREG predicted vs what happened, lesson candidates with dated anchor.

---

## §10 — Audit hooks (runnable)

```bash
# Reproduce the scored verdict
python lab/analysis/spx500_f09_gate_2026-06-20/f09_gate.py --reproduce

# Confirm §0 anchors still resolve
git log -1 --format='%h' -- core/bar_export_loader.py    # expect 5cba8af (or later, re-verify decode contract)
git log -1 --format='%h' -- ops/instruments/SPX500.md

# Leakage assertion (the load-bearing check): S_t must not use r_t.
grep -n "shift" lab/analysis/spx500_f09_gate_2026-06-20/f09_gate.py   # state series must be lagged

# Forbidden-move audit: confirm no L-sweep drove the verdict
grep -n "L = 63\|LOOKBACK" lab/analysis/spx500_f09_gate_2026-06-20/f09_gate.py
```

---

## Pre-Lock Checklist

- [x] §0 paths read and anchored (commit hashes, 2026-06-20)
- [x] §3 passes symptom-only rephrase
- [x] §4 hypothesis falsifiable (binary §6 triggers)
- [x] §5 forbidden moves genuinely tempting (L-sweep, estimator-swap, outlier-deletion were all real temptations)
- [x] §6 gates have specific numerical triggers
- [x] §8 falsifier fixed before `f09_gate.py` exists
- [x] §10 audit hooks runnable
