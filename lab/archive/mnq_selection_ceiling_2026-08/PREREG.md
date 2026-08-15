# `Q-MNQSEL-1` Phase 0 — VERDICT PRE-REGISTRATION: selection-value ceiling on MNQ

**FROZEN ON THIS FILE'S INTRODUCING COMMIT. No candidate-path PnL may be computed before
freeze. Zero path outcomes have been computed at freeze time.**

**Parent:** [`Q-MNQSEL-1` scoping](lab/archive/../../../docs/briefs/rnd-pipeline/Q-MNQSEL-1-selection-value-ceiling-scoping.md).
**Purpose:** bound whether **perfect take/skip (top-k) among causal restart-clock candidates**
can clear EM1 (≥0.40R net) on at least one direction arm — before any feature catalogue or
Route B campaign is opened. Same epistemic class as Step 1's event ceiling: a FAIL is
conclusive; a PASS licenses only an ITERATE to approximate the oracle, never a candidate.
**K:** `0` — one-way bounding measurement, no GO state (§5). **Cost:** `$0.00` (MNQ 1m on disk).
**No manifest. No Cap seat.** **Class:** order-free, mechanism-free, strategy-free.
**Authored:** 2026-08-07 · Cursor (Composer), operator-directed plan execute.

---

## §0 — Rule 0 reads (verified this session 2026-08-07)

- **[`core/firm_rules.py`](lab/archive/../../../core/firm_rules.py) `Tradeify_Select_100K` @ `83b665d`** — live geometry: `max_dd_pct 3.0`, `profit_target_pct 6.0`, `cost_per_side_usd 0.91`, `inactivity_max_idle_days 5`, `micro_contract_cap 80`, `daily_loss_pct None`, `dd_lock_offset_usd` unreachable (1_000_000). Asserted this session via live dict.
- **[`lab/analysis/c1/mnq_event_ceiling_2026-08-04/PREREG.md`](lab/analysis/c1/mnq_event_ceiling_2026-08-04/PREREG.md) @ `1eeb35c`** — greedy disjoint-window construction, session cut, roll exclusion, `G(s) = 0.40·s + 1.41`. **Reused unmodified** for restart clocks; this file does not re-derive the count.
- **[`lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md`](lab/analysis/c1/mnq_event_ceiling_2026-08-04/RESULTS.md) @ `5e83949`** — N11: median **145**/day at `s=40` / `G=17.41`; bottleneck relocated to selection.
- **[`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](lab/archive/../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md) @ `d08537a`** — EM1 ≥0.40R; EM3 independence; EM4 weekly; EM0 catalogue wall.
- **[`lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md`](lab/analysis/c1/eval_inverse_requirements_2026-08-03/RESULTS.md) @ `d08537a`** — 0.40R inversion; rope arithmetic.
- **[`ops/instruments/MNQ.md`](lab/archive/../../../ops/instruments/MNQ.md) @ `a4b36f8`** — `$2.00/pt`; N11 · N13 · F2 GUARD; Cap seat spent (N16).
- **[`docs/briefs/closures/MNQBASE-1-closure-intake-dry.md`](lab/archive/../../../docs/briefs/closures/MNQBASE-1-closure-intake-dry.md) @ `d08537a`** — STOP; re-proposal = **new sourcing channel** (this measurement is that channel's Phase 0, not a harvest re-pass).
- **[`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md) @ `87b0547`** — Route B working budget K=1–2 if ITERATE fires.

**Gitignore pre-flight.** No Pine read or cited. No Databento pull. No TBBO/MBP.

---

## §1 — What is being measured, and why it is a ceiling

**The quantity.** Reuse Step 1's greedy partition at **`s = 40` only** (`G = 17.41`). Each
**restart clock** — session first bar, and the bar immediately after each completed window
(`restart at j+1` per Step-1 §2) — is a **causal candidate entry**. At each clock, simulate a
hypothetical independent hard-stopped trade (long arm and short arm **separately**):

- Entry: **open** of the restart bar
- Stop: `s = 40` pt adverse
- Target: `G = 17.41` pt favorable
- Flat: **16:00 ET** (EM5 / envelope E1 default), forced exit at that bar's close if neither
  stop nor target hit
- Cost: Tradeify round-trip **1.41 pt** (`2 × 0.91 / $2.00/pt`), subtracted from realized
  points before converting to R (`R = (pts − 1.41) / s`)

**Why restart clocks are causal.** The clock is known when the prior window completes (or at
session open). No future path is required to *name* the candidate. Completed-window identity
is **not** a feature and is never scored as a selectable label.

