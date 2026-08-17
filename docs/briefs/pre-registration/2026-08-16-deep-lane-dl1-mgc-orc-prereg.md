# DL-1 — deep-lane campaign 1 pre-registration: opening-range continuation on gold (GC-train / MGC-confirm)

**Status:** `FROZEN` — operator GO (JA) 2026-08-16 ("GO on DL-1"). §1–§7 below are binding;
no amendment after this mark (Trap #12 — a change closes this campaign and opens a fresh one
under the lane's counters). Path recorded on the [charter](../../adr/2026-08-16-deep-iteration-lane-charter.md)
running-count line.
**The GO mark adjudicates the five gathered operator items (Verification block):**
(1) **bar-scope reading accepted** — the 5th-leg BINDING BAR's domain does not reach deep-lane
paid-data seed generation; route (1) stands as disclosure only, claimable ex post per the F1
precedent; this reconciles the charter §2.1 letter for this campaign. (2) **pause residual
broad reading rejected for DL-1** — the CON-5/dense-1m pause does not reach this non-index,
non-route-① family. (3) **channel-origin accepted** — internally-generated; harvest intake
not owed. (4) **"Closed for ORB: gold" cleared for this distinct composition** — the survey
prior is engaged (§7.6), its panel-overlap disclosed; the 08:30-anchor/drift-filter/structural-
stop composition is adjudicated as a new construct, not a survey re-run. (5) **step-4
strike-mapping ratified** — a cost-law-recheck failure counts on the lane's yield limb.
**Authored:** 2026-08-16 · Claude Code (JA commission, charter §7 step 1)
**Lane:** `deep` (first campaign under the [deep-iteration lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md), `Accepted` 2026-08-16, GO-1 fully discharged, GO-2 K ≈ 10)
**Mechanism id:** `opening-range-continuation` (existing registry id — `instrument_profiles.py` names it; no new MECHANISMS.md entry)
**Authorizes:** nothing. Pre-registration ≠ run. The train pull, iteration, nomination, confirm
read, and every downstream step fire only after the GO mark, in the §6 order, and the confirm is
read exactly once.

---

## §0 — Rule-0 reads (this session @ `73ad4d5`, 2026-08-16)

| Source | Anchor | Supplies |
|---|---|---|
| [Deep-lane charter](../../adr/2026-08-16-deep-iteration-lane-charter.md) | `73ad4d5` | §2.1–§2.7 campaign requirements; GO-2 K≈10; GO-1 discharged (frontier + dry-run); §4 counting machinery (abandonment vs strike) |
| [`lab/research_utils/axis_screen.py`](../../../lab/research_utils/axis_screen.py) | executed this session | **Conjunct (i):** K=10 ≤ 33 ✓. **Conjunct (ii):** `floor_at_k(10, years=7.62)` = **1.170** ≤ 2.0 ✓. **Conjunct (iii):** Gaussian-approx power at the named design-target edge (below), se = 1/√7.62 = 0.362: target 1.8 → **0.959** ≥ 0.50 ✓ (0.882 even at 1.6) |
| [MSL design-box re-derivation](../../notes/notice/N-2026-08-13-msl-design-box-rederivation.md) | read this session | Target geometry (rr ∈ [2,3], WR 0.30–0.42, hard stop, k=1, no pyramiding); the MGC cost cell (RT **$4.12**, R_max $177 at p=0.35/rr=3); the §7 Guardian→MGC adverse-prior Stage-0 obligation |
| [`ops/instruments/MGC.md`](../../../ops/instruments/MGC.md) | read this session | W1 metals sign-constraint (co-leg only) · **W2 explicitly prescribes this campaign's data geometry** ("Deep history may use GC parent; re-scale tick/margin; reserve native-micro era as OOS") · W4/G1: DISC-CAMP-0 bank = disclosure, not a kill · E1–E6 **P**, E7 **N/A** (overlay-only), N-SHAPE class-attested **P** · disposition `RE-ENTERED — K-void cleared; class-attested; not elected` · R8 fix-window kill (different mechanism, untouched) |
| [Charter Databento addendum](../../adr/2026-08-16-deep-iteration-lane-charter.md) | `73ad4d5` | Both windows priced $0.0000 at `ohlcv-1m`; roots confirmed (`GC.FUT`/`MGC.FUT`); `--phase` boundary enforcement verified live |
| [Q-POLFRONT-1 closure](../closures/Q-POLFRONT-1-closure-resolved-quantified.md) | read this session | §3 **mandatory named risk** (GO-1): the policy frontier's 5.1× headroom is EOD-clock-fragile (median stress delta +55.2pp vs flat +1.63pp) — consumed in §6 step 5 as a disclosure arm only, never primary admission |
| [Family-K ADR](../../adr/2026-08-04-family-k-bank-disclosure-not-gate.md) + [`discovery_manifests/disccamp0_gc_2010_18.json`](../../../discovery_manifests/disccamp0_gc_2010_18.json) | read this session | **K_banked(GC/MGC family) = 3,177** (DISC-CAMP-0, closed) **plus the CFD-era gold-ORB survey trials** (`orb_universe_2026-06-22`: XAUUSD scored within its 7-instrument, per-instrument-battery sweep — bank facts cited from the campaign artifacts per W4, not re-litigated) — disclosed per Req-3, not charged; K_eff = K_intrinsic = **10**. The ADR's own §6 honesty note (sequential K unpriced) is acknowledged, not evaded |
| [W4 dormancy ADR](../../adr/2026-08-07-w4-minimal-gate-set-dormancy.md) | read this session | SPA/StepM re-arm = prereg names thresholds AND operator GO dated after 2026-08-07 → **this prereg names p ≤ 0.10 (§6 step 2); the GO mark on this file is that GO.** PBO/CPCV not re-armed — no cross-validated selection is used (nomination is a single frozen statistic on the full train window), so the PBO leakage-argument row does not fire |
| [Q-EVALSEQ-1](../closures/Q-EVALSEQ-1-closure-falsified.md) / [Q-POLFRONT-1 RESULTS](../../../lab/analysis/c1/q_polfront_1_2026-08/RESULTS.md) | read this session | The state-policy lever's measured state (survival-axis real; pass-axis dead; EOD-fragile) — context for §6 step 5's N-SURV arms |

**Executed door-check (charter §2.1, pasted verbatim — exit 1, bar answered by route in §7):**

```
$ python scripts/instrument_profiles.py cell MGC opening-range-continuation
=== MGC x opening-range-continuation ===
ledger: ops/instruments/MGC.md
verdict: untested — no prior on this cell.
class finding (mechanism-wide, not specific to MGC): Session-aware continuation on MYM failed on
seven independent grounds at once (D2–D8, N=403) — placebo p=0.2144, gross/cost ratio 0.693
against a 4.00 bar, net −0.0210R. D3 is arithmetically unrescuable by sizing (gross/cost reduces
to 0.655; contracts and stop-width cancel out). [MYM.md M2/M3](MYM.md)
BINDING BAR: free-data-5th-leg-snag-closed-2026-07-01 -> ../../docs/rejected_candidates.md
K bank: read ../../discovery_manifests/ — never trust a snapshot.
prior: Third-leg E-K elimination is void as a gate after K-bank ADR; large disclosed bank remains
a Req-3 fact, not an inherited kill. DISC-CAMP-0 history is disclosure, not re-litigation. [#G1]
```

**Standing-pause attestation (charter §2.1):** the CON-5 / dense-1m OHLCV
temporal-selectivity / entry-geometry pause (Branch A, U0 KEEP 2026-08-15) is attested
non-binding here on two grounds that the record actually supports — **not** on lane
membership, which MSL-S2B disproves as a scoping argument (the pause was enforced against a
15m MYM card outside the lane): **(i) instrument class** — every application of the pause on
record (CON-1..5, S2B, U0 KEEP) is entangled with the index-intraday-OHLCV raised bar's
domain; MGC sits outside that bar entirely; **(ii) route-independence** — S2B needed the
paused temporal-selectivity route ① to clear the index raised bar; DL-1 has no index bar to
clear and never invokes route ① or the 2026-08-10 ruling. **The residual broad reading (the
pause reaches any 1m-sourced entry-geometry family regardless of instrument) is stated here
and put to the operator: the GO mark on this prereg adjudicates it; it is not
self-adjudicated.** MSL E1 HOLD binds MSL slate cards, not lane campaigns (charter §2.7).
Attested against the current STATE.

**Channel-origin attestation (charter §2.1):** internally-generated family — composed this
session from the design-box geometry; not an externally-published seed (no paper, no named
external anomaly), so harvest intake and its limb-2 counter are not touched. The generic
"opening range breakout" concept is trading folklore, not a citable published cohort; the
family's specific **composition** (08:30 data-impulse anchor, overnight-drift filter,
structural stop, this instrument) is original to this prereg — but the family **on gold is
not estate-novel** (the CFD-era survey scored and closed XAUUSD ORB-30; engaged in §7 item
6). If the operator judges either the folklore ancestry or the survey lineage pushes this to
harvest-intake territory, the honest route is intake-clearance first — flagged, not
self-adjudicated.

