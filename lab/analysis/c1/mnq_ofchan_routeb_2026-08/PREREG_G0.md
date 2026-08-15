# Q-OFCHAN-1 — Route B G0 charter (FROZEN shape; explore GO issued)

**Status:** `FROZEN G0 · G2 COMPLETE 2026-08-07 — VOID-COVERAGE` — schema×window only (`tbbo` · `MNQ.v.0` · EXPLORATION). **No CONFIRM. Cap seat not claimed.** Empty candidate list → STOP this catalogue.
**Date:** 2026-08-06
**Parent brief:** [`docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md`](../../../../docs/briefs/Q-OFCHAN-1-orderflow-channel-route-b-scoping.md)
**Route:** Avenue A **Route B** ([`ADR`](../../../../docs/adr/2026-08-05-avenue-a-generate-confirm-route.md) `Accepted`)
**Screen:** EM0–EM5 ([`spec`](../../../../docs/spec/2026-08-05-eval-mechanism-shape-screen.md) `RATIFIED 2026-08-06`) — applied **before** this freeze (§2.0a)
**Cost so far:** G1 **$0.0000**; EXPLORATION pull **COMPLETE** via batch `GLBX-20260807-EHX5KUSF7K` @ **$0.0** → `~/.databento_cache/q_ofchan_1_exploration_tbbo/GLBX-20260807-EHX5KUSF7K/` (155 `*.tbbo.dbn.zst`, ~3.49 GB). **G2 COMPLETE** → [`RESULTS_g2.md`](RESULTS_g2.md) `VOID-COVERAGE` (coverage 7.36%). CONFIRM untouched.
**`K_intrinsic = 1`** (catalogue size). Cap 1.0 → DSR floor **0.650**, headroom **0.350**.
**Confirm-budget M = 1** (frozen here; Bonferroni/Holm N/A at M=1).
**Cap seat:** **not claimed** — Cap spent on Q-CAPA-1; this is ordinary Route B disclosure.

Frozen before any exploration score exists for this construct.

---

## §0 — Rule-0 / depth-census context (mandatory)

| Source | What it pins |
|---|---|
| Parent brief §0 | Geometry, Route B Accept, EM ratification, entitlement |
| MNQFLOW / N14 RESULTS | Depth census: L1 thin (p50 total ≈7); size-derived features coarse / high tie rate — disclosed, not evaded |
| MSCHAN salvage | ≥5 s horizon; flicker filter (arXiv 2507.22712); no ES→MNQ lead-lag |
| Checklist G0 | Windows, catalogue, promotion, cost ceiling placeholder, M |

**Parent→micro proxy discipline:** instrument is **`MNQ.v.0`** (micro). NQ parent depth is **not** claimed as MNQ economics. No NQ.v.0 / ES cross-book cell.

---

## §1 — Windows (non-overlapping halves of free 1y `tbbo`)

Pinned from entitlement inventory + Cap/N14 free-year precedent (end exclusive). Split:
**CONFIRM = older half · EXPLORATION = newer half** (checklist worked example; plan lock).

| Window | ISO bounds (UTC dates; `--end` exclusive) | Role |
|---|---|---|
| **CONFIRM** | **2025-08-06 → 2026-02-06** | Reserved holdout. **No exploration score may use it.** |
| **EXPLORATION** | **2026-02-06 → 2026-08-06** | Sole window for Stage-G promotion metrics |

- Symbol / stype: `MNQ.v.0`, continuous
- Schema: **`tbbo` only** (no `mbp-10` / `mbo` escalation in this campaign)
- Cost ceiling placeholder: **$0.00** inside free entitlement; if G1 estimate > $0, **halt** and return to operator before pull
- Re-estimate command (explore GO / G1 only — **not run this session**):

```bash
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate \
  --symbols MNQ.v.0 --stype continuous --schema tbbo \
  --start 2026-02-06 --end 2026-08-06
```

---

## §2 — Catalogue (size 1 → `K_intrinsic = 1`)

