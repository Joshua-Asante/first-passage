# Venue-legality re-expression lane for the seven-strategy Select campaign — post-view session bounding admitted under an exogenous trigger — `venue-legality-re-expression`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-09-03 ("I ratify the lane ADR"), before any replacement export existed and therefore before any replacement result could be inspected. The ratification-order requirement in §2 is satisfied on the record.
**Decision date:** 2026-09-03
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** campaign close (seven-strategy `Tradeify_Select_100K` configuration campaign) or the campaign's own retirement, whichever is first
**Authors:** Joshua (direction) + Claude Code (drafter)
**Layer:** methodology + campaign scope. No `dd_protection`, `firm_rules`, allocation, lifecycle, locked Pine, or rail config touched; nothing armed; no venue action; no spend.
**Tier:** full — the record gates whether a class of results is admissible at all, so the ceremony-tiering escalation rule ("ambiguous tier → FULL") applies.

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this record, this session (2026-09-03):

- `core/firm_rules.py` — anchor `d4d1c5e` (2026-09-03). Tradeify re-verification block (articles 10495876 / 10495868 / 10468222 / 10495897 / 12853921 / 12268167, read 2026-07-22): "FLAT DEADLINE is now 16:45 ET regular (was 16:59); 12:59 ET holiday-short unchanged; auto-flatten still explicitly NON-FATAL. **No field models it — documentation-only**." Also the hedging / correlated-products rule: opposing directions within a Product Group are prohibited in one account **and across accounts**, the Equity Index group being ES/MES/NQ/MNQ/YM/MYM/RTY/M2K/EMD/NKD plus EUREX index. `Tradeify_Select_100K`: `micro_contract_cap` 80, `cost_per_side_usd` 0.91, `weekend_holds` False ("firm-wide 16:45 ET auto-flatten").
- `ops/prop_envelope_default.md` — anchor `e4962f7` (2026-08-29). §1 E1: Tradeify **16:45 ET / 12:59 ET holiday-short**, primary-verified 2026-07-13 and corrected 2026-07-22 from 16:59. E1's design consequence is explicit: "**never design to the auto-flatten as a backstop**." §2.1: the *research expression* and the *deployable expression* are always distinguished, and a brief "must pre-register the deployable decomposition" — the existing doctrine this record leans on.
- `lab/research_utils/trade_reconciliation.py` — anchor `98e82b2` (2026-09-03). `_deadline_timestamps` builds the day's deadline as `12:59` when the date is in `early_close_dates` else `16:45`, localised to `America/New_York` with `ambiguous="raise"` / `nonexistent="raise"`, and flags when **`entry < deadline <= exit_`**. An exit filled *exactly at* the deadline instant is therefore a `FORCE_FLAT_VIOLATION`; only a fill strictly before it is legal.
- `docs/superpowers/plans/2026-09-02-seven-strategy-tradeify-select-configuration.md` — anchor `73c97cf` (2026-09-03). §Objective: the campaign uses "the seven supplied strategies **without changing their signal rules after results are viewed**." §Phase 6: "**No failed candidate is repaired by changing a strategy's signal parameters inside this campaign.**" These are the two clauses this record amends, narrowly.
- `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/phase1_config.json` — anchor `ca6748a` (2026-09-03). The three affected declared sessions and bar sizes: `orb_mnq_recon_v7` 15-minute, `09:15-16:55 America/New_York`; `vanguard_mgc_v04` 15-minute, `09:00-16:59 America/New_York`; `aegis_6j1` 15-minute, `10:00-13:45 America/New_York, Mon-Wed; force-flat 16:30 America/New_York`.
- `docs/adr/2026-08-08-adr-ceremony-tiering.md` — anchor `e4962f7` (2026-08-29). "Ambiguous tier → FULL"; a light record later found to gate a full-tier matter is superseded, never padded. Tier chosen accordingly.
- `docs/methodology/inqhiori-canon.md` — anchor `9c89dfa` (2026-08-31). §15 Rule 2 (budget before acting); an iteration is one complete attempt-and-check cycle. Each replacement's Phase 1 pass consumes iterations and is counted, not exempt.

**Post-ratification source reads (2026-09-03, after the operator supplied the five Pine bodies).** These confirm §1's
table and **refute** one hypothesis this record relied on:

