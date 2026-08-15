# Cheap falsifier — EVT-1 (scheduled macro-release day, post-release continuation) · `KILL` — dual-authority, no split; the reformulated framing dies on SIGN, not selectivity

**Date:** 2026-08-10 · **$0.00 · K=0 · no Q-ID spent · no G0 authored** · EXPLORATION only (sessions ≤ 2025-08-31; CONFIRM unread)
**Trigger:** operator elected P-A from the reformulated-framing exploration (this session), after the cell-#3
slate exhaustion. INQHIORI §6 compliance: this is not a fourth draft from the dead prior-space — the three
kills all *detected* their state from intraday price and the states weren't rare (T-IMB 53.1%, SWING-1 99.9%);
here rarity is exogenous (the release schedule), detection burden zero. Named from the failure-mode autopsy +
the public calendar only; **no panel data, oracle output, or scored artifact was consulted about which days
perform, and T-IMB's winner-shape disclosures were not used as design inputs** (ADR
`TEMPORAL-SELECTIVITY-OPEN-2026-08-10` §2-B(1)/T1 attested).
**Dedup (executed this session, outputs in session record):** `instrument_profiles.py cell MNQ
event-window-reversal` → **untested — no prior on this cell** (settlement + auction class findings do not touch
the macro-release limb); `BINDING BAR index-intraday-ohlcv-directional-timing-2026-07-21` answered by **route
①** per the 2026-08-10 ruling (a calendar criterion is within-instrument temporal selectivity, causally named a
priori by construction). Adverse adjacencies disclosed, none binding: RATES-EV-ZF-1 (CPI/NFP-anchored
*breakout* on ZF cost-walled marginal; its closure explicitly preserves the release-anchored non-breakout shape
as never-run; its P0.1 event-day range concentration 17.62:1 PASSED), NG-EIA-1 (post-announcement δ noise on
NG, +8.30bp t+0.93 n=323), D5/intraday-momentum DEAD on MNQ (unconditional pooled — §0 of any successor must
argue the event-conditioned family distinction and cite D5 as adverse), `day-of-week-selection-gate` class
(post-hoc clock cuts — distinguished by causal a-priori naming of an information event), exogenous-ORB-gate
battery exhaustion (regime-gating an existing edge — different object; its orthogonality lesson noted for any
EXPLORATION stage).

## Frozen before running (written before the run; generous so failure is conclusive)

- **Universe:** `_mnq_1m.parquet` (UTC `ts_event` → ET). Session = ET date with ≥300 RTH (09:30–15:59) 1m
  bars, date ≤ **2025-08-31**. CONFIRM (≥ 2025-09-01) reserved and unread.
- **Criterion (one cell, frozen):** session date ∈ union{**CPI**, **NFP**, **scheduled FOMC decision days**}.
  CPI/NFP from `lab/archive/rates_ev_zf_recon_2026-07/build_calendar.py` (**primary-BLS provenance**, browsed
  per-year schedule pages; 2025 shutdown gap outside this window). FOMC 2019–2023 reused verbatim from the
  estate's pinned `FOMC_DATES_ET` (`git show pre-prune-2026-08-08:lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/stage2_run.py`),
  **minus the two labeled unscheduled/emergency actions (2020-03-03, 2020-03-15)** — the a-priori criterion is
  "the calendar said a decision comes today"; 2024–2025-08 extended from assistant knowledge. ⚠ **FOMC
  provenance caveat (estate-standard):** hand-pinned, NOT fetched; mitigations: two independent transcriptions
  agree on all 40 scheduled 2019–2023 dates, DOW assertion in-harness (all Wed except 2024-11-07 Thu), and the
  union is dominated 160:52 by primary-sourced BLS dates. Primary re-verification owed before any G0 freeze if
  this survives.
- **Anchor / direction / entry (uniform rule: direction = sign of post-release repricing; entry = first RTH
  bar at/after the anchor):**
  - CPI/NFP (08:30 ET): ref = close of the 08:29 ET bar (last pre-release price); sign = sign(09:30 bar open −
    ref); entry = 09:30 bar open.
  - FOMC (14:00 ET): ref = close of the 13:59 bar; sign = sign(14:00 bar close − ref); entry = 14:01 bar open.
  - Same-day collision (08:30-class + FOMC): **first anchor wins** (08:30 class) — once per session.
  - sign = 0 or required bars missing → skip, counted and disclosed.
- **Trade:** long/short per sign from entry; stop **G** pts adverse, touched intrabar (entry bar included) →
  exit at stop, gross = −G; else exit at the last RTH bar close (session-flat). **G=10 primary / G=20 reported**
  (generous). RT **1.41 pt**; net R = (gross_pts − 1.41)/G.
