# SLR-MYM-1 — sweep-liquidity-reclaim at the open, MYM third leg (scoping)

**Status:** **`CLOSED-FALSIFIED`** — closed at Stage 0 on 2026-07-29, **$0 spent / 0 K consumed**.
Closure record: [`docs/briefs/closures/SLR-MYM-1-closure-falsified-stage0.md`](../closures/SLR-MYM-1-closure-falsified-stage0.md).
Two independent gates fired: **0-A** (harvest Req-1a — both constraint framings fail the delete/flip
tests) and **0-C** (S5+S3 day set — best compliant set 81 IS entries vs a 120 floor). **0-B was
granted** (route 1 clears) and that ruling survives the closure. **The mechanism was never tested —
do not read this as evidence about sweep-and-reclaim edge** (closure §6).
**Authored:** 2026-07-28
**Closed:** 2026-07-29
**Authors:** Joshua (design) + claude.ai (brainstorm, authoring, review synthesis)
**Parent question:** N/A — cites Q-ICT-CASCADE-1 (closed) and the third-leg target spec as warrant, not as a re-gate
**Loop:** Inquire-phase Pre-Q — gates whether a liquidity-sweep-and-reclaim entry, gated by validated weekly/daily structure, is worth a data pull as a third c1 leg on MYM
**Artifact path:** `docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md`
**Type:** brief (Pre-Q scoping) · **Lane:** mechanism-first (harvest intake, in-house component reuse)
**Base:** `origin/main` @ `6502c7c` (third-leg spec) / `31d7df0` (K-ledger + ADR 2026-07-26)
**Proposes:** ONE pre-committed confirm, `K_intrinsic = 1`, on MYM.
**Does NOT propose:** re-opening Q-ICT-CASCADE-1, re-gating its M=65 survivors, composing into the c1 book ahead of Phase 4, a rail/Pine change, or any spend.

> **⚠ STAGE-0 EXECUTED 2026-07-29 — TWO GATES FIRED. RECOMMENDED DISPOSITION: `FALSIFIED (as scoped)`, $0, zero K.**
>
> The operator issued all three rulings; discharging them produced two independent kills, both free:
>
> - **Ruling A — "Admissible; the mechanism is more sophisticated than 'stops get hunted'."** The
>   operator's *ground* is correct (§2.6.1 names a measured effect, not a story), but sophistication
>   is not what ADR 2026-07-26 §2-A tests. Two constraint framings were drafted and each adversarially
>   refuted; **neither survives the delete-test or the flip-test** — remove the constraint story and no
>   §1 rule changes; reverse its sign and no §1 rule changes. A warrant whose truth value cannot touch
>   the trade rule is §5 laundering. **Path 1a cannot be written.** (§2.6)
> - **Ruling B — "questioning the three-route disjunction."** Well-founded on a real axis, and
>   **granted**: the bar's scope is broader than its evidence, and **route 1 clears** (§2.7). But it
>   **blocks nothing** — the bar is a ledger-layer gate the ratified third-leg screen never imports.
> - **Ruling C — "test all days, remove the days that wouldn't work."** Executed as a **measured**
>   census on the local panel (§7 Phase 0.5). **No S5-compliant day set reaches the pre-registered
>   120-entry IS floor** — best available is **81** — and the proxy used is a deliberate *upper*
>   bound, so real 1-minute counts are lower. **Stage 0-C fires FALSIFIED on arithmetic.**
>
> The cap-reallocation rider cannot rescue it and is separately out of scope for this artifact
> (§2.5.1). Disposition is the operator's; the pre-registered trigger has fired.

---

## §0 — Rule 0 reads (production + artifact source, verified this session, 2026-07-28)

| Path | Anchor | What it grounds |
|---|---|---|
| `docs/spec/2026-07-27-third-leg-target-spec.md` | `6502c7c` 2026-07-27 | RATIFIED §7 screen (S1–S6, R1–R5, T1–T5, M1–M3) — **scored explicitly in §2.5**; §7.5 negative control (ORB-MNQ SCREEN-FAIL on five grounds); §2.2 day-of-week cap table; §2.3 R1 derivation + basis caveat; §2.4 Slot-1/Slot-2 definitions and the Slot-1 power cost; §6.2 SCREEN verdict mechanics |
| `core/firm_rules.py:319-332` | `cb60516` 2026-07-26 | `Tradeify_Select_100K`: `max_dd_pct=3.0` ($3,000 EOD trailing), `dd_lock_offset_usd=100` (**open defect, next row**), `daily_loss_pct=None`, `profit_target_pct=6.0`, `min_trading_days=3`, `weekend_holds=False`, `inactivity_max_idle_days=5`, `micro_contract_cap=80` (**account-aggregate**), `cost_per_side_usd=0.91`, `consistency_rule_pct=40.0` |
| `core/firm_rules.py:264-290` | same | **Open defect, unfixed.** Coded `dd_lock_offset_usd=100` models a drawdown *lock* the eval phase does not have (Tradeify verbatim, article 10495897: "Evaluation accounts do not have drawdown locking"). Fix = unreachable-offset variant `1_000_000.0` (idiom verified in `tests/core/test_trailing_locking_boundary.py`). Measured correction: book-alone Part A bust **2.65% → 4.74%** — i.e. **already above the 3.0% ceiling at 1.00×**, which is why §6 Stage 4 must declare its weight basis (see §6) |
| `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md` **§2-A** | `31d7df0` 2026-07-26 | **The admissibility blocker.** Req-1a sharpened to a four-clause constraint test; verbatim: *"Preference/behavioral stories (\"retail chases,\" **\"stops get hunted\"**) no longer satisfy 1a — they route to 1b's four-part evidence-robustness test or die."* SLR-MYM's mechanism story is a stop-run story. See §2.6 |
| same ADR **§2-C** + change history | same | Executed-K closure rule; worked example verbatim: *"MNQ bank 2 → K_eff 3 → floor 0.98 (open, but AT the cap...) **MYM bank 1** → K_eff 2 → **floor 0.85**"*; ST-EH-1 `K=2` spans TWO families (1 MNQ + 1 MYM) — do not add 2 to either. §5 also requires a dedup attestation that **pastes command output**, searched **by mechanism family** |
| `docs/rejected_candidates.md:402-436` | `fbf3590` 2026-07-27 | **The domain raised bar, actual text.** "Single-instrument index-futures intraday OHLCV directional timing — RAISED BAR (tail-exhaustion; **NOT** a SNAG closure) 2026-07-21." Verdict **STABLE (saturating)**, 1-admission not 0. Re-proposal test is a **three-route disjunction — clear ONE of**: (1) a mechanism **outside the mapped cost-ratio-lever set** {price, instrument-selection, hold-time}; (2) a **different modality** or a **venue** relaxing a binding wall; (3) evidence it **beats incumbent ORB-MNQ net-of-cost**. Scoped to "*directional intraday timing* … from **OHLCV structure alone**, deployable **flat-by-close**" |
| `lab/archive/ict_cascade_2026-06-18/PREREG-W.md:28,54,60-62,78` | `fad8984` 2026-07-14 | **Tier 1, verbatim.** `vStruct = close > wEma ? 1 : close < wEma ? -1 : 0`; `emaLen = 20` **LOCKED**; verdict object `gateBias = vStruct`. **Scope limit, load-bearing:** L62 — `gateBias` "fixes **leg (a) only** … It is STILL a **weekly-close proxy**, NOT per-entry gate accuracy (**leg b**)"; leg (b) is a *separate* probe, explicitly **not settled** |
| `lab/archive/ict_cascade_2026-06-18/CLOSURE-1M-INSUFFICIENT-N.md:53` + `TEST_PLAN.md:25` | `47cc3eb` / `fad8984` | **Tier 1, grepped verbatim.** W: `gateHitRate` **0.5571**, 95% block-CI **[0.5242, 0.5901]**, halves 0.547/0.567, thirds 0.561/0.555/0.556, **eff_N 910**, **COMPOSITE-KILLED**. Routes to "path-independent confirmation, **not deploy**"; **"NOT a 1M-gate license"** |
| same, 1M closure body | `47cc3eb` | **The 1M layer closed on TWO independent grounds, not one.** Ground 1 = **0/247 limit orders filled** (entry-mechanism non-viability, logged HIGH confidence, characterized instrument-general). Ground 2 = the TV 1m data wall. **Only ground 2 is removed by databento** — see §2.1 |
| `lab/archive/ict_revcon_2026-06-19/` (`Q-ICT-1M-ENTRY-1`) | archived 2026-07-12 | **Lineage the first draft omitted.** The 1M entry-redesign re-attempt: broke the fill wall, returned **n=23, drop-top-1 negative**, CLOSED NOT-CONFIRMED. Directly relevant precedent for any 1M-execution redesign |
| `lab/archive/pharos_us500_sweepfvg/README.md` | archived 2026-07-12 | **Tier 1.** ICT sweep→FVG→pool-draw on Pepperstone US500 **15m CFD**. FALSIFIED 2026-06-17: signal real (block-perm **p=0.0144**) but **drop-top-3 = −0.152R**, 3-trade-concentrated, block-CI straddles 0 |
| `ops/instruments/MYM.md` | last updated 2026-07-25 | Five DEAD entries (§2.2 table); **M6 cost hurdle 6.57 bp/event — which IS ALREADY the 4× figure**, verbatim "4× Tradeify hurdle ≈ 6.57 bp/event"; `bars:` carries the raised-bar id; M7 panel provenance (`MYM_M15.csv`, n=141,471, 2020-07-01→2026-07-03Z). **Two internal contradictions flagged, not corrected here:** its prose says "MYM family K bank remains **0**" (stale — the ADR banks 1) while its DEAD table records `K` = **2** for `S-MYM-ORC-02` (see §0.1) |
| `lab/discovery/cost_model.py:58-71` | PR #515 | `MYM = InstrumentSpec(multiplier=0.50, tick_size=1.00, tick_value=0.50)` — MYM tick is **1.00 index point**, not MNQ's 0.25. `bp_hurdle()` requires `firm_key` + `slip_ticks` + `slip_convention`, no defaults |
| `docs/briefs/pre-registration/Q-COSTGEO-1-verdict-preregistration.md:13,21` | 2026-07-23 | Standing convention `SLIPPAGE_TICKS_PER_SIDE = 1.0`, **declared, never measured**. Its own finding: the B6 dry-fire (n=1, −$[redacted]) "**is not a slippage measurement**." No measured slippage figure exists in this repo |
| `lab/discovery/register_search.py` | `67cc146`+ | **Three HARD gates on a `mechanism-first` `open`:** `--profile-cell <SYMBOL>:<mechanism-id>`, `--profile-consult <saved output>`, and `--reachability-attestation` (§R, per-clause, same-units, panel-basis — ADR 2026-07-13 §4.4 + ADR 2026-07-16 §2.1–2.3). All three are pre-registration deliverables; enumerated in §8 |
| `core/data/bar_data/MYM_M15.csv` | present in the **primary checkout** (8.2 MB, 2026-07-21); **absent from this worktree** (vendor data is gitignored) | A **$0** local 15m panel that can bound the event rate before any paid pull — see §7 Phase 0.5 |
| `lab/research_utils/breadth.py` | `bd92d8e` 2026-07-24 | Emits `n_eff_risk_delta` (R4) — necessary, **not sufficient** (spec §2.1: ORB passed at +0.003 then produced 38.75% bust) |

