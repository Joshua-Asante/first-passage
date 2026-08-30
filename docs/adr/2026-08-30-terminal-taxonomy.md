# Terminal taxonomy — `EXPRESSION-FAIL` as a fifth WHY-rejected class, confirm-phase verdict vocabulary, and the `N_expr` expression ladder — `terminal-taxonomy`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-30; see Ratification note.
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Amends-in-part:** `2026-06-14-rejected-candidate-patterns.md` — adds a fifth §A class
(`expression-failure`) with its own add-back condition, alongside the existing four, **and** widens
the existing `venue / cost-constraint` class's add-back condition to explicitly cover a payoff-shape
kill alongside its existing cost-law/lower-cost-venue wording (§2 below) — a real amendment, not
merely a routing reading, corrected into this header by a review pass (§7). Lands as a **dated
addendum overlay** on that ADR, never an in-place table edit — its own 2026-08-29 addendum forbids
rewriting §1-§10 in place. `2026-08-30-
candidate-contract.md` — freezes the mechanism-level discriminator's complete adjudication rule
(statistic, null, direction, threshold, coverage/power) as a founding-freeze field, discharging that
ADR's own §3 deferral of "the mechanism-level discriminator's adjudication rule" — also added by a
review pass (§7): this ADR's `MARKET-NULL`/`EXPRESSION-FAIL` distinction is meaningless unless that
rule is frozen before the holdout is read, and no ADR in this series had actually added the field.
**Layer:** methodology (confirm-phase disposition vocabulary and registry-routing rules only). No
`dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue
action; no spend.
**Tier:** full — Limb 4 fires (creates standing verdict vocabulary and amends the ratified
WHY-rejected taxonomy).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, this session (2026-08-30):

- `docs/notes/2026-08-30-generate-evaluate-tensions.md` — anchor `419433a` (2026-08-30). "Use one
  terminal taxonomy" row: `MARKET-NULL` → edge-failure and a pre-explore reachability kill →
  venue/cost-constraint or portfolio-fit/tail losslessly map onto the existing four classes;
  `EXPRESSION-FAIL` maps onto none of them and needs a fifth class with its own binary add-back;
  `EVIDENCE-VOID` and `ROLE-BLOCKED` are nonterminal and excluded from every register; `CHANNEL-FAIL`
  is a channel-level process disposition, not evidence against any candidate. Evaluate-phase step 3
  (verdict emission on the untouched confirm run) and step 5 (two-axis append-only disposition, the
  `N_expr` expression-attempt ladder, migration to venue/cost-constraint when cost/geometry limbs
  fired) supply this ADR's operative mechanics.
- `docs/adr/2026-06-14-rejected-candidate-patterns.md` — anchor `0395f56` (2026-08-29). §A: the four
  ratified classes (`edge-failure`, `portfolio-fit / tail`, `venue / cost-constraint`,
  `non-rediscovery / role-duplicate`), each with its own binary add-back condition — "the class
  records **why** a candidate was rejected... that is the whole point of not conflating them." §C:
  the add-back gate — "re-tuning an edge-failure is not an add-back, it is the degeneration move."
  §D: schema-extension precedent — new attributes are **added** to the existing
  `<!-- concept-intake-entry … -->` comment schema, never a replacement, because `dedup.py`'s
  `_KV_RE` ignores unknown keys. This ADR's `N_expr`/expression-history fields reuse that exact
  additive pattern (§7 below), not a new registry file.
- `docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md` — anchor `e11fd39`
  (2026-08-24). §2 D3: register topology is scope-routed, not class-routed —
  per-direction/instrument-scoped mechanism rejections go to the instrument ledger
  (`ops/instruments/<SYM>.md` + `profiles.json`, machine-consulted); domain-level/cross-instrument
  bars go to `docs/rejected_candidates.md`; meta-layer methodology signals go to
  `docs/methodology/rejected_signals.md`. "The WHY class alone cannot select an owning register" —
  this ADR's own §2 below inherits that rule unedited; the `N_expr` ledger field attaches to
  whichever row D3 already routes a mechanism's kill history to, never a new fourth register.
- `docs/adr/2026-08-05-strategy-venue-binding-axis.md` — anchor `e2d21b9` (2026-08-24), as amended
  by `2026-08-24-venue-binding-axis-t1-disposition.md` (same anchor; §2/§4/§5/§6/§7 untouched by
  that amendment). §2: book evidence (candidate confirmation) and venue-edition state (placement at
  a specific firm) are **orthogonal axes** — a venue-placement failure does not overwrite a
  standalone confirmed status. This ADR's two-axis disposition (§2 below) is an **application** of
  that already-ratified split, not a new axis decision.
- `docs/adr/2026-08-24-sourcing-phase-channel-retirement.md` — anchor `340722c` (2026-08-24). Route
  B's four campaigns closed `VOID-COVERAGE`, `FALSIFIED`, `FALSIFIED`, `AMBIGUOUS-HOLD` — none
  reached confirm, so none of this ADR's confirm-phase verdict classes were ever actually exercised
  by that channel; the retirement decision fired on channel-level liveness (§4 of
  `2026-08-30-channel-liveness-gate.md`), a `CHANNEL-FAIL`-shaped event under this ADR's vocabulary,
  independent of any single candidate's WHY-rejected class.
- `docs/methodology/strategy_harvest.md` — anchor `936eb0f` (2026-08-29). Requirement 2's
  discriminator/observable framing (the mechanism-level test that must adjudicate cleanly, distinct
  from the payoff-object test) — the same separation this ADR's `EXPRESSION-FAIL` definition below
  depends on: a discriminator pass plus a payoff-object rejection is what makes the failure about
  the expression, not the mechanism.
- `docs/adr/2026-08-30-tradeable-reachable-gate.md` — anchor `a682b74` (2026-08-30, this branch).
  §2: "Which terminal class that typed verdict routes into is `2026-08-30-terminal-taxonomy.md`'s
  decision, cited here, not re-decided" — this ADR is that forward-cited decision; §2 below rules on
  it directly (the pre-explore-kill routing rule).
- `docs/adr/2026-08-30-candidate-contract.md` — anchor `7669664` (2026-08-30, this branch). §2's
  founding-freeze fields (instrument, feature catalogue, entry/exit object) are the object this
  ADR's dispositions append against. §3 explicitly names "the mechanism-level discriminator's
  adjudication rule" as deferred to a separate amending ADR — a gap a review pass caught unfilled by
  any of this series' six ADRs (§7): this ADR now amends it in via the header `Amends-in-part` edge,
  since the discriminator concept is native to this ADR's own `MARKET-NULL`/`EXPRESSION-FAIL`
  distinction.

**Amendment-first / dedup (Rule 8 sub-rule 10), run at ratification:**

```
$ python scripts/check_advisor_dedup.py --keywords "terminal taxonomy expression-failure fifth WHY-rejected class confirm verdict vocabulary N_expr ladder"
```

272 candidates surfaced; the highest-scoring hit (`docs/notes/audits/programme-audit/2026-08-05-claim-alignment/03-agent-facing.md`, score 10, matching "expression/fifth/ladder") was read in full and confirmed a false positive — its "expression" is a Python expression in an M1 desk-card script, its "fifth" refers to an unrelated send-vs-arm cluster member, and its "ladder" refers to a funded-scaling contract-size ladder, not this ADR's expression-attempt ladder. No genuine prior art; no existing ADR or brief performs this ADR's decision.

---

## §1 — Context

The estate has one ratified rejection taxonomy (`2026-06-14-rejected-candidate-patterns.md` §A, four
classes) and one ratified register-routing rule (`2026-08-09-...` §D3, scope-based, not class-based).
Neither anticipated a confirm-phase failure where the *mechanism* (the causal observable) passes its
own discriminator test while the *expression* (the specific entry/exit implementation built on it)
is rejected — a distinction the ratified taxonomy has no class for and would misclassify either way:
forcing it into `edge-failure` would apply that class's "genuinely new mechanism" add-back to a
mechanism that was never actually falsified, while leaving it unclassified would mean a confirm-phase
rejection with no registry-eligible disposition at all.

Two more gaps compound this. First, the confirm-phase run itself (per the note's lean evaluate phase)
needs a small, closed verdict vocabulary — today `FALSIFIED`, `STOP`, `VOID`, and ad hoc shape/venue
failure language are used inconsistently across closures, without a declared mapping onto the
ratified WHY-rejected classes. Second, a pre-explore `TRADEABLE-REACHABLE` kill
(`2026-08-30-tradeable-reachable-gate.md`) produces a typed verdict with nowhere ruled to route: that
ADR explicitly defers the routing decision here.

**Decision driver (one sentence):** the estate has a ratified four-class rejection taxonomy and a
ratified scope-based register router, but no ruling on where a mechanism-survives/expression-fails
confirm result belongs, no closed confirm-phase verdict vocabulary, and no routing rule for a
pre-explore economic-gate kill — each currently only exists as unratified language in an interpretive
note.

---

## §2 — Decision

**Decision:** Ratify a closed confirm-phase verdict vocabulary, add `expression-failure` as a fifth
WHY-rejected class with its own add-back and `N_expr`-bounded re-entry ladder, and rule the routing
of every terminal and nonterminal disposition this vocabulary produces.

**The discriminator is a candidate-contract field, frozen before the holdout is read.** This
vocabulary is only meaningful if "the discriminator adjudicated cleanly" is a pre-committed fact, not
a post-hoc reading — so this ADR amends `2026-08-30-candidate-contract.md` (header) to freeze the
mechanism-level discriminator's complete adjudication rule (statistic, null hypothesis, direction,
threshold, and coverage/power requirement, measured independently of the specific entry/exit
implementation's payoff) as a founding-freeze field, discharging that ADR's own §3 deferral. No
confirm run may adjudicate `MARKET-NULL` vs. `EXPRESSION-FAIL` against a discriminator rule chosen or
interpreted after Explore or after the holdout is read.

**Confirm-phase verdicts (evidence axis, per candidate, per confirm attempt).** Exactly four:
`CONFIRMED`, `MARKET-NULL`, `EXPRESSION-FAIL`, `EVIDENCE-VOID`. `EXPRESSION-FAIL` applies only when
the frozen discriminator's complete adjudication rule (candidate-contract-frozen, above — Requirement
2's discriminator/observable separation, §0) returns a clean pass while the specific entry/exit
implementation is rejected. If the discriminator itself cannot adjudicate (its own frozen coverage or
power requirement unmet), that takes precedence over any payoff verdict and the candidate is
`EVIDENCE-VOID`, never `MARKET-NULL` — an underpowered discriminator is not evidence against the
mechanism. A discriminator that cleanly fails (a powered, adjudicated no) routes the candidate to
`MARKET-NULL` **regardless of the payoff/temporal implementation's own read** — including the case
where the implementation's own confirm statistic happens to pass despite the discriminator's clean
no. A payoff pass without a validated mechanism association is not confirmable evidence: it is the
exact spurious-selection shape this discipline exists to prevent, and treating it as `CONFIRMED`
would let a discriminator-failed mechanism through on a possibly-overfit implementation alone.
`CONFIRMED` therefore requires **both** the discriminator and the payoff/temporal implementation test
to clear; any other combination routes to `MARKET-NULL`, `EXPRESSION-FAIL`, or `EVIDENCE-VOID` per
the rules above — no fifth combination is left undefined.

**Edition axis (post-confirm, `CONFIRMED` candidates only).** Placement-clear or `VENUE-FAIL`, per
the already-ratified venue-binding axis (§0) — orthogonal to the evidence axis. `CONFIRMED ·
VENUE-FAIL(edition)` is a valid, standing disposition: neither fact overwrites the other.

**WHY-rejected class mapping (registry routing, evidence axis only):**
- `MARKET-NULL` → `edge-failure` (2026-06-14 §A). Lossless: the existing add-back ("a genuinely new
  entry mechanism") carries over unchanged.
- A pre-explore `TRADEABLE-REACHABLE` kill (cost, latency, geometry, **or** payoff-shape limb) →
  `venue / cost-constraint` (2026-06-14 §A), only as a **candidate-level** kill (before Explore).
  The registry entry records "priors-derived, no mechanism test run" so a shape-limb kill is never
  misread as mechanism evidence — no placebo-controlled test ran, so `edge-failure` is unavailable;
  no discriminator adjudicated, so `expression-failure` is too. **This ADR formally amends** (header,
  `Amends-in-part`) that row's own add-back text — a real edit, not merely a reading — from "a
  geometry that clears the cost-law pre-flight with margin... OR a materially lower-cost venue" to
  additionally admit: a shape/geometry that clears the failed limb with margin, or a venue whose
  rules remove the constraint. Latency and firm-geometry kills already fit the row's unedited
  cost/geometry language; the payoff-shape case is the only genuinely new admission this amendment
  adds.
- A post-confirm edition-axis `VENUE-FAIL` against a `CONFIRMED` candidate is **not** a candidate
  rejection and enters **no** WHY-rejected register — the candidate's confirmed status stands; only
  the placement failed.
- `EXPRESSION-FAIL` maps onto **none** of the four existing classes — see the new fifth class below.
- `EVIDENCE-VOID` and `ROLE-BLOCKED` are excluded from the mapping entirely: both are nonterminal
  for the candidate (an exhausted attempt or a re-screenable role fit, never a rejection), consistent
  with §D3's own exclusion of power-voids and non-rejections from every register.
- `CHANNEL-FAIL` (a channel hitting its liveness ceiling, `2026-08-30-channel-liveness-gate.md`) is
  excluded too: a channel-level process disposition, never evidence against any specific candidate.

**§A amendment — fifth class, `expression-failure`:**

| Class | Definition | Add-back condition (binary) |
|---|---|---|
| **expression-failure** | The mechanism-level discriminator adjudicates cleanly (a powered, pre-specified pass) while the specific entry/exit expression built on it is rejected on confirm. | A materially new expression class of the same mechanism, differing on a declared structural axis (stop logic, exit family, or holding-horizon class — never a parameter re-tune), admitted as a new candidate contract with fresh K and a fresh holdout, citing the failed entry and its ordinal in the mechanism's expression history. |

**The `N_expr` expression ladder.** The expression-attempt bound (`N_expr`, default 2) and the
running attempt history are keyed to the **mechanism**, not the contract — persisted on the same
D3-routed row that already owns the mechanism's rejection entries (instrument ledger or
`rejected_candidates.md`, per scope; §0), using the additive schema-extension pattern 2026-06-14 §D
already established. Every new expression contract must cite that history and declare its ordinal
(attempt `k` of `N_expr`, naming each prior failed expression class); a contract that omits or
contradicts the ledger's count is integrity-invalid at the evaluate phase's contract-integrity check
(the note's lean evaluate phase, step 1) — a later attempt cannot present itself as attempt one.

**Ladder termination.** Once `N_expr` independent expression classes have each produced
`EXPRESSION-FAIL` while the discriminator kept passing, no further expression attempt is available
under the standard add-back. The terminal state then depends on what the recorded failures actually
establish:
- If any recorded failure fired on a cost or execution-geometry limb, the mechanism entry migrates
  to `venue / cost-constraint` and adopts its existing add-back — legitimate only because cost
  evidence actually fired, never fabricated to close the ladder early.
- If every failure fired on non-cost limbs (temporal instability, say), the mechanism entry stays in
  `expression-failure` with the ladder closed: its exhausted add-back becomes a **new expression
  class structurally distinct from every failed one**, admissible only by operator ratification
  citing the full failure history — never by routine re-admission.

**Nonterminal dispositions (never registry entries, recorded on the contract only):**
- `ROLE-BLOCKED` — a role/compliance state-drift failure
  (`2026-08-30-evaluation-order.md`'s role state-drift re-check); re-screenable when the scoped
  account/book or its occupancy changes.
- `EVIDENCE-VOID` — contract-integrity mismatch, or ordinary coverage/power/holdout-integrity
  failure of the confirm run itself; exhausts the attempt, eligible for a fresh campaign with a
  fresh holdout, never a terminal registry destination.
- `CHANNEL-FAIL` — the channel-liveness ceiling firing (`2026-08-30-channel-liveness-gate.md`);
  recorded at the channel level, never attributed to any one candidate's disposition.

**Effective:** immediately upon acceptance, for any confirm-phase verdict emitted, or `TRADEABLE-
REACHABLE` pre-explore kill recorded, after this date.
**Scope:** confirm-phase verdict vocabulary, WHY-rejected class routing, and the expression-failure
ladder, across all five live channels (GROW is tooling inside deep-iteration, not a sixth channel —
matching `2026-08-30-channel-liveness-gate.md`'s own derivation). Does not alter 2026-06-14's four existing classes, 2026-08-09's
§D3 routing rule, or 2026-08-05's axis split — it amends the first additively and applies the other
two unedited.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Force `EXPRESSION-FAIL` into the existing `edge-failure` class | Applies "genuinely new mechanism" as the add-back to a mechanism that was never falsified — the discriminator passed. Wrong in the direction that matters most: it would bar re-trying a still-live mechanism under a fresh expression, or license a full mechanism re-litigation when only the expression needed to change. |
| Leave `EXPRESSION-FAIL` unclassified, routed to neither a register nor a ladder | Reproduces exactly the defect this ADR exists to close: a confirm-phase rejection with no auditable disposition and no bounded re-entry rule, inviting unbounded expression-retrying under an alive discriminator. |
| Let the WHY class alone select the owning register, bypassing §D3's scope-based routing | Directly reopens a question 2026-08-09 §D3 already ruled, and for good reason ("the WHY class alone cannot select an owning register") — a class-based router would misfile per-direction/instrument-scoped kills into the domain-level registry or vice versa. |
| Uncap `N_expr` (no ladder termination) | Reproduces the "re-tuning is the degeneration move" failure 2026-06-14 §C already names for edge-failure, one level up — an alive discriminator would become a standing license to keep buying expression attempts indefinitely. |
| Route every pre-explore `TRADEABLE-REACHABLE` kill to `edge-failure`, since it is an early "no" | Misrepresents an arithmetic, pre-data kill as mechanism evidence — no placebo-controlled test ran. `venue / cost-constraint` is the correct existing class; this ADR maps to it rather than inventing a new one for what is structurally the same failure family as an existing cost-law kill. |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** a fifth `expression-failure` class, a closed four-verdict confirm vocabulary,
and a mechanism-keyed `N_expr` ladder correctly separate "the mechanism survived, the expression
didn't" from every other rejection shape, without creating a new unbounded re-entry path or
misrouting registry entries.

**Revert trigger:** if, by the next scheduled quarterly programme audit after this ADR's acceptance,
either (a) an `EXPRESSION-FAIL` disposition is found routed to a register other than the one §D3
would assign by scope, (b) a mechanism is found to have exceeded `N_expr` expression attempts without
either migrating to `venue / cost-constraint` on genuine cost/geometry grounds or securing an
operator ratification citing the full failure history, or (c) an `EVIDENCE-VOID` or `ROLE-BLOCKED`
disposition is found written into a WHY-rejected register — this ADR is revoked.

**Revert action:** author a superseding ADR that either re-specifies the ladder-termination rule more
strictly (e.g. a mechanical integrity check refusing a contract whose declared ordinal exceeds the
ledger's recorded count, closing gap (b) in code rather than by audit) or narrows the nonterminal
exclusion list's enforcement. Never silently edit this ADR's decision text.

**Trigger check schedule:** every quarterly programme audit (next: 2026-11-08).

---

## §5 — Forbidden moves (under this ADR)

- **Applying `edge-failure`'s "genuinely new mechanism" add-back to an `EXPRESSION-FAIL` entry.**
  Ruled out in §2/§3 — the discriminator passed; only the expression is barred, and the new class's
  own add-back (a structurally distinct expression, not a new mechanism) governs.
- **Fabricating a cost-limb failure to migrate an exhausted expression-failure ladder into `venue /
  cost-constraint` early.** Ruled out in §2 — migration is legitimate only when cost/geometry
  evidence actually fired in the recorded failure history; otherwise the ladder stays closed under
  `expression-failure` pending operator ratification.
- **Routing by WHY class instead of by §D3's scope rule**, to make register placement "follow the
  taxonomy." Ruled out in §3 — a class-based router would relitigate 2026-08-09's already-ratified
  scope-based topology.
- **Writing `EVIDENCE-VOID`, `ROLE-BLOCKED`, or `CHANNEL-FAIL` into any WHY-rejected register**, to
  give a nonterminal or channel-level event an audit trail. Ruled out in §2 — all three stay on the
  contract or the channel record only; a register entry implies a terminal, candidate-level
  rejection, which none of the three are.
- **Uncapping or silently raising `N_expr` per-mechanism** without a superseding decision. Each
  mechanism's bound is the same `N_expr` default (2) unless a future ADR rules otherwise generally —
  not something an individual campaign or operator note may adjust ad hoc.

---

## §6 — Consequences

**Positive consequences:**
- Closes the exact classification gap the note's tension #4/#8 analysis diagnosed: a confirm-phase
  rejection now always has a correctly-shaped disposition, never forced into the wrong existing class
  or left unclassified.
- Bounds expression-retrying under an alive discriminator with the same anti-degeneration discipline
  2026-06-14 §C already applies to edge-failure re-tuning — closing an asymmetric loophole the
  four-class taxonomy left open (unbounded re-tries were barred for a falsified mechanism but
  unaddressed for a surviving one).
- Gives `TRADEABLE-REACHABLE`'s pre-explore kill (2026-08-30-tradeable-reachable-gate.md) a ruled
  destination, discharging that ADR's own forward citation.
- Nonterminal states (`EVIDENCE-VOID`, `ROLE-BLOCKED`, `CHANNEL-FAIL`) stay off the permanent
  rejection record, keeping the registries a record of actual candidate-level kills only.

**Negative consequences (real cost, not theatrical):**
- A mechanism that keeps producing well-powered, cleanly-failing expressions now has a hard ceiling
  (`N_expr`, default 2) before it needs an operator ratification to continue — real friction versus
  today's unbounded (if informally discouraged) re-try practice.
- Every future confirm closure must now correctly classify itself across five classes and four
  verdicts instead of ad hoc `FALSIFIED`/`STOP`/`VOID` language — a real authoring-discipline cost,
  not free ceremony.

**Risks (probabilistic, distinct from costs):**
- `N_expr`'s default (2) is asserted here, not re-derived from cost/K data specific to this estate;
  if it proves too tight or too loose in practice, that is a parameter-calibration question for a
  future amending ADR, not evidence against the ladder mechanism itself.

**Downstream artifacts:**
- `docs/rejected_candidates.md` and `ops/instruments/<SYM>.md` schemas — still owed: additive
  fields for `class="expression-failure"`, the `N_expr` ordinal, and the cited failure history, per
  2026-06-14 §D's existing extension pattern (mechanical implementation, §7).
- `2026-06-14-rejected-candidate-patterns.md` — **landed at ratification** as a dated addendum
  overlay (its own 2026-08-29 addendum forbids in-place §A edits): the fifth class plus the
  `venue / cost-constraint` row's widened add-back, both layered on top of the byte-stable original
  table, never rewriting it.
- `2026-08-30-candidate-contract.md` — **landed at ratification**: the mechanism-level
  discriminator's complete adjudication rule added as a founding-freeze field, discharging that
  ADR's own §3 deferral.
- `2026-08-30-tradeable-reachable-gate.md` §6 — its own forward citation to this ADR is now
  discharged; no edit needed to that ADR's text (Trap #12 — decisions stay byte-stable once landed).
- `STATE.md` — new forward-board row: schema-extension implementation (registry fields, discriminator
  field) owed as a separate handoff (§7).

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time.
- **Phase 1** — this ADR's own body is the complete policy deliverable; the `Amends-in-part` edges to
  `2026-06-14-rejected-candidate-patterns.md` and `2026-08-30-candidate-contract.md` **landed at
  ratification** (this commit) — the former as a dated addendum overlay (its own 2026-08-29 addendum
  forbids in-place §A edits), the latter as a new §2 subsection.
- **Phase 2** — grep-sweep (Known Trap #7): **(i)** no predecessor to check (`Supersedes: none`);
  **(ii)** `grep -rl "EXPRESSION-FAIL\|EVIDENCE-VOID\|ROLE-BLOCKED\|CHANNEL-FAIL\|MARKET-NULL\|N_expr"
  docs/ lab/` — already executed at authoring time (§0 methodology): zero hits outside the source
  note itself, confirming these are genuinely novel vocabulary this ADR is the first to ratify, not
  a restatement of an existing convention. Re-run at implementation time to confirm no other
  in-flight branch introduced conflicting usage in the interim.

  **Post-review corrections (found by a Codex review pass on this PR, not by the sweep above):**
  three gaps in the first draft, all fixed in §2/header above. **(a)** The discriminator's
  adjudication rule, which the `MARKET-NULL`/`EXPRESSION-FAIL` distinction depends on entirely, was
  never actually frozen into the candidate contract by any of this series' six ADRs — `2026-06-14`'s
  own §3 named it as deferred, and no ADR had claimed it. Fixed by amending
  `2026-08-30-candidate-contract.md` in via this ADR's header. **(b)** Reading the `venue /
  cost-constraint` row's existing add-back as covering a shape-limb kill, without formally amending
  that row's text, left registry consumers reading the unedited row and the un-widened add-back —
  fixed by adding that row to this ADR's `Amends-in-part` scope. **(c)** The four-verdict vocabulary
  left the case "discriminator cleanly fails, payoff/temporal implementation passes" undefined —
  fixed by ruling it routes to `MARKET-NULL` (the discriminator's clean fail takes precedence over
  any payoff read, mirroring the already-stated `EVIDENCE-VOID` precedence rule).
- **Phase 3** — verification block executes; status → `Accepted`.

Mechanical enforcement (the integrity check refusing a contract with a wrong `N_expr` ordinal, and
the schema-field additions themselves) is a **separate implementation handoff** — doctrine binds
now; code may lag, per the HARV-lane precedent (`2026-08-30-candidate-contract.md` §0).

---

## §10 — Audit hooks (runnable)

```bash
# Vocabulary genuinely novel at authoring time (re-run to catch drift since).
grep -rn "EXPRESSION-FAIL\|EVIDENCE-VOID\|ROLE-BLOCKED\|CHANNEL-FAIL\|MARKET-NULL" docs/ lab/ 2>/dev/null \
  | grep -v "2026-08-30-generate-evaluate-tensions.md\|2026-08-30-terminal-taxonomy.md"

