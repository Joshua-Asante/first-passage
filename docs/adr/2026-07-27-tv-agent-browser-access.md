# ADR 2026-07-27 — Agent browser access to TradingView

**Status:** `Accepted`
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Supersedes-in-part:** `2026-06-23-tv-backtest-egress-automation.md` in part — the agent-access prohibition only, as applied to page-level browser reads. The layered egress strategy (§2), the allowlist-circumvention bullet, the second-account bullet and the private-Pine bullet are **retained**.
**Retain-until:** none
**Decision date:** 2026-07-27
**Authors:** Joshua (operator directive) + Claude Code (Opus 5)
**Related:** `2026-06-23-tv-backtest-egress-automation.md` (+ its Addendum 2026-07-27); `2026-06-30-no-manual-trading-cfd-retirement.md`; `2026-07-17-c1-rail-build-account-registration-go.md`
**Layer:** infrastructure

---

## §0 — Rule 0 reads (verified 2026-07-27)

- **`docs/adr/2026-06-23-tv-backtest-egress-automation.md`** — read in full this session. §1 rationale, §3 path table, §5 forbidden moves, §0's empirical probe. Verbatim §5 bullet 1: *"Running any TV automation (A/B/D) on the live-edge account — ruled out absolutely; a backtest-automation ban takes down live execution."* Verbatim §0: the Claude-in-Chrome MCP *"refuses to navigate to `tradingview.com`"* — **verified by a `navigate` call**, 2026-06-23.
- **Same ADR §3** — Path A1 (DOM scrape) **Refuted**: the List-of-Trades table is virtualized. Path B (WebSocket) requires the live-edge `sessionid`. Both closed on **technical** grounds, independent of policy.
- **`docs/SESSIONS.md`** — grepped for TradingView across all 2026-07-27 entries: **no agent-side TV access is recorded**. The 07-27 TV housekeeping (stale duplicate MYM script deleted) is logged as performed *by the operator*.
- **Browser surface probe, this session** — `tabs_context` on the in-app browser returned *"No preview is open."* No TV session was open on the agent surface at the time of the directive.
- **`docs/notes/rail_build/B7_STAGE1_DESK_CARD_2026-07-28.md`** — the five TV items the reversal is meant to make agent-checkable.

---

## §1 — Context

Operator directive, 2026-07-27, verbatim: *"i want to reverse the adr that restricts your usage of Tradingview in the browser … I want you to be unrestricted in your access to Tradingview if it saves time."*

The immediate motivation is B7 Stage 1: five TV facts (one active alert per leg, venue edition selected, `alert_message` passthrough, webhook URL + `path_token`, expiry) currently gate an operator-attended session and cannot be verified from the repo. Everything else in that pre-flight was verified agent-side on 2026-07-27; TV is the only remaining blind spot.

**A premise correction, recorded because it was part of the directive's basis.** The directive stated *"We were just looking at Tradingview from this surface earlier today."* §0 finds no such access: no TV mention in any 07-27 session entry, the one logged TV action was operator-performed, and no browser tab was open on the agent surface. This matters only because prior uneventful agent access would have been *evidence* about risk; operator use of their own account is not. The reversal below therefore rests on the operator's risk acceptance, not on a precedent.

---

## §2 — Decision

**The repo-side prohibition on agent browser access to TradingView is REVERSED.** An agent may drive a browser surface against TradingView for operator-directed work, at human cadence, without a per-session ADR or a fresh grant.

### §2.1 — What this ADR cannot do

**It cannot grant access the tooling itself withholds.** The `tradingview.com` refusal recorded in the 2026-06-23 §0 probe is a **platform safety control on the browser tool**, not a repo policy. A repo ADR has no authority over it. If the surface refuses, the correct outcome is **"blocked"**, reported as such — never a workaround.

Accordingly the 2026-06-23 §5 bullet — *"Circumventing the browser safety allowlist … the restriction is a safety control; the answer is a different driver under isolation, not a bypass"* — is **explicitly retained and not superseded**. This ADR permits *use* of whatever surface is available; it authorises no bypass of any surface that declines.

### §2.2 — What the reversal does and does not unlock

Most of what the 2026-06-23 ADR discussed was closed on **technical**, not policy, grounds. Reversing policy does not reopen it:

| Capability | Status after this ADR |
|---|---|
| Page-level **reads** — alert list/state, alert condition + message body, webhook config, expiry, chart/script identity | **Unlocked** (this is the operative change) |
| Path A1 — DOM-scrape List-of-Trades | Still dead — table is virtualized (technical) |
| Path B — chart WebSocket backtest egress | Still coupled to the live-edge `sessionid` (technical) |
| Backtest CSV egress generally | Unchanged: **manual export remains the sanctioned default**; Path E (local port) remains the real leverage |
| Second TV account | Still forbidden — multi-account house rule, collateral-ban risk (retained) |

**Net:** this buys pre-flight verification and debugging, not an egress pipeline.

### §2.3 — Reads vs writes

**Reads are authorised broadly.** **Writes are not.** Creating, modifying, deleting or disabling an alert changes account settings on the sole signal origin of the live rail, and remains **confirm-first, per action** — consistent with the standing harness rule on account-setting changes, which this ADR does not and cannot override. The operator's "unrestricted access" is read as *access to look*, not a standing grant to mutate the alert set.

