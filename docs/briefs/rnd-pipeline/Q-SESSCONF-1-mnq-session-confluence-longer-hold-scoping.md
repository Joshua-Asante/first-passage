# Q-SESSCONF-1 — MNQ session-confluence longer-hold: is there headroom over the incumbent?

> ⚠ **CLOSED — FALSIFIED (2026-08-02).** This Stage-0 screen resolved: `max_h annSR_h − annSR_close
> = +0.091` (13:45 cell, admissible ladder) against the pre-registered `Δ* = +0.124` — the
> hold-window axis does not clear the K-price ceiling; the externally-carved-out 60-75 min class
> measured adverse (+0.501/+0.490 vs incumbent +0.842). The MNQ Cap seat remains unspent ($0/K=0),
> discharging the 2026-07-21 domain audit's 'untested' preservation. Full disposition:
> [`lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md`](../../../lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md);
> ledger entry: [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) 2026-08-02; bar
> discharge: [`docs/rejected_candidates.md`](../../rejected_candidates.md) 2026-08-02 status
> update. The `Status: OPEN` / `Closed: N/A` line below is the original pre-registration state,
> retained byte-intact per Rule 14 — it is superseded, not current.
>
> Since `RESULTS.md` already contains every element §9 requires of a closure record (verdict,
> `max_h annSR_h` vs `annSR_close` vs Δ\*, the panel SHA256, what §4 predicted vs what happened,
> and confirmation the Cap seat remains unspent), it stands in place of the never-produced §9
> closure artifact — no separate `docs/briefs/closures/Q-SESSCONF-1-closure-falsified.md` was
> authored, or is owed.

**Status:** `OPEN` — Stage-0 scoping, **K=0 / $0 / no manifest / seat unspent**
**Authored:** 2026-08-01
**Closed:** N/A
**Authors:** Joshua (operator ruling 2026-08-01: "hold the seat; K=0 screen first") + Claude Code (Fable 5)
**Parent question:** N/A — cites the 2026-07-21 domain audit's explicitly-preserved thread as warrant, not as a re-gate
**Loop:** Inquire-phase Pre-Q — closure gates on a single order-free ceiling computation
**Artifact path:** `docs/briefs/rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md`

**Spends nothing.** No `register_search`, no discovery manifest, no data pull, no K. The MNQ family's
single remaining `K_intrinsic=1` Cap seat stays **unspent** — this brief exists to decide whether it is
worth spending, and is designed to be able to answer "no" for zero runs.

---

## §0 — Rule 0 reads (production/artifact source, verified 2026-08-01 at `491d3b6`, worktree clean, 0/0 vs `origin/main`)

