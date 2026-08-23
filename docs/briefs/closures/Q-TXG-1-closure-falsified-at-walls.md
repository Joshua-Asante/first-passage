# Q-TXG-1 H_A — CLOSURE: `FALSIFIED-at-walls` (operator elected A)

**Verdict:** `FALSIFIED-at-walls`
**Closed:** 2026-08-12
**Lane:** transfer-expression / Q-TXG-1
**Pre-registration / design:** [`2026-08-11-transfer-expression-grid-design.md`](../../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) §6 · both cell PREREGs §6
**Decision artifact:** [`Q-TXG-1-ha-reargument.md`](../Q-TXG-1-ha-reargument.md) — operator elected **(A) CLOSE**
**Spend / K:** $0.00 · K=0 · no scoring · docs only
**Live effect:** none on the rail or locked book. No `core/` / Pine / allocation / `dd_protection` / firm_rules change. c1 stays warm/disarmed; M1/GO untouched.
**Cell closures (prior):** [`striker_nas100×MYM DEAD(cost)`](2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) · [`striker×MNQ DEAD(N-SURV)`](2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) · [`Guardian→MGC DEAD(N-SURV)`](2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) · Aegis→6J both-layers ([`ops/instruments/6J.md`](../../../ops/instruments/6J.md) J4b+J14)

---

## 1. Verdict against the design §6 / packet §6 gate

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| **(A) CLOSE** | Operator elects A on the H_A re-argument packet | Operator chat election "A" 2026-08-12 | **✓** |
| (B) HOLD | Operator elects B | not elected | — |
| (C) CONTINUE | Operator elects C | not elected | — |

Design §6 owed the re-argument after two consecutive elected-cell FALSIFIEDs. The packet proposed; the operator ruled **CLOSE**.

**Structural basis (packet §2–§3, verified):** all four positive-net transfers died at the composition of the frozen per-trade cost floor and the trailing-DD survival ceiling. Edge transfer was never falsified. Cite `lesson_trailing_dd_survival_is_skew_governed`. Remaining 23 OPEN cells are stop-unscreenable; unlock = ATR-median spend the CLOSE bar refuses without new mechanism evidence.

---

## 2. What this closure does NOT license

- Killing any of the four locked mechanisms on their home instruments.
- Killing ENV-1 instruments as a class.
- Softening `required_net_r`, bust ≤3.0%, or locked risk%.
- A third Q-TXG-1 election, ATR-median campaign, or new-cell spend under this Q-ID.
- Treating TNEC-AU-1 as rescuing any of the four (margin-decisive / non-cadence kills).

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `FALSIFIED-at-walls` (operator A)
- **Model update:** Transfer of locked long-biased trend mechanisms onto the ENV-1 micro pool at Tradeify Select trailing geometry fails at walls, not at edge absence. Small-edge expressions fail the cost tax; large-edge expressions fail trailing-DD survival (skew-governed). Compile-time H_A OPEN does not survive Phase-B dual-FALSIFIED + unscreenable remainder under CLOSE.
- **Next:** STOP
- **Routing:** STOP — lane closed; generation re-aims off this transfer/expression Q-ID (ORB payability + paid/new-venue routes remain the design §6 EMPTY-branch pointer; not opened here).
- **Entry packet:** n/a — STOP.
- **Stop rule / re-proposal bar:** **new mechanism evidence with a demonstrably different loss-side shape**, or a **venue class whose survival geometry differs** (not an EOD-trailing prop clone) — **not** new cells, new instruments, or ATR-input spend alone.
- **Board write:** STATE · lab/CATALOG · docs/briefs/INDEX · rejected_candidates · GRID/RESULTS status · SESSIONS — this pass.

- **Registry:** rejected_candidates.md — ### Transfer/expression lane (Q-TXG-1) — FALSIFIED-at-walls

## §10 audit-hook discharge

```text
operator elected exactly one of A/B/C                          OK    A CLOSE
packet Status CLOSED — FALSIFIED-at-walls                     OK
registry lane row + re-proposal bar                           OK
CATALOG / RESULTS no longer ACTIVE for further election       OK
third election barred                                         OK
Iterate Next: exactly one token (STOP)                        OK
core/ / firm_rules / dd_protection / Pine untouched           OK
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-12 | Lane closure authored; operator A; boards + registry | Cursor (operator-directed) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-TXG-1-closure-falsified-at-walls.md
rg -n "FALSIFIED-at-walls|operator elected" docs/briefs/Q-TXG-1-ha-reargument.md
rg -n "transfer/expression lane|FALSIFIED-at-walls" docs/rejected_candidates.md
```
