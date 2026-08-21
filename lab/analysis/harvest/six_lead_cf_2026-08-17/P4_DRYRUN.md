# P4 (L2) — dealer-gamma / delta-hedging EOD transplant — Databento options cost dry-run

**Date:** 2026-08-20
**Authority:** [`P4_ROUTEMEMO.md`](P4_ROUTEMEMO.md) §3 — *"The concrete next step, if pursued, is narrow and cheap: a **Databento cost dry-run** (estimate only, no pull) on CME index-options greeks/open-interest schemas for NAS100/NQ-adjacent products, checking (a) whether the data exists and is affordably priced, and (b) whether it is a genuinely different construction from open-interest-derived GEX... This memo does not run that dry-run; it names it as the next licensed step, pending operator direction."* Operator direction this session: draft (and run) exactly that dry-run. Licenses `estimate` only — no `pull`, no G0 freeze, no construct design.
**Cost / K:** $0.00 billed · K=0 — metadata endpoints only (`estimate`, not `pull`); no `register_search open`, no Cap claim, no CONFIRM read.
**Campaign tag:** `P4-L2-GAMMA` (route memo's own tag, reused — no new tag minted)

## Verdict: cost clears trivially; the binding open question is data density, not price

Every schema tested on `NQ.OPT` (definition, ohlcv-1d, statistics, trades, tbbo) is affordable —
full-history worst case ≈ **$8.54** against the $700 ceiling (82× headroom). That answers route-memo
question (a) cleanly: **yes, the data exists and is affordably priced.**

Question (b) — whether a *realized-flow* (not OI-repackaged) measure is actually constructible — is
**not resolved by cost**, and the record counts surface a real caution the route memo didn't have in
hand: the entire `NQ.OPT` complex trades at **~985 trades/session** (OOS era, all strikes and expiries
combined) versus **~361,390 trades/session** on the underlying `NQ.FUT` itself — a **367×** density
gap. This doesn't kill the route (see §3 — the gap may be an artifact of aggregating far-OTM/far-dated
strikes that a real dealer-hedging proxy wouldn't use), but it means the next step this memo can license
is a small `definition`+`trades` **pull** to check volume concentration by moneyness/tenor, not a G0
freeze on the mechanism as designed.

---

## §0 — Rule-0 reads (this session)

- [`P4_ROUTEMEMO.md`](P4_ROUTEMEMO.md) — read in full. §3's own words are the authority for this dry-run
  (quoted above); §1 frames L2 as wanting a **flow-based** (not OI-based) proxy, explicitly closer to
  order-flow/microstructure than to a coarse OI-derived GEX index — which is why this dry-run targets
  trade-level schemas (`trades`/`tbbo`) rather than `statistics` (settlement/OI snapshots), even though
  `statistics` was checked too (§2) for completeness against "greeks/open-interest schemas" in the
  route memo's own phrasing.
- [`docs/rejected_candidates.md`](../../../../docs/rejected_candidates.md) `dealer-gamma-regime-gate`
  entry — the frozen `addback_condition`: *"paid NDX-native gamma with demonstrated orthogonal
  separation OR a different exogenous flow series — not a sweep, sign-flip, or same-hypothesis
  re-run."* `NQ.OPT` (E-mini Nasdaq-100 options, CME-native, paid via Databento) is the literal
  "paid NDX-native" target this bar names — not a free proxy feed like the SqueezeMetrics SPX-index
  feed that killed `Q-ORB-GEX-1`.
- [`lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md:63`](../koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md) —
  L2's source paper measures **realized delta-hedging rebalancing flow** (China, SSE50/CSI300 ETF
  options), not a static OI snapshot. A CME transplant needs the same shape: intraday trading activity
  in the options themselves, not an end-of-day open-interest count.
- `docs/spec/databento-data` skill (`schemas-and-symbology.md`) — schema ladder (`ohlcv` → `tbbo` →
  `mbp-1` → `mbp-10` → `mbo`) and `parent` stype confirmed to resolve options families the same way as
  futures (`ES.OPT` example in the skill; used `NQ.OPT` here as the NDX-native equivalent).
