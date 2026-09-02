# Pre-Q — 08-08 packet pre-triage: prune the quarterly slate to a decidable set
**Status:** **RATIFIED 2026-07-12 (operator).** Owed §0 reads discharged; classification verified + corrected against source, then operator-adjudicated. The 08-08 decisions themselves remain operator GO/NO-GO at the gate. Ratification record: §2.6.

> **Living-board supersessions (2026-07-22/23 — do not aim 08-08 from the body alone):**
> - **A2 · D2** — **DISCHARGED 2026-07-22 by retirement** (not re-derivation). Pepperstone released from successor-diagnostic duty; quarterly C2→C0 check **RETIRED**. See rescope ADR §Addendum 2026-07-22. **Off the 08-08 slate.**
> - **C1 · C2→C0 regime check** — **RETIRED** with D2; do not run as an 08-08 obligation.
> - **`ACTIVE_FIRM` stays FXIFY** (§1) — **superseded** Phase 1 → live default `Tradeify_Select_100K`; historical MC pins `FIRM_RULES["FXIFY"]` by name.
> - **D1 critical-path claim** (§1 caveat linking D2→11-08) — **moot**: D1/Q-SFRISK-1 closed 2026-07-15; D2 retired 2026-07-22.
> Canonical forward board: [`STATE.md`](../../../STATE.md) (last curated 2026-07-23).

