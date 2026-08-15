# ADR 2026-07-15 — External-mechanism harvest intake (standing sourcing + admission screen)

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s5-bounded-promotion-lane.md` — per-candidate operator GO before capital/account action **only as applied to in-ceiling sandbox admits** (operator approves budgets not candidates). Stage-0 pre-registration, K bind, cost-law, and ceiling-crossing / account-funding GOs **stand**.
**Retain-until:** none
**Decision date:** 2026-07-15
**Authors:** Joshua (authority) + Claude Code (Fable 5, drafting — operator directive: "codify these recommendations so that this is how we harvest strategies from now on")
**Supersedes:** none — this ADR ratifies the **sourcing/admission front end** upstream of the campaign chain; it does not supersede the Campaign-defaults, statistics-adoption, DSR-K, or HARV-lane ADRs, and it does not re-open any closed screen verdict.
**Related:** [`2026-07-13-harv-discovery-lane-ratification.md`](2026-07-13-harv-discovery-lane-ratification.md) (campaign-level lane this intake feeds); [`docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md`](../briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md) (the frozen two-clause screen this ADR generalizes); [`docs/briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md`](../briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md) (`RESOLVED` 2026-07-15 — D5 the worked instance); [`docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md`](../briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) (Cursor-authored bounded literature Pre-Q, `LOCKED` 2026-07-16, PR #391 — **first execution instance under this ADR**, amended same day to inherit requirement 1 pre-Phase-1; see §1 reconciliation note below); companion procedure doc [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) (lands with this ADR; canonical on acceptance)
**Layer:** methodology (discovery-sourcing doctrine)

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR (session 2026-07-15, main checkout on branch `claude/strategy-factory-progress-31da50`, base `4ec95a4`):

- `docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md` — anchor `936a9e0` 2026-07-15 (freeze commit `b304f2c`; §E verdict **RESOLVED** fired 2026-07-15 with D5 PASS) — supplies the frozen two-clause formula this ADR generalizes: Clause K (`K_eff = K_intrinsic + K_banked(family)`, floor(K_eff) ≤ Cap 1.0 ⇔ K_eff ≤ 3, DSR ≥ 0.95 at V = 1/n) + Clause N (power = Φ(√N·|δ|/σ − 1.96) ≥ 0.50, δ cohort-cited, UNSCREENABLE-never-patched) + "a PASS never blesses"
- `docs/briefs/Q-KBUDGET-1-phase1-inventory.md` — anchor `1417b79` (ratification anchor `ca02030`, G2) — supplies the §C declaration 5-tuple (family→K_banked, design→K_intrinsic, era→N, cohort-cited δ/σ or UNSCREENABLE, blockers) reused as the seed-manifest schema
- `lab/archive/q_kbudget_1_2026-07/floor_scan.py` — anchor `936a9e0` — the production screen harness (hardcoded `AXES` list; the promotion target for the reusable module in §6/§7)
- `lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md` — anchor `4a2471e` at initial read, re-verified at `5a8713f` 2026-07-16 (PR #391 doc-sync: status header updated to reflect the already-ratified state; substantive derivation untouched) — the worked external-harvest instance: Baltussen et al. 2021 *JFE* NQ cohort, δ/σ = 0.113 (conservative t-scaled, not the 0.194 R² reading), power 0.947 at N = 1000; the SPX→NQ transplant refusal for the gamma-sign construct; the net-of-cost caveat
- `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — anchor `fad8984` (`Accepted` 2026-07-14) — the campaign-level lane this intake feeds; its reachability HARD gate blocks `register_search open`, not sourcing
- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` + `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` — anchors `fad8984` — the standing rules-of-evidence chain (referenced, not restated)
- `docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md` — anchor `fb9b9c9` (`STAGE-0 FROZEN · §R GO SIGNED 2026-07-15`) — proof the downstream chain consumes an intake-shaped seed end-to-end
- `lab/discovery/register_search.py` — anchor `67cc146` — `open --lane mechanism-first` rejects a missing/empty reachability attestation (the enforcement point a screen-PASS declaration binds to, pre-reg §C: "the manifest is the enforcement point")
- `lab/research_utils/deflated_sharpe.py` — anchor `48b8cef` — production floor arithmetic (`expected_max_sharpe`, `deflated_sharpe`) the screen and the promoted module both call
- `docs/rejected_candidates.md` — anchor `193c41c` — the dedup registry every seed checks first
- `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` — anchor `fad8984` — Stage-0 template the funded campaign inherits (LTM path; Read by path, not Grep)

---

## §1 — Context

Q-GATECART-1 (M-19) established that wide mining is structurally unfundable: banked K in the thousands puts the DSR demonstrability floor (2.05 at K = 3,177) above the best validated in-house edge (Aegis 1.83). Q-KBUDGET-1's frozen two-clause screen then showed the *only* axis class that clears the floor is externally-published, mechanism-first, ≤3-hypothesis seeds on unburned families — and its sole PASS (D5, Baltussen et al. 2021 *JFE*, ratified 2026-07-15, verdict RESOLVED) is exactly a publicly-harvested strategy. But that screen was a one-shot investigation artifact: its inventory was assembled once (Phase 1, ratified `ca02030`) and its re-screen trigger names only D5-input-supply / 2026-08-08. There is **no standing rule** governing how the *next* externally-sourced mechanism enters the ratified inventory — which sources count, what a seed must declare, what kills it before it costs anything, and who ratifies. Without one, each new seed re-derives the Q-KBUDGET machinery ad hoc, and sourcing quality drifts toward whatever paper is being argued for (the same drift §A of the screen pre-reg froze against, one layer up).

**Decision driver (one sentence):** the fundable-discovery bottleneck has moved from code (Gen-2 pipeline proven) and from axis-screening (frozen formula exists, RESOLVED fired) to **seed supply** — and the 08-08 → 11-08 runway needs a standing intake so new public-strategy seeds arrive screenable instead of arriving as arguments.

**Operator pushback incorporated (2026-07-15, same session):** two challenges landed against the initial four-requirement draft. First — given the downstream gate chain (HARV reachability HARD gate, universe gate, realism, survivor scoring), is pre-screening at intake redundant friction? Resolved by checking each requirement against what the gates actually catch (§2 below, per-requirement rationale) — three of four requirements protect a resource the gates cannot refund (banked K is permanent; an underpowered confirm can kill a *true* mechanism by producing an uninformative null that still enters the dead-list), so the bar stays. Second — the mechanism requirement as originally drafted excludes robust, well-replicated anomalies with no settled economic explanation (momentum-class effects), which is a real and unintended exclusion. Resolved by splitting requirement 1 into two satisfaction paths (§2 below) rather than weakening it uniformly.

**Parallel-work reconciliation (2026-07-16):** independently of this ADR's authoring, the operator directed Cursor to draft and lock a bounded literature Pre-Q — [`Q-KBUDGET-HARVEST-1`](../briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md), merged via PR #391 — that reinvents most of this ADR's mechanics independently: a near-identical four-field extraction template (K_banked / K_intrinsic / N / cohort-cited δ,σ), matching Tier-1/Tier-2 source bars, and the same D5 worked-example citation. Its scope differs (a one-time bounded sweep against a frozen Q1–Q6 query-family list, vs. this ADR's standing forever-doctrine) and it is a genuinely useful concrete asset this ADR lacks (an actual enumerated search plan). But its four-field template, as merged, carried **no test for requirement 1** (mechanism-vs-evidence-robustness) — the exact gap this ADR's Path 1a/1b exists to close. Reconciled same day, pre-Phase-1 (no paper had been extracted): Q-KBUDGET-HARVEST-1's pre-reg §C.1 and parent §7 were amended to inherit this ADR's requirement 1 as a mandatory pre-check, citing this ADR as its front-door doctrine. Q-KBUDGET-HARVEST-1 is now read as this ADR's **first execution instance**, not a parallel or competing gate — its Q1–Q6 query families become the first funded sweep under the standing intake once its own Phase 1 runs.

---

## §2 — Decision

**Decision:** externally-published trading strategies/anomalies enter the discovery program **only** through the harvest intake: a seed is admitted to the ratified axis inventory iff it (a) files the declaration manifest, (b) passes the standing two-clause intake screen, and (c) receives operator ratification of its inventory row — after which it proceeds to campaign scoping under the existing HARV-lane / Campaign-defaults / DSR-K chain, unchanged.

The intake's four **admission requirements** (all mandatory before screening; requirement 1 has two alternative satisfaction paths):

1. **Requirement 1 — economic grounding, satisfied via either path:**
   - **Path 1a — named mechanism.** Who systematically loses money and why. Pattern-only publications are not seeds (mechanism-blind mining is the class DISC-CAMP-0 falsified and Clause K kills).
   - **Path 1b — evidence-robustness in lieu of a settled mechanism.** Admits anomalies with competing or no consensus mechanism (the momentum-class shape) if published evidence clears **all four** of: **(i)** documented across ≥3 decades of covered sample period; **(ii)** replicates across ≥3 independent, non-overlapping cohorts (distinct markets/instruments/eras — same no-transplant discipline as requirement 2: the δ used for *our* target instrument must come from that instrument's own cohort, not a borrowed one); **(iii)** at least one replication was published ≥10 years after the effect's original discovery (excludes a single long-window backtest constructed after the fact with hindsight — that is one look, not decades of evidence); **(iv)** no known regime/venue condition under which the sign structurally reverses (name any such condition rather than asserting immunity). Path 1b is a **higher** evidentiary bar than 1a in exchange for not requiring a settled mechanism story — it does not relax requirements 2–4, which apply identically regardless of path.
   - **Rationale for keeping either path mandatory rather than deferring to the gates (operator pushback, addressed):** the downstream gates (HARV reachability, universe gate, realism, survivor scoring) catch *false positives* — candidates that look real but aren't. Requirement 1 protects against a different failure the gates cannot catch after the fact: a mechanism-blind or evidence-thin seed that reaches campaign scoping consumes authoring/session cost and — because the campaign lane requires K_intrinsic ≤ 3 pre-committed hypotheses — needs *some* argument for why so few hypotheses were pre-committed. Path 1a/1b are that argument, checked before the cost is spent, not after.
2. **Cohort-cited per-instrument δ/σ** — a published (or in-house-measured) effect size on the target instrument's own cohort, plugged at the conservative central reading with a publication-decay haircut. **Cross-instrument transplant is inadmissible** (D5 gamma-sign precedent). No citable δ ⇒ UNSCREENABLE, routed (δ-extraction probe or drop), never patched with an invented number. **Rationale (operator pushback):** the HARV reachability HARD gate requires an effect-size prior to simulate a plausible-true world at all — deferring this to campaign scoping just moves the same literature work to after scoping effort is spent (the Q-HARV-1 shape: died at pre-registration, having already consumed the authoring session this requirement exists to save).
3. **Unburned family K-bank** — `K_banked(family)` from the closed-manifest ledger; any GC/MGC-class family bank that pushes floor(K_eff) above Cap kills the seed regardless of quality (D1/D4 precedent). **Rationale (operator pushback):** K-banking is permanent — abandoned and failed campaigns still bank K against their instrument family (Campaign-defaults ADR). The floor is pure arithmetic, computable before any spend; running a campaign to learn what the arithmetic already told you wastes the slot *and* banks additional K on an already-dead family. Of the four, this is the one no downstream gate can ever recover from — the universe gate would catch it too, but only after the pull.
4. **Confirm-power ≥ 0.50 at the declared panel N** — under the frozen Clause-N formula. Monthly-event mechanisms at bp-scale effects are dead on arrival (D3/D7 precedent, killed twice); daily-or-intraday event frequency is the practical bar. **Rationale (operator pushback) — the one requirement no downstream gate substitutes for:** the gates control false positives; nothing downstream protects against a test that is uninformative *by construction*. At power 0.30, a **true** mechanism fails its confirm 70% of the time — the campaign spends the pull, the sessions, and the K, gets a null either way, and the class enters the dead-list, making a real edge *harder* to re-propose later (Q-HARV-1 was DECLINED at §R for exactly this, power 5–6%).

**Screen constants are inherited by citation, never re-derived here:** Cap = 1.0, DSR ≥ 0.95, V = 1/n, K_eff ≤ 3, power ≥ 0.50, z = 1.96 — all from the frozen Q-KBUDGET screen pre-reg §B (freeze `b304f2c`) and its upstream anchors (Q-GATECART-1 Cap resolution; DSR-K ADR). Changing any constant requires superseding those artifacts by their own close-and-reopen rules, not editing this intake. Path 1b's (i)–(iv) are new criteria introduced by this ADR (not inherited from the frozen screen, which is silent on mechanism-vs-evidence sourcing) and may be tightened/loosened only by superseding this ADR.

**Campaign-lane note (reading, not a redefinition of an Accepted ADR):** both Path 1a and Path 1b seeds are *pre-committed-hypothesis* shaped (K_intrinsic ≤ 3 fixed expressions, not a search) and therefore both open via `register_search open --lane mechanism-first` — the HARV lane's K-accounting and reachability-gate protections apply to the campaign *shape* (pre-committed vs. mined), which is orthogonal to whether the pre-commitment argument is a named mechanism or a replication-robustness case. This ADR does not edit the HARV-lane ADR's text or scope; if this reading is ever contested, resolve via that ADR's own supersession discipline, not a silent reinterpretation here.

**Confirm-not-mine:** a seed declares K_intrinsic ≤ 3 fixed hypothesis expressions at admission. Any post-admission widening (parameter sweep around the seed, extra windows, extra variants) voids the screen result and constitutes a **new axis** requiring fresh declaration + re-screen — same enforcement point as pre-reg §C: a campaign `register_search open` binding K above the declared band voids the PASS.

**A screen PASS never blesses** — it licenses campaign scoping only; the HARV reachability HARD gate, cost gate, and all downstream gates still bind (verbatim inheritance of pre-reg §B's asymmetry).

**Effective:** upon acceptance.
**Scope:** all externally-sourced strategy/anomaly seeds targeting the discovery program from acceptance onward. Out of scope: Class-S existing-strategy books (own route — survivor-scoring gate + the 2026-07-14 candidate-class ADR); Gen-2 internally-mined candidates (Campaign-defaults chain directly); any re-opening of closed screen verdicts.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Status quo — one-shot screens per investigation** | Each new seed re-authors Q-KBUDGET-shaped machinery under time pressure; anchor drift toward the seed being argued for is exactly what the screen pre-reg §A froze against. Rework cost is real (the D7 δ-extraction + D5 rescreen each took a session). |
| **Screen only at campaign pre-reg (rely on the HARV HARD gate)** | The HARD gate catches unreachable *clauses* after scoping effort is already spent, and checks neither family K-banks nor sourcing quality. The intake kills dead seeds for ~zero cost (pure arithmetic, zero pulls, zero K) *before* scoping — the DROP-early asymmetry the screen was built for. |
| **Amend the HARV-lane ADR in place to add sourcing** | In-place edits of an Accepted ADR's §2 are forbidden by its own §5-class discipline; and the surfaces differ — HARV owns campaign shape (mechanism-first + reachability), this owns what may enter the inventory at all. Separate ADR, chained by reference. |
| **Build an automated harvester/scraper pipeline now** | Premature — sourcing is judgment-heavy literature work at current volume (one funded seed). The Algorithm orders Automate as the tail of Accelerate; codify the discipline first, automate if seed volume ever justifies it. |

---

## §4 — Falsifier (revert trigger)

**H:** externally-published mechanisms admitted through this intake (mechanism + cohort-cited δ with decay haircut + unburned family + power ≥ 0.50) reproduce on our panels at rates that justify the intake as the standing seed source — i.e. the transfer premise holds often enough to fund the discovery program.

**Revert trigger (binary):** among the first **two** intake-class seeds to reach campaign closure (D5 explicitly counts as intake-class — it is the worked instance this ADR generalizes), **both** close FALSIFIED on their primary confirm clause (mechanism not reproduced on our panel under a correctly-reachable gate — a gate-geometry failure per the HARV ADR §4 routes to *that* falsifier instead, not this one). Then the transfer premise is falsified and this ADR is superseded: harvest intake demotes to research-only; re-proposal requires a source-class post-mortem (which admission requirement failed to protect), not a third seed.

**Idle guard:** if by **2026-11-08** the intake has admitted zero screen-PASS seeds beyond D5, the intake is idle-not-working — fold its disposition into the 11-08 program review (it may survive as dormant doctrine, but it must be *named* idle, not presumed active).

**Verdict vocabulary:** **RESOLVED** if ≥1 of the first two intake-class campaign closures confirms its mechanism OOS; **FALSIFIED** per the revert trigger; **AMBIGUOUS** if no intake-class campaign closes by 2026-11-08 (then re-test at the following quarterly).

**Revert action:** superseding ADR citing the two dated closures; never a silent §2 edit.

**Trigger check schedule:** rides the standing quarterly programme audits — **2026-08-08** (progress read: D5 campaign state + any new admissions), **2026-11-08** (idle guard + any fired closures), then quarterly.

---

## Addendum 2026-08-15 — Second §4 limb (gate-stack audit R10)

**Status:** `Accepted` — operator GO (JA) 2026-08-15 after PR #15 merged. Limb 2 binds. Limb 4 of the ceremony-tiering ADR (creates/amends a falsifier) — full amend-in-place, not light. This addendum does **not** rewrite the §4 revert trigger (ADR §5: silent amendment of §4 is Trap #12; supersede or add, never silently edit). Limb 1 stands byte-unedited. Count on limb 1 stays **0-of-2**.

**§0 Rule 0 (verified 2026-08-15, ratification session):**

| Source | Anchor | Supplies |
|---|---|---|
| This addendum as drafted | `aa2e4be6` 2026-08-15 | Status was `Proposed`; pin named; fire-on-yes warned |
| This ADR §4 revert trigger | `aa2e4be6` | Limb 1 unedited; gate-geometry failures still route to HARV ADR §4 |
| [08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) R10 / §3.7 | `aa2e4be6` | Observed miss: D5 + H-OD-1 reclassified as gate-geometry; five-plus dead campaigns never reach limb-1 strike one |
| [D5 scoping](../briefs/rnd-pipeline/D5-NQ-intraday-momentum-scoping.md) | `027a7295` 2026-08-14 | `CLOSED — Stage-2 cost-law KILL 2026-07-16` |
| [H-OD-1 scoping](../briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md) | `027a7295` 2026-08-14 | `CLOSED — Stage-2 cost-law KILL 2026-07-16` (mechanism CONFIRMED-IS) |
| [H-TSMOM-1 scoping](../briefs/rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md) | `027a7295` 2026-08-14 | `CLOSED — Clause-N FAIL 2026-07-16` (P1=c, N≈86, power 0.34) |

**Amendment-first (sub-rules 8/10, this ratification):** `rg` on `lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/rejected_candidates.md` for `second §4 limb|fundability-transfer|R10` — empty. Owner is this file. `check_advisor_dedup.py --keywords "harvest intake limb 2 R10 fundability-transfer"` — no slug; keyword overlap only.

**Cheap falsifier (PARENT-side, before this stamp):**

```
rg -n "Status: \`Proposed\`" docs/adr/2026-07-15-external-mechanism-harvest-intake.md
# present on origin/main @ 52f39979 (PR #15 merge) — this stamp flips it
rg -n "CLOSED — Stage-2 cost-law KILL 2026-07-16" docs/briefs/rnd-pipeline/D5-NQ-intraday-momentum-scoping.md docs/briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md
rg -n "CLOSED — Clause-N FAIL 2026-07-16" docs/briefs/rnd-pipeline/H-TSMOM-1-ES-tsmom-scoping.md
```

**Decision (binding):** **limb 2 — fundability-transfer**. Among intake-class seeds that reach a dated kill at Stage-2 cost-law or Clause-N/power — including when the mechanism was confirmed in-sample, or was never reached because that upstream gate killed first — if **two** such kills accumulate, the *fundability-transfer* premise is FALSIFIED. Harvest intake then demotes to research-only / idle-named on the same 2026-11-08 vehicle. Limb 2 does **not** require a Stage-6 confirm closure. Scoping-stage Clause-N FAILs (H-TSMOM-1 class) **do** count. Remedy is the same as limb 1: superseding ADR + source-class post-mortem. Not a third sourcing channel. Not a Cap change.

**Pin (still open — this GO does not mark it):** do already-closed D5 / H-OD-1 / H-TSMOM-1 count? If yes, limb 2 fires on the mark. If no, only post-mark kills count. The three dated surfaces are verified above; they are **not** a fire. Do not read this GO as a silent yes or a silent no. Canonical count is unset until the pin is marked.

**Forbidden under this addendum:** rewrite limb 1; treat this GO as a limb-2 fire; treat an unanswered pin as a zero-count start; treat a limb-2 fire as licence to raise Cap or open a third channel.

**Falsifier of this addendum:** if the pin is still unmarked at the 2026-11-08 harvest §4 reading, that audit must mark it (yes → fire / no → count starts at 0). An unmarked pin at that reading is a decorative-threshold finding against this addendum. Do not silently drop.

---

## §5 — Forbidden moves (under this ADR)

- **Claiming Path 1b with fewer than 3 independent cohorts, fewer than 3 decades, or no post-hoc-replication check ((iii))** — the obvious gaming vector is asserting "well-replicated" without meeting the counted bar. All four Path-1b sub-criteria are mandatory; a seed meeting 3 of 4 is not admitted, it is UNSCREENABLE on requirement 1 pending the missing criterion.
- **Using Path 1b to route around requirement 2's no-transplant rule** — Path 1b's cohort-count (ii) is about the *mechanism/pattern's* documented breadth; the δ/σ plugged into Clause N must still come from the target instrument's own cohort. Citing "3 decades of SPX evidence" does not supply an NQ δ.
- **Cross-instrument δ transplant** to make a seed screenable (SPX→NQ was already declined once in D5's own rescreen — the temptation is real and recurring). No per-instrument cohort ⇒ UNSCREENABLE, full stop.
- **Patching a missing δ with an invented or "reasonable" number** — the screen pre-reg §B already forbids this (metric-cohort provenance binding); restated here because intake is where the temptation now lives.
- **Post-admission K widening** ("just sweep a few parameters around the seed") — that converts a K≤3 confirmatory axis back into the mining class Clause K exists to kill. Widening = new axis, fresh declaration, re-screen.
- **Re-proposing a screened-dead class with a new citation but no new mechanism evidence** — month-end from a different paper is still the month-end class (killed at D3 *and* D7); a new source is not new evidence. Same bar as `docs/rejected_candidates.md`: new mechanism evidence, not new packaging.
- **Quoting intake admission or a screen PASS as promotion evidence** — PASS licenses scoping only; the asymmetry is load-bearing and inherited verbatim.
- **Tuning screen constants (Cap, DSR_MIN, power threshold, z) inside the reusable module** to admit a marginal seed — constants inherit from the frozen pre-regs; the Q-GATECART-1 Cap workflow already rejected exactly this loosening as circular. Supersede upstream or live with the floor.
- **Silent amendment of §4** to match an emerging miss — Known Trap #12; supersede instead.

---

## §6 — Consequences

**Gate reminder (ties to §4):** doctrine check uses **RESOLVED / FALSIFIED / AMBIGUOUS** as named in §4 — a doctrine-level gate, not a live trading gate.

**Positive:**
- Public-strategy seeding becomes a dated, repeatable route with the kill-cheap property (pure arithmetic before any spend), replacing per-seed ad-hoc derivation.
- The four admission requirements convert "which paper should we port?" into a checklist any session can run — and most seeds correctly die at requirement 2 or 4 for the cost of a literature read.
- Sourcing connects mechanically to the existing chain: manifest → screen → inventory ratification → HARV lane → defaults/DSR-K → survivor scoring. No new gate authority is created.

**Negative (real cost):**
- Admission overhead per seed (manifest + citation work) even for seeds that die — accepted; that is the cheap-death working as intended.
- Requirement 2 (cohort-cited δ) structurally excludes most practitioner-code sources (TradingView scripts, GitHub strategies) until someone pays for a δ-extraction probe — a real narrowing of the sourcing funnel, accepted deliberately (unquantifiable publication bias is the alternative).

**Risks:**
- Published-effect decay makes even honest δ citations optimistic — mitigated by the mandatory conservative-central + decay-haircut reading (D5 precedent: 0.113 over 0.194) and by the §4 falsifier actually being reachable (D5 counts).
- Intake ossifies into ceremony if no seeds flow — mitigated by the §4 idle guard.

**Downstream artifacts (on acceptance):**
- [`docs/methodology/strategy_harvest.md`](../methodology/strategy_harvest.md) — becomes canonical procedure owner (lands with this ADR as companion; carries the sourcing tiers, manifest template, and worked example).
- `lab/research_utils/axis_screen.py` — promote `floor_scan.py`'s arithmetic to a manifest-consuming reusable module; Cursor handoff drafted at [`docs/briefs/handoffs/2026-07-15-cursor-handoff-axis-screen-module.md`](../briefs/handoffs/2026-07-15-cursor-handoff-axis-screen-module.md) (HELD until acceptance).
- `.claude/skills/futures-anomaly-discovery/SKILL.md` — add the Harvest-intake section + trigger phrases ("harvest", "public strategy", "port a published strategy", "seed discovery"); text specified in §7 Phase 2.
- `STATE.md` forward board — intake registered; §4 checks ride 08-08 / 11-08.
- `CLAUDE.md` Methodology references — one pointer line to the methodology doc.

---

## §7 — Implementation plan

- **Phase 0** — DONE (Rule-0 reads above, this session).
- **Phase 1** — DONE: ADR drafted + companion methodology doc + Cursor handoff draft (HELD).
- **Phase 1.5** — DONE, same session: operator pushback on requirement bar + mechanism-light evidence-robustness class incorporated (§1/§2/§5 amended pre-acceptance — this is authoring, not a post-acceptance edit).
- **Phase 2** — DONE, same session (acceptance sweep): `docs/methodology/strategy_harvest.md` updated (relief-valve note + Path 1a/1b + manifest field); Cursor handoff released (HELD → RELEASED) at [`2026-07-15-cursor-handoff-axis-screen-module.md`](../briefs/handoffs/2026-07-15-cursor-handoff-axis-screen-module.md); skill amendment landed in `.claude/skills/futures-anomaly-discovery/SKILL.md` (Harvest-intake section + trigger phrases + hand-off line); `STATE.md` forward-board entry added (2026-07-15 section); `CLAUDE.md` Methodology-references pointer line added.
- **Phase 3** — DONE: verification block passes (below); status flips `Accepted`; no `core/` / locked-parameter / MC-anchor touch at any phase (confirmed by §10 hook).

---

## §10 — Audit hooks (runnable)

```bash
# Status + one-decision scope
grep -n "Status:" docs/adr/2026-07-15-external-mechanism-harvest-intake.md

