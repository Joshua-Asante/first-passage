# CC handoff — four-firm dated re-MC: executor packet (§8 step 6)

**Date:** 2026-10-06.
**Status:** DRAFT. It was drafted on the operator's "GO" (2026-10-06) to draft the executor card. **The run needs a separate operator go on this card, after review CLEAN.** Nothing runs before that.
**Brief type:** CC handoff, executor packet (decision-bearing run).
**Authority (on go):** a coordinator (4) worker. Requirement owner: the FROZEN pre-registration [`2026-10-02-four-firm-dated-remc-prereg-DRAFT.md`](../pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md) (`FROZEN 2026-10-05`, merged `bfb13f9`), cited as "prereg". The gate of record is [prereg v2](../pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md). Run by **2026-10-30**; verdict recorded by **2026-11-06**.
**Rule:** the frozen prereg governs. This card only maps it onto calls and adds no rule. Where the merged harness cannot express a frozen step directly, the card states the mechanical equivalent and flags it (§0.5 item 4).
**Return boundary:**
- a public RESULTS with per-tier aggregates and the mechanical prereg §4 verdict;
- private full reports;
- a return to coordinator (4), which records the verdict (prereg §8 step 7);
- or BLOCKED / NEEDS_CONTEXT exactly where §0.5 item 8 says.

## §0 — Production reads (`main@dd54369`, 2026-10-06)

Read at `main` `dd54369` on 2026-10-06. Re-read at dispatch.

