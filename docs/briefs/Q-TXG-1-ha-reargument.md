# Q-TXG-1 — H_A re-argument packet (post dual-elected-cell FALSIFIED)

**Status:** `CLOSED — FALSIFIED-at-walls` · operator elected **(A) CLOSE** 2026-08-12
**Authored:** 2026-08-12
**Closed:** 2026-08-12
**Lane:** transfer-expression / Q-TXG-1
**Authors:** Cursor (operator-directed) · operator ruling via chat election "A"
**Parent:** Q-TXG-1 design §6 — two consecutive elected-cell FALSIFIEDs ⇒ re-argue H_A before a third election
**Spend / K:** $0.00 · K=0 · no scoring · docs only
**Artifact path:** `docs/briefs/Q-TXG-1-ha-reargument.md`
**Lane closure:** [`closures/Q-TXG-1-closure-falsified-at-walls.md`](closures/Q-TXG-1-closure-falsified-at-walls.md)

> **Ruling (2026-08-12 / JA via chat).** Operator elected **(A) CLOSE**. The transfer/expression lane is **FALSIFIED-at-walls** under the current mechanism set × ENV-1 pool × EOD-trailing prop survival geometry. Third election barred. Registry row + board/CATALOG flips land in the same ruling commit as this §-ruling.

---

## §0 — Rule 0 reads (verified 2026-08-12 @ HEAD `2a342fe`)

