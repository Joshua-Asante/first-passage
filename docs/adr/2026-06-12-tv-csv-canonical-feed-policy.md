# ADR — TV CSV exports are canonical for analysis; no canonical reliance on programmatic bar feeds

**Status:** Accepted (operator executive decision, recorded) — **§2.3 + §4 Forbidden-move #3 (tooling retained / don't-delete) SUPERSEDED 2026-06-17 by `docs/adr/2026-06-17-dukascopy-retirement.md`** (Dukascopy retired entirely; the rest of this ADR — TV exports canonical — stands)
**Superseded-by:** none
**Retain-until:** none
**Superseded-in-part-by:** `2026-06-17-dukascopy-retirement.md` - Section 2.3 + Section 4 Forbidden-move #3 (tooling retained / don't-delete) superseded; TV-exports-canonical clause stands.
**Decision date:** 2026-06-12
**Addendum 2026-08-08 (substrate, not doctrine):** the core clause — *TV CSV exports are canonical for analysis* —
**stands and is load-bearing** (24 citing surfaces incl. six live `ops/instruments/*.md` ledgers). What has died
underneath it is the substrate this ADR named: the **canonical family is now CME futures TV exports**
(`core/data/tv_exports/cme/`) after the Pepperstone feed retired 2026-08-02 and OANDA 2026-06-24;
`core/data/bar_data/` is **RETAINED but FROZEN** (three CME micros, producer pipeline dead); and the
Dukascopy/OANDA fetch paths named in §0 no longer exist. Reviving any second feed still requires a
pre-registered decision with independent cross-feed corroboration per the OANDA-retirement ADR §4 revert
trigger — never a casual revival.
**Authors:** Joshua (decision) + Claude Code (recorder, this session)
**Supersedes:** the per-analysis "Dukascopy canonical" data-source designations in R&D briefs (e.g. CC-HANDOFF-USDCAD-RDM-001-stage1-f1 §2.2(a)); does NOT supersede `docs/spec/feed_equivalence_discovery_test_LOCKED.md` (firm-onboarding execution-feed equivalence — different question, unaffected)
**Related:** `docs/adr/2026-05-10-manifest-integrity-gate.md` (vendor-CSV integrity) · `docs/methodology/lessons/methodology_lessons.md` (parity-gate lesson: feed-source + PF≈1 calibration) · PR #152/#153 (the Dukascopy adapter this policy demotes to staging)
**Layer:** governance (data-source doctrine for `lab/` analyses and anything feeding a canonical verdict)

---

## §0 — Rule 0 reads (this session, 2026-06-12)

- `core/data/tv_exports/candidates/concept-gbpusd-vbr-001/full_2018_2024/rank_cert_verdict.json` — the load-bearing divergence record: python bar-feed engine vs TV native on the same GBPUSD window/config: **892 vs 894 trades ("different logic, not rounding"), net profit off by 137.267%** ($11,834 vs $4,988), PF diff 1.69%. Verdict field PENDING (1/12 paired) — the cross-feed anchor info is the relevant part here.
- `lab/analysis/silver_regime_2026-06-10/dukascopy_feed_equiv.py` — the honest counterpoint: at **daily-range granularity** Dukascopy XAGUSD contained 10/10 Pepperstone trade-leg prices across 3 regimes (2022 chop / 2023 runner / 2025 trend); bar-equivalence at that granularity passed.
- `core/lib/dukascopy.py` (anchor `a43919b`) — the adapter being demoted: tick-file feed, mapped point factors, closed-market 5xx skip+count.
- `core/data/bar_data/` + `SHA256SUMS` — existing pinned bar files (GBPUSD_M15.csv et al.) remain manifest-tracked staging artifacts.
- `lab/analysis/usdcad_rdm/CARD.md` (this session) — the first analysis authored under this policy: USDCAD/WTI price series are operator-supplied TV chart exports; official rate series (Treasury/BoC) unchanged.

## §1 — Context

Two R&D shakeouts established that **strategy-level results do not transfer across feeds** at the precision our verdicts need: the GBPUSD parity shakeout (TV chart feed ≠ REST feed broke trade-count-exact parity; symmetric gross drop, not slippage) and the rank-cert cross-feed record above (net off by 137% at PF≈1 — net is ill-conditioned there, which is itself the lesson). Meanwhile the Silver feed-equivalence checks passed at daily granularity — so the divergence is granularity- and use-case-dependent, and every new analysis was paying a fresh "is this feed equivalent enough?" argument.

The operator's executive decision removes that per-case argument: **one canonical data family.** TV CSV exports are already canonical for strategy behavior (Rule 0), MC anchors (Pepperstone panels), and the BT-OFF doctrine; this extends the same status to analysis inputs.

## §2 — Decision

1. **Canonical analyses, verdicts, locks, and registry entries rest on TV CSV exports** (chart exports or Strategy Tester exports) or on **official non-bar series** (central-bank / treasury / statistical-agency data, e.g. BoC Valet, treasury.gov), which are not bar feeds and are unaffected.
2. **Programmatic bar feeds (Dukascopy, broker REST) are staging-only**: prototyping, ranking, smoke tests, pre-filtering. Nothing staged on a bar feed becomes canonical without TV verification (the rank-cert pattern: python stages, TV native runs certify).
3. **Tooling is retained, not deleted**: `core/lib/dukascopy.py`, `scripts/fetch_oanda_bars.py`, and pinned `core/data/bar_data/` files stay (staging + historical reproducibility). The Stage-3 sweep survives explicitly under this policy as a staging consumer.
4. A canonical artifact citing price data must name its TV export (or official series) the same way MC anchors name their panel CSVs.

## §3 — Falsifier / revert triggers

- An analysis class becomes impossible under the policy (e.g. an intraday cross-instrument join TV exports cannot supply at the needed depth) and the choice is policy violation vs analysis abandonment → revisit scope at that dated incident, not before.
- A TV-export-sourced canonical verdict is later shown wrong **specifically because** the TV feed diverged from the broker execution feed → the policy's premise inverts; reopen.
- TV export availability/limits change materially (plan limits, format).

## §4 — Forbidden moves

1. Citing staged bar-feed results as canonical because "the numbers looked close" — that is the per-case equivalence argument this ADR exists to end.
2. Re-running a failed TV-based verdict on a bar feed to shop for a pass.
3. Deleting the staging tooling as "dead under policy" — it is demoted, not dead; the M-9 manifest gate still applies to its pinned artifacts.
4. Extending this ADR to the firm-onboarding feed-equivalence question — that stays governed by the LOCKED spec.
