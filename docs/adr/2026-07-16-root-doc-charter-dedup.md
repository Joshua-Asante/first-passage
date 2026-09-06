# ADR — Root-doc charter ratified; posture narrative demoted to pointers

**Status:** `Accepted`
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-16
**Authors:** Joshua + Claude Code
**Supersedes:** none (extends `docs/operational_rules.md` Rule 7 from *values* to *decision narrative*)
**Related:** Rule 7 origin incident (2026-06-03 STATE.md drift); [`2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) ("retire, but do not over-retire")
**Layer:** infrastructure (governance docs)

> **Current routing (2026-09-06):** the [dated amendment](#addendum-2026-09-06--current-work-routing-and-root-consolidation) owns the current root roles and executable audit commands. The five-file charter, protected CLAUDE sections, and semantic-loss falsifier remain in force; prior command lists are historical.

---

## §0 — Rule 0 reads (production-source verification)

All read in-session on 2026-07-16, before authoring (anchors = `git log -1 --format='%h %ci' -- <path>`):

- `README.md` — anchor `e6ec1ff` (2026-07-15). Public-clone note = 20 lines duplicating CLAUDE.md §Public-clone posture.
- `CLAUDE.md` — anchor `ae6eb27` (2026-07-15). §Live-execution posture = 4 dense paragraphs retelling the R6 / FXIFY / rescope / prop-reopen ADRs.
- `STATE.md` — anchor `e0724cb` (2026-07-15). Four dated `## 2026-07-1x` sections (~72 lines) re-summarizing Accepted ADRs, ahead of the dormant-threads + forward-board content its own header declares as its charter.
- `REPO_MAP.md` / `PIPELINES.md` — anchor `e6ec1ff` (2026-07-15). Static-vs-dynamic split confirmed clean; PIPELINES carries a one-paragraph dormancy preamble (kept — see §3).
- `docs/operational_rules.md` — anchor `83ba1b2` (2026-07-12). Rule 7 (one canonical owner per fact) + its 2026-06-03 origin incident.
- `scripts/validate_params.py` + `scripts/verify_lock_anchors.py` — anchor `f2be990` (2026-07-11). Confirmed the gated CLAUDE.md surface: the Strategy Reference table cells (risk% / contractValue / version) and every bolded `**N% pass / N% bust ...**, p99 DD N%` headline (+ trailing `median N` token). Both parsed regions live OUTSIDE the sections demoted here; the posture prose's bare `(99.83/0.17/4.37)` mention does not match the headline regex.
- `scripts/check_root_doc_liveness.py` — anchor `e6ec1ff` (2026-07-15). Dead-link gate over exactly these five docs; all links in the demoted replacements must resolve.

---

## §1 — Context

The five root docs have a sound division of labor (README = human entry index; CLAUDE.md = agent orientation + gated lock surface; REPO_MAP = static layer map; PIPELINES = dynamic data-flow map; STATE = open-threads + forward-obligation register), but three duplication classes have crept in:

1. **Live-execution posture told three times** — CLAUDE.md §Live-execution posture (multi-paragraph), STATE.md's dated 2026-07-10/11/12/15 decision blocks, and PIPELINES.md's dormancy preamble — all re-summarizing the same Accepted ADRs (R6 NO-GO, FXIFY closure, claims re-scope, prop-portfolio reopen).
2. **Public-clone posture told twice** — README's three-class note duplicates CLAUDE.md's fuller §Public-clone posture.
3. **STATE.md grown past its charter** — its header says "not a state snapshot," yet ~72 lines of dated ADR re-summaries sat above the register content. This is the exact failure class Rule 7 was written for: on 2026-06-03, STATE.md silently drifted three weeks stale restating the strategy table and MC anchor. Narrative restatements drift the same way values do.

**Decision driver (one sentence):** the operator reviewed the five-doc split on 2026-07-16, ratified the file roles, and directed the three duplication classes be removed permanently rather than re-trimmed session by session.

---

## §2 — Decision

**Decision:** Ratify the five-root-doc charter and extend Rule 7 from canonical *values* to canonical *decision narrative*: the owning ADR is the sole home of a decision's retelling; root docs carry at most **one pointer line + one-line consequence** per standing decision.

Concretely (all executed with this ADR):

- **CLAUDE.md §Live-execution posture** → demoted to a pointer block: a short current-scale-path paragraph + one bullet per standing decision (bolded consequence + ADR link). The gated lock surface (Strategy Reference table, MC-anchor headlines, §Protection) is untouched.
- **STATE.md dated decision sections** → demoted to a compact "Executed operator decisions — pointer log" (one line per decision, newest first). Dormant threads, the discovery-campaign register, and the forward-trigger board stay. The harvest-intake §4 falsifier + idle guard move onto the forward board where they belong.
- **README.md §Public-clone note** → one sentence + link to CLAUDE.md §Public-clone posture.
- **`docs/operational_rules.md` Rule 7** → role list gains CLAUDE.md-§posture and README rows; dated edit-log entry added.

**Effective:** immediately.
**Scope:** the five root orientation docs (`README.md`, `CLAUDE.md`, `REPO_MAP.md`, `PIPELINES.md`, `STATE.md`). Future posture decisions add one pointer line to CLAUDE.md §posture and one to STATE.md's pointer log — never a retelling.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Merge CLAUDE.md into README (one entry doc) | Different consumers: README is the human index; CLAUDE.md is the agent-loaded orientation + machine-gated lock surface (`validate_params` / `verify_lock_anchors` parse it). Merging couples human prose churn to a parsed surface. |
| Collapse STATE.md into `docs/SESSIONS.md` | SESSIONS is an append-only per-session narrative; STATE is the mutable cross-session board (dormant threads + dated obligations) that no single session entry carries. Distinct jobs. |
| Also strip PIPELINES.md's dormancy preamble | Operator-scoped leave-alone; the one-paragraph dormancy read is load-bearing for its status column (a pipeline map that ignored dormancy would document machinery that isn't turning). It is a labeled framing paragraph, not a per-decision retelling. |
| Delete the historical posture facts outright | Over-retire — violates the 2026-07-11 rescope directive ("retire, but do not over-retire"). Demotion keeps every fact reachable one hop away in its ADR. |
| Status quo (re-trim ad hoc) | The 2026-06-03 incident shows restatements drift silently; without an ownership rule the retellings regrow with each new decision. |

