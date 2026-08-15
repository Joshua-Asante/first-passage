# Pre-registration — Q-TXG-1 cell: Striker DJ30 × MNQ (sibling-swap)

> **Ordering honesty (load-bearing):** this PREREG is frozen **before** port code,
> offline parity, native-TV export, PnL reads, or N-SURV. It refuses the MGC ordering
> defect ([closure §4](../closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md)).
> Known Trap #12: do not amend floors in place after results.

**Status:** `FROZEN` · 2026-08-12 · **authorizes port build + RUNSPEC only** ($0 · K=0 until
manifest open in Block 4)
**Election:** **operator election via task start** · 2026-08-12 · election packet
[`ELECTION.md`](../../../lab/archive/transfer_expression_grid_2026-08/ELECTION.md) rank **#2**
**Parent:** [Q-TXG-1 design §5](../../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) ·
[GRID_RESULTS](../../../lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.md) H_A OPEN
**Cell:** mechanism `striker` (Striker DJ30 v4.5, LOCKED) × instrument **MNQ** (CME micro Nasdaq)
**Transfer type:** **cross-underlying** (sibling-swap — DJ30 breakout logic on Nasdaq micro; transplant prior 0/2 named burden)
**De-scope disclosure:** Striker-**mechanism** research on a **different** instrument under the
2026-08-04 de-scope amendment — a **new leg**, **NOT** the barred locked-book redeploy of
striker×MYM (WITHDRAWN(F1)). Cite:
[`docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md)
Addendum 2026-08-04 (*"Tradeify-shaped base-construct research is not barred"*).
**K:** **K=1** declared for the eventual cell score (Block 4 `register_search open`). This freeze
commits **no** K and opens **no** manifest.
**Spend this block:** $0 · no pulls · **no PnL/return reads** until Block 4.

---

## §0 — Rule-0 reads (verified 2026-08-12 @ HEAD `4e3bc48`)

- [`docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md`](../../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) @ `5fe755e` — §5 kill-chain · §6 two-FALSIFIED→re-argue-H_A · §7 forbidden moves
- [`lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.json`](../../../lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.json) @ `bd9a593` — frozen `port_must_beat` for this cell
- [`docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](../closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) @ `42e27a1` — ordering defect + DEAD(N-SURV) kill class
- [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](2026-07-13-prop-survivor-scoring-prereg.md) @ `91137fb` — Part A bust ≤3.0% ∧ P(pass)≥50%
- [`docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md`](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md) @ `45e3cea` — redeploy bar + research amendment
- [`docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md`](../../adr/2026-07-10-strategies-never-locked-lifecycle-governance.md) @ `45e3cea` — parameter axis LOCKED
- [`core/strategies/_archive/striker/LOCK.md`](../../../core/strategies/_archive/striker/LOCK.md) @ `85156a0` — DJ30 locked config (signal identity)
- [`core/firm_rules.py`](../../../core/firm_rules.py) @ `0356be2` — `_BASE_RISK["striker"]=0.0070` · `Tradeify_Select_100K` balance 100_000
- [`docs/spec/2026-07-27-third-leg-target-spec.md`](../../spec/2026-07-27-third-leg-target-spec.md) @ `5563cf4` — S7 occupancy mechanism (disclosure)

Pine source is gitignored; port build reads locked `.pine` bytes from a local clone and
hash-pins the edition — Pine is not transcribed into this freeze.

---

## §1 — Port mapping rule (locked logic untouched)

| Layer | Fixed |
|---|---|
| Signal / risk identity | **Striker DJ30 v4.5** — lookback 15 · ATR 11 · SL **1.20×ATR** · TP 8.5×ATR · BE 0.15/0.05 · trail 0.15/0.90/0.80 · maxHold 55b · pyramid 1.29×ATR / **750%** / minBars 6 · risk **0.70%** · session **13–17 UTC** · DOW **Tue/Fri** — **byte-identical** to locked DJ30 Pine (LOCK.md). **No** NAS100 parameter borrow. |
| Instrument mapping | CME **`MNQ1!`** 15m (micro Nasdaq) — the **only** declared change of identity |
| Sizing / cost | Integer qty at locked risk% vs MNQ tick economics ($2.00/pt, tick 0.25); Tradeify Select commission $0.91/side + 1-tick slip; `accountSize` 100_000; `microCap` 80 — venue mechanics class of the withdrawn MNQ edition, **not** a locked-constant change |
| Venue hold | EOD force-flat ET-pinned (FRIENDLY auto-liquidate); discharge default ~15:45 ET bar → ~16:00 ET fill |
| Offline parity | Allowed (`series[k]` offset, `percent_of_equity` traps). **No verdict off offline fills** — native TV panel is the arbiter (design §7) |

