# `MNQSR-1` — Phase-1 bars-only intraday S/R structure screen (MNQ)

**Status:** `FROZEN` — register K before any score; run is bars-only on the
authorized 1m OHLCV cache. **Date:** 2026-08-06.
**Instrument:** native `MNQ.v.0` continuous 1m OHLCV.
**K_intrinsic = 14** — 7 families × 2 limbs (attraction, reaction). Within-family
secondary levels are descriptive under BH-FDR only; they do not expand primary K.
**Lane:** blind Notice-phase structure screen (not harvest / not mechanism-first).

---

## §0 — Priors (disclose; do not retune)

| Prior | Disposition in this cell |
|---|---|
| US500 VWAP reversion anti-edge (`lab/analysis/legacy/us500_discovery_2026-06-22`) | Re-test on MNQ under this construct; do not drop VWAP a priori |
| Harvest triage DROP of Camarilla / VWAP-band fades (`lab/archive/external_sourcing_2026-06-30/triage.md`) | Same — structure screen, not fade-strategy re-proposal |
| MNQPROX-1 VOID-TOD-CONFOUND on PDH/PDL as *book* control | Different endpoint; reaction limb **requires** ToD-matched null |

---

## §1 — Question

Which Phase-1 level families show MNQ **path dependence (attraction)** and/or
**post-touch respect (reaction)** beyond pre-registered nulls?

Two limbs are never blended into one score.

---

## §2 — Frozen construct

| # | Element | Frozen value |
|---|---|---|
| S1 | Data | `MNQ.v.0` continuous `ohlcv-1m`; default window **2025-08-06 → 2026-08-04** (MNQPROX cache). Widen only after estimate + operator GO |
| S2 | Session hybrid | **RTH** = 09:30–16:00 ET (`orb_lib.OPEN_TOD_US` / session end). **Prior RTH** H/L for PDH/PDL. **Overnight** = 18:00 ET prior → 09:29 ET. Evaluation = RTH only |
| S3 | Families | `prior_rth`, `overnight`, `std_pivot`, `fib_pivot`, `camarilla`, `atr`, `vwap` |
| S4 | Primary levels | prior_rth: PDH+PDL; overnight: ONH+ONL; std/fib: R1+S1; camarilla: R3+S3; atr: open±1.0·ATR₁₄; vwap: ±2σ band |
| S5 | Touch | First 1m bar i≥1 where \|mid−level\| ≤ **1 tick (0.25)** and prior bar was strictly farther (MNQPROX rule). Mid = (H+L)/2 |
| S6 | Attraction | Per level-day: hit before 15:45 ET; time-to-touch if hit. **Decision null = distance-matched mirror** about RTH open. Report calendar-day distance shuffle as descriptive. VWAP attraction: day hits \|z\|≥2; null = within-day return-shuffle path |
| S7 | Reaction | At first touch; primary horizon **H=15m** (5/30/60 descriptive). Respect = signed move toward session interior / toward VWAP for band. **Decision null = ToD-matched** random mid within ±5 min same session |
| S8 | Inference | Session-block bootstrap 10,000 reps, seed **20260806**. BH-FDR across **K=14** primary cells at α=0.05 |
| S9 | Power | VOID-POWER attraction if n_RTH_sessions < 30; reaction if n_primary_touches < 50 |

**Secondary levels (descriptive only):** PP/R2/S2; Camarilla R1/R2/S1/S2; ATR ±0.5; VWAP ±1σ and VWAP midline.

---

## §3 — Forbidden moves

- **FM-1** Threshold / formula / horizon / tick-tolerance sweeps after data.
- **FM-2** Join ORB outcomes, strategy PnL, or any win/loss table.
- **FM-3** Promote a PASS to a trade entry without a fresh Inquire brief + validation gate.
- **FM-4** MBP/MBO / volume-profile / candle confirmation inside this freeze.
- **FM-5** Redefine overnight vs RTH after seeing results.
- **FM-6** Drop families a priori because of US500 / harvest priors.
- **FM-7** Re-declare K after scores (`register_search open` is immutable).

---

## §4 — Outputs (closed list)

- Coverage ledger (sessions, touches per family)
- Per-family attraction Δ_hit vs mirror (or VWAP shuffle), bootstrap CI, p
- Per-family reaction Δ_respect @15m vs ToD null, bootstrap CI, p
- BH-FDR table over 14 primary p-values
- ToD diagnostics (median/IQR of touch times)
- Phase-2 gate line: which families (if any) license candle (B) or VP/L2 (C)

## §5 — Amendment log

| Date | Change |
|---|---|
| 2026-08-06 | Reaction ToD-null RNG uses deterministic `_FAMILY_SEED` offsets — never `hash(family)` (`PYTHONHASHSEED` made early draws non-reproducible). Same null class; re-scored once for RESULTS pin. |
| 2026-08-06 | **Disclosure (not a retune):** session VWAP expanding-σ makes \|z\|≥2 nearly immediate on many days (ToD cluster ~09:34). Attraction null also hits → Δ≈0. A min-bars-before-z gate would be a **new** cell, not this freeze. |
