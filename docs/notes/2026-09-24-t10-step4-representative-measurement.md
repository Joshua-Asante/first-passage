# T10 step 4 — representative workload measurement (first pass, 2026-09-24)

**Status:** STARTED — first pass returned. Packet: [T10 source and freeze packet](../briefs/handoffs/2026-09-21-tradeify-t10-source-and-freeze-packet.md) §2 step 4 (contradiction 4).
**Class:** `TEST_ONLY_SYNTHETIC_REDUCED_DEPTH_NOT_DECISION_BEARING`. The only fixture used is the repository's own signed TEST_ONLY composition fixture: invented ports, calendar and panels, with keys generated fresh on each run. No private port, panel, account figure or qualification stream was read. No real attempt was used as a benchmark, and no stage above N2's reduced depth was run. **No numerical budget is proposed or approved**; that decision belongs to the operator.

**Harness files** are kept as `.py.txt` so the repo import-boundary gate does not treat them as modules; bytes and recorded SHA-256 are unchanged, and each runs from the checkout root after renaming to `.py`.

**Tree measured:** `0c12dab`, whose contents are identical to `main@2f2e751` (#485). Runs used one process on the operations launcher interpreter: CPython 3.13.2, executable `d70fced7…`, on Windows 11 build 26200. Nothing else ran alongside, but other system activity was not isolated. Raw data, harnesses and source hashes are in [2026-09-24-t10-step4/](2026-09-24-t10-step4/).

## 1. Signed TEST_ONLY composition, split by component

Harness: [`measure_composition.py`](2026-09-24-t10-step4/measure_composition.py.txt) (`3f536ee3…`). It runs the same route as `tests/ops/qualification/test_composition_route.py`: `build_verified_composition`, then the signed preflight and journal, then `_run_composition_e1` (N1, CUTOFF, N2 with Part B, Part A), then runtime inventory, the frozen adjudicator and result-envelope validation.

Four `ProductionSource` methods are timed with exclusive self-time wrappers, so a nested call counts only toward its own bucket:
- **runtime:** `replay`.
- **proof:** `proof`, `verify_for` and `_build_composition`.
- **controller:** everything else in the E1 run (journal, checkpoint dispatch and receipts, budget checks, stage adjudication).

The wrappers are removed before adjudication. Left in place, the frozen adjudicator's runtime-inventory check refuses them, which it did on the first probe. That refusal is the integrity guard working.

Fixture geometry: 174 sessions, 4 bars per session per leg, 4 legs, horizon 5 sessions, Part A 2→4 panels × 2 paths. Three sequential repeats per depth:

| confirmation depth | paths | E1 wall, median (min–max) s | runtime (path replay) s | proof s | of which `verify_for` s (calls) | controller residual s | setup s | adjudication + envelope s |
|---|---|---|---|---|---|---|---|---|
| 2 | 16 | 42.66 (42.19–42.76) | 2.72 | 38.31 | 38.26 (32) | 1.52 | 16.85 | 31.58 |
| 10 | 40 | 75.54 (73.56–78.65) | 3.50 | 69.98 | 69.87 (56) | 2.06 | 17.78 | 46.13 |
| 30 | 96 | 169.31 (165.58–178.11) | 4.73 | 161.48 | 161.48 (107) | 3.05 | 21.26 | 35.21 |

Depth 30 ran at alpha 0.05, and its synthetic N2 decision did not pass, so Part A did not run. The pass/fail outcome of invented data carries no meaning. The row is kept for cost only.

Peak process memory was 124–129 MB. Journal size was 94–115 KB, path inventory 4–10 KB and result envelope about 2.7 KB.

**Finding.** Source re-verification dominates, and path replay is small.
- `verify_for` runs once per replayed path plus once per checkpoint admission. Each call costs about 1.2–1.5 s on this fixture.
- The cost is `_execution_snapshot`: a recursive hash over the issued source's whole object graph, about 217k objects at this size (cProfile, one call).
- The controller residual stays at 1.5–3 s across depths. Setup and adjudication are roughly fixed per run.

## 2. How `verify_for` scales with source size

Harness: [`scale_verify.py`](2026-09-24-t10-step4/scale_verify.py.txt) (`f3182a1d…`). It uses the same fixture with a longer interval or more bars per session (extra bars placed 09:30–15:30 ET, inside the retained interval), and times `verify_for` three times each:

| source | sessions | bars (4 legs) | `verify_for` s (3 calls) |
|---|---|---|---|
| 8 months × 4 bars | 174 | 2,784 | 1.16 / 1.30 / 1.19 |
| 16 months × 4 bars | 350 | 5,600 | 2.54 / 2.52 / 2.59 |
| 32 months × 4 bars | 695 | 11,120 | 4.66 / 4.66 / 5.24 |
| 8 months × 16 bars | 174 | 11,136 | 3.07 / 2.98 / 3.01 |
| 8 months × 29 bars | 174 | 20,184 | 5.15 / 5.14 / 5.04 |

The bar counts are sessions × bars per session × 4. The JSON's `panel_bytes` and `panel_bars_all_legs` fields read 0 because of a key-lookup bug in this probe; they are not source facts. Over the measured range, cost fits a linear model: about **3.2 ms per session plus 0.23 ms per bar**. Both the interval-length rows and the bar-density rows agree with it.

**Linear extrapolation, not measured.** The accepted cold-replay source spans 2022-09-01 to 2026-09-03 and holds about 95k M15 bars per leg (Aegis 94,893 and Vanguard 94,617, per the phase-1 note). That is about 380k bars and roughly 1,000 sessions, 19× beyond the largest measured size. The model then gives about 89 s per `verify_for` call.

At one call per path:
- The draft E1 ordinary workload (23,510 paths) would spend about 580 h on re-verification alone.
- The 200-panel reserved maximum (43,510 paths) would spend about 1,080 h.
- Sole n3 (2,910 paths) would spend about 72 h.

For comparison, the 2026-09-16 linear illustrations for replay were 66 h, 122 h and 8.2 h. If the extrapolation holds, the per-path whole-source snapshot is the budget-dominant term, about 9× replay. That makes it a design question for the qualification owner, not a measurement to scale up.

This note changes nothing. The snapshot is an integrity control, and any change goes through its owner and that change's own acceptance.

## 3. The 500-session synthetic benchmarks, re-run at HEAD

Harness: [`bench500.py`](2026-09-24-t10-step4/bench500.py.txt). It re-runs the recorded commands `c1_rail.qualification.benchmark` and `benchmark_part_a` with `--horizon 500 --seed 791946223`, three sequential repeats each, as subprocesses.

**Output digests are unchanged** from the 2026-09-16 record: path `744a5972…` and Part A `185561d9…`, identical across all repeats. The engine moved at `7ba7844`, but its output on these synthetic shapes did not.

| workload | subprocess wall s (3 repeats) | 2026-09-16 median |
|---|---|---|
| 500-session path | 15.39 / 13.74 / 15.55 | 10.09 |
| Part A panel + path | 25.24 / 14.64 / 15.20 (internal total 17.61 / 12.47 / 12.64) | 11.47 |

Subprocess wall includes interpreter start. The 2026-09-16 runs used CPython 3.12.14 in-process, so these walls are not a like-for-like regression signal. The Part A internal components at the median repeat (12.64 s total) were:
- path replay/kernel: 7.33 s
- proof rebuild: 2.73 s
- serialization: 1.83 s
- source build: 0.76 s

These benchmarks bypass `ProductionSource`, so they do not include the re-verification cost found in §1–2.

## 4. What this pass does not cover, and what comes next

- **Horizon 500 inside the signed composition.** The signed fixture's horizon is 5 sessions, pinned in both the TEST_ONLY workload policy and the contract document. Per-path replay at horizon 500 comes from §3, not from the signed route. A signed composition at horizon 500 needs a fixture extension. It is the next measurement.
- **Re-verification at real-source object counts.** §2 is an extrapolation. Confirming it takes one `verify_for` timing on a synthetic source of about 1,000 sessions × 92 bars × 4 legs. That is a cheap next probe, and it needs no private data.
- **Not measured:** controller costs of the execution service, runtime capture, and durable G5 signing and transport. These are in `ops/c1_rail/qualification/execution/*`, outside the in-process composition route. They are still owed for the full controller/proof/runtime split.
- **Private-port replay cost** needs the corrected ports on the primary checkout (`FP_PORT_ROOT`; see the phase-1 note §Operator confirmation). It is outcome-bearing on real panels, so it needs its own authorization. It is not a step-4 default.
