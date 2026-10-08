# CC handoff — T00 step-12 diagnostic, Tier 1: reproduce and explain (session level)

**Date:** 2026-10-08.
**Status:** Tier 1 ADMITTED by Joshua, 2026-10-08, directly to the step-12 owner session: "I'll admit tier 1". The admission covers this card's real-source run only: the sealed replay of at most 18 already-scored step-12 paths, outside [build card](2026-10-03-t00-screen-authority-build-card-DRAFT.md) §7. Execution starts after this card merges and the executor is named.
**Brief type:** CC handoff, executor packet (diagnostic, non-decision-bearing).
**Owner:** the T00 card owner (coordinator (4)). The executor delivers one report. The deployment coordinator keeps combined acceptance, and Joshua keeps investment decisions.
**Subject:** the step-12 result recorded in #724 (`NO-GO-evidence-robust`, `VERIFIED`; results `a5b985d0…42dc`, attestation `f627e805…1ed5`, REPORT `bebceb93…9984`), run from H `5d25f9cfc1e8ff00bacda45478322f9858176e8b`.
**Return boundary:** a private report plus a public return of hashes and labels only, or BLOCKED / NEEDS_CONTEXT exactly where §5 says.

## §0 — Production reads

Read at H `5d25f9c` on 2026-10-08. Re-read at dispatch.

| Surface (H `5d25f9c`) | Use |
|---|---|
| `production_source.py:926-936` `_seal`; `:1232-1254` `replay_bracket` (H `5d25f9c`) | For a source-only contract (r3c), `replay_bracket` returns `SourceOnlyBracket`. Per session it carries `pnl`, `intraday_low`, `fills`, `flat_before_deadline`, `start_flat` and `end_flat`; per run it carries `events_sha256`, the consumed-split placements and `deadline_failure`. **It never returns the event stream.** |
| `production_source.py:1183-1199` `_verify_integrity`, `:1210-1214` `_check_path` (H `5d25f9c`) | Every `replay_bracket` call re-runs the full integrity check, about 71 s (design §6.2). |
| `p7_driver.py:39-48` (H `5d25f9c`) | The admitted construction: `validate_source_contract` → `ProductionSource.build(receipt, artifact_root=…)` → `replay_bracket(path)`. Tier 1 uses this pattern and nothing else. |
| `t00_screen/worker.py:162-182` (H `5d25f9c`) | The retained PATH identities: `path_sha256`, and per run a `digest` over `[rows, events_sha256]`, where each row is `[source_session_id, occurrence, float.hex(pnl), float.hex(intraday_low), fills, flat_before_deadline, start_flat, end_flat]`. Each of these is computable from the sealed output, so a re-execution can be matched exactly. |
| `t00_screen/plan.py:42` `seed`, `:120` `rebuild_candidates`; `worker.py:344-346` (H `5d25f9c`) | Path re-assembly from a key: the retained `manifest.json` candidates, `seed(purpose='path', …)`, `PathAssembler(path_start_date).sample(…)`. |
| `replay.py:164-631`; `book_policy.py:65-114` (H `5d25f9c`) | The raw event kinds (`fill` with qty, price, side, commission and reason; `refused`; `capacity_takeover_*`; `session_mode`; `bar_equity`), and the replay's protection policy, `candidate_book_protection_policy()` (trailing, trigger `0.01`, scale `0.40`). Both are **Tier 2 only**: see §2. |

## §0.5 — Prerequisites (each must hold before the first replay; otherwise BLOCKED)

