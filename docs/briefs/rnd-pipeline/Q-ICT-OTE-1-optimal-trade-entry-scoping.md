# `Q-ICT-OTE-1` — Optimal Trade Entry (Fibonacci retracement off a confirmed sweep-impulse leg) on native MNQ

**Status:** `STOP — cheap falsifier FALSIFIED 2026-08-20. Never reached PREREG_G0. $0.00 spent, K=0.`
**Cheap falsifier:** [`_cheap_falsifier_ict_ote_1_2026-08-20_LOG.md`](../../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_ict_ote_1_2026-08-20_LOG.md)
— both arms n≥100, session-block CI entirely below 0 (long −0.525R, short −0.518R), mean stop_dist
13.16pt confirming the §2.4 CON-5-shaped risk prediction exactly. Licensed by
[`the override ADR`](../../adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md) §7 Phase 1;
that ADR's own §4 revert trigger fired — the exception is spent, no G0 freeze follows.
**Class:** order-free at scoping time; a real construct once opened — **NOT** the `Q-ICTEXP-1` zero-K
falsifier class (see §9 — this is a genuinely new entry-geometry construct, not a one-way kill test).
**Purpose:** define the OTE construct precisely enough to freeze a G0 the moment governance clears it,
so no further scoping work is owed before an operator GO — and state, without softening, exactly what
currently blocks it.
**Occasioned by:** operator instruction, 2026-08-20, following the [ICT concept-gap
ranking](../../SESSIONS.md#2026-08-20c--operator-override-u1-exception-reopens-q-tnec-con-4-confirm-inside-the-dense-1m-pause)
that placed OTE first among the untested wider-ICT-vocabulary candidates on population and
cost-geometry grounds.
**Loop of record:** OUTER (INQHIORI) — candidate scoping, not a STRATEGIC-tier decision. **Authored:**
2026-08-20 · Claude Code (Sonnet 5), operator-directed.

---

## §0 — Rule-0 reads (verified this session, 2026-08-20)

- [`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md`](../../spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md)
  — the dense-1m TNEC lane this construct's *shape* resembles but is **not** filed under. §1: the
  next fresh Q-ID in that lane's own numbering would be `Q-TNEC-CON-6` — explicitly **not licensed**
  by `DENSE1M-UNPAUSE` (see below). This scoping deliberately uses an independent `Q-ICT-OTE-1` id,
  not `CON-6`, so it never appears to claim a license it doesn't have.
- [`docs/adr/2026-08-15-analogue-modality-route-ruling.md`](../../adr/2026-08-15-analogue-modality-route-ruling.md)
  (`Accepted`) — **the load-bearing governance fact.** Its own test, quoted exactly: *"the test is the
  **absence** of named entry geometry, not the presence of the word [analogue]."* Its Boundary clause:
  *"θ-parameterised entry-geometry constructs stay paused **on their own terms**"* — independent of
  timeframe (see next read). OTE names a level (the 0.62–0.79 Fib band) and a trigger
  (retracement-touch) by definition — it fails this test on construct-type grounds alone.
- [`docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md`](../../adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
  (`Accepted`) — the **separate, timeframe axis**, checked explicitly so this scoping doesn't miss an
  available escape. D1: the pause is textually scoped to *"the dense-1m G=10 universe"* — a card
  outside that literal lane (e.g. 15m) may argue it's exempt, but only after clearing D2's $0 cheap
  falsifier (mean signed gross ≥ 0.5× CON-5's own clearance bar, on the card's own IS panel). **This
  does not rescue OTE**: D2 only licenses escaping the *"dense-1m/G=10 lane-membership"* argument to
  clear the domain-level raised bar via route ① — it says nothing about the analogue-modality ADR's
  separate construct-type test above, and that ADR's own Boundary clause is explicit that
  entry-geometry constructs "stay paused on their own terms" regardless of timeframe. Moving OTE to
  5m/15m would not change the verdict below.
- [`docs/briefs/closures/Q-TNEC-CON-5-closure-ambiguous-hold.md`](../closures/Q-TNEC-CON-5-closure-ambiguous-hold.md)
  and [`docs/briefs/closures/Q-TNEC-CON-4-closure-ambiguous-hold.md`](../closures/Q-TNEC-CON-4-closure-ambiguous-hold.md)
  — the pause's own origin (9 consecutive zero-yield closes as of 2026-08-20, after CON-4's CONFIRM
  reconfirmed dead) and the precedent for how a construct of this shape actually gets admitted: parent
  cheap falsifier → `PREREG_G0` freeze → operator explore GO → EXPLORATION score → typed closure.
- [`docs/adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md`](../../adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md)
  (`Accepted`) — the only precedent in this repo for admitting a paused-class construct: a full,
  named, scoped operator override ADR, spent same-day on a single already-frozen exception. Reusable
  as a template if the operator elects to override again for OTE (see §9).
- [`lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py`](../../../lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py)
  and [`PREREG_EXP.md`](../../../lab/analysis/_inbox/ict_mnq_2026-08/PREREG_EXP.md) — the raid-scan
  (`pvLen=2`, `raidWin=8`, heap-based, 42 unit tests) and DOL-target (`h1High`/`h1Low`, 1H
  range-extreme, `lookN=60`) machinery this construct reuses verbatim (§2 below) rather than
  re-deriving. `Q-ICTEXP-1`'s own construct is `AMBIGUOUS` (null, `SUBTRACT` — [`b7
  pursuit`](../../pursuits/b7-ict-line.md)) at its **frozen DOL-target exit**; OTE changes the *entry*
  only (Fib retracement vs. FVG-mid), so it is a genuinely different hypothesis, not a relabeled
  re-proposal of a dead one.
- [`ops/instruments/MNQ.md`](../../../ops/instruments/MNQ.md) N6 (cost hurdle ≈3.01bp/session, 4×RT =
  5.640pt at the Tradeify basis) and the CON-4/CON-5 pair's own stop-geometry lesson (wide structural
  stop survives RT but needs the edge to carry the weight; tight stop lets RT dominate and WR
  collapses it) — the exact tension §7's geometry choice below has to resolve.

**Amendment-first / dedup (Rule 8 sub-rule 10), executed this session:**

```
$ python scripts/check_advisor_dedup.py --keywords "optimal trade entry OTE fibonacci retracement"
  slugs found:    (none)
  top hits: gate-stack audit (shared terms: 'entry','optimal','trade' — false positive,
  unrelated), S-MYM-ORC-01 closure (shared term 'entry' only — false positive).
```

**Judgment:** no prior owner exists for OTE specifically. Nearest neighbors on record are the FVG
entry (`Q-ICTEXP-1`, different entry rule, same DOL target — see below) and the impulse-pullback-VWAP
construct (`CON-5`, different retracement anchor — VWAP, not a swept-leg Fibonacci band, and a
different, tighter stop rule). Neither is a substitute for OTE; nothing here is re-derived.

---

## §1 — Governance verdict (read this before the construct — it is the load-bearing fact)

**OTE is blocked, not merely unscoped.** It names an entry level (the 0.62–0.79 retracement band) and
a trigger (touch of that band) — the exact shape the 2026-08-15 analogue-modality ADR rules stays
paused "on their own terms," independent of timeframe (2026-08-16 ADR checked and does not help — see
§0). This scoping document freezes the construct so it is ready the moment that changes, but **it does
not, and cannot, license a cheap falsifier, a `PREREG_G0` freeze, or any real-panel score on its own.**
See §9 for the two paths that would change this and exactly what each needs from you.

---

## §2 — Construct definition (frozen at scoping; genuinely new only in §2.3)

Reuses two already-built, already-unit-tested pieces verbatim; only §2.3 (the impulse-leg /
retracement-zone logic) is new code.

### 2.1 Sweep detection (reused verbatim, unmodified)

Heap-based raid scan from `run_1m_diag.py`: `pvLen=2` pivot detection, `raidWin=8` same-direction
pairing window. A sell-side liquidity raid (SSL sweep) precedes a bullish setup; a buy-side raid (BSL
sweep) precedes a bearish setup. This is the identical detector `Q-ICTEXP-1`'s 32,355-event population
came from — no re-derivation, no new K on this piece.

### 2.2 Confirmed impulse leg (new — the swing-confirmation rule OTE requires that FVG-entry did not)

An impulse leg is confirmed when price, following the sweep, closes beyond a structural pivot in the
sweep's direction (the same `pvLen=2` pivot definition as §2.1, applied post-sweep) **and** the
displacement from sweep-extreme to that pivot clears `dispMlt=1.5×ATR(14)` — the identical
displacement threshold already frozen for FVG detection in this corpus (`PREREG-1M.md`), reused rather
than invented. The leg's start is the sweep extreme; its end is the confirming pivot's close.

**This is the one placeholder value that needs an a-priori choice before G0 freeze:** whether
"confirmed" additionally requires a same-direction FVG on the leg (ICT's textbook OTE precondition) or
stands on the displacement threshold alone. Recommend requiring the FVG (tighter population, but
directly reuses the already-tested FVG detector with zero new logic) — named here so it is chosen
before any measurement exists, not after seeing which reads better (Known Trap #12).

### 2.3 Entry zone (Fibonacci retracement of the confirmed leg)

`fib_level = leg_end - direction * (leg_end - leg_start) * pct`, `pct ∈ [0.62, 0.79]`. Entry is a limit
order at first touch of this band, arming from the pivot-confirmation bar onward within the same
session (no cross-session carry — mirrors `Q-ICTEXP-1`'s `retraceK`-style bounded arming window, value
TBD at freeze, not invented here).

### 2.4 Stop, target, exit, cost (reused verbatim from `Q-ICTEXP-1`'s frozen DOL construct)

| Element | Value | Source |
|---|---|---|
| Stop | beyond the sweep extreme (i.e., beyond the 1.0 Fib level) | new (leg-anchored, not FVG-anchored) |
| Target | `dolMode = range-extreme` — 1H `h1High`/`h1Low`, `lookN=60`, `[1]`-lagged, non-repaint | `PREREG-1H.md` / `B2_B3_CHANGES.md`, reused verbatim |
| Exit | target touch, or E1 flat-by-16:00 ET, whichever first | `ops/prop_envelope_default.md` E1, reused verbatim |
| Cost basis | Tradeify RT 1.41pt (MNQ $2.00/pt) | `core/firm_rules.py`, reused verbatim |
| Bar | 4.0 × 1.410 = **5.640 pt** mean expectancy per filled event | identical to `Q-ICTEXP-1`'s frozen bar |

**Why the stop is likely tight (the CON-5-shaped risk flagged in the concept-ranking pass):** a sweep
extreme to a confirming pivot is a leg-scale distance, not a session-range distance — almost certainly
closer to CON-5's ≈17.5pt than CON-4's ≈257pt. This is exactly the geometry that made RT dominate R and
collapsed WR to 11–14% on CON-5. **The cheap falsifier (§9, once licensed) must test this directly and
first** — report mean stop_dist alongside gross pts, not after.

---

## §3 — Question

Does a Fibonacci retracement entry, taken only after a confirmed post-sweep impulse leg, into the
already-frozen 1H range-extreme DOL target, clear a materially different cost geometry than
`Q-ICTEXP-1`'s FVG-mid entry did on the identical target — or does it inherit the same RT-tax problem
(this time from the stop side, given the anchor is a leg extreme rather than a session range)?

---

## §4 — Falsifiable hypothesis

**H-OTE-1:** the OTE entry, scored EXPLORATION-only against the frozen DOL target, produces at least
one arm whose mean net R has a session-block 95% CI entirely above 0 (and DSR ≥ 0.650 at
`K_intrinsic=1`), distinguishing it from `Q-ICTEXP-1`'s own null result on the same target with a
different entry.

**Falsifier:** both arms fail with CI entirely below 0 at powered n → `FALSIFIED`, re-proposal bar =
new mechanism, not a Fib-band retune. Mirrors CON-4/CON-5's own gate shape exactly — no new criterion
invented.

---

## §5 — Forbidden moves

- **Filing this under `Q-TNEC-CON-6`** or scaffolding `mnq_ict_ote_1_*` inside the paused dense-1m
  lane's own directory convention — `DENSE1M-UNPAUSE` explicitly does not license CON-6 authorship.
  This scoping stays a standalone `Q-ICT-OTE-1`, deliberately outside that lane's numbering.
- **Reading §2's construct definition as a G0 freeze.** No commit here starts the freeze-before-result
  clock; that only happens after §9's governance question is resolved.
- **Running the §9 cheap falsifier without an explicit operator answer to §9** — even though it would
  be $0/no-K, doing so pre-empts the governance decision this document exists to surface.
- **Loosening §2.2's FVG-precondition choice, or the retracement band, after seeing which reads
  better** — both are named now, before any number exists, exactly to prevent this.
- **Treating a future PASS as licensing Cap, Pine, deploy, or arming** — this construct, if it ever
  runs, inherits the same restrictions every TNEC/ICT cell in this corpus carries.

---

## §6 — Gate (once governance clears — not active today)

Identical shape to CON-4/CON-5's own gate (`FALSIFIED` / `SHAPE-CLEAR-CANDIDATE` / `AMBIGUOUS-HOLD`,
same CI/placebo/DSR/halves limbs) — no new gate mechanic invented for this construct. Today's actual
gate is §1: **blocked**, pending §9.

---

## §9 — Governance: what needs operator approval, and in what order

This is not K-free the way `Q-ICTEXP-1`/`Q-ICTSTOP-1` were — those were one-way falsifiers on an
*already-existing* population with no GO state by construction. OTE is a genuinely new entry-geometry
construct with a real (if small) GO state, so it is priced like CON-4/CON-5: `K_intrinsic=1` once a
manifest opens, not $0/K=0 throughout.

**Two paths exist. Nothing below is authorized by this document alone.**

1. **Operator override (fast, has direct precedent today).** File a fresh ADR — same shape as
   [`2026-08-20-dense1m-u1-operator-override-con4-reopen.md`](../../adr/2026-08-20-dense1m-u1-operator-override-con4-reopen.md)
   — marking a bounded, named exception for `Q-ICT-OTE-1` specifically, on authority alone, no new
   modality claimed. **What you'd be approving:** admitting a construct whose own stop-geometry
   analysis (§2.4) already flags it as CON-5-shaped risk, immediately after CON-4's CONFIRM
   reconfirmed the pause's rationale for the tenth-adjacent time. Cost if I run it and it fails: one
   more zero-yield close in the same thread, same as CON-4 just was. Cost if it passes: a real,
   distinguishing result — the concept-ranking pass placed OTE first among the four wider-ICT
   candidates specifically because nothing else scored as well on population *and* had a
   non-catastrophic-on-its-face cost geometry.
2. **Wait for a genuine new modality.** Per both governing ADRs, this means order-flow/microstructure
   data or a construct that names no entry level at all (like `Q-TODVOL-1`'s volatility-threshold
   design, which escaped on construct-type grounds without needing an override) — not a timeframe
   change, which §0 already ruled out as an escape for OTE specifically.

**If you approve path 1, the concrete next steps are, in order:**
1. I author the override ADR (≈30 min, mirrors the CON-4 template).
2. Parent-side cheap falsifier on the existing reused MNQ 1m panel — <5 min, $0, generous by design
   (per `lesson_run_cheap_falsifier_before_authoring`), specifically testing the stop-geometry risk
   named in §2.4 before anything else.
3. If the cheap falsifier doesn't kill it outright, freeze `PREREG_G0` + your explore GO, then score
   EXPLORATION exactly as CON-4/CON-5 were scored.

**Nothing past step 1 happens without a separate explore GO from you**, per this corpus's standing
discipline (cheap-falsifier and G0-freeze steps don't themselves license scoring).

---

## §10 — Audit hooks (runnable)

```bash
# This scoping must not have opened a manifest or scaffolded a CON-6 directory:
ls discovery_manifests/ | grep -iE "ict.ote|ote.1"
test -d lab/analysis/c1/mnq_tnec_con6* && echo "VIOLATION: CON-6 scaffolded" || echo "OK: no CON-6"

# The two governing ADRs must still read as quoted in §0:
grep -n "absence of named entry geometry" docs/adr/2026-08-15-analogue-modality-route-ruling.md
grep -n "dense-1m G=10 universe" docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md

# Reused machinery must still be byte-identical (this scoping never edits it):
git diff HEAD -- lab/analysis/_inbox/ict_mnq_2026-08/run_1m_diag.py lab/archive/ict_cascade_2026-06-18/

# Dedup re-check before any future re-authoring:
python scripts/check_advisor_dedup.py --keywords "optimal trade entry OTE fibonacci retracement"
```

---

## Amendment log (append-only)

- **2026-08-20 — SCOPED.** Not run, not pre-registered, no K bound, no manifest, $0 committed.
  Authored at operator instruction following the ICT concept-gap ranking pass. §1 states the
  governance blocker up front, not as a caveat at the end.
- **2026-08-20b — OPERATOR OVERRIDE GRANTED, then STOP same day.** Operator approved an override ADR
  ([`Accepted`](../../adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md)); its Phase 1
  cheap falsifier ran and returned `FALSIFIED` — decisive, both arms powered and CI entirely below 0,
  mean stop_dist (13.16pt) confirming this document's own §2.4 prediction. `PREREG_G0` never frozen;
  no K spent beyond the $0 falsifier; no mechanism id registered. STOP — re-proposal needs new
  mechanism evidence, not a parameter retune (§5).