**Why this is a strict upper bound on selection value.** Oracle top-k and oracle take/skip
use perfect foresight of each candidate's realized path outcome. No live rule can beat that
information set on the same candidate set. A FAIL (oracle cannot clear EM1) is conclusive for
this universe. A PASS says only that *some* selection rule *might* exist — it licenses an
ITERATE to approximate the oracle, never a strategy.

**What it deliberately is not.** Not a feature hunt, not Route B, not a deployable selector,
not a ranking of completed Step-1 windows (that ranking is look-ahead — REFUTED in the parent
brief). Not MNQDTL-bound.

**Anti-tautology note.** Under `G(s) = 0.40·s + 1.41`, a clean target-hit earns ≈0.40R net by
construction. Therefore **mean R of the subset {candidates with R ≥ 0.40}** is tautological
whenever that subset is non-empty. **It is not a primary gate.** Primary gates use
**oracle top-k/day mean R** (which can fail if the day's best path is still &lt; 0.40R) and
**all-take / random baselines**.

---

## §2 — Frozen construction

**Data.** `MNQ.v.0` continuous 1m, databento GLBX.MDP3, on disk at `$0.00` — same panel class
as Step 1.

**Session window.** **18:00 ET (prior calendar day) → 16:00 ET**, keyed by 16:00 ET close date.
Score only sessions with ≥ 60 one-minute bars. **Roll exclusion:** `in_roll_window` (±4 days
of the 3rd Friday of Mar/Jun/Sep/Dec) at session level — inherited unmodified from
[`build_w_export.py`](lab/archive/../ict_mnq_2026-08/build_w_export.py).

**Cell.** Exactly one stop: **`s = 40`**, **`G = 17.41`**. No grid search (FM-2).

**Path resolution (bar order, frozen).** Within each bar after entry, evaluate in this order:
(1) if bar range touches stop level → stop out at −`s` pts gross; (2) else if bar range touches
target → exit at +`G` pts gross; (3) else continue. Same-bar stop-and-target: **stop wins**
(adverse assumption). Forced flat at 16:00: mark-to-close of the 16:00 bar.

**Arms.** Long and short are separate populations. Never pool into one mean for a gate.

**Oracle / baseline statistics (all pre-registered; report all; gates in §4):**

| ID | Statistic | Definition |
|---|---|---|
| **S1** | All-take mean R | Mean R of taking **every** restart-clock candidate on that arm |
| **S2** | Random-1/day mean R | Each session, pick one candidate uniformly at random; mean R across sessions (seed frozen in runner; 10,000 reps for CI optional disclosure only — gate uses the single frozen seed mean) |
| **S3** | Oracle top-1/day mean R | Each session, pick the candidate with **highest realized R** on that arm; mean across sessions |
| **S4** | Oracle top-2/day, top-3/day mean R | Same as S3 with k∈{2,3}; if fewer than k candidates that session, take all |
| **S5** | Target-hit density | Median across sessions of count of candidates with target-before-stop (gross +G before −s) |
| **S6** | Sessions with ≥1 target-hit | Fraction of scored sessions with ≥1 target-hit candidate |

**R definition.** `R = (realized_pts − 1.41) / 40`. Realized_pts ∈ {+G, −s, flat_pts}.

---

## §3 — Question

**Symptom-only:** MNQ offers ~145 independent G-windows/day at a holdable stop, yet every
sourced construct and the incumbent book fire near zero; harvest intake is dry. Nobody has
measured whether **perfect selection among causal entry clocks** can clear the EM1 floor.

**Q-MNQSEL-1 (Phase 0):** On the frozen restart-clock candidate set at `s=40`, does oracle
top-1/day mean net R clear **≥ 0.40** on at least one arm while all-take stays below 0.40 —
i.e. is selection value the binding residual — or is even perfect selection insufficient?

---

## §4 — Falsifiable hypothesis

**H-SEL-1.** On at least one arm (long or short), **oracle top-1/day mean net R (S3) ≥ 0.40**,
**and** **all-take mean R (S1) &lt; 0.40**.

**Falsifier — frozen trigger table.**

| # | Trigger | Threshold | Verdict |
|---|---|---|---|
| C1 | scored sessions | **&lt; 250** | **`INSUFFICIENT-N`** |
| C2 | S3 &lt; 0.40 on **both** arms | — | **`FALSIFIED` / STOP** — selection cannot mint EM1 edge on this universe |
| C3 | S1 ≥ 0.40 on **any** arm | — | **`SURPRISE-DIRECTION`** — direction bias without selection; **not** a selector win; do not open a feature campaign under "selection" framing |
| C4 | S3 ≥ 0.40 on ≥1 arm **and** S1 &lt; 0.40 on that arm | — | **`RESOLVED` / ITERATE** — licenses a Route B **K_intrinsic=1–2** feature campaign to approximate oracle (separate GO; Cap seat not claimed) |

**Precedence:** C1 → C3 → C2 → C4. If C3 fires on an arm, that arm is removed from C4 eligibility;
if the other arm still clears C4, ITERATE may proceed on the non-surprise arm only.

**S4 / S5 / S6** are **reported**, not gated. They inform cadence (EM4) and top-k sensitivity
for any successor packet; they do not move the Phase-0 verdict.

**Pre-registered expectation.** Most likely branch: **C4** — oracle top-1 clears because
target-hits exist among ~145 clocks (S5/S6 high), while all-take fails because most clocks
are noise. Second most likely: **C2** if restart clocks are path-misaligned with the
range-count construction (entry-at-open after completion does not inherit the completed
window's direction). Recorded before running.

---

## §5 — Forbidden moves

- **FM-1 — Ranking completed Step-1 windows or using completed-window labels as features.** Look-ahead; REFUTED as a live selector.
- **FM-2 — Expanding the `s`/`G` grid after seeing outcomes.** Cell is `s=40` only.
- **FM-3 — Using mean R of {R ≥ 0.40} as a primary gate.** Tautological under G construction (§1).
- **FM-4 — ORB filter slices / F2 GUARD laundering** (Friday / Monday / OR-hi / same_bar).
- **FM-5 — Binding MNQDTL D1/D2** into Phase 0 gates.
- **FM-6 — TBBO/MBP pull, Cap-seat claim, Pine, rail, `core/`, lock, allocation, `dd_protection`, lifecycle, `LEG_MAP`.**
- **FM-7 — Editing Step-1 PREREG/RESULTS** to rescue a FAIL here.
- **FM-8 — Reading `RESOLVED` as a candidate or edge.** ITERATE only; feature campaign needs a fresh G0 + explore GO.
- **FM-9 — Pyramiding / scale-ins / same-signal multi-entry** in any path model (EM3).
- **FM-10 — Pooling long and short into one gated mean.**

---

## §6 — Gate criteria and typed dispositions

| Verdict | Trigger | **Disposition (pre-registered)** |
|---|---|---|
| `INSUFFICIENT-N` | C1 | **STOP** — panel too short; should not fire on the Step-1 panel |
| `FALSIFIED` | C2 | **STOP** this universe. Re-proposal bar: a **different causal candidate set** (not denser OF on the same clocks; not completed-window ranking) |
| `SURPRISE-DIRECTION` | C3 (and C4 not cleared on the other arm) | **ITERATE → Investigate** under a direction-bias framing, **not** a selector framing. Packet: S1/S3/S5/S6 both arms |
| `RESOLVED` | C4 | **ITERATE → Route B K=1–2 feature campaign** approximating oracle on the clearing arm(s). Entry packet: this PREREG + RESULTS tables S1–S6; EM0–EM5 bind at G0; Cap seat not claimed. **Names no feature and no candidate** |

**Board write** owed at closure in all branches.

---

## §10 — Audit hooks (runnable)

```bash
# Freeze ordering must be git-auditable: this file's commit precedes RESULTS.md's.
git log --format="%h %cs" -- lab/archive/mnq_selection_ceiling_2026-08/PREREG.md
git log --format="%h %cs" -- lab/archive/mnq_selection_ceiling_2026-08/RESULTS.md

# Cost basis and point value (expect 0.91; $2.00/pt in ledger):
python -c "import sys;sys.path.insert(0,'.');from core import firm_rules as F;print(F.FIRM_RULES['Tradeify_Select_100K']['cost_per_side_usd'])"
rg -n "\\$2\\.00/pt" ops/instruments/MNQ.md

# G(s)=0.40*s+1.41 at s=40 equals 17.41 — pin to Step-1 PREREG:
rg -n "17\\.41|0\\.40 · s|0\\.40·s" lab/analysis/c1/mnq_event_ceiling_2026-08-04/PREREG.md

# Primary gate is S3 (top-1/day), not filtered mean R≥0.40:
rg -n "Oracle top-1/day|tautolog" lab/archive/mnq_selection_ceiling_2026-08/PREREG.md

# No look-ahead completed-window ranking as candidate definition:
rg -n "restart clock|completed-window" lab/archive/mnq_selection_ceiling_2026-08/PREREG.md

# No manifest / K / Cap for this measurement (expect 0):
rg -icE "mnqsel|selection_ceiling" discovery_manifests/ || true
```

---

## Amendment log (append-only)

- **2026-08-07 — FROZEN** on this file's introducing commit. No path PnL existed at freeze.
  Primary gate is oracle **top-1/day** mean R (anti-tautology vs mean of R≥0.40 subset under
  G construction). Naïve completed-window ranking explicitly forbidden (FM-1).