# Screen constants inherited, not restated as new authority (expect: citations to b304f2c / pre-reg §B, no novel values)
grep -n "b304f2c\|inherited by citation" docs/adr/2026-07-15-external-mechanism-harvest-intake.md

# Chain intact: HARV ADR still Accepted and unedited by this ADR
grep -n "Status:" docs/adr/2026-07-13-harv-discovery-lane-ratification.md
# Expected: Accepted

# Companion procedure doc exists and points back
test -f docs/methodology/strategy_harvest.md && grep -n "2026-07-15-external-mechanism-harvest-intake" docs/methodology/strategy_harvest.md

# §4 evidence sources: D5 campaign state (first intake-class closure feeds the falsifier)
grep -n "Status:" docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md

# Idle guard data: intake-class admissions since acceptance (expect >=1 row beyond D5 by 2026-11-08, else name idle)
grep -rn "admission-date" docs/methodology/strategy_harvest.md docs/briefs/ 2>/dev/null | grep -v template || echo "no admissions yet"

# No locked constant / allocation / dd_protection / MC-anchor touch
git diff origin/main -- core/ | grep -E "DD_TRIGGER|BASE_RISK" || echo "core clean"

# §4 trigger reminders — quarterly: 2026-08-08 (progress), 2026-11-08 (idle guard + closure count)