### §0.1 — K-ledger reproduction (run this session)

```
d5_nq_intraday_mom             closed  K=1     (MNQ)
orb_mnq_intraday_breakout      open    K=1     (MNQ — OPEN, banks nothing per harvest Req 3)
st_eh_supertrend_grid          closed  K=2     declared_K=84  operator-stopped
                                                 executed_looks = 1 MNQ + 1 MYM (split; do not add 2 to either)
disccamp0_gc_2010_18           closed  K=3177  (GC/MGC — dead family)
h_od_1 / harv2026 / fb_eia / fc_carry   closed K=1 each (ES/CL/6E)
```

`floor_at_k(2) = 0.85`, `floor_at_k(3) = 0.98`, `CAP = 1.0` — reproduced from `floor_scan.py`.
**MYM family bank = 1** ⇒ with `K_intrinsic = 1`, `K_eff = 2`, **DSR floor 0.85**, headroom 0.15 under the Cap.

**⚠ Disclosure — an unreconciled MYM K claim outside the manifest ledger.** `ops/instruments/MYM.md`'s DEAD table records `K` = **2** for `S-MYM-ORC-02` (two pre-registered, operator-signed, executed MYM trials). The codified banking convention (harvest Req 3) defines `K_banked(family)` from **closed manifests only**, and no ORC manifest exists — so bank = 1 and floor 0.85 stand **on the convention as written**. But if those two trials are ruled bankable, MYM goes to 3 ⇒ `K_eff` 4 ⇒ floor **1.06 > Cap 1.0 ⇒ FAIL-K at Stage 0**, and this campaign is dead before it starts. **This is a Stage-0 disclosure item, not a settled fact**; it is surfaced here rather than left for a later audit to find.

**Divergent-citation note (corrected 2026-07-28).** `WSTRUCT-M2K-1` §3.1 treats ST-EH-1's *declared* K=84 as binding for the MNQ/MYM family (floor 1.620, "0.62 above the Cap"). This brief uses the ADR's ratified executed-K disposition instead. **The first draft of this brief explained the divergence as WSTRUCT-M2K-1 being unable to read an unpushed manifest; that explanation is wrong on git and is withdrawn.** WSTRUCT-M2K-1 landed at `5120f63` (2026-07-26 23:16:18) and the executed-K disposition at `31d7df0` (2026-07-26 23:57:32) — the **same day, 41 minutes later**, so the disposition did not yet exist in any commit when WSTRUCT was authored. WSTRUCT took a defensible conservative doctrinal position that **ADR §2-C subsequently superseded**. The ADR is the newer, higher-tier, directly-verified source and governs. WSTRUCT-M2K-1's own verdict is unaffected (it died independently on cost-law); no correction to that file is proposed here.

### §0.2 — Corrections carried from authoring and review (precision-vs-grounding, Trap #13)

1. **The structure filter is `close vs EMA(20)`**, not swing/pivot structure. The daily leg is a *fresh, parameter-free extension* of the same rule, **never independently gated** — PREREG-W's verdict is "weekly-close structure-only… no more."
2. **No measured slippage figure exists.** Standing convention is `slip_ticks = 1.0/side`, declared-not-measured.
3. **`6.57 bp/event` is already the 4× hurdle.** The first draft's §4/§6 said "≥4× the pinned 6.57 bp hurdle," double-applying the multiple (16× RT). Corrected throughout — see §2.3.
4. **The 1-ATR reachability cap does NOT bound the stop.** The first draft claimed it "doubles as a stop-distance ceiling." False: the cap constrains (09:30 open − armed level); 1R = (sweep excursion below the level) + buffer, which that cap does not bound. A separate explicit stop cap is now declared in §1.

---

## §1 — Mechanism spec (frozen constants; every ambiguity resolved)

Instrument **MYM**, RTH open **09:30 ET**. **Long-only. One trade per day maximum. No adds, no pyramid, no re-entry after exit.** All times ET.

