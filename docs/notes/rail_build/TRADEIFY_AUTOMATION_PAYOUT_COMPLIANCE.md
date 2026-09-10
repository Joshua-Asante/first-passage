# Tradeify automation / payout compliance — coverage record

**Created:** 2026-09-10
**Reader:** `ops/sentinel/activity_week.py` (`format_activity_decision_line`), wired as a
Claude Code `SessionStart` hook in `.claude/settings.json`. That module names this file as the
designated authoritative record of a week's operator decision / trade.
**Venue rule:** per-Mon–Fri-week bucket, at least one trade per week (art. 10468318).
**Posture owner:** [STATE](../../../STATE.md#scheduled-forward-triggers) owns the recurrence and
the deadline roll. This file records what happened; it does not set policy.

## 1 — Scope, and what this file must never contain

This repository is public. This record carries **trade days only**. It must never contain an
account identifier, account balance, position size, fill price, or realised P&L — those stay
private under the [public-clone posture](../../../CLAUDE.md#public-clone-posture). A coverage row
needs the bucket and the day; nothing further is required to discharge the venue rule, so nothing
further is published here.

This file is **not** a licence to trade, a reminder to trade, or an instruction to any agent.
**No agent may place a trade.** Every row below records a trade the operator placed.

The file was created on 2026-09-10. It does **not** retroactively attest any week before that
date; absence of a row for an earlier week means no row was written, not that the week was idle.

## 2 — Weekly activity coverage

### 2a — Append-only coverage protocol

Rows are appended, never edited or reordered. One row per Mon–Fri bucket. The reader matches a
history row of this exact shape:

| Bucket | Trade day | Status | Note |
|---|---|---|---|
| `MM-DD`→`MM-DD` | `YYYY-MM-DD (Day)` | `✅ COVERED` | free text, no `|` |

A week is marked covered only when the operator has confirmed a filled trade inside that bucket.
A week whose trade day is unknown is **not** written as a covered row — record the gap in §3
instead. Missing evidence is not completion.

### 2b — Coverage history

| Bucket | Trade day | Status | Note |
|---|---|---|---|
| 08-31→09-04 | 2026-09-02 (Wed) | ✅ COVERED | Sole trade of that bucket. Day resolved 2026-09-10 from the operator's platform P&L calendar, which shows one trade that week, on the 02. Supersedes the earlier 09-02/09-03 ambiguity. |
| 09-07→09-11 | 2026-09-10 (Thu) | ✅ COVERED | Operator-placed MNQU6 round trip, market in and out, both legs filled. Confirmed by operator 2026-09-10. |

## 3 — Owed and not claimed

- **Weeks before 08-31.** Not covered by this file; see the campaign record's attestation history.
- The 08-31→09-04 row above closes the obligation STATE carried for that week. Its day came from a
  platform view the operator supplied, not from a fills export held in this repository; the
  underlying view is private and is not reproduced here.
- This record makes **no live check**. Rail arm status is authoritative only from the deployed host
  (RUNBOOK §B7). Nothing here changes the standing posture: c1 is warm and disarmed, no deployed
  book.
