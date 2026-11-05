# First Passage: bounded context architecture
## Specification, implementation plan, then checkpoint contracts

**Status:** PROPOSED — documentation-only specification and plan. Implementation checkpoints have not been dispatched; this document does not ratify standing-instruction or policy changes.
**Prepared:** November 4, 2026, America/New_York.
**Inspected main:** `535494eecc32aa8f9276b999cf055bf46da91a21`.
**Budget interpretation:** approximately 250,000 tokens maximum **per checkpoint**, including investigation, implementation, verification, review, and corrections across all participating sessions.
**Program relationship:** extend the existing org-cleanup program; reuse its G1–G3 and P2 work rather than create competing owners.

## 1. Specification

### 1.1 Outcome

An agent should identify the applicable rules, current task owner, relevant code and evidence, and verification command without reading a repository-wide Markdown dump.

Success means substantially less routine context with the same authority, evidence access, and operational constraints. Total repository size is a secondary measure. A historical record may remain large and valuable while costing nothing in an ordinary task that does not need it.

### 1.2 Verified baseline and limits

The GitHub tree and selected file contents were inspected at the pinned revision. Runtime loading on Joshua's actual Claude and Codex installations has not been tested.

| Surface | Current observation | Meaning for this work |
|---|---:|---|
| Root `AGENTS.md` | 277 lines; 30,455 bytes | Already dense; reducing lines alone is insufficient |
| `STATE.md` | 187 lines; 33,734 bytes | Long lines and accumulated detail also affect orientation |
| `PIPELINES.md` | 122 lines; 10,313 bytes | Already under 200 lines, but above the existing 4 KiB target |
| `REPO_MAP.md` | 16,328 bytes | Contains a large generated script table; preserve its generator |
| Defined T0 proxy | 65,213 bytes | AGENTS + STATE + the configured 1,024-byte hook allowance; not an observed runtime measurement |
| Tracked Markdown | 1,143 files; 24,548,947 bytes | Tree metadata total; not a tokenizer measurement |
| Instruction hierarchy | Root `AGENTS.md` only | No nested AGENTS files in the inspected tree |
| Claude root shim | Absent by an explicit existing decision | Do not reintroduce `CLAUDE.md` by default |
| Search exclusions | `.rgignore` already excludes three cold trees | Extend cautiously; do not create competing ignore owners |
| Document budget enforcement | Existing checker, configuration and tests | Extend existing controls rather than invent a new subsystem |

The supplied **12.7M-token** estimate is not independently verified here. It may describe a different snapshot or include content outside tracked Markdown. Do not make success depend on that number.

There is already an approved target of **8,192 bytes for AGENTS**, **5,120 for STATE**, **4,096 for PIPELINES**, **14,336 for T0**, and **25,600 for T0 plus initial task orientation**. Reaching the normal T0 target would cut the current proxy by approximately **78%**.

The existing D5 fallback permits AGENTS at 9,216 bytes if required binding content does not fit. With STATE and the hook allowance unchanged, that totals 15,360 bytes; disclose the exception and reconcile the aggregate cap explicitly. Never report 14,336-byte compliance using that fallback.

### 1.3 Scope

Included:

- Meaning-preserving root and STATE thinning through existing G1–G3.
- Five small scoped instruction files: core, lab, ops, docs, scripts.
- A clearer retrieval table, task-oriented map entries and a short glossary.
- Better default search selection with an explicit cold-evidence retrieval route.
- One bounded catalog/capability navigation pilot.
- Extraction or refinement of a few repeatable workflows using existing skill owners.
- Focused checks and representative runtime retrieval exercises.

Excluded from this program increment:

- Strategy, risk, venue, capital, live-execution or research-acceptance changes.
- Reformatting, renaming or relocating pinned research engines, data, ports, manifests or frozen evidence.
- Bulk history deletion, Git history rewriting, branch cleanup or private archive migration.
- Physical code/test reorganization merely to obtain files shorter than 200 lines.
- A new vector database, retrieval service, repository-wide knowledge graph or extra governance layer.
- Updating every catalog or creating a skill for every routine command.

Actual archival and runtime retirement remain with their existing cleanup owners and release conditions.

### 1.4 Instruction and retrieval architecture