**Loop of record:** STRATEGIC
**D-S-A domain:** meta-process (Delete against the review slate/calendar — explicit **no-cascade**: this brief authorizes no data-corpus deletion and no finding disposition; items pruned are rescheduled or reclassified, never adjudicated by omission)
**Authored:** 2026-07-12 · **Must land before:** 2026-08-01 (one full session ahead of the gate)
**Related:** `STATE.md` forward-trigger board; `docs/methodology/strategy_lifecycle.md`; [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../../adr/2026-07-11-challenge-era-claims-rescope.md); [`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](../../adr/2026-07-12-prop-portfolio-four-friendly-firms.md); [`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md); [`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md); [`docs/notes/notice/N-2026-07-11-terminal-standing-displaces-portfolio-action.md`](../../notes/notice/N-2026-07-11-terminal-standing-displaces-portfolio-action.md)
**Verification:** classification checked by an adversarially-verified 10-agent workflow (2026-07-12) — 4 owed reads, 3 new-artifact confirmations, 1 bidirectional STATE↔class audit, 2 adversarial passes. Corrections applied are logged in §2.5.

---
## §0 — Rule-0 reads (all discharged 2026-07-12)
**Read earlier this session (parent):** `STATE.md` (full); `docs/SESSIONS.md` (top 8 entries); `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`; `docs/methodology/strategy_lifecycle.md` (Calls 1–5); the rescope ADR (§4/§5); `PIPELINES.md` (full); `docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md` (full, git `0e26a7b`, **merged to main**); `ops/prop_envelope_default.md` (full, git `802ee60`); `ops/instruments/6J.md` (full — B2 substantiation + the stale rail line); `core/firm_rules.py` (registry — `AUTOMATION_FRIENDLY_PROP_FIRMS` confirmed landed); `tests/core/test_automation_friendly_prop_firms.py`.

**Owed reads — now DISCHARGED (were flagged, not skipped; §3 was gated on these):**
- **[`docs/adr/2026-05-11-objective-map-section-4-tighten-falsifier.md`](../../adr/2026-05-11-objective-map-section-4-tighten-falsifier.md)** (git `31110f5`, 2026-05-13). ✅ Confirms the **Q7-close audit hook is dated 2026-07-19** and is a one-shot precursor, **OFF the 08-08 slate** (not silently folded). **Two caveats now carried (§2 Off-slate row):** the ADR Status is still `Proposed` (never flipped to Accepted), and the hook counts metrics in the **Notion Objective-Map Registry, which was retired 2026-06-12** — so whether the 2026-07-19 hook can fire against a live Registry is itself an open question. Q7 is ~1 week out (nearer than the slate).
- **[`docs/notes/notice/N-2026-07-11-terminal-standing-displaces-portfolio-action.md`](../../notes/notice/N-2026-07-11-terminal-standing-displaces-portfolio-action.md)** (git `c7f8990`, 2026-07-11). ✅ §10 hook text + graduation criteria extracted. **Result contradicts the draft's A5 placement → reclassified A→C** (§2.5 correction #1). Verbatim §5: *"Re-check date: 2026-08-08 (rides the existing quarterly regime check and its `accept-beta` fork — the same review Q-DECAY-1 feeds)."* The date is **inherited, not load-bearing**; fire log is empty; neither terminal branch (graduate on ≥1 fire / drop after 2 quiet windows) can fire at the first window.
- **[`docs/adr/2026-07-03-hardcore-p3-compounding-ceiling-amendment.md`](../../adr/2026-07-03-hardcore-p3-compounding-ceiling-amendment.md)** (git `a5de124`) and **[`…-p4-tail-survival-gate.md`](../../adr/2026-07-03-hardcore-p4-tail-survival-gate.md)** (git `f2be990`). ✅ **P3 "Kill-D" = Class C confirmed** (standing documentary check; 08-08 explicitly non-load-bearing; existence bar dormant under R6). **P4 = Class C confirmed but rationale CORRECTED** — P4 is **not** a historical-semantics diagnostic like C1; it is a *dependent reading of the KEPT, still-live bust/p99-DD regime falsifier* (the 06-07 HOLD §4 limb-2), and its substance is delegated to A2/D2 (§2.5 correction #4).

**§3 is now unblocked** — all three owed reads landed and their findings are folded into §2.

---
## §1 — Context
`STATE.md`'s forward-trigger board routes many distinct obligations to 2026-08-08 by default — most because "park it to the quarterly" was the cheapest disposition at each individual closure, not because the date is load-bearing for that item. Cheap dispositions compound into one overloaded session. An overloaded review does not produce careful decisions; it produces two or three, and the rest become rubber-stamps indistinguishable, in the record, from ratifications — `programme-audit`'s degeneration signal #4 ("methodology invoked to rationalize a decision already made; tell: the disposition is written before the evidence is assembled").

### What changed today (2026-07-12), verified
Two artifacts landed **on main** and reshape this packet:
1. **[`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md`](../../adr/2026-07-12-prop-portfolio-four-friendly-firms.md)** (`Accepted`, git `0e26a7b`) reopens futures-prop — **not** by reversing R6 (the locked book's fan-out stays NO-GO; DJ30→MYM and NAS100 falsifiers stand), but by authorizing a **new, greenfield discover → productionalize → execute program** at four attended-automation firms (Bulenox, Tradeify, MyFundedFutures, BluSky), fed by the same Gen-2 pipeline DISC-CAMP-0 sits inside. Rail build + account registration **remain gated**; `ACTIVE_FIRM` stays FXIFY. *(Body historical as of 2026-07-12; `ACTIVE_FIRM` live default is now `Tradeify_Select_100K` — substrate Phase 1 2026-07-22; see living-board supersessions banner above.)*
2. Its constraint set, **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md)** (git `802ee60`), is seeded and already the scoring target for candidates (verified: Q-HARV-0 was scored against it) but remains **PROVISIONAL v0.1** — its §5 lists five open items (E1 deadline print, E2 checkpoint semantics, E7 default-vs-overlay, ETF policy, the ratifying ADR).

### The load-bearing finding: a resource collision at 2026-11-08 (CONFIRMED)
| Obligation | Owner | Miss consequence |
|---|---|---|
| Successor self-funded risk-framework Pre-Q | Rescope ADR **§4 completion falsifier** (audit note §5.2 / D1) | Escalates to a **mandatory blocker on Aegis→M6J go-live** |
| Prop-portfolio primary falsifier — ≥1 pre-registered candidate clears the bust ceiling on ≥2 of 4 `FRIENDLY` firm tiers | Four-firms ADR **§4** | Demotes the entire prop program to **research-only** |

Both hard-date to **2026-11-08** (verbatim-confirmed in both ADRs; the four-firms ADR §4 schedule literally tags 11-08 "hard date for primary falsifier"). Both draw on the same scarce inputs — operator Fri/Sun hours, Cursor/CC bandwidth, and (for the second) Gen-2 discovery throughput, currently frozen behind the DISC-CAMP-0 unblock. Every hour 08-08 spends on ceremonial re-ratification is an hour not spent closing that gap before 11-08. This is the strongest argument for pruning now.

**Two caveats the verification added (both sharpen, not weaken, the argument):**
- **The prune must be SELECTIVE, not wholesale.** Audit item **D2 (Class A2) is scheduled AT 08-08 and is on the critical path to the 11-08 D1 obligation** — D1's successor risk-framework depends on the D2 successor criterion. "Buys runway" holds only if the prune preserves the D1/D2 chain (and the two hard-date programs) while shedding genuinely lower-priority 08-08 load. A blanket 08-08 prune would *hurt* the 11-08 deadline.
- **The collision is currently invisible from STATE.md alone.** STATE's forward board registers the D1 half but **omits the prop-portfolio 11-08 falsifier entirely** — it is only visible by juxtaposing the two ADRs. This is a genuine bookkeeping skew, fixed this session in the same pass as this brief (STATE.md forward board updated 2026-07-12; §2.5 note S).

---
## §2 — The slate, classified (verified)
Test for every item: **what does 2026-08-08 supply that no other date supplies?**

### Class A — MUST-DECIDE at 08-08 (the date is load-bearing)
| Item | Why the date is load-bearing | Decidability at 08-08 |
|---|---|---|
| **A1 · Accept-beta fork** (Q-DECAY-1 cost × Q-PERSIST-1 probability) | Both paired closures route here; the decompound HOLD has ridden two quarters — a third park is the "HOLD dying quietly" the R6 ADR forbids | **Fully decidable** — a synthesis of two *closed* analyses; no live data required. The one unambiguous decision on the slate. |
| **A2 · D2** — `dd_protection` objective re-derivation | The rescope retired the *question* C2 was tuned to answer; every quarter it runs un-re-derived is risk control aimed at nothing. **On the critical path to the 11-08 D1 deadline** | **Decidable-to-OPEN only.** Scope/frame D2 at 08-08; resolution is gated on the 11-08 successor Pre-Q (numbers-before-question forbidden). Constants stay frozen until then. |
| **A3 · Lifecycle Calls 1 & 4 first eval** | Must **exercise** the AMBIGUOUS clause, not skip it — skipping silently converts "provisional-until-data" into "never evaluated" | **Exercise-and-record, expect no decision.** Call 1 → AMBIGUOUS (live PF below min trade count; feeds unbuilt) → re-confirm 11-08. **Call 4 → vacuous 0/4** (every leg off-venue ⇒ WATCH count 0 by construction) — **record the null explicitly; STATE currently carries no provisional caveat for Call 4 (added this session).** |
| **A4 · Q-HARV-0 buy-positioning-data fork** *(promoted from orphan)* | The AMBIGUOUS close (+19.2 bp, p=0.013, placebo clause proven structurally un-passable) upgrades the fork to *"flow data adjudicates crowded-expression vs mechanism-death, which price data cannot"* — a data-procurement **decision**, structurally a sibling of A1 | **Decidable** — a qualitative adjudication fed at 08-08, no code run. Was an orphan in the draft (folded into C4, which covers only the parked successor pre-Q); it is a decision fork, not a status item. |
| **A5 · Decompound-HOLD §4 limb-2 regime re-MC** *(added — was silently folded into A1)* | A **live** config-falsifier: run `regime_gate.py` on the trailing-6-month panel at the locked config; **p99 DD ≥5% OR bust ≥1% ⇒ HOLD FALSIFIED** → open a regime-adaptive-sizing Pre-Q **+ interim 55% haircut on all four allocations**. Distinct harness/criterion/action from C1's pass-rate check; runs *alongside* it | **Run-and-branch.** Shallow ratify if no breach; **operator must-decide GO/NO-GO on the 55% haircut if it breaches.** Its result is the shared input that A1 pairs with and that C5 (P4) reads. Highest-stakes possible outcome on the slate (a live allocation change). |

**Evidence to pre-assemble (Class A):** A1 — both closures' §Re-check hooks (~11.7% conditional-on-kill median DD; +0.46pp bust understatement, decompounded-panel basis). A2 — rescope ADR §4 + audit §5.2; current C2 (1.5%/0.40×) provenance. A3 — live trade count (≈zero fills anywhere); expected AMBIGUOUS/vacuous, recorded not silently re-parked. A4 — Q-HARV-0 RESULTS.md + closure note (crowded-expression vs mechanism-death framing). A5 — `docs/adr/2026-06-07-decompound-remc-hold.md` §4 (limb-2 gate + k≈0.55 mitigation); the trailing-6-month panel.

### Class B — DECIDE EARLY (before 08-08; the date is arbitrary, the item blocks *now*)
| Item | Why it can't wait | Action / home |
|---|---|---|
| **B1 · `ops/prop_envelope_default.md` → v1.0 ratification** | DISC-CAMP-0 survivors must declare `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` against this file per four-firms ADR §2 step 1. Scoring against a **PROVISIONAL** target risks a wasted verdict if E1/E2/E7 shift at ratification | One short ADR: lock §1's E1–E7; resolve §5's open items. **Now registered on the STATE forward board (was absent).** |
| **B2 · Aegis→6J owed items** (commission-schedule lookup, EOD-OFF run, H-PARITY, Pine-header staleness, **stale rail-blocker line**) | Small, mechanical, no quarterly dependency. The stale line in `ops/instruments/6J.md:43` — *"TradersPost→Bulenox routing… residual program R3… No live-chain work on 6J until R3 closes"* — is doubly dead: the KEEP rail is now TV→CrossTrade→NT8 (TradersPost rejected, corrected in PIPELINES.md P5), and R3/the residual program **closed** under R6. It will mislead the next session | Operator-run per `6J.md`'s own ACTIVE/OPEN list. **Correctly homed in the instrument ledger, NOT STATE** — this is why the STATE-scoped audit hook can't see it (expected, not a skew). Pine-header fix stays deferred to the v0.4 authoring pass (do not re-pin the hash). |
| **B3 · Multiplier-spine forward-relevance flag** | A scoping question (does the account-multiplier layer still matter given 6J sizing reality / J5's effective-risk finding), answerable independently of quarterly cadence | Decide alongside the 6J items. **Was registered only in a SESSIONS Open/next — now added to the STATE forward board.** |

### Class C — RATIFY-OR-SLIP (quarterly cadence is fine; keep shallow, mechanical)
| Item | Disposition |
|---|---|
| **C1 · C2→C0 regime check** | Run `time_to_pass.py --regime-check` — **historical-semantics diagnostic only** (challenge-denominated; venue closed). Record, don't deliberate. *Distinct harness from A5* — do not conflate. |
| **C2 · Q-USOIL-1 revisit** | Prior park re-confirmed 07-10; expect a 2-minute re-confirmation absent new evidence. |
| **C3 · T2/T3/T4 R&D tooling gaps** | Status check, not a decision — report % complete. *(Note: the T4 rolling-PF σ-harness + tier-demotion state writer is the same undelivered artifact A3/Call-1 waits on — one item, two homes.)* |
| **C4 · HARV successor pre-Q / lane ADR** | Gated on DISC-CAMP-0 landing regardless of 08-08 — likely **not ready**; record and move on. Covers only the parked successor pre-Q + lane ADR (STATE L179b/L183); the **flow-data fork is A4**, not here. |
| **C5 · P4 verdict** | Shallow ratify-or-slip. **Corrected rationale:** P4 is a *dependent reading of the KEPT, still-live regime falsifier* (the 06-07 HOLD §4 limb-2 = item A5), **not** a historical-semantics diagnostic like C1. Its substance is delegated to A2/D2. Read as "HOLD stands / tail-survival remains regime-conditional; live successor-criterion work is A2/D2." Not a futures existence-bar (07-10 SESSIONS). |
| **C6 · P3 Kill-D** | **RESOLVED — Class C** (no longer pending). Standing documentary check; 08-08 non-load-bearing; existence bar dormant under R6. Watch-item (not a reclassification): if Kill-D ever runs live, its comparator `R_alt` must recompute against the currently-active lane (Aegis→M6J), since its named fork (Guardian-MGC) is itself parked. |
| **C7 · Four-firms ADR quarterly check-in** | One-line status note. 08-08 is a **progress check**; the hard falsifier is 11-08 (§1). **Now registered on the STATE forward board (was absent).** |

### Off-slate — explicitly listed so it is visibly NOT-folded, not merely absent
| Item | Disposition |
|---|---|
| **Objective-Map Q7-close audit hook** | **2026-07-19** (≈1 week out — *nearer* than the slate, easy to miss). One-shot precursor, not a quarterly item. **Caveats:** ADR status still `Proposed`; the Notion Objective-Map Registry it counts against was retired 2026-06-12, so its fireability is itself open. Owned by `docs/adr/2026-05-11-objective-map-section-4-tighten-falsifier.md`. Siblings Q8-close (2026-10-19) and Pre-Q12 (2027-10-19) likewise off-slate. **→ RETIRED 2026-07-12 (operator decision, post-ratification annotation — not a slate change; the fireability caveat resolved by retiring the whole hook family incl. both siblings; see the ADR's retirement addendum).** |

---
## §2.5 — Corrections applied from the owed reads + bidirectional audit
The draft's classification was verified against source; the following changed. Each is grounded in a dated read (§0) or the 2026-07-12 audit.

1. **A5 → C (reclassify).** The Notice N-2026-07-11 re-check is not date-load-bearing: its 08-08 date *rides* the quarterly regime check, its fire log is empty, and neither terminal branch can fire at the first window. It belongs in ratify-or-slip. *(Owed read: Notice §4/§5/§10.)*
2. **A4 "Medallion two-tier rigor ratification" → DROPPED as a phantom.** Verified: "Medallion" exists in-repo only as the *closed* Q-NEFF-1 many-uncorrelated-edges diversification strand (SESSIONS L107); "two-tier rigor" exists nowhere; the "07-11 draft lesson" it cites *is* the web-advisor lesson that already became Notice N-2026-07-11 (= the old A5); the "reachability rule (ADR 2026-07-12)" is the DSR-K/variance-floor ADR, already `Accepted`/merged (PR #341). A4 carries **no STATE trigger and no open ADR obligation of any shape** — it must not sit in the must-decide class. **Operator note:** if a standing discovery-rigor doctrine was intended, it needs its own anchored obligation + a decidable ratification question; it cannot ride this slate under a name with no referent.
3. **Q-HARV-0 buy-positioning-data fork → PROMOTED to Class A (A4).** It was an orphan in the draft (the one-directional §5 hook, walking top-level STATE bullets, mapped the Q-HARV-0 bullet to C4 via its *sub-item (b)* and silently dropped *sub-item (a)*). It is a data-procurement decision fork, a sibling of A1 — not a shallow status item.
4. **C5 P4 rationale corrected** (placement unchanged). P4 is a dependent reading of the KEPT live bust/p99-DD regime falsifier, not a historical-semantics diagnostic like C1; grouping the two under one "historical-semantics" rationale would wrongly retire P4's live regime-robustness escalation path.
5. **C6 P3 Kill-D resolved** from PENDING → Class C (owed read discharged).
6. **A5 (new) added — decompound-HOLD §4 limb-2 regime re-MC.** The adversarial audit caught that the draft (and the first-pass audit) folded this live, config-falsifying, allocation-haircut-triggering quarterly check into A1 on the word "pairs." It is a distinct 08-08 obligation with its own harness (`regime_gate.py`), criterion (p99 DD ≥5% OR bust ≥1%), and action (55% haircut + Pre-Q). Its result is the shared input A1 pairs with and C5 reads.
7. **Decidability caveats added** (A3): STATE flags Call-1's forced-AMBIGUOUS but **not** Call-4's vacuous-0/4 — added so the slate does not present four "decisions" when only A1 (and a possible A5 breach / A4 fork) can actually decide.
8. **§5 audit hook made bidirectional** (see §5) — the draft's one-directional hook FAILED: it admitted 5 phantoms into the slate (A4-Medallion + the STATE-absent B1/B3/C7) and dropped 1 orphan + 1 mis-map. Note B2/C6 are correctly-homed elsewhere (ledger / P3 ADR), not skews.

## §2.6 — Ratification record (operator, 2026-07-12)
Operator ratified this classification. Three confirmations recorded:
- **A4 "Medallion two-tier rigor" — DROP confirmed.** Off the slate; no repo referent (§2.5 #2). If a discovery-rigor doctrine is later wanted, it opens as its **own anchored obligation**, not via this slate.
- **Class A membership confirmed** for the two audit-surfaced additions: the **decompound-HOLD §4 limb-2 regime re-MC** (run-and-branch; live 55% haircut on breach) and the **Q-HARV-0 buy-positioning-data fork** (adjudication fork).
- Classification is now **fixed** per §3.1 / §4 — any post-ratification move needs a fresh brief, not an in-session call.

Owed follow-through (this session): SESSIONS.md entries for the four-firms ADR + this pre-triage (Cursor handoff [`docs/ltm/briefs/handoffs/2026-07-12-cursor-handoff-sessions-entry.md`](handoffs/2026-07-12-cursor-handoff-sessions-entry.md)); STATE/CLAUDE skew already repaired (note S).

**S · STATE.md forward-board skew fixed same session:** the obligations that showed as "phantoms" *because STATE never registered them* — the prop-portfolio 08-08 check + 11-08 hard falsifier (C7 / the collision's second half), prop_envelope v1.0 ratification (B1), multiplier-spine forward-relevance (B3), and the decompound §4 regime re-MC (A5) — were added to STATE's forward board on 2026-07-12, plus a dated section for the four-firms program. This is doc-skew repair, not a slate change (no-cascade holds).

**Addendum (2026-07-13) — proposed input to A1 (accept-beta fork), NOT a slate change:** the ratified Stage-8 exposure-companion ADR ([`2026-07-13-stage8-mechanistic-exposure-companion`](../../adr/2026-07-13-stage8-mechanistic-exposure-companion.md) §2c) hands the packet owner a proposed **shock-conditional MC module** for the program-level MC pricing the accept-beta decision: impose an adverse NY-morning gap over a pre-registered grid (e.g. −1% to −5%) on a max-concurrency day, all in-market legs at entry-time sizing, evaluated against per-account rule sets — because stream resampling cannot generate the common-mode event (zero occurrences in the 7-yr panels). Packet owner accepts/rejects at packet assembly; the ADR's own §4 falsifier (first run owed with the 08-08 packet work, hard check 2026-11-08) prices whether the module is material (≥1pp bust-delta anywhere on the grid) or demotes to annotation-only.

---
## §3 — Recommended disposition
1. **This session, before 08-01:** operator ratifies this (now source-verified) classification. The three owed §0 reads have landed; §2.5 lists every change from the draft.
2. **Before 08-08:** close every Class B item (B1 envelope-ratification ADR; B2 6J ledger items; B3 multiplier-spine flag). None require the full quarterly session.
3. **At 08-08:** work Class A only, oldest-riding first (**A1 accept-beta**). Run **A5's regime re-MC early** — its result feeds A1 and C5, and a breach forces a same-session operator GO/NO-GO on the 55% haircut. Budget Class C to one shallow pass at the end. Keep the D1/D2 chain intact (A2 is critical-path to 11-08).
4. **Explicitly log**, don't silently re-park, any Class A item that can't be decided — most likely **A3 Calls 1/4** (AMBIGUOUS / vacuous 0/4 for lack of live data) and **A2/D2** (decidable-to-open only, gated on the 11-08 Pre-Q). Record with a re-confirm date, per the lifecycle ADR §6 clause.

---
## §4 — Forbidden moves (under this brief)
- Treating a Class B resolution — or the 2026-07-12 STATE/CLAUDE doc-skew repair — as license to touch any locked parameter, allocation, `dd_protection` constant, or Pine source. None of them are; the skew fix is pointer/narrative only.
- Using this pre-triage to delete a finding, closure, or evidence artifact — the no-cascade declaration is binding; meta-process Delete here touches the review calendar only.
- Silently dropping a Class A item to Class C because it's inconvenient in-session — classification is fixed at ratification (§3.1); moving an item after the fact needs a fresh brief, not an in-session call.
- Re-admitting A4 "Medallion two-tier rigor" to the slate under its current unanchored name — a real discovery-rigor doctrine needs its own obligation, not this slot.
- Treating A5's regime re-MC as a mere status check — a breach is a live-allocation event, not a ratify-or-slip.

---
## §5 — Audit hook (bidirectional — the draft's one-directional hook FAILED this check)
```bash
# Forward leg (STATE -> class): every STATE.md forward-trigger dated 2026-08-08 maps to exactly one class.
grep -n "2026-08-08\|08-08" STATE.md
grep -n "Class A\|Class B\|Class C\|Off-slate" docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md

# Reverse leg (class -> STATE): every Class A/B/C item is EITHER a STATE 08-08 trigger OR has a named
# canonical home (ledger / ADR / SESSIONS). Any item that is neither is a phantom -> challenge it.
#   Correctly-homed-elsewhere (NOT STATE skews): B2 -> ops/instruments/6J.md ACTIVE/OPEN; C6 -> P3 ADR.
#   Now-registered-in-STATE (were skews, fixed 2026-07-12): B1, B3, C7, A5, the 11-08 prop falsifier.
#   True phantom (no home anywhere): A4-Medallion -> must not appear on the slate.

# Compound-bullet decomposition: STATE L179 (Q-HARV-0) carries TWO 08-08 items -
#   (a) buy-positioning-data fork = A4 ; (b) successor pre-Q = C4. Both must be present.
grep -n "buy-positioning\|successor pre-Q\|fork" STATE.md docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md

# Collision witness: STATE must now register BOTH 11-08 hard dates (D1 successor Pre-Q + prop falsifier).
grep -n "2026-11-08" STATE.md
```
**Expected:** every STATE 08-08 trigger in exactly one class; no orphan (the L179a fork is now A4); no duplicate; no phantom on the slate (A4-Medallion removed); both 11-08 obligations visible in STATE.

## §6 — Verification
```bash
# Discipline checks (mechanical)
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md
# §0 anchors
git log -1 --format='%h %ci' -- docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md   # expect 0e26a7b
git log -1 --format='%h %ci' -- docs/notes/notice/N-2026-07-11-terminal-standing-displaces-portfolio-action.md
# Collision citations
grep -n "hard date for primary falsifier" docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md   # §4 L79
grep -n "2026-11-08" docs/adr/2026-07-11-challenge-era-claims-rescope.md                                # §4 completion falsifier
# A5 consequence
grep -n "p99 DD ≥ 5% OR bust ≥ 1%\|k≈0.55" docs/adr/2026-06-07-decompound-remc-hold.md                 # §4 limb-2 + mitigation
```

## §10 — Forward audit hooks (re-run at ratification, at 08-08, and whenever STATE changes)
```bash
# 1. The phantom must not creep back. "Medallion two-tier rigor" has no repo referent;
#    if it reappears on any slate, it is unanchored ceremony -> reject.
grep -rn "Medallion two-tier\|two-tier rigor" docs/ && echo "PHANTOM PRESENT — investigate" || echo "clean"

# 2. Both 11-08 hard dates must stay visible in STATE (the collision witness).
grep -c "2026-11-08" STATE.md   # expect >= 2 (D1 successor Pre-Q + prop-portfolio primary falsifier)

# 3. The A5 live falsifier must not be silently re-folded into A1. STATE must carry it as its own line.
grep -n "regime_gate\|decompound-HOLD.*§4\|limb-2\|55%" STATE.md

# 4. At 08-08, confirm each Class-A item was worked and any undecidable one was LOGGED (not re-parked):
#    A1 decided; A2/D2 opened (resolution -> 11-08); A3 Calls 1/4 recorded AMBIGUOUS/vacuous-0/4;
#    A4 HARV fork adjudicated; A5 regime re-MC run (+ operator GO/NO-GO if breached).
grep -n "AMBIGUOUS\|vacuous\|re-confirm 2026-11-08" docs/SESSIONS.md   # the 08-08 entry must show the logged nulls

# 5. This brief was actually re-read at the gate (Known Trap #10 — audit hooks that never fire).
#    The 08-08 SESSIONS entry must cite this brief by path.
grep -n "2026-07-12-08-08-packet-pretriage" docs/SESSIONS.md
```

---

## Addendum 2026-08-29 — A1/A5 pairing DECAYED (brief-decay-audit)

Per Rule 14, this addendum lands where the A1/A5 pairing is read (§2 Class A table above, §3
disposition, §10 hook #4). The table, §3, and §10 above are byte-unedited; this is the
correction.

1. **A5 (decompound-HOLD §4 limb-2 regime re-MC) was struck from Class A.**
   [`docs/adr/2026-08-02-pepperstone-feed-retirement.md`](../../adr/2026-08-02-pepperstone-feed-retirement.md)
   §2-B/§2-D struck it outright (Pepperstone feed + CFD venue both retired — the panel A5 read
   is gone). It is now **SUSPENDED-ORPHANED / permanently `NOT_EXECUTABLE`**, per
   [`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md)'s
   own 2026-08-03 addendum — and the **quarterly schedule itself is struck**, not deferred: no
   future 08-08/11-08/02-08/05-08 date carries a live A5 obligation. §2's Class A row and §10
   hook #4 (`grep -n "regime_gate|decompound-HOLD.*§4|limb-2|55%" STATE.md`) can no longer be
   satisfied by a run — only by the ADR's own successor design landing.

