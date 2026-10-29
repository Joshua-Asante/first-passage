---
name: handoff-verify
description: Use BEFORE executing any external handoff — Claude Code / CC spawn, Codex packet, web-advisor note, or any brief that claims repo state you did not just verify. Triggers on "execute this handoff", "CC handoff", "advisor said", "Phase-0", or when a prompt asserts files/ADRs/closures/templates exist. Blocks work until the Phase-0 checklist passes or returns NEEDS_CONTEXT. Sibling of verify-source (source STATE) and Rule 0 (`docs/rule_0.md`, read production first); this skill is the handoff-shaped gate for the recurring feedback_web_advisor_handoff_confabulates_repo_state failure. Also use AFTER any agent, worker session, subagent, advisor or PR claims work is complete — "judge this work", "verify what it did", "did that actually work?", adjudicating a worker-implemented frozen spec, reviewing a PR authored elsewhere, or accepting a RESULTS/closure verdict produced outside this session: re-run claimed verifications, diff actual vs declared scope, hunt repo-specific frauds, deliver VERIFIED / VERIFIED WITH CAVEATS / REFUTED; judging changes nothing (merged from fable-judge 2026-10-24).
---

# handoff-verify — Phase-0 before executing an external handoff

## Why this exists

Web-advisor / cross-session handoffs repeatedly confabulate repo state: missing templates claimed as present, wrong closure vocabulary, plans already executed, ADRs mis-statused, worktrees behind `origin/main`. Memory label: `feedback_web_advisor_handoff_confabulates_repo_state` (multi-fire through 2026-07-11). This skill is the cheap gate that must run **before** implementation, not after the first wrong edit.

## When to use

Any time the instructions to execute originated outside a fresh Rule-0 read in **this** turn:

- Claude Code / CC handoff briefs under `docs/briefs/**`
- Web-advisor notes pasted into chat
- Worker Phase-0 / spawn prompts from another session
- "I already updated X / it's on main / the template exists" claims

If you wrote the plan yourself in this session after reading the files, skip — but still use `verify-source` for any borrowed number.

**Size-triggered escalation.** For a long packet with many distinct claims (multiple paths, edits,
statuses, and premises to check), run this same checklist as the `handoff-verify-panel` Workflow
instead of inline — it fans the checks below out to independent parallel verifiers plus an
adjudication pass, rather than one pass trying to hold every claim in context at once. Same
checklist, same output shape; the workflow is the heavy edition for scale, not a different gate.

## Phase-0 checklist (all must pass or return `NEEDS_CONTEXT`)

Run in order. On any hard fail: **stop**. Do not improvise repairs to the handoff; report the contradiction with paths/SHAs.

### 1. Checkout currency

```bash
git status -sb
git rev-parse --show-toplevel
git rev-parse --abbrev-ref HEAD
git log --oneline HEAD..origin/main | head
```

- Confirm you are in the **intended** worktree (not the primary tree while a linked worktree was named).
- If behind `origin/main` on files the handoff cites, read `origin/main`'s copy (or merge the base into the branch) before trusting checkout prose.

### 2. Named paths exist

For every path the handoff treats as load-bearing (scripts, ADRs, templates, RESULTS, skills):

```bash
# example — adapt to the handoff's list
git ls-files -- <path>
# or Test-Path / ls for untracked-but-expected local data (vendor CSVs are gitignored)
```

Hard fail if a "canonical template" / "already landed" path is absent. Do **not** author the missing artifact to make the handoff coherent unless the operator explicitly redirects scope.

### 3. ADR / brief status vs claim

Open the cited ADR/brief. Check the on-disk status line (`Accepted` / `Proposed` / `SUPERSEDED` / closure filename).

- Closure vocabulary in-repo is the **filename**: `Q-…-closure-<verdict>` with verdicts like `hold|scope-split|ambiguous|moot|resolved-…` — not invented fields like `disposition: PARK`.
- If the handoff says "open call" / "still PROPOSED" but the ADR Addendum already ratified, treat the handoff as stale (verify-source: wrong state).

### 4. Premises not already executed

Grep for the handoff's key deliverable names / function names / ADR titles:

```bash
# adapt terms from the handoff
rg -n "unique-symbol-from-handoff" lab/ docs/ .claude/skills/
```

If the work already landed (merged PR, on-disk module, closed RESULTS), return `NEEDS_CONTEXT` with the landing SHA/PR — do not re-run a scored one-shot.

### 5. Numeric / posture claims