- **Dual-authority kill (frozen, SWING-1 form):** **KILL iff mean gross pt/trade < 5.64 (4× bar) AND net-R
  t < 2, at G=10.** A gross<bar-but-t≥2 outcome goes to the operator as a split verdict, not self-adjudicated.
  Halves (chronological) + long/short arms + stop rate + per-class counts disclosed.
- **Not licensed by any outcome:** no G0, no Q-ID, no retune of any frozen constant, no wider union, no
  per-release-type sub-scoring (screen the class, not the winner — EM §2.0a). Survival routes to the operator
  for the CON-3 authoring path (step-1a consult already executed).

## Result

Panel universe: **1,575** sessions clear the ≥300-RTH-bar filter ≤ 2025-08-31 (⚠ differs from the sibling
falsifiers' 1,456 — session-filter divergence disclosed; the criterion's own event set is self-contained so the
kill does not depend on it). Event days in panel: **193 (12.3% of sessions)** — CPI 75 · NFP 72 · FOMC 46;
3 same-day collisions resolved by the frozen first-anchor rule; **0 skips** (every event day had the reference
and entry bars). DOW assertion fired once on 2020-11-05 — a true post-election **Thursday** decision present
verbatim in the estate's pinned list; whitelist corrected (2020-11-05, 2024-11-07), no date changed.

| G | n | gross pt/trade | vs 5.64 bar | net R | t | WR | stopped | halves gross (older/newer) |
|---|---|---|---|---|---|---|---|---|
| 10 | 193 | **−2.127** | **−0.38×** | −0.3537 | **−1.41** | 0.067 | 93.3% | −2.909 / −1.353 |
| 20 | 193 | **−2.551** | **−0.45×** | −0.1980 | −1.09 | 0.135 | 86.5% | −1.581 / −3.510 |

**KILL fires on both limbs simultaneously** — mean gross is not merely under the 4× bar, it is **negative**,
with wrong-signed t under the ratified N-EDGE authority. Both halves negative at both geometries. No split
verdict exists to elect. Arms at G=10: long n=114 gross −3.882 / short n=79 gross +0.405 — the long
(post-release up-repricing continuation) side is the bleeder.

## Disclosures (none licenses anything)

- **The selectivity premise HELD — first criterion in the lane where it did.** 12.3% of sessions, base rate
  computable from the calendar before any data read (vs T-IMB 53.1%, SWING-1 99.9%). The kill is on the
  **direction rule's sign**, not on rarity: on the frozen union the post-release repricing **fades to
  wrong-signed-null rather than continues**. The detectability wall and the sign wall are different walls;
  cell #3 has now hit both.
- **Per-class gross (disclosure only, the frozen cell is the union):** CPI −9.10 / NFP **+9.51** / FOMC −8.97
  at G=10 (−8.75 / +10.43 / −12.77 at G=20). ⚠ **The NFP-positive read is a named laundering trap** — electing
  an NFP-only successor off this table is a post-hoc winner-pick from a scored list, the exact move ADR
  `TEMPORAL-SELECTIVITY-OPEN-2026-08-10` T1 voids and EM §2.0a forbids (screen the class, not the winner).
  Recorded, not elected, not electable as governed.
- **Sign-inversion (fade the post-release move) is not licensed** — the lane boundary bars sign-invert
  (CON-1 STOP precedent), and inverting after seeing results is the same post-hoc move in mirror form.
- **The FOMC provenance caveat does not carry the kill:** excluding every hand-pinned FOMC date, the
  primary-BLS-sourced 147 CPI+NFP events alone give mean gross ≈ **+0.02 pt/trade = 0.003× the bar**
  (from the printed per-class means) — still an order of magnitude dead. The kill is
  primary-provenance-robust.

## Disposition — both drafted framings of cell #3 are now dead at $0

**No G0 authored. No Q-ID spent.** Four pre-authoring falsifier kills on this cell in one day, spanning the
only two framings drafted: **price-detected rarity** (stop-width design · T-IMB · SWING-1 — states weren't
rare) and **schedule-given rarity** (EVT-1 — state rare, direction wrong-signed). The measured read tightens
the SWING-1 log's wall statement: the oracle headroom (3.3% of ~170 pt/session) remains real, and neither a
detected state nor an exogenously-scheduled state has captured any of it. A fifth criterion draft needs a
stated reason to differ from **both** dead framings, not just from the three price-detected kills.
**Re-proposal bar for EVT-1 specifically:** a materially different causal criterion on the schedule-based
framing — not a union re-cut, not a per-class winner-pick (T1), not sign inversion, not an anchor/reference
retune. Lane stop-rule count unchanged (falsifier kills are not campaigns; CON-1 alone stands FALSIFIED).
The decline option (HOLD, per the board default) and the external-route elections (C5 COT δ-probe · SSRN/R8
pull · L1 unpause ruling) return to the operator.
