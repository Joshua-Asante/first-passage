# Pre-registration — route-native editions of ORB MNQ and Striker MYM for the Tradeify book

**Status:** `DRAFT — NOT FROZEN.` Fields marked **OWED (operator)** must be answered before freeze. Nothing in this file binds a replay, E1 run or verdict until the Status line reads `FROZEN <date>` and the freeze commit's SHA is recorded in [campaign record §59](../programs/2026-09-03-seven-strategy-select-campaign-state.md#59--route-native-expressions-for-the-accepted-book-three-operator-rulings-2026-09-25). No replay, E1 dispatch or screen may run on either edition before that.
**Owner:** campaign record §59, ruling 3, step 1 ("pre-register the two editions … written before any replay or E1 run on the editions and is not changed after").
**Loop of record:** STRATEGIC (expression change forced by route capability; K = 1 per leg, not a search).
**Authored:** 2026-09-25, Claude Code (drafting); operator (Joshua) owns every rule marked OWED and the freeze.

---

## §0 — Rule-0 reads (anchors at `main@7d78970`, 2026-09-25)

| Source | What it fixes for this file |
|---|---|
| `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md` §55 (D-B4 (a)), §59 | The accepted four-leg book, K = 1; §59 amends D-B4 (a) only to admit these two editions once frozen here. |
| `docs/notes/2026-09-10-tradeify-protection-selection.md` "Selected book", "Protection behavior selected" | Leg settings (ORB: one micro per base/add, up to two adds; Striker MYM: 30-max-contract setting), 1% combined trigger, 40% scale, ORB base unreduced, ORB adds off under protection, 80-micro capacity, Aegis-priority takeover. |
| `docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md` Addendum 2026-09-24 §A1, §A4 (+ 2026-09-25 correction) | The narrowed request shape both editions must satisfy; the per-primitive route table (L2(e)/(f)/(g) U). |
| `docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md` S2, S3 (a)/(b)/(d)/(e), R-B3 L-2 | Why the declared expressions fail on this route: ORB needs L2(g) native trailing; Striker needs L2(f) attach and multi-contract residual cover. I8: a substitute expression is a different strategy until requalified. |
| `core/strategies/PORT_MANIFEST.sha256`, `ops/c1_signal_daemon/book_adapters.py` (port pins) | How private Pine editions and Python ports are bound by digest without publishing their contents. |
| `AGENTS.md` "Public-clone posture"; "Strategy Reference" | No Pine source, parameter values or executable ports of locked logic in this public file. Rules below are stated as shapes; values live only in the pinned private files. |

The declared ORB and Striker Pine and ports were **not read** by the drafting session (private). Every behavioral statement about them below is either from a public owner cited above or marked OWED.

## §1 — What is pre-registered

Exactly two new venue-edition expressions, one per leg, each K = 1:

| Leg | Edition id (venue-edition ledger, `CANDIDATE`) | Replaces, on this route only |
|---|---|---|
| ORB MNQ | `orb_mnq_fixed_stop_oso@Tradeify_Select_100K` | The declared ORB expression whose bracket carries trailing parameters |
| Striker MYM | `striker_dj30_mym_entry_with_stop@Tradeify_Select_100K` | The declared Striker MYM expression that enters bare and attaches protection a bar later |