- This worktree — no prior Databento cost estimate exists anywhere under `lab/analysis/` for any
  options/greeks schema on any CME index-options product (confirmed by the route memo's own §0 check
  and independently re-confirmed by `rg` before this session's calls).

---

## §1 — Schema choice: why `tbbo`, not `trades` alone, is the coarsest schema that answers (b)

Per the databento-data skill's Rule 2 ("coarsest schema that answers the question"): a **signed**
flow measure — net buy-side vs. sell-side pressure, which is what "delta-hedging rebalancing flow"
actually means — needs the prevailing quote at each trade to classify aggressor side (tick/quote
rule). A bare `trades` schema gives price+size+time but no BBO context, so it cannot by itself
distinguish "dealers buying to hedge" from "dealers selling to hedge." `tbbo` (trade + BBO-in-force)
is the minimum schema that could support that classification — one step past `trades`, still well
short of `mbp-1`/`mbp-10`/`mbo`. `statistics` (settlement price, cleared volume, open interest) was
also estimated because the route memo's own phrasing named "greeks/open-interest schemas," but it is
exactly the **OI-snapshot** shape the route memo's §1 says would *not* clear the addback bar on its
own — included here for completeness, not as the licensed target.

---

## §2 — Databento `estimate` (no pull)

`--symbols NQ.OPT --stype parent` · research: system Python (no `.venv-research` present in this
worktree; `databento` 0.81.0 importable, `DATABENTO_API_KEY` present) · runner
`PYTHONPATH=lab python -m databento_fetch.db_fetch estimate`.

| Schema | Window | Phase | Cost | Billable | Records |
|---|---|---|---:|---:|---:|
| `definition` | 2010-06-06 → 2019-01-01 | discovery | **$0.0000** | 4.5385 GB | 8,727,886 |
| `definition` | 2019-01-01 → 2026-08-20 | oos | **$0.0000** | 2.8052 GB | 5,394,525 |
| `ohlcv-1d` | 2010-06-06 → 2019-01-01 | discovery | **$0.0000** | 0.0149 GB | 265,577 |
| `ohlcv-1d` | 2019-01-01 → 2026-08-20 | oos | **$0.0000** | 0.0261 GB | 466,272 |
| `statistics` (OI/settlement) | 2019-01-01 → 2026-08-20 | oos | **$0.0000** | 25.8353 GB | 322,941,508 |
| `trades` | 2010-06-06 → 2019-01-01 | discovery | **$1.1837** | 0.0454 GB | 945,671 |
| `trades` | 2019-01-01 → 2026-08-20 | oos | **$2.0193** | 0.0941 GB | 1,961,200 |
| `tbbo` | 2010-06-06 → 2019-01-01 | discovery | **$1.9728** | 0.0757 GB | 945,671 |
| `tbbo` | 2019-01-01 → 2026-08-20 | oos | **$3.3656** | 0.1569 GB | 1,961,200 |
| `tbbo` contrast, **`NQ.FUT`** (underlying, not options) | 2019-01-01 → 2026-08-20 | oos | **$1,293.5808** | 57.5910 GB | 719,887,969 |

Full-history `tbbo` on `NQ.OPT` alone (the licensed target schema): $1.9728 + $3.3656 = **$5.34**.
Adding `definition` + `ohlcv-1d` (both $0 both eras) for context/roll-handling: **$5.34** total,
unchanged. Every combination tested sits **≥130× under** the $700 ceiling — cost is not a gating
constraint on this candidate, unlike P3's `tbbo` finding on `CL.FUT` (12.4× *over* ceiling on a single
parent). `statistics` alone (oos era) is $0 despite being the largest byte volume tested (25.8 GB) —
consistent with Databento's general pricing pattern (bar/definition/statistics tiers are cheap;
trade-level and above bill).

Dataset floor confirmed live: `2010-06-06` (same GLBX.MDP3 floor as futures). `mbo` still
schema-limited to `2017-05-21+` (disclosed via the tool's own range metadata; not estimated — out of
scope, `mbo` is order-flow-microstructure-tier, not licensed pre-candidate per Rule 2).

---

## §3 — The liquidity finding: 367× fewer trades than the underlying, complex-wide

`NQ.OPT` (all strikes, all expiries, summed) traded **1,961,200** times over the OOS era (2019-01-01 →
2026-08-20, 1,992 weekdays) — **~985 trades/session** complex-wide. The underlying `NQ.FUT` traded
**719,887,969** times over the identical window — **~361,390 trades/session**. That is a **367.1×**
density gap (discovery era: **~423** options trades/session, same order of magnitude).

