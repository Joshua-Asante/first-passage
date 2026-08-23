# Strategy harvest — sourcing + admission of externally-published mechanisms

**Owner ADR:** [`docs/adr/2026-07-15-external-mechanism-harvest-intake.md`](../adr/2026-07-15-external-mechanism-harvest-intake.md) (`Accepted` 2026-07-15 — this doc is canonical procedure). §4 limb 2 (R10) is `Accepted` 2026-08-15; pin marked `no`; post-mark count lives on that addendum, not this file.
**Superseded-in-part-by:** [`S5 ADR`](../adr/2026-08-07-loop-s5-bounded-promotion-lane.md) (`Accepted` 2026-08-07) — per-candidate operator GO before capital/account action is replaced by **budget approval** for in-ceiling sandbox admits only; Stage-0 / K / cost-law and ceiling-crossing GOs stand.
**Position in the chain:** this is the **front door**. Everything downstream already exists and is unchanged by this doc:

```
public source → seed manifest → intake screen → inventory ratification (operator)
    → campaign scoping (HARV lane ADR 2026-07-13: reachability HARD gate)
    → register_search open (K binds; mechanism-first + DSR-cap refuse) → cost-gated Databento pull
    → stage24_runner → temporal_consistency / realism (universe_gate SPA/PBO dormant — W4)
    → survivor-scoring (G0–G5+G8 live shape; G6/G7 only via close+reopen) vs prop envelope
```
Post-W4 shape: [`W4 ADR`](../adr/2026-08-07-w4-minimal-gate-set-dormancy.md).

**Why this lane exists (one paragraph):** wide mining is structurally unfundable (Q-GATECART-1 M-19: DSR floor 2.05 at banked K = 3,177 > best in-house edge 1.83). A published mechanism inverts the cost: the original author paid the mining cost on their data; we pay only the confirmation cost on ours, entering at K_intrinsic ≤ 3 → floor 0.65–0.98, which is beatable. The seed's job is to **replace** mining, not to aim it — the fundable verb is *confirm*. Worked proof: D5 (Baltussen et al. 2021 *JFE* intraday momentum) is the only axis ever to PASS the two-clause screen, and it is exactly a harvested public strategy ([`d5_clause_n_rescreen.md`](../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md), verdict RESOLVED 2026-07-15).

---

## 1. The five admission requirements (all mandatory before screening)

A seed that fails any requirement is not screened — it is either routed to a recovery path (see the relief-valve note below) or dropped with the failure named.

