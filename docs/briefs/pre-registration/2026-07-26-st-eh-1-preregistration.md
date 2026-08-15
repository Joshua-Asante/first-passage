# Stage-0 verdict pre-registration — ST-EH-1 (Supertrend long-panel baseline + dual-track grid, MNQ / MYM)

**Status:** `STAGE-0 FROZEN · §8 GO SIGNED 2026-07-26/JA` (search universe, gate
thresholds, dual-track windows, every data-derived-integer *rule*, and the
reserved-holdout boundary are bound; frozen before the first billable pull —
`register_search open` + the estimate→pull sequence are the unblocked execution
step).
**Campaign:** ST-EH-1 — Supertrend `ST(period, mult)` flip-only stop-and-reverse on
15m, NQ/YM parents + MNQ/MYM native micros. Two instrument families (MNQ, MYM); one
campaign manifest.
**Lane:** blind (grid characterization — mining-shaped, not mechanism-first; the
HARV attestation HARD gate does not bind, but a §R reachability section is included
anyway per the gate-reachability lesson M-20 / Q-HARV-0 scar).
**Authorizing instruction:** parent-session CC handoff
[`docs/briefs/handoffs/2026-07-26-cc-handoff-st-eh-1.md`](../handoffs/2026-07-26-cc-handoff-st-eh-1.md)
(authored 2026-07-25 by the claude.ai advisor session; archived verbatim). Two
premise corrections applied at execution (§1): tooling paths (`lab/`, not
`scripts/`), deliverable root (`lab/analysis/harvest/st_eh_2026-07/`, not `research/st_eh/`).
**Inherits:** ratified Campaign defaults
([`2026-07-11-discovery-campaign-defaults-ratified.md`](../../adr/2026-07-11-discovery-campaign-defaults-ratified.md))
+ DSR K/V supersession
([`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md))
**by reference** — values snapshotted below, not re-ratified. **One structural
extension/override is declared** (§3 — the dual-track flag lane + reserved holdout,
operator-directed 2026-07-26); companion policy ADR
[`2026-07-26-regime-candidate-flag-lane.md`](../../adr/2026-07-26-regime-candidate-flag-lane.md)
(`Proposed`) would make the same structure standing — this campaign's design is
legal under the existing per-campaign override clause regardless of that ADR's fate.
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-26 · Claude
Code (Fable 5), operator-directed.

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-26)

Worktree `supertrend-harness-baseline-dd3529`, branch
`claude/supertrend-harness-baseline-dd3529`, up to date with `origin/main` @ `a35adcd`.

- **[`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) @ `691fd48` (2026-07-25)** — W1 (`.c.0` vs `.v.0` changes bar existence; `.v.0` = TV-`1!` analogue), W4 (micro-era OOS is a reserved gate), N6 (MNQ 4× cost hurdle ≈ 3.01 bp/session for intraday constructs — different units from this campaign's per-trade hurdle, cited for lineage not reuse), N5 (D5 scar: IS +1.461 bp → OOS −0.327 bp — the window-luck failure shape §3's holdout design answers), DEAD list + F2 guard.
- **[`ops/instruments/MYM.md`](../../../ops/instruments/MYM.md) @ `691fd48` (2026-07-25)** — W1–W4 (incl. W3 vendor-refresh pin invalidation), M6 (MYM 4× Tradeify hurdle ≈ 6.57 bp/event, same lineage note), DEAD list, "MYM family K bank remains 0", the 2026-07-21 raised bar on single-instrument index-futures intraday OHLCV directional timing (this campaign is exactly that class — acknowledged, not evaded: it is characterization + flag-detection, and any promotion clears the full inherited universe correction).
- **[`core/firm_rules.py`](../../../core/firm_rules.py) @ `fd95c72` (2026-07-24)** — Tier-1 verbatim cost constants: `Tradeify: cost_per_side_usd: 0.91` (line 279, "all-in, index micros (MNQ/MYM/MES…)"), `Bulenox: 0.61` (line 91), `MFFU: 0.95` (line 373). MNQ tick 0.25 pt × $2.00/pt = $0.50; MYM tick 1.00 pt × $0.50/pt = $0.50.
- **[`lab/databento_fetch/db_fetch.py`](../../../lab/databento_fetch/db_fetch.py) @ `0439996` (2026-07-13)** — estimate/pull subcommands, `--max-cost` required on pull, `--campaign-id`/`--phase` cache scoping, `--phase discovery` hard-refuses `--end` past the IS boundary (2018-12-31), PD-1 range fail-fast, PD-2 atomic cache write.
- **[`lab/discovery/register_search.py`](../../../lab/discovery/register_search.py) @ `67cc146` (2026-07-14)** — `open` binds `--search-space-size` (K) + `--data-window` + `--hypothesis` pre-result; `--lane blind` default; `close` takes survivor p-values.
- **[`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) @ `7af4224` (2026-07-20)** — §Campaign-defaults (RATIFIED 2026-07-11; Default #3 K/V amended 2026-07-12) + the override clause this campaign's §3 uses; Stage 0–8 pipeline.
- **[`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md`](2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md) @ `df13e74` (2026-07-16)** — lineage template (override discipline, §R shape, §8 GO gate shape).
- **`discovery_manifests/*.json`** (read this session) — MNQ family banked K: `d5_nq_intraday_mom` closed K=1; `orb_mnq_intraday_breakout` **open** K=1 (counted conservatively in the DSR denominator below). MYM family banked K=0.
- **Source CSVs (fidelity anchors), manifested this session** in `core/data/tv_exports/cme/SHA256SUMS`: `ST-EH_CME_MINI_MNQ1!_2026-07-25_80e00.csv` (`04973b14…`, n=551 incl. 1 open row) and `ST-EH_CBOT_MINI_MYM1!_2026-07-25_c93ef.csv` (`076fcec3…`, n=550); span 2025-08-31 22:15 → 2026-07-24 16:45 ET; Commission column sums $0.00 (parent-session §0-A, re-verifiable via §10 hook 6).
- **Operator answers (this session, 2026-07-26):** TV chart TZ = `America/New_York`; MNQ1!/MYM1! **not back-adjusted** at export (TV default); TV slippage = 0; canonical cost model = **Tradeify**; IS/OOS resolution = **dual-track hybrid** (operator selected after a structured challenge to Default #1 — see §3).

---

## §1 — Context

ST-EH-1 sits in the instrument-first research direction (MNQ/MYM profiling). The
parent session built a Supertrend edge harness (ST-EH v0.1) to convert
signal-emitting TV indicators into exportable strategy panels, ran the 1-yr TV
panels on both micros, and found: baseline `ST(10,3)` PF 1.026/1.049, costed
avg/trade +$0.95 (MNQ) / −$0.64 (MYM) at the Tradeify RT $2.82 — **both coin flips
(P(expectancy≤0) ≈ 0.5 costed), neither near the 4× convention ($11.28/trade)**,
and MNQ gave back its entire accumulated P&L intra-panel (DD $12,877 vs peak
$12,790). Prior is LOW — raw Supertrend on liquid index futures is among the most
publicly mined constructs in existence; a cheap kill is an acceptable and likely
outcome, and the harness + 16-yr panels generalize regardless.

TV bar history caps the 15m panel at ~11 months, so the questions this campaign
answers — (a) is the 1-yr result representative of a regime-diverse 16-yr panel,
(b) does ANY pre-registered `(period × mult)` cell clear the costed hurdle with
selection effects priced — require the Databento/Python replication path
(one engine, one feed; Phase-2 fidelity gate licenses the engine).

**Premise corrections vs the archived handoff** (author had no repo access; flagged
per its own template note): tooling lives at `lab/databento_fetch/db_fetch.py` +
`lab/research_utils/{step0_battery,selection_tests,plateau_tracker}.py` (not
`scripts/`); deliverables land at `lab/analysis/harvest/st_eh_2026-07/` (no `research/`
layer exists in the 4-layer monorepo). Neither correction touches the frozen
science.

**Structural change vs the handoff (operator-directed, 2026-07-26, pre-result):**
the handoff's Phase 4/5 ran selection over the full 2010→2026 panel, unaware of the
ratified Default #1 (IS 2010→2018 tuning / 2019+ hold-out). The operator challenged
Default #1's blind spot (regime-born modern edges — e.g. ORB-MNQ-1's own
post-2020-conditional edge would be invisible to IS-only selection), and after a
structured options review selected the **dual-track hybrid** frozen in §3: ratified
promotion track unchanged + a non-promoting REGIME-CANDIDATE flag lane + a reserved
2024+ holdout that keeps a clean confirm window for any flagged cell. This
resolution happened **before any Databento pull and before any grid number was
computed** — the only results seen to date are the two 1-yr TV baselines archived
in the handoff.

---

## §2 — Frozen search universe + design (Stage-0)

| Item | Frozen value |
|---|---|
| **Instruments** | NQ/YM parents (discovery panels, 2010-06-06→) + MNQ/MYM native micros (2019-05-06→). Micro economics only (×0.1 parent→micro rescale; parent commission structures never used). |
| **Mechanism (named)** | Supertrend flip-only stop-and-reverse: ATR-banded price-level recursion; always-in-market; signal on bar close, fill next bar open. The null being tested is "the band flip carries no exploitable directional information net of costs at the 4× convention." |
| **Engine spec (frozen, verbatim from ST-EH v0.1)** | `src=hl2; atr=RMA(TR, period); up=src−mult·atr, ratcheted up when close[1]>up_prev; dn=src+mult·atr, ratcheted down when close[1]<dn_prev; trend +1 start; −1→+1 on close>dn_prev; +1→−1 on close<up_prev (prev = prior bar FINAL adjusted values, nz-seeded); no costs at signal layer.` 15m bars, ET-anchored :00/:15/:30/:45, bar-open timestamps, 24h Globex with the 17:00–18:00 ET halt excluded (no synthetic bars). |
| **Grid (fixes campaign-local K)** | ATR period ∈ {7, 10, 14, 21} × mult ∈ {2.0, 2.5, 3.0, 3.5, 4.0} = **20 cells per symbol**, hl2, RMA ATR, flip-only, one engine, one feed. Baseline cell = (10, 3). No timeframe axis, no filter axis, no price-source axis (each would be a new pre-registration). |
| **Windows (the dual-track core)** | **IS (Track-1 selection):** 2010-06-06→2018-12-31, parents. **Flag window (Track-2 selection, declared override):** 2019-05-06→2023-12-31, parents + native-micro sign check. **RESERVED HOLDOUT:** 2024-01-01→present — per-cell results in this window are **not computed and not reported** in this campaign, with exactly two allowlisted exceptions: (a) the (10,3) baseline (H1 + the Phase-2 fidelity gate need it; a disclosed 1-cell reveal), (b) Track-1 IS-survivors' confirm read (2019-05-06→present, parent + micro — confirmation is the read's stated purpose). Mechanically enforced: the grid runner hard-caps scoring at 2023-12-31; the confirm module takes an explicit allowlist. |
| **K (bound now, pre-result)** | Each cell is read on **two** selection windows (IS + flag), and both reads are selection events (each can fire a lane): 20 cells × 2 windows × 2 symbols = **80** grid trials + **4** baseline trials (2 × 1-yr TV already run, 2 × long-panel H1) = **K = 84**, split MNQ-family 42 / MYM-family 42. Campaign-local best-of-K nulls run at K=20 per symbol-window. DSR denominator (Default #2, family-cumulative): MNQ 42+2 banked (D5 closed K=1 + ORB-MNQ open K=1, counted conservatively) = **44**; MYM 42+0 = **42**. `V = 1/n` per amended Default #3. |
| **Costs (frozen)** | Tradeify (operator-selected): $0.91/side commission + 1 tick/side slippage; MNQ and MYM tick both $0.50 → **RT $2.82**, 4× hurdle **$11.28/trade**, both symbols. Bulenox ($0.61/side → RT $2.22) and MFFU ($0.95/side → RT $2.90) reported as sensitivity columns only, never gating. |
| **Data** | Databento GLBX.MDP3, `ohlcv-1m`, `.v.0` volume-lead continuous (TV-`1!` analogue per MNQ.md W1), resampled 1m→15m ET. Continuous is served **unadjusted**; long-panel signal generation runs on a locally back-adjusted series (additive panama offsets at `.v.0` roll transitions, each roll documented); the Phase-2 fidelity gate runs on the **unadjusted** series to match the operator-confirmed not-back-adjusted TV export. Cost gate: per-pull `--max-cost 5.00`, **campaign total ceiling $20.00** checked against the summed estimates before any pull (Default #6). Cache: `~/.databento_cache`, campaign-tagged `ST-EH-1`; derived 15m parquet panels SHA256-recorded in RESULTS. |
| **Fidelity gate (licenses the engine — HALT gate)** | Window 2025-08-31→2026-07-24 (warm-up from ≥2025-06-01), closed trades only, unadjusted native MNQ/MYM 15m vs the two manifested TV CSVs: closed-trade count ±2%; entry-timestamp Jaccard ≥0.95; gross profit AND gross loss each ±5%; direction agreement on matched entries ≥98%. Any miss → HALT, campaign `AMBIGUOUS`, `NEEDS_CONTEXT` to operator (roll-spanning trades reported per symbol as the expected residual source; forcing tolerances is forbidden, §5). High Jaccard is the GOAL here (replication), the opposite polarity from cross-feed independence Jaccard — do not confuse. |
| **Panel integrity** | `lab/research_utils/step0_battery.py` logic on every generated panel (entry-minute census vs 15m, session/hour coverage, DOW census, duplicates, n-bounds, span coverage) — machine-check before any metric. |

---

## §3 — Frozen gate thresholds + the declared override

Snapshot of inherited defaults; **one structural override** (marked), per the
template's own campaign-override clause.

| Gate | Frozen threshold / rule | Bound at |
|---|---|---|
| **H1 (baseline representativeness)** | `ST(10,3)` on the full 2010-06-06→present parent panel, per symbol: costed expectancy ≥ 4× RT hurdle ($11.28) AND costed bootstrap-10K 90% CI lower bound > 0. Not a search (single pre-registered config) — full-panel scoring is Default-#1-compliant. Zero-cost AND costed reported; micro-scaled dollars (×0.1); per-year + halves + thirds stationarity; native micro era reported separately. | Phase 4 |
| **Track 1 — promotion (ratified axis, unchanged)** | Cell promotable to CANDIDATE only if ALL of: (1) costed bootstrap 90% CI LB > 0 on **IS**; (2) costed point expectancy ≥ 4× hurdle on **IS**; (3) confirm: costed expectancy > 0 on parent 2019-05-06→present AND native micro same window; (4) plateau: ≥6 of available grid-adjacent neighbors costed-positive on IS, dome not cliff; (5) best-of-20 demeaned null on IS per symbol, P(best ≥ observed | zero-edge) < 0.05; (6) inherited universe correction (Default #3): DSR ≥ 0.95 at family K (44/42), V=1/n; SPA on the campaign-local return set; PBO < 0.5 via CPCV (config selection occurred — the grid is one). | Phase 6 |
| **Track 2 — REGIME-CANDIDATE flag (OVERRIDE — structural extension of Default #1)** | **Override:** cells failing Track-1 IS criteria are additionally scored on the **flag window 2019-05-06→2023-12-31** (a selection-shaped read of Default #1's hold-out era — declared here, pre-result, per the override clause). Flag fires iff, on the flag window: costed expectancy ≥ 4× hurdle AND costed 90% CI LB > 0 AND the plateau criterion AND the best-of-20 demeaned null < 0.05 (same bar as promotion, no DSR — detection, not admission). Micro-era sign must agree. **A flag NEVER promotes.** It authorizes authoring a follow-up pre-registration only: selection window 2019-05→2023-12 (already spent by the flag), confirm window = the untouched reserved holdout 2024-01→present, fresh K increment, separate operator GO. **Reason for override:** Default #1's IS-only selection is structurally blind to regime-born modern edges (the operator's challenge, 2026-07-26; live precedent: ORB-MNQ-1's post-2020-conditional edge). The reserved holdout preserves what makes the eventual confirm honest — cf. the D5 scar (window-luck: IS +1.461 → OOS −0.327 bp). Full disclosure, zero silent promotion. Companion ADR proposes this as standing policy. | Phase 6 |
| **Reserved-holdout discipline** | 2024-01-01→present per-cell numbers absent from every table, log, and artifact of this campaign except the two allowlisted reads (§2). Violation = the flag lane's follow-up confirm is void (soft contamination — the selector saw the window) → any Track-2 flag downgrades to observation-only. | All phases |
| **Block size** | From the scored return-series ACF (never `sqrt(T)`), bound at the bootstrap step, back-filled here. | Phase 6 |
| **Min-detectable disclosure (amended Default #3, pre-freeze)** | At family K=44 (MNQ) / 42 (MYM), V=1/n, DSR ≥ 0.95 requires approximately **net annualized Sharpe ≥ 3.87/√years ≈ 1.44 on the 7.2-yr confirm era** (nearly n-invariant: the per-trade floor and annualization factor cancel). Stated plainly: Track-1 promotion demands an extraordinary cell; given the §1 cohort (PF 1.03–1.05), promotion is expected UNREACHABLE and the campaign's live value is H1 adjudication + flag detection + infrastructure (§R). This is disclosure, not a complaint — the K-governed floor is the honest price of an 84-trial campaign on a heavily-mined construct. | Frozen now |
| **Cost gate (Default #6)** | Σ(6 estimates) ≤ **$20.00** before any pull; per-pull `--max-cost 5.00`; any single estimate > $5.00 → report + `NEEDS_CONTEXT`, no `--force`. | Phase 1 |
| **Decay monitor (Default #5)** | Any promoted cell ships with a CUSUM decay-monitor spec calibrated during validation; inadmissible without it. (Expected moot; binding if Track 1 fires.) | Admission |

---

## §R — Reachability (not HARD-gated in the blind lane; included per M-20)

- **R.1 — H1:** trivially reachable as a *test* (it is a measurement, not a search;
  both verdict directions are informative). Under the §1 cohort scale
  (avg/trade ≈ +$0.95 costed at 1× on MNQ), H1 is **expected FALSIFIED** — the 4×
  bar sits ~12× above the observed cohort point. This is the low prior on the
  record, not a design defect.
- **R.2 — Track-1 promotion:** under a plausible-true-STRONG world (some cell
  carries genuine net annSR ≥ 1.5 with ≥4× hurdle clearance — e.g. a slow-cell
  regime harvest at ~200 trades/yr, avg/trade ≥ $32 vs the $11.28 bar), all six
  criteria are simultaneously satisfiable: CI LB > 0 at n > 1,000 follows from the
  Sharpe scale; plateau follows from parameter-smoothness of a real band effect;
  the best-of-20 null and DSR 1.44-floor are cleared by construction of the
  hypothesized scale. Under the plausible-true-WEAK world (cohort scale), promotion
  is **UNREACHABLE — disclosed in §3**. Both worlds stated; no gate is frozen that
  cannot be passed in any plausible-true world.
- **R.3 — Track-2 flag:** on the 4.65-yr flag window at 150–550 trades/yr
  (n ≈ 700–2,550), the binding criterion is CI LB > 0, requiring avg/trade ≈
  $10–16 at a per-trade std of ~$300 — i.e. a genuine ≥4×-hurdle modern edge fires
  the flag; a marginal 1–2× one does not. Reachable under
  plausible-true-modern-edge; correctly deaf to cohort-scale noise.
- **R.4 — Fidelity gate:** the engine spec is transcribed verbatim from the
  harness that PRODUCED the two TV panels; the operator confirmed TZ/adjustment/
  slippage assumptions this session. Expected residual = roll-spanning trades
  (~4 quarterly rolls in-window) against tolerances of ±2%/0.95/±5%/98%.
  Reachable; a structural feed divergence (TV vs GLBX) would surface here as the
  designed `AMBIGUOUS`, which is the gate doing its job.

---

## §4 — Falsifiable hypotheses (binary)

Each hypothesis below is binary — a verdict is forced either way; "needs more
data" is not available (the panel is 16 years).

- **H1 (baseline representativeness):** **if** `ST(10,3)` on the 2010→present
  parent panel shows costed expectancy ≥ 4× hurdle AND bootstrap 90% CI LB > 0 for
  NQ and/or YM, **then** H1 holds (`H1-VIABLE` — proceed to a follow-up pre-reg,
  never directly to live); **otherwise H1 is FALSIFIED** (expected, per §R.1).
- **H2-T1 (grid, ratified track):** **if** ≥1 cell satisfies all six Track-1
  criteria on at least one symbol, **then** `GRID-CANDIDATE(cells…)` — route to
  Stage-7/8 + lifecycle CANDIDATE intake; **otherwise H2-T1 is FALSIFIED.**
- **H2-T2 (flag lane):** **if** ≥1 Track-1-failing cell satisfies all four flag
  criteria on the flag window with micro sign agreement, **then**
  `REGIME-FLAG(cells…)` — authorizes authoring the follow-up pre-registration
  (separate operator GO; confirm on the reserved holdout); **otherwise H2-T2 is
  FALSIFIED** and the reserved holdout is never opened per-cell.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Peeking at the reserved holdout** ("compute it anyway, just don't gate on
  it") — the whole flag-lane value IS the unread window; one look voids it
  (§3 reserved-holdout discipline).
- **Promoting a flag-lane cell directly** because its flag-window numbers look
  strong — the flag window selected it; promotion on the selecting window is the
  D5 shape.
- **Adding any filter mid-campaign** (session, DOW, EOM, min-ATR, hour-block)
  because a slice looks good — ORB-MNQ-1 §5 precedent binds; filters are a
  separate future pre-registration.
- **Widening the grid after seeing results** ("try mult 5.0") — new pre-reg with
  an explicit K increment, never an amendment.
- **Adding a timeframe axis** — out of scope; new pre-reg.
- **Mixing engines or feeds** — no TV-derived number enters any long-panel
  comparison; after the fidelity gate passes, the TV panels are historical
  context only.
- **Relaxing the DSR floor post-hoc** because ≈1.44 "looks harsh" once results
  exist — the floor is the pre-declared price of K=84 (Trap #12 /
  methodology-layer p-hacking).
- **Treating parent-era P&L as micro P&L** without the ×0.1 rescale, or skipping
  the micro-era gates.
- **Escalating to tick/MBO data "for realism"** — bars only; microstructure
  escalation requires a surviving candidate first.
- **Any pull without a prior estimate**, any hand-written `get_range` outside
  `db_fetch.py`, or `--force` past a ceiling.
- **Forcing the fidelity tolerances** when the gate misses — that is the
  plan-premise-wrong branch; escalate, do not force (`BLOCKED:
  plan-itself-wrong`).

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **H1-VIABLE** | H1 holds on ≥1 symbol (§4) | RESOLVED-positive on H1; follow-up pre-reg required before anything live-shaped; grid tracks still adjudicated independently |
| **GRID-CANDIDATE(cells…)** | ≥1 cell passes all six Track-1 criteria | RESOLVED-positive on H2-T1; Stage-7 realism → Stage-8 breadth → lifecycle CANDIDATE intake with calibrated decay monitor |
| **REGIME-FLAG(cells…)** | No Track-1 pass; ≥1 cell passes all four Track-2 criteria + micro sign | RESOLVED-flag on H2-T2; follow-up pre-registration authorized-to-author (own GO, own K, confirm = reserved holdout); no promotion from this campaign |
| **FALSIFIED-AT-COST** | H1 AND H2-T1 AND H2-T2 all falsified | Clean close (expected); manifest closed all-null; K=84 banked (MNQ 42 / MYM 42); nulls-alive ledger in RESULTS |
| **AMBIGUOUS** | Fidelity gate unresolvable, data defect (Step-0 hard fail), or reserved-holdout discipline violated | Close with the defect named; no grid verdict is quotable; re-entry requires a fresh Stage-0 |

Composite verdicts are legal (e.g. H1 FALSIFIED + REGIME-FLAG). Status returns use
`DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED(sub-case)` per the handoff §6.

---

## §7 — Run protocol

0. **Stage 0 (this file):** operator reviews — especially the §3 override row and
   the reserved-holdout allowlist — then §8 GO/NO-GO. Commit this file + the
   companion ADR (`Proposed`) + the archived handoff **before** the first pull.
1. **On GO:** `register_search open --tool st-grid --search-space-size 84
   --data-window 2010-06-06:2026-07-26 --lane blind --campaign… --hypothesis "…"
   --params <grid+windows JSON>` → then 6 × `db_fetch estimate` (NQ/YM: discovery
   phase →2019-01-01 + oos phase 2019-01-01→present, the oos leg starting
   2019-01-01 purely for RMA warm-up with scoring from 2019-05-06; MNQ/MYM: oos
   2019-05-06→present) → Σ ≤ $20 check → 6 × `pull` (`--campaign-id ST-EH-1`,
   `--phase` tagged, `--max-cost 5.00` each).
2. **Panels:** 1m→15m ET resample; `.v.0` roll transitions detected + additive
   back-adjustment (per-roll table in RESULTS); Step-0 battery on every panel;
   unadjusted variants retained for the fidelity gate.
3. **Fidelity gate (HALT):** engine vs both TV CSVs per §2 tolerances. Pass →
   engine licensed; miss → `AMBIGUOUS`, stop.
4. **Phase 4:** H1 baseline per §3 row 1.
5. **Phase 5:** grid on IS + flag windows ONLY (runner hard-capped at
   2023-12-31); all 40 symbol-cells reported on both windows, no omissions.
6. **Phase 6:** Track-1 adjudication (incl. universe correction) → Track-2
   flags for Track-1 failers → verdict per §6.
7. **Close:** `register_search close` (survivor p-values or all-null); RESULTS +
   nulls-alive ledger + roll table + session record at
   `lab/analysis/harvest/st_eh_2026-07/`; engine + tests
   (`engine.py`, `test_engine_fidelity.py`), `results/replication_gate.md`,
   `results/baseline_longpanel.csv`, `results/grid_results.csv` (80 rows: 40
   symbol-cells × 2 windows); panel SHA256s recorded.

---

## §8 — Operator GO gate (the decision)

```
§3 OVERRIDE + RESERVED-HOLDOUT REVIEWED / GO: 2026-07-26 / JA
Part 1 CONFIRMED — dual-track structure: Track-1 promotion on the ratified IS→OOS
  axis; Track-2 REGIME-CANDIDATE flag lane on 2019-05-06→2023-12-31 (declared
  selection-shaped read of the hold-out era, never promoting); reserved holdout
  2024-01-01→present unread per-cell except the two allowlisted reads. The
  operator raised the Default-#1 modern-edge challenge that produced this
  structure and selected the dual-track hybrid over both the pure ratified
  default and a modern-era-IS override.
Part 2 CONFIRMED — K=84 (dual-window reads counted as selection events; MNQ 42 /
  MYM 42) and the ≈1.44 annSR min-detectable disclosure acknowledged: Track-1
  promotion is expected UNREACHABLE at the observed cohort scale, and the
  campaign is authorized on its H1-adjudication + flag-detection + infrastructure
  value, with FALSIFIED-AT-COST the expected close.
Part 3 CONFIRMED — Tradeify cost model ($0.91/side + 1 tick ⇒ RT $2.82, 4× bar
  $11.28), $20 campaign cost ceiling, fidelity-gate HALT semantics.
Authorizes `register_search open` + the 6 estimate→pull sequence. GO signature
  consumes no K and fetches no data.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-result is git-auditable: this pre-registration's commit must PRECEDE
#    both the manifest and any RESULTS artifact (the ORB-MNQ-1 freeze-ordering convention).
git log -1 --format='%h %ci  PREREG' -- docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md
git log -1 --format='%h %ci  MANIFEST' -- discovery_manifests/st_eh_supertrend_grid.json 2>/dev/null
git log -1 --format='%h %ci  RESULTS' -- lab/analysis/harvest/st_eh_2026-07/RESULTS.md 2>/dev/null
# Expected: PREREG timestamp strictly earlier than MANIFEST and RESULTS.

# 2. K entry matches: 84 bound pre-result, family split 42/42.
grep -n "K = 84\|MNQ-family 42 / MYM-family 42" docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md

# 3. Grid completeness: 80 rows (40 symbol-cells x 2 windows), no cell dropped.
python -c "import pandas as pd; df=pd.read_csv('lab/analysis/harvest/st_eh_2026-07/results/grid_results.csv'); assert len(df)==80, len(df); print('grid OK')"

# 4. Reserved-holdout discipline: no per-cell 2024+ numbers outside the allowlist.
grep -rniE "2024|2025|2026" lab/analysis/harvest/st_eh_2026-07/results/grid_results.csv; # expect NO date-window columns past 2023-12-31

# 5. Estimate-before-pull discipline (cache + shell history are the record; manifest params carry the summed estimate).
python -c "import json,glob; m=[json.load(open(p)) for p in glob.glob('discovery_manifests/*st*eh*.json') or glob.glob('discovery_manifests/*st_eh*.json')]; print(m)"

# 6. Fidelity anchors still manifested.
grep -n "ST-EH" core/data/tv_exports/cme/SHA256SUMS   # expect 2 lines, hashes 076fcec3… / 04973b14…

# 7. Forbidden-move tripwire: no filter logic in the engine.
grep -inE "session|dayofweek|day_of_week|eom|min_atr|hour" lab/analysis/harvest/st_eh_2026-07/engine.py; # expect no matches (resample module excepted)

# 8. Companion ADR status (Proposed until operator ratifies; campaign legality does not depend on it).
grep -n "Status:" docs/adr/2026-07-26-regime-candidate-flag-lane.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- ops/instruments/MNQ.md                       # 691fd48
git log -1 --format='%h %ci' -- core/firm_rules.py                           # fd95c72
git log -1 --format='%h %ci' -- lab/databento_fetch/db_fetch.py              # 0439996
git log -1 --format='%h %ci' -- lab/discovery/register_search.py             # 67cc146

# Cost arithmetic reproduces (pure division, no data touch)
python -c "
rt = 2*0.91 + 2*0.50; print('RT=%.2f hurdle=%.2f' % (rt, 4*rt))"
# Expected: RT=2.82 hurdle=11.28

# Min-detectable floor reproduces (K=44, gamma=0.5772, DSR>=0.95, 7.2y confirm era)
python -c "
from math import sqrt, e
from statistics import NormalDist
z = NormalDist().inv_cdf
K = 44; g = 0.5772
mult = (1-g)*z(1-1/K) + g*z(1-1/(K*e))
print('SR0 mult=%.3f ann floor ~= %.2f' % (mult, (mult+1.645)/sqrt(7.2)))"
# Expected: mult ~2.22, ann floor ~1.44

# Banked-K inputs reproduce
python -c "import json; d=json.load(open('discovery_manifests/d5_nq_intraday_mom.json')); o=json.load(open('discovery_manifests/orb_mnq_intraday_breakout.json')); print('D5', d['status'], d['K'], '| ORB', o['status'], o['K'])"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-26 | Stage-0 authored — dual-track design (operator-selected after challenging Default #1), K=84 bound, Tradeify cost model + $20 ceiling frozen, engine spec + fidelity tolerances transcribed from the archived handoff, reserved holdout 2024-01-01→present declared with a two-read allowlist, min-detectable annSR ≈1.44 disclosed. Awaiting operator §8 GO. | Joshua (direction) + Claude Code (Fable 5) |
| 2026-07-26 | **§8 GO SIGNED (JA) — all three parts confirmed.** Part 1: dual-track structure (Track-1 ratified promotion / Track-2 non-promoting flag lane / reserved 2024+ holdout with a two-read allowlist). Part 2: K=84 and the ≈1.44 annSR unreachability disclosure acknowledged — campaign authorized on H1-adjudication + flag-detection + infrastructure value. Part 3: Tradeify costs, $20 ceiling, fidelity HALT semantics. Authorizes `register_search open` + the 6 estimate→pull sequence. | Joshua (GO) |
