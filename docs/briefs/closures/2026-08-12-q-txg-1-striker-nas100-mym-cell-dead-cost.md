# Q-TXG-1 cell striker_nas100×MYM — CLOSURE: `DEAD(cost)`

**Verdict:** `DEAD(cost)`
**Closed:** 2026-08-12
**Lane:** transfer-expression / Q-TXG-1
**Election:** #1 · [`ELECTION.md`](../../../lab/archive/transfer_expression_grid_2026-08/ELECTION.md)
**Pre-registration:** [`2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md`](../pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) (`FROZEN`)
**Spend / K:** $0.00 · K declared=1 · K actual=1
**Live effect:** none on the rail or locked book. Cell is dead as a transfer candidate under the frozen cost / `port_must_beat` gate. No `core/` / Pine / allocation / `dd_protection` / firm_rules change by this closure. c1 stays warm/disarmed; M1/GO untouched.
**Artifacts:** [`PANEL_SCORE.json`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/PANEL_SCORE.json) · [`RESULTS.md`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/RESULTS.md) · [`score_cell.py`](../../../lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/score_cell.py) · [`manifest`](../../../discovery_manifests/q_txg1_striker_nas100_mym_20260812.json)

**Lane rule (design §6 / both cell PREREGs §6):** both elected cells are now DEAD/FALSIFIED (this cell `DEAD(cost)`; cell #2 [`DEAD(N-SURV)`](2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md)). **H_A re-argument is now owed before any third election.** A silent third election from remaining OPEN cells is barred.

---

## 1. Verdict against the frozen gate (PREREG §4 / design §5)

| Route | Trigger | Actual | Fired? |
|---|---|---|---|
| **`DEAD(cost)`** | net ≤ 0 after measured venue cost, **or** mean net expectancy fails frozen `required_net_r` / `port_must_beat` (0.06) | Net **+$4,356.40** but mean_net_r **0.0129** < required_net_r **0.06** (~4.6× below cost-tax floor; static-equity recompute OK) | **✓** |
| `DEAD(N-SURV)` | any partition fails bust ≤3.0% ∧ P(pass)≥50% | not reached (cost gate failed first) | — |
| `CANDIDATE-proposal` | cost clear **and** N-SURV clear on full + both halves | not reached | — |
| `AMBIGUOUS` | reserved noise-band only | not reached | — |

Frozen floors (cited, not re-decided): PREREG §2.1–§2.2 · GRID `port_must_beat` · 2026-07-13 prop-survivor Part A (N-SURV not exercised).

---

## 2. Measurement notes (disclosures — not verdict-rescue)

- **Ordering:** `register_search open` (K=1) **before** any PnL/return read — PREREG ordering limb held.
- **Panel:** native TV List-of-Trades for `striker_nas100_v1_mym_qtxg1_prototype` (PORT pin `19264da2…c2756c`); landed bytes SHA `20348086…4a4ebf` (matches tracked `inputs/SHA256SUMS`); N=190; PF 1.110; WR 53.68%; 1R $1,775.75 (full-stop mean, n=11).
- **ENV-1:** cell fully OPEN (power floor 0.0891) — disclosed; does not loosen floors.
- **Bars / N-SURV:** bar-derived path prepared (`MYM_M15` sha `24e16952…597a58`) but **not run** — cost gate closed the cell first.

## 3. What this closure does NOT license

- Killing **MYM the instrument** or **Striker NAS100 on NAS100/MNQ**.
- Treating net>0 alone as a cost PASS (frozen `required_net_r` 0.06 binds).
- A third Q-TXG-1 election without an H_A re-argument packet.
- Locked-parameter retune, floor amendment, firm-shopping, or offline-fill verdicts.
- Re-litigating the 2026-08-04 de-scope (research-leg disclosure already in the PREREG).
- Arming, deploying, or changing live posture.

## 4. Defects found in the frozen brief (recorded, not repaired)

None found. Ordering held; floors unmoved.

## 5. Lesson candidates

Below the two-incident bar as a standalone lesson. Paired with cell #2's DEAD(N-SURV), the elected sibling-swap pair is dual-dead — watch for H_A re-argument product before promoting a "transfer clears cost-tax rarely" claim.

## Iterate — loop exit (MANDATORY)

- **Verdict used:** `DEAD(cost)`
- **Model update:** Cross-underlying Striker-NAS100→MYM sibling-swap produces positive dollar Net but fails the frozen ENV-1 cost-tax / `required_net_r` 0.06 beat (mean_net_r 0.013). Cost limb kills before N-SURV. With cell #2 already DEAD(N-SURV), the election-pair is dual-FALSIFIED — transfer without locked-parameter edits did not clear either elected cell.
- **Next:** ITERATE
- **Routing:** ITERATE — return to **H (H_A re-argument)** per design §6 / PREREG §6 before any third election. Do not elect another OPEN cell from the Block-1 grid silently.
- **Entry packet:** H_A re-argument packet must carry: both cell closures + PANEL_SCORE facts; GRID_RESULTS H_A OPEN n=25 compile provenance; design §5–§7 constraints; forbidden: locked-parameter retune, floor amendment, firm-shopping, treating either panel as CANDIDATE. Operator GO required to open the re-argument (named, not opened here).
- **Stop rule / re-proposal bar:** **new mechanism evidence** (or a fresh Q-TXG-1 election **after** H_A re-argument + cell PREREG) — **not** a locked-parameter retune, **not** amending `required_net_r` / 3.0% floors, **not** firm-shopping.
- **Board write:** STATE forward-trigger — Q-TXG-1 dual-dead → H_A re-argument owed before third election; SESSIONS Open/next carries the same.

- **Registry:** rejected_candidates.md — ### Striker NAS100 → MYM sibling-swap (Q-TXG-1 cell #1) — DEAD(cost)

## §10 audit-hook discharge

```text
register_search open before panel read                    OK    opened_at < first PANEL_SCORE write
K actual == K declared (=1)                             OK    OPERATOR-STOPPED banked K=1
static-equity recompute                                 OK    max|Δ|~0
cost gate mean_r vs required_net_r                      OK    DEAD(cost) 0.0129 < 0.06
N-SURV not run after cost fail                          OK    PREREG close-there
Lane:/Closed: forward fields                            OK
Iterate Next: exactly one token (ITERATE)               OK
core/ / firm_rules / dd_protection / Pine untouched     OK
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-12 | Closure authored; cell #1 DEAD(cost); dual-dead → H_A re-argument owed; boards + manifest close | Cursor (operator-directed) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md
python -X utf8 -c "import json;print(json.load(open('lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/PANEL_SCORE.json'))['cost_gate'])"
```