| # | Requirement | Kill precedent |
|---|---|---|
| 1 | **Economic grounding — Path 1a (named mechanism) or Path 1b (evidence-robustness).** **1a — FOUR CLAUSES, all required, all ex ante** (sharpened 2026-07-26, [`mechanism-counterparty-constraint-boundaries`](../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) §2-A `Accepted`; supersedes the prior "who systematically loses money and why" wording): **(i) WHO pays — a *constraint*, not a preference.** An identified counterparty class trading under mandate, benchmark, or mechanical rule (rebalance mandates, benchmark-execution windows, expiry mechanics, hedging requirements, index-tracking), which keeps paying because it is compensated elsewhere (tracking error avoided, mandate compliance). **Preference/behavioral stories ("retail chases", "stops get hunted") no longer satisfy 1a** — they route to 1b or die. **(ii) WHEN — schedule or trigger declared before any data is read** (this is what downstream placebo tests test). **(iii) WHY it survives — an explicit capacity/awkwardness argument** for why arbitrage capital has not consumed the rent (capacity below institutional minimum ticket, assembly-awkward data, mandate-inelastic demand). "Nobody has noticed" is inadmissible; this clause is where a seed states its *lesser-mined* claim on the (data × expressibility × capacity) axes. **(iv) HOW it dies — a constraint observable** (AUM, fix volume, imbalance size, OI) that the Default-#5 decay monitor watches alongside the edge CUSUM. **1b** (for anomalies with no consensus mechanism — e.g. momentum-class effects): admits if published evidence clears **all four** of (i) ≥3 decades covered sample period, (ii) ≥3 independent non-overlapping cohorts, (iii) ≥1 replication published ≥10yr after original discovery, (iv) no known sign-reversal condition. 1b is a *higher* evidentiary bar in exchange for not requiring a settled mechanism story; it does not relax requirements 2–5. A pattern with neither a mechanism nor 1b-grade replication evidence is not a seed. | DISC-CAMP-0 (mechanism-blind, FALSIFIED 0/6); Clause K kills the class wholesale |
| 2 | **Cohort-cited per-instrument δ/σ** — published or in-house effect size on the *target instrument's own cohort*. Conservative central reading + publication-decay haircut (see §4). **Cross-instrument transplant inadmissible** (this holds under both 1a and 1b — 1b's cohort *count* is about the pattern's documented breadth, not a substitute source for the target instrument's own δ). No citable δ ⇒ UNSCREENABLE → route to a δ-extraction probe or drop; never invent a number. | D5 gamma-*sign* construct held UNSCREENABLE (all peer-reviewed estimates SPX-only; SPX→NQ transplant refused); D4 (no citable δ, 4-bar partial) |
| 3 | **Family K-bank — MANDATORY DISCLOSURE, not a gate** (amended 2026-08-04, [ADR](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) `Accepted`). `K_banked(family)` is still read from the closed-manifest ledger (`discovery_manifests/`) at admission and **must be stated in every pre-registration and screen row** — but it does **not** enter `K_eff` and **cannot fail a seed**. A large bank is a signal for the *reviewer* to weigh, not an automatic kill. Current banks (**re-read the manifests; do not trust this line's snapshot**): GC/MGC 3,177 · ES 2 · **MNQ 2** (D5 1 + ST-EH-1 1 — 2026-08-04 ADR-era snapshot; **live MNQ disclosure:** [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) §K_BANKED) · **MYM 1** (ST-EH-1) · **6E 1** (fc_carry) · CL 1 · all others 0. **Read these as history, no longer as floors** — under the amended rule a `K_intrinsic=1` seed screens at floor **0.65** on *every* family, GC/MGC included. **Split warning:** `st_eh_supertrend_grid` banks `K=2` spanning TWO families — the split is 1 MNQ + 1 MYM (see its `executed_looks`); do not add 2 to either. It closed `operator-stopped` under [§2-C](../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) banking executed reads (declared 84 retained in `declared_K`) — **and note it carries no verdict at all**, which is exactly the kind of entry that was doing real damage as a gate and is harmless as a disclosure. | *(none — this requirement no longer kills; D1/D4's GC/MGC deaths are withdrawn as K-kills and stand or fall on their own mechanism records)* |
| 4 | **Confirm-power ≥ 0.50 at the declared panel N** — frozen formula `power = Φ(√N·|δ|/σ − 1.96)`. Practical bar: **daily-or-intraday event frequency**. Monthly-event mechanisms at bp-scale effects have been killed twice and are presumptively dead. | D3 (ES month-end, power 0.24–0.30); D7 (6J month-end, power 0.30) |
| 5 | **Cost-law reachability (added 2026-07-16, [`harv-attestation-same-units-supersession`](../adr/2026-07-16-harv-attestation-same-units-supersession.md) ADR `Accepted`).** Mandatory inequality: `cohort δ (bp/event) ≥ 4 × RT_frac(panel-era median price, frozen execution model, commissions included)`. `RT_frac` computed at the basis the campaign's Stage-2 gate actually scores on (IS panel — never present-day or convenience price levels), commissions shown explicitly, never waived as negligible. Fails ⇒ UNREACHABLE: redesign the gate/instrument or do not open the campaign — this is a Stage-0 arithmetic check, not a judgment call. | D5 (cohort ≈2.97bp vs 11.06bp hurdle, unreachable ~3.7×); H-OD-1 (cohort 1.5bp vs 5.05bp IS-panel hurdle) — both would have died here at admission, for the cost of one division, instead of after a full freeze→GO→register→pull→screen cycle |

**Confirm-not-mine:** the seed declares **K_intrinsic ≤ 3 fixed hypothesis expressions** at admission (both 1a and 1b seeds are pre-committed-hypothesis shaped and open via `register_search open --lane mechanism-first`, which since 2026-07-25 also requires `--profile-cell` + `--profile-consult` — see the profile-consult block below). Post-admission widening (parameter sweeps, extra windows, extra variants) voids the screen result and is a new axis — fresh manifest, fresh screen. Enforcement point (screen pre-reg §C): a campaign `register_search open` that binds K above the declared band voids the PASS.