| Surface | Use |
|---|---|
| Prereg §1a, I-1..I-25, §4 (:100-109), §7, §8 step 3 | Identity and pins; gate numbers; verdict table and precedence; blockers; re-hash list |
| [Candidate #1 prereg](../pre-registration/2026-07-15-existing-strategy-book-candidate-1-prereg.md) §2, §8 | Frozen G1 envelope criterion: **per-leg** gross edge per round trip ≥ 4× the per-firm RT cost (`2 × cost_per_side_usd`) at `R_deploy`, with pyramid entries counted as fills. G2 is per leg (prereg I-22). |
| `lab/discovery/remc_series_builder.py` (#702) | Candidate series; `parse_trade_list_csv`, `load_trade_table` and `apply_quantity_rule` for per-leg trades; the I-24 flag |
| `lab/discovery/prop_survivor_scoring.py` `score_candidate(tier_series=…, mode_trigger=…)` (#711), `cost_law_kill`, `score_part_a` | One call scores all four tiers. Mode-switching (#708) is forwarded. G2 inside the call is pooled; see §0.5 item 4. |
| `lab/discovery/remc_reference_panel.py` (#710) | The I-20 reference series and intraday channel |
| `ops/c1_rail/book_policy.py` `CANDIDATE_TRIGGER = "0.01"` | `mode_trigger`, asserted, never retyped |
| `docs/methodology/regime_robustness_gate.md` | The I-21 rider, on RESOLVED only |

## §0.5 — Clarifications resolved at freeze

1. **Start gate (I-17):** `git merge-base --is-ancestor debc13363ff3b85ed5ee41bca97a0ae9d76c5767 origin/main` must hold, giving ON. Record the `main` SHA read and that #708 merge SHA. The run starts only after this.
2. **Re-hash (prereg §8 step 3; blocker 4b).** Each value is compared to its pin:

   | # | Input | Pin |
   |---|---|---|
   | 1–8 | `sha256sum -c core/strategies/BOOK_SOURCES.sha256`: Aegis, Striker, Vanguard and ORB Pine; ports `aegis_6j`, `dj30_mym_p250` (corrected), `vanguard_mgc`, `orb_mnq_v7` | `db78ecba…adca7c`, `712cf395…7fffd7`, `af26899c…bad15`, `176c4f70…052a3`; `11763740…e84f`, `efd479b6…11f4`, `e6a03d04…57a3`, `b1f4e573…317d` |
   | 9 | `ops/c1_rail/book_policy.py` at `main` | `ffcd3aab…567a` |
   | 10 | the `BOOK_SOURCES.sha256` manifest | `6dc8b6af…252e` |
   | 11–16 | A-0, S-0, V-0 (Downloads); O-N, S-P, O-P (`E/`) | `71e732fc…6eaa`, `5a500658…998e`, `7b9cc65c…72f9f2`, `8e4902c3…e861`, `0373f211…710a`, `2cb58fb6…3e40` |
   | 17–19 | reference exports ae744, 15d8b, beabf | `e82a2c25…8ca38`, `9acfa297…01b9e`, `8884e6dd…c6419` |
   | 20 | reference panel (I-20 path) | `a2e9192a…aa50a2` |

   Full digests are in prereg §1a / I-20. Any mismatch is **BLOCKED** before the run: no output, no verdict.
3. **Candidate scoring:** one `score_candidate` call.
   - `tier_series`: each tier's series-builder CSV (CLI with the six inputs, `--export-tz America/New_York`, default quantity spec).
   - `mode_trigger`: `float(Fraction(book_policy.CANDIDATE_TRIGGER))`.
   - `candidate_daily_pnl` (G1 expectancy ratio): the builder's normal-mode daily gross.
   - `full_res_trades`: the in-window normal-mode trades' gross P&L. Source: `load_trade_table` → `apply_quantity_rule` with the default spec (Aegis rescaled to 8), in the builder window. Pyramid rows count as fills.
   - v2 defaults: 10k × 42/123/2026, horizon 1500.
   - Record the builder window's start weekday. `paired_blocks_from_daily` blocks positionally, so a non-Monday start gives 5-consecutive-business-day blocks starting on that weekday. That is disclosed, not trimmed.
4. **G1 and G2 per leg** (prereg I-22 → candidate #1 §2, §8). **Flagged mechanism:**
   - **G2:** for each leg and each tier, `cost_law_kill(tier, r_deploy=leg trades, gross_edge_usd=leg gross)`. A tier where any leg fails is **G2-killed**.
   - **G1 envelope:** `YES` if at least one tier has every leg passing; otherwise `NO`, and the call halts at G1 (early-fail).
   - **Equivalence:** the merged `score_candidate` evaluates G2 pooled. The executor therefore passes the per-leg-derived envelope to the call, and treats a per-leg-G2-killed tier as **not clearing**. That tier's G4 figures are withheld from the verdict and from RESULTS. This gives the same verdict as not running the tier. Because a G1 `NO` means every tier is killed, the reading of "per-firm" cannot change any verdict.
5. **Reference scoring:** one call through the same harness, OFF, with `candidate_daily_pnl` = the panel's legs summed and `intraday_low` = the panel's. Prereg §4 AMBIGUOUS is bust-only, so the reference must reach a bust figure on **every** tier: it bypasses G1/G2 (`envelope_verdict="YES"`, `gross_edge_usd=float("inf")`), and that is recorded. Disclosed: the reference trades are net of costs as exported.
6. **Verdict (prereg §4, in order):**
   - **AMBIGUOUS:** the reference's gating-run (Run-2 where consistency exists) `headline_bust` ≤ 0.05 on ≥ 2 tiers, whatever its pass rate. A missing reference bust on any tier is "run incomplete".
   - **INSUFFICIENT**, any of the five frozen triggers: missing producer context; missing synchronized `intraday_low` for a gating tier (`gate_grade=False`); the I-20 reference's intraday channel unavailable; run incomplete at frozen depth; any §2 item unset.
   - **Candidate rows:**
     - I-24 is applied first: if `mffu_admissible` is false, MFFU does not clear.
     - A per-leg-G2-killed tier does not clear.
     - Then count clears: RESOLVED (I-4 met) / ONE-TIER / FALSIFIED — partial / FALSIFIED — early-fail.
7. **Completeness (I-15, I-16):** each call is 19 arms (per tier: guard EOD, zeros and real, plus Run-1; Run-2 on Tradeify, MFFU and BluSky), 38 in total, each 3 seeds × 10k. The executor checks that every non-killed tier has guard, Run-1 and (where consistency exists) Run-2 at 10k. Anything missing is "run incomplete" → INSUFFICIENT.
8. **Stops** (frozen text only):
   - re-hash mismatch → **BLOCKED** (blocker 4b);
   - a builder timestamp-format failure on a real export → **NEEDS_CONTEXT** (series-builder card §7, concern 2);
   - a builder late-exit raise → INSUFFICIENT (series-builder card §0.5 item 2);
   - every other failure follows prereg §4 (INSUFFICIENT).
   Nothing is re-run in place (prereg §3, §5).
9. **RESULTS:** public `lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md`.
   - Header: cites the prereg and v2 by path (v2 hook 6), with the run date, the `main` SHA and the #708 merge SHA.
   - Body: per tier and run, bust %, P(pass), median days, `breach_clock`, `gate_grade`, the I-24 label and G2 per leg; the reference bust per tier; the verdict; the I-21 rider on RESOLVED only.
   - Excluded: dollar figures and input bodies. Full JSON stays private, cited by digest.

## §1 — Goal

Run the frozen candidate and the calibration reference once, under the frozen contract, and return the mechanical prereg §4 verdict with RESULTS.

## §4 — Hypothesis and falsifier

H-REMC is prereg §3 verbatim. Verdicts are prereg §4: RESOLVED / ONE-TIER / FALSIFIED — partial / FALSIFIED — early-fail / AMBIGUOUS / INSUFFICIENT.

## §5 — Constraints and forbidden moves

- Every forbidden move in prereg §5 applies.
- No varying, no re-running in place, no substitution, no reading outputs before the mechanical assignment.
- No Pine, port body, effective-input value, account identifier or dollar figure in any public file.
- Budget: one executor session (I-15 bound ≈ 15.9 h serial).

## §6 — Acceptance and return taxonomy

Return labels:
- **DONE:** RESULTS in a PR, private reports digested, verdict assigned.
- **DONE_WITH_CONCERNS:** DONE, plus a disclosure.
- **NEEDS_CONTEXT / BLOCKED:** only as in §0.5 item 8.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, research.run, worktree.write, branch.push, pr.open]
constraints:
  - no_main_write
  - no_merge
  - frozen_prereg_only
  - no_rerun_in_place
  - no_private_copy_or_commit
  - no_public_dollar_figures
  - no_owner_record_edit
  - no_force_push
acceptance:
  - results_md_with_mechanical_verdict
```

## §7 — Return

*(Filled by the executor after the operator's go.)*

## §10 — Audit hooks

```bash
# RESULTS cites both pre-registrations by path once it exists (v2 hook 6).
test ! -f lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md || grep -c "2026-10-02-four-firm-dated-remc-prereg\|2026-08-26-prop-survivor-scoring-prereg-v2" lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md
# Start-gate ancestry on current main.
git merge-base --is-ancestor debc13363ff3b85ed5ee41bca97a0ae9d76c5767 origin/main && echo I-17-ON
```
