# INSTRUMENT LEDGER — XAUUSD

**Symbol:** XAUUSD (Gold spot) · **Tradable:** **none** — FXIFY/DXTrade CFD venue closed 2026-07-10 · **Asset class:** precious metal
**Canonical feed:** **TV CSV export — Pepperstone** (per [`docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md`](../../docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md)). Programmatic bar feeds (Dukascopy / broker REST) and the **Alchemy** TV feed are **staging-only**; any staging result is TV-Pepperstone-verified before it gates anything. (Metals *may* fall in the proposed FX/metals Dukascopy carve-out — [`docs/adr/2026-06-12-rnd-feed-instrument-class-split.md`](../../docs/adr/2026-06-12-rnd-feed-instrument-class-split.md) §2 — but that ADR is **proposed, not ratified**; until then, Pepperstone TV CSV is canonical.)
**Status:** **DORMANT — no live venue.** The FXIFY/DXTrade CFD venue closed 2026-07-10 ([`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`](../../docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md) + its 2026-07-10 Addendum), which is what this ledger's own `venue_tradable: false` / `venue_note` already record. **Guardian Gold v5.5 remains `LOCKED · AUTHORIZED @1.00×`** at the parameter and authorization axes — what lapsed is the *execution venue*, not the strategy (the two axes are orthogonal per [`docs/methodology/strategy_lifecycle.md`](../../docs/methodology/strategy_lifecycle.md)). Plus one short-complement concept under zero-build kill-test. **Not** a clean research instrument — read W1.
**Last updated:** 2026-07-28 · **Canonical panel (Guardian baseline):** `core/data/tv_exports/pepperstone/Guardian_Gold_v5.5_PEPPERSTONE_XAUUSD_2026-05-24_1bb97.csv` (N=203, 2022-01-11 → 2026-05-14; the LOCK-of-record baseline panel, gitignored vendor bytes).

