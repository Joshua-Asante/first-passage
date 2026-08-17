# Six-lead pursuit plan — Koijen axis-2 survivors

**Status:** DRAFT · channel + priority election fixed by operator (2026-08-17, this session) ·
authorizes nothing beyond Phase 0 reads/screens ($0 · K=0) · **this document is the claim
manifest for the program** — the orchestrator session is its only writer. **Phase 0 execution
HELD pending operator review of this record** (operator interrupt, 2026-08-17 — record the plan
first, review before any Phase 0 substep runs).
**Objective:** carry the six [Koijen axis-2 OpenAlex-substitute](../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md)
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
| Rates sleeve venue-dead | [`core/firm_rules.py`](../../core/firm_rules.py) ~L259 | "US TREASURIES (ZB/ZN/ZF/ZT/UB) ARE NOT TRADABLE HERE" (article 10468222); sole rates products are EUREX bonds |
| 2026-06-30 Micro10Y/2YY MR rejection | [`docs/rejected_candidates.md`](../rejected_candidates.md) L428 | Confirmed — chop-native 5th-leg sweep, era/tail-wall kill |
| OHLCV raised bar | [`docs/rejected_candidates.md`](../rejected_candidates.md) L24 | `index-intraday-ohlcv-directional-timing-2026-07-21`, tier=always |
| §4a hedging sign-constraint | [`core/firm_rules.py`](../../core/firm_rules.py) comment block | Equity Index Product Group = ES/MES/NQ/MNQ/YM/MYM/RTY/M2K/EMD/NKD + EUREX index; opposing directions prohibited within-group, one account or across |
| TNEC N-SHAPE definition | [`docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md`](../spec/2026-08-08-tradeify-necessary-conditions-target-spec.md) L11 | EM3 independence + hard-stop integrity + EM5 session/slot legality (flat-16:00-ET-inside-16:45-print · micro-expressible · §4a sign constraint · S7 occupancy) |
| MSL slate-2 design box (why it can't fit these leads) | [`docs/adr/2026-08-13-msl-slate-2-design-box.md`](../adr/2026-08-13-msl-slate-2-design-box.md) | `rr`∈[2,3], WR 0.30–0.42, R at bust≤3.0% diffusion frontier, hard-stop mandatory, k=1, no pyramiding — a daily hold-to-close reversal shape does not fit this box |
| M6A `FLAG-COSTBIND` | [`ops/instruments/M6A.md`](../../ops/instruments/M6A.md) | Confirmed: Stage-1 Currencies SURVIVOR under FLAG-COSTBIND; cost-tax 0.0902 binds before the 0.0891 pooled-panel floor; Stage-2 ex-FOMC flips COST→POWER |
| MGC instrument state | [`ops/instruments/MGC.md`](../../ops/instruments/MGC.md) | RE-ENTERED, class-attested, not elected; one dated cell (`event-window-reversal` DEAD, unrelated mechanism); no binding bar against a hold-to-close reversal shape |
| `scripts/instrument_profiles.py cell <SYM> <mechanism-id>` | read in full | Data-independent — reads only `ops/instruments/*.md` + committed `MECHANISMS.md`; safe to run in this worktree without vendor panels |
| On-hand CME panels in **this worktree** | `ls core/data/tv_exports/cme/` | **Only `SHA256SUMS` present — no panel bytes in this worktree.** Matches the plan's own Phase-3 note ("worktrees lack gitignored vendor data, even locally"). Dedup/venue/cost-screen work (data-independent) can proceed here; any actual CSV read (Phase 1 cheap falsifiers) needs `-Copy`/`FP_DATA_ROOT` staging from the primary checkout or a fresh pull |
| GC.FUT deep-history cache | `lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/` | Confirmed real: `CAMPAIGN_ID = "DL1-MGC-ORC"`, `GC.FUT` parent TRAIN 2010-06-06→2019-01-01 (2,168 CME sessions), `MGC.FUT` reserved as CONFIRM/OOS. This is the deep-lane cache the plan proposes reusing for L1/L3's gold cell — same bytes, second consumer, no re-pull |
| 2026-08-17 Koijen axis-2 STATE decision line | [`STATE.md`](../../STATE.md) L64–73 | Matches SOURCES_LOG exactly: 296→234→230→17→7/6 funnel, $0/K=0, no candidate admitted |

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
| P1 | **L3+L6** overnight-reversal program (merged pending overlap resolution) — SOURCES_LOG rows 3 & 6, Della Corte/Kosowski(/Wang \| /Liu/Wang) | Concrete WHO, testable today at $0 on panels the primary checkout holds | Effective universe shrank hard: rates sleeve venue-dead (§0); index sleeve blocked by the OHLCV raised bar + §4a sign-constraint; MCL pre-killed by arithmetic (~10.7bp generous bar vs the paper's ~4bp/day commodity effect — **arithmetic not yet re-derived in this session, carried from the prior chat's reading of the paper's own commodity-leg Sharpe**, flag for Phase 0 re-verification); M6A marginal (`FLAG-COSTBIND`, §0). Informative cells ≈ MGC (+6J as FX signal panel) — both on hand at the primary checkout |
| P2 | **L1** index-flow daily reversal — row 1, Da/Tang/Tao/Yang | Same $0 panels, commodity-native | Must test the venue-expressible slice (18:00–reopen/open → close next day, paying the decomposed RT count), not raw close-to-close autocorrelation — raw existence can pass while the expressible component nets negative |
| P3 | **L5** curve-slope momentum — row 5, Bianchi/Fan/Miffre/Zhang | Real reported edge, weakest WHO | Gated on a Databento multi-tenor cost dry-run ($0) before anything else; USOIL-carry adjacency (already-FALSIFIED `commodity-carry-term-structure` on USOIL) needs dedup adjudication before this is treated as distinguishable |
| P4 | **L2** dealer-gamma EOD transplant — row 2, delta-hedging demand | Real mechanism, uncertain data route | Governed by the Q-ORB-GEX-1 rejection (2026-06-25, edge collapsed to a realized-vol proxy) + exogenous-conditioning orthogonality priors, not the OHLCV bar. Phase 1 = route memo only |
| P5 | **L4** mutual-fund overweight — row 4, Chen/Chen/Cohen | Expected cheap kill | Access probe on the holdings-data real-time lag (13F/N-Q, ~45-day disclosure lag per SOURCES_LOG); likely UNSCREENABLE |

**L-number ↔ SOURCES_LOG row map** (for future readers — this table is new index, not a
retelling of the evidence in [`SOURCES_LOG.md`](../../lab/analysis/harvest/koijen_axis2_openalex_2026-08-17/SOURCES_LOG.md)):
L1=row 1 · L2=row 2 · L3=row 3 · L4=row 4 · L5=row 5 · L6=row 6.

---

## §3 Phase 0 — Consolidation & triage ($0 · K=0 · all CC-side, ~1 session)

**Execution status: NOT STARTED beyond the §0 grounding reads above.** Held for operator review
of this record before any item below runs.

| # | Item | Status | Note |
|---|---|---|---|
| 0.1 | Fetch origin + verify merged SOURCES_LOG content (verify-content-not-path) | **DONE** (this session) | `git fetch origin` clean, HEAD `5d8bf59` = merge of PR #31; SOURCES_LOG read in full, matches STATE.md decision line |
| 0.2 | L3/L6 overlap resolution — read both PDFs (SSRN 403s; CICF-hosted PDF route reported working in the prior chat) | **OWED** | Required by the traversal record itself (SOURCES_LOG row 6: "Treat #3 and #6 as one research program... until resolved by reading both papers directly") before either stages |
| 0.3 | Machine profile consults — `scripts/instrument_profiles.py cell <SYM> <mechanism-id>` per (instrument, lead) cell, output pasted not prose-adjudicated | **OWED** | Tool confirmed data-independent (§0), safe to run in this worktree. Mechanism ids for these six leads are not yet registered in `ops/instruments/MECHANISMS.md` — first sub-step is naming/declaring the mechanism ids, or the consult will FATAL on unknown-mechanism |
| 0.4 | Venue screen — E1 envelope (exit pinned to 16:00 ET build target, 12:59 holiday-short handling), §4a hedging sign-constraint for any index expression, per-instrument cost bars computed before any harness is built | **PARTIALLY GROUNDED** | E1/§4a rule text confirmed (§0); per-instrument cost bars for MCL/6J/M2K not yet pulled from their ledgers — MGC and M6A cost-tax figures already on file (§0) |
| 0.5 | Cost/power pre-screen (rationale: cheapness, `strategy_harvest` §2.2 — not strike-avoidance; the limb-2 pin does not exempt these) | **OWED** | Needs 0.4's per-instrument cost bars first |
| 0.6 | Dedup pastes per lead, incl. family-adjacent H-OD-1, M2K overnight-fade, third-Friday-MYM-overnight kills | **OWED** | Per Rule 8 sub-rule 8 (paste literal search output before new work) — not yet run for these six leads specifically |
| 0.7 | Data-route map | **PARTIALLY DONE** | Confirmed this worktree has no vendor CME panels (§0); confirmed GC.FUT/MGC.FUT DL-1 cache is real and reusable at $0 for L1/L3's gold cell (§0). Still owed: confirm era-split floor (2010-06-06) applies cleanly to a daily-reversal construct, not just the deep-lane's own ORC use; CL/6A on-disk status at the primary checkout unverified from this worktree |
| 0.8 | Operator marks packet (per-lead GO/HOLD; limb-2 counter ruling — do pre-staging CF kills count toward harvest §4's 0/2?; rank-1 channel-scope amend-in-place note) | **OWED — assembles last** | Depends on 0.2–0.7. Once assembled, queues as STATE.md OPERATOR QUEUE row 3 of ≤5 (behind F1, B7-REFIRE/M1) |

---

## §4 Phase 1 — $0 kill-only cheap falsifiers (recorded for continuity; not started)

CC-side inline (panel: these fail the fleet surface-allocation test-3 for Cursor — <1hr builds,
data local-only).

- **P1-CF:** fade-overnight-move / hold-to-16:00 on `MGC_M15` + `6J_M15` (+ `GC.FUT` cache for
  depth). Segmentation/roll-exclusion/holiday handling **frozen a priori** — an unfrozen CF has
  forking-paths freedom that undermines its own kill authority. Hard-stop overlay priced in.
- **P2-CF:** venue-expressible next-day-reversal slice (18:00–reopen/open → close next day, paying
  the decomposed RT count), same panels — not raw close-to-close autocorrelation.
- **P3:** Databento curve-data cost dry-run only.
- **P4/P5:** route/access memos only.

**Asymmetric by declaration:** FAIL kills a sleeve; PASS licenses only a priced data-extension
decision — never direct Phase-2 staging (at ~4bp/day, local-panel N can't separate the effect
from zero; H-TSMOM Clause-N precedent). Multi-instrument selection is falsify-only or enumerated
in `K_intrinsic`.

Kills land on all four surfaces: dated LOG · CANDIDATE_ROWS addendum · STATE line · registry row
where closure-shaped. Blind-channel 2/3 counter untouched; harvest limb-2 (0/2) is the counter at
risk.

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
| Plan drafted (this document) | this session | **DRAFTED** | pending | Full plan recorded on `claude/six-lead-pursuit-stage-0-a2c299`; §0 grounding reads executed; Phase 0 items 0.2–0.8 unstarted |
| Phase 0 items 0.2–0.8 | — | **OWED** | — | Held pending operator review of this record |

## §11 Program-level stop rules (pre-committed)

- **Phase 0 screen yields zero survivors** (all six leads die on venue/cost/dedup before any CF
  runs) ⇒ cohort closes at $0, no Databento spend, registry rows filed per lead — same
  asymmetric-by-declaration discipline as Phase 1.
- **§4 (Phase 1) asymmetric-by-declaration** stands as stated above — PASS never licenses direct
  staging.
- **2026-11-08** with no admitted Req-1a candidate from this cohort ⇒ folds into the standing
  four-firms §4 / harvest limb clocks — no separate clock, no extension by re-framing.
- **L3/L6 not resolved as one-vs-two programs before either stages** (item 0.2) ⇒ neither may
  enter Phase 1 independently; this is a hard precondition, not a preference.

## §12 Cost envelope

$0 and K=0 through Phase 0 and Phase 1 in full. Phase 2 introduces the first possible spend
(Databento dry-runs, then priced pulls against the $700 ceiling) — gated on operator GO, not
assumed. No `register_search open`, no Cap claim, no live-risk surface touched anywhere in this
plan.

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
```
