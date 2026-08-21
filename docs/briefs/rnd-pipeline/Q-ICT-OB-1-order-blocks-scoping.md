# `Q-ICT-OB-1` — Order Blocks (last opposing candle before a displacement move) on native MNQ

**Status:** `STOP — cheap falsifier FALSIFIED 2026-08-20. Never reached PREREG_G0. $0.00 spent, K=0.`
**Cheap falsifier:** [`_cheap_falsifier_ict_ob_1_2026-08-20_LOG.md`](../../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ob_1_2026-08-20_LOG.md)
— both arms n≥100, CI entirely below 0 (long −1.039R, short −0.379R), mean stop_dist 14.75pt
confirming §2.4's prediction, WR 11–12% (essentially identical to `Q-ICT-OTE-1`'s own 8–12%). Licensed
by [`the override ADR`](../../adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md) §7 Phase 1;
its §4 revert trigger fired — exception spent, no G0 follows.
**Class:** a real construct once opened — same class as `Q-ICT-OTE-1`, **not** the `Q-ICTEXP-1`
zero-K falsifier class.
**Purpose:** define the Order Block construct precisely enough to freeze a G0 the moment governance
clears it. **Occasioned by:** operator instruction, 2026-08-20, following `Q-ICT-OTE-1`'s `FALSIFIED`
close — Order Blocks was the other candidate flagged CON-5-shaped-risk-but-abundant-population in the
original concept-gap ranking, and the operator pre-approved an override ADR for it in the same
instruction that requested this scoping.
**Loop of record:** OUTER (INQHIORI). **Authored:** 2026-08-20 · Claude Code (Sonnet 5),
operator-directed.

---

## §0 — Rule-0 reads (verified this session, 2026-08-20)

All governance grounding is inherited from `Q-ICT-OTE-1`'s own §0 (same session, same governing
ADRs) — re-verified here rather than re-derived:

- [`docs/adr/2026-08-15-analogue-modality-route-ruling.md`](../../adr/2026-08-15-analogue-modality-route-ruling.md)
  (`Accepted`) — the construct-type test: *"the absence of named entry geometry, not the presence of
  the word."* Order Blocks names a level (the OB candle's own high-low range) and a trigger
  (return-to-range) — fails this test on the same grounds `Q-ICT-OTE-1` did.
