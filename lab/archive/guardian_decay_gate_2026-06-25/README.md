# Guardian v5.5 live-decay retirement gate — build

**Verdict: CLOSED — DP-1…DP-7 resolved and the gate built, then dormant: no live Guardian venue, and the terminal DECAYED verdict stays DP-4 classifier-interlocked off. Archived 2026-07-22 as an anchor consumer (substrate-retirement disposition C). Restore with `archive_lab_analysis.py --unarchive` if a live Guardian venue ever exists.**

Resolves DP-1…DP-7 of [`Q-GUARDIAN-DECAY-1`](lab/archive/../../docs/ltm/briefs/Q-GUARDIAN-DECAY-1.md).
Values + rationale: [`Q-GUARDIAN-DECAY-1-DP-RESOLUTION`](lab/archive/../../docs/ltm/briefs/Q-GUARDIAN-DECAY-1-DP-RESOLUTION.md).

**Research-layer only. No `core/` file is modified; no locked parameter is touched.**
The gate emits a verdict — it never toggles execution, alerts, or copy-trading.

## Files
- `build_envelope.py` — DP-7 Guardian-only MC envelope + DP-2/DP-3 CUSUM calibration. Imports `core/portfolio_mc` and drives it with a single-strategy dict, so it is byte-faithful to the canonical 4-strategy machinery (same scaling / week-blocks / dd_protection C2 / seeds). Writes `envelope.json`.
- `decay_gate.py` — the gate: lower-CUSUM (DP-1) on the regime-conditional R stream, ARMED/WATCH/DECAYED state machine (DP-5/DP-6) mapped to the programme-audit disposition vocabulary, with the DP-4 hard interlock (DECAYED unreachable until a regime classifier is validated).

## Vendor data
The locked Guardian Pepperstone CSV is gitignored. On a public clone / remote container both scripts SKIP cleanly (`NEEDS_DATA`, exit 0). Run locally where `core/data/tv_exports/pepperstone/` is populated.

## Run
```bash
# 1. build the envelope (needs the locked panel locally; ~1 min for the solo MC)
python lab/analysis/guardian_decay_gate_2026-06-25/build_envelope.py

# 2. prove the gate mechanics (no data needed)
python lab/analysis/guardian_decay_gate_2026-06-25/decay_gate.py --self-test

# 3. evaluate a live stream (per-trade R-multiples; DXTrade fills → R)
python lab/analysis/guardian_decay_gate_2026-06-25/decay_gate.py \
    --live fills.csv --regime-labels regime.csv [--classifier-validated]
```

### Live CSV format
One row per closed trade. Provide either an `r_multiple` column, or `pnl` + `risk_dollars` (R = pnl/risk_dollars). Optional `exit_date`/`date` for logging + regime join.

### Regime CSV format (DP-4)
`date,favorable` where favorable ∈ {1/0,true/false}. Omit the file to run UNCONDITIONED — in which case DECAYED stays interlocked off (max state WATCH). `--classifier-validated` is set ONLY when the regime classifier has passed its own regime-robustness gate.

## Status
`DONE_WITH_CONCERNS` — the gate is mechanically correct and the §5 false-positive guard is provable, but: (1) live N≈2 → forward-armed, dormant ~14 months (DP-5 M=60 in-regime trades); (2) no validated regime classifier yet → DECAYED interlocked off until one exists (DP-4); (3) the real detection power populates only on Joshua's local `build_envelope.py` run — if low, DP-1/DP-5 need revisiting.

### 2026-07-01 dormancy update (retirement back-propagation — operational-rules Rule 11)
The ~14-month dormancy estimate in (1) assumed live Guardian fills continuing to accrue on the CFD venue. **That assumption no longer holds:** 5 days after this build, Guardian lost *all* live venues — CFD retired 2026-06-30 (`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`), and Guardian is **BLOCKED** on the futures-prop venue (46.4% of trades hold >1 day; force-flat-incompatible per `lab/analysis/futures_prop_hold_compat_2026-06-30/RESULTS.md`). Guardian's only remaining home is a self-funded MGC account that does not yet exist. **Dormancy is therefore indefinite, not ~14 months** — the gate accrues zero in-regime trades until Guardian is live somewhere again. Re-arm condition: a live Guardian execution venue exists and fills accrue. No change to the gate mechanics or thresholds (research-layer, delegation-defaults still unratified per `Q-GUARDIAN-DECAY-1-DP-RESOLUTION`).
