# DISC-CAMP-0 — CLOSURE: FALSIFIED — pipeline shakedown SUCCESS (real 0-column traversal executed), candidate hypothesis NULL

**Status:** `FINAL — Option B executed 2026-07-13` (operator selected Option B — run the real 0-column Stage-4→7 traversal before closing; see §Operator disposition and §Option B — executed below)
**Parent brief:** [`docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md`](rnd-pipeline/DISC-CAMP-0-shakedown.md)
**Pre-registration:** [`docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md`](pre-registration/DISC-CAMP-0-preregistration.md) (frozen commit `4b810a6` 2026-07-11; pre-pull staging amendment `b9bebaa` 2026-07-13 — both predate the first `pull`)
**Verdict (final, per §6 of the parent brief):** `FALSIFIED` — pipeline stages 0–7 traversed clean **on real data, non-vacuously**: **0 of 6** mined candidates cleared the Stage-4 IS cost-law triage, so zero candidates reached the OOS era; Stage-4 was executed against the real MGC OOS series (not skipped by inference) and correctly emitted the 0-survivor bundle; Stage-5/6/7 correctly detected the resulting marker and wrote `SKIPPED (0 candidates)` reports without crashing. No AMBIGUOUS-HOLD trigger fired anywhere in the chain.
**Run-id / manifest:** `disccamp0_gc_2010_18` — `discovery_manifests/disccamp0_gc_2010_18.json`, status `closed`, 0 survivors at naive α / Bonferroni / BH-FDR.
**Harness:** `lab/analysis/harvest/disccamp0_gc_2010_18/run_stage3.py` (commit `c783533`, 2026-07-13); binding artifacts `bind_k.py`, `block_size.py`, `series.py`.
**Disposition:** research layer only — no `core/`, allocation, `dd_protection`, `ACTIVE_FIRM`, or Pine touched (verified, empty diff — see Verification). Cumulative GC/MGC family K banked at **3,177** regardless of final disposition.

---

## Operator disposition — RESOLVED 2026-07-13: Option B

Two paths were both consistent with the pre-registered §6 gate (recorded verbatim below for the record):

**Option A — direct FALSIFIED close.** All 6 candidates died at the Stage-4 IS cost-law kill (`cost_law_pass: false` for every candidate, permutation p=1.0 for every candidate — not marginal, categorically dead). None of the six ever reaches an OOS return matrix column, so "zero candidates clear on the OOS era" is vacuously true — there would have been nothing left for Stage 5 (block-size/SPA), Stage 6 (temporal consistency), or Stage 7 (MGC realism) to test.

**Option B — run the formal 0-column Stage 4→7 traversal first, then close.** The parent brief's §5 forbidden-moves list explicitly warns against "declaring success on the traversal while quietly skipping the MGC realism gate — the micro gate is the whole reason GC/MGC was chosen; skipping it defeats the shakedown." That warning was written for a *surviving*-candidate scenario, but the pipeline-validation half of H-CAMP-0 ("does the assembled discovery→validation pipeline execute correctly end-to-end") was arguably still open: the 0-survivor code path through `emit_stage4` → `universe_gate` → `temporal_consistency` → `realism_mgc` had never actually been exercised end-to-end (only fixture-tested in the synthetic runner).

