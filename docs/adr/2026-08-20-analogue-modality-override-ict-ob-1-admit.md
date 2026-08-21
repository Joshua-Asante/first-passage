# Operator override — admit `Q-ICT-OB-1` (Order Blocks) to the standard construct lifecycle despite the entry-geometry pause — `analogue-modality-override-ict-ob-1-admit`

**Status:** `Accepted` — ratified by operator (Joshua) 2026-08-20, in-session direct instruction
("let's spec the Order Blocks concept, if it requires an ADR override then I approve it so we can test
this concept") — approval given **before** the scoping doc existed, on the explicit condition that an
override is what §1 of that scoping doc would find necessary. See Ratification note.
**Decision date:** 2026-08-20
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Related:** [`Q-ICT-OB-1` scoping](../briefs/rnd-pipeline/Q-ICT-OB-1-order-blocks-scoping.md) (the
construct this ADR admits) ·
[`2026-08-15-analogue-modality-route-ruling.md`](2026-08-15-analogue-modality-route-ruling.md) (the
pause this ADR creates a bounded exception to — same mechanism as the OTE override) ·
[`2026-08-20-analogue-modality-override-ict-ote-1-admit.md`](2026-08-20-analogue-modality-override-ict-ote-1-admit.md)
(direct same-session precedent — same form, same governing mechanism, `Q-ICT-OTE-1` closed `FALSIFIED`
on its own cheap falsifier before this ADR was drafted)

---

**Tier:** full. Limb 4 fires, identical reasoning to the OTE override: creates a bounded exception to
the analogue-modality ADR's Boundary clause, this time for `Q-ICT-OB-1`. Limb 1 does not fire — this
licenses the $0 cheap-falsifier step only, same two-gate discipline as the OTE override.

---

## §0 — Rule-0 reads (2026-08-20)

Inherits the OTE override ADR's own §0 in full (same governing ADRs, same session, re-verified not
re-derived) plus:

- [`Q-ICT-OB-1` scoping](../briefs/rnd-pipeline/Q-ICT-OB-1-order-blocks-scoping.md) — read in full.
  **Load-bearing fact:** §2.4 names the stop-geometry risk *before* any measurement — a single-candle
  range is tighter than OTE's already-dead 13.16pt sweep-extreme anchor, so a result at or below that
  figure is the expected case, not a surprise.
- [`docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md`](2026-08-20-analogue-modality-override-ict-ote-1-admit.md)
  §7 Phase 1 outcome (`FALSIFIED`, mean stop_dist 13.16pt, WR 8-12%, both arms CI entirely below 0) —
  the immediate, same-session precedent this override is granted in light of, not blind to.

---

## §1 — Context

Following `Q-ICT-OTE-1`'s decisive `FALSIFIED` close, the operator instructed scoping Order Blocks and
pre-approved an override ADR for it in the same message — a standing authorization for this specific
construct, conditioned only on the scoping doc actually finding an override necessary (it did, §1 of
that doc, on identical grounds to OTE).

**Decision driver:** operator direct in-session instruction, 2026-08-20, given as advance approval
before the scoping work existed — an evidence-free exercise of standing operator authority, explicitly
undertaken with the OTE precedent's null result already known.

---

## §2 — Decision

**Decision:** `Q-ICT-OB-1` is admitted to the standard TNEC/ICT construct lifecycle — cheap falsifier →
`PREREG_G0` freeze → operator explore GO → EXPLORATION score → typed closure — as if the
analogue-modality pause did not apply, specifically and only for this construct.

**Licensed now:** the parent-side cheap falsifier only (§7 Phase 1) — $0, cache reuse of the panel
already on disk.

**Not licensed:** `PREREG_G0` freeze or any real-panel EXPLORATION score — gated behind a separate,
later operator explore GO, identical discipline to the OTE override.

**Scope:** `Q-ICT-OB-1` alone. Breaker Blocks and SMT Divergence remain unadmitted.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Treat the operator's advance pre-approval as also covering Breaker Blocks or SMT | Not instructed — the operator named "the Order Blocks concept" specifically; broader admission would be scope creep beyond the actual instruction. |
| License the full lifecycle through explore GO in one shot | Collapses the freeze-before-result discipline; identical reasoning to the OTE override §3. |
| Decline, citing OTE's fresh null as evidence against trying again | Not what was instructed — the operator explicitly pre-approved knowing OTE's shape was likely to recur (§2.4 of the scoping doc states this plainly); declining would substitute my judgment for an instruction already given with the relevant information in hand. |

---

## §4 — Falsifier (revert trigger)

**H:** an entry at the last opposing candle before a qualifying displacement clears a materially
different cost geometry against the frozen 1H DOL target than `Q-ICT-OTE-1`'s sweep-extreme entry did.