**Dedup attestation (executed, sub-rule 8 — corrected at adversarial review):**

```
$ grep -rn -iE "opening.range.*(gold|MGC|GC)|((gold|MGC)[^a-z].*opening.range)" \
    lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
(empty on those three surfaces — but see below: the empty grep is NOT the conclusion)
```

The mechanism-family search (per the standing lesson: an empty grep is not evidence of no
prior work) surfaces a **scored, closed gold opening-range prior the grep pattern could not
see** — [`orb_universe_2026-06-22`](../../../lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md)
(CATALOG one-liner names no instruments) scored **XAUUSD ORB-30 on the CFD-era Pepperstone
panel**: n=1,644, meanR +0.0311, t=+1.03, long +0.113 / short **−0.048**, placebo p=0.0005
flagged "† placebo 'significant' in the WRONG direction" (the breakout **fades** on
gold-short), fill-cliff 0.89× sub-cost; verdict line: "**Closed for ORB:** … gold (long-beta +
sub-cost)". This prior is engaged as adverse prior **6** in §7 — not routed around — and its
trial count is disclosed in the family-K row below. The consult's "untested — no prior on this
cell" is ledger-side (MGC × this mechanism id) and remains true; the *family on gold* is not
estate-novel. Other adjacent non-matches: `orb_mnq_2026-07` (index, MNQ — parked candidate);
ORB-ZB (rates — engaged as adverse prior 7 in §7); MSL-C2 London-range fade on MGC (a
**fade**, opposite role — its bar scopes "not other session-structure fades" and does not
reach continuation entries).

