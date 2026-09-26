# Pre-registration: route-native fixed-stop edition of Vanguard MGC for the Tradeify book

**Status:** `DRAFT — NOT FROZEN.` Fields marked **OWED (operator)** must be answered before freeze. Nothing here binds a replay, E1 run or verdict until the Status line reads `FROZEN <date>` and the freeze commit's SHA is recorded in [campaign record §59](../programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25). No replay, E1 dispatch or screen may run on this edition before then.

**Precondition — operator decision not yet made:** the [Vanguard trailing determination](../handoffs/2026-09-26-vanguard-mgc-trailing-determination.md#5-executor-return) returned `TRAILING ACTIVE`, which leaves two options:
- (A) a route-native fixed-stop Vanguard edition under the §59 K = 1 pattern;
- (B) rejecting the Vanguard leg on this route.

This file exists **only for option A**. If the operator chooses B, close this draft unfrozen with a one-line note and open nothing else.

**Owner:** campaign record §59, extended to Vanguard by the operator's option-A ruling (still owed). It follows the ruling 3 step 1 pattern: written before any replay or E1 run on the edition, and not changed afterwards.
**Loop of record:** STRATEGIC. The expression change is forced by the route's capability; K = 1, not a search.
**Authored:** 2026-09-26, Claude Code (drafting, cloud session). The operator owns every OWED rule and the freeze.

**Sibling:** [ORB/Striker editions pre-registration](2026-09-25-tradeify-route-native-editions-prereg.md), also unfrozen. The two files are separate so each keeps its own scope and K accounting. They requalify together in the same production E1 (§6).

---

## §0 — Rule-0 reads (anchors at PR branch `claude/practical-curie-imvz7n`, 2026-09-26)

| Source | What it fixes for this file |
|---|---|
| Campaign record §55 (D-B4 (a)), §59, §60 | The accepted four-leg book at K = 1. §59 ruling 1 recorded Vanguard as fitting the narrowed shape; the determination below shows that premise fails for trailing. §60 governs agent reads of private sources. |
| [Vanguard trailing determination §5](../handoffs/2026-09-26-vanguard-mgc-trailing-determination.md#5-executor-return) | `TRAILING ACTIVE`. Triggered-trail parameters ride on every Vanguard bracket: entry, scale-in and each managed-bar amend. They come from the port's source defaults, because the effective binding has no overrides. Pine agrees. Breakeven and grace are inactive. |
| [REST route assessment §6.5, §6.7](../handoffs/2026-09-25-crosstrade-rest-route-assessment.md#65-per-leg-primitive-map-step-4) | L2(g) triggered trailing is U on this route under both REST and webhooks. The only activated trail available is CrossTrade-managed and not fill-anchored. L2(c) native modify is K (drill D2). |
| `docs/notes/2026-09-10-tradeify-protection-selection.md` | Book settings inherited unchanged: 1% combined trigger, 40% scale, 80-micro capacity, Aegis-priority takeover. Vanguard is zero at every WATCH tier (O-5). |
| Incident ADR 2026-09-17, Addendum 2026-09-24 §A1, §A4 | The narrowed request shape (§2 below) and the per-primitive route table. |
| Rail spec 2026-09-12, R-B3 L-2 and I8 | L2(g) is required by any port whose bracket sets trailing parameters. A substitute expression is a different strategy until requalified. |
| `core/strategies/BOOK_SOURCES.sha256`, `ops/c1_signal_daemon/book_adapters.py:51-55` | Current Vanguard pins: Pine `af26899c…`, port `e6a03d04…`. The edition gets new pins; neither current file is edited. |
| `AGENTS.md` "Public-clone posture" | No Pine source, parameter value or port code appears here. Rules are stated as shapes only. |

The drafting session **did not read** the Vanguard Pine or port; they are not in the cloud clone. Behavioural statements come from the determination return or the public owners above, or are marked OWED. **§3a** adds a later source mapping from a local §60 read, done after drafting.

## §1 — What is pre-registered

Exactly one new venue-edition expression, K = 1:

| Leg | Edition id (venue-edition ledger, `CANDIDATE`) | Replaces, on this route only |
|---|---|---|
| Vanguard MGC | `vanguard_mgc_fixed_stop_oso@Tradeify_Select_100K` | The declared Vanguard expression, whose brackets carry triggered-trail parameters |

**Inherited, not re-selected:** the book's legs and allocations; the protection cell; capacity; takeover order; the WATCH-tier rule; and every Vanguard signal, setup, entry and add-eligibility condition. Only the **order expression** changes: how protection travels with exposure, and how quantity is split into requests.

## §2 — Shape constraints (from incident ADR §A1)

Every exposure-creating request (entry or add) must:
1. be a single market or stop entry for **exactly one contract**;
2. carry its **own native fixed stop in the same request** (CrossTrade `place` with `stop_loss`, which becomes one Tradovate `placeoso`);
3. be sent **without** `delay=`, ATM fields, trailing fields, `cancel_after`, or copier or multi-account fan-out.

A multi-contract intent is sent as that many one-contract requests, each carrying its own stop.

## §3 — Vanguard MGC edition

| # | Rule | Status |
|---|---|---|
| VAN-1 | Entry and scale-in: each request is one contract carrying its fixed protective stop and, where declared, its target, in the same request. No trailing parameters are sent or modelled. | Fixed by §2 |
| VAN-2 | **Fixed stop level at entry.** Is it the declared bracket's existing fixed-stop component, unchanged? The determination found the grace branch inactive, so the declared stop is active from entry. | **OWED (operator)** |
| VAN-3 | **What replaces the trail as an exit.** The declared trail closed some trades. Name the existing exit that now closes them: the fixed stop, the existing target, the timed or scheduled exit, or another existing rule. **No new exit rule is invented here.** If no existing exit covers the case, say so; the edition is then a different strategy needing a fresh decision (§7). | **OWED (operator)** |
| VAN-4 | **Stop and target modification after entry.** The declared port re-issues its bracket on every managed bar. Once trailing is removed, does the edition still amend the fixed stop or target after entry? If yes, it depends on L2(c) native modify, which is K on this route (drill D2) and must be listed as an open route dependency. If no, write "none". | **OWED (operator)** |
| VAN-5 | **One-contract split and adds.** State the maximum contracts per Vanguard signal and per add on this account, including any cap. Each contract is its own request with its own stop. | **OWED (operator)** |
| VAN-6 | **Partial acknowledgement of a split.** Track each of N one-contract requests separately: confirmed fills establish position quantity; accepted-but-unfilled requests remain working orders with their required reservations; conclusively rejected requests follow the accepted release rule; unknown requests retain reservations under the incident ADR. An acknowledgement alone never increments position. Confirm that the edition consumes confirmed fill events and does **not** re-send an unresolved request merely because no fill is observed. For example, two accepted requests with one fill mean one confirmed contract and one working request, not two contracts. The [route note](../../notes/2026-09-25-tradingview-signal-route-evaluation.md) (line 207) records that the add counter advances when an add is proposed, not when it fills; state whether that stays as declared. | **OWED (operator; fill-based position semantics required by book_protocol.py; counter decision remains owed)** |
| VAN-8 | **Exit split.** The port closes the whole position with one market exit (§3a). Under the one-contract rule, state how a multi-contract close is realized: N sequential one-contract closes generated by the rail after admission (not by the port), their order, and how each is resolved. State the replay treatment for sequential closes (same rule as §6, or another stated now). This is a rail dependency, like the entry split, but its semantics are fixed here before freeze. | **OWED (operator)** |
| VAN-7 | Breakeven and grace stay inactive, as in the accepted binding. The edition does not enable them. | Fixed (determination §5) |

## §3a — Source mapping of the OWED rules (local §60 read, 2026-09-26)

A local session read the pinned Vanguard port (`e6a03d04…`) and Pine (`af26899c…`) in place under campaign §60, together with public rail code. It maps what the source already constrains for each OWED rule. **Nothing here answers a rule:** each OWED row still needs the operator's words at freeze. Findings are stated as behaviour; no parameter values appear. Port lines are cited `port:N`, Pine lines `.pine:N`, both from the pinned bodies.

| Rule | What the source constrains | Suggested answer (operator decides) |
|---|---|---|
| VAN-2 | The fixed stop and the target are price levels set once, at the signal bar (`port:244`). With grace inactive, the declared stop is the level sent from entry. Adds carry the same stop and target levels (`port:269`). | "The declared fixed stop, unchanged, sent with each request." |
| VAN-3 | Besides the trail, four exits already exist: the fixed stop, the target limit, a stale exit after the maximum hold (`port:276`, `.pine:508`) and the end-of-day flat (`port:278`, `.pine:512`). The drawdown close (`port:231`, `.pine:383`) is display-only in the pinned backtest mode. The Pine header records that historically the realised exits were the stop and the EOD flat, with the trail capturing gains early; the target's contribution is not isolated (`.pine:30-35`, `:167`). | Existing exits cover every case, so no new rule is needed. Removing the trail is a real behaviour change, and E1 measures its effect. |
| VAN-4 | The port sends a bracket amend on every managed bar (`port:274`). With trailing, breakeven and grace all off, the stop and target never change after entry. The rail compares each amend with the broker-observed bracket (`ops/c1_rail/book_protection_owner.py:594-603`, `book_protection.py:132`): an unchanged bracket becomes `noop` and sends **no broker command** (`unchanged_protection`). The only cost is the protection read that precedes the comparison. | **"None"**: amends continue but never modify at the broker, so L2(c) / drill D2 is not a dependency of this edition. |
| VAN-5 | Base size is risk-based with a contract cap (`port:162-166`); adds are sized from the base, up to a declared number of adds (`port:168-173`). Under protection mode the injected quantity rule can give zero, which means no entry. The port emits one intent per entry or add: **no code in `ops/c1_rail` or the daemon splits a multi-contract intent into one-contract requests today**. The incident ADR's proposed §A8 rules 9–10 place splitting at admission (whole-or-nothing, one unresolved request per symbol). | Confirm the cap as declared. Record the split as a shared rail dependency (see below), not a port change. |
| VAN-6 | Position is the sum of confirmed fills (`port:124-147`), and the port never re-sends. The add counter advances when an add is proposed, not when it fills (`port:271`), which matches the route note. | "Confirm: position comes only from confirmed fill events; nothing is re-sent; counters as declared." |

**Rail dependencies this edition shares with the ORB/Striker editions (not port work):**
- **Entry and add split.** Nothing yet turns an N-contract intent into N one-contract requests. The owner is T09 / TB-I3 scope under incident ADR §A8 rules 9–10.
- **Exit split.** The port's close is one market exit for the whole position (`port:183-185`). Incident ADR §A8 assumes an exit is for one contract under the one-contract rule, so a multi-contract close also needs splitting at the rail. Recorded as freeze item VAN-8 here and STR-7 / ORB-6 in the sibling.

## §4 — Identity binding (filled at freeze)

| Artifact | Binding | Status |
|---|---|---|
| Vanguard edition Pine (private) | SHA-256 recorded in `core/strategies/BOOK_SOURCES.sha256` (or `PORT_MANIFEST.sha256`, per the §59 owner's convention) and here | **OWED** |
| Vanguard edition Python port (private) | SHA-256 pin added beside the existing pins in `ops/c1_signal_daemon/book_adapters.py`, as a separate reviewed change | **OWED** |
| Effective inputs for the edition | Either the existing binding (`66406dee…` source bytes, `9d4d4e1d…` runtime digest) or a successor digest. If trailing is removed by an input override rather than a code change, name that input here as a shape, with no value. *§3a:* trailing is a single on/off input in both the port and the Pine, and VAN-4 needs no code change, so an **input-only** edition is possible: a successor effective-inputs file with the trail input off, the port code unchanged, and the port-pin row above becoming "unchanged". The effective-inputs file holds all four legs, so a successor changes the **book-wide** runtime digest. | **OWED (operator)** |
| This file at freeze | Commit SHA recorded in campaign record §59 | At freeze |

The realization and identity-binding scheme must be specified before file production; reused pins are fixed then, while new output digests are supplied by production before freeze. The final tuple includes: Pine SHA-256, port SHA-256, embedded PINE_SHA256, registry leg identity, and effective-input source/runtime digests. The existing loader requires the embedded Pine identity to equal the registry Pine identity. Reusing unchanged port bytes with a newly changed Pine therefore does not work under the current loader. Override-only is admissible only with unchanged compatible Pine/port identities and explicitly bound effective settings, or after a separately reviewed identity-contract change. If new Pine bytes are required under the current loader, use a new port identity with matching embedded Pine identity; do not weaken the loader check. No such identity-contract change is authorized here. The production handoff must stop if this tuple is unresolved.

The public repository receives identities and behavior shapes only, never source bodies or private parameter values. The current Vanguard Pine and port (`af26899c…`, `e6a03d04…`) are not edited.

## §5 — Relationship to the ORB/Striker file

- K accounting is per leg: this file adds one expression for Vanguard, and the sibling file's two expressions are unchanged.
- If both files freeze, the book's E1 runs with all three route-native editions plus Aegis as declared.
- The §6 replay-modelling rule for the split **should match** the sibling file's choice. State here whether it does; a different rule must be justified.

## §6 — How the edition requalifies, and what counts as a result

- **No new screen is bought.** The edition requalifies through the production E1 already owed for the book (deployment checklist T10 → T15), under the criteria frozen by the existing owners (Track B umbrella and the full-E1 specification). This file adds no statistic, threshold, depth or seed.
- **Replay modelling of the split — OWED (operator and coordinator).** Before freeze, state how the qualification replay prices N sequential one-contract requests:
  - (a) all N at the same fill as today's single order (optimistic);
  - (b) a concrete replay algorithm stated here in full: the per-request price and fill rule for request k of N, any delay model, and its frozen inputs. The rail spec's I8 classifies live latency deviation but defines no replay pricing, so naming I8 alone does not satisfy this;
  - (c) another rule stated now.

  *§3a note:* the sibling file's §6 choice is also still OWED, so the two can be decided together. Under the proposed ADR §A8 rule 10, one-contract requests go out sequentially, so (a) would be optimistic by construction, and a stated sequential rule under (b) is the source-consistent option.

  It cannot be tuned afterwards.
- **Replay model for N sequential exit requests — OWED (pre-registration owner, then operator acceptance).** Operator ruling 2026-09-26: "Mark OWED; block freeze". Under option (b), the replay must also price the one-contract closes of VAN-8, where a multi-contract close becomes N sequential one-contract exit requests. The pre-registration owner states here the exact replay algorithm and its frozen inputs: the per-request delay, and the price and fill rule for exit request k of N. The operator then accepts it. Reusing the entry-split algorithm is allowed only if this item states how it applies to exits. Naming I8, or "same as §6" alone, does not satisfy this. This file cannot freeze while this item is OWED.
- **Verdict:**
  - PASS: the Vanguard route-native edition is qualified as part of the book's E1 result.
  - NO-GO: the route is rejected for Vanguard. **No second expression is tried** under this pre-registration, and what happens to the book then is a new operator decision.

## §7 — Forbidden moves

- Screening more than one Vanguard expression, whether by alternative stop levels, trail substitutes or entry timings.
- Substituting a CrossTrade-managed trail for the declared trail. It is vendor-driven, not fill-anchored, and not native L2(g) (REST assessment §6.7 (4)).
- Changing any signal, setup or entry condition, allocation, protection cell, capacity rule, takeover order or WATCH-tier rule.
- Inventing a new exit to replace the trail (VAN-3). If no existing exit covers a case, stop and return to the operator.
- Editing the locked Vanguard Pine, the current port, or `core/strategies` artifacts in place. The edition uses new private files and pins where the ruled realization changes bytes; an override-only realization reuses the explicitly compatible source identities and binds new effective settings.
- Publishing Pine source, parameter values or port code in this or any public file.
- Amending this file after any replay or E1 output on the edition exists. Close it and open a fresh one instead.
- Treating the edition as qualified, selected or deployable before the E1 verdict.

## §8 — Freeze procedure

1. The operator rules option A (edition) over option B (reject). Without that ruling, nothing below proceeds.
2. The operator answers VAN-2 to VAN-6 and VAN-8, the §4 effective-inputs row and the §6 replay choice, in words and without parameter values. The §6 sequential-exit replay model is specified by the pre-registration owner and accepted by the operator.
3. Once the capability allocation is accepted (checklist T09 gate D; operator ruling 2026-09-26, [production handoff](../handoffs/2026-09-26-vanguard-fixed-stop-edition-production.md) G3b), the operator, or a separately authorized session in the primary checkout, produces the files required by the ruled realization and supplies the complete source/effective-input identity tuple. §60 alone grants reads, not file creation. An override-only realization explicitly records reused compatible Pine/port pins.
4. Claude fills §3–§6, runs the §10 hooks, and the operator reviews the full text.
5. The operator says "freeze". The Status line becomes `FROZEN <date>`, and the commit SHA goes into campaign record §59.

## §10 — Audit hooks

```bash
# Status must read FROZEN before any edition replay or E1 run exists
grep -n '^\*\*Status:\*\*' docs/briefs/pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md
# No unresolved status may remain at freeze; expect no output.
# The pattern matches status cells and the replay-choice marker only, not explanatory prose.
grep -nE '\| \*\*OW[E]D|\(OW[E]D,|— OW[E]D \(' docs/briefs/pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md
# Edition id present in the venue-edition ledger as CANDIDATE
grep -n 'vanguard_mgc_fixed_stop_oso' ops/venue_editions/Tradeify_Select_100K.md
# No edition Pine or port bodies committed; expect no output
git ls-files 'ops/c1_signal_daemon/ports/*.py' ':(icase)*vanguard*fixed*stop*' | grep -v '\.md$'
```
