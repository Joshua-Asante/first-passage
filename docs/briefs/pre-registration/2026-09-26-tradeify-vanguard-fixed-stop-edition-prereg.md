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

The drafting session **did not read** the Vanguard Pine or port; they are not in the cloud clone. Behavioural statements come from the determination return or the public owners above, or are marked OWED.

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
| VAN-6 | **Partial acknowledgement of a split.** If k of N requests are acknowledged and the rest are refused or unknown, the leg holds k contracts, plus held reservations for the unknowns under the incident ADR. Confirm the edition treats the confirmed k as its position and does **not** re-send the rest. The [route note](../../notes/2026-09-25-tradingview-signal-route-evaluation.md) (line 207) records that the add counter advances when an add is proposed, not when it fills; state whether that stays as declared. | **OWED (operator; recommended: confirm, counters as declared)** |
| VAN-7 | Breakeven and grace stay inactive, as in the accepted binding. The edition does not enable them. | Fixed (determination §5) |

## §4 — Identity binding (filled at freeze)

| Artifact | Binding | Status |
|---|---|---|
| Vanguard edition Pine (private) | SHA-256 recorded in `core/strategies/BOOK_SOURCES.sha256` (or `PORT_MANIFEST.sha256`, per the §59 owner's convention) and here | **OWED** |
| Vanguard edition Python port (private) | SHA-256 pin added beside the existing pins in `ops/c1_signal_daemon/book_adapters.py`, as a separate reviewed change | **OWED** |
| Effective inputs for the edition | Either the existing binding (`66406dee…` source bytes, `9d4d4e1d…` runtime digest) or a successor digest. If trailing is removed by an input override rather than a code change, name that input here as a shape, with no value. | **OWED (operator)** |
| This file at freeze | Commit SHA recorded in campaign record §59 | At freeze |

The public repository receives digests only. The current Vanguard Pine and port (`af26899c…`, `e6a03d04…`) are not edited.

## §5 — Relationship to the ORB/Striker file

- K accounting is per leg: this file adds one expression for Vanguard, and the sibling file's two expressions are unchanged.
- If both files freeze, the book's E1 runs with all three route-native editions plus Aegis as declared.
- The §6 replay-modelling rule for the split **should match** the sibling file's choice. State here whether it does; a different rule must be justified.

## §6 — How the edition requalifies, and what counts as a result

- **No new screen is bought.** The edition requalifies through the production E1 already owed for the book (deployment checklist T10 → T15), under the criteria frozen by the existing owners (Track B umbrella and the full-E1 specification). This file adds no statistic, threshold, depth or seed.
- **Replay modelling of the split — OWED (operator and coordinator).** Before freeze, state how the qualification replay prices N sequential one-contract requests:
  - (a) all N at the same fill as today's single order (optimistic);
  - (b) the latency class the rail spec already uses (I8);
  - (c) another rule stated now.

  It cannot be tuned afterwards.
- **Verdict:**
  - PASS: the Vanguard route-native edition is qualified as part of the book's E1 result.
  - NO-GO: the route is rejected for Vanguard. **No second expression is tried** under this pre-registration, and what happens to the book then is a new operator decision.

## §7 — Forbidden moves

- Screening more than one Vanguard expression, whether by alternative stop levels, trail substitutes or entry timings.
- Substituting a CrossTrade-managed trail for the declared trail. It is vendor-driven, not fill-anchored, and not native L2(g) (REST assessment §6.7 (4)).
- Changing any signal, setup or entry condition, allocation, protection cell, capacity rule, takeover order or WATCH-tier rule.
- Inventing a new exit to replace the trail (VAN-3). If no existing exit covers a case, stop and return to the operator.
- Editing the locked Vanguard Pine, the current port, or `core/strategies` artifacts in place. The edition is new private files with new pins.
- Publishing Pine source, parameter values or port code in this or any public file.
- Amending this file after any replay or E1 output on the edition exists. Close it and open a fresh one instead.
- Treating the edition as qualified, selected or deployable before the E1 verdict.

## §8 — Freeze procedure

1. The operator rules option A (edition) over option B (reject). Without that ruling, nothing below proceeds.
2. The operator answers VAN-2 to VAN-6, the §4 effective-inputs row and the §6 replay choice, in words and without parameter values.
3. The private edition Pine and port are produced by the operator, or by a separately authorized session on the primary checkout under §60, and their SHA-256s are supplied.
4. Claude fills §3–§6, runs the §10 hooks, and the operator reviews the full text.
5. The operator says "freeze". The Status line becomes `FROZEN <date>`, and the commit SHA goes into campaign record §59.

## §10 — Audit hooks

```bash
# Status must read FROZEN before any edition replay or E1 run exists
grep -n '^\*\*Status:\*\*' docs/briefs/pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md
# No OWED field may remain at freeze; expect no output
grep -n 'OWED' docs/briefs/pre-registration/2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md
# Edition id present in the venue-edition ledger as CANDIDATE
grep -n 'vanguard_mgc_fixed_stop_oso' ops/venue_editions/Tradeify_Select_100K.md
# No edition Pine or port bodies committed; expect no output
git ls-files 'ops/c1_signal_daemon/ports/*.py' '*vanguard*fixed*stop*' | grep -v '\.md$'
```