---

## §1 — The family (one mechanism, one instrument, frozen)

**NY-session opening-range continuation on gold.** After the 08:30 ET NY data/metals impulse
establishes an opening range, a break that holds in the direction of the overnight drift tends
to continue on trend days. All structure below is frozen; only the §2 variant axes are searched.

- **Session anchor:** OR measured from **08:30:00 ET** (fixed — the CPI/NFP/data impulse window;
  not searched). Force-flat **15:55 ET** (design-box flat-by-16:00 build target; not searched).
- **Entry:** stop order at OR extreme + 1 tick, direction per variant filter; **≤ 1 entry per
  day** (first triggered side only; no re-entry, no reverse). k = 1 by construction.
- **Initial hard stop:** opposite OR extreme (structural; rr defined by geometry). No trail, no
  BE move, no pyramiding, no scale-in/out (EM3-clean).
- **Target:** fixed multiple of the realized per-trade risk (2R or 3R per variant), else flat at
  15:55 ET. rr ∈ [2,3] and expected WR 0.30–0.42 → squarely the design-box archetype
  (trend-continuation, positively-skewed loss side, frequent small bounded losses).
- **Drift filter (variants):** `sign(return from prior 17:00 CT reopen → 08:30 ET)` — break
  taken only in the drift direction (filtered variants) or either direction (unconditional).
