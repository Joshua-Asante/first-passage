# Call-1 OC — synthetic RESULTS (T4 Task 2)

**Date:** 2026-08-23
**Owner:** [`2026-07-11-tradable-anomalies-statistics-adoption.md`](../../adr/2026-07-11-tradable-anomalies-statistics-adoption.md) §7 T4
**Harness:** [`lab/discovery/lifecycle_call1/oc.py`](../../../lab/discovery/lifecycle_call1/oc.py)
**Authorization:** GO 2026-08-23 for historical/synthetic OC only. **No** `lifecycle_state.json` write. Does not claim the 2026-08-08 first evaluation happened.

## Pre-registered box

| Knob | Value |
|---|---|
| k | 1.0 (ratified Call-1) |
| persist | 2 consecutive windows |
| metric | `decay_breach(rolling_pf, baseline_pf, pf_sigma)` |
| false-kill target (flat paths) | 0 at k=1.0 when PF sits on baseline |

## Synthetic outcome (this commit)

- Flat PF = baseline: `false_kill_rate = 0` (`tests/test_call1_oc.py`).
- Known-decay path (PF drops below `baseline − 1σ` and stays): detection lag = 5 windows at persist=2 on the planted series.
- `wrote_lifecycle_state = false` on every path.

Live-PF σ-source remains fill-gated. Task 3 writer is not authorized.
