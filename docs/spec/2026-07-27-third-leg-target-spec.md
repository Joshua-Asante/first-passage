# Third-Leg Target Spec — admissible shape for a third c1 book leg

**Status:** **`RATIFIED 2026-07-27 · SCOPE DEAD 2026-08-04`** — screening standard only; admission still not authorized.
Ratification does **not** admit any candidate, authorize a rail slot, or license spend; it makes
§7 the standing screen that a third-leg proposal is measured against before any K or pull is spent.

> **2026-08-23 — §2.5 re-homing (venue-binding ADR, recorded not executed as a rescoring).**
> Limbs S1/S2/S4/S6 are EDITION (Tradeify venue facts). S5/S7 and R1–R4 are DEPLOYMENT
> and vacuous while the account is empty. T1–T5 and M1–M3 stay BOOK and remain the real bar.
> This note does not score any limb PASS/FAIL and does not lift SCOPE DEAD.
> Owner: [`2026-08-05-strategy-venue-binding-axis.md`](../adr/2026-08-05-strategy-venue-binding-axis.md) §2.5.

> ⚠ **SCOPE DEAD 2026-08-04 — do not score limbs PASS/FAIL.** This spec's own header scopes it to
> "a third leg **on the same account as the c1 book**". As of the Tradeify de-scope
> ([`ADR 2026-08-04`](../adr/2026-08-04-tradeify-venue-descope-eval-included.md)), there is **no book**,
> **no account**, and **no occupied symbol** in deployment. **No limb may be scored PASS or FAIL
> until a successor-venue ADR supplies replacement values.** ([`S1`](../adr/2026-08-07-loop-s1-environment-ratification.md)
> ruled F3 = no successor migration now — limbs stay unscored, not reopened.)
>
> **CARRIED FORWARD (tombstone — not a discard):** the seven-limb taxonomy; **S7's mechanism**
> (entries send `flatten_first=true`, exits a quantity-less `closeposition`, both keyed
> account+instrument — two strategies on one symbol destroy each other bidirectionally,
> uncurable by cap donation); S4's hedging logic; the §7.5 negative control and the S7
> non-vacuity check.
>
> **Do not recompute §2.4's session counts in either direction** — session-day recomputation stays
> moot regardless of occupancy status while SCOPE DEAD holds (no book, no account). ⚠ **Correction
> 2026-08-26:** the prior text here claimed `ops/instruments/MYM.md` "withholds release" of
> `MYM1!`/`MNQ1!` (retained-not-released under S1) — that is now stale.
> [`MSL Board B8`](../adr/2026-08-12-msl-mym-occupancy-release.md) released MYM1!/MNQ1!
> symbol/cap occupancy for new **non-Striker** research 2026-08-12, and `MYM.md`'s own session log
> confirms the release. This does not lift SCOPE DEAD or reopen §7 scoring — occupancy release
> is orthogonal to the missing book/account this banner is about.


```
RATIFICATION:    Third-leg target spec adopted as the standing screen for a
                 same-account third c1 book leg. Screening standard only —
                 admits nothing, arms nothing, spends nothing.
DATE / INITIALS: 2026-07-27 / JA
```

**Change control:** §7 thresholds change only by a superseding ADR or by the §6.1 verdict firing.
§2 derivations may be re-run and corrected without an ADR (they are measurements, not decisions);
if a re-run moves a §7 threshold, that is a §6.1 event, not an edit.
**Authored:** 2026-07-27
**Artifact path:** `docs/spec/2026-07-27-third-leg-target-spec.md`
**Scope:** a third leg **on the same Tradeify Select 100K account** as the c1 book (operator
election, 2026-07-27). The separate-account fork is explicitly out of scope — see §8.
**Supersedes:** nothing. **Superseded by:** nothing.
**Superseded-in-part-by:** `2026-08-04-tradeify-venue-descope-eval-included.md` — same-account / live-book screening premise only. Taxonomy, S7 mechanism, S4 hedging, §7.5 negative control, and S7 non-vacuity check **carry forward**.
**Amended-in-part by:** [`docs/adr/2026-07-29-third-leg-symbol-occupancy-limb.md`](../adr/2026-07-29-third-leg-symbol-occupancy-limb.md)
(`Accepted` 2026-07-29) — adds **S7 order-symbol occupancy** to §7.1, corrects §2.2's sufficiency
claim, narrows §2.4 Slot 2 to unoccupied symbols, and adds a sixth failing row to the §7.5 negative
control. Origin: [`SLR-MYM-1 closure`](../briefs/closures/SLR-MYM-1-closure-falsified-stage0.md) F1.
**Amended-in-part by:** [`docs/adr/2026-08-02-third-leg-liveness-limb.md`](../adr/2026-08-02-third-leg-liveness-limb.md)
(`Accepted` 2026-08-02) — adds **§7.6 / L1 liveness contribution** as a **REPORTED** limb (never a bar,
excluded from §6.2), and repairs §6.2's `SCREEN-PASS` trigger, which still read *"S1–S6"* after the
S7 amendment landed. Origin: [`c1_liveness_diversification_2026-08-02`](../../lab/analysis/c1/c1_liveness_diversification_2026-08-02/RESULTS.md).

---

## §0 — Rule 0 reads (production-source verification)

All read before authoring. Anchors from `git log -1 --format='%h %ci' -- <path>` on 2026-07-27.

