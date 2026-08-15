# Pre-registration — Q-6JCOMPOSE-2: composed bust for Aegis-6J as a c1 third leg (basis-corrected)

**Status:** `CLOSED — VOID` (C2 RED; gate unreachable by construction) — see [closure](../closures/Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md). Frozen body below is the record, byte-unchanged (Trap #12).
**Supersedes-relationship:** does **not** amend or reopen
[`Q-6JCOMPOSE-1`](Q-6JCOMPOSE-1-verdict-preregistration.md) — that pre-reg is **CLOSED `VOID`**
([closure](../closures/Q-6JCOMPOSE-1-closure-void-unexecutable.md)) and stays byte-unchanged
(Trap #12). This is the sanctioned **close-and-reopen-fresh** route, correcting **one** defect class:
a frozen arm specified in units the frozen gate cannot see. Precedent:
[`aegis-6j v1→v2 window-realigned`](2026-07-16-aegis-6j-prop-reconstruction-v2-window-realigned-prereg.md)
(`FRESH-PREREG-OK` — window realignment, not gate-lowering).
**Adjudication basis:** **FRESH-PREREG-OK, and the correction is STRICTER, not looser** — see §2.1.
**Loop of record:** STRATEGIC. **D-S-A domain:** data.
**Aegis declaration (ADR 2026-07-14 §5, explicit):** this artifact **IS Aegis-bearing** — solo 6J leg
composed against the incumbents; mechanism frozen to Aegis→6J v0.3 identity. No lever is free.
**Authored:** 2026-07-29 · Claude Code (operator-directed: proceed with the close-and-reopen).

---

## §0 — Rule-0 reads (executed this session, not recalled)

| # | Source | What it established |
|---|---|---|
| 1 | `run_class_s_c1_scoring.py` L260-305 (`build_scaled_panel`) | `scale = alloc×ACCOUNT / r_dollars`, `r_dollars` = full-stop mean **of that series** ⇒ **exactly scale-invariant**. Read directly; this is the whole reason Q-6JCOMPOSE-1 is void. |
| 2 | same, L67-93 | `ACCOUNT = BASELINE_BALANCE` ($200K static decompound), `R_BASIS = "full_stop_mean"`, `MIN_FULL_STOP_N = 5`; `PANEL_FILES["aegis"]` = **`ae744`**, `CAL_STRATS`/`CAL_ALLOCS` (aegis **0.0150**), `EXPECTED_1R_AEGIS` = **$2,912.96 / n=11** ⇒ the aegis leg is **already wired**. |
| 3 | `run_compose_regime_remc.py` L254-294 | composition site: `panel2` → third column → `pd.concat` → `book_daily_at_100k(panel3)`; asserts columns and index. Engine imported **unmodified**. |
| 4 | [`6J.md`](../../../ops/instruments/6J.md) **J10 / J11** | panel of record is **per purpose**; `ae744` is KNOWN-config, H1-covering, operator PICK 2026-07-15/JA. |
| 5 | [`Q-6JCOMPOSE-1 closure`](../closures/Q-6JCOMPOSE-1-closure-void-unexecutable.md) | Phase-0 hooks 1,2,3,4,5,7 all PASS — **carried forward, not re-derived**. |
| 6 | [`M-SWAP-1`](../../methodology/lessons/methodology_lessons.md) | 1R-normalized MC absorbs additive cost as reduced size ⇒ wrong instrument for cost/cap questions. |

## §1 — Question

**Does adding Aegis-6J to the 2-leg c1 book keep composed bust ≤ 3.0% on all four partitions?**
The standalone survival question is answered (J4b/J8, window-limited); the **composed** quantity —
the one the ratified gate actually scores — has never been computed.

## §2 — Method (FROZEN)

**Engine:** `run_compose_regime_remc.py`, imported **unmodified**. 10,000 sims × seeds 42/123/2026,
horizon 1500, Run-2 consistency-on, bootstrap n=100 / 126 bd / seed 20260715. **No engine constant
touched.** The wrapper supplies input only: it patches `ORB_COL` → `"aegis_6j"` and
`build_orb_usd_column` → a builder that returns the 6J column, leaving every downstream primitive
(`book_daily_at_100k`, `compose_verdict_4tier`, `breadth_declaration`, the scoring) untouched.

**Tier: `Tradeify_Select_100K` ONLY, and the run is RESTRICTED to it (amended 2026-07-29,
pre-signature).** The wrapper narrows the tier list via
`dataclasses.replace(thr, tier_keys=("Tradeify_Select_100K",))` — `ScoringThresholds` is a frozen
dataclass, so this is a copy, not a mutation. **No threshold value is touched:**
`eval_bust_ceiling` 3.0% and `pass_floor` 50% are inherited unchanged. This is a **reporting-surface
narrowing**, not a gate change.

*Why:* C1 measured **4,562 s (76 min)** for 4 tiers; the engine loops tiers serially, so ~3/4 of
that wall clock produces rows the verdict never reads. Single-tier ⇒ **≈19 min**. Restricting it is
only legitimate as a *pre-registered* choice — after the freeze it would be an engine edit (hook 2)
or a method deviation, which is why it is decided here.

> **⚠ CONSEQUENCE, pre-registered so it cannot be discovered post-hoc: the engine's own aggregate
> `VERDICT` line becomes uninterpretable at `n_tiers = 1` and is NOT this pre-registration's
> verdict.** `compose_verdict_4tier` defines `RESOLVED` as "all four clear on **≥2 tiers** incl ≥1
> `trailing_locking`" and `AMBIGUOUS-HOLD` as "all-four clear on exactly 1 tier" — so with one tier
> `RESOLVED` is **structurally unreachable** and the engine would print `AMBIGUOUS-HOLD` even on a
> clean sweep. **Our verdict is read from the `Tradeify_Select_100K` row's four partitions against
> the §4 table (≤3.0% on all four ∧ P(pass) ≥ 50%) — never from the engine's printed verdict
> string.** The engine's cross-tier "FALSIFIED on EVERY tier" limb is likewise inapplicable and is
> not used.

**Baseline (fixed, cited, not recomputed):** 2-leg at WATCH-1 0.50×, corrected geometry —
full **0.11%** / H1 **0.22%** / H2 **0.04%** / boot-95th **1.20%**.

**The single composed arm (frozen — no sweep):**

| Element | Value | Why fixed |
|---|---|---|
| panel | **`ae744`** · n=152 · sha256 `e82a2c25…` · 2020-02-24 → 2026-07-01 | operator PICK; KNOWN-config (J11); **H1-covering** — `8e269` would zero-fill the governing partition |
| basis | **frozen `build_scaled_panel`**, static $200K decompound, `pin_r_basis(full_stop_mean)` | satisfies P4 by construction; `EXPECTED_1R_AEGIS` guard ($2,912.96 / n=11) stays armed |
| **risk allocation** | **`alloc = 0.0075`** = Aegis locked **1.50% × WATCH-1 0.50×** | **this is the size lever, and the only one the gate can see** (§2.1) |
| session set | **Mon + Wed only** (Tuesday dropped) | forced by S5 — Tue free capacity is 0 |
| incumbent cap | **unchanged** MYM 69 / MNQ 11 | S5 forbids re-allocation |
| cap 8 / commission $3.10 | **EXPLICITLY OUT OF SCOPE** | not expressible through a scale-invariant gate (§2.1) |

**Exactly one composed cell is run.** No sweep of rung, alloc, panel, session set, or tier.

### §2.1 — The basis decision, stated (this is the correction)

Q-6JCOMPOSE-1 froze the arm as *"cap 8 × constant 0.50×"*. The frozen gate **cannot see that**: its
1R normalization is scale-invariant, so cap-8 is absorbed entirely and commission largely so
(M-SWAP-1). Specifying size by **risk allocation** is therefore the only expressible form — and it is
the *right* form on two independent grounds:

1. **It matches how the rail actually sizes.** Live c1 sizing is
   `r_eff = BASE_RISK × DD_SCALE × lifecycle`, floored to integer qty, **with the cap as a ceiling** —
   risk-driven, not cap-derived. `alloc = 0.0075` is exactly `1.50% × 0.50×`.
2. **It is cap-feasible, so nothing is smuggled.** `scale = 1500/2912.96 = 0.515×` of `ae744`
   ⇒ ≈ **5.85 contracts** on avg qty 11.36 — **inside cap 8**. No granularity lockout, no cap breach.

**The correction is STRICTER than the void arm, and that is the auditable point.** 0.515× carries
**+46.2%** more size than the void arm's 0.352×, hence more variance, hence a *harder* gate. A fresh
pre-reg that makes the test harder cannot be gate-lowering — which is the objection close-and-reopen
must always answer.

**What this run therefore does and does not measure.** It measures **variance composition at the
deployed risk allocation**. It does **not** price contract cap or commission — those are governed by
the standalone survival measurement (J4b/J8/J10), and §8 forbids reading this run as if it did.

## §3 — Preconditions

- **P1 — Mon+Wed variant, not the panel.** Tuesday trades are dropped (S5). Expect **dropped 28 /
  retained 124** on `ae744` (28 Tue of 152). Must be printed (§7 C3). *Carried from Q-6JCOMPOSE-1 P1,
  operator-accepted 2026-07-29; counts re-derived for `ae744`.*
- **P2 — cap 8 inferred.** Operator-accepted as inferred 2026-07-29, verification delegated. **Now
  non-binding for this run**: cap enters only as the feasibility check in §2.1, and 5.85 < 8 holds for
  any cap ≥ 6.
- **P3 — basis.** **DISCHARGED BY CONSTRUCTION** — the frozen primitive does the de-compounding and
  1R pinning; the `EXPECTED_1R_AEGIS` guard fails loudly if the panel or basis drifts. Controlled by
  §7 C2.
- **P4 — panel identity.** **DISCHARGED** — ledger J11 (`ae744` KNOWN-config, H1-covering).
- **P5 — engine equivalence.** Requires §7 C1 green. **C1 is already running** (unmodified engine,
  ORB row) and its result is inherited.

## §4 — Falsifiable hypothesis + disclosed prior

**H:** Adding Aegis-6J (`ae744`, Mon+Wed, `alloc = 0.0075`, frozen basis) to the 2-leg c1 book at
WATCH-1 0.50× keeps composed bust **≤ 3.0% on all four partitions** (full, H1, H2, bootstrap-95th)
**and** P(pass) ≥ 50%.

**If** all four partitions are ≤ 3.0% **and** P(pass) ≥ 50%, **then** H holds and the leg is
*screenable* (not admitted — §8). **If** any one partition exceeds 3.0%, **or** P(pass) < 50%,
**then** H is FALSIFIED and D2's survival objection is re-established on the composed quantity that
actually governs. **If** either control C1 or C2 is red, **then** no verdict is read at all and the
run is VOID.

| Observation | Threshold | Conclusion |
|---|---|---|
| max(full, H1, H2, boot-95th) | ≤ 3.0% **and** P(pass) ≥ 50% | H holds → **RESOLVED-SCREENABLE** |
| max(full, H1, H2, boot-95th) | > 3.0% **or** P(pass) < 50% | H falsified → **FALSIFIED** |
| controls C1/C2 not green | — | **VOID** (no verdict read) |

**Disclosed prior, unchanged and now stronger: FALSIFIED expected.** Grounds: the standalone leg
fails on the H1-covering panel (6.26% / 3.43%, directional), Q-COMPOSE-1 took the book 2.65% →
38.75% on a leg whose standalone numbers were fine, and this arm is **+46.2% larger** than the one
previously contemplated. Recording the expectation is the point — an unrecorded prior is what this
line keeps getting caught by.

## §5 — Forbidden moves

- **No sweep.** Exactly one composed cell. Any second composed cell in the artifact voids the run (§7 C4).
- **No engine edit.** Hook 2 must stay empty. A wrapper supplies input; it never changes a constant.
- **No re-selecting the arm after seeing a number.** `alloc`, panel, session set and tier are fixed in
  §2; if any must change, this pre-reg **closes** and a fresh one opens (no in-place amendment).
- **No reading cap or commission conclusions out of this run** — the gate is scale-invariant and
  cannot see them (§2.1, §8). Those belong to the standalone measurement.
- **No incumbent cap re-allocation** (hook 5): MYM 69 / MNQ 11 stay put.
- **No verdict if a control is red.** The run is VOID, not "reported with caveats".
- **No substituting `8e269` for `ae744`** to make §7 C3's predecessor counts line up — that would
  reinstate the H1 zero-fill defect this pre-reg exists to avoid.

## §6 — Verdict grammar

`RESOLVED-SCREENABLE` / `FALSIFIED` / `VOID` (controls red) / `AMBIGUOUS` (a partition lands within
Monte-Carlo noise of 3.0% — report the CI and do not round toward a verdict).

## §7 — Controls (all green before any 6J number is read)

- **C1 — engine equivalence.** Unmodified engine must reproduce the published Q-COMPOSE-1 ORB row
  (**38.75 / 54.73 / 25.84 / 47.14** at `Tradeify_Select_100K`). *Inherited — running.*
- **C2 — basis / non-perturbation.** With the 6J column supplied as **all zeros**, the composed run
  must reproduce the 2-leg baseline **0.11 / 0.22 / 0.04**. Any deviation means the wrapper perturbs
  the incumbents ⇒ VOID.
- **C3 — variant disclosure.** Print dropped (**expect 28**), retained (**124**), and Mon+Wed net.
- **C4 — single-cell.** Exactly one composed cell for `Tradeify_Select_100K` in the artifact.
- **C5 — guard armed.** `EXPECTED_1R_AEGIS` ($2,912.96 / n=11) must be asserted, not bypassed.

**K accounting: no new discovery K.** Pre-existing candidate, ratified gate, one inherited cell.
A measurement against a standing gate, not a search.

## §8 — What a PASS licenses (and does not)

A PASS makes the leg **screenable**, nothing more. It does **not** admit a third leg, authorize a
rail change, license spend, or unpark D2 — those need an amending ADR + operator GO. It does **not**
speak to contract cap or commission (§2.1). And it does not override the standalone window finding;
it composes with it.

## §9 — Operator sign-off

**SIGNED / FROZEN: 2026-07-29 / JA** — operator approval in-session, verbatim: *"I want both,
proceed with your recommended actions"*, answering both open decisions (single-tier §2 amendment,
and signature). Freeze is in effect from this commit; the body is **no longer amendable in place**
(Trap #12). Any change from here closes this pre-reg and opens a fresh one.

- [x] **§2.1 read and accepted** — the arm is specified by **risk allocation** (`alloc = 0.0075`),
      cap 8 / $3.10 commission are **explicitly out of scope**, and the arm is **+46.2% larger
      (stricter)** than the void predecessor's.
- [x] **§8 accepted** — a PASS admits nothing.
- [x] **Mon+Wed variant accepted** — 28 dropped / 124 retained on `ae744`.
- [x] **Single-tier restriction accepted** (§2, amended pre-signature) — `Tradeify_Select_100K`
      only, ~76 min → ~19 min; thresholds untouched; **the engine's aggregate verdict string is not
      this pre-reg's verdict** (RESOLVED is structurally unreachable at `n_tiers = 1`).

**Pre-signature amendments disclosed (both legal, both made while §9 was unsigned):** (1) the
single-tier restriction above; (2) §4/§5 reformatting to satisfy `check_brief` (explicit if/then
falsifier, bulleted forbidden moves) — no threshold, arm element, or control was altered by it.
`check_brief` 6/6 at signature.

**Controls status at signature:** **C1 GREEN** — exact digit-for-digit reproduction of
38.75 / 54.73 / 25.84 / 47.14 ([record](../../../lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/C1_CONTROL.md)),
so §3 P5 is discharged. **C2 not yet run** — it executes as the first step of the run, and a red C2
means VOID with no verdict read.

**Author's recommendation: sign.** Phase-0 is done, C1 is running, the basis defect that voided the
predecessor is corrected in the conservative direction, and the run is one engine invocation at $0.

## §10 — Audit hooks (runnable)

**Hook 1 — freeze precedes execution.**
```bash
git log -1 --format=%ci -- docs/briefs/pre-registration/Q-6JCOMPOSE-2-verdict-preregistration.md
```
**Hook 2 — engine unmodified (must be empty).**
```bash
git diff --stat HEAD -- lab/archive/q_compose_1_2026-07/run_compose_regime_remc.py
```
**Hook 3 — baseline still current (must return line 15).**
```bash
rg -n "0\.11% / 99\.80%" lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md
```
**Hook 4 — S5 collision reproduces on the ARM's panel (`ae744`): Mon 51 / Tue 28 / Wed 73 / Thu 0 / Fri 0.**
```bash
python lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/s5_day_distribution.py --panel ae744
```
**Hook 5 — no cap re-allocation (must show MYM 69 / MNQ 11).**
```bash
rg -n "cap_alloc" ops/c1_rail/c1_sizing_host_reference.py
```
**Hook 6 — scale-invariance is real (the defect that voided the predecessor).** Must print `True`.
```bash
python -c "print(abs((0.0075*200000/2912.96)-(0.0075*200000/(2912.96*3)))>1e-9 and round(0.0075*200000/2912.96,6)==round((0.0075*200000*3)/(2912.96*3),6))"
```
**Hook 7 — lock untouched.**
```bash
python scripts/validate_params.py && git diff --stat HEAD -- core/ ops/c1_rail/c1_sizing_host_reference.py
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/pre-registration/Q-6JCOMPOSE-2-verdict-preregistration.md --type inquire
```