- **Retest variants:** after a break, entry via limit at the broken OR extreme (retest fill)
  instead of the breakout stop order — an execution-style axis, same mechanism.
- **Roll days:** sessions containing a front-month volume-roll are excluded from entries
  (flagged, not traded) — the OR is a *level* object and stitched levels across a roll are
  phantom (databento schemas reference, back-adjustment discipline).

**N-ACT design note (the S2A death, addressed at composition):** MSL-S2A died at 0.511
trades/week — a selective trigger under-firing. An OR break fires most sessions by
construction (only inside-days and filtered-against-drift days skip); expected cadence ≥ 2–3
trades/week even for filtered variants. Measured trades/week on train is a §6 nomination gate,
not an assumption.

## §2 — The frozen variant set (K_intrinsic = 10; the axes ARE the search)

| V | OR window | Drift filter | Entry style | Target |
|---|---|---|---|---|
| 1 | 30 min | unconditional | breakout stop | 2R |
| 2 | 30 min | unconditional | breakout stop | 3R |
| 3 | 30 min | drift-aligned | breakout stop | 2R |
| 4 | 30 min | drift-aligned | breakout stop | 3R |
| 5 | 60 min | unconditional | breakout stop | 2R |
| 6 | 60 min | unconditional | breakout stop | 3R |
| 7 | 60 min | drift-aligned | breakout stop | 3R |
| 8 | 30 min | drift-aligned | retest limit | 2R |
| 9 | 60 min | drift-aligned | retest limit | 3R |
| 10 | 30 min | unconditional | retest limit | 2R |

**Closed set.** No variant may be added, retuned, or substituted after any train number is seen
(D-K1 imported: every variant available to be chosen counts, and these ten are all there are).
Iteration = scoring these ten on train and diagnosing; it never mints an eleventh.

## §3 — Data and the frozen partition (charter §2.3)

| Partition | Symbols | Window | Phase | Schema | Priced |
|---|---|---|---|---|---|
| **TRAIN** | `GC.FUT` (parent; front-month series assembled per the frozen stitch rule below) | 2010-06-06 → 2019-01-01 | `discovery` (boundary-enforced by `db_fetch.py`) | `ohlcv-1m` | $0.0000 (charter addendum) |
| **CONFIRM** | `MGC.FUT` (native micro; same stitch rule) | 2019-01-01 → 2026-08-16 (**7.62 y**) | `oos` | `ohlcv-1m` | $0.0000 (charter addendum) |

- **Frozen stitch rule (both partitions, imported verbatim from the family's own frozen
  precedent, DISC-CAMP-0 manifest params):** front month = **per-UTC-day `ohlcv-1d` volume
  leader, outrights only**; a roll day = the day the leader changes (excluded from entries per
  §1). Honest pin restatement: the Q-TVCOV attestation is for Databento's `.v.0` continuous
  product ("`.v.0` is the TV-`1!`-equivalent"); this assembled series **replicates** a
  volume-lead roll and is not itself the attested `.v.0` object — stated, not blurred. No
  back-adjustment anywhere: all levels, entries, exits, and P&L are the actual contract's
  prices (the OR is a level object; §1 roll-day exclusion handles the seam).
- **All iteration feedback reads TRAIN only.** The confirm partition is read **once**, on the
  single nominee, after the §6 step-2 gates. Per-variant confirm results are never computed.
- **Proxy discipline (MGC W2, verbatim ledger warning):** GC-parent train re-scaled to micro
  specs at scoring (MGC = 10 oz, $10/point, tick 0.1 = $1).

