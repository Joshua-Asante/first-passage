# One candidate contract per generated candidate — hash-pinned, append-only, replacing duplicate seed-manifest/G0/preregistration restatement — `candidate-contract`

**Status:** `Proposed`
**Decision date:** 2026-08-30
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Authors:** Joshua (direction) + Claude Code (drafter)
**Layer:** methodology (candidate-generation admission + document discipline only). No `dd_protection`, allocation, lifecycle, Pine, or rail config touched; nothing armed; no venue action; no spend.
**Tier:** full — Limb 4 fires (creates standing doctrine binding every future candidate-generation artifact).

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR, this session (2026-08-30):

- `docs/notes/2026-08-30-generate-evaluate-tensions.md` — anchor `419433a` (2026-08-30). Table row "Merge generation charter and admission manifest": "G0, seed manifests, and later preregistrations can restate instrument, K, windows, costs, and feature definitions... Create one immutable candidate contract at generation open; later stages append results and hashes rather than copying fields." Table row "Delete proxy-only promotion": "Do not admit a generated candidate unless it already specifies signal, entry clock, stop, exit/target, holding horizon, and costed payoff unit."
- `docs/methodology/strategy_harvest.md` — anchor `936eb0f` (2026-08-29). §5 seed-manifest template restates instrument, K, δ/σ, N/event-frequency, dedup attestation; §6 procedure runs Dedup → Manifest → Stage-0 preregistration as three separate documents in sequence. §2.3 confirms this per-lane duplication pattern; no field-level consolidation exists anywhere in the estate today.
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` — anchor `e11fd39` (2026-08-24). HARV lane's owning ADR (Accepted, standing doctrine, §5 forbids silent amendment). Requirement 1a mandates the four-clause mechanism definition (WHO/WHEN/WHY/HOW) at admission — the closest existing analogue to "a complete trade object required before candidate status." Requirement 1a does not, however, require a costed entry/exit *trade* object (stop, target, holding horizon) — it requires a *mechanism* story, which is a weaker admission bar than this ADR's.
- `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` — anchor `151cb18` (2026-08-29). HARD gate: a pre-registration gate-reachability simulation of every bundled clause, before freeze / before `register_search open`. Names the freeze-chain shape (seed manifest → intake screen → Stage-0 preregistration) this ADR replaces with a single contract for HARV specifically.
- `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` — anchor `e11fd39`. Dense-1m/TNEC freeze-chain: scoping brief (step 1) → `PREREG_G0.md` freeze (step 3), two separate documents restating instrument/K/windows/cost/entry construct.
- `docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md` — anchor `e11fd39`. MSL freeze-chain: slate card (step 1) → G0 preregistration freeze (step 5), same two-document restatement pattern.
- `docs/adr/2026-08-12-msl-sourcing-channel-ratification.md` — anchor `e11fd39`. MSL's ratifying ADR; confirms the charter's freeze-chain shape is itself ratified doctrine, not informal practice.
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` — anchor `e11fd39`. A fifth live channel with its own admission/freeze mechanics, confirmed in scope for this ADR's forward-looking requirement.
- `docs/adr/2026-08-16-deep-iteration-lane-charter.md` — anchor `e11fd39`. The fifth live channel (the `--lane deep` path), its own grammar/K freeze mechanics, confirmed in scope. GROW-lane tooling is inside deep-iteration, not a sixth channel — matching `2026-08-30-channel-liveness-gate.md` §1's own derivation, missed in this ADR's first-draft channel count (corrected throughout, caught by review).
- `docs/methodology/avenue_a_generate_confirm.md` — anchor `340722c` (2026-08-24). Withdrawn Route B checklist; its C0 step required the confirmatory preregistration to "copy the feature byte-faithfully from G2" *specifically* so the explore-stage (G0) and confirm-stage (C0) commits stayed separate artifacts — an anti-laundering boundary that stops the confirm run from being scored with knowledge of which explore candidate "won." This is the property a single mutable "contract" file must not silently destroy.
- `lab/discovery/register_search.py` — anchor `e11fd39`. `open_run()` (lines 640–714) is the one place K is machine-enforced today, writing to `discovery_manifests/*.json`. This ADR does not replace that ledger; see §2 K-ledger ruling.
- `discovery_manifests/README.md` — anchor `e11fd39`. "The rigorous universe-level correction... happens downstream... this ledger just makes K an auditable, timestamped fact." Confirms the ledger's role is narrower than a full candidate record — it is the K accounting layer, not the candidate's full field set.
- `docs/rejected_candidates.md` — anchor `0c305d7` (2026-08-24). Confirms candidates that never reach a tradeable object today still consume registry/dedup bandwidth as free-text entries; a required entry/exit object at admission reduces this class going forward.
- `docs/adr/2026-06-14-rejected-candidate-patterns.md` — anchor `0395f56` (2026-08-29). §A's 4-class WHY-rejected taxonomy and its add-back conditions; this ADR's contract must not disturb any add-back condition (§5).