---

## §3 — Risk accepted (explicit)

The 2026-06-23 posture was **consequence-driven, not probability-driven**: it refused regardless of odds because the downside is total. That asymmetry is unchanged and is re-stated here so the acceptance is informed, not implicit:

- The TradingView account is the **sole origin** of every c1 entry, add, exit and flat (2026-06-23 Addendum). There is no second signal source; manual execution is retired.
- ToS enforcement against that account — restriction, automation challenge, or ban — **stops all alert delivery**, which stops the rail.
- The 2026-06-23 ADR does **not** quantify this risk for page-level reads, and elsewhere accepts *"non-zero residual ban risk"*. Neither this ADR nor its predecessor can offer a probability; the operator accepts an unquantified, non-zero tail in exchange for agent-executable verification.

**Retained mitigations:** human cadence; read-oriented use; no scripted or looped egress; no unattended sessions; no second account.

---

## §4 — Falsifier (revert trigger)

**H:** If agent browser access to TradingView is exercised under §2 and, over the following 90 days, TradingView issues **no** automation warning, bot challenge, rate-limit, capability restriction or account action, **then** the reversal holds and page-level agent reads are established as low-risk on this account. **Otherwise** — any such signal, or **any alert-delivery failure whose window follows an agent TV session** — this ADR **reverts immediately** to the 2026-06-23 posture, the incident is recorded in `docs/SESSIONS.md` and the RUNBOOK, and re-opening requires a fresh ADR with the incident as evidence.

**Hard check date: 2026-10-25.** Revert is **automatic on trigger**, not on review — the check date exists to close the ADR if nothing fires, not to defer action if something does.

Note the falsifier is deliberately asymmetric: one enforcement signal reverts it; 90 quiet days only *retain* it. Given §3's consequence structure, that is the correct asymmetry.

---

## §5 — Forbidden moves

**Retained verbatim from `2026-06-23` §5 (NOT superseded):**
- **Circumventing the browser safety allowlist** to reach TV through any MCP — the restriction is a safety control; a refusal is an answer, not an obstacle.
- **A second TV account** — independently bannable; shared device/IP/payment/fingerprint can collateral-ban the live account.
- **Uploading private Pine to any third-party compiler/optimizer** — edge-protection doctrine.
- **Treating Path A1 or Path C as viable** — both refuted; re-proposal needs new evidence, not a restated plan.

**New under this ADR:**
- **Mutating alerts without per-action operator confirmation** (§2.3) — reads are granted; writes are not.
- **Scripted, looped or unattended TV automation** — the grant is for human-cadence, operator-directed work. A polling loop against TV is the shape the 2026-06-23 risk model was actually about.
- **Treating a tool refusal as a problem to engineer around** — report it and stop.
- **Citing this ADR to reopen backtest egress** — §2.2 is explicit that egress stays closed on technical grounds and that manual export remains the sanctioned default.
- **Agent TV access during the live signal window (13:00–17:00 UTC) unattended** — attended is fine; unattended is not, because that is when alert delivery is in flight.

---

## §6 — Consequences

**Positive:** the B7 Stage-1 TV pre-flight becomes agent-checkable, removing the last blind spot from an otherwise fully-verified pre-flight; TV-side debugging of alert-delivery failures (the 2026-07-21 miss class) no longer requires an operator round-trip.

**Negative / accepted:** an unquantified non-zero enforcement tail on the account that is the rail's sole signal origin (§3). The 2026-06-23 ADR's reasoning for refusing this is not rebutted here — it is **overridden by operator election**, with §4 as the tripwire.

**Neutral:** no change to egress policy, the locked book, sizing, `dd_protection`, Pine, or any rail surface.

---

## §10 — Audit hooks (runnable)

```bash
# 1. The retained bullets really are retained (this ADR must not have quietly dropped them).
grep -n "Circumventing the browser safety allowlist\|second TV account\|private Pine" \
  docs/adr/2026-07-27-tv-agent-browser-access.md

# 2. The predecessor records the partial supersede, and its Addendum re-points the dead §1 chain.
grep -n "Superseded-in-part-by\|Addendum 2026-07-27" \
  docs/adr/2026-06-23-tv-backtest-egress-automation.md

# 3. Egress policy unchanged: manual export still the sanctioned default.
grep -n "Manual List-of-Trades export stays the sanctioned default" \
  docs/adr/2026-06-23-tv-backtest-egress-automation.md

# 4. Falsifier is dated and the revert is automatic-on-trigger, not review-gated.
grep -n "2026-10-25\|Revert is \*\*automatic on trigger\*\*" \
  docs/adr/2026-07-27-tv-agent-browser-access.md

# 5. ADR graph consistency (supersede fields parse; index regenerates clean).
python scripts/check_adr_graph.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-27 | Authored on operator directive reversing the agent-access prohibition. Scoped to page-level reads; retains the allowlist-circumvention, second-account and private-Pine bullets; records that the reversal rests on operator risk-acceptance rather than on precedent (§1 premise correction), and that the platform browser control is outside repo authority (§2.1). | Joshua (directive) + Claude Code (Opus 5) |
