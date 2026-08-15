# Scoping + seed manifest — RATES-EV-ZF-1: 08:30-release event-day breakout on 5Y Treasury futures (ZF)

**Status:** `CLOSED — FALSIFIED at Phase-0` (2026-07-21). Operator GO recorded (§8); Databento ZF pull `$0.00`; K=0 consumed (the pre-committed PRIMARY+SECONDARY design never opened `register_search`). **P0.2 cost-law KILL (headline 1.15× vs 4.0× bar) and P0.4 power FAIL (0.30 vs 0.50)** on the full CPI+NFP cohort. Mixed, informative result: **P0.1 instrument-choice thesis VALIDATED** (17.6:1 event-day range/RT, vs ZB's unconditional 4.3:1) and **P0.5 decorrelation thesis VALIDATED** (ρ=0.28, zero-padded) — but the edge itself is marginal (gross t=1.45) and consumed by realistic cost; per-year sign alternates (same noise signature as NG-EIA-1). Closes the program's rates-event 2×2 matrix fully dead. Phase-1 never reached. Results: [`lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md`](../../../lab/archive/rates_ev_zf_recon_2026-07/RESULTS.md). Disposition: append to [`rejected_candidates.md`](../../rejected_candidates.md); lock HELD (no `core/`/allocation/`dd_protection`/Pine touch).
**Candidate:** RATES-EV-ZF-1 — the ORB-MNQ-1 opening-range-breakout construct, applied **only on CPI/NFP announcement days**, on the CBOT 5-Year T-Note future (ZF), anchored at the 08:30 ET release.
**Lane:** venue-native reconstruction / cross-instrument transplant (kin to ORB-MNQ-1 and today's ORB-ZB-1, `CLOSED FALSIFIED`) **crossed with** the event-conditioning class (kin to H-ZNAUC-1/F-B, both `CLOSED SCREEN-FAIL`). This is the **one untested cell** in that 2×2 matrix — see §1.
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-20 · Claude (Sonnet 5), operator-directed (post-brainstorm workflow selection).

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-20)

- **`discovery_manifests/*.json` (all 7, listed this session)** — no ZB/ZN/ZF/ZT manifest exists ⇒ **entire Treasury-complex family K_banked = 0** (`ls discovery_manifests/`, verified 2026-07-20). **K-family-grouping judgment, disclosed:** ZB and ZN were both tested this program (ORB-ZB-1 breakout; H-ZNAUC-1 auction-drift) but **neither consumed K** — both closed as no-K measurements (ORB-ZB-1: Phase-0 δ-extraction, not a registered search; H-ZNAUC-1: "K consumed 0... no manifest opened" per its own closure). Whether ZB/ZN/ZF should be treated as one "Treasury-complex" family or three separate instrument families is a genuine open question this brief does not resolve — under **either** reading the floor stands: combined-family K_eff (this candidate's K_intrinsic, see §2) + 0 banked ≤ 3 ⇒ floor ≤0.98; separate-family reading gives an even more permissive floor. The verdict is unaffected either way; flagged for honesty, not because it changes anything.
- **[`lab/archive/orb_zb_recon_2026-07/RESULTS.md`](../../../lab/archive/orb_zb_recon_2026-07/RESULTS.md) @ `568c639`** — today's ORB-ZB-1 closure, `CLOSED FALSIFIED`. **The load-bearing negative result this brief is built against:** the ORB-MNQ construct, applied **unconditionally** (every day) on ZB, has **negative gross edge in every window** (full −0.048R), and the within-day placebo (p=0.001) shows breakouts lose on *every* intraday ZB window — Treasuries fade their opening range unconditionally. RATES-EV-ZF-1 does **not** dispute this finding; it tests a **different, narrower claim** — that the breakout survives *only* on the small subset of days carrying a large exogenous information shock (CPI/NFP), where the unconditional-fade regime may not apply. ZB's own median-day cost geometry (10-tick OR vs 2-tick RT, ratio 4.3:1) is also independently the worst on the curve (§0 next bullet) — this brief switches instrument to ZF for that reason, not only the conditioning change.
- **[`lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py`](../../../lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py) @ `b89f9a6`** — the calibration-pinned `orb_backtest`/`placebo_within_day` engine, reused verbatim for the event-day subset (identical discipline to ORB-ZB-1: only the loader + day-filter + `Instrument` economics are new).
- **[`docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md`](../closures/H-ZNAUC-1-closure-screen-fail.md) @ `aa0738d`** — the program's three own-cohort post-event-drift measurements to date, all sub-cost: ZN post-auction δ 1.01bp (vs 6–10bp hurdle), CL post-EIA unconditional δ ~1.16bp (vs 6–10bp), ES overnight drift 1.5bp (vs 5.05bp). **Honest kill-vector, disclosed:** if RATES-EV-ZF-1's measured event-day continuation δ lands anywhere near this ~1–1.5bp band, it fails ZF's hurdle (§2) just as badly as its three predecessors — the construct's entire case rests on event-day range being *categorically* larger than routine post-event drift, not merely somewhat larger.
- **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) @ `7af4224`**, §1 row E1 (line 16): 16:00 ET flat deadline (Treasury futures pit session itself closes 15:00 ET, so this construct clears E1 with an hour to spare by construction). §2 item 4 (line 29): no firm-specific facts in research artifacts — same posture as the sibling NG-EIA-1 brief; ZF firm availability is unverified in-repo and correctly out of scope here.
- **`core/firm_rules.py` @ `a53ee99`** — no ZF row; generic Bulenox `cost_per_side_usd=0.61` convention used, matching ORB-ZB-1/H-ZNAUC-1/NG-EIA-1.
- **[`docs/methodology/strategy_harvest.md`](../../methodology/strategy_harvest.md) @ `268851b`** — §1 Requirement 2: "No citable δ ⇒ UNSCREENABLE → route to a δ-extraction probe or drop; never invent a number." **This candidate is UNSCREENABLE at admission** — no ZF-specific post-announcement-continuation δ exists anywhere in the literature (the adjacent evidence, Brooks-Katz-Lustig NBER WP 25127 on post-FOMC drift in Treasuries, is multi-day-horizon and not intraday, and Fleming-Remolona 1999 documents *initial* adjustment completing within minutes — cutting against, not for, naive immediate entry). Routed to the δ-extraction probe per the Req-2 relief valve, same posture as ORB-ZB-1.
- **[`docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`](../../adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md) @ `7af4224`** — the binding composition gate; this candidate's sparsity (in-market ~24 days/yr) is designed to clear `ρ < 1.0` structurally at any plausible weight (§2 arithmetic).
- **External, WebSearch/WebFetch-verified this session (not repo-internal):**
  - CME public contract specs, cross-verified two independent sources: CBOT ZF (5-Year T-Note) — **$100,000 face value, tick = 1/4 of 1/32 point = $7.8125/contract.** This is the **best tick-geometry instrument on the Treasury curve** for this construct (vs ZB's 1/32 = $31.25/tick and ZN's 1/64 = $15.625/tick) — DV01 ≈ $44, ≈5.6 ticks/bp of yield, roughly 1.5–4× more ticks-per-dollar-of-yield-move than ZB/ZN.
  - **CPI/NFP calendar-sourcing gotcha (memory `reference_bls_release_date_sourcing`, 14 days old at recall — used as a sourcing-discipline pointer, not as a live-data substitute):** `bls.gov` returns HTTP 403 to WebFetch (host-level bot-block); reachable via the claude-in-chrome browser MCP instead. **NFP release dates diverge materially from a "first Friday of month" heuristic** — 2nd Friday in ~5 months 2022–2025, non-Friday 4× (including three 2025–2026 government-shutdown shifts). This is a **direct, load-bearing pre-registration risk** for this brief's event calendar — see §5.

---

## §1 — Context (the symptom this probe addresses)

**The one untested cell.** The 2026-07-20 brainstorm workflow's adversarial screen (23 agents) organized the program's rates-event graveyard into a 2×2: {unconditional, conditional} × {routine drift, event-day breakout}. Three cells are dead with real measurements: **unconditional routine drift** (ZN auction 1.01bp, CL EIA-unconditional 1.16bp, ES overnight 1.5bp — all confirmed-mechanism-but-sub-cost) and **unconditional breakout** (ZB today, negative gross edge — Treasuries fade). The fourth cell — **conditional (top-information days only) × breakout, on the best available curve geometry** — has never been measured. The executioner assigned to kill this candidate in the brainstorm workflow tried and could not do it honestly at the screen stage: every kill argument available is a cross-instrument prior, and the same R2 discipline that forbids the candidate from being *admitted* on a transplanted number forbids the executioner from *killing* it on one either. That is the precise shape of a legitimate δ-extraction candidate, not a pre-judged one.

**Why this might work where ZB's unconditional breakout didn't.** Two independent, additive reasons: (1) **Cost geometry.** ZF's tick is worth 4× less in yield terms than ZB's (5.6 vs 3.7 ticks/bp — wait, more ticks per bp of yield is *better* geometry, i.e. ZF needs a smaller yield move to generate the same tick-count as ZB), giving ZF an event-day range/RT ratio estimated (from the researched CPI/NFP range literature, not yet repo-measured) at roughly 13–16:1 on a median event day and 26–65:1 in the 2022-23 high-surprise era — versus ZB's unconditional 4.3:1. (2) **Conditioning.** CPI/NFP-day ranges run 3–6× a routine day's range; the mechanism this brief tests (duration hedgers and slow-moving institutional capital chasing the post-surprise repricing rather than fading it — Brooks-Katz-Lustig's post-FOMC-drift story, transplanted from FOMC/multi-day to CPI-NFP/intraday, disclosed as an *adjacent*, not on-cohort, grounding) predicts continuation is concentrated exactly on these days, not spread thin across every session the way ZB's unconditional test measured.

**Why the honest prior is still low, not high.** Fleming-Remolona (1999) documents that the *initial* Treasury-price adjustment to a macro surprise completes within minutes — which argues against a naive immediate-entry breakout capturing much, and *for* the specific opening-range-then-follow-through shape this construct uses (the OR forms during/just after the initial adjustment; the trade is on what happens *next*). But the program's three own-cohort post-event measurements (§0) all landed near 1–1.5bp — categorically below any plausible cost hurdle on any Treasury instrument. If CPI/NFP-day continuation behaves like routine post-event drift rather than like a genuine event-day breakout, this candidate dies the same way its predecessors did, just on better geometry. **This is a probe, not a conviction — the asymmetric-payoff justification (near-$0, K≤2, one session) is the entire case for running it, not a claimed edge.**

**Threading the vise (the prize, if it clears).** Sparse by construction (~24 event-days/yr, ~10% of sessions, $0 exposure otherwise) — daily-$std at 1-lot is near-zero on non-event days, giving `ρ ≪ 1` at any plausible weight almost mechanically (unlike ORB-MNQ-1's every-day exposure, which failed exactly this gate). Direction is set by the macro-surprise sign, not equity intraday momentum. And the regime complement is favorable: the book's worst bleed regime (2020-23 chop) contains the richest CPI-day rates ranges in the sample (the 2022-23 CPI cycle) — if there is P&L here at all, it concentrates where the book needs it most.

---

## §2 — Seed manifest (`strategy_harvest.md` §5 template)

```markdown
# Harvest-seed manifest — RATES-EV-ZF-1

- admission-date: 2026-07-20
- requirement-1 path: 1a (named flow) — ADJACENT-EVIDENCE grounding, disclosed
- mechanism (req 1a): after a macro surprise, duration hedgers (MBS
  servicer/portfolio convexity hedging extends duration on selloffs, forcing
  mechanical follow-on selling) and slow-moving institutional capital (bond
  mutual-fund flows) re-price over hours, not at the print -- the loser is
  named (whoever must transact after the initial repricing, in the direction
  of the surprise). Grounding evidence (Brooks-Katz-Lustig NBER WP 25127,
  post-FOMC drift in Treasuries) is MULTI-DAY-HORIZON, not intraday, and
  FOMC-specific, not CPI/NFP-specific -- an adjacent-evidence transplant,
  weaker than an on-cohort intraday citation. Fleming-Remolona (1999,
  peer-reviewed) cuts partly against naive immediate entry (initial
  adjustment completes in minutes) and partly for the OR-then-follow-through
  shape this construct actually uses.
- source + tier: Brooks/Katz/Lustig NBER WP 25127 (SSRN/NBER-WP tier, not
  peer-reviewed-journal tier) for the mechanism; Fleming/Remolona 1999
  (peer-reviewed) for the initial-adjustment-speed caveat. NO source for a
  ZF-specific intraday continuation delta -- see req-2.
- target instrument + family (req 3): ZF (CBOT 5-Year T-Note, full-size).
  Chosen over ZB/ZN/TN on tick geometry (tick=$7.8125, ~5.6 ticks/bp,
  best range/RT ratio on the curve for this construct per §1 research
  estimates -- NOT yet repo-measured, that is what Phase-0 does).
- K_banked(family): 0 under either family-grouping reading (§0 disclosure).
- K_intrinsic (confirm-not-mine): 2 -- PRIMARY (full CPI+NFP event-day
  cohort, frozen OR/breakout construct) + SECONDARY (disclosed, non-gating
  robustness: high-surprise/large-range subcohort only). This is the
  rescuer's own proposed design from the brainstorm workflow screen and
  matches the confirm-not-mine K<=3 ceiling. NO window/anchor/instrument
  sweep beyond these two pre-committed cells.
- K_eff + floor(K_eff): K_eff = 2 -> floor 0.85 (combined-family reading;
  0.85 or better under the separate-family reading too -- see §0).
- delta/sigma (req 2): UNSCREENABLE at admission -- NO citable delta exists
  for ZF (or any Treasury instrument) intraday post-CPI/NFP continuation.
  Routed to the Phase-0 delta-extraction (the Req-2 relief valve, same as
  ORB-ZB-1). Honest anchor for what FAILURE looks like: the program's three
  own-cohort post-event deltas (ZN auction 1.01bp, CL EIA-uncond 1.16bp, ES
  overnight 1.5bp) all sit far below any plausible ZF hurdle (~1.5bp,
  computed below) -- if this candidate's delta lands in that same band, it
  is DEAD, and that band is the single most likely outcome on priors.
- N + event frequency (req 4): CPI (12/yr) + NFP (12/yr) = ~24 events/yr x
  ~7.5y (2019-2026) = N ~ 180, less any dating-ambiguous events dropped per
  §5. Floor for power=0.50 at N=180: delta/sigma >= 1.96/sqrt(180) = 0.146.
- power: PENDING Phase-0 delta (cannot be computed before the extraction --
  this IS what Phase-0 measures, unlike NG-EIA-1's sibling brief where a
  published delta already exists).
- dedup attestation: rejected_candidates.md + closed discovery manifests +
  docs/methodology/rejected_signals.md checked 2026-07-20. Nearest entries:
  "rates-intraday-mean-reversion on MICRO10Y/2YY" (a FADE, not a breakout;
  different mechanism) and today's "opening-range-breakout on ZB"
  (UNCONDITIONAL breakout; this candidate is CONDITIONAL -- disclosed as the
  one untested cell in §1, not a re-proposal of either).
- screen verdict: UNSCREENABLE(req-2: no cohort delta anywhere -> Phase-0
  delta-extraction probe)
- operator ratification: PENDING (this brief requests the Phase-0 GO, §8)
```

---

## §3 — Phase-0 cheap-falsifier battery (K=0 measurement + the pre-committed K=2 primary/secondary split; ~$0)

Single native-ZF δ-extraction (Databento GLBX.MDP3 `ZF.v.0` continuous ohlcv-1m, 2019→2026, resampled 15m ET, `orb_lib.py` reused verbatim), scoped to CPI+NFP event days only. All limbs from one pre-committed script (the F-B/H-ZNAUC-1/ORB-ZB-1 discipline: gates coded before any return is read).

| # | Screen | Measure | PASS condition | Precedent |
|---|---|---|---|---|
| **P0.1 — event-day range geometry** | median OR range on event days vs RT cost (both single- and two-RT conventions) | range/RT ratio materially better than ZB's unconditional 4.3:1 (the instrument-choice thesis; a null result here means ZF isn't actually better geometry on the *event-day* subset even if its per-tick math is better) | ORB-ZB-1 pattern, scoped to event days |
| **P0.2 — PRIMARY cost-law (Req 5)** | mean gross OR-breakout edge_R on the full CPI+NFP cohort (K_intrinsic cell 1) | `edge/cost ≥ 4.0×` on at least the single-RT convention | The gate that killed D5/H-OD-1/H-ZNAUC-1/F-B/ORB-ZB-1; this is the verdict cell |
| **P0.3 — SECONDARY (disclosed, non-gating)** | same construct, high-surprise/large-OR-range subcohort only (frozen split, e.g. top-half by realized OR range) | reported alongside P0.2, never substituted for it | Rescuer's pre-registered design; guards against a diluted-primary/concentrated-secondary result being silently promoted |
| **P0.4 — Req-4 power** | `power = Φ(√N·\|δ/σ\| − 1.96)` at the realized dating-clean N | power ≥ 0.50 | H-ZNAUC-1/F-B/NG-EIA-1 formula, reused |
| **P0.5 — decorrelation pre-flight (Stage-8 ADR)** | `ρ = ZF event-day daily-$std / c1-book daily-$std` at a bound reference weight | `ρ < 1.0` (expected to pass near-mechanically given ~10% in-market days — see §1; not assumed, computed) | The exact gate ORB-MNQ-1 failed; ORB-ZB-1's own P0.2 pattern |

**Ordering:** P0.1 first (cheapest, and the instrument-choice thesis itself — if ZF's event-day geometry isn't actually better than ZB's, the whole rationale for switching instruments collapses before the breakout numbers are even examined). P0.2 (PRIMARY) is the actual verdict. P0.3 is reported alongside, never gating. P0.4/P0.5 are computed once P0.2 clears (moot otherwise).

---

## §4 — Falsifiable hypothesis (H-RATES-ZF-0; binary)

**H-RATES-ZF-0 — if** the fixed CPI/NFP-day OR-breakout construct on native ZF clears **P0.1** (materially better event-day geometry than ZB's unconditional 4.3:1) **and P0.2 PRIMARY cost-law ≥ 4.0×** **and P0.4 power ≥ 0.50** **and P0.5 (ρ<1.0)**, **then** RATES-EV-ZF-1 graduates to a Phase-1 §R-freeze confirmation campaign; **otherwise** it closes FALSIFIED (or `NEEDS_CONTEXT` if the CPI/NFP calendar cannot be reliably dated, re-run once corrected) and is appended to `docs/rejected_candidates.md`, extending the {conditional, unconditional} × {routine-drift, breakout} matrix to fully-dead.

**Numeric accept threshold:** graduate iff PRIMARY `edge/cost ≥ 4.0×` AND `power ≥ 0.50` AND `ρ < 1.0`. **Falsified** on any limb failing with a correctly-dated event set. P0.3 (SECONDARY) is never substituted for P0.2 as the accept criterion — a candidate whose *only* signal is in the surprise-conditioned subcohort while the full primary cohort fails is the F-B informed-flow trap in a different costume and closes FALSIFIED, not AMBIGUOUS.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Using a "first Friday of the month" heuristic for NFP dates.** **Directly forbidden by memory `reference_bls_release_date_sourcing`** (§0): NFP diverges materially from this heuristic — 2nd-Friday in ~5 months 2022–2025, non-Friday 4× including three 2025–2026 shutdown-shifted dates. **Required instead:** primary-sourced dates from `bls.gov/schedule/YYYY/home.htm` (per-year "Schedule of Selected Releases") via the claude-in-chrome browser MCP (WebFetch is 403-blocked on bls.gov), cross-checked against `bls.gov/bls/news-release/empsit.htm` for non-publications (the memory flags a real 2025 government-shutdown gap).
- **Using a naive mid-month heuristic for CPI dates**, for the same class of reason — CPI release dates also shift around holidays and are not perfectly periodic; source them from BLS's own published schedule pages with the same primary-source discipline as NFP, not inferred.
- **Sweeping the OR anchor time (08:30 vs a later re-anchor) or the event set (adding FOMC) after seeing a weak P0.2 result** — K_intrinsic is pre-committed at 2 (PRIMARY full-cohort + SECONDARY surprise-subcohort). Adding FOMC, changing the anchor, or re-defining the subcohort *after* reading a result is exactly the K-inflating search this discipline forbids; any of those is a fresh manifest, not a Phase-0 branch.
- **Substituting ZN, TN, or ZB mid-probe if ZF's numbers disappoint** — ZF is the pre-committed instrument on tick-geometry grounds (§0/§1). A different Treasury instrument is a documented alternative requiring its own fresh pre-reg, never a same-probe swap (the exact move ORB-ZB-1's §5 also forbade).
- **Treating P0.3's SECONDARY subcohort result as the verdict if it passes while P0.2's PRIMARY fails** — explicit in §4; this is the F-B informed-flow trap (a real, large, conditional-only effect with no unconditional edge) recurring in event-breakout form.
- **Opening `register_search` / pulling the confirm panel before Phase-0 clears and a fresh operator GO is signed.**
- **Quoting a Phase-0 PASS as an edge** — licenses campaign scoping only.
- **Silently treating the Brooks-Katz-Lustig FOMC/multi-day mechanism as if it were an on-cohort CPI/NFP-intraday citation** — it is disclosed as adjacent evidence in §2's manifest precisely so this substitution cannot happen quietly later.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED (graduate)** | P0.1 geometry confirmed better than ZB AND P0.2 PRIMARY ≥ 4.0× AND P0.4 power ≥ 0.50 AND P0.5 ρ<1.0 | Author Phase-1 Stage-0 pre-reg (K=2, §R attestation per the D5/ORB-ZB-1/NG-EIA-1 model) → fresh operator GO → `register_search open` → confirm campaign |
| **FALSIFIED (close + register)** | Any of P0.1/P0.2/P0.4/P0.5 fails with a correctly-dated calendar | Close; append to `rejected_candidates.md` — completes the rates-event 2×2 matrix as fully-dead; K spend recorded per §7; Treasury-complex family bank updated |
| **AMBIGUOUS** | CPI/NFP calendar cannot be reliably dated (primary BLS sourcing fails or conflicts), or N too thin for a stable estimate | Closure names the re-test condition; no in-place threshold edit |

No calendar hard-date beyond the parent programme's 2026-11-08 idle review; Phase-0 is a single-session run once GO'd.

---

## §R — Reachability attestation (SKELETON — populated only at the Phase-1 freeze)

Not required for the Phase-0 measurement (H-ZNAUC-1/F-B/ORB-ZB-1 precedent — a δ-extraction is not a registered search). Drafted so the Phase-1 path is visible if Phase-0 clears:

- **R.1 — PRIMARY confirm gate:** reachable *iff* the Phase-0-extracted δ implies `edge/cost ≥ 4.0×` with power ≥0.50 — this is exactly what P0.2/P0.4 measure; cannot be honestly written before Phase-0 returns numbers (same logic as ORB-ZB-1's and NG-EIA-1's §R skeletons).
- **R.2 — SECONDARY/placebo gate:** a non-event-day control cohort (ordinary Tuesdays, say) with the identical OR-breakout construct — expected to reproduce ORB-ZB-1's unconditional-fade finding (negative or near-zero), which is itself the discriminating test: if the *control* also shows a positive breakout edge, the "conditioning" isn't doing any work and the PRIMARY result is suspect regardless of its own numbers. To be frozen precisely at Phase-1, not this scoping brief.

---

## §7 — Run protocol

0. **This brief:** manifest + Phase-0 battery frozen. **Operator reviews §8 → GO/NO-GO on Phase-0.**
1. **On Phase-0 GO:** build the CPI+NFP event calendar via primary BLS sourcing (claude-in-chrome browser MCP per §5's discipline — this is a real multi-step sourcing task, not a one-line script) → Databento `db_fetch estimate` (dry-run, mandatory) → cost-gate check → pull `ZF.v.0` continuous ohlcv-1m 2019→2026 (expect ~$0, matching the identical-class ZB pull) → run P0.1–P0.5 in one pre-committed script (`orb_lib` reused verbatim, day-filtered to the event calendar). **K = 0** (measurement; the K=2 PRIMARY/SECONDARY split is a Phase-0 *design* choice pre-registered here, not a K-consuming registered search — no `register_search open` occurs at Phase-0). Results land in `lab/archive/rates_ev_zf_recon_2026-07/`.
2. **On P0 RESOLVED only:** author the Phase-1 Stage-0 pre-reg (D5/ORB-ZB-1/NG-EIA-1 model — §R fully populated, K_intrinsic=2 formally bound via `register_search open`) → **fresh operator §R GO** → confirm panel → Stage 5/6/7/8 → survivor-scoring gate G0–G8 → (only then) lifecycle CANDIDATE intake.
3. **On P0 FALSIFIED:** append to `rejected_candidates.md`; the rates-event 2×2 (§1) is now fully dead; done.

---

## §8 — Operator GO gate (Phase-0 δ-extraction only; DRAFT until filled)

```
PHASE-0 GO: 2026-07-21 / JA (operator chat: "run both Phase-0 probes")
Ratified: a two-cell (PRIMARY + SECONDARY, K_intrinsic=2 pre-committed design,
  K=0 consumed at Phase-0), ~$0 native-ZF delta-extraction on the CPI+NFP
  event calendar (P0.1-P0.5). Calendar sourced via claude-in-chrome (bls.gov
  per-year schedule pages, all 8 years 2019-2026) BEFORE the pull, per the
  requirement below.
Did NOT authorize (none occurred): register_search open, K spend, the Phase-1
  confirm panel, or any live/Pine/allocation/dd_protection/ACTIVE_FIRM touch.
  Databento spend $0.00 confirmed.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Phase-0 GO unfilled -> no ZF manifest and no rates_ev_zf pull may exist yet.
grep -n "PHASE-0 GO: ____________" docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md \
  && echo "GO unfilled -- no register_search / pull for ZF" || echo "GO filled"

# 2. Treasury-complex family bank is 0 (Requirement-3 basis; re-derive, do not trust prose).
ls discovery_manifests/ | grep -iE 'z[bnft]|treasury|bond' && echo "a Treasury manifest EXISTS -- recheck K" || echo "family bank 0 confirmed"

# 3. K_intrinsic pinned at 2 (PRIMARY+SECONDARY), no sweep beyond that.
grep -n "K_intrinsic (confirm-not-mine): 2\|PRIMARY (full CPI+NFP" docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md

# 4. Dedup: this is disclosed as the untested cell, not a re-proposal of ZB or MICRO10Y/2YY.
grep -n "rates-intraday-mean-reversion\|opening-range-breakout on ZB" docs/rejected_candidates.md

# 5. NFP-heuristic forbidden move is explicit (memory-sourced discipline).
grep -n "first Friday of the month.*heuristic\|reference_bls_release_date_sourcing" docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md

# 6. Stage-8 risk-N_eff gate has a real input (P0.5's binding statistic when reached).
grep -n "n_eff_risk_delta" lab/research_utils/breadth.py

# 7. Construct engine reused verbatim (no reimplementation drift).
grep -nE "def orb_backtest|def placebo_within_day|def session_panel" lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python <brief-authoring>/scripts/check_brief.py docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md --type inquire
# Expected: all 6 checks PASS

# §0 anchors current
git log -1 --format='%h %ci' -- lab/archive/orb_zb_recon_2026-07/RESULTS.md              # 568c639
git log -1 --format='%h %ci' -- lab/analysis/orb/orb_universe_2026-06-22/orb_lib.py           # b89f9a6
git log -1 --format='%h %ci' -- docs/briefs/closures/H-ZNAUC-1-closure-screen-fail.md     # aa0738d

# K-bank ledger reproduces the instrument-selection finding (Treasury complex still 0)
python -c "import json,glob; [print(p, json.load(open(p))['status'], json.load(open(p))['K']) for p in glob.glob('discovery_manifests/*.json')]"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-20 | Scoping + seed manifest authored (post-brainstorm-workflow selection, the lower-prior/higher-prize sibling to NG-EIA-1). Phase-0 δ-extraction GO requested. NFP/CPI calendar-sourcing risk (first-Friday heuristic is wrong per memory) surfaced and resolved via a primary-BLS-sourcing requirement in §5. | Joshua (direction) + Claude (Sonnet 5) |
| 2026-07-21 | Full CPI+NFP calendar sourced via claude-in-chrome from bls.gov's 8 per-year schedule pages (179 events; confirmed the 2025 government-shutdown gap — October-reference-month never published for either series — and the 2026-02-11 shutdown-catchup date, both matching memory `reference_bls_release_date_sourcing`). ZF.v.0 pulled `$0.00`; Phase-0 run. **CLOSED FALSIFIED** — P0.2 cost-law KILL (1.15× vs 4.0×) + P0.4 power FAIL (0.30 vs 0.50), despite P0.1 geometry (17.6:1) and P0.5 decorrelation (ρ=0.28) both validating. Closes the rates-event 2×2 matrix fully dead. K=0. RESULTS + rejected_candidates disposition. | Joshua (GO) + Claude (Sonnet 5) |
