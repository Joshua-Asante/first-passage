# SPEC S4: sensor layer

Status: CODE_LANDED (EQ schema) · 2026-08-07 · Gate RESOLVED still owes item-5 dry_run
signal from ruled host + `operator_signoff` · authorizes nothing ($0 · K=0) · depends: S1
Objective: Take M1 to `RESOLVED` — it is the arm-gate and the loop's only honest feedback
channel; no automated loop exists without it.

Steps:
1. Enumerate open items in `M1_MONITORING_ACCEPTANCE.json`; close them — ✔ item-5
   **origin** re-ruled by [S2 ADR](../adr/2026-08-07-loop-s2-signal-host-fork.md)
   (Python-native); discharge evidence (dry_run non-zero-size signal event) still owed.
2. Fold in [Q-MONSURF-1](../briefs/Q-MONSURF-1-monitoring-surface-triage-scoping.md)
   — ✔ F2 ruled rail-retained ([S1 ADR](../adr/2026-08-07-loop-s1-environment-ratification.md));
   M-B Phase-3 independence stands; live-pointing still gated on M1 RESOLVED.
3. Extend the EventLedger schema with per-fill execution-quality fields **before** the
   first fill — ✔ `BrokerEvidence` additive fields in `ops/c1_rail/c1_rail_telemetry.py`
   (intended_price · fill_slippage_pts · fill_latency_ms · commission_usd · signal_origin ·
   exit_*).

Gate: RESOLVED when the acceptance JSON's `status` field reads `RESOLVED` (all
`RESOLVED_REQUIRED` fields evidenced + `operator_signoff`) and
`scripts/validate_c1_monitoring_acceptance.py` passes; FALSIFIED if any M1 ADR §4
falsifier fires — revert per the ADR and stay disarmed.
**2026-08-07 progress:** steps 2–3 landed; step 1 origin ruled; evidence + signoff still operator.
Boundary: `dry_run=false` stays forbidden until then (M1 ADR Addendum 2026-07-31b);
disarm always precedes `armed_until` expiry (07-31 self-brick is the anchor).
Reads (at HEAD `a6a5fe6` 2026-08-07): `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` ·
[M1 ADR](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md) · Q-MONSURF-1
Owner: M1 ADR + Q-MONSURF-1.
