# INSTRUMENT LEDGER — NQ

**Symbol:** CME E-mini Nasdaq-100 ($20/pt) futures (NQ; Globex, Databento dataset `GLBX.MDP3`) · **Micro sibling:** MNQ ($2/pt) · **Asset class:** equity index futures
**Status (2026-08-04):** Micro sibling [`MNQ.md`](MNQ.md) is **NO LONGER A LIVE c1 LEG — withdrawn from deployment** (Tradeify de-scoped for the locked Striker book, evaluation included — [`ADR 2026-08-04`](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md); Addendum narrows the bar to redeployment, not Tradeify-shaped research). **All deployment / sizing / cap / rail facts live on [`MNQ.md`](MNQ.md)** — this parent does not restate them (Rule 10). Lifecycle on the book side unchanged (`AUTHORIZED · MECHANISM @ 1.00×`; canonical: [`strategy_lifecycle.md`](../../docs/methodology/strategy_lifecycle.md)). Cash-index sibling (NAS100 CFD) hosts locked Striker NAS100 v1 on a closed venue — nothing in this ledger touches it.
**Last updated:** 2026-08-06

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Any session deriving/testing/adjudicating on NQ/MNQ MUST read this at session start and append a dated disposition. **Created 2026-07-24** by operator ruling #6 of the Algorithm repo review ([`docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`](../../docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md)) — the 2026-07-16 coverage inventory had left the NQ/MNQ side open (parent-hosts-micro convention per [`YM.md`](YM.md)). Distinct instrument from the NAS100 CFD surface — findings do not transfer automatically in either direction.

## PROFILE (machine-readable)

```yaml
symbol: NQ
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: AMBIGUOUS-PARKED
    date: 2026-07-23
    source: "../../docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md"
  - mechanism: intraday-momentum
    verdict: DEAD
    date: 2026-07-21
    source: "../../docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md"
  - mechanism: opening-pressure
    verdict: DEAD
    date: 2026-07-21
    source: "../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md"
bars:
  - id: index-intraday-ohlcv-directional-timing-2026-07-21
    source: "../../docs/rejected_candidates.md"
```

---

## STANDING WARNINGS (read first — bind any GLBX/Databento window work)

