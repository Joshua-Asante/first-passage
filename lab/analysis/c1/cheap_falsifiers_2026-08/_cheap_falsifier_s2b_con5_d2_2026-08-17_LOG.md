# Cheap falsifier — MSL-S2B successor, CON-5 D2 route-reliance gate — `D2_FAIL`

**Date:** 2026-08-17
**ADR (spec frozen there):** [`docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md`](../../../docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) §2 D2
**Card:** [MSL-S2B](../msl_s2b_mym_2026-08/STAGE1.md) successor — `sweep-failure-filtered-continuation` × MYM 15m
**Cost / K:** $0.00 · K=0 — pre-G0 door-check, no `register_search open`, no Q-ID
**CONFIRM:** never touched — IS partition only (panel start .. 2025-08-31)
**Runner:** [`_cheap_falsifier_s2b_con5_d2_2026-08-17.py`](_cheap_falsifier_s2b_con5_d2_2026-08-17.py)
**Raw:** [`_cheap_falsifier_s2b_con5_d2_2026-08-17_RESULTS.json`](_cheap_falsifier_s2b_con5_d2_2026-08-17_RESULTS.json)
**Panel:** `core/data/bar_data/MYM_M15.csv`, sha256 `24e16952…97a58` (verified against `SHA256SUMS`, matches [STAGE0](../msl_s2b_mym_2026-08/STAGE0.md)'s pin)

## Why this needed an operator decision first (not silently authored)

Every S2B document (STAGE0, STAGE1, `card.yaml`, `MECHANISMS.md`, the second-slate
brief) describes the "continuation entry" only as the qualitative story *"trend-
continuation entry... gated by a PDH/PDL sweep-failure state."* No document ever
operationalizes a trigger — the card died at Stage-1 kill-limb-1 (route
declaration) before reaching that point, and `card.yaml`'s own numeric geometry is
flagged "NOT freeze-time claims... not an assumed-edge region freeze." Running the
D2 falsifier therefore required either inventing a trigger or reusing an
already-coded one. **Operator elected (2026-08-17):** reuse sibling construct
MSL-C1's own PDH/PDL sweep + failed-extension-reclaim signal
([`construct_lib.py`](../../msl_c1_mym_2026-08/construct_lib.py)), taken on the
**flip** (join the original sweep direction) side — the only pre-existing,
non-invented candidate matching "sweep-failure gates continuation." Imported
verbatim (`find_failed_extension_signal`, `rth_hl`), not re-derived.

## Frozen geometry used (a priori, not re-tuned)

| Knob | Value | Source |
|---|---|---|
| Signal | first RTH sweep of prior-day PDH/PDL that closes back inside (failed extension) | C1 `construct_lib.find_failed_extension_signal`, unmodified |
| Side | **flip** = join the original sweep direction (opposite of C1's own fade side) | C1 `construct_lib`, `mode="flip"` semantics |
| Entry | next bar open after the reclaim bar | C1 `construct_lib`, unmodified |
| Stop | **40 pts**, hard | S2B `card.yaml` (placeholder geometry — reused as-is per the ADR's "not re-tuned" instruction) |
| Target | **120 pts** (rr=3, upper end of the elected [2,3] slate-2 box) | S2B `card.yaml` |
| Cadence | k=1, first valid signal per session | S2B mechanism draft |
| RT cost | $2.82/contract → 5.64 pts (point value $0.5/pt) | S2B `STAGE1.md` Cost basis |
| Pass bar | 0.5 × (4 × 5.64) = **11.28 pts** mean signed gross per signal | ADR §2 D2 |

**Implementation note (bug caught + fixed before scoring):** C1's own
`path_pts_stop_target_flat` hardcodes the target-hit payout as `+stop_dist`,
correct only for C1's symmetric 1R:1R box. Reusing it unmodified against S2B's
asymmetric 40/120 box silently paid every target hit as +40 instead of +120,
producing a materially wrong first result (mean −19.07 pts). Replaced with a
locally-corrected path function (same stop-first-same-bar / target / flat
priority order, correct asymmetric payout) before reporting below.

## Result

| Check | Value |
|---|---|
| eligible sessions (valid prior PDH/PDL) | 1,605 |
| n trades (signal fired) | 850 (coverage **52.96%**) |
| exit kind | stop 627 · target 192 · flat 31 |
| mean signed gross | **−1.00 pt** |
| WR | **25.41%** (≈ the rr=3 breakeven WR of 25%) |
| gross / (4×RT) | **−0.044×** |
| pass bar | +11.28 pts (0.5 × 4×RT) |

**Verdict:** `D2_FAIL` — mean signed gross is negative (−1.00 pt), nowhere near
the +11.28 pt generous half-bar. Not a marginal miss: WR sits almost exactly at
the box's own breakeven point before any cost is deducted, so the construct has
no edge to begin with under this entry+box combination, let alone one that
clears a round-trip tax.

## Disposition

Per ADR D2: **route B (temporal-selectivity-as-continuation via CON-5's textual
opening) closes for `sweep-failure-filtered-continuation` × MYM 15m at $0, no
Board debate needed** — exactly how CON-1..5 themselves were closed. This does
**not** reopen or alter MSL-S2B's own frozen 2026-08-14 `STAGE-1 FAIL` (route)
verdict (D3 is prospective only) — see the forward-pointer addendum on
[STAGE1.md](../msl_s2b_mym_2026-08/STAGE1.md). CONFIRM remains unread. No Cap
claim, no Pine, no arming.

**Caveat carried forward, not hidden:** this result tests one specific entry
definition (C1's flip signal) against one specific box (S2B's own placeholder
40/120). It does not test every possible operationalization of "trend-
continuation gated by sweep-failure" — a different entry trigger remains
untested and would need its own falsifier, not a reopening of this one.
