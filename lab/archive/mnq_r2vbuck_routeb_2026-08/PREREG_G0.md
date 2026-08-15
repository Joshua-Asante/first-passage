# Q-R2VBUCK-1 — Route B G0 charter (FROZEN shape; G2 COMPLETE)

**Status:** `FROZEN G0 · G2 COMPLETE 2026-08-08 — FALSIFIED` — schema×window×catalogue frozen. **Empty candidates → STOP this catalogue.** Cap seat not claimed. CONFIRM reserved, unread.
**Date:** 2026-08-08
**Parent brief:** [`docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md`](lab/archive/../../../docs/briefs/Q-R2VBUCK-1-volume-bucket-aggressor-route-b-scoping.md)
**Route:** Avenue A **Route B** ([`ADR`](lab/archive/../../../docs/adr/2026-08-05-avenue-a-generate-confirm-route.md) `Accepted`)
**Screen:** EM0–EM5 + MNQDTL D1/D2 as **class** attestation ([`EM`](lab/archive/../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md) · [`MNQDTL-1`](lab/archive/../../../docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) `RATIFIED`) — applied **before** this freeze (§2.0a)
**SPEC S6:** [`admission_s6.json`](admission_s6.json) + [`ADMISSION_S6_LOG.md`](ADMISSION_S6_LOG.md) — `evaluate_admission` **ADMIT** 2026-08-08 (`catalogue_k=1`, floor 0.650, power 0.9988 ≥ 0.50). First campaign under the schema.
**Cost so far:** **$0.0000**. EXPLORATION bytes = reuse of OFCHAN cache (no new pull). Explore GO paid 2026-08-08 (cache reuse only).
**`K_intrinsic = 1`** (catalogue size). Cap 1.0 → DSR floor **0.650**, headroom **0.350**.
**Confirm-budget M = 1** (frozen here) — **moot** (no candidates).
**Cap seat:** **not claimed** at G0/G2.
**Confirm $ budget (pre-registered):** **USD 50.00** — unused (CONFIRM unread).

G2 artifacts: [`RESULTS_g2.md`](RESULTS_g2.md) / [`RESULTS_g2.json`](RESULTS_g2.json).

---

## Amendment log

- **2026-08-08 — Explore GO RATIFIED (operator) + G2 COMPLETE → `FALSIFIED` (empty candidates).** Operator explore GO under MNQDTL **R2** (cache reuse only; no new pull). Runner `run_r2vbuck_g2.py` + `r2vbuck_lib.py` scored C1 on EXPLORATION only. n_retained **77,656** / eligible **77,656** = **100%** (coverage PASS; power PASS). ρ **−0.005478** · CI95 **[−0.016881, +0.005984]** includes 0 · \|ρ\| < placebo p95 **0.007958**. Candidate list **[]**. CONFIRM untouched. Cap seat not claimed. G3 disposition: **STOP** this G0 catalogue (new campaign required to reopen).

---

## §0 — Rule-0 / cheap falsifier (parent-side, 2026-08-08)

| Check | Result |
|---|---|
| OFCHAN EXPLORATION cache present | 155 `*.tbbo.dbn.zst` at `~/.databento_cache/q_ofchan_1_exploration_tbbo/GLBX-20260807-EHX5KUSF7K/` |
| Sample day `2026-02-06` columns | `action,side,price,size,bid_px_00,ask_px_00,…` — **mid computable**; all rows `action=T` |
| Mid target on `tbbo` | **OK** (no `trades`-first ladder) |
| Outside-window bucket census | `ohlcv-1m` from `lab/archive/mnq_selection_ceiling_2026-08/_mnq_1m.parquet`, RTH Mon–Fri 09:30–15:59 ET, **2025-01-02 → 2025-06-30** (outside CONFIRM+EXPLORATION) → volume median **2540.5** → **B = 2550** (nearest 50) |
| S6 admission | ADMIT (see `admission_s6.json`) |

