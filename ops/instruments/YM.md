# INSTRUMENT LEDGER — YM

**Symbol:** CME E-mini Dow ($5) futures (YM; Globex, Databento dataset `GLBX.MDP3`) · **Micro sibling:** MYM ($0.50/pt) · **Asset class:** equity index futures
**Status:** **Research/discovery venue only for YM itself.** Micro-sibling deployment status is owned by [`MYM.md`](MYM.md) — this parent does **not** restate it (Rule 10). Locked-book futures-prop transfer remains NO-GO ([`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](../../docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md)); the DJ30→MYM transfer prototype is **FALSIFIED** (Y3). The cash-index sibling hosts the locked Striker DJ30 strategy — parked **NO-MECH** per Q-MECH-1 to the 2026-08-08 review; nothing in this ledger touches it.
**Last updated:** 2026-08-06

**Purpose:** single source of instrument-level truth (operational rule 10, [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Any session deriving/testing/adjudicating on YM MUST read this at session start and append a dated disposition. **Created 2026-07-12** — Q-HARV-0's Phase-0 Rule-0 read found the card ABSENT ([`PHASE0_REPORT.md §0.8`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/PHASE0_REPORT.md)). Distinct instrument from any DJ30 CFD surface (closed FXIFY venue) — findings do not transfer automatically in either direction. Live MYM c1 facts live on [`MYM.md`](MYM.md); this parent card carries the shared venue-geometry pin (Y4) so the NQ↔YM mirror stays complete.

## PROFILE (machine-readable)

```yaml
symbol: YM
asset_class: equity-index-futures
family: []
venue_tradable: true
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: venue-transfer
    verdict: DEAD
    date: 2026-07-09
    source: "../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md"
bars:
  - id: index-intraday-ohlcv-directional-timing-2026-07-21
    source: "../../docs/rejected_candidates.md"
```

---

## STANDING WARNINGS (read first — bind any GLBX/Databento window work)

- **W1 — `.c.0` continuous is calendar-roll, front-month, UNADJUSTED.** Same feed rule as ES ([`ES.md`](ES.md) W1, where the decisive +1.35%/+69.5pt ESH4→ESM4 phantom jump was measured). YM rolls **quarterly, mid-month** (3rd-Fri expiry: Mar/Jun/Sep/Dec) exactly like ES/ZN — any YM return window spanning a roll date carries a phantom calendar-spread jump; month-end windows (e.g. close(T-3)→close(T-1)) are roll-clean, month-spanning lookbacks are NOT for quarter-end months.
- **W2 — Databento `ohlcv-1d` buckets by UTC calendar day → phantom Sunday bars.** Feed-general (measured on the shared GLBX panel loader): the Sunday-evening Globex reopen lands in a thin Sunday-settle-date bar that shifts every month-end T-k offset. **Drop settle-date weekday > 4 before any trade-date offset work.** Close print ≈19–20:00 ET UTC-bar close, not the 16:00 ET equity settle. See [`ES.md`](ES.md) W2 / [`NOTES.md`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/NOTES.md).

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **Y1** | **GLBX `.c.0` roll rule + UTC-day bucketing (W1/W2) apply to YM/MYM unchanged.** The HARV-0 panel loader's weekend-bar drop and roll-aware window discipline were applied to the YM leg identically to ES; the roll-jump magnitude was measured on ES, the geometry (quarterly mid-month, unadjusted front-month) is contract-structural for YM too. | [`NOTES.md`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/NOTES.md), 2026-07-12 | **HIGH** (structural; jump magnitude measured on the ES leg only). |
| **Y2** | **In HARV-2026-001, YM was a breadth check, not independent evidence.** The month-end rebalancing mechanism (balanced-fund/TDF stock↔bond flow) concentrates in the broad benchmark (ES); YM shares the driver and is correlated — it adds robustness, **not independent N**. No YM-specific edge claim is on file; the parent candidate closed **AMBIGUOUS 2026-07-12** (see [`ES.md`](ES.md) E3 for the numbers: +19.21bp perm p=0.0129 pooled, era-decaying, RTH-concentrated, −15.96bp next-month reversal). | [`docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md`](../../docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md) §"Why ES (not YM/NQ) as primary" | **HIGH** (design fact). |
| **Y3** | **Striker DJ30→MYM transfer prototype FALSIFIED (operator-accepted 2026-07-09):** OOS PF ratio **0.559 < 0.8×** on structural venue costs — the pre-registered R5 B2-edition successor that had kept DJ30 conditionally alive through the P2 edge-transfer gate. Its failure fired the R6 §4 falsifier → locked-book futures-prop NO-GO. **The transfer / reconstruction lane hosts no admitted strategy** (c1's MYM venue edition of locked Striker DJ30 is a separate live-ops path — see [`MYM.md`](MYM.md)); re-proposal of a DJ30-family *transfer* onto YM/MYM requires new mechanism evidence, not re-tuned costs/params. | [`lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md`](../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md) + [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](../../docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md) | **HIGH**. |
| **Y4** | **Venue-fact correction 2026-07-22 binds the MYM leg's order geometry.** Tradeify's contract cap is **account-aggregate, not per-leg** — allocated **MYM 69** (MNQ 11) instead of each leg assuming the full 80 (the prior read was 1.91× the real limit); **flat deadline 16:45 ET**; **US Treasuries untradable** at this firm; the hedging rule (MYM+MNQ share the Equity Index Product Group) **clears by construction** because c1 is long-only at Pine, rail, and realized layers. Same pass **withdrew the prop-portfolio §4 discharge** (eval rows had modeled a drawdown lock neither Tradeify nor MFFU applies in eval → both `trailing_locking` tiers flip Part A PASS→FAIL, zero clearers at the frozen gate's $100K band, 11-08 hard date unchanged), which flagged the c1 GO's WATCH-1 0.50× risk figures as unmeasured under corrected geometry. **Updated 2026-07-25:** those figures were **measured 2026-07-24 and the open B7 input is CLOSED benign** (full-panel 0.11% / H1 0.22% / H2 0.04%, all PASS); §4 stays undischarged. Mirror of [`NQ.md`](NQ.md) N7. ⚠ The 69/11 `LEG_MAP` split binds **no deployed geometry** today and is **retained-not-released** under S1 (headroom not freed) — do not quote it as consuming live cap headroom for a third leg. | [`withdrawal ADR`](../../docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) · [`GO ADR §Addendum 2026-07-22`](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) + [`§Addendum 2026-07-24`](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) · [`RESULTS`](../../lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/RESULTS.md) | **HIGH** (primary-sourced venue re-verify). |

## DEAD / REJECTED (instrument-specific)

| Rejection | Discriminator | Source |
|---|---|---|
| Striker DJ30 → MYM venue transfer | OOS PF ratio 0.559 < 0.8× on structural venue costs (R5 gate) | FALSIFIED, operator-accepted 2026-07-09 — [`lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md`](../../lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md) |

## ACTIVE / OPEN

- ~~c1 MYM leg (micro sibling) — live-but-disarmed~~ — **WITHDRAWN 2026-08-04**; record on [`MYM.md`](MYM.md). Contract-cap / flat / hedging / §4 geometry remains a dated venue-fact on **Y4** (not a live ACTIVE row).
- YM parent remains research-only: assembled GLBX daily panel (parents 2010-06→2026-07, micros MYM 2019-05→2026-07, via the HARV-0 [`assemble_panels.py`](../../lab/archive/harv_0_month_end_rebalance_es_2026-07/assemble_panels.py) infra) — reusable for a future breadth/robustness leg, subject to W1/W2. Any *primary* YM candidate needs its own pre-registered brief and its own mechanism case (Y2: YM was explicitly not the flow-concentration leg).

## SESSION LOG

- **2026-08-26** — **`LEG_MAP` cap_alloc RELEASED (0/0, was 69/11)** — operator ruling,
  [`2026-08-26-striker-legmap-cap-release.md`](../../docs/adr/2026-08-26-striker-legmap-cap-release.md).
  Separate, narrower dimension than the 2026-08-12 occupancy release below: this one is the
  code-level `cap_alloc` in `ops/c1_rail/c1_sizing_host_reference.py`, not research-symbol
  permission. Full 80-micro account cap now unclaimed for a future leg's own allocation; Y4's
  "retained-not-released (headroom not freed)" line below is now historical on **both** dimensions.
- **2026-08-12** — **Occupancy posture updated (pointer):** MSL Board B8 released MYM/MNQ headroom for new non-Striker research ([`ADR`](../../docs/adr/2026-08-12-msl-mym-occupancy-release.md)). Canonical detail on [`MYM.md`](MYM.md). The 2026-08-06 “retained-not-released / headroom not freed” line is historical for that claim-alignment pass.
- **2026-08-06** — **Claim-alignment M22:** deleted sibling-status restatement from Status (pointer to [`MYM.md`](MYM.md) only). Moved former ACTIVE c1 row to past tense / out of live ACTIVE. Y4 (+ mirrored N7 on [`NQ.md`](NQ.md)): appended **retained-not-released** (then under S1 — headroom not freed) — 69/11 must not be quoted as consuming live headroom. ⚠ Superseded for *new non-Striker research occupancy* by B8 2026-08-12 (above). No `core/`, lock, allocation, lifecycle, Pine, rail, or `LEG_MAP` change.
- **2026-07-25** — Closed the owed NQ↔YM mirror gap: added **Y4** (account-aggregate MYM 69 / MNQ 11, flat 16:45 ET, Treasuries untradable, hedging clears by construction, §4 undischarged, WATCH-1 0.50× B7 input CLOSED benign) matching [`NQ.md`](NQ.md) N7; pointed Status / ACTIVE / Y3 at [`MYM.md`](MYM.md) for the live c1 path. No `core/`, lock, allocation, `dd_protection`, or Pine change.
- **2026-07-12** — Ledger created (Q-HARV-0 Phase-0 §0.8 found YM.md ABSENT). Seeded W1/W2 + Y1–Y3 from the HARV-2026-001 study and the R5/R6 record. No core/lock/allocation/dd_protection change; no live strategy on this instrument.
