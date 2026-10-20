# ADR — TV CSV exports are canonical for analysis; no canonical reliance on programmatic bar feeds

**Status:** Accepted (operator executive decision, recorded) — §2.3 and §4 #3 (tooling retained) were reversed 2026-06-17 when Dukascopy was retired (Dukascopy retired entirely; the rest of this ADR — TV exports canonical — stands); the retired-feed records are consolidated in §Retired feeds below.
**Superseded-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — Dukascopy (2026-06-17) and OANDA (2026-06-24) retirement ADRs consolidated into §Retired feeds below (ADR decay audit; operator direction 2026-10-15). Prior text at blob `c85facd8c15d01b5d8e5c3bd6adae2914b5e933b` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Superseded-in-part-by:** `2026-06-17-dukascopy-retirement.md` - Section 2.3 + Section 4 Forbidden-move #3 (tooling retained / don't-delete) superseded; TV-exports-canonical clause stands. (record tombstoned; content consolidated in §Retired feeds)
**Decision date:** 2026-06-12
**Addendum 2026-08-08 (substrate, not doctrine):** the core clause — *TV CSV exports are canonical for analysis* —
**stands and is load-bearing** (24 citing surfaces incl. six live `ops/instruments/*.md` ledgers). What has died
underneath it is the substrate this ADR named: the **canonical family is now CME futures TV exports**
(`core/data/tv_exports/cme/`) after the Pepperstone feed retired 2026-08-02 and OANDA 2026-06-24;
`core/data/bar_data/` is **RETAINED but FROZEN** (three CME micros, producer pipeline dead); and the
Dukascopy/OANDA fetch paths named in §0 no longer exist. Reviving any second feed still requires a
pre-registered decision with independent cross-feed corroboration per the second-feed reopen trigger in
§Retired feeds — never a casual revival.
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

---

## Addendum 2026-09-01 — bar_data/ panel count stale (three -> six CME micros)

This session's ADR-corpus sweep checked the 2026-08-08 addendum's claim that `core/data/bar_data/`
is "RETAINED but FROZEN (three CME micros, producer pipeline dead)" against current production
state. That count is stale.

