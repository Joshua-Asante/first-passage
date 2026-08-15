# ORB-MNQ-1 decay-monitor calibration RESULTS — lifecycle Call-1 seed

**Campaign:** `orb_mnq_intraday_breakout` · **Harness:** [`run_decay_monitor.py`](run_decay_monitor.py)
**Discharges:** the acceptance-checklist item in
[`core/strategies/orb/orb_mnq_v0_1_CANDIDATE.md`](../../../core/strategies/orb/orb_mnq_v0_1_CANDIDATE.md)
— "Decay monitor calibrated to the live venue (Stage-6d CUSUM seed, block_size=2) —
owed at admission-to-live per lifecycle Call-1" — and the matching ADMISSION.md
"Still gated" item.
**Precedes:** [`RESULTS_stage7.md`](RESULTS_stage7.md) (firm × slip realism).

---

## Verdict — calibration COMPLETE (a SEED, not a fired monitor — no live data exists)

Exactly the same posture as the four locked legs' own Call-1 harness
(`lab/discovery/lifecycle_call1/`, landed 2026-07-14): the numeric floor is
established now, against frozen OOS backtest returns, so it is ready the instant a
live venue produces fills. It has not fired, because nothing has traded live yet —
the self-check below proves the wiring, not a live breach.

| Window | n trades | ACF block_size | baseline_pf | pf_sigma | floor (baseline − 1.0σ) |
|---|---:|---:|---:|---:|---:|
| **2021+ (CALIBRATION BASELINE)** | 1,420 | 2 | **1.1691** | 0.0836 | **1.0855** |
| FULL 2019-05→present (transparency only) | 1,846 | 2 | 1.1090 | 0.0693 | 1.0397 |

**Venue + window:** Tradeify economics ($0.91/side + 1 tick, `core/firm_rules.py`
live import), 2021+ window. Not an arbitrary pick — Stage-7 (`RESULTS_stage7.md`
Table 1) showed the FULL window passes the Sharpe-limb gate only at Bulenox/≤1-tick
fills, while 2021+ passes at **all four** FRIENDLY firms up to 3-tick slip and is
explicitly named there "the operationally relevant read... the regime the
mechanism actually lives in." The full-window row above is reported for
transparency only (matching the Stage-6/7 "report both, flag which is decisive"
convention) — it is not the calibration baseline, and Stage-7 already showed it is
the more cost-fragile of the two.