# Q-KBUDGET-HARVEST-1 (PR #391, first execution instance) inherited requirement 1 pre-Phase-1
grep -n "Path 1a\|Path 1b" docs/briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md docs/briefs/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md
# Expected: both files reference the pre-check
ls lab/analysis/harvest/q_kbudget_harvest_1_2026-07/ 2>/dev/null && echo "Phase 1 has started — reconciliation amendment must predate this dir's first commit" || echo "Phase 1 not yet started (expected at ADR authoring time)"
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python "C:\Users\joshu\.claude\skills\brief-authoring\scripts\check_brief.py" docs/adr/2026-07-15-external-mechanism-harvest-intake.md --type adr
# Expected: all checks PASS

# §0 anchors reproduce
git log -1 --format='%h %cs' -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md   # 936a9e0 2026-07-15
git log -1 --format='%h %cs' -- docs/adr/2026-07-13-harv-discovery-lane-ratification.md              # fad8984 2026-07-14
git log -1 --format='%h %cs' -- lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md             # 4a2471e 2026-07-15

# Frozen-screen §B untouched by this ADR (Trap-12 guard)
git diff b304f2c -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | grep -A2 '## §B' && echo "CHANGED — investigate" || echo "stable"

# R10 limb 2 Accepted; pin unmarked; not fired
grep -n "Status: \`Accepted\` — operator GO" docs/adr/2026-07-15-external-mechanism-harvest-intake.md
grep -n "Canonical count is unset" docs/adr/2026-07-15-external-mechanism-harvest-intake.md
# Expected: both present. Limb 1 revert trigger above this addendum stays byte-unedited.
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-15 | Initial `Proposed` draft — generalizes the Q-KBUDGET two-clause screen + D5 worked instance into standing sourcing/admission doctrine; companion methodology doc + HELD Cursor handoff land same commit | Joshua (authority) + Claude Code (draft) |
| 2026-07-15 | Operator pushback incorporated pre-acceptance: per-requirement rationale added to §1/§2 (why the gates don't substitute for admission); requirement 1 split into Path 1a (mechanism) / Path 1b (evidence-robustness, 4 sub-criteria) to admit momentum-class anomalies with no consensus mechanism; §5 anti-gaming forbidden moves added for Path 1b; methodology doc relief-valve note + manifest field added; `Proposed` → `Accepted`; §7 Phase 2 downstream sweep executed (skill, STATE.md, CLAUDE.md, Cursor handoff released) | Joshua (ratify) + Claude Code (draft + sweep) |
| 2026-07-16 | Reconciled against PR #391 (merged by operator): Q-KBUDGET-1's `RESULTS.md`/`d5_clause_n_rescreen.md` doc-sync accepted as-is (anchor updated `4a2471e`→`5a8713f`, content unaffected); the independently-authored `Q-KBUDGET-HARVEST-1` bounded Pre-Q named as this ADR's first execution instance and amended pre-Phase-1 (its own freeze pre-reg, not this ADR) to inherit requirement 1's Path 1a/1b — see §1 reconciliation note, §10 audit hook | Claude Code (reconciliation, operator-directed) |
| 2026-07-16 | Sourcing-layer elaboration landed (upstream of this ADR's admission requirements, no scope change here): `docs/methodology/strategy_harvest.md` §2 rewritten from a screenability-only tier list into a class-priority + ranked channel portfolio (design: [`docs/superpowers/specs/2026-07-16-mechanism-sourcing-strategy-design.md`](../superpowers/specs/2026-07-16-mechanism-sourcing-strategy-design.md)), driven by the D5/H-OD-1 confirmed-but-cost-killed finding. Explicitly does not duplicate the pending [`2026-07-16-harv-attestation-same-units-supersession.md`](2026-07-16-harv-attestation-same-units-supersession.md) ADR's cost-law admission requirement — cites it as `Proposed` and treats the §2.2 inequality as non-binding sourcing guidance until that ADR is Accepted. No new ADR authored for this elaboration. | Claude Code (operator-directed brainstorm → design → landing) |
| 2026-08-15 | **Proposed** second §4 limb (gate-stack audit R10) — fundability-transfer trigger covering cost-law / Clause-N kills the existing limb routes away. Limb 1 unedited. Not ratified here. | Cursor (spec) — operator GO still owed |
| 2026-08-15 | **Accepted** — operator GO (JA) after PR #15 merged. Limb 2 binds. Pin (already-closed D5 / H-OD-1 / H-TSMOM-1) left unmarked; not fired. Limb 1 unedited. | Joshua (GO) + Cursor (stamp) |
