# Rejected portfolio candidates

Standing registry of strategy / instrument / parameter combinations investigated and rejected as portfolio additions. One entry per direction. Re-proposal of any entry on this list requires **new mechanism evidence**, not new parameters or a wider sweep.

This file is appended to at the close of any Pre-Q that closes FALSIFIED on strategy grounds, or at the close of a parent programme on SNAG-budget-exhaustion grounds (the Guardian-on-XAGUSD precedent below). New entries link to the closure artifact authoritative for the rejection.

The intake bar is the same as for any candidate: a mechanism-level claim with falsifiable specifics, not "let's try a wider grid."

> **2026-07-15 · AUDIT-2026-07-11 §5.4 confirmation:** challenge-era claim re-scope is **not** new mechanism evidence. Zero rejection-registry entries re-opened this sweep. Every re-proposal bar below stands unmodified (K7). Inventory: [`docs/notes/audits/programme-audit/2026-07-15-gate-denominated-closure-annotation-sweep.md`](notes/audits/programme-audit/2026-07-15-gate-denominated-closure-annotation-sweep.md).

---

## Entries

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
