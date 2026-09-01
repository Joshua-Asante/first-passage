# Six-lead pursuit plan — Koijen axis-2 survivors

**Status:** Phase 0 EXECUTED · P1-CF/P2-CF FAIL · P3 GO executed 2026-08-17 and **CLOSED
(venue SCREEN-FAIL)** · P4 un-HOLD'd 2026-08-20 → route memo, dry-run + concentration check same
day, disposition **HOLD** throughout (data-sourcing question, evidence now leaning against a bare
trade-count construction, not a kill) · P5 un-HOLD'd 2026-08-20 → access probe, disposition
**`UNSCREENABLE`**, closed · OpenAlex channel addendum landed (17d) ·
**this document is the claim manifest for the program** — the orchestrator session is its
only writer. Title still says "six" pending a forward correction (L3=L6 same paper; five
distinct programs).
**Objective:** carry the — **five, corrected from six this session, see §13** —
[Koijen axis-2 OpenAlex-substitute](../../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md)
leads from screen-level survivors to either a priced Databento extension decision or a registry
kill, through harvest intake, against the **2026-11-08** clock (four-firms §4 + harvest limb-1
idle guard + limb-2 exposure).
**Layering:** single CC orchestrator session for judgment/doctrine/K-$/data-route calls; Cursor
dispatch only for Phase-3 engines that clear the ≥1hr/≥3-file surface-allocation test (never
Pine, never locked surfaces).

---

## §0 Rule 0 / grounding reads (this session, HEAD `5d8bf59`, 2026-08-17)

Verified before this plan was drafted, not reconstructed after:

