# Cursor Handoff — `register_search` HARD-gate: block open of mechanism-first campaigns without a reachability attestation

**Date:** 2026-07-14
**Parent session:** Claude Code operator session (Joshua + Claude) — authoring the mechanical enforcement handoff the HARV ADR deferred as "separate implementation handoff." The doctrine (ADR 2026-07-13 §2.4) is already `Accepted`; this build makes the code catch up.
**Spawn target:** Cursor (frozen-spec implementation — see [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md); §0.5 uses the Cursor variant). `register_search.py` is **stdlib-only by design** — no venv/deps concern, runs on any Python the repo already uses.
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (multi-step)
**Parent question:** HARV lane ADR ([`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md)) §2 point 4 — the **HARD gate**: "the reachability simulation … blocks `register_search open` until every bundled clause has a written reachability attestation in the campaign's pre-registration." §6 Downstream: "Optional later: mechanical `register_search open` guard (separate implementation handoff — doctrine binds now; code may lag)." This handoff is that guard.
**Authority:** Joshua (CEO). Claude Code authored this brief; Cursor executes. No commit/merge without Joshua's go. **Locked surfaces Cursor must NOT touch:** the HARV ADR text (`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`), the campaign template (`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`), the entire blind-campaign `open`/`close`/`status` behavior (must stay byte-identical), any `core/*` anchor-path file, `core/dd_protection.py` / allocations / MC-anchor constants, `ACTIVE_FIRM`, and Pine.

> **Build-ahead-of-candidate (read first).** No mechanism-first campaign has opened since the HARD gate was ratified (2026-07-14) — Q-HARV-0 (AMBIGUOUS) and DISC-CAMP-0 (FALSIFIED) both closed *before* it. This gate is enforcement infrastructure that must exist and be proven correct **before** the next HARV-shaped campaign reaches Stage-3 `register_search open`. Build + test entirely against synthetic attestation files (a `tmp_path` non-empty file, an empty file, a missing path). Do not wait for or reference a real campaign.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any code)

Cursor: read each item and post a read-report in your first response **before** writing a line of code. If any repo fact below contradicts a §2 assumption, return `NEEDS_CONTEXT` with the discrepancy quoted (do not resolve it unilaterally — ADR 2026-07-14 §2 test 2).

- [`lab/discovery/register_search.py`](../../../lab/discovery/register_search.py) — report **in full**, specifically: `open_run(args)` (lines 91–116) and the exact manifest dict it builds (lines 99–111: keys `run_id, status, opened_at, tool, K, alpha, data_window, hypothesis, params, closed_at, results`); the immutability refuse-overwrite guard (lines 93–95, `sys.exit("ABORT: '{run_id}' already registered …")`); the `K < 1` guard (lines 96–97); `_resolve_params(args)` (lines 71–88) and note it reads optional args via **`getattr(args, "params_file", None)`** (line 78) — this getattr-with-default idiom is the pattern the new optional args must copy so the existing `Namespace`-based tests don't `AttributeError`; the `sys.exit("ABORT: …")` convention (lines 82, 87, 94, 97); and `build_parser()`'s `open` subparser args (lines 224–239: `--run-id`, `--tool`, `--search-space-size`, `--alpha`, `--data-window`, `--hypothesis`, `--params`, `--params-file`). Confirm the file's stdlib-only import block (lines 34–43: `argparse, csv, json, math, os, sys, datetime, pathlib` + `research_utils.repo_root`).
- [`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md) — report **§2 point 2** (line 45: mandate a pre-registration reachability simulation of every bundled clause), **§2 point 4** (line 49: the HARD gate wording — "blocks `register_search open` until every bundled clause has a written reachability attestation"), **§5** (line 86: "Quietly downgrading the HARD gate to a recommended step … is a silent §2 edit" — this is the forbidden move this build must NOT commit), and **§6 Downstream** (line 115: the "separate implementation handoff" line this brief discharges).
- [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) — report **Stage-0 row** (line 25: the reachability-attestation HARD-gate row) and the **"Authoring a new campaign" step 2** (lines 83–85: "include a reachability attestation per bundled clause … before `register_search open`"). Report **where** the attestation physically lives per the template: the campaign's pre-registration file at `docs/briefs/pre-registration/<CAMP-ID>-preregistration.md`. This is the artifact whose path the gate checks for existence + non-emptiness.
- [`tests/test_discovery_register_search.py`](../../../tests/test_discovery_register_search.py) — report the ledger/repo-root anchor test shape (it imports `from discovery import register_search`; `PYTHONPATH=lab` is the import root).
- [`tests/test_register_search_params_file.py`](../../../tests/test_register_search_params_file.py) — report the **`ledger` fixture** (lines 22–26: `monkeypatch.setattr(rs, "LEDGER", tmp_path/"discovery_manifests")`), the **`_open_args(**kw)` Namespace builder** (lines 29–37 — note it does **NOT** set `lane` or `reachability_attestation`; your new code must tolerate their absence via `getattr`), and the four `open_run` behavioral tests (valid-JSON round-trip, invalid-JSON abort, both-given abort, legacy-unchanged). **These are the exact patterns §2's new tests extend.**
- `git log -1 --format='%h %ci' -- lab/discovery/register_search.py` — report the commit hash + date as your build anchor.

After Phase 0: post the read-report; proceed to §2 only once §0.5 is resolved.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Parent-recommended defaults are stated; **confirm or challenge each in the Phase-0 response.** Set `Status: NEEDS_CONTEXT` until resolved. Cursor applies each default *unless* its Phase-0 read contradicts it, in which case it bounces `NEEDS_CONTEXT` with the conflict quoted (ADR 2026-07-14 §2 test 2). Do not resolve a spec ambiguity unilaterally.

- **(A) Manifest schema for the blind path — byte-identical, or always-add-keys?** The `open` manifest today has a fixed 11-key schema (lines 99–111). Recording `lane`/`reachability_attestation` unconditionally would change *every* future blind manifest's bytes. **Recommended default:** record the two new keys **only on the `mechanism-first` path**; the `blind` (default) path builds the manifest **byte-identically to today** — no `lane` key, no `reachability_attestation` key. Absence of a `lane` key on a manifest therefore reads as "blind / legacy," which is the correct backward-compatible semantics and directly satisfies the "blind open unchanged" test (c). This honors the header's "byte-for-byte" contract literally. Confirm, or flag if you read the ADR/template as requiring `lane` stamped on blind manifests too.
- **(B) Optional-arg tolerance for the existing `Namespace`-based tests.** `test_register_search_params_file.py::_open_args` constructs an `argparse.Namespace` that does **not** carry `lane`/`reachability_attestation`. `open_run` must read them defensively. **Recommended default:** read both via the existing idiom — `getattr(args, "lane", "blind")` and `getattr(args, "reachability_attestation", None)` — exactly mirroring `_resolve_params`'s `getattr(args, "params_file", None)` (line 78). A missing `lane` attr defaults to `blind`, so every current test that calls `open_run` on a bare Namespace stays green with zero edits. Confirm.
- **(C) Non-empty definition.** **Recommended default:** "non-empty" = the file exists **and** `Path(p).read_text(encoding="utf-8").strip()` is truthy (rejects a whitespace-only file), and it is a regular file (not a directory). A file that exists but is 0 bytes or whitespace-only aborts. This mirrors the intent of a "written attestation" (the ADR wording, line 49). Confirm, or propose bytes-length `> 0` if you prefer a stricter/simpler check.
- **(D) Gate depth — mechanical existence check, not semantic per-clause verification.** The ADR (line 49) says the gate blocks "until every bundled clause has a written reachability attestation." The frozen design has this gate verify only that **one attestation file path exists and is non-empty** — it does **not** parse the file to confirm one note *per clause*. **Recommended default:** implement the mechanical existence + non-emptiness check only; the per-clause *content* completeness stays owned by the authoring/`check_brief` + operator-review path (the human doctrine layer), not this code gate. Record this scope boundary explicitly in the closure report so no one later reads the mechanical gate as a semantic guarantee. Confirm this is the intended interpretation — if you read the design as requiring per-clause parsing, bounce `NEEDS_CONTEXT`.
- **(E) Abort message + exit path.** **Recommended default:** on a mechanism-first `open` with a missing/empty/absent-path attestation, call `sys.exit("ABORT: mechanism-first campaign requires a non-empty reachability attestation (HARV ADR 2026-07-13 §2 HARD gate). Pass --reachability-attestation <path>. <specific reason: not provided | file not found | file empty>.")` — reusing the file's existing `sys.exit("ABORT: …")` convention (non-zero exit, no manifest written), so the failure is a hard refusal, never a warn-and-continue. Confirm.

---

## §1 — Context

The HARV mechanism-first lane ADR was `Accepted` 2026-07-14 with the **HARD gate** explicitly chosen over the softer "recommended step" (ADR §2.4, §3 option A) — precisely because Q-HARV-0 showed that authoring + `check_brief` + the executor *all* missed an unreachable bundled clause when the reachability step was informal. The doctrine binds now; the ADR §6 flagged that "code may lag" and named a "separate implementation handoff." This is that handoff: a mechanical guard in `register_search.py open` so a mechanism-first campaign **cannot** open its pre-registration ledger entry without a reachability attestation on disk.

**What Cursor is asked to produce:**
- An edit to [`lab/discovery/register_search.py`](../../../lab/discovery/register_search.py) `open_run` + `build_parser`'s `open` subparser: a `--lane {blind,mechanism-first}` argument (default `blind`) and a `--reachability-attestation <path>` argument. When `--lane mechanism-first`, `open` **refuses** (`sys.exit`, non-zero, no manifest written) unless the attestation path is provided, exists, and is non-empty; on success it records `{lane, reachability_attestation}` into the manifest (per §0.5(A), mechanism-first path only). The `blind` path is byte-identical to today.
- Extended tests in [`tests/test_register_search_params_file.py`](../../../tests/test_register_search_params_file.py) (or a sibling test module if you prefer isolation — your call, stated in the closure report): (a) mechanism-first `open` **without** an attestation → aborts, no manifest; (b) mechanism-first `open` **with** a valid non-empty attestation → succeeds and the manifest records `lane="mechanism-first"` + the attestation path; (c) blind `open` unchanged — manifest byte-identical to today, no new keys.

**What Cursor is NOT asked to do:** change any `open`/`close`/`status` behavior for blind campaigns (backward compatibility is mandatory — every current test stays green); weaken the gate to a warning; parse the attestation file's *content* for per-clause completeness (§0.5(D) — existence + non-empty only); add any non-stdlib dependency; edit the HARV ADR or the campaign template to match the code (the doctrine is canonical, the code implements it); touch `core/*`, `dd_protection`, `ACTIVE_FIRM`, or Pine.

---

## §2 — Execution plan

TDD throughout; every step's tests run offline, stdlib-only, no network.

### Step 2.1 — Add the two `open` arguments (parser + defaults)
- **Inputs:** `build_parser()` `open` subparser (register_search.py lines 224–239); §0.5(A)/(B) resolutions.
- **Action:** add `o.add_argument("--lane", choices=["blind", "mechanism-first"], default="blind", help=…)` and `o.add_argument("--reachability-attestation", default=None, help=…)` to the `open` subparser only (`close`/`status` untouched). Do not yet wire the gate logic.
- **Expected output:** parser edit + a parser test: `open --tool catch22 --search-space-size 10 --data-window … --hypothesis h` parses with `lane == "blind"`, `reachability_attestation is None` (defaults preserved); an explicit `--lane mechanism-first --reachability-attestation p.json` parses through.
- **Per-step gate:** `close` and `status` subparsers are byte-unchanged; the existing `test_cli_parser_accepts_params_file_flag` still passes.

### Step 2.2 — Gate logic in `open_run`
- **Inputs:** `open_run` (lines 91–116); §0.5(B)(C)(D)(E) resolutions.
- **Action:** at the **top of `open_run`, after the existing run-id/immutability/K guards** (so a bad run-id or K<1 still aborts first with its current message), read `lane = getattr(args, "lane", "blind")` and `att = getattr(args, "reachability_attestation", None)`. If `lane == "mechanism-first"`: `sys.exit("ABORT: …")` (per §0.5(E)) when `att` is None, the path does not exist, is not a regular file, or is empty/whitespace-only (per §0.5(C)) — **before** `_save` is ever called, so no manifest is written on refusal. On success, add `"lane": lane` and `"reachability_attestation": att` to the manifest dict. When `lane == "blind"`: build the manifest **exactly as today** — do not add either key (§0.5(A)).
- **Expected output:** gate logic + the three §-mandated tests (a/b/c below in Step 2.3).
- **Per-step gate:** grep confirms the refusal uses `sys.exit` (non-zero, hard), never `print(...)`-and-continue; no manifest file exists on the abort path.

### Step 2.3 — Tests (synthetic fixtures, stdlib-only)
- **Inputs:** the `ledger` fixture + `_open_args` Namespace builder pattern from `test_register_search_params_file.py` (lines 22–37).
- **Action:** add tests mirroring the existing style (extend `_open_args` to accept `lane`/`reachability_attestation`, or pass them via `**kw`; keep defaults so the *existing* four tests still construct valid args):
  - **(a) mechanism-first WITHOUT attestation aborts:** `with pytest.raises(SystemExit): rs.open_run(_open_args(lane="mechanism-first", reachability_attestation=None))`; assert `not (ledger / "test_run.json").exists()`. Add a variant for a **missing path** (`reachability_attestation=str(tmp_path/"nope.md")`) and an **empty file** (`pf.write_text("")` and a whitespace-only `"   \n"`) — all three abort, no manifest.
  - **(b) mechanism-first WITH valid non-empty attestation succeeds + records it:** write a non-empty attestation fixture (`pf.write_text("clause C1 reachable under plausible-true world: …")`), `rs.open_run(_open_args(lane="mechanism-first", reachability_attestation=str(pf)))`; load the manifest and assert `manifest["lane"] == "mechanism-first"` and `manifest["reachability_attestation"] == str(pf)`.
  - **(c) blind open unchanged (byte-identical schema):** `rs.open_run(_open_args())` (default lane); assert the manifest has **no** `lane` key and **no** `reachability_attestation` key, and its key set equals today's 11-key schema (`run_id, status, opened_at, tool, K, alpha, data_window, hypothesis, params, closed_at, results`).
- **Expected output:** the three tests (with the sub-variants) all green; **every pre-existing test in the file still green** (the load-bearing backward-compat assertion).
- **Per-step gate:** run `PYTHONPATH=lab python -m pytest tests/test_register_search_params_file.py tests/test_discovery_register_search.py -q` — all pass, zero pre-existing tests edited in a way that changes their assertions.

### Step 2.4 — Closure report
Post the §6-format closure report. Include the §0.5(D) scope boundary statement explicitly (mechanical existence check, not semantic per-clause verification) and confirm no non-stdlib import was added.

---

## §4 — Falsifiable hypothesis

**N/A — build task, no hypothesis under test.** This handoff implements the HARV ADR 2026-07-13 §2.4 HARD gate mechanically. The parent gate it feeds is doctrinal, not empirical: the ADR §4 falsifier fires only if a *future* mechanism-first campaign freezes with a structurally-unreachable bundled clause **and** its pre-registration omitted the reachability simulation. This code makes the "omitted attestation" half of that failure mode mechanically impossible at `register_search open` time — it does not adjudicate clause *reachability content* (that is the human/authoring layer, §0.5(D)).

---

## §5 — Forbidden moves

- **Downgrading the gate to a warning / recommended step.** The ADR ratified HARD and §5 (line 86) explicitly forbids "quietly downgrading the HARD gate to a recommended step" as a silent §2 edit. The refusal MUST be `sys.exit` (non-zero), never `print(...)`-and-continue. This is the single most important constraint in this build.
- **Changing any blind-campaign behavior.** `blind` (default) `open` — and all of `close`/`status` — must be byte-identical to today. Backward compatibility is mandatory; every current test stays green with its assertions unedited (§0.5(A)/(B)).
- **Adding a non-stdlib dependency.** `register_search.py` is deliberately stdlib-only (imports at lines 34–43). No `yaml`, no third-party path/validation lib — use `pathlib` + `json` only.
- **Editing the HARV ADR or the campaign template to match the code.** The doctrine is canonical; the code implements it. If you find a genuine contradiction between the ADR wording and this spec, that is a `NEEDS_CONTEXT` bounce, not a doc edit.
- **Semantic per-clause parsing of the attestation.** Out of scope (§0.5(D)) — existence + non-emptiness only. Building a per-clause verifier is scope creep into a larger, separate piece of work.
- **Re-deriving §0 facts.** If the manifest schema, the `getattr` idiom, or the abort-message convention you read on disk differs from what §0/§2 assert, do NOT proceed on the inconsistent version — return `NEEDS_CONTEXT` with the discrepancy quoted.
- **The "while I was in there" refactor** of `open_run`, `_resolve_params`, `_bh`, `close_run`, or `build_parser` beyond the two new args + the gate block. Log any observation under `DONE_WITH_CONCERNS`.

---

## §6 — Gate + status return taxonomy

Report EXACTLY one of these four statuses.

| Status | Meaning | Parent action |
|---|---|---|
| `DONE` | All §2 steps passed; gate refuses hard on mechanism-first-without-attestation; blind path byte-identical; every pre-existing test green; no scope creep. | Accept, review, merge. |
| `DONE_WITH_CONCERNS` | Built + green, but Cursor flags a correctness/scope/methodology doubt the parent should resolve before accepting. | Parent reviews concerns; accept or re-dispatch. |
| `NEEDS_CONTEXT` | Cannot proceed without missing input (a §0.5 default contradicted by Phase-0 read, a file not on disk, an underspecified param). | Parent supplies context; Cursor re-dispatches same plan. |
| `BLOCKED` | Structural obstruction; sub-case required. | Parent escalates/decomposes/re-spawns. |

**`BLOCKED` sub-cases (mandatory):** `context-problem` (re-dispatch with more context) · `capability-problem` (stronger model / human) · `scope-problem` (decompose) · `plan-itself-wrong` (the §2 plan is structurally broken — escalate to parent).

**Closure report format:**
```
Status: <DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED — <sub-case>>
Per-step gates: 2.1 [pass/concern/skip], 2.2 [...], 2.3 [...]
Diffs (files touched): <list — expect only lab/discovery/register_search.py + the test module>
§0.5 resolutions applied: A=<...>, B=<...>, C=<...>, D=<...>, E=<...>
Gate refusal is hard (sys.exit, non-zero): <yes/no — load-bearing>
Blind manifest byte-identical (no new keys): <yes/no — load-bearing>
Pre-existing tests still green: <count / result>
Stdlib-only (no new deps): <yes/no>
§0.5(D) scope boundary (existence check, not per-clause semantics): <restated>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (after Cursor returns)

**Pass 1 — Spec-compliance.** Diff list contains ONLY `lab/discovery/register_search.py` + the test module — no `core/`, no ADR, no template, no Pine. Both new args present with correct defaults (`--lane` default `blind`, `--reachability-attestation` default `None`). The gate block sits after the existing run-id/K guards. No `close`/`status` change.

**Pass 2 — Quality.** The refusal genuinely uses `sys.exit` (temporarily relax it to a `print` in review and confirm test (a) would then wrongly pass — the "does this test test anything" check). The blind manifest is genuinely byte-identical (key set unchanged, verified in test (c)). The `getattr(args, "lane", "blind")` idiom means the four pre-existing `open_run` tests pass **without their assertions edited** — confirm the diff didn't quietly weaken them. Non-empty check rejects whitespace-only (§0.5(C)).

**Pass 3 — Consolidated read** (multi-step): the mechanism-first path and the blind path share one `open_run` — confirm a mechanism-first refusal writes NO manifest AND a subsequent blind open of the same run-id still behaves as today (the abort must not leave partial state). Confirm the two new keys appear only on the mechanism-first success path, nowhere else.

Only after all three passes does the parent recommend Joshua accept/merge.

---

## §10 — Audit hooks (runnable)

```bash
# The gate refuses hard — sys.exit, not a warning (expect a sys.exit near the lane check)
grep -n "reachability\|--lane\|mechanism-first" lab/discovery/register_search.py

# No non-stdlib import crept in (expect: only stdlib + research_utils.repo_root)
sed -n '34,43p' lab/discovery/register_search.py

# Blind path byte-identical: the manifest schema keys are unchanged for blind
grep -n '"lane"\|"reachability_attestation"' lab/discovery/register_search.py
# Expect: only inside the mechanism-first branch, never in the blind default build

# Tests green (stdlib-only, offline)
PYTHONPATH=lab python -m pytest tests/test_register_search_params_file.py tests/test_discovery_register_search.py -q

# Neither the ADR nor the template was edited (expect: empty)
git diff --name-only origin/main -- docs/adr/2026-07-13-harv-discovery-lane-ratification.md docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md

# No core/ / dd_protection / Pine touch (expect: empty)
git diff --name-only origin/main -- core/ '**/*.pine'
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py \
  docs/briefs/rnd-pipeline/2026-07-14-cursor-handoff-register-search-reachability-gate.md --type cc_handoff
# Expected: all checks PASS

git log -1 --format='%h %ci' -- lab/discovery/register_search.py   # build anchor
grep -E "^Status: (DONE|DONE_WITH_CONCERNS|NEEDS_CONTEXT|BLOCKED)" <cursor-return>
```

If Cursor returns `NEEDS_CONTEXT` or `BLOCKED`, this handoff is not complete; re-dispatch per §6.

---

## Related

- Doctrine (canonical): [`docs/adr/2026-07-13-harv-discovery-lane-ratification.md`](../../adr/2026-07-13-harv-discovery-lane-ratification.md) §2.4 HARD gate, §6 Downstream
- Attestation format/location: [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) Stage-0 row + "Authoring a new campaign" step 2
- Surface-allocation governance: [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md)
- Sibling Cursor handoff (same discipline): [`docs/ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md`](../../ltm/briefs/rnd-pipeline/2026-07-13-cursor-handoff-prop-survivor-scoring-harness.md)
