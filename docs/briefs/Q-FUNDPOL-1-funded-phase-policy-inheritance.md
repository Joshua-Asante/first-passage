# Q-FUNDPOL-1 — The funded phase inherits the eval phase's policy by default; is that inheritance materially costly?

**Status:** `DORMANT 2026-08-04` — §6 hard scheduling gate **retired** (no eval can convert); Select-Flex thresholds **non-transferable** (new derivation at F3, not a reschedule). **§8 pre-registration DISCHARGED 2026-07-31** (`d0200a4`, [artifact](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md)); the run remains gated (§6 preconditions + the pre-reg §9 code contract). Nothing here authorizes a sizing change. ⚠ **This brief's §1/§7 funded-geometry prose is superseded** — see §8 (D1: verified four-rung ladder 30→40→50→80, no $1,000 payout minimum).
**Authored:** 2026-07-28
**Closed:** N/A
**Authors:** Joshua (directive: "proceed as recommended") + Claude Code (Opus 5, authoring)
**Parent question:** `Q-EVALSEQ-1` §7 — the fork it names and explicitly declines to open ("Funded-phase schedule — whether a *funded*-phase schedule exploiting the $100,100 floor-lock is a separate question … Not opened here.")
**Sub-questions opened:** none
**Loop:** Inquire-phase Pre-Q — closure gated on the §6 verdict read of a bounded MC over a frozen policy set, after the §6 preconditions clear
**Artifact path:** `docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md`

---

> ⚠ **DORMANT 2026-08-04 (claim-alignment M33) — obligation retired; analysis retained.**
> The §6 "hard scheduling gate" fires on an eval pass converting — **none can**. Every
> threshold under test is Select-Flex-specific; re-dating to F3 would be false precision.
> Preserve §8 pre-registration (`d0200a4`, K frozen = 4) and P1/P2 discharges **unspent**.
> **Do not build** §9-C1 `funded_sim(..., policy=)` or the `PAYOUT_MIN → 0` override.


## §0 — Rule 0 reads (production-source verification)

All anchors verified on 2026-07-28 via `git log -1 --format='%h %cs' -- <path>` at `602b692` (main).

