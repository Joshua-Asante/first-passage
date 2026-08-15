# Q-RAIL-1 Phase 1 — execution-expression inventory

**Date:** 2026-07-17  
**Parent brief:** [`docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md`](../../../docs/briefs/Q-RAIL-1-c1-execution-rail-go-live-scoping.md) §7 Phase 1  
**Scope:** locate venue editions; emit FUTURES_LOCK ↔ Tradeify/MFFU delta list. **No Pine edits.**

---

## 1. Edition locate

| File | PORT_MANIFEST pin | On-disk | Hash check |
|---|---|---|---|
| `core/strategies/striker/striker_dj30_v4.5_mym.pine` | `fd91f37b2c76…` | **PRESENT** (23,851 B) | **MISMATCH** — on-disk sha256 `632baeeac785…` ≠ pin |
| `core/strategies/nas/striker_nas100_v1_mnq.pine` | `4bb377296541…` | **MISSING** | N/A |

**Local search (this session):**

- Repo + all linked git/`.claude` worktrees: MNQ `.pine` absent everywhere (only `*_FUTURES_LOCK.md` + unrelated CME trade CSV `…MNQ1!_…beabf.csv`).
- `~/Downloads`, `~/Documents`: zero `*mnq*.pine` / `*nas100*.pine` hits.
- Broad home rglob aborted after Downloads/Documents null (Desktop path absent on this machine).

**Disposition:** MNQ edition is **lost locally** (gitignored ⇒ not in git history). Re-author-from-locked-source (`striker_nas100_v1.pine` → MNQ edition) is the recovery route — **operator authorization required** before any re-author (brief §7 Phase 1; precedent 2026-07-06). MYM is present but **hash-drifted** vs PORT_MANIFEST — treat as untrusted until reconciled (diff vs pin unknown; do not deploy; do not silently re-pin).

**F3 remains `BLOCKED-ON-INPUT`.** Named inputs:

1. Operator GO to re-author MNQ edition (or produce the missing file from a private store).
2. Reconcile MYM on-disk vs `fd91f37b…` pin (restore pinned bytes **or** re-verify + re-pin after deliberate edit audit).
3. Execute both FUTURES_LOCK acceptance checklists (TV compile + CFD parity + hash re-pin) after venue re-parameterization.

---

## 2. Current Bulenox parameterization (sources)

### MYM edition — on-disk Pine (content-read; hash-mismatched)

| Constant | On-disk value | Source |
|---|---|---|
| `commission_value` | **$0.61**/side | `strategy()` header |
| `slippage` | 1 tick | header |
| `accountSize` default | **150000** | futures input group |
| `microCap` default | **150** | futures input (Bulenox 150K-tier shaped) |
| `mymPointValue` | $0.50 | futures input |
| EOD force-flat | ON; bar **16:30 ET** → fill ~**16:45 ET** | `isEodBar` |
| `riskPerTrade` | 0.70% | risk group (locked) |
| `strikerDayStopPct` | **−1.15%** | promoted Bulenox-chain default |
| `maxDailyDD` | 1.15% | risk group |
| RESERVE | `floor(microCap / (1 + pyramidSize/100))` | sizing path |

### MNQ edition — FUTURES_LOCK only (Pine missing)

| Constant | Sheet value | Source |
|---|---|---|
| Costs | $0.61/side + 1-tick slip | FUTURES_LOCK §4 |
| EOD force-flat | 16:30 ET bar → ~16:45 ET fill | FUTURES_LOCK §3 |
| Caps | Bulenox Option-1 ladder 30/70/120/150/250 | FUTURES_LOCK §Venue constants |
| Point value | $2/pt | FUTURES_LOCK |
| Day-stop | *not promoted* (CFD defaults carried) | FUTURES_LOCK §5 |
| Acceptance | all unchecked | FUTURES_LOCK checklist |

### Firm / envelope targets (100K discharge pair)

| Field | Tradeify_Select_100K | MFFU_Rapid_100K | Owner |
|---|---|---|---|
| `cost_per_side_usd` | **0.91** | **0.95** | `firm_rules.py` `a53ee99` |
| `micro_contract_cap` | **80** | **80** | same |
| `max_dd_pct` / geometry | 3.0 trailing_locking (+$100 lock) | 3.0 trailing_locking (+$100 lock) | same |
| Flat deadline | **16:59 ET** (auto-flatten non-fatal) | **16:10 ET** auto-liq (post-16:10 can DISQUALIFY) | envelope §4 |
| E1 build target | **16:00 ET** (both) | **16:00 ET** | envelope E1 |
| Consistency (eval) | 40% soft | 50% soft | `firm_rules` / envelope |
| `accountSize` for $100K tier | **100000** | **100000** | discharge tier |

