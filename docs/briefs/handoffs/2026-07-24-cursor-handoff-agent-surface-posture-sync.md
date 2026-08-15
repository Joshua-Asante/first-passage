# Cursor Handoff — agent-surface posture sync (skills + settings frozen at the 2026-07-11 posture)

> **STATUS 2026-07-24: DISCHARGED — DO NOT DISPATCH.** All five §2 steps landed
> on `main` before this brief could be dispatched, applying this brief's frozen
> strings verbatim. Verified item-by-item on the merged tree: (2.1)
> `ops/c1_rail/c1_sizing_host_reference.py:10` now opens "This module IS the live sizing
> host"; (2.2) all six dead `cli.py`/`portfolio_mc` allows are gone from
> `.claude/settings.json`; (2.3) `prop-firm-challenge/SKILL.md` carries the
> frozen 2026-07-24 posture block (the only surviving `ops/accounts.py` mention
> is this brief's own "spine is DELETED" sentence); (2.4)
> `handoff-verify/SKILL.md:72` carries the frozen Live-posture line; (2.5)
> `brief-authoring/SKILL.md` has zero "Notion Command Center" hits and
> `pinescript-v6`'s description names the locked-book venue editions.
> **One residual applied directly instead** (the brief's route is spent): the
> frozen posture text predated the 2026-07-22 venue-fact correction, so the
> §4-withdrawal / per-leg-contract-cap / 16:45-ET clause quoted in §2.3 below
> was added straight to the landed skill in the same commit as this stamp.
> Retained as the review record + §10 audit hooks.

**Date:** 2026-07-24
**Parent session:** Claude Code operator session — Algorithm repo review (umbrella: `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`).
**Spawn target:** Cursor
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** N/A — executes verified staleness repairs; no Pre-Q.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **Docstring/description/config text only — zero logic changes anywhere.** All replacement text in this brief is FROZEN by the parent session; apply verbatim, bounce `NEEDS_CONTEXT` on any conflict with Phase-0 reads.
**Dispatch order:** after the deploy-packaging fix (brief #1); BEFORE the gate-estate brief (#3), whose extended `check_skill_refs` gate would otherwise fail on the dead reference this brief removes.

---

## Routing-test self-check (per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`)

- **Test 0:** no vendor bytes, no secrets. Cloud or local eligible. (The post-merge deployed-bundle sync in §7 is operator-local and OUTSIDE this handoff's scope.)
- **Test 1:** No locked surface. Files: 4 × `.claude/skills/*/SKILL.md` (repo copies — the authoring source per `feedback_skill_amendments_via_authoring_path`), `.claude/settings.json`, and the module docstring of `ops/c1_rail/c1_sizing_host_reference.py` (docstring ONLY; its 29-test suite must pass byte-identically on logic). No `core/` anchor code, no Pine, no CLAUDE.md/STATE.md.
- **Test 2:** Yes — every replacement string is frozen below.
- **Test 3:** Clears (~6 files).

---

## §0 — Rule 0 reads (PHASE 0 — read-report before any edit)

Anchors verified by the parent session at `33356ea` (2026-07-24). Report each; `NEEDS_CONTEXT` on contradiction.

- `ops/c1_rail/c1_sizing_host_reference.py` — report the module docstring paragraph beginning "This module is NOT the live host" (anchored ~lines 10–14) and confirm `docs/spec/c1_nt8_sizing_host_impl.md` records Option C adopted 2026-07-18 (Python reference IS the live host; NinjaScript port not needed). Also report `pytest tests/ops/ -k sizing -q` collection count (expect 29 tests referencing this module's oracle behavior).
- `.claude/settings.json` — report the `permissions.allow` list (anchored lines 7–12 carry: `Bash(python -m portfolio_mc:*)`, `Bash(python portfolio_mc.py:*)`, `Bash(python cli.py status:*)`, `Bash(python cli.py lots:*)`, `Bash(python cli.py add:*)`, `Bash(python cli.py update:*)`). Confirm `ops/cli.py` exposes only the `tearsheet` subparser and `ops/accounts.py` is untracked (substrate Phase 2, ADR `docs/adr/2026-07-22-challenge-era-substrate-retirement.md` §2-D).
- `.claude/skills/prop-firm-challenge/SKILL.md` — report the "## Current posture (2026-07-11 …)" block in full (it asserts: R6 NO-GO with "CrossTrade/NT8 rail not built, no live automated execution"; "Aegis→M6J is the sole **active** lane"; "`ACTIVE_FIRM` remains `"FXIFY"`"). Each claim is falsified by: c1 GO + B6 dry-fire PASSED (`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`); self-funded CLOSED/parked (`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`); `ACTIVE_FIRM = "Tradeify_Select_100K"` (substrate Phase 1). Also report the later line referencing "`ops/accounts.py`'s multiplier system" if present.
- `.claude/skills/handoff-verify/SKILL.md:72` — report the "Live posture:" checklist line ("FXIFY closed, futures-prop R6 NO-GO, self-funded Aegis→M6J sole active lane…").
- `.claude/skills/brief-authoring/SKILL.md` — report description line 3 (contains "or the Notion Command Center") and the artifact-destination table rows ~90–96 (lock briefs routed "Notion Command Center + `docs/briefs/locks/`"). Notion surface retired as canonical 2026-06-12 (`docs/adr/2026-06-12-notion-surface-retirement.md`).
- `.claude/skills/pinescript-v6/SKILL.md` — report description line 3 clause "Also trigger for FXIFY strategy work (Guardian Gold, Striker USTec)".
- `CLAUDE.md` §Live-execution posture — read in full; it is the posture source the frozen texts below transcribe. Do not re-derive posture from any other doc.

---

## §0.5 — Clarifying questions (Cursor variant — parent-recommended defaults)

- **(A) settings.json rules NOT in scope.** **Recommended default:** remove ONLY the six rules quoted in §2.2. Keep `Bash(python dd_protection.py:*)` (live MVD self-check), `Bash(python scripts/verify_lock_anchors.py:*)`, both `notion-*` MCP allows (operator personal use — a separate open QUESTION owned by the umbrella note), and everything else untouched.
- **(B) prop-firm-challenge body edits beyond the posture block.** **Recommended default:** replace the posture block + repair the dead `ops/accounts.py` sentence per §2.3; leave all other body sections (firm rules mechanics, MC, dd_protection) untouched even if wording feels dated — deeper rescope is a CC authoring task, not this handoff.
- **(C) Skill `description:` frontmatter edits** change routing for deployed bundles. **Recommended default:** apply exactly the frozen description edits (§2.3, §2.5); no other frontmatter fields.

---

## §1 — Context

The Algorithm review (2026-07-24) found the live-ops routing layer frozen at the 2026-07-11 posture: skills assert facts falsified by the c1 GO (07-17), the self-funded close (07-16), and substrate Phases 1–2 (07-22/24) — and the most safety-critical live-rail file carries a docstring saying it is not the live host when it is. A skill that misdirects an agent is negative-value; this handoff lands the mechanical text repairs. (The separate R1 coverage gap — no skill covers the c1 rail at all — is a CC authoring task recorded in the umbrella note, NOT this handoff.)

**Deliverable:** one `cursor/*` PR touching exactly the six files in §2.
**NOT asked:** authoring a c1-rail skill, editing the deployed AppData bundle, touching CLAUDE.md/STATE.md, any logic change.

---

## §2 — Execution plan

### Step 2.1 — `ops/c1_rail/c1_sizing_host_reference.py` docstring correction

- **Action:** replace the paragraph "This module is NOT the live host — the live host is a NinjaScript component (Cursor-implemented) whose outputs must match this reference at the B6 dry-fire gate. It exists so the sizing law is proven against the committed F2 oracle (lab/analysis/c1/q_rail_1_2026-07/f2_floors.json) before it is embedded in C# that repo CI cannot compile." with this FROZEN text:

  > This module IS the live sizing host (Option C, adopted 2026-07-18 — see
  > docs/spec/c1_nt8_sizing_host_impl.md): ops/c1_rail/c1_rail_listener.py runs
  > C1SizingHostReference directly on the TV->CrossTrade->Tradovate rail; the
  > NinjaScript port is a dormant fallback and was never built. The sizing law
  > remains proven against the committed F2 oracle
  > (lab/analysis/c1/q_rail_1_2026-07/f2_floors.json), which the B6 dry-fire gate
  > (PASSED 2026-07-20) matched exactly.

- **Per-step gate:** `git diff` on this file shows docstring lines only; `pytest tests/ops/ -q` green with identical test count.

### Step 2.2 — `.claude/settings.json` dead-allow prune

- **Action:** delete exactly these six rules: `Bash(python -m portfolio_mc:*)`, `Bash(python portfolio_mc.py:*)`, `Bash(python cli.py status:*)`, `Bash(python cli.py lots:*)`, `Bash(python cli.py add:*)`, `Bash(python cli.py update:*)`.
- **Per-step gate:** JSON parses (`python -c "import json;json.load(open('.claude/settings.json'))"`); no other rule added/removed.

### Step 2.3 — `prop-firm-challenge/SKILL.md` posture refresh

- **Action:** (a) retitle the posture block "## Current posture (2026-07-24 — verify against CLAUDE.md; trust ADRs over this paragraph)" and replace its body with this FROZEN text:

  > **One live rail, disarmed.** The c1 rail (TV -> listener -> CrossTrade ->
  > Tradovate; Option C) is BUILT on one Tradeify Select 100K eval —
  > `ACTIVE_FIRM = "Tradeify_Select_100K"` (substrate Phase 1, 2026-07-22).
  > B6 dry-fire PASSED 2026-07-20; currently disarmed (`dry_run=true`); the
  > next armed send is gated on M1 monitoring RESOLVED + operator B7 GO
  > (`docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`,
  > `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`).
  > **Self-funded scale CLOSED/parked** (Aegis->M6J + Guardian-MGC,
  > `docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`);
  > manual trading + CFD venue retired; FXIFY closed 2026-07-10. Historical
  > MC / challenge semantics pin `FIRM_RULES["FXIFY"]` **by name**, never via
  > `ACTIVE_FIRM` (`docs/adr/2026-07-22-challenge-era-substrate-retirement.md`).
  > The continuous-lot multiplier spine (`ops/accounts.py` + account CLI) is
  > DELETED (substrate Phase 2); live sizing is
  > `BASE_RISK x DD_SCALE x lifecycle` with integer-qty flooring in
  > `ops/c1_rail/c1_sizing_host_reference.py`.
  > **Venue facts corrected 2026-07-22 (read the ADR, do not re-derive):** the
  > eval rows had modeled a drawdown lock neither Tradeify nor MFFU applies in
  > eval; corrected, both `trailing_locking` tiers flip Part A PASS->FAIL, so the
  > prop-portfolio **section-4 falsifier is UNDISCHARGED** (hard date 2026-11-08)
  > and the c1 GO's WATCH-1 0.50x risk figures are **unmeasured under corrected
  > geometry** (open B7 input). Also: the contract cap is account-aggregate and
  > now allocated per leg (MYM 69 / MNQ 11), flat deadline 16:45 ET, US
  > Treasuries untradable at this firm, hedging rule cleared by construction
  > (long-only) --
  > `docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` +
  > `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` Addendum
  > 2026-07-22.

  (b) repair any remaining sentence claiming `ops/accounts.py` / the multiplier system funnels sizing — point it at `ops/c1_rail/c1_sizing_host_reference.py` instead. (c) In the frontmatter description, replace "or account-multiplier tooling" with "or c1 rail sizing questions".
- **Per-step gate:** `grep -n "accounts.py\|sole active lane\|remains \"FXIFY\"\|rail not built" .claude/skills/prop-firm-challenge/SKILL.md` returns zero hits.

### Step 2.4 — `handoff-verify/SKILL.md:72` posture-anchor refresh

- **Action:** replace the "Live posture:" line with this FROZEN text:

  > - Live posture: FXIFY closed; self-funded lanes PARKED; prop-portfolio program at the four AUTOMATION_FRIENDLY firms; sole live rail = c1 (TV->CrossTrade->Tradovate, Tradeify Select 100K, **disarmed**, B7 gated on M1 RESOLVED) — see `CLAUDE.md` Live-execution posture. Handoffs that assume an open FXIFY challenge, an Aegis->M6J active lane, or an unbuilt CrossTrade rail are stale.

- **Per-step gate:** `grep -n "sole active lane" .claude/skills/handoff-verify/SKILL.md` → zero hits.

### Step 2.5 — `brief-authoring/SKILL.md` + `pinescript-v6/SKILL.md` retired-surface references

- **Action:** brief-authoring — in description line 3 delete "or the Notion Command Center" (keep `docs/adr/`, `docs/briefs/`); in the destination table replace "Notion Command Center + `docs/briefs/locks/`" with "`docs/briefs/locks/` (Notion surface retired 2026-06-12)" and replace the Notice-log row's "or Notion" with "(`docs/notes/notice/`)". pinescript-v6 — replace "Also trigger for FXIFY strategy work (Guardian Gold, Striker USTec)" with "Also trigger for locked-book strategy work (Guardian Gold, Striker DJ30/NAS100 and their MYM/MNQ venue editions)".
- **Per-step gate:** `grep -rn "Notion Command Center" .claude/skills/brief-authoring/SKILL.md` → hits only in historical/anchor prose outside the description + destination table (report remaining hits); `grep -n "USTec" .claude/skills/pinescript-v6/SKILL.md` → zero.

### Step 2.6 — Closure

Report per §6; PR body lists every replaced string old→new.

---

## §4 — Falsifiable hypothesis

**H (premise, not an investigation):** every §0-anchored staleness claim still holds at dispatch time. **Falsified if** any Phase-0 read contradicts its anchor — the premise, not the plan, has failed; bounce `NEEDS_CONTEXT` with the discrepancy quoted.

---

## §5 — Forbidden moves

- **Rescoping skill bodies beyond the frozen edits** (tempting — much surrounding prose is dated). Log observations as §6 concerns; deeper rescope is CC-owned authoring.
- **Editing the deployed AppData bundle or running `scripts/sync_skills.py` from a worktree.** Post-merge sync is operator-local from the primary checkout (§7); worktree-sourced sync is a known corruption path.
- **Touching CLAUDE.md/STATE.md** to "align" them — owned by operator directive 2026-07-23 #4 (separate session).
- **Removing the two `notion-*` MCP allows** while pruning settings.json — open operator QUESTION, not this handoff.
- **Any edit to `ops/c1_rail/c1_sizing_host_reference.py` outside the docstring.**

---

## §6 — Gate + status return

Report EXACTLY one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>` per `references/cc_handoff.md` §6, with the standard closure-report format (status, per-step gates, diff list, concerns, next action). This handoff produces no investigation verdict (no RESOLVED / FALSIFIED / AMBIGUOUS claim) — the four-state return plus the per-step gates is the entire closure.

---

## §7 — Parent-session review (after return)

Pass 1: diff = exactly the six §2 files. Pass 2: every frozen string applied byte-verbatim; grep gates green; sizing tests count-identical. Pass 3 (multi-step): read the four SKILL.md diffs together — posture statements must now agree with each other and with CLAUDE.md. **Post-merge operator step (NOT Cursor):** from the primary checkout run `python scripts/sync_skills.py` to refresh the deployed bundle, and delete the retired extras the sync never prunes (`fxify-challenge`, `live-execution-journal` in the AppData bundle — evidenced still-served on 2026-07-24).

---

## §10 — Audit hooks (runnable)

```bash
grep -rn "rail not built\|sole active lane\|remains \"FXIFY\"" .claude/skills/   # expect: zero hits
grep -n "cli.py status\|cli.py lots\|portfolio_mc" .claude/settings.json          # expect: zero hits
grep -n "NOT the live host" ops/c1_rail/c1_sizing_host_reference.py                       # expect: zero hits
git diff origin/main..HEAD --name-only                                            # expect: exactly the six §2 files
```

---

## Verification (parent-side)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-24-cursor-handoff-agent-surface-posture-sync.md
python scripts/check_skill_refs.py --all
```
