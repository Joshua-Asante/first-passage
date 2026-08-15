# Pre-registration — Aegis→6J prop reconstruction **v2** (window-realigned Stage-1 re-slice → Stage-2 solo Part A)

> ⚠ **2026-07-22:** this frozen body's "already-discharged four-firms ADR §4" premise was
> **WITHDRAWN** — see [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> §4 is undischarged (hard date 2026-11-08 unchanged). Body left frozen as written (Trap #12); this Q's own verdict is unaffected.

**Status:** `FROZEN` (operator §9 signed 2026-07-16 / JA — approved in-session). Stage-1-v2
re-slice + Stage-2 H-SOLO authorized. Frozen body below is the record — no in-place amendment
(Known Trap #12); any change closes this pre-reg and opens a fresh one.
**Supersedes-relationship:** does **not** amend or reopen the CLOSED v1 pre-reg
[`2026-07-16-aegis-6j-prop-reconstruction-prereg.md`](2026-07-16-aegis-6j-prop-reconstruction-prereg.md)
(`CLOSED — Stage-1 FALSIFIED`) — that closure **stands, byte-unchanged** (Known Trap #12:
no in-place amendment). This is the sanctioned **close-and-reopen-fresh** route: a *new*
pre-reg correcting a single pre-registration defect (a gate frozen unreachable on the
window it gated). Prior closure:
[`docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md`](../closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md).
Adjudication basis: FRESH-PREREG-OK — **window realignment, not gate-lowering**
(operator adjudication 2026-07-16; the license is the reachability defect, not the near-miss).
**Scope:** Stages **0–2** of
[`docs/superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md`](../../superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md)
@ `eaa1191` (plan of record, unchanged). Stage-3 compose out of scope (separate Class-S
pre-reg after H-SOLO RESOLVED).
**Candidate class:** Class S venue/sizing reconstruction of the locked-leg **Aegis→6J**
native-futures expression (weights + sizing + EOD **fill** deadline as venue variables).
Admitted under
[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md)
(`Accepted` 2026-07-15). **Not** CFD-edge transfer; R5/P2 stay FALSIFIED.
**Aegis declaration (ADR §5, explicit):** **this artifact IS Aegis-bearing** — solo 6J leg
only at Stage 2. Mechanism core frozen to Aegis→6J v0.3 identity; free levers remain the
Class-S venue variables only (`max_contracts`, `risk_pct_display`, `eod_fill_deadline_et`).
**Wave-2 levers (`max_hold_bars`, narrower `entry_session`) are NOT admitted** — out of
Class S without a fresh §9 class-membership ratification.
**The single change from v1:** the Stage-1 **selection/holdout window boundary** (§2.5).
Everything else — mechanism, EOD semantics, degeneracy collapse, the 12-cell grid, the
selection rule, the Stage-2 gate engine — re-freezes **byte-identical** to v1.
**Gate of record (Stage 2; unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
(FROZEN 2026-07-13).
**Loop of record:** STRATEGIC.
**Feeds:** future Class-S Aegis-solo (S3) scoring → optional compose with candidate #1
MYM+MNQ; four-firms ADR §4 already discharged by candidate #1 — this pre-reg does **not**
carry discharge urgency (no deadline pressures the retry).
**Authored:** 2026-07-16 · Claude Code (operator-directed: adjudicate near-miss → draft
window-realigned fresh pre-reg).

---

## §0 — Rule-0 reads (verified this session 2026-07-16, byte-exact @ `c6d72b7`)

This pre-reg **re-decides no production constant**. It inherits the frozen protocol of the
CLOSED v1 pre-reg and changes only the Stage-1 window boundary; §0 therefore anchors (i) the
v1 close and its pinned data (read byte-exact this session), (ii) the **reachability
recomputation** on the realigned window (the load-bearing new fact), and (iii) the inherited
v1 §0 production reads, cited unchanged.

**(i) Read byte-exact this session, `git show c6d72b7:<path>`:**

- **[`docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md`](../closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md)** —
  v1 verdict FALSIFIED; binding fail = (d) sel N≥80 on 2022-01-12→2024-12-31 (73–74);
  "Full-span N is 129–130 (Stage-0's N≥80 used full span; Wave-1 (d) does not)."
- **[`2026-07-16-aegis-6j-prop-reconstruction-prereg.md`](2026-07-16-aegis-6j-prop-reconstruction-prereg.md)** (v1, CLOSED) —
  §2.1–2.7 frozen protocol; §2.5 v1 windows; §2.6 hard filters (a)–(e); §2.7 Stage-2.
- **[`lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md`](../../../lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/SWEEP_LOG.md)** —
  per-cell table; all 12 `Y/Y/Y/N/Y` (only (d) fails); operator-confirmed degeneracies
  c02≡c04 / c05≡c06 / c11≡c12 → 9 unique panels.
- **[`lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_metrics.json`](../../../lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/wave1_metrics.json)** —
  12 records; `PASS_all`=0; `sel_n`∈{73,74}; `n_full`∈{129,130}; per-cell
  `PASS_a/a2/c/e`=True, `PASS_d`=False (verified programmatically).
- **`.../WAVE1_SHA256SUMS`** + the **9 unique pinned CSVs** (`c01…c12`) — the Stage-1
  re-slice inputs; sha256 pins are the integrity anchor for Stage-1-v2 (no new export).
- **`.../stage0_baseline_check.py`** — metric/slice semantics mirrored by the re-slice
  (exit-based counts; `Type` startswith "Exit"; `dt`=`Date and time`).

**(ii) Reachability recomputation (this session; the check v1 lacked).** Slicer validated
against the pins — reproduces `sel_n`∈{73,74} on the v1 window and reconciles `n_full`
(see note). On the **realigned** selection window **2022-01-12 → 2025-06-30**:

| Quantity | Value (all 12 cells) | vs bar |
|---|---|---|
| Realigned **sel N** | **94–95** (min 94; near cell-invariant) | (d) N≥80 → **reachable, +14 headroom** |
| Realigned **holdout N** (2025-07-01→2026-06-30) | **33** | ample for a net≥0 veto |
| v1 sel N (validation, →2024-12-31) | 73–74 | reproduces pins exactly ✓ |

**`n_full` note (honesty):** the pinned CSVs export through **2026-07-15**; `n_full`∈{129,130}
counts the whole file, incl. exactly **2** small-loss exits dated 2026-07-01 and 2026-07-15
that fall **outside** the declared Stage-2 panel end (2026-06-30). Date-bounded to
2026-06-30 the full span is 127–128; both figures reconcile (Δ=2 tail exits). All v2
windows are date-bounded and exclude that tail. This does not affect the falsification
(which was about sel N) nor the realigned reachability.

**(iii) Inherited v1 §0 production reads — cited UNCHANGED, not re-decided here.** The v1
§0 anchored these @ SHAs; v2 alters none of them. See v1 pre-reg §0 for the full list. The
load-bearing inherited constants this pre-reg *relies on structurally* (Stage-2 engine):
survivor gate [`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
@ `be6dda6` — Part A **bust ≤ 3.0%** + **P(pass) ≥ 50%**, Run-2, seeds **42/123/2026**,
10k×3, horizon 1500, `dd_protection` OFF, inactivity off, $100K×4 tiers;
`Tradeify_Select_100K` / `MFFU_Rapid_100K` trailing_locking; `ACTIVE_FIRM="FXIFY"` untouched.
**Nothing in v2 re-decides any of it.**

---

## §1 — Context

**What v1 established, and the defect.** v1's frozen 12-cell TV sweep produced clean
exports (overnight 0%, fills ≤ deadline, sel maxDD 0.49–1.24% ≪ 6%, holdout net all
positive). Every **substantive** hard filter passed on all 12 cells. The **only** failing
filter was **(d) N≥80**, applied to the Stage-1 *selection sub-window* 2022-01-12→2024-12-31,
which structurally holds only ~74 Aegis→6J exits. That N≥80 bar was inherited from Stage-0,
which cleared it on the **full span** (N=130); it was pinned onto the ~3-year selection
sub-window **without a reachability check** (v1 plan L178 states the gate with no
derivation). The bar was therefore **unreachable by construction** — cell-invariant at 73–74
regardless of any sizing/fill choice. The falsification is attributable to a
**gate-window mismatch**, not to any weakness of the candidate. (Lesson:
`gate_reachability_preregistration` — gates must be reachability-checked before freeze.)

**The v2 fix — realign the window, keep the bar.** v2 corrects the mismatch by moving the
selection/holdout boundary to a **principled fixed 12-month OOS holdout**: selection =
all data through **2025-06-30**, holdout = the final **12 months** 2025-07-01→2026-06-30.
On that window N≥80 is honestly reachable (**sel N 94–95, +14 headroom**; §0(ii)) — chosen
as a standard OOS length, **not tuned to just-clear 80** (it clears by 14–15). **N≥80 is
retained, never lowered** (retaining the inherited floor is the anti-p-hacking move; lowering
it to 74 would be selecting the gate on the observed data).

**No new market data.** The pinned Wave-1 CSVs are **full-span** exports (through 2026-07-15).
Stage-1-v2 is therefore a **pure offline re-slice** of the 9 unique pinned CSVs on the
realigned windows — **no TV re-export, no new Pine run**. Cheap, deterministic, and pinned
by `WAVE1_SHA256SUMS`.

**Claim (unchanged from v1):** Stage-2 claims **solo Aegis-6J native-book bust-geometry**
on `Tradeify_Select_100K` and `MFFU_Rapid_100K` under the frozen survivor gate. It does
**not** claim CFD-edge preservation, does not reopen R5/P2, does not amend locked Aegis v4.3.

---

## §2 — Frozen protocol

### §2.1 Mechanism FROZEN (not on the sweep) — **unchanged from v1**

| Item | Fixed |
|---|---|
| Signal identity | Aegis→6J v0.3 mean-reversion / spot-inversion path |
| BE mechanic | v0.3 default — **no** pad floor (BEPAD FALSIFIED) |
| `max_hold_bars` | v0.3 default — **not** a free lever |
| `entry_session` | v0.3 default — **not** a free lever |
| Locked CFD Aegis v4.3 | untouched |
| Symbol / TF | `CME:6J1!` 15m, adjust-for-contract-changes ON |
| Early-close calendar | ON (F3) |
| TV commission baseline | Tradeify **$3.10**/side (note MFFU $2.56; do not swap mid-sweep) |
| Cap ceiling | `max_contracts ≤ 8` (working mini-equiv; operator-cleared) |

### §2.2 EOD lever semantics (F1 — load-bearing) — **unchanged from v1**

Pine cutoff **trigger** fires on the trigger bar; **fill** lands **+15m**.

| Cell `eod_fill_deadline_et` | Required `pine_eod_trigger_et` | Forbidden |
|---|---|---|
| **16:00** | **15:45** | Pine trigger 16:00 (→ fill 16:15 > MFFU 16:10) |
| **15:45** | **15:30** | Designing to Tradeify 16:59 |

The re-slice inherits each pinned CSV's fill semantics verbatim (baked into the export).

### §2.3 Paper degeneracy collapse — **unchanged from v1**

Six unique sizing profiles × two fill deadlines = 12 labels; operator-confirmed byte-identical
collapses **c02≡c04 / c05≡c06 / c11≡c12** ⇒ **9 unique panels**. No cell may be added.

### §2.4 Wave-1 cell list (the only cells that may re-slice) — **unchanged from v1**

| Cell | max_contracts | risk_pct_display | eod_fill_deadline_et | pine_eod_trigger_et |
|---|---:|---:|---|---|
| c01 | 3 | 0.25% | 16:00 | 15:45 |
| c02 | 5 | 0.25% | 16:00 | 15:45 |
| c03 | 5 | 0.40% | 16:00 | 15:45 |
| c04 | 8 | 0.25% | 16:00 | 15:45 |
| c05 | 8 | 0.40% | 16:00 | 15:45 |
| c06 | 8 | 0.55% | 16:00 | 15:45 |
| c07 | 3 | 0.25% | 15:45 | 15:30 |
| c08 | 5 | 0.25% | 15:45 | 15:30 |
| c09 | 5 | 0.40% | 15:45 | 15:30 |
| c10 | 8 | 0.25% | 15:45 | 15:30 |
| c11 | 8 | 0.40% | 15:45 | 15:30 |
| c12 | 8 | 0.55% | 15:45 | 15:30 |

Spent 3-leg weights **0.75%** and **1.50%** are **not** on this grid. Inputs re-slice the
**existing pinned CSVs** — no re-export.

### §2.5 Windows (pinned — **THE ONLY CHANGE vs v1**)

| Window | v1 (CLOSED) | **v2 (this pre-reg)** | Role |
|---|---|---|---|
| Stage-1 selection | 2022-01-12 → 2024-12-31 | **2022-01-12 → 2025-06-30** | Metrics for hard filters (c)/(d) + selection |
| Stage-1 holdout | 2025-01-01 → 2026-06-30 | **2025-07-01 → 2026-06-30** | Hard-fail veto (e) only — never selects |
| Stage-2 MC panel | 2022-01-12 → 2026-06-30 | **2022-01-12 → 2026-06-30** (unchanged) | Solo Part A panel span (winner CSV) |

**Boundary rationale (pre-committed, not tuned):** the holdout is a **fixed final 12-month
OOS** window (a standard OOS length chosen independent of the N target); the selection
window is "all data minus that 12 months." §0(ii) confirms this yields **sel N 94–95 ≥ 80**
with +14 headroom — reachable, not threshold-tuned. Do **not** claim a 2020-01-06 start
(no verified deep export). The 2 post-2026-06-30 tail exits (§0 note) fall outside every
v2 window by the 2026-06-30 bound.

### §2.5b Reachability attestation (the check v1 lacked — binds at freeze)

Frozen at signature: on the §2.5 realigned selection window, **every** cell's exit count is
**≥ 80** (measured 94–95, §0(ii); slicer validated against the pins). If a re-run of the
frozen re-slice shows any cell < 80 on this window, that is a tooling/pin regression, **not**
a licence to move the boundary — halt and reconcile against `WAVE1_SHA256SUMS`.

### §2.6 Stage-1 selection rule (mechanical) — **unchanged from v1**

**Hard filters** (all required, evaluated on the §2.5 v2 windows):

| ID | Filter |
|---|---|
| (a) | overnight holds = 0% |
| (a2) | every EOD exit fill timestamp ≤ cell `eod_fill_deadline_et` |
| (c) | sel maxDD (bar-close) ≤ **6%** on selection window |
| (d) | sel N ≥ **80** trades on selection window *(now reachable — §2.5b)* |
| (e) | holdout-window **net ≥ 0** (veto; does not select) |

**Among survivors:** select the cell with **maximum mean position quantity**.
**Tie-break (order):** lower sel maxDD → higher selection-window net $.
**If zero survivors:** Stage-1 **FALSIFIED** — do not invent a new lever, do not move the
window again.

**Non-selection diagnostics (log only):** best-day/net share; PF; expectancy(R).

### §2.7 Stage-2 solo Part A (only after Stage-1 RESOLVED) — **unchanged from v1**

| Item | Fixed |
|---|---|
| Book | **Solo Aegis-6J** — winner cell only; no MYM/MNQ |
| Panel | Winner CSV (hash-pinned; documented Pine inputs), sliced to panel window |
| Panel window | 2022-01-12 → 2026-06-30 (2 tail exits excluded by bound; immaterial to MC) |
| Risk / cap | Winner's `risk_pct_display` / `max_contracts` / fill deadline |
| Discharge surface | **`Tradeify_Select_100K` AND `MFFU_Rapid_100K`** (both required — H-SOLO stricter than gate's ≥2-of-4) |
| Engine | Verbatim frozen gate: Run-2, seeds 42/123/2026, 10k×3, horizon 1500, dd_protection OFF, inactivity off |
| Bulenox / BluSky | Diagnostic only |
| 1R guard | `pin_r_basis(full_stop_mean)` — **hard-fail** on FALLBACK or n<5 full-stops (5274c class) |
| Prior-look | Disclose **all 12** Stage-1 cells + **v1 FALSIFIED close** + §7 rows (best-of-K honesty) |

---

## §3 — Calibration / discrimination note — **unchanged from v1**

The frozen 3.0% ceiling was calibrated for K≈1. Stage-1 is best-of-up-to-12 (same 12 cells
as v1, re-sliced — **not** a fresh 12 on top of v1: K is not doubled, it is the same K
re-evaluated on a corrected window; disclosed in §7). Honesty control = full cell +
v1-close disclosure in the Stage-2 RESULTS prior-look. No ceiling move. No holdout-as-selector.

---

## §4 — Falsifier (H)

**H-SWEEP-v2:** on the §2.5 realigned windows, at least one of c01–c12 clears hard filters
(a)–(e); the mechanical max-mean-qty rule yields exactly one winner with envelope-YES
(overnight 0%, fills ≤ deadline, `DEPLOYABLE-DEFAULT-ENVELOPE: YES`).

**H-SOLO (unchanged):** that winner's panel alone clears Part A (bust ≤ 3.0% + P(pass) ≥ 50%,
Run-2) on **both** `Tradeify_Select_100K` and `MFFU_Rapid_100K`.

**Revert / close:**
- Stage-1-v2 **FALSIFIED** if (x) **any** cell reaches the selection rule but zero clear
  (a)–(e), **or** (y) all survivors fail holdout net ≥ 0, **or** (z) the realigned selection
  window unexpectedly yields sel N < 80 on all cells (cadence genuinely insufficient — **STOP;
  do not move the boundary a third time**; the instrument's trade cadence cannot support this
  selection statistic and the H-SWEEP approach retires).
  → Close **this** pre-reg; any further try needs another fresh pre-reg + operator GO.
- Stage-2 FALSIFIED → close the winner expression; do **not** compose; do **not** reweight
  in place.

---

## §5 — Forbidden moves (each genuinely tempting; ★ = new-in-v2)

- ★ **Moving the selection/holdout boundary again to chase N or a survivor.** The boundary is
  fixed at a principled 12-month OOS (§2.5). One realignment for a reachability defect is the
  whole licence; a second move is boundary-shopping / p-hacking.
- ★ **Lowering N≥80 (e.g., to 74) "because it was close."** The near-miss earns nothing
  (adjudication: NO-EXCEPTION on proximity). N≥80 is retained, not lowered.
- ★ **Re-exporting the cells from TV with any changed Pine input.** Stage-1-v2 is a re-slice
  of the **existing pinned CSVs** only; a fresh export is a new experiment (new K, new pins).
- ★ **Treating H1-2025 — veto-only in v1, now selection data — as pre-blessed.** It was only
  ever checked for net≥0 (which passed); its maxDD/mean-qty were never used to select. Disclose
  (§7); do not lean on the prior look.
- ★ **Tuning to the known max-qty winner.** The selection is max-mean-qty = sizing-driven and
  window-invariant; the leading cells were visible in v1's SWEEP_LOG (c05/c06 sel meanQ 4.68).
  The re-slice must run the rule mechanically, not back-fill the "expected" winner.
- **Pine EOD trigger = 16:00** (fill 16:15 / MFFU DISQUALIFY class) — F1 regression.
- **Treating envelope "16:00 flat-print" as the Pine trigger** — cutoff ≠ fill.
- **Adding Wave-2 levers** (`max_hold`, narrower `entry_session`) — leaves Class S.
- **Using expectancy(R) / PF to pick among sizing cells** — sizing-invariant when saturated.
- **Re-introducing 0.75% / 1.50%** because they "almost worked" in 3-leg priors.
- **Applying the selection rule before §9 signature.**
- **Composing with MYM+MNQ inside this pre-reg** — Stage 3 needs its own Class-S pre-reg and
  must carry candidate #1's **regime-fragile** caveat.
- **Reading `compute_default_config()['bust_rate']`** for Part A (use `summarize_outcomes`).
- **Touching BE-pad / SL / TP / ATR** to rescue a cell.

---

## §6 — Gate criteria (binary)

### Stage 1-v2 (re-slice)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** | ≥1 cell clears (a)–(e) on §2.5 windows; one winner by max mean qty (+ tie-breaks); winner Pine inputs + CSV sha256 pinned | Proceed to Stage-2 solo pre-scoring under §2.7 |
| **FALSIFIED** | Zero cells clear (a)–(e), **or** all survivors fail holdout net ≥ 0, **or** all cells sel N < 80 on the realigned window (§4z — STOP) | Close; any retry needs another fresh pre-reg |
| **AMBIGUOUS** | Two cells tie on mean qty **and** both tie-breaks | Close AMBIGUOUS; fresh pre-reg must add one pre-declared tie-break (no post-hoc metric) |

### Stage 2 (solo Part A) — **unchanged from v1**

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (H-SOLO) | Part A PASS on Tradeify_Select_100K **and** MFFU_Rapid_100K | Authorize Stage-3 Class-S compose pre-reg (separate artifact); rail/account still gated |
| **FALSIFIED** | Either firm fails Part A | Winner expression closes; no compose; no in-place reweight |
| **AMBIGUOUS** | Only if a frozen-gate calibration reference (if run) clears 3.0% on ≥2 tiers | Quarantine per gate §4/§6; do not claim H-SOLO |

Regime rider for Stage 2: owed only on RESOLVED, per gate §7(7); FAIL does not overturn
mechanical Part A but rides into G8 as caveat (candidate #1 regime-fragile inheritance for
any later compose).

---

## §7 — Prior-look disclosure (complete at freeze)

**Best-of-K honesty:** K is the **same 12 cells** as v1, re-evaluated on a corrected window
(not a fresh 12). The v1 FALSIFIED close and the full v1 cell table are disclosed; the
Stage-2 RESULTS prior-look must reproduce all 12 rows **plus** the v1 close **plus** this
window-realignment provenance.

| # | Date | Artifact | Numbers / note |
|---|---|---|---|
| 1 | 07-05 | 6J J1 panel / ledger | PF 2.318; EOD Flat **60.0%** of net; F1/F3 fill lag; J5 $45–90/ctr |
| 2 | 07-05 | Q-AEGIS-6J-BEPAD-1 | CLOSED-FALSIFIED — pad floor off-limits |
| 3 | 07-11 | futures3 remc 3-leg ae744 @ 1.50% | Tradeify 100K bust **17.70%** / +cons **17.88%** |
| 4 | 07-11 | bustcut 2b ae744 @ 0.75% 3-leg | 50K bust **2.02%**, Aegis attr **47.8%** |
| 5 | 07-15 | Class-S candidate #1 | Part A DISCHARGED 2.65%/2.64%; **regime GATE FAIL** H1 ~4.37% / boot ~10.4% |
| 6 | 07-15/16 | Class-S candidate #2 | 3-leg @ 0.75% Tradeify/MFFU **5.69%** FALSIFIED |
| 7 | 07-16 | **v1 Stage-1 H-SWEEP** | **FALSIFIED** — all 12 cells (a)(a2)(c)(e) PASS, **(d) sel N 73–74 < 80** on 2022-01-12→2024-12-31; degeneracies c02≡c04/c05≡c06/c11≡c12 |
| 8 | 07-16 | **v2 reachability recompute** | realigned sel window →2025-06-30 gives **sel N 94–95 ≥ 80**; holdout N 33; slicer reproduces v1 pins {73,74} |
| 9 | 07-16 | **H1-2025 boundary shift** | 2025-01-01→2025-06-30 moves from v1 veto-holdout into v2 selection; in v1 it was net≥0-veto-only (all cells passed), never a selector |

Stage-1-v2 cell results, once run, append to the Stage-2 RESULTS prior-look (all 12 + rows 7–9).

---

## §8 — Run protocol

### Stage 0 (baseline) — already ENVELOPE-YES (v1)

Stage-0 baseline `68f0e` stands (overnight 0%, fills ≤16:00, max qty 8, full-span
envelope-YES). No re-run.

### Stage 1-v2 (offline re-slice — no TV)

1. §9 signed.
2. Confirm the 9 unique CSVs match `WAVE1_SHA256SUMS` (`sha256sum -c` / `Get-FileHash`).
3. Author a re-slice driver under `lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/`
   (e.g. `wave1_reslice_v2.py`) that, per pinned CSV, computes on the **§2.5 v2 windows** the
   same metrics as v1's `wave1_metrics.json` (exit-based, `stage0_baseline_check.py`
   semantics): sel N, sel maxDD, sel mean qty, sel net, holdout net, overnight, max exit time.
4. Apply §2.6 → one winner or FALSIFIED/AMBIGUOUS. Write `wave1_v2_metrics.json` +
   `SWEEP_LOG_v2.md`; the re-slice reads only pinned bytes (record input sha256s).
5. Pin winner Pine inputs + winner CSV sha256 + `DEPLOYABLE-DEFAULT-ENVELOPE: YES`.

### Stage 2 (scoring session) — **unchanged from v1**

1. Author/land Aegis-solo scoring driver under `lab/analysis/class_s_aegis_solo_scoring_YYYY-MM-DD/`.
2. G0–G8 per frozen gate; Part A on Tradeify + MFFU only for H-SOLO.
3. RESULTS header cites **this v2** pre-reg + `2026-07-13-prop-survivor-scoring-prereg.md` + the v1 close.
4. Disclose all 12 Stage-1 cells + prior-look rows 7–9.

---

## §9 — Operator signature (the Stage-1-v2 / Stage-2 freeze decision)

```
SIGNED / FROZEN: 2026-07-16 / JA          (operator-approved in-session)
Authorized Stage-1-v2 re-slice + Stage-2 H-SOLO under plan 2026-07-16-aegis-6j-prop-reconstruction
and Class-S ADR 2026-07-14. Window realignment §2.5 (fixed 12-month OOS holdout) accepted;
N≥80 retained (reachable per §2.5b). Cell list c01–c12 + selection rule §2.6 fixed as drafted.
No Stage-1 selection and no Stage-2 G4 cell before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature before selection
grep -n "SIGNED / FROZEN:" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md

# 2. v2 windows pinned; v1 windows NOT reused as selection
grep -n "2022-01-12 → 2025-06-30\|2025-07-01 → 2026-06-30\|2022-01-12 → 2026-06-30" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md

# 3. N≥80 retained (NOT lowered)
grep -n "N ≥ \*\*80\|N≥80\|retained, never lowered" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md

# 4. Reachability attestation present (sel N 94–95)
grep -n "94–95\|reachable, +14\|§2.5b" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md

# 5. Re-slice-not-re-export discipline
grep -n "offline re-slice\|no TV re-export\|WAVE1_SHA256SUMS" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md

# 6. Reachability reproduces (run against the pins; expect sel≥80 all cells, v1 pins {73,74})
python - <<'PY'
import glob, pandas as pd
from datetime import date
S=date(2022,1,12); B2=date(2024,12,31); B_V2=date(2025,6,30)
for p in sorted(glob.glob("lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/c0*_*.csv")
              + glob.glob("lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/c1*_*.csv")):
    df=pd.read_csv(p, encoding="utf-8-sig"); df["d"]=pd.to_datetime(df["Date and time"]).dt.date
    ex=df[df["Type"].str.startswith("Exit")]
    v1=int(((ex["d"]>=S)&(ex["d"]<=B2)).sum()); v2=int(((ex["d"]>=S)&(ex["d"]<=B_V2)).sum())
    print(p.split("/")[-1][:3], "v1_sel", v1, "v2_sel", v2, "OK" if (v1 in (73,74) and v2>=80) else "CHECK")
PY

# 7. v1 close stands (this pre-reg does not amend it)
grep -n "does \*\*not\*\* amend or reopen\|closure \*\*stands\|Known Trap #12" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md --type brief

# Reachability + pin reproduction (audit hook #6)
sha256sum -c lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/WAVE1_SHA256SUMS

# v1 close + closed pre-reg unchanged (byte)
git log -1 --format="%h %ci" -- docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Authored PROPOSED — v2 window-realigned fresh pre-reg (single change: §2.5 selection/holdout boundary → fixed 12-month OOS; N≥80 retained, reachability-attested sel N 94–95); re-slice of v1 pinned CSVs | Claude Code (operator-directed) |
| 2026-07-16 | §9 signed → `FROZEN`; Stage-1-v2 re-slice + Stage-2 H-SOLO authorized; `wave1_reslice_v2.py` driver stubbed + validated against v1 pins | JA (operator, in-session) + Claude Code |
| 2026-07-16 | Stage-1-v2 ran (offline re-slice): **12/12 clear (a)–(e)**; max mean qty tied c05≡c06 (byte-identical) → **AMBIGUOUS** (§6). Resolved by fresh v2.1 tie-break pre-reg → winner **c05** (does not amend this frozen body — Trap #12) | JA (operator) + Claude Code |
