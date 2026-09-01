# ADR 2026-07-22 — Retire the challenge-era substrate after decoupling the futures path

**Status:** `Accepted` — operator approved in principle 2026-07-22; §7 Phase 0 returned `RESOLVED` 2026-07-22 (all five §4 pre-acceptance conditions met), which authorizes Phases 1-6. **Phase 1 decoupling MERGED** 2026-07-22 (PRs #477 / #479: historical fixture named; `ACTIVE_FIRM=Tradeify_Select_100K`; synthetic planted-defect fixtures; FXIFY-C2 `dd_geometry` seed retired). **Phase 2 (multiplier spine) MERGED** 2026-07-24 (PR #485). **Phase 3 (Pepperstone executable anchor) MERGED** 2026-07-24 (PR #488). **Phase 4 (FXIFY core defaults) MERGED** 2026-07-30 (PR #572, `fc14682`) — `FIRM_RULES["FXIFY"]` / `ACTIVE_FIRM` / `BASELINE_BALANCE` deleted; historical challenge semantics frozen in `core/historical_challenge.py`; living firm selection is always an explicit `FIRM_RULES` key. **Phase 5 (OANDA + Dukascopy wipe) CODE_LANDED** on `chore/substrate-phase-5-oanda-duka` — OANDA dir removed from `MANIFEST_DIRS`; eight OANDA CSVs + three `*_duka.csv` deleted; hashes in [`docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`](../ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md). **Phase 6 docs landed** 2026-08-23 ([completion](../ltm/notes/2026-08-23-substrate-phase-6-completion.md)); destroy-copy remains operator-gated.
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

---

## §0 — Rule 0 reads and cheap falsifier

Read before authoring on 2026-07-22, after `git fetch origin main`; `origin/main`
had no newer commits touching the target paths.

- `core/firm_rules.py` — anchor `a53ee99` (2026-07-13). `FIRM_RULES["FXIFY"]`
  is the closed-venue rule row; `ACTIVE_FIRM="FXIFY"` selects it at import
  time. The same module also owns active four-firm prop configurations and the
  locked risk mirror; those are separate from the FXIFY fixture.
- `core/dd_protection.py` — anchor `a53ee99` (2026-07-13). Import-time
  `FIRM_RULES[ACTIVE_FIRM]` derives the FXIFY target, daily-loss, static-DD, and
  $200K state defaults. The venue-agnostic sizing law
  `BASE_RISK × DD_SCALE × lifecycle` is also here and is consumed by c1.
- `core/mc/modes.py` — anchor `a53ee99` (2026-07-13). The default mode is an
  FXIFY challenge simulator over four named Pepperstone panels; it exposes
  `PEPPERSTONE_PANELS`, `DEFAULT_PANEL`, and challenge-derived module globals.
- `core/config/params.toml` — anchor `784a9ab` (2026-06-24).
  `[mc_anchor_pepperstone]` owns the derived 99.83/0.17/4.37/26 mirror.
- `tests/core/test_mc_anchors.py` — anchor `83ba1b2` (2026-07-12). The four
  Pepperstone bytes gate the anchor tests through `skipif`; missing bytes can
  therefore produce a green suite without executing the pin.
- `ops/accounts.py` — anchor `8c461bc` (2026-07-11). The account store and
  `calc_multiplier` depend on `RISK_TIERS`, `BASELINE_BALANCE`, and
  `BASELINE_RISK`; no production module outside `ops/cli.py` imports the
  multiplier functions.
- `ops/cli.py` — anchor `859e505` (2026-07-20). `add`, `update`, `status`, and
  `lots` are the multiplier-spine surface. `tearsheet` is independently useful
  and must be extracted before the spine is removed.
- `scripts/check_data_manifests.py` — anchor `f2be990` (2026-07-11). OANDA is
  one of six mandatory manifest directories; deleting it requires changing
  the gate and its tests, not only removing CSV bytes.
- `docs/adr/2026-06-17-dukascopy-retirement.md` — anchor `ba943a1`
  (2026-07-17). The adapter is retired but three `*_duka.csv` panels were
  explicitly retained as manifest-pinned history.
- `docs/adr/2026-06-24-oanda-retirement.md` — anchor `ba943a1`
  (2026-07-17). OANDA code and the executable cross-feed tier are gone, but
  eight CSVs were explicitly frozen.
- `docs/adr/2026-07-11-challenge-era-claims-rescope.md` — anchor `ba943a1`
  (2026-07-17). It retained the Pepperstone anchor and FXIFY constants as an
  engine/panel regression fixture while removing their live-claim status.
- `docs/adr/2026-07-11-ops-cfd-estate-retirement.md` — anchor `ba943a1`
  (2026-07-17), plus the B3 disposition at
  `docs/briefs/programs/2026-07-14-b3-multiplier-spine-forward-relevance-disposition.md`
  anchor `d9d764b`. B3 found no forward consumer but chose DORMANT-RETAIN.
- `docs/spec/c1_watch_realization_multiplier_layer.md` — accepted 2026-07-17.
  Its “multiplier layer” is the active rail-side `r_eff` quantity law, not
  `ops/accounts.py::calc_multiplier`; the former must survive removal of the
  latter.
- `core/dd_geometry.py` — the concept is venue-agnostic, but its sole registry
  row and import-time validator are explicitly FXIFY-C2. Preserving the module
  therefore requires retiring that row and pin, not preserving the file
  byte-for-byte.
- `docs/notes/notice/N-2026-07-17-cfd-data-estate-trigger-dated-disposition.md`
  — anchor `9901abb` (2026-07-17). It blocks class-wide deletion on live
  dependencies and names the silent anchor-skip hazard.

**Cheap falsifier, run before this ADR was written:**

```text
Tracked manifests declare: 8 OANDA TV exports, 3 Dukascopy bar files, and
4 Pepperstone 2026-05-24 anchor panels.

This cloud clone contains none of those gitignored vendor bytes and has no
ops/data/accounts.json. check_data_manifests.py therefore reports the declared
vendor files MISSING; the anchor test cannot execute here (pandas is absent,
and the four panel bytes are absent).

Static reverse-dependency checks found:
- calc_multiplier/get_multipliers: only ops/accounts.py, ops/cli.py, and tests;
- ACTIVE_FIRM/FXIFY import-time coupling: dd_protection.py, mc/modes.py,
  mc/simulation.py, inactivity_simulator.py, and research harnesses;
- PEPPERSTONE_PANELS/default-anchor coupling: anchor tests, verifier/tooling,
  scripts, and several lab studies.
```

The empirical result falsifies a direct-delete plan: this environment cannot
prove byte identity or run the anchor, and removing FXIFY before decoupling
would break import-time behavior. It supports a staged retirement whose
destructive byte step runs only in the operator checkout where the vendor files
and research environment exist.

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

### Pre-acceptance gate

**RESOLVED — acceptance permitted only if all are true:**

1. In the operator checkout, the pre-delete manifest check is clean and the
   historical Pepperstone anchor executes once—not skips—and reproduces its
   recorded pins within existing tolerance.
2. A byte-for-byte offline rollback copy exists for every gitignored file in
   A–C, with a generated inventory matching the tracked pre-delete hashes.
3. The Pepperstone panel is released from successor-diagnostic duty — either
   by the D2/T2 decision, or by a validated replacement diagnostic that no
   longer reads the four anchor panels. Release must be *recorded*, not
   assumed; no calendar dependency. (Amended 2026-07-22 — see Change history.)
4. Every active code consumer of A–E—including Class-S scoring, regime riders,
   c1 sizing, `dd_geometry`, and parameter validation—has a named migration or
   archive disposition and an executable acceptance command.
5. Baseline outputs are captured for c1 sizing vectors, alert golden path,
   lifecycle, current firm preflight/scoring, and the historical anchor.

No Phase-1–6 implementation result is required to accept the ADR; requiring
post-removal tests before acceptance would be circular. The five checks above
authorize implementation, not declare it complete.

**FALSIFIED — stop and supersede this proposal if either occurs:**

- the panel-release decision (D2/T2 or its equivalent) retains the Pepperstone
  panel as a successor diagnostic with no validated replacement; or
- any c1 quantity, lifecycle multiplier, named current-firm outcome, or
  forward risk-policy result changes solely because the historical substrate
  was removed; or
- a current dated obligation still requires one of the A–C bytes and has no
  validated replacement input.

**AMBIGUOUS — no destructive deletion:** any missing operator byte, unavailable
dependency, skipped pre-acceptance test, unresolved active consumer, or
non-reproducing pre-delete anchor routes here.

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

**Trigger check schedule:** at pre-acceptance Phase 0 and after each
implementation phase; final consolidated check before the vendor-byte backup
is destroyed. A recorded panel-release resolution is mandatory before
acceptance; it gates on the decision existing, not on a calendar date.

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

**Downstream artifacts to update during implementation:**

- `CLAUDE.md`, `PIPELINES.md`, `REPO_MAP.md`, `STATE.md`, `README.md`
- `docs/mc_anchor_history.md` and a new LTM data-manifest tombstone
- the four partially superseded ADR headers when this proposal is accepted
- `core/config/params.toml`, `scripts/verify_lock_anchors.py`,
  `scripts/validate_params.py`, `scripts/check_data_manifests.py`
- `core/firm_rules.py`, `core/dd_protection.py`, `core/mc/*`
- `ops/accounts.py`, `ops/cli.py`, extracted tearsheet entry point
- corresponding tests, Makefile targets, skills, and operational references
- `docs/SESSIONS.md`

---

## §7 — Implementation plan

### Phase 0 — operator-side evidence and freeze

1. Re-fetch `origin/main`; re-run the reverse-dependency audit with
   `rg --no-ignore`.
2. Run the pre-delete data-manifest check and the full historical anchor test
   in the operator checkout. An all-skipped anchor result is failure.
3. Create an offline byte inventory for all A–C files; verify every SHA-256
   against the active manifests.
4. Obtain a recorded decision releasing the Pepperstone panel from
   successor-diagnostic duty — the D2/T2 review, or a validated replacement
   diagnostic that no longer reads the four anchor panels. Phase 0 cannot
   resolve until that release is recorded; the source of the release is open,
   its existence is not.
5. Inventory every active A–E consumer, including Class-S scoring/regime
   runners, `dd_geometry`, `validate_params`, and c1, with a migration and
   executable acceptance command.
6. Record baseline outputs for c1 sizing vectors, current firm preflight/
   scoring, lifecycle, and MC synthetic controls.
7. Return `RESOLVED`, `FALSIFIED`, or `AMBIGUOUS` under §4. Only `RESOLVED`
   permits this ADR to move from `Proposed` to `Accepted`.
8. In the same commit that flips this ADR to `Accepted`, add the matching
   partial-supersession reverse edge to all seven predecessor ADRs and
   regenerate `docs/adr/INDEX.md`. Acceptance must never leave the ADR graph
   temporarily red.

### Phase 1 — decouple forward code from FXIFY

- Parameterize firm rules and account basis throughout `core/mc/`.
- Separate the venue-agnostic protection calculation from the historical
  challenge-state/reporting CLI.
- Update research harnesses to pass explicit bases and named firms.
- Remove the Class-S candidate scorer’s `ACTIVE_FIRM == "FXIFY"` integrity
  assertion and replace it with checks over explicit tier inputs; execute both
  the scorer and regime-rider smoke paths.
- Remove the FXIFY-C2 `dd_geometry` seed and import-time pin while retaining the
  venue-agnostic policy type and reference-mode mapping.
- Land replacement synthetic engine fixtures and prove their planted-defect
  sensitivity.
- Verify c1 quantities and current firm outcomes before removing any fixture.

### Phase 2 — retire the multiplier spine

- Extract tearsheet.
- Delete account/multiplier code, commands, state, and tests.
- Remove multiplier-only constants after a zero-consumer sweep.
- Run ops, c1, lifecycle, and boundary tests.

### Phase 3 — retire the Pepperstone executable anchor

- Confirm Phase 0’s mandatory panel-release decision is recorded; otherwise stop.
- Record the final operator-side reproduction.
- Remove the four anchor bytes and manifest rows.
- Atomically remove config pins, default-panel contract, verifier parsing,
  historical anchor tests, and canonical living headlines.
- Preserve the historical record and hash inventory in LTM.
- Confirm no pin test remains skip-gated.

### Phase 4 — remove FXIFY core defaults — MERGED 2026-07-30 (PR #572)

- Delete the FXIFY rule row and `ACTIVE_FIRM`.
- Remove remaining challenge-derived globals and default CLI behavior.
- Run the complete core, c1, prop-scoring, lifecycle, and synthetic-engine
  suites.

### Phase 5 — retire OANDA and Dukascopy frozen data — CODE_LANDED 2026-07-30

- Archive or mark blocked studies first. ✅ (`feed_divergence_2026-06` HOLD +
  BLOCKED banner; `oanda_stage1` already RETIRED; cold archive exempt)
- Delete OANDA and Dukascopy bytes. ✅
- Remove OANDA from `MANIFEST_DIRS`; regenerate affected manifests. ✅
- Update manifest tests and living restore instructions. ✅
- LTM tombstone:
  [`docs/ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md`](../ltm/notes/2026-07-30-oanda-dukascopy-data-tombstone.md)

### Phase 6 — consolidated documentation and completion

- Update root orientation docs and session log without rewriting historical
  bodies.
- Run §10 and the final full suite.
- Mark the explicit point of no return. Destroy the temporary offline byte
  copy only after a separate operator confirmation; after that action A–C are
  intentionally irreversible.

Each numbered phase lands in its own commit and may use its own PR. No later
phase begins while an earlier phase is red or ambiguous.

---

## §10 — Audit hooks

```bash
# Proposed ADR structure and graph
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

# Active Class-S explicit-tier bounded executions
OUT_DIR="$(mktemp -d)"
python3 lab/analysis/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_scoring.py \
  --n-sims 200 --out-dir "$OUT_DIR/scoring"
python3 lab/analysis/class_s_candidate1_scoring_2026-07-15/run_class_s_c1_regime_gate.py \
  --smoke --n-jobs 1 --out-dir "$OUT_DIR/regime"

# Full acceptance
python3 -m pytest tests/ -q
```

---

## Verification

```bash
# Mechanical authoring checks
python3 scripts/check_brief.py \
  docs/adr/2026-07-22-challenge-era-substrate-retirement.md --type adr
python3 scripts/check_adr_graph.py

# Rule-0 anchors
git log -1 --format='%h %ci' -- core/firm_rules.py
git log -1 --format='%h %ci' -- core/dd_protection.py
git log -1 --format='%h %ci' -- core/mc/modes.py
git log -1 --format='%h %ci' -- ops/accounts.py
git log -1 --format='%h %ci' -- tests/core/test_mc_anchors.py

# Scope evidence in this authoring PR: ADR/session only, no retirement executed
git diff --name-only origin/main...HEAD
```

Cloud-authoring caveat: the local vendor manifest and anchor-test checks cannot
pass in this clone because the gitignored CSVs and research dependencies are
absent. That is recorded as §0 evidence and deliberately routes destructive
execution to Phase 0 in the operator checkout; it does not permit assuming the
missing bytes were safely deleted.

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-22 | Initial `Proposed` ADR; full retirement scope requested, destructive acceptance gated on operator-side evidence | Joshua + Cursor |
| 2026-07-22 | Operator approval-in-principle recorded; status remains `Proposed` until mandatory D2/T2 and operator-checkout Phase-0 evidence return `RESOLVED` | Joshua |
| 2026-07-22 | **§4 condition 3 amended** — calendar lock on the 2026-08-08 D2/T2 date replaced by the substantive requirement it encoded: a *recorded* release of the Pepperstone panel from successor-diagnostic duty, from D2/T2 **or** a validated replacement diagnostic. Rationale: the date was a proxy for "nothing still needs these four panels"; binding on the proxy blocked the program on a calendar rather than on evidence, while binding on the substance preserves the protection (the panels are gitignored and unrecoverable) and lets Phase 0 resolve as soon as the release exists. Propagated to §4 FALSIFIED limb, §4 trigger schedule, §7 Phase-0 step 4, and §7 Phase-3 step 1. **Not** a weakening of the deletion gate: conditions 1, 2, 4, 5 are unchanged and all remain unmet. | Joshua (decision) + Claude Code (amendment) |
| 2026-07-22 | **`Proposed` → `Accepted`.** §7 Phase 0 returned `RESOLVED` — all five §4 pre-acceptance conditions met (anchor reproduced 6 passed/0 skipped; 15-file offline rollback copy verified 15/15 against tracked manifests; D2 released the Pepperstone panel; every A–E consumer dispositioned; baselines captured). Seven partial-supersession reverse edges added and `INDEX.md` regenerated in this same commit per §7 step 8, so the ADR graph is never left red. Authorizes Phases 1–6; **no phase has run and no vendor byte has been deleted.** | Joshua (decision) + Claude Code (recording) |
| 2026-08-23 | **Phase 6 docs landed.** Completion note + §10 cheap-subset evidence. Destroy-copy still operator-gated. No §2 edit. Offline rollback copy not destroyed. | Cursor Cloud Agent |

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
Recorded here as owed; not landed in this change.