| Source | Anchor | What it supplies |
|---|---|---|
| [`docs/rejected_candidates.md`](../../rejected_candidates.md) L405–420 | `fbf3590` 2026-07-27 | **The governing raised bar**, verbatim clauses 1–3, and the verbatim preservation of this thread. |
| [`docs/notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md`](../../notes/audits/programme-audit/2026-07-21-index-futures-intraday-ohlcv-domain-audit.md) | `e8be736` 2026-07-21 | Domain verdict **STABLE (saturating)**, NOT a SNAG; §5 follow-up #1 (the bar) — **confirmed LANDED**, see §2 attestation. |
| [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) | `66c2a14` 2026-07-31 | N1 (ORB real/regime-conditional), **N3 (both exit-redesign spaces pre-killed order-free)**, N6 cost hurdle 3.01 bp/session, W3 (1m feed cannot fill), F2 guard. |
| [`lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md`](../../../lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md) | `df13e74` 2026-07-16 | Incumbent annSR at **Tradeify** $0.91/side +1 tick: **+0.835** full / **+1.140** 2021+. |
| [`lab/research_utils/deflated_sharpe.py`](../../../lab/research_utils/deflated_sharpe.py) L89–98 | `48b8cef` 2026-07-12 | Production `expected_max_sharpe` — the selection benchmark §4's threshold is derived from (not re-implemented). |
| [`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](../pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) §2/§5 | `df13e74` 2026-07-16 | Pinned floor ladder K=1→0.65 · 2→0.85 · 3→0.98 · 4→1.06 FAIL; frozen construct; forbidden-moves list. |
| [`docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md`](../../adr/2026-07-31-orb-mnq-unpark-payability-target.md) Add. 2026-07-31b/c | `b22aef8` 2026-07-31 | **Ruling 1** `K_banked(MNQ)=2`, one seat left, unspent; T1 PASS; **adverse**: corrected-clock RF **0.93**, 2026 YTD **−$2,431**. |
| [`docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md`](SLR-MYM-1-liquidity-sweep-reclaim-scoping.md) | `33a40f8` 2026-07-29 | Nearest-shape precedent: a session-structure mechanism on the sibling instrument, **CLOSED-FALSIFIED at Stage 0, $0/0K**. |

**Data-path read (Trap #14 pre-flight — the panel is gitignored vendor data).**
`core/data/bar_data/MNQ_M15.csv` is **absent from this worktree** and **present in the primary
checkout** at `C:\Users\joshu\multi_firm_operations\core\data\bar_data\MNQ_M15.csv`
(8,667,680 bytes, mtime 2026-07-21). Per MNQ.md N7 the panel is BAR EXPORT v0.2 `CME_MINI:MNQ1!`,
n=141,536, span **2020-07-01 → 2026-07-03Z**. §7 therefore resolves the panel from the primary
checkout explicitly and **re-pins deliberately, never incidentally** (N7: a live-ops refresh once
invalidated a research pin).

---

## §1 — Context & motivation

The 2026-07-21 object-layer domain audit returned **STABLE (saturating)** for
single-instrument index-futures intraday OHLCV directional timing, declined the requested
domain-SNAG, and landed a raised re-proposal bar. That bar explicitly preserves two things:
`ORB-MNQ-1` (the survivor) and the **session-confluence longer-hold** thread, tagged verbatim
*"(untested, low-priority — ORB-MNQ already occupies that class)"*. It has carried that
"untested" status for eleven days and rides the **2026-08-08** slate.

Two things make now the moment to discharge it rather than carry it further. First, a
reachability computation run 2026-08-01 (§2) established that the arithmetic cost of composing
anything onto the incumbent is **+0.124 annualized Sharpe** — a number that did not previously
exist and that turns the bar's qualitative clause 3 into a threshold. Second, the operator ruled
the same day to **hold the MNQ Cap seat and run a K=0 screen first**, which is only coherent if
the screen can return a decisive negative. This brief is that screen.

**The honest position on the bar, stated up front rather than argued around:** of the three
re-proposal clauses, this thread clears **only clause 3**. Clause 1 fails — "longer-hold" is a
*hold-time* lever, and the bar names price / instrument-selection / hold-time as all mapped, with
"a re-tune of any mapped lever" being the exhausted move. Clause 2 fails — same OHLCV modality,
same venue, no binding wall relaxed. So the thread is alive on one clause, and that clause is the
hardest one: *beats the incumbent net-of-cost*.

---

## §2 — Prior art / lineage, and the dedup attestation (command output pasted, per ADR §2-C §5)

**Searched by mechanism family across the whole tree including LTM and archive** (`rg --no-ignore`,
because Claude Code Grep silently excludes `lab/archive/` and `docs/ltm/`), and explicitly
including `docs/notes/notice/` — the surface the 2026-07-31 fade attestation was found to have
missed.

```
$ rg --no-ignore -il "session.?confluence|longer.?hold|hold.?time.?lever" --glob '!**/.git/**'
lab\archive\guardian_decay_gate_2026-06-25\README.md
docs\briefs\Q-RAIL-1-c1-execution-rail-go-live-scoping.md
docs\rejected_candidates.md
docs\methodology\rejected_signals.md
docs\methodology\lessons\methodology_lessons.md
docs\briefs\rnd-pipeline\SLR-MYM-1-liquidity-sweep-reclaim-scoping.md
docs\briefs\rnd-pipeline\OPENPRESS-1-opening-volume-efficiency-map.md
docs\notes\rail_build\B7_STAGE1_DESK_CARD_2026-07-28.md
STATE.md
lab\analysis\aegis_6j_transfer_2026-07-05\RUNSPEC_EOD_OFF.md
docs\notes\audits\programme-audit\2026-07-11-core-fxify-anchoring-audit.md
docs\notes\audits\programme-audit\2026-07-21-index-futures-intraday-ohlcv-domain-audit.md

$ ls docs/notes/notice/          # the surface the 2026-07-31 fade attestation missed
2026-05-25-guardian-swap-not-in-backtest.md          N-2026-06-20-nas100-identify-corpus-routing.md
2026-05-25-tweaks-1-2-5-falsifier-window.md          N-2026-07-10-vendor-csv-manifest-drift.md
N-2026-05-29-pepperstone-alchemy-feed-divergence.md  N-2026-07-11-terminal-standing-displaces-portfolio-action.md
N-2026-06-01-guardian-grace-label-stale.md           N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md
N-2026-06-03-nas100-indicator-contractvalue-missing.md  N-2026-07-26-forced-flow-census.md
# None bears on an MNQ intraday hold-window mechanism. N-2026-07-26 is a forced-flow census
# (CL/energy feeder for the fade program), not an index-futures timing surface.

$ rg -n "index-futures intraday|session-confluence" docs/rejected_candidates.md
411:### Single-instrument index-futures intraday OHLCV directional timing — RAISED BAR ... 2026-07-21
416:**Re-proposal bar (domain-level).** A *new* ... candidate is **not admitted for a full Pre-Q** unless it clears one of:
420:**Explicitly preserved (NOT rejected):** `ORB-MNQ-1` (the survivor) and the **session-confluence
     longer-hold** thread (untested, low-priority — ORB-MNQ already occupies that class).
```

⚠ **Reader note (2026-08-23):** the `ls` paste above is the original attestation and is not rewritten. `N-2026-07-26-forced-flow-census.md` was later pruned at the Great Prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`.

**Attestation result: CLEAR, with one raised bar and one adverse precedent — no prior closure bars
this thread.** Audit follow-up #1 is **DISCHARGED** (the bar landed at L411; the audit's own §5 had
listed it as owed to the operator at/before 08-08).

