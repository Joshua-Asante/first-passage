# P4 (L2) — dealer-gamma / delta-hedging EOD transplant — route memo

**Date:** 2026-08-20
**Authority:** operator un-HOLD ("1 and 2" — this session) on
[`docs/briefs/programs/2026-08-17-six-lead-pursuit-plan.md`](../../../../docs/briefs/programs/2026-08-17-six-lead-pursuit-plan.md)
§2 P4. Licenses the plan's own Phase-1 item only: **route memo, not a scored
construct** — the plan itself scoped P4 as "route memo only."
**Cost / K:** $0.00 · K=0 — no data pull, no `register_search open`, no Cap claim.
**Campaign tag:** `P4-L2-GAMMA`

## Verdict: HOLD — mechanism is not a clean re-run of `Q-ORB-GEX-1`, but is not clear of its orthogonality failure either; the open question is a data-sourcing one, unresolved here

---

## §0 — Rule 0 reads (this session)

- [`lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md:63`](../koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md) — L2 row: *"Delta-hedging demand and intraday momentum: Evidence from China"* (`W4280500240`). Mechanism: option dealers defer delta/gamma-hedge rebalancing to end-of-day; same-day rest-of-day return predicts last-30-min return, decaying ~3 days. Tested on Chinese SSE50/CSI300 ETF options; the log's own note calls a CME transplant (SPX/ES, NDX/NQ dealer-GEX) "plausible," not demonstrated, and flags it "adjacent to this repo's own `Q-ORB-GEX-1`... different construction, but that orthogonality failure is a named caution."
- `docs/rejected_candidates.md` concept-intake-entry, `mechanism_family="dealer-gamma-regime-gate"`, `instrument="NAS100"`, dated 2026-06-25 — the full rejection record for `Q-ORB-GEX-1`. Pre-registered single cut (ORB-entry gated on prior-close SqueezeMetrics SPX-proxy GEX sign) was NULL: neg-gamma cut flat (t=0.22), edge direction CONTRADICTED in the positive-gamma complement, and decisively — **`G-regime-orthogonality` FAILED**: after partialling out `|gap|` and OR-range (both realized-volatility proxies), the GEX indicator's own partial-t collapsed to **−0.58**, with `corr(GEX, |gap|) = −0.27` and `corr(GEX, OR) = −0.25`. Plain reading: the free SqueezeMetrics SPX-proxy GEX feed is substantially a repackaged realized-vol proxy, not independent information about dealer positioning.
- **`addback_condition` (verbatim, the frozen re-proposal bar):** *"paid NDX-native gamma with demonstrated orthogonal separation OR a different exogenous flow series — not a sweep, sign-flip, or same-hypothesis re-run."*
- `core/data/bar_data/` (this worktree) — only `README.md` + `SHA256SUMS` present; no options/gamma-adjacent data of any kind on hand locally. No Databento cost dry-run has been run for options/greeks data on any CME index-options product as of this session (checked: no `estimate` artifact under `lab/analysis/` references options schemas for NDX/SPX/NAS100).

---

## 1. Is L2 the same hypothesis as `Q-ORB-GEX-1`, or a different one?

**Different construction, confirmed.** `Q-ORB-GEX-1` used prior-close GEX **sign** as a binary **regime gate** conditioning a separate ORB entry (a filter on when to trade something else). L2's mechanism is a **standalone momentum-continuation signal**: same-day rest-of-day return predicts the session's last-30-minute return, with the causal story being dealer hedge-rebalancing flow accumulating toward the close — a same-day, same-instrument autocorrelation claim, not a cross-session conditioning gate. These are genuinely different signal shapes, not a sweep or sign-flip of the same test.

**But the underlying exogenous flow series is the same family.** Both constructs are rooted in options-dealer gamma/delta-hedging exposure as the causal driver. `Q-ORB-GEX-1`'s specific failure was that its *particular data feed* (SqueezeMetrics' free SPX-proxy GEX) collapsed to a realized-vol proxy under an orthogonality test — a measurement-quality finding about that feed, not necessarily a general indictment of every possible way to measure dealer-hedging flow. The `addback_condition` reads this the same way: it doesn't bar dealer-gamma mechanisms outright, it bars re-proposing them on the **same, already-failed data source** — "paid NDX-native gamma with demonstrated orthogonal separation" is explicitly offered as one of two legitimate reopen paths.

**One point in L2's favor the plan's own note doesn't emphasize:** L2's evidentiary base (China, realized delta-hedging **rebalancing flow**) is architecturally closer to order-flow/microstructure than to a coarse open-interest-derived GEX index. `docs/rejected_candidates.md`'s own domain-level raised bar for single-instrument index-futures OHLCV directional timing names *"a different modality (order-flow/microstructure)"* as a standing, independent route (route ②) — separate from the mapped-cost-ratio-lever route ① that `Q-ORB-GEX-1` and this repo's dealer-gamma family sit under. If a genuinely orthogonal, flow-based (not OI-based) dealer-hedging proxy exists for CME index options, L2 might not even need the `Q-ORB-GEX-1` addback bar at all — it could route in as a microstructure-modality candidate instead.

## 2. What actually blocks a decision here

Nothing in this repo currently answers whether a CME-native, orthogonal dealer-hedging-flow measure is obtainable and affordable. No options/greeks Databento cost dry-run has been run for any index-options product. Without that, there is no way to tell whether L2 clears the `addback_condition` (different flow series, demonstrated orthogonal) or would just reproduce `Q-ORB-GEX-1`'s own vol-proxy collapse on a different feed.

## 3. Recommendation

**HOLD, not KILL, not GO.** The mechanism itself is not disqualified by the same reasoning that killed `Q-ORB-GEX-1` — but it is also not licensed to proceed to any construct design or G0 freeze on the evidence in hand. The concrete next step, if pursued, is narrow and cheap: a **Databento cost dry-run** (estimate only, no pull) on CME index-options greeks/open-interest schemas for NAS100/NQ-adjacent products, checking (a) whether the data exists and is affordably priced, and (b) whether it is a genuinely different construction from open-interest-derived GEX (i.e., a realized-flow measure, not another repackaged OI snapshot) — that second check is what would actually let it clear `G-regime-orthogonality` where `Q-ORB-GEX-1` didn't. This memo does not run that dry-run; it names it as the next licensed step, pending operator direction.

## 4. Registry / harvest limb-2

Not admitted through intake (no `register_search open`, no manifest) — per the standing precedent (P1/P2/P3 dispositions this same plan), harvest §4 limb-2's counter does **not** increment. No `docs/rejected_candidates.md` row is warranted — this is a route assessment, not a mechanism kill.

---

## Verification

```bash
grep -n "addback_condition.*dealer-gamma-regime-gate" ../../../../docs/rejected_candidates.md
# Expected: the paid-NDX-native-or-different-flow-series bar, unedited

ls ../../../../core/data/bar_data/
# Expected: README.md, SHA256SUMS only — no options/gamma data on hand
```
