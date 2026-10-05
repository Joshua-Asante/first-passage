# Pre-registration (DRAFT) — dated re-MC for the four-firm §4 falsifier (hard date 2026-11-08)

**Status:** `DRAFT — NOT FROZEN.` Nothing here binds a run, verdict or record until this line reads `FROZEN <YYYY-MM-DD>`, §9 is signed and every OWED value and OPEN decision is ruled. No re-MC, replay, backtest or screen of any candidate named here may run before freeze (§R).
**Owner of the falsifier:** [four-firm ADR §4](../../adr/2026-07-12-prop-portfolio-four-friendly-firms.md#4--falsifier-revert-trigger); **§4 status** is delegated to the [withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) (four-firm ADR header line 11, change history line 387). **Gate of record (adopted, not re-decided):** [prereg v2](2026-08-26-prop-survivor-scoring-prereg-v2.md), FROZEN 2026-08-26.
**Ruled 2026-10-02:** O-1, O-3 and O-12 (operator ruling 2026-10-02 (~01:50Z, to deployment coordinator (3), option B(b), "all recommended"); §6). **Ruled 2026-10-03:** O-2, O-4, O-13. **Ruled 2026-10-05:** O-5 to O-11, O-14 to O-18, INSUFFICIENT and a Class-S number later corrected (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))). **Corrected 2026-10-05:** Class-S number **#3**, replacing the #2 ruling, which rested on a wrong fact (#2 is `class_s_candidate2_scoring_2026-07-15`, FALSIFIED all-four-fail; `lab/CATALOG.md:109`); operator 2026-10-05, directly to coordinator (4). **Ruled 2026-10-05 (later):** the O-8/I-17 mechanism (mode-switching, with a dated fallback) and the I-20 acceptance with an intraday clock (operator 2026-10-05, directly to coordinator (4), and to a coordinator (4) worker ("go on your O-8 mode-switching recommendation", ~18:48Z)). **Why now:** operator ruling 2026-09-23 (condition 4): "A T00 screen does not count as falsifier evidence"; the falsifier "needs its own dated re-MC before 2026-11-08 regardless of T00" ([T00 §7.8](../handoffs/2026-09-22-tradeify-t00-step1-producer-inventory.md#78-operator-rulings-on-the-return-2026-09-23); [STATE 2026-11-08](../../../STATE.md#2026-11-08)).
**Loop of record:** STRATEGIC. **Authored:** 2026-10-02, Claude Code worker (drafting only) for the deployment coordinator. The operator owns every OWED value, every OPEN decision, the signature and the freeze.

## §D — Disclosure: what the drafter saw

