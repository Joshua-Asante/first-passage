# PREREG — `H-DSTRUCT-MNQ-1`: daily structural bias at its own granularity (Tier-1 screen)

**Class:** Tier-1 mechanism screen — measurement only, strategy-free, **no candidate is produced
by any outcome**. Same class as `Q-WLEGB-1` (K=0-adjacent frozen probe); this one is disclosed as
**K=1** (one new frozen object) rather than argued to zero.
**Date frozen:** 2026-08-18, committed **before** `run_dstruct.py` reads a single real bar.
**Operator context:** commissioned by JA this session ("a standalone daily structure idea"),
as the first live Tier-1 screen of the mechanism-by-mechanism program (deep-iteration lane
Step-0 pipeline). **Spend:** $0.00 (cached panel) · no manifest · no pull · Cap seat untouched.

---

## §1 — Object (frozen; no variants)

Daily analogue of the validated W-layer structure, **native to daily bars** — a NEW object, not
the W bias at another lag (see §3 bar-adjacency):

- **Daily close series:** last 15m-bar close per CME **session-day** (`date(et + 7h)` — Sunday
  18:00 ET bars belong to Monday, matching TV daily bars), from the cached MNQ 15m panel.
- **Bias:** `b_d = sign(close_{d−1} − EMA20(close)_{d−1})` — the **prior completed session-day**;
  `EMA20` = `ewm(span=20, adjust=False)` seeded at the first bar; bias undefined (excluded)
  for daily-bar index < 19.
- **Verdict cell:** `y_d = sign(rth_close_d − rth_open_d)` — **RTH open→close** (09:30→16:00 ET,
  `orb_lib.session_panel` convention). This is the only E1-deployable granularity; it is the
  verdict cell for exactly the reason `RESULTS_LEGB.md` §4 gave.
- **Disclosure cell:** session close-to-close `sign(close_d − close_{d−1})`.
- **Scored day:** `b ≠ 0` and `y ≠ 0` and RTH open/close both finite. `gateHit = (b == y)`.

## §2 — Panel & boundary

`_mnq_15m.pkl` from the primary checkout (`lab/analysis/orb/orb_mnq_2026-07/`), sha256 printed at
run time and compared against Q-SESSCONF-1's pinned `81c05e9a…` (mismatch → disclose + STOP).
Window: session-days **2019-05-06 → 2026-07-15** (the ORB campaign's already-read boundary;
nothing dated after it is read, keeping every reserved window untouched).

## §3 — Dedup & bar-adjacency (executed this session, summarized; full outputs in session log)

- `grep -niE "weekly|w.layer|wstruct" docs/rejected_candidates.md` → WSTRUCT (weekly, cost-killed),
  NG-EIA, TAS — none is a daily-EMA direction screen.
- `grep -niE "gate on the|regime.gate|selection.gate" docs/rejected_candidates.md` → GEX / T10Y3M /
  Friday gates **on ORB** (this screen conditions nothing on ORB — F2 guard not engaged) + gold
  KER/TSMOM overlay (gold, overlay-role — different instrument and role).
- `ops/instruments/MNQ.md` read: **N5** D5-RECOST intraday momentum OOS −0.327 bp (adverse prior,
  different object: first-half-hour→rest-of-day); **N8** leg (a) weekly fact + **Q-WLEGB-1 DEAD row**
  (weekly bias sub-weekly transfer FALSIFIED — its re-proposal bar covers *weekly structure carrying
  intraday*; this object is daily-native, so the bar is not engaged, and this prereg does NOT cite
  the W finding as warrant); **SIZEDIV F3** same-day-direction-relabel discriminator (imported into
  §5 reading discipline); ST-EH supertrend (15m flip construct, closed manifest; its per-cell 2024+
  holdout is not read here — this screen reads raw bars, no ST cells).
- No prior daily close-vs-EMA → next-day direction test exists on any instrument in
  `docs/rejected_candidates.md`, the MNQ ledger, or `lab/CATALOG.md` (`grep -riE "daily.*(ema|structural bias)"`).

## §4 — Frozen limbs (PASS requires ALL FOUR, verdict cell only)

1. **n-floor:** scored days ≥ 400.
2. **Block-bootstrap 95% CI lower bound > 0.50** (10-day circular blocks, 4,000 draws, seed 42).
3. **Both halves > 0.50** (time-ordered split of scored days).
4. **PRIMARY — beats the base-rate-matched, clustering-preserving placebo:** observed `gateHit`
   > p95 of 2,000 block-shuffles of the bias sequence (contiguous **60-day** blocks, order
   permuted, outcomes fixed; seed 7). 60-day blocks are frozen deliberately large — EMA20-bias
   streaks are long, and fragmenting them narrows the null (the exact overstatement
   `lesson: block-shuffle time-clustered signals` warns about). The closed-form base rate
   `f(+1)·P(up) + f(−1)·P(down)` is reported beside it as the analytic cross-check.

**Verdict:** `SIGNAL` = all four limbs; `NULL` = limb 4 fails (regardless of 1–3 — the
Q-WLEGB lesson is that 1–3 pass on marginals alone); `AMBIGUOUS` = n < 400 or panel defect.

## §5 — Predictions (frozen before compute) & reading discipline

- `f(+1)` (share of up-bias days) expected 0.60–0.80; O→C up-rate expected 0.49–0.53 (overnight
  carries most index drift); closed-form base expected 0.50–0.53.
- **Expected outcome: NULL** — adjacent priors (N5 OOS-dead intraday momentum; Q-WLEGB base-rate
  arithmetic; SIZEDIV "daily momentum in disguise"; eodadv null reversal) all point one way. The
  screen is run because it is $0, closes the operator's direct question at the granularity that
  matters, and a SIGNAL would be genuinely new information.
- **Per-side decomposition is disclosure only** (leg-b format). A bearish arm that improves but
  does not cross 50% is a "less long" license, not a short signal — pre-stated so it cannot be
  promoted post-hoc.
- **If SIGNAL:** routes to one Step-0 slate row (O→C day-hold expression; MNQ cost arithmetic at
  the 2.82 bp `hurdle_4x`); NOT to ORB conditioning (F2 guard), NOT to a candidate (index
  raised-bar routes get argued at campaign time, not here). **If NULL:** daily-EMA structure joins
  leg (b); the Step-0 slate proceeds with geometry-class daily ideas on the non-index triad.

## §6 — Forbidden moves

No second `emaLen` / horizon / lag / instrument on any outcome (that is the sweep this K=1
declaration excludes). No reading past 2026-07-15. No per-entry or ORB-conditioned variant.
No quoting limb-1–3 passes if limb 4 fails. No re-run with more shuffles on a near-miss
(outcome-conditional re-testing, per RESULTS_LEGB §6.4).