**What this does and does not show:**

- It does **not** by itself falsify the route — `NQ.OPT`'s aggregate spans potentially hundreds of
  strike/expiry combinations per day, most of them far-OTM or far-dated with near-zero volume. A real
  delta-hedging-flow proxy would only need the **near-the-money, near-dated** slice, which could carry
  most of the 985 trades/session at meaningfully higher density than the complex-wide average implies.
  **This dry-run did not check concentration by moneyness/tenor** — that requires a small `definition`
  (to get the strike/expiry grid) + `trades` (to see where volume actually sits) **pull**, not an
  estimate, and is not licensed here.
- It **does** mean the complex-wide aggregate is thin enough that "just sum all `NQ.OPT` trades per
  session" — the coarsest possible construction — is very unlikely to carry a stable signal on its
  own; some moneyness/tenor filter is almost certainly required before this is a usable input, which
  is new information for scoping any future G0 freeze (a bare complex-wide flow sum was not
  distinguished from a moneyness-filtered one in the route memo).

**Addendum 2026-08-20 — the concentration check named above was executed same day, $0.00:** see
[`p4_concentration_2026-08-20/RESULTS.md`](p4_concentration_2026-08-20/RESULTS.md). Headline: the
near-the-money/near-dated slice is **thinner relative to the underlying (~1,423×), not richer**, than
the complex-wide 367× gap above — narrowing to the construction-relevant region widens the density
gap rather than closing it. Does not settle feasibility (trade-size/notional-weighted signal
strength untested); moves the evidence against a bare trade-count construction. P4 stays `HOLD`.
- The 367× gap is a useful **sizing prior**: whatever slice of `NQ.OPT` ends up used, its trade count
  will be a small fraction of the underlying's — a future construct needs to budget for sparse-data
  handling (session-level aggregation, not intrabar) rather than assume options-market depth
  comparable to the future.

---

## §4 — What this does / does not license

**Licensed and done:** the route memo's named next step — Databento `estimate` (no pull) on CME
index-options schemas for the NDX-native family, answering both (a) cost/existence and (b) a first
pass at construction feasibility (flow-schema choice + a liquidity caution the route memo didn't
have).

**Not licensed:** any `pull` (including the small moneyness/tenor concentration check named in §3);
any G0 freeze or construct design for L2; `register_search open`; a Cap claim; running the estimate
against `ES.OPT`/`SPX` (the route memo's addback bar names *NDX*-native specifically — an ES/SPX
comparison would be its own, unlicensed scope creep); confirming whether a **micro**-listed NQ
options product exists (not verified either way this session — if one exists it wasn't checked).

**Forbidden moves:** citing the $8.54 full-history figure as if it also answered the construction
question; treating "cheap" as "GO"; treating the 367× density gap as a kill (it is a caution about
construction, not a cost or existence finding) — both would be reading past what this dry-run actually
establishes.

## §5 — Registry / harvest limb-2

Not admitted through intake (no `register_search open`, no manifest) — matching the standing
precedent for every other Phase-1 item on this plan (P1/P2/P3/P5). Harvest §4 limb-2's counter does
**not** increment. No `docs/rejected_candidates.md` row is warranted — this is a feasibility
dry-run, not a mechanism kill.

---

## Verification

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols NQ.OPT --stype parent --schema tbbo \
  --start 2019-01-01 --end 2026-08-20 --phase oos --campaign-id P4-L2-GAMMA
# expect: cost $3.3656, records 1,961,200

PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols NQ.FUT --stype parent --schema tbbo \
  --start 2019-01-01 --end 2026-08-20 --phase oos --campaign-id P4-L2-GAMMA-contrast
# expect: cost $1,293.5808, records 719,887,969 (367x the NQ.OPT trade count)

grep -n "addback_condition.*dealer-gamma-regime-gate" ../../../../docs/rejected_candidates.md
# expect: the paid-NDX-native-or-different-flow-series bar, unedited

rg -n "P4-L2-GAMMA" ../../../../lab/CATALOG.md ../../../../docs/briefs/2026-08-17-six-lead-pursuit-plan.md
# expect: no CATALOG row change needed (reuses the existing six_lead_cf_2026-08-17 slug, per P3's own precedent)
```