---

## §4 — Falsifier (revert trigger)

**H:** one pointer line + one-line consequence per standing decision is sufficient orientation for the root docs — no future decision error will be attributable to the demotion (the fact was one ADR-hop away and the pointer named the consequence).

**Revert trigger (H falsified if):** a dated incident occurs in which a decision (operator, agent, or Cursor session) goes materially wrong **because** a fact removed from a demoted block was needed at orientation time and the one-hop ADR link did not surface it (i.e., the defect log of a session or a Rule 6 skew audit attributes the error to the demotion, not to a stale ADR).

**Revert action:** restore the specific inline block class that was needed (posture paragraph, STATE dated section, or README note) by superseding addendum on this ADR — not a silent regrow.

**Trigger check schedule:** rides the quarterly review dates (next 2026-08-08): confirm zero demotion-attributed defects, and spot-check that the pointer blocks have not regrown into retellings (§10 hooks).

---

## §5 — Forbidden moves (under this ADR)

- **Editing the gated lock surface while trimming CLAUDE.md** — the posture prose sits directly above the Strategy Reference table and repeats the anchor triple informally; it is tempting to "normalize" the parsed headline copies or the table while in the file. Ruled out: `verify_lock_anchors.py` treats every bolded headline as a pinned copy, and `validate_params.py` pins the table cells. Any anchor-block change requires its own re-MC governance, never a doc-cleanup ride-along.
- **Adding "just this once" narrative for the next big decision** — the next R6-scale decision will feel too important for one line. Ruled out: that is exactly how the current triple-telling accreted (07-10 → 07-11 → 07-12 → 07-15, each one paragraph at a time). The ADR carries the weight; the pointer carries the consequence.
- **Extending the demotion to REPO_MAP / PIPELINES** — tempting for symmetry (PIPELINES restates dormancy). Operator-scoped out; see §3.
- **Deleting STATE's one-liner facts that have no other committed home** (the 2026-07-10 operator retirements bullet, the local `accounts.json` migration note) — tempting as "not forward-board material." Ruled out: they are recorded one-line facts whose canonical homes are weak or local-only; dropping them is over-retirement.

