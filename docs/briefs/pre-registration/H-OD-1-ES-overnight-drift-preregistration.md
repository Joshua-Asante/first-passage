# Stage-0 verdict pre-registration — H-OD-1 ES overnight-drift campaign

**Status:** `STAGE-0 FROZEN · §R attested · §8 GO SIGNED 2026-07-16 (JA)` (this file freezes
the search universe + gate thresholds + the execution/cost model + every data-derived-integer
*rule* + the per-clause reachability attestation). The HARV HARD gate (ADR 2026-07-13) is
satisfied *in this document* by §R, and the operator has **signed the §8 GO gate
(2026-07-16/JA)** — so committing the freeze artifacts, then `register_search open --lane
mechanism-first --reachability-attestation <this file>` (K = 1, K_eff = 2), then the
cost-gated ES/MES pulls are now the unblocked **execution** step (Operator + Cursor, §7
step 1). **Signing GO consumes no K and fetches no data.** Freeze-order requirement: this
file + the scoping brief (both authored 2026-07-16) must land in the **same commit**, before
any `register_search open` (§10 hook 1).
**Campaign:** H-OD-1 — ES overnight-drift inventory-risk, confirm window **02:00–03:00 ET**
(Boyarchenko, Larsen & Whelan, FRBNY Staff Report **SR917**, *The Overnight Drift*).
**ES parent sole anchor; BtD conditional DROPPED at freeze** (operator pin P1(a), 2026-07-16).
**Lane:** mechanism-first (HARV HARD gate — ADR 2026-07-13 `Accepted`).
**Inherits:** ratified Campaign defaults ([`2026-07-11-discovery-campaign-defaults-ratified.md`](../../adr/2026-07-11-discovery-campaign-defaults-ratified.md)) + DSR K/V supersession ([`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md)) + HARV lane ([`2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md)) **by reference** — values snapshotted below, not re-ratified. One declared deviation from the inherited defaults: the **frozen passive execution model** (§3 Stage-2 row + §R.1), declared pre-result with its rationale.
**Parents:** [`H-OD-1-ES-overnight-drift-scoping.md`](../rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md) (scoping; P1(a) decided 2026-07-16) · [`Q-KBUDGET-HARVEST-1` closure](../closures/Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md) (`CLOSED-RESOLVED`; H1 PASS both clauses) · [inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) · [`PHASE2_RATIFICATION.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md) (incl. MNQ-expression amendment).
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-16 · Claude Code (Fable 5), operator-directed ("P1(a) — H1-only. freeze the Stage-0 pre-reg").

---

## §0 — Rule-0 reads (verified this session 2026-07-16)

- **[`docs/briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md`](../rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md)** (this-session artifact; commits with this file) — §0.5 P1 **decided (a)**: H1-only, K_intrinsic = 1; P2/P3 defaults confirmed by the same directive. §1 draft H-set; §2 HARD-gate order; §3 forbidden moves. **This pre-reg executes scoping §4 action 2.**
- **[Inventory addendum](../Q-KBUDGET-HARVEST-1-inventory-addendum.md) §1 row H1 (RATIFIED 2026-07-16)** — family **ES → K_banked = 1** (Q-HARV-0 closed manifest); declared **N = 1000** daily OD events (~6.5y OOS); **δ/σ = 0.093** (SR917 Table I, t-scaled; +1.5bp/day, t = 7.1); Path 1a; honesty riders (Table IX net-of-cost collapse; 2021+ RSV-dispersion fade).
- **[`PHASE2_RATIFICATION.md`](../../../lab/analysis/harvest/q_kbudget_harvest_1_2026-07/PHASE2_RATIFICATION.md) amendment (2026-07-16)** — any **MNQ/NQ (or MYM) expression is `UNSCREENABLE:nq-native-delta-sigma-not-extracted`**; cross-instrument δ transplant inadmissible (intake ADR req. 2). ES micro sibling = MES ([`ops/instruments/ES.md`](../../../ops/instruments/ES.md)).
- **[`lab/archive/q_kbudget_1_2026-07/floor_scan.py`](../../../lab/archive/q_kbudget_1_2026-07/floor_scan.py) `floor_at_k` (frozen method, pre-reg §F hook #3)** — recomputed this session: **floor(2) = 0.85 · floor(3) = 0.98 · floor(4) = 1.06 > Cap 1.0**. Grounds both the K_eff = 2 floor below and the P1(a) consequence (H-TSMOM-1 preserved at future K_eff = 3).
- **[`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md)** — Stage 0–8 pipeline; Campaign-defaults #1–#6 snapshotted in §2/§3.
- **[`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md)** — §2 HARD gate (attestation blocks `register_search open`); §1 the Q-HARV-0 scar. §R below applies the "redesign or drop pre-freeze" mandate to the **cost model** (R.1), not only the placebo.
- **[`lab/discovery/register_search.py`](../../../lab/discovery/register_search.py)** — `open --lane mechanism-first` rejects a missing/empty `--reachability-attestation`. §R is that non-empty artifact; §7 names the invocation.

---

## §1 — Context (the symptom this freeze addresses)

Q-KBUDGET-HARVEST-1 resolved H-OD-1 to a screened PASS on both clauses (Clause K floor
0.85–0.98 ≤ Cap 1.0; Clause N power 0.837 at the ratified N = 1000, δ/σ = 0.093). A screen
PASS **licenses campaign scoping only**. Absent a Stage-0 freeze, three post-hoc degrees of
freedom would be available after numbers are visible: (1) the **BtD conditional** could be
added back as a second candidate (a K expansion that also forecloses H-TSMOM-1 — the P1
fork the operator just closed); (2) the **execution/cost model** could be chosen after
seeing which one the data clears — decisive here, because the axis's known kill-risk is
net-of-cost (SR917 Table IX) and the gross edge is only ~1.5bp/day; (3) the **placebo hour**
could be picked where it is quietest. This file freezes all three pre-result, plus the
universe, gates, and integer rules, under the HARV HARD gate.

Standing doctrine: HARV lane HARD gate (ADR 2026-07-13); Campaign defaults (ADR 2026-07-11)
+ DSR K/V (ADR 2026-07-12); harvest-intake ADR 2026-07-15 (this is the first funded
intake-class campaign after D5 — its closure counts toward the intake §4 doctrine
falsifier); `strategy_lifecycle.md` (a survivor admits as lifecycle CANDIDATE @1.00×).

---

## §2 — Frozen search universe + design (Stage-0)

| Item | Frozen value |
|---|---|
| **Instrument** | **ES parent** (CME E-mini S&P 500, GLBX.MDP3) sole confirm anchor — the SR917 cohort instrument. **MES** is a Stage-7 realism/cost diagnostic leg only (micro-cost cliff, §3). **MNQ/NQ/MYM expression FORBIDDEN** (UNSCREENABLE per Phase-2 amendment; δ does not transplant). Single-instrument campaign. |
| **Mechanism (named, π argument)** | Dealer/market-maker overnight inventory risk ⇒ positive ES drift concentrated in the **02:00–03:00 ET** hour (into the European open), unconditional, daily (SR917). Not a rediscovery of generic long-equity drift — the null is zero mean *in that specific clock hour* vs the rest of the overnight session. |
| **Construct (H1, sole candidate)** | Long ES at the **02:00 ET 1-minute bar open**, exit at the **03:00 ET 1-minute bar open**, every trading day, 1 contract. Window is the **cohort's declaration** (America/New_York, DST-aware; databento UTC timestamps converted via IANA tz; US/UK DST-misalignment weeks ride as-is — frozen rule, defect-log observation if material). **No window, threshold, or conditioning search.** |
| **Candidate set (fixes K)** | **One primary candidate = H1.** **H2 (BtD conditional, RSV < 0) is DROPPED at freeze** — operator pin P1(a) 2026-07-16: it would raise K_eff to 3 *and* push the ES family bank to 3, foreclosing H-TSMOM-1 at K_eff = 4 (floor 1.06 > Cap 1.0). Adding it later requires a fresh Stage-0 freeze **and** re-accepting that foreclosure in writing. **H3 is a placebo *falsification clause*, not a candidate** (consumes no selection-K). |
| **K_eff (bound now, pre-result)** | Manifest binds this campaign's **K = 1** (H1 sole candidate). **K_eff = K_banked(ES = 1, Q-HARV-0) + 1 = 2** ⇒ Clause-K DSR floor = **annualized Sharpe ≥ 0.85** (`floor_at_k(2)`, reproduced §10 hook 5). `V = 1/n` per Default #3. On campaign close the ES bank becomes 2 (H-TSMOM-1 later screens at K_eff = 3, floor 0.98 ≤ Cap — preserved by design). |
| **OOS axis (Default #1)** | IS + all diagnostics on **ES parent 2010-06-06 : 2018-12-31** (GLBX.MDP3 dataset floor — PD-1 lesson; SR917 published sample ends within IS, so OOS is post-publication). Confirm on **ES parent 2019-01-02 : pull date**. MES realism leg **2019-05-05 : pull date** (micro launch). |
| **Frequency / N** | One signal/day ⇒ OOS sessions ≈ 1,880 (7.5y); the **Clause-N declared panel stays N = 1000** (the ratified declaration — conservative; power quoted at the declared N, never at the realized count). |
| **Schema / pull** | `ohlcv-1m`, `.v.0` continuous volume-roll (Q-TVCOV-1 pin, D5 precedent). Cost-gated estimate before every pull (`--max-cost`), era-tagged `--phase discovery` / `--phase oos`. Known vendor degraded days (2020-02-27/28, 2020-06-30 — D5 [`PULL_LOG.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/PULL_LOG.md)) → Stage-6 note. |
| **Execution/cost model (FROZEN — load-bearing, see §R.1)** | **Passive-both-sides:** limit at the 02:00 bar-open price (entry) and 03:00 bar-open price (exit); modeled friction = **0.5 tick round-trip total + commissions**. Commissions: parent ES ≤ $3.00/side assumption (≤ 0.03bp — negligible, disclosed); MES leg uses `firm_rules.cost_per_side_usd` (micro cliff, §3). **Fill-risk rider:** passive fills can miss; Stage-7 must report the modeled fill-rate (limit touched within the window's first 5 minutes) and a **fill-rate < 80% ⇒ AMBIGUOUS** (§6), not a silent model swap. The cross-both-ways alternative is shown structurally un-passable in §R.1 — freezing it would ship an unreachable bundle. |
| **Deployable envelope** | Position held 02:00–03:00 ET only — inside the Globex session, never through the 17:00 ET close/maintenance; flat at 16:00 ET by construction ⇒ **E1-compliant**, `DEPLOYABLE-DEFAULT-ENVELOPE` expected YES (confirmed with deployable RT count at Stage 1). Firm-specific "overnight" definitions are a prop-G4 check, not a campaign gate. |

---

## §3 — Frozen gate thresholds + data-derived-integer rules

Snapshot of inherited Campaign defaults (single source of truth = the template). The one
declared deviation: the Stage-2 cost basis uses the **frozen passive execution model** (§2),
not an unstated crossing assumption — declared here pre-result because the two models
straddle the hurdle (§R.1 arithmetic).

| Gate | Frozen threshold / rule | Bound at |
|---|---|---|
| **Stage-2 cost-law kill** | Gross edge ≥ **4× cost hurdle** at the deployable RT count, cost = frozen passive model (0.5 tick RT + commissions) on ES parent. At OOS-era index levels this is ≈ 4 × 0.29–0.35bp ≈ **1.16–1.40bp** vs gross **1.5bp** — passable but thin; a realized-gross shortfall kills honestly. | Stage 2 |
| **Confirm / DSR (Clause-K floor)** | **Net-of-cost annualized Sharpe ≥ 0.85** on the ES-parent OOS era (DSR ≥ 0.95 at K_eff = 2, V = 1/n). **Min-detectable disclosure (Default #3):** at N = 1000, the α=0.05 one-sided min-detectable net effect is δ/σ ≈ 1.96/√1000 ≈ 0.062 ⇒ ≈ 1.0bp/day net; the plausible-true net (§R.1, ≈ 1.15–1.21bp) is detected with power ≈ **0.6–0.7** — reachable, not comfortable, disclosed. | Stage 6 |
| **Universe correction** | SPA/StepM degenerate at single candidate (reported, not gating); **DSR ≥ 0.95** operative; PBO N/A (no config selection — single fixed construct, stated). | Stage 6 |
| **Block size** | From the **IS return-series ACF** (never `sqrt(T)`); daily one-hour returns ⇒ expected small; **value bound at Stage 5, back-filled**. | Stage 5 |
| **Temporal-consistency battery (Default #4)** | Sub-era **sign** ≥ ⌈0.7·Y⌉ of Y OOS calendar years positive; **drop-top-year**; regime slices as **test conditions, never filters**; CUSUM on the OOS edge series. The ratified **2021+ RSV-dispersion fade rider** is adjudicated here (as a named sub-era read), not by a new clause. | Stage 6 |
| **Decay monitor (Default #5)** | Inadmissible without a CUSUM decay-monitor spec calibrated during validation (Stage-6d death certificate). | Admission |
| **Cost gate (Default #6)** | `--max-cost` checked against summed `db_fetch estimate` before any pull. ES/MES `ohlcv-1m` scope only. | Stage 1 |
| **Stage-7 realism (micro cliff — named now)** | MES leg re-run with `firm_rules.cost_per_side_usd`: micro commission alone ≈ 0.6–0.8bp RT on ≈ $22–32K notional — **the micro expression plausibly fails net even where the parent passes.** A parent-PASS / micro-FAIL outcome is a **deployment-envelope restriction** (parent-only deployability), not a campaign falsification; recorded in the Stage-8 exposure declaration. Fill-rate diagnostic per §2. | Stage 7 |
| **Breadth (Stage 8)** | 5th-column ENB / cross-leg-correlation delta vs the locked 4-leg frame + mechanistic-exposure declaration (side; **02:00–03:00 ET**; in-market ≈ 4% of session clock ⇒ episodic — realized-corr insufficient, structural-overlap declaration mandatory). | Stage 8 |

---

## §R — Reachability attestation (HARV HARD gate, ADR 2026-07-13 §2 — the load-bearing section)

**Requirement:** simulate every bundled clause under a *plausible-true world*; a clause
structurally un-passable under a true-mechanism world must be **redesigned or dropped
pre-freeze**. Bundled clauses: **R.1** the H1 confirm chain (Stage-2 hurdle + Stage-6 net
floor), **R.2** the H3 placebo gate. R.1 is where this axis's known kill-risk lives (Table
IX rider) — the attestation does the cost arithmetic explicitly rather than quoting the
gross screen numbers.

### R.1 — H1 confirm chain (Stage-2 4× hurdle; Stage-6 net Sharpe ≥ 0.85) — **REACHABLE under the frozen passive model; the crossing model is shown un-passable and is NOT frozen**

*Plausible-true world:* the SR917 ES effect is real at the cohort-cited central magnitude —
gross **+1.5bp/day** in the 02:00–03:00 ET hour (t = 7.1; δ/σ = 0.093 ⇒ hourly σ ≈ 16.1bp;
gross annualized Sharpe ≈ 0.093 × √252 ≈ **1.48**).

Cost arithmetic (net annualized Sharpe ≈ (1.5 − c) × 0.98 for round-trip cost *c* in bp of
notional; floor 0.85 ⇒ **c ≤ ~0.64bp**; Stage-2 hurdle ⇒ **c ≤ 1.5/4 = 0.375bp**):

| Execution model | c at OOS-era index (~2,900–6,400; mean ≈ 4,400) | Stage-2 (4c ≤ 1.5?) | Stage-6 net Sharpe |
|---|---|---|---|
| **Cross both ways** (1 tick = 0.25pt RT + comm) | ≈ 0.40–0.87bp (mean ≈ 0.58) | **FAIL at every OOS-era index level below ≈ 6,700** (4c ≈ 2.3bp > 1.5bp) | 0.6–1.1 (era-dependent) |
| **Passive both sides — FROZEN** (0.5 tick RT + comm) | ≈ 0.21–0.44bp (mean ≈ 0.29) | **PASS** (4c ≈ 1.16bp ≤ 1.5bp; thin, honest) | ≈ **1.13–1.19** ≥ 0.85 |

- Under the crossing model the Stage-2 hurdle sits **above the cohort's own gross effect**
  at any OOS-era index level — structurally un-passable in a true world. Per the HARV §2.4
  mandate this clause was **redesigned pre-freeze**: the passive model is frozen in §2 with
  its fill-risk rider (fill-rate < 80% ⇒ AMBIGUOUS, §6). This mirrors Table IX's own
  finding (the unconditional edge collapses when you pay the spread) — the mechanism's
  tradability *is* the question, and the frozen model states pre-result what execution it
  assumes. Swapping models after results are visible is a §5 forbidden move.
- The tick-to-notional geometry is era-dependent and improving: 0.25pt RT = 0.86bp at index
  2,900 (2019) but 0.39bp at 6,400 (2026). The low-index sub-era is where net survival is
  weakest — the temporal battery (sign-by-year, drop-top-year) adjudicates this honestly
  rather than an era cherry-pick.
- **Honest caveat carried forward:** reachability means *a true world can pass*, not *it
  will pass*. Confirm power at the plausible net magnitude is ≈ 0.6–0.7 (§3 min-detectable
  disclosure) and Stage-2 passes with only ~1.3× slack. A FALSIFIED close is a live outcome
  and is success-eligible (banks ES family K, feeds the intake §4 doctrine falsifier).

**R.1 verdict: REACHABLE** (frozen passive model: hurdle 1.16 ≤ gross 1.5; net ≈ 1.13–1.19 ≥ floor 0.85).

> **POST-CLOSURE DEFECT ANNOTATION (2026-07-16 — recorded after the Stage-2 KILL; no frozen
> value edited, the campaign is closed).** This R.1 REACHABLE verdict did not survive
> execution — two arithmetic defects: **PD-1** commissions mis-scaled ×10 ("≤0.03bp" above;
> correct: 0.27bp RT at index 4400, 0.62bp at the IS median), and **PD-2** the hurdle was
> priced at recent index ~4400 while Stage-2 adjudicates on the IS panel (median 1942.1,
> ~2.3× the cost fraction). Corrected: hurdle 5.05bp (IS, full cost) / 2.23bp (4400, full
> cost) vs cohort 1.5bp — **the plausible-true world passes at no commissions-included
> basis**, so the Stage-2 clause was structurally unreachable at freeze and this attestation
> failed to flag it. The HARV lane ADR §4 falsifier fired on this closure. See
> [`RESULTS.md`](../../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md) + amending ADR
> [`2026-07-16-harv-attestation-same-units-supersession.md`](../../adr/2026-07-16-harv-attestation-same-units-supersession.md).

### R.2 — H3 placebo gate — **REACHABLE** (and structurally not the Q-HARV-0 geometry)

*Placebo construction (frozen):* **disjoint-hour placebo** — the identical passive
construct on the **20:00–21:00 ET** hour (Asian session, pre-committed now; SR917 attributes
no drift concentration there). *Placebo gate:* the placebo mean is **not significant at the
primary's α AND |placebo| < 50% of the H1 effect**.

- *Plausible-true world:* the inventory-risk mechanism concentrates the drift into the
  European-open hour; it implies **no** systematic 20:00–21:00 ET effect ⇒ placebo ≈ 0 ⇒
  the gate clears with wide margin under a true world.
- **The Q-HARV-0 scar cannot arise structurally:** H1 is *unconditional* — there is no
  conditioning window for the placebo to nest inside, and the placebo hour is a disjoint
  clock window: `placebo_window ∩ confirm_window = ∅` **by construction**. No mechanical
  carryover floor exists.

**R.2 verdict: REACHABLE** (disjoint clock hour; placebo null-by-mechanism under a true world).

**Attestation conclusion:** both bundled clauses are reachable under a plausible-true world
— R.1 only after the pre-freeze cost-model redesign recorded above, which is exactly the
HARD gate working as designed. This file is the non-empty `--reachability-attestation`
artifact `register_search open --lane mechanism-first` requires.

---

## §4 — Falsifiable hypothesis (H-HOD1; binary)

**H-HOD1 — if** the fixed ES 02:00–03:00 ET construct (H1), scored on the ES-parent OOS era
(2019-01-02 → pull date) under the frozen passive cost model and gates, delivers
**net-of-cost annualized Sharpe ≥ 0.85** (DSR ≥ 0.95 at K_eff = 2) **AND** clears the
temporal-consistency battery (sign ≥ ⌈0.7·Y⌉, drop-top-year, CUSUM, regime-slice-as-test —
incl. the named 2021+ fade read) **AND** the disjoint-hour placebo (H3) stays null per §R.2,
**then** H-OD-1 is a confirmed candidate → Stage-7 realism (parent + MES cliff + fill-rate)
→ Stage-8 breadth → lifecycle CANDIDATE @1.00× intake; **otherwise** the campaign closes
(all-null close is success-eligible — banks the ES family cumulative K = 2 + the defect log,
and counts toward the harvest-intake §4 doctrine falsifier alongside D5).

**Reject/accept threshold (numeric):** accept iff net Sharpe ≥ 0.85 on the OOS era with
placebo null and temporal battery cleared. **H-HOD1 is falsified** on any of: Stage-2 kill
(gross < 4× frozen cost), net Sharpe < 0.85, placebo fires, or the battery fails.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Opening the search / pulling before this freeze is committed and §8 is filled** —
  freeze-order is git-checkable; a pull before `register_search open` voids the campaign.
- **Re-introducing the BtD conditional (RSV < 0) after seeing H1's result** — post-hoc
  second candidate; K was bound at 1 pre-result, **and** it forecloses H-TSMOM-1 (ES bank
  → 3 ⇒ its K_eff = 4, floor 1.06 > Cap). A genuine BtD campaign needs a fresh Stage-0
  freeze + that foreclosure accepted in writing.
- **Swapping the execution model after results are visible** (passive ↔ cross, fill-window
  tuning) — the model is frozen in §2 *because* the two models straddle the hurdle; a
  post-result swap is Trap-#12 gate-editing. Fill-rate problems route to AMBIGUOUS, not to
  a quieter cost model.
- **Any MNQ/NQ/MYM expression** — the unburned-K lure; `UNSCREENABLE` per the Phase-2
  amendment; a native δ extraction is a *new axis*, screened separately.
- **Window or threshold search** (shifting the 02:00–03:00 clock, sweeping the placebo
  hour, RSV thresholds) — the windows are cohort/pre-committed declarations, not tunables.
- **Quoting gross Sharpe 1.48 or screen power 0.837 against the floor** — Table IX rider;
  the Stage-6 **net** gate is the test.
- **Wide mining / STUMPY tiling on ES** — Clause-K FAIL class; forecloses both remaining
  fundable axes.
- **Amending any threshold here after a result is visible** — close + re-open a fresh Stage-0.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (candidate confirmed) | Stage-2 pass AND net Sharpe ≥ 0.85 on OOS AND placebo null AND temporal battery cleared | Stage-7 realism (parent + MES cliff + fill-rate) → Stage-8 breadth → lifecycle CANDIDATE @1.00×; feeds the 08-08/11-08 slate |
| **FALSIFIED** (all-null) | Stage-2 kill OR net Sharpe < 0.85 OR placebo fires OR battery fails | Close; bank ES family K (→ 2) + defect log; success-eligible; counts toward harvest-intake §4 doctrine falsifier (with D5) |
| **AMBIGUOUS** | Modeled fill-rate < 80% (§2 rider), OR OOS count too low for a stable Sharpe estimate (`dsr_unreachable_low_n`), OR vendor data-quality hole material to the confirm window | Closure names the re-test condition; no in-place threshold edit |

08-08 is a **progress check**; the campaign's own confirm run is the hard adjudication.

---

## §7 — Run protocol (maps to the template Stage pipeline; gated at each step)

0. **Stage 0 (this file):** universe + gates + cost model + integer rules + §R frozen.
   **Operator reviews §R → GO/NO-GO (§8).**
1. **On GO:** commit freeze artifacts, then `register_search open --lane mechanism-first
   --reachability-attestation docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md
   --tool sr917-fixed-hour --search-space-size 1 --data-window 2010-06-06:2018-12-31`
   (binds K = 1; K_eff = 2 with the ES bank). **Then** `db_fetch estimate` → cost-gate →
   pull (ES parent `ohlcv-1m` IS `--phase discovery`, OOS `--phase oos`; MES OOS realism leg).
2. **Stage 2** cost-law kill (frozen passive model). **Stage 4** OOS edge series (single
   fixed construct). **Stage 5** block size from IS ACF. **Stage 6** DSR ≥ 0.95 (net Sharpe
   ≥ 0.85) + temporal battery + placebo, on ES-parent OOS. **Stage 7** realism (MES cliff +
   fill-rate). **Stage 8** breadth + exposure declaration.
3. **Admission** only from RESOLVED: lifecycle CANDIDATE @1.00× with the Stage-6d decay monitor.

Results land in `lab/analysis/` under a dated slug citing this pre-registration by path.

---

## §8 — Operator GO gate (scoping §4 action 3; SIGNED)

```
§R REVIEWED / GO: 2026-07-16 / JA
Confirms both bundled clauses REACHABLE (R.1 confirm chain under the FROZEN passive model;
R.2 disjoint-hour placebo, no conditioning-overlap geometry).
Acknowledges: crossing-model un-passability (R.1 table); fill-rate AMBIGUOUS rider; micro
(MES) cost cliff named at Stage 7; ES bank → 2 on close (H-TSMOM-1 preserved at K_eff = 3).
Authorizes `register_search open --lane mechanism-first` (K = 1, K_eff = 2) + the
cost-gated ES/MES pulls.
NO register_search open and NO Databento pull before this block is filled.  ← now filled;
§7-step-1 execution (commit freeze artifacts → register_search open → cost-gated pull,
Operator + Cursor) is unblocked. The GO signature consumes no K and fetches no data.
```

---

## §10 — Audit hooks (runnable)

```bash
# All patterns below use a [bracketed] final character so a hook never matches its own
# §10 line (M-AHF: hooks must test the artifact's stored form, not self-match).

# 1. Freeze-before-open: while GO is unfilled, no ledger entry / pull may exist for H-OD-1.
grep -n "REVIEWED / GO: ___________[_]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md \
  && echo "GO unfilled — register_search open + pull must NOT have run" || echo "GO filled"
grep -rln "h_od_[1]" discovery_manifests/ 2>/dev/null && echo "manifest exists — GO must be filled" || echo "no manifest"

# 2. The attestation is non-empty (register_search open rejects empty).
test -s docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md && echo "attestation non-empty OK"

# 3. Both clauses attested REACHABLE in the §R bodies.
grep -c "verdict: REACHABL[E]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md  # expect 2

# 4. Placebo sits in a separate ET clock window from the confirm (no conditioning-overlap).
grep -c "disjoint clock hou[r]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md  # expect 1 (R.2 body)

# 5. K bound pre-result; BtD dropped; floor numbers reproduce from the frozen scan function.
grep -c "Q-HARV-0) + 1 = [2]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md   # expect 1 (§2 K_eff row)
grep -c "is DROPPED at freez[e]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md  # expect 1 (§2 candidate-set row)
python -c "import sys; sys.path.insert(0,'lab'); sys.path.insert(0,'lab/archive/q_kbudget_1_2026-07'); \
from floor_scan import floor_at_k; assert (floor_at_k(2), floor_at_k(3), floor_at_k(4)) == (0.85, 0.98, 1.06); print('floors OK: 0.85 / 0.98 / 1.06')"

# 6. Frozen execution model present + declared as the one deviation (no silent default drift).
grep -c "0.5 tick RT + comm[)]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md   # expect 1 (§R.1 table, frozen-model row)
grep -c "One declared deviatio[n]" docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md        # expect 1 (header)

# 7. register_search HARD-gate flag exists in production (the gate this file feeds).
grep -n "reachability-attestation" lab/discovery/register_search.py | head -2
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python scripts/check_brief.py docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md --type inquire

# §0 anchors (scoping + this file are same-session artifacts — must land in ONE commit;
# post-commit, re-run these and record the hash)
git log -1 --format='%h %ci' -- docs/briefs/rnd-pipeline/H-OD-1-ES-overnight-drift-scoping.md
git log -1 --format='%h %ci' -- docs/briefs/Q-KBUDGET-HARVEST-1-inventory-addendum.md
git log -1 --format='%h %ci' -- docs/adr/2026-07-13-harv-discovery-lane-ratification.md

# Clause-K floors reproduce (zero pulls, zero K)
python -c "import sys; sys.path.insert(0,'lab'); sys.path.insert(0,'lab/archive/q_kbudget_1_2026-07'); from floor_scan import floor_at_k; print(floor_at_k(2), floor_at_k(3), floor_at_k(4))"

# Screen state this freeze relies on (3 PASS incl. H-OD-1)
python lab/archive/q_kbudget_1_2026-07/floor_scan.py | tail -3

# register_search rejects an empty attestation (the gate is real)
grep -n "file empty" lab/discovery/register_search.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Stage-0 FROZEN — universe (ES parent sole; MES = Stage-7 realism leg; MNQ/MYM forbidden), K = 1 bound (K_eff = 2, floor 0.85; BtD DROPPED per operator P1(a), preserving H-TSMOM-1), passive execution/cost model frozen (crossing model shown un-passable in §R.1 and rejected pre-freeze), disjoint-hour placebo 20:00–21:00 ET frozen, §R attested (R.1 + R.2 REACHABLE). §8 GO gate OPEN — no `register_search open`, no pull. | Joshua (P1(a) direction) + Claude Code (Fable 5) |
| 2026-07-16 | **§8 GO signed (JA)** — both clauses confirmed REACHABLE (R.1 confirm chain under the frozen passive model; R.2 disjoint-hour placebo). Authorizes commit-freeze → `register_search open` (K = 1, K_eff = 2) → cost-gated ES/MES pulls as the Operator + Cursor execution step. GO signature consumes no K and fetches no data. | Joshua (GO) |
| 2026-07-16 | **Campaign CLOSED — Stage-2 cost-law KILL + gate-geometry defect.** Stage-1: register opened (Cursor `95178dc`; Cursor cloud then `BLOCKED — capability-problem` on the missing databento key), ES-parent IS pulled locally at $0.00. Stage-2 (frozen passive model, fresh `lab/discovery/cost_es.py` — D5's crossing `cost_mnq.py` NOT reused): mean gross edge **+1.444bp** vs 4× hurdle **5.046bp** at the IS basis → KILL, while the **mechanism CONFIRMED-IS** (t≈5.0, positive all 9 years). Post-closure §R.1 defect annotation added above (PD-1 ×10 commission scaling; PD-2 price-basis mismatch) — the clause was unreachable at freeze; **HARV lane §4 falsifier FIRED**; amending ADR `Proposed`. Manifest closed (K=1 banked; ES family → 2). Harvest-intake doctrine count corrected to **0-of-2** (gate-geometry routing, not a counting mechanism-falsification). | Joshua (classification call) + Claude Code (Fable 5) |
