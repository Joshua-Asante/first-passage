**Theme:** regime
**Status:** ACTIVE — dd_protection trigger re-MC on proposed de-risk bundle
# Q-DDTRIG-1 — dd_protection trigger re-MC on the proposed de-risk bundle (2026-06-07)

**Question.** Given the proposed all-unlocked bundle, does tightening the
`dd_protection` trigger **1.5% → 1.0%** (DD_SCALE held at 0.40×) recover the
regime breach PR #157 found on the locked bundle? (Brief:
`docs/ltm/briefs/Q-DDTRIG-1-dd-trigger-tail-cost.md`; scoped to "build the bundle
re-MC" by Joshua 2026-06-07.)

**Verdict — RESOLVED → HOLD.** The tighter trigger **passes the brief's §4 full-panel
thresholds marginally** (and the replay even shows 0 busts at 1.0%) — but it **fails
the mandatory regime-robustness gate decisively**: the 2020–2023 half busts **11.76%**
(floor 1.0%) with p99 DD **7.84%** (cap 5.0%) at 1.0%, barely better than 13.34% / 7.98%
at the current 1.5%. The full-panel "improvement" is the benign-regime-weighted average
PR #157 already identified; no trigger value makes 2020–23 regime-robust. The replay's
"0 busts at 1.0%" is exactly the path-tuning signal the brief's §5 forbidden-move #2
rules out. **Current trigger holds.**

This is a research artifact in `lab/`. It does **not** modify `core/`, the canonical
panels, the locked anchor, or any manifest. No re-lock implied.

---

## Phase 0 — Rule-0 production reads (decision-grade)

Real paths are `core/` (the brief's `prop_firm_pipeline/` tree does not exist —
confabulated authoring environment).

* `core/dd_protection.py` (last commit `4331e65`): **`DD_TRIGGER = 0.015` (1.5%) /
  `DD_SCALE = 0.40`** — LIVE. Single tier, `risk *= multiplier` scale (not `min`),
  fires `round(dd_from_peak,6) >= 0.015`, clears on recovery. Import-time spec-pin
  hard-raises if constants ≠ (0.015, 0.40); `portfolio_mc` overrides the *simulation*
  value via `--dd-trigger`/`--dd-scale` without tripping the pin.
  **→ Premise resolved: live trigger is 1.5%, not 1.0%** (the brief's 1.0% citation
  was a stale skill snapshot).