- `aegis_6J1.pine` — its EOD block fires `eod_zone` at 16:30 ET and the script does not set `process_orders_on_close`,
  so the close fills at the next bar's open, 16:45 ET. Its header documents this as a deliberate 14-minute buffer
  against **Bulenox's** 15:59 CT (16:59 ET) deadline. Its filters already resolve through an explicit
  `America/New_York` input — deviation [1] in its own header, added precisely to avoid the exchange-timezone shift.
  **The timezone diagnosis in the campaign artifact was therefore wrong and is corrected there.**
- `Vanguard_Gold_MGC_v0.4.pine` — `lastSafeBar` backs off exactly one bar from a **16:59 ET** deadline input, firing
  16:30 and filling 16:45. Its header's STILL OPEN list already states "Holiday-short calendar (early-close days) not
  modeled".
- `orb_mnq_7_reconstruction.pine` — `sessEndM` 55 makes `lastBarOfSession` the bar opening 16:45, and
  `process_orders_on_close=true` records the flat on that bar. Its own tooltip already anticipated the fix: "Tradeify
  auto-flattens 16:45 ET regular … set 30 for a venue-faithful paper run." It also already cancels its resting stop
  entries at the session-end bar.
- Both Striker bodies — `calcSize` sizes from a **static `accountSize` input (100000)**, not `strategy.equity`, and both
  set `margin_long=0, margin_short=0`. Their EOD fires 15:45 ET for a 16:00 fill, which is why neither carries a
  force-flat flag. Their day soft-stop, however, is anchored to `strategy.initial_capital` and is **not** gated by
  `backtestMode`.

**Consequence for this lane.** The permitted change (§2.2) is confirmed to be a one-input edit in each of the three
bodies, not a rewrite: the scripts already contain correct, timezone-aware, deadline-parameterised flatten machinery
pointed at the wrong deadline. That is the narrowest possible form of the change this record authorises.

---

## §1 — Context