**OFCHAN coverage pathology (motivation, not a retune):** VOID-COVERAGE 7.36% driven by flicker filter needing ≥5 same-sign TBBO updates in 1 s at each *clock minute* on trade-tagged TBBO ([`RESULTS_g2`](lab/analysis/c1/mnq_ofchan_routeb_2026-08/RESULTS_g2.md)). Volume-bucket sampling removes minute-grid denseness as the coverage driver.

---

## §1 — Windows (non-overlapping; CONFIRM = fresh holdout)

| Window | ISO bounds (UTC dates; `--end` exclusive) | Role |
|---|---|---|
| **CONFIRM** | **2025-09-01 → 2026-02-06** | **Fresh** reserved holdout (not OFCHAN’s 2025-08-06→2026-02-06). No exploration score may use it. Cells-examined-against-this-holdout at G0: **0**. |
| **EXPLORATION** | **2026-02-06 → 2026-08-06** | Sole window for Stage-G. **Bytes = OFCHAN cache reuse** (same interval). |

**Holdout adjudication (Avenue A checklist):** OFCHAN stopped at G2 with CONFIRM unread — but a second catalogue against the *same* reserved interval would accumulate cells-examined. This campaign uses a **shifted CONFIRM** (fresh holdout). Disclose: cells-examined-against-OFCHAN’s old holdout remains **1** (OFCHAN C1 only); this CONFIRM starts clean.

- Symbol / stype: `MNQ.v.0`, continuous
- Schema: **`tbbo` only** (no `trades` / `mbp-10` / `mbo` in this campaign)
- Parent→micro: micro economics only; no NQ/ES cross-book cells

---

## §2 — Catalogue (size 1 → `K_intrinsic = 1`)

### Cell C1 — volume-bucket aggressor imbalance → 60 s mid return