- [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py) — anchor `c134060` (2026-07-24). **The symptom, read directly.** The sizing law is `r_eff = BASE_RISK[leg] × DD_SCALE(dd_state) × M_lifecycle(tier)`, `qty = min(floor(E_firm·r_eff / (SL_pts·$/pt)), floor(cap_alloc/(1+pyr%/100)))`. `rg -n -i "funded|eval_phase|phase"` returns **exactly one hit, a docstring** ("Phase-3 audit log row"). There is **no funded/eval branch anywhere in the live sizing host** — funded sizing is whatever the eval rung was set to. `LEG_MAP` pins `cap_alloc` MYM 69 / MNQ 11 against the firm's account-aggregate cap.
- [`core/firm_rules.py`](../../core/firm_rules.py) — anchor `cb60516` (2026-07-26). `Tradeify_Select_100K`: `dd_type="trailing_locking"`, `max_dd_pct=3.0` ($3,000), `profit_target_pct=6.0`, `micro_contract_cap=80`, `dd_lock_offset_usd=100`. **The lock is a real FUNDED mechanic** — the known defect (lines 264–290) is that the *eval* rows carry it, not that the mechanic is fictional. This brief concerns only the phase where it is real.
- [`core/dd_protection.py`](../../core/dd_protection.py) — anchor `656bbfe` (2026-07-22). `DD_TRIGGER = 0.015` / `DD_SCALE = 0.40`, applied multiplicatively in the same risk_pct layer. A funded policy would be a further multiplicative factor at that layer — it multiplies, never edits (axis separation).
- [`lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py) `funded_sim` (lines 210–250) — anchor `4fac99c` (2026-07-27). Read in full, ±20 lines. **`funded_sim` is NOT affected by the 2026-07-28 eval-lock defect** (that defect is `eval_sim`-scoped; funded accounts genuinely lock). Constants line 74–75: `FLOOR_LOCK_BAL=103_100`, `FLOOR_LOCKED=100_100`, `DD=3_000`, `TIER_UNLOCK=103_000`, `CAP_LO=40`, `CAP_HI=80`, plus `PAYOUT_CAP`/`PAYOUT_MIN`/`WIN_MIN`/`SPLIT`. Verbatim state machine:
  - `floor = np.where(locked, FLOOR_LOCKED, peak - DD)`
  - `locked |= peak >= FLOOR_LOCK_BAL` — equity trigger
  - `locked |= want` — **a payout request also locks the floor**
  - `want &= first | (bal > last_req)` — subsequent payouts require balance above the prior request
  - `cap = np.where(tier_hi, CAP_HI, CAP_LO)`; `tier_hi |= bal >= TIER_UNLOCK` — contract cap doubles 40→80
- [`docs/adr/2026-07-23-c1-rung-selection-ev-objective.md`](../adr/2026-07-23-c1-rung-selection-ev-objective.md) — anchor `9ab2e8b` (2026-07-23), `Accepted`. Rung-selection objective is EV-per-dollar-day **among regime-robust admissible rungs** (regime-robustness is a hard precondition, not overridden by EV). §2 scope is explicitly "the c1 book's rung selection only"; its A0b analysis is **eval-phase** (both-halves gate on eval bust). §5 forbids sizing above 1.00× (down-only ladder).
- [`docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md`](pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) — anchor `25bd4d8` (2026-07-24). The parent fork (§7) and the discipline this brief copies: a schedule is a fourth multiplicative factor at the risk_pct layer; K frozen; run gated; pre-registration ≠ recommendation. Its §2 also warns: "the funded floor-lock … sits past the eval target, so its benefit accrues mostly to the *funded* phase, not eval pass — do not over-credit it to the eval gate." **That deferred credit is this brief's subject.**

**Contingent venue-fact citation (Tier 2 — flagged, not assumed).** The **payout-triggered lock** ("or first payout, whichever first") and the funded start-tier thresholds are cited from [`docs/briefs/2026-07-23-tradeify-book-composition.md`](2026-07-23-tradeify-book-composition.md) §1 (anchor `4fac99c`), a secondary source, and are encoded in `funded_sim` as literals. **UPDATE 2026-07-29:** the payout-triggered lock is now **verified** against the published help-centre article and matches the model (see §6 P1). The **funded start-tier** figures cited from the same secondary source are **NOT** confirmed — the real ladder is 3 mini / 30 micro scaling **30→40→50→80** (EOD-calibrated), not a binary 40→80. `funded_sim` is wrong there and is being corrected under a separate spec; **any arm this brief runs must consume the corrected ladder**, since the start tier governs exactly the low-equity region where the funded floor binds hardest. — **LANDED 2026-07-29 (`78a6e8b`):** the ladder now has exactly one definition, [`funded_scaling.py`](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/funded_scaling.py), and `funded_sim` consumes it via `caps=` + an EOD one-way `latch`. **But the sibling correction did *not* land in that file** — `PAYOUT_MIN` is still the phantom `1_000.0` literal with no parameter hook, and it gates payout *timing*, which is half this question. Handling frozen in the §8 pre-registration (§1-D2 / §9-C2). Given that this session found two separate defects from exactly this class of unverified venue encoding, the payout-lock clause is a **§6 precondition**, not an assumption: if it does not exist, the "lock early via payout" lever vanishes and one whole policy family is void. It rides the already-owed Tradeify rule-pin dashboard verification (`STATE.md` operator-queue item 4).

---

## §1 — Context & motivation

Two structural facts collide. First, the live sizing host has **no funded-phase branch** (§0) — whatever rung the eval runs at is what a funded account would inherit, by omission rather than by decision. Second, the funded phase's geometry is **not the eval's**: `funded_sim` shows a floor that *freezes* at $100,100 once EOD peak reaches $103,100, a contract cap that *doubles* (40→80) once balance reaches $103,000, and a payout request that *itself* triggers the freeze at the cost of a balance ratchet. Those two thresholds sit **$100 apart**, so a single ~$3.1K climb simultaneously doubles position size and converts a trailing barrier into a fixed one. Nothing in the estate has characterized what that implies for policy.

The question is live now rather than after a pass because the answer is an input to sizing, and sizing is set before the account converts, not after. It is also **build-ahead-of-data** — no funded account exists, the rail is disarmed, and no strategy-signal fill has occurred — which is a legitimate posture in this estate (the lifecycle Call-1 harness landed the same way, 2026-07-14) but bounds the verdict to a *modeled* one with a live falsifier attached (§6).

Standing doctrine tested: the down-only lifecycle ladder ([`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md)); the `concept-not-constant` change-control chain ([`docs/adr/2026-07-13-dd-protection-concept-not-constant.md`](../adr/2026-07-13-dd-protection-concept-not-constant.md)); and the EV-objective scope fixed by ADR 2026-07-23 (§0), which resolved the *eval* rung and is silent on funded.