The Phase 1 venue audit (PR #283, gate verdict `NEEDS_CONTEXT`) measured how many trades in each supplied
export span the venue's daily force-flat instant:

| Strategy | Deadline-spanning trades | Declared session (config) | Diagnosis |
|---|---|---|---|
| `orb_mnq_recon_v7` | **310 / 681** | `09:15-16:55` ET | session runs **10 minutes past** the 16:45 ET deadline — structural |
| `vanguard_mgc_v04` | **226 / 343** | `09:00-16:59` ET | session runs **14 minutes past** the deadline — structural |
| `aegis_6j1` | **9 / 122** | `10:00-13:45` ET, force-flat 16:30 ET | session ends three hours before the deadline and the Pine already declares its own flatten, so the 9 are an **implementation defect**, not a design choice |

As exported, those three cannot pass Phase 2: the plan makes a venue flag a block on that strategy, never a
tuning opportunity. The operator's D11 election is to re-express rather than drop.

**The tension this record resolves.** Re-expression is a post-view change: the audit results were seen
before the decision to change the strategies was taken. Read literally, the plan's Objective clause and its
Phase 6 no-repair clause forbid it, and repeating Phase 1 on the replacement does not cure the post-view
selection. Codex raised this on PR #284 (round 4, P1) and it verified against the plan. Without an explicit,
dated amendment the replacement results would be inadmissible — and an amendment written *after* the
replacement results were inspected would be worthless.

---

## §2 — Decision

A **venue-legality re-expression lane** is admitted inside this campaign, bounded as follows.

1. **Trigger is exogenous and named.** The lane may be entered for a strategy **only** on a venue-legality
   flag raised by the Phase 1 audit — a `FORCE_FLAT_VIOLATION`, a weekend/overnight hold, or a
   contract-cap breach. It may **never** be entered on a performance result: not net P&L, win rate, profit
   factor, drawdown, Sharpe, bust probability, or any ranking derived from them.
2. **The permitted change is the session bound and nothing else.** A re-expression may add or tighten an
   entry cut-off and a forced flatten so that every exit fills strictly before the venue deadline. Every
   other parameter — entry logic, stop, target, ATR, trail, break-even, risk percent, pyramid, day-of-week
   filter, instrument, bar size — is carried across **byte-identical in intent** and re-verified by diff.
   The permitted edit is specified in
   [`2026-09-03-venue-bound-session-guard.md`](../superpowers/specs/2026-09-03-venue-bound-session-guard.md).
3. **A replacement is a new expression, not a repaired one.** It gets a new strategy id, a new Pine filename,
   its own hash pin, and a fresh config entry. The superseded entry is retained as a
   `superseded_sources` record carrying its hash, filename and the flag that retired it. No verdict, anchor,
   or result transfers from the original to the replacement.
4. **The replacement's export is development data.** It is produced by the operator on the whole span and
   is viewed, so it carries the same whole-export ruling as the original set: model-fitted, never
   out-of-sample, and the `EXPLORATORY` claim class stands.
5. **The full Phase 1 gate reapplies.** Each replacement passes G1.1–G1.10 on the replaced set, with its own
   inventory, reconciliation anchors, per-row hashes, byte sizes and venue audit. The twelve-item delta read
   covers the current exports only and never a replacement.
6. **The original stays retired either way.** If a replacement fails the gate or is not produced, the
   strategy is **dropped**; the venue-illegal export never advances as it stands.

**Ratification order is load-bearing.** This record must be `Accepted` **before** any replacement export's
results are inspected — by the operator, the orchestrator, or any worker. Inspecting first and ratifying
afterwards voids the lane and the affected strategies drop.

---

## §3 — Why this is not result-laundering

- **The constraint pre-dates the results.** Tradeify's 16:45 ET deadline has been encoded in
  `ops/prop_envelope_default.md` since the 2026-07-13 ratification and re-verified into `core/firm_rules.py`
  on 2026-07-22, six weeks before these exports existed. The audit revealed a violation of a **known,
  written, exogenous** rule; it did not discover a preference.
- **The trigger carries no performance information.** A deadline-spanning trade count is a legality fact
  about the session clock. Nothing in the trigger ranks the strategies or tells the operator which one to
  keep, so entering the lane cannot select on edge.
- **The direction of the change is forced, not chosen.** There is exactly one compliant session bound per
  strategy given its bar size, and it is written down in advance in the spec. There is no free parameter to
  search over, hence no multiplicity to correct and no `K` to charge.
- **The doctrine already distinguishes these two objects.** `prop_envelope_default.md` §2.1 requires every
  brief to carry both a research expression and a deployable, E1-compliant decomposition. The lane is that
  decomposition arriving late for three strategies, not a new licence.
- **The cost is paid, not waived.** A re-expressed strategy loses whatever edge lived in the forfeited
  session minutes, and E1's design consequence says so plainly: overnight and late-session components of an
  edge are forfeited under the envelope. If the strategy only worked past 16:45, the re-expression will show
  it, and the gate will drop it.

What would make it laundering, and is therefore forbidden below: re-expressing because a result was
disliked, tuning anything beyond the session bound, or re-running until a replacement scores well.

---

## §4 — Forbidden moves

- Entering the lane on any performance result, or on a hunch, rather than a named venue flag.
- Changing any parameter other than the entry cut-off and the forced flatten.
- Producing more than **one** replacement per strategy. A second attempt at the same strategy is a search
  over session bounds and is void; the strategy drops instead. ⚠ **The count starts at the first export taken
  against the VERIFIED D12 early-close calendar.** An export run against the interim placeholder list is not a
  replacement at all and must not be produced; the one-attempt rule must never be satisfied by a body whose
  holiday dates were known-unverified, or the rule would consume the single attempt on a configuration nobody
  intended to test. **The clock starts 2026-09-03**, with the re-pointed bodies below.
- ~~**Exporting any of the three before the verified per-product-group early-close calendar replaces the interim
  list.**~~ **DISCHARGED 2026-09-03 — the calendar is landed and the three bodies are re-pointed; exporting is
  permitted from this date.** The prohibition stood because the interim list was carried over from
  `aegis_6J1.pine`, an **FX** body, while MGC is COMEX metals and ORB is CME equity index, and D12 records that
  the three groups keep different holiday sessions. The research bore that out — on an ordinary US federal
  holiday equity index closes 13:00 ET, metals 14:30 ET, and FX often not at all — but it also showed the fix is
  **not** a per-product-group list. Tradeify's 12:59 ET holiday-short deadline is a blanket account-level rule,
  so the correct construction is the **union** over the three groups, identical in every body; a per-group list
  would omit ordinary federal holidays from the FX body and leave 6J resting past the deadline. All three bodies
  now carry the same 75-date union list owned by
  [`ops/calendars/cme_holiday_calendar_2022_2026.json`](../../ops/calendars/cme_holiday_calendar_2022_2026.json).
  ⚠ **Two conditions ride with the discharge.** (1) The calendar's provenance is **SECONDARY** — no CME primary
  source was reachable — so a replacement export inherits a `NEEDS_CONTEXT` provenance cap it cannot clear on its
  own; that is a cap on the *verdict*, not a bar on the *export*. (2) Three dates close **before** 12:59 ET
  (2023-04-07, 2026-04-03, 2025-01-09) and no deadline can express them; Aegis 6J is the live exposure, trading
  to 11:15 ET on both Good Fridays. Those need a no-trade block, and a replacement that silently relies on the
  deadline there is not venue-legal. See the campaign-state artifact §12.
- Carrying the original expression's Phase 1 verdict, reconciliation anchors, or TradingView summary
  anchors onto the replacement.
- Inspecting replacement results before this record is `Accepted`.
- Using the lane for the two dropped Q-TXG-1 swap-port exports (D10 (ii)). Those were dropped for a sizing
  defect, not a venue flag, and a mis-sized export is not re-expressible — it is re-runnable only with the
  point-value input corrected, which is a different matter requiring its own ruling.
- Treating the venue's auto-flatten as the backstop that makes a late exit acceptable
  (`prop_envelope_default.md` §1 E1, verbatim).

---

## §5 — Gate

Binary, per replacement strategy, evaluated at the Phase 1 re-read:

```
PASS   iff  FORCE_FLAT_VIOLATION count == 0
      and  friday_to_sunday_holds == 0
      and  the diff matches the applied-edit table in the guard spec §8 exactly —
           the deadline input(s), the strategy title, and (MGC/ORB only) the added
           early-close calendar block; nothing else
      and  G1.1–G1.10 otherwise clear on the replaced set
DROP   otherwise
```

A replacement that still flags on the deadline has not been bounded correctly and does not get a third
attempt: the strategy drops.

---

## §6 — Falsifier

**H:** the lane changes venue legality without changing edge selection — every replacement differs from its
predecessor by exactly the prescribed session bound, and by nothing that could have been chosen from a result.

⚠ **The falsifier tests process compliance, not economic outcome** (corrected 2026-09-03 after Codex's review of
[#289](https://github.com/Joshua-Asante/first-passage/pull/289), accepted). An earlier draft would have counted
any change in the strategies' net-P&L *ranking* as falsification. That was wrong: the deadline bites the three
strategies by wildly different amounts — 310 of 681 ORB-MNQ trades against 9 of 122 for Aegis — so a legitimate,
pre-declared, uniformly-applied cutoff is *expected* to reorder them. Rejecting a replacement because its
predeclared edit had the economic effect it was always going to have would reject valid work for the wrong reason.

**FALSIFIED if:** any replacement's session bound differs from the one the spec prescribes for its bar size,
**or** its diff against the superseded body touches anything beyond what the guard spec §8 table records for that
script, **or** any frozen re-export setting (date range, chart, timeframe, initial capital, commission,
slippage, pyramiding, detalization, DEEP) differs from the superseded export's, **or** a second replacement is
produced for any strategy.

**RESOLVED at:** the Phase 1 re-read of the replaced set, if every replacement passes §5 and each diff and
settings comparison comes back clean.

**AMBIGUOUS** (extend to Phase 2) if a re-export setting cannot be recovered from the superseded export, since
the comparison then rests on recollection rather than record.

---

## §7 — Consequences

- The campaign's Phase 1 population becomes: two unchanged strategies (`striker_dj30_mym_pyramid_250`,
  `striker_nas100_mnq_dow_wed_excluded`), up to three replacements, two provenance-only `dropped_sources`
  records, and up to three `superseded_sources` records.
- Contract item 14's per-template contract count stays **five** — a replacement is a cell of the same
  template as the body it supersedes, not a sixth template.
- Rule 2: each replacement's Phase 1 cycle is a counted iteration against constituent (i) of contract
  item 13. It is not exempt, and the ≤8 ceiling is unchanged.
- The `EXPLORATORY` claim class and the whole-export development-data ruling are unchanged.
