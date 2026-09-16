# ADR — Worker-surface allocation: the coordinator designs and adjudicates, workers implement frozen specs

**Status:** Accepted (ratified 2026-07-14)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise — converted from the original full format by the 2026-09-15 revision, which consolidated §0–§10 and six addenda into Decision / Grounds / Current owner plus the §8 disposition table. Prior full-format text at the blob pinned below.
**Decision date:** 2026-07-14
**Revision:** 2026-09-15 — **RATIFIED** by the operator in-session ("execute my decisions").
Retires Cursor as a worker surface and rescopes this decision to the surviving surfaces
(Claude Code, Codex); consolidates the six 2026-07-16 → 2026-09-04 addenda into the §8
disposition table. This revised text is the effective decision. Prior decision text, in full
and unedited, at blob `0bcd6699fd683a18b9493e25bb053797dcf4fafe`
(`git show 0bcd6699fd683a18b9493e25bb053797dcf4fafe`), commit
`b448e2b6f852a49c2a46e278ade95a4c4e2c4c54`.
**Supersedes:** `2026-08-14-cc-cursor-autonomous-loop.md` full — its entire subject (Cursor
dispatch without chip approval, `cursor/*` webhook detection, and auto-merge on a binary gate)
retires with the Cursor lane; the surviving general rule is restated in §2 below.
**Authors:** Joshua + Claude Code (2026-07-14); revision Joshua + Claude Code (2026-09-15)
**Related:** [`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md) (consumer-side gate) ·
[`task-routing`](../../.claude/skills/task-routing/SKILL.md) (canonical local-vs-cloud checklist) ·
[`cc_handoff` template](../../.claude/skills/brief-authoring/references/cc_handoff.md) (producer-side contract)
**Layer:** infrastructure

> ⚠ **REVISED 2026-09-15 — Cursor is retired as a worker surface.** The body below is the
> rescoped decision, not the 2026-07-14 text, and is **operator-ratified and effective**. The
> clause-by-clause record of what survived, what was restated and what retired is §8. The
> pre-revision text is pinned at the blob in the header.

---

<a id="2--decision"></a>

## Decision

Work is routed between **surfaces** by a four-question test, with an authored handoff brief as
the mechanical eligibility gate. The **coordinator** designs, specifies and adjudicates;
**workers** implement frozen specs and never merge.

**Surfaces, as of the 2026-09-15 revision:** the coordinator is a Claude Code session. Workers
are Claude Code sessions and Codex. **Cursor is retired** — no Cursor lane, no `@cursor`
dispatch, no dispatch-chip approvals, no `cursor/*` branches, no `cursor[bot]` allow-listing.
New worker branches use `codex/` or `claude/`. This is an operator scope election (in-session,
2026-09-15: *"cursor is being retired altogether, we will no longer be incorporating cursor
agents. it will be just claude and codex"*), already ruled for one campaign as
[D-B6](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) on 2026-09-11
and applied repo-wide here. It carries no falsifier and no review cadence: there is no
measurement that would reinstate a surface the operator has removed from spend.

**Routing test (apply in order).** The tests are about the *work* and the *environment*, not
about which vendor runs the session, so all four survive the retirement unchanged:

0. **Does Phase-0 reading require bytes or credentials not verifiably present in the dispatch
   environment?** Specifically (a) any path under `core/data/tv_exports/**`,
   `core/data/bar_data/**`, `core/data/external/**` (gitignored vendor data), or (b) any API
   key or secret. If yes and unconfirmed-present in the target environment → **local**, full
   stop, regardless of how 1–3 resolve. This binds every remaining surface: Claude Code and
   Codex each have local and cloud modes, and a cloud checkout structurally lacks gitignored
   bytes unless staged for *that* dispatch. Canonical checklist owner:
   [`task-routing`](../../.claude/skills/task-routing/SKILL.md).
1. **Does the task author doctrine or touch a locked/governed surface?** (ADRs, Pre-Qs,
   pre-registrations, closures, lifecycle state, `CLAUDE.md`/`STATE.md`/memory; any *edit* to
   `core/` anchor-path code — `dd_protection.py`, `firm_rules.py`, `portfolio_mc.py`,
   `core/mc/*`, `lifecycle.py`, `dd_geometry.py` — or Pine.) → **coordinator**, full stop.
   Read-only imports of `core/` from `lab/` code are fine on any surface.
2. **Is the spec frozen?** Binary acceptance gates, resolved ambiguities, enumerated forbidden
   moves, no judgment calls expected mid-build. If not → the coordinator either does the work
   or freezes the spec first. A worker never resolves a spec ambiguity unilaterally; it bounces
   `NEEDS_CONTEXT`.
3. **Does the build clear the handoff-overhead threshold?** If the build is smaller than the
   brief (rule of thumb: < ~1 focused hour, or fewer than ~3 files touched), it stays on
   whichever surface is already open. Above threshold and spec-frozen → dispatch to a worker.

**Handoff contract (all five required for worker eligibility):**

- A handoff brief under `docs/briefs/**` passing `check_brief.py`.
- §0 Phase-0 reads with a **read-report-before-code** requirement and a `NEEDS_CONTEXT` bounce
  on any contradiction; the worker runs the [`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md)
  checklist as that Phase 0.
- §5 forbidden moves naming the locked surfaces the task runs near.
- §0 states explicitly whether any read touches a gitignored vendor-data path or a secret
  (test 0), and if so names the confirmed-present staging/credential check performed for *this*
  dispatch — not a prior one, not a general belief the bytes or key exist "somewhere."
- **Return contract:** a worker branch (`codex/*` or `claude/*`), a PR with tests green, and a
  four-state status — `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`. **No commit
  or merge without the operator.** `DONE_WITH_CONCERNS` is adjudicated by the coordinator before
  merge; `NEEDS_CONTEXT` gets one re-anchor and re-dispatch, then falls back to the coordinator
  (two bounces means the spec was not freezable and the packet was mis-routed).

**Merge authority is the operator's, with no automated exception.** The 2026-08-14 binary
auto-merge gate is retired with the mechanism it drove (§8). Neither a green CI run, nor a clean
automated review, nor an adjudication verdict is merge authority.

**Orchestrating more than one worker at a time.** When work decomposes into 2+ independent
spec-freezable packets, the coordinator owns the claim manifest and every packet still clears
tests 0–3 individually. Three rules carried enough dated failure evidence to survive the
retirement of the skill that stated them:

- **Disjoint file footprints.** No two packets touch the same file. `docs/SESSIONS.md`,
  `STATE.md`, campaign-state files, and all board/index files are **reserved to the
  coordinator's integration commit** — the single-writer rule. Workers never write them.
- **Dispatch-moment Phase-0 re-check, not authoring-moment.** Re-verify each packet's premises
  against current `origin/main` at dispatch, with an explicit no-op condition ("if already fixed
  on main → return DONE, cite the commit"). Three artifacts were overtaken between authoring and
  dispatch on 2026-07-24 alone.
- **A brief's review round is part of the freeze, not a track running alongside the builds.** The
  umbrella brief's pre-dispatch review must have COMPLETED and any re-freeze it produced must be
  merged to `main` **before the first packet is dispatched**. Dispatching from the brief as first
  opened is a forbidden move.
- **The dispatch pointer carries the brief's frozen SHA** — the post-review-round freeze, never
  the as-first-opened commit. A worker whose pointer SHA no longer matches the brief on `main`
  returns `NEEDS_CONTEXT` rather than building: a stale pointer is a stale spec, and building it
  anyway is how a withdrawn packet gets built.

  Both rules are paid for by SESSIONS `2026-09-04f`: all three workers were fired from `af0203f`
  while the review was still running; the re-freeze withdrew packet B (built anyway, #304 closed
  without merge) and moved packet C's guard mid-build (C falsified, fix round C1 owed). Relay lag,
  not worker error — the workers had no SHA to notice the drift by. Ratified as
  [#402](https://github.com/Joshua-Asante/first-passage/pull/402) against the `cursor-fleet`
  skill on 2026-09-15 and carried here verbatim in substance when that skill was deleted the same
  day; nothing of #402 is lost.

**Effective:** the 2026-07-14 decision on acceptance; the 2026-09-15 rescoping on the
operator's same-day in-session ratification.
**Scope:** task routing between the coordinator and worker surfaces on this repo. Other external
surfaces (web advisors, claude.ai) keep their existing gates; this ADR does not re-govern them.

## Grounds

**For the original allocation (2026-07-14, unchanged in substance).** Since 2026-07-06 the repo
ran a two-surface workflow without a written rule, producing four clean lands in eight days and
zero locked-surface incidents. The counter-pattern is also documented: external instruction
packets confabulate repo state when not gated
(`feedback_web_advisor_handoff_confabulates_repo_state`, multi-fire through 2026-07-11), which is
why `handoff-verify` exists. Unwritten, the allocation would drift under speed pressure until a
judgment-heavy or locked-surface task crossed a line. Routing by "code vs docs" was rejected as
the wrong axis in both directions: a mechanical `SESSIONS.md` entry was successfully handed off,
while `dd_geometry.py` — code — was correctly kept in-session because it sits on a governed
surface. Spec-completeness and surface-proximity predict outcomes; artifact type does not. A
vendor-supplied CC-vs-Cursor performance comparison offered at the time was treated as
unverified marketing material and is explicitly non-load-bearing: the decision would stand
unchanged if every vendor claim were false.

**For the 2026-09-15 retirement.** The operator removed Cursor from recurring spend on
2026-09-10 ([`d16`](../pursuits/d16-cursor-subscription.md), `SUBTRACT`;
[subscription ledger](../pursuits/SUBSCRIPTION_LEDGER.md)), and on 2026-09-11 ruled for Track B
that "Cursor is not a lane… packets marked Cursor-eligible go to Codex local"
([D-B6](../briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md)). The
2026-09-15 instruction generalises that to the repo. A surface with no subscription cannot be
dispatched to, so leaving the lane documented as live would leave the routing test describing a
destination that does not exist — the drift this ADR was written to prevent, pointing the other
way.

**Why this is a revision and not a new ADR.** The subject of this record *is* surface
allocation; retiring one of the two surfaces is a change of scope to this decision, not a
different decision. [ADR ceremony tiering](2026-08-08-adr-ceremony-tiering.md) (revised
2026-09-08) provides exactly this mechanism — "approved changes update effective decision text
with a dated revision and immutable prior version" — and explicitly retired the rule requiring
"new sibling ADRs for every amendment." A third file on this subject would have continued the
corpus growth that policy revision exists to stop, and would have created a second owner for
rules Rule 7 assigns to one.

## Current owner

- **This ADR** owns the routing test, the handoff contract, the return contract and merge
  authority.
- [`task-routing`](../../.claude/skills/task-routing/SKILL.md) owns the canonical local-only
  (test 0) checklist. One owner: this ADR states the test, that skill holds the list.
- [`cc_handoff.md`](../../.claude/skills/brief-authoring/references/cc_handoff.md) owns the
  producer-side brief template, including the §0.75 local-only dependency block and the
  recommended-defaults pattern for resolving ambiguity ahead of a frozen-spec dispatch.
- [`handoff-verify`](../../.claude/skills/handoff-verify/SKILL.md) owns the consumer-side
  Phase-0 gate.
- [`TOMBSTONES.md`](TOMBSTONES.md#2026-09-15-cursor-agent-retirement) owns retrieval of the
  artifacts removed by the retirement sweep.
- `docs/SESSIONS.md` and the programme audits own the dated failure evidence behind the
  orchestration rules; this ADR states the rules, not the incident log.

## §8 — Disposition of the prior decision's clauses and addenda

> **Two HTML anchors in this file are load-bearing and must not be removed:**
> `#2--decision` (the slug of the pre-revision `## §2 — Decision` heading) and
> `#addendum-2026-09-04-disable-notify-cursor`. The 2026-09-15 revision dropped both
> headings and broke two live incoming links — `docs/SESSIONS.md:424` and the Track B
> [campaign state](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md).
> The SESSIONS citation sits in a merged entry that `sessions-append-only` forbids
> editing, so the anchor is pinned here rather than the caller repointed.

Every clause of the 2026-07-14 body and its six addenda, dispositioned per
[ceremony tiering](2026-08-08-adr-ceremony-tiering.md) ("disposition each obligation as retained,
discharged, superseded or explicitly retired"). Full prior text at blob
`0bcd6699fd683a18b9493e25bb053797dcf4fafe`.

| Prior clause | Disposition |
|---|---|
| §2 routing test 0 (local-only dependency pre-check, 2026-07-16 addendum) | **Retained**, surface-agnostic. Binds Claude Code and Codex equally; checklist owner is `task-routing`. |
| §2 routing test 1 (locked/governed surface → coordinator) | **Retained** verbatim in substance. No surface exception, no size exception. |
| §2 routing test 2 (spec frozen; never resolve ambiguity unilaterally) | **Retained**, "Cursor" → "a worker". |
| §2 routing test 3 (handoff-overhead threshold) | **Retained**. Its 2026-08-29 reading as *proactive dispatch authority* (act, don't merely label) is also retained. |
| §2 handoff contract, items 1–3 and 5 (brief passing `check_brief`; §0 read-report + `NEEDS_CONTEXT`; §5 forbidden moves; vendor-bytes/secret declaration) | **Retained** unchanged. |
| §2 return contract, "no commit/merge without operator go" | **Retained, and restored to its unnarrowed form** — the 2026-08-14 narrowing retires with its mechanism. |
| §2 return contract, `cursor/*` branch | **Superseded** — worker branches are `codex/*` or `claude/*`. |
| Four-state return taxonomy (`DONE`/`DONE_WITH_CONCERNS`/`NEEDS_CONTEXT`/`BLOCKED`) | **Retained** and promoted into §Decision; it was previously stated only by the deleted `cursor-fleet` skill. |
| §4 falsifier limb 1 (≥2 judgment-defect PRs in 8 weeks) | **Retained**, re-scoped to worker PRs on any surviving surface. |
| §4 falsifier limb 2 (overhead exceeds value, ≥3 consecutive handoffs) | **Retained**, surface-agnostic. |
| §5 forbidden move — verbal-spec handoffs | **Retained**. The containment is the brief, whatever the worker. |
| §5 forbidden move — scope-creep via adjacency | **Retained**. |
| §5 forbidden move — merging on green tests without review | **Retained**, unnarrowed (see above). |
| §5 forbidden move — retro-fitting a brief after the build | **Retained**. |
| §5 forbidden move — quoting the vendor comparison's numbers in routing arguments | **Explicitly retired** — the comparison was Cursor-vs-CC and has no remaining referent. Its *principle* (don't ground routing doctrine in vendor marketing) is generic and survives under `verify-source`. |
| §6 downstream artifacts; §7 implementation plan (Phases 0–3) | **Discharged** 2026-07-14/16. Completed maintenance acts; no standing obligation. |
| §10 audit hooks (cursor-branch merge/locked-surface sweeps) | **Superseded** by §10 below — the old hooks scan a branch namespace that no longer exists. |
| Addendum 2026-07-16 (Step 0 + 5th contract item) | **Folded into §Decision above**; binding, not an appendix. |
| Addendum 2026-08-14 (auto-merge narrowing) | **Explicitly retired** with its parent mechanism. See the `2026-08-14` ADR's own retirement. |
| Addendum 2026-08-23 (automatic Claude judgment review) | **Already self-superseded 2026-08-29** — the mechanism never fired (`GITHUB_TOKEN`-authored comments do not trigger workflow runs) and its files were deleted then. No live obligation. |
| Addendum 2026-08-29 #1 (Codex native GitHub review) | **Retained and now load-bearing** — Codex's account-level review is a surviving surface's review path. Its standing bar — *this repo's CI grants Codex no write/push credential without a superseding ADR* — **survives the Cursor retirement unchanged**; nothing here relaxes it. |
| Addendum 2026-08-29 #1 — **its revert trigger**: a rolling 8-week window in which Codex's native review is demonstrably lower-signal than Claude's on the same class of PR, or the operator disables the `chatgpt.com/codex/settings/code-review` toggle for this repo (operator-judged, logged in `docs/SESSIONS.md`) | **Retained.** Revert action unchanged and still correct: none in this tree — the mechanism is account-level, so reverting is toggling that setting off, not editing this repo. |
| Addendum 2026-08-29 #2 — **its revert trigger**: two proactively-dispatched tasks in a rolling 8-week window turn out to have needed operator judgment the coordinator lacked (wrong root cause, misjudged scope, a spec that was not actually frozen) | **Retained**, re-scoped to the surviving worker surfaces. Revert action: back to per-task "dispatch this" confirmation before any worker dispatch. |
| Addendum 2026-08-29 #1, "relay findings to Cursor's Cloud Agent" | **Explicitly retired** — the relay target is gone. Findings are addressed by the coordinator or a Codex/Claude Code worker. |
| Addendum 2026-08-29 #2 (proactive dispatch; lightweight GitHub-issue + `@cursor` format) | **Split.** Proactive-dispatch authority is **retained** (above). The lightweight issue format is **retained in shape** — a complete issue body in place of a full brief for small precedented fixes — but its `@cursor` dispatch step is **explicitly retired**; dispatch is to a Codex or Claude Code worker. |
| <a id="addendum-2026-09-04-disable-notify-cursor"></a>Addendum 2026-09-04 (`notify-cursor.yml` auto-ping disabled) and its revert trigger ("operator asks to turn the ping back on"; restore `on:` events from `4f3ddc6`) | **Explicitly retired, not left standing.** The workflow is deleted by this revision's sweep; the revert trigger is unreachable and is discharged rather than carried as a dead obligation. Retrieval via [`TOMBSTONES.md`](TOMBSTONES.md#2026-09-15-cursor-agent-retirement). |

### Deliberately retained (not over-swept)

Three Cursor-named things survive on purpose; a future reader should not treat them as a
missed sweep:

- **`scripts/check_pine_manifest.py`'s `cursoragent@cursor.com` author denylist.** Dormant —
  that identity can no longer appear — but retained as cheap anti-re-entry armor for the
  incident it encodes (commit `66c2a14`/PR #574: a Pine manifest pin authored from a
  disposable Cursor cloud checkout, bytes lost). The guard costs nothing and still fires if
  the lane is ever restored. `.github/workflows/manifest-check.yml`'s matching comment is
  that incident's record.
- **The `cursor` alternation in both copies of `check_brief.py`'s type-inference regex.**
  Retained as inert tolerance for two frozen historical briefs that self-declare
  `**Brief type:** Cursor handoff`. **Correction (2026-09-15, adversarial review):** an earlier
  draft of this section claimed removing the alternation "would silently reclassify those
  records." That was **false** and is corrected here rather than quietly dropped — `infer_type`
  also matches on filename, and both briefs carry `cursor-handoff` in their names, so removal was
  measured to change zero classifications across all 858 markdown files. The alternation stays
  because it is harmless and costs nothing, not because anything depends on it. The regex reads
  history; it authorizes nothing.
- **`lab/research_utils/msl_preflight.py`'s ripgrep fallback** to a Cursor *editor* install
  path. It is a guarded filesystem probe reached only when `rg` is absent from `PATH`, with no
  agent semantics; removing it could only reduce robustness on a host that still has the editor.

Dated Cursor attributions in instrument ledgers, `lab/CATALOG.md`, `PORT_MANIFEST.sha256`,
`docs/SESSIONS.md`, closures and superseded specs are historical record and are **not** swept —
history stays, per the reader-intercept principle this revision relies on.

## §4 — Falsifier (revert trigger), restated surface-agnostically

Both limbs survive the retirement; only "Cursor" becomes "a worker". Restored here
because the 2026-09-15 consolidation carried their *thresholds* into the §8 table but
dropped their revert **actions** and their check schedule — a falsifier without a
stated consequence is the failure mode this repo has a lesson for.

**Revert trigger (either limb):**

1. **Allocation-caused defects** — over any rolling 8-week window, ≥2 merged
   worker-built PRs carry defects traceable to *spec-interpretation judgment* (the
   worker resolved an ambiguity instead of bouncing `NEEDS_CONTEXT`) rather than to
   spec error.
2. **Overhead exceeds value** — ≥3 consecutive handoffs where authoring and verifying
   the brief demonstrably cost more session time than the gated build
   (operator-judged, logged in `docs/SESSIONS.md`).

**Revert action:** limb 1 → supersede with a tightened rule (narrower worker scope, or
mandatory coordinator re-verification of every worker diff hunk); limb 2 → carve the
affected task class back to the coordinator by superseding ADR — **do not silently stop
writing briefs.**

**Trigger check schedule:** rides the standing quarterly programme review.

## §9 — Operator actions this repo cannot perform

Three Cursor residues sit outside what a file edit can reach, so merging the sweep could not touch
them. Recorded here, in the hot record, so the retirement is not mistaken for complete at the
account level. **Items 1 and 2 verified already gone on 2026-09-15** (same-day follow-up session,
run on the operator's machine and account):

1. **The GitHub webhook trigger** created under the now-superseded autonomous-loop ADR (routine
   `trig_012nvuH7jqmjFUFgoFVpZ6RP`, firing unfiltered on `pull_request: opened`) — an
   account-level routine, not a repo file. **Deleted.** `RemoteTrigger get` on the id returns
   HTTP 404 `Trigger not found` from the same account whose 2026-08-15 session transcript holds
   the routine's API record; `list_runs` shows zero sessions against a `52 */6 * * *` cron that
   would have produced ~4/day; and all 30 `cursor/*` PRs opened after 2026-08-14 were merged by
   the operator or `app/cursor`, never by the routine. The API's `list` returns only the 20
   newest routines and does not page, so the earlier "not in the listing" was uninformative
   either way — the resource-level 404 is the evidence. Nothing to disable. One residual check
   only the operator can make: the routines page at `claude.ai/code/routines`, confirming no
   *other* routine carries a GitHub event source on `first-passage` (a routine object exposes no
   event-source field, so the API cannot answer this).
2. **`daily-repo-truth-sync`**, the operator-machine scheduled task whose step 2 classified
   `cursor/*` branches SPENT / CARRIES-WORK / UNKNOWN. **Deleted.** The desktop scheduler
   reports `taskDeleted: true` (42 runs; last 2026-09-14 00:59Z). Its `SKILL.md` remains under
   `~/.claude/scheduled-tasks/` as the scheduler's documented post-delete residue, not a live
   task. Nothing to prune.
3. **Four spent `cursor/*` refs still on `origin`** — a remote deletion, not a file edit, so the
   sweep could not perform it (and §10 hook 3 read "empty" from an unfetched checkout):
   `cursor/research-asset-registry-0ba4` (#315 merged), `cursor/scripts-side-2026-09-04-p3`
   (#303 merged), `cursor/windows-handoff-job-accounting-7785` (#326 merged) — each an ancestor
   of `main` — and `cursor/scripts-side-2026-09-04-p2` (#304 closed unmerged, "Packet B was
   withdrawn before dispatch"), one commit ahead holding the withdrawn diff, which stays
   reachable from the PR after deletion. Operator: `git push origin --delete <ref>` ×4.

None of this blocks ratification. A fourth item is the operator's alone: the **Cursor row in the
[subscription ledger](../pursuits/SUBSCRIPTION_LEDGER.md)** still records a cancellation date and
final charges as not supplied. That is an operator reconfirmation, not an agent edit.

### In-flight work this revision interacts with (2026-09-15)

Two PRs were open against `main` when this revision landed. Neither is editable from this
branch; both need a pass at merge time:

- **[#402](https://github.com/Joshua-Asante/first-passage/pull/402)** amends
  `.claude/skills/cursor-fleet/SKILL.md`, which this revision **deletes** at operator
  instruction. Whichever lands second conflicts. The deletion is the operator's ruling and
  should win; #402's substance (a brief's review round is part of the freeze, and the dispatch
  pointer carries the frozen SHA) is **already carried** in §Decision's orchestration rules, so
  nothing of it is lost by closing it against the deletion.
- **[#401](https://github.com/Joshua-Asante/first-passage/pull/401)** adds a
  `work-decomposition` skill whose line 19 reads "retired by operator instruction on 2026-09-15
  (**retirement record pending**)". **This revision is that record** — the pointer resolves here
  once both land. #401 also makes pointer edits to `cursor-fleet`, which will need re-homing to
  this ADR for the same reason.

## §10 — Audit hooks (runnable)

```bash
# 1. No Cursor harness, dispatch script or workflow survives in the tree.
git ls-files .cursor scripts/dispatch_cursor.ps1 scripts/test_dispatch_cursor.ps1 \
             .github/workflows/notify-cursor.yml .claude/skills/cursor-fleet
# Expected after ratification: empty.

# 2. No live agent-facing surface still names a Cursor lane, dispatch or branch namespace.
#    Three carriers are deliberately excluded and are the ONLY permitted hits:
#      - comment lines recording why the lane is gone;
#      - scripts/agent_handoff.md's retirement note in prose;
#      - scripts/check_pine_manifest.py's `cursoragent@cursor.com` author denylist, retained as
#        dormant anti-re-entry armor for the PR #574 incident (bytes lost to a Cursor cloud agent).
#    Any OTHER hit is a finding.
rg -n -i "@cursor|cursor/\*|dispatch_cursor|cursor\[bot\]|cursor-agent" .claude scripts .github \
  | grep -vE ':[0-9]+: *#' \
  | grep -v '^scripts/agent_handoff.md:' \
  | grep -v '^scripts/check_pine_manifest.py:'
# Verified empty at authoring (2026-09-15). The workflow half is additionally pinned
# mechanically by tests/test_claude_review_workflows.py::test_no_workflow_dispatches_cursor.
# Historical citations in docs/adr/, docs/SESSIONS.md, docs/notes/ and lab/ARCHIVED.json are
# deliberately out of scope — history is not swept.

# 2b. No LIVE handoff brief still offers the retired surface as a spawn target.
#     Scope widened 2026-09-15 after a Codex review found
#     docs/briefs/handoffs/2026-09-11-track-a-a1b-... at "Status: dispatch now" still reading
#     "Spawn target: Codex (or Cursor)" while hooks 1-2 reported clean: they scan only
#     .claude/ scripts/ .github/, so a dispatchable brief was outside them.
rg -n -i "spawn target.*cursor" docs/briefs docs/superpowers
# Expected, as of 2026-09-15, exactly two hits, both spent and both verified as such:
#   docs/briefs/handoffs/2026-07-24-cursor-handoff-agent-surface-posture-sync.md
#     -- its own banner reads "STATUS 2026-07-24: DISCHARGED - DO NOT DISPATCH";
#   docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-lifecycle-call1-sigma-harness.md
#     -- no DISCHARGED line, but discharged BY DELIVERY: its deliverable exists at
#     lab/discovery/lifecycle_call1/, whose __init__.py:12 cites this brief as its handoff.
# (A third hit, the 2026-07-24 core-dead-code-prune brief, matches only because it says
#  "NOT Cursor-eligible" -- it routes AWAY from the retired surface, which is correct.)
# Any hit on a brief that is still dispatchable is a finding.

# 3. Worker branches use a surviving namespace. Ask the remote: `git branch -a` sees only refs
#    this checkout has fetched, which is how the authoring pass read "empty" while origin held
#    four (the same unfetched-branch trap the #401 search fell into — SESSIONS 2026-09-15a).
git ls-remote --heads origin 'cursor/*'
# Expected: empty once the §9 item-3 refs are deleted. Verified 2026-09-15: exactly the four
# spent refs named in §9 item 3. Any ref not in that list is a finding.

# 4. The retirement did not silently drop the surviving clauses' owners.
test -f .claude/skills/task-routing/SKILL.md \
  && test -f .claude/skills/brief-authoring/references/cc_handoff.md \
  && test -f .claude/skills/handoff-verify/SKILL.md && echo "owners present"
python scripts/check_skill_refs.py --all
# Expected: "owners present" and a clean skill-refs pass.

# 5. Falsifier limb-1 evidence sweep (at each quarterly check).
grep -in "worker\|packet" docs/SESSIONS.md | grep -in "defect\|redesign\|NEEDS_CONTEXT"
# Adjudicate hits against the two §4 limbs; log the verdict in the review entry.
```

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-07-14-cc-cursor-surface-allocation.md --type adr
python scripts/check_adr_graph.py
python scripts/check_skill_refs.py --all
git show 0bcd6699fd683a18b9493e25bb053797dcf4fafe   # prior decision text, unedited
```

Mechanical form checks do not establish semantic equivalence or ratification.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-14 | Initial authoring | Joshua + Claude Code |
| 2026-07-14 | Ratified — status `Proposed` → `Accepted`; §6 downstream sweep executed | Joshua |
| 2026-07-16 | Addendum RATIFIED — routing-test Step 0 + handoff-contract 5th item | Joshua |
| 2026-08-14 | Addendum RATIFIED — auto-merge narrowing (sibling ADR) | Joshua |
| 2026-08-23 | Addendum RATIFIED — automatic Claude judgment review (review-only) | Joshua |
| 2026-08-29 | Addendum RATIFIED — Codex second look via its native GitHub integration | Joshua |
| 2026-08-29 | Second addendum RATIFIED — proactive dispatch; lightweight issue format | Joshua |
| 2026-09-04 | Addendum RATIFIED — `notify-cursor.yml` auto-ping disabled | Joshua |
| 2026-09-15 | **Revision RATIFIED** — Cursor retired as a worker surface; decision rescoped to Claude Code + Codex; six addenda consolidated into the §8 disposition table; `2026-08-14-cc-cursor-autonomous-loop.md` superseded in full. Prior text at blob `0bcd6699fd683a18b9493e25bb053797dcf4fafe`. §4 falsifier restated; two 2026-08-29 revert triggers restored and one false retention claim corrected after adversarial review. | Joshua (in-session ratification) + Claude Code |
