# Q-6JCOMPOSE-1 — pre-registration: does adding Aegis-6J to the c1 book keep composed bust inside the ratified floor?

**Status:** `CLOSED — VOID (UNEXECUTABLE AS FROZEN)`, signed `2026-07-29 / JA` (§9), closed the same
day. **No 6J composed number was ever read.** Closure:
[`Q-6JCOMPOSE-1-closure-void-unexecutable.md`](../closures/Q-6JCOMPOSE-1-closure-void-unexecutable.md).
Successor: [`Q-6JCOMPOSE-2`](Q-6JCOMPOSE-2-verdict-preregistration.md) — itself subsequently
**CLOSED VOID** ([closure](../closures/Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md)).
Frozen body below is the record, byte-unchanged (Trap #12).
> **Header corrected 2026-08-02, in two passes — the first pass was wrong and is recorded rather than
> silently overwritten.** This line read `DRAFT — §9 UNSIGNED` from authoring (`cfe7fa7`) and was
> never updated by either the signing commit (`daf8f11`) or the closure, so the file simultaneously
> asserted `UNSIGNED` here and `SIGNED / FROZEN` at §9 while actually being `CLOSED VOID`. My first
> correction resolved only the header-vs-§9 contradiction and asserted *"SIGNED / FROZEN … UNRUN"* —
> **also wrong**, because it missed the closure entirely. Both errors have the same root: reading this
> file without reading its closure. **Metadata only — no gate, threshold, method, input or criterion
> has been moved in either pass.**

No item below changes after any composed number is seen —
amendments require closing this pre-registration and opening a fresh one (Known Trap #12). The
freeze is git-auditable: this file's commit must strictly precede any harness execution (§10 hook 1).
**Authored:** 2026-07-29 · Claude Code (Opus 5), operator-directed
**Loop of record:** OUTER (INQHIORI) — measurement against a ratified gate, not a tempo decision.
**D-S-A domain:** data. **Any live application is a separate `system` change** requiring an amending
ADR + operator GO — this brief cannot arm, size, admit, or edit anything.
**Artifact path:** `docs/briefs/pre-registration/Q-6JCOMPOSE-1-verdict-preregistration.md`
**Harness:** `lab/archive/q_compose_1_2026-07/run_compose_regime_remc.py` — the Q-COMPOSE-1 frozen
engine, to be **imported unmodified** with a third leg supplied as input.

---

## §0 — Rule-0 reads (verified this session 2026-07-29, HEAD `c12eb0c`)

Per the Q-COSTGEO-3 repair, each row states **the verification performed**, not merely the value.

| # | Artifact + anchor | Value consumed | Verification performed |
|---|---|---|---|
| 1 | `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md` @ `c12eb0c` | Frozen engine: 10,000 sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on, bootstrap n=100/126 bd seed 20260715. Floor: **bust ≤ 3.0% ∧ P(pass) ≥ 50%**, plus **bootstrap-95th ≤ 3.0%**. Four partitions: full / H1 2020-23 / H2 2023-26 / boot-95th | Read in full. Confirmed the 2-leg **1.00×** baseline row (full 2.65% PASS, H1 4.37% FAIL, H2 1.70% PASS, boot95 10.37% FAIL) and the composed ORB row (38.75 / 54.73 / 25.84 / 47.14). Confirmed the closure's own causal reading: **variance dominance**, not regime common-mode — ORB's $438/day exceeded the whole book's $273/day. |
| 2 | `lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md` @ `c12eb0c` L15 | **Baseline of record for this brief** — 2-leg book at WATCH-1 **0.50×**, corrected geometry, `Tradeify_Select_100K`: full **0.11% / P(pass) 99.80%**, H1 **0.22%** PASS, H2 **0.04%** PASS | Read L1–30. Confirmed the method line: frozen 2026-07-15 regime primitives + the 2026-07-22 correction idiom (`dd_lock_offset_usd → 1_000_000.0` on both `trailing_locking` tiers, restored after) + frozen 2026-07-16 haircut injection (`daily_100k × mult`). **Confirmed this file carries NO bootstrap** — L28 says so explicitly; the 1.20% boot-95th is a separate 2026-07-28 measurement and is consumed as a *cited* figure, not from this file. |
| 3 | `ops/instruments/6J.md` @ `c12eb0c` — findings J1, J4b, J7, J8 | Panel of record n=129, net +$39,056.10, PF 2.318, 1R $1,385.74 (full-stop mean, **n=10**); J8 deployed-rung standalone at cap 8 / $3.10 / constant 0.50×: **0.00% rot / 0.67% L13 / 0.77% L26**, eval pass 97.46%, consistency-OK 100% | Read the full DURABLE FINDINGS table + SESSION LOG. Confirmed the `venue-transfer` PROFILE cell is `AMBIGUOUS-PARKED`, **not falsified**, and that the v0.3 prototype is **do-not-deploy** (Aegis v4.3 is the only locked Aegis spec). |
| 4 | `docs/spec/2026-07-27-third-leg-target-spec.md` @ `c12eb0c` §7.1 / §7.2 | **S5** — must fit the §2.2 day-of-week cap table **without re-allocating cap from MYM or MNQ**. **S2** — expressible in micro contracts. **S7** — order-symbol occupancy. R1 ≤ ~$125/contract | Read §2.3 + §7.1 + §7.2 in full. Confirmed free micro-equivalent capacity is deterministic from locked Pine filters: **Mon 69 / Tue 0 / Wed 80 / Thu 80 / Fri 11**, and that **Tuesday is closed under any static scheme**. Confirmed §2.3 is self-labelled a **pre-screen, not a ratified gate** (Trap #13). |
| 5 | `core/firm_rules.py` @ `c12eb0c` `Tradeify_Select_100K` | `dd_type` `trailing_locking`, `starting_balance` 100000, `max_dd_pct` 3.0, `dd_lock_offset_usd` 100, `profit_target_pct` 6.0, `min_trading_days` 3, `micro_contract_cap` **80**, `consistency_rule_pct` 40.0, `cost_per_side_usd` 0.91 | Dumped the tier block programmatically this session. Note `cost_per_side_usd` 0.91 is the **index-micro** figure; full-size 6J is **$3.10/side** (row 6) and is NOT in `firm_rules`. |
| 6 | `lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/` @ `c12eb0c` — `RESULTS.md`, `RESULTS_R1.md`, `RESULTS_GAP.md` | J4b geometry equivalence; **R1 PASS** (6J 0.138× ORB per-contract, all-days); commission **break-even ≤ $1.30/side** vs Tradeify $3.10 / MFFU $2.56 / Bulenox $2.36 — all fail | Authored + run this session; reproduction control **12/12** against the committed J4 harness (both anchors to the cent, all ten published rows). Cap 8 is **INFERRED**; P&L re-scale is **linear**, not a native replay (F2 precedent ±2%). |
| 7 | `docs/methodology/regime_robustness_gate.md` @ `c12eb0c` | Both-halves discipline: a lever passes only if it passes on **both** half-panels, each pinned to the brief floor | Read in full. This is why §6 requires all four partitions and forbids a full-panel-only read. |

**Not read, and why it does not bind:** locked Pine sources (`**/*.pine`, gitignored). The 6J
prototype's session filter enters only through the panel's realized trade dates (§3 P1), which are
measured from the pinned CSV, never re-derived from Pine.

---

## §1 — Context + the question (symptom-only)

Aegis-6J has been PARKED under book-composition **D2** since 2026-07-16. Three of the reasons given
have since been shown wrong or moot: the FTA contract-type **mixing clause is rescinded**; the
"1R cohort n=1" figure scored an unreconciled export (panel of record is **n=10**); and the "J4
says it busts" reading rested on a **Bulenox ramp-up tactic** (0.5×-until-freeze-then-FULL) that no
c1 leg would run. At the **deployed** WATCH-1 0.50× constant rung the leg's standalone breach is
**0.67–0.77%** against a 3.0% ceiling.

None of that is admission evidence. The ratified gate is **composed** bust on the frozen engine, and
Q-COMPOSE-1 is the standing proof that standalone results do not predict it: adding ORB took the
book from **2.65% → 38.75%** on a leg whose own numbers looked survivable, via **variance
dominance**.

**Symptom-only phrasing:** *a candidate leg's standalone survival is now measured and clears, but
the quantity the admission floor is denominated in — composed book bust across all four partitions —
has never been computed for it.*

---

## §2 — Method (frozen)

**Engine:** `run_compose_regime_remc.py` imported **unmodified** from `lab/archive/q_compose_1_2026-07/`.
10,000 sims × seeds 42/123/2026, horizon 1500, Run-2 consistency-on, bootstrap n=100 / 126 bd /
seed 20260715. **No engine constant is touched.** If the harness requires a code change to accept a
third leg, that change is a **wrapper** that supplies input, and its equivalence must be proven by
reproducing the Q-COMPOSE-1 ORB row (§7 control C1) before any 6J number is read.

**Tier:** `Tradeify_Select_100K` only (the registered account). Other tiers are **not** run — adding
tiers is adding arms.

**Baseline (fixed, not recomputed):** 2-leg book at WATCH-1 0.50×, corrected geometry —
full **0.11%** / H1 **0.22%** / H2 **0.04%** / boot-95th **1.20%** (cited, §0 rows 2 + 6).

**The single composed arm (frozen — no sweep):**

| Element | Value | Why fixed |
|---|---|---|
| leg | Aegis-6J v0.3, **`ae744`** — n=152, sha256 `e82a2c25…`, **2020-02-24 → 2026-07-01** | **corrected pre-signature, 2026-07-29.** Originally read *"panel of record n=129 (`c3b34162…`) — the only 6J panel of record (J1)"*. **Both halves of that were wrong for this run:** (a) J10 established there is **no single** 6J panel of record — it is **per purpose**; (b) `8e269` starts 2022-01-12 and would **zero-fill H1** (2020-23 chop), systematically flattering the partition that governs — the defect P5 exists to prevent. `ae744` is the **operator PICK** (2026-07-15/JA), is **KNOWN-config** (J11), is **H1-covering**, carries a valid remc 1R cohort (**n=11**), and is what the frozen Class-S harness already pins. Amendment is legal: **§9 was unsigned**, so Trap #12 (no in-place amendment of a *frozen* artifact) does not bite. |
| ↳ cap re-scale | `ae744` is **cap 12** ⇒ arithmetic **12→8** re-scale required | inherits J10's **known-optimistic** bias (~0.4pp low on breach, +6.5% high on net) ⇒ **all composed breach figures are declared a LOWER BOUND, not point estimates** (§6 must read them that way) |
| lifecycle rung | **constant 0.50×** | the deployed c1 rung; identical to both incumbents |
| contract cap | **8** | inferred Tradeify mini-bucket limit (§3 P2) |
| commission | **$3.10/side** | verified cross-firm full-size 6J (2026-07-13) |
| session set | **Mon + Wed only** (Tuesday dropped) | forced by **S5** (§3 P1) |
| incumbent cap | **unchanged** MYM 69 / MNQ 11 | S5 forbids re-allocation |

**Exactly one composed cell is run.** No rung sweep, no cap sweep, no commission sweep, no tier
sweep. The rung/cap/commission values are inherited from prior measurement, not selected here.

---

## §3 — Preconditions (each must be discharged or declared BEFORE the run)

**P1 — S5 cap collision on Tuesday (MEASURED, binding).** At cap 8 × 0.50× = **4 contracts** =
**40 micro-equivalents** (10 micros = 1 mini). Free capacity by day is Mon 69 / **Tue 0** / Wed 80 /
Thu 80 / Fri 11. The 6J panel's realized day distribution is **Mon 44 (34.1%) · Tue 25 (19.4%) ·
Wed 60 (46.5%) · Thu 0 · Fri 0**. So **80.6% of the leg fits and Tuesday's 19.4% does not.**

> **Consequence, declared here rather than discovered later: the arm in §2 is a Mon+Wed VARIANT of
> the panel of record, not the panel of record.** Dropping 25 of 129 trades changes the leg's P&L,
> its serial structure, and its survival profile. The variant must be constructed by **date filter
> only** — never by re-running or re-fitting the strategy — and the dropped-trade count and net must
> be reported alongside the verdict.

**P2 — Cap 8 is INFERRED, not verbatim.** Tradeify publishes eval limits as mini/micro pairs
(`8/80` at this tier) and lists currencies in their own table, labelled neither mini nor micro. The
inference is that a full-size 6J counts against the **8** bucket at 10 micro-equivalents each. **If
this is wrong, both P1 and §2 are wrong.**
> **Operator disposition 2026-07-29: ACCEPTED AS INFERRED for now; verification delegated to
> operator (Tradeify support, separately).** Any verdict produced under this pre-registration
> therefore carries a standing conditional on cap 8, and §6 AMBIGUOUS fires if the verdict flips
> between cap 8 and cap 12.

**P5 — PANEL IDENTITY IS UNRESOLVED, AND IT IS DECISIVE. *** BLOCKING *** (found at Phase-0, 2026-07-29).**
The frozen Class-S scoring harness already wires an aegis leg
(`run_class_s_c1_scoring.py` `PANEL_FILES["aegis"]`, `CAL_STRATS`, `CAL_ALLOCS` aegis 0.0150,
`EXPECTED_1R_AEGIS` = $2,912.96 / n=11, `MIN_FULL_STOP_N` = 5) — so injection via the frozen
`build_scaled_panel` primitive is available and would resolve **P4 outright** (the harness
decompounds to a static basis and pins 1R by `full_stop_mean`). **But it pins a different export
than every measurement in this line.** At least four 6J exports exist:

| export | n | net | span | role |
|---|---:|---:|---|---|
| `…PROTOTYPE…2026-07-05_8e269.csv` | 129 | $39,056.10 | **2022-01-12** → 2026-07-01 | ledger **J1 panel of record**; basis of J4b / J7 / J8 |
| `…BEPAD-TEST…2026-07-11_ae744.csv` | 152 | $41,247.30 | **2020-02-24** → 2026-07-01 | **pinned by the frozen scoring harness** |
| `…BEPAD-TEST…2026-07-11_5274c.csv` | — | — | — | second BEPAD arm |
| `…BEPAD-TEST…2026-07-23_6aa5d.csv` | ~143 | — | — | book-composition input (§0.5(2) unreconciled) |

**Two measured facts make this blocking, not bookkeeping:**

1. **Window drives the verdict.** The composed panel inherits the 2-leg index (2020-01-06 →
   2026-06-30) and **H1 is the 2020-23 chop half**. On `8e269` the leg is zero-filled through
   2020-21, systematically flattering composed H1. Re-measuring the **J8 configuration** (cap 8,
   constant 0.50×, $3.10/side) on each panel: `8e269` → **0.67% L13 / 0.77% L26 (PASS)**;
   `ae744` → **6.26% / 3.43% (FAIL)**. The 23 extra trades add only **$1,759** of net and raise
   L13 breach **~9×**.
2. **`ae744` differs from `8e269` on 7 of 129 overlapping days** (e.g. 2023-03-08 $3,576.60 vs
   $3,974.00) — so it is not merely a longer window.
   > **⚠ CORRECTED 2026-07-29 (later).** This clause originally read that the divergence was
   > "consistent with a BE-pad `k>0` arm" and invoked Q-AEGIS-6J-BEPAD-1's `FALSIFIED` closure.
   > **That was an unsupported inference of mine.**
   > [`PANEL_OF_RECORD.md`](../../../lab/analysis/aegis/aegis_6j_transfer_2026-07-05/PANEL_OF_RECORD.md)
   > §1 classifies `ae744` as **PARTIALLY UNKNOWN** — BE-pad k, account size and `max_contracts`
   > are **not determinable from the bytes** — and the **operator PICKED `ae744`** for
   > prop-candidate remc scoring on **2026-07-15 / JA** (1R decompound @$200K `full_stop_mean`
   > **$2,912.96, n=11**). The frozen harness pin is therefore a **decision, not a defect**, and
   > `ae744` is **not** established as a falsified configuration. What is true and blocking is
   > narrower: its Pine inputs are **unclassified**, an item routed to the operator on 2026-07-14
   > and still unanswered.

> **✅ P5 DISCHARGED 2026-07-29 (later) — ledger J11.** `ae744` **is** KNOWN-config: the same Pine
> configuration as `8e269` (v0.3 PROTOTYPE, BE-pad **k=0**, cap 12, $100K, $1.30/side) exported on a
> 2020-start window; the `BEPAD-TEST` filename is a label carry-over. Decisive evidence:
> per-contract P&L identical on **all 129** overlap days, including **all 65 scratch (≤1-bar)
> trades** with **0** duration differences — the BE-pad floor acts on exactly that cohort, so a
> non-zero k cannot hide there. The 7 differing days are **+1 contract each** (TV
> percent-of-equity compounding from 23 extra earlier trades), and `ae744` belongs to a matched
> same-day 3-leg export set built for the 07-11 book re-MC at a common ~2020 window.
> **`ae744` is therefore the panel for this pre-registration**, and the run is specifiable.
> **Residual, non-blocking:** it is cap 12, so a cap 12→8 re-scale is required and inherits the
> **known-optimistic** bias measured in J10 (~0.4pp low on breach, +6.5% high on net) — declare the
> resulting figures as a conservative-direction *lower bound* on breach, not a point estimate.
> **§4's prior is unchanged: FALSIFIED expected.**
>
> ~~**Consequence (as corrected): no existing export is both KNOWN-config AND H1-covering.**~~
> The composed run **cannot be specified** until one exists. Producing it is an **operator TV
> re-export** of the hash-pinned v0.3 prototype at k=0 over 2020-01-06 → 2026-06-30 — a
> *measurement*, not a parameter change. Until then this pre-registration is **not signable**.

**P3 — Linear cap re-scale, not a native replay.** Per-contract P&L is re-derived arithmetically
(F2 precedent: ±2% vs a native TV run). A native cap-8 Mon+Wed replay would supersede.

**P4 — The 6J leg's daily series must enter the engine on the same basis as the incumbents.**
The incumbents' composed $273/day figure is a **static-$100K, deployable-weight** quantity; raw TV
panel P&L is **compounded** (measured this session: book trade-day std H1 $1,381 → H2 $2,282,
1.65×). The wrapper must de-compound the 6J series to the same basis or the composition is
apples-to-oranges. **This is the most likely silent defect in the run and must be controlled (§7 C2).**

---

## §4 — Falsifiable hypothesis + disclosed prior

**H:** Adding Aegis-6J (Mon+Wed variant, cap 8, constant 0.50×, $3.10/side) to the 2-leg c1 book at
WATCH-1 0.50× keeps composed bust **≤ 3.0% on all four partitions** (full, H1, H2, bootstrap-95th)
**and** P(pass) ≥ 50%.

**If** all four partitions are ≤ 3.0% and P(pass) ≥ 50%, **then** the leg is *screenable* (not
admitted; §8). **If** any one partition exceeds 3.0%, or P(pass) < 50%, **then** H is FALSIFIED and
D2's survival objection is re-established on the quantity that actually governs.

| Observation | Threshold | Conclusion |
|---|---|---|
| max(full, H1, H2, boot-95th) | ≤ 3.0% | H holds → RESOLVED-SCREENABLE |
| max(full, H1, H2, boot-95th) | > 3.0% | H falsified → FALSIFIED |
| P(pass) | < 50% | H falsified → FALSIFIED |

**⚠ PRIOR REVISED AT PHASE-0, 2026-07-29 — before any composed number, and in the unfavourable
direction.** P5 showed the J8 standalone PASS is **window-limited**: the same configuration on a
panel covering 2020-21 returns **6.26% / 3.43%, FAIL**. The standalone survival objection is
therefore **NOT resolved** — it is unconfirmed. Since composition adds variance, a leg that fails
standalone on the H1-covering window **fails composed a fortiori**, and the expected verdict is now
**FALSIFIED**. The original prior is retained verbatim below as the record of what was expected
before Phase-0 corrected it.

**Original disclosed prior (superseded): H holds on full/H1/H2 and
the bootstrap-95th limb is the live risk.** Reasoning, stated so it can be scored: 6J's per-contract
daily-$ std is **0.138× ORB's** (all-days), so the variance-dominance mechanism that destroyed the
ORB composition is ~7× weaker here. But at deployable weight (4 contracts) σ₃ ≈ **$150/day** against
a book ~$273/day ⇒ composed ≈ $311/day, an **inflation of ~+14%, above the spec's +10% design
budget** — so this is *not* a comfortable margin, and the boot-95th limb (which the 2-leg book only
clears at 1.20%, its tightest partition) is where a +14% inflation would first bite. **A verdict
that clears every partition by a wide margin should itself be treated as suspicious** and routed to
§7 control C2 (basis error) before it is believed.

---

## §5 — Forbidden moves

Each of these was genuinely available to the author; none is a strawman.

- **Re-allocating cap from MYM or MNQ to make Tuesday fit.** Directly violates S5, and it would
  silently re-open Q-CAPALLOC-1 (whose verdict is `AMBIGUOUS (d)` with 69/11 standing). Tuesday
  stays dropped.
- **Sweeping the lifecycle rung, cap, or commission to find a passing cell.** The best-of-K
  graveyard. All three are inherited as fixed inputs; the ladder was already tested exhaustively
  in J8 and is not re-opened.
- **Reporting the exhaustive-rotation row as the headline.** Its 95% CI at n=129 is
  [1.27%, 8.81%] and cannot resolve a 3.0% gate. Decisive rows are the engine's four partitions.
- **Reading full-panel only, or declaring PASS on three of four partitions.** The both-halves gate
  and the bootstrap limb are jointly required.
- **Treating a PASS as admission, or as licence to arm, size, or unpark.** See §8.
- **Dropping Tuesday silently, or re-fitting the strategy to a Mon+Wed session filter.** The
  variant must be a *date filter on the pinned panel*, disclosed with its dropped-trade count —
  never a re-run of the Pine, which would be a parameter change on a prototype and a fresh K.
- **Adding tiers, seeds, or horizons if the first result is unfavourable.** One cell, one tier.
- **Quietly substituting the raw compounded panel for a de-compounded one** (P4). If the basis
  cannot be matched, the run is ABORTED, not approximated.

---

## §6 — Gate (binary)

Assert against the four partitions at `Tradeify_Select_100K`, composed 3-leg vs the fixed 2-leg
baseline (0.11 / 0.22 / 0.04 / 1.20):

| Verdict | Trigger |
|---|---|
| **RESOLVED-SCREENABLE** | All four partitions **≤ 3.0%** AND P(pass) ≥ 50% AND controls C1–C3 green. The leg clears the survival floor as a composed member. **Admits nothing** (§8). |
| **FALSIFIED** | **Any** partition > 3.0%, OR P(pass) < 50%. D2's survival objection re-established on the governing quantity; 6J closes as a c1 third leg absent a new mechanism. |
| **AMBIGUOUS** | Controls C1–C3 not all green; OR P2 (cap 8) undischarged at read time and the verdict flips between cap 8 and cap 12; OR the Mon+Wed variant's dropped-trade effect is large enough that the leg's own economics fail (panel net below the $6,000 eval target), making a survival PASS meaningless. |

No criterion below moves after any number is seen.

---

## §7 — Prior looks, controls, and K accounting

**Prior looks — disclosed, because they burn something.** The author has already seen the 6J
**standalone** results at this exact rung (J8: 0.00 / 0.67 / 0.77%), the R1 measurement (J7), and
the commission break-even. **The composed quantity has never been computed.** The standalone look
does not burn the composed panel, but it does mean the author holds a directional expectation — hence
the §4 disclosed prior and the §5 no-sweep clauses.

**Controls, all required green before the verdict is read:**

- **C1 — engine equivalence.** The wrapper must reproduce the published Q-COMPOSE-1 **ORB** composed
  row (38.75 / 54.73 / 25.84 / 47.14 at `Tradeify_Select_100K`) to within reporting precision. If it
  cannot, the wrapper is not the frozen engine and the run is void.
- **C2 — basis control (P4).** The 2-leg baseline must reproduce **0.11 / 0.22 / 0.04** when the 6J
  leg is supplied as an all-zero series. Any deviation means the wrapper perturbs the incumbents.
- **C3 — variant disclosure.** Dropped-trade count (expect **25**), retained count (**104**), and
  the Mon+Wed net must be printed in the run log.

**K accounting: no new discovery K is consumed.** The candidate is pre-existing (`venue-transfer`
cell, `AMBIGUOUS-PARKED`), the gate is the ratified floor, and exactly **one** composed cell is run
with every input inherited rather than selected. This is a **measurement against a standing gate**,
not a search. Should the operator later request a sweep, that is a *new look* requiring its own
pre-registration and K.

---

## §8 — What a PASS licenses (and does not)

A `RESOLVED-SCREENABLE` verdict means **one thing**: the leg clears the survival floor as a composed
member of the book. It does **not**:

- unpark D2 (whose other conditions are governed by the book-composition brief and the operator);
- clear **S2**, which still excludes non-micro contracts by text — moving it is a **§6.1 event and
  an operator call**;
- discharge **P2** (cap 8 inferred) or **P3** (linear re-scale);
- authorize any rail change, arming, sizing, spend, or `LEG_MAP` edit — all of which require an
  amending ADR **and** a separate operator GO, sequenced **after** B7;
- alter the locked parameter axis in any way. The v0.3 prototype remains **do-not-deploy**; Aegis
  v4.3 remains the only locked Aegis spec.

Given the verdict-flipping arm that surfaced late in the J8 pass **from the author's own framing
error**, a PASS here should additionally be **adversarially reviewed** before it is cited downstream.

---

## §9 — Operator sign-off

**SIGNED / FROZEN: 2026-07-29 / JA** — operator approval given in-session, verbatim:
*"I approve running. consider it signed."* Freeze is in effect from this commit; the body below is
the record and **is no longer amendable in place** (Trap #12). Any change from here closes this
pre-reg and opens a fresh one.

**Pre-signature amendment disclosed (legal, and stated so it is auditable):** §2's leg row was
corrected from `8e269` (n=129, 2022-start) to **`ae744`** (n=152, 2020-start) *before* this
signature. Reason: `8e269` would zero-fill **H1**, the governing partition — the defect P5 exists to
prevent — and J10 established the panel of record is **per purpose**, not singular. `ae744` is the
operator PICK, KNOWN-config (J11), and H1-covering. This was amendable only because §9 was unsigned
at the time; it is not amendable now.

- [x] **Operator accepts §8 — a PASS admits nothing** (covered by the approval to run, 2026-07-29).
- [x] **Operator accepts the arm is a Mon+Wed variant** of the panel, not the panel (2026-07-29).
- [x] **Operator accepts cap 8 as inferred for now** (2026-07-29); Tradeify-support verification
      delegated to operator, handled separately. Any verdict carries a standing conditional on it.
- [x] ~~**BLOCKED — P5 panel identity.**~~ **DISCHARGED 2026-07-29 (later), ledger J11** — `ae744`
      is KNOWN-config (v0.3 PROTOTYPE, k=0, cap 12, $100K, $1.30/side) on a 2020-start window and
      **is** the panel for this pre-reg. **No operator TV re-export is required.** The method's
      input now exists.

**Author's recommendation (revised 2026-07-29, later): the run is now specifiable and cheap, but
§4's prior still expects FALSIFIED.** The re-export I previously said might be needed is **not**
needed — that was resolved from bytes at zero cost. The remaining decision is narrow and is the
operator's: sign and spend one frozen-engine run to convert an *expected* FALSIFIED into a
*recorded* one (which would close D2's survival limb on the governing window, on the ratified gate),
or accept the standalone evidence and leave D2 PARKED without the composed record. **I recommend
signing** — the run is one engine invocation, the prior is disclosed, and an unrecorded expectation
is exactly what this line keeps getting caught by.

---

## §10 — Audit hooks (runnable)

**Hook 1 — freeze precedes execution.** The pre-registration commit must be strictly earlier than
any composed report artifact.

```bash
git log -1 --format=%ci -- docs/briefs/pre-registration/Q-6JCOMPOSE-1-verdict-preregistration.md
```

**Hook 2 — engine unmodified.** Must return empty at run time.

```bash
git diff --stat HEAD -- lab/archive/q_compose_1_2026-07/run_compose_regime_remc.py
```

**Hook 3 — baseline figures still current.** Must return line 15.

```bash
rg -n "0\.11% / 99\.80%" lab/analysis/c1/class_s_c1_haircut_regime_remc_2026-07-16/CORRECTED_FULLPANEL.md
```

**Hook 4 — S5 collision reproduces.** Must print Mon 44 / Tue 25 / Wed 60 / Thu 0 / Fri 0 against
the pinned CSV (sha256 `c3b34162…`).

```bash
python lab/analysis/aegis/aegis_6j_trail_tradeify_2026-07-29/s5_day_distribution.py
```

**Hook 5 — no cap re-allocation smuggled in.** Must still show MYM 69 / MNQ 11.

```bash
rg -n "cap_alloc" ops/c1_rail/c1_sizing_host_reference.py
```

**Hook 6 — single-cell discipline.** Exactly one composed cell for `Tradeify_Select_100K`; more than
one composed cell in the run artifact is a §5 violation (no-sweep clause).

```bash
python -c "import json,sys; d=json.load(open(sys.argv[1])); print(len([k for k in d if 'composed' in str(k)]))"
```

**Hook 7 — lock untouched.** 0 HARD violations, and an empty diff on the locked surfaces.

```bash
python scripts/validate_params.py && git diff --stat HEAD -- core/ ops/c1_rail/c1_sizing_host_reference.py
```

---

## Verification

Run before declaring this pre-registration complete:

```bash
python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/pre-registration/Q-6JCOMPOSE-1-verdict-preregistration.md --type inquire
```
