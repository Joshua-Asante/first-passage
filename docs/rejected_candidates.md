# Rejected portfolio candidates

Standing registry of strategy / instrument / parameter combinations investigated and rejected as portfolio additions. One entry per direction. Re-proposal of any entry on this list requires **new mechanism evidence**, not new parameters or a wider sweep.

This file is appended to at the close of any Pre-Q that closes FALSIFIED on strategy grounds, or at the close of a parent programme on SNAG-budget-exhaustion grounds (the Guardian-on-XAGUSD precedent below). New entries link to the closure artifact authoritative for the rejection.

The intake bar is the same as for any candidate: a mechanism-level claim with falsifiable specifics, not "let's try a wider grid."

> **2026-07-15 · AUDIT-2026-07-11 §5.4 confirmation:** challenge-era claim re-scope is **not** new mechanism evidence. Zero rejection-registry entries re-opened this sweep. Every re-proposal bar below stands unmodified (K7). Inventory: [`docs/notes/audits/programme-audit/2026-07-15-gate-denominated-closure-annotation-sweep.md`](notes/audits/programme-audit/2026-07-15-gate-denominated-closure-annotation-sweep.md).

---

## Entries

### buyback-blackout abstention × MNQ — KILL (POWER; pre-G0)

**Rejection scope:** the Phase B lane B3 construct `buyback-blackout abstention` on CBOT
**MNQ** (aggregate cap-weight-in-blackout sleeve; daily short-at-open / cover-15:45) as folded
into A1's compelled-abstention arithmetic check — not MNQ the instrument, not other
compelled-absence families, not a sleeve riding beside an independent daily mechanism.
**Closure date:** 2026-08-23
**Authoritative artifact:** [`A1 audit §6`](notes/audits/2026-08-23-kill-register-attribution-audit.md)
**Closure basis:** POWER class, category-inherited from F5/D3 (power 0.24–0.30 at single-digit
bp/session). Cadence survived with disclosure (token-trade covers clustered gaps). No card
authored; $0/K=0. Fold-in ran so this idea never consumed an MSL card slot.
**Surviving finding (NOT rejected):** the Phase C sleeve *rule* (a sleeve must name a daily
partner); MNQ instrument standing; B1/B2 live Phase B lanes.
**Re-proposal bar:** a materially different magnitude argument than F5's three failed instances
— **not** a cadence re-litigation, not a sleeve-only card, not a parameter retune.

<!-- concept-intake-entry mechanism_family="buyback-blackout-abstention" instrument="MNQ" rejection_reason="pre-G0 POWER kill, category-inherited from F5/D3 (power 0.24–0.30 at single-digit bp/session); cadence survived with disclosure; no card authored" harness_disposition_ref="A1 audit §6 (docs/notes/audits/2026-08-23-kill-register-attribution-audit.md)" date="2026-08-23" class="pre-g0-power-kill" role_tested="arithmetic-fold-in" falsifier_failed="POWER vs F5/D3 class precedent" addback_condition="materially different magnitude argument than F5's three failed instances — NOT cadence re-litigation / sleeve-only card / param retune" -->

### turn-of-month-premium × SPX500

**Rejection scope:** the Q-TOM-SPX-1 construct `turn-of-month-premium` on
**SPX500** / Pepperstone US500 daily (`[T+1:T+3]` window vs off-days; Etula
dash-for-cash) as frozen in [`Q-TOM-SPX-1.md`](briefs/Q-TOM-SPX-1.md) — not
SPX500 the instrument, not other calendar families.
**Closure date:** 2026-08-23
**Authoritative artifact:** [`Q-TOM-SPX-1-closure-dead`](briefs/closures/Q-TOM-SPX-1-closure-dead.md) ·
Layer-A record on [`SPX500.md`](../ops/instruments/SPX500.md) F5
**Closure basis:** Layer-A 2026-06-16 on the canonical Pepperstone US500 daily
feed (n=113) hard-absent (Welch t=0.64, perm p=0.2544, COVID-concentrated,
halves sign-reverse). Formal Pine confirmation unpaid since 2026-06; operator
GO (P10) did not reserve it. $0/K=0 this close. Decay UNTESTED (feed starts
2017); capturability PENDING (W3).
**Surviving finding (NOT rejected):** SPX500 instrument standing; Layer-A
harness + frozen thresholds; other SPX500 families (D1/D2/D3) on their own rows.
**Re-proposal bar:** new mechanism evidence — **not** a wider window, new
thresholds, or a Dukascopy re-run of this key.

<!-- concept-intake-entry mechanism_family="turn-of-month-premium" instrument="SPX500" rejection_reason="Layer-A RESOLVED-ABSENT on canonical Pepperstone US500 daily (t=0.64, perm p=0.2544, COVID-concentrated, halves sign-reverse); reserved Pine unpaid; operator DEAD 2026-08-23" harness_disposition_ref="Q-TOM-SPX-1 Layer-A 2026-06-16 (ops/instruments/SPX500.md F5)" date="2026-08-23" class="dead-absent" role_tested="existence" falsifier_failed="existence battery hard-absent (t<1.0; perm p>=0.10; drop-top-k / halves)" addback_condition="new mechanism evidence — NOT window/threshold retune or Dukascopy re-run" -->

### MSL-S2B sweep-failure-filtered continuation × MYM — STAGE-1 FAIL (route; pre-G0)

**Rejection scope:** the MSL-S2B card’s unpaid G0 path for `sweep-failure-filtered-continuation`
on CBOT **MYM** (15m; PDH/PDL sweep-failure as **filter** on a trend-continuation entry; k=1;
rr ∈ [2,3]) after Stage-1 door-check FAIL — not MYM the instrument, not MSL the channel, not
filter-role reuse of C1 DELETE PASS under a cleared route.
**Closure date:** 2026-08-14
**Authoritative artifact:** [`MSL-S2B-closure-stage1-fail-route`](briefs/closures/MSL-S2B-closure-stage1-fail-route.md) ·
[`STAGE1`](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md)
**Closure basis:** raised bar `index-intraday-ohlcv-directional-timing-2026-07-21` unbound for
continuation *entry*. Candidate A (SLR route ①) clears MR-at-level *filter* only. Candidate B
(temporal selectivity) blocked by Q-TNEC-CON-5 default pause; no Board un-pause. Composite
clearance forbidden. Steps 3–4 not reached. CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** MYM instrument standing; B8 occupancy; C1 DELETE PASS as
filter-role evidence; MSL channel; slate-2 design box.
**Re-proposal bar:** new modality / Board un-pause with explicit non-route-① thesis / different
loss-side shape — **not** θ-retune, not composite clearance, not silent reopen of C1 entry.

<!-- concept-intake-entry mechanism_family="sweep-failure-filtered-continuation" instrument="MYM" rejection_reason="Stage-1 FAIL (route): index raised bar unbound for continuation entry; SLR route ① filter-only; temporal-selectivity paused; composite forbidden" harness_disposition_ref="MSL-S2B STAGE1 (lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md)" date="2026-08-14" class="stage1-fail-route" role_tested="entry+filter" falsifier_failed="route declaration kill limb #1" addback_condition="new modality OR Board un-pause + non-route-① thesis — NOT composite clearance / θ-retune / C1 entry reopen" -->

### MSL-S2A pullback-failure resumption × MCL — FALSIFIED (explore IS)

**Rejection scope:** the MSL-S2A G0 construct `pullback-failure-resumption` on NYMEX **MCL**
(15m; impulse + failed-pullback resumption; k=1; rr=3; 09:00–14:30 ET) as frozen in
[`PREREG_G0`](../lab/archive/msl_s2a_mcl_2026-08/PREREG_G0.md) — not MCL the instrument,
not MSL the channel, not other continuation classes.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-S2A-closure-falsified`](briefs/closures/MSL-S2A-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md)
**Closure basis:** N-ACT FAIL (0.511 trades/week &lt; 1). Long FLIP FAIL (join-pullback beat
resumption). DELETE PASS both arms (moot under FALSIFIED). Means negative; CI not entirely
&lt; 0 (n 31/46). CONFIRM unread; Cap unclaimed; $0/K=0. Not `BOOK-CONDITIONAL(cadence)`.
**Surviving finding (NOT rejected):** MCL instrument standing; MSL channel; Stage-1 screen
arithmetic as a pre-G0 filter (passed here; explore killed); DELETE selection vs TOD sham.
**Re-proposal bar:** new mechanism evidence (different reference class / direction / TF) —
**not** I/P-window, stop-buffer, or rr retune on this G0.

<!-- concept-intake-entry mechanism_family="pullback-failure-resumption" instrument="MCL" rejection_reason="explore IS FALSIFIED: N-ACT 0.511 trades/week; long FLIP FAIL (join-pullback +0.047 vs resume -0.175). DELETE PASS both. CONFIRM unread." harness_disposition_ref="MSL-S2A RESULTS_g2 (lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="N-ACT trades/week < 1; long FLIP Req1a FAIL" addback_condition="new mechanism evidence — NOT I/P-window/stop-buffer/rr retune on this G0" -->

### MSL-C1 PDH/PDL failed-break reclaim × MYM — FALSIFIED (explore IS)

**Rejection scope:** the MSL-C1 G0 construct `pdh-pdl-failed-break-reclaim` on CBOT **MYM**
(15m; prior-day RTH PDH/PDL failed-break reclaim; k=1) as frozen in
[`PREREG_G0`](../lab/archive/msl_c1_mym_2026-08/PREREG_G0.md) — not MYM the instrument,
not MSL the channel, not other session-structure fades.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C1-closure-falsified`](briefs/closures/MSL-C1-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md)
**Closure basis:** both arms n≥100, mean net R ≈ −0.18 / −0.11, session-block 95% CI entirely &lt; 0
(FALSIFIED). DELETE PASS both arms (moot). CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** MYM instrument standing; B8 occupancy ADR; MSL channel;
Stage-0/1 door-check discharge for this card.
**Re-proposal bar:** new mechanism evidence — not stop-buffer / overnight-sham / window retune on this G0.

<!-- concept-intake-entry mechanism_family="pdh-pdl-failed-break-reclaim" instrument="MYM" rejection_reason="explore IS FALSIFIED: both arms CI upper < 0 (mean ≈ −0.18/−0.11R)" harness_disposition_ref="MSL-C1 RESULTS_g2 (lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms" addback_condition="new mechanism evidence — NOT θ-retune of this G0" -->

### MSL-C3 PDH/PDL failed-break reclaim × M2K — OPERATOR-KILL (B4 declined; pre-G0)

**Rejection scope:** the MSL-C3 card’s unpaid G0 path for `pdh-pdl-failed-break-reclaim` on
**M2K** after Stage-1 PASS — not M2K the instrument, not the mechanism **class**, not MYM/C1.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C3-closure-operator-kill`](briefs/closures/MSL-C3-closure-operator-kill.md) ·
[`STAGE1`](../lab/archive/msl_c3_m2k_2026-08/STAGE1.md)
**Closure basis:** operator declined B4; no G0 freeze; $0/K=0. Stage-1 screens had PASSed.
**Surviving finding (NOT rejected):** M2K instrument standing; MSL channel; mechanism class
`pdh-pdl-failed-break-reclaim` (available to MSL-C1 on MYM); Stage-0 L3/WSTRUCT/W4 discharge.
**Re-proposal bar:** fresh Stage-1 + new B4 — not a silent revive of this unpaid path.
**Addback closed (does not clear this row):** [`STAGE1_K2`](../lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) +
[ADR 2026-08-13](adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) +
[`PREREG_G0`](../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md) → explore
**`FALSIFIED`** both axes ([closure](briefs/closures/MSL-C3-K2-closure-falsified.md)). New mechanism
evidence still required for any further M2K addback of this class.

<!-- concept-intake-entry mechanism_family="pdh-pdl-failed-break-reclaim" instrument="M2K" rejection_reason="operator-kill pre-G0 (B4 declined): Stage-1 PASS but G0 never frozen; slot handed to MSL-C1." harness_disposition_ref="MSL-C3 STAGE1 (lab/archive/msl_c3_m2k_2026-08/STAGE1.md)" date="2026-08-13" class="operator-stop" role_tested="entry" falsifier_failed="n/a — B4 declined" addback_condition="fresh Stage-1 + new B4 GO — NOT silent revive of this unpaid G0 path" -->

### MSL-C3-K2 dual-axis MR-at-level × M2K — FALSIFIED (explore IS; K=2)

**Rejection scope:** the dual-axis G0 on **M2K** licensing both `pdh-pdl-failed-break-reclaim`
and `overnight-range-failed-extension-fade` at `K_intrinsic=2` — not M2K the instrument, not
MSL the channel, not MYM/C1 (already separate).
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C3-K2-closure-falsified`](briefs/closures/MSL-C3-K2-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md) ·
[`PREREG_G0`](../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
**Closure basis:** both axes both arms CI entirely &lt; 0 on IS (A means ≈ −0.15/−0.20R; B ≈ −0.12/−0.11R).
CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** M2K instrument standing; MSL channel; Stage-0/1 screen arithmetic;
estate Cap/DSR/floor ladder unchanged.
**Re-proposal bar:** new mechanism evidence — NOT θ-retune / stop-buffer / silent K=1 drop on this G0.

<!-- concept-intake-entry mechanism_family="pdh-pdl-failed-break-reclaim" instrument="M2K" rejection_reason="explore IS FALSIFIED (C3-K2 Axis A): both arms CI upper < 0 (mean ≈ −0.15/−0.20R)" harness_disposition_ref="MSL-C3-K2 RESULTS_g2 (lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms" addback_condition="new mechanism evidence — NOT θ-retune of this G0" -->
<!-- concept-intake-entry mechanism_family="overnight-range-failed-extension-fade" instrument="M2K" rejection_reason="explore IS FALSIFIED (C3-K2 Axis B): both arms CI upper < 0 (mean ≈ −0.12/−0.11R)" harness_disposition_ref="MSL-C3-K2 RESULTS_g2 (lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms" addback_condition="new mechanism evidence — NOT θ-retune of this G0" -->

### MSL-C2 London-range failed-extension fade × MGC — FALSIFIED (explore IS)

**Rejection scope:** the MSL-C2 G0 construct `london-range-failed-extension-fade` on COMEX **MGC**
(15m; London H/L fade after failed extension; k=1) as frozen in
[`PREREG_G0`](../lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md) — not MGC the instrument,
not MSL the channel, not other session-structure fades.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C2-closure-falsified`](briefs/closures/MSL-C2-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)
**Closure basis:** both arms n≥300, mean net R ≈ −0.18, session-block 95% CI entirely &lt; 0
(FALSIFIED). DELETE FAIL both arms (sham prior-RTH less negative than London-constrained).
CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** MGC instrument standing; MSL channel; Stage-1 screen
arithmetic as a pre-G0 filter (passed here; explore killed).
**Re-proposal bar:** new mechanism evidence (different reference class / direction / TF) —
**not** stop-buffer, rr, or London-window retune on this G0.

<!-- concept-intake-entry mechanism_family="london-range-failed-extension-fade" instrument="MGC" rejection_reason="edge-failure (FALSIFIED): explore IS both arms mean_R≈-0.18, CI entirely <0 (long n327 [-0.287,-0.071]; short n310 [-0.292,-0.075]); DELETE FAIL (sham prior-RTH less negative). CONFIRM unread." harness_disposition_ref="MSL-C2 explore G0 (lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)" date="2026-08-13" class="edge-failure" role_tested="entry" falsifier_failed="both-arms CI upper <0; DELETE Req1a FAIL" addback_condition="new mechanism evidence — NOT stop-buffer/window/rr retune on this G0" -->

### Transfer/expression lane (Q-TXG-1) — FALSIFIED-at-walls

**Rejection scope:** the Q-TXG-1 transfer/expression programme — incumbent locked mechanisms
(Guardian / Striker / Striker NAS100 / Aegis) × ENV-1 7-micro pool at Tradeify Select
EOD-trailing survival geometry — as a *lane*, not any single home-instrument strategy and not
ENV-1 instruments as a class.
**Closure date:** 2026-08-12
**Authoritative artifact:** [`docs/briefs/Q-TXG-1-ha-reargument.md`](briefs/Q-TXG-1-ha-reargument.md)
(operator elected **(A) CLOSE**) ·
[`lane closure`](briefs/closures/Q-TXG-1-closure-falsified-at-walls.md) ·
cell closures [`nas100×MYM DEAD(cost)`](briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) ·
[`striker×MNQ DEAD(N-SURV)`](briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) ·
[`Guardian→MGC DEAD(N-SURV)`](briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) ·
Aegis→6J both-layers ([`ops/instruments/6J.md`](../ops/instruments/6J.md) J4b+J14)
**Closure basis:** two consecutive elected-cell FALSIFIEDs forced H_A re-argument (design §6);
operator elected CLOSE. Four positive-net transfers; zero survivors against the composition of
the frozen per-trade cost floor and the trailing-DD survival ceiling
(`lesson_trailing_dd_survival_is_skew_governed`). Remaining 23 OPEN cells are stop-unscreenable
(ATR-median unlock refused without new mechanism evidence).
**Surviving finding (NOT rejected):** locked-book mechanisms on home instruments; ENV-1
instrument-lane eligibility; ORB payability and paid/new-venue generation routes.
**Re-proposal bar:** new mechanism evidence with a **demonstrably different loss-side shape**,
or a **venue class whose survival geometry differs** (not an EOD-trailing prop clone) —
**not** new cells, new instruments, or ATR-input spend alone.

### Striker NAS100 → MYM sibling-swap (Q-TXG-1 cell #1) — DEAD(cost)

**Rejection scope:** the Striker NAS100 v1 → CBOT MYM cross-underlying sibling-swap cell
(execution-mechanics port only; locked parameters untouched), not Striker-on-NAS100 and not
the WITHDRAWN(F1) striker_nas100×MNQ redeploy.
**Closure date:** 2026-08-12
**Authoritative artifact:** [docs/briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md](briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) ·
[cell PREREG](briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) ·
[manifest](../discovery_manifests/q_txg1_striker_nas100_mym_20260812.json)
**Closure basis:** native-TV panel cost FAIL vs frozen `required_net_r` 0.06 / `port_must_beat`
(N=190; Net +$4,356.40; mean_net_r **0.0129** < 0.06; PF 1.110; static-equity recompute OK).
N-SURV not reached.
**Re-proposal bar:** subsumed by the lane-level Q-TXG-1 FALSIFIED-at-walls bar above (different loss-side shape or different venue-class survival geometry) — not a locked-parameter retune, not amending `required_net_r`, not firm-shopping, not a silent third election.

### Striker DJ30 → MNQ sibling-swap (Q-TXG-1 cell #2) — DEAD(N-SURV)

**Rejection scope:** the Striker DJ30 v4.5 → CME MNQ cross-underlying sibling-swap cell
(execution-mechanics port only; locked parameters untouched), not Striker-on-DJ30 and not
the WITHDRAWN(F1) striker×MYM redeploy.
**Closure date:** 2026-08-12
**Authoritative artifact:** [docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md](briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) ·
[cell PREREG](briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md) ·
[manifest](../discovery_manifests/q_txg1_striker_mnq_20260812.json)
**Closure basis:** native-TV panel cost PASS (mean_net_r 0.0419 > required_net_r 0.03; N=222) then

surv_channel.py on bar-derived MNQ_M15 daily series (n=164) against Tradeify_Select_100K at the
frozen 2026-07-13 floors (bust ≤3.0% ∧ P(pass)≥50%). Bust **98.13%** full / **96.76%** H1 /
**99.37%** H2 — ~32×–33× over ceiling on every partition.
**Re-proposal bar:** subsumed by the lane-level Q-TXG-1 FALSIFIED-at-walls bar above (different loss-side shape or different venue-class survival geometry) — not a locked-parameter retune, not amending the 3.0% floor, not inventing an ENV-1 panel N, not a silent third election.


### Guardian→MGC transfer cell (R7 / b8) — DEAD(N-SURV)

**Rejection scope:** the Guardian Gold v5.5 → MGC venue-transfer cell (execution-mechanics
port only; locked parameters untouched), not Guardian-on-XAUUSD and not MGC-the-instrument.
**Closure date:** 2026-08-11
**Authoritative artifact:** [`docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) ·
[`cell PREREG (retroactive)`](briefs/pre-registration/2026-08-11-guardian-mgc-transfer-cell-prereg.md) ·
[`b8`](pursuits/b8-guardian-mgc-transfer-lane.md)
**Closure basis:** `nsurv_channel.py` on the v0.3 native MGC1! panel (N=329 / daily n=276)
against `Tradeify_Select_100K` at the frozen 2026-07-13 floors (bust ≤3.0% ∧ P(pass)≥50%).
Bust **42.2%** full / **72.4%** H1 / **16.5%** H2 — 5.5×–24× over ceiling on every
partition. Same trailing-survival failure class as Aegis→6J J4b, more severe. Two
disclosed caveats (unpre-registered half-boundary; AE-approximated `intraday_low`) keep
the score exploratory-grade; the margin settles the qualitative DEAD.
**Surviving finding (NOT rejected):** MGC remains venue-legal / instrument-lane eligible;
Guardian v5.5 on XAUUSD is untouched. ⚠ Q-TXG-1 lane later **FALSIFIED-at-walls** (operator A, 2026-08-12) — further transfer elections under that Q-ID are barred; see lane row above.
**Re-proposal bar:** new mechanism evidence (fresh cell PREREG + operator election under
Q-TXG-1 or equivalent) — **not** locked-parameter retune, **not** re-reading the
AE-approximated score, **not** amending the 3.0% floor.


### Guardian-family strategy on XAGUSD (Silver)

**Rejection scope:** the direction is rejected, not only a single parameter port.
**Closure date:** 2026-05-14
**Authoritative artifact:** `Q-CORR-1-closure.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-CORR-1-closure.md`)
**Closure basis:** parent programme Q-CORR-1 closed on SNAG-budget exhaustion. Q-CORR-1.1 falsified the v5.5-parameter-equivalence port (DD 11.52% > 8.0%; WR 11.34% below band). Q-CORR-1.2 (parameter-freedom WFO) was withdrawn pre-lock as part of the parent closure. Parallel v1.5-sweep track yielded a single +2% tweak running in-sample; quarantined-hint, not evidence.
**Surviving belt finding (NOT rejected):** instrument-level correlation is not a reliable proxy for strategy-level correlation. The NAS100/DJ30 strategy-level decorrelation despite tight instrument correlation stands as a portfolio-construction belt finding, independent of this candidate's rejection. A 5th strategy on a different instrument, or on Silver with genuinely new mechanism evidence, remains open at the standard intake bar.
**Re-proposal bar:** new mechanism evidence. "New parameters" / "a wider sweep" / "longer panel" / "different correlation gate threshold" do not clear the bar — that is precisely the move the parent closure rejected.

**2026-07-01 override + closure annotation (alongside, does not delete the above).** The
Guardian **Silver v1.0** BE-off variant (0.15% fair-weather) was *admitted* 2026-06-11 via an
explicit operator override of this registry entry + the regime-robustness gate
([`docs/briefs/2026-06-11-guardian-silver-v1-admission-override.md`](briefs/2026-06-11-guardian-silver-v1-admission-override.md)),
which recorded in its own text that it "does not manufacture a mechanism claim …
operator-judgment admission, logged as such" (§7) — i.e. it did **not** clear the
new-mechanism bar. A same-day amendment made admission conditional on a §9 H1-counterbalance
leg (6-strat H1 bust ≤ 24.54%). **No counterbalance ever materialized** (5th-leg target spec
0/24; chop-native 0/9, `cb8e930`), so Silver never entered the live book (`core/firm_rules.py`
`_BASE_RISK` has 4 keys, no silver). **Operator CLOSED Guardian Silver v1.0 — NOT ADMITTED
(2026-07-01);** the WFO admission gate (Q-CORR-1.2) is retired as superseded (`STATE.md`).
The XAGUSD direction above therefore **remains rejected at its original bar** — the override
attempt is logged here for lineage, not as a re-admission. (Formal brief STATUS stamp + the
STATE.md/PREREG reconcile land via branch `claude/post-pivot-skew-fixes` `73eeab6`, unmerged
at this writing — see the 2026-07-01 audit follow-ups.)

### Custodian-family month-end equity-hedging flow on EURUSD

**Rejection scope:** the direction (month-end WM/Reuters-fix hedging-flow / Melvin–Prins channel on EURUSD) is **shelved — soft and reversible** (`for now`, 2026-06-10).
**Closure date:** 2026-06-10
**Authoritative artifact:** [`docs/briefs/rnd-pipeline/CC-HANDOFF-custodian-eurusd-v0.1-mechanism-probe.md`](briefs/rnd-pipeline/CC-HANDOFF-custodian-eurusd-v0.1-mechanism-probe.md) + probe scaffolding `lab/analysis/custodian_eurusd/CARD.md` (README + `verdict.md`).
**Closure basis:** intake **ADMIT 7/7**, but codification could not compose the concept (calendar-flow / cross-instrument / two-sided archetype is outside the primitive library — `compose_from_hint` raises). Routed to the cheap `lab/analysis/` mechanism-probe lane (USOIL/NOCT precedent); the pre-registered regression (β>0 sig@5%, 2016–26 EURUSD pre-fix return on prior-month US−EZ equity return) **never completed — the Dukascopy fetch hung.** A hand-authored Pine (`core/strategies/candidates/custodian-eurusd-v0.1.pine`, gitignored) was tested manually on TradingView and **underperformed** (operator read). This is therefore a **manual-test rejection, NOT a completed formal falsifier.**
**Surviving finding (NOT rejected):** the codification capability-boundary — `compose_from_hint` only codifies intraday-technical / single-instrument / long-only archetypes; calendar-flow / cross-instrument-direction / two-sided concepts need a primitive-library extension. Independent of this candidate's fate.
**Re-proposal bar:** a **completed mechanism probe** (the regression that never ran) **or genuinely new mechanism evidence** — NOT Pine parameter tweaks, a different fix-window, or a wider sweep.

<!-- concept-intake-entry mechanism_family="custodian-family" instrument="EURUSD" rejection_reason="SHELVED 2026-06-10 (soft). Manual TradingView backtest of hand-authored Pine underperformed; the formal pre-registered regression (beta>0 @5%, 2016-26) never ran (Dukascopy fetch hung). Manual-test rejection, not a completed falsifier. Re-proposal bar: a COMPLETED mechanism probe or new mechanism evidence, not Pine param tweaks." harness_disposition_ref="manual-TV-backtest (no harness DispositionRecord; probe incomplete, lab/analysis/custodian_eurusd/CARD.md)" date="2026-06-10" -->

### Short-only mean-reversion spike-fader on USOIL

**Rejection scope:** the direction (short-only fade of upside overextension on USOIL) is rejected as an **entry** mechanism — not only a parameter port. First entry written under the extended taxonomy schema (ADR [`docs/adr/2026-06-14-rejected-candidate-patterns.md`](adr/2026-06-14-rejected-candidate-patterns.md) §D).
**Closure date:** 2026-06-14
**Class:** edge-failure (primary) + venue/cost-constraint (secondary)
**Authoritative artifact:** [`docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md`](adr/2026-06-14-reject-usoil-rdm-spike-fader.md) + probe `lab/analysis/usoil_rdm/` ([RESULTS.md](../lab/archive/usoil_rdm/RESULTS.md)).
**Closure basis:** `CONCEPT-USOIL-RDM-001` killed pre-build (0 forward slots). Pre-registered 4H probe falsified on all three limbs, **confirmed on the canonical `PEPPERSTONE:SPOTCRUDE` feed**: cost geometry (mean realized cost 0.090R; gross expectancy negative at every target cell — sub-ATR confirmation-stop infeasible), placebo p=0.718 (indistinguishable from a random short), thirds all negative. Staging `FX_USOIL` corroborates (the lone +0.008 recent third is statistically zero, n=102, and absent on canonical). Distinct mechanism class from the carry (D2) and breakout-regime-capture (active RGC) USOIL entries.
**Re-proposal bar (add-back):** a **genuinely new entry mechanism** (distinct class) — NOT a re-tune, subset/regime slice, or stop-geometry tweak of this confirmation-fade entry. Per role-asymmetry, a fade *signal* may still be probed as an exit/filter without clearing this entry-rejection.

<!-- concept-intake-entry
     mechanism_family="mean-reversion-spike-fade" instrument="USOIL"
     rejection_reason="edge-failure: pre-registered 4H spike-fader killed pre-build. CANONICAL PEPPERSTONE:SPOTCRUDE (2020-23, n=198): mean realized cost 0.090R, net E[R]<0 all T{1.0,1.5,2.0,2.5}, gross<0 every cell, placebo p=0.718, thirds all neg (-0.069/-0.274/-0.115), all horizons neg. Staging FX_USOIL corroborates (p=0.273; lone +0.008 recent third statistically zero, absent on canonical). Sub-ATR confirmation-stop -> ~0.09R hurdle (L-COST-GEOMETRY)."
     harness_disposition_ref="CONCEPT-USOIL-RDM-001 (no harness DispositionRecord; never intaked; ADR-sourced, lab/analysis/usoil_rdm)"
     date="2026-06-14"
     class="edge-failure+venue-cost"
     role_tested="entry"
     falsifier_failed="canonical placebo p=0.718 (n=198); net E[R]<0 all T all H; gross<0 every cell; thirds all neg"
     addback_condition="NEW entry mechanism (distinct class) ONLY - not re-tune, subset/regime slice, or stop-geometry tweak"
     config_fingerprint="usoil-rdm/4H/sma50/atr14/m2.0/entry=reentry/stop=spikehigh/Tcurve{1.0,1.5,2.0,2.5}/H{12,30,60}/feed=PEPPERSTONE:SPOTCRUDE(c35c1)+FX_USOIL(staging)" -->
- **mean-reversion-spike-fade on USOIL** — rejected 2026-06-14 (edge-failure: canonical PEPPERSTONE:SPOTCRUDE placebo p=0.718, net/gross E[R]<0 all cells, thirds all neg; sub-ATR confirmation-stop ~0.09R hurdle); ADR-sourced `CONCEPT-USOIL-RDM-001` (never intaked; `lab/analysis/usoil_rdm`).

### FX intraday fixing-reversal (session mean-reversion) on EURUSD

**Rejection scope:** the direction (London 16:00 WM/Reuters fix fade — long EURUSD into the fix, protective stop, time-exit) is rejected as a 5th-leg **entry** mechanism on **cost-geometry** grounds. Distinct from the shelved *custodian-family month-end-flow on EURUSD* above: that is a calendar/month-end fix-flow hedging concept; this is the **daily** intraday fix microstructure (Krohn/Mueller/Whelan, *J. Finance* 2024) — a different mechanism family, no dedup collision.
**Closure date:** 2026-06-22
**Class:** venue/cost-constraint (gross edge is real; cost kills it — not edge-failure).
**Authoritative artifact:** [`lab/archive/fixrev_costscreen_2026-06-22/`](../lab/archive/fixrev_costscreen_2026-06-22/README.md) (README + `RESULTS.md`; 15 self-tests; reuses core `decode_bar_signal` zero-fork; zero `core/` touch). Decision stub: [`lab/analysis/fixrev_costscreen_2026-06-22/CARD.md`](../lab/analysis/fixrev_costscreen_2026-06-22/CARD.md).
**Closure basis:** cost **pre-screen** (the cheapest falsifier — **NOT** a full pre-registered Pre-Q) on the canonical Pepperstone 5m EURUSD feed (445,798 bars, 2020-06 → 2026-06, **n=1550 fix-days**). The gross post-fix reversal **reproduces the source paper's magnitude** (best cell +0.0455R ≈ ~2 bps mean post-fix move) and is correct-signed (long-EURUSD-post-fix net-positive across the grid = the paper's USD-reverses-after-fix). But the **best-of-grid break-even is 0.277 pip ≪ FXIFY ~0.8 pip all-in**: net R is negative in every (hold × stop) cell at ≥0.4 pip cost, and the verdict is **robust to the exact spread** (gross edge ≤0.055R even at zero cost). Confirms the paper's own "not easy to exploit once transaction costs are accounted for." Same cost-law wall as the USDCAD Aegis-MR transfer (0.097R @1.42×ATR) and the USOIL spike-fader.
**Re-proposal bar (add-back):** evidence of **materially better-than-retail execution** on the fix (the paper survives only at half-spread), OR a **genuinely different mechanism**. NOT a re-tune of the hold/stop grid, a different fix (Tokyo/Frankfurt), or a wider panel — the cost geometry, not the parameters, is what failed; re-tuning is the named degeneration move.

<!-- concept-intake-entry
     mechanism_family="fx-fixing-reversal-session-mr" instrument="EURUSD"
     rejection_reason="venue/cost-constraint: London 16:00 fix fade cost-pre-screen FAIL on canonical PEPPERSTONE 5m EURUSD (n=1550 fix-days, 2020-06->2026-06). Gross post-fix reversal reproduces the source paper (~2bps; best cell +0.0455R) and is correct-signed, but best-of-grid break-even 0.277 pip << FXIFY ~0.8 pip all-in; net R<0 every (hold x stop) cell at >=0.4 pip; robust to spread (gross edge <=0.055R at zero cost). Confirms Krohn/Mueller/Whelan JF2024 after-cost conclusion. COST PRE-SCREEN, not a full pre-registered Pre-Q."
     harness_disposition_ref="cost pre-screen (no harness DispositionRecord; lab/analysis/fixrev_costscreen_2026-06-22/CARD.md)"
     date="2026-06-22"
     class="venue-cost-constraint"
     role_tested="entry"
     falsifier_failed="cost pre-screen: best-of-grid break-even 0.277 pip << 0.8 retail; net R<0 all (hold x stop) cells >=0.4 pip; n=1550 fix-days"
     addback_condition="materially better-than-retail fix execution evidence (paper survives only at half-spread) OR genuinely new mechanism - NOT grid re-tune / different fix / wider panel" -->
- **fx-fixing-reversal-session-mr on EURUSD** — rejected 2026-06-22 (venue/cost-constraint: London-fix fade cost-pre-screen FAIL on canonical EURUSD; gross reproduces the paper ~2bps but best-of-grid break-even 0.277 pip ≪ 0.8 retail, net<0 all cells; cost pre-screen, not a full Pre-Q); artifact `lab/analysis/fixrev_costscreen_2026-06-22/CARD.md`.
### Aegis-v4.3 mean-reversion template port on EURGBP