| Path | Anchor | What it grounds |
|---|---|---|
| `ops/c1_rail/c1_sizing_host_reference.py` | `c134060` 2026-07-24 | L76: `69/11 -> MYM base 8 + add 60 = 68`; the account-aggregate cap split |
| `docs/adr/2026-07-17-c1-rail-build-account-registration-go.md` | `153b64e` 2026-07-24 | §Addendum 2026-07-22: static split rationale, runtime-check rejection + upgrade path, hedging clearance |
| `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md` | `7af4224` 2026-07-20 | `n_eff_risk_delta > 0` required; `ρ ≥ 1.0` presumptive reject |
| `lab/research_utils/breadth.py` | `bd92d8e` 2026-07-24 | `participation_ratio` on weekly cov = the gated statistic |
| `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` | `4de8085` 2026-07-20 | daily-$ basis: book $273 / ORB $438 / composed ~$539; bust 2.65% → 38.75%; §5 no-weight-iteration |
| `lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md` | `9620138` 2026-07-16 | weekly-$ basis: MYM 814 / MNQ 932 / ORB@0.37% 1761; risk N_eff 1.9593 → 1.9628 |
| `lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md` | `fccda29` 2026-07-24 | ORB standing caveats; `CANDIDATE @ 1.00×` |
| `docs/briefs/closures/ST-EH-1-closure-operator-stopped.md` | `31d7df0` 2026-07-26 | DSR floors: MNQ 0.98 (at cap) / MYM 0.85 / 6E 0.85 / GC-MGC 2.05 dead |
| `ops/prop_envelope_default.md` | `2fbc996` 2026-07-24 | E1–E7 envelope; §4a hedging + contract-cap corollary |
| `lab/archive/c1_capalloc_2026-07-27/RESULTS.md` | `d03fdf4` 2026-07-27 | **Q-CAPALLOC-1 `AMBIGUOUS (d)`** — 69/11 stands; book net split MYM 27% / MNQ 73%; the 07-22 re-allocation cut book net 43.2% (read on merge, post-ratification — see §2.3 basis caveat and §9.5) |
| `lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv` | tracked (`git check-ignore` returns nothing) | entry-rate + day-of-week derivation in §2.2 |

**Two measurement bases are in play and must never be mixed.** Q-COMPOSE-1 reports **daily-$ std at
the $100K basis**; `RESULTS_stage8_neff.md` reports **weekly-$ std on the Stage-8 scoring panel**.
`√5 × 273 ≠ 1269` — these are different conventions, not a reconciliation error. Every threshold
below states which basis it is on.

**One panel is NOT the Stage-8 panel.** `tradeify_book_composition_2026-07-23/out/daily_panel.csv`
is at a different leg weighting (it yields risk N_eff 1.484, not the published 1.9593). It is used
here **only** for day-of-week and entry-rate structure, never for variance thresholds.

---

## §1 — Context & motivation

The c1 book is two legs (Striker DJ30→MYM, Striker NAS100→MNQ) on one Tradeify Select 100K eval,
disarmed, with zero strategy-signal fills. The only admitted third-leg candidate, ORB-MNQ-1, was
falsified as a book leg by [Q-COMPOSE-1](../briefs/closures/Q-COMPOSE-1-closure-falsified.md):
composing it at 0.37% took full-panel bust **2.65% → 38.75%**, 15–23× over the 3.0% ceiling.

The mechanism was **variance dominance**, not correlation. That closure names the finding but does
not state the *envelope* — the region of candidate-space that would have survived. Absent that,
every future third-leg proposal re-derives it, and the last one re-derived it wrong: ORB **passed**
the Stage-8 risk-N_eff limb (+0.003) and still destroyed the book, so a candidate designed to the
written gate is not thereby admissible.

This spec states the envelope so a candidate can be screened before anything is scored, and so the
K budget is not spent discovering the same wall again.

---

## §2 — Derived constraint surface

### §2.1 — The written gate is necessary, not sufficient

ORB @0.37% scored risk N_eff **1.9593 → 1.9628** (delta **+0.003 > 0**) and ρ = 438/273 = **1.60**.
It cleared the `n_eff_risk_delta > 0` limb and failed only the `ρ ≥ 1.0` presumptive-reject limb —
then produced 38.75% bust. Reproducing the published Stage-8 numbers with `breadth.py` and sweeping a
synthetic leg shows the `n_eff_risk_delta > 0` region admits σ₃ up to ≈1.4× the whole book at ρ=0.

**Consequence:** Stage-8 alone does not screen. It must be applied together with §2.3.

### §2.2 — Contract cap is fully allocated; day-of-week is the only free capacity

The cap is account-aggregate 80 micros, statically split **MYM 69 / MNQ 11** (maxima 68 + 11 = 79).
Session filters are **locked Pine** properties, so free capacity is deterministic. Verified against
the panel: 0 off-schedule traded days on either leg.

| Day | Incumbents able to fire | Reserved | **Free (fail-safe, static)** |
|---|---|---|---|
| Mon | MNQ | 11 | **69** |
| Tue | MYM + MNQ | 80 | **0** |
| Wed | none | 0 | **80** |
| Thu | none | 0 | **80** |
| Fri | MYM | 69 | **11** |

