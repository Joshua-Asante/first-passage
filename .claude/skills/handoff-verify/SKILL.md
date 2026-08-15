---
name: handoff-verify
description: Use BEFORE executing any external handoff — Claude Code / CC spawn, web-advisor note, Cursor Phase-0 handoff, or any brief that claims repo state you did not just verify. Triggers on "execute this handoff", "CC handoff", "advisor said", "Phase-0", or when a prompt asserts files/ADRs/closures/templates exist. Blocks work until the Phase-0 checklist passes or returns NEEDS_CONTEXT. Sibling of verify-source (source STATE) and rule-0 (read production first); this skill is the handoff-shaped gate for the recurring feedback_web_advisor_handoff_confabulates_repo_state failure.
---

# handoff-verify — Phase-0 before executing an external handoff

## Why this exists

Web-advisor / cross-session handoffs repeatedly confabulate repo state: missing templates claimed as present, wrong closure vocabulary, plans already executed, ADRs mis-statused, worktrees behind `origin/main`. Memory label: `feedback_web_advisor_handoff_confabulates_repo_state` (multi-fire through 2026-07-11). This skill is the cheap gate that must run **before** implementation, not after the first wrong edit.

## When to use

Any time the instructions to execute originated outside a fresh Rule-0 read in **this** turn:

- Claude Code / CC handoff briefs under `docs/briefs/**`
- Web-advisor notes pasted into chat
- Cursor Phase-0 / spawn prompts from another session
- "I already updated X / it's on main / the template exists" claims

If you wrote the plan yourself in this session after reading the files, skip — but still use `verify-source` for any borrowed number.

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
- If behind `origin/main` on files the handoff cites, read `origin/main`'s copy (or ff/rebase per operator) before trusting checkout prose.

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
- Live posture is owned by `CLAUDE.md` §Live-execution posture — read it there, never from this file. A handoff is **STALE** if it assumes any of: an open FXIFY challenge; an active Aegis→M6J lane; an unbuilt CrossTrade rail; **the Striker MYM/MNQ legs deployed at Tradeify**; **an armed live book** (both legs withdrawn 2026-08-04; environment = incumbent eval for **new** strategies with rail warm/disarmed — [`S1 ADR`](../../../docs/adr/2026-08-07-loop-s1-environment-ratification.md); F2/F3 closed).
- Any specific constant (risk %, DD_TRIGGER, anchor): apply `verify-source` (branch currency + open the bytes).

### 6. Gate reachability (research handoffs only)

If the handoff freezes a campaign gate (DSR K, placebo clause, SPA family size): confirm a **reachability / power attestation** exists or is explicitly tasked before freeze. Unreachable frozen gates are the Q-HARV-0 / DISC-CAMP-0 class. Do not start pulls against a gate the audit already called unreachable.

## Output shape

On success, one short block:

```
HANDOFF-VERIFY: PASS
toplevel: <path>
branch: <name> @ <sha>
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
| `rule-0` / `docs/rule_0.md` | Read production source, not memory |
| `verify-source` | Source STATE (currency, vintage, cohort) for a value/claim |
| **handoff-verify** | Whole external instruction packet before acting |
| `fable-judge` | Completed-work claims after acting (post-execution mirror of this gate) |
| `brief-authoring` | Authoring well-formed handoffs (producer side) |
| `repo-hygiene` | Worktree/branch debris after the work lands |

## Rationalizations — STOP

| Thought | Reality |
|---|---|
| "The handoff looks detailed and internally consistent." | Consistency is the confabulation signature. Open the bytes. |
| "I'll fix small premise errors as I go." | Premise errors fork the whole plan; return NEEDS_CONTEXT. |
| "Path missing — I'll create the template so the chain works." | Scope creep that launders a false handoff. Ask first. |
| "Status says PROPOSED in the packet." | Packet may be days behind the ADR Addendum. |
