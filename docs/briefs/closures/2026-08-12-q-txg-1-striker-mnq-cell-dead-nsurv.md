# Q-TXG-1 cell striker×MNQ — CLOSURE: `DEAD(N-SURV)`

**Verdict:** `DEAD(N-SURV)`
**Closed:** 2026-08-12
**Lane:** transfer-expression / Q-TXG-1
**Election:** #2 · [`ELECTION.md`](../../../lab/archive/transfer_expression_grid_2026-08/ELECTION.md)
**Pre-registration:** [`2026-08-12-q-txg-1-striker-mnq-cell-prereg.md`](../pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md) (`FROZEN`)
**Spend / K:** $0.00 · **K declared=1 · K actual=1** ([manifest](../../../discovery_manifests/q_txg1_striker_mnq_20260812.json) closed OPERATOR-STOPPED after panel+N-SURV)
**Live effect:** none — research cell only; no rail / locked-book / Pine / `dd_protection` / `firm_rules` change. De-scope disclosure: Striker-*mechanism* on a *different* instrument under the 2026-08-04 amendment — **not** WITHDRAWN(F1) striker×MYM redeploy ([ADR](../../adr/2026-08-04-tradeify-venue-descope-eval-included.md)).
**Artifacts:** [`PANEL_SCORE.json`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json) · [`NSURV_BLOCK.txt`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/NSURV_BLOCK.txt) · [`score_cell.py`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/score_cell.py) · panel pin `inputs/SHA256SUMS`

---

## Sibling cell status at authoring (lane rule)

**Cell #1 `striker_nas100×MYM`:** **not closed** at authoring time — no closure under `docs/briefs/closures/`, no open PR, sibling worktree still at pre-closure surface (operator export landed; this closure does **not** score or adjudicate cell 1).

**Lane rule (design §6 / both cell PREREGs §6):** H_A re-argument fires only when **both** elected cells close DEAD/FALSIFIED. That condition is **not met** here — cell 2 is dead; cell 1 unfinished. **No H_A re-argument packet in this closure.** If cell 1 later also closes DEAD/FALSIFIED, the lane rule binds at that closure — a third election without re-arguing H_A remains barred once both are dead. One survivor would reset the count; that path is not available to this cell.

---

## 1. Verdict against the frozen gate (PREREG §4 / design §5)

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| `DEAD(cost)` | net ≤ 0 after measured venue cost | Net **+$22,789.58** · mean_net_r **0.0419** > required_net_r **0.03** (static-equity recompute OK) | — |
| **`DEAD(N-SURV)`** | any partition fails bust ≤3.0% ∧ P(pass)≥50% | Full **98.13%** bust / 1.87% pass; H1 **96.76%** / 3.24%; H2 **99.37%** / 0.63% — bust ceiling missed on **every** partition (~32×–33×) | **✓** |
| `CANDIDATE-proposal` | cost clear **and** N-SURV clear on full + both halves | not reached | — |

