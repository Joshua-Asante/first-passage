# CC Handoff — Discovery pipeline hardening (3 tracks: date-cap · consistency battery · breadth column)

**Date:** 2026-07-11
**Spawn target:** Claude Code (research venv) — three independently-dispatchable tracks
**Repo:** `multi_firm_operations`
**Target path:** `docs/briefs/rnd-pipeline/2026-07-11-cc-handoff-discovery-pipeline-hardening.md`
**Brief type:** CC handoff (multi-track)
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **Ordering constraint (binding):** Track A edits `db_fetch.py`, a frozen deliverable of the pending stack PR (`claude/databento-research-stack-226b46`). Per `docs/adr/2026-07-10-databento-research-stack.md` §5 ("post-integration amendments go through the normal skill-authoring path with their own review"), Track A lands **after the stack PR merges, as its own commit/PR** — never folded into the integration diff. Tracks B and C are new files and may proceed once the stack is available.

---

## §0 — Rule 0 reads (PHASE 0 — CC executes BEFORE proposing any diff)

The authoring environment (claude.ai advisor) could not read the target source (local Windows-MCP server unresponsive mid-session). Per brief-authoring's canonical pattern, §0 is a **Phase-0 task for CC**: `cat` each file at the current merge commit and report the named structures BELOW **before** writing a single line of change. If repo state contradicts an assumption in §2, return `NEEDS_CONTEXT` with the discrepancy quoted — do not proceed on a stale assumption.

