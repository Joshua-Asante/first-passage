# Notice — MNQ daily range-state persistence: strong raw effect, VOIDs under the frozen corrected battery

**Notice ID:** N-2026-08-29-mnq-daily-range-persistence
**Observed:** 2026-08-29
**Author:** Claude Code
**Source:** own MC/statistical computation this session (`daily-range-state-persistence` class, MECHANISMS.md), candidate 1 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `HELD until operator scope call` (no calendar date — see §5)
**Lives in:** `docs/notes/notice/N-2026-08-29-mnq-daily-range-persistence.md`

---

## §0 — Source anchor

- **Source:** [`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate1_range_persistence.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate1_range_persistence.py) → `candidate1_results.json`; consolidated in [`RESULTS.md`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/RESULTS.md) §Candidate 1.
- **Observed at:** 2026-08-29, this session, run against `core/data/bar_data/MNQ_M15.csv` (BAR EXPORT v0.2, n=141,541 bars).
- **K:** registered before any result was examined — [`discovery_manifests/mnq_dailygeom_notice_20260829.json`](../../../discovery_manifests/mnq_dailygeom_notice_20260829.json), `--lane blind`, K=5 (batch of all 5 candidates in this session), closed with p=1.0 for this cell (VOID; no valid p may be quoted, see §1).
- **Prior art consulted:** `python scripts/instrument_profiles.py cell MNQ daily-range-state-persistence` → `verdict: untested — no prior on this cell`, `BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21`. MECHANISMS.md's `daily-range-state-persistence` class (frozen corrected battery, GC/CL only) and `docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md` (frozen, reused verbatim as method).

---

## §1 — The observation

Session-aggregated (full trading-day, 18:00 ET cutover) Wilder's True Range on MNQ: a day whose TR sits in the trailing top quintile (P80 of the strictly-prior 60 valid days) is followed by an elevated next-day TR (above the P50 of the trailing-through-today 60 valid days) **68.67%** of the time (n_cond=332 of n_scored=1497), CI [0.608, 0.753], both halves >0.66. That is a materially higher raw conditional rate than either instrument this exact frozen pipeline has been run on before — GC 0.5299 (NULL under the battery) and CL 0.6282 (SIGNAL-GENERIC under the battery). Running the same frozen battery on MNQ (new leaf, X_code=3, no spec amendment) found: L1/L2/L3 presence limbs all PASS cleanly, but L4 (by-year floor) reads AMBIGUOUS (this panel only has 6 calendar years with n_cond≥20, one short of the frozen 7-year floor — 2020 is a partial year), and L5 (IAAFT attribution) hits diagnostic-gate FAIL at both iter=100 and iter=500 (byte-identical Spearman-ACF mismatch, med 0.0511 / p95 0.0707, both over the 0.04/0.07 tolerance), with the final escalation-ladder step (Schreiber end-matching trim, ≤2% of record) finding no improving offset. Per the spec's own §3 CASE V, this is a **VOID**: no p_upper/p_lower may be quoted, and the anti-rescue guard means this is not a null result to report either — it is an uncertified one.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** GC and CL, the only two instruments this frozen battery has ever scored, landed NULL and SIGNAL-GENERIC respectively, both well below 0.65 conditional rate. MNQ's raw number (0.6867) is the highest yet observed under this exact pipeline shape.
- **Delta:** the raw effect is large and clean on the presence limbs (L1/L2/L3 all pass with real margin) — but the correction machinery built specifically to stop a strong-looking-but-invalid presence read (the incident this battery exists to prevent) cannot currently issue a verdict on MNQ, for two independent, disclosed reasons (short panel for L4; ACF-tolerance mismatch for L5). This is exactly the situation the corrected battery was designed to catch: a naive read of L1–L3 alone would have called this SIGNAL.
- **Frequency check:** first time `daily-range-state-persistence` has been run on any index-futures instrument (Step-0 scoped it to the non-index GC/CL/MCL triad); first time the frozen battery has hit a diagnostic-gate VOID rather than resolving to NULL/SIGNAL-GENERIC/SIGNAL-EXCESS/AMBIGUOUS.

---

## §3 — Candidate mechanisms (informal)

- **A — genuine, stronger volatility clustering on MNQ than on GC/CL.** Equity index futures are known to cluster more sharply than commodities in some regimes (e.g. VIX-term-structure-linked vol regimes); a real 0.69 conditional rate would not be shocking on priors.
- **B — panel-length artifact, not an instrument difference.** GC/CL's train era was 2010–2019 (9–10 full years); MNQ's only available panel is 2020-07→2026-07 (6 years, one partial). A shorter, more autocorrelated-at-longer-lag panel is exactly the shape that would both inflate L1–L3 point estimates AND blow the L5 tolerance calibrated on a longer, more IAAFT-friendly commodity panel.
- **C — MNQ's TR series has different higher-order structure than IAAFT (linear-ACF-preserving) can represent** — e.g. real regime breaks, not just linear serial dependence — which is a structural fact about the instrument's own vol dynamics, independent of whether the persistence claim itself is true.
- **D — could be noise inflated by the short-panel/small-by-year-cell interaction** — n_cond as low as 6 for 2020 makes the whole by-year read fragile even before applying the n<20 exclusion rule.

---

## §4 — Routing decision

**HOLD.** Reason: the raw observation is real, large, and worth carrying forward, but the frozen battery — the only validated instrument for adjudicating this claim family — cannot currently certify it on this panel, for reasons (short span; ACF-tolerance mismatch) that are about the panel and the battery's calibration, not about whether MNQ's TR series persists. Forcing a GRADUATE off the uncorrected 0.6867 number would repeat exactly the mistake the corrected battery exists to prevent (see 2026-08-18 audit note on the retired block-shuffle placebo). DROP would discard a real, large, well-powered raw effect for no principled reason — nothing in this session's measurement says MNQ is null, only that it is uncertified.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** none — operator-triggered, not calendar-triggered (this is a methodology-scope call, not a wait-for-more-data call).
- **Trigger condition:** either (a) the MNQ panel is extended to ≥7 full calendar years (discharges L4 mechanically), or (b) a fresh surrogate class is designed and reviewed for this series (the frozen spec's own pre-named O5 remedy: ARFIMA/FGN or GARCH-fitted surrogates in place of IAAFT) and clears its own diagnostic gate on MNQ's TR series — either would let this cell re-run to a real verdict.
- **Drop trigger:** if a future re-run under either remedy above still lands NULL, this notice's "worth carrying forward" framing was wrong and the cell should close DEAD like GC.
- **Calendar entry:** none.

**Forbidden moves, this notice:**
- Quoting 0.6867, the CI, or "L1–L3 all PASS" as evidence of a real signal — the battery this claim family requires VOIDed before issuing any p-value; a presence-limb-only read is precisely the invalidated block-shuffle-era mistake.
- Treating this as a second AMBIGUOUS/NULL data point alongside GC/CL — it is neither; it is uncertified, a different status.
- Re-running the IAAFT battery with a hand-tuned tolerance to force a PASS — the 0.04/0.07 tolerance is frozen and calibrated on GC/CL; loosening it for MNQ specifically would be outcome-conditional test-hardening, the exact anti-pattern the spec's own anti-rescue guard exists to block.

---

## §10 — Audit hooks

```bash
# Reproduce the VOID (deterministic given the frozen seed block; ~1-2 min on this panel size)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate1_range_persistence.py
# Expected: PILOT gate=FAIL med=0.0511 p95=0.0707 at both iter=100 and iter=500 (byte-identical);
# Schreiber end-match trim search best_k=0; final line "VOID per spec CASE V".

# Confirm the profile consult that gates this cell
python scripts/instrument_profiles.py cell MNQ daily-range-state-persistence
# Expected: exit 1, BINDING BAR index-intraday-ohlcv-directional-timing-2026-07-21

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-29-mnq-daily-range-persistence" docs/briefs/Q-*.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-daily-range-persistence.md --type notice
```