2. **A1 (accept-beta fork) is consequently not decided.** With A5 gone, A1 cannot be resolved on
   the Pepperstone-shaped input the pairing assumed, and it is not decided by default either — it
   carries forward as an **open fork**, per the retirement ADR §2-C, no longer paired with a live
   A5 reading. Any future A1 decision must state which venue-native evidence it rests on instead
   (§2-C names candidates: Q-COMPOSE-1 breadth, fork-program exhaustion, ORB-ZB falsification,
   the ORB-MNQ correct-clock scorecard).

3. **The self-declared successor was never linked forward from here, and is itself stale.**
   [`docs/briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md`](2026-07-17-0808-packet-delta-and-sequence.md)
   records the A5 strike and the A1 re-scope in more detail than this brief ever did — but this
   file carries no pointer to it, and that successor brief carries its own 2026-08-06 reader
   intercept flagging that it predates the 2026-08-04 Tradeify venue de-scope and must not be
   treated as a live execution slate without re-walking the board at the gate.

4. **The literal 2026-08-08 date passed, but not via anything this brief adjudicated.** The
   session that actually landed on 2026-08-08 was the 47-ADR-rider Great Prune sweep
   ([`docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md`](../../notes/audits/programme-audit/2026-08-08-quarterly-audit.md)) —
   a rider-discharge audit that never names this brief, A1, A5, or D2 by row. It touches the
   decompound-HOLD limb-2 orphaning only in passing (as one of three gates whose
   unfalsifiability it propagated to, §"Unfalsifiable census"). **Class A/B/C as classified in §2
   above remain formally undischarged under their own terms** — no session ever worked this
   slate as §3 instructed.

**Pointers:** decompound-HOLD ADR addendum —
[`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md)
(§4 banner + §Addendum 2026-08-03); Pepperstone retirement ADR —
[`docs/adr/2026-08-02-pepperstone-feed-retirement.md`](../../adr/2026-08-02-pepperstone-feed-retirement.md)
§2-B/§2-C/§2-D.
