# Reachability attestation — `Q-ICT-1MEXEC-1`

Per HARV ADR 2026-07-13 §2 (mechanism-first HARD gate). Full accounting lives in the frozen
pre-registration; this file is the required non-empty attestation artifact `register_search open`
checks for presence.

- **K_intrinsic = 1** — one frozen construct (raid → same-direction displacement FVG → limit fill →
  PDH/PDL target vs swept-pool stop), no conditioning gate, no exit variant, no grid. See
  [pre-registration](../../../../docs/briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md)
  §2.1.
- **K_banked(MNQ) = 21** (disclosed, does not enter `K_eff` per ADR 2026-08-04, `Accepted`).
- **`K_eff = K_intrinsic = 1` → annSR floor 0.650 → admissible band [0.650, 1.000], 0.350 wide** —
  see the pre-registration's 2026-08-24 SUPERSESSION section for the corrected arithmetic (the
  document's own §2 is stale, retained as record).
- **Profile-consult BLOCKING bar addressed**: `MNQ x ict-liquidity` is `DEAD` (2026-08-04,
  `mnq_fvg_draw_probe_2026-08-04`) with a standing "route-1 presumptively exhausted, needs operator
  review" caution. Addressed in the pre-registration's second 2026-08-24 disclosure: this campaign
  operates on 1-minute-bar objects with a real stop and a same-session-reachable PDH/PDL target,
  not the daily-horizon, stop-free, distant-target construct that DEAD verdict tested. Operator GO
  (2026-08-24, direct instruction after reading a report naming this exact distinction) is read as
  the review that bar calls for.
- **Stage 2 (cost-law) runs first**, per the pre-registration's own §8 sequencing — the cheapest
  kill, where D5 and H-OD-1 both died.

Cost-law reachability (Requirement-5/§2.2 pre-flight, ADR 2026-07-16 §4/§6):
- value: 4.0 | units: ratio (edge/cost) | basis: Tradeify $0.91/side + 1 tick round-trip,
  1.41pt total (matches the already-established MNQPOOL-1 basis) | source: pre-registration §3/§4 F1
