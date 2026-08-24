> ⚠ **2026-08-23 reader-intercept (R1 CLOCK repair, fix-pass):** the Gate-arm table below (25K
> 0.50% · 50K 2.81% · 100K 12.42% · 150K 8.74% · 250K 21.16% bust) is **EOD-clock**, produced on the
> same live `simulate_path` engine R1 measures, with `intraday_low` never populated — every bust
> figure here is a lower bound, not an estimate. The 100K/150K/250K cells are already FAIL against
> the current 3.0% survivor-scoring ceiling and can only deepen on the honest clock (monotonicity);
> the 25K/50K cells PASS on this clock but are a named, un-re-run residual — not confirmed to still
> PASS honest-clock. See
> [`../../analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md`](../../analysis/c1/firm_model_repair_r1_7tier_2026-08-23/RESULTS.md)
> §2/§4b for the full accounting and why this campaign is not re-run. Frozen body unedited below.

# C5 — integer-contract Bulenox re-MC (cap-aware, cost-aware)

**Date:** 2026-07-03. Layers onto C4 ([`RESULTS_C4_forceflat_2026-07-03.md`](RESULTS_C4_forceflat_2026-07-03.md)): FF DJ30 + clean NAS100, static tier balance, `PRE_SHOCK_1R`-pinned ideal panel, C2-off gate arm — now with **per-trade integer-contract ratios** (time-matched roll-masked futures ATR(11) at each entry, era-correct), **Bulenox Option 1 contract caps** (primary-confirmed 30/70/120/150/250 micros), **RESERVE cap policy** (base ≤ ⌊cap/(1+pyr)⌋ so the pyramid add — the edge — fits at full ratio; matches the B1/B2 editions exactly), and **$2.22/contract RT costs** ($0.61/side all-in per Bulenox Rates.pdf + 1-tick slip/side).

## Gate arm — integer + costs, C2-off, inactivity mitigated (token trade)

| Tier | pass / bust (all trailing) | p99 DD | med days | DJ30 mean ratio (base cap) | NAS ratio / skips | hist. 1st payout |
|---|---|---|---|---|---|---|
| 25K | 99.50% / 0.50% | 5.28% | 136 | 0.61 (cap@3) | 0.44, **71/163 base skipped** | d375 |
| 50K | 97.19% / 2.81% | 4.91% | 107 | 0.77 (cap@8) | 0.73, 10 skipped | d369 |
| 100K | 87.58% / 12.42% | 2.98% | 95 | 0.72 (cap@14) | 0.86, 3 skipped | d369 |
| **150K** | **91.26% / 8.74%** | 2.98% | 101 | 0.62 (cap@17) | 0.90, 1 skipped | d369 |
| 250K | 78.84% / 21.16% | 2.19% | 87 | 0.63 (cap@29) | 0.94, 0 skipped | d369 |

Sensitivities: **no-cost** arm = 25K 99.98 / 50K 99.70 / 100K 96.91 / 150K 98.05 / 250K 92.31 (isolates cost drag: −0.5 to −13.5pp — hits big tiers hardest because the fixed-$ trailing cushion is a smaller % there). **Unmitigated inactivity=5 idle bdays @150K: 95.58% of paths die to inactivity** (pass 4.38%).

## Findings

1. **Pre-registered pooled gates (bust <1%, p99 DD <5%): NO tier passes both.** 50K–250K clear p99 but fail bust <1%; 25K clears bust but fails p99 and is design-void anyway. Reported without softening (pre-reg is binding). **Gate-provenance flag, not a re-gate:** the <1% bust gate was calibrated for the one-shot FXIFY $200K challenge; Bulenox evals are $145–$535/mo cheap-retry instruments with fan-out. Whether 91–97% pass at ~$150–325/attempt-month is acceptable EV is a **new, operator-owned gate decision** — it cannot be inherited from the FXIFY criterion and must not be decided post-hoc by this doc.
2. **The token-trade insurance is MANDATORY, not optional.** Bulenox's ≥1-trade-per-5-trading-days rule, unmitigated, kills ~96% of paths (the book structurally idles Wed+Thu; ~23% of weeks are signal-dead). A scheduled 1-micro token trade (~$2.22 + a tick of risk, automatable in TradersPost) reduces this to ~zero. This is now a hard requirement of the execution layer.
3. **Tier ordering inverts vs C4's %-equity picture.** Cost drag + cap binding move the optimum: 25K/50K's shiny C4 numbers were phantoms (25K: NAS skips 44% of entries — that is not the designed book; 50K NAS runs 0.73×). **150K is the most designed-book-faithful tier** (NAS 0.90×, 1 skip) at 91.26%; 100K is *worse* than 150K (87.58%) because its looser DJ30 cap lets more risk through against the same 3.0% cushion; 250K's 2.2% cushion is simply too tight (78.84%).
4. **DJ30 is cap-bound everywhere (~0.61–0.77× locked risk).** The Bulenox contract cap — not granularity — is DJ30's binding constraint at every tier, exactly as the B0 flag predicted. The RESERVE policy preserves the 750% pyramid *ratio*; the cost is base size. This is a venue constraint, not a parameter change (locked 0.70% untouched).
5. **The payout picture is the sobering one.** Historical-path first 40%-consistency-eligible payout ≈ **day 369–375** at every tier (single 2022-start path; the big early DJ30 trend days dominate the best-day numerator). Point estimate only — the MC-distribution version is owed — but it corroborates the standing finding that the consistency rule forces late, lumpy extraction. Median *pass* is also slow: 87–136 days vs FXIFY's 26.