Lineage that bears directly:

- **The raised bar itself** (`rejected_candidates.md` L416) — governs. Clause 3 is the only live route (§1).
- **ORB conditioning-gate class — 4/4 FALSIFIED, recorded at tail-exhaustion**: overnight-path → gap → **GEX** (G-regime-orthogonality partial-t −0.58, collapses to a vol proxy) → **T10Y3M** (G-era-confound year-FE t +0.81 n.s.) → plus **Friday** (G1 wide-best-of-K fw-p 0.0996 over a 24-cut family). This class is the *residual* if the hold-time axis fails — see §6.
- **MNQ.md N3** — both exit-redesign spaces already **pre-killed order-free, zero runs** (tighter stops lose 0.03–0.06R; no fixed profit target reaches baseline, `E_best` max +0.088 vs +0.099). §7's Limb A is the *same method* applied to a different axis (time-exit horizon), and N3 is the precedent that it can be decisive without a run.
- **SLR-MYM-1** (`33a40f8`, 2026-07-29) — a session-structure (liquidity-sweep-reclaim) mechanism on the sibling instrument, **CLOSED-FALSIFIED at Stage 0, $0/0K**. Nearest-shape precedent and it went the adverse way.
- **External bound** — arXiv 2605.04004: 14 signal families on MNQ, **0/14** survive a 2-pt cost. The 60–75 min class is what that study carved out, which is the entire reason this thread was ever tagged untested.
- **Q-COMPOSE-1** — forbids iterating the book weight; this brief does not touch composition into the c1 book.

**The reachability computation (run 2026-08-01, parent-side, before this brief was authored).**
Using production `expected_max_sharpe` at V=1/n, the DSR ≥ 0.95 floor is
`(E[maxZ_K] + 1.645) / √T` — trade frequency cancels, so only K and the scoring-era length T bind.
Method validated: the pinned ladder reproduces at implied T = 6.40 / 6.49 / 6.50 / 6.47 yr for
K = 1/2/3/4, i.e. the ladder carries an implicit **6.5-year era basis**.

| Scoring era | T (yr) | floor K=2 | floor K=3 | **K-price (3−2)** |
|---|---:|---:|---:|---:|
| Full native MNQ 2019-05-06+ | 7.233 | 0.8048 | 0.9287 | **+0.1238** |
| "Since 2020" 2020-01-01+ | 6.578 | 0.8438 | 0.9738 | +0.1300 |
| 2021+ | 5.574 | 0.9168 | 1.0579 (**> Cap 1.0**) | +0.1411 |

