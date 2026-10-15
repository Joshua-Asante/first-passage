# ADR 2026-07-22 — Retire the challenge-era substrate after decoupling the futures path

**Status:** `Accepted` — operator approved in principle 2026-07-22; §7 Phase 0 returned `RESOLVED` 2026-07-22 (all five §4 pre-acceptance conditions met), which authorizes Phases 1-6. **Phase 1 decoupling MERGED** 2026-07-22 (PRs #477 / #479: historical fixture named; `ACTIVE_FIRM=Tradeify_Select_100K`; synthetic planted-defect fixtures; FXIFY-C2 `dd_geometry` seed retired). **Phase 2 (multiplier spine) MERGED** 2026-07-24 (PR #485). **Phase 3 (Pepperstone executable anchor) MERGED** 2026-07-24 (PR #488). **Phase 4 (FXIFY core defaults) MERGED** 2026-07-30 (PR #572, `fc14682`) — `FIRM_RULES["FXIFY"]` / `ACTIVE_FIRM` / `BASELINE_BALANCE` deleted; historical challenge semantics frozen in `core/historical_challenge.py`; living firm selection is always an explicit `FIRM_RULES` key. **Phase 5 (OANDA + Dukascopy wipe) MERGED** 2026-08-02 (`0091c5f`, pre-public history) — OANDA dir removed from `MANIFEST_DIRS`; eight OANDA CSVs + three `*_duka.csv` deleted; hashes in [Phase 5 tombstone (private archive)](https://github.com/Joshua-Asante/first-passage-archive/blob/00cdd1484ef1087ee97c7da2e4011777384b5cbf/docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md). **Phase 6 docs landed** 2026-08-23 ([completion](../ltm/notes/2026-08-23-substrate-phase-6-completion.md)); destroy-copy remains operator-gated. Consolidated owner of the closed CFD/challenge era (§11).
**Decision date:** 2026-07-22
**Supersedes:** `2026-06-17-dukascopy-retirement.md` in part — cached `*_duka.csv` retention clause
**Supersedes:** `2026-06-24-oanda-retirement.md` in part — frozen OANDA CSV retention clause
**Supersedes:** `2026-07-11-challenge-era-claims-rescope.md` in part — Pepperstone anchor, FXIFY fixture, and challenge-diagnostic retention clauses
**Supersedes:** `2026-07-11-ops-cfd-estate-retirement.md` in part — multiplier-spine KEEP clause
**Supersedes:** `2026-07-12-prop-portfolio-four-friendly-firms.md` in part — `ACTIVE_FIRM="FXIFY"` retention/prohibition only
**Supersedes:** `2026-07-13-dd-protection-concept-not-constant.md` in part — FXIFY-C2 seed-row and `ACTIVE_FIRM` retention only
**Supersedes:** `2026-07-17-c1-rail-build-account-registration-go.md` in part — `ACTIVE_FIRM` retention prohibition only
**Supersedes:** `2026-05-10-mc-c2-anchor-ratification.md` in part — Pepperstone C2 anchor pins and audit hooks
**Supersedes:** `2026-06-06-firm-constants-single-source.md` in part — the ACTIVE_FIRM-selector-mechanism clause
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Revision:** 2026-10-15 — retention trim (ADR decay audit; operator direction 2026-10-15): §0 per-path reads and cheap-falsifier record, the §4 pre-acceptance gate (with its FALSIFIED/AMBIGUOUS limbs), the §6 downstream-artifact list, the §7 Phase 0–6 bullets (now a table), the §10 Class-S block and `## Verification` removed; §11 added (consolidation). Pre-trim text at blob `2de3e1a2ee69f3170e5ef86792cc1101694435b0` (commit `4121e84c95f4990b71962e3b9570c4c3fad88426`).

---

## §0 — Rule 0 reads and cheap falsifier

Read before authoring on 2026-07-22 (anchor `a53ee99`, 2026-07-13): `core/firm_rules.py`,
`core/dd_protection.py`, `core/mc/modes.py`, `ops/cli.py`, `scripts/check_data_manifests.py`,
`core/dd_geometry.py`, the then-live account store and the predecessor ADRs. The cheap
falsifier (no vendor bytes in the cloud clone; FXIFY import-time coupling) refuted a
direct-delete plan and set the staged program. The per-path reads and the falsifier record
are in the pre-trim text (Revision line).

---

## §1 — Context

FXIFY/DXTrade, OANDA, and Dukascopy are retired venues or feeds. The old
manual-CFD ops estate has already been deleted, the c1 execution path now uses
Tradeify/Tradovate, and B3 confirmed that the continuous-lot multiplier spine
has no forward consumer on either surviving integer-micro path. The remaining
challenge-era substrate is retained mainly to reproduce one historical
FXIFY-shaped Pepperstone result, while the T1 self-funded framework and the
prop-portfolio firm-specific scoring path now own forward risk questions.

That retention has a continuing cost: `ACTIVE_FIRM="FXIFY"` determines core
module globals at import time; a missing vendor panel silently skips the anchor;
the account CLI presents dormant challenge-era operations beside the c1 rail;
and active manifest policy still treats fully retired OANDA and Dukascopy bytes
as required local state. Retaining historical prose and checksums is useful;
retaining the historical venue as executable default state is not.

**Decision driver (one sentence):** the forward futures stack now has its own
risk framework, firm rules, sizing path, and execution rail, so the closed
CFD/challenge substrate should leave executable `core/` and `ops/` after those
forward consumers are mechanically decoupled.

---

## §2 — Decision

**Decision:** retire the challenge-era executable and vendor-data substrate as
one governed program of independently reviewable code phases, while preserving
the venue-agnostic risk mechanism, active futures-prop rules, c1 rail, locked
strategy parameters, historical narrative, and cryptographic provenance.
Code phases are reversible through Git; vendor-byte deletion becomes
irreversible when the operator later destroys the offline rollback copy.

The retirement has five coupled dispositions:

### A. OANDA frozen data — DELETE

- Delete the eight gitignored CSVs under `core/data/tv_exports/oanda/`.
- Remove `core/data/tv_exports/oanda/SHA256SUMS` from the active manifest
  contract and remove the directory from `MANIFEST_DIRS`.
- Preserve the retired filenames and hashes in one LTM tombstone record; do
  not preserve runnable OANDA panels.
- Repair living documentation that still describes the OANDA directory as a
  required local restore target. Historical ADR bodies remain historical.

### B. Dukascopy cached data — DELETE

- Delete the three `core/data/bar_data/*_duka.csv` files and their active
  manifest rows.
- Close/archive or explicitly mark non-runnable every study that still reads
  those bytes before deletion.
- Preserve producer-retirement history and hashes in the same LTM tombstone;
  do not restore the Dukascopy adapter or retain a runnable frozen panel.

### C. Pepperstone historical anchor — RETIRE AS AN EXECUTABLE PIN

- Delete the four 2026-05-24 anchor CSV bytes only after the Phase-0 operator
  checkout records a clean final reproduction and an offline rollback copy.
- Remove those four rows from the active Pepperstone `SHA256SUMS`; preserve
  filenames, hashes, final reproduced metrics, seeds, and panel cardinality in
  historical documentation.
- Remove `[mc_anchor_pepperstone]` from `core/config/params.toml`, the
  `PEPPERSTONE_PANELS`/`DEFAULT_PANEL` historical-default contract, anchor
  parsing from `scripts/verify_lock_anchors.py`, and the skip-gated anchor tests.
- Replace the deleted anchor's *engine correctness* role with small committed
  synthetic fixtures that exercise deterministic simulation, daily/static/
  trailing bust semantics, DD scaling, seeded serial/parallel equivalence, and
  panel-shape guards without vendor bytes or historical pass-rate assertions.
- Keep `core/mc/` only as a parameterized simulation library used by current
  firm scoring and research. Remove the bare-command implication that its
  default answer is an FXIFY challenge result.
- Keep the historical numbers in `docs/mc_anchor_history.md` as retired
  evidence, not as a validator input, root-doc headline, or live invariant.

### D. Multiplier spine — DELETE; tearsheet survives separately

- Delete `ops/accounts.py`, `tests/ops/test_accounts.py`, and the gitignored
  `ops/data/accounts.json` after confirming no account is registered.
- Remove `add`, `update`, `status`, and `lots` from `ops/cli.py`, together with
  account persistence and continuous-lot multiplier documentation.
- Extract the independent `tearsheet` command to a narrow historical-analysis
  entry point before deleting the general account CLI surface.
- Keep `core/csv_parser.py` and `core/lib/tearsheet.py` only while that extracted
  entry point consumes them. Independently, preserve or relocate
  `csv_parser.STRATEGY_DAYS`, which `scripts/validate_params.py` consumes as a
  live parameter-drift gate; parser disposition requires both consumers to be
  removed or migrated.
- Remove `RISK_TIERS`, `BASELINE_RISK`, and any $200K multiplier-only aliases
  from `core/firm_rules.py` after the consumer sweep is empty.

This deletes only the legacy continuous-lot account spine. It does **not**
delete or weaken c1’s active rail-side sizing law:
`r_eff = BASE_RISK × DD_SCALE × lifecycle`, followed by integer quantity and
RESERVE-cap flooring. Q-PYRPARITY-1 made that mechanism mandatory; it does not
call `ops/accounts.py::calc_multiplier`.

### E. FXIFY core constants and default selection — DELETE AFTER DECOUPLING

- Delete `FIRM_RULES["FXIFY"]` and `ACTIVE_FIRM`.
- Remove import-time derivation of challenge target, daily-loss, static-DD,
  inactivity, and starting-equity globals from `core/dd_protection.py`,
  `core/mc/modes.py`, `core/mc/simulation.py`, and
  `scripts/inactivity_simulator.py`.
- Pass firm rules and account basis explicitly into simulation/scoring
  functions. Current prop scoring must continue to select named Tradeify,
  MFFU, Bulenox, or BluSky tiers explicitly.
- Remove `BASELINE_BALANCE` from `firm_rules.py`; any surviving research basis
  must be named locally for what it represents rather than inherited from the
  closed FXIFY challenge.
- Preserve `DD_TRIGGER`, `DD_SCALE`, `BASE_RISK`, lifecycle multipliers, the
  venue-agnostic `dd_geometry` types/mapping contract, and locked strategy
  allocations. Retire `POLICY_REGISTRY["FXIFY-C2"]`,
  `_validate_fxify_seed()`, and their FXIFY pin tests; admit no replacement
  registry row without the existing pre-registration → re-MC → both-halves
  regime gate → ADR chain.
- Preserve all active automation-friendly firm rows, especially
  `Tradeify_Select_100K`, which c1 sizing reads.

**Effective:** upon acceptance, which is permitted only after the
pre-acceptance gate in §4 returns `RESOLVED`. While status is `Proposed`, all
supersession edges are pending and no implementation or predecessor retain
clause changes. Acceptance authorizes Phases 1–6; each remains subject to the
post-acceptance falsifier.

**Scope:** executable challenge defaults, continuous-lot account tooling, the
three retired feed/anchor byte classes, their active manifests, tests, and
living documentation. No Pine source, strategy parameter, allocation,
lifecycle tier, c1 order path, CME data, current Tradeify/MFFU/Bulenox/BluSky
rule, or T1 risk claim is changed.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep all frozen fixtures indefinitely | This is the current posture. It leaves a closed venue as the core import-time default, lets the anchor silently disappear behind `skipif`, and keeps retired vendor trees in the active manifest contract. |
| Delete all five classes immediately | Falsified by §0: FXIFY is import-time coupled, active studies still reference retired-feed bars, the cloud clone cannot verify vendor bytes, and Pepperstone deletion would silently disable rather than consciously retire its test. |
| Delete only OANDA and Dukascopy | Removes low-risk bytes but leaves the larger architectural contradiction: FXIFY remains the default and the dormant multiplier/anchor continue to define the apparent purpose of `core/` and `ops/`. |
| Keep the Pepperstone anchor but move it to LTM | Vendor bytes are gitignored and cannot become an LTM artifact; keeping them locally still preserves the same non-portable executable pin. Hashes and final metrics are sufficient historical evidence once synthetic engine fixtures replace its correctness role. |
| Keep multiplier code as a future template | B3 found its premises absent from both forward paths. A future continuous-lot multi-account operation should be designed against its actual venue rather than reactivating a $200K FXIFY abstraction. Git history remains the design reference. |
| Delete the entire MC and DD stack with the anchor | Over-retirement. Current prop scoring, c1 sizing, lifecycle authorization, and venue-agnostic risk work still consume those mechanisms. This ADR parameterizes and preserves them. |
| Erase the historical numbers and decisions | Historical claims are evidence, not runtime. Removing prose would make prior locks and retirements unauditable without reducing executable complexity. |

---

## §4 — Falsifier and acceptance gate

**Hypothesis:** after explicit firm/account parameterization and replacement
synthetic fixtures, removing OANDA, Dukascopy, the Pepperstone executable
anchor, multiplier spine, and FXIFY defaults will leave c1 sizing and current
prop/research simulation behavior unchanged while eliminating every executable
dependency on the closed CFD/challenge world.

The pre-acceptance gate (five conditions) returned `RESOLVED` 2026-07-22 (Change history);
its text is in the pre-trim body (Revision line).

### Post-acceptance implementation falsifier

After acceptance, each phase must prove its own behavior-preserving gate.
Before the vendor bytes are deleted, the replacement synthetic MC tests must
fail under each planted defect and pass on the decoupled engine. With all
retirement targets absent, c1 sizing vectors, Class-S scoring/regime smoke
tests, current firm preflight, lifecycle, surviving lock verification, and
`make check` must pass. Any miss reverts that phase and requires a superseding
ADR or corrected implementation before work continues.

**Revert action:** code and tracked manifests revert by commit. Gitignored
vendor bytes restore only from the Phase-0 offline copy. A future need for
OANDA, Dukascopy, or a challenge-class anchor requires a new ADR and fresh
venue data; it does not silently re-arm this historical fixture.

**Trigger check schedule:** 2026-10-31 — Pepperstone feed/data 90-day check (2026-08-02 Pepperstone ADR §4; §11 table) · 2026-11-01 — CFD `bar_data` + `tv_exports/candidates` 90-day check (2026-08-03 bar-data ADR §4; §11 table) · 2026-11-08 — end of the two-quarter windows of the 2026-08-03 params-toml ADR §4 (a live defect traced to Pine/`dd_protection`/`firm_rules`/root-doc skew that the retired `validate_params` hub would have hard-failed and no surviving gate catches → shape-2 restore ADR or git restore) and of the 2026-08-03 futures-refocus ADR §4/§6 (a dated incident attributing a decision error to a fact that pass demoted → restore that block class) · 2026-11-08, 2027-02-08, 2027-05-08 — quarterly reviews of the event triggers now quoted in §11 rules 2–3 (2026-07-10 R6 ADR §4, 2026-07-11 claims-rescope ADR §4) and the 2026-11-08 Gen-1 quarterly ride (2026-07-11 Gen-1 ADR §4; its codification limb was discharged by the 2026-07-24 bridge retirement) · 2027-01-11 — Gen-1 extraction-incompleteness check (2026-07-11 Gen-1 ADR §4; §11 table) · before any offline copy is destroyed — final consolidated check (§10), then a separate operator confirmation (§11).

---

## §5 — Forbidden moves

- **Deleting vendor bytes before the operator-side manifest check, final anchor
  reproduction, and offline inventory.** These bytes are gitignored and cannot
  be recovered from repository history.
- **Removing FXIFY first and repairing imports afterward.** The current modules
  derive globals at import time; decoupling must land and pass while the
  historical fixture still exists.
- **Removing `DD_TRIGGER`, `DD_SCALE`, `BASE_RISK`, lifecycle, `dd_geometry`, or
  active firm rows as “FXIFY constants.”** They have forward c1 or
  prop-portfolio consumers and are explicitly outside this retirement.
- **Changing allocations, Pine parameters, or c1 quantities to make the
  decoupled tests pass.** The retirement must be behavior-preserving for the
  forward stack.
- **Deleting anchor tests while leaving anchor prose/config/defaults active, or
  leaving skip-gated tests after deleting bytes.** The pin retires atomically
  across data, config, verifier, tests, and living claims.
- **Deleting `ops/cli.py` before extracting tearsheet.** Multiplier retirement
  does not silently retire the independently retained CSV-analysis capability.
- **Treating historical ADR and LTM references as stale code references and
  bulk-rewriting them.** Repair living instructions; preserve point-in-time
  decision bodies.
- **Deleting CME panels, current BAR EXPORT inputs, Pine manifests, c1 rail
  code, or the Tradeify account rule.** Similar location is not shared
  disposition.
- **Accepting all phases as one unreviewable commit.** Code decoupling,
  multiplier removal, anchor retirement, and each vendor-data class require
  independent rollback boundaries.

---

## §6 — Consequences

The program-level verdict remains the binary §4 result:
`RESOLVED`, `FALSIFIED`, or `AMBIGUOUS`; consequences below do not soften that
gate.

**Positive consequences:**

- `core/` no longer selects a closed firm at import time.
- `ops/` reflects the actual c1 execution path rather than a dormant
  continuous-lot account product.
- Retired OANDA and Dukascopy files leave the active manifest contract.
- Engine correctness becomes portable and CI-executable through committed
  synthetic fixtures instead of local proprietary bytes.
- The historical anchor remains auditable as narrative plus hashes without
  masquerading as a current runtime invariant.

**Negative consequences (real costs):**

- Exact re-execution of the 99.83/0.17/4.37 historical result is intentionally
  lost after the offline rollback copy expires.
- Closed OANDA/Dukascopy studies lose local rerunnability.
- The implementation is a non-trivial parameterization of core MC and
  protection code, not a data-only prune.
- Removing the multiplier CLI discards a tested convenience surface that would
  otherwise be recoverable immediately from the working tree.
- Vendor-byte deletion is irreversible after the operator destroys the offline
  rollback copy; Git can restore manifests and code, not proprietary CSVs.

**Risks:**

- Synthetic fixtures may cover mechanics but miss an emergent full-panel
  interaction formerly caught by the historical anchor. Mitigation: planted
  defect tests plus current prop-scoring regression vectors.
- A research script may hide a path dependency outside indexed search.
  Mitigation: `rg --no-ignore`, catalog disposition, and phase-by-phase tests.
- Historical numbers may continue to appear as canonical through stale living
  documentation. Mitigation: root-doc and path-liveness sweeps in the same
  program.

---

## §7 — Implementation plan

| Phase | Scope | PR / commit | Date |
|---|---|---|---|
| Phase 0 | Operator-side evidence and freeze: manifest check, anchor reproduction, offline byte inventory, recorded Pepperstone panel release, consumer inventory, baselines; returned `RESOLVED` | acceptance commit (Change history) | 2026-07-22 |
| Phase 1 | Decouple forward code from FXIFY: explicit firm rules and account basis in `core/mc/`, Class-S explicit tiers, FXIFY-C2 `dd_geometry` seed retired, synthetic engine fixtures | #477 / #479 | 2026-07-22 |
| Phase 2 | Retire the multiplier spine (tearsheet extracted first) | #485 | 2026-07-24 |
| Phase 3 | Retire the Pepperstone executable anchor: bytes, manifest rows, config pins, default-panel contract, verifier parsing and anchor tests removed atomically; record and hashes kept in LTM | #488 | 2026-07-24 |
| Phase 4 | Remove FXIFY core defaults (`FIRM_RULES["FXIFY"]`, `ACTIVE_FIRM`, challenge-derived globals) | #572 (`fc14682`) | 2026-07-30 |
| Phase 5 | Retire OANDA and Dukascopy frozen data: studies marked blocked first, bytes deleted, OANDA removed from `MANIFEST_DIRS`, LTM tombstone | `0091c5f` (pre-public history) | 2026-08-02 |
| Phase 6 | Consolidated documentation and completion ([completion note](../ltm/notes/2026-08-23-substrate-phase-6-completion.md)). Mark the explicit point of no return. Destroy the temporary offline byte copy only after a separate operator confirmation; after that action A–C are intentionally irreversible. | Phase-6 note | 2026-08-23 |

Each numbered phase lands in its own commit and may use its own PR. No later
phase begins while an earlier phase is red or ambiguous.

---

## §10 — Audit hooks

```bash
# ADR structure and graph
python3 scripts/check_brief.py \
  docs/adr/2026-07-22-challenge-era-substrate-retirement.md --type adr
python3 scripts/check_adr_graph.py

# Forward code must not reference retired selectors/surfaces after completion
rg -n 'ACTIVE_FIRM|FIRM_RULES\["FXIFY"\]|calc_multiplier|get_multipliers' \
  core ops lab scripts tests --glob '*.py' --glob '!lab/archive/**'
# Expected: empty in active code. Historical prose and cold archive are exempt.

# Retired executable anchor must be absent rather than skipped
rg -n 'PEPPERSTONE_PANELS|mc_anchor_pepperstone|requires_pepperstone' \
  core lab scripts tests --glob '*.{py,toml}' --glob '!lab/archive/**'
# Expected: empty.

# OANDA and Dukascopy are no longer active manifest owners
rg -n 'tv_exports/oanda|_duka\\.csv' \
  scripts/check_data_manifests.py core/data/*/SHA256SUMS
# Expected: empty.

# Active forward invariants remain
rg -n 'Tradeify_Select_100K' core/firm_rules.py ops/c1_rail/c1_sizing_host_reference.py
rg -n '^DD_TRIGGER|^DD_SCALE|^BASE_RISK' core/dd_protection.py
rg -n 'TIER_MULTIPLIER' core/lifecycle.py ops/c1_rail/c1_sizing_host_reference.py

# No silent vendor skip replaces the retired anchor
rg -n 'skipif.*Pepperstone|requires_pepperstone' tests
# Expected: empty.

# Mechanical gates after every data phase
python3 scripts/check_data_manifests.py
python3 scripts/check_boundaries.py
python3 scripts/check_path_liveness.py
python3 scripts/check_root_doc_liveness.py
python3 scripts/verify_lock_anchors.py
make check

# Targeted forward regressions
python3 -m pytest tests/ops/test_c1_sizing_host_reference.py \
  tests/ops/test_c1_rail_listener.py \
  tests/test_lifecycle.py \
  tests/core/test_mc_preflight.py \
  tests/core/test_dd_geometry.py \
  tests/core/test_firm_constants_single_source.py -q
# NOTE: lifecycle tests live at tests/test_lifecycle.py, NOT tests/core/.
# The original path here did not resolve (fixed 2026-07-22 during Phase-0
# condition-5 capture); dd_geometry + firm-constants added as A-E consumers.

# Full acceptance
python3 -m pytest tests/ -q
```

---

<a id="cfd-challenge-era-carried-forward"></a>
## §11 — Closed CFD/challenge era: carried-forward rules and obligations (consolidated 2026-10-15)

Consolidated 2026-10-15 from `2026-07-10-r6-nogo-futures-residual-disposition`,
`2026-07-11-challenge-era-claims-rescope`, `2026-07-11-gen1-pipeline-retirement`,
`2026-07-11-ops-cfd-estate-retirement`, `2026-08-02-pepperstone-feed-retirement`,
`2026-08-03-bar-data-cfd-and-candidates-retirement`, `2026-08-03-params-toml-gate-retirement` and
`2026-08-03-claude-md-futures-refocus` (removed; see
[TOMBSTONES](TOMBSTONES.md#2026-10-15-adr-decay-audit-removals)). This section owns what survives of
them; quoted clauses keep their original authority and source. The removed bodies are history only
and grant nothing.

**Standing rules**

1. **No manual execution** — the no-manual-execution rule and its reconciliation with
   [AGENTS.md §Live-execution posture](../../AGENTS.md#live-execution-posture) remain owned by the
   [2026-06-30 no-manual/CFD retirement ADR](2026-06-30-no-manual-trading-cfd-retirement.md)
   (including its 2026-07-10 CFD venue closure) pending a later consolidation.
2. **Locked-book futures-prop fan-out NO-GO** — 2026-07-10 R6 ADR §4: "the futures-prop path re-opens
   **only** on **new mechanism evidence** that a locked leg transfers to a prop-micro venue with
   edge-preservation ≥ 0.8× under realistic (commission + slippage + force-flat) modeling — a *dated,
   pre-registered* result, not a re-run of any spent gate (P2 K2/E1 or R5 B2) on a shifted window.
   Absent that, the NO-GO holds." Program-level restatement:
   [four-firm ADR §2 R6 boundary](2026-07-12-prop-portfolio-four-friendly-firms.md); kill evidence
   `lab/archive/striker_dj30_mym_prototype_2026-07/RESULTS.md`.
3. **Challenge-era numbers are historical** — 2026-07-11 claims-rescope ADR §4: when a live
   challenge-class venue re-enters, "the re-arming ADR must commission a fresh re-MC under *that
   venue's* rules (never a revival of 99.83/0.17/4.37 as a live number — it stays historical
   regardless)". Its Addendum 2026-07-22 retired the quarterly C2→C0 revert check; `dd_protection`
   change-control is the chain in [AGENTS.md §Protection](../../AGENTS.md#protection).
4. **Retired surfaces** — (a) ops CFD-estate ADR §4 Trigger A: "**rebuild repo-native against the
   *actual* venue microstructure FIRST** (the retired code is design reference via `git show`, not a
   drop-in restore) — do **not** `git revert` the DXTrade-coupled design". (b) params-toml ADR §5:
   "Reintroducing a derived `params.toml` (or equivalent hub mirror) without a new ADR" and "Weakening
   `check_pine_manifest` / path-liveness / skill no-constants to "make retirement green"" are
   forbidden; hook lesson (its Addendum 2026-08-08): "a hook of the form `git diff -- <path>` cannot
   distinguish *absent* from *unchanged*, and an `A && B` hook silently disables `B` when `A` is
   retired. Prefer `test -e <path> &&` guards, or separate the limbs onto their own lines." (c) Gen-1
   ADR: the hand-rolled harness stays retired ([strategy-validation §8a](../../.claude/skills/strategy-validation/SKILL.md),
   "do not reimplement"); a specific module is restored only via the 2027-01-11 row below; Addendum
   2026-07-24: "a future Python→Pine bridge is a fresh build against the then-current survivor format,
   not a restore." (d) OANDA, Dukascopy or a challenge-class anchor: §4 Revert action above.
5. **Feeds** — owner: [feed policy §Retired feeds](2026-06-12-tv-csv-canonical-feed-policy.md#retired-feeds).

**Open obligations**

| Item | Date / wake | Rule (verbatim source) |
|---|---|---|
| Pepperstone feed/data retirement (2026-08-02 ADR §4) | 2026-10-31 | "if within **90 days** any live decision — a rail change, a lifecycle rung move, a screen verdict, or an 11-08 §4 limb — requires a Pepperstone-sourced number that no venue-native substitute can supply … restore from the offline copy and re-admit the panel via a superseding ADR." RESOLVED: no blocked decision (copy may be considered for destruction under a separate ruling) · FALSIFIED: restore from copy (b); re-admit by superseding ADR; record what the venue-native substitute failed to supply · AMBIGUOUS: historical reproduction only → read-only restore; **no** manifest re-admission. |
| CFD `bar_data` + `tv_exports/candidates` (2026-08-03 ADR §4) | 2026-11-01 | "if within **90 days** a live rail / screen / §4 / lifecycle decision is blocked on a deleted basename that no CME / Databento substitute can supply → restore from the offline copy and re-admit via superseding ADR." AMBIGUOUS (historical only): read-only restore; **no** re-admission. |
| Gen-1 extraction-incompleteness (2026-07-11 Gen-1 ADR §4) | 2027-01-11 | "a Gen-2 discovery campaign reaches admission and needs a capability that lived only in the retired Gen-1 code and was *not* captured by the three extractions (controls, rank-ρ parity invariant, §8 invariants #1–#4) → … restore the specific module from git history" and record it here. |
| Offline copies: (a) 2026-07-22, 15 files (8 OANDA, 3 Dukascopy, 4 Pepperstone anchor); (b) 2026-08-02, 35 Pepperstone files; (c) 2026-08-03, 9 CFD bar files + candidates tree (operator machine, `backups/first-passage-*-preretirement-*`) | operator request | "Destroy the temporary offline byte copy only after a separate operator confirmation; after that action A–C are intentionally irreversible" (§7 Phase 6). Not destroyed as part of either retirement (2026-08-02 §5-1; 2026-08-03 §5-3). |

Hash inventories of the deleted bytes: `first-passage-archive` @ `00cdd148`,
`docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`,
`docs/ltm/notes/2026-08-02-pepperstone-data-tombstone.md`,
`docs/ltm/notes/2026-08-03-bar-data-cfd-candidates-tombstone.md`.

**A1 (accept-beta fork)** — 2026-08-02 Pepperstone ADR §2-C: "A1 may not be decided on a
Pepperstone-shaped input that no longer exists, and may not be decided by default either"; §5-2:
"Inventing an A5-substitute number to close A1" is forbidden. A5's retirement and the orphaned
decompound limb 2 (§2-B, §2-D, §5-3, §5-4) are owned by
[decompound HOLD Addendum 2026-08-03](2026-06-07-decompound-remc-hold.md) (its §5 items 1–4 and the
"not pass-rate-shaped" constraint); the [08-08 packet](../briefs/programs/2026-07-17-0808-packet-delta-and-sequence.md)
rows A1/A5 are mirrors.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-22 | Initial `Proposed` ADR; full retirement scope requested, destructive acceptance gated on operator-side evidence | Joshua + Cursor |
| 2026-07-22 | Operator approval-in-principle recorded; status remains `Proposed` until mandatory D2/T2 and operator-checkout Phase-0 evidence return `RESOLVED` | Joshua |
| 2026-07-22 | **§4 condition 3 amended** — calendar lock on the 2026-08-08 D2/T2 date replaced by the substantive requirement it encoded: a *recorded* release of the Pepperstone panel from successor-diagnostic duty, from D2/T2 **or** a validated replacement diagnostic. Rationale: the date was a proxy for "nothing still needs these four panels"; binding on the proxy blocked the program on a calendar rather than on evidence, while binding on the substance preserves the protection (the panels are gitignored and unrecoverable) and lets Phase 0 resolve as soon as the release exists. Propagated to §4 FALSIFIED limb, §4 trigger schedule, §7 Phase-0 step 4, and §7 Phase-3 step 1. **Not** a weakening of the deletion gate: conditions 1, 2, 4, 5 are unchanged and all remain unmet. | Joshua (decision) + Claude Code (amendment) |
| 2026-07-22 | **`Proposed` → `Accepted`.** §7 Phase 0 returned `RESOLVED` — all five §4 pre-acceptance conditions met (anchor reproduced 6 passed/0 skipped; 15-file offline rollback copy verified 15/15 against tracked manifests; D2 released the Pepperstone panel; every A–E consumer dispositioned; baselines captured). Seven partial-supersession reverse edges added and `INDEX.md` regenerated in this same commit per §7 step 8, so the ADR graph is never left red. Authorizes Phases 1–6; **no phase has run and no vendor byte has been deleted.** | Joshua (decision) + Claude Code (recording) |
| 2026-08-23 | **Phase 6 docs landed.** Completion note + §10 cheap-subset evidence. Destroy-copy still operator-gated. No §2 edit. Offline rollback copy not destroyed. | Cursor Cloud Agent |
| 2026-10-15 | Revision: retention trim (pre-trim blob `2de3e1a2`, commit `4121e84c`); §11 consolidates the 07-10 R6, 07-11 claims-rescope/Gen-1/ops-CFD, 08-02 Pepperstone and 08-03 bar-data/params-toml/futures-refocus ADRs (TOMBSTONES); the 2026-06-30 no-manual/CFD ADR stays the owner of its rule; Trigger field carries their future riders. | Claude Code (ADR decay audit) |

---

## Addendum 2026-08-08 — Rule 11 dormancy record (the survivor-scoring prereg's ACTIVE_FIRM hooks)

Rule 11 discharge for the `ACTIVE_FIRM` / `BASELINE_BALANCE` deletion (Phase 4). Recorded here because the
affected body is a **frozen pre-registration** — editable only by close+reopen — so the correction cannot land
where it is read.

**(a) Body darkened.** `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md`, whose §0
load-bearing anchor is `core/firm_rules.py @ 6a0c801 — ACTIVE_FIRM="FXIFY"` (:24):

- **§10 hook 7** (:242-243) — `grep -n "^ACTIVE_FIRM = " core/firm_rules.py   # expect FXIFY`. **Executed
  2026-08-08: exit 1, zero output.** Reads as a breach; is in fact a retirement.
- **§5 forbidden moves** (:175-176) — both name "switching `ACTIVE_FIRM`", now unperformable.
- **§Expected at first scoring** (:248) — asserts `ACTIVE_FIRM=FXIFY`.

**(b) Why this now matters more than when it was written.** [`W4`](2026-08-07-w4-minimal-gate-set-dormancy.md)
(Accepted 2026-08-07) defines the **live minimal gate set** as *"G0–G5 + G8, and any limb a campaign's own frozen
prereg still binds"* — which promotes this body to the definition of the live validation floor, and W4 §5
simultaneously **forbids editing it**. A reader arriving via W4 meets a §0 anchor that no longer exists and a
self-check that false-REDs.

**(c) Degraded, not dark — state it precisely.** Hooks 1–4 still pass; the ADR-relevant failures are hook 7 (above)
and hook 6, which returns 0 because a comment wrap split its search string. Call the gate **degraded at 3 of 7**,
not broken.

**(d) Re-arm condition: none for `ACTIVE_FIRM`** — the selector was deleted, not renamed. Live c1 uses the explicit
tier key `Tradeify_Select_100K`; historical challenge semantics live in `core/historical_challenge.py`. The
prereg's *substantive* scoring protocol is unaffected: `core/mc/preflight.py` exists, the micro contract cap is
live, and G0–G5 + G8 remain computable.

**(e) Surviving coverage.** Verify the tier key directly instead of the deleted selector:

```bash
grep -n 'Tradeify_Select_100K' core/firm_rules.py
```

**Reader-path note.** Neither the four-firms program ADR nor `STATE.md` cites this prereg today, so a W4-only
intercept would miss both checkpoint reader paths — the pointer is owed on W4 §2 and on the STATE forward board.
W4 half landed (W4 §2 note); the STATE half was not landed as of 2026-10-15 (open).