**Revert trigger:** the cheap falsifier (§7 Phase 1), once run, fails its pass bar — or, if it passes
and a later EXPLORE score returns `FALSIFIED` or `AMBIGUOUS-HOLD` under `Q-ICT-OB-1`'s own frozen gate.

**Revert action:** if the cheap falsifier fails, `Q-ICT-OB-1` is `STOP`-closed at $0, no G0 ever
frozen, and this override is spent with nothing further owed. If a later EXPLORE score is null, close
per the scoping doc's own §6 gate; the exception does not auto-renew for a retuned parameter (§5 bars
this explicitly). Either way this becomes the next data point in the short-horizon MNQ microstructure
thread, recorded honestly, not laundered as new evidence for a future override.

**Trigger check schedule:** on the cheap-falsifier run itself (one-shot, this session).

---

## §5 — Forbidden moves (under this ADR)

- **Reading this ADR as marking U1/U2 in the dense-1m lane's own vocabulary**, or as reopening
  `CON-1–5`/licensing `CON-6`. `Q-ICT-OB-1` is filed outside that lane; this is a separate,
  analogue-modality-specific exception, same as the OTE override.
- **Skipping or reordering the cheap falsifier's stop-geometry test.** The scoping doc's §2.4 names
  this as the first thing to check, not a disclosure after the fact.
- **Treating a cheap-falsifier PASS as license for `PREREG_G0` freeze or real-panel scoring.** §2 is
  explicit: those need a separate explore GO.
- **Retuning `dispMlt`, `ATR_LEN`, `ENTRY_ARM_WIN`, or the OB candle definition (full-range vs. body,
  single vs. multi-candle) after seeing any falsifier or explore number** — named in the scoping doc's
  §2.2/§5 before any measurement exists, specifically to prevent this.
- **Using this override as precedent to admit Breaker Blocks or SMT Divergence** without each getting
  its own ADR — this is a single named exception, not a doctrine change to the pause mechanism.
- **Treating a future PASS as licensing Cap, Pine, deploy, or arming.**

---

## §6 — Consequences

**Positive:** executes the operator's advance instruction; $0/no-K, bounded to the falsifier step.

**Negative:** a second override spent same-day on a construct whose own scoping already predicts the
same failure mode as the first. If this also returns null, the thread extends to an 11th zero-yield
close with two overrides spent in one session for no new information beyond confirming a predicted
pattern twice.

**Risks:** none beyond what §4/§5 already name.

---

## §7 — Implementation plan

- **Phase 1 (licensed)** — cheap falsifier for `Q-ICT-OB-1`, same panel, house convention
  (`_cheap_falsifier_ict_ob_1_2026-08-20.py` / `_LOG.md`), stop_dist reported first.
- **Phase 2/3 (not licensed)** — `PREREG_G0` freeze and explore GO remain separate operator decisions.

---

## §10 — Audit hooks (runnable)

```bash
ls discovery_manifests/ | grep -iE "ict.ob|ob.1"
ls lab/analysis/c1/cheap_falsifiers_2026-08/ | grep -i "ict_ob"
grep -n "dense-1m OHLCV temporal-selectivity lane default \*\*paused\*\*" docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md
```

---

## Ratification note

**Ratified by:** Joshua, in-session direct instruction — *"let's spec the Order Blocks concept, if it
requires an ADR override then I approve it so we can test this concept"* (2026-08-20) — approval given
in advance of, and conditioned on, the scoping doc's own governance finding. Authority channel:
explicit owner adjudication.

**Preconditions at ratification:** the scoping doc's §1 confirmed the override is necessary (identical
construct-type grounds to OTE) · `python scripts/check_brief.py
docs/adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md --type adr` passing ·
`python scripts/check_adr_graph.py` passing.

**Not licensed by this ratification:** anything §5 excludes — no `PREREG_G0` freeze, no real-panel
score, no admission of Breaker Blocks or SMT Divergence.

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md --type adr
python scripts/check_adr_graph.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-20 | Authored and ratified same-turn (operator advance-approval instruction). Status `Accepted` on introduction. | Joshua + Claude Code |
| 2026-08-20 | **§7 Phase 1 executed same session.** Cheap falsifier returned `FALSIFIED` — [`LOG`](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ob_1_2026-08-20_LOG.md): both arms n≥100, CI entirely below 0 (long −1.039R, short −0.379R), mean stop_dist 14.75pt. §4's revert trigger fired: exception spent, `PREREG_G0` never frozen. `Q-ICT-OB-1` closes `STOP` at $0/K=0. | Claude Code (operator-licensed run) |
