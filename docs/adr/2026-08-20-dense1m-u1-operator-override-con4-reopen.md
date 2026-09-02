# Operator override — mark U1 on the dense-1m OHLCV pause, reopen `Q-TNEC-CON-4` CONFIRM only — `dense1m-u1-operator-override-con4-reopen`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-20, in-session
direct instruction ("ratify the ADR"); see Ratification note
**Decision date:** 2026-08-20
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`Q-TNEC-CON-4` closure](../briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md)
(`AMBIGUOUS-HOLD`, the construct this ADR authorizes CONFIRM-scoring on) ·
[`Q-TNEC-CON-5` closure](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
(`AMBIGUOUS-HOLD` → operator Branch A STOP — the closure that imposed the pause
this ADR carves one exception into) ·
[`DENSE1M-UNPAUSE` closure](../briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md)
(`RESOLVED`, U0 KEEP — the dedicated review that kept the pause five days
later) · [dense-1m lane spec](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
(the lane this pause and this exception both live inside) ·
[ceremony-tiering ADR](2026-08-08-adr-ceremony-tiering.md) (`Accepted` — this
ADR's own tier justification, and the source of the "full limb-4 ADR"
requirement the pause's own closures already named)

---

**Tier:** full. Limb 4 (creates or amends doctrine — a rule, gate, or
convention that binds future work) fires unambiguously: this amends a
standing pause and `Q-TNEC-CON-4`'s own re-proposal bar. Not a close call —
the pause's own governing closure states directly that reversing it "still
needs a **full limb-4 ADR**" ([`DENSE1M-UNPAUSE` closure](../briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md)
§Iterate, stop-rule line). Limb 1 (K/money) does not fire — this authorizes
reading an already-collected, already-priced panel at $0, no new K.

---

## §0 — Rule 0 reads (2026-08-20)

- [`Q-TNEC-CON-4` closure](../briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md)
  — anchor `027a729` 2026-08-14. Read in full. **Load-bearing facts:** verdict
  `AMBIGUOUS-HOLD` (both arms' CIs straddle 0; long mean −0.0066R, short mean
  +0.0053R; gross ≈ +1.50 pt vs a 5.640 pt / 4×RT bar, i.e. **0.27×** — flat,
  not a near-miss); CONFIRM (2025-09-01→2026-08-05) **reserved and unread**;
  operator elected Branch B (lane continue) over the closure's own
  recommended Branch A (STOP) on 2026-08-11; this construct's own re-proposal
  bar is *"new mechanism evidence or a materially different cost geometry —
  not PDH/PDL / first→N / stop-geometry edits."*
- [`Q-TNEC-CON-5` closure](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
  — anchor `027a729` 2026-08-14. Read in full. **Load-bearing fact:** the
  Branch-B continuation from CON-4 itself produced a second `AMBIGUOUS-HOLD`
  (both arms mean-negative), and the operator then elected Branch A — STOP —
  citing **8 consecutive zero-yield closes** since 2026-08-08 across the
  short-horizon MNQ microstructure thread (Q-R2VBUCK-1, Q-R2FLOW-1,
  Q-R2AGRUN-1, Q-MNQDTL-CON-1, Q-TNEC-CON-2/3/4/5) against the Q-SCORE-1
  Block-1 tail-exhaustion anchor. This is the closure that actually imposed
  the "dense-1m OHLCV temporal-selectivity lane default **paused**" text.
- [`DENSE1M-UNPAUSE` closure](../briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md)
  — anchor `2e9944a` 2026-08-15. Read in full. **Load-bearing fact:** a
  dedicated review offered the operator U1 (admit one exception) or U2
  (default-open); operator marked **U0 — "Leave the pause"**, five days after
  imposing it. Its own §3 explicitly does NOT license "Re-opening CON-1–5
  CONFIRM," and its own stop-rule/re-proposal bar states the reopening path
  is *"a later Board mark of U1 or U2 (each still needs a full limb-4 ADR)
  or a new modality / non-route-① thesis — not a θ-retune, first/session-only
  cap, or stop-width rescue."* **This ADR is that full limb-4 ADR**, marking
  **U1**, not U2.
- [`docs/briefs/programs/2026-08-15-dense1m-lane-unpause-review.md`](../briefs/programs/2026-08-15-dense1m-lane-unpause-review.md)
  — anchor `2e9944a` 2026-08-15. The frozen packet the U0 mark above was made
  against; §6 route table confirms U1/U2 were live, named options at that
  review, not foreclosed ones.
- [dense-1m entry-mechanism lane spec](../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
  — anchor `73a77f7` 2026-08-16.
- [`Q-TNEC-CON-4` scoping brief](../briefs/Q-TNEC-CON-4-pdh-pdl-breakout-scoping.md)
  — anchor `027a729` 2026-08-14.
- [`lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md)
  frozen `57dc638`. **Load-bearing fact:** the CONFIRM/EXPLORATION split and
  gate (`SHAPE-CLEAR` / `FALSIFIED` / `VOID` as specified at explore GO) are
  already frozen on this file — this ADR authorizes *reading* CONFIRM against
  that already-frozen gate, it does not author a new one. The runner
  (`run_construct_g0.py`) already refuses to score a real-panel path without
  an explicit GO artifact (`EXPLORE_GO.md` was that artifact for EXPLORATION);
  Phase 3 below must locate/author the CONFIRM-side equivalent at execution
  time, not invent new gate criteria here.
- [ceremony-tiering ADR](2026-08-08-adr-ceremony-tiering.md) — anchor
  `91e6caa` 2026-08-15. Tier test applied above.

**Amendment-first / dedup (Rule 8 sub-rule 10):**

```
$ python scripts/check_advisor_dedup.py --keywords "dense-1m OHLCV pause unpause CON-4 PDH PDL breakout continuation operator override"
  slugs found:    ['CON-4']
  keywords found: 8 significant terms
  top hits: MECHANISMS.md, MNQ.md, Q-TNEC-CON-4/-5 closures, CON-3 closure,
  SESSIONS.md, Q-TRAINKILL-1/-3 closures — all prior art on the *paused*
  state, none on an override/reopening ADR.
```

**Judgment:** no prior owner exists for the override decision itself. The
three closures above are the existing owners of the *pause* — they gain
addenda (§7 Phase 1), not rewrites. Nothing here is re-derived.

---

## §1 — Context

The dense-1m OHLCV temporal-selectivity lane was paused by direct operator
election — [`Q-TNEC-CON-5` Branch A](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md),
2026-08-12 — after eight consecutive zero-yield closes across the
short-horizon MNQ microstructure thread. Five days later a dedicated review
([`DENSE1M-UNPAUSE`](../briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md))
asked the operator directly whether to lift it, in either of two named forms
(U1 admit-one, U2 default-open), and the operator kept it (U0). Inside that
paused lane sits `Q-TNEC-CON-4` — PDH/PDL RTH with-break — closed
`AMBIGUOUS-HOLD`, flat at 0.27× the cost bar on EXPLORATION, with its
CONFIRM window (2025-09-01→2026-08-05) still sitting unread.

On 2026-08-20, in-session, the operator instructed a direct reopening of
`Q-TNEC-CON-4` and an unpause of the dense-1m lane, explicitly **without**
new mechanism evidence, a new cost-geometry argument, or a new (non-OHLCV)
modality — the three routes the governing closures left open. This is a
legitimate exercise of standing operator authority (`inqhiori-canon.md`'s
D-user-gate; GRAND ADR §D5, "Joshua decides, always" — the same authority
class, one tier down from GRAND itself) to reverse his own prior decision.
It is not an evidentiary reversal, and this ADR does not pretend otherwise.

**Decision driver (one sentence):** operator direct in-session instruction,
2026-08-20, to reopen `Q-TNEC-CON-4` and unpause the lane, on authority alone.

---

## §2 — Decision

**Decision:** Mark **U1 (ADMIT-ONE)** on the dense-1m OHLCV temporal-selectivity
lane pause — a single, named exception scoped to `Q-TNEC-CON-4` only. Within
that exception, license exactly one action: **score the already-reserved
CONFIRM window (2025-09-01→2026-08-05) on `Q-TNEC-CON-4`'s already-frozen G0**
(`lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/PREREG_G0.md`, frozen
`57dc638`), against the verdict gate that file already froze at explore GO —
no new gate is authored here. No edit to any frozen CON-4 constant. No new
G0. No new K charge (same `K_intrinsic=1` already disclosed at EXPLORE).

**U2 is explicitly not marked.** `Q-TNEC-CON-1/2/3/5` and any future
`CON-6+` remain paused under the original U0 terms — this decision does not
reopen the lane default, only this one cell.

**Effective:** immediately upon acceptance.
**Scope:** `Q-TNEC-CON-4` CONFIRM-window scoring only. Nothing else in the
dense-1m lane, and no downstream Cap/deploy/Pine/arming decision (those stay
separate operator decisions per the construct's own closure, unchanged by
this ADR).

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Mark **U2** (default-open the whole lane) | Broader than the operator's stated ask; would silently reopen `CON-6+` and every other paused cell without addressing the 8-consecutive-null tail-exhaustion evidence that drove the pause. Scope creep beyond the instruction actually given. |
| Author a fresh, materially different G0 ("CON-4b") | This is what CON-4's own re-proposal bar actually asks for (new mechanism evidence) — the evidentiary path the operator explicitly declined this session. Available later as its own ADR-free pre-registration if the operator wants it; not what was instructed. |
| Wait for a genuinely new modality (order-flow/microstructure) | This is the pause's own stated preferred reopening route. Operator explicitly chose override instead of waiting for this. Available later. |
| Status quo — leave U0 in force | Does not execute the operator's direct instruction this session. |

---

## §4 — Falsifier (revert trigger)

This ADR is itself an evidence-free override, so its "falsifier" is a
one-shot spend condition rather than a monitoring trigger:

**Revert trigger:** `Q-TNEC-CON-4`'s CONFIRM-window score, once run, returns
`FALSIFIED` or `AMBIGUOUS-HOLD` under the gate already frozen in `PREREG_G0.md`
(matching or worse than the EXPLORATION read).

**Revert action:** the U1 exception is spent — file an addendum on
`Q-TNEC-CON-4`'s closure recording the CONFIRM score, and the cell reverts to
U0 (paused) with no further exception auto-granted. This becomes the ninth
consecutive zero-yield close in the short-horizon MNQ microstructure thread
(now on out-of-sample data), which *strengthens* rather than weakens the
original pause rationale. A second attempt at `CON-4` or any other paused
cell requires its own fresh ADR — this override does not create a standing
license to keep trying.

**If CONFIRM instead clears** (a live pass under the frozen gate): this ADR
grants no further authority — Cap claim, Pine, deploy, and arming remain
separate, later operator decisions, exactly as `Q-TNEC-CON-4`'s own closure
already restricts (§5 below).

**Trigger check schedule:** on the CONFIRM run itself (one-shot, not
calendar) — see §7 Phase 3.

---

## §5 — Forbidden moves (under this ADR)

- **Reading this override as marking U2.** It marks U1, scoped to `Q-TNEC-CON-4`
  only. `CON-1/2/3/5` and any future `CON-6+` stay paused under U0 — silently
  treating this ADR as a general lane reopening is exactly the scope-creep §3
  rules out.
- **Editing `Q-TNEC-CON-4`'s frozen G0 constants** (PDH/PDL definition,
  first→N, stop geometry) before or after reading CONFIRM. The entire point
  of this exception is to score the *already-frozen* construct; any edit
  voids the freeze and requires a brand-new G0 and its own K charge
  (`strategy_harvest.md`'s post-admission-widening rule — a conditioning or
  parameter change after freeze "voids the screen result... fresh manifest,
  fresh screen").
- **Treating a CONFIRM live-pass as an automatic Cap claim, deploy, Pine
  authorship, or rail arming.** `Q-TNEC-CON-4`'s own closure already
  restricts this ("What this closure does NOT license"); this ADR does not
  loosen it.
- **Using this override as precedent to reopen `CON-1`, `CON-2`, `CON-3`, or
  `CON-5`, or to author `CON-6`, without each getting its own ADR.** This
  override is a single named exception, not a doctrine change to the pause
  mechanism itself.
- **Reading "no new evidence required" as a standing exception mechanism**
  for other paused/closed constructs elsewhere in the repo (e.g. the PDH/PDL
  failed-break-reclaim family, or `Q-ICTEXP-1`). Each override is its own
  dated, ADR-recorded operator instruction — this ADR authorizes nothing
  beyond `Q-TNEC-CON-4`.

---

## §6 — Consequences

**Positive consequences:**
- Executes the operator's direct instruction.
- Bounded to an already-collected, already-priced panel — $0, no new K,
  no new manifest.

**Negative consequences (real cost, not theatrical):**
- Spends the CONFIRM window's status as a virgin out-of-sample check for this
  G0 — once read, it can never again be a clean holdout for `CON-4`, win or
  lose.
- Does not address the tail-exhaustion diagnosis (`Q-SCORE-1` Block-1, 8
  consecutive zero-yield closes) that justified the pause; if CONFIRM is also
  null, no new information is gained at the cost of the read itself.

**Risks (probabilistic, distinct from costs):**
- A marginal/ambiguous CONFIRM read has no clean fallback — no further OOS
  data exists in the reserved window for this G0, so the exception is
  genuinely one-shot with no do-over.
- Precedent risk: an operator override with no evidentiary bar is easy to
  cite loosely later ("we did it for CON-4"). §5's explicit scope-limits and
  §4's "no further exception auto-granted" language exist specifically to
  block that reading.

**Downstream artifacts that need updating:**
- `docs/briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md` — addendum
  recording the U1 exception and CONFIRM authorization; historical body
  unchanged.
- `docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md` — addendum
  noting a bounded exception now exists inside its pause; the pause itself
  stands unchanged for everything else.
- `docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md` —
  addendum noting U1 is now marked (scoped to `CON-4` only); its own §3
  "does NOT license" list stays historically accurate as "as of 2026-08-15,"
  not rewritten.
- `STATE.md` / `docs/SESSIONS.md` — forward-board line if either currently
  restates the pause as unconditional for `CON-4` specifically (Phase 2
  sweep below).

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified current this session (done, above).
- **Phase 1** — file addenda on the three closures named in §6's downstream
  list. Addenda only — no rewrite of ratified closure text.
- **Phase 2** — grep-sweep, two limbs (Known Trap #7):
  (i) stale restatements of "CONFIRM ... unread forever" specific to `CON-4`
  across `STATE.md`, `docs/briefs/INDEX.md`, `lab/CATALOG.md`,
  `docs/SESSIONS.md` — update any `CON-4`-specific pointer only;
  (ii) confirm no hit references `CON-1/2/3/5` in a way this ADR would
  incorrectly appear to touch — those stay paused and unedited.
- **Phase 3** — the actual CONFIRM-scoring run is a **separate, later
  action** this ADR authorizes but does not execute. At execution time:
  locate or author the CONFIRM-side equivalent of `EXPLORE_GO.md` (the
  runner already refuses real-panel scoring without an explicit GO artifact
  per `PREREG_G0.md` step 3-4), run against the frozen gate, file the result
  as a `Q-TNEC-CON-4` closure addendum per §4.
- **Phase 4** — verification block below executes; status moves to
  `Accepted` only after the explicit ratification named in the header.

---

## §10 — Audit hooks (runnable)

```bash
# The pause text must still exist verbatim for the general lane (U1 does not erase U0's text):
grep -n "dense-1m OHLCV temporal-selectivity lane default \*\*paused\*\*" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
# Expected: 1 hit — pause stands for CON-1/2/3/5 and any future CON

# This ADR's U1 mark must be cross-referenced from DENSE1M-UNPAUSE's addendum once Phase 1 lands:
grep -n "U1" docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md
# Expected: addendum hit pointing at this ADR's slug, post-Phase-1

# CON-1/2/3/5 must remain untouched by this ADR's own commits:
git log --format='%h' -- docs/briefs/closures/Q-TNEC-CON-1-closure* docs/briefs/closures/Q-TNEC-CON-2-closure* docs/briefs/closures/Q-TNEC-CON-3-closure* | head -1
# Expected: no commit from this ADR's authoring session appears here

# Freeze-ordering: CONFIRM scoring (once run) must postdate this ADR's acceptance commit
git log --format='%h %cs' -- docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md | tail -1
git log --format='%h %cs' -- lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/ | tail -1
```

---

## Ratification note

**Drafting authorized by:** Joshua, in-session direct instruction — an
explicit operator override, no new evidence, choosing to reverse the
2026-08-12 (`Q-TNEC-CON-5`) and 2026-08-15 (`DENSE1M-UNPAUSE`, U0 KEEP)
decisions on authority alone (2026-08-20).

**Ratified by:** Joshua, in-session direct instruction — *"ratify the ADR"*
(2026-08-20), distinct from the earlier general override instruction that
only authorized drafting. Authority channel: explicit owner adjudication.

**Preconditions at ratification:** `python scripts/check_brief.py
docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md --type adr` →
`RESULT: well-formed` (0 HARD, 1 WARN — §6 lacks a binary verdict keyword;
expected, §6 here is Consequences, not a gate — the actual binary gate is §4)
✓ · `python scripts/check_adr_graph.py` → `OK` ✓.

**ACCEPTED same-commit downstream updates:** `docs/adr/INDEX.md` regenerated
via `check_adr_graph.py --regenerate-index` · §7 Phase 1 addenda filed on the
three named closures · §7 Phase 2 grep-sweep executed (see this ADR's
Change history for results). §7 Phase 3 (the actual CONFIRM-scoring run) is
**not** part of this ratification — it is a separate, later execution step
this ADR authorizes but does not itself perform.

**Not licensed by this ratification:** anything §5's forbidden moves already
exclude — this ratifies the *U1 exception and CONFIRM-read authorization*
for `Q-TNEC-CON-4` only. It does not itself run CONFIRM, does not mark U2,
and does not reopen `CON-1/2/3/5`.

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md --type adr
python scripts/check_adr_graph.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Initial authoring — drafts the U1 exception for `Q-TNEC-CON-4` per operator's in-session override instruction. `Proposed`, not yet ratified. | Claude Code (drafted at operator request) |
| 2026-08-20 | Ratified `Proposed` → `Accepted` (operator in-session instruction, "ratify the ADR"). §7 Phase 1/2 executed same commit: Change-history addenda filed on the `Q-TNEC-CON-4`, `Q-TNEC-CON-5`, and `DENSE1M-UNPAUSE` closures; `docs/briefs/INDEX.md` CON-4 row and `lab/CATALOG.md` CON-4 row updated to note the U1 exception; `docs/SESSIONS.md` entry `2026-08-20c` added. Phase 2 sweep confirmed `CON-1/2/3/5` closures and their INDEX/CATALOG rows untouched. `docs/adr/INDEX.md` regenerated. Phase 3 (the CONFIRM-scoring run) deliberately **not** executed — separate, later step. | Joshua + Claude Code |
| 2026-08-20 | **§7 Phase 3 executed, same session, operator instruction ("go ahead, execute the run").** Panel re-pulled (`MNQ.v.0` continuous 1m, $0.0000, `db_fetch.py estimate` confirmed before pull); `CONFIRM_GO.md` + a new window-only sibling runner `run_confirm_g0.py` authored (neither `run_construct_g0.py` nor `construct_lib.py` touched); 11/11 unit tests green pre-run (a real latent bug in the halves-aggregation helper, inherited faithfully from the EXPLORE runner, was caught by the new synthetic tests and fixed in the new file only). CONFIRM scored `AMBIGUOUS-HOLD` — [`RESULTS_CONFIRM.md`](../../lab/analysis/c1/mnq_tnec_con4_pdh_pdl_break_2026-08/RESULTS_CONFIRM.md). §4's revert trigger fired as pre-registered: U1 exception spent, `CON-4` reverted to `U0`. Closure addenda + INDEX/CATALOG rows updated to the final state. | Claude Code (operator-instructed run) |