| Surface | Responsibility | What it should contain |
|---|---|---|
| Root `AGENTS.md` | Repository-wide contract and navigation | Short purpose; hard invariants; compact rule links; live posture; layer map; exact launcher commands; retrieval table |
| `STATE.md` | Current priorities and obligations | Short current rows with dated owner links; required parsable formats retained |
| Scoped `AGENTS.md` files | Local conventions and routes | Local boundary, relevant owners, commands, evidence/pin hazards, applicable tests |
| `REPO_MAP.md` | Code and ownership lookup | Capability → implementation → tests → owner; generated portions remain generated |
| `PIPELINES.md` | Current producer/consumer relationships | Current handoffs, evidence transitions and route status |
| `docs/operational_rules.md` | Full standing rule text | Canonical rules and stable aliases; loaded by relevant rule |
| Proposed `docs/glossary.md` | Terminology lookup | Brief definitions linked to owners; no new policy |
| Existing catalogs and ADR indexes | Evidence and decision discovery | Small entry surfaces; detailed bodies remain on demand |
| Existing archive guidance | Historical retrieval | Location, identity and retrieval procedure |
| Existing skills | Repeatable procedures | Trigger, inputs, bounded steps, output and validation |

**Instruction semantics:** scoped files add local requirements and may specialize conventions; their authored content must not weaken root safety, privacy, ownership or execution constraints. The generic phrase “closest file wins” is not a sufficient policy.

**Harness compatibility:** Codex's documented discovery builds the root-to-working-directory chain at startup. A session launched at the root must explicitly read the applicable subtree instructions before editing there; do not assume changing directories reloads the chain. Claude's current documentation supports native AGENTS loading under stated version/configuration conditions. Preserve the repo's AGENTS-only decision and test the actual installations. Optional Claude path rules should address demonstrated cross-cutting routing needs, with explicit path scopes and no duplicated policy body.

**Tests outside a subtree:** a change to `tests/core/`, `tests/ops/`, or a cross-layer test must retrieve the instructions for the behavior it exercises, even when those files are not ancestors of the test path. Root routing must cover this case.

### 1.5 Size and loading requirements

| ID | Requirement |
|---|---|
| S1 | Root target: approximately 150–200 readable lines and ≤8,192 LF-normalized bytes, subject only to the already authorized disclosed fallback |
| S2 | Retain all 42 `rule-0` through `rule-41` links required by the current G2 contract |
| S3 | Each new scoped file: target 40–80 lines; ≤3,072 bytes; local information only |
| S4 | Initial task orientation: T0 plus selected scoped/navigation content ≤25,600 bytes under the normal profile; deep evidence reads are measured separately |
| S5 | No root imports that expand all scoped files, operational rules, catalogs or history into every session |
| S6 | Glossary target: ≤30 initially evidenced terms and ≤6,144 bytes; ambiguous terms get an explicit owner-specific meaning |
| S7 | Add no unconditional Claude rule file. If path rules are needed, include valid path frontmatter and prove relevant/nonrelevant loading behavior |
| S8 | Existing byte ratchets only tighten for existing surfaces; add scoped-file caps through the existing budget configuration |
| S9 | Report source bytes, tokenizer/model-specific counts when available, and actual harness-loaded material separately |

The existing T0 checker counts a configured hook allowance, not captured hook output. Runtime acceptance must measure the output; a configured number does not prove actual compliance. Global instructions, skill descriptions, memory, tool schemas and worktree ancestor instructions must be identified separately so an apparent repository reduction is not mistaken for the entire prompt size.

### 1.6 Meaning and evidence preservation

Every removed instruction sentence must map to a canonical destination or an identified duplicate. An independently reviewable mapping belongs with the PR; do not publish another standing encyclopedia.

Preserve these known readers and contracts:

- The historical MC triple parsed by `ops/recall/guard.py`. **Recommended first release: keep the short literal in AGENTS.** Moving it is unnecessary for the size goal. Any later move requires the parser and its regression tests in the same change.
- Exact protected AGENTS headings, including Protection, Strategy Reference, Public-clone posture, Gate composition authority and Live-execution posture.
- Rule aliases, legacy anchors, seat-authority references, root-document liveness and STATE parser formats.
- Data-class restrictions, frozen controls and literal operator grants.
- Generated indexes, trial-accounting manifests, append-only dispositions, hash pins and frozen engine identities.

