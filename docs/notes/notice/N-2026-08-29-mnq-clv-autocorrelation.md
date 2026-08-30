# Notice — MNQ M15 closing-location is weakly mean-reverting bar-to-bar (real but small; scope ruled, cost-law pre-screen run — DROP)

**Notice ID:** N-2026-08-29-mnq-clv-autocorrelation
**Observed:** 2026-08-29; **cost-law pre-screen run 2026-08-30**
**Author:** Claude Code
**Source:** own statistical computation this session, candidate 5 of a pre-specified 5-candidate MNQ Notice-phase batch
**Status:** `DROP` (2026-08-30 — $0 cost-law pre-screen fails the floor cleanly; see §4/§5)
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

**DROP (2026-08-30, superseding the original HOLD below — the $0 cost-law pre-screen this notice's own §5 named has now run).** Script: [`candidate5_clv_cost_screen.py`](../../../lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_cost_screen.py). Design: unconditional whole-sample CLV_t deciles (P10=0.1134, P90=0.9091); forward 1-bar real return close_t→close_{t+1} in bp (not a CLV-to-CLV proxy); fade direction set by the data's own sign, not assumed. Result: top-decile lift −0.1470bp, bottom-decile lift +0.1333bp, combined implied gross edge **+0.1402 bp/event**, 95% block-bootstrap CI **[−0.0381, +0.3244]** (n_events=28,477, straddles 0) — against MNQ's own N6 hurdle (**3.01 bp**, already a 4× round-trip-cost figure, unit-comparable to a per-event round-trip directly — see the script's own docstring for why "bp/session" is a labeling artifact of the original momentum construct's 1×/day frequency, not a required frequency rescaling here). The implied edge is roughly 20× below the hurdle and its CI includes 0. **This clears ADR §4 D2** (pre-screen fails cleanly): DROP per that ADR, no Pre-Q authored.

~~**HOLD** (original, struck 2026-08-30 by the pre-screen result above). Reason: the finding is real and well-powered, but the magnitude is small enough that its practical/tradeable relevance is unproven — rho≈−0.03 has not been converted into an economically meaningful statistic that would tell a future session whether authoring a full falsifiable H is worth the investigation cost. GRADUATE would commit to that cost before that question is answered; DROP would discard a statistically real, well-powered, directionally stable effect for no principled reason.~~

**Admission-route status — resolved by [`docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md`](../../adr/2026-08-29-clv-autocorrelation-admission-route-scope.md) (`Proposed`, pending re-ratification after a same-day correction — see that ADR's Change history), superseding the "genuinely unclear" framing this notice originally used.** The ruling: a bar-shape statistic with no entry rule attached does not trigger the raised bar's admission gate at all — that gate fires at Pre-Q admission for an actual directional-timing *candidate*, which this is not yet. If/when converted into an entry construct: **Route 1 is plausibly open** — CLV's mechanism (bar-shape mean-reversion) sits outside the raised bar's three specifically-mapped cost-re-derivation axes (price / instrument-selection / hold-time), not merely outside the 2026-08-10 ADR's one temporal-selectivity worked example, and this openness is independent of and in addition to Route 3; **Route 2 does not apply** (same OHLCV modality); **Route 3 (beat `ORB-MNQ-1` net-of-cost, not merely clear the cost floor) remains separately available.** Route 1 eligibility still requires full G0 discipline (adversarial review, `K_intrinsic`, the F2 guard) — it is a scope reading, not a clearance. The cheap $0 cost-law pre-screen named in §5(b) below is the concrete next step before any Pre-Q either way, per that ADR's 2-C.

---

## §5 — DROP disposition (was: "If HOLD: re-check trigger")

**N/A — superseded 2026-08-30.** The drop trigger below fired; there is no re-check.

~~- **Re-check date:** none — operator/D-S-A-triggered, not calendar-triggered.
- **Trigger condition:** a cheap follow-up (b) converts rho≈−0.03 into a decile-conditioned expected-value read (e.g., P(next-bar CLV in bottom tercile | this-bar CLV in top decile) vs base rate, or an implied gross edge in bp/event) and checks it against MNQ's own cost hurdle (N6, ≈3.01 bp/session) — a necessary-condition-only floor check, per the admission-route ADR's corrected 2-C. Clearing it does **not** by itself graduate this to a Pre-Q: the full Route 3 comparison against `ORB-MNQ-1`'s own net-of-cost edge (+0.0626R/trade) needs an actual entry/exit construct to compute a comparable R-figure, which does not exist yet — that comparison is deferred to whenever such a construct is built. The route question itself no longer blocks graduation (resolved above; Route 1 is also plausibly open, independent of Route 3).
- **Drop trigger:** if the decile-conditioned follow-up in (b) shows the effect is economically negligible even at the extremes (e.g., <2-3pp lift on any conditional read), or fails either cost check, this notice should close DROP as a real-but-immaterial microstructure artifact.~~ — **fired**: the pre-screen's implied edge (+0.14 bp/event, CI straddles 0) is economically negligible against N6 (3.01bp).
- **Calendar entry:** none.

**Forbidden moves, this notice:**
- Treating a marginal pass of MNQ's own N6 cost hurdle as sufficient — per the admission-route ADR, Route 3 requires beating `ORB-MNQ-1`'s own net-of-cost edge, not merely clearing the generic floor.
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

# Reproduce the $0 cost-law pre-screen (2026-08-30 DROP disposition)
python lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate5_clv_cost_screen.py
# Expected: implied gross edge +0.1402 bp/event, CI=[-0.0381,+0.3244], vs N6 hurdle 3.01bp -- CLEARS=False
# (CI corrected 2026-08-30, Codex review PR #219: the fade-rule series is now built in
# chronological event order before block-bootstrapping, not concatenated-by-decile-then-
# bootstrapped -- mean edge is unchanged, only the CI's precision shifted slightly)

# Confirm no Pre-Q was opened for this DROP (per ADR §4 D2)
grep -rln "N-2026-08-29-mnq-clv-autocorrelation" docs/briefs/Q-*.md
# Expected: empty
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-29-mnq-clv-autocorrelation.md --type notice
```
