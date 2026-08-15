# SPEC: Dense-1m entry-mechanism lane — convert Q-MNQSEL-2's oracle headroom into a TNEC-clearing construct

> ⚠ **READER-INTERCEPT 2026-08-10 — this lane's door check is UNBINDING, and a live machine-enforced bar
> blocks the next campaign.** Step 1's door check is scoped to *C1–C11 + the MNQ DEAD list* and never reaches
> the **domain-level** [`index-intraday-ohlcv-directional-timing-2026-07-21` raised bar](../rejected_candidates.md),
> which `scripts/instrument_profiles.py` (gate `instrument-profiles`, **tier=always**) prints as `BINDING BAR`
> on every MNQ intraday cell. Verified by execution: the bar appears **nowhere** in this spec, the CON-2 brief,
> or its `PREREG_G0` — so **CON-1 and CON-2 both ran unbound by it**
> (`lesson_gate_reachability_preregistration`, unbinding form, **5th firing**).
> ✅ **BOTH ITEMS RULED / REPAIRED 2026-08-10 (JA)** — [`ADR`](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md).
> **(1) Ruled OPEN:** within-instrument **temporal** selectivity is **outside** the mapped set — the mapping's
> provenance is *cross-index* RV ranking (dilution across a universe), which never tested choosing among moments
> within one instrument. Route ① is open to it under the ADR's §2-B conditions (a priori causal criterion frozen
> at G0 · every axis charges `K_intrinsic` · F2 guard and all downstream gates unchanged). **Price and hold-time
> stay mapped and exhausted; cross-index selection stays closed.**
> **(2) Repaired:** step **1a** below now requires the executed profile consult with every `BINDING BAR`
> answered by route — an unanswered bar blocks the G0 freeze.
> Evidence + the $0 falsifier that surfaced both:
> [`_cheap_falsifier_cost_geometry_2026-08-10_LOG.md`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md).

Status: PROPOSED · 2026-08-09 · authorizes nothing ($0 · K=0) · depends: [TNEC-1](2026-08-08-tnec-1-tradeify-necessary-conditions.md) `RATIFIED` · Q-MNQSEL-2 `RESOLVED` · Q-MNQDTL-CON-1 `FALSIFIED` STOP
Objective: iterate named entry mechanisms, one per campaign, on the dense-1m G=10 universe — the estate's only measured non-phantom headroom (oracle S3 ≈ 0.858 both arms vs the 0.40R inversion floor, inside the K-wall's 5–20 pt viable band) — until one clears TNEC N-EDGE+N-SHAPE or the lane stop-rule fires.

Steps:

1. **Cursor** proposes ONE new entry-mechanism family (fresh Q-ID, `Q-TNEC-CON-<n>`, next **n=6**). Mechanism class must be distinct from ES/NQ divergence (CON-1's kill), from the CON-2 compression-break row, from CON-3 HTF-native compression, from CON-4 PDH/PDL break, from CON-5 impulse-pullback-VWAP-reclaim, and from every §3.1 door C1–C11 / MNQ DEAD-list row — the brief's §0 cites the door check explicitly, per family not per parameterization.
   **1a — DOMAIN-BAR CHECK (added 2026-08-10, [ADR](../adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-D; the repair for CON-1/CON-2 running unbound).** The C1–C11 + DEAD-list check is **instrument-scoped and does not reach domain-level bars**. Additionally **execute** the profile consult and paste its output into the brief's §0:
   ```bash
   python scripts/instrument_profiles.py cell <SYM> <mechanism-id>   # exit 1 ⇒ a prior binds
   ```
   **Every `BINDING BAR` line must be answered in §0 by naming the route that clears it.** For
   `index-intraday-ohlcv-directional-timing-2026-07-21` the routes are ① mechanism outside the mapped
   cost-ratio levers {price · **cross-**instrument-selection · hold-time} · ② different modality/venue ·
   ③ beats incumbent ORB-MNQ net-of-cost. **Ruled 2026-08-10:** within-instrument **temporal** selectivity is
   **outside** the mapped set ⇒ route ① is open to it, under the ADR's §2-B conditions (criterion causally named
   a priori and frozen at G0; every axis charges `K_intrinsic`; F2 guard and all downstream gates unchanged).
   **An unanswered binding bar blocks the G0 freeze** — no exceptions, and a remembered answer is not an
   executed one.
2. Parent-side **cheap falsifier** (<5 min, designed GENEROUS so failure is conclusive) BEFORE authoring the G0 — on the existing `_mnq_1m.parquet` panel; a failed cheap falsifier kills the proposal at $0 with no Q-ID spent.
3. Freeze `PREREG_G0` (schema × window × catalogue ≤3 cells; `K_intrinsic` = catalogue size) + S6 `evaluate_admission` ADMIT (`lab/discovery/admission_schema.py`) in a commit **strictly earlier** than any score (Rule 8.7; sentinel PREREG scans watch this).
4. **Operator explore GO** — cache reuse only (`_mnq_1m.parquet`, existing tbbo caches). Any new Databento pull needs its own cost dry-run + separate GO.
5. Score EXPLORATION; close with the TNEC verdict string `N-ACT N-SURV N-EDGE N-SHAPE N-SIZE | bust | P(pass) | μ(disclosed)` + typed Iterate block. CONFIRM windows stay unread until a separate confirm GO.
6. **Lane stop-rule:** 3 consecutive FALSIFIED mechanisms on this universe → a lane-review packet to the operator (SNAG discipline), never a 4th campaign by default.

Gate: RESOLVED if a campaign emits ≥1 candidate clearing N-EDGE + N-SHAPE at pre-registered explore→confirm discipline (routes to operator GO; admits and arms nothing). FALSIFIED per-campaign as each PREREG pre-registers; the lane itself carries **no calendar clock** — 2026-11-08 belongs to [four-firms §4](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) alone.
Boundary: no retune of G / lookback / θ-window and **no sign-invert** (CON-1 STOP; own-instrument momentum → C5/D5-RECOST-1) · no C1–C11 reopen without new *mechanism* evidence · MNQDTL D1/D2/μ are recorded preferences, never gates · no deploy, no Pine, no arming, no `LEG_MAP` claim.
Reads: [TNEC-1](2026-08-08-tnec-1-tradeify-necessary-conditions.md) §N-limbs · [Q-MNQSEL-2 RESULTS](../../lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/RESULTS.md) · [CON-1 closure](../briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md) (STOP scope) · [MNQ ledger](../../ops/instruments/MNQ.md) C1–C11 + DEAD · [K-wall](../../lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) · [Route B checklist](../methodology/avenue_a_generate_confirm.md)
Verify (Phase-0, Cursor runs before authoring): `ls lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet` · `rg -n "N-EDGE" docs/spec/2026-08-08-tnec-1-tradeify-necessary-conditions.md` · `rg -n "new entry mechanism" docs/briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md`
Owner: TNEC-1 §2 intake (this spec is its L4 construct lane); campaigns dock under fresh Q-IDs.