**Relief valve — requirement 3 is a mandatory disclosure, not a gate.** The five requirements read as a bouncer; in practice most of them have a documented recovery route, and the family K-bank (requirement 3) cannot fail a seed:

- **Requirement 1** can be satisfied two ways (1a/1b above); a seed with no named mechanism is not automatically dead — check 1b before dropping it.
- **Requirement 2**'s "nearest analytic analogue" provision (screen pre-reg §B) let D7 screen at all despite having no non-circular JPY-native δ (it borrowed the HARV class-analogue reading instead of inventing a number); a rank-6 (§2.3) seed with no independent cohort can fund a **δ-extraction probe** to generate one (costs data spend + K, but is a real path, not a dead end).
- **Requirement 4**'s UNSCREENABLE routing is explicitly re-triable: D5 itself went from UNSCREENABLE (no citable δ on the pinned construct) to PASS purely because an operator ratification supplied the missing construct-pin decision — no re-derivation of the arithmetic. The standing **re-screen trigger** is "when the missing input is supplied, or the next quarterly review, whichever first."
- **Requirement 3** no longer kills at all — it **discloses** ([ADR 2026-08-04](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md), `Accepted`). `K_banked(family)` still only grows and is still re-read from the closed-manifest ledger at admission, but it no longer enters `K_eff` and cannot FAIL a seed. **What replaced the automatic kill is reviewer judgment**, which is why the disclosure is mandatory rather than optional: a heavily-mined family is now something a reader must *see and weigh*, not something the arithmetic silently forecloses. The prior wording — *"a family-bank kill does not soften with time or new evidence … the bar is a fact about the ledger, not a judgment call"* — is **withdrawn**; under the amended rule it is precisely a judgment call. Mechanism-level foreclosure is unaffected and still binding: it lives in [`rejected_candidates.md`](../rejected_candidates.md) and the per-entry re-proposal bars, which K was never the right instrument for.
- **Requirement 5** has a redesign route, not a re-screen one: the inequality failing at the panel basis means the *gate/instrument pairing as declared* is unreachable, not necessarily that no expression of the mechanism could clear it — redesigning the instrument (e.g. a bigger-δ cohort) or the gate is a legitimate next step, distinct from disputing the arithmetic.

**Profile consult (added 2026-07-25).** Before screening, declare the seed's
`(instrument, mechanism-class)` cell and record the consult:

```bash
python scripts/instrument_profiles.py cell <SYMBOL> <mechanism-id>
```

A nonzero exit means a prior binds the cell — a re-proposal bar, a parked concept
sharing the anti-SNAG budget, or a running forward test. The pre-registration must
name and address it; it is not a permanent bar. `structure` priors print on every
consult regardless of verdict: the nulls aim the next candidate, not merely block it.
Canonical: [`docs/adr/2026-07-25-instrument-profile-index.md`](../adr/2026-07-25-instrument-profile-index.md).

## 2. Sourcing — class-priority + ranked channel portfolio (added 2026-07-16)

**Why this section exists:** the five admission requirements (§1) and the two-clause screen (§3) govern what happens *once a seed exists*. Neither one aims the search. Two funded campaigns since this doc's authoring — D5 and H-OD-1 — both **confirmed their mechanism** (H-OD-1: +1.444bp vs SR917's +1.5bp, t≈5.0, 9/9 IS years positive) and both **died at Stage-2 cost-law** (D5: 11.06bp hurdle vs ≈2.97bp cohort-implied; H-OD-1: 5.05bp hurdle vs 1.5bp cohort) — see [`STATE.md`](../../STATE.md) harvest-intake entry and [`2026-07-16-harv-attestation-same-units-supersession.md`](../adr/2026-07-16-harv-attestation-same-units-supersession.md). The lesson: sourcing effort spent on high-frequency, small-per-event-δ mechanisms is structurally cost-walled regardless of mechanism truth. §2.1–§2.3 below aim sourcing at the surviving band; full design rationale in [`docs/superpowers/specs/2026-07-16-mechanism-sourcing-strategy-design.md`](../superpowers/specs/2026-07-16-mechanism-sourcing-strategy-design.md).

### 2.1 Mechanism-class priority

