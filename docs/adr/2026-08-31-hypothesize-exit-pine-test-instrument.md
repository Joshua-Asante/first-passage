# Hypothesize-exit frozen Pine test instrument for trading investigations, plus manual-TradingView-look K accounting — `hypothesize-exit-pine-test-instrument`

**Status:** `Proposed` — drafted by Claude Code, ratification is an operator decision. Date below is the draft date, not a ratification date — see §9.
**Decision date:** 2026-08-31
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Amends-in-part:** `2026-08-30-candidate-contract.md` §2 (on ratification) — adds the Pine execution-semantic field set genuinely not already frozen there (timezone/session, bar resolution, signal timing, next-bar-vs-same-bar execution, pyramiding, stop/target ordering, position-sizing methodology, exposed inputs — NOT date windows or costs, both already owned by candidate-contract.md §2, corrected in review round 5) at the Hypothesize-exit freeze point; see §2.1 and §9.
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
- `docs/adr/2026-08-30-evaluation-order.md` — step 6 ("Explore," K-ledger-bound, closed by an append-only selection freeze) and step 9 (one atomic untouched confirm run, multiplicity-adjusted). Confirmed via full-text grep: no Pine/TradingView content. This ADR does not redefine "Explore" or "confirm" — see §7 (deferred items) for why PR #229's §6 is *not* ratified here.
- `docs/adr/2026-08-30-operator-approvals-campaign-envelope.md` — the multiplicity/K-spend envelope, explicitly orthogonal to Rule 2's iteration budget (§2, lines 176–180: "Neither this ADR nor Rule 2 is amended by the other"). The manual-TradingView-look accounting this ADR ratifies (§2 below) is wired into this envelope's multiplicity configuration by citation, not reinvented.
- `docs/adr/2026-06-16-rule-2-budget-before-acting.md` + canon §15 — Rule 2's OUTER-8 iteration budget. Checked independently this session (`docs/notes/audits/rule-2-trip-log.md`), **before this PR added `scripts/check_rule2_trip_log_liveness.py`**: **zero scripts anywhere in the repo enforce this budget** (`grep -rl "rule.2\|rule_2\|OUTER.*8" scripts/*.py` returned no hits on that pre-PR tree). That grep is no longer reproducible verbatim on this PR's own resulting tree — `check_rule2_trip_log_liveness.py`'s own text now matches the same pattern (round 6 of this PR's review caught this) — but the underlying claim it supported is unchanged: that script reports whether a programme-audit note mentions Rule 2, it does not enforce the OUTER-8 budget itself (see its own module docstring, "THIS SCRIPT DOES NOT ADJUDICATE AUDIT-CYCLE COUNTING"), so the gap this ADR is built on is still real, just no longer evidenced by a grep that has to exclude its own new sibling. The trip-log itself is hand-appended prose with 3 rows total since codification (2026-06-16); its own audit trail documents a missed 2026-08-08 quarterly check that was never recorded as having not run until a later, unrelated sweep caught it. PR #229's §4 (weighted LIGHT/STANDARD/HEAVY phase budgets) proposes to amend this ADR specifically — not the six 2026-08-30 ADRs — and is not ratified here; see §7 below.
- `ops/instruments/MECHANISMS.md` — confirms the conditioner-role vocabulary is already live practice, tagged "Conditioner-role, not entry-role" since 2026-08-18 (13 days before PR #229 proposed the same concept as a new CONDITIONER-BRIDGED tier). Not touched by this ADR — see §7.
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

### 2.1 — Hypothesize exits with a frozen Pine `strategy()` once a tradeable contract exists

For a trading investigation whose candidate has cleared `candidate-contract.md`'s admission — i.e. a complete tradeable entry/exit object exists and a contract is open, matching the exemption clause's own binding point below — the Hypothesize (H) phase does not exit until it produces, alongside its ranked hypotheses, an executable, versioned Pine Script **`strategy()` test instrument** for the paired confirm-phase read. An investigation merely *seeking* admission, with a complete trade object as its immediate goal but no contract open yet, is not bound by this gate (round 6 of this PR's review caught that the prior "or is actively seeking" wording bound the gate to a case with, by construction, no frozen fields to derive `strategy()` from — the same trap the round-1 diagnostic fix below closes for mechanism-only work, reopened here for expression-first work that simply hadn't opened its contract yet). Two field sets feed it. **Already frozen by `candidate-contract.md` §2** (re-derived here, not re-decided): instrument, signal, entry clock, stop, exit/target, holding horizon, costed payoff unit, exploration/confirm date windows, and costs. **Genuinely new execution semantics that ADR does not itself own** (confirmed via full-text grep, corrected in review — round 4 of this PR's review incorrectly re-listed some of the above, already-owned fields as new; round 5 caught it): timezone/session, bar resolution, signal timing (the intra-bar mechanical detection point, distinct from the discriminator signal itself), next-bar-vs-same-bar execution, pyramiding, stop/target ordering (execution sequencing, distinct from the stop/target values), position-sizing methodology, and every exposed input. That ADR's own text says field extension beyond its baseline list "is by amendment, not by this ADR alone" — this ADR is that amendment (`Amends-in-part`, header) for the genuinely-new field set only; the already-frozen fields are reused as-is, not re-frozen. A Python/Pine parity contract (fixture dates or event rows, expected signal counts, tolerated numeric differences, known irreducible differences declared before either result is read) travels with it.

If a faithful `strategy()` cannot be written from those frozen fields, Hypothesize does not exit for this candidate. The routes are: revise the expression (return to Question), or the candidate-routing STOP already owned by canon §16's closure-resident Iterate/closure contract — Iterate with budget zero, recording the re-proposal bar (`docs/adr/2026-08-04-iterate-closure-exit-mandatory.md`) — not Rule 2's own STOP, which is a budget-tripwire action that can lead to re-audit or an owner-authorized extension and does not apply to a candidate that simply cannot be encoded in Pine. No new terminal state is created either way.

**A mechanism-only investigation that has not opened a contract is not bound by this requirement.** Per `candidate-contract.md` §2, a diagnostic (proxy work with no defined trade) "cannot open a contract, consume a confirm holdout, or claim candidate status" — so by construction there are no frozen candidate-contract fields for a `strategy()` to derive from, and no confirm-phase read for a test instrument to pair with (Codex found this gap in review: as originally drafted, this section required deriving *any* Pine instrument, including a diagnostic's, from "frozen candidate-contract fields" that a diagnostic never has — trapping it). A diagnostic may still build a supporting Pine `indicator()` to aid its own mechanism-discriminator read; that is a tool choice, not an H-exit gate. The diagnostic's own exit routing — continue as diagnostic, or accumulate a complete trade object and open a contract, at which point this section's `strategy()` requirement binds — is already governed by `candidate-contract.md`'s diagnostic tier, unchanged by this ADR.

Writing the Pine instrument is test design, explicitly not Integrate — it must not modify a production strategy, and it does not imply authorization to trade. Test-instrument Pine remains subject to the existing `**/*.pine` gitignore/hash-pin posture (`MANIFEST.sha256`); the specific manifest entry format for a *test-only* instrument (as distinct from a production strategy edition) is an implementation detail for whoever builds the first one, not specified by this ADR.

### 2.2 — TradingView exploration is Explore before the confirm holdout is read; after it is read, it voids the attempt

`evaluation-order.md` step 6 already requires the campaign's K-ledger (`register_search.py open_run()`) to bind K/α/window against the frozen contract *before any exploration data is read*, and Explore to score only "every declared cell in the frozen catalogue," closed by an append-only selection freeze before any holdout access; step 9 requires the confirm run to be "one untouched confirm run... as one atomic step." Neither that ADR nor `register_search.py` distinguishes which *tool* ran an Explore-phase look — a manual TradingView Strategy Tester parameter change is the same kind of event as a Python-side one. This ADR states that explicitly, closing the one gap none of the six 2026-08-30 ADRs cover (TradingView is out of scope for all of them; confirmed by full-text grep, §0 above): **a manual TradingView configuration tried before the confirm holdout is read is Explore activity, and is legitimate only when it is a cell already declared in the frozen catalogue at the K-ledger bind** — counting it toward K does not, on its own, license inventing an off-catalogue configuration mid-Explore (round 5 of this PR's review caught that the prior text could be read that way). A cell not in the frozen catalogue is an integrity mismatch, routed the same way `evaluation-order.md` step 7 routes any other: voided, never scored as a structural or evidentiary finding — not salvaged by being counted after the fact.

**A manual TradingView configuration tried *after* the confirm holdout has been read is not a look to count — it voids the current confirm attempt.** Codex's review caught that the original text here claimed such a look could be retroactively added to the same campaign's K record; that is not mechanically possible and, more importantly, not the right rule. `register_search.py`'s `open_run()` is pre-registration-only and refuses re-declaration once a run is open (`lab/discovery/register_search.py:712-716`: "Pre-registration is immutable; pick a new run-id rather than re-declaring K after results"), and `close_run()` computes thresholds only from the K frozen at open (the narrow `--operator-stopped` path may only *reduce* a not-yet-executed run's banked K, never add to an executed one). Consistent with `evaluation-order.md` step 7's own handling of any post-freeze mismatch ("never recorded as a structural or evidentiary rejection") and `terminal-taxonomy.md`'s `EVIDENCE-VOID` class (§0): post-read TradingView exploration voids the current confirm attempt, full stop, and requires a fresh campaign against a fresh, uncontaminated holdout — never a K-adjustment layered onto the run that was already read. The best-performing configuration found this way is never substituted for the frozen confirm-phase configuration; it may motivate a fresh, separately-budgeted Iterate cycle, but confers nothing on the current campaign's verdict.

This narrows what PR #229's original §6.3 proposed (which implied a post-hoc look could be safely retained by counting it) to the boundary that is actually sound: pre-read is Explore and gets counted; post-read is a holdout violation and gets voided, not counted.

## §3 — What this ADR does **not** ratify, and why

PR #229's remaining clauses are not adopted here because each is already owned:

| PR #229 clause | Already owned by | Disposition |
|---|---|---|
| §2 (Notice-exit bridge template, TRADE-BRIDGED/DIAGNOSTIC exit rule) | `candidate-contract.md` §2 — the same six declared fields, the same diagnostic/candidate binary, the same consequence (no confirm holdout, no candidate status) | Not ratified; cite `candidate-contract.md` instead of re-deriving it under new vocabulary |
| §3 (paired Q-M/Q-E question contract, `MARKET-NULL`/`EXPRESSION-FAIL`/`VENUE-FAIL`/`EVIDENCE-VOID` vocabulary, precedence rule) | `terminal-taxonomy.md` §2 — the same four-class evidence axis, the same discriminator-fail-dominates-payoff-pass precedence rule, near-verbatim spurious-selection language | Not ratified; a second Question-phase packaging of an already-Accepted confirm-phase vocabulary would create two competing terms for the same four classes |
| §7 (Observe minimum-observation packet) | `evaluation-order.md` steps 7 and 9 (contract-integrity check, minimum frozen temporal-consistency battery) + the terminal-taxonomy split, repackaged | Not ratified; derivative of already-ratified integrity/robustness requirements |
| §8 (Reflect/terminal routing: ITERATE/INTEGRATE/STOP) | canon §16 (`Accepted` 2026-08-04) — live in the `Q-RANGEXFER-1` and `Q-RANGECOND-1` closures verbatim (`## Iterate` block: Verdict used / Model update / Next / routing / entry packet / stop rule / board write) | Not ratified; PR #229's §9 already (correctly) acknowledges this contract "remains intact" |

## §4 — Falsifier (revert trigger)

**H (hypothesis):** requiring a frozen, executable Pine `strategy()` test instrument at the
Hypothesize-exit boundary (§2.1), and counting a manual TradingView Strategy Tester look toward
K only when it is a pre-declared frozen-catalogue cell (§2.2), closes the two real gaps an
independent review found (Python/Pine execution-semantic drift; a discovery channel invisible to
every 2026-08-30 ADR's K accounting) without creating a new loophole, and without blocking
legitimate diagnostic-tier work that has no contract to derive `strategy()` fields from.

**Revert trigger:** if, by the next scheduled quarterly programme audit after the first trading
investigation reaches a Hypothesize-exit bound by this ADR (i.e. after the first post-ratification
`candidate-contract.md` admission with an open contract), any of the following is found true, this
ADR is revoked: (a) a confirm-phase read proceeded for a candidate that had cleared contract
admission without an executable, versioned Pine `strategy()` test instrument satisfying §2.1 — i.e.
the H-exit gate did not actually block a candidate it should have; (b) a manual TradingView
configuration made *before* the confirm holdout was read was counted toward K, or excused from
voiding, without being a cell already declared in the frozen catalogue at the K-ledger bind — i.e.
the catalogue-membership boundary §2.2's first paragraph draws did not hold in practice; or (c) a
manual TradingView configuration made *after* the confirm holdout was read was retained or counted
rather than voided — regardless of whether it was a declared catalogue cell — i.e. §2.2's second
paragraph's unconditional post-read voiding rule did not hold in practice (round 6 of this PR's
review caught that (b) alone, as drafted, only tests catalogue membership and would not catch a
retained post-read look that happened to be an in-catalogue configuration; (c) is deliberately
independent of catalogue membership to close that gap).

**Revert action:** author a superseding ADR that either (a) tightens §2.1's gate (e.g. requiring
the parity contract itself, not just the `strategy()` file, to be checked at Hypothesize-exit), or
(b) narrows or removes §2.2's catalogue-membership carve-out or post-read voiding rule if either
proves unenforceable in practice. Never silently edit this ADR's decision text (§2) to patch a
found gap.

