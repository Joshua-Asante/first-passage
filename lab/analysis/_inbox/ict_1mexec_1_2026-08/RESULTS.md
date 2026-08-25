**Theme:** _inbox

# Q-ICT-1MEXEC-1 — RESULTS: the real MNQ 1-minute execution test

**Status:** **RESOLVED (FALSIFIED at Stage 2, F1).** The frozen construct's gross edge does not
clear 4.0x the round-trip cost hurdle at the Tradeify basis. Per its own falsifier table, Stages
3-8 never run. `register_search close` recorded 0 of 1 survivors; `K_intrinsic=1` spent.
Does not reopen the family's standing `MNQ x ict-liquidity` DEAD verdict.

**Pre-registration:** [`2026-08-04-ict-1m-execution-mnq-preregistration.md`](../../../../docs/briefs/pre-registration/2026-08-04-ict-1m-execution-mnq-preregistration.md)
— frozen `FROZEN — GO (Option B)` 2026-08-24, correcting a stale reachability screen and
addressing the profile-consult BLOCKING bar before any code ran.

---

## §1 — What was measured

The frozen raid → same-direction displacement FVG → limit-fill entry (the exact mechanism that
returned 0/247 fills on US500 and was measured false as a price-behavior blocker on native MNQ/ES
data, `RESULTS_1M_DIAG.md`), simulated end-to-end on **native MNQ.v.0 continuous 1-minute bars**
(databento GLBX.MDP3, 2019-05-06 → 2026-08-23, 2,573,467 bars, $0.00 pull), against a
**reconstructed** exit (stop = swept-pool price ± 1 tick; target = PDH/PDL — the Pine exit
geometry is permanently lost, see the pre-registration's third 2026-08-24 disclosure).

| Stage | Result |
|---|---|
| Chain construction | 129,331 displacement FVGs → 26,105 raid-paired → 24,470 survive the arm-time geometry filters (`4x target/hurdle`, `target≥2R`) |
| Tradeability floor (ledger F8, flat Tradeify basis, 1.41pt) | 1,771 dropped (stop_dist too small to be a sane risk unit) → **22,699 valid trades** |
| **Stage 2 (cost-law, F1)** | mean gross R **+0.0631** · mean cost R **0.2636** · **ratio 0.239** (need ≥4.0) → **FALSIFIED** |
| Net of cost | mean net R **−0.2005** · **10.3%** of trades net-positive |

Bulenox basis (report-only, $0.61/side): ratio 0.234 — same conclusion, cost basis choice is not
what decides this.

**Read honestly:** the gross edge is small but **real and positive** — this is not a null result
manufactured by looking at the wrong number. It simply isn't large enough to survive round-trip
cost by anything close to the required margin. The construct clears no bar; it isn't ambiguous.

---

## §2 — Three real bugs found and fixed before this number could be trusted

This session ran the analysis **three times** before the result above was defensible. Recorded in
full because the debugging process is itself part of the evidentiary record — each fix is
independently verified, not just asserted.

1. **O(bars × pools) raid detection.** A first implementation called the frozen `detect_raid`
   primitive literally, per bar, over the full unswept-pool registry. `run_1m_diag.py`'s own
   `raid_bars` docstring had already diagnosed this exact mistake as "a multi-day runtime on 2.5M
   bars" — missed on first read, found the hard way (killed after ~7 CPU-hours, no result
   produced). Replaced with that file's verified O(bars + pools·log pools) heap-based
   implementation, extended (and re-verified bit-for-bit against the original across 8 synthetic
   seeds) to also track the swept price needed for stop placement.
2. **Missing target-side validation.** PDH/PDL can land on the wrong side of entry (price already
   crashed below yesterday's high before a long fires). Without a check, the target is trivially
   "hit" on the fill bar at whatever adverse price the market already sits at. Found via a −85R
   "trade" on 2020-03-02 (COVID crash) that violated the standing invariant every stop-hit trade
   must obey: `exit_price == stop_price` by construction, so gross R can never be below −1.0.
3. **Deadline-bar check-order bug.** The exit walk checked "have we reached the 16:00 ET flat
   deadline" *before* checking that same bar's own stop/target, so a gap through the stop landing
   exactly on the deadline bar exited at that bar's open instead of the stop. Found via 13 residual
   invariant violations (min −31.26R) on the **full** panel after fix #2 alone — a 300K-bar smoke
   test never surfaced it.

The `exit_price == stop_price` invariant is now a permanent `AssertionError` in
`run_stage2_costlaw.py`, not a one-off diagnostic. A future regression of this class hard-fails the
run instead of silently reporting a wrong verdict.

---

## §3 — What this does and does not license

- **Does not reopen** the family's standing `MNQ x ict-liquidity` DEAD verdict (`MNQFVG-1`/
  `MNQPOOL-1`) — this campaign's own pre-registration addressed that bar as a genuinely different
  construct (1-minute objects, real stop, session-reachable target vs. those probes' daily-horizon,
  stop-free, distant-target design) before running anything; the DEAD verdict itself is untouched.