---

## §2 — Prior art / lineage

- **`Q-EVALSEQ-1`** (pre-registered 2026-07-24, run 08-08-gated) — the direct parent. Tests a *within-eval* front-load schedule; its §7 names the funded-phase schedule as a separate question and declines to open it. Its §2 explicitly defers the floor-lock's benefit to the funded phase. This brief opens exactly that fork and must not duplicate its eval-side K.
- **`ADR 2026-07-23` c1 rung-selection EV objective** (`Accepted`) — establishes the objective (EV/dollar-day) and the hard regime-robustness precondition, for the **eval** rung. Its A0b resolved NO-GO on 1.00× on eval-phase evidence. Funded is out of its stated scope, so this brief inherits its *objective form* and its *precondition*, not its verdict.
- **`Q-FUNNEL-1`** (`CLOSED-RESOLVED` 2026-07-22) — modeled funded payouts, but its own closure records: "**Floor lock-on-first-payout-request is not modeled** — the funded-phase continuation locks the floor only via the equity trigger." So the funnel harness lacks the very lever this brief is about, while `gap_stage2_capbound.funded_sim` has it. Instrument choice matters and is fixed in §7.
- **`2026-07-23-tradeify-book-composition`** — source of the funded mechanics and of `funded_sim`. Its **eval** figures are contaminated by the 2026-07-28 eval-lock defect (§Addendum there); its **funded** simulator is not. This brief consumes `funded_sim` and must not consume the contaminated `$339/acct-mo` as a baseline (§5).
- **`Q-CAPALLOC-1`** (`CLOSED-AMBIGUOUS (d)` 2026-07-27) — found the dominating `48/32` split "survives at the modeled $200 winning-day / **40-micro start tier** and dies … at an 80-micro tier." That is the same start-tier mechanic this brief is about, and it means cap allocation and funded policy are coupled, not independent.
- **`lesson_trailing_dd_survival_is_skew_governed`** (2026-07-25) — survival against a fixed-dollar barrier is governed by loss-side shape, not mean/vol. Directly relevant: post-lock the barrier is *fixed and far*, so the property that governs pre-lock survival stops binding after the threshold. This is the mechanism that makes the phase genuinely two-regime.

---

## §3 — Question (Q-FUNDPOL-1)

**Pre-Q gate test (symptom-only rephrase):** "The funded phase's barrier and cap geometry differ structurally from the eval's, and the live sizing host has no funded branch, so funded policy is whatever eval policy happens to be — inherited by omission. Whether that inheritance is costly, and in which direction, is unmeasured." No fix is baked in: the question does **not** ask "should funded size up after the lock."

**Q-FUNDPOL-1:** What does the funded phase's threshold structure (floor-freeze at $103,100 peak or at first payout; contract-cap doubling at $103,000; payout balance-ratchet) imply for the policy governing it, and does the inherited flat eval policy leave material value unclaimed or carry unpriced ruin risk?

---

## §4 — Falsifiable hypothesis (H-FUNDPOL)

