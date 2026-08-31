# INSTRUMENT LEDGER — GER40

**Symbol:** GER40 (DAX 40 index CFD; aka GER30 / DE40 / DAX) · **Tradable:** FXIFY / DXTrade · **Asset class:** equity index (EUR-denominated)
**Canonical feed:** (historical — Pepperstone retired 2026-08-02; see [feed retirement ADR](../../docs/adr/2026-08-02-pepperstone-feed-retirement.md)) TV CSV export — **Pepperstone / GER40** (operator-supplied panel `BAR_EXPORT_v0.1_PEPPERSTONE_GER40_2026-06-22_37fa8.csv`, 131,504 15m bars 2020-2026, Step-0 PASS; EUR-denominated → `Price EUR` column; epoch UTC → convert to **Europe/Berlin** for the 09:00 CET cash open; bytes deleted from checkout, offline-copy-only per the ADR).
**DXTrade contractValue:** **UNVERIFIED** (EUR/index-point) — broker-verify before any sizing (the DJ30 default-1 = ~7%-risk class of bug). Not in `firm_rules.py`.
**Status:** **Research / concept-stage — not allocated, no live strategy.** First R&D = the 2026-06-22 ORB study.
**Last updated:** 2026-06-22

**Purpose:** Single source of instrument-level truth (operational rule 10). Any session deriving/testing on GER40 MUST read this at session start and append a dated disposition. **Created 2026-06-22** (ORB cross-instrument study; operator supplied the panel mid-session as the synthesis's #1 acquisition — DAX is the *only* FXIFY instrument with a genuine discrete cash open that closes overnight).

## PROFILE (machine-readable)

```yaml
symbol: GER40
asset_class: equity-index
family: []
venue_tradable: false
venue_note: "FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present."
k_bank_source: "../../discovery_manifests/"
cells:
  - mechanism: opening-range-breakout
    verdict: AMBIGUOUS-PARKED
    date: 2026-06-22
    source: "#G2"
structure:
  - claim: "GER40's genuine discrete cash open (the literature's most-discriminating ORB trait) did NOT make it the best ORB instrument — ORB tradeability is dominated by opening-range/spread ratio, not by discreteness of the open (NAS100, a 23h feed, beats DAX)."
    source: "#G2"
```

---

## DURABLE FINDINGS

| # | Finding | Evidence | Confidence |
|---|---|---|---|
| **G1** | **GER40 has a genuine discrete cash open** (Xetra 09:00 CET; the CFD feed shows real overnight gaps, unlike the 23h US-index feeds). It is the **only** FXIFY instrument satisfying the literature's most-discriminating ORB trait — yet **empirically it is NOT the best ORB instrument.** | ORB study 2026-06-22 ([`lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md`](../../lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md)) | **HIGH**. |
| **G2** | **GER40 ORB-30 FAILS the within-day placebo (p=0.126)** — the opening range is *not* significantly special vs arbitrary intraday windows — and the edge is **regime-concentrated** (meanR +0.060 / t 1.63 but 2022 alone +0.331; 2020/2023/2026 negative; halves +0.113/+0.007; short side weak +0.028). Good fill-cliff headroom (slip-to-zero 2.67× spread) but the discrete-open advantage did **not** translate into a robust signal. **Decisive lesson: ORB tradeability is dominated by opening-range/spread ratio, not by discreteness of the open** (NAS100, a 23h feed, beats DAX). | ORB study 2026-06-22 | **HIGH** (n=1646, canonical Pepperstone 2020-2026). |

## ACTIVE / OPEN

- **ORB on GER40 — deprioritized.** Best-by-spec but placebo-fail + regime-fragile (G2). Not the ORB answer (NAS100 is — see [`NAS100.md`](NAS100.md) N1). The operator-supplied 2020-2026 panel is retained for other European-session work. No anti-SNAG slot consumed (characterization).

## SESSION LOG

- **2026-06-22** — Ledger created. ORB cross-instrument study: GER40 is the only true-discrete-open FXIFY CFD but its ORB-30 fails the placebo (G2) → deprioritized for ORB. No core/lock/Pine change. See [`lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md`](../../lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md) + [`docs/SESSIONS.md`](../../docs/SESSIONS.md).
