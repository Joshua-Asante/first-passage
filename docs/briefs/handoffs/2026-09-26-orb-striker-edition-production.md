# ORB MNQ and Striker MYM route-native editions: produce the private edition files (bounded local handoff)

**Status:** DRAFT. **Not dispatchable** until every §0 gate holds. It runs only on the operator's primary checkout, because the private Pine and ports exist nowhere else. Commit this packet before dispatch and record the dispatch revision in §7.

**Selected outcome:** the private files for the two editions pre-registered in [the ORB/Striker editions pre-registration](../pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md), built exactly as its answered rules state:
- `orb_mnq_fixed_stop_oso@Tradeify_Select_100K`: a new edition Pine and a new edition port;
- `striker_dj30_mym_entry_with_stop@Tradeify_Select_100K`: a new edition Pine and a new edition port;
- the SHA-256 of each file.

This is step 2 of that pre-registration's §8 freeze procedure. The editions implement answered rules; they design nothing new.

**Sibling:** the [Vanguard edition production handoff](2026-09-26-vanguard-fixed-stop-edition-production.md) has the same shape and handling rules. If both are dispatched, use one file-naming and pinning convention (§2), and do them sequentially, not in one session.

**Ownership:**
- One local executor, named at dispatch.
- The operator authorizes file creation (§0 G2), answers every rule and freezes the pre-registration.
- The coordinator accepts the return.
- Pin registration (`book_adapters.py`, `book_policy.py`, `BOOK_SOURCES.sha256` or `PORT_MANIFEST.sha256`, the venue-edition ledger) is a **separate reviewed change**, not part of this packet.

**Return boundary:** new private files plus §7 only. Out of scope: replay, E1, screens, backtests, TradingView runs, account access, alerts, drills and spend. Do not edit any existing Pine, port, manifest, registry, the pre-registration or campaign records.

## 0. Dispatch gates (all must hold; otherwise return `BLOCKED — <gate>`)

| Gate | Condition | Where it is recorded |
|---|---|---|
| G0 | Campaign §59 ruling 3 adopted both editions (already satisfied, 2026-09-25). Confirm it has not been withdrawn since. | Campaign record §59 |
| G1 | Pre-registration items answered in words: ORB-2 to ORB-4, STR-2 to STR-6, the §6 replay-modelling choice and the §6 sequential-exit replay model. No `OWED` remains in §3, §4 or §6; the §5 pin rows are exempt, because this packet fills them. | The pre-registration at a named commit |
| G1a | Realization and identity-binding scheme under pre-registration §5 are explicit: reused pins fixed; new output digests supplied by this packet; embedded Pine identity compatible with proposed registration. | G1 commit; separately reviewed identity contract if needed |
| G2 | The operator explicitly authorizes an agent to **create** new private edition files under the paths in §2. §60 grants read access only. | Dispatch message or campaign record |
| G2b | **Allocation gate (operator ruling 2026-09-26: "Yes, gate on allocation").** Producing these edition files waits until the TradingView/CrossTrade [capability allocation and deletion map](2026-09-25-tradeify-capability-allocation-deletion-map.md) is **ACCEPTED** under gate D of the checklist's [T09 gate acceptance record](../../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#t09-gate-acceptance-record), and the accepted map keeps these legs' runtime ports as the controller boundary. A committed or merged map is not acceptance. If the accepted allocation delegates the behavior these ports implement, this packet is withdrawn, not run. | Checklist T09 gate D acceptance record (named revision); allocation map disposition |
| G3 | The pre-registration is **not frozen**, and no replay or E1 output exists for either edition | Pre-registration Status line; campaign record |

Record the pre-registration commit you build against. If the pre-registration changes after that commit, stop and return; do not reconcile.

**Per-leg independence:** if G1 is answered for one leg only, you may produce that leg alone, and must record the other as `BLOCKED — G1 (<leg>)`. Do not guess an unanswered rule.

## 1. Read first

