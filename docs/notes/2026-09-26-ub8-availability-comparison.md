# UB-8 bounded availability comparison: preserve-and-block vs Proposed option B (2026-09-26)

**Status:** RETURNED for coordinator review. This is Task 1 of the [B–D packet card](../briefs/handoffs/2026-09-26-bd-packet-parallel-drafts.md). It is a documentary comparison. It changes no code, contract, STATE, plan or ADR, accepts nothing, and grants no drill, access, spend or GO. It answers [incident ADR](../adr/2026-09-17-bounded-platform-protection-incident-contract.md) §A9.1 UB-8 and the §A10 acceptance condition.
**Executor:** assessor subagent (Claude Code, Opus 5.5), branch `claude/ub8-availability`. **Dispatch revision:** `f31157886d624050046f3c64887ce6d720ac8458` (HEAD descends from it; verified). All code and documents were read at that revision.

## 0. Answer first

**Recommendation: it depends on named conditions (§8). By default the first release runs preserve-and-block, so B is not needed for it.** B stays Proposed for a later release, which §A10's acceptance condition already provides for. None of the conditions that would make B worth its burden can be shown today:
- the residual-unknown rate is unmeasured;
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
| ρₓ | Share of the rest resolved across sessions | **0 until D5** shows prior-session lookup works (§6.4) |
| c, k | Per-session probability of a clustered outage, and the symbols it hits (k ≤ 4; rule 10 allows ≤ 1 in flight per symbol) | Unmeasured |
| λ | Residual unknowns per session = (1−ρ)(1−ρₓ)·(p·Σn_s + c·k) | Derived |
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
| 4 | Unknown just before the session reset | The last entry is at or before cutoff D − 15 min ≤ 15:45 ET (halt/resume §5), so the ~17:00 ET reset leaves at least about 75 minutes for the same-session recipe. The case bites when the outage or absent attendance outlasts the reset. After that the block is effectively permanent, since ρₓ = 0 until D5 | Reservation held across sessions. UB-2 requires recalculating the allowance and treats stale inputs as a stop, so the allowance may widen for overnight gap risk. Resume only in a later session after recovery to flat |
| 5 | Partial split, then lost monitoring | While monitoring is out: halt; filled children's stop activation cannot be verified (§2 protection-uncertain row → attended). Afterwards, blocked for good if the child stays unknown | While monitoring is out, identical (rule 11.1–11.3). Afterwards: recovery to flat, resume under 4a. The affected leg's adds depend on whether a sequence with an unknown child counts as "closed" (UB-4, open) |
| 6 | Repeated unknowns across days | The first residual unknown ends automated risk-adds; later ones cannot occur | Allowances accumulate and are never released without evidence (rule 2). Large intents drop out first as n*(q,s) falls; rule 8 stops all risk-adds once R − M − Σa < min w(1,s). Every residual unknown costs another halt and recovery to flat |

## 5. Per-scenario comparison on the five dimensions

| # | Opportunities lost under P | Additional opportunities B admits | Reservation accumulation / exhaustion (B) | Operator interventions and unresolved obligations | Work the scenario exercises |
|---|---|---|---|---|---|
| 1 | 0 | 0, by construction | None | None in either posture | B: prove rule 4′ inert (§A6 replay). P: nothing new |
| 2 | Every automated intent from the event to H: about the intents per session × (H − T₁) | Intents with w(q,s) ≤ R − M − E − a_s after resume. Never a normal-mode full Aegis | One allowance. Exhausted at entry if a_s > R − M − E − min w (rule 4b); then B = P | P: 1 halt, 1 permanent obligation. B: the same, plus 1 resume, then 4a on every later admission | B: C06b loss model; C15b; UB-10 record; 4c transfer (UB-7) |
| 3 | Same as 2 | As 2 with Σ over k allowances, so a smaller admissible set | k allowances in one event, so n* is reached k times faster | P: 1 halt, k obligations. B: 1 halt, k obligations, 1 resume | B: rule 11 "required monitoring" list and thresholds (OPEN) |
| 4 | Same as 2 once the reset passes with the unknown unresolved | As 2, from a later session | One allowance; it may be recalculated wider for gap risk (UB-2) | Same as 2; attended past the planned end (halt/resume §3) | Both: D5 read. B: UB-2 recalculation and stale-input rule; UB-6 |
| 5 | Same as 2; nothing while monitoring is out | As 2 after restoration. Affected-leg adds: UB-4 open | One allowance for the unknown child. Unsent children are released (UB-4) | Both: attended protection check on the filled children plus the unknown child. B: plus 1 resume | B: UB-4, UB-10 states, rule 11. Both: T13 channels |
| 6 | Same as 2; the loss is fixed at the first event | Continues until Σ a reaches exhaustion. Expected residuals by session t ≈ λt, so large intents stop near λt ≈ n*(q,s) and all risk-adds near λt ≈ n*(1,s_min) | Monotone. R moves with equity, so the exhaustion session is path-dependent | P: 1 halt. B: one halt, recovery to flat and resume per residual unknown | B: 4a accumulation, UB-9/rule 12 re-evaluation, calibration (UB-6) |