## Caveats

- **Transplant frame:** CFD trade P&L × integer ratios, not futures-native panels — C3's attribution ladder (needs the TV backtests of the B1/B2 editions) refines this.
- Assumes **one strategy per master account** (fan-out), so caps aren't shared; a shared account would bind harder on Tue overlaps.
- Historical-path payout delay is a point estimate; per-path MC distribution owed (C5 prereg #4).
- Engine's inactivity proxy = consecutive zero-P&L bdays (a BE-exit day counts as active — close enough at panel granularity).

## Reproduction

Driver: session scratchpad `c5_integer_remc.py` (RESERVE policy; `run_seed` called directly with `dd_scale=1.0` for C2-off; caps/costs/targets from the 2026-07-03 primary-source sweep; NQ/YM bars re-parsed from the 2026-07-01 BAR_EXPORTs).

## Addendum 2026-07-03 — base-skip chain-kill sensitivity (open verification item, NAS100-specific)

An independent parallel build (PR #275, closed unmerged in favor of this doc — see below) modeled the same hostable-set / integer-sizing question with a simpler sizing layer (risk-floor only, no contract cap) and surfaced a distinct sensitivity worth checking against this C5 model: **if a base entry's contract count rounds to 0, can its pyramid add still be independently sized and counted as a real trade?** Physically it cannot — there is no base position to add to — so a model that floors the add from its own risk fraction, independent of whether the base survived, can count "orphan adds" that couldn't happen live. In that simpler build, applying a base-skip chain-kill rule (suppress any add whose base rounded to 0) flipped the headline 25K p99 DD from 4.95% to 5.11% (a 0.16pp swing, thinner than the semantic ambiguity itself) — 27% of NAS100 base entries rounded to 0 at that tier in that model.

**Why this likely doesn't affect DJ30 here:** the RESERVE cap policy above computes the base cap as `⌊cap/(1+pyr)⌋` and the add as a fraction of that *already-capped* base — the add is structurally derived from the base's surviving size, so a 0-contract DJ30 base cannot produce a nonzero add by construction, at every tier (DJ30 is cap-bound everywhere per Finding #4).

**Why this is an open question for NAS100:** the B1/B2 edition notes describe NAS100 as "cap-safe at all tiers" (never hits the Bulenox contract cap), which means its sizing is plausibly a pure risk%-of-equity floor rather than RESERVE-coupled — the same shape as the simpler build's vulnerable case. NAS100's own base-skip counts here are non-trivial at the small tiers (71/163 at 25K, 10 at 50K) — the same regime where the sensitivity would bite hardest. Whether this C5 model's NAS100 add-sizing is base-derived (safe) or independently floored (vulnerable) is not resolvable from this doc alone; the driver (`c5_integer_remc.py`) is an untracked session scratchpad, not checked into the repo, so it could not be inspected to confirm either way as part of this addendum.

**Disposition:** not a correction to the table above — flagged as a targeted follow-up for whoever next touches the NAS100 sizing path in a lock-grade version of this driver. Given 25K is already called design-void here (Finding #3) and the 50K skip count is small (10/≈163), the practical exposure is bounded to that one already-caveated tier.

**PR #275 disposition:** closed unmerged 2026-07-03. It reached the same ultimate verdict as this doc (no tier cleanly passes the pre-registered bust<1%/p99 DD<5% gates) via a materially less complete methodology — no Bulenox contract-cap modeling, no cost modeling, no explicit `PRE_SHOCK_1R` pin — which is why its intermediate per-tier numbers diverge from this doc's (e.g. its uncapped 100K/150K bust rates run ~18% vs this doc's cap-aware 12.42%/8.74%). This doc is canonical for the P4 futures-constrained re-MC question.

## Addendum 2026-07-05 — driver recovered + landed; orphan-add question RESOLVED (no orphans)

The driver is no longer an uninspectable scratchpad: [`c5_integer_remc.py`](c5_integer_remc.py) was recovered from the authoring session's transient scratchpad before cleanup (byte-identical to the run vintage, sha256 `1300cede117fba9c55a7ae1fc9d2bfdffee1fcf0fed66ad3d29ee7e594155257`) and is now tracked in this directory.

**Inspection resolves the 2026-07-03 addendum's open item: NAS100 add-sizing is base-derived, exactly like DJ30 — orphan adds are structurally impossible in this model.** The add-sizing branch applies to both legs uniformly: `add_int = int(math.floor(p["base_int"] * cfg["pyr"])) if p["base_int"] > 0 else 0`, followed by `add_int = min(add_int, cap - int(p["base_int"]))`. Every add is derived from its parent base's *integer* (post-floor, post-RESERVE-cap) contract count and is forced to 0 when the base rounds to 0. The "independently floored" vulnerable shape from the PR #275 build does not exist here. **The gate-arm table above stands as-is; the targeted follow-up is CLOSED.**

Provenance caveat for re-runs: the driver hardcodes `REPO = .../adoring-nobel-143d23` — the (since-removed) worktree it ran in. It is landed verbatim as the provenance artifact for the table above; repoint that path (and re-verify the bar/CSV inputs) before any re-execution.
