# Strategy Authorization Lifecycle

**Status:** Active — **canonical owner** of the authorization axis and the five ratified lifecycle values.
**Established:** 2026-07-10.
**Decision record:** [`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`](../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md) (`Accepted`, ratified 2026-07-10). The ADR carries the *reasoning*; this file carries the *values* and is what downstream (CLAUDE.md, code, STATE.md) points at.
**Supersedes-in-part (Call 5 up-asymmetry):** [`S5 ADR`](../adr/2026-08-07-loop-s5-bounded-promotion-lane.md) (`Accepted` 2026-08-07) — bounded sandbox-up exception only; see Call 5.
**Forward triggers:** registered on the [`STATE.md`](../../STATE.md) forward-trigger board (first eval **2026-08-08**).
**Stage-map pointer:** this file is the capital-authorization mechanism that stage 5 of [`docs/governance/systematic-trading-lifecycle.md`](../governance/systematic-trading-lifecycle.md) feeds. Call-5 WATCH-tier demotions are reversible OUTER acts (rules-mandated; no STRATEGIC sign-off). Only `RETIRED` and full beta shutdown are instrument-tier Deletes and therefore STRATEGIC-LoR per [`three-loop binding` D2](../adr/2026-06-12-three-loop-methodology-binding.md).

---

## Why this exists (one paragraph)

Live edges decay, and "consistent over time" can only be *disproven*, never confirmed. So a strategy cannot be authorized to hold capital *indefinitely* — but its parameters should still be immutable (anti-overfitting). The word "LOCKED" was silently doing both jobs. This file splits them: **parameters stay `LOCKED`** (stronger than before), while **capital authorization becomes an explicit, always-revocable, graded axis** governed by pre-registered triggers — so decay is met by a cheap reversible de-risk fired by a *rule*, not by in-the-moment discretion (the −$4,188.85 receipt, `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`).

## The two orthogonal axes

| Axis | Values | Mutable? | Owner |
|---|---|---|---|
| **Parameter** | `LOCKED` | **No** — SL/TP/ATR/risk%/pyramid/session/BE/trail + Pine source are immutable | Pine source + `dd_protection.py` / `firm_rules.py` (per Rule 0) |
| **Authorization** | `CANDIDATE → AUTHORIZED → WATCH{-1,-2} → RETIRED` | **Yes — always revocable** (down only, plus S5 bounded sandbox-up; see Call 5) | this file |
| **Durability-source tag** | `{MECHANISM \| SURVIVAL-ONLY}` | set at go-live; selects surveillance regime | this file |

**Third axis (venue binding), Accepted 2026-08-22:** BOOK → VENUE EDITION → DEPLOYMENT — [`venue-binding ADR`](../adr/2026-08-05-strategy-venue-binding-axis.md). Does not edit this table or `core/lifecycle.py`. Registry: [`ops/venue_editions/Tradeify_Select_100K.md`](../../ops/venue_editions/Tradeify_Select_100K.md) (Phase 1 landed; live set empty).

A live strategy's descriptor is the triple **`<version> · LOCKED · <authorization> · <durability-source>`** — e.g. *"Guardian v5.5 · LOCKED · AUTHORIZED · MECHANISM."*