- `.claude/skills/databento-data/scripts/db_fetch.py` — report: the argparse subcommand/flag structure (`estimate` / `pull`), the **cache-key construction** (which request params key the DBN cache), and the exact cost-gate control flow (where `--max-cost` aborts). *(Track A patch site.)*
- `.claude/skills/databento-data/reference/proxy-discipline.md` — confirm the ratified IS boundary (2018-12-31) and the 2019-05-06 micro-era start. *(Track A + C constants.)*
- `.claude/skills/strategy-validation/scripts/selection_tests.py` — report: its subcommand structure and how it constructs bootstrap CIs (does it call `arch` or resample IID?). *(Track B extend-vs-new decision.)*
- `.claude/skills/strategy-validation/scripts/deflated_sharpe.py` + `SKILL.md` §8 — confirm the block-bootstrap engine already imported (`arch.bootstrap`), so Track B reuses it rather than reimplementing. *(Track B primitive reuse.)*
- `core/portfolio_mc.py` — report: whether the joint **Mon-anchored week-block bootstrap frame** is built by an **importable pure function** or inline in a script `__main__`; and the current commit (memory: the joint week-block engine is commit `83e589f` — verify). *(Track C design fork.)*
- `tests/test_mc_anchors.py` + `core/config/params.toml` — confirm the anchor test that must stay byte-identical (99.83/0.17/4.37) if Track C touches `portfolio_mc.py` at all.
- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` — the ratified defaults these three tracks operationalize.

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY required)

CC must **halt and ask** rather than default-guess on any of these; a wrong guess wastes the session.

- **(A) Track A flag surface** (operator): default assumed = additive, keyword-only, **default-off** — `--campaign-id <id>` + `--phase {discovery,oos}`; a `discovery` pull with `--end` beyond the campaign's ratified IS boundary (2018-12-31) **aborts**; cache entries tagged by era so a discovery read cannot silently include OOS bars. Confirm the flag names + that default-off preserves every existing call byte-for-byte.
- **(B) Track B home** (executor→operator, gated on the Phase-0 read of `selection_tests.py`): default = a **new module** `temporal_consistency.py` under the strategy-validation skill (the battery is conceptually distinct from within-panel selection tests, and §8 lives in strategy-validation). If Phase 0 shows `selection_tests.py` already has a clean subcommand pattern the battery fits, propose extend-in-place instead and ask before choosing.
- **(C) Track C design fork** (operator, gated on the Phase-0 read of `portfolio_mc.py`): if the week-block frame builder is **already importable as a pure function** → new breadth script imports it, zero engine change (preferred). If it is **not** cleanly importable → HALT and ask whether to (i) accept a documented read-only re-derivation of the frame in the new script, or (ii) do a pure-function **extraction refactor** of `portfolio_mc.py` under full anchor-preservation gates. Do **not** silently pick one.

---

## §0.5 — Answers (Phase-0 reads completed, 2026-07-11)

All three forks resolved by opening the actual target files (Rule 0), not by
re-deriving from a prior secondhand report. No code has been written — this is
the Phase-0 read + fork resolution only; the tracks remain gated on Joshua's go
to execute.

**(A) Track A flag surface — CONFIRMED, no changes to the proposed design.**
Read `.claude/skills/databento-data/scripts/db_fetch.py` in full (157 lines).
- `estimate`/`pull` share a `common` parser (`--symbols --stype --schema --start --end`, lines 122–138); `pull` adds `--max-cost` (required, no default), `--force`, `--out` (lines 144–149). **No name collision** with `--campaign-id` / `--phase`.
- Cache key (`_cache_path`, lines 59–62): SHA1 of `DATASET|symbols|stype|schema|start|end` → `{schema}_{stype}_{digest}.dbn`. Folding `campaign_id`/`phase` into that join string **only when non-None** keeps the hash — and every existing cache filename — byte-identical for calls that omit the new flags.
- Cost-gate flow (`pull`, lines 87–95): always calls `estimate()` first, then aborts if `cost > args.max_cost and not args.force`. The `--phase discovery` era-boundary abort should short-circuit **before** this (fail cheap, before even the free metadata call) — it does not need to touch the cost-gate order.
- Key handling (`_client`, lines 41–45): reads only `os.environ["DATABENTO_API_KEY"]`; untouched by this track.

**Confirmed:** `--campaign-id <id>` (str, default `None`) + `--phase {discovery,oos}` (default `None`), added to `common` (both subcommands carry them, enforcement only in `pull`). Design is achievable byte-identical for the no-flag path. **Track A cleared to implement as specified.**

**(B) Track B home — CONFIRMED, new module stands.**
Read `.claude/skills/strategy-validation/scripts/selection_tests.py` in full (128 lines).
- **Not a clean subcommand pattern.** One `main()`, one positional `cmd` (`choices=['bootstrap','dropk','halves','bestof','perm','costs']`), one `if/elif` dispatch, and every subcommand shares one flat, already-overloaded flag namespace (`--by`, `--labels`, `--k`, `--gate`, `--commission-pct`, …) — materially different from `register_search.py`'s or `db_fetch.py`'s clean `add_subparsers()` architecture.
- **No `arch` import anywhere** — pure numpy/pandas, IID resampling throughout (`bootstrap`: `rng.choice(p, n, True)`, line 54; `bestof`/`perm`: label permutation on pooled per-trade PnL, lines 73–110). Track B's CUSUM null requires the `arch` block-bootstrap engine (§8/8a) — a dependency this file does not carry today.
- Shape mismatch: `selection_tests.py` operates on one TV-export CSV's per-trade PnL; the battery needs OOS calendar-year sub-eras, externally-supplied regime labels (ruptures/HMM), and an edge-series CUSUM — a different input shape and provenance.

**Confirmed:** new module `temporal_consistency.py` under `.claude/skills/strategy-validation/scripts/`, importing `arch`, per §2. Extending in place would both violate the file's current zero-heavy-dependency design and further overload its flat flag namespace. **Track B cleared to implement as specified (new module).**

**(C) Track C design fork — CONFIRMED, zero-engine-change path (re-verified directly, not from a secondhand report).**
Read `core/portfolio_mc.py` in full (51-line facade) and opened `core/mc/ingest.py` / `core/mc/simulation.py` directly.
- `build_daily_panel(trades_by_strat, allocations, fixed_1r_reference=None) -> (panel_df, scale_info)` — `core/mc/ingest.py:139`, pure function (risk-normalizes P&L, aggregates to business days; no I/O, no global state).
- `build_week_blocks(panel) -> np.ndarray` — `core/mc/ingest.py:169`, pure function (Mon-anchored non-overlapping 5-bday blocks).
- `run_seed(seed, n_sims, blocks, dd_trigger, dd_scale, ...) -> dict` — `core/mc/simulation.py:125`, pure function (deterministic block-bootstrap for one RNG seed).
- `core/portfolio_mc.py` is a compatibility facade that re-exports every non-dunder name from `mc.modes` (lines 19–21) — a new script does **not** need the facade at all; it imports `build_daily_panel`/`build_week_blocks` from `core.mc.ingest` and `run_seed` from `core.mc.simulation` directly. Anchor: last commit touching both files is `f2be990` (2026-07-11); current HEAD `4b810a6`.

**Confirmed: the preferred path applies.** The breadth script imports these three functions unmodified, appends the candidate's daily P&L as a 5th panel column before `build_week_blocks`, and runs `run_seed` unchanged — **zero engine change, no extraction refactor.** The §0.5(C) HALT fork does not trigger; `portfolio_mc.py`'s MC behavior and the 99.83/0.17/4.37 anchor are untouched by construction (the breadth script never invokes the 4-leg config path). **Track C cleared to implement as specified (import, do not refactor).**

---

## §1 — Context

The discovery-campaign template (2026-07-10, ratified 2026-07-11) encodes three disciplines that are currently *disciplinary* (operator must remember them) rather than *structural* (code enforces them): the IS/OOS partition, the temporal-consistency battery, and the incremental-breadth test. These three tracks make each structural. They are the follow-ups explicitly deferred at template-authoring time as post-integration, gateable work — not folded into the stack integration because each touches either a frozen deliverable (A) or production risk-adjacent code (C) or a statistical surface that must reuse vetted primitives (B). This handoff is the gated form; it exists so the changes are executed where they can be tested, boundary-checked, and anchor-verified — none of which the advisor environment can do.

**What CC is NOT asked to do:** modify any locked strategy parameter, allocation, `dd_protection` constant, or Pine source; change `portfolio_mc.py`'s MC behavior (the 99.83/0.17/4.37 anchor is inviolable); reimplement any `arch`/`skfolio` primitive; wire anything toward live execution (R6 = NO-GO).

---

## §2 — Execution plan (three independent tracks)

### Track A — `db_fetch.py` campaign-scoped date-cap (structural IS/OOS enforcement) — LANDS POST-STACK-MERGE
- **Goal:** a discovery-phase pull physically cannot read the OOS partition; the cache cannot silently mix eras.
- **Action:** additive `--campaign-id` + `--phase {discovery,oos}` (default-off per §0.5(A)). In `discovery` phase, refuse `--end > 2018-12-31` (the ratified IS boundary) with a clear abort; tag/partition the DBN cache by `(campaign_id, phase)` so a discovery read returns only IS bars. **Preserve byte-for-byte:** the env-var-only key handling, the mandatory-`estimate`-before-`pull` gate, and the `--max-cost` abort. The new path adds a cap; it removes no guard.
- **Per-step gate:** `check_boundaries` green; existing skill tests pass unchanged; **new test**: a `--phase discovery --end 2019-06-01` pull aborts; a default (no `--phase`) call is byte-identical to pre-change behavior; `git grep -nE 'db-[A-Za-z0-9]{20,}'` → zero key hits; the other two delivered skill files untouched (`git diff --stat` scoped to `db_fetch.py` only).
- **Return artifact:** the diff + the new test + a one-line note in the skill's SKILL.md red-flags (era-mix is now a hard abort).

### Track B — temporal-consistency battery (`temporal_consistency.py`, pending §0.5(B))
- **Goal:** the ratified four-part battery as runnable code, orchestrating **vetted primitives** (import `arch`; do not reimplement).
- **Action:** implement (a) sub-era sign consistency (≥ ⌈0.7·Y⌉ of Y calendar-year sub-eras sign-positive over the OOS window); (b) drop-top-year concentration (survivor's edge stays > gate with its single best year removed); (c) regime-slice survival (accept externally-provided ruptures/HMM labels; report edge per slice; labels are **test conditions, never filters**); (d) CUSUM on the candidate's own edge series over the OOS era, with the **null calibrated via the existing block-bootstrap engine** (same `arch` stationary/circular bootstrap as §8 — NOT a hand-rolled IID null). Output a per-candidate battery verdict + the calibrated CUSUM spec (the artifact that ships with an admitted candidate per the decay-monitor requirement).
- **Per-step gate:** unit tests on synthetic series — a known-consistent edge PASSES all four; a single-year-concentrated edge FAILS drop-top-year; a linearly-decaying edge TRIPS CUSUM; a regime-confined edge fails slice survival. `check_boundaries` green. **No reimplementation:** grep the diff for any hand-rolled bootstrap/normal-null — must import `arch`.
- **Return artifact:** the module + tests + a §-hook in strategy-validation SKILL.md pointing Stage-6 of the campaign template at it.

### Track C — incremental-breadth 5th column (read-only vs `portfolio_mc.py`, pending §0.5(C))
- **Goal:** given a candidate's daily return series, compute its correlation to the four-leg composite and the **N_eff delta**, by feeding it as a 5th column into the SAME joint Mon-anchored week-block frame — without changing MC behavior.
- **Action:** per §0.5(C), preferred path = new script imports `portfolio_mc`'s frame builder and appends the candidate column, then computes realized cross-leg correlation and N_eff (dependence-breadth and Aegis-weighted risk-breadth, per Q-NEFF-1). If extraction is required, it is a pure-function refactor that **must leave the 4-leg MC output byte-identical**.
- **Per-step gate (load-bearing):** **sanity anchor** — with no 5th column, the breadth script must reproduce the known Q-NEFF-1 figures (N_eff ≈ **3.98** dependence / ≈ **3.09** risk) on the existing four legs; if it doesn't, the frame is being consumed wrong — STOP. If `portfolio_mc.py` was touched at all, `tests/test_mc_anchors.py` stays byte-identical (99.83/0.17/4.37). `check_boundaries` green.
- **Return artifact:** the breadth script + the sanity-anchor test + (only if refactor was needed) the byte-identity proof from `test_mc_anchors`.

### Step 2.N — Closure
Each track returns per §6 independently. Track A's return must state explicitly that it landed as a separate post-stack-merge commit (not in the integration diff).

---

## §4 — Falsifiable hypothesis

**H:** If each track lands its specified change AND passes its per-step gate (Track A: era-mix aborts + byte-identical default path + no key leak; Track B: the four synthetic-series tests + arch-reuse; Track C: the N_eff sanity anchor reproduces 3.98/3.09 + MC anchor byte-identical), then the three template disciplines are structurally enforced and the pipeline is hardened.

**Falsifier:** any track whose gate fails — Track C's N_eff sanity anchor not reproducing 3.98/3.09 (frame consumed wrong), Track A's default path drifting from byte-identity (a guard was disturbed), or Track B tripping on a hand-rolled null (reimplementation crept in) — is **not landed**; the track returns `BLOCKED`/`DONE_WITH_CONCERNS` and the change is withheld pending fix. A gate that cannot be made to pass falsifies the track's design, not just its implementation.

**Ambiguous-hold if:** Phase 0 reveals a structural obstacle (e.g., `portfolio_mc.py` frame not importable) → the affected track holds at the §0.5 decision point for operator input; the other tracks proceed.

---

## §5 — Forbidden moves (each genuinely tempting)

- **Folding Track A into the stack PR "since it's the same skill."** The stack integration is as-delivered (ADR §5); Track A is a separate post-merge commit with its own review.
- **"Improving" `db_fetch.py`'s cost gate or key handling while in there.** Track A is additive-only; touching the estimate gate or env-var handling is scope creep that fails the spec-compliance pass (§7).
- **Reimplementing a bootstrap or a normal-null in Track B.** strategy-validation §8 forbids it — import `arch`; the CUSUM null uses the same block engine. A hand-rolled null is the classic subtle-correctness trap.
- **Modifying `portfolio_mc.py`'s MC behavior for Track C.** The 99.83/0.17/4.37 anchor is inviolable; breadth reads the frame, it does not change the engine. A refactor is allowed ONLY as behavior-preserving extraction under the anchor test.
- **Skipping the N_eff sanity anchor and trusting the breadth number.** Reproducing 3.98/3.09 on the 4 legs is the proof the frame is consumed correctly; without it the 5th-column correlation is unverifiable.
- **Treating any of these as licensing live execution.** R6 = NO-GO; none of this code places an order.

---

## §6 — Gate + status return taxonomy

Each track returns exactly one of: `DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`, with `BLOCKED` carrying its mandatory sub-case (`BLOCKED — context-problem` → re-dispatch with context; `BLOCKED — capability-problem` → stronger model/human; `BLOCKED — scope-problem` → decompose; `BLOCKED — plan-itself-wrong` → escalate to parent). Use `NEEDS_CONTEXT` (not BLOCKED) when Phase 0 finds a supplyable gap; use `DONE_WITH_CONCERNS` when a track's gate passes but CC noticed something off-pattern the parent should adjudicate before accepting.

Per-track binary verdict maps to the four-state as: gate fully green + spec-exact → `DONE`; gate green but a flagged doubt → `DONE_WITH_CONCERNS`; a missing input → `NEEDS_CONTEXT`; an unresolvable obstruction → `BLOCKED — <sub-case>`. Program-level: the handoff is **RESOLVED** when all three tracks return `DONE`/`DONE_WITH_CONCERNS` and their diffs are accepted; **AMBIGUOUS** if a track holds at a §0.5 fork; **FALSIFIED** for any track whose gate cannot be made to pass (change withheld).

---

## §7 — Parent-session review (two passes, then consolidated)

Per track, two passes: **spec-compliance** (did CC build EXACTLY §2 — a "while I was in there" cost-gate tweak in Track A, or an unrequested feature in Track B, fails pass 1 even if good) then **quality** (gates sound, tests meaningful). After all three: a **consolidated read** — the known hot spot is that Track A's era boundary (2018-12-31), Track C's OOS start (2019-05-06), and the ratified template default must be the SAME constants; a drift among them is exactly the integration-inconsistency per-step gates miss.

---

## §10 — Audit hooks (runnable)

```bash
# Track A landed as its OWN commit, not inside the stack PR
git log --oneline --follow -- .claude/skills/databento-data/scripts/db_fetch.py | head
# era-mix is a hard abort now
python .claude/skills/databento-data/scripts/db_fetch.py pull --phase discovery --end 2019-06-01 --symbols GC.FUT --stype parent --schema ohlcv-1h --start 2010-01-01 --max-cost 5.00 2>&1 | grep -i "abort\|IS boundary"

