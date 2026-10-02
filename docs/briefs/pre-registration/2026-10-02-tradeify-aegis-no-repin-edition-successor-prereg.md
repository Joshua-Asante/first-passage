# Pre-registration SKELETON (2026-10-02): route-native no-re-pin edition of Aegis 6J for the Tradeify book

**Status:** `DRAFT — NOT FROZEN.` **SKELETON:** every expression field is **OWED (operator)**, and no row carries an answer. Nothing here binds a replay, E1 run or verdict until the Status line reads `FROZEN <date>` and the freeze commit's SHA is recorded in the owning record named under §8 step 1. No replay, E1 dispatch or screen may run on this edition before then. The standing rule in §R applies.

**Format:** written in the 2026-10-02 successor structure (§D, §R, §S), modelled on the [Vanguard successor](2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md). There is no Aegis original, so it **supersedes nothing**.

**What "no-re-pin" means here:** the declared Aegis port moves its stop to breakeven and re-pins its target once, after entry. Each move is a `BracketAmend`, an L2(c) native modify, which is `K` on this route ([capability map C10d](../../notes/2026-09-25-tradeify-capability-allocation-deletion-map.md); [REST route assessment §6.5](../handoffs/2026-09-25-crosstrade-rest-route-assessment.md#65-per-leg-primitive-map-step-4)). A no-re-pin edition is one whose protective levels do not change after entry. Whether that holds, and what replaces the moves, is OWED (AEG-3, AEG-4).

- **Precondition — OWED (operator).** No operator ruling creates an Aegis edition. The operator's direction of 2026-09-26 (B–D packet B-8, R-EDITIONS) keeps Aegis's breakeven and re-pin as declared, dependent on GC-2b and GC-3. If either fails, the leg returns to the operator with alternatives, and **no replacement edition is created automatically**. Those alternatives are named in [packet GC-2b](../../notes/2026-09-26-tradeify-bd-decision-packet.md#12-other-decisive-capabilities): a fixed-stop edition, a different amend realization under a contract change, or excluding the leg. The GC-2b decision for Striker and Aegis is still owed (checklist M2 row). This skeleton prepares **one** of those alternatives on coordinator dispatch (Ticket O). It is not an operator direction and adopts nothing. If the operator does not choose this edition, close the file unfrozen with a one-line note and open nothing else.

**Owner:** OWED. If the operator adopts this edition, the owning record is the one the operator names, expected to be campaign record §59 by analogy with [Ruling 4](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-4--vanguard-mgc-fixed-stop-edition-on-this-route-2026-09-26).
**Loop of record:** STRATEGIC. If adopted, the expression change is forced by the route's capability: K = 1, not a search.
**Authored:** 2026-10-02 by Claude Code (cloud worker, drafting only), on the deployment coordinator's Ticket O. The operator owns every OWED item, the precondition and the freeze.

**Siblings:** the [ORB/Striker successor](2026-10-02-tradeify-route-native-editions-successor-prereg.md) and the [Vanguard successor](2026-10-02-tradeify-vanguard-fixed-stop-edition-successor-prereg.md), both unfrozen. Each file keeps its own scope and K accounting. If this file is adopted and frozen, all four editions requalify together in the same production E1 (§6).

## §D — Disclosure: what was seen before this skeleton was written

- **This drafting session** (Claude Code cloud worker, 2026-10-02) read only the public files listed in §0 at `origin/main@bd30646`, including the two siblings' §D sections. It read no private Pine, port or effective-input file, no PR comment holding replay counts, and no replay output. It ran no replay, emulator, port or backtest.
- **The siblings' §D** discloses candidate replays of the accepted ORB and Vanguard ports and an inspection of structural counts. Neither names the Aegis port.
- **Disclosure completeness — OWED (operator).** This session cannot know whether any candidate-configurable replay of the Aegis port has been run, for example with its breakeven or re-pin disabled, or what was inspected. The operator completes this list before ratification. If such output exists, the operator also rules how it bears on this file, as the siblings' §7 **Successor validity** item does for theirs.

**Answerer exposure statement (same form as the siblings):** whoever answers AEG-3, the row that names what replaces the breakeven and re-pin moves, must state whether they have seen either of these:
- any replay output of an Aegis expression without those moves;
- the counts disclosed in the siblings' §D.

The statement goes in AEG-3's status cell (the last cell), in exactly this form: `Answerer exposure: seen — <answerer name>` or `Answerer exposure: not seen — <answerer name>`. The name after the em dash must not be empty. §7 makes this a freeze item, and §10 checks it.

## §R — Standing rule: no candidate-configurable replay before freeze

*Operator ruling 2026-10-02 ([PR #590](https://github.com/Joshua-Asante/first-passage/pull/590) item 7.6.1; [checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) item 7.6.1):* no agent runs any candidate-configurable replay against a pre-registered edition before that pre-registration is frozen. That includes an accepted port with input overrides. This file is not frozen; the rule applies to the edition it pre-registers.

## §S — What this skeleton takes from the Vanguard successor

**Taken as structure:** the header form, §D, §R, the §2 shape constraints (verbatim from incident ADR §A1), the §6 requalification and verdict form, the §7 forbidden-move pattern, the §8 freeze sequence, and the §10 hooks retargeted to this file.

**Not taken:** every Vanguard answer, proposed answer, dated direction marker and §3a finding.
- **C-a is not proposed here.** The successors' C-a answer is proposed under PR #590 item 7.2 for ORB-6, STR-7 and VAN-8 only.
- **Ruling 5's split constraints are recorded only for Striker and Vanguard** (STR-3/4, VAN-5/6). They are cited here as context and are not recorded as extending to Aegis.

---

## §0 — Rule-0 reads (public, `origin/main@bd30646`)

| Source | What it fixes for this file |
|---|---|
| Campaign record §55 (D-B4 (a)), [§59 Ruling 1](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-1--vanguard-mgc-and-aegis-6j-fit-the-narrowed-shape-operator-attested), [Ruling 5](../programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-5--edition-directions-2026-09-26), [§60](../programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25) | The accepted four-leg book at K = 1. Ruling 1: the operator attested that Aegis fits the narrowed shape (a stop in the same order; expressible as one-contract requests), while "L2(c) for Aegis's breakeven modify and the takeover composite remain K". §60 governs agent reads of private sources. |
| [REST route assessment §6.5](../handoffs/2026-09-25-crosstrade-rest-route-assessment.md#65-per-leg-primitive-map-step-4) | Aegis column: L2(c) is **used** for the breakeven and target re-pin on each child; full close is K, including the timed exit; the takeover composite is K; L2(g) is not indicated. |
| [Capability map](../../notes/2026-09-25-tradeify-capability-allocation-deletion-map.md) C10d and the amend-decision row | The one-time breakeven and target re-pin is a port-emitted `BracketAmend` that depends on L2(c). The re-pin is a strategy decision, and a vendor trail is not equivalent. |
| [B–D decision packet](../../notes/2026-09-26-tradeify-bd-decision-packet.md) GC-2b, B-8 | A failed modify capability returns with alternatives; no automatic replacement edition (R-EDITIONS). |
| [Incident ADR](../../adr/2026-09-17-bounded-platform-protection-incident-contract.md) §A1, §A4 (Aegis row), §A8 rules 9–10, §A9.1 UB-4 | The narrowed request shape. Aegis needs per-contract requests. Split admission is whole-or-nothing, with one unresolved request per symbol. UB-4: abandoning a remainder must enter the Aegis pre-registration where Aegis splits, and be replayed. |
| [Scaling-faithfulness read](../../notes/2026-09-12-track-b-scaling-faithfulness-read.md) (Aegis row) | Aegis exits are price-only (stop, target, breakeven, stale, EOD). The rail expresses the captured size as a fixed quantity (TB-S1 (F)). |
| [Signal-route evaluation](../../notes/2026-09-25-tradingview-signal-route-evaluation.md) (Aegis rows) | Entry state and the daily count advance locally. The breakeven latch, target re-pin and holding clock are local strategy state at the completed-bar boundary. |
| `ops/c1_rail/book_policy.py:176-183`; `ops/c1_signal_daemon/book_adapters.py:39-43`; `core/strategies/BOOK_SOURCES.sha256` | Aegis is the short leg, at priority 1 (the takeover taker), protected rule `SCALE`. Current pins: Pine `db78ecba…`, port `11763740…`. Neither file is edited. |
| [Deployment checklist](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md) first-release item 7 | Intentional partial exits are unsupported in the first release. C-a is directed, not selected, for every strategy close and scheduled flatten. |
| `AGENTS.md` "Public-clone posture" | No Pine source, parameter value or port code appears here. Rules are stated as shapes only. |

The drafting session **did not read** the Aegis Pine or port; neither exists in the cloud clone. No behavioural statement here comes from private source.

## §1 — What would be pre-registered

Exactly one new venue-edition expression, K = 1, if the precondition is ruled:

| Leg | Edition id (venue-edition ledger, `CANDIDATE`) | Replaces, on this route only |
|---|---|---|
| Aegis 6J | `aegis_6j_no_repin_oso@Tradeify_Select_100K` (working name) | The declared Aegis expression, whose brackets are amended after entry (breakeven and target re-pin) |

**Edition id and ledger row — OWED (operator).** The ledger has no Aegis row today.

**Inherited, not re-selected:** the book's legs and allocations; the protection cell; capacity; Aegis-priority takeover ordering, with Aegis as the taker; the WATCH-tier rule; and every Aegis signal, setup, entry and filter condition. Only the **order expression** changes: how protection travels with exposure, whether it moves after entry, and how quantity is split into requests.

## §2 — Shape constraints (from incident ADR §A1)

Every exposure-creating request (entry or add) must:
1. be a single market or stop entry for **exactly one contract**;
2. carry its **own native fixed stop in the same request** (CrossTrade `place` with `stop_loss`, which becomes one Tradovate `placeoso`);
3. be sent **without** `delay=`, ATM fields, trailing fields, `cancel_after`, or copier or multi-account fan-out.

A multi-contract intent is sent as that many one-contract requests, each carrying its own stop.

## §3 — Aegis 6J edition

| # | Rule | Status |
|---|---|---|
| AEG-1 | **Entry request shape.** Each request is one contract, carrying its fixed protective stop and, where declared, its target in the same request. State whether the declared entry order type is kept unchanged. | **OWED (operator)** |
| AEG-2 | **Stop and target levels at entry.** Are they the declared bracket's levels at entry, unchanged, sent with each request? | **OWED (operator)** |
| AEG-3 | **What replaces the breakeven and re-pin moves as exits.** The declared moves changed how some trades closed. Name the existing exit that now covers each such case: the fixed stop, the original target, the stale or timed exit, the EOD flat, or another existing rule. **No new exit rule is invented here.** If no existing exit covers a case, say so; the edition is then a different strategy needing a fresh decision (§7). | **OWED (operator)** |
| AEG-4 | **Stop and target modification after entry.** The edition's working name assumes "none". State it. If any amend remains, it depends on L2(c), which is K (drill D2), and this edition would not remove the dependency it exists to remove. Return to the operator in that case. | **OWED (operator)** |
| AEG-5 | **One-contract split.** State the maximum contracts per Aegis signal on this account, including any cap. State whether the split follows whole-intent capacity reservation and sequential submission. Ruling 5 records that rule for Striker and Vanguard only. | **OWED (operator)** |
| AEG-6 | **Partial acknowledgement of a split.** Track each one-contract request separately:<br>• confirmed fills establish position quantity;<br>• accepted-but-unfilled requests remain working orders with their reservations;<br>• conclusively rejected requests follow the accepted release rule;<br>• unknown requests keep their reservations under the incident ADR.<br>An acknowledgement alone never increments position. Confirm that nothing is re-sent merely because no fill is observed. State whether the unsent remainder is abandoned on an exceptional outcome (UB-4). | **OWED (operator; fill-based position semantics required by book_protocol.py)** |
| AEG-7 | **State the removed moves also fed.** The breakeven latch, holding clock and daily count are local strategy state (§0). State which of them remain, unchanged, for purposes other than the removed amends, such as the timed exit or entry eligibility. | **OWED (operator)** |
| AEG-8 | **Exit split.** State how a multi-contract Aegis close is realized: strategy exits, the timed exit and the scheduled flatten. The checklist directs C-a for every first-release strategy close, but that is not selected. The successors' C-a answer is proposed for other legs' rows only. This file proposes no answer. | **OWED (operator)** |

## §3a — Source mapping (owed; not done)

**OWED (operator):** a local session in the primary checkout reads the pinned Aegis port and Pine in place under §60, and maps what the source already constrains for each AEG row, as Vanguard's §3a did. It records behaviour only, with no parameter values and no execution, and it never runs the port (§R). This cloud session could not do it, because no private inputs exist here. The mapping suggests; it answers nothing. If the operator does not request it (§8 step 2), this marker is replaced with "not requested" and the date.

## §4 — Identity binding (filled at freeze)

| Artifact | Binding | Status |
|---|---|---|
| Aegis edition Pine (private) | SHA-256 recorded in `core/strategies/BOOK_SOURCES.sha256` (or `PORT_MANIFEST.sha256`, per the §59 owner's convention) and here, or the retained compatible identity | **OWED** |
| Aegis edition Python port (private) | SHA-256 pin beside the existing pins in `ops/c1_signal_daemon/book_adapters.py`, as a separate reviewed change, or the retained compatible identity | **OWED** |
| Realization and leg identity | Override-only or code edition; keep or renew `leg_id`. The options and their cascade are in the [realization and leg-identity options note](../../notes/2026-10-02-edition-realization-and-leg-id-options.md), which proposes no scheme | **OWED (operator)** |
| Effective inputs for the edition | Explicit source and runtime digests, reused or successor as ruled. The effective-inputs file holds all four legs, so a successor changes the **book-wide** runtime digest | **OWED (operator)** |
| This file at freeze | Commit SHA recorded in the owning record (§8 step 1) | At freeze |

The realization and identity-binding scheme is specified before file production. Reused pins are fixed then; new output digests are supplied by production before freeze.

The final tuple includes:
- Pine SHA-256;
- port SHA-256;
- embedded `PINE_SHA256`;
- registry leg identity;
- effective-input source and runtime digests.

The existing loader requires the embedded Pine identity to equal the registry Pine identity. Override-only is admissible only with unchanged compatible Pine and port identities and explicitly bound effective settings. If new Pine bytes are required, use a new port identity with a matching embedded Pine identity; do not weaken the loader check. No identity-contract change is authorized here.

The public repository receives identities and behaviour shapes only, never source bodies or private parameter values. The current Aegis Pine and port (`db78ecba…`, `11763740…`) are not edited.

## §5 — Relationship to the sibling files

- K accounting is per leg. This file would add one expression for Aegis; the siblings' three expressions are unchanged.
- If all three files freeze, the book's E1 runs with four route-native editions.
- The §6 split replay rule **should match** the siblings' choice. State here whether it does; a different rule must be justified. One concrete option (b) is in [ED-10](../../notes/2026-10-02-ed10-sequential-split-replay-pricing.md). Aegis is the short leg, so any rule must be side-aware.

## §6 — How the edition requalifies, and what counts as a result

- **No new screen is bought.** The edition requalifies through the production E1 already owed for the book (deployment checklist T10 → T15), under the criteria frozen by the existing owners (the Track B umbrella and the full-E1 specification). This file adds no statistic, threshold, depth or seed.
- **Replay modelling of the split — OWED (operator and coordinator).** Before freeze, state how the qualification replay prices N sequential one-contract requests:
  - (a) all N at the same fill as today's single order;
  - (b) a concrete replay algorithm stated here in full: the per-request price and fill rule for request k of N, any delay model, and its frozen inputs. The rail spec's I8 defines no replay pricing, so naming I8 alone does not satisfy this;
  - (c) another rule stated now.

  It cannot be tuned afterwards.
- **Replay model for exit-side requests — OWED (operator).** This follows the AEG-8 answer. If a close is one request, state that this item is moot and why.
- **Verdict:**
  - PASS: the Aegis route-native edition is qualified as part of the book's E1 result.
  - NO-GO: the route is rejected for Aegis. **No second expression is tried** under this pre-registration. What happens to the book then is a new operator decision; Aegis is the takeover taker, so the takeover ordering is part of that decision.

## §7 — Forbidden moves

- Screening more than one Aegis expression, whether by alternative stop or target levels, breakeven substitutes or entry timings.
- Substituting a vendor-managed breakeven, auto-move or trail for the declared moves. The re-pin is a strategy decision, and a vendor mechanism is not equivalent (capability map).
- Changing any signal, setup, entry or filter condition, allocation, protection cell, capacity rule, takeover order or WATCH-tier rule.
- Inventing a new exit to replace the removed moves (AEG-3). If no existing exit covers a case, stop and return to the operator.
- Editing the locked Aegis Pine, the current port, or `core/strategies` artifacts in place.
- Publishing Pine source, parameter values or port code in this or any public file.
- Amending this file after any replay or E1 output on the edition exists. Close it and open a fresh one instead.
- **Precondition — freeze item.** This file cannot freeze while its header **Precondition** bullet remains OWED. §10 checks it.
- **Answerer exposure — freeze item.** This file cannot freeze unless the answered AEG-3 row's status cell carries `Answerer exposure: seen — <answerer name>` or `Answerer exposure: not seen — <answerer name>`, with a nonempty name (§D). §10 checks it.
- Running any candidate-configurable replay against this edition before this file is FROZEN (§R), including an accepted port with input overrides.
- Treating the edition as adopted, qualified, selected or deployable before the operator's precondition ruling and the E1 verdict.

## §8 — Freeze procedure

1. **Precondition.** The operator rules on adopting this edition among the GC-2b alternatives and names the owning record. Without that ruling nothing below proceeds. If the operator declines, close this file unfrozen with a one-line note.
2. **Source mapping (optional).** If the operator wants it before answering, a local §60 session produces the §3a mapping.
3. **Answers.** The operator answers AEG-1 to AEG-8, the §4 realization and effective-inputs rows, and the two §6 items, in words and without parameter values. The operator completes the §D disclosure.
4. **Files.** The ledger `CANDIDATE` row is added. A production handoff shaped like its siblings is drafted; none exists yet. After the capability allocation is accepted (checklist T09 gate D), the files required by the ruled realization are produced and the complete identity tuple is supplied. §60 grants reads, not file creation.
5. **Audit.** Claude fills §3–§6 and runs every §10 hook **except the Status hook**, and the operator reviews the full text. If any text changes after this step, run §10 again before freeze.
6. **Freeze.** The operator says "freeze". The Status line must begin exactly ``**Status:** `FROZEN YYYY-MM-DD` ``, with the freeze date and no trailing period inside the backticks. The commit SHA goes into the owning record.
7. **Re-audit.** In the freeze commit, Claude reruns the **full** §10 audit, including the Status hook. If any hook fails, the freeze is void: the Status line reverts to `DRAFT — NOT FROZEN.` and the owning record's SHA entry is withdrawn.

## §10 — Audit hooks

```bash
# Precondition (header, §7, §8 step 1): expect no output at freeze
grep -n '^- \*\*Precondition — OW[E]D' docs/briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md
# Disclosure completeness (§D): expect no output at freeze
grep -n '^- \*\*Disclosure completeness — OW[E]D' docs/briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md
# Answerer-exposure freeze item (§D, §7): at freeze, expect exactly one line, the answered AEG-3 row
grep -nE '^\| AEG-3 [^|]*\| [^|]*\| [^|]*Answerer exposure: (seen|not seen) — [A-Za-z][^|]* \|$' docs/briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md
# Status must read FROZEN before any edition replay or E1 run exists: expect exactly one line
grep -nE '^\*\*Status:\*\* `FROZEN [0-9]{4}-[0-9]{2}-[0-9]{2}`' docs/briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md
# No unresolved status may remain at freeze; expect no output
grep -nE '\| \*\*OW[E]D|\(OW[E]D,|— OW[E]D \(|^\*\*OW[E]D \(|^\*\*Owner:\*\* OW[E]D' docs/briefs/pre-registration/2026-10-02-tradeify-aegis-no-repin-edition-successor-prereg.md
# Edition id present in the venue-edition ledger as CANDIDATE (the id as ruled at step 3)
grep -n 'aegis_6j_no_repin_oso' ops/venue_editions/Tradeify_Select_100K.md
# No edition Pine or port bodies committed; expect no output
git ls-files 'ops/c1_signal_daemon/ports/*.py' ':(icase)*aegis*repin*' | grep -v '\.md$'
```