---

## 3. Per-edition delta list (Bulenox → Tradeify / MFFU)

Shared across both legs unless noted. **Mandatory before any live use** (brief §5 forbids reusing Bulenox editions as-is).

| # | Constant | Current (Bulenox editions) | Target Tradeify 100K | Target MFFU Rapid 100K | Applies | Notes |
|---|---|---|---|---|---|---|
| D1 | `commission_value` ($/side) | **0.61** | **0.91** | **0.95** | MYM + MNQ | TV backtest costs only; live pays firm schedule — still must match for panel fidelity |
| D2 | `microCap` (RESERVE basis) | MYM default **150**; MNQ sheet Bulenox ladder | **80** | **80** | MYM + MNQ | RESERVE base max → `floor(80/8.5)=9` (MYM) / `floor(80/11)=7` (MNQ). Cap-bind on MYM **tightens** vs Bulenox 150 |
| D3 | `accountSize` default | MYM **150000** | **100000** | **100000** | MYM + MNQ | Discharge tier; WATCH-1 haircut stays at account-multiplier layer (F1), not here |
| D4 | EOD force-flat bar | **16:30 ET** (~16:45 fill) | ≤**16:00 ET** trigger (E1) | ≤**16:00 ET** trigger (E1; binding firm 16:10) | MYM + MNQ | **MFFU-critical.** Designing to Tradeify 16:59 is forbidden (envelope). Prefer 15:45 or 16:00 ET bar so fill ≤16:00 |
| D5 | Day soft-stop default | MYM **−1.15%** promoted | **Operator call** — keep −1.15 (automated-chain rationale) vs restore CFD −2.00 | same | MYM (MNQ: confirm source default on re-author) | Not a firm_rules field; automation-safety default from Bulenox chain |
| D6 | Slippage model | 1 tick | Re-verify vs firm/platform | Re-verify vs firm/platform | MYM + MNQ | Keep 1-tick until primary says otherwise; not a hard firm constant |
| D7 | Inactivity / min days | Bulenox ≥1 trade / 5 days (sheet) | Tradeify min **3** trading days (eval); idle rules per FTA | MFFU min **2** days; idle per firm | automation layer | Not necessarily a Pine constant — rail/ops obligation |
| D8 | Acceptance checklist | all open | must execute after D1–D5 | must execute after D1–D5 | MYM + MNQ | TV compile + per-candle CFD parity + hash re-pin |
| D9 | MNQ file existence | **MISSING** | re-author + pin | re-author + pin | MNQ only | Blocks F3 |
| D10 | MYM pin integrity | on-disk ≠ `fd91f37b…` | reconcile before deploy | same | MYM only | Blocks honest F3 PASS even after MNQ returns |

**Not deltas (byte-carry / unchanged):** entry/exit/filter/session hour-blocks, ATR(11), SL 1.20×, locked risk% / pyramid% (parameter axis LOCKED). WATCH-1 0.50× is **not** a Pine risk% edit — F1 fallback = account multiplier.

---

## 4. Cap arithmetic at discharge 100K (informational)

Using Phase-0/F2 RESERVE math at `microCap=80`:

| Leg | RESERVE base max | Recent-90d ideal base @ WATCH-1 | Binding |
|---|---:|---:|---|
| MYM (pyr 750%) | 9 | 11 → capped **9** | **cap binds** (same class as Bulenox finding; tighter at 80 vs 150) |
| MNQ (pyr 1000%) | 7 | 1 | ATR/granularity binds first; cap headroom remains |

---

## 5. Phase 1 verdict

| Item | Result |
|---|---|
| MNQ locate | **FAILED — lost; re-author GO owed** |
| MYM locate | PRESENT but **hash mismatch vs PORT_MANIFEST** |
| Delta list | **EMITTED** (§3 D1–D10) |
| Pine edits | **NONE** (honored) |
| F3 | stays **`BLOCKED-ON-INPUT`** |

**Operator decision owed (unblocks F3 path):** authorize MNQ re-author-from-locked-source + decide MYM pin reconciliation path (restore vs audit-and-re-pin). Acceptance checklists and D1–D5 edits are a subsequent implementation step (still not this Phase-1 inventory).

---

## 6. Next

- After operator GO: re-author MNQ + apply D1–D5 to both editions + run FUTURES_LOCK acceptance → re-score F3.
- Phase 3 (rail architecture docs) can proceed in parallel — it does not require the `.pine` bytes.
- Phase 4 still waits on F3 PASS (or executed fallback) + cost ceiling.