**Current state, verified 2026-09-01** (`core/data/bar_data/SHA256SUMS` + `README.md`, read in
full): six CME micro panels are tracked -- `6J_M15`, `MNQ_M15`, `MYM_M15` (the original three,
frozen since the Pepperstone producer died 2026-08-02) plus `MCL_M15`, `M2K_M15`, `MGC_M15` (landed
2026-08-12/2026-08-13 via explicit operator-supplied CME BAR EXPORT `--in`, per
`docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md` and the directory README) -- not
simply "frozen since the pipeline died." The automated Pepperstone-fed producer
(`scripts/parse_bar_export.py`'s default path) is still dead; the three newer panels arrived through
a separate, still-live manual-supply path, not a revived pipeline.

This does not touch this ADR's load-bearing clause -- TV CSV exports remain canonical for analysis,
and the canonical feed family (CME futures TV exports; Pepperstone/OANDA retired) is unchanged. Only
the `bar_data/` parenthetical count in the 2026-08-08 addendum is corrected here. Not rewritten in
place per Rule 14; this addendum stands alongside it. No operator disposition is needed here -- this
is a factual count correction, not a decision. Correction 2026-10-15: since 2026-09-03 all four of 6J/MNQ/MYM/MGC have been refreshed via CME BAR EXPORT v0.2 `--in` ([`core/data/bar_data/README.md`](../../core/data/bar_data/README.md)); regenerable for each fresh export's window.

<a id="retired-feeds"></a>
## Retired feeds and the re-introduction bar (consolidated 2026-10-15)

Consolidated 2026-10-15 from `2026-06-17-dukascopy-retirement` and `2026-06-24-oanda-retirement`
(removed; see [TOMBSTONES](TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)); the Pepperstone
feed doctrine and the bar-data producer bars below are quoted from the 2026-08-02 Pepperstone and
2026-08-03 bar-data ADRs (also removed). Pepperstone's data retirement, offline copy (b) and 90-day
check are owned by
[substrate §11](2026-07-22-challenge-era-substrate-retirement.md#cfd-challenge-era-carried-forward).

| Feed | Retired | Removed | Survives |
|---|---|---|---|
| Dukascopy (tick REST) | 2026-06-17 | `core/lib/dukascopy.py`, its test, the Q-FEED-1 fetcher; cached `*_duka.csv` deleted in substrate Phase 5 | frozen closed-study code in `lab/archive/feed_divergence_2026-06/`; instrument-class-split ADR tombstoned |
| OANDA (REST + TV panel) | 2026-06-24 | `core/lib/oanda.py`, `oanda_creds.py`, `scripts/fetch_oanda_bars.py`, `ops/cli.py --from-oanda`, `--panel oanda`, `[mc_anchor_oanda]`; eight panel CSVs deleted in substrate Phase 5 | frozen OANDA overlay in `docs/analytics/mc_anchor_evolution/` (labelled historical); two-tier (OANDA proxy / Pepperstone validates) methodology retired to single-tier |
| Pepperstone | 2026-08-02 | TV exports + BAR EXPORT inputs (35 files), both manifest dirs | Pepperstone ADR §5-5: "Treating "no canonical CFD feed" as "no canonical feed."" is forbidden — CME futures exports are canonical for everything live |
| Databento | 2026-09-10 | — | [retirement record](2026-07-10-databento-research-stack.md#addendum-2026-09-10---operator-retirement-of-databento) |

**Bar producer** (Dukascopy ADR §2): `core/bar_export_loader.py` is the canonical bar producer of
`core/data/bar_data/<SYMBOL>_M15.csv`. Its Pepperstone default input is dead (Pepperstone ADR §2-F);
current panels land via explicit `scripts/parse_bar_export.py --in` from operator-supplied CME BAR
EXPORT captures and are regenerable only for the window a fresh export captures
([`bar_data/README.md`](../../core/data/bar_data/README.md)). Forbidden: "Writing producer
intermediates (`*_pep.csv`, `*.bars.csv`) into `core/data/bar_data/`" (Dukascopy §5); "Inventing a
CME bar regenerator / rewiring `parse_bar_export.py` without a separate producer ADR" and
"Re-pointing deleted CFD consumers to CME panels and calling the old study still runnable"
(2026-08-03 bar-data ADR §5-4, §5-5).

**Re-introduction bar.** Dukascopy §5: "A programmatic feed returns only via the §4 revert trigger or
a fresh Pre-Q, not by quietly adding an adapter." OANDA §5: "A second feed returns only via the §4
revert trigger or a fresh Pre-Q, not by quietly re-adding an adapter or a `--panel <broker>` key." A
`PANELS_BY_BROKER` key needs an admitting ADR plus registration in `core/mc/modes.py` (precedent:
[2026-08-19 CME admission](2026-08-19-cme-broker-panel-admission-for-breadth-revival.md)).

**Reopen triggers** (event-driven; fire openly with the dated incident as anchor; never edit in place):
1. Dukascopy §4: "if a **pre-registered** deep-history FX/metals gate — an `N≥100` panel OR a
   regime-robustness half-panel split that a brief floor requires — **cannot be assembled from
   operator-supplied bar exports within a single working session** (concretely, the export labor
   exceeds one session for one symbol's required window), the programmatic-feed question is reopened
   with that dated incident as the anchor."
2. OANDA §4: "if a **pre-registered** lock or allocation decision materially depends on an
   **independent second-feed corroboration** that the single Pepperstone/TV feed [now: CME futures TV
   exports] structurally cannot provide — concretely, a dated decision whose §0/§Falsifier names a
   cross-feed agreement check … and that check cannot be run because no second feed exists — then the
   single-feed posture is reopened with that dated decision as the anchor."

**Trigger check schedule:** event-driven — the two reopen triggers above fire at the dated incident; and reviewed at each quarterly programme audit (Dukascopy and OANDA ADR §4 schedules).

**Also forbidden** (both ADRs §5): citing frozen or cached bytes of a retired feed as canonical-fresh;
loosening either trigger after it proves inconvenient; re-proposing the instrument-class split,
full-Dukascopy retention, or "keep the OANDA panel as a frozen cross-check" without new mechanism
evidence against the recorded reasons (broker fidelity; carrying cost above corroboration value);
"Silently overwriting the canonical Pepperstone anchor with any OANDA-derived number" — the OANDA
overlay stays labelled historical.

**Operator follow-up** (OANDA ADR §7, undated): delete `~/.keys/oanda.txt`.
