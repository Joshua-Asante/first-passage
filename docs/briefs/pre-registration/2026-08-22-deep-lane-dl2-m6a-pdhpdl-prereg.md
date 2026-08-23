# DL-2 — deep-lane campaign 2 pre-registration: prior-session breakout continuation on AUD (6A-train / M6A-confirm)

**Status:** `FROZEN` — operator GO (JA) 2026-08-22 ("GO on freeze"). §1–§6 below are binding; no
amendment after this mark (Trap #12 — a change closes this campaign and opens a fresh one under
the lane's counters). Path recorded on the [charter](../../adr/2026-08-16-deep-iteration-lane-charter.md)
running-count line.
**The GO mark adjudicates the one remaining gathered operator item (Verification block),
confirmed back to the operator before the mark — standing-pause reading**: the D2a-grounded
attestation (§0) is accepted as discharging the CON-5 pause for this campaign. **The mechanism-id
item was RESOLVED earlier in this same session** (operator decision, on the ox-alpha second
opinion): declared `NEW` (`prior-session-breakout-continuation`), not reused — §1, `MECHANISMS.md`,
and Change history.
**This mark also serves as:** (a) the W4 dormancy ADR's required re-arm GO (dated after
2026-08-07, naming the SPA threshold p≤0.10 — §6 step 2b); (b) authorization for §6 **step 1
only** (the two staged $0 pulls, mechanical) and **step 2** (train scoring + nomination gates
2a–2d) to proceed. **It does NOT authorize the confirm read** — per this session's own standing
instruction, confirm-read is its own separate operator mark, asked for again once — and only if
— the nominee clears every step-2 gate.
**Prior drafting record (unchanged by this mark):** drafted `Proposed` 2026-08-22 on "GO on M6A
× pdh-pdl-breakout-rth — draft the prereg"; adversarially reviewed the same session (6-lens,
findings applied); given a sanitized ox-alpha second opinion (`2026-08-22-ox-alpha-adversarial-lens-scope.md`),
on which the operator reversed the mechanism-id election to `NEW`. Full detail in Change history.
**Authored:** 2026-08-22 · Claude Code (JA commission — sourcing session, family converged
2026-08-22; charter §7 step 1)
**Lane:** `deep` (second campaign under the [deep-iteration lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md),
`Accepted` 2026-08-16, amended 2026-08-22 by the [two-ledger K ADR](../../adr/2026-08-22-grow0-two-ledger-k-question.md)
§2.2(iv); GO-2 K ≈ 10)
**Mechanism id:** `prior-session-breakout-continuation` — **`NEW`**, added to
[`MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) in this same session (per the growth
rule: "declares NEW... lands here in the SAME COMMIT as the pre-registration that introduced
it"). Declared NEW rather than reusing `pdh-pdl-breakout-rth` (this document's own first-draft
election) after an ox-alpha sanitized second opinion argued the reuse defaulted the wrong way —
see §1 for the full reasoning and Change history for the decision record.
**Authorizes:** nothing. Pre-registration ≠ run. The train pull, iteration, nomination, confirm
read, and every downstream step fire only after a **separate** freeze GO, in the §6 order, and
the confirm is read exactly once.

---

## §0 — Rule-0 reads (this session @ `2cefd3c`, 2026-08-22)

| Source | Anchor | Supplies |
|---|---|---|
| [Deep-lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md) | `7e56f81` | §2.1–§2.7 campaign requirements; GO-2 "reserving the K=33 corner for a family that has earned it" — nothing has, so this campaign also declares K≈10; §4 counting machinery (DL-1 sits at abandoned 1/2, active campaign none) |
| [Two-ledger K ADR](../../adr/2026-08-22-grow0-two-ledger-k-question.md) | `7e56f81` | §2.2(iv) sealed-consultation disclosure — new fourth conjunct, disclosure-only, channel-agnostic query over `burned_segments`; first campaign obligated under it (DL-1 predates it) |
| [`lab/research_utils/axis_screen.py`](../../../lab/research_utils/axis_screen.py) | executed this session | **Conjunct (i):** K=10 ≤ 33 ✓. **Conjunct (ii):** `floor_at_k(10, years=7.6386)` = **1.170** ≤ 2.0 ✓ (confirm window 2019-01-01→2026-08-22, computed live, not assumed). **Conjunct (iii):** Gaussian-approx power, se=1/√7.6386=0.3617: target 1.8 → **0.9592** ≥ 0.50 ✓ (0.9659 at 1.83; 0.8827 even at 1.6) |
| [MSL design-box ADR](../../adr/2026-08-13-msl-slate-2-design-box.md) + [re-derivation](../../notes/notice/N-2026-08-13-msl-design-box-rederivation.md) | `027a729` / `1f3a2bb` | Target geometry (rr∈[2,3], WR 0.30–0.42, hard stop, k=1, no pyramiding, non-index instrument set MGC·MCL·M6A); §9 audit-hook formula re-executed live this session at M6A's **corrected** RT $2.60 (cheaper than every instrument the note itself priced — see the `core/firm_rules.py` row below, not a coincidental match to the note's own "index micros" cell as this document's first draft claimed) |
| [`ops/instruments/M6A.md`](../../../ops/instruments/M6A.md) | `f3b1cd1` | Stage-1 Currencies SURVIVOR/FLAG-COSTBIND, Stage-2 ex-FOMC POWER-bind (A1/A2 — a *different* statistic than this campaign's own cost-law check, kept unconflated per the same-units attestation rule below); Q-TNEC-ENV-1 census authored **no M6A entry** for any mechanism (A4); no `cells:` row registered — every mechanism id is genuinely untested here, including this campaign's own (§1). **A1's own RT figure ($2.82, at $0.91/side) is not used here — corrected against `core/firm_rules.py` directly, next row: the true M6A commission is lower.** |
| [`core/firm_rules.py`](../../../core/firm_rules.py) | L230–233, executed this session | **Correction to M6A.md #A1, caught this session by adversarial review.** The comment block publishing Tradeify's commission schedule states round-trip all-in **$1.60 for M6E/M6A** (a distinct, cheaper FX-micros group), not the $1.82 index-micros figure ($0.91/side) `M6A.md` A1 and this document's first draft both used. Per-side: $1.60/2 = **$0.80**. Corrected M6A RT (commission + 1-tick slip at tick_value $1.00) = 2×$0.80 + $1.00 = **$2.60**, not $2.82. The $0.91/side error traces to `lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md`, which applied one flat commission across M2K/MCL/M6A/MGC alike — already caught and fixed for MGC (→ $1.06/side, RT $4.12, DL-1's own cost pin) but never fixed for M6A until this review. **This document uses the corrected $2.60 throughout (§3/§4/§6); `M6A.md` itself is not edited by this prereg — the error is disclosed here as forward work owed to that ledger, not silently repaired elsewhere.** |
| [`ops/instruments/MECHANISMS.md`](../../../ops/instruments/MECHANISMS.md) | `385bdbf` pre-edit; `NEW` entry added this session, own commit | `pdh-pdl-breakout-rth` id definition + its one prior score (MNQ, `AMBIGUOUS-HOLD`) — the nearest existing class, not this construct's own id; `opening-range-continuation` class finding (DL-1's dead family, MYM) confirming this is a **different** family either way, not a re-proposal of DL-1's kill; **this campaign's own id, `prior-session-breakout-continuation`, added `NEW` this session** (§1) |
| [Same-units attestation ADR](../../adr/2026-07-16-adr-same-units-attestation-blind-channel.md) | cited, not re-read this session | A gate discharges only in its own units, at the basis it scores on — governs how §0's M6A.md A1/A2 cost-tax finding (a fraction-of-Clause-N-power-floor statistic) is disclosed here without being blurred into this campaign's own gross/RT cost-law ratio (a different statistic entirely) |
| [DL-1 prereg](2026-08-16-deep-lane-dl1-mgc-orc-prereg.md) | `02a236f` | The one precedent's structure (this file mirrors its §0–§7/§10 shape) and its own abandonment reasons (all 10 variants net-negative on MGC train, SPA p=0.94) — a different instrument and a different mechanism family, so DL-1's kill does not bind this campaign, but its shape (frozen partition, single nomination, one confirm read) is reused verbatim |
| [Charter Databento addendum](../../adr/2026-08-16-deep-iteration-lane-charter.md) | `7e56f81` | `6A.FUT`/`M6A.FUT` **already priced $0.0000** at `ohlcv-1d/1h/1m`, both TRAIN (2010-06-06→2019-01-01) and CONFIRM (2019-01-01→2026-08-16) windows, in the *same* dry-run that covered GC/MGC and CL/MCL — GO-1's cost gate is already discharged for this instrument; no fresh dry-run needed |
| [`lab/discovery/burned_segments.py`](../../../lab/discovery/burned_segments.py) | `fcb4ac7`, executed this session (§2.2(iv) below) | `consultation_count`/`consultation_history` — channel-agnostic, extended per the two-ledger K ADR's own Phase 2 |
| [W4 dormancy ADR](../../adr/2026-08-07-w4-minimal-gate-set-dormancy.md) | cited, unchanged | SPA/StepM re-arm = prereg names thresholds AND operator GO dated after 2026-08-07 → this prereg names p ≤ 0.10 (§6 step 2); a freeze GO on this file is that GO. PBO/CPCV not re-armed — nomination is a single frozen statistic on the full train window, no cross-validated selection, so the PBO leakage-argument row does not fire (same posture as DL-1) |
| [CON-5 timeframe-scope ADR](../../adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md) | read this session (adversarial review caught this document's first draft never cited it) | §2 **D2a, the controlling authority**: "A card that never invokes the paused route needs no D2 falsifier — it is outside the pause's subject matter entirely, **whatever its bar timeframe or data sourcing**. DL-1... is the worked instance." This is an instrument-level ground (no raised bar on M6A to clear) — it does not depend on any mechanism id's own history, which is now moot for this campaign anyway since the mechanism-id decision (§1) means this construct carries no prior use anywhere |

**Executed door-check (charter §2.1, pasted verbatim — exit 0, no bar; re-run under the `NEW`
mechanism id after `instrument_profiles.py build` regenerated `profiles.json`/`PROFILES.md` to
register it):**

```
$ python scripts/instrument_profiles.py build
instrument_profiles: wrote ops/instruments/PROFILES.md + ops/instruments/profiles.json (27 ledger(s))
$ python scripts/instrument_profiles.py cell M6A prior-session-breakout-continuation
=== M6A x prior-session-breakout-continuation ===
ledger: ops/instruments/M6A.md
verdict: untested — no prior on this cell.
cost hurdle: 2.82 USD/round-trip (1-tick slip) (Stage-1 third-leg map Inputs: commission $0.91/side; RT 1t $2.82 / 2t $3.82; cost-tax 1t r=1 = 0.0902 (FLAG-COSTBIND vs own-panel floor 0.0891)) — VERIFY at #A1
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Stage-1 Currencies SURVIVOR under FLAG-COSTBIND — cost-tax binds before the own-panel Clause-N floor on the pooled panel; Stage-2 ex-FOMC flips the binding constraint COST->POWER. [#A1]
prior: Q-TNEC-ENV-1 envelope NON-EMPTY at 20/40/80/160-tick cells (8-tick DEAD on cost); census authored no M6A entry; published FX-fix delta refused as cross-instrument transplant under strategy_harvest Requirement 2. [#A4]
$ echo "exit: $?"
exit: 0
```

**No class-finding line — genuinely blank slate, not merely "untested here."** Because the id is
`NEW`, no instrument anywhere carries a score for it (unlike the old-draft's `pdh-pdl-breakout-rth`
door-check, which surfaced MNQ's `AMBIGUOUS-HOLD` as adjacent context). See §7 item 2 for how the
nearest-class MNQ result is disclosed instead.

**Door-check cost figure superseded.** The pasted output's "cost hurdle: 2.82 USD/round-trip" is
the tool's live, faithful read of `M6A.md` #A1 — reproduced verbatim above, not altered, because
it is what the consult actually printed. That figure is itself the error corrected in §0's
`core/firm_rules.py` row above: this document uses the corrected **$2.60** throughout (§3/§4/§6).
`M6A.md` is not edited by this prereg; the ledger still needs its own correction, disclosed as
forward work.

**No BINDING BAR.** Unlike MGC and MCL, whose door-checks for this same `NEW` id both return
`BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01` (re-run this session for disclosure — the
bar is instrument-scoped in `ops/instruments/<SYM>.md`'s own `bars:` list, so it carries over
identically regardless of which mechanism id is checked — see §7 item 1), M6A's door is clean
outright. This campaign therefore needs no scope-adjudication of that bar (DL-1 needed one,
ratified on its own GO mark) — stated here so a future reader does not assume every deep-lane
prereg carries that adjudication.

**Standing-pause attestation (charter §2.1) — corrected during adversarial review (the first
draft's ground (ii) was factually wrong and is withdrawn, not silently fixed), and simplified
again after the mechanism-id decision made part of that correction moot.** The dense-1m OHLCV
temporal-selectivity/entry-geometry pause (Branch A, U0 KEEP re-affirmed 2026-08-15) — the same
pause the charter elsewhere calls the "CON-5 θ-parameterised entry-geometry pause" (one pause,
two names; confirmed, no second pause exists) — is attested non-binding here on the **D2a ground**
([CON-5 timeframe-scope ADR](../../adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
§2, already `Accepted`, cited directly rather than re-argued): "A card that never invokes the
paused route needs no D2 falsifier — it is outside the pause's subject matter entirely, whatever
its bar timeframe or data sourcing." M6A carries **no** index raised bar to clear (§0 door-check
— exit 0, no BINDING BAR at all), so there is no occasion for this campaign to invoke route ①.
D2a names DL-1 as "the worked instance" of exactly this — non-index, no raised bar, route ①
never invoked.

**Why the earlier correction (arguing about `pdh-pdl-breakout-rth`'s own route-① history) is now
moot, not just fixed.** The first draft's withdrawn ground (ii) claimed the *mechanism id itself*
never used route ① — false, since its one prior score (MNQ `Q-TNEC-CON-4`) needed route ① to
clear the index raised bar there. That correction mattered while this campaign was instantiating
the *shared* id. Now that §1 declares a `NEW` id (`prior-session-breakout-continuation`) with no
prior use anywhere, there is no mechanism-history question left to argue about at all — D2a's
own test is purely instrument-level (does *this campaign* need route ① on *this* population),
and the answer is no regardless of any sibling id's history. The correction is preserved here as
a disclosed record of what the first draft got wrong, not because it still does argumentative
work.

**Channel-origin attestation (charter §2.1):** internally-generated family. `prior-session-breakout-continuation`
is a `NEW` estate registry id authored in this same session, as the full-session generalization
of the existing `pdh-pdl-breakout-rth` id (`NEW 2026-08-10`, MSL-CON-4 sourcing) — not an
externally-published seed either way; harvest intake and its limb-2 counter are not touched. The
construction (§1) is original to this prereg, not a citable published cohort.

**Dedup attestation (executed, sub-rule 8 — rescoped during adversarial review: the first draft's
`grep ... docs/ lab/CATALOG.md` self-matched this document's own untracked file once it existed
on disk, the same defect DL-1's own dedup grep avoided by scoping to specific pre-existing
surfaces only; re-run here on that narrower, DL-1-mirroring scope):**

```
$ grep -rniE "M6A.*(pdh|pdl|breakout|prior.day)|(pdh|pdl).*breakout.*M6A" \
    lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
(empty)
$ grep -rlniE "pdh.pdl.breakout.rth" docs/rejected_candidates.md
(empty)
$ grep -rniE "prior.session.breakout.continuation" \
    lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
(empty)
```

No prior work on this (instrument, mechanism) pair, and no prior use anywhere of the `NEW` id
itself, on any of the searched surfaces. Per the standing lesson (an empty grep is not evidence
of no prior work), this is corroborated by the door-check's own `verdict: untested — no prior on
this cell` (both under the nearest-existing-class name during scoping and under the `NEW` id
itself, post-election) and by `M6A.md`'s `cells:` list carrying zero rows — independent surfaces
agree, not one.

**§2.2(iv) — sealed-consultation disclosure (new conjunct, disclosure-only, executed this
session):**

```
$ python -c "
import sys; sys.path.insert(0,'lab')
from discovery.burned_segments import consultation_count, consultation_history
print('M6A confirm window (2019-01-01..2026-08-22):', consultation_count('M6A','2019-01-01','2026-08-22'))
print('M6A history:', consultation_history('M6A','2019-01-01','2026-08-22'))
print('6A train window (2010-06-06..2019-01-01):', consultation_count('6A','2010-06-06','2019-01-01'))
"
M6A confirm window (2019-01-01..2026-08-22): 0
M6A history: []
6A train window (2010-06-06..2019-01-01): 0
```

`M = 0` on both partitions, queried channel-agnostically over the whole ledger (not deep-lane-scoped
per the two-ledger K ADR's own correction). `burned_segments.json` carries exactly one entry
estate-wide (MNQ, 2025-09-01→2026-08-05, from the dual-panel review — unrelated instrument and
window). This is the cleanest possible disclosure state, not merely a passing one: this campaign
is the first to touch this family-K bank at all (no `discovery_manifests/` entry exists for 6A or
M6A on any prior campaign either — checked, empty), so unlike DL-1 (GC/MGC family bank 3,177,
disclosed per Req-3) there is no cross-campaign bank to disclose beyond this M=0 reading.

---

## §1 — The family (one mechanism, one instrument, frozen)

**Prior-session breakout continuation on AUD/USD (M6A).** After the prior CME Globex trading
session closes, a break of that session's high or low, confirmed by a subsequent session close
beyond the level, tends to continue in the break direction. All structure below is frozen; only
the §2 variant axes are searched.

**Mechanism id — declared `NEW`, resolved by operator decision, 2026-08-22.** This campaign uses
`prior-session-breakout-continuation`, a full-Globex-session generalization of the registered
`pdh-pdl-breakout-rth` id, added to `MECHANISMS.md` in this same session. **This document's own
first draft elected the opposite** — reuse `pdh-pdl-breakout-rth` rather than mint a new id, on
the reasoning that the *trigger logic* (close-beyond-prior-extreme, enter next bar, structural
stop at the opposite extreme) is unchanged and only the *window that logic operates over* is
instrument-appropriate rather than transplanted. That election was flagged, not settled, as an
explicit operator-adjudicated item, because the repo's own registry convention runs the other
way: `overnight-range-failed-extension-fade` was minted as a **new, sibling** id (2026-08-13)
from `pdh-pdl-failed-break-reclaim` for the structurally identical move — swapping "prior-day
RTH" for "Globex overnight" as the reference window while holding every other element fixed —
and its own "rejected nearest classes" line states the split turns on exactly that swap.

**Reversed after a sanitized ox-alpha second opinion** (`2026-08-22-ox-alpha-adversarial-lens-scope.md`,
sent a genericized version of exactly this question with no repo-specific content): independently,
via "jingle fallacy" framing (same label, different construct, if the reference window is
definitional rather than incidental — which it is here, since the window determines which price
events count as the reference level at all), it concluded reuse is "a real labeling problem"
given this repo's own precedent, and that "the burden of justification flips" toward minting a
new label by default. The operator weighed this against the first draft's reasoning and elected
to declare `NEW` — see Change history for the decision record.

**Roll-day lookback rule (frozen; a genuine ambiguity the design-box precedent never faced,
caught during adversarial review — `opening-range-continuation` has no prior-session-lookback
concept to seed, so DL-1 never needed this rule).** If the session that would serve as the
lookback reference (§2's 1- or 2-session window) was itself excluded as a roll day (§3's stitch
rule), the reference level is instead taken from the last non-roll session **before** it — a
roll-day session never seeds a PDH/PDL level, only its own entries are suppressed. This keeps the
reference level anchored to a session with no leader-switch seam in its own OHLC.

**Session definition — a genuine construction choice, stated and reasoned, not imported.**
M6A trades on a near-continuous CME Globex clock (daily 17:00–16:00 CT session with a ~60min
maintenance break), not an equity cash session. `MCL.md` W3 warns explicitly against certifying
non-equity instruments against an assumed equity-RTH window ("do not treat equity-RTH PASS as
Energy-session validity") — the same risk applies here a fortiori, since AUD/USD's most liquid
hours are Asia/London, not the 09:30–16:00 ET window every other `pdh-pdl-breakout-rth` /
`pdh-pdl-failed-break-reclaim` construct in this estate has used. Rather than transplant an
equity convention or invent an untested Asia-session boundary, this campaign uses the
**venue-native full Globex trading day** as the sole session unit — objectively derivable from
the exchange calendar and the feed's own timestamps, importing no assumption about which hours
are "active":

- **Session boundary:** 18:00 ET (previous calendar day) → 17:00 ET (current calendar day) — the
  ET-converted CME Globex daily session (17:00 CT → 16:00 CT next day).
- **Force-flat:** 16:55 ET (5 minutes before the daily rollover/maintenance break, mirroring
  DL-1's own 5-minutes-before-boundary convention).
- **Entry:** first valid signal per session only (≤1 entry per day; k=1 by construction; no
  re-entry, no reverse).
- **Initial hard stop:** opposite prior-period extreme (structural; rr defined by geometry). No
  trail, no BE move, no pyramiding, no scale-in/out (EM3-clean).
- **Target:** fixed multiple of the realized per-trade risk (2R or 3R per variant), else flat at
  16:55 ET. rr∈[2,3], expected WR 0.30–0.42 → the design-box archetype.
- **Roll days:** sessions containing a front-month volume-roll are excluded from entries (M6A/6A
  roll quarterly, IMM cycle) — frozen stitch rule imported verbatim from DISC-CAMP-0/DL-1: front
  month = per-UTC-day `ohlcv-1d` volume leader, outrights only; a roll day = the day the leader
  changes.
- **FOMC/RBA days are NOT excluded** (unlike MCL's `CONFIG-B-MCL` convention). Disclosed
  limitation, not a forbidden move: this construct has no announcement-window story to exclude
  against, and adding an exclusion axis not present in the design-box precedent would smuggle an
  undeclared fifth axis into K. If event-day volatility drives the result, the confirm-halves
  fragility check (§6 step 3) is the control that would catch it.

## §2 — The frozen variant set (K_intrinsic = 10; the axes ARE the search)

| V | Lookback | Drift filter | Entry style | Target |
|---|---|---|---|---|
| 1 | 1 session | unconditional | close-confirm | 2R |
| 2 | 1 session | unconditional | close-confirm | 3R |
| 3 | 1 session | aligned | close-confirm | 2R |
| 4 | 1 session | aligned | close-confirm | 3R |
| 5 | 2 sessions | unconditional | close-confirm | 2R |
| 6 | 2 sessions | unconditional | close-confirm | 3R |
| 7 | 2 sessions | aligned | close-confirm | 3R |
| 8 | 1 session | aligned | retest-limit | 2R |
| 9 | 2 sessions | aligned | retest-limit | 3R |
| 10 | 1 session | unconditional | retest-limit | 2R |

- **Lookback:** the "prior period" whose high/low defines the breakout level — either the single
  immediately-prior session (canonical PDH/PDL) or the high/low across the prior **2** sessions
  (a wider structural level, still "prior extreme", not a different mechanism — the direct analog
  of DL-1's OR-window axis, which varied lookback length while holding the OR/PDH-PDL concept
  fixed).
- **Drift filter:** `unconditional` (either side) or `aligned` — take the break only if in the
  same direction as the lookback period's own realized drift, `sign(lookback-window's last
  session close − lookback-window's first session open)` (self-referential; no external data,
  same discipline as DL-1's drift filter).
- **Entry style:** `close-confirm` — per the registered mechanism id: first session close beyond
  the level → enter next 1m bar's open (+1 tick, mirrored for shorts). `retest-limit` — after the
  close-confirm trigger fires, rest a limit order at the broken level itself (long: buy-limit at
  the broken high; short: sell-limit at the broken low) instead of entering at next-open; filled
  if price returns to the level before session flat, otherwise no trade that session (same
  execution-style axis DL-1 used for its retest variants — same mechanism, different fill).
- **Target:** fixed multiple of realized risk, 2R or 3R.

**Closed set.** No variant may be added, retuned, or substituted after any train number is seen
(D-K1 imported verbatim). Iteration = scoring these ten on train and diagnosing; it never mints
an eleventh.

**Disclosed axis-coverage imbalance in the curated 10 (caught by the ox-alpha sanitized-lens
second opinion, `2026-08-22-ox-alpha-adversarial-lens-scope.md`, reconciled against this table).**
The 10 rows are not a balanced fraction of the 16-cell full factorial: entry style splits
7 (close-confirm) : 3 (retest-limit); lookback splits 6 (1-session) : 4 (2-session); drift filter
and target split evenly 5:5. This mirrors DL-1's own identically-shaped curation (lens 2's finding
during adversarial review — "structurally isomorphic," a copied template, not an optimized-for-DL-2
subset) but does not make the imbalance itself harmless: in a flat argmax-of-10 nomination (§6
step 2), a setting sampled at more cells has more chances to win purely by cell count, independent
of true edge. **This is not corrected here** — doing so would mean redesigning the frozen K=10
grid past what the freeze GO addressed — but it is named as a genuine, disclosed limitation of the
nomination procedure, not a discovered defect that blocks freezing: the SPA gate (§6 step 2b,
below) is the control that actually protects against this, since it tests the nominee against the
full 10-variant universe regardless of which cells that universe over- or under-samples.

## §3 — Data and the frozen partition (charter §2.3)

| Partition | Symbols | Window | Phase | Schema | Priced |
|---|---|---|---|---|---|
| **TRAIN** | `6A.FUT` (parent; front-month series assembled per the frozen stitch rule below) | 2010-06-06 → 2019-01-01 | `discovery` (boundary-enforced by `db_fetch.py`) | `ohlcv-1m` | $0.0000 (charter addendum, §0) |
| **CONFIRM** | `M6A.FUT` (native micro; same stitch rule) | 2019-01-01 → 2026-08-22 (**7.6386 y**) | `oos` | `ohlcv-1m` | $0.0000 (charter addendum, §0) |

- **Frozen stitch rule (both partitions, imported verbatim from DISC-CAMP-0/DL-1):** front month
  = per-UTC-day `ohlcv-1d` volume leader, outrights only; a roll day = the day the leader changes
  (excluded from entries per §1). No back-adjustment anywhere: all levels, entries, exits, and
  P&L use the actual contract's prices (the PDH/PDL is a level object; the roll-day exclusion
  handles the seam).
- **All iteration feedback reads TRAIN only.** The confirm partition is read **once**, on the
  single nominee, after the §6 step-2 gates. Per-variant confirm results are never computed.
- **Proxy discipline (M6A, corrected cost basis):** 6A-parent train re-scaled to micro specs at
  scoring (M6A tick_value $1.00; RT **$2.60** at 1-tick slip — corrected from M6A.md's own $2.82
  figure this session; see §0).

**Frozen scoring conventions (each pinned here before any train number is seen):**

1. **The statistic** ("net annSR" everywhere in this prereg): Sharpe of the **daily net P&L
   series** — CME trading calendar, flat days included as zeros — annualized by **√252**,
   computed identically on train and confirm. Maps to `floor_at_k`'s f=1.0 row, same convention
   as DL-1.
2. **Sizing for the P&L series:** 1 contract per trade, costs $/contract. N-SURV sizing (§6 step
   5) is a separate, downstream question — this statistic is edge-shape only.
3. **Cost pin (pass/fail):** RT **$2.60**/contract (`core/firm_rules.py` L230–233, $0.80/side
   commission + $1.00 tick_value at 1-tick slip — corrected against the canonical live-sizing
   source, not M6A.md's own $2.82 figure; see §0) on both partitions.
4. **Fill engine (1m bars):** entries at stop/limit price ± 1 tick (or bar open if the bar gaps
   through, for `close-confirm` variants); **adverse-first same-bar resolution** (if one 1m bar
   touches both stop and target, the stop fills); stop exits at stop price − 1 tick slip
   (mirrored for shorts); target exits at target price; 16:55 ET force-flat at bar close.

Pull commands staged (fire only on freeze GO, `--campaign-id DL2-M6A-PDHPDL`, cache era-tagged
by phase):

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols 6A.FUT --stype parent \
  --schema ohlcv-1m --start 2010-06-06 --end 2019-01-01 --phase discovery \
  --campaign-id DL2-M6A-PDHPDL --max-cost 1.00
PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols M6A.FUT --stype parent \
  --schema ohlcv-1m --start 2019-01-01 --end 2026-08-22 --phase oos \
  --campaign-id DL2-M6A-PDHPDL --max-cost 1.00
```

## §4 — Falsifiable hypothesis and the named design target

**Design-target edge (named a priori, conjunct iii):** confirm-partition net annualized Sharpe
**1.8** for the nominee — the same design point DL-1 used, marginally below the charter's GO-2
point (true-1.83), conservative in the binding direction. Power at the actual 7.6386y confirm:
**0.9592** at 1.8 (0.9659 at 1.83; 0.8827 even at 1.6). The charter's own §6 honesty clause
stands unchanged: the lane demands a mechanism materially better than anything measured in the
futures era, and a true-at-the-bar edge is a coin flip — this prereg bets on the design target,
disclosed as such.

**Cost-law pre-arithmetic (family-selection stage, charter §2.5), re-executed this session at
the corrected RT.** At the design-box point p=0.35/rr=3 (gross expectancy m₀=0.40R), M6A's
**corrected** RT $2.60 (not the $2.82 first draft used — see §0; M6A is now the **cheapest** of
the three design-box instruments, not tied with the index-micro cell): **R_max $181.29, net m
0.3857R, μ/trade $69.92, n≈85.8 trades to the $6,000 target, all-win day $541.27 (clears the
$200 payability floor), worst single-trade+cost $183.89.** The nomination gate's own ≥4×
cost-law check (§6 step 2a) requires the nominee's realized stop ≥ **26.0 ticks** at this design
point (`4 × $2.60 / (0.40 × $1.00 tick_value)`) — a modest bar for a currency whose typical
session range comfortably exceeds it, disclosed as a sanity pre-check on unverified real-world
range data, not a guarantee; the actual gate re-checks against realized train geometry, never
this arithmetic.

**Not gameable by position sizing (clarified after the ox-alpha review asked the natural
question of a fixed-cost/scalable-edge gate).** Size is fixed at 1 contract per trade (§3); the
free quantity in the ≥4× check is stop width (ticks), which is a market-realized quantity read
off the actual prior-period range each session, not a knob chosen to clear the gate. The
inequality cannot be satisfied by "sizing up" — there is nothing to size up.

**H:** the train-nominated variant achieves confirm net annSR ≥ **1.170** (= DSR ≥ 0.95 at K=10
on the 7.6386y confirm) **AND** both confirm halves (split **2022-10-27**, frozen; per-half floor
**SR > 0**, frozen — charter §2.4 fragility control) are positive.
**H fails** (a lane **strike**, 1 of the 2-campaign falsification budget — DL-1's own abandonment
does not count toward this budget per charter §4(c)) if the nominee is read and misses either
limb — including the `FALSIFIED-FRAGILE` shape (pooled pass, half fail).
**Abandonment** (dated on the charter, no strike, consecutive-abandonment counter — currently
1/2 from DL-1) if the **nominee** — the train-annSR argmax, the only variant the gates are ever
applied to — fails any §6 step-2 gate, so the confirm is never read. There is no fallback
nomination.

## §5 — Forbidden moves

- **Reading confirm during iteration**, computing any per-variant confirm number, or
  re-nominating after the read. One nominee, one read, ever.
- **Touching the variant set** after any train number is seen (add/retune/substitute — D-K1).
- **Moving the session boundary, force-flat time, roll rule, or split date** after seeing
  results.
- **Instrument-hopping.** The door-check was also run on MGC and MCL (same `NEW` mechanism id)
  before election; both carry the `free-data-5th-leg-snag-closed-2026-07-01` bar M6A does not. M6A was
  elected on its clean door plus its (corrected) cost geometry being the cheapest of the three
  design-box instruments — switching instruments later is a new campaign under the lane's counters, never an amendment of
  this one.
- **Adding an event-day (FOMC/RBA) exclusion axis mid-campaign.** Named as a genuinely tempting
  move in §1 (MCL's own `CONFIG-B` precedent excludes FOMC days) and explicitly declined at
  freeze to avoid an undeclared fifth axis — if it turns out to matter, that is what the
  confirm-halves fragility check is for, not a mid-campaign patch.
- **Quoting train-side numbers as evidence of edge.** Train output is selection apparatus; only
  the confirm read carries evidential weight (reporting-burns-holdout discipline).

## §6 — Frozen procedure and gate

| Step | What happens | Gate (frozen) |
|---|---|---|
| 1. Pulls | Both staged pulls fire (`--max-cost 1.00` each; estimates already $0.0000 per the charter's own addendum) | mechanical |
| 2. Train + nomination | All 10 variants scored on TRAIN under the §3 frozen conventions. **Nominee = argmax train net annSR, full stop — no fallback, no walk-down.** If the nominee fails **any** gate below, the campaign **ABANDONS**; a lower-ranked variant is never promoted. **Nomination gates, all train-only, all on the nominee:** (a) train net annSR > 0 AND cost-law ratio ≥ **4×** at the nominee's realized train geometry (pre-arithmetic above: realized median stop ≥ ~26.0 ticks at the design point; the realized-train-geometry check is binding because the structural stop's width is data-dependent); (b) survives **SPA (Hansen) consistent p ≤ 0.10** against the full 10-variant universe — pinned implementation: loss series = daily net P&L per §3, benchmark = zero-return series, Politis–Romano stationary bootstrap, expected block length **20 days**, B = **10,000**, RNG seed **11** (the W4 re-arm this prereg names — a fresh seed, not DL-1's 7, to avoid any appearance of a copied draw across unrelated instruments); (c) the **nominee's** measured train cadence ≥ **1 trade/week** (N-ACT) — PDH/PDL breaks fire on most trending sessions, a materially higher-frequency trigger than the pullback-failure construct that died on this exact gate on MCL (0.511 trades/week), but this is measured fresh, not assumed; (d) the nominee's train net annSR stays > 0 at +1 tick/side additional slip (M-16) | nominee fails any gate ⇒ **ABANDONMENT** (dated, no strike) |
| 3. Confirm read | Once, nominee only, native M6A 2019-01-01→2026-08-22 | net annSR ≥ **1.170** AND halves (2022-10-27) both > 0 ⇒ **SURVIVOR**; else **STRIKE** (1 of 2) |
| 4. Cost-law recheck | At the nominee's realized confirm geometry ($2.60 pin, corrected — §0/§3) | ratio ≥ 4× or the SURVIVOR is demoted to **STRIKE** — same charter §4 H composition ("confirm + cost-law + N-SURV") DL-1's own freeze GO ratified; this freeze GO ratifies the identical mapping for this campaign |
| 5. N-SURV scoring | Frozen survivor gate (intraday-honest bust ≤ 3.0% ∧ P(pass) ≥ 50%), **flat-R primary**; any policy/cushion-sizing arm reported as disclosure only, per DL-1's own forbidden-move precedent (§5) | frozen 2026-07-13 prereg, byte-untouched |
| 6. Anchor + intake | Native-TV anchor, then lifecycle intake at SURVIVAL-ONLY / WATCH-1; every further step (Pine, TV, arming) under its own operator GO | charter §2.5, unchanged |

**Verdict vocabulary:** `SURVIVOR` / `STRIKE` / `ABANDONMENT` per the charter §4 counting
machinery; every outcome is recorded on the charter's canonical running-count line with a date.
Roster mapping (INDEX/closure surfaces): SURVIVOR closes `RESOLVED`; STRIKE closes `FALSIFIED`;
ABANDONMENT closes `AMBIGUOUS` (confirm never read).

## §7 — Adverse priors and instrument-hopping disclosure (engaged, not routed around)

1. **No BINDING BAR** (§0). The general 5th-leg free-data-expansion programme this bar polices
   still exists estate-wide — disclosed for completeness — but its door-check does not attach to
   M6A for this mechanism, so no scope-adjudication is owed on this freeze GO (unlike DL-1's).
2. **No prior anywhere under this campaign's own id — a genuinely blank slate, disclosed as
   such, not dressed up as corroboration.** `prior-session-breakout-continuation` is `NEW`; no
   instrument carries a score for it. The **nearest existing class**, `pdh-pdl-breakout-rth`,
   has one prior score — MNQ (index), `AMBIGUOUS-HOLD` (long −0.007R / short +0.005R, CIs
   straddle zero, gross/(4×RT)≈0.27×) — disclosed here as adjacent context, not this construct's
   own prior: it was scored under equity-RTH reference/entry-window semantics this campaign
   deliberately does not use (§1), on an index instrument, at MNQ's own parameterization rather
   than the design-box's rr∈[2,3] geometry. Neither a kill nor a corroboration transfers cleanly.
3. **Not the same family as DL-1's kill.** `opening-range-continuation` (DL-1, MGC, abandoned —
   all 10 variants train-net-negative) anchors to the *current session's own* opening range;
   `prior-session-breakout-continuation` anchors to the *prior* session's full range and requires
   a close confirmation before entry. `MECHANISMS.md`'s own registry cross-references both as
   distinct "rejected nearest classes" of each other — this is not a retune of DL-1's dead
   construct wearing a new instrument, and the mechanism-id decision (§1) does not change that.
4. **Currencies-class cost-tightness finding (M6A.md A1/A2), disclosed and kept unconflated.**
   Cost-tax 0.0902 sits *above* the Stage-1 pooled-panel Clause-N power floor (0.0891, hence
   `FLAG-COSTBIND`) but *below* the Stage-2 ex-FOMC floor (0.0924, hence a COST→POWER flip
   ex-FOMC). That statistic answers a different question (blind-mining cost-tax as a fraction of
   a search-power floor) than this campaign's own gross-edge/RT cost-law ratio (§4, computed at
   ≥4× the realized stop). Per the same-units attestation rule, the A1/A2 finding is disclosed
   here as context, not substituted for this campaign's own §6 step-2a gate, and does not by
   itself indicate this construct will fail that gate.
5. **M6A's only instrument-specific rejection** — `P3-4 MULTI-FIX-FX` (event-window FX-fix
   transplant, `UNSCREENABLE(δ)`) — is a different mechanism family (scheduled-fix flow, not
   structural through-break) and does not bind.
6. **Instrument-hopping, engaged directly (charter §5 concern; also §5 above).** The identical
   door-check was run on MGC and MCL for this exact `NEW` mechanism id before election; both
   return the free-data bar M6A does not. This is stated as the honest reason M6A, not merely as a
   convenient fact: a cleaner door is a real procedural advantage (no scope-adjudication owed)
   but is not itself evidence of edge, and is not being cited as such anywhere in §4's H.
7. **No locked-book transfer precedent exists on M6A** (unlike MGC's Guardian-transfer
   `DEAD(N-SURV)` adverse prior DL-1 had to price) — there is nothing analogous to disclose here;
   named so a future reader does not wonder why this section is shorter than DL-1's.

---

## §10 — Audit hooks

```bash
# Conjuncts reproduce (constants frozen):
python -c "import sys; sys.path.insert(0,'lab'); from research_utils import axis_screen as a; print(round(a.floor_at_k(10, years=7.6386),3))"
# Expected: 1.17

# Door-check output unchanged since this prereg (re-run before freeze GO):
python scripts/instrument_profiles.py cell M6A prior-session-breakout-continuation

# NEW mechanism id landed in MECHANISMS.md (growth rule: same commit as this prereg):
grep -n "^## prior-session-breakout-continuation$" ops/instruments/MECHANISMS.md

# §2.2(iv) disclosure reproduces (M=0 both partitions, as of this drafting):
python -c "
import sys; sys.path.insert(0,'lab')
from discovery.burned_segments import consultation_count
print(consultation_count('M6A','2019-01-01','2026-08-22'), consultation_count('6A','2010-06-06','2019-01-01'))
"
# Expected: 0 0

# Frozen split integrity (this file, post-freeze — no amendment to §2/§3/§4/§6):
git log --oneline -- docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md

# Charter count line carries this campaign after freeze GO:
grep -n "Running counts (canonical, this ADR)" docs/adr/2026-08-16-deep-iteration-lane-charter.md

# Confirm never read before nomination (cache era-tagging):
ls ~/.databento_cache 2>/dev/null | grep -i dl2 || echo "no DL2 pulls yet"
```

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md --type inquire
# RESULT (executed 2026-08-22): 0 HARD violation(s), 0 WARN violation(s), well-formed.
# NOTE: repo-side checker = mechanical subset only (its own banner says so, per DL-1's own
# precedent) — form-only, not a substitute for substantive review.
```

**Adversarial review — completed this session, not skipped.** The `pre-ratification-adversarial-panel`
skill's own Workflow invocation failed on a harness-side error (persistent across 3 retries, not
an input problem — the tool's own error confirmed "the tool input from the model was valid").
Rather than skip the gate, its phases were replicated directly: 6 independent refute-first
Agent-tool lenses (Rule-0/citation accuracy; K/multiplicity arithmetic; mechanism-construction
validity; standing-pause/bar/dedup completeness; cost-law arithmetic; forbidden-moves/gate
bindingness) each read the target plus its cited doctrine and searched for genuine BLOCKERs.
**Findings, all applied to this document (not merely logged):**
- **BLOCKER (cost-law lens):** the RT cost pin was wrong — $2.82 (index-micros commission rate)
  instead of M6A's own $2.60 (`core/firm_rules.py` L230–233, FX-micros commission group).
  Corrected throughout §0/§3/§4/§6; `M6A.md`'s own A1 finding carries the same error, disclosed
  as forward work, not edited here.
- **BLOCKER (pause/bar lens):** the standing-pause attestation's ground (ii) falsely claimed
  `pdh-pdl-breakout-rth` never uses route ① — its one prior use (MNQ `Q-TNEC-CON-4`) did, to
  clear the index raised bar. Corrected to the actually-controlling, already-ratified authority
  (CON-5 timeframe-scope ADR §2 D2a: a campaign with no raised bar of its own never invokes the
  paused route, independent of the mechanism id's history elsewhere).
- **BLOCKER (mechanism-construction lens), two findings:** (a) the session-window substitution
  (equity RTH → full Globex session) may warrant a `NEW` MECHANISMS.md id under this repo's own
  `overnight-range-failed-extension-fade` precedent — reframed as an explicit operator-adjudicated
  item (Status block) rather than a settled claim; (b) roll-day sessions' role in seeding the
  lookback level was undefined — a frozen skip-back rule added to §1.
- **Minor (citation-accuracy lens):** the dedup grep's first draft would self-match this
  document's own file once written to disk (docs/ is too broad a scope) — rescoped to the three
  specific pre-existing surfaces DL-1's own dedup grep used, re-run, confirmed empty.
- **NO BLOCKERS** from the K/multiplicity-arithmetic lens (all three conjuncts, §2.2(iv), and the
  cross-campaign counting claim re-derived exactly) or the forbidden-moves/gate-bindingness lens
  (§5/§6/charter-compliance all checked out).
- Two immaterial rounding discrepancies ($180.70 vs $180.69, $183.52 vs $183.51 in the
  pre-correction arithmetic) were superseded by the cost-pin correction itself, which
  re-executed all downstream figures fresh rather than patching the old ones.

This satisfies the substance of DL-1's own precedent (adversarial review before presenting a
freeze candidate) even though the named skill's own orchestration tool failed; the failure and
the substitute method are disclosed here, not hidden.

**Ox-alpha sanitized-lens second opinion (per `2026-08-22-ox-alpha-adversarial-lens-scope.md`,
run after the above, reconciled against this real document — not logged as a finding until
checked).** Four sanitized, genericized questions (10-of-16 curation fairness; the cost-law
inequality; mechanism-id reuse; the pause/route scope logic) were sent to `stealth/ox-alpha` via
the OpenRouter chat-completions API, zero repo/tool access, no proprietary numbers/names/dates.
**Applied:** the 7:3/6:4 axis-coverage imbalance in the K=10 grid (§2, above — a genuine finding
my own 6-lens review missed) and a clarifying note that the cost-law gate is not
position-size-gameable (§4, above). **Checked and found not to apply, once reconciled:** its
"no multiplicity plan for nomination" objection — already discharged by §6 step 2b's SPA gate,
invisible to the sanitized excerpt since only the four targeted questions were sent, not the full
gate table; its "no-resurrection rule" objection — already discharged by the existing D-K1
forbidden move. **Independently reinforces, via different reasoning ("jingle fallacy" — same
label measuring a different regime; "the burden of justification flips" given the repo's own
precedent), the mechanism-id operator item already named in the Status block** — flagged
explicitly, not silently absorbed, since the operator's earlier standing GO on that specific item
preceded this second opinion.

**Operator decision on the mechanism-id item, 2026-08-22 (resolves the flag immediately
above).** Presented with ox-alpha's reasoning, the operator elected to declare `NEW`
(`prior-session-breakout-continuation`) rather than proceed with the already-accepted reuse of
`pdh-pdl-breakout-rth` — an explicit reversal of a standing GO on this specific point, made
before any freeze, train pull, or score. This document, `MECHANISMS.md`
(`prior-session-breakout-continuation` entry, cross-referenced both ways with
`pdh-pdl-breakout-rth`), and `ops/instruments/PROFILES.md`/`profiles.json` (regenerated via
`instrument_profiles.py build`) were updated throughout in the same pass — every citation of the
old id as *this campaign's own* mechanism was changed; citations of it as the *nearest existing
class* / adjacent prior (§0, §7 item 2) were kept, since that comparison is still the honest
basis for the split. The operator separately noted ox-alpha should be leaned on going forward
given its combination of capability and (current, free-tier) cost — noted here as the reason this
second-opinion step is likely to recur on future campaigns, not asserted as a standing policy
change (the governing ADR's own scope and forbidden moves are unchanged by that preference).

§0 production reads with executed anchors incl. the pasted door-check (exit 0, no bar) and the
fresh dedup (empty) ✓ · §1 session-definition choice stated and reasoned against the MCL.md W3
equity-RTH-transplant risk, not silently inherited ✓ · §2 ten frozen variants, closed set ✓ · §3
partition frozen, cost pin corrected against `core/firm_rules.py` (not taken from the ledger's
own stale figure), pulls staged not fired ✓ · §4 H binary with
named design target + cost-law pre-arithmetic computed live ✓ · §5 forbidden moves include a
genuinely tempting one (FOMC exclusion) explicitly declined, not a strawman list ✓ · §6 gates
binary, nomination strict-argmax with no walk-down, SPA implementation pinned with a fresh seed,
scoring conventions frozen ✓ · §7 engages seven adverse/neutral priors with mechanisms, not
dismissals, and states plainly where this campaign's evidentiary basis is *thinner* than DL-1's
(no locked-transfer prior, no BINDING BAR to adjudicate, and now no prior score anywhere under
its own mechanism id either) ✓ · §10 runnable ✓ · **mechanism-id operator item RESOLVED (`NEW`
declared, `MECHANISMS.md` updated, document updated throughout); standing-pause reading RESOLVED
on the freeze GO — both operator items closed, this document is `FROZEN`.**

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-22 | Drafted `Proposed` on operator GO ("GO on M6A × pdh-pdl-breakout-rth — draft the prereg"), following the prior turn's sourcing session (family converged: M6A door-check clean vs MGC/MCL's shared bar; dedup empty; §2.2(iv) M=0 on both partitions). | Claude Code (drafter) |
| 2026-08-22 | Adversarial review (6-lens, replicated by hand after the `pre-ratification-adversarial-panel` skill's own Workflow call failed with a harness error). 2 BLOCKER-class defects found and corrected in place: cost pin $2.82→$2.60 (wrong commission group, `core/firm_rules.py`), pause attestation ground (ii) factually wrong (`pdh-pdl-breakout-rth`'s prior MNQ use did invoke route ①; corrected to the actually-controlling CON-5 timeframe-scope ADR §2 D2a). 2 further findings converted to explicit operator-adjudicated items (mechanism-id reuse vs `NEW`; roll-day lookback rule, previously undefined, now frozen in §1). Dedup grep rescoped (self-match defect). Still `Proposed` — not frozen; a separate freeze GO is owed per charter §7 step 1. | Claude Code (drafter, same session) |
| 2026-08-22 | Ox-alpha sanitized second opinion (`2026-08-22-ox-alpha-adversarial-lens-scope.md`), four genericized questions on the axis-curation, cost-law, mechanism-id, and pause-scope reasoning, reconciled against this real document. Applied: disclosed the 7:3/6:4 axis-coverage imbalance in the K=10 grid (§2); clarified the cost-law gate is not position-size-gameable (§4). Checked and found already-discharged: "no multiplicity plan" (§6 step 2b's SPA gate) and "no-resurrection rule" (existing D-K1 move) objections. Reinforced the already-flagged mechanism-id item with independent reasoning, surfaced to the operator despite an already-standing GO on that point. **Operator reversed the standing GO** and elected to declare `NEW` — `prior-session-breakout-continuation` added to `MECHANISMS.md` (cross-referenced both ways with `pdh-pdl-breakout-rth`), `PROFILES.md`/`profiles.json` regenerated, and every citation of the mechanism-id throughout this document updated (§0 door-check/dedup re-run under the new id, §0 pause attestation simplified since the mechanism-history question is now moot, §1, §5, §7 items 2/3/6, §10). Mechanism-id operator item now RESOLVED; standing-pause reading remains the one open item at freeze. Still `Proposed` — not frozen. | Claude Code (drafter, same session) |
| 2026-08-22 | **`Proposed` → `FROZEN` — operator GO ("GO on freeze"), after the operator was asked what the mark decides and confirmed with a direct explanation (pulls + train scoring authorized; confirm-read stays a separate future ask; pause-reading item resolved; W4 SPA re-arm discharged).** | Joshua (GO) + Claude Code |
| 2026-08-22 | **§6 step 1 executed — both pulls fired, both confirmed $0.0000.** TRAIN (`6A.FUT`, parent, `ohlcv-1m`, 2010-06-06→2019-01-01, `--phase discovery`): 3,259,026 rows, cache `ohlcv-1m_parent_628b3020421840e1.dbn`. CONFIRM (`M6A.FUT`, parent, `ohlcv-1m`, 2019-01-01→2026-08-22, `--phase oos`): 2,110,056 rows, cache `ohlcv-1m_parent_01f8f1910c17eb9f.dbn`. Both under the `DL2-M6A-PDHPDL` campaign id, `--max-cost 1.00` cap never approached. Matches the charter's own GO-1 dry-run promise exactly — no surprise cost. **Confirm partition cached but not read** — §5's forbidden-move discipline applies to *scoring* it, not to the mechanical fact of its bytes being on disk (same posture DL-1's own pull-then-abandon precedent established). Step 2 (train scoring + nomination) is the next work item, not yet started. | Claude Code (mechanical step, same freeze-GO authorization) |
