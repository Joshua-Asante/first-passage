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
- **Cloud return channel (operator, 2026-10-24).** A cloud session cannot message its coordinator, and no note arrives when it ends. So every cloud brief names where results go: a PR the session opens, whose description begins `Cloud-task: <session name>`, or an existing PR or issue, for work that may commit nothing or that commits to a branch that already has a PR (a read-only review names the PR it reviews). The session posts its final report, or any blocking question, there as a comment beginning `Cloud-task: <session name>`; if an open PR already carries that name, it posts there instead of opening a second. The coordinator reads the target it named, finds opened PRs with `gh pr list --search "Cloud-task"`, and answers by messaging the session. A PR stacked on another open PR says so; the merge-train conductor retargets it to `main` (`merge-train` §2; merged branches are kept, so GitHub does not). Cloud clocks run on UTC: date records by the operator's ET day (`TZ=America/New_York date +%F`). Work that will need the operator's decisions partway through goes to a local session, whose turns report back.
- **Cloud review (operator, 2026-09-27).** A cloud reviewer of a pushed, pinned revision returns findings without writing to the reviewed branch.

## Local-only checklist

Any hit forces `local`:

- Needs gitignored inputs a fresh clone lacks (vendor CSVs, `.cache` verification records)
- Needs secrets, API keys, or credentials (including `.env`)
- Needs local-only services (DB, Docker, VPN, hardware, private network)
- Needs GUI, interactive approval, or browser-on-this-machine
- Depends on uncommitted or untracked changes. An unpushed branch is not a hit: the cloud clones its start branch from `origin`, so push it before launch (a fresh branch from `main`: `git fetch origin main && git push origin origin/main:refs/heads/<branch>`)
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
