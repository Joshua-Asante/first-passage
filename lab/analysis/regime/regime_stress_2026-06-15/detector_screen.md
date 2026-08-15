# Detector-separation screen (participation-gate precondition)

**LoR:** OUTER (INQHIORI). Cheapest precondition for the participation-gate Phase 1. Research artifact;
locked config untouched. 2026-06-15. **Verdict: PARTIAL PASS — gold-carried, leg-specific (`DONE_WITH_CONCERNS`).**

**Question.** Does a causal, trailing-window trend-persistence detector (KER / multi-month TSMOM-return /
variance-ratio), computed daily on the price series, *separate* the hostile (chop, pre-2023-03-21) from
the benign (trend, post) regime? Necessary condition for any deploy-vs-wait gate. Data: OANDA M15→daily,
2020-2026 (staging feed). One-sided falsifier (pre-registered): separates if AUC ≥ 0.70.

## Results (AUC = P[detector higher on benign date]; >0.70 separates)

| instrument | KER_63 | KER_126 | TSMOM_126 | TSMOM_252 | VR2 | VR5 |
|---|---:|---:|---:|---:|---:|---:|
| **Guardian / XAUUSD** | 0.580 | **0.752** | **0.821** | **0.939** | 0.460 | 0.360 |
| DJ30 / US30USD | 0.529 | 0.499 | 0.517 | 0.578 | 0.580 | 0.523 |
| NAS100 | 0.557 | 0.561 | 0.606 | 0.615 | 0.487 | 0.574 |
| Aegis / USDJPY | 0.533 | **0.415** | 0.472 | **0.338** | 0.489 | 0.492 |
| **combined equity/gold mean KER_126** | | **0.678** | | | | |

## The honest read — not a clean pass

**Only GOLD separates.** Guardian/XAUUSD trend-persistence cleanly distinguishes the regimes (KER_126
0.75, TSMOM_126/252 0.82/0.94 — gold genuinely trended far less in 2020-2022 than 2023-2026). But:

- **The two equity Strikers do NOT separate** (DJ30 ~0.50, NAS100 ~0.56–0.62), and the brief's recommended
  **combined equity/gold signal is 0.678 — below the 0.70 bar.** The separation is **gold-carried**, not broad.
- **This is mechanistically correct, and it relocates the regime.** Equities *trended* in 2020-2021
  (post-COVID rally); their chop was mostly 2022. So the portfolio "hostile" calendar half (2020 → 2023-03)
  is **not an equity-chop phenomenon** — it's a **gold-chop + USDJPY-carry-trend** phenomenon. Gold was the
  chopping leg; the daily equity detectors correctly show no clean split at this boundary.
- **USDJPY is INVERTED** (KER_126 0.415, TSMOM_252 0.338 — *higher* persistence in the hostile half).
  This empirically **confirms the brief's Aegis insight**: 2020-2022 USDJPY was a powerful carry *trend*,
  and the mean-reverter was run over. Aegis's regime is the *opposite sign* — a portfolio-average label is wrong.
- **VR non-separating across the board** (and its levels look mis-scaled — but it didn't separate either way, so it's out regardless).

## Verdict — PARTIAL PASS, and it narrows the direction

The **necessary condition is met by one leg**: gold trend-persistence describes the portfolio's hostile
regime (AUC up to 0.94). The direction is **not dead**, but it is far narrower than a portfolio-wide gate:

- **Supported:** a **gold-trend-persistence deploy/wait gate** (equivalently, a Guardian down-weight) — and
  Guardian is the #1 hostile bust driver, so this targets the biggest contributor with a detectable signal.
- **Not supported by this screen:** an equity-Striker gate (their bust regime isn't visible in daily
  trend-persistence) and a portfolio-average label (USDJPY runs the opposite way). Aegis would need a
  *USDJPY-trend* detector (inverted sign), not a chop detector.

## Concerns (why "PASS" is weak)

1. **n=2 regime blocks.** AUC here measures "is the detector level different between 2020-22 and 2023-26."
   With one hostile and one benign block, *any* slow variable separates — TSMOM_252's 0.94 is largely
   "gold rallied 2023-2026," which is the momentum signal itself, nearly tautological. **High AUC is weak
   evidence; only the failures (equities, USDJPY) are informative.**
2. **Descriptive, not predictive.** The screen tests whether the detector *describes* the regime (trailing
   window overlaps it). Whether it *predicts* the forward pass window is the Dacco-Satchell question the
   brief flags as likely-to-fail-OOS — unresolved here.
3. **Gold-only gate is blind to a different next regime.** If the next hostile regime is equity-chop-driven
   (not gold), a gold detector misses it — the n=1 fragility the brief warns about, now concrete.
4. **Staging feed** (OANDA bars) — fine for a regime screen, not a lock candidate.

## Recommendation

Proceed to Phase 1 **only as a gold-anchored gate** (gold trend-persistence → portfolio deploy/wait, or
Guardian-specific down-weight), with the Aegis/USDJPY leg handled by an inverted (trend-detection) signal,
and the Strikers left ungated pending a different (intraday/breakout-reversal) signal — daily
trend-persistence is the wrong scale for their pyramid tail. The **forward live-PnL tripwire remains the
real gate**; this screen only establishes that a single mechanism-aligned signal (gold efficiency) clears
the necessary descriptive bar, and that the regime is leg-specific exactly as the brief argued.

**Artifacts (gitignored):** `reports/regime_stress/detector_screen.py` + `detector_screen.json`.