* `core/portfolio_mc.py`: 5%-daily check is `pnl / STARTING_EQUITY` = **static $200K**
  (Finding #1 confirmed; out of scope per §3). Estimator is a **1R-normalized
  week-block bootstrap** — does not de-compound, does not reset-at-$210K. The
  de-compounded banded-reset model the brief describes **is** PR #157's harness
  (`lab/analysis/decompound_remc_2026-06-07/`), reused here.

## Harness fidelity gate (passed before trusting any number)

Reproduced PR #157's committed headline on this disk:
`B_2020 (locked allocs, banded, C2) = 97.08% / 2.92% / 5.93%` — **exact**. Decompound
self-check: counts 309/264/149/280, roundtrip $0.000000.

## Input verification (proposed-bundle CSVs, Rule 0)

| strat | n | range | roundtrip $err | loader_net = cum_net | export-risk (med\|roe\|loser) |
|---|---|---|---|---|---|
| guardian (0.25% + day-DD stop, 23 DD-Limit) | 321 | 2020-01-16→2026-05-25 | 0.000000 | $272,783 ✓ | 0.25% ✓ |
| striker DJ30 (0.50% / pyr 750) | 269 | 2020-01-14→2026-05-29 | 0.000000 | $253,861 ✓ | 0.50% ✓ |
| aegis (1.50%, unchanged) | 149 | 2020-02-24→2026-05-19 | 0.000000 | $195,032 ✓ | full-stop ~1.6% ✓ |
| striker NAS (0.37% / pyr 700 / **Mon-Tue-Fri**) | 420 | 2020-01-06→2026-06-02 | 0.000000 | $416,352 ✓ | 0.37% ✓ |

`loader_net == final cumulative` for all four → pyramid pairing captures full trade
P&L (the `iloc[0]`-exit concern is resolved). All scale factors = **1.000** →
each CSV was exported at the proposed risk, so `fixed_1r = alloc × $200K` is valid.

## Re-MC cells (proposed bundle, decompounded 2020-26; SEEDS=(42,123,2026), 10k×3)

**BANDED (headline — Joshua's skim-to-$200K-at-$210K model):**

| dd cell | pass | bust | bustD | bustS | inact | p99 DD | p50 DD | median | gate |
|---|---|---|---|---|---|---|---|---|---|
| 1.5%/0.40 (current) | 98.92% ±0.09 | **1.08%** ±0.09 | 0.00% | 1.08% | 0.00% | **5.21%** | 1.80% | 32 | **fail** |
| 1.0%/0.40 (tighter) | 99.22% ±0.08 | 0.78% ±0.08 | 0.00% | 0.78% | 0.00% | 5.00% | 1.68% | 37 | pass (knife-edge) |
| OFF (scale 1.0) | 92.79% ±0.09 | 7.21% ±0.09 | 0.00% | 7.21% | 0.00% | 7.39% | 1.79% | 26 | fail |

STATIC reference is identical to 2 dp except tighter p99 = **5.01%** (fails the cap).
All busts are **static; zero daily** — the brake (which reads peak/eq at day-start) can
move static busts, which is why tightening helps at all; it structurally cannot catch a
single −5% day (none occur here).

**Two facts the headline must be read against:**
1. The **current** trigger already **fails both gates on the de-risked bundle**
   (1.08% > 1%, 5.21% > 5%). De-risking + current trigger ≠ regime-safe.
2. The tighter cell's "pass" is **knife-edge and within seed σ of failing**: p99 = 5.00%
   banded / 5.01% static; Δbust = exactly +0.30pp (the §4 floor); σ ≈ ±0.09pp.

## §4 hypothesis check (full-panel, banded) — marginally MET

| criterion | value | threshold | |
|---|---|---|---|
| Δbust (cur − tig) | +0.30 pp | ≥ +0.30 | ok (exact) |
| tighter p99 DD | 5.00% | ≤ 5.00% | ok (exact) |
| tighter pass | 99.22% | ≥ 90% | ok |
| Δtimeout (tig − cur) | +0.00 pp | ≤ +3.00 | ok |

Taken literally, §6 would read **RE-LOCK CANDIDATE**. This is the trap: §4 as written
has no regime partition.

## Portfolio reset-replay (real chronological path, tail cross-check)

| dd cell | cycles | attempts | busts | bust% | bust dates |
|---|---|---|---|---|---|
| 1.5%/0.40 (current) | 31 | 32 | 1 | 3.12% | 2020-05-04 (static) |
| 1.0%/0.40 (tighter) | 28 | 28 | **0** | 0.00% | — |
| OFF | 40 | 43 | 3 | 6.98% | 2020-04-17, 2021-12-08, 2024-05-07 (all static) |

Reproduces the brief's directional cross-check (marginal 2020 bust at 1.5%, removed at
1.0%, OFF much worse). Canonical count is **1** bust at 1.5%, not the brief's 2 — the
brief's second bust (2022-01-12 Aegis) was a per-leg artifact of its non-canonical
rebuild; the portfolio-level canonical replay does not reproduce it. **The "0 busts at
1.0%" is the §5-forbidden path-tuning signal** — see the regime split for why it misleads.

## Regime-robustness gate (decisive) — FAIL at both triggers

Half-panel split at the bday midpoint (regime_gate.py Part B; floor = bust<1% AND
p99<5% in **each** half; static streams to match PR #157):

| trigger | half | range | pass | bust | p99 DD | median | gate |
|---|---|---|---|---|---|---|---|
| 1.5% (current) | H1 | 2020-01→2023-03 | 86.64% | **13.34%** | **7.98%** | 76 | **FAIL** |
| 1.5% (current) | H2 | 2023-03→2026-06 | 99.89% | 0.11% | 4.29% | 20 | PASS |
| 1.0% (tighter) | H1 | 2020-01→2023-03 | 88.21% | **11.76%** | **7.84%** | 92 | **FAIL** |
| 1.0% (tighter) | H2 | 2023-03→2026-06 | 99.91% | 0.09% | 4.02% | 21 | PASS |

The gate (= bootstrap **AND** H1 **AND** H2) fails because H1 fails outright at both
triggers — tightening moves H1 bust only 13.34% → 11.76% (still ~12× the 1% floor) and
H1 p99 7.98% → 7.84% (still ~2.8pp over the cap). The n=100 6-month-block bootstrap
(Part A; `regime_gate_bundle.py`) was **not run** — Part A cannot flip a gate already
FAILed by Part B, so it carries no decision value here.

## Conclusion

* The dd-trigger is the **wrong lever** for the 2020–23 regime tail, on the proposed
  bundle exactly as on the locked one (PR #157). It is a *conditional* brake; in a
  chop regime where static busts cluster, no trigger value brings 2020–23 under the
  lock gates without slowing the challenge to impracticality.
* The proposed de-risk bundle **does not** clear the gates either: current trigger
  fails the full panel; tighter only knife-edge-clears the full panel while the regime
  gate fails at both.
* **HOLD the current 1.5%/0.40× trigger.** The cross-check's 2-bust signal — and this
  run's full-panel §4 "pass" + replay "0 busts" — are regime artifacts, not a trigger
  defect.

**Methodology note (candidate lesson).** The brief's §4 thresholds, applied to the
full panel, would have produced a *false* RE-LOCK CANDIDATE. The regime partition is
not optional for a `dd_protection`-class brief — it must be **inside** the §4 floor
(cf. the Phase-4-floor amendment). This is the third instance of "full-panel masks
regime split" (Q-REGIME-1 / PR #157 / here).

---

## Reproduce

```bash
# Inputs (gitignored, vendor-licensed): drop the 4 proposed-bundle Pepperstone exports
#   into inputs/ (filenames in bundle_remc.py:PROPOSED_FILES), then:
cd lab/analysis/q_ddtrig_1_2026-06-07
PYTHONUTF8=1 python bundle_remc.py            # verification + cells + §4 + replay + half-split
PYTHONUTF8=1 python regime_gate_bundle.py 100 # optional formal n=100 Part-A bootstrap (not decision-bearing)

# Harness fidelity gate (reproduces PR #157 B_2020 = 97.08/2.92/5.93):
cd ../decompound_remc_2026-06-07 && python decompound.py
```