### Cell C1 — flicker-filtered L1 signed size imbalance → 60s mid return (RTH grid)

| Element | Frozen definition |
|---|---|
| Sampling grid | CME equity-index **RTH** Mon–Fri **09:30–15:59 ET** inclusive start minutes; sample on the **clock minute** (`…:00`) so consecutive samples are 60 s apart. **Not** ORB-trigger-tied. Drop holiday / early-close sessions lacking a full RTH grid (pre-register exclusion list at harness time from CME calendar; do not drop after seeing returns). |
| Feature `A_raw` | At each grid time `t`, take the last TBBO quote with `ts ≤ t`: `A_raw = (bid_sz_00 − ask_sz_00) / (bid_sz_00 + ask_sz_00)`. Undefined if `bid_sz_00 + ask_sz_00 == 0` → sample dropped. |
| Flicker filter | Cite arXiv **2507.22712**. Retain sample at `t` only if `sign(A_raw)` is unchanged across the **last 5 TBBO updates** at the touch with `ts ∈ (t − 1s, t]` (wall-clock 1 s lookback). If fewer than 5 updates in the lookback, **drop** the sample (do not impute). Filtered feature `A = A_raw` on retained samples. |
| Target | Mid return over **[t, t+60s)`**: `r = (mid_{t+60s−} − mid_t) / mid_t` where `mid = (bid_px_00 + ask_px_00) / 2`, using last quote ≤ each endpoint. Horizon **60 s ≥ 5 s** floor. |
| Unit of analysis | One retained `(A, r)` pair per grid minute. |
| Statistic (promotion) | Pearson correlation `ρ(A, r)` on EXPLORATION retained pairs; **session-block bootstrap** 95% CI, **10,000** reps, seed **20260806**; within-session **label-shuffle placebo** on `r`, **1,000** reps, same seed; two-sided \|ρ\| vs placebo p95. |
| Sign / CI limb | CI excludes 0 |
| Placebo limb | \|ρ\| > placebo \|.\| p95 |
| Halves | Split EXPLORATION session-dates into older/newer halves; disagree on `sign(ρ)` → **AMBIGUOUS-HOLD** (do not promote) |
| Magnitude floor | **AMBIGUOUS-HOLD** if CI/placebo clear but \|ρ\| **< 0.02** (pre-registered minimal interpretable association; not a Sharpe claim) |
| VOID-COVERAGE | Retained samples / eligible RTH grid minutes **< 90%** → `VOID-COVERAGE` |
| VOID-POWER | Retained n **< 2,000** → `VOID-POWER` (evaluated before ρ) |

**Forbidden inside the cell:** ORB timestamp conditioning; outcome joins (R, win/loss, MFE/MAE); ES/NQ parent features; schema other than `tbbo`; reading any CONFIRM quote for exploration metrics.

---

## §3 — Promotion rule (EXPLORATION only)

Promote C1 to "candidate" iff, **on EXPLORATION only**:

1. Not VOID-POWER / VOID-COVERAGE
2. Bootstrap CI for ρ excludes 0
3. \|ρ\| beats placebo p95
4. Halves agree on sign
5. \|ρ\| ≥ 0.02

Else: empty candidate list (or AMBIGUOUS-HOLD per halves/magnitude). **Do not** treat promotion as edge, admission, or harvest PASS.

---

## §4 — Confirm budget / Stage-C pointer

- **M = 1** — at most one candidate confirmed this campaign.
- C0 confirmatory PREREG (not authored this session) must restate CONFIRM window **2025-08-06 → 2026-02-06**, identical or stricter limbs, and M=1.
- Ordering trap: any CONFIRM metric before C0 commit **voids** confirm — new campaign required.

---

## §5 — EM attestation (copy of brief §6a)

`P U U D D D` — EM0 PASS; EM1/EM2 SHAPE-UNSCREENABLE; EM3–EM5 design grounds. Not SHAPE-CLEAR.

---

## §6 — Forbidden moves (G0)

- FM-1 — CONFIRM peek / score before C0
- FM-2 — Catalogue growth after this freeze
- FM-3 — ORB-tie or outcome joins (F2 GUARD)
- FM-4 — Cap-seat claim
- FM-5 — Treat G2 as admission / edge
- FM-6 — `mbp-10`/`mbo` without new campaign
- FM-7 — Patch EM1/EM2 to PASS
- FM-8 — Explore pull without operator explore GO + G1 estimate
- FM-9 — Edit this freeze after seeing a number (Trap #12)

---

## §7 — Protocol order

1. This file + parent brief on branch (**G0 freeze shape**) — **this session**.
2. Operator **explore GO**.
3. G1 estimate EXPLORATION (`$0` expected) → pull EXPLORATION only.
4. G2 single run → candidate list (0 or 1).
5. If candidate: C0 freeze → operator **confirm GO** → Stage-C on CONFIRM only.
6. Closure + boards.

---

## §8 — Audit hooks

```bash
rg -n "CONFIRM|EXPLORATION|M = 1|K_intrinsic = 1|tbbo only" \
  lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md
