# Handoff packets — routing rule

**Earlier handoffs remain historical evidence; current dispatch is the coordinator's board row plus its frozen card.**

A packet in this directory is a record of an assignment, its context and its provenance at the date in its filename. Committing a packet does not dispatch it, and an older packet's ownership statements do not override later ownership decisions. To find the current assignment for a workstream, read the coordinator's board (`coordinator` skill §3); Joshua assigns the coordinator per session (§1).

## Pre-mortem (every multi-loop packet)

Multi-loop packets carry the pre-mortem and pre-run checks of `brief-authoring` checks 11–14.

## Packet status

The eleven packets PR #444 committed on 2026-09-20 from previously untracked files, the E1 coordinator handoff, which was already tracked and which #444 only amended with its publication addendum, and the later coordinator snapshots.

| Packet | Status |
|---|---|
| `2026-09-12-astra-tradeify-contract-pr-closeout.md` | HISTORICAL — names Astra as coordinator; superseded by the three-seat ADR revision (PR #442) and later ownership decisions |
| `2026-09-12-tb-s3-kernel-redesign.md` | HISTORICAL — Track B; see the Track B umbrella and its closures |
| `2026-09-15-operator-codex-deployment-checklist.md` | SUPERSEDED by the 2026-09-20 checklist and its amendment |
| `2026-09-15-phase1-parallel-session.md`, `…-phase2-parallel-session.md`, `…-phase3-parallel-preparation.md` | HISTORICAL — phase-preparation assignments; their surviving requirements live in `docs/briefs/phase3-preparation/2026-09-15/` and are consumed by T10 |
| `2026-09-17-qualification-structural-closure.md` | COMPLETED — see the structural-closure plan's ledger |
| `2026-09-19-full-e1-coordinator-handoff.md` | HISTORICAL — the S2 coordinator handoff (tracked before #444; #444 added only its publication addendum); S2 was accepted and merged 2026-09-21 (PR #436) |
| `2026-09-19-full-e1-s1-budget-recovery.md` | COMPLETED — S1 accepted (PR #428) |
| `2026-09-19-glm-s2-enforcement-continuation.md`, `…-glm-s2-linux-diagnostic-steering.md` | COMPLETED — S2 continuations; returns in the execution-slices ledger |
| [`2026-09-19-jev-experimentation-claude.md`](https://github.com/Joshua-Asante/first-passage/blob/4121e84c95f4990b71962e3b9570c4c3fad88426/docs/briefs/handoffs/2026-09-19-jev-experimentation-claude.md) | REMOVED 2026-10-15 — unrelated to the Tradeify deployment track; the pilot falsified its saving prediction and no integration was enabled (pinned blob) |
| `2026-09-22-full-e1-coordinator-handoff.md`, `2026-09-24-full-e1-coordinator-handoff.md`, `2026-09-25-full-e1-claude-continuation.md` | HISTORICAL — coordinator snapshots; the coordinator role is assigned per session (surface-allocation ADR Addendum 2026-10-28) |

