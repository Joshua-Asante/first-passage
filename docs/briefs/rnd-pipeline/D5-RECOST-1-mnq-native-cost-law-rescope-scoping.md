# Campaign scoping — D5-RECOST-1: MNQ-native cost-law re-derivation of the D5 Baltussen H1 construct

**Status:** `CLOSED — FALSIFIED 2026-07-21` (Stage-0 frozen `2dad8f9`, run executed same session; OOS edge **decayed to −0.33 bp** → Stage-2 KILL — the cost-geometry lever narrowed the hurdle 3.7× but the edge itself went negative OOS). Verdict: [`RESULTS.md`](../../../lab/archive/d5_recost_2026-07/RESULTS.md).
**Axis:** re-derivation of the D5 intraday-momentum footprint's Stage-2 cost-law gate at current MNQ notional levels (same construct, same signal — cost geometry only).
**Lane:** mechanism-first (HARV ADR `Accepted` — HARD gate applies to any fresh `register_search open`).
**Parents:** [`D5-NQ-intraday-momentum-scoping.md`](D5-NQ-intraday-momentum-scoping.md) (`CLOSED — Stage-2 cost-law KILL 2026-07-16`) · [`D5-NQ-intraday-momentum-preregistration.md`](../pre-registration/D5-NQ-intraday-momentum-preregistration.md) (Stage-0 frozen 2026-07-15) · [`d5_nq_intraday_mom RESULTS.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md) (the closed verdict this re-opens)
**Trigger:** 2026-07-21 deep-research fan-out on prop-fundable strategy archetypes (this session) — external replication of the Baltussen construct as the strongest futures-native academic edge, cross-checked against our own D5 closure, surfaced that D5's Stage-2 kill was measured entirely on **2010–2018 parent-NQ price levels** while the campaign's own cached OOS panel (2019-05-06→2026-07-16, already pulled, $0.00) sits at 4–7× higher notional.

---

## §0 — Rule-0 reads (production-source verification, this session 2026-07-21)

- [`lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md) @ `e1c51f0` (2026-07-16) — the closed verdict: mean gross edge **+1.4613 bp/session** vs 4× hurdle **11.063 bp** at IS-era median NQ price **4013.5**; `corr(r_rod,r_last)=+0.081`; "native-MNQ OOS would not change the kill — the gross edge would need to rise ~7.6× ... not a micro-vs-parent rescaling" (line 48) — **this claim is the one under test below; it was reasoning about micro-vs-parent contract rescaling, not about the price level having moved across eras.**
- [`lab/analysis/orb/d5_nq_intraday_mom_2026-07/stage2_4_report.json`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/stage2_4_report.json) @ `e1c51f0` — machine-readable Stage-2 numbers, confirmed matching RESULTS.md verbatim (`mean_edge_bp: 1.4612647044076368`, `hurdle_4x_bp: 11.062663510651548`, `median_px_1530: 4013.5`).
- [`lab/discovery/cost_mnq.py`](../../../lab/discovery/cost_mnq.py) @ `e1c51f0` — `hurdle_from_price(mnq_price, firm_key)` computes `notional = mnq_price × MNQ_MULTIPLIER($2)`, `rt_cost = 2×(commission_per_side + 1_tick_slip)`, `hurdle_4x_frac = 4×rt_cost/notional`. **Confirmed monotonic decreasing in `mnq_price`** — a fixed-dollar cost divided by a rising notional mechanically shrinks the bp hurdle. This is the load-bearing mechanism this campaign tests, verified by direct read of the formula, not inferred.
- [`lab/analysis/orb/d5_nq_intraday_mom_2026-07/series.py`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/series.py) @ `e1c51f0` — confirms `cached_mnq_continuous_1m()` reads the **already-pulled** `MNQ.v.0` continuous OOS panel (2019-05-06→2026-07-16, $0.00, 2,535,465 rows per [`PULL_LOG.md`](../../../lab/analysis/orb/d5_nq_intraday_mom_2026-07/PULL_LOG.md) @ `e1c51f0`) — **no new pull required for this campaign.**
- [`core/firm_rules.py`](../../../core/firm_rules.py) @ `a53ee99` (2026-07-13) — `cost_per_side_usd`: Bulenox 0.61, Tradeify_Select 0.91, MFFU_Rapid 0.95, BluSky 0.95 (index micros). `DEFAULT_FIRM_KEY = "Bulenox_100K"` in `cost_mnq.py` — the cheapest of the four automation-friendly firms; **flagged in §5 as a forbidden-move risk** (see below).
- [`D5-NQ-intraday-momentum-preregistration.md`](../pre-registration/D5-NQ-intraday-momentum-preregistration.md) @ `fb9b9c9` (2026-07-15) — confirms the **original** OOS axis design (§2): "IS + all tuning on parent NQ 2010-01-01:2018-12-31; statistical/realism OOS on native micro MNQ 2019-05-06:present. Native-micro re-run is a **realism** gate, not an independence axis." The OOS panel was **already earmarked** for Stage 5-8 confirmation of this exact construct — it was never scored because Stage-2 (on IS) killed first. This campaign proposes running the cost-law step **on the panel already designated for it**, not opening a new data source.
- **Pre-flight computation this session** (verified against production `cost_mnq.py`, not re-derived by hand): loaded the cached `MNQ.v.0` OOS panel, extracted the 15:30 ET bar close (same convention as the closed Stage-2 `median_px_1530`) per session, computed median price across five windows plus a recency check:

  | Window | n sessions | median 15:30 px | repriced `hurdle_4x_bp` (Bulenox) | frozen IS edge (1.461 bp) vs hurdle |
  |---|---|---|---|---|
  | IS era (as-closed) | 2,127 | 4,013.5 | 11.063 | 13.2% of hurdle — **fail, 7.6× short** |
  | OOS full (≥2019-05-06) | 1,791 | 14,767.2 | 3.007 | 48.6% — fail |
  | ≥2021 | 1,378 | 15,959.5 | 2.782 | 52.5% — fail |
  | ≥2023 | 877 | 19,868.8 | 2.235 | 65.4% — fail |
  | ≥2024 | 629 | 21,505.5 | 2.065 | 70.8% — fail |
  | ≥2025 | 380 | 24,434.4 | 1.817 | 80.4% — fail |
  | last 60 sessions | 60 | 29,448.25 | 1.508 | 96.9% — **fail, but essentially at par** |

  **This is a repricing of the hurdle only — the "edge" column above is the unchanged, frozen IS-era number (+1.461 bp). No OOS edge has been measured yet.** It is a pre-flight motivating question, not a result: does re-measuring the edge *and* the hurdle jointly on OOS-native data change the verdict, or does the edge itself decay to below-hurdle on the modern-era panel (the open question the original campaign never got to ask)?

