---
name: fable-judge
description: Adversarial verification of finished work — a "done" report is a set of claims, not evidence. Use AFTER any agent, advisor, Cursor session, subagent, or PR claims work is complete. Triggers on "judge this work", "verify what it did", "did that actually work?", adjudicating a Cursor-implemented spec (CC adjudicates per the 2026-07-14 CC/Cursor surface-allocation ADR), reviewing a PR authored elsewhere, or accepting a RESULTS/closure verdict produced outside this session. Re-runs claimed verifications, diffs actual vs declared scope, hunts repo-specific frauds, delivers VERIFIED / VERIFIED WITH CAVEATS / REFUTED. Post-execution sibling of handoff-verify (pre-execution packet gate) and verify-source (single value/claim). Judging changes nothing — read and run only.
---

# fable-judge — adversarial verification of finished work

Adapted 2026-07-15 from `Sahir619/fable-method@88b5cf3` (`skills/fable-judge/`); the repo-specific fraud table and verification surfaces below replace the source's coding defaults. Port record lives in the private archive (excluded from the public seed).

The stance is fixed: **a report is a set of claims, not evidence. Nothing is believed that was not observed.** The most documented failure of agentic work is claiming success regardless of reality — and this repo has its own incident on file: `feedback_web_advisor_handoff_confabulates_repo_state` ("I stamped <path>" — nothing was stamped) plus the §7 review-skip lesson (load-bearing validator reasoning lived only in a review section that was skipped).

Position in the gate family: `handoff-verify` gates an instruction packet **before** acting; `verify-source` gates a single borrowed value; **this skill gates a completed-work claim after acting.** It is the mechanical form of CC's adjudicator role under `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` — a Cursor-implemented frozen spec is not merged on its own report.

## Procedure

Target: the most recent completed work in this conversation, or whatever the operator names (a diff, a branch, a PR, a RESULTS.md, another agent's report pasted in).

1. **Collect the claims.** From the report: what was supposedly done, what was supposedly verified ("make validate passes", "byte-identical", "anchor unchanged", "all tests green"), and what was supposedly left untouched. Each becomes a row to prove or refute.
2. **Establish what actually changed.** `git diff` / `git status` (or `gh pr diff`). The diff is ground truth; the report is not. Compare touched files against the ask's blast radius and against the declared scope (a handoff's §5 forbidden moves, a spec's file list).
3. **Re-run every claimed verification yourself.** Do not read code and nod. Repo surfaces:
   - `make validate` — params + data manifests + pine manifest gates.
   - `python -m pytest tests/` or the exact test node the claim names. **Count skips:** vendor-CSV-dependent tests skip-if-missing; "400+ tests pass" on a tree without local data is a different claim than the same sentence with data present.
   - `python -m pytest tests/core/test_mc_synthetic_engine.py -q` whenever anything on the MC path was touched — vendor-free engine regression. (`python core/portfolio_mc.py --panel pepperstone` raises since the executable anchor retired 2026-07-24; `PANELS_BY_BROKER = {}`. The 99.83/0.17/4.37 figures are historical record, not a live pin.)
   - `python scripts/check_boundaries.py` for any layer-contract claim (`lab↔ops` isolation, `core` imports nothing internal).
   - "Byte-identical" / "no functional change" claims → an actual diff or hash, never prose.
   - A claim that cannot be re-run here (missing vendor CSVs, TV-side behavior — there is no TV backtest API and TV egress is never automated) is labeled **UNVERIFIABLE**, never assumed true.
4. **Hunt the frauds** (table below), in order of expected frequency.
5. **Deliver the verdict, evidence first.** First line is the verdict; then a claims table (claim → what was observed); then frauds found, if any; then the recommended action.
   - **VERIFIED** — every load-bearing claim reproduced, no frauds.
   - **VERIFIED WITH CAVEATS** — sound; list exactly what could not be re-run and any minor debris.
   - **REFUTED** — a claim failed reproduction or a fraud was found: name the exact claim, show the contradicting output, state the smallest fix.
   Never soften a refutation to be polite; never inflate a caveat into a refutation to look rigorous.

## Repo fraud table

| Fraud | Symptom |
|---|---|
| **Weakened pins** | `tests/core/test_mc_synthetic_engine.py` (or planted-defect fixtures) pins/tolerances edited to green a failing run; `baselines.md` rows changed to match new output; assertions loosened, deleted, or skipped. A changed pin is guilty until its justification traces to a ratified ADR. The retired Pepperstone executable pin is record-only — see `git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md` (pruned 2026-08-08). |
| **Manifest laundering** | `SHA256SUMS` regenerated with no data-change rationale in the same commit — or data changed with no manifest delta (the M-9 gate exists because this drifts silently). |
| **False completion** | A pass claimed with no output shown; skipped tests counted as passes; "should work now"; success language over a failure transcript. |
| **Locked-surface creep** | Diff touches Pine, `dd_protection` constants, `firm_rules` risk %, or allocations without a ratified ADR. Surviving mechanical checks: `scripts/check_pine_manifest.py`, `scripts/check_skills_no_constants.py`, `scripts/verify_lock_anchors.py`. |
| **Unauthorized action** | Push/merge/publish, account registration, or live spend with no operator quote behind it — rail build and registration are explicitly ADR-gated (no live spend). |
| **Stale-posture claims** | Challenge-era MC numbers quoted as live pass-probabilities (re-scoped 2026-07-11); FXIFY treated as open; R6 treated as pending; quarterly pass-rate output quoted outside its historical-semantics lens. |
| **Cohort-free metrics** | PF/WR/p99/DD quoted without (n, filter, window) — a value whose denominator did not travel with it. |
| **Spec betrayal** | Code changed to satisfy a check that contradicts the ADR/LOCK.md. Authority order: explicit operator statement > ADR/LOCK > tests > current code behavior. |
| **Debris** | Scratch files, debug prints, orphan worktrees, commented-out code. Cleanup itself routes to `repo-hygiene`. |

## Standing rules

- **Judging changes nothing.** Read and run only; fixes happen only if the operator asks afterward. (This is what makes the CC-adjudicator role safe.)
- This is a gate, not a second implementation: minutes, not hours. If verification needs an environment you lack, hand that back rather than guessing.
- **Layer boundary:** this skill checks the claims-vs-artifacts layer (RESULTS said X — does the on-disk output say X? was the command actually run?). Whether a backtest verdict is *statistically* sound (overfitting, multiplicity, SNAG) is `strategy-validation` territory; route there when the claims reproduce but the inference is the question.
- If the work touched nothing runnable, say plainly what a judge can and cannot check here.