- **Tier A — fund-first.** Low-frequency, large-per-event-δ, futures-native: time-series momentum/trend, carry, term-structure/roll-yield, factor-momentum, positioning-extreme reversal. `H-TSMOM-1` (Moskowitz-Ooi-Pedersen TSMOM, ES family) is the sole current occupant and the reference case for what a fundable seed looks like post-cost.
- **Tier B — conditional.** Announcement/auction drift, seasonality, index-rebalance flow, month-end pension flow. Admits only if event rate clears requirement 4 (confirm-power ≥ 0.50) **and** per-event δ clears the cost inequality below — check both, assume neither.
- **Tier C — graveyard-watch.** Intraday microstructure, dealer-gamma footprint. **D5 and H-OD-1 both died here on parent contracts (MNQ/ES) — contract size is not a mitigating lever**, so there is no size-based carve-out for this tier. Single admission condition: the seed's cohort δ clears §2.2's inequality at the adjudication panel's own price/cost basis. Default posture: do not source here absent that clearance.

### 2.2 Cost-reachability at sourcing time

**Applies §1 Requirement 5, at sourcing time rather than admission time** — run the same inequality before staging a candidate row, so a seed that cannot clear it dies for the cost of one division instead of consuming a manifest cycle. No independent constant or formula lives here; Requirement 5 is the sole authority.

### 2.3 Ranked channel portfolio (replaces the old screenability-only tiers)

| Rank | Channel | Method | Note |
|---|---|---|---|
| 1 | Citation-graph traversal from confirmed Tier-A axes | Semantic Scholar Academic Graph API (free), forward-citations | **Scoped**: influential-citation filter + futures-cohort keyword requirement — an unscoped traversal from a canonical TSMOM-class paper runs into thousands of citations and is not by-hand tractable |
| 2 | Survey / replication meta-studies (McLean-Pontiff-class) | Manual read | Feeds Path-1b's four-part evidence-robustness test directly |
| 3 | Futures-native journals (*Journal of Futures Markets*, *Journal of Banking & Finance*, JFQA) | Targeted search | Under-mined relative to generalist JFE/JF venues to date |
| 4 | CFTC COT/TFF positioning data | Direct data read | Tier-A positioning-reversal mechanism source; flagged power-marginal at weekly event frequency — check requirement 4 before manifesting |
| 5 | Strategy encyclopedias (Quantpedia-class) | Index only | Never cited directly — points into rank-1/3 sources |
| 6 | Practitioner books / code / blogs (GitHub, QuantConnect, old-Quantopian archives, TradingView, Carver, Chan) | Idea generation only | No independent-cohort δ; requires a δ-extraction probe (costs data spend + K) before requirement 2 can pass. Unquantifiable publication bias. Only worth the probe if requirement 1 is independently strong |
| **1-tie** | **Structural flow census — direct enumeration of mandated/mechanical flows on venue-legal instruments** (added 2026-07-26, [ADR §2-B](../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md) `Accepted`) | Hand-built enumeration from market-structure facts (exchange mechanics, mandate documents, fund filings), recorded in a Notice log — first instance `N-2026-07-26-forced-flow-census.md` (pruned at the Great Prune; retrieve via `git show pre-prune-2026-08-08:docs/notes/notice/N-2026-07-26-forced-flow-census.md`; tag is private-archive-only on this public clone — [`docs/ltm/README.md`](../ltm/README.md)) | **Ranked with rank-1 because it sources the Requirement-1a clauses directly rather than inheriting them from a paper.** A census entry is an OBSERVATION, not a seed: it consumes **zero K** (no PnL/δ examined) and graduates only through the unchanged admission path. Each entry must carry the four 1a clauses + a venue check (`core/firm_rules.py`) + the family K-bank **disclosure** (ADR 2026-08-04 — disclosure, not a gate; there is no floor to compute) + a graveyard-adjacency attestation. Complements the literature ranks: they supply δ for known effects, the census supplies mechanisms the literature has no incentive to publish (sub-institutional capacity) |

### 2.4 Standing radar cadence — zero new code