Withdrawn same-underlying `striker×MYM` is **out of scope** (F1). This cell is the
cross-underlying sibling, not a redeploy.

---

## §2 — Frozen floors + port_must_beat (verbatim)

### §2.1 Survival / cost floors (owners cited — not re-decided)

| Item | Frozen value | Owner |
|---|---|---|
| Tier | `Tradeify_Select_100K` | S1 / `firm_rules` |
| N-SURV bust ceiling | ≤ **3.0%** | 2026-07-13 prop-survivor prereg §3 Part A |
| N-SURV pass floor | P(pass) ≥ **50%** | same |
| Regime | **both halves** must clear | regime_robustness_gate / Q-TXG-1 H_B |
| Net-after-cost | net expectancy **> 0** after measured venue cost | design §5 step 4 |
| K | **K=1** at scoring | design §7 |

### §2.2 `port_must_beat` (verbatim from GRID_RESULTS.json `open_cells[]`)

```json
{
  "cost_tax_r": 0.03,
  "env1_cell_verdict": "OPEN-CONDITIONAL(power)",
  "lifecycle": 1.0,
  "nsurv_ceiling_pct": 3.0,
  "qty_at_locked_risk": 8,
  "required_net_r": 0.03,
  "risk_pct": 0.007,
  "stop_ticks": 160
}
```

Compile notes: stop mapped **160t** from raw **218.45t** (1.20 × MNQ ATR(11) 45.5095 pts /
tick 0.25) — nearest ladder rung (ties → larger). ENV-1 verdict
**OPEN-CONDITIONAL(power)**: no committed MNQ panel N in the ENV-1 power floor —
**disclosed here; not resolved** in Blocks 2–3.

---

## §3 — S7 / slot-overlay disclosure (never a Block-3 kill)

From Block-1 disclosure: **MNQ Mon+Tue · MYM Tue+Fri**; both c1 legs withdrawn;
`LEG_MAP` retained-not-released. Bindingness deferred — disclosure only for this freeze.
This cell's DJ30 DOW is **Tue/Fri**; MNQ third-leg overlay marks **Mon+Tue** — Tuesday
overlap is named, not adjudicated as a kill here. W-CADENCE / W-REGIME remain disclosure.

---

## §4 — Falsifiable hypothesis (H_B for this cell)

**H-DJMNQ:** the execution-mechanics-only Striker-DJ30→MNQ port, at locked v4.5 risk identity
and true Tradeify Select 100K geometry, produces a native-TV panel with **net>0 after measured
venue cost** and clears N-SURV (bust ≤3.0% ∧ P(pass)≥50%) on the **full panel and both halves**.

**Reject (cell FALSIFIED) if:** net≤0 after measured cost → `DEAD(cost)`; any N-SURV partition
fails bust or pass floor → `DEAD(N-SURV)`; locked-parameter edit detected → protocol void.
**Accept path:** CANDIDATE-proposal only via unchanged lifecycle (named by a later closure —
never executed by this freeze).
**Power condition:** ENV-1 `OPEN-CONDITIONAL(power)` stays a disclosure — it does not loosen
§2.1 floors and does not authorize inventing a panel N.

---

## §5 — Forbidden moves

- **Locked-parameter retune** ("session-tuned MNQ edition") — design §7; not transfer.
- **Redeploy narrative** — treating this as the withdrawn striker×MYM c1 leg.
- **Resolving OPEN-CONDITIONAL(power) by invention** — disclose only until a committed N exists.
- **Offline-fill verdict** — native-TV-arbiter lesson.
- **PnL/return reads before manifest** — Block 4 only.
- **Invented ATR / borrow across ATR lengths**.
- **Third election after two FALSIFIEDs without re-arguing H_A** — design §6 (below).
- **Firm-shopping / floor amendment** after seeing numbers — Known Trap #12.

---

## §6 — Pre-committed lane rule (before results)

**Two consecutive elected-cell FALSIFIEDs force a re-argument of H_A, not a third election.**
This cell is election-pair member #2. Recorded now so a FAIL cannot be repaired by silently
electing the next UNSCREENABLE OPEN cell.

---

## §7 — Block boundary (HARD STOP of Blocks 2–3)

Blocks 2–3 end when: this PREREG is committed · port is gitignored + hash-pinned · RUNSPEC is
authored. **STOP before scoring.** No `register_search open`, no panel metrics, no N-SURV run.

**RUNSPEC (operator-owed):**
[`lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/RUNSPEC.md`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/RUNSPEC.md)
**(authored in Block 3; path reserved here).** TV login automation is **PROHIBITED**.
