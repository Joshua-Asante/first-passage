# Open-Question Roster (Q-roster)

Created 2026-06-13 as part of the Notion Phase-2 migration (`docs/adr/2026-06-12-notion-surface-retirement.md` §2.5).
The Notion Command Center previously held the live Q-roster; that surface is retired (read-only). This file is the
repo home for **open / dormant** investigation questions — one home per open Q. Closed questions live in
[`docs/briefs/closures/`](closures/) (hot). Pre-prune / restored bodies are mostly
**absent on this public clone** — retrieve via `git show pre-prune-2026-08-08:docs/ltm/briefs/…`
or the private archive / `git log --follow` ([`docs/ltm/README.md`](../ltm/README.md)).
They are not re-listed in Open.

**Convention:** each open Q has exactly one canonical repo home (the row's "Home"). When a Q closes, file the
closure under `docs/briefs/closures/` and delete its Open row (Recently-closed may keep a one-line pointer).

## Open

| Q | Status | Home (canonical) | Next action |
|---|---|---|---|
| **Q-SIGID-1** — measured live↔backtest signal-identity gap from mid-bar `alert()`/`strategy.entry` on c1 venue editions; architectures that close it (locked-axis, not EQ) | **`OPEN`** 2026-07-28 — cheap falsifier: 07-28 MNQ bar is a phantom (`longSignal` mid-true / close-false on `body_ok`); offline phantoms ~0.7× confirmed signals; Fri §2b clean re-measure owed | [`Q-SIGID-1-intra-bar-signal-identity.md`](Q-SIGID-1-intra-bar-signal-identity.md) · [pre-reg](pre-registration/Q-SIGID-1-verdict-preregistration.md) · [RESULTS](../../lab/analysis/c1/c1_signal_identity_2026-07-28/RESULTS.md) | Ruled host is **built** (S2b, `emit_enabled=false`). Offline limb MNQ 0.68 / MYM 0.70 stands. §2b re-measure needs no fill/order/arming. Pine edit only under separate operator GO. |
| **Q-FILLTAX-1** — TV fill-optimism gap + Pine↔Python / engine↔TV parity | **`OPEN`** — V2 Phase-0 scaffold `CODE_LANDED` 2026-08-07 ($0 under S1 incumbent); V1 disposition follows S1 (Tradeify geometry); Gate RESOLVED needs first family TV anchor | [`Q-FILLTAX-1-fill-realism-and-parity-scoping.md`](Q-FILLTAX-1-fill-realism-and-parity-scoping.md) · [`parity_gen2`](../../lab/analysis/c1/parity_gen2_2026-08/) · [`RESULTS`](../../lab/analysis/c1/parity_gen2_2026-08/RESULTS.md) | Operator: first family same-feed CME TV anchor → Gen-2 ADMIT. No post-hoc band tuning. Mutation battery (Phase 1) still owed. |

Ten of the eleven 2026-08-18 assumption-sweep Qs are now closed (Q-M1WIRE-1 `FALSIFIED` 2026-08-21; Q-TRADECAP-1 `RESOLVED`, Q-SIZECOMP-1 `RESOLVED`, Q-STATVALID-1 `FALSIFIED`, Q-INTAKEGOV-1 `AMBIGUOUS-HOLD`, Q-S5CAP-1 `RESOLVED`, Q-FIRMEOD-1 `FALSIFIED`, Q-DATAFIDELITY-1 `FALSIFIED`, Q-PUBTRANS-1 `FALSIFIED`, Q-CALLBOUND-1 `AMBIGUOUS-HOLD`, the latter nine all 2026-08-23) — see `## Recently closed` below for each. Origin: [`docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`](../notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md) (25 verified-unexamined findings; these Qs combine 22 of them — 2 stay audit-note-resident: D5 Notice-phase 5-tool coverage, D10 D-S-A canon staleness routed to the next quarterly methodology audit instead (D1 MEMORY reach closed 2026-08-23, P2 Approach A)).

## Dormant (no current session home; resurface before assuming dead)

| Q | Status | Home | Note |
|---|---|---|---|
| ~~**Q-FUNDPOL-1** — funded-phase policy inheritance~~ → **DORMANT 2026-08-04** (§6 gate retired — eval pass converting cannot occur; Select-Flex thresholds non-transferable). §8 pre-reg (`d0200a4`, **K frozen = 4**) + P1/P2 discharges **unspent**; §1–§5 analysis retained as worked method. **Do not build** §9-C1 / `PAYOUT_MIN → 0`. | measurement / method record | [`Q-FUNDPOL-1-funded-phase-policy-inheritance.md`](Q-FUNDPOL-1-funded-phase-policy-inheritance.md) · pre-reg [`Q-FUNDPOL-1-verdict-preregistration.md`](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md) · [`docs/pursuits/b5-q-fundpol-1.md`](../pursuits/b5-q-fundpol-1.md) | **RENEWED 2026-08-16** — corrected wake condition (the F3-successor-venue clause is now unreachable per S1's no-migration ruling): re-enter when Q-POLFRONT-1 reads positive on funded-relevant cells OR a candidate reaches funded-phase modeling. New expiry **2027-02-08**. |

## Recently closed (cross-reference; not open)

One line per the file's own convention (see above) — verdict, date, one-clause finding, links out to
the closure for detail. All are $0/K=0 unless noted.

- **Q-TRADECAP-2** — per-trade loss bound election — **`RESOLVED` 2026-08-24**, frozen ID 2 (observe-only), no tripwire wired. [`closure`](closures/Q-TRADECAP-2-closure-resolved.md) · [`elect-2`](../adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md)
- **Q-TOM-SPX-1** — SPX500 turn-of-month existence — **`DEAD` 2026-08-23**, Layer-A `RESOLVED-ABSENT` on Pepperstone. [`closure`](closures/Q-TOM-SPX-1-closure-dead.md)
- **Q-MONSURF-1** — venue-free monitoring-surface triage (M-A/M-B/M-C) — **`RESOLVED` 2026-08-23**, M-B registration-ready (gated on F3 only), M-C fill-gated, M-A elective. [`closure`](closures/Q-MONSURF-1-closure-resolved.md)
- **Q-TRADECAP-1** — per-trade dollar-loss bound, predecessor — **`RESOLVED` 2026-08-23**, absent on all four checked limbs; successor [`Q-TRADECAP-2`](Q-TRADECAP-2-per-trade-bound-election.md). [`closure`](closures/Q-TRADECAP-1-closure-resolved.md)
- **Q-STATVALID-1** — DSR/multiplicity rigor on the MC engine's own resampling + constant search — **`FALSIFIED` 2026-08-23**, Limb C fires both grids; Limb B AMBIGUOUS (panel unrecoverable). [`closure`](closures/Q-STATVALID-1-closure-falsified.md)
- **Q-SIZECOMP-1** — does the live sizing host compose lifecycle × `DD_SCALE` × Call-4 beta-death as documented — **`RESOLVED` 2026-08-23**, it doesn't compose beta-death at all; test-coverage gap named. [`closure`](closures/Q-SIZECOMP-1-closure-resolved.md)
- **Q-S5CAP-1** — does S5's capped concurrency hold system-wide or only per-packet — **`RESOLVED` 2026-08-23**, holds; mechanism gap only, zero real S5 promotions on record. [`closure`](closures/Q-S5CAP-1-closure-resolved.md)
- **Q-FIRMEOD-1** — Tradeify EOD-clock defect applied to the 7 Bulenox/BluSky trailing tiers — **`FALSIFIED` 2026-08-23**, CLOCK fails on all 7; bust figures stay EOD-lower-bound pending a successor re-run. [`closure`](closures/Q-FIRMEOD-1-closure-falsified.md)
- **Q-DATAFIDELITY-1** — do the stated data-integrity nets cover TV price fidelity + feed-equivalence + manifest scope — **`FALSIFIED` 2026-08-23**, both limbs fire (2/9 sampled dates exceed tolerance; 0 documented scope caveat). [`closure`](closures/Q-DATAFIDELITY-1-closure-falsified.md)
- **Q-INTAKEGOV-1** — does discovery-intake/rejected-registry governance tooling cover what it's relied on for — **`AMBIGUOUS-HOLD` 2026-08-23**, split: dedup-corpus gap confirmed real, no re-examination mechanism for a standing REJECTED verdict. [`closure`](closures/Q-INTAKEGOV-1-closure-ambiguous-hold.md)
- **Q-CALLBOUND-1** — lifecycle Call-system automation-boundary symmetry + completeness — **`AMBIGUOUS-HOLD` 2026-08-23**, symmetry clean, completeness inconclusive. [`closure`](closures/Q-CALLBOUND-1-closure-ambiguous-hold.md)
- **Q-PUBTRANS-1** — did the 2026-08-14 public-visibility transition complete cleanly (ADR
  Status stale, residual-disclosure risk untested, sentinel queue orphaned; B5+D8+D9) —
  **`FALSIFIED` 2026-08-23** — H-PUBTRANS rejected outright: Limb D8 concretely fails —
  Guardian Gold's ATR multiplier (1.55×), grace-stop multiplier (2.0×), and grace-bar window
  are stated in cleartext at `docs/methodology/1r_estimation.md:77,379`, a file absent from the
  admitting ADR's own downstream-artifact inventory and missed by the 2026-08-14 sweep — a live
  leak of Pine-only-locked strategy detail on the now-public repo, still present. ⚠ **Not
  remediated by this closure — flagged for immediate operator attention, see chat.** Limb B5
  (withheld literal account/$ grep) and Limb D9 (pre-transition sentinel-queue disposition —
  corrected count 12, not 11) remain individually open pending operator input; D9's own premise
  that it "needs private-archive access" is shown to be wrong (the archive is an already-fetched
  local git remote).
  [`closure`](closures/Q-PUBTRANS-1-closure-falsified.md) ·
  [`brief`](Q-PUBTRANS-1-public-transition-completeness.md) ·
  [`pre-reg`](pre-registration/Q-PUBTRANS-1-verdict-preregistration.md).
- **Q-M1WIRE-1** — does M1 arming interlock verify what its acceptance package claims — **`FALSIFIED` 2026-08-21**, two limbs confirmed missing; rail stays disarmed, M1 stays not-`RESOLVED`. [`closure`](closures/Q-M1WIRE-1-closure-falsified.md)
- **Q-GATESTACK-1** — does anything on GitHub require the gate stack to pass before `main` — **`FALSIFIED` 2026-08-19**, `main` was unprotected; doc-correction executed same turn. [`closure`](closures/Q-GATESTACK-1-closure-falsified.md)
- **Q-NSURV-2** — magnitude-resampling second-uncertainty-layer for N-SURV — **`RESOLVED` 2026-08-20**, wrapper reproduces both known candidates' headline estimates within 2pp. [`closure`](closures/Q-NSURV-2-closure-resolved.md) · [`ADR`](../adr/2026-08-20-nsurv-magnitude-resampling-disclosure.md)
- **Q-ORBSURV-1** — cushion sizing vs the frozen survivor-scoring gate at untested configs — **`FALSIFIED` 2026-08-20**, gate-clear is k-dependent, not robust; does not license unpark. [`closure`](closures/Q-ORBSURV-1-closure-falsified.md)
- **Q-NSURV-1** — is the N-SURV single-history magnitude blindspot general or idiosyncratic to c1 — **`RESOLVED` 2026-08-20**, confirmed general on a second candidate (different axis each). [`closure`](closures/Q-NSURV-1-closure-resolved.md)
- **Q-ORBCUSH-1** — trailing edge/cost classifier for ORB-MNQ-1's 2021-09-28 regime break — **`FALSIFIED` 2026-08-20**, break stays real and mechanistically unexplained; bust-elimination unaffected. [`closure`](closures/Q-ORBCUSH-1-closure-falsified.md)
- **Q-XMEM-1** — per-surface agent-memory invisibility; Mem0 sidecar pilot — **`CLOSED` / GRAND-tier `SUBTRACT` 2026-08-19**. [`closure`](closures/Q-XMEM-1-closure-subtract.md)
- **Q-TRAINKILL-3** — Block F vs Block A winner between NEG and DEP — **`AMBIGUOUS-HOLD` 2026-08-18**, split; census STOP. [`closure`](closures/Q-TRAINKILL-3-closure-ambiguous-hold.md)
- **Q-TRAINKILL-2** — bounded recovery / alt DGP fit — **`AMBIGUOUS-HOLD` 2026-08-18**, extremes still disagree. [`closure`](closures/Q-TRAINKILL-2-closure-ambiguous-hold.md)
- **Q-TRAINKILL-1** — explore/train kill record vs zero edge — **`AMBIGUOUS-HOLD` 2026-08-18**, BOUNDED extremes disagree. [`closure`](closures/Q-TRAINKILL-1-closure-ambiguous-hold.md)
- **Q-EXPR-1** — what explains the regularity→expression orphaning — **`RESOLVED` 2026-08-18**, horizon-mismatch (4/4). [`closure`](closures/Q-EXPR-1-closure-resolved.md)
- **Q-CONDVAL-1** — does the CL range-state lift buy anything in R terms — **`FALSIFIED` 2026-08-18**, below the frozen threshold. [`closure`](closures/Q-CONDVAL-1-closure-falsified.md)
- **Q-POLFRONT-1** — policy-augmented seed-target frontier — **`RESOLVED-QUANTIFIED` 2026-08-16**, 5.1× headline. ⚠ Does not survive intraday-honest remeasure (fork 2026-08-17/20) — see closure for the load-bearing caveat. [`closure`](closures/Q-POLFRONT-1-closure-resolved-quantified.md)
- **Q-EVALSEQ-1** — within-eval front-load schedule — **`FALSIFIED` 2026-08-16**; surviving finding (cushion sizing cuts bust) routed to Q-POLFRONT-1. [`closure`](closures/Q-EVALSEQ-1-closure-falsified.md)
- **Q-CAPBAND-1** — has `CAP = 1.0` ever excluded a surviving axis — **`RESOLVED` 2026-08-15**, both band axes fail on other gates; Cap cost nothing on named axes. [`closure`](closures/Q-CAPBAND-1-closure-resolved.md)
- **Q-BUSTGATE-2** — does updated external data move the Part-A eval bust ceiling — **`RESOLVED` 2026-08-15**, ceiling reconfirmed byte-unedited. [`closure`](closures/Q-BUSTGATE-2-closure-resolved.md)
- **Q-CAPFLOW-1** — OR-window aggressor flow → ORB trade R (Cap-spend) — **`FALSIFIED` 2026-08-14**, CI95 includes 0; Cap held. [`closure`](closures/Q-CAPFLOW-1-closure-falsified.md)
- **Q-TNEC-CON-5** — impulse→pullback→VWAP-reclaim — **`AMBIGUOUS-HOLD` → Branch A STOP 2026-08-12**, dense-1m lane paused. [`closure`](closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
- **Q-TNEC-CON-4** — PDH/PDL RTH with-break — **`AMBIGUOUS-HOLD` 2026-08-11**; U1 override re-test 2026-08-20 confirmed the same verdict, reverted to paused. [`closure`](closures/Q-TNEC-CON-4-closure-ambiguous-hold.md)
- **Q-TNEC-CON-3** — HTF-native 5m compression→expansion break — **`AMBIGUOUS-HOLD` 2026-08-10**, lane paused. [`closure`](closures/Q-TNEC-CON-3-closure-ambiguous-hold.md)
- **Q-TNEC-CON-2** — dense-1m compression→expansion with-break @ G=10 — **`AMBIGUOUS-HOLD` non-promotable 2026-08-10**, cost eats the gross edge. [`closure`](closures/Q-TNEC-CON-2-closure-ambiguous-hold.md)
- **GSUB-1** — first GRAND-Subtract pass over the pursuit portfolio — **`RESOLVED-LOADBEARING` 2026-08-09**, 19 ratified dispositions of a 37-row inventory. [`closure`](closures/GSUB-1-closure-resolved-loadbearing.md)
- **Q-TVCOV-1** — TV intraday bar-coverage census — **closed 2026-08-09** (verdicts landed 2026-07-13: FALSIFIED for 6J+MNQ, AMBIGUOUS MYM). [`closure`](closures/Q-TVCOV-1-closure-falsified.md)
- **Q-OFCHAN-1** — flicker-filtered TBBO L1 imbalance → 60s mid — **Stage-G VOID-COVERAGE 2026-08-07**, 7.36% coverage; STOP this catalogue. [`closure`](closures/Q-OFCHAN-1-closure-void-coverage.md)
- **Q-TXG-1** — transfer/expression lane — **CLOSED — FALSIFIED-at-walls 2026-08-12**. [`lane closure`](closures/Q-TXG-1-closure-falsified-at-walls.md)
- **Q-TXG-1 cell striker_nas100×MYM** — **DEAD(cost) 2026-08-12**. [`closure`](closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md)
- **Q-TXG-1 cell striker×MNQ** — **DEAD(N-SURV) 2026-08-12**, cost PASS but ~98% bust all partitions. [`closure`](closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md)
- **Q-MNQSEL-1** — selection-value ceiling on causal restart clocks — **CLOSED-FALSIFIED 2026-08-07**. [`closure`](closures/Q-MNQSEL-1-closure-falsified.md)
- **Q-R2VBUCK-1** — volume-bucket aggressor imbalance → 60s mid — **Stage-G FALSIFIED 2026-08-08**, CI includes 0. [`closure`](closures/Q-R2VBUCK-1-closure-falsified.md)
- **Q-MNQDTL-CON-1** — EM construct on dense RTH 1m opens — **CLOSED FALSIFIED 2026-08-09**. [`closure`](closures/Q-MNQDTL-CON-1-closure-falsified.md)


These had Notion tracker cards that are now retired. Hot closures live in `docs/briefs/closures/`. Older restored records are **not** on this public clone — retrieve via `git show` / private archive ([`docs/ltm/README.md`](../ltm/README.md)):

- **Q-R2FLOW-1** — clock-minute net signed aggressor → 60s mid — **Stage-G FALSIFIED 2026-08-08**, CI includes 0. [`closure`](closures/Q-R2FLOW-1-closure-falsified.md)
- **Q-MNQSEL-2** — dense RTH 1m selection ceiling at G=10 — **RESOLVED (C4) 2026-08-08**, construct ITERATE. [`closure`](closures/Q-MNQSEL-2-closure-resolved.md)
- **Q-R2AGRUN-1** — aggressor-run trade-count → 60s mid — **AMBIGUOUS-HOLD (magnitude) 2026-08-08**, operator non-promotable STOP. [`closure`](closures/Q-R2AGRUN-1-closure-ambiguous-hold.md)
- **Q-CAPA-1** — Cap-seat Route A forward tripwire vs hold Cap — **RESOLVED 2026-08-06**, Cap seat spent. [`closure`](closures/Q-CAPA-1-closure-resolved.md)
- **Q-RAIL-1** — c1 execution-path scoping (F1–F5, GO/NO-GO) — **RESOLVED 2026-07-17**, Tradeify Select recommended, §8 ceiling $700 signed. ⚠ §1's discharge claim WITHDRAWN 2026-07-22 — see [`ADR`](../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md). [`closure`](closures/Q-RAIL-1-closure-resolved.md)
- **Q-PYRPARITY-1** — WATCH-1 pyramid-proportionality on TV — **FALSIFIED-NONPROPORTIONAL 2026-07-17**. [`closure`](closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md)
- **Q-INVENTORY-1** — fundable-inventory zero — **FALSIFIED 2026-07-17**, 0 admissible seeds. [`closure`](closures/Q-INVENTORY-1-closure-falsified.md)
- **Q-BUSTGATE-1** — Part-A eval bust ceiling basis — **FALSIFIED 2026-07-23**; live rung stays WATCH-1 0.50×. [`closure`](closures/Q-BUSTGATE-1-closure-falsified.md)
- **Q-KBUDGET-HARVEST-1** — bounded Tier-1/Tier-2 literature harvest — **RESOLVED 2026-07-16**. [`closure`](closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md)
- **Q-GEOFIT-1** — trailing-DD funding-envelope map — **AMBIGUOUS-PARAMETERIZATION 2026-07-25**. [`closure`](closures/Q-GEOFIT-1-closure-ambiguous-parameterization.md)
- **Q-JOINT-TAIL-1** — cross-strategy daily co-failure — **BLOCKED-RETIRED 2026-05-27** (temporally diversified at day-of-week level). Succeeded by Q-JOINT-TAIL-WEEKLY. Closure absent here — retrieve `git show pre-prune-2026-08-08:docs/ltm/briefs/Q-JOINT-TAIL-1-closure.md` (private archive only, see §CLAUDE.md caveat).
- **Q-JOINT-TAIL-WEEKLY** — cross-strategy joint-tail at week-block resolution — **RETIRED 2026-07-14** (panel-shape assumption failed at the pre-registered sanity gate). [`closure`](closures/Q-JOINT-TAIL-WEEKLY-closure-retired.md)
- **Q-PRECOND-1** — mechanism preconditions — **FALSIFIED 2026-05-21** (precondition-as-retirement-rule too sensitive on the long-DD window). Closure absent here — same private-archive retrieval as above.
- **Q-REGIME-RATEVOL-1** — exogenous rate-vol blind-spot complement — **FALSIFIED 2026-06-16** (anti-aligned with the regime). Closure absent here. Parent Q-REGIME-STRESS-1.
- **Q-REGIME-AEGIS-1** — USDJPY trend-persistence vs Aegis win/loss regime — **FALSIFIED 2026-06-16** (chance-level AUC); 2nd consecutive FALSIFIED on the blind-spot-detector thread → INQHIORI tail-exhaustion, no 3rd detector. Closure absent here. Parent Q-REGIME-STRESS-1.
- **Q-ICT-SWEEPFVG-1** — PHAROS sweep→FVG→draw on US500 15m — **FALSIFIED 2026-06-17** (real direction, but concentrated in 3 trades — not robust). Closure absent here; consolidated ledger [`ops/instruments/SPX500.md`](../../ops/instruments/SPX500.md).
- Q-SWAP-1/2/3/4, Q-REGIME-1/2, Q-REGIME-TIME-1, Q-DDTRIG-1, Q-FEED-1, Q-PARITY-1 — retrieve under `docs/ltm/briefs/` (private archive only; Q-FEED-1 restored here as `Q-FEED-1-dukascopy-tv-feed-divergence.md`).
- **Q-ICT-CASCADE-1** — five-layer ICT cascade on US500 — **CLOSED 2026-06-19** (`INSUFFICIENT-N`). [`closure`](closures/Q-ICT-CASCADE-1-closure-insufficient-n.md)
- **Q-USOIL-1** — USOIL regime-capture / Silver §9 counterbalance — **CLOSED / SUBTRACT 2026-08-09** (GSUB-1 b4). [`closure`](closures/Q-USOIL-1-closure-subtract.md)

> Forward triggers (methodology 90-day review 2026-07-29; 08-08 packet — C2→C0 revert check **retired** 2026-07-22 per rescope ADR D2 addendum) live in `STATE.md` §Scheduled forward triggers / pointer log, not here. Full living-board sync of retired lines is a deferred doc-drift session.