**Frozen scoring conventions (each of these was an exploitable degree of freedom until pinned
here; none may move after any train number is seen):**

1. **The statistic** ("net annSR" everywhere in this prereg): Sharpe of the **daily net P&L
   series** — CME trading calendar, flat days included as zeros — annualized by **√252**,
   computed identically on train and confirm. This maps to `floor_at_k`'s f=1.0 row; the
   harness's most-permissive-f convention across FREQS is its own documented behavior and the
   floor 1.170 is quoted from the harness verbatim, so the comparison is conservative or exact,
   never generous.
2. **Sizing for the P&L series:** 1 contract per trade, costs $/contract. (N-SURV sizing at §6
   step 5 is a separate, downstream frontier question — this statistic is edge-shape only.)
3. **Cost pin (pass/fail):** RT **$4.12**/contract (design-box MGC cell, incl. slippage
   allowance) on both partitions. The native-confirm-era slippage re-parameterization is a
   **disclosed sensitivity arm only** — it never moves the SURVIVOR/STRIKE boundary.
4. **Fill engine (1m bars):** entries at stop price + 1 tick (or bar open if the bar gaps
   through); **adverse-first same-bar resolution** (if one 1m bar touches both stop and
   target, the stop fills); stop exits at stop price − 1 tick slip (mirrored for shorts);
   target exits at target price; 15:55 ET force-flat at bar close.
- Pull commands staged (fire at GO, `--campaign-id DL1-MGC-ORC`, cache era-tagged by phase):

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols GC.FUT --stype parent \
  --schema ohlcv-1m --start 2010-06-06 --end 2019-01-01 --phase discovery \
  --campaign-id DL1-MGC-ORC --max-cost 1.00
PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols MGC.FUT --stype parent \
  --schema ohlcv-1m --start 2019-01-01 --end 2026-08-16 --phase oos \
  --campaign-id DL1-MGC-ORC --max-cost 1.00
