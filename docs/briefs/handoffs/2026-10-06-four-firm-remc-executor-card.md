# CC handoff — four-firm dated re-MC: executor packet (§8 step 6)

**Date:** 2026-10-06.
**Status:** DRAFT. It was drafted on the operator's "GO" (2026-10-06) to draft the executor card. **The run needs a separate operator go on this card.** Nothing runs before that.
**Brief type:** CC handoff, executor packet (decision-bearing run).
**Authority (on go):** a coordinator (4) worker. Requirement owner: the FROZEN pre-registration [`2026-10-02-four-firm-dated-remc-prereg-DRAFT.md`](../pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md) (`FROZEN 2026-10-05`, merged `bfb13f9`) and the gate of record [prereg v2](../pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md). Run by **2026-10-30**; verdict recorded by **2026-11-06**.
**Rule:** this card maps the frozen file onto exact calls. It decides nothing the file leaves open. The one interpretation it adds is flagged in §0.5 item 7 for the operator's go.
**Return boundary:**
- a public RESULTS with per-tier aggregates and the mechanical §4 verdict;
- private full reports;
- a return to coordinator (4), which records the verdict at the withdrawal ADR, STATE and SESSIONS (§8 step 7);
- or NEEDS_CONTEXT under §0.5 item 7.

## §0 — Production reads (`main@dd54369`, 2026-10-06)

Read at `main` `dd54369` on 2026-10-06. Re-read at dispatch.

| Surface | Use |
|---|---|
| Frozen prereg §1a, I-1..I-25, §4, §8 | Candidate identity and pins; gate numbers; verdict table and precedence; start gate; re-hash list |
| `lab/discovery/remc_series_builder.py` (#702) | Candidate per-tier series (normal and protected P&L and lows), the I-24 flag and a manifest |
| `lab/discovery/prop_survivor_scoring.py` `score_candidate(tier_series=…, mode_trigger=…)` (#711), `TierSeries` | One call scores all four tiers. Mode-switching (#708) is forwarded per tier. |
| `lab/discovery/remc_reference_panel.py` (#710) and the private panel `a2e9192a…` | The I-20 reference series and its intraday channel |
| `ops/c1_rail/book_policy.py` `CANDIDATE_TRIGGER` | The `mode_trigger` value; the executor asserts equality, never retypes it |
| `docs/methodology/regime_robustness_gate.md` | The I-21 rider, run only on RESOLVED |

## §0.5 — Clarifications resolved at freeze

1. **Start gate** (I-17):
   - `git merge-base --is-ancestor debc133 origin/main` must succeed, giving branch ON.
   - Record the `main` SHA read and #708's merge SHA `debc13363ff3b85ed5ee41bca97a0ae9d76c5767`.
   - Then re-run the §8 step-3 re-hash (20 digests). Any mismatch: stop (blocker 4b).
2. **Candidate series:** the series-builder CLI with the six §1a inputs at their pinned paths, `--export-tz America/New_York` and the default quantity spec. Output goes to the private root `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/local_artifacts/four-firm-remc-run-<date>/`.
3. **Candidate scoring:** one `score_candidate` call.
   - `tier_series`: each tier's builder CSV (`normal_pnl`, `normal_low`, `protected_pnl`, `protected_low`).
   - `mode_trigger`: `float(Fraction(book_policy.CANDIDATE_TRIGGER))`.
   - `candidate_daily_pnl` (G1 only): the builder's normal-mode daily gross.
   - `full_res_trades` and `gross_edge_usd` (G1/G2): the in-window normal-mode trades' gross P&L after the Aegis rescale, and their sum.
   - `envelope_verdict`: `YES`, because the builder has already enforced same-trade-date entry and exit and no exit in [16:45, 18:00) ET for every trade (it raises otherwise). Record that reason.
   - Thresholds and depth: the v2 defaults (`load_scoring_thresholds()`; 10k × 42/123/2026; horizon 1500).
4. **Reference scoring:** one `score_candidate` call through the same harness, with no mode-switching (I-20, OFF).
   - `candidate_daily_pnl`: the panel's three legs summed.
   - `intraday_low`: the panel's `intraday_low`.
   - `full_res_trades` / `gross_edge_usd`: its scaled trades.
   - `envelope_verdict`: `YES` only if no reference trade spans two trade dates; otherwise `NO`, recorded.
   - The candidate and reference calls may run as two parallel processes (I-15 executor note).
5. **Mechanical verdict** (prereg §4):
   - Precedence: AMBIGUOUS (reference clears Part A on ≥ 2 tiers), then INSUFFICIENT (the candidate report has `gate_grade=False`, the reference's intraday channel is unavailable, or the run is incomplete), then the candidate rows.
   - I-24: when `mffu_admissible` is false, MFFU's Part A clear is set false before `discharges_falsifier` is evaluated. Both values are reported.
6. **RESULTS:** public `lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md`.
   - Header: cites the prereg and v2 by path (v2 hook 6), with the run date, the `main` SHA and the #708 merge SHA.
   - Body: per-tier, per-run bust %, P(pass), median days, `breach_clock`, `gate_grade`, the I-24 label, the reference rows, the verdict and, on RESOLVED only, the I-21 rider.
   - Excluded: dollar figures and input bodies.
   - Full JSON reports stay in the private root, cited by digest.
7. **Flagged interpretation (operator confirms with the go):** if any step fails *before any tier output exists* (a builder raise on real exports, a re-hash mismatch, a harness error), the executor returns **NEEDS_CONTEXT** to the operator: no verdict, nothing seen. Once any tier output exists, a failure reads **INSUFFICIENT** (§4), and nothing is re-run in place (§3, §5).

## §1 — Goal

Run the frozen candidate and the calibration reference once, under the frozen contract, and return the mechanical §4 verdict with RESULTS.

## §4 — Hypothesis and falsifier

H-REMC is the frozen prereg's §3. Verdicts and their precedence are §4 of that file, verbatim: RESOLVED / ONE-TIER / FALSIFIED — partial / FALSIFIED — early-fail / AMBIGUOUS / INSUFFICIENT.

## §5 — Constraints and forbidden moves

- Every forbidden move in prereg §5 applies.
- No varying, no re-running in place, no tier or candidate substitution, no reading outputs before the verdict is assigned mechanically.
- No Pine, port body, effective-input value, account identifier or dollar figure in any public file.
- The budget is one executor session (I-15 bound ≈ 15.9 h serial).

## §6 — Acceptance and return taxonomy

Return labels:
- **DONE:** RESULTS committed in a PR, private reports digested, verdict assigned.
- **DONE_WITH_CONCERNS:** DONE, plus a disclosure.
- **NEEDS_CONTEXT:** under §0.5 item 7.
- **BLOCKED:** with the exact obstruction.

```yaml authority
seat: worker
parent: docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push, pr.open]
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
c=docs/briefs/handoffs/2026-10-06-four-firm-remc-executor-card.md
# RESULTS cites both pre-registrations by path once it exists (v2 hook 6).
test ! -f lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md || grep -c "2026-10-02-four-firm-dated-remc-prereg\|2026-08-26-prop-survivor-scoring-prereg-v2" lab/analysis/c1/four_firm_remc_2026-10/RESULTS.md
# The start gate's ancestry holds on current main.
git merge-base --is-ancestor debc13363ff3b85ed5ee41bca97a0ae9d76c5767 origin/main && echo I-17-ON
```