The root currently says it is the only agent instruction file. Replace that statement as part of the root change and amend its owning charter to allow **one canonical hierarchy**, retaining the decision against a second independently maintained Claude root.

Do not resolve conflicting trading or posture records by guessing during this cleanup. Route a discrepancy to its current owner; preserve the distinction between proposed, accepted, historical and current claims.

### 1.7 Retrieval design

Keep the root table to approximately 8–12 routes. Suggested rows:

| Agent needs | First route |
|---|---|
| Current task and obligations | STATE, then the named owner |
| Code ownership or dependencies | REPO_MAP, then the applicable scoped AGENTS |
| Data flow or pipeline handoff | PIPELINES |
| Tests, lint/checks or gate execution | scripts/README, launcher and gates.yml |
| Firm rules and frozen protection | core/AGENTS and canonical core owners |
| Discovery, preregistration or research disposition | lab/AGENTS, discovery owners and relevant catalog |
| Venue, deployment or monitoring | ops/AGENTS and the current route owner |
| ADR, evidence or catalog editing | docs/AGENTS and the owning generator/form |
| Domain terminology | docs/glossary |
| Historical or excluded evidence | docs/ltm/README and the appropriate archive index |
| Test-only change | Scoped instructions for the implementation under test |

For glossary candidates such as “rail,” “envelope,” “1R,” “N-SURV,” “locked,” “authorized” and “deployed,” retrieve the definition from its owner. This specification does not invent their project-specific meanings. A term without a verified definition stays unresolved or is omitted.

Maps should route to an owner in no more than two navigation hops on the acceptance cases. An authoritative body can still require substantial reading once located.

### 1.8 Cold content and capability slices

Search exclusion, model context loading, file permissions and Git tracking are separate mechanisms.

- Keep `.rgignore` as the current search-exclusion owner.
- Default search may omit proven historical bodies; explicit path reads and targeted `rg --no-ignore` searches must still work.
- A negative default search is not proof of absent historical evidence.
- Keep small archive entry points and current indexes reachable in ordinary navigation, even when bodies are excluded.
- Do not hide all `*.json`, `discovery_manifests/`, `lab/analysis/` or `docs/`. File format and age do not establish coldness.
- Do not use `.gitignore` to simulate context control. It does not remove already tracked files and can hide new required records.
- Do not add `.claudeignore` or resurrect Cursor configuration without verified support and actual use.

Prefer capability-oriented **navigation** first: connect a capability's existing implementation, tests, specification and evidence through a compact local entry. Physical relocation is a separate proposal only if a measured navigation failure remains and imports, frozen paths and hashes permit it.

### 1.9 Acceptance

Five acceptance clusters keep the program focused:

1. **Size and loading:** normal root/T0 targets met; scoped files within caps; runtime evidence distinguishes automatic content from explicitly read content.
2. **Meaning and authority:** sentence mapping reviewed; protected readers and literals preserved; no weakened privacy, live-execution or frozen-control requirement.
3. **Retrieval:** every representative task finds the right owner, implementation/test route and command; no operational decision uses a superseded record as current authority.
4. **Integrity:** no new broken links; generated sections reproduce; required project checks and doc-reader tests pass on the relevant head.
5. **Bounded maintenance:** a new ordinary task does not require updating several copies of the same rule; optional additions demonstrate value or are omitted.

## 2. Implementation plan

### 2.1 Integrate with the current program

Use this as an amendment/implementation view of the approved cleanup specification. The November 3 consolidation document was read as prior analysis, not treated as fresh proof of its old counts or unresolved PR statuses.

| Work here | Existing owner or relationship |
|---|---|
| Full rule destinations and stable aliases | G1 |
| Thin AGENTS and PIPELINES | G2 |
| Thin STATE | G3 |
| Skill consolidation and trimming | P1.7, P2.1, P2.2 |
| Historical retention and removals | Existing P1/P3 and retirement legs; not repeated here |
| Final measurements and ratchets | P3.6 |
| Nested instructions, glossary, retrieval exercises | Proposed additions to the same program |