```

## §4 — Falsifiable hypothesis and the named design target

**Design-target edge (named a priori, conjunct iii):** confirm-partition net annualized Sharpe
**1.8** for the nominee — this prereg's own named target, marginally below the charter's GO-2
design point (true-1.83) and therefore conservative in the binding direction. Power at the
actual 7.62y confirm: **0.959** at 1.8 (0.966 at the charter's 1.83; 0.882 even at 1.6). The
charter's own §6 honesty clause stands: the lane demands a mechanism materially better than
anything measured in the futures era, and a true-at-the-bar edge is a coin flip — this prereg
bets on the design target, disclosed as such.

**H:** the train-nominated variant achieves confirm net annSR ≥ **1.170** (= DSR ≥ 0.95 at
K=10 on the 7.62y confirm) **AND** both confirm halves (split **2022-10-24**, frozen; per-half
floor **SR > 0**, frozen — charter §2.4 fragility control) are positive.
**H fails** (a lane **strike**, 1 of the 2-campaign falsification budget) if the nominee is
read and misses either limb — including the `FALSIFIED-FRAGILE` shape (pooled pass, half fail).
**Abandonment** (dated on the charter, no strike, consecutive-abandonment counter) if the
**nominee** — the train-annSR argmax, the only variant the gates are ever applied to — fails
any §6 step-2 gate, so the confirm is never read. There is no fallback nomination.

## §5 — Forbidden moves

- **Reading confirm during iteration**, computing any per-variant confirm number, or
  re-nominating after the read. One nominee, one read, ever.
- **Touching the variant set** after any train number is seen (add/retune/substitute — D-K1).
- **Moving the session anchor, flat time, roll rule, or split date** after seeing results.
- **Instrument-hopping.** The door-check was also run on MCL (same bar) and M6A (exit 0, no
  bar) before election; MGC was elected on the design box's own cost cell and session story,
  **with the cleaner M6A door visibly declined** — switching instruments later is a new
  campaign under the lane's counters, never an amendment of this one.
- **Resting admission on the policy frontier.** N-SURV primary scoring is **flat-R**; the
  cushion-policy arm is a disclosure with the Q-POLFRONT-1 EOD-clock caveat attached (§6 step
  5). The 5.1× headroom number may not justify sizing anywhere in this campaign.
- **Reading the §7 bar answer as bar removal** — the 5th-leg bar stands for free-data CFD-book
  expansion; this campaign passes through its paid-data route, nothing more.
- **Quoting train-side numbers as evidence of edge.** Train output is selection apparatus;
  only the confirm read carries evidential weight (reporting-burns-holdout discipline).

## §6 — Frozen procedure and gate

| Step | What happens | Gate (frozen) |
|---|---|---|
| 1. Pulls | Both staged pulls fire (`--max-cost 1.00` each; estimates already $0.0000) | mechanical |
| 2. Train + nomination | All 10 variants scored on TRAIN under the §3 frozen conventions. **Nominee = argmax train net annSR, full stop — no fallback, no walk-down.** If the nominee fails **any** gate below, the campaign **ABANDONS**; a lower-ranked variant is never promoted. **Nomination gates, all train-only, all on the nominee:** (a) train net annSR > 0 AND cost-law ratio ≥ **4×** at the nominee's realized train geometry — pre-arithmetic at the design point: gross expectancy 0.40R (p=0.35, rr=3); per-contract ratio = 0.40 × stop_ticks × $1 / $4.12, so ≥ 4× requires realized median stop ≥ **~41.2 ticks (~$4.1/oz)** — consistent with the ENV-1 ≥40-tick guidance the design box cites; the realized-train-geometry check is binding because the structural stop's width is data-dependent; (b) survives **SPA (Hansen) consistent p ≤ 0.10** against the full 10-variant universe — pinned implementation: loss series = daily net P&L per §3, benchmark = zero-return series, Politis–Romano stationary bootstrap, expected block length **20 days**, B = **10,000**, RNG seed **7** (the W4 re-arm this prereg names); (c) the **nominee's** measured train cadence ≥ **1 trade/week** (N-ACT); (d) the nominee's train net annSR stays > 0 at +1 tick/side additional slip (M-16) | nominee fails any gate ⇒ **ABANDONMENT** (dated, no strike) |
| 3. Confirm read | Once, nominee only, native MGC 2019-01-01→2026-08-16 | net annSR ≥ **1.170** AND halves (2022-10-24) both > 0 ⇒ **SURVIVOR**; else **STRIKE** (1 of 2) |
| 4. Cost-law recheck | At the nominee's realized confirm geometry ($4.12 pin; native-era slippage as the disclosed sensitivity arm per §3) | ratio ≥ 4× or the SURVIVOR is demoted to **STRIKE** — mapping note: this demotion is charter §4 H's own composition ("confirm + cost-law + N-SURV"), not a new transition; the charter's yield-limb text names confirm and N-SURV failures explicitly, and **the GO mark on this prereg ratifies the cost-law limb's inclusion in the same count** |
| 5. N-SURV scoring | Frozen survivor gate (intraday-honest bust ≤ 3.0% ∧ P(pass) ≥ 50%), **flat-R primary**; cushion-policy arm reported as disclosure with the Q-POLFRONT-1 EOD-clock caveat verbatim | frozen 2026-07-13 prereg, byte-untouched |
| 6. Anchor + intake | Native-TV anchor, then lifecycle intake at SURVIVAL-ONLY / WATCH-1; every further step (Pine, TV, arming) under its own operator GO | charter §2.5, unchanged |

**Verdict vocabulary:** `SURVIVOR` / `STRIKE` / `ABANDONMENT` per the charter §4 counting
machinery; every outcome is recorded on the charter's canonical running-count line with a date.
Roster mapping (for INDEX/closure surfaces): SURVIVOR closes `RESOLVED`; STRIKE closes
`FALSIFIED`; ABANDONMENT closes `AMBIGUOUS` (confirm never read — nothing was tested).

## §7 — Binding-bar answer and adverse priors (engaged, not routed around)

1. **`free-data-5th-leg-snag-closed-2026-07-01` (the consult's BINDING BAR) — answered on the
   SCOPE ground, with route (1) as disclosure only, and the adjudication put to the GO mark.**
   Route (1) verbatim (the earlier draft's elision was load-bearing and is corrected):
   *"Paid / exogenous data **the free searches could not access** (e.g. NDX-native dealer
   gamma, intraday 0DTE order-flow), demonstrating an edge that is **both** vol-orthogonal
   **and** within-era robust."* Per the F1-MOC precedent (2026-07-27: "no citable δ, no
   cohort, no measurement, so the route is unclaimed rather than cleared"), a promised
   in-campaign demonstration does **not** clear route (1) ex ante — so this prereg does not
   claim it. Disclosure: the Databento GLBX parent-era history is paid-catalog data the
   CFD-era free searches could not access (the $0.00 estimates are promotional credits, not
   free-tier data), and *if* the campaign survives, its halves limb is a within-era-robustness
   demonstration — route (1) would then be claimable **ex post**, per F1's own logic.
   **Primary answer — scope:** the bar's domain is the 5th-leg free-data expansion programme
   (adding a leg to the then-live book from already-held free data); this campaign is deep-lane
   Tradeify seed generation under its own Accepted charter, on data outside that domain. The
   consult wires the bar `tier=always`, so the scope reading is **for the operator to mark,
   not for this prereg to self-adjudicate: the GO mark records that adjudication**, and it
   simultaneously reconciles the charter §2.1 letter ("must print no BINDING BAR") for this
   campaign — a bar answered-by-adjudicated-scope, not a bar ignored.
2. **Mechanism-wide adverse prior (consult class finding): session-aware continuation on MYM
   failed 7 grounds (placebo p=0.2144; gross/cost 0.693 vs 4.0; "unrescuable by sizing").**
   Engaged: (a) that measurement is an **index** instrument inside the index raised bar's
   domain — the design box's non-index thesis is precisely that this squeeze is
   index-resident; (b) its cost geometry (gross/cost 0.655–0.693) is the construct's, not the
   class's — this family's structural-stop geometry prices at ratio ≥ 4× as a **gate** (§6
   step 2a), not an assumption; (c) the placebo lesson is imported as the SPA gate. If the
   MYM finding generalizes to gold, this campaign dies at step 2 or 3 and the lane counts it —
   that is the honest test of the non-index thesis, not a reason to skip it.
3. **Guardian→MGC DEAD(N-SURV) (bust 42.2%) — the design-box Stage-0 obligation:** that cell
   was the locked Guardian book transferred **at its own sizing** (risk 0.34% ≈ $340/trade at
   1.00×) with Guardian's trail/BE loss shape. This campaign's R is solved to the bust-≤3.0%
   frontier (design-box MGC cell: R_max **$177** at p=0.35/rr=3 — roughly half Guardian's, at
   a hard-1R-bounded loss shape). Stated per the obligation: R ≈ $177-band vs $340, different
   loss-side shape, different admission path (N-SURV scored fresh at step 5).
4. **R8 fix-window kill (MGC ledger DEAD row):** `event-window-reversal` at the LBMA fix —
   different mechanism, different session object; untouched by this campaign.
5. **W1 metals sign-constraint:** single-leg campaign; binds only if ever co-legged with
   another metals position — carried forward to any future book composition, not operative here.
6. **The CFD-era gold-ORB survey (`orb_universe_2026-06-22`) — the family's own closest prior,
   surfaced at adversarial review after the grep missed it.** XAUUSD ORB-30: t=+1.03, long
   +0.113 / short **−0.048**, placebo p=0.0005 in the **wrong direction** (gold-short breakouts
   fade), fill-cliff 0.89× sub-cost; "Closed for ORB: … gold (long-beta + sub-cost)". **What
   carries adversely:** the long-side edge being partly gold-bull beta bears directly on this
   family's drift-aligned longs; the short-side fade signature bears on the unconditional
   variants (1/2/5/6/10). **What does not carry:** the survey's kill was substantially
   cost-driven on CFD fill-cliff geometry (0.89×) vs this campaign's exchange-traded $4.12 RT
   at ≥40-tick structural stops; its battery was cash-open-anchored, not the 08:30
   data-impulse session; the drift filter and structural stop are new axes. **Two operator
   items ride the GO:** (i) whether the survey's campaign-level "Closed for ORB: gold" line
   requires re-proposal-style clearance before this prereg freezes; (ii) the disclosure that
   the survey's Pepperstone panel calendar overlaps this campaign's confirm window — different
   venue/feed, so the untouched-confirm property survives, but it is stated here, not
   discovered later.
7. **ORB-ZB (rates, rejected 2026-07-20):** the registry's own load-bearing line — opening-range
   *momentum* is equity-index-specific; ZB shows opening-range *mean-reversion* (negative gross
   every window, placebo sign-reversed). A second non-index instrument where the breakout
   faded. Engaged, not omitted: the mechanism distinction this family bets on is gold's 08:30
   US-data impulse session (a scheduled information shock ZB's fade window and the survey's
   cash-open anchor do not test); the ZB addback bar is ZB-scoped and does not bind MGC. If
   the bet is wrong, steps 2–3 kill it inside the lane's budget — that is what the lane is for.

## §10 — Audit hooks

```bash
# Conjuncts reproduce (constants frozen):
python -c "import sys; sys.path.insert(0,'lab'); from research_utils import axis_screen as a; print(round(a.floor_at_k(10, years=7.62),3))"
# Expected: 1.17

