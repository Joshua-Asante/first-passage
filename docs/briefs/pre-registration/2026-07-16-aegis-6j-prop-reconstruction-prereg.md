# Pre-registration — Aegis→6J prop reconstruction (Stage-1 TV sweep → Stage-2 solo Part A)

> ⚠ **2026-07-22:** this frozen body's "already-discharged four-firms ADR §4" premise was
> **WITHDRAWN** — see [`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md`](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md).
> §4 is undischarged (hard date 2026-11-08 unchanged). Body left frozen as written (Trap #12); this Q's own verdict is unaffected.

**Status:** `CLOSED — Stage-1 FALSIFIED` (operator accepted 2026-07-16). Frozen body
below is historical record — do not amend filters in place (Known Trap #12). Closure:
[`docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md`](../closures/2026-07-16-aegis-6j-prop-reconstruction-stage1-falsified.md).
**Prior status:** `FROZEN` (operator signed §9, 2026-07-16). No item below changes after
signature or after any Stage-1 cell result is used for selection (Known Trap #12 —
amendments require closing this pre-reg and opening a fresh one).
**Scope:** Stages **0–2** of
[`docs/superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md`](../../superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md)
@ `eaa1191` (plan of record after adversarial review fixes). Stage 3 compose is **out of
scope** here — it requires a separate Class-S candidate pre-reg after H-SOLO RESOLVED.
**Candidate class:** Class S venue/sizing reconstruction of the locked-leg **Aegis→6J**
native-futures expression (weights + sizing + EOD **fill** deadline as venue variables).
Admitted under
[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md)
(`Accepted` 2026-07-15). **Not** CFD-edge transfer; R5/P2 stay FALSIFIED.
**Aegis declaration (ADR §5, explicit):** **this artifact IS Aegis-bearing** — solo 6J
leg only at Stage 2. Mechanism core frozen to Aegis→6J v0.3 identity; free levers are
Class-S venue variables only (`max_contracts`, `risk_pct_display`, `eod_fill_deadline_et`).
**Wave-2 levers (`max_hold_bars`, narrower `entry_session`) are NOT admitted** — out of
Class S without a fresh §9 class-membership ratification.
**Gate of record (Stage 2; unchanged, cited not re-decided):**
[`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
(FROZEN 2026-07-13).
**Loop of record:** STRATEGIC.
**Feeds:** future Class-S Aegis-solo (S3) scoring → optional compose with candidate #1
MYM+MNQ; four-firms ADR §4 already discharged by candidate #1 — this pre-reg does **not**
carry discharge urgency.
**Authored:** 2026-07-16 · Cursor (operator-directed: clear pre-Step-0.1 → draft pre-reg).
**Pre-Step-0.1 checklist:** operator-cleared 2026-07-16 (incl. accepting working
`max_contracts ≤ 8` mini-equivalent ceiling for Tradeify/MFFU 100K pending any later
product-article re-verify at deploy).

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-16)

All content-read from the working tree on `main`; per-file anchors (`git log -1 --format='%h %ci'`):

- **[`docs/superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md`](../../superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md) @ `eaa1191`** —
  plan of record. F1 fill≠cutoff; selection = max mean qty; Wave-2 dropped; #1
  regime-fragile carried; windows pinned; paper degeneracy Task 0a.
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `be6dda6`** —
  Part A **bust ≤ 3.0%** + **P(pass) ≥ 50%**, Run-2, seeds **42/123/2026**, 10k×3,
  horizon 1500, `dd_protection` OFF, inactivity off; frozen $100K×4 tiers; discharge
  ≥2 firms incl. ≥1 `trailing_locking`. **Nothing here re-decides any of it.**
- **[`docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md`](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) @ `507761a`** —
  Class S admits weights/sizing as venue variables; claim = native bust-geometry;
  R5/P2 stay FALSIFIED; per-candidate pre-reg + prior-look disclosure required.
- **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) @ `6b94032`** —
  E1 flat-print **16:00 ET** (MFFU **16:10** binding; post-16:10 can DISQUALIFY);
  Tradeify consistency 40% / MFFU 50% soft; no M6J; full 6J commissions noted.
- **[`ops/instruments/6J.md`](../../../ops/instruments/6J.md) @ `fad8984`** —
  F1/F3 cutoff→fill +15m; J1 PF 2.318 / EOD Flat **60.0%** of net; J5 $45–90/contract;
  BEPAD CLOSED-FALSIFIED; ae744 PARTIALLY UNKNOWN for prop use.
- **[`lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md`](../../../lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md) @ `507761a`** —
  ae744 pick + 1R $2,912.96 (n=11); 5274c disqualified (median fallback).
- **[`lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md)**
  + **[`REGIME_GATE.md`](../../../lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/REGIME_GATE.md) @ `163b0b5`** —
  MYM+MNQ Part A DISCHARGED (Tradeify 2.65% / MFFU 2.64%); regime **GATE FAIL**
  (H1 ~4.37%; bootstrap 95th ~10.4%) — inherited compose caveat only (Stage 3).
- **[`lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md`](../../../lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md) @ `87cf980`** —
  3-leg @ Aegis 0.75% **FALSIFIED** Tradeify/MFFU **5.69%**; 1.50% calibration 17.88%.
- **`core/firm_rules.py` @ `a53ee99`** — `Tradeify_Select_100K` / `MFFU_Rapid_100K`
  trailing_locking; consistency 40/50; micro_contract_cap 80 (= 8 mini / 80 micro);
  cost comments Tradeify 6J $3.10 / MFFU 6J $2.56; `ACTIVE_FIRM="FXIFY"` untouched.
- **[`lab/analysis/aegis/aegis_6j_transfer_2026-07-05/RUNSPEC_EOD_OFF.md`](../../../lab/analysis/aegis/aegis_6j_transfer_2026-07-05/RUNSPEC_EOD_OFF.md)** —
  optional Stage-0 measurement only; not a selection cell.

---

## §1 — Context

Candidate #2 showed Aegis@0.75% in a 3-leg book fails the frozen 100K Part A ceiling
(5.69%). Candidate #1 (MYM+MNQ alone) cleared Part A but is regime-fragile. The plan
isolates Aegis: reconstruct a Tradeify/MFFU-compliant 6J expression via a frozen
sizing/EOD-fill sweep, then gate **solo** before any compose.

**Claim:** Stage-2 claims **solo Aegis-6J native-book bust-geometry** on Tradeify_Select_100K
and MFFU_Rapid_100K under the frozen survivor gate. It does **not** claim CFD-edge
preservation, does not reopen R5/P2, and does not amend locked Aegis v4.3.

**Decision driver:** without a frozen selection rule and fill-deadline semantics, a TV
sweep cannot produce a mechanical winner or an envelope-YES panel for Part A.

---

## §2 — Frozen protocol (the entire variant set)

### §2.1 Mechanism FROZEN (not on the sweep)

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
| Cap ceiling | `max_contracts ≤ 8` (working mini-equiv; operator-cleared for this pre-reg) |

### §2.2 EOD lever semantics (F1 — load-bearing)

Pine cutoff **trigger** fires on the trigger bar; **fill** lands **+15m**.

| Cell value `eod_fill_deadline_et` | Required `pine_eod_trigger_et` | Forbidden |
|---|---|---|
| **16:00** | **15:45** | Pine trigger 16:00 (→ fill 16:15 > MFFU 16:10) |
| **15:45** | **15:30** | Designing to Tradeify 16:59 |

CSV acceptance: overnight holds = 0%; **zero exit fill timestamps ≥ cell fill deadline**.

### §2.3 Paper degeneracy collapse (Task 0a — FROZEN)

Central J5 mid **$67.50**/contract @ $100K (bounds $45 / $90 noted; collapse uses mid):

| max_c | risk% | $ risk | qty @ $67.50 | Action |
|---|---:|---:|---:|---|
| 3 | 0.25 / 0.40 / 0.55 | 250–550 | → **3** | **Collapse → one profile** (label risk **0.25%**) |
| 5 | 0.25 | 250 | ~3.7 | **Keep** |
| 5 | 0.40 / 0.55 | 400–550 | → **5** | **Collapse → one profile** (label risk **0.40%**) |
| 8 | 0.25 | 250 | ~3.7 | **Keep** |
| 8 | 0.40 | 400 | ~5.9 | **Keep** |
| 8 | 0.55 | 550 | → **8** | **Keep** |

**Six unique sizing profiles × two fill deadlines = 12 Wave-1 cells** (below). No other
cells may be added after §9 signature.

### §2.4 Wave-1 cell list (COMPLETE — the only cells that may run)

| Cell ID | max_contracts | risk_pct_display | eod_fill_deadline_et | pine_eod_trigger_et |
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

Spent 3-leg weights **0.75%** and **1.50%** are **not** on this grid.

### §2.5 Windows (pinned — no runtime wiggle)

| Window | Dates | Role |
|---|---|---|
| Stage-1 selection | **2022-01-12 → 2024-12-31** | Metrics for hard filters (c)/(d) and selection |
| Stage-1 holdout | **2025-01-01 → 2026-06-30** | Hard-fail veto (e) only — never selects |
| Stage-2 MC panel | **2022-01-12 → 2026-06-30** | Solo Part A panel span (winner CSV) |

Do **not** claim 2020-01-06 start unless a verified deep export reaches it and a
**fresh** pre-reg re-declares.

### §2.6 Stage-1 selection rule (mechanical)

**Hard filters** (all required):

| ID | Filter |
|---|---|
| (a) | overnight holds = 0% |
| (a2) | every EOD exit fill timestamp ≤ cell `eod_fill_deadline_et` |
| (c) | maxDD (bar-close) ≤ **6%** on selection window |
| (d) | N ≥ **80** trades on selection window |
| (e) | holdout-window **net ≥ 0** (veto; does not select) |

**Among survivors:** select the cell with **maximum mean position quantity**.
**Tie-break (order):** lower maxDD → higher selection-window net $.
**If zero survivors:** Stage-1 **FALSIFIED** — do not invent a new lever.

**Non-selection diagnostics (log only):** best-day/net share (multi-year ≤40% will not
bind; J1-class ~9.3%); PF; expectancy(R). Early-eval consistency is gated by Run-2 at
Stage 2, not here.

### §2.7 Stage-2 solo Part A (only after Stage-1 RESOLVED)

| Item | Fixed |
|---|---|
| Book | **Solo Aegis-6J** — winner cell only; no MYM/MNQ |
| Panel | Winner CSV (new hash-pinned; documented Pine inputs — kills ae744 provenance gap) |
| Panel window | 2022-01-12 → 2026-06-30 |
| Risk / cap | Winner's `risk_pct_display` / `max_contracts` / fill deadline |
| Discharge surface | **`Tradeify_Select_100K` AND `MFFU_Rapid_100K`** (both required — H-SOLO stricter than gate's ≥2-of-4) |
| Engine | Verbatim frozen gate: Run-2, seeds 42/123/2026, 10k×3, horizon 1500, dd_protection OFF, inactivity off |
| Bulenox / BluSky | Diagnostic only |
| 1R guard | `pin_r_basis(full_stop_mean)` — **hard-fail** on FALLBACK or n<5 full-stops (5274c class) |
| Prior-look | Must disclose **all 12** Stage-1 cells + §7 rows (best-of-K honesty) |

---

## §3 — Calibration / discrimination note

The frozen 3.0% ceiling was calibrated for K≈1 candidates. Stage-1 is best-of-up-to-12.
Honesty control = full cell disclosure in the Stage-2 scoring RESULTS prior-look table.
No ceiling move. No holdout-as-selector.

---

## §4 — Falsifier (H)

**H-SWEEP:** at least one of c01–c12 clears hard filters (a)–(e); the mechanical max-qty
rule yields exactly one winner with envelope-YES (overnight 0%, fills ≤ deadline,
`DEPLOYABLE-DEFAULT-ENVELOPE: YES`).

**H-SOLO:** that winner's panel alone clears Part A (bust ≤ 3.0% + P(pass) ≥ 50%, Run-2)
on **both** `Tradeify_Select_100K` and `MFFU_Rapid_100K`.

**Revert / close:** Stage-1 FALSIFIED → close this pre-reg; next try needs a fresh pre-reg
+ operator GO. Stage-2 FALSIFIED → close the winner expression; do **not** compose; do
**not** reweight in place.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Pine EOD trigger = 16:00** (fill 16:15 / MFFU DISQUALIFY class) — F1 regression.
- **Treating envelope "16:00 flat-print" as the Pine trigger** — cutoff ≠ fill.
- **Adding Wave-2 levers** (`max_hold`, narrower `entry_session`) mid-sweep — leaves Class S.
- **Using expectancy(R) / PF to pick among sizing cells** — sizing-invariant when saturated.
- **Re-introducing 0.75% / 1.50%** because they "almost worked" in 3-leg priors.
- **Opening Stage-1 CSVs for selection before §9 signature.**
- **Adding cells after seeing results** (Trap #12).
- **Composing with MYM+MNQ inside this pre-reg** — Stage 3 needs its own Class-S pre-reg
  and must carry candidate #1's **regime-fragile** caveat.
- **Citing absolute 6J PF against R5/P2.**
- **Claiming 2020-start panel** without a verified export + fresh pre-reg.
- **Reading `compute_default_config()['bust_rate']`** for Part A (use `summarize_outcomes`).
- **Touching BE-pad / SL / TP / ATR** to rescue a cell.

---

## §6 — Gate criteria (binary)

### Stage 1 (sweep)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** | ≥1 cell clears (a)–(e); one winner by max mean qty (+ tie-breaks); Pine inputs + CSV sha256 pinned | Proceed to Stage-2 solo pre-scoring under §2.7 |
| **FALSIFIED** | Zero cells clear (a)–(e), **or** all survivors fail holdout net ≥ 0 | Close; fresh pre-reg required |
| **AMBIGUOUS** | Two cells tie on mean qty **and** both tie-breaks — mechanical rule cannot discriminate | Close AMBIGUOUS; fresh pre-reg must add one pre-declared tie-break (no post-hoc metric) |

### Stage 2 (solo Part A)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (H-SOLO) | Part A PASS on Tradeify_Select_100K **and** MFFU_Rapid_100K | Authorize Stage-3 Class-S compose pre-reg (separate artifact); rail/account still gated |
| **FALSIFIED** | Either firm fails Part A | Winner expression closes; no compose; no in-place reweight |
| **AMBIGUOUS** | Only if a frozen-gate calibration reference (if run) clears 3.0% on ≥2 tiers | Quarantine per gate §4/§6; do not claim H-SOLO |

Regime rider for Stage 2: owed only on RESOLVED, per gate §7(7); FAIL does not overturn
mechanical Part A but rides into G8 as caveat.

---

## §7 — Prior-look disclosure (complete at freeze)

| # | Date | Artifact | Numbers / note |
|---|---|---|---|
| 1 | 07-05 | 6J J1 panel / ledger | PF 2.318; EOD Flat **60.0%** of net; F1/F3 fill lag; J5 $45–90/ctr |
| 2 | 07-05 | Q-AEGIS-6J-BEPAD-1 | CLOSED-FALSIFIED — pad floor off-limits |
| 3 | 07-11 | futures3 remc 3-leg ae744 @ 1.50% | Tradeify 100K bust **17.70%** / +cons **17.88%** |
| 4 | 07-11 | bustcut 2b ae744 @ 0.75% 3-leg | 50K bust **2.02%**, Aegis attr **47.8%** |
| 5 | 07-15 | Class-S candidate #1 | Part A DISCHARGED 2.65%/2.64%; **regime GATE FAIL** H1 ~4.37% / boot ~10.4% |
| 6 | 07-15/16 | Class-S candidate #2 | 3-leg @ 0.75% Tradeify/MFFU **5.69%** FALSIFIED |
| 7 | 07-16 | This plan @ `eaa1191` | Architecture + review fixes; no TV cell results yet |

Stage-1 cell results, once run, append to the Stage-2 RESULTS prior-look table (all 12).

---

## §8 — Run protocol

### Stage 0 (baseline — measurement, not selection)

1. v0.3 prototype; `pine_eod_trigger_et=15:45` (fill target 16:00); `max_contracts=8`;
   commission $3.10; early-close ON.
2. Export → `lab/analysis/aegis/aegis_6j_prop_reconstruction_2026-07/` + hash.
3. Confirm envelope-YES before any Wave-1 cell. Optional: EOD-OFF per RUNSPEC.

### Stage 1 (operator TV)

1. §9 signed.
2. Run **exactly** c01–c12; filename encodes cell id.
3. `SWEEP_LOG.md`: N, net, maxDD, mean qty, max exit time, overnight count, best-day %
   (diagnostic), holdout net.
4. Apply §2.6 → one winner or FALSIFIED/AMBIGUOUS.
5. Pin winner Pine inputs + CSV sha256 + `DEPLOYABLE-DEFAULT-ENVELOPE: YES`.

### Stage 2 (scoring session)

1. Author/land Aegis-solo scoring driver under
   `lab/analysis/class_s_aegis_solo_scoring_YYYY-MM-DD/`.
2. G0–G8 per frozen gate; Part A on Tradeify + MFFU only for H-SOLO.
3. RESULTS header cites **this** pre-reg + `2026-07-13-prop-survivor-scoring-prereg.md`.
4. Disclose all 12 Stage-1 cells in prior-look.

---

## §9 — Operator signature (the Stage-1/2 freeze decision)

```
SIGNED / FROZEN: 2026-07-16 / JA
Authorized Stage-1 sweep + Stage-2 H-SOLO under plan 2026-07-16-aegis-6j-prop-reconstruction
and Class-S ADR 2026-07-14.
Cell list c01–c12 + selection rule §2.6 fixed as drafted.
No Stage-1 selection and no Stage-2 G4 cell before this block is filled.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Signature before selection
grep -n "SIGNED / FROZEN:" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md

# 2. Fill≠cutoff pinned; Pine 16:00 forbidden
grep -n "pine_eod_trigger_et\|15:45\|FORBIDDEN\|fill 16:15" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md

# 3. Exactly 12 cells; spent weights not on grid as free cells
grep -E "^\| c[0-9]{2} " docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md | wc -l
# expect 12

# 4. Wave-2 excluded
grep -n "not a free lever\|Wave-2" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md

# 5. Windows pinned
grep -n "2022-01-12 → 2024-12-31\|2025-01-01 → 2026-06-30\|2022-01-12 → 2026-06-30" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md

# 6. Selection = max mean qty
grep -n "maximum mean position quantity" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md

# 7. Plan of record + regime caveat cited
grep -n "eaa1191\|regime-fragile\|4.37" docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md

# 8. No Stage-2 RESULTS before signature (pre-run)
ls lab/analysis/class_s_aegis_solo_scoring_* 2>/dev/null && echo "UNEXPECTED early scoring dir" || echo "OK: no solo scoring yet"
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md --type brief

git log -1 --format="%h %ci" -- docs/superpowers/plans/2026-07-16-aegis-6j-prop-reconstruction.md
git log -1 --format="%h %ci" -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
git log -1 --format="%h %ci" -- docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md
git log -1 --format="%h %ci" -- ops/instruments/6J.md
git log -1 --format="%h %ci" -- lab/archive/class_s_candidate2_scoring_2026-07-15/RESULTS.md

grep -n "5.69\|2.65\|2.64\|47.8\|60.0" \
  docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-prereg.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Authored PROPOSED — Stage-1 12-cell collapsed grid + Stage-2 H-SOLO; awaiting §9 | Cursor (operator-directed) |
| 2026-07-16 | §9 signed → `FROZEN`; Stage-0 baseline export authorized | JA (operator) + Cursor |
| 2026-07-16 | Stage-1 H-SWEEP **FALSIFIED** (sel N 73–74 < 80 all cells); operator accepted close; Stage-2 not run | JA (operator) + Cursor |
