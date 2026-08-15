# Q-ICT-CASCADE-1 — Falsification test campaign for the 5-layer ICT cascade

**Status:** `CLOSED — 2026-06-19 (all 5 layers disposed; NO deployable edge — see cont. 10 + CLOSURE-1M-INSUFFICIENT-N.md §4)`
**Authored:** 2026-06-18
**Closed:** 2026-06-19
**Authors:** Joshua + Claude (audit + plan)
**Parent question:** N/A (this IS the parent campaign; five forked module sub-claims, §3/§4)
**Sub-questions opened:** Q-ICT-W, Q-ICT-D, Q-ICT-1H, Q-ICT-1M, Q-ICT-LIB
**Loop:** Inquire-phase Pre-Q — closure gated per-layer in §6; the cascade closes only when every layer's gate fires or a go/no-go blocker (§7.A) kills the campaign.
**Artifact path:** `lab/analysis/ict_cascade_2026-06-18/TEST_PLAN.md`

> **This file is the multi-session campaign tracker.** Read the Progress Ledger first.
> The five `.pine` files are the canonical source (Rule 0 — read the code, not this doc).
> Nothing here is validated; this is a *falsification rig*, not a strategy with established edge.

---

## Progress Ledger (reverse-chron — update at every session wrap)

| Date | Session did | State | Next action (top of stack) |
|---|---|---|---|
| 2026-06-19 (cont. 10) | **1M-layer attempt (operator F8-override) + CASCADE CLOSE.** Operator chose "Override F8, run single-regime" and ran the 1M strategy in the Strategy Tester. Default (all gates on) → 0 trades (bias∧PD near-contradictory in a trend — the same tension that falsified 1H). All-gates-off, `useBody=false`, max 1m history (~2 days, TV's 1m cap) → **247 orders placed, 0 filled (0%), all 247 expired**; `closed trades = 0`. Diagnosed via the on-chart B4 table: the raid→FVG→target chain works (only 6 cost / 8 no-draw skips), but the locked `limit-on-return / mid / retraceK=6` entry **never fills** (displacement FVGs continue rather than retrace within 6 1m bars). No locked param or entry-mode changed (would void). | **1M = INSUFFICIENT-N** (dual wall): (a) n=0 ≪ 100 floor (0% fill); (b) ~2-day single-regime 1m → F8 BINDING SPEC unmet. **Q-ICT-CASCADE-1 CLOSED** — LIB OK · W RESOLVED · D SSL-RESOLVED/BSL-FALSIFIED · 1H FALSIFIED · 1M INSUFFICIENT-N → **no layer licenses a deployable edge.** Closure `CLOSURE-1M-INSUFFICIENT-N.md` (incl. §4 cascade summary + §5 cross-instrument/NAS100 implications). **F9** (0%-fill entry non-viability + 1m data wall) filed in `SPX500.md`. | **None for the campaign** (closed). Optional forward strategy-dev (NOT this campaign): redesign the 1M entry mechanism (market-on-FVG / wider retraceK / near-edge), gated behind a validatable multi-regime 1m data path that the canonical TV feed cannot supply. No `core/`/lock/allocation change. |
| 2026-06-19 (cont. 9) | **1H-layer verdict + CRITICAL harness-defect fix.** Operator exported **US500 1H** (`PEPPERSTONE_US500, 60_a6b6b.csv`, 3039 bars, 2025-12-11→2026-06-18 — TV's 1H history cap, single benign regime). First scoring surfaced a verdict-flipping defect: `recompute_hits` transcribed Pine's historical offset `series[fwdK]` (= fwdK bars BACK) as a FORWARD array index `series[i+fwdK]`, scoring the COMPLEMENT of the claim (matched exported Pine cols only ~36% vs a backward reconstruction's 100%; rates were 1−Pine). The look-ahead audit fired `ok=False`/~49% but the harness mis-handled it (trusted the buggy recompute over the correct export). **First run VOID.** Fixed (faithfulness, decision-bar form, resolution-bar audit, placebo direction, re-pinned tests + complement regression guard; 42/42 1H, 178/178 campaign, boundaries OK). **Blast-radius: 4-agent adversarial audit → defect ISOLATED to harness_1h; W/D/1M verdicts UNAFFECTED.** | **1H = FALSIFIED** (corrected, powered: n_eff prem 151 / disc 92; audit ok=True). prem→down 0.5085/0.4725 (dead); disc→up 0.5641/0.5430 **near-miss** (fails 9-cell penalty by 0.0014). range-LAG transfer clears (0.994/0.000); price-BASIS moot (no PASS). Single benign regime → re-proposal bar = **multi-regime 1H data**, not re-tuning; disc→up = forward-watch belt finding. Lesson [[M-ICT-1H-OFFSET]] (M-15). Cascade **3/5** (W RESOLVED, D SSL-RESOLVED, 1H FALSIFIED). | **Operator exports (next):** the **1M** 16-export ablation (bias×PD×killzone × 2 `useBody`) on the F8 multi-regime window; then `python harness_1m.py`. (1H needs NO 1M export — it falsified at the unconditional gate.) Closure `CLOSURE-1H-FALSIFIED.md`; PREREG-1H 2026-06-19 amendment has the void/fix audit trail. |
| 2026-06-18 (cont. 8) | **D-layer verdict + D-1 smoke-test.** Operator exported **US500 Daily OHLC** (Pepperstone, 4,570 bars, 2008-2026; clean OHLC via Export-chart-data after removing the buggy `ict_daily_dol` from the chart -- its empty-array `for i=0 to size-1` runs *downward* in Pine, a separate drawing bug not needed for D). Ran `harness_d` (fully offline reconstruction; no indicator behind it). | **D-1 smoke-test PASSED** (offline `fvgRate` 0.729 BSL / 0.795 SSL, n=85/156 > 0, NOT pinned ~100% -> the D-1 `barIdx > f.bar` guard works live). **D = side-split: SSL RESOLVED / BSL FALSIFIED.** SSL.fvg (bear-FVG draw) **0.795 > base 0.712**, stationary (halves 0.82/0.77), selectivity-survived -> RESOLVED. BSL.fvg (bull) 0.729 ~= base 0.731; **both pools BELOW base** (0.55/0.34 vs 0.76/0.61 -> pool-draw falsified both sides). Per-side OR gate -> the bear-FVG draw is the real positive finding; single-panel -> path-independent confirmation, not deploy. | **Operator exports (next):** **1H** data-window + paired 1M, then the **1M** 16-export ablation on the multi-regime window; then `python harness_<L>.py`. Cascade **2/5** (W RESOLVED, D SSL-RESOLVED). PR #198 awaiting merge. |
| 2026-06-18 (cont. 7) | **Harness hardening + first layer verdict (W).** Deferred adversarial review = **20 confirmed / 6 rejected, ALL in the offline instruments** (none in the published Pine lib) -> TDD fix-pass + lib publish (Private v1, `jalexante_trades/constellation_ict_lib/1`, behavior-preserving CE10237 `dol()` fix) + 1H price-basis EQ-ALIGN, shipped as [PR #198](https://github.com/Joshua-Asante/multi_firm_operations/pull/198) (177 tests, check_boundaries OK). Operator exported the **US500 Weekly** data-window (Pepperstone, ~2008-2026, all 4 votes on); ran the fixed `harness_w`. | **W = RESOLVED.** structure-only gateHitRate **0.5571**, 95% block-CI **[0.5242, 0.5901]** (lb > 0.50), stationary halves (0.547/0.567) + thirds (0.561/0.555/0.556), eff_N **910** / L_W 1 / 910 scored weeks. **Vote sub-verdict = COMPOSITE-KILLED** -- no vote beats structure-only; **vStruct delta +0.0000 validates the R3-1 prior-pairing fix on live data**; the §4 H-W "vote-adds-nothing" claim is CONFIRMED. Caveats: vSeason inert (empty seasonal months -> untested; doesn't change the verdict); RESOLVED routes to continued-use + a per-entry transfer probe + path-independent confirmation, NOT deploy and NOT a 1M-gate license (H-CASCADE separate). | **Operator exports (next):** D = **Daily US500 OHLC** (switch chart to 1D -> Export chart data), then **1H** data-window + paired 1M, then the **1M** 16-export ablation on the multi-regime window. Then `python harness_<L>.py` per export. **PR #198 awaiting merge.** Optional: §9 formal `CLOSURE-W-RESOLVED.md`. |
| 2026-06-18 (cont. 6) | **Offline front-load** (the run is gated on the operator TV step, so everything pre-run was front-loaded). Authored the 4 per-layer **PREREG-W/D/1H/1M.md** + the **DSR_PBO_LEDGER.md** (joint selection family **M=65**) via an adversarial Workflow (author -> ledger synth -> skeptic review). Review BLOCKed 3 PREREGs + the ledger; **all fixed** (two EDT-as-UTC §0 anchor traps [[platform-display-tz-edt]], D n-floor unit pinned to blocks, ledger false-"committed" provenance -> PROPOSED + OP-GATED inventory + INSUFFICIENT-N gate, W B=10000 flagged GC-3; W/D/1H halves-stationarity made consistent). Built **`_ict_offline.py`** (28-fn faithful detector + pre-registered-stats port, 42 tests) + **harness_{w,d,1h,1m}.py** + TDD tests via a 2nd Workflow: **158 tests pass, check_boundaries clean.** Harness adversarial-review phase died on a session limit -> the load-bearing pieces (detector port / D reconstruction clocks / 1M cost-law) hand-verified instead. Wrote **README.md**. | PREREGs + ledger **PROPOSED / uncommitted** (the commit is the firewall-lift; await operator ratification of the flagged GENUINE CHOICES). Harnesses built + self-tested + **skip-if-no-export**. Pre-Lock checklist: per-layer PREREG-*.md drafted; §8.5 DSR/PBO ledger opened. No `core/` touch. | **Operator:** (1) ratify the flagged GENUINE CHOICES (n-floors; 1M multi-regime window + the 1pt tradeability floor; 1H lookN/eqBand grids) then commit -> lifts the firewalls; (2) **the TV-execution wall** — publish the patched lib Private -> compile the 4 drafts -> 8-run gate-ablation on a genuinely multi-regime window -> export per the README export table. Then the harnesses produce the layer verdicts. |
| 2026-06-18 (cont. 5) | **Killzone filter drafted** (ET, DST-safe via `America/New_York`): `useKillzone` ablation gate + London Open / NY AM (on) / NY PM (off), gates the arm. **Independently reviewed → SHIP-WITH-NITS** (code + DST correct; folded §8 `PREREG-killzone` booking the 8-run ablation + freezing the zone set/windows + arm-time entry-spill disclosure). | All Pine code blockers done (B0–B5 + killzone). Remaining = TV-execution path (yours) + offline tests (D-2/D-3, 1H price-basis). | **You on TV:** publish patched lib → compile 4 drafts → ablation matrix (bias × PD × killzone = 8 runs) on a multi-regime window → export. Then I run the offline layer tests. |
| 2026-06-18 (cont. 4) | **B5 `pvLen` pinned** (1M=2 LOCK / D=3 provisional / 1H=5 exploration; per-layer — pvLen does NOT couple to gate transfers, correcting the synthesis "2/3/5/3"). **D1/B4 independently reviewed → SHIP-WITH-NITS**; folded the fixes (`dolMode` → REPORT-ONLY quarantine so it's not a best-of-K leak; stale line-ref). | B0✅/B1✅/B2-3✅/B4 drafted+reviewed/B5 pinned. Remaining: killzone (needs your session window) + the TV-execution path. | **You on TV:** publish patched lib → compile 4 drafts → first 4 backtests (variant × gate-ablation) on a **multi-regime** window → export. Then I run the offline layer tests. (Optional: I draft the killzone once you give the session window.) |
| 2026-06-18 (cont. 3) | **Operator OVERRODE the anti-SNAG block (B0)** — logged in [`SPX500.md`](lab/archive/../../ops/instruments/SPX500.md). Cleared B0; resolved B1 (orientation fixture → standard-ICT, objection-gated); **drafted B4/D1** (DOL target → opposing range-extreme, design D1(a), `dolMode` input default → unblocks 1M starvation). | B0 ✅ / B1 ✅(objection-gated) / B4 drafted. Now on B5 + the TV-execution path. **1M test window MUST be multi-regime + block-resampled (F8 dissent).** | **D1 target ratify** (range-extreme vs nearest-pool-significance) → **B5 pvLen** pin → publish lib on TV + compile + first 4 backtests (variant × gate-ablation) → export. |
| 2026-06-18 (cont.) | Committed plan (`4bc886a`). Drafted the measurement-correctness slice of B2/B3 into `pine_drafts/` (gitignored; Downloads originals untouched): **B3 D-1** (lib self-touch → `barIdx > f.bar`), **B2-W** (structure-only `gateBias` column + `scored`/`gateScored` exports), **B2-1H** (`[1]`-lagged gate-basis `zoneGate` + on-chart `zone agree%`). See `B2_B3_CHANGES.md`. | Drafts ready but **UNCOMPILED** — the `<your_tv_username>` library import + **B1 orientation** still gate reading any verdict. D-2/D-3 and the 1H price-basis residual remain OFFLINE. Drafts independently Pine-reviewed → SHIP-WITH-NITS (one W overclaim fixed → leg-a/leg-b). **Filed in [`SPX500.md`](lab/archive/../../ops/instruments/SPX500.md): anti-SNAG-BLOCKED 4th concept (1M = D2 geometry family).** | **B0 anti-SNAG override decision** (operator call — SPX500 ledger flags this as the blocked 4th concept) → **B1 orientation sign-off** → publish lib + compile drafts → B4 starvation + D-3 base-rate null (offline). |
| 2026-06-18 | Full read of all 6 files; 11-agent adversarial audit (per-module analyze → refute → synthesize). Authored this plan. **No code fixed, no test run.** | Audit complete. 5 go/no-go blockers identified; 2 of them (D-1 self-touch, the two transfer claims) were missed on the first manual pass and caught by the audit. | **Blocker B1 (FVG orientation sign-off)** — run the orientation fixture as order-0. Then B2/B3 (transfer columns + Daily self-touch/base-rate). See §7.A. |

**Standing rule for this campaign:** no layer verdict is trustworthy until its upstream go/no-go blockers (§7.A) clear. A green offline table is NOT a verdict (the live tables are autocorrelated smoke tests by the scripts' own admission).

---

## §0 — Rule 0 reads (production-source verification)

The ICT Pine sources are **gitignored** (`.gitignore:75` → `**/*.pine`) AND live outside the repo in `C:\Users\joshu\Downloads\`. They were **read verbatim (full contents, with line numbers) in session 2026-06-18** — this is a direct Tier-1 read, not a citation substitute. All line references in this doc are as-of the `LastWriteUTC` snapshots below. **A resuming session MUST re-read the files** (Downloads is mutable; the line numbers drift if the files are edited).

| Source file (Downloads) | Bytes | LastWrite (UTC) anchor |
|---|---|---|
| `constellation_ict_lib.pine` | 10260 | 2026-06-18T15:56:24Z |
| `ict_weekly_bias.pine` | 7542 | 2026-06-18T15:56:20Z |
| `ict_daily_dol.pine` | 8456 | 2026-06-18T15:56:18Z |
| `ict_1h_premium_discount.pine` | 5911 | 2026-06-18T15:56:22Z |
| `ict_1m_execution.pine` | 18163 | 2026-06-18T15:56:17Z |
| `ICT_SYSTEM_DESIGN_1.md` | 27650 | 2026-06-18T15:56:13Z |

Re-anchor command (run at session start): `Get-ChildItem 'C:\Users\joshu\Downloads\*ict*.pine','C:\Users\joshu\Downloads\constellation_ict_lib.pine','C:\Users\joshu\Downloads\ICT_SYSTEM_DESIGN_1.md' | Select Name,LastWriteTimeUtc,Length`

---

## §1 — Context & motivation

Joshua is testing a concept-stage ICT (Inner Circle Trader) top-down system: a shared Pine v6 primitives library plus four consumer scripts (Weekly bias → Daily DOL → 1H Premium/Discount → 1M Execution strategy), each owning one falsifiable hypothesis. The design's stated goal is to convert ICT's buried discretion into explicit, swept-able rules that each emit a falsifiable hit-rate. Standing doctrine that bears: the `strategy-validation` discipline (USDCAD chain, 2026-06-11 — test-ordering by P(changes verdict)/cost, Step-0, cost-law pre-flight, selection-before-sweeps, pre-registration); the feed canon (`tv-csv-canonical-feed-policy`: gate-bearing tests on TV/Pepperstone, bar feeds staging-only); the instrument-ledger governance (read `ops/instruments/<SYMBOL>.md` before instrument R&D). The 2026-06-18 audit found that, **as coded, four of the five layers measure something other than their stated claim** — this plan exists to gate testing behind the fixes/ratifications that restore interpretability.

---

## §2 — Prior art / lineage

- **`strategy-validation` skill (USDCAD chain, 2026-06-11)** — the test mechanics this plan inherits: Step-0 panel integrity, cost-law in R (cost ∝ price/stop_dist), excursion-bounded counterfactuals, selection/permutation before plateaus, pre-registration. The ICT 1M cost-law is the same instrument that killed USDCAD (0.097R at 1.42×ATR).
- **`tv-csv-canonical-feed-policy` (PR #175, 2026-06-12; superseded §2.3 on 2026-06-17)** — canonical analyses on TV exports/official series; bar-export now canonical producer. Gate-bearing ICT tests use TV/Pepperstone SPX-class feed.
- **`ICT_SYSTEM_DESIGN_1.md`** — the design doc. Its §6 flags (FVG orientation, bridge schema, library publish, "I can't compile Pine here"), §8 parameter buckets, §9 faithfulness protocol, and §11 open decisions (D1 DOL target, D2 raid rejection, D3 FVG entry) are the author's own surfaced risks; this plan verifies them against code.
- **Repo R&D-pipeline precedent** — concept→codify→sweep→validate; ρ≥0.70 + parity-band≤2% pre-registered; native-parity pre-gate (USOIL-RGC Gate B). The 1H→1M "transfer" question here is the same native-parity shape: does the cheap proxy measure what the live gate uses?
- **Memory anchors that bear:** `feedback_parity_gate_feed_and_pf_calibration` (feed-source breaks parity), `feedback_static_equity_default_for_param_compare` (TV compounding artifact), `reference_dj30_ddcap...` / NAS100 `contractValue=10` sizing-bug class (the `pointVal` finding E3), `feedback_oanda_dow_feed_artifact` (DOW slices), `portfolio_mc_1r_fallback_trap`.
- **NOT a novel surface — prior ICT art on this instrument (ledger read 2026-06-18):** [`ops/instruments/SPX500.md`](lab/archive/../../ops/instruments/SPX500.md) records **D2 / `Q-ICT-SWEEPFVG-1`** (sweep→FVG→opposing-pool draw, US500 15m) **FALSIFIED 2026-06-17** on §6 robustness — the **1M execution layer here is the same ICT-geometry family**. The instrument's **anti-SNAG budget is firing (3 nulls / 3 families)**, so this cascade is the warned-of **4th concept → anti-SNAG-BLOCKED** pending operator override (§7.A B0). Ledger findings that bind this campaign: **F6** (direction real, p=0.0144 — supporting belt), **F8** (pseudo-replication / tradeability floor `stop_dist ≥ max(1pt,cost)`), **F7** (asymmetric overnight swap), **W2** (`contractValue` TBD — independently the audit's E3 `pointVal=1.0` finding).

---

## §3 — Question

**Pre-Q gate (symptom-only rephrase):** "Each ICT layer prints a hit-rate that is claimed to be falsifiable and to license the live 1M gate; what does each layer actually measure, and does any layer's number bear on the claim/gate it is cited for?" (Names the symptom — uninterpretable measurements — not a fix.)

**Q-ICT-CASCADE-1 (parent):** For each layer of the ICT cascade, does the script as coded measure its stated falsifiable claim, and do the cheap offline layer tests transfer to the live 1M execution gate they are built to license?

Forked module sub-questions (each runnable on its own export; gated independently in §6):

- **Q-ICT-LIB** — Do the shared primitives faithfully and consistently encode the convention every consumer assumes (orientation, edges, clocks, ties)?
- **Q-ICT-W** — Does last week's bias predict next-week direction > 0.5, beating structure-only, surviving best-of-K — and does that hit-rate transfer to the 1M `structBias` gate?
- **Q-ICT-D** — Do pools / FVGs draw price within K days better than a radius-matched base rate, fairly compared?
- **Q-ICT-1H** — Does the premium/discount split carry directional follow-through > coin flip, and does the 1H zone transfer to the 1M PD gate?
- **Q-ICT-1M** — Is post-cost E[R] > 0 and ≥ 4× the cost hurdle, surviving the wick/body split, gate ablation, and a DOW/session permutation — at sufficient n to bound the CI?

---

## §4 — Falsifiable hypotheses

**Cascade-level (the load-bearing transfer claim):**
**H-CASCADE:** *If* the W structure-only hit-rate and the 1H follow-through rate are measured on the **same object/basis the 1M gate uses** (structBias-only per-entry; 1-min close vs `[1]`-lagged hourly range), *then* a layer PASS licenses the corresponding 1M gate; *otherwise* the offline layer economy is invalid and the only valid evidence is the full 1M end-to-end run.
- **Reject** if 1H-zone↔1M-gate-zone sign-agreement < 90% OR rate gap > 3pp (E1 transfer test), OR if the W headline rate is computed on the composite vote rather than structBias-only.
- **Accept** if both transfer pre-gates clear (W structure-only column isolated; 1H native-basis agreement ≥ 90% AND rate gap ≤ 3pp).

**Per layer:**
- **H-LIB:** Orientation as coded (standard ICT BISI/SIBI: bull FVG = `low[0] > high[2]`) matches Joshua's intended convention and every consumer's near/far reads. *Reject* if the orientation fixture shows a consumer near/far comment disagreeing with lib output, or if the intended convention is the brief's prose (→ flip + re-verify all consumers).
- **H-W:** P(bias correct) > 0.5 (structure-only, autocorrelation-corrected CI). *Reject* if corrected 95% CI straddles 0.50. *Vote-adds-nothing* if no non-structure input solo-beats structure-only after the best-of-K penalty (composite-vote claim killed; structure-only stands/falls on its own CI).
- **H-D:** corrected poolRate and/or fvgRate exceeds the radius-matched base rate by > 95% bootstrap CI half-width. *Reject the layer* if neither clears the base rate after D-1/D-2/D-3 fixes.
- **H-1H:** de-overlapped prem→down OR disc→up rate CI lies > 0.5 by ≥ 2pp under BOTH stride and block-bootstrap estimators, AND beats the random-EQ placebo. *Reject* if both rates straddle 0.5 across anchor rules after the multiplicity penalty (split is decorative).
- **H-1M:** post-cost E[R] CI lower bound > `minRmult × median-hurdle` at n ≥ 100, with each retained gate showing positive marginal E[R] (CI excludes 0) and no single DOW/session slice carrying the edge beyond the permutation null. *Reject* if E[R] CI ⊆ (−∞, hurdle], OR both gates add nothing, OR the edge lives in one slice, OR n < 100 (→ `INSUFFICIENT-N`, claim unfalsifiable on this data).

---

## §5 — Forbidden moves

- **Reading the live on-chart tables as the verdict.** premRate/discRate (1H), poolRate/fvgRate/dolRate (D), hitRate (W) are computed over **overlapping/autocorrelated** windows and the scripts say so (`ict_1h:15-16`, `ict_daily:131-132`). The verdict is the **de-overlapped offline** estimate only. Citing the table number is the autocorrelation trap.
- **Sweeping any parameter before the selection-level tests run.** Plateau ≠ validity (strategy-validation §0). A plateau around a spurious selection still passes. Orientation → pvLen → selection tests (placebo/permutation/transfer) come first; plateaus last.
- **Crediting a layer PASS to the 1M gate before the transfer pre-gate (§7.A B2) clears.** This is the cascade's load-bearing failure (W-1, E1). A W/1H PASS measured on the wrong object/basis licenses nothing.
- **Silently "fixing" the faithfulness / definitional knobs.** DOL target (D1), FVG edge convention, raid-rejection, killzone, orientation — these are *definitional choices to ratify* (§B), not bugs to patch. Patching one before ratifying changes what the system claims to be (the Iran/Hormuz silent-relabel shape). Flag, ratify, then change.
- **Outcome-conditional tuning.** e.g. "drop the no-draw skips, then measure E[R]," or choosing `eqBand`/`minAbsR` to fatten n and then reading the rate on that n. n-throttle knobs (`eqBand`, `minAbsR`, `useDOL`) must report n-per-cell so an n-driven "win" is visible (multiplicity §C).
- **Locking a knob without booking its selection into the §8.5 DSR/PBO ledger.** ~16 LOCK knobs + two best-of-K grids (1H anchor×lookN×eqBand; W vote set) — the lock *order* mitigates dependence, not family-wise error.
- **Treating the default-config run as evidence about the ablation arms.** Several defects (double-raid short-bias LIB-5/E6; W composite-vote transfer break) are **dormant in the default and live only in the mandated ablation/importance arm**. Audit the arm-specific path, not just the default.
- **Using a $-denominated metric off the raw TV print.** `strategy.equity` compounds and `pointVal=1.0` mis-scales index notional; the headline currency is **R**, and any $/DD criterion uses the recomputed static-$200K series.

---

## §6 — Gate criteria (closure verdict, per layer)

Each sub-question closes independently. Pre-register the exact thresholds in §8 before the first run of each.

| Layer | RESOLVED | FALSIFIED | AMBIGUOUS-HOLD |
|---|---|---|---|
| **LIB** | Orientation fixture passes AND pd/dol unit battery passes AND edge/clock conventions ratified (§B) | Orientation flip required and not intended → system inverted | Convention undecided → hold, no downstream run |
| **W** | Structure-only corrected 95% CI lower bound > 0.50 AND stationary across halves/thirds | Corrected CI straddles 0.50 | CI > 0.50 but non-stationary (one-regime) → hold, name re-test window |
| **D** | Corrected poolRate and/or fvgRate > base_rate + CI, on matched footing (D-1/2/3 fixed) | Neither clears base_rate after fixes | Clears only on one censoring/selectivity convention → hold |
| **1H** | De-overlapped rate CI > 0.5 by ≥2pp (both estimators) AND beats placebo AND transfer pre-gate clears | Both rates straddle 0.5 across anchors after penalty | Clears unconditional but fails the bias-conditioned (gate-relevant) variant → hold |
| **1M** | E[R] CI lower bound > 4× hurdle at n≥100, gates earn marginal E[R], survives DOW/session permutation | E[R] CI ⊆ (−∞, hurdle] OR gates add nothing OR one-slice edge | `INSUFFICIENT-N` (n<100 after starvation fix) — re-spec target, re-test |

**Pre-registered before any data touches analysis.** Amending §6 mid-campaign to match emerging evidence is methodology-layer p-hacking (close AMBIGUOUS, capture why, open fresh).

---

## §7 — Execution plan

### §7.A — GO/NO-GO BLOCKERS (resolve BEFORE any layer verdict; ranked by P(invalidate-everything) ÷ cost)

> None requires running the strategy. All are code/offline/ratification fixes that gate interpretability. **Work top-down; do not read any layer verdict until its upstream blockers clear.**

**B0 — instrument-governance gate (anti-SNAG) — ✅ CLEARED (operator override 2026-06-18, logged in `SPX500.md`)**
- The [`SPX500.md` ledger](lab/archive/../../ops/instruments/SPX500.md) flagged this cascade as the anti-SNAG **4th SPX500 concept** (1M raid→FVG layer = **same ICT-geometry family as the FALSIFIED D2**, on a 3-null/3-family instrument). The operator **explicitly waived** the D2/SNAG re-proposal bar 2026-06-18; the cascade proceeds to B1–B5.
- **Dissent retained — binds the DESIGN, not the override:** because the 1M layer is the D2 family, the 1M test is now under hard pre-registration constraints — a genuinely **multi-regime** window, **block-resampling by entry event**, and the **tradeability floor** `stop_dist ≥ max(1pt, cost)` (ledger F8). A single benign window would reproduce D2's exact failure mode (drop-top-k carried, thirds back-loaded). This is a constraint on the test, no longer a gate.

**B1 — FVG orientation sign-off** *(order-0; one-line cost, total cost if wrong)*
- Code: `constellation_ict_lib.pine:45-48` codes standard ICT (bull = `low[0] > high[2]`). The design brief prose ("bullish = low two-back above current high") describes the **bearish** case. Code is internally self-consistent across all consumers — **NOT a coded bug** — but a wrong intended-convention call silently passes a fully-inverted system.
- Do: build a hand-constructed bullish-displacement 3-bar fixture (replay or seeded series); confirm `bullFVG` fires and the 1M prints long bias / Daily prints draw-up. Cross-check consumer near/far comments (`1m:189`, `1m:220`, `lib:126/129`).
- Gate: PASS iff standard-ICT-as-coded is what Joshua intends (almost certainly yes). Annotate the brief prose as loose. **No other test is interpretable before this.**
- **✅ RESOLUTION 2026-06-18 — CONFIRMED standard-ICT; proceeding (objection-gated).** Fixture (worked example): a bull-displacement 3-bar pattern with `high[2] = 100.0`, `low[0] = 100.5` ⇒ `bullFVG = (low[0] > high[2]) = (100.5 > 100.0) = TRUE`; `bullBounds ⇒ top = low[0] = 100.5 (NEAR), bot = high[2] = 100.0 (FAR)`; a long arms after an SSL sweep + this bull FVG and draws UP. That is standard ICT BISI/SIBI and matches every consumer's near/far reads (audit-verified, internally consistent). **Proceeding on standard-ICT. Object ONLY if your intended convention is the brief's bearish prose** ("bullish = low two-back above current high") — a one-line flip in `bullFVG`/`bearFVG`/bounds that inverts the entire system.

**B2 — Restore the two transfer claims** *(breaks the cascade's reason to exist)*
- W (`weekly:85-89` composite vote vs `1m:91-92` structBias-only): add a **structure-only "GATE bias" column** to the W export; pre-register that ONLY it transfers; label the composite-vote rate RESEARCH.
- 1H (`1h:46-55` [0]-fresh/1H-close zone vs `1m:94-100` [1]-lagged/1M-close zone): run the **native-basis transfer pre-gate** — re-score the 1H on the gate's actual 1-min/[1]-lagged hourly-range zone, measure sign-agreement + rate gap (H-CASCADE thresholds). If the gap is material, the only valid evidence is the full 1M end-to-end run.

**B3 — Make the Daily layer measurable** *(currently measures nothing)*
- D-1 self-touch: change `markTouchedFVGs` to require a strictly-later touch (`barIdx > f.bar`, or start the touch scan at `f.bar+1`). Offline equivalent: start each FVG's K-window at `f.bar+1`.
- D-3 base-rate null: compute the radius-matched random-level base rate offline (bootstrap CI), pre-register the pass band. **The layer cannot be falsified until this null exists.**
- D-2 clock asymmetry: start pool and FVG K-windows from a common origin (recover sweeps inside the pvLen confirmation window for pools).

**B4 — Confirm the 1M can produce trades at all** *(starvation → unfalsifiable)*
- Run the starvation diagnostic (§7.B, 1M order-1): `ordPlaced`/`skipCost` under `useDOL` on vs off. If nearest-pool starves n→0, **re-spec the DOL target to opposing range-extreme liquidity** (doc D1 candidate (a), unifies with the 1H range); quarantine nearest-pool. Pre-register which target definition the claim is tested against.

**B5 — `pvLen` pin — ✅ DRAFTED 2026-06-18 (per-layer pre-registration)**
- Ground truth (grep): `pvLen` is in **3 files** (Weekly = EMA, no pvLen; lib = passed-in): **Daily=3** (pool universe for the draw-rate), **1H=5** (swing-pair anchor **only** — the gate uses lookback-extremes, so pvLen is **inert for the gate path**), **1M=2** (raid pools). **Correction to the earlier synthesis ("2/3/5/3 / four files / compounds the transfer failure"):** pvLen is load-bearing *within* each layer (1M raid detection, Daily pool universe) but does **NOT** couple to the W/1H→1M gate transfers (EMA / lookback-extremes, not pvLen pivots).
- **Pin (per-layer — the values mean different things at different TFs/roles, so homogenizing is wrong):** **1M=2 LOCKED** (gate-bearing; marked in the draft tooltip), **Daily=3 provisional** (measurement knob — sweep {2,3,5} per §7.B D-4), **1H=5 exploration-only** (swing-pair; not the gate). Recorded in §8 `PREREG-pvLen`.
- Still owed: the D-2 back-stamp clock fix is **offline** (not a Pine edit — the pool doesn't exist during its confirmation lag); handled in the §7.B D reconstruction.

### §7.B — Per-module ordered test plans

Each step lists what / how / data / pass-fail / which null it kills. Verdict is always the **de-overlapped offline** estimate. Feed = canonical TV/Pepperstone SPX-class.

**LIB (foundation):**
1. **Orientation fixture** (= B1). Synthetic bull/bear/no-gap/body-edge 3-bar fixtures; confirm `bullFVG`/bounds and consumer-edge agreement.
2. **pd()/dol() unit battery.** px on EQ / EQ±band; `eqBand=0`; `rHigh==rLow`; all-na and exact-tie distances. PASS iff ties → 0/stand-down, EQ-edge → stand-down (verified correct as coded; pin it).

**W — Weekly bias:**
1. **Step-0 + de-overlap.** Export the 7 data-window series; one row per *confirmed* week; drop the live bar; record outcome autocorrelation. Note the `hit` column collapses miss/stand-down/flat into 0 — recompute `scored = bias[1]!=0 and outcome!=0` from `bias`/`outcome` columns (don't trust `hit`).
2. **Structure-only baseline CI** *(headline)*. `nHit/nScored`, votes off, with a **moving-block bootstrap** CI (block from step-1 autocorrelation) — NOT binomial. KILL if corrected 95% CI straddles 0.50.
3. **Per-input importance (best-of-K).** Solo hit-rate per vote vs structure-only; max-statistic permutation penalty over the 4 inputs. **Regenerate vRates without repaint** (`close[1]`, W-2). Vote dies if no input beats baseline after penalty.
4. **Label-permutation placebo** on the composite (block-permute).
5. **Halves/thirds stationarity.**
6. **Gate-transfer probe** (= B2-W). 1M bias-gate ablation; compare per-entry directional accuracy to the weekly-close hit-rate.

**D — Daily DOL:**
1. **Self-touch sanity** (= B3 D-1). Read `fvgRate`; if ≥0.98 across ≥3 symbols, confirmed broken. Patch, re-read.
2. **Offline base-rate null** (= B3 D-3). Radius-matched random pseudo-levels per side, MC ≥5000, bootstrap CI.
3. **Fair re-measurement** (= B3 D-2 / B5). Common-origin clocks, identical censoring; two-proportion test on `poolRate − fvgRate`.
4. **Filtered-vs-unfiltered probe.** `dispMlt ∈ {0,1.5,3.0}` × `pvLen ∈ {2,3,5}`; if draw-rate tracks selectivity, restate as a matched-selectivity comparison.
5. **Censoring + halves stationarity.**

**1H — Premium/Discount:**
1. **Step-0 + overlap census.** Native 1H; effective independent windows = `floor(N_scored / fwdK)`.
2. **Non-overlapping de-overlap** *(gate-bearing)*. Stride-by-`fwdK` (primary) + moving-block bootstrap (cross-check). PASS iff a rate's CI clears 0.5 by ≥2pp under both.
3. **Regression-to-the-range placebo.** Random-EQ / sign-shuffle null; real rate must beat it (a [0]-fresh range extreme mean-reverts mechanically).
4. **Anchor sweep with pre-registered penalty.** `anchor × lookN × eqBand`, declare cell count first, deflated-Sharpe/Bonferroni; winner must clear 0.5 after penalty.
5. **1H→1M transfer falsifier** (= B2-1H). Sign-agreement + rate gap on the gate's native basis.
6. **premHit/discHit look-ahead audit.** Reproduce the rate from raw `zone`/`close`; if mismatch, discard the columns.
7. **Halves/thirds stationarity.** (Also add a **bias-conditioned** variant — split by sign of weekly structBias — since the 1M only trades bias∧PD, never PD alone.)

**1M — Execution:**
0. **Step-0 + n-floor.** Entry-minute census (not all `:00`), DOW/session census, dup detection; **HALT if closedtrades < 100.**
1. **Starvation diagnostic** (= B4). `skipCost`/`ordPlaced` under `useDOL` on/off.
2. **Cost-law confirmation.** Hand-recompute `cost_R` on 5 trades vs TV realized cost. Units verified to agree (`commission_value=0.002`% = `commPct=0.00002` fraction; `slippage=1`=`slipTk=1`) — confirm empirically and pin with a comment so a future edit can't desync them.
3. **Variant split** `useBody` true/false — two frozen pre-registered configs; post-cost E[R] + bootstrap CI.
4. **Gate ablation** — **8 runs** (bias × PD × **killzone**, all on/off combos); each gate must lift E[R] (CI excludes 0), not just prune n. (3 gates now — booked in §8 `PREREG-killzone`.)
5. **`useDOL` vs fixed-R** at comparable n.
6. **Best-of-K DOW/session permutation** — on the **post-killzone** population, partition by DOW and by **arm-time** killzone; kill if the edge concentrates in one slice beyond the permutation null. (The killzone is now a pre-registered in-code gate, so this is the concentration check WITHIN the gated trades — not a separate session axis; no double-count.)
7. **Static-$200K recompute** — strip `strategy.equity` compounding; evaluate $/DD on the static series.
8. **Parameter plateaus — last only**, in the doc §8 lock order, DSR/PBO-budgeted.

---

## §8 — Verdict pre-registration (mandatory before each layer's first run)

Per layer, before Phase 1 of that layer, write the exact thresholds (the §6 row + numeric values: minimum effective-n post-de-overlap, CI method + block length, multiplicity cell count + penalty, base-rate MC size, permutation B). Stamp the date and, once this campaign dir is committed, the commit hash. **A power floor is mandatory** (e.g. minimum effective-n for "CI straddles 0.5" to be a decision rather than `INSUFFICIENT-N`) — several layers route the verdict to a block-bootstrap and a starved layer otherwise returns ambiguity indistinguishable from a null.

Stubs (fill before run 1):
- `PREREG-W.md` — n-floor, bootstrap block length, best-of-K cell count + penalty.
- `PREREG-D.md` — base-rate MC size + radius-match definition, clock-origin convention, selectivity-match definition.
- `PREREG-1H.md` — de-overlap stride/block, placebo design, anchor×lookN×eqBand grid cardinality + penalty, transfer agreement/gap thresholds.
- `PREREG-1M.md` — n-floor (≥100), cost-hurdle multiple, ablation marginal-E[R] CI rule, permutation B, DOL-target definition under test.
- **`PREREG-pvLen` (✅ pinned 2026-06-18)** — **1M=2 LOCKED** (gate-bearing raid-pool strength); **Daily=3 provisional** (draw-rate measurement knob, sweep {2,3,5}); **1H=5 exploration-only** (swing-pair; gate uses lookback-extremes). Per-layer by design (different TF/role); pvLen does NOT couple to the gate transfers. Any change to 1M=2 voids the validation.
- **`PREREG-dolMode` (✅ pinned 2026-06-18)** — gate-bearing DOL target = **range-extreme** (design D1(a)). **`nearest-pool` is REPORT-ONLY:** descriptive variant, NOT eligible for the lock decision and does NOT consume a best-of-K / permutation budget (closes the dolMode selection-leak the D1 review flagged).
- **`PREREG-killzone` (✅ booked 2026-06-18)** — `useKillzone` is the 3rd ablation gate → the gate-ablation matrix is **2³ = 8 runs** (bias × PD × killzone), booked against the §8.5 DSR/PBO budget. **FROZEN (not swept):** zone set = London Open `0200-0500` + NY AM `0700-1000` **ON**, NY PM `1330-1600` **OFF**, all ET windows fixed — the per-zone toggles + window edits are NOT a best-of-K surface. Gates the **arm**; the §6 one-slice test slices by **arm-time** zone (entry may spill ≤ raidWin bars past the window).

---

## §9 — Closure record format

Per layer, on gate firing: `lab/analysis/ict_cascade_2026-06-18/CLOSURE-<layer>-<verdict>.md` with: verdict, anchor numbers vs gate thresholds, what the pre-registration predicted vs what happened, "which nulls remain alive" delta (§D), lesson candidates with dollar/dated anchor. Update the Progress Ledger. The cascade closes when all five layers close or a §7.A blocker is declared fatal.

---

## §10 — Audit hooks (runnable)

```bash
# --- §0 re-anchor (run at session start; files are mutable, outside the repo) ---
#   PowerShell:
#   Get-ChildItem 'C:\Users\joshu\Downloads\*ict*.pine','C:\Users\joshu\Downloads\constellation_ict_lib.pine' |
#     Select Name,LastWriteTimeUtc,Length
#   If LastWriteUTC differs from §0 table -> RE-READ before trusting any line citation.

# --- B1 orientation (interpretability gate) ---
#   Until signed off, every downstream number is suspect. Confirm in fixture:
#   bull fixture (low[0] > high[2]) -> bullFVG true -> 1M prints long / Daily draw-up.

# --- B3 D-1 self-touch falsifier (fastest eyeball check in the whole cascade) ---
#   First Daily backtest run: if the "FVG draw-rate" table cell reads 100.0%
#   (fvg n > 0), the self-touch bug is live and fvgRate measures nothing.
#   Target after fix: fvgRate < 1.0 and tracks a plausible touch frequency.

# --- B4 starvation (1M unfalsifiable check) ---
#   1M table: if skip:cost/R dominates and closedtrades < 100 under useDOL=true,
#   the E[R] CI is unbounded -> INSUFFICIENT-N, re-spec target before any verdict.

# --- E2 session-filter absence (faithfulness) — grep the Pine for any time gate ---
grep -nE 'hour\(|session|killzone|time\(|input\.session' 'C:\Users\joshu\Downloads\ict_1m_execution.pine'
#   Expected today: only the comment at :14. Any zero matches in logic => no killzone gate.

# --- Cost-law unit equivalence (must stay true after any edit) ---
#   strategy.commission.percent value 0.002  ==  0.002%  ==  0.00002 fraction  ==  commPct
#   slippage 1 tick == slipTk 1.  If a future edit changes one side only -> gate desyncs.

# --- pvLen reconciliation (B5) — confirm one value or a pre-registered per-layer note ---
grep -nE 'pvLen|Swing strength' 'C:\Users\joshu\Downloads\ict_daily_dol.pine' \
  'C:\Users\joshu\Downloads\ict_1h_premium_discount.pine' \
  'C:\Users\joshu\Downloads\ict_1m_execution.pine'
#   Today: D=3, 1H=5 (pivot strength), 1M=2. Pin or pre-register the difference.
```

---

## Appendix A — Critical-error registry (post-adversarial-verification severities)

Severities are the **verifier-corrected** values (↓ = down-weighted from the analyst's first call). Class: A-compile / B-measurement / C-faithfulness / D-operational.

| ID | Sev | Class | Location | Issue (one line) |
|----|-----|-------|----------|------|
| **D-1** | CRIT | B | `lib:126` + `daily:51,58,88` | FVG self-touch on registration bar → `fvgRate` mechanically ~100%, miss-branch is dead code |
| **D-3** | CRIT | B | `daily:14,168-171` | Base-rate null the KILL condition names is never computed → layer unfalsifiable |
| **D-2** | CRIT | B | `daily:40,43,57,80` | Pool back-stamp blind window → pool/FVG clocks asymmetric by ~pvLen |
| **W-1** | CRIT | C | `weekly:85-89` vs `1m:91-92` | Weekly transfer false: composite-vote table ≠ structBias-only gate (and weekly-close ≠ per-entry) |
| **1H-E1** | CRIT | C | `1h:46-55` vs `1m:94-100` | 1H transfer false: [0]-fresh/1H-close zone ≠ [1]-lagged/1M-close gate zone (different conditional support) |
| **1M-E1** | HIGH ↓ | D | `1m:66,194,225` | Trade starvation (nearest-pool target) → n→0 → E[R] CI unbounded (was CRIT; starves, tunable) |
| **LIB-2 / D-4** | HIGH | B/C | `daily:42-45` vs `49-54` | Unfiltered pools vs displacement-filtered FVGs → "fair comparison" confounded by selectivity |
| **D-2b (missed)** | HIGH | B | `daily:43,45` vs `51,54` | K-window ORIGIN asymmetry: pool t0 = pivot−pvLen, FVG t0 = registration (compounds D-2) |
| **1M-E2** | HIGH | C | `1m` (absence) | No killzone/session filter — 24h trading dilutes edge AND rigs the one-slice kill both ways |
| **1M-E3** | HIGH | D | `1m:71,202,233` | `pointVal=1.0` on an index = contractValue-bug class — breaks $/dd_protection sizing, **NOT the R-claim** |
| **W-3** | MED ↓ | B | `weekly:94,108` | Hit-rate denominator (`nScored`) censors stand-down/flat; table bias-up/dn on a different base |
| **W-4** | MED | B | `weekly:101-108` | Running proportion, no CI; autocorrelated weekly regimes → effective-n ≪ nScored |
| **W-2** | MED ↓ | B | `weekly:76` | Rates vote repaints (no `[1]`) — only live table (nScored is isconfirmed-gated); rates default-off |
| **W-5** | MED | D | `weekly:31-49` | Votes default-off + empty months → single export has only vStruct live; importance test needs all-on run |
| **W-6** | MED | C | `weekly:68-69` | Structure = plain EMA cross; library import unused in W → proxy, not an ICT mechanism |
| **LIB-1** | MED ↓ | B | `lib:155` vs `169` | `nearestFVG` midpoint vs `nearestPool` level → pool-biased magnet (confined to quarantined dolBias) |
| **LIB-4** | MED | B | `lib:71-73` | `displacement` range on [1] but ATR at [0] includes the displacement candle + successor (contaminated denom) |
| **LIB-5 / 1M-E6** | MED | D/C | `1m:145-163` | Raid *rejection* not formalized; same-bar double-raid arms SHORT by code order — **only in gates-off ablation arm** |
| **1M-E4** | MED ↓ | B | `1m:202,233` | `strategy.equity` compounding ≠ static-$200K (recoverable in post; R-claim invariant) |
| **1H-E2** | HIGH | B | `1h:60-65,72-82` | Overlapping windows reported as iid (fwdK=12) — no valid CI vs 0.5 |
| **1H-E4** | HIGH | B | `1h:22-29,46-55` | anchor×lookN×eqBand free + "maximize" claim → best-of-K manufactures >0.5 without penalty |
| **1H-E3** | HIGH | C | `1h:9-14` vs `1m:104-107` | 1H measures unconditional reversion; 1M only trades bias∧PD (trend-continuation) — wrong conditional |
| **1H-E5** | MED | B | `1h:46-55` | Regression-to-the-range confound: a [0]-fresh extreme reverts mechanically, inflating the rate |
| **1H-E6** | MED | D | `1h:29` | `eqBand` is both a measurement knob and an n-throttle (→0 scores every bar, worsens overlap) |
| **1M-E5** | MED | B | `1m:252-254` | Fill-by-not-flat one-bar lag → `fillRate` undercounts intrabar round-trips (not PF/closedtrades) |
| **1M-A4/zone-flicker (missed)** | MED | B | `1m:100,256-262` | Flip/expire cancel runs every bar (not isconfirmed-gated) → live intrabar zone flicker can cancel a resting limit |
| **D-6** | LOW | C | `daily:108,120` | "nearest N" loops select by recency, not distance — display/faithfulness only |
| **D-7 / LIB-6** | LOW | A/D | `lib:80-81,116-117` | FIFO eviction survivorship + na-int latent trap — dormant at maxReg=5000/daily, live on intraday |
| **E7 (1H import)** | MED ↓ | A | `1h:19` | `<your_tv_username>` placeholder + unpublished library → script does not compile until resolved (blocks all testing) |

**Verified positives (don't re-flag as bugs):** every library for-loop is guarded by `size>0` (no empty-array underflow); FVG near/far edges internally consistent end-to-end; `displacement` correctly takes ATR as a param (avoids ta.* in-library gotcha); `pd()`/`dol()` boundary + tie handling correct; non-repaint HTF via `[1]` inside `request.security` (1M) is correct; cost-law units agree; R-invariance to `pointVal` is a genuine strength for the R-claim; ablation/variant toggles physically re-route logic; skip-counter instrumentation is first-class; flipped-gate limit cancel is handled.

---

## Appendix B — Ambiguities to ratify (definitional calls — NOT bugs; decide before run 1)

1. **FVG orientation** (B1) — confirm standard-ICT-as-coded is intended. One-line flip if not; getting it wrong passes a fully-inverted system.
2. **DOL target (doc D1)** — nearest-pool (starves n) vs **opposing range-extreme** (recommended: meaningful R, unifies with P/D range) vs fixed-R. The claim's R depends entirely on this.
3. **FVG edge convention** — near-edge (scoring/touch) vs midpoint (magnet) vs mid/CE (entry). At minimum make scoring and magnet the *same* edge so dolBias isn't pool-biased.
4. **Pool draw clock origin** — true pivot bar (faithful, needs offline reconstruction) vs confirmation bar (simple, like-for-like). Pre-register; reject the current mixed convention.
5. **Raid definition** — inclusive touch (`>=`/`<=`, current, symmetric) vs strict penetration (a true stop-hunt). Keep symmetric for the Daily fairness; consider strict for the 1M arm separately.
6. **Killzone/session filter — ✅ DRAFTED 2026-06-18 (ET, DST-safe).** `useKillzone` ablation gate + London Open `0200-0500` / NY AM `0700-1000` (on) / NY PM `1330-1600` (off), all ET via `America/New_York` (auto EST/EDT — resolves the repo EDT-display trap). Frozen + booked in §8 `PREREG-killzone`. Gates the arm; reviewed SHIP-WITH-NITS.
7. **Flat-week scoring (W)** — exclude (current) vs count-as-miss vs report-separately. Recommend report-separately + exclude from the directional rate; pre-register.

---

## Appendix C — Cross-cutting findings & multiplicity

- **Two transfer claims false as coded (CRIT)** — the cascade's cost-saving premise (cheap offline layer test licenses the live gate) is broken at the W and 1H joints. Until B2 fixes them, offline layer verdicts are decoupled from the gate. *This is the single most invalidating finding.*
- **`pvLen` inconsistency (2/3/5 across the 3 files that use it) (HIGH → PINNED 2026-06-18)** — each layer tests a different swing universe; load-bearing *within* a layer (1M raid detection, Daily pool universe) and the root of the D-2 clock asymmetry. **Correction:** it does **NOT** compound the gate transfers (W=EMA, 1H gate=lookback-extremes, not pvLen). Pinned per-layer (1M=2 LOCK / Daily=3 provisional / 1H=5 exploration-only) — §7.A B5, §8.
- **FVG orientation single-point flip (HIGH)** — not a coded bug, but the one convention whose inversion inverts everything, silently.
- **Daily structurally unfalsifiable + confounded 4 ways (HIGH)** — D-1, D-3, D-2, D-4 all stack on the same headline claim.
- **Dormant-in-default / live-in-ablation pattern (HIGH)** — double-raid short-bias and W composite-vote break are invisible in the default config and active exactly in the mandated ablation/importance arms. "The default passed" is false reassurance.
- **Multiplicity (HIGH)** — ~16 LOCK knobs + two explicit best-of-K grids (1H anchor×lookN×eqBand; W vote set), with `eqBand`/`minAbsR`/`useDOL` doubling as n-throttles, and several per-knob nulls uncalibrated (D base-rate absent; 1H regression-to-range un-subtracted). The pre-registered lock *order* reduces sequential dependence but does NOT bound family-wise error. Required: declare every grid's cardinality, book each into the §8.5 DSR/PBO ledger, apply a per-cell penalty, report n-per-cell for n-throttle knobs, and state a joint DSR/PBO budget over the UNION of selection surfaces.

---

## Appendix D — "Which nulls remain alive" ledger (per strategy-validation §0)

Seed (update as tests fire):
- **All five layers:** every null is alive — no test has run.
- Permutation tests (when run) kill random-labeling, **NOT path-overfit** — log path-overfit as still-alive after any 1M/1H/W permutation.
- Selectivity confound (D-4), regression-to-the-range (1H-E5), and the bias-conditioned-vs-unconditional gap (1H-E3) are nulls that survive a naive >0.5 rate — each needs its named placebo.

---

## Verification

```bash
# Discipline checks (mechanical) — campaign-tracker variant of the Pre-Q template
$ python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" \
    "lab/analysis/ict_cascade_2026-06-18/TEST_PLAN.md" --type inquire
#   Expected: §0/§4/§5/§6/§10 populated; note this is a 5-forked-sub-claim campaign,
#   not a single-Q brief (per parent-Q convention; trap #11 handled by forking).

# §0 Rule-0 confirmation (sources are outside the repo, gitignored)
$ Get-ChildItem 'C:\Users\joshu\Downloads\*ict*.pine' | Select Name,LastWriteTimeUtc,Length
#   Confirm LastWriteUTC matches the §0 table; if not, re-read before trusting line citations.

# Cross-reference: confirm the .pine gitignore that drove citation-mode
$ grep -n '\*\*/\*\.pine' .gitignore     # expect a hit (line 75)
```

---

## Pre-Lock Checklist (remove once locked)

- [ ] B1 orientation signed off (intended convention confirmed, brief prose annotated)
- [ ] B2 transfer columns added (W structure-only GATE column; 1H native-basis transfer pre-gate run)
- [ ] B3 Daily fixes (D-1 touch at `f.bar+1`; D-3 base-rate null; D-2 common-origin clocks)
- [ ] B4 1M starvation diagnostic run; DOL target ratified (D1)
- [ ] B5 pvLen pinned/pre-registered; back-stamp clock fixed
- [ ] Per-layer PREREG-*.md committed BEFORE that layer's run 1 (incl. n-floor)
- [ ] §8.5 DSR/PBO ledger opened; grid cardinalities declared
- [ ] Killzone/DST convention pinned (Appendix B #6)
