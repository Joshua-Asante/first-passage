# Pre-registration — Q-FUNDPOL-1 (funded-phase policy inheritance)

**FROZEN 2026-07-31, before any Q-FUNDPOL-1 arm runs.** This artifact discharges the
[companion brief](../Q-FUNDPOL-1-funded-phase-policy-inheritance.md)'s **§8** obligation: it carries
the §6 gate table verbatim, the exact policy-arm definitions with **K frozen**, the metric
definitions, the frozen geometry every arm consumes, and the P1/P2 precondition handling. Nothing
below changes after a number is read; a change requires closing this pre-registration and opening a
fresh one (Known Trap #12).

**Status:** `FROZEN / not-yet-exercised`. **Nothing is run here** — this session is docs-only.
**Loop of record:** OUTER (INQHIORI Inquire-phase).
**Companion Pre-Q:** [`../Q-FUNDPOL-1-funded-phase-policy-inheritance.md`](../Q-FUNDPOL-1-funded-phase-policy-inheritance.md) (`OPEN` 2026-07-28, anchor `52b2805`).
**Parent:** `Q-EVALSEQ-1` §7 fork ([`2026-07-24-2leg-eval-frontload-schedule-preregistration.md`](2026-07-24-2leg-eval-frontload-schedule-preregistration.md), anchor `25bd4d8`).
**Authored:** 2026-07-31 · Claude Code (Opus 5), operator-directed ("docs-only freeze before any run").
**Authorizes:** nothing. Pre-registration ≠ recommendation ≠ run authorization. Phase 1 additionally
requires the §9 code contract to land and the §6 preconditions to print DISCHARGED.

---

## §0 — Rule 0 reads (re-verified at HEAD `257e294`, 2026-07-31)

Every anchor below was re-read at this worktree's HEAD, **not** carried over from the brief. Three
had moved since the brief was authored on 2026-07-28; each was re-read rather than re-cited.

| Source | Anchor | What was re-verified |
|---|---|---|
| [`ops/c1_rail/c1_sizing_host_reference.py`](../../../ops/c1_rail/c1_sizing_host_reference.py) | `c134060` 2026-07-24 | **The symptom, re-read directly.** `rg -n -i "funded\|eval_phase"` returns **ZERO hits** (exit 1). There is still no funded/eval branch in the live sizing host — the brief's premise is intact. `LEG_MAP` `cap_alloc` **MYM 69 / MNQ 11** unchanged. |
| [`core/dd_protection.py`](../../../core/dd_protection.py) | ⚠ **moved** `656bbfe` → `fc14682` 2026-07-30 | Re-read: `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40` — **unchanged**. The move is substrate Phase 4 (pre-divided constants), not a control change. Line 208 still states the axis-separation contract: lifecycle "MULTIPLIES against BASE_RISK/DD_SCALE — it never edits them". |
| [`core/firm_rules.py`](../../../core/firm_rules.py) | ⚠ **moved** `cb60516` → `fc14682` 2026-07-30 | Re-read `Tradeify_Select_100K` (lines 308–321): `dd_type="trailing_locking"`, `starting_balance=100_000`, `max_dd_pct=3.0`, `dd_lock_offset_usd=100`, `profit_target_pct=6.0`, `min_trading_days=3`, `micro_contract_cap=80`, `consistency_rule_pct=40.0`, `daily_loss_pct=None` — **all unchanged**. |
| [`lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py`](../../../lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py) | ⚠ **moved** `4fac99c` → `78a6e8b` 2026-07-29 | `funded_sim` (lines ~226–262) re-read in full. State machine unchanged (`floor = np.where(locked, FLOOR_LOCKED, peak - DD)`; `locked |= peak >= FLOOR_LOCK_BAL`; `locked |= want`; `want &= first \| (bal > last_req)`). **Two changes since the brief:** the binary `np.where(tier_hi, CAP_HI, CAP_LO)` cap is **replaced** by the four-rung `FS` ladder (`caps=` parameter + end-of-day `FS.latch`); `PAYOUT_MIN` is **still `1_000.0` at line 82** and is **not** a parameter (line 248 `want &= amt >= PAYOUT_MIN`). See §1-D2. |
| [`lab/analysis/c1/tradeify_book_composition_2026-07-23/funded_scaling.py`](../../../lab/analysis/c1/tradeify_book_composition_2026-07-23/funded_scaling.py) | `78a6e8b` 2026-07-29 (**new since the brief**) | Single source of truth for the funded ladder. `LADDERS[100_000.0] = ((0, 30), (101_500, 40), (102_000, 50), (103_000, 80))`. `legacy_two_step()` reproduces the old binary 40→80 @ $103,000. `latch()` is one-way and documented as end-of-day (a rung reached today raises the cap **next** day). |
| [`lab/archive/c1_capalloc_2026-07-27/run_capalloc.py`](../../../lab/archive/c1_capalloc_2026-07-27/run_capalloc.py) | `28f7cb9` 2026-07-29 (**new since the brief**) | The **proven driver** for the §7 instrument: `import gap_stage2_capbound as G` (line 70), pin override `G.WIN_MIN, G.PAYOUT_MIN = args.win_min, args.payout_min` (line 284), ladder switch `--funded-ladder verified\|legacy` (lines 269–283, and `setattr(G, ...)` line 463), call site `G.funded_sim(...)` (line 195). This is how a corrected-pin run of the §7 instrument is executed today. |
| [`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../../notes/2026-07-24-tradeify-rulepin-verification.md) | ⚠ **moved** `…` → `b7ebc4a` 2026-07-31 | P1 evidence + the **2026-07-31 precedence correction** (see §1-D3). Pin table lines 30–33; payout-lock verbatim lines 68–71. |
| [`docs/briefs/2026-07-23-tradeify-book-composition.md`](../2026-07-23-tradeify-book-composition.md) | ⚠ **moved** `4fac99c` → `b7ebc4a` 2026-07-31 | §Addendum 2026-07-29: the corrected funded figures (see §1-D1) and the second H1 retarget to $299.80/acct-mo. |
| [`lab/analysis/c1/tradeify_book_composition_2026-07-23/RESULTS.md`](../../../lab/analysis/c1/tradeify_book_composition_2026-07-23/RESULTS.md) | `78a6e8b` 2026-07-29 | §Addendum 2026-07-29 four-arm attribution table + the bit-identical legacy-ladder behaviour-preservation control. |
| [`docs/methodology/regime_robustness_gate.md`](../../methodology/regime_robustness_gate.md) | — | Part B half-panel split: "Unequal-length halves are acceptable; document the split point." |
| [`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](../../adr/2026-07-23-c1-rung-selection-ev-objective.md) | `9ab2e8b` 2026-07-23 | `Accepted`. Regime-robustness is a hard precondition, not EV-overridable. §5 forbids sizing above 1.00×. |
| [`docs/methodology/strategy_lifecycle.md`](../../methodology/strategy_lifecycle.md) | — | Down-only ladder; fixed rungs **1.00× / 0.50× / 0.25× / 0.00×**. The only source of the θ values used in §7. |

**Panel provenance (read, not assumed):** [`out/daily_panel.csv`](../../../lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv)
spans **2020-08-04 → 2026-07-21**. Inputs (`inputs/*.csv`) are gitignored — **absent on this worktree,
present in the main checkout** (`C:\Users\joshu\multi_firm_operations\lab\analysis\tradeify_book_composition_2026-07-23\inputs\`,
all four 2026-07-23 TV exports named in `paths.CSV`). See §9 reachability.

---

## §1 — What changed since the brief, and what this pre-registration therefore freezes

The brief was authored **2026-07-28**. Three things landed after it. All three are **venue-fact or
harness corrections dated after the brief** — none is a response to any Q-FUNDPOL-1 result, because
no Q-FUNDPOL-1 arm has ever run. Recording them here, before Phase 1, is the pre-registration doing
its job; folding them in silently at read time would be Trap #12.

### D1 — The funded geometry the brief describes is superseded. The brief's §1 prose is stale.

The brief §1 says the contract cap "*doubles* (40→80) once balance reaches $103,000". The verified
rule ([`funded_scaling.py`](../../../lab/analysis/c1/tradeify_book_composition_2026-07-23/funded_scaling.py),
help-centre article 12853966 §"Contract Scaling Plan (Funded Accounts Only)") is a **four-rung,
EOD-calibrated, one-way ladder**: **30 → 40 @ $101,500 → 50 @ $102,000 → 80 @ $103,000**.

What survives, what does not:

- **Survives — and it is the brief's actual load-bearing observation:** the top rung ($103,000) and
  the floor-lock equity trigger ($103,100) still sit **$100 apart**. The "one ~$3.1K climb
  simultaneously maximises position size and converts a trailing barrier into a fixed one" structure
  is intact. The question is unharmed.
- **Does not survive:** "doubles 40→80". The start tier is **30**, not 40; the step at $103,000 is
  **50→80** (1.6×). The full start→top span is 30→80 (2.67×), reached across **three** thresholds,
  two of which ($101,500, $102,000) the brief never names.
- **New structure the brief could not have known:** two additional thresholds sit in the
  low-equity region — exactly where the funded floor binds hardest and where mortality is decided.

Also falsified on 2026-07-29: the modelled `PAYOUT_MIN = $1,000` **does not exist**. Select **Flex**
has no minimum payout ($250 belongs to Select *Daily*).

**Frozen consequence:** every arm consumes the §2 geometry. No arm may run against the binary
40→80 ladder or a non-zero payout minimum except the §6 P2-a legacy reproduction control.

### D2 — The §7 instrument is only *half* corrected, and the uncorrected half is this question's subject

`gap_stage2_capbound.funded_sim` took the ladder fix (`caps=` parameter, `FS.latch`). It did **not**
take the payout-minimum fix: `PAYOUT_MIN = 1_000.0` is still a module-level literal (line 82) gating
`want &= amt >= PAYOUT_MIN` (line 248), with no parameter hook.

This is disqualifying if left alone. `PAYOUT_MIN` gates **when a payout may be requested**, a payout
request **is** a floor-lock trigger, and payout timing is half of what Q-FUNDPOL-1 tests (brief §7
Phase 2 limb (b)). Running the timing arms against a phantom $1,000 floor would put a fabricated
constraint at the centre of the question. Independently measured: removing the payout minimum alone
moves funded `dead-1y` **+2.84 pp**, and **+6.29 pp** jointly with the ladder — super-additive
(RESULTS §Addendum 2026-07-29).

**Frozen consequence:** Phase 1 sets `G.PAYOUT_MIN = 0.0` via the **already-proven**
`run_capalloc.py` override pattern (§0). No new plumbing is invented; §9 pins the contract.

### D3 — P1's evidentiary basis got *stronger* on 2026-07-31, not weaker

P1 was discharged 2026-07-29 against the published help-centre article. On 2026-07-31 (`b7ebc4a`) a
full read of the Funded Trader Agreement found the repo's precedence rule had been **backwards in
five documents**. FTA **§11**: "*the Help Center rule shall prevail with respect to trading rules,
account parameters, product classifications and groupings, and the definition of prohibited trading
conduct*"; §4.1 incorporates help-centre rules as binding.

The payout-triggered floor lock is an **account parameter**. P1 therefore read the **governing**
source, not a subordinate one awaiting FTA confirmation. **P1 stays discharged and is strengthened.**

**Residual, recorded not discharged:** an **authenticated in-dashboard** read is still owed
([`STATE.md`](../../../STATE.md) operator-queue item 4). It is a standing venue-drift obligation
across the whole Tradeify surface — it is **not** a Q-FUNDPOL-1 precondition and does not gate
Phase 1. Its failure mode is covered by `Q-CAPALLOC-2`, which owns venue-drift survivability.

---

## §2 — Frozen geometry (every arm consumes exactly this; no arm may vary it)

| Constant | Frozen value | Source |
|---|---|---|
| `starting_balance` | `100_000.0` | `firm_rules.Tradeify_Select_100K` `fc14682` |
| `DD` (trailing, pre-lock) | `3_000.0` | `max_dd_pct=3.0` · `gap_stage2_capbound.py:81` |
| `FLOOR_LOCKED` | `100_100.0` | `dd_lock_offset_usd=100` · help-centre art. 12853966 |
| `FLOOR_LOCK_BAL` (EOD equity trigger) | `103_100.0` | help-centre art. 12853966 |
| Payout-triggered lock | **ON** (`locked |= want`) | P1, verified 2026-07-29 (§1-D3) |
| Funded contract ladder | **`((0, 30), (101_500, 40), (102_000, 50), (103_000, 80))`** | `FS.ladder_for(100_000.0)` `78a6e8b` |
| Ladder semantics | EOD-calibrated, **one-way latch**, effective **next** trading day | `FS.latch` docstring; art. 12853966 |
| `WIN_MIN` | `200.0` | **verified** 2026-07-29 (1 of 3 pins that matched) |
| `PAYOUT_MIN` | **`0.0`** | **corrected** 2026-07-29 — Flex has no minimum (§1-D1) |
| `PAYOUT_CAP` | `4_000.0` | `gap_stage2_capbound.py:83` |
| `SPLIT` | `0.90` | 90/10 profit split |
| Payout balance ratchet | **ON** (`want &= first | (bal > last_req)`) | `gap_stage2_capbound.py:243` |
| Leg caps | MYM **69** / MNQ **11** | `LEG_MAP` `c134060` |
| `h_fund` (horizon) | `780` business days | `run_scenario` default |
| Seeds | `(11, 12, 13)` | `run_scenario` default |
| `n_paths` | `6_000` per seed | `run_scenario` default |
| `BD_PER_MO` | `21.7` | `rerun_section2.py:36` |
| Book under test | **2-leg c1 only** (Striker DJ30/MYM + Striker NAS100/MNQ) | brief §1 |

**ORB and Aegis legs are excluded from every arm.** Book *composition* is a different question
(`Q-COMPOSE-1`, `Q-BOOKFIT-1`); ORB-MNQ was unparked to active research 2026-07-31 under its own
ADR. Mixing composition into a policy question would make the verdict uninterpretable.

**Regime halves (pinned, equal-length, from the sibling that uses this same panel):**
**H1 = 2020-08-04 → 2023-07-27** (778 bd) · **H2 = 2023-07-28 → 2026-07-21** (778 bd) · total 1,556 bd.
Source: [`c1_capalloc_2026-07-27/RESULTS.md`](../../../lab/archive/c1_capalloc_2026-07-27/RESULTS.md)
line 23. The split point is the panel midpoint, per `regime_robustness_gate.md` Part B default.

---

## §3 — Question (carried verbatim; not re-opened here)

**Q-FUNDPOL-1:** What does the funded phase's threshold structure (floor-freeze at $103,100 peak or
at first payout; contract-cap doubling at $103,000; payout balance-ratchet) imply for the policy
governing it, and does the inherited flat eval policy leave material value unclaimed or carry
unpriced ruin risk?

**Reading note, per §1-D1:** "contract-cap doubling at $103,000" is the brief's 2026-07-28 wording.
The verified mechanic is the four-rung ladder topping out at 80 micros at $103,000. The question is
unchanged — the $103,000/$103,100 adjacency it turns on is intact — but **the arms in §7 are written
against the verified ladder, not against the brief's wording.**

---

## §4 — Hypothesis and falsifier (carried **verbatim** from brief §4 — not amendable here)

**H-FUNDPOL:** The funded phase is a **distinct policy surface** — i.e. under the frozen policy set
(§6) and the modeled funded geometry, at least one threshold-aware policy beats the inherited flat
policy by **> 25% on expected net payout cash per account-month** at **no worse modeled ruin**
(12-month funded mortality within +0 pp), **and** that lift holds in **both** regime halves. If so,
funded policy must be selected on its own terms rather than inherited, and the finding routes to an
operator fork + its own admitting ADR. **Otherwise** — no policy clears +25% at equal-or-better
ruin, or the lift reverses across halves — inheritance is adequate, the funded lever is spent, and
flat-by-inheritance stands as a *recorded* decision rather than an omission.

**Reject H-FUNDPOL → `FALSIFIED` if:** best policy's lift ≤ 25% vs the flat control, **OR** any
policy achieving > 25% does so with higher modeled 12-month mortality, **OR** the sign of the best
policy's lift reverses between H1 and H2.
**Accept H-FUNDPOL → `RESOLVED` if:** ≥1 policy shows > 25% lift **AND** mortality ≤ control **AND**
same-sign lift in both halves.
**Ambiguous-hold if:** the best policy clears +25% and both-halves sign but its bootstrap band
overlaps the control's (lift not separable from resampling noise), **or** the §6 payout-lock
precondition resolves UNVERIFIED — re-test on the trigger named in §6.

The **25%** floor is inherited from Q-FUNNEL-1 §3(a) so this brief's bar cannot be tuned to its own
result. It is **not** a knob and is not re-derived here.

---

## §5 — Forbidden moves (brief §5 carried forward, plus the four this freeze creates)

Carried from the brief (each still live):

- **Reading the 2026-07-28 eval-lock fix as license to also "correct" `funded_sim`'s lock.** The
  funded lock is **real** and now doubly-sourced (§1-D3).
- **Consuming `$339/acct-mo`, `63%`, or `8.2 mo` as a baseline or objective calibration.** Contaminated.
  The control is this brief's own flat arm, run in the same harness, never a published figure.
- **Treating a post-lock free-roll as license to size above 1.00×.** The ladder is down-only.
- **Adopting any winning policy without a separate admitting ADR** (`concept-not-constant` chain).
- **Optimizing payout timing for lock-capture while ignoring the balance ratchet.** Every timing arm
  is scored on full-horizon cash, never on time-to-lock.
- **Re-opening the eval rung.** ADR 2026-07-23 resolved it. Funded-phase only.
- **Outcome-conditional D-tests.** The policy set is frozen in §7, now, before Phase 1.

New, created by this freeze:

- **Substituting `$318.20` or `$299.80` for `$339` and calling the baseline fixed.** All three are
  *eval-inclusive chain* rates. This brief's objective is **funded-only cash per account-month**
  (§8-M1) and is not any of them. A published chain figure must never appear as this brief's control.
- **Running any arm against the legacy binary 40→80 ladder or `PAYOUT_MIN = 1_000`.** The single
  exception is the §6 P2-a reproduction control, whose *only* permitted output is MATCH/MISMATCH.
- **Fixing `PAYOUT_MIN` by editing `gap_stage2_capbound.py`'s module literal.** It is shared with
  five other kernels (the M-24 sweep found six binary-cap sites across five files). Phase 1 uses the
  proven `run_capalloc.py` **override** pattern (§9-C2); an in-place literal edit silently re-scores
  every other consumer.
- **Widening the arm set after seeing P2's baseline.** K is frozen at **4** in §7. A fifth arm
  requires closing this pre-registration and opening a fresh one.

---

## §6 — Gate criteria (brief §6 table, reproduced **verbatim**)

> **Preconditions (both must clear before Phase 1 runs; neither is a verdict):**
>
> - **P1 — payout-lock clause verified against primary Tradeify source** — **DISCHARGED 2026-07-29,
>   present as modeled.** Verbatim from the published help-centre article: "your drawdown locks at
>   $100 above your starting balance … either automatically at EOD when your balance reaches $52,100
>   (for 50K), **or immediately when you request a payout — whichever comes first**." For the 100K
>   tier that is lock **$100,100**, trigger EOD **$103,100** or first payout — matching
>   `FLOOR_LOCKED` / `FLOOR_LOCK_BAL` exactly. **No policy family is void; the payout-timing arms
>   stand.**
> - **P2 — `funded_sim` reproduction control.** Re-run the published funded figures
>   (`funded-dead-1y 43%` for the 2-leg book) and print MATCH/MISMATCH before any policy arm is
>   scored. MISMATCH ⇒ halt; the harness or its inputs have drifted and no arm is interpretable.
>
> | Verdict | Trigger condition | Disposition |
> |---|---|---|
> | `RESOLVED` | best policy lift **> 25%** on net payout cash per account-month vs the flat control **AND** modeled 12-month mortality ≤ control **AND** same-sign lift in both regime halves | Funded policy is a distinct surface → operator fork + its own admitting ADR (`concept-not-constant` chain). **No sizing change from this brief.** |
> | `FALSIFIED` | best lift **≤ 25%**, **OR** any >25% arm carries higher mortality than control, **OR** best arm's lift reverses sign across H1/H2 | Funded lever spent. Record flat-by-inheritance as a **decided** policy, not an omission; close. |
> | `AMBIGUOUS-HOLD` | best arm clears +25% and both-halves sign but its bootstrap band overlaps the control's (P1 discharged 2026-07-29, so that limb can no longer fire) | Re-test trigger: P1 verification lands, **or** the first funded account accumulates 12 months of live data — whichever first. |
>
> **Hard scheduling gate:** this brief must reach a verdict **before the first funded account
> exists** (i.e. before an eval pass converts). It is deliberately **not** placed on the 2026-08-08 slate.

**The table above is frozen and is the verdict rule. Nothing below re-writes it.**

### P1 — handling (state at freeze: **DISCHARGED**)

Discharged 2026-07-29; **strengthened** 2026-07-31 by the FTA §11 precedence correction (§1-D3).
Phase 0 re-prints the evidence for the record; it does not re-adjudicate. The AMBIGUOUS-HOLD table
row already notes the P1 limb "can no longer fire". The authenticated in-dashboard read remains a
standing operator obligation and is **not** a Phase-1 gate (§1-D3).

### P2 — handling (the target `43%` is a **legacy-ladder** figure; split into two parts)

P2's stated target `funded-dead-1y 43%` was published **2026-07-28**, before the 2026-07-29 ladder
and payout-minimum corrections. Under the §2 frozen geometry the 2-leg funded `dead-1y` is
**49.06%**, not 43%. A verbatim P2 run would therefore print MISMATCH **for the right reason** —
the rules changed — and halt Phase 1 on a correction the estate has already made and verified.

P2's *purpose* is "prove the harness and its inputs have not drifted." That purpose is preserved
exactly, at strictly higher power, by splitting it. **This is a precondition-mechanics correction
made before any arm runs, driven by a dated venue-fact correction — not a gate amendment after
seeing a result. §4 and the §6 verdict table are untouched.**

| Part | Run | Expected | On failure |
|---|---|---|---|
| **P2-a** — harness integrity (**this is the literal `43%` control**) | §7 instrument with `--funded-ladder legacy --payout-min 1000` | 2-leg funded `dead-1y` **42.77%** ±1 pp; eval pass **37.78%** ±1 pp; chain **$318.20** ±$15 | **HALT.** Harness or inputs drifted. No arm interpretable. |
| **P2-b** — corrected-geometry baseline (establishes the control's operating point) | §7 instrument at the **§2 frozen geometry** | 2-leg funded `dead-1y` **49.06%** ±1 pp; chain **$299.80** ±$15; eval pass **37.78%** ±1 pp (must be **identical** to P2-a — both corrections are funded-only) | **HALT.** The §2 freeze does not reproduce the published verified-truth arm. |

Both parts print MATCH/MISMATCH **before any policy arm is scored**. Reference values:
[`RESULTS.md` §Addendum 2026-07-29](../../../lab/analysis/c1/tradeify_book_composition_2026-07-23/RESULTS.md)
four-arm table (control / arm (a) / arm (b) / arm (c)) and `out/arm_control.json`, `out/arm_c_both.json`.

The **eval-pass identity check** (37.78% in both parts) is the load-bearing sanity limb: both
corrections are funded-only, so any eval-pass movement between P2-a and P2-b proves the arm switch
leaked into `eval_sim` and invalidates everything downstream.

---

## §7 — Frozen policy arms (**K_intrinsic = 4**, no grid, no post-hoc additions)

The policy is a **fifth multiplicative factor at the risk_pct layer** — after `BASE_RISK`,
`DD_SCALE`, `M_lifecycle`, and any eval-phase schedule. It **multiplies; it never edits** a locked
constant (`dd_protection.py:208` axis-separation).

**Every θ below is a ratified lifecycle-ladder rung, not a chosen number.** `strategy_lifecycle.md`
fixes the ladder at **1.00× / 0.50× / 0.25× / 0.00×**; the arms use 1.00, 0.50, 0.25 and nothing
else. This is what makes the set a *policy family* rather than a parameter sweep, and it is why no
arm has a tunable knob.

| Arm | Type | Definition (exact) | Mechanism it isolates |
|---|---|---|---|
| **C0 — control** | — | `m_policy = 1.00` for all `t`. Payout requested whenever `funded_sim` deems eligible (default). **This is the inherited flat policy** and the sole baseline for every §6 comparison. | Inheritance by omission — the status quo. |
| **A1 — lock-state step** | sizing | `m_policy = 0.50` while `not locked`; `m_policy = 1.00` once `locked` (either trigger). Payout: default. | The barrier changing *kind* — trailing → fixed-and-far. Ladder-compliant: it de-risks pre-lock and **restores to**, never exceeds, 1.00×. |
| **A2 — floor-distance-proportional** | sizing | `m_policy = clip((bal − floor) / DD, 0.25, 1.00)`, evaluated on the **prior** day's EOD `bal`/`floor`, `DD = 3_000`. Payout: default. | Continuous cushion-awareness, incl. the two low-equity rungs ($101,500 / $102,000) A1 cannot see. Shape mirrors Q-EVALSEQ-1 arm (c) so the two questions' results are commensurable. |
| **B1 — equity-lock-deferred payout** | timing | `m_policy = 1.00` (sizing identical to C0). Payout requests **suppressed** until `locked` becomes true via the **equity trigger only** (`peak ≥ 103_100`); default thereafter. | The ratchet cost. C0 buys the lock early via `locked \|= want` but sets `last_req` at a low balance; B1 pays in delayed cash to set the ratchet high. Isolated because sizing is held at C0. |
| **C1 — joint (A1 ⊕ B1)** | both | A1's sizing **and** B1's payout rule, simultaneously. | **Required, not optional.** The two verified funded corrections were **super-additive** (+1.93 and +2.84 pp separately, **+6.29 pp** together). An additive read of A1 and B1 is therefore known-unsafe in this system. |

**K accounting.** `K_intrinsic = 4` non-control policy arms, banked to **this question's own
multiplicity**. DSR / placebo per `strategy-validation` applied to the **best-of-K at read**, using
K = 4. **No draw on the instrument-ledger K seats** — `K_banked(MNQ) = 2` with one Cap seat
remaining is a *strategy-candidate* ledger; a funded-phase sizing policy on an already-admitted book
is not a strategy candidate and must not consume it. Precedent: `Q-EVALSEQ-1` §6
(`K_intrinsic = 3`, self-contained) and `Q-CAPALLOC-2` §"No fresh selection K".

**Sizing arms are cap-clipped, not cap-exempt.** `funded_sim` already clips the day's stack to the
current ladder rung. `m_policy < 1` therefore reduces exposure **below** the rung; it can never lift
it above. No arm can breach the account cap by construction.

---

## §8 — Metric definitions (frozen; computed identically for every arm and every half)

| ID | Metric | Exact definition | Role |
|---|---|---|---|
| **M1** | **Net payout cash per account-month (funded-only)** | `mean(cash) / (mean(t_dead) / 21.7)` where `cash` is `funded_sim`'s SPLIT-adjusted (90%) payout total and `t_dead` is business days alive (capped at `h_fund = 780`). Averaged across seeds `(11, 12, 13)`. | **§4/§6 primary.** Deliberately **not** the book-comp `chain` (`pp * mean_cash / cyc`), which folds in eval pass-probability and eval months — this brief is funded-only (§5). |
| **M2** | **Lift** | `(M1_arm − M1_C0) / M1_C0`, as a percentage. Gate: **> 25%**. | §6 `RESOLVED` limb 1. |
| **M3** | **12-month funded mortality** | `mean(t_dead <= 260)`, verbatim from `run_scenario`'s `dead_1y`. | §6 `RESOLVED` limb 2. Gate: `M3_arm ≤ M3_C0` (the brief's "+0 pp"). |
| **M4** | **Both-halves sign agreement** | `sign(M2)` computed on H1 and H2 independently (§2 split). Gate: **same sign in both**, and the arm must be the best-of-K on the **full panel** — the halves test the winner, they do not select it. | §6 `RESOLVED` limb 3 · `regime_robustness_gate` Part B. |
| **M5** | **Bootstrap band** | 6-month-block bootstrap on the source panel, 1,000 resamples, seed `11`; 95% CI on `M2`. **Overlap with the control ⇒ `AMBIGUOUS-HOLD`**, even when M2/M3/M4 all pass. | §6 `AMBIGUOUS-HOLD` limb · `regime_robustness_gate` Part A. |
| **M6** | Diagnostics (**recorded, never a gate**) | `med_first_pay_bd`, `no_payout_pct`, `npay`, `mean_life_bd`, realised lock-trigger mix (equity vs payout). | Mechanism attribution in §9 closure. **Explicitly non-decisional** — promoting a diagnostic to a gate at read time is Trap #12. |

**Best-of-K selection rule, fixed now:** the "best policy" in §6 is the arm maximising **M1 on the
full panel**. Ties (within ±$1/acct-mo) break toward **lower M3**, then toward the **lower-K** arm
(A1 → A2 → B1 → C1). No other selection rule may be introduced at read.

---

## §9 — Run protocol, code contract, and reachability

### Reachability attestation (per `lesson_gate_reachability_preregistration`)

**The gate is reachable.** Harness `78a6e8b` + driver `28f7cb9` both exist and are proven (both were
executed 2026-07-29). Panel CSVs are gitignored and **absent on this worktree**, but **present in
the main checkout** at `lab/analysis/c1/tradeify_book_composition_2026-07-23/inputs/` (all four exports
named in `paths.CSV`, verified 2026-07-31). Phase 1 runs from the main checkout, or copies `inputs/`
into the worktree first. This is **not** a Q-HARV-0 / DISC-CAMP-0 unreachable-frozen-gate.

### C1 — the one code change Phase 1 needs, and its frozen contract

`funded_sim(p, q, m, h, caps=None)` takes a **scalar** `m`. The §7 arms need a **state-dependent**
factor. Phase 1 extends the signature by exactly one optional parameter:

```
funded_sim(p, q, m, h, caps=None, policy=None)
    policy: optional callable (state) -> ndarray[float] of per-path multipliers in [0, 1],
            evaluated ONCE per day t, BEFORE that day's `d` is computed, against the
            PRIOR day's EOD state (bal, floor, locked, rung, last_req, windays).
            None => 1.0 everywhere => byte-identical to today's behaviour.
```

Frozen requirements — any deviation voids this pre-registration:

1. **`policy=None` must be byte-identical to the current kernel.** Assert before any arm runs
   (same seeds ⇒ identical `cash`, `t_dead`, `npay` arrays). This is the behaviour-preservation
   control that isolates arm differences to the policy, exactly as the ladder refactor did it
   (RESULTS §Addendum 2026-07-29 evidence item 2).
2. **Prior-day state only.** A policy reading the *current* day's `bal` before that day's P&L is a
   look-ahead defect (`lesson_pine_offset_port_faithfulness_anchor` / `series[k] = k BACK`).
3. **Payout arms gate `want`, never `amt`.** B1/C1 suppress the *request*; they must not alter
   payout sizing, `PAYOUT_CAP`, or `SPLIT`.
4. **No edit to any §2 constant, `eval_sim`, `core/`, `dd_protection`, allocations, Pine, or the
   rail.** Read-only analysis; writes only under the harness's `out/`.
5. **Unit tests before arms**, mirroring `tests/lab/test_funded_scaling_ladder.py`: `policy=None`
   identity; prior-day-state ordering; clip bounds `[0, 1]`; `want`-only gating for B1.

### C2 — pin override (proven pattern; do not invent new plumbing)

```
import gap_stage2_capbound as G, funded_scaling as FS
G.PAYOUT_MIN = 0.0          # §1-D2 — verified: Flex has no minimum
G.WIN_MIN    = 200.0        # verified 2026-07-29
# ladder: G.FUNDED_LADDER default is already FS.ladder_for(100_000.0) — the verified ladder.
# P2-a ONLY: G.FUNDED_LADDER = FS.legacy_two_step(); G.PAYOUT_MIN = 1_000.0
```

Mirrors `run_capalloc.py:284` / `:463` exactly. **Never** edit the module literal in place (§5).

### Phase sequence (halt-on-failure; no phase may be skipped or reordered)

| Phase | Action | Halt condition |
|---|---|---|
| **0** | Re-verify §0 anchors; land C1 + its unit tests; print P1 evidence; run **P2-a** then **P2-b** | any anchor moved with a changed constant · any unit test red · either P2 part MISMATCH · P2-a/P2-b eval pass not identical |
| **1** | **C0 control** at §2 geometry; record M1/M3/M6 | control does not reproduce P2-b |
| **2** | **A1, A2, B1, C1** at §2 geometry; record M1/M2/M3/M6 each | any arm mutates a §2 constant |
| **3** | Select best-of-K by §8 rule; **then** H1/H2 re-score of control + winner (M4); bootstrap band (M5) | — |
| **4** | Assert §6 table against actual numbers; DSR/placebo at K = 4; write §9 closure | — |

Closure artifact per brief §9: `closures/Q-FUNDPOL-1-closure-{resolved,falsified,ambiguous}.md`,
referencing **this file by commit hash**, and recording what §7 predicted vs what happened.

---

## §10 — Audit hooks (runnable)

```bash
# --- This pre-registration precedes every arm (the brief §8 obligation). -------
git log --oneline -- docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md
git log --oneline --diff-filter=A -- lab/analysis/q_fundpol_1_*/   # must be EMPTY at freeze

# --- The SYMPTOM assertion: still no funded branch in the live sizing host. ----
# Expect ZERO hits (exit 1). Any hit => the brief's premise changed; re-read §1.
rg -n -i "funded|eval_phase" ops/c1_rail/c1_sizing_host_reference.py

# --- §2 frozen geometry still matches production/harness. ---------------------
rg -n "FLOOR_LOCK_BAL, FLOOR_LOCKED, DD" lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py
rg -n "100_000.0: " lab/analysis/c1/tradeify_book_composition_2026-07-23/funded_scaling.py
#   expect: ((0.0, 30.0), (101_500.0, 40.0), (102_000.0, 50.0), (103_000.0, 80.0))
rg -n "DD_TRIGGER = 0.015|DD_SCALE = 0.40" core/dd_protection.py
rg -n '"dd_lock_offset_usd": 100|"micro_contract_cap": 80' core/firm_rules.py

# --- §1-D2: the PAYOUT_MIN literal is STILL 1_000 and MUST be overridden, ------
# --- not edited (§5). If this line ever reads 0.0, an in-place edit happened. --
rg -n "WIN_MIN, PAYOUT_CAP, PAYOUT_MIN, SPLIT" lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py

# --- The override pattern Phase 1 must copy still exists. ---------------------
rg -n "G.WIN_MIN, G.PAYOUT_MIN|import gap_stage2_capbound as G" lab/archive/c1_capalloc_2026-07-27/run_capalloc.py

# --- P2 reference values (the numbers §6 P2-a/P2-b assert against). -----------
python -c "import json;d=json.load(open('lab/analysis/c1/tradeify_book_composition_2026-07-23/out/arm_control.json'));print('P2-a',d['rows'][0])"
python -c "import json;d=json.load(open('lab/analysis/c1/tradeify_book_composition_2026-07-23/out/arm_c_both.json'));print('P2-b',d['rows'][0])"
#   expect P2-a dead_1y 42.77 / chain 318.20 ; P2-b dead_1y 49.06 / chain 299.80 ; pass_pct 37.78 both

# --- Contaminated / eval-inclusive figures must never be this brief's control. -
rg -n '\$339|\$318|\$299\.80' docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md
#   Expect EXACTLY 6 hits, all benign (verified 2026-07-31): §0 book-comp lineage
#   row; §5 forbidden-move x2; §6 P2-a and P2-b reproduction targets; this hook's
#   own line (self-match). A SEVENTH occurrence -- or ANY hit inside §7 or §8 --
#   means an eval-inclusive chain rate leaked into an arm definition or the objective.

# --- Reachability (panel CSVs are gitignored; main checkout is the run site). --
ls lab/analysis/c1/tradeify_book_composition_2026-07-23/inputs/ 2>/dev/null \
  || echo "panel local-only (gitignored) - run Phase 1 from the main checkout"

# --- P1 evidence + the 2026-07-31 precedence correction still resolve. --------
rg -n "payout-triggered floor lock is REAL|whichever comes first" docs/notes/2026-07-24-tradeify-rulepin-verification.md
rg -n "Precedence corrected 2026-07-31|Help Center rule shall prevail" \
  docs/notes/2026-07-24-tradeify-rulepin-verification.md \
  docs/notes/rail_build/TRADEIFY_AUTOMATION_PAYOUT_COMPLIANCE.md

# --- Parent fork lineage resolves both ways. ---------------------------------
rg -n "Funded-phase schedule" docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md
```

---

## Verification

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md --type inquire
# Expected: all 6 checks PASS

# Rule-0 confirmation (the load-bearing symptom read, re-run at HEAD)
rg -n -i "funded|eval_phase" ops/c1_rail/c1_sizing_host_reference.py        # expect ZERO hits
rg -n "DD_TRIGGER = 0.015|DD_SCALE = 0.40" core/dd_protection.py    # expect both

# §6 table is verbatim from the brief (diff the block, expect only blockquote markers)
rg -n "best policy lift \*\*> 25%\*\*" docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md \
  docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md   # expect 1 hit each

# §4 is verbatim from the brief
rg -c "H-FUNDPOL" docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md \
  docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md

# The 25% floor is inherited, not re-derived
rg -n "0.25|25%" docs/briefs/pre-registration/Q-FUNNEL-1-verdict-preregistration.md | head
```

**Discipline checklist:** §0 populated with commit anchors, three re-read after drift ✓ ·
§4 falsifier carried verbatim, binary ✓ · §5 lists genuinely tempting moves incl. four this freeze
creates ✓ · §6 table verbatim + R/F/A ✓ · §3 question is symptom-shaped ✓ · §10 runnable ✓ ·
K frozen = 4 with explicit no-draw on the instrument ledger ✓ · reachability attested ✓ ·
metric definitions pinned and separated from the eval-inclusive `chain` ✓ · every θ traced to a
ratified ladder rung, no free knob ✓ · **nothing run** ✓.
