# Cursor Handoff — Candidate reproducibility index (Stage 2 of the CME-breadth-revival design)

**Date:** 2026-08-19
**Parent session:** Claude Code
**Spawn target:** Cursor (frozen-spec implementation — `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, §0.5 Cursor variant; dispatched directly per `docs/adr/2026-08-14-cc-cursor-autonomous-loop.md` §2.1, no chip approval required)
**Repo:** `first-passage`
**Brief type:** CC handoff (multi-step)
**Parent question:** N/A — executes Stage 2 of `docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md` (design doc, `Proposed`, not itself an ADR)
**Authority:** Joshua (CEO), "dispatch implementation to Cursor". No commit/merge without operator go (Stage 1 of the same design — `core/mc/modes.py` baseline-panel wiring — is explicitly OUT of scope for this packet; it is held back pending an unresolved MNQ-export-freshness call, see design spec §7 item 1).

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

Report full contents (or the specific excerpt named) in your first response before writing any code.

- `docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md` §3.2, §5, §6, §7 — report these four sections in full. This packet implements §3.2/§5/§6 exactly; §7's open items are why Stage 1 is excluded from this packet.
- `lab/discovery/register_search.py` — report full contents. You will add one optional field to `close_run()`'s candidate handling; every existing `_require_*` function in this file is the house style to match (all-or-nothing optional groups, `sys.exit("ABORT: ...")` on refusal, docstrings citing the governing artifact).
- `lab/discovery/frozen_rules.py` — report full contents. `load_frozen_rules(path) -> list[FrozenRule]` is the existing, tested loader (raises `FrozenRuleLoadError` on `shape_hash` mismatch) — reuse it verbatim, do not reimplement.
- `lab/discovery/motif_rules.py` — report `FrozenRule`, `RuleEval`, and `evaluate_rule` in full. `evaluate_rule(rule, series, *, cost_frac_per_rt=0.0) -> RuleEval` is a pure, deterministic function; `RuleEval.bar_returns` is a plain `np.ndarray`, same length as the input `series`, with no date index today — closing that gap is this packet's central job.
- `tests/test_stage4_7_drivers.py` — report `test_load_frozen_rules_roundtrip` and `test_load_frozen_rules_tamper_fails` in full (the existing `FrozenRule` JSON round-trip pattern — your provenance-file format must stay compatible with what these tests already exercise, do not invent a second schema).
- `lab/research_utils/breadth.py` — report `compute_breadth`'s signature and its `candidate: pd.Series | None` parameter docstring only (not the full file — this packet does not touch `breadth.py`; report it only to confirm the exact shape your output must satisfy: a `pandas.Series` with a datetime index, `.name` set to the candidate id).
- `git log -1 --format='%h %ci' -- lab/discovery/register_search.py lab/discovery/frozen_rules.py lab/discovery/motif_rules.py` — report the three anchors.

After Phase 0: post the read-report. Wait for confirmation of any §0.5 ambiguity before proceeding to §2 (Cursor variant: apply the stated recommended default and proceed, unless your Phase-0 read contradicts it — see §0.5 below).

---

## §0.75 — Local-only dependency check (required, Spawn target is Cursor)

- **Gitignored vendor data:** No §0 read or §2 step in this packet touches `core/data/tv_exports/**`, `core/data/bar_data/**`, or `core/data/external/**`. The function this packet builds (`regenerate_return_series`) is deliberately scoped to accept an **injectable series-loader callable** rather than reading real CME CSVs itself (see §2 Step 2.2 and §0.5 item 2) — this is precisely so the build and its tests need zero vendor bytes and are safe to run in a cloud checkout. **NOT APPLICABLE — confirmed by design, not merely unconfirmed.**
- **Secrets/API keys:** None needed. **N/A.**

If your Phase-0 read of this packet's own scope disagrees (e.g. you believe a real CME loader must be wired in to satisfy the acceptance tests), STOP and return `NEEDS_CONTEXT` quoting the conflict — do not wire one in unilaterally. Wiring a real production loader is explicitly Stage 1 territory, held back in the parent design (see §5 forbidden moves below).

---

## §0.5 — Clarifying questions (Cursor variant — recommended defaults, apply unless Phase-0 contradicts)

1. **Exact wire format for the rule-provenance pointer on `close_run()`.**
   **Recommended default:** a new, optional `--rule-provenance-file <path>` CLI flag on the `close` subcommand, taking a JSON file mapping `candidate_id -> path` (a dict, not the `load_frozen_rules`-shaped list — one candidate id may share a provenance file with siblings from the same campaign, so the manifest needs to record which id maps to which file, not assume 1:1). Mirrors the existing `--params-file`/`--admission-file` pattern (bypasses shell-quoting, validated as JSON before use). All-or-nothing per the file's own presence: if `--rule-provenance-file` is omitted, `close_run()` behaves exactly as it does today (byte-identical manifest for every existing caller/test) — the manifest's `candidates` list gains a `rule_provenance_path` key on each entry **only when the flag is supplied**, and only for candidate ids present in the mapping (an id missing from the mapping gets no key added for that candidate, not a null/empty string).
2. **How `regenerate_return_series` obtains the underlying market series to re-run `evaluate_rule` against.**
   **Recommended default:** accept a required keyword-only parameter `series_loader: Callable[[str, str], np.ndarray]` — signature `(instrument_or_data_window_tag, data_window) -> np.ndarray`, no default value. If called without one, raise `TypeError` from Python's own missing-required-kwarg behavior — do not supply a stub default that silently does something wrong. Document in the docstring, verbatim: *"No production CME-series loader is wired in by this function — supplying one that reads real market data is Stage 1 / a separate follow-up, deliberately out of scope here so this module has zero vendor-data dependency."* Tests supply a synthetic loader (e.g. one that returns `synthetic_bars.generate_synthetic_bars(...)`-derived arrays, or a simple fixed `np.ndarray`).
3. **Where the new module lives and what it's named.**
   **Recommended default:** `lab/discovery/return_series_index.py`, matching this packet's own file-footprint list in §2. If you have a strong naming objection, note it in `DONE_WITH_CONCERNS` rather than silently renaming — the design spec and this brief both cite the name, and a silent rename breaks that cross-reference.

---

## §1 — Context

This executes Stage 2 only of a two-stage design (`docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md`) reviving a dormant portfolio-risk-breadth tool (`lab/research_utils/breadth.py`) on canonical CME data. Stage 1 (wiring `core/mc/modes.py`'s baseline-panel registry) is held back — it depends on an unresolved MNQ-export-freshness call that is an operator decision, not something this packet should make. Stage 2 is independent of that decision: it builds a reproducibility index so a candidate's daily return series can be regenerated on demand from a frozen-rule pointer, rather than stored as a growing raw-data corpus (the design spec's §3.2 explicitly rejects raw storage — read it before writing any code).

**What CC is being asked to produce:**
- An optional `rule_provenance_path` pointer added to `register_search.py`'s `close_run()` candidate records (§2 Step 2.1).
- A new module, `lab/discovery/return_series_index.py`, housing `regenerate_return_series(run_id, candidate_id, *, ledger_dir=None, series_loader) -> pd.Series` (§2 Step 2.2).
- Tests for both, paired positive/negative, using only synthetic fixtures — no vendor CSVs (§2 Step 2.3).

**What CC is NOT being asked to do:**
- Touch `core/mc/modes.py`, `lab/research_utils/breadth.py`, or any Stage-1 concern.
- Wire a real, production CME-data loader — the `series_loader` parameter stays abstract/injectable in this packet.
- Change any existing `_require_*` gate's behavior, refusal condition, or manifest shape for callers that don't supply the new flag.
- Pick a canonical CME export filename for anything — not this packet's concern.

---

## §2 — Execution plan

### Step 2.1 — Optional rule-provenance pointer on `close_run()`

- **Inputs:** `lab/discovery/register_search.py` (read in full at §0).
- **Action:** Add `--rule-provenance-file` per §0.5 item 1's recommended default (or the confirmed alternative if §0.5 surfaced a conflict). Wire it into `close_run()` so each candidate entry in `manifest["results"]["candidates"]` gains `rule_provenance_path` when (a) the flag is supplied and (b) that candidate's id is a key in the JSON mapping. Validate the JSON file parses and is a flat `dict[str, str]` before use; `sys.exit("ABORT: ...")` on malformed input, same style as `_resolve_params`'s existing `--params-file` validation.
- **Expected output:** a diff to `register_search.py` only; no behavior change for any existing caller that omits the new flag (verify: existing test suite — `tests/test_register_search_admission.py`, `tests/test_discovery_register_search.py`, `tests/test_register_search_operator_stopped.py`, `tests/test_register_search_params_file.py`, `tests/test_register_search_prereg.py`, `tests/test_register_search_cost_law.py` — all still pass unmodified).
- **Per-step gate:** DONE requires the six existing test files above to pass unmodified, plus new paired positive (`rule_provenance_path` recorded when supplied and the id matches) / negative (flag omitted → no new key anywhere; id not in mapping → no key for that one candidate; malformed JSON → `ABORT`, no manifest write) tests in a new file, `tests/test_register_search_rule_provenance.py`.

### Step 2.2 — `regenerate_return_series`

- **Inputs:** `lab/discovery/frozen_rules.py`'s `load_frozen_rules`, `lab/discovery/motif_rules.py`'s `evaluate_rule`, the manifest shape from Step 2.1.
- **Action:** Implement `regenerate_return_series(run_id, candidate_id, *, ledger_dir=None, series_loader)` in the new module (§0.5 item 3's default path). Load the manifest for `run_id` (reuse `register_search`'s own manifest-loading convention — do not duplicate its JSON-read logic if it's cleanly importable; if importing creates a layering problem, say so in `DONE_WITH_CONCERNS` rather than working around it silently). Resolve `rule_provenance_path` for `candidate_id`; if absent, raise a clear, actionable error (not a bare `KeyError`) naming that this candidate has no recorded provenance. Call `load_frozen_rules(path)`, find the entry whose `candidate_id` matches (the file may contain multiple rules from the same campaign — filter, don't assume index 0; if no match, raise naming the mismatch). Call `series_loader(...)` per §0.5 item 2's contract, then `evaluate_rule(rule, series, cost_frac_per_rt=...)` — read the manifest for whatever cost input close_run originally used, if recorded; if not recorded, use `cost_frac_per_rt=0.0` and note this as a `DONE_WITH_CONCERNS` limitation, do not guess a nonzero value. Attach the date index: `series_loader`'s returned array's own index (if it returns a `pandas.Series`) or a synthetic `pd.RangeIndex`-to-date mapping the tests control explicitly — resolve the exact mechanics against what `series_loader` actually returns in your Phase-0 read of `synthetic_bars.py`/the existing `evaluate_rule` callers, and state your choice plainly in the closure report rather than leaving it implicit.
- **Expected output:** `lab/discovery/return_series_index.py`, containing `regenerate_return_series` and any small private helpers it needs.
- **Per-step gate:** the returned `pandas.Series` has a datetime-like index, `.name == candidate_id`, and its values exactly reproduce (or match within float tolerance) `evaluate_rule`'s own `bar_returns` output for the same rule + series — i.e. calling `evaluate_rule` directly and calling `regenerate_return_series` (with a synthetic loader returning the same series) must agree numerically.

### Step 2.3 — Tests

- **Inputs:** the two new modules above; `lab/discovery/synthetic_bars.py` and `lab/discovery/motif_rules.py::freeze_rule_from_spec` for fixtures (same pattern already used in `tests/test_stage4_7_drivers.py` and this session's own `tests/test_scorer_near_duplicates.py` — read the latter for the exact fixture-construction idiom before writing new fixtures from scratch).
- **Action:** Paired positive/negative tests per this repo's house style (no vacuous asserts — every negative test asserts on the actual raised exception's message content, not just `pytest.raises(Exception)`).
- **Expected output:** `tests/test_register_search_rule_provenance.py`, `tests/test_return_series_index.py`.
- **Per-step gate:** `PYTHONPATH=lab python -m pytest tests/test_register_search_rule_provenance.py tests/test_return_series_index.py tests/test_register_search_admission.py tests/test_discovery_register_search.py tests/test_register_search_operator_stopped.py tests/test_register_search_params_file.py tests/test_register_search_prereg.py tests/test_register_search_cost_law.py -q` exits 0, plus `python scripts/check_boundaries.py` exits 0.

### Step 2.4 — Closure

No formal closure artifact required (this is not a Pre-Q). Return the §6 status report below, and — separately, do not merge — leave the design spec and this brief untouched; the parent session updates the design spec's status if/when Stage 2 is accepted.

---

## §4 — Falsifiable hypothesis

Not a Pre-Q investigation, but this packet's own load-bearing premise is falsifiable and must be
tested as such, not merely asserted:

**H:** `regenerate_return_series`, given a `FrozenRule` and the same series `evaluate_rule` originally
scored, deterministically reproduces that original `bar_returns` output — i.e. the reproducibility
index is genuinely reproducible, not an approximation.

**Falsified if:** Step 2.2's per-step gate test (calling `evaluate_rule` directly vs. calling
`regenerate_return_series` with a synthetic loader returning the identical series) produces numerically
different results beyond float tolerance. If that happens, this is not a `DONE_WITH_CONCERNS` — it
means the central design premise (reproducibility over storage, per the design spec §3.2) does not
hold for this implementation, and the packet returns `NEEDS_CONTEXT` naming the discrepancy rather
than shipping a "reproducibility index" that does not actually reproduce.

**Accept if:** the two outputs match within float tolerance across the acceptance test's fixtures.

---

## §5 — Forbidden moves

- **Wiring a real production CME-data loader into `series_loader`'s default**, "since it would make the function actually useful." Explicitly the Stage-1-adjacent move the design spec defers — see §0.75. If tempted, log the observation in `DONE_WITH_CONCERNS`, do not act on it.
- **Touching `core/mc/modes.py` or `lab/research_utils/breadth.py`** — zero diff lines in either file, regardless of how small a change would look. Both are out of this packet's file footprint by design.
- **Reimplementing `load_frozen_rules` or its hash-verification logic** instead of importing and reusing it verbatim from `frozen_rules.py`.
- **Changing any existing `_require_*` function's refusal condition or manifest field shape** in `register_search.py` — this packet is additive-only, same posture as every optional field already in that file (`--cost-law-*`, `--admission-file`, `--prereg`).
- **Guessing the `cost_frac_per_rt` value** for a manifest that doesn't record it, rather than defaulting to `0.0` and flagging the limitation — see §2 Step 2.2.
- **Re-deriving §0 facts** — if `load_frozen_rules`'s actual signature, `evaluate_rule`'s actual return shape, or `close_run`'s actual candidate-list structure differ from what this brief describes, trust what you read on disk and return `NEEDS_CONTEXT` naming the discrepancy, don't silently proceed on the brief's text.

---

## §6 — Gate + status return taxonomy

Report back with exactly one of `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>`, per the standard four-state taxonomy (`docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §2 handoff contract).

```
Status: <...>
Per-step gates: 2.1 [...], 2.2 [...], 2.3 [...]
Diffs (files touched): <list — must match exactly: lab/discovery/register_search.py, lab/discovery/return_series_index.py (new), tests/test_register_search_rule_provenance.py (new), tests/test_return_series_index.py (new)>
Concerns surfaced (if any): <list>
Next action recommended: <one sentence>
```

Branch: `cursor/candidate-return-series-index`. PR with tests green. **No commit/merge without operator go** — this packet's diff does not touch the auto-merge-forbidden surface list (`docs/adr/2026-08-14-cc-cursor-autonomous-loop.md` §2), but the parent session reviews before merge regardless, per that same ADR's structural point that `docs/adr/**`/`docs/spec/**` changes (none expected here) would route this to CC, not Cursor, in the first place — this packet touches neither.

---

## §10 — Audit hooks (runnable)

```bash
PYTHONPATH=lab python -m pytest tests/test_register_search_rule_provenance.py tests/test_return_series_index.py -q
python scripts/check_boundaries.py
git diff origin/main --name-only
# Expected: exactly lab/discovery/register_search.py, lab/discovery/return_series_index.py,
# tests/test_register_search_rule_provenance.py, tests/test_return_series_index.py
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python .claude/skills/brief-authoring/scripts/check_brief.py docs/briefs/handoffs/2026-08-19-cursor-handoff-candidate-return-series-index.md --type cc_handoff
```