- The [pre-registration](../pre-registration/2026-09-25-tradeify-route-native-editions-prereg.md) at the G1 commit. It is the **only** specification.
- [Rail spec 2026-09-12](../../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) S2 and S3 (a)/(b)/(d)/(e): what the declared expressions do on each leg. The declared ORB uses native trailing, L2(g). The declared Striker enters bare and attaches its stop a bar later, L2(f).
- [REST route assessment §6.5](2026-09-25-crosstrade-rest-route-assessment.md#65-per-leg-primitive-map-step-4): the per-leg primitive map. Any post-entry amend depends on L2(c), which is K here (drill D2).
- Campaign record §59 and §60, and AGENTS.md "Public-clone posture": the handling rules.

## 2. Inputs, outputs and handling

**Inputs.** Read these in place and hash-verify them first. The pins come from `core/strategies/BOOK_SOURCES.sha256`, which also matches `book_adapters.py` and `book_policy.py`.

| Leg | File | Path | SHA-256 |
|---|---|---|---|
| ORB | Pine | `core/strategies/book/orb_mnq_7_reconstruction_venue_bound.pine` | `176c4f70…` |
| ORB | Port | `ops/c1_signal_daemon/ports/orb_mnq_v7.py` | `b1f4e573…` |
| Striker | Pine | `core/strategies/book/striker_dj30_v4.5_mym_pyramid_250_cap100k.pine` | `712cf395…` |
| Striker | Port (**corrected generation**) | `lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/inputs/private_overrides/op1/2026-09-14-seven/step3-coverage/corrected-ports/dj30_mym_p250.py` | `efd479b6…` |

**Striker trap.** The default `ops/c1_signal_daemon/ports/dj30_mym_p250.py` is the preserved original (`c81aa59c…`), which the registry rejects. Never base the edition on it, and never overwrite either Striker generation.

Also read the `effective_inputs.json` that sits beside the ports (`66406dee…`). It tells you which declared branches are active under the accepted binding: ORB adds off under protection, breakeven state, stall-exit state. An input existing in the source does not make it active.

Any file whose hash does not match stops that leg.

**Outputs.** New files only, in the same private roots as the originals, named after the edition id:

| Leg | New Pine | New port |
|---|---|---|
| ORB | `core/strategies/book/orb_mnq_7_fixed_stop_oso.pine` | `ops/c1_signal_daemon/ports/orb_mnq_v7_fixed_stop_oso.py` |
| Striker | `core/strategies/book/striker_dj30_v4.5_mym_entry_with_stop.pine` | `ops/c1_signal_daemon/ports/dj30_mym_p250_entry_with_stop.py` |

Before writing, confirm with `git check-ignore -v` that every output path is ignored. If any path is not ignored, stop: a tracked private file would be published.

If the pre-registration rules an override-only realization for ORB (trailing removed by an effective-input change, with no code change), follow the R1 pattern and identity-compatibility gate in the Vanguard handoff §3: retain both compatible Pine and port identities and produce the successor effective settings. A changed Pine with the unchanged port fails the current loader. If that combination is required, stop for an operator-ruled code edition or separately reviewed identity contract.

**Handling.**
- Never modify, rename or overwrite the accepted Pine, ports or effective inputs.
- Never copy private files outside the primary checkout's private roots (§60).
- Nothing private goes into a tracked file, a PR, a comment or this packet. §7 records behavior as shapes, hashes and `file:line` references into the new files.

## 3. ORB MNQ edition: steps

- [ ] **Remove trailing (ORB-1).** No bracket carries trailing fields on the base or on adds. Entry stays a resting stop entry. As with STR-3, splitting a base or add into one-contract requests happens at the rail after admission, not in the port, so the ORB port still emits one intent per base or add or add, with its fixed stop in the same request.
- [ ] **Fixed stop at entry (ORB-2):** the level as ruled.
- [ ] **Exit that replaces the trail (ORB-3):** use only the existing exit the pre-registration names. Add no new exit logic. If the ruled exit doesn't cover a case you find in the source, stop and return.
- [ ] **Post-entry stop changes (ORB-4):** as ruled. If the answer is "none", confirm that no path amends the stop after entry.
- [ ] **Adds (ORB-5):** keep adds-off under protection as inherited. Keep the stall-exit disabled under adds-off, as the route note records; do not invent a stall action.
- [ ] Opening-range, entry, add-eligibility and every signal condition stay byte-identical.

## 4. Striker MYM edition: steps

- [ ] **Entry carries its stop (STR-1).** The market entry carries its protective stop in the same request. There is no bare entry and no later `ATTACH`, and the delayed-attach path is removed.
- [ ] **Stop level at entry (STR-2):** as ruled. If the ruling is "the level the declared port would issue, computed on the entry bar", show where that value is available on the entry bar. If it isn't available there, stop and return; do not substitute.
- [ ] **One-contract split (STR-3):** the port keeps emitting **one** intent per signal, which the rail admits and sizes once (`BookLegExecution.admit`, `ops/c1_signal_daemon/book_bundle_execution.py:142-182`, which refuses a second entry on a non-empty leg). The split into one-contract requests is a post-admission rail dependency (T09 / TB-I3, incident ADR §A8 rules 9–10), **not port work**. Do not make the port emit N requests. Record the ruled maximum N and any cap as the admitted-quantity bound; the port applies no split logic.
- [ ] **Split outcomes (STR-4):** rail-side. The port's `on_execution` handling of partial and refused outcomes stays as declared unless STR-4 rules a port-visible change. Record any such change; do not add per-request tracking to the port.
- [ ] **Close-time crossed-level exits (STR-5):** as ruled.
- [ ] **Post-entry stop changes (STR-6):** as ruled. The declared Striker amends every bar (breakeven, tightening, ratchet), and any amend that remains depends on L2(c).
- [ ] Every signal condition, pyramid and add-eligibility rule not changed by an STR item stays byte-identical.

## 5. Static verification (both legs, no execution)

1. Produce a line diff of each new file against its original. Classify every hunk by the ORB/STR rule or accepted identity binding it implements; any unclassified hunk fails. Inspect in place without retained private-source extracts.
2. **ORB:** under the pinned effective settings, show that every reachable bracket construction emits null trailing fields and every reachable Pine exit has no active trailing arguments, including entry/add/amend paths. Retained unreachable trailing code is permitted in an override-only realization. Different or missing settings invalidate the proof.
3. **Striker:** show that no path emits an entry without a stop in the same intent, and that no `ATTACH` or delayed-protection path remains.
4. **Both:** list every remaining post-entry amend path by `file:line`. These are the leg's L2(c) dependencies; record them even when the ruling keeps them.
5. A `py_compile` syntax check of the new ports runs **only if** the G2 authorization permits it. Otherwise skip it and say so.
6. Verify the proposed identity tuple without importing private ports: embedded Pine identity, proposed registry Pine/port pins and leg identity, and effective-input source/runtime digests. New Pine bytes require matching embedded identity in a new port under the current loader. Hash every new file and any successor effective settings; registration remains a separate change.

## 6. Forbidden

- Running, importing or backtesting any edition or original, in Python or TradingView.
- Any change not traceable to an answered ORB/STR rule or accepted identity binding. That includes cleanup, refactors, renames inside a file, and comment edits that change behavior.
- Adding a CrossTrade-managed trail, a new exit, a new filter or any parameter change beyond the explicitly ruled edition settings. Changing opening-range, signal, pyramid or allocation logic.
- Basing Striker on the rejected original port, or overwriting either Striker generation.
- Editing the accepted files, the pre-registration or any governance document. Freezing the pre-registration. Treating either edition as qualified.

**Owed follow-ups (not this packet):**
1. A reviewed pin change that adds both editions beside the existing pins.
2. Filling pre-registration §5 with this return's hashes, followed by the operator freeze (pre-registration §8 step 4).
3. `CANDIDATE` rows in the venue-edition ledger for both edition ids.
4. Requalification through the book's production E1.

## 7. Executor return

**Status:** not dispatched.

| Field | ORB MNQ | Striker MYM |
|---|---|---|
| Executor / dispatch revision | | |
| Gates G0–G3, including G1a and G2b (evidence link each) | | |
| Pre-registration commit built against | | |
| Checkout revision, tree state, `doctor` result | | |
| Input hashes (match/mismatch) | | |
| Realization (new port / override-only) | | n/a (new port) |
| `git check-ignore` result per output path | | |
| New file paths and SHA-256 | | |
| Hunk classification (rule → `file:line`) | | |
| Identity tuple and loader compatibility (static evidence) | | |
| Protection proof under pinned effective settings (no trail / no bare entry, file:line) | | |
| Remaining post-entry amend paths (L2(c)) | | |
| Syntax check (run / skipped and why) | | |
| Deviations or stops | | |

**Coordinator disposition:** pending.
