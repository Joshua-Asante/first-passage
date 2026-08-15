# Q-R2AGRUN-1 — Route B G0 charter (FROZEN shape; explore GO unpaid)

**Status:** `FROZEN G0 · G2 COMPLETE 2026-08-08 — AMBIGUOUS-HOLD` — schema×window×catalogue frozen. **Empty candidates → ITERATE (magnitude floor).** Cap seat not claimed. CONFIRM reserved, unread.
**Date:** 2026-08-08
**Parent brief:** [`docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md`](../../../../docs/briefs/Q-R2AGRUN-1-aggressor-run-length-route-b-scoping.md)
**Route:** Avenue A **Route B** ([`ADR`](../../../../docs/adr/2026-08-05-avenue-a-generate-confirm-route.md) `Accepted`)
**Screen:** EM0–EM5 + MNQDTL D1/D2 as **class** attestation ([`EM`](../../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md) · [`MNQDTL-1`](../../../../docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md) `RATIFIED`) — applied **before** this freeze (§2.0a)
**SPEC S6:** [`admission_s6.json`](admission_s6.json) + [`ADMISSION_S6_LOG.md`](ADMISSION_S6_LOG.md) — `evaluate_admission` **ADMIT** 2026-08-08 (`catalogue_k=1`, floor 0.650, power 0.9988 ≥ 0.50).
**Cost so far:** **$0.0000**. EXPLORATION bytes = reuse of OFCHAN cache (no new pull). Explore GO paid 2026-08-08 (cache reuse only).
**`K_intrinsic = 1`** (catalogue size). Cap 1.0 → DSR floor **0.650**, headroom **0.350**.
**Confirm-budget M = 1** (frozen here) — **moot** (no candidates).
**Cap seat:** **not claimed** at G0/G2.
**Confirm $ budget (pre-registered):** **USD 50.00** — unused (CONFIRM unread).

G2 artifacts: [`RESULTS_g2.md`](RESULTS_g2.md) / [`RESULTS_g2.json`](RESULTS_g2.json).

---

## Amendment log

- **2026-08-08 — Explore GO RATIFIED (operator) + G2 COMPLETE → `AMBIGUOUS-HOLD` (empty candidates).** Operator explore GO under MNQDTL **R2** (cache reuse only; no new pull). Runner `run_agrun_g2.py` + `agrun_lib.py` scored C1 on EXPLORATION only. n_retained **22,304,297** / eligible **22,304,297** = **100%**. ρ **−0.001306** · CI95 **[−0.002589, −0.000020]** excludes 0 · \|ρ\| > placebo p95 **0.000398** · halves agree · \|ρ\| **< 0.02** magnitude floor → **AMBIGUOUS-HOLD**. Candidate list **[]**. CONFIRM untouched. Cap seat not claimed. G3 disposition: **ITERATE** (do not score CONFIRM; no post-hoc floor retune).
- **2026-08-08 — Explore GO RATIFIED (operator) — cache reuse only; G2 in flight.** No new Databento pull. CONFIRM untouched.
- **2026-08-08 — G0 FROZEN.** Catalogue / windows / promotion limbs locked. Explore GO unpaid. No G2 score exists.

---

## §0 — Rule-0 / cheap falsifier (parent-side, 2026-08-08)

| Check | Result |
|---|---|
| OFCHAN EXPLORATION cache present | 155 `*.tbbo.dbn.zst` at `~/.databento_cache/q_ofchan_1_exploration_tbbo/GLBX-20260807-EHX5KUSF7K/` |
| Sample day columns | `action,side,price,size,bid_px_00,ask_px_00,…` — **mid computable**; rows `action=T`; sides `B`/`A` |
| Mid target on `tbbo` | **OK** (no `trades`-first ladder) |
| `N_min` | **2** a priori / definitional (a singleton is not a run). **Not** fit from EXPLORATION. Structural sanity only (run formation works; mid finite) disclosed without freezing any EXPLORATION-derived length threshold |
| S6 admission | ADMIT (see `admission_s6.json`) |

**Why not R2VBUCK retune:** R2VBUCK tested **signed aggressor size imbalance inside volume buckets**. This cell tests **signed length of maximal same-side aggressor runs** (herding/exhaustion object). Different feature; same schema/window reuse.

---

## §1 — Windows (non-overlapping; CONFIRM = fresh holdout)

| Window | ISO bounds (UTC dates; `--end` exclusive) | Role |
|---|---|---|
| **CONFIRM** | **2025-09-01 → 2026-02-06** | **Fresh** reserved holdout (same shifted holdout as R2VBUCK — not OFCHAN’s older half). No exploration score may use it. Cells-examined-against-this-holdout at G0: **0**. |
| **EXPLORATION** | **2026-02-06 → 2026-08-06** | Sole window for Stage-G. **Bytes = OFCHAN cache reuse** (same interval). |