Rides the existing quarterly review dates already on the forward board (2026-08-08, 2026-11-08) rather than adding a scheduler — consistent with this ADR's own §3 "automate last" ordering and current low seed volume. Each pass: (1) citation-graph traversal per rank-1, scoped, seeded from every Tier-A axis confirmed since the last pass; (2) class-directed query-family pass — **inherits the frozen Q1–Q6 families from Q-KBUDGET-HARVEST-1 by reference, never edits them**; a pass wanting new families opens its own pre-registration; (3) survey-paper harvest per rank-2; (4) stage candidate rows, apply §2.2's sniff test before opening any manifest. A thin on-demand Semantic Scholar script is the named automate-later step, gated on seed volume rising enough to justify it — not built now.

**Dedup first, before any manifest work:** check [`docs/rejected_candidates.md`](../rejected_candidates.md), the closed discovery manifests, and `docs/methodology/rejected_signals.md`. A screened-dead **class** stays dead under a new citation — month-end from a different paper is still month-end. Re-proposal bar: new *mechanism evidence*, not new packaging.

## 3. The intake screen (constants inherited, never re-derived)

Source of truth: [`Q-KBUDGET-1-screen-preregistration.md`](../briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md) §B (freeze `b304f2c`) — **for Clause N, the floor ladder, Cap, and DSR/V only.** ⚠ **The deference does NOT extend to the Clause-K *formula*:** that pre-registration is frozen at the summed form `K_intrinsic + K_banked(family)`, which [ADR 2026-08-04](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) (`Accepted`) amended. A frozen pre-registration records what was true at freeze and is **never** back-edited, so on this one point **this doc and the ADR govern, and the frozen §B is historical**. Everything else below still restates §B for convenience and defers to it on divergence:

