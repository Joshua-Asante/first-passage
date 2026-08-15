# NOCT-SPX-001 — Stage 1+2 channel-isolating falsifier

Mechanism falsifier for **CONCEPT-NOCT-SPX-001** (Nocturnal inventory-reversal
harvest on SPX500). Tests whether the SPX500 European-open window (02:00–05:30 ET)
return is carried **specifically by days following a US-session sell-off** (dealer
inventory-reversal / Grossman–Miller immediacy premium), or whether it is just an
unconditional time-of-day drift (already dead after costs). **Mechanism probe only
— no strategy is built** (brief §5). Mirrors the `lab/analysis/oil_carry/` F1
precedent: a cheap `lab/analysis/` falsifier that gates whether the concept ever
earns a codify→sweep→validate pass.

Source brief: `CC-HANDOFF-NOCT-SPX-001-stage1-2` (Tech Advisor, 2026-06-06),
executed 2026-06-07.

## Pipeline placement (house R&D loop)

1. **Front gate** — `CONCEPT-NOCT-SPX-001.yaml` registered in
   `lab/validation/concept_intake/concepts/` and passed the admissibility gate
   (`check_concept.py` → **ADMIT 7/7, dedup CLEAR**) before any data was mined
   (ADR 2026-06-05-concept-admissibility).
2. **This probe** — Stage 1+2 falsifier (here).
3. **Loop closure** — if FALSIFIED, the rejection is appended to
   `docs/rejected_candidates.md` via `validation/concept_intake/feedback.py`
   (additions-only; `dedup_check` reads it so the direction can't regenerate).

## Data route (Decision 1 — Dukascopy, the canonical R&D feed)

- Feed: **Dukascopy `USA500IDXUSD` m15** via `core/lib/dukascopy.py` (PR #152),
  the stdlib-only R&D bar adapter (no env mutation). Written to the canonical
  `core/data/bar_data/USA500IDXUSD_M15.csv` schema (gitignored vendor data).
- **`point_factor = 1e3`** — empirically verified (Phase 0): Dukascopy raw /
  OANDA `SPX500_USD` close ≈ 1000, and historical levels track the S&P 500
  (2011≈1216 · 2016≈2020 · COVID≈2452 · 2026≈7550). Indices are not in the
  adapter's factor map, so the factor is passed explicitly.
- **Sample: 2020-01-01 → present** (~6.4yr) per operator scope (Joshua). NB this
  **deviates from the brief's pre-registered "≥8 years" Stage 1 window** — see
  Deviations.
- Cross-feed caveat: Dukascopy ≠ TradingView/Alchemy byte-for-byte. For a
  tercile-conditioned *return* gate this is immaterial; the cost overlay is the
  live-venue (FXIFY/Alchemy) spread, not Dukascopy's.

## The pre-registered gate (brief §2–§4)

All net of cost. Conditioning is the **prior trading day's** US session
(`R_US_prev` = `R_US.shift(1)`) — the EU window on day *t* precedes that day's
09:30 US open, so same-day conditioning would be look-ahead; the mechanism
("days *following* a US sell-off") fixes the one-session lag.

- **(a)** bottom-tercile (largest prior US sell-off) mean `R_EU` > 0, t ≥ 2, n ≥ 200.
- **(b)** separation = bottom-tercile mean − all-days mean, t ≥ 2, with the
  **overlap-correct SE** (all-days contains the bottom tercile). Algebra:
  `mean_B − mean_all = ((n−n_B)/n)(mean_B − mean_complement)`, so the overlap-aware
  t **equals the bottom-vs-complement Welch t**. Cross-checks: bottom-vs-top and
  bottom-vs-complement Welch t reported alongside.
- **(c)** monotonicity: bottom-tercile `R_EU` > top-tercile `R_EU`.
- **Stage 1 PASS** iff (a)∧(b)∧(c). **KILL** if no separation (b fails) even when
  the unconditional average is positive, or if net bottom-tercile ≤ 0.
- **Stage 2** (2021–2026 subsample, re-terciled within): PASS iff conditional net
  Sharpe ≥ 0.5 **and** sign of (a)/(b)/(c) preserved.
- **Overall = Stage 1 PASS ∧ Stage 2 PASS.**

Bar mapping (m15 stamped at bar-open): `R_US = (close[15:45 ET] − open[09:30 ET]) /
open[09:30 ET]`; `R_EU = (close[05:15 ET] − open[02:00 ET]) / open[02:00 ET]`;
`R_US_last90` (open[14:30]→close[15:45]) is a **robustness check only**, never a
pass route (brief §5 #4). DST handled via `tz_convert("America/New_York")`
(reusing the `oanda_stage1` house pattern); spot-checked across DST-mismatch dates.

Cost: round-trip spread on `R_EU` (entry+exit). No recorded FXIFY/Alchemy SPX500
spread, so the gate **sweeps {0,1,2,3,5} bps and reports the breakeven** (Decision
2). Swap = 0: the 02:00–05:30 ET window is intraday, after the 17:00 ET prior
rollover and before the next — no overnight financing event.

## Deviations from the brief (all flagged, none silent)

| # | Brief said | Reality / decision | Why |
|---|---|---|---|
| 1 | Dukascopy "canonical R&D feed" (assumed absent in Phase 0) | **Confirmed real** — `core/lib/dukascopy.py` merged PR #152; my Phase-0 "not in repo" was a stale worktree (based at PR #150). Rebased to `origin/main` `f94977d`. | Decision 1 |
| 2 | Output to `reports/noct-spx-001/` + manual `rejected_candidates.md` edit | **`lab/analysis/noct_spx/`** + concept-intake gate + `feedback.py` auto-append | Decision 3 (house pipeline; oil_carry precedent) |
| 3 | `reports/ecr/` rolling-runner convention | Does not exist (ECR = live-journal Edge-Captured-Ratio); used the `lab/` R&D harness conventions instead | confabulated path |
| 4 | "≥8 years" Stage 1 sample | **2020-01-01 → present (~6.4yr)** per operator scope | Joshua's call; **CONCERN** — Stage 1/Stage 2 windows now overlap heavily, weakening the pre/post-2020 decay isolation |
| 5 | (point_factor not mentioned — assumed `dukascopy-node` auto-scales) | `point_factor=1e3` determined empirically | adapter requires explicit index factor |
| 6 | (adapter assumed robust) | flagged the closed-hour-503 fatal-abort gap → fixed in the adapter itself (PR #153: skip+count, `strict=` opt-in); `fetch_panel.py` uses the native handling | adapter originally made non-404 fatal, aborting multi-year pulls |

## Reproduce

```bash
python lab/analysis/noct_spx/run_gate.py          # fetch (if missing) + gate
# or step-by-step:
python lab/analysis/noct_spx/fetch_panel.py --out core/data/bar_data/USA500IDXUSD_M15.csv --start 2020-01-01 --end 2026-06-07
python lab/analysis/noct_spx/gate.py --bars core/data/bar_data/USA500IDXUSD_M15.csv --out lab/analysis/noct_spx
```

## Files

- `fetch_panel.py` — chunked Dukascopy fetch; relies on the adapter's native closed-hour-503 skip+count (PR #153).
- `gate.py` — the falsifier: session returns, terciles, (a)/(b)/(c), Stage 2 Sharpe, DST spot-check → `gate_result.json`.
- `run_gate.py` — one-command reproducer.
- `gate_result.json` — full numeric result (written by gate.py).
- `verdict.md` — the binary verdict + figures (Stage 1, Stage 2, overall).
