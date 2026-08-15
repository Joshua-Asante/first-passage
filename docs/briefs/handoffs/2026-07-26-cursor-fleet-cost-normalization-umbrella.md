# CC/Cursor fleet handoff — cost-model normalization + attestation completeness (umbrella)

**Fleet slug:** `cost-normalization` · **Date:** 2026-07-26 · **Type:** handoff (umbrella, 2 packets)
**Orchestrator:** Claude Code (this session) — owns decomposition, spec freeze, review, integration.
**Workers:** 2 Cursor packets (A, B), dispatched via `scripts/dispatch_cursor.ps1`.
**Base ref:** `origin/main` @ `1158820` (PR #511 merged 2026-07-26T15:42:39Z).
**Governing:** [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md) (every clause binds per packet) ·
[`docs/adr/2026-07-25-instrument-profile-index.md`](../../adr/2026-07-25-instrument-profile-index.md) (governs the surface B touches).

---

## §0 — Rule 0 reads (production source, verified this session)

Read directly at `origin/main` @ `1158820`. Path first, then the facts, per the
`check_brief` fence-parity convention: `lab/discovery/cost_mnq.py`.

```
lab/discovery/cost_mnq.py       SLIPPAGE_TICKS_PER_SIDE = 1.0   (crossing, 2 ticks RT)
                                DEFAULT_FIRM_KEY = "Bulenox_100K" (cost_per_side_usd 0.61)
lab/discovery/cost_es.py:14-28  PASSIVE_SLIP_TICKS_RT = 0.5     (HALF a tick for the WHOLE
                                round trip, NOT per side) + docstring: "do NOT substitute
                                D5's cost_mnq.py crossing model"
                                ES_PARENT_COMMISSION_PER_SIDE = 3.00  (hardcoded, no FIRM_RULES)
lab/discovery/cost_mgc.py:10-18 COMMISSION_PER_SIDE_USD = 0.62  (hardcoded; below the repo's
                                own cheapest MGC row, 0.76)
lab/discovery/register_search.py:91-115   _require_reachability_attestation -- docstring:
                                "Mechanical check only (exists + regular file + strip()-truthy)
                                -- does not parse per-clause content."
lab/discovery/register_search.py:117-186  _require_profile_consult + PROFILE_CONSULT_HEADER.
                                Consumes WRITTEN output, never imports scripts/ (check_boundaries
                                enforces lab/ !-> scripts/). Cell match is ANCHORED on the header,
                                not substring -- substring false-accepted MNQ's consult for a
                                declared NQ ("NQ" occurs inside "MNQ").
lab/discovery/register_search.py:213-222  manifest schema. Comment: "Blind / legacy: keep the
                                11-key schema byte-identical."
core/firm_rules.py:65-67        the 0.61 per-side figure is an INFERENCE: "the PDF header says
                                only 'ALL IN RATES' -- per-side is an arithmetically forced
                                inference ... not primary-verbatim", Sept-2024 vintage, STALE >90d.
docs/adr/2026-07-25-instrument-profile-index.md:42-75  PROFILE schema already carries
                                cost_hurdle: {value, units, basis, source}, units commented
                                "as-stated; never normalized across units". Plus the
                                value-carrying rule and the "generated, never authored" invariant.
.claude/skills/databento-data/reference/proxy-discipline.md:36-42  contract-spec table
                                (MYM tick_size = 1.00 index pt, tick_value $0.50 -- the outlier).
```

Corpus evidence motivating both packets (this session, 14-agent extraction over the closed
corpus; frozen numbers, no re-runs): `lab/analysis/orb/orb_mnq_2026-07/run_stage2.py:36` hardcodes
`rt_cost_pt=1.11` with no `firm_rules` import — the corpus's only cost-law PASS was scored at
Bulenox by hand-transcription, and correcting to the live firm moves 5.31x -> 4.180x against a
4.0x bar. Across the corpus only `d5_recost_2026-07` live-imports `FIRM_RULES`; every other
study hardcodes its own commission (3.00 / 0.91 / 0.62 / 0.61 / bare 6.0-10.0 literals).

---

## §0.5 — Clarifying questions and pre-answered defaults

**Workers must NOT resolve ambiguity.** Anything not answered here halts to
`CURSOR_RETURN.md` as `NEEDS_CONTEXT`. Pre-answered:

1. **New file or edit existing?** Packet A adds a NEW module. It must NOT modify
   `cost_mnq.py` / `cost_es.py` / `cost_mgc.py` — those are frozen per-campaign inputs whose
   figures appear in closed verdicts; changing them would silently move published numbers.
2. **May A normalize R and bp into one number?** NO. No conversion exists (R normalizes by
   opening-range points, bp by notional; the R-denominated studies report no price by
   construction). A carries both laws side by side and refuses cross-unit comparison.
3. **May B import a cost model to recompute a hurdle?** NO — out of scope for B. B enforces
   declaration COMPLETENESS only. Arithmetic recompute is a later packet, deliberately split so
   A and B stay independent.
4. **Commission default?** None. A takes `firm_key` as a required argument with no default.
   A missing firm_key is an error, not a fallback — the Bulenox default is the defect being fixed.
5. **Python / venv?** `C:/Users/joshu/multi_firm_operations/.venv-research/Scripts/python.exe`
   (absolute — fresh worktrees lack `.venv-research`).
6. **Commit / push / PR?** Commit to your own branch only. Do NOT push, do NOT open a PR, do
   NOT merge. The orchestrator reviews the branch and integrates.

---

## §1 — Context

The 2026-07-26 graveyard extraction established that the discovery corpus does not share a cost
model: each campaign hardcodes its own constants, two ratio conventions differ by exactly 4x
(`edge/mean_cost_R` bar 4.0 vs `edge/hurdle_4x` bar 1.0), two slippage conventions differ by 4x
(per-side vs total-round-trip), and five studies publish the reciprocal ratio. A single unverified
inference (`0.61` per-side vs round-turn) sits under a large fraction of the corpus's cost verdicts.

Separately, HARV Requirement 5 has no mechanical enforcement: `_require_reachability_attestation`
checks only that a file exists and is non-empty. That is the exact regime under which D5 and
H-OD-1 passed signed freezes — D5's Stage-2 clause was never simulated, and H-OD-1's carried a
x10 commission mis-scaling. Lesson M-20 requires every gate be simulated "in the gate's own
units, at the adjudication panel's price basis"; nothing enforces it.

These are the two forward-value items left after the cost-geometry re-score was answered
analytically and cancelled (no candidate is revived by any achievable hurdle reduction; only
MYM-3FPS-1 has a ceiling above 1.0 and it fails power independently by ~4-8x).

---

## §2 — Claim manifest (dispatch table; orchestrator-owned)

| Packet | Branch | File footprint (DISJOINT) | Status |
|---|---|---|---|
| A — normalized cost model | `cursor/cost-normalization-pA` | `lab/discovery/cost_model.py` (new) · `tests/test_cost_model.py` (new) | DISPATCHED |
| B — attestation completeness gate | `cursor/cost-normalization-pB` | `lab/discovery/register_search.py` · `tests/test_discovery_register_search.py` | DISPATCHED |

**Reserved to the orchestrator — no worker writes these:** `docs/SESSIONS.md`, `STATE.md`,
`lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/adr/**`, `ops/instruments/**`, this brief.

Footprints are disjoint by construction: A creates two new files; B edits one module and its
existing test file. Neither touches the other's paths.

---

## §3 — Packet A: normalized instrument cost model

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git log --oneline -5 origin/main
ls lab/discovery/cost_model.py 2>/dev/null && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
grep -rn "SLIPPAGE_TICKS_PER_SIDE\|PASSIVE_SLIP_TICKS_RT" lab/discovery/
```

**Frozen scope.** Create `lab/discovery/cost_model.py` exposing one parameterized model covering
both cost laws found in the corpus. Required behaviour:

- `bp_hurdle(...)` implementing `hurdle_4x = 4 * 2*(commission_per_side + slip*tick_value) / (price*multiplier)`.
- `r_hurdle(...)` implementing `rt_pt = 2*(commission_per_side + slip*tick_value)/multiplier`, then
  `mean_cost_R = mean(rt_pt / or_range_i)` — MEAN-OF-RATIOS over per-trade ranges, NOT
  `rt_pt / median(range)` (the wrong form understates by ~21% on the ORB-MNQ panel).
- An explicit `slip_convention` parameter with exactly two legal values, `"per_side"` and
  `"total_rt"`, and NO default. `cost_es.py` uses `total_rt`; `cost_mnq.py`/`cost_mgc.py` use
  `per_side`; conflating them is a 4x error.
- An explicit `ratio_convention` field on every returned object recording which denominator was
  used (`edge_over_hurdle_4x`, bar 1.0; or `edge_over_mean_cost_R`, bar 4.0).
- `firm_key` REQUIRED, resolved through `core.firm_rules.FIRM_RULES`. No default. Raise on a
  missing or unknown key. Where a firm has no commission row for the instrument (ZN, ZB, ZF, CL,
  NG, full-size 6E all lack one), raise a clear error naming the gap — never substitute an
  index-micro rate (`rates_ev_zf_recon` applied the 0.61 index-micro rate to a full-size CBOT
  product; that is the defect shape to refuse).
- Instrument specs from a single table, sourced to
  `.claude/skills/databento-data/reference/proxy-discipline.md`. MYM's `tick_size` is 1.00 index
  point (not 0.25) — a copy-paste of MNQ's is wrong.
- NO R<->bp conversion function. If asked to compare across units, raise.
- Docstring must state that this module does NOT supersede the frozen per-campaign
  `cost_*.py` files, which remain the citable basis for their closed verdicts.

**Acceptance test (this is packet A's falsifier, see §4).** `tests/test_cost_model.py` must
reproduce, from each campaign's own declared primitives, these frozen published figures:

```
cost_mnq  / D5-RECOST  Bulenox_100K  px 14769.25  slip 1.0 per_side  -> hurdle_4x 3.0062460856 bp
cost_es   / H-OD-1     comm 3.00     px 1942.125  slip 0.5 total_rt  -> hurdle_4x 5.046019180021883 bp
cost_mgc  / DISC-CAMP-0 comm 0.62    px 1355      slip 1.0 per_side  -> hurdle_4x 9.5638 bp (approx, assert 4dp)
MYM-3FPS               comm 0.91     px 34312.0   slip 1.0 per_side  -> hurdle_4x 6.57495919794824 bp
NG-EIA-1               comm 0.61     px 2.868     slip 1.0 per_side  -> hurdle_4x 29.595536959553694 bp
scale-invariance: NG (mult 10000) and MNG (mult 1000) must return the SAME slippage term.
```

Tolerance: 1e-9 relative on the exact figures, 1e-4 on the MGC approximate. Reproduce WITHOUT
special-casing any campaign — a per-campaign branch is a spec violation.

**Forbidden moves (A).** No edits to `cost_mnq.py` / `cost_es.py` / `cost_mgc.py`, `core/**`,
Pine, ADRs, `STATE.md`, `CLAUDE.md`, or any file outside the two in your footprint. No default
`firm_key`. No R<->bp conversion. No re-running any campaign.

---

## §3b — Packet B: attestation completeness gate

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git log --oneline -5 origin/main
sed -n '91,115p' lab/discovery/register_search.py
grep -n "units\|basis\|clause" lab/discovery/register_search.py || echo "NOT YET IMPLEMENTED -- proceed"
```

**Frozen scope.** Upgrade the mechanism-first attestation gate from presence-only to
declaration-completeness, in `lab/discovery/register_search.py`:

- The reachability attestation, when it is JSON (see the compatibility rule below), must declare
  a per-clause list where every bundled gate carries `{value, units, basis, source}` — reusing
  the field names ADR 2026-07-25 §2a already established for `cost_hurdle`, NOT a new schema.
- Abort with a clear `ABORT:` message naming the offending clause when a clause is missing any
  of the four fields, or when `units` is empty. Follow the existing message style at
  `register_search.py:96-113` (prefix `ABORT:`, name the flag, say what to do).
- `units` is recorded verbatim and never normalized (ADR 2026-07-25 §2a: "as-stated; never
  normalized across units").
- Store the parsed clause table on the manifest under a mechanism-first-only key. The blind /
  legacy 11-key schema MUST stay byte-identical (`register_search.py:215` comment).
- **Backward compatibility is REQUIRED.** Existing attestations are prose markdown, not JSON.
  A non-JSON attestation keeps today's behaviour exactly (exists + non-empty) and emits a WARN
  to stderr naming the ADR. Do NOT hard-fail prose attestations — that would retroactively
  invalidate every frozen pre-registration in the repo.
- Anchored matching only. Where you compare a declared token against file content, anchor it —
  the substring form false-accepted MNQ's consult for a declared NQ
  (`register_search.py:137-144`). Do not reintroduce substring matching.

**Regression test set (this is packet B's falsifier, see §4).** Extend
`tests/test_discovery_register_search.py`:

- A JSON attestation with a clause missing `units` -> `SystemExit`, message names that clause.
- A JSON attestation with all four fields on every clause -> passes, and the manifest records
  the clause table.
- A prose (non-JSON) attestation -> passes with a WARN, behaviour byte-identical to today.
- A blind-lane open -> manifest has exactly the 11 legacy keys, byte-identical.
- Re-registering an existing `run_id` still aborts (immutability, `register_search.py:190`).

**Forbidden moves (B).** Do NOT import from `scripts/` (`check_boundaries.py` forbids
`lab/` -> `scripts/`; the profile gate consumes written output for exactly this reason). Do NOT
import any `cost_*.py` or compute a hurdle — recompute is out of scope. Do NOT cache or
snapshot a `K_banked` value (ADR 2026-07-25 §5: pointer, never a value). Do NOT hand-edit
`ops/instruments/profiles.json` or `PROFILES.md` (generated, never authored). Do NOT touch
`core/**`, Pine, ADRs, `STATE.md`, or any file outside your two.

---

## §4 — Falsifiable hypotheses (both packets)

**H-A:** a single parameterized cost model reproduces every frozen per-campaign cost figure in
the corpus from that campaign's own declared primitives, to stated tolerance, with no
per-campaign special-casing. **FALSIFIED** if any figure in the §3 acceptance table cannot be
reproduced without branching on the campaign — which would mean the corpus's cost models differ
in substance, not merely in parameters, and normalization is the wrong move.

**H-B:** the Requirement-5 failure mode is detectable mechanically at `register_search open`
without re-running any analysis. **FALSIFIED** if enforcing completeness cannot be done without
either hard-failing existing prose attestations (retroactively invalidating frozen
pre-registrations) or importing an analysis module across the `lab/` -> `scripts/` boundary.
Either outcome means the gate belongs elsewhere; halt `NEEDS_CONTEXT` rather than forcing it.

---

## §5 — Forbidden moves (fleet-wide, in addition to per-packet)

- No writes to any orchestrator-reserved file listed in §2.
- No writes outside your declared file footprint, for any reason.
- No commit to `main`, no push, no PR, no merge.
- No resolving ambiguity: halt to `CURSOR_RETURN.md` as `NEEDS_CONTEXT` instead.
- No touching the other packet's files, even to fix an obvious defect — report it instead.
- No modifying frozen per-campaign `cost_*.py` constants or any published figure.
- No `--no-verify`, no skipping gates, no disabling a failing test to go green.

---

## §6 — Gate criteria and status taxonomy

**Binary verdict per packet.** The packet's §4 hypothesis returns exactly one of:
**RESOLVED** (spec met, gates green — the normal PASS), **FALSIFIED** (the acceptance table
cannot be reproduced without per-campaign special-casing for A, or completeness cannot be
enforced without breaking prose attestations / crossing the layer boundary for B — a real
result, report it, do not force a pass), or **AMBIGUOUS** (the spec's premise could not be
established either way — return `NEEDS_CONTEXT`, never a guess).

RESOLVED requires all of: (a) the diff touches ONLY the declared footprint;
(b) the packet's acceptance/regression tests are present and green; (c) `python -m pytest` shows
no new failures; (d) `python scripts/check_boundaries.py` is clean; (e) no forbidden-move
violation. Otherwise FAIL.

**Return contract.** Write `CURSOR_RETURN.md` at the worktree root with exactly one status:

- `DONE` — spec met, gates green.
- `DONE_WITH_CONCERNS` — spec met, but something the orchestrator must adjudicate. State it.
- `NEEDS_CONTEXT` — the spec is ambiguous or its premise is false. State what you need. Do not guess.
- `BLOCKED` — cannot proceed. State why.

Include: files changed, test command run, its output tail, and any deviation from spec.
One `NEEDS_CONTEXT` bounce gets a re-anchor and re-dispatch; a second means the spec was not
freezable and the packet falls back to CC solo.

---

## §10 — Audit hooks (runnable)

```bash
# Packet A landed and generalizes without special-casing
test -f lab/discovery/cost_model.py && echo "A: module present"
grep -c "def bp_hurdle\|def r_hurdle" lab/discovery/cost_model.py
grep -n "slip_convention\|ratio_convention" lab/discovery/cost_model.py | head
# no default firm_key, and the frozen models untouched
grep -n "firm_key" lab/discovery/cost_model.py | head
git diff --name-only origin/main...HEAD -- lab/discovery/cost_mnq.py lab/discovery/cost_es.py lab/discovery/cost_mgc.py
# ^ MUST be empty

# Packet B landed, legacy schema intact, prose attestations still accepted
grep -n "units" lab/discovery/register_search.py | head
python -m pytest tests/test_discovery_register_search.py -q
python scripts/check_boundaries.py

# Fleet-wide: footprint discipline
git diff --name-only origin/main...HEAD
# ^ MUST be a subset of the packet's declared footprint, nothing else
```
