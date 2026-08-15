# Q-RAIL-1 — CLOSURE: `RESOLVED` (decision-ready GO/NO-GO packet emitted)

**Closed:** 2026-07-17
**Parent brief:** [`../Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../Q-RAIL-1-c1-execution-rail-go-live-scoping.md)
**Pre-registration:** [`../pre-registration/Q-RAIL-1-verdict-preregistration.md`](../pre-registration/Q-RAIL-1-verdict-preregistration.md) (mechanism followed: ceiling deferred to Phase 4, then re-requested fresh)
**Annex (the packet — the recommendation artifact per §9):** [`lab/analysis/c1/q_rail_1_2026-07/PHASE4.md`](../../../lab/analysis/c1/q_rail_1_2026-07/PHASE4.md) · full evidence chain [`RESULTS.md`](../../../lab/analysis/c1/q_rail_1_2026-07/RESULTS.md)

## Verdict

**H-RAIL-1 ACCEPTED → `RESOLVED`.** A ToS-compliant, attended-automation execution path for c1's WATCH-1 deployable expression exists at **both** discharge tiers:

- **F1–F5 all PASS** (F1 via the ratified account-multiplier-layer fallback; F3 via Step-2 parity + C3 1a→1c on operator CME exports).
- **Rail chain documented end-to-end from primary sources:** TV alert → CrossTrade cloud → NT8 Add-On → Tradovate (either firm), with the NT8-side sizing host as the §4-screened computation path.
- **Cost table complete and ceiling signed:** operator set the §8 ceiling at **$700** (2026-07-17, `AskUserQuestion` against the assembled table — the fresh sign-off the ratification deferred). Cost-to-first-live-fill: Tradeify Select **$328 list / $258 promo** · MFFU Rapid **$414** · worst case + one reset **$681** — **both tiers clear, with one-reset headroom**. H-RAIL-1's cost clause ACCEPTS at both tiers.

**Tier recommendation (packet §5): `Tradeify_Select_100K` primary, `MFFU_Rapid_100K` fallback** — cheaper all-in, softer EOD failure mode (16:59 non-fatal auto-flatten vs post-16:10 DISQUALIFY), consistency rule stricter on paper (40% vs 50%) but eval-only-soft per `firm_rules.py`.

## What this closure does NOT do (§5 + self-funded-close ADR §5 honored)

The GO on rail build + account registration + live spend is **not made here** — it is a fresh operator decision requiring its own ADR. This closure emits the decision-ready packet only. No account opened, no CrossTrade/NT8 wiring, no spend, no `ACTIVE_FIRM` switch.

## On GO (pre-registered consequences, §6)

1. Fresh GO ADR names the tier, the account, and the build plan (packet §4 preconditions: alert-payload contract on venue editions · NT8 sizing host · CrossTrade Pro + Account Manager ≤16:00 ET · Tradovate-at-checkout landmine).
2. Q-NAS-ECR-1 successor Pre-Q authorized (MNQ fill source exists; re-point is not type-preserving — fresh Pre-Q per STATE).
3. ORB-MNQ-1 decay-monitor calibration re-scoped to the live venue.
4. Fill-starved threads re-arm: Q-DECAY-1 re-arm limb, lifecycle Call-1 live inputs.

## Standing risk framing (carried verbatim from the packet — must ride any GO ADR)

WATCH-1 ~doubles median days-to-pass (pass ≥95% in-horizon); Q-DECAY-1 common-mode edge death uncovered (drawdown-only detection); Q-PERSIST-1 +0.46pp bust optimism; the H1 regime rescue is the haircut's doing; return language stays bust/pass-geometry, never P&L.