---

## §6 — Consequences

**Positive:**
- One narrative owner per decision (the ADR); the drift surface shrinks from three tellings to one telling + pointers.
- CLAUDE.md orientation cost drops (~40 dense lines → ~15 pointer lines) without losing the load-bearing operational facts (`ACTIVE_FIRM` pin, 08-08-is-a-checkpoint, gated-rail status).
- STATE.md returns to its charter; its register content is findable again.

**Negative (real cost):**
- Detail is one hop away: an agent that reads only CLAUDE.md loses the inline nuance (e.g., the −$4,188.85 discretionary-tilt episode, P2 gate mechanics). Mitigation: each pointer names its consequence, and the ADR links are adjacent.
- One-line consequences are lossy compressions authored once; a badly compressed line could mislead until the ADR is opened. A dated incident of this class fires §4 and the demotion is FALSIFIED for that block class (restore by addendum); absent any such incident through two quarterly reviews, treat the charter as RESOLVED-stable.

**Risks:**
- A future session "helpfully" re-expands the pointers (the reverse failure). Mitigation: Rule 7 role rows + §10 size hooks make the regrowth mechanically visible.

**Downstream artifacts updated with this ADR:**
- `CLAUDE.md` (§Live-execution posture demoted), `STATE.md` (pointer log + forward-board harvest line), `README.md` (public-clone one-liner), `docs/operational_rules.md` (Rule 7 rows + edit log), `docs/SESSIONS.md` (session entry).

---

## §7 — Implementation plan

Executed in the same PR as this ADR (single-commit-family change):

- **Phase 0** — §0 reads (done; anchors above). Confirm `verify_lock_anchors.py --quiet` routes `Closed` pre-edit.
- **Phase 1** — the four doc edits per §2.
- **Phase 2** — grep-sweep: no remaining multi-paragraph posture retelling outside ADRs; all links in edited docs resolve (`check_root_doc_liveness.py`).
- **Phase 3** — verification block below passes; ADR lands `Accepted` (operator direction to execute was given in-session 2026-07-16).

---

## §10 — Audit hooks (runnable)

```bash
# 1. Gated surfaces still intact after any root-doc edit
python scripts/verify_lock_anchors.py --quiet     # expect: ROUTING: Closed (exit 0)
python scripts/validate_params.py                 # expect: exit 0
python scripts/check_root_doc_liveness.py         # expect: exit 0

# 2. Posture block has not regrown into a retelling (pointer block ≈ 15 lines)
awk '/^## Live-execution posture/,/^## Architecture/' CLAUDE.md | wc -l   # expect: <= 25

# 3. STATE.md carries no dated decision sections (pointer log only)
grep -cE '^## 2026-' STATE.md                     # expect: 0

# 4. README public-clone note stays a one-liner + link
awk '/^## Public-clone note/,0' README.md | wc -l # expect: <= 8

# 5. Rule 7 role rows present
grep -n 'Live-execution posture' docs/operational_rules.md   # expect: >= 1 hit
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-16-root-doc-charter-dedup.md --type adr
# §0 anchors re-checkable:
git log -1 --format='%h' -- CLAUDE.md STATE.md README.md docs/operational_rules.md
# Downstream sweep = §10 hooks 1–5 above.
```

---

## Addendum 2026-09-04 — Consolidation pass: what moved, and what was ruled immovable

**Status:** `Accepted` (operator-directed in-session). **Does not amend** §2's charter, §4's
falsifier, or §5's forbidden moves — it records one execution of the charter and narrows the
factual scope of the *first* forbidden move, which had gone stale.

**What moved out of `CLAUDE.md`:**

| Block | New owner | Why it is not a root-doc fact |
|---|---|---|
| §Load-bearing numbers (2 standing rules + 6-row live-value table, added 2026-09-03) | [`docs/load_bearing_numbers.md`](../load_bearing_numbers.md) | An index that restates six figures from six owners. Root docs carry pointers; the index is one hop away and named in Rule 7's owner table |
| §Strategy Reference *table* (risk% / pyramid / version / `contractValue`) | [`core/strategies/CATALOG.md`](../../core/strategies/CATALOG.md) §Locked parameter record | A human-readable mirror of Pine + `historical_challenge.HISTORICAL_CHALLENGE_BASE_RISK`, sitting beside the CARD stubs and dispositions it describes |
| §Vendor-data integrity gate command blocks | this repo's [manifest integrity ADR](2026-05-10-manifest-integrity-gate.md) §Decision (already held them) | Verbatim duplicate of the ADR's own decision items 1–2 |

