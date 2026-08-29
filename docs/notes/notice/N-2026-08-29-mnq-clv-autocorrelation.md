# Notice — MNQ M15 closing-location is weakly mean-reverting bar-to-bar (real but small; raised-bar route unresolved)

**Notice ID:** N-2026-08-29-mnq-clv-autocorrelation
**Observed:** 2026-08-29
**Author:** Claude Code
**Source:** own statistical computation this session, candidate 5 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `HELD until operator/D-S-A scope call` (no calendar date — see §5)
**Lives in:** `docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md`

---

## §0 — Source anchor

- **Source:** [`lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_autocorr.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_autocorr.py) → `candidate5_results.json`; consolidated in [`RESULTS.md`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/RESULTS.md) §Candidate 5.
- **Observed at:** 2026-08-29, this session, on the full continuous bar sequence of `core/data/bar_data/MNQ_M15.csv` (141,540 consecutive M15-to-M15 pairs, RTH+overnight, no session gating). Zero H==L degenerate bars confirmed in this panel (checked before computing CLV — the `lesson_bar_export_ohlc_degenerate_fine_tick` failure mode does not apply at M15 on this instrument).

---

## §1 — The observation

Close-location value CLV_t = (close_t − low_t)/(high_t − low_t) ∈ [0,1] shows a real, negative, precisely-estimated lag-1 rank autocorrelation: Spearman rho(CLV_t, CLV_{t+1}) = **−0.0301** (n=141,540). A block-shuffle null (block=96≈1 trading day, 2000 permutations — reorders contiguous day-blocks of the t+1 series, preserving each series' own within-block structure and marginal distribution, testing only whether the observed pairing carries more dependence than a block-reordered one) puts the band at [−0.0052, +0.0051] (mean −0.0001, sd 0.0026) — the real value sits far outside it, p_lower = 0.0005 (0 of 2000 permutations at or below observed). Both halves of the panel carry the same sign (H1 −0.0385, H2 −0.0219; some attenuation over time, no sign flip).

---

## §2 — Why it stands out (the N signal)

- **Baseline:** no prior test of this construct exists anywhere in MECHANISMS.md or MNQ.md. The nearest neighbors are explicitly different claims: Baltussen momentum (sign-of-return persistence, `intraday-momentum` class, ABSENT on MNQ per N5) and every level/breakout construct (keyed to a reference price, not to where-within-its-own-range a bar closed).
- **Delta:** the correlation is small in magnitude (rho≈−0.03, well under 0.1% of variance) but the statistical evidence for it being real (not noise) is strong — a well-powered sample (n=141k), a null that controls for within-block serial structure rather than a naive iid shuffle, and directional stability across both halves.
- **Frequency check:** first instance.

---

## §3 — Candidate mechanisms (informal)

- **A — microstructure mean-reversion in close location** (bid-ask-bounce-adjacent): a bar that closes strong near its own high plausibly gives back some of that strength into the next bar's opening print, a very short-horizon effect unrelated to any directional edge over a meaningful holding period.
- **B — partial retracement / profile-shape artifact of M15 aggregation itself** — 15 minutes may simply be long enough for an intrabar extreme to partially mean-revert before the bar closes, independent of anything happening bar-to-bar; the "autocorrelation" could be an artifact of how OHLC bars are constructed rather than a genuine two-bar relationship.
- **C — could be noise despite surviving the block-shuffle null** — the null controls for within-block dependence but the effect's small magnitude means even a modest unmodeled confound (e.g., residual ToD seasonality in typical close-location, since RTH-open/close bars may systematically close differently than mid-session bars) could still be contributing; not tested this session.

---

## §4 — Routing decision

**HOLD.** Reason: the finding is real and well-powered, but two things are unresolved and both matter more for this candidate than for the other four: (1) **the raised bar's admission-route status is genuinely unclear** — this is a bar-to-bar autocorrelation claim, not obviously within-instrument temporal *selectivity* (Route 1's opened lever, which is about choosing WHEN within a session to act, not about a claim that holds at every bar), not obviously a different modality (Route 2), and not yet measured against ORB-MNQ-1 net-of-cost (Route 3) — deciding which route (if any) covers it is explicitly a call for whoever freezes a G0 on it, not a call this session is positioned to make; and (2) **the magnitude is small enough that its practical/tradeable relevance is unproven** — rho≈−0.03 has not been converted into an economically meaningful statistic (e.g., an expected-R read conditioned on extreme CLV deciles) that would tell a future session whether authoring a full falsifiable H is worth the investigation cost. GRADUATE would commit to that cost before either question is answered; DROP would discard a statistically real, well-powered, directionally stable effect for no principled reason.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** none — operator/D-S-A-triggered, not calendar-triggered.
- **Trigger condition:** either (a) an operator or the next session's D-S-A gate rules on which raised-bar route (if any) this claim needs to clear, or (b) a cheap follow-up converts rho≈−0.03 into a decile-conditioned expected-value read (e.g., P(next-bar CLV in bottom tercile | this-bar CLV in top decile) vs base rate) large enough to justify the investigation cost regardless of route — either would let this graduate to a proper Pre-Q.
- **Drop trigger:** if the decile-conditioned follow-up in (b) shows the effect is economically negligible even at the extremes (e.g., <2-3pp lift on any conditional read), this notice should close DROP as a real-but-immaterial microstructure artifact.
- **Calendar entry:** none.

**Forbidden moves, this notice:**
- Assuming Route 1 (or any specific route) covers this construct without an explicit ruling — the handoff itself flagged this as unresolved, and nothing measured this session resolves it.
- Treating rho=−0.03 as if it were candidate 2's or candidate 4's effect size — it is roughly an order of magnitude smaller in practical terms even though all three cleared their respective statistical bars.

---

## §10 — Audit hooks

```bash
# Reproduce the block-shuffle null (~10-20s, 2000 perms over n=141,540 pairs)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_autocorr.py
# Expected: rho ~-0.0301, block-shuffle band [-0.0052, 0.0051], p_lower=0.0005, halves same sign

# Confirm zero degenerate H==L bars in this panel (precondition for CLV being well-defined everywhere)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/data_lib.py 2>&1 | grep "degenerate"
# Expected: 0 / 141541

# If GRADUATED: confirm the Pre-Q references this notice
grep -rn "N-2026-08-29-mnq-clv-autocorrelation" docs/briefs/Q-*.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md --type notice
```