**$-space, not R-space:** `$PnL_per_trade = R_net × OR_range_pt × $2/pt` (MNQ
multiplier), derived from `orb_lib.py`'s own formula `R = (pnl_pt − rt_cost_pt) /
range` (verified against source, not assumed) — so `R × range = pnl_pt − rt_cost_pt`
recovers net P&L in points, and ×$2/pt converts to dollars at 1-contract sizing
(matching the frozen Pine construct's "sizing = fixed 1 contract" convention).
`n_trades=1846` on the FULL window reproduces Stage-6's own reported `n=1846`
exactly — an internal-consistency check that this reuses the same underlying
series, not a re-derivation.

**Method — no reinvention.** Every primitive is reused verbatim from code that
already exists and is already tested:
- `orb_lib.orb_backtest` + `run_stage7._gross` — the frozen construct, Tradeify
  commission read live from `core/firm_rules.py` (not transcribed).
- `research_utils.universe_gate.acf_block_size` — the same ACF rule Stage-5/6 used
  (which is why it reproduces `block_size=2` independently here, on a $-scaled
  series, rather than being hardcoded from Stage-6's report).
- `discovery.lifecycle_call1.pf_sigma.{pf_from_daily_pnl, pf_sigma_from_panel}` —
  the same block-bootstrap σ machinery the four locked legs' Call-1 harness uses.
- `discovery.lifecycle_call1.evaluate.evaluate_window` — the same
  BREACH/CLEAR/AMBIGUOUS wrapper around `core.lifecycle.decay_breach` (never
  reimplemented; `k_sigma=1.0`, `MIN_TRADE_COUNT=30` imported, not restated).
- `n_draws=2000`, `seed=20260716` — the same pre-reg GO-date seed
  `run_stage6.py` already uses for this campaign's own bootstrap (`run_temporal_battery(...,
  seed=20260716)`), kept for one traceable seed convention across the campaign.

---

## The load-bearing caveats

### 1. This does NOT plug into the four-locked-leg Call-1 apparatus, by design

`lab/discovery/lifecycle_call1/harness.py` and `baselines.py` are hard-gated to
`core.lifecycle.STRATEGY_KEYS = frozenset({"Guardian", "Striker", "Aegis", "Striker
NAS100"})` — `baselines.py` raises `ValueError` on any other keyset, and
`harness.py` raises on any strategy not in that frozenset. ORB-MNQ-1 is explicitly
**not** one of the four locked legs and is **not** wired into
`lifecycle_state.json` (ADMISSION.md, verbatim: "that file is gitignored/local-only
and scoped to the four locked legs' demotion tracking"). This calibration therefore
reuses only the generic, non-gated primitives (`pf_sigma.py`, `evaluate.py`,
`acf_block_size`) directly — it does not call, extend, or route through
`run_call1_harness`, and it writes no lifecycle state.

### 2. Durability-source tag: SURVIVAL-ONLY (a determination, not a default I ducked)

`strategy_lifecycle.md` Call 3 splits surveillance tightness by durability tag —
`MECHANISM` (starts `AUTHORIZED`, 2-consecutive-window Call-1 trigger, quarterly
review) vs `SURVIVAL-ONLY` (starts `WATCH-1`, **1**-window trigger, quarterly + one
interim review). Call 3's own text: new discovery-stack additions and
residual-program lanes "enter `SURVIVAL-ONLY` by default." ADMISSION.md caveat 2 is
explicit that ORB-MNQ-1 is "a confirmation of a **pre-selected** construct... not a
blind OOS discovery" — mined CFD-side over an extensive search, then confirmed
native, not derived from an ex-ante economic model. On that basis this calibration
tags it **`SURVIVAL-ONLY`** and uses the tighter **1-consecutive-window** Call-1
trigger (not 2).

**This affects surveillance tightness only — it does NOT revisit the starting
multiplier.** Call 3's `SURVIVAL-ONLY` starting tier (`WATCH-1`, 0.50×) is a
*default* for cases with no specific admission decision; ORB-MNQ-1 has one — the
operator's explicit, dated 2026-07-16 "admit it" at `CANDIDATE @ 1.00×`
(`ADMISSION.md`). That decision is not re-litigated here. If this durability-tag
determination is wrong, it is cheap to correct (flip `DURABILITY_TAG` in
`run_decay_monitor.py` and re-run) and does not touch anything already decided.

### 3. Call-1 action-on-breach at CANDIDATE — Proposed ADR (awaiting Accept)

`core/lifecycle.py`'s coded ladder starts at `AUTHORIZED`; ORB-MNQ-1 sits at
`CANDIDATE`. Governance for Call-1 breach at that standing is owned by
[`ADR 2026-08-06-candidate-call1-action-on-breach`](../../../docs/adr/2026-08-06-candidate-call1-action-on-breach.md)
(**Status: `Proposed`** — awaiting operator Accept): **operator review flag only;
no autonomous demotion; `RETIRED` remains Call-5 GO**. Until Accept, treat that
rule as the standing interim posture (same sentence the calibration recorded
before the ADR existed). This calibration still owns only the numeric floor —
it does not invent ladder rungs or Cap fire thresholds.

### 4. Provisional, not ratified

`MIN_TRADE_COUNT=30` and the whole Call-1 floor mechanism are flagged in
`evaluate.py` and `strategy_lifecycle.md` itself as "**pre-registration against
future data**, not live-evaluable... the ADR §6 AMBIGUOUS clause governs" until a
live venue exists. This calibration inherits that posture unchanged — it does not
attempt to ratify a different threshold for ORB-MNQ-1 specifically.

---

## Companion observable (registered, not wired)

**2026-08-06:** Cap-spend forward L1 `A` on `[t, t+60s)` at ORB triggers is a
**registered companion** beside this PF-CUSUM seed — pre-P&L structural watch,
docs-only. Canonical: [`ADR 2026-08-06`](../../../docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md)
(`Accepted` 2026-08-06). Cap evidence:
[`RESULTS`](../../c1/mnq_capa_n14_tripwire_2026-08-06/RESULTS.md) ·
[`closure`](../../../docs/briefs/closures/Q-CAPA-1-closure-resolved.md).
This seed is unchanged. Registration does **not** arm the companion, invent fire
thresholds, or wire Call-1 / entry filters.

---

## Backtest-replay consumer (wired, not live-fired)

**2026-08-06:** A campaign-local research harness evaluates non-overlapping calendar
quarters of the same ORB + Tradeify series against **this** frozen floor and emits
`OPERATOR_REVIEW_FLAG` only under the SURVIVAL-ONLY consecutive=1 rule — not
lifecycle demotion, not Cap fire, not unpark. Canonical:
[`RESULTS_decay_monitor_replay.md`](RESULTS_decay_monitor_replay.md) ·
[`run_decay_monitor_replay.py`](run_decay_monitor_replay.py). This calibration
artifact remains the floor owner; the replay is a consumer.

---

## Disposition

- **Acceptance-checklist item discharged:** the decay monitor is calibrated
  (baseline_pf, pf_sigma, floor established at the venue-appropriate window/economics).
  **Rail integration remains separately gated** — not touched, not authorized by
  this work (`ADMISSION.md`: "Rail build, account registration, and live spend
  remain separately gated").
- **No `core/`, `lifecycle_state.json`, allocation, `dd_protection`, `ACTIVE_FIRM`,
  or Pine touch.** Lock HELD. `discovery_manifests/orb_mnq_intraday_breakout.json`
  left **open**, untouched — closing it would bank a second K unit against the MNQ
  family (`K_banked` only grows; see `discovery_manifests/` / the K-bank
  ledger) and is a separate, consequential decision this work does not make.
- **Output artifact:** [`decay_monitor_calibration.json`](decay_monitor_calibration.json)
  (machine-readable; same fields as this table, plus provenance).

Reproduce:

```bash
PYTHONPATH=lab .venv-research/Scripts/python.exe lab/analysis/orb_mnq_2026-07/run_decay_monitor.py
```