- Public records only, read for this draft: the owners in §0 and the published figures they carry (candidate #1's corrected-geometry table and 1.00× honest-clock guard run in the [withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md); the combined-book figures cited in prereg v2 §0; the ORB-MNQ four-firm payability result in [b3](../../pursuits/b3-orb-mnq-payability-line.md)). The T00 step-2 draft ([PR #581](https://github.com/Joshua-Asante/first-passage/pull/581), head `b07e4f6`) was read; it holds no results.
- The drafter's context held a one-line memory summary of the 2026-09-09 Tradeify feasibility screen ("fragile"); none of its figures were read.
- No Pine, port, effective-input file or private artifact was read. No MC, replay, screen or backtest was run.

The operator adds any further prior look before freeze (§7 item 6). The candidate-specific prior-look table is §1b.

## §R — Standing rule for this file

No candidate named or proposed here is run through any frozen tier, decision-bearing screen, tier replay or MC before this file is FROZEN (coordinator direction 2026-10-02, "nothing may be run before freeze"; [existing-strategy ADR §5](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md) "Running the frozen $100K×4 tiers before the candidate pre-registration is committed"; [candidate #1 §5](2026-07-15-existing-strategy-book-candidate-1-prereg.md) "an unsigned run voids this pre-registration"). Committing this DRAFT is not that commitment. Harness code needed by §8 step 2 is tested on synthetic inputs only. **Exempt and disclosed (§1b), ruling 2026-10-05:** the completed T00 step-1b P7 producer-verification replay (retained-input `replay_bracket`, [P7 closure](../handoffs/2026-09-24-tradeify-t00-p7-closure.md)) predates this file, scored no tier and was not decision-bearing.

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
| `lab/discovery/prop_survivor_scoring.py` | `DEFAULT_PREREG` → v2; `discharges_falsifier`; `score_candidate(intraday_low=…)` threads the paired channel into every G4 run with the non-vacuity guard and `gate_grade` label (O-4 Slice A, `4ce71de`; before 2026-10-05 this row said "no `intraday_low` argument"); `run_tier_remc` passes `NO_PROTECTION_TRIGGER` (:599), so I-17 needs a `dd_trigger`/`dd_scale` keyword |
| `core/mc/preflight.py` | `firm_kwargs` (incl. `inactivity_off`), `assert_engine_ready`, `summarize_outcomes` |
| [STATE](../../../STATE.md#2026-11-08) | 2026-11-08 row; PARK b1 / b3 / b6 expiries the same day |

---

## §1 — What is pre-registered

### §1a — Candidate(s)

| Item | Value | Status |
|---|---|---|
| Candidate set | One of, or a named combination of: **(A)** the accepted Tradeify book (four legs: Aegis 6J, Striker MYM, Vanguard MGC, ORB MNQ), declared expressions, at the identities T00 step 1 resolved P7 for ([P7 closure](../handoffs/2026-09-24-tradeify-t00-p7-closure.md)), with its own protection policy (`ops/c1_rail/book_policy.py::candidate_book_protection_policy`); **(B)** the same book with the route-native editions, after both successor preregs freeze and P7 exists for those identities; **(C)** Class-S candidate #1 (2-leg MYM+MNQ), re-scored at 1.00× on the intraday-honest clock under its frozen §2 construction. See O-2. | **RULED (A)** — O-2, operator 2026-10-03 |
| Class-S numbering and authorization | (A) is **Class-S candidate #3**; authorized by the O-2 ruling (existing-strategy ADR §4). Correction 2026-10-05: an earlier 2026-10-05 entry here read #2 on the false premise that no other number was in use; #2 is the 3-leg Aegis book `class_s_candidate2_scoring_2026-07-15`, FALSIFIED all-four-fail (`lab/CATALOG.md:109`) | **RULED** — operator 2026-10-05 (corrected) |
| Identity binding | Public digests/pins only; no Pine, port body or parameter value in this file (AGENTS.md "Public-clone posture") | **OWED (operator)** — fills from the chosen candidate's owner |
| Variant count | Exactly the candidate(s) above; no weights, sizes, stops or legs varied | Fixed by existing-strategy ADR §5 and v2 §5 |

### §1b — Prior looks per candidate option (pointers; the finalizer completes the chosen row)

| Option | Known public prior looks |
|---|---|
| (A)/(B) | T00 step 1 and the step-1b P7 re-run (producer verification, including the retained-input `replay_bracket` execution in the [P7 closure](../handoffs/2026-09-24-tradeify-t00-p7-closure.md); no screen output; exempt under §R); the 2026-09-09/10 feasibility screen and its [closure](../../notes/2026-09-10-tradeify-protection-selection.md#feasibility-screen-closure) (Tradeify only, EOD clock); per-leg looks such as ORB-MNQ-1 at all four firms ([b3 addendum 2026-08-24](../../pursuits/b3-orb-mnq-payability-line.md)) and the Aegis+ORB combined book (v2 §0); Class-S candidate #2, an Aegis-bearing 3-leg book seen on all four frozen tiers (FALSIFIED all-four-fail, `class_s_candidate2_scoring_2026-07-15`, `lab/CATALOG.md:109`) |
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
| I-6 | Depth, seeds, horizon | 10,000 sims × seeds 42 / 123 / 2026; horizon 1500 | v2 §2 G4; **RULED** — O-6 (adopted verbatim under design (i)) |
| I-7 | Consistency | Run-2 gates: Tradeify 40% / MFFU 50% / BluSky 34%; Bulenox single run | v2 §7(5) |
| I-8 | Inactivity | barrier OFF (`inactivity_off=True`) | v2 §2 G4; `load_bearing_numbers.md` §2 |
| I-9 | Eval geometry | corrected: no eval-phase drawdown lock | withdrawal ADR §2; `core/firm_rules.py` |
| I-10 | Part B funded ceiling | ≤ 1.0%, G7 diagnostic, never gates §4 | v2 §3 |
| I-11 | Hard date | results dated on or before **2026-11-08** | four-firm ADR §4 |
| I-12 | Breach clock | intraday-honest mandatory for every gating tier read; EOD-clock reads may be reported, never gate a clear | **Adopted** — O-3 (ruling 2026-10-02) |
| I-13 | MC design and producer | (i) v2 G4 daily-block bootstrap with paired `intraday_low` blocks, or (ii) per-path bar-level replay through candidate 3′, parameterized per tier | **RULED (i)** — O-4, operator 2026-10-03 |
| I-14 | Path construction | Monday-anchored 5-day week blocks from `paired_blocks_from_daily`; one index set per sim shared by the P&L and `intraday_low` channels (`run_seed`); seeds per I-6; pristine start (I-18) | **RULED** — O-6, operator 2026-10-05 |
| I-15 | Compute budget | cap: one executor session for candidate + calibration reference (Run-1, Run-2 and guard arms on all four tiers); the wall-clock figure comes from a synthetic same-shape timing (§8 step 2d) and is written here before freeze | **RULED** — O-6, operator 2026-10-05; figure **OWED (operator)** |
| I-16 | Run-1 (consistency-off) | mandatory diagnostic on every tier with eval consistency (v2 G4, §7(5)); gate on Run-2; Bulenox single run | **RULED** — O-7, operator 2026-10-05 |
| I-17 | Protection posture | **Book policy ON by mode-switching**, as part of candidate (A). Each day of each path carries paired normal-mode and protected-mode P&L/`intraday_low` channels, drawn with one index set. The day runs protected when the prior session's close is at or below −1% of the running EOD peak (`book_policy.is_protected`, rounded to 6 places, no latch), else normal. There is no continuous `dd_scale` (scale 1). Protected inputs per leg: Striker S-P; ORB O-P; Aegis by `book_policy`'s protected quantity per trade on A-0 (timing invariance, Track B read :100); Vanguard zero (no entries). **Parity test:** on synthetic paths, the code's day-mode sequence equals `book_policy`'s `settle`/`mode_for` sequence (the `dd_scale` parity test is retired). **Code:** a separate code PR (wrapper over, or keyword on, the kernel path loop; the default path stays byte-identical), with Codex review and synthetic tests only. **Pre-registered fallback, fixed before any run:** if that PR is not merged on `main` by 2026-10-25, the run uses protection OFF on normal-mode inputs as a disclosed departure. Exact check: mode-switching merged on `origin/main` by 2026-10-25T23:59 ET → ON; otherwise → OFF (disclosed). The check depends on no result, is read before the run and is recorded in RESULTS. The code PR may implement only this frozen I-17 text. The executor run starts only after the branch is fixed: the mode-switching merge observed on `main`, or the 2026-10-25T23:59 ET cutoff passed. RESULTS records the `main` SHA read and the merge SHA (or "none"). **Named approximations:** each export's internal state (e.g. Striker's day soft-stop and halt at its own size) is taken from a continuous single-mode TV run, not re-derived on the switched path; capacity and takeover remain outside the daily series (O-4 risk). Disclosed: the policy is the single unadmitted `Tradeify_Select_100K` instance (`book_policy.py:62-69`), applied unchanged on all four tiers as part of the candidate, not an admission of per-tier policies; this departs from v2 §7(6) "default OFF" as candidate definition, not a gate overlay. The calibration reference runs OFF | **RULED** — O-8 operator 2026-10-05; mechanism re-ruled 2026-10-05 (mode-switching + fallback) |
| I-18 | Initial state | pristine $100K on all four tiers (v2 common band); the Tradeify read is a fresh-eval read, not the incumbent account's odds | **RULED** — O-9, operator 2026-10-05 |
| I-19 | Costs | each tier's daily series netted at that tier's `core/firm_rules.py` `cost_per_side_usd` from gross P&L and per-day contract-sides; the MGC leg at the index-micro rate is a disclosed optimistic bias. Harness change: `score_candidate` takes one `candidate_daily_pnl` and reuses the same blocks for every tier (`prop_survivor_scoring.py:652-731`), so it needs a per-tier series argument with `intraday_low` netted to match | **RULED** — O-5, operator 2026-10-05 |
| I-20 | Calibration reference | candidate #1 §3's registered non-candidate (the 3-leg native full-Aegis ae744 book), same harness, **same intraday clock** (I-12), same session, run once. **Prior look, all four tiers** (EOD clock, 10k, Run-2, dated 2026-07-15, `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md:81-86`): Bulenox 21.52%, Tradeify 17.88%, MFFU 17.74%, BluSky 26.68%. Each is ≥ 3.5× the 5.0% ceiling and the intraday clock can only raise bust, so AMBIGUOUS is predicted not to fire: the operator accepts the v2 §7(9) check as near-formal, disclosed. The reference panel is not retained ([PR #698](https://github.com/Joshua-Asante/first-passage/pull/698) §7) and is reassembled before freeze (§8 step 2(e)); if its intraday channel cannot be built, the run reads INSUFFICIENT | v2 §7(9); **RULED** — O-10 operator 2026-10-05; "Accept, intraday" 2026-10-05 |
| I-21 | Regime rider | candidate #1 §6 text: regime gate (6mo block bootstrap + half-panel split per `docs/methodology/regime_robustness_gate.md`) on the candidate series before RESOLVED is trusted into G8; reported beside, never overturns, rides into G8 as a caveat | v2 §7(7); **RULED** — O-10, operator 2026-10-05 |
| I-22 | G1/G2 (E1 reduction, ≥4× cost hurdle) | mandatory, in order, as in candidate #1 §8 (v2 §2, §7(4)); G1 `NO` or a G2 kill on every tier means no tier clears (§4 early-fail); a G2 kill on one tier means that tier does not clear | v2; **RULED** — O-10, operator 2026-10-05 |
| I-23 | Results location | public `lab/analysis/<dated slug>/RESULTS.md` with per-tier aggregates only (bust, pass, median days, `breach_clock`, `gate_grade`, admissibility labels), header citing this file and v2 by path; inputs stay private in the primary checkout; verdict as a dated addendum at the withdrawal ADR plus STATE's 2026-11-08 row | **RULED** — O-11, operator 2026-10-05 |
| I-24 | MFFU flatten admissibility | the series is built under Tradeify's rules (16:45 ET flatten; its 80-micro cap is the lowest of the four). MFFU auto-liquidates at 16:10 ET (`core/firm_rules.py:365-367`): an MFFU clear counts toward I-4 only if no series position is open past 16:10 ET on any day, checked mechanically by the series builder at run time; otherwise MFFU reads "inadmissible — 16:10 unmodeled" (no clear) | **RULED** — O-5, operator 2026-10-05 |
| I-25 | Export timezone | **`America/New_York`, DST-aware**, converted with `zoneinfo`, never a fixed offset; passed as the series builder's `export_tz` ([PR #702](https://github.com/Joshua-Asante/first-passage/pull/702)). Evidence: the 2026-07-23 anchoring of the MYM/MNQ trade lists against UTC-stamped 15m bars: `America/New_York` 96.2% / 97.4%, fixed UTC-4 64.8% / 68.8% ([Q-COSTGEO-2](Q-COSTGEO-2-verdict-preregistration.md) :18, :89) | **RULED** — operator 2026-10-05, directly to coordinator (4): "America/New_York, with daylight saving" |

---

## §3 — Hypothesis (H-REMC)

**If** the frozen candidate(s), run under §2 on the four frozen $100K tiers with a dated run completing on or before 2026-11-08, clear Part A (I-1 and I-2, Run-2 where consistency exists, on the I-12 clock) on **≥ 2 distinct firms including ≥ 1 `trailing_locking`**, **then** the four-firm §4 falsifier is discharged on measured footing as of the run date and the candidate routes to v2 G8 (lifecycle CANDIDATE @ 1.00×); rail, account and deployment stay separately gated. **Otherwise** the verdict follows §4; no candidate is varied or re-run in place.

## §4 — Verdicts (assigned mechanically; numbers are v2's)

Precedence: AMBIGUOUS first, then INSUFFICIENT, then the candidate rows. A G1 `NO`, or a G2 kill on every tier, is FALSIFIED — early-fail. An MFFU tier inadmissible under I-24 does not clear.

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** | Discharge rule I-4 met | §4 falsifier discharged (measured); G8 intake; recorded at the withdrawal ADR (dated addendum), the §4 status owner |
| **ONE-TIER** | Exactly one firm clears | Not a discharge; §4 stays undischarged; the operator decides at 11-08 (O-12, ruling 2026-10-02) |
| **FALSIFIED — partial** | ≥ 2 firms clear but I-4 is unmet (no `trailing_locking`) | Not a discharge (I-4); candidate closes; the 11-08 program reading is not covered by the 2026-10-02 ruling (O-12 residual) |
| **FALSIFIED — early-fail** | No tier clears | Not a discharge; §4 stays undischarged (O-1); candidate closes; early-fail branch arms: any subsequent candidate requires fresh operator authorization (existing-strategy ADR §4; candidate #1 §6). Does not by itself demote the program (below) |
| **AMBIGUOUS** | Calibration reference (I-20) clears 5.0% on ≥ 2 tiers | **Overrides every other row.** Gate cannot discriminate: close v2 and re-derive in a fresh brief (v2 §6); the candidate result is quarantined (neither discharge nor early-fail) |
| **INSUFFICIENT** | Missing producer context, missing synchronized `intraday_low` for a gating tier (`gate_grade=False`), run incomplete at frozen depth, or any §2 item unset | Adopted (operator 2026-10-05). No verdict from this run; at 11-08 it reads FALSIFIED, undischarged at the deadline (O-13) |

**Program level (checked at 2026-11-08, separate from the per-run verdict above):** the revert trigger fires (demote to research-only) if no pre-registered candidate clears Part A on any tier by 2026-11-08 (four-firm ADR §4; v2 §6 FALSIFIED). No verdict by then reads as O-13 records; exactly one tier is O-12 (operator decides); ≥ 2 clears with no `trailing_locking` tier is the O-12 residual (not ruled).

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
| O-5 | **Firm-specific rules inside a replay** for the three non-Tradeify tiers: own-flat deadline (Tradeify's account rule is built in), contract caps, per-firm costs (I-19). | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): **no per-tier replay code**; each tier reads through its own `firm_kwargs` (v2 G4); per-tier cost netting (I-19); caps need nothing (Tradeify's 80 is lowest); MFFU 16:10 admissibility (I-24); no `core/firm_rules.py` change and no Slice B. | **RESOLVED (operator 2026-10-05)** |
| O-6 | **Depth, path construction and budget** (I-6, I-14, I-15) for the chosen design; bar-level replay cost at 10k × 3 × 4 tiers × horizon 1500 is unmeasured. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): v2 G4 verbatim (I-6, I-14); budget cap one executor session, figure from a synthetic timing before freeze (I-15). Bar-level replay cost applies only to design (ii), not chosen. | **RESOLVED (operator 2026-10-05)** |
| O-7 | **Run-1 diagnostic** (I-16) and, for design (ii), how R1/R2 `UNDETERMINED` paths count. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): Run-1 is a mandatory diagnostic (I-16). The `UNDETERMINED` path rule belongs to design (ii) and does not apply. | **RESOLVED (operator 2026-10-05)** |
| O-8 | **Protection posture** (I-17): book policy inside the replay with kernel overlay OFF for (A)/(B); OFF for (C) per its frozen §2. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): book policy ON inside the bootstrap via `dd_trigger`/`dd_scale` with a synthetic parity test; reference OFF (I-17). Harness change: §7 blocker 4. **Re-ruled 2026-10-05** (operator 2026-10-05, directly to coordinator (4), and to a coordinator (4) worker ("go on your O-8 mode-switching recommendation", ~18:48Z)): **mode-switching** (I-17); the `dd_scale` parity test is retired; fallback to protection OFF if the code PR is not merged by 2026-10-25. | **RESOLVED (operator 2026-10-05)** |
| O-9 | **Initial state** (I-18): pristine or used (campaign record §6 D23). | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): pristine (I-18). | **RESOLVED (operator 2026-10-05)** |
| O-10 | **Riders** (I-20 to I-22): the non-candidate calibration reference at 5.0% (identity and harness); how the regime rider applies; whether G1/G2 apply to a Class-S book. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): candidate #1 §3's reference (I-20); candidate #1 §6 regime-rider text (I-21); G1/G2 mandatory (I-22). | **RESOLVED (operator 2026-10-05)** |
| O-11 | **Results location and public verdict record** (I-23). *Depends on O-1 (resolved): the §4 verdict record sits at the withdrawal ADR, not the four-firm ADR.* | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): public RESULTS with aggregates only; verdict at the withdrawal ADR (I-23). | **RESOLVED (operator 2026-10-05)** |
| O-12 | **Exactly-one-tier reading** (four-firm ADR Addendum 2026-08-22, `PARTIAL`). | Ruled 2026-10-02 (O-1 ruling): a clear on exactly one tier is not a discharge; the operator decides at 11-08 (§4 ONE-TIER). Residual, not ruled: the 11-08 reading of ≥ 2 clears without a `trailing_locking` tier. | **RESOLVED (operator 2026-10-02)** |
| O-13 | **No verdict by 11-08** (INSUFFICIENT, or run not started). *Depends on O-1 (resolved): §4 is undischarged absent a clear; whether that fires demotion stays open.* The revert trigger reads "no … candidate clears … in a dated lab re-MC". | Ruled (operator ruling 2026-10-03T22:14:55Z, to deployment coordinator (4), "go on your 616 recommendations"): **FALSIFIED.** No verdict by 2026-11-08 (INSUFFICIENT, or run not started) fires the revert trigger as written: demote to research-only. Recorded as "undischarged at the deadline", not as evidence the book fails; new pass-rate evidence may reinstate per the four-firm ADR §4. Track B qualification keeps its own gates (O-15, O-17 stay open). | **RESOLVED (operator 2026-10-03)** |
| O-14 | **"No second pre-registration for the same falsifier"** (D-T00 wording). | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): confirmed: this file is a candidate-and-run-contract pre-registration under v2, not a second gate pre-registration; a v2 number change closes v2 (Trap #12). | **RESOLVED (operator 2026-10-05)** |
| O-15 | **Proposed rule: a deployment session after 2026-11-08 needs a pass.** From the acceleration plan relayed by the coordinator (2026-10-02); not adopted here. If adopted, it belongs at the deployment-checklist owner. Related: four-firm ADR §4 says that after demotion "no execution-rail ADR may cite this ADR as live mandate without new pass-rate evidence"; whether Track B's deployment authority rests on that mandate is not established here. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): not a freeze input; routed to the deployment-checklist owner as its own decision, recommended there as not adopted (the four-firm ADR §4 revert trigger already bars citing that ADR as live mandate after demotion). | **RESOLVED (operator 2026-10-05)** |
| O-16 | **Dates**: freeze-by and run-by dates inside 2026-11-08. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): freeze by Fri 2026-10-23; run by Fri 2026-10-30; verdict recorded by Fri 2026-11-06. Missing freeze-by follows O-13. | **RESOLVED (operator 2026-10-05)** |
| O-17 | **H's "before any live account spend"** (four-firm ADR §4): the incumbent eval exists (AGENTS.md). | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): historical sequencing; the dated reading is owed at the four-firm ADR (coordinator ledger batch), not here. Live spend stays gated by M1 `RESOLVED` plus per-session GO (AGENTS.md). | **RESOLVED (operator 2026-10-05)** |
| O-18 | **Same-day PARK expiries** b1 (Aegis→6J), b3 (ORB-MNQ), b6 (Q-NAS-ECR) convert to SUBTRACT on 2026-11-08 absent renewal ([pursuits](../../pursuits/)). This re-MC neither renews nor expires them. | Ruled (operator 2026-10-05 (~18:25Z, directly to a coordinator (4) worker, "go on your 616 recommendations"; recommendations: [PR #696 sheet](https://github.com/Joshua-Asante/first-passage/pull/696))): not a freeze input; ruled in the 2026-11-08 sitting STATE already schedules. | **RESOLVED (operator 2026-10-05)** |

---

## §7 — Freeze blockers (the file cannot freeze while any holds)

1. Any OWED value in §1–§2 or OPEN item in §6 unruled (the §10 marker grep). O-1 and O-12 were ruled 2026-10-02; O-2, O-4 and O-13 on 2026-10-03; the rest on 2026-10-05. Still OWED: §1a identity binding; I-15's timing figure.
2. Candidate identities not bound by public digests (§1a).
3. Availability check (§8 step 2a) not passed: a TV-export trade list with a per-trade adverse-excursion column for each of the four legs at the P7 identities (returned DONE_WITH_CONCERNS, [PR #698](https://github.com/Joshua-Asante/first-passage/pull/698); the I-20 reference panel is carried by 4a).
4. Harness work required by O-3 and O-5 (series builder incl. protected-mode channels, per-tier series and cost netting, I-24 flag) not merged, or tested on anything other than synthetic inputs. The O-8 mode-switching code is the one exception: the file may freeze before it merges, because I-17's dated fallback (2026-10-25) decides the branch mechanically before the run.
4a. Reference panel (I-20) not reassembled with its intraday channel. A reassembly failure by 2026-10-16 goes to the operator before freeze; the file does not freeze into a run already bound to INSUFFICIENT.
5. Calibration reference (I-20) not named with its identity and harness.
6. §D or §1b incomplete: the operator has not added any further prior look.
7. §9 unsigned.

## §8 — Procedure

1. The operator rules §6 in words (no parameter values) and fills §1–§2 OWED cells.
2. Each build is its own authorized packet, built and tested on synthetic inputs only, and merged with a launcher record: (a) availability check first (existence and columns only; no metric computed); (b) series builder: public `lab/` code tested on synthetic inputs and merged, which reads the private exports only at run time and writes its outputs to a gitignored private root (never merged): daily gross P&L, per-day contract-sides, `intraday_low` (≤ 0), the I-24 flag and the no-protection check; (c) per-tier series and cost netting; (c′) the O-8 mode-switching code PR with its day-mode parity test (merge by 2026-10-25, else the I-17 fallback); (d) synthetic timing for I-15; (e) reassemble the I-20 reference panel with its intraday channel.
3. Claude fills §1–§2 from the rulings and runs §10 except the Status and signature hooks; if text changes afterwards, rerun.
4. The operator signs §9 and says "freeze". The Status line becomes exactly ``**Status:** `FROZEN YYYY-MM-DD` ``. The freeze commit SHA is recorded outside this file (a commit cannot hold its own SHA): in the PR, the RESULTS header and the withdrawal-ADR addendum.
5. In the freeze commit, rerun the full §10. Any failure voids the freeze: Status reverts to `DRAFT — NOT FROZEN.`
6. The FROZEN file is merged to `main` (existing-strategy ADR §5 "committed"). A separate executor packet then runs the frozen candidate(s) and the calibration reference in one session, under Rule 2 budget, and records the run date. Results cite this file and v2 by path.
7. The verdict is assigned mechanically under §4 and recorded at the [withdrawal ADR](../../adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md) (dated addendum; the §4 status owner per four-firm ADR lines 11 and 387) and STATE's 2026-11-08 row; SESSIONS cites v2 (v2 hook 6). All of this by 2026-11-08.

## §9 — Operator signature (blank until ruled)

- **Candidate set and Class-S authorization:** —
- **Rulings on O-1 to O-18:** —
- **Freeze-by / run-by dates:** —

---

## §10 — Audit hooks

```bash
f=docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md
# Gate numbers are v2's and the loader resolves v2 (expect 0.05 0.01 0.5).
python -I scripts/fp.py python -c "import sys; sys.path[:0]=['lab','core']; from discovery.prop_survivor_scoring import load_scoring_thresholds as l; t=l(); print(t.eval_bust_ceiling, t.funded_bust_ceiling, t.pass_floor)"
grep -n "2026-08-26-prop-survivor-scoring-prereg-v2" lab/discovery/prop_survivor_scoring.py
# Each frozen tier appears here (fails on the first missing one).
for t in Bulenox_100K Tradeify_Select_100K MFFU_Rapid_100K BluSky_Premium_100K; do grep -q "$t" "$f" || { echo "missing $t"; false; }; done
# Discharge rule unchanged in code.
grep -n "≥2 distinct firms clear Part A, of which ≥1 is trailing_locking" lab/discovery/prop_survivor_scoring.py
# The ruled intraday wrapper and its non-vacuous channel pass on synthetic inputs.
python -I scripts/fp.py python -m pytest -q tests/test_prop_survivor_intraday_channel.py tests/test_prop_survivor_scoring.py
# No unresolved value or decision at freeze (absence exits 0).
! grep -nE '\*\*OW[E]D \(operator\)\*\*|\*\*OP[E]N \(operator\)\*\*' "$f"
# §9 filled at freeze (absence exits 0).
! grep -nE '^- \*\*[^*]+:\*\* —$' "$f"
# Frozen form at freeze: expect exactly one line.
grep -nE '^\*\*Status:\*\* `FROZEN [0-9]{4}-[0-9]{2}-[0-9]{2}`' "$f"
# No result cites this file before freeze: expect no output until the run.
grep -rl "2026-10-02-four-firm-dated-remc-prereg" lab/ || true
# No accepted runtime port named in the book manifest is tracked (absence exits 0).
test -z "$(grep -oE '[^ ]+\.py$' core/strategies/BOOK_SOURCES.sha256 | xargs git ls-files --)"
```