**Trigger check schedule:** every quarterly programme audit (next: 2026-11-08).

## §5 — Forbidden moves (under this ADR)

- **Reading §2.2's K-counting rule as license to invent an off-catalogue TradingView configuration
  mid-Explore.** Ruled out in §2.2 (round 5 of this PR's review caught the prior text could be
  misread this way): counting toward K requires catalogue membership first; an off-catalogue cell
  is voided per `evaluation-order.md` step 7, never salvaged by being counted after the fact.
- **Retroactively adding a post-confirm-holdout-read TradingView look to the same campaign's K
  record.** Ruled out in §2.2 (round 2 finding: not mechanically possible — `open_run()` is
  pre-registration-immutable — and not the right rule regardless): a post-read look voids the
  current confirm attempt outright; it never becomes a K adjustment on the run already read.
- **Citing §2.1's STOP as Rule 2's own budget-tripwire STOP.** It is not — it is canon §16's
  closure-owned candidate-routing STOP (`2026-08-04-iterate-closure-exit-mandatory.md`), for a
  candidate that structurally cannot be encoded in Pine, not for an iteration-budget overrun
  (round 4 finding, an internal inconsistency this ADR's own §3 table had already avoided
  elsewhere).
- **Applying §2.1's `strategy()` requirement to a diagnostic-tier investigation that has not opened
  a contract.** Ruled out in §2.1: a diagnostic has no frozen candidate-contract fields to derive
  `strategy()` from by construction, and no confirm-phase read for a test instrument to pair with
  (round-1 Codex finding on the original draft).
  A diagnostic building its own supporting Pine `indicator()` is a tool choice, not this gate.