- [`docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md`](../../adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
  (`Accepted`) — checked again, same conclusion as `Q-ICT-OTE-1`'s §0: this is a different axis
  (dense-1m lane-membership, not construct-type) and does not offer an escape here either.
- [`docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md`](../../adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md)
  (`Accepted`) — direct same-day precedent for both the override *form* and the outcome: OTE's own
  stop-geometry risk (§2.4 of its scoping doc) was confirmed exactly by its cheap falsifier
  (`FALSIFIED`, mean stop_dist 13.16pt, WR 8–12%). Order Blocks carries the **identical** stop-geometry
  risk (§2.4 below) — this scoping does not pretend otherwise.
- [`lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ote_1_2026-08-20_LOG.md`](../../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ote_1_2026-08-20_LOG.md)
  — the reconstruction note applies identically here: `run_1m_diag.py` (the original displacement/FVG
  detector) is absent from this public worktree; this construct's displacement detection is
  reconstructed fresh from the same documented parameters (`dispMlt=1.5×ATR(14)`), not imported code.
- [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) N9 (liquidity pools are anti-attractors,
  30-34% of a random-walk-matched base) — relevant background only: Order Blocks are a different
  object class from N9's pools (a displacement-adjacent candle, not an untouched prior extreme), so N9
  does not bind this construct directly, but its own lesson (naive ICT "magnet" framings have not
  survived contact with MNQ data in this corpus) is the right prior to hold walking in.

**Amendment-first / dedup (Rule 8 sub-rule 10), executed this session:**

```
$ python scripts/check_advisor_dedup.py --keywords "order block bullish bearish institutional zone displacement candle"
  slugs found:    (none)
```
No prior owner. `Q-ICT-OTE-1`'s own dedup (2026-08-20) already covers the near-neighbor tokens; that
result is not re-derived here.

---

## §1 — Governance verdict (unchanged conclusion from `Q-ICT-OTE-1`)

**Order Blocks is blocked on the identical construct-type grounds as OTE was**, and the operator has
already pre-approved an override for it (see this session's instruction). §9 below is therefore short:
an override ADR follows this scoping doc directly, mirroring
[`2026-08-20-analogue-modality-override-ict-ote-1-admit.md`](../../adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md).

---

## §2 — Construct definition

### 2.1 Displacement detection (reconstructed from documented parameters, same as `Q-ICT-OTE-1`)

A displacement move at bar `t` is `|close[t] - close[t-1]| >= dispMlt * ATR(14)`, `dispMlt=1.5` —
identical threshold already frozen for FVG/OTE detection in this corpus.

### 2.2 Order block candle (new — the object OTE never needed)

The order block is the **last opposite-colored candle immediately before a displacement sequence
begins.** For an upward displacement (bullish OB): scan backward from the first displacement bar for
the nearest down-close (`close < open`) candle — that candle's `[low, high]` is the OB range. Symmetric
for a downward displacement (bearish OB): nearest up-close candle before it.

**No sweep precondition** in this first pass — any qualifying displacement gets an OB candidate,
matching the population estimate from the concept-gap ranking pass (~1:1 with displacement-FVG count,
≈128,089). Adding a sweep-precondition (only score OBs that follow a liquidity raid, tightening toward
`Q-ICT-OTE-1`'s own population) is named here as a **later, separate construct** if this one's
population turns out too loose to be informative — not a retune of this G0 (§5).

### 2.3 Entry (return to the OB range)

Entry arms once price displaces away from the OB candle and is live until either (a) price returns
into `[OB.low, OB.high]` (entry at that touch) or (b) `ENTRY_ARM_WIN` bars elapse un-touched (signal
expires, no trade). Entry price = the touch price (limit-style, matching `Q-ICT-OTE-1`'s convention).

### 2.4 Stop, target, exit, cost — and the risk flagged before any number exists

| Element | Value | Source |
|---|---|---|
| Stop | beyond the OB candle's far edge (below `OB.low` for bullish, above `OB.high` for bearish) | new — candle-range-anchored |
| Target | `dolMode = range-extreme` — 1H `h1High`/`h1Low`, reused verbatim | `PREREG-1H.md`, same as `Q-ICT-OTE-1` |
| Exit | target touch, or E1 flat-by-16:00 ET, whichever first | reused verbatim |
| Cost basis | Tradeify RT 1.41pt | reused verbatim |
| Bar | 5.640 pt | identical to `Q-ICT-OTE-1`'s frozen bar |

**Named before measurement, not after (Known Trap #12):** a single-candle range on 1m MNQ bars is a
**tighter** stop than OTE's already-leg-scale sweep-extreme anchor, which itself measured 13.16pt and
died decisively. The concept-gap ranking pass flagged Order Blocks and Breaker Blocks as *tied, worst*
on cost-geometry for exactly this reason. This scoping does not soften that finding — the cheap
falsifier (§9) must report mean stop_dist first, and a result at or below OTE's 13.16pt should be read
as expected, not surprising.

---

## §3 — Question

Does an entry at the last opposing candle before a qualifying displacement, into the same frozen 1H
DOL target OTE used, clear a materially different cost geometry than OTE's sweep-extreme entry did — or
does it inherit the identical single-digit-to-teens-point stop problem, only more so (no sweep
precondition to filter for higher-conviction setups)?

---

## §4 — Falsifiable hypothesis

**H-OB-1:** the OB entry, scored EXPLORATION-only against the frozen DOL target, produces at least one
arm whose mean net R has a session-block 95% CI entirely above 0 (DSR ≥0.650 at `K_intrinsic=1`).

**Falsifier:** both arms CI entirely below 0 at powered n → `FALSIFIED`. Identical gate shape to
`Q-ICT-OTE-1`/CON-4/CON-5 — no new criterion invented.

---

## §5 — Forbidden moves

- Adding a sweep-precondition, a body-only (vs. full-range) OB definition, or a multi-candle OB
  variant after seeing any result — each is a new construct, named in §2.2 as a possible *later* step,
  not a retune of this one.
- Filing under `CON-6` or the dense-1m lane's own numbering.
- Treating the cheap falsifier as anything but a stop-geometry-first test (§2.4).
- Retuning `dispMlt`, `ATR_LEN`, or `ENTRY_ARM_WIN` after seeing a result.
- Cap / Pine / deploy / arming from this packet, ever.

---

## §6 — Gate

Identical shape to `Q-ICT-OTE-1`/CON-4/CON-5. Today's actual gate is §1: blocked pending the override
below.

---

## §9 — Governance

Operator pre-approved an override ADR for this construct in the same instruction that requested this
scoping (2026-08-20). See
[`docs/adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md`](../../adr/2026-08-20-analogue-modality-override-ict-ob-1-admit.md)
— licenses the cheap-falsifier step only; `PREREG_G0`/explore GO remain separately gated, same
discipline as `Q-ICT-OTE-1`.

---

## §10 — Audit hooks (runnable)

```bash
ls discovery_manifests/ | grep -iE "ict.ob|ob.1"
test -d lab/analysis/c1/mnq_tnec_con6* && echo "VIOLATION: CON-6 scaffolded" || echo "OK: no CON-6"
grep -n "absence of named entry geometry" docs/adr/2026-08-15-analogue-modality-route-ruling.md
python scripts/check_advisor_dedup.py --keywords "order block bullish bearish institutional zone displacement candle"
```

---

## Amendment log (append-only)

- **2026-08-20 — SCOPED.** Not run, not pre-registered, no K bound, no manifest, $0 committed.
  Authored at operator instruction, override pre-approved in the same instruction.
- **2026-08-20b — OVERRIDE RATIFIED, cheap falsifier run, STOP same session.** Verdict `FALSIFIED`:
  both arms powered, CI entirely below 0, mean stop_dist 14.75pt confirming §2.4. `PREREG_G0` never
  frozen. Cross-cutting note (⚠ **corrected 2026-08-20e below, on two counts**): this was originally
  described as "the third of three same-session entry-geometry constructs (`Q-TNEC-CON-4` CONFIRM,
  `Q-ICT-OTE-1`, `Q-ICT-OB-1`) to die anchored to the identical frozen 1H DOL target."
- **2026-08-20e — TWO CORRECTIONS to the note above.** (1) `Q-TNEC-CON-4` does not use the 1H DOL
  target at all — its exit is session-flat only (re-verified against its own frozen geometry table).
  Only `Q-ICTEXP-1`, `Q-ICT-OTE-1`, and `Q-ICT-OB-1` share it. (2) The "shared target is the point of
  failure" hypothesis was tested directly and **refuted** —
  [`ict_target_investigation_2026-08-20/RESULTS.md`](../../../lab/analysis/c1/ict_target_investigation_2026-08-20/RESULTS.md):
  a zero-run distance sweep (5–300pt, bracketing both this stop's scale and the DOL's own ~285pt
  measured distance) found mean R negative at every tested distance. The entries lack directional edge
  independent of exit choice; the target itself is exonerated. Re-proposal bar (§ above) now explicitly
  excludes a target retune, not just a parameter retune.
