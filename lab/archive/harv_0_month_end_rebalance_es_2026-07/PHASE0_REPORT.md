# Q-HARV-0 Phase-0 Rule-0 Report (Track B)

**Wave:** Q-HARV-0 Wave 0 / Track B  
**Working directory:** `c:\Users\joshu\multi_firm_operations`  
**Report date:** 2026-07-11  
**Scope:** Read-and-report only. No analysis, no Databento pull, no schema decision.

---

## Summary card (PASS / FAIL / ABSENT)

| # | Read | Verdict |
|---|---|---|
| 0.1 | `docs/rule_0.md` | **PASS** |
| 0.2 | Branch `claude/databento-research-stack-226b46` → main (PR #308) | **PASS** (MERGED) |
| 0.3 | `db_fetch.py` estimate / pull `--max-cost` (path remap) | **PASS** |
| 0.4 | futures-anomaly-discovery SKILL + `register_search.py` K ledger | **PASS** |
| 0.5a | strategy-validation SKILL §8 micro-era / native-micro proxy | **PASS** (wording noted; HARV uses §4 P-micro-OOS) |
| 0.6 | Brief § headers vs `inquire_brief.md` drift | **PASS** (drift listed; brief untracked) |
| 0.7 | `scripts/check_brief.py` hash + runnable | **PASS** runnable; repo-side check **MALFORMED**; skill-side **PASS** w/ WARN |
| 0.8 | `ops/instruments/ES.md`, `YM.md` | **ABSENT** |
| 0.9 | Envelope reconcile | **REPORTED** (5 contradictions; see ENVELOPE_RECONCILE.md) |
| 0.10 | `docs/ltm/briefs/Q-MECH-1.JPY_h_register.md` MECHANISM-NAMED-ENDOGENOUS | **PASS** (path remap) |

---

## 0.1 `docs/rule_0.md`

**`git log -1 --oneline -- docs/rule_0.md`:**
```
7196893 docs: fix monorepo-move link rot + doc/code skew
```

**Finding for HARV-0:** Rule 0 is audit-first — read production sources before any decision brief or implementation touching risk controls; prior docs are not a Rule-0 substrate. Order: production file → brief against ground truth → validate → lock → implementation. Corollaries: code wins over docs on disagreement; load-bearing claims need code-resident verification. **Implication:** this Phase-0 report *is* the Rule-0 substrate for HARV-0; no Phase-1 analysis until 0.1–0.10 are reported (brief §0 Rule-0 statement).

**Verdict:** PASS

---

## 0.2 Branch `claude/databento-research-stack-226b46`

**Evidence:**
- Merge commit on ancestry of HEAD: `1316290 Merge pull request #308 from Joshua-Asante/claude/databento-research-stack-226b46`
- `gh pr view 308`: `state=MERGED`, `mergedAt=2026-07-11T02:15:25Z`, `baseRefName=main`, `headRefName=claude/databento-research-stack-226b46`, merge OID `1316290c4a037148300c13d04ae33dfcedf668a1`
- `git merge-base --is-ancestor 1316290 HEAD` → exit 0 (ancestor of current HEAD)
- Remote branch tip `origin/claude/databento-research-stack-226b46` is gone (expected after merge); merge commit remains on main lineage

**Finding for HARV-0:** Adjudication dependency cleared. `futures-anomaly-discovery` (K ledger) and strategy-validation §8 extension are on the mainline consumed by this executor. **No HALT / NEEDS_CONTEXT** on merge state.

**Verdict:** PASS

---

## 0.3 Databento fetch CLI — PATH REMAP

**Brief said:** `scripts/db_fetch.py`  
**Actual path:** `.claude/skills/databento-data/scripts/db_fetch.py`

**`git log -1 --oneline -- .claude/skills/databento-data/scripts/db_fetch.py`:**
```
0a1e8f9 fix(skills): drop deprecated get_cost mode= param; clarify venv-recreate note
```

**Argparse signature (confirmed):**
- Subcommands via `add_subparsers(dest="cmd", required=True)`:
  - `estimate` — free read-only cost/size/record dry-run; parents=`common` (`--symbols`, `--stype`, `--schema`, `--start`, `--end`)
  - `pull` — runs estimate first, then streams if under ceiling
    - `--max-cost` `float`, **required=True**, no default (abort if estimate exceeds)
    - `--force` optional override
    - `--out` optional parquet path

**Example from module docstring:**
```
python db_fetch.py estimate --symbols ... --schema ... --start ... --end ...
python db_fetch.py pull ... --max-cost 5.00 --out es_1m.parquet
```

**Finding for HARV-0:** Interface matches databento-data skill cost-gate doctrine (estimate before pull; `--max-cost` mandatory on pull). Brief path remap required for all audit hooks citing `scripts/db_fetch.py`.

**Verdict:** PASS (with PATH REMAP noted)

---

## 0.4 K ledger format — futures-anomaly-discovery

**Paths:**
- `.claude/skills/futures-anomaly-discovery/SKILL.md`
- `.claude/skills/futures-anomaly-discovery/scripts/register_search.py`

**`git log -1 --oneline` (both):**
```
4b810a6 docs(research): adopt tradable-anomalies statistics + land discovery-campaign chain
```

**Ledger format:**
- Default dir: `<repo-root>/discovery_manifests/` (override `DISCOVERY_LEDGER`)
- One JSON file per run: `{run_id}.json`
- Subcommands: `open` / `close` / `status`
- **`open` manifest fields:** `run_id`, `status="open"`, `opened_at`, `tool`, **`K`** (`--search-space-size`), `alpha`, `data_window`, `hypothesis`, `params`, `closed_at=None`, `results=None`
- **`close`:** submits survivor p-values; computes Bonferroni `alpha/K`, BH-FDR with denominator **pre-registered K**, expected FP `K*alpha`; hands off to strategy-validation (never promotes)
- SKILL.md: K-ledger / least-overfit-first discipline; statistics anchor `docs/methodology/references/statistics-of-tradable-anomalies.md`

**Finding for HARV-0:** Trial-count logging is JSON manifests under `discovery_manifests/`, not a CSV. K = pre-registered search-space size (hypotheses examined), immutable after `open`. Brief §8 / audit hook #3 should target this ledger.

**Verdict:** PASS

---

## 0.5a strategy-validation SKILL.md §8 — micro-era OOS / native micro proxy

**`git log -1 --oneline -- .claude/skills/strategy-validation/SKILL.md`:**
```
4b810a6 docs(research): adopt tradable-anomalies statistics + land discovery-campaign chain
```

**§8 Integration wording (load-bearing for micro-era):**
> A candidate is not promoted until it clears (8a) universe-adjusted significance, (8b) DSR, and — wherever time-series leakage is a risk — (8c) PBO, **on native micro-era data (the `databento-data` proxy gate)**. The ledger's cheap floor is a pre-filter, not a substitute for 8a.

**§8 ladder (full promotion path):** 8a SPA/RealityCheck/StepM/MCS (`arch.bootstrap`) → 8b Deflated Sharpe → 8c PBO via CPCV → 8d block bootstrap discipline.

**HARV-0 note (do not conflate):** This brief's gate uses **§4 `P-micro-OOS`** — frozen operationalization:
> **P-micro-OOS:** 2019-05→present native-MES conditional effect is **same-signed** as the parent-panel effect.

That is a **same-signed micro-era proxy check**, bundled into RESOLVED iff H1 ∧ P-placebo ∧ P-instrument ∧ P-covariance ∧ P-micro-OOS. It is **not** the full §8 SPA/DSR/PBO promotion ladder. Skipping micro-era is a listed forbidden move (#8) citing databento Rule 4.

**Ambiguity retained:** exact operator-facing wording of “micro-era OOS gate” vs §8 Integration vs P-micro-OOS remains in §0.5 item 1 (unresolved).

**Verdict:** PASS (read complete; scope note recorded)

---

## 0.6 Brief § headers vs `inquire_brief.md` — drift list

**Canonical template:** `.claude/skills/brief-authoring/references/inquire_brief.md`  
**`git log -1 --oneline`:**
```
c7c3345 chore(skills): import brief-authoring references/ to VC (durability)
```

**HARV brief:** `docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md`  
**`git log -1 --oneline`:** **ABSENT** (working tree only — `??` untracked; no commit history yet)

### Header drift (template → HARV)

| Template (`inquire_brief.md`) | HARV brief | Drift |
|---|---|---|
| §0 Rule 0 reads (production-source verification) | §0 Rule-0 reads (executor Phase 0: …) | Retitled; table of 0.1–0.10 executor reads vs bullet file list |
| §1 Context & motivation | §1 Context | Shortened; doctrine connections expanded |
| §2 Prior art / lineage | §2 Execution plan | **Renamed / repurposed** — lineage folded into §1; execution moved up |
| §3 Question (Q-X) | §3 Register record (candidate intake) | **Different purpose** |
| §4 Falsifiable hypothesis (H-X) | §4 Falsifiable hypothesis (frozen operationalization — one, only) | Same family; stronger freeze language |
| §5 Forbidden moves | §5 Forbidden moves | Aligned in role |
| §6 Gate criteria (closure verdict) | §6 Gate (binary) and reporting | Aligned; HARV adds reporting |
| §7 Execution plan | §7 Parent-session review (two passes + consolidated read) | **Different** — execution already in HARV §2 |
| §8 Verdict pre-registration | §8 Multiplicity & trial-count K | **Different** |
| §9 Closure record format | §9 Prop viability & operational checks | **Different** |
| §10 Audit hooks | §10 Audit hooks (runnable) | Aligned |
| — | §0.5 Ambiguity surfacing | **HARV-only** |
| Verification | Verification (author/executor…) | Present both |
| Pre-Lock Checklist | — | **Missing in HARV** |
| — | Appendix — lane observations… | **HARV-only** |

**check_brief results (also §0.7):** see below.

**Verdict:** PASS (drift enumerated; brief not yet on main)

---

## 0.7 `scripts/check_brief.py`

**`git log -1 --oneline -- scripts/check_brief.py`:**
```
e6ebbc6 chore(rnd-pipeline): close carried-forward follow-ups (check_brief, admissibility ADR, testpaths, native-tier driver)
```

**SHA256 (working-tree bytes):**
```
3c05d84e6ea85551562a46fa9ffedd47da09c5672473b69c647b286ffa911458
```

**Runnable:** YES (`python scripts/check_brief.py --help` succeeds; accepts `--type inquire` mapped to internal mechanical subset).

### Command run

```bash
python scripts/check_brief.py docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md --type inquire
```

**Repo-side result:**
```
check_brief: docs\briefs\Q-HARV-0-month-end-rebalance-ES.md  (type=brief)
  HARD: §4 | no hypothesis statement (expected 'H:' or 'hypothesis')

Summary: 1 HARD violation(s), 0 WARN violation(s)
RESULT: MALFORMED
note: 'inquire' is a skill-side brief type; this repo-side script ran only its mechanical
subset (internal type 'brief'). For the authoritative discipline gate, run the skill-side
checker (~/.claude/skills/brief-authoring/scripts/check_brief.py).
```

**Skill-side authoritative checker** (`~/.claude/skills/brief-authoring/scripts/check_brief.py`):
```
Brief: docs/ltm/briefs/Q-HARV-0-month-end-rebalance-ES.md
Type:  inquire

  [1] §0 Rule 0 reads populated                  ✓ PASS
  [2] §4 falsifiable hypothesis                  ✓ PASS
  [3] §5 forbidden moves explicit                ! WARN  — §5 has 0 bullet(s) — typically 3+ tempting moves should be listed
  [4] §6 binary verdicts (R/F/A)                 ✓ PASS
  [5] §3 question names symptom                  ✓ PASS
  [6] §10 audit hooks runnable                   ✓ PASS

RESULT: PASS (5/6 checks)  [1 warning(s)]
```

**Finding for HARV-0:** Repo-side `scripts/check_brief.py` is runnable but is a **mechanical subset** — it MALFORMED on §4 hypothesis regex while skill-side PASS. Prefer skill-side for inquire discipline. §5 WARN (0 bullets detected) may be a parser/header mismatch vs numbered list — do not “fix” without operator intent.

**Verdict:** PASS (tool exists + runnable); gate interpretation = skill-side PASS w/ WARN; repo-side MALFORMED noted

---

## 0.8 `ops/instruments/ES.md`, `YM.md`

**`git log -1 --oneline -- ops/instruments/ES.md`:** (no output) → **ABSENT**  
**`git log -1 --oneline -- ops/instruments/YM.md`:** (no output) → **ABSENT**  
**Filesystem:** `Test-Path` both → False

**Neighbors under `ops/instruments/`:**
```
6J.md
BTCUSD.md
EURGBP.md
GER40.md
MJY.md
NAS100.md
SPX500.md
US500.md
USDCAD.md
USOIL.md
XAUUSD.md
```

**Finding for HARV-0:** No instrument cards for ES/YM (or month-end calendar dead-lists). Closest equity-index neighbors: `SPX500.md`, `US500.md`, `NAS100.md`. No ES/YM durable findings to harvest from this tree.

**Verdict:** ABSENT

---

## 0.9 Envelope reconcile

**Source:** [`ENVELOPE_RECONCILE.md`](ENVELOPE_RECONCILE.md) (Track C)  
**Envelope path:** `ops/prop_envelope_default.md` (landed from companion; PROVISIONAL v0.1)

**Contradiction count: 5** (2 High):
1. **E1 clock print** — envelope 16:00 ET vs repo futures-prop MC/force-flat at **17:00 ET** (~16:59 rail comment). Intent (no overnight) aligns; deadline print does not.
2. **E3 trail geometry** — envelope = intraday unrealized; a major configured family is EOD-locking (`trailing_locking`) — overlay, not default.
3. E1 CFD fixture `weekend_holds: True` (fixture class mismatch; historical).
4. E3 Option-1 real-time intent vs possible EOD simulation semantic (medium).
5. E4 daily LL present-by-default vs all futures-prop fixtures `daily_loss_pct: None` (low / expected).

**Aligned:** E2 @ 40%, E5 micros, E6 attended (rail dormant under NO-GO), E7 overlay-only, E1 no-overnight *intent* on futures-prop fixtures.

**Verdict:** REPORTED (contradictions logged; no improvisation — envelope stays PROVISIONAL build target)

---

## 0.10 MECHANISM-NAMED-ENDOGENOUS — PATH REMAP

**Brief said:** `docs/methodology/inqhiori-canon.md` §Q-MECH-1 JPY standing  
**Actual path (register):** `docs/ltm/briefs/Q-MECH-1.JPY_h_register.md`

**`git log -1 --oneline -- docs/ltm/briefs/Q-MECH-1.JPY_h_register.md`:**
```
62e7dc0 q-mech-1.jpy-t(register): terminal standing — MECHANISM-NAMED (endogenous), EOM guard-band is the mechanism
```

**Wording (terminal standing, parent-adjudicated 2026-07-06):**
- Standing label: **MECHANISM-NAMED (endogenous)** — H-JPY-C reaches NAMED-WITH-MONITOR: mechanism = permitted-day dips (transient flow that reverts) vs boundary/excluded-day dips (persistent month-end benchmark/repatriation flow); counterparty = month-end benchmark executors; **monitorable leading variable = the month-end calendar**; discriminators surviving T1 EXCLUDED-LIKE.
- Family synthesis cell updated to **MECHANISM-NAMED-ENDOGENOUS**; family tally “0/4 **external** mechanism” unchanged (this close is endogenous).
- Consequence: month-end guard-band opens as a **separate overlay-class Pre-Q**; **no overlay/filter/sizing/parameter change flows from this close**.

**Finding for HARV-0:** HARV extends the month-end family forward (mechanism at t=0) to an equity-index leg. Claims in §4 must not re-label endogenous calendar mechanism as external counterparty mechanism; JPY standing constrains interpretation, not live sizing.

**Verdict:** PASS (with PATH REMAP noted)

---

## §0.5 Ambiguity list (do NOT resolve)

Per brief §0.5 halt-on-ambiguity — listed for operator; Track B does not default:

1. **Micro-era OOS exact wording** — §8 Integration (“native micro-era data / databento-data proxy gate” + full SPA/DSR/PBO ladder) vs HARV §4 **P-micro-OOS** (same-signed native-MES 2019-05→present). Which phrase is binding for §6(e)?
2. **Envelope 16:00 ET / 40% consistency** — flat-deadline print and consistency % pending Track C / read 0.9; do not invent defaults.
3. **CME holiday-calendar source of truth** — for trading-day offsets (T-2 / T-1 window construction); unspecified.
4. **ohlcv-1d close print** — settlement vs last trade; Phase-1 confirmation still owed before treating close as pre-deadline proxy.

---

## Track B closure note

Phase-0 Rule-0 reads **0.1–0.8 and 0.10 complete**. **0.9 deferred to Track C.** No NEEDS_CONTEXT on the databento-stack merge (0.2 PASS). Path remaps required in downstream audit hooks: `db_fetch.py` under `.claude/skills/databento-data/scripts/`; Q-MECH-1 standing under `docs/ltm/briefs/Q-MECH-1.JPY_h_register.md` (not inqhiori-canon). Brief remains **untracked** until an operator commit lands it on main.
