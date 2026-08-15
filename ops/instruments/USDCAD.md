# INSTRUMENT LEDGER — USDCAD

**Purpose:** Single source of instrument-level truth. Any session deriving, testing, or tuning on USDCAD MUST read this file at session start and append its disposition at session end (operational rule 10, ratified 2026-06-11 — see [`docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md`](../../docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md)). Created 2026-06-11 after a parallel-session concept collision (see Resolved Decisions). Canonical path: `ops/instruments/USDCAD.md`.

Ownership boundary (operational rules 5/7): this ledger owns instrument-level findings, concept status, and the shared anti-SNAG budget. Strategy parameters stay canonical in Pine source; locked-risk constants in `dd_protection.py`/`firm_rules.py`. The ledger links out, never restates.

## PROFILE (machine-readable)

```yaml
symbol: USDCAD
asset_class: fx-major
family: []
venue_tradable: false
venue_note: "FXIFY/DXTrade CFD venue closed 2026-07-10; no live venue for this instrument at present."
k_bank_source: "../../discovery_manifests/"
cost_hurdle:
  value: 0.097
  units: "R round-trip"
  basis: "1.42x ATR(15m) stop (COST LAW: cost-in-R proportional to price/stop_dist)"
  source: "#durable-1"
cells:
  - mechanism: band-pierce-continuation
    verdict: CONTINGENT-FORWARD
    date: 2026-06-16
    source: "../../docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md"
  - mechanism: opening-range-breakout
    verdict: DEAD
    date: 2026-06-14
    source: "../../lab/archive/usdcad_reverse_2026-06-14/RESULTS.md"
  - mechanism: trend-following
    verdict: DEAD
    date: 2026-06-14
    source: "../../lab/archive/usdcad_reverse_2026-06-14/RESULTS.md"
  - mechanism: mean-reversion-fade
    verdict: DEAD
    date: 2026-06-26
    source: "../../lab/archive/usdcad_fade_2026-06-26/RESULTS.md"
structure:
  - claim: "A day-of-week effect is statistically real in-sample (Tuesday-minus-rest permutation p=0.006) but the mechanism is unresolved — this is what BPC-001 conditions on, not an established edge on its own."
    source: "#durable-3"
  - claim: "USDCAD's 15m price-action mechanism space is exhausted on OHLC alone (2026-H1 reverse-engineering): VR<1 at every horizon, no momentum at any TF, breakouts fade with a directional asymmetry — corroborated on the full 2020-26 panel; revival needs an exogenous regime gate (CA-US rate-diff / WTI), not a re-tuned OHLC level."
    source: "#durable-8"
```

---

## Resolved decisions

**Sovereign v0.2-X15 vs BPC pre-registration forbidden move #3 — ADJUDICATED 2026-06-11 (Joshua): Reading A.**
The BPC forward-test pre-reg (2026-06-11) forbids "new USDCAD in-session concepts" during the forward window, citing the anti-SNAG provision. A parallel session the same day moved Sovereign USDCAD (H4 rate-differential trend-rider) onto a 15-minute execution layer (v0.2-X15), creating genuine ambiguity over whether X15 falls under FM#3.
- **Ruling:** FM#3's scope is the **band-pierce / NY-morning in-session signal family**, not any 15m USDCAD strategy. Sovereign is a different mechanism (H4 regime + 15m trigger) → outside FM#3 scope. X15 derivation continues.
- **Wording amendment:** landed as Amendment A1 in the pre-reg ([`docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md`](../../docs/ltm/briefs/pre-registration/FWD-PREREG-BPC-USDCAD-TUE-2026-06-11.md)), dated 2026-06-11 — before any forward data exists (first eligible trade 2026-06-16), so checkpoints remain clean under the pre-reg's own audit hook.
- **Budget consequence:** SVRN is tracked as a separate H4-regime family in the anti-SNAG ledger below; the band-pierce family budget is unaffected by SVRN runs.

## Active concepts