**Operator selected Option B 2026-07-13.** The Stage-4→7 drivers landed (Cursor, PR #364, 21/21 tests green) with the 0-survivor path as a first-class, tested deliverable; the traversal was then executed for real (see §Option B — executed below), discharging the recommendation stated in the prior draft of this section.

**Either way, unchanged:** the candidate-hypothesis verdict does not change — it is NULL on the mined tool ladder over this IS window, by a wide, unambiguous margin (see §Result). The Stage 4-7 traversal did not and could not alter that; it answered the separate procedural question (has the *pipeline* fully proven itself on real data, not by inference) — see §Option B — executed.

---

## Stage-by-stage execution record

| Stage | Ran? | Clean, or needed a fix? |
|---|---|---|
| 0 Register (pre-registration freeze) | Yes, 2026-07-11 | Clean at authorship; **amended pre-result** twice (K/V rule supersession 2026-07-12 per ADR; staging amendment 2026-07-13 for PD-1 below) — both amendments predate the first pull, so freeze-ordering integrity holds |
| 1 Pull | Yes, 2026-07-13 | **Needed a fix (PD-1):** first `estimate` attempt at the frozen IS start `2010-01-01` 422'd — corrected to the GLBX.MDP3 dataset floor `2010-06-06` before any pull. After correction: clean. GC.FUT parent `ohlcv-1h` (634,173 records) + `ohlcv-1d` (83,166 records), $0.00 billed, era-tagged cache (`--campaign-id disccamp0_gc_2010_18 --phase discovery`) |
| 2 Mine | Yes, 2026-07-13 | Clean, with one design addition: `miner.py` needed additive `run_stumpy`/`run_ruptures` stage flags (not previously exercised on real data) because PELT-RBF's O(n²) Gram matrix is intractable at ~52K hourly bars but tractable at 2,655 daily bars — STUMPY ran on the stitched 1h series, ruptures on the stitched daily series. Legacy default behavior byte-identical (9/9 tests). Runtime 1,965s (~33 min) |
| 3 Bind K | Yes, 2026-07-13 | Clean. Integrity gate held: recomputed T (51,659, from the pinned volume-lead stitch) reproduced K_DSR=3,177 exactly matching the bound `register_search open` manifest value — no drift between the binding-time computation and the mining-time recomputation |
| 4 Score (IS) | Yes, 2026-07-13 | Clean. All 6 candidates evaluated on IS only (holdout never touched — no OOS data exists on disk for this campaign at all yet, so IS-only selection is structurally enforced, not just policy); cost-law + permutation-p triage killed all 6 |
| 5 Block size | Bound 2026-07-13; **real driver run 2026-07-13** | `block_size = 3` bound from the stitched GC 1h IS return ACF (first lag inside the 95% white-noise band), per §2.2's rule. `run_stage5_6.py` executed against real MGC OOS data; detected the Stage-4 0-survivor marker and wrote a `SKIPPED (0 candidates)` gate report — clean, no crash, no fabricated columns |
| 6 Confirm (OOS) | **Real driver run 2026-07-13** | No candidate survives to feed it (0 columns) — `run_stage5_6.py`'s temporal-battery half detected the same marker and wrote `SKIPPED (0 candidates)`, same invocation as Stage 5 |
| 7 Realism | **Real driver run 2026-07-13** | No candidate survives to feed it — `run_stage7.py` detected the marker and wrote a `SKIPPED (0 candidates)` report; the MGC realism engine (`reconstruct_gross_gc`/`ratio_clause`/`hurdle_clause`) was never invoked because there was nothing to evaluate, which is correct, not skipped-by-omission |
| 8 Breadth | Not run | No candidate survives to feed it; Stage 8 (`lab/research_utils/breadth.py`, Track C) awaits a real DISC-CAMP-0 (or future campaign) survivor — out of scope for this closure, unaffected by Option B |

---

## Result — the six candidates (all killed at Stage 4)

Tool ladder as pre-registered, no sweep: STUMPY motif (argmin) + discord (argmax) at each of the 3 frozen windows m∈{30,60,90}; horizon=3 bars, trigger-quantile=0.05 (landed module defaults, not re-chosen). Cost hurdle: 4× MGC round-trip cost at the IS-mean stitched close ($1,355.12) = **+9.56 bp**.

| Candidate | n (IS trades) | mean net trade | vs. +9.56bp hurdle | perm. p | cost-law |
|---|---|---|---|---|---|
| motif_m30 | 2,063 | −2.02 bp | fail | 1.0000 | FAIL |
| discord_m30 | 2,333 | −2.19 bp | fail | 1.0000 | FAIL |
| motif_m60 | 2,242 | −2.05 bp | fail | 1.0000 | FAIL |
| discord_m60 | 2,311 | −1.67 bp | fail | 1.0000 | FAIL |
| motif_m90 | 2,109 | −1.04 bp | fail | 1.0000 | FAIL |
| discord_m90 | 2,256 | −0.40 bp | fail | 1.0000 | FAIL |

`register_search close` result: **0 of 6** pass naive α=0.05 (0 "significant" even before any multiplicity correction — expected ~0.3 false positives at this K under the global null, and even the loosest possible bar found none); 0 pass Bonferroni (threshold 1.574e-05); 0 BH-FDR survivors. **K_SPA binds 0.**

All six candidates are net-*negative* in expectation on IS, not merely sub-hurdle — the miner did not surface a marginal, cost-killed edge; it surfaced nothing resembling an edge at all on this tool ladder over this window.

**Cumulative GC/MGC family K after this campaign: 3,177** (prior = 0). Banked for the next GC/MGC campaign's DSR denominator.

---

## Process-defect log (dated) — the primary deliverable of this shakedown

Per the parent brief's §9, this log — not the null result itself — is what the shakedown exists to produce.

**PD-1 (2026-07-13, FIXED same session) — frozen IS start predates the dataset's actual availability.** The original pre-registration froze IS start at `2010-01-01`; GLBX.MDP3's actual floor is `2010-06-06`. The first `estimate` call failed `422 data_start_before_available_start` inside `client.metadata.get_cost`, not at a friendlier pre-check. Corrected pre-result via a staging amendment (commit `b9bebaa`) before any pull. **Fix landed:** `db_fetch.py estimate()` now calls `_check_request_in_range()` right after a successful `get_dataset_range` fetch, comparing the requested `--start`/`--end` against the per-schema (preferred) or dataset-wide available window and `sys.exit`-ing with a clear, actionable message *before* `get_cost` — same behavior on a failed range fetch (non-fatal, unchanged). 8 new tests (`tests/test_db_fetch_pd1_pd2.py`), TDD (red-then-green), including the "prefers per-schema range" and "skips cleanly on fetch failure" cases.

**PD-2 (2026-07-13, FIXED same session) — non-atomic cache write.** `db_fetch.py pull()` streamed `data.to_file(path)` directly to the final cache path. A mid-stream failure (the PD-1 422 actually happened *before* any write attempt, so this did not bite in practice this session) would leave a partial/corrupt file at the real cache path, which the next invocation's `path.exists()` check would then silently treat as a valid cache hit — no re-billing, but also no correctness. **Fix landed:** writes now go to a same-directory `.tmp` path, then `os.replace()` atomically into the final cache path (atomic on POSIX and Windows), with cleanup-on-exception; `_cache_path()`'s hashing scheme is untouched (every existing era-tagged cache entry still hits). Covered by the same 8-test file above (crash-mid-write leaves no final-path file; failure-then-retry recovers cleanly; a valid cache entry still short-circuits to a cache hit).

**PD-3 (2026-07-13, FIXED same session) — `register_search open --params` round-trips through PowerShell/argparse into a non-JSON-valid string.** The manifest's `params` field for this run (`disccamp0_gc_2010_18`) contains literal backslash-escaped quotes (`\"...\"` as text, not parsed JSON) — a shell-quoting artifact, not a `register_search.py` bug per se, since the tool offered no escape hatch around it. The provenance intent (K-rule citation, T, T-series description) is still human-readable in the stored string as-run, so nothing about THIS campaign's record was lost — but the field cannot be machine-parsed as JSON as stored, and this run's manifest is left as-is (immutable once opened, per the tool's own discipline). **Fix landed:** new `--params-file <path>` option reads a JSON file directly, validates it parses before ever touching the manifest, and errors clearly if both `--params` and `--params-file` are given or if the file isn't valid JSON — bypassing shell quoting entirely for any future campaign's `register_search open` call. 5 new tests (`tests/test_register_search_params_file.py`), TDD, legacy `--params` behavior confirmed byte-identical when `--params-file` is omitted.