The inspected open-PR snapshot includes #1016, #1026, #1032, #1036, #1037, #1038, #1043, #1063, #1080 and #1081, as well as #977. This is a coordination warning, not a diff review. Re-read current changed-file sets before claiming overlapping paths; titles do not establish scope. In particular, root/posture, STATE and bulk cleanup work already have concurrent proposals.

Preserve existing governance-lane serialization and per-PR ruling-class requirements. This planning request authorizes producing the spec and plan; it is not a claim that new instruction changes or all future merges have already been ratified. Prepare concrete diffs and review evidence before any required final approval.

### 2.2 Work order

1. Reconcile the existing program, live PRs and actual harness loading. Freeze the new scope and acceptance cases.
2. Establish canonical destinations through G1 before deleting detail from the root.
3. Implement G2, then G3 under their existing dependencies. Preserve the small parser-sensitive root content.
4. Improve retrieval and terminology.
5. Add each layer's scoped instructions and test actual discovery.
6. Narrow default search only after retrieval routes exist.
7. Pilot one catalog/capability improvement and refine a few workflow entries.
8. Run integrated retrieval acceptance and close measurements.

The earliest valuable release is **G1 + G2 + G3**. It does not wait for catalog splitting, skills work or physical code organization. If a standing dependency blocks one governance leg, continue only independent, disjoint work already in scope.

C5–C8 share the budget configuration, so their default execution order is sequential. Parallel drafting may be useful, but implementation cannot treat those footprints as disjoint. No parallel agent dispatch is required by this plan.

### 2.3 Token and iteration control

The budget is total checkpoint work, not a model context-window claim.

- Plan most checkpoints for **50k–180k tokens**. None is intentionally sized to use 250k.
- Count parent investigation, implementer work, reviewer work and corrections together. A second session or re-dispatch does not reset the allowance.
- For observable usage, count input and output across calls, including replayed/cached input; include separately reported reasoning usage. Where telemetry is unavailable, mark consumption estimated and keep extra margin.
- Treat 200k as a stop-starting-new-work threshold. Use the remaining allowance to finish the current check, preserve evidence and produce a bounded return.
- A checkpoint forecast to exceed 250k is split **before** further implementation. Splitting must not silently increase the existing parent program's authorized iteration or PR budget.
- Read an initial evidence packet of roughly 20k–35k tokens, then retrieve only the next required sections. Prefer a live working context below roughly 100k–120k; this is an operating target, not a platform limit.
- Preserve the existing limits on reviews and failed corrections. Budget for one substantive review and correction; further permitted rounds must still fit the checkpoint's total.
- Research trials K = 0. No new vendor, VM or hosting spend. Model usage still consumes the user's existing allowance.
- Dispatch and return summaries should normally fit within 2,000 tokens each. Link detailed evidence rather than copying transcripts.

The planned ranges below total **0.99M–1.66M tokens** across all 13 checkpoints if all are needed. These are planning estimates, not measured forecasts or an authorization to spend. Already completed work and no-op returns should reduce that total. The first four checkpoints total approximately **350k–560k**.

### 2.4 Common task contract

Before dispatch, replace each proposed footprint with an exact allowed-path list, current base SHA, canonical owner, and required check names. Unresolved destinations are a planning dependency, not permission to edit arbitrary files.

Each task must have:

- One concrete output and a decisive verification cluster.
- Current premises and an “already on main → return DONE with commit evidence” condition.
- Required inputs, allowed files, forbidden surfaces, dependencies and token allowance.
- One writer; reviewer chosen under the existing cross-agent rule.
- A return of DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED, with head SHA, diff summary, check records and remaining uncertainty.
- Independent revertability; dependent changes roll back leaf-first.

Task contracts remain provisional until their upstream output exists. Do not issue downstream execution prompts from today's path guesses.

## 3. Bounded checkpoints

All ranges include investigation, implementation, review and corrections. **Each has a hard ceiling of 250k tokens.** The following are proposed work units, not dispatched jobs.

