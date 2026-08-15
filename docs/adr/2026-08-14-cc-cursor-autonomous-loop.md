# ADR — CC/Cursor autonomous loop: dispatch without approval, merge without operator go under a binary gate

**Status:** Accepted (ratified 2026-08-14) — **effective upon webhook creation** (§7 Phase 1, separately confirmed)
**Superseded-by:** none
**Superseded-in-part-by:** none
**Supersedes:** `2026-07-14-cc-cursor-surface-allocation.md` in part — its §2 "no commit/merge without operator go" return-contract line and §5 forbidden move "Merging on green tests without CC/operator review" are narrowed to: *without operator go, unless the binary auto-merge gate in §2 below clears.* Everything else in that ADR — the routing test, the handoff contract, locked-surface exclusions — stands unchanged.
**Retain-until:** none — standing law; falsifier rides the same 2026-11-08 cadence as the parent ADR
**Decision date:** 2026-08-14
**Authors:** Joshua (direction + ruling) + Claude Code
**Related:** [`2026-07-14-cc-cursor-surface-allocation.md`](2026-07-14-cc-cursor-surface-allocation.md) (parent, routing test unchanged) · `.claude/skills/fable-judge/SKILL.md` (adjudication instrument) · `scripts/dispatch_cursor.ps1` (dispatch mechanism, unchanged) · `C:\Users\joshu\.claude\scheduled-tasks\daily-repo-truth-sync\SKILL.md` (existing GitHub-state-check precedent)
**Layer:** infrastructure

---

## §0 — Rule 0 reads (production-source verification, 2026-08-14)

- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` — read in full this session. §2 routing test, handoff contract, §5 forbidden moves, §4 falsifier all verified current (no edits since its 2026-07-16 addendum).
- `scripts/dispatch_cursor.ps1` — read in full this session. Confirmed: dispatch is already a single vetted command (built so the operator allow-lists one script instead of the raw `cursor-agent` binary); the script's own printed output states "the agent does NOT commit/push/PR; that stays operator/CC-gated" — the thing this ADR changes, not the thing that was blocking dispatch.
- `C:\Users\joshu\.claude\scheduled-tasks\daily-repo-truth-sync\SKILL.md` — read in full this session. Confirmed live precedent: a daily report-only task already fetches `origin/main`, lists open PRs (`gh pr list --state open`), classifies `cursor/*` branches SPENT / CARRIES-WORK / UNKNOWN, and flags dispatch-queue staleness — deliberately never acts on findings ("report-only... never act on findings").
- `mcp__scheduled-tasks__list_scheduled_tasks` + `CronList` — queried live this session. No existing GitHub-webhook-driven trigger exists; the closest analog is the daily poll above.
- `RemoteTrigger` tool schema — loaded this session. `create_webhook_trigger` attaches a GitHub event source (repo-scoped, filtered) to a routine; this is the mechanism named in §7.
- Same-session grounding: the F-2 ADR-corpus audit (`docs/notes/audits/programme-audit/2026-08-14-f2-adr-corpus-disposition.md`) and the requirements-backlog verification (`docs/notes/audits/2026-08-14-requirements-backlog-ratification.md`), both this session, are the evidentiary basis for trusting fable-judge-plus-gates as a real check rather than ceremony — both surfaced concrete defects a single pass would have missed, which is exactly what §2's gate is designed to still catch even without a human in the loop.

---

## §1 — Context

The 2026-07-14 ADR ratified CC-designs/Cursor-implements with an explicit operator-go requirement before merge. That requirement has held without incident. Tonight, working through an unrelated requirements-pruning session, the operator raised a direct question: coordination between CC and Cursor still runs through the operator as a manual relay (approve a dispatch chip, notice when Cursor is done, approve the merge), and that relay just failed silently — five dispatched chips were auto-dismissed before ever reaching the operator's UI, discovered only because the operator asked why they'd only seen two of the seven chips claimed.

The operator's stated goal: remove themselves from the loop as much as possible, having explicitly weighed and overruled the caution that manual review just caught two real problems this session (the 0-of-4 adversarial-rescue result on ADR deletions, and the chip-visibility failure itself). Asked specifically whether merge-to-main should also automate or stay manual once dispatch and detection are automated, the operator chose: automate it too, gated on a clean `fable-judge` verdict.

**Decision driver (one sentence):** the operator has explicitly chosen speed over a human glance at each step, provided the substitute check is real — this ADR specifies exactly how real that check has to be.

---

## §2 — Decision

**Decision:** Three steps of the CC↔Cursor loop move from operator-gated to automatic. The 2026-07-14 routing test (which tasks are Cursor-eligible at all) is unchanged and remains the upstream filter.

1. **Dispatch — no chip approval required.** For any task that clears the existing 2026-07-14 routing test (questions 0–3: not doctrine/locked-surface, spec frozen, clears the overhead threshold) and has a compliant handoff brief, CC invokes `scripts/dispatch_cursor.ps1` directly. Chips remain available for tasks the operator wants visibility into regardless of eligibility, or where CC itself is uncertain of eligibility — chips are now the exception-handling path, not the default gate.

2. **Detection — event-driven, not manual.** A GitHub webhook (via `RemoteTrigger create_webhook_trigger`, §7) fires a routine on `cursor/*` branch PR-ready events (PR opened or synchronized, with checks green). No scheduled poll is the primary signal (though `daily-repo-truth-sync` keeps running as a fallback report — see §6 risk).

3. **Merge — automatic, iff the binary gate below clears in full. Any single failure routes to manual review exactly as today: report, do not merge, do not retry silently.**

**The auto-merge gate (all required, mechanically checked, no partial credit):**

| # | Condition | Check |
|---|---|---|
| a | `fable-judge` verdict is exactly `VERIFIED` | Not `VERIFIED WITH CAVEATS`, not `REFUTED` — a caveat is a human-review signal by design |
| b | Full gate battery green | `python scripts/gate_manifest.py --tier pre-commit` exits 0 |
| c | Full test suite green | `pytest tests/` exits 0 — the gate battery alone is explicitly insufficient per this repo's own retention-test discipline (`docs/operational_rules.md` Rule 16: "the pre-commit gate battery does not run tests and is not sufficient evidence of safety") |
| d | Diff touches zero paths in the **auto-merge-forbidden surface list** (below) | Mechanical path-prefix check against the PR's changed-files list |
| e | A compliant handoff brief exists for the dispatched task, unchanged from the 2026-07-14 contract | `check_brief.py --type cc_handoff` |

**Auto-merge-forbidden surface list (deliberately wider than the 2026-07-14 routing test's Cursor-eligibility list — see below for why):**

```
core/dd_protection.py, core/firm_rules.py, core/portfolio_mc.py, core/mc/**,
core/lifecycle.py, core/dd_geometry.py, **/*.pine,
ops/c1_rail/**, ops/instruments/**, docs/notes/rail_build/**,
scripts/validate_c1_monitoring_acceptance.py, docs/adr/**, docs/spec/**,
docs/operational_rules.md, CLAUDE.md
```

**Why this list is wider than the parent ADR's routing-test list, stated explicitly (not a silent assumption):** the 2026-07-14 routing test governs whether a task is *eligible for Cursor at all* — its locked-surface list (six `core/` files + Pine) is scoped to that narrower question. This is a different question: given a Cursor PR already exists, is it safe to merge *without a human looking at it*? Those are not the same bar. `ops/c1_rail/` and the M1 acceptance path are not in the parent's Cursor-eligibility list at all — meaning, read literally, a Cursor PR touching the live-execution rail was never explicitly barred from *being built*, only from touching six named `core/` files. Tonight's session found and fixed a stale safety claim in exactly this area (CLAUDE.md's M1-interlock warning, dead since 2026-08-09 but still read as current risk). Auto-merge is the step this ADR controls, and it does not inherit that gap: anything under the rail, instrument ledgers, or governance-doc surfaces requires a human regardless of verdict cleanliness. `docs/adr/**` and `docs/spec/**` are barred from auto-merge for a structural reason, not a safety one: Cursor does not author doctrine under the parent ADR, so a Cursor PR touching those paths is itself a routing-test violation and should never reach this gate in the first place — the check is a backstop, not the primary control.

**Effective:** upon webhook creation (§7 Phase 1) — not upon ADR acceptance alone. The decision is ratified now; the live mechanism is a separate, explicitly confirmed action per the operator-permission boundary for persistent integrations.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Slack channel for completion notification | Raised first by the operator; declined once discussed — adds a new integration surface for a signal GitHub already carries natively (PR state, checks), and this repo already has a working GitHub-state-check precedent (`daily-repo-truth-sync`) to extend rather than replace. |
| Keep merge manual, automate only dispatch + detection | This was the default recommendation going in (tonight's caution: manual review just caught two real problems). Operator explicitly heard the tradeoff and overruled it — reversibility of the underlying git state (a bad merge can be reverted) and the binary gate's specificity were the deciding factors. Recorded here per Rule 0, not silently adopted. |
| Interval polling instead of a webhook | Viable fallback (`daily-repo-truth-sync`-style, tighter interval) if webhook creation is declined or fails — kept as §6 fallback, not primary, because event-driven is faster and a poll interval is itself a source of "notification lag" the operator is trying to remove. |
| Auto-merge with no surface-list check, `fable-judge` alone as the gate | Ruled out — a single adjudication pass, however good, is still one pass; tonight's own adversarial-rescue work (0 of 4 tombstone candidates survived a *second* independent check) is direct evidence in this exact session that a single pass misses real dependencies. The surface list is a second, independent, mechanical check that doesn't depend on `fable-judge` having reasoned correctly. |
| Widen Cursor's routing-test eligibility (question 1) to match this ADR's forbidden list | Out of scope — that's the parent ADR's decision to revisit, not this one's. This ADR only touches the merge gate; it does not propose Cursor build on any surface it couldn't already build on. |

---

## §4 — Falsifiers (revert triggers)

1. **Auto-merged defect.** Any auto-merged PR later found to carry a defect that the gate's own conditions (a–e) should have caught, or that a human reviewer would plausibly have caught and the gate's design did not account for → revert §2's merge automation to operator-gated; supersede this ADR with the specific gap named and closed.
2. **Surface-list breach.** Auto-merge fires on any diff touching a path in the forbidden list — a bug in the mechanical check itself, not a judgment failure → **immediate hard stop on the entire auto-merge capability** (not just a revert-and-continue), logged as an incident, until the check is fixed and re-verified against a synthetic positive case (a test PR that *should* trip it).
3. **Silent-failure recurrence.** The detection/notification link itself fails silently again (webhook doesn't fire, routine errors without surfacing) for more than 48 hours without the operator noticing → the heartbeat mitigation (§6) has failed; add a second, independent dead-man's-switch check.
4. **Parent falsifier, inherited unchanged.** The 2026-07-14 ADR's own §4 limb 1 (≥2 judgment-defect PRs in a rolling 8-week window) still governs whether Cursor should be building the task class at all, independent of this ADR's merge-automation question.

**Trigger check schedule:** rides the same cadence as the parent ADR — the 2026-11-08 programme audit.

---

## §5 — Forbidden moves

- **Auto-merging a `VERIFIED WITH CAVEATS` or `REFUTED` verdict** — the caveat or refutation is the signal this whole gate exists to catch; treating it as "close enough" defeats the point.
- **Widening the auto-merge-forbidden surface list's *exclusions* without a fresh ADR** — this list is exactly the kind of thing that erodes under convenience pressure ("it's just a one-line doc fix in `docs/adr/`, surely that's fine to auto-merge") — the parent ADR named this exact pressure pattern for the routing test; it applies here too.
- **Skipping the full `pytest` run in favor of the gate battery alone** — explicitly ruled out per Rule 16's own stated reasoning, not a new judgment call.
- **Silent retry on gate failure** — a failed condition reports and stops. It does not re-dispatch, re-run fable-judge with different framing, or attempt the merge again without a human noticing something needed a second look.
- **Treating this ADR as authorizing wider Cursor task eligibility** — it does not; see §3's ruled-out alternative.

---

## §6 — Consequences

**Positive:** removes the two friction points the operator named — dispatch-approval and completion-detection — while extending, not replacing, infrastructure that already exists (`dispatch_cursor.ps1`, the daily GitHub-state-check pattern). The gate is mechanical and auditable after the fact (every auto-merge should be traceable to which of a–e passed).

**Negative (real cost):** none of the review discipline goes away, it moves earlier — the handoff brief and the routing test now carry more weight, since they're the only human-authored checkpoints left before a PR can auto-merge. A poorly-specified handoff brief is a bigger single point of failure than before, structurally.

**Risk, named explicitly (not hedged):** tonight's own chip-visibility failure is direct evidence that a notification-adjacent mechanism in this environment can fail silently. An auto-merge pipeline is worse if it fails silently, because "nothing merged" and "nothing needed to merge" look identical from the operator's side. Mitigation: `daily-repo-truth-sync`'s existing step 2 (open PRs / branches, SPENT / CARRIES-WORK / UNKNOWN classification) keeps running as a **daily heartbeat independent of the webhook** — if a `cursor/*` branch sits open past one daily cycle without the webhook having fired, that surfaces in the morning digest even if the event-driven path is silently broken. This is why §6 keeps the poll alive rather than retiring it in favor of the webhook.

**Downstream artifacts (on acceptance):**
- Dated addendum on `2026-07-14-cc-cursor-surface-allocation.md` recording the narrowing (this commit).
- `CLAUDE.md` — no change needed; its posture section doesn't currently restate the CC/Cursor merge rule (confirmed via this session's earlier Rule-7 audit work), so there's nothing to keep in sync.

---

## §7 — Implementation plan

- **Phase 0 (this ADR).** Ratifies the policy. Does not itself create the webhook.
- **Phase 1 (separately confirmed action — persistent integration, not covered by this ADR's ratification alone).** Create the webhook trigger: `RemoteTrigger create_webhook_trigger`, scoped to this repo, filtered to `cursor/*` branch PR-ready-for-review / checks-completed events, firing a routine that runs the §2 adjudication sequence (fable-judge → gate battery → pytest → surface check → merge-or-report). Requires the operator's explicit go on the specific webhook configuration before it fires, per the standing rule that persistent integrations/webhooks need in-chat confirmation regardless of standing delegation to move fast.
- **Phase 2.** CC's own dispatch behavior changes immediately on acceptance (no separate technical step) — future Cursor-eligible tasks get dispatched via `dispatch_cursor.ps1` directly rather than via chip.
- **Phase 3.** Addendum landed on the parent ADR (this commit, see below).

---

### Addendum (2026-08-14, same day) — §7 Phase 1 complete: webhook live

The GitHub webhook trigger is configured and confirmed live via the routine's own page (`https://claude.ai/code/routines/trig_012nvuH7jqmjFUFgoFVpZ6RP` → "Triggers on"): `joshua-asante/first-passage`, event **Pull request: Opened**, alongside the existing 6-hour cron (`52 */6 * * *`).

**Correction to §7's original plan:** the mechanism is not the raw `RemoteTrigger create_webhook_trigger` API call — that path requires a `scope_id` with no documented way to obtain one, confirmed via direct research (no public docs mention it) and dead-end API exploration (`hook_type=app` → missing scope_id; `hook_type=url` → "minted by the bound session, not created through this API"). The actual, correct mechanism is the routine's own web UI: Edit → "+ Add another trigger" → "GitHub event," which handles the GitHub App authorization internally. No separate connector or App-installation page exists to find; searching for one was the wrong framing.

**Known gap, not blocking:** the trigger fires unfiltered on every `pull_request: opened` event repo-wide, not scoped to `cursor/*` branches at the webhook level — a "Head branch starts with" filter exists in the UI but did not respond reliably to automated interaction, and shipping a malformed empty filter risked silently blocking all events, so it was removed rather than left broken. This does not affect §2's correctness: the routine's own prompt step 1 re-derives the `cursor/*` scope from scratch on every invocation regardless of trigger cause, so an unscoped webhook fire on a non-`cursor/*` PR is a wasted invocation, not a gate bypass. Narrowing the filter is a quota-efficiency polish item, addable directly in the UI, not tracked as a falsifier.

## §10 — Audit hooks (runnable)

```bash
# Every auto-merged commit since this ADR's effective date traces to a passing gate:
git log --oneline --since=<webhook-creation-date> --grep="auto-merge" -- .
# Expected: each hit's PR has a corresponding fable-judge VERIFIED record and green CI run — spot-check via gh pr view <n> --json

# No auto-merge ever touched the forbidden surface list:
git log --all --oneline --since=<webhook-creation-date> -- core/dd_protection.py core/firm_rules.py core/portfolio_mc.py core/mc/ core/lifecycle.py core/dd_geometry.py ops/c1_rail/ ops/instruments/ docs/notes/rail_build/ docs/adr/ docs/spec/ docs/operational_rules.md CLAUDE.md
# Expected: any hit in this window is either a manual (operator/CC) commit, or a finding for falsifier limb 2.

# Webhook liveness (the heartbeat mitigation is doing its job):
grep -A3 "OPEN PRs" <latest daily-repo-truth-sync digest>
# Expected: no cursor/* branch sits CARRIES-WORK for more than one daily cycle without a corresponding auto-merge or a flagged manual-review reason.

# Falsifier limb 1 sweep (quarterly, rides parent ADR cadence):
grep -in "auto-merge" docs/SESSIONS.md | grep -in "defect\|revert\|incident"
```

---

## Verification

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-14-cc-cursor-autonomous-loop.md --type adr
git log -1 --format='%h %ci' -- docs/adr/2026-07-14-cc-cursor-surface-allocation.md scripts/dispatch_cursor.ps1
```
