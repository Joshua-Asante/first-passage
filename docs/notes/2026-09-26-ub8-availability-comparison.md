# UB-8 bounded availability comparison: preserve-and-block vs Proposed option B (2026-09-26)

**Status:** RETURNED for coordinator review. This is Task 1 of the [B–D packet card](../briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md). It is a documentary comparison. It changes no code, contract, STATE, plan or ADR, accepts nothing, and grants no drill, access, spend or GO. It answers [incident ADR](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) §A9.1 UB-8 and the §A10 acceptance condition.
**Executor:** assessor subagent (Claude Code, Opus 5.5), branch `claude/ub8-availability`. **Dispatch revision:** `f31157886d624050046f3c64887ce6d720ac8458` (HEAD descends from it; verified). All code and documents were read at that revision.

## Corrections (executive review 2026-09-26) — these govern

Recommended (executive review 2026-09-26); operator ruling pending. Where the text below conflicts with this table, the table governs. Edited sentences carry **[Corr. N]**; superseded wording is struck through where seeing it helps. These corrections limit how far the note can be relied on quantitatively. They accept no gate and authorize no drill.

| # | Correction | Edited in |
|---|---|---|
| 1 | **Cross-session recovery is unknown, not an observed zero rate.** The REST assessment records it as "not established" (§6.4, session-boundary bullet), and D5 is untested and unauthorized. ρₓ = 0 may appear only as a labelled conservative scenario. | §3 ρₓ; §4 row 4; §5 rows 2 and 6 |
| 2 | **One successful prior-session lookup (D5) would not establish a recovery-time bound τ for every unknown.** D5 as defined is a lifecycle read by id for a prior-session order (REST §6.6, session-reset row; §6.9, D5). Whether any read reaches a request whose `orderId` was not learned before the reset is unestablished, not impossible (same row); one D5 success would not show that coverage. It also says nothing about orders our id does not correlate (repair-placed OCO pairs, copier fan-out; §6.6) or about timing. BE-4 needs a demonstrated recovery mechanism, shown coverage of the unknown classes that matter, and a supported τ. | BE-4; band; C4 |
| 3 | **Clustered outages change both the number of unknowns per event and the probability of any disruption.** The Poisson arithmetic (1 − e^(−λH), λt, λHτ, P's expected loss) is illustrative only. It is not an acceptance test. | §0; §3 λ; §5 row 6; §6 preamble; BE-1; BE-4; §9 |
| 4 | **B can have value even if it only postpones exhaustion or shortens a recoverable block.** The break-even conditions are not all logically necessary. The §6 band statement ("B earns its place only when … roughly ε < λH < n*") is an illustrative sufficient-condition sketch, not a necessary condition. | §0; BE-3; BE-4; band; §8 lead-in, C3, C4 |
| 5 | **No numerical tolerance ε is requested.** Without a defensible failure-rate estimate, a tolerance cannot establish readiness. The operator decision is whether to accept the concrete consequence: *one unresolved request may suspend automation on this account indefinitely* (as the note reads the sources, not executive-review wording: automated trading on the account stays halted, since recovery cannot complete and resume is refused while a request is unresolved, halt/resume §3–§4; the owner code's risk-add fence, §2, is the part implemented today; manual trading, including the weekly preservation trade, is unaffected, scope §1). Recommended horizon: one attended session, then explicit review. This supersedes the routing of ε under Q4 in the coordinator review; H stays an operator input. | §0; BE-1; band; C1; §8 closing lines; Q4; coordinator review Q4 (pointer only) |
| 6 | **These corrections do not overturn the scope recommendation:** the first release runs preserve-and-block, and B stays Proposed. | — |

## 0. Answer first

**Recommendation: it depends on named conditions (§8). By default the first release runs preserve-and-block, so B is not needed for it.** B stays Proposed for a later release, which §A10's acceptance condition already provides for. ~~None of the conditions that would make B worth its burden can be shown today:~~ The §8 conditions are an illustrative sufficient set, not all necessary. C1 and C5 are pending operator rulings; C2–C4 need figures or evidence that do not exist today **[Corr. 4, 5]**:
- the residual-unknown rate is unmeasured, so the note's arithmetic is illustrative only and no tolerance is requested **[Corr. 3, 5]**;
- B's room figures are unbound (UB-2, UB-6);
- as the texts stand, B's continuity means resuming after an attended recovery to flat with the reservation still held. It does not mean uninterrupted trading (§2).

**UB-8 does not make an unqualified close route viable.** D19 is a separate first-order blocker ([allocation map](2026-09-25-tradeify-capability-allocation-deletion-map.md), corrected decision list). The rail contract's `CLOSE(scope)` and S5 need verified L2(d) and L2(e), and L2(e) is contradicted on this route. No close route is viable until a route-native close and protection cleanup is defined and qualified, or the close contract is amended. Neither posture changes that, and neither changes the gate-C K primitives (D1–D3, D6, takeover composite).

## 1. Inputs and reading rules

| Source (at `f311578`) | Used for |
|---|---|
| Incident ADR §A1–§A10 | B's rules: 4′, 4a–4c, 9′, 11, 12, rule 8 exhaustion, rule 5 capacity, rule 2 release; §A5 propagation text; §A6 falsifiers |
| Allocation map, "Coordinator-corrected recommendation and decision list" first, then rows C06b, C15, C15b, B13, B16 and §B | Burden comparison; D19; the E1 freeze-inventory effect of owner changes |
| [Scope note](../superpowers/specs/2026-09-24-bounded-exposure-unknown-request-amendment-scope.md) §1–§4 | What preserve-and-block does to the account; invariants both postures keep |
| [REST assessment](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md) §6.3, §6.4, §6.6, [§6.11](../briefs/handoffs/2026-09-25-crosstrade-rest-route-assessment.md#611-gate-a-factual-disposition) | What can resolve an unknown: same-session positive lookup only (A1); no no-send status (A3); a session reset at about 17:00 ET (Q22); every drill "Not demonstrated" |
| [Halt/resume contract](../spec/2026-09-14-tb-s3-halt-resume-contract.md) §2–§5 | Halt trigger, recovery-complete condition, resume, schedule |
| `ops/c1_rail/book_account_owner.py` :759–798, :1605–1704 | Current fence and admission |
| `ops/c1_rail/book_capacity.py` :137–190, :260–288; `ops/c1_rail/book_policy.py` :63, :132, :177–196 | Capacity arithmetic; per-intent quantities |

**Frequencies are symbolic.** No tracked public document gives this route's lost-response rate, its residual-unknown rate, or the book's requests per session. The only counts used are per-intent quantities from public tracked code. No private source, effective input, local artifact, account figure or P&L was read.

## 2. The two postures as the texts and code stand

| Aspect | Preserve-and-block, "P" (current) | Proposed B (§A10) |
|---|---|---|
| What fences | Any unresolved entry/add attempt refuses **every** risk-add on **every** leg (`unknown_order`, `:1608`; fence `:768-798`) | A narrowed-shape unknown puts the account in exceptional mode (rule 4′). Non-entry unknowns keep the leg block and attended handling (§A2 rule 7), as under P |
| Halt on the event | Halt/resume §2 row 1: an "uncertain transport/order outcome" publishes a durable halt into INTERVENTION. The owner code as read records `UNKNOWN` and fences without halting (`:1686-1704`); the contract's halt is TB-I3 scope | **Same.** §A5 amends halt/resume §3 ¶2 and §4, not the §2 trigger row |
| Recovery complete | Needs "no unresolved requests" (§3 ¶2), so it **never completes** while a residual unknown exists | §A5 lets recovery complete with the reservation held. The rest of §3 stands: zero gross positions, no working orders or orphans |
| Resume | Refused: "unresolved owner cannot be overridden" (§4) | A fresh operator resume (§4), plus rule 11.3. Admission then runs under rule 4a for as long as the unknown is held |
| Admission afterwards | None | R − M ≥ Σ a(held) + E + w(intent) (4a, 9′), re-run after every revoking event (rule 12). Stops on stale monitoring (rule 11) |
| Capacity | Held contracts stay `reserved` | Same (rule 5; `book_capacity.py:137-154`) |
| Release | Only uniquely correlated accepted evidence (A1, A3) | Same (rule 2), plus optional vendor bound A |

**Consequence.** On the event session the two postures behave identically: halt, attended intervention, and an attended close under INTERVENTION. They differ only afterwards. Under P, automated risk-adds never return while the unknown stays unresolved; manual trading, including the weekly preservation trade, is unaffected (scope §1). Under B they can return after an attended recovery to flat and a fresh resume, but only under the stricter exceptional-mode check. **Continuation without a halt and a return to flat would need a further amendment of halt/resume §2 and §3, which §A5 does not propose** (open question Q1).

## 3. Symbols

| Symbol | Meaning | Status |
|---|---|---|
| H | Sessions in the first-release horizon | Operator. Each armed session needs its own GO, so H is not fixed |
| n_s | One-contract child requests per session on symbol s (= intent quantities, §A1, §A8) | No public count. Per-intent quantities are below |
| p | Probability that a child's transport outcome is unknown | Unmeasured; no trace exists (§6.11 drill map) |
| ρ | Share of unknowns positively resolved in the same session (REST recipe, A1) | Unmeasured; D4 unauthorized |
| ρₓ | Share of the rest resolved across sessions | ~~**0 until D5** shows prior-session lookup works (§6.4)~~ **Unknown**: cross-session recovery is not established (§6.4). ρₓ = 0 is a labelled conservative scenario only **[Corr. 1]** |
| c, k | Per-session probability of a clustered outage, and the symbols it hits (k ≤ 4; rule 10 allows ≤ 1 in flight per symbol) | Unmeasured |
| λ | Residual unknowns per session = (1−ρ)(1−ρₓ)·(p·Σn_s + c·k) | Derived. An expected count; when outages cluster it is not an independent-arrival rate **[Corr. 3]** |
| R, M | Room to the intraday-enforced venue floor; reserve margin | UB-6, unbound (§A3) |
| a_s | Conditional loss allowance per held unknown on s | UB-2, unbound |
| E | Remaining loss exposure of open positions and acknowledged working entries (4a) | Varies with the book |
| w(q,s) | Allowance of a new q-child intent on s (9′) | Unbound |
| n*(q,s) | Held allowances that still admit a q-child intent on s: the largest n with n·ā ≤ R − M − E − w(q,s) | Derived; exhaustion comes only from this inequality |

**Per-intent quantities** (public, `book_policy.py:177-196`; protected mode scales Aegis, Vanguard and Striker to 40%):
- Aegis: 8 contracts of 6J at 10 micro-equivalents each, which is 80, the whole account cap (`:63`, `:132`).
- Striker: base 1–22, plus one add at 250% of confirmed base.
- Vanguard: base 1–2, plus up to two adds.
- ORB: 1, plus up to two one-contract adds.

## 4. Scenario × posture matrix

| # | Scenario | P | B |
|---|---|---|---|
| 1 | No unresolved requests | Normal admission | Byte-identical normal admission by rule 4′; §A6 replay falsifier must prove it |
| 2 | One unknown stays unresolved | Halt → attended close. Automated risk-adds end for the account unless later positive evidence arrives | Same event handling → recovery to flat → resume. Intents admitted iff w ≤ R − M − E − a_s. Exceptional mode is permanent (rule 2). A full-size normal-mode Aegis intent can no longer be admitted: its 80 needs the whole cap, so a held 6J unknown refuses it, and with a held unknown elsewhere a takeover cannot complete while a displaced leg holds a reservation (`book_capacity.py:277-280`) |
| 3 | Several symbols hit by one outage | Same as 2; the count is irrelevant | Up to k ≤ 4 held allowances at once (rule 10), charged together. Rule 11.1 (and halt/resume §2 "loss of required broker evidence") stop everything until reconciliation. Then as 2 with Σ a over k |
| 4 | Unknown just before the session reset | The last entry is at or before cutoff D − 15 min ≤ 15:45 ET (halt/resume §5), so the ~17:00 ET reset leaves at least about 75 minutes for the same-session recipe. The case bites when the outage or absent attendance outlasts the reset. After that the block ~~is effectively permanent, since ρₓ = 0 until D5~~ has no known end: cross-session recovery is unknown, not zero **[Corr. 1]** | Reservation held across sessions. UB-2 requires recalculating the allowance and treats stale inputs as a stop, so the allowance may widen for overnight gap risk. Resume only in a later session after recovery to flat |
| 5 | Partial split, then lost monitoring | While monitoring is out: halt; filled children's stop activation cannot be verified (§2 protection-uncertain row → attended). Afterwards, blocked for good if the child stays unknown | While monitoring is out, identical (rule 11.1–11.3). Afterwards: recovery to flat, resume under 4a. The affected leg's adds depend on whether a sequence with an unknown child counts as "closed" (UB-4, open) |
| 6 | Repeated unknowns across days | The first residual unknown ends automated risk-adds; later ones cannot occur | Allowances accumulate and are never released without evidence (rule 2). Large intents drop out first as n*(q,s) falls; rule 8 stops all risk-adds once R − M − Σa < min w(1,s). Every residual unknown costs another halt and recovery to flat |

## 5. Per-scenario comparison on the five dimensions

| # | Opportunities lost under P | Additional opportunities B admits | Reservation accumulation / exhaustion (B) | Operator interventions and unresolved obligations | Work the scenario exercises |
|---|---|---|---|---|---|
| 1 | 0 | 0, by construction | None | None in either posture | B: prove rule 4′ inert (§A6 replay). P: nothing new |
| 2 | Every automated intent from the event to H while the unknown stays unresolved (ρₓ = 0 is the conservative scenario) **[Corr. 1]**: about the intents per session × (H − T₁) | Intents with w(q,s) ≤ R − M − E − a_s after resume. Never a normal-mode full Aegis | One allowance. Exhausted at entry if a_s > R − M − E − min w (rule 4b); then B = P | P: 1 halt, 1 ~~permanent~~ open-ended obligation (cross-session recovery unknown) **[Corr. 1]**. B: the same, plus 1 resume, then 4a on every later admission | B: C06b loss model; C15b; UB-10 record; 4c transfer (UB-7) |
| 3 | Same as 2 | As 2 with Σ over k allowances, so a smaller admissible set | k allowances in one event, so n* is reached k times faster | P: 1 halt, k obligations. B: 1 halt, k obligations, 1 resume | B: rule 11 "required monitoring" list and thresholds (OPEN) |
| 4 | Same as 2 once the reset passes with the unknown unresolved | As 2, from a later session | One allowance; it may be recalculated wider for gap risk (UB-2) | Same as 2; attended past the planned end (halt/resume §3) | Both: D5 read. B: UB-2 recalculation and stale-input rule; UB-6 |
| 5 | Same as 2; nothing while monitoring is out | As 2 after restoration. Affected-leg adds: UB-4 open | One allowance for the unknown child. Unsent children are released (UB-4) | Both: attended protection check on the filled children plus the unknown child. B: plus 1 resume | B: UB-4, UB-10 states, rule 11. Both: T13 channels |
| 6 | Same as 2; the loss is fixed at the first event while that unknown stays unresolved **[Corr. 1]** | Continues until Σ a reaches exhaustion. Expected residuals by session t ≈ λt, so large intents stop near λt ≈ n*(q,s) and all risk-adds near λt ≈ n*(1,s_min) (illustrative; clustering changes the path **[Corr. 3]**) | Monotone. R moves with equity, so the exhaustion session is path-dependent | P: 1 halt. B: one halt, recovery to flat and resume per residual unknown | B: 4a accumulation, UB-9/rule 12 re-evaluation, calibration (UB-6) |

## 6. Break-even conditions (where the conclusion flips)

Illustration only, not an acceptance test **[Corr. 3]**: residual unknowns arrive at rate λ per session, independently. ~~Clustering (c, k) changes how many arrive at once, which matters under B, but has little effect on whether at least one arrives, which is what decides P.~~ Clustering (c, k) changes both how many arrive at once (which matters under B) and the probability of any disruption (which decides P), so the formulas below do not hold under it **[Corr. 3]**.

| # | Condition | If it holds | If it fails |
|---|---|---|---|
| BE-1 ~~Frequency floor~~ Consequence accepted **[Corr. 5]** | ~~P(≥ 1 residual in H) = 1 − e^(−λH) is at or below the operator's tolerance ε for ending automated trading in the first release~~ The operator accepts that one unresolved request may suspend automation on this account indefinitely, over the chosen horizon (recommended: one attended session, then explicit review) | B is not needed ~~: P almost never binds~~ for that horizon: P's consequence is accepted | P's cost is the automated sessions lost after the first residual unknown (illustratively ≈ H − (1 − e^(−λH))/λ under independent arrivals **[Corr. 3]**); go to BE-2 |
| BE-2 Room | R − M − E − a_s ≥ w(q,s) for the intents that matter (n* ≥ 1; ≥ 2 to survive a second event) | B admits a real subset after resume | B = P after the first unknown (rule 4b). B not needed |
| BE-3 Frequency ceiling | λH < n* | B carries the horizon | B postpones the end rather than preventing it. Route reliability is the binding problem, not the posture. Postponing the end can still have value, so this is not a reason to reject B **[Corr. 4]** |
| BE-4 Recoverability | ~~D4/D5 show residual unknowns become positively resolvable within latency τ~~ A demonstrated recovery mechanism resolves residual unknowns positively, with shown coverage of the unknown classes that matter (including requests whose `orderId` was never learned) and a supported bound τ. One successful D5 lookup does not establish τ **[Corr. 2]** | P's block is recoverable and lasts about τ, not the rest of the account; B's gain shrinks (illustratively ≈ λHτ sessions). ~~B not needed~~ B may still have value if it shortens that block **[Corr. 3, 4]** | P's block stays open-ended |
| BE-5 Continuity form | The operator values *resume after recovery to flat, per residual unknown* (texts as written) | B's gain per event = sessions after that recovery | B's value needs a further §2/§3 amendment (Q1), which adds to its burden |
| BE-6 Burden | The value of the sessions B recovers exceeds B's build, verification and governance cost (§7) plus its normal-path risk. That value is not estimated here (no P&L) | B needed | P |

**The band where B pays: an illustrative sufficient-condition sketch, not a necessary condition [Corr. 4].** ~~B earns its place only when BE-1 fails, BE-2 and BE-3 hold, BE-4 fails and BE-5 is accepted: roughly ε < λH < n*. The band is empty if n* < 1, or if D5 makes residual unknowns recoverable.~~ B's case is clearest when the operator does not accept P's consequence (BE-1 fails), B keeps admissible room (BE-2), B carries the horizon (BE-3), no demonstrated mechanism bounds P's block (BE-4 fails) and resume-after-flat is accepted (BE-5). Not all of these are necessary: B can still have value if it only postpones exhaustion or shortens a recoverable block. If n* < 1, B equals P after an unknown (BE-2) **[Corr. 2, 4, 5]**.

## 7. Implementation and verification burden

| Item | P | B | Owner / source |
|---|---|---|---|
| Unknown fence (C15) | Exists (`:768-798`, `:1608`) | Split narrowed-shape unknowns out of the refusal (§A5 last row) | Allocation map C15 |
| Both postures need these anyway | Outcome classifier per Gate A A3 (i)–(iii); REST producer and post-placement poll (B15, A7); D4/D5 reads (D12); 1-lot split and whole-intent capacity (B13, C09); UB-4, UB-5; D19; gate-C K primitives | Same | Allocation map C13–C15, B13, B15, D12 |
| Account-wide loss check (C06b) | None | **New engineering**: held allowances + open positions + working entries + new intent, without double-counting equity (UB-1 adj.) | C06b, D11 |
| Reservation-held unknowns (C15b) | None | UB-10 per-child record extending `attempts` (`:764`, `:791`, `:1674`); UB-9 revoking events; UB-3 stops | C15b, D11 |
| Deferred package (B16) | Not built | Built only if B is needed for the first release | B16: DEFER until UB-8 and acceptance |
| §A10 OPEN items | — | (1) 4a floor, formula, inputs, stale data, calibration (UB-6); (2) which component computes 4a, from what observations; (3) 4c resolution evidence and transfer (UB-7); (4) 9′ partial split (UB-4); (5) rule 11 required monitoring and staleness thresholds; (6) rule 12 stream vs poll (Gate A A7) | §A10 |
| Qualification | Current fence stays in the E1 freeze inventory | Changes `book_account_owner` (the `listener_account_owner` role), so it re-enters the freeze inventory. §A6 falsifiers: byte-identical no-unknowns replay; T13 measurement of failed-stop detection within the room left | Allocation map §B; §A6 |
| Governance | None | §A8 step-4 reviews (refute-first, then cross-vendor); §A5 propagation to five owners; Q1 amendment if continuation without a halt is intended | §A5, §A8 |
| Rule 10 sequencing | Not needed for unknown accounting: the first unknown fences later children. D10 decides it on other grounds | Needed for the one-per-symbol bound | B13 (PROVISIONAL-B) |

## 8. Recommendation and decisive assumptions

**Form: conditional. Default for the first release: preserve-and-block; B not needed.** ~~B becomes needed for the first release only if **all** of these hold:~~ The case for B in the first release is clearest when all of these hold. They are an illustrative sufficient set, not all necessary **[Corr. 4]**:
- **C1:** ~~evidence puts λH above the operator's tolerance ε. The sources are D1/D4/D5 traces or attended-session records; there is no estimate today.~~ the operator does not accept that one unresolved request may suspend automation on this account indefinitely over the chosen horizon **[Corr. 5]**. D1/D4/D5 traces or attended-session records would inform that ruling; there is no estimate today.
- **C2:** the bound UB-2/UB-6 figures give n* ≥ 1, preferably ≥ 2, for the book's typical intents at typical open exposure E.
- **C3:** λH < n*, so B carries the horizon rather than postponing the end. If it fails, postponing the end can still have value **[Corr. 4]**.
- **C4:** ~~D4/D5 do not make residual unknowns resolvable within a bounded time.~~ no demonstrated recovery mechanism, with coverage of the residual unknowns that matter, bounds P's block; one D5 success would not **[Corr. 2]**. If one does, B may still shorten the block **[Corr. 4]**.
- **C5:** the operator accepts continuity as *resume after recovery to flat per event*, or rules a further §2/§3 amendment (Q1).

~~C2 needs figures, C1, C3 and C4 need evidence, and C5 is a ruling. None can be decided now, and none of them blocks the first release under P.~~ C2 needs figures, and C3 and C4 need evidence; none exists today. C1 and C5 are operator rulings, pending **[Corr. 5]**. The operator decision Correction 5 names, whether to accept P's consequence for the chosen horizon, stays open (Q4).

**Decisive assumptions:**
1. Only unknowns still unresolved after the same-session REST recipe matter. Found orders resolve positively under both postures (A1).
2. The first release is attended, bounded and GO-per-session, so H is short. A long H strengthens the case for B.
3. The texts stand as written: B keeps the §2 halt and the §3 recovery to flat.
4. Capacity rule 5 plus the 80-micro cap means that under B any held unknown excludes a normal-mode full-size Aegis intent.
5. No value per session is estimated, so BE-6 is the operator's judgment.

## 9. Limitations

- There is no failure-rate estimate, and no trace of any REST outcome: every drill is "Not demonstrated". The Poisson model only illustrates the break-even conditions; it is not an acceptance test, and clustering breaks it **[Corr. 3]**.
- "Opportunities" are counted as intents or sessions, not money.
- B's exhaustion is stated only as inequalities in unbound symbols. Nothing here says how many unknowns end trading.
- The halt reading (§2) is derived from the halt/resume and §A5 texts. The coordinator or operator may intend otherwise (Q1).
- The code was read, not executed. The Aegis takeover interaction and the fence's treatment of accepted attempts (Q2) were not traced end to end.
- Per-intent quantities may change at edition freeze (UB-4, D10). Private ports were not read.

## 10. Open questions for the coordinator

- **Q1.** Does B intend narrowed-shape unknowns to keep halt/resume §2's halt and §3's recovery to flat? §A5 leaves both in place, while rule 4′ reads like continuous admission. The answer changes B's value (BE-5) and its burden.
- **Q2.** The fence also counts an **accepted** entry/add attempt as unresolved once one bar period has passed without an accepted terminal (`:787-797`). Read literally, a resting ORB stop entry would refuse account-wide risk-adds after 15 minutes under P. Under B, it would put the account in exceptional mode, because rule 4′ defines that mode by this fence. Is that intended? This was not traced to tests.
- **Q3.** Under B, should a held unknown's reservation that blocks a full-size Aegis intent (80 of 80) be accepted as a capacity consequence, or excluded from takeover arithmetic? The current code refuses the intent or leaves the takeover unable to complete.
- **Q4.** ~~H and ε are the operator's to set. Without them, BE-1 cannot be evaluated.~~ H is the operator's to set; no numerical ε is requested. The operator decides whether to accept that one unresolved request may suspend automation on this account indefinitely. Recommended: one attended session, then explicit review **[Corr. 5]**.
- **Q5.** For add eligibility, does a split with an unknown child count as a "closed" submission sequence (UB-4)?

---

## Coordinator review (2026-09-26): ACCEPTED AS INPUT

Reviewer: the coordinating session. Artifact: `8350157`. The comparison meets its card: both postures under the same six scenarios, symbolic figures, break-even conditions instead of a failure rate, burden compared, and D19 kept separate. The open questions were checked against source:

- **Q1 — confirmed; contract conflict for gate B.** Halt/resume §2 halts on any "uncertain transport/order outcome". §A5 amends only §3 ¶2 and §4. As written, B gives *resume after an attended return to flat*, not continuous admission, while §A10 rule 4′ reads as continuous admission. The operator must choose: amend §2 as well (B continuous), or accept B as resume-after-flat. That choice changes BE-5 and B's burden.
- **Q2 — confirmed as a code/spec divergence; a gate-C/T09 item before the ORB freeze.** The spec's S1 one-bar cut makes an order UNKNOWN when there is **no order-level evidence** for a bar (the kernel refreshes `last_evidence_at`). The production fence (`book_account_owner.py:787-797`) counts any accepted entry or add with **no accepted terminal** one bar after preparation. Rail S2/RC-9 cancels a resting entry older than one bar unless it is re-issued, and the allocation map (C08) found the ORB port cancels only at session end. The resting-entry lifecycle, the fence semantics and ORB behavior must be reconciled and traced. Under B, this also decides when exceptional mode begins (rule 4′ is defined by this fence).
- **Q3 — takeover condition confirmed; capacity arithmetic plausible, not traced.** `book_capacity.py:277-278` requires displaced legs to hold neither confirmed nor reserved capacity. Whether a held reservation blocks a full-size Aegis entry is recorded as a stated consequence to accept or reject under B.
- **Q4 (H, ε) and Q5 (a split with an unknown child counting as "closed") go to the operator decision list.** **[ε superseded by Corr. 5: no ε is requested; H stays an operator input]**

