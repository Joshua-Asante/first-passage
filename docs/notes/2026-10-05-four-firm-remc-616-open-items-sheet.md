# Recommendation sheet: PR #616 open items O-5..O-11, O-14..O-18, and DRAFT → FROZEN

**Date:** 2026-10-05. **For:** deployment coordinator (4), owner of [PR #616](https://github.com/Joshua-Asante/first-passage/pull/616) (four-firm dated re-MC prereg, head `8f8d093`). **Author:** Claude Code worker, dispatched by Joshua directly.
**Status:** recommendations only. Nothing is ruled, frozen or run here. The operator rules each item; this sheet does not amend the prereg.
**Anchors:** `main@7082a08`; prereg at `8f8d093:docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md` (cited as "prereg").
**Fixed by earlier rulings (not reopened):** O-1, O-3, O-12 (2026-10-02); O-2 (A) alone, K = 1; O-4 design (i); O-13 no verdict by 11-08 = FALSIFIED (2026-10-03T22:14:55Z).

## Facts this sheet relies on

| # | Fact | Source |
|---|---|---|
| F-1 | `score_candidate` now accepts `intraday_low`, threads it into every G4 run, runs the non-vacuity guard and labels `gate_grade`. The prereg's "no `intraday_low` argument" (§0, O-4) is stale. | `4ce71de` (O-4 Slice A); `lab/discovery/prop_survivor_scoring.py:652-690` |
| F-2 | `run_tier_remc` passes `NO_PROTECTION_TRIGGER` to `run_seed`, so the bootstrap runs protection-off. | `prop_survivor_scoring.py:65`, `:595-605` |
| F-3 | The kernel already applies a day's scale when EOD drawdown from the running peak is at or below `-dd_trigger`. That is the same trailing geometry as the book policy (`reference_mode="trailing"`). The scale also applies to `intraday_low`. | `core/mc/simulation.py:409-410`; `ops/c1_rail/book_policy.py:78-92` |
| F-4 | v2 freezes G1/G2 (≥4× cost hurdle) as mandatory, the overlay posture as "default OFF for scoring", Run-1 + Run-2 where consistency exists, and a calibration reference re-run at 5.0%. | [v2](../briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md) §2 (:102-117), §7(4)-(6), (9) |
| F-5 | Flatten deadlines: Tradeify 16:45 ET; MFFU **16:10 ET** (auto-liquidation; post-16:10 orders can disqualify); BluSky ~16:45 ET; Bulenox force-flat EOD. Micro caps: Tradeify 80, MFFU 80, BluSky 100, Bulenox 120. Costs per side: 0.91 / 0.95 / 0.95 / 0.61 (index micros; MGC is higher, in comments only). | `core/firm_rules.py:133-135`, `:319-321`, `:365-378`, `:403-404`, `:458-464`, `:478-558` |
| F-6 | Candidate #1's registered non-candidate calibration reference is the 3-leg native full-Aegis book, as run in futures3 remc. It was already run on all four tiers (EOD, 10k, Run-2, 2026-07-15): Bulenox 21.52%, Tradeify 17.88%, MFFU 17.74%, BluSky 26.68%. *Corrected 2026-10-05; this row first cited only 17.70% Tradeify.* |  [candidate #1 prereg](../briefs/pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md) §3 (:148-159); `lab/analysis/c1/class_s_candidate1_scoring_2026-07-15/RESULTS.md:81-86` |
| F-7 | Class-S #1 and #2 are both used: #2 is the 3-leg Aegis book `class_s_candidate2_scoring_2026-07-15`, FALSIFIED all-four-fail. The next free number is #3. *Corrected 2026-10-05; this row first said no other number was in use.* | `lab/CATALOG.md:109`; `docs/briefs/Q-COMPOSE-1-orb-classs-book-regime-breadth.md:45` |
| F-8 | Four-firm H reads "… before any live account spend". The revert trigger also bars citing the ADR as live mandate after demotion. | [four-firm ADR](../adr/2026-07-12-prop-portfolio-four-friendly-firms.md) :77, :79 |
| F-9 | D-T00 wording: "Step 2's pre-registration cites [v2] and either adopts it or states why …; no second pre-registration for the same falsifier." | [checklist amendment](../superpowers/plans/2026-09-21-tradeify-deployment-checklist-amendment-PROPOSAL.md) :132 |
| F-10 | STATE's 2026-11-08 row already carries the b1/b3/b6 PARK expiries and the §4 demotion check. | [STATE](../../STATE.md#2026-11-08) :136-141 |
| F-11 | Slice B (per-tier T00 replay) is conditional on design (ii), which was not chosen. Own-flat deadlines are not in code. | [Slice A card](../briefs/handoffs/2026-10-02-remc-o4-slice-a-build-card.md) §8 :158 |

## Recommendations

| ID | Recommendation | Consequence | Sources |
|---|---|---|---|
| **O-5** firm rules | **No per-tier replay code.** Each tier reads through its own `firm_kwargs` (v2 G4). The lab series is built once, under Tradeify's rules. Each tier's daily series is netted at that tier's `cost_per_side_usd`, so the builder emits gross P&L plus per-day contract-sides. Caps need nothing: the Tradeify cap of 80 is the lowest. Flatten needs one pre-registered admissibility rule: **an MFFU clear counts toward I-4 only if no series position is open past 16:10 ET on any day.** The builder checks this mechanically at run time; on failure MFFU reads "inadmissible, 16:10 unmodeled". Disclose MGC costed at the index-micro rate as an optimistic bias. | No `core/firm_rules.py` change and no Slice B. If the book holds positions past 16:10, discharge needs Tradeify plus one other firm (Tradeify becomes the only `trailing_locking` route). Bulenox and BluSky keep F2 optimistic labels. Harness change: `score_candidate` takes one `candidate_daily_pnl` and reuses its blocks for every tier (`prop_survivor_scoring.py:652-731`), so it needs a per-tier series argument, with `intraday_low` netted to match. | F-5, F-11; v2 G2, G4 |
| **O-6** depth, path, budget | **Adopt v2 G4 verbatim:** 10,000 sims × seeds 42/123/2026, horizon 1500. Blocks are Monday-anchored 5-day weeks from `paired_blocks_from_daily`, with one index set per sim shared by both channels. Path start is pristine (O-9). Budget: before freeze, time one tier × one seed at 10k on synthetic same-shape blocks (§R allows synthetic). Pre-register a cap of one executor session covering candidate and reference: Run-1, Run-2 and the guard arms on four tiers. | No new path parameter. TB-F1 block choice applies only to design (ii). Drop the "bar-level replay cost" text. | F-1; v2 §2 G4; Slice A card §0 |
| **O-7** Run-1 | **Run Run-1 as a diagnostic; it is not waivable.** v2 requires both runs where consistency exists and gates on Run-2. Strike the `UNDETERMINED`/A5 path-verdict text: it belongs to design (ii). | About 2× compute on Tradeify, MFFU and BluSky. Bulenox runs once. | F-4; v2 §7(5) |
| **O-8** protection | **Book policy ON inside the bootstrap.** O-2's candidate is the book "with its own protection policy" (prereg §1a), and running it OFF would measure a different candidate. Thread `dd_trigger`/`dd_scale` keywords through `score_candidate` → `run_tier_remc`, defaulting to `NO_PROTECTION_TRIGGER`. Values are passed by the executor (lab cannot import ops). Add a `tests/` parity test, on synthetic paths, that the kernel's scaling equals `book_policy`'s rule. Add a builder check that the export series carries no protection scaling, to avoid a double application. Disclose the departure from v2's "default OFF" as part of the candidate definition, not a gate overlay. The calibration reference keeps its own posture (OFF). Disclose that the policy is the single unadmitted `Tradeify_Select_100K` instance (`book_policy.py:62-69`), applied unchanged on all four tiers as part of the candidate, not as an admission of per-tier policies. **Contradicted 2026-10-05:** the availability check ([PR #698](https://github.com/Joshua-Asante/first-passage/pull/698) §7) finds protection is a per-leg quantity rule, not a P&L scale, so this mechanism cannot pass its parity test. A mode-switching bootstrap over normal and protected inputs is the faithful replacement. **Re-ruled 2026-10-05: mode-switching**, falling back to protection OFF if the code PR is not merged by 2026-10-25 (#616 I-17). | Harness change: freeze blocker 4 must name O-8 (Codex r4179012744). Continuous 0.40× scaling only approximates integer contracts; that is already inside O-4's named daily-series risk. | F-2, F-3, F-4; prereg §1a, I-17 |
| **O-9** initial state | **Pristine $100K on all four tiers.** | The Tradeify read is a fresh-eval read, not the odds for the incumbent account (whose state stays private and covers one tier only). | v2 §3 common band; AGENTS.md "Account" |
| **O-10** riders | (a) **Calibration reference:** reuse candidate #1's registered reference (F-6), same harness, same session, run once. Use the intraday channel if one is buildable; the EOD fallback first recommended here departs from #616's "same harness and clock" and is withdrawn: settle the reference clock before freeze (its panel is not retained; PR #698). Disclose all four prior cells (F-6). Each is ≥ 3.5× the ceiling and the intraday clock only raises bust, so AMBIGUOUS is predicted not to fire; the operator accepts that explicitly. **Ruled 2026-10-05: "Accept, intraday"**; the panel is reassembled before freeze (step 3e). (b) **Regime rider:** adopt candidate #1 §6's text unchanged. The half-panel split is reported beside the verdict, never overturns it, and rides into G8. (c) **G1/G2 are mandatory, not operator options** (Codex r4179012739). A G1 `NO`, or a G2 kill on every tier, means no tier clears: FALSIFIED early-fail. | Removes I-22 from OWED. The reference adds one candidate-sized run to the O-6 budget. Reference panel availability is checked in step 3a. | F-4, F-6; v2 §7(4), (7), (9); candidate #1 §6, §8 |
| **O-11** results | **Public `lab/analysis/<dated slug>/RESULTS.md`**, holding per-tier aggregates only: bust, pass, median days, `breach_clock`, `gate_grade`, admissibility labels. Its header cites this prereg and v2 by path (v2 hook 6). Inputs (TV exports, ports, effective inputs) stay private in the primary checkout. The verdict is a dated addendum at the **withdrawal ADR** plus the STATE 11-08 row; SESSIONS cites v2. Fix the private-root option, which points at the four-firm ADR (Codex r4179012748). | One public verdict location, matching §8 step 7. Nothing vendor-licensed or account-specific is published. | prereg §8.7; candidate #1 §8; AGENTS.md "Public-clone posture" |
| **O-14** D-T00 wording | **Confirm.** This file is a candidate-and-run-contract pre-registration under v2, not a second gate pre-registration. Write that phrase in §0. | Any change to a v2 number closes v2 (Trap #12); it is never edited here. | F-9; v2 §5 |
| **O-15** post-11-08 deployment pass | **Remove from this file. It is not a freeze input.** Route it to the deployment-checklist owner as its own decision. Recommend not adopting it as a new rule: the four-firm revert trigger already bars citing the ADR as live mandate after demotion (F-8). Whether Track B rests on that mandate is the owner's question. | Unblocks freeze. Track B gates are unchanged. | F-8; prereg O-15 text |
| **O-16** dates | **Freeze by Fri 2026-10-23; run by Fri 2026-10-30; verdict recorded by Fri 2026-11-06.** | Leaves about two weeks for the step-3 builds and one week of slack. Missing freeze-by means the O-13 path (FALSIFIED, undischarged at deadline); there is no in-place re-run either way. | four-firm ADR §4; O-13 ruling |
| **O-17** "before any live account spend" | **Read as historical sequencing. Record that reading at the four-firm ADR (dated addendum), not here.** Live spend stays gated by M1 `RESOLVED` plus a per-session GO. | The incumbent eval does not void the falsifier. Removed from this file's blockers. | F-8; AGENTS.md "Live-execution posture" |
| **O-18** PARK expiries b1/b3/b6 | **Separate decision, not a freeze input.** Rule them in the 11-08 sitting STATE already schedules. Keep a pointer only. | Unblocks freeze. The re-MC neither renews nor expires them. | F-10 |

Also owed to the operator, outside the O-list: **Class-S number = candidate #3** (F-7; corrected from #2, which is taken; operator confirmed directly 2026-10-05) for the §1a row, and explicit **adoption of the INSUFFICIENT verdict**, which was still labeled "proposed" (Codex r4179012756).

## DRAFT → FROZEN steps

Owners and by-dates (all before freeze-by 2026-10-23):

| Step | Owner | By |
|---|---|---|
| 1 Rulings | operator (Joshua) | done 2026-10-05, including the O-8 re-ruling and the I-20 acceptance |
| 2 Codex fold | coordinator (4) | done at `7f0cefb` |
| 3a Availability | coordinator (4) worker | done ([PR #698](https://github.com/Joshua-Asante/first-passage/pull/698)) |
| 3b Series builder | coordinator (4), dispatched worker | 2026-10-16 |
| 3c Per-tier series and cost netting | coordinator (4), dispatched worker | 2026-10-16 |
| 3c′ O-8 mode-switching code PR (Codex review) | coordinator (4), dispatched worker | merged by 2026-10-25, else the pre-registered fallback (protection OFF) |
| 3e Reassemble the reference panel (intraday) | coordinator (4), dispatched worker | 2026-10-16 |
| 3d Timing | coordinator (4), dispatched worker | 2026-10-19 |
| 4 Fill | coordinator (4) | 2026-10-20 |
| 5 Pre-freeze audit | coordinator (4) | 2026-10-21 |
| 6 Sign and freeze | operator | 2026-10-23 |
| 7 Commit to main | coordinator (4) (merge agent) | 2026-10-23 |

1. **Rulings.** The operator rules O-5..O-11, O-14 and O-16; disposes of O-15, O-17 and O-18 out of the file; and adopts Class-S #3 and INSUFFICIENT.
2. **Fold the Codex review at `8f8d093`** (unanswered), plus the stale F-1 text:
   - r4179012750: narrow §R to decision-bearing tier screens and MC. Exempt the completed P7 producer-verification replay and disclose it in §1b.
   - r4179012755: AMBIGUOUS overrides every candidate-level verdict; state the precedence.
   - r4179012756: INSUFFICIENT is adopted per step 1, with no "proposed" label.
   - r4179012739: G1/G2 are mandatory (O-10c).
   - r4179012744: blocker 4 names O-8.
   - r4179012748: the O-11 private option points at the withdrawal ADR.
   - r4179012725: the SHA cannot sit in its own commit. Drop §9's freeze-SHA field and record the SHA in the PR comment, the RESULTS header and the withdrawal-ADR addendum.
   - r4179012727: write the negative hooks as `! grep …`, so absence exits 0.
   - r4179012728: one grep per tier literal.
   - r4179012732: derive port paths from `core/strategies/BOOK_SOURCES.sha256` and check each with `git ls-files`.
   - r4179012753: replace the `intraday_blocks` grep with the Slice A synthetic tests, `tests/test_prop_survivor_intraday_channel.py` and the `score_candidate(intraday_low=…)` tests.
3. **Build packets.** Each has its own frozen card. Code merges only after synthetic tests pass, with a launcher `record.json`; private outputs never merge:
   - (a) **Availability check first** (prereg O-4 first build step). For each of the four legs at the P7 identities, a TV-export trade list exists with a per-trade adverse-excursion column, and the reference panel exists. Existence and columns only: no metric is computed (a structural count is a look). Any gap means INSUFFICIENT, raised now rather than at run time.
   - (b) **Series builder.** Public `lab/` code, tested on synthetic inputs and merged; it reads the private exports only at run time and writes to a gitignored private root. Outputs: daily gross P&L, per-day contract-sides, `intraday_low` (≤ 0; the conservative coincident-excursion sum is recommended), the 16:10 flag and the no-protection check.
   - (c) **Harness:** per-tier series and cost netting (O-5).
   - (c′) **O-8 mode-switching code PR:** paired normal and protected channels, a day mode from `book_policy.is_protected`, and a day-mode parity test against `book_policy` (the `dd_scale` test is retired). It may merge after freeze, until 2026-10-25; the fallback is fixed in #616 I-17.
   - (e) **Reassemble the I-20 reference panel** with its intraday channel; if that can't be built, the run reads INSUFFICIENT.
   - (d) **Synthetic timing** for the O-6 cap.
4. **Fill the prereg.** Claude fills §1a identity from public pins (`BOOK_SOURCES.sha256` digests, no bodies), §2 cells from the rulings, and §1b prior looks (P7 replay, the 09-09/10 screen, per-leg looks). The operator adds any further prior look to §D.
5. **Pre-freeze audit.** Run the corrected §10 except the Status and signature hooks, and re-run it after any text change.
6. **Sign and freeze.** The operator signs §9 and says "freeze". Status becomes ``**Status:** `FROZEN YYYY-MM-DD` ``. The full §10 runs in that commit; any failure reverts the Status.
7. **Commit to main.** Merge the FROZEN PR before any executor packet, satisfying the existing-strategy ADR §5 "committed" condition. Record the freeze SHA outside the file, per the r4179012725 item in step 2.
8. **Out of scope here:** the executor run, its verdict and the 11-08 program check (prereg §8 steps 6-7).

## Contradictions checked

- O-8 against v2 §7(6) ("default OFF"): resolved by treating the policy as part of the candidate (O-2), not as a gate overlay. It is flagged for the operator, not assumed.
- §R against the completed P7 replay: real, and fixed by step 2.
- Neither blocks this sheet, so there is no NEEDS_CONTEXT.
- *Added 2026-10-05, after the review of `774ed0e` and the availability check:* the Class-S #2 premise was false (F-7), and so was O-8's P&L-scale premise. Both are corrected above. O-8 was re-ruled the same day (mode-switching with a dated fallback).