- **Does not touch** any locked/frozen surface, allocation, `dd_protection` constant, Pine, or rail.
  Offline research only; the c1 rail stays disarmed throughout.
- **Closes the ICT-MNQ execution-layer question** raised by `RESULTS_1M_DIAG.md`'s own "that
  decision is now live for the operator ... it is not opened here" — it is now closed, on a
  measured number, not an assumption.
- **Re-proposal bar:** a genuinely different candidate mechanism on this cell, not a re-tuned
  parameter on this one (retraceK, pvLen, dispMlt, the reconstructed exit geometry) — matching the
  frozen pre-registration's own FM-2.

---

## §4 — Artifacts

- `mnq_1m.parquet` — **gitignored, regenerable at $0.00** (databento free-tier pull; not vendor-
  licensed bytes worth pinning). Re-pull with:
  ```bash
  python lab/databento_fetch/db_fetch.py pull --symbols MNQ.v.0 --stype continuous \
      --schema ohlcv-1m --start 2019-05-06 --end 2026-08-24 --phase oos \
      --campaign-id ict-1mexec-1 --max-cost 1.00 \
      --out lab/analysis/_inbox/ict_1mexec_1_2026-08/mnq_1m.parquet
  ```
  Expect 2,573,467 rows, span 2019-05-06 → 2026-08-23, $0.00 actual cost.
- [`build_1m_trades.py`](build_1m_trades.py) — native-bar trade generator (module docstring carries
  the full recovered-vs-reconstructed accounting and the three-bug history in detail)
- [`run_stage2_costlaw.py`](run_stage2_costlaw.py) — Stage 2 runner + the standing invariant check
- [`results_stage2_costlaw.json`](results_stage2_costlaw.json) · [`run_log_stage2.txt`](run_log_stage2.txt)
- [`reachability_attestation.md`](reachability_attestation.md) · [`search_params.json`](search_params.json) · [`admission.json`](admission.json)
- `discovery_manifests/ict-1mexec-1.json` — closed, 0/1 survivors, `K_intrinsic=1` spent
- Retrieved, pruned-upstream dependencies (git-show, not re-derived): `_run_1m_diag_retrieved_9aaa578.py`,
  `_run_1m_probe_retrieved_82575fc.py`, `_build_w_export_retrieved*.py`

## §5 — Audit hooks

```bash
# Confirm the invariant would catch a regression (re-run raises AssertionError on any violation)
cd lab/analysis/_inbox/ict_1mexec_1_2026-08 && python run_stage2_costlaw.py

# Confirm the closed manifest
cat discovery_manifests/ict-1mexec-1.json

# Confirm the DEAD verdict this campaign addressed is untouched
git log --oneline -- lab/archive/mnq_fvg_draw_probe_2026-08-04/

# Confirm the raid-detection reference file is unmodified from its retrieval
git show 9aaa578:lab/analysis/ict_mnq_2026-08/run_1m_diag.py | diff - lab/analysis/_inbox/ict_1mexec_1_2026-08/_run_1m_diag_retrieved_9aaa578.py | grep -v "^[<>] import build_w_export\|^[<>] import run_1m_probe\|^---\|^[0-9]"
```

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-24 | Campaign executed under operator GO. Three real bugs found and fixed via a standing `exit_price==stop_price` invariant (raid-detection performance/correctness, missing target-side validation, deadline-bar check-order) before the reported number could be trusted. Final verdict: `FALSIFIED` at Stage 2 (F1) — mean gross R +0.0631 vs. required 4x cost hurdle (ratio 0.239). `register_search close`: 0/1 survivors, `K_intrinsic=1` spent. | Claude Opus 5, operator GO |