---

## §1 — Context & motivation

D5 closed `FALSIFIED` (Stage-2 cost-law KILL) on 2026-07-16 by measuring the Baltussen-2021-JFE H1 construct's IS-era (2010–2018) gross edge against a hurdle computed at **2010–2018 NQ notional** ($8,027, median px 4013.5). The closure's own note reasoned that native-MNQ OOS "would not change the kill... not a micro-vs-parent rescaling" — correct on the *contract* axis (MNQ vs parent NQ share the same $2/point multiplier), but that note did not address the **temporal** axis: NQ has traded at 4–7× the IS-era notional across the campaign's own already-cached OOS window, and the cost hurdle is a fixed-dollar-cost-over-notional ratio that shrinks mechanically as notional rises. The pre-flight above shows the repriced-hurdle margin has narrowed from "7.6× short" to "essentially at par" at current prices — using the *old, frozen* edge number. Whether the *real* (OOS-native) edge clears a *jointly re-measured* OOS-native hurdle is the open, previously-unasked question this campaign poses.

This connects to standing doctrine: the HARV lane's Requirement 5 cost-law-at-admission rule ([`strategy_harvest.md`](../../methodology/strategy_harvest.md) §1) and the harvest-intake ADR's own precedent that a **cost-geometry change, not a parameter re-tune, is admissible re-proposal grounds** — the closest analogue is the [fixrev EURUSD closure](../../rejected_candidates.md) ("materially better-than-retail execution... OR a genuinely different mechanism" as the re-proposal bar); here the analogous new fact is a **venue-external, dated, verifiable market-structure change** (NQ's own price level), not a re-tuned parameter or a wider grid.

---

## §2 — Prior art / lineage

- **D5-NQ-intraday-momentum** (`CLOSED — Stage-2 cost-law KILL`, 2026-07-16) — the parent campaign this re-derives. Banked K=1 for the MNQ family. This scoping does **not** dispute the IS-era verdict (it stands, correctly computed at IS-era prices); it asks whether the *same construct* clears at *current* economics.
- **H-OD-1 (ES overnight drift)** — sibling Stage-2 cost-law KILL same week, mechanism itself confirmed in-sample (+1.444 bp, t≈5.0, positive all 9 IS years) yet sub-cost — same "mechanism real, magnitude thin" shape as D5. Not directly reopened here (different instrument, different cost trajectory — ES notional has not moved as dramatically relative to its own IS calibration window), but the **general lesson** (cost-law kills can be magnitude-thin, not mechanism-null) is the shared thread.
- **DISC-CAMP-0** — established the "0/6 candidates clear cost-law" pattern on GC/MGC mining; not directly relevant to this single mechanism-first re-derivation, but is the reason cost-law is treated as the hard, non-negotiable first gate rather than something to route around.
- **2026-07-21 deep-research synthesis** (this session, not yet a committed artifact) — external academic literature (Baltussen et al. 2021 *JFE*; independent MNQ 0/14-signal-family falsification, arXiv 2605.04004) corroborates that (a) this exact construct is the single strongest futures-native, cost-aware academic result on liquid index futures, and (b) the broader class of OHLCV intraday signals dies on cost-law at *current* MNQ economics in an independent study — meaning if this construct is going to clear cost-law anywhere, current-era repricing (not further signal search) is the lever, consistent with the pre-flight above.

---

## §3 — Question (D5-RECOST-1)

**Bad form (rejected):** "Should we re-run D5 at today's prices to get it to pass?" — bakes in the desired outcome.

**Good form:** What is the joint gross-edge-and-cost-hurdle relationship for the D5 Baltussen H1 construct when both are measured on the **same, already-designated, native-MNQ OOS window** — has the fixed-dollar-cost-over-rising-notional mechanism narrowed the original 7.6×-short margin enough that the construct's *own OOS-era edge* (not the frozen IS number) clears a *jointly-measured* OOS-era hurdle?

---

## §4 — Falsifiable hypothesis (H-D5-RECOST)

**H-D5-RECOST:** if the Baltussen H1 construct's gross edge, measured fresh on the native-MNQ OOS panel (2019-05-06→2026-07-16, or a pre-registered recent sub-window chosen to avoid regime-mixing — e.g. ≥2023-01-01), clears **4× the cost hurdle computed on that same window's own median notional** (Bulenox_100K economics, 1-tick slippage, unchanged from the original frozen construct), **then** D5-RECOST is a confirmed Stage-2 PASS and routes to the **already-frozen** Stage 5-8 pipeline (block size, DSR≥0.95/Sharpe≥0.65, temporal-consistency battery, disjoint-session placebo, MNQ realism, breadth) from the original D5 pre-registration — no re-freeze of those gates needed, only Stage-2's price-level input; **otherwise** D5-RECOST closes FALSIFIED and the "7.6× short → narrows but does not close" finding is banked as a defect-log entry, foreclosing the cost-geometry lever specifically (not the whole campaign family — see §6).

**Reject H-D5-RECOST if:** OOS-native (or the declared recent-sub-window) gross edge < 4× the OOS-native hurdle.
**Accept H-D5-RECOST if:** OOS-native gross edge ≥ 4× the OOS-native hurdle.
**Ambiguous-hold if:** the declared window's session count is too low for a stable mean-edge estimate (mirrors the parent pre-reg's `dsr_unreachable_low_n` Default #3 condition) — re-test window named at closure.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Repricing the hurdle with a cherry-picked recent window (e.g., "last 60 sessions," median px 29,448) while leaving the edge frozen at the IS number.** This is exactly the pre-flight table above — it is the *motivating* computation, explicitly **not** the gate. The last-60-session window is the single most favorable, smallest-N, most recency-biased cut available; using it as the actual verdict would be a best-of-window pick disguised as due diligence. The real gate (§4) requires **jointly** re-measuring edge and hurdle on the *same*, pre-declared window.
- **Using `DEFAULT_FIRM_KEY="Bulenox_100K"` (cps $0.61, the cheapest of the four automation-friendly firms) without disclosing the sensitivity.** Continuity with the original campaign's default is defensible (same firm_key = apples-to-apples vs the closed verdict), but at 2025+ prices MFFU_Rapid_100K's hurdle is 2.374 bp vs Bulenox's 1.817 bp — a ~30% swing. The re-derivation must report both, not silently anchor on the friendliest cost basis to make the pass easier.
- **Treating a Stage-2 PASS here as a survivor.** Mirrors the original campaign's own forbidden move #6 — Stage-2 clearing licenses Stage 5-8, not deployment or lifecycle admission. The full battery (placebo, temporal consistency, realism, breadth) still gates.
- **Re-opening this as a fresh hypothesis with a fresh K binding** without an explicit operator ruling on whether it consumes new K or reuses the original K_eff=1 (H1 sole candidate) binding. This is genuinely ambiguous under the existing manifest ledger (D5 banked K=1 for the MNQ family as a closed/non-survivor) — resolving it silently either way (assume free reuse, or assume a fresh K=1 charge) is a forbidden move; §7 names this as an explicit operator decision before `register_search open`.
- **Expanding the window search to find the best-performing recent sub-period** (e.g., trying 2023, 2024, 2025, last-60 and reporting the best). One window is declared at freeze; this is the Q-ORB-FRIDAY-1 best-of-K trap in a new guise.
- **Quoting the pre-flight table's "96.9% of hurdle" row as if it were a confirm result.** It is a hurdle-only recomputation against a stale edge number — stated explicitly in §0 and repeated here so it cannot be mis-cited downstream.

---

## §6 — Gate criteria (binary)

| Verdict | Trigger condition | Disposition |
|---|---|---|
| `RESOLVED` (Stage-2 PASS) | OOS-native (declared window) gross edge ≥ 4× OOS-native hurdle (Bulenox_100K, 1-tick slip) | Route to the **already-frozen** Stage 5-8 pipeline from the original D5 pre-reg (no new Stage-0 freeze for those gates); MFFU-basis hurdle reported alongside as a sensitivity note |
| `FALSIFIED` | OOS-native gross edge < 4× OOS-native hurdle | Close; bank as a defect-log entry on the MNQ family — the cost-geometry lever specifically closes, not the broader mechanism-first program; success-eligible research outcome |
| `AMBIGUOUS-HOLD` | Declared window session count insufficient for a stable mean-edge estimate | Re-test window named at closure; no in-place threshold edit |

08-08 is a progress-check date only; this campaign's own run is the hard adjudication.

---

## §7 — Next actions (operator decisions required before Stage-0 freeze)

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | **Operator ruling: does this re-derivation consume fresh K, or reuse the original D5 K_eff=1 binding (same construct, same candidate, previously-designated confirm window never scored)?** | Operator | **OPEN — blocks `register_search open`** |
| 2 | **Operator ruling: declare the frozen sub-window for the joint edge+hurdle re-measurement** (candidates: full OOS 2019-05-06→2026-07-16; or ≥2023-01-01 to reduce regime-mixing with the COVID-era 2020-21 window already flagged degraded-quality in `PULL_LOG.md`) | Operator | **OPEN** |
| 3 | Author full Stage-0 pre-registration (mirrors [`D5-NQ-intraday-momentum-preregistration.md`](../pre-registration/D5-NQ-intraday-momentum-preregistration.md) structure) with the declared window frozen, §R reachability attestation, and the dual-firm-key (Bulenox + MFFU) hurdle report as a pre-committed output, not a discretionary add | CC (on operator GO) | Not started |
| 4 | On Stage-0 freeze + operator GO: recompute Stage-2 jointly on the declared window (reuses `cost_mnq.hurdle_from_price` + a fresh `session_edges` run over `cached_mnq_continuous_1m()` — **zero new pull**, both already cached at $0.00) | Lab | Not started |
| 5 | If PASS: continue into the original pre-reg's Stage 5-8 (block size, DSR, temporal battery, placebo, realism, breadth) — those gates are already frozen and do not need re-authoring | Lab | Contingent on #4 |

---

## §10 — Audit hooks (runnable)

```bash
# 1. Confirm the cited IS-era numbers still match the closed verdict (verbatim, unchanged).
grep -n "1.4612647044076368\|11.062663510651548\|4013.5" \
  lab/analysis/orb/d5_nq_intraday_mom_2026-07/stage2_4_report.json

# 2. Confirm the OOS panel is still cached (no re-pull needed).
python -c "from pathlib import Path; p=Path.home()/'.databento_cache'/'ohlcv-1m_continuous_ce119c1e8f923316.dbn'; print(p, p.exists())"

# 3. Confirm the hurdle formula is unchanged (monotonic-in-price mechanism this campaign relies on).
grep -n "def hurdle_from_price\|notional = mnq_price" lab/discovery/cost_mnq.py

# 4. Confirm firm_rules cost_per_side_usd values (Bulenox 0.61 / MFFU 0.95) haven't drifted.
grep -n "cost_per_side_usd.*0.61\|cost_per_side_usd.*0.95" core/firm_rules.py

# 5. Reproduce the pre-flight repricing table (hurdle-only, frozen edge) from this file's §0.
#    (ad hoc script, not yet committed to lab/ — commit under d5_recost_2026-07/ on Stage-0 freeze)
```

---

## Verification

```bash
PYTHONIOENCODING=utf-8 python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/D5-RECOST-1-mnq-native-cost-law-rescope-scoping.md --type inquire

# §0 anchors
git log -1 --format='%h %ci' -- lab/analysis/orb/d5_nq_intraday_mom_2026-07/RESULTS.md            # e1c51f0
git log -1 --format='%h %ci' -- lab/discovery/cost_mnq.py                                       # e1c51f0
git log -1 --format='%h %ci' -- core/firm_rules.py                                              # a53ee99
git log -1 --format='%h %ci' -- docs/briefs/pre-registration/D5-NQ-intraday-momentum-preregistration.md  # fb9b9c9

# Pre-flight repricing table reproduces (zero pulls, zero K; uses already-cached data)
# See §10 hook #5 — script to be committed alongside the Stage-0 pre-reg on operator GO.
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-21 | Scoping drafted — pre-flight repricing computed against production `cost_mnq.py` + the cached MNQ OOS panel (zero new pulls). Margin narrows from 7.6× short (IS era) to ~1.0–1.2× short at current prices, using the frozen IS edge — motivating, not sufficient. Two operator decisions (§7 #1–2) block Stage-0 freeze. | Claude Code (Sonnet 5), operator-directed |