Aegis 6J keeps its declared expression (operator-attested to fit the narrowed shape, §59 ruling 1). **Vanguard MGC is qualified:** the [trailing determination](../handoffs/2026-09-26-vanguard-mgc-trailing-determination.md#5-executor-return) returned `TRAILING ACTIVE`, so its §59 ruling 1 fit attestation is not current evidence, and it depends on L2(g). Vanguard is handled by its own [edition pre-registration](2026-09-26-tradeify-vanguard-fixed-stop-edition-prereg.md) or by the operator rejecting the leg on this route. This file's freeze inventory must carry that pending decision; it must not treat Vanguard as fitting.

**Unchanged for the whole book (inherited, not re-selected):** legs and allocations; the 1% combined-peak trigger, 40% scale, ORB base unreduced and ORB adds off under protection; 80-micro shared capacity; Aegis-priority takeover ordering; every signal/entry condition of both legs. Only the **order expression** (how protection rides with exposure, and how quantity is split into requests) changes.

## §2 — Shape constraints both editions must meet (from incident ADR §A1)

Every exposure-creating request (entry or add) is:
1. a single market or stop entry for **exactly one contract**;
2. carrying its **own native fixed stop in the same request** (CrossTrade `place` with `stop_loss` → one Tradovate `placeoso`);
3. sent **without** `delay=`, ATM fields, trailing fields, `cancel_after`, or copier / multi-account fan-out.

A multi-contract intent is sent as that many one-contract requests, each with its own stop.

## §3 — ORB MNQ edition

| # | Rule | Status |
|---|---|---|
| ORB-1 | Entry: resting stop entry (as declared, S2), one contract per base or add, carrying its fixed protective stop in the same request. No trailing parameters are sent or modelled. | Fixed by §59 |
| ORB-2 | **Fixed stop level at entry.** State the rule: is it the declared bracket's existing fixed-stop component, unchanged? | **OWED (operator)** |
| ORB-3 | **What replaces the trail as an exit.** The declared trail closed some trades. State which existing exit now closes them: the fixed stop, an existing target, the scheduled flatten, or another existing rule. No new exit rule is invented here; if none of the existing exits applies, say so, and the edition is a different strategy that needs a fresh decision (§7). | **OWED (operator)** |
| ORB-4 | **Stop modification after entry.** Does the edition ever amend the fixed stop (per-bar re-issue, breakeven)? If yes, that needs L2(c) native modify, which is K on this route (drill D2). If no, write "none". | **OWED (operator)** |
| ORB-5 | Adds: each add is one contract with its own stop; adds remain off under protection (inherited). | Fixed by §59 |
| ORB-6 | **Exit split.** As STR-7, for any multi-contract ORB close (base plus adds, scheduled flatten). | **OWED (operator)** |

## §4 — Striker MYM edition

| # | Rule | Status |
|---|---|---|
| STR-1 | Entry: market entry carrying its fixed protective stop in the same request; no bare entry and no later `ATTACH`. | Fixed by §59 |
| STR-2 | **Stop level at entry.** The declared port issues its first stop a bar after entry. State the rule for the level sent with the entry: (a) the level the declared port would issue, computed on the entry bar (say whether that is computable there), or (b) another rule you specify. This is the decision most likely to change results. | **OWED (operator)** |
| STR-3 | **One-contract split.** A signal for N contracts is sent as N one-contract requests. State the maximum N per signal on this account (the selection records a 30-max-contract setting) and whether any cap below that applies. | **OWED (operator)** |
| STR-4 | **Partial acknowledgement of a split.** Position quantity is established only by confirmed fills, never acknowledgements. Track accepted-but-unfilled requests as working orders with required reservations, conclusively rejected requests under the accepted release rule, and unknown requests with held reservations under the incident ADR. Confirm the edition consumes fill events and does **not** re-send an unresolved request merely because no fill is observed. | **OWED (operator; fill-based position semantics required by book_protocol.py)** |
| STR-5 | **Close-time crossed-level exits (S3 (d)).** State how they are realized: a market exit of the scope (as declared), unchanged. | **OWED (operator)** |
| STR-6 | **Stop modification after entry.** Per-bar re-issue of the stop needs L2(c) (drill D2). State whether the edition modifies the stop after entry. | **OWED (operator)** |
| STR-7 | **Exit split.** A multi-contract close (including close-time crossed-level exits, STR-5, and scheduled flatten) must become one-contract closes under the one-contract rule. State how the rail generates them after admission (not the port), their order and resolution, and the replay treatment. | **OWED (operator)** |

## §5 — Identity binding (fills at freeze)

| Artifact | Binding | Status |
|---|---|---|
| ORB edition Pine (private) | SHA-256 recorded in `core/strategies/PORT_MANIFEST.sha256` and here | **OWED** |
| Striker edition Pine (private) | SHA-256 recorded in `core/strategies/PORT_MANIFEST.sha256` and here | **OWED** |
| ORB and Striker edition Python ports (private) | SHA-256 pins added beside the existing pins in `ops/c1_signal_daemon/book_adapters.py` (a separate, reviewed change) | **OWED** |
| Effective inputs for each edition | Explicit source/runtime digests and Pine/port setting binding; reused or successor as ruled | **OWED (operator)** |
| This file at freeze | Commit SHA recorded in campaign record §59 | At freeze |

Before file production, specify each realization and its identity-binding scheme; fix reused pins and leave only new output digests for production before freeze. The current loader requires the port-embedded PINE_SHA256 to match the registry Pine identity. A changed Pine needs a matching new port identity under that contract. An ORB override-only realization may retain compatible Pine/port identities only with explicit effective settings bound for both; otherwise return to the operator for a code edition or separately reviewed identity contract. Do not weaken the loader checks.

The public repository receives identities and behavior shapes only, never private source or parameter values. The Pine and the ports stay in the private roots (AGENTS.md "Public-clone posture").

## §6 — How the editions requalify, and what counts as a result

- **No new screen is bought.** The editions requalify through the production E1 that was already owed for the book (deployment checklist T10 → T15), under the criteria frozen by their existing owners ([Track B umbrella](../handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md) and the full-E1 specification). This file adds no statistic, threshold, depth or seed.
- **Replay modelling of the split (OWED, operator + coordinator).** Before freeze, state how the qualification replay prices N sequential one-contract requests. Options: (a) all N at the same fill as today's single order (optimistic); (b) a concrete replay algorithm stated here in full: the per-request price and fill rule for request k of N, any delay model, and its frozen inputs. The rail spec's I8 classifies live latency deviation but defines no replay pricing, so naming I8 alone does not satisfy this; (c) another rule stated now. The choice must be written here before any run; it cannot be tuned after.
- **Verdict per leg.** PASS: the leg's route-native edition is qualified as part of the book's E1 result. NO-GO: the route is rejected for that leg; **no second expression is tried** under this pre-registration. What happens to the book then (drop the leg, or requalify the book without it) is a new operator decision, not decided here.

## §7 — Forbidden moves

- Screening more than one expression per leg (alternative stop levels, trail substitutes, entry timings).
- Changing any signal or entry condition, allocation, protection cell, capacity rule or takeover order.
- Inventing a new exit to replace the trail (ORB-3). If no existing exit covers the case, stop and return to the operator.
- Editing locked Pine or `core/strategies` artifacts in place. The editions use new private files with new pins where bytes change; an explicitly ruled ORB override-only realization retains compatible source identities and binds new effective settings.
- Publishing Pine source, parameter values or port code in this or any public file.
- Amending this file after any replay or E1 output on either edition exists (Known Trap #12: close it and open a fresh one instead).
- Treating the editions as qualified, selected or deployable before the E1 verdict.

## §8 — Freeze procedure

1. The operator answers ORB-2..ORB-4, STR-2..STR-6 and the §6 replay-modelling choice, in words (no parameter values).
2. The private edition Pine and ports are produced (operator, or a separately authorized session on the primary checkout) and their SHA-256s supplied.
3. Claude fills §3–§6, runs the §10 hooks, and the operator reviews the full text.
4. The operator says "freeze". The Status line becomes `FROZEN <date>`, and the commit SHA goes into campaign record §59.

## §10 — Audit hooks

```bash
# Status must read FROZEN before any edition replay or E1 run exists
grep -n '^\*\*Status:\*\*' docs/briefs/pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md
# No unresolved status may remain at freeze; expect no output.
# The pattern matches status cells and the replay-choice marker only, not explanatory prose.
grep -nE '\| \*\*OW[E]D|\(OW[E]D,|— OW[E]D \(' docs/briefs/pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md
# Both edition ids present in the venue-edition ledger as CANDIDATE
grep -n 'orb_mnq_fixed_stop_oso\|striker_dj30_mym_entry_with_stop' ops/venue_editions/Tradeify_Select_100K.md
# No edition Pine or port bodies committed; expect no output
git ls-files 'ops/c1_signal_daemon/ports/*.py' ':(icase)*orb*fixed*stop*' ':(icase)*striker*entry*with*stop*' | grep -v '\.md$'
```