- **Treating §2.1's "genuinely new execution semantics" field list as re-freezing fields
  `candidate-contract.md` §2 already owns** (date windows, costs, instrument, signal, entry clock,
  stop, exit/target, holding horizon, costed payoff unit). Ruled out in §2.1 (round 5 caught this
  ADR's own round-4 fix had re-listed some already-owned fields as new) — this ADR's
  `Amends-in-part` scope is the genuinely-new set only.
- **Building the frozen Pine test instrument as, or later repurposing it into, a production
  strategy edition.** §2.1 is explicit: writing it is test design, not Integrate, and confers no
  trading authorization. The manifest-entry format for a test-only instrument remains an open
  implementation detail (§0), not license to skip the `**/*.pine` gitignore/hash-pin posture
  entirely.
- **Treating this ADR as ratifying any part of PR #229 beyond §2.1/§2.2.** §3 and §8 are explicit
  that everything else in PR #229 is either already owned elsewhere or explicitly deferred (§7) —
  citing this ADR as authority for PR #229's §2/§3/§4/§6/§7/§8 as a whole is a misreading.

## §6 — Consequences

**Positive consequences:**
- Closes the one execution-semantic gap none of the six 2026-08-30 ADRs cover: nothing today
  requires a candidate's Python-side frozen fields to ever be faithfully re-expressed as
  executable Pine before a confirm-phase read, so Python/Pine drift was invisible until this ADR.
- Closes the one discovery-channel gap none of the six 2026-08-30 ADRs cover: `evaluation-order.md`
  and `register_search.py` are both tool-agnostic in principle but TradingView-blind in practice
  (confirmed by full-text grep, §0) — this ADR states explicitly that a manual TradingView look is
  the same kind of Explore event as a Python-side one, closing the gap without redefining Explore.
- Narrows PR #229's own §6.3 (which implied a post-hoc TradingView look could be safely retained by
  counting it) to the boundary that is actually sound, before any live campaign could rely on the
  unsound version.
