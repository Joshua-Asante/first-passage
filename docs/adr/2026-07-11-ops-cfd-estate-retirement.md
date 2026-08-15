# ADR 2026-07-11 — Retire the ops/ manual-CFD-execution estate

**Status:** `Accepted` — operator disposition approved 2026-07-11 (aggressive prune); executed on branch `claude/ops-retirement-plan-0d1741`. **Rescoped 2026-07-11 to estate-only** after main landed a *parallel* FXIFY retirement while this branch was open: the `accounts.py`/`cli.py` FXIFY surgery this ADR had planned as **PR-2 is subsumed** by [`fxify-ops-surface-retirement`](2026-07-11-fxify-ops-surface-retirement.md) (which excised that path AND deliberately *kept* `tearsheet` as generally-useful on historical CSVs — superseding this ADR's tearsheet-retire). This ADR now covers **only the manual-CFD-execution estate** — `live_journal/` (ECR/reconcile/counterfactual), `parity_check.py`, `regime_gate/`, `corpus_fdr/` — i.e. the reconcile-subsystem disposition that the fxify-ops-surface ADR explicitly *parked*.
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - multiplier-spine KEEP clause only (§2 KEEP rows for `ops/accounts.py` core + `ops/cli.py` add/update/status/lots). This is the §4 Trigger-B follow-on that ADR itself flagged rather than pre-decided. Estate deletions stand.
**Retain-until:** none
**Decision date:** 2026-07-11
**Authors:** Joshua + claude.ai (advisor)
**Related:** [`docs/adr/2026-07-11-fxify-ops-surface-retirement.md`](2026-07-11-fxify-ops-surface-retirement.md) (**parallel** FXIFY-challenge-surface retirement — did the `accounts.py`/`cli.py` excision this ADR's PR-2 planned, kept `tearsheet`, and *parked* the reconcile subsystem this ADR dispositions); [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](2026-07-11-challenge-era-claims-rescope.md) (re-scoped the challenge-era MC/claims to historical record — the CLAUDE.md/STATE.md context this branch merges with); [`docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md`](2026-06-30-no-manual-trading-cfd-retirement.md) (+ 2026-07-10 Addendum — the posture whose ops-layer consequence this ADR executes); [`docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md`](2026-07-10-r6-nogo-futures-residual-disposition.md) (futures-prop NO-GO — closes the re-arm path for the ECR/reconcile machinery); [`docs/ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md`](../ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md) (the immediate ops-retirement precedent — delete + git-history-retrieval convention)
**Layer:** infrastructure (ops-layer scope; **no `core/`, allocation, `dd_protection`, or Pine touch — no re-MC required**; locked anchor 99.83/0.17/4.37 untouched)

---

## §0 — Rule 0 reads (production-source verification)

All read in-worktree (`claude/ops-retirement-plan-0d1741`) **before** authoring, with cross-reference grep evidence per the SKILL.md cruft-classification sub-rule (report N callers before proposing a delete).

**Production source read (with anchors):**

- `ops/accounts.py` — anchor `2c09e12` (verified `git log -1` 2026-07-11). Full read. FXIFY logic has a clean seam: `FxifyChallengeStatus` (L48–84), `_phase_completed_at_from_dict` (L87–103), the FXIFY branch of `Account.flags` (L194–205), `evaluate_fxify_challenge_status` (L286–359), `fxify_status_summary` (L362–373), the FXIFY branch of `update_balance` (L518–526), and the FXIFY-only Account fields (`prior_eod_equity`/`last_trade_at`/`trading_days_count`/`phase_completed_at`, L121–128) are separable from the firm-agnostic multiplier core (`calc_multiplier` L376–397, `get_multipliers` L400–407, persistence L410–536).
- `ops/cli.py` — anchor `4441c72` (2026-07-11). Full read. FXIFY/DXTrade coupling isolated to: `cmd_challenge` (L128–152), `cmd_tearsheet` (L155–165), the FXIFY branches in `cmd_update` (L84–91) and `cmd_status` (L113–115), and the `challenge`/`tearsheet` subparsers (L249–274). `add`/`update`(core)/`status`(core)/`lots` survive intact.
- `ops/fxify_rule_validator.py` — anchor `4441c72` (2026-07-11). Callers: `ops/accounts.py` (lazy import L293), `ops/cli.py` (transitively via `accounts` functions), `tests/ops/test_fxify_rule_validator.py`, `tests/ops/test_fxify_challenge_integration.py`. **N=4, all inside the FXIFY-excision scope** — no caller survives the excision.
- `ops/live_journal/` (tree) — anchor `04fee2e` (2026-07-11). Cross-ref grep for importers **outside the subtree**: `scripts/run_ecr.py` + `scripts/preprocess_pine_ecr_logs.py` (real imports — both are thin ECR wrappers that retire *with* the estate), `core/csv_parser.py:11` (docstring **prose only**, names the ECR bridge to explain a layer boundary — not an import), `scripts/check_skill_refs.py:33,71` (navigation-allowlist *string*), `pyproject.toml:25` (the optional `pdf` extra exists *solely* for `dxtrade_pdf_to_csv`), Makefile `ecr`/`test-ops` targets. **No `core/` runtime importer** (verified `grep -rn "from live_journal" core/` → clean).
- **`ops/live_journal/references/execution_lessons.md`** (buried inside the estate) — **NOT execution machinery: a canonical, $-anchored lessons registry** ("the canonical anchor for behavioral lessons"; E1/E2 promoted on >$3K single-incident cost). Cited by **8 sites outside the estate**: `.claude/skills/brief-authoring/{SKILL.md,references/lesson_capture.md}`, `.claude/skills/live-execution-journal/SKILL.md`, `docs/adr/2026-06-04-lean-portfolio-meta-layer.md`, `docs/ltm/briefs/2026-07-06-ecr-double-count-backaudit.md`, `docs/methodology/lessons/methodology_lessons.md`, `docs/superpowers/{plans,specs}/2026-07-08-prop-firm-challenge-skill*`. The `.claude/skills/live-execution-journal/references/` copy has **diverged** from this one (`diff` → differ). A blind `git rm -r ops/live_journal/` destroys it → **must be extracted and KEPT** (§2), not swept with the estate.
- **Skill-layer coupling** — verified `grep -rln "live_journal|journal_review|ecr_rolling|fxify_rule_validator" .claude/skills/`: **only `.claude/skills/live-execution-journal/` matches** (SKILL.md + its stale `execution_lessons.md` copy). `prop-firm-challenge` and the repo `brief-authoring/SKILL.md` do **not** reference the retired code (the "edge-captured citation" sub-rule lives in the *global* brief-authoring cache, not the tracked repo copy — 0 matches). **`scripts/check_skill_refs.py:33,71` allowlists `live_journal/` *because* that skill points there** — so the allowlist entry is dropped in the same PR that retires the skill (never before), and no other skill edit is required.
- `ops/tv_mt5_pnl_reconciliation.py` — anchor `e3b03eb` (2026-06-06, untouched since the monorepo move). Sole caller: `tests/ops/test_tv_mt5_pnl_reconciliation.py`. **N=1 (test only)** — zero production consumer.
- `ops/parity_check.py` — anchor `e3b03eb` (2026-06-06). Sole caller: `tests/ops/test_parity_check.py`. **N=1 (test only).** The `parity_check` symbol imported across `lab/` is a **different** function (`validation.sweep.parity.parity_check`), not this module (confirmed by import-path grep). REPO_MAP §4 records that this file's former `parity_check.py:222` ops→lab edge was already dissolved when `tv_export_loader` moved to `core/`.
- `ops/regime_gate/README.md` + `ops/regime_gate/gold_gate_shadow.py` — anchor `5bc12d5` (2026-06-25). README header states **"⚠ 2026-07-01 — SHADOW GATE RETIRED (signal FALSIFIED out-of-sample)"**; shadow logging is already DISCONTINUED (gold KER/TSMOM signal inverted OOS twice — Q-REGIME-OOS-1, Q-REGIME-POSTCOVID-1), code + 2-row log "retained for record only." No code importer; doc references live only in point-in-time specs/notes (exempt).
- `ops/sentinel/scan.py` — anchor `6bcb034` (2026-07-02). Driven by `make sentinel`; Tier-1 deterministic commit-hygiene scan (Rule 8.7 freeze-before-results). Governance discipline, **not** execution — KEEP (verified live-wired).
- `core/lib/tearsheet.py` — anchor `dd4e4aa` (2026-06-06). Docstring: "HTML tearsheet generator for **DXTrade** trade history." Sole caller is `cli.py cmd_tearsheet`. Lives under **locked `core/`** → excluded from this ops pass (see §5).
- `ops/data/accounts.json` — **ABSENT on disk** (verified `test -f`). Zero registered accounts; the entire multiplier surface is currently dormant.
- `scripts/inactivity_simulator.py` — read head. **NOT CFD-execution estate** despite the "FXIFY" in its docstring: it is the Q-MCTO-1 Phase-1 reference implementation of the FXIFY-correct 60-bday MC timeout that `portfolio_mc.py` ports (the semantic behind the *locked* anchor). LEAVE ALONE (MC-anchor provenance, not live-ops).

**Precedent / convention reads:**

- [`docs/ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md`](../ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md) — the ops-retirement pattern this ADR follows. Confirms the repo convention since the 2026-06-05 monorepo prune: **delete + git-history retrieval** (`git show <pre-deletion-commit>:<path>`), no parallel `archive/` tree, and **REPO_MAP move-provenance rows are annotated-retired, not deleted**.
- `Makefile` (`ecr` L59, `sentinel` L65, `test-ops` L28–29 → currently `pytest ops/live_journal/tests/`) and `pyproject.toml:25` (`pdf` extra) — the tooling tail that must move with the estate.
- Test baseline: **684 tests collected** in the default suite (`pytest --co -q`; `pyproject.toml:41` pins `testpaths = ["tests"]`). **Correction (second pass):** the **126 `ops/live_journal/tests/` are OUTSIDE the 684** — they live under `ops/`, not `tests/`, so they run only via `make test-ops` and never enter the default suite. The 684's estate share is therefore just the `tests/ops/` tests (the five FXIFY/tearsheet/parity/tv_mt5 files = **113** + the ECR/counterfactual/schema facade tests + `tests/core/test_inactivity_boundary.py`) — order ~150. The 126 `live_journal` tests vanish as a separate suite. `tests/conftest.py` verified clean of estate imports (no shared-fixture break).

---

## §1 — Context

The 2026-07-10 operator batch ([`no-manual-trading-cfd-retirement`](2026-06-30-no-manual-trading-cfd-retirement.md) Addendum + [`r6-nogo`](2026-07-10-r6-nogo-futures-residual-disposition.md)) closed the world the ops layer was built for. Manual trading is retired; the FXIFY $200K DXTrade challenge is **formally closed** (credentials removed); the futures-prop pivot is **NO-GO** (no Bulenox account, no rail); and the sole surviving scale path is a **self-funded, automated Aegis→M6J** lane whose go-live is a separate gated decision. Yet `ops/` still carries the full manual-CFD-execution estate: the `live_journal/` reconcile/ECR/counterfactual subsystem (~30 files, ~4.5K LOC), the FXIFY challenge validator, TV↔MT5 and Pine↔TV parity reconcilers, an already-falsified shadow gold gate, and the FXIFY-specific half of the account CLI. **None of the fill-consuming tools has a live fill source** — the pre-registered ECR gate (Q-NAS-ECR-1) is PARKED-unreachable because the DXTrade fill it waited on can no longer occur, and Q-DECAY-1 confirmed ECR "needs live fills that no longer accrue." This is the ops-layer consequence of decisions already made; it is not a new strategy or risk-control choice.

The retirement discipline is inherited, not invented: the [weekly-review-feeder retirement](../ltm/briefs/2026-07-06-weekly-review-feeder-retirement.md) five days earlier established the exact pattern (an ops package whose only live data path was severed → delete + git-history retrieval, rebuild-repo-native-first if the need returns). This ADR applies that pattern at estate scale.

**Decision driver (one sentence):** the ops layer is ~85% machinery for a manual-CFD-execution world that three operator decisions have retired, with zero live data source and zero `core/` coupling — carrying it as live code misrepresents the operational posture and taxes every future reader, test run, and audit.

---

## §2 — Decision

**Decision:** Retire the `ops/` manual-CFD-execution estate under an **aggressive-prune** line — keep only what is load-bearing for the forward posture (the account-multiplier spine, governance/discipline tooling, and cited provenance), excise the FXIFY-specific machinery from the surviving CLI, and remove everything whose live data source is gone. Removal is **delete + git-history retrieval** (repo convention since the 2026-06-05 prune; no `archive/` tree). Execution is **staged across two PRs** so the delicate `accounts.py`/`cli.py` surgery is isolated from the zero-risk bulk removal.

**Effective:** on merge of each staged PR (§7). ADR flips `Proposed`→`Accepted` when PR-2 lands and the full suite is green.
**Scope:** the `ops/` layer + its `scripts/`-resident tooling tail (`run_ecr.py`, `preprocess_pine_ecr_logs.py`) + the Makefile/pyproject/allowlist references. **Explicitly out of scope:** any `core/` file (locked tier — see §5), `dd_protection.py`, `firm_rules.py` sizing, allocations, Pine, and the MC anchor.

### Disposition inventory

**KEEP — forward spine + governance:**

| Component | Reason |
|---|---|
| `ops/accounts.py` firm-agnostic core (`calc_multiplier`, `get_multipliers`, `Account` core fields, persistence) | The multiplier tool — the pipeline's stated purpose |
| `ops/cli.py`: `add` / `update` / `status` / `lots` | Core multiplier surface (post-FXIFY-excision) |
| `ops/sentinel/` | INQHIORI Tier-1 hygiene scan (`make sentinel`) — governance discipline, not execution |
| `ops/reports/regime_time_cost/RESULTS.md` → **relocated 2026-08-03** to `lab/analysis/regime/regime_time_cost_2026-06-09/RESULTS.md`; `ops/reports/` deleted | Load-bearing: cited by the Q-PERSIST-1 closure as evidence |
| `ops/instruments/` | Instrument-ledger registry (governance-ratified); dead-candidate ledgers **are** the rejected-candidate record |
| `ops/reference/regime_calendar.md`, `ops/data/reconciles/` · ~~`ops/data/audits/`~~ → **relocated 2026-08-03** to `docs/notes/audits/issue_54_ulp_audit.*` | Cheap markdown provenance — retiring records has no benefit (matches repo's keep-provenance pattern) |
| **`execution_lessons.md`** — **extract** from `ops/live_journal/references/` before the estate rm; relocate to `docs/methodology/lessons/execution_lessons.md` (alongside `methodology_lessons.md`), reconciling the diverged skill copy | Canonical $-anchored lessons registry cited by 8 external sites (§0); dies with a blind estate rm |

**RETIRE — the manual-CFD-execution estate (this ADR's scope; `git rm`, retrieval via `git show <pre-deletion-commit>:<path>`):**

| Component | Reason |
|---|---|
| `ops/live_journal/` — entire subtree (~30 files, ~4.5K LOC + 126 tests) **EXCEPT `references/execution_lessons.md`** (extracted → KEEP) | ECR/reconcile/counterfactual/DXTrade-PDF/zero-fills — **no live fill source** (Q-NAS-ECR-1 parked-unreachable; re-arm path closed by R6 NO-GO). **This is the reconcile subsystem the fxify-ops-surface ADR explicitly *parked*** ("out of scope for a controls prune"); this ADR is the disposition it deferred to. The `data/ingest_runs/*.md` historical logs go too (git history retains). |
| `ops/parity_check.py` (+ its test) | Zero production consumer (test-only); MT5/TV parity is a manual-execution-era concern. Main **kept** it (out of its FXIFY scope) — this ADR retires it. |
| `ops/regime_gate/gold_gate_shadow.py` + `README.md` + `ops/data/gold_gate_shadow_log.csv` | **Already retired 2026-07-01** (signal falsified OOS twice); README's falsification record folded into `docs/rejected_candidates.md`. |
| `ops/reports/corpus_fdr/` (3 JSON) | Orphaned research output, **no reader**; producer `scripts/run_corpus_fdr.py` itself retired 2026-07-11 (Gen-1). |
| `scripts/run_ecr.py`, `scripts/preprocess_pine_ecr_logs.py` | Thin ECR wrappers — retire with the engine. |
| `ops/reports/ecr/`, `ops/mc_runs/` (empty `.gitkeep` dirs) | Orphaned producer-output scaffolds. |
| Tooling tail: Makefile `ecr` target + re-point `test-ops`→`tests/ops/`; `pyproject` `pdf` extra; `check_skill_refs` `live_journal/` allowlist (L33/L71); `.claude/skills/live-execution-journal/` | Reference cleanup so the retirement is grep-clean. **This branch uniquely retires the skill** — main kept it (verified `git ls-tree origin/main` = 2 files); my deletion carries cleanly through the merge. |

**DONE BY THE PARALLEL `fxify-ops-surface-retirement` ADR (not this one — recorded so the two ADRs reconcile):** `ops/fxify_rule_validator.py`, `ops/tv_mt5_pnl_reconciliation.py`, and the `accounts.py`/`cli.py` FXIFY-challenge path (`FxifyChallengeStatus`, `evaluate_fxify_challenge_status`, `cmd_challenge`, the four FXIFY-only fields) were retired there (PRs #320/#323) while this branch was open. **`cmd_tearsheet` was deliberately KEPT** by that ADR ("generally useful on historical CSVs") — this ADR's earlier tearsheet-retire is **superseded**. This ADR does **not** touch `accounts.py`/`cli.py` at all.

**LEAVE ALONE (adjacent, not the estate):** `scripts/inactivity_simulator.py` (MC-anchor timeout reference impl), `scripts/lock_event_hook.py` (governance hook), and `ops/accounts.py`/`ops/cli.py` (owned by the fxify-ops-surface ADR — already FXIFY-excised on main; untouched here). **`core/csv_parser.py` and `core/lib/tearsheet.py` both stay** — locked-`core/` tier and both live: `csv_parser` feeds `validate_params` (a KEPT gate), and `tearsheet.py` backs the `tearsheet` command main deliberately kept. Neither is an orphan; neither is touched.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Conservative / reactivatable** — keep ECR engine + `fxify_rule_validator` as templates for a future automated-fill or new-firm world; gitignore/park rather than delete | Rejected by the operator (retention-line decision, this session). Substantively: the re-arm paths are *closed*, not merely dormant — R6 NO-GO means no prop book, and any future fill stream is a *different venue microstructure* (futures MNQ/M6J, not DXTrade CFD) that Q-NAS-ECR-1's own dormancy flag says is **not type-preserving** ("re-pointing needs a fresh Pre-Q"). Keeping DXTrade-shaped code as a "template" preserves the wrong shape. |
| **Big-bang single PR** — one commit does estate removal + accounts/cli surgery + tail | Matches the 2026-07-10 batch style and is faster, but co-mingles a zero-risk mechanical bulk delete (nothing live depends on it) with the one genuinely delicate change (surgical FXIFY excision from a KEPT module). Isolating the surgery in its own PR buys an independent review + full-suite gate for the only step that can regress the surviving spine. |
| **Plan-only, execute later** — author this ADR, land no code | The disposition is already grounded (§0 cross-refs complete, `core/` confirmed clean); deferring execution leaves 250+ dead tests and a misleading surface in place for no benefit. The ADR + staged PRs *is* the plan-then-execute. |
| **Status quo — leave the estate as live code** | The estate silently misrepresents posture (a reader sees a live execution-journal subsystem for trading that no longer happens), taxes every `make test`/audit/grep, and grows the exact class of frozen-surface cruft the weekly-review-feeder retirement just removed. No offsetting benefit once the fill source is gone. |
| **Also retire the multiplier spine** (accounts.py/cli.py entirely) | Genuinely on the table — the spine is dormant (no accounts) and was built for CFD/prop-challenge sizing, while M6J sizes in native micro-contracts. But retiring the repo's **stated core purpose** is a distinct structural decision that turns on the M6J go-live sizing design (unresolved), not on CFD retirement. Deferred to the §4 strategic-flag falsifier, not folded in here. |

---

## §4 — Falsifier (revert trigger)

Two independent triggers; either firing revisits a specific part of this decision.

**Trigger A — a live fill source re-emerges (estate premature).** If, before the **2026-08-08** quarterly review, a live fill stream begins accruing (self-funded M6J go-live, or any leg going live on any venue) **AND** an edge-capture (ECR) or broker↔TV reconciliation need re-emerges, then retiring `live_journal/` was premature. **Revert action:** per the weekly-review-feeder add-back order, **rebuild repo-native against the *actual* venue microstructure FIRST** (the retired code is design reference via `git show`, not a drop-in restore) — do **not** `git revert` the DXTrade-coupled design (§5). Binary check: `git log --since=2026-07-11 -- <new fill-ingest path>` non-empty AND an open Pre-Q naming the reconciliation need.

**Trigger B — M6J go-live resolves the multiplier-spine question.** When the Aegis→M6J go-live design is settled: **if** it sizes via Pine-indicator-lot × account-multiplier, the KEEP decision for the spine is confirmed correct and this trigger closes; **if** it sizes natively in integer micro-contracts and no other account/firm is onboarded, open a **follow-on ADR** to evaluate retiring the multiplier spine too (the prune was correct but incomplete). This ADR does **not** pre-decide that — it flags it.

**Trigger check schedule:** ride the **2026-08-08** quarterly regime check (already on the STATE.md forward board); no separate calendar item.

---

## §5 — Forbidden moves (under this ADR)

- **`git revert`-ing the DXTrade-coupled `live_journal` design unchanged if a fill source returns.** The DXTrade fill microstructure this code models does not transfer to the futures venue (Q-NAS-ECR-1 dormancy flag: re-point is not type-preserving). Rebuild repo-native against the real venue first — restoring the old shape re-imports the wrong assumptions (direct analog of the weekly-review-feeder §5).
- **`git rm`-ing `execution_lessons.md` with the estate.** It is a canonical $-anchored lessons registry cited by 8 external sites, not execution machinery — it must be extracted to `docs/methodology/lessons/` first (§2 KEEP). A blind `git rm -r ops/live_journal/` that takes it down is the single highest-loss error in this ADR.
- **Touching any `core/` file in this ops pass** — `core/lib/tearsheet.py` becomes *orphaned* once `cmd_tearsheet` goes, but `core/` is the locked, imports-nothing-internal tier; its disposition is a **separate follow-on**, never a side effect of an ops cleanup. (`core/csv_parser.py` is **not** orphaned — `validate_params.py` uses it — so it is not even a follow-on candidate; leave it.) Leaving a dead-but-locked orphan is acceptable; reaching into `core/` here is not.
- **Deleting REPO_MAP.md move-provenance rows instead of annotating them retired.** The 2026-06-05 moves genuinely happened; annotate-retired (matching the weekly-review-feeder and validation/codification rows), do not erase history.
- **Retiring the multiplier spine as a side effect of this cleanup.** That is the §4 Trigger-B decision, gated on M6J sizing design and operator GO — not something to fold into a CFD-estate prune because the spine "looks dormant too."
- **Half-excising FXIFY** (e.g., loosening `evaluate_fxify_challenge_status` to a stub, or leaving `fxify_rule_validator.py` importable "just in case"). The FXIFY path and its validator retire *together* as one clean seam; a stub is a frozen-surface remnant, the exact thing this prune removes.
- **Retiring `sentinel/`, `reports/regime_time_cost/RESULTS.md`, or the `instruments/` registry.** Surface-similar to the estate but load-bearing (live governance / cited evidence / ratified registry) — KEEP is explicit, not incidental.

---

## §6 — Consequences

**Positive:**
- `ops/` shrinks to ~15% of its current footprint; the surviving surface (multiplier spine + `sentinel` + provenance) matches the actual posture, so a reader/auditor sees what is live.
- ~250+ tests for retired code removed — faster `make test`, smaller audit surface, no test-enshrined DXTrade fixtures pinning dead behavior.
- Closes the standing "is this live?" ambiguity around `live_journal/`, the FXIFY validator, and the already-falsified gold gate in one recorded decision.
- Grep-clean retirement (Makefile/pyproject/allowlist tail included), so no dangling references accrete as noise.

**Negative (real cost):**
- In-tree ECR/reconcile machinery is gone if a fill source returns — mitigated by full git recoverability + the §4 rebuild-repo-native path (and the retired code was DXTrade-shaped, i.e., the *wrong* shape for the futures venue anyway).
- Loses `fxify_rule_validator` as a ready-made firm-onboarding template — mitigated: futures-prop is NO-GO, and any genuinely new firm gets a fresh validator against *its* rules, not FXIFY's.
- The `WIRING`/README design notes in `live_journal/` + `regime_gate/` leave the live tree — preserved in git history and (for the gold gate's falsification finding) folded into `docs/rejected_candidates.md`.

**Risks (probabilistic, distinct from costs):**
- The only code-regression risk is the `accounts.py`/`cli.py` FXIFY surgery on a KEPT module — contained by isolating it in PR-2 with its own review and a full-suite gate. `core/` is confirmed clean of retire-target imports, so the bulk removal (PR-1) carries no import-break risk.

**Downstream artifacts to update (across the two PRs):**
- `CLAUDE.md` — Architecture ops-module list (drop `live_journal fxify_rule_validator parity_check tv_mt5_pnl_reconciliation`; note the multiplier-tool-only ops surface) + a retirement pointer to this ADR.
- `REPO_MAP.md` — `ops/` §1 rows + `scripts/` §2.1 ops list: annotate the retired entries (do not delete).
- `STATE.md` — forward board: note the estate retirement; fold the Q-NAS-ECR-1 "engine: `ecr_rolling.py`" pointer into "engine retired 2026-07-11, rebuild-repo-native per ADR §4."
- `Makefile` — remove `ecr`; re-point `test-ops` to `tests/ops/`.
- `pyproject.toml` — remove the `pdf` optional extra (L25).
- **Skill layer (`.claude/`, governance — second-pass addition):** **retire** `.claude/skills/live-execution-journal/` in full (its DXTrade-pipeline premise is moot post-no-manual-trading, and it is the *only* skill referencing the retired code). Relocate the canonical `execution_lessons.md` → `docs/methodology/lessons/` and fix the one live cross-ref link (`methodology_lessons.md:4`; the `2026-06-04` ADR + `2026-07-06` brief line-number citations are point-in-time-exempt). No `prop-firm-challenge` or `brief-authoring` edit needed (verified no retired-code refs). Run `make skills-check` after.
- `scripts/check_skill_refs.py` — drop `live_journal/` from the navigation allowlist (L33 comment + L71) **only after** the skill refs above are retired/re-pointed (else `make skills-check` fails on a live ref to a now-un-allowlisted path). Ordering matters.
- `docs/rejected_candidates.md` — absorb the gold-gate OOS-falsification record from `regime_gate/README.md` before its `git rm`.
- `docs/SESSIONS.md` — new entry per PR.

---

## §7 — Implementation plan (single PR — PR-2 subsumed by main)

**Phase 0:** re-verify §0 anchors current (`git log -1` on each target still matches; `core/` still clean); capture the pre-removal `pytest -q` baseline count; confirm no removed test file provides a fixture consumed by a KEPT test (`tests/conftest.py` verified clean of estate imports).

**The estate-retirement PR (executed on `claude/ops-retirement-plan-0d1741`, commit `67e0ef7`; then reconciled with main via merge — see the reconciliation step):**
1. **Extract-before-delete (do this FIRST):** `git mv ops/live_journal/references/execution_lessons.md docs/methodology/lessons/execution_lessons.md`, reconcile the diverged `.claude/skills/live-execution-journal/references/` copy, and re-point the 8 citing sites (§0). Absorb the gold-gate OOS record from `ops/regime_gate/README.md` into `docs/rejected_candidates.md`.
2. `git rm -r ops/live_journal/` (now lessons-free); `git rm ops/tv_mt5_pnl_reconciliation.py ops/parity_check.py ops/regime_gate/gold_gate_shadow.py ops/regime_gate/README.md ops/data/gold_gate_shadow_log.csv`; remove the emptied `ops/regime_gate/`, `ops/reports/ecr/`, `ops/mc_runs/`; `git rm -r ops/reports/corpus_fdr/`.
3. `git rm scripts/run_ecr.py scripts/preprocess_pine_ecr_logs.py`; remove estate tests `tests/ops/test_tv_mt5_pnl_reconciliation.py test_parity_check.py test_ecr_* test_counterfactual_schema test_schema test_journal_review_facade`.
4. **Skill layer (governance):** `git rm -r .claude/skills/live-execution-journal/` (the sole skill referencing retired code). **Only then** drop `live_journal/` from `check_skill_refs.py` (L33/L71). Run `make skills-check`. (No `prop-firm-challenge`/`brief-authoring` edit — verified no refs.)
5. Tooling tail + docs: Makefile (`ecr` out, `test-ops`→`tests/ops/`), `pyproject.toml` (`pdf` extra out), and the annotate-retired doc edits in CLAUDE.md/REPO_MAP.md (§1 ops rows + §2.1 scripts list)/STATE.md.
6. Verification: `pytest -q` green (default suite drops only its ~150 `tests/ops/` estate tests); `make skills-check` + `python scripts/check_boundaries.py` + `make validate` pass; §10 grep hooks clean.

**Reconciliation step (post-commit, this branch):** merge `origin/main` (which advanced ~20 commits while the branch was open, including the parallel FXIFY retirement). All estate deletions are UNCHANGED-on-main → clean; the only conflicts are CLAUDE.md + REPO_MAP.md ops rows, resolved to carry **both** retirements. Re-run the full gate on the merged tree.

**PR-2 — SUBSUMED (no action).** The `accounts.py`/`cli.py` FXIFY excision + `fxify_rule_validator.py` removal this ADR had planned as a second PR were **done by the parallel [`fxify-ops-surface-retirement`](2026-07-11-fxify-ops-surface-retirement.md)** (PRs #320/#323) while this branch was open; `cmd_tearsheet` was deliberately **kept** there. Nothing remains to excise — this ADR ships as a single PR and moves to `Accepted` on merge.

---

## §10 — Audit hooks (runnable)

```bash
# Estate is gone (PR-1)
for p in ops/live_journal ops/tv_mt5_pnl_reconciliation.py ops/parity_check.py \
         ops/regime_gate/gold_gate_shadow.py scripts/run_ecr.py scripts/preprocess_pine_ecr_logs.py; do
  test -e "$p" && echo "STILL PRESENT: $p" || echo "OK retired: $p"
done

# FXIFY validator gone + no live-code references (PR-2); ADRs/specs/notes are point-in-time, exempt
test -e ops/fxify_rule_validator.py && echo "STILL PRESENT" || echo "OK retired"
grep -rln "fxify_rule_validator\|live_journal\|tv_mt5_pnl_reconciliation" --include="*.py" ops/ core/ scripts/ 2>/dev/null
# Expected: empty

# Surviving spine still works against an empty/absent store
python ops/cli.py lots   ; # Expected: "No active accounts." (no traceback)
python ops/cli.py status ; # Expected: "No accounts registered."

# KEEP items untouched
test -f lab/analysis/regime/regime_time_cost_2026-06-09/RESULTS.md && test -d ops/sentinel && echo "OK keeps present"
make sentinel >/dev/null 2>&1 && echo "OK sentinel runs"

# Tooling tail clean
grep -nE "^ecr:|live_journal" Makefile ; grep -n "pdf =" pyproject.toml ; grep -n "live_journal" scripts/check_skill_refs.py
# Expected: no `ecr:` target, no live_journal in Makefile/allowlist, no `pdf` extra

# Retirement pointer present + locked layers untouched
grep -n "2026-07-11-ops-cfd-estate-retirement" CLAUDE.md REPO_MAP.md STATE.md
git diff --name-only origin/main -- core/ 'core/**/*.pine'
# Expected: pointer hits; second grep EMPTY (no locked-layer touch — my branch's core/ == main's)

# Lessons registry preserved (NOT lost with the estate)
test -f docs/methodology/lessons/execution_lessons.md && echo "OK lessons kept" || echo "LOST — abort"
test -e ops/live_journal/references/execution_lessons.md && echo "STILL in estate (extract first)" || echo "OK extracted"

# Skill-ref gate green (the allowlist drop must not outrun the skill-ref retirement)
make skills-check
# Expected: PASS — no live skill ref to a removed live_journal/ path

# Full suite green (run at each PR). NOTE: the 126 ops/live_journal/tests/ are NOT in
# testpaths=["tests"], so they never counted toward 684 — the default suite drops only
# its ~150 tests/ops/ estate tests. Both the count-drop AND all-green are required.
python -m pytest -q

# §4 calendar trigger
# Quarterly regime check / M6J-sizing resolution due: 2026-08-08
```

---

## Verification

```bash
# Discipline checks (mechanical)
$ python "C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py" docs/adr/2026-07-11-ops-cfd-estate-retirement.md --type adr
# Expected: all 6 checks PASS

# Production-source verification (Rule 0 confirmation)
$ for f in ops/accounts.py ops/cli.py ops/fxify_rule_validator.py ops/tv_mt5_pnl_reconciliation.py \
           ops/parity_check.py ops/regime_gate/gold_gate_shadow.py; do git log -1 --format='%h %ci' -- "$f"; done
$ grep -rn "from live_journal\|import fxify_rule_validator\|import parity_check\|import tv_mt5_pnl_reconciliation" --include=*.py core/
# Expected: anchors match §0; core/ grep EMPTY

# Cross-reference verification (test baseline + absent store)
$ python -m pytest --co -q | tail -1              # Expected: 684 collected
$ test -f ops/data/accounts.json || echo "store absent (dormant surface)"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial authoring — disposition approved (aggressive prune), execution staged PR-1/PR-2 | Joshua + claude.ai |
| 2026-07-11 | Second-pass corrections (pre-acceptance, same session): (1) extract `execution_lessons.md` to KEEP — a blind estate rm destroyed a cited $-anchored registry; (2) added the skill-layer workstream + `check_skill_refs` ordering; (3) fixed the test-count claim (126 `live_journal` tests are outside `testpaths`); (4) `csv_parser` is not orphaned (validate_params uses it) — only `tearsheet` is; (5) `corpus_fdr` retire not relocate; + FXIFY-key / `dd_type` restraint notes | Joshua + claude.ai |
| 2026-07-11 | **Merge reconciliation → `Accepted`.** Main landed a *parallel* FXIFY retirement while this branch was open ([`fxify-ops-surface-retirement`](2026-07-11-fxify-ops-surface-retirement.md) PRs #320/#323 + [`challenge-era-claims-rescope`](2026-07-11-challenge-era-claims-rescope.md) PR #324). **Rescoped this ADR to estate-only:** PR-2 (accounts/cli FXIFY surgery) is **subsumed** by that ADR, which also **kept `tearsheet`** — superseding this ADR's tearsheet-retire. Merged `origin/main` (2 doc conflicts resolved: CLAUDE.md + REPO_MAP.md carry both retirements). Single-PR now; `Accepted` on merge. | Joshua + claude.ai |
| 2026-07-11 | **`core/` follow-on (the §5 "separate follow-on" this ops pass deferred).** Retired the orphaned `account_aliases` scaffold — `core/config/account_aliases.README.md` + `core/config/account_aliases.example.json`. Rationale: its sole consumer was `live_journal/signals/schema.py` (defined `ACCOUNT_ALIAS_MAP_PATH`), `git rm`'d with the estate here; no live reader remains (grep-verified — only historical briefs cite it), and the DXTrade-shaped `FXIFY-A1` scaffold is the wrong shape for any future venue (§3 rejected "keep DXTrade-shaped code as a template"). It is a limb of the *retired estate*, not the KEPT multiplier spine (which persists via `ops/data/accounts.json`, a separate mechanism). Resolves the "keep/remove" flag open on the README since 2026-06-25. Delete + git-history retrieval per repo convention. The sibling stale comments in `core/csv_parser.py` (which stays — `validate_params`/`tearsheet` consume it) were trimmed in the same pass. | Joshua + claude |
| 2026-08-03 | **`ops/reports/` deleted.** Sole remaining KEEP (`regime_time_cost/RESULTS.md`) relocated beside its harness at `lab/analysis/regime/regime_time_cost_2026-06-09/RESULTS.md`. Q-PERSIST-1 closure citation + REPO_MAP §1 updated; LTM historical citations left as audit trail. | Joshua + Cursor |
| 2026-08-03 | **`ops/data/audits/` deleted.** Sole contents (`issue_54_ulp_audit.{json,md}`) relocated to `docs/notes/audits/`. PIPELINES / REPO_MAP / fxify-ops ADR pointers updated. | Joshua + Cursor |