**H-FUNDPOL:** The funded phase is a **distinct policy surface** — i.e. under the frozen policy set (§6) and the modeled funded geometry, at least one threshold-aware policy beats the inherited flat policy by **> 25% on expected net payout cash per account-month** at **no worse modeled ruin** (12-month funded mortality within +0 pp), **and** that lift holds in **both** regime halves. If so, funded policy must be selected on its own terms rather than inherited, and the finding routes to an operator fork + its own admitting ADR. **Otherwise** — no policy clears +25% at equal-or-better ruin, or the lift reverses across halves — inheritance is adequate, the funded lever is spent, and flat-by-inheritance stands as a *recorded* decision rather than an omission.

**Reject H-FUNDPOL → `FALSIFIED` if:** best policy's lift ≤ 25% vs the flat control, **OR** any policy achieving > 25% does so with higher modeled 12-month mortality, **OR** the sign of the best policy's lift reverses between H1 and H2.
**Accept H-FUNDPOL → `RESOLVED` if:** ≥1 policy shows > 25% lift **AND** mortality ≤ control **AND** same-sign lift in both halves.
**Ambiguous-hold if:** the best policy clears +25% and both-halves sign but its bootstrap band overlaps the control's (lift not separable from resampling noise), **or** the §6 payout-lock precondition resolves UNVERIFIED — re-test on the trigger named in §6.

The 25% floor is set at authoring time and is **not** a knob: it is the materiality threshold Q-FUNNEL-1 used (`0.25` relative lift, its `§3(a)` gate), reused so this brief's bar cannot be tuned to its own result.

---

## §5 — Forbidden moves

- **Reading the 2026-07-28 eval-lock fix as license to also "correct" `funded_sim`'s lock.** The funded lock is **real** (article 10495897 scopes locking *to* Sim Funded). Removing it would be the mirror image of the defect just fixed — and the temptation is live precisely because a lock was just deleted one function above it in the same file.
- **Consuming `$339/acct-mo`, `63%`, or `8.2 mo` as a baseline or objective calibration.** Those are contaminated by the eval-lock defect and are pending re-derivation. This brief's control is its own flat-policy arm run in the same harness, never a published figure.
- **Treating a post-lock free-roll as license to size above 1.00×.** The down-only ladder caps at 1.00× (`strategy_lifecycle.md`; ADR 2026-07-23 §5). The EV optimum is read at the ladder maximum, never past it — and "the floor is frozen so risk is bounded" is exactly the argument that makes exceeding it feel safe.
- **Adopting any winning policy from this brief without a separate admitting ADR.** A funded policy is a risk_pct-layer factor and inherits the `concept-not-constant` chain (pre-registered re-MC + both-halves regime gate + admitting ADR). Pre-registration ≠ recommendation (Q-EVALSEQ-1 §5).
- **Optimizing payout timing for lock-capture while ignoring the balance ratchet.** `want &= first | (bal > last_req)` means an early lock-capturing payout sets a floor on all future requests. A policy scored on "time to first lock" alone would look excellent and be wrong; every payout-timing arm must be scored on the full-horizon cash, not the lock event.
- **Re-opening the eval rung.** ADR 2026-07-23 resolved it (0.50×, A0b NO-GO on 1.00×). This brief is funded-phase only; using a funded result to argue an eval rung change is the forbidden override.
- **Outcome-conditional D-tests** — e.g. selecting the policy set after seeing which threshold behavior helps, or excluding paths that die before reaching funded. The policy set is frozen in §8 before Phase 1.

---

## §6 — Gate criteria (closure verdict)