| ID | Observable output | Planned tokens | Dependency |
|---|---|---:|---|
| C0 | Reconciled scope, baseline and frozen acceptance cases | 50k–90k | This specification |
| C1 | Canonical rule text ready to receive root detail | 120k–180k | C0; existing G1 prerequisites |
| C2 | Thin root contract and current pipeline map | 100k–160k | C1; existing G2 prerequisites |
| C3 | Thin current STATE with all obligations reachable | 80k–130k | C2; existing G3/owner-disposition prerequisites |
| C4 | Working retrieval routes and sourced glossary | 80k–130k | C2 |
| C5 | Scoped core instructions | 50k–90k | C4 |
| C6 | Scoped lab instructions | 60k–110k | C4 |
| C7 | Scoped ops instructions | 60k–110k | C4; current route owners resolved |
| C8 | Scoped documentation and tooling instructions | 60k–110k | C4 |
| C9 | Cold-content search policy with verified retrieval | 80k–130k | C4, C8 |
| C10 | One catalog/capability navigation pilot, or evidenced no-op | 90k–150k | C4, C6, C8 |
| C11 | Focused workflow entries and necessary path rules | 80k–140k | C5–C8; existing P2 dependencies |
| C12 | Integrated acceptance and final size report | 80k–130k | C3, C9–C11 |

### C0 — Reconcile the scope so that later tasks have stable inputs

**Owner:** planning/coordinator role. **Output:** one reviewed amendment and checkpoint manifest attached to the existing program.

Read the current cleanup spec, root charter, byte configuration and relevant open-PR diffs. Inventory instruction files, generated maps, known document readers and the proposed changed paths. Record actual Claude/Codex versions, launch directories, ancestor instructions and loading behavior on the environments that will use the result.

Freeze the representative cases in §4 before editing and record baseline retrieval paths. A local-only runtime probe must be routed to the operator's environment; absence here is an explicit unverified dependency, not a reason to claim compatibility.

**Allowed:** existing program spec/plan amendment and its attached evidence. No standing instruction rewrite yet.
**Acceptance:** one nonconflicting scope/ownership manifest; current SHA; baseline measurements; loading matrix; named frozen cases.
**Split trigger:** resolving unrelated cleanup disputes or reviewing all historical evidence. Return those to existing owners.

### C1 — Prepare canonical rule owners so that root detail can move safely

**Owner:** existing G1 author/reviewer pairing. **Output:** the G1 PR or an identified already-merged equivalent.

Use the current G1 contract. Preserve Rule 13 data-class requirements, machine-read headings, all full-slug anchors and the 42 short aliases. Produce a sentence/obligation destination table for the material C2 will remove.

**Footprint:** G1's exact existing allowlist, including operational_rules, its approved rule-0 migration, authorized inbound references and its byte cap.
**Acceptance:** G1's semantic mapping and focused reader tests; aliases resolve; document budget meets the current approved target.
**Out of scope:** root trimming, new policy, ADR-wide cleanup.
**Split trigger:** a new rule decision or unrelated ADR fold. Do not bury it in a wording change.

### C2 — Thin AGENTS and PIPELINES so that every session starts with a usable map

**Owner:** existing G2 author/reviewer pairing. **Output:** one root/navigation PR.

Retain protected headings, the short MC literal, required rule links, privacy requirements and current hard execution constraints. Move detail only after its destination exists. Add the compact start-here table and exact common launcher commands. Replace the “only instruction file” statement with the hierarchy contract and amend the owning charter under the integrated scope.

**Footprint:** AGENTS, PIPELINES, own budget rows, expressly named receiving owners and the root-charter amendment. No guard-parser refactor is needed in the recommended cut.
**Acceptance:** ≤8,192 bytes/approximately ≤200 lines for AGENTS, ≤4,096 bytes for PIPELINES; A-lit, root liveness and anchor checks; reviewed meaning map.
**Out of scope:** editing STATE, scoped files, changing posture authority.
**Split trigger:** meeting the cap would require changing a frozen reader or weakening a rule. Use the disclosed fallback or return the conflict.

### C3 — Thin STATE so that current obligations remain visible

**Owner:** existing G3 owner. **Output:** one STATE/archive PR.

Apply the existing roll conventions and owner-disposition dependencies. Keep unresolved obligations visible with owner links; archive narrative through the existing path. A date alone never discharges an obligation, including future-dated records already present in the repository.

