# B2 / B3 / B4 draft code changes — Q-ICT-CASCADE-1

**Date:** 2026-06-18
**Status:** DRAFT — uncompiled, untested. Starting point for the next session.
**Applies to:** the `.pine` files needing *measurement-correctness* edits (B2/B3, no discretion) **plus the B4 DOL-target re-spec** (D1 definitional choice — the design's recommended option (a); default-on after the **operator anti-SNAG override 2026-06-18**, `nearest-pool` retained as a selectable variant).
**Parent:** [TEST_PLAN.md](TEST_PLAN.md) §7.A blockers B2, B3, B4.

> **Where the drafts live:** `lab/analysis/ict_cascade_2026-06-18/pine_drafts/` — these are copies of the
> Downloads originals with the edits below applied. `.pine` is gitignored (`.gitignore:75`, private-Pine
> posture), so the drafts are **on-disk only, NOT committed**; this changelog is the committed, reconstructable
> record. **The Downloads originals were NOT modified.** Re-anchor before trusting line numbers — the
> Downloads files are mutable (TEST_PLAN.md §0).

---

## What was changed (3 files, all measurement-correctness — no faithfulness/definitional change)

### 1. `constellation_ict_lib.pine` — B3 / D-1 (CRITICAL, B-measurement)

**Function `markTouchedFVGs` (was lib:125).** Guard the near-edge touch test so an FVG cannot be
marked "touched" on its own registration bar:

```pine
// before:  if not f.touched
// after:   if not f.touched and barIdx > f.bar
```

**Why:** a bull FVG's near edge is `f.top = low[0]`, and `markTouchedFVGs` runs on the same bar the FVG is
pushed, so `lo <= f.top` = `low <= low[0]` is *always true* at age 0 → every FVG scored an instant hit →
`fvgRate` pinned at ~100% and the Daily miss-branch was dead code. The guard requires a strictly-later bar,
so only a genuine *return* to the near edge counts (this implements Appendix-B ambiguity #FVG-edge option (a):
touch = first later bar reaching the near edge).

**Blast radius:** the Daily draw-rate only. The 1M execution calls `markTouchedFVGs` but does **not** gate
entries on `f.touched` (it uses `freshBull`/`freshBear`), so 1M behavior is unchanged. `markFilledFVGs` was
**not** touched — far-edge fill cannot self-trigger (registration requires `low[0] > high[2] = f.bot`, so
`lo <= f.bot` is false on bar 0). Verified against the audit (D-1 verification, far-edge confirmed clean).

### 2. `ict_weekly_bias.pine` — B2-W (CRITICAL, C-faithfulness: restore the transfer claim)

Added a **structure-only `gateBias`** hit-rate alongside the existing composite `bias` hit-rate, because the
1M gate is `structBias`-only (`ict_1m_execution.pine:91-92`) and the composite `bias` (which mixes
seasonal/rates/earnings) is what the table scored — so the printed hit-rate stopped transferring the moment
any vote was enabled (the exact best-of-K importance workflow this script exists to run).

- New block after `hitRate` (drafts ~line 110): `gateBias = vStruct` + its own `priorGateBias` / `gateScored`
  / `gateHit` / `nGateScored` / `nGateHit` / `gateHitRate` accumulators (mirrors the composite scoring).
- Table: resized `2,8 → 2,10`; row 1 relabeled `"hit-rate" → "hit% (composite)"`; added rows 8/9
  `GATE hit% (live)` + `GATE n` (lime = the object-correct number; see the leg-a/leg-b caveat below).
- Exports: added `gateBias`, `gateHit`, `gateScored`, and `scored` to the data window. The `scored`/`gateScored`
  flags fix the missed-defect where the `hit`/`gateHit` columns collapse miss + stand-down + flat all into 0
  (the harness must recompute the denominator from these flags, not `mean(hit)`).

**Scope of the fix — leg (a) vs leg (b).** W-1 has two legs: (a) the table scored the COMPOSITE vote, not the
`structBias` OBJECT the gate uses; (b) the W metric scores a WEEKLY-CLOSE outcome, while the gate filters
per-minute entries. `gateBias` fixes **leg (a) only** — it is the object-correct number to cite, but it remains
a **weekly-close proxy** for per-entry gate accuracy. Leg (b) is the separate offline gate-transfer probe
(TEST_PLAN §7.B W-6). Also: `gateHitRate` only transfers when `emaLen == the 1M wEmaLen` (both default 20) —
pin this before any importance sweep desyncs them.

**Still owed (not in this draft):** W-2 rates-repaint fix (`request.security(rateSym,"W",close[1],…)`), needed
only before the rates vote enters the importance test.

### 3. `ict_1h_premium_discount.pine` — B2-1H (CRITICAL, C-faithfulness: the LAG half of the transfer test)

Added a **gate-basis `zoneGate`** computed on the `[1]`-lagged lookback-extremes range
(`ta.highest/lowest(lookN)[1]`) — the basis the 1M PD gate actually uses — plus an on-chart `zone agree%`
counter (sign-agreement between the native `[0]`-fresh `zone` and `zoneGate`).

- New block after the `zone`/`eq` assignment (drafts ~line 59): `rHighGate`/`rLowGate` (`[1]`-lagged),
  `gateValid`, `zoneGate`, `zoneAgree`, `agreeTot`/`agreeOk`, `agreeRate`.
- Table: resized `2,6 → 2,8`; added rows 6/7 `zoneGate ([1]-lag)` + `zone agree%`.
- Exports: added `zoneGate`, `zoneAgree`.

**Scope / limitation (read this):** this isolates only the **range-lag** axis of the transfer gap
(`[0]`-fresh vs `[1]`-lagged). The **price-basis** axis (the gate scores a *1-min* close, this script a *1H*
close) **cannot** be reproduced on a 1H chart and stays an **offline** reconstruction against the paired 1M
export (TEST_PLAN §7.B 1H step 5). `zone agree%` is only meaningful if `lookN` here == the 1M `pdLookN`
(both default 60) — set them equal before reading it.

### 4. `ict_1m_execution.pine` — B4 / D1 (HIGH, D-operational: fix the trade-starvation)

**Definitional change, unblocked by the operator anti-SNAG override (2026-06-18).** Re-spec the `useDOL=true`
target from the **nearest unswept opposing pool** (which starved n → `skip:cost/R` dominates → unfalsifiable) to
the **opposing dealing-range extreme** — the design's own recommended **D1(a)** (`ICT_SYSTEM_DESIGN_1.md` §11 D1).
`nearest-pool` is retained as a selectable, quarantined variant (non-destructive).

- New input `dolMode` (`range-extreme` | `nearest-pool`, default **range-extreme**) in group `gT`, after `useDOL`;
  `useDOL` label updated ("opposing liquidity — see DOL target mode").
- LONG target: `dolPx = dolMode == "nearest-pool" ? ict.nearestPoolPx(pools, entryEst, true) : h1High`
  (`h1High` = the 1H range high already computed earlier for the PD gate — `:94` original / `:96` draft); `noDraw = useDOL and (na(dolPx) or dolPx <= entryEst)`
  (reject a range high already taken out → no draw up).
- SHORT target: symmetric on `h1Low`; `noDraw = … or dolPx >= entryEst`.

**Why this is the keystone:** the audit's E1 starvation (B4) + the ledger's F8 tradeability floor both say the
nearest-pool target can't pay; the range-extreme target gives a meaningful R and unifies the target with the P/D
range the gate already computes. `h1High`/`h1Low` are `[1]`-lagged HTF values (non-repaint).

**Dissent that now binds the test (ledger F8):** because the 1M layer is the FALSIFIED-D2 geometry family, the
E[R] test MUST use a **multi-regime window + block-resample by entry event + the `stop_dist ≥ max(1pt,cost)` floor**
— a single benign window would reproduce D2's failure (drop-top-k carried). A §8 pre-reg constraint, not optional.

**Multiplicity guard (D1 review).** `dolMode` adds a 4th selectable axis (range-extreme vs nearest-pool) on top of
`useDOL` on/off. To prevent a selection leak, **`nearest-pool` is pre-registered REPORT-ONLY** — it does not enter
the lock decision or consume a best-of-K / permutation budget (§8 `PREREG-dolMode`; marked in the input tooltip).

**Mirror-risk (D1 review).** A *far* range-extreme TP may rarely be **reached** on a 1m chart before the stop/limit
resolves (the opposite of nearest-pool's too-close problem), depressing WR — the F8 multi-regime + drop-top-k E[R]
test is the right mitigation and is already mandated.

**Compile note:** the `dolMode == "nearest-pool" ? nearestPoolPx(...) : h1High` ternary conditionally evaluates
`nearestPoolPx` — safe because it is a pure array function (no `ta.*`/series state), so skipping it on
range-extreme bars cannot corrupt history. **Pending TV-compile verification** like the rest.

### 5. `ict_1m_execution.pine` — Killzone / session gate (B-killzone; C-faithfulness fix for E2)

ICT is killzone-bound; the strategy traded 24h (audit E2). Added an **ablatable ET killzone gate** on the
RAID/arm. **Drafted at operator request (ET-displaying); reviewed independently → SHIP-WITH-NITS.**

- New group `gKZ`: master `useKillzone` (default on) + 3 killzones, each a toggle + `input.session`:
  **London Open** `0200-0500` (on), **NY AM** `0700-1000` (on), **NY PM** `1330-1600` (off). All ET.
- `inLO/inNYam/inNYpm = useX and not na(time(timeframe.period, kzX, "America/New_York"))`; `inKZ = or`;
  `killzoneOK = not useKillzone or inKZ`. Added `and killzoneOK` to both arm conditions. Table row 11 + `inKZ` export.
- **DST-safe (the load-bearing bit):** `America/New_York` resolves the windows in NY wall-clock with automatic
  EST↔EDT, so they match the ET-displaying chart year-round — resolves the repo's fixed-UTC-4 trap
  ([[platform-display-tz-edt]]). More correct than the locked DJ30/NAS `hour(time,"UTC")` pattern (those windows
  are authored in UTC; these in ET).
- **Gating granularity (disclosed):** gates the **arm** (raid), not the entry/limit — so the FVG entry can fire
  ≤ `raidWin` bars (≈8 min) after the window closes ("hunt in-zone, entry follows"). Trades tag by **arm-time**
  zone; the §6 one-slice test slices by arm time to match.
- **Multiplicity (booked):** `useKillzone` makes the gate-ablation **2³ = 8 runs**; the zone set + windows are
  **FROZEN, not swept** (§8 `PREREG-killzone`) — not a best-of-K surface.

---

## What was deliberately NOT changed (and why)

- **B3 / D-2 (pool back-stamp clock) and D-3 (base-rate null)** — these are **offline-analysis** fixes, not
  single-script Pine edits. D-2's blind window is unrecoverable in Pine (the pool doesn't exist in the registry
  during its `pvLen` confirmation lag, so a same-bar scan can't see sweeps that already happened); both are
  done in the offline harness per TEST_PLAN §7.B (D steps 2-3). Left for the offline session.
- **B1 (FVG orientation) — RESOLVED 2026-06-18** (orientation fixture → standard-ICT, objection-gated; TEST_PLAN
  §7.A B1). **B4 (DOL target) — DRAFTED above** (design D1(a) default; independently reviewed → SHIP-WITH-NITS,
  nits folded). **B5 (`pvLen`) — PINNED 2026-06-18** per-layer (1M=2 LOCK in the draft tooltip / Daily=3 provisional /
  1H=5 exploration-only; §7.A B5, §8). **Killzone/session filter — DRAFTED 2026-06-18** (new §5 below; ET via
  `America/New_York`, DST-safe; reviewed SHIP-WITH-NITS). On the Pine side, only the **offline-only** D-2/D-3
  (above) remain.
- **The `<your_tv_username>/constellation_ict_lib/1` import placeholder** — pre-existing in all four consumers;
  unchanged. The drafts **will not compile** until the library is published Private and the username substituted
  (or the primitives inlined). This is a setup step, not a logic defect.

---

## Apply / verify (next session)

1. **Do B1 first.** No draft verdict is interpretable until FVG orientation is signed off (TEST_PLAN §7.A B1).
2. Publish `constellation_ict_lib.pine` (with the D-1 edit) Private on TV; substitute `<your_tv_username>`;
   confirm `/1` version in the three consumers.
3. Compile the three drafts on a TV chart (W on Weekly, 1H on 1H). Expect compile-clean apart from a benign
   "unused variable `eg`" warning in the 1H gate block.
4. **D-1 falsifier:** on the Daily (which imports the patched lib), confirm the `FVG draw-rate` table cell is
   now **< 100%** (was pinned at 100.0%). That single number is the fastest check the fix worked.
5. **B2-W:** with all votes off, `GATE hit%` should equal the old composite `hit%`; with a vote on, they diverge
   — confirming the composite was not the gate.
6. **B2-1H:** set `lookN == pdLookN`; read `zone agree%` as the lag-component transfer number; then do the
   price-basis half offline against the 1M export.

## Adversarial review (2026-06-18)

Independent Pine v6 review of the three drafts + this changelog. **Verdict: SHIP-WITH-NITS.** Confirmed correct:
D-1 fully neutralizes the registration-bar self-touch in both wick/body and bull/bear with no missed legitimate
touch; `markFilledFVGs` correctly left untouched (far-edge self-fill already impossible); the blast radius is
genuinely Daily-only (the 1M sets `touched` but never reads it — entries use `freshBull`/`freshBear`, and
`nearestFVG` keys on `filled` not `touched` and is Daily-only); W `gateBias`/`priorGateBias` is the same
object/lag/EMA as the 1M `structBias` gate; 1H `zoneGate` correctly expresses the `[1]`-lagged range;
`zoneAgree`/`agreeRate` scoped correctly; both tables in-bounds (≤100 cells); all `plot()`/`var` at global
scope; int/int rate divisions are float. **One nit (fixed above):** the W comment/changelog overclaimed
"transfers" — refined to leg-a (object) vs leg-b (per-entry, offline) plus the `emaLen == wEmaLen` pin.

**B4/D1 1M draft — separately reviewed 2026-06-18 → SHIP-WITH-NITS.** Independent pass confirmed: `h1High`/`h1Low` non-repaint + correct orientation (long→high, short→low); the `dolMode` ternary conditionally evaluates the pure `nearestPoolPx` array-fn safely (no `ta.*`/series state); `noDraw` (`<=`/`>=`) precludes a zero `targetR` with the `minAbsR=2.0` backstop; the `useDOL=off` ablation arm is intact. Two nits FOLDED: `dolMode`/`nearest-pool` pre-registered **REPORT-ONLY** (multiplicity guard) + the stale `:94` line-ref corrected. Still **pending TV-compile verification** like the rest.

**Killzone gate — separately reviewed 2026-06-18 → SHIP-WITH-NITS.** Code + DST correct (`time(tf,session,"America/New_York")` valid + na-safe, sessions valid, table in bounds, `America/New_York` auto EST↔EDT matches the ET chart). Three non-code gaps FIXED: §8 `PREREG-killzone` books the 8-run ablation + freezes the zone set/windows; the arm-only entry-spill (≤raidWin) is disclosed (tooltip + comment); the §6 one-slice test tags by arm-time. Pending TV-compile.

---

## Verification (run record)

```bash
# Drafts exist and are gitignored (not committed — private-Pine posture):
$ git check-ignore lab/analysis/ict_cascade_2026-06-18/pine_drafts/constellation_ict_lib.pine
#   -> path echoed = ignored (correct)

# Confirm the D-1 guard landed in the draft lib:
$ grep -n "barIdx > f.bar" lab/analysis/ict_cascade_2026-06-18/pine_drafts/constellation_ict_lib.pine

# Confirm the gate columns landed:
$ grep -n "gateBias\|gateHitRate" lab/analysis/ict_cascade_2026-06-18/pine_drafts/ict_weekly_bias.pine
$ grep -n "zoneGate\|agreeRate" lab/analysis/ict_cascade_2026-06-18/pine_drafts/ict_1h_premium_discount.pine

# Downloads originals UNCHANGED (last-write must still match TEST_PLAN §0 anchors):
$ # PowerShell: Get-ChildItem 'C:\Users\joshu\Downloads\*ict*.pine' | Select Name,LastWriteTimeUtc
```
