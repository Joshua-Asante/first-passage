# P3 docs-runtime inventory — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** **GO 2026-08-23.** Operator promoted P3 as queue #3 (same shape as P2). Charter: [`2026-08-23-repo-pain-point-packets.md`](2026-08-23-repo-pain-point-packets.md) §P3. Does not jump B7/M1 or the Q-TRADECAP-1 election.

**Goal:** A report-only inbound-reference index of Python runtime reads of `docs/` and root orientation files, including pathlib joins the Great Prune classifier missed.

**Architecture:** One scanner, two detectors (quoted-path + pathlib-join), one generated markdown report, `gates.yml` path-conditional gate that always exits 0.

**Tech Stack:** stdlib (`argparse`, `re`, `pathlib`). Existing `gate_manifest.py`.

## Global Constraints

- Index only. No deletes. Not a prune list.
- No HARD fail. No `tier: soft`.
- Skip `lab/archive/`. Do not treat an empty default-grep as absence.
- Do not auto-promote P4/P5.
- Cheap falsifier (2026-08-23): `ops/c1_rail/c1_rail_arm.py` has no `docs/notes/rail_build` substring; `ops/recall/guard.py` contains `CLAUDE.md`; `lab/discovery/register_search.py` contains `docs/`.

## File Structure

| File | Change |
|---|---|
| `scripts/check_docs_runtime_inventory.py` | Scanner + `--write` / `--check` |
| `docs/notes/audits/docs-runtime-inventory.md` | Generated report |
| `tests/test_docs_runtime_inventory.py` | Tmp-tree + known-read + --check exit 0 |
| `scripts/gates.yml` | `docs-runtime-inventory` path-conditional |
| `tests/test_gate_manifest.py` | Probe + expected-id set |
| `STATE.md` | #3 during land; delete on completion |
| `docs/SESSIONS.md` | Prepend only |

---

### Task 1: STATE #3

- [x] Cheap falsifier (above).
- [x] Add queue row 3 pointing at this plan + Great Prune §3.2.

### Task 2: Tests then scanner

- [x] Failing tests (tmp CLAUDE.md read + pathlib `docs` join; real-repo known reads; `--check` exit 0).
- [x] Implement quoted-path + pathlib-join detectors.
- [x] `--write` inventory. Wire gate. Reachability probe = `ops/c1_rail/c1_rail_arm.py`.

### Task 3: Close row

- [x] Delete STATE #3. Decision-index. Charter start-when. SESSIONS prepend. Bind + liveness green.