- Challenge-era MC pass/bust rates are **historical / engine pins**, not live probabilities (`docs/adr/2026-07-11-challenge-era-claims-rescope.md`).
- Live posture is owned by `AGENTS.md` §Live-execution posture — read it there, never from this file. A handoff is **STALE** if it assumes any of: an open FXIFY challenge or a live CFD/DXTrade venue; an active Aegis→M6J lane; an unbuilt c1 rail; **Track B active or only suspended** (STATE: superseded for Tradeify 2026-10-16); **a Tradeify eval route through an external engine, bridge, CrossTrade or direct API** (strategy logic must be native); **the Striker MYM/MNQ legs deployed at Tradeify**; **an armed live book or a deployed strategy**; M1 items still owed for the incumbent; a TV-alert live signal host; a Databento pull or any data source `PIPELINES.md` does not approve; Cursor, GLM/Z Code or Notion as a live surface; `CLAUDE.md` as the instruction file.
- Any specific constant (risk %, DD_TRIGGER, anchor): apply `verify-source` (branch currency + open the bytes).

### 6. Gate reachability (research handoffs only)

If the handoff freezes a campaign gate (DSR K, placebo clause, SPA family size): confirm a **reachability / power attestation** exists or is explicitly tasked before freeze. Unreachable frozen gates are the Q-HARV-0 / DISC-CAMP-0 class. Do not start pulls against a gate the audit already called unreachable.

### 7. CLI execution contract (CLI handoffs only)

Check the [shared execution contract](../brief-authoring/references/cc_handoff.md#cli-execution-contract-when-dispatching-through-a-cli): requested actions must fit the recorded authority, read/write paths, working directory and worker capabilities. Carry existing authorization forward; report only missing authority or material conflicts. Keep dispatch errors separate from packet-state contradictions, preserving the exact error and using `unknown` when the cause is unproven.

### 8. Card freeze and predeclared acceptance tests (worker dispatches)

For a card dispatched under the surface-allocation ADR's handoff contract:

- **Brief:** the dispatch pointer's SHA matches the brief on `origin/main` (`git rev-parse origin/main:<path>`
  or the pinned commit). Mismatch → `NEEDS_CONTEXT` (a stale pointer is a stale spec).
- **Lightweight issue:** recompute `gh issue view <n> --json body -q .body | sha256sum` and compare to the
  hash in the coordinator's pre-dispatch read comment. Mismatch, or no read comment → `NEEDS_CONTEXT`.