# Door-check output unchanged since this prereg (re-run before GO):
python scripts/instrument_profiles.py cell MGC opening-range-continuation

# Frozen split integrity (this file, post-GO — no amendment to §2/§3/§4/§6):
git log --oneline -- docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md

# Charter count line carries this campaign after GO:
grep -n "Running counts (canonical, this ADR)" docs/adr/2026-08-16-deep-iteration-lane-charter.md

# Confirm never read before nomination (cache era-tagging):
ls ~/.databento_cache 2>/dev/null | grep -i dl1 || echo "no DL1 pulls yet"
```

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md --type inquire
# NOTE: repo-side checker = mechanical subset only (its own banner says so). The skill-side
# authoritative checker (~/.claude/skills/brief-authoring/scripts/check_brief.py) is absent
# from this install (verified 2026-08-16 — skill dir carries SKILL.md + references only);
# the substantive gate for this draft was the 2-agent adversarial review (wf_3b87fddb),
# 10 blockers + 9 minors found and applied before this freeze candidate.
```

§0 production reads with executed anchors incl. the pasted door-check and the CORRECTED dedup
(gold-ORB prior surfaced and engaged) ✓ · §4 H binary with this prereg's own named design
target + the three conjuncts computed ✓ · §5 moves genuinely tempting (confirm peek; variant
add; fallback nomination — now structurally impossible; instrument hop with a visibly cleaner
door declined; policy-sized admission) ✓ · §6 gates binary, nomination strict-argmax with no
walk-down, SPA implementation pinned, scoring conventions frozen ✓ · §7 answers the BINDING
BAR on the scope ground with route (1) demoted to disclosure per the F1 precedent, and engages
all **seven** adverse priors/constraints with mechanisms, not dismissals ✓ · §10 runnable ✓ ·
Operator items the GO mark adjudicates, gathered: bar-scope reading (§7.1) · pause residual
broad reading (§0 attestation) · channel-origin/harvest-intake judgment (§0 attestation) ·
"Closed for ORB: gold" re-proposal question + panel-overlap disclosure (§7.6) · step-4
strike-mapping ratification (§6).