# Track B imports arch, reimplements nothing
grep -n "from arch\|import arch" .claude/skills/strategy-validation/scripts/temporal_consistency.py
python -m pytest tests/ -k temporal_consistency -q

# Track C reproduces the N_eff sanity anchor and leaves the MC anchor byte-identical
python -m pytest tests/test_mc_anchors.py -q                 # 99.83/0.17/4.37 unchanged
grep -n "3.98\|3.09" <track-C-sanity-test>                  # N_eff dependence/risk reproduced on 4 legs

# The three era constants agree (consolidated-read check)
grep -rn "2018-12-31" .claude/skills/databento-data/scripts/db_fetch.py
grep -rn "2019-05-06" .claude/skills/strategy-validation/scripts/temporal_consistency.py docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md

# This brief stays well-formed
python scripts/check_brief.py docs/briefs/rnd-pipeline/2026-07-11-cc-handoff-discovery-pipeline-hardening.md --type cc_handoff
```

---

## Verification (run before declaring this brief complete)

```bash
python scripts/check_brief.py docs/briefs/rnd-pipeline/2026-07-11-cc-handoff-discovery-pipeline-hardening.md --type cc_handoff
# Expected: no HARD violations (§0.5 present; §6 four-state taxonomy present)
```

---

## Landing note (Claude Code, 2026-07-11)

Landed as the brief-of-record. §0 confirmed the Databento stack PR **is merged**
(`1316290` / PR #308, feat `7814ec6`; skills on disk), so Track A's post-merge
ordering constraint is satisfied. All three §0.5 forks were subsequently resolved by
direct Phase-0 reads — see **§0.5 — Answers** above for the evidence and the
confirmed design for each track. **The three code tracks are still NOT executed** —
cleared to implement per §0.5, gated on Joshua's go per this brief's Authority line.