Two consequences, both new: composing raises the candidate's own bar by **+0.124 at the most
generous admissible era**; and the seat only exists at all if the scoring era runs **longer than
6.24 years** (start ≤ ~2020-05), because at shorter eras `floor(K=3)` exceeds the 1.0 Cap.

---

## §3 — Question

**Pre-Q gate test:** the symptom is a preserved-but-unmeasured thread whose only admission route
now carries a quantified threshold; the question names that gap, not a construct to build.

**Q-SESSCONF-1:** The session-confluence longer-hold thread on MNQ has been carried as "untested"
since 2026-07-21 while its only surviving admission route requires beating the incumbent
net-of-cost — **what is the maximum improvement over `ORB-MNQ-1` that any hold-window
restructuring of an MNQ intraday directional construct could deliver, and does that ceiling reach
the threshold the K arithmetic sets?**

---

## §4 — Falsifiable hypothesis (H-SESSCONF-1)

Let **Δ\* = +0.124 annualized Sharpe** — the K-price of composition at the most generous
admissible scoring era (§2). Let `annSR_close` be the incumbent construct's net annualized Sharpe
at Tradeify economics measured **on the local panel**, and `max_h annSR_h` the maximum over a
frozen, enumerated set of fixed time-exit horizons on **that same panel**.

**H-SESSCONF-1 — If** `max_h annSR_h − annSR_close ≥ Δ*`, **then** the hold-window axis carries
headroom sufficient to pay for the K that composing costs, the thread clears raised-bar clause 3
in principle, and it warrants a component δ-extraction (Limb B) — **otherwise** the hold-window
axis is exhausted, the residual thread collapses into the ORB conditioning-gate class that is
already 4/4 FALSIFIED and recorded at tail-exhaustion, and the thread closes **FALSIFIED at
Stage 0 for zero runs, zero K, and zero spend**.