Every affected heading was **kept as a stub**, because 15 files cite `CLAUDE.md §Strategy Reference`
and three hookify rules plus `scripts/install_hooks.sh` cite `§Vendor-data integrity gate` by name —
several of them frozen bodies (`docs/adr/TOMBSTONES.md`, `docs/ltm/`, the 2026-04-17 allocations ADR)
that Trap #12 bars editing. A stub keeps the hop alive; deleting the heading would have broken it.

**What was ruled immovable, and the §5 correction that ruling rests on.** §5's first forbidden move
("editing the gated lock surface while trimming CLAUDE.md") justified itself by naming two parsers:
`validate_params.py` and `verify_lock_anchors.py`. Both claims are now stale, verified in-session
2026-09-04:

* `scripts/validate_params.py` **no longer exists** — deleted with the
  [`params.toml` gate retirement](2026-08-03-params-toml-gate-retirement.md).
* `scripts/verify_lock_anchors.py` **no longer reads `CLAUDE.md`** — its `read_text` calls are
  `dd_protection.py`, `historical_challenge.py`, `firm_rules.py` only.

The live machine-reader is instead `ops/recall/guard.py`, which regex-reads the MC-anchor triple
(`99.83% pass / 0.17% bust`, `p99 DD 4.37%`) out of `CLAUDE.md` to build the recall-sidecar denylist.
**That block stays in `CLAUDE.md`**, and the tempting re-point was measured and rejected: the first
anchor-shaped match in `docs/mc_anchor_history.md` is `99.84 / 0.16 / 4.55` — the Q-SWAP-1 swap-aware
figures, not the canonical triple — so re-pointing the parser at that file would have silently
denylisted the **wrong three numbers** while every gate stayed green. Moving a safety guard's source
of truth is its own decision with its own verification, never a doc-cleanup ride-along; §5's
underlying instruction is upheld even though its cited evidence had rotted.

**§10 hook 2 measurement** (`awk '/^## Live-execution posture/,/^## Architecture/' CLAUDE.md | wc -l`,
expected ≤ 25): **88 → 41 lines**. Still over the hook's ceiling; the operator call recorded on
`STATE.md`'s size-hook row (accept as a bounded safety-content exception, or trim further) remains
open and is **not** discharged by this addendum. What remains above the ceiling is the Safety
invariants block, the account-state paragraph, and the 12-row standing-decisions table this ADR's own
§2 sanctions.

**Also landed with this pass:** a `## Continuous improvement` section (operator-supplied text) giving
the escalation order test → hook → skill → `CLAUDE.md` → ADR/lesson, with a line mapping each layer
to its home in this repo.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Initial authoring + same-session execution | Joshua + Claude Code |
| 2026-09-04 | Addendum: consolidation pass; §5 forbidden-move evidence corrected; anchor block ruled immovable | Joshua + Claude Code |

---

## Addendum 2026-09-06 — Current-work routing and root consolidation

**Status:** `Accepted` — the operator approved the root-document review and directed
"create a task list to completion and execute it" on 2026-09-06. This is the
implementation of that instruction, including the proposed ownership/reader amendment.

**Grounding before edits:** baseline `7185ccf` contains all five root files,
`docs/operational_rules.md` Rule 7, `scripts/check_sessions_queue_bind.py`,
`scripts/check_state_currency.py`, `scripts/check_repo_map_scripts_table.py`,
`ops/recall/guard.py`, and the current Select plan/record. They were read directly;
`core/dd_protection.py` and `core/firm_rules.py` were also read before describing
the preserved risk-control boundary. The original reader compared live queue
IDs to the latest historical session entry. README described P4 as idle while
PIPELINES called it active; PIPELINES still blocked M1 on a selected strategy
despite the 2026-08-24 license. The five root files totaled 14,206 words.

**Decision and scope:**

