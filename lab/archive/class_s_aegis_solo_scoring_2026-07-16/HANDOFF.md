# Stage-2 setup — Aegis-6J **solo** Part A scoring (H-SOLO on the v2.1 winner)

**Status:** `CLOSED — H-SOLO FALSIFIED` (2026-07-16) under v2.2. See [`RESULTS.md`](RESULTS.md) +
[`Stage-2 closure`](lab/archive/../../docs/briefs/closures/2026-07-16-aegis-6j-prop-reconstruction-stage2-hsolo-falsified.md).
Below is the frozen setup record (native panel construction confirmed; driver landed).
**Authority (frozen):**
- Winner (v2.1 §6): **c05** — `max_contracts` 8 · `risk_pct_display` **0.40%** · `eod_fill_deadline_et`
  16:00 · panel sha **`ED91CD2D5D40`**. Pre-reg
  [`docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-16-aegis-6j-prop-reconstruction-v2.1-tiebreak-prereg.md) (`FROZEN`).
- Frozen gate: [`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`](lab/archive/../../docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md) — Part A **bust ≤ 3.0%** + **P(pass) ≥ 50%**, Run-2, seeds **42/123/2026**, 10k×3, horizon 1500, `dd_protection` OFF, inactivity off.
- Harness base (adapt, do NOT copy verbatim): [`../class_s_candidate2_scoring_2026-07-15/run_class_s_c2_scoring.py`](lab/archive/class_s_candidate2_scoring_2026-07-15/run_class_s_c2_scoring.py).
- **H-SOLO ≻ gate:** Part A must PASS on **BOTH** `Tradeify_Select_100K` **AND** `MFFU_Rapid_100K` (stricter than the gate's ≥2-of-4). Bulenox/BluSky diagnostic only.

---

## §0 — Rule-0 reads (done 2026-07-16, this session)

- **`run_class_s_c2_scoring.py`** — `phase0_verify` (signature + `ACTIVE_FIRM=="FXIFY"` fixture +
  gate ceilings 0.03/0.5 + frozen tier tuple); `build_scaled_panel` → `pin_r_basis(full_stop_mean)`
  1R guard (`_assert_1r_guard`: FALLBACK or n<5 → `NeedsContext`); `score_book` → `score_candidate`
  (daily_100k, full_res_trades, envelope, thresholds, n_sims, gross_edge_usd); `book_daily_at_100k`
  scales a $200K panel ×(100/200). **Verdict**: RESOLVED iff ≥2 clear + a `trailing_locking` firm.
- **`core/firm_rules.py`** — `Tradeify_Select_100K` (L227) + `MFFU_Rapid_100K` (L286) present; both
  `dd_type: trailing_locking`; `starting_balance` 100_000; `cost_per_side_usd` set.
- **c05 panel** `lab/analysis/aegis_6j_prop_reconstruction_2026-07/c05_fill1600_cap8_r40_ed91cd2d.csv`
  — native `CME:6J1!` export; `detect_initial` ≈ **$100K** (first row Cum USD −499.8 / Cum % −0.50 →
  ~99,960); already sized cap8/0.40% native futures. sha `ED91CD2D5D40` (in `WAVE1_SHA256SUMS`).

---

## §1 — The load-bearing design point (panel construction) — CONFIRM

The candidate #1/#2 harness takes a **CFD** panel, decompounds to $200K static, and **re-scales**
to the target futures risk% via the 1R ratio (`scale = target_1r / r_dollars`). **That path is
WRONG for the solo reconstruction** because **c05 is a native-futures export already sized at
cap8 / 0.40%** — re-scaling would double-size it. The v2 reconstruction existed precisely to
produce this native panel and "kill the ae744 provenance gap" (v2 §0/§2.7).

**Pinned construction (recommended):**
1. Load c05 CSV; `pair_trades`; **slice to the Stage-2 panel window 2022-01-12 → 2026-06-30**
   (drops the 2 post-panel July-2026 tail exits, consistent with v2 §2.5 / §0 note).
2. `detect_initial` → ~$100K; **decompound to STATIC at $100K** (`reconstruct_static` at
   ACCOUNT=100_000) to remove TV equity-compounding — the gate's convention. **No 1R re-scale.**
3. Daily book = per-day Σ static Net PnL → this **is** `daily_100k` directly (native $100K; no
   ×0.5 band scale).
4. **1R guard = DIAGNOSTIC only:** `pin_r_basis(full_stop_mean)` must yield ≥5 full-stops and not
   FALLBACK (5274c class) — hard-fail `NEEDS_CONTEXT` otherwise. It gates panel validity; it does
   **not** feed a re-scale.

**Alternative (only if operator rejects the above):** treat c05 like a CFD panel and re-scale to
0.40%×$100K. Flagged as **not recommended** — it re-sizes an already-native panel. Do not pick
silently.

---

## §2 — Driver spec (`run_aegis_solo_scoring.py`, to author under this dir)

- **Phase-0:** v2.1 §9 signature present; `ACTIVE_FIRM=="FXIFY"` fixture; gate ceilings 0.03/0.5;
  frozen tier tuple intact. Fail → exit 3.
- **Panel:** §1 pinned construction. Single leg (`aegis_c05`). Hash-check the c05 CSV vs
  `WAVE1_SHA256SUMS` (blob/LF bytes — see the `.gitattributes eol=lf` fix on
  `claude/cursor-dispatch-infra`; run against blob if a fresh Windows checkout is CRLF).
- **Score:** `score_candidate` per frozen `load_scoring_thresholds(GATE_PREREG)`; Run-2; n_sims
  default = gate `sims_per_seed`; envelope-YES carried from v2 (overnight 0%, fills ≤ 16:00).
- **Firms:** score `Tradeify_Select_100K` and `MFFU_Rapid_100K` (both required); Bulenox/BluSky
  diagnostic. Thread tiers via `firm_kwargs`; read bust via `summarize_outcomes` **only**.
- **Verdict:** **RESOLVED (H-SOLO)** iff Part A PASS on Tradeify **and** MFFU; else **FALSIFIED**
  (winner expression closes — no compose, no in-place reweight; v2.1 §4). Regime rider owed only
  on RESOLVED (gate §7(7)).
- **Prior-look (RESULTS):** disclose all 12 Stage-1 cells + v1 FALSIFIED close + v2 AMBIGUOUS +
  v2.1 tie-break (best-of-K honesty).
- **Outputs:** `RESULTS.md` (cites v2.1 + gate pre-regs) + `aegis_solo_report.json`.

---

## §3 — Forbidden (halt `NEEDS_CONTEXT` / `PHASE0_FAIL`, do not improvise)

- Switching `ACTIVE_FIRM` off the FXIFY fixture.
- CFD-decompound **re-scaling** the native c05 panel (§1) without operator sign-off.
- `compute_default_config()['bust_rate']` for Part A (use `summarize_outcomes`).
- Composing with MYM+MNQ (Stage-3 needs its own Class-S pre-reg + candidate #1 regime-fragile caveat).
- Using ae744 (provenance-gapped) instead of the c05 winner CSV.
- Touching BE/SL/TP/ATR or the locked Aegis v4.3.

---

## §4 — Open items for operator

1. **Confirm §1 panel construction** (native, no re-scale) — the one choice that changes the verdict.
2. Implement `run_aegis_solo_scoring.py` — **inline (CC)** or **Cursor dispatch** (frozen spec →
   fits the CC/Cursor ADR; use `scripts/dispatch_cursor.ps1` once allow-listed).
3. Then run → H-SOLO verdict (the actual question: does solo Aegis-6J clear both prop firms?).