## 6. Break-even conditions (where the conclusion flips)

Illustration only: residual unknowns arrive at rate λ per session, independently. Clustering (c, k) changes how many arrive at once, which matters under B, but has little effect on whether at least one arrives, which is what decides P.

| # | Condition | If it holds | If it fails |
|---|---|---|---|
| BE-1 Frequency floor | P(≥ 1 residual in H) = 1 − e^(−λH) is at or below the operator's tolerance ε for ending automated trading in the first release | B is not needed: P almost never binds | P's expected loss ≈ H − (1 − e^(−λH))/λ sessions; go to BE-2 |
| BE-2 Room | R − M − E − a_s ≥ w(q,s) for the intents that matter (n* ≥ 1; ≥ 2 to survive a second event) | B admits a real subset after resume | B = P after the first unknown (rule 4b). B not needed |
| BE-3 Frequency ceiling | λH < n* | B carries the horizon | B postpones the end rather than preventing it. Route reliability is the binding problem, not the posture |
| BE-4 Recoverability | D4/D5 show residual unknowns become positively resolvable within latency τ | P's block lasts about τ, not the rest of the account; B's gain shrinks to about λHτ sessions. B not needed | P's block stays open-ended |
| BE-5 Continuity form | The operator values *resume after recovery to flat, per residual unknown* (texts as written) | B's gain per event = sessions after that recovery | B's value needs a further §2/§3 amendment (Q1), which adds to its burden |
| BE-6 Burden | The value of the sessions B recovers exceeds B's build, verification and governance cost (§7) plus its normal-path risk. That value is not estimated here (no P&L) | B needed | P |

**The band where B pays.** B earns its place only when BE-1 fails, BE-2 and BE-3 hold, BE-4 fails and BE-5 is accepted: roughly ε < λH < n*. The band is empty if n* < 1, or if D5 makes residual unknowns recoverable.

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

**Form: conditional. Default for the first release: preserve-and-block; B not needed.** B becomes needed for the first release only if **all** of these hold:
- **C1:** evidence puts λH above the operator's tolerance ε. The sources are D1/D4/D5 traces or attended-session records; there is no estimate today.
- **C2:** the bound UB-2/UB-6 figures give n* ≥ 1, preferably ≥ 2, for the book's typical intents at typical open exposure E.
- **C3:** λH < n*, so B carries the horizon rather than postponing the end.
- **C4:** D4/D5 do not make residual unknowns resolvable within a bounded time.
- **C5:** the operator accepts continuity as *resume after recovery to flat per event*, or rules a further §2/§3 amendment (Q1).

C2 needs figures, C1, C3 and C4 need evidence, and C5 is a ruling. None can be decided now, and none of them blocks the first release under P.

**Decisive assumptions:**
1. Only unknowns still unresolved after the same-session REST recipe matter. Found orders resolve positively under both postures (A1).
2. The first release is attended, bounded and GO-per-session, so H is short. A long H strengthens the case for B.
3. The texts stand as written: B keeps the §2 halt and the §3 recovery to flat.
4. Capacity rule 5 plus the 80-micro cap means that under B any held unknown excludes a normal-mode full-size Aegis intent.
5. No value per session is estimated, so BE-6 is the operator's judgment.

## 9. Limitations

- There is no failure-rate estimate, and no trace of any REST outcome: every drill is "Not demonstrated". The Poisson model only illustrates the break-even conditions.
- "Opportunities" are counted as intents or sessions, not money.
- B's exhaustion is stated only as inequalities in unbound symbols. Nothing here says how many unknowns end trading.
- The halt reading (§2) is derived from the halt/resume and §A5 texts. The coordinator or operator may intend otherwise (Q1).
- The code was read, not executed. The Aegis takeover interaction and the fence's treatment of accepted attempts (Q2) were not traced end to end.
- Per-intent quantities may change at edition freeze (UB-4, D10). Private ports were not read.

## 10. Open questions for the coordinator

- **Q1.** Does B intend narrowed-shape unknowns to keep halt/resume §2's halt and §3's recovery to flat? §A5 leaves both in place, while rule 4′ reads like continuous admission. The answer changes B's value (BE-5) and its burden.
- **Q2.** The fence also counts an **accepted** entry/add attempt as unresolved once one bar period has passed without an accepted terminal (`:787-797`). Read literally, a resting ORB stop entry would refuse account-wide risk-adds after 15 minutes under P. Under B, it would put the account in exceptional mode, because rule 4′ defines that mode by this fence. Is that intended? This was not traced to tests.
- **Q3.** Under B, should a held unknown's reservation that blocks a full-size Aegis intent (80 of 80) be accepted as a capacity consequence, or excluded from takeover arithmetic? The current code refuses the intent or leaves the takeover unable to complete.
- **Q4.** H and ε are the operator's to set. Without them, BE-1 cannot be evaluated.
- **Q5.** For add eligibility, does a split with an unknown child count as a "closed" submission sequence (UB-4)?
