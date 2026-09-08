# ADR 2026-08-21 — One subscription ledger and monthly reconfirmation

**Status:** `Accepted` — operator ratified the ledger, checks and monthly cadence on 2026-08-21.
**Decision date:** 2026-08-21
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Format:** concise
**Revision:** 2026-09-08 — remove the retired role's hooks; ledger terms unchanged.
**Prior version:** `4fb2b88f3b7d56d77463c43ba45c87ffadff6a31`.

## Decision

**D1 — One ledger.** [SUBSCRIPTION_LEDGER](../pursuits/SUBSCRIPTION_LEDGER.md)
owns the cost figures for d11–d17. Pursuit records link to it rather than repeat
numbers. Missing figures remain unknown, not zero; this revision adjudicates none.

**D2 — Ledger pointer.** [check_pursuit_records.py](../../scripts/check_pursuit_records.py)
requires a ledger pointer on KEEP records of class `(d) meta-belt (subscription)`
or `(d) meta-belt (venue account)`. It reports WARN and exits zero on a completed
scan; no severity escalation or class widening is authorized. Reverify the actual
corpus before any separately approved widening. This remains a scoped check, not
a general required-field mandate for every pursuit.

**D3 — Monthly reconfirmation.** The operator confirms the ledger figures monthly,
next due 2026-09-21, rolling the STATE deadline after each occurrence. Confirm even
when unchanged; silence is not evidence of currency. The former charter/spawn-time
check is retired with the role. No replacement role, hook or scheduled service is
commissioned; STATE holds the forward reminder, not a claim about external scheduling.

**D4 — Update at disclosure.** A cost supplied in-session updates its ledger row
in that session. This is a practice, not a telemetry subsystem. Additional automation
needs evidence that the practice is insufficient and its own decision.

**Trigger check schedule:** every monthly reconfirm (2026-09-21, then rolled forward).

At each reconfirm, check whether the pointer rule gave a false-positive WARN for a
record with no meaningful cost, or the ledger missed a stale/wrong figure that the
former per-pursuit text would have caught. Either finding requires a decision to
narrow/redesign the affected mechanism, with the miss recorded. Three consecutive
reconfirms with no figure changes and no staleness found warrant proposing a quarterly
cadence; they do not authorize changing it silently. The original verdict distinction
remains: RESOLVED when the mechanism runs without those failures, FALSIFIED for a
confirmed mechanism failure, AMBIGUOUS for that cadence signal pending a proposal.

## Grounds

Scattered cost tags left a known information gap open for twelve days. One owner
plus a creation-time pointer check makes the figures discoverable; operator
reconfirmation checks their truth. HARD-gating, a parallel monthly cron and new
telemetry were rejected as extra machinery without evidence. Monthly was the
operator's chosen interval, so its suitability remains reviewable under the rule above.
The original implementation narrative is retrievable at the prior revision. It
creates no current charter, log or review duty for a retired role.

## Current owner

- [Ledger](../pursuits/SUBSCRIPTION_LEDGER.md): figures, billing questions and confirmation dates.
- [STATE](../../STATE.md): rolling monthly reminder.
- [Pursuit checker](../../scripts/check_pursuit_records.py) and
  [its tests](../../tests/scripts/test_check_pursuit_records.py): class/pointer contract.

Verification: `python scripts/check_pursuit_records.py` and
`python -m pytest tests/scripts/test_check_pursuit_records.py`.