- Gives `candidate-contract.md` a precise, minimal `Amends-in-part` edge — the genuinely-new
  execution-semantic field set only, not PR #229's broader unratified table.

**Negative consequences (real cost, not theatrical):**
- Adds a standing authoring requirement to every future trading investigation that opens or seeks
  a contract: an executable, versioned Pine `strategy()` plus a Python/Pine parity contract, at the
  Hypothesize-exit boundary. No exemption beyond the diagnostic carve-out (§2.1).
- The test-instrument manifest-entry format is left unresolved (§0, §5) — the first investigation
  to build one under this ADR inherits that open decision, not a ready answer.

**Risks (probabilistic, distinct from costs):**
- If the "already frozen vs. genuinely new" execution-semantic field split (§2.1) proves wrong in
  either direction — a field claimed already-frozen turns out unowned by `candidate-contract.md`,
  or vice versa — before the first real trading investigation reaches Hypothesize-exit under this
  ADR, the split needs correcting by amendment, not quiet drift in practice. §4's falsifier targets
  the gate's operative behavior (did it block, did the catalogue boundary hold), not this narrower
  field-accounting risk directly — flagged here so a reviewer catches it before first real use.

**Downstream artifacts that need updating (on ratification, per §9):**
- `docs/methodology/inqhiori-canon.md` — owed the Hypothesize-phase pointer (§9).
- `docs/adr/2026-08-30-candidate-contract.md` §2 "Amended fields" list — owed this ADR's entry
  (§9).

