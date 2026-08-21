# Operator override — admit `Q-ICT-OTE-1` to the standard construct lifecycle despite the entry-geometry pause — `analogue-modality-override-ict-ote-1-admit`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-20, in-session direct instruction
("Approve an override ADR"), given in direct response to a fully-specified proposal (this ADR's own
§2/§9 scope, laid out before the instruction — see Ratification note)
**Decision date:** 2026-08-20
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`Q-ICT-OTE-1` scoping](../briefs/rnd-pipeline/Q-ICT-OTE-1-optimal-trade-entry-scoping.md)
(the construct this ADR admits) ·
[`2026-08-15-analogue-modality-route-ruling.md`](2026-08-15-analogue-modality-route-ruling.md) (the
pause this ADR creates a bounded exception to) ·
[`2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md`](2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
(the sibling, timeframe-axis ruling — checked and confirmed **not** to apply here; different
mechanism) · [`2026-08-20-dense1m-u1-operator-override-con4-reopen.md`](2026-08-20-dense1m-u1-operator-override-con4-reopen.md)
(direct same-day precedent for an evidence-free operator override; different pause mechanism — that
one marked U1 in the dense-1m lane's own vocabulary, this one does not, see §5) ·
[`docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md`](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
and [`Q-TNEC-CON-4-closure-ambiguous-hold.md`](../briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md)
(the 9-consecutive-null thread this override is evaluated against)

---

**Tier:** full. Limb 4 fires: this creates a bounded exception to standing doctrine (the analogue-modality
ADR's Boundary clause) that binds how `Q-ICT-OTE-1` specifically may proceed. Limb 1 (K/money) does not
fire yet — this ADR licenses the cheap-falsifier step (same $0, cache-reuse discipline as every prior
TNEC/ICT cell) but explicitly withholds the K-spending G0-freeze/explore-GO steps to a separate,
later operator decision (§2, §9).

---

## §0 — Rule-0 reads (2026-08-20)

- [`Q-ICT-OTE-1` scoping](../briefs/rnd-pipeline/Q-ICT-OTE-1-optimal-trade-entry-scoping.md) — anchor:
  authored this session, uncommitted at read time. Read in full. **Load-bearing facts:** the construct
  reuses `Q-ICTEXP-1`'s raid-scan and frozen 1H DOL target verbatim; only the impulse-leg/Fib-zone
  entry (§2.2–§2.3) is new; §2.4 flags the stop is likely leg-scale (CON-5-shaped risk, not
  CON-4-shaped) and states the cheap falsifier must test this first, not last.
- [`docs/adr/2026-08-15-analogue-modality-route-ruling.md`](2026-08-15-analogue-modality-route-ruling.md)
  — `Accepted`. **The rule this ADR creates an exception to**, quoted exactly: *"θ-parameterised
  entry-geometry constructs stay paused on their own terms."* Its own Gate section names its re-test
  condition (2026-11-08 audit, "if no algorithmic-analogue construct ever opens a manifest") — this
  override does not touch that gate; it operates a level below it, as a named exception for one
  construct, the same way the CON-4 ADR operated a level below the dense-1m pause's own U0/U1/U2
  vocabulary without amending it.
- [`docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md`](2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
  — `Accepted`. Checked and confirmed **inapplicable**: its D2 falsifier gate exempts cards from the
  *dense-1m lane-membership* argument only; it does not touch the analogue-modality construct-type
  test this ADR is granting an exception to. Cited so a future reader does not assume this ADR is that
  gate's falsifier-pass event — it is not; this is a direct operator override, not a D2 PASS.
- [`docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md`](2026-08-20-dense1m-u1-operator-override-con4-reopen.md)
  — `Accepted`, same session. Direct precedent for the *form* of an evidence-free operator override
  (bounded, single-construct, named forbidden moves, revert trigger tied to the construct's own gate).
  **Not precedent for scope**: that ADR marked U1 in the dense-1m lane's own vocabulary because CON-4
  lives inside that lane; `Q-ICT-OTE-1` is deliberately filed outside it (its own §0), so this ADR
  grants a different, analogue-modality-specific exception instead — see §5 forbidden move 1.
- [`Q-TNEC-CON-5` closure](../briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md) and [`Q-TNEC-CON-4`
  closure](../briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md) — the 9-consecutive-zero-yield
  thread (as of `CON-4`'s CONFIRM score, 2026-08-20) this override is evaluated against, not blind to.
- [`ops/instruments/MNQ.md`](../../ops/instruments/MNQ.md) N6 and the CON-4/CON-5 stop-geometry pair —
  the cost-law framework the cheap falsifier below applies.

**Amendment-first / dedup (Rule 8 sub-rule 10):**

```
$ python scripts/check_advisor_dedup.py --keywords "optimal trade entry OTE override admit analogue modality exception"
```
No prior owner exists for an OTE-specific override — `Q-ICT-OTE-1`'s own §0 dedup (executed at
scoping time) already cleared the construct itself; this is the governance act admitting it, a
distinct, undocumented decision until now.

---

## §1 — Context

`Q-ICT-OTE-1` was scoped 2026-08-20 and found blocked on construct-type grounds: it names entry
geometry (a Fibonacci retracement band, a touch trigger), which the 2026-08-15 analogue-modality ADR
rules stays paused "on their own terms" independent of timeframe (checked separately against the
2026-08-16 timeframe-scope ADR, which does not apply — different axis). Presented with the governance
finding and two paths (override now, or wait for a genuine new modality), the operator elected
**override**, in-session, immediately following a fully specified proposal of what that would cost and
authorize.

**Decision driver (one sentence):** operator direct in-session instruction, 2026-08-20, "Approve an
override ADR," given in response to an already-laid-out scope (cheap falsifier next, G0/explore GO
separately) — an evidence-free exercise of standing operator authority, not a new-modality claim.

---

## §2 — Decision

**Decision:** `Q-ICT-OTE-1` is admitted to the standard TNEC/ICT construct lifecycle — parent-side
cheap falsifier → `PREREG_G0` freeze → operator explore GO → EXPLORATION score → typed closure —
**as if the analogue-modality pause did not apply to it**, specifically and only for this construct.

**What this ADR licenses right now:** the parent-side cheap falsifier only (§7 Phase 1) — $0, cache
reuse of the already-on-disk MNQ 1m panel (pulled this session for `Q-TNEC-CON-4`'s CONFIRM run), no
manifest, no Q-ID spend, generous-by-design per `lesson_run_cheap_falsifier_before_authoring`.

**What this ADR does NOT license:** the `PREREG_G0` freeze or any real-panel EXPLORATION score. Those
remain gated behind a **separate, later operator explore GO** — the same two-step discipline every
TNEC/ICT cell in this corpus (including `Q-TNEC-CON-4`/`CON-5` themselves) has always used, and the
same discipline the CON-4 override ADR applied to its own Phase 3. This ADR's own approval does not
collapse that gate.

**Effective:** immediately upon acceptance, for the cheap-falsifier step only.
**Scope:** `Q-ICT-OTE-1` alone. No other candidate from the wider-ICT-vocabulary ranking (Order
Blocks, Breaker Blocks, SMT Divergence) is admitted by this decision.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Admit the whole wider-ICT-vocabulary class (OB/OTE/Breaker/SMT) | Broader than instructed; Order Blocks and Breaker Blocks were independently flagged CON-5-shaped-or-worse on cost-geometry, and SMT was flagged doubly-barred and population-starved — admitting all four on one override would spend the same evidence-free authority on the two weakest candidates too. |
| License the full lifecycle through explore GO in one shot | Collapses the freeze-before-result discipline this corpus enforces everywhere else (cheap falsifier and G0 freeze are pre-registration steps that must precede, not substitute for, a distinct explore GO). Also front-loads K-spend before the $0 cheap falsifier has had a chance to kill the construct outright, as CON-4's own cheap falsifier nearly did not but was designed to be able to. |
| Wait for a genuine new modality | The path the governing ADRs actually prefer; operator explicitly declined it this session in favor of override. |
| Status quo — decline the override | Does not execute the operator's direct instruction. |

---

## §4 — Falsifier (revert trigger)

**Revert trigger:** the cheap falsifier (§7 Phase 1), once run, fails its generous pass bar — or, if it
passes and a later EXPLORE score returns `FALSIFIED` or `AMBIGUOUS-HOLD` under `Q-ICT-OTE-1`'s own
frozen gate (§6 of the scoping doc).

**Revert action:** if the cheap falsifier fails, `Q-ICT-OTE-1` is `STOP`-closed at $0, no G0 ever
frozen, and this override is spent with nothing further owed — the exception was for this attempt, not
a standing license. If a later EXPLORE score is null, file the closure per the scoping doc's own §6
gate; the exception does not auto-renew for a re-tuned Fib band or FVG-precondition choice (§5 of the
scoping doc's own forbidden moves already bar that). Either way this becomes the 10th (or later) data
point in the short-horizon MNQ microstructure thread — recorded honestly, not laundered as new
evidence for a future override.

**If the cheap falsifier passes:** this ADR does **not** auto-license the G0 freeze or explore GO —
those need the separate operator decision named in §2.

**Trigger check schedule:** on the cheap-falsifier run itself (one-shot, this session).

---

## §5 — Forbidden moves (under this ADR)

- **Reading this ADR as marking U1/U2 in the dense-1m lane's own vocabulary**, or as reopening
  `CON-1–5` or licensing `CON-6`. `Q-ICT-OTE-1` is filed outside that lane by its own scoping §0; this
  ADR's exception is to the analogue-modality ADR's Boundary clause specifically, a different governing
  mechanism, and touches nothing in the dense-1m lane.
- **Skipping or reordering the cheap falsifier's stop-geometry test.** The scoping doc's §2.4 names
  this as the first thing to check, not a disclosure after the fact — the falsifier must report mean
  stop_dist alongside mean gross pts, exactly as CON-4/CON-5 did.
- **Treating a cheap-falsifier PASS as license for `PREREG_G0` freeze or real-panel scoring.** §2 is
  explicit: those need a separate explore GO.
- **Retuning the Fib band (0.62–0.79) or the FVG-precondition choice (scoping §2.2) after seeing any
  falsifier or explore number** — both were named before any measurement exists specifically to
  prevent this (Known Trap #12).
- **Using this override as precedent to admit Order Blocks, Breaker Blocks, or SMT Divergence** without
  each getting its own ADR — this is a single named exception, not a doctrine change to the pause
  mechanism.
- **Treating a future PASS as licensing Cap, Pine, deploy, or arming** — unchanged from every other
  TNEC/ICT cell.

---

## §6 — Consequences

**Positive:** executes the operator's direct instruction; the cheap falsifier is $0/no-K and, per its
own design, most likely to kill a bad construct cheaply rather than let it advance.

**Negative (real cost, not theatrical):** spends operator override authority — a scarce, socially
costly resource in this corpus's own governance culture — on a construct whose own scoping already
flagged real stop-geometry risk, immediately after a 9-consecutive-null pattern. If the cheap falsifier
or EXPLORE both pass through to a null, the override reads, in hindsight, as spent on a predictable
result.

**Risks:** none beyond what §4/§5 already name — the design (cheap falsifier first, K-gated behind a
separate GO) bounds the downside to $0 unless the operator separately authorizes further spend.

**Downstream artifacts that need updating:** `docs/briefs/rnd-pipeline/Q-ICT-OTE-1-optimal-trade-entry-scoping.md`
§1/§9 (this override discharges the governance question those sections posed) · `docs/SESSIONS.md`
(board write, this session).

---

## §7 — Implementation plan

- **Phase 0** — §0 reads verified current this session (done, above).
- **Phase 1 (licensed by this ADR, executed same session)** — author and run the parent-side cheap
  falsifier for `Q-ICT-OTE-1`: reuse the existing `_mnq_1m.parquet` panel; test the raid→confirmed-leg→
  Fib-zone→sweep-extreme-stop construct's mean signed gross against a generous pass bar (same
  discipline as every prior `_cheap_falsifier_*` in `lab/analysis/c1/cheap_falsifiers_2026-08/`),
  reporting stop_dist first per §5's forbidden-move guard. File the result as a `_cheap_falsifier_ict_ote_1_2026-08-20_LOG.md`
  in that directory, matching house convention.
- **Phase 2 (NOT licensed by this ADR)** — if Phase 1 passes: `PREREG_G0` freeze, still no K spent
  until an explore GO is separately granted.
- **Phase 3 (NOT licensed by this ADR)** — operator explore GO, then EXPLORATION score, then typed
  closure per the scoping doc's own §6 gate.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR must not itself have opened a manifest or scored a real panel:
ls discovery_manifests/ | grep -iE "ict.ote|ote.1"
test -f lab/analysis/c1/ict_ote_1_*/PREREG_G0.md && echo "VIOLATION: G0 frozen without separate GO"

# The cheap falsifier this ADR licenses must land in the standing directory, house-named:
ls lab/analysis/c1/cheap_falsifiers_2026-08/ | grep -i ote

# The dense-1m lane's own U0/U1/U2 vocabulary must be untouched by this ADR:
grep -n "dense-1m OHLCV temporal-selectivity lane default \*\*paused\*\*" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
# Expected: 1 hit, unchanged

# Freeze-ordering: cheap falsifier must postdate this ADR's acceptance
git log --format='%h %cs' -- docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md | tail -1
```

---

## Ratification note

**Ratified by:** Joshua, in-session direct instruction — *"Approve an override ADR"* (2026-08-20),
given in direct response to a fully-specified proposal (this ADR's own §2/§9 scope: cheap falsifier
licensed now, G0/explore-GO gated separately, cost and risk both stated before the instruction).
Authority channel: explicit owner adjudication.

**Preconditions at ratification:** `python scripts/check_brief.py
docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md --type adr` passing ·
`python scripts/check_adr_graph.py` passing (checked below, same commit).

**Not licensed by this ratification:** anything §5 already excludes — in particular, no `PREREG_G0`
freeze and no real-panel score happen under this ratification alone; both need a separate explore GO.

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md --type adr
python scripts/check_adr_graph.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Authored and ratified same-turn (operator instruction, "Approve an override ADR," given in response to an already-laid-out scope). Status `Accepted` on introduction. | Joshua + Claude Code |
| 2026-08-20 | **§7 Phase 1 executed same session.** Cheap falsifier ran (reconstructing the sweep/pivot detector fresh — original code unavailable in this public worktree, see the falsifier's own reconstruction note) and returned `FALSIFIED` — [`LOG`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ote_1_2026-08-20_LOG.md): both arms n≥100, CI entirely below 0 (long −0.525R, short −0.518R), mean stop_dist 13.16pt confirming the scoping doc's own predicted CON-5-shaped risk. §4's revert trigger fired: exception spent, `PREREG_G0` never frozen, Phase 2/3 do not follow. `Q-ICT-OTE-1` closes `STOP` at $0/K=0. | Claude Code (operator-licensed run) |
