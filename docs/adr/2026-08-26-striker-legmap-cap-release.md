# ADR 2026-08-26 — Release Striker's 69/11 LEG_MAP cap allocation

**Status:** `Accepted` — operator ruling 2026-08-26 (chat directive, verbatim: *"I want to zero out
Striker's 69+11 share and free that headroom for a new leg"*)
**Decision date:** 2026-08-26
**Supersedes:** [`2026-08-08-edge-cohort-correction-and-necessity-retarget.md`](2026-08-08-edge-cohort-correction-and-necessity-retarget.md)
in part — its §L4 row's "Named ruling owed before any deployment: `LEG_MAP`'s 69/11 allocation is
retained-not-released under S1" clause only; the rest of L4 (book-shape admission) stands.
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Tier:** light
**Authors:** Joshua (ruling) + Claude Code (recorder)
**Related:** [edge-cohort ADR](2026-08-08-edge-cohort-correction-and-necessity-retarget.md) §L4 ·
[third-leg symbol-occupancy limb](2026-07-29-third-leg-symbol-occupancy-limb.md) (occupancy
dimension, untouched by this ADR — already separately released by the MSL B8 ADR below) ·
[MSL B8 occupancy release](2026-08-12-msl-mym-occupancy-release.md) (sibling ruling, occupancy
dimension only — this ADR is the cap-dollar dimension the edge-cohort ADR left open) ·
`ops/c1_rail/c1_sizing_host_reference.py` `LEG_MAP` · `ops/instruments/{MYM,MNQ}.md`
**Layer:** live-sizing constant (`ops/c1_rail/c1_sizing_host_reference.py`) + doctrine/ledger
posture. **$0 / K=0.** No arming, no Pine, no `dd_protection` change, no strategy deployed.

## Decision

Release both Striker legs' `cap_alloc` share of Tradeify's account-aggregate micro-contract cap.
`LEG_MAP["dj30_mym"]["cap_alloc"]` and `LEG_MAP["nas100_mnq"]["cap_alloc"]` are set to **0** (were
69 / 11). The full 80-micro account cap is now unclaimed — available for a future leg's own
`cap_alloc` to be chosen against, not pre-committed to Striker.

This is the **cap-dollar** dimension only, distinct from and narrower than the **research-occupancy**
dimension the 2026-08-12 MSL B8 ADR already released (whether new non-Striker research/G0 may use
the `MYM1!`/`MNQ1!` symbols at all). That ADR's own scope note is explicit that it does not touch
`LEG_MAP` code; this ADR is the code-level companion the edge-cohort ADR's L4 row named as owed.

## Grounds

Both Striker legs have sent zero signals since withdrawal (2026-08-04); the rail is disarmed
(`dry_run=true`); no strategy is deployed. `LEG_MAP`'s cap_alloc values were never a live-risk
control on their own — the sizing host's fail-safe doctrine (halt-to-zero on any missing/malformed
input, never a permissive default) meant Striker's continued 69/11 allocation was pure unused
bookkeeping, not a position that needed protecting. Continuing to reserve it blocked a future third
leg's own admission math from seeing accurate headroom without a hand-derivation each time (the
third-leg target spec's own S5 check — "fits the day-of-week cap table... without re-allocating cap
from MYM or MNQ" — silently assumed Striker's share was untouchable).

## Reads (verified this session, 2026-08-26)

- `ops/c1_rail/c1_sizing_host_reference.py` — `LEG_MAP` definition + the `cap_alloc` doc comment
  (2026-07-22 account-aggregate split rationale); `reserve_cap = floor(cap_alloc / (1 + pyr_pct /
  100))`, `qty_out = min(qty_base_raw, reserve_cap)` — confirmed a zeroed leg floors to `qty_out=0`
  via the existing fail-safe path, never a halt, never a fallback to `cap_firm` (which would
  resurrect the pre-2026-07-22 1.91× over-cap bug this split was built to prevent).
- `tests/ops/test_c1_sizing_host_reference.py` — `test_cap_alloc_sums_to_account_cap` (`==` →
  `<=`, "no over/under-commit" was a deliberate design choice at write-time, not accidental; only
  the over-commit half was ever actually dangerous — see `test_combined_max_position_within_account_cap`,
  unaffected). `test_worked_check_components_mym_recent` and the whole non-halt-path suite pin
  against a new `HISTORICAL_LEG_MAP` module constant (cap_alloc 69/11), decoupled from the live
  `LEG_MAP` — the frozen spec worked-example and `f2_floors.json` oracle both cite 69/11 verbatim
  and are **not** edited by this ADR (Trap #12: they remain an accurate historical record of the
  sizing math at that cap_alloc value, permanently, independent of what's live today).
- `docs/spec/c1_nt8_sizing_host_impl.md` §7 Phase 1 — the frozen worked-example text itself;
  confirmed untouched, correctly still describing 2026-07-22→2026-08-26 behavior.
- `docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` §L4 — the exact clause
  this ADR discharges, confirmed it already carries two prior `Superseded-in-part-by` lines
  (2026-08-12 MSL-ratification targeting L2, 2026-08-24 sourcing-phase-channel-retirement
  targeting L1); this ADR **appends** a third, targeting L4 only — never overwrites the other two.

## Gate

RESOLVED when this ADR is Accepted and `LEG_MAP`'s `cap_alloc` values read 0/0 in the committed
tree. No further discharge condition — this is a doctrine/bookkeeping release, not a build gate.

## Boundary

Do **not** read this as authorizing Striker-leg redeploy (de-scope clauses 1–2 stand; both legs stay
barred). Do not read this as choosing or sizing any specific new leg — this ADR frees the headroom,
it does not spend it; a future leg's own `cap_alloc` is a separate admission decision under the
third-leg target spec's own S5/S7 screens. Do not treat this as touching the **occupancy** dimension
(symbol/research permission) — that was already ruled by the 2026-08-12 MSL B8 ADR; this ADR is
cap-dollars only. Do not edit the frozen spec worked-example or `f2_floors.json` oracle under cover
of this record — both remain accurate historical illustrations of the pre-release math.
