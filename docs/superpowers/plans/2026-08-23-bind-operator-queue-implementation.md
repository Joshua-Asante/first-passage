# Bind the operator queue — implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**AUTHORIZATION:** **GO — landed 2026-08-23.** Operator named row 3 = Lane A (blind / no-counterparty channel). Tasks 2–5 execute on this GO. This packet serves the Survive bound; it does not jump F1 / B7–M1.

**Goal:** Stop leftover/nav/SESSIONS work from being served ahead of the operator queue by making `Open / next` queue-led, adding one doable generation row (the current top two are waits), and enforcing that at session start plus a SESSIONS-only gate.

**Architecture:** Amendment-first addenda on the Survive-bound and W5 ADRs. Rewrite the three carry-forward surfaces that immortalize leftovers. A path-conditional checker reads only the newest SESSIONS `Open / next` and asserts it cites every live STATE queue row number. No path-allowlist; no hours budget; no new generation channel.

**Tech Stack:** existing `gate_manifest.py` / `gates.yml`, stdlib argparse checker, Cursor always-apply rule + Claude hookify SessionStart/warn.

**Companion:** first-look residuals live on [`2026-08-23-repo-pain-point-packets.md`](2026-08-23-repo-pain-point-packets.md) (charter owns the live packet list). Bind has landed.

## Global Constraints