This axis is **orthogonal** to `dd_protection` (intra-challenge drawdown, this account/window) and to observation-disposition routing (finding disposition — Notice-log's `GRADUATE/DROP/HOLD` for narrative findings; `observation_routing.md`'s Closed/Action/Forward survives only as one mechanical gate's exit codes, per [`ADR 2026-08-15`](../adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md)). It composes with them; it replaces neither. Because the lifecycle multiplier only ever *reduces* size, any WATCH-active book is strictly lower-risk than the AUTHORIZED-state MC config (historical pin: [`docs/mc_anchor_history.md`](../mc_anchor_history.md) · gated headline [`CLAUDE.md`](../../CLAUDE.md) §Strategy Reference) — the bust/DD gates move only safe-side, so a de-risk **never requires a re-MC**.

---

## Ratified values (operator, 2026-07-10 — all five calls accepted as recommended)

### Call 1 — Decay-detection threshold (the regret preference)

A live edge in a normal drawdown and a dead edge are statistically indistinguishable in the window where you must act — so this is a **regret preference set in advance**, not a detection rule that can be made "correct." Same structural shape as the §Protection revert trigger: a rolling metric vs a pre-registered floor, with **persistence** so a single drawdown cannot trip it. Action is **de-risk (→ WATCH), never kill** — which is what makes the tight setting affordable.

- **Metric:** rolling live **PF vs its MC/backtest baseline** (per-strategy baseline in [`.claude/skills/trade-csv-reconcile/references/baselines.md`](../../.claude/skills/trade-csv-reconcile/references/baselines.md)). ECR **corroborates but does not trip** (accrues too slowly — Q-NAS-ECR-1). The CFD-era engine (`ops/live_journal/scripts/ecr_rolling.py`) was **RETIRED 2026-07-11** with the manual-CFD estate; if a self-funded fill source returns, rebuild repo-native (estate ADR §4) — do not treat the deleted path as live.
- **Floor (ratified):** rolling live PF below **[baseline PF − 1.0σ of the MC PF distribution]** for **2 consecutive** review windows → demote one tier (→ WATCH-1).
- **σ = 1.0** (tighter than a kill-trigger's 2σ, *because* the action is reversible); **window = the review cadence** (Call 3); **consecutive count = 2**.
- **Below `AUTHORIZED` / at `CANDIDATE`:** the coded demotion ladder in `core/lifecycle.py` starts at `AUTHORIZED`. Action-on-breach when authorization standing is `CANDIDATE` is **not** an autonomous tier-step — ratified rule (`Accepted` 2026-08-21): operator review flag only; `RETIRED` remains Call 5 — [`docs/adr/2026-08-06-candidate-call1-action-on-breach.md`](../adr/2026-08-06-candidate-call1-action-on-breach.md).
- **Provisional-until-data:** with manual trading retired and the automated rail **built / disarmed / no book deployed**, live PF may not accrue to a minimum trade count for a long time. These floors are **pre-registration against future data**, not live-evaluable at 2026-08-08 — the ADR §6 AMBIGUOUS clause governs, re-confirm at 2026-11-08 if the count is short.

### Call 2 — Sizing as the response variable (stepped, not smooth)

Authorization is **continuous in effect, discrete in mechanism**: stepped tiers, never a smooth `f(confidence)` curve (a smooth curve invites continuous discretionary micro-adjustment — tinkering in a lab coat). Steps are auditable.

**Ratified tier ladder:**

| Tier | Lifecycle multiplier | Meaning |
|---|---|---|
| `AUTHORIZED` | **1.00×** | full durability confidence |
| `WATCH-1` | **0.50×** | one decay trigger fired; degrading |
| `WATCH-2` | **0.25×** | second trigger / deeper degradation |
| `RETIRED` | **0.00×** | capital withdrawn; authorization revoked |

**Integration layer (ratified — corrected against production).** There is **no unified sizing product** in the code: [`core/dd_protection.py`](../../core/dd_protection.py) scales `risk_pct` (inside TradingView), the live sizing host [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py) scales quantity (outside TV), and they **never meet in one expression**. ⚠ **Corrected 2026-08-03:** this sentence previously named `ops/accounts.py` `calc_multiplier`, deleted 2026-07-24 with the continuous-lot spine (`ff3510d`, substrate Phase 2). ⚠ **Path corrected 2026-08-06 (claim-alignment M26):** the 08-03 repair omitted the `c1_rail/` segment. The outside-TV layer is the c1 rail's integer-quantity sizing host, which imports `TIER_MULTIPLIER` via `from lifecycle import TIER_MULTIPLIER` ([`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py) — cite the symbol, not a line anchor). The lifecycle multiplier is a **per-strategy risk-authorization haircut** and lands at the **risk_pct layer, compounding multiplicatively with `DD_SCALE`**:

```
risk_pct_live[strategy] = BASE_RISK[strategy] × DD_SCALE × lifecycle_multiplier[strategy]
```

Consequence (ratified as intended): a strategy **both** decaying (WATCH-1, 0.50×) **and** in portfolio drawdown (`DD_SCALE`, 0.40×) sizes to **0.20×** risk_pct — two independent de-risk signals correctly stack. Placement is ~equivalent to an account-layer placement (Pine ~linear in risk_pct); the build-time contingency is **Pine pyramid-nonlinearity parity** (DJ30 750% / NAS100 1000%) — if scaling input risk_pct does not scale the pyramided stack proportionally, apply the haircut at the **quantity layer** instead (operational fallback — see the CONFIRMED-FALLBACK entry below for what realizes it today).

**Axis-separation invariant (non-negotiable).** The lifecycle factor **multiplies** `BASE_RISK` / `DD_SCALE` / `DD_TRIGGER` at compute time; it **never edits** them (they stay byte-identical; MVD spec-pin is the literals `if DD_TRIGGER != 0.015:` / `if DD_SCALE != 0.40:` in `core/dd_protection.py` (currently ~L292/L297) — cite by literal so the pin cannot re-stale). A tier change that mutates any locked constant is an integrity failure (ADR §4 trigger 3). Round-down/never-up is preserved at the sizing host's integer-quantity floor (`calc_multiplier` was its prior home and is deleted).

### Call 3 — The explained/unexplained differential

Dropping the explanation requirement moves the invoice from the "mechanism" line to the "statistics + surveillance" line — **the bar rises to pay it**. The **durability-source tag** carries this. Direction is fixed: `SURVIVAL-ONLY ⟹ smaller start / faster review / tighter trigger` than `MECHANISM`.

| | `MECHANISM` | `SURVIVAL-ONLY` |
|---|---|---|
| **Starting tier** | `AUTHORIZED` (1.0×) | `WATCH-1` (0.5×) — one-tier haircut |
| **Promotion to AUTHORIZED** | n/a | only after **one full regime-check cycle AND ≥ a minimum live-trade count** (pre-registered before go-live) |
| **Review cadence** | quarterly regime-check dates | **2×** (quarterly regime check **+** one interim) |
| **Call-1 trigger tightness** | 2 consecutive windows | **1** window |

**Portfolio nuance (load-bearing):** all four *current* legs are one mechanism-adjacent shared beta (Q-MECH-1), so at portfolio level the durability question is about *the beta*, not each leg. The per-leg `SURVIVAL-ONLY` regime therefore bites hardest on **new** additions — residual-program lanes (R5 DJ30/MYM, Aegis→6J, Guardian-MGC/R7) and any unexplained signal from the discovery stack (STUMPY/PySR/matrix-profile). Those enter `SURVIVAL-ONLY` by default. (This is why the per-leg tier machinery can be *built* after the beta monitor — see Implementation status.)

### Call 4 — The beta-level trigger (the portfolio killer) — SEQUENCE FIRST

Because the four legs are one beta, decay can arrive **portfolio-wide at once**; correlated simultaneous degradation is the signature of the *shared beta dying*. This is the only **portfolio-fatal** trigger and is structurally low-n (possibly zero calibration events before the real one) — pre-registered from the existing regime-split evidence (`docs/adr/2026-06-07-decompound-remc-hold.md`, the 2020–23 adverse half), most-conservative action.

- **Soft flag (ratified):** **2 of 4** legs simultaneously in `WATCH` within one regime-check window → pull the next review forward; run the transfer-entropy / lead-lag **beta-cohesion** check across the four legs + parents.
- **Beta-death trigger (ratified):** **3 of 4** legs simultaneously in `WATCH` within one regime-check window → **portfolio-wide de-risk to 0.50×** (a beta-level lifecycle multiplier across all legs) **AND** raise a **mandatory operator GO/NO-GO** on full shared-beta shutdown. Autonomous action stops at 0.5×; going to zero is operator-confirmed (Call 5).
- **First evaluation: 2026-08-08**, reusing `time_to_pass.py --regime-check` + a new beta-cohesion read.

### Call 5 — The automation boundary (reversibility)

The boundary is **reversibility**, inheriting the repo's existing asymmetry (`dd_protection` computes 0.40× with no sign-off; sizing always rounds **down, never up**).

**Rail caveat (read first):** the c1 rail is **built, warm, and disarmed** — posture owner [`CLAUDE.md`](../../CLAUDE.md) §Live-execution posture · ops routing [`.claude/skills/c1-rail/SKILL.md`](../../.claude/skills/c1-rail/SKILL.md) · environment [`S1 ADR`](../adr/2026-08-07-loop-s1-environment-ratification.md). Manual CFD trading is retired; **no strategy is deployed** (Striker legs withdrawn 2026-08-04). Call 5 binds the rail's autonomy boundary; today "autonomous / fires without the operator" means **"rules-mandated, no fresh in-the-moment judgment"** on the authorization axis — arming / live send remain operator GO + M1 (see c1-rail skill), not this file.

- **Reversible de-risk → autonomous (rules-mandated):** tier demotions (AUTHORIZED→WATCH-1→WATCH-2), Call-1 firings *on the coded ladder*, and the Call-4 soft flag + 0.5× beta de-risk fire without fresh operator judgment.
- **`CANDIDATE` Call-1 breach → not autonomous demotion** (`Accepted` 2026-08-21): no reversible rung below AUTHORIZED is coded; mandated action is operator review flag only — [`docs/adr/2026-08-06-candidate-call1-action-on-breach.md`](../adr/2026-08-06-candidate-call1-action-on-breach.md).
- **Irreversible retirement → operator GO/NO-GO against pre-registered criteria:** WATCH-2→`RETIRED` (capital to zero) and full beta shutdown. Operator role = **verification of pre-registered criteria**, not fresh judgment at max load (mirrors R6). Same Call-5 gate applies to any `CANDIDATE`→`RETIRED` path.
- **Hard asymmetry (load-bearing):** automation may move authorization **down only**, with **exactly one** bounded up-exception — the sandbox promotion lane in [`S5 ADR`](../adr/2026-08-07-loop-s5-bounded-promotion-lane.md) (`Accepted` 2026-08-07): gate-validated candidates may be admitted into a capped sandbox (micro size · fixed per-candidate loss/attempt budget · capped concurrency); the operator approves **budgets** not candidates; every ceiling-crossing stays operator-only; demotion stays universal and instant. Outside that lane, automation may **never** promote a tier, re-enter a RETIRED strategy, increase size beyond the authorized tier, or re-optimize. Automate the protective direction; gate every risk-adding direction (sandbox admit is the sole pre-registered exception).

---

## Forbidden moves (the "locked-harder" column)

These are locked *tighter* than any parameter, so "living authorization" cannot decay into "fiddling":

- **Decay is never a re-optimization trigger.** A decayed strategy is retired to zero, not re-fit. Any replacement is a **new hypothesis with fresh K-accounting + fresh out-of-sample**, not a "tuned version" of the dead one (inherits `rejected_candidates.md` / `rejected_signals.md`).
- **Decay/kill thresholds are themselves LOCKED at authorization.** You may revoke capital; you may **not** move the line that triggers revocation once it is live. Approaching a threshold is not license to move it.
- **Surveillance is scheduled measurement against pre-set thresholds — not continuous discretionary P&L-staring.** Look on cadence; the only permitted outputs are the fixed menu {hold / de-risk one tier / retire}. No in-the-moment threshold-editing, no re-fit, no fifth option under drawdown stress (inherits `observation_routing.md`: Action requires a triggering rule).
- **No autonomous size-up outside the S5 sandbox.** Automation moves authorization down only, except the bounded sandbox-up lane ([`S5 ADR`](../adr/2026-08-07-loop-s5-bounded-promotion-lane.md)); ceiling-crossings and size past sandbox remain operator-only.
- **No loosening a trigger in place because a drawdown got uncomfortable.** Fire the trigger openly (supersede the ADR) or hold. The discomfort *is* the named cost (verbatim from `2026-06-30` §5).
- **The lifecycle multiplier may not touch any LOCKED parameter.** It multiplies against `BASE_RISK`/`DD_SCALE`/`DD_TRIGGER`, never edits them.

---

## Implementation status

- **2026-08-06 — claim-alignment M26+C20:** sizing-host path corrected to `ops/c1_rail/c1_sizing_host_reference.py` (drop stale `:54` line anchor; cite `from lifecycle import TIER_MULTIPLIER`); MVD pin cited by `DD_TRIGGER`/`DD_SCALE` literals; L113 modality demoted to *would realize* + 8/60 exact worked check (9/67 provenance-only). No edit to `core/dd_protection.py` or `core/lifecycle.py`.
- **2026-07-10 — decision `Accepted`** (ADR ratified). Canonical values recorded here.
- **2026-07-10 — Phase 2 docs** (this file + CLAUDE.md authorization-axis note + STATE.md forward-board entries): **DONE** (commit `285b2ad`).
- **2026-07-10 — Phase 2 code items 1–2: DONE** (`core/lifecycle.py` + `dd_protection.py` wiring + `tests/test_lifecycle.py`). The per-strategy `lifecycle_multiplier` is applied at `scaled_risk` as `BASE_RISK × DD_SCALE × lifecycle` (default 1.0× ⇒ behavior-neutral; full suite green + CLI-driven: Guardian WATCH-1 ⇒ risk_pct 0.34%→0.17%, RETIRED ⇒ 0.00%). Axis-separation pinned (a tier change leaves `BASE_RISK`/`DD_SCALE`/`DD_TRIGGER` byte-identical). `lifecycle_state.json` is the runtime tier interface (gitignored; absent ⇒ all AUTHORIZED).
- **CONFIRMED-FALLBACK — Pine pyramid-parity (2026-07-17):** TV observation [`Q-PYRPARITY-1`](../briefs/Q-PYRPARITY-1-watch1-pyramid-proportionality.md) → [`closure`](../briefs/closures/Q-PYRPARITY-1-closure-falsified-nonproportional.md) / [`RESULTS`](../../lab/archive/q_pyrparity_1_2026-07/RESULTS.md) fired **`FALSIFIED-NONPROPORTIONAL`**. Pine is linear in `riskPerTrade` (Phase 0); MYM1! binds a TV/symbol qty ceiling (17 base / 127 add @ $200K) so halving the risk% input does **not** halve the pyramided stack when the ceiling binds. **Operational rule:** for DJ30/MYM and NAS100/MNQ, realize a WATCH-tier haircut at the **quantity layer**, not via TV risk%-input scaling. ⚠ **Route corrected 2026-08-03** (gate-stack audit R7): this rule previously named `ops/accounts.py` / `cli.py lots`, both deleted 2026-07-24 (`ff3510d`). The layer that **would** realize it is [`ops/c1_rail/c1_sizing_host_reference.py`](../../ops/c1_rail/c1_sizing_host_reference.py) (nothing realizes a live WATCH haircut today — both c1 legs withdrawn 2026-08-04; rail retained warm/disarmed under [`S1`](../adr/2026-08-07-loop-s1-environment-ratification.md)), which computes `r_eff = BASE_RISK × DD_SCALE × M_lifecycle(tier)` and **floors to integer contracts** — a quantity-layer application. Whether integer flooring fully discharges the pyramid-parity contingency is **base-dependent** (exact at even reserve bases, lossy at odd ones) and must be evaluated at the leg's actual `cap_alloc`-derived base — see [`docs/spec/c1_watch_realization_multiplier_layer.md`](../spec/c1_watch_realization_multiplier_layer.md) §2 worked check **8/60**, where `floor(8 × 0.50)/8 = 0.500` (exact). The older `floor(9 × 0.5)/9 = 0.444` figures are retained in that spec **for provenance only** and must not be quoted as current. This is the rail's question to answer, not this document's. Risk-input scaling remains fine for flat (non-pyramided) legs.
- **2026-07-10 — Phase 2 code, Call-4 control + Call-1 pure logic: DONE.** `core/lifecycle.py`: `beta_death_assessment` / `get_effective_multipliers` (2-of-4 → soft flag; 3-of-4 → autonomous portfolio **0.50× on every leg** + operator GO/NO-GO), wired into `dd_protection` sizing + an honest BETA-DEATH display banner; `decay_breach` (the Call-1 `PF < baseline − k·σ` test, k=1.0) / `next_tier_down` / `autonomous_demote` (tier ladder; autonomous demotion **caps at WATCH-2** — WATCH-2→RETIRED is operator-gated, Call 5). Constants pinned (2/3/0.50). Behavior-neutral today; CLI-verified (3-of-4 ⇒ every leg ×0.50 + banner).
- **Pending — data-dependent Phase 2 code:** (a) **Call-1 σ-source + harness** (reads `baselines.md` + a live-PF source; applies `decay_breach`/`autonomous_demote`; writes demotions into `lifecycle_state.json`) — σ-source design in flight; (b) the **beta-cohesion diagnostic** (transfer-entropy/lead-lag, informs the soft-flag interim review) — design in flight.
- **DONE, THEN RETIRED — `ops/cli.py lots` read-only auth surface** (built 2026-07-10; retired 2026-07-24, `ff3510d`): loaded `get_lifecycle_multipliers` and printed a de-auth caution when any leg sat below AUTHORIZED; deliberately did **not** apply the haircut. Retired with the continuous-lot spine. **No successor read-only auth surface exists** — the de-auth caution is currently unrendered anywhere. Recorded as a gap, not repaired here.
- **Sequencing:** build **Call 4 (beta-death monitor) first** — it defends the shared-beta exposure. The transfer-entropy/lead-lag beta-cohesion read is the concrete first artifact, first eval 2026-08-08.
- **Scope note (Delete-until-needed):** the four current legs are one beta, so the per-leg tier machinery is largely inert today — Call 4 is what bites. The per-strategy tier state-machine can be built when the first `SURVIVAL-ONLY` addition needs it; do not gold-plate a four-leg one-beta book.

## Audit hooks

```bash
cd "C:/Users/joshu/multi_firm_operations"
# The five ratified values live here (canonical owner).
grep -nE "1\.00×|0\.50×|0\.25×|0\.00×|risk_pct layer|2 of 4|3 of 4|SURVIVAL-ONLY|MECHANISM" docs/methodology/strategy_lifecycle.md
# Authorization vocabulary is in CLAUDE.md OUTSIDE the LOCKED table. Use DISTINCTIVE
# tokens — a bare grep for WATCH/RETIRED also hits pre-existing prose (Trap M-AHF).
grep -n "Strategy Authorization Lifecycle\|durability tag\|risk_pct-layer" CLAUDE.md
# No locked constant edited by the lifecycle work (pre-code-phase).
git diff --stat HEAD -- core/dd_protection.py core/firm_rules.py core/config/params.toml
# Forward triggers registered; next eval 2026-08-08.
grep -n "decay review\|beta-death\|strategy_lifecycle" STATE.md
```
