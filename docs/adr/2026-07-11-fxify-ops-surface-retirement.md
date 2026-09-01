# ADR 2026-07-11 — FXIFY/DXTrade-era ops surface: retire the untangled dead controls, park the reference scaffold

**Status:** `Accepted` — **operator STRATEGIC-LoR ratification recorded 2026-07-11 (Joshua): FXIFY is retired whether or not Tradeify is locked — see the §2 disposition override.** **Executed 2026-07-11** on branch `claude/fxify-ops-retirement-90703d` (`git rm` of validator/TV-MT5/zero-fills + `accounts.py`/`cli.py` FXIFY-path excision). Retiring ops machinery coupled to the account model is a subsystem-tier Delete (three-loop binding ADR reserves it to STRATEGIC-LoR).
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-22-challenge-era-substrate-retirement.md` - accounts.py/cli.py KEEP row only (Phase 2, merged 2026-07-24, PR #485); `2026-07-11-ops-cfd-estate-retirement.md` - dxtrade_pdf_to_csv.py PARK row only.
**Retain-until:** none
**Decision date:** 2026-07-11
**Authors:** Joshua (decision) + claude.ai advisor (drafting) + Claude Code (execution)
**Supersedes:** none. Dispositions the ops surface left dormant by `docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md` (FXIFY $200K DXTrade formally CLOSED, 2026-07-10 addendum) and `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (R6 = NO-GO — no prop rail).
**Related:** `docs/adr/2026-07-11-gen1-pipeline-retirement.md` (the format + the **park-don't-delete precedent** — `codification` parked because the future live path needs its shape; this ADR reuses that logic for the firm-rule scaffold); the firm-constants single-source ADR (FXIFY constants consolidated into `core/firm_rules.py`/`portfolio_mc.py`/`dd_protection.py` — the reason those are anchor-bearing and OUT of scope); the surviving Aegis→M6J self-funded lane + the active Tradeify prop-firm exploration (`lab/analysis/tradeify_*_remc_*`).
**Layer:** ops tooling only. **Not** locked core: no `core/firm_rules.py` FXIFY constants, no `core/dd_protection.py`, no `core/portfolio_mc.py`, no MC anchor (99.83/0.17/4.37). The CFD portfolio was FXIFY-validated, so those core constants are anchor-bearing evidence — untouched.

---

## §0 — Rule 0 reads (production-source verification)

Content-read via the Windows filesystem on 2026-07-11 (this authoring session); the reverse-dependency audit was executed, not deferred. Ratification still requires re-confirming against the merge-base commit.

- `ops/accounts.py` — a **firm-agnostic** account + persistence + sizing scaffold (`Account` L107, `load/save/get/add_account`, `calc_multiplier`/`get_multipliers`) with an FXIFY-specific evaluation path **woven in**: `FxifyChallengeStatus` (L49), `evaluate_fxify_challenge_status` (L286 → `from fxify_rule_validator import …`), `fxify_status_summary` (L362), and `if firm == "FXIFY"` branches inside `flags()` (L192) and `update_balance()` (L484). The FXIFY logic is not a separable file — it is interleaved with the general model.
- `ops/fxify_rule_validator.py` — standalone FXIFY 3-Phase validators (daily-loss / max-static-DD / inactivity limit checks; profit-target / min-trading-days completion checks). **Constants sourced from `firm_rules.FIRM_RULES["FXIFY"]`** — the validator is the ops *consumer* of the locked core constants, not their owner. The limit/completion + boundary-inclusive structure is firm-shaped, not FXIFY-unique.
- Reverse-dependency (live callers): `ops/cli.py` imports `accounts` (L25) and exposes FXIFY validator detail (L129/L252); `dxtrade_pdf_to_csv` is **imported by the reconcile pipeline** (`ops/live_journal/reconcile/__main__.py` L18, referenced by `replication.py`/`tv_log.py`); `zero_fills_attestation` has **no code importer** (only `no_manual_attestation_log.md` + its own test); `tv_mt5_pnl_reconciliation` has **no code importer** (standalone script + its own test).
- Locked-core FXIFY presence (scope-out check): `core/firm_rules.py` (5 hits) + `core/dd_protection.py` (2 hits) — anchor-bearing; the retirement touches the ops consumer, never these.
- Tests on the surface: `tests/ops/test_accounts.py`, `tests/ops/test_fxify_challenge_integration.py`, `tests/ops/test_fxify_rule_validator.py`, `tests/ops/test_tv_mt5_pnl_reconciliation.py`, `ops/live_journal/tests/test_dxtrade_pdf_to_csv.py`, `ops/live_journal/tests/test_zero_fills_attestation.py` (+ general `accounts`/`dxtrade` references in `tests/core/test_atomic_io.py`, `tests/core/test_csv_parser.py`).

---

## §1 — Context

FXIFY $200K DXTrade is formally CLOSED and manual trading retired (2026-06-30 ADR addendum, 2026-07-10); R6 = NO-GO, so there is no prop rail. The FXIFY/DXTrade ops surface therefore has **no live producer**. But the reverse-dependency audit (§0) shows it is **not free-floating dead code** — it is a coupled cluster: `accounts.py` (firm-agnostic scaffold with FXIFY interleaved) ↔ `fxify_rule_validator.py` (the firm-rule-evaluator template) ↔ `cli.py`; and `dxtrade_pdf_to_csv.py` ↔ the reconcile pipeline.

The surviving scale path (Aegis→M6J) is *self-funded* and carries no prop-challenge semantics, so on that path the challenge machinery is dead. **But the operation is actively exploring Tradeify** (a futures prop firm — the `tradeify_*_remc` investigations), and any prop-firm rail (Tradeify, or R6 flipping GO) needs exactly this shape: an account-challenge model, a firm-rule validator (adapted to the new firm's constants), and statement reconciliation. So most of this surface is a dormant **reference scaffold**, not dead weight — the identical situation to `codification` in the Gen-1 retirement, which was parked (not deleted) because the future live path needs its shape.

**Decision driver (one sentence):** retire only the genuinely dead-and-untangled controls (no producer, no importer, no template value); PARK the entangled reference scaffold behind a prop-rail re-point trigger, rather than strand the machinery the active Tradeify exploration would otherwise rebuild from scratch.

---

## §2 — Decision (proposed)

**Operator ratification (2026-07-11) — disposition override.** The operator ratified retirement and resolved §7 Phase-0c: **FXIFY is retired whether or not Tradeify is locked.** This overrides the PARK recommendation for the FXIFY-specific scaffold — the rows for `fxify_rule_validator.py` (+ its tests) and the `accounts.py` FXIFY path change **PARK → RETIRE**: a future prop firm's validator will be built fresh against that firm's rules rather than adapted from FXIFY's, so the weak template value does not outweigh the standing maintenance/test surface. Two things do **not** change: `dxtrade_pdf_to_csv.py` stays **PARKED** (coupled to the live-journal reconcile pipeline — a separate, larger disposition, not the FXIFY-challenge surface), and the locked `FIRM_RULES["FXIFY"]` constants in `core/firm_rules.py` stay (anchor-bearing; the retirement is ops-consumer-only). Execution: [`CC handoff — FXIFY-ops retirement`](docs/ltm/briefs/rnd-pipeline/2026-07-11-cc-handoff-fxify-ops-retirement.md). The original per-file analysis is retained below — it records why PARK was proposed and why the operator chose otherwise.

Per-file disposition (original recommendation; the override above changes the two FXIFY-scaffold rows PARK → RETIRE):

| Subsystem | Disposition | Why | Blocking-first |
|---|---|---|---|
| `ops/live_journal/scripts/zero_fills_attestation.py` + `ops/live_journal/tests/test_zero_fills_attestation.py` | **RETIRE** | Weekly no-manual attestation for the *manual-trading* era; **never ran** (STATE.md 2026-07-10); no code importer (a data note + its test only); **no template value** — future execution is automated, so no manual-idle attestation is ever needed again. | confirm the `no_manual_attestation_log.md` reference is a historical record, not a live hook (it is). |
| `ops/tv_mt5_pnl_reconciliation.py` + `tests/ops/test_tv_mt5_pnl_reconciliation.py` | **RETIRE** | CFD-era TradingView↔MT5 P&L reconciliation; standalone; no code importer; the futures path has **no MT5 leg** (TV→CrossTrade→NT8/Rithmic). | Phase-0b: re-confirm zero importers (grep shows none) before `rm`. |
| `ops/fxify_rule_validator.py` + `tests/ops/test_fxify_rule_validator.py` + `tests/ops/test_fxify_challenge_integration.py` | **PARK — do NOT delete** | The firm-rule-evaluator **template**. FXIFY's constants/URLs are dead, but the validator *structure* (limit/completion checks, boundary-inclusive semantics, `firm_rules`-sourced constants) is exactly what a Tradeify/next-firm validator adapts. Import-clean already. | re-point/retire trigger = a prop-rail decision (Tradeify verdict / R6 flip). |
| FXIFY path **inside** `ops/accounts.py` (`FxifyChallengeStatus`, `evaluate_fxify_challenge_status`, `fxify_status_summary`, the `firm=="FXIFY"` branches) + the FXIFY cases in `tests/ops/test_accounts.py` | **PARK** | Interleaved with the firm-agnostic `Account` model that `cli.py` and the (pending) sizing surface keep. Excising it now is premature surgery on the model the next prop firm reuses. | excise only under a future full-retire ADR at the trigger. |
| `ops/live_journal/scripts/dxtrade_pdf_to_csv.py` + `ops/live_journal/tests/test_dxtrade_pdf_to_csv.py` | **PARK (entangled)** | Still imported by the reconcile pipeline (`reconcile/__main__.py`, `replication.py`, `tv_log.py`). DXTrade statements no longer arrive, but retiring the parser requires **first** dispositioning the reconcile subsystem — out of scope for a controls prune. | retire only alongside a reconcile-pipeline disposition. |
| `ops/accounts.py` general machinery, `ops/cli.py`, the reconcile framework | **KEEP** | Firm-agnostic account/sizing/reconciliation scaffold; not FXIFY-specific. | — |

**Explicitly NOT retired / touched:** `core/firm_rules.py` FXIFY constants, `core/dd_protection.py`, `core/portfolio_mc.py`, the MC anchor (anchor-bearing evidence); any `docs/` FXIFY audit/closure (`docs/notes/audits/issue_54_ulp_audit.*` — relocated from `ops/data/audits/` 2026-08-03, `no_manual_attestation_log.md`) — evidence, annotate-never-delete.

**Effective:** on the ratification commit, and only after §7 Phase 0 passes. **Scope:** the two RETIRE rows + REPO_MAP/STATE provenance edits. No `core/`, no Pine, no locked constant, no accounts.py excision.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| **Full wholesale retire** (delete every FXIFY/DXTrade ops file + excise `accounts.py`) | Strands the firm-rule-evaluator template + the account-challenge model the active Tradeify exploration (and any prop rail) would rebuild from scratch — the exact stranding the Gen-1 ADR avoided by parking `codification`. The `accounts.py` excise is surgical (FXIFY woven through `flags()`/`update_balance()`) — a real cost for a scaffold you may re-point within weeks. Also entangles the reconcile pipeline (via `dxtrade_pdf_to_csv`). |
| **Status quo — keep everything, mark nothing** | Leaves `zero_fills` + `tv_mt5` as standing maintenance/test surface with no producer, no importer, no template value — the Gen-1 "dead weight" argument applies to exactly those two. |
| **Park everything, retire nothing** | `zero_fills` + `tv_mt5` have no template value and no importer; parking them is ceremony. The repo precedent (dukascopy/oanda/notion/Gen-1) is clean removal with provenance for genuinely dead machinery. |
| **Retire `fxify_rule_validator`, keep only `accounts.py`** | Breaks `accounts.py`'s FXIFY path (a live import) and forces the excise now — the premature surgery this ADR defers. |
| **Retire `dxtrade_pdf_to_csv` too** | It is imported by the reconcile pipeline; deleting it breaks `reconcile/__main__.py` + `replication.py`. Its retirement belongs to a reconcile-pipeline disposition, not a controls prune. |

---

## §4 — Falsifier (revert trigger)

**H:** Retiring the two untangled dead controls (`zero_fills_attestation`, `tv_mt5_pnl_reconciliation`) loses nothing the operation needs, and parking the entangled scaffold (`fxify_rule_validator`, the `accounts.py` FXIFY path, `dxtrade_pdf_to_csv`) preserves its template value for the prop-rail path.

**Falsifier** — git preserves every retired byte, so revert is cheap and the bar to fire is low. The retirement is *falsified* if:
- **Retire-was-wrong:** if within two quarterly cycles a live-ops need for `zero_fills` (manual-idle attestation) or `tv_mt5` (TV↔MT5 reconciliation) returns → restore from history and amend.
- **Park-should-have-been-retire:** if the prop-rail path is definitively abandoned (Tradeify dead AND R6 stays NO-GO AND self-funded-only confirmed) → the scaffold's template value is void; open a follow-on to retire `fxify_rule_validator` + excise the `accounts.py` FXIFY path.
- **Park-should-have-been-rebuild** (codification-mirror): if at the re-point trigger the parked validator cannot be adapted to the new firm's constants → the PARK verdict was wrong; open a rebuild ADR.

**Trigger check schedule:** rides the standing quarterly review (2026-08-08 → 2026-11-08); the prop-rail disposition (Tradeify) is the near-term gate.

---

## §5 — Forbidden moves (under this ADR)

- **Touching `core/firm_rules.py` FXIFY constants, `core/dd_protection.py`, `core/portfolio_mc.py`, or the MC anchor.** Anchor-bearing, out of scope; a diff touching them is an integrity failure of this change.
- **Excising `accounts.py`'s FXIFY path.** That is the parked scaffold; excise only under a future full-retire ADR at the re-point trigger — not here.
- **Retiring `dxtrade_pdf_to_csv` without first dispositioning the reconcile pipeline** that imports it — build-breaking.
- **Deleting FXIFY evidence** (`docs/notes/audits/issue_54_ulp_audit.*` — was `ops/data/audits/` until 2026-08-03, `no_manual_attestation_log.md` as a record) — annotate-never-delete.
- **Ratifying without operator STRATEGIC-LoR sign-off AND the operator's prop-rail (Tradeify) disposition** — the park-vs-retire calls depend on it.
- **"Improving" any parked file while marking it** — park is inert; edits are scope creep.

---

## §6 — Consequences

**Positive:** two dead controls (+ two test files) leave the active surface; less suite + boundary-scan surface; the reference scaffold is preserved for the Tradeify path with an explicit re-point trigger; the anchor and locked core are untouched.
**Negative (real):** modest yield — two files, **not** the whole surface (the reverse-dep audit showed most is entangled or template); the parked scaffold still carries FXIFY tests in the suite until the prop-rail decision.
**Risks:** a mis-scoped `tv_mt5` retire if a hidden importer exists (Phase-0b grep mitigates); green FXIFY tests on a parked scaffold may tempt "fixing" a closed firm's logic (accepted, pending the prop-rail decision). Note `test_zero_fills_attestation` imports `dxtrade_pdf_to_csv` (PARKED-kept), so removing the attestation test does **not** disturb the parser or the reconcile tests.

---

## §7 — Implementation plan

**Phase 0 — BLOCKING (no `git rm` until all clear).**
- **0a — reverse-dependency audit** — **DONE this session** (reported §0): `zero_fills`/`tv_mt5` have no code importers; `fxify_rule_validator`/`dxtrade_pdf_to_csv`/`accounts.py`-FXIFY are entangled (park).
- **0b — `tv_mt5_pnl_reconciliation` importer re-confirm** — `git grep -nE 'tv_mt5_pnl|import tv_mt5'` across `core lab ops scripts tests` → expect zero non-self hits; if a live importer exists, downgrade `tv_mt5` to PARK.
- **0c — OPERATOR INPUT (prop-rail disposition)** — the Tradeify / prop-rail decision that sets park-vs-retire for the scaffold rows. Without it, only the two untangled RETIRE rows may proceed; the PARK rows stay parked by default.

**Phase 1 — Retire the untangled dead controls.** `git rm` `zero_fills_attestation.py` + its test; `git rm` `tv_mt5_pnl_reconciliation.py` + its test (post-0b). Then: `check_boundaries` green, `validate_params` green, full `pytest` green (retired fixtures removed, not skipped).

**Phase 2 — Park provenance (no code change).** Mark `fxify_rule_validator.py`, the `accounts.py` FXIFY path, and `dxtrade_pdf_to_csv.py` as **PARKED** in `REPO_MAP.md` with the re-point trigger ("a prop-firm rail is pursued — Tradeify verdict / R6 flip"). Import-clean already; no severing needed.

**Phase 3 — Provenance.** `REPO_MAP.md` struck-through rows for the two retired controls (weekly-review-feeder / Gen-1 pattern); `STATE.md` open-thread note; `CLAUDE.md` only if it names a retired path. Commit on a branch; PR for operator confirmation — **no self-merge**.

---

## §10 — Audit hooks (runnable)

```bash
cd "C:/Users/joshu/multi_firm_operations"

# RETIRE targets gone from the active tree (post-execution → expect empty)
git ls-files ops/live_journal/scripts/zero_fills_attestation.py ops/tv_mt5_pnl_reconciliation.py
git ls-files ops/live_journal/tests/test_zero_fills_attestation.py tests/ops/test_tv_mt5_pnl_reconciliation.py

# PARKED scaffold present + import-clean (expect NON-empty; validator still resolves its core constants)
git ls-files ops/fxify_rule_validator.py ops/live_journal/scripts/dxtrade_pdf_to_csv.py | head
git grep -nE 'FIRM_RULES\["FXIFY"\]|from fxify_rule_validator' -- ops/fxify_rule_validator.py ops/accounts.py   # consumer intact

# dxtrade parser still imported by reconcile (proof it was NOT retired)
git grep -nE 'dxtrade_pdf_to_csv' -- ops/live_journal/reconcile

# Locked core FXIFY constants + anchor UNTOUCHED (expect empty diff)
git diff --stat <ratification>~1..<ratification> -- core/firm_rules.py core/dd_protection.py core/portfolio_mc.py '*.pine'
python -m pytest tests/test_mc_anchors.py -q     # 99.83/0.17/4.37 byte-identical

# Provenance recorded
grep -niE 'retired|parked' REPO_MAP.md | grep -iE 'zero_fills|tv_mt5|fxify|dxtrade'

# Evidence preserved (expect NON-empty)
git ls-files docs/notes/audits/issue_54_ulp_audit ops/live_journal/data/no_manual_attestation_log.md
```

---

## Verification

```bash
# Discipline check (mechanical)
python scripts/check_brief.py docs/adr/2026-07-11-fxify-ops-surface-retirement.md --type adr
# Expected: no HARD violations

# Reverse-dep re-confirm before any rm (Phase-0b)
git grep -nE 'tv_mt5_pnl' -- core lab ops scripts tests | grep -v '^ops/tv_mt5_pnl_reconciliation.py\|test_tv_mt5'   # expect EMPTY
```

---

## Addendum (2026-08-02) — Copygram alert-validator estate retired

The 2026-07-24 Algorithm repo review
(`docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`; handoff
`docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md`)
found the TV→Copygram→DXTrade alert-validation estate —
`core/config/symbol_inventory.toml` + `scripts/validate_alert_payloads.py` +
`tests/test_validate_alert_payloads.py` — survived both this ADR and the
2026-07-22 substrate ADR unenumerated: a fail-closed gate for a rail closed
2026-07-10, with zero executable consumers (the c1 rail's
`ops/c1_rail/crosstrade_payload.py` never imported it). Deleted 2026-08-02 on operator
GO for the dead-FXIFY/NT8 surface prune (Cloud Agent session). Bytes remain in
git history; restore requires a fresh decision, not a revert. The handoff's broader orphan slate is discharged under **Addendum 2026-08-02b** + Gen-1 codification addendum (Packet D GO).

---


## Addendum (2026-08-02b) — remaining 2026-07-24 orphan one-shots pruned

Operator GO recorded on
`docs/briefs/handoffs/2026-07-24-cursor-handoff-dead-surface-retirements.md`
(via parent prune brief Packet D,
`docs/briefs/programs/2026-08-02-retired-surface-mission-alignment-prune.md`). Deleted:

- `scripts/inactivity_simulator.py` (Q-MCTO-1 shadow; production `bust_inactivity`
  lives in `core/mc/simulation.py`)
- `scripts/migrate_adr_headers_m1.py` (migration complete; `check_adr_graph.py`
  is the durable gate)
- `.claude/commands/mc-anchors.md` (hard-fails post-substrate-Phase-3)
- the two GBPUSD-VBR cert RUNBOOK work-instruction files (cert permanently 1/12
  PENDING; evidence JSONs retained)

Copygram validator estate was already retired under Addendum 2026-08-02 (Slice 1).
`lab/codification/` + repo-side `notion-mcp-api-patterns` skill are dispositioned
under the Gen-1 retirement ADR addendum / ruling #3+#4 (same GO). Bytes remain in
git history; restore requires a fresh decision, not a revert.


## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial draft — `Proposed`, awaiting operator STRATEGIC-LoR ratification + the prop-rail (Tradeify) disposition; §0 reads + Phase-0a reverse-dependency audit executed this session (surface found coupled → retire 2 untangled controls, park the reference scaffold) | claude.ai advisor |
| 2026-07-11 | **Operator ratification + disposition override** — Status to Accepted; §7 Phase-0c resolved (FXIFY retired regardless of Tradeify); `fxify_rule_validator` + `accounts.py` FXIFY path PARK to RETIRE; `dxtrade_pdf_to_csv` stays parked (reconcile-coupled), core FXIFY constants untouched (anchor); execution handoff dispatched | Joshua (operator) + claude.ai advisor |
| 2026-08-02 | **Addendum 2026-08-02b** — remaining 07-24 orphan one-shots pruned (Packet D GO) |
| 2026-08-02 | **Addendum** — Copygram alert-validator estate (`symbol_inventory.toml` + `validate_alert_payloads.py` + test) retired; broader 2026-07-24 orphan slate still GO-gated | Cursor Cloud Agent (operator prune GO) |
| 2026-08-03 | Pointer update: `issue_54_ulp_audit.*` relocated `ops/data/audits/` → `docs/notes/audits/`; annotate-never-delete still holds | Joshua + Cursor |

## Addendum 2026-08-29 — §2 KEEP and PARK rows both superseded by later dispositions

The §2 KEEP row (`ops/accounts.py` general machinery + `ops/cli.py` `add`/`update`/`status`/`lots`)
was superseded by [`2026-07-22-challenge-era-substrate-retirement.md`](2026-07-22-challenge-era-substrate-retirement.md)
Phase 2 (the "multiplier spine," merged 2026-07-24, PR #485) — both files' non-tearsheet surface is
deleted; `ops/cli.py` now exposes only `tearsheet`. Verified on this repo as of 2026-08-29:
`ops/accounts.py` and `ops/fxify_rule_validator.py` do not exist, and `ops/cli.py`'s only
`add_parser` call is `tearsheet`.

The §2 PARK row for `ops/live_journal/scripts/dxtrade_pdf_to_csv.py` was discharged by
[`2026-07-11-ops-cfd-estate-retirement.md`](2026-07-11-ops-cfd-estate-retirement.md) (the
reconcile-pipeline disposition this ADR deferred to per that ADR's own §2/§0 — see its explicit
"DONE BY THE PARALLEL `fxify-ops-surface-retirement` ADR... this ADR does **not** touch
`accounts.py`/`cli.py` at all" note), which retired the entire `ops/live_journal/` subtree.
`dxtrade_pdf_to_csv.py` is confirmed absent from the current repo.

Current authoritative pointer for the ops surface: [`REPO_MAP.md`](../../REPO_MAP.md).

Never edit §0-§10 or the addendum above in place — this addendum records the two supersessions only.