**Holdout adjudication:** OFCHAN + R2VBUCK both stopped at G2 with CONFIRM unread on their respective reserved intervals. This campaign reuses R2VBUCK’s **shifted CONFIRM** (still unread). Disclose: cells-examined-against OFCHAN’s old holdout remains OFCHAN-only; against this CONFIRM interval remains **0** at G0 (R2VBUCK never scored it).

- Symbol / stype: `MNQ.v.0`, continuous
- Schema: **`tbbo` only** (no `trades` / `mbp-10` / `mbo` in this campaign)
- Parent→micro: micro economics only; no NQ/ES cross-book cells

---

## §2 — Catalogue (size 1 → `K_intrinsic = 1`)

### Cell C1 — signed aggressor-run trade-count → 60 s mid return

| Element | Frozen definition |
|---|---|
| Run | Maximal contiguous sequence of RTH `action=T` prints with the same aggressor `side ∈ {B,A}` in time order. A print with `side=N` (or any non-`B`/`A`) **breaks** the current run without starting a new one. |
| `N_min` | **2** — retain a run only if its trade-count ≥ 2. A priori / definitional. |
| Completion time `t` | Timestamp of the **last** trade in the run (the print immediately before a side flip, an `N` break, or RTH end). |
| Feature `A` | `A = +n_trades` if run side is `B` (buy aggressor); `A = −n_trades` if run side is `A` (sell aggressor). Trade-count only — **not** size-sum imbalance, **not** resting ToB size. |
| Target | Mid return over **[t, t+60s)`**: `r = (mid_{t+60s−} − mid_t) / mid_t` where `mid = (bid_px_00 + ask_px_00) / 2`, using last TBBO quote ≤ each endpoint (at print `t`, use that row’s BBO). Horizon **60 s ≥ 5 s** floor. |
| RTH | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET**; drop holiday / early-close sessions lacking a full RTH (pre-register CME calendar exclusions at harness time; do not drop after seeing returns). |
| Unit of analysis | One retained `(A, r)` pair per completed eligible run. |
| Statistic (promotion) | Pearson correlation `ρ(A, r)` on EXPLORATION retained pairs; **session-block bootstrap** 95% CI, **10,000** reps, seed **20260808**; within-session **label-shuffle placebo** on `r`, **1,000** reps, same seed; two-sided \|ρ\| vs placebo p95. |
| Sign / CI limb | CI excludes 0 |
| Placebo limb | \|ρ\| > placebo \|.\| p95 |
| Halves | Split EXPLORATION session-dates into older/newer halves; disagree on `sign(ρ)` → **AMBIGUOUS-HOLD** (do not promote) |
| Magnitude floor | **AMBIGUOUS-HOLD** if CI/placebo clear but \|ρ\| **< 0.02** |
| **Eligible** | Completed runs with `n_trades ≥ N_min`, end time `t` inside RTH, **and** valid mid exists at `t` and at `t+60s−` |
| **VOID-COVERAGE** | retained / eligible **< 90%** → `VOID-COVERAGE` |
| **VOID-POWER** | retained **n < 2,000** → `VOID-POWER` (evaluated before ρ) |

**Naming:** this is **aggressor-run length**, not volume-bucket imbalance (R2VBUCK) and not MNQSEL restart-clock selection.

**C9 clearance (quote):** MNQFLOW-1 DEAD re-proposal bar requires *"a named feature that is **not** top-of-book size imbalance…"*. Signed **aggressor-run trade-count** clears limb 1 — tape aggressor sequence length, **not** resting ToB size imbalance.

**Depth-census disclosure (transfers):** L1 total p05/p50/p95 ≈ **2/7/17**, 99.98% tied (MNQFLOW re-aim). Feature here is a **run aggregate over tape prints**, not a per-quote resting-size predictor.

**Forbidden inside the cell:** ORB timestamps; outcome joins (R, win/loss, MFE/MAE); flicker-filter retune of OFCHAN C1; resting ToB size imbalance; volume-bucket aggressor imbalance (R2VBUCK); MNQSEL restart-clock selection; fitting `N_min` from data; size-sum as the promotion feature; bars-only S/R; ICT/ORB gates; N14/Cap tripwire as filter; ES/NQ parent features; schema other than `tbbo`; reading any CONFIRM quote for exploration metrics; D1/D2 μ scoring inside G2.

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
| EM4 | **D** — weekly idle cleared by design if runs fire on most RTH days (not a G2 gate) |
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

- **MNQSEL** oracle top-1/day &lt; 0.40R applies to **restart-clock event windows**, not this aggressor-run→mid universe — different candidate set; not a universal ceiling.
- **K-wall** viable stop band **5–20 pt** implies ~**3–9 pt** predicted directional edge per trade to matter under EM1 economics. A bare \|ρ\| ≥ 0.02 limb is an association floor only; converting ρ into points requires the realized σ of 60 s mid returns on the EXPLORATION panel (disclose at G2; do not amend promotion limbs post-hoc).
