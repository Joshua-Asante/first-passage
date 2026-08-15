# ORB MNQ v0.1 — native-MNQ candidate edition (ORB-MNQ-1)

**Status:** `CANDIDATE · NOT LIVE` — first authoring 2026-07-21 (operator GO: "create the
pine for the nas orb strategy that survived", discharging the ADMISSION note's gated
Pine-authoring item). **Superseded as the active working edition by
[`orb_mnq_v0_2_CANDIDATE.md`](orb_mnq_v0_2_CANDIDATE.md)** (calendar conformance D1–D4 +
D5 full-session clock pin). Retain this note as the OCA-fixed baseline. Rail build,
account registration, and live spend remain separately gated
([ADMISSION](../../../lab/analysis/orb_mnq_2026-07/ADMISSION.md); reconstruction ADR
[`2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../../../docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) §4/§7).
**Edition file:** `orb_mnq_v0_1.pine` (gitignored per public-clone posture; hash pinned in
[`PORT_MANIFEST.sha256`](../PORT_MANIFEST.sha256) — **`df05512d…`**, supersedes `c4ac4c00…`
— 2026-07-21 OCA fix, see Acceptance checklist).
**Lifecycle:** ORB-MNQ-1 `CANDIDATE @ 1.00×` (admitted 2026-07-16, with standing caveats:
regime-conditional post-2020 edge, cost-marginal on the full window, regime-common-mode +
high-variance/risk-dominant breadth read). **Naming:** `orb_mnq`, not `striker-*` — ORB is
a distinct mechanism from the locked Striker NAS100 v1 swing/pyramid.

## Provenance chain

1. **Construct origin:** `ops/instruments/NAS100.md` N1 (CFD NAS100 ORB-30) via
   [`lab/analysis/orb/orb_universe_2026-06-22/`](../../../lab/analysis/orb_universe_2026-06-22/RESULTS.md)
   (`orb_lib.py::orb_backtest`, or_bars=2).
2. **CFD Pine reference:** `core/strategies/candidates/nas100_orb_v0_1.pine` — reconciled
   against the harness 2026-06-24 (OR-completion order timing + resting-order-leak fixes
   carried from that vintage).
3. **Native-MNQ validation:** [`lab/analysis/orb/orb_mnq_2026-07/`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS.md)
   — Stage-2 cost-law PASS 5.31×/8.10×, Stage-6 DSR 0.9754 / annSR +0.890 / placebo
   p=0.0040, Stage-7 all-four-firms PASS on 2021+, Stage-8 realized N_eff 1.99→2.95.
   Frozen by [`2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../../../docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md)
   (§8 GO signed 2026-07-16/JA).

## Frozen construct (parameter axis — do not tune)

OR = first 2 regular-session 15m bars (09:30 + 09:45 ET) → both-sides touch-fill breakout
of OR hi/lo (stop orders) → protective stop = opposite OR extreme → flat at session close
(~16:00 ET) → one trade/day. No conditioning gates, no give-back/trailing exit, no
parameter sweep (confirm-not-mine, K_intrinsic=1).

## Venue deltas vs the CFD candidate (the ONLY changes)

1. **EOD force-flat on the 15:45 ET bar** (fill at 16:00 bar open) — envelope E1 / MFFU
   16:10 binding; the CFD out-of-session close would fill ~16:30 on CME's halt calendar.
2. **Entry placement window ends on the 15:30 ET bar** (last fill-eligible bar = 15:45 =
   harness `rest_tods` tail); unfilled OCO cancelled on the EOD bar.
3. **Frozen research economics baked in:** commission `cash_per_contract` **$0.61/side**
   (Bulenox, `core/firm_rules.py::cost_per_side_usd`) + `slippage=1` tick — the exact
   Stage-2/6/7 cost model. TV-properties overrides: Tradeify $0.91, MFFU/BluSky-NT $0.95
   (2021+ window passes all four firms up to 3 ticks; FULL window is
   Bulenox-and-≤1-tick-specific — [`RESULTS_stage7.md`](../../../lab/analysis/orb_mnq_2026-07/RESULTS_stage7.md)).
4. **`initial_capital` $100,000** (prop survivor-scoring band); margin 0/0.

**Sizing = fixed 1 contract** (parity with the fixed-R harness; risk unit = OR range).
Live sizing belongs to the account-multiplier layer (Q-PYRPARITY-1) — never TV inputs.
**Alerts are informational only** — the B1 JSON alert-payload contract is deliberately NOT
included: ORB-MNQ is not a c1 leg; that contract lands only with an operator-GO'd rail
integration (and a re-pin).

## Known approximations (inherited from the reconciled CFD candidate)

- Same-bar both-sides touch resolves by TV's intrabar path assumption, NOT the harness's
  bar-open-vs-OR-midpoint tiebreak — the OCA fix (below) stops the double-fill/reversal but
  does not make the *which-side-wins* choice on a both-touched bar identical to the harness.
- No protective stop during the entry bar itself (exit order exists from the next bar).
- Early-close days (no 15:45 bar): the out-of-session backstop exits on the next session's
  first bar; the firm force-flat is the operational backstop.

## 2026-07-21 TV-export reconcile + OCA fix

First TV Strategy Tester export (`CME_MINI:MNQ1!` 15m, 2022-07→2026-07, n=1,070) reconciled
against the harness. Coarse parity held (net-of-cost meanR +0.081R vs the harness 2021+
anchor +0.089R; 2024/2025 nearly exact) but surfaced a **same-bar reversal defect**: without
an OCA link, a bar breaching both OR extremes intrabar filled the "L" and "S" stop orders in
sequence — opening a position then immediately reversing it — a class the harness's
mutually-exclusive touch-fill assumption never has. Measured: **30 reversal events** (~2.8%
of trading days), the reversal-opened second leg netting **-$1,896** (WR 0.22). Fixed by
linking both entries into one `oca_name`/`oca_type=strategy.oca.cancel` group (engine-level
same-bar cancel, not the script-level `strategy.cancel()` calls already present, which only
take effect on the following bar). No construct/parameter change — order-placement-only, per
the frozen-construct discipline (pre-reg §5).

**Filter-suggestion note (operator asked "what filters qualify as structural edge"):** none
do, at current evidence. Pre-reg §5 forbids conditioning gates outright (four prior attempts —
gap/GEX/T10Y3M/Friday — all FALSIFIED on the CFD twin), and any filtered variant is a new
candidate: K_eff rises 2→3, pushing the DSR Sharpe floor 0.85→0.98, a bar the *unfiltered*
construct's full-window annSR (+0.890) does not clear. The one axis with an ex-ante
mechanism (cost_R = rt/(OR range), so small-range days are cost-dominated) shows a
non-monotone quartile profile in the export (Q1 weak as predicted, but Q2 > Q3), so a
threshold there is not yet distinguishable from curve-fitting. DOW/hour cuts visible in the
export (e.g. Fri > Mon by ~2 SE) are exactly the class N10 already falsified and are quoted
here only as the diagnostic that was checked, not as a proposal.

## 2026-07-21 second TV-export reconcile — per-trade parity vs the harness (OCA-fixed)

Fresh export (`ORB_MNQ_v0.1_..._fe29d.csv`, same window, n=1,040 — exactly 30 fewer than
the pre-fix export) confirms the OCA fix mechanically: **zero** reversal-tagged exits, zero
multi-trade days (both were 30/27 pre-fix). Went further than the coarse year-level check —
ran a true per-trade join against the Stage-2 harness (`orb_lib.orb_backtest` on the same
cached `MNQ.v.0` decode, 2019-05-06→2026-07-16) on entry day, side, entry-tod, and
stopped-vs-EOD flag, for all 1,035 days in both series:

- **Side + entry-tod + stopped-flag all match: 1,003/1,035 (96.9%).**
- **26/32 mismatches (2.51% of all common trades) confirmed as the disclosed same-bar
  both-extremes-touched tiebreak** (verified directly against the underlying 15m bars: at
  the actual entry bar, both `up` and `dn` are true). Both engines score it a loss either
  way (harness R ≈ −1.0 in nearly every case) — Pine's own intrabar-path stop-fill
  assumption picks the opposite side from the harness's open-vs-midpoint rule on exactly
  this bar shape. This is the KNOWN APPROXIMATION already named above, now quantified: it
  affects entry direction attribution, not net P&L sign, on ~2.5% of trades.
- **6/32 (0.58% of all common trades) are a genuine residual**, not explained by the
  tiebreak: same side, but the stopped-vs-EOD flag (5 days) or entry bar (1 day, 15-min
  offset) disagrees. Consistent with a boundary-price disagreement between TV's live
  `CME_MINI:MNQ1!` feed and the databento `.v.0` continuous decode the harness runs on (a
  few ticks near a stop/OR level flips a touch/no-touch outcome) — not a Pine logic defect.
  No fix applied; too small (0.58%) and too consistent with known feed-splice noise to chase
  further at this stage.

**Verdict: PASS.** No new defect found; the OCA fix is confirmed structurally sound.

**Follow-on measurements (same day):** fill-realism penetration audit + excursion-bounded
exit kill tests + 2026-partial feed-sign resolution — [`RESULTS_tv_export_realism.md`](../../../lab/analysis/orb_mnq_2026-07/RESULTS_tv_export_realism.md).
Headlines: the 1-tick slip assumption is empirically underwritten (only 0.7% of entries are
shallow-touch); tighter-stop and fixed-profit-target redesigns are both pre-killed
(every tighter stop loses 0.03–0.06R; no fixed target reaches baseline even best-case);
the 0.50R median close give-back is unharvestable by any admissible exit class; the
harness-vs-TV 2026 "sign disagreement" flagged in the prior session was a stale local-file
join artifact, not a feed discrepancy — **both feeds read 2026 negative** on a matched
window (harness −0.0118, TV −0.0246, n=136 both sides), so the N2 decay tripwire should be
read as confirmed-negative-to-date, not ambiguous.

## Acceptance checklist (owed before any live use)

- [x] Compile clean — `python scripts/pine_check.py` **OK 2026-07-21** (guest
  translate_light endpoint); re-verified clean after the OCA fix.
- [x] Hash pinned in `PORT_MANIFEST.sha256` in the same motion (`df05512d…`, supersedes
  `c4ac4c00…`).
- [x] First TV-export reconcile run 2026-07-21 — coarse parity OK; same-bar reversal defect
  found and fixed (OCA group, above).
- [x] **Per-trade parity reconcile on the OCA-fixed edition** vs the harness R-series on
  CME_MINI:MNQ1! 15m — **PASS 2026-07-21** (96.9% exact match on side/entry-tod/stopped-flag;
  residual fully attributed above). See writeup.
- [x] Decay monitor calibrated to the live venue (Tradeify economics, 2021+ window) —
  baseline_pf 1.1691, pf_sigma 0.0836, floor 1.0855, block_size=2 (ACF, reproduces
  Stage-6d) — [`RESULTS_decay_monitor.md`](../../../lab/analysis/orb_mnq_2026-07/RESULTS_decay_monitor.md).
  A SEED calibration (no live venue exists yet to fire it), tagged `SURVIVAL-ONLY`
  (surveillance tightness only — does not revisit the ADMISSION-decided CANDIDATE
  @ 1.00× starting multiplier). Call-1 action-on-breach at `CANDIDATE`:
  [`ADR 2026-08-06-candidate-call1-action-on-breach`](../../../docs/adr/2026-08-06-candidate-call1-action-on-breach.md)
  (`Proposed` — operator review flag only; awaiting Accept).
- [x] Cap tripwire companion **registered** (docs-only, not live-wired) beside the
  PF-CUSUM seed — [`ADR 2026-08-06`](../../../docs/adr/2026-08-06-capa-tripwire-pfcusum-companion-registration.md)
  (`Accepted` 2026-08-06). Cap evidence:
  [`RESULTS`](../../../lab/archive/mnq_capa_n14_tripwire_2026-08-06/RESULTS.md).
  Fire thresholds deferred; no runner / lifecycle / entry-filter authority.
- [ ] Rail integration (alert-payload contract, sizing-host mapping) — separate operator
  GO; not authorized by this authoring.
