# STATE — First Passage

**Last curated:** 2026-08-23

This file is the **open-threads + forward-obligation register** — cross-session
items with no other home, plus the forward-trigger board. It is **not** a state
snapshot: it carries no risk %, MC anchor, strategy version, hash, working-tree
status, or canonical-owner table. Those live with their owners — see
[`docs/operational_rules.md`](docs/operational_rules.md) §7.

For uncommitted work: `git status`. For history: `git log`. For session narrative
and the live **Open / next**: [`docs/SESSIONS.md`](docs/SESSIONS.md) (read its top
entry first).

**Anti-accretion (standing):**

- New operator decision → **one line + owning ADR** (never a paragraph here) —
  [`docs/operational_rules.md`](docs/operational_rules.md) Rule 7.
- Item leaves the queue or closes → **delete the STATE row**; do not leave
  “Cleared …” footnotes.
- Forward triggers: date/criterion + owner link only; detail stays with the owner.
- Retention test for every row: *open or still owed, and no other home.* If either
  fails, it leaves.
- **Entry classes + 40-word cap (W5 direction):** Decision / Build / Measurement /
  Hygiene — see [`W5 ADR`](docs/adr/2026-08-07-w5-governance-diet.md); prefer links
  over prose.

**Standing base case:** absent an N-clear candidate, the 2026-11-08 §4 falsifier
(prop-portfolio program) reads **FALSIFIED** — the four-firms ADR's demotion clause is
the designed, legitimate outcome if the date passes without one. See
[`N-2026-08-18-iteration2-identify-notice.md`](docs/notes/notice/N-2026-08-18-iteration2-identify-notice.md) §0.

---

## OPERATOR QUEUE — strictly ordered, ≤5 live items

**Agent-hours are cheap and budgeted (K-ledger, cost dry-runs, $700 spend ceiling);
operator-hours are the binding resource and were the only unrationed one.** This
board is the sequencing fix: the next operator-attention items in dependency order,
so they are not served in whatever order the week happens to present them.
**Pointers only** — each item's owner artifact holds the detail (Rule 7).

**Standing rule: new decision packets, advisor triage, and sizing questions queue
BEHIND this list.** Items leave when done; it stays ≤5 so it cannot decay into a backlog.