**Preconditions (both must clear before Phase 1 runs; neither is a verdict):**
- **P1 — payout-lock clause verified against primary Tradeify source** — **DISCHARGED 2026-07-29, present as modeled.** Verbatim from the published help-centre article ([Select Flex and Select Daily Payout Policies](https://help.tradeify.co/en/articles/12853966-select-flex-and-select-daily-payout-policies)): "your drawdown locks at $100 above your starting balance … either automatically at EOD when your balance reaches $52,100 (for 50K), **or immediately when you request a payout — whichever comes first**." For the 100K tier that is lock **$100,100**, trigger EOD **$103,100** or first payout — matching `FLOOR_LOCKED` / `FLOOR_LOCK_BAL` exactly. **No policy family is void; the payout-timing arms stand.** Record: [`docs/notes/2026-07-24-tradeify-rulepin-verification.md`](../notes/2026-07-24-tradeify-rulepin-verification.md).
- **P2 — `funded_sim` reproduction control.** Re-run the published funded figures (`funded-dead-1y 43%` for the 2-leg book) and print MATCH/MISMATCH before any policy arm is scored. MISMATCH ⇒ halt; the harness or its inputs have drifted and no arm is interpretable.

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` | best policy lift **> 25%** on net payout cash per account-month vs the flat control **AND** modeled 12-month mortality ≤ control **AND** same-sign lift in both regime halves | Funded policy is a distinct surface → operator fork + its own admitting ADR (`concept-not-constant` chain). **No sizing change from this brief.** |
| `FALSIFIED` | best lift **≤ 25%**, **OR** any >25% arm carries higher mortality than control, **OR** best arm's lift reverses sign across H1/H2 | Funded lever spent. Record flat-by-inheritance as a **decided** policy, not an omission; close. |
| `AMBIGUOUS-HOLD` | best arm clears +25% and both-halves sign but its bootstrap band overlaps the control's (P1 discharged 2026-07-29, so that limb can no longer fire) | Re-test trigger: P1 verification lands, **or** the first funded account accumulates 12 months of live data — whichever first. |

**Hard scheduling gate:** this brief must reach a verdict **before the first funded account exists** (i.e. before an eval pass converts), because its output is a sizing input set in advance. It is deliberately **not** placed on the 2026-08-08 slate — that slate is already carrying the decay/beta reviews, the decompound re-MC, and Q-EVALSEQ-1, and this question has no calendar dependency, only an event one.

**Pre-registered before any data touches analysis.** Amending §6 mid-investigation is `p`-hacking at the methodology layer (Trap #12).

---

## §7 — Execution plan

Instrument fixed: **`gap_stage2_capbound.funded_sim`** — it is the only harness in the estate modeling the payout-triggered lock (Q-FUNNEL-1's does not, per §2) and it is unaffected by the eval-lock defect. `eval_sim` is **not** used by this brief.

- **Phase 0 — Rule-0 + preconditions.** Re-verify §0 anchors; discharge P1 and P2 (§6). Report both before any arm runs.
- **Phase 1 — Control.** Flat inherited policy (constant multiplier, no threshold awareness) through `funded_sim`; record net payout cash per account-month, 12-month mortality, time-to-first-payout, full-horizon cash.
- **Phase 2 — Frozen policy arms** (set fixed in §8, K frozen, no grid): the arms span (a) threshold-aware sizing around the $103,000 cap-unlock / $103,100 floor-lock pair, and (b) payout timing relative to the lock trigger, including the ratchet cost. Each arm scored on the same metrics as the control.
- **Phase 3 — Regime split.** Both-halves (H1/H2) re-score of the control and the best arm; sign agreement is a §6 limb.
- **Phase 4 — Verdict assertion.** Run §6 against actual numbers; produce the §9 closure artifact.

---

## §8 — Verdict pre-registration (mandatory before Phase 1)

A separate file at `docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md` containing the §6 table verbatim, the exact policy arm definitions with **K frozen**, the metric definitions, and the P1/P2 precondition handling — committed **before** any analysis script runs. The §9 closure references it by commit hash.

Pre-registration commit hash: **`d0200a4`**
Pre-registration date: **2026-07-31**
Artifact: [`docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md`](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md)

**§8 DISCHARGED 2026-07-31.** The §6 table and the §4 hypothesis are carried **verbatim** into the
pre-registration and are not amendable there. K frozen at **4** (`A1` lock-state step · `A2`
floor-distance-proportional · `B1` equity-lock-deferred payout · `C1` joint A1⊕B1), every θ pinned
to a ratified lifecycle rung, no grid, no draw on the instrument-ledger K seats.

**Three post-authoring corrections are recorded in the pre-registration's §1 — read it before
trusting this brief's §1/§7 prose:** (**D1**) this brief's "cap *doubles* (40→80)" is **superseded**
— the verified rule is a four-rung one-way EOD ladder **30 → 40 @ $101,500 → 50 @ $102,000 → 80 @
$103,000**, and the modeled `PAYOUT_MIN = $1,000` **does not exist** (Flex has no minimum). The
$103,000/$103,100 adjacency this question turns on is **intact**; (**D2**) the §7 instrument took the
ladder fix but **not** the payout-minimum fix — Phase 1 must override `PAYOUT_MIN → 0` via the proven
`run_capalloc.py` pattern, never an in-place literal edit; (**D3**) **P1 is strengthened**, not
weakened, by the 2026-07-31 FTA §11 precedence reversal (the help centre governs account parameters).

**§6 P2 is split, not amended** — its stated `43%` target is the *legacy*-ladder figure, so a verbatim
run would MISMATCH for the right reason. **P2-a** reproduces **42.77%** under the legacy ladder
(harness integrity); **P2-b** establishes **49.06%** at the frozen geometry. Rationale and reference
values in the pre-registration §6.

**This brief is not runnable until §8 is committed.** Authoring the question is not authorization to
run it. §8 is now committed; Phase 1 additionally requires the pre-registration's §9 code contract to
land and both P2 parts to print MATCH.

---

## §9 — Closure record format

- **If RESOLVED:** `docs/briefs/closures/Q-FUNDPOL-1-closure-resolved.md` (+ operator fork routing; no `recommendation.md` unless PROMOTE)
- **If FALSIFIED:** `docs/briefs/closures/Q-FUNDPOL-1-closure-falsified.md`
- **If AMBIGUOUS-HOLD:** `docs/briefs/closures/Q-FUNDPOL-1-closure-ambiguous.md` with the explicit re-test trigger from §6

Must include: verdict, anchor numbers vs gate thresholds, what §8 predicted vs what happened, P1/P2 discharge evidence, and lesson candidates with dated anchors.

---

## §10 — Audit hooks (runnable)

```bash
# §0 anchors still resolve (re-verify before trusting this brief later)
git log -1 --format='%h %cs' -- ops/c1_rail/c1_sizing_host_reference.py          # expect c134060 or later
git log -1 --format='%h %cs' -- lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py

# The SYMPTOM assertion: the live sizing host still has no funded branch.
# Expect ZERO hits. Any hit means a funded branch now exists and this brief's
# premise changed - re-read §1 before trusting anything downstream.
# (Adding `|phase` to the pattern returns one unrelated docstring hit, "Phase-3
# audit log row" - that is why the narrower pattern is the assertion.)
rg -n -i "funded|eval_phase" ops/c1_rail/c1_sizing_host_reference.py

# The funded lock mechanic this brief is about is still present and funded-scoped.
# eval_sim must NOT contain FLOOR_LOCK (fixed 2026-07-28); funded_sim MUST.
rg -n "FLOOR_LOCK_BAL|FLOOR_LOCKED|TIER_UNLOCK|locked \|= want" \
  lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py

# Contaminated figures must not appear as this brief's baseline (§5).
rg -n '\$339|63%|8\.2 mo' docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md
# Expect EXACTLY 3 hits, all benign: the §2 lineage note, the §5 forbidden-move
# line, and this hook's own line (self-match). Any FOURTH occurrence means a
# contaminated figure leaked into an objective or baseline - investigate.

# §8 must be committed before any Q-FUNDPOL-1 analysis script runs.
git log --oneline -- docs/briefs/pre-registration/Q-FUNDPOL-1-verdict-preregistration.md

# Parent fork lineage resolves both ways.
rg -n "Funded-phase schedule" docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md
```

---

## Verification

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md --type inquire
# Expected: all 6 checks PASS

# Rule-0 confirmation (the load-bearing symptom read)
rg -n -i "funded|eval_phase|phase" ops/c1_rail/c1_sizing_host_reference.py   # expect 1 docstring hit only
sed -n '210,250p' lab/analysis/c1/tradeify_book_composition_2026-07-23/gap_stage2_capbound.py

# Cross-reference: the parent fork exists and says what S2 claims
rg -n "separate question|Not opened here" \
  docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md

# Doctrine: the ladder cap S5 relies on
rg -n "1.00|down-only|ladder" docs/methodology/strategy_lifecycle.md | head
```