---

## §1 — Context

Every live sourcing channel runs its own multi-document freeze chain — a
seed manifest or slate card, then a separate intake screen, then a separate
Stage-0/G0 preregistration — each restating the same facts about the same
candidate (instrument, K, windows, costs, feature definition) in its own
file. `strategy_harvest.md` §5–§6 names this explicitly for HARV; the
dense-1m/TNEC and MSL charters run the identical two-document shape under
different names. None of this restatement is machine-checked for
consistency across the documents that carry it — a candidate's Stage-0
preregistration can drift from its seed manifest with no gate to catch it.
Separately, nothing in any of these freeze chains requires a candidate to
specify a complete, costed, tradeable entry/exit object before it is
admitted — Requirement 1a's four-clause mechanism definition is a *causal
story* requirement, not a *trade* requirement, and Route B's own
retrospective diagnosis (`docs/notes/2026-08-30-generate-evaluate-tensions.md`
tension 4) found this gap let a generated statistic (a correlation target)
win generation and consume a reserved confirm window years before anyone
checked whether it described an executable trade.

**Decision driver (one sentence):** five live channels each restate the same
candidate facts across separate documents with no consistency check between
them, and none requires a tradeable object before admission.

---

## §2 — Decision

**Decision:** At generation-open, every new candidate — across every
sourcing channel — gets exactly **one candidate contract**: a single
hash-addressed artifact, structured as a sequence of named, append-only
freeze points rather than one freely-editable file (preserving the
anti-laundering separation `avenue_a_generate_confirm.md`'s C0 step
achieved by requiring separately-committed documents, §0). The founding
freeze (generation-open, before any exploration data is examined) must
record, at minimum:

- **Instrument** and **feature catalogue** (the declared candidate
  description / search space).
- A **complete tradeable entry/exit object** — signal, entry clock, stop,
  exit/target, holding horizon, and a costed payoff unit. A candidate
  missing any one of these fields is not yet a candidate and cannot be
  admitted; exploratory proxy work (a correlation, an order-flow
  aggregate, a response statistic with no defined trade) may continue as
  a diagnostic, but cannot open a contract, consume a confirm holdout, or
  claim candidate status. This discharges the "delete proxy-only
  promotion" requirement (§0) as a hard admission gate, not a review
  norm.
- **Exploration and confirm windows**, **K**, **costs**, and **schema
  ladder**.
- The **campaign envelope** it opens under.

**Cardinality — one contract per campaign, not per selected cell.** The
contract's "feature catalogue" field (above) already declares a *search
space*: one fixed entry/exit object template (signal, entry clock, stop,
exit/target, holding horizon, costed payoff unit), explored across
whichever feature/parameter cells the catalogue enumerates. "One candidate
contract" means one contract per such generation-open campaign, opened
once, before Explore runs. `2026-08-30-evaluation-order.md`'s Explore step
selects **up to `M`** winning cells from that one catalogue — each a
parameterization of the *same* template, not a separately-defined trade
object — and each selected cell is tracked as its own hash-pinned
sub-entry **within** the single contract (the selection freeze, ranking,
and `2026-08-30-operator-approvals-campaign-envelope.md`'s multiplicity
configuration all live at the contract's own top level, governing every
cell the catalogue produces, never duplicated per cell). `M > 1` never
means `M` candidates sharing one contract improperly, nor `M` separate
contracts with no artifact owning the family: it means one contract whose
Explore step is licensed to advance up to `M` of its own catalogue's cells.
A genuinely distinct entry/exit **template** — a different signal, stop
family, or holding-horizon class, not a different parameterization of the
same one — requires its own, separately-opened contract; it is never a
second cell inside an existing one. (This paragraph resolves a cardinality
ambiguity a review pass caught in the first draft — see §7.)

No separate seed-manifest, slate-card, G0, or Stage-0 preregistration
document may restate these fields going forward. Each channel's existing
freeze-chain steps (HARV's seed-manifest → intake-screen → Stage-0
preregistration; dense-1m/TNEC's scoping-brief → `PREREG_G0`; MSL's
slate-card → G0-freeze; and the equivalent steps in the
no-counterparty-statistical/geometric and deep-iteration channels) are
replaced, at each existing freeze point, by an append to the single
contract — never a new file restating fields the contract already holds.
Later pipeline stages (reachability attestations, economic pre-gates,
exploration results, confirm verdicts, terminal dispositions) append their
own typed, hash-pinned entries to the same contract; they never copy its
founding fields elsewhere.