| Concept | Mechanism | Status | Owner-session anchor |
|---|---|---|---|
| BPC-001 (Tuesday) | 15m band-pierce impulse continuation, short-only | **CONTINGENT-FORWARD** — frozen config, demo from 2026-06-16, checkpoints n=12/25/50 per FWD-PREREG-BPC-USDCAD-TUE-2026-06-11. **⚠ CHECKPOINTS UNREACHABLE (recorded 2026-07-28, verdict NOT flipped — operator adjudication owed):** the forward test's execution surface no longer exists. (a) The FXIFY/DXTrade CFD venue closed **2026-07-10** (this ledger's own `venue_tradable: false`), so no USDCAD demo fills can accrue; (b) its measurement engine `ops/live_journal/` + the `live-execution-journal` skill were **retired 2026-07-11** ([`docs/adr/2026-07-11-ops-cfd-estate-retirement.md`](../../docs/adr/2026-07-11-ops-cfd-estate-retirement.md)). The n=12/25/50 checkpoints have therefore been unable to advance since 2026-07-10 and cannot. **Live consequence:** `CONTINGENT-FORWARD` is a BLOCKING verdict (`scripts/instrument_profiles.py` L79) whose stated grounds are "a frozen forward test is running on this cell" — so this cell currently blocks any second band-pierce proposal on behalf of a test that cannot run. Resolving it means moving to `DEAD` or `AMBIGUOUS-PARKED` (`ORPHANED` is not in the verdict vocabulary) — a real disposition with gate consequences, deliberately **not** taken as hygiene. | Aegis/BPC session 2026-06-11 |
| Sovereign (SVRN) | H4 trend-rider, daily-EMA + rate-spread regime; v0.2-X15 = 15m execution variant | Derivation: **cfg10 = current best** (cfg05 base + useRegimeExit=TRUE: N=204, PF 1.232, WR 50.5%, DD 1.87%, RF +1.93); cfg05 prior best (PF 1.127, RF +0.31, DD 2.40%, N=58); cfg11 (lb=3) confirmed the 2024/2025 exit-timing tradeoff is unresolvable by spreadLookbackD; X15 derivation continues per FM#3 Reading A, limited to the pullback/structure-break pair already specified | SVRN sessions 2026-06-11 (per `SVRN_session_handoff_2026-06-11.md`) |
| CONCEPT-USDCAD-RDM-001 (Sovereign rate-differential mechanism, SVRN family) | 5d CA-US rate-spread loading; mechanism probe only (no strategy build, brief FM#1) | Stage-1 **ADMIT 7/7** / dedup CLEAR; **F1 mechanism falsifier PASS** — spread-loading beta +0.0338, perm p<0.0005, all 3 episodes positive, survives trend+WTI controls; concern #1: conditional anti-correlation clears the binary bar (−0.0167) but is economically ≈0. Next stage codify→sweep→validate, **operator-gated**; carry concerns #1/#2 into portfolio-fit | RDM session 2026-06-12 (PR #176; [`lab/analysis/usdcad_rdm/CARD.md`](../../lab/analysis/usdcad_rdm/CARD.md)) |

## Dead / parked (do not revive without new mechanism-level evidence)

- **Aegis USDCAD v0.1** (mean-reversion transfer): FAILED — n=245, PF 0.756. Loss character = pervasive trend-impulse; no hour/day/regime refuge.
- **Inverse-direction (raw pierce shorts):** FAILED by excursion-bounded analysis — all stop/target cells ≤0 at best-case path resolution; signal has no raw directional edge.
- **BPC all-days variant:** Mon −0.068R / Wed −0.096R under frozen tuned config; only Tuesday positive.
- **SVRN dead axes** (per SVRN handoff): atr 3.0; fast/slow faster than 20/80; ema=200 isolation; "fixing 2024 with a parameter" (2024 = regime, not parameter); spread gate as entry filter without mechanism redesign. **2026-06-11 addition:** regime-exit lookback tuning (cfg11) — no spreadLookbackD simultaneously preserves 2024 (needs quick exit) and 2025 (needs to hold); the 2025 give-back is a known, accepted cost of the cfg10 mechanism.
- **15m volatility breakout** (Donchian + opening-range, long-short): FAILED — falsified on 2026-H1 (pre-reg `PREREG-USDCAD-BREAKOUT-2026-06-14`), 0/734 eligible configs positive net, **negative even gross** (−0.10R) under both next-open AND intrabar stop-level fills; breakouts fade. 3-agent harness audit confirmed TRUSTWORTHY. New mechanism family (not band-pierce) → exploratory, anti-SNAG budget unconsumed.
- **15m trend-pullback** (`ema_recovery`, long-short): FAILED — apparent best +0.148R (dome 6/6, H1/H2 both+, timing-perm p=0.027) is a **selection artifact**: DSR 0.144 (need >0.95) + random-entry best-of-N null P=1.0 (null best +0.25R > observed). Also fails the 4×-cost-hurdle gate. Do not revive at 15m without multi-regime OOS. Pre-reg `PREREG-USDCAD-PULLBACK-2026-06-14`.
- **15m up-spike fade** (short-only, fade Donchian up-breakouts): NULL on the **full 2020-26 panel** (the 2026-06-14 NULL's named multi-regime reopener) — best +0.030R/trade is **SUB-COST** (4× hurdle 0.16R; →−0.002R @1.6pip), **DSR 0.44**, and **REGIME-FRAGILE** (positive 2023-25 trend, **−0.040R in 2021 CAD-strength**; walk-forward H2→H1 −0.039R). The up-fade asymmetry is REAL (up-fade +0.030 > down-fade −0.026, durable #8 corroborated on 6yr) but **not tradeable on price action**. Revival needs an **exogenous** regime gate (CA-US rate-diff / WTI), not a re-tuned OHLC level (graveyard lesson). Pre-reg `PREREG-USDCAD-FADE-2026-06-26`; RESULTS `lab/archive/usdcad_fade_2026-06-26/RESULTS.md`. FXIFY candidate Pine shipped OUT-OF-EVIDENCE-BASE.

## Durable instrument findings (binding on all USDCAD designs)

1. **COST LAW:** cost-in-R ∝ price/stop_dist under risk sizing. Measured 0.097R RT at 1.42×ATR(15m) stops; 0.055–0.072R at 2.5×ATR. Tight-stop designs pay a structural tax; compute the hurdle pre-flight.
2. **No raw directional edge at 1.9σ lower-band pierces** (NY morning); post-pierce excursions symmetric. Only the impulse-confirmed cohort (~27%) follows through.
3. **Day-of-week effect is statistically real in-sample** (Tue-minus-rest permutation p=0.006) but mechanism unresolved — see BPC pre-reg.
4. **2024 regime split:** BoC-cutting/Fed-holding divergence (**window pinned 2026-06-15: Jun 5 2024 BoC first cut → Sep 17 2024, the day before the Fed's Sep 18 −50bp cut; widest spread −125bp**) was SVRN's worst year and BPC's best (+1.125R, n=8). Candidate regime-complementarity datapoint for the anti-Constellation thesis; treat as hypothesis, not established. (SVRN cfg10's regime-exit turned 2024 from −3,511 to +1,675 — mechanism-as-designed, an exit not an entry filter.)
5. **Feed notes:** Pepperstone↔OANDA near-identical for 15m threshold signals (entry-date Jaccard 0.96 on BPC). **Dukascopy diverges enough to break threshold-signal replication — disqualified as TV-proxy for this instrument** (qualifies the canonical-R&D-feed convention; echoes ECR DJ30 finding). TV exports may be CAD-denominated ("Net PnL CAD") — use the column-mapped shim; PF/WR/DD% currency-invariant.
6. **BoC decision-day array 2022–2026** verified **2022–2026** vs bankofcanada.ca (**2022 gap closed 2026-06-15**: 8 dates, all 10:00 ET, confirmed vs BoC FAD press releases). Announcement time **10:00 ET through 2023 (last: Dec 6 2023) → 09:45 ET from Jan 24 2024** (presser ~10:30; change announced Dec 2023 re: FX-option-expiry timing). Lives in bpc_usdcad_v0_1.pine (**blocks OFF for the Tue-only forward test**); extend yearly. Full verified array → [`lab/archive/usdcad_ratemap_verify_2026-06-15/RESULTS.md`](../../lab/archive/usdcad_ratemap_verify_2026-06-15/RESULTS.md).
7. **Event map (ET):** CA data 8:30; US data 8:30/10:00; EIA Wed 10:30 (holiday weeks → Thu 11:00); WMR fix 11:00; US/CA jobs collide first Fridays; CAD month-end flow edge reportedly defunct post-2013 (CPP unhedged shift).
8. **15m price-action is mean-reverting and the mechanism space is exhausted (2026-H1 reverse-engineering, exploratory).** VR<1 at every horizon (0.96→0.76), no momentum at any TF; breakouts fade with a **directional asymmetry** (up-spikes fade hard −0.43R/24bar, down-moves flat). Breakout NULL, pullback = selection artifact, raw reversion sub-cost (corroborates finding #2 / the closed `raw-inverse` null) — all on 2026-H1. The binding constraint is the cost law (#1). Verdict & reusable triple-audited harness: [`lab/archive/usdcad_reverse_2026-06-14/RESULTS.md`](../../lab/archive/usdcad_reverse_2026-06-14/RESULTS.md). **TZ note:** this BAR_EXPORT's clock is UTC (chart was ET); convert UTC→ET (DST-aware) for any session logic. **2026-06-26 OOS update (full 2020-26 panel = the named reopener):** the up-fade asymmetry is **corroborated** (up-fade +0.030R > down-fade −0.026R) but **SUB-COST and REGIME-FRAGILE** — negative in 2021 CAD-strength, walk-forward H2→H1 −0.039R. Exhaustion now confirmed **across regimes**, not just the 2026-H1 window; revival = exogenous gate only. → [`lab/archive/usdcad_fade_2026-06-26/RESULTS.md`](../../lab/archive/usdcad_fade_2026-06-26/RESULTS.md).

## Regime calendar (2020–2026)

Shared USDCAD-family regime labels so per-year tables cite the same rows instead of ad-hoc narratives. Confidence tags: [H]=high (well-documented), [M]=medium (verify before load-bearing use), [L]=low/TBD (must verify). Formerly `ops/reference/regime_calendar.md` (inlined here 2026-07-16). Maintenance: append 2026 rows quarterly. **Not** an input to the portfolio MC regime trigger (`time_to_pass.py --regime-check` consumes TV panel exports).

| Year | Fed | BoC | Policy-divergence read | USD trend | Oil | USDCAD path | Tag |
|---|---|---|---|---|---|---|---|
| 2020 | Slash to ~0 (Mar), QE | Slash to 0.25 (Mar) | Parallel panic easing | Spike (Mar) then decline | Collapse (neg. WTI Apr) → recovery | Spike ~1.46 → grind down | [H] |
| 2021 | Hold, taper talk H2 | Early taper (Apr, first G7) | BoC-hawkish lean | Soft H1, firming H2 | Strong rally all year | CAD-favorable; range-down then base | [H] |
| 2022 | 0→4.25/4.5 aggressive | 0.25→4.25 (incl. 100bp Jul) | Parallel aggressive hiking | USD supertrend (DXY peak Sep) | Spike H1 (Ukraine), fade H2 | 1.25→~1.39 trend up | [H] |
| 2023 | →5.25/5.50 peak (Jul), hold H2 | →5.00 peak (Jul), hold H2 | Parallel peak-and-hold | Choppy, no supertrend | Rangebound | ~1.31–1.39 range | [H] |
| 2024 | Hold till Sep, then ~100bp cuts | Cuts from Jun (first G7), 5.00→3.25 | **BoC-dovish divergence** | USD firm vs CAD | Rangebound-weak | Grind up toward ~1.44 | [H] |
| 2025 | Resumed cuts H2 → 3.50–3.75% (75bp) | →2.75% (Mar 12); pause; →2.50% (Sep 17) →2.25% (Oct 29), hold | Early-year tariff shock; BoC eases below Fed | USD broadly weaker over year (DXY → ~96) | Volatile, politically driven | Feb tariff spike ~1.476–1.479 intraday (high since 2003; ~1.454 daily high) → drift down; year-end 1.3706 (2025 low 1.3573, avg ~1.397) | [H] |
| 2026 YTD | Hold 3.50–3.75% (Jan/Mar/Apr/Jun); Jun dots erase 2025-penciled cut → cuts pushed to 2027-28 (Iran-war inflation) | Hold 2.25% (Jan 28 / Mar 18 / Apr 29 / Jun 10; 5th straight incl. Dec-25) | Both on hold; Fed ≈137bp above BoC → USD-carry-favorable | USD firmer vs CAD in H1 | Iran war (Feb 28 start), Hormuz supply risk, war-premium; faded to ~$70 WTI on late-Jun US–Iran deal | Grind up ~1.37 (Jan) → ~1.42 (H1 high 1.4235–1.4243, Jun 24–25) | [M] |

**Usage:** cite Tag by year in per-year tables; upgrade any [M]/[L] cell before load-bearing use. Known datapoint: 2024 divergence = SVRN-worst / BPC-best (durable finding #4).

**2026-08-08 verification — DISCHARGED 2026-07-02** (programme-audit R6): 2025 [M]→[H]; 2026 YTD [L]→[M] (partial year — full-year label + H2 append at year-end). Sources: BoC FAD releases; Fed FOMC 2026-06-17; public USDCAD/oil prints cited in the 2026-07-02 verification pass (PR #268).

## Anti-SNAG ledger (shared budget — all sessions count)

**Band-pierce / NY-morning in-session 15m family** (= FM#3 scope per the 2026-06-11 adjudication): Aegis-reversion (null), raw-inverse (null). BPC survives only as forward-contingent. **Two nulls recorded — no third in-session 15m concept in the band-pierce family without path-independent new evidence.** (2026-06-14: an exploratory reverse-engineering *control* that fades Donchian/ORB breakouts reproduced this null at sub-cost expectancy — corroboration of the closure, **not** a third concept; budget unconsumed. The two new dead entries above — breakout, pullback — are distinct mechanism families, not band-pierce.)

**SVRN H4-regime family:** tracked separately per the FM#3 adjudication; no nulls recorded (derivation active).

## Session log (append-only)

- 2026-06-11 / Aegis→BPC session: kill record + session record + forward pre-reg issued; status CONTINGENT-FORWARD.
- 2026-06-11 / SVRN sessions: cfg00–05 complete (session 1); cfg10/11/12 run (session 2) — cfg10 BEST; handoff doc with forbidden moves; v0.2-X15 built.
- 2026-06-11 / This entry (original Downloads draft): ledger created; collision documented; adjudication pending.
- 2026-06-11 / CC placement session: ledger placed at `ops/instruments/USDCAD.md` (P1 ratified; P2 forward-WIP cap **NOT ratified** — see ADR §2c); FM#3 adjudicated **Reading A** by Joshua, Amendment A1 appended to the in-repo pre-reg copy; **stale-row correction:** the Downloads draft's SVRN row ("cfg05 = live best, cfg06–10 queue") predated its own cited handoff — cfg10/11/12 had already run with cfg10 BEST (N=204, PF 1.232); row updated from `SVRN_session_handoff_2026-06-11.md`. P3 cfg-fingerprint convention ratified — propagate into SVRN v0.2-X15 at its next legitimate edit (not a standalone touch).
- 2026-06-12 / Sovereign RDM session (PR #176; **disposition backfilled** at PR #174 merge-resolution — that session merged to main before this ledger landed, so it could not append): CONCEPT-USDCAD-RDM-001 stage-1 ADMIT 7/7 + F1 mechanism falsifier PASS (row added above). SVRN family → outside FM#3 per Reading A; anti-SNAG budget unchanged (PASS, not a null). Same day, ADR `2026-06-12-tv-csv-canonical-feed-policy` made TV CSV exports canonical (bar feeds staging-only) — consistent with durable finding #5's Dukascopy disqualification; the RDM brief's "Dukascopy canonical" step was superseded mid-run.
- 2026-06-14 / 15m price-action reverse-engineering (exploratory, off-pipeline R&D; operator-driven INQHIORI; [PR #184](https://github.com/Joshua-Asante/multi_firm_operations/pull/184)): two pre-registered loops on the 2026-H1 BAR_EXPORT, both **NULL** — breakout (Donchian+ORB, 0/734 positive, negative-gross, 3-agent audited) and trend-pullback (selection artifact: DSR 0.144, random-entry null P=1.0). Step-0 caught the **UTC-not-ET** timezone trap. Findings → durable #8 + two dead-list entries; anti-SNAG budget **unconsumed** (distinct mechanism families; reversion control corroborates the closed band-pierce null). No `core/` touch, no lock/allocation change. → [`lab/archive/usdcad_reverse_2026-06-14/RESULTS.md`](../../lab/archive/usdcad_reverse_2026-06-14/RESULTS.md), pre-regs `PREREG-USDCAD-{BREAKOUT,PULLBACK}-2026-06-14`.
- 2026-06-15 / Macro-fact verification (repo-side CC verifying a claude.ai web-research doc; no repo access on the authoring side): verified the CA-US rate-diff regime map + BoC decision-day array against BoC/Fed primary sources. **2022 gap closed** (8 dates, all 10:00 ET, vs BoC FAD releases); 10:00→**09:45 ET convention pinned to Jan 24 2024** (last 10:00 = Dec 6 2023); **2024 divergence window pinned Jun 5 → Sep 17 2024** (−125bp widest, day before Fed's Sep 18 −50bp). Anti-confabulation + feed-policy scans PASS (official series only; no bar feed; zero strategy-perf claims). Durable findings **#4 + #6 updated**. **BoC-array `.pine` write DEFERRED** — BPC blocks are OFF (Tue-only) and the frozen forward window opens 2026-06-16, so patching the array is inert + an FM#1 hazard; recorded in the report instead. No `core/` touch, no `.pine` touch, no lock/allocation change. → [`lab/archive/usdcad_ratemap_verify_2026-06-15/RESULTS.md`](../../lab/archive/usdcad_ratemap_verify_2026-06-15/RESULTS.md).
- 2026-06-26 / 15m up-spike-fade candidate + validation (exploratory off-pipeline R&D; brainstorming → strategy-validation): operator supplied the 6-year 2020-06→2026-06 Pepperstone BAR_EXPORT (the 2026-06-14 NULL's named multi-regime reopener) and asked for a FXIFY-compliant Pine shaped by USDCAD lessons. Pre-registered a **short-only up-spike fade** (`PREREG-USDCAD-FADE-2026-06-26`); Step-0 PASS (UTC→ET verified, peak ET 10:00); frozen 8-config grid → **NULL** (G1 cost-hurdle fail +0.030R<0.16R; G2 DSR 0.44; G3 walk-forward H2→H1 −0.039R; G5 asymmetry PASS — real but sub-cost). Per-year smoking gun: edge in 2023-25 trend, **−0.040R in 2021 CAD-strength**. **Confirms the prior NULL on its own reopener**; graveyard lesson reproduced (revival = exogenous rate-diff/WTI gate, not OHLC re-tune). FXIFY candidate Pine shipped **OUT-OF-EVIDENCE-BASE** (compiles clean via `pine_check.py`), nothing deployed. **Anti-SNAG budget unconsumed** (up-fade = inverse of the distinct breakout-continuation family; exploratory endpoint; corroborates exhaustion, not a band-pierce concept). No `core/`/lock/allocation/dd_protection change; anchor 99.83/0.17/4.37 stands. **Native-TV confirmed same day** (`UCAD-FADE` TV export, 494 trades, 2020-03→2026-06 incl COVID): **+1.02%/6.3yr, PF 1.046, WR 48%, maxDD 2.51%; 2021 −0.19%** — NULL confirmed by the native arbiter (PF ties Python's 1.069 within ~2%). Event-avoidance ON flips mid-year signs vs the Python panel (marginal-non-edge signature); FXIFY halts never fired. → [`lab/archive/usdcad_fade_2026-06-26/RESULTS.md`](../../lab/archive/usdcad_fade_2026-06-26/RESULTS.md), pre-reg `PREREG-USDCAD-FADE-2026-06-26`.
- 2026-07-16 / Hygiene: regime calendar inlined from deleted `ops/reference/regime_calendar.md` into this ledger (`## Regime calendar`); Sentinel retargeted. No concept/status change.
- 2026-07-28 / D7 hygiene (annotation only, **no verdict change**): recorded that BPC-001's `CONTINGENT-FORWARD` checkpoints have been **structurally unreachable since 2026-07-10** — venue closed 07-10, measurement engine retired 07-11 — and that the cell is consequently blocking on behalf of a forward test that cannot run. The verdict token was **deliberately left as-is**: flipping a BLOCKING verdict changes what `instrument_profiles.py` forecloses, which is an operator adjudication, not documentation repair. Four prior sessions flagged this "operator call / not adjudicated"; this entry supplies the missing fact (*why* it cannot advance) so the call can actually be made. Disposition: [`docs/notes/2026-07-28-tier-c-thread-dispositions.md`](../../docs/notes/2026-07-28-tier-c-thread-dispositions.md) §D7. No `core/`, Pine, panel, or allocation change.