> **This cap IS the portfolio-level Survive bound** (ruled 2026-08-09,
> [`ADR`](docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md)). The bound is
> **concurrency-denominated, not hours-denominated** — Rule 2's §5 forbidden move #2
> bars expressing a budget in wall-clock "anywhere in canon or ADR" (*"neither client
> can meter wall-clock"*), and nothing in the estate meters operator time. The
> rationale paragraph above was deleted 2026-08-03 and **restored 2026-08-09**; four
> surfaces cite it, one with a runnable command
> (`docs/notes/2026-07-29-comparative-advantage-thesis.md:369`).

| # | Item | Owner artifact | Blocks |
|---|---|---|---|
| 1 | **B7-REFIRE Stage 1 + M1** — both wait on an acceptable strategy on the ruled (Python-native) host. Eval live; no book deployed | [`GO ADR Addendum`](docs/adr/2026-07-17-c1-rail-build-account-registration-go.md) · [`S2`](docs/adr/2026-08-07-loop-s2-signal-host-fork.md) · [`M1`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) | live-signal / arming path |
| 2 | **Per-trade dollar-loss bound — elect within-day hard-cap vs. live-observed tripwire** (Q-TRADECAP-1 `RESOLVED`: confirmed no bound exists anywhere in the live sizing/arming path on Tradeify's intraday-enforced geometry). Orphaned CFD-era fork from `1r_estimation.md`, never re-scoped until now | [`Q-TRADECAP-1 closure`](docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md) · [`1r_estimation.md`](docs/methodology/1r_estimation.md) L231–263 | any future arming session carries the gap unresolved |

---

## Executed operator decisions — decision index

ADRs own the decision narrative ([`docs/operational_rules.md`](docs/operational_rules.md)
Rule 7; [`docs/adr/2026-07-16-root-doc-charter-dedup.md`](docs/adr/2026-07-16-root-doc-charter-dedup.md)).
One line per executed decision, newest first — consequence + owner. Posture summary:
[`CLAUDE.md`](CLAUDE.md) §Live-execution posture.

- **2026-08-23** — `Q-MONSURF-1` closed `RESOLVED` — monitoring obligations corrected from one stranded "first live fill" class to three true gate depths; M-B (idle-clock monitor) acceptance battery passes 0 missed / 0 spurious across all 312 real historical weeks, mutation-verified, registration-ready (gated on F3 only). Board triage rewritten. [`closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
- **2026-08-23** — `Q-TRADECAP-1` closed `RESOLVED` — no per-trade dollar-loss bound exists anywhere in the live sizing/arming path (sizing law, M1 arming interlock, EM2, disaster-stop all checked, all confirmed absent) on Tradeify's intraday-enforced geometry. Successor decision packet queued (row 2). [`closure`](docs/briefs/closures/Q-TRADECAP-1-closure-resolved.md)
- **2026-08-23** — Fork F1 ruled (12:59, after an 11:37/12:23 concurrent-session sweep had just re-confirmed F1's deferred posture as precedent for the sibling PARTIAL-disposition addendum — considered override, not a miss): a Tradeify-resting §4 discharge does not satisfy the four-firms falsifier (functionally a 3-firm set — Bulenox/MFFU/BluSky — for §4 counting purposes); queue row 1 closed. `MNQTAPE-2` ($308.69 larger-N tape-aggressor replication) declined NO-GO same session. MSL-S4 (MGC) Pine hash-pinned locally; confirmed already `PARKED` (post-`AMBIGUOUS-HOLD` Explore-confirm) — its RUNBOOK's TV-backtest recommendation is stale/superseded, not a live next step. Every currently-sourced MSL Tradeify candidate is now closed or PARKED. [`ADR addendum`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) [`prereg`](docs/briefs/pre-registration/2026-08-23-mnqtape-2-larger-n-prereg.md) [`MSL-S4 card`](core/strategies/candidates/candidates_CARD.md)
- **2026-08-23** — Coldstore Phase B/C: operator GO retired Guardian Gold + Aegis USDJPY from living `dd_protection.BASE_RISK` (LOCKED legacy book table now 2 strategies — Striker DJ30/NAS100 only); frozen risk% moved to `historical_challenge.HISTORICAL_CHALLENGE_BASE_RISK`, authorization axis unchanged. [`Phase B ADR`](docs/adr/2026-08-23-strategy-coldstore-phase-b.md) [`Phase C ADR`](docs/adr/2026-08-23-strategy-coldstore-phase-c.md) [`PR #122`](https://github.com/Joshua-Asante/first-passage/pull/122)
- **2026-08-23** — SESSIONS class D tightened to a judgment-call gate; stub-entry mechanism added for Open/next continuity without violating `sessions-append-only`. [`W5 ADR addendum`](docs/adr/2026-08-07-w5-governance-diet.md) [`PR #120`](https://github.com/Joshua-Asante/first-passage/pull/120)
- **2026-08-23** — Blind channel: canonical pre-G0 kill count corrected 1/3 → 2/3 (`MNQ-SIZEDIV-1`'s own 2026-08-15 kill had been recorded in this file and `MNQ.md` since the 2026-08-16 port but never synced to the channel ADR's own canonical line — 8-day mirror/owner lag, disclosed and fixed). Second door re-walk against the deep-lane's cached 6A/M6A and GC/MGC panels: entry-geometry/dense-1m temporal-selectivity doors reopen on those two non-index instruments (still blocked on MNQ); FM-4's reach to a pre-G0 kill's instrument-hop, and whether the sibling lane's own GO/cost-dry-run discharges this channel's identical requirement, both flagged operator-call-needed. No construct named; one pre-G0 kill slot remains before generation-dry. [`channel ADR addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-22** — DL-2 (M6A × `prior-session-breakout-continuation`, `NEW` mechanism id) prereg `FROZEN`; §6 step 1 pulls landed $0.0000. [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md) [`prereg`](docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md)
- **2026-08-22** — Leftover Proposed ADRs: four `Accepted`, one `Withdrawn`. [`disaster-stop`](docs/adr/2026-07-28-c1-disaster-stop-payload-supported.md) [`venue-binding`](docs/adr/2026-08-05-strategy-venue-binding-axis.md) [`W1`](docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md) [`public-visibility`](docs/adr/2026-08-14-repo-public-visibility-transition.md) [`WATCH-1H withdrawn`](docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md)
- **2026-08-21** — `REPO_MAP.md` second-pass coherence repair; §5 coverage-check repaired. [`campaign addendum`](docs/notes/audits/2026-08-21-coherence-campaign.md)
- **2026-08-21** — CFO subscription-ledger consolidation ratified (one ledger + monthly reconfirm). [`ADR`](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md)
- **2026-08-21** — `REGIME-CANDIDATE` flag lane `Accepted`; discovery-campaign template restored. [`ADR`](docs/adr/2026-07-26-regime-candidate-flag-lane.md)
- **2026-08-21** — Persona hierarchy narrowed to Front Office; Middle/Back-office run as mechanical gates. [`ADR`](docs/adr/2026-08-21-persona-hierarchy-front-office-only.md)
- **2026-08-21** — `Q-M1WIRE-1` closed `FALSIFIED`. [`M1 ADR`](docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) [`closure`](docs/briefs/closures/Q-M1WIRE-1-closure-falsified.md)
- **2026-08-21** — Incumbent CI honesty patches landed. [`PR #75`](https://github.com/Joshua-Asante/first-passage/pull/75) [`SESSIONS 2026-08-21e`](docs/SESSIONS.md)
- **2026-08-21** — C-P1-10 CATALOG `--slug` archive landed. [`campaign`](docs/notes/audits/2026-08-21-coherence-campaign.md) [`CATALOG`](lab/CATALOG.md)
- **2026-08-21** — Coherence leftover menu ratified: F1 HOLD; B7/M1 HOLD; H1–H5 GO; H6–H13 HOLD. [`campaign`](docs/notes/audits/2026-08-21-coherence-campaign.md)
- **2026-08-20** — P4 Databento cost dry-run + concentration: HOLD stands, evidence leans against. [`P4_DRYRUN`](lab/analysis/harvest/six_lead_cf_2026-08-17/P4_DRYRUN.md)
- **2026-08-20** — N-SURV disclosure ADR + Rule 0 ADR ratified. [`N-SURV ADR`](docs/adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md) [`Rule 0 ADR`](docs/adr/2026-08-20-rule0-anchor-verification-and-triage-discipline.md)
- **2026-08-20** — `Q-TODVOL-1` frozen and D2-falsified same day. [`RESULTS`](lab/archive/todvol_1_2026-08-20/RESULTS.md)
- **2026-08-20** — Six-lead pursuit P4/P5 un-HOLD'd and dispositioned — P4 stays `HOLD` (sharper reason), P5 closes `UNSCREENABLE`. [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) [`P4_ROUTEMEMO`](lab/analysis/harvest/six_lead_cf_2026-08-17/P4_ROUTEMEMO.md)
- **2026-08-20** — `Q-ORBSURV-1` closed `FALSIFIED` — cushion-sizing's gate-clear is k-dependent, not robust. [`closure`](docs/briefs/closures/Q-ORBSURV-1-closure-falsified.md) [`brief`](docs/briefs/Q-ORBSURV-1-cushion-sizing-gate-configurations.md)
- **2026-08-20** — `Q-NSURV-2` closed `RESOLVED` — additive N-SURV disclosure layer confirmed buildable; light ADR `Accepted` same day. [`ADR`](docs/adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md) [`closure`](docs/briefs/closures/Q-NSURV-2-closure-resolved.md)
- **2026-08-20** — N-SURV single-history magnitude blindspot HOLD→RESOLVED (`Q-NSURV-1`). [`closure`](docs/briefs/closures/Q-NSURV-1-closure-resolved.md)
- **2026-08-19** — `"cme"` broker panel admitted; `breadth.py`'s risk-N_eff mechanism revived on canonical data. [`ADR`](docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md) [`design spec`](docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md)
- **2026-08-19** — Persona-hierarchy review panel ADR ratified; first real C-suite panel run (GSUB-2) SUBTRACTs b2 + c1. [`ADR`](docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md) [`closure`](docs/briefs/closures/GSUB-2-closure-resolved-loadbearing.md)
- **2026-08-18** — MNQ family-K disclosure: Notice-phase closed manifests and Cap-seat K bank. [`ADR 2026-08-04` Addendum](docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md) [`MNQ.md` §K_BANKED](ops/instruments/MNQ.md)
- **2026-08-18** — Q-TRAINKILL-3 `AMBIGUOUS-HOLD` — event-class blocks split; TRAINKILL census STOP. [`closure`](docs/briefs/closures/Q-TRAINKILL-3-closure-ambiguous-hold.md) [`RESULTS`](lab/analysis/_inbox/q_trainkill_3_2026-08/RESULTS.md)
- **2026-08-18** — Q-TRAINKILL-2 `AMBIGUOUS-HOLD` — both named alternates fit; no singleton power finding. [`closure`](docs/briefs/closures/Q-TRAINKILL-2-closure-ambiguous-hold.md) [`RESULTS`](lab/analysis/_inbox/q_trainkill_2_2026-08/RESULTS.md)
- **2026-08-18** — Q-TRAINKILL-1 `AMBIGUOUS-HOLD` — no named power finding; no gate number moves. [`closure`](docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md) [`RESULTS`](lab/analysis/_inbox/q_trainkill_1_2026-08/RESULTS.md)
- **2026-08-18** — Q-EXPR-1 `RESOLVED` (H1) — next slate admission screens claim horizon vs E1. [`closure`](docs/briefs/closures/Q-EXPR-1-closure-resolved.md) [`RESULTS`](lab/archive/q_expr_1_2026-08/RESULTS.md)
- **2026-08-18** — Q-CONDVAL-1 `FALSIFIED` — S1b conditioner-engineering branch parked. [`closure`](docs/briefs/closures/Q-CONDVAL-1-closure-falsified.md) [`RESULTS`](lab/archive/q_condval_1_2026-08/RESULTS.md)
- **2026-08-17** — Six-lead P3 (L5 curve-slope) un-HOLD → GO → sleeve CLOSED (venue). [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) [`P3_DRYRUN`](lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md)
- **2026-08-17** — Q-POLFRONT-1 intraday-honest remeasure: 5.1× policy frontier does not survive. [`RESULTS`](lab/analysis/c1/q_polfront_1_2026-08/RESULTS_INTRADAY_HONEST.md)
- **2026-08-17** — Six-lead pursuit channel-scope addendum landed; queue row 3 closes. [`harvest intake ADR` addendum](docs/adr/2026-07-15-external-mechanism-harvest-intake.md#addendum-2026-08-17--openalex-admitted-as-a-sourcing-channel-substitute) [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md)
- **2026-08-17** — Harvest §4 limb-2 counter ruled: P1-CF/P2-CF FAIL does NOT increment. [`harvest intake ADR` — Ruling 2026-08-17](docs/adr/2026-07-15-external-mechanism-harvest-intake.md) [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md)
- **2026-08-17** — Six-lead pursuit P1-CF/P2-CF EXECUTED → FAIL, all four legs (MGC+6J). [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md) [`CF LOG`](lab/analysis/harvest/six_lead_cf_2026-08-17/LOG.md)
- **2026-08-17** — Six-lead Phase 0 executed; same-day Koijen count 6→5. [`plan`](docs/briefs/2026-08-17-six-lead-pursuit-plan.md)
- **2026-08-17** — Koijen axis-2 OpenAlex substitute: 6 screen-level leads, none admitted. [`SOURCES_LOG`](lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md)
- **2026-08-17** — MSL-S2B successor's CON-5 D2 falsifier executed → `D2_FAIL`; route B closes for this construct-shape at $0. [`ADR`](docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) [`LOG`](lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_s2b_con5_d2_2026-08-17_LOG.md)
- **2026-08-16** — DL-1 ABANDONED (train scoring executed). [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md) [`results`](lab/archive/dl1_mgc_orc_2026-08-16/train_results.json)
- **2026-08-16** — CON-5 pause scope ruled: dense-1m route-scoped, with a $0 cheap-falsifier gate for out-of-lane route-① reliance (operator election, third of three options). [`ADR`](docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
- **2026-08-16** — Weekly venue-idle token: fresh-decision-per-week is the standing design. [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md)
- **2026-08-16** — DL-1 prereg `FROZEN` (operator GO). [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md) [`prereg`](docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md)
- **2026-08-16** — Databento parent-era cost dry-run executed; deep-lane GO-1 fully discharged. [`charter addendum`](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
- **2026-08-16** — Deep-iteration lane charter `Accepted` (operator "P2 + GO", overriding its own HOLD default eyes-open). [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
- **2026-08-16** — State-policy packet marked `P2`. [`closure`](docs/briefs/closures/STATE-POLICY-closure-resolved-p2.md)
- **2026-08-16** — Governance-holes closing pass (4 of 5 S4 items). [`AMBIGUOUS-HOLD ADR`](docs/adr/2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds.md)
- **2026-08-15** — `MNQ-SIZEDIV-1` KILLED pre-G0 at the Stage-2 falsifier; $90.22 spent; pre-G0 kill count → 2/3. [`freeze`](lab/analysis/c1/mnq_sizediv_blind_2026-08/DESIGN_FREEZE.md) [`STAGE2_FALSIFIER`](lab/analysis/c1/mnq_sizediv_blind_2026-08/STAGE2_FALSIFIER.md)
- **2026-08-15** — Blind-channel staged GO elected; `MNQ-SIZEDIV-1` frozen pre-data. [`freeze`](lab/analysis/c1/mnq_sizediv_blind_2026-08/DESIGN_FREEZE.md)
- **2026-08-15** — Harvest §4 limb 2 pin marked `no`. [`harvest addendum`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **2026-08-15** — Harvest §4 limb 2 (R10) `Accepted`. [`harvest addendum`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **2026-08-15** — 08-03 gate-stack R3/R4/R5/R6 executed; R10 drafted then `Accepted` same day. [`harvest addendum`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md) [`08-03 audit`](docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)
- **2026-08-15** — Dense-1m unpause Board U0 KEEP recorded. [`closure`](docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md) [`packet`](docs/briefs/2026-08-15-dense1m-lane-unpause-review.md)
- **2026-08-15** — Blind-channel generation attempt: naming set empty. [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — Blind-channel consecutive-pre-G0-kill threshold elected N = 3. [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — `Q-CAPBAND-1` closed `RESOLVED` — Cap 1.0 evidence-ratified on the named axes. [`closure`](docs/briefs/closures/Q-CAPBAND-1-closure-resolved.md) [2026-08-03 audit](docs/notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)
- **2026-08-15** — Aegis 1.83 WITHDRAWN as a reachability ceiling; `Q-CAPBAND-1` opened. [`Q-CAPBAND-1`](docs/briefs/Q-CAPBAND-1-cap-band-counterfactual.md) [`pre-reg`](docs/briefs/pre-registration/Q-CAPBAND-1-verdict-preregistration.md)
- **2026-08-15** — Pre-G0 kills are NOT §4 strikes (blind channel). [`addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — Blind-channel cost geometry measured; `MNQ-ANALOGUE-1` killed pre-G0 at $0/K=0. [`route ruling`](docs/adr/2026-08-15-analogue-modality-route-ruling.md) [`K-cap addendum`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — No-counterparty statistical sourcing channel `Accepted` (full-tier ADR). [`ADR`](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md)
- **2026-08-15** — F1/F2/Board-lite discharged (3 light ADRs). [`F1 ADR`](docs/adr/2026-08-15-regime-gate-scope-ratification.md) [`Board-lite ADR`](docs/adr/2026-08-15-board-lite-label-ratification.md)
- **2026-08-15** — `Q-BUSTGATE-2` closed `RESOLVED` — bust ceiling reconfirmed unchanged. [`closure`](docs/briefs/closures/Q-BUSTGATE-2-closure-resolved.md) [`brief`](docs/briefs/Q-BUSTGATE-2-bust-gate-re-derivation-2026-08.md)
- **2026-08-15** — MSL-era wall-scope audit + 08-03 follow-up verification landed. [`audit`](docs/notes/audits/programme-audit/2026-08-15-msl-wall-scope-audit.md)
- **2026-08-14** — MSL WHO-track `STILL DRY` (estate-wide). [`notice`](docs/notes/notice/N-2026-08-14-msl-who-track.md)
- **2026-08-14** — MSL §7 E1 HOLD recorded. [`closure`](docs/briefs/closures/MSL-S7-closure-resolved-e1-hold.md) [`packet`](docs/briefs/2026-08-14-msl-slate-generation-review.md)
- **2026-08-14** — MSL §7 slate-generation review packet authored; election then recorded E1 (line above). [`packet`](docs/briefs/2026-08-14-msl-slate-generation-review.md)
- **2026-08-14** — MSL slate-3 `BLOCKED` (mechanism-dry). notice (`git show ef48b015:docs/notes/notice/N-2026-08-14-msl-slate-3-constraints.md`)
- **2026-08-14** — MSL-S2B Stage-0/1 `STAGE-1 FAIL` (route; pre-G0). [`closure`](docs/briefs/closures/MSL-S2B-closure-stage1-fail-route.md) [`STAGE1`](lab/analysis/c1/msl_s2b_mym_2026-08/STAGE1.md)
- **2026-08-13** — Dedup-first-before-new-work `Accepted`; §7 mechanical wiring merged (PR #800). [`ADR`](docs/adr/2026-08-13-dedup-first-before-new-work.md)
- **2026-08-13** — Tradeify Select 100K checkout price re-sourced (PR #801). note (`git show 67e4b209:docs/notes/2026-08-13-tradeify-select-100k-checkout-price.md`)
- **2026-08-13** — MSL-C3-K2 dual-axis explore FALSIFIED. [`closure`](docs/briefs/closures/MSL-C3-K2-closure-falsified.md) [`PREREG_G0`](lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
- **2026-08-13** — MSL-C3-K2 dual-axis G0 FROZEN. [`ADR`](docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) [`PREREG_G0`](lab/archive/msl_c3_m2k_2026-08/PREREG_G0.md)
- **2026-08-13** — MSL-C3-K2 dual-axis Stage-1 revive ELECTED. [`ADR`](docs/adr/2026-08-13-msl-c3-k2-dual-axis-revive.md) [`STAGE1_K2`](lab/archive/msl_c3_m2k_2026-08/STAGE1_K2.md)
- **2026-08-13** — MSL-S2A explore GO → `FALSIFIED` (N-ACT). [closure](docs/briefs/closures/MSL-S2A-closure-falsified.md) [`RESULTS_g2`](lab/archive/msl_s2a_mcl_2026-08/RESULTS_g2.md)
- **2026-08-13** — MSL-S2A B4 GO → G0 FROZEN. [`PREREG_G0`](lab/archive/msl_s2a_mcl_2026-08/PREREG_G0.md)
- **2026-08-13** — MSL slate-2 box ELECTED + P3.4 S2A Stage-1 PASS (B4 unpaid). [`ADR`](docs/adr/2026-08-13-msl-slate-2-design-box.md) [STAGE1](lab/archive/msl_s2a_mcl_2026-08/STAGE1.md)
- **2026-08-13** — MSL-C2 explore GO → `FALSIFIED` (both-arms CI&lt;0). [closure](docs/briefs/closures/MSL-C2-closure-falsified.md) [`RESULTS_g2`](lab/archive/msl_c2_mgc_2026-08/RESULTS_g2.md)
- **2026-08-13** — `implied_annualized_sr` DEMOTED gate → report-only (`IMPLIED-SR-REPORT-ONLY-2026-08-13`); Tradeify-native fade design-region REOPENED as geometry. [`ADR`](docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md)
- **2026-08-12** — MSL-C2 B4 GO → G0 FROZEN. [`PREREG_G0`](lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md)
- **2026-08-12** — MSL implied-SR off kill list (interim; now Superseded). [ADR](docs/adr/2026-08-12-msl-implied-sr-disclosure-not-kill.md)
- **2026-08-12** — MSL Board B1–B3 + B8 ratified. [occupancy](docs/adr/2026-08-12-msl-mym-occupancy-release.md) [ratification](docs/adr/2026-08-12-msl-sourcing-channel-ratification.md)
- **2026-08-12** — Q-TXG-1 CLOSED — FALSIFIED-at-walls (operator A). [lane closure](docs/briefs/closures/Q-TXG-1-closure-falsified-at-walls.md) [packet](docs/briefs/Q-TXG-1-ha-reargument.md)
- **2026-08-12** — Q-TXG-1 cell #2 striker×MNQ → DEAD(N-SURV). [closure](docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) [PANEL_SCORE](lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json)
- **2026-08-12** — Q-TXG-1 Blocks 2–3 frozen; HARD STOP before scoring. [`ELECTION`](lab/archive/transfer_expression_grid_2026-08/ELECTION.md)
- **2026-08-12** — Q-TNEC-CON-5 Branch A STOP elected. [closure](docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
- **2026-08-11** — `Q-TXG-1` Block 1 executed at $0. [`GRID_RESULTS`](lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.md) [`PREREG`](lab/archive/transfer_expression_grid_2026-08/PREREG.md)
- **2026-08-11** — `Q-SCORE-1` Block 1 H_A FALSIFIED at $0. [`closure`](docs/briefs/closures/Q-SCORE-1-closure-falsified.md) [`BLOCK1_RESULTS`](lab/archive/approach_scoreboard_2026-08/BLOCK1_RESULTS.md)
- **2026-08-11** — `Q-MCLTAS-1` closed `FALSIFIED` (Wall B magnitude) at $0/K=0 — the probe was never run. [`closure`](docs/briefs/closures/Q-MCLTAS-1-closure-falsified.md) [`RESULTS`](lab/analysis/c1/cheap_falsifiers_2026-08/_probe_stage0_RESULTS_2026-08-11.md)
- **2026-08-11** — `Q-TNEC-ENV-1` post-closure rulings (JA, light record). [`closure`](docs/briefs/closures/Q-TNEC-ENV-1-closure.md)
- **2026-08-11** — `Q-TNEC-ENV-1` closed `NULL` (H_B=0, STOP per PREREG F7) at $0. [`closure`](docs/briefs/closures/Q-TNEC-ENV-1-closure.md) [`RESULTS`](lab/archive/tnec_envelope_compile_2026-08/RESULTS.md)
- **2026-08-11** — `Q-TNEC-ENV-1` Phase A executed at $0. [`PREREG`](lab/archive/tnec_envelope_compile_2026-08/PREREG.md) [`RESULTS`](lab/archive/tnec_envelope_compile_2026-08/RESULTS.md)
- **2026-08-10** — Temporal selectivity ruled outside mapped cost-ratio levers; dense-1m door-check repaired. [`ADR`](docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)
- **2026-08-10** — Dense-1m cell #3 cheap falsifier `FALSIFIED` (exit-geometry) at $0. [`falsifier`](lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md)
- **2026-08-10** — `Q-TNEC-CON-2` explore GO → `AMBIGUOUS-HOLD` (non-promotable) at $0. [`closure`](docs/briefs/closures/Q-TNEC-CON-2-closure-ambiguous-hold.md) [`RESULTS_g2`](lab/analysis/c1/mnq_tnec_con2_compression_break_2026-08/RESULTS_g2.md)
- **2026-08-10** — `implied_annualized_sr` PROMOTED report-only → gate (`IMPLIED-SR-GATE-2026-08-10`, JA in-session); Tradeify-native fade design-region CLOSED on its own arithmetic. [`ADR`](docs/adr/2026-08-10-implied-sr-plausibility-gate.md)
- **2026-08-09** — GRAND tier `Accepted` + GSUB-1 CLOSED `RESOLVED-LOADBEARING` (JA in-session, same day). [`ADR`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **2026-08-09** — `Q-MNQDTL-CON-1` explore GO → `FALSIFIED` (STOP catalogue) at $0. [`closure`](docs/briefs/closures/Q-MNQDTL-CON-1-closure-falsified.md) [`RESULTS`](lab/archive/mnq_con1_dense1m_stage0_2026-08/RESULTS.md)
- **2026-08-09** — `Q-MNQDTL-CON-1` ENTRY named + explore harness wired. [`PREREG_G0`](lab/archive/mnq_con1_dense1m_stage0_2026-08/PREREG_G0.md) [#699](https://github.com/Joshua-Asante/first-passage-archive/pull/699)
- **2026-08-08** — PR693 parallel integrate: CapFLOW Cap-spend path BLOCKED on join. [Cap RESULTS](lab/archive/mnq_capflow_orb_r_2026-08/RESULTS.md)
- **2026-08-08** — TNEC-1 intake gate `RATIFIED` + edge-cohort ADR `Accepted` (§8 JA). [`ADR`](docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md) [`Q-CAPRES-2`](docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md)
- **2026-08-08** — Absolute path items 1–3 landed (`Q-MNQSEL-2` RESOLVED; Cap reservation unpaid). [`Q-CAPRES-2`](docs/briefs/Q-CAPRES-2-mnq-cap-seat-reservation.md)
- **2026-08-08** — `Q-R2FLOW-1` explore GO → G2 `FALSIFIED` (STOP catalogue) at $0. [`brief`](docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md) [`RESULTS_g2`](lab/archive/mnq_r2flow_routeb_2026-08/RESULTS_g2.md)
- **2026-08-08** — `Q-R2AGRUN-1` CLOSED non-promotable (`AMBIGUOUS-HOLD`); `Q-R2FLOW-1` G0 frozen — explore GO unpaid. [`closure`](docs/briefs/closures/Q-R2AGRUN-1-closure-ambiguous-hold.md) [`brief`](docs/briefs/Q-R2FLOW-1-signed-minute-flow-route-b-scoping.md)
- **2026-08-08** — `Q-R2AGRUN-1` explore GO → G2 `AMBIGUOUS-HOLD` (ITERATE) at $0. [`brief`](docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md) [`RESULTS_g2`](lab/analysis/c1/mnq_r2agrun_routeb_2026-08/RESULTS_g2.md)
- **2026-08-08** — `Q-R2AGRUN-1` G0 frozen (MNQDTL R2) — signed aggressor-run trade-count → 60 s mid; explore GO unpaid. [`brief`](docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md) [`PREREG_G0`](lab/analysis/c1/mnq_r2agrun_routeb_2026-08/PREREG_G0.md)
- **2026-08-08** — Quarterly dd_protection/regime review run: item 1 (C2→C0 revert check) confirmed dead, removed from the `fwd-quarterly-regime-ddrevert` cron. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md) [`claims-rescope ADR`](docs/adr/2026-07-11-challenge-era-claims-rescope.md)
- **2026-08-08** — ADR ceremony stakes-tiering `Accepted` (JA). [`ADR`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **2026-08-08** — `Q-R2VBUCK-1` explore GO ratified (MNQDTL R2) → G2 `FALSIFIED` (STOP catalogue) at $0. [`brief`](docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md) [`RESULTS_g2`](lab/archive/mnq_r2vbuck_routeb_2026-08/RESULTS_g2.md)
- **2026-08-08** — SPEC S2b `Accepted` + S2b build ADR `Accepted` + operator build GO. [`build ADR`](docs/adr/2026-08-08-s2b-signal-daemon-build.md) [`SPEC S2b`](docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md)
- **2026-08-07** — Loop S1 environment ratification `Accepted` — F2+F3 ruled. [`S1 ADR`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) [SPEC S1](docs/spec/2026-08-07-loop-s1-environment-ratification-spec.md)
- **2026-08-07** — Closed-loop S1–S6 specs opened; S1 ADR `Accepted` same day; S3/S7 specs remain `PROPOSED`. [index](docs/spec/2026-08-07-loop-spec-index.md)
- **2026-08-07** — `Q-MNQSEL-1` Phase-0 RUN → `FALSIFIED` (C2) at $0/K=0 — STOP this restart-clock universe. [`brief`](docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md) [`RESULTS`](lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md)
- **2026-08-06** — EM0–EM5 screen `RATIFIED`; `Q-OFCHAN-1` G2 `VOID-COVERAGE`. [`spec`](docs/spec/2026-08-05-eval-mechanism-shape-screen.md)

> ⚠ **Truncated to the newest 15 at the 2026-08-08 Great Prune.** Older executed decisions are
> owned by their ADRs (`docs/adr/`, tombstoned rows in [`TOMBSTONES.md`](docs/adr/TOMBSTONES.md));
> full prior index: `git show pre-prune-2026-08-08:STATE.md`.

## Dormant cross-session threads

Open investigations with no current session home. Closed threads leave (owners =
closures/ADRs).

Dormant threads b6/b7 (PARK — open) → [`docs/pursuits/`](docs/pursuits/) (ratified 2026-08-09, GSUB-1
Phase 3). c5/Q-MSCHAN-1 (SUBTRACT — dead) left this section per its own rule above; its record
stands alone at [`c5`](docs/pursuits/c5-q-mschan-1.md).

**Registry backfill debt (2026-08-15).** 33 closures classified as strategy-grounds kills
(read against each one's actual `**Verdict:**` line, not filename) never got a
`rejected_candidates.md` row — the 2026-08-03→08-11 feed-stop the registry-feed sub-rule
(9) was written to close. Forward-only: nothing new accretes here. Backfill is one
judgment call per row (which heading, how it's worded) and stays operator-paced —
`python scripts/check_closure_disposition.py --list-debt` lists the current set;
rows leave this debt only by landing in `docs/rejected_candidates.md`, not by editing
`REGISTRY_DEBT_2026_08` directly.

---

## Scheduled forward triggers

Canonical dates/criteria live with their owners; this board is a pointer so
obligations are not lost between sessions. Closed/retired/discharged rows are
deleted (not struck).

### Weekly — recurring (rolling; next deadline **2026-08-28**, bucket 08-24→08-28)

> Prior week 08-17→08-21 satisfied (operator-confirmed 2026-08-22). New week unpaid. Row stays
> live — roll this date forward each Monday. **Recurrence ruled 2026-08-16** (decision index,
> above): re-electing coverage every week is the standing design, not an open question — this
> row's own weekly cadence is that design in practice, not a symptom of anything unresolved.

- **Venue idle-clock — ≥1 operator-placed trade per Mon–Fri week on the live account (identifier
  redacted from the public tree).**
  Consequence of a miss is account **DELETION, not a warning** (Tradeify art. 10468318; venue day
  is 6pm-anchored, so a Fri 18:30 ET fill belongs to the *next* session). ⚠ **No agent may place
  it** — operator-placed at the venue; the rail is not the instrument (`dry_run` stays `true`).
  **Roll this date forward each Monday.** Booked here 2026-08-09 *specifically so the existing
  daily 07:04 `daily-repo-truth-sync` forward-obligation radar surfaces it* — that task reads this
  section for obligations dated within 7 days, and row 0's queue-table placement was invisible to
  it.   [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
  [audit FU-1](docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md)

### Monthly — recurring (rolling; next deadline **2026-09-21**)

> **Recurrence ruled 2026-08-21** ([`ADR`](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md)
> D3, operator: "reconfirm ledger once a month"): the same recurring-obligation shape as the weekly
> row above, reusing the same radar rather than standing up a second scheduling surface. **Roll this
> date forward each occurrence** (same day-of-month as this row's own creation, 21st).

- **Subscription-ledger reconfirm — `docs/pursuits/SUBSCRIPTION_LEDGER.md`'s seven d11-d17 rows
  re-checked against current reality.**
  Confirm each "Last confirmed" date and $/mo figure still holds; update any that changed; chase the
  two still-open rows (Fly.io, Tradeify) if a figure has since surfaced. A null result (nothing
  changed) is still a reconfirm — record it, don't skip it (CFO 2026-08-21 recommendation #4: silence
  is not evidence of currency). Booked here *specifically so the existing daily `daily-repo-truth-sync`
  forward-obligation radar surfaces it*, same mechanism as the weekly row above — no new
  infrastructure. [`ADR`](docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md) ·
  [`cfo.md`](docs/personas/cfo.md) (standing check + Writes field, D3) ·
  [`cfo-log.md`](docs/personas/cfo-log.md) (source recommendations, 2026-08-21)

### No fixed date / gated

> ⚠ **Monitoring obligations were recorded as one stranded "first live fill" class; `Q-MONSURF-1`
> (`RESOLVED` 2026-08-23) found they sit at three distinct gate depths — corrected here, not
> restated as before.** [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) kept the
> incumbent `Tradeify_Select_100K` eval as the environment; the weekly idle-clock is live; there
> is no c1 book (locked Striker legs stay barred). **Q-SIGID-1** is **not** among any of the below
> — pursuit standing **KEEP**, resolving via the S2b daemon; see [`c2`](docs/pursuits/c2-q-sigid-1.md).
>
> - **M-B (idle-clock monitor) — gated on F3 (a registered account), NOT first live fill.**
>   `RESOLVED`/registration-ready: acceptance battery passed 0 missed / 0 spurious across all 312
>   real historical weeks, mutation-tested. No further design work owed — deploys alert-only the
>   moment F3 registers a successor venue (Phase 5: re-freeze idle-clock semantics against that
>   venue's own DP2-verified rules if they differ from the Tradeify-shaped provisional freeze used
>   here, then wire to the live account). [`closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
> - **M-C (ECR live-edge-capture monitor + per-fill add-slippage capture) — genuinely fill-gated.**
>   Correctly waits on first strategy-signal fill; row below, pointing at its own prereg.
> - **M-A (shadow market-data regime observer) — elective, not scheduled, gate itself unruled.**
>   Venue-free but low-consequence (alerts on a book that isn't trading). Whether the design's
>   own "first live fill" build gate binds a pure market-data observer (vs. only a fill-coupled
>   monitor) is an **explicit operator ruling still owed** — not assumed either way. Row below.
>
> **Two other threads share the same prior home** (deleted operator-queue row 3), unrelated to
> the monitoring triage above:
>
> - **lifecycle Call-1** — rolling-PF σ-source has no live data until a strategy is on the
>   book. Its 2026-08-08 review row below still stands but can only return AMBIGUOUS on thin data.
> - **ORB decay re-scope** — no other row in this file; recorded here so the deletion of queue
>   row 3 does not silently lose it.
>
> `PREREG-C1-DEDUPE-1` (row below) is unrelated to monitoring — waits on M1 `RESOLVED` + a
> separate operator GO, not on a live fill. Everything above except M-B waits on the same thing as
> queue row 1 (B7 / M1); M-B alone is now gated on F3 only. Not closed, not discharged, not
> re-homed to a successor venue — F3 was no-migration (S1).
> [`S1`](docs/adr/2026-08-07-loop-s1-environment-ratification.md) ·
> [`ADR 2026-08-04`](docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md) (Striker-book bar)

- **Idle-clock monitor (M-B) — registration-ready, gated on F3 only** — Q-MONSURF-1 `RESOLVED`; standalone module built and acceptance-tested (0 missed / 0 spurious, all 312 real historical weeks, mutation-verified). No design work owed; wire to the live account at F3 registration (Phase 5 — re-freeze idle-clock semantics against the actual successor's DP2-verified rules first if they differ from the Tradeify-shaped provisional freeze). [`module`](lab/analysis/c1/msl_monsurf_1_idle_clock_2026-08/idle_clock_monitor.py) · [`closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
- **Sentinel Tier-2/3 promotion (limb B1)** — before next quarterly slate; promotion not a build. [`sentinel design`](docs/spec/2026-06-23-inqhiori-sentinel-design.md) · [`Hermes closure`](docs/briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md)
- **PREREG-C1-DEDUPE-1** — gated on M1 `RESOLVED` + separate operator GO. [`pre-reg`](docs/spec/PREREG-C1-DEDUPE-1-intent-key-functional-property.md) · [`impl plan`](docs/spec/PREREG-C1-DEDUPE-1-implementation-plan.md)
- **R&D tooling T2 / T3 / T4** — GO 2026-08-23 executed (kit + breadth calibration + synthetic Call-1 OC). T4 Task 3 state writer still fill-gated. [`ADR §7`](docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md) · [T4 RESULTS](docs/notes/research/2026-08-23-call1-oc-synthetic.md)
- **Per-fill add-slippage capture (B7 Stage 2b) — Q-MONSURF-1 M-C** — waits first strategy-signal **add** fill; prerequisite ledger price-capture landed. [`Q-COSTGEO-3`](docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md) · B7 procedure in the private archive
- **Forward regime monitor / decompound limb-2 successor — Q-MONSURF-1 M-A (elective, not scheduled)** — ORPHANED same hole: CFD limb-2 cannot fire; venue-native design landed (not ratified); build-gate scope ruling owed (does "first live fill" bind a pure market-data observer?) before this is even buildable. [`decompound ADR §Addendum 2026-08-03`](docs/adr/2026-06-07-decompound-remc-hold.md) · [`Pepperstone retirement`](docs/adr/2026-08-02-pepperstone-feed-retirement.md) · [`Q-MONSURF-1 closure`](docs/briefs/closures/Q-MONSURF-1-closure-resolved.md)
- **CFD data-estate class-wide delete** — trigger-dated; blocked on T1 (F3 FUTURES_LOCK) + substrate Phase-6 confirm. [`CFD estate ADR`](docs/adr/2026-07-11-ops-cfd-estate-retirement.md) · [gate audit](docs/notes/audits/2026-07-17_gate_cfd-estate-classwide-delete.md)
- **Mechanism-sourcing radar** — on-demand cadence; 08-08/11-08 = progress/idle checkpoints; idle guard 2026-11-08. [`harvest §2`](docs/methodology/strategy_harvest.md)
- **Deep-iteration lane — §4(c) supply-side audit DELIVERED 2026-08-23 (`AMBIGUOUS`); its named nearest supply lead, `MNQFLOW-1-DEPTH`, is now `HOLD` (operator, value-uncertain — not cost-blocked, not declined).** The audit ([note](docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md)) named `MNQFLOW-1-DEPTH` (order-flow) as the nearest reachable supply lead, "one sign-off away." Two independent, non-overlapping 30-day systematic samples of its own frozen 255-trigger population were each P0-priced and each blocked (original **$148.04**, redraw **$154.73**, both vs the **$125.00** ceiling) — reading as structural (~$150 true cost, not $125), not unlucky draws. Presented with three named forward paths (raise the ceiling to ≈$160–175; a smaller-N fresh pre-registration; decline), the **operator held**: *"I am not ruling it out but I do not know if it is worth the spend"* — recorded verbatim in [`PREREG_S2B.md`](lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md)'s own Status block. No forced re-test date; naturally revisited at 2026-11-08 alongside the lane's own broader supply question, or sooner at the operator's initiative. $0 spent across both pricing attempts. The free alternate (a published MOC-imbalance cohort δ) and the blind channel (unsourced, 1/3) remain the estate's other two named supply routes — **neither requires any further action on the order-flow route to stay available.** Background: DL-2's construction retired for M6A (geometric-feasibility diagnostic, median R=1.0/0.687, 85–97% of fired trades never reach 1R); DL-1 is a separate candidate-level failure — no shared template defect. [`PREREG.md`§9.2](lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG.md) · [`charter`](docs/adr/2026-08-16-deep-iteration-lane-charter.md)
### 2026-08-08 — DISCHARGED

> ✅ **The quarterly vehicle ran 2026-08-08.** Verdicts, the full rider partition
> (2 discharged / 37 owed / 3 moot / 5 unfalsifiable of 47), the unfalsifiable-check census, and
> every named follow-up now live in
> [`2026-08-08-quarterly-audit.md`](docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md).
> The former ~90-line rider blockquote is deleted per the retention test — it restated obligations
> the audit note now owns. **Operator rulings still open** are carried as queue rows, not here.

### 2026-08-24 (Monday)

- **Disaster-stop Phase 0a — attended real-account SIM.** Operator will attend and run the
  `stop_loss=` / `closeposition` observation on the real (non-paper) Tradeify eval account this
  session (committed 2026-08-23). Only a recorded PASS unlocks Phase 1 (`sl=` wiring into
  `ops/c1_rail/c1_rail_listener.py`); the prior unattended attempt came back BLOCKED. [`plan`](docs/superpowers/plans/2026-08-23-disaster-stop-phase-0-1-implementation.md) · [`BLOCKED note`](docs/notes/rail_build/2026-08-23-disaster-stop-phase-0.md)

### 2026-10-11 (approx.)

- **prop_envelope §4 overlay 90-day re-verify** — rows verified 2026-07-13; stale after ~2026-10-11. [`prop_envelope`](ops/prop_envelope_default.md) · [`ratification ADR`](docs/adr/2026-07-13-prop-envelope-v1-ratification.md)

### 2026-11-08

- **ADR ceremony-tiering §Falsifier review** — first quarterly programme audit after 2026-08-08; check light share ≥⅕ and dated omitted-apparatus incidents (incl. 2026-08-14 candidate: implied-SR light records). Count 1-vs-2 is operator/audit. [`ADR addendum`](docs/adr/2026-08-08-adr-ceremony-tiering.md)
- **GRAND-tier ADR §4 scheduled re-read** — H already satisfied 2026-08-09 (19 ratified differences; tier load-bearing, sunset did **not** arm). This slate is the first scheduled re-check, not a sunset. [`ADR addendum`](docs/adr/2026-08-09-grand-tier-quintessentials-binding.md) · [`closure`](docs/briefs/closures/GSUB-1-closure-resolved-loadbearing.md)
- **GSUB-1 PARK expiries (5)** — b1 Aegis→6J · b3 ORB-MNQ line · b5 Q-FUNDPOL-1 · b6 Q-NAS-ECR-1 · c3 Q-TOM-SPX-1. Each converts to SUBTRACT absent explicit operator renewal (ADR §2.3). b2 (Striker-MYM) and c1 (Q-XMEM-1) already resolved to `SUBTRACT` early via GSUB-2 (2026-08-19, ~80 days ahead of this expiry); b7 (ICT line) also already resolved to `SUBTRACT` — its own named re-entry step had already fired 2026-08-04, ~96 days ahead of this expiry, corrected this session (2026-08-20) — all three dropped from this row, not still pending. [`docs/pursuits/`](docs/pursuits/)
- **Guardian-MGC (R7) transfer lane — SUBTRACT / DEAD(N-SURV) 2026-08-11** — exploratory N-SURV FAIL (full 42.2% / H1 72.4% / H2 16.5% bust vs ≤3.0%); margin-decisive; retroactive cell PREREG + typed closure filed. Re-entry = new mechanism evidence (not param retune). [`b8`](docs/pursuits/b8-guardian-mgc-transfer-lane.md) · [`closure`](docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)
- **Prop-portfolio §4 primary falsifier (HARD)** — ≥1 candidate clears bust ceiling on ≥2 of 4 FRIENDLY firms; else demote program to research-only. Status undischarged (2026-07-22 withdrawal). [`four-firms ADR §4`](docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md) · [`withdrawal ADR`](docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md)
- **Mechanism-boundaries ADR §4** — clauses 2-A / 2-B / 2-C first check. [`ADR`](docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md)
- **Harvest-intake §4 doctrine falsifier + idle guard** — limb 1 still 0-of-2; limb 2 `Accepted` (R10 GO); pin marked `no`; post-mark count 0/2 (not fired). Idle = zero screen-PASS seeds beyond D5. [`harvest ADR §4`](docs/adr/2026-07-15-external-mechanism-harvest-intake.md)
- **Regime-monitor successor §6 gate** — if no live fill by 11-08, gap is ≥3 months; re-raise as standing-unfalsifiable in that programme audit. [`decompound ADR`](docs/adr/2026-06-07-decompound-remc-hold.md)
- **Blind-channel §4 reading** — sourced-vs-empty (`AMBIGUOUS-HOLD` if still unsourced); disclose pre-G0 count and whether N fired; analogue-modality ruling re-test (inert if no analogue manifest). Owner: [channel ADR](docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) · [analogue ruling](docs/adr/2026-08-15-analogue-modality-route-ruling.md)