- **Clause K:** **`K_eff = K_intrinsic`** — the seed's own **within-search** trial count. floor(K_eff) = min annualized Sharpe clearing DSR ≥ 0.95 at (K_eff, V = 1/n), most-permissive f ∈ {0.5, 1, 2, 4}/day, 6.5y (production `lab/research_utils/deflated_sharpe.py`). **PASS iff floor ≤ Cap 1.0 ⇔ K_eff ≤ 3.** Reference floors: K=1→0.65 · 2→0.85 · 3→0.98 · 4→1.06 (FAIL). **`K_banked(family)` is NOT summed in** — it is a mandatory *disclosure* (see Requirement 3), reported by the screen alongside `k_eff`, never added to it ([ADR 2026-08-04](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md), `Accepted`). **A grid still pays in full:** every axis a design varies — parameter sweeps, conditioning gates, exit alternatives, best-of-K — counts in its own `K_intrinsic`. The change is to *which* selection is priced, never to *whether* selection is priced.
- **Clause N:** `power = Φ(√N·|δ|/σ − 1.96) ≥ 0.50`, N = full declared OOS event count (generous by design), δ = cohort-cited conservative central effect.
- **Asymmetry (load-bearing):** a FAIL is strong (generous inputs couldn't rescue it); a **PASS never blesses** — it licenses campaign scoping only. All downstream gates (HARV reachability HARD gate, cost gate, universe gate, realism, survivor scoring) still bind.
- **Harness:** until `lab/research_utils/axis_screen.py` lands (Cursor handoff, HELD on ADR acceptance), extend the [`floor_scan.py`](../../lab/archive/q_kbudget_1_2026-07/floor_scan.py) pattern campaign-locally. After it lands, a new seed screens by adding a manifest row — never by writing new screen code.

**Report with every verdict:** the required-quality percentile context (floor vs S_B median 0.3–0.5 / top-decile 0.85), so a PASS reads as "requires a top-decile-or-better edge to demonstrate," not as cheap.

## 4. The decay haircut (requirement 2 mechanics)

Published effects decay post-publication (McLean & Pontiff-class evidence) and are selected upward by the publication process itself. Rules:

- Use the **conservative central** derivation, not the optimistic one. D5 precedent: t-scaled δ/σ = 0.113 chosen over the R²-derived 0.194.
- When multiple derivations exist, plug the lowest defensible one and record the break-even (D5: power holds to δ/σ ≈ 0.062 — that margin is part of the verdict's honesty).
- Record the **net-of-cost caveat** explicitly: published Sharpes are gross; net tradeability on the micro is *the campaign's* question, never the screen's answer (D5: only SPX-futures shown to survive tick costs in the cited literature).

## 5. Seed manifest (declaration template)

Copy this block into the seed's admission artifact (lives with the inventory addition; one manifest per seed). The fields are the Phase-1 inventory §C declaration 5-tuple plus provenance. Provenance is **§2.3 rank** (channel 1–6 / 1-tie), not §2.1's mechanism-class Tier A/B/C. Pre-rewrite fills that used `source + tier` against the old screenability list (Tier 1 = peer-reviewed/WP, Tier 2 = encyclopedias, Tier 3 = practitioner) stand; old Tier 3 ≡ rank 6.

```markdown
# Harvest-seed manifest — <short name>

- **admission-date:** YYYY-MM-DD
- **requirement-1 path:** 1a (named mechanism) | 1b (evidence-robustness)
- **mechanism (req 1a) — all four clauses, omit if 1b:**
  - **(i) WHO pays (constraint):** <counterparty class + the mandate/benchmark/mechanical rule
    obliging them; what they are compensated with. A preference is not a constraint.>
  - **(ii) WHEN (schedule/trigger):** <clock, calendar, or state condition — declared before data>
  - **(iii) WHY it survives (capacity/awkwardness):** <why arbitrage capital has not consumed it:
    capacity below institutional minimum size / assembly-awkward data / mandate-inelastic demand.
    "Nobody has noticed" is inadmissible.>
  - **(iv) HOW it dies (constraint observable):** <AUM / fix volume / imbalance size / OI that the
    Stage-6d decay monitor watches alongside the edge CUSUM>
- **evidence-robustness (req 1b, all four required):** <(i) decades covered; (ii) cohort count +
  names; (iii) replication citation + years-post-discovery; (iv) known sign-reversal conditions,
  or "none found" — omit if 1a>
- **source + tier (§2.3 rank):** <full citation; rank 1–6 or 1-tie; if rank 6, link the δ-extraction probe>
- **target instrument + family (req 3):** <e.g. MNQ / NQ-family>
- **K_banked(family) — DISCLOSURE, not a gate:** <value + manifest citation, re-read at admission. Mandatory even though it no longer fails a seed; omitting it is an implementation defect per [ADR 2026-08-04](../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) §4 trigger 2>
- **K_intrinsic (confirm-not-mine):** <=3; **enumerate every axis the design varied** — sweeps, conditioning gates, exit alternatives, discarded-before-freeze variants. This is now the ONLY brake on selection inflation, so understating it is the single largest exposure the amended rule creates>
- **K_eff + floor(K_eff):** <from the screen harness; `K_eff = K_intrinsic`>
- **δ/σ (req 2):** <value; cohort; derivation (conservative central); decay-haircut note;
  break-even δ/σ; net-of-cost caveat>
- **N + event frequency (req 4):** <declared OOS event count; events/yr>
- **power:** <Φ(√N·|δ|/σ − 1.96)>
- **dedup attestation:** <rejected_candidates.md + closed manifests + rejected_signals.md
  checked YYYY-MM-DD; nearest dead class and why this is not it>
- **screen verdict:** PASS / FAIL(K) / FAIL(N) / UNSCREENABLE(<missing input + route>)
- **operator ratification:** <date + G-anchor, or PENDING>
```

## 6. Procedure (end to end)

1. **Dedup** (§2) — kill or proceed.
2. **Manifest** (§5) — fill every field; an incomplete manifest is unscreenable by construction.
3. **Screen** (§3) — zero pulls, zero K. FAIL/UNSCREENABLE rows are recorded below-the-line in the inventory, never silently dropped (pre-reg §C).
4. **Operator ratification** of the inventory addition (the G2 pattern, anchor commit recorded in the manifest).
5. **Campaign scoping** under the HARV lane: Stage-0 pre-registration with per-clause reachability attestation (HARD gate), defaults + DSR-K inherited by reference. Model: [`D5-NQ-intraday-momentum-preregistration.md`](../briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md).
6. **`register_search open`** (binds the declared K; default lane `mechanism-first`; attestation + profile consult + `--admission-file` enforced by `lab/discovery/register_search.py`) — **SPEC S6 + TNEC-1:** EM0 / EM2–EM5 + optional N-EDGE + DSR-cap / confirm-power refuse at open with **no manifest write** when `floor_at_k(K) > Cap` (empty band; K≥4), power < 0.50, or a supplied N-EDGE limb fails; **EM1 / D1 / D2 are disclosure-only** (never refuse). Admit records the admission summary on the manifest → cost-gated pull (`db_fetch` estimate → pull; IS/OOS date-cap enforced) → `stage24_runner` → gates.
7. **Survivor** → prop survivor-scoring at the frozen $100K band (G0–G5+G8; G6/G7
   changes only via close+reopen of the frozen prereg — W4) → Class-S/production
   handoff. Discovery never blesses; the gate chain does. Universe SPA/PBO dormant.

## 7. Worked example — D5 (the reference traversal)

Baltussen, Da, Lammers & Martens 2021 (*JFE*, "Hedging demand and market intraday momentum") → construct pinned by operator to the intraday-momentum footprint (gamma-*sign* construct refused: no per-instrument cohort) → manifest-equivalent declaration in the Phase-1 inventory (MYM/MNQ, K_banked 0, K_intrinsic 1–3) → screen PASS (floor 0.65–0.98; power 0.947 at N = 1000, δ/σ = 0.113 conservative) → verdict RESOLVED (2026-07-15) → Stage-0 pre-reg FROZEN, §R GO signed, K_eff = 1, DJ30 leg dropped on liquidity grounds. Every future seed should look like this file trail: [`d5_clause_n_rescreen.md`](../../lab/archive/q_kbudget_1_2026-07/d5_clause_n_rescreen.md) → [`Q-KBUDGET closure`](../briefs/closures/Q-KBUDGET-1-axis-reachability-screen.md) → [`D5 scoping`](../briefs/rnd-pipeline/D5-NQ-intraday-momentum-scoping.md) → [`D5 Stage-0 pre-reg`](../briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md).

**In flight — Q-KBUDGET-HARVEST-1** (bounded Tier-1/Tier-2 literature sweep, `LOCKED` 2026-07-16, PR #391): a frozen, enumerated 6-query-family search plan (intraday-footprint / session-timing / order-flow / FX-microstructure / metals-mechanism / anomaly-survey classes) targeting the same D1–D7 inventory this doc's screen consumes. Authored independently of this doc and reconciled same day, pre-Phase-1, to inherit requirement 1 (Path 1a/1b) as a mandatory pre-check — see [`Q-KBUDGET-HARVEST-1-verdict-preregistration.md`](../briefs/pre-registration/Q-KBUDGET-HARVEST-1-verdict-preregistration.md) §C.1. Read as this intake's **first funded execution instance**, not a second gate: its Q1–Q6 families are a concrete search plan this doc deliberately left abstract (§2 names sourcing tiers, not specific queries).

## 8. Audit hooks

```bash
# Owner ADR status (this doc is canonical only when Accepted)
grep -n "Status:" docs/adr/2026-07-15-external-mechanism-harvest-intake.md

# Screen constants here match the frozen pre-reg §B (divergence ⇒ this doc is stale, pre-reg wins)
grep -n "Cap 1.0\|DSR ≥ 0.95\|power.*0.50" docs/methodology/strategy_harvest.md
git diff b304f2c -- docs/briefs/pre-registration/Q-KBUDGET-1-screen-preregistration.md | grep -A2 '## §B' && echo "CHANGED — reconcile" || echo "stable"

# Family K-banks quoted in §1 are snapshots — re-derive from manifests
python -c "import json,glob; [print(p, json.load(open(p)).get('status'), json.load(open(p)).get('K')) for p in glob.glob('discovery_manifests/*.json')]"

# Admissions ledger (idle-guard input for the ADR §4)
grep -rn "admission-date" docs/ --include=*.md | grep -v strategy_harvest.md || echo "no admissions yet"

# Amending ADR now Accepted — Requirement 5 is binding, not sourcing-time-only guidance
grep -n "Status:" docs/adr/2026-07-16-harv-attestation-same-units-supersession.md
# Expected: Accepted

# Requirement 5 present in §1's admission table, and §2.2 doesn't restate the formula
# (scoped to before "## 8. Audit hooks" so this hook's own quoted pattern below doesn't self-match — M-AHF)
awk '/^## 8\. Audit hooks/{exit} {print}' docs/methodology/strategy_harvest.md | grep -c "cohort δ (bp/event) ≥ 4"
# Expected: 1 (only in §1's Requirement 5 row — §2.2 must not restate the formula)

# Radar cadence riding the existing quarterly dates, not a new schedule
grep -n "2026-08-08\|2026-11-08" docs/methodology/strategy_harvest.md
```