1. **Window.** Every replay must finish before **2026-10-14T02:08Z**, when the r3c source approval `2cc7195e…` expires. After that, `ProductionSource` refuses unless Joshua signs a renewal over the same r3c bytes. No renewal is requested by this card.
2. **Code and environment.** Run from a clean detached worktree at H (`core.autocrlf=false`, clean with `--untracked-files=all`) on the operations venv. The interpreter and venv must be unchanged during the run, and the worktree must be clean before and after.
3. **Inputs.** Re-hash the r3c contract, the source approval and the registry against the pins in build card §8. Any mismatch is BLOCKED.
4. **Entry point.** Only `ProductionSource.build` and `replay_bracket`. **Forbidden:** `screen_bracket`, `screen_epoch`, `_engine`, `_replay_raw` and `replay`; any attribute access that reaches unsealed results; any edit under `ops/`, `core/` or `scripts/`. If the report needs more than the sealed output gives, return NEEDS_CONTEXT naming Tier 2. Do not work around it.
5. **Host.** No overlap with a heavy run booked by the deployment coordinator (#651). The diagnostic runs as one process of about 0.6 GiB.

## §1 — Purpose and non-goals

The purpose is to determine, from at most 18 already-scored paths, whether the step-12 failures show a credible portfolio-construction mechanism worth a controlled test. The output is an attribution report. It is not a bust-rate estimate, a replacement book or qualification evidence, and selected cases cannot estimate population rates or prove that changing a mechanism helps.

## §2 — Evidence: Tier 1 versus Tier 2

| Draft evidence item | Tier 1 (sealed) | Needs Tier 2 (raw events) |
|---|---|---|
| Equity against the drawdown floor, per session | Yes: cumulative `pnl` and `intraday_low`. Floor crossings computed here are **descriptive**; the kernel status stays the retained one, because `evaluate_replay` refuses sealed input | — |
| Bust timing, and shock versus grind | Yes: the first session the descriptive floor is crossed; the `intraday_low` gap at that session | — |
| Recovery on passing paths | Yes: depth and duration of drawdowns before the pass day | — |
| Activity | Yes: `fills` per session | — |
| Each strategy's contribution | — | Yes |
| Protection state and its changes (`session_mode`) | — | Yes |
| Requested and filled base and add quantities | — | Yes |
| Capacity refusals, takeovers, forced closes, costs | — | Yes |

Tier 2 needs a reviewed capability that returns raw events for a diagnostic evidence class. That is a code change, so it means a new H, review, a P7 re-run at that H and new signatures. Scope it only if Tier 1 shows a mechanism worth attributing.

## §3 — Sample

- **Strata:** population (FULL, H1, H2) × retained class (agreed PASS, agreed FAILURE, `UNDETERMINED`, read from `bracket_status`). That gives 9 strata of 2 paths each, 18 in all.
- **Rule:** within each stratum, sort the keys by `sha256(canonical_json_bytes(key))` ascending and take the first two. Freeze the 18 keys before any replay. The key list stays private; the return carries its SHA-256.
- The `UNDETERMINED` stratum's R1/R2 composition is accepted as the hash rule draws it, and is not rebalanced.

## §4 — Hypothesis and falsifier

**H (reproduction):** a sealed `replay_bracket` re-execution at H of each selected path reproduces its retained `path_sha256`, and per run its `digest`, `events_sha256`, `consumed_intrabar_splits_sha256` and `deadline_failure`, byte for byte.

**Falsifier:** any one mismatch falsifies H. The run stops at that path, with no replacement and no retry.

The mechanism reading (shock versus grind, recovery depth) is descriptive and conditional on H holding. It is not a gate and does not test a mechanism.

## §5 — Sequence, stops and verdict

1. Re-assemble all 18 paths. Each one's `path_sha256` must equal its retained PATH record **before any replay**. A mismatch is FALSIFIED, and nothing is replayed.
2. **Checkpoint:** replay the first FULL agreed-FAILURE key, check its identities under §4, and measure the CPU and wall time.
3. If the checkpoint matches and its cost is within §7, replay the other 17.
4. **Stop on:** any identity mismatch; a refusal (for example `SOURCE_APPROVAL_EXPIRED`); the budget in §7. Never replace a path, change a comparison criterion or retry automatically. A stop returns partial evidence.

## §6 — Return and verdict

**Verdict on H:** **RESOLVED** if every replayed path matches and the report is delivered. **FALSIFIED** if any identity mismatches. **AMBIGUOUS** if a prerequisite, refusal or budget stop leaves fewer than 18 paths replayed with no mismatch.

**Status (exactly one):**
- **DONE:** 18 paths replayed, H RESOLVED, report delivered.
- **DONE_WITH_CONCERNS:** all of DONE, plus a named concern. A mismatch is never this.
- **NEEDS_CONTEXT:** a missing fact or ruling, including evidence that only Tier 2 can supply. Name it.
- **BLOCKED:** a §0.5 prerequisite fails, H is FALSIFIED, a refusal, or the budget stops the run. State the exact obstruction.

- **Private** (outside every worktree, in the private root): the frozen key list, per-path sealed series, the report, and the stdout, stderr and timing of each step.
- **Public** (to coordinator (4)): the key-list SHA-256; the match result per path (MATCH / MISMATCH, by ordinal 1–18, with no keys); the §5 verdict; report SHA-256; CPU and wall time. No counts, rates or values.
- **Report contents:**
  1. Reproduction results and evidence identities.
  2. Session-level explanations of failures, and contrasting recoveries.
  3. Supporting and contradicting session-level evidence for a shock or grind mechanism. Any claim that would need Tier 2 data is marked as such.
  4. One recommendation: Tier 2 scoping, a controlled repair comparison, fresh research, or a precisely stated remaining uncertainty.

## §7 — Budget

The step-12 run took 8 h 21 m on 8 workers for 3,006 paths, about 80 s of wall time per path per worker, with integrity hoisted. `replay_bracket` adds about 71 s of integrity per call, so expect about 150 s per path. The source build takes about 3 min.

- Estimate: about 50 min for the checkpoint plus 17 paths.
- **Ceiling: 2 CPU-hours and 3 h of wall time, at most 18 paths and 36 bracket runs.**
- **Checkpoint stop:** if path 1 costs more than 1.5 × 150 s, return with the measurement.

## §8 — Exposure

The diagnostic reads per-session detail for scored step-12 paths, beyond the verdict. The executor logs every reader (name, date, and what they saw: series, report or neither) with the private report. Any successor pre-registration, for example of an adjusted book, must carry an exposure statement that names these readers (design §4.5).

## §9 — Forbidden moves

- Any change to the book, the ports, the parameters or protection; any alternative or repair run; beginning qualification.
- Any entry point other than §0.5 item 4; any code change; GLM or any external service.
- New simulations, resampling, threshold changes or resizing.
- Any private value (counts, rates, P&L, keys, Pine or port bodies) in a public surface.
- Treating `NO-GO-evidence-robust` as statistical confidence or out-of-sample validation.
- Writing to, or changing, the step-12 run directory.

## §10 — Audit hooks

```bash
# Card form (expect RESULT: well-formed).
python -I scripts/fp.py python scripts/check_brief.py --type handoff docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md

# The sealed boundary this card relies on (expect SourceOnlyBracket returned for source-only contracts).
git show 5d25f9c:ops/c1_rail/qualification/production_source.py | sed -n '1232,1254p'

# The admitted construction pattern.
git show 5d25f9c:ops/c1_rail/qualification/p7_driver.py | sed -n '39,48p'

# Retained identities the reproduction compares.
git show 5d25f9c:ops/c1_rail/qualification/t00_screen/worker.py | sed -n '162,182p'

# No private value in this card (expect no output).
rg -n "P&L =|\\$[0-9]{2,}|account [0-9]" docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md | grep -v 'rg -n'
```