| Path | Anchor | What was read |
|---|---|---|
| [`docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md`](../superpowers/specs/2026-08-11-transfer-expression-grid-design.md) | `5fe755e` | §3 H_A / H_B · §6 two-FALSIFIED→re-argue-H_A · §7 forbidden moves |
| [`docs/briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md`](closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) | `a66fce4` | cell #1 DEAD(cost); dual-dead → H_A re-argument owed; silent third election barred |
| [`docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md`](closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) | `9856a39` | cell #2 DEAD(N-SURV); cost PASS; bust ~98%/97%/99% |
| [`docs/briefs/closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md`](closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) | `42e27a1` | Guardian→MGC DEAD(N-SURV) 42.2/72.4/16.5; b8 SUBTRACT |
| [`ops/instruments/6J.md`](../../ops/instruments/6J.md) | `45e3cea` (file) · J4b + J14 body | Aegis→6J +$39,056 / PF 2.318 / +0.218R; J4b trail fail; J14 both-layers CLOSED |
| [`lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.md`](../../lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.md) | `7821be0` | 28-cell table · H_A OPEN n=25 · `port_must_beat` · 23/25 UNSCREENABLE |
| [`docs/spec/2026-08-11-tnec-application-unit-book-admission.md`](../spec/2026-08-11-tnec-application-unit-book-admission.md) | `d692c2c` (merged #759) | PROPOSED · BOOK-CONDITIONAL cadence-only · margin-decisive kills stay dead · bust never book-only |
| [`docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md`](pre-registration/2026-08-12-q-txg-1-striker-nas100-mym-cell-prereg.md) | `60597a1` | §6 lane rule frozen before results |
| [`docs/briefs/pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md`](pre-registration/2026-08-12-q-txg-1-striker-mnq-cell-prereg.md) | `60597a1` | §6 lane rule frozen before results |
| [`STATE.md`](../../STATE.md) forward-trigger 2026-08-12 | tip `2a342fe` | dual-dead → H_A re-argument owed; third election barred |
| PANEL_SCORE cells (byte-check) | `a66fce4` / `9856a39` | mean_net_r / required_net_r / nsurv partitions |

**Why owed (design §6, verified):**

> Elected cell FALSIFIED → ITERATE … **two consecutive cell FALSIFIEDs ⇒ re-argue H_A before a third**

Both cell PREREGs §6 pre-committed the same rule. Cell #1's closure declared the re-argument owed and barred a silent third election. STATE 2026-08-12 carries the bar.

---

## §1 — Context

Q-TXG-1 systematized the transfer lane after Aegis→6J discovered walls mid-campaign. Block 1 compiled a 4×7 grid at $0 (H_A OPEN, n=25). Block 2 elected the only two stop-mapped OPEN cells — `striker_nas100×MYM` then `striker×MNQ`. Both are now dead under frozen floors. Design §6 + both PREREGs §6 force this re-argument before any third election. The question is no longer "which OPEN cell next?" — it is whether H_A still licenses further election spend under the walls the elected pair already hit.

Standing doctrine that binds: locked-parameter immutability (design §7); frozen cost / N-SURV floors (2026-07-13 survivor prereg — not re-decided here); `lesson_trailing_dd_survival_is_skew_governed` (survival vs a fixed-$ trail is loss-shape, not mean/vol); rejected-candidates re-proposal bars elsewhere that refuse new cells / new instruments / ATR-input spend without new *mechanism* evidence.

---

## §2 — Evidence table (verified against closures / PANEL_SCORE / 6J ledger)

| Cell | Gross / net | Cost gate | Survival gate | Standing |
|---|---|---|---|---|
| **Aegis→6J** (2026-07; outside ENV-1 pool; lane precedent) | Net **+$39,056.10** · PF **2.318** · n=129 · expectancy **+0.218R** (J1) | passed (+0.218R venue residual; frictionless +0.342R) | J4b best cell **3.88%** bust vs ≤3.0% (1.3×); matrix arms through **~9–18%**; J14 composed 3-leg **0/3 tiers** (10.96 / 3.78 / 3.54) + **cap-infeasible** (6J=10 micro-eq; M6J at no FRIENDLY) → **CLOSED both layers** | instrument ledger J4b + J14 |
| **Guardian→MGC** (2026-08-11) | exploratory panel (N=329 / daily n=276) | not reached as gate | bust **42.2 / 72.4 / 16.5** full/H1/H2 — **5.5–24×** over ≤3.0% → **DEAD(N-SURV)**; b8 **SUBTRACT** | [closure](closures/2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md) |
| **striker_nas100×MYM** (2026-08-12, election #1) | Net **+$4,356.40** · PF **1.110** · N=190 | **FAILED:** mean_net_r **0.0129** < required_net_r **0.06** (~4.6×) | not reached | [closure](closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md) · PANEL_SCORE |
| **striker×MNQ** (2026-08-12, election #2) | Net **+$22,789.58** | **PASSED:** mean_net_r **0.0419** > required_net_r **0.03** | bust **98.13 / 96.76 / 99.37** full/H1/H2 — **~32–33×** over ≤3.0% → **DEAD(N-SURV)** | [closure](closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md) · PANEL_SCORE |

All four cells showed **positive net dollars** (Guardian exploratory panel was not cost-gated as a kill, but was not a net≤0 kill either). Edge *transfer* — positive expectancy after venue mapping — was never the falsifier.

---

## §3 — Structural finding

**The lane dies in the composition of the frozen per-trade cost floor and the trailing-DD survival ceiling — not in the absence of transferable edge.**

- Small-edge / shallow-stop expressions fail the cost tax (`required_net_r` / `port_must_beat`): election #1 cleared net>$0 and still missed 0.06R by ~4.6×.
- Large-edge expressions clear cost and carry loss shapes the EOD-trailing prop geometry cannot survive: election #2 (~33× over bust), Guardian→MGC (5.5–24×), Aegis→6J (both-layers close after the best trail cell still sat 1.3× over).

Cite: **`lesson_trailing_dd_survival_is_skew_governed`** — survival against a fixed-dollar trailing barrier is governed by loss-side shape, not mean/vol. Positive mean with the wrong skew still busts the trail. That is the kill class shared by Aegis→6J J4b, Guardian→MGC, and striker×MNQ.

**Remaining-surface fact (from GRID_RESULTS, after both elections):**

- Compile: H_A OPEN n=25; **23/25** carried `stop_cell: UNSCREENABLE`; the only two mapped-stop OPEN cells were the ones elected — both now dead.
- **23 OPEN cells remain**, every one stop-unscreenable. Unlock path named by the grid: **ATR-matched-median campaigns** (input spend), not a free re-score.
- Composition of the 23 (verified, correcting a parent-session shorthand that said "Guardian/Aegis only"): **Guardian 6 · Striker 5 · Striker_NAS100 5 · Aegis 7**. Striker-family remainder exists, but has no mapped stop and no surviving mapped sibling — the two cells that *could* be scored without ATR spend are the dual-dead pair.
- Both mechanisms that already produced **strong** expressions died at these exact walls: Guardian's same-underlying MGC cell at N-SURV (margin-decisive); Aegis produced the lane's best gross (+$39k / +0.218R) and still died at survival + cap. Guardian's locked risk% (**0.34%**) is the smallest of the four mechanisms — smaller than the cost-killed cell's mechanism risk (**0.37%**) — so the deeper-stop "cut the tax" rescue is *more* qty-hostile for Guardian expressions, not less (counter-arithmetic in disposition C).

---

## §4 — Question (symptom form)

**Q-TXG-1 / H_A re-argument:** Given two consecutive elected-cell FALSIFIEDs at the frozen cost and trailing-survival walls, and a remaining OPEN surface that is entirely stop-unscreenable, does H_A still license further election or ATR-input spend — or is the transfer lane exhausted *at these walls* under the current mechanism set and venue class?

(Symptom only: dual-dead + unscreenable remainder + walls that killed strong positive-net expressions. Does not bake in CLOSE / HOLD / CONTINUE.)

---

## §5 — Forbidden moves

- **Silent third election** from remaining OPEN cells — barred by design §6, both PREREGs §6, cell #1 closure, and STATE 2026-08-12.
- **Re-scoring any dead cell** / editing any closure / softening any wall constant (`required_net_r`, bust ≤3.0%, pass ≥50%, locked risk%, trail geometry).
- **Locked-parameter retune** framed as "transfer" — design §7; the move this lane exists to resist.
- **ATR-input spend or third election without an operator ruling on this packet** — CONTINUE is a typed disposition, not a default.
- **Treating TNEC-AU-1 (PROPOSED, #759) as rescuing any of the four** — see §8 boundary notes.
- **Executing registry / CATALOG / lane-closure writes from this packet alone** — proposes only; operator rules.
- **Firm-shopping** or amending floors to launder a bust / cost miss.
- **Offline-fill verdicts** or inventing ATR medians to flip UNSCREENABLE → OPEN without a named campaign.

---

## §6 — Binary election gate (exactly one)

| Verdict | Trigger | Disposition this packet pre-registers for the *ruling* (not executed here) |
|---|---|---|
| **(A) CLOSE** | Operator elects A | STOP — lane FALSIFIED-at-walls; registry row + re-proposal bar (below); board/CATALOG flips in the ruling commit |
| **(B) HOLD** | Operator elects B | HOLD — GRID_RESULTS stands as decision basis; no further election or ATR-input spend; rides **2026-11-08**; re-entry needs operator re-open |
| **(C) CONTINUE** | Operator elects C | ITERATE — fund ATR-median campaigns + third election under a fresh cell PREREG; K/ATR budget named in the ruling |

**Ambiguous / deferred is not a legal vote.** Exactly one of A / B / C.

---

## §7 — Dispositions (strongest honest case → lean)

### (A) CLOSE — lane FALSIFIED-at-walls

**Strongest honest case.** Four positive-net transfers; zero survivors against the frozen composition of cost floor + trailing-DD ceiling. The elected pair exhausted the only stop-mapped OPEN cells. Remaining 23 require ATR-median spend to become scorable, and the mechanisms that already cleared strong expressions (Aegis best gross; Guardian same-underlying) died at these walls. Further cells / instruments / ATR campaigns without new *mechanism* evidence (or a different venue-class survival geometry) are the exhausted move the registry bars elsewhere. Matches design §6's H_A EMPTY spirit even though compile-time H_A was OPEN — the Phase-B kill-chain falsified the transferable-and-survivable reading.

**Proposed registry bar (for the ruling commit, not this packet):** new mechanism evidence with a **demonstrably different loss-side shape**, or a **venue class whose survival geometry differs** (not an EOD-trailing prop clone) — **not** new cells, new instruments, or ATR-input spend alone.

**Lean weight:** high — this is the registry-consistent close.

### (B) HOLD — grid RESULTS as decision basis; park to 2026-11-08

**Strongest honest case.** Compile-time H_A was OPEN (n=25); design §6 already names a HOLD branch for "H_A ≥1, no election." Dual-dead ends the *election pair*, not necessarily the compile claim. HOLD freezes spend (no third election, no ATR campaign) while preserving the grid as the standing instrument-lane input through the **2026-11-08** four-firms / PARK-expiry audit. Re-entry is an operator re-open, not agent default. Avoids writing a domain rejection before the dated programme review if the operator wants optionality without authorizing CONTINUE's spend.

**Lean weight:** high — same practical posture as A on spend; differs on whether the lane is named FALSIFIED-at-walls in the registry now.

### (C) CONTINUE — ATR-median campaigns + third election

**Strongest honest case.** The cost-floor kill was geometry-specific: election #1's `required_net_r` 0.06 sat on an 80-tick mapped stop (ENV-1 cost tax 0.060R at that rung). A deeper ATR-matched stop lowers cost tax (tax ∝ 1/stop_$). Some of the 23 UNSCREENABLE cells could, after honest ATR-median unlock, clear cost and present a different loss shape than the dual-dead Striker pair. Striker-family remainder (10 cells) has not been scored; Guardian/Aegis have not been scored on ENV-1 micros under Q-TXG-1 Phase B. CONTINUE is the only disposition that treats compile-time H_A OPEN as still fireable.

**Counter-arithmetic (why the strongest case fails under frozen constraints).** Take MYM-class RT ≈ $2.40 (the ENV-1 tax that produced 0.06R at 80t × $0.50). Cost tax = RT / R_usd. To drive tax down to the **delivered** mean_net_r of the cost-killed cell (0.0129) — i.e. so that cell's own edge would have cleared — needs R_usd ≈ $186 → **~372 ticks** on a $0.50/tick micro. At Guardian's locked **0.34%** risk ($340 on $100k): qty = ⌊340 / 186⌋ = **1**. Push tax lower and qty stays 1 until R_usd > $340 (**>680 ticks**) → **DEAD(cap)**. Deeper stops that "fix" cost therefore collapse qty toward the cap wall and enlarge the $ loss per full-stop — the exact input that trailing-DD survival is skew-governed by. Aegis already cleared a *large* residual (+0.218R) and still died at the trail. CONTINUE spends ATR-median K to rediscover walls the strong expressions already hit.

**Lean weight:** low — the exhausted move.

### Recommended lean (parent session → recommendation, not ruling)

**A or B.** Continuing is the exhausted move the registry bars elsewhere. Prefer **A** if the operator wants the lane named FALSIFIED-at-walls with an explicit re-proposal bar now; prefer **B** if the operator wants the same spend-freeze without a registry write until the 2026-11-08 audit. This packet does not pick between A and B.

---

## §8 — Boundary notes (TNEC-AU-1)

[`docs/spec/2026-08-11-tnec-application-unit-book-admission.md`](../spec/2026-08-11-tnec-application-unit-book-admission.md) is **PROPOSED** (merged #759). On its own terms it **rescues none of these four**:

- **Margin-decisive N-SURV kills stay dead** — Guardian→MGC is the calibration case named in the spec boundary; striker×MNQ (~33×) and Aegis→6J are the same class.
- **The bust ceiling never becomes book-only** — composed/book admission does not waive standalone trail failure of this magnitude.
- **`BOOK-CONDITIONAL(cadence)` saves cadence-only kills** — none of these four died on cadence / N-ACT.

If the operator elects **A or B**, any future re-proposal is adjudicated under **whatever application-unit regime is then in force** (this PROPOSED spec, a ratified successor, or neither). That forward pointer is not a rescue of the present record.

---

## §9 — What this packet does / does not execute

| Executes now | Does **not** execute (ruling-only) |
|---|---|
| Authors this proposal | Elect A / B / C |
| STATE line: packet authored, ruling pending | `docs/rejected_candidates.md` row |
| SESSIONS class-A entry | lab/CATALOG or briefs INDEX status flip |
| Keeps third-election bar up | Lane closure / H_A EMPTY board write |
| | ATR-median campaign funding / third cell PREREG |

---

## §10 — Audit hooks (runnable)

```bash
# Lane rule still on the design
rg -n "two consecutive cell FALSIFIEDs" docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md
# Expected: §6 row present

# Dual-dead bar still on STATE
rg -n "H_A re-argument" STATE.md
# Expected: 2026-08-12 forward-trigger (updated by this pass to note packet authored)

# Evidence numbers still match closures / PANEL_SCORE
python -X utf8 -c "import json;d=json.load(open('lab/archive/transfer_expression_grid_2026-08/cells/striker_nas100_mym/PANEL_SCORE.json'));c=d['cost_gate'];assert c['verdict'].startswith('DEAD(cost)');assert abs(c['mean_net_r']-0.0129)<5e-4;assert c['required_net_r']==0.06"
python -X utf8 -c "import json;d=json.load(open('lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/PANEL_SCORE.json'));assert d['cost_gate']['verdict']=='PASS_COST';n=d['nsurv'];assert n['nsurv']=='FAIL';assert abs(n['full']['headline_bust']-0.9813)<5e-4"

# Remaining OPEN surface still 23 UNSCREENABLE after dual election (compile artifact unchanged)
python -X utf8 -c "import json;from collections import Counter;d=json.load(open('lab/archive/transfer_expression_grid_2026-08/GRID_RESULTS.json'));print(d['h_a'],len(d['open_cells']),Counter((c['mech'], 'UNSCR' if c['port_must_beat'].get('stop_cell')=='UNSCREENABLE' else 'MAPPED') for c in d['open_cells']))"
# Expected: OPEN, 25 compile-open (artifact frozen); 23 UNSCR + 2 MAPPED at compile — mapped pair now dead by closures, not by re-compile

# TNEC-AU-1 boundary still names margin-decisive stay-dead
rg -n "margin-decisive|BOOK-CONDITIONAL|bust ceiling never becomes book-only" docs/spec/2026-08-11-tnec-application-unit-book-admission.md

# This packet has not silently ruled
rg -n "RULING PENDING|exactly one of A / B / C" docs/briefs/Q-TXG-1-ha-reargument.md
```

---

## Verification

```bash
# §0 anchors resolve at the cited commits
git log -1 --format=%h -- docs/superpowers/specs/2026-08-11-transfer-expression-grid-design.md   # 5fe755e
git log -1 --format=%h -- docs/briefs/closures/2026-08-12-q-txg-1-striker-nas100-mym-cell-dead-cost.md  # a66fce4
git log -1 --format=%h -- docs/briefs/closures/2026-08-12-q-txg-1-striker-mnq-cell-dead-nsurv.md          # 9856a39
git log -1 --format=%h -- docs/spec/2026-08-11-tnec-application-unit-book-admission.md                 # d692c2c

# No registry / CATALOG mutation in this pass
git diff --name-only
# Expected: docs/briefs/Q-TXG-1-ha-reargument.md · STATE.md · docs/SESSIONS.md only
```

---


---

## §-ruling — operator election (A) CLOSE

**Elected:** **(A) CLOSE** — lane FALSIFIED-at-walls  
**Date:** 2026-08-12  
**Authority:** operator chat election ("A") on the A/B/C gate in §6 of this packet  
**Not elected:** B HOLD · C CONTINUE  

**Effect:**
- Transfer/expression lane closed at the composition of the frozen per-trade cost floor and the trailing-DD survival ceiling (see §3).
- No further Q-TXG-1 cell election; no ATR-median unlock campaign under this Q-ID.
- Registry row filed under `docs/rejected_candidates.md` with the re-proposal bar below.
- CATALOG / GRID RESULTS / STATE / INDEX updated by the ruling commit.

**Re-proposal bar (binding):** new mechanism evidence with a **demonstrably different loss-side shape**, or a **venue class whose survival geometry differs** (not an EOD-trailing prop clone) — **not** new cells, new instruments, or ATR-input spend alone.

**TNEC-AU-1 note:** any future re-proposal is adjudicated under whatever application-unit regime is then in force (§8).

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-12 | Packet authored; A/B/C proposed; lean A-or-B; ruling pending | Cursor (operator-directed) |
| 2026-08-12 | Operator elected **(A) CLOSE**; status → `CLOSED — FALSIFIED-at-walls`; lane closure + registry | Cursor (operator-directed) |