1. Retain the five files. README is human routing; CLAUDE is agent constraints and
   essential safeguards; PIPELINES is workflow/handoffs; STATE owns priorities
   and obligation pointers; REPO_MAP is present architecture and module entry points.
2. Campaign implementation plans own executable next steps. Campaign records
   own evidence, gate dispositions and operator decisions. SESSIONS owns history.
   Its living header points to STATE; a session's optional Open / next is historical
   context. A queue change does not require editing an old entry or adding a stub.
   This explicitly replaces the queue-copy requirement of the W5 and Survive-bound
   2026-08-23 addenda, recorded on those owners in the same change.
3. Preserve numbered STATE rows and the decision-index/date/recurrence fields
   consumed by the remaining readers. Keep its executed-decision index compact.
   The root-layer script table remains generated in REPO_MAP, with its existing
   generator interface. No sixth root document, new state store, or word-count gate.
4. Correct M1 item 5 / B7 Stage 1 to its licensed independent test-strategy route.
   Winner-specific parity and the M1 RESOLVED plus operator-GO arm gate remain separate.
   No execution authority or risk-control change follows from this doc revision.
5. Retain CLAUDE's entire Strategy Reference and Protection sections and the
   operator-supplied Continuous improvement section. The recall guard's exact
   historical MC source remains at the same file and the old heading stubs remain.

**Alternatives:** retaining live queue copies in append-only session entries
requires repetitive stubs and leaves a competing current-work surface; rejected.
Deleting STATE's decision index or moving the generated script table would require
unnecessary reader migration; both remain. A monolithic root guide combines
different readers and cadences; the existing five-file division remains preferable.

**Tradeoff:** readers use the queue and current campaign plan for continuation
instead of treating the latest session entry as a work order. Historical detail is
one owner-hop away. Essential safety remains inline; the existing §4 falsifier
and role-specific restoration action continue to cover loss caused by demotion.
Its next quarterly check is 2026-11-08; no new review cadence is introduced.

**Completed-row disposition:** the discharged 2026-08-08 audit remains in
`docs/notes/audits/programme-audit/2026-08-08-quarterly-audit.md`; Guardian-MGC's
terminal transfer record remains in `docs/pursuits/b8-guardian-mgc-transfer-lane.md`;
the spent 2027-02-08 mechanism-2B cross-reference is represented by the still-live
channel-retirement limb-3 row. No open obligation is retired by those removals.
Monitoring obligations and channel-reconciliation debts retain individual wake
conditions or their owning debt lists.

**Posture-size obligation discharged:** the rewritten Live-execution posture is
21 lines, or 22 with the following Architecture heading included as §10's awk
command does. It satisfies the existing ≤25-line hook; no exception or new ceiling
is adopted. The corresponding STATE size-exception row is removed. The protected
sections sit outside this trimmed block and are unchanged.

**Reader amendment:** `scripts/check_sessions_queue_bind.py` retains its filename,
gate id and CLI. It checks the living header's relative Markdown route to STATE
and the existence of its OPERATOR QUEUE section, not historical queue numbers.
Regression cases cover queue changes without journal churn, optional Open / next,
misdirected/missing links, links only in history, and malformed/missing inputs.
The gate trigger includes both consumed files and the checker. Existing session
entries retain the append-only protection.

**Current audit commands** (replace this ADR's obsolete §10 command recipe, not
its semantic-loss falsifier):

```text
python scripts/check_root_doc_liveness.py
python scripts/check_state_currency.py
python scripts/check_sessions_queue_bind.py
python scripts/check_repo_map_layers.py
python scripts/check_repo_map_scripts_table.py --check
python scripts/verify_lock_anchors.py --quiet
python scripts/check_lifecycle_consistency.py
python scripts/roll_sessions.py --check-order
python scripts/roll_sessions.py --check-append-only
python -m pytest tests/test_sessions_queue_bind.py tests/test_state_currency.py tests/test_repo_map_layers.py tests/test_repo_map_scripts_table.py tests/ops/test_recall_guard.py -q
```

The old `validate_params.py` command is retired and must not be resurrected.
Link/date checks alone do not validate semantic agreement: review the current
Select-plan route, independent M1 route, protected blocks and retained obligations.
Execution checklist and verification evidence:
[implementation plan](../superpowers/plans/2026-09-06-root-docs-current-workflow.md).
