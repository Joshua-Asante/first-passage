# Pre-registration (DRAFT) — dated re-MC for the four-firm §4 falsifier (hard date 2026-11-08)

**Status:** `DRAFT — NOT FROZEN.` Nothing here binds a run, verdict or record until this line reads `FROZEN <YYYY-MM-DD>`, §9 is signed and every OWED value and OPEN decision is ruled. No re-MC, replay, backtest or screen of any candidate named here may run before freeze (§R).
**Owner of the falsifier:** [four-firm ADR §4](../../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#4--falsifier-revert-trigger); **§4 status** is delegated to the [withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) (four-firm ADR header line 11, change history line 387). **Gate of record (adopted, not re-decided):** [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md), FROZEN 2026-08-26.
**Ruled 2026-10-02:** O-1, O-3 and O-12 (operator ruling 2026-10-02 (~01:50Z, to deployment coordinator (3), option B(b), "all recommended"); §6). **Why now:** operator ruling 2026-09-23 (condition 4): "A T00 screen does not count as falsifier evidence"; the falsifier "needs its own dated re-MC before 2026-11-08 regardless of T00" ([T00 §7.8](../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23); [STATE 2026-11-08](../../../STATE.md#2026-11-08)).
**Loop of record:** STRATEGIC. **Authored:** 2026-10-02, Claude Code worker (drafting only) for the deployment coordinator. The operator owns every OWED value, every OPEN decision, the signature and the freeze.

## §D — Disclosure: what the drafter saw

- Public records only, read for this draft: the owners in §0 and the published figures they carry (candidate #1's corrected-geometry table and 1.00× honest-clock guard run in the [withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md); the combined-book figures cited in prereg v2 §0; the ORB-MNQ four-firm payability result in [b3](../../pursuits/b3-orb-mnq-payability-line.md)). The T00 step-2 draft ([PR #581](https://github.com/Joshua-Asante/first-passage/pull/581), head `b07e4f6`) was read; it holds no results.
- The drafter's context held a one-line memory summary of the 2026-09-09 Tradeify feasibility screen ("fragile"); none of its figures were read.
- No Pine, port, effective-input file or private artifact was read. No MC, replay, screen or backtest was run.

The operator adds any further prior look before freeze (§7 item 6). The candidate-specific prior-look table is §1b.

## §R — Standing rule for this file

No candidate named or proposed here is run through any frozen tier, replay or MC before this file is FROZEN (coordinator direction 2026-10-02, "nothing may be run before freeze"; [existing-strategy ADR §5](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) "Running the frozen $100K×4 tiers before the candidate pre-registration is committed"; [candidate #1 §5](2026-07-15-existing-strategy-book-candidate-1-prereg.md) "an unsigned run voids this pre-registration"). Committing this DRAFT is not that commitment. Harness code needed by §8 step 2 is tested on synthetic inputs only.

---

## §0 — Owners read (anchors: `origin/main@10b3929`, 2026-10-02)

| Owner | What it fixes here |
|---|---|
| [Four-firm ADR](../../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) §4 + Addendum 2026-08-22 (`Proposed`) | H (≥2 of four tiers clear an operator-pre-registered ceiling); revert trigger ("by 2026-11-08, no pre-registered portfolio candidate clears … on any … tier in a dated lab re-MC → demote to research-only"); hard date; the exactly-one-tier gap (ruled 2026-10-02, O-12). It does **not** own §4 status: its header (line 11) and change history (line 387, 2026-07-24) delegate that to the withdrawal ADR |
| [F1 reversal](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md#addendum-2026-09-01--f1-reversed-a-tradeify-resting-discharge-now-counts-toward-4) (2026-09-01) | Four-firm set: Bulenox · Tradeify · MFFU · BluSky; a Tradeify-resting discharge counts |
| [Prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md) §2–§7 | Every threshold and engine parameter in §2 below; discharge rule; F2 labels; calibration-reference and regime riders |
| [Withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) + [Addendum 2026-09-03](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md#addendum-2026-09-03--candidate-1-re-admitted-at-the-50-ceiling-accepted) (`Accepted`) | **Owner of §4 status.** Corrected eval geometry (no eval-phase lock); candidate #1 re-admitted at 5.0% and the §4 discharge restored, EOD-clock only; "the gate-grade intraday-honest re-score remains unrun". That EOD-clock discharge is **withdrawn** by the 2026-10-02 ruling (O-1); its dated addendum is owed at this ADR (coordinator ledger batch), not here |
| [Existing-strategy ADR](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) §4–§5 | Class-S route; "dated, pre-registered G4 re-MC"; each candidate consumes an explicit operator decision; early-fail branch; prior-look disclosure; no tier run before the candidate pre-registration |
| [Candidate #1 prereg](2026-07-15-existing-strategy-book-candidate-1-prereg.md) §2–§9 | Precedent for a book-level candidate: fixed candidate table, calibration-reference registration, verdict table incl. partial and early-fail, G0–G8 mapping, signature block |
| [`load_bearing_numbers.md`](../../load_bearing_numbers.md) §1–§3 | EOD-clock bust figures are lower bounds; inactivity barrier OFF; 5.0% / 50% / ≥1 `trailing_locking` live, owned by v2; four-firm set |
| [D-T00 row](../../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md#d-t00--tick-step-1-now-the-one-decision-on-the-1108-clock) (ratified 2026-09-22) | "no second pre-registration for the same falsifier"; condition 4 ruled NO |
| T00 step-2 draft (PR #581, not ratified) §0, §2 A1–A5, §4 OD-2 | Candidate 3′ producer (`ops/c1_rail/qualification/`); its kernel call is fixed to `Tradeify_Select_100K`, consistency 0.40, its own `intraday_low` (`runner.py:20–44`); R1/R2 `UNDETERMINED` path verdicts; declared expressions vs route-native editions |
| [ORB/Striker](2026-10-02-tradeify-route-native-editions-successor-prereg.md) and [Vanguard](2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md) successor preregs (DRAFT) | Route-native editions are unfrozen; §R there bars any candidate-configurable replay of an edition before its freeze |
| `lab/discovery/prop_survivor_scoring.py` | `DEFAULT_PREREG` → v2; `discharges_falsifier`; `score_candidate` (no `intraday_low` argument); `run_tier_remc(intraday_blocks=…)` and `paired_blocks_from_daily` exist |
| `core/mc/preflight.py` | `firm_kwargs` (incl. `inactivity_off`), `assert_engine_ready`, `summarize_outcomes` |
| [STATE](../../../STATE.md#2026-11-08) | 2026-11-08 row; PARK b1 / b3 / b6 expiries the same day |

---

## §1 — What is pre-registered

### §1a — Candidate(s)

| Item | Value | Status |
|---|---|---|
| Candidate set | One of, or a named combination of: **(A)** the accepted Tradeify book (four legs: Aegis 6J, Striker MYM, Vanguard MGC, ORB MNQ), declared expressions, at the identities T00 step 1 resolved P7 for ([P7 closure](../handoffs/2026-09-24-tradeify-t00-p7-closure.md)), with its own protection policy (`ops/c1_rail/book_policy.py::candidate_book_protection_policy`); **(B)** the same book with the route-native editions, after both successor preregs freeze and P7 exists for those identities; **(C)** Class-S candidate #1 (2-leg MYM+MNQ), re-scored at 1.00× on the intraday-honest clock under its frozen §2 construction. See O-2. | **RULED (A)** — O-2, operator 2026-10-03 |
| Class-S numbering and authorization | (A)/(B) would be a new Class-S candidate; each consumes an explicit operator decision (existing-strategy ADR §4). (C) is a re-score of a frozen candidate under a different clock and the live ceiling. | **OWED (operator)** |
| Identity binding | Public digests/pins only; no Pine, port body or parameter value in this file (AGENTS.md "Public-clone posture") | **OWED (operator)** — fills from the chosen candidate's owner |
| Variant count | Exactly the candidate(s) above; no weights, sizes, stops or legs varied | Fixed by existing-strategy ADR §5 and v2 §5 |

### §1b — Prior looks per candidate option (pointers; the finalizer completes the chosen row)

| Option | Known public prior looks |
|---|---|
| (A)/(B) | T00 step 1 and the step-1b P7 re-run (producer verification; no screen output); the 2026-09-09/10 feasibility screen and its [closure](../../notes/2026-09-10-tradeify-protection-selection.md#feasibility-screen-closure) (Tradeify only, EOD clock); per-leg looks such as ORB-MNQ-1 at all four firms ([b3 addendum 2026-08-24](../../pursuits/b3-orb-mnq-payability-line.md)) and the Aegis+ORB combined book (v2 §0) |
| (C) | All four frozen $100K tiers seen on the EOD clock (withdrawal ADR §2); a 1.00× honest-clock guard run, not gate-grade (withdrawal ADR Addendum 2026-09-03); the 0.50× honest-clock arm ([`RESULTS_INTRADAY_W1`](../../../lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/RESULTS_INTRADAY_W1.md)) |

---

## §2 — Frozen inputs

| # | Input | Value | Owner / status |
|---|---|---|---|
| I-1 | Part A ceiling | headline bust **≤ 5.0%**, daily + static + trailing via `summarize_outcomes` | v2 §3 |
| I-2 | Pass floor | **P(pass) ≥ 50%**, finite median days-to-target **≤ 1500** | v2 §3, §7(1) |
| I-3 | Tiers | exactly `Bulenox_100K` · `Tradeify_Select_100K` · `MFFU_Rapid_100K` · `BluSky_Premium_100K`; all others diagnostics only | v2 §3 |
| I-4 | Discharge rule | ≥ 2 distinct firms clear Part A, ≥ 1 `trailing_locking` (Tradeify or MFFU); a Bulenox/BluSky-only pair does not count; F2 optimistic-lower-bound labels on Bulenox/BluSky | v2 §3; `discharges_falsifier` |
| I-5 | Engine | `firm_kwargs` threading, never module constants; `assert_engine_ready` GREEN per tier (G3); per-seed bucket-sum assertion | v2 §2 G3–G5, §7(2) |
| I-6 | Depth, seeds, horizon | 10,000 sims × seeds 42 / 123 / 2026; horizon 1500 | v2 §2 G4 (applicability to a path-replay design: O-6) |
| I-7 | Consistency | Run-2 gates: Tradeify 40% / MFFU 50% / BluSky 34%; Bulenox single run | v2 §7(5) |
| I-8 | Inactivity | barrier OFF (`inactivity_off=True`) | v2 §2 G4; `load_bearing_numbers.md` §2 |
| I-9 | Eval geometry | corrected: no eval-phase drawdown lock | withdrawal ADR §2; `core/firm_rules.py` |
| I-10 | Part B funded ceiling | ≤ 1.0%, G7 diagnostic, never gates §4 | v2 §3 |
| I-11 | Hard date | results dated on or before **2026-11-08** | four-firm ADR §4 |
| I-12 | Breach clock | intraday-honest mandatory for every gating tier read; EOD-clock reads may be reported, never gate a clear | **Adopted** — O-3 (ruling 2026-10-02) |
| I-13 | MC design and producer | (i) v2 G4 daily-block bootstrap with paired `intraday_low` blocks, or (ii) per-path bar-level replay through candidate 3′, parameterized per tier | **RULED (i)** — O-4, operator 2026-10-03; O-5 open |
| I-14 | Path construction | block family, block length, RNG namespaces from I-6 seeds, path start | **OWED (operator)** — O-6 |
| I-15 | Compute budget | per tier and per candidate | **OWED (operator)** — O-6 |
| I-16 | Run-1 (consistency-off) | owed as diagnostic, or waived | **OWED (operator)** — O-7 |
| I-17 | Protection posture | kernel overlay OFF (v2 §7(6)); for (A)/(B) the book's own policy runs inside the replay as part of the candidate | **OWED (operator)** — O-8 |
| I-18 | Initial state | proposed: pristine (v2's $100K common band) | **OWED (operator)** — O-9 |
| I-19 | Costs | per-tier `cost_per_side_usd` (v2 G2) vs a reviewed per-firm cost model in the replay | **OWED (operator)** — O-5 |
| I-20 | Calibration reference | one non-candidate, same harness and clock, run once in the same session; not yet run at 5.0% | v2 §7(9) (mechanism); identity **OWED (operator)** — O-10 |
| I-21 | Regime rider | half-sample read reported beside the verdict; does not overturn the mechanical read | v2 §7(7); application **OWED (operator)** — O-10 |
| I-22 | G1/G2 (E1 reduction, ≥4× cost hurdle) for a Class-S book | proposed: applied as in candidate #1 §8 | **OWED (operator)** — O-10 |
| I-23 | Results location | public RESULTS path citing this file and v2 by path, or private root with a public verdict record | **OWED (operator)** — O-11 |

---

## §3 — Hypothesis (H-REMC)

**If** the frozen candidate(s), run under §2 on the four frozen $100K tiers with a dated run completing on or before 2026-11-08, clear Part A (I-1 and I-2, Run-2 where consistency exists, on the I-12 clock) on **≥ 2 distinct firms including ≥ 1 `trailing_locking`**, **then** the four-firm §4 falsifier is discharged on measured footing as of the run date and the candidate routes to v2 G8 (lifecycle CANDIDATE @ 1.00×); rail, account and deployment stay separately gated. **Otherwise** the verdict follows §4; no candidate is varied or re-run in place.

## §4 — Verdicts (assigned mechanically; numbers are v2's)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** | Discharge rule I-4 met | §4 falsifier discharged (measured); G8 intake; recorded at the withdrawal ADR (dated addendum), the §4 status owner |
| **ONE-TIER** | Exactly one firm clears | Not a discharge; §4 stays undischarged; the operator decides at 11-08 (O-12, ruling 2026-10-02) |
| **FALSIFIED — partial** | ≥ 2 firms clear but I-4 is unmet (no `trailing_locking`) | Not a discharge (I-4); candidate closes; the 11-08 program reading is not covered by the 2026-10-02 ruling (O-12 residual) |
| **FALSIFIED** | No tier clears | Program demotes to research-only (four-firm ADR §4); §4 enters the run undischarged (O-1); early-fail branch arms for Class-S (existing-strategy ADR §4) |
| **AMBIGUOUS** | Calibration reference (I-20) clears 5.0% on ≥ 2 tiers | Gate cannot discriminate: close v2 and re-derive in a fresh brief (v2 §6); this result is quarantined |
| **INSUFFICIENT** *(proposed)* | Missing producer context, missing synchronized `intraday_low` for a gating tier, run incomplete at frozen depth, or any §2 item unset | No verdict from this run; how the falsifier reads at 11-08 is O-13 |

## §5 — Forbidden moves

- Running any candidate on any frozen tier, replay or MC before FROZEN (§R).
- Moving any v2 number, the tier set, the discharge rule or the hard date (v2 §5; Trap #12). A number change closes v2; it is not made here.
- Substituting tiers, candidates, weights, sizes or clocks after any output exists; adding a second candidate after seeing the first's result without a fresh operator decision (existing-strategy ADR §4).
- Citing an EOD-clock clear as survival (`load_bearing_numbers.md` §1), or reading `compute_default_config()['bust_rate']` for a prop tier (v2 §5).
- Treating a T00 screen or a Track B E1 result as this re-MC (condition 4; E1 validates the Tradeify portfolio, not the four frozen tiers).
- Running a route-native edition before its own pre-registration freezes (successor §R).
- Publishing Pine, port bodies, effective-input values, account identifiers or account figures.

---

## §6 — OPEN operator decisions (stated, not decided)

| ID | Decision | Readings (none adopted) | Status |
|---|---|---|---|
| O-1 | **Falsifier status of record.** The withdrawal ADR Addendum 2026-09-03 (`Accepted`) restored the §4 discharge on candidate #1's figures, EOD-clock only. | Ruled (operator ruling 2026-10-02 (~01:50Z, to deployment coordinator (3), option B(b), "all recommended")): "A clear that gates §4 must hold on the intraday-honest clock. The 2026-09-03 EOD-clock discharge is withdrawn, and §4 stays undischarged until a pre-registered re-MC clears it (≥2 of the four $100K tiers incl ≥1 trailing_locking) by 2026-11-08. A clear on exactly one tier is not a discharge; Joshua decides at 11-08." Recorded at the withdrawal ADR (dated addendum, coordinator ledger batch), not here. | **RESOLVED (operator 2026-10-02)** |
| O-2 | **Candidate set** (§1a): A, B, C, or a named combination; and Class-S authorization for each. | Ruled (operator ruling 2026-10-03T22:14:55Z, to deployment coordinator (4), "go on your 616 recommendations"): **(A) alone**, the accepted Tradeify book as a new Class-S candidate; K = 1 at the book layer. (B) cannot freeze with P7 before 11-08; (C) has the heaviest prior looks and is not the deployed book. (A)'s §1b prior looks are disclosed at freeze. | **RESOLVED (operator 2026-10-03)** |
| O-3 | **Breach clock** (I-12). v2 is silent; `load_bearing_numbers.md` §1 makes EOD bust a lower bound. | Ruled 2026-10-02 (O-1 ruling): intraday-honest clock mandatory on every gating tier read; I-12 adopted. EOD-clock reads may be reported, never gate a clear. | **RESOLVED (operator 2026-10-02)** |
| O-4 | **MC design and producer** (I-13). *Depends on O-3 (resolved): every gating tier needs a paired intraday-honest `intraday_low` path.* (i) `score_candidate` has no `intraday_low` argument, so it needs a wrapper or extension over `run_tier_remc(intraday_blocks=…)`; for (A)/(B), T00's P1 finding says daily-series transforms cannot reproduce integer sizing, ORB base/add, capacity or takeover. (ii) The candidate 3′ kernel call is fixed to `Tradeify_Select_100K` and consistency 0.40, and its step-3 path needs a contract class P7's source-only contract refuses (T00 draft §5 item 3). | Ruled (operator ruling 2026-10-03T22:14:55Z, to deployment coordinator (4), "go on your 616 recommendations"): **design (i)**, the v2 G4 daily-block bootstrap with paired `intraday_low` blocks, on lab series built from the TV-export trade lists at traded sizes; a thin `score_candidate` wrapper over `run_tier_remc(intraday_blocks=…)`, tested on synthetic inputs only. The T00 producer does not serve this re-MC. **Named risk (carried into §5 at freeze):** per T00's P1 finding, a daily series does not reproduce capacity or takeover (integer sizing and ORB base/add enter only as traded). First build step: confirm a synchronized `intraday_low` exists for every gating tier; where it does not, the run reads INSUFFICIENT. | **RESOLVED (operator 2026-10-03)** |
| O-5 | **Firm-specific rules inside a replay** for the three non-Tradeify tiers: own-flat deadline (Tradeify's account rule is built in), contract caps, per-firm costs (I-19). | Parameterize per tier from `core/firm_rules.py` (code change, separate authorization), or hold Tradeify's and label the other tiers accordingly. | **OPEN (operator)** |
| O-6 | **Depth, path construction and budget** (I-6, I-14, I-15) for the chosen design; bar-level replay cost at 10k × 3 × 4 tiers × horizon 1500 is unmeasured. | Same as T00 draft §3 items 1 and 4; Track B leaves block family/length to TB-F1. | **OPEN (operator)** |
| O-7 | **Run-1 diagnostic** (I-16) and, for design (ii), how R1/R2 `UNDETERMINED` paths count. | T00 draft A5's pessimistic/optimistic rule, or another rule stated before any run. | **OPEN (operator)** |
| O-8 | **Protection posture** (I-17): book policy inside the replay with kernel overlay OFF for (A)/(B); OFF for (C) per its frozen §2. | Ratify, or state another. | **OPEN (operator)** |
| O-9 | **Initial state** (I-18): pristine or used (campaign record §6 D23). | Pristine matches v2's common band. | **OPEN (operator)** |
| O-10 | **Riders** (I-20 to I-22): the non-candidate calibration reference at 5.0% (identity and harness); how the regime rider applies; whether G1/G2 apply to a Class-S book. | Candidate #1 §3/§6/§8 is the precedent; its reference was registered for 3.0%. | **OPEN (operator)** |
| O-11 | **Results location and public verdict record** (I-23). *Depends on O-1 (resolved): the §4 verdict record sits at the withdrawal ADR, not the four-firm ADR.* | Public `lab/analysis/` RESULTS (v2 hook 6 precedent) or private root with a public verdict at the four-firm ADR. | **OPEN (operator)** |
| O-12 | **Exactly-one-tier reading** (four-firm ADR Addendum 2026-08-22, `PARTIAL`). | Ruled 2026-10-02 (O-1 ruling): a clear on exactly one tier is not a discharge; the operator decides at 11-08 (§4 ONE-TIER). Residual, not ruled: the 11-08 reading of ≥ 2 clears without a `trailing_locking` tier. | **RESOLVED (operator 2026-10-02)** |
| O-13 | **No verdict by 11-08** (INSUFFICIENT, or run not started). *Depends on O-1 (resolved): §4 is undischarged absent a clear; whether that fires demotion stays open.* The revert trigger reads "no … candidate clears … in a dated lab re-MC". | Ruled (operator ruling 2026-10-03T22:14:55Z, to deployment coordinator (4), "go on your 616 recommendations"): **FALSIFIED.** No verdict by 2026-11-08 (INSUFFICIENT, or run not started) fires the revert trigger as written: demote to research-only. Recorded as "undischarged at the deadline", not as evidence the book fails; new pass-rate evidence may reinstate per the four-firm ADR §4. Track B qualification keeps its own gates (O-15, O-17 stay open). | **RESOLVED (operator 2026-10-03)** |
| O-14 | **"No second pre-registration for the same falsifier"** (D-T00 wording). | This file adopts v2 as the gate and adds only candidate and run contract; T00 step 2 is not a falsifier pre-registration (#580 correction). Confirm. | **OPEN (operator)** |
| O-15 | **Proposed rule: a deployment session after 2026-11-08 needs a pass.** From the acceleration plan relayed by the coordinator (2026-10-02); not adopted here. If adopted, it belongs at the deployment-checklist owner. Related: four-firm ADR §4 says that after demotion "no execution-rail ADR may cite this ADR as live mandate without new pass-rate evidence"; whether Track B's deployment authority rests on that mandate is not established here. | Adopt, reject, or amend. | **OPEN (operator)** |
| O-16 | **Dates**: freeze-by and run-by dates inside 2026-11-08. | Set in §9. | **OPEN (operator)** |
| O-17 | **H's "before any live account spend"** (four-firm ADR §4): the incumbent eval exists (AGENTS.md). | Still binding, or read as historical sequencing. | **OPEN (operator)** |
| O-18 | **Same-day PARK expiries** b1 (Aegis→6J), b3 (ORB-MNQ), b6 (Q-NAS-ECR) convert to SUBTRACT on 2026-11-08 absent renewal ([pursuits](../../pursuits/)). This re-MC neither renews nor expires them. | Schedule the renewal decisions in the same sitting, or separately. | **OPEN (operator)** |

---

## §7 — Freeze blockers (the file cannot freeze while any holds)

1. Any OWED value in §1–§2 or OPEN item in §6 unruled (the §10 marker grep). O-1 and O-12 were ruled 2026-10-02; O-2, O-4 and O-13 on 2026-10-03.
2. Candidate identities not bound by public digests (§1a).
3. If (B) is chosen: either successor pre-registration not FROZEN, or no accepted P7 for the edition identities.
4. Harness work required by O-3 to O-5 not merged, or tested on anything other than synthetic inputs.
5. Calibration reference (I-20) not named with its identity and harness.
6. §D or §1b incomplete: the operator has not added any further prior look.
7. §9 unsigned.

## §8 — Procedure

1. The operator rules §6 in words (no parameter values) and fills §1–§2 OWED cells.
2. Any harness change from O-3 to O-5 is dispatched as its own authorized packet, built and tested on synthetic inputs only, and merged.
3. Claude fills §1–§2 from the rulings and runs §10 except the Status and signature hooks; if text changes afterwards, rerun.
4. The operator signs §9 and says "freeze". The Status line becomes exactly ``**Status:** `FROZEN YYYY-MM-DD` ``, and the freeze commit SHA is recorded in §9.
5. In the freeze commit, rerun the full §10. Any failure voids the freeze: Status reverts to `DRAFT — NOT FROZEN.`
6. A separate executor packet runs the frozen candidate(s) and the calibration reference in one session, under Rule 2 budget, and records the run date. Results cite this file and v2 by path.
7. The verdict is assigned mechanically under §4 and recorded at the [withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) (dated addendum; the §4 status owner per four-firm ADR lines 11 and 387) and STATE's 2026-11-08 row; SESSIONS cites v2 (v2 hook 6). All of this by 2026-11-08.

## §9 — Operator signature (blank until ruled)

- **Candidate set and Class-S authorization:** —
- **Rulings on O-1 to O-18:** —
- **Freeze-by / run-by dates:** —
- **Freeze commit SHA:** —

---

## §10 — Audit hooks

```bash
f=docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md
# Gate numbers are v2's and the loader resolves v2 (expect 0.05 0.01 0.5).
python -I scripts/fp.py python -c "import sys; sys.path[:0]=['lab','core']; from discovery.prop_survivor_scoring import load_scoring_thresholds as l; t=l(); print(t.eval_bust_ceiling, t.funded_bust_ceiling, t.pass_floor)"
grep -n "2026-08-26-prop-survivor-scoring-prereg-v2" lab/discovery/prop_survivor_scoring.py
# The four frozen tiers appear here (expect all four).
grep -c "Bulenox_100K\|Tradeify_Select_100K\|MFFU_Rapid_100K\|BluSky_Premium_100K" "$f"
# Discharge rule unchanged in code.
grep -n "≥2 distinct firms clear Part A, of which ≥1 is trailing_locking" lab/discovery/prop_survivor_scoring.py
# Intraday threading available to the bootstrap design.
grep -n "intraday_blocks" lab/discovery/prop_survivor_scoring.py core/mc/simulation.py
# No unresolved value or decision at freeze: expect no output.
grep -nE '\*\*OW[E]D \(operator\)\*\*|\*\*OP[E]N \(operator\)\*\*' "$f"
# §9 filled at freeze: expect no output.
grep -nE '^- \*\*[^*]+:\*\* —$' "$f"
# Frozen form at freeze: expect exactly one line.
grep -nE '^\*\*Status:\*\* `FROZEN [0-9]{4}-[0-9]{2}-[0-9]{2}`' "$f"
# No result cites this file before freeze: expect no output until the run.
grep -rl "2026-10-02-four-firm-dated-remc-prereg" lab/ || true
# No runtime port bodies committed: expect no output.
git ls-files 'ops/c1_signal_daemon/ports/*.py'
```