## §7 — Deliberately deferred, not resolved by this ADR

Two items an independent review surfaced are real, but are operator decisions, not something this ADR should resolve unilaterally:

1. **PR #229's CONDITIONER-BRIDGED tier appears to conflict with `candidate-contract.md`'s admission binary**, not merely fill a gap beside it. `candidate-contract.md` §2 draws no distinction between a bare correlation and a well-specified conditioner — both are "diagnostic," barred from a confirm holdout or candidate status. PR #229's CONDITIONER-BRIDGED route does not repeat that bar for a conditioner with a complete provisional expression, which would license confirm-window access and non-LIGHT budget for something with no entry/exit of its own. Live practice (`Q-RANGEXFER-1`, `Q-RANGECOND-1`, `Q-CONDVAL-1`, all 2026-08-29 through 08-31) already runs conditioner-role research and already names the base construct a conditioner modifies — but stays diagnostic-tier throughout ("no entry, sizing, or timing construct on any surviving conditioner," `Q-RANGEXFER-1` closure). Formalizing a non-diagnostic conditioner tier is a real, live question — does the estate want one, and if so does it amend `candidate-contract.md` explicitly (`Amends-in-part`) or redefine the tier as "append to the base trade's existing contract" rather than "open its own campaign"? This ADR takes no position; it is an operator call.