**Footprint:** STATE, its existing archive pair, its budget rows.
**Acceptance:** ≤5,120 bytes; state-currency, sessions/queue and state-roll checks; every pre-change live obligation maps to a current row or its evidenced owner disposition.
**Out of scope:** inventing dispositions, editing the trading owners, changing date-parser formats.
**Split trigger:** required owner decisions are absent. Return a precise blocked dependency; do not extend or close them by inference.

### C4 — Build retrieval routes so that agents find owners without broad scans

**Owner:** navigation/documentation author. **Output:** one retrieval-map PR.

Add task-oriented entries to the non-generated portion of REPO_MAP and create a small sourced glossary only if no existing glossary can serve. Validate the routes introduced in C2. For each selected capability, identify implementation, tests, specification and evidence.

**Footprint:** REPO_MAP non-generated sections, proposed docs/glossary, necessary links from AGENTS/PIPELINES and relevant budget rows. Reserve these shared files to this writer.
**Acceptance:** routes resolve to canonical owners in at most two navigation hops on the frozen cases; every glossary definition cites an owner; no generated-table hand edits.
**Out of scope:** reading every ADR, rewriting catalogs, defining financial terminology from memory.
**Split trigger:** more than 30 terms or a route requires changing ownership instead of documenting it.

### C5 — Add core instructions so that shared-engine work respects its boundaries

**Output:** `core/AGENTS.md` and its verification evidence.

Cover core's import boundary; canonical firm-rule/protection owners; frozen parameter/data constraints; vendor-free tests; links to MC, lifecycle, ingestion and strategy ownership. Explicitly distinguish code ownership from live authority.

**Footprint:** core/AGENTS and its byte-cap entry; a related README link only if required.
**Acceptance:** ≤3,072 bytes; core and test-only probes retrieve the right owner and command; boundary and relevant documentation checks pass.
**Forbidden:** core Python changes, data, strategy sources, manifests and frozen engine files.
**Split trigger:** an instruction cannot be written without resolving a core policy dispute.

### C6 — Add lab instructions so that research context loads only for research work

**Output:** `lab/AGENTS.md` and its verification evidence.

Route discovery, preregistration, K accounting, evaluation order, instrument dispositions, costs and catalog updates to existing owners. Explain the distinction between current evidence, archived evidence and reproducible generated indexes.

**Footprint:** lab/AGENTS and its cap entry; no deeper file under lab/builder.
**Acceptance:** a research-disposition probe finds the required owner, instrument ledger, catalog and validation entry; ≤3,072 bytes; no changed frozen hashes.
**Forbidden:** preregs, results, manifests, research verdicts, builder inputs/code and private materials.
**Split trigger:** a proposed definition changes a research gate or threshold.

### C7 — Add ops instructions so that operations work finds the current route

**Output:** `ops/AGENTS.md` and its verification evidence.

Route instruments, venues, calendars, deployment, monitoring and retirement status. Keep current native execution and retired c1 evidence distinguishable. Scope local guidance without granting orders, host access or deployment.

**Footprint:** ops/AGENTS and its cap entry.
**Acceptance:** a native-route probe identifies its owner and limits, while a historical-rail probe labels retirement correctly; ≤3,072 bytes; public-clone restrictions preserved.
**Forbidden:** operational code/configuration, hosts, accounts, monitoring acceptance, calendars and private records.
**Split trigger:** current route owners disagree; return that conflict to the owning lane.

### C8 — Add docs and scripts instructions so that records and gates follow their owners

**Output:** the small governance/tooling instruction set, `docs/AGENTS.md` and `scripts/AGENTS.md`.

Docs explains canonical versus derived versus frozen records, indexes/generators, append-only history and retrieval. Scripts explains launcher use, gates.yml authority, fail-closed behavior, generated outputs and meaningful verification records.

**Footprint:** the two AGENTS files and their cap entries; relevant existing README links if needed.
**Acceptance:** a catalog-edit probe finds the generator; a gate-change probe finds gates.yml and the appropriate test; both files ≤3,072 bytes; no contradictory policy copies.
**Forbidden:** broad docs rewrites, new gate composition, CI reconfiguration and hand-edited generated indexes.
**Split trigger:** more than one new workflow or changes to checker semantics.