- No hours figure (Rule 2 §5 #2; Survive-bound ADR Boundary).
- No second Great Prune; no hard doc-budget gate (F-2 addendum declined).
- No new generation *channel* — row 3 is the next concrete step on an existing owner.
- Do not use `tier: soft` (`gates.yml` header: dead, no caller).
- Gate reads `docs/SESSIONS.md` + `STATE.md` operator table only.
- Amendment-first (Rule 8 sub-rule 10): addenda on existing ADRs, not sibling ADRs.

## Why the existing cap failed

[`STATE.md`](../../../STATE.md) ≤5 queue already *is* the Survive bound ([`docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md`](../../adr/2026-08-09-survive-bound-is-the-queue-cap.md)). Falsifier: **work repeatedly served out of order** (first check 2026-11-08).

1. **#1 and #2 are waits.** F1 is “do not decide early.” B7/M1 wait on a strategy on the ruled host. Agents cannot execute either, so they execute carried `Open / next` leftovers.
2. **Carry-forward immortalizes leftovers.** [`.cursor/rules/session-discipline.mdc`](../../../.cursor/rules/session-discipline.mdc), [`.claude/hookify.session-log.local.md`](../../../.claude/hookify.session-log.local.md), and the [`docs/SESSIONS.md`](../../SESSIONS.md) header all require copying the prior `Open / next` line. W5’s judgment-gate cut entry length, not topic.

## File Structure

| File | Change |
|---|---|
| `docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md` | Addendum: out-of-order serving is the live defect; repair = queue-led Open/next + doable row 3 while #1/#2 are waits. |
| `docs/adr/2026-08-07-w5-governance-diet.md` | Addendum: Open/next lead line is the queue; leftovers stay on owner artifacts. |
| `STATE.md` | Row 3 + one-sentence parking rule (no parking-lot section). |
| `.cursor/rules/session-discipline.mdc` | Replace carry-forward with queue-led Open/next + session-start refuse. |
| `.claude/hookify.session-log.local.md` | Same wrap-up rule. |
| `.claude/hookify.queue-bind-session-start.local.md` | **Create.** SessionStart/warn: Read STATE queue; refuse off-queue asks unless `queue-exception:`. |
| `docs/SESSIONS.md` | Header rewrite + first stub entry whose Open/next is queue-led. |
| `scripts/check_sessions_queue_bind.py` | **Create.** Parse newest entry Open/next; HARD fail if any live `#N` is missing. |
| `scripts/gates.yml` | `sessions-queue-bind` path-conditional on `^docs/SESSIONS[.]md$`. |
| `tests/test_sessions_queue_bind.py` | **Create.** Fixture pass/fail cases. |

---

### Task 1: Operator names row 3 (GO gate)

**Files:** none until the name exists. After GO, Task 2 writes it into `STATE.md`.

**Short list (pick one; do not invent a fourth channel):**

| Candidate | Clock / state | Owner |
|---|---|---|
| Blind channel | 2/3 pre-G0 kills; one slot left | [`docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md`](../../adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md) |
| MSL | own hard clock ~2026-10-07 | [`docs/adr/2026-08-14-msl-yield-falsifier-survival-limb.md`](../../adr/2026-08-14-msl-yield-falsifier-survival-limb.md) |
| Deep lane | DL-1/DL-2 abandoned; only if a DL-3 is already chartered | [`docs/adr/2026-08-16-deep-iteration-lane-charter.md`](../../adr/2026-08-16-deep-iteration-lane-charter.md) |
| Harvest P4 | currently HOLD | [`lab/analysis/harvest/six_lead_cf_2026-08-17/P4_DRYRUN.md`](../../../lab/analysis/harvest/six_lead_cf_2026-08-17/P4_DRYRUN.md) |

- [x] **Step 1:** Operator picks one row and one *next concrete step* (not a channel reboot). **Lane A** — blind channel; name or decline the next construct on the reopened 6A/M6A or GC/MGC doors.
- [x] **Step 2:** If no pick, stop. Do not implement Tasks 2–5 (bind with only wait-rows produces idle or universal `queue-exception:`).

### Task 2: ADR addenda + STATE row

**Files:**
- Modify: `docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md`
- Modify: `docs/adr/2026-08-07-w5-governance-diet.md`
- Modify: `STATE.md` operator table

- [x] **Step 1:** Cheap falsifier: `rg -n "Open / next|carry the prior" .cursor/rules/session-discipline.mdc .claude/hookify.session-log.local.md docs/SESSIONS.md` — those three hits are the carry-forward bug Task 3 rewrites. Write the addenda against that count, not a remembered list.
- [x] **Step 2:** Survive-bound addendum: name the live defect (out-of-order serving); name the repair (queue-led Open/next + doable row 3); reaffirm no hours figure; forbidden = leftover names leading Open/next, new generation channel, `tier: soft`.
- [x] **Step 3:** W5 addendum: does not amend the A–D class table; Open/next lead = `STATE queue: #1 … · #2 … · #3 …`; residue after that line only with `queue-exception:` and an existing owner.
- [x] **Step 4:** STATE: keep #1 F1 and #2 B7–M1; add #3 from Task 1; one parking sentence under the table — leftovers stay on their owners; re-entry = promote to a queue row and drop something else (cap ≤5). No new section.
- [x] **Step 5:** STATE decision-index one-liner + owner addenda links.

### Task 3: Rewrite carry-forward + session-start refuse

**Files:**
- Modify: `.cursor/rules/session-discipline.mdc`
- Modify: `.claude/hookify.session-log.local.md`
- Create: `.claude/hookify.queue-bind-session-start.local.md`
- Modify: `docs/SESSIONS.md` header only in this task (stub entry is Task 5)

Replacement rule (all three wrap-up surfaces):

- Lead line of `Open / next` = `STATE queue: #1 <title> · #2 <title> · #3 <title>` (titles + owner links).
- Default wrap-up does **not** copy leftover names from the previous top entry.
- Off-queue residue may follow the lead line only if this session used `queue-exception: <reason>` and the residue’s owner already exists.

Session-start (Cursor always-apply + Claude hook):

- First read: `STATE.md` operator table.
- If the user ask is not a queue row, refuse and name the three rows unless they wrote `queue-exception: <reason>`.

- [x] **Step 1:** Edit the three wrap-up surfaces to the replacement rule.
- [x] **Step 2:** Land the SessionStart/warn hookify file; keep `warn-session-log` for wrap-up (do not collapse the two hooks).
- [x] **Step 3:** `rg -n "Carry the prior top entry" .cursor/rules .claude docs/SESSIONS.md` — expect zero hits on the old sentence.

### Task 4: SESSIONS-only gate

**Files:**
- Create: `scripts/check_sessions_queue_bind.py`
- Create: `tests/test_sessions_queue_bind.py`
- Modify: `scripts/gates.yml`
- Modify: `tests/test_gate_manifest.py` (add `sessions-queue-bind` to the path-conditional reachability map next to `sessions-append-only`)

Checker contract:

- Read `STATE.md` operator table row numbers (`#1` … `#N` currently live).
- Read the newest `## YYYY-MM-DD` entry in `docs/SESSIONS.md`.
- Find its `**Open / next:**` (or `**Open / next**`) line.
- HARD fail if any live `#N` is absent from that line.
- Do not parse leftover names. Do not scan other files.
- `--file` / `--state` flags for tests (default repo paths).

- [x] **Step 1:** Write failing tests: (a) Open/next missing `#2` → exit 1; (b) Open/next cites every live `#N` → exit 0; (c) checker does not open `lab/` or `docs/adr/`.
- [x] **Step 2:** Run `pytest tests/test_sessions_queue_bind.py -q` — expect fail (script missing).
- [x] **Step 3:** Implement the checker; re-run tests — expect pass.
- [x] **Step 4:** Add `sessions-queue-bind` to `gates.yml` as `path-conditional` with `when.staged_regex: '^docs/SESSIONS[.]md$'` (same class as `sessions-order` / `sessions-append-only`). Update `test_path_conditional_gates_are_reachable`.
- [x] **Step 5:** Cheap falsifier on current `docs/SESSIONS.md` (top entry as of this plan still leads with leftovers): `python scripts/check_sessions_queue_bind.py` — expect fail until Task 5’s stub.

### Task 5: First queue-led stub entry

**Files:**
- Modify: `docs/SESSIONS.md` (append-only new top entry)

- [x] **Step 1:** `python scripts/roll_sessions.py --next-label <today>` and write a **stub** (heading + `Open / next` only). Lead line cites `#1` F1, `#2` B7–M1, `#3` <named shot>. Do not copy O10/O15/P7/P8/W5 CI/keep-20/coldstore into the lead. *(Landed as a full judgment+build entry `2026-08-24o` — Lane A GO is a judgment call.)*
- [x] **Step 2:** `python scripts/check_sessions_queue_bind.py` — expect pass.
- [x] **Step 3:** `python scripts/roll_sessions.py --check-order` and `--check-append-only` — expect pass.

## Success / falsifier

**H:** After land, two consecutive session days have queue-led top `Open / next`, and off-queue sessions either cite `queue-exception:` or do not exist.

**FALSIFIED if:** a leftover name leads `Open / next` again; a new generation channel is opened instead of filling row 3 from an existing owner; the gate is moved to `soft` or `--no-verify` becomes the standing path.

## Forbidden moves

- Building Tasks 2–5 before Task 1 GO.
- Path-allowlist of queue owner artifacts (blast-radius + concurrent PRs brick).
- A STATE “parking lot” section (anti-accretion).
- Rolling SESSIONS keep-20 in this PR (separate GO; see pain-point packets).
- Deriving CI from `gates.yml` (W5 H6 HOLD; existing plan).
- Deciding F1 or arming B7/M1.
