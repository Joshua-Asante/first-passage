# ADR 2026-07-10 — Databento research stack: discovery-first futures research on deep granular data; Nautilus research-only; live rail KEEP

**Status:** `Accepted` — the strategic decision was made operator-side on 2026-07-10 (advisor session authored the deliverables; the CC handoff enacting it states "this handoff does not re-litigate it"). This ADR records the decision and lands with the integration commit.
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s1-environment-ratification.md` - the §2 rail-verdict clause only (TradingView/NinjaTrader8/Rithmic/Bulenox chain). The §4 falsifier never fired; the rail changed via a different mechanism these two ADRs describe.
**Superseded-in-part-by:** `2026-08-07-loop-s2-signal-host-fork.md` - the §2 rail-verdict clause only (TradingView/NinjaTrader8/Rithmic/Bulenox chain). The §4 falsifier never fired; the rail changed via a different mechanism these two ADRs describe.
**Retain-until:** none
**Decision date:** 2026-07-10
**Authors:** Joshua (decision) + claude.ai advisor (stack authoring + rail verdict) + Claude Code (integration + this record)
**Supersedes:** none. Extends the research layer; touches no execution, allocation, or strategy decision.
**Related:** `docs/ltm/briefs/futures_residual_program_2026-07-05.md` (the pre-registered lanes this stack serves — R5 DJ30/MYM edition, Aegis→6J, Guardian-MGC); `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` (P2 FALSIFIED on the as-mapped CME-micro venue — the finding that motivates *discovery-first* rebuilding instead of re-mapping CFD edges); `docs/adr/2026-06-17-dukascopy-retirement.md` + `docs/adr/2026-06-24-oanda-retirement.md` (prior data-feed retirements — Databento is the first vendor feed added since, and the first tick/book-capable one); `docs/adr/2026-06-05-monorepo-layer-boundaries.md` (the boundary contract the additions must survive); the 2026-07-09 DJ30→MYM prototype falsification (memory: structural venue costs, not tunable — the dead end that makes anomaly-*discovery* on native futures data the surviving research direction).
**Layer:** infrastructure + methodology (research tooling only). **Not** strategy/risk-control parameters — no SL/TP/ATR/risk%/pyramid constant, no `dd_protection` constant, no allocation, no Pine source is touched. The locked MC anchor (99.83/0.17/4.37) is untouched.

---

## §0 — Rule 0 reads (production-source verification)

All read 2026-07-10 in the integration worktree, branch `claude/databento-research-stack-226b46`, anchor `git log --oneline -1` = `e5a63f9` (merge of PR #307; merge-base with `origin/main` is the same commit — the branch is off current main).

- `CLAUDE.md` — live-execution posture 2026-07-06: manual trading retired, CFD winding down, futures scale rides the residual program's pre-registered lanes; **rail correction R3:** TradersPost cannot connect to Bulenox — the identified (not yet built) rail is **TradingView → CrossTrade → NinjaTrader 8 → Bulenox via Rithmic**; R6 GO/NO-GO not made; no live automated execution exists today. This ADR's rail verdict (§2) must not contradict that state — it doesn't; it KEEPs it.
- `.gitignore` — lines 12–14 already cover `.venv/`, `venv/`, `env/`; lines 39–41 cover `.env` / `.env.*` (with `!.env.example`). No gitignore edit is needed for the research venv or any env file; verified before venv creation.
- `scripts/check_boundaries.py` — `.claude/` is a governance prefix (line 44); governance→core is the only legal internal edge from there. The three bundled skill scripts import only stdlib/third-party (`databento`, optional `scipy`), so no illegal edge and no allowlist change. Name-collision index covers only `core/ lab/ ops/` top-level + `scripts/wfo` (lines 112–124) — skill scripts are not indexed, so no collision surface.
- `Makefile` (`validate` = `validate-params` + `validate-data` + `validate-pine`) + installed hook `.git/hooks/pre-commit` (six gates: validate_params, check_skill_refs --all, conditional data-manifests, check_pine_manifest, check_boundaries, check_path_liveness). Baseline run 2026-07-10 pre-change: all pass in this worktree (Pine + vendor-CSV checks WARN-skip as documented for clones without the gitignored bytes).
- `scripts/check_skill_refs.py` — bundled-asset refs (`scripts/…`, `references/…`) are never hard-failed (SKILL_ASSET_DIRS, line 82); only unresolved repo-navigation refs fail. The new skills' `reference/*.md` tokens resolve skill-relative.
- `scripts/validate_params.py` — `GUARDED_SKILLS = ("inqhiori", "ooda-loop", "programme-audit", "brief-authoring")` (line 751); the no-constants guard does not extend to the three skills landing here, and none of them restates an operational constant anyway.
- `.claude/skills/strategy-validation/SKILL.md` — patch anchors confirmed present: `description:` frontmatter (line 3) and `## Boundaries` (line 58). The §8 extension applies as three marker-anchored edits, not a rewrite.
- `pyproject.toml` — carries the ops-pipeline dependency set. The research stack is deliberately **not** added here (see §3, alternative "single environment").
- The three deliverable packages, read in full from `Downloads` extracts before placement: `databento-data/` (SKILL.md, `scripts/db_fetch.py`, `reference/schemas-and-symbology.md`, `reference/proxy-discipline.md`), `futures-anomaly-discovery/` (SKILL.md, `scripts/register_search.py`, `reference/tool-discipline.md`), `strategy-validation-EXTENSION.md` + `scripts/deflated_sharpe.py`. Verified: `db_fetch.py` reads the key only from `os.environ["DATABENTO_API_KEY"]` and its `pull` path is cost-gated behind a mandatory estimate + `--max-cost` ceiling; `register_search.py` and `deflated_sharpe.py` are stdlib-only (scipy optional). No file contains a key or any credential.

---

## §1 — Context

The futures pivot's edge-transfer gate closed FALSIFIED (P2, operator-ratified 2026-07-06): the locked CFD strategies do not transfer as-mapped to CME micros, and the 2026-07-09 DJ30→MYM prototype rebuild also died on structural venue costs. What survives is the reframe already approved 2026-07-08: futures edge must be **discovered natively on the futures venue**, not ported. Native discovery needs what TradingView exports cannot provide — deep (2010+), granular (tick/TBBO/order-book) CME history — and it manufactures multiple-comparisons risk at industrial scale, which the existing validation skill handled only within-panel (§5), not across K searched candidates.

This decision integrates a three-part research stack answering both gaps: **`databento-data`** (cost-gated GLBX.MDP3 access with parent→micro proxy discipline), **`futures-anomaly-discovery`** (candidate generation with mandatory pre-registered trial-count K), and a **`strategy-validation` §8 extension** (universe-level correction: SPA/StepM/MCS via `arch`, DSR via bundled script, PBO/CPCV via `skfolio`). Supporting Python stack: `databento stumpy ruptures tsfresh pycatch22 hmmlearn arch skfolio vectorbt nautilus_trader` (+ `pysr`), isolated in a dedicated research venv.

**Decision driver (one sentence):** with edge-porting falsified twice, the surviving futures path is discovery-first on deep granular data — which requires a data rail, a multiplicity ledger, and a universe-level gate to exist *before* the first mining run, because K cannot be reconstructed after results have been seen.

---

## §2 — Decision

**Decision:** Adopt the Databento research stack as the canonical futures-research data + discovery + validation layer, integrated as three skills under `.claude/skills/` plus a pinned, isolated research venv — research-only, with the live execution rail explicitly unchanged.

Component roles:

| Component | Role | Explicitly NOT |
|---|---|---|
| `databento-data` skill + `db_fetch.py` | Cost-gated GLBX.MDP3 pulls (estimate mandatory before every pull); schema ladder (bars → TBBO → depth → MBO); parent→micro proxy discipline with 2019+ native-micro OOS gate | Not a live data feed for execution; no pull without estimate |
| `futures-anomaly-discovery` skill + `register_search.py` | Candidate generation (STUMPY / ruptures / tsfresh / catch22 / hmmlearn / PySR) with K registered *before* results; cheap Bonferroni/BH triage on close | Never promotes a candidate; outputs are observations, not signals |
| `strategy-validation` §8 + `deflated_sharpe.py` | Universe-level correction consuming the ledger's K: SPA/StepM/MCS (`arch.bootstrap`), DSR, PBO via CPCV (`skfolio`) | Does not replace §1–§7 within-panel protocols |
| `nautilus_trader` | **Research / fill-realism backtesting only** — realistic fill simulation for surviving candidates | **Not an execution rail.** NautilusTrader has no Rithmic adapter and therefore cannot execute to Bulenox |
| `vectorbt` | Fast vectorized sweep layer for bar-level triage | Not the fill-realism arbiter |
| Research venv (`.venv`, py3.11) + `requirements-research.txt` lockfile | Isolation of the numba/Julia-heavy stack from the ops pipeline env | Research deps do not enter `pyproject.toml` |

**Live-rail verdict: KEEP** TradingView → CrossTrade → NinjaTrader 8 → Bulenox via Rithmic (the identified, not-yet-built rail per CLAUDE.md R3; R6 GO/NO-GO remains operator-only and unmade). Nautilus cannot reach Bulenox (no Rithmic adapter), so no migration question exists today. **Migration trigger:** the Nautilus-as-execution question re-opens if and only if the operation leaves the prop-firm model for a direct-API broker (e.g., IBKR) — at that point a fresh ADR weighs Nautilus against the incumbent rail.

**Data-spend discipline (binding):** every pull is preceded by a free `estimate`; `pull` refuses above `--max-cost`. The $125 free-credit window is the validation budget for the workflow itself.

**Effective:** immediately upon this commit.
**Scope:** research layer only (`.claude/skills/`, research venv, lockfile). No execution, allocation, strategy, or risk-control code is touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| NautilusTrader as unified research **and** execution platform | No Rithmic adapter → cannot execute to Bulenox; the prop-firm rail is non-negotiable while the residual program's lanes are Bulenox-denominated. Research-only role captured; execution role structurally impossible today. |
| Migrate to a direct-API broker now so Nautilus could execute | Inverts the decision hierarchy: the venue is chosen by the residual program (R6 GO/NO-GO, operator-only, unmade), not by tooling convenience. Recorded as the migration trigger instead. |
| Keep TV-only research (Pine + TV exports) for futures too | TV cannot serve deep granular CME history (tick/TBBO/MBO, 2010+), and the discovery-first reframe *requires* it. TV/Pepperstone remains canonical for the locked CFD legs — unchanged. |
| Alternative data sources (Dukascopy, OANDA, broker exports) | Both prior feeds retired by ADR (2026-06-17, 2026-06-24); neither offers CME order-book depth. Databento is the identified vendor with metadata-priced estimates, making the cost gate mechanically enforceable. |
| Install the stack into the existing ops env / `pyproject.toml` | The stack is numba-heavy (stumpy, vectorbt) plus a Julia runtime (pysr) with tight interlocking pins (nautilus_trader) — a dependency-resolution and stability hazard for the ops pipeline. Isolation in a pinned research venv is cheap; contamination is not. |
| Hand-roll the multiplicity/DSR/PBO layer instead of `arch`/`skfolio` | Bootstrap re-centering and purged CV have subtle correctness traps; the extension explicitly delegates to vetted libraries and hand-writes only the closed-form DSR. Re-implementation is forbidden (§5). |
| Status quo — no stack | Leaves the discovery reframe without data, without K accounting, and without a universe-level gate: the first mining run would be unsalvageably snooped (K undeclarable post-hoc). |

---

## §4 — Falsifier (revert trigger)

**Revert trigger (uselessness):** if by **2027-01-10** (two quarterly review cycles) the stack has produced **zero** closed `register_search.py` manifests whose survivors were handed to the §8 gate — i.e., no discovery run has completed the pipeline even once — the stack is dead weight; archive the three skills and retire the venv/lockfile via a superseding ADR.

**Revert trigger (cost-gate breach):** any Databento billing event that was not preceded by a recorded `estimate`, or any single pull >$25 without prior operator sign-off, falsifies the "mechanically enforceable cost gate" premise → freeze all pulls, audit the breach, re-decide the data rail.

**Rail-verdict falsifier:** the KEEP verdict is falsified only by its trigger — leaving the prop-firm model for a direct-API broker. If that happens, this ADR's rail section is superseded by a fresh execution-rail ADR; nothing here pre-commits that choice.

**Trigger check schedule:** rides the standing quarterly review (next 2026-08-08, then 2026-11-08; uselessness check due 2027-01-10). Check: `ls discovery_manifests/*.json` (or `DISCOVERY_LEDGER`) for closed manifests + Databento billing history vs. recorded estimates.

---

## §5 — Forbidden moves (under this ADR)

- **Wiring Nautilus (or any research component) toward live execution** — tempting once it's installed and simulating fills well; ruled out because no Rithmic adapter exists and the rail decision belongs to R6 (operator-only, unmade). Research code never places an order.
- **Running any discovery tool before `register_search.py open`** — the "just a quick look at the matrix profile" move. K cannot be declared after results are seen; the script refuses `close` without `open`, and the operator side must refuse the informal peek.
- **Pulling MBO/MBP-10 before a bar-level candidate survives** — the granularity temptation is the classic way to burn the credit budget on a hypothesis bars would have killed free. Schema ladder is binding.
- **Skipping the estimate because "it's small"** — every pull, no exceptions; the estimate is free by construction.
- **Adding research deps to `pyproject.toml` or installing them into the ops env** — single-environment convenience is exactly how a numba/Julia stack destabilizes the pipeline that computes live multipliers.
- **Treating a parent-era (ES/NQ/YM/GC) result as micro-validated** — the 1:10 economics re-scale + native-micro 2019+ OOS gate are mandatory before any candidate is trusted (proxy discipline).
- **"Improving" the three delivered skills or scripts during integration** — they are authored, tested deliverables; integration is as-is. Post-integration amendments go through the normal skill-authoring path with their own review.
- **Hardcoding, printing, or committing `DATABENTO_API_KEY`** — env-var reference only, everywhere, always.

---

## §6 — Consequences

**Positive:**
- The discovery-first reframe becomes executable: deep CME history behind a mechanical cost gate, trial-count K as a recorded fact, and a universe-level correction layer that was previously a known gap (§5 of strategy-validation was within-panel only).
- Multiplicity discipline moves from intention to file: pre-registration is a script artifact, matching the repo's pre-registration doctrine.

**Negative (real costs):**
- A second Python environment to maintain (heavy stack; pysr pulls a Julia runtime on first import). Owned via the pinned `requirements-research.txt`.
- Databento is metered: research now has a marginal dollar cost per query. The estimate gate bounds but does not eliminate spend.
- CME's 2025+ non-display/EOD licensing flux (noted in the skill) means fee assumptions need re-confirmation before scaled pulls.

**Risks:**
- Stack-version drift (nautilus/vectorbt/numba pins are tight) — mitigated by the lockfile; upgrades are deliberate, not incidental.
- The JPY micro (M6J vs MJY, quote inversion) is flagged UNRESOLVED in `reference/proxy-discipline.md` — building the FX lane before resolving it is a named red-flag stop, not an ADR risk to accept.

**Downstream artifacts:**
- The three skills + lockfile land in the same commit as this ADR. `CLAUDE.md` / `STATE.md` are deliberately untouched (handoff scope); if the stack becomes load-bearing for a live decision, surfacing it in `CLAUDE.md` is a follow-up, not part of this change.

---

## §7 — Implementation plan

Enacted by the 2026-07-10 CC handoff (this commit):

- **Phase 0** — §0 reads + baseline gate run (done pre-change; all pass).
- **Phase 1** — research venv (worktree-root `.venv`, py3.11, gitignored) + full stack install + `requirements-research.txt` pin; `databento-data/` + `futures-anomaly-discovery/` placed as-is under `.claude/skills/`; `strategy-validation` patched via the three marker-anchored edits + `scripts/deflated_sharpe.py` added.
- **Phase 2** — env wiring verified: `DATABENTO_API_KEY` resolves from `os.environ`; free `estimate` call confirms the rail live; key appears in no output and no tracked file (grep-proven).
- **Phase 3** — full gate suite green (validate-params, data-manifests, pine-manifest, boundaries, skill-refs, path-liveness); commit on `claude/databento-research-stack-226b46`; PR for operator adjudication — no merge by the executor.

---

## §10 — Audit hooks (runnable)

```bash
# SECURITY: key in no tracked file — expect ZERO hits
git grep -nE 'db-[A-Za-z0-9]{20,}' -- . ':!*.lock'
grep -rIn 'DATABENTO_API_KEY' .claude/skills/   # env-var references only, never a value

# Skills present + patched
ls .claude/skills/databento-data/SKILL.md .claude/skills/futures-anomaly-discovery/SKILL.md
grep -n '## 8. Universe-level correction' .claude/skills/strategy-validation/SKILL.md
ls lab/databento_fetch/db_fetch.py \
   lab/discovery/register_search.py \
   lab/research_utils/deflated_sharpe.py
# skill wrappers (launchers) still present for skill-ref stability:
ls .claude/skills/databento-data/scripts/db_fetch.py \
   .claude/skills/futures-anomaly-discovery/scripts/register_search.py \
   .claude/skills/strategy-validation/scripts/deflated_sharpe.py

# Stack imports (research venv)
.venv/Scripts/python -c "import databento, stumpy, ruptures, tsfresh, arch, skfolio, vectorbt, nautilus_trader; print('stack OK')"

# Cost-gate discipline: estimate is free, pull is ceiling-gated (code assertion)
grep -n 'max-cost' lab/databento_fetch/db_fetch.py   # required arg, no default

# §4 uselessness check (quarterly; due 2027-01-10)
ls discovery_manifests/*.json 2>/dev/null || echo "no closed discovery runs yet"

# Boundary + validate gates
python scripts/check_boundaries.py && python scripts/validate_params.py && python scripts/check_skill_refs.py --all
```

---

## Verification

```bash
# Discipline checks (mechanical)
python <brief-authoring>/scripts/check_brief.py docs/adr/2026-07-10-databento-research-stack.md --type adr

# Production-source verification (Rule 0 confirmation)
git log --oneline -1                          # e5a63f9 at authoring
sed -n '12,14p;39,41p' .gitignore             # .venv + .env coverage
grep -n 'GUARDED_SKILLS' scripts/validate_params.py
grep -n 'SKILL_ASSET_DIRS' scripts/check_skill_refs.py
```

---

## Addendum (2026-07-11) — post-integration ledger-path anchor

Under §5's "post-integration amendments go through the normal skill-authoring path
with their own review," `register_search.py`'s manifest ledger default was anchored
from a cwd-relative `./discovery_manifests` to **`<repo-root>/discovery_manifests`**
(via `Path(__file__).resolve().parents[4]` at the time), so manifests land in one committed,
auditable location regardless of the invoking directory — matching the intent of §4's
uselessness check and §10's `ls discovery_manifests/*.json` hook (which both assume a
repo-root `discovery_manifests/`). The `DISCOVERY_LEDGER` override is unchanged, and a
`discovery_manifests/README.md` marks the committed home. Reviewed under
`docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md`; the stack's cost gate,
K semantics, and rail verdict are untouched.

## Addendum (2026-07-11) — code home relocates to `lab/` (Approach B)

Post-integration relocation (not an "improve the skills during integration" violation —
the deliverables already landed): **canonical Python for the Gen-2 stack moves under
`lab/`** so campaigns can import without `sys.path` hacks into `.claude/skills/`.

| Component | Canonical path | Skill `scripts/` role |
|---|---|---|
| DSR / step0 / selection / plateau | `lab/research_utils/` | stdlib subprocess launchers only |
| K-ledger (`register_search`) | `lab/discovery/register_search.py` | launcher |
| Databento fetch | `lab/databento_fetch/db_fetch.py` | launcher |

**Unchanged:** research-venv isolation (`requirements-research.txt` stays out of
`pyproject.toml`); cost gate; K semantics; live-rail KEEP; hand-roll ban on SPA/PBO/CPCV.
**Boundary:** skill wrappers must not import lab packages (governance→lab illegal);
they forward via `PYTHONPATH=lab python -m …`. Ledger default now uses
`research_utils.repo_root()` (still repo-root `discovery_manifests/`). Spec:
[`docs/superpowers/specs/2026-07-11-lab-research-stack-relocation-design.md`](../superpowers/specs/2026-07-11-lab-research-stack-relocation-design.md).
Planted-control DSR self-test: `tests/test_validation_selftest_dsr_gate.py`.

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-10 | Initial authoring, landed with the integration commit | Joshua + claude.ai (advisor) + Claude Code |
| 2026-07-11 | Addendum: `register_search.py` ledger default anchored to `<repo-root>/discovery_manifests` (cwd-independent) | Claude Code |
| 2026-07-11 | Addendum: Gen-2 script bodies relocate to `lab/`; skills become thin launchers | Cursor agent (lab-functions-eval worktree) |

## Addendum 2026-08-29 — §2 rail-verdict clause superseded-in-fact by the S1/S2 loop ADRs (adr-decay-audit `DECAYED_UNDOCUMENTED` discharge)

The `adr-decay-audit` sweep flagged §2's *"Live-rail verdict: KEEP TradingView → CrossTrade →
NinjaTrader 8 → Bulenox via Rithmic"* sentence as stale: current reality has moved past it with no
discharge recorded. This addendum is that discharge; §0–§10 above stay byte-unedited as the
historical record (Rule 14).

**What actually changed, and how.** §4's own **rail-verdict falsifier** — *"leaving the prop-firm
model for a direct-API broker"* — never fired; the prop-firm model is still the model. The rail
changed anyway, via an unrelated mechanism this ADR did not anticipate: the 2026-08-04 Tradeify
de-scope withdrew both Striker legs, and the 2026-08-07 loop closed it out — S1
([`2026-08-07-loop-s1-environment-ratification.md`](2026-08-07-loop-s1-environment-ratification.md))
ratified the environment (incumbent `Tradeify_Select_100K` eval, not Bulenox) and S2
([`2026-08-07-loop-s2-signal-host-fork.md`](2026-08-07-loop-s2-signal-host-fork.md)) ratified the
signal origin (a Python daemon, not TradingView). Neither S1 nor S2 originally listed this ADR
under their own `Supersedes:` field — this addendum plus the header field above is the missing
reciprocal edge, and both ADRs' `Related:` fields now point back here in turn.

**Current live rail, verified against production** (`ops/c1_rail/__init__.py`, docstring, this
session):

> *"c1 rail — ruled host → listener → CrossTrade → Tradovate (Tradeify Select 100K)."*

I.e.: **ruled Python signal host → listener → CrossTrade → Tradovate, on venue
`Tradeify_Select_100K`.** Every clause of the original §2 verdict has moved: TradingView → the
ruled Python-daemon host (S2); NinjaTrader 8 → Tradovate; Bulenox via Rithmic → Tradeify via
CrossTrade→Tradovate (S1). CrossTrade is the one leg that survived unchanged.

**What is NOT stale — untouched by this addendum.** This ADR's actual research-stack decision
(the component table: `databento-data` cost-gated GLBX.MDP3 access, `futures-anomaly-discovery`
candidate generation, `strategy-validation` §8 universe-level correction, Nautilus **research-only**
role, the isolated research-venv boundary) is unaffected — none of it depended on the §2 rail
identity, and none of it has been superseded. Only §2's rail-verdict sentence and §4's rail
falsifier (which never fired, and is now effectively moot — the rail already changed by the S1/S2
route, not the direct-API-broker route it names) are stale. Reader encountering §2/§4 today: read
the current rail from `ops/c1_rail/__init__.py` and the S1/S2 ADRs, not from this ADR's own text.