### C9 — Adjust cold search selection so that history stays retrievable

**Output:** a small, justified search-exclusion PR or a no-op finding.

Classify at most three additional cold path families. Inspect current readers, glob readers and archive entry points before adding exclusions. Keep an explicit, narrow force-search recipe and small discoverable pointers.

**Footprint:** .rgignore and the existing archive/search guidance; exact candidate families frozen at dispatch.
**Acceptance:** default search omits the selected historical bodies; explicit public-path reads and targeted no-ignore searches recover them; all frozen current-owner routes still pass.
**Forbidden:** .gitignore expansion, untracking/deleting files, blanket format exclusions, private-file reads, new ignore files for unused tools.
**Split trigger:** a candidate contains active obligations or required searchable indexes. Leave that family unchanged rather than broaden this task.

### C10 — Pilot one catalog/capability entry so that related work is discoverable together

**Output:** one measured navigation improvement, or an evidenced no-op.

Choose **one** public, active catalog whose routing fails or is unnecessarily expensive in the frozen baseline. Prefer section links and compact entries before sharding. If a split is justified, migrate its generator and consumers atomically; maintain entry identities and old inbound anchors or explicit redirects.

**Footprint:** one named catalog, its generator and tests, and tightly bounded inbound links. Use a local capability entry to join existing code, tests and owner records; no physical code move.
**Acceptance:** all original entries remain represented once; generation reproduces; lookups reach the same owners with less reading; relevant catalog/link tests pass.
**Forbidden:** multiple catalogs, frozen evidence moves, changing dispositions, relocating code/tests.
**Split trigger:** multiple consumers require unrelated rewrites. Stop at the measured proposal; dispatch a separate migration only after its own sizing.
**No-op:** if the existing entry already passes the retrieval budget, retain it.

### C11 — Refine repeatable workflows so that agents load procedures when needed

**Output:** one small workflow-routing PR.

Select at most three concrete workflows: gate execution, catalog/disposition update, and firm-rule validation. Extend existing skill/reference owners where they already cover the task. Add at most two new skill bodies only if there is no existing owner and repeated demand is evidenced.

Claude path rules are optional within this unit: add only small, validly scoped pointers where nested instructions do not adequately cover a cross-cutting file class. Do not duplicate full policies.

**Footprint:** exact selected skill/reference/adapter files, necessary .agents discovery pointers, any justified .claude/rules files, and relevant existing validation tests.
**Acceptance:** each trigger selects the intended workflow and command; irrelevant tasks avoid its body; skill references validate; scoped rules pass positive and negative load probes.
**Forbidden:** strategy-validation changes unless separately in scope; mass skill expansion; user-level release/sync; unconditional rule bundles.
**Split trigger:** more than three workflows, a required policy ruling, or unavailable release authority. Repository preparation and installed release are reported separately.

### C12 — Verify the integrated design so that reduced context does not lose correctness

**Output:** one final acceptance report and necessary existing-program closeout updates.

Run the §4 cases on the integrated revision in each supported harness. Record loaded instruction paths, initial orientation size, navigation hops, correct owner/test/command, and any historical retrieval. Compare with C0. Apply final byte ratchets using the existing checker.

**Footprint:** final program/PR evidence and existing budget/baseline rows that are justified by completed work.
**Acceptance:** all five §1.9 clusters pass; every frozen case succeeds; actual loading limits are disclosed; no new living-link failures; required integrated checks have valid completed records.
**Forbidden:** open-ended cleanup, a new dashboard/service, physical code reorganization or filling a failed case with additional unconditional context.
**Split trigger:** a failure needs a substantial new change. Return a bounded defect with its invalidated acceptance cases; do not silently enlarge closeout.

## 4. Representative verification cases

C0 freezes concrete public example paths and expected owner identities at its chosen base. These are navigation tasks, not authorization to perform the operational activity.