**PD-4 (2026-07-13) — `estimate()`'s dataset-range guard was print-only, not a gate.** Directly related to PD-1; same fix (see PD-1 above — this was the other half of the same defect, now closed by the same `_check_request_in_range` addition).

**PD-5 (2026-07-13, observation, not a defect) — degraded-quality data days.** Databento flagged 2014-06-11 through 2014-06-13 as "reduced quality" (`BentoWarning`) in the GC 1h pull. Not investigated further (does not affect the all-null verdict — three degraded days out of 2,655 cannot flip a −6-for-6 result), but logged in case a future campaign's window includes these dates and the effect is less clearly immaterial.

**PD-6 (2026-07-13, observation, not a defect) — the frozen ruptures PELT penalty (10.0) found 1 segment / 0 breaks on the full 2,655-day IS daily series.** This is a real, if slightly surprising, output of a genuinely-fixed, non-swept penalty — not a bug, and per the parent brief's §5 forbidden moves, **was not retuned** to "find" breaks. Logged because a future campaign reusing this frozen penalty on a different instrument/window should not be surprised by a similarly degenerate segmentation, and because it is a candidate diagnostic for whether penalty=10.0 is well-calibrated for GC daily returns specifically (a question for a *future* pre-registration, not this one).

**PD-7 (2026-07-13, observation, not a defect) — the block-size ACF rule, applied exactly as frozen, is not monotonic.** `block_size=3` (first lag inside the 95% white-noise band) is correct per the pre-registered rule, but the ACF re-exceeds the band at lags 7–13 (max |ρ|=0.0169 at lag 11) before settling. The frozen "first-in-band" rule does not require monotonic decay, and none was retuned or second-guessed — but this is worth a future methodology note on whether "first-in-band" or "last-in-band-before-sustained-quiet" is the more robust convention for block-bootstrap dependence-horizon selection.

