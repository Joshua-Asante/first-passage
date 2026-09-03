# Evaluation order — one canonical ordered pipeline; role and composition screens gate fit, never lifecycle admission — `evaluation-order`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-30; see Ratification note.
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Amends-in-part:** `2026-08-30-candidate-contract.md` — adds the scoped account/book identifier +
compliance-state snapshot, the ROLE-BLOCKED succession-rule declaration, and the append-only
selection-freeze commit to the contract schema; the frozen multiplicity configuration (`α`/`M`/
Bonferroni-or-Holm procedure identity) itself is **not** added here — it is
`2026-08-30-operator-approvals-campaign-envelope.md`'s field, cited by this ADR's confirm-ordering
step, not re-decided.
**Layer:** methodology (pipeline sequencing and role/composition-screen scope only). No
`dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue
action; no spend.
**Tier:** full — Limb 4 fires (creates the standing binding order every candidate contract's
pipeline must follow).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, this session (2026-08-30):

- `docs/notes/2026-08-30-generate-evaluate-tensions.md` — anchor `419433a` (2026-08-30). "Simplify
  evaluation order" and "Defer portfolio composition" rows: one ordered battery from structural
  class-level screening (pre-K, pre-pull) through contract freeze, `TRADEABLE-REACHABLE`, Explore
  closed by a selection freeze, contract integrity, a zero-K role state-drift re-check, one atomic
  confirm verdict, to portfolio/venue fit last. Generate-phase steps 2/5/7 and evaluate-phase steps
  1/2/4 supply this ADR's operative mechanics; step 2's ordering point (structural limbs pre-K) is
  already ratified doctrine (next bullet), not something this ADR re-decides.
- `docs/spec/2026-08-05-eval-mechanism-shape-screen.md` §2.0a — anchor `340722c` (2026-08-24).
  RATIFIED, general form (post-Route-B-retirement addendum, same section): "EM0–EM5 is applied to a
  candidate *class* or a *catalogue*, before any data is examined — never to a scored candidate list
  afterward... applying it early costs nothing and applying it late costs K." This ADR's step-1
  ordering point (structural limbs pre-catalogue-freeze) applies this already-ratified placement
  rule to the canonical pipeline; it does not re-decide §2.0a.
- `docs/methodology/objective_composition_map.md` — anchor `e11fd39` (2026-08-24). "Candidate
  admission" section: Stage-8 variance-dominance/risk-breadth and the third-leg spec's own screens
  are "necessary, not sufficient — never a substitute for" the survivor-scoring Part-A admission
  gate; "gate[s] composition-into-the-book only. They do not gate lifecycle admission" (quoting
  Stage-8's own doctrine row and methodology lesson M-21). This ADR's ruling that role/composition
  screens gate fit-for-scope, never candidate lifecycle, **applies** this already-ratified
  precedence — it is not a new precedence rule.
- `docs/spec/2026-07-27-third-leg-target-spec.md` §7.1 — anchor `25711e2` (2026-08-26). S1–S7 hard
  structural/compliance limbs (Product-Group/sign, session, cap, S7 order-symbol occupancy,
  instrument-class), explicitly "no discretion" and adjudicated before R4 (risk-breadth) ever scores
  (§6.2 adjudication table, cited via the composition map, §0 above). These are the concrete limbs
  this ADR's role state-drift re-check re-validates against the *current* compliance snapshot.
- `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md` — anchor `e11fd39` (2026-08-24),
  as superseded-in-part by `2026-08-07-w4-minimal-gate-set-dormancy.md` (same anchor): risk-N_eff
  coordinates stay Stage-8 doctrine but `breadth.py` is tombstoned as sole producer — report-optional
  until a re-arm ADR restores a producer. This ADR's role re-check includes variance-dominance only
  while a producer is live, per that dormancy status, unedited here.
- `ops/prop_envelope_default.md` §4a — anchor `e11fd39` (2026-08-24). Hedging/Product-Group
  precedence: absolute, no exceptions, across **any account under the same control** — wider scope
  than the account/book-scoped cap/session/S7-occupancy limbs. This ADR's role re-check inherits
  this scope distinction unedited (§2 below).
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` §2 item 1 — anchor `e11fd39`.
  "`register_search open --lane blind` before results are seen" — the estate's own standing
  convention that a manifest binds K before any exploration data is read, not merely checked
  afterward. Found via a review pass on this ADR's first draft (§7): step 6 (Explore) originally
  read as permitting the catalogue to be scored before step 7's K check ever ran, letting real trials
  proceed unbound — this citation grounds the fix (K-ledger bind moved to the start of step 6, §2).