2. **PR #229's §4 (weighted LIGHT/STANDARD/HEAVY phase budgets) belongs to Rule 2's own ADR** (`2026-06-16-rule-2-budget-before-acting.md`), not the six 2026-08-30 ADRs, and should not be adopted piecemeal here. Two independent problems with §4 as drafted, found this session: (a) its own phase-allocation arithmetic is not self-consistent — HEAVY allocates 2+2+5+3=12 cycles against an 8-cycle guarantee, and the cumulative curve `[2, 4, 9, 12]` crosses the cycle-8 tripwire *inside* Investigate, before any of the three Observe/Reflect/closure cycles are spent, making the "possible" 9–12 extension arithmetically unavoidable rather than a genuine operator choice; (b) Rule 2's OUTER-8 budget has no mechanical tracking today for *any* investigation, trading or general — the trip-log is 3 rows of hand-maintained prose in 2.5 months, and its own audit trail records a missed quarterly review that nobody caught until an unrelated sweep found it. Amending Rule 2 to recognize a weighted form, while the base mechanism it would be layered on has never been verified to bind, compounds an unresolved problem rather than fixing one. Recommend: audit and repair Rule 2's own trip-log discipline first; revisit §4 only after that baseline exists.

3. **PR #229's §6 (Python-Explore/TradingView-confirmation split) reuses "Explore" and "confirmation" as tool-defined sub-activities of Investigate without stating their relationship to `evaluation-order.md`'s already-ratified steps of the same names** (step 6: K-ledger-bound Explore closed by an append-only selection freeze; step 9: one atomic multiplicity-adjusted confirm run). If §6's Explore/confirm are meant as the same steps, §6 as drafted omits the K-ledger-bind and selection-freeze discipline that makes them binding; if meant as a different activity layered on top, the shared name is misleading. §2.2 above ratifies the one clean, additive piece of §6 (manual-look K accounting) without adopting the vocabulary collision that surrounds it.

## §8 — Recommendation on PR #229 itself

Given §3 and §7, PR #229 should be closed as superseded rather than merged: its ratifiable content is captured narrowly by this ADR (§2), its remaining content either restates already-Accepted decisions under new vocabulary (§3) or contains open questions this ADR does not resolve (§7). A comment to that effect, linking this ADR, is the appropriate close reason — not a silent close.

## §9 — Ratification note

Not yet ratified. On operator GO: set Status to `Accepted`, set Decision date, and — as separate, later edits, not bundled into this ADR's own ratification — (1) add the corresponding canon-side pointer under canon's Hypothesize-phase treatment (matching the §16 pattern: "Canonical source: this ADR... if it and the ADR ever disagree, the ADR wins"), canon.md being the single most load-bearing methodology file in the estate; and (2) add this ADR's pointer to `candidate-contract.md`'s own "Amended fields" list (§2, matching the format its existing four amending-ADR entries already use), naming the execution-semantic field set §2.1 above adds and their Hypothesize-exit freeze point — that list's own text says it is "landed on ratification of the amending ADRs," so it stays unedited (and this ADR's `Amends-in-part` header field stays the operative record) until this ADR is actually `Accepted`.

---

## §10 — Audit hooks (runnable)

```bash
# Discipline checks (mechanical)
python scripts/check_brief.py docs/adr/2026-08-31-hypothesize-exit-pine-test-instrument.md --type adr
python scripts/check_adr_graph.py

# Pre-ratification: the two owed pointer-edits (§9) must NOT have landed yet --
# this ADR is still `Proposed`. Expect no hits until Status -> Accepted.
grep -n "hypothesize-exit-pine-test-instrument" docs/methodology/inqhiori-canon.md
grep -n "hypothesize-exit-pine-test-instrument" docs/adr/2026-08-30-candidate-contract.md

# Rule 0 production-source verification -- confirm the cited files this ADR was
# read against haven't drifted since drafting
git log -1 --format="%h %ci" -- docs/adr/2026-08-30-candidate-contract.md
git log -1 --format="%h %ci" -- docs/adr/2026-08-30-evaluation-order.md
git log -1 --format="%h %ci" -- lab/discovery/register_search.py

# Sibling WARN-tier gates this ADR's own review produced (docs/spec/ provenance,
# Rule 2 trip-log liveness) -- both report-only, both scanned here for context
python scripts/check_spec_provenance.py --stats
python scripts/check_rule2_trip_log_liveness.py --stats

# K-ledger immutability this ADR's §2.2 depends on -- still true?
grep -n "Pre-registration is immutable" lab/discovery/register_search.py

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08 (also §4's falsifier check window)
```