---

## Option B — executed 2026-07-13 (real 0-column Stage-4→7 traversal)

Drivers per [`docs/briefs/rnd-pipeline/2026-07-13-cursor-handoff-stage-4-7-drivers.md`](rnd-pipeline/2026-07-13-cursor-handoff-stage-4-7-drivers.md) (Cursor, PR #364, 21/21 offline tests green — re-confirmed in `.venv-research` before this run). Executed operator-side (data pull + real-data invocation are explicitly not Cursor's to fire per that handoff's §5).

**1. MGC OOS pull.** `databento-data` skill's mandatory dry-run first:
```
PYTHONPATH=lab python -m databento_fetch.db_fetch estimate --symbols MGC.FUT --stype parent --schema ohlcv-1h --start 2019-05-06 --end 2026-07-01
# [estimate] cost: $0.0000 USD (streaming); billable ~0.0183 GB; 326,136 records
```
Pull, era-tagged into the OOS cache slot (`--campaign-id disccamp0_gc_2010_18 --phase oos`, distinct from the Stage-2 IS cache):
```
PYTHONPATH=lab python -m databento_fetch.db_fetch pull --symbols MGC.FUT --stype parent --schema ohlcv-1h --start 2019-05-06 --end 2026-07-01 --max-cost 1.00 --campaign-id disccamp0_gc_2010_18 --phase oos
# [done] 326,136 rows in cache; $0.00 billed
```

**2. `run_stage4.py --real-oos`.** Loaded the 6 frozen IS-dead candidates (`stage3_frozen_rules.json`), built the MGC OOS stitched series (volume-lead, within-contract returns — same conventions as the IS series), found 0 IS-cost-law survivors (matches Stage-3: all 6 `cost_law_pass: false`), and emitted the §0.5(E) zero-survivor bundle:
```json
{"k_spa": 0, "k_dsr": 3177, "zero_survivor": true}
```
`disccamp0_stage4__stage4_matrix.meta.json` records full kill provenance (all 6 candidates, `cost_law_pass: false`, IS p=1.0 each) plus the real MGC OOS cost convention (`cost_price_input_oos_mean_close: 2304.19`, vs the IS convention's `1355.12` — expected, different era/instrument mean). `disccamp0_stage4__stage45_skipped.json` marker written alongside.

**3. `run_stage5_6.py --run-id disccamp0_stage4`.** Detected the stage45 marker on its first check (before touching `universe_gate`/`temporal_consistency`) and wrote `SKIPPED (0 candidates)` reports for both Stage 5 (`disccamp0_stage4__stage5_gate_report.json`) and Stage 6 (`disccamp0_stage4__stage6_battery_report.json`). Exit 0, no crash — this is the AMBIGUOUS-HOLD trigger's negative case holding.

**4. `run_stage7.py --run-id disccamp0_stage4`.** Same marker-detection path; wrote `SKIPPED (0 candidates)` (`disccamp0_stage4__stage7_realism_report.json`). The MGC realism engine (`reconstruct_gross_gc`/`ratio_clause`/`hurdle_clause`) was never called — correct, since there is nothing to evaluate, not an omission.

**Result:** the pipeline traverses clean end-to-end on real data with a genuinely empty candidate set — Stage-4 evaluated real OOS bars and correctly found nothing to promote; Stages 5/6/7 correctly recognized the empty state and degraded gracefully rather than crashing or fabricating output. This is the non-vacuous version of "traverses clean" the draft's Option B reasoning called for. All 5 emitted artifacts are committed alongside this closure note.

**PD-8 (2026-07-13, observation, not a defect) — degraded-quality days in the OOS pull.** Databento flagged several OOS-era days as reduced-quality (`BentoWarning`) during the MGC 1h pull, visible before SDK message truncation: `2020-02-27`, `2020-02-28`, `2020-06-30`, and at least one more truncated by the warning's own formatting (not re-queried further — re-running `pull` is a pure cache hit and would not re-surface the full list; chasing it further is not warranted, see below). Same class as PD-5 (IS-era degraded days) — logged for a future campaign whose window includes these dates; immaterial here since the categorical 0-survivor result does not turn on data quality on any specific day (all 6 candidates failed cost-law by wide, uniform margins, not a borderline result a few noisy days could flip).

---

## Verification

```bash
# Pre-registration predates the first pull (freeze ordering)
git log --format='%h %ad %s' --date=short -- docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md
# Expect: b9bebaa (2026-07-13, staging amendment) and 4b810a6 (2026-07-11, original freeze)
# both dated before/at the first pull (2026-07-13, same session, staging amendment committed first)

# Manifest is CLOSED, 0 survivors, K=3,177
python -c "import json; d=json.load(open('discovery_manifests/disccamp0_gc_2010_18.json')); print(d['status'], d['K'], d['results']['n_pass_bh'])"
# Expect: closed 3177 0

# All 6 candidates categorically fail cost-law (not marginal)
python -c "
import json
d = json.load(open('lab/analysis/harvest/disccamp0_gc_2010_18/stage3_report.json'))
assert len(d['candidates']) == 6
assert all(c['cost_law_pass'] is False for c in d['candidates'])
assert all(c['is_pvalue'] == 1.0 for c in d['candidates'])
print('OK: 6/6 candidates, all cost_law_pass=False, all p=1.0')
"

# T/K integrity (recomputation matches the bound manifest K)
grep -n "integrity OK" <(PYTHONPATH=lab python -c "
import json
d = json.load(open('lab/analysis/harvest/disccamp0_gc_2010_18/stage3_report.json'))
assert d['integrity']['T'] == 51659
assert d['integrity']['k_dsr'] == d['integrity']['manifest_K'] == 3177
print('integrity OK: T=51659 k_dsr=manifest_K=3177')
")

# No locked-constant / allocation / dd_protection / Pine touch BY THIS CAMPAIGN
# (scoped to this campaign's own commits, b9bebaa..HEAD — core/dd_protection.py DOES
# differ vs the older 4b810a6 pre-reg-freeze commit, but that delta is unrelated prior
# work: PR #356 engine pre-flight + the dd_geometry concept-not-constant ADR, both
# landed on main BEFORE this campaign's b9bebaa staging amendment — verify via
# `git log 4b810a6..b9bebaa -- core/dd_protection.py` if re-checking from scratch)
git diff --stat b9bebaa HEAD -- core/config/params.toml core/dd_protection.py core/portfolio_mc.py
# Expect: empty
```

Note: closure notes in this repo (`Q-BTC-1`, `Q-PERSIST-1`, `Q-DECAY-1`, etc.) are narrative records, not a `check_brief`-gated type — none of them invoke it, and neither does this one.

### Option B execution — verification

```bash
# MGC OOS cache is present and era-tagged distinct from the IS cache
PYTHONPATH=lab python -c "
from series import mgc_oos_cache_exists
assert mgc_oos_cache_exists(), 'MGC OOS cache missing'
print('OK: MGC OOS ohlcv-1h cache present')
"

# Stage-4 real run: 0 survivors, K bracket matches the bound manifest value
python -c "
import json
m = json.load(open('lab/analysis/harvest/disccamp0_gc_2010_18/disccamp0_stage4__stage4_matrix.meta.json'))
assert m['zero_survivor'] is True
assert m['k_spa'] == 0
assert m['k_dsr'] == 3177
assert len(m['kill_provenance']) == 6
assert all(c['cost_law_pass'] is False for c in m['kill_provenance'])
print('OK: Stage-4 real 0-survivor bundle matches expected provenance')
"

# Stage-5/6/7 all detected the marker and SKIPPED cleanly (no crash, no AMBIGUOUS-HOLD)
python -c "
import json
for stage, fname in [(5, 'stage5_gate_report'), (6, 'stage6_battery_report'), (7, 'stage7_realism_report')]:
    d = json.load(open(f'lab/analysis/harvest/disccamp0_gc_2010_18/disccamp0_stage4__{fname}.json'))
    assert d['verdict'] == 'SKIPPED', f'Stage {stage} did not report SKIPPED'
print('OK: Stage 5, 6, 7 all report SKIPPED (0 candidates)')
"

# No data-acquisition / ledger-mutation calls inside the drivers themselves
grep -rn "Historical(\|get_range\|get_cost\|metadata\." lab/analysis/harvest/disccamp0_gc_2010_18/run_stage4.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage5_6.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage7.py
grep -rn "register_search" lab/analysis/harvest/disccamp0_gc_2010_18/run_stage4.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage5_6.py lab/analysis/harvest/disccamp0_gc_2010_18/run_stage7.py
# Expect: no matches for either

# check_boundaries stays green
python scripts/check_boundaries.py
```