Measured entry rates (panel, exit-date = entry-date since all holds are intraday): MYM **30.7%**
(191/623 Tue+Fri sessions), MNQ **30.5%** (190/623 Mon+Tue sessions).

A fail-safe headroom check must reserve a leg's worst case for as long as that leg **can still
fire**. The locked entry window is 09:00–13:00 ET for both, so **no dynamic scheme frees anything
inside the trading window** — the table above is the ceiling for any static or runtime design. (The
costing of the runtime alternative is in §8.)

> **⚠ AMENDED 2026-07-29 (ADR `2026-07-29-third-leg-symbol-occupancy-limb`) — this table is
> NECESSARY, NOT SUFFICIENT.** Free contract cap on a day does **not** imply the day is available.
> Cap and **order-symbol occupancy** are independent constraints: cap is divisible, an open position
> is not. On any session an incumbent **can** fire, its order symbol is occupied, and a second
> strategy on that same symbol in the same account cannot hold an independent position **regardless
> of how much cap is allocated to it** — our own rail sends `flatten_first=true` on every entry and a
> quantity-less `closeposition` on every exit, both keyed `account` + `instrument`
> (`ops/c1_rail/crosstrade_payload.py:62-73, 86-87`). **Check S7 (§7.1) before reading this table.** The
> incumbent occupancy map is the "Incumbents able to fire" column above: **MNQ1! on Mon+Tue, MYM1! on
> Tue+Fri.**

### §2.3 — Risk-geometry envelope (the binding constraint)

Bust is governed by dollar-variance against a fixed $3,000 EOD trailing barrier. Two calibration
points exist on the **daily-$ / $100K basis**:

| Composed daily-$ std | Bust (Tradeify Select 100K, full panel) |
|---|---|
| $273 (book alone) | 2.65% — PASS |
| $539 (book + ORB@0.37%) | 38.75% — FAIL |

Working backward from a variance-inflation budget, assuming the third leg is uncorrelated with the
book (`σ_composed = √(273² + σ₃²)`):

| Inflation budget | **σ₃ ceiling (daily-$, $100K basis)** | as ×book |
|---|---|---|
| +5% | **$87** | 0.32× |
| **+10%** | **$125** | **0.46×** |
| +15% | $155 | 0.57× |
| +20% | $181 | 0.66× |

**⚠ Basis caveat (added on merge with Q-CAPALLOC-1, 2026-07-27).** The $273/day book figure and the
814/932 weekly leg figures come from runs dated **2026-07-16/17** — i.e. **before** the 2026-07-22
69/11 re-allocation, which cut MNQ base 4→1 / add 40→10 and took book net **$127,826 → $55,206
(43.2%)**. The **live** book is therefore materially smaller than the basis these thresholds were
derived against, and a fixed $3,000 trail is relatively larger against it. **Direction of the error is
known: the $125 ceiling is conservative**, not permissive — so it does not admit anything it should
reject, and §7 remains safe to screen with. Re-deriving at post-69/11 sizing would loosen R1; doing so
is a **§6.1 event, not an edit** (§9.5). The §2.2 cap table is unaffected — it reads the live split
directly.

**⚠ Grounding limit (Trap #13).** The inflation budget is a **derived design target, not a ratified
gate**. Only two (σ, bust) points exist; the curve between them is unmeasured and the ratified
criterion remains bust ≤3.0% on all four partitions from the frozen engine. Treat §2.3 as a
**pre-screen that decides what is worth running**, never as a substitute for the run.

**Granularity is the real wall.** Using the repo's own ORB calibration (1R ≈ $160·k from the
book-composition brief; 0.37% of $100K = $370 ⇒ k ≈ 2.31), ORB's **per-contract** daily-$ std is
438 / 2.31 ≈ **$190** — already ~1.5× the +10% budget. Meeting the budget needs k ≈ 0.66 contracts,
which is not expressible. So:

> **The binding requirement is per-contract daily-$ std ≤ ~$125 at the $100K basis. That is an
> instrument-and-holding-period property, not a sizing knob.**

Point values per index point: **MYM $0.50 · MNQ $2 · MES/M2K $5**. MYM is 4× finer-grained than
MNQ — which is exactly why the split gives it 69 contracts and squeezes MNQ to base 1.

---

### §2.4 — The two admissible slots

Both slots are **temporal-disjointness** designs. Neither requires a rail change.

#### Slot 1 — Calendar-disjoint (Wed + Thu)

| Property | Value |
|---|---|
| Cap available | **80 micros**, both days, deterministic |
| Incumbent interaction | **none** — neither leg can fire, so no same-bar co-fire, no order-dependence |
| Sessions/week | 2 (~104/yr) |
| Variance treatment | adds to the weekly path variance (the EOD trail integrates across days); **never** same-day |
| Rail change | none — a day-of-week allocation table |

**Cost:** 2 sessions/week is a **power** constraint. Clause N requires confirm-gate power ≥ 0.50, and
this program has already killed a candidate on exactly that (H-TSMOM-1, N≈86, power 0.34). A Slot-1
candidate must reach the power floor on ~104 sessions/yr.

#### Slot 2 — Session-disjoint (Mon + Fri, afternoon)

| Property | Value |
|---|---|
| Cap available | **Mon 69 · Fri 11** (static reservation) |
| Incumbent interaction | same day, but entries are structurally separated (incumbents 09:00–13:00 ET) |
| Sessions/week | +2 (~104/yr), taking a Slot-1+2 leg to ~208/yr |
| Variance treatment | same-day, so it **does** stack with incumbent excursion on days they fire (30.7% / 30.5%) |
| Rail change | none |

