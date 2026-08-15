# Pre-registration — Guardian→MGC transfer cell (R7 / b8) N-SURV gate

> **Ordering honesty (load-bearing):** this artifact is **retroactive**. The v0.1–v0.3
> execution-mechanics port, the native MGC1! panels, and the exploratory N-SURV score
> (full 42.2% / H1 72.4% / H2 16.5% bust) were all produced **before** this pre-registration
> was authored. It freezes the claim that *was* under test and the floors that *were*
> applied — it does **not** pretend a pre-commitment existed before the numbers. Closure
> cites this body as the cell PREREG of record under Q-TXG-1 §5 shape; treat every
> numeric claim as post-measurement ratification, not pre-data freeze.

**Status:** `CLOSED — DEAD(N-SURV)` (operator-directed cell closure 2026-08-11; body frozen
as historical record — do not amend floors in place; Known Trap #12). Closure:
[`docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](../closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md).
**Prior status:** never `FROZEN` before measurement — see ordering note above.
**Scope:** one transfer cell — Guardian (locked XAU trend, v5.5) × MGC (COMEX micro gold)
at the incumbent eval environment (`Tradeify_Select_100K`). Port mapping =
execution-mechanics only. Survival gate = frozen 2026-07-13 N-SURV thresholds via
`lab/research_utils/nsurv_channel.py`.
**Candidate class:** Class-S / venue-transfer reconstruction (same-underlying metals
re-expression). **Not** a locked-parameter search; **not** a Q-TXG-1 Block-1 grid compile
or Block-2 election (those remain the grid's own process).
**Gate of record:** [`2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md)
(FROZEN 2026-07-13) — Part A **bust ≤ 3.0%** ∧ **P(pass) ≥ 50%**, both-halves regime split.
**Loop of record:** STRATEGIC (pursuit b8 / R7).
**Authored:** 2026-08-11 · Cursor (operator-directed: retroactive cell PREREG + DEAD closure).
**Spend:** K=1 declared for the cell score (panel of record already landed); $0 new spend
on this authoring pass.

---

## §0 — Rule-0 reads (verified this authoring session 2026-08-11)

Per-file anchors (`git log -1 --format='%h %ci'` against worktree HEAD `68fa67f`, plus
working-tree CARD bodies landed this session's measurement pass):

- **[`docs/pursuits/b8-guardian-mgc-transfer-lane.md`](../../pursuits/b8-guardian-mgc-transfer-lane.md) @ `dda516c` + working-tree Residuals** —
  RATIFIED PARK; N-SURV FAIL table (42.2 / 72.4 / 16.5) + two exploratory caveats named;
  pre-reg limb owed (this artifact discharges it).
- **`core/strategies/guardian/guardian_gold_futures_mgc_v0_{1,2,3}_CARD.md` (working tree)** —
  port mapping record: F1–F3 sizing/commission (`syminfo.pointvalue`, cap, `Tradeify_Select_100K`
  initial capital); F4 venue-mandatory EOD force-flat; F5 CME-maintenance-halt fill-lag
  (cutoff 16:15 ET → fill ~16:30). Every CARD states locked parameters remain
  byte-identical to v5.5 (values redacted from the public tree 2026-08-14 — see the
  private archive). Hash pins in each CARD + `PORT_MANIFEST.sha256`.
- **[`core/strategies/guardian/guardian_gold_v5.5_CARD.md`](../../../core/strategies/guardian/guardian_gold_v5.5_CARD.md)** —
  locked Guardian identity the port must not touch.
- **[`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `91137fb`** —
  frozen N-SURV floors; nothing here re-decides them.
- **`lab/research_utils/nsurv_channel.py` @ `765390b`** — W1-pin-proven scoring channel;
  intended `intraday_low` = bar-level daily equity troughs.
- **[`docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md`](../../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) @ `5fe755e`** —
  Q-TXG-1 §5 Phase-B cell PREREG shape this body follows; §7 forbidden locked-parameter edits.
- **[`ops/instruments/6J.md`](../../../ops/instruments/6J.md) @ `45e3cea`** — J4b precedent:
  "PARKED stands, now on a measured basis" at true Tradeify geometry (best cell 3.88% vs
  3.0% — 1.3× over). Same failure class; this cell's margin is larger.
- **[`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](../../adr/2026-07-10-r6-nogo-futures-residual-disposition.md)** —
  R7 origin (Guardian-MGC parked as data-blocked, not adversely resolved — that clause is
  what this measurement retires).
- **[`docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md`](../../adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md)** —
  self-funded lane close; Guardian-MGC remained PARKED.

**Bar-derived re-run check (authoring gate):** `rg` / directory census over `lab/analysis/`
for Guardian-MGC-shaped N-SURV after 2026-08-11 → **none**. Exploratory AE-approximated
numbers remain the measurement of record.

---

## §1 — Context

R7 (Guardian→MGC) was parked under R6 because the granularity-floor work was
**data-blocked**, not falsified. A 2026-08-11 native MGC1! port cleared the bar-export
limb (v0.1–v0.3 prototypes + panels) and scored N-SURV against the incumbent eval. The
score failed every partition by a wide margin. This PREREG records the port mapping rule
and the survival floor so the DEAD disposition is attributable to a named gate, not an
ad-hoc read — even though the freeze arrives after the score (see header).

Standing doctrine: parameter axis LOCKED
([lifecycle ADR](../../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md));
transfer = declared venue mapping only (Q-TXG-1 §7); N-SURV floors frozen 2026-07-13.

---

## §2 — Frozen protocol (what was scored)

### §2.1 Port mapping rule (execution-mechanics only)

| Layer | Fixed |
|---|---|
| Signal / risk identity | Guardian Gold v5.5 — locked parameters **byte-identical** (values redacted from the public tree, see the private archive) |
| Instrument | CME/COMEX `MGC1!` (micro gold) |
| Sizing / cost (F1–F3) | `syminfo.pointvalue` division, commission, contract-count cap, `initial_capital` = Tradeify Select 100K — see v0.1 CARD |
| Venue hold (F4) | EOD force-flat (FRIENDLY firms auto-liquidate daily); no re-entry-on-continuation mechanic — see v0.2 CARD |
| Fill clock (F5) | `flatMinuteET` 15 → signal 16:15 ET / fill ~16:30 ET (CME 17:00–18:00 ET maintenance halt) — see v0.3 CARD |
| Panel of record | v0.3 native TV trade-list (N=329 trades; daily-aggregated n=276 days for N-SURV) |

### §2.2 Survival floor under test

| Item | Frozen value | Owner |
|---|---|---|
| Channel | `lab/research_utils/nsurv_channel.py` | W1-pin-proven |
| Tier | `Tradeify_Select_100K` | S1 / firm_rules |
| Bust ceiling | ≤ **3.0%** | 2026-07-13 prereg |
| Pass floor | ≥ **50%** | 2026-07-13 prereg |
| Regime | both-halves must clear | regime_robustness_gate / Q-TXG-1 H_B |

### §2.3 Disclosed measurement caveats (not floors)

These do **not** loosen §2.2. They bound epistemic grade:

1. Half-boundary **2024-07-02** = midpoint-by-day-count split — **not** a pre-registered regime date.
2. `intraday_low` approximated from each trade's Adverse-Excursion (attributed to entry date), **not** genuine bar-level daily equity troughs (the channel's intended input; W1 used bars).

---

## §4 — Falsifiable hypothesis

**Hypothesis (H-GMGC-SURV):** the execution-mechanics-only Guardian→MGC port, at locked v5.5 risk identity
and true Tradeify Select 100K geometry, clears N-SURV (bust ≤ 3.0% ∧ P(pass) ≥ 50%) on the
full panel **and** both regime halves.

**Falsifier — Reject H-GMGC-SURV if:** any scored partition busts **> 3.0%**, or any partition's
P(pass) **< 50%**, under the §2.2 channel/tier. (Q-TXG-1 H_B cell FAIL → `DEAD(N-SURV)`.)

**Accept H-GMGC-SURV if:** full + both halves clear §2.2 on a **bar-derived** `intraday_low`
panel (exploratory AE approximation alone cannot mint CANDIDATE).

**Ambiguous if:** bust in (3.0%, 3.2%] noise band on the binding partition with bar-derived
inputs — not reached here.

---

## §5 — Forbidden moves

- **Re-tune locked Guardian parameters** (EMA/ATR multiples/SL/TP/risk%/session/day/pyramid)
  to chase an N-SURV pass — that is re-optimization, not transfer (Q-TXG-1 §7; lifecycle
  parameter axis).
- **Amend the 3.0% / 50% floors** after seeing the 42.2/72.4/16.5 numbers (Trap #12).
- **Treat the AE-approximated `intraday_low` run as decision-grade CANDIDATE evidence**
  even if it had passed — the caveats are directional for FAIL (margin) and disqualifying
  for PASS.
- **Silently claim a Q-TXG-1 Block-2 cell election** — this PREREG closes a measured cell;
  it does not elect the next grid cell or compile the 4×7 grid.
- **Widen to a parameter grid (K>1) inside the cell** — cell is K=1; any new axis is a
  fresh PREREG + K charge.
- **Re-open R5/P2 or redeploy the withdrawn Striker book** under cover of this metals cell.

---

## §6 — Gate criteria (closure verdict)

| Verdict | Trigger | Disposition |
|---|---|---|
| `CANDIDATE-proposal` | bar-derived N-SURV clears §2.2 on full + both halves; net>0 after measured venue cost | `INTEGRATE` — lifecycle path (named, not executed here) |
| `DEAD(N-SURV)` | any §2.2 partition fails bust or pass floor (exploratory grade allowed when margin makes bar-derived flip implausible) | `STOP` — pursuit SUBTRACT; registry row |
| `AMBIGUOUS` | bar-derived result in the (3.0%, 3.2%] noise band on the binding partition | `ITERATE` — fresh PREREG only |

**Default prior (post-measurement, disclosed):** `DEAD(N-SURV)` — H2 alone is 5.5× over
ceiling; full/H1 are 14×/24×.

---

## §10 — Audit hooks

```bash
# Pursuit standing flipped off PARK
rg -n "Standing:" docs/pursuits/b8-guardian-mgc-transfer-lane.md
# expect: SUBTRACT (not PARK)

# Closure Iterate tokens
python scripts/check_closure_disposition.py docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md

# Numbers still cited exactly
rg -n "42\.2%|72\.4%|16\.5%" docs/pursuits/b8-guardian-mgc-transfer-lane.md docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md

# No locked-parameter edit licensed
rg -n "byte-identical to v5.5|re-tune locked" docs/briefs/pre-registration/2026-08-11-guardian-mgc-transfer-cell-prereg.md

# No silent bar-derived supersession without reading lab/analysis
rg --no-ignore -il "guardian.*mgc|mgc.*nsurv" lab/analysis || true
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-11 | Retroactive cell PREREG authored after exploratory N-SURV FAIL; closed DEAD(N-SURV) same pass | Cursor (operator-directed) |
