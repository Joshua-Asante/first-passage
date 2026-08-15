# Verdict pre-registration — Q-SFRISK-1 (successor self-funded risk framework)

**Status:** `NUMERIC FROZEN` (2026-07-14 — F1/F3/F4 operator-confirmed via "confirm T1"; F2 deferred)
**Pre-registered:** 2026-07-14 (question architecture + §6 table), **BEFORE** any successor-semantics MC.
**Parent brief:** [`docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md`](../Q-SFRISK-1-successor-self-funded-risk-framework.md)
**Owning ADR (completion falsifier):** [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../../adr/2026-07-11-challenge-era-claims-rescope.md) §4 / §5
**Instrument (reference, not yet run under successor bars):** `lab/analysis/regime/decompound_remc_2026-06-07/` + [`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md)

---

## What is frozen now (architecture)

1. **Question (symptom form):** After challenge-era P(pass) was retired, what is the cost of operating with no live self-funded risk claim, and what falsifiable claim-set architecture can replace P(pass) for Aegis→M6J go-live design?
2. **Claim-set dimensions (named, thresholds not invented):**
   - Operator max-DD line (breach definition)
   - Time-under-water tolerance
   - Withdrawal / reset model (decompound +5%/$200K-reset is the reference *instrument*, not a frozen answer)
3. **Hypothesis H-SFRISK-1:** a jointly specified triple evaluated on decompound-remc with **both regime halves required to clear** yields a binary go-live-admissible vs unreachable outcome (see parent §4).
4. **§6 verdict table** — copied from the parent brief (RESOLVED / FALSIFIED / AMBIGUOUS-HOLD triggers).

---

## Phase-0 numeric freeze — CONFIRMED 2026-07-14

| Field | Status | Rule |
|---|---|---|
| Max-DD breach bar | **CONFIRMED** — p99 max-DD ≤ 10% per regime half | Agent-proposed, operator-confirmed; rescope ADR §5 |
| Time-under-water bar | **DEFERRED** — not part of this freeze (no producing code in the instrument) | Operator scoped this freeze to F1/F3/F4 only; re-openable via a fresh amendment |
| Withdrawal / reset parameters | **CONFIRMED** — ADOPT +5% / $200K base / reset-to-base (banded) | Documented production default (`decompound.py`), adopted as-is |
| Operational impracticality bar | **CONFIRMED** — median business-days-to-first-$210K-skim > 252 bd | Agent-proposed, operator-confirmed |
| Candidate triple grid | **CONFIRMED** — single triple T1 (3-dimension: F1 + F3 + F4; F2 absent) | See grid below |

**Phase-0 amendment procedure — EXECUTED 2026-07-14.** Numeric table filled, status bumped to `NUMERIC FROZEN`, this file committed alone. Analysis (Phase 1) may now proceed against T1 — as a **separate, not-yet-taken** step (not part of this freeze).

---

## Phase-0 numeric amendment — CONFIRMED 2026-07-14

> **These are Joshua's risk-tolerance numbers.** Nobody else declares them (rescope ADR §5; parent brief §5). F1 and F4 were agent-proposed (reasoning retained below for audit) and **operator-confirmed 2026-07-14** via "confirm T1." F3 is the documented production default, adopted as-is. F2 (TUW) is **deferred**, scoped out by the operator.
> **Rule-0 anchors for the binds-to column** (read 2026-07-14): `lab/analysis/regime/decompound_remc_2026-06-07/decompound.py` (`ACCOUNT=200_000`, `WITHDRAW_AT=210_000`, mode `banded`); `.../regime_gate.py` (`FLOOR_P99=0.05`, `FLOOR_BUST=0.01`, H1/H2 half-panel split, Part-A 6mo block bootstrap); emitted metrics = `pass_rate / bust_rate / p99_dd / p95_dd / median_days_to_pass / max_dds`.

> ✅ **FILL STATE (2026-07-14): FROZEN.** F1 + F3 + F4 confirmed; F2 deferred (not part of T1). Status bumped `NUMERIC PHASE-0 PENDING` → `NUMERIC FROZEN` in this commit. **No MC has run yet** — Phase 1 (running the decompound instrument against T1) is a separate, not-yet-taken step, and F4's metric (median days-to-first-skim) still needs a small instrument add before it can run (§ note below).

### Field 1 — Max-DD breach bar *(the capital-ruin gate; replaces challenge bust/static-DD)*
- **Binds to:** `regime_gate.py` `FLOOR_P99` / `FLOOR_BUST`, applied **per regime half** (H1 2020–2023 chop, H2 2023–2026 trend).
- **Pick a form, then the number(s):**
  - `[x]` Path max-DD ceiling — **p99 max-DD ≤ 10 %** *(instrument emits `p99_dd` today; direct)*   ← **OPERATOR-CONFIRMED 2026-07-14**
  - `[ ]` Breach-probability ceiling — **P( max-DD > ____ % ) ≤ ____ %** *(a ruin line + a probability)*
- **Calibration context (fact, NOT a bar):** on the clean-vintage decompound instrument the locked book already runs **p99 DD 5.32% / bust 1.47%** — *both* old challenge gates (5% / 1%) breach, hard regime-split (H1 bust ~13.8%). A successor bar looser than that is a documented loosening; tighter forces de-risk.
- **Why 10% (agent reasoning, retained for audit):** self-funded has **no external bust line**, so the ~5% challenge ceiling does not transfer; 10% ≈ 2× the benign clean-vintage p99 (5.32%) and makes the **2020–2023 chop half** (p99 DD ~7.5%, bust ~9–13%) the binding constraint — testing the exact regime tail the decompound HOLD flagged, rather than re-litigating it. Sensitivity menu recorded at proposal time: `5%` re-litigates the HOLD → near-auto-FALSIFIED · `~8%` knife-edge on H1 · `10–12%` benign-clears, chop-binding · `≥15%` weak gate. **Operator confirmed 10% — 2026-07-14 ("confirm T1").**
- **VALUE:** `p99 max-DD ≤ 10% per regime half`  *(CONFIRMED 2026-07-14)*   ·   **form chosen:** `path max-DD ceiling`

### Field 2 — Time-under-water tolerance *(duration risk the pass-timeout proxied poorly)*
- **Binds to:** ⚠ **NO PRODUCING CODE YET.** The instrument tracks max-DD *magnitude* (`max_dds`) and `days_to_pass`, **not** time-below-prior-peak. Declaring this bar commits to a small instrument extension (a TUW accumulator in the sim/summary path) **before Phase 1** — carry the obligation into the analysis handoff.
- **Form:** **p95 TUW ≤ ____ business days**, per regime half *(or state an alternative TUW statistic if p95 is not the one you want)*.
- **Calibration context:** none in-repo (metric not yet computed) — this is a from-scratch tolerance.
- **VALUE:** `DEFERRED 2026-07-14` — operator scoped F1/F3/F4 only; TUW needs an instrument extension first. Not part of this freeze; add via a follow-up amendment if wanted. The T1 grid row therefore carries **no F2 clause** (a 3-dimension triple, not 4).

### Field 3 — Withdrawal / reset model *(the model UNDER TEST — a choice, not a threshold)*
- **Binds to:** `decompound.py` `rebank(mode='banded')`: base **$200,000**, skim **+5% → $210,000 back to base** (`WITHDRAW_AT`). This is the current reference model, not a pre-chosen answer (brief §3).
- **Pick one:**
  - `[x]` **ADOPT** as-is: +5% skim / $200K base / reset-to-base.   ← **FIRM AGENT CALL** (documented default; already Joshua's chosen model per `decompound.py`)
  - `[ ]` **AMEND:** skim at **+____ %** / base **$________** / reset to **$________**.
  - `[ ]` **REJECT** and specify a different cashflow model: `__________`
- **Why ADOPT:** this is the *existing* production model (`WITHDRAW_AT=210_000`, mode `banded`), documented in-source as Joshua's chosen withdrawal model. Selecting the status-quo default is a legitimate agent call — not a risk-appetite invention. Change it only if the self-funded cashflow reality has shifted.
- **VALUE:** `ADOPT — +5% skim / $200K base / reset-to-base (banded)`

### Field 4 — Operational impracticality bar *(makes "clears only by being useless" binary)*
- **Binds to:** instrument emits `median_days_to_pass` today; a self-funded analogue (median time-to-first-skim / median DD-recovery time / capital-lockup ceiling) may need selecting.
- **Form:** the lane is **IMPRACTICAL if ____** *(e.g. median business-days-to-first-$210K-skim > N, OR capital locked below base for > M days)*.
- **Why "median days-to-first-skim > 252 bd (~1 yr)" (agent reasoning, retained for audit):** the self-funded analogue of `median_days_to_pass`; a book that cannot return its first +5% skim within a trading year is too slow to justify carrying the regime tail F1 accepts. Round, defensible, and it makes "clears only by being useless" binary. **Operator confirmed — 2026-07-14 ("confirm T1").**
- ⚠ **Open instrument obligation (carries into Phase 1):** days-to-first-skim is not emitted by `decompound.py`/`remc.py` today — a small add to the banded-equity path (cheaper than TUW; falls straight out of the existing `rebank(mode='banded')` reset loop). Must land **before** Phase 1 can score F4. Whoever authors the Phase-1 analysis handoff carries this obligation forward explicitly (parent brief §7 step 3).
- **VALUE:** `median business-days-to-first-$210K-skim > 252 bd ⇒ IMPRACTICAL`  *(CONFIRMED 2026-07-14)*   ·   **metric chosen:** `median days-to-first-skim`

### Candidate triple grid — pre-register ALL triples before the first MC cell
Each row is one (Max-DD, TUW, Withdrawal, Impracticality) combination to evaluate; **both regime halves must clear** for a row to be admissible (H-SFRISK-1). One triple ⇒ one row; add rows if sweeping.

| Triple ID | F1 Max-DD bar | F2 TUW bar | F3 Withdrawal model | F4 Impracticality bar |
|---|---|---|---|---|
| **T1** *(CONFIRMED 2026-07-14 — 3-dim)* | p99 max-DD ≤ 10% / half | — *(deferred, not in T1)* | ADOPT +5%/$200K banded | median days-to-first-skim > 252 bd |
| *(T2 optional)* | | | | |

### Commit procedure (in order — the freeze IS this commit)
1. ✅ Fill every `VALUE:` field + form checkbox above; complete the grid. — done (F1/F3/F4; F2 deferred, not blank — an explicit scoped-out decision).
2. F2 (TUW) was **not declared** (deferred), so no TUW instrument obligation carries forward. F4's own metric (days-to-first-skim) **does** carry a producing-code obligation — recorded above, not silently dropped.
3. ✅ Status line bumped: `NUMERIC PHASE-0 PENDING` → `NUMERIC FROZEN` (this commit).
4. ✅ This file committed **alone**, message `Q-SFRISK-1 Phase-0 numeric freeze`.
5. → Commit hash written back into the parent brief §8 (`Pre-registration commit hash`) as a **separate** follow-up edit/commit.
6. Phase 1 (running the decompound instrument against T1) is **NOT started by this freeze** — it is a distinct, heavier step (compute + the F4 instrument add) that needs its own go.

---

## Pre-registered verdicts (architecture — numeric cells filled at Phase-0)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | Phase-0 numeric amendment committed **and** ≥1 declared triple clears both regime halves without crossing the impracticality bar | Admitting ADR / go-live risk artifact |
| `FALSIFIED` | Phase-0 numeric amendment committed **and** every declared triple fails ≥1 half or only "clears" via impracticality | Close; go-live stays blocked pending fresh Pre-Q |
| `AMBIGUOUS-HOLD` | Leading triple splits halves, or a half is vacuous | Closure names re-test window |

---

## Forbidden moves (pre-registration)

- Running any successor-semantics / decompound re-MC under "trial" numbers before this file's Phase-0 numeric amendment is committed.
- Inventing max-DD / TUW / withdrawal thresholds in the parent brief to satisfy ceremony.
- Editing the §6 triggers after seeing results (Known Trap #12).
- Treating challenge-era 99.83/0.17/4.37 as a live self-funded claim.

---

## Audit hooks

```bash
# Status must now read NUMERIC FROZEN, not PENDING
grep -n "^\*\*Status:\*\*" docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md
# Expected: NUMERIC FROZEN (2026-07-14 ...)

# All four fields resolved (CONFIRMED or DEFERRED), zero blank VALUE placeholders
grep -n "VALUE:" docs/briefs/pre-registration/Q-SFRISK-1-verdict-preregistration.md
# Expected: 4 lines, none reading a bare `__________`

# Existence discharge for rescope §4 completion falsifier
ls docs/briefs/ docs/briefs/pre-registration/ | grep -iE "SFRISK|successor|self-funded"

# Parent brief §8 carries this freeze's commit hash (populated as a follow-up commit)
grep -n "Pre-registration commit hash" docs/briefs/Q-SFRISK-1-successor-self-funded-risk-framework.md

# No MC yet under this Pre-Q — Phase 1 is a separate, not-yet-taken step
ls lab/analysis/ 2>/dev/null | grep -i SFRISK || echo "no SFRISK analysis dir (expected — Phase 1 not started)"

# F4's instrument obligation (days-to-first-skim) is not silently forgotten
grep -n "days-to-first-skim" lab/analysis/regime/decompound_remc_2026-06-07/*.py || echo "not yet built (expected — Phase-1 prerequisite)"
```
