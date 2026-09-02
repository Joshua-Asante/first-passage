# CC/Cursor fleet handoff — MSL P2 tooling (umbrella)

**Fleet slug:** `msl-tooling` · **Date:** 2026-08-12 · **Type:** handoff (umbrella, 3 packets)
**Orchestrator:** Cursor Track-B session (this fleet) — owns decomposition, spec freeze, review, integration.
**Workers:** 3 Cursor packets (A, B, C). All **LOCAL-only** (see §0.5 q5).
**Base ref:** `origin/main` @ `e0f414b` (PR #769 Board B1–B3 + B8 merged 2026-08-12).
**Governing:** [`docs/adr/2026-07-14-cc-cursor-surface-allocation.md`](../../adr/2026-07-14-cc-cursor-surface-allocation.md) (every clause binds per packet) ·
[`docs/briefs/programs/2026-08-12-msl-program-plan.md`](../programs/2026-08-12-msl-program-plan.md) §3 (worker layer) ·
[`.claude/skills/cursor-fleet/SKILL.md`](../../../.claude/skills/cursor-fleet/SKILL.md) ·
template lineage [`2026-07-31-cursor-fleet-fade-mcl-parity-umbrella.md`](2026-07-31-cursor-fleet-fade-mcl-parity-umbrella.md).

**Nothing in this fleet spends money, opens K, proposes a mechanism, authors an ADR, or
touches the rail.** Packets build `lab/` tooling only. Adjudication (PASS/KILL/route) stays
with the P3.x campaign manager — never in a worker tool.

**Solo-build estimates (frozen at dispatch for the §7 fleet falsifier):**
W-A ≈ **1.5h** · W-B ≈ **2h** · W-C ≈ **45m** (CC-solo equivalents from the program plan / Track-B plan).

---

## §0 — Rule 0 reads (production source, verified this session at `e0f414b`)

Read directly before implementing. Path first, then the facts:

```
lab/research_utils/nsurv_channel.py @ 765390b (2026-08-11)
  score_nsurv(frame, *, half_boundary_date, firm_key=Tradeify_Select_100K, ...)
  Input contract: date, pnl_usd, intraday_low (≤ 0). Intraday-honest clock mandatory.
  Emits NSurvReport with full/H1/H2 PartitionScore + nsurv PASS|FAIL.
  Do NOT reimplement remc / Part-A — import and call.

lab/research_utils/book_score.py @ 7ed348f (2026-08-12)
  score_book / compose_book — composed N-SURV via score_nsurv.
  Same input contract. TOOLING_DISCLAIMER = "computes, does not admit".
  CLI pattern (argparse --leg NAME=PATH --half-boundary) is the style mirror for W-B.

scripts/instrument_profiles.py @ e20e240 (cell printer ~L662–688)
  `cell <SYMBOL> <mechanism>` prints BINDING BAR: {id} -> {source} for every
  bar in inst["bars"] + inst["inherited_bars"]. Any bar ⇒ exit code 1 (blocking).
  W-A shells this and surfaces RAW stdout — never interprets PASS/KILL.

docs/adr/2026-08-10-implied-sr-plausibility-gate.md @ a5171ef
  Gate: implied_annualized_sr = per_trade_sharpe(p, rr) × √(n·252).
  Ceiling SHARPE_CEILING = 1.83 (futures-native ≈0.89 disclosed).
  Fade admitted-region floor measured **2.98** (ADR Decision ¶2).

docs/notes/2026-07-31-fade-stage1-frozen-rulings.md ~L347–356
  Formula corroboration + floor table: min over admitted region = 2.98 = 1.63× ceiling.

core/firm_rules.py @ 0356be2 — Tradeify Select comments (~L226–231, L318)
  cost_per_side_usd index micros $0.91; comment pin **MGC=$1.06** (RT/2 from $2.12).
  dd_lock_offset_usd on Select evals = 1_000_000.0 (unreachable; fixed 2026-08-04).
  W-B consumes firm_rules AS-IS — verify, never re-patch.

lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/score_cell.py
  @ 9856a39 — static_equity_recompute(df) ~L37–65
  Pair Exit↔Entry by Trade #; net = qty*(exit-entry)*point_value − 2*commission*qty.
  Compare to TV Net P&L USD. W-C LIFTS this into a shared util (parameterized
  point_value + commission_per_side); does not edit score_cell.py.

Formula pin (verbatim from pruned design_law.per_trade_sharpe / implied_annualized_sr;
retrieve: git show 283d1de^:lab/analysis/c1/tradeify_fade_stage0_2026-07-30/design_law.py):
  expectancy_r = p * rr - (1.0 - p)
  per_trade_sharpe = expectancy_r / (sqrt(p*(1-p)) * (1+rr))
  implied_annualized_sr = per_trade_sharpe * sqrt(n_trades) * sqrt(252)
  design_law rounded published cells to 2dp.
```

**Phase-0 existence (authoring-time; re-check at dispatch):** none of
`lab/research_utils/msl_preflight.py`, `msl_score.py`, or `tv_static_equity.py` exist on
`origin/main` @ `e0f414b`.

---

## §0.5 — Clarifying questions and pre-answered defaults

**Workers must NOT resolve ambiguity.** Anything not answered here halts to `CURSOR_RETURN.md`
as `NEEDS_CONTEXT`. Pre-answered:

1. **New files only?** **YES.** Create only the files in your §2 footprint. Do not edit
   `nsurv_channel.py`, `book_score.py`, `instrument_profiles.py`, `firm_rules.py`,
   `score_cell.py`, any ADR, Pine, `docs/SESSIONS.md`, `STATE.md`, or the program plan.
2. **May W-A emit PASS/KILL/route verdicts?** **NO.** Evidence tables and raw subprocess
   output only. Adjudication is campaign-manager work (program plan §3).
3. **May W-B invent a new MC / remc path?** **NO.** Adapter only: TV CSV → daily panel →
   existing `score_nsurv` / `book_score`. Reuse-don't-rewrite.
4. **May any packet pull data / spend K / $?** **NO.** `$0 / K=0`. Fixtures are hand-authored
   under `lab/research_utils/fixtures/`. Never `db_fetch pull`, never `register_search open`.
5. **Cloud or local?** **LOCAL, all three.** Dispatch via `scripts/dispatch_cursor.ps1` into
   `.worktrees/<slug>`. No vendor-secret requirement, but keep local for fleet consistency.
6. **Python?** Plain `python` on PATH (pandas/numpy available). Fresh worktrees have no `.venv`.
7. **Commit / push / PR?** Commit on your `cursor/msl-tooling-p{A,B,C}` branch. **Do push and
   open a PR** titled `MSL P2 W-{A|B|C} …` so the orchestrator can review. Do **NOT** merge,
   do **NOT** write SESSIONS/STATE/plan §6.
8. **Implied-SR fade fixture inputs?** **Recommended default:** fixture card carries
   `p=0.654`, `rr=0.66`, `n_trades=3` (yields `round(implied_annualized_sr, 2) == 2.98` under
   the §0 formula). Acceptance asserts **2.98** (±0.01). If Phase-0 read of the ADR/notes
   contradicts, bounce `NEEDS_CONTEXT` with both numbers — do not retune the pin.
9. **BINDING BAR fixture instrument?** **Recommended default:** card `instrument: MES` (or
   any symbol whose PROFILE already carries `bars:` on current `origin/main` — MES has
   `index-intraday-ohlcv-directional-timing-2026-07-21`). Do not depend on in-flight MGC
   Stage-0 bars (sibling Track A). Shell:
   `python scripts/instrument_profiles.py cell MES <any-mechanism>` and surface raw stdout.
10. **W-C point_value / commission defaults?** **Recommended default:** API takes
    `point_value_usd` and `commission_per_side` as required parameters (no silent MNQ hardcode
    in the shared util). Fixture may use MNQ `2.00` / `0.91` to match score_cell provenance.
11. **Test location?** `tests/test_msl_preflight.py`, `tests/test_msl_score.py`,
    `tests/test_tv_static_equity.py` at repo `tests/` root (sibling of `tests/test_nsurv_channel.py`).
12. **Return artifact?** `CURSOR_RETURN.md` at worktree root with exactly one of
    `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`.

---

## §0.75 — Local-only dependency check

- **Gitignored vendor data:** none required for acceptance. W-B/W-C fixtures are committed
  under `lab/research_utils/fixtures/`. Optional live TV exports are out of scope.
  - Confirmed: N/A — route LOCAL anyway for fleet consistency.
- **Secrets/API keys:** none.
  - Confirmed: N/A.

---

## §1 — Context

MSL Board B1–B3 + B8 landed (PR #769). Program plan §3 unlocks three `lab/` tooling packets
so Stage-1 campaigns can preflight cards, score TV exports through the frozen N-SURV channel,
and compare compounded TV equity on a static-equity basis. This umbrella freezes disjoint
footprints and dispatches them in parallel under the cursor-fleet skill.

**What workers produce:** three mergeable PRs, each green on its acceptance anchors.
**What workers do NOT do:** write SESSIONS/STATE/plan/boards/ADRs/Pine; adjudicate cards;
re-patch `firm_rules`; build a new MC engine; touch the c1 rail / `dry_run`.

---

## §2 — Claim manifest (dispatch table; orchestrator-owned)

| Packet | Branch | File footprint (DISJOINT) | Solo est. | Status |
|---|---|---|---|---|
| A — `msl_preflight` | `cursor/msl-tooling-pA` | `lab/research_utils/msl_preflight.py` (new) · `tests/test_msl_preflight.py` (new) · `lab/research_utils/fixtures/msl_preflight/` (new) | ~1.5h | **MERGED** #775 |
| B — `msl_score` | `cursor/msl-tooling-pB` | `lab/research_utils/msl_score.py` (new) · `tests/test_msl_score.py` (new) · `lab/research_utils/fixtures/msl_score/` (new) | ~2h | **MERGED** #776 |
| C — `tv_static_equity` | `cursor/msl-tooling-pC` | `lab/research_utils/tv_static_equity.py` (new) · `tests/test_tv_static_equity.py` (new) · `lab/research_utils/fixtures/tv_static_equity/` (new) | ~45m | **MERGED** #774 |

**Reserved to the orchestrator — no worker writes these:** `docs/SESSIONS.md`, `STATE.md`,
`CLAUDE.md`, `lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/briefs/programs/2026-08-12-msl-program-plan.md`
(§6 claim rows), `docs/adr/**`, `ops/instruments/**`, `core/**`, `**/*.pine`,
`ops/c1_rail/**`, and any other packet's footprint.

Footprints are disjoint by construction: three distinct module/test/fixture trees.

---

## §3 — Packet A: `msl_preflight` (evidence-only CLI)

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git fetch origin
git log --oneline -5 origin/main
test -f lab/research_utils/msl_preflight.py && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
gh pr list --state open --search "msl_preflight OR msl-tooling-pA"
```

**No-op condition:** if `lab/research_utils/msl_preflight.py` already exists on `origin/main`
(or an open PR already owns that footprint) → **DONE**, cite the commit/PR; do not duplicate.

**Frozen scope.** Create a CLI that reads a slate-card YAML and emits **evidence tables only**:

1. **Dedup block** — run `rg` (or equivalent) against the registry/graveyard paths named in the
   card (or a frozen default set under `docs/rejected_candidates.md` + `lab/CATALOG.md` stubs)
   and print **raw hit lines**. A fixture with a known registry string MUST surface that string.
2. **Instrument cell block** — subprocess
   `python scripts/instrument_profiles.py cell <symbol> <mechanism>` and print **raw stdout**
   (incl. any `BINDING BAR:` lines). A fixture on an instrument with bars MUST emit a bar line.
3. **Arithmetic tables** — cost-law / payability / worst-day / σ_d / **implied-SR** computed from
   card fields. Implied-SR uses the §0 formula verbatim. Fade-region fixture → **2.98**.
4. **Clean card round-trip** — hand-computed fixture loads, prints tables, exits 0; no exception.

**CLI shape (recommended default):**
`python -m research_utils.msl_preflight path/to/card.yaml` (or `python lab/research_utils/msl_preflight.py …`)
printing UTF-8 text/JSON blocks. Exit 0 on successful evidence emission even when bars/hits
appear — **surfacing ≠ killing**.

**Acceptance tests (`tests/test_msl_preflight.py`):**

- Fixture with known registry hit → hit appears in dedup block.
- Fixture on MES (or other barred instrument) → output contains `BINDING BAR:`.
- Fade-region fixture → implied-SR **2.98** (±0.01) in the arithmetic table.
- Clean card round-trips (load → emit → no crash; golden substring or structured keys present).

**Forbidden moves (A).** No PASS/KILL/route strings as verdicts. No edits outside footprint.
No ADR/Pine/`firm_rules` edits. No writes to SESSIONS/STATE/plan.

---

## §3b — Packet B: `msl_score` (adapter only)

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git fetch origin
git log --oneline -5 origin/main
test -f lab/research_utils/msl_score.py && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
gh pr list --state open --search "msl_score OR msl-tooling-pB"
```

**No-op condition:** if `lab/research_utils/msl_score.py` already exists on `origin/main`
→ **DONE**, cite commit; do not duplicate.

**Frozen scope.** Adapter: TV trade-list CSV → daily panel (`date`, `pnl_usd`, `intraday_low`)
→ `nsurv_channel.score_nsurv` and/or `book_score.score_book` → TNEC verdict JSON.

Required behaviour:

- **Entry/Exit pairing** from TV export columns (Trade #, Type, Date and time, Net P&L USD,
  and when present Run-up/Drawdown). Mirror pairing discipline from `score_cell.py` /
  trade-csv-reconcile — do not invent a second P&L definition.
- **Honesty rule:** if `intraday_low` is reconstructed from trade closes only (omitting
  within-trade open excursion), the output JSON **MUST** carry label **`LOWER BOUND`**
  even though the channel still scores. If TV Run-up/Drawdown columns are present and used
  to bound within-trade excursion, that label may be omitted / set to full-honesty.
- Call `score_nsurv` (single) / `book_score` (composed) — **no new remc**.
- Consume `firm_rules` as-is (`dd_lock_offset_usd` already corrected). Verify; never re-patch.
- Emit JSON including the channel's N-SURV line / partition busts and the honesty label.

**Acceptance tests (`tests/test_msl_score.py`):**

- **Primary:** reuse / assert against `tests/test_nsurv_channel.py` headline_bust pins
  (import helpers or feed an identical daily panel through the adapter's scoring path and
  match channel output).
- Hand-paired TV-export fixture round-trips exactly (panel rows + JSON keys).
- LOWER BOUND branch: fixture without Run-up/Drawdown → label present; fixture with usable
  excursion columns → documented honesty path.

**Forbidden moves (B).** No new MC engine. No `firm_rules` / `dd_protection` edits. No writes
outside footprint. No SESSIONS/STATE/plan. Optional ORB 77.01% cross-harness pin is **out of
scope** (needs pruned git-history retrieval — do not chase).

---

## §3c — Packet C: `tv_static_equity` (lift static-equity util)

**Phase-0 staleness check (run FIRST; if already satisfied, return DONE and cite the commit):**

```bash
git fetch origin
git log --oneline -5 origin/main
test -f lab/research_utils/tv_static_equity.py && echo "ALREADY EXISTS -- STOP, return DONE with the commit that added it"
gh pr list --state open --search "tv_static_equity OR msl-tooling-pC"
```

**No-op condition:** if `lab/research_utils/tv_static_equity.py` already exists on `origin/main`
→ **DONE**, cite commit; do not duplicate.

**Frozen scope.** Lift/generalize `static_equity_recompute` from
`lab/archive/transfer_expression_grid_2026-08/cells/striker_mnq/score_cell.py` into
`lab/research_utils/tv_static_equity.py`:

- Parameterize `point_value_usd` and `commission_per_side` (required args).
- Input: TV trade-list DataFrame (or path) with Entry/Exit rows.
- Output: per-trade static-equity series + summary dict compatible with score_cell's keys
  (`n_legs`, `tv_net_sum`, `recompute_net_sum`, `max_abs_delta`, `mean_abs_delta`,
  `ok_within_1usd`) plus an explicit flag when the export looks **compounded** (TV equity
  path diverges from static recompute beyond tolerance) → `compounded_divergent: true`.
- Do **not** edit `score_cell.py` in this packet (orchestrator may later thin-wrap).

**Acceptance tests (`tests/test_tv_static_equity.py`):**

- Hand-recomputed known export matches (fixture under `fixtures/tv_static_equity/`).
- Compounded fixture flagged divergent (`compounded_divergent` / equivalent).

**Forbidden moves (C).** No edits to transfer-grid cell files. No writes outside footprint.
No SESSIONS/STATE/plan.

---

## §4 — Falsifiable hypotheses

**H-A:** a slate-card YAML can be reduced to evidence tables (dedup raw · cell raw · arithmetic
incl. implied-SR) without embedding adjudication, and the fade-region arithmetic reproduces
**2.98**. **FALSIFIED** if implied-SR cannot match 2.98 under the §0 formula for any honest
fixture — bounce `NEEDS_CONTEXT` with computed vs pinned.

**H-B:** TV trade-list → daily panel → existing `score_nsurv`/`book_score` is sufficient for a
TNEC verdict JSON, and the LOWER BOUND label is enforceable when excursion is reconstructed
from closes. **FALSIFIED** if the channel rejects the adapted panel for a structural contract
reason the adapter cannot fix without editing `nsurv_channel` — bounce `NEEDS_CONTEXT`.

**H-C:** `static_equity_recompute` generalizes to a shared util without cell-local constants,
and can flag compounded divergence. **FALSIFIED** if TV column schema in fixtures cannot
support pairing without inventing columns — bounce `NEEDS_CONTEXT`.

---

## §5 — Forbidden moves (fleet-wide, in addition to per-packet)

- No writes to any orchestrator-reserved file listed in §2.
- No writes outside your declared file footprint, for any reason.
- No commit to `main`, no merge (push + open PR is allowed per §0.5 q7).
- No resolving ambiguity: halt to `CURSOR_RETURN.md` as `NEEDS_CONTEXT` instead.
- No touching another packet's files, even to fix an obvious defect — report it instead.
- **No data purchase, no `db_fetch pull`, no `register_search open`.** `$0 / K=0` is absolute.
- **No mechanism / no Pine / no ADR authorship / no rail / no `dry_run` toggle.**
- **No adjudication in W-A** (no PASS/KILL/route as tool output semantics).
- **No new MC engine in W-B.**
- No `--no-verify`, no skipping gates, no disabling a failing test to go green.
- No editing `firm_rules` / `dd_protection` / locked strategy parameters.

---

## §6 — Gate criteria and status taxonomy

**Binary verdict per packet.** The packet's §4 hypothesis returns exactly one of:
**RESOLVED** (spec met, gates green), **FALSIFIED** (falsifier fired — report, do not force),
or **AMBIGUOUS** (bounce `NEEDS_CONTEXT`).

RESOLVED requires all of: (a) diff touches ONLY the declared footprint; (b) acceptance tests
present and green; (c) `python -m pytest tests/test_<module>.py -q` green; (d)
`python scripts/check_boundaries.py` clean; (e) no forbidden-move violation.

**Return contract.** Write `CURSOR_RETURN.md` at the worktree root with exactly one status:

- `DONE` — spec met, gates green.
- `DONE_WITH_CONCERNS` — spec met, but something the orchestrator must adjudicate. State it.
- `NEEDS_CONTEXT` — the spec is ambiguous or its premise is false. State what you need.
- `BLOCKED` — cannot proceed. State why.

Include: files changed, test command + output tail, PR URL if opened, any deviation from spec.
One `NEEDS_CONTEXT` bounce gets a re-anchor + re-dispatch; a second means the packet falls
back to CC solo.

---

## §7 — Merge order (orchestrator)

Packets are independent. Prefer **C → A → B** or **A → C → B** (B is heaviest; land thin
utils first). Re-run fast gates between merges.

**Single integration commit (orchestrator only, after all green merges):** update program
plan §6 (`P2 tooling fleet → MERGED`), append `docs/SESSIONS.md`, flip this manifest's
statuses to **MERGED**, carry Open/next forward. Workers never write those files.

---

## §10 — Audit hooks (runnable)

```bash
# Footprints exist and stay disjoint
test -f lab/research_utils/msl_preflight.py && echo "A: present"
test -f lab/research_utils/msl_score.py && echo "B: present"
test -f lab/research_utils/tv_static_equity.py && echo "C: present"

# W-A evidence-only (no adjudication API)
rg -n "PASS|KILL|route_verdict|adjudicat" lab/research_utils/msl_preflight.py || echo "OK: no adjudication API"

# W-B reuses channel (no remc reimplementation)
rg -n "score_nsurv|score_book" lab/research_utils/msl_score.py | head
rg -n "run_tier_remc|simulate_path" lab/research_utils/msl_score.py && echo "FAIL: remc leaked" || echo "OK: no remc"

# W-C parameterized lift (no silent MNQ-only hardcode required at module top)
rg -n "def static_equity|point_value|commission" lab/research_utils/tv_static_equity.py | head

# Fleet-wide: no core/ops/docs governance writes by workers
git diff --name-only origin/main...HEAD
# worker PR diffs must be subset of their §2 footprint

# No spend
rg -n "db_fetch|register_search" lab/research_utils/msl_*.py lab/research_utils/tv_static_equity.py || echo "OK: no pull"
```
