# ORB-MNQ-1 decay-monitor REPLAY RESULTS — PF-CUSUM backtest dry-fire

**Campaign:** `orb_mnq_intraday_breakout` · **Harness:** [`run_decay_monitor_replay.py`](run_decay_monitor_replay.py)
**Consumes:** frozen floor in [`decay_monitor_calibration.json`](decay_monitor_calibration.json)
(owner: [`RESULTS_decay_monitor.md`](RESULTS_decay_monitor.md)) — replay does **not** re-bootstrap σ.
**Machine output:** [`decay_monitor_replay.json`](decay_monitor_replay.json)

---

## Verdict — research harness WIRED (backtest dry-fire; not live decay evidence)

Non-overlapping **calendar quarters** on the 2021+ Tradeify-economics ORB series are
evaluated against the frozen Call-1 floor. Under the `SURVIVAL-ONLY` consecutive=1
rule, each BREACH window emits an **`OPERATOR_REVIEW_FLAG` only** — no
`lifecycle_state.json` write, no Cap arming, no entry filter, no authorization demotion.

**Integrity:** whole-window 2021+ PF recomputed from the same $-series matches the
calibration baseline exactly (`n=1420`, `delta_pf=0.0`). Floor / σ remain owned by
the calibration artifact; this run is a consumer.

**Standing caveat:** backtest dry-fire ≠ live decay evidence. ORB-MNQ-1 remains
**re-PARKED** (payability target FALSIFIED — see ADR 2026-08-03). A replay BREACH
is not an unpark signal.

| Field | Value |
|---|---|
| Windows | calendar quarters (Call-3 SURVIVAL-ONLY cadence) |
| Trigger | `call1_consecutive_windows=1` → flag on first BREACH |
| Quarters evaluated | 23 (2021Q1–2026Q3 trailing partial) |
| BREACH quarters | 9 |
| OPERATOR_REVIEW_FLAG events | 9 |
| Trailing partial | 2026Q3 `n=11` → AMBIGUOUS (`< MIN_TRADE_COUNT`); streak inert |

---

## Per-quarter outcomes

Floor pinned from calibration `windows["2021+"]` (link out — not restated as authority).

| Quarter | n | rolling_pf | outcome | consec after | flag |
|---|---:|---:|---|---:|---|
| 2021Q1 | 63 | 0.9012 | BREACH | 1 | YES |
| 2021Q2 | 63 | 1.7375 | CLEAR | 0 | |
| 2021Q3 | 66 | 1.1623 | CLEAR | 0 | |
| 2021Q4 | 65 | 1.0454 | BREACH | 1 | YES |
| 2022Q1 | 64 | 0.9398 | BREACH | 2 | YES |
| 2022Q2 | 64 | 1.6117 | CLEAR | 0 | |
| 2022Q3 | 66 | 0.9724 | BREACH | 1 | YES |
| 2022Q4 | 63 | 1.7104 | CLEAR | 0 | |
| 2023Q1 | 64 | 0.8556 | BREACH | 1 | YES |
| 2023Q2 | 63 | 1.4422 | CLEAR | 0 | |
| 2023Q3 | 64 | 1.0734 | BREACH | 1 | YES |
| 2023Q4 | 64 | 1.8928 | CLEAR | 0 | |
| 2024Q1 | 63 | 0.7579 | BREACH | 1 | YES |
| 2024Q2 | 65 | 1.6019 | CLEAR | 0 | |
| 2024Q3 | 66 | 1.5288 | CLEAR | 0 | |
| 2024Q4 | 65 | 1.3248 | CLEAR | 0 | |
| 2025Q1 | 62 | 1.3811 | CLEAR | 0 | |
| 2025Q2 | 63 | 1.1519 | CLEAR | 0 | |
| 2025Q3 | 66 | 0.9881 | BREACH | 1 | YES |
| 2025Q4 | 65 | 1.1590 | CLEAR | 0 | |
| 2026Q1 | 63 | 1.3770 | CLEAR | 0 | |
| 2026Q2 | 62 | 0.8661 | BREACH | 1 | YES |
| 2026Q3 | 11 | 0.0509 | AMBIGUOUS | 1 | |

Flagged quarters: **2021Q1, 2021Q4, 2022Q1, 2022Q3, 2023Q1, 2023Q3, 2024Q1, 2025Q3, 2026Q2**.

---

## Stop rules

- Replay BREACH ≠ authorization demotion and ≠ unpark signal
- Does not ratify Cap fire thresholds
- Does not bank K / close discovery manifest
- Floor / σ remain owned by calibration artifact; replay is a consumer

---

## Method (no reinvention)

- `orb_lib.orb_backtest` at `rt=0` with additive per-trade `"day"` (same length as `R`)
- Tradeify economics: `$PnL = (gR - rt/range) × range × $2/pt` (same formula as
  [`run_decay_monitor.py`](run_decay_monitor.py))
- Floor / σ / `k_sigma` / consecutive trigger loaded from calibration JSON
- `evaluate_window` + `breach_tracker.update_consecutive` (AMBIGUOUS inert)
- Campaign-local runner — does **not** call the four-leg Call-1 harness

---

## Disposition

- Seed calibration still owns the numeric floor ([`RESULTS_decay_monitor.md`](RESULTS_decay_monitor.md)).
- Replay is a wired research consumer; still not live-fired / not demotion-wired.
- Call-1 action-on-breach at `CANDIDATE` owned by
  [`ADR 2026-08-06-candidate-call1-action-on-breach`](../../../docs/adr/2026-08-06-candidate-call1-action-on-breach.md)
  (`Accepted` 2026-08-21): this harness's `OPERATOR_REVIEW_FLAG`-only posture matches that
  rule; supersession is operator — do not rewrite this runner into demotion.

Reproduce:

```bash
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb/orb_mnq_2026-07/run_decay_monitor_replay.py
```