**Bar/session bases (declared, non-repainting):**
- **Weekly and daily `vStruct`** use the **prior completed** weekly/daily bar (`close[1]` convention, inheriting the cascade's own non-repaint fix). Nothing computed at 09:30 may reference the in-progress daily bar.
- **Daily/weekly bars are RTH-basis** (09:30–16:00 ET), derived from 1m, ET-bucketed. `ATR(14, daily)` is on the same RTH-basis daily series, **as of the prior close**.
- **Prior-day low** = prior RTH session low. **Overnight low** = Globex low from 18:00 ET prior day to 09:29 ET. **Prior-week low** = prior completed RTH week.

**Gate (pre-09:30):** weekly `vStruct` bullish **AND** daily `vStruct` bullish. Either not bullish → **no trade**.

**Level menu:** the nearest level **strictly below the 09:30 open** among {prior-day RTH low, overnight low, prior-week low}.
- Ties (two levels equal): treat as one level.
- **No level below the open** (gap-up above all three) → no trade.
- **Nearest level > 1×ATR(14, daily) below the open** → no trade (reachability).
- **The 09:30 open is already below a level** (gap-down through it): that level is **consumed, not armed** — a gap-through is not a sweep. Arm the nearest level below the *open*.

**Sweep (09:30–10:00):** the armed level is swept when a 1m bar's **low trades strictly below** it. **First sweep only**; a later sweep of the same level does not re-arm. No sweep by 10:00 → no trade.

**Reclaim (trigger):** a 1m bar **closes strictly above** the armed level, at or before **10:15**. Enter long at the **next 1m bar's open**.
- **Same-bar sweep and reclaim** (one 1m bar's low < level and close > level) **counts** as sweep + reclaim; entry is the next bar's open.
- No reclaim by 10:15 → no trade.

**Stop:** `sweep_extreme − max(2 ticks, 0.10 × ATR(14, daily))`, where `sweep_extreme` = the lowest low printed from sweep bar through the entry-signal bar inclusive, **frozen at entry**.
- **Stop cap (new, §0.2 item 4):** if the resulting stop distance exceeds **0.50 × ATR(14, daily)**, no trade. This is the bound the reachability cap does *not* provide, and it is what makes 1R boundable for R1.

**Target:** **+1.5R** (`R` = entry − stop), resting limit, no trail, no breakeven move.

**Intrabar resolution (declared — this materially moves backtest results):** if a single 1m bar touches **both** stop and target, the **stop is taken**. No favorable-ordering assumption, at any resolution.

**Time-flat:** market order at **13:00**, cancelling any resting stop/target in the same bar.

**Deployment day set: OPEN — Stage-0 ruling C (§6).** The mechanism carries **no day term** (M1 day-agnostic by construction) and the confirm measures all five weekdays. But S5 forbids requiring Tuesday (0 free cap), and the day set materially changes N — see §2.5.

---

## §2 — Prior art, screen scoring, and admissibility

### §2.1 — Cascade components: what they license, stated at their actual scope

- **W-layer RESOLVED** (`vStruct`, 0.5571) — this brief uses it as a **pre-trade filter**. **Honest scope statement (corrected):** the W verdict fixes **leg (a) only** (weekly-close structure-only hit-rate) and PREREG-W explicitly does **not** settle leg (b) (per-entry gate accuracy), and its closure states it is **"NOT a 1M-gate license."** The first draft's claim that this use is "exactly as its own closure licensed" **overclaimed and is withdrawn.** Using vStruct as a daily filter on a 1-minute entry is a **new expression that cites W as warrant**, and its per-entry transfer is **assumed, not established** — a declared risk this campaign carries, not a validated premise.
- **D-layer** — **neither side transfers.** SSL FVG-draw RESOLVED (0.795 vs base 0.712) is a **10-day** reachability claim about **fair-value-gap** objects; this design's menu is **pivot-class**, the class the D-layer **FALSIFIED as attractors on both sides** (BSL pool 0.55 vs base 0.76; SSL 0.34 vs base 0.61 — swept *less* than radius-matched random). Cited so no reader conflates them; **§5 forbids** citing 0.795 as support.
- **1M layer** — **closed on two independent grounds, and only one is removed.** Ground 1: **0/247 limit orders filled** — an entry-mechanism non-viability finding, logged at HIGH confidence and characterized as instrument-general. Ground 2: the TV 1m data wall. **databento removes ground 2 only.** SLR-MYM's answer to ground 1 is structural rather than evidential: it enters on a **bar-close reclaim with a market order at the next bar's open**, never a resting limit at an FVG mid — the exact fill mechanism that returned 0/247. That is a reason to expect fills, not evidence of an edge.
- **`Q-ICT-1M-ENTRY-1`** (`lab/archive/ict_revcon_2026-06-19/`) — the entry-redesign re-attempt that **did** break the fill wall and returned **n=23, drop-top-1 negative**, CLOSED NOT-CONFIRMED. Omitted from the first draft; it is the closest precedent to this campaign and its n=23 is a warning about conditioned-stack starvation.

### §2.2 — MYM DEAD list (`ops/instruments/MYM.md`), scored against this design

| Rejection | Class | Distinct because |
|---|---|---|
| `S-MYM-ORC-02` (D2–D8 FAIL, N=403) | Opening-range **continuation** | Direction of the trade relative to the level is opposite: continuation *through* the range vs reversal *against* a breach. **Weakest distinction in this table** — both are opening-window level-relative constructs; argued at Stage 0, not asserted |
| `S-MYM-ORC-01` (AMBIGUOUS-HOLD) | Continuation, force-flat blind spot | Same family; its finding is a spec blind spot (53 exchange early closes) — **inherited as a hazard by this design**, see §2.5 S1 |
| `MYM-3FPS-1` (power + cost FAIL) | Calendar/expiry **reversal** | Different WHEN clock — 3rd-Friday settlement, not the daily open |
| `OPENPRESS-1` (wrong-signed + cost FAIL) | Opening **volume × directional efficiency** | Different signal class — volume/efficiency statistic, not a price level. ~~Raised the domain bar in §2.7~~ — **corrected 2026-07-29: false at source.** The §2.7 bar was raised by the 2026-07-21 programme audit on a four-closure basis (D5, D5-RECOST, H-TSMOM-1, cross-index-RV); OPENPRESS-1 is not its origin |
| DJ30→MYM transfer (R5) | Venue/cost parity transfer | Not a new-mechanism test |

### §2.3 — Cost law (corrected — the double-4× is removed)

**MYM primitives:** commission `$0.91`/side ⇒ `$1.82`/RT; slippage `1.0 tick/side × $0.50 tick_value × 2` = `$1.00`/RT ⇒ **RT = $2.82**. **4× cost law ⇒ $11.28 per contract per trade.**

**`6.57 bp/event` (MYM.md M6) IS ALREADY the 4× hurdle** — it must be *met*, never multiplied again. §4 and §6 are corrected accordingly.

**⚠ The pinned bp figure is loose on this campaign's panel, and the gate is therefore stated in $/contract/RT.** M6's 6.57 bp was computed at `median_friday_open` ≈ 34,312 over MYM-3FPS-1's **full 2019–2026** third-Friday span. SLR-MYM's declared IS is **2019–2023**, a materially lower-priced regime, so the same $ cost is a **larger** bp fraction there — reusing 6.57 bp unadjusted would set a **looser** gate than the cost law requires. Harvest Req 5 (same-units, own-panel basis) forbids this. **Binding form of T1 for this campaign: gross edge ≥ $11.28 per contract per round trip, at the panel-era price basis, computed by `cost_model.py::bp_hurdle()` on the IS panel's own median price — not by importing M6's number.**

**Win-rate implication (with the correction that the first draft's two-outcome formula ignores time-flat exits):** at 1.5R/−1R and a 100pt stop (1R = $50), the hurdle is 0.2256R ⇒ break-even WR **49.0%**; at a 60pt stop (1R = $30) ⇒ **55.0%**; at the §2.4 floor case (40pt stop, 1R = $20) the hurdle is **0.564R** ⇒ WR **62.6%**. **The two-outcome formula is optimistic**, because 13:00 time-flat exits land between −1R and +1.5R and drag realized expectancy toward zero. Phase 2 must compute expectancy from the **realized three-outcome distribution**, not this formula, which is a screening bound only.

### §2.4 — R1 pre-screen arithmetic (estimate, pending Phase-2 measurement)

Spec §7.2 makes R1 (**per-contract** daily-$ std ≤ ~$125 at the $100K basis) the requirement a candidate "fails first and cheapest." SLR-MYM's stop geometry is declared (§1) **including the new 0.50×ATR stop cap**, so R1 is computable pre-pull, avoiding `SCREEN-DEFER`.

With MYM at `$0.50`/index-point and the stop bounded above by `0.50 × ATR(14, daily)`: on plausible recent-regime daily ATR (≈300–500 Dow pts) the stop spans ≈**40–250 pts**, i.e. per-contract **1R ≈ $20–125**. Outcomes are bounded by construction, one trade/day, no adds.

| 1R/contract | entry rate | per-contract daily-$ std | vs $125 wall |
|---|---|---|---|
| $60 | 0.132 (measured proxy, §7 Phase 0.5) | ≈ $26 | **PASS** |
| $60 | 0.40 | ≈ $46 | **PASS** |
| $125 (stop-cap worst case) | 0.40 | ≈ $95 | **PASS**, thin |
| $125 | 1.00 | ≈ $150 | **FAIL** — but unreachable: entry rate cannot be 1.00 under the §1 gate stack |

**The coefficient is an approximation and is flagged as such.** For outcomes {+1.5R w.p. p, −1R w.p. q, ≈0 otherwise} at entry rate e, the daily-series std is `R·√(e·(2.25p + q) − e²·(1.5p − q)²)`; at p=q=0.5 this is ≈ `1.27·R·√e`, close to the `1.2·R·√e` used above. Non-entry days contribute 0 to the numerator but **do** enter the denominator — handled by the `√e` term.

**Grounding limit (Trap #13).** The ATR range and the outcome coefficient are **assumptions**; no MYM 1-minute panel has been examined. This is a pre-screen that decides what is worth running (spec §2.3's own framing), never a substitute for Phase-2 measurement or the Phase-4 frozen engine. **R2 and R3 are NOT derivable from R1** — both are defined at the **deployable weight**, and this brief declares **no contract count**; ORB's ρ = 1.60 came from 438/273 at k ≈ 2.31 contracts. The first draft's claim that "R3 follows from R1 by the same arithmetic" is **withdrawn**; R2/R3 are Phase-2 outputs once a weight is set.

**Do not confuse with MYM.md M7.** M7's provisional 1R floor (full-median **$3,234**) is the *locked incumbent leg's* position-level 1R at deployed size — a different quantity at a different basis from the **per-contract** $20–125 here. They are not reconcilable and must never be compared.

### §2.5 — §7.1 hard-structural screen (S1–S6), scored — the section the first draft omitted

| # | Requirement | SLR-MYM | Verdict |
|---|---|---|---|
| S1 | Flat before 16:45 ET | flat 13:00 | **PASS** — ⚠ with a hazard: Tradeify's deadline is **12:59 ET on holiday-short sessions**, and MYM.md M4 records a prior candidate killed by exactly this blind spot (53 exchange early closes). §1's 13:00 flat is **after** 12:59 on those days. **A holiday-calendar early-close rule is owed at pre-registration** |
| S2 | Micro contracts | MYM | **PASS** |
| S3 | Attended existing rail | ⚠ **UNRESOLVED — flagged as a Phase-0 verification item.** Both the incumbent Striker DJ30→MYM leg and SLR-MYM resolve to the same order symbol `MYM1!`. Whether the rail/sizing host can attribute and net two independent strategies on one symbol is **not established in this brief** and must be verified against `ops/c1_rail/c1_sizing_host_reference.py` before any GO. If it cannot, this is a **rail redesign**, not a slot addition | **UNRESOLVED** |
| S4 | Long-only if Equity Index | long-only by construction; bearish alignment = stand-aside | **PASS** |
| S5 | Fits the day-of-week cap table without re-allocating from MYM/MNQ | **FAILS AS WRITTEN** — §1's mechanism fires any weekday, so it requires **Tuesday**, where free cap is **0** (MYM 69 + MNQ 11 = the full aggregate 80). This is **verbatim ORB-MNQ's §7.5 S5 FAIL** | **FAIL → forces Stage-0 ruling C** |
| S6 | No US Treasuries | MYM | **PASS** |

**Stage-0 ruling C — EXECUTED 2026-07-29, and it fires FALSIFIED.** Spec §7.4 M1 permits *scheduling* a day-agnostic mechanism into free days. The operator ruled "test all days, and remove the days that wouldn't work." That is implementable in exactly one form (§2.5.2), and executing it kills the campaign on arithmetic.

**Two structural constraints close days, both invariant to data:**

1. **S5 — free contract cap.** Tuesday has **0** free micros (MYM 69 + MNQ 11 = the full aggregate 80).
2. **S3 — order-symbol occupancy (found in review; this is the one the first draft missed).** Both the incumbent Striker DJ30→MYM leg and SLR-MYM resolve to the **same order symbol `MYM1!`**, and the venue holds **one net position per symbol per account**. On days the incumbent MYM leg can fire — **Tuesday and Friday** (spec §2.2) — a second MYM strategy cannot hold an independent position **regardless of how much cap is donated to it**. This is a position-netting fact, not a sizing fact.

**Together they close Tue and Fri**, leaving **Mon + Wed + Thu** as the only S5-and-S3-compliant set.

**Measured (§7 Phase 0.5, real panel, IS partition = 860 sessions):**

| Day | IS sessions | IS entries | rate | free cap | S3 clash |
|---|---|---|---|---|---|
| Mon | 158 | 21 | 13.3% | 69 | — |
| Tue | 178 | **31** | 17.4% | **0** | **incumbent MYM** |
| Wed | 179 | 26 | 14.5% | 80 | — |
| Thu | 175 | 34 | 19.4% | 80 | — |
| Fri | 170 | **31** | 18.2% | 11 | **incumbent MYM** |

| Day set | IS entries | vs the pre-registered 120 floor |
|---|---|---|
| Wed + Thu (spec Slot 1) | **60** | **BELOW** |
| **Mon + Wed + Thu** (the only compliant set) | **81** | **BELOW — Stage 0-C FIRES** |
| Mon + Wed + Thu + Fri (S3-noncompliant) | 112 | BELOW |
| All five (S5- **and** S3-noncompliant) | 143 | clears — but not deployable |

**The proxy is a deliberate UPPER bound.** It counts a sweep at *any* time of day, whereas §1 requires the sweep inside 09:30–10:00 with a reclaim by 10:15. Real 1-minute counts are therefore **lower**, not higher — a day set below the floor here **cannot** clear it on real data. The kill is robust in the direction that matters.

### §2.5.1 — The cap-reallocation rider (operator ruling C, second limb)

The operator is "open to this replacing some of the cap held by the Striker legs if the data points to it increasing pass rate." Three things, in order of decisiveness:

1. **It cannot rescue the day set.** The Tuesday/Friday obstruction is S3 (one net position per symbol), not cap. Donating cap does not create a second independent MYM position.
2. **It is procedurally closed to this artifact.** Spec §5, verbatim: *"Cap re-allocation in **either** direction is owned by Q-CAPALLOC-1 and its successor ADR, **never by a third-leg proposal**."* S5 is a §7 threshold that moves only by a superseding ADR.
3. **"Increases pass rate" is not the right target.** In this engine pass rate is identically `1 − P(bust)` with **no P&L term**, so it is maximised by trading *less*. The load-bearing counterexample is on this exact book: Q-COMPOSE-1 added ORB-MNQ — a **positive-expectancy** leg — and bust went **2.65% → 38.75%**. Adding expected return raised failure ~15×. The implementable criterion is Q-CAPALLOC-1's ratified D1–D5 bundle (time-to-payout and E[cash] as *objectives*; pass rate and 1-yr mortality as *guards*), scored on **both** halves.

### §2.5.2 — "Remove the days that wouldn't work" — the only compliant reading

The literal reading (drop days whose realized P&L was poor) is **outcome-conditional day selection**: it voids §7.4 M1 and is already forbidden by §5. The compliant form is an **information-set constraint**: the day set must be a deterministic function of `(cap table, order-symbol occupancy, exchange calendar)` — all knowable **before** any outcome is examined — and is frozen at pre-registration. Under that rule Tue and Fri are removed *structurally* (cap 0; symbol collision), and **no day may be removed on realized-performance grounds at any later point**.

### §2.6 — Harvest admissibility (Req 1a / 1b and Req 2) — Stage-0 ruling A

**This is the most likely kill in the brief, and it is free.**

ADR 2026-07-26 §2-A (effective 2026-07-26, ratified) sharpened harvest Requirement 1a to a four-clause **constraint** test — WHO pays (a constraint, not a preference) / WHEN it must appear / WHY it survives / HOW it dies — and names this brief's own mechanism story as inadmissible, **verbatim**: *"Preference/behavioral stories ('retail chases,' **'stops get hunted'**) no longer satisfy 1a."*

SLR-MYM's mechanism *is* a stop-run story. Therefore:

- **Path 1a is closed** unless a genuine constraint-based WHO can be named — an identified counterparty class trading under **mandate, benchmark, or mechanical rule**, not preference. Resting retail stops are placed by preference even though they execute mechanically; **this brief does not claim to have cleared that bar.**
- **Path 1b** (untouched by the ADR) requires **all four** of: ≥3 decades covered · ≥3 independent cohorts · ≥1 replication ≥10 years post-discovery · no known sign-reversal condition. **This brief asserts none of them.** Meeting 1b requires a real literature pass on stop-cascade / liquidity-run evidence, which has **not been done**.
- **Req 2** (cohort-cited **per-instrument** δ/σ, no cross-instrument transplants): **not satisfied.** No cohort-cited δ for a sweep-reclaim effect on MYM/YM exists in this brief. The 2026-07-28 M2K ruling refused a proposal on precisely this ground.

### §2.6.1 — Ruling A executed (2026-07-29): both framings drafted, both refuted

The operator ruled **admissible**, on the ground that the mechanism is "more sophisticated than 'stops get hunted'." **That ground is correct and is not overruled here** — but sophistication is not what §2-A tests. Two constraint framings were written to §2-A's specificity standard and each was adversarially refuted:

| Framing | WHO it names | Verdict |
|---|---|---|
| **1 — mechanical forced liquidation** (prop-account trailing-DD auto-liquidation, margin calls; a population genuinely concentrated in CME micros) | Accounts liquidated **by rule**, not by choice | **CANNOT BE WRITTEN.** Every mechanical rule in that population is **account-equity-triggered**: it determines *whether* a position closes, never *where*. The entire price content of §1's level menu comes from the assumption that these traders *choose* to place stops at prior-session extremes — which is preference. Swapping "retail with stops" for "accounts under mechanical liquidation" changes the vocabulary and not the load-bearing content. That substitution **is** the §5 laundering move |
| **2 — overnight inventory rebalancing at the RTH open** | Globex-session liquidity providers rebalancing at the scheduled deep-liquidity moment | **PARTIALLY WRITEABLE — and the stronger claim.** Its constraint is *not* vocabulary on nothing: this repo **measured** it (H-OD-1, ES, **+1.444 bp** vs SR917's declared +1.5 bp, t≈5.0, 9/9 IS years positive). But the constraint predicts **sign-agnostic transient displacement plus reversion**; every element converting that into "buy the 1-minute reclaim of the nearest level below the open, gated on two bullish EMA(20) relations, stop at sweep extreme, target +1.5R" is a **price-pattern** decision with zero constraint backing |

**The two decisive tests, which both framings fail:**
- **DELETE test** — remove the constraint paragraph entirely. Does any §1 rule change? **No.**
- **FLIP test** — assert the constraint runs the *other* way (overnight inventory was net short, so the class must **buy** at 09:30). Does the trade change? **No** — SLR-MYM still only buys reclaims.

A warrant whose truth value cannot touch the trade rule is not doing mechanism work; it is post-hoc justification. **Path 1a cannot be written for this construct.**

**Prior art the first draft missed** (surfaced by the mandatory by-mechanism-family dedup, executed this pass): framing 2's family has been tested **twice** in this repo — `CONCEPT-NOCT-SPX-001` "nocturnal inventory-reversal harvest" (**FALSIFIED 2026-06-07**, registry `mechanism_family=inventory-reversal-immediacy-premium`; the conditional channel did not separate from unconditional drift) and **H-OD-1** (mechanism confirmed, killed at Stage-2 cost-law, 1.5 bp vs a 5.05 bp hurdle). Borrowing H-OD-1's 1.444 bp to MYM is a **cross-instrument transplant**, which harvest Req 2 forbids outright.

**Correction to this section's own first draft (Req 2).** §2.6 originally graded Requirement 2 "not satisfied" and §6 carried it as a kill conjunct. **That is wrong and is withdrawn:** harvest doctrine routes a *missing* per-instrument δ to a **δ-extraction probe** (`UNSCREENABLE → probe`), and names **Req 3 as the only permanent kill**. The relief route is measured on this exact instrument at **$0.00 and K=0** (MYM-3FPS-1 discharged an identical Req-2 gap via a native `MYM.v.0` minute extraction). **Requirement 1 is the gap, not Requirement 2** — and since the probe is gated behind Req 1 clearing, nothing is loosened by the correction.

**Disposition:** (i) is unavailable — Path 1a cannot be written. (ii) Path 1b remains theoretically open but nothing in the repo's own funded 13-family literature sweep supplies it (the one family-adjacent row is rank-6 practitioner, undated, unverified: **0 of 4** required limbs). (iii) **Close at zero K and zero spend** is the honest disposition on this limb — and it is moot in any case, because Stage 0-C (§2.5) fires independently on arithmetic.

**If the operator wants ruling A to stand regardless**, exactly one instrument carries it honestly: a **recorded §2-A override** — admitted *as an override*, not as "§2-A satisfied" — so the ADR's own falsifier keeps counting. Silently recording it as satisfied would corrupt the ledger the ADR exists to protect.

### §2.7 — The domain raised bar, scored against its actual three-route test — Stage-0 ruling B

The first draft cited this bar via MYM.md's `bars:` id and paraphrased its addback condition from a different artifact's wording. **Corrected: the governing text is `docs/rejected_candidates.md:411-436`**, a *tail-exhaustion raised bar* (explicitly **not** a SNAG closure), whose test is a **three-route disjunction — a new candidate is not admitted for a full Pre-Q unless it clears ONE of**:

| Route | SLR-MYM | Assessment |
|---|---|---|
| **1.** Mechanism **outside the mapped cost-ratio-lever set** {price, instrument-selection, hold-time} | Sweep-reclaim is an **entry-trigger** mechanism; it is not a re-tune of price basis, not an instrument swap, not a hold-time change | **The strongest available route.** Argued, not asserted — a reviewer may reply that "a different entry trigger on the same OHLCV" is precisely the same-space mining the bar exists to slow |
| **2.** Different **modality** or a **venue** relaxing a binding wall | SLR-MYM uses **OHLCV alone** — no new modality. The 1m-resolution/databento point is a *data-access* change, not a modality change | **FAIL** — and the 2026-07-28 M2K ruling explicitly refused "new modality" claims lacking a cohort-cited δ |
| **3.** Beats incumbent **ORB-MNQ net-of-cost** | Unmeasured; would require running the campaign first | **Not available pre-pull** |

**Honest reading:** the bar's scope line — "*directional intraday timing* … from **OHLCV structure alone**, deployable **flat-by-close**" — describes SLR-MYM exactly. Admission rests **entirely on route 1**.

### §2.7.1 — Ruling B executed (2026-07-29): GRANTED, and it blocks nothing

The operator questioned the three-route disjunction. Adjudicated against source:

- **The brief did not mis-state the bar.** It *is* literally a three-route disjunction ("unless it clears **one of**: 1 … OR 2 … OR 3"), operator-ratified 2026-07-21, and SLR-MYM *is* literally inside its stated scope. No "out of scope" defence is available and none should be invented.
- **But the scepticism is well-founded on a different and provable axis: the bar's SCOPE is broader than its EVIDENCE.** Its declared basis is four momentum/continuation/selection closures (D5, D5-RECOST, H-TSMOM-1, cross-index-RV) plus a *continuation* survivor, and the originating audit contains **zero** occurrences of "mean-reversion", "reversal", or "fade". **Route 1 exists precisely for a mechanism the evidence never examined**, and the repo's own same-week ZF calibration says a mean-reversion/fade construct "is not barred by this note."
- **Reductio confirming route 1 clears:** reading route 1 to exclude every OHLCV price construct would empty it for a domain *defined* as OHLCV-only — converting a formally **declined** SNAG ("Requested closure DECLINED") into a de facto SNAG. The bar also expressly preserves the *session-confluence longer-hold* thread, which is a **mapped-lever** thread — proving the levers are not a topical exclusion.

**Ruling: route 1 clears; the bar does not bar SLR-MYM.** And the practical consequence is nil — the bar is a **ledger-layer gate that the ratified third-leg screen never imports**, and it has never been dispositive for any candidate. **Grant B in full and the brief still dies**, at 0-C on arithmetic and at 0-A on admissibility. If the operator nevertheless wants the bar's text amended, the instrument is a **dated amendment at the already-scheduled 2026-08-08 slate**, mirrored as an addendum to the 2026-07-21 audit — **not** an ADR (no ADR created it) and not a brief-level reinterpretation.

**Separate ledger defect found, not this brief's to fix:** two materially different texts of this bar id circulate, and the one the tooling surfaces carries an impossible provenance; a sibling brief (WSTRUCT-M2K-1) has been adjudicated against the wrong text and has never seen the three routes. Worth its own correction pass. Relatedly, **§2.2's attribution of the bar's origin to OPENPRESS-1 is false at source** and is corrected there.

---

## §3 — Question

**Q-SLR-MYM-1:** the one never-verdicted layer of the ICT cascade (1-minute raid→reversal execution) closed partly on a data wall that no longer exists, and the one component that survived (weekly structure) has never been carried into a new entry expression on a live c1 instrument — but the mechanism's own story is a stop-run narrative that the current admission rules name inadmissible on its default path, and the design as first written fails the venue's day-of-week capacity screen on the same ground as the last candidate that reached a frozen-engine run; so is this construct admissible at all, and if admitted, does it clear the ratified third-leg screen on MYM?

---

## §4 — Falsifiable hypothesis (H-SLR-MYM-1)

**H-SLR-MYM-1:** if Stage-0 rulings A (admissibility), B (raised bar), and C (day set) all clear, and the census projects **N ≥ 120 entries on the declared IS partition** (not the full panel — see §6), then the frozen SLR-MYM expression of §1 clears **T1** (gross edge ≥ **$11.28/contract/RT** at the IS panel's own price basis — the 4× cost law applied **once**), the MYM-family **DSR floor 0.85** at `K_eff=2`, **Clause-N power ≥ 0.50** at realized IS N, the **both-halves** regime gate, and composes on the frozen engine at bust ≤3.0% on all four partitions under the **corrected (unreachable-offset)** eval geometry at a **declared lifecycle weight** — in which case it is a screenable third-leg candidate; otherwise it closes at whichever gate fires first.

**Falsifier — H-SLR-MYM-1 is FALSIFIED if any one of:** Stage-0 ruling A closes it on admissibility · OR ruling B rules the raised bar binding · OR no day set satisfying S5 also reaches the N floor (ruling C) · OR projected IS N < 120 · OR gross edge < $11.28/contract/RT · OR realized annSR < 0.85 at `K_eff=2` · OR Clause-N power < 0.50 at realized IS N · OR either regime half fails · OR composed bust > 3.0% on any of the four partitions. **A single failed limb is decisive; no partial credit accrues.**

**Accept if:** all clear **and** R1/R2/R3 hold at the declared weight **and** the composed re-MC passes on both `trailing_locking` tiers.

**Ambiguous-hold if:** a Stage-0 ruling is deferred rather than decided, or the panel cannot support a clean IS/holdout split at the required N — re-test: next operator session, **no scope widening**.

---

## §5 — Forbidden moves

- **Adding the FVG-entry arm.** `pharos_us500_sweepfvg` already tested sweep→FVG as a trade: real but non-robust (drop-top-3 −0.152R). `K_intrinsic` is **1**, not 2, for this reason.
- **Self-clearing Stage-0 rulings A, B, or C.** Each is argued both ways and routed to the operator. Arguing only the favorable side is the failure the M2K ruling names.
- **Treating "MYM futures ≠ SPX500 CFD" as clearing the raised bar.** Instrument novelty alone does not clear it (2026-07-28 M2K precedent).
- **Citing the D-layer SSL FVG rate (0.795) as support for the pivot-class level menu.** Different object class — the class the D-layer falsified — and a 10-day clock, not 30 minutes.
- **Re-importing MYM.md's 6.57 bp as the gate, or multiplying it by 4.** It is already the 4× figure and it is on a foreign panel's price basis (§2.3).
- **Re-tuning any §1 constant after Phase 0.5 or Phase 1 numbers are seen** — EMA period, ATR multiples (reachability 1.0×, buffer 0.10×, stop cap 0.50×), the 10:00/10:15 deadlines, the 1.5R target, the 13:00 flat, or the day set once ruled. All are frozen pre-data; a change is a **new campaign**.
- **Choosing the day set to maximize N after seeing per-day entry rates.** Ruling C must be decided on **cap availability and uniform-size** grounds (§2.5), with the N consequence *disclosed*; picking days by yield is the fitted-calendar move M1 exists to kill.
- **Resolving intrabar stop-vs-target ordering favorably**, or assuming limit-fill-at-touch on 1m bars. §1 declares stop-first; changing it inflates results.
- **Reporting a news-day or day-of-week sub-cut as a filter.** Diagnostics only.
- **Skipping any Stage-0 ruling to save a session.** They are free and each can kill for $0.
- **Composing into the c1 book before Phase 4** (Q-COMPOSE-1; spec §5 no weight iteration).
- **Outcome-conditional D-tests** — categorically forbidden.

---

## §6 — Gate criteria

| Stage | Trigger | Disposition | **Executed 2026-07-29** |
|---|---|---|---|
| **0-A admissibility** | Cannot name a constraint-based WHO for Path 1a **and** will not fund a Path-1b evidence pass. *(The Req-2 conjunct is **removed** — a missing per-instrument δ routes to a $0/K=0 extraction probe, not a kill; Req 3 is the only permanent kill. See §2.6.1.)* | `FALSIFIED (as scoped)` — $0, zero K | **FIRED** — both framings fail the delete/flip tests (§2.6.1). Operator may override, but only as a *recorded* §2-A override |
| **0-B raised bar** | Operator rules the bar binding (route 1 rejected) | `FALSIFIED (as scoped)` — $0, zero K | **NOT fired** — route 1 clears (§2.7.1); and the bar blocks nothing regardless |
| **0-C day set / S5+S3** | No day set both satisfies S5 (no Tuesday requirement) **and S3 (no order-symbol collision with the incumbent MYM leg)** and projects IS N ≥ 120 | `FALSIFIED` — the venue cannot host the mechanism at demonstrable power | **FIRED** — best compliant set (Mon+Wed+Thu) = **81 IS entries** vs a 120 floor, on an *upper-bound* proxy (§2.5, §7 Phase 0.5) |
| **0-D §7.1 screen** | Any of S1–S6 fails after ruling C, **or** S3 same-symbol netting is verified to preclude an independent second MYM position | `SCREEN-FAIL` — no pull, $0, zero K | **S3 is the binding limb** and closes Tue+Fri structurally (§2.5). Verification against the CrossTrade/Tradovate netting layer is owed before any successor proposal |
| **0-E K disclosure** | The `S-MYM-ORC-02` K=2 claim (§0.1) is ruled bankable ⇒ MYM bank 3 ⇒ floor 1.06 > Cap | `FALSIFIED (FAIL-K)` — $0 | not reached |
| **1 census** | Projected **IS-partition** N < 120 entries on the ruled day set | `FALSIFIED` |
| **2 frozen IS** | Gross edge < **$11.28/contract/RT** at the IS price basis (4× applied **once**), OR either regime half fails, OR either half has < 40 entries | `FALSIFIED` |
| **3 confirm** | Clause-N power < 0.50 at realized IS N, OR realized annSR < 0.850 | `FALSIFIED` |
| **3 holdout** | Single 2024+ read; survive-or-close, no iteration | — |
| **4 survivor** | Standalone or composed bust > 3.0% on any of the four partitions, either `trailing_locking` tier, under corrected (unreachable-offset) geometry **at the declared lifecycle weight** — noting the book alone is already **4.74%** at 1.00×, so the weight basis must be declared with the run or the gate is unreadable | `FALSIFIED` |
| **4 pass** | All partitions ≤3.0%, both tiers | `RESOLVED` — screenable candidate; fires the third-leg spec's §6.1 verdict and supplies its third σ→bust calibration point |
| **any** | Panel/holdout cannot be constructed at required N | `AMBIGUOUS-HOLD` — no scope widening |

**N-basis note (the first draft's error).** Stage 1 previously killed on *full-panel* N while Stage 3 evaluates power at *realized IS* N; IS (2019–2023) is ~64% of the panel, so a candidate could clear Stage 1 and be arithmetically guaranteed to fail Stage 3 — after a paid pull. **Both are now stated on the IS partition.**

**Pre-registered before any OHLC touches Phase 1.** Amending this table mid-campaign to match emerging numbers is methodology-layer p-hacking (Trap #12).

---

## §7 — Execution plan

- **Phase 0 — Stage-0 rulings (free, operator).** A (§2.6 admissibility), B (§2.7 raised bar), C (§2.5 day set), D (S1–S6 incl. **verifying S3 rail attribution** against `ops/c1_rail/c1_sizing_host_reference.py`), E (§0.1 K disclosure). Also: re-run §10 hooks; confirm no new MYM DEAD entry since 2026-07-25.
- **Phase 0.5 — FREE event-rate bound. EXECUTED 2026-07-29.** Run on `core/data/bar_data/MYM_M15.csv` (n=141,477, 2020-07-23→2026-07-02, primary checkout; vendor data gitignored so absent from worktrees). Harness: `scratchpad/phase05_census.py`. **Zero outcomes examined — entry counts only, zero K, $0.**

  **Result — 1,481 scoreable RTH sessions, IS (≤2023-12-31) = 860 (58.1%):**

  | Cumulative filter | rate | n |
  |---|---|---|
  | weekly + daily `vStruct` bullish | 56.38% | 835 |
  | + a level below the open | 56.38% | 835 |
  | + within 1×ATR | 55.64% | 824 |
  | + swept | 34.71% | 514 |
  | + reclaimed = **ENTRY** | **17.96%** | **266** |

  Full-panel entry rate **17.96%** (266 entries); **IS-partition 16.63% (143 entries)**. Per-day and per-day-set breakdowns are in §2.5. **The brief's own feared kill is refuted** — the mechanism fires often enough in the abstract. What kills it is that the S5- and S3-compliant day set retains only **81** of those IS entries.

  **Two honesty notes.** (i) This is a **15m proxy, not a measurement of the 1m mechanism** — a 15m bar cannot resolve a sweep and reclaim inside itself. (ii) The proxy is deliberately **loose in the permissive direction**: it counts a sweep at *any* time of day, where §1 requires the sweep inside 09:30–10:00 and the reclaim by 10:15. So these are **upper bounds**, real 1-minute counts are lower, and a day set below the floor here **cannot** clear it on real data. Phase 0.5 **does not discharge Phase 1** — but a failing upper bound does discharge the *need* for Phase 1.
- **Phase 1 — Census on 1m.** databento cost dry-run first (mandatory, `--max-cost`, no `--force`). Pull MYM 1m, 2019-05→present, `MYM.v.0`; drop UTC-bucketed weekend bars (W1/W2). Derive RTH daily/weekly per §1. Compute the entry-rate product **from bars only — zero outcomes, zero K**. Kill: IS N < 120 on the ruled day set.
- **Phase 2 — Frozen IS run.** IS 2019–2023; holdout 2024+ reserved as a code property. Headline expression only (`K_intrinsic=1`). T1 via `cost_model.py::bp_hurdle()` at the IS median price. Expectancy from the **realized three-outcome distribution**. Both-halves regime gate with a ≥40-entry-per-half floor. MFE/MAE and news-day diagnostics reported, never filtered.
- **Phase 3 — Confirm.** Clause-N power at realized IS N *before* the holdout opens; DSR vs 0.85 at `K_eff=2`; single holdout read.
- **Phase 4 — Survivor scoring + composition.** Standalone and composed Part A, corrected geometry, declared weight, both tiers, all four partitions.
- **Phase 5 — Productionalize.** Pine edition, hash pin, lock anchor, rail-slot (or rail-redesign) ADR. Out of scope; separate GO.

---

## §8 — Pre-registration deliverables (before Phase 1)

Not yet due — Stage 0 must clear first. Once ratified, `docs/briefs/pre-registration/SLR-MYM-1-verdict-preregistration.md` must carry **all** of:

1. `register_search open --tool <t> --search-space-size 1` binding **`K_intrinsic = 1`**.
2. **`--profile-cell MYM:<mechanism-id>`** — requires a `MECHANISMS.md` vocabulary entry landing **in the same commit** (the nearest existing class, `ict-liquidity`, is recorded **DEAD on SPX500**; a `NEW` class is likely the honest declaration).
3. **`--profile-consult <saved output>`** — the instrument-profile consult, pasted.
4. **`--reachability-attestation`** — the **§R gate-reachability simulation of EVERY bundled clause**, per-gate, in that gate's own units, at the basis the gate scores on (ADR 2026-07-13 §4.4; ADR 2026-07-16 §2.1–2.3). **This is a HARD gate and its absence from the first draft is exactly the defect class it exists to catch** — the double-4×, the N-basis mismatch, and the undeclared Stage-4 weight basis are all §R-shaped failures that `check_brief.py` passed 6/6 without noticing.
5. The §6 thresholds verbatim, plus the ruled day set and the holiday early-close rule.
6. A **faithfulness/fidelity gate** for the offline harness against a source-of-truth artifact (ST-EH-1's convention is borrowed by name in §7; its HALT-gated fidelity gate must be borrowed with it).

---

## §9 — Closure record format

- `RESOLVED` → `docs/briefs/closures/SLR-MYM-1-closure-resolved.md` + `recommendation.md`
- `FALSIFIED` → `docs/briefs/closures/SLR-MYM-1-closure-falsified-<stage>.md`; append to `ops/instruments/MYM.md` DEAD list + session log, and to `docs/rejected_candidates.md` if the *mechanism* failed rather than this expression
- `AMBIGUOUS-HOLD` → `docs/briefs/closures/SLR-MYM-1-closure-ambiguous.md` with an explicit re-test trigger
- Update `lab/CATALOG.md` (the authoritative surface for `scripts/check_status_consistency.py`) alongside the ledger and registry

Every closure states: verdict, anchor numbers vs §6 thresholds, what §4 predicted vs what happened, lesson candidates with a dated/dollar anchor.

---

## §10 — Audit hooks (runnable; corrected — the first draft shipped two that did not fire)

```bash
# §0.1 K ledger (expect MYM bank 1 / MNQ bank 2; one manifest commit since 07-26)
python -c "import json,glob;[print(json.load(open(f))['run_id'], json.load(open(f))['status'], json.load(open(f))['K']) for f in glob.glob('discovery_manifests/*.json')]"
git log --oneline --since=2026-07-26 -- discovery_manifests/

# §0.1 the unreconciled MYM K claim must still be a disclosure, not a silent contradiction
# NOTE (Trap M-AHF): the ledger stores this with markdown bold -- "K bank remains **0**" -- so a
# literal "K bank remains 0" grep returns 0 hits and exits 1. Match form-agnostically.
grep -nE "K bank remains \*{0,2}0" ops/instruments/MYM.md
grep -n "S-MYM-ORC-02" ops/instruments/MYM.md | head -3

# §2.7 the raised bar's THREE-ROUTE test must still read as three routes (not the paraphrase)
sed -n '411,436p' docs/rejected_candidates.md | grep -n "outside the mapped cost-ratio-lever set\|different modality\|beats the incumbent"

# §2.6 the Req-1a blocker must still name behavioral stories inadmissible
grep -n "stops get hunted" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md

# §2.3 6.57 must still be labelled as ALREADY 4x (if this wording changes, re-derive T1)
grep -n "4× Tradeify hurdle" ops/instruments/MYM.md

# §2.1 W verdict scope + the leg-(b) limit this brief must not overclaim past
grep -n "weekly-close structure-only hit-rate" lab/archive/ict_cascade_2026-06-18/PREREG-W.md
grep -n "leg (a) only" lab/archive/ict_cascade_2026-06-18/PREREG-W.md

# §2.1 pharos verdict (guards the FVG-arm forbidden move)
grep -n "FALSIFIED\|drop-top-3" lab/archive/pharos_us500_sweepfvg/README.md

# §2.5 S5 — cap split still 69/11 inside an aggregate 80, and Tuesday still closed
grep -n "69/11" ops/c1_rail/c1_sizing_host_reference.py
grep -n "Tuesday is closed" docs/spec/2026-07-27-third-leg-target-spec.md

# §7 Phase 0.5 — the free local panel (primary checkout only; absent from worktrees)
ls -la ../../../core/data/bar_data/MYM_M15.csv 2>/dev/null || ls -la core/data/bar_data/MYM_M15.csv 2>/dev/null || echo "not in this checkout - run Phase 0.5 from the primary repo"

# §8 the three HARD gates on a mechanism-first open
grep -n "profile-cell\|profile-consult\|reachability-attestation" lab/discovery/register_search.py | head -6

# §6 Stage 4 — the eval-geometry open defect must still be unfixed (else re-read the gate)
grep -n "dd_lock_offset_usd" core/firm_rules.py | head -2
```

---

## §11 — Revision record

**2026-07-29 — Stage-0 executed after a 12-agent ruling-discharge workflow.** Operator issued rulings A/B/C; discharging them fired two independent kills, both at $0 and zero K.

- **A (admissible) — could NOT be discharged as stated.** Two constraint framings written to §2-A's standard, each attacked by independent skeptics; both fail the **delete test** and the **flip test** (§2.6.1). The operator's *ground* is correct — framing 2 names an effect this repo measured (H-OD-1, +1.444 bp on ES) — but §2-A tests constraint-selects-the-trade, not sophistication. Dedup also surfaced two prior in-repo tests of framing 2's family the brief had not cited (`CONCEPT-NOCT-SPX-001` FALSIFIED 2026-06-07; H-OD-1 cost-law kill).
- **B (three-route disjunction) — GRANTED, and moot.** The bar *is* verbatim a three-route disjunction and SLR-MYM *is* in its scope — but its scope is broader than its evidence (the originating audit contains zero occurrences of "mean-reversion"/"reversal"/"fade"), so **route 1 clears** (§2.7.1). It blocks nothing regardless: the ratified third-leg screen never imports it. Amendment instrument, if wanted: the 2026-08-08 slate, not an ADR.
- **C (day set + cap) — FIRED.** Executed as a measured census (§7 Phase 0.5). A second structural constraint the first draft missed — **S3 order-symbol occupancy**, since both legs resolve to `MYM1!` and the venue nets one position per symbol — closes **Friday as well as Tuesday**. Best compliant set **Mon+Wed+Thu = 81 IS entries vs a 120 floor**, on an upper-bound proxy. The cap rider cannot rescue it (the obstruction is symbol, not cap), is procedurally owned elsewhere (spec §5), and its criterion is inverted (pass rate is `1 − P(bust)`; Q-COMPOSE-1 raised bust 2.65%→38.75% by adding a *profitable* leg).
- **Req-2 correction:** removed as a Stage 0-A kill conjunct — a missing per-instrument δ routes to a $0/K=0 probe, not a kill; Req 3 is the only permanent kill.
- **§2.2 correction:** OPENPRESS-1 is not the origin of the §2.7 domain bar (false at source).
- **Flagged, not fixed here:** two materially different texts of the same bar id circulate in the ledger, and a sibling brief has been adjudicated against the wrong one.

**Recommended disposition: `FALSIFIED (as scoped)` at Stage 0-C, $0 spent, zero K consumed, MYM family bank unchanged at 1.** Operator owns the disposition.

**2026-07-28 — revised after a 14-agent adversarial review** (12 lenses: 5 citation-verification clusters + 7 attack lenses; plus a completeness critic and a synthesizer that adjudicated conflicts by re-reading source). 80 raw findings, 14 BLOCKER / 39 MAJOR pre-dedup; 24 ranked patches after dedup and discard. Applied here.

**What the review changed, materially:**

1. **Added §2.5** — the S1–S6 screen the first draft claimed to apply but never scored. **S5 FAILS as first written** (requires Tuesday, 0 free cap) — verbatim ORB-MNQ's failure, the one the brief opens by saying it must not repeat.
2. **Added §2.6** — ADR 2026-07-26 **§2-A** closes Path 1a for a stop-run story. The first draft cited §2-C of the same ADR and never read §2-A. This is now the **most likely kill**.
3. **Rewrote §2.7** — the raised bar's real test is a **three-route disjunction**, not the paraphrase the first draft used. Admission rests entirely on route 1.
4. **Fixed a real arithmetic error** — `6.57 bp` is *already* the 4× hurdle; §4/§6 were double-applying it (16× RT). Also: the pin is on a **foreign panel's price basis** and is **loose** here, so T1 is restated in $/contract/RT.
5. **Fixed the N-basis mismatch** — Stage 1 killed on full-panel N while Stage 3 scores IS N (~64% of panel); a candidate could clear Stage 1 and be *guaranteed* to fail Stage 3 after a paid pull.
6. **§1 now declares** non-repaint bases, RTH-vs-ETH, gap-through-level, same-bar sweep+reclaim, first-sweep-only, ties, intrabar stop-vs-target ordering (**stop first**), and a **0.50×ATR stop cap** — replacing the first draft's false claim that the 1-ATR reachability cap bounded the stop.
7. **Withdrew two overclaims** — that vStruct is used "exactly as its closure licensed" (PREREG-W fixes **leg (a) only**), and that the 1M layer closed on a data wall alone (it closed on **two** grounds; databento removes one).
8. **Corrected the §0 divergent-citation chronology** — the first draft's "unpushed branch" explanation is wrong on git and is withdrawn.
9. **Added §8's four missing pre-registration deliverables**, incl. the **HARD §R reachability attestation** — whose absence is itself the defect class it exists to catch, and which both `check_brief.py` gates passed 6/6 without noticing.
10. **Added a free Phase 0.5** — a local 15m panel bounds the event rate at $0 before any pull, and it **refuted the brief's own stated worry**: measured 13.2%/session, N≈238 full-panel, well above the 120 floor. The binding constraint is not event rate; it is **Tuesday carrying 23% of entries against 0 free cap**.

**Discarded by the synthesizer as unfounded** (recorded so they are not re-raised): a claimed Tradeify ">50% of trades held >10s" minimum-hold rule (**no such rule exists in this repo** — the 10s figures are Tradeify's *hedging-detection* threshold and a different firm's ToS); the claim that MYM's family bank should be 3 (kept only as the §0.1 disclosure); and an R5 mis-attribution.

---

## Verification

```bash
python scripts/check_brief.py docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md --type inquire
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/rnd-pipeline/SLR-MYM-1-liquidity-sweep-reclaim-scoping.md --type inquire

# §0 anchors resolve
for f in docs/spec/2026-07-27-third-leg-target-spec.md core/firm_rules.py \
         docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md \
         docs/rejected_candidates.md ops/instruments/MYM.md lab/discovery/cost_model.py; do
  git log -1 --format="%h %ci $f" -- "$f"; done

# Figures cited verbatim
grep -n "0.5571\|emaLen = 20" lab/archive/ict_cascade_2026-06-18/PREREG-W.md
grep -n "MYM bank 1\|floor 0.85" docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md
```

**Discipline checklist:** §0 anchored ✓ · S1–S6 actually scored, not claimed (§2.5) ✓ · admissibility blocker surfaced rather than omitted (§2.6) ✓ · raised bar scored against its real three-route test (§2.7) ✓ · cost law applied once, in the right units, on the right panel (§2.3) ✓ · N basis consistent across Stage 1 and Stage 3 (§6) ✓ · every §1 ambiguity resolved so the implementer guesses nothing (§1) ✓ · overclaims withdrawn and named (§2.1, §0.1) ✓ · §5 moves genuinely tempting ✓ · §6 binary per stage ✓ · §10 hooks re-run and the two broken ones fixed ✓ · three Stage-0 rulings routed to the operator, none self-cleared ✓.

---

## Pre-Lock Checklist (DRAFT brief only)

- [x] §0 paths read and anchored
- [x] §3 question passes the symptom-only rephrase test
- [x] §4 hypothesis falsifiable with binary §6 triggers
- [x] §5 forbidden moves genuinely tempting
- [x] §6 gates have specific numerical triggers on consistent bases
- [x] §10 audit hooks runnable (re-run this session)
- [ ] **Stage-0 rulings A / B / C / D / E — OWED, operator**
- [ ] §8 pre-registration (incl. §R attestation) — not due until Stage 0 clears