- `docs/adr/2026-08-30-candidate-contract.md` — anchor `7669664` (2026-08-30, this branch). §2's own
  text names "evaluation order" as the owner of deferred fields including the multiplicity
  configuration and, implicitly, the fields this ADR's Amends-in-part adds; §3 explicitly rules that
  enumerating those fields inside ADR-1 itself "would violate 'ADRs document ONE decision.'"
- `docs/adr/2026-08-30-tradeable-reachable-gate.md` — anchor `a682b74` (2026-08-30, this branch).
  §2: `TRADEABLE-REACHABLE` runs pre-Explore, after contract freeze — this ADR places it at exactly
  that point in the canonical sequence (step 4 below) and does not re-decide its own mechanics.
- `docs/adr/2026-08-30-terminal-taxonomy.md` — anchor `60e8cd3` (2026-08-30, this branch). §2: the
  closed confirm-phase verdict vocabulary (`CONFIRMED`/`MARKET-NULL`/`EXPRESSION-FAIL`/
  `EVIDENCE-VOID`) and the nonterminal `ROLE-BLOCKED` disposition this ADR's role re-check (step 5
  below) emits into — **this ADR is the decision terminal-taxonomy's own `ROLE-BLOCKED` bullet
  forward-cited as `2026-08-30-candidate-contract.md`'s evaluate-phase role re-check**, a citation
  error caught by this ADR's own Phase-2 sweep (§7) — the role re-check is this ADR's decision, not
  ADR-1's; corrected in that ADR as a follow-up (§6 below).

**Amendment-first / dedup (Rule 8 sub-rule 10), run at ratification:**

```
$ python scripts/check_advisor_dedup.py --keywords "evaluation order canonical pipeline sequence role composition screen fit lifecycle admission selection freeze"
```

186 candidates surfaced, all keyword-overlap noise from instrument ledgers and unrelated claim-alignment audit findings — none proposes a single canonical ordered pipeline. No existing ADR or brief performs this ADR's decision.

---

## §1 — Context

Three pipeline-sequencing facts are each separately ratified today — `eval-mechanism-shape-screen.md`
§2.0a places structural class-level screening before any data is examined; the composition map
records that role/composition screens are necessary-but-not-sufficient pre-screens, never a
substitute for lifecycle admission; `2026-08-30-tradeable-reachable-gate.md` places its own pre-gate
after contract freeze and before Explore — but no single artifact states the **complete** ordered
sequence a candidate contract actually moves through, end to end. Two further mechanics that
sequence depends on are undefined anywhere: an append-only commit closing Explore before any holdout
access (so "the selected set matches the frozen contract" is checkable), and a cheap, zero-K
re-validation between scoping and confirm that catches occupancy/cap drift without re-running the
class-level screen.

