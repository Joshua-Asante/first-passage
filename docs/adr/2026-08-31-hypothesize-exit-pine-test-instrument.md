# Hypothesize-exit frozen Pine test instrument for trading investigations, plus manual-TradingView-look K accounting — `hypothesize-exit-pine-test-instrument`

**Status:** `Proposed` — drafted by Claude Code, ratification is an operator decision. Date below is the draft date, not a ratification date — see §6.
**Decision date:** 2026-08-31
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Claude Code (drafter, independent review of PR #229)
**Layer:** methodology (INQHIORI Hypothesize-phase exit contract for trading investigations only; the general-purpose loop is unchanged). No `dd_protection`, allocation, lifecycle, or rail config touched; nothing armed; no venue action; no spend.
**Tier:** full — creates a standing exit requirement on the H phase for every future trading investigation.

---

## §0 — Rule 0 reads (production-source verification)

Files read in full before drafting this ADR:

- `docs/spec/2026-08-31-inqhiori-mechanism-to-trade-bridge.md` (PR #229, open, not merged) — the artifact this ADR triages. §5 ("Hypothesize exit — frozen Pine test instrument") and §6.3 (manual-TradingView-look multiplicity accounting) are the two clauses this ADR ratifies. The rest is explicitly **not** ratified here — see §3 below.
- `docs/methodology/inqhiori-canon.md` (all 16 sections) — canon's own phase diagram (§1: `I → N → [D→S→A] → Q → H → I → O → R → I`) confirms Hypothesize (H) is a real, named phase; canon defines no exit contract for it today (only Notice's exit, and the closure-resident Iterate exit added by §16, 2026-08-04). This ADR is the first to define an H-exit contract, scoped to trading investigations.
- `docs/adr/2026-08-30-candidate-contract.md` — the founding-freeze admission gate (declared fields: signal, entry clock, stop, exit/target, holding horizon, costed payoff unit). Confirmed via full-text grep: contains no Pine/TradingView/`strategy()` content. Does not conflict with a Hypothesize-exit Pine requirement — candidate-contract freezes *declared fields*, this ADR freezes *executable test code* built from those fields, one phase later.
- `docs/adr/2026-08-30-terminal-taxonomy.md` — confirm-phase verdict vocabulary (`CONFIRMED`/`MARKET-NULL`/`EXPRESSION-FAIL`/`EVIDENCE-VOID`, orthogonal `VENUE-FAIL` edition axis). Not touched by this ADR; the Pine test instrument is an *input* to a future confirm read, not a new verdict class.
- `docs/adr/2026-08-30-evaluation-order.md` — step 6 ("Explore," K-ledger-bound, closed by an append-only selection freeze) and step 9 (one atomic untouched confirm run, multiplicity-adjusted). Confirmed via full-text grep: no Pine/TradingView content. This ADR does not redefine "Explore" or "confirm" — see §4 (deferred items) for why PR #229's §6 is *not* ratified here.
- `docs/adr/2026-08-30-operator-approvals-campaign-envelope.md` — the multiplicity/K-spend envelope, explicitly orthogonal to Rule 2's iteration budget (§2, lines 176–180: "Neither this ADR nor Rule 2 is amended by the other"). The manual-TradingView-look accounting this ADR ratifies (§2 below) is wired into this envelope's multiplicity configuration by citation, not reinvented.
- `docs/adr/2026-06-16-rule-2-budget-before-acting.md` + canon §15 — Rule 2's OUTER-8 iteration budget. Checked independently this session (`docs/notes/audits/rule-2-trip-log.md`): **zero scripts anywhere in the repo enforce this budget** (`grep -rl "rule.2\|rule_2\|OUTER.*8" scripts/*.py` returns no hits); the trip-log itself is hand-appended prose with 3 rows total since codification (2026-06-16); its own audit trail documents a missed 2026-08-08 quarterly check that was never recorded as having not run until a later, unrelated sweep caught it. PR #229's §4 (weighted LIGHT/STANDARD/HEAVY phase budgets) proposes to amend this ADR specifically — not the six 2026-08-30 ADRs — and is not ratified here; see §4 below.
- `ops/instruments/MECHANISMS.md` — confirms the conditioner-role vocabulary is already live practice, tagged "Conditioner-role, not entry-role" since 2026-08-18 (13 days before PR #229 proposed the same concept as a new CONDITIONER-BRIDGED tier). Not touched by this ADR — see §4.
- `lab/pine/README.md` (added by PR #227, merged 2026-08-31) — an existing, informal, non-ratified Pine `indicator()` used for Python/TradingView parity checking on the MNQ/MYM mechanism-diagnostic work. Confirms light prior *practice* for the pattern this ADR formalizes as a *requirement*, though it predates and does not itself define an exit contract.
- `CLAUDE.md` — public-clone posture: `**/*.pine` is gitignored, hash-pinned in `core/strategies/MANIFEST.sha256`; executable Python ports are hash-pinned in `PORT_MANIFEST.sha256`. A frozen *test* Pine instrument (not a production strategy) has no existing manifest convention — flagged as an open implementation detail in §2, not resolved here.

**Amendment-first / dedup (Rule 8 sub-rule 10), run at drafting:**

```
$ python scripts/check_advisor_dedup.py --keywords "hypothesize exit frozen pine test instrument trading investigation manual tradingview tester multiplicity K record"
```

279 candidates surfaced (top match score 10/13 keywords); all keyword-overlap noise from instrument ledgers, audit notes, and programme-audit hook files — none proposes a Hypothesize-exit Pine-freeze requirement or a manual-Tester-look K-accounting rule. No existing ADR or brief performs this ADR's decision.

---

## §1 — Decision driver (one sentence)

An independent adversarial review of PR #229 found that most of its proposed "mechanism-to-trade bridge" restates decisions the estate ratified the day before under different vocabulary (see §3), but two of its clauses are genuinely unowned anywhere in canon or the six 2026-08-30 ADRs and are worth ratifying on their own, narrow terms.

## §2 — Decision

**Ratify two clauses only**, both scoped to **trading investigations** (the general-purpose INQHIORI loop is unchanged, matching PR #229's own §0 scope line):

### 2.1 — Hypothesize exits with a frozen Pine test instrument

For a trading investigation, the Hypothesize (H) phase does not exit until it produces, alongside its ranked hypotheses, an executable Pine Script **test instrument** for the paired confirm-phase read: a versioned `strategy()` when the candidate's payoff claim is tradeable, or an `indicator()` when the investigation is mechanism-only (per `candidate-contract.md`'s diagnostic tier — an `indicator()` cannot itself confirm a candidate-contract admission, only support the discriminator read). The frozen instrument must declare: symbol, timezone/session, bar resolution, signal timing, next-bar-vs-same-bar execution, pyramiding, stop/target ordering, commissions, slippage, position sizing, date windows, and every exposed input. A Python/Pine parity contract (fixture dates or event rows, expected signal counts, tolerated numeric differences, known irreducible differences declared before either result is read) travels with it.

If a faithful Pine test instrument cannot be written from the frozen candidate-contract fields, Hypothesize does not exit. The routes are: revise the expression (return to Question), or STOP (Rule 2's existing stop vocabulary — no new terminal state is created). Writing the Pine instrument is test design, explicitly not Integrate — it must not modify a production strategy, and it does not imply authorization to trade. Test-instrument Pine remains subject to the existing `**/*.pine` gitignore/hash-pin posture (`MANIFEST.sha256`); the specific manifest entry format for a *test-only* instrument (as distinct from a production strategy edition) is an implementation detail for whoever builds the first one, not specified by this ADR.

### 2.2 — Every tried TradingView configuration counts toward the campaign's K/multiplicity record

When a trading investigation's confirm-phase work involves manual exploration inside TradingView's Strategy Tester (parameter changes, threshold nudges, alternate date windows tried by hand rather than through the pre-declared search contract), **every configuration tried counts toward the campaign's declared multiplicity/K record** — the same discipline `operator-approvals-campaign-envelope.md` already requires for Python-side looks, extended to close the one channel that ADR does not cover (TradingView is out of scope for all six 2026-08-30 ADRs; confirmed by full-text grep, §0 above). The best-performing TradingView configuration found this way is never silently substituted for the frozen confirm-phase configuration; an unplanned discovery is recorded for Observe and can motivate a fresh, separately-budgeted Iterate cycle, but cannot improve the current campaign's confirm verdict.

This wires into existing machinery by citation, not by inventing a parallel ledger: the K count these manual looks add is the same `K_intrinsic` `candidate-contract.md` and `register_search.py`'s `open_run()` already track: a manual TradingView look is a look, full stop, regardless of which tool ran it.

## §3 — What this ADR does **not** ratify, and why

PR #229's remaining clauses are not adopted here because each is already owned:

| PR #229 clause | Already owned by | Disposition |
|---|---|---|
| §2 (Notice-exit bridge template, TRADE-BRIDGED/DIAGNOSTIC exit rule) | `candidate-contract.md` §2 — the same six declared fields, the same diagnostic/candidate binary, the same consequence (no confirm holdout, no candidate status) | Not ratified; cite `candidate-contract.md` instead of re-deriving it under new vocabulary |
| §3 (paired Q-M/Q-E question contract, `MARKET-NULL`/`EXPRESSION-FAIL`/`VENUE-FAIL`/`EVIDENCE-VOID` vocabulary, precedence rule) | `terminal-taxonomy.md` §2 — the same four-class evidence axis, the same discriminator-fail-dominates-payoff-pass precedence rule, near-verbatim spurious-selection language | Not ratified; a second Question-phase packaging of an already-Accepted confirm-phase vocabulary would create two competing terms for the same four classes |
| §7 (Observe minimum-observation packet) | `evaluation-order.md` steps 7 and 9 (contract-integrity check, minimum frozen temporal-consistency battery) + the terminal-taxonomy split, repackaged | Not ratified; derivative of already-ratified integrity/robustness requirements |
| §8 (Reflect/terminal routing: ITERATE/INTEGRATE/STOP) | canon §16 (`Accepted` 2026-08-04) — live in the `Q-RANGEXFER-1` and `Q-RANGECOND-1` closures verbatim (`## Iterate` block: Verdict used / Model update / Next / routing / entry packet / stop rule / board write) | Not ratified; PR #229's §9 already (correctly) acknowledges this contract "remains intact" |

## §4 — Deliberately deferred, not resolved by this ADR

Two items an independent review surfaced are real, but are operator decisions, not something this ADR should resolve unilaterally:

1. **PR #229's CONDITIONER-BRIDGED tier appears to conflict with `candidate-contract.md`'s admission binary**, not merely fill a gap beside it. `candidate-contract.md` §2 draws no distinction between a bare correlation and a well-specified conditioner — both are "diagnostic," barred from a confirm holdout or candidate status. PR #229's CONDITIONER-BRIDGED route does not repeat that bar for a conditioner with a complete provisional expression, which would license confirm-window access and non-LIGHT budget for something with no entry/exit of its own. Live practice (`Q-RANGEXFER-1`, `Q-RANGECOND-1`, `Q-CONDVAL-1`, all 2026-08-29 through 08-31) already runs conditioner-role research and already names the base construct a conditioner modifies — but stays diagnostic-tier throughout ("no entry, sizing, or timing construct on any surviving conditioner," `Q-RANGEXFER-1` closure). Formalizing a non-diagnostic conditioner tier is a real, live question — does the estate want one, and if so does it amend `candidate-contract.md` explicitly (`Amends-in-part`) or redefine the tier as "append to the base trade's existing contract" rather than "open its own campaign"? This ADR takes no position; it is an operator call.

2. **PR #229's §4 (weighted LIGHT/STANDARD/HEAVY phase budgets) belongs to Rule 2's own ADR** (`2026-06-16-rule-2-budget-before-acting.md`), not the six 2026-08-30 ADRs, and should not be adopted piecemeal here. Two independent problems with §4 as drafted, found this session: (a) its own phase-allocation arithmetic is not self-consistent — HEAVY allocates 2+2+5+3=12 cycles against an 8-cycle guarantee, and the cumulative curve `[2, 4, 9, 12]` crosses the cycle-8 tripwire *inside* Investigate, before any of the three Observe/Reflect/closure cycles are spent, making the "possible" 9–12 extension arithmetically unavoidable rather than a genuine operator choice; (b) Rule 2's OUTER-8 budget has no mechanical tracking today for *any* investigation, trading or general — the trip-log is 3 rows of hand-maintained prose in 2.5 months, and its own audit trail records a missed quarterly review that nobody caught until an unrelated sweep found it. Amending Rule 2 to recognize a weighted form, while the base mechanism it would be layered on has never been verified to bind, compounds an unresolved problem rather than fixing one. Recommend: audit and repair Rule 2's own trip-log discipline first; revisit §4 only after that baseline exists.

3. **PR #229's §6 (Python-Explore/TradingView-confirmation split) reuses "Explore" and "confirmation" as tool-defined sub-activities of Investigate without stating their relationship to `evaluation-order.md`'s already-ratified steps of the same names** (step 6: K-ledger-bound Explore closed by an append-only selection freeze; step 9: one atomic multiplicity-adjusted confirm run). If §6's Explore/confirm are meant as the same steps, §6 as drafted omits the K-ledger-bind and selection-freeze discipline that makes them binding; if meant as a different activity layered on top, the shared name is misleading. §2.2 above ratifies the one clean, additive piece of §6 (manual-look K accounting) without adopting the vocabulary collision that surrounds it.

## §5 — Recommendation on PR #229 itself

Given §3 and §4, PR #229 should be closed as superseded rather than merged: its ratifiable content is captured narrowly by this ADR (§2), its remaining content either restates already-Accepted decisions under new vocabulary (§3) or contains open questions this ADR does not resolve (§4). A comment to that effect, linking this ADR, is the appropriate close reason — not a silent close.

## §6 — Ratification note

Not yet ratified. On operator GO: set Status to `Accepted`, set Decision date, and add the corresponding canon-side pointer under canon's Hypothesize-phase treatment (matching the §16 pattern: "Canonical source: this ADR... if it and the ADR ever disagree, the ADR wins"), as a separate, later edit — canon.md is the single most load-bearing methodology file in the estate and editing it is not bundled into this ADR's own ratification.