**K-ledger ruling.** `lab/discovery/register_search.py`'s
`discovery_manifests/*.json` ledger stays the sole machine-enforced source
of truth for K (§0) — this ADR does not replace it. The contract's own `K`
field is a **declaration that must match** the corresponding
`register_search.py` manifest's `K`, checked the same way a later ADR's
multiplicity-configuration field is contract-integrity-checked; the ledger
is not folded into the contract, and the contract is not a second K
authority.

**Field extension is by amendment, not by this ADR alone.** This ADR fixes
only the contract's existence, its baseline field list above, its
append-only/hash-pinned discipline, and the anti-laundering separate-freeze
-point structure. It does **not** enumerate every field a complete
generate/evaluate pipeline eventually needs — the mechanism-level
discriminator's adjudication rule, payoff-shape priors, the multiplicity
configuration (α/M/procedure), scoped account/book identifiers, or
per-candidate terminal-disposition axes. Each of those is its own decision,
added by a separate ADR that amends this one **in part** (per the
`Amends-in-part` pattern already precedented in
`docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md`'s
header, §0), naming exactly which field(s) it adds and at which freeze
point.

**Effective:** immediately upon acceptance, for any candidate whose
generation-open freeze occurs after this date.
**Scope:** candidate-level generation/admission doctrine across all five
live channels (HARV, dense-1m/TNEC, MSL, no-counterparty-statistical/
geometric, deep-iteration) and any future channel. Does **not** retroactively
rewrite any already-frozen candidate's existing manifest/prereg documents;
see §5.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Status quo — leave each channel's multi-document freeze chain as-is | No consistency check exists between a candidate's seed manifest and its later Stage-0 preregistration today; drift is possible and undetected. Proxy-only promotion (Route B, tension 4) already happened once under this status quo. |
| A single **repo-wide** template file replacing all per-lane specs | Channels differ in real, load-bearing ways (HARV's mechanism-first four-clause test vs. MSL's manual slate-card sourcing vs. deep-iteration's grammar-generation budget) — collapsing lane-specific gates into one universal document would either lose those gates or bloat the contract with fields most candidates never use. The contract holds the facts every candidate shares; each lane's own gates still run against it. |
| Fold the machine-enforced K ledger (`discovery_manifests/*.json`) into the contract itself | `register_search.py`'s ledger is already machine-checked, timestamped, and consumed by the downstream multiplicity correction (`discovery_manifests/README.md`, §0). Duplicating K into a second, human-authored surface reintroduces exactly the drift-risk this ADR exists to remove. The contract cites the ledger's `run_id`; it does not re-author K. |
| Enumerate every downstream field (discriminator rule, multiplicity config, disposition axes, etc.) inside this ADR | Each of those is a load-bearing decision belonging to the ADR that actually needs it (economic gates, evaluation order, terminal taxonomy) — folding them all in here would violate "ADRs document ONE decision" and make this ADR's own ratification hostage to unrelated design questions still in progress. |
| Retroactively migrate every already-open candidate's existing manifest/prereg documents into the new contract format | Real, non-regenerable work across an unknown number of open candidates, undertaken without first validating the contract format against a live channel. New candidates adopt it going forward (§2); existing ones are named as owed, not silently rewritten (§5). |

---

## §4 — Falsifier (revert trigger)

**H (hypothesis):** a single hash-pinned, append-only candidate contract
removes the cross-document drift risk and the proxy-only-promotion gap
without weakening the exploration/confirmation firewall Route B's checklist
protected.

**Revert trigger:** if, by the next scheduled quarterly programme audit
after the first candidate contract is opened under this ADR, either (a) a
confirm-stage entry is found to have been written with access to
information that should have been sealed at the founding freeze — i.e. the
append-only/hash-pinned structure failed to preserve the G0/C0
anti-laundering separation (§0) — or (b) two or more live channels report
that the fixed baseline field list (§2) is insufficient to express a
real candidate their prior per-lane documents could express, forcing an
informal side-document to reappear — this ADR is revoked.

**Revert action:** author a superseding ADR that either (a) tightens the
append-only mechanism's technical guarantee (e.g. requiring a
cryptographic commitment at the founding freeze, not just "append-only by
convention"), or (b) restores per-lane freedom to add lane-specific fields
via a formally-declared extension mechanism rather than reverting to
separate documents. Never silently edit this ADR's decision text.

**Trigger check schedule:** every quarterly programme audit (next:
2026-11-08).

---

## §5 — Forbidden moves (under this ADR)

- **Retroactively rewriting already-open candidates' existing manifest/
  prereg documents into contract form as part of this ADR's own
  implementation.** Tempting because it would make the migration look
  complete immediately — ruled out because it is real, potentially
  error-introducing work on live candidates undertaken before the format
  has been validated against a single real channel. Existing candidates
  keep their current documents; only newly-opened candidates use the
  contract (§2).
- **Silently editing each channel's owning artifact** (the HARV-lane ADR,
  the dense-1m/TNEC spec, the MSL charter, the no-counterparty-statistical
  channel ADR, the deep-iteration lane charter) **to redirect their freeze
  steps at the contract, inside this ADR's own Phase-2 sweep.**
  Amendment-first discipline requires each channel's own dated addendum —
  this ADR names the requirement; each channel's owning artifact adopts it
  on its own ratified addendum (tracked as an owed STATE.md row, §6),
  mirroring `2026-08-30-channel-liveness-gate.md`'s identical pattern for
  the same five channels.