# CONFIRM must appear; no CONFIRM metrics / ρ numbers may appear in RESULTS until C0

rg -n "2025-08-06|2026-02-06|2026-08-06" \
  lab/analysis/c1/mnq_ofchan_routeb_2026-08/PREREG_G0.md

# No pull yet
git status -- lab/analysis/c1/mnq_ofchan_routeb_2026-08/
```

---

## Amendment log (append-only)

- **2026-08-07 — G2 COMPLETE → `VOID-COVERAGE` (empty candidates).** Runner `run_ofchan_g2.py` + `ofchan_lib.py` scored C1 on EXPLORATION cache only. n_retained **3,558** / eligible **48,360** = **7.36%** (< 90% floor) → VOID-COVERAGE precedes CI/placebo. Observed ρ **−0.012** (CI includes 0). Candidate list **[]**. CONFIRM untouched. Cap seat not claimed. G3 disposition: **STOP** this G0 catalogue (new campaign required to reopen). Artifacts: [`RESULTS_g2.md`](RESULTS_g2.md) / [`RESULTS_g2.json`](RESULTS_g2.json).
- **2026-08-07 — EXPLORATION pull COMPLETE (batch).** Streaming aborted (~70m premature EOF). Batch **`GLBX-20260807-EHX5KUSF7K`** state=`done`, cost **$0.0**, records **157,115,499**, package **3,487,999,301** bytes. Downloaded to `C:/Users/joshu/.databento_cache/q_ofchan_1_exploration_tbbo/GLBX-20260807-EHX5KUSF7K/` — **155** `glbx-mdp3-YYYYMMDD.tbbo.dbn.zst` covering **2026-02-06 → 2026-08-05** (end exclusive 2026-08-06). Sample sha256-16: `20260206`=`1aaaf64b3c046a9b`, `20260805`=`203753af92bb8253`. **G2 owed.** CONFIRM untouched. Cap seat not claimed.
- **2026-08-07 — EXPLORATION pull in progress (batch).** Streaming `db_fetch pull` aborted (~70m, `BentoError: Response ended prematurely`; vendor >5 GB → batch). Batch job **`GLBX-20260807-EHX5KUSF7K`** @ **$0.0** same schema×window; download dir `~/.databento_cache/q_ofchan_1_exploration_tbbo/`.
- **2026-08-06 — G1 estimate (EXPLORATION).** `tbbo` · `MNQ.v.0` continuous · `2026-02-06`→`2026-08-06`: **$0.0000**; billable **12,569,239,920** bytes; records **157,115,499**. Within ceiling. Do not pass `--phase discovery` (era-mix abort).
- **2026-08-06 — Operator explore GO issued.** G1 → EXPLORATION pull only. M=1 / K=1. Not authorized: CONFIRM; mbp-10/mbo; Cap seat; catalogue growth.
- **2026-08-06 — G0 FROZEN (docs only).** Explore GO unpaid; no estimate run; no pull; no harness results.