**Purpose:** Single source of instrument-level truth. Any session deriving, testing, tuning, or adjudicating on XAUUSD MUST read this file at session start and append a dated disposition at session end (operational rule 10, ratified 2026-06-11 — see [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). **Created 2026-06-15** — first post-ratification session touching XAUUSD for *new* R&D (the COMPLEMENT-XAUUSD-CGB-001 kill-test). Not a pre-emptive backfill of Guardian's lock history (that lives in [`core/strategies/_archive/guardian/LOCK.md`](../../core/strategies/_archive/guardian/LOCK.md) + `docs/adr/`). Canonical path: `ops/instruments/XAUUSD.md`.

**Ownership boundary (operational rules 5/7):** this ledger owns instrument-level findings, concept status, and the shared anti-SNAG budget. Strategy parameters stay canonical in Pine source; locked-risk constants in `dd_protection.py` / `firm_rules.py`. The ledger links out, never restates.

## PROFILE (machine-readable)

```yaml
symbol: XAUUSD
asset_class: precious-metal-spot
family: []
venue_tradable: false
venue_note: "FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: trend-following
    verdict: LIVE
    date: 2026-04-23
    source: "../../core/strategies/_archive/guardian/LOCK.md"
  - mechanism: naive-direction-mirror
    verdict: DEAD
    date: 2026-06-15
    source: "../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md"
  - mechanism: regime-overlay
    verdict: DEAD
    date: 2026-07-01
    source: "../../docs/rejected_candidates.md"
  - mechanism: compression-gated-breakout
    verdict: AMBIGUOUS-PARKED
    date: 2026-06-15
    source: "../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md"
structure:
  - claim: "Cost-law is benign on gold (~0.05R at $0.30 round-trip) — cost is not the binding constraint here."
    source: "#F3"
  - claim: "Excursion censoring is structural at ~1R, so trailing-short theses are unobservable by the excursion method and need a bar-level backtest."
    source: "#F4"
```

---

## STANDING WARNINGS (read first)

- **W1 — XAUUSD is Guardian's LIVE, LOCKED instrument.** Guardian Gold v5.5 (long-only trend-rider) trades XAUUSD in the live book. Any XAUUSD R&D (a) must NOT touch the locked strategy/params/allocation (Rule 0 / Key Principle), and (b) must clear a **book-correlation gate** vs Guardian (and the rest of Constellation) before admission — a 5th leg that re-couples to Guardian destroys the diversification rationale. Guardian's config of record (EMA/SL/TP/maxHold/session/risk) and baseline metrics (N/PF/WR/Net/DD/1R) are **not restated here** — per this ledger's own "links out, never restates" rule (line 10), see [`core/strategies/_archive/guardian/LOCK.md`](../../core/strategies/_archive/guardian/LOCK.md) (Pine config) and [`.claude/skills/trade-csv-reconcile/references/baselines.md`](../../.claude/skills/trade-csv-reconcile/references/baselines.md) (canonical baseline cache).
- **W2 — Feed discipline. Canonical = Pepperstone TV CSV. Alchemy and Dukascopy are staging-only.** Pepperstone↔Alchemy XAUUSD **diverge** ([`docs/notes/notice/N-2026-05-29-pepperstone-alchemy-feed-divergence.md`](../../docs/notes/notice/N-2026-05-29-pepperstone-alchemy-feed-divergence.md)); XAUUSD also has feed-specific stop-proximity drift on the order of ~16–29% (trade-csv-reconcile Rule-0 sub-rule). **A non-canonical-feed result does NOT transfer** — reproduce on Pepperstone TV before any disposition (the USOIL-RDM `FX_USOIL` precedent). Path-independence means an independent price *path/period*, not a feed-swap (OANDA↔Pepperstone entry-date Jaccard ≈0.96 = same path).
- **W3 — DXTrade `contractValue` for XAUUSD = 100** (verified; trade-csv-reconcile sub-rule + CLAUDE.md table). Confirmed in Guardian's live sizing. Do not size off a default of 1.
- **W4 — Guardian export entry-hour census spans 08–18** in the export's display TZ across the full 2022–26 panel (recent 2025-08+ slice is a clean 08–16). The "0800–1600 UTC" Pine header is a known doc bug — Guardian's session is chart-TZ (ET), not UTC. **A DST-aware UTC→ET mapping is required for strict Step-0 session validation** of any XAUUSD export; it does not affect excursion/cost math. (Generalizes [[platform-display-tz-edt]] / [[guardian-aegis-chart-tz-not-utc]].)

---

## DURABLE FINDINGS (instrument characterization)

> **Evidence basis:** the canonical Pepperstone Guardian XAUUSD panel (`…1bb97.csv`, N=203, 2022–2026), reduced 2026-06-15 by the excursion-bounded counterfactual + cost-law harness [`lab/analysis/legacy/xauusd_cgb_2026-06-15/`](../../lab/analysis/legacy/xauusd_cgb_2026-06-15/) (self-test verified; adversarial-verification this session). These characterize **Guardian's long trades** and what they imply for a same-bar SHORT counterfactual — NOT a standalone short backtest (which the excursion method structurally cannot produce; see F4).

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **F1** | **Guardian 1R pin validated on canonical data.** De-compounded Guardian loss median **−1.008R** (matches the independently-claimed −1.005R), confirming the 1R = 0.34%×equity-before basis. Long-trade mean **+2.03R**, median **−1.008R**, WR **22.17%** (= LOCK baseline exactly). | Canonical panel reduction 2026-06-15. | **HIGH.** Reproduces LOCK WR exactly; 1R basis = median loss per trade-csv-reconcile. |
| **F2** | **The naive Guardian-inverse (short with Guardian's own entries/exits) is DEAD.** Mean **−2.09R/trade** full panel (~−3.4R on the recent 2025-08→2026-05 window). Inverting a PF-3.75 trend-rider loses; Guardian's rare big trend-winners + violent counter-trend bounces destroy a fader. | Canonical panel; reproduces the brief's Alchemy −3.09R claim. | **HIGH.** A short complement must have its OWN compression-gated timing + tight stop, NOT a Guardian inverse. |
| **F3** | **Cost-law on gold is BENIGN** (unlike USDCAD 0.097R / USOIL 0.090R). Median 1R stop distance $5.68 (ATR≈$3.67); median cost-in-R ≈ **0.05R at $0.30 round-trip**, **0.09R at $0.50**, **0.12R at $0.70**. Scales *down* in recent high-ATR gold (~0.02R at $0.30). **Below the 0.10R kill line at realistic costs.** | Canonical panel; cost-in-R ∝ price/stop_dist. | **MODERATE-HIGH.** Cost is not the binding constraint here. **Caveat:** the live FXIFY/DXTrade gold round-trip cost is **UNVERIFIED** — broker-confirm before finalizing the hurdle (W3-class discipline). |
| **F4** | **Excursion censoring is structural at ~1R.** Because Guardian sizes `size=(equity·0.34%)/stopDist` (so 1R≡stopDist) and stops at −1.55×ATR, a long-loser ENDS at ~−1R — censoring a same-bar short's favorable excursion at ~+1R. **Short targets >1R collapse to scratch (unobservable).** Therefore the "let declines RUN past 1R with a trailing exit" thesis — the actual intended design — **CANNOT be tested by the excursion method; it requires a bar-level backtest.** | Pine source + canonical panel (at T≥1.5R: win=0, ambiguous=0 across all S). | **HIGH / structural.** This is *why* the backtest is load-bearing, not the zero-run test. |
| **F5** | **Guardian day filter (exclude Wed/Fri) is VALIDATED KEEP as drawdown control — not as a profit filter.** Excluded bucket is individually +0.90R (N=240), so on a profit objective the filter discards edge; combined Mon–Fri test: removing the filter ≈+4% net while DD inflates +45% static / +80% compounded. Displaced M/T/Th winners avg +2.66R. | [`lab/analysis/legacy/guardian_filter_sweep_2026-06-20/`](../../lab/analysis/legacy/guardian_filter_sweep_2026-06-20/); session log 2026-06-21 | **HIGH** (combined-export evidence). |
| **F6** | **Guardian session filter (NY-Ext 08–16) is VALIDATED KEEP, decisively.** Removing it loses ≈−86.5R net **and** roughly doubles DD. Per-trade “REMOVES-EDGE” on out-of-session trades is displacement-illusory — overturned by the combined test. For long-hold single-position strategies the displacement+DD test is load-bearing. | Same harness; session log 2026-06-21 | **HIGH**. |
| **F7** | **Guardian hour-blocks (Tue H08 / Mon H08 / Mon H09 / H12-entry / H12-signal-day) are VALIDATED KEEP, marginal.** Removing them loses ≈−30.8R net with +1.32pp compounded DD. Most marginal of the three filter groups; sweep complete — all three KEEP. | Same harness; session log 2026-06-21 | **HIGH** (net+DD reproduced). |
| **F8** | **Exogenous US-Treasury rate-vol does NOT carry a gold regime / participation signal** complementary to the (now-dead) KER/TSMOM gate — Q-REGIME-RATEVOL-1 FALSIFIED (marginal AUC ≈0.50; conditional-on-gold 0.582 < 0.70 bar). Hostile-era gold-chop was ZIRP low-bond-vol. | [`lab/archive/regime_ratevol_2026-06-16/`](../../lab/archive/regime_ratevol_2026-06-16/); closure in briefs INDEX | **HIGH** as a null on that exogenous series. |

**Net read (durable):** a same-instrument gold SHORT complement is **not killed** by the cheap tests, but the cheap tests can only see a **1R-scalp** short (bounds straddle zero — inconclusive), and give **zero** information on the intended **trailing trend-short**. The naive inverse is dead (F2). Cost is benign (F3). The edge claim lives entirely in the **censored** region (F4) → bar-level backtest is the load-bearing instrument. Locked Guardian filters (F5–F7) are risk/displacement controls, not profit maximizers. Rate-vol exogenous gate is dead (F8); gold KER/TSMOM participation overlay is dead (D2).

---

## ACTIVE CONCEPTS

| Concept | id | Mechanism | Status | Brief / artifact |
|---|---|---|---|---|
| Compression-gated breakout, short-primary | `COMPLEMENT-XAUUSD-CGB-001` | enter shorts only after a volatility-COMPRESSION phase resolves into downside expansion; own tight stop; trailing exit to let declines run (the inverse of Striker's `atrExpanding` common-mode gate) | **CONCEPT — kill-test AMBIGUOUS / operational HOLD (2026-06-15; 3-agent adversarially verified). Build NOT triggered.** Naive-inverse sub-thesis FALSIFIED (F2/D1). Two BLOCKERs: (a) **design-test mismatch** — the intended *trailing trend-short* payoff is 100% in the censored region (0/203 trades reach short FE≥1.5R, F4), so the cheap test gives ZERO info on the proposed strategy; (b) the only *observable* proxy (≤1R scalp) is **uneconomic** — mid-case +0.089R < 4× cost hurdle 0.211R, positive lean is ambiguous-optimism. Resolvable only by a bar-level backtest, **deferred behind the 2026-08-08 regime check** (shared with USOIL-RGC + Silver). | CC-HANDOFF Stage 1 (XAUUSD regime complement); [`lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md`](../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md) |

**Dual role:** candidate anti-Constellation **regime/direction complement** (the portfolio's first SHORT leg; first leg positively keyed to the adverse commodity-inflation/impulse regime). Must clear the book-correlation gate (|ρ_book| < 0.3) AND not go quiet in the same drought windows as the book — independently of any in-sample edge.

**Coordination (READ before progressing):** `CONCEPT-USOIL-RGC-001` remains a parked anti-Constellation complement candidate (see [`USOIL.md`](USOIL.md)). **Guardian Silver v1.0 is NOT in the book** — operator CLOSED NOT ADMITTED 2026-07-01 after the 2026-06-11 override failed its counterbalance condition; full silver record lives on [`XAGUSD.md`](XAGUSD.md). The **2026-08-08 regime check** remains the shared decision/budget point for CGB-001 + USOIL-RGC. The brief's "2-slot forward WIP limit" is **NOT a ratified rule** (P2 declined — see USDCAD ledger / ADR 2026-06-11 §2c).

---

## DEAD / REJECTED (instrument-specific)

| # | Rejection | Class | Discriminator that fired | Source |
|---|---|---|---|---|
| **D1** | **Naive Guardian-inverse on XAUUSD** (flip Guardian's long entries/exits to short) | edge-failure (sub-thesis) | Excursion-bounded counterfactual on canonical Pepperstone: **−2.09R/trade** (full) / ~−3.4R (recent). Inverting a profitable trend-rider loses by construction. | [`lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md`](../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md) (F2). Sub-thesis of CGB-001, not a standalone registry entry yet. |
| **D2** | **Gold trend-persistence regime-gate** (`KER_126 ≥ 0.12` AND `TSMOM_252 > 0` deploy-vs-wait overlay) | edge-failure (OOS invert) | In-sample separation was an n≈2-regime-block artifact; OOS falsifiers **invert** (Q-REGIME-OOS-1 DEPLOY +0.004R vs WAIT +0.284R; Q-REGIME-POSTCOVID-1 KER leg inverted). Shadow kill-tripwire unfireable. Locked book untouched. | [`docs/rejected_candidates.md`](../../docs/rejected_candidates.md) §Gold trend-persistence; `regime_stress` / `regime_oos` / `regime_postcovid` labs; ops CFD-estate retirement ADR 2026-07-11 |

**Gold-family cross-references (not XAUUSD-specific, but binding context):**
- **Guardian-family on XAGUSD (Silver)** — REJECTED 2026-05-14 (Q-CORR-1). **Guardian Silver v1.0** operator override 2026-06-11 → **CLOSED NOT ADMITTED 2026-07-01** (no counterbalance materialized). Canonical instrument card: [`XAGUSD.md`](XAGUSD.md). Re-proposal bar: new mechanism evidence, not new params.

> **§0 step-3 "re-testing something killed?" verdict (this session):** the *specific* direction (compression-gated, short-primary XAUUSD) is **NOT** on the rejected registry → admissible. But adjacent archetypes are repeatedly dead on other instruments by cost-law / no-edge (USDCAD inverse-shorts + breakouts + pullbacks; USOIL spike-fader; USOIL carry) — a strong prior that breakout/fade short edges are hard to bank. Carry that prior into the build.

---

## ANTI-SNAG LEDGER (shared budget — all sessions count)

**XAUUSD short-complement family (CGB-001):** one sub-thesis null recorded (D1, naive inverse). The compression-gated short itself is **not killed** (inconclusive-by-censoring) — distinct mechanism (own compression-gated entry + trailing exit) from the dead inverse, so D1 does not bound it. **Budget:** the brief scopes ONE concept to a forward-test admission decision; the build + selection battery is the next consumption. Coordinate with the 2026-08-08 regime check (shared with USOIL-RGC + Silver).

---

## FEED & BROKER / OPS NOTES

- **Canonical feed: Pepperstone TV CSV** (W2). Guardian XAUUSD panels present locally: Pepperstone (`…1bb97` current LOCK baseline + dated predecessors) and OANDA cross-feed. **Alchemy is staging-only and divergent** — the brief's §2.1 "precomputation" was on a non-existent-in-repo Alchemy export and is treated as unverified; the canonical kill-test (2026-06-15) supersedes it.
- **DXTrade contractValue = 100** (W3). Any short-leg sizing inherits this; a short leg also needs a `BASE_RISK` entry in `dd_protection.py` + a portfolio re-MC before go-live (the single portfolio-DD trigger scales all legs ×0.40 at −1.5%).
- **TZ:** export display TZ is chart-TZ (ET); DST-aware UTC→ET mapping for session validation (W4).

---

## OPEN QUESTIONS / WATCH

- **OQ1 — Live gold round-trip cost UNVERIFIED.** F3's hurdle (~0.05R) assumes $0.30 round-trip; broker-verify the actual FXIFY/DXTrade XAUUSD spread+commission before finalizing the cost gate.
- **OQ2 — Does the censored edge exist?** The load-bearing question (do declining-regime down-moves extend materially past the ~1R censoring point after a compression-gated entry) is answerable only by a bar-level backtest (F4). This is the build's RESOLVED/FALSIFIED pivot.
- **Decision point:** 2026-08-08 regime check — shared budget boundary with USOIL-RGC + Guardian Silver.

---

## Session log (append-only)

- 2026-06-15 / COMPLEMENT-XAUUSD-CGB-001 Stage-1 kill-test (Claude Code): ledger CREATED (first post-ratification session touching XAUUSD for new R&D). **Rule-0 landing of the claude.ai-authored CC-handoff brief surfaced three confabulations** — (a) `ops/instruments/XAUUSD.md` named as a required read but never existed; (b) validation scripts `step0_battery.py`/`selection_tests.py`/`plateau_tracker.py` named at `scripts/` but never existed (real tooling = per-investigation `lab/analysis/` harnesses + the codification pipeline); (c) the §2.1 "precomputation" cited a `Guardian_Gold_v5.5_ALCHEMY_XAUUSD_2026-06-14` export + excursion analysis with **no on-disk artifact** anywhere, on the non-canonical divergent Alchemy feed. Also: the brief's "Dukascopy canonical" feed default inverts the ratified TV-CSV policy (same error caught in the USOIL brief), and its "2-slot WIP limit" is unratified. **Operator decision (AskUserQuestion):** reproduce the kill-test on the **canonical Pepperstone** panel before any build; build only if it clears. **Result (canonical, N=203):** naive Guardian-inverse DEAD (−2.09R/trade, F2/D1); stop-disciplined short S=T=1R bounds straddle zero [−0.21, +0.38]R, **mid +0.089R < 4× cost hurdle 0.211R**; cost-law BENIGN (~0.05R, F3); the intended trailing-short edge is CENSORED (0/203 reach short FE≥1.5R) and requires a bar backtest (F4). **Verdict: AMBIGUOUS / HOLD** — 3-agent adversarial verification reproduced every number exactly; the verdict-stress agent overturned a draft "build" label with two BLOCKERs (design-test mismatch — the proposed trailing-short payoff is 100% censored; + the observable ≤1R-scalp proxy is uneconomic at mid-case). One MINOR harness bug fixed (naive cost double-count 2×→1×, −2.139→−2.086). **Build deferred behind the 2026-08-08 regime check.** No `core/` touch, no lock/allocation change. → [`lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md`](../../lab/analysis/legacy/xauusd_cgb_2026-06-15/RESULTS.md).

- 2026-06-21 / FILTER-SWEEP-XAUUSD day filter (Claude Code): landed a claude.ai filter-validation CC-handoff via Rule 0 — its `scripts/{filter_validation,selection_tests,step0_battery,plateau_tracker}.py` were **CONFABULATED** (same class as the 2026-06-15 entry); real tooling built at [`lab/analysis/legacy/guardian_filter_sweep_2026-06-20/`](../../lab/analysis/legacy/guardian_filter_sweep_2026-06-20/README.md). **DAY FILTER DISPOSITION: REMOVES-EDGE-on-profit → VALIDATED / KEEP (drawdown control).** Excluded Wed/Fri bucket is individually **+0.90R** on canonical Pepperstone (N=240; bootstrap CI [+0.25,+1.62]; distributed — survives drop-top-5; stationary) → on a profit objective the filter discards profitable trades. The objective was undocumented (operator did not recall), so resolved empirically via a **combined Mon-Fri export** (N=323): removing the filter gains only **+4% net (+17R static)** while inflating DD **+45% static / +80% compounded** (5.28→7.68% / 5.96→10.74%), RF 27→19; 37 displaced M/T/Th trades averaged **+2.66R** (big trend winners crowded out by Wed/Fri multi-day holds). The day filter is a DD control; Mon/Tue/Thu dominates on any DD-constrained basis. **No `core/`/lock/allocation change.** Also **corrected memory `feedback_oanda_dow_feed_artifact`**: Guardian day_wed's 2026-05-02 "Pepperstone feed-artifact" Stage-2 rejection (verbal, evidence-free) is a MISATTRIBUTION — Wed +0.43R OANDA replicates as +0.38R Pepperstone; real mechanism is displacement/DD (as the parallel Striker case correctly identified). Report: [`docs/ltm/briefs/Q-FILTER-SWEEP-XAUUSD-2026-06-21.md`](../../docs/ltm/briefs/Q-FILTER-SWEEP-XAUUSD-2026-06-21.md).

- 2026-06-21 / FILTER-SWEEP-XAUUSD session filter (Claude Code): **SESSION FILTER (NY-Ext 08-16) DISPOSITION: VALIDATED / KEEP, decisively.** Combined test on a `useSession=false` export (N=498, hours 0-23, days locked): removing the session filter **LOSES net −86.5R / −$58,798 static AND doubles drawdown** (static 5.28→11.07% / compounded 5.96→13.03%, +110/119%), RF 26.6→10.0 — net-negative on BOTH objectives. 379 weak out-of-session trades (E +0.48R, WR 10%, bootstrap CI-low at **0**) displace 111/203 in-session trades (203→119). The per-trade classifier flags REMOVES-EDGE (E +0.48 > gate) but it is **displacement-illusory** — overturned by the combined test. **Methodology note:** for a long-hold single-position strategy the per-trade REMOVES-EDGE view is insufficient; the combined (displacement+DD) test is load-bearing. **No `core/`/lock change.** Both day + session filters now validated; **hour-blocks remain un-swept.** Harness `run_session.py`; report §4d.

- 2026-06-21 / FILTER-SWEEP-XAUUSD hour-blocks (Claude Code): **HOUR-BLOCKS (Tue H08 / Mon H08 / Mon H09 / H12-entry / H12-signal-day) DISPOSITION: VALIDATED / KEEP, marginal.** Combined test on an all-blocks-off export (N=270, days+session locked, blocked cells repopulated): removing them **loses −30.8R net / −$20,912 static** with **+1.32pp compounded DD** (static DD ~flat 5.28→5.33%). Per-cell (in-context): Tue H08 +0.52R, Mon H08 +0.44R, Mon H09 +0.12R, H12 +0.11R (all WR 8-12%, tail-carried); blockH12Day is stateful (in combined only). 104 added trades avg +0.34R displace 37 trades avg +1.49R — same displacement mechanism, modest magnitude. **Most marginal of the 3 groups** (near-break-even); KEEP. **SWEEP COMPLETE — all 3 filter groups (day/session/hour-blocks) validated, all KEEP. No `core/`/lock change.** Independent re-derivation + adversarial-critique workflow (7 agents) returned **GO** — all 3 KEEP verdicts reproduce exactly on join-independent net+DD evidence. One secondary-diagnostic fix landed: cross-book displacement re-keyed on `(entry_time, entry_price)` and a **false reconciliation line corrected** to the exact identity `added − displaced + survivor_drift = book_delta` (the −24.8R survivor-exit-drift, real cross-book path property, was omitted before). Displaced/added cohorts (+2.66R vs +0.89R) and all headline net+DD deltas are unaffected. Harness `run_hourblocks.py`; report §4e + §5.

---

## Changelog
| Date | Entry | By |
|---|---|---|
| 2026-07-28 | **Prose-vs-YAML skew repaired (D7 hygiene, no status decision).** Header still read `Tradable: FXIFY / DXTrade` and `Status: LIVE instrument` though the CFD venue closed 2026-07-10 — while this ledger's own machine-readable PROFILE already carried `venue_tradable: false` + the correct `venue_note`. The gate (`scripts/instrument_profiles.py`) validates the YAML, not the prose, so the human layer drifted silently for ~18 days while the machine layer stayed right. Header brought in line with the YAML; **no cell, verdict, `venue_tradable`, or lifecycle value changed** — Guardian v5.5 stays `LOCKED · AUTHORIZED @1.00×`. Disposition: [`docs/notes/2026-07-28-tier-c-thread-dispositions.md`](../../docs/notes/2026-07-28-tier-c-thread-dispositions.md) §D7. | Joshua + Claude Code |
| 2026-07-16 | Coverage A+B: promoted filter-sweep KEEP → **F5–F7**; rate-vol null → **F8**; KER/TSMOM overlay → **D2**; Silver cross-ref corrected to NOT ADMITTED + [`XAGUSD.md`](XAGUSD.md). Inventory [`docs/notes/2026-07-16-instrument-ledger-coverage-inventory.md`](../../docs/notes/2026-07-16-instrument-ledger-coverage-inventory.md). No core/lock change. | Joshua + Cursor |
| 2026-06-21 | FILTER-SWEEP **COMPLETE** — hour-blocks VALIDATED/KEEP (marginal: removing loses −31R net + 1.3pp comp DD). All 3 groups (day/session/hour-blocks) swept, all KEEP. No locked-config change. | Joshua + Claude Code |
| 2026-06-21 | FILTER-SWEEP session filter **VALIDATED/KEEP** (removing it = −86R net AND DD doubles 5.3→11.1% static); per-trade REMOVES-EDGE flag is displacement-illusory (CI-low at 0). Day+session both validated; hour-blocks remain. | Joshua + Claude Code |
| 2026-06-21 | FILTER-SWEEP day filter dispositioned **REMOVES-EDGE-on-profit / VALIDATED-on-risk** (DD control; combined Mon-Fri test = +4% net for +45–80% DD; displaced M/T/Th winners avg +2.66R). Corrected `feedback_oanda_dow_feed_artifact` (Guardian Wed replicates on Pepperstone — not a feed artifact). No locked-config change. Harness at `lab/analysis/legacy/guardian_filter_sweep_2026-06-20/`. | Joshua + Claude Code |
| 2026-06-15 | Ledger created at `ops/instruments/XAUUSD.md`. Seeded W1–W4, F1–F4, D1 (naive-inverse null −2.09R), gold-family cross-refs (XAGUSD/Silver), active concept `COMPLEMENT-XAUUSD-CGB-001` (kill-test **AMBIGUOUS/HOLD**, 3-agent verified; build deferred behind 2026-08-08), anti-SNAG, feed/ops notes, OQ1–OQ2. Canonical kill-test on Pepperstone supersedes the brief's unverified Alchemy precomputation. | Joshua + Claude Code |