- **Folding `discovery_manifests/*.json` into the contract**, or treating
  the contract's own `K` field as authoritative over the ledger. Ruled out
  in §2/§3 — the ledger stays the sole K authority; the contract's K field
  is a checked declaration, never a second source.
- **Enumerating downstream fields (discriminator rule, multiplicity
  config, disposition axes, shape priors) inside this ADR** to make the
  contract look "complete" on day one. Ruled out in §2/§3 — each is a
  separate decision, added by its own amending ADR.
- **Treating a contract's baseline-field completeness as sufficient for
  admission on its own.** A complete entry/exit object bans proxy-only
  promotion; it does not itself pass any lane's mechanism-quality bar
  (Requirement 1a, the no-counterparty channel's own evidentiary grade,
  etc.) — those gates are unaffected by this ADR and still apply on top.

---

## §6 — Consequences

**Positive consequences:**
- Removes the cross-document drift risk between a candidate's seed
  manifest/slate card and its later Stage-0/G0 preregistration — one
  object, one set of founding facts.
- Makes "delete proxy-only promotion" (§0) a hard, checkable admission
  gate rather than a review norm: a candidate without a complete entry/exit
  object cannot open a contract.
- Gives every later ADR in this formalization sequence (economic gates,
  evaluation order, terminal taxonomy, operator approvals) one well-defined
  object to amend-in-part, instead of each having to separately decide
  where its own fields live.
- Preserves the Route B/`avenue_a_generate_confirm.md` anti-laundering
  separation by construction (named freeze points, not one mutable file).

**Negative consequences (real cost, not theatrical):**
- Every live channel's owning artifact now carries an owed migration
  addendum (§5) before the contract actually replaces that channel's
  current freeze chain — until then, the channel's existing documents
  remain its live practice.
- A slightly higher authoring bar at generation-open: a candidate cannot
  be provisionally admitted on a proxy statistic alone, which may slow
  early-stage exploratory work that previously used a looser seed-manifest
  format.

**Risks (probabilistic, distinct from costs):**
- If the baseline field list (§2) proves genuinely insufficient for a real
  channel's needs before its formal amending ADR lands, that channel may
  informally reintroduce a side document to cover the gap — exactly the
  drift this ADR exists to prevent. §4's falsifier is designed to catch
  this at the next audit.

**Downstream artifacts that need updating:**
- `docs/adr/2026-07-15-external-mechanism-harvest-intake.md` /
  `docs/adr/2026-07-13-harv-discovery-lane-ratification.md` /
  `docs/methodology/strategy_harvest.md` §5–§6 — owed a dated addendum
  redirecting HARV's freeze-chain steps at the contract.
- `docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md` — owed the
  same, for dense-1m/TNEC.
- `docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md` /
  `docs/adr/2026-08-12-msl-sourcing-channel-ratification.md` — owed the
  same, for MSL.
- `docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` —
  owed the same.
- `docs/adr/2026-08-16-deep-iteration-lane-charter.md` — owed the same.
- `STATE.md` — new forward-board row: all five channels owed a dated
  candidate-contract migration addendum (may share the row already added
  by `2026-08-30-channel-liveness-gate.md` if convenient — same five
  channels, same owed-addendum shape).

---

## §7 — Implementation plan