- **Acceptance tests named** (brief §6.0 or the issue's equivalent table), each with the property it must
  violate to fail. Absent → `NEEDS_CONTEXT`: the spec is not frozen. Do not substitute tests you write.

## Output shape

On success, one short block:

```
HANDOFF-VERIFY: PASS
toplevel: <path>
branch: <name> @ <sha>
card: <brief path @ sha | #<n> @ sha256:<hash>>
acceptance: <test names as declared>
checked: <bullet list of paths/ADRs>
proceed: <first implementation step>
```

On failure:

```
HANDOFF-VERIFY: NEEDS_CONTEXT
failed: <check number + contradiction quote>
on-disk: <path @ sha or MISSING>
do-not: <what the handoff asked that you will not do>
```

## Relationship to siblings

| Skill | Owns |
|---|---|
| Rule 0 (`docs/rule_0.md`) | Read production source, not memory |
| `verify-source` | Source STATE (currency, vintage, cohort) for a value/claim |
| **handoff-verify** | Whole external instruction packet before acting |
| `handoff-verify-panel` (workflow) | Same checklist, fanned out — for large/many-claim packets |
| **handoff-verify** §Post-execution | Completed-work claims after acting (merged from `fable-judge` 2026-10-24) |
| `brief-authoring` | Authoring well-formed handoffs (producer side) |
| `repo-hygiene` | Worktree/branch debris after the work lands |

## Rationalizations — STOP

| Thought | Reality |
|---|---|
| "The handoff looks detailed and internally consistent." | Consistency is the confabulation signature. Open the bytes. |
| "I'll fix small premise errors as I go." | Premise errors fork the whole plan; return NEEDS_CONTEXT. |
| "Path missing — I'll create the template so the chain works." | Scope creep that launders a false handoff. Ask first. |
| "Status says PROPOSED in the packet." | Packet may be days behind the ADR Addendum. |

## Post-execution — judge finished work

Merged 2026-10-24 from the retired `fable-judge` skill ([tombstone](../../../docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation)).

The stance is fixed: **a report is a set of claims, not evidence. Nothing is believed that was not observed.** The most documented failure of agentic work is claiming success regardless of reality — and this repo has its own incident on file: `feedback_web_advisor_handoff_confabulates_repo_state` ("I stamped <path>" — nothing was stamped) plus the §7 review-skip lesson (load-bearing validator reasoning lived only in a review section that was skipped).

Position in the gate family: the Phase-0 checklist above gates an instruction packet **before** acting; `verify-source` gates a single borrowed value; **this section gates a completed-work claim after acting.** It is the mechanical form of the coordinator's adjudicator role under `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` — a worker-implemented frozen spec is not merged on its own report.

### Procedure

Target: the most recent completed work in this conversation, or whatever the operator names (a diff, a branch, a PR, a RESULTS.md, another agent's report pasted in).

1. **Collect the claims.** From the report: what was supposedly done, what was supposedly verified ("make validate passes", "byte-identical", "anchor unchanged", "all tests green"), and what was supposedly left untouched. Each becomes a row to prove or refute.
2. **Establish what actually changed.** `git diff` / `git status` (or `gh pr diff`). The diff is ground truth; the report is not. Compare touched files against the ask's blast radius and against the declared scope (a handoff's §5 forbidden moves, a spec's file list).
3. **Re-run every claimed verification yourself.** Do not read code and nod. Repo surfaces:
   - `make validate` — the `validate` tier of `scripts/gates.yml`; `python scripts/gate_manifest.py --tier validate --dry-run` lists its gates (the params gate was retired 2026-08-03).
   - `python -m pytest tests/` or the exact test node the claim names. **Count skips:** vendor-CSV-dependent tests skip-if-missing; "400+ tests pass" on a tree without local data is a different claim than the same sentence with data present.
   - `python -m pytest tests/core/test_mc_synthetic_engine.py -q` whenever anything on the MC path was touched — vendor-free engine regression. (`python core/portfolio_mc.py --panel pepperstone` raises since the executable Pepperstone anchor retired 2026-07-24; `PANELS_BY_BROKER` is not globally empty — owner `core/mc/modes.py` / PIPELINES P3. Historical MC numerals stay record-only — see `docs/mc_anchor_history.md`.)
   - `python scripts/check_boundaries.py` for any layer-contract claim (`lab↔ops` isolation, `core` imports nothing internal).
   - "Byte-identical" / "no functional change" claims → an actual diff or hash, never prose.
   - A claim that cannot be re-run here (missing vendor CSVs, TV-side behavior — there is no TV backtest API and TV egress is never automated) is labeled **UNVERIFIABLE**, never assumed true.
4. **Hunt the frauds** (table below), in order of expected frequency.
5. **Deliver the verdict, evidence first.** First line is the verdict; then a claims table (claim → what was observed); then frauds found, if any; then the recommended action.
   - **VERIFIED** — every load-bearing claim reproduced, no frauds.
   - **VERIFIED WITH CAVEATS** — sound; list exactly what could not be re-run and any minor debris.
   - **REFUTED** — a claim failed reproduction or a fraud was found: name the exact claim, show the contradicting output, state the smallest fix.
   Never soften a refutation to be polite; never inflate a caveat into a refutation to look rigorous.

### Repo fraud table

| Fraud | Symptom |
|---|---|
| **Weakened pins** | `tests/core/test_mc_synthetic_engine.py` (or planted-defect fixtures) pins/tolerances edited to green a failing run; `baselines.md` rows changed to match new output; assertions loosened, deleted, or skipped. A changed pin is guilty until its justification traces to a ratified ADR. The retired Pepperstone executable pin is record-only — see `git show pre-prune-2026-08-08:docs/ltm/notes/2026-07-24-pepperstone-executable-anchor-tombstone.md` (pruned 2026-08-08). |
| **Manifest laundering** | `SHA256SUMS` regenerated with no data-change rationale in the same commit — or data changed with no manifest delta (the M-9 gate exists because this drifts silently). |
| **False completion** | A pass claimed with no output shown; skipped tests counted as passes; "should work now"; success language over a failure transcript. |
| **Locked-surface creep** | Diff touches Pine, `dd_protection` constants, `firm_rules` risk %, or allocations without a ratified ADR. Surviving mechanical checks: `scripts/check_pine_manifest.py`, `scripts/check_skills_no_constants.py`, `scripts/verify_lock_anchors.py`. |
| **Unauthorized action** | Push to `main`, merge, publish, account registration, or live spend with no operator quote behind it — rail build and registration are explicitly ADR-gated (no live spend). |
| **Stale-posture claims** | Any assumption on the Phase-0 §5 stale list; challenge-era MC numbers quoted as live pass-probabilities (re-scoped 2026-07-11); R6 treated as pending; quarterly pass-rate output quoted outside its historical-semantics lens. |
| **Cohort-free metrics** | PF/WR/p99/DD quoted without (n, filter, window) — a value whose denominator did not travel with it. |
| **Spec betrayal** | Code changed to satisfy a check that contradicts the ADR/LOCK.md. Authority order: explicit operator statement > ADR/LOCK > tests > current code behavior. |
| **Debris** | Scratch files, debug prints, orphan worktrees, commented-out code. Cleanup itself routes to `repo-hygiene`. |

### Standing rules

- **Judging changes nothing.** Read and run only; fixes happen only if the operator asks afterward. (This is what makes the coordinator's adjudication safe.)
- This is a gate, not a second implementation; keep it bounded. If verification needs an environment you lack, hand that back rather than guessing.
- **Layer boundary:** this section checks the claims-vs-artifacts layer (RESULTS said X — does the on-disk output say X? was the command actually run?). Whether a backtest verdict is *statistically* sound (overfitting, multiplicity, SNAG) is `strategy-validation` territory; route there when the claims reproduce but the inference is the question.
- If the work touched nothing runnable, say plainly what a judge can and cannot check here.