# §A's original table stays byte-stable forever (that ADR's own 2026-08-29 addendum forbids
# in-place edits) -- expect 4 in the scoped range always, both before and after ratification.
# The fifth class lands as a dated addendum overlay, not a table row -- check for that instead.
sed -n '/^### §A/,/^### §B/p' docs/adr/2026-06-14-rejected-candidate-patterns.md | grep -c "^| \*\*"
grep -n "Addendum 2026-08-30" docs/adr/2026-06-14-rejected-candidate-patterns.md

# TRADEABLE-REACHABLE's forward citation is discharged (no edit expected to that ADR's text).
grep -n "terminal-taxonomy" docs/adr/2026-08-30-tradeable-reachable-gate.md

# Discriminator field landed in the candidate contract's founding freeze?
grep -n "terminal-taxonomy\|discriminator" docs/adr/2026-08-30-candidate-contract.md

# venue/cost-constraint row's add-back widened to admit a shape-limb clear?
grep -n "shape/geometry that clears" docs/adr/2026-06-14-rejected-candidate-patterns.md

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-30-terminal-taxonomy.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/adr/2026-06-14-rejected-candidate-patterns.md
$ git log -1 --format="%h %ci" -- docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md

# Downstream artifact update verification (post Amends-in-part landing)
$ grep -n "expression-failure" docs/adr/2026-06-14-rejected-candidate-patterns.md
```

---

## Ratification note

**Ratified by:** Joshua, direct instruction ("ratify the six ADRs," 2026-08-30), following a
self-conducted adversarial re-read (the full 6-lens Workflow panel was declined for cost) that added
the missing amendment-first/dedup attestation (§0), and executed both `Amends-in-part` edges
(`2026-06-14-rejected-candidate-patterns.md` as a dated addendum overlay — not an in-place table
edit, per that ADR's own 2026-08-29 addendum forbidding one; `2026-08-30-candidate-contract.md` as a
new §2 subsection) at this same ratification.

**§6-class preconditions at ratification:** mechanical checks clean (`check_brief.py` 0 HARD,
`check_adr_graph.py` OK) ✓ · amendment-first dedup run, one high-scoring hit read in full and
confirmed a false positive, no genuine prior art ✓ · the Codex review round's 3 findings on this
file (unfrozen discriminator field, un-amended existing taxonomy row, the undefined
discriminator-fail/payoff-pass verdict combination) verified already fixed in this file's current
text ✓ · both `Amends-in-part` edges confirmed landed (§10 hooks) ✓.

**Not licensed by this ratification:** building the `N_expr` ordinal integrity check or the registry
schema-field additions (§7, separate implementation handoff) · any edit to `core/`, `ops/`,
`dd_protection`, or allocations.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring | Joshua + Claude Code |
| 2026-08-30 | Ratified — status → `Accepted`; both `Amends-in-part` edges landed | Joshua (operator ratification) |