| Element | Frozen definition |
|---|---|
| Bucket size **B** | **2550** contracts (outside-window RTH 1m volume median 2540.5, rounded nearest 50; census window 2025-01-02→2025-06-30 on selection-ceiling `ohlcv-1m` panel) |
| Sampling | Walk RTH trade prints (`action=T`) in time order. Accumulate `size` into the current bucket. When cumulative size reaches **B**, close the bucket; sample time `t` = timestamp of the completing trade. Start next bucket with remainder size if any. |
| Feature `A` | Inside the closed bucket: signed aggressor size imbalance. Using TBBO `side`: treat `B` as buy aggressor, `A` as sell aggressor (Databento convention). `A = (buy_sz − sell_sz) / (buy_sz + sell_sz)`. Drop bucket if `buy_sz + sell_sz == 0` (should not occur). |
| Target | Mid return over **[t, t+60s)`**: `r = (mid_{t+60s−} − mid_t) / mid_t` where `mid = (bid_px_00 + ask_px_00) / 2`, using last TBBO quote ≤ each endpoint (at print `t`, use that row’s BBO). Horizon **60 s ≥ 5 s** floor. |
| RTH | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET**; drop holiday / early-close sessions lacking a full RTH (pre-register CME calendar exclusions at harness time; do not drop after seeing returns). |
| Unit of analysis | One retained `(A, r)` pair per completed eligible bucket. |
| Statistic (promotion) | Pearson correlation `ρ(A, r)` on EXPLORATION retained pairs; **session-block bootstrap** 95% CI, **10,000** reps, seed **20260808**; within-session **label-shuffle placebo** on `r`, **1,000** reps, same seed; two-sided \|ρ\| vs placebo p95. |
| Sign / CI limb | CI excludes 0 |
| Placebo limb | \|ρ\| > placebo \|.\| p95 |
| Halves | Split EXPLORATION session-dates into older/newer halves; disagree on `sign(ρ)` → **AMBIGUOUS-HOLD** (do not promote) |
| Magnitude floor | **AMBIGUOUS-HOLD** if CI/placebo clear but \|ρ\| **< 0.02** |
| **Eligible** | Completed volume-buckets whose end time `t` is inside RTH **and** valid mid exists at `t` and at `t+60s−` |
| **VOID-COVERAGE** | retained / eligible **< 90%** → `VOID-COVERAGE` |
| **VOID-POWER** | retained **n < 2,000** → `VOID-POWER` (evaluated before ρ) |

**Naming:** this is **volume-bucket sampling**, not an MNQSEL **restart clock** (event-window construct). Different object.

**C9 clearance (quote):** MNQFLOW-1 DEAD re-proposal bar requires *"a named feature that is **not** top-of-book size imbalance, **or** a cohort-cited futures-native order-flow δ … — **not** a horizon re-cut, a threshold on `I`, more days of the same feature, or a hop to MNQ's own book for a different tick grid."* Signed **trade** (aggressor) imbalance clears limb 1 — tape aggressor, **not** resting ToB size imbalance (OFCHAN / MNQFLOW cheapest swing).

**Depth-census disclosure (transfers):** L1 total p05/p50/p95 ≈ **2/7/17**, 99.98% tied (MNQFLOW re-aim). Feature here is a **window aggregate** over B contracts of tape, not a per-quote resting-size predictor.

**Forbidden inside the cell:** ORB timestamps; outcome joins (R, win/loss, MFE/MAE); flicker-filter retune of OFCHAN C1; resting ToB size imbalance; MNQSEL restart-clock selection / completed-window ranking; bars-only S/R; ICT/ORB gates; N14/Cap tripwire as filter; ES/NQ parent features; schema other than `tbbo`; reading any CONFIRM quote for exploration metrics; D1/D2 μ scoring inside G2.

---

## §3 — Promotion rule (EXPLORATION only)

Promote C1 to "candidate" iff, **on EXPLORATION only**:

1. Not VOID-POWER / VOID-COVERAGE
2. Bootstrap CI for ρ excludes 0
3. \|ρ\| beats placebo p95
4. Halves agree on sign
5. \|ρ\| ≥ 0.02

Else: empty candidate list (or AMBIGUOUS-HOLD). **Do not** treat promotion as edge, admission, harvest PASS, or strategy.

---

## §4 — Confirm budget / Cap gate / Stage-C pointer

- **M = 1** — at most one candidate confirmed this campaign.
- **Cap-seat reservation (operator)** required **after G3 (≥1 candidate) and before any C0 score**. Without reservation → STOP at candidates (MNQDTL §4).
- C0 confirmatory PREREG (not authored this session) must restate CONFIRM window **2025-09-01 → 2026-02-06**, identical or stricter limbs, M=1, and the confirm $ budget.
- Ordering trap: any CONFIRM metric before C0 commit **voids** confirm — new campaign required.
- Do **not** re-cut CONFIRM after G2.

---

## §5 — EM / MNQDTL attestation (re-derived at K=1)

`P U U D D D` + D1/D2 class True —

| Limb | Attestation |
|---|---|
| EM0 | **PASS** — catalogue_k=1 ≤ 3; S6 ADMIT |
| EM1 | **U** — SHAPE-UNSCREENABLE until tradeable stop/R exists |
| EM2 | **U** — same |
| EM3 | **D** — independence + hard stops required at construct time |
| EM4 | **D** — weekly idle cleared by design if buckets fire on most RTH days (not a G2 gate) |
| EM5 | **D** — RTH session/slot legal on Tradeify Select |
| D1/D2 | **True as target class** (MNQDTL) — **not** G2 promotion gates |

Not SHAPE-CLEAR. Screen the class, not a winner.

---

## §6 — Explore path (after operator GO)

1. Operator explore GO: **cache reuse only** — no new Databento pull for EXPLORATION.
2. G2: score C1 on EXPLORATION only; emit candidate list (may be empty).
3. G3: empty → STOP catalogue; ≥1 → Cap reservation → C0 (separate packet).

---

## §7 — Economic honesty (not a promotion gate)

- **MNQSEL** oracle top-1/day &lt; 0.40R applies to **restart-clock event windows**, not this volume-bucket aggressor→mid universe — different candidate set; not a universal ceiling.
- **K-wall** viable stop band **5–20 pt** implies ~**3–9 pt** predicted directional edge per trade to matter under EM1 economics. A bare \|ρ\| ≥ 0.02 limb is an association floor only; converting ρ into points requires the realized σ of 60 s mid returns on the EXPLORATION panel (disclose at G2; do not amend promotion limbs post-hoc).
