# Q-TODVOL-1 — `tod-baseline-range-trigger` — causal G0 freeze + D2 pre-G0 falsifier pre-registration

**Frozen:** 2026-08-20, before any signal is scored. Byte-unedited from this point forward —
amendments via a fresh Q, never an in-place edit (brief-authoring Known Trap #12).
**Authority:** operator direction, this session ("write it up as a proper causally-named G0
freeze and then check whether it can actually be tested"), following up on
[`ADR 2026-08-10`](../../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)'s
route-① opening for within-instrument temporal selectivity.
**Status:** PRE-G0 — this freeze licenses the D2 cheap falsifier only. A full G0/Explore campaign
under a fresh Q-ID is a separate, later step, gated on D2 passing.

---

## §0 — Rule 0 reads + domain-bar consult (this session)

- [`docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md`](../../../../docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md)
  §2-A/§2-B — route ① OPEN to within-instrument temporal selectivity, under conditions: criterion
  causally named a priori and frozen at G0 (never chosen after seeing which moments performed);
  every axis charges `K_intrinsic`; nothing downstream weakened.
- [`docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md`](../../../../docs/briefs/closures/DENSE1M-UNPAUSE-closure-resolved-u0-keep.md)
  — U0 KEEP, 2026-08-15: the **dense-1m (1-minute MNQ, G=10) lane** stays paused. This freeze runs
  on **native 15m RTH bars** — a different timeframe, explicitly outside that lane's own defining
  scope (`docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md:22`, "the dense-1m G=10
  universe"). Not a CON-6; no `Q-TNEC-CON-6` opened; the dense-1m pause is not touched.
- [`docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md`](../../../../docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md)
  §2 D1/D2 — a card outside the dense-1m lane may invoke route ①, but only after clearing the
  **frozen D2 pre-G0 cheap falsifier** (reused verbatim below, not re-derived). This freeze is
  exactly that card.
- `ops/instruments/MECHANISMS.md` — `tod-baseline-range-trigger` declared **NEW**, same commit as
  this freeze. Nearest-class comparison recorded there (`compression-gated-breakout`,
  `intraday-momentum`, `opening-range-breakout`, PDH/PDL and VWAP-reclaim classes,
  `opening-pressure`) — none share this class's time-of-day-conditioned volatility-baseline
  trigger with no compression precondition and no reference price level.
- Domain-bar consult, executed this session:
  ```
  $ python scripts/instrument_profiles.py cell MNQ tod-baseline-range-trigger
  BINDING BAR: index-intraday-ohlcv-directional-timing-2026-07-21 -> ../../docs/rejected_candidates.md
  ```
  **Answered:** route ① (mechanism outside the mapped cost-ratio levers — price / cross-instrument
  selection / hold-time). Within-instrument temporal selectivity was ruled outside that mapped set
  by the 2026-08-10 ADR; this card additionally clears the 2026-08-16 ADR's timeframe-scope
  condition by construction (15m, not 1m) and is gated by that ADR's own D2 falsifier, run below.
- Panel check, this session: `lab/analysis/orb/orb_mnq_2026-07/_mnq_15m.pkl` (via the primary
  checkout, same fallback path `run_evalseq_orb_intraday.py` already uses) — 1,857 RTH sessions,
  26 fifteen-minute slots/session (09:30–15:45 ET), span 2019-05-05 → 2026-07-15. Structure check
  only (session count, time-of-day grid) — no return/PnL number read before this freeze.

---

## §1 — Causal story (the a-priori argument, before any score is seen)

Volatility clustering — serial dependence in the *magnitude* of price moves, independent of
their sign — is a broadly-corroborated market-microstructure regularity (ARCH/GARCH-class
canon; this estate's own `daily-range-state-persistence` class finds it at the DAILY grain on
GC/CL). At the intraday, single-session grain, a bar whose range meaningfully exceeds its own
historical norm **for that specific time-of-day slot** is a real-time-observable signal that
unusual information or order flow has just arrived at that moment — distinct from a fixed clock
window (ORB's first-N-bars) or a static reference price level (PDH/PDL, VWAP, London/overnight
range). The trigger is "when is something happening right now, relative to what usually happens
at this point in the session," not "where is price relative to a level."

This shares a causal family with `intraday-momentum` (Baltussen-class, already killed on modern
MNQ — N3) but is not a re-run of it: that class tested a fixed-lag prior-bar/prior-session
momentum claim; this class conditions entry *timing* on a real-time volatility-threshold event,
with no claim about yesterday's or the prior bar's direction.

---

## §2 — Frozen construction (single cell; `K_intrinsic = 1`)

No sweep. No parameter left to pick after seeing a result. Exactly these values:

| Parameter | Frozen value | Rationale (stated, not derived from any score) |
|---|---|---|
| Instrument / timeframe | MNQ, native 15m RTH bars, Tradeify geometry | Same panel/instrument as ORB-MNQ-1 and the CON/MSL family; 15m keeps this outside the paused dense-1m lane |
| Excluded window | First 2 bars (09:30–10:00 ET) | Matches ORB-MNQ-1's own `or_bars=2` opening-range definition — avoids mechanically triggering on the naturally elevated first bars and avoids overlapping ORB-MNQ-1's own territory |
| Trailing baseline | Median range at the **same time-of-day slot**, trailing **60 sessions**, causal (`.shift(1)`, no look-ahead) | 60 sessions (~3 months) is long enough for a stable per-slot median, short enough to adapt; comparable order of magnitude to other trailing windows already used in this estate (Q-ORBCUSH-1's 20/63/126-session set) |
| Threshold multiple `θ` | **2.0×** the trailing per-slot median range | A round, standard "meaningfully large" multiple; not tuned |
| Trigger | First eligible bar (after the excluded window) whose range ≥ `θ × baseline` for its own slot | First valid signal per session only (k=1), matching the domain's own trade-count economics finding |
| Direction | Trigger bar's own close-vs-open sign | No separate direction parameter |
| Stop | 1.0× the trigger bar's own range, opposite side of entry | Tied to the same real-time-observable quantity that triggers entry — avoids introducing an independent, untethered point-count parameter |
| Target | 2.0× the trigger bar's own range, trade direction (`rr = 2`) | Matches the `rr ∈ [2,3]` convention already standing for this estate's continuation-shaped constructs |
| Exit discipline | Session-flat, k=1 | Matches every other MNQ mechanism class in this estate |

**`K_intrinsic = 1`** — one cell, no threshold/window sweep. Well within the domain ADR's
EM0 ≤ 3 / working-budget-1–2 ceiling.

---

## §3 — D2 pre-G0 cheap falsifier (frozen spec, reused verbatim from the 2026-08-16 ADR §2 D2 — not re-derived)

- **Test:** on this construct's own IS panel only (no CONFIRM split touched at this stage), compute
  mean signed gross points per triggered signal, using the frozen stop/target box above — not
  re-tuned for this test.
- **Pass bar:** `mean signed gross ≥ 0.5 × (4 × RT_frac)` — half of the standard 4× cost hurdle,
  in points, at this panel's own cost basis. Generous by design (`lesson_run_cheap_falsifier_before_authoring`)
  so a FAIL is conclusive.
- **Report:** coverage % (sessions with a valid trigger), n, mean signed gross, the 4×RT hurdle in
  matching units, and WR — the same four figures CON-5's own closure reported, for direct
  comparability.
- **Cost:** $0, no `register_search open`, no Q-ID spend beyond this freeze's own `K_intrinsic=1`,
  no CONFIRM read.

**Pass/fail rule:** if mean signed gross misses the bar, this closes route ① for this construct
shape at $0 — no G0, no Board debate, exactly how CON-1..5 themselves were closed. If it clears,
that licenses a **full G0/Explore campaign under a fresh Q-ID** (not this freeze) — the D2 pass
is necessary, not sufficient; Req 1a, delete/flip, cost-law, and every other requirement still
bind in full at that later step.

---

## §4 — Forbidden moves

- **Re-tuning `θ`, the 60-session lookback, or the stop/target multiples after seeing the D2
  result.** A miss is a miss (Known Trap #12).
- **Treating a D2 PASS as a G0 freeze, an admitted candidate, or any downstream gate discharge.**
  It is a pre-G0 door-check only, per the 2026-08-16 ADR §5.
- **Reading this freeze as reopening the dense-1m lane** (untouched; U0 KEEP stands) or any of
  CON-1..5's own findings.
- **Widening this to a sweep** (multiple `θ`/lookback cells) to "give it a better chance." One
  cell, `K_intrinsic=1`, as frozen above.

---

## Verification

```bash
python scripts/instrument_profiles.py cell MNQ tod-baseline-range-trigger
# Expected: BINDING BAR line present, answered above in §0

rg -n "tod-baseline-range-trigger" ops/instruments/MECHANISMS.md
# Expected: NEW entry present, same commit as this freeze

git log --oneline lab/analysis/c1/todvol_1_2026-08-20/FREEZE.md
# Expected: this freeze commit predates any results file in this directory
```