**Honest limitation:** Slot 2's cap is **static-reserved**, so the afternoon placement buys *no
extra contracts* over an all-day leg on the same days. Its value is (a) session count toward the
power floor, and (b) intraday-regime separation from the incumbents' morning window. Recovering
extra afternoon capacity requires the runtime headroom build costed in §8 — which is **not
recommended**.

> **⚠ AMENDED 2026-07-29 (same ADR) — SLOT 2 IS UNAVAILABLE TO A CANDIDATE ON AN OCCUPIED SYMBOL.**
> Slot 2 was derived on cap grounds alone. Under **S7**, the incumbent **MNQ** leg can fire **Monday**
> and the incumbent **MYM** leg can fire **Friday** — so an MNQ candidate collides on Mon and a MYM
> candidate collides on Fri, and the collision is destructive in both directions, not merely a
> sizing conflict. **Slot 2 survives only for a candidate on an UNOCCUPIED symbol.**
> **Slot 1 (Wed + Thu) is unaffected** — neither incumbent can fire, so no symbol is occupied and
> both the full 80-micro cap and the symbol are free.
>
> **The cheap escape (ADR §2-E).** S7 is satisfied *trivially* by any venue-tradable symbol the book
> does not occupy — **MES, M2K, MGC**, and the micro-FX pair are all unoccupied today. Such a
> candidate gets the **full** §2.2 cap table with no session-disjointness argument required, and both
> slots remain open to it. Picking an unoccupied instrument is therefore a first-class design move,
> not an afterthought — though S7 is one of seven S-limbs, and each of those symbols still faces S4,
> its own instrument-ledger bars, and its own K bank.

**Tuesday is closed** under any static scheme (0 free). A candidate must not require Tuesdays.

---

## §3 — Question

**Pre-Q gate test:** stated as a symptom, not a fix.

**Q-3LEG:** The one composition attempt made against this book failed by 15–23× on a mechanism the
written gate does not screen for, and the envelope that would have caught it has never been stated —
so what does the admissible region actually look like, and what does a candidate cost to reject?

---

## §4 — Falsifiable hypothesis

**H-3LEG:** If a candidate satisfies **all** of §7.1–§7.4 — in particular R1 (per-contract daily-$
std ≤ ~$125 at the $100K basis) — then a frozen-engine composed re-MC at its deployable weight
returns bust ≤ 3.0% on all four partitions (full / H1 / H2 / bootstrap-95th) on both
`trailing_locking` tiers.

The three verdict triggers are stated numerically in §6.

---

## §5 — Forbidden moves

Each was genuinely on the table in the session that produced this spec.