- **W1 — `.c.0` continuous is calendar-roll, front-month, UNADJUSTED.** Same feed rule as ES/YM ([`ES.md`](ES.md) W1). NQ rolls quarterly, mid-month (3rd-Fri expiry: Mar/Jun/Sep/Dec) — windows spanning a roll date carry a phantom calendar-spread jump. **`.v.0` (volume-roll) matches TV's `1!` continuous** — the ORB-MNQ pipeline and D5 pulls used `MNQ.v.0` for exactly this reason (see memory-anchored roll-rule lesson: roll rule changes bar EXISTENCE, not just prices).
- **W2 — Databento `ohlcv-1d` buckets by UTC calendar day → phantom Sunday bars.** Feed-general ([`ES.md`](ES.md) W2): drop settle-date weekday > 4 before any trade-date offset work.
- **W3 — Databento cost boundary (2026-07-24):** the entitlement is recent-data, not by-schema — full-span `bbo-1s`/`tbbo` pulls BILL (both c1 legs quoted $272.91); granularity is per-day, so pull event-days only and never extrapolate a span cost from a 1-month sample. Run the mandatory cost dry-run (databento-data skill) before every pull.

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **N1** | **ORB-MNQ-1 (opening-range breakout, exit-at-close) is the pipeline's only full Stage 2–8 survivor — admitted lifecycle `CANDIDATE @ 1.00×` 2026-07-16, PARKED by operator directive 2026-07-23.** Stage-2 cost-law PASS (5.31×/8.10× — convention `edge / mean_cost_R`, **bar 4.0×**; NOT the `edge / hurdle_4x` bar-1.0 convention the bp-denominated rows above use, and the two differ by exactly 4×. Basis = the frozen **Bulenox $0.61/side + 1-tick** research cost model, `rt_pt` 1.11), DSR full 0.9754 / annSR +0.890, temporal 2021+ PASS, placebo p=0.0040, Stage-8 risk N_eff 1.99→2.95, corr +0.15 vs the MNQ-Striker leg. **Stage-7 firm rider — do not quote the full-window pass unqualified:** 2021+ survives all four friendly firms (to 3-tick slip), but the FULL window clears **only at Bulenox at ≤1 tick**; Tradeify ($0.91, `rt_pt` 1.41), MFFU and BluSky-NT ($0.95 NT-schedule proxy — ⚠ M40: not venue-published for F3 ranking, 1.45), and BluSky-Rithmic ($0.50) — **no basis is privileged** (Bulenox $0.61 / Tradeify $0.91 / MFFU · BluSky-NT $0.95 / BluSky-Rithmic $0.50; see [`MNQ.md`](MNQ.md) 2026-08-04d). Tradeify / MFFU / BluSky-NT all **FAIL** the full window on the Stage-6 limb (Tradeify annSR +0.835 / DSR 0.9644), and even Bulenox fails at 2 ticks. Standing caveats: regime-common-mode + high-variance/risk-dominant; live-venue decay-monitor calibration owed on the open manifest [`orb_mnq_intraday_breakout`](../../discovery_manifests/orb_mnq_intraday_breakout.json). | [`ADMISSION`](../../lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md) · [`RESULTS`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS.md) · [`RESULTS_stage7`](../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md) (firm × slip table) | **HIGH** (full pre-registered pipeline). |
| **N2** | **Composing ORB-MNQ into the c1 2-leg book FAILS on variance dominance** (Q-COMPOSE-1 CLOSED FALSIFIED 2026-07-17): ORB @0.37% carries $438/day std vs $273/day for the entire 2-leg book — correlation breadth without risk breadth is anti-help against a $-denominated trailing barrier (H1 bust 54–68% composed). Breadth lever closed; sizing (WATCH-1 0.50×) is the lever that passed. | [`closure`](../../docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md) | **HIGH**. |
| **N3** | **Intraday momentum (Baltussen-class) is statistically absent on modern MNQ.** D5: IS +1.46 bp gross vs 11.06 bp hurdle (cost-law KILL 2026-07-16); D5-RECOST-1 (2026-07-21): the cost-geometry thesis was real (hurdle 11.06→3.01 bp) but the OOS edge decayed **negative** (−0.327 bp, gross Sharpe −0.13) — corroborates the published post-2021 decay and the external MNQ 14-signal-family falsification (arXiv 2605.04004). Re-proposal needs new mechanism evidence, not new costs/windows. | [`D5 RESULTS`](../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md) · [`D5-RECOST RESULTS`](../../lab/archive/d5_recost_2026-07/RESULTS.md) | **HIGH**. |
| **N4** | **Opening-volume × directional-efficiency has no usable signal on MNQ** (OPENPRESS-1 CLOSED FALSIFIED 2026-07-21: MNQ HAC t underpowered; no threshold/window rescue). Opening-range *momentum* is equity-index-specific (ORB-ZB-1: does not port to Treasuries) — the mechanism class lives here, but only the N1 construct has survived costs. | [`OPENPRESS closure`](../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md) · [`ORB-ZB closure`](../../docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md) | **HIGH**. |
| **N5** | **Data panels on file:** databento `MNQ.v.0` continuous `ohlcv-1m` 2019-05-06→2026-07-16 (2,535,465 rows, $0.00, `--phase oos`) + parent `NQ.FUT` `ohlcv-1m` 2010-06-06→2019-01-01 (3,396,639 rows, `--phase discovery`) — [`PULL_LOG`](../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/PULL_LOG.md); BAR EXPORT v0.2 `MNQ1!` TV panel → `core/data/bar_data/MNQ_M15.csv` (n=141,536; 2020-07-01→2026-07-02Z; manifest-pinned). Provisional locked-risk floor mirror (2026-07-16): MNQ full-median **$15,591** / recent-90d **$29,559**. | [`STATE.md`](../../STATE.md) reconstruction line · PULL_LOG | **HIGH** (recorded pulls). |
| **N7** | **Venue-fact correction 2026-07-22 (Tradeify geometry — dated record).** Tradeify's contract cap is **account-aggregate, not per-leg** — `LEG_MAP` allocates **MNQ 11** / MYM 69 (the prior undivided-80 read was 1.91×); **flat deadline 16:45 ET**; **US Treasuries untradable** at this firm; the hedging rule (MYM+MNQ share the Equity Index Product Group) **clears by construction** because c1 is long-only at Pine, rail, and realized layers. ⚠ Does **not** bind a deployed MNQ leg's order geometry today (leg withdrawn 2026-08-04); do not treat 11/69 as a live reservation consuming headroom. Same pass **withdrew the prop-portfolio §4 discharge** (eval rows had modeled a drawdown lock neither Tradeify nor MFFU applies in eval → both `trailing_locking` tiers flip Part A PASS→FAIL, zero clearers at the frozen gate's $100K band, 11-08 hard date unchanged), which flagged the c1 GO's WATCH-1 0.50× risk figures as unmeasured under corrected geometry. **Updated 2026-07-25:** those figures were **measured 2026-07-24 and the open B7 input is CLOSED benign** (full-panel 0.11% / H1 0.22% / H2 0.04%, all PASS); §4 stays undischarged. ⚠ The 69/11 `LEG_MAP` split binds **no deployed geometry** today and is **retained-not-released** under S1 (headroom not freed) — do not quote it as consuming live cap headroom for a third leg. | [`withdrawal ADR`](../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) · [`GO ADR §Addendum 2026-07-22`](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) + [`§Addendum 2026-07-24`](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) · [`RESULTS`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md) | **HIGH** (primary-sourced venue re-verify). |
| **N6** | **MNQ venue-edition facts (leg withdrawn from deployment 2026-08-04; findings below are venue-independent):** NAS100/MNQ Pine venue edition is JSON-only alerts (the 2026-07-21 B7 miss root cause was informational-alert shadowing — fixed + re-pinned in `core/strategies/PORT_MANIFEST.sha256`); WATCH-1 haircut realizes at the **account-multiplier layer**, not TV risk%-input scaling (Q-PYRPARITY-1 FALSIFIED-NONPROPORTIONAL — pyramid legs don't scale proportionally). | [`Q-PYRPARITY-1 closure`](../../docs/briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) | **HIGH**. |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator | Source |
|---|---|---|
| D5 intraday momentum (NQ/MNQ) | Stage-2 cost-law KILL (IS); OOS edge decayed negative (D5-RECOST-1) | [`RESULTS`](../../lab/archive/d5_recost_2026-07/RESULTS.md), 2026-07-16 / 2026-07-21 |
| OPENPRESS-1 opening-volume × efficiency | MNQ HAC t underpowered; no rescue | [`closure`](../../docs/briefs/closures/OPENPRESS-1-closure-falsified.md), 2026-07-21 |
| ORB-MNQ composed into the c1 book | Variance dominance (Q-COMPOSE-1 §6 row-2, every tier) | [`closure`](../../docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md), 2026-07-17 |

## ACTIVE / OPEN

- **ORB-MNQ-1: lifecycle `CANDIDATE @ 1.00×`, PARKED** (unparked 2026-07-31 → re-PARKED 2026-08-03); payable-standalone-Tradeify-leg target **FALSIFIED** (§4 T2 FIRED), scoped to one target at one firm — lifecycle not demoted, K not spent, mechanism not rejected. Manifest `orb_mnq_intraday_breakout` **closed 2026-08-04** (`operator-stopped`, `executed_k=0`) — no open-manifest obligation. See [`MNQ.md`](MNQ.md).
- None other open on this parent — c1 / rail / execution-quality obligations are not instrument-ledger ACTIVE rows (see session log 2026-08-06).

## SESSION LOG

- **2026-08-26** — **Mirror-sync gap closed (pointer):** MSL Board B8 released MYM/MNQ headroom for
  new non-Striker research ([`ADR`](../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)),
  2026-08-12 — [`YM.md`](YM.md)'s mirror row Y4 got this pointer the same day; N7 below did not.
  Canonical detail on [`MNQ.md`](MNQ.md). N7's "retained-not-released / headroom not freed" line is
  historical for that 2026-08-06 claim-alignment pass.
- **2026-08-06** — **Claim-alignment M21/C10:** Status rewritten to withdrawal + Rule-10 delegate to [`MNQ.md`](MNQ.md) (no restatement of deployment mechanics). ACTIVE/OPEN: deleted B7-REFIRE row (rail obligation, unreachable) and execution-quality row (SUSPENDED — no data source; W3 is not the binding obstacle) — both recorded here, not in ACTIVE. ORB row updated to re-PARK + target FALSIFIED + manifest closed. N1: struck "The live account is Tradeify"; no basis privileged (four friendly-firm bases; BluSky-NT $0.95 is NT-schedule proxy per M40). N7: voided "binds … order geometry" / live 11/69 reservation reading. N6 retitled only (account-multiplier layer retained). No `core/`, lock, allocation, lifecycle, Pine, rail, or `LEG_MAP` change.
- **2026-07-24** — Ledger created (operator ruling #6, Algorithm repo review). Seeded W1–W3 + N1–N6 from the ORB-MNQ admission, D5/D5-RECOST, OPENPRESS-1, Q-COMPOSE-1, Q-PYRPARITY-1, and the rail-build record. No core/lock/allocation/dd_protection change.