**Rejection scope:** the direction (Aegis-v4.3 Bollinger-band mean-reversion template — BB 19/1.9 + ATR19 + break-even, long-only, 15m — ported to EURGBP) is rejected, not only a single parameter set. **Refuted pre-build at 5th-leg adversarial review** — no EURGBP panel was exported or run.
**Closure date:** 2026-06-21
**Class:** venue/cost-constraint (primary) + edge-failure (secondary)
**Authoritative artifact:** [`ops/instruments/EURGBP.md`](../ops/instruments/EURGBP.md) (ledger stub D1 + durable findings F1–F3); refutation basis cross-references [`ops/instruments/USDCAD.md`](../ops/instruments/USDCAD.md) (durable #1 + dead-list) and [`docs/audits/2026-05-28-aegis-v43-indicator-strategy-diff.md`](audits/2026-05-28-aegis-v43-indicator-strategy-diff.md):214.
**Closure basis:** refuted on the EDGE & COST angle, all basis facts verified on disk. (1) **Cost geometry fails** — EURGBP is the lowest-volatility G10 cross (ATR(14) ~6 pips; 15m ATR a few pips), so an Aegis 1.42×ATR(15m) stop is *smaller in price* than USDCAD while spread is comparable (~0.6–1 pip + commission); by the USDCAD COST LAW (cost-in-R ∝ price/stop_dist), cost/R ≥ 0.097R — USDCAD measured exactly 0.097R round-trip at 1.42×ATR(15m) and already failed a 4×-cost-hurdle gate. After-cost PF≈2.0 is not credible. (2) **Direct precedent dead** — Aegis USDCAD v0.1 (the same mean-reversion transfer to a comparable cross) FAILED: n=245, PF 0.756, pervasive trend-impulse loss character, no hour/day/regime refuge. (3) **Edge-persistence-in-chop fails** — the H1 (2020–2023) window that must be survived contains the 2022 sterling crisis (sustained EURGBP move ~0.82→~0.90, mini-budget spike to ~0.923 on 26 Sep 2022), the strong-trend sub-regime where MR bleeds; our own Aegis/USDJPY had 2022 PF only ≈1.12.
**Re-proposal bar:** **new mechanism evidence** — specifically a **measured spread/ATR geometry that clears the cost hurdle on the canonical feed** (from the realized stop, not an assumed k·ATR). NOT new parameters, a different Bollinger setting, a longer panel, or a wider sweep — those do not clear the bar.

<!-- concept-intake-entry
     mechanism_family="bollinger-band-mean-reversion" instrument="EURGBP"
     rejection_reason="venue/cost-constraint + edge-failure: Aegis-v4.3 MR template port refuted PRE-BUILD at 5th-leg adversarial review 2026-06-21 (no EURGBP panel run). (1) Cost geometry: EURGBP lowest-vol G10 cross (ATR14 ~6 pips), 1.42xATR(15m) stop smaller in price than USDCAD, spread comparable -> cost/R >= 0.097R by the USDCAD COST LAW; USDCAD measured 0.097R RT @ 1.42xATR and failed a 4x-cost-hurdle gate -> after-cost PF~2.0 not credible (L-COST-GEOMETRY). (2) Direct precedent: Aegis USDCAD v0.1 (same MR transfer, comparable cross) FAILED n=245 PF 0.756, pervasive trend-impulse, no regime refuge. (3) H1 2020-2023 contains the 2022 sterling crisis (0.82->0.90, spike 0.923 on 26 Sep 2022) -> strong-trend sub-regime where MR bleeds; Aegis/USDJPY 2022 PF ~1.12. See ops/instruments/EURGBP.md."
     harness_disposition_ref="(no harness DispositionRecord; refuted at 5th-leg adversarial review, never intaked; ledger ops/instruments/EURGBP.md)"
     date="2026-06-21"
     class="venue-cost+edge-failure"
     role_tested="entry"
     falsifier_failed="adversarial-review refutation (no panel run): cost-law cost/R >= 0.097R (USDCAD-measured @ 1.42xATR, failed 4x-cost-hurdle) -> after-cost PF~2.0 not credible; direct precedent Aegis USDCAD v0.1 n=245 PF 0.756; H1 contains 2022 sterling-crisis trend (Aegis/USDJPY 2022 PF ~1.12)"
     addback_condition="a MEASURED spread/ATR geometry (from the realized stop, not assumed k*ATR) that clears the cost hurdle on the canonical feed - NOT new params, a Bollinger re-tune, or a longer panel"
     config_fingerprint="aegis-v4.3-port/EURGBP/15m/BB19@1.9/ATR19/SL1.42xATR/TPbasis+0.8ATR/BE(0.30/0.15)/long-only/feed=canonical-TV-CSV(NO PANEL RUN - refuted pre-build at adversarial review)" -->
- **bollinger-band-mean-reversion on EURGBP** — rejected 2026-06-21 (venue/cost-constraint + edge-failure: Aegis-v4.3 MR template port refuted pre-build at 5th-leg adversarial review. EURGBP lowest-vol G10 cross → 1.42×ATR(15m) stop smaller than USDCAD, spread comparable → cost/R ≥ 0.097R by the USDCAD COST LAW (USDCAD measured 0.097R RT @ 1.42×ATR, failed 4×-cost-hurdle) → after-cost PF~2.0 not credible; direct precedent Aegis USDCAD v0.1 dead (n=245, PF 0.756); H1 contains the 2022 sterling-crisis trend (Aegis/USDJPY 2022 PF ~1.12)); ledger `ops/instruments/EURGBP.md` (no harness DispositionRecord; refuted pre-build, never intaked).

### Gold trend-persistence regime-gate (KER_126 + TSMOM_252 deploy-vs-wait)

**Rejection scope:** the direction (a gold-regime "deploy vs wait" participation gate keyed on gold `KER_126 ≥ 0.12` **AND** `TSMOM_252 > 0`) is rejected as an overlay — not only these thresholds. Absorbed here from the retired `ops/regime_gate/` shadow tool per ADR [`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](adr/2026-07-11-ops-cfd-estate-retirement.md).
**Closure date:** 2026-07-01 (shadow logging discontinued; tool `git rm`-ed 2026-07-11 with the ops CFD-estate retirement).
**Class:** edge-failure (the in-sample separation was an n≈2-regime-block artifact; the gate inverts OOS).
**Authoritative artifact:** retired `ops/regime_gate/README.md` (retrieve via `git show <pre-2026-07-11-commit>:ops/regime_gate/README.md`); OOS falsifiers **Q-REGIME-OOS-1** (`f2ae609`, 2026-06-21) + **Q-REGIME-POSTCOVID-1** (`f6f0524`, 2026-06-22); graduated from [`lab/analysis/regime/regime_stress_2026-06-15/`](../lab/analysis/regime/regime_stress_2026-06-15/RESULTS.md).
**Closure basis:** the KER/TSMOM gold-regime signal falsified twice OOS after deployment — Q-REGIME-OOS-1 deep-OOS AUC 0.448 / 0.563 (the gate **inverts**: DEPLOY +0.004R vs WAIT +0.284R), Q-REGIME-POSTCOVID-1 held-out AUC 0.556 with the KER leg inverted. The pre-registered forward kill-tripwire was structurally unfireable in shadow mode (it keys on acted-on `DEPLOY` outcomes; shadow emits none), so continued logging accrued no decision value. The locked book (99.83 / 0.17 / 4.37) was never touched by this gate.
**Re-proposal bar:** **new mechanism evidence that survives OOS** — NOT a re-run of this signal, a refit of the `0.12` / sign thresholds, or a longer shadow log. Refitting the frozen constants is the named overlay-scar move.

### Other directions (entries pending formalization)

Directions named in `Q-CORR-1-closure.md` §3 as existing on this list under prior disposition. Each requires its own entry written at the close of its authoritative investigation; the closure note references them as comparators only, not as content for this file.

- AUDNZD
- CHN50U
- Sentinel USDCHF
- ORATS short-vol strangles
- Aegis SHORT v0.1
- Guardian-on-USOIL

When the next closure note appends to this registry, that closure's author writes the relevant entry above this list and removes the corresponding bullet.

---

### Aegis→6J prop-reconstruction Wave-1 sizing/EOD-fill sweep × 6J — FALSIFIED (H-SWEEP Stage-1)

**Rejection scope:** the Aegis→6J prop-reconstruction pre-reg's Stage-1 H-SWEEP path — the
frozen Wave-1 grid (`c01`–`c12`, 9 unique sha256 panels after operator-confirmed
byte-identical collapses) of `max_contracts` × `risk_pct_display` × `eod_fill_deadline_et`
sizing/EOD-fill variants of the locked Aegis v0.3 mechanism on CME **6J**, scored against
the pinned 2022-01-12→2024-12-31 selection window under hard filters (a)–(e) — not 6J the
instrument, not the Aegis→6J native-futures v0.3 mechanism finding (untouched), not the
Class-S venue/sizing-reconstruction candidate class generally, not locked CFD Aegis v4.3.
**Closure date:** 2026-07-16
**Authoritative artifact:** [`2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified`](briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md) ·
[`SWEEP_LOG`](../lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md) ·
[`prereg (FROZEN)`](briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md)
**Closure basis:** 0/12 Wave-1 cells clear the frozen hard-filter set. Filters (a)
overnight-holds = 0%, (a2) exit fills ≤ cell deadline, (c) selection-window maxDD ≤ 6%
(measured 0.49–1.24%), and (e) holdout-window net ≥ 0 **PASS on all 12 cells**; filter
**(d) selection-window N ≥ 80 FAILS on all 12** — the pinned 2022-01-12→2024-12-31 window
yields only 73 trades (cap3/cap5@0.25% cells) or 74 trades (cap5/8@≥0.40% cells) against a
full-span N of 129–130 (Stage-0's own N≥80 envelope check PASSed at 130 using the *full*
2022-01-12→2026-07-15 span — the selection-window truncation, not the mechanism, produces
the miss). The mechanical max-mean-quantity selection rule was never reached (zero
survivors to rank); Stage-2 H-SOLO not authorized.
**Surviving finding (NOT rejected):** 6J instrument standing; the Aegis→6J native-futures
v0.3 mechanism finding cited in this pre-reg's own Rule-0 reads (`ops/instruments/6J.md`
J1: PF 2.318 / EOD-flat 60.0% of net) — untouched, not itself re-tested by this sizing
sweep; the Class-S venue/sizing-reconstruction candidate class generally (candidate #1
MYM+MNQ Part A DISCHARGED separately, Tradeify 2.65% / MFFU 2.64%) — ⚠ that discharge was
**WITHDRAWN 2026-07-22** under corrected eval-lock geometry; do not cite these figures as
current, see [S4 discharge-withdrawal ADR](adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md);
locked CFD Aegis v4.3;
Stage-0 ENVELOPE-YES baseline (`68f0e`, N=130 full-span) as measurement.
**Re-proposal bar:** a **fresh** pre-registration (this one stays closed per Known Trap
#12) that either sources a materially longer/deeper 6J export to raise the realized
selection-window trade count, or independently pre-declares its own selection-window/N-bar
**before** any cell is run — not derived post-hoc from this sweep's realized 73–74 count.
**Not** an in-place amendment of N≥80 or the 2022-01-12→2024-12-31 window on this pre-reg,
**not** picking a "best" cell by PF / expectancy / full-span N, and **not** treating the
0.40%≡0.55% sizing-profile degeneracy as license to retune BE/SL/TP/ATR.

<!-- concept-intake-entry mechanism_family="aegis-6j-sizing-eod-fill-wave1-sweep" instrument="6J" rejection_reason="Stage-1 H-SWEEP FALSIFIED: 0/12 Wave-1 cells clear hard filters (a)-(e); filter (d) sel N>=80 FAILS all 12 (sel N=73-74 vs full-span N=129-130 on pinned 2022-01-12-2024-12-31 window; Stage-0 envelope N>=80 PASSed at full-span 130); all other filters PASS all 12; mechanical max-mean-qty rule never reached (0 survivors)." harness_disposition_ref="Aegis-6J Wave-1 SWEEP_LOG (lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md)" date="2026-07-16" class="stage1-fail-n-gate" role_tested="venue-sizing-selection" falsifier_failed="Stage-1 hard filter (d) sel N>=80 FAIL all 12 cells (sel N 73-74 < 80; full-span N 129-130)" addback_condition="fresh pre-reg with an independently pre-declared selection-window/N-bar (not derived post-hoc from this sweep's 73-74 count) or a materially longer 6J export -- NOT in-place N-bar/window amendment (Trap #12), NOT best-of-12 pick by PF/expectancy/full-span N" -->

### Aegis→6J v0.3 native-venue solo reconstruction (Stage-2 H-SOLO) — FALSIFIED

**Rejection scope:** the Class-S venue/sizing reconstruction of locked Aegis v4.3 → CME **6J**
native futures, tested **solo** (no MYM/MNQ compose) as Stage-2 H-SOLO Part A on the v2.1
tie-break winner cell **c05** (`max_contracts=8` / `risk_pct_display=0.40%` /
`eod_fill_deadline_et=16:00`; panel sha `ED91CD2D5D40`) under the v2 / v2.1 / v2.2 pre-reg
chain — not the locked Aegis v4.3 CFD strategy on USDJPY (untouched), not 6J the instrument,
not the other Wave-1 cells individually, not the composed Aegis+MYM+MNQ book (Stage-3, never
reached — the winner expression closes here).
**Closure date:** 2026-07-16
**Authoritative artifact:** [`2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md`](briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md) ·
[`RESULTS.md`](../lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md) ·
[`v2.2 native-guard prereg`](briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.2-1r-native-guard-prereg.md)
**Closure basis:** frozen gate 2026-07-13 (Part A: bust ≤ 3.0% ∧ P(pass) ≥ 50%, Run-2, seeds
42/123/2026, 10k×3, horizon 1500, `dd_protection` OFF) run on the native c05 $100K daily book
(n=128 trades, span 2022-01-12→2026-06-22, envelope YES, net_static $13,736.16, 1R median $87
diagnostic-only / 0 full-stops above $1,000): **both** required firms FAIL Part A —
Tradeify_Select_100K and MFFU_Rapid_100K each show `bust_trailing` **0.0641** (6.41%, more
than double the 3.0% ceiling) while `bust_daily` / `bust_static` / `bust_inactivity` are all
0.0 (the **trailing**-DD rule alone kills it); `pass_rate` **0.9327** clears the 50% floor on
both, so the shortfall is on the bust ceiling only, not participation. v2.2's native-path
1R-guard re-spec (hard-fail → non-gating median diagnostic) is confirmed **not** load-bearing
on this outcome — 1R is not a scoring input on the native-no-rescale path, so the guard-drop
could not and did not bias the verdict.
**Surviving finding (NOT rejected):** locked Aegis v4.3 on USDJPY (parameter axis untouched);
6J the instrument (venue-legal; occupancy released 2026-08-12 for non-Striker research); the
Class-S venue/sizing-reconstruction candidate route itself (ADR 2026-07-14 — Class-S candidate
#1 MYM+MNQ separately DISCHARGED Part A with its own regime-fragile caveat, **since WITHDRAWN
2026-07-22**); the Stage-1-v2
window-realignment fix (reachability defect correctly repaired, N≥80 retained not lowered,
12/12 cells honestly cleared); four-firms ADR §4 discharge — ⚠ **WITHDRAWN 2026-07-22**; current
state is zero Part A clearers at any frozen tier, see
[S4 discharge-withdrawal ADR](adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md); self-funded
Aegis→M6J scale-path (PARKED separately the same day, not by this Part A result).
**Re-proposal bar:** new mechanism evidence — a demonstrably different **trailing-DD
loss-side shape** on a genuinely **native** (non-rescaled) Aegis-6J book, or a venue class
whose trailing-survival geometry differs from Tradeify/MFFU's EOD-trailing rule. **NOT**
reweighting c05's risk%/cap or swapping its fill deadline (forbidden by the closure itself),
**NOT** selecting a different Wave-1 cell on sizing/fill alone (all share the same v0.3
mean-reversion/spot-inversion signal and loss distribution), **NOT** composing with MYM+MNQ to
dilute the standalone bust rate, **NOT** re-reading pass≈93% as a soft pass against the frozen
3.0% ceiling, **NOT** re-litigating the v2.2 1R guard-drop as able to change the MC outcome.

<!-- concept-intake-entry mechanism_family="aegis-6j-native-venue-solo-reconstruction" instrument="6J" rejection_reason="H-SOLO Part A FALSIFIED: both required firms (Tradeify_Select_100K, MFFU_Rapid_100K) bust_trailing 0.0641 (6.41%) vs 3.0% ceiling on c05 native $100K panel (n=128, Run-2 seeds 42/123/2026); pass_rate 0.9327 clears 50% floor; bust_daily/static/inactivity all 0.0 -- trailing-DD rule alone is the killer; v2.2 1R guard-drop confirmed not load-bearing (1R not a scoring input on native-no-rescale path)." harness_disposition_ref="Stage-2 H-SOLO RESULTS.md (lab/archive/class_s_aegis_solo_scoring_2026-07-16/RESULTS.md)" date="2026-07-16" class="trailing-dd-survival-failure" role_tested="sizing/venue-reconstruction (solo book, no compose)" falsifier_failed="Part A bust ceiling: bust_trailing 0.0641 vs 0.03 ceiling on both required firms (Run-2)" addback_condition="new mechanism evidence: different trailing-DD loss-side shape on a native non-rescaled Aegis-6J book, or a venue class with different trailing-survival geometry -- NOT c05 risk%/cap reweight, NOT a different Wave-1 cell on sizing/fill alone, NOT MYM+MNQ compose to dilute bust, NOT re-reading pass~93% as soft pass" -->

### S-MYM-ORC-02 session-aware opening-range continuation × MYM — FALSIFIED (development)

**Rejection scope:** the `S-MYM-ORC-02` exact frozen construct — long-only CBOT **MYM** 15m
opening-range continuation (OR = 09:30+09:45 bars; entry on the first 10:00–11:45 ET bar closing
above OR-high; 2.00×ATR(11) stop; one 100%-add at +1.00R; 4.00R target; 12-bar max hold; exact
53-date session-aware force-flat calendar; `K_reconstruction=2`) as frozen in
[`PREREG`](briefs/pre-registration/2026-07-16-striker-mym-reconstruction-candidate-2-prereg.md) —
not MYM the instrument, not the Striker→MYM reconstruction programme generally (a fresh
candidate #3 remains available under new operator authorization), not the locked Striker DJ30
v4.5 / NAS100 v1 book, not `S-MYM-ORC-01` (separately closed `AMBIGUOUS`).
**Closure date:** 2026-07-16
**Authoritative artifact:** [`2026-07-16-striker-mym-reconstruction-candidate-2-falsified`](briefs/closures/2026-07-16-striker-mym-reconstruction-candidate-2-falsified.md) ·
[`DEVELOPMENT_RESULTS.md`](../lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/DEVELOPMENT_RESULTS.md)
**Closure basis:** the valid development-only run (2020-07-01→2023-12-31, N=403 completed base
trades; D0 Step-0 integrity and D1 N≥120 both PASS) failed seven of the nine remaining frozen
hard gates: D2 opening-anchor placebo p=0.2144 (gate requires p &lt; 0.05 across 10,000 date-wise
anchor reassignments); D3 gross expectancy / mean actual cost_R = 0.6929× (gate requires ≥
4.00×); D4 net expectancy −0.0210R with net PF 0.9514 (gate requires net &gt; 0R and PF ≥ 1.25);
D5 stationary-bootstrap 95% CI for mean net R = [−0.1221, 0.0806], lower bound negative (gate
requires lower bound &gt; 0); D6 first-half/second-half net expectancy −0.0367R / −0.0052R, both
negative (gate requires both &gt; 0R); D7 drop-top-five-trades net expectancy −0.0673R (gate
requires &gt; 0R); D8 max closed-equity drawdown 6.625% (gate ceiling 6.0%). D9 execution
integrity PASSed (0 fills after scheduled force-flat across 387 standard / 16 allowlisted-session
trades; max 34 contracts; 0.0% quantity-zero skip rate). Under the frozen §6.4 verdict table, any
one valid D1–D9 failure is terminal `FALSIFIED`; the untouched 2024-01-01→2026-06-30 holdout
(H0–H9) was never opened.
**Surviving finding (NOT rejected):** MYM instrument standing is untouched (the disclosed prior
look — the R5 mapped edition, OOS PF 2.038 / preservation ratio 0.559 on a different, excluded
parameter set — is neither retested nor contradicted here); the session-aware 53-date force-flat
calendar repair mechanism itself worked as designed (0 fills after scheduled force-flat on both
standard and allowlisted-early-close sessions) and is reusable by any future MYM candidate; the
Striker→MYM reconstruction programme remains open to a fresh candidate #3 under new
authorization; locked Striker DJ30 v4.5 / NAS100 v1 parameters untouched.
**Re-proposal bar:** genuinely new mechanism evidence for a distinct entry construct (different
opening anchor, breakout definition, or reference class) under a fresh candidate ID and fresh
signed pre-registration — **not** a retune of the 2.00×ATR stop / 4.00R target / add threshold,
**not** a lower-cost model, **not** promoting one of the six placebo-null opening anchors
(09:45–11:00 ET, pre-registered as nulls, not candidate variants) into a rescued signal, and
**not** deleting losing dates, years, or force-flat trades to pass D6–D8.

<!-- concept-intake-entry mechanism_family="mym-opening-range-continuation" instrument="MYM" rejection_reason="FALSIFIED at development: D2 placebo p=0.2144 (>=0.05); D3 gross/cost_R=0.6929x (<4.00x); D4 net expectancy -0.0210R, PF 0.9514 (PF<1.25); D5 95% CI [-0.1221,0.0806] lower<0; D6 half-window -0.0367R/-0.0052R both negative; D7 drop-top-5 -0.0673R; D8 max DD 6.625% (>6.0%). D0/D1/D9 PASS, N=403. Holdout never opened." harness_disposition_ref="S-MYM-ORC-02 DEVELOPMENT_RESULTS.md (lab/analysis/striker/striker_mym_reconstruction_candidate1_2026-07/DEVELOPMENT_RESULTS.md)" date="2026-07-16" class="edge-failure" role_tested="entry" falsifier_failed="D2 placebo p>=0.05; D3 gross/cost<4.00x; D4 net<=0R/PF<1.25; D5 CI lower<=0; D6 both half-windows negative; D7 drop-top-5<=0; D8 DD>6.0%" addback_condition="new mechanism evidence for candidate #3 (distinct entry construct) + fresh operator authorization + fresh frozen pre-registration — NOT stop/target/add retune, NOT lower-cost model, NOT promoting a placebo-null opening anchor, NOT date/year deletion" -->

### Guardian→MGC transfer cell (R7 / b8) — DEAD(N-SURV)

**Rejection scope:** the Guardian Gold v5.5 → MGC venue-transfer cell (execution-mechanics
port only; locked parameters untouched), not Guardian-on-XAUUSD and not MGC-the-instrument.
**Closure date:** 2026-08-11
**Authoritative artifact:** [`docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) ·
[`cell PREREG (retroactive)`](briefs/pre-registration/2026-08-11-guardian-mgc-transfer-cell-prereg.md) ·
[`b8`](pursuits/b8-guardian-mgc-transfer-lane.md)
**Closure basis:** `nsurv_channel.py` on the v0.3 native MGC1! panel (N=329 / daily n=276)
against `Tradeify_Select_100K` at the frozen 2026-07-13 floors (bust ≤3.0% ∧ P(pass)≥50%).
Bust **42.2%** full / **72.4%** H1 / **16.5%** H2 — 5.5×–24× over ceiling on every
partition. Same trailing-survival failure class as Aegis→6J J4b, more severe. Two
disclosed caveats (unpre-registered half-boundary; AE-approximated `intraday_low`) keep
the score exploratory-grade; the margin settles the qualitative DEAD.
**Surviving finding (NOT rejected):** MGC remains venue-legal / instrument-lane eligible;
Guardian v5.5 on XAUUSD is untouched. ⚠ Q-TXG-1 lane later **FALSIFIED-at-walls** (operator A, 2026-08-12) — further transfer elections under that Q-ID are barred; see lane row above.
**Re-proposal bar:** new mechanism evidence (fresh cell PREREG + operator election under
Q-TXG-1 or equivalent) — **not** locked-parameter retune, **not** re-reading the
AE-approximated score, **not** amending the 3.0% floor.

<!-- concept-intake-entry mechanism_family="guardian-v5.5-venue-transfer-port" instrument="MGC" rejection_reason="DEAD(N-SURV): nsurv_channel.py on v0.3 native MGC1! panel (N=329 trades / daily n=276) vs Tradeify_Select_100K frozen floors (bust ≤3.0% ∧ P(pass) ≥50%); bust 42.2% full / 72.4% H1 / 16.5% H2 — 5.5×–24× over ceiling on every partition; exploratory grade (AE-approximated intraday_low; unpre-registered half-boundary), margin-decisive" harness_disposition_ref="nsurv_channel.py exploratory cell score (docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md; no lab/analysis RESULTS artifact — K=1 cell score, no manifest/pull)" date="2026-08-11" class="dd-survival-failure" role_tested="venue-transfer (execution-mechanics port; N-SURV gate)" falsifier_failed="any partition busts >3.0% or P(pass) <50% — all three partitions failed the bust ceiling (42.2/72.4/16.5% vs 3.0%)" addback_condition="new mechanism evidence (fresh cell PREREG + operator election under Q-TXG-1 or equivalent) — NOT locked-parameter retune, NOT re-reading the AE-approximated score, NOT amending the 3.0% floor" -->

### Striker DJ30 → MNQ sibling-swap (Q-TXG-1 cell #2) — DEAD(N-SURV)

**Rejection scope:** the Striker DJ30 v4.5 → CME **MNQ** cross-underlying sibling-swap cell
(execution-mechanics port only; locked parameters untouched) — not MNQ the instrument, not
the Q-TXG-1 lane generally, not Striker-on-DJ30 (home identity), and not the WITHDRAWN(F1)
striker×MYM redeploy.
**Closure date:** 2026-08-12
**Authoritative artifact:** [docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md](briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) ·
[cell PREREG](briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md) ·
[manifest](../discovery_manifests/q_txg1_striker_mnq_20260812.json)
**Closure basis:** native-TV panel cost gate **PASS_COST** (N=222 legs; static-equity recompute
OK, max|Δ|≈0; Net +$22,789.58; PF 1.308; WR 62.61%; mean_net_r **0.0419** > required_net_r
**0.03**). Then `nsurv_channel.py` on the bar-derived `MNQ_M15` daily series (n=164 business
days, 4 post-panel days dropped for missing bar coverage; bars SHA `6c86f41a…e00a`) against
`Tradeify_Select_100K` at the frozen 2026-07-13 floors (bust ≤3.0% ∧ P(pass)≥50%): full bust
**98.13%** / pass 1.87% (n=164); H1 bust **96.76%** / pass 3.24% (n=82); H2 bust **99.37%** /
pass 0.63% (n=82) — every partition fails, ~32×–33× over the 3.0% ceiling. N-SURV FAIL.
**Surviving finding (NOT rejected):** MNQ instrument standing and ENV-1 lane eligibility beyond
this cell; Striker DJ30 v4.5 on its home DJ30/MYM locked-book identity is untouched; the
execution-mechanics port itself cleared the cost gate — only the trailing-DD survival wall
killed it; sibling cell #1 (`striker_nas100×MYM`, DEAD(cost)) is adjudicated separately, not
by this row. ⚠ The Q-TXG-1 lane itself later closed FALSIFIED-at-walls (operator elected CLOSE,
2026-08-12) — further transfer elections under that Q-ID are barred; see the lane-level row
above.
**Re-proposal bar:** subsumed by the lane-level Q-TXG-1 FALSIFIED-at-walls bar above (different
loss-side shape or different venue-class survival geometry) — not a locked-parameter retune,
not amending the 3.0% floor, not inventing an ENV-1 panel N, not a silent third election.

<!-- concept-intake-entry mechanism_family="striker-dj30-v4.5-cross-underlying-sibling-swap" instrument="MNQ" rejection_reason="DEAD(N-SURV): cost gate PASS (N=222, Net +$22,789.58, PF 1.308, mean_net_r 0.0419 > required 0.03) but nsurv_channel.py FAIL on bar-derived MNQ_M15 (n=164 bdays) at Tradeify_Select_100K frozen floors (bust<=3.0% AND P(pass)>=50%) -- full bust 98.13%/pass 1.87%, H1 bust 96.76%/pass 3.24%, H2 bust 99.37%/pass 0.63%, ~32x-33x over ceiling every partition" harness_disposition_ref="Q-TXG-1 striker×MNQ RESULTS + PANEL_SCORE.json (lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/RESULTS.md)" date="2026-08-12" class="portfolio-fit" role_tested="entry" falsifier_failed="N-SURV floor bust<=3.0% AND P(pass)>=50% at Tradeify_Select_100K -- full/H1/H2 all FAIL (bust 98.13%/96.76%/99.37%), ~32x-33x over ceiling every partition" addback_condition="a validated counterbalance or venue-class whose survival geometry clears the trailing-DD wall (re-MC <= ceiling) -- NOT a locked-parameter retune, NOT amending the 3.0% floor, NOT inventing an ENV-1 panel N, NOT a silent third election under Q-TXG-1 (subsumed by the lane-level FALSIFIED-at-walls bar)" -->

### Striker NAS100 → MYM sibling-swap (Q-TXG-1 cell #1) — DEAD(cost)

**Rejection scope:** the Striker NAS100 v1 → CBOT MYM cross-underlying sibling-swap cell
(execution-mechanics port only; locked parameters untouched), not Striker-on-NAS100 and not
the WITHDRAWN(F1) striker_nas100×MNQ redeploy.
**Closure date:** 2026-08-12
**Authoritative artifact:** [docs/briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md](briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) ·
[cell PREREG](briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) ·
[manifest](../discovery_manifests/q_txg1_striker_nas100_mym_20260812.json)
**Closure basis:** native-TV panel cost FAIL vs frozen `required_net_r` 0.06 / `port_must_beat`
(N=190; Net +$4,356.40; mean_net_r **0.0129** < 0.06; PF 1.110; WR 53.68%; static-equity
recompute OK, max|Δ|~0). N-SURV not reached — cost gate closed the cell first.
**Surviving finding (NOT rejected):** MYM instrument standing (killing MYM the instrument is
not licensed by this cell result); Striker NAS100 on its home instrument NAS100 untouched; the
WITHDRAWN(F1) striker_nas100×MNQ redeploy unaffected. ⚠ Q-TXG-1 lane later FALSIFIED-at-walls
(operator election (A) CLOSE, 2026-08-12) — further transfer elections under that Q-ID are
barred; see lane row above.
**Re-proposal bar:** subsumed by the lane-level Q-TXG-1 FALSIFIED-at-walls bar above (different loss-side shape or different venue-class survival geometry) — not a locked-parameter retune, not amending `required_net_r`, not firm-shopping, not a silent third election.

<!-- concept-intake-entry mechanism_family="striker-nas100-cross-underlying-sibling-swap" instrument="MYM" rejection_reason="DEAD(cost): native-TV panel (N=190) Net +$4,356.40 but mean_net_r 0.0129 < required_net_r 0.06 (port_must_beat; ~4.6x below cost-tax floor); PF 1.110; WR 53.68%; static-equity recompute OK (max|delta|~0). N-SURV not reached (cost gate closed the cell first)." harness_disposition_ref="Q-TXG-1 cell #1 PANEL_SCORE.json (lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/PANEL_SCORE.json)" date="2026-08-12" class="venue-cost-constraint" role_tested="entry" falsifier_failed="cost-tax floor: mean_net_r 0.0129 < required_net_r 0.06 (net>0 alone insufficient per PREREG §4 / design §5 step4)" addback_condition="subsumed by lane-level Q-TXG-1 FALSIFIED-at-walls bar — new mechanism evidence with a different loss-side shape or different venue-class survival geometry — NOT locked-parameter retune, NOT amending required_net_r, NOT firm-shopping, NOT a silent third election" -->

### H-FBEIA-1 (F-B) EIA post-release unconditional reversal × CL — SCREEN-FAIL (informed-flow)

**Rejection scope:** the H-FBEIA-1 / F-B `eia-postrelease-reversal` PRIMARY construct on NYMEX **CL** (CL.c.0 continuous, 1m; fade `-sign(m0)` where `m0` is the 10:30→10:35 ET EIA-release log-return, entered 10:35 ET, held to 10:50 ET; K=1) as pre-registered in [`fb_eia_cl_reversal`](../discovery_manifests/fb_eia_cl_reversal.json) — not CL the instrument, not the EIA inventory-*surprise*-conditioned expression of the same release (never tested here; per the closure it is the surprise number, not the realized price move, that carries the 25.6 bp effect), and not the sibling Q-BOOKFIT-1 F-A (ZN auction) / F-C (carry) forks or the Q-BOOKFIT-1 book-*fit* (risk-geometry) result for this same expression, which is a separate axis that PASSED (ρ 0.615, risk-N_eff Δ +0.945) and stands undisturbed.
**Closure date:** 2026-07-20
**Authoritative artifact:** [`H-FBEIA-1-closure-screen-fail`](briefs/closures/H-FBEIA-1-closure-screen-fail.md) · [`RESULTS`](../lab/archive/q_fbeia_1_2026-07/RESULTS.md) · manifest [`fb_eia_cl_reversal`](../discovery_manifests/fb_eia_cl_reversal.json)
**Closure basis:** N=445 EIA Weekly Petroleum Status Report events, CL.c.0 ohlcv-1m (Databento GLBX.MDP3, est+billed $0.00), IS era 2010-06-06→2018-12-31. Faithfulness anchor: release reaction |m0| (10:30→10:35 ET) = **25.6 bp**, matching the published Rousse-Sévi (2019) ~25 bp conditional effect — confirms correct event dating and a real underlying mechanism. PRIMARY unconditional reversal (fade m0, 10:35→10:50 ET): δ = **−1.163 bp**, σ 50.0 bp, δ/σ **−0.0233**, t **−0.49**, two-sided p **≈0.623–0.624**. SANITY unconditional long (10:30→10:45 ET): δ = −1.888 bp, t −0.68 (≈0, consistent with surprise-symmetry). Manifest survivors **0/0/0** at naive/Bonferroni/BH. **Req-4 power FAIL** (|δ/σ| 0.0233 vs the 0.122 floor) and **Req-5 cost-law FAIL** (|δ| 1.16 bp vs the 6–10 bp CL round-trip hurdle) — both fail by roughly an order of magnitude. K=1 banked (`register_search` opened before any return was computed; expression frozen in the extraction-script header).
**Surviving finding (NOT rejected):** CL instrument standing (open to other constructs, including the separately-scored Q-BOOKFIT-1 F-C carry fork on the same instrument family); the Q-BOOKFIT-1 book-*fit* (risk-geometry) result for this same expression — ρ 0.615, risk-N_eff Δ +0.945, PASS — is a different axis (portfolio-composition coordinate, not edge) and is untouched by this edge-side rejection; the EIA release itself is a real, correctly-dated 25.6 bp event (faithfulness confirmed) — only the *unconditional* fade/continuation trade around it is dead; `strategy_harvest.md` Requirement-2's informed-flow guard is corroborated, not created, by this instance (this is its first confirmed worked example; the later NG-EIA-1 and Q-MCLTAS-1 closures both cite it as precedent).
**Re-proposal bar:** genuine access to the EIA inventory-*surprise* number (i.e., an actually informed/conditional expression that trades the surprise, not the realized post-release price) that then clears its own cost-law and power floors — NOT a retune of the m0 window, the 10:35→10:50 hold, the σ/δ normalization, or a re-run of the unconditional fade/continuation pair (continuation = −reversal was already scored here and is equally sub-cost).

<!-- concept-intake-entry mechanism_family="eia-postrelease-reversal" instrument="CL" rejection_reason="SCREEN-FAIL (informed-flow): unconditional PRIMARY reversal (fade 10:30-10:35 ET release reaction m0, hold 10:35-10:50 ET) delta=-1.163bp, sigma=50.0bp, delta/sigma=-0.0233, t=-0.49, two-sided p=0.623-0.624 on N=445 EIA events. Req-4 power FAIL (0.0233 vs 0.122 floor). Req-5 cost-law FAIL (1.16bp vs 6-10bp CL RT hurdle). 0/0/0 manifest survivors naive/Bonferroni/BH. Faithfulness anchor |m0|=25.6bp matches Rousse-Sevi(2019) ~25bp conditional effect -- event dating and mechanism confirmed real; the null is on the UNCONDITIONAL edge only. SANITY unconditional long delta=-1.888bp t=-0.68 (~0, surprise-symmetry)." harness_disposition_ref="F-B eia-postrelease-reversal manifest (register_search open, K=1; discovery_manifests/fb_eia_cl_reversal.json; lab/archive/q_fbeia_1_2026-07/eia_results.json)" date="2026-07-20" class="screen-fail-informed-flow" role_tested="entry" falsifier_failed="Req-4 power |delta/sigma| 0.0233 vs 0.122 floor; Req-5 cost-law |delta| 1.16bp vs 6-10bp hurdle; two-sided p=0.623-0.624; 0/0/0 manifest survivors" addback_condition="genuine EIA inventory-surprise-conditioned expression (new data input) clearing cost-law + power -- NOT a m0-window/hold retune, NOT a re-run of the unconditional fade/continuation pair" -->

### F-C carry-timing (own-carry-sign) × 6E/6J/CL — SCREEN-FAIL (effect absent)

**Rejection scope:** the F-C pre-committed **own-carry-sign carry-timing** construct under **H-FCCARRY-1** — per-instrument front−second carry sign as the timing signal, monthly rebalance, equal-weight combined portfolio across **6E/6J/CL** (one combined return series, K=1), as frozen in [`extract_carry_delta.py`](../lab/archive/q_fccarry_1_2026-07/extract_carry_delta.py) header + manifest `fc_carry_6e6j6cl` — not 6E/6J/CL the instruments, not carry as a factor in general, and not Q-BOOKFIT-1's risk-geometry PASS for this fork (ρ 0.295), which this does not disturb.
**Closure date:** 2026-07-20
**Authoritative artifact:** [`H-FCCARRY-1-closure-screen-fail`](briefs/closures/H-FCCARRY-1-closure-screen-fail.md) ·
[`carry_results.json`](../lab/archive/q_fccarry_1_2026-07/carry_results.json) ·
[manifest `fc_carry_6e6j6cl`](../discovery_manifests/fc_carry_6e6j6cl.json)
**Closure basis:** the pre-committed combined portfolio (N=103 months, 2010-06-06→2018-12-31 IS)
earns δ=6.75 bp/mo on σ=253.3 bp/mo, δ/σ=0.0267 — **Req-4 power FAIL** (≪ the 0.122 threshold);
annualized Sharpe **0.092**; t=0.27, one-sided p=**0.394**. Manifest survivors 0/0/0 at naive-α /
Bonferroni / BH. Per-leg Sharpe all small-positive (6E 0.058 / 6J 0.112 / CL 0.041) — the M-15
faithfulness check confirms the null is real, not a sign-inversion artifact (CL front-month
reproduces the known 2014–2016 oil-crash decline, ~$105→~$31). Req-5 cost-law never reached —
moot, no edge to charge cost against. K=1 banked.
**Surviving finding (NOT rejected):** 6E/6J/CL instrument standing; carry as a factor class in
general — a **cross-sectional** carry factor (rank a broad universe, long top / short bottom) or a
magnitude-weighted timing rule is a distinct, unpre-registered hypothesis; Q-BOOKFIT-1's RESOLVED
risk-geometry PASS for this fork (F-C ρ 0.295, risk-N_eff Δ +0.321 at the 0.37% reference weight —
"the risk geometry fits," never "edge exists") stands untouched; F-A (H-ZNAUC-1, separate Stage-2
cost-wall death) and F-B (CL EIA, formally un-run) as distinct, separately-dispositioned forks.
**Re-proposal bar:** new mechanism evidence — a **cross-sectional** carry factor or a
magnitude-weighted timing rule, each requiring its own pre-registration and K — **not** a re-run
or parameter retune of this own-carry-sign construction, and not a wider instrument grid on the
same construction (re-running variants until one works is the multiplicity the K-ledger forbids,
per the closure's own Trap #12 note).

<!-- concept-intake-entry mechanism_family="carry-timing-own-sign" instrument="6E/6J/CL (combined portfolio)" rejection_reason="SCREEN-FAIL (effect absent): pre-committed combined carry-timing portfolio N=103mo (2010-06-06:2018-12-31) delta=6.75bp/mo sigma=253.3bp/mo delta/sigma=0.0267 far below Req-4 0.122; Sharpe_ann 0.092; t=0.27 one-sided p=0.394; manifest survivors 0/0/0 naive/Bonferroni/BH. Per-leg Sharpe all small-positive (6E 0.058/6J 0.112/CL 0.041); M-15 faithfulness confirms real null (CL front-month reproduces 2014-16 oil crash ~$105->~$31). Req-5 cost-law never reached (moot)." harness_disposition_ref="H-FCCARRY-1 carry_results.json (lab/archive/q_fccarry_1_2026-07/carry_results.json); manifest fc_carry_6e6j6cl (discovery_manifests/fc_carry_6e6j6cl.json)" date="2026-07-20" class="edge-failure" role_tested="entry(timing)" falsifier_failed="Req-4 power delta/sigma>=0.122" addback_condition="new mechanism evidence: cross-sectional carry factor OR magnitude-weighted timing rule, each with fresh pre-registration and K -- NOT a re-run/retune of this own-carry-sign construct" -->

### H-ZNAUC-1 post-auction dealer-hedging-unwind drift × ZN — SCREEN-FAIL (cost-wall)

**Rejection scope:** the H-ZNAUC-1 primary construct — an **unconditional** long in ZN opened at
the auction-close minute and held over a fixed post-auction window (15/30/60m), scored on the
pre-committed PRIMARY 10-Year-family cohort (verdict-bearing) and SECONDARY all-coupon cohort
(disclosed robustness), as frozen pre-δ in [`extract_delta.py`](../lab/archive/q_znauc_1_2026-07/extract_delta.py)
— not ZN the instrument, not the Treasury-complex generally (ZB/`ORB-ZB-1` and ZF/`RATES-EV-ZF-1`
are separate, independently-dead constructs on other tenors), and not the bid-to-cover-conditional
variant (never run — a distinct F-B informed-flow question, explicitly barred from being read as
this construct's edge).
**Closure date:** 2026-07-20
**Authoritative artifact:** [`H-ZNAUC-1-closure-screen-fail`](briefs/closures/H-ZNAUC-1-closure-screen-fail.md) ·
[`RESULTS`](../lab/archive/q_znauc_1_2026-07/RESULTS.md) ·
[`delta_results.json`](../lab/archive/q_znauc_1_2026-07/delta_results.json)
**Closure basis:** K=0 own-cohort δ-extraction (Databento `ZN.c.0` ohlcv-1m, GLBX.MDP3, IS
2010-06-06→2018-12-31, est+billed $0.00; auction dates from fiscaldata.treasury.gov, free; cohort/
window/gate defined in `extract_delta.py`'s header before any δ was read). PRIMARY 10Y-family
[0→15m] (the gated verdict): N=134, δ = **1.01 bp**, σ=7.29bp, δ/σ=0.139, t=1.61. **Req-5 cost-law
(binding kill):** ZN single-RT ≈1.5bp (1 tick = 1/64 pt = $15.625 ≈1.25bp at the in-era median
price 126.4, + commission) → 4×=**6bp** hurdle; conservative two-RT ≈2.5bp → 4×=**10bp** hurdle.
Every one of the six measured cohort/window cells in `delta_results.json` fails both hurdles:
PRIMARY 0→30m δ=0.28bp, 0→60m δ=1.45bp; SECONDARY all-coupon 0→15m δ=0.39bp, 0→30m δ=0.63bp,
0→60m δ=0.83bp — all **6–10× under**. Req-4 power is a secondary, marginal consideration: the
δ/σ≥0.122 floor was calibrated at the pre-registered N≈259 (Q-INVENTORY-1) and is nominally
cleared at the realized δ/σ=0.139, but at the realized N=134 the power-0.50 break-even rises to
≈0.170 — above the measured margin, and t=1.61 does not clear significance; the cost-wall is
decisive regardless. Direction is positive and confirms the Smales (2021) primary-dealer
short-hedge-unwind mechanism — real in direction, ~6–10× too small to trade net of ZN
microstructure cost. Third Tier-B/C futures event-drift seed (after D5, H-OD-1) to confirm
mechanism direction and die at the identical Stage-2 cost-law.
**Surviving finding (NOT rejected):** ZN instrument standing (family bank stays 0, Req-3 CLEAR);
the Smales (2021) mechanism direction itself (confirmed, just sub-cost); Q-BOOKFIT-1's
composition/book-fit finding (ρ 0.512, risk-N_eff Δ +0.787 — "risk geometry fits" is a separate,
undisturbed claim from "edge exists"); fork **F-C** (carry timing-δ, 6J/6E/CL) — steps up next
per the F-A→F-C→F-B priority order, pending its own family-K operator nod; the bid-to-cover-
conditional variant, never run.
**Re-proposal bar:** new mechanism evidence for a genuinely different ZN construct — e.g. a real,
measured execution cost materially below the modeled 1.5–2.5bp RT, or a distinct non-drift
mechanism — not a window retune (15/30/60m already swept, all fail), not a cross-instrument δ
transplant (forbidden under Req 2), and not reading the bid-to-cover-conditional coefficient as
the tradeable δ (the informed-flow trap the scoping brief's §4 explicitly bars).

<!-- concept-intake-entry mechanism_family="post-auction-dealer-hedging-unwind-drift" instrument="ZN" rejection_reason="SCREEN-FAIL (cost-wall): own-cohort K=0 delta-extraction on native ZN.c.0 (Databento GLBX, $0.00, IS 2010-06-06 to 2018-12-31). PRIMARY 10Y-family [0->15m] N=134 delta=1.01bp sigma=7.29bp delta/sigma=0.139 t=1.61. Req-5 cost-law KILL: ZN RT ~1.5bp single / ~2.5bp two-RT -> 4x hurdle 6bp/10bp; measured delta 6-10x under at every one of 6 cohort/window cells (PRIMARY 0->30m 0.28bp, 0->60m 1.45bp; SECONDARY all-coupon 0->15m 0.39bp, 0->30m 0.63bp, 0->60m 0.83bp - all FAIL). Req-4 power nominally clears the N=259-calibrated 0.122 floor (0.139) but at realized N=134 the power-0.50 break-even rises to ~0.170, above the margin (t=1.61 not significant). Direction confirms Smales (2021) dealer short-hedge-unwind mechanism, real in direction, sub-cost. Third Tier-B/C event-drift seed (after D5, H-OD-1) to confirm mechanism and die at the identical Stage-2 cost-law." harness_disposition_ref="H-ZNAUC-1 delta-extraction (no harness DispositionRecord; lab/archive/q_znauc_1_2026-07/delta_results.json)" date="2026-07-20" class="venue-cost-constraint" role_tested="entry" falsifier_failed="Req-5 cost-law: PRIMARY 0->15m delta 1.01bp vs 6bp/10bp hurdle (6-10x under); all 6 cohort/window cells FAIL" addback_condition="new mechanism evidence for a different ZN construct (materially lower measured cost basis or a distinct non-drift mechanism) - NOT a window retune (15/30/60m already swept), NOT cross-instrument delta transplant, NOT the bid-to-cover-conditional coefficient read as the tradeable delta" -->

### MSL-C1 PDH/PDL failed-break reclaim × MYM — FALSIFIED (explore IS)

**Rejection scope:** the MSL-C1 G0 construct `pdh-pdl-failed-break-reclaim` on CBOT **MYM**
(15m; prior-day RTH PDH/PDL failed-break reclaim; k=1) as frozen in
[`PREREG_G0`](../lab/archive/msl_c1_mym_2026-08/PREREG_G0.md) — not MYM the instrument,
not MSL the channel, not other session-structure fades.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C1-closure-falsified`](briefs/closures/MSL-C1-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md)
**Closure basis:** both arms n≥100, mean net R ≈ −0.18 / −0.11, session-block 95% CI entirely &lt; 0
(FALSIFIED). DELETE PASS both arms (moot). CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** MYM instrument standing; B8 occupancy ADR; MSL channel;
Stage-0/1 door-check discharge for this card.
**Re-proposal bar:** new mechanism evidence — not stop-buffer / overnight-sham / window retune on this G0.

<!-- concept-intake-entry mechanism_family="pdh-pdl-failed-break-reclaim" instrument="MYM" rejection_reason="explore IS FALSIFIED: both arms CI upper < 0 (mean ≈ −0.18/−0.11R)" harness_disposition_ref="MSL-C1 RESULTS_g2 (lab/archive/msl_c1_mym_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms" addback_condition="new mechanism evidence — NOT θ-retune of this G0" -->

### MSL-C2 London-range failed-extension fade × MGC — FALSIFIED (explore IS)

**Rejection scope:** the MSL-C2 G0 construct `london-range-failed-extension-fade` on COMEX **MGC**
(15m; London H/L fade after failed extension; k=1) as frozen in
[`PREREG_G0`](../lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md) — not MGC the instrument,
not MSL the channel, not other session-structure fades.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C2-closure-falsified`](briefs/closures/MSL-C2-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)
**Closure basis:** both arms n≥300, mean net R ≈ −0.18, session-block 95% CI entirely &lt; 0
(FALSIFIED). DELETE FAIL both arms (sham prior-RTH less negative than London-constrained).
CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** MGC instrument standing; MSL channel; Stage-1 screen
arithmetic as a pre-G0 filter (passed here; explore killed).
**Re-proposal bar:** new mechanism evidence (different reference class / direction / TF) —
**not** stop-buffer, rr, or London-window retune on this G0.

<!-- concept-intake-entry mechanism_family="london-range-failed-extension-fade" instrument="MGC" rejection_reason="edge-failure (FALSIFIED): explore IS both arms mean_R≈-0.18, CI entirely <0 (long n327 [-0.287,-0.071]; short n310 [-0.292,-0.075]); DELETE FAIL (sham prior-RTH less negative). CONFIRM unread." harness_disposition_ref="MSL-C2 explore G0 (lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)" date="2026-08-13" class="edge-failure" role_tested="entry" falsifier_failed="both-arms CI upper <0; DELETE Req1a FAIL" addback_condition="new mechanism evidence — NOT stop-buffer/window/rr retune on this G0" -->

### MSL-C3-K2 dual-axis MR-at-level × M2K — FALSIFIED (explore IS; K=2)

**Rejection scope:** the dual-axis G0 on **M2K** licensing both `pdh-pdl-failed-break-reclaim`
and `overnight-range-failed-extension-fade` at `K_intrinsic=2` — not M2K the instrument, not
MSL the channel, not MYM/C1 (already separate).
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C3-K2-closure-falsified`](briefs/closures/MSL-C3-K2-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md) ·
[`PREREG_G0`](../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
**Closure basis:** both axes both arms CI entirely &lt; 0 on IS (A means ≈ −0.15/−0.20R; B ≈ −0.12/−0.11R).
CONFIRM unread; Cap unclaimed; $0/K=0.
**Surviving finding (NOT rejected):** M2K instrument standing; MSL channel; Stage-0/1 screen arithmetic;
estate Cap/DSR/floor ladder unchanged.
**Re-proposal bar:** new mechanism evidence — NOT θ-retune / stop-buffer / silent K=1 drop on this G0.

<!-- concept-intake-entry mechanism_family="pdh-pdl-failed-break-reclaim" instrument="M2K" rejection_reason="explore IS FALSIFIED (C3-K2 Axis A): both arms CI upper < 0 (mean ≈ −0.15/−0.20R)" harness_disposition_ref="MSL-C3-K2 RESULTS_g2 (lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms" addback_condition="new mechanism evidence — NOT θ-retune of this G0" -->
<!-- concept-intake-entry mechanism_family="overnight-range-failed-extension-fade" instrument="M2K" rejection_reason="explore IS FALSIFIED (C3-K2 Axis B): both arms CI upper < 0 (mean ≈ −0.12/−0.11R)" harness_disposition_ref="MSL-C3-K2 RESULTS_g2 (lab/archive/msl_c3_m2k_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms" addback_condition="new mechanism evidence — NOT θ-retune of this G0" -->

### MSL-C3 PDH/PDL failed-break reclaim × M2K — OPERATOR-KILL (B4 declined; pre-G0)

**Rejection scope:** the MSL-C3 card’s unpaid G0 path for `pdh-pdl-failed-break-reclaim` on
**M2K** after Stage-1 PASS — not M2K the instrument, not the mechanism **class**, not MYM/C1.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-C3-closure-operator-kill`](briefs/closures/MSL-C3-closure-operator-kill.md) ·
[`STAGE1`](../lab/archive/msl_c3_m2k_2026-08/STAGE1.md)
**Closure basis:** operator declined B4; no G0 freeze; $0/K=0. Stage-1 screens had PASSed.
**Surviving finding (NOT rejected):** M2K instrument standing; MSL channel; mechanism class
`pdh-pdl-failed-break-reclaim` (available to MSL-C1 on MYM); Stage-0 L3/WSTRUCT/W4 discharge.
**Re-proposal bar:** fresh Stage-1 + new B4 — not a silent revive of this unpaid path.
**Addback closed (does not clear this row):** [`STAGE1_K2`](../lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md) +
[ADR 2026-08-13](adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) +
[`PREREG_G0`](../lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md) → explore
**`FALSIFIED`** both axes ([closure](briefs/closures/MSL-C3-K2-closure-falsified.md)). New mechanism
evidence still required for any further M2K addback of this class.

<!-- concept-intake-entry mechanism_family="pdh-pdl-failed-break-reclaim" instrument="M2K" rejection_reason="operator-kill pre-G0 (B4 declined): Stage-1 PASS but G0 never frozen; slot handed to MSL-C1." harness_disposition_ref="MSL-C3 STAGE1 (lab/archive/msl_c3_m2k_2026-08/STAGE1.md)" date="2026-08-13" class="operator-stop" role_tested="entry" falsifier_failed="n/a — B4 declined" addback_condition="fresh Stage-1 + new B4 GO — NOT silent revive of this unpaid G0 path" -->

### MSL-S2A pullback-failure resumption × MCL — FALSIFIED (explore IS)

**Rejection scope:** the MSL-S2A G0 construct `pullback-failure-resumption` on NYMEX **MCL**
(15m; impulse + failed-pullback resumption; k=1; rr=3; 09:00–14:30 ET) as frozen in
[`PREREG_G0`](../lab/archive/msl_s2a_mcl_2026-08/PREREG_G0.md) — not MCL the instrument,
not MSL the channel, not other continuation classes.
**Closure date:** 2026-08-13
**Authoritative artifact:** [`MSL-S2A-closure-falsified`](briefs/closures/MSL-S2A-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md)
**Closure basis:** N-ACT FAIL (0.511 trades/week &lt; 1). Long FLIP FAIL (join-pullback beat
resumption). DELETE PASS both arms (moot under FALSIFIED). Means negative; CI not entirely
&lt; 0 (n 31/46). CONFIRM unread; Cap unclaimed; $0/K=0. Not `BOOK-CONDITIONAL(cadence)`.
**Surviving finding (NOT rejected):** MCL instrument standing; MSL channel; Stage-1 screen
arithmetic as a pre-G0 filter (passed here; explore killed); DELETE selection vs TOD sham.
**Re-proposal bar:** new mechanism evidence (different reference class / direction / TF) —
**not** I/P-window, stop-buffer, or rr retune on this G0.

<!-- concept-intake-entry mechanism_family="pullback-failure-resumption" instrument="MCL" rejection_reason="explore IS FALSIFIED: N-ACT 0.511 trades/week; long FLIP FAIL (join-pullback +0.047 vs resume -0.175). DELETE PASS both. CONFIRM unread." harness_disposition_ref="MSL-S2A RESULTS_g2 (lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md)" date="2026-08-13" class="explore-falsified" role_tested="entry" falsifier_failed="N-ACT trades/week < 1; long FLIP Req1a FAIL" addback_condition="new mechanism evidence — NOT I/P-window/stop-buffer/rr retune on this G0" -->

### MSL-S2B sweep-failure-filtered-continuation × MYM — SCREEN-FAIL (D2 route-B cheap falsifier)

**Rejection scope:** the ADR 2026-08-16 D2 cheap-falsifier test of *route B* (temporal-selectivity-
as-continuation via the CON-5 pause's own dense-1m-scoped textual opening) for
`sweep-failure-filtered-continuation` × **MYM** 15m — specifically the one operationalization run:
MSL-C1's own PDH/PDL sweep + failed-extension-reclaim signal (`construct_lib.find_failed_extension_signal`)
taken on the **flip** (continuation) side, entered next-bar-open, against S2B's own frozen
placeholder box (40 pt stop / 120 pt target, rr=3, k=1). Not MYM the instrument, not the MSL
channel, not the base MSL-S2B 2026-08-14 `STAGE-1 FAIL` (route) verdict (registered separately,
entry above; unedited by this test — ADR D3 is prospective only), not the CON-5 pause's own
dense-1m lane (untouched), not any other untested operationalization of "sweep-failure gates
continuation."
**Closure date:** 2026-08-17
**Authoritative artifact:**
[`_cheap_falsifier_s2b_con5_d2_2026-08-17_LOG`](../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_s2b_con5_d2_2026-08-17_LOG.md) ·
[`ADR 2026-08-16`](adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) §2 D2 (falsifier spec) ·
[`STAGE1 addendum`](../lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md) ·
[`MSL-S2B-closure-stage1-fail-route`](briefs/closures/MSL-S2B-closure-stage1-fail-route.md) (base
verdict, unedited by this test)
**Closure basis:** IS partition only (panel start .. 2025-08-31; CONFIRM never touched). 1,605
eligible sessions (valid prior-day PDH/PDL); signal fired on 850 (coverage **52.96%**; exits: stop
627 · target 192 · flat 31). Mean signed gross **−1.00 pt** across those 850 signals; WR **25.41%**
(≈ the box's own rr=3 breakeven WR of 25%); gross/(4×RT) **−0.044×** against the ADR's own generous
**+0.5× (11.28 pt)** pass bar (0.5 × 4 × $2.82 RT ÷ $0.5/pt) — a clean, non-marginal `D2_FAIL`. (An
initial run mis-paid the asymmetric 40/120 box via an unmodified C1 path-function bug — corrected
before this result was scored.)
**Surviving finding (NOT rejected):** MYM instrument standing; MSL channel standing; the base
MSL-S2B 2026-08-14 `STAGE-1 FAIL` (route) verdict (registered separately above, unedited — ADR D3
is prospective only); the ADR's own D1 textual-narrow scoping of the CON-5 pause (still stands — a
15m/non-dense-1m card may still invoke route ① via temporal selectivity, subject to this falsifier
gate); the D2 falsifier-gate mechanism itself as a reusable channel tool (this is one gated card's
result, not a verdict on the gate — ADR §4 tracks that separately); MSL-C1's own DELETE PASS
filter-role finding (untouched — this test reused the same underlying signal only on its
flip/continuation *entry* role, not the filter role C1 established).
**Re-proposal bar:** a different entry-trigger operationalization of "trend-continuation gated by
sweep-failure" — a new construct/box pairing run through its own fresh D2-class falsifier — **not**
a re-run of this same C1-flip-signal / 40-pt-stop-120-pt-target pairing, **not** a θ-retune of the
box, **not** treating this FAIL as reopening the base 2026-08-14 Stage-1 FAIL verdict.

<!-- concept-intake-entry mechanism_family="sweep-failure-filtered-continuation" instrument="MYM" rejection_reason="D2 cheap-falsifier route-B closure (ADR 2026-08-16 sec 2 D2): reused MSL-C1's PDH/PDL sweep+failed-extension-reclaim signal on the flip side, S2B's own 40/120 placeholder box, IS-only; 850/1605 eligible sessions fired (coverage 52.96%); mean signed gross -1.00 pt; WR 25.41% (~rr=3 breakeven); gross/(4xRT) -0.044x vs +0.5x (11.28 pt) pass bar. D2_FAIL." harness_disposition_ref="MSL-S2B D2 cheap-falsifier LOG (lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_s2b_con5_d2_2026-08-17_LOG.md)" date="2026-08-17" class="edge-failure" role_tested="entry (route-B/D2 falsifier)" falsifier_failed="ADR 2026-08-16 D2 pass bar: mean signed gross -1.00 pt < +11.28 pt (0.5x4xRT); WR 25.41% ~= rr=3 breakeven; gross/(4xRT) -0.044x" addback_condition="different entry-trigger operationalization of sweep-failure-filtered-continuation (not this C1-flip-signal/40-120-box pairing), tested under its own fresh D2-class falsifier -- NOT a re-run of this signal/box pairing, NOT reopening the base 2026-08-14 Stage-1 FAIL route verdict" -->

### Third-Friday derivative-settlement reversal on MYM

**Rejection scope:** the exact Baltussen/Terstegge/Whelan derivative-payoff-bias expression on native MYM: short the calendar third-Friday 09:30 ET open and cover at 12:00 ET. The overnight Thursday-close→Friday-open spike is a mechanism-faithfulness measurement, not a traded limb.
**Closure date:** 2026-07-21
**Class:** edge-failure (underpowered, unstable) + venue/cost-geometry
**Authoritative artifact:** [`lab/archive/mym_3fps_recon_2026-07/RESULTS.md`](../lab/archive/mym_3fps_recon_2026-07/RESULTS.md) + [`closure`](briefs/closures/MYM-3FPS-1-closure-falsified.md).
**Closure basis:** frozen K=0 native-micro extraction, 2019-05-06→2026-07-21, exact timestamps and no nearest-bar substitutions. Coverage passed (84/87, 96.6%), but the overnight spike was only +1.54 bp (`delta/sigma=0.0256`, power 0.042) and the open-to-noon short only +2.68 bp (`delta/sigma=0.0500`, power 0.067), both far below the frozen 0.2139 standardized-effect floor. The short also failed the Tradeify cost law: +2.68 bp vs 6.57 bp 4× hurdle. Year signs were unstable and the tradable limb was negative in 2019, 2024, 2025, and 2026. The published ~12 bp DJIA effect does not transfer at useful magnitude to the native MYM era.
**Re-proposal bar:** new target-instrument mechanism evidence. NOT a 09:15/09:20 entry, different exit, quarterly/triple-witch subset, MNQ rescue, overnight limb, or pooled-index version; each is a new hypothesis and the first three are precisely the post-result selection moves this probe froze out.

<!-- concept-intake-entry mechanism_family="third-friday-derivative-settlement-reversal" instrument="MYM" rejection_reason="edge-failure + venue/cost-geometry: frozen K=0 native-MYM third-Friday 09:30->12:00 short, n=84/87 exact events (96.6%). Overnight spike +1.54bp, delta/sigma 0.0256, power 0.042; open-to-noon short +2.68bp, delta/sigma 0.0500, power 0.067; both below 0.2139 floor. Cost-law FAIL: +2.68bp vs 6.57bp 4x Tradeify hurdle. Year signs unstable; short negative 2019/2024/2025/2026. Published ~12bp DJIA effect absent at useful magnitude in native MYM era." harness_disposition_ref="MYM-3FPS-1 Phase-0 (K=0 delta extraction; lab/archive/mym_3fps_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure+venue-cost-geometry" role_tested="entry" falsifier_failed="P0.1 overnight delta/sigma 0.0256; P0.2 reversal delta/sigma 0.0500 vs 0.2139 floor; P0.3 +2.68bp vs 6.57bp hurdle" addback_condition="new target-instrument mechanism evidence - NOT timing/exit/expiry-subtype retune, MNQ rescue, overnight limb, or pooled-index variant" config_fingerprint="3fps/MYM.v.0/calendar-third-Friday/short-open09:30ET->12:00ET/cost=Tradeify0.91+1tick-side/feed=Databento-GLBX-MYM.v.0-ohlcv1m-2019-05-06..2026-07-21" -->

### Opening-volume × directional-efficiency pressure map on MNQ/MYM

**Rejection scope:** the continuous BAR EXPORT opening-pressure mechanism — high opening volume as continuation when the first 30 minutes are directionally efficient and as reversal when absorbed into a low-efficiency range — on native MNQ and MYM M15 panels. Not a strategy or entry rule.
**Closure date:** 2026-07-21
**Class:** edge-failure (underpowered / wrong-signed on development)
**Authoritative artifact:** [`lab/archive/opening_pressure_map_2026-07/RESULTS.md`](../lab/archive/opening_pressure_map_2026-07/RESULTS.md) + [`closure`](briefs/closures/OPENPRESS-1-closure-falsified.md).
**Closure basis:** frozen K=0 hash-pinned diagnostic (`MNQ_M15.csv` `ddb14f…e1f7e3ac`, `MYM_M15.csv` `298ab8…f9059c`). Neither instrument passed. MNQ development t=1.53 and pooled t=1.60 (both <2) despite positive slopes and a cost-clearing P90−P10 spread; MYM development slope wrong-signed (−3.63 bp) and predicted spread 1.71 bp below the 6.41 bp 4× Tradeify hurdle. Exactly-zero instruments passed → overall `FALSIFIED` (not AMBIGUOUS).
**Re-proposal bar:** new modality / mechanism evidence (e.g. true order-flow or absorption measures). NOT an RV threshold, alternate opening window, weekday slice, single-instrument selection after seeing the pair, or re-pin to a newer BAR EXPORT panel to rescue the slope.

<!-- concept-intake-entry mechanism_family="opening-volume-directional-efficiency" instrument="MNQ+MYM" rejection_reason="edge-failure: frozen K=0 BAR EXPORT pressure-alignment diagnostic. MNQ FAIL (dev t=1.53, pooled t=1.60 <2); MYM FAIL (dev slope -3.63bp wrong-signed; pred spread 1.71bp < 6.41bp 4x cost). Neither PASS → FALSIFIED." harness_disposition_ref="OPENPRESS-1 (lab/archive/opening_pressure_map_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure" role_tested="mechanism-diagnostic" falsifier_failed="MNQ HAC t<2; MYM wrong-signed + cost FAIL" addback_condition="new modality/mechanism - NOT threshold/window/instrument rescue on same OHLCV" -->

### OR-window net signed aggressor size × MNQ — FALSIFIED (CI includes 0)

**Rejection scope:** the Q-CAPFLOW-1 Cap-spend cell testing OR-window **net signed aggressor
size** (tape-flow Feature A, §2 S3 of the frozen construct: Σ size·(+1 buy-aggressor, −1
sell-aggressor) over prints in `[OR_start, t_trigger)`) against realized R of CME **MNQ**
ORB-MNQ-1 trades, as frozen in [`PREREG`](../lab/archive/mnq_capflow_orb_r_2026-08/PREREG.md)
— not MNQ the instrument, not ORB-MNQ-1 the survivor (lifecycle PARKED, unchanged), not the
resting-L1 order-flow construct (N14), which is a distinct, untouched cell.
**Closure date:** 2026-08-14
**Authoritative artifact:** [`Q-CAPFLOW-1-closure-falsified`](briefs/closures/Q-CAPFLOW-1-closure-falsified.md) ·
[`RESULTS`](../lab/archive/mnq_capflow_orb_r_2026-08/RESULTS.md) ·
[`PREREG`](../lab/archive/mnq_capflow_orb_r_2026-08/PREREG.md)
**Closure basis:** coverage/power cleared (255/255 triggers covered, coverage 1.000 —
VOID-POWER/VOID-COVERAGE not fired). Primary Pearson ρ(A, R) = **+0.020012**; session-block
bootstrap 95% CI **[−0.089845, +0.114398]** includes 0; within-session shuffle placebo |·| p95
= **0.020012**, empirical p = **1.00** (observed ρ indistinguishable from the placebo noise
floor). Halves disagree in sign (H1 ρ=+0.0419, H2 ρ=−0.0067) as a non-reached secondary — the
CI/placebo limb fired first per §5. Cap held: `cap_spent=false`, `k_intrinsic=0`, $0 spend.
**Surviving finding (NOT rejected):** MNQ instrument standing; ORB-MNQ-1 survivor and its
PARKED lifecycle status (untouched); the Cap-reservation seat Q-CAPRES-2 (RESOLVED — discharged
its unpaid score obligation, not consumed); the C11/N14 resting-L1 tripwire (a distinct cell);
other Cap-spend features or survivor-tied questions on this or other survivors.
**Re-proposal bar:** a fresh Cap-reservation GO + Cap-spend GO + new G0/construct testing a
**different feature or different survivor-tied question** — not a retune of the |ρ|≥0.02
magnitude floor, the OR-window definition, or a re-score of this same event set.

<!-- concept-intake-entry mechanism_family="or-window-net-signed-aggressor-size" instrument="MNQ" rejection_reason="Cap-spend cell FALSIFIED: session-block CI95 [-0.089845,+0.114398] includes 0 on rho=+0.020012 (n=255, coverage 1.000); within-session shuffle placebo |.| p95=0.020012, p_emp=1.00 (observed rho indistinguishable from placebo); halves disagree in sign (h1=+0.0419, h2=-0.0067). Cap held, cap_spent=false, k_intrinsic=0." harness_disposition_ref="Q-CAPFLOW-1 RESULTS.json (lab/archive/mnq_capflow_orb_r_2026-08/RESULTS.json)" date="2026-08-14" class="edge-failure" role_tested="correlation/companion (Cap-spend association test, not an ORB entry mechanism)" falsifier_failed="S5 verdict gate: CI95 includes 0 or fails placebo — both fired (CI spans 0; observed |rho| equals placebo p95)" addback_condition="fresh Cap-reservation GO + Cap-spend GO + new G0/construct (different feature or different survivor-tied question) — NOT a retune of the |rho|>=0.02 magnitude floor, the OR-window definition, or this event set" -->

### Q-COMPOSE-1 ORB-MNQ-1 breadth-leg composition × MYM+MNQ Class-S c1 book — FALSIFIED (regime-breadth re-MC)

**Rejection scope:** the Q-COMPOSE-1 pre-registered composed 3-leg book — MYM-Striker @0.70% +
MNQ-Striker @0.37% (both byte-pinned, un-reweighted from Class-S candidate #1) + **ORB-MNQ-1
@0.37%** (SINGLE frozen weight, 1.00× lifecycle, operator-signed §9) — as a book-level
regime-breadth remedy for the 2-leg Class-S c1 book's H1 chop-fragility, at this tested
weight/geometry only. **Not** ORB-MNQ-1 the mechanism (standalone lifecycle standing unchanged),
not MYM/MNQ the instruments, not the c1 book's sizing/haircut lever (which passed), not the
combined composed×haircut arm (never licensed — the haircut single didn't also fail).
**Closure date:** 2026-07-17
**Authoritative artifact:** [`Q-COMPOSE-1-closure-falsified`](briefs/closures/Q-COMPOSE-1-closure-falsified.md) ·
[`RESULTS`](../lab/archive/q_compose_1_2026-07/RESULTS.md) ·
[`pre-reg`](briefs/pre-registration/Q-COMPOSE-1-verdict-preregistration.md)
**Closure basis:** the §4/§6 `FALSIFIED` trigger (H1 headline bust exceeding 3.0% OR
bootstrap-95th bust exceeding 3.0% on every tier) fired on all 4 tiers via **both** limbs: H1
headline bust ranged 54.17% (MFFU_Rapid_100K) to 67.63% (BluSky_Premium_100K); bootstrap-95th
bust ranged 46.80% (MFFU_Rapid_100K) to 59.58% (BluSky_Premium_100K) — 15–23× over the 3.0%
ceiling. Discharge-tier detail vs the 2-leg baseline (`REGIME_GATE.md`): Tradeify_Select_100K
full 2.65%→38.75%, H1 4.37%→54.73%, H2 1.70%→25.84%, boot-95th 10.37%→47.14%; MFFU_Rapid_100K
full 2.64%→38.54%, H1 4.36%→54.17%, H2 ~1.70%→25.79%, boot-95th 10.33%→46.80% — every partition
worse under composition, including full-panel and H2, which the 2-leg book passes. Zero tiers
cleared all four partitions (0 `RESOLVED` clearers). Mechanism, from the §2-required breadth
declaration: dependence N_eff rose 1.9948→2.9502 (Δ+0.9554, near-max correlation breadth) while
risk N_eff stayed flat at 1.9593→1.9628 (Δ+0.0034) — ORB-MNQ-1 alone carries roughly $438/day std
at the $100K basis vs $273/day for the entire 2-leg book (composed roughly $539/day, ~2×),
against the unchanged $3,000 trailing barrier: the added leg is variance-dominant, so correlation
breadth without risk-weight balance did not shrink the dollar-denominated trailing-DD tail.
**Surviving finding (NOT rejected):** MYM-Striker/MNQ-Striker instrument and 2-leg c1 book
standing — the sizing lever passed its own sibling haircut re-MC (WATCH-1 0.50× clears all four
partitions × both discharge tiers) and **was** the c1 book's sole deployable path at the time
(2026-07-17 G8 ratification), independent of this fork. ⚠ Both Striker legs were **WITHDRAWN
2026-08-04** and stay barred from redeploy — there is no live c1 book today; see CLAUDE.md
Live-execution posture. This finding is historical, not a current deployment path. ORB-MNQ-1
standalone lifecycle standing is unchanged —
remains `CANDIDATE @ 1.00×` with its own ADMISSION.md caveats; this closure kills only its role
as a book leg at the tested weight/geometry, it does not demote the candidate. The dependence-vs-risk-N_eff
decomposition itself (check PR(cov), not just PR(corr), before composing) is a portfolio-construction
lesson, not a rejection.
**Re-proposal bar:** new mechanism evidence — a breadth-leg candidate (ORB-MNQ-1 or otherwise)
whose risk N_eff (PR-cov), not just its dependence N_eff (PR-corr), also rises under composition —
i.e. NOT variance-dominant relative to the existing book (daily $ vol materially below the ~2× ORB
showed here) — so diversification can actually shrink the dollar trailing-DD tail. **Not** a
re-tune/re-sweep of ORB's own weight (§5 bars weight iteration on a failed composed candidate — a
failed candidate closes, it does not iterate weight; 0.70%/1.50% were disclosed §7 prior-looks,
never tested arms, and stay untested). **Not** reopening the combined composed×haircut arm — that
arm is licensed only if both singles fail, and the haircut single passed.

<!-- concept-intake-entry mechanism_family="regime-breadth-composition-leg" instrument="ORB-MNQ-1+MYM-Striker+MNQ-Striker (composed 3-leg c1 book)" rejection_reason="composed 3-leg book (MYM@0.70%+MNQ@0.37%+ORB-MNQ-1@0.37%/1.00x lifecycle) FALSIFIED: H1 bust 54.17-67.63% and bootstrap-95th bust 46.80-59.58% vs 3.0% ceiling on all 4 tiers; dependence N_eff rose 1.9948->2.9502 while risk N_eff stayed flat 1.9593->1.9628" harness_disposition_ref="Q-COMPOSE-1 RESULTS (lab/archive/q_compose_1_2026-07/RESULTS.md)" date="2026-07-17" class="regime-remc-falsified" role_tested="portfolio-breadth-leg (book composition, not entry/filter)" falsifier_failed="§4/§6 FALSIFIED trigger: H1 bust > 3.0% OR bootstrap-95th bust > 3.0% on every tier — met on all 4 tiers via both limbs" addback_condition="new mechanism evidence: a breadth leg whose risk N_eff (not just dependence N_eff) also rises under composition, i.e. not variance-dominant vs the book — NOT a re-tune of ORB's weight (failed candidate closes, does not iterate weight, §5), NOT reopening the combined composed x haircut arm (singles didn't both fail)" -->

### Blind high-K discovery-axis mining (Q-GATECART-1 DSR-admission reachability) — FALSIFIED (K-conditional, K=3,177)

**Rejection scope:** the finding that **blind, high-K discovery-axis mining** (K banked at
**3,177** — DISC-CAMP-0's blind matrix-profile search) cannot produce a realistically-demonstrable
single-strategy candidate for the frozen Part-A survivor gate at the $100K band — not the survivor
bust/pass gate itself (3.0% / 50% / 1.0% ceilings, untouched — its own amendment route is its own
close-and-reopen), not `DD_TRIGGER`/`DD_SCALE`, not any specific instrument or mechanism family
(no candidate was ever scored — "N/A" per the closure's Deployability annotation), and not
**low-K (≤441), pre-committed mechanism-first axes** (the HARV lane), which this same finding
leaves open.
**Closure date:** 2026-07-14 (CLOSED-FALSIFIED at Phase 0.5, ahead of the Phase-1 cartography grid
— the grid was never run; the realism-band anchors alone settled it)
**Authoritative artifact:** [`Q-GATECART-1 closure`](briefs/closures/Q-GATECART-1-survivor-gate-cartography.md) ·
[`Q-GATECART-1 brief`](briefs/Q-GATECART-1-survivor-gate-cartography.md) ·
verdict pre-registration §F results annex, frozen `453148a` / §F filled `1367265` — moved into the
LTM corpus same-day (`fad8984`) then pruned at the Great Prune; retrieve via
`git show pre-prune-2026-08-08:docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md`
**Closure basis:** frozen formula (§B, byte-stable through close): a profile is realistic iff
S_floor ≤ annualized Sharpe ≤ Cap, Cap = smallest grid rung ≥ max(S_A, S_B). Measured post-freeze
(§F, 2026-07-14): **S_A = 1.828** (Aegis — max standalone annualized Sharpe of the four locked legs
on the canonical Pepperstone panel; Guardian 1.48, DJ30 1.11, NAS100 1.45; portfolio-of-4 reference
2.80 is *not* S_A — single-leg only). **S_B = 0.85** (top-decile net-of-cost annualized Sharpe from
the multiple-testing-corrected published anomaly/CTA literature; range 0.6–1.05; median
single-strategy ~0.3–0.5). |S_A−S_B| = 0.978 &gt; 0.5 → divergence branch fired, so Cap is
operator-adjudicated within the admissible range **[1.0, 2.0]**. **S_floor = 2.050** at K=3,177 /
V=1/n (production `deflated_sharpe`; robust 2.05–2.06 across the frozen frequency set 0.5–4
trades/day). Every admissible Cap ≤ 2.0 &lt; S_floor 2.05 — the band [S_floor, Cap] is **empty
under every resolution of the divergence branch**, so H-CART's "otherwise" branch fired vacuously
and the Phase-1 grid became moot. The DSR-floor-vs-K scan shows the constraint is K-governed, not
n-governed: floor ≤ Aegis quality (1.83) needs K ≤ 441; ≤ Guardian quality (1.48) needs K ≤ 33; ≤
typical corrected-anomaly quality (1.00) needs K ≤ 3.
**Surviving finding (NOT rejected):** the frozen survivor bust/pass gate (3.0% / 50% / 1.0%) and
`DD_TRIGGER` 1.5% / `DD_SCALE` 0.40× — untouched; the four locked legs' own standing (Aegis remains
the best in-house validated single edge at 1.83); **low-K (≤441), pre-committed mechanism-first
discovery axes (the HARV lane)** — the K-scope explicitly reopens the band at K≤441, so this is a
kill of blind high-K mining, not of discovery generally; the Phase-1 grid harness spec (frozen +
Cursor-ready) — DEFERRED as moot at the banked K, never run and never disproven on its own terms.
**Re-proposal bar:** not a wider grid, a re-tuned felt cap, or more sims at the same K — the finding
is K-governed, so re-proposal needs either (a) a genuinely **low-K (≤441, better ≤33 for
Guardian-quality margin) pre-committed mechanism-first axis** under the HARV lane discipline, or
(b) new external evidence that moves an anchor — a corrected S_B figure materially above the
measured 0.85 top-decile ceiling, or a different S_floor K-accounting (not a re-derivation of the
3,177 constant itself, which belongs to DISC-CAMP-0's own closure). Amending the frozen survivor
gate ceilings or the DSR K/V rule in response to this finding is forbidden by H-CART §5, carried
verbatim into the closure.

<!-- concept-intake-entry mechanism_family="blind-high-k-discovery-mining" instrument="n/a (program-level DSR-admission reachability finding; anchors reference all four locked legs, no candidate scored)" rejection_reason="FALSIFIED at Phase 0.5 (ahead of the Phase-1 grid): realism-band S_floor 2.050 (K=3177,V=1/n) > every admissible Cap in [1.0,2.0] (Cap=max(S_A=1.828 Aegis, S_B=0.85 top-decile-net); |S_A-S_B|=0.978>0.5 fired divergence branch). Band [S_floor,Cap] empty under every Cap resolution -> H-CART otherwise branch fired vacuously; blind high-K (K=3,177) mining structurally dead at DSR admission; floor is K-governed not n-governed (K<=441 for Aegis-quality, K<=33 for Guardian-quality, K<=3 for typical-anomaly-quality)." harness_disposition_ref="Q-GATECART-1 closure (docs/briefs/closures/Q-GATECART-1-survivor-gate-cartography.md); verdict pre-reg freeze 453148a / §F filled 1367265 (pruned from working tree at the Great Prune 2026-08-08 — git show pre-prune-2026-08-08:docs/ltm/briefs/pre-registration/Q-GATECART-1-verdict-preregistration.md)" date="2026-07-14" class="reachability-constraint" role_tested="n/a (axis-reachability screen, not a scored entry/filter mechanism — Deployability annotation: N/A, no candidate scored)" falsifier_failed="S_floor 2.050 (K=3,177) > Cap ceiling admissible range [1.0,2.0]; zero realism-band-compliant grid points possible under any Cap resolution" addback_condition="K<=441 low-K pre-committed mechanism-first axis (HARV lane) reopens band to Aegis-quality; K<=33 to Guardian-quality — NOT wider/high-K mining, NOT felt-cap retune, NOT touching the frozen survivor gate (3.0%/50%/1.0%) or DD_TRIGGER/DD_SCALE" -->

### Q-INVENTORY-1 external-mechanism harvest sourcing burst × multi-instrument — FALSIFIED (0 admissible seeds)

**Rejection scope:** the bounded Q-INVENTORY-1 sourcing burst run under `docs/methodology/strategy_harvest.md` §1 admission requirements 1–5 — rank-1 forward-citation traversal from Baltussen-Da-Lammers-Martens 2021 (≈90 unique S2+OpenAlex citing works, 15 detail-reviewed), rank-2 survey/meta pass (10 searches), rank-3 futures-native journal pass (12 searches), all under the inherited Q1–Q6 query families — and the eight specific published-mechanism expressions it staged and sniff-screened dead: pre-FOMC ES drift (Lucca-Moench / Kurov-Wolfe-Gilbert); macro pre-release ES/ZN drift (Kurov-Sancetta-Strasser-Wolfe); FX fixing-window 6E/6J drift (Krohn-Mueller-Whelan); post-FOMC Treasury drift (Brooks-Katz-Lustig) + Pan-Peng pre-FOMC bonds; announcement-day SPX premium (Savor-Wilson / Knox-Londono-Samadi); VIX-complex momentum + EOD-pressure (Huang et al. / Bangsgaard-Kokholm); the venue-walled KC/Nikkei/Deribit/China rows; gold-fix rows (Caminschi-Heaney). Not ES, ZN, 6E, 6J, SPX, GC, or MGC the instruments; not the harvest-intake channel/lane; not the three UNSCREENABLE probe-funding stubs (priced, not screened).
**Closure date:** 2026-07-17
**Authoritative artifact:** [`Q-INVENTORY-1-closure-falsified`](briefs/closures/Q-INVENTORY-1-closure-falsified.md) · [`RESULTS`](../lab/archive/q_inventory_1_2026-07/RESULTS.md) · [`CANDIDATE_ROWS`](../lab/archive/q_inventory_1_2026-07/CANDIDATE_ROWS.md)
**Closure basis:** zero of eight staged row-groups cleared Req 1–5 at sniff-arithmetic level (Default-#1 OOS clock, 2019-05-06→). Power-wall ×3: pre-FOMC ES post-2016 δ≈9.2bp/event vs σ(24h ES)≈110bp → δ/σ≈0.08, N≈58 → power≈0.09 (break-even needs ≈28bp/event; only the decayed pre-2015 figure clears); announcement-day SPX +8.3bp/event vs σ≈110bp → δ/σ 0.075, N≈252 → power≈0.22; post-FOMC Treasuries (cash-yield cohort, not per-contract futures δ) + Pan-Peng long-bond pre-FOMC 0.68bp/event, ~4–8 events/yr → power dead. Cost-wall ×1 at the 4× multiple: FX fixing-window 6E/6J (n=2515, 2009–2018) — the strongest row staged, EUR pre-Europe window published net +5.53%/yr, SR 0.99 — ÷252 ≈2.2bp/event net → ≈3.3bp gross, against a 6E RT_frac≈1.1bp × 4 = 4.4bp hurdle; a published net-positive intraday effect still fails Req-5. Informed-flow/Req-2 ×1: macro pre-release ES/ZN δ (γ 0.066–0.154%/1σ surprise) is signed by the realized surprise itself; the "Drift Begone!" causal shutoff (UK ended prerelease access Jul 2017) erases ≈40% of the total adjustment. Venue-wall ×5: VIX-complex (VX untradeable at the four FRIENDLY firms; the ES EOD-pressure footprint is D5's Tier-C sibling — no extractable δ, documented reversal); KC coffee (ICE), Nikkei 225 (JPX), Deribit BTC, SHFE-class China commodity — none expressible at the four firms' CME micro books. K-wall ×1 (permanent): gold-fix rows, GC/MGC bank 3,177. Burst discipline held throughout: `discovery_manifests/` count 5→5 (delta 0), zero `register_search`, zero pulls, zero K spent across 22 total targeted searches (ranks 2–3) plus the rank-1 citation traversal.
**Surviving finding (NOT rejected):** ES, ZN, 6E, 6J, SPX, GC, and MGC instrument standing — the kill lands on these specific published expressions/parameters, not the instruments; the harvest-intake channel/lane itself (accept-idle firing the 2026-11-08 idle guard is the intake ADR's own success-eligible outcome, not a lane failure); the deployment axis (Q-RAIL-1, closed `RESOLVED` the same day) unaffected; the three UNSCREENABLE probe-funding stubs — ZN Treasury-auction dealer-hedging δ (Smales 2021), CL EIA-inventory unconditional-event δ, and the 6J/6E/CL carry timing-δ — priced (≈$0 data + one family-K each) but **not funded**, pending a fresh operator GO/NO-GO, not falsified; the standing 4× cost-law doctrine multiple, sharpened (not newly discovered) by the FX fixing-window row.
**Re-proposal bar:** new external mechanism evidence — a fresh published cohort δ clearing the Req-5 4× cost inequality at the panel basis, or a funded probe resolving one of the three named UNSCREENABLE stubs' missing input (per the closure's priced forks) — not a re-citation of any of the eight dead classes under a different paper (Req-3 dedup-first rule; GC/MGC bank 3,177 is a permanent K-wall), not a transplanted or invented δ, not a relaxed Default-#1 OOS start date (2019-05-06), and not "one more channel" appended to this closed burst.

<!-- concept-intake-entry mechanism_family="external-mechanism-harvest-sourcing-burst" instrument="ES+ZN+6E+6J+SPX+VX+GC+MGC" rejection_reason="H-INVENTORY-1 FALSIFIED: bounded rank-1 (~90 unique S2+OpenAlex citing works of Baltussen-Da-Lammers-Martens 2021) + rank-2 (10 searches) + rank-3 (12 searches) sourcing burst staged 8 row-groups, 0 cleared Req 1-5. Power-wall x3: pre-FOMC ES post-2016 delta~9.2bp vs sigma(24h)~110bp -> delta/sigma~0.08, N~58, power~0.09; announcement-day SPX +8.3bp/event vs sigma~110bp -> delta/sigma 0.075, N~252, power~0.22; post-FOMC Treasuries (cash-yield cohort, not futures delta) + Pan-Peng 0.68bp/event, ~4-8/yr, power dead. Cost-wall x1 at 4x hurdle: FX fixing-window 6E/6J (Krohn-Mueller-Whelan, n=2515) EUR pre-Europe window net +5.53%/yr SR0.99 published -> ~2.2bp/event net -> ~3.3bp gross vs 6E RT_frac~1.1bp x4=4.4bp hurdle. Informed-flow Req-2 x1: macro pre-release ES/ZN delta signed by realized surprise (gamma 0.066-0.154%/1sigma); Drift Begone causal shutoff (UK ended prerelease access Jul-2017) erases ~40% of total drift. Venue-wall x5: VX untradeable at the four FRIENDLY firms + ES EOD-pressure footprint (D5 Tier-C sibling, no delta, documented reversal); KC coffee/Nikkei 225/Deribit BTC/SHFE-class China commodity not expressible at the four firms' CME micro books. K-wall x1 (permanent): gold-fix rows, GC/MGC bank 3,177. Burst discipline held: discovery_manifests count 5->5 delta 0, zero register_search, zero pulls, zero K, 22 total targeted searches plus rank-1 citation traversal." harness_disposition_ref="Q-INVENTORY-1 RESULTS + CANDIDATE_ROWS (lab/archive/q_inventory_1_2026-07/RESULTS.md, lab/archive/q_inventory_1_2026-07/CANDIDATE_ROWS.md)" date="2026-07-17" class="screen-fail-multi-mechanism" role_tested="sourcing-screen (Req 1-5 sniff-arithmetic, pre-harness)" falsifier_failed="0-of-8 staged row-groups cleared Req 1-5 (power-wall x3 / cost-wall x1 at 4x / Req-2 informed-flow x1 / venue-wall x5 / K-wall x1 permanent)" addback_condition="new published cohort delta clearing the Req-5 4x cost inequality at the panel basis, OR a funded probe resolving one of the three named UNSCREENABLE stubs (ZN auction delta / CL EIA unconditional delta / 6J-6E-CL carry timing-delta) - NOT re-citation of any of the 8 dead classes under a new paper (GC/MGC bank 3,177 is a PERMANENT K-wall), NOT a transplanted/invented delta, NOT a relaxed Default-#1 OOS start (2019-05-06)" -->

### TAS settlement-window replication on MCL (CME CL 14:28–14:30 ET)

**Rejection scope:** the **outright** MCL expression of CME CL settlement-window benchmark-replication
flow — enter with the mandated-flow direction in the 14:28–14:30 ET settlement window, 20-tick stop,
~120 s horizon. Rejected on **magnitude reachability**, at $0/K=0, without the δ-extraction probe ever
being run. Distinct from `BE3`/`SFX-1` (killed by the *fade-program* $200/1.83 design law, ruled
fade-scoped and not a TNEC limb on 2026-08-10) and from `R8` (gold benchmark-fix, whose family scope is
the venue-legal **metals** set — MCL is Energy and outside it).
**Closure date:** 2026-08-11
**Class:** magnitude-unreachable (screened-dead pre-probe; mechanism plausible, required effect out of range)
**Authoritative artifact:** [`Q-MCLTAS-1 closure`](briefs/closures/Q-MCLTAS-1-closure-falsified.md) +
[`Stage 0 RESULTS`](../lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)
**Closure basis:** two independent walls, pre-registered. **Wall B (dispositive)** — the Req-5 hurdle is
11.60 ticks/event ($11.60/contract) = **14.87 bp** at the 2023 panel basis vs an estate causal-public δ
ceiling of **3.21 bp** (4.63×), falling only to 3.01× at an implausible $120 oil and surviving the
forbidden bare-commission ablation (3.04×). Converted to cohort-bound **δ/σ** against MCL's own *measured*
σ surface, the required δ/σ is **0.62–1.35** vs D5's committed **0.113 conservative / 0.194 optimistic** —
a floor of **3.2×** under maximal stacked generosity and **7.0×** at the defensible reading. **Wall A** —
the intersection of {free ∧ signed ∧ price-exogenous ∧ window-aligned} sign sources is **EMPTY**: published
TAS volume is gross by construction, ΔOI is directionally agnostic, COT is weekly and lagged, and CME
publishes **no** settlement-window imbalance print (the structural asymmetry vs the equity closing auction
that `F1`/MOC traded). One entitled-but-**costed** route (TAS-book order flow in `GLBX.MDP3`) survives
unverified; it cannot reach Wall B. Adverse mechanism prior: TAS exists *so that* mandated flow can lock
settlement without revealing direction to the outright book, so the public residue is small by
construction — R8's measured structure, and the informed-flow signature's **third** confirmed instance
on the family where it was **first** confirmed (`H-FBEIA-1`, −1.16 bp, wrong-signed).
**Re-proposal bar:** a **published, post-hoc-free cohort δ for CL/MCL settlement-window flow ≥ the 4×
hurdle at a named venue-legal outright expression** (mirrors R8's bar). NOT a re-read of this arithmetic,
a window/stop re-tune, the DISCLOSURE bare-commission basis, a spread re-frame (a **new campaign** per
ENV-1 §6.4.1, and `SFX-1` is already dead), or resolution of Wall A's costed route — which cannot reach
Wall B. **MCL the instrument is NOT rejected** — what dies is this design region, per the ledger's
2026-08-10c precedent.

<!-- concept-intake-entry mechanism_family="tas-settlement-window-replication" instrument="MCL" rejection_reason="magnitude-unreachable (screened dead pre-probe, $0/K=0): outright MCL expression of CME CL settlement-window (14:28-14:30 ET) benchmark-replication flow, 20-tick stop, 120s horizon. Wall B dispositive: Req-5 hurdle 11.60 ticks/event = 14.87bp at 2023 panel basis vs estate causal-public delta ceiling 3.21bp (4.63x); 3.01x at implausible $120 oil; 3.04x under the forbidden bare-commission ablation. In cohort-bound delta/sigma against MCL's own MEASURED sigma surface (stage2_sigma.windowed_sigma, wed_thu ex-FOMC, 15-min column sqrt-time scaled to the 2-min window): required delta/sigma 0.62-1.35 vs D5 committed 0.113 conservative / 0.194 optimistic = floor 3.2x under maximal stacked generosity, 7.0x defensible. Wall A: intersection of {free, signed, price-exogenous, window-aligned} sign sources EMPTY - published TAS volume is gross by construction, delta-OI directionally agnostic, COT weekly+lagged, and CME publishes NO settlement-window imbalance print (structural asymmetry vs the equity closing auction F1/MOC traded); one entitled-but-costed route (TAS-book order flow in GLBX.MDP3) survives unverified and cannot reach Wall B. Adverse mechanism prior: TAS exists so mandated flow can lock settlement WITHOUT revealing direction to the outright book, so public residue is small by construction - informed-flow signature third confirmed instance, on the family where it was first confirmed (H-FBEIA-1, -1.16bp, wrong-signed). Probe never run; the two free pre-stages establish it is unfundable before design. NOT the BE3/SFX-1 kill (fade-program design law, ruled fade-scoped 2026-08-10) and NOT inside R8's metals-only family scope." harness_disposition_ref="Q-MCLTAS-1 Stage 0a+0b (no harness DispositionRecord; lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)" date="2026-08-11" class="magnitude-unreachable" role_tested="entry" falsifier_failed="Wall B: required delta 14.87bp vs 3.21bp estate causal-public ceiling (4.63x, min 3.01x); cohort-bound required delta/sigma 0.62-1.35 vs D5 0.113/0.194 (floor 3.2x, defensible 7.0x)" addback_condition="published post-hoc-free cohort delta for CL/MCL settlement-window flow >= the 4x hurdle at a named venue-legal OUTRIGHT expression (mirrors R8's bar) - NOT a re-read of this arithmetic, window/stop re-tune, DISCLOSURE bare-commission basis, spread re-frame (new campaign per ENV-1 6.4.1; SFX-1 already dead), or resolution of Wall A's costed route" config_fingerprint="tas-settlement/MCL/window=1428-1430ET/stop=20t/horizon=120s/RT=2.90-F3-primary/hurdle=4x/sigma=stage2-windowed-wed-thu-exFOMC" -->

### MNQDTL-CON-1 ES-NQ 5m divergence relative-contrarian × MNQ — FALSIFIED (explore IS)

**Rejection scope:** the Q-MNQDTL-CON-1 G0 construct catalogue cell C1 —
`es-nq-log-divergence-relative-contrarian` (ES−NQ 5m log-return divergence vs 20-session
median |d| threshold, relative contrarian, LONG iff d≥+θ / SHORT iff d≤−θ) on CME **MNQ**
(dense RTH 1m opens; G=10 hard stop; session-flat exit; EM3 independence; k=1) as frozen in
[`PREREG_G0`](../lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md) §2 — not MNQ the
instrument, not the MNQSEL-2 dense-1m-@-G=10 selection-ceiling result that licensed this
construct, not the broader construct catalogue (other entry rules on this universe are
untested by this cell).
**Closure date:** 2026-08-09
**Authoritative artifact:** [`Q-MNQDTL-CON-1-closure-falsified`](briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md) ·
[`RESULTS`](../lab/archive/mnq_con1_dense1m_stage0_2026-08/RESULTS.md) ·
[`PREREG_G0`](../lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md)
**Closure basis:** both arms `FALSIFIED` on the default full joined MNQSEL-2 panel (1,645
eligible sessions, 100% signal coverage, ~11.6 trades/eligible session). Long n=10,093 mean
net R **−0.1065**, session-block 95% CI **[−0.191, −0.017]** (entirely &lt;0), WR 0.083, stop
rate 0.915, halves h1/h2 both negative (sign agree), annSR −0.899, **DSR 0.011** (floor
0.650). Short n=9,000 mean net R **−0.1113**, CI **[−0.209, −0.005]** (entirely &lt;0), WR
0.075, stop rate 0.920, halves both negative (sign agree), annSR −0.825, **DSR 0.021**. Kill
is negative edge with CI below 0 on both arms — not thin-n, not halves VOID. CONFIRM /
N-SURV / deploy unread; Cap not claimed; $0.00 / K_intrinsic=1.
**Surviving finding (NOT rejected):** MNQ instrument standing; the `Q-MNQSEL-2` RESOLVED
dense-RTH-1m-@-G=10 selection-ceiling result that unlocked this universe; TNEC-1 intake-gate
discharge (Stage-0 cheap-falsifier `CHEAP_FALSIFIER_OK`) as a process finding; the construct
catalogue itself (untested entry rules on this universe remain open).
**Re-proposal bar:** a new entry mechanism — **not** G / lookback / θ-window retune of this
cell. Sign inversion is explicitly forbidden: it collapses into own-instrument momentum,
already dead as C5 / D5-RECOST-1.

<!-- concept-intake-entry mechanism_family="es-nq-log-divergence-relative-contrarian" instrument="MNQ" rejection_reason="explore IS FALSIFIED: both arms session-block 95% CI entirely <0 (long n=10093 mean_R=-0.1065 CI[-0.191,-0.017]; short n=9000 mean_R=-0.1113 CI[-0.209,-0.005]); stop-dominated (WR 0.083/0.075, stop rate 0.915/0.920); halves sign-agree both negative; DSR 0.011/0.021 far below 0.650 floor. CONFIRM/N-SURV/deploy unread." harness_disposition_ref="Q-MNQDTL-CON-1 RESULTS (lab/archive/mnq_con1_dense1m_stage0_2026-08/RESULTS.md)" date="2026-08-09" class="explore-falsified" role_tested="entry" falsifier_failed="primary CI entirely < 0 both arms; DSR 0.011/0.021 << 0.650 floor" addback_condition="new entry mechanism — NOT G/lookback/theta-window retune of this cell; sign invert explicitly forbidden (own-instrument momentum = C5/D5-RECOST-1, already dead)" -->

### Q-MNQSEL-1 restart-clock oracle top-1/day selection ceiling × MNQ — FALSIFIED (C2; Phase-0 ceiling)

**Rejection scope:** the Q-MNQSEL-1 Phase-0 measurement of **perfect (oracle) top-1/day
take/skip selection** among causal **restart-clock** candidates (session-open bar + the bar
immediately after each completed window, reused unmodified from Step-1's greedy `s=40`/`G=17.41`
partition) on CME **MNQ** — not MNQ the instrument, not the Step-1 event-ceiling count
(median 145 clocks/session) that fed it, not other candidate-set definitions (denser
order-flow sub-sampling or completed-window ranking are explicitly out of scope for any
successor, not tested or rejected here on their own terms).
**Closure date:** 2026-08-07
**Authoritative artifact:** [`Q-MNQSEL-1-closure-falsified`](briefs/closures/Q-MNQSEL-1-closure-falsified.md) ·
[`RESULTS`](../lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md) ·
[`PREREG`](../lab/archive/mnq_selection_ceiling_2026-08/PREREG.md)
**Closure basis:** frozen gate C2 fired — oracle top-1/day mean net R (S3) **below** EM1 0.40
on **both** arms (long **0.3998**, short **0.3984**; n_sessions **1,674** ≥ 250, so C1
`INSUFFICIENT-N` did not fire). All-take (S1) is deeply negative on both arms (long **−0.0364**,
short **−0.0362**), ruling out C3 `SURPRISE-DIRECTION`. By the `G(s)=0.40·s+1.41` construction
(G=17.41 at s=40; round-trip cost 1.41 pt = 2×0.91/$2.00pt) a clean target-hit earns ≈0.40R
almost by definition, and S6 shows 99.9%/99.7% of sessions have ≥1 target-hit (S5 median
98.0/97.0 hits/day) — winner density is not the bottleneck. The ~0.1–0.3% of sessions with
**no** target-hit pull the oracle mean a few ten-thousandths under the 0.40 floor, with zero
margin on either arm.
**Surviving finding (NOT rejected):** MNQ instrument standing; the Step-1 restart-clock
construction and event count (median 145 clocks/session at s=40) as a measurement technique;
the finding that all-take carries no free direction bias (S1 deeply negative both arms); the
target-hit density itself (S5/S6) as evidence that winners are abundant on this clock set — the
gate failure is a **selection ceiling**, not opportunity scarcity.
**Re-proposal bar:** a **different causal candidate set** — **not** denser order-flow
sub-sampling on the same restart clocks, **not** completed-window ranking (look-ahead, already
forbidden under FM-1), and not reading S3 ≈ 0.40 as "close enough" to clear EM1.

<!-- concept-intake-entry mechanism_family="restart-clock-oracle-top1-selection" instrument="MNQ" rejection_reason="Phase-0 FALSIFIED (C2): oracle top-1/day mean net R (S3) below EM1 0.40 both arms (long 0.3998, short 0.3984; n=1,674 sessions >= 250). All-take (S1) deeply negative both arms (-0.0364/-0.0362), no SURPRISE-DIRECTION. Target-hit density high (S5 97-98/day, S6 99.7-99.9%) but the ~0.1-0.3% no-hit sessions pull the oracle mean under the 0.40 knife-edge with zero margin." harness_disposition_ref="Q-MNQSEL-1 RESULTS (lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md)" date="2026-08-07" class="phase0-selection-ceiling" role_tested="selection (oracle take/skip among fixed causal restart-clock entries)" falsifier_failed="C2: S3 oracle top-1/day < 0.40 both arms (0.3998 long / 0.3984 short)" addback_condition="different causal candidate set — NOT denser order-flow on the same restart clocks, NOT completed-window ranking (FM-1, look-ahead)" -->

### Striker DJ30 pyramid-stack risk%-input scaling × MYM — FALSIFIED-NONPROPORTIONAL

**Rejection scope:** the risk%-input-scaling route for realizing a lifecycle authorization haircut
(e.g. WATCH-1 0.50×) on the Striker DJ30 v4.5 pyramided leg (750% pyramid add) via TV on
CBOT **MYM1!** at the $200K panel-of-record account size — i.e., halving `riskPerTrade` as the
mechanism to halve the executed base+add stack — not MYM1! the instrument, not Striker DJ30's
LOCKED parameters/Pine (untouched), not the account-multiplier-layer haircut mechanism (the
surviving fallback), and not the NAS100/MNQ1! leg (that cohort scored `AMBIGUOUS-HOLD` on this
same protocol, not `FALSIFIED`).
**Closure date:** 2026-07-17
**Authoritative artifact:** [`Q-PYRPARITY-1-closure-falsified-nonproportional`](briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) ·
[`RESULTS`](../lab/archive/q_pyrparity_1_2026-07/RESULTS.md) ·
[`PHASE0`](../lab/archive/q_pyrparity_1_2026-07/PHASE0.md) ·
[`pre-registration`](briefs/pre-registration/Q-PYRPARITY-1-verdict-preregistration.md)
**Closure basis:** Branch B (equity-normalized, add normalized on entry-bar equity per Phase 0)
per-fill ratio harness (`verify_phase2.py`) on paired native TV exports, MYM1! @ $200K, Striker
DJ30 (750% pyramid): base cohort n=232 paired fills, median ratio **0.8707** (frac inside the
±0.02 band = 0.082); add cohort n=35 paired, median **0.9164** (frac in ±0.02 = 0.086) — both
cohorts miss the pre-registered accept bands (median within 0.500 ± 0.005 AND ≥95% of paired
fills within 0.500 ± 0.02) by a wide margin and trip the reject clause (median outside
0.500 ± 0.02). Mechanism, read off the r0 export: MYM1! carries a hard TV/symbol-runtime qty
ceiling — base clips at **17** contracts (210/232 r0 base fills sit at exactly 17), add clips at
**127** (= 17 × 7.5 floored; 30/35 r0 adds at exactly 127). Sliced by whether r0 sits at the
ceiling: fills where r0 is below the cap reproduce H-PYRPARITY-1 almost exactly (base n=22 median
**0.502**, raw-qty median 0.500; add n=5 median **0.496**, raw-qty median 0.495), while fills at
the cap collapse toward 1.0 (both-at-17 n=87 median 1.042; r0-at-17/r½-below n=123 median 0.764).
The Phase-0 Pine-source read confirms the sizing path (`calcSize`, `striker_dj30_v4.5.pine:149-151`;
add derivation `:275-276`) is exactly linear in `riskPerTrade` with no floor/cap/round/min-qty —
the ceiling is TV/broker-runtime behavior on `CBOT_MINI:MYM1!` at this account size, not a Pine
defect.
**Surviving finding (NOT rejected):** MYM1! instrument standing and the Striker DJ30 v4.5 leg
itself (LOCKED parameters, no Pine edit — parameter axis untouched); below-ceiling proportionality
(H-PYRPARITY-1 holds structurally per the Phase-0 source read and empirically on the below-cap
fill slices); the account-multiplier-layer haircut as the surviving WATCH-1 realization mechanism
(`strategy_lifecycle.md:113` → CONFIRMED-FALLBACK 2026-07-17; Q-RAIL-1 F1 = PASS-via-fallback); the
NAS100/MNQ1! leg's own parity test, which scored `AMBIGUOUS-HOLD` (list misalignment + base-cohort
fill-fraction FAIL) on this same protocol — a separate, unresolved finding, not itself a rejection.
**Re-proposal bar:** new evidence that the $200K-account MYM1! TV/broker qty ceiling (base 17 /
add 127) does not bind at the account tier actually deployed — not a re-run of this same protocol
at the same $200K test size, not a Pine parameter retune (parameter axis LOCKED), and not loosening
the pre-registered 0.500 ± 0.02 / ± 0.005 tolerance bands (Known Trap #12 — no amendment after data
is seen).

<!-- concept-intake-entry mechanism_family="risk-pct-input-pyramid-stack-scaling" instrument="MYM" rejection_reason="FALSIFIED-NONPROPORTIONAL: TV/symbol qty ceiling on MYM1!@$200K (base clip 17, add clip 127=17×7.5 floored) collapses the realized halve-risk ratio toward 1.0 above the ceiling. Branch-B median ratio: base 0.8707 (n=232 paired, frac in ±0.02 = 0.082), add 0.9164 (n=35 paired, frac in ±0.02 = 0.086), vs required median 0.500±0.005 / ≥95% in ±0.02. Below-ceiling slices confirm proportionality holds (base n=22 median 0.502; add n=5 median 0.496). Pine sizing path confirmed exactly linear in riskPerTrade, no floor/cap/round (Phase 0)." harness_disposition_ref="Q-PYRPARITY-1 RESULTS Phase 2 (lab/archive/q_pyrparity_1_2026-07/RESULTS.md)" date="2026-07-17" class="execution-fidelity-failure" role_tested="sizing-realization-route" falsifier_failed="median Branch-B ratio outside 0.500±0.02 on both MYM cohorts (base 0.8707 n=232 paired; add 0.9164 n=35 paired) vs required median 0.500±0.005 AND ≥95% of paired fills within 0.500±0.02" addback_condition="new evidence the $200K MYM1! TV qty ceiling (base 17 / add 127) does not bind at the deployed account tier — NOT a re-test at the same $200K size, NOT a Pine parameter retune (LOCKED), NOT a tolerance-band change (Trap #12)" -->

### R2FLOW clock-minute net signed aggressor flow × MNQ — FALSIFIED (Stage-G association null)

**Rejection scope:** the Q-R2FLOW-1 Route B G0 catalogue's single frozen cell C1 — clock-minute
net signed aggressor size (buy_sz − sell_sz contracts, `tbbo` schema) → 60-second mid return on
`MNQ.v.0` continuous RTH, at `K_intrinsic=1` — as frozen in
[`PREREG_G0`](../lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md) — not MNQ the instrument,
not the Route B / Avenue A generate-confirm channel, not the sibling OF cells (OFCHAN resting-size
flicker-filter, R2VBUCK imbalance **ratio**, R2AGRUN aggressor-run **length**), which are
separately scoped and closed on their own limbs.
**Closure date:** 2026-08-08
**Authoritative artifact:** [`Q-R2FLOW-1-closure-falsified`](briefs/closures/Q-R2FLOW-1-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md) ·
[`PREREG_G0`](../lab/archive/mnq_r2flow_routeb_2026-08/PREREG_G0.md)
**Closure basis:** Stage-G EXPLORATION-only (2026-02-06→2026-08-06, OFCHAN-cache reuse, 124
sessions scored). VOID-POWER PASS (n_retained 48,360 ≥ 2,000) and VOID-COVERAGE PASS
(48,360/48,360 = 100%), but Pearson ρ(A, r) = **−0.000701** with 95% session-block bootstrap CI
**[−0.014612, +0.013510]** (10,000 reps, seed 20260808) — CI includes 0, primary limb FAIL.
\|ρ\| 0.000701 is also below the 0.02 magnitude floor. Halves disagree in sign (H1 −0.020313 /
H2 +0.014732), not reached as the deciding limb since CI already failed; placebo skipped under
PREREG CI-precedence. Candidate list **empty** ([]) → zero promotions. CONFIRM
(2025-09-01→2026-02-06) unread; Cap seat not claimed; $0 spend, `K_intrinsic=1` disclosure-only.
**Surviving finding (NOT rejected):** MNQ instrument standing; the OFCHAN `tbbo` cache / Route B
data pipeline; the Avenue A generate/confirm methodology itself; the three prior Route B OF
cells' own independent findings (OFCHAN VOID-COVERAGE, R2VBUCK ratio FALSIFIED, R2AGRUN magnitude
AMBIGUOUS-HOLD) — this entry rejects only the net-signed-aggressor-flow construct on the
clock-minute grid, not the broader order-flow / microstructure channel.
**Re-proposal bar:** new mechanism evidence — a genuinely different order-flow construct — not a
grid, horizon, or catalogue retune of this G0 (per PREREG_G0's own re-proposal bar / brief §6
STOP disposition).

<!-- concept-intake-entry mechanism_family="clock-minute-net-signed-aggressor-flow" instrument="MNQ" rejection_reason="Stage-G association null (FALSIFIED): EXPLORATION-only 2026-02-06->2026-08-06 (124 sessions), n_retained 48,360/48,360=100% coverage, VOID-POWER/COVERAGE both PASS; Pearson rho(A,r)=-0.000701, 95% session-block bootstrap CI [-0.014612,+0.013510] includes 0 (primary limb FAIL); |rho| 0.000701 << 0.02 magnitude floor; halves disagree sign (H1 -0.020313 / H2 +0.014732, not reached); placebo skipped under CI-precedence. Candidate list empty. CONFIRM unread." harness_disposition_ref="Q-R2FLOW-1 RESULTS_g2 (lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md)" date="2026-08-08" class="edge-failure" role_tested="entry" falsifier_failed="Stage-G CI-excludes-0 limb FAIL; |rho|>=0.02 magnitude limb FAIL" addback_condition="new mechanism evidence (a genuinely different order-flow construct) — NOT a grid/horizon/catalogue retune of this G0" -->

### Q-R2VBUCK-1 volume-bucket aggressor imbalance × MNQ — FALSIFIED (Stage-G association-null)

**Rejection scope:** the Q-R2VBUCK-1 Route B G0 construct `volume-bucket-aggressor-imbalance` on
CME **MNQ.v.0** (RTH; signed tape-aggressor size imbalance inside completed volume buckets
B=2550 → 60 s mid return; `tbbo` schema only; k=1) as frozen in
[`PREREG_G0`](../lab/archive/mnq_r2vbuck_routeb_2026-08/PREREG_G0.md) — not MNQ the instrument,
not the order-flow/tape-aggressor mechanism class generally, not the OFCHAN minute-grid
resting-ToB-size cell (separate construct, already closed VOID-COVERAGE), not volume-bucket
sampling as a coverage technique.
**Closure date:** 2026-08-08
**Authoritative artifact:** [`Q-R2VBUCK-1-closure-falsified`](briefs/closures/Q-R2VBUCK-1-closure-falsified.md) ·
[`RESULTS_g2`](../lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md) ·
[`PREREG_G0`](../lab/archive/mnq_r2vbuck_routeb_2026-08/PREREG_G0.md)
**Closure basis:** VOID-POWER PASS (n_retained **77,656** ≥ 2,000) and VOID-COVERAGE PASS
(**77,656 / 77,656 = 100%** ≥ 90%), but every association limb fails: ρ **−0.005478**,
session-block bootstrap CI95 **[−0.016881, +0.005984]** includes 0 (CI limb FAIL); \|ρ\| =
0.005478 &lt; within-session placebo \|·\| p95 **0.007958** (placebo limb FAIL); \|ρ\| &lt; **0.02**
magnitude floor (FAIL); halves disagree in sign (H1 **−0.017417** / H2 **+0.002439**, not
reached as the deciding limb since CI/placebo already failed). Candidate list = **[]** → G3
STOP. CONFIRM (**2025-09-01→2026-02-06**) unread; Cap seat not claimed; $0.00 spend;
`K_intrinsic=1`.
**Surviving finding (NOT rejected):** MNQ.v.0 instrument standing (occupancy released
2026-08-12 for new non-Striker research); the Avenue A / Route B generate→confirm methodology;
volume-bucket sampling as a technique that cleared the OFCHAN minute-grid coverage pathology
(100% coverage here vs 7.36% on OFCHAN's clock-minute flicker filter) — the failure here is
association, not denseness; C9's tape-aggressor-vs-resting-ToB-size distinction (this construct
clears C9 limb 1, independent of this cell's outcome); the CONFIRM window itself, still unread
and reserved.
**Re-proposal bar:** new G0 / new mechanism (a different causal object) — **not** a retune of
B (bucket size), the 60 s horizon, or this catalogue (FM-9 / Trap #12).

<!-- concept-intake-entry mechanism_family="volume-bucket-aggressor-imbalance" instrument="MNQ" rejection_reason="Stage-G association-null (explore IS): VOID-POWER/COVERAGE both PASS (n=77,656/77,656=100%) but rho=-0.005478, CI95[-0.016881,+0.005984] includes 0, |rho|<placebo p95 0.007958, |rho|<0.02 magnitude floor, halves disagree (H1 -0.017417/H2 +0.002439). Candidate list=[]. CONFIRM unread; Cap unclaimed; $0/K=1(disclosure)." harness_disposition_ref="Q-R2VBUCK-1 RESULTS_g2 (lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md)" date="2026-08-08" class="association-null" role_tested="signal" falsifier_failed="CI95 includes 0; |rho|<placebo p95; |rho|<0.02 magnitude floor; empty candidate list at G3" addback_condition="new G0 / new mechanism (different causal object) — NOT a retune of B, horizon, or this catalogue" -->

### TV bar-coverage-artifact hypothesis (2022 trade-rate break) × MYM/MNQ/6J — FALSIFIED (H; MYM operator BREAK-REAL)

**Rejection scope:** the Q-TVCOV-1 H (coverage-artifact) explanation for the 2022 MYM/MNQ/6J
trade-rate discontinuity — tested on the pre-registered 9-month frozen grid (2019-09/2020-03/
2020-09/2021-03/2021-09 pre-break, 2022-03/2023-06/2024-03/2025-06 post-break) as either
(a) Databento GLBX.MDP3 volume-rolled (`.v.0`) canonical coverage pre-break trailing post-break
by ≥5pp, or (b) canonical complete but TV 15m (BAR EXPORT v0.2) bar counts ≥5% below canonical
on ≥2 pre-break months — not MYM/MNQ/6J the instruments, not the locked strategies that trade
them (Guardian Gold / Striker DJ30 / Aegis USDJPY / Striker NAS100), not the 2026-07-12
seven-year evidential panels' standing, and not the calendar-rolled `.c.0` first-pass symbology
(that ARTIFACT-CONFIRMED read was withdrawn same day as the audit's own roll-rule artifact, not
re-adjudicated here).
**Closure date:** 2026-07-13 (verdicts landed, same day as the roll-rule correction); roster row
bookkeeping-closed 2026-08-09 (GSUB-1 c4, no re-verdict); formal closure brief backfilled
2026-08-11 (records-completeness reconstruction, not a re-adjudication).
**Authoritative artifact:** [`Q-TVCOV-1-closure-falsified`](briefs/closures/Q-TVCOV-1-closure-falsified.md) ·
[`RESULTS.md`](../lab/analysis/c1/tvcov_2026-07/RESULTS.md) ·
[`pursuit c4`](pursuits/c4-q-tvcov-1.md)
**Closure basis:** corrected canonical series (`.v.0`, volume-rolled) coverage complete both eras
— 6J 98.86% pre / 99.16% post (Δ+0.31pp); MYM/MNQ 96.35% pre / 99.04% post (Δ+2.69pp, the
residual traced to the pre-2021 16:15-ET equity-index maintenance-halt slot, not liquidity) —
limb (a) NOT MET on all three (&lt;5pp). TV (BAR EXPORT v0.2) matches canonical exactly (0.0%
deviation) on all 5 pre-break months for 6J and within ±0.1% for MNQ — limb (b) NOT MET,
±1%-match falsifier MET → **6J/MNQ H FALSIFIED, break real**. MYM matches exactly on 4/5
pre-break months; 2020-03 is −4.3% = a single missing TV day (2020-03-16, the COVID limit-down
session; 29/31 slots), not era-wide thinness — below the limb-(b) bar (needs ≥5% on ≥2 months) →
grid **AMBIGUOUS**, operator-accepted **BREAK-REAL** 2026-07-13. First-pass calendar-rolled
`.c.0` had issued 6J **ARTIFACT-CONFIRMED** (57.61%→72.87%, +15.26pp) same day — traced to a
serial-month roll-mapping defect (`6J.c.0` 2021-09 = 335 slots vs `6J.v.0`/TV = 734 slots
identically) and **withdrawn**. Two independent blind recomputes matched all 27 corrected-series
cells each (54/54); a third skeptic-agent pass returned 4/4 CONFIRMED on the roll-rule
attribution.
**Surviving finding (NOT rejected):** the 2026-07-12 seven-year evidential panels retain full
standing (MYM carries the standing 2020-03-16 annotation obligation); MYM/MNQ/6J instrument
standing and the locked Guardian/Striker/Aegis/NAS100 strategies that trade them are untouched —
this audit tested TV data-coverage only (its own brief states "not a discovery campaign; K=0, no
candidate is mined"); BAR EXPORT v0.2 stands as the default TV-side leg for future coverage/
parity questions; the `.v.0`-not-`.c.0` roll-rule pin for TV-`1!` comparisons (already discharged
in the `databento-data` skill reference since 2026-07-13).
**Re-proposal bar:** new mechanism evidence about bar *availability* — a different feed class, a
different roll protocol, or a day TV actually served that was previously missing — **not** a
re-census of the same nine quarterly-expiry months on `.c.0` (already shown to be the audit's own
symbology artifact, not a property of the data the backtests ran on).

<!-- concept-intake-entry mechanism_family="tv-bar-coverage-artifact-hypothesis" instrument="6J" rejection_reason="H FALSIFIED -- break real: corrected canonical (.v.0) 98.86% pre / 99.16% post (delta +0.31pp, limb-a NOT MET); TV (BAR EXPORT v0.2) matches canonical exactly (0.0% dev) on all 5 pre-break months (limb-b NOT MET, +/-1% falsifier MET). First-pass .c.0 ARTIFACT-CONFIRMED (+15.26pp) withdrawn as a serial-month roll-mapping artifact (335 vs 734 slots, 2021-09)." harness_disposition_ref="Q-TVCOV-1 RESULTS.md sec.Falsifier disposition (lab/analysis/c1/tvcov_2026-07/RESULTS.md)" date="2026-07-13" class="data-integrity-coverage-artifact-falsified" role_tested="n/a -- data-coverage audit (K=0, no strategy candidate mined), not entry/exit/filter/size" falsifier_failed="canonical coverage complete (delta +0.31pp < 5pp); TV 0.0% deviation all 5 pre-break months (< 5% and < 1%)" addback_condition="new mechanism evidence about bar availability (different feed class, different roll protocol, or a previously-missing day TV actually served) -- NOT a re-census of the same 9 quarterly-expiry months on .c.0" -->
<!-- concept-intake-entry mechanism_family="tv-bar-coverage-artifact-hypothesis" instrument="MNQ" rejection_reason="H FALSIFIED -- break real: corrected canonical (.v.0) 96.35% pre / 99.04% post (delta +2.69pp, limb-a NOT MET, fully explained by the pre-2021 16:15-ET equity-index halt-slot elimination); TV within +/-0.1% all pre-break months (limb-b NOT MET, +/-1% falsifier MET)." harness_disposition_ref="Q-TVCOV-1 RESULTS.md sec.Falsifier disposition (lab/analysis/c1/tvcov_2026-07/RESULTS.md)" date="2026-07-13" class="data-integrity-coverage-artifact-falsified" role_tested="n/a -- data-coverage audit (K=0, no strategy candidate mined), not entry/exit/filter/size" falsifier_failed="canonical coverage complete (delta +2.69pp < 5pp, halt-slot-explained); TV max +0.1% deviation all pre-break months (< 5% and < 1%)" addback_condition="new mechanism evidence about bar availability (different feed class, different roll protocol, or a previously-missing day TV actually served) -- NOT a re-census of the same 9 quarterly-expiry months on .c.0" -->
<!-- concept-intake-entry mechanism_family="tv-bar-coverage-artifact-hypothesis" instrument="MYM" rejection_reason="Grid AMBIGUOUS -> operator-accepted BREAK-REAL 2026-07-13: corrected canonical (.v.0) 96.35% pre / 99.04% post (delta +2.69pp, limb-a NOT MET); TV matches exactly 4/5 pre-break months, 2020-03 -4.3% = single missing TV day (2020-03-16 COVID limit-down, 29/31 slots) not era-wide thinness -- below limb-b bar (needs >=5% on >=2 months); +/-1%-match falsifier NOT MET on 2020-03 alone." harness_disposition_ref="Q-TVCOV-1 RESULTS.md sec.Falsifier disposition + sec.Operator disposition (lab/analysis/c1/tvcov_2026-07/RESULTS.md)" date="2026-07-13" class="data-integrity-coverage-artifact-falsified" role_tested="n/a -- data-coverage audit (K=0, no strategy candidate mined), not entry/exit/filter/size" falsifier_failed="grid AMBIGUOUS on +/-1% limb (2020-03 -4.3%, single day); limb-b NOT MET (one month, needs >=2-month bar); operator parent call taken, not a mechanical FALSIFIED" addback_condition="new mechanism evidence about bar availability (different feed class, different roll protocol, or a previously-missing day TV actually served) -- NOT a re-census of the same 9 quarterly-expiry months on .c.0; standing 2020-03-16 annotation obligation stays wherever 2020-Q1 Striker-MYM behavior is analyzed" -->

### Transfer/expression lane (Q-TXG-1) — FALSIFIED-at-walls

**Rejection scope:** the Q-TXG-1 transfer/expression programme — incumbent locked mechanisms
(Guardian / Striker / Striker NAS100 / Aegis) × ENV-1 7-micro pool at Tradeify Select
EOD-trailing survival geometry — as a *lane*, not any single home-instrument strategy and not
ENV-1 instruments as a class.
**Closure date:** 2026-08-12
**Authoritative artifact:** [`docs/briefs/Q-TXG-1-ha-reargument.md`](briefs/Q-TXG-1-ha-reargument.md)
(operator elected **(A) CLOSE**) ·
[`lane closure`](briefs/closures/Q-TXG-1-closure-falsified-at-walls.md) ·
cell closures [`nas100×MYM DEAD(cost)`](briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) ·
[`striker×MNQ DEAD(N-SURV)`](briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) ·
[`Guardian→MGC DEAD(N-SURV)`](briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) ·
Aegis→6J both-layers ([`ops/instruments/6J.md`](../ops/instruments/6J.md) J4b+J14)
**Closure basis:** two consecutive elected-cell FALSIFIEDs forced H_A re-argument (design §6);
operator elected CLOSE. Four positive-net transfers; zero survivors against the composition of
the frozen per-trade cost floor and the trailing-DD survival ceiling
(`lesson_trailing_dd_survival_is_skew_governed`). Remaining 23 OPEN cells are stop-unscreenable
(ATR-median unlock refused without new mechanism evidence).
**Surviving finding (NOT rejected):** locked-book mechanisms on home instruments; ENV-1
instrument-lane eligibility; ORB payability and paid/new-venue generation routes.
**Re-proposal bar:** new mechanism evidence with a **demonstrably different loss-side shape**,
or a **venue class whose survival geometry differs** (not an EOD-trailing prop clone) —
**not** new cells, new instruments, or ATR-input spend alone.

<!-- concept-intake-entry mechanism_family="locked-mechanism-cross-underlying-transfer-expression" instrument="ENV-1" rejection_reason="lane FALSIFIED-at-walls (H_A re-argument, design §6): two consecutive elected-cell kills — striker_nas100×MYM DEAD(cost) mean_net_r 0.0129<required_net_r 0.06 (N=190, net +$4,356.40, PF 1.110); striker×MNQ PASS_COST (mean_net_r 0.0419>0.03, N=222, net +$22,789.58) then DEAD(N-SURV) bust 98.13%/96.76%/99.37% full/H1/H2 vs ≤3.0% ceiling — forced re-argument; operator elected CLOSE. All four positive-net transfer expressions died at the same composition of frozen cost floor + trailing-DD survival ceiling: Guardian→MGC DEAD(N-SURV) bust 42.2%/72.4%/16.5%; Aegis→6J J4b best cell 3.88% bust (1.3× over) + J14 composed 3-leg 0/3 tiers and cap-infeasible. Edge transfer itself was never falsified — GRID_RESULTS.json confirms 25 compile-open cells, 23 stop-unscreenable (Aegis 7 / Guardian 6 / Striker 5 / Striker_NAS100 5), only the 2 mapped-stop cells (the elected, now-dead pair) were scorable without ATR-median spend." harness_disposition_ref="Q-TXG-1 H_A re-argument (docs/briefs/Q-TXG-1-ha-reargument.md); lane closure docs/briefs/closures/Q-TXG-1-closure-falsified-at-walls.md" date="2026-08-12" class="falsified-at-walls" role_tested="cross-underlying locked-mechanism transfer/expression port (cost-tax + trailing-DD N-SURV gates)" falsifier_failed="composition of frozen required_net_r/port_must_beat cost floor AND trailing-DD bust≤3.0% N-SURV ceiling across all four positive-net transfer expressions (lesson_trailing_dd_survival_is_skew_governed)" addback_condition="new mechanism evidence with a demonstrably different loss-side shape, or a venue class whose survival geometry differs (not an EOD-trailing prop clone) — NOT new cells, new instruments, or ATR-input spend alone" -->

### SLR-MYM-1 liquidity sweep-and-reclaim × MYM — FALSIFIED (as scoped; Stage 0, pre-G0)

**Rejection scope:** the frozen SLR-MYM-1 `liquidity-sweep-and-reclaim` construct (§1: long-only,
09:30–10:15 ET sweep of the nearest level below the open + 1m bar-close reclaim, gated by weekly
**and** daily `vStruct` EMA(20) bullish, stop = sweep extreme − buffer capped at 0.50×ATR(14,daily),
target +1.5R, flat 13:00 ET) proposed as a **same-account third leg sharing the `MYM1!` order symbol**
with the incumbent Striker DJ30→MYM leg — not MYM the instrument, not the `ict-liquidity` mechanism
class generally, not the ICT cascade's weekly `vStruct` finding, not the domain raised bar's route-1
ruling, and not a future expression on an unoccupied symbol or a calendar-disjoint day set.
**Closure date:** 2026-07-29
**Authoritative artifact:** [`SLR-MYM-1-closure-falsified-stage0`](briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) ·
[`SLR-MYM-1-liquidity-sweep-reclaim-scoping`](briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md) (frozen §1 spec, §2.5/§2.6 scoring) ·
[`phase05_census RESULTS`](../lab/archive/slr_mym_phase05_2026-07-29/RESULTS.md)
**Closure basis:** two independent Stage-0 gates fired, either alone decisive; Stages 1–4 never
reached. **0-A admissibility** (ADR 2026-07-26 §2-A four-clause constraint test) — two constraint
framings were drafted (mechanical forced-liquidation; overnight Globex inventory rebalancing at the
RTH open, citing H-OD-1's measured ES +1.444 bp) and **both fail the DELETE test** (removing the
constraint paragraph changes no §1 rule) **and the FLIP test** (reversing the constraint's sign does
not change the trade) — Path 1a ruled unwritable. **0-C day set** (S5 contract-cap ∧ S3 order-symbol
occupancy) — the incumbent Striker DJ30→MYM leg fires Tue/Fri and shares order symbol `MYM1!`; the
venue nets one position per symbol per account, so those two days close structurally regardless of
cap. The best S5+S3-compliant day set (Mon+Wed+Thu), measured by `phase05_census.py` on the local
`MYM_M15.csv` panel (n=141,477 bars, 1,481 scoreable RTH sessions, IS partition n=860,
2019–2023) on a deliberately loose (any-time-of-day) 15m upper-bound proxy, yields **81 IS
entries** against the pre-registered **120-entry floor**. Full-panel entry rate **17.96%**
(266/1,481 sessions); IS-partition **16.63%** (143/860) — power was not the binding constraint; the
day-set/occupancy collision was. $0.00 spent · 0 K consumed · no manifest opened · no
pre-registration authored.
**Surviving finding (NOT rejected):** MYM instrument standing (incumbent Striker DJ30→MYM leg
PF 1.80 / WR 40.3% / n=263, `ops/instruments/MYM.md` M1); the `ict-liquidity` mechanism class
generally, including H-OD-1's measured overnight-inventory effect on ES (+1.444 bp, t≈5.0, 9/9 IS
years positive), which stands independently on its own instrument; the ICT cascade's weekly
`vStruct` RESOLVED finding (leg (a), 0.5571 hit-rate) — only its untested per-entry transfer
(leg (b)) to this 1m expression falls with this closure; the domain raised bar's route-1 ruling
(**GRANTED/CLEAR**, closure §2.7.1) — survives for future candidates; F1 order-symbol occupancy on
shared `MYM1!` — a durable structural constraint, now standing in `ops/instruments/MYM.md`,
that applies to any future same-account MYM leg. **No claim, positive or negative, is made about
sweep-and-reclaim's edge anywhere — the mechanism itself was never scored** (closure §6).
**Re-proposal bar:** needs **both**: (i) a Path-1a four-clause constraint claim that passes the
delete- and flip-tests, **or** a funded Path-1b evidence pass (≥3 decades, ≥3 independent cohorts,
≥1 replication ≥10 yr post-discovery, no known sign-reversal — all four); **and** (ii) an
**unoccupied order symbol**, or a session-disjointness argument that survives F1 and still reaches
the power floor. Neither a re-tuned day set, a different level menu, nor a wider panel clears (i).

<!-- concept-intake-entry mechanism_family="liquidity-sweep-and-reclaim" instrument="MYM" rejection_reason="Stage-0 dual-gate kill, mechanism never tested: 0-A admissibility — both constraint framings (forced-liquidation; overnight-inventory) fail DELETE+FLIP tests (ADR 2026-07-26 §2-A); 0-C day set — S3 order-symbol occupancy on shared MYM1! with incumbent Striker DJ30->MYM (fires Tue/Fri) plus S5 zero free cap on Tue jointly close Tue+Fri; best compliant set (Mon+Wed+Thu) = 81 IS entries vs 120 floor (15m upper-bound proxy, IS n=860)." harness_disposition_ref="SLR-MYM-1 Phase 0.5 census (lab/archive/slr_mym_phase05_2026-07-29/phase05_census.py + RESULTS.md)" date="2026-07-29" class="admissibility-fail+occupancy-fail" role_tested="entry" falsifier_failed="0-A: DELETE+FLIP tests fail both framings (Path 1a unwritable); 0-C: best S5+S3-compliant day set 81 IS entries < 120 floor" addback_condition="(i) Path-1a four-clause constraint claim passing delete/flip, OR funded Path-1b (>=3 decades / >=3 cohorts / >=1 replication >=10yr / no sign-reversal, all four); AND (ii) an unoccupied order symbol or a session-disjointness argument surviving F1 that still reaches the power floor — NOT a re-tuned day set, different level menu, or wider panel" -->

## Queryable index (concept-intake gate, added 2026-06-05)

> ⚠ **CORRECTED 2026-08-08 — the machine consumer described below no longer exists.**
> `validation/concept_intake/` and its `dedup_check()` were deleted with the Gen-1 tree
> (ADR 2026-07-11); verified absent at HEAD. **No program parses the
> `<!-- concept-intake-entry -->` schema today.** The live consumers of this file are
> `scripts/check_advisor_dedup.py` and `scripts/check_status_consistency.py`, neither of
> which reads the structured records.
> ⚠ **Amended 2026-08-09 — that consumer list was incomplete, and the omission is the load-bearing
> one.** A **third** consumer exists and it is a **hard gate**: `ops/instruments/profiles.json`
> carries `source` pointers into this file, consumed by `scripts/instrument_profiles.py` (gate id
> `instrument-profiles`, **tier=always**, `scripts/gates.yml:91-92`), whose `_resolve()` treats a
> missing source as a failure — *"an unsourced claim must fail the gate"*. **Deleting or moving this
> file hard-fails CI today.** So the liveness posture is not "a registry appended-to but never
> read": its *domain-bar* tier is machine-consulted and blocking (verified —
> `python scripts/instrument_profiles.py cell MNQ ict-liquidity` prints `BINDING BAR` and blocks),
> while its *per-direction* tier has no enforcement instrument at all. Those two tiers must be
> reasoned about separately — see [`ADR 2026-08-09`](adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) D2/D3/D4.
> **Forbidden move #4 still binds, and now describes this section's own history** — a
> registry appended-to but never read is a graveyard. The practical control is the
> **executed** dedup attestation: search by mechanism family (including `rg --no-ignore`
> over LTM), and **paste the output**; an attestation that was not run is not an
> attestation. The structured records below are **retained** — they are cheap, and they
> are the ready-made input if a parser is ever rebuilt.

This registry was designed as a **machine-readable control** for the (now retired)
concept-intake gate. `dedup_check(concept)` parsed this file at call time and returned
`CLEAR | DUPLICATE | NEAR_MATCH` using the composite
**(mechanism_family × instrument)** key. The parser read BOTH:

* the prose `### <heading>` directional entries above (e.g. *Guardian-family
  strategy on XAGUSD*) and the pending-list bullets, AND
* structured `<!-- concept-intake-entry ... -->` records auto-appended by the
  harness→registry feedback hook (`validation/concept_intake/feedback.py`) below.

Structured-entry schema (one HTML-comment line per harness rejection, fields
match the §2.4 hook + `validation/disposition.py` `DispositionRecord`):

```
<!-- concept-intake-entry mechanism_family="..." instrument="..."
     rejection_reason="..." harness_disposition_ref="<candidate_id>"
     date="YYYY-MM-DD" -->
```

**Extended attributes (ADR [`2026-06-14-rejected-candidate-patterns.md`](adr/2026-06-14-rejected-candidate-patterns.md) §D, additive).** Hand-authored / ADR-sourced entries from 2026-06-14 also carry `class`, `role_tested`, `falsifier_failed`, `addback_condition`, `config_fingerprint` on the same comment. `dedup` ignores unknown attributes (it keys only on `mechanism_family`×`instrument`), so this is backward-compatible; `role_tested`+`falsifier_failed` are mandatory on new entries. First use: the `mean-reversion-spike-fade × USOIL` entry below.

The four locked-book strategies (Guardian Gold v5.5 / XAUUSD, Striker DJ30 v4.5 /
DJ30, Aegis USDJPY v4.3 / USDJPY, Striker NAS100 v1 / NAS100) are pinned in the
gate's `admissibility_contract.yaml` `locked_book` block and are also dedup
targets. **Additions only** — never edit or delete a prior rejection; the gate's
loop depends on the lineage staying intact.

---

### Exogenous dealer-gamma (GEX) sign regime-gate on the NAS100 ORB

**Rejection scope:** the direction (gate the NAS100 ORB candidate on the sign of prior-close dealer GEX — "negative-gamma-on") is rejected as a **selection/regime-conditioning mechanism**, on the free SqueezeMetrics **SPX cross-index proxy**. Sibling to the HELD/pre-registered-NULL VIX-term-structure gate (`Q-ORB-VIXTS-1`); this is the mechanistically-stronger probe (signed dealer-hedging flow = the N2 post-2020 mechanism itself), run and falsified.
**Closure date:** 2026-06-25
**Class:** edge-failure (the signal carries no orthogonal information **and the pre-registered direction is contradicted**) — NOT a cost-constraint (the gate is free).
**Authoritative artifact:** [`docs/briefs/Q-ORB-GEX-1-closure-falsified.md`](briefs/Q-ORB-GEX-1-closure-falsified.md) (+ pre-registration `e03e72d`, frozen before the run; harness [`lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py`](../lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py) + OUTPUT).
**Closure basis:** pre-registered single cut (family size 1; take the ORB iff prior-trading-day `GEX<0`). Calibration reproduced N1 (n=1666/+0.0853/t2.88 ≈ 1663/+0.0872/2.94); neg-gamma frac 0.117. The negative-gamma cut (n=195) is **flat** (meanR +0.018, t+0.22, perm-p 0.79); the edge is in the positive-gamma complement (opposite to the dealer-momentum hypothesis, and not independently significant, perm-p 0.198). G-info FAIL (p=0.79), G-bestofK FAIL (fw-p=0.80), G-tail FAIL (drop-top-5/10 negative + thin 2025-26 n=17), and the **decisive G-regime-orthogonality FAIL: indicator-t = −0.58 after partialling BOTH |gap| AND OR-range** (corr(GEX,|gap|)=−0.27, corr(GEX,OR-range)=−0.25 → GEX is partly a vol proxy and adds no orthogonal signal in the predicted direction — the same death VIX-TS was pre-registered to die).
**Surviving finding (NOT rejected) — load-bearing:** **exogenous is necessary but not sufficient — the signal must also be orthogonal to |gap|+OR-range, and dealer-gamma-sign is not.** Even the strongest exogenous flow candidate collapsed to a realized-vol proxy under the orthogonality partial. This materially raises the bar for the whole exogenous-ORB-regime thread (now 3 features failed the same battery: overnight-path / gap-conditioned / GEX → at/near tail-exhaustion).
**Re-proposal bar:** **new mechanism evidence** — a fresh single-cut pre-reg on **paid NDX-native** dealer gamma showing a genuine orthogonal separation (would have to restore significance AND flip the contradicted sign), OR a different exogenous flow series (e.g. intraday 0DTE order-flow). NOT a magnitude/threshold sweep, NOT a sign-flip to positive-gamma-on, NOT the same GEX-sign hypothesis re-run on a different feed.

<!-- concept-intake-entry mechanism_family="dealer-gamma-regime-gate" instrument="NAS100" rejection_reason="edge-failure (FALSIFIED): pre-registered single cut (ORB iff prior-close SqueezeMetrics SPX-proxy GEX<0) NULL. Calibration reproduced N1 (n1666/+0.0853/t2.88). neg-gamma cut n195 flat (+0.018/t0.22/perm-p0.79); edge in positive-gamma complement (direction CONTRADICTED, complement perm-p0.198 not sig). G-info FAIL p0.79, G-bestofK FAIL fw-p0.80, G-tail FAIL (drop-top neg; thin 25-26 n17), G-regime-orthogonality FAIL indicator-t=-0.58 after partialling |gap|+OR-range (corr GEX/|gap|=-0.27, GEX/OR=-0.25 -> vol proxy). Leakage clean but wrong-signed. SPX cross-index proxy; NDX-native (paid) only triggered on a PASS." harness_disposition_ref="Q-ORB-GEX-1 (manual pre-registered gate, no harness DispositionRecord; lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_gex_gate.py)" date="2026-06-25" class="edge-failure" role_tested="selection-gate" falsifier_failed="G-regime-orthogonality partial-t -0.58 (|gap|+OR-range); G-info p0.79; G-bestofK fw-p0.80; G-tail neg; direction contradicted" addback_condition="paid NDX-native gamma with demonstrated orthogonal separation OR a different exogenous flow series - not a sweep, sign-flip, or same-hypothesis re-run" config_fingerprint="orb/NAS100_pep/OR2/both/exit@close/rt1.55/cut=GEX<0/feed=SqueezeMetrics-SPX-proxy(sha 27afb7c2)" -->
- **dealer-gamma-regime-gate on NAS100** — rejected 2026-06-25 (edge-failure FALSIFIED: pre-registered ORB-iff-prior-close-GEX<0 NULL; neg-gamma cut flat t0.22, direction contradicted, G-regime-orthogonality partial-t −0.58 after |gap|+OR-range → vol proxy); `Q-ORB-GEX-1` (`docs/briefs/Q-ORB-GEX-1-closure-falsified.md`).

### Exogenous Treasury-term-spread (T10Y3M) sign regime-gate on the NAS100 ORB

**Rejection scope:** the direction (gate the NAS100 ORB candidate on the sign of the prior-day 10y-3m Treasury term spread — "steep-on") is rejected as a **selection/regime-conditioning mechanism**, on the free FRED `T10Y3M` series. The mechanistically-distinct sibling to the GEX gate: a **non-vol-class macro/growth-cycle** signal (the one enumerated candidate that would *survive* the |gap|+OR-range vol partial that killed GEX) — run and falsified for a **different** reason (era-collinearity).
**Closure date:** 2026-06-27
**Class:** edge-failure (the signal carries no orthogonal information **and the pre-registered direction is contradicted**) — NOT a cost-constraint (the gate is free FRED data).
**Authoritative artifact:** [`docs/briefs/Q-ORB-T10Y3M-1-closure-falsified.md`](briefs/Q-ORB-T10Y3M-1-closure-falsified.md) (+ pre-registration `fe7bba5`, frozen before the run; harness [`lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_t10y3m_gate.py`](../lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_t10y3m_gate.py) + OUTPUT).
**Closure basis:** pre-registered single cut (family size 1; take the ORB iff prior-day `T10Y3M>0`, steep-on). Calibration reproduced N1 (n=1666/+0.0853/t2.88); steep frac 0.603. The steep-on cut (n=1005) is **weaker than baseline** (meanR +0.0706, t+1.89, perm-p **0.7109**); the edge is in the **inverted complement** (n=661, +0.1076, t+2.21 — opposite to the steep-growth hypothesis). G-info FAIL (p=0.71), G-bestofK FAIL (fw-p=0.71), G-tail FAIL (thin 2025-26 drop-top-10 −0.0405), G-regime-orthogonality FAIL (indicator-t **−0.44**, wrong sign, after |gap|+OR-range), and the **decisive G-era-confound FAIL: indicator-t = +0.81 (n.s.) after adding year fixed-effects** — the apparent inverted-direction edge collapses once the era is controlled (2023 100% / 2024 95% inverted = the strongest ORB years → "inverted" is a relabel of the N2 2023-24 momentum regime).
**Surviving finding (NOT rejected) — load-bearing (L-T10Y3M-ORB-1):** **exogenous + vol-orthogonal is still not sufficient — a macro-regime series must also be ERA-orthogonal (hold within year, not just across).** T10Y3M is genuinely NOT vol-class (corr to |gap| +0.085 / OR-range +0.164, far below GEX's −0.27/−0.25) — it dodged the vol gate but died on era-collinearity. The orthogonality battery gains a frozen year-FE gate. 4th feature to fail the battery (overnight-path → gap → GEX → T10Y3M); the exogenous-ORB-regime thread is at tail-exhaustion.
**Re-proposal bar:** **new mechanism evidence** — a flow/positioning series that is BOTH vol-orthogonal AND era-orthogonal (varies *within* the post-2020 era): paid NDX-native dealer gamma with demonstrated within-era separation, or a genuine intraday 0DTE order-flow series. NOT a sign-flip to "take iff inverted" (the contradicted direction is the era-confound; it fails G-era-confound at +0.81 n.s.), NOT a construction sweep (T10Y2Y / 2s10s / level), NOT running other macro series and reporting the best.

<!-- concept-intake-entry mechanism_family="term-spread-regime-gate" instrument="NAS100" rejection_reason="edge-failure (FALSIFIED): pre-registered single cut (ORB iff prior-day FRED T10Y3M>0, steep-on) NULL. Calibration reproduced N1 (n1666/+0.0853/t2.88). steep-on cut n1005 weaker than baseline (+0.0706/t1.89/perm-p0.71); edge in inverted complement n661 (+0.1076/t2.21, direction CONTRADICTED). G-info FAIL p0.71, G-bestofK FAIL fw-p0.71, G-tail FAIL (thin 25-26 drop-top-10 -0.0405), G-regime-orthogonality FAIL indicator-t=-0.44 wrong-sign after |gap|+OR-range (corr T10Y3M/|gap|=+0.085, /OR=+0.164 -> NOT vol-class), decisive G-era-confound FAIL indicator-t=+0.81 n.s. after year-FE (era-collinear: 2023 100%/2024 95% inverted = strongest ORB years). Leakage clean. Non-vol macro series; died on era-collinearity not vol-proxy." harness_disposition_ref="Q-ORB-T10Y3M-1 (manual pre-registered gate, no harness DispositionRecord; lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_t10y3m_gate.py)" date="2026-06-27" class="edge-failure" role_tested="selection-gate" falsifier_failed="G-era-confound year-FE indicator-t +0.81 n.s.; G-regime-orthogonality -0.44 wrong-sign; G-info p0.71; G-bestofK fw-p0.71; G-tail thin-25-26 neg; direction contradicted" addback_condition="flow/positioning series vol-orthogonal AND era-orthogonal (within-era separation) - paid NDX-native gamma or intraday 0DTE order-flow; not a sign-flip, construction sweep, or other-macro-series best-of-K" config_fingerprint="orb/NAS100_pep/OR2/both/exit@close/rt1.55/cut=T10Y3M>0/feed=FRED-T10Y3M(sha 95653c84)" -->
- **term-spread-regime-gate on NAS100** — rejected 2026-06-27 (edge-failure FALSIFIED: pre-registered ORB-iff-prior-day-T10Y3M>0 NULL; steep-on cut weaker than baseline t1.89/perm-p0.71, direction contradicted, decisive G-era-confound indicator-t +0.81 n.s. after year-FE → era-collinear relabel of the 2023-24 momentum regime, NOT vol-class); `Q-ORB-T10Y3M-1` (`docs/briefs/Q-ORB-T10Y3M-1-closure-falsified.md`).

### Day-of-week (Friday) selection-gate on the NAS100 ORB

**Rejection scope:** the on-file day-level cut (take the NAS100 ORB only on Fridays) is rejected as a **selection-gate** — a post-hoc pick from the edge-forensics DOW table (Friday n=328, meanR +0.2498, t+3.42, 58% of net). The last `RELIABLE_UNTESTED` on-file lever from the 2026-06-27 improvement map.
**Closure date:** 2026-06-27
**Class:** edge-failure (inside the best-of-K envelope of the eyeballed family + mechanism-less + thin-window-fragile) — NOT a cost-constraint.
**Authoritative artifact:** [`docs/briefs/Q-ORB-FRIDAY-1-closure-falsified.md`](briefs/Q-ORB-FRIDAY-1-closure-falsified.md) (+ pre-registration `711d499`, frozen before the run; harness [`lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_friday_validate.py`](../lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_friday_validate.py) + OUTPUT).
**Closure basis:** **G1 wide-best-of-K FAIL** — corrected over the frozen 24-cut eyeballed family (DOW × month × OR-tercile × hour × side, n≥50), **fw-p 0.0996** (Friday rank 2/24; April max t3.44). The K=5 DOW fw-p 0.021 was the best-of-K trap. **G2 era-confound PASS** (indicator-t +2.79 after \|gap\|+OR-range+year-FE — genuinely within-era robust, positive every year, unlike T10Y3M) — but necessary≠sufficient. **G3 OPEX-flow mechanism FALSIFIED** (triple-witching Fridays WEAKEST t0.47; ordinary Fridays carry it t2.90 → generic end-of-week, no mechanism). **G4 thin-2025-26 tail FAIL** (drop-top-10 −0.0177).
**Surviving finding (NOT rejected) — load-bearing (L-FRIDAY-ORB-1):** **passing the orthogonality/era gates does not rescue a cut inside the selection envelope — best-of-K over the WHOLE eyeballed family is a separate, prior gate for any hand-picked bucket.** A high single-cut t (3.42) is unremarkable once ~24 eyeballed cuts are counted; the right multiplicity universe is the whole battery, not the one dimension the cut came from.
**Re-proposal bar:** **genuinely out-of-sample evidence** — a Friday (or end-of-week) effect that survives wide-family multiplicity on FORWARD or independent data with a pre-specified mechanism, NOT a re-pick from the same forensic table, NOT a Friday×<dimension> intersection (thinner, higher-multiplicity), NOT the OPEX-flow story (falsified here).

<!-- concept-intake-entry mechanism_family="day-of-week-selection-gate" instrument="NAS100" rejection_reason="edge-failure (FALSIFIED): post-hoc Friday-only cut (n328/+0.2498/t3.42/58% of net). G1 wide-best-of-K FAIL fw-p 0.0996 over frozen 24-cut eyeballed family (DOW/month/ORterc/hour/side n>=50; Friday rank 2/24, April max t3.44) -> the K=5 DOW fw-p 0.021 was the best-of-K trap. G2 era-confound PASS (+2.79 after |gap|+OR-range+year-FE, within-era robust, positive every year). G3 OPEX-flow mechanism FALSIFIED (triple-witching weakest t0.47, ordinary-Fri t2.90 -> generic end-of-week, no mechanism). G4 thin-2025-26 tail FAIL (drop-top-10 -0.0177). Robust-within-sample but inside selection envelope + mechanism-less + thin-fragile." harness_disposition_ref="Q-ORB-FRIDAY-1 (manual pre-registered gate; lab/analysis/orb/orb_universe_2026-06-22/nas100_orb_friday_validate.py)" date="2026-06-27" class="edge-failure" role_tested="selection-gate" falsifier_failed="G1 wide-best-of-K fw-p 0.0996 (24-cut family); G4 thin-25-26 drop-top-10 -0.0177; G3 OPEX-flow mechanism contradicted (TW weakest t0.47)" addback_condition="forward/independent OOS Friday effect surviving wide-family multiplicity with a pre-specified mechanism - not a re-pick from the same table, Friday-x-dimension intersection, or the falsified OPEX-flow story" config_fingerprint="orb/NAS100_pep/OR2/both/exit@close/rt1.55/cut=dow==Fri/family=24cut-eyeballed" -->
- **day-of-week-selection-gate on NAS100** — rejected 2026-06-27 (edge-failure FALSIFIED: post-hoc Friday-only cut; G1 wide-best-of-K FAIL fw-p 0.0996 over the 24-cut eyeballed family (rank 2/24) → the K=5 DOW fw-p 0.021 was best-of-K; G2 era-confound PASS +2.79 but G3 OPEX mechanism falsified + G4 thin-25-26 tail fail); `Q-ORB-FRIDAY-1` (`docs/briefs/Q-ORB-FRIDAY-1-closure-falsified.md`).

### Intraday mean-reversion on micro Treasury-yield futures (Micro 10Y / 2YY) — chop-native 5th-leg candidate

**Rejection scope:** the direction (single-instrument intraday range-fade mean-reversion on CME Micro 10Y/2YY yield futures, proposed as a concurrent chop-native 5th leg under the 2026-06-29 futures-prop venue) is rejected as an **entry** mechanism. Top-scored survivor (26/100) of the 8-family chop-native sweep — clears cost + venue-eligibility + novelty, killed on the era/tail wall.
**Closure date:** 2026-06-30
**Class:** edge-failure (no standalone edge) + regime/tail-co-occurrence (the binding kill)
**Authoritative artifact:** [`lab/archive/chop_native_leg_2026-06-30/RESULTS.md`](../lab/archive/chop_native_leg_2026-06-30/RESULTS.md) §3 + harness [`rates_era_split.py`](../lab/archive/chop_native_leg_2026-06-30/rates_era_split.py) (pre-registered kill rule frozen before scoring).
**Closure basis:** free-data 2022-rates era-split (cheapest falsifier, NOT a full Pre-Q) on Yahoo `^TNX` (10Y) / `^FVX` (5Y) daily 2010-2026 — a daily proxy that tests the **regime/tail-co-occurrence mechanism**, the disqualifier. 2022 was a violent one-directional rates selloff (10Y 1.63%→3.88%, +2.25pp), so a range-fade was **short a relentless uptrend through the 2020-2023 H1 chop window** = the Aegis-USDJPY-2022 bleed mode. Canonical daily fade (z=(y−SMA20)/SD20, fade |z|≥1): **worst year 2022 (10Y −124bp / 5Y −116bp, hit 44%); H1 net-negative both tenors (Sharpe −0.31 / −0.47)** → K1 (tail co-occurrence) fires: the leg deepens the book's H1 co-drawdown rather than offsetting it. K2 (era-relabel) does not fire but the **PRE-2020 edge is economically zero** (Sharpe +0.22 / +0.31, mean ~+0.07 bp/day) — no standalone edge to insert, let alone after-cost PF≈2.0. Robust across the 3×3 n/thr grid (only barely-trading thr=1.5 dodges 2022, and even there no PRE-and-H1-positive cell). The only published standalone rates-MR result (jerryxyx curve-cointegration Sharpe 1.98) is a 2017 single-year **different** mechanism.
**Re-proposal bar:** **new mechanism evidence** — a *chop-specific* exogenous-conditioned rates edge (an entry whose P&L is generated in directionless rates ranges AND that is vol-orthogonal + within-era robust), NOT a lookback/threshold re-tune, a different tenor, or a longer panel. A daily-proxy caveat applies: a genuinely pure-intraday rates edge that leaves no daily trace would need a Micro-10Y 15m panel (none in-repo) — but its tail still co-occurs with 2022, so the bar additionally requires showing the worst drawdown does NOT land in the H1 trend window.

<!-- concept-intake-entry mechanism_family="rates-intraday-mean-reversion" instrument="MICRO10Y" rejection_reason="edge-failure + regime/tail-co-occurrence (FALSIFIED): single-instrument intraday range-fade MR on CME Micro 10Y/2YY yield futures, proposed as a chop-native 5th leg under the 2026-06-29 futures-prop pivot. Free-data 2022 era-split (cheapest falsifier, NOT a full Pre-Q) on Yahoo ^TNX/^FVX daily 2010-2026 (FRED/Stooq egress-blocked). 2022 rates were a violent one-directional selloff (10Y 1.63->3.88%, +2.25pp), so a fade was short a relentless uptrend through the 2020-2023 H1 chop window. Canonical daily fade z=(y-SMA20)/SD20 fade|z|>=1: WORST YEAR 2022 (10Y -124bp/5Y -116bp, hit 44%), H1 net-negative both tenors (Sharpe -0.31/-0.47) -> K1 tail co-occurrence FIRES (deepens the book H1 co-drawdown). K2 era-relabel does not fire but PRE-2020 edge economically zero (Sharpe +0.22/+0.31, mean ~+0.07bp/day) << PF2.0. Robust across 3x3 n/thr grid. Daily proxy for a 15m fade -- disqualifier is regime-level (2022 trended at all timescales)." harness_disposition_ref="chop-native-leg-sweep (top survivor, manual era-split falsifier; lab/analysis/chop_native_leg_2026-06-30/CARD.md)" date="2026-06-30" class="edge-failure+regime-tail-co-occurrence" role_tested="entry" falsifier_failed="2022 era-split: worst year 2022 (-124bp 10Y/-116bp 5Y); H1 Sharpe -0.31/-0.47 net-negative; PRE-2020 Sharpe +0.22/+0.31 economically zero; grid-robust; tail co-occurs with H1" addback_condition="chop-specific exogenous-conditioned rates edge, vol-orthogonal + within-era robust, with the worst drawdown NOT in the H1 trend window - NOT a lookback/threshold re-tune, different tenor, or longer panel" config_fingerprint="rates-MR/MICRO10Y2YY/daily-proxy/z=(y-SMA20)/SD20/fade|z|>=1/h=1d/feed=Yahoo-^TNX-^FVX-2010-2026" -->
- **rates-intraday-mean-reversion on MICRO10Y/2YY** — rejected 2026-06-30 (edge-failure + tail-co-occurrence FALSIFIED: chop-native 5th-leg top survivor; free-data 2022 era-split — worst year 2022 (−124bp 10Y), H1 Sharpe −0.31, PRE-2020 Sharpe +0.22 ≈ economically zero; a fade is short the 2022 one-directional rates uptrend through the H1 window → deepens the co-drawdown); `lab/archive/chop_native_leg_2026-06-30/RESULTS.md` §3.

### Index dispersion / correlation-risk-premium (sell index vol, buy single-name vol) on SPX500 — chop-native 5th-leg candidate

**Rejection scope:** the direction (harvest the implied-correlation premium — short index volatility / long single-name volatility — as a concurrent chop-native 5th leg) is rejected on **venue** grounds (decisive) + co-occurring left tail. The most mechanistically chop-native concept of the survey; killed pre-build at the venue falsifier.
**Closure date:** 2026-06-30
**Class:** venue-constraint (decisive) + regime/tail-co-occurrence
**Authoritative artifact:** [`lab/archive/chop_native_leg_2026-06-30/RESULTS.md`](../lab/archive/chop_native_leg_2026-06-30/RESULTS.md) §4.
**Closure basis:** one-page venue falsifier (pre-registered: venue decisive, tail secondary). (1) **Venue INELIGIBLE** — dispersion needs an options book (index + single-name); US futures-prop firms (Apex/Topstep/Bulenox) are **futures-only, no equity/single-stock options**, and the only single-instrument proxy, Cboe **DSPX** (launched Sept-2023), has **no listed tradable future/option** (it is a benchmark index — "may be used in future as the basis of listed/unlisted derivatives"). Not a futures product at all — a *harder* kill than short-vol (VX is at least a future, on the wrong exchange CFE). (2) **Tail WRONG-SIGN** — the short-correlation harvest blows up when realized correlation spikes to ~1 in systemic risk-off (2008, Feb-2018, Mar-2020) = the same H1 risk-off window the long-biased book co-draws → deepens the co-drawdown. **Structural finding:** the entire vol/correlation-risk-premium branch (short-vol, dispersion, gamma-scalp, IV-calendar-spread) is uniformly venue-blocked because the futures-prop venue is **options-free**; the futures pivot opens the cost wall but NOT the most-chop-native branch.
**Re-proposal bar:** an **options-capable venue** outside the futures-prop scaling path (the futures-prop pivot is the binding constraint, not the strategy), OR a **listed, routable DSPX derivative** — plus evidence the harvest tail does not co-occur with the book's risk-off window. NOT a re-spec of the options legs, a different index, or an OTC/variance-swap construct that no retail-accessible venue offers.

<!-- concept-intake-entry mechanism_family="index-dispersion-correlation-premium" instrument="SPX500" rejection_reason="venue-constraint (decisive) + regime/tail-co-occurrence: harvest the implied-correlation premium (short index vol / long single-name vol) as a chop-native 5th leg. Killed pre-build at the venue falsifier 2026-06-30. (1) VENUE INELIGIBLE - needs an options book (index + single-name); US futures-prop firms (Apex/Topstep/Bulenox) are futures-only (no equity/single-stock options); only proxy Cboe DSPX (Sept-2023) has NO listed tradable future/option (benchmark index only). Harder kill than short-vol (not a futures product at all). (2) TAIL WRONG-SIGN - short-correlation blows up when realized corr spikes to ~1 in systemic risk-off (2008/Feb-2018/Mar-2020) = the H1 window the book co-draws. Structural: entire vol/correlation-RP branch (short-vol/dispersion/gamma-scalp/IV-calendar) uniformly venue-blocked because futures-prop venue is options-free." harness_disposition_ref="chop-native-leg-sweep (un-scored-gap, manual venue falsifier; lab/analysis/chop_native_leg_2026-06-30/CARD.md)" date="2026-06-30" class="venue-constraint+regime-tail-co-occurrence" role_tested="entry" falsifier_failed="venue: futures-prop firms futures-only (no equity/single-stock options); Cboe DSPX no listed tradable derivative; + short-correlation tail co-occurs with H1 risk-off (2008/2018/2020)" addback_condition="an options-capable venue outside the futures-prop scaling path OR a listed routable DSPX derivative, plus a harvest tail that does NOT co-occur with the book risk-off window - not an options-leg re-spec, different index, or OTC variance-swap construct no retail venue offers" config_fingerprint="dispersion/SPX500/sell-index-vol+buy-single-name-vol/proxy=DSPX-untradable/venue=futures-prop-options-free" -->
- **index-dispersion-correlation-premium on SPX500** — rejected 2026-06-30 (venue-constraint + tail-co-occurrence: most chop-native concept of the survey; futures-prop firms are options-free (no equity/single-stock options), Cboe DSPX has no listed tradable derivative, and the short-correlation harvest tail co-occurs with H1 risk-off); `lab/archive/chop_native_leg_2026-06-30/RESULTS.md` §4.

### Opening-range breakout (ORB) on 30Y Treasury futures (ZB)

**Rejection scope:** the direction (the ORB-MNQ-1 opening-range-breakout construct — 30-min OR from the 09:30 ET open, both-sides touch-fill, stop = opposite OR extreme, exit-at-close — transplanted to **ZB** as a *risk-off-decorrelated large-δ leg*) is rejected as an **entry** mechanism. Proposed to thread the Q-COMPOSE-1 / decompound-HOLD "vise" (a cost-viable breakout that is *counter-cyclical* to the index-momentum book); killed at the cheapest Phase-0 falsifier.
**Closure date:** 2026-07-20
**Class:** edge-failure (primary — negative gross edge) + venue/cost-geometry (secondary)
**Authoritative artifact:** [`lab/archive/orb_zb_recon_2026-07/RESULTS.md`](../lab/archive/orb_zb_recon_2026-07/RESULTS.md) + scoping/pre-reg [`docs/briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md`](briefs/rnd-pipeline/ORB-ZB-1-risk-off-decorrelated-breakout-scoping.md).
**Closure basis:** K=0 δ-extraction on native `ZB.v.0` (Databento GLBX, `$0.00`, 1m→15m ET, 2019-2026, n=1,853), reusing the calibration-pinned `orb_lib.orb_backtest` engine verbatim. **Mean GROSS edge negative in every window** (full −0.0480 R t−1.61; 2021+ −0.0293; 2019 −0.0686; 2020 −0.1379) → cost-law ratio negative (−0.20× headline / −10.66× even at 0-slip commission-only); net PF 0.59, WR 0.34. The within-day OR-window placebo (2021+, **p=0.0010**) confirms it structurally but sign-reversed: the real 09:30 OR breakout (−0.265 R) is merely *less* loss-making than arbitrary-window breakouts (placebo mean −0.545 R) — **breakouts lose on every intraday window; ZB fades its opening range rather than continuing it.** Cost geometry is independently hostile (median OR 10 ticks vs ~2-tick RT → cost_R 0.235 R, 4× hurdle 0.94 R) but moot under the negative sign.
**Surviving finding (NOT rejected) — load-bearing:** **opening-range momentum is an equity-index property; it does not transfer to Treasuries (ZB shows opening-range mean-reversion).** This *tightens the vise* — the one cost-viable mechanism class (large-δ index intraday breakout) is mechanistically tied to the equity-index book the locked/c1 legs already harvest, so cost-survival and decorrelation are in tension by construction, not merely empirically (Q-COMPOSE-1).
**Re-proposal bar:** **new mechanism evidence** for a *different* ZB construct — NOT an anchor re-tune (09:30 → 08:30 bond-data window) or a param sweep of this breakout (the named degeneration move; brief §5 forbids it). A ZB **mean-reversion / fade** is the sign-consistent direction but is a distinct mechanism with its own intake, and inherits both an adverse cost geometry (10-tick OR vs 2-tick RT) and the dead rates-intraday-MR precedent (MICRO10Y/2YY above).
**⛔ Venue-availability bar (added 2026-07-22 — independent of, and additional to, the edge verdict):** **the entire US Treasury complex is untradable at the registered firm.** ZB/ZN/ZF/ZT/UB are absent from Tradeify's supported products ([article 10468222](https://help.tradeify.co/en/articles/10468222), article-dated 2026-05-20, verified 2026-07-22); the only rates products are **EUREX bonds (FGBX/FGBS/FGBM/FGBL)**. This applies equally to the sibling rates closures **H-ZNAUC-1** (ZN) and **RATES-EV-ZF-1** (ZF). Any successor proposing a Treasury construct **for the c1 account must clear venue availability first** — before edge, cost-law, or decorrelation is even measured — and must either re-express on EUREX bonds or name a different firm. Note the cost bases in these closures were computed on **Bulenox $0.61**, not the registered firm's schedule, so they never priced this venue in the first place.

<!-- concept-intake-entry mechanism_family="opening-range-breakout" instrument="ZB" rejection_reason="edge-failure (negative gross edge) + venue/cost-geometry: ORB-MNQ-1 opening-range-breakout construct (30-min OR from 09:30 ET, both-sides touch-fill, exit-at-close) transplanted to ZB (30Y T-bond) as a risk-off-decorrelated large-delta leg. K=0 delta-extraction on native ZB.v.0 (Databento GLBX, $0.00, 1m->15m ET, 2019-2026, n=1853), orb_lib.orb_backtest verbatim. Mean GROSS edge negative EVERY window (full -0.0480R t-1.61; 2021+ -0.0293; 2019 -0.0686; 2020 -0.1379) -> cost-law ratio -0.20x headline / -10.66x at 0-slip; net PF 0.59 WR 0.34. Within-day OR placebo p=0.0010 sign-reversed (real OR -0.265R LESS loss-making than arbitrary-window -0.545R -> ZB fades the opening range). Cost geometry hostile (median OR 10 ticks vs ~2-tick RT, cost_R 0.235R, 4x hurdle 0.94R) but moot under negative sign. Load-bearing: opening-range MOMENTUM is equity-index-specific; ZB shows opening-range MEAN-REVERSION." harness_disposition_ref="ORB-ZB-1 Phase-0 (K=0 delta-extraction, no harness DispositionRecord; lab/archive/orb_zb_recon_2026-07/RESULTS.md)" date="2026-07-20" class="edge-failure+venue-cost-geometry" role_tested="entry" falsifier_failed="P0.1 cost-law: negative gross edge every window (-0.20x headline, -10.66x 0-slip); within-day placebo p=0.0010 sign-reversed (breakouts lose every window; OR least-bad); net PF 0.59" addback_condition="NEW mechanism for a different ZB construct - NOT an anchor re-tune (09:30->08:30) or param sweep of this breakout; a ZB fade is a distinct mechanism with its own intake + adverse cost geometry" config_fingerprint="orb/ZB.v.0/OR2x15m@09:30ET/both/exit@close/rt=0.06372pt(Bulenox$0.61+1tick)/feed=databento-GLBX-ZB.v.0-1m(d2f56c0d)" -->
- **opening-range-breakout on ZB** — rejected 2026-07-20 (edge-failure + venue/cost-geometry: ORB-MNQ construct transplanted to the 30Y T-bond as a risk-off-decorrelated large-δ leg; K=0 δ-extraction on native ZB.v.0 (Databento, $0.00, n=1,853) → **negative gross edge every window** (full −0.048 R, −0.20× headline / −10.66× at 0-slip), within-day placebo p=0.0010 sign-reversed → ZB *fades* its 09:30 opening range; opening-range momentum is equity-index-specific); `lab/archive/orb_zb_recon_2026-07/RESULTS.md`.

### Short-NG announcement-bracket premium on weekly EIA storage days

**Rejection scope:** the direction (short NYMEX Henry Hub Natural Gas across the **post**-announcement window of the weekly EIA Natural Gas Storage Report — short ~10:25 ET blind entry ahead of the 10:30 ET release, cover 11:00 ET) is rejected as an **entry** mechanism. Sourced via the external-mechanism harvest lane (`strategy_harvest.md`); the only candidate this program screened with a target-cohort, peer-reviewed, net-of-cost published δ (~23bp/event, ~6× the estimated RT cost) — and it still died at the cheapest Phase-0 falsifier.
**Closure date:** 2026-07-21
**Class:** edge-failure (δ not distinguishable from zero on the native micro-era, sign-unstable) + venue/cost-geometry (secondary — the point estimate is also ~3.6× under the realistic-cost hurdle)
**Authoritative artifact:** [`lab/archive/ng_eia_recon_2026-07/RESULTS.md`](../lab/archive/ng_eia_recon_2026-07/RESULTS.md) + scoping/pre-reg [`docs/briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md`](briefs/rnd-pipeline/NG-EIA-1-announcement-bracket-premium-scoping.md).
**Closure basis:** K=0 δ-extraction on native `NG.v.0` (Databento GLBX, `$0.00`, n=323 primary-BLS-and-EIA-schedule-sourced events 2019–2026, holiday-ambiguous weeks conservatively dropped). **Construct-definition correction applied before this run**: the source paper's citable δ (Prokopczuk/Wese Simen/Wichmann, *Energy Journal* 2021 — 12%/yr net, t=2.93) attaches only to the **post**-announcement window; the pre-announcement half is surprise-conditional (verified: "entirely generated on days when storage levels exceed analysts' expectations") — the exact F-B/CL-EIA informed-flow trap, excluded from PRIMARY. On the corrected, post-only construct: **δ = +8.30bp (σ 159.7bp, δ/σ 0.052, t +0.93)** — Req-4 power **FAIL** (0.052 vs the N=323 floor 0.109) and Req-5 cost-law **KILL** (8.30bp vs the 4×-hurdle 29.6bp, ~3.6× under). Faithfulness anchor clean (mean |m0| 50.7bp — larger than F-B's own 25.6bp, confirming correct event dating; the null is real, not a dating defect). Per-year delta **alternates sign nearly every year** (2019 +20 / 2020 −4 / 2021 −3 / 2022 −13 / 2023 −7 / 2024 +10 / 2025 +41 / 2026 +37) — the signature of sampling noise around a true-zero effect, not a decaying-but-real premium. SANITY-1 (the wider pre+post bracket) offers no rescue (δ +9.42bp, t +0.95 — comparable, not larger enough to matter).
**Surviving finding (NOT rejected) — load-bearing:** the source paper's own Requirement-1 weakness (framed by its authors as an unresolved "puzzle," sign-inverted vs standard announcement-risk-premium theory, no independent-cohort replication for the directional claim — R1-PENDING at admission) is **empirically corroborated**: the modern native-micro-era post-window premium is statistically indistinguishable from zero. A large, real release reaction (confirmed) does not imply a harvestable *directional* premium around it — R1-PENDING is not a formality; it can and did resolve to not-confirmed.
**Re-proposal bar:** **new mechanism evidence** for a *different* NG construct — NOT a re-tune of the bracket window (entry lead time, hold length) or a re-read of the same paper's numbers; the construct was already corrected once (pre+post → post-only) before this closure and the corrected version is still what died.

<!-- concept-intake-entry mechanism_family="announcement-bracket-risk-premium" instrument="NG" rejection_reason="edge-failure (delta not distinguishable from zero, sign-unstable) + venue/cost-geometry (secondary): short NG across the POST-ONLY EIA storage-report window (10:25->11:00 ET), corrected before run from a pre+post draft (pre-leg is surprise-conditional per source-paper verification, the F-B/CL-EIA trap). K=0 delta-extraction on native NG.v.0 (Databento, $0.00, n=323, 2019-2026, EIA-schedule-sourced calendar with holiday-ambiguous weeks dropped). delta=+8.30bp (sigma 159.7bp, delta/sigma 0.052, t+0.93). Req-4 power FAIL (0.052 vs 0.109 floor at N=323). Req-5 cost-law KILL (8.30bp vs 29.6bp 4x-hurdle, ~3.6x under). Faithfulness anchor clean (|m0|=50.7bp, larger than F-B's 25.6bp -- correct dating, real null). Per-year sign alternates nearly every year (noise signature, not decay). SANITY-1 wider bracket no rescue (+9.42bp t+0.95)." harness_disposition_ref="NG-EIA-1 Phase-0 (K=0 delta-extraction, no harness DispositionRecord; lab/archive/ng_eia_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure+venue-cost-geometry" role_tested="entry" falsifier_failed="Req-4 power 0.052 vs 0.109 floor; Req-5 cost-law 8.30bp vs 29.6bp hurdle (~3.6x under); per-year sign alternates (noise)" addback_condition="NEW mechanism evidence for a different NG construct - NOT a bracket-window re-tune; the construct was already corrected once (pre+post->post-only) before this closure" config_fingerprint="eia-bracket/NG/short-10:25->11:00ET/K=0/feed=databento-GLBX-NG.v.0-1m(718110b3)/calendar=ir.eia.gov-ngs-schedule-2019-2026" -->
- **announcement-bracket-risk-premium on NG** — rejected 2026-07-21 (edge-failure + venue/cost-geometry: post-only EIA storage-bracket short, corrected before run from a pre+post draft that would have re-imported the F-B/CL-EIA surprise-conditional trap; K=0 δ-extraction on native NG.v.0 (Databento, $0.00, n=323) → **δ not distinguishable from zero** (+8.30bp, δ/σ 0.052, t+0.93), Req-4 power FAIL, Req-5 cost-law KILL (~3.6× under); per-year sign alternates — noise, not the paper's claimed decaying premium; faithfulness anchor clean, so the null is real); `lab/archive/ng_eia_recon_2026-07/RESULTS.md`.

### Conditional event-anchored opening-range breakout on 5Y Treasury futures (ZF)

**Rejection scope:** the direction (the ORB-MNQ-1/ORB-ZB-1 opening-range-breakout construct, OR-anchored at the 08:30 ET CPI/NFP release instead of the equity cash open, day-filtered to CPI+NFP announcement days only, on the CBOT 5-Year T-Note) is rejected as an **entry** mechanism — the one previously-untested cell in the program's rates-event 2×2 matrix (unconditional-drift × conditional-drift × unconditional-breakout × **conditional-breakout**), now closing the matrix fully dead.
**Closure date:** 2026-07-21
**Class:** edge-failure (marginal, cost-walled, underpowered) — explicitly **NOT** venue/cost-geometry and **NOT** decorrelation-failure; both of those limbs independently *passed*.
**Authoritative artifact:** [`lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md`](../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md) + scoping/pre-reg [`docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md`](briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md).
**Closure basis:** K=0 δ-extraction (pre-committed PRIMARY+SECONDARY K_intrinsic=2 design; `register_search` never opened) on native `ZF.v.0` (Databento GLBX, `$0.00`, n=143 event-day breakouts from 179 CPI+NFP events, primary-sourced from `bls.gov`'s 8 per-year schedule pages via browser — **not** a first-Friday heuristic; sourcing independently confirmed the 2025 government-shutdown reference-month gap a prior-session memory had already flagged). **Two limbs of the four-part gate PASSED**: P0.1 event-day range geometry **17.62:1** (vs ZB's unconditional 4.3:1 — the instrument-choice thesis validated) and P0.5 decorrelation ρ **0.280** (zero-padded daily-$ series, honestly reflecting the construct's 6.1%-in-market sparsity — the "sparse by construction" thesis validated). **Two limbs FAILED, and those are the ones that matter**: P0.2 PRIMARY cost-law **KILL** at the realistic headline convention (mean gross +0.1033R, t+1.45 — not significant; ratio 1.15× vs the 4.0× bar, though it clears trivially at an unrealistic 0-slip floor, 15.94×) and P0.4 power **FAIL** (0.3047 vs the 0.50 bar). The within-day placebo (p=0.0010) is informative, not a rescue: on event days, arbitrary-window breakouts are strongly negative (−0.39 mean) while the actual OR window is merely flat (+0.014) — the OR window is "the least bad," not a real edge. SECONDARY (top-half-by-OR-range subcohort) does not rescue it either (0.74× ratio, net-negative). Per-year delta alternates sign nearly every year — the identical noise signature that closed the sibling NG-EIA-1 candidate the same day.
**Surviving finding (NOT rejected) — load-bearing:** **cost-geometry and decorrelation are necessary but not sufficient — an edge still has to exist.** On genuine Treasury-complex instruments this program has now tested three distinct entry-construct shapes — auction-day drift (ZN, H-ZNAUC-1), unconditional intraday breakout (ZB, ORB-ZB-1), conditional (CPI/NFP) intraday breakout (ZF, this closure) — three independently-verified, distinct failure modes, zero survivors. (CL-EIA/F-B is an *adjacent* informed-flow precedent on a different instrument class, not a fourth rates-instrument cell; a "conditional fixed-hold drift" construct — release-anchored, no breakout/stop structure — was never itself run on any Treasury instrument and is not claimed dead here.) The instrument-selection and construct-engineering discipline (better tick geometry, event-conditioning, sparse-exposure decorrelation) all worked exactly as designed — the market simply does not pay this program's book for showing up with the right tools if there is no edge underneath.
**Re-proposal bar:** **new mechanism evidence** — a rates construct that is not a re-tune of the event set, OR-anchor window, or instrument within this same conditional-breakout shape (that shape is now closed at N=143/power=0.30, and widening N by adding more macro-release types is a fresh manifest, not a re-run of this one). **Tail-methodology-exhaustion note (INQHIORI §6, not a formal domain-SNAG closure — this file's own domain-SNAG precedent below is calibrated to ~17–22 candidates, a different scale):** this is the third directional (drift/breakout) construct on a Treasury-complex instrument to close dead, sharing the parent question "does a directional entry construct clear cost on this complex" at the same analysis level (H-ZNAUC-1 → ORB-ZB-1 → this). Per the guardrail, a fourth directional construct at this level should not be funded without reformulating the question — mean-reversion/fade (a different level/shape entirely, genuinely untested at native-intraday resolution) is not barred by this note.

<!-- concept-intake-entry mechanism_family="conditional-event-anchored-orb" instrument="ZF" rejection_reason="edge-failure (marginal, cost-walled, underpowered) -- NOT venue/cost-geometry, NOT decorrelation-failure (both passed). ORB-MNQ/ORB-ZB construct OR-anchored at 08:30 ET CPI/NFP release, day-filtered to event days, on CBOT 5Y T-Note. K=0 delta-extraction (PRIMARY+SECONDARY K_intrinsic=2 pre-committed) on native ZF.v.0 (Databento, $0.00, n=143 of 179 CPI+NFP events, primary-BLS-sourced). P0.1 geometry PASS (17.62:1 vs ZB unconditional 4.3:1). P0.5 decorrelation PASS (rho=0.280, zero-padded). P0.2 PRIMARY cost-law KILL (mean gross +0.1033R t+1.45 n.s.; headline ratio 1.15x vs 4.0x bar; passes trivially at unrealistic 0-slip 15.94x). P0.4 power FAIL (0.3047 vs 0.50 bar). Placebo p=0.0010 informative not rescue (arbitrary-window breakouts strongly negative -0.39 on event days; OR window merely flat +0.014 -- least-bad not real edge). SECONDARY top-half-range subcohort no rescue (0.74x, net-negative). Per-year sign alternates (same noise signature as sibling NG-EIA-1 same day). Third of three distinct directional entry-construct shapes tested on genuine Treasury-complex instruments this session (ZN auction-drift H-ZNAUC-1; ZB unconditional-breakout ORB-ZB-1; ZF conditional-breakout, this closure) -- 0 survivors, 3 distinct failure modes; tail-methodology-exhaustion per INQHIORI §6 (not a formal domain-SNAG closure -- that bar in this file is calibrated to ~17-22 candidates, a different scale). CL-EIA/F-B is an adjacent informed-flow precedent on a DIFFERENT instrument (crude oil), not a fourth rates cell; a fixed-hold conditional-drift construct (no breakout/stop) was never itself run on a Treasury instrument." harness_disposition_ref="RATES-EV-ZF-1 Phase-0 (K=0 delta-extraction, no harness DispositionRecord; lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure" role_tested="entry" falsifier_failed="P0.2 cost-law 1.15x vs 4.0x bar; P0.4 power 0.3047 vs 0.50 bar; per-year sign alternates (noise)" addback_condition="NEW mechanism evidence not a re-tune of event-set/OR-window/instrument within this conditional-breakout shape (closed at N=143/power=0.30); a 4th directional Treasury-complex construct at the same analysis level needs the parent question reformulated per INQHIORI §6, not just a new instrument/window" config_fingerprint="orb-event/ZF.v.0/OR2x15m@08:30ET-CPI+NFP/both/exit@15:00ET/rt=0.01685pt(Bulenox$0.61+1tick$7.8125)/feed=databento-GLBX-ZF.v.0-1m(3af3c763)/calendar=bls.gov-8yr-schedule-2019-2026(179events)" -->
- **conditional-event-anchored-orb on ZF** — rejected 2026-07-21 (edge-failure — marginal/cost-walled/underpowered, explicitly NOT a geometry or decorrelation failure: both of those PASSED; the ORB construct OR-anchored at the CPI/NFP 08:30 ET release, day-filtered to 179 primary-BLS-sourced events; K=0 δ-extraction on native ZF.v.0 (Databento, $0.00, n=143) → P0.1 geometry 17.62:1 PASS, P0.5 ρ=0.280 PASS, but **P0.2 cost-law KILL** (1.15× vs 4.0×, t+1.45 n.s.) and **P0.4 power FAIL** (0.30 vs 0.50); per-year sign alternates — same noise signature as NG-EIA-1 the same day; third of three distinct directional constructs on the Treasury complex, 0 survivors — tail-methodology-exhaustion per INQHIORI §6); `lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md`.

### Cross-index relative-volume ranking (Stocks-in-Play analogue) on equity-index futures

**Rejection scope:** the direction (recover the Zarattini "Stocks in Play" cross-sectional ORB selection edge by ranking a small universe of US equity-index futures — ES/NQ/YM/RTY — on opening relative volume and trading the ORB only on the most "in-play" index each day) is rejected as a **selection/rotation** mechanism. Surfaced as one of two untested threads from the 2026-07-21 prop-fundable-archetype deep-search (open question #3); killed at the cheapest necessary-condition falsifier on the 2-index universe we hold intraday.
**Closure date:** 2026-07-21
**Class:** edge-failure (the selection *dilutes* rather than concentrates edge — strictly dominated by the incumbent single-instrument ORB-MNQ) + data/universe-constraint (secondary — the 4–6-way ES/NQ/YM/RTY universe is unavailable without a real ES+RTY intraday pull).
**Authoritative artifact:** [`lab/archive/xindex_rv_recon_2026-07/RESULTS.md`](../lab/archive/xindex_rv_recon_2026-07/RESULTS.md) + `run_probe.py`.
**Closure basis:** cheapest-falsifier necessary-condition pre-screen (Notice-phase, cached data, **no K bound**) on the widest-spread US large-cap pair we hold intraday — Nasdaq (`MNQ_M15`) vs Dow (`MYM_M15`), 1,534 common RTH sessions 2020-07→2026-07. **(A) DISPERSION** compressed-but-non-zero: `corr(RV_nq,RV_ym)=0.717`, 68% of days RV within ±25%. **(B) PREDICTIVENESS** fails on the metric that matters: the higher-RV index has a marginally bigger same-day \|move\| (+1.86 bp, sign-p 0.008) but **NOT** a better ORB edge (win 0.487, +0.22 bp, sign-p 0.329 — null, slightly wrong-signed). **Killer stat:** RV-rank selection captures **+2.64 bp** ORB edge vs +2.39 bp random and vs **+5.19 bp for always trading MNQ alone** (MYM ORB unconditional −0.35 bp) — the rotation gives *half* the incumbent single-instrument edge because ~half the days RV selects the weaker index (Dow). The Stocks-in-Play mechanism (in-play → better breakout) does not fire: in-play predicts a bigger but not more *directional* move (whipsaw, not edge).
**Surviving finding (NOT rejected) — load-bearing:** the cross-index ranking is **strictly dominated by the incumbent single-instrument ORB-MNQ** — index aggregation compresses the idiosyncratic dispersion that makes Stocks-in-Play work (1,000-stock cross-section → 4–6 co-moving broad baskets), so a small-universe RV ranking harvests weak factor-rotation noise. This specializes the **venue-wall** pattern: the *strong* documented intraday edge (Stocks-in-Play, Sharpe 2.8) needs a **single-stock cross-section the futures-prop venue cannot host** — same class as crypto-trend (venue-walled) and dispersion/short-vol (options-free venue).
**Re-proposal bar:** **new mechanism evidence** — a scoped **ES + RTY intraday pull** demonstrating that adding small-cap (RTY) idiosyncrasy raises cross-sectional RV dispersion AND that higher-RV then predicts a *better* ORB edge (the (B) limb that failed here). This is a **DEFER-procurement** trigger with a poor prior — NOT a re-tune of the RV window (opening-30m / 14-session lookback), the ORB construct, or the 2-index universe (the exhausted moves); adding **ES alone** is inadmissible (it sits between Nasdaq and Dow — more homogeneous, cannot rescue dispersion).

<!-- concept-intake-entry mechanism_family="cross-index-relative-volume-ranking" instrument="ES-NQ-YM-index-futures" rejection_reason="edge-failure (selection dilutes not concentrates) + data/universe-constraint: recover the Zarattini Stocks-in-Play cross-sectional ORB selection edge by ranking US equity-index futures (ES/NQ/YM/RTY) on opening relative volume, trading ORB only on the most in-play index/day. Cheapest necessary-condition pre-screen (Notice-phase, cached data, no K) on the 2 indices held intraday = Nasdaq MNQ_M15 vs Dow MYM_M15 (widest US large-cap spread), 1534 common RTH sessions 2020-07..2026-07. (A) DISPERSION corr(RV)=0.717, 68% days RV within +/-25% (compressed non-zero). (B) PREDICTIVENESS: higher-RV bigger |move| +1.86bp sign-p0.008 but NOT better ORB edge (win 0.487 / +0.22bp / sign-p0.329, null slightly wrong-signed). Killer: RV-selection ORB edge +2.64bp vs random +2.39bp vs always-MNQ +5.19bp (MYM uncond -0.35bp) -> rotation captures HALF the incumbent single-instrument edge. In-play predicts bigger but not more directional move (whipsaw). Strictly dominated by ORB-MNQ. 4-6-way ES/NQ/YM/RTY universe unavailable without a real ES+RTY intraday pull (only daily ES cached; no RTY)." harness_disposition_ref="cross-index RV necessary-condition pre-screen (Notice-phase, no harness DispositionRecord; lab/archive/xindex_rv_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure+data-universe-constraint" role_tested="selection-gate" falsifier_failed="(B) higher-RV NOT better ORB edge (win 0.487, +0.22bp, sign-p0.329); RV-selection +2.64bp < always-MNQ +5.19bp (dominated by incumbent); (A) dispersion compressed corr(RV)=0.717" addback_condition="scoped ES+RTY intraday pull showing small-cap idiosyncrasy raises RV dispersion AND higher-RV then predicts better ORB edge (DEFER-procurement, poor prior) - NOT an RV-window/ORB/2-index re-tune; ES-alone inadmissible (more homogeneous)" config_fingerprint="xindex-rv/MNQ_M15+MYM_M15/open30m-RV-lookback14/ORB-first-break-exit-close/n=1534/2020-07..2026-07/feed=core-data-bar_data" -->
- **cross-index-relative-volume-ranking on ES/NQ/YM index futures** — rejected 2026-07-21 (edge-failure + data-universe-constraint: recover the Stocks-in-Play cross-sectional ORB selection edge by ranking index futures on opening relative volume; cheapest necessary-condition pre-screen on the 2 indices held intraday (Nasdaq MNQ vs Dow MYM, n=1,534) → dispersion compressed (corr 0.717) and higher-RV does NOT predict a better ORB edge (win 0.487, sign-p 0.329); RV-selection captures +2.64 bp vs **+5.19 bp for always-MNQ** → strictly dominated by the incumbent single-instrument ORB-MNQ; the strong Stocks-in-Play edge needs a single-stock cross-section the futures-prop venue can't host); `lab/archive/xindex_rv_recon_2026-07/RESULTS.md`.

### TAS settlement-window replication on MCL (CME CL 14:28–14:30 ET)

**Rejection scope:** the **outright** MCL expression of CME CL settlement-window benchmark-replication
flow — enter with the mandated-flow direction in the 14:28–14:30 ET settlement window, 20-tick stop,
~120 s horizon. Rejected on **magnitude reachability**, at $0/K=0, without the δ-extraction probe ever
being run. Distinct from `BE3`/`SFX-1` (killed by the *fade-program* $200/1.83 design law, ruled
fade-scoped and not a TNEC limb on 2026-08-10) and from `R8` (gold benchmark-fix, whose family scope is
the venue-legal **metals** set — MCL is Energy and outside it).
**Closure date:** 2026-08-11
**Class:** magnitude-unreachable (screened-dead pre-probe; mechanism plausible, required effect out of range)
**Authoritative artifact:** [`Q-MCLTAS-1 closure`](briefs/closures/Q-MCLTAS-1-closure-falsified.md) +
[`Stage 0 RESULTS`](../lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)
**Closure basis:** two independent walls, pre-registered. **Wall B (dispositive)** — the Req-5 hurdle is
11.60 ticks/event ($11.60/contract) = **14.87 bp** at the 2023 panel basis vs an estate causal-public δ
ceiling of **3.21 bp** (4.63×), falling only to 3.01× at an implausible $120 oil and surviving the
forbidden bare-commission ablation (3.04×). Converted to cohort-bound **δ/σ** against MCL's own *measured*
σ surface, the required δ/σ is **0.62–1.35** vs D5's committed **0.113 conservative / 0.194 optimistic** —
a floor of **3.2×** under maximal stacked generosity and **7.0×** at the defensible reading. **Wall A** —
the intersection of {free ∧ signed ∧ price-exogenous ∧ window-aligned} sign sources is **EMPTY**: published
TAS volume is gross by construction, ΔOI is directionally agnostic, COT is weekly and lagged, and CME
publishes **no** settlement-window imbalance print (the structural asymmetry vs the equity closing auction
that `F1`/MOC traded). One entitled-but-**costed** route (TAS-book order flow in `GLBX.MDP3`) survives
unverified; it cannot reach Wall B. Adverse mechanism prior: TAS exists *so that* mandated flow can lock
settlement without revealing direction to the outright book, so the public residue is small by
construction — R8's measured structure, and the informed-flow signature's **third** confirmed instance
on the family where it was **first** confirmed (`H-FBEIA-1`, −1.16 bp, wrong-signed).
**Re-proposal bar:** a **published, post-hoc-free cohort δ for CL/MCL settlement-window flow ≥ the 4×
hurdle at a named venue-legal outright expression** (mirrors R8's bar). NOT a re-read of this arithmetic,
a window/stop re-tune, the DISCLOSURE bare-commission basis, a spread re-frame (a **new campaign** per
ENV-1 §6.4.1, and `SFX-1` is already dead), or resolution of Wall A's costed route — which cannot reach
Wall B. **MCL the instrument is NOT rejected** — what dies is this design region, per the ledger's
2026-08-10c precedent.

<!-- concept-intake-entry mechanism_family="tas-settlement-window-replication" instrument="MCL" rejection_reason="magnitude-unreachable (screened dead pre-probe, $0/K=0): outright MCL expression of CME CL settlement-window (14:28-14:30 ET) benchmark-replication flow, 20-tick stop, 120s horizon. Wall B dispositive: Req-5 hurdle 11.60 ticks/event = 14.87bp at 2023 panel basis vs estate causal-public delta ceiling 3.21bp (4.63x); 3.01x at implausible $120 oil; 3.04x under the forbidden bare-commission ablation. In cohort-bound delta/sigma against MCL's own MEASURED sigma surface (stage2_sigma.windowed_sigma, wed_thu ex-FOMC, 15-min column sqrt-time scaled to the 2-min window): required delta/sigma 0.62-1.35 vs D5 committed 0.113 conservative / 0.194 optimistic = floor 3.2x under maximal stacked generosity, 7.0x defensible. Wall A: intersection of {free, signed, price-exogenous, window-aligned} sign sources EMPTY - published TAS volume is gross by construction, delta-OI directionally agnostic, COT weekly+lagged, and CME publishes NO settlement-window imbalance print (structural asymmetry vs the equity closing auction F1/MOC traded); one entitled-but-costed route (TAS-book order flow in GLBX.MDP3) survives unverified and cannot reach Wall B. Adverse mechanism prior: TAS exists so mandated flow can lock settlement WITHOUT revealing direction to the outright book, so public residue is small by construction - informed-flow signature third confirmed instance, on the family where it was first confirmed (H-FBEIA-1, -1.16bp, wrong-signed). Probe never run; the two free pre-stages establish it is unfundable before design. NOT the BE3/SFX-1 kill (fade-program design law, ruled fade-scoped 2026-08-10) and NOT inside R8's metals-only family scope." harness_disposition_ref="Q-MCLTAS-1 Stage 0a+0b (no harness DispositionRecord; lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)" date="2026-08-11" class="magnitude-unreachable" role_tested="entry" falsifier_failed="Wall B: required delta 14.87bp vs 3.21bp estate causal-public ceiling (4.63x, min 3.01x); cohort-bound required delta/sigma 0.62-1.35 vs D5 0.113/0.194 (floor 3.2x, defensible 7.0x)" addback_condition="published post-hoc-free cohort delta for CL/MCL settlement-window flow >= the 4x hurdle at a named venue-legal OUTRIGHT expression (mirrors R8's bar) - NOT a re-read of this arithmetic, window/stop re-tune, DISCLOSURE bare-commission basis, spread re-frame (new campaign per ENV-1 6.4.1; SFX-1 already dead), or resolution of Wall A's costed route" config_fingerprint="tas-settlement/MCL/window=1428-1430ET/stop=20t/horizon=120s/RT=2.90-F3-primary/hurdle=4x/sigma=stage2-windowed-wed-thu-exFOMC" -->
- **tas-settlement-window-replication on MCL** — rejected 2026-08-11 (magnitude-unreachable, $0/K=0, probe never run: Req-5 hurdle 11.60 ticks = 14.87 bp vs a 3.21 bp estate causal-public ceiling → 4.63×, floor 3.01×; cohort-bound required δ/σ 0.62–1.35 vs D5's 0.113/0.194 → floor **3.2×**, defensible 7.0×; and the {free ∧ signed ∧ exogenous} sign-source intersection is empty — TAS volume is gross by construction and CME publishes no settlement-window imbalance print); [`Q-MCLTAS-1 closure`](briefs/closures/Q-MCLTAS-1-closure-falsified.md).

### Third-Friday derivative-settlement reversal on MYM

**Rejection scope:** the exact Baltussen/Terstegge/Whelan derivative-payoff-bias expression on native MYM: short the calendar third-Friday 09:30 ET open and cover at 12:00 ET. The overnight Thursday-close→Friday-open spike is a mechanism-faithfulness measurement, not a traded limb.
**Closure date:** 2026-07-21
**Class:** edge-failure (underpowered, unstable) + venue/cost-geometry
**Authoritative artifact:** [`lab/archive/mym_3fps_recon_2026-07/RESULTS.md`](../lab/archive/mym_3fps_recon_2026-07/RESULTS.md) + [`closure`](briefs/closures/MYM-3FPS-1-closure-falsified.md).
**Closure basis:** frozen K=0 native-micro extraction, 2019-05-06→2026-07-21, exact timestamps and no nearest-bar substitutions. Coverage passed (84/87, 96.6%), but the overnight spike was only +1.54 bp (`delta/sigma=0.0256`, power 0.042) and the open-to-noon short only +2.68 bp (`delta/sigma=0.0500`, power 0.067), both far below the frozen 0.2139 standardized-effect floor. The short also failed the Tradeify cost law: +2.68 bp vs 6.57 bp 4× hurdle. Year signs were unstable and the tradable limb was negative in 2019, 2024, 2025, and 2026. The published ~12 bp DJIA effect does not transfer at useful magnitude to the native MYM era.
**Re-proposal bar:** new target-instrument mechanism evidence. NOT a 09:15/09:20 entry, different exit, quarterly/triple-witch subset, MNQ rescue, overnight limb, or pooled-index version; each is a new hypothesis and the first three are precisely the post-result selection moves this probe froze out.

<!-- concept-intake-entry mechanism_family="third-friday-derivative-settlement-reversal" instrument="MYM" rejection_reason="edge-failure + venue/cost-geometry: frozen K=0 native-MYM third-Friday 09:30->12:00 short, n=84/87 exact events (96.6%). Overnight spike +1.54bp, delta/sigma 0.0256, power 0.042; open-to-noon short +2.68bp, delta/sigma 0.0500, power 0.067; both below 0.2139 floor. Cost-law FAIL: +2.68bp vs 6.57bp 4x Tradeify hurdle. Year signs unstable; short negative 2019/2024/2025/2026. Published ~12bp DJIA effect absent at useful magnitude in native MYM era." harness_disposition_ref="MYM-3FPS-1 Phase-0 (K=0 delta extraction; lab/archive/mym_3fps_recon_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure+venue-cost-geometry" role_tested="entry" falsifier_failed="P0.1 overnight delta/sigma 0.0256; P0.2 reversal delta/sigma 0.0500 vs 0.2139 floor; P0.3 +2.68bp vs 6.57bp hurdle" addback_condition="new target-instrument mechanism evidence - NOT timing/exit/expiry-subtype retune, MNQ rescue, overnight limb, or pooled-index variant" config_fingerprint="3fps/MYM.v.0/calendar-third-Friday/short-open09:30ET->12:00ET/cost=Tradeify0.91+1tick-side/feed=Databento-GLBX-MYM.v.0-ohlcv1m-2019-05-06..2026-07-21" -->
- **third-Friday-derivative-settlement-reversal on MYM** — rejected 2026-07-21 (edge-failure + cost: native K=0 exact-window probe, n=84; overnight +1.54 bp / power 0.042; short reversal +2.68 bp / power 0.067; cost hurdle 6.57 bp; unstable and recently wrong-signed); `lab/archive/mym_3fps_recon_2026-07/RESULTS.md`.

### Opening-volume × directional-efficiency pressure map on MNQ/MYM

**Rejection scope:** the continuous BAR EXPORT opening-pressure mechanism — high opening volume as continuation when the first 30 minutes are directionally efficient and as reversal when absorbed into a low-efficiency range — on native MNQ and MYM M15 panels. Not a strategy or entry rule.
**Closure date:** 2026-07-21
**Class:** edge-failure (underpowered / wrong-signed on development)
**Authoritative artifact:** [`lab/archive/opening_pressure_map_2026-07/RESULTS.md`](../lab/archive/opening_pressure_map_2026-07/RESULTS.md) + [`closure`](briefs/closures/OPENPRESS-1-closure-falsified.md).
**Closure basis:** frozen K=0 hash-pinned diagnostic (`MNQ_M15.csv` `ddb14f…e1f7e3ac`, `MYM_M15.csv` `298ab8…f9059c`). Neither instrument passed. MNQ development t=1.53 and pooled t=1.60 (both <2) despite positive slopes and a cost-clearing P90−P10 spread; MYM development slope wrong-signed (−3.63 bp) and predicted spread 1.71 bp below the 6.41 bp 4× Tradeify hurdle. Exactly-zero instruments passed → overall `FALSIFIED` (not AMBIGUOUS).
**Re-proposal bar:** new modality / mechanism evidence (e.g. true order-flow or absorption measures). NOT an RV threshold, alternate opening window, weekday slice, single-instrument selection after seeing the pair, or re-pin to a newer BAR EXPORT panel to rescue the slope.

<!-- concept-intake-entry mechanism_family="opening-volume-directional-efficiency" instrument="MNQ+MYM" rejection_reason="edge-failure: frozen K=0 BAR EXPORT pressure-alignment diagnostic. MNQ FAIL (dev t=1.53, pooled t=1.60 <2); MYM FAIL (dev slope -3.63bp wrong-signed; pred spread 1.71bp < 6.41bp 4x cost). Neither PASS → FALSIFIED." harness_disposition_ref="OPENPRESS-1 (lab/archive/opening_pressure_map_2026-07/RESULTS.md)" date="2026-07-21" class="edge-failure" role_tested="mechanism-diagnostic" falsifier_failed="MNQ HAC t<2; MYM wrong-signed + cost FAIL" addback_condition="new modality/mechanism - NOT threshold/window/instrument rescue on same OHLCV" -->
- **opening-volume × directional-efficiency on MNQ/MYM** — rejected 2026-07-21 (edge-failure: frozen continuous pressure score; MNQ underpowered HAC t; MYM wrong-signed + cost FAIL; neither PASS); `lab/archive/opening_pressure_map_2026-07/RESULTS.md`.

### Leveraged/inverse-ETF end-of-day rebalance flow on ES/NQ — free-data 5th-leg candidate

**Rejection scope:** trade the mechanical EOD rebalance of constant-leverage ETFs (rebalance flow ≈ `AUM·L(L−1)·r`, momentum-amplifying, concentrated on large-|r| days) via intraday ES/NQ futures, flat by the close (Tradeify-compatible). Rejected as a free-data 5th-leg directional mechanism (advisor Avenue D2). Distinct from the exogenous-ORB-gate thread (this is a standalone directional mechanism, not a day-selection gate) and from the Avenue-A microstructure modality (the signal is public-AUM-derived, not paid order-flow).
**Closure date:** 2026-07-24
**Class:** free-data-domain-bar (reject-at-bar; mechanism real, domain exhausted)
**Authoritative artifact:** [`docs/briefs/2026-07-24-d2-letf-eod-flow-ruling.md`](briefs/2026-07-24-d2-letf-eod-flow-ruling.md)
**Closure basis:** the rebalance direction + size are fully reconstructable from issuer-published daily AUM + public index return + known leverage → the signal is **free-data**, landing inside the tail-exhausted free-data 5th-leg domain (§ SNAG closure below). It clears **none** of the three re-proposal routes: not paid/exogenous data (public-derivable), not a new venue class (same futures-prop ES/NQ), no dated live incident. Mechanism is real + long-documented (Cheng–Madhavan 2009) but widely front-run/decaying and, per the a4-flow prior, thin/redundant as tradable alpha. Advisor AUM figures (~$117B Sept-2024 / ~$198–201B mid-2026, 754 funds) are unverified and non-load-bearing to the free-data classification.
**Re-proposal bar:** paid NDX-native rebalance/order-flow showing an edge that is *both* orthogonal to the incumbent book and non-decayed; OR a new venue class; OR a dated live incident the existing book failed that this leg would have covered. NOT a free-data re-run, a magnitude re-estimate, a different index/leverage tier, or a longer panel.

<!-- concept-intake-entry mechanism_family="leveraged-etf-eod-rebalance-flow" instrument="ES/NQ" rejection_reason="free-data-domain-bar (reject-at-bar): advisor Avenue D2 - trade constant-leverage ETF EOD rebalance (flow ~ AUM*L(L-1)*r, momentum-amplifying, large-|r| days) via intraday ES/NQ flat-by-close. Rebalance signal reconstructable from public daily AUM + public index return + known leverage => FREE-DATA, inside the tail-exhausted free-data 5th-leg domain. Clears none of the 3 routes: not paid/exogenous (public-derivable), not new venue (same futures-prop ES/NQ), no dated incident. Mechanism real (Cheng-Madhavan 2009) but front-run/decaying + a4-flow thin/redundant prior. AUM figures unverified, non-load-bearing." harness_disposition_ref="D2-bar-ruling (manual free-data-bar falsifier; docs/briefs/2026-07-24-d2-letf-eod-flow-ruling.md)" date="2026-07-24" class="free-data-domain-bar" role_tested="entry" falsifier_failed="free-data classification: rebalance signal derivable from public AUM+return+leverage => hits tail-exhausted free-data 5th-leg domain; clears no re-proposal route (paid-data/new-venue/dated-incident)" addback_condition="paid NDX-native rebalance/order-flow with orthogonal + non-decayed edge, OR new venue class, OR dated live incident the book failed - not a free-data re-run, magnitude re-estimate, different leverage tier, or longer panel" config_fingerprint="letf-eod-flow/ES-NQ/rebalance~AUM*L(L-1)*r/signal=public-AUM-derived/venue=futures-prop" -->
- **leveraged-etf-eod-rebalance-flow on ES/NQ** — rejected 2026-07-24 (free-data-domain-bar: EOD rebalance signal is public-AUM-derivable ⇒ free-data, inside the exhausted 5th-leg domain; clears no paid-data/new-venue/dated-incident route; mechanism real but front-run/decaying); [`docs/briefs/2026-07-24-d2-letf-eod-flow-ruling.md`](briefs/2026-07-24-d2-letf-eod-flow-ruling.md).

### Closing-auction / MOC-imbalance flow on MYM — paid-data 5th-leg candidate

**Rejection scope:** trade the published closing-auction order imbalance (~15:50 ET publication →
16:00 ET close) as a directional entry on MYM, flat well before the 16:45 ET deadline. Rejected as a
**paid-data** 5th-leg directional mechanism at the **procurement gate**. Distinct from the LETF
EOD-flow rejection (that signal was public-AUM-derivable ⇒ free-data; this one is exchange-licensed,
so the free-data classification does **not** reach it) and from Avenue-A depth-shape discovery (this
is a published signed imbalance, not book geometry, so the a4 category-non-identifiability prior does
not reach it either).
**Closure date:** 2026-07-27
**Class:** paid-data-procurement-gate (reject-at-bar; mechanism real, evidence absent, procurement gated)
**Authoritative artifact:** [`docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)
**Closure basis:** clears no route. Free-data route 1 requires *demonstrating* a vol-orthogonal,
within-era-robust edge — F1 has no citable δ, no cohort, no measurement, so the route is unclaimed
rather than cleared; routes 2/3 (new venue class / dated incident) plainly fail. The OHLCV raised
bar's order-flow modality is expressly parenthesised to the standing **"don't buy explanatory data
before a survivor justifies it"** rule, operationalised by the 2026-07-24 Avenue-A scoping (§6
qualifying triple; standing disposition *scoped-not-procured*) — F1 is blind discovery on paid data
with no survivor tie, the exact prohibited shape. Independently, harvest **Requirement 2** renders it
**UNSCREENABLE** (no MOC→MYM δ; transplant and invention both forbidden), and the δ-extraction probe
route is circular because it needs the gated data. Secondary unvalidated link: MOC imbalance is a
cash-equity phenomenon; transmission to a micro Dow future is unestablished. Cost context (non-load-bearing,
pure arithmetic): MYM RT $2.82 ⇒ 4× hurdle $11.28 ⇒ ≈22.6 Dow points/trade in a ten-minute window.
**Re-proposal bar:** a **published cohort δ for imbalance → index-futures response** citable without
procurement (free, zero-K — the only route attemptable today); OR a **survivor tie** meeting Avenue-A
§6's qualifying triple; OR the data becoming free (which would *drop it into the D2 free-data kill*,
not rescue it); OR a dated live incident the book failed. NOT a micro-capacity re-framing, a different
index/instrument, a longer window, or a well-formed four-clause card.

<!-- concept-intake-entry mechanism_family="closing-auction-moc-imbalance-flow" instrument="MYM" rejection_reason="paid-data-procurement-gate (reject-at-bar): census entry F1 - trade published MOC order imbalance (15:50 ET publication -> 16:00 ET close) directionally on MYM, flat by 16:45. Clears NO route: free-data route 1 requires demonstrating a vol-orthogonal + within-era-robust edge and F1 has zero delta/cohort/measurement (unclaimed, not cleared); no new venue class; no dated incident. Binding constraint = the standing 'don't buy explanatory data before a survivor justifies it' rule, operationalised by the 2026-07-24 Avenue-A scoping (qualifying triple unmet, scoped-not-procured) - F1 is blind discovery on paid data with no survivor tie. Independently UNSCREENABLE under harvest Req 2 (no MOC->MYM delta; transplant/invention forbidden; delta-extraction probe circular since it needs the gated data). Unvalidated cash-equity -> micro-Dow-future transmission. NOT killed by the D2 free-data classification (imbalance is exchange-licensed, not public-derivable) nor by the a4 category prior (published signed imbalance != category splitting) - those distinctions are stated so a future session does not borrow the wrong kill." harness_disposition_ref="F1-bar-ruling (manual paid-data-procurement-gate falsifier; docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md)" date="2026-07-27" class="paid-data-procurement-gate" role_tested="entry" falsifier_failed="no route cleared: free-data route 1 unclaimed (zero demonstration), OHLCV route-2 order-flow modality gated by no-buy-before-survivor + Avenue-A qualifying triple, harvest Req 2 UNSCREENABLE with circular probe route" addback_condition="published cohort delta for imbalance->index-futures response citable WITHOUT procurement (free, zero-K, only route attemptable today), OR a survivor tie meeting Avenue-A section-6 qualifying triple, OR the data becoming free (which drops it into the D2 free-data kill), OR a dated live incident - NOT micro-capacity re-framing, different index, longer window, or a well-formed four-clause card" config_fingerprint="moc-imbalance/MYM/signal=exchange-published-signed-imbalance/window=1550-1600ET/venue=futures-prop-flat-1645" -->
- **closing-auction-moc-imbalance-flow on MYM** — rejected 2026-07-27 (paid-data-procurement-gate: no route cleared; free-data route 1 unclaimed for want of any δ; order-flow modality gated by "don't buy explanatory data before a survivor" + Avenue-A qualifying triple; UNSCREENABLE under Req 2 with a circular probe route); [`docs/briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md`](briefs/2026-07-27-f1-moc-imbalance-mym-ruling.md).

### ORB-MNQ-1 as a payable standalone `Tradeify_Select_100K` leg — DEPLOYMENT-TARGET rejection (NOT a mechanism rejection)

**⚠ Read the scope before borrowing this entry.** This rejects **one deployment target at one
firm**, not the ORB mechanism family and not ORB on MNQ. It is filed here so the re-proposal bar is
discoverable, and it deliberately carries **no `concept-intake-entry` comment and no queryable-index
line** — registering it in the dedup machinery would make `mechanism_family="opening-range-breakout"
instrument="MNQ"` return REJECTED to every future caller, which is not what was decided.

**Rejection scope:** the *target* — running the frozen ORB-MNQ-1 construct at k ∈ {1,2,3} as a
payable standalone leg on a `Tradeify_Select_100K` account. **Not rejected:** the construct's edge
(full-window net meanR **+0.0626**, n=1,846), its Stage-2 cost-law PASS, or its Stage-7 result that
2021+ clears all four FRIENDLY firms to 3 ticks. Lifecycle standing is **unchanged** at
`CANDIDATE @ 1.00×` — parking is operational, not a lifecycle demotion, and no `core/lifecycle.py`
write occurred.
**Closure date:** 2026-08-03
**Class:** venue-survivability failure (trailing-drawdown geometry) — NOT an edge failure, NOT a
cost-constraint, NOT a selection/multiplicity failure.
**Authoritative artifact:** [`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md`](adr/2026-08-03-orb-mnq-repark-payability-falsified.md)
(supersedes the 07-31 unpark ADR's §2/§4 in part; measurement
[`RESULTS_t2_intraday_bust.md`](../lab/analysis/orb/orb_mnq_2026-07/RESULTS_t2_intraday_bust.md),
harness `run_t2_intraday_bust.py`, 7 controls passed).
**Closure basis:** §4 T2 ruled **FIRED** on the Part A bust reading. Against the frozen
survivor-scoring gate (**bust ≤ 3.0% ∧ P(pass) ≥ 50%**, pre-reg `be6dda6`, unedited), intraday-honest
bust is **67.67% / 77.01% / 80.18%** and P(pass) is **32.33% / 22.99% / 19.82%** at k=1/2/3 — **both
limbs fail at every admissible k**, and one contract is the smallest integer expression, so T2's own
prescribed remedy (cap k=1) is **inert**. Independent of the bootstrap, a `Tradeify_Select_100K` eval
walked over the *realized* panel busts in **March 2020** at every k (both clocks, same day); realized
max DD **−$6,527** at k=1 = 2.18× the $3,000 trail against +$17,780 net. The intraday correction is
**not** what fires it — the EOD arm already read 74.00% at k=2; intraday honesty adds +3.01pp.
**Surviving finding (NOT rejected) — load-bearing, falsifier-construction class:** **a falsifier can
have every limb survive literally while the thing it was written to test dies.** H's limb (b)
(*"positive single-day headroom"*) is **SATISFIED** at $1,432 and was ruled to keep its literal
wording; limb (a) carries no numeric threshold at all. The target dies on Part A bust and P(pass) —
criteria H never bound. Sibling to the 2026-07-31 fade-program *"the screen interrogates the GEOMETRY
and never the EDGE"* finding and to `lesson_gate_reachability_preregistration` (bundled clauses in
mismatched units). Carried **candidate-status** pending a third firing.
**Re-proposal bar:** for **Tradeify at this tier** — a documented change to the venue's drawdown
geometry (static DD, a larger trail, or a mechanism other than the $3,000 intraday-enforced one)
under which k=1 clears **both** frozen limbs on the unedited survivor-scoring protocol, plus a fresh
operator GO. For **any other firm** — a non-Tradeify re-scope was **offered and declined** at closure
(target-shopping after seeing the data), so it needs the 2026-07-24 addendum's standing bar (fresh
operator GO + pre-registration) **and** a survivor-scoring pass at that firm's geometry **before**
unparking, not after. NOT a k re-pick, NOT the 15:30 exit (barred, reaffirmed 2026-08-02), NOT a
conditioning gate (four falsified, pre-reg §5 forbids), NOT a re-scoped payability threshold.

## Domain-level SNAG closures

Distinct from the per-direction entries above: a **research-domain** closed on
SNAG-budget exhaustion (multiple consecutive null/falsified loops in one search
domain), with a shared re-proposal bar that governs *every* future candidate in that
domain. Precedent: the Guardian-on-XAGUSD entry closed on parent-programme
SNAG-exhaustion. Re-proposal of anything in a closed domain requires clearing the
domain bar, not merely the per-candidate bar.

### 5th-leg / portfolio-expansion (free-data search) — SNAG-CLOSED 2026-07-01

**Scope:** the search for a 5th portfolio leg / concurrent expansion strategy
sourced from **free data** (internal within-strategy alpha, free-exogenous regime
gates, published/retail strategies, chop-native decorrelated legs). Does **not**
close: expansion via **paid data** or a **genuinely new venue class** (those clear
the bar below).

**Closure basis (2026-07-01 programme audit, object-layer):** in the 2026-05-27→07-01
window the domain ran **≈17–22 consecutive terminal closures with 0 admissions** —
every candidate died on one of the same three walls (H1-regime co-occurrence; single-
account non-codifiability; signal reduces-to-returns / falsified-by-source / era-
collinear). Sibling domains corroborate and are also exhausted: **regime-detection**
(9 consecutive nulls, operator SNAG-closed 2026-06-28, `4603be4`); **within-strategy
-alpha** (6–7 nulls, closed by designed synthesis — `project_missed_alpha_sweep_synthesis`,
"NO regime-robust within-strategy alpha"); **external-sourcing** (69 candidates → 0
saved, `96470f3`). The per-direction entries above (XAGUSD, USOIL×3, EURGBP, EURUSD×2,
GEX, T10Y3M, Friday, rates-MR, dispersion) are the object-level instances; this entry
is the domain-level roll-up that sets the shared bar. Full evidence:
[`docs/notes/audits/programme-audit/2026-07-01-portfolio-audit.md`](notes/audits/programme-audit/2026-07-01-portfolio-audit.md)
§4 (obj-#2/#4) + the loop census; consolidated recommendation in the
[cross-layer synthesis](notes/audits/programme-audit/2026-07-01-cross-layer-synthesis.md) R2.

**Re-proposal bar (domain-level).** A new free-data 5th-leg/expansion candidate is
**not admitted for a full Pre-Q** unless it clears one of:
1. **Paid / exogenous data** the free searches could not access (e.g. NDX-native
   dealer gamma, intraday 0DTE order-flow), demonstrating an edge that is *both*
   vol-orthogonal *and* within-era robust; OR
2. A **genuinely new venue class** that relaxes a *binding* wall (not just cost) —
   e.g. an options-capable venue for the vol/correlation branch, or a venue that
   admits a mechanism the CFD/futures-prop venues structurally cannot host; OR
3. A **dated live incident** the existing book demonstrably failed to handle that a
   specific new leg would have covered (the `rejected_signals.md`-style bar).

"Another free-data mechanism", "a wider sweep", "a different instrument", or "a
longer panel" do **not** clear the domain bar — that is the exhausted move. This bar
supersedes nothing per-candidate; it adds a domain gate ahead of the per-candidate
gate.

**Operator-ratified 2026-08-09** — discharging the 2026-07-01 portfolio-audit §5.3 mandate
("Owner: operator ratifies; CC authors"), whose authoring half landed same-day as `13c01d0` and
whose ratifying half had been outstanding since. Ratified by in-session operator instruction under
[`ADR 2026-08-09 rejection-register topology`](adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) D1.

⚠ **Correction 2026-08-09 — this entry previously claimed "Reviewed at the 2026-08-08 slate."**
That sentence was written on **2026-07-01**, in this entry's own authoring commit (`13c01d0`), as a
*forward instruction* — and the review **did not happen**: the 2026-08-08 quarterly audit note
contains no review of this entry (grep for `5th-leg|SNAG` returns only its diagnostic-4 RED cell).
A forward instruction that reads as a completed record is exactly the phantom-discharge failure the
estate has a recorded lesson for. **This bar was also unwired and had zero recorded consults across
the entire 2026-08-03→09 kill run** — per ADR D2, it was inert prose until today's ratification, and
must not be read retrospectively as having gated any in-window work. Its force runs **forward from
2026-08-09**. The deferred maximal-harvest question remains open and is not adjudicated here.

---

## Domain-level tail-exhaustion raised bars

Distinct from the SNAG closures above: a domain the object-layer programme audit found
**STABLE (saturating)** rather than exhausted — it has produced *and retains* a survivor and
sits well below the ~17–22-closure SNAG bar, but where further *same-space* mining has low
expected yield. A raised re-proposal bar governs **new** candidates only; the survivor and any
untested threads are explicitly preserved. Escalates to a genuine SNAG closure only if the
census later reaches the SNAG bar **and** the survivor is retired to 0.

### Single-instrument index-futures intraday OHLCV directional timing — RAISED BAR (tail-exhaustion; NOT a SNAG closure) 2026-07-21

**Disposition:** a **tail-exhaustion raised re-proposal bar**, explicitly **NOT** a domain-SNAG closure. The domain was audited 2026-07-21 (object-layer programme audit) and returned **STABLE (saturating)** — see [`docs/notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md`](notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md). **Operator-ratified 2026-07-21** (STABLE verdict accepted; this bar landed). It does not carry the SNAG section's "closed" force — it adds a domain gate ahead of the per-candidate gate for *new* candidates.
**Scope:** a *directional intraday timing* edge on a **single liquid US equity-index future**, from **OHLCV structure alone**, deployable **flat-by-close**. Does **not** cover: the exogenous-ORB-gate conditioning sub-thread (its own tail-exhaustion note above, GEX/T10Y3M/Friday/VIX-TS), overnight mechanisms (H-OD-1 — venue-walled), non-index complexes, or the incumbent survivor.
**Basis (why a raised bar, not a closure):** 4 own in-domain closures — **D5** (Stage-2 cost-law, 2026-07-16) / **D5-RECOST** (OOS edge decayed negative, 2026-07-21) / **H-TSMOM-1** (Clause-N power, 2026-07-16) / **cross-index-RV-ranking** (dominated by incumbent, 2026-07-21) — **plus 1 admitted survivor `ORB-MNQ-1` (lifecycle CANDIDATE @1.00×, 2026-07-16)** + external corroboration (two 2026-07-21 literature deep-searches; independent MNQ 0/14-family falsification, arXiv 2605.04004). The count is ~⅓ of this file's ~17–22 domain-SNAG bar and the domain is **1-admission, not 0**, so the audit declined SNAG per the same-week **ZF calibration** (3 constructs = INQHIORI §6 tail-exhaustion, not SNAG). The three cost/edge-ratio levers are now mapped — **price** (D5-RECOST: moot, edge decayed), **instrument-selection** (cross-index: dilutes below the single best incumbent), **hold-time** (ORB-MNQ already exploits it via exit-at-close) — so a re-tune of any lever is the exhausted move.
**Re-proposal bar (domain-level).** A *new* single-instrument index-futures intraday OHLCV directional-timing candidate is **not admitted for a full Pre-Q** unless it clears one of:
1. a **mechanism outside the mapped cost-ratio-lever set** (price / instrument-selection / hold-time) — a re-tune of any mapped lever, a different RV/ORB window, or a different index is the exhausted move; OR

   > ⚖ **SCOPE RULED 2026-08-10 (JA) — [`ADR`](adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md) §2-A.**
   > **"instrument-selection" here means CROSS-instrument selection.** Its provenance is the cross-index RV-ranking
   > closure below, which measured *dilution across a universe* (+2.64 bp RV-ranked vs **+5.19 bp always-MNQ**) —
   > choosing among **instruments**, never among **moments within one instrument**. **Within-instrument temporal
   > selectivity is therefore OUTSIDE the mapped set and route 1 is OPEN to it**, under the ADR's §2-B conditions:
   > criterion causally named a priori and frozen at G0 (never read off a scored list) · every axis charges
   > `K_intrinsic` · the F2 guard and every downstream gate unchanged. **Price and hold-time stay mapped and
   > exhausted** (hold-time additionally re-falsified 2026-08-10 by a $0 stop-width sweep: 0.02–0.10× the 4× cost
   > bar across the whole ratified 5–20 pt band); **cross-index selection stays closed at its own entry below.**
   > ⚠ Enforcement note: this bar is machine-consulted (`scripts/instrument_profiles.py cell`, **tier=always**,
   > exit 1 when it binds) — but two dense-1m campaigns (CON-1, CON-2) nonetheless ran **unbound** because their
   > lane's door check never reached domain-level bars. Repaired at that lane's step 1a; `lesson_gate_reachability_preregistration`
   > stands at **5 firings**.

2. a **different modality** (order-flow / microstructure — untouched per the "don't buy explanatory data before a survivor" rule) or a **venue** that relaxes a binding wall; OR
3. evidence it **beats the incumbent ORB-MNQ net-of-cost**, not merely clears the cost floor.
**Explicitly preserved (NOT rejected):** `ORB-MNQ-1` (the survivor) and the **session-confluence longer-hold** thread (untested, low-priority — ORB-MNQ already occupies that class). Reviewed at the 2026-08-08 slate; escalates to a genuine domain-SNAG only if own in-domain closures reach ~17–22 **and** ORB-MNQ is retired to 0 (audit §10 hook 3).
**⚠ Status update 2026-08-02 — the session-confluence longer-hold preservation is DISCHARGED, not still untested.** `Q-SESSCONF-1` measured it and closed **FALSIFIED** ($0/K=0): the hold-window ceiling is **+0.091 annSR** against a **+0.124** K-price, and the externally-carved-out **60–75 min class measures +0.501/+0.490 against the incumbent's +0.842** — adverse, not merely unproven. [`lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md`](../lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md). The survivor preservation is unchanged.

---

### End-of-day adversity on index-futures intraday constructs (mechanism explanations) — RAISED BAR (tail-exhaustion) 2026-08-02

**Disposition:** a **tail-exhaustion raised re-proposal bar** on *mechanism explanations for
late-session adversity*, **operator-ratified 2026-08-02**. Not a SNAG closure (the count is far below
the ~17–22 bar) and not a rejection of the incumbent. Four mechanism attempts closed in two days, all
at **$0 spend / K=0 / no manifest**, and the fourth was killed by its own reachability pre-flight
before a brief was authored.

**Scope:** the claim that the **final RTH block (15:30–16:00 ET) is anomalous** for an intraday
trend-aligned, fixed-stop index-futures construct, and any mechanism proposed to explain it. Does
**not** cover: the incumbent `ORB-MNQ-1`; the *exit-time* question itself (settled separately by
[`ADR 2026-07-31`](adr/2026-07-31-orb-mnq-unpark-payability-target.md) §5, which bars adopting the
15:30 exit); non-index complexes; or the exit-policy arithmetic finding below.

**Basis — four attempts, and then the premise itself failed:**

| # | Mechanism | Verdict | Discriminator |
|---|---|---|---|
| 1 | Directional reversal into the close | **REFUTED** | `corr(r_10:00→15:30, r_15:30→16:00) = +0.0127`, NW(5) t **+0.321** — weakly *positive*, replicating D5-RECOST's pre-recorded +0.024 prior |
| 2 | Variance expansion against a fixed stop | **NOT SUPPORTED** | final-block range 1.06× (frozen comparator) / 1.12× (exposure-relevant), z **+0.21** |
| 3 | Drift exhaustion against a constant hazard | **FALSIFIED** | OOS on MYM: L1/L2 passed but `t*` degenerate at **03:15 ET** (before the session opens); P3 missed by **16×** tolerance |
| 4 | Equity-close flow (auction imbalance / rebalance) | **NOT AUTHORED** | reachability pre-flight: every date-conditional subgroup underpowered **2–5×** (MDE 0.067–0.162 vs a 0.030 effect; needs **n ≈ 1,194** usable days/subgroup) |

**The decisive finding — the phenomenon does not survive multiplicity.** Measured identically on both
index futures for the first time, with per-day standard errors: MNQ final block **t = −1.78**, and
**max |t| across all 11 session blocks = 1.84**, *below* the expected max of 11 null draws (≈2.2–2.4);
MYM final block **t = −2.18**, sitting *at* that expected max. MNQ's **14:00 block (−1.84) is as
negative as the final block**, so "the final block is special" fails even descriptively.
**Correction carried:** `Q-SESSCONF-1`'s published **z = −2.90** exposure control differenced the
ladder and estimated dispersion from those same 11 differenced points as if independent; the direct
per-day test returns **t = −1.78**, and **z = −2.90 must not be re-quoted**.

**Re-proposal bar (domain-level).** A *new* mechanism explanation for late-session adversity is **not
admitted for a full Pre-Q** unless it clears one of:

1. a **different modality** — order-flow / microstructure that observes flow directly (signed order
   flow, book depth, the auction-imbalance tape) rather than inferring it from OHLCV. **Note the
   collision:** the nearest such route is already gated — *Closing-auction / MOC-imbalance flow on
   MYM* (2026-07-27) sits at a **paid-data procurement gate** in this same file; OR
2. **evidence the phenomenon itself survives multiplicity** — a pre-registered test showing the
   final-block effect exceeds the expected max over the session's blocks, on an instrument or panel
   not used in the 2026-08-01/02 studies; OR
3. a panel materially beyond **n ≈ 1,200 usable days per subgroup**, which is what makes
   date-conditional flow tests reachable at all.

**Explicitly preserved (NOT rejected):** `ORB-MNQ-1` (untouched; `K_eff = 2`, clears its own floor);
the **exit-policy arithmetic** — holding a fixed stop longer exposes it to more −1R events (76.3%
stop-out channel, **−0.488R** per event vs −0.0056R for a survivor) — which is **real, ordinary, and
not an end-of-day effect**; and the **MNQ family's last `K_intrinsic=1` Cap seat, UNSPENT**.

**Authoritative artifacts:** [`lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md`](../lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md) ·
[`lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md`](../lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md) ·
[`lab/analysis/harvest/driftex_2026-08/RESULTS.md`](../lab/analysis/harvest/driftex_2026-08/RESULTS.md) (incl. the
§Addendum 2026-08-01 reachability pre-flight and the z→t correction).

---

### COT/TFF positioning-extreme reversal (hedging-pressure contrarian signal) — DROP (unscreenable; shape + power)

**Rejection scope:** the direction (fade CFTC COT/TFF non-commercial or leveraged-fund positioning once
it reaches a rolling historical extreme, across a 9-instrument menu — 6E/6J/MGC/MCL/ZN/ZB/ZF/MES/M2K) is
rejected as an **entry mechanism**, on **shape + power** grounds — not on mechanism-reality grounds (the
underlying hedging-pressure literature is real and citable). Not `H-COTREV-6A` (AUD/M6A-scoped, a
narrower prior instance of the same family) and not `Q-ORBPOS-1` (a diagnostic question about one dated
MNQ regime break, not a strategy-candidate proposal).
**Closure date:** 2026-08-24
**Class:** shape-failure (primary, decisive) + power-starvation (independently sufficient) — not a
cost-law kill; cost-law was never reached.
**Authoritative artifact:** [`docs/notes/research/2026-08-24-cot-positioning-reversal-harvest-sourcing.md`](notes/research/2026-08-24-cot-positioning-reversal-harvest-sourcing.md)
**Closure basis:** predicted payoff shape is symmetric, ~40–50% win rate (possibly sub-coin-flip), with
no a-priori reason for mean-win > mean-loss — a contrarian entry into a persistent positioning extreme
risks being stopped out just before the eventual reversal. The venue's own 630-cell shape-feasibility
sweep ([`shape_feasibility_map_2026-08/RESULTS.md`](../lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md))
found no cell at win_rate ≤50% is FEASIBLE for any tested shape/cadence/risk — this candidate's predicted
shape sits 15–30 points inside that dead zone, and the failure is structural (mechanism character, not
sample noise), so a real-panel pull would very likely confirm rather than rescue it. Independently
sufficient: realistic event count (accounting for multi-week autocorrelation/persistence of positioning
extremes, not the raw 52 weekly releases/yr) is ~20–160/instrument over the ~20yr TFF era — the same
low-N regime that killed H-TSMOM-1 (N≈86, power 0.34); the one usable literature Sharpe (Dreesmann,
Herberger & Charifzadeh 2023, best-of-6-of-many-markets, fails portfolio-level aggregation) implies
δ/σ ≈0.17–0.29, below this program's own applied 0.35–0.65 power floor at N<150 across nearly the whole
plausible range. Cost-law never reached (moot).
**Surviving finding (NOT rejected):** the hedging-pressure mechanism class itself — real and
multi-decade-citable (Bessembinder 1992 through Kang-Rouwenhorst-Tang 2020, JF) — kept as a
sourced-but-not-viable Tier-A entry, not a fabricated mechanism; the 6E/6J/MGC/MCL/ZN/ZB/ZF/MES/M2K
instruments standing; a genuinely higher-frequency crowding proxy or a hedger-sentiment (not
speculator-extreme) specification, neither evaluated here.
**Re-proposal bar:** a higher-frequency (intraday/daily, not weekly-COT-derived) crowding proxy, using
the hedger-sentiment rather than speculator-extreme specification (per `H-COTREV-6A`'s own unspent
recovery path), with a demonstrably right-skewed rather than symmetric predicted payoff — **NOT** a
parameter retune of the extreme threshold, a different instrument on the same speculator-extreme
specification, or a wider COT-era window (the power problem is autocorrelation-driven, not
sample-length-driven).

<!-- concept-intake-entry mechanism_family="cot-tff-positioning-extreme-reversal" instrument="6E,6J,MGC,MCL,ZN,ZB,ZF,MES,M2K" rejection_reason="DROP (unscreenable-drop): predicted payoff shape symmetric ~40-50% WR (possibly sub-coin-flip), no a-priori mean-win>mean-loss -- sits 15-30pp inside the venue's own shape_feasibility_map dead zone (no win_rate<=50% cell FEASIBLE at any shape/cadence/risk). Independently sufficient power fail: realistic event count ~20-160/instrument over 20yr TFF era (autocorrelation-driven extreme-clustering, not raw 52/yr); best literature Sharpe (Dreesmann et al 2023, 6-of-many markets, portfolio-aggregation FAILS) implies delta/sigma ~0.17-0.29, below this program's own 0.35-0.65 applied floor at N<150 across nearly the whole plausible range. Cost-law never reached (moot). Wang(2003) sign-direction complication: speculator extremes CONTINUE, hedger extremes REVERSE -- undermines the literal 'speculator-extreme reversal' framing." harness_disposition_ref="literature sourcing note (docs/notes/research/2026-08-24-cot-positioning-reversal-harvest-sourcing.md); no register_search, no manifest, no K spent" date="2026-08-24" class="shape-failure+power-starvation" role_tested="entry" falsifier_failed="predicted shape inside venue's win_rate<=50% dead zone (independently sufficient); power delta/sigma 0.17-0.29 vs 0.35-0.65 applied floor at realistic N=20-160 (independently sufficient)" addback_condition="higher-frequency (intraday/daily) crowding proxy using the HEDGER-sentiment (not speculator-extreme) specification, with a demonstrably right-skewed predicted payoff -- NOT a threshold retune, a different instrument on the same speculator-extreme spec, or a wider COT-era window (power problem is autocorrelation-driven, not sample-length-driven)" -->
- **cot-tff-positioning-extreme-reversal on 6E/6J/MGC/MCL/ZN/ZB/ZF/MES/M2K** — rejected 2026-08-24
  (shape-failure + power-starvation: predicted ~40–50% WR symmetric shape sits inside the venue's own
  win_rate≤50% dead zone; realistic event count ~20–160/instrument implies δ/σ ≈0.17–0.29 vs. the
  0.35–0.65 applied power floor; cost-law never reached). Dedup: closest sibling `H-COTREV-6A` (AUD,
  UNSCREENABLE Req-2, 2026-08-16) shares the same Wang-2003 sign defect; `Q-ORBPOS-1` (FALSIFIED
  2026-08-23, MNQ diagnostic, no registry row per its own convention) independently reinforces. Artifact
  [`docs/notes/research/2026-08-24-cot-positioning-reversal-harvest-sourcing.md`](notes/research/2026-08-24-cot-positioning-reversal-harvest-sourcing.md).
### London-fix wake (dealer-inventory-normalization fade) on 6E/6B — FALSIFIED (placebo/orthogonality battery)

**Rejection scope:** the direction (fade the 10:58–11:04 ET benchmark-fix impulse sign in the 11:10–13:00 ET wake window, on full-size 6E and 6B futures) is rejected as an **entry mechanism**, on **edge-failure** grounds (not cost — B2.0 already confirmed 6E/6B clear the 4× cost floor at full size; this is a signal-does-not-exist finding on top of a cost-feasible venue expression). Adjacent to, but a distinct mechanism family from, the *FX intraday fixing-reversal (session mean-reversion) on EURUSD* entry above (F3): that entry scored the fix **print** itself (event-time, cash EURUSD, cost-killed); this lane scored a later dealer-normalization **wake** window (11:10–13:00 ET, full-size futures) that an operator ruling (B2.1, 2026-08-24) admitted as new mechanism evidence clearing F3's "not a different fix" re-proposal bar — the wake-WHO was tested on its own merits here, not dismissed by F3's cost-law wall.
**Closure date:** 2026-08-24
**Class:** edge-failure (the signal carries no orthogonal information over generic reversal for either symbol; 6B additionally sits below the placebo null's own median at both tested clock resolutions, 6E's decisive minute-resolution placebo statistic does not — see Closure basis) — NOT a cost-constraint (B2.0 already confirmed both symbols clear the 4× cost floor at full size).
**Authoritative artifact:** [`docs/notes/research/2026-08-24-phase-b-lane-b2-placebo-battery-results.md`](notes/research/2026-08-24-phase-b-lane-b2-placebo-battery-results.md) (+ harness [`lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/run_b22_placebo_battery.py`](../lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/run_b22_placebo_battery.py) + `RESULTS.md` + raw log).
**Closure basis:** frozen plan kill criterion (`docs/superpowers/plans/2026-08-23-viable-strategy-phase-b-mechanism-supply.md`, Lane B2 task B2.2): "Kill if the fix dummy adds nothing over generic reversal or sits ≤ placebo 60th percentile." On 2 years of Databento GLBX.MDP3 `ohlcv-1m`/`ohlcv-1h` (continuous `.v.0`, 2024-08-24→2026-08-24; n=469 6E / n=447 6B valid fix-observations): orthogonality regression (`target ~ 1 + trailing_vol + prior_hour_return + imp_sign`, adapted from the gamma-family GEX-gate precedent's `partial_out_t`) fails for **both** symbols on its own — 6E correctly-signed but far short of significance (t=−0.90 vs the |t|≥2 bar); 6B wrong-signed (t=+1.63, positive = momentum-continuation, not fade). Placebo null, decided on the clock resolution matching the orthogonality leg (1-minute bars; 1,000 replicates, day-of-week + trailing-vol matched by construction and verified): 6B's real statistic ranks at the 4.9th percentile of the null (below its own median), also kill-eligible on this leg — but **6E's real statistic ranks at the 67.1st percentile, clearing the 60th-percentile bar** (a coarser hourly-bar null, run first and kept as a cross-check, had ranked it at the 20.9th — the two resolutions disagree, itself consistent with 6E's Step-3 sign-fragility across clock resolutions; see the artifact for the full breakdown). Net: 6B is killed by both legs independently; **6E is killed by the orthogonality leg alone**, its placebo leg does not corroborate at the resolution matching that leg — still sufficient under the criterion's own OR, but a narrower finding for 6E than for 6B.
**Re-proposal bar:** evidence the wake effect is **orthogonal** to generic hourly mean reversion (|t|≥2, correctly signed, after controlling for trailing-vol and prior-hour-return) **and** clears the placebo-null 60th percentile, on a panel or window this battery did not already test — NOT a re-tune of the placebo-hour menu, the trailing-vol window, or the entry/exit clock offsets within the same 10:58–13:00 ET span; and NOT a subset/direction cut mined after this whole-sample test failed (the "adds nothing over generic reversal" finding is a whole-sample result, and post-hoc cuts are the named degeneration move this repo's own methodology already flags).

<!-- concept-intake-entry
     mechanism_family="fx-fixing-reversal-dealer-wake" instrument="6E,6B"
     rejection_reason="FALSIFIED (B2.2 placebo/orthogonality battery, plan Lane B2): orthogonality regression (target ~ 1 + trailing_vol + prior_hour_return + imp_sign) NOT significant/correctly-signed for either symbol -- 6E t=-0.90 (correct sign, |t|<2), 6B t=+1.63 (wrong sign) -- kills both symbols on its own. Placebo null decided on the clock resolution matching the orthogonality leg (1-minute bars, 1000 replicates, day-of-week+trailing-vol matched): 6B ranks 4.9th pctile (below the null's own median, also kill-eligible); 6E ranks 67.1th pctile (CLEARS the 60th-pctile bar -- a coarser hourly-bar null, kept as cross-check, had ranked it 20.9th; the two resolutions disagree). Net: 6B killed by both legs, 6E killed by orthogonality alone. 2yr Databento GLBX.MDP3 ohlcv-1m/1h, continuous .v.0, 2024-08-24->2026-08-24, n=469/447."
     harness_disposition_ref="B2.2 frozen kill criterion (lab/analysis/_inbox/b2_london_fix_wake_2026-08-24/RESULTS.md)"
     date="2026-08-24"
     class="edge-failure"
     role_tested="entry"
     falsifier_failed="orthogonality regression |t|<2 or wrong-signed (both symbols, sufficient alone) OR minute-resolution placebo rank <=60th pctile (6B only -- 6E's placebo leg clears at 67.1th pctile)"
     addback_condition="orthogonal to generic hourly reversal (|t|>=2, correct sign) AND clears placebo 60th pctile, on a panel/window not already tested here -- NOT a placebo-menu/vol-window/clock re-tune, NOT a post-hoc subset/direction cut" -->
- **fx-fixing-reversal-dealer-wake on 6E/6B** — rejected 2026-08-24 (edge-failure: B2.2 placebo/orthogonality battery FALSIFIED both symbols — orthogonality regression |t|<2 or wrong-signed kills both on its own (6E t=-0.90, 6B t=+1.63); minute-resolution placebo null additionally kills 6B (rank 4.9th pctile) but 6E's placebo leg clears it (rank 67.1th, vs 20.9th at the coarser hourly cross-check) — 6E is a single-leg kill; n=469/447 over 2yr Databento GLBX.MDP3); artifact `docs/notes/research/2026-08-24-phase-b-lane-b2-placebo-battery-results.md`.

---

## Audit hooks

```bash
# Closure-pointer integrity: every rejected direction names an authoritative artifact
grep -n "Authoritative artifact" docs/rejected_candidates.md
# Expected: one line per directional rejection

# Re-proposal-bar discipline: every direction states "new mechanism evidence"
grep -n "Re-proposal bar" docs/rejected_candidates.md
# Expected: one line per directional rejection; phrasing names mechanism evidence, not "new parameters"

# Pending-entry hygiene: directions in the pending list either gain a full entry above or are dropped
grep -A1 "Other directions" docs/rejected_candidates.md
# Expected: list shrinks monotonically; entries never reappear once promoted
```

## Harness-fed rejections (auto-appended)

> ⚠ **DEAD SECTION — corrected at the point of use, 2026-08-09.** The preamble here previously
> asserted in the present tense that this section is *"auto-appended by the concept-intake feedback
> hook (`validation/concept_intake/feedback.py`)"* and *"read by `dedup_check` at call time."*
> **Both are false and have been since the Gen-1 tree was deleted** (ADR 2026-07-11);
> `ls validation/` → no such directory at HEAD. **No program appends to or parses this section
> today.** A correction was landed 2026-08-08 as a blockquote at `:138-149` — 400 lines *above* the
> place a future appender actually writes, so it never reached the reader who needed it. This is the
> `lesson_corrections_land_where_read` pattern firing inside the very file the 2026-08-08 audit
> flagged. Recorded per [`ADR 2026-08-09`](adr/2026-08-09-rejection-register-topology-and-bar-wiring.md) D5.
>
> **Do not append here.** Per that ADR's D3, per-direction instrument-scoped mechanism rejections
> belong in `ops/instruments/<SYM>.md` (which has a live machine consult at a tier=always gate);
> this file owns domain-level and cross-instrument bars. Entries below are **frozen historical
> record**.

_(Historical preamble, retained verbatim for provenance: "Auto-appended by the concept-intake feedback hook (validation/concept_intake/feedback.py) when the validation harness rejects a candidate. Read by dedup_check at call time. Additions only — never edit or delete prior entries.")_

<!-- concept-intake-entry mechanism_family="commodity-carry-term-structure" instrument="USOIL" rejection_reason="harness verdict F1-FALSIFIED: curve-state conditioning did not separate forward returns vs contango (primary 5d gap -0.024R, Welch p=0.74, MW p=0.26, perm p=0.66; backwardation UNDERperformed contango at 1/5/10d). Disguised long-oil trend trade. See lab/analysis/oil_carry/." harness_disposition_ref="CONCEPT-USOIL-CARRY-001 (F1 mechanism probe, lab/analysis/oil_carry)" date="2026-06-06" -->
- **commodity-carry-term-structure on USOIL** — rejected 2026-06-06 (harness verdict F1-FALSIFIED: curve-state conditioning did not separate forward returns vs contango (primary 5d gap -0.024R, Welch p=0.74, MW p=0.26, perm p=0.66; backwardation UNDERperformed contango at 1/5/10d). Disguised long-oil trend trade. See lab/analysis/oil_carry/.); harness disposition `CONCEPT-USOIL-CARRY-001 (F1 mechanism probe, lab/analysis/oil_carry)`.
<!-- concept-intake-entry mechanism_family="inventory-reversal-immediacy-premium" instrument="SPX500" rejection_reason="harness verdict FALSIFIED (Stage 1+2 channel-isolating falsifier): the conditional inventory-reversal channel does NOT separate from the unconditional European-open drift. Stage 1 (a) t=1.06 and separation (b) t=0.34 both <2 (cost-invariant); bottom-tercile EU mean 0.0198% vs all-days 0.0148% (D=0.0050%, n=529 trig / 1587 days, 2020-2026); bottom-vs-top t=0.34. Stage 2 (2021-2026) conditional net Sharpe 0.325 even at 0 cost (->0.08/-0.16 at 1/2bp; breakeven 1.35bp). Reduces to the already-dead unconditional overnight/EU drift; on the corrected sample the bottom tercile is not even significantly positive. See lab/analysis/noct_spx/CARD.md NB sample 2020-2026 (~6.4yr) vs brief >=8yr (operator-scoped); a Monday-dropping lag bug in the first run was fixed before this verdict." harness_disposition_ref="CONCEPT-NOCT-SPX-001 (Stage 1+2 channel-isolating falsifier, lab/analysis/noct_spx/CARD.md)" date="2026-06-07" -->
- **inventory-reversal-immediacy-premium on SPX500** — rejected 2026-06-07 (harness verdict FALSIFIED (Stage 1+2 channel-isolating falsifier): the conditional inventory-reversal channel does NOT separate from the unconditional European-open drift. Stage 1 (a) t=1.06 and separation (b) t=0.34 both <2 (cost-invariant); bottom-tercile EU mean 0.0198% vs all-days 0.0148% (D=0.0050%, n=529 trig / 1587 days, 2020-2026); bottom-vs-top t=0.34. Stage 2 (2021-2026) conditional net Sharpe 0.325 even at 0 cost (->0.08/-0.16 at 1/2bp; breakeven 1.35bp). Reduces to the already-dead unconditional overnight/EU drift; on the corrected sample the bottom tercile is not even significantly positive. See lab/analysis/noct_spx/CARD.md NB sample 2020-2026 (~6.4yr) vs brief >=8yr (operator-scoped); a Monday-dropping lag bug in the first run was fixed before this verdict.); harness disposition `CONCEPT-NOCT-SPX-001 (Stage 1+2 channel-isolating falsifier, lab/analysis/noct_spx/CARD.md)`.
