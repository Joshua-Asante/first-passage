# Stage-0 verdict pre-registration — ORB-MNQ-1 (NAS100-ORB-30 venue-native reconstruction candidate)

**Status:** `STAGE-0 FROZEN · §R GO SIGNED 2026-07-16/JA` (this file froze the search
universe + gate thresholds + every data-derived-integer *rule* + the per-clause
reachability attestation, per the mechanism-first HARD gate; the operator signed the §8
GO gate 2026-07-16, both parts confirmed). `register_search open --lane mechanism-first`
(K_eff=2) + the subsequent $0.00 decode of the already-cached MNQ/NQ bytes are now the
unblocked **execution** step. This document is the first Phase-2 artifact under the
reconstruction ADR (§7). **GO-signing consumes no K and fetches no data;** the K-bind and
decode run in the execution environment that carries the `databento` research venv (absent
in the authoring worktree — see §0 data-availability note and §7 step 1).
**Campaign:** ORB-MNQ-1 — NAS100 opening-range-breakout (ORB-30), venue-native
reconstruction for MNQ (CME Micro Nasdaq-100). **Sole anchor: MNQ.** Not a DJ30/MYM
candidate (see §1 dedup — DJ30 already failed the ORB placebo on the CFD feed).
**Lane:** mechanism-first (HARV HARD gate — ADR 2026-07-13 `Accepted`; same-units
attestation — ADR 2026-07-16 `Accepted`).
**Authorizing decision:** [`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md)
§2.2 / §7 Phase 2 ("author a Pre-Q / pre-registration for the first reconstruction
candidate... before any Pine parameter search").
**Inherits:** ratified Campaign defaults ([`2026-07-11-discovery-campaign-defaults-ratified.md`](../../adr/2026-07-11-discovery-campaign-defaults-ratified.md)) + DSR K/V supersession ([`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md)) + HARV lane ([`2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md)) + same-units attestation ([`2026-07-16-harv-attestation-same-units-supersession.md`](../../adr/2026-07-16-harv-attestation-same-units-supersession.md)) **by reference** — values snapshotted below, not re-ratified. **One default is explicitly overridden** — see §3.
**Loop of record:** STRATEGIC (discovery Stage-0). **Authored:** 2026-07-16 · Claude Code (Fable 5), operator-directed (in response to "based on the analysis in labs, what mechanism makes sense to investigate next?").

---

## §0 — Rule-0 reads (production source, verified this session 2026-07-16)

- **[`ops/instruments/NAS100.md`](../../../ops/instruments/NAS100.md) @ `fad8984` (2026-07-14)** — the full N1–N10 durable-findings ledger this campaign inherits. N1 (statistical footprint), N2 (regime-conditionality, twice-confirmed), N3 (not lock-grade under the CFD-challenge bust/p99DD framing), N5/N7 (give-back/IR-exit exit is **fill-fragile** on native re-export — the load-bearing negative lesson this campaign's frozen construct is designed to avoid), N6/N8/N9/N10 (four independent exogenous/selection-conditioning attempts all FALSIFIED — the conditioning-overlay avenue is exhausted, not reopened here).
- **[`lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md`](../../../lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md) @ `83b51d8` (2026-06-22)** — source of the frozen construct (OR-30, both-sides, exit-at-close, cost-net) and the operator ruling ("results proven since 2020 are admissible; COVID-19 is a structural watershed; 6.5 years (2020-2026) is a sufficient sample; ORB-on-NASDAQ is APPROVED as a strategy") that this campaign's §3 default-override cites directly.
- **[`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md) @ `9aa2dbf` (2026-07-16)** — the authorizing ADR. §2.2 names "design new Striker-family candidate editions engineered for CME micro microstructure" as the active research lane; §5 forbids re-running locked-Pine transfers and forbids treating this ADR as go-live authorization; §7 Phase 2 is this document.
- **[`core/firm_rules.py`](../../../core/firm_rules.py) @ `a53ee99` (2026-07-13)** — `cost_per_side_usd` for MNQ across FRIENDLY tiers: Bulenox $0.61, Tradeify $0.91, MFFU $0.95, BluSky $0.95 (NT-rail) / $0.50 (Rithmic-rail). This campaign uses **Bulenox $0.61/side**, matching the D5/H-OD-1 convention for direct cross-campaign comparability.
- **[`ops/prop_envelope_default.md`](../../../ops/prop_envelope_default.md) @ `6b94032` (2026-07-13)** — E1 build target 16:00 ET (binding minimum MFFU 16:10 ET). The frozen construct (exit-at-close, session close) is E1-compliant by construction — same logic as D5's `DEPLOYABLE-DEFAULT-ENVELOPE: YES`.
- **[`docs/rejected_candidates.md`](../../rejected_candidates.md) @ `193c41c` (2026-07-15)** — dedup pass (§1 below): confirms Q-ORB-GEX-1 / Q-ORB-T10Y3M-1 / Q-ORB-FRIDAY-1 are **conditioning-gate** rejections (a filter layered on top of ORB), not entry-mechanism rejections; confirms the 5th-leg/portfolio-expansion domain SNAG closure (2026-07-01) and its 3-clause re-proposal bar, which §1 argues option 2 discharges.
- **[`docs/methodology/rejected_signals.md`](../../methodology/rejected_signals.md)** — checked; no entry bears on this candidate (methodology-signal registry, not strategy-candidate).
- **[`lab/discovery/register_search.py`](../../../lab/discovery/register_search.py) @ `67cc146` (2026-07-14)** — confirms `open --lane mechanism-first` rejects a missing/empty `--reachability-attestation`; this file is authored as that non-empty artifact.
- **[`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) @ `268851b` (2026-07-16)** — Stage 0–8 pipeline + `§Campaign-defaults` values snapshotted in §2/§3; the same-units attestation specification (§R below follows it).
- **[`docs/adr/2026-07-16-harv-attestation-same-units-supersession.md`](../../adr/2026-07-16-harv-attestation-same-units-supersession.md) @ `268851b` (2026-07-16)** — the specification §R below satisfies: simulate every bundled gate in its own units, at the panel-era basis, commissions included.
- **[`lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md) @ `e1c51f0`** + **[`lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md`](../../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md) @ `514a366`** — both closed 2026-07-16, both cost-law Stage-2 kills, one (H-OD-1) with a confirmed mechanism killed only by a mis-attested gate. §R below is authored specifically to not repeat their PD-1/PD-2 same-units mistakes.
- **`discovery_manifests/d5_nq_intraday_mom.json`** — confirms MNQ family `K_banked = 1` (D5's closed manifest). This campaign's K accounting (§2) reads that value directly.
- **Data availability (verified this session):** the parent-NQ IS 1m cache (`~/.databento_cache/ohlcv-1m_parent_de42fcda759883ba.dbn`, 2010-06-06→2018-12-31) and native-MNQ OOS 1m cache (`~/.databento_cache/ohlcv-1m_continuous_ce119c1e8f923316.dbn`, 2019-05-06→2026-07-16) from D5's Stage-1 pull are **both present on disk, $0.00 marginal cost to reuse**. This worktree does not carry a provisioned `.venv-research` (checked; absent), so decoding them requires whichever environment executes Stage-1 — noted as a Stage-1 prerequisite, not a blocker to freezing this document.

---

## §1 — Context (why this candidate, and the dedup tension named explicitly)

Per the operator's question "what mechanism makes sense to investigate next," the
lab record was surveyed end-to-end (CATALOG.md, STATE.md forward board, the
harvest-intake doctrine, and every RESULTS artifact touching the current
reconstruction lane). Three independent walls have converged on the same narrow
band of survivable mechanisms:

1. **Power (Clause N).** Four monthly/weekly-event-frequency seeds killed on
   confirm-power < 0.50: D3 (0.24–0.30), D7 (0.30), H-TSMOM-1 (0.34), H-TSMOM-6J
   (0.26).
2. **Cost-law (Requirement 5 / same-units).** D5 and H-OD-1 both **confirmed**
   their mechanism in-sample (H-OD-1: t≈5.0, 9/9 years positive) and both died at
   Stage-2, 3.5–7.6× below their own cost hurdle.
3. **Force-flat (envelope E1).** All four FRIENDLY firms flatten by ~16:00–16:59
   ET; the self-funded (overnight-capable) lane is closed
   ([2026-07-16 ADR](../../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md)).

The surviving band is: **daily event frequency × R-multiple-scale per-event edge ×
intraday-complete (no overnight hold)**. The NAS100 ORB-30 finding (N1,
`ops/instruments/NAS100.md`) is the one mechanism in the entire lab record with
measured evidence inside that band: cost-net meanR +0.0872R (t+2.94, n=1663),
short side independently positive (+0.070, not long-beta), within-day placebo
p=0.014, best-of-K-corrected p=0.009, 6/7 years positive including the 2022 bear,
and — the discriminator that D5 and H-OD-1 both lacked — **fill-cliff headroom
>3× spread** (edge-band-to-cost ≈77:1, the exact ratio that let NAS100 beat US500's
sub-cost ORB).

**Why this is a reconstruction candidate, not a repeat of a closed domain (the
tension this section names explicitly rather than papering over):**

- **`docs/rejected_candidates.md`'s 5th-leg/portfolio-expansion domain was
  SNAG-CLOSED 2026-07-01.** NAS100 ORB-30 was literally built and evaluated
  *as an instance of that domain* (a 5th CFD leg on the locked FXIFY book — see
  `ops/instruments/NAS100.md` sessions "5th-leg build," "5-leg re-MC," "5-leg GO
  withdrawn"). A naive re-proposal of "NAS100 ORB as a new leg" would need to
  clear the domain's own re-proposal bar: (1) paid/exogenous data showing a
  vol- and era-orthogonal edge — **already tried four times and failed** (N6, N8,
  N9, N10); (2) a genuinely new venue class that relaxes a *binding* wall; or (3)
  a dated live incident.
- **This campaign is argued under clause (2), not a bare re-proposal.** The
  binding walls that killed the CFD version were: **(a)** N3's "no risk level
  clears both CFD-challenge lock gates (bust<1%, p99DD<5%) and passes usefully" —
  that wall is a *self-funded-FXIFY-challenge* framing, and the entire
  self-funded/challenge frame is now CLOSED
  ([2026-06-30 ADR](../../adr/2026-06-30-no-manual-trading-cfd-retirement.md);
  [2026-07-11 rescope](../../adr/2026-07-11-challenge-era-claims-rescope.md)) —
  the wall itself no longer applies to a discovery-campaign Stage-6 DSR/Sharpe
  gate. **(b)** N5/N7's fragility finding was specifically about a **give-back/
  trailing exit** breaking on native CFD/DXTrade fills — this campaign's frozen
  construct (§2) uses **exit-at-close only**, the one exit basis N1–N3 already
  validated as non-fragile and that N7 itself never found broken. The 2026-07-16
  ADR is a fresh, dated operator authorization for exactly this venue-class shift
  (CFD → CME-native futures, self-funded-challenge → prop-portfolio
  discovery-campaign gates) — **this is the clause-(2) trigger, not an assertion
  invented here.** The operator confirms or rejects this reading at the §8 GO
  gate below; it is not silently assumed.
- **Distinct from `Q-ORB-VIXTS-1`.** That item (STATE.md dormant-threads log,
  2026-07-10: "re-proposal bar declined, Phase 2 never run") was a proposed
  **VIX-term-structure regime-conditioning gate layered on top of the base ORB
  signal** — a different, narrower thing from the base entry mechanism this
  campaign tests. This campaign adds **no conditioning gate of any kind** (see
  §5 forbidden moves) — the four conditioning attempts (N6 gap, N8 GEX, N9
  T10Y3M, N10 Friday) are dead ends this campaign does not reopen.
- **Not Class-S.** Class-S ([2026-07-14 ADR](../../adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md))
  scores *existing locked-leg* native-futures expressions with **immutable**
  Pine. NAS100 ORB-30 is mechanistically distinct from the locked Striker NAS100
  v1 (different clock: 09:30 ET cash open vs Mon/Tue 13:00–17:00 UTC swing/
  pyramid) — this is a **new candidate**, built under the reconstruction ADR's
  broader authorization, not a Class-S scoring exercise.
- **DJ30/MYM dropped at this freeze.** The original cross-instrument screen found
  DJ30's ORB **fails its own within-day placebo** (p=0.194) — NAS100's edge is
  driven by its uniquely high opening-range/spread ratio, not a generic
  index effect. Single-instrument campaign (MNQ sole anchor), matching D5's own
  DJ30/MYM-drop precedent.

---

## §2 — Frozen search universe + design (Stage-0)

| Item | Frozen value |
|---|---|
| **Instrument** | **MNQ** (CME Micro E-mini Nasdaq-100) sole anchor. DJ30/MYM dropped (placebo fail on the CFD twin — see §1). Single-instrument campaign. |
| **Mechanism (named)** | Opening-range breakout: NAS100's opening-session realized volatility widens the edge-band (opening range) faster than cost (spread/commission) scales, so a breakout of the first ~30 minutes' range persists intraday. Literature grounding (Gao-Han-Li-Zhou *JFE* 2018 *Market Intraday Momentum*; Zarattini-Aziz; Crabel 1990) cited in the original cross-instrument study. Not a rediscovery of unconditional index drift — both directions (long AND short) are independently positive (N1), so the null being rejected is "the opening range carries no directional information," not "NAS100 goes up." |
| **Tool ladder** | None — **confirm-not-mine**. A single fixed construct inherited from an already-executed, adversarially-tested cross-instrument study (10 dated session-log entries, `ops/instruments/NAS100.md`). No STUMPY/tsfresh/ruptures search; no parameter sweep. |
| **Candidate set (fixes K)** | **One primary candidate = H1.** Construct: `OR_bars=2` (≈30-minute opening range from the 09:30 ET RTH cash-index open), **both-sides** directional-by-touch (enter long on upside breakout, short on downside — N1's own exit-at-close calibration shows both sides independently positive: long +0.102, short +0.070; unlike N7's give-back-exit finding where the long leg was a money-loser, exit-at-close does **not** exhibit that asymmetry, so both-sides is not diluted here), **exit at session close (~16:00 ET)**, cost-net at MNQ's own economics. **No second variant, no give-back/trailing exit, no conditioning gate.** |
| **K_eff (bound now, pre-result)** | **K_intrinsic = 1** (H1 sole candidate). **K_banked(MNQ family) = 1** (D5's closed manifest, `discovery_manifests/d5_nq_intraday_mom.json`). **K_eff = 2.** Clause-K DSR floor at K_eff=2 = **annualized Sharpe ≥ 0.85** (reference floors: K=1→0.65 · 2→0.85 · 3→0.98 · 4→1.06 FAIL). `V = 1/n` per Default #3. |
| **OOS axis (Default #1, applied as CONFIRM not discovery)** | This is a **confirm-shaped** campaign (frozen construct from an established cohort), not a mining campaign — there is no parameter-fitting IS phase. Default #1's stated OOS window (**native MNQ 2019-05-06 : present**) is used directly as the confirm window; the parent-NQ 2010-06-06:2018-12-31 window (already cached, $0.00) is used **only** as a free negative-control check (§3), not as a tuning window — see the regime-design note below. |
| **Frequency / N** | One signal-eligible session/day (both directions mutually exclusive by touch) ⇒ declared panel **N ≈ 1650–1700** (matching N1's own n=1663–1667 over a comparable ~6.5-year window on the CFD twin). |
| **Deployable envelope** | Exit-at-close is **inherently E1-compliant by construction** (session close ≈16:00 ET, no overnight hold) — `DEPLOYABLE-DEFAULT-ENVELOPE` expected **YES**, same logic as D5. |
| **Regime-design note (load-bearing; see §R.3)** | N2 (twice-independently-confirmed on Pepperstone + OANDA feeds) dates the mechanism's turn-on to ~2020–2021; pre-2020 is **falsified** on the CFD twin. Freezing Default #1's OOS window literally (2019-05-06→present) risks folding 1–2 likely-negative/mixed years (2019 partial, 2020) into the temporal-consistency sub-era count. §3 below **overrides** the sub-era window for that one default, with the reason and citation stated, rather than freezing a gate this campaign already has reason to believe is borderline-unreachable. |

---

## §3 — Frozen gate thresholds + data-derived-integer *rules*

Snapshot of the inherited Campaign defaults; **one explicit override** (marked).

| Gate | Frozen threshold / rule | Bound at |
|---|---|---|
| **Stage-2 cost-law kill** | Mean gross edge ≥ **4× cost hurdle**, MNQ economics (`firm_rules.cost_per_side_usd`, Bulenox $0.61/side) + 1-tick modeled slippage, computed at the **confirm-panel price/range basis** (not present-day levels) — same-units per the 2026-07-16 ADR. | Stage 2 |
| **Confirm / DSR (Clause-K floor)** | **Net-of-cost annualized Sharpe ≥ 0.85** (DSR ≥ 0.95 at K_eff=2, V=1/n). Min-detectable disclosure: reachable under the cohort-cited t-stat (see §R.1); the *net native-MNQ* realization is what Stage 6 actually tests. | Stage 6 |
| **Universe correction** | SPA/StepM degenerate at K_intrinsic=1 (reported, not gating); **DSR ≥ 0.95** is the operative universe gate; PBO N/A (no config selection — single fixed construct). | Stage 6 |
| **Block size** | Set from the confirm-era return-series ACF (never `sqrt(T)`) — bound at Stage 5, back-filled. | Stage 5 |
| **Temporal-consistency battery — Default #4, OVERRIDDEN** | **Override:** sub-era **sign**-consistency is scored on calendar years **2021–present** (post-turn-on window), not the full 2019-05-06→present Default-#1 OOS span. **Reason:** N2 is a twice-independently-confirmed (Pepperstone + OANDA) dated regime break at ~2020–2021; freezing the literal full-OOS sub-era count would very likely fold 2019 (confirmed negative on both feeds) and 2020 (transition year, both feeds negative-to-flat) into the ⌈0.7·Y⌉ positive-year count, manufacturing a gate failure the mechanism's own established evidence already explains rather than contradicts. **Precedent cited, not invented:** the operator's own 2026-06-22 ruling on this exact mechanism (`orb_universe_2026-06-22/RESULTS.md`): "results proven since 2020 are admissible; COVID-19 (March 2020) is treated as a structural watershed... a pre-2020 OOS failure is not a disqualifier." **Full 2019-05-06→present numbers are still reported, not hidden** — the override changes what the *gate scores on*, not what gets disclosed. drop-top-year concentration and CUSUM run on the 2021+ window; regime-slice survival (ruptures/HMM) stays a test condition, not a filter, per the un-overridden part of Default #4. | Stage 6 |
| **Negative-control check (free, additive — not a gate)** | The parent-NQ 2010-06-06:2018-12-31 window (already cached, $0.00) is scored on the identical frozen construct and is **expected to reproduce N2's null/negative finding**. This is a sanity check that the porting methodology (CFD→native-futures feed) doesn't itself manufacture a different regime story — not a tuning window, not gated, reported alongside Stage-4/6 regardless of outcome. | Stage 4 (opportunistic, zero marginal cost) |
| **Decay monitor (Default #5)** | Inadmissible without a CUSUM decay-monitor spec calibrated during validation (Stage-6d). | Admission |
| **Cost gate (Default #6)** | Declared `--max-cost`, checked against summed `db_fetch estimate` before any pull. Both legs' bytes are **already cached from D5's pull ($0.00)** — Stage-1 for this campaign is expected to be a $0.00 re-decode, not a new billable pull, but the estimate step still runs per discipline. | Stage 1 |
| **Breadth (Stage 8)** | 5th-column ENB / correlation delta vs the locked 4-leg frame + mechanistic-exposure declaration. **Flag (not a Stage-0 blocker):** the locked 4-leg frame this reproduces is the CFD book; this candidate is a MNQ-venue prop-portfolio book member, not a slot in the CFD book — Stage 8's comparison target needs an explicit decision (compare to the CFD 4-leg anchor as a reference point, or to the emerging prop-portfolio book composition) before that stage runs. Not resolved here; noted for the Stage-8 executor. | Stage 8 |

**Inheritance / override discipline:** every value above is the inherited default
except the one row marked OVERRIDDEN, whose reason is stated in-line per the
template's own override clause (no in-place edit of the canonical defaults table;
this is a campaign-local snapshot + override).

---

## §R — Reachability attestation (HARV HARD gate, same-units specification)

Per the 2026-07-16 same-units ADR: simulate **every** bundled gate in **its own
units**, at the **panel-era price/range basis**, commissions included — not a
Sharpe-space argument standing in for a bp/R-space gate (the exact mistake that
killed D5's and H-OD-1's own attestations).

### R.1 — Stage-2 cost-law gate (mean gross edge ≥ 4× cost hurdle) — **REACHABLE, with an honest bound**

*Cohort input (CFD twin, not yet native-MNQ-confirmed):* cost-net meanR **+0.0872R**
(t+2.94, n=1663, `ops/instruments/NAS100.md` N1), computed against **Pepperstone's
own CFD cost** (spread + RT ≈1.55pt against a median opening range of 95.9pt ⇒
CFD cost_R ≈ 0.0162R — `orb_universe_2026-06-22/RESULTS.md`: "cost_R is only
0.016").

*MNQ's own cost, computed at MNQ economics (same-units, not borrowed):*

```
RT_usd = 2 x (0.61 + 0.50) = $2.22      # Bulenox cost_per_side_usd + 1-tick slip, D5 convention
RT_pts = 2.22 / 2.00 = 1.11 pt          # MNQ multiplier $2/point
cost_R = 1.11 / 95.9 (median OR range, CFD-measured) = 0.0116 R
hurdle_4x = 4 x 0.01158 = 0.0463 R
```

*Two readings, both stated (no cherry-pick):*

- **Conservative (no gross add-back):** compare the CFD's cost-net +0.0872R
  directly to the MNQ hurdle 0.0463R ⇒ **ratio 1.88×** — clears the 4×-of-
  MNQ-cost bar with margin, though this slightly understates true gross (the CFD
  number already had ~0.0162R of a *different* cost subtracted).
- **Gross-approximated (add back the CFD's own tiny cost):** ≈0.0872+0.0162 ≈
  **0.1034R gross-ish** vs the 0.0463R hurdle ⇒ **ratio ≈2.2×**.

Both readings clear ≥4× on the *conservative* reading only if read as "meanR ≥
4×MNQ-cost_R" directly (0.0872/0.0116 ≈ **7.5×**, clears comfortably) — the 1.88×/
2.2× figures above are a *different*, stricter comparison (headroom above the
bare pass line, not the pass ratio itself). Stated plainly: **the primary
same-units test (mean edge / MNQ cost_R ≥ 4) passes at ≈7.5×, far above the D5
(hurdle 7.6× *short*) and H-OD-1 (hurdle 3.5× *short*) misses** — this is the
first candidate in the current pipeline where the direction of the miss is
reversed.

**Honest bound (not a reachability failure, a disclosed limit):** this is a
**cross-venue cohort proxy** (CFD Pepperstone spread/range economics standing in
for native MNQ fill/commission economics), not yet a same-instrument
measurement. The median opening range (95.9pt) is itself CFD-measured over
2020–2026; native MNQ execution quality (limit/stop fills on an exchange book vs
a CFD dealing-desk quote) is **unmeasured** and could differ in either
direction. **R.1 verdict: REACHABLE at the cohort-proxy level (≈7.5× the bare
4× bar)** — Stage 2 replaces this proxy with a real same-instrument, same-panel
measurement; it is not assumed to reproduce the exact ratio.

### R.2 — Within-day placebo gate — **REACHABLE (direct inheritance)**

*Placebo construction (frozen, unchanged from the original study):* compare the
opening-window return to a matched arbitrary intraday window; gate = the opening
window is significantly more informative (already measured: p=0.014, N1).

This gate is not re-derived — it is **inherited by citation** from an
already-executed, already-passed test on the CFD twin of the same underlying
index. The mechanism (discrete 09:30 ET cash-index open) is identical on MNQ
(same index, same open). **R.2 verdict: REACHABLE** — no plausible-true-world
argument makes this fail differently on the futures feed than it already passed
on the CFD feed for the same index.

### R.3 — Temporal-consistency battery (Default #4, overridden per §3) — **REACHABLE under the override; FLAGGED AT RISK under the literal default**

*Plausible-true world:* the mechanism is real and turned on ~2020–2021 (N2,
twice-confirmed). Under the **literal, un-overridden Default #1 OOS window**
(2019-05-06→present), the sub-era sign-consistency count would very likely
include 2019 (confirmed negative both feeds) and 2020 (transition, negative-to-
flat both feeds) — **2 of ~7 years already known-adverse before any data is
pulled**, putting the ⌈0.7·Y⌉ threshold at genuine risk of failing **for a reason
the mechanism's own well-established evidence already explains, not a reason
that indicates the mechanism is false.** This is exactly the shape the ADR wants
caught pre-freeze: a clause that could be structurally disadvantaged by a known,
dated, already-doubly-confirmed fact.

**Redesign applied (not a rescue after the fact):** §3 overrides the sub-era
scoring window to 2021–present, citing the operator's own dated 2026-06-22
ruling that treats COVID-19 as a structural watershed and pre-2020 as non-
disqualifying for this specific mechanism. Under that window, N1's own
per-year record (6/7 of the *full* 2020–2026 span positive, including the 2022
bear) makes the ⌈0.7·Y⌉ bar comfortably reachable. **R.3 verdict: REACHABLE
under the stated override; explicitly FLAGGED AT RISK (not reachable with
comfortable margin) under the literal un-overridden default** — disclosed here
so the operator can reject the override at the GO gate rather than discover the
tension after a result is visible.

### R.4 — Force-flat / E1 envelope limb — **REACHABLE (by construction)**

The frozen construct enters after the opening range completes and exits at
session close (~16:00 ET) — no overnight hold, no position carried past any
FRIENDLY firm's flat deadline (earliest binding: MFFU 16:10 ET). This is not a
probabilistic reachability argument; it is a structural fact about the
construct. **R.4 verdict: REACHABLE (trivial, by construction).**

**Attestation conclusion:** three of four bundled clauses are reachable with
real margin under a plausible-true world (R.1 ≈7.5×, R.2 direct inheritance, R.4
structural); the fourth (R.3) is reachable **only under a stated, precedented
override**, which is disclosed rather than silently applied. This file is the
non-empty `--reachability-attestation` artifact `register_search open --lane
mechanism-first` requires.

---

## §4 — Falsifiable hypothesis (H-ORB-MNQ-1; binary)

**H-ORB-MNQ-1 — if** the fixed NAS100-ORB-30 construct (H1: OR=2 bars,
both-sides, exit-at-close), scored on native MNQ over the confirm window
(2019-05-06→present, sub-era gate scored 2021–present per the §3 override),
delivers **net-of-cost annualized Sharpe ≥ 0.85** (DSR ≥ 0.95 at K_eff=2) **AND**
clears the (overridden) temporal-consistency battery **AND** the within-day
placebo stays significant on the native feed, **then** ORB-MNQ-1 is a confirmed
candidate → routes to Stage-7 realism (integer micro sizing, force-flat
mechanics already trivial) + Stage-8 breadth (with the comparison-target
question from §3 resolved first) + lifecycle CANDIDATE @1.00× intake as a
prop-portfolio book member; **otherwise** it closes (all-null close is
success-eligible — banks the MNQ family cumulative K + the process-defect log).

**Reject/accept threshold (numeric):** accept iff net-of-cost annualized Sharpe
≥ 0.85 on the confirm era, placebo significant, and the (overridden) temporal
battery clears. **H-ORB-MNQ-1 is falsified** on any of: net Sharpe < 0.85,
placebo non-significant on native data, or the sign/drop-top-year/CUSUM battery
fails under the 2021+ scoring window.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Re-adding any conditioning gate** (VIX-term-structure / GEX / T10Y3M /
  day-of-week) — four independent attempts already FALSIFIED (N6, N8, N9, N10);
  this campaign tests the **base** entry mechanism only. Re-litigating a
  conditioning gate here as a silent "improvement" is exactly the exhausted
  move `docs/rejected_candidates.md` already closed.
- **Reintroducing a give-back / trailing / IR-exit variant** — N5/N7 proved this
  class is fill-fragile on native re-export (idealized-fill artifact). Adding it
  as a second candidate would also raise K_intrinsic to 2 (K_eff=3, floor 0.98)
  for no evidenced benefit on this venue.
- **Widening to DJ30/MYM** "in case MNQ disappoints" — DJ30 already failed its
  own within-day placebo (p=0.194) on the CFD twin; re-adding it is a fresh axis,
  not this campaign, and duplicates the D5 DJ30-drop precedent.
- **Silently applying the §3 temporal-consistency override without disclosing
  it** — the override is real and precedented, but freezing it invisibly (not
  naming R.3's "at risk under the literal default" finding) would repeat the
  Q-HARV-0 failure shape this document is explicitly trying to avoid.
- **Treating the R.1 cost-law reachability proxy as a Stage-2 result** — it is a
  cross-venue cohort estimate (CFD spread/range standing in for MNQ execution),
  explicitly bounded in §R.1. Quoting "≈7.5× headroom" as if it were the
  native-MNQ Stage-2 number would be exactly the mistake this campaign's own
  §R section warns against for itself.
- **Treating the 2026-07-16 ADR's "new venue class" reading as settled** without
  operator confirmation — §1 argues it; the §8 gate is where the operator
  actually rules on it.
- **Amending any threshold here after a result is visible** (Trap #12) — close
  and re-open a fresh Stage-0 if the gates prove wrong.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger | Disposition |
|---|---|---|
| **RESOLVED** (candidate confirmed) | Net-of-cost annualized Sharpe ≥ 0.85 on the confirm era AND placebo significant on native data AND the (2021+-scored) temporal battery clears | Route to Stage-7 realism → Stage-8 breadth (comparison-target question resolved first) → lifecycle CANDIDATE @1.00×; feeds the 08-08→11-08 reconstruction-lane slate as a live dated RESULTS artifact |
| **FALSIFIED** (all-null) | Net Sharpe < 0.85 OR placebo non-significant OR temporal battery fails under the 2021+ window | Close; bank MNQ family cumulative K (→2) + defect log; success-eligible research outcome; the reconstruction ADR's §4 idle-limb clock keeps running (a dated FALSIFIED closure discharges it same as RESOLVED) |
| **AMBIGUOUS** | Confirm-era trade count too low for a stable Sharpe estimate (Default #3 `dsr_unreachable_low_n`), OR the operator declines the §1 clause-(2)/domain-SNAG reading at the §8 gate | If low-n: closure names the re-test condition. If operator declines the domain reading: this campaign does not open; §1's argument is recorded as rejected, and NAS100 ORB stays under the 2026-07-01 domain SNAG bar unchanged |

08-08 is a progress check; this campaign's own confirm run is the hard
adjudication (no calendar hard-date beyond the parent 2026-07-16 ADR's 11-08).

---

## §7 — Run protocol

0. **Stage 0 (this file):** universe + gates + override + §R frozen. **Operator
   reviews §1's domain-SNAG/clause-(2) argument AND §R (especially R.3) →
   GO/NO-GO** (§8).
1. **On GO:** `register_search open --lane mechanism-first
   --reachability-attestation <this file> --tool orb-fixed
   --search-space-size 1 --data-window 2019-05-06:present --hypothesis "..."`
   (binds K_intrinsic=1, K_eff=2). **Then** `db_fetch estimate` on the MNQ
   continuous 1m + NQ parent 1m windows (expected **$0.00** — both already
   cached from D5's Stage-1 pull) → cost-gate check → decode (needs a
   provisioned `.venv-research` with `databento` installed; absent in this
   worktree, present wherever Stage-1 actually executes).
2. **Stage 2** cost-law kill (real same-units MNQ measurement, replacing the
   §R.1 proxy) — **hard stop if it fails, same as D5/H-OD-1.** **Stage 4** IS/
   confirm edge series + the free parent-NQ negative-control check (§3). **Stage
   5** block size from the confirm-era ACF. **Stage 6** DSR ≥ 0.95 (Sharpe ≥
   0.85) + the 2021+-scored temporal battery + native placebo (§R.2). **Stage 7**
   MNQ realism (integer sizing; force-flat already trivial). **Stage 8** breadth
   — resolve the comparison-target question (§3) before scoring.
3. **Admission** only from RESOLVED: lifecycle CANDIDATE @1.00× with the
   Stage-6d decay monitor, as a prop-portfolio book member (not a CFD 5th leg).

Results land in `lab/analysis/orb/orb_mnq_2026-07/` (or the operator's preferred
slug), citing this pre-registration by path.

---

## §8 — Operator GO gate (the decision; DRAFT until filled)

```
§R REVIEWED / GO: 2026-07-16 / JA
Part 1 CONFIRMED — §1 clause-(2) reading holds: this is a genuinely new venue class
  under the 2026-07-16 reconstruction ADR (CFD → CME-native MNQ; self-funded-challenge
  frame → discovery-campaign DSR/Sharpe gates), NOT a bare re-proposal against the
  2026-07-01 domain-SNAG-closed 5th-leg bar. The two walls that killed the CFD 5th-leg
  version — N3's challenge-framed lock gates, and N5/N7's give-back-exit fill-fragility —
  are respectively moot (challenge frame closed) and structurally avoided (exit-at-close
  only). Domain re-proposal clause (2) is satisfied.
Part 2 CONFIRMED — §3 temporal-consistency override authorized: sub-era sign-consistency
  scored on 2021–present, citing the operator's own 2026-06-22 ORB ruling (COVID-19
  structural watershed; pre-2020 OOS failure non-disqualifying for this mechanism). R.3's
  explicitly-flagged at-risk reading under the literal un-overridden default is
  acknowledged and accepted; the full 2019-05-06→present figures are still reported, not
  hidden.
Authorizes `register_search open --lane mechanism-first` (K_intrinsic=1, K_eff=2) and the
  subsequent $0.00 decode of the already-cached MNQ/NQ 1m bytes.
```

---

## §10 — Audit hooks (runnable)

```bash
# 1. Freeze-before-open: while GO is unfilled, no register_search ledger entry exists for this campaign.
grep -n "§R REVIEWED / GO or NO-GO: ____________" docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md \
  && echo "GO unfilled — register_search open must NOT have run" || echo "GO filled"
ls discovery_manifests/orb_mnq*.json 2>/dev/null && echo "UNEXPECTED: manifest exists before GO" || echo "no manifest yet, as expected"

# 2. K accounting matches the closed D5 manifest (MNQ family bank = 1).
python -c "import json; print(json.load(open('discovery_manifests/d5_nq_intraday_mom.json'))['results'])"
grep -n "K_eff = 2\|K_banked(MNQ family) = 1" docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md

# 3. Both bundled-clause-critical verdicts present (R.1-R.4 all attested).
grep -c "R\.[1234] verdict:" docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md  # expect 4

# 4. The override is disclosed, not silent (Q-HARV-0 discipline).
grep -n "OVERRIDDEN" docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md

# 5. No conditioning gate re-added (forbidden-move check).
grep -icE "vix-term|gex|t10y3m|day-of-week gate|friday.*gate" docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md
# Expected: only appears inside the §5 forbidden-moves / §1 dedup prose (naming what NOT to do), never as an active design element

# 6. Cached bytes still present (Stage-1 should be $0.00, not a new pull).
ls -la ~/.databento_cache/ohlcv-1m_parent_de42fcda759883ba.dbn ~/.databento_cache/ohlcv-1m_continuous_ce119c1e8f923316.dbn

# 7. Reconstruction ADR still Accepted (this campaign's authorizing decision).
grep -n "Status:" docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md
# Expected: Accepted

# 8. register_search HARD-gate flag exists in production (the gate this file feeds).
grep -n "reachability-attestation" lab/discovery/register_search.py | head -2
```

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- ops/instruments/NAS100.md                                                        # fad8984
git log -1 --format='%h %ci' -- lab/analysis/orb/orb_universe_2026-06-22/RESULTS.md                                  # 83b51d8
git log -1 --format='%h %ci' -- docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md       # 9aa2dbf
git log -1 --format='%h %ci' -- core/firm_rules.py                                                               # a53ee99

# MNQ family K-bank reproduces from the closed D5 manifest (zero pulls, zero new K)
python -c "import json; m=json.load(open('discovery_manifests/d5_nq_intraday_mom.json')); print('K_banked(MNQ)=', m['K'], 'status=', m['status'])"

# Cost-law arithmetic reproduces (pure division, no data touch)
python -c "
rt_usd = 2*(0.61+0.50); rt_pts = rt_usd/2.00; cost_r = rt_pts/95.9; hurdle = 4*cost_r
print('RT_usd=%.2f RT_pts=%.4f cost_R=%.4f hurdle_4x=%.4f ratio(0.0872/cost_R)=%.2f' % (rt_usd, rt_pts, cost_r, hurdle, 0.0872/cost_r))
"
# Expected: RT_usd=2.22 RT_pts=1.1100 cost_R=0.0116 hurdle_4x=0.0463 ratio=7.53

# register_search rejects an empty attestation (the gate is real)
grep -n "file empty" lab/discovery/register_search.py
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-16 | Stage-0 FROZEN — MNQ sole anchor, K_eff=2 (K_intrinsic=1 + K_banked(MNQ)=1), frozen construct (OR=2 exit-at-close both-sides, inherited from the CFD ORB study), §3 Default-#4 override (2021+ temporal-consistency scoring window, cited to the 2026-06-22 operator ruling), §R reachability attestation (R.1 cost-law ≈7.5× REACHABLE-with-disclosed-proxy-bound, R.2 placebo REACHABLE-by-inheritance, R.3 temporal battery REACHABLE-under-override/AT-RISK-under-literal-default, R.4 force-flat REACHABLE-by-construction). §1 names the domain-SNAG dedup tension explicitly and argues (for operator confirmation, not by fiat) that the 2026-07-16 reconstruction ADR is the clause-(2) new-venue-class trigger. Awaiting operator §8 GO before `register_search open` / any decode. | Joshua (direction, via "what mechanism makes sense to investigate next?") + Claude Code (Fable 5) |
| 2026-07-16 | **§8 GO SIGNED (JA) — both parts confirmed.** Part 1: the clause-(2) new-venue-class reading holds (the two CFD-5th-leg walls are moot / structurally avoided). Part 2: the §3 2021+ temporal-consistency override authorized (cites the 2026-06-22 ORB ruling; R.3 at-risk-under-literal-default accepted, full-OOS figures still reported). Authorizes `register_search open --lane mechanism-first` (K_eff=2) + the $0.00 decode of the cached MNQ/NQ bytes as the execution step. GO signature consumes no K and fetches no data. | Joshua (GO) |
