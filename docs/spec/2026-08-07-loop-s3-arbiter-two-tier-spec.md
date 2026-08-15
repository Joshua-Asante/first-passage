# SPEC S3: arbiter, two-tier

Status: PROPOSED · **CODE_LANDED scaffold 2026-08-07** · authorizes nothing ($0 · K=0) ·
depends: S2, S4 (Step 4)
Objective: Give a Python engine research authority per strategy family (one manual TV
anchor validates it; the paste gate shrinks from O(candidates) to O(families)), and make
micro-size eval fills the deployment truth — no backtester models the venue.

**Scaffold note (2026-08-07):** Gen-2 gate landed at
[`lab/analysis/c1/parity_gen2_2026-08/`](../../lab/analysis/c1/parity_gen2_2026-08/)
(`PREREG.md` bands `FROZEN-PRE-RUN`, `parity_gate.py`, synthetic `test_parity_gate.py`).
**Gate RESOLVED still needs the first family TV anchor (operator).** No post-hoc band
tuning; no fabricated family parity numbers; nothing armed.

Steps:
1. Execute [Q-FILLTAX-1](../briefs/Q-FILLTAX-1-fill-realism-and-parity-scoping.md)
   (OPEN; V2 Phase-0 scaffold CODE_LANDED 2026-08-07) as the evidence base — its V2 parity
   limb executes now at $0 under the S1 incumbent env; its V1 fill-realism-tax limb
   disposition follows S1 (Tradeify geometry).
2. Rebuild the parity gate Gen-2 on same-feed TV CME exports (the Gen-1 `lab/validation`
   harness is retired); freeze bands **before** any run — per the Gen-1 precedent
   [owner](../methodology/prefilter_rank_correlation_gate.md), refrozen not inherited.
   → scaffold: [`parity_gen2_2026-08/PREREG.md`](../../lab/analysis/c1/parity_gen2_2026-08/PREREG.md).
3. Per family: one manual TV anchor run → pass grants the engine research authority inside
   that family's envelope; fail keeps the family native-only.
4. Deployment truth = micro-size eval fills (B7 **Stage-2** generalized — Stage 1 is
   unarmed and routes no order), captured via `c1_rail_telemetry.py` into S4's ledger,
   analyzed by `c1_rail_slippage.py` (read-only). Path documented in
   [`parity_gen2_2026-08/README.md`](../../lab/analysis/c1/parity_gen2_2026-08/README.md).

Gate: RESOLVED if the first family passes anchor parity; FALSIFIED if two families fail
after engine-semantics fixes — the arbiter stays manual. *(Scaffold CODE_LANDED ≠ Gate
RESOLVED.)*
Boundary: no post-hoc band tuning · TV paste for anchors only · no offline-port authority
without a native anchor (offline fill-ports inflate — standing lesson) · fill capture only
after M1 `RESOLVED` + per-session arm GO (Addendum 2026-07-31b).
Reads (at HEAD `a6a5fe6` 2026-08-07): Q-FILLTAX-1 · `core/data/tv_exports/cme/SHA256SUMS` ·
`ops/c1_rail/c1_rail_slippage.py`
Owner: Q-FILLTAX-1.
