# External-strategy sourcing — Triage (§2.3, auditable funnel)

**Date:** 2026-06-30. **Input:** [catalog.md](catalog.md) (65 CONFIRMED + 4 MISREPRESENTED rows, ~12 distinct mechanism clusters).
**Locks:** [PREREGISTRATION-0.5-locks.md](PREREGISTRATION-0.5-locks.md). **Cull order (CC-HANDOFF §2.3):** dedup → codifiability → cost-law → era/vol-orthogonality. Plus the two structural edits: **Edit-1** (publication-date OOS gate → documented post-pub decay is disqualifying weight) and **Edit-2** (a returns-INDEPENDENT, probe-checkable side-prediction is mandatory; a side-prediction that reduces to the strategy's own returns → `CULLED_AT_INTAKE`).

## The three pre-existing walls (every cluster is scored against these)

The locked book = **long-gold-trend (Guardian)** + **long-index-momentum (Striker DJ30+NAS100)** + **USDJPY-MR (Aegis)**. Its canonical risk is the **2020–2023 (H1) chop / follow-through-deficit** regime (decompound HOLD, `docs/adr/2026-06-07-decompound-remc-hold.md`). A useful 5th leg must **pay in chop AND decorrelate from the book in H1**. Three walls have killed every prior chop-native search (memory: chop-native-leg sweep 0/8, EURGBP/USDCAD Aegis-MR ports, USOIL spike-fader, NOCT-SPX, GEX/T10Y3M/Friday gates):

1. **Cost-law** — cost-in-R ∝ price/stop_distance; a tight-stop intraday MR/fade pays a crippling round-trip hurdle (USDCAD measured **0.097R** @1.42×ATR; target ≥4× hurdle). Kills tight-stop 15m fades pre-build.
2. **H1 tail co-occurrence** — a **long-biased dip-buy MR** buys dips that extend into the 2022-style one-directional move, bleeding *exactly when the book co-draws* (Aegis/USDJPY 2022 PF ~1.12; EURGBP 2022 sterling crisis; chop-native sweep K1). A leg that escapes this must be **market-neutral** or **vol-amplified** (pays MORE in chop), not net-long.
3. **Single-account non-codifiability** — multi-leg (cross-sectional / pairs / spread / carry) cannot be auto-composed by the 4-family codifier (`bb_reversion_long` long-only, `ema_crossover_long`, `ema_recovery_long`, `donchian_breakout`). → **Lane B** (mechanism-probe only), stops at the mechanism verdict with `CODIFIER_GAP` flagged (a spread primitive is a separate future ADR — CC-HANDOFF §1).

**Graveyard dedup keys** (`docs/rejected_candidates.md`, key = mechanism_family × instrument): mean-reversion-spike-fade×USOIL, fx-fixing-reversal×EURUSD, bollinger-band-MR×EURGBP, dealer-gamma/term-spread/day-of-week gates×NAS100, rates-intraday-MR×MICRO10Y, index-dispersion×SPX500, commodity-carry-term-structure×USOIL (harness F1-FALSIFIED), inventory-reversal-immediacy (NOCT)×SPX500 (harness FALSIFIED).

---

## Disposition by cluster

### A. Short-period oscillator / close-location MR — Connors RSI(2), cumulative-RSI, ConnorsRSI, Williams %R, dynamic-RSI, IBS, Bhatti FX z-score (rows 0–4,8–11,22–27,57,67)
- **Codifiability:** the codifier has **no RSI/oscillator entry primitive** → not Lane A. Non-codifiable → Lane B at best.
- **Edit-2:** the "mechanism" is short-horizon overreaction reversal; the side-prediction reduces to "forward return is monotone in the oscillator value" = **the edge restated** → returns-DEPENDENT → `CULLED_AT_INTAKE`. (StatOasis's ATR-contraction "side-prediction" is *tautological* — the filter defines the entries; verifier flagged it.)
- **Edit-1 decay:** Connors RSI(2) post-2014 decay **disclosed in-source**; d=2008 → the OOS window is the decayed window.
- **H1 + correlation:** long-only index dip-buy → bleeds in H1; on DJ30/NAS100/SPX500 = the book's own index legs → **correlated, not decorrelated**.
- **Disposition: DROP** the cluster (returns-dependent side-pred + documented decay + H1 dip-buy bleed + index-correlated). **Single exception kept for Lane B:** **IBS / close-location** [22,27] — the *only* row with a demonstrated **returns-independent** side-prediction (close-location bucket → next-bar return monotonicity is a price-only property). Routed to Lane-B shortlist **flagged low-priority** (index-correlated + H1 dip-buy → likely portfolio-gate fail, but the side-prediction is genuinely independent so it is testable).

### B. Bollinger / z-score BAND fade — StatOasis Z, QC 1-stdev, Kevin Davey BB, ayusattv, Krishna-Peri BB+RSI, %b (rows 0,1,5,6,7,29,66,68)
- **This is the Aegis family.** Aegis/USDJPY (the book's existing leg) IS a BB19/1.9 long-only MR. A long-only band fade is the **same mechanism already in the book → correlated with Aegis, not decorrelating** → fails the thesis.
- **Dedup:** bollinger-band-MR×EURGBP is in the graveyard (cost-law); Aegis USDCAD v0.1 dead (n=245 PF 0.756).
- **Edit-2:** band-revert side-prediction = the edge → returns-dependent.
- **H1:** long-only dip-buy → H1 bleed.
- **Disposition: DROP.** The one *codifiable* (Lane-A) cluster is the one we least want — a 5th Aegis (correlated + dip-buy + already-rejected ports). Codifiability does not rescue a thesis-mismatch.

### C. Opening-range / gap / VWAP / pivot intraday fades — Option-Alpha ORB-MR, failed-ORB, NQ gap-fill, gap-fade, VWAP-band, Camarilla, Mind-the-Gap (rows 12,13,17,30,49,50,51,65)
- **Dedup:** ORB family heavily worked & dead (NAS100 ORB NO-GO/HOLD; GEX/T10Y3M/Friday gates rejected; US500 ORB-30 "not tradeable — fill cliff"). Index gap-fade = the NOCT overnight-drift family (harness FALSIFIED). Pivot/%b/gap-DOW rows are **MISREPRESENTED** (excluded).
- **Cost-law + fill-cliff:** tight intraday fades → cost wall; the US500 ORB-30 fill-cliff is the measured precedent.
- **Edit-2:** fade side-prediction = the edge → returns-dependent.
- **Disposition: DROP** (dedup vs ORB/NOCT graveyard + cost-law/fill-cliff + returns-dependent side-pred).

### D. Overnight / intraday short-term reversal — Tug-of-War (Lou-Polk-Skouras), **Della Corte-Kosowski (VIX-amplified, multi-asset)**, Cooper-Cliff-Gulen, multi-asset overnight reversal, Brogaard intraday-residual, correlated cross-asset stress reversal (rows 15,16,18,20,36,37,48,53,62)
- **Edit-2 (genuine fit):** the **VIX / overnight-illiquidity amplification** (Della Corte-Kosowski) is a **returns-INDEPENDENT** side-prediction — reversal magnitude scales with VIX/closure-illiquidity, checkable on market data, not the strategy's P&L. The catalog's cleanest Edit-2 + thesis fit.
- **Thesis fit:** a reversal that **amplifies in high-vol/chop** could pay MORE in H1 → potentially **anti-correlated** with the book (escapes Wall 2 by vol-amplification rather than market-neutrality).
- **Walls/priors:** the single-instrument time-series version (fade the overnight move) is **Lane B** (session-timing overlay, not in the codifier); the cross-sectional version is multi-leg. **NOCT-SPX already FALSIFIED** a related overnight-reversal-on-index ("reduces to dead overnight drift") → real negative prior; heavily-mined decay risk (Edit-1).
- **Disposition: Lane-B shortlist (strong).** Probe Della Corte-Kosowski's VIX-amplified market-closure reversal — test the returns-independent VIX/illiquidity side-prediction on the book's instruments, windowed post-d, + the decorrelation. Carry the NOCT prior explicitly.

### E. Carry / term-structure / roll-yield — commodity carry, theory-of-storage, FX carry, cross-asset carry (rows 31–34,61)
- **Dedup:** commodity-carry-term-structure×USOIL **already harness-FALSIFIED** (F1: curve-state didn't separate; disguised long-oil trend).
- **Wall 2 (decisive):** carry is **short-vol — it crashes in risk-off** (2008/2020 carry unwind) → its tail **co-occurs with the book's H1 risk-off** = the textbook co-drawdown. Fails regime-robustness a priori.
- **Wall 3:** FX/cross-asset carry are cross-sectional → multi-leg → non-codifiable.
- **Disposition: DROP** (dedup + carry-crash H1 co-occurrence + single-account).

### F. Market-NEUTRAL spread / ratio reversion — GGR pairs, Fil, WTI/Brent spread, HMM-crude, **gold/silver ratio**, Kalman-ML gold/silver (rows 42–47)
- **Wall 2 ESCAPE (the key one):** a **market-neutral** spread/ratio MR carries **no directional beta** → does **not** co-draw with the book in H1 risk-off (the spread can be stable while both legs fall). This is the **one cluster that escapes the wall that killed every prior long-biased chop search.**
- **Edit-2 (genuine fit):** **cointegration / stationarity / half-life of the spread** is a **price-only, returns-independent** side-prediction.
- **Wall 3:** two-leg → non-codifiable in the 4-family codifier → **Lane B**, stops at mechanism verdict, `CODIFIER_GAP` flagged (spread primitive = future ADR).
- **Dedup nuance:** gold/silver-ratio touches **XAGUSD** (Guardian-on-XAGUSD *trend* is rejected, SNAG) but **relative-value ratio-MR is a different mechanism** → clears the "new mechanism evidence" bar (Q-CORR-1 explicitly leaves silver open at the standard intake bar). WTI/Brent touches USOIL (spike-fader/carry dead) but cointegration-spread is again a different mechanism.
- **Cost:** daily wide-band spread MR is low-turnover (dodges Wall 1) but pays **two** round-trips — needs a cost check at probe.
- **Disposition: Lane-B shortlist (strongest structural fit).** Advance the cleanest single one (**gold/silver ratio cointegration MR** [46]; WTI/Brent [44] as alternate). **DROP** the HMM/Kalman-ML variants [45,47] — added regime-switching/ML = overfitting-suspect + non-codifiable + complexity with no codifier path.

### G. Calendar / seasonality — turn-of-month, FOMC-cycle even-week, pre-FOMC drift, Sell-in-May, gold Sep/Nov (rows 38–41,58,59,63)
- **Edit-2:** cleanest possible (the side-prediction is a **calendar date** — fully returns-independent). BUT:
- **Thesis-mismatch:** these are **directional-timing overlays** (net-long index/gold in a window), **not chop-paying mechanisms** — they don't fill the chop/follow-through gap and they're **index/gold-correlated** with the book + H1 co-draw if the window lands in a selloff.
- **Edit-1 decay:** turn-of-month / Sell-in-May / pre-FOMC heavily mined & decayed; **gold Sep/Nov explicitly FAILS Hansen SPA** in its own source (data-snooping).
- **Disposition: DROP** (thesis-mismatch + index/gold-correlated + documented decay; gold-seasonal fails its own SPA test).

### H. Cross-sectional reversal — Wang-Yu volume-weekly, Jegadeesh/Lehmann, G6 currency MR, **gold abnormal-day contrarian** (rows 52,53,55,56,60,54)
- **Wall 3:** cross-sectional basket → multi-leg → non-codifiable single-account → DROP the basket forms.
- **Single exception:** **gold abnormal-day contrarian (Caporale-Plastun)** [54] — single-instrument **XAUUSD**, event-conditioned (abnormal-return day = a price-only trigger, returns-independent), the *only XAUUSD-native reversal* evidence, and it would **decorrelate from Guardian by regime** (Guardian rides trends; the contrarian fades spikes). **Marginal Lane B** — flagged: daily (not 15m), and "naive RSI MR fails on gold (trending)" is a contrary signal.
- **Disposition: DROP** the cross-sectional; **gold abnormal-day contrarian → Lane-B shortlist (marginal).**

### I. Volatility-contraction — NR7 time-exit, BB-in-Keltner squeeze (rows 21,25)
- BB-in-Keltner squeeze [25] is documented **in-source as a NEGATIVE/calibration result** (naive entry fails). NR7 is a vol-timing overlay (vol-contraction = a vol-proxy — the same GEX/T10Y3M death mode), not a directional chop-leg, non-codifiable.
- **Disposition: DROP.**

### J. Trend-fade practitioner — Kaufman Fade-The-Trend (row 64)
- Trend-fade = dip-buy → Wall 2 (H1 bleed) + cost-law + no returns-independent side-pred. **DROP.**

---

## Funnel

| Stage | Count |
|---|---|
| Harvested (verified rows) | 69 |
| Source-CONFIRMED | 65 |
| MISREPRESENTED (excluded) | 4 |
| Distinct mechanism clusters | ~12 |
| **DROP at triage** | clusters A(bulk), B, C, E, G, H(bulk), I, J |
| **Lane-A survivors** | **0** (the only codifiable cluster, B, is a thesis-mismatched 5th-Aegis) |
| **Lane-B shortlist (proposed for intake)** | **≤4** — see below |

## Lane-B shortlist proposed for §2.4 intake + §2.5 freeze (Joshua's call)

Ranked by how cleanly they escape the three walls + carry a returns-independent side-prediction:

1. **Gold/Silver ratio cointegration MR** (F) — **STRONGEST.** Market-neutral → escapes H1 co-draw (the wall that killed every prior search); returns-independent side-prediction = ratio cointegration/half-life; "new mechanism evidence" on silver. Two-leg → `CODIFIER_GAP` (stops at mechanism verdict). Cost: two round-trips, check at probe.
2. **VIX-amplified market-closure short-term reversal — Della Corte-Kosowski** (D) — vol-amplified (pays more in chop → potentially anti-correlated in H1); returns-independent VIX/illiquidity side-prediction; multi-asset incl. book instruments. Carries the **NOCT-SPX falsified prior** + decay risk.
3. **Gold abnormal-day contrarian — Caporale-Plastun** (H) — *marginal.* Single-instrument XAUUSD, returns-independent event trigger, decorrelates from Guardian by regime. Flags: daily-not-15m; gold-MR-fails-in-trend contrary signal.
4. **IBS close-location MR** (A) — *marginal.* The only demonstrated returns-independent side-prediction in the oscillator cluster; but index-correlated + H1 dip-buy → likely portfolio-gate fail.

**Honest read:** the catalog surfaced **no Lane-A codifiable survivor** and **no candidate that cleanly escapes all three walls** — the two structurally-strongest (spread-MR, VIX-reversal) escape Wall 2 only by being market-neutral / vol-amplified, and both are **Lane-B mechanism-probes that stop at a verdict** (non-codifiable). This is consistent with the program's prior-exhausted chop-native search and the brief's expected low-to-near-zero saved-candidate outcome. The value of advancing 1–2 of these is a **cheap, returns-independent mechanism probe** (Edit-2) on a genuinely-decorrelating mechanism the internal searches did not cover (market-neutral relative-value, vol-amplified reversal).