| Claim in the plan | Verified against | Result |
|---|---|---|
| Rates sleeve venue-dead | [`core/firm_rules.py`](../../../core/firm_rules.py) ~L259 | "US TREASURIES (ZB/ZN/ZF/ZT/UB) ARE NOT TRADABLE HERE" (article 10468222); sole rates products are EUREX bonds |
| 2026-06-30 Micro10Y/2YY MR rejection | [`docs/rejected_candidates.md`](../../rejected_candidates.md) L428 | Confirmed — chop-native 5th-leg sweep, era/tail-wall kill |
| OHLCV raised bar | [`docs/rejected_candidates.md`](../../rejected_candidates.md) L24 | `index-intraday-ohlcv-directional-timing-2026-07-21`, tier=always |
| §4a hedging sign-constraint | [`core/firm_rules.py`](../../../core/firm_rules.py) comment block | Equity Index Product Group = ES/MES/NQ/MNQ/YM/MYM/RTY/M2K/EMD/NKD + EUREX index; opposing directions prohibited within-group, one account or across |
| TNEC N-SHAPE definition | [`docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md`](../../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) L11 | EM3 independence + hard-stop integrity + EM5 session/slot legality (flat-16:00-ET-inside-16:45-print · micro-expressible · §4a sign constraint · S7 occupancy) |
| MSL slate-2 design box (why it can't fit these leads) | [`docs/adr/2026-08-13-msl-slate-2-design-box.md`](../../adr/2026-08-13-msl-slate-2-design-box.md) | `rr`∈[2,3], WR 0.30–0.42, R at bust≤3.0% diffusion frontier, hard-stop mandatory, k=1, no pyramiding — a daily hold-to-close reversal shape does not fit this box |
| M6A `FLAG-COSTBIND` | [`ops/instruments/M6A.md`](../../../ops/instruments/M6A.md) | Confirmed: Stage-1 Currencies SURVIVOR under FLAG-COSTBIND; cost-tax 0.0902 binds before the 0.0891 pooled-panel floor; Stage-2 ex-FOMC flips COST→POWER |
| MGC instrument state | [`ops/instruments/MGC.md`](../../../ops/instruments/MGC.md) | RE-ENTERED, class-attested, not elected; one dated cell (`event-window-reversal` DEAD, unrelated mechanism); no binding bar against a hold-to-close reversal shape |
| `scripts/instrument_profiles.py cell <SYM> <mechanism-id>` | read in full | Data-independent — reads only `ops/instruments/*.md` + committed `MECHANISMS.md`; safe to run in this worktree without vendor panels |
| On-hand CME panels in **this worktree** | `ls core/data/tv_exports/cme/` | **Only `SHA256SUMS` present — no panel bytes in this worktree.** Matches the plan's own Phase-3 note ("worktrees lack gitignored vendor data, even locally"). Dedup/venue/cost-screen work (data-independent) can proceed here; any actual CSV read (Phase 1 cheap falsifiers) needs `-Copy`/`FP_DATA_ROOT` staging from the primary checkout or a fresh pull |
| GC.FUT deep-history cache | `lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/` | Confirmed real: `CAMPAIGN_ID = "DL1-MGC-ORC"`, `GC.FUT` parent TRAIN 2010-06-06→2019-01-01 (2,168 CME sessions), `MGC.FUT` reserved as CONFIRM/OOS. This is the deep-lane cache the plan proposes reusing for L1/L3's gold cell — same bytes, second consumer, no re-pull |
| 2026-08-17 Koijen axis-2 STATE decision line | [`STATE.md`](../../../STATE.md) L64–73 | Matches SOURCES_LOG exactly: 296→234→230→17→7/6 funnel, $0/K=0, no candidate admitted |

---

## §1 Channel election (fixed up front)

All six leads route through **harvest intake (external-mechanism)**, not MSL — the MSL slate-2
design box (`rr`∈[2,3], WR 0.30–0.42, hold-through-intraday) cannot fit a daily-reversal shape and
would kill every one of them on arrival (verified §0). Stop authority is therefore **TNEC
N-SHAPE** (hard-stop integrity + EM5 session legality, verified §0), which a hold-to-close
construct with a hard-stop overlay satisfies by construction.

## §2 Priority order (recomputed after venue/cost corrections)

| # | Lead | Why this rank | What the venue/cost pass changed |
|---|---|---|---|
| P1 | **L3=L6** overnight-reversal — **RESOLVED SAME PAPER** (not "merged pending overlap"): SOURCES_LOG rows 3 & 6 are the 2015 and 2022 drafts of one Della Corte/Kosowski(+Liu)/Wang paper, same SSRN abstract `2730304` — see [SOURCES_LOG addendum](../../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md#addendum-2026-08-17--3-and-6-are-the-same-paper-not-two-independent-leads-count-corrects-65). Carry the 2022 draft (4 authors, richer robustness) forward as the authoritative version | Concrete WHO, testable today at $0 on panels the primary checkout holds | Effective universe shrank hard: rates sleeve venue-dead (§0); index sleeve blocked by the OHLCV raised bar + §4a sign-constraint; MCL pre-killed by arithmetic — **verified this session**: MCL's own measured cost_bp 5.3423 (Stage-0 2023 median, `ops/instruments/MCL.md` C1) × 2 (generous bar) = 10.68bp ≈ the "10.7bp" figure, vs the paper's commodities leg 0.04%/day (t=6.76) = 4bp/day → pre-killed; M6A marginal (`FLAG-COSTBIND`, §0). Informative cells ≈ MGC (+6J as FX signal panel) — both on hand at the primary checkout; 6J carries no cost_hurdle on its ledger yet (needs fresh measurement) |
| P2 | **L1** index-flow daily reversal — row 1, Da/Tang/Tao/Yang | Same $0 panels, commodity-native | Must test the venue-expressible slice (18:00–reopen/open → close next day, paying the decomposed RT count), not raw close-to-close autocorrelation — raw existence can pass while the expressible component nets negative |
| P3 | **L5** curve-slope momentum — row 5, Bianchi/Fan/Miffre/Zhang | Real reported edge, weakest WHO | **GO executed 2026-08-17 — sleeve CLOSED (venue SCREEN-FAIL).** Dry-run $0 on bars; paper S-strategy is a calendar spread, already illegal at this firm. Dedup vs USOIL-carry: DISTINGUISHABLE, not ADMIT. See [`P3_DRYRUN`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md) |
| P4 | **L2** dealer-gamma EOD transplant — row 2, delta-hedging demand | Real mechanism, uncertain data route | Governed by the Q-ORB-GEX-1 rejection (2026-06-25, edge collapsed to a realized-vol proxy) + exogenous-conditioning orthogonality priors, not the OHLCV bar. Phase 1 = route memo only |
| P5 | **L4** mutual-fund overweight — row 4, Chen/Chen/Cohen | Expected cheap kill | Access probe on the holdings-data real-time lag (13F/N-Q, ~45-day disclosure lag per SOURCES_LOG); likely UNSCREENABLE |

**L-number ↔ SOURCES_LOG row map** (for future readers — this table is new index, not a
retelling of the evidence in [`SOURCES_LOG.md`](../../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md)):
L1=row 1 · L2=row 2 · L3=L6=row 3/row 6 (**same paper, confirmed this session — see §Phase 0
findings below**) · L4=row 4 · L5=row 5. **Five distinct research programs, not six** — the
2026-08-17 STATE.md decision line and this plan's own title still say "six leads" pending a
forward correction line (see §13).

---

## §3 Phase 0 — Consolidation & triage ($0 · K=0 · all CC-side, ~1 session)

**Execution status: items 0.1–0.7 DONE this session** (operator approved the plan shape and asked
to proceed with Phase 0 execution). Item 0.8 (operator marks packet) is assembled at §13 below —
its contents are recommendations for operator sign-off, not yet operator-marked.

| # | Item | Status | Note |
|---|---|---|---|
| 0.1 | Fetch origin + verify merged SOURCES_LOG content (verify-content-not-path) | **DONE** | `git fetch origin` clean, HEAD `5d8bf59` = merge of PR #31; SOURCES_LOG read in full, matches STATE.md decision line |
| 0.2 | L3/L6 overlap resolution — read both PDFs | **DONE — RESOLVED SAME PAPER** | Not "one research program," the literal same paper across a 2015→2022 redraft (same SSRN abstract `2730304`, explicit self-citation of the title change, additive author list). Full evidence: [SOURCES_LOG addendum](../../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md#addendum-2026-08-17--3-and-6-are-the-same-paper-not-two-independent-leads-count-corrects-65). **Six leads corrects to five.** CICF-hosted PDF route (`cicfconf.org/sites/default/files/paper_357.pdf`) worked for the 2015 draft as the prior chat noted; SSRN itself 403'd in-session as expected |
| 0.3 | Machine profile consults — `scripts/instrument_profiles.py cell <SYM> <mechanism-id>` | **DONE (bounded)** | `MECHANISMS.md` read in full: no existing id matches any of the five shapes (growth rule forbids registering `NEW` outside a same-commit pre-registration — Phase 0 cannot invent ids). Ran consults against the *nearest existing* ids for adjacency signal: `MNQ × intraday-momentum` → `DEAD` 2026-07-21 (Baltussen-class decayed on modern MNQ, OHLCV bar attached — relevant to L2's adjacency); `USOIL × commodity-carry-term-structure` → `DEAD` 2026-06-06 (disguised trend trade — relevant to L5's adjacency, but L5 trades curve-slope *change*, distinguishable per §2 P3); `MCL`/`MGC × commodity-carry-term-structure` → untested, no cell, but both carry the `free-data-5th-leg-snag-closed-2026-07-01` BINDING BAR; `6J × event-window-reversal` → untested, no binding bar. **Open sub-item, not yet resolved:** the SNAG-closed bar on MCL/MGC appears (per `docs/rejected_candidates.md` context, "5th-leg target spec 0/24; chop-native 0/9") to scope to the **5th-portfolio-leg self-funded addition programme**, a different channel from harvest intake — but the ledgers' `bars:` YAML doesn't encode that channel scope explicitly the way the M2K OHLCV bar's class-level framing does. Flagged for the door-check at G0, not resolved here |
| 0.4 | Venue screen — E1 envelope, §4a hedging sign-constraint, per-instrument cost bars | **DONE** | Cost bars now on file for every relevant instrument: MCL 5.3423 bp/RT (2023 median); M2K 11.89 bp/RT (confirms index sleeve is the most expensive — already blocked by the OHLCV bar independently); M6A cost-tax 0.0902 (`FLAG-COSTBIND`); MGC cites the same third-leg-map 0.0902 figure; **6J has no `cost_hurdle` registered on its ledger** — the Aegis→6J work never needed one (self-funded panel-economics questions, not a cost-bp screen) — a fresh Req-5 cost measurement is owed before 6J stages past Phase 0 |
| 0.5 | Cost/power pre-screen | **DONE (bounded)** | Directly enabled by 0.4's bars. MCL/MGC clear expressibility at the geometry level (per their own ledgers' `SIGMA-NATIVE`/class-attestation entries — geometry ≠ edge, unchanged). No power/N figure computed yet for any of the five shapes specifically — that's a Phase-1 CF output (trade count under the frozen construct), not a Phase-0 input |
| 0.6 | Dedup pastes per lead | **DONE** | **H-OD-1** identified precisely: ES 02:00–03:00 ET overnight-drift hour, Boyarchenko-Larsen-Whelan FRBNY SR917 **dealer inventory-risk** mechanism — died at Stage-2 cost-law (`strategy_harvest.md` §2.1 Tier C: "D5 and H-OD-1 both died here on parent contracts... contract size is not a mitigating lever"). This is the **closest prior precedent in the whole estate** to L3/L6's WHO (market-maker/dealer inventory-risk absorption) and to L2 (dealer-gamma hedging flow) — same null mode the plan already anticipated, now with a named, dated analog. **M2K overnight-fade** = `overnight-range-failed-extension-fade` (MSL-C3-K2 dual-axis explore, both arms CI < 0, FALSIFIED 2026-08-13) — a level-gated fade, structurally different from L3/L6's unconditional close→open reversal, so not a direct dedup collision, but same instrument-class caution. **Third-Friday-MYM-overnight** = the `event-window-reversal` MYM M5 finding (third-Friday derivative-settlement reversal, exact-coverage sourced but power legs below floor, tradable limb negative 2024–2026) — a *scheduled-window* reversal, distinguishable from L3/L6's *every-session* reversal. **L2 dealer-gamma**: `Q-ORB-GEX-1` reconfirmed verbatim (rejected 2026-06-25, NAS100 ORB dealer-GEX sign-gate, edge collapsed to a realized-vol proxy under the orthogonality partial) |
| 0.7 | Data-route map | **DONE** | This worktree has no vendor CME panels (§0, confirmed). `GC.FUT` DL-1 cache is real, TRAIN-only (2010-06-06→2019-01-01), reusable at $0 for L3/L6's gold cell. **CL.FUT/6A.FUT confirmed symbol-valid and $0-cost-dry-run-priced** (deep-lane charter §0/§2.3: `GC.FUT,CL.FUT,6A.FUT` parent all resolve on GLBX.MDP3, TRAIN window priced at $0.00 both schemas) **but NOT yet pulled/cached** — only `GC.FUT` was actually scored for DL-1's abandoned TRAIN run; a fresh $0 pull is needed for CL/6A if L5 stages. Era-split floor `2010-06-06` confirmed as the dataset floor (deep-lane charter, same source) |

---

## §4 Phase 1 — $0 kill-only cheap falsifiers (recorded for continuity; not started)

CC-side inline (panel: these fail the fleet surface-allocation test-3 for Cursor — <1hr builds,
data local-only).

- **P1-CF:** fade-overnight-move / hold-to-16:00 on `MGC_M15` + `6J_M15` (+ `GC.FUT` cache for
  depth). Segmentation/roll-exclusion/holiday handling **frozen a priori** — an unfrozen CF has
  forking-paths freedom that undermines its own kill authority. Hard-stop overlay priced in.
- **P2-CF:** venue-expressible next-day-reversal slice (18:00–reopen/open → close next day, paying
  the decomposed RT count), same panels — not raw close-to-close autocorrelation.
- **P3:** Databento curve-data cost dry-run only. **EXECUTED 2026-08-17** — bars $0; sleeve CLOSED on standing calendar-spread SCREEN-FAIL ([`P3_DRYRUN`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md)).
- **P4/P5:** route/access memos only.

**Asymmetric by declaration:** FAIL kills a sleeve; PASS licenses only a priced data-extension
decision — never direct Phase-2 staging (at ~4bp/day, local-panel N can't separate the effect
from zero; H-TSMOM Clause-N precedent). Multi-instrument selection is falsify-only or enumerated
in `K_intrinsic`.

Kills land on all four surfaces: dated LOG · CANDIDATE_ROWS addendum · STATE line · registry row
where closure-shaped. Blind-channel 2/3 counter untouched; harvest limb-2 (0/2) is the counter at
risk.

### P1-CF / P2-CF design freeze (2026-08-17, this session — required before any harness is built)

**Instruments:** `MGC` + `6J` (P1-CF), same pair (P2-CF). MCL excluded from both — pre-killed by
arithmetic (§2 P1, §0). Panel: TV `1!` volume-lead continuous (`MGC.v.0` / `6J.v.0` equivalent) —
the repo's own standing admissible convention (`.c.0` calendar-roll is inadmissible for P&L per
[`M2K.md` W1](../../../ops/instruments/M2K.md)); no fixed-calendar roll-exclusion band is invented
here, since volume-lead panels already carry the correct front-month by construction.

**Roll handling:** exclude any session where the panel's front-month designation changes intraday
(the DL-1 stitch convention — "front month = per-day volume leader; a roll day = the day the
leader changes," [`stitch.py`](../../../lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/stitch.py)) —
this is a **fresh application of a standing repo convention to a new instrument pair, not a
re-derivation of the frozen `ROLL-EXCLUDE-2026-07-31` ruling**, which governs MCL/M2K/MYM only and
is out of scope here by its own text's terms.

**Session boundary:** flat by **16:00 ET** (E1 default print, confirmed —
[`prop_envelope_default.md`](../../../ops/prop_envelope_default.md) L87: "all four FRIENDLY deadlines
primary-verified; binding minimum MFFU 16:10 ET"). Holiday-short handling: flat by **12:59 ET** on
CME early-close days, per the original plan text — **not yet cross-checked against a current CME
holiday calendar this session**; do that check before the CF runs for real, not after (matches the
6J ledger's own standing warning that early-close lists go stale annually).

**Segmentation:** one signal per session (fade the overnight move, hold to the flat boundary) —
no intraday re-entry, no pyramiding, hard-stop overlay sized at the session's own measured σ
(reuse the `SIGMA-NATIVE` convention already applied to MCL/MGC rather than an assumed k·ATR).

**What this does NOT resolve:** the actual CF run needs `MGC_M15`/`6J_M15` (or `.v.0` 1m/native)
panel bytes, which **this worktree does not have** (§0 confirmed). The primary checkout is where
these panels live per the original plan text ("on hand"). This is a logistics fork, not a design
question — raised to the operator alongside this mark, not resolved unilaterally.

### P1-CF / P2-CF EXECUTED 2026-08-17 — FAIL, all four legs

Operator chose to switch to the primary checkout for execution. `core/data/bar_data/MGC_M15.csv`
(frozen, 2022-08-01→2026-08-12, 95,262 bars) and `6J_M15.csv` (frozen, through 2026-07-01, 161,752
bars) were already on hand there — an operator-supplied fresh MGC export
(`BAR_EXPORT_v0.2_COMEX_MINI_MGC1!_2026-08-17_05851.csv`) turned out not to be needed for this run
(landed anyway, available for a future `MGC_M15.csv` refresh).

**Result: FAIL on all four legs** (P1×MGC, P1×6J, P2×MGC, P2×6J) — three gross-negative outright;
the fourth (P1×6J) gross-positive but t=0.64 (not significant) and 0.73× the 4× cost hurdle (below
it). Stop-trigger rate 3.3–4.7% across all legs rules out the hard-stop as the driver; the
long/short split shows each instrument's own trend swamping the fade, not a construction defect.
Full writeup: [`six_lead_cf_2026-08-17/LOG.md`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/LOG.md).
Landed on 3 of the plan's 4 required surfaces: dated LOG ✓ ·
[CANDIDATE_ROWS addendum](../../../lab/analysis/harvest/radar_tier_a_burst_2026-07/CANDIDATE_ROWS.md#addendum-2026-08-17b--l3l6-resolved-same-paper-not-two-leads-p1p2-cheap-falsifiers-fail-all-four-legs) ✓
· STATE line (pending, this commit) · registry row — **not added**, pre-G0 CF kills don't get a
`rejected_candidates.md` row per the 2026-08-15 pre-G0-kills-are-not-§4-strikes precedent (matches
`MNQ-ANALOGUE-1`/`MNQ-SIZEDIV-1`'s own pattern).

**The harvest §4 limb-2 counter question is now RULED** (§13 below) — does not increment; running
count stays 0/2. $0/K=0 throughout — panels on hand, no pull.

## §5 Phase 2 — Priced extension + intake staging for survivors (recorded; not started)

Databento dry-runs → operator spend GO ($700 ceiling) → sharpened Req-1a scoring (four-clause
constraint test first; preference-shaped WHOs route to 1b's counted bar — L3/L6's "risk-averse
market makers" is arguably preference-shaped, decided here) → δ/σ extraction per instrument cohort
(digitize precedent recovered via `git show 7ce592a`) → K_banked + Requirement-5 arithmetic →
candidate rows. First admission here also flips the harvest limb-1 idle guard reading before its
2026-11-08 date.

## §6 Phase 3 — G0 + explore, serialized (recorded; not started)

One lead at a time. Engines clearing the surface-allocation test 3 (≥1hr, ≥3 files) go to Cursor
as single handoffs — built against committed synthetic fixtures, real-panel bytes via
`-Copy`/`FP_DATA_ROOT` staging (worktrees lack gitignored vendor data, confirmed §0). Dispatch is
direct — `scripts/dispatch_cursor.ps1` per the 2026-08-14 autonomous-loop ADR. Reuse table for
packets: `cost_es.py`/`cost_mnq.py` frozen cost models, `universe_gate.py` (SPA/DSR), DL-1
`stitch.py` as the volume-lead-stitch reference. K charged at G0; CONFIRM reserved unread.

## §7 Phase 4 — Nominee-only CONFIRM → N-SURV/bust-frontier (recorded; not started)

Tradeify trailing-DD geometry, intraday-honest clock; the Q-POLFRONT-1 cushion-proportional-sizing
lever applies (`RESOLVED-QUANTIFIED`) with its EOD-clock fragility caveat named (median stress
delta +55.2pp vs +1.63pp — carried forward, not a footnote).

---

## §8 Clocks

**2026-11-08** (four-firms §4 + harvest limb-1 idle guard + limb-2 exposure) is the binding clock.
2026-10-07 is context-only — no standing rule ties it to this work. Weekly token trade:
**2026-08-21**.

## §9 CC vs Cursor (one line)

Everything that is judgment, doctrine, K/$, operator-facing, or touches local-only data stays
with this orchestrator session; only Phase-3 engines (and any >1hr Phase-2 tooling, e.g. an
NS-curve-fitting harness for L5) dispatch to Cursor, directly via the dispatch script.

---

## §10 Claim manifest (orchestrator-only writes)

| Item | Holder | Status | PR | Note |
|---|---|---|---|---|
| Plan drafted (this document) | this session | **DRAFTED** | [#32](https://github.com/Joshua-Asante/first-passage/pull/32) merged | Full plan recorded, then executed, on `claude/six-lead-pursuit-phase1-execution` (superset of `-stage-0-a2c299`) |
| Phase 0 items 0.1–0.7 | this session | **DONE** | #32 merged | See §3 execution ledger; headline finding is the L3/L6 same-paper correction (§13) |
| SOURCES_LOG addendum (L3=L6) | this session | **DONE** | #32 merged | [`SOURCES_LOG.md` addendum](../../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md) |
| Phase 0 item 0.8 (operator marks packet) | operator | **MARKED** | #32 merged (marks); OpenAlex addendum landed 17d | §13 — per-lead GO/HOLD marked 2026-08-17; limb-2 counter **RULED** (does not increment); OpenAlex channel addendum **landed** (17d) |
| P3 GO + dry-run | operator un-HOLD (this session) | **DONE — sleeve CLOSED (venue)** | pending | [`P3_DRYRUN`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md) — bars $0; S-strategy calendar-spread SCREEN-FAIL; USOIL-carry DISTINGUISHABLE |
| STATE.md correction line | this session | **DONE** | #32 merged | New dated decision-index line, not a retro-edit of the 2026-08-17 historical line |
| P1-CF/P2-CF execution | this session | **DONE — FAIL all four legs** | #32 merged | [`CF LOG`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/LOG.md) |
| Limb-2 counter ruling | operator direction + this session (draft) | **DONE — does not increment** | pending | [`harvest intake ADR` ruling block](../../adr/2026-07-15-external-mechanism-harvest-intake.md#ruling-2026-08-17--p1-cfp2-cf-does-not-increment-limb-2) |

## §11 Program-level stop rules (pre-committed)

- **Phase 0 screen yields zero survivors** (all five leads die on venue/cost/dedup before any CF
  runs) ⇒ cohort closes at $0, no Databento spend, registry rows filed per lead — same
  asymmetric-by-declaration discipline as Phase 1.
- **§4 (Phase 1) asymmetric-by-declaration** stands as stated above — PASS never licenses direct
  staging.
- **2026-11-08** with no admitted Req-1a candidate from this cohort ⇒ folds into the standing
  four-firms §4 / harvest limb clocks — no separate clock, no extension by re-framing.
- ~~**L3/L6 not resolved as one-vs-two programs before either stages**~~ **DISCHARGED 2026-08-17**
  — resolved same paper (§13), not two programs; the precondition this rule guarded against no
  longer applies to a single lead.

## §12 Cost envelope

$0 and K=0 through Phase 0 and Phase 1 in full. Phase 2 introduces the first possible spend
(Databento dry-runs, then priced pulls against the $700 ceiling) — gated on operator GO, not
assumed. No `register_search open`, no Cap claim, no live-risk surface touched anywhere in this
plan.

## §13 Phase 0 findings & operator marks packet (item 0.8 — recommendations, not elections)

This is the STATE.md OPERATOR QUEUE row-3 payload (queues behind F1, B7-REFIRE/M1). Everything
below is a recommendation for operator sign-off — none of it is self-executing.

### Headline finding: six leads corrects to five

L3 and L6 are the same paper (2015 "Market Closure and Short-Term Reversal" →2022
"Overnight-Intraday Reversal Everywhere", same SSRN abstract `2730304`, explicit self-citation of
the retitle). This isn't a close call needing a judgment mark — it's a documentary fact, verified
against the papers themselves. **Recommend:** accept as resolved (no operator mark needed on the
fact itself); the marks below are about what to *do* with the now-five-lead cohort.

### Per-lead GO/HOLD — OPERATOR MARKED 2026-08-17

| Lead | Mark | Why |
|---|---|---|
| **P1 (L3=L6)** overnight-reversal | **GO** — operator, 2026-08-17 | Overlap resolved; MGC+6J panels on hand at the primary checkout; MCL pre-kill confirmed by arithmetic so excluded from the CF's instrument set; 6J needs a fresh cost-bp measurement before its own CF leg, not before MGC's |
| **P2 (L1)** index-flow reversal | **GO** — operator, 2026-08-17 | Same $0 panels; venue-expressible-slice discipline already specified in the plan (§4) |
| **P3 (L5)** curve-slope momentum | **GO** — operator un-HOLD, 2026-08-17 (this session); prior HOLD same day discharged | Dry-run + paper read + USOIL-carry dedup executed. Sleeve **CLOSED** on standing calendar-spread SCREEN-FAIL (paper S-strategy = long front / short fourth). Bars $0; `tbbo` CL-parent $1,543.90 (contrast only). Dedup: DISTINGUISHABLE from static USOIL carry, not ADMIT. [`P3_DRYRUN`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P3_DRYRUN.md) |
| **P4 (L2)** dealer-gamma EOD | **HOLD** — operator, 2026-08-17; un-HOLD'd 2026-08-20 → route memo run, disposition HOLD (unchanged verdict, sharper reason); **dry-run + concentration check run same day, disposition still HOLD, evidence updated against** | H-OD-1 dedup (§3 item 0.6) strengthens the existing Q-ORB-GEX-1 + intraday-momentum-decay caution. Route memo found L2 is mechanism-distinct from `Q-ORB-GEX-1` (momentum-continuation vs. regime-gate) but shares the same exogenous flow series and the same orthogonality risk that killed it. Databento `estimate` on `NQ.OPT`: full-history cost trivial (~$5.34, tbbo), but complex-wide trade density is 367× thinner than `NQ.FUT`. Concentration check (definition+trades pull, $0.00): the near-the-money/near-dated slice a real construction would use is **thinner relative to the underlying (~1,423×), not richer** — narrowing to the plausible-construction region widens the density gap instead of closing it. Trade-size/notional-weighted signal strength untested; not a kill, but the open data-sourcing question is now evidenced against a bare trade-count construction. [`P4_ROUTEMEMO`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P4_ROUTEMEMO.md) · [`P4_DRYRUN`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P4_DRYRUN.md) · [`concentration RESULTS`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/p4_concentration_2026-08-20/RESULTS.md) |
| **P5 (L4)** mutual-fund overweight | **HOLD** — operator, 2026-08-17; **un-HOLD'd 2026-08-20 → access probe run, disposition `UNSCREENABLE`, CLOSED** | 13F/N-Q ~45-day disclosure lag is a hard real-time-reconstructibility wall on its face. Confirmed by web verification 2026-08-20: 13F = 45-day lag, Form N-PORT = 60-day lag, 2026 SEC proposal narrows rather than accelerates disclosure; no systematic near-real-time substitute exists. [`P5_ACCESSPROBE`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P5_ACCESSPROBE.md) |

**Still unmarked** (not addressed by the P1/P2 GO): the limb-2 counter ruling and the
channel-scope amend-in-place note, both below. The GO licenses *attempting* P1-CF/P2-CF — it does
not resolve what a FAIL on either costs the harvest channel's own bookkeeping.

### Limb-2 counter ruling — RESOLVED 2026-08-17, does not increment

**Question restated as a symptom, not a fix:** does a Phase-1 cheap-falsifier kill on one of these
leads count toward harvest §4 limb-2's 0/2, or does it stay outside that counter the way pre-G0
kills stay outside §4 strikes generally (per the 2026-08-15 pre-G0-kills-are-not-§4-strikes
ruling)?

**Ruled** (operator direction, Claude Code draft) on the P1-CF/P2-CF FAIL result: **does not
increment.** Two independent grounds — landed on the counter's own canonical surface, not restated
here:
[`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](../../adr/2026-07-15-external-mechanism-harvest-intake.md)
counting-machinery table + "Ruling 2026-08-17" block. (1) Neither lead was ever **admitted**
through this intake — no declaration manifest, no `register_search open`, no ratified inventory
row — and §4's falsifier is scoped to mechanisms "admitted through this intake," so an
unadmitted screen cannot be an intake-class closure. (2) Even setting admission aside, the kill
class doesn't match the counted categories (Stage-2 cost-law / Clause-N power) — P1-CF/P2-CF used
this plan's own frozen cheap-falsifier construction, not the harvest campaign's Stage-0/cohort-δ
machinery. Running count stays **0/2**.

### Channel-scope amend-in-place note (drafted for operator ratification, not yet landed)

The 2026-08-16 fork election (admit an OpenAlex-based substitute traversal when S2 has no record
of a seed paper) has no corresponding line in
[`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](../../adr/2026-07-15-external-mechanism-harvest-intake.md)
— checked this session, zero `OpenAlex` mentions in that ADR. Recommended addendum text for that
ADR (operator ratifies or edits before landing):

> **2026-08-17 addendum — OpenAlex admitted as a Semantic-Scholar-index-gap substitute channel.**
> When S2 has no record of a seed paper (DOI/title/author search all empty, independently
> re-verified), OpenAlex's citation graph (`api.openalex.org/works?filter=cites:<id>`) is an
> admitted substitute traversal, screened via the same keyword-shortlist → manual-screen →
> adversarial-verify funnel. OpenAlex carries no `isInfluential`-equivalent flag, so a substitute
> run screens every keyword-shortlisted survivor by hand rather than pre-narrowing on a citation-
> importance signal — arguably more exhaustive on that one axis, at higher review cost.

**Recommend:** operator marks GO/edit-then-GO/HOLD on landing this addendum; it is not landed by
this plan.

---

## Verification

```
# Grounding reads (§0) — re-run to confirm nothing drifted since 5d8bf59
git log --oneline -1
sed -n '255,270p' core/firm_rules.py
grep -n "Micro10Y\|OHLCV raised bar\|index-intraday-ohlcv" docs/rejected_candidates.md
sed -n '1,15p' docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md
grep -n "FLAG-COSTBIND" ops/instruments/M6A.md
ls core/data/tv_exports/cme/
sed -n '1,35p' lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/stitch.py

# Phase 0 execution (§3) — re-run to confirm nothing drifted
# L3/L6 same-paper finding: re-fetch https://www.cicfconf.org/sites/default/files/paper_357.pdf
# (2015 draft, 3 authors) and the 2022-draft PDF found via WebSearch "Della Corte Kosowski Liu Wang
# Overnight-Intraday Reversal Everywhere"; both self-cite SSRN abstract=2730304 — see the
# SOURCES_LOG addendum for the exact extracted quotes (primary evidence already captured there)
python scripts/instrument_profiles.py cell MNQ intraday-momentum
python scripts/instrument_profiles.py cell USOIL commodity-carry-term-structure
python scripts/instrument_profiles.py cell MCL commodity-carry-term-structure
grep -n "cost_hurdle" -A3 ops/instruments/MCL.md ops/instruments/M2K.md
grep -n "H-OD-1" STATE.md docs/methodology/strategy_harvest.md
grep -n "OpenAlex" docs/adr/2026-07-15-external-mechanism-harvest-intake.md  # expect: no matches (addendum not yet landed)
```