- **Re-running ORB at a lower weight.** Q-COMPOSE-1 §5: "a failed composed candidate closes; it does
  not iterate weight," and the combined (composed × haircut) arm is **NOT licensed** because the
  haircut single passed. Sizing ORB down is the obvious lever and it is procedurally shut. A fresh
  pre-registration is the only route, and it must surface the injected-leg vs book daily-$-std ratio
  in *its own* §7 disclosure (that closure's lesson candidate 2).
- **Designing to the Stage-8 gate alone.** ORB passed `n_eff_risk_delta > 0` at +0.003 and produced
  38.75% bust. Treating the written gate as the spec reproduces the exact failure.
- **Fitting the mechanism to Wed/Thu.** The free days are a *scheduling* fact about the incumbents,
  not evidence about the market. Selecting an edge because it appears on the free days is a
  fitted-calendar artifact (§7.4 M1).
- **Taking contract cap from MNQ.** It is the cheapest source in contracts (11) and the most
  expensive in edge — MNQ is already squeezed to base 1, and its add legs carry **87.7%** of its
  panel net. MYM's carry 63.6%. Neither is a free donor. **Strengthened by Q-CAPALLOC-1 (2026-07-27):
  MNQ carries 73% of *book* net to MYM's 27%**, so the 69/11 split's own stated premise ("MYM carries
  the size") is false on P&L. Taking cap from MNQ is worse than this spec originally stated. Note the
  converse is also now measured and also forbidden here: shifting cap *toward* MNQ buys full-panel P&L
  and sells chop-half survival monotonically — the sweep argmax `17/63` (+74% net) fails the gate
  decisively on H1. Cap re-allocation in **either** direction is owned by Q-CAPALLOC-1 and its
  successor ADR, never by a third-leg proposal.
- **Building the runtime headroom check to "unlock" cap.** Costed in §8: it frees nothing inside the
  trading window, and the constraint it relieves is not the binding one.
- **Treating §2.3's $125 as a gate.** It is a two-point extrapolation. It decides what is worth
  running; the frozen engine decides admission.

---

## §6 — Gate criteria (binary)

### §6.1 — Spec-level verdict (fires on the first candidate that reaches a composed re-MC)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` | A candidate meeting all of §7.1–§7.4 composes at bust ≤3.0% on **all four** partitions, both `trailing_locking` tiers | Thresholds are load-bearing; spec becomes the standing screen |
| `FALSIFIED` | A candidate meeting **every** §7 requirement still composes **>3.0%** on any committed partition | The §2.3 derivation is wrong in *shape*, not level. Spec screens nothing further until re-derived from a measured σ→bust curve |
| `AMBIGUOUS-HOLD` | A candidate meeting §7.1/§7.3/§7.4 but missing R1 by 1.0–1.3× composes ≤3.0% | Ceiling is conservative. Re-derive the budget from the new third point; do **not** loosen it by judgement. Re-test window: next composed re-MC |

### §6.2 — Per-candidate screening verdict (fires before any data is pulled)

| Verdict | Trigger | Disposition |
|---|---|---|
| `SCREEN-PASS` | All of §7.1 (**S1–S7**), §7.2 R1+R3, §7.4 M1–M3 hold. **§7.6 L1 is REPORTED and deliberately excluded** — it never admits or rejects | Proceed to a pre-registered campaign; §7.3 T1–T5 and §7.2 R4 run in the normal pipeline |
| `SCREEN-FAIL` | Any single S-, R1/R3-, or M-requirement fails | Close. Record which requirement fired. **No K consumed, no pull.** |
| `SCREEN-DEFER` | All hold except R1, and per-contract σ is unknown because contract specs or a stop distance are undetermined | Determine the stop geometry first — arithmetic, not research, and free |

`SCREEN-PASS` licenses **scoping only**. It is not admission, not a rail slot, and not spend.

---

## §7 — The target spec (operable checklist)

A candidate is **screenable** as a third c1 leg if and only if it meets all of the following.

### §7.1 — Hard structural (venue / compliance; no discretion)

| # | Requirement | Source |
|---|---|---|
| S1 | Flat before **16:45 ET** (Tradeify); no overnight, no weekend, no holds through the maintenance break | envelope E1 + §4 overlay |
| S2 | Expressible in **micro contracts** | envelope E5 |
| S3 | Runs under **attended automation** on the existing TV → listener → CrossTrade → Tradovate rail | envelope E6 |
| S4 | If it trades an **Equity Index Product Group** symbol (ES/MES/NQ/MNQ/YM/MYM/RTY/M2K/…), it must be **long-only**. A short-capable Equity Index leg violates the hedging rule against the long-only c1 book — *in any account under the same control* | envelope §4a; GO ADR §5 forbidden move |
| S5 | Fits the **day-of-week cap table** in §2.2 without re-allocating cap from MYM or MNQ | `c1_sizing_host_reference.py:76` |
| S6 | **No US Treasuries** (untradable at this firm); rates = EUREX only | envelope §4 overlay |
| **S7** | **Order-symbol occupancy.** Must not require an **order symbol already traded by an incumbent c1 leg in the same account** on any session that incumbent **can** fire. Satisfied **trivially** by an unoccupied symbol (MES / M2K / MGC / micro-FX are unoccupied today). Otherwise requires **session-disjointness from the incumbent on that symbol**, established from **locked Pine session filters — never from observed trade frequency** (a leg that *can* fire occupies the symbol whether or not it did). Current occupancy: **MNQ1! Mon+Tue · MYM1! Tue+Fri**. Rationale: every entry sends `flatten_first=true` and every exit sends a quantity-less `closeposition`, both keyed `account`+`instrument` — two strategies on one symbol destroy each other's positions **bidirectionally**, and cap donation cannot fix it | `ops/c1_rail/crosstrade_payload.py:62-73, 86-87`; ADR [`2026-07-29-third-leg-symbol-occupancy-limb`](../adr/2026-07-29-third-leg-symbol-occupancy-limb.md) |

### §7.2 — Risk geometry (the pre-screen that does the work)

| # | Requirement | Threshold |
|---|---|---|
| R1 | **Per-contract** daily-$ std at the $100K basis | **≤ ~$125** (from the +10% budget; see §2.3 grounding limit) |
| R2 | Deployable-weight daily-$ std, composed | keeps `√(273² + σ₃²)` within the declared inflation budget |
| R3 | `ρ = candidate daily-$std / book daily-$std` | **< 1.0** (Stage-8 presumptive-reject limb); in practice ≲0.46 to satisfy R1 |
| R4 | `n_eff_risk_delta` on the weekly covariance | **> 0** (Stage-8 binding limb) — necessary, **not** sufficient |
| R5 | Excursion reporting against the intraday-trail posture | MFE/MAE stats declared at the deployment fork (envelope E3, §2 item 3) |

**R1 is the screen.** R3/R4 are the ratified gate and must still be run, but R1 is what a candidate
fails first and cheapest, and it can be computed from contract specs and a stop distance before any
data is pulled.

### §7.3 — Statistical (unchanged; stated so a candidate carries them from the start)

| # | Requirement | Threshold |
|---|---|---|
| T1 | Cost-law | ≥ **4×** hurdle at the deployable expression's round-trip count |
| T2 | Clause N power | ≥ **0.50** at the declared panel — the binding one for a 2-session/week slot |
| T3 | DSR floor | `floor_at_k(K_intrinsic)` from [`lab/research_utils/axis_screen.py::floor_at_k`](../../lab/research_utils/axis_screen.py) — **0.650 for every family** at `K_intrinsic=1`; disclose the family bank; never treat it as a bar (ADR 2026-08-04 family-K-bank disclosure-not-gate). |
| T4 | Regime | **both-halves** gate (H1 chop AND H2 trend), not full-panel only |
| T5 | Part A bust, standalone and composed | ≤ **3.0%** on all four partitions from the frozen engine |

**T3 is an instrument-selection constraint, not a statistics footnote.** ~~MNQ has effectively no K runway left; a fresh family starts clean and carries the loosest floor.~~ **STRUCK 2026-08-06 (claim-alignment M10):** under disclosure-not-gate, every family screens at `floor_at_k(K_intrinsic)`; the bank is disclosed, never a bar.

### §7.4 — Mechanism

| # | Requirement |
|---|---|
| M1 | The mechanism must be **day-agnostic by construction** and merely *scheduled* into the free days. A day-of-week-selected edge is a fitted-calendar artifact — the exact class the gates exist to kill, with a standing scar here (day-of-week read off exit dates) |
| M2 | Must be **alive in H1 chop**. ORB's second defect was regime-common-mode: dead in exactly the regime the book busts in. A leg that is also dead there adds variance without adding survival |
| M3 | Not a re-expression of a rejected entry. Re-proposal requires **new mechanism evidence**, not new parameters, a wider sweep, or a longer panel |

### §7.5 — Negative control: ORB-MNQ-1 scored against this spec

A screen that does not reject the known-bad candidate is vacuous. Scoring the one candidate whose
composed outcome is measured:

| Req | ORB-MNQ-1 | Verdict |
|---|---|---|
| S1 flat 16:45 ET | intraday only | PASS |
| S2 micros | MNQ | PASS |
| S3 attended rail | Pine authored + hash-pinned | PASS |
| S4 long-only if Equity Index | MNQ **is** Equity Index; ADMISSION.md calls it *direction-agnostic* | **FAIL-or-UNRESOLVED** — a short-capable leg is a hedging violation against the long-only book |
| S5 day-of-week cap table | trades daily, so requires Tuesday | **FAIL** — 0 cap available Tue |
| **S7 order-symbol occupancy** *(added 2026-07-29)* | trades **MNQ daily**; the incumbent Striker NAS100→MNQ leg can fire **Mon + Tue** | **FAIL — `MNQ1!` occupied.** Destructive both ways: ORB's entry would `flatten_first` the incumbent's position, and its exit would `closeposition` the incumbent's. **Not curable by cap donation** |
| R1 per-contract daily-$ ≤$125 | ≈$190 | **FAIL** (1.5×) |
| R3 ρ < 1.0 | 1.60 | **FAIL** |
| R4 `n_eff_risk_delta` > 0 | +0.003 | **PASS** — the only one it clears |
| T3 DSR floor | own 0.9754 at K_eff=2; ~~a new MNQ expression now faces **0.98 at K_eff=3**~~ → **STRUCK 2026-08-06 (M10):** use `floor_at_k(K_intrinsic)` | historical record / see T3 |
| M2 alive in H1 chop | dead 2019–2020, regime-conditional | **FAIL** |
| **L1 liveness contribution** *(added 2026-08-02)* | trades **MNQ daily**, so it is eligible on **Wed + Thu**, which no incumbent can fire; at near-daily firing its L1.b approaches the **100% ceiling** (dead weeks 82 → ~0) and its L1.c would collapse the p95 run from 4 to ~0 | **`LIVENESS-POSITIVE` — and it changes nothing.** See the non-vacuity note below: this is the strongest possible liveness score attaching to the known-bad candidate |

**Result: `SCREEN-FAIL` on six independent grounds** (S5, **S7**, R1, R3, M2, plus S4 pending
directionality), at zero K and zero spend. The single requirement ORB clears is **exactly the
written gate that let it through to a 1.5-hour frozen-engine run**. That is the spec's whole
justification.

**Non-vacuity check for L1 (added 2026-08-02) — inverted, and deliberately so.** Every other limb
here earns its place by *rejecting* ORB. **L1 cannot, and the negative control is where that is
proven rather than asserted:** ORB-MNQ is the single best liveness candidate this book has ever
seen — daily firing, eligible on exactly the two days no incumbent covers, driving dead weeks toward
zero and collapsing the 4-week tail. **It is also the candidate measured to take composed bust from
2.65% to 38.75%.**

That pairing is the argument for L1's force level. A limb that could gate on liveness would here be
pulling *hardest in favour of the worst candidate on record* — which is precisely the
rationalized-overlay failure the screen exists to prevent. **L1 is therefore correct only as a
reported tie-break among candidates that have already cleared everything else**, and its
`LIVENESS-POSITIVE` verdict on ORB must never be read as partial credit. ORB remains
`SCREEN-FAIL`; L1 does not appear in that result and cannot.

**Non-vacuity check for S7 (added 2026-07-29).** A new limb that does not reject the known-bad
candidate would be decoration. S7 rejects ORB-MNQ independently of every other limb — and it rejects
it for a reason none of the others capture, since S5 (cap) would have been satisfiable by a
day-of-week restriction while S7 would not. It also correctly *admits* the escape it is meant to
signpost: the same ORB construct on an **unoccupied** symbol would clear S7 outright.

---

### §7.6 — Liveness contribution *(added 2026-08-02)* — **REPORTED, never a bar**

⚠ **Force level, stated first because it is the whole design.** L1 **never admits and never
rejects.** It does not enter §6.2 and cannot produce `SCREEN-PASS` or `SCREEN-FAIL`. Its only
decision role is a **tie-break between candidates that have already cleared everything else**.
A liveness benefit is **never** a reason to relax a threshold or to rescue a failing limb —
see §5-adjacent forbidden moves in the admitting ADR.

| # | Requirement | Source |
|---|---|---|
| **L1** | **Liveness contribution.** Report three fields: **L1.a** — weekday sessions the candidate **can** fire that **no incumbent can**, taken from **locked Pine session filters, never observed trade frequency** (S7's rule, inherited); **L1.b** — modeled reduction in the book's **82 dead Mon–Fri weeks** at the candidate's **measured** per-eligible-session entry rate, with the measured **1.13× common-mode discount** applied; **L1.c** — effect on the **p95 longest consecutive dead run** (baseline **4 weeks**). Verdicts `LIVENESS-POSITIVE / NEUTRAL / NEGATIVE`, none of which gates. **Both source rules bind:** eligibility from Pine filters (a leg that *can* fire covers the session as a matter of schedule), **firing rate from the measured panel** (a leg eligible Wed/Thu that fires 5% of the time covers almost nothing) — a report giving only one is incomplete, not conservative | [`c1_liveness_diversification_2026-08-02`](../../lab/analysis/c1/c1_liveness_diversification_2026-08-02/RESULTS.md); ADR [`2026-08-02-third-leg-liveness-limb`](../adr/2026-08-02-third-leg-liveness-limb.md) |

**Why the limb exists.** The book is zero-trade in **82/312 Mon–Fri weeks (26.3%)**, longest run
**4**, against an idle rule enforced by **irreversible account deletion**. And the effect is
measured, not modeled — the two incumbents are each other's natural experiment: MYM alone 150 dead
weeks (run 9), MNQ alone 151 (run 10), **together 82 (run 4)**. The second leg cut dead weeks ~45%
and more than halved the worst run **at corr(daily P&L) = −0.13** — *legs can diversify liveness
without diversifying returns*, which no other limb can see. Current incumbent occupancy
**`MNQ1!` Mon+Tue · `MYM1!` Tue+Fri** leaves **Wed + Thu** free — 622 of 1,556 business days (~40%)
on which the book has never traded.

**L1 is subordinate to M1 (§7.4).** M1 requires the mechanism be *day-agnostic by construction and
merely scheduled into the free days*. **L1 scores the schedule, never the edge.** If a candidate's
edge exists *only* on Wed/Thu, **M1 fails it and L1 is irrelevant** — M1 is evaluated first, and L1
is computed only for candidates that already satisfy it.

**L1 is not a substitute for the token mechanism.** Measured: at the incumbents' own entry rate
(~30.7%) a Wed/Thu leg cuts dead weeks 82 → ~40–45, but the **p95 longest run stays 4**. Only
near-daily firing removes it. L1 reduces how often the obligation bites; it does not close the tail.

**The Wed/Thu window is where liveness would pay — not evidence that edge lives there.** The
constraint **narrows** the search space and may well be empty; that is not evidence against it.

## §8 — Out of scope / costed and rejected

**Separate-account fork — out of scope by operator election (2026-07-27).** On its own eval a leg
shares neither the $3,000 barrier nor the 80-micro cap, so §2.2 and §2.3 both vanish and the leg only
needs standalone Part A ≤3%. It costs a second eval fee and one of five household slots, and S4
(hedging) still binds across accounts. If the election changes, this spec does not apply and a
separate one is owed.

**Runtime headroom check — costed, NOT recommended.** Named as the upgrade path in the GO ADR
(`153b64e`, §Addendum 2026-07-22), and M1 does supply the prerequisite (`confirmed_base_qty`,
broker-confirmed and restart-durable, `c1_rail_telemetry.py:354`, with adds boundable from the locked
750%/1000% ratios). Costing:

- **Marginal capacity inside 09:00–13:00 ET: zero, every day** — a fail-safe check must reserve worst
  case while a leg can still fire.
- Post-13:00 expectation is real (Tue E[55], Fri E[59], Mon E[77]) but **stochastic**: Tuesday is
  {80: 45.9%, 69: 23.3%, 11: 20.4%, 0: 10.4%}. Capacity is known at entry time but varies 0–80 day
  to day, which breaks a pyramided expression (granularity fragility).
- Wed/Thu gain is **zero** — Slot 1 already has the full 80.
- It would encode locked Pine session windows **into the host**, creating a new doc/code skew surface
  of exactly the class the params-manifest gate exists for.
- It couples the candidate's size to incumbent activity, so the candidate has **no independent daily
  panel** — and every downstream gate (`breadth.py`, the Q-COMPOSE-1 engine, survivor-scoring Part A)
  takes one as input. It would make the result unscoreable by the frozen machinery.
- Five artifacts, one operator-signed (ADR amending the 69/11 disposition), landing on the critical
  path of the first live fill in the week the rail produced an unintended live fill and disproved
  `order_id` idempotency.

**It relieves the cap, which is not binding. It does not touch the variance budget, which is.**

---

## §9 — Open items

1. ~~**Not ratified.**~~ **DISCHARGED 2026-07-27/JA** — ratified as the standing screen (header
   block). No ADR was authored: the falsifier lives in §6.1 and the precedent for a ratified
   `docs/spec/` screening standard is `feed_equivalence_discovery_test_LOCKED.md` (status-header
   lock, no companion ADR). A superseding ADR is still the only instrument that may move a §7
   threshold.
2. **§2.3 has two calibration points.** A third — any composed re-MC at an intermediate σ₃ — would
   convert the budget from extrapolation to interpolation. Cheapest source is a future candidate's
   own run; no dedicated run is proposed.
3. **Session-window pin.** §2.2 depends on the incumbents' locked 09:00–13:00 ET filter. If either
   venue edition's session changes, the cap table changes with it. The §10 hook covers this.
5. **§2.3's variance basis predates the 69/11 re-allocation** (Q-CAPALLOC-1, read on merge). The
   $273/day book figure is from 2026-07-16/17; the 07-22 re-allocation cut book net 43.2%. Error
   direction is known and safe — **R1 is conservative** — so §7 screens correctly today, but the
   ceiling is tighter than the live book warrants. Re-deriving R1 at post-69/11 sizing is a **§6.1
   event**. Cheapest correct trigger: fold it into whichever composed re-MC supplies the third
   calibration point in item 2, rather than running it standalone. **Note the cap split itself is not
   settled** — Q-CAPALLOC-1 is `AMBIGUOUS (d)` with the three ⚠ Tradeify rule pins as a hard blocker;
   if verification flips 69/11, the §2.2 cap table changes with it and this spec must be re-read.
4. **No futures-venue lock anchors exist** for any live or candidate leg (`baselines.md` is CFD-era,
   synced 2026-06-04). A Slot-1/2 candidate would need one before activation, same as the incumbents.

---

## §10 — Audit hooks (runnable)

```bash
# S5 / §2.2 -- cap split still 69/11 and still summing inside 80
grep -n "69/11" ops/c1_rail/c1_sizing_host_reference.py

# §2.2 -- day-of-week structure still holds (expect 0 off-schedule days both legs)
python - <<'PY'
import pandas as pd
p = "lab/analysis/c1/tradeify_book_composition_2026-07-23/out/daily_panel.csv"
d = pd.read_csv(p, index_col=0, parse_dates=True); d["dow"] = d.index.dayofweek
print("MYM off-schedule:", int(((d.striker_dj30 != 0) & ~d.dow.isin([1, 4])).sum()))
print("MNQ off-schedule:", int(((d.striker_nas  != 0) & ~d.dow.isin([0, 1])).sum()))
# reproduces the §2.2 entry rates (expect ~30.7% / ~30.5%)
print("MYM entry rate:", round((d.striker_dj30[d.dow.isin([1, 4])] != 0).mean(), 4))
print("MNQ entry rate:", round((d.striker_nas [d.dow.isin([0, 1])] != 0).mean(), 4))
PY

# §2.1 -- the gated statistic still exists (guard against breadth.py regressing)
grep -n "n_eff_risk_delta" lab/research_utils/breadth.py \
  || echo "breadth.py no longer emits n_eff_risk_delta -- R4 has no input"

# §6 -- the doctrine this spec rests on must remain closed absent a superseding ADR
git log -1 --format='%h %ci' -- docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md
grep -n "does not iterate weight\|NOT licensed" docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md

# T3 -- floor_at_k is the computed source (claim-alignment M10 2026-08-06);
# ST-EH-1's 0.98 / "at the cap" prose is historical banking record, not the live floor.
rg -n "def floor_at_k" lab/research_utils/axis_screen.py
python -c "import sys; sys.path.insert(0,'lab'); from research_utils.axis_screen import floor_at_k; print(floor_at_k(1))"

# S4 -- hedging clearance premise (c1 long-only) still asserted
grep -n "long-only" docs/adr/2026-07-17-c1-rail-build-account-registration-go.md

# §9.3 -- session-window pin. The lock files do NOT store the window numerically
# ("Entry session stays hour(time,'UTC') per source"), so this is a PROPERTY
# assertion, not a value grep (Trap M-AHF): the pins must still declare session
# logic unchanged. The empirical check is the day-of-week hook above -- if either
# edition's session is ever re-authored, off-schedule days become non-zero.
grep -n "session logic changed" \
  core/strategies/striker/striker_dj30_v4.5_mym_FUTURES_LOCK.md \
  core/strategies/nas/striker_nas100_v1_mnq_FUTURES_LOCK.md
```

---

## Verification

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py \
  docs/spec/2026-07-27-third-leg-target-spec.md --type inquire

# §0 anchors resolve
for f in ops/c1_rail/c1_sizing_host_reference.py lab/research_utils/breadth.py \
         docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md \
         lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md; do
  git log -1 --format="%h %ci $f" -- "$f"; done

# Published anchors this spec cites verbatim
grep -n "1.9593\|1.9628\|814\|932\|1761" lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage8_neff.md
grep -n "438\|273\|38.75" docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md
```

**Discipline checklist:** §0 populated with paths + anchors ✓ · two-basis hazard flagged ✓ ·
wrong-panel hazard flagged ✓ · falsifiable H in §5 with all three verdicts triggered numerically ✓ ·
§6 moves genuinely tempting (each was live this session) ✓ · §7 binary ✓ · §2.3 grounding limit
stated rather than implied (Trap #13) ✓ · doctrine-connected (Q-COMPOSE-1, Stage-8 ADR, envelope,
ST-EH-1) ✓ · §10 runnable ✓ · not-ratified status stated in the header ✓.
