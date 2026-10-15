# ADR 2026-07-10 — Databento research stack: discovery-first futures research on deep granular data; Nautilus research-only; live rail KEEP

**Current source disposition (reported 2026-09-10): Databento retired.** The operator has unsubscribed and retired Databento as an information source for First Passage. No replacement source is approved. See the retirement addendum below; historical acquisition decisions are not current authority to access Databento.

**Status:** `Accepted` — operator decision 2026-07-10; Databento acquisition retired 2026-09-10 (operator report, addendum below); the non-provider research-stack clauses stand.
**Superseded-by:** none
**Superseded-in-part-by:** `2026-08-07-loop-s1-environment-ratification.md` - the §2 rail-verdict clause only (TradingView/NinjaTrader8/Rithmic/Bulenox chain). The §4 falsifier never fired; the rail changed via a different mechanism these two ADRs describe.
**Superseded-in-part-by:** `2026-08-07-loop-s2-signal-host-fork.md` - the §2 rail-verdict clause only (TradingView/NinjaTrader8/Rithmic/Bulenox chain). The §4 falsifier never fired; the rail changed via a different mechanism these two ADRs describe.
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 per-path reads, §7, `## Verification`, the §2 data-spend and rail-verdict text, the §4 cost-gate and rail limbs, the §5 MBO/estimate bullets and most of §10 removed; Addendum 2026-08-29 shortened. Pre-trim text at blob `2d43500abe0e60251d0d94fafedfe99084621fe2` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).
**Decision date:** 2026-07-10
**Authors:** Joshua (decision) + claude.ai advisor (stack authoring + rail verdict) + Claude Code (integration + this record)
**Supersedes:** none. Extends the research layer; touches no execution, allocation, or strategy decision.
**Related:** `docs/ltm/briefs/futures_residual_program_2026-07-05.md` (the pre-registered lanes this stack serves — R5 DJ30/MYM edition, Aegis→6J, Guardian-MGC); `docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` (P2 FALSIFIED on the as-mapped CME-micro venue — the finding that motivates *discovery-first* rebuilding instead of re-mapping CFD edges); `docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md` §Retired feeds (prior data-feed retirements — Databento is the first vendor feed added since, and the first tick/book-capable one); `docs/adr/2026-06-05-monorepo-layer-boundaries.md` (the boundary contract the additions must survive); the 2026-07-09 DJ30→MYM prototype falsification (memory: structural venue costs, not tunable — the dead end that makes anomaly-*discovery* on native futures data the surviving research direction).
**Layer:** infrastructure + methodology (research tooling only). **Not** strategy/risk-control parameters — no SL/TP/ATR/risk%/pyramid constant, no `dd_protection` constant, no allocation, no Pine source is touched. The locked MC anchor (99.83/0.17/4.37) is untouched.

---

## §0 — Rule 0 reads (production-source verification)

All read 2026-07-10 in the integration worktree at anchor `e5a63f9`: `.gitignore`,
`scripts/check_boundaries.py`, `scripts/check_skill_refs.py`,
`.claude/skills/strategy-validation/SKILL.md`, `pyproject.toml` and the three delivered skill
packages. The per-path findings are in the pre-trim text (Revision line).

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
| `databento-data` skill + `db_fetch.py` | retired 2026-09-10 — the skill is a retirement notice | Not a live data feed for execution; no pull without estimate |
| `futures-anomaly-discovery` skill + `register_search.py` | Candidate generation (STUMPY / ruptures / tsfresh / catch22 / hmmlearn / PySR) with K registered *before* results; cheap Bonferroni/BH triage on close | Never promotes a candidate; outputs are observations, not signals |
| `strategy-validation` §8 + `deflated_sharpe.py` | Universe-level correction consuming the ledger's K: SPA/StepM/MCS (`arch.bootstrap`), DSR, PBO via CPCV (`skfolio`) | Does not replace §1–§7 within-panel protocols |
| `nautilus_trader` | **Research / fill-realism backtesting only** — realistic fill simulation for surviving candidates | **Not an execution rail.** NautilusTrader has no Rithmic adapter and therefore cannot execute to Bulenox |
| `vectorbt` | Fast vectorized sweep layer for bar-level triage | Not the fill-realism arbiter |
| Research venv (`.venv`, py3.11) + `requirements-research.txt` lockfile | Isolation of the numba/Julia-heavy stack from the ops pipeline env | Research deps do not enter `pyproject.toml` |

**Live-rail verdict:** superseded in part by S1/S2 (header; Addendum 2026-08-29); the current rail is in `ops/c1_rail/__init__.py`.

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

**Rail-verdict falsifier:** never fired; superseded by S1/S2 (Addendum 2026-08-29).

**Trigger check schedule:** rides the standing quarterly review (next 2026-08-08, then 2026-11-08; uselessness check due 2027-01-10). Check: `ls discovery_manifests/*.json` (or `DISCOVERY_LEDGER`) for closed manifests + Databento billing history vs. recorded estimates.

---

## §5 — Forbidden moves (under this ADR)

- **Wiring Nautilus (or any research component) toward live execution** — tempting once it's installed and simulating fills well; ruled out because no Rithmic adapter exists and the rail decision belongs to R6 (operator-only, unmade). Research code never places an order.
- **Running any discovery tool before `register_search.py open`** — the "just a quick look at the matrix profile" move. K cannot be declared after results are seen; the script refuses `close` without `open`, and the operator side must refuse the informal peek.
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

## §10 — Audit hooks (runnable)

```bash
# SECURITY: key in no tracked file — expect ZERO hits
git grep -nE 'db-[A-Za-z0-9]{20,}' -- . ':!*.lock'
grep -rIn 'DATABENTO_API_KEY' .claude/skills/   # env-var references only, never a value

# §4 uselessness check (quarterly; due 2027-01-10)
ls discovery_manifests/*.json 2>/dev/null || echo "no closed discovery runs yet"
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

§2's rail-verdict clause (TradingView → CrossTrade → NinjaTrader 8 → Bulenox via Rithmic) is superseded by S1
([`2026-08-07-loop-s1-environment-ratification.md`](2026-08-07-loop-s1-environment-ratification.md)) and S2
([`2026-08-07-loop-s2-signal-host-fork.md`](2026-08-07-loop-s2-signal-host-fork.md)); §4's rail-verdict falsifier never fired.
The reciprocal edges are in the header. The current live rail is read from `ops/c1_rail/__init__.py`; the research-stack decision is unaffected.

## Addendum 2026-09-10 - operator retirement of Databento

Joshua reported that Databento has been retired as an information source for First Passage and the subscription has been cancelled. This records the report date; it does not invent an earlier cancellation date or independently attest billing status. The retirement applies to research acquisition and the proposed daemon feed. Do not connect, pull, estimate, renew or infer access from installed SDKs, retained scripts, old credentials or earlier GO documents. No replacement source has been approved.

Historical artifacts, source fingerprints, tooling and prior results remain historical records; this change neither deletes data nor grants new rights to use retained vendor data. Non-provider research methodology and protection/strategy decisions are unchanged. The old acquisition and feed selections above are superseded by this explicit operator retirement, not by a claimed firing of the original falsifiers.

The [daemon build ADR](2026-08-08-s2b-signal-daemon-build.md) records the execution consequence. M1 item 5 still needs a qualifying evaluate-hook event and separate signoff. Any proposal to qualify controlled replay instead of the currently specified live feed requires an explicit acceptance amendment; retirement alone does not approve a substitute or weaken the no-arm gate.