- **Phase 0** — re-confirm §0 anchors current at apply-time.
- **Phase 1** — no direct edits to any per-lane owning artifact (§5
  forbids it inside this ADR); this ADR's own body is the complete Phase-1
  deliverable. A review pass on the drafted series caught two defects
  fixed before finalizing: the channel count was wrongly stated as six
  throughout (five, matching `2026-08-30-channel-liveness-gate.md`'s own
  derivation — GROW is tooling inside deep-iteration, not a sixth
  channel), and the contract's cardinality relative to
  `2026-08-30-evaluation-order.md`'s `M`-candidate confirm selection was
  unstated — both corrected in §0/§1/§2/§6/§10 above.
- **Phase 2** — grep-sweep, two limbs (Known Trap #7): **(i)** no
  predecessor to check (`Supersedes: none`); **(ii)** consumers of
  seed-manifest/G0/preregistration vocabulary — `grep -rl "seed manifest\|
  slate card\|Stage-0 preregistration\|PREREG_G0" docs/adr/ docs/spec/
  docs/methodology/`, run this session. Raw hit list beyond the seven
  channel-owning artifacts already named in §0/§1 (five channels; HARV and
  MSL each have two owning files): `2026-08-08-edge-
  cohort-correction-and-necessity-retarget.md`, `2026-08-10-temporal-
  selectivity-outside-mapped-levers.md`, `2026-08-13-msl-c3-k2-dual-axis-
  revive.md`, `2026-08-14-msl-explore-stage-5a.md`, `2026-08-16-con5-
  timeframe-scope-cheap-falsifier-gate.md`, `2026-08-20-analogue-modality-
  override-ict-ob-1-admit.md`, `2026-08-20-analogue-modality-override-ict-
  ote-1-admit.md`, `2026-08-20-dense1m-u1-operator-override-con4-reopen.md`,
  `2026-08-24-sourcing-phase-channel-retirement.md`. Disposition: every one
  of these is a **campaign-level** decision or override operating inside
  an already-named channel (dense-1m/TNEC or MSL), not a channel-owning
  artifact with its own freeze chain — none defines a new channel, and
  none is owed a separate migration addendum; each inherits its parent
  channel's addendum once written. No hit surfaced a sixth channel.
- **Phase 3** — add the STATE.md forward-board row (§6); verification
  block executes; status → `Accepted`.

Per-channel migration to the contract format is **each channel's own
future addendum**, not required for this ADR's acceptance — the same
policy-first, code/migration-may-lag shape as
`2026-08-30-channel-liveness-gate.md`.

---

## §10 — Audit hooks (runnable)

```bash
# Which channel owning artifacts still lack a candidate-contract migration addendum?
# Expected at ratification: all print (none has the addendum yet) -- five
# channels, seven owning files (HARV and MSL each have two).
grep -L "candidate-contract" \
  docs/adr/2026-07-15-external-mechanism-harvest-intake.md \
  docs/adr/2026-07-13-harv-discovery-lane-ratification.md \
  docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md \
  docs/spec/2026-08-12-msl-manual-sourcing-loop-charter.md \
  docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md \
  docs/adr/2026-08-16-deep-iteration-lane-charter.md

# Any new candidate document restating founding fields outside the contract,
# post-acceptance, on a channel that HAS migrated? (manual periodic check;
# no channel has migrated yet, so expect no matches pre-migration)
grep -rl "seed manifest\|slate card\|Stage-0 preregistration\|PREREG_G0" \
  lab/analysis/ lab/archive/ 2>/dev/null | tail -20

# K-ledger ruling still holds -- contract never becomes a second K authority
grep -rn "K_intrinsic\|K_eff" docs/adr/2026-08-30-candidate-contract.md
# Expected: only the K-ledger ruling paragraph and its citations, no
# competing K arithmetic

# Calendar trigger reminder
# Quarterly programme audit due: 2026-11-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python scripts/check_brief.py docs/adr/2026-08-30-candidate-contract.md --type adr

# ADR lifecycle graph
$ python scripts/check_adr_graph.py

# Production-source verification (Rule 0 confirmation)
$ git log -1 --format="%h %ci" -- docs/methodology/strategy_harvest.md
$ git log -1 --format="%h %ci" -- docs/adr/2026-07-15-external-mechanism-harvest-intake.md
$ git log -1 --format="%h %ci" -- lab/discovery/register_search.py

# Downstream artifact update verification (post-migration addenda)
$ grep -rln "candidate-contract" docs/adr/ docs/spec/
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-30 | Initial authoring | Joshua + Claude Code |
