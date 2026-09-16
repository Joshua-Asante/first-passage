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

1. **Honor explicit override.** If the user already said local or cloud for this work, use that. Skip the ask.
2. **Run the local-only checklist.** Any hit → `local`. State which item hit.
3. **No hits → cloud-eligible.** Do **not** launch yet. Ask for GO with a one-line reason.
4. **Unclear → `local`.** Safe default.

## Local-only checklist

Any hit forces `local`:

- Needs gitignored / vendor data not present in a fresh remote checkout
- Needs secrets, API keys, or credentials
- Needs local-only services (DB, Docker, VPN, hardware, private network)
- Needs GUI, interactive approval, or browser-on-this-machine
- Depends on uncommitted, unpushed, or worktree-only state
- Needs durable local disk or paths outside a fresh cloud checkout

## Output contract

Emit this before launch (or before the cloud ask):

```text
Routing: local | cloud-eligible
Reason: <checklist hit, or "no local-only deps">
Action: launching local | waiting for cloud GO
```

**Cloud ask** (one sentence): why eligible + “Launch in cloud?”

## Non-goals

- No project ADR / Test-0 coupling
- No scripts
- Does not decide whether a Task should exist — only `environment` once Task is chosen

## Related

This skill is the **canonical home** for the local-only checklist. Any multi-packet dispatch
re-applies it per packet at dispatch time, not once at authoring time — the dispatch-moment
re-check is the load-bearing part, because a packet's environment premises go stale between
authoring and dispatch.

The retired `cursor-fleet` skill carried that per-packet restatement; it is removed with the
Cursor lane ([worker-surface allocation](../../../docs/adr/2026-07-14-cc-cursor-surface-allocation.md),
Revision 2026-09-15). Nothing was lost: the checklist itself never moved from here.