Absent an explicit order, two failure modes are live. First, a role or composition check could be
read as gating candidate survival itself (contradicting the composition map's own ruling) if nothing
states which gate is genuinely a lifecycle admission gate and which is a fit-for-scope check.
Second, without an append-only selection freeze, a post-Explore "which candidates were actually
selected" claim is unverifiable — selection necessarily post-dates contract freeze, so nothing
today pins it before holdout access.

**Decision driver (one sentence):** the pipeline's already-ratified sequencing facts and gates need
one explicit end-to-end order that ties them together, plus two currently-undefined mechanics (an
append-only post-Explore selection freeze, and a zero-K pre-confirm role/compliance re-check) that
the order cannot be stated correctly without.

---

## §2 — Decision

**Decision:** Every candidate contract moves through one canonical ordered pipeline. Each step's
gating scope is stated explicitly — lifecycle-admission, fit-for-scope, or integrity-only — so no
step is ever read outside its own scope.

1. **Structural class-level screening (pre-catalogue-freeze, pre-K, pre-pull).** The structural limbs
   of the eval-mechanism-shape screen (EM0 catalogue, EM3 independence arithmetic, EM4 activity by
   construction, EM5/N-SHAPE importing Product-Group/sign, session law, and S7 occupancy by
   reference) apply to the candidate class/catalogue, per §2.0a's already-ratified placement (§0) —
   this ADR states the ordering point, not the rule. The measured N-EDGE/N-SIZE limbs defer to their
   declared data source and are not claimed here (unchanged from §0's own text).
2. **CONFIRM-window reservation, then payoff-shape priors or extraction probe.** Per
   `2026-08-30-tradeable-reachable-gate.md` §2 — cited, not re-decided.
3. **All-clause reachability attestation (pre-freeze, HARV-lane).** Per the same ADR §2 and its own
   §0 citations — cited, not re-decided.
4. **Contract freeze.** Per `2026-08-30-candidate-contract.md` §2 — cited, not re-decided, plus the
   three fields this ADR's Amends-in-part adds (below).
5. **`TRADEABLE-REACHABLE` (pre-Explore).** Per `2026-08-30-tradeable-reachable-gate.md` §2 — cited,
   not re-decided.
6. **K-ledger bind, then Explore, closed by an append-only selection freeze.** Before any cell is
   scored — before any exploration data is read — the campaign's `register_search open` manifest
   binds K/α/window against the frozen contract's declared values, per the K-ledger ruling
   (`2026-08-30-candidate-contract.md` §2) and the estate's own standing convention that a manifest
   opens "before results are seen" (§0: `2026-08-15-no-counterparty-statistical-sourcing-channel.md`
   §2 item 1). Binding K only at step 7, after Explore's reads already happened, would let real
   trials run with no live-tracked ledger entry — a later integrity check cannot retroactively
   restore accounting for reads that already occurred unbound. Only once the manifest is open does
   Explore score every declared cell in the frozen catalogue and select at most the frozen confirm
   count. Explore closes with an **append-only selection freeze**: the full scored ranking (not only
   the selected subset) and the selected candidates are committed to the contract, hash-pinned,
   before any holdout access. Without this commit, "the selected set matches the frozen contract" is
   unverifiable, since selection necessarily post-dates step 4's freeze — this is this ADR's own new
   mechanic, not a restatement of an existing one. (Corrected in review — see §7 for the finding this
   fixes.)
7. **Contract-integrity check (evaluate phase, first, integrity-only).** Before any other evaluate-
   phase check runs: confirm that code/data hashes, the register_search manifest's `K` against the
   contract's declared `K` (bound at step 6, re-checked here, not bound for the first time here), the
   frozen multiplicity configuration (owned by `2026-08-30-operator-approvals-campaign-envelope.md`,
   cited not re-decided here), the candidate under evaluation against step 6's hash-pinned commit —
   **either as a member of the originally selected set, or, for a succession substitute entering
   under step 8's pre-declared mechanical-succession rule, at its own frozen rank position in step
   6's full scored ranking** (not only the originally-selected subset — a substitute is never
   already a member of that subset by definition, so checking against the subset alone would reject
   every legitimate succession) — and the holdout against step 2's reservation, all match the frozen
   contract. A mismatch voids or stops the attempt on its own — it is never recorded as a structural
   or evidentiary rejection (consistent with `2026-08-30-terminal-taxonomy.md`'s `EVIDENCE-VOID`
   class, §0).
8. **Role state-drift re-check (zero-K, fit-for-scope, never lifecycle).** Before any holdout is
   consumed, re-validate each selected candidate against the *current* compliance snapshot versus the
   one frozen in the contract: Product-Group/sign, cap, session, and S7 order-symbol occupancy
   (third-leg spec §7.1 S1–S7, §0), plus variance-dominance/risk-N_eff-delta only while a live
   producer exists (report-only while `breadth.py` stays tombstoned, §0). This step exists because
   step 1 already ran the *class-level* application of these limbs — a failure here means the
   *state* moved (occupancy or cap changed between scoping and confirm), never that a screen was
   skipped. **None of these limbs are candidate-lifecycle absolute** — each gates only the
   candidate's proposed role at the currently scoped account/book, consistent with the composition
   map's own ruling (§0), never the candidate outright. Cap, session, and S7 occupancy are scoped to
   the single account/book in scope — a rejection there may clear on a different, non-affiliated
   account. Product-Group/sign is scoped wider — absolute across *any* account under the same
   control (`prop_envelope_default.md` §4a, §0) — so a Product-Group/sign rejection clears only
   outside the whole controlled-account group. A failure emits `ROLE-BLOCKED`
   (`2026-08-30-terminal-taxonomy.md` §2) naming the limb and the compliance snapshot scored against
   — a role verdict, never a rejection, never a register entry. Its confirm slot follows the
   **succession rule frozen in the contract** (this ADR's own Amends-in-part field, below):
   **forfeit by default** (the slot goes unread, the multiplicity divisor stays at the frozen `M`),
   or, if pre-declared, **mechanical succession** — the next-ranked candidate from the step-6 frozen
   ordering takes the slot, after itself passing steps 7 and 8 in full, never directly into a
   holdout read.
9. **One untouched confirm run, including temporal robustness, as one atomic step.** Per
   `2026-08-30-terminal-taxonomy.md` §2's verdict vocabulary — cited, not re-decided. The confirm
   statistic and the frozen minimum temporal-consistency battery run together; a single verdict is
   emitted only once both clear.
10. **Portfolio and venue fit, last.** For a `CONFIRMED` candidate only: re-run step 8's role
    re-check if the deployment target changed since scoping, and always re-check S7 occupancy
    specifically (dynamic, can move independently of the target). Then score remaining composition,
    firm-level aggregate constraints, activity, drawdown, and sizing — **only after an edge exists**.
    A failure here rejects that book-leg placement, not the candidate's standalone confirmed status
    (`2026-08-30-terminal-taxonomy.md`'s edition axis, §0) — never evidence the market effect is
    false.

**Scope-class summary (the ruling this whole order exists to make explicit):** steps 1 and 8/10's
role/composition limbs are **fit-for-scope** gates, step 7 is **integrity-only**, and only the
survivor-scoring Part-A admission gate (outside this ADR's scope entirely — per the composition map,
§0) is **lifecycle-admission**. No step in this pipeline gates candidate lifecycle by itself.

**Effective:** immediately upon acceptance, for any candidate contract frozen after this date.
**Scope:** the ordered pipeline and role/composition-screen scope, across all five live channels
(GROW is tooling inside deep-iteration, not a sixth channel — matching
`2026-08-30-channel-liveness-gate.md`'s own derivation). Does not alter any cited gate's own
thresholds, ownership, or mechanics — it sequences them.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Let the role state-drift re-check (step 8) gate candidate lifecycle when it fails | Directly contradicts the composition map's own ratified precedence — role/composition screens are "necessary, not sufficient... They do not gate lifecycle admission." Making step 8 lifecycle-absolute would silently overturn that ruling without an amending ADR naming it. |
| Skip the append-only selection freeze (step 6); let the evaluate phase trust whatever candidates arrive | Makes "the selected set matches the frozen contract" unverifiable, since selection necessarily post-dates contract freeze — reopens exactly the kind of undetected drift `2026-08-30-candidate-contract.md` exists to close for the founding fields. |
| Re-run the full class-level structural screen (step 1) again at step 8, instead of a lighter state-drift re-check | Wastes K re-scoring limbs that provably have not changed (the catalogue-level structure is frozen at step 4); the state that actually moves between scoping and confirm is compliance snapshot data (occupancy, cap), not the catalogue — a targeted re-check is the correct-cost instrument. |
| Fold the multiplicity configuration into this ADR's own decision, since step 7 needs to check it | The note's own row structure (§0) introduces `α`/`M`/procedure under "simplify operator approvals," not evaluation order; duplicating ownership here would contradict `2026-08-30-candidate-contract.md`'s own naming of a distinct forthcoming ADR for it and risk two ADRs defining the same field inconsistently. |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** one explicit ten-step ordered pipeline, with role/composition screens correctly
scoped as fit-not-lifecycle at every step, correctly closes the sequencing gap without silently
promoting any fit-for-scope check into a lifecycle-admission gate.

**Revert trigger:** if, by the next scheduled quarterly programme audit after this ADR's acceptance,
either (a) a candidate is found rejected from the estate's admission register on the strength of
step 1, 8, or 10 alone (with no separate Part-A admission-gate finding), or (b) a candidate contract
is found to have run any step out of the order above without a documented, pre-declared exception —
this ADR is revoked.

**Revert action:** author a superseding ADR that either re-states the scope-class boundary more
mechanically (e.g. a lint refusing a `ROLE-BLOCKED`/`VENUE-FAIL` disposition to be cited as grounds
for a lifecycle-register entry) or corrects the ordering itself if a genuine sequencing defect is
found. Never silently edit this ADR's decision text.

**Trigger check schedule:** every quarterly programme audit (next: 2026-11-08).

---

## §5 — Forbidden moves (under this ADR)

- **Treating a `ROLE-BLOCKED` or step-10 `VENUE-FAIL` disposition as grounds for a lifecycle-register
  entry.** Ruled out in §2/§3 — both are fit-for-scope verdicts; the composition map's own
  already-ratified precedence governs, unedited by this ADR.
- **Re-running step 1's full class-level screen at step 8** to avoid defining a lighter re-check.
  Ruled out in §3 — wastes K on limbs that cannot have changed since freeze.
- **Skipping the append-only selection freeze (step 6)** for a channel whose tooling makes it
  inconvenient. Ruled out in §2/§3 — the freeze is what makes the evaluate phase's integrity check
  (step 7) meaningful at all.
- **Defining or freezing the multiplicity configuration inside this ADR** because step 7 needs to
  check it. Ruled out in §3 — that field belongs to
  `2026-08-30-operator-approvals-campaign-envelope.md`; this ADR cites it once ratified.
- **Letting mechanical succession (step 8) exercise discretion after exploration results are
  visible.** The next-ranked candidate is fixed by the step-6 frozen ordering alone — never a
  post-hoc pick.

---

## §6 — Consequences

**Positive consequences:**
- States, for the first time in one place, the complete ordered sequence a candidate contract moves
  through — closing the implicit-ordering gap the note's tension #8 (reachable process falsifiers)
  and #5 (firm-specific feasibility bleeding into sourcing) both partly trace to.
- Makes explicit, at every step, whether a gate is lifecycle-admission, fit-for-scope, or
  integrity-only — preventing the specific misreading (a role/composition screen silently treated as
  lifecycle-absolute) the composition map already warns against for Stage-8 and the third-leg spec.
- Gives Explore a verifiable closing commit (the selection freeze) and gives the evaluate phase a
  cheap, correctly-targeted re-check (state-drift, not a full re-screen) instead of either an
  unverifiable selection claim or a wastefully-repeated structural screen.

**Negative consequences (real cost, not theatrical):**
- Every channel's tooling must now produce an explicit, hash-pinned selection-freeze commit at
  Explore close — real build work, not free ceremony (§7).
- A candidate that drifts out of compliance between scoping and confirm now costs its confirm slot
  (forfeit) or requires a pre-declared succession rule to recover it — friction versus today's
  undocumented ad hoc handling.

**Risks (probabilistic, distinct from costs):**
- If a future channel's tooling cannot cheaply distinguish "class-level structural state" from
  "compliance snapshot state," step 8's cost advantage over re-running step 1 may not materialize in
  practice — a build-time risk for the separate implementation handoff (§7), not a defect in this
  ADR's own ordering logic.

**Downstream artifacts:**
- `2026-08-30-candidate-contract.md` — **landed at ratification** (this commit): scoped account/book
  identifier + compliance-state snapshot, ROLE-BLOCKED succession-rule declaration, and the
  selection-freeze commit added to the contract schema.
- `2026-08-30-terminal-taxonomy.md` — its `ROLE-BLOCKED` bullet currently cites
  `2026-08-30-candidate-contract.md`'s "evaluate-phase role re-check," which does not exist in that
  ADR's own text; the role re-check is this ADR's decision (step 8). Correcting that citation is a
  small follow-up edit to an already-`Proposed` (not yet `Accepted`) ADR — landed alongside this
  commit (Trap #12 does not apply pre-acceptance).
- `STATE.md` — new forward-board row: selection-freeze + role-re-check mechanical implementation
  owed as a separate handoff (§7).

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time.
- **Phase 1** — this ADR's own body is the complete policy deliverable; the `Amends-in-part` edge to
  `2026-08-30-candidate-contract.md` **landed at ratification** (this commit), as a new §2 subsection
  on that ADR.
- **Phase 2** — grep-sweep (Known Trap #7): **(i)** no predecessor to check (`Supersedes: none`);
  **(ii)** `grep -rl "selection freeze\|state-drift\|contract.integrity\|ROLE-BLOCKED" docs/adr/
  docs/spec/ docs/methodology/` — executed at authoring time: exactly 3 hits, all under `docs/adr/`
  and all this session's own prior work — `candidate-contract.md`, `terminal-taxonomy.md`, and this
  file itself. Zero hits in `docs/spec/` or `docs/methodology/`, confirming these mechanics are
  genuinely undefined outside this session's own three-ADR set (the source note under `docs/notes/`
  is outside this sweep's searched paths by construction, same convention ADR-1/ADR-2 used). The
  `2026-08-30-terminal-taxonomy.md` hit is the citation-error bullet corrected in that file as part
  of this same change (§6 above).

  **Post-review corrections (found by a Codex review pass on this PR):** two ordering defects in the
  first draft's step sequence, both fixed in §2 above. **(a)** Step 6 (Explore) permitted scoring the
  full catalogue before step 7's K-integrity check ever ran, letting real trials proceed with no
  live-tracked ledger entry — a later check cannot retroactively restore accounting for reads that
  already happened unbound. Fixed by moving the `register_search open` K-ledger bind to the start of
  step 6, before any cell is scored, per the estate's own "before results are seen" convention (§0).
  **(b)** Step 8's mechanical-succession substitute (drawn from step 6's full ranking, not the
  originally-selected subset) had no path to pass step 7's integrity check as originally worded,
  since that check validated only against "the selected candidates" — a substitute is, by
  definition, never a member of that subset. Fixed by stating explicitly that step 7 validates a
  candidate either as an original selectee or, for a succession substitute, at its own frozen rank
  position in the full scored ranking.
- **Phase 3** — verification block executes; status → `Accepted`.

Mechanical enforcement (the selection-freeze hash-pinning tool, the state-drift re-check script) is
a **separate implementation handoff** — doctrine binds now; code may lag, per the HARV-lane
precedent (`2026-08-30-candidate-contract.md` §0).

---

## §10 — Audit hooks (runnable)

```bash
# Every step's gating scope is stated (lifecycle-admission / fit-for-scope / integrity-only).
grep -c "fit-for-scope\|lifecycle-admission\|integrity-only" docs/adr/2026-08-30-evaluation-order.md

# ROLE-BLOCKED citation in terminal-taxonomy.md points at THIS ADR, not candidate-contract.md.
grep -n "ROLE-BLOCKED" -A2 docs/adr/2026-08-30-terminal-taxonomy.md | grep -n "evaluation-order\|candidate-contract"

# Candidate-contract amendment landed?
grep -n "evaluation-order" docs/adr/2026-08-30-candidate-contract.md

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-30-evaluation-order.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/spec/2026-08-05-eval-mechanism-shape-screen.md
$ git log -1 --format="%h %ci" -- docs/methodology/objective_composition_map.md

# Downstream artifact update verification (post Amends-in-part landing)
$ grep -n "evaluation-order" docs/adr/2026-08-30-candidate-contract.md
```

---

## Ratification note

**Ratified by:** Joshua, direct instruction ("ratify the six ADRs," 2026-08-30), following a
self-conducted adversarial re-read (the full 6-lens Workflow panel was declined for cost) that added
the missing amendment-first/dedup attestation (§0).

**§6-class preconditions at ratification:** mechanical checks clean (`check_brief.py` 0 HARD,
`check_adr_graph.py` OK) ✓ · amendment-first dedup run, no genuine prior art ✓ · the Codex review
round's 2 findings on this file (the K-ledger bind ordering vs. step-6 Explore; the mechanical-
succession/integrity-check gap) verified already fixed in this file's current text ✓ · the
`Amends-in-part` edge to `candidate-contract.md` confirmed landed (§10 hook) ✓.

**Not licensed by this ratification:** building the selection-freeze hash-pinning tool or the
state-drift re-check script (§7, separate implementation handoff) · any edit to `core/`, `ops/`,
`dd_protection`, or allocations.

---

## Addendum 2026-09-03 — canonical-owner cross-reference: `PIPELINES.md` P1 and the throughline diagram now point here; this ADR's decision text is unedited

**Status of this addendum: informational, no decision-text change (Trap #12 — §2's decision stands
byte-stable).** Filed to close a gap the pipeline-diagram re-audits named without fixing: PR #262's
`open_gaps` entry (carried unresolved into PR #264) read *"Three competing decompositions of one
pipeline now coexist: this map's 12 phases, `PIPELINES.md`'s Stage 2→8..., and `evaluation-order`'s 10
steps. None cross-references the others."*

This ADR is the **single canonical owner** of pipeline step ordering — its own title says so, and §2
states it as "one canonical ordered pipeline." `PIPELINES.md` P1 now points here explicitly, framing
its Stage 2→8 list as the **document shape** that is today's live practice (per
`2026-08-30-candidate-contract.md` §6: each channel's existing freeze-chain documents remain its live
practice until that channel's own migration addendum lands) — never as a rival step order. That
carve-out is `candidate-contract`'s own, about which artifact records a candidate; it does not extend
to this ADR. §2's own effectivity clause carries no migration carve-out ("immediately upon acceptance,
for any candidate contract frozen after this date"), so this ADR's order already governs any contract
frozen after 2026-08-30, including one still recorded in a pre-migration channel's old document shape.
`docs/diagrams/generate-evaluate-throughline.html` is the visual/interactive companion and now states
the identical distinction (its own 2026-09-03 revision), and its per-ADR `pending_doctrine` entry
already carried the correct "EFFECTIVE for any candidate contract frozen after 2026-08-30" framing
this addendum aligns `PIPELINES.md` to.

Neither `PIPELINES.md` nor the diagram gains authority to redefine this ADR's step order — a future
change to §2 lands here first. But neither is a bare pointer today: `PIPELINES.md` carries its own
ordered Stage 2→8 list and the diagram's `pending_doctrine.items` entry for this ADR restates the full
ten-step sequence for readers who don't open this file. A future §2 change means updating **both**
restatements to match, not only their pointer prose — Rule 7 (`docs/operational_rules.md`) makes this
ADR the fact's owner, not the sole place the fact may ever appear.

This addendum also discharges this ADR's own §6 "STATE.md — new forward-board row" downstream
artifact, together with the three sibling 2026-08-30 ADRs carrying the identical unmet obligation
(`terminal-taxonomy`, `tradeable-reachable-gate`, `operator-approvals-campaign-envelope`) — one shared
row, `STATE.md`'s 2026-11-08 section, the same row-sharing convention `2026-08-30-channel-liveness-gate.md`
and `2026-08-30-candidate-contract.md` already used for their own shared row. This addendum does not
build the selection-freeze hash-pinning tool or the state-drift re-check script (§7) — those remain
owed, dated, unbuilt.

No `core/`, `ops/`, `dd_protection`, Pine, or allocation change. No campaign, contract, K, or spend
opened. $0/K=0.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring | Joshua + Claude Code |
| 2026-08-30 | Ratified — status → `Accepted`; `Amends-in-part` edge to candidate-contract.md landed | Joshua (operator ratification) |
| 2026-09-03 | Addendum — cross-referenced `PIPELINES.md` and the throughline diagram as pointers to this ADR's canonical order; discharged the four ADRs' shared owed STATE.md row | Claude Code |