Frozen floors (cited, not re-decided): [`2026-07-13-prop-survivor-scoring-prereg.md`](../pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — bust ≤ **3.0%** ∧ P(pass) ≥ **50%** at `Tradeify_Select_100K`.

**N-SURV block (verbatim):**

```text
firm=Tradeify_Select_100K sizing_basis=$100,000 half_boundary=2024-03-19
floor: bust≤3.0% ∧ P(pass)≥50%
full: bust=98.13% pass=1.87% FAIL (n=164)
H1: bust=96.76% pass=3.24% FAIL (n=82)
H2: bust=99.37% pass=0.63% FAIL (n=82)
N-SURV FAIL
```

---

## 2. Measurement notes (disclosures — not verdict-rescue)

- **Ordering:** `register_search open` (K=1) **before** any PnL/return read — PREREG ordering limb held.
- **Panel:** native TV List-of-Trades for `striker_dj30_v4.5_mnq_qtxg1_prototype` (PORT pin `178a2a8e…806d`); landed bytes SHA `7bf08a23…4025`; N=222; PF 1.308; static-equity recompute max |Δ| ~0 (commission $0.91/side already in TV Net).
- **ENV-1 `OPEN-CONDITIONAL(power)`:** MNQ power floor remains **UNSCREENABLE** (no committed panel N) — **disclosed only; not resolved**; does not loosen §2.1 floors.
- **Half boundary:** midpoint-by-day-count **2024-03-19** — **not date-frozen in the cell PREREG**; disclosed (MGC midpoint caveat class). Both halves still fail bust by ~32×.
- **Bars:** canonical `core/data/bar_data/MNQ_M15.csv` (SHA `6c86f41a…e00a`, W1-proven parse of CME MNQ M15 BAR EXPORT). **4** post-panel days after bar end (2026-07-02) dropped for missing coverage; n=164 business days scored. Bar-derived `intraday_low` (not AE approximation).
- **Kill class:** same trailing-DD survival failure family as Guardian→MGC / Aegis→6J J4b at Tradeify Select 100K; overshoot here is larger than MGC's exploratory best-half bust.

---

## 3. What this closure does NOT license

- Killing **MNQ the instrument** or ENV-1 posture beyond this cell.
- Killing **Striker DJ30 v4.5** on DJ30 / MYM locked-book identity.
- Adjudicating cell #1 `striker_nas100×MYM` (read-only status above).
- H_A EMPTY / transfer-lane-exhausted board write (both elected cells not yet dual-dead).
- Locked-parameter retune, floor amendment, firm-shopping, or treating offline fills as a verdict.
- Re-litigating the 2026-08-04 de-scope (research-leg disclosure already in the PREREG).

---

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `DEAD(N-SURV)`
- **Model update:** Cross-underlying Striker-DJ30→MNQ sibling-swap clears the cost gate (mean_net_r 0.042 > 0.03) but collapses at the trailing-DD wall under frozen Part A — same qualitative kill class as prior transfer cells, larger bust overshoot. Transfer without locked-parameter edits is not a survival free lunch on MNQ either.
- **Next:** ITERATE
- **Routing:** ITERATE — cell #2 dead; await cell #1 `striker_nas100×MYM` Blocks 4–5 closure for the lane rule. If cell 1 also DEAD/FALSIFIED → H_A re-argument before any third election (design §6). If cell 1 clears → one survivor resets the consecutive-FALSIFIED count; no re-argument.
- **Entry packet:** cell-1 closure (or its BLOCKED/export status) · then either H_A re-argument packet **or** survivor INTEGRATE path — not a silent third election.
- **Stop rule / re-proposal bar:** **new mechanism evidence** for a Striker-family × MNQ expression (or a fresh Q-TXG-1 election + cell PREREG on a different OPEN cell) — **not** a locked-parameter retune, **not** amending the 3.0% floor, **not** firm-shopping, **not** inventing an ENV-1 panel N.
- **Board write:** STATE · lab/CATALOG · docs/briefs/INDEX · rejected_candidates · SESSIONS `2026-08-12j` — this pass.

- **Registry:** rejected_candidates.md — ### Striker DJ30 → MNQ sibling-swap (Q-TXG-1 cell #2) — DEAD(N-SURV)

## §10 audit-hook discharge

```text
register_search open before PnL                         OK    manifest opened 2026-08-12T04:56:54Z
K actual == K declared (=1)                             OK    OPERATOR-STOPPED banked K=1
static-equity recompute                                 OK    max|Δ|~0
cost gate net>0 / mean_r>required_net_r                 OK    PASS_COST
N-SURV bar-derived MNQ_M15                              OK    FAIL all partitions
ENV-1 OPEN-CONDITIONAL(power) disclosed not resolved    OK
sibling cell-1 not adjudicated                          OK
Lane:/Closed: forward fields                            OK
Iterate Next: exactly one token (ITERATE)               OK
core/ / firm_rules / dd_protection / Pine untouched     OK
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-12 | Closure authored; cell #2 DEAD(N-SURV); boards + manifest close | Cursor (operator-directed) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md
python -X utf8 -c "import json;print(json.load(open('lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json'))['nsurv']['nsurv'])"
```