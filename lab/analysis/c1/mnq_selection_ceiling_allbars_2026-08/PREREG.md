# `Q-MNQSEL-2` Phase 0 — VERDICT PRE-REGISTRATION: selection ceiling on dense RTH 1m opens

**FROZEN ON THIS FILE'S INTRODUCING COMMIT. No candidate-path PnL may be computed before
freeze. Zero path outcomes have been computed at freeze time (cheap falsifier = clock count
+ R arithmetic only — see [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md)).**

**Parent:** [`Q-MNQSEL-2` scoping](../../../../docs/briefs/rnd-pipeline/Q-MNQSEL-2-dense-1m-selection-ceiling-scoping.md).
**Purpose:** bound whether **perfect take/skip (top-k) among causal dense RTH 1m bar-open
candidates** at frozen stop **G=10 pt** (1R target = G) can clear EM1 (≥0.40R net) on at
least one direction arm — before any feature catalogue or construct. Successor to
`Q-MNQSEL-1` (restart clocks at s=40 **FALSIFIED**); this universe was explicitly unbound.
**K:** `0` — one-way bounding measurement. **Cost:** `$0.00` (MNQ 1m on disk).
**No manifest. No Cap seat.** **Class:** order-free, mechanism-free, strategy-free.
**Authored:** 2026-08-08 · Cursor; absolute-path plan execute.

---

## §0 — Rule 0 reads (verified 2026-08-08)

- **[`core/firm_rules.py`](../../../../core/firm_rules.py) `Tradeify_Select_100K` @ `45e3cea`** — rope/target/idle/cap/cost; RT → 1.41 pt at $2/pt.
- **[`lab/archive/mnq_selection_ceiling_2026-08/{PREREG,RESULTS}.md`](../../../archive/mnq_selection_ceiling_2026-08/RESULTS.md)** — restart-clock universe FALSIFIED; re-proposal = different causal set; all-bars unbound (§4).
- **[`docs/spec/2026-08-05-eval-mechanism-shape-screen.md`](../../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md)** — EM1 ≥0.40R; EM3 independence; EM5 flat.
- **[`lab/analysis/c1/catalogue_k_wall_2026-08-05/RESULTS.md`](../catalogue_k_wall_2026-08-05/RESULTS.md)** — MNQ stop band **5–20 pt**.
- **[`docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md`](../../../../docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md)** — MNQDTL R2 live; Cap reservation separate.
- **[`ops/instruments/MNQ.md`](../../../../ops/instruments/MNQ.md)** — $2.00/pt; F2 GUARD; Cap spent (N16).
- **Cheap falsifier** — [`ADMISSION_FALSIFIER_LOG.md`](ADMISSION_FALSIFIER_LOG.md) OK.

**Gitignore pre-flight.** No Pine. No Databento pull. No TBBO/MBP.

---

## §1 — What is being measured

**Candidate clocks:** every CME equity-index **RTH** Mon–Fri **09:30–15:59 ET** completed
1-minute bar open on `MNQ.v.0`. Causal: named at bar open without path foresight.

**Trade geometry (gate cell):**

- Entry: **open** of the clock bar
- Stop: **G = 10.0** pt adverse
- Target: **G = 10.0** pt favorable (1R)
- Flat: last in-session RTH bar close (sessionize drops bars outside 09:30–15:59)
- Cost: Tradeify RT **1.41** pt; `R = (pts − 1.41) / 10`
- Same-bar stop-and-target: **stop wins**

**Diagnostics (pre-registered, not gate limbs):** same construction at **G=5** and **G=20**.
Reported for disclosure only; do not retune the gate after seeing them.

**Why a ceiling.** Oracle top-k uses perfect foresight of each candidate's path. FAIL is
conclusive for this universe. PASS licenses only ITERATE toward approximating the oracle /
construct design — never a candidate by itself.

---

## §2 — Frozen construction

**Data.** Same panel class as MNQSEL-1: `ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn` → local
`_mnq_1m.parquet` (gitignored).

**Session key.** RTH session date = ET calendar date of the 09:30–15:59 block. Score sessions
with ≥ 60 RTH bars. **Roll exclusion:** `in_roll_window` (±4 days of 3rd Friday Mar/Jun/Sep/Dec)
inherited from [`build_w_export.py`](../../_inbox/ict_mnq_2026-08/build_w_export.py).

**Arms.** Long and short separate. Never pool for a gate.

**Statistics S1–S6** — identical definitions to MNQSEL-1 PREREG §2, applied to dense clocks:

| ID | Statistic |
|---|---|
| S1 | All-take mean R |
| S2 | Random-1/day mean R (seed **20260808**) |
| S3 | Oracle top-1/day mean R (**primary**) |
| S4 | Oracle top-2 / top-3/day mean R |
| S5 | Median target-hit count/session |
| S6 | Fraction sessions with ≥1 target-hit |

---

## §3 — Question

**Q-MNQSEL-2 (Phase 0):** On dense RTH 1m bar-open candidates at G=10 (1R target), does
oracle top-1/day mean net R clear **≥ 0.40** on ≥1 arm while all-take stays **&lt; 0.40**?

---

## §4 — Falsifiable hypothesis

**H-SEL-2.** On ≥1 arm: **S3 ≥ 0.40** and **S1 &lt; 0.40**.

**Triggers (precedence C1 → C3 → C2 → C4):**

| Code | Condition | Verdict |
|---|---|---|
| C1 | n_sessions &lt; 250 | `INSUFFICIENT-N` |
| C3 | S1 ≥ 0.40 on an arm and no non-surprise C4 arm | `SURPRISE-DIRECTION` |
| C2 | S3 &lt; 0.40 on **both** arms | `FALSIFIED` — STOP this universe |
| C4 | S3 ≥ 0.40 and S1 &lt; 0.40 on ≥1 non-surprise arm | `RESOLVED` — selection headroom exists; construct ITERATE licensed |

---

## §5 — Forbidden moves

- Restart-clock re-run / s=40 retune (MNQSEL-1 closed).
- Completed-window ranking (look-ahead).
- OF features; Cap claim; Route B catalogue from this file alone.
- Promoting G=5/20 diagnostics into the gate after seeing numbers.
- ORB filter laundering (F2 GUARD).
- Pine / rail / deployment / Striker redeploy.

---

## §6 — Disposition

- `RESOLVED` → board: construct packet (`Q-MNQDTL-CON-1`) unpaid until operator GO.
- `FALSIFIED` → STOP dense-bar selection; re-proposal = yet another causal set.
- Diagnostics G=5/20 never move the gate.

---

## Amendment log

- **2026-08-08 — G0/Phase-0 FROZEN.** Absolute-path plan; explore/path PnL unpaid until this commit lands.