**Accept (RESOLVED) if:** `max_h annSR_h − annSR_close ≥ +0.124`.
**Reject (FALSIFIED) if:** `max_h annSR_h − annSR_close < +0.124`.
**Ambiguous-hold if:** the local panel cannot support the comparison — trade count on the
reconstructed baseline falls below **n = 400** (the Default-#3 `dsr_unreachable_low_n` shape), or
the reconstructed `annSR_close` fails to reproduce the published Stage-7 Tradeify figure within
**±0.15 annSR** after accounting for the panel's shorter span (2020-07-01 vs 2019-05-06). Either
condition means the harness is measuring something other than the incumbent, which is a defect,
not a verdict.

**Cohort-binding note (load-bearing).** The published +0.835 / +1.140 are measured on the native
harness over 2019-05+ and 2021+. The local panel starts **2020-07-01**. Baseline and alternatives
must therefore be computed **within the same panel** and compared to each other; the published
figures are a *reproduction check* (the ±0.15 band above), never the comparator. Comparing a
local-panel alternative against a published-cohort baseline is the "mixes two panels" error
corrected in the fade program on 2026-07-31.

---

## §5 — Forbidden moves

- **Adopting the argmax horizon `h*` as a construct.** Genuinely tempting: the sweep will name a
  best horizon, and it will look like a finding. The sweep is a **ceiling computation only** — its
  output is `max_h`, used to *falsify*. Adopting `h*` is exit-time tuning inside a space pre-killed
  by `RESULTS_tv_export_realism.md` §2b/2c and by MNQ.md N3, it is precisely the "re-tune of a
  mapped lever" the raised bar calls the exhausted move, and it would make the result a new
  candidate at `K_eff = 3` (floor 0.98+) that the construct's own 0.890 annSR does not clear.
  This is the same shape as the 15:30-exit temptation the ORB unpark ADR §5 forbids.
- **Routing a surviving horizon into the F2-guarded slice class.** MNQ.md's F2 guard names
  ORB slices that "look better" in-sample (Friday / Monday / OR-hi / same_bar) as the highest-risk
  laundering move on this instrument. A horizon result must not be crossed with any of them.
- **Re-running the four falsified conditioning gates as "confluence components."** Renaming
  gap/GEX/T10Y3M/DOW as confluence does not revive them; each has a recorded `addback_condition`
  and none is met.
- **Treating a Limb-A pass as admission.** A pass authorizes Limb B (δ-extraction), nothing more.
  The Cap seat still requires a frozen era ruling and a separate operator GO.
- **Freezing a scoring era by looking at which one clears.** The §2 table shows the eras move the
  floor in opposite directions to the measured Sharpe; picking on that basis is best-of-window,
  the move `D5-RECOST` §5 forbids. Any era freeze is an operator ruling made on principle first.
- **Amending Δ\* after seeing `max_h`.** Known Trap #12. Δ\* is pinned here at +0.124 with its
  derivation; if it is wrong, close this brief AMBIGUOUS and open a fresh one.
- **Outcome-conditional D-tests** — e.g. computing horizons only on days the incumbent lost.
  Categorically forbidden; it encodes the conclusion.

---

## §6 — Gate criteria

Frozen before Phase 1. Phase 1 has not run.

| Verdict | Trigger | Disposition |
|---|---|---|
| `FALSIFIED` | `max_h annSR_h − annSR_close < +0.124` on the local panel | **Close at $0/K=0.** The hold-window axis is exhausted; the residual (confluence-conditioning only) is the 4/4-FALSIFIED tail-exhausted class, so the thread closes rather than forking. Discharge the 07-21 "untested" preservation, record the result against the 08-08 slate, and **the MNQ Cap seat stays unspent**. Update `rejected_candidates.md` L420 to reflect the discharged status. |
| `RESOLVED` | `max_h annSR_h − annSR_close ≥ +0.124` | Authorizes **Limb B only** (component δ-extraction, still K=0). Does **not** admit a candidate, open a manifest, or spend the seat. A composite proposal after Limb B needs: a frozen era ruling, a frozen single construct with `K_intrinsic=1`, and a separate operator GO. |
| `AMBIGUOUS-HOLD` | n < 400 on the reconstructed baseline, **or** `annSR_close` misses the published Stage-7 Tradeify figure by > ±0.15 | Harness defect, not a verdict. Name the specific reproduction failure; re-test once the panel or the reconstruction is repaired. Do **not** report a Δ from a baseline that does not reproduce. |

---

## §7 — Execution plan (self-executing; K=0, $0, no pull)

- **Phase 0 — Rule-0 + data resolution.** Confirm the §0 anchors still resolve. Resolve the panel
  from the primary checkout (`C:\Users\joshu\multi_firm_operations\core\data\bar_data\MNQ_M15.csv`),
  record its **SHA256 and mtime in the RESULTS artifact** before any computation — the panel is
  gitignored, so the hash is the only provenance (N7: re-pin deliberately). Confirm span and n.
- **Phase 1 — Baseline reproduction (the gate that makes Phase 2 interpretable).** Rebuild the
  frozen ORB construct (OR = 2×15m from the 09:30 ET cash open, both-sides touch-fill, stop at the
  opposite OR extreme, exit at session close 16:00 per D5) on the local panel at **Tradeify
  economics** ($0.91/side + 1 tick ⇒ `rt_pt` 1.41). Report n and `annSR_close`. **Halt** on the §6
  AMBIGUOUS conditions. This mirrors the Q-GEOFIT-1 discipline: an exact-fit anchor arm is what
  distinguishes "wrong ranges" from "wrong family."
- **Phase 2 — The ceiling.** Compute `annSR_h` over the frozen horizon set
  **h ∈ {30, 45, 60, 75, 90, 120, 150, 180 min, close}** (15m panel ⇒ 2–12 bars; the 60–75 min
  cells are the externally-carved-out class). Report the **full table**, not the max alone — a
  silent top-N is the "no silent caps" failure. Emit `max_h annSR_h − annSR_close`.
- **Phase 3 — Verdict assertion.** Run §6 against the actual numbers. Produce the closure artifact
  per §9. Land `lab/analysis/orb/sessconf_mnq_2026-08/RESULTS.md` with the panel hash, the full
  horizon table, and the verdict.

Artifacts land in `lab/analysis/orb/sessconf_mnq_2026-08/`, citing this brief by path.

### §7 note — 2026-08-01, PRE-RESULT: the frozen horizon axis is not natively expressible

Recorded **before any Phase-1 run** (no `lab/analysis/orb/sessconf_mnq_2026-08/` exists; §10 hook 1
asserts this). Execution mechanics only — **§4, §6 and Δ\* = +0.124 are untouched.**

**Prerequisites verified present:** `.venv-research` Python and the cached panel
`lab/analysis/orb/orb_mnq_2026-07/_mnq_15m.pkl` (15,757,437 bytes, 2026-07-17) both resolve in the
primary checkout.

**The finding.** `orb_lib.orb_backtest` exits at **session close**, where the session is defined by
`Instrument.close_tod` — a **time-of-day**, not a hold duration (`orb_lib.py:58`, `:271`, `:312–317`).
Phase 2's frozen set `h ∈ {30…180 min, close}` is *minutes-after-entry*, which the engine has no
parameter for. So Phase 2 as frozen requires **an engine extension or a reimplemented exit**, and
that carries a faithfulness cost the repo's own native harness explicitly refuses:
*"`orb_lib.orb_backtest` is called verbatim; this file never reimplements the engine"*
([`run_v02_native_clock_kgrid.py`](../../../lab/analysis/orb/orb_mnq_2026-07/run_v02_native_clock_kgrid.py)).
Engine↔Pine parity is already only 96.9%; a hand-rolled exit would sit on top of that.

**A strictly-faithful alternative exists** — sweep `inst.close_tod` (session truncation), engine
called verbatim, exactly as the ADR-blessed clock study does. Because ORB entries cluster shortly
after the 10:00 ET OR completion, a truncated `close_tod` **approximates** the hold-duration
question. It is **not identical**: truncating the session also shortens the *entry* window (so `n`
moves) and the stop-detection window (`rest_tods`), which the hold-duration axis would not.

**Disposition — deliberately NOT self-taken.** Swapping the measured axis is a basis change, and
basis changes made quietly are the exact failure this session already caught twice (the era/floor
mismatch corrected in §2; the fade program's Ruling 4 "mixes two panels"). It is recorded here
pre-result so the choice is made on method, not on which axis is convenient. Either route is legal;
neither may be selected after seeing a number.

### §7 amendment — 2026-08-01, PRE-RESULT: operator ruling, axis = faithful `close_tod` sweep

**Operator ruled in chat 2026-08-01: "use the faithful close_tod sweep."** Phase 2 runs the
session-truncation axis with `orb_lib.orb_backtest` called **verbatim** — no engine extension, no
reimplemented exit. Declared before any run. **§4, §6 and Δ\* = +0.124 are unchanged.**

**Frozen ladder** (12 cells; deliberately fine, because a larger set makes the ceiling *more*
generous and therefore a FALSIFIED verdict *more* conclusive):

`close_tod ∈ {10:45, 11:00, 11:15, 11:45, 12:15, 12:45, 13:15, 13:45, 14:15, 14:45, 15:15, 15:45}` ET

`15:45` (session end 16:00, the v0.2 D5 contract) is the incumbent baseline. The `11:00`/`11:15`
cells are the externally-carved-out **60–75 min class**, measured from the 10:00 ET OR completion.

**Axis semantics, restated.** `h` is now a session-truncation *time-of-day*, not minutes-after-entry.
Truncation also shortens the **entry** window and the stop-detection window (`rest_tods`), so `n`
moves across cells. That is inherent to the faithful axis; per-cell `n` is reported, never hidden.

**Annualization disclosure (load-bearing, declared pre-result).** The published Stage-7 figure uses
`annSR = perTradeSR × √252` — a **fixed** factor ([`run_stage7.py:76`](../../../lab/analysis/orb/orb_mnq_2026-07/run_stage7.py)).
Truncated cells trade less often, so a fixed √252 **overstates** their annualized Sharpe. Both
conventions are computed and reported per cell: `ann252` (published convention, for baseline
comparability) and `annFreq = perTradeSR × √(n/years)` (frequency-correct). **The gate reads the
MORE GENEROUS of the two**, so a FALSIFIED verdict cannot be an artifact of the annualization choice.

**Provenance pinned pre-run.** Engine `orb_lib.py` sha256 `dcfe83e1ad8db180…` and loader
`run_stage2.py` `65f3c9c5e3718949…` are **byte-identical** between this worktree (`origin/main`
`491d3b6`) and the primary checkout (`docs/fade-mcl-parity-integration` `2c5f937`) where the
gitignored panel lives — so the engine run is the engine §0 anchors. Panel `_mnq_15m.pkl` sha256
`81c05e9a4ee319e8b3efa61333cf00a1…`, mtime 2026-07-17, source dbn 2026-07-16 (pickle newer ⇒ the
cache path is taken, no re-decode).

---

## §8 — Verdict pre-registration

§6 is frozen **in this file**, committed before any analysis script exists — proportionate to a
K=0 / $0 / no-pull Stage-0 screen, and matching the SLR-MYM-1 precedent (`33a40f8`), which closed
FALSIFIED at Stage 0 under the same shape. The git commit introducing this brief **is** the
pre-registration; §10 hook 1 asserts it precedes the first Phase-1 artifact.

Pre-registration commit: `<populated at commit time>` · Pre-registration date: 2026-08-01

---

## §9 — Closure record format

- **FALSIFIED** → `docs/briefs/closures/Q-SESSCONF-1-closure-falsified.md` (no `recommendation.md`).
- **RESOLVED** → `docs/briefs/closures/Q-SESSCONF-1-closure-resolved.md`, scoped to "Limb B authorized," never to admission.
- **AMBIGUOUS-HOLD** → `docs/briefs/closures/Q-SESSCONF-1-closure-ambiguous.md` naming the reproduction failure and the re-test condition.

Every closure states: verdict, `max_h annSR_h` vs `annSR_close` vs Δ\* = +0.124, the panel SHA256,
what §4 predicted vs what happened, and whether the Cap seat remains unspent (it must).

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-run: this brief predates any Phase-1 artifact.
git log --format='%h %ci' -1 -- docs/briefs/rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md
ls lab/analysis/orb/sessconf_mnq_2026-08/ 2>/dev/null || echo "no results yet, as expected pre-run"

# 2. The seat is still unspent (the invariant this whole brief protects).
ls discovery_manifests/ | grep -i sessconf && echo "VIOLATION: manifest opened" || echo "OK: no manifest, K unspent"
python -c "import json,glob; print([(f, json.load(open(f)).get('status'), json.load(open(f)).get('K')) for f in glob.glob('discovery_manifests/*.json')])"
# Expected: MNQ family bank still 2 (d5 closed K=1 + st_eh MNQ half); orb manifest 'open' banks nothing.

# 3. The governing bar and this thread's preserved status still read as cited.
rg -n "index-futures intraday|session-confluence longer-hold" docs/rejected_candidates.md   # expect L411 + L420

# 4. Delta-star reproduces from PRODUCTION code (not a re-implementation).
python -c "
import importlib.util,math
s=importlib.util.spec_from_file_location('d','lab/research_utils/deflated_sharpe.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
f=lambda k,T:(m.expected_max_sharpe(k,1.0)+1.6448536269514722)/math.sqrt(T)
print('pinned-ladder check K=3 @6.5y = %.4f (expect ~0.98)'%f(3,6.5))
print('K-price @7.233y            = %+.4f (expect +0.1238)'%(f(3,7.233)-f(2,7.233)))
print('seat exists iff T > %.3f yr'%((m.expected_max_sharpe(3,1.0)+1.6448536269514722)**2))
"

# 5. Forbidden-move check: no argmax horizon was promoted into a construct.
rg -in "h\*|argmax|best horizon" lab/analysis/orb/sessconf_mnq_2026-08/ 2>/dev/null
# Expected: appears only as a ceiling//forbidden-move reference, never as an adopted parameter.

# 6. Incumbent untouched — this brief changes no locked surface.
git diff --stat main -- core/ ops/instruments/ docs/adr/ '*.pine'
# Expected: empty.
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/Q-SESSCONF-1-mnq-session-confluence-longer-hold-scoping.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- docs/rejected_candidates.md                                    # fbf3590
git log -1 --format='%h %ci' -- ops/instruments/MNQ.md                                         # 66c2a14
git log -1 --format='%h %ci' -- lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md                 # df13e74
git log -1 --format='%h %ci' -- lab/research_utils/deflated_sharpe.py                          # 48b8cef

# Cited incumbent figures match the Stage-7 table
rg -n "Tradeify.*0\.91.*0\.835.*1\.140|\+0\.835|\+1\.140" lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage7.md

# Panel resolves in the primary checkout (gitignored; absent from this worktree by design)
ls -la /c/Users/joshu/multi_firm_operations/core/data/bar_data/MNQ_M15.csv
```
