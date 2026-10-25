---
name: task-routing
description: >-
  Routes Task/subagent work to local vs cloud from dependency checks. Use
  automatically before launching a Task (or any subagent spawn that picks
  environment), and when choosing whether work should run locally or in the cloud.
---

# Task routing (local vs cloud)

Decide `environment: local` vs `cloud` **before** launching a Task / cloud-capable subagent. This skill only picks the environment — not whether to use a Task.

## Procedure

1. **Honor explicit override.** If the user already said local or cloud for this work, use that. Skip the rest.
2. **Run the local-only checklist.** Any hit → `local`, and the card, handoff or dispatch prompt says **"Must run locally"** near its top with the reason (the checklist item that hit).
3. **No hits → `cloud`.** Cloud is the default for chip tasks, handoffs and dispatch cards ([AGENTS.md §Purpose](../../../AGENTS.md#purpose), operator direction 2026-10-13); no environment GO is asked.
4. **Unclear → resolve the item.** Run the cheap check (is the path tracked? is the credential needed?). If it stays unresolved, treat it as a hit and apply step 2.

## Standing preferences

- **Cloud default (operator, 2026-10-13).** Owner: [AGENTS.md §Purpose](../../../AGENTS.md#purpose). A local packet without the "Must run locally" line and its reason is malformed.
- **Cloud return channel (operator, 2026-10-24).** A cloud session cannot message its coordinator, and no note arrives when it ends. So the coordinator fixes the return destination before launch, and the brief names it: a session that will commit opens its own PR whose description begins `Cloud-task: <session name>`; a session that may commit nothing (a read-only review, or work on a branch that already has a PR) posts on an existing PR the brief names, in a comment beginning `Cloud-task: <session name>`. Either way, the final report or any blocking question goes there as a PR comment. The coordinator finds results with `gh pr list --search "Cloud-task"` (GitHub search also matches comments), and answers by messaging the session. Push the branch the cloud session starts from before launching it. Work that will need the operator's decisions partway through goes to a local session, whose turns report back.
- **Cloud review (operator, 2026-09-27).** A cloud reviewer of a pushed, pinned revision returns findings without writing to the reviewed branch.

## Local-only checklist

Any hit forces `local`:

- Needs gitignored / vendor data not present in a fresh remote checkout
- Needs secrets, API keys, or credentials
- Needs local-only services (DB, Docker, VPN, hardware, private network)
- Needs GUI, interactive approval, or browser-on-this-machine
- Depends on uncommitted, unpushed, or worktree-only state
- Needs durable local disk or paths outside a fresh cloud checkout
- Needs the private read surface or other private evidence writes ([AGENTS.md §Public-clone posture](../../../AGENTS.md#public-clone-posture)) or the operator's machine or VM

## Output contract

Emit this before launch:

```text
Routing: local | cloud
Reason: <checklist hit, or "no local-only deps">
Action: launching local ("Must run locally: <reason>" on the packet) | launching cloud
```

## Non-goals

- No project ADR / Test-0 coupling
- No scripts
- Does not decide whether a Task should exist — only `environment` once Task is chosen

## Related

This skill is the **canonical home** for the local-only checklist. Any multi-packet dispatch
re-applies it per packet at dispatch time, not once at authoring time — the dispatch-moment
re-check is the load-bearing part, because a packet's environment premises go stale between
authoring and dispatch.