| Case | What the agent must find | Critical failure |
|---|---|---|
| Shared core fix | Owning core module, boundary and focused test | Editing without frozen-control awareness |
| Test-only core change | Applicable core guidance despite starting under tests | Assuming ancestor instructions cover the implementation |
| Research disposition | Preregistration/evaluation owner, K record, instrument ledger and closure route | Inventing a verdict or treating old rejection as automatic veto |
| Firm-rule validation | Canonical firm-rule owner and preflight | Copying a stale table from a skill or narrative |
| Native deployment question | Current route owner, authorization limits and monitoring evidence | Treating retired rail acceptance as native acceptance |
| Catalog edit | Canonical inputs, generator and check | Hand-editing a generated body |
| Gate change | gates.yml composition and appropriate tests | Maintaining a second gate list |
| Historical incident | Exact retained record/archive identity and targeted retrieval | Treating empty default search as no evidence |
| Multi-scope change | Both relevant instruction sets and their boundary | One subtree's conventions silently overriding global constraints |
| Unrelated small docs edit | Only relevant navigation/instructions | Loading the entire research/ops corpus to start |

For root, scoped and multi-scope tasks, capture startup loading separately from later explicit reads. Run positive and negative probes for any Claude path rule.

### Verification commands

Use the checkout's existing launcher. Portable forms for the confirmed entry points are:

```bash
python -I scripts/fp.py doctor
python -I scripts/fp.py check
python -I scripts/fp.py python scripts/check_doc_budgets.py
python -I scripts/fp.py python scripts/check_md_anchors.py --baseline scripts/md_anchor_baseline.txt
python -I scripts/fp.py python scripts/check_root_doc_liveness.py
python -I scripts/fp.py python scripts/check_skill_refs.py --all
python -I scripts/fp.py python -m pytest <task-specific-test-paths>
```

Windows equivalents use `.\fp.ps1`. These are launcher/verification entry points, not a replacement for gates.yml. Do not invent a separate lint command: name the applicable existing gate after checking its owner.

AGENTS changes include the existing A-lit reader tests. G1 and G3 retain their existing specialized tests. Docs-only work uses the existing docs-readers CI route; code changes retain required full-suite checks. Final acceptance follows the existing program's integrated check/test requirements. Do not repeat a completed expensive check unless the candidate, dependency, failure or acceptance requirement justifies it.

## 5. Decisions embedded in this proposal

1. Keep **AGENTS-only**, with one canonical nested hierarchy; do not restore a CLAUDE shim by default.
2. Keep existing G1–G3 budgets and ownership; add scoped navigation as an explicit amendment.
3. Preserve small parser-sensitive root statements in the first cut.
4. Improve search selection before considering movement of cold records.
5. Pilot a single catalog/capability entry; decline broad reshuffling without measured benefit.
6. Prefer existing workflows and references over increasing the skill count.
7. Defer physical code/test relocation and arbitrary code line caps.
8. Treat token budgets as total checkpoint expenditure, with a 200k stop-starting threshold and 250k ceiling.

## 6. Sources and evidence boundary

Repository links below are pinned to the inspected revision. Recheck changed owners at dispatch.

- [AGENTS.md](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/AGENTS.md)
- [STATE.md](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/STATE.md)
- [REPO_MAP.md](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/REPO_MAP.md)
- [PIPELINES.md](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/PIPELINES.md)
- [Approved cleanup program](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/docs/superpowers/specs/2026-10-28-org-cleanup-programme-spec.md)
- [Root-document charter](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/docs/adr/2026-07-16-root-doc-charter-dedup.md)
- [Byte budgets](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/scripts/doc_budgets.yml)
- [Budget checker](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/scripts/check_doc_budgets.py)
- [Search exclusions](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/.rgignore)
- [Launcher and gate entry points](https://github.com/Joshua-Asante/first-passage/blob/535494eecc32aa8f9276b999cf055bf46da91a21/scripts/README.md)
- Prior consolidation proposal, November 3 (operator-provided planning input): used for coordination concerns, not as current execution evidence. Its current repository owners are linked above.
- [Official Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md): root-to-working-directory loading at startup; documented 32 KiB default.
- [Official Claude memory/instruction behavior](https://code.claude.com/docs/en/memory): AGENTS support conditions, subtree loading and path-scoped rules.

No implementation tests or actual agent-runtime probes were run for this planning deliverable. The empirical claims here are repository observations, arithmetic and the cited documentation. Token estimates, new scoped-file budgets and retrieval acceptance thresholds are proposed design choices.

