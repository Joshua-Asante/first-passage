# Rule consolidation — step 1: inventory, 42 core rules, classification

**Status:** proposal for operator ruling. No rule source is edited by this plan; edits come in
later PRs after Joshua rules (§7).

**Question:** which of the repo's documented agent rules are still needed, and what ~42 core rules
state the rest? **Decision it changes:** what the consolidation PRs keep, absorb, move or delete,
and how "Rule N" citations resolve afterwards.

**Budget:** `Rule 2: which agent rules survive the consolidation and how Rule N resolves · STRATEGIC 3
constituent investigations (inventory; core-rule design; classification) · K=0`. All three ran; the
budget is at its bound, so this plan is the structured stop: spent 3/3, remaining 0, state below,
recommendation **stop and rule** (low-reversibility governance act; the ruling, not a fourth
investigation, is the next step).

**Base:** inventory read at `3feb596`; reconciled to `b8524d17` after #906, #907, #908, #909 and
#911 merged during the pass (§2.4). Seats: Claude coordinator; Codex reviews this PR
([Rule 5 below](#authority-review-and-orientation), ruling 2026-10-25).

## 1. Collision check

Open PRs at start (2026-10-25 04:45Z) were read for overlap; none edits a rule source for
consolidation. Recently merged work this plan builds on, not over:

| PR | Effect on this pass |
|---|---|
| #901 skills consolidation, #904 cost pre-gate report-only, #899/#902 credential deny rules and custody | Their results are the inventory's input; Requirement 5 and the universal cost gate are gone. |
| #907 Requirement 5 repoint, #908 cloud return destination, #909 delete superseded rule text | Merged mid-pass; reconciled row by row (§2.4). #909 already deleted 3 inventoried rows. |
| #911 Claude does not review its own work | Merged mid-pass; it is core Rule 5. |

## 2. Inventory and recount

### 2.1 How rules were counted

Each source was read in full by one extraction agent (27 chunks over 218 files). A **rule** is one
distinct standing directive that binds future agent work: an obligation, a prohibition, a
conditional permission, a gate or check, or a binding definition other rules depend on. Within a
chunk, a directive repeated in several places counts once (the other places are recorded). A
sentence that only restates a directive owned elsewhere is counted as a *restatement*. Rationale,
history, evidence and worked examples are not rules. For gates and hooks: one rule per `gates.yml`
gate, harness hook, `permissions.deny` group, git hook and seat-grant group. Rule text below is a
≤30-word paraphrase; no private values are quoted.

A cruder upper bound (regex for normative words, sentence by sentence) finds **4,271** normative
sentences across the same text sources, inflated by ADR narrative.

### 2.2 Counts by source

| Source | Files | Rules | Live | Restatements | Frozen-control | Mechanically enforced |
|---|---:|---:|---:|---:|---:|---:|
| AGENTS.md | 1 | 146 | 145 | 16 | 49 | 27 |
| operational_rules.md | 1 | 92 | 90 | 1 | 13 | 20 |
| Canon and methodology (canon, rule_0, regime gate, lifecycle, harvest, …) | 12 | 208 | 192 | 14 | 19 | 25 |
| Skills (22 skills, their references) | 36 | 838 | 826 | 63 | 95 | 98 |
| Gates, hooks, settings, seat registry, commands, workflows | 15 | 129 | 128 | 13 | 25 | 84 |
| Accepted ADRs | 134 | 1,775 | 1,398 | 127 | 332 | 268 |
| ADRs not Accepted, ADR INDEX/README/TOMBSTONES | 9 | 142 | 92 | 42 | 65 | 13 |
| Root docs (STATE, PIPELINES, REPO_MAP, README, load-bearing numbers, MC anchor history) | 7 | 133 | 120 | 24 | 33 | 19 |
| Rejected-candidates register (one re-proposal bar per entry) | 1 | 95 | 93 | 7 | 9 | 3 |
| Lesson registries (M- and E-lessons) | 2 | 178 | 150 | 13 | 19 | 10 |
| **Total** | **218** | **3,736** | **3,234** | **320** | **659** | **567** |

Not live: 212 unclear, 120 superseded, 108 discharged, 62 historical. Only 15% of rules have a
mechanical enforcer; the rest depend on an agent reading them.

### 2.3 The ~1,070 figure

At this grain the corpus holds **3,736** rules, about 3.5× the ~1,070 figure. The method behind
~1,070 is not recorded in the repo. The nearest reproduction is AGENTS.md (145) + operational_rules
(91) + skills (836) = **1,072** at the inventory base, which is the agent-facing instruction layer
without ADRs, registries and lessons; that match may be coincidence. Cutting differently: live,
non-restating rules in AGENTS.md, operational rules, canon and methodology, skills and gates number
**1,273**. The 2026-08-08
conventions audit counted ~188 binding items at a coarser grain (named rules only); the corpus now
carries 630 distinct numbered labels.

### 2.4 Reconciliation to HEAD

After the base, 16 inventoried files changed. Each was re-read at `b8524d17`: 588 rows present, 7
changed (Requirement 5 repoints, surface-allocation ADR rewording, task-routing return destination),
3 already removed by #909 (committed-handoff rule, GLM credential isolation, struck census rows),
and 5 new directives added (including #911's ruling). The classification had independently marked
all three removed rows for deletion. The appendix marks each change *at HEAD*.

## 3. The 42 core rules

One numbered list, Rule 0 to Rule 41. Each is one or two lines in AGENTS.md (§4.1) and links its
owner, where the detail it absorbs stays. Rule 0 (audit first), Rule 1 (small-cell variance prior,
numeral fixed by the [Rule 2 ADR §5.7](../../adr/2026-06-16-rule-2-budget-before-acting.md)) and
Rule 2 (budget) keep their numerals. Frozen controls (Rules 10–15) are pointers to their owners and
weaken nothing: dd_protection constants, locked parameters, Pine, the MC literals in AGENTS.md
(read by `ops/recall/guard.py`), and the live-execution, credential, private-data and public-clone
controls stay exactly as their owners state them.

The draft was classified against by 27 agents; their wording and scope feedback is folded into the
statements below without renumbering, so every row in the appendix still points at the right rule.
"Rows" counts the inventory rows that fall under each rule.

### Authority, review and orientation

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 0 — Audit first** | Read the production source or primary artifact before a claim, brief, decision or edit. Prior docs, memory, handoffs and self-consistent artifacts are premises to verify; load-bearing claims need code-resident checks; returned work is judged against its artifacts. | [`docs/rule_0.md`](../../rule_0.md); [operational_rules §8–§9](../../operational_rules.md) (§0 sub-rules); `verify-source`, `handoff-verify` skills | canon Rule 0; op-Rule 2, op-Rule 8 §0 sub-rules, op-Rule 9 citation chain; verify-source; handoff-verify Phase-0 and judging; brief-authoring Check 1 / Trap #3; fixture-test 'Rule 0 ext'; MVD assertions | none (MVD helpers and anchor fixture tests per claim) | 55 / 75 / 5 |
| **Rule 1 — Small-cell variance prior** | Small samples and short streaks are variance: no parameter, size, timing or signal change on them, no override of a valid signal on a narrative or forecast, and no regime overlay without a full INQHIORI investigation. | [INQHIORI canon](../../methodology/inqhiori-canon.md) (numeral fixed by Rule 2 ADR §5.7); [operational_rules §1, §4](../../operational_rules.md) | canon Rule 1; regime-gate 'Rule 1 extension' (partition permutation); op-Rules 1 and 4; E1 | none | 13 / 9 / 4 |
| **Rule 2 — Budget before acting** | Budget substantial work in one line — iterations by loop class, plus $ and K where it spends, never minutes; at the bound make a structured stop and never expand silently or weaken acceptance. | [Rule 2 ADR](../../adr/2026-06-16-rule-2-budget-before-acting.md); canon §15 | canon Rule 2 and corollaries 1–3; Rule 2 ADR §2, addenda; work-decomposition budget arithmetic | rule2-trip-log-liveness (audit tier) | 12 / 24 / 7 |
| **Rule 3 — The operator decides; grants are literal** | Direct operator instructions govern; a ruling, GO or record grants only what it states, and history, relays or other agents add none. Ratification, spend, deletion, retirement and irreversible acts are the operator's; a tool's or control's refusal is reported, never worked around; no value judgment waives a legal, capital, credential, private-data, verification or release control. | [AGENTS.md §Purpose, §Contribution, §Output efficiency](../../../AGENTS.md); [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md) (decision packets; approval bound to its object) | surface-ADR 'Rule 2 (approval bound to object)'; repo-hygiene Rule 1; 'no X granted' lines; tool-safety non-circumvention | guard_operator_acts (prompt), guard_shell_command | 46 / 51 / 13 |
| **Rule 4 — Seats, action classes and cards** | Act within the seat's grants and the card's authority block — cards only narrow and operator acts are never delegated; parallel workers keep disjoint footprints and single-writer reserved files; a frozen card's worker returns contradictions, not scope changes, as a pushed branch plus PR with a four-state status. | [surface-allocation ADR](../../adr/2026-07-14-cc-cursor-surface-allocation.md); [`scripts/seat_authority.yml`](../../../scripts/seat_authority.yml) | surface-ADR seat table, action classes, 'Rule 1 (card only narrows)'; work-decomposition atomic tests | handoff-authority, guard_operator_acts | 26 / 47 / 6 |
| **Rule 5 — A separate reviewer** | Claude does not review its own work: Codex is the separate reviewer and reviewer ≠ planner. A Claude-run review, panel or escalation pass informs the author but is never the review. | [surface-allocation ADR Addendum 2026-10-25](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-25--operator-ruling-claude-does-not-review-its-own-work); [scripts/README §Independent review](../../../scripts/README.md#independent-review) | reviewer ≠ planner; escalation item 2 (see ruling D3); M-42, M-46, M-47 | none (merging agent's obligation) | 5 / 6 / 0 |
| **Rule 6 — PRs and merges** | Land work by PR from a `codex/` or `claude/` branch; merge only pinned to a head whose Codex review is clean within three and whose checks are all green; never auto-merge, never merge a DRAFT/HOLD without an explicit lift, never rewrite pushed history you do not own; resolve a concurrent-session collision before pushing. | [surface-allocation ADR Addendum 2026-10-24b](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-24b--operator-rulings-conditioned-merge-go-and-credential-custody); [operational_rules §12](../../operational_rules.md) | op-Rule 12; repo-hygiene Rules 2–5; M-37; pr.merge grant | main ruleset (required check), guard_operator_acts, check_push_collision | 17 / 43 / 10 |
| **Rule 7 — Stop after two failed corrections** | After two failed corrections of one issue — this count overrides any per-skill bound — stop, summarize and restart cleaner on the named escalation lane; a PR whose three Codex reviews all found issues returns to its owner for a rewrite. | [AGENTS.md §Continuous improvement](../../../AGENTS.md); surface-allocation ADR escalation triggers | M-38, M-39; code-defect Phase 4.5; fable-method Step 5 | none | 2 / 12 / 0 |
| **Rule 8 — Orient and dedup first** | Start from STATE and the owning plan or record; before new research or a new artifact, search CATALOG In-flight, briefs INDEX, the instrument ledger and rejection bars and paste the literal output — an empty search proves nothing. | [operational_rules §8.8](../../operational_rules.md) (dedup-first ADR is rationale) | op-Rule 8.8 (sub-rule 8), op-Rule 10 dedup clause; dedup-first ADR | hookify advisor-dedup-first (prompt warning) | 19 / 11 / 3 |
| **Rule 9 — Name the question; pick the loop** | Before substantial work name the question and the decision it changes (pre-Q gate, D-S-A) and pick the loop tier — INNER, OUTER, STRATEGIC or GRAND — by reversibility, exiting to the owning skill lane. | [INQHIORI canon §1–§8, §14](../../methodology/inqhiori-canon.md); three-loop ADR | canon §2–§8, §14; three-loop binding ADR; Quintessentials (GRAND) | none | 23 / 51 / 3 |

### Frozen controls — point to, never weaken

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 10 — Live-execution gates** | Confirm host state first; arming an instance needs its own M1 RESOLVED; live spend needs M1 plus a per-session operator GO inside the signed ceiling; disarm before `armed_until`; orders, exits, cancels, deploys and host access only at operator direction; no discretionary manual strategy execution; venue compliance terms (Tradeify eval: native logic only) bind every deployment. | [AGENTS.md §Live-execution posture](../../../AGENTS.md); `c1-rail` skill; rail-GO, M1 and deployment-checklist records | AGENTS live-execution bullets; c1-rail invariants and authority table; op-Rule 3 (dormant) | c1_rail_arm interlock, m1-artifact-structure, guard_operator_acts | 33 / 104 / 28 |
| **Rule 11 — Rail operating invariants** | Fresh tag per payload; a send is not a fill; an unobserved side effect is IN_DOUBT and reconciled, never auto-retried; an unhealthy source emits nothing and an unknown request halts; exits, flats and disarms never wait while risk-adds halt on any unpersisted decision; recovery never restores authority; operation is attended. | c1 monitoring-maturity, S2/S2b daemon and incident-contract records | surface-ADR 'Rule 3 (IN_DOUBT)'; incident-contract Rules 9–10, §A12; c1-rail invariants | b1_payload fresh tag; rail and daemon tests | 12 / 101 / 21 |
| **Rule 12 — Credentials** | Act under the agent's own scoped credentials, never the operator's; hold no Fly or broker credential; reference secrets, never embed them. | [surface-allocation ADR Addendum 2026-10-24b B](../../adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-24b--operator-rulings-conditioned-merge-go-and-credential-custody) | AGENTS §Merges and credentials; dispatch_codex limits | settings.json permissions.deny, secret-shape checks | 6 / 17 / 1 |
| **Rule 13 — Private data and the public clone** | Never commit or quote account identifiers, P&L, locked-book backtest figures or parameter values, vendor CSVs, Pine or locked ports; read the private surface in place only and never pass it to an external service; the VM copy exception is the §60 addenda's alone. | [AGENTS.md §Public-clone posture](../../../AGENTS.md); campaign §60; visibility-transition ADR | op-Rule 9; campaign §60; visibility ADR redactions | staged-debris, pine-manifest, pine-pin-provenance, private-Pine-read test | 17 / 41 / 10 |
| **Rule 14 — Locked parameters and protection** | Locked parameters, allocations and Pine are immutable (Pine owns strategy parameters; `BASE_RISK` is the live sizing authority); dd_protection's constants and structure and the MC literals resident in AGENTS.md change only by pre-registration → re-MC → both-halves regime gate → admitting ADR; a lock is complete only when its skew audit has run and every consumer reflects it. | [AGENTS.md §Strategy Reference, §Protection](../../../AGENTS.md); [operational_rules §5–§6](../../operational_rules.md); [regime gate](../../methodology/regime_robustness_gate.md) (change-control order) | op-Rules 5–6; dd-protection ADRs; trade-csv-reconcile Rule 0; prop-firm Rule 7; skew-audit 'Rule 6' | _validate_protection_rule, pine-manifest, recall-guard test, lock_event_hook | 49 / 125 / 29 |
| **Rule 15 — Capital authorization is separate and revocable** | Lock, capital authorization and venue deployment are separate axes and each fact lives at one level (book, edition, deployment); an account holds one pre-registered book; decay permits only pre-registered de-risking and upward moves need their full gate chain; automation moves authorization down only, bar the sandbox lane; retirement needs operator GO; a de-scope is not escaped by renaming; neither a lock nor a result grants capital. | [`strategy_lifecycle.md`](../../methodology/strategy_lifecycle.md); lifecycle, venue-binding and book-segregation ADRs | lifecycle governance ADR; venue-binding axis; book segregation; shrinkage convention | lifecycle-consistency, core/lifecycle tests | 34 / 116 / 19 |

### Firms, venues, data and figures

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 16 — Firm rules: one source and a pre-flight** | Define firm rules once in `core/firm_rules.py` and import them; every tier carries `starting_balance`; run the engine pre-flight; an unsourced venue rule is flagged and blocked, never defaulted away; documented-but-unmodelled terms live in the prop envelope; a new firm needs an ADR and a re-MC when used. | [AGENTS.md §Firm Expansion](../../../AGENTS.md); firm-constants ADR; `ops/prop_envelope_default.md` | firm-constants single source; inactivity sourcing ADRs; prop envelope | prop-tier test, engine pre-flight | 15 / 49 / 15 |
| **Rule 17 — Venue facts: quote, source, date, scope** | Record venue obligations verbatim with source, date read and scope; silence on scope reads broad; never inherit a qualifier the source lacks; model discretionary or warning-first limits as enforced. | [operational_rules §13](../../operational_rules.md) | op-Rule 13 | none | 8 / 21 / 1 |
| **Rule 18 — Feeds are admitted, never assumed** | The canonical research feed is the CME TV exports; retired feeds and vendors stay retired and their retained data is historical only; a new feed needs an ADR and the feed-equivalence pre-flight; pre-filter and confirm run on one feed; geometry is feed-specific; research code never wires toward live execution. | TV-CSV feed-policy ADR; feed-equivalence spec; vendor retirement ADRs | Dukascopy, OANDA, Pepperstone, Databento retirements; sweep-engine same-feed rule | none | 24 / 39 / 17 |
| **Rule 19 — Vendor-data integrity** | Commit each SHA256SUMS delta with its data change; `bar_data` changes only by a fresh operator CME export; install hooks per clone and never use `--no-verify` as the standing path; verify non-regenerable bytes before removing them. | [manifest-integrity ADR](../../adr/2026-05-10-manifest-integrity-gate.md) | M-9, M-12, M-13, M-22 | data-manifests, guard_shell_command | 18 / 22 / 7 |
| **Rule 20 — Figures come from their owner** | Quote prop-tier figures through the load-bearing-numbers index and their owners: bust claims are EOD lower bounds unless intraday-honest, and published figures assume the inactivity barrier is off; never invent, hand-edit, extrapolate or transplant a figure — convert borrowed numbers and re-run MC; historical anchors are never live claims. | [`docs/load_bearing_numbers.md`](../../load_bearing_numbers.md) (index) and each figure's owner | M-29; AGENTS §Load-bearing numbers | none | 32 / 66 / 10 |

### Verification

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 21 — Report verification honestly** | Report command, interpreter, revision, actual result and record.json; a pass needs completed, exit 0 and stable source; disclose pre-existing failures; a form check is not semantic proof and an unexercised gate is unproven; a re-implementation reproduces its baseline before a delta counts; numbers that feed a gate are computed in code; an override is logged beside the honest result. | [AGENTS.md §Python environment](../../../AGENTS.md); [scripts/README verification evidence](../../../scripts/README.md#automatic-verification-evidence) | AGENTS §Python environment; external-mapping guardrail 2 | guard_open_verification_record | 25 / 50 / 3 |
| **Rule 22 — Use the checkout's launcher** | Run project Python through `fp` (doctor, test, check); never fall back silently to system Python; spawn with `sys.executable`; the CI substitution covers only the qualification timeout; add no dependency without operator instruction. | [AGENTS.md §Python environment](../../../AGENTS.md); [scripts/README launcher](../../../scripts/README.md#local-operations-launcher) | AGENTS launcher bullets; fable-method dependency bar | fp doctor | 5 / 9 / 0 |

### Research

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 23 — Pre-register; count K honestly** | Freeze criteria in their own commit before results; never rescue with post-hoc filters; declare K honestly (no splitting, informal exploration counts); every frozen gate is reachable and binding; frozen preregs and defaults change only by dated superseding record; results on viewed data are exploratory. | `futures-anomaly-discovery` skill; candidate-contract ADR; HARV same-units ADR | Discovery Rule 1 (declare K); op-Rule 8 prereg-freeze clause; gate-reachability lesson | sentinel prereg scan, register_search refusals | 65 / 152 / 30 |
| **Rule 24 — Verdicts from the pre-registered gates, in order** | Validate mechanically at the declared gates (DSR-at-K, net of costs, intraday-honest clock, placebo and temporal battery) in the evaluation-order sequence; dormant gates re-arm only on a dated operator GO; qualifying risk-control lock changes also clear the regime-robustness gate. | [evaluation-order ADR](../../adr/2026-08-30-evaluation-order.md); `strategy-validation` skill; [regime gate](../../methodology/regime_robustness_gate.md) (mechanics) | validation battery K-tiering; W4 dormancy; prefilter gate | none | 21 / 191 / 36 |
| **Rule 25 — Generation never blesses** | Discovery output and harvested strategies are candidates: state a mechanism before mining, admit external mechanisms only through harvest intake, carry the manifest and K into validation, and retire a channel at its liveness ceiling. | [`strategy_harvest.md`](../../methodology/strategy_harvest.md); `futures-anomaly-discovery` skill | Discovery Rules 2–3; harvest Requirements 1–4; concept-admissibility | none | 14 / 69 / 14 |
| **Rule 26 — Rejections bar re-proposal** | Re-propose a rejected candidate only with new mechanism evidence; route rejections by scope (instrument ledger or register); the register is additions-only and a bar binds once ratified and wired; every closure names its Registry line. | [`docs/rejected_candidates.md`](../../rejected_candidates.md); rejected-candidate-patterns and rejection-register ADRs | op-Rule 8.9; 95 registry re-proposal bars | closure-disposition, instrument-rejection-coverage | 35 / 130 / 7 |
| **Rule 27 — Instrument ledgers** | Read `ops/instruments/<SYM>.md` before the first run or edit on an instrument and append a dated disposition at the end; create on first touch, never backfill; keep its PROFILE block and cfg fingerprint current. | [operational_rules §10](../../operational_rules.md); ledger and instrument-profile ADRs | op-Rule 10 | instrument-profiles | 8 / 25 / 2 |
| **Rule 28 — Closures, falsifiers and audits** | Every closure carries a typed Iterate exit and naming a successor never opens it; falsifiers and kill thresholds never move — a fired one's remedy becomes due and dated verdicts are the operator's; retiring an input migrates or retires each falsifier it fed (an unreachable check is not a pass); programme audits run at their cadence. | [iterate-exit ADR](../../adr/2026-08-04-iterate-closure-exit-mandatory.md); [operational_rules §11, §17](../../operational_rules.md); `programme-audit` skill | op-Rules 11 and 17; ADR 'Rule 11' citations | closure-disposition, falsifier-reachability (audit) | 29 / 214 / 47 |

### Records and communication

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 29 — One canonical owner per fact** | Each fact has one owner; elsewhere link it or label a mirror; check and amend the owner before opening a new artifact; AGENTS.md is the only instruction file among five root guides; memory and retired surfaces are never owners; cite code by symbol, not line. | [operational_rules §7](../../operational_rules.md); root-doc charter ADR | op-Rule 7, op-Rule 8.10; 'Rule 7' citations in ADRs and skills | adr-graph (status rows), root-doc-liveness | 58 / 51 / 7 |
| **Rule 30 — Correct where the error is read** | Mark a withdrawal where readers meet it; frozen evidence gets an addendum and an upstream banner; sweep a withdrawn claim repo-wide by mechanism, not token, and re-read its consumers; recompute corrected numbers from source. | [operational_rules §14](../../operational_rules.md); `blast-radius` skill | op-Rule 14; brief-authoring Trap #7 | supersession-placement | 36 / 29 / 2 |
| **Rule 31 — Artifacts earn their place** | Keep an artifact only if it passes the retention test; classify deletion by execution, migrate every obligation and reader first, tombstone removed ADRs and pin incoming anchors, verify retrieval; never revive retired code by revert. | [operational_rules §16](../../operational_rules.md); ADR ceremony-tiering | op-Rule 16 R1–R5; Great Prune | docs-runtime-inventory (report-only) | 33 / 40 / 22 |
| **Rule 32 — ADRs only under the admission rule** | Create an ADR only when the admission test holds; Accepted needs a dated operator GO; an approved revision updates effective text and keeps the immutable prior; Proposed and DRAFT records decide nothing; the superseded record's header carries every supersession edge, wherever the ruling lives. | [ADR ceremony-tiering](../../adr/2026-08-08-adr-ceremony-tiering.md) | Trap #12 (revision part); superseding-ADR conventions | adr-graph | 43 / 17 / 12 |
| **Rule 33 — Cards, briefs, notices and lessons follow their form** | A card, committed or prompted, carries the full contract — check_brief form, named acceptance tests, authority block, 'Must run locally' when it applies; never retro-fit; observations route through the notice log; lessons are cited from their registry, not re-derived. | `brief-authoring` skill; surface-allocation ADR handoff contract; notice-log ADR; [lesson registries](../../methodology/lessons/) | brief-authoring checks and traps; handoff contract items 1–7 | handoff-brief-form, handoff-authority | 29 / 93 / 15 |
| **Rule 34 — STATE, SESSIONS and CATALOG stay current and thin** | STATE points to owners — at most five queue items, one-line decision bullets, current deadlines; SESSIONS is append-only; CATALOG and INDEX are generated, never hand-edited. | root-doc charter ADR; [operational_rules §7](../../operational_rules.md) STATE rows; catalog-hot ADR | op-Rule 7 STATE/SESSIONS rows | state-currency, sessions-*, lab-catalog, adr-graph INDEX sync | 13 / 39 / 6 |
| **Rule 35 — Fewest words** | Use the fewest words that meet the objective and link the owner; no 'not granted' disclaimers, but keep a verdict's limits on how it may be read; never trade away correctness or honest reporting. | [AGENTS.md §Output efficiency](../../../AGENTS.md) | AGENTS §Output efficiency | none | 4 / 10 / 0 |
| **Rule 36 — Subtract, then improve once** | Use the cheapest trustworthy evidence; add no ledger, form, approval layer, registry or tool without a decision; volume is not value; write a rule only after an observed failure and promote feedback only when high-severity or recurring; make at most one durable intervention per mechanism, at the cheapest layer; edit standing instructions only on request. | [AGENTS.md §Contribution, §Continuous improvement](../../../AGENTS.md); `agent-improvement` skill | surface-ADR 'Rule 4 (enforcement points)'; op Rule maintenance | none | 25 / 31 / 3 |

### Engineering and routing

| Rule | Statement | Owner (detail lives here) | Absorbs | Enforced by | Rows (abs / det / del) |
|---|---|---|---|---|---|
| **Rule 37 — Layer boundaries** | `core` imports no internal layer, `lab` and `ops` never import each other, and REPO_MAP owns placement; fix an illegal edge by placement, never by relaxing the contract. | monorepo-layer ADR; [REPO_MAP.md](../../../REPO_MAP.md) | layer ADR | boundaries, repo-map-layers | 7 / 23 / 3 |
| **Rule 38 — Gates and tooling** | scripts/gates.yml alone composes gates and report-only checks stay in the audit tier; checkers fail closed — empty input is never green and SKIP is never a pass — and match the storage form without self-matching; cited paths resolve; skills publish only by explicit release. | [`scripts/gates.yml`](../../../scripts/gates.yml); [scripts/README](../../../scripts/README.md) | gate tiers; skill lifecycle; path/link liveness | gate_manifest tier validation, skill-refs, path-liveness | 8 / 18 / 8 |
| **Rule 39 — Configuration as code** | Define reused configuration once and compose it, separate shared, variant and instance layers, validate the resolved configuration where consumed, and keep its identity through deployment. | [AGENTS.md §Configuration as code](../../../AGENTS.md) | AGENTS §Configuration as code | none | 6 / 5 / 2 |
| **Rule 40 — Root cause and contract first** | Name the mechanism before a fix — no band-aid default, broad except, retry or looser schema without a ROOT CAUSE / FIX / VERIFICATION block; design verifier and order/state code from an invariant table or state model. | `code-defect-debugging` skill §11 | M-38, M-39 (state-model-first); fable-method band-aid ban | none | 7 / 44 / 0 |
| **Rule 41 — Route, host and delegate deliberately** | Run cards in the cloud unless they say 'Must run locally'; always-on services run on an always-on host, which never implies unattended arming; split oversized work into gated child units; relays carry communication only. | `task-routing`, `work-decomposition`, `relay-skill` skills; [operational_rules §15](../../operational_rules.md) | op-Rule 15; c1 'Invariant 10 / Rule 15' | none | 7 / 94 / 0 |

### 3.1 What happens to the 3,736 rules

| Disposition | Rows | Meaning |
|---|---:|---|
| Absorbed | 944 | The core line, read with its owner, fully states it; the source sentence shrinks to a link or goes. 104 of AGENTS.md's 146 rows are here. |
| Kept as detail | 2,364 | Still needed but too specific for a core line (values, procedure steps, scoped exceptions, venue, campaign or instrument contracts, frozen terms). Stays at an owner under its core rule; 278 rows should move to a different owner (named in the appendix). |
| Proposed for deletion | 428 | No longer needed: superseded, discharged, executed, historical or tied to a retired surface, with the evidence per row. 3 are already gone at HEAD (#909). 240 carry plain evidence (§5, D9); 188 need a ruling (§5, D4–D8). |

Every deletion that touches a frozen control is in the ruling set, whatever its evidence.

## 4. Namespace scheme

**Recommendation:**

1. **"Rule N" means only the core list.** The 42 rules are stated in AGENTS.md under a new
   §Core rules, one or two lines each with the owner link; AGENTS.md prose that only restates them is
   cut to the link. No new document: AGENTS.md is already the only instruction file.
2. **Every other numbered thing loses the bare word "Rule".** operational_rules.md sections stay
   as detail owners, cited `operational_rules §N` (anchor, not numeral); the canon cites core rules;
   skill-local numerals become named checks — futures-anomaly-discovery "Discovery check 1–3",
   repo-hygiene "Hygiene check 1–5", trade-csv-reconcile "Reconcile check 0"; the surface-allocation
   ADR's "Rule 1–4" and the incident contract's "Rule 4a–12" become named clauses. The regime gate's
   "Rule 1 extension" is canon Rule 1 already and keeps that name. `Requirement N`, `Trap #N`,
   `Check N` and lesson IDs (`M-n`, `E-n`) are not "Rule" tokens and stay.
3. **Frozen records are not edited** (operational_rules §14). Old citations in dated ADRs,
   closures, preregs and SESSIONS resolve through one legacy map, kept at the end of
   operational_rules.md (where most legacy numerals originate):

| Legacy citation | Core rule |
|---|---|
| canon Rule 0 / `rule_0.md` | Rule 0 |
| canon Rule 1, regime-gate Rule 1 extension | Rule 1 |
| canon Rule 2 and corollaries | Rule 2 |
| op-Rule 1 (no macro override), op-Rule 4 (streaks are variance) | Rule 1 |
| op-Rule 2 (audit production code) | Rule 0 |
| op-Rule 3 (DXTrade contractValue, dormant) | Rule 10 (deletion proposed, D5) |
| op-Rule 5 (Pine owns parameters), op-Rule 6 (skew audit at lock) | Rule 14 |
| op-Rule 7 (one canonical owner) | Rule 29; its STATE/SESSIONS rows → Rule 34 |
| op-Rule 8 (§0 sub-rules) | Rule 0; 8.8 → Rule 8, 8.9 → Rule 26, 8.10 → Rule 29, prereg-freeze clause → Rule 23 |
| op-Rule 9 (Pine read in place) | Rule 13; citation chain → Rule 0 |
| op-Rule 10 (instrument ledgers) | Rule 27; dedup clause → Rule 8 |
| op-Rule 11 (retirement back-propagates), op-Rule 17 (audit checklist) | Rule 28 |
| op-Rule 12 (DRAFT/HOLD lift) | Rule 6 |
| op-Rule 13 (venue facts) | Rule 17 |
| op-Rule 14 (corrections where read) | Rule 30 |
| op-Rule 15 (always-on host) | Rule 41 |
| op-Rule 16 (retention, R1–R5) | Rule 31 |
| futures-anomaly-discovery Rule 1 / 2 / 3 | Rule 23 / 25 / 25 |
| repo-hygiene Rule 1 / 2–5 | Rule 3 / 6 |
| trade-csv-reconcile Rule 0 | Rule 14 |
| surface-allocation ADR Rule 1 / 2 / 3 / 4 | Rule 4 / 3 / 11 / 36 |
| incident contract Rules 4a–12 | Rule 11 |
| `Rule 0-T` (cited by three production tests, never defined) | Rule 21 — define once or retire (D10) |

4. **No new gate.** The repoint is one mechanical PR (`rg '\bRule [0-9]'` over living surfaces,
   checked against the map). If bare-numeral drift recurs, extend an existing checker rather than add
   one (Rule 36).

## 5. Rulings requested

Joshua decides; nothing below executes without the ruling. Recommendations are marked.

| # | Decision | Recommendation |
|---|---|---|
| D1 | Adopt the 42 core rules as worded in §3 | Adopt; wording changes welcome before the AGENTS.md PR |
| D2 | Namespace scheme and legacy map (§4) | Adopt |
| D3 | Rule 5 scope: does the pre-ratification refute-first pass (surface-allocation ADR escalation item 2, M-42, `pre-ratification-adversarial-panel`) remain a Claude-run gate before ADR, prereg and closure ratification, or is it now the separate reviewer's (Codex) job, with Claude panels optional input? | Codex's job; Claude panels optional (follows the 2026-10-25 rulings) |
| D4 | **C1 — Track B and the CrossTrade route for Tradeify** (62 rows): the 2026-10-16 checklist addendum superseded Track B for Tradeify, but the 2026-09-12 book-protection instance ADR still reads Accepted / Superseded-by none and AGENTS.md still calls Track B "suspended until 11-08" with the TB-I3 activation gate owed. Record the supersession in that ADR's header and AGENTS.md, delete the Tradeify-only rules (instance ADR, ORB R2 draft, venue-legality lane, incident option B, STATE restatements), and move the host-side activation gate to the personal-lane owner | Adopt |
| D5 | **C2 — retired venues, feeds and vendors** (31 rows): DXTrade (op-Rule 3), CFD and FXIFY execution lessons, Pepperstone panel warnings, Databento pull rules — delete, or keep dormant with a named re-arm condition | Delete; history stays in git and the archive |
| D6 | **C3 — lesson registries** (14 rows): retire the legacy promotion state machine and the per-lesson dollar-cost field (conflicts with the public-clone redaction); superseded lessons are tombstoned like any artifact instead of kept forever | Adopt |
| D7 | **C4 — MSL sourcing channel** (5 rows): the hard rung was met 2026-10-07; delete the channel's operating rules with the closing record | Adopt, with the closing record |
| D8 | **C5 and C6** (45 frozen-control rows each superseded by a named live owner; 31 other dormant, discharged or unclear rows) | Approve as a batch; veto any row by ID |
| D9 | The 240 deletions with plain evidence (superseded with owner named, discharged, executed, historical) | Approve as a batch; Codex review of the deletion PRs checks each |
| D10 | Contradictions that need a choice, not a repair: (a) CI write credential — the surface-allocation ADR §8 row keeps "CI grants Codex no write credential" while Addendum 2026-10-24b B keeps `claude.yml` write permissions; (b) op-Rule 6 logs every losing streak in SESSIONS while op-Rule 7 limits SESSIONS to judgment calls; (c) lesson promotion threshold — AGENTS "high-severity or recurring" vs lesson_capture "$ threshold or three firings"; (d) `Rule 0-T`: define or retire | (a) 10-24b governs; (b) streaks go to the instrument ledger, not SESSIONS; (c) AGENTS governs; (d) define under Rule 21 |

### 5.1 Rows behind D4–D8

Each row's evidence is from the classification pass; the full row also appears in Appendix A with
its location.

<details><summary><b>C1 — Track B and the CrossTrade route for Tradeify</b>: 62 rows</summary>

| ID | File | Rule | Evidence |
|---|---|---|---|
| ADR03-79 | `adr/2026-07-10-databento-research-stack.md` | Keep the TV-CrossTrade-NT8-Bulenox rail; reopen Nautilus-as-execution only if the operation leaves the prop-firm model for a direct-API broker. | Superseded in part by S1/S2 ADRs (header); Addendum 2026-08-29 calls the rail falsifier moot; §5 keeps Nautilus research-only. |
| ADR03-99 | `adr/2026-07-10-r6-nogo-futures-residual-disposition.md` | Do not stand up the CrossTrade/NinjaTrader-8/Rithmic rail for a closed book. | Superseded by rail GO 2026-07-17 (R6 Addendum 2026-09-01); closed-book deployment barred by AGENTS.md §Strategy Reference. |
| ADR04-76 | `adr/2026-07-12-prop-portfolio-four-friendly-firms.md` | Execute through attended automation on TV to CrossTrade to NT8 to Rithmic/Tradovate. | Route superseded by S2 daemon→listener ADRs and Tradeify native-only ruling 2026-10-12 (AGENTS.md standing consequences), the stricter live owners. |
| ADR06-15 | `adr/2026-07-17-c1-rail-build-account-registration-go.md` | Execute rail build steps B1–B7 in order; no step skips its predecessor. | Superseded by Track B supersession (checklist Addendum 2026-10-16) and AGENTS.md arm gates; B1-B6 done, B7 route barred at Tradeify. |
| ADR06-18 | `adr/2026-07-17-c1-rail-build-account-registration-go.md` | When CrossTrade ships Account Manager for Tradovate, apply the EOD-flatten and DD-guard settings as a re-add, not a re-decision. | CrossTrade route barred for Tradeify eval (route record 2026-10-12; Track B superseded 2026-10-16); personal-lane CrossTrade question still open. |
| ADR13-3 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Enter the re-expression lane only on a named Phase 1 venue-legality flag (force-flat, weekend/overnight hold, contract-cap breach), never on a performance result or hunch. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-4 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Change only the session bound (entry cut-off and forced flatten); carry every other parameter across byte-identical in intent and re-verify by diff. | Stricter live owner: AGENTS.md locked parameters immutable (no lane exception remains); applied edits recorded in guard spec §8; campaign closed 2026-09-10. |
| ADR13-7 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Re-run the full Phase 1 gate G1.1–G1.10 on each replacement with its own inventory, anchors, hashes and venue audit; never use the twelve-item delta read. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-8 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Drop the strategy if its replacement fails the gate or is not produced; never advance the venue-illegal original export. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-10 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Produce at most one replacement per strategy, counted from the first export against the verified D12 calendar; a second attempt is void and the strategy drops. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-15 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Add a no-trade block on early-close dates closing before the holiday-short deadline; a replacement relying on the deadline there is not venue-legal. | Lane obligation; campaign selection CLOSED 2026-09-10; Track B superseded 2026-10-16; Good-Friday exposure also recorded at campaign-state §12. |
| ADR13-16 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Do not use the lane for the dropped Q-TXG-1 swap-port exports; a mis-sized export is re-runnable only with corrected input under its own ruling. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-18 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Pass a replacement only with zero force-flat violations, zero Friday-to-Sunday holds, a diff matching guard spec §8 exactly and G1.1–G1.10 clear; otherwise drop, no third attempt. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-19 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Falsify the lane on process compliance only: bound differs from spec, diff exceeds §8, frozen re-export settings differ, or a second replacement; never on expected economic reordering. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-20 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Count a replacement as a cell of its superseded body's template, keeping the per-template contract count at five. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-21 | `adr/2026-09-03-venue-legality-re-expression-lane.md` | Count each replacement's Phase 1 cycle as a Rule 2 iteration against contract item 13; it is not exempt and the ceiling is unchanged. | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-56 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Do not let unaccepted execution-model drafts #368–#370 or historical #365 ratify this ADR, admit its row or satisfy any policy or activation gate. | Review boundary moot: Track B superseded for Tradeify 2026-10-16 (checklist addendum); instance not pursued; ADR header unchanged. |
| ADR13-59 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Record the instance's reference_mode as fixed trailing by this ADR, never dispatched via reference_mode_for_dd_type; TB-D0 must test that no code path resolves it so. | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-60 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | If the evaluation lock becomes reachable or book_policy and the registry disagree on reference_mode, halt the live path and re-admit under a fresh ADR; never edit. | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-62 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Record the per-leg response map as a book property in book_policy.BOOK_LEGS/TB-S1; the registry row carries only three variables; ORB's mode response replaces the multiplier there only. | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-65 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Apply the regime-robustness gate in full for a new POLICY_REGISTRY instance; state and ratify each deviation from its canonical procedure rather than assuming it. | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-66 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Build Part A from 100 resampled 6-month-block panels at original session length with rebuilt inner blocks; require p5 pass-rate ≥ the full-panel floor; keep close-call and sanity rules. | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-67 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Replace the H1+H2 path-count sanity check with source-session partitioning; keep full parent MC depth separately for full, H1 and H2; never substitute half depth. | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-68 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Freeze Part A's exact integer depth, budget calculation, block, RNG and percentile rules at TB-F1; TB-E1 is forbidden until a second dated operator addendum ratifies that depth, no placeholders. | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-69 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Evaluate each Part B half with a one-sided 95% upper failure bound ≤ 5%, never a statistic weaker than the gate's point criterion; no separate regime floor. | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-71 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Admit in two stages (TB-D0 executable admission after TB-E1's seal; TB-E2 qualification; TB-D2 plus GO reseal authorization); refuse the arm at every stage before T11. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-79 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Land the registry row only in TB-D0 after TB-E1's seal, with provenance naming both ratifications, the TB-E1 freeze date and FBR digest; otherwise git-revert it and record the deviation. | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-81 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Record the TB-D1 ORB operator GO before V1 binding, the live test and B7, and recheck it before n3; a withheld GO blocks. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-82 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Run image v1 as dry-run emit only; --arm must refuse while the GO artifact is absent. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-83 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Seal EF1 at B7 only when every shared component, including the size-vector hash, equals FBR, so the rail sizes with the qualified vector; otherwise no B7, recapture. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-84 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | On a failed sole n3, retire the row: closure supersedes this ADR, remove the row, redeploy an image without it before any later arm, never write the GO. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-85 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Write the TB-D2 decision record with digests and verdict labels only, at a docs/notes path outside the listener build context. | Stricter live owner AGENTS.md §Public-clone posture governs; TB-D2 record never written; Track B superseded 2026-10-16. |
| ADR13-87 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Reseal only if the build-context diff is exactly the GO path, shared/config digests equal EF1, non-GO image layers match v1 in order, and S is valid without activity. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-96 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | On seal invalidation (C10) void the seal and dependent n3 and stop for the operator; never auto-draw a replacement or combine results; continuation needs a new operator decision. | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-98 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Make each downstream packet (TB-P1/F1, TB-S3 R-L, TB-D0, TB-I3, TB-B7, TB-E2, TB-D2, TB-O1) state its §2a obligations; derive every summary from the acceptance trace. | Packet list is Track B's (superseded 2026-10-16); TB-I3/TB-O1 obligations already live in §2a; retention is the operator's call. |
| ADR13-104 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Do not let TB-I2 consume or TB-E1 seal evidence produced with pre-ruling book_policy laws; include book_policy's digest in FBR and pin the ruled Striker cap and Vanguard WATCH zero. | Spine evidence rule superseded 2026-10-16; tests/ops/test_book_policy.py still pins the caps, so dropping ADR text is the operator's call. |
| ADR13-105 | `adr/2026-09-12-tradeify-book-protection-instance-admission.md` | Keep the policy PR's merge separate from recording dated operator decisions; ratification addenda must name actual values and frozen evidence, never placeholders. | Pending second ratification belongs to the E1 spine superseded 2026-10-16; placeholder ban otherwise covered by Rule 3 literal grants. |
| ADRX-7 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | Treat the ORB R2 supersession ADR as deciding nothing until TB-D1 fills the Decision slot from TB-E1 and the operator's fresh GO is a dated addendum. | Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE); TB-E1/TB-D1 never fill. Withdrawing a PROPOSED ADR with unmet Retain-until is the operator's. |
| ADRX-10 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | Treat missing, incomplete or failed O-N/O-P (or O-N'/O-P') parity intake as BLOCKED capability-problem at the parity owner, not a failed book confirmation. | TB-E1 parity-intake BLOCKED classification; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE) ends the E1 spine. |
| ADRX-11 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | If a validly executed TB-E1 fails legality, n1, n2 or regime-gate Part A with ORB present, record not superseded and end the attempt: no runner-up, no re-run without ORB. | TB-E1 failure-terminal rule; Tradeify E1 spine superseded 2026-10-16 (checklist addendum); no TB-E1 will run under this ADR. |
| ADRX-12 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | On a passing sealed TB-E1, record digests and disposition and request the operator's fresh GO; a withheld GO is BLOCKED context-problem, never FALSIFIED. | TB-E1 pass/GO-request branch; E1 spine superseded 2026-10-16 and R-2 qualification declined 2026-10-19 (checklist addenda). |
| ADRX-13 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | Once accepted, void the acceptance if the sole n3 (TB-E2) fails any bound; re-pointing again needs a new frozen contract and new ADR. | TB-E2 voiding rule depends on an acceptance that cannot occur after the 2026-10-16 Tradeify Track B supersession. |
| ADRX-14 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | Do not fill a PASS/GO-request Decision without TB-E1's qualifying seal; no pre-E1, feasibility-screen or weighting-study evidence may fill either branch. | Decision-slot fill restriction for TB-E1 seal; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE); slot never fills. |
| ADRX-16 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | TB-D1 fills the slot after TB-E1 and before TB-V1 and the B7-sealed image; record the operator's GO as a dated addendum and add STATE's decision-index row. | TB-D1 fill and GO ordering before TB-V1/B7; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE); sequence not pursued. |
| ADRX-17 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | For the trail-free orb_mnq_fixed_stop_oso edition, read the export pin as O-0' (SHA OWED) and parity grounds as O-N'/O-P' on its frozen effective settings. | O-0'/O-N'/O-P' re-pointing for orb_mnq_fixed_stop_oso@Tradeify; Tradeify edition preregs superseded 2026-10-16 (checklist addendum). |
| ADRX-18 | `adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md` | Never relabel finite margin as zero; O-N'/O-P' margin follows the frozen settings and owed ORB finite-margin amendment, basis owed to the runtime owner. | Scoped to Tradeify O-N'/O-P' parity, superseded 2026-10-16; general never-relabel-finite-margin rule stays at runtime-interface plan :16. |
| ADRX-45 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Admit the bounded-exposure reservation only for one-contract entries carrying a native stop in one request, and only while CAP records single-call creation and first-fill activation. | Option B deferred (§A11, §A12.3), CrossTrade placeoso-shaped (§A1); route rejected for Tradeify evals; stricter live owner §A12 F1(c) halt-on-unknown. |
| ADRX-46 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | In exceptional mode, admit a risk-add only if held allowances, open exposure and the new request fit room-to-floor less reserve; no waiver restores exhausted room. | Option-B exceptional-mode admission deferred (§A11, §A12.3); F6 keeps no loss-room check; CrossTrade route rejected; ADR says deferred-not-deleted. |
| ADRX-47 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Admit a split multi-contract intent whole or not at all: reserve whole-intent capacity before the first child; loss allowance applies only in exceptional mode. | Rule 9' deferred (§A12.3); surviving split constraint owned by campaign §59 Ruling 5; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE). |
| ADRX-50 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | For any later option-B release, withhold acceptance until every UB-1 to UB-10 question has a written answer; §A12.3 replaced that gate only for the first release. | Acceptance gate for deferred option B only; moot once option B (ADRX-45/46/54/55/57/59) is removed; stricter live owner §A12 F1(c) halt. |
| ADRX-54 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | In exceptional mode, re-run the loss check before each admission after any new unknown, owned fill or terminal, equity update or stale input. | UB-9 exceptional-mode re-check deferred by ruling (§A12.3 L521, L527); option B dormant; CrossTrade route rejected for Tradeify evals. |
| ADRX-55 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Define the reservation as a conditional admission allowance, not a maximum loss; freeze formula, inputs, stale-data behaviour and calibration before production qualification; out-of-envelope values refuse binding. | UB-2 reservation definition deferred (§A12.3 L521) with option B; CrossTrade route rejected; first release uses F1(b) unbound charge. |
| ADRX-57 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Keep exactly one obligation record per child request in the account owner's existing attempt journal, never a parallel ledger, so no reservation is freed twice. | UB-10 deferred (§A12.3 L521) with option B; no first-release reader; CrossTrade-shaped route rejected for Tradeify evals. |
| ADRX-58 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | On option-B acceptance, give each named owner a dated addendum with the §A5 text; edit no owner text before acceptance. | Option-B acceptance propagation; B deferred, first release used reduced §A12.4 set applied 2026-10-05; moot unless option B returns. |
| ADRX-59 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Reject the narrowed-shape reservation if CAP cannot record entry-stop atomicity, a vendor mechanism can grow or unprotect exposure, or a one-contract request can fill in several prints. | Option-B narrowed-shape falsifier; B deferred (§A11, §A12.3) on CrossTrade CAP evidence; stricter live owner §A12 F1(c) halt-on-unknown. |
| AGENTS-53 | `AGENTS.md` | Treat Track B as suspended from 2026-10-13 until the 11-08 sitting or an operator ruling; the personal lane continues. | Superseded by deployment-checklist Addendum 2026-10-16: Track B superseded (not suspended) for Tradeify, branch (a) withdrawn; STATE row 1 agrees. |
| ROOT-12 | `STATE.md` | No production feed is selected or funded and nothing arms; provider-neutral prep and no-spend Q&A may proceed; provider-specific work and spend wait for source-independent gates and operator funding. | Track B source disposition; superseded for Tradeify by checklist Addendum 2026-10-16; AGENTS data-source/arming lines and self-funded ADR gates are stricter live owners. |
| ROOT-13 | `STATE.md` | Open CP-7 funding only after T00 GO-evidence, the bound equivalence spec and A9-PREP; its grant covers the provider adapter and emission-disabled shadow collection only. | CP-7 feed funding (#790) frozen by checklist Addendum 2026-10-13, Track B superseded 2026-10-16; checklist §4 CP-7 keeps the record. |
| ROOT-20 | `STATE.md` | Pass campaign ownership only by an execution-slices ledger handoff entry naming the successor; a coordinator ending without one returns the role to the operator. | Protected Full E1 (Track B) superseded for Tradeify by checklist Addendum 2026-10-16; campaign record §58 keeps the rule; operator default is Rule 3. |
| ROOT-21 | `STATE.md` | The operator retains ratifications, merges and operational GOs for the campaign. | Track B campaign superseded 2026-10-16; merge retention conflicts with surface-allocation Addendum 2026-10-24b merge GO; ratification/GO retention is Rule 3. |
| ROOT-26 | `STATE.md` | Dispatch implementation only with an approved card issued via the deployment coordinator. | O1 R1/R2 work frozen by checklist Addendum 2026-10-13 and Track B superseded 2026-10-16; card-based dispatch is Rules 4 and 33. |
| SKILL02-65 | `.claude/skills/c1-rail/SKILL.md` | Retired CrossTrade Alert History source-of-truth rule; any revived route needs its own source-of-truth rule. | Already retired 2026-10-24 by operator ruling; tombstoned at docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation; CrossTrade Tradeify route rejected. |

</details>

<details><summary><b>C2 — Retired venues, feeds and vendors</b>: 31 rows</summary>

| ID | File | Rule | Evidence |
|---|---|---|---|
| ADR01-3 | `adr/2026-04-17-dd-trigger-calibration.md` | Treat the queued post-challenge DD retune proposal as inactive; it is not current protection. | FXIFY challenge retired; AGENTS.md §Protection chain (pre-reg, re-MC, both-halves, ADR) is stricter and governs any retune. |
| ADR01-37 | `adr/2026-05-08-dd-trigger-c2-relock.md` | Reopen C0/C2 if rolling 6-month MC pass-rate falls below 95% for two consecutive windows; check quarterly via time_to_pass --regime-check. | Retired by 2026-07-11-challenge-era-claims-rescope.md Addendum 2026-07-22 (§D2); Pepperstone panel retired, check reports AMBIGUOUS-no-input. |
| ADR01-63 | `adr/2026-05-16-fxify-correct-timeout-semantic.md` | Revert to the 150-bday semantic and prior anchor pins if any falsifier limb fires: rule change, live idle run, quarterly drift, or anchor non-reproduction. | FALSIFIER-UNREACHABLE banner 2026-08-08: FXIFY closed, Pepperstone retired, PANELS_BY_BROKER empty; dormant falsifier on retired venue. |
| ADR01-88 | `adr/2026-06-04-lean-portfolio-meta-layer.md` | Re-arm the allocation meta-layer only if a producing edge-captured-ratio surface exists and an allocation decision cites it. | Meta-layer falsifier fired 2026-07-30; ECR engine journal_review.py retired 2026-07-11 (absent); OODA fallback skill retired 2026-10-24. |
| ADR01-92 | `adr/2026-06-04-lean-portfolio-meta-layer.md` | Label allocation changes projection-driven until a producing rolling ECR exists; never call them data-driven without it. | Producing ECR engine journal_review.py retired 2026-07-11 and absent; meta-layer dormant by discharge addendum 2026-08-14. |
| ADR01-93 | `adr/2026-06-04-lean-portfolio-meta-layer.md` | Trust an automated path with size only after per-strategy verification that it reproduces the backtest signal; pyramiders also need verified close logic. | ECR/Copygram/DXTrade route retired; superseded by M1 RESOLVED, per-session GO and campaign Phase 8 shadow parity gate. |
| ADR02-81 | `adr/2026-06-12-three-loop-methodology-binding.md` | Every telemetry alert or report names its consuming loop and cadence. | Plan T telemetry tied to Copygram/DXTrade estate retired 2026-07-11; lifecycle map row 4 keeps consumer-loop routing descriptively. |
| ADR03-36 | `adr/2026-06-30-no-manual-trading-cfd-retirement.md` | Reconsider manual execution only on a clean edge-captured ratio of at least 80% over six-plus weeks of system-faithful execution, never to recover P&L. | Unreachable: journal_review.py deleted with ops/live_journal 2026-07-11 (absent; 2026-08-02 note); directed orders now under AGENTS.md 2026-09-30 amendment. |
| ADR03-37 | `adr/2026-06-30-no-manual-trading-cfd-retirement.md` | Never log back into the idle FXIFY/DXTrade account to trade it discretionarily. | Superseded by stricter Addendum 2026-07-10: account closed, credentials removed (enforced by construction); §2.1 no-manual rule remains. |
| ADR03-39 | `adr/2026-06-30-no-manual-trading-cfd-retirement.md` | Weekly, download the idle DXTrade fills export and run zero_fills_attestation.py; any in-window fill is a no-manual breach. | Retired by Addendum 2026-07-10 item 3 (account closed); ops/live_journal tooling absent from tree. |
| ADR03-73 | `adr/2026-07-10-databento-research-stack.md` | Precede every Databento pull with a free estimate; pulls refuse above --max-cost; no exceptions for small pulls. | Superseded by stricter Addendum 2026-09-10 (no pulls or estimates at all); dormant spend control should Databento return. |
| ADR03-82 | `adr/2026-07-10-databento-research-stack.md` | Any Databento billing without a recorded estimate, or any pull over $25 without operator sign-off, freezes pulls and forces an audit. | Superseded by Addendum 2026-09-10: Databento retired, no pulls exist to breach; dormant billing control should the vendor return. |
| ADR04-5 | `adr/2026-07-11-challenge-era-claims-rescope.md` | Retain the multi-firm prop multiplier tooling and ACTIVE_FIRM=FXIFY as dormant-historical fixtures. | ops/accounts.py, ops/fxify_rule_validator.py absent; firm_rules asserts no ACTIVE_FIRM; Addendum 2026-09-01 left this clause's disposition to the operator. |
| ADR04-27 | `adr/2026-07-11-discovery-campaign-defaults-ratified.md` | Declare a per-campaign --max-cost total and check it against the summed estimate before any data pull. | --max-cost/estimate gate is Databento-shaped (lab/databento_fetch); Databento retired 2026-09-10, no replacement; dormant if a paid vendor returns. |
| ADR08-23 | `adr/2026-08-03-claude-md-futures-refocus.md` | Keep one aggregated era-closure pointer line for closed CFD/challenge-era decisions only; never delete it; new posture decisions get their own line. | AGENTS.md carries no era-closure line (grep empty); refocus Addendum 2026-09-01 ruled hook #3a historical-only; rule forbids own removal. |
| ADR10-141 | `adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md` | New data for this channel needs a cost dry-run and separate GO; a later construct re-attests this channel's own GO and cost even on cached paid bytes. | Databento retired 2026-09-10, no approved vendor; new spend stays operator act (seat_authority spend); cached-byte re-attestation reads as a routine permission the 2026-10-24 ruling deleted. |
| ADR11-19 | `adr/2026-08-16-deep-iteration-lane-charter.md` | Use parent-era Databento history for a long train side only after a mandatory cost dry-run, then operator GO, pull and panel manifest. | References retired Databento: retired and unsubscribed 2026-09-10, no replacement approved (AGENTS.md data source; Databento ADR addendum). |
| ADR11-38 | `adr/2026-08-16-deep-iteration-lane-charter.md` | Bar-schema Databento pulls need only the campaign's operator GO; tbbo or finer needs bar survival, explicit --max-cost and operator sign-off; an estimate never authorizes a pull. | References retired Databento pulls: retired and unsubscribed 2026-09-10, no replacement approved (AGENTS.md data source). |
| GATES-85 | `.claude/commands/lock-check.md` | Never treat the Pepperstone portfolio_mc CLI as the re-MC; use the vendor-free engine regression tests/core/test_mc_synthetic_engine.py. | Pepperstone panel map retired (core/mc/modes.py, ADR 2026-07-22 §2-C); vendor-free engine regression owned by AGENTS §Strategy Reference. |
| LESSONS-E-4 | `docs/methodology/lessons/execution_lessons.md` | Demote a promoted lesson only after 12+ months without its watch-point firing and once the structural condition producing it no longer exists. | Inoperative: 2026-08-14 freeze bars the 12-month clock; only E1/E2 promoted, feeder journal_review.py absent. Operator chose MARK-DORMANT over delete (2026-08-08 audit item 6). |
| LESSONS-E-10 | `docs/methodology/lessons/execution_lessons.md` | When a signal specifies a single entry size, execute one entry; do not re-enter on minor BB-touches within the held position, splitting one stop into many. | Manual FIRE-alert execution retired (ADR 2026-06-30; FXIFY closed 2026-07-10 addendum); but ADR 2026-07-11 §2 KEEPs lesson rules, so removal is operator's call. |
| LESSONS-E-12 | `docs/methodology/lessons/execution_lessons.md` | Log a one-line skip entry (date, strategy, alert tag, one-sentence reason) at the moment of skipping a signal, not reconstructed later. | Never-promoted candidate for manual signal skips, retired by ADR 2026-06-30; ops/live_journal skip surface absent; registry KEEP (ADR 2026-07-11) makes it operator's call. |
| LESSONS-E-14 | `docs/methodology/lessons/execution_lessons.md` | Keep the live indicator on the execution feed; never manually re-derive SL or size from a different-feed indicator during the fire window. | Names retired Alchemy/DXTrade (FXIFY closed 2026-07-10) and manual SL/size entry (ADR 2026-06-30); feed-specific geometry lives in Rule 18; candidate status unclear. |
| LESSONS-M1-50 | `docs/methodology/lessons/methodology_lessons.md` | Treat a deadline-capped challenge as a Sharpe race: compute the analytic edge-times-frequency versus barrier pass ceiling before commissioning a full first-passage MC. | No FIRM_RULES tier has a deadline cap (grep core/firm_rules.py); FXIFY anchor deleted Phase 4 (PR #572); a time-capped objective could return. |
| LESSONS-M1-51 | `docs/methodology/lessons/methodology_lessons.md` | Choose challenge exits by information ratio and time-to-target under the horizon cap, not by maximum positive skew. | Same as M-18 screen: deadline-capped FXIFY challenge is a historical fixture (core/historical_challenge.py); no current capped tier. |
| LESSONS-M2-24 | `docs/methodology/lessons/methodology_lessons.md` | When a half-panel split lands within two months of 2024-04-30, treat the H1/H2 spread as priors-shifting; never discount it as sample-size noise without a multi-boundary sweep. | Anchor is retired Pepperstone legacy panel (2026-08-02 retirement ADR); CME transfer unestablished; operator decides whether the 2024 inflection carries. |
| LESSONS-M2-26 | `docs/methodology/lessons/methodology_lessons.md` | If the 2024-boundary spread is verdict-deciding, consider a multi-boundary sweep (portfolio_mc --boundary-sweep) as a cheap falsifier even when only one boundary is specified. | --boundary-sweep is hard-wired to legacy GA-4 allocations, FXIFY swap and PRE_SHOCK_1R (core/mc/modes.py L896); Pepperstone panel retired. |
| LESSONS-M2-27 | `docs/methodology/lessons/methodology_lessons.md` | If a brief frames the spread as artifact-vs-structural, include at least three non-2024 boundaries with 18+ months per side, or document the narrowing. | Search-space bound serves only the retired-panel 2024 artifact-vs-structural question (Pepperstone retired 2026-08-02); operator decides transfer. |
| METHOD-188 | `docs/methodology/1r_estimation.md` | Flag the Striker initial-entry tail as a re-cal-trigger candidate at next MC pre-flight; look for layer-2 pyramid divergence at the 6-month live reconciliation. | Historical: CFD Striker legs withdrawn (ADR 2026-08-04 venue descope); AGENTS.md says no live book, so live reconciliation never fires. |
| OPS-4 | `docs/operational_rules.md` | If DXTrade is explicitly reactivated, verify contractValue=10 for DJ30 before any Striker trade. | DXTrade/CFD retired by 2026-06-30 ADR, FXIFY DXTrade closed 2026-07-10 (core/csv_parser.py); value 10 survives in core/strategies/CATALOG.md locked table. |
| ROOT-162 | `docs/rejected_candidates.md` | Formalize each pending direction as a full entry at its authoritative closure, removing its bullet; the pending list only shrinks and promoted entries never reappear. | All six pending bullets are CFD-era or options directions; CFD estate retired (ADR 2026-07-11 ops-cfd-estate-retirement), so their formalizing closures cannot occur. |

</details>

<details><summary><b>C3 — Lesson registries</b>: 14 rows</summary>

| ID | File | Rule | Evidence |
|---|---|---|---|
| ADR08-97 | `adr/2026-08-04-strategy-coldstore-phase-a.md` | Cold-store unused strategy Pine and lock/changelog/candidate docs under core/strategies/_archive/<family>/, keep hot CARD stubs and CATALOG, re-pin manifest path columns only. | Phase A executed (core/strategies/_archive/ present); live controls ADR08-99 and pine-manifest gate keep pins. |
| ADR08-103 | `adr/2026-08-04-strategy-coldstore-phase-a.md` | Any non-_archive .pine under the six watched family dirs after Phase A claims complete is incomplete delivery; whether candidates/ is exempt remains an open operator call. | Phase A delivered (_archive present); candidates/ exemption left as open operator call since Addendum 2026-09-01. |
| ADR09-117 | `adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md` | Do not reopen MNQDTL doors C1-C11, ORB-MNQ at Tradeify, either Striker leg, Aegis-6J admission, or any safety invariant. | Superseded: ORB/Aegis readmitted by operator selection 2026-09-10 and ORB route-native CANDIDATE 2026-09-25; remaining clauses held by withdrawal ADR, rejected_candidates. |
| ADR10-63 | `adr/2026-08-12-msl-sourcing-channel-ratification.md` | MSL is a named L2 sourcing channel; it does not clear the MNQBASE-1 bar by assertion; MNQ-scoped work clears it per candidate only under R-REQSCOPE. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-65 | `adr/2026-08-12-msl-sourcing-channel-ratification.md` | Harvest Req 1b/Req 2 do not bind MSL composition; candidates enter G0/explore-confirm discipline with Req 1a delete/flip, EM0-EM5 and TNEC-1 still binding. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR12-131 | `adr/2026-09-02-portable-edge-cultivation-campaign-objective.md` | Make the Confirm interval's first eligible bar strictly later than the founding-freeze commit; bars between the last source read and the freeze are excluded. | Campaign-scoped (§1.4) rule; campaign closed 2026-09-03b; candidate-contract freezes never adopted it. Operator decides whether to generalize. |
| LESSONS-M1-12 | `docs/methodology/lessons/methodology_lessons.md` | Before declaring a Pine strategy lock complete, read the locked source and confirm every signal condition has a paired alert() call, not only alertcondition(), inside the active-window guard. | Signal origin is the Python daemon (S2 ADR 2026-08-07); c1-rail skill invariant 9 (JSON-only alerts, re-pin) owns Pine alerts; legacy book retired. |
| LESSONS-M1-13 | `docs/methodology/lessons/methodology_lessons.md` | When alert() plumbing is missing at lock, halt the lock and patch it in the same session; never defer it to the next lock cycle. | Same as M-7 Rule: TV alert path not the live signal origin (S2 ADR); c1-rail invariant 9 owns Pine-edition alert changes. |
| LESSONS-M1-30 | `docs/methodology/lessons/methodology_lessons.md` | Apply every Pine parameter-lock change to both the strategy and indicator .pine, diff both for each changed parameter, and re-export both before declaring it complete. | Indicator .pine exist only in _archive (MANIFEST.sha256); accepted book is strategy-only (BOOK_SOURCES); locked params immutable and agents never edit Pine. |
| LESSONS-M1-31 | `docs/methodology/lessons/methodology_lessons.md` | Add 'update the indicator .pine alongside the strategy .pine' as a step of the params.toml same-commit workflow. | params.toml and scripts/validate_params.py absent; retired by docs/adr/2026-08-03-params-toml-gate-retirement.md. |
| LESSONS-M1-32 | `docs/methodology/lessons/methodology_lessons.md` | Do not read validate_params.py 0/0 as evidence the indicators are current when Pine is absent from the clone. | scripts/validate_params.py absent (ADR 2026-08-03); green-gate-is-not-coverage stands at M-27 and Rule 21. |
| LESSONS-M2-99 | `docs/methodology/lessons/methodology_lessons.md` | Apply Pine parameter-lock changes to both strategy and indicator .pine and re-export both to TradingView. | Superseded by stricter AGENTS.md: locked parameters immutable, never edit Pine; indicators only in _archive (MANIFEST); test_validate_params.py absent. |
| ROOT-179 | `docs/rejected_candidates.md` | The GC/MGC family bank is a permanent K-wall; never re-cite a dead harvest class under a different paper (Requirement 3 dedup-first). | 'Permanent K-wall' superseded: ADR 2026-08-04 made the family K-bank disclosure-only (strategy_harvest Req 3); no-re-citation bar survives in ROOT-178. |
| ROOT-195 | `docs/rejected_candidates.md` | Treat the four locked-book strategies as dedup targets pinned in the concept-intake gate's admissibility_contract.yaml locked_book block. | Concept-intake gate and admissibility_contract.yaml retired by ADR 2026-07-11 gen1-pipeline-retirement (validation/ absent); locked book is in core/strategies/CATALOG.md. |

</details>

<details><summary><b>C4 — MSL sourcing channel</b>: 5 rows</summary>

| ID | File | Rule | Evidence |
|---|---|---|---|
| ADR10-64 | `adr/2026-08-12-msl-sourcing-channel-ratification.md` | Non-index MSL cards proceed under the fade spec §2.1 framing (outside the 5th-leg SNAG domain), recording the framing per card in the door-check. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-68 | `adr/2026-08-12-msl-sourcing-channel-ratification.md` | Do not pick R-FRAMING per card by whichever reading admits it, or cite this ADR as evidence the channel works. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-69 | `adr/2026-08-12-msl-sourcing-channel-ratification.md` | The three MSL ruling names must resolve to identical elections in the MSL charter and this ADR. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-86 | `adr/2026-08-13-msl-slate-2-design-box.md` | Author MSL slate-2 cards inside the elected box (rr 2-3, target WR band, diffusion-frontier R, mandatory hard stop, k=1, no pyramiding), S2A first. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-88 | `adr/2026-08-13-msl-slate-2-design-box.md` | Do not open the eval-sprint/retry lane under the slate-2 election. | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |

</details>

<details><summary><b>C5 — Frozen-control rows superseded by a named live owner</b>: 45 rows</summary>

| ID | File | Rule | Evidence |
|---|---|---|---|
| ADR01-2 | `adr/2026-04-17-dd-trigger-calibration.md` | Fire DD protection at the C0 trigger (1.0% drawdown from peak). | Superseded by docs/adr/2026-05-08-dd-trigger-c2-relock.md (header Superseded-in-part-by); live DD_TRIGGER=0.015 in core/dd_protection.py L80. |
| ADR01-40 | `adr/2026-05-08-dd-trigger-c2-relock.md` | Pin the C2 MC anchor in tests/test_mc_anchors.py and tests/test_mvd_selfchecks.py. | tests/core/test_mc_anchors.py removed in substrate Phase 3 (2026-07-24) per docs/mc_anchor_history.md L3; synthetic engine test replaces. |
| ADR01-44 | `adr/2026-05-10-dd-protection-ulp-rounding.md` | Re-run MC after the ULP fix to confirm the C2 anchor; drift beyond tolerance triggers a separate C2 re-evaluation ADR. | Discharged by docs/adr/2026-05-10-mc-c2-anchor-ratification.md: re-run delta 0.00pp, GH#55 closed. |
| ADR01-45 | `adr/2026-05-10-dd-protection-ulp-rounding.md` | Audit other risk-control comparison sites for ULP defects (Pre-Q if three or more), re-evaluate historical state logs, and review the self-check epsilon. | #54 targets absent accounts.py, #56 absent dd_protection_state.json; issues in retired multi_firm_operations repo; #57 epsilon question still open (1e-4, L251). |
| ADR01-52 | `adr/2026-05-10-mc-c2-anchor-ratification.md` | Do not repin anchor tests to bitwise-identical post-fix values as ceremonial confirmation. | Anchor pin tests deleted in substrate Phase 3 2026-07-24 (mc-c2 ratification Addendum 2026-08-29); nothing left to repin. |
| ADR01-72 | `adr/2026-05-23-allocation-refresh-2.md` | Under the no-version-bump doctrine, a version label (v4.5, v1) denotes whatever the current Pine production parameters are. | Contradicted by stricter AGENTS.md §Strategy Authorization Lifecycle (locked parameters immutable) and pine-manifest pins; doctrine status unclear. |
| ADR01-73 | `adr/2026-05-23-allocation-refresh-2.md` | Treat the refresh-2 MC anchor as the canonical calibration reference, pinned by tests/test_mc_anchors.py. | Superseded by AGENTS.md §Strategy Reference (historical record, not live claim) and mc_anchor_history.md L3; test pins deleted 2026-07-24. |
| ADR01-74 | `adr/2026-05-23-allocation-refresh-2.md` | Invalidate the allocation and revert both strategies to the documented prior config if the regime-check or live edge-captured-ratio limbs fire. | All three limbs dark (Addenda 2026-07-01/08-02); operator accepted absence 2026-08-15; re-arm needs fresh Pre-Q remap. |
| ADR01-83 | `adr/2026-05-23-allocation-refresh-2.md` | If a Pine parameter shift occurs without written motivation, trigger a methodology audit of silent parameter drift. | Superseded by stricter AGENTS.md locked-parameter immutability and pine-manifest gate (core/strategies/MANIFEST.sha256) blocking silent Pine drift. |
| ADR01-95 | `adr/2026-06-04-lean-portfolio-meta-layer.md` | Decide kill-switch design (coded circuit-breaker vs human pause) consciously via an inqhiori Pre-Q before any automated path carries size. | Q-KILLSWITCH never opened (only this ADR mentions it); c1 arming/disarm and per-session GO controls now govern. |
| ADR02-31 | `adr/2026-06-06-firm-constants-single-source.md` | Keep each change to a P0 locked core module in its own isolated diff and lock cycle; never bundle it with refactors or another P0 change. | Forbidden move scoped to this ADR's own derivation edit, deleted in Phase 4; AGENTS §Protection owns stricter frozen-control change-control. |
| ADR03-51 | `adr/2026-07-01-guardian-pyport-public-tracking.md` | Untrack the Guardian signal port and its test, hash-pin them, and keep generic engine/driver files tracked. | Discharged: .gitignore L137-144 untracks both files; pine-manifest checks PORT_MANIFEST; AGENTS.md §Public-clone posture is the live rule. |
| ADR03-54 | `adr/2026-07-01-guardian-pyport-public-tracking.md` | Leave the parameter-transcription class (LOCK.md blocks, specs) to the operator's Forward decision; do not redact it unilaterally. | Superseded by 2026-08-14 repo-public-visibility-transition ADR: §2.6 Forward question resolved toward redaction. |
| ADR03-55 | `adr/2026-07-01-guardian-pyport-public-tracking.md` | If a port's local copy is lost or unverifiable, revert to tracked-with-exception; after two tracked-port incidents, escalate to a mechanical port-manifest gate. | Revert-to-tracked conflicts with stricter AGENTS.md §Public-clone posture; escalation branch done (check_pine_manifest.py covers PORT_MANIFEST). |
| ADR03-94 | `adr/2026-07-10-r6-nogo-futures-residual-disposition.md` | Self-funded Aegis-to-M6J is the sole active scale lane; its lane authorization is not a live-start authorization. | Superseded by 2026-07-16 self-funded-lane-close ADR (lane closed, b1 PARK), stricter than the lane authorization. |
| ADR04-3 | `adr/2026-07-11-challenge-era-claims-rescope.md` | Run the quarterly C2-to-C0 revert check only as a historical-semantics diagnostic until D2 is resolved. | Retired by this ADR's Addendum 2026-07-22; stricter live owner is the dd-protection concept-not-constant pre-reg→re-MC→both-halves→ADR chain. |
| ADR04-11 | `adr/2026-07-11-challenge-era-claims-rescope.md` | Do not delete or weaken the anchor test pins or the lock-criteria test; keep them as engine-regression pins. | tests/core/test_mc_anchors.py absent; AGENTS.md names vendor-free successor tests/core/test_mc_synthetic_engine.py; frozen-MC-adjacent, so operator call. |
| ADR04-15 | `adr/2026-07-11-challenge-era-claims-rescope.md` | Do not quote the 2026-08-08 historical-semantics diagnostic output as a live pass-probability. | Diagnostic retired by Addendum 2026-07-22 (2026-08-08 carries no run); §2.1 and Rule 20 already bar quoting anchors as live. |
| ADR04-31 | `adr/2026-07-11-gen1-pipeline-retirement.md` | Keep this subsystem retirement out of core/, Pine, locked constants and the MC anchor. | One-off scope executed (bdc45a3/PR #317 per Status line); Rule 14 and AGENTS.md §Protection remain the stricter live owners. |
| ADR05-107 | `adr/2026-07-14-cc-cursor-surface-allocation.md` | Run GLM workers without the operator's merge-capable gh credential or Fly configuration, as a separate user or sandbox. | Superseded: GLM dropped by Addendum 2026-10-24; stricter live custody for all agents in Addendum 2026-10-24b B (scoped PAT, no Fly credential). |
| ADR06-12 | `adr/2026-07-17-c1-rail-build-account-registration-go.md` | Never switch ACTIVE_FIRM; run engines on tier configs directly. | Superseded: ACTIVE_FIRM deleted (substrate Phase 4, PR #572); tests/core/test_firm_constants_single_source.py asserts absence; ADR06-101 owns explicit-key selection. |
| ADR06-87 | `adr/2026-07-22-c1-venue-native-monitoring-maturity.md` | Revisit the item-5 deletion decline after 4 qualifying attended Stage-1 sessions without discharge; never auto-delete or relax; elapsed date is not a fired review. | Discharged: item 5 recorded in M1_MONITORING_ACCEPTANCE.json, status RESOLVED 2026-09-14; trigger could re-apply to a new instance's M1. |
| ADR06-92 | `adr/2026-07-22-c1-venue-native-monitoring-maturity.md` | If a third armed session occurs with M1 unresolved, make c1_rail_arm --arm refuse unless the acceptance artifact reads RESOLVED. | Discharged: ops/c1_rail/c1_rail_arm.py now calls validate_m1_acceptance(require_resolved=True); AGENTS.md states the interlock. |
| ADR06-94 | `adr/2026-07-22-c1-venue-native-monitoring-maturity.md` | Read a non-empty arm-interlock hook as 'a gate exists', not as validation of the acceptance artifact. | Superseded: c1_rail_arm.py validates the artifact with require_resolved=True; AGENTS.md §Live-execution owns the current interlock-scope caveat. |
| ADR06-111 | `adr/2026-07-22-challenge-era-substrate-retirement.md` | Accept the retirement only after operator-checkout anchor reproduction, offline rollback inventory, recorded panel release, consumer dispositions and baselines. | Discharged: Phase 0 returned RESOLVED 2026-07-22, all five §4 conditions met (ADR Status line). |
| ADR07-9 | `adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md` | Close the corrected-geometry WATCH-1 reduced-risk full-panel reference before B7 arms. | Discharged: CORRECTED_FULLPANEL.md published (ARCHIVED.json class_s_c1_haircut_regime_remc_2026-07-16; cited in rung ADR figure caveat 2026-08-06); WATCH-1 Striker book barred since 2026-08-04. |
| ADR07-77 | `adr/2026-07-27-tv-agent-browser-access.md` | No unattended agent TradingView access during the locked live signal window; attended access is fine. | Subsumed by same ADR's stricter §5 ban on all unattended TV automation (ADR07-75); S2 fork moved signal origin to the Python daemon. |
| ADR08-24 | `adr/2026-08-03-claude-md-futures-refocus.md` | Keep the Strategy Reference table byte-intact and machine-pinned as the locked legacy book while trimming root docs. | Superseded by Phase C ADR 2026-08-23 (CLAUDE table retired); live owner core/strategies/CATALOG.md §Locked parameter record. |
| ADR08-101 | `adr/2026-08-04-strategy-coldstore-phase-a.md` | If any moved file's SHA-256 differs from its pre-move manifest digest, halt moves, restore from snapshot and supersede. | Phase A moves complete; window was its move commits; pine-manifest gate still hash-checks MANIFEST.sha256 pins. |
| ADR08-102 | `adr/2026-08-04-strategy-coldstore-phase-a.md` | Revert any BASE_RISK, lifecycle, LEG_MAP or Pine-parameter change in a PR citing only this ADR; check every such PR until Phase C admits. | Check window closed at Phase C admission 2026-08-23; general ride-along ban survives in refocus ADR §5-1 (ADR08-25). |
| ADR09-47 | `adr/2026-08-07-loop-s1-environment-ratification.md` | Agents may not place trades; token trades for account activity stay operator-only. | Superseded by operator Addendum 2026-09-30b (live owner, restated as ADR09-46); S1 header 2026-10-01 marks it historical. |
| ADR09-154 | `adr/2026-08-08-s2b-signal-daemon-build.md` | On incident, the listener performs qualified risk-reducing recovery dispatch for the fixed four-leg book (rev8). | Superseded by S2b Addendum 2026-09-15 rev9 attended recovery (stricter live owner; header says rev9 replaces rev8 dispatch). |
| ADR10-91 | `adr/2026-08-14-repo-public-visibility-transition.md` | Go public via fresh-repo transplant after remediation (scrub, redact, untrack, LICENSE), archive the private repo, repoint clones. | Executed one-time transplant: 'Initial public release' 027a7295 (2026-08-14), Accepted 2026-08-22; live owner AGENTS.md §Public-clone posture. |
| ADR10-97 | `adr/2026-08-14-repo-public-visibility-transition.md` | Exclude docs/notes/**, docs/ltm/** and docs/superpowers/** from the public seed tree wholesale. | One-time seed exclusion executed 2026-08-14; docs/notes, docs/ltm, docs/superpowers now tracked; AGENTS.md §Public-clone posture governs content. |
| ADR10-100 | `adr/2026-08-14-repo-public-visibility-transition.md` | Ship LICENSE with the first public commit and seed a genuinely separate repo, not a renamed or toggled one. | Executed: LICENSE in initial public commit 027a7295; separate public repo seeded; live owner AGENTS.md §Public-clone posture. |
| ADR13-122 | `adr/2026-09-14-a7-attended-agent-capture.md` | Keep M1 acceptance unchanged until A8 obtains the actual evidence and dated signoff. | Discharged: A8 signed acceptance 2026-09-14; live owner docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json reads RESOLVED. |
| ADRX-52 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Stop risk-adds on all legs when monitoring or broker evidence is stale or a failed stop/unexplained exposure is open; restoration alone never resumes trading. | D5 (2026-10-02): UB-3 not carried as text; superseded by stricter §A12.5 stale-evidence latch (session-closed admission), F5 and T13/D-MON. |
| ADRX-66 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | Perform R-1/R-2 REST reads operator-only, read-only, after entitlement confirmation; no purchase, new access, route change or order mutation. | R-1 discharged 2026-10-01, R-2 closed with limits 2026-09-29 (§A12.5 UB-7 row); spent permission; AGENTS.md live-execution bars remain stricter. |
| ADRX-68 | `adr/2026-09-17-bounded-platform-protection-incident-contract.md` | No agent places, amends or cancels an order. | Superseded by surface-allocation Addendum 2026-09-30b; this ADR's L3 clarification marks it historical; frozen-adjacent, so operator's call. |
| AGENTS-50 | `AGENTS.md` | A licensed test strategy may discharge M1 item 5 / B7 Stage 1 independently of strategy selection. | Incumbent M1 RESOLVED 2026-09-14 (A8) via option-D attended input (M1 addendum 2026-09-11), not the licence; reuse for new instance is operator call. |
| ROOT-16 | `STATE.md` | Obtain a CP-3 before each further route-commissioning row. | X-3/X-4 commissioning rows not pursued per checklist Addendum 2026-10-16; branch (a) restart-under-CP-3 withdrawn; checklist §4 CP-3 retains the term. |
| ROOT-32 | `STATE.md` | T08 drills and R-1/R-2 reads are operator-performed; each drill returns as an individual operator decision. | T08 and route drills superseded for Tradeify by checklist Addendum 2026-10-16; incident ADR §A11.1 keeps the record; AGENTS operator-direction rule covers orders. |
| ROOT-36 | `STATE.md` | Count an X-3 or X-4 drill fill toward the preservation obligation in the week it fills. | X-3/X-4 drills superseded for Tradeify (checklist Addendum 2026-10-16), so drill-fill counting is moot; drill plan §2.0 keeps the ruling. |
| ROOT-236 | `docs/mc_anchor_history.md` | Opportunistically re-test the Q-SWAP-4 structural follow-up at the next allocation-refresh ADR. | Q-SWAP domain retired on SNAG exhaustion (mc_anchor_history §Q-SWAP); legacy book has no live venue (AGENTS); no allocation-refresh ADR is expected. |
| SKILL02-51 | `.claude/skills/c1-rail/SKILL.md` | Agents may fly deploy the listener or signal-daemon app only after all six deploy pre-conditions, scoped per app. | Superseded: seat_authority.yml rail.deploy is an operator act; ADR 2026-10-24b B: agents hold no Fly credential, rail.deploy stays operator act. |

</details>

<details><summary><b>C6 — Other dormant, discharged or unclear rows</b>: 31 rows</summary>

| ID | File | Rule | Evidence |
|---|---|---|---|
| ADR01-16 | `adr/2026-04-23-guardian-risk-relock-0.34.md` | Re-lock Guardian per-trade risk just under both bust and static-DD caps with preserved headroom; Striker and Aegis unchanged. | Guardian cold-stored by 2026-08-23-strategy-coldstore-phase-c.md; frozen 0.0034 preserved in core/historical_challenge.py L63; no live _BASE_RISK entry. |
| ADR01-38 | `adr/2026-05-08-dd-trigger-c2-relock.md` | Do not conflate the retired C2 revert check with allocation-refresh-2's §Falsifier forward-revert trigger, which the banner calls still live. | Intercept's 'still live' claim contradicted by allocation-refresh-2 Addenda 2026-08-02/08-15 (zero live catch-paths); keep-or-drop distinction is operator's call. |
| ADR01-57 | `adr/2026-05-16-fixture-test-requirement.md` | For a CC spawn brief with three or more mechanical edits in one defect family, dry-run the edits on a local snapshot before handoff. | Only owner is archived docs/methodology/archive/notion/methodology-canon.md §7; no live skill, ADR or rule carries the dry-run rule. |
| ADR01-89 | `adr/2026-06-04-lean-portfolio-meta-layer.md` | Retain this ADR rather than delete it while the concept-admissibility and three-loop-binding ADRs cite it as parent doctrine. | Conflicts with operational_rules §16: a citation alone is a dependency to resolve, not a retention entitlement; ADR retention is operator's call. |
| ADR02-23 | `adr/2026-06-05-sweep-engine.md` | Do not revive the in-Pine multi-config optimizer or native-only-as-sole-engine options without new evidence invalidating their recorded rejection reasons. | Alternatives weighed for sweep machinery retired 2026-07-11; Python-as-sole covered by live doctrine; native-only is now the prefilter gate's fallback. |
| ADR02-58 | `adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md` | Record in each forward pre-registration or ledger entry how many forward tests ran concurrently, so confirmation counts read against the right denominator. | Not in force: §2c records P2 not ratified 2026-06-11 and lists concurrency disclosure as part of any P2 re-proposal. |
| ADR02-136 | `adr/2026-06-16-rule-2-budget-before-acting.md` | Keep Rule 2 in its own ADR; do not fold it into the three-loop binding ADR. | Authoring-time forbidden move discharged when Rule 2 landed in its own ADR 2026-06-16; future ADR consolidation governed by ceremony-tiering ADR. |
| ADR03-20 | `adr/2026-06-23-tv-backtest-egress-automation.md` | Use native-CSV browser automation (Path A2) only as a fallback on a structurally isolated research account, at human cadence, never as a batch loop. | Unreachable: second TV account forbidden (same ADR §5; tv-agent-browser-access §2.2), so no isolated account exists for Path A2. |
| ADR03-44 | `adr/2026-07-01-add-back-metric-layer-split.md` | Use Guardian Silver only as the object-layer add-back anchor; never in meta-layer statements. | Stale anchor: three-loop ADR hook #6 records Silver admission reversed 2026-07-01 (object rate 0/1); cross-layer ban carried by D2. |
| ADR04-82 | `adr/2026-07-12-prop-portfolio-four-friendly-firms.md` | If exactly one frozen tier clears at 2026-11-08, read the falsifier as PARTIAL: no discharge or demotion; re-check 2027-02-08, then demote if still one or fewer. | Addendum 2026-08-22 stays Proposed; withdrawal ADR Addendum 2026-10-02 ruling 4 reserves the exactly-one-tier call to Joshua at 2026-11-08. |
| ADR05-150 | `adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md` | Use T1 (per-regime-half p99 drawdown cap, adopted withdrawal model, days-to-first-skim practicality bar; TUW deferred) as risk-characterization input for any Aegis→M6J go-live decision. | T1 input only for parked Aegis to M6J (parked by docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md §2.1); reopened self-funded lane uses 15% standard (2026-10-09 ADR Decision 4). |
| ADR05-180 | `adr/2026-07-16-root-doc-charter-dedup.md` | Keep the main checkout on a CLAUDE.md-free commit so .claude/worktrees sessions load AGENTS.md, not the retired file. | Post-merge condition: CLAUDE.md deleted in 5fae4d2d and absent at HEAD 3feb5961; operator local checkout state unverifiable from here. |
| ADR06-16 | `adr/2026-07-17-c1-rail-build-account-registration-go.md` | Run the pre-registered same-size control before any live-fill claim relies on MYM CME-native timing precision. | Striker venue-edition MYM leg withdrawn 2026-08-04; 2026-10-19 addendum: no book-lineage case at Tradeify; accepted-book Striker MYM could revive need. |
| ADR06-88 | `adr/2026-07-22-c1-venue-native-monitoring-maturity.md` | Complete the §2b clean mid-bar re-measurement independently of M1 as an execution-quality question. | Moved to Q-SIGID-1 (briefs INDEX: DORMANT-OTHER 2026-10-15); S2b closed-bar host reads §2b EQUAL; close-or-keep is operator's. |
| ADR06-125 | `adr/2026-07-22-challenge-era-substrate-retirement.md` | Land pointers to this dormancy record on W4 §2 and the STATE forward board. | W4 half landed (W4 Addendum 2026-08-08 links the dormancy record); STATE pointer never landed; thin-STATE need is operator's call. |
| ADR07-103 | `adr/2026-07-31-orb-mnq-unpark-payability-target.md` | Route ORB-complement fade work as K=0 Stage-0 extraction under the fade program; no register_search open, manifest or K spend. | ORB re-parked (2026-08-03 ADR); fade program body cold-stored though CATALOG/ARCHIVED.json still list ACTIVE; operator confirms routing is spent. |
| ADR08-35 | `adr/2026-08-03-orb-mnq-repark-payability-falsified.md` | On any T2-harness re-run, a miss beyond ±1.0pp or a broken control A/B/G halts and voids this ADR's basis pending a superseding ADR. | R1 harness run_t2_intraday_bust.py deleted by Great Prune 283d1de; Addendum 2026-08-30 records dormancy; restorable from private archive. |
| ADR08-120 | `adr/2026-08-04-tradeify-venue-descope-eval-included.md` | Exclude a Tradeify clearance from the §4 count only by a dated, independent finding that the frozen simulation no longer proxies the venue, never by the de-scope alone. | Addendum 2026-08-22 still Proposed/unratified; F1 ruled directly by Accepted Addenda 2026-08-23 and 2026-09-01 without this canon. |
| ADR08-121 | `adr/2026-08-04-tradeify-venue-descope-eval-included.md` | Any §4 success claim resting on a Tradeify clearance must disclose the 2026-08-04 withdrawal and F1's ruling status; no unconditional claim while F1 is open. | Proposed/unratified; F1 ruled 2026-09-01 so 'while F1 open' cannot arise; disclosure practice carried by Addendum 2026-09-01 L550. |
| ADR09-105 | `adr/2026-08-08-adr-ceremony-tiering.md` | Treat the former light-share target and its November-8 omitted-apparatus review as retired by policy replacement, not passed. | Historical Grounds note; grep finds light-share target/Nov-8 review only in this ADR and archived SESSIONS-2026-Q3; no live consumer. |
| ADR11-37 | `adr/2026-08-16-deep-iteration-lane-charter.md` | Build --lane deep on register_search, add lane-scoping notes to strategy_harvest Clause-K and M-19, and add the lane row to the anomaly-discovery skill. | Steps 2-4 landed: register_search --lane deep, strategy_harvest.md L105 row, skill L123/148; only M-19 intercept missing, owed-or-drop is operator's. |
| ADR11-57 | `adr/2026-08-21-cfo-subscription-ledger-consolidation.md` | KEEP pursuit records of subscription or venue-account meta-belt class must point to the ledger; the check WARNs only, with no severity escalation or class widening. | gates.yml L59-63 retired the pursuit-records check 2026-08-24 as always-exit-0; pointer duty is D1; manual script retained, operator's call. |
| ADR12-44 | `adr/2026-08-26-striker-legmap-cap-release.md` | Set LEG_MAP cap_alloc for dj30_mym and nas100_mnq to 0, releasing the 80-micro account cap. | Executed: ops/c1_rail/c1_sizing_host_reference.py L108/L114 set cap_alloc 0 with release comments; allocation-adjacent, so operator confirms. |
| METHOD-115 | `docs/methodology/observation_routing.md` | Route every observation to exactly one of Closed (one paragraph, no standing artefacts), Action (owned change plus verification) or Forward (cheapest-falsification-first question). | Superseded: ADR 2026-08-15 §2 downgrades three-bucket routing to an optional tag; that ADR rules out deleting the concept, so operator call. |
| OPS-36 | `docs/operational_rules.md` | For any move targeting an archive, §0 lists the current archive subtrees to confirm the destination convention. | Targets repo-root archive/, which no longer exists (ls); lab moves use scripts/archive_lab_analysis.py; docs/ltm/README owns archive retrieval. |
| ROOT-120 | `docs/rule_0.md` | Apply the archived resurrection rule and 90-day review gate (pre-prune-2026-06-05 methodology archive README) when resurrecting pruned rules. | Cited tag pre-prune-2026-06-05 absent on this clone (git tag empty); docs/ltm/README owns retrieval; Rule 36 governs re-adding rules. |
| SKILL02-108 | `.claude/skills/code-defect-debugging/SKILL.md` | Review the skill quarterly (defects, Phase-1 adherence, mis-routes, lessons, 4.5 firings); revise its description if mis-routes exceed one per quarter. | Unenforced self-review cadence; no review recorded in SESSIONS/STATE; programme-audit owns cadence audits; ceremony under Rule 36. |
| SKILL02-210 | `.claude/skills/futures-anomaly-discovery/reference/proxy-discipline.md` | Use MJY (not M6J) for micro JPY; check its thin liquidity and margin fresh before any campaign sizing. | ops/instruments/MJY.md: MJY RETIRED as execution/replay venue 2026-07-05; symbology owned by MJY.md M4; revival only via Bulenox. |
| SKILL03-162 | `.claude/skills/prop-firm-challenge/SKILL.md` | After re-exporting broker and TV CSVs, investigate when pass/bust drifts beyond about 1σ from locked expectation (usually regime change). | Legacy book has no live venue and no book is deployed (AGENTS §Strategy Reference, §Live-execution posture); no broker-CSV drift input exists. |
| SKILL03-170 | `.claude/skills/prop-firm-challenge/SKILL.md` | Model each firm's inactivity rule in MC via inactivity_max_idle_days. | Contradicted by docs/load_bearing_numbers.md §2: published figures assume inactivity barrier OFF; barrier-ON re-MC degenerate, run twice. |
| SKILL04-10 | `.claude/skills/prop-firm-challenge/references/strategy_reference.md` | Apply the manual binary-event pause rule to Aegis around central-bank decisions. | Target section removed in 2a5eac5f; contradicts operational_rules §1 (no BOJ skip), but archived aegis LOCK.md still records a permanent pause. |

</details>

## 6. Contradictions and drift found

These restore consistency with rulings already in force, so they need no new decision; they ride
the later PRs (§7). ✓ = re-read at `b8524d17` by the coordinator; the rest were reported by the
inventory agents with paths and are re-checked when repaired.

| # | Where | Conflict | Repair |
|---|---|---|---|
| 1 ✓ | `.claude/skills/c1-rail/SKILL.md` L23 | Agent authority table allows `fly deploy` | `rail.deploy` is an operator act and agents hold no Fly credential (Addendum 2026-10-24b); mark it operator-only, same for agent `fly ssh` status/disarm rows |
| 2 ✓ | `.claude/skills/fable-method/SKILL.md` L57 | "never … merge … absent explicit operator instruction" | Point to the conditioned merge GO (Rule 6) |
| 3 ✓ | `.claude/skills/brief-authoring/references/cc_handoff.md` L9 | "no merge without Joshua's go" | Same |
| 4 ✓ | `scripts/seat_authority.yml` `pr.merge` comment | "independent review (not the PR's author)" lacks the Codex-at-head and three-review conditions | Align the comment with Rule 6 |
| 5 ✓ | `code-defect-debugging` Phase 4.5, `fable-method` Step 5 | Stop after three failed fixes; AGENTS.md says two failed corrections | Two (Rule 7) |
| 6 ✓ | `.claude/skills/handoff-verify/SKILL.md` L189 | "minutes, not hours" | Drop the time unit (Rule 2 ADR §5.2) |
| 7 ✓ | `scripts/githooks/post-merge` L48 | "main carries no branch protection or required checks" | `main` requires a PR and `skills (3.12)` |
| 8 | AGENTS.md §Live-execution table; STATE | Track B "suspended until 11-08" vs superseded 2026-10-16 | With D4 |
| 9 ✓ | AGENTS.md §Public-clone, Rule 19 source text | `bar_data` "no regenerable producer" — four panels were refreshed 2026-09-03 from operator CME exports | "changes only by a fresh operator export plus its SHA256SUMS delta" |
| 10 ✓ | `scripts/gates.yml` governance-prose-control-chars | Trigger regex selects only three files; the script scans STATE, ADRs, briefs and notes | Widen the trigger (Rule 38: gates must be reachable) |
| 11 | supersession-placement gate vs operational_rules §14 | Text covers desk cards; gate scope is `lab/analysis/**/RESULTS*.md` only | Narrow the text or widen the gate |
| 12 ✓ | `prop-firm-challenge/references/strategy_reference.md` L51, `trade-csv-reconcile/references/baselines.md` | Aegis binary-event pause conflicts with operational_rules §1 and points at a removed section | Delete (Rule 1) |
| 13 | `docs/rejected_candidates.md` | 12 entries appear twice; the instrument-profiles gate is described as tier=always (it is path-conditional) | Dedupe; correct the description |
| 14 | `methodology_lessons.md` | M-1…M-6 phantom (no headings), numbering gated on retired Notion, no M-25 | With D6 |
| 15 | `rule_0.md` L24, `fable-method` Step 2.1, canon §12 | Retrieval via `pre-prune-*` tags absent from the public clone | Point to `docs/ltm/README.md` retrieval |
| 16 | `LESSONS_INDEX.jsonl` E1–E4 | `trigger_globs` point at `ops/live_journal/**`, which does not exist | With D5/D6 |
| 17 | `scripts/README.md` §Independent review | Panel mechanics read as the independent review | Note that a Claude panel on Claude work is not the review (Rule 5, D3) |
| 18 | `strategy_harvest.md` §2.4; discovery-campaign template §R | Still apply the deleted cost "sniff test" / cost-law inequality | Repoint to each candidate's own net-of-cost estimate |
| 19 | `.claude/workflows/gate-reachability-audit.js` L196 | Cites an archived ADR (AMBIGUOUS-HOLD streak doctrine) still treated as live | Give the doctrine a live owner (Rule 28) or drop the citation |
| 20 | `lesson_capture.md` | Registry path stale; per-lesson `$` cost field | With D6 |
| 21 | `c1-rail` verification commands | Bare `pytest`/`python` | `fp` launcher (Rule 22) |
| 22 | Many ADR falsifier clauses | "revert only by superseding ADR, never edit in place" vs the ceremony-tiering 2026-09-08 dated-revision rule | Rule 32 wording governs; repoint on touch |

## 7. Sequence after the ruling

Each step is one PR on a `claude/` branch, reviewed by Codex, budgeted under Rule 2 in its own
description.

1. **AGENTS.md §Core rules** (D1): add the 42 lines; cut the 104 absorbed AGENTS.md rows to links;
   keep §Live-execution posture, §Protection and the MC literals in place.
2. **Namespace** (D2): legacy map at the end of operational_rules.md; repoint living "Rule N"
   citations; rename skill-local numerals.
3. **Deletions with plain evidence** (D9), one PR per source group; each carries its rows' IDs.
4. **Ruled deletions** (D4–D8), one PR per cluster, recording each supersession where its readers
   meet it (Rule 30).
5. **Repairs** (§6) and the D10 choices.
6. **Detail moves**: the 278 detail rows whose owner should change, by destination owner.

## 8. Verification

| Check | Command | Result |
|---|---|---|
| Gate suite at the base, before any edit | `python -I scripts/fp.py check` (ops venv `tmp/ops-env` built from `requirements-ops.lock --require-hashes`, Python 3.12.3, after `git fetch --unshallow`) | exit 0, `status: completed`, `source_stable: true` at `3feb596`; record `.cache/fp-verification/20261025T044350Z-8e1768a11408/record.json`. `check_skill_deploy_sync` SKIPped (no deployed bundle in a cloud container) — not checked, not a pass; data-manifest absent-tree WARNs (vendor bytes are not in a public clone). |
| Gate suite on this PR | `python -I scripts/fp.py check` at this PR's head | Reported in the PR description |
| Inventory completeness | 27 extraction chunks, 3,731 rows; 27 classification files, 3,731 rows (one per rid); 16 reconciliation files | Every extracted rule has exactly one classification; the generator refuses otherwise |

Reproduction: the inventory, classification and reconciliation are per-rule JSON lines produced in
the coordinating session; Appendix A is generated from them and is the durable record. Rule text
there is paraphrase, scanned for account identifiers, P&L and private parameter values before
commit (none found; figures that appear are already public in AGENTS.md or Accepted ADRs).

## Appendix A — Classification of every rule

Inventory base `3feb596`, reconciled to `b8524d17`. Columns: **ID** (chunk-number), **Where** (section and approximate line), **Rule** (paraphrase, ≤30 words), **→** (core rule and disposition: `abs` absorbed, `det` kept as detail, `DEL` proposed deletion, `DEL⚖` deletion that needs a ruling), **Note** (for a detail, where it should live if not its current file; for a deletion, the evidence; changes on main since the base are marked *at HEAD*).


### AGENTS.md — 146 rules


<details><summary><code>AGENTS.md</code> — 146 rules: 104 absorbed, 40 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| AGENTS-1 | §Purpose L5 | Scope work to automated futures strategies at core/firm_rules.AUTOMATION_FRIENDLY_PROP_FIRMS; mission is generate, evaluate, deploy, measure, update. | R3 det |  |
| AGENTS-2 | §Purpose L9 | Orient from STATE.md for priorities and obligations, then the owning campaign plan and record; PIPELINES.md for handoffs, REPO_MAP.md for code, SESSIONS.md for history. | R8 abs |  |
| AGENTS-3 | §Purpose L12 | Let direct operator instructions govern the current task. | R3 abs |  |
| AGENTS-4 | §Purpose L12 | Do not infer new work or authorization from historical dispatches. | R3 abs |  |
| AGENTS-5 | §Purpose L15 | Treat AGENTS.md as the only agent instruction file; read a dated record's 'CLAUDE.md §X' as 'AGENTS.md §X'. | R29 det |  |
| AGENTS-6 | §Purpose L17 | Take seats and escalation-lane triggers from the surface-allocation ADR, their sole owner. | R4 abs |  |
| AGENTS-7 | §Purpose L20 | Run chip tasks, handoffs and dispatch cards in the cloud by default. | R41 abs |  |
| AGENTS-8 | §Purpose L20 | A card that must run locally states 'Must run locally' near its top, with the reason (private read surface, operator machine/VM, private evidence writes). | R41 det | → .claude/skills/task-routing/SKILL.md |
| AGENTS-9 | §Purpose L25 | Keep decisions with their owning specification, campaign, plan or PR. | R32 abs |  |
| AGENTS-10 | §Purpose L25 | Admit ADRs only under the ADR ceremony-tiering admission rule. | R32 abs |  |
| AGENTS-11 | §Purpose L26 | Other documents link the decision's owner or label themselves a derived mirror. | R29 abs |  |
| AGENTS-12 | §Purpose L27 | Documents must serve the pipeline and pass the retention test. | R31 abs |  |
| AGENTS-13 | §Purpose L29 | Retrieve removed evidence via docs/ltm/README.md archive guidance and lab/ARCHIVED.json. | R31 det | → docs/ltm/README.md |
| AGENTS-14 | §Contribution L34 | STATE's operator queue and owning records' sequencing decide what to work on; this section governs only how authorized work is done. | R3 abs |  |
| AGENTS-15 | §Contribution L36 | Before substantial work, name the question and the decision its answer changes (pre-Q gate). | R9 abs |  |
| AGENTS-16 | §Contribution L36 | Budget substantial work in one line under Rule 2, which defines substantial work and excludes routine fixes. | R2 abs |  |
| AGENTS-17 | §Contribution L36 | When the budget bound is reached, reassess; never expand the budget or weaken acceptance. | R2 abs |  |
| AGENTS-18 | §Contribution L37 | Use the cheapest trustworthy evidence: reuse valid evidence and run focused tests. | R36 det |  |
| AGENTS-19 | §Contribution L37 | Never skip reviews or checks a card, ADR or gate requires on cheapest-evidence grounds. | R3 abs |  |
| AGENTS-20 | §Contribution L38 | Do not treat PR counts, document volume or architectural completeness as evidence of value. | R36 abs |  |
| AGENTS-21 | §Contribution L38 | Record negative findings where they are read. | R30 abs |  |
| AGENTS-22 | §Contribution L39 | No value judgment waives a legal, capital, credential, private-data, verification or release control. | R3 abs |  |
| AGENTS-23 | §Contribution L39 | Do not add a new form, ledger, report or approval layer for routine fixes. | R36 abs |  |
| AGENTS-24 | §Output efficiency L43 | Use the fewest words that meet the objective in text, code, tool calls and records; no preamble, recap, filler or restated context; link the owner. | R35 abs |  |
| AGENTS-25 | §Output efficiency L44 | Never trade away correctness, required confirmations or honest verification reporting for brevity. | R35 abs |  |
| AGENTS-26 | §Output efficiency L47 | A ruling, GO, acceptance or record grants only what it states; anything unstated is not granted. | R3 abs |  |
| AGENTS-27 | §Output efficiency L48 | Do not append 'no X granted' disclaimers. | R35 abs |  |
| AGENTS-28 | §Output efficiency L48 | Keep stated limits on how a verdict may be read, such as a closure's negative-scope section. | R35 det |  |
| AGENTS-29 | §Live-execution posture L54 | Confirm actual host state before operational work; the recorded posture (disarmed, no deployed book, emission off) is not proof. | R10 abs |  |
| AGENTS-30 | §Live-execution posture L54 | Read M1 RESOLVED as covering only the incumbent's Stage 1 monitoring; fp check printing RESOLVED is expected; arming still needs every other gate. | R10 det |  |
| AGENTS-31 | §Live-execution posture L54 | Require a separate M1 acceptance for any new instance, such as the personal account. | R10 abs |  |
| AGENTS-32 | §Live-execution posture L56 | Do not use Databento; it is retired and unsubscribed, and no replacement data source is approved. | R18 abs |  |
| AGENTS-33 | §Live-execution posture L56 | Keep daemon signal emission blocked (emit_enabled=false) while no data source is approved. | R10 det |  |
| AGENTS-34 | §Live-execution posture L58 | Setting dry_run=false requires M1 RESOLVED; the gate's object is the arm, not the send. | R10 abs |  |
| AGENTS-35 | §Live-execution posture L59 | Disarm before the absolute armed_until expiry; never let an armed session lapse. | R10 abs |  |
| AGENTS-36 | §Live-execution posture L60 | Live spend requires M1 RESOLVED and a separate operator GO. | R10 abs |  |
| AGENTS-37 | §Live-execution posture L60 | Obtain a fresh operator GO for every armed session. | R10 abs |  |
| AGENTS-38 | §Live-execution posture L61 | Agents may place orders, exit positions and cancel orders, including via computer use, only when the operator directs; arming, spend and per-session GO gates still apply. | R10 abs |  |
| AGENTS-39 | §Live-execution posture L61 | Weekly account-preservation trades may be operator- or agent-placed at the operator's direction; the deadline lives in STATE. | R10 abs |  |
| AGENTS-40 | §Live-execution posture L62 | Treat the arming interlock as structural only: it gates just the arm helper, checks no signature, and the rail boot gate does not check M1. | R10 det |  |
| AGENTS-41 | §Live-execution posture L62 | Deliver the host-side activation gate at TB-I3 (still owed). | R10 det | → docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md |
| AGENTS-42 | §Live-execution posture L62 | Invoke --acknowledge-m1-unresolved only through the operator-act prompt; it overrides a structurally valid unresolved artifact and writes an arming_deviation record. | R10 det | → docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-09-26 |
| AGENTS-43 | §Live-execution posture L64 | order_id idempotency is disproven: give every payload a fresh tag. | R11 abs |  |
| AGENTS-44 | §Live-execution posture L64 | Keep private account figures private. | R13 abs |  |
| AGENTS-45 | §Live-execution table L68 | Retain the incumbent environment; no successor migration. | R10 abs |  |
| AGENTS-46 | §Live-execution table L69 | Route signals from the Python signal daemon to the listener. | R11 abs |  |
| AGENTS-47 | §Live-execution table L69 | Do not automate TradingView login. | R11 det | → docs/adr/2026-08-07-loop-s2-signal-host-fork.md |
| AGENTS-48 | §Live-execution table L70 | Keep withdrawn Striker editions barred; separate campaign expressions are only conditionally eval-eligible. | R15 abs |  |
| AGENTS-49 | §Live-execution table L71 | Rail build and account registration hold GO, bounded by the rail GO ADR's spend ceiling. | R10 det | → docs/adr/2026-07-17-c1-rail-build-account-registration-go.md |
| AGENTS-50 | §Live-execution table L72 | A licensed test strategy may discharge M1 item 5 / B7 Stage 1 independently of strategy selection. | R10 DEL⚖ | Incumbent M1 RESOLVED 2026-09-14 (A8) via option-D attended input (M1 addendum 2026-09-11), not the licence; reuse for new instance is operator call. |
| AGENTS-51 | §Live-execution table L73 | Hold the four-firm program falsifier at 2026-11-08; a Tradeify resting discharge counts toward it again. | R28 abs |  |
| AGENTS-52 | §Live-execution table L74 | On Tradeify eval accounts, strategy logic must be native: no external engine, bridge or direct API. | R10 abs |  |
| AGENTS-53 | §Live-execution table L74 | Treat Track B as suspended from 2026-10-13 until the 11-08 sitting or an operator ruling; the personal lane continues. | R10 DEL⚖ | Superseded by deployment-checklist Addendum 2026-10-16: Track B superseded (not suspended) for Tradeify, branch (a) withdrawn; STATE row 1 agrees. |
| AGENTS-54 | §Live-execution table L74 | Place the weekly trade only on a supported platform, never through CrossTrade or the API. | R10 abs |  |
| AGENTS-55 | §Architecture L78 | Layer ownership: core holds shared engines and frozen controls, lab research, ops operational services, governance at root; REPO_MAP.md maps owners and boundaries. | R37 abs |  |
| AGENTS-56 | §Architecture L79 | Never import between lab and ops. | R37 abs |  |
| AGENTS-57 | §Architecture L79 | core must import no other internal layer. | R37 abs |  |
| AGENTS-58 | §Architecture L83 | Before opening research, read lab/CATALOG.md In flight, docs/briefs/INDEX.md, the relevant instrument ledger and its rejection bar. | R8 abs |  |
| AGENTS-59 | §Architecture L85 | Do not treat an empty rg result as evidence of no prior work; check cold stores, history and catalog paths via retrieval guidance. | R8 abs |  |
| AGENTS-60 | §Load-bearing numbers L91 | Read docs/load_bearing_numbers.md, which owns scope, exceptions and historical values, before quoting prop-tier figures. | R20 abs |  |
| AGENTS-61 | §Load-bearing numbers L92 | State eval bust claims as EOD-clock lower bounds unless an intraday-honest RESULTS artifact backs them. | R20 abs |  |
| AGENTS-62 | §Load-bearing numbers L93 | Read published bust/pass claims as assuming the inactivity barrier is OFF. | R20 abs |  |
| AGENTS-63 | §Load-bearing numbers L94 | Do not reopen the degenerate barrier-ON re-MC as a fresh finding. | R20 abs |  |
| AGENTS-64 | §Strategy Reference L96 | Locked parameters and artifacts are immutable; do not modify the locked legacy book (record in core/strategies/CATALOG.md). | R14 abs |  |
| AGENTS-65 | §Strategy Reference L99 | Treat the locked legacy book as having no live venue and not being a live book. | R15 det | → core/strategies/CATALOG.md |
| AGENTS-66 | §Strategy Reference L99 | Live sizing authority is dd_protection.BASE_RISK / firm_rules._BASE_RISK; every other strategy parameter lives only in Pine. | R14 det | → core/strategies/CATALOG.md |
| AGENTS-67 | §Strategy Reference L103 | Treat the AGENTS.md MC calibration triple as historical record, never a live claim. | R20 abs |  |
| AGENTS-68 | §Strategy Reference L104 | Keep the MC calibration literals in AGENTS.md; reword or move them only alongside the ops/recall/guard.py parser. | R14 det |  |
| AGENTS-69 | §Strategy Reference L108 | Keep MC engine regression vendor-free. | R13 det | → tests/core/README.md |
| AGENTS-70 | §Strategy Reference L108 | Use CME futures TV exports (core/data/tv_exports/cme/) as the canonical feed; OANDA and Pepperstone are retired. | R18 abs |  |
| AGENTS-71 | §Strategy Authorization Lifecycle L113 | Keep parameter lock, capital authorization and venue deployment as separate axes; strategy_lifecycle.md owns lifecycle, venue editions own venue binding. | R15 abs |  |
| AGENTS-72 | §Strategy Authorization Lifecycle L117 | Under decay, apply only pre-registered de-risking; never re-optimize. | R15 abs |  |
| AGENTS-73 | §Strategy Authorization Lifecycle L118 | Automation may move authorization down only, except via the bounded sandbox-up promotion lane. | R15 abs |  |
| AGENTS-74 | §Strategy Authorization Lifecycle L120 | Retirement and full beta shutdown require operator GO/NO-GO. | R15 abs |  |
| AGENTS-75 | §Strategy Authorization Lifecycle L120 | Read effective multipliers from core/lifecycle.py and its state; never infer a live haircut from historical rail operation. | R15 det | → docs/methodology/strategy_lifecycle.md |
| AGENTS-76 | §Protection L126 | dd_protection.py holds the single protection rule, consumed by the rail sizing path; it is unused while no strategy is deployed. | R14 det |  |
| AGENTS-77 | §Protection L129 | DD tier: when equity drawdown from peak reaches DD_TRIGGER, scale that day's sizing by DD_SCALE; it clears automatically at peak. | R14 det |  |
| AGENTS-78 | §Protection L131 | Do not change DD_TRIGGER or DD_SCALE; they are frozen and guarded at import. | R14 abs |  |
| AGENTS-79 | §Protection L132 | Change dd_protection constants only via pre-registration, re-MC, the both-halves regime-robustness gate, then an admitting ADR. | R14 abs |  |
| AGENTS-80 | §Protection L136 | Concept-not-constant: keep the mechanism invariant; trigger, scale and reference_mode are per-(portfolio, firm-tier) variables. | R14 det | → docs/adr/2026-07-13-dd-protection-concept-not-constant.md |
| AGENTS-81 | §Protection L138 | Reintroducing a second protection tier needs fresh pre-registration; the deleted equity tier's revert triggers are lost, not lookup-able. | R14 det |  |
| AGENTS-82 | §Firm Expansion L143 | Define firm rules in core/firm_rules.py. | R16 abs |  |
| AGENTS-83 | §Firm Expansion L143 | After defining firm rules, run the core/mc/preflight.py engine-support pre-flight; configuration alone does not prove clock or firm-class support. | R16 abs |  |
| AGENTS-84 | §Firm Expansion L145 | Every prop tier must carry starting_balance. | R16 abs |  |
| AGENTS-85 | §Firm Expansion L145 | A new firm requires an ADR, the pre-flight, and a re-MC when used. | R16 abs |  |
| AGENTS-86 | §Firm Expansion L146 | A new execution feed also requires the feed-equivalence pre-flight. | R18 abs |  |
| AGENTS-87 | §Methodology references L151 | Read production sources before risk-control or locked-Pine claims. | R0 abs |  |
| AGENTS-88 | §Methodology references L152 | Re-propose a rejected candidate only with new mechanism evidence, not parameter changes. | R26 abs |  |
| AGENTS-89 | §Methodology references L153 | Select loops under the INQHIORI canon's three-loop authority. | R9 abs |  |
| AGENTS-90 | §Methodology references L154 | Follow the evaluation-order ADR's standing sequence; campaign-specific amendments stay with their owners. | R24 abs |  |
| AGENTS-91 | §Methodology references L156 | Apply the regime robustness gate to every qualifying risk-control lock change. | R24 abs |  |
| AGENTS-92 | §Continuous improvement L161 | During authorized work, actively notice concrete plan flaws, preventable mistakes, recurring failures and evidenced waste. | R36 abs |  |
| AGENTS-93 | §Continuous improvement L162 | At planning, correction and completion moments, use the agent-improvement skill when an opportunity appears; read its source if the harness does not list it. | R36 abs |  |
| AGENTS-94 | §Continuous improvement L164 | Without an improvement opportunity, create no extra reflection artifact or task. | R36 abs |  |
| AGENTS-95 | §Continuous improvement L165 | Implement and verify local, reversible, evidence-supported improvements fitting the task and seat, without changing outcome or acceptance criteria, including pre-failure repair of agent-owned execution sequences. | R36 det | → .claude/skills/agent-improvement/SKILL.md |
| AGENTS-96 | §Continuous improvement L167 | Existing authorization carries forward to in-scope improvements; do not re-ask merely because it is an improvement. | R36 det | → .claude/skills/agent-improvement/SKILL.md |
| AGENTS-97 | §Continuous improvement L171 | Improvement authority is the task's existing authorization, bounded by seat grants in scripts/seat_authority.yml and the card's authority block; never an operator act or forbidden capability. | R4 abs |  |
| AGENTS-98 | §Continuous improvement L176 | Keep a frozen worker card frozen: workers return contradictions, scope changes and improvement evidence to the coordinator; other seats route out-of-scope changes by seat. | R4 abs |  |
| AGENTS-99 | §Continuous improvement L179 | Make at most one durable intervention per failure mechanism, at the cheapest reliable layer: source/test, hook, skill, AGENTS.md, then ADR/lesson. | R36 det | → .claude/skills/agent-improvement/SKILL.md |
| AGENTS-100 | §Continuous improvement L186 | Retain evidence with the existing owner; write an owner record only under a card granting governance.author (no card: operator-scoped owner); otherwise route via task return. | R4 det | → .claude/skills/agent-improvement/SKILL.md |
| AGENTS-101 | §Continuous improvement L190 | Promote one-off feedback into standing guidance only when high-severity or independently recurring. | R36 det | → .claude/skills/agent-improvement/SKILL.md |
| AGENTS-102 | §Continuous improvement L192 | Do not edit standing instructions, including harness hooks in .claude/settings.json, unless the user requests it; unasked, propose; requested, implement within Bound 1. | R36 abs |  |
| AGENTS-103 | §Continuous improvement L196 | After two failed corrections of one issue, stop, summarize learnings, and restart with a cleaner prompt and explicit verification criteria on the ADR-named escalation lane. | R7 abs |  |
| AGENTS-104 | §Public-clone posture L202 | Treat the repository as public; private history lives in first-passage-archive, retrieved per docs/ltm/README.md. | R13 det |  |
| AGENTS-105 | §Public-clone posture L204 | Do not commit account identifiers or P&L, vendor-licensed CSVs, Pine source, or executable Python ports of locked strategy logic. | R13 abs |  |
| AGENTS-106 | §Public-clone posture L205 | Pin private sources via SHA256SUMS, core/strategies/MANIFEST.sha256 and PORT_MANIFEST.sha256; new locked ports follow the same policy. | R13 det |  |
| AGENTS-107 | §Public-clone posture L207 | Make vendor-dependent tests skip when their inputs are absent. | R13 det |  |
| AGENTS-108 | §Public-clone posture L208 | Treat core/data/bar_data/ as retained but frozen: usable panels with no regenerable producer. | R19 abs |  |
| AGENTS-109 | §Public-clone posture L211 | Agents may read the accepted book's four Pine sources, BOOK_SOURCES.sha256-listed runtime ports and effective_inputs.json only in place in the operator's primary checkout. | R13 det |  |
| AGENTS-110 | §Public-clone posture L215 | Never copy private read-surface files into a worktree, commit or quote their bodies or values, edit them, or pass them to any external service. | R13 det |  |
| AGENTS-111 | §Public-clone posture L218 | Only the ports and effective_inputs.json (never Pine) may be copied to the Joshua-controlled Windows VM, solely for runs and terms the §60 VM addenda admit. | R13 det | → docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25 |
| AGENTS-112 | §Vendor-data integrity gate L223 | Commit each re-export's SHA256SUMS delta with its change; the checker hashes working-tree bytes (commands owned by the manifest integrity ADR). | R19 abs |  |
| AGENTS-113 | §Vendor-data integrity gate L224 | Install the repo git hooks once per clone (scripts/install_hooks.sh or scripts\install_hooks.bat). | R19 abs |  |
| AGENTS-114 | §Vendor-data integrity gate L225 | Do not use git commit --no-verify as the standing path. | R19 abs |  |
| AGENTS-115 | §Gate composition authority L230 | gates.yml and its runner own gate composition and scripts/README.md the entry points; do not maintain a parallel gate list. | R38 abs |  |
| AGENTS-116 | §Gate composition authority L232 | main requires a PR and the skills (3.12) status; other path-filtered checks are not required merge checks. | R6 det | → docs/briefs/closures/Q-GATESTACK-1-closure-falsified.md |
| AGENTS-117 | §Merges and credentials L235 | An agent may merge a PR, pinned to its head SHA, only after a clean Codex review at that head and every CI check completed green. | R6 abs |  |
| AGENTS-118 | §Merges and credentials L235 | Never enable auto-merge. | R6 abs |  |
| AGENTS-119 | §Merges and credentials L235 | After fixing Codex findings, push and comment '@codex review' for a fresh review of the new head. | R6 det | → docs/adr/2026-07-14-cc-cursor-surface-allocation.md#addendum-2026-10-24b--operator-rulings-conditioned-merge-go-and-credential-custody |
| AGENTS-120 | §Merges and credentials L235 | Merge only if a Codex review is clean within three reviews; after three reviews with findings, stop fixing and return the PR to its original owner for rewrite. | R6 abs |  |
| AGENTS-121 | §Merges and credentials L235 | Act under the agent's own scoped credentials (repo-scoped GitHub PAT), never the operator's tokens. | R12 abs |  |
| AGENTS-122 | §Merges and credentials L235 | Agents hold no Fly or broker credential. | R12 abs |  |
| AGENTS-123 | §Python environment L239 | Use the launcher of the checkout being tested: fp python, test, test-ops, check, python -m pytest; without PowerShell 7.3+, python -I scripts/fp.py. | R22 abs |  |
| AGENTS-124 | §Python environment L239 | Run fp doctor before project Python work. | R22 abs |  |
| AGENTS-125 | §Python environment L240 | If launcher validation fails, diagnose it; never silently fall back to system Python or bypass validation. | R22 abs |  |
| AGENTS-126 | §Python environment L240 | Keep the separately pinned research environment separate from the operations environment. | R22 det | → scripts/README.md#local-operations-launcher |
| AGENTS-127 | §Python environment L241 | When project Python spawns another Python process, use sys.executable, not bare python. | R22 abs |  |
| AGENTS-128 | §Python environment L242 | Report the command, interpreter, tested revision or working-tree state, and actual results of every check. | R21 abs |  |
| AGENTS-129 | §Python environment L242 | Disclose any pre-existing gate failure; never describe the complete gate suite as passing. | R21 abs |  |
| AGENTS-130 | §Python environment L243 | Cite the printed record.json for each recorded check. | R21 abs |  |
| AGENTS-131 | §Python environment L243 | Keep source and Git state unchanged while a recorded check runs. | R21 abs |  |
| AGENTS-132 | §Python environment L243 | Claim verification only with status completed, exit zero, stable source, complete capture, valid reports and Docker cleanup; never infer a pass from a record existing. | R21 abs |  |
| AGENTS-133 | §Python environment L244 | If a local full suite fails only from the 3,600 s qualification timeout, same-head all-green PR CI substitutes; still disclose the timeout and cite the incomplete record. | R22 det | → scripts/README.md#local-operations-launcher |
| AGENTS-134 | §Python environment L244 | Any other local failure needs a clean-base reproduction or a fix. | R21 det |  |
| AGENTS-135 | §Python environment L245 | For independent pytest cases, select affected tests first, then add workers; worker count never replaces related-case coverage. | R22 det | → scripts/README.md#local-operations-launcher |
| AGENTS-136 | §Python environment L245 | Run Docker sequence checks through tools/local_verification/run.ps1 and record them. | R22 det | → scripts/README.md#local-operations-launcher |
| AGENTS-137 | §Configuration as code L249 | Default to configuration as code for new or changed configuration the work already touches, especially reused, preserving accepted policy behavior. | R39 abs |  |
| AGENTS-138 | §Configuration as code L251 | Define reusable configuration objects once in a canonical source that consumers reference or compose; never copy. | R39 abs |  |
| AGENTS-139 | §Configuration as code L252 | Separate shared configuration, product/environment variants and instance bindings; make overrides explicit. | R39 abs |  |
| AGENTS-140 | §Configuration as code L253 | Validate the resolved configuration where it is consumed. | R39 abs |  |
| AGENTS-141 | §Configuration as code L254 | Reference credentials; never embed secrets in versioned configuration. | R12 abs |  |
| AGENTS-142 | §Configuration as code L255 | Deployments preserve the resolved configuration's identity and version so validation and activation refer to the same configuration. | R39 abs |  |
| AGENTS-143 | §Key Principle L260 | Run research under its own approved campaign contract. | R23 abs |  |
| AGENTS-144 | §Key Principle L261 | Treat capital authorization as revocable. | R15 abs |  |
| AGENTS-145 | §Key Principle L261 | Neither a parameter lock nor a research result grants capital. | R15 abs |  |
| AGENTS-NEW-1 | §Merges and credentials L235 | Never review your own work as Claude; a separate reviewer, here Codex, must review it. | R5 abs | *at HEAD:* new 488f757 (PR #911) |

</details>

### operational_rules.md — 92 rules


<details><summary><code>docs/operational_rules.md</code> — 92 rules: 38 absorbed, 52 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| OPS-1 | §1 L7 | Never skip or override a valid Pine signal because of a scheduled macro event, headline or volatility forecast; take the trade. | R1 abs |  |
| OPS-2 | §1 L11 | Reduce exposure for a regime only through a formal risk overlay at the sizing layer; never improvise per-trade skips. | R1 abs |  |
| OPS-3 | §2 L17 | Before authoring any brief, ADR or decision doc that specifies risk-control parameters, read the current production code first, not remembered state. | R0 abs |  |
| OPS-4 | §3 L27 | If DXTrade is explicitly reactivated, verify contractValue=10 for DJ30 before any Striker trade. | R10 DEL⚖ | DXTrade/CFD retired by 2026-06-30 ADR, FXIFY DXTrade closed 2026-07-10 (core/csv_parser.py); value 10 survives in core/strategies/CATALOG.md locked table. |
| OPS-5 | §4 L41 | Do not adjust parameters, reduce size or skip signals in response to 3+ consecutive losses on one strategy; treat it as normal variance. | R1 abs |  |
| OPS-6 | §4 L45 | Log a losing streak in docs/SESSIONS.md (on the c1 rail, against M1 telemetry/fill evidence) and keep executing signals. | R1 det |  |
| OPS-7 | §4 L45 | Consider intervention only if the streak exceeds the 5yr backtest p99, no regime shift explains it, and logs show a systematic issue. | R1 det |  |
| OPS-8 | §5 L54 | Pine is the source of truth for strategy parameters; when any document disagrees, Pine wins and the document is fixed. | R14 abs |  |
| OPS-9 | §5 L58 | Exceptions to Pine ownership: dd_protection.py parameters, firm_rules.py allocations and any active overlay live in the Python sizing layer. | R14 det |  |
| OPS-10 | §6 L65 | On any strategy version lock or locked risk/allocation/dd_protection constant change, run a doc/code skew audit before closing the lock commit. | R14 abs |  |
| OPS-11 | §6 L71 | Skew audit covers core/strategies/CATALOG.md and AGENTS.md safeguards, every ADR Code: pointer and version mention, active overlays, and docs/methodology. | R14 det |  |
| OPS-12 | §6 L77 | In ADRs update stale Code: pointers but leave conclusion text intact, adding a parenthetical noting what changed since the decision-era version. | R14 det |  |
| OPS-13 | §6 L85 | Methodology measurements quoting a prior version as observed must be re-measured or marked pre-version-bump archival. | R14 det |  |
| OPS-14 | §6 L75 | When updating unrelated AGENTS.md claims, preserve the recall guard's historical MC literals in place. | R14 det | → AGENTS.md §Strategy Reference |
| OPS-15 | §6 L89 | The skew-audit trigger is the lock event itself, not a calendar cadence or every commit touching core/strategies/. | R14 det |  |
| OPS-16 | §6 L95 | If the audit cannot run inline with the lock, run it in the next repo-touch session and gate that session's decision work on finishing it. | R14 det |  |
| OPS-17 | §6 L97 | Measure and log the doc/code skew window on every lock, logging even a 0-day window. | R14 det |  |
| OPS-18 | §7 L120 | Every fact has one canonical owner; other mentions link to it or are labeled derived mirrors, never silent restatements. | R29 abs |  |
| OPS-19 | §7 L131 | Use the owner table: Pine/CATALOG mirror, LOCK.md, load_bearing_numbers (index, never owner), code constants, mc_anchor_history, STATE, SESSIONS, campaign plans, Iterate blocks, ADR headers, TOMBSTONES. | R29 det |  |
| OPS-20 | §7 L138 | Decisions and rationale live with the owning spec, campaign, plan or PR; create a distinct ADR only under the ADR admission rule. | R32 abs |  |
| OPS-21 | §7 L139 | Independent review mechanics are owned by scripts/README.md#independent-review and its implementation; operator authority stays separate from it. | R5 abs |  |
| OPS-22 | §7 L148 | Treat Claude-project MEMORY.md and memory files as assistive-only: never a Rule 7 owner, a Rule 0/§0 read, or sub-rule 8/10 attestation. | R29 det |  |
| OPS-23 | §7 L151 | STATE.md carries no canonical values (working-tree status, risk %, anchors, versions, hashes, owner tables); it points to owners. | R34 abs |  |
| OPS-24 | §7 L155 | Record executed operator decisions in STATE only as one-line decision-index bullets with an owner link, never dated narrative sections. | R34 abs |  |
| OPS-25 | §7 L159 | Delete closed or retired STATE rows rather than striking them; detail stays with the owning decision record or closure. | R34 det |  |
| OPS-26 | §7 L161 | SESSIONS.md is append-only history that links owners instead of duplicating values; its living header links to STATE for current work. | R34 abs |  |
| OPS-27 | §7 L164 | Write a full SESSIONS entry only for a real judgment call; never add a session stub just to copy the live queue. | R34 det |  |
| OPS-28 | §7 L167 | Keep AGENTS.md §Live-execution posture a pointer block: a new posture decision adds one pointer line with owner link, not a retelling. | R29 abs |  |
| OPS-29 | §7 L171 | The AGENTS.md MC-anchor triple and §Protection are canonical owners resident there (recall guard regex-reads the triple), not mirrors; do not relocate them. | R14 det |  |
| OPS-30 | §7 L177 | README.md links out everywhere; its public-clone note is a one-liner pointing at AGENTS.md §Public-clone posture. | R29 abs |  |
| OPS-31 | §7 L181 | Keep STATE Last curated current, Weekly/Monthly recurring deadlines within 7/31 days, past dated headings marked standalone DISCHARGED; digests or reminders cannot discharge this. | R34 det |  |
| OPS-32 | §7 L191 | If a dated defect traces a material error to missing orientation detail or a lost dormant thread, restore only that STATE block/role and amend Rule 7 with the reason. | R34 det |  |
| OPS-33 | §7 L195 | Do not restore the whole STATE snapshot or owner table by default, copy private project memory into the repo, or commission a memory index/new state store. | R34 det |  |
| OPS-34 | §7 L220 | Before authoring a new pointer/wrapper artifact over a fact family with an outstanding dated debt, land the debt or record an explicit decision to drop it. | R29 det |  |
| OPS-35 | §8.1 L232 | Before classifying a move/delete as isolated cruft, grep its basename across active paths and report caller count in §0; over 3 callers is doctrine-referenced cruft. | R31 det |  |
| OPS-36 | §8.2 L238 | For any move targeting an archive, §0 lists the current archive subtrees to confirm the destination convention. | R31 DEL⚖ | Targets repo-root archive/, which no longer exists (ls); lab moves use scripts/archive_lab_analysis.py; docs/ltm/README owns archive retrieval. |
| OPS-37 | §8.3 L242 | When a brief cites a specific line, the §0 read covers the surrounding section (at least ±20 lines), not the line alone. | R0 det |  |
| OPS-38 | §8.4 L246 | For edits to production code unseen this conversation, §0 reads the actual architecture, proposes the edit shape, and confirms before executing. | R0 det |  |
| OPS-39 | §8.5 L253 | A lock is incomplete until firm_rules, dd_protection, lifecycle and the c1 sizing host reflect it; lock memos include an operational-tooling-integrated checklist item. | R14 det |  |
| OPS-40 | §8.6 L261 | A brief asserting live performance or proposing changes from live behavior must cite the latest edge-captured/fill-quality artifact for that venue. | R0 det |  |
| OPS-41 | §8.7 L271 | Land a pre-registration freeze in its own commit, an ancestor of the first results commit; the run commit must not edit frozen verdict logic. | R23 abs |  |
| OPS-42 | §8.7 L279 | A closure commit may rewrite only the prereg's single Status header line, with the stamp saying so; everything below stays unedited. | R23 det |  |
| OPS-43 | §8.8 L309 | Before opening a new lab/analysis dir or core-adjacent work, §0 pastes literal output of CATALOG, briefs INDEX, git log and check_advisor_dedup searches; bare attestation is void. | R8 det |  |
| OPS-44 | §8.8 L317 | Before the first run or edit on an instrument, or any work naming a candidate mechanism for it, read ops/instruments/<SYM>.md in full, on every surface. | R27 abs |  |
| OPS-45 | §8.8 L347 | At authoring time run scripts/check_instrument_ledger_coverage.py alongside the dedup probe and hand-check docs/rejected_candidates.md hits per symbol. | R8 det |  |
| OPS-46 | §8.9 L358 | Every non-grandfathered closure carries a Registry: line in its Iterate block: a rejected_candidates.md heading for strategy-grounds kills, else n/a with reason. | R26 abs |  |
| OPS-47 | §8.10 L368 | Check and amend the existing owner before opening a new ADR, brief, notice or research slug; routine fixes and in-envelope decisions use the owner or PR. | R29 abs |  |
| OPS-48 | §8 origin L383 | The brief-authoring skill is downstream of Rule 8; on drift between them, the repo text wins. | R29 abs |  |
| OPS-49 | §9 L409 | Read book, legacy locked and candidate Pine in place by the primary checkout's absolute path; never copy it into a worktree, clone, sandbox or scratch dir. | R13 det |  |
| OPS-50 | §9 L418 | Where no local checkout holds the Pine, use the §0 citation chain (audit-doc quote, then LOCK.md, then CHANGELOG/baselines); cite, never infer. | R0 det |  |
| OPS-51 | §9 L423 | Do not edit locked .pine files; Pine edits happen only in the primary checkout. | R14 det |  |
| OPS-52 | §9 L424 | Put new candidate Pine under core/strategies/candidates/, a distinct non-locked path. | R14 det |  |
| OPS-53 | §10 L443 | A session deriving, testing, tuning or adjudicating on an instrument appends a dated disposition entry to its ledger at session end. | R27 abs |  |
| OPS-54 | §10 L454 | Instrument ledgers own only instrument-level findings and concept status; parameters stay in Pine, sizing constants in code, all else links out. | R27 det |  |
| OPS-55 | §10 L457 | Create an instrument ledger on the first session touching a new instrument; do not backfill ledgers for history-only instruments. | R27 abs |  |
| OPS-56 | §10 L449 | The anti-SNAG budget is instrument-level and shared, counted across all sessions, with family sub-ledgers only where mechanisms genuinely differ. | R23 det |  |
| OPS-57 | §10 L463 | When a verdict changes, update the ledger PROFILE block and rebuild the derived view with scripts/instrument_profiles.py build. | R27 det |  |
| OPS-58 | §10 L472 | Opening a new candidate entry mechanism: at Phase 0, before the first backtest, run cost_geometry_pregate.py and record cost_R, band and sub-ATR flag in the ledger (report-only). | R24 det |  |
| OPS-59 | §10 L489 | Feed the cost-geometry check the strategy's realized stop (--realized-stop for structural stops) on the canonical TV 15m series, never an assumed comfortable k·ATR. | R24 det |  |
| OPS-60 | §10 L493 | Never treat a low cost_R as edge evidence; the pre-registered backtest still runs. | R24 abs |  |
| OPS-61 | §11 L511 | When retiring a venue, feed, role or other falsifier input, explicitly migrate, discharge, supersede or retire each affected obligation; an unaccruable input is not a passing check. | R28 abs |  |
| OPS-62 | §11 L516 | For a retained dormant limb name the unavailable input, a re-arm condition and surviving coverage; for permanent retirement record the reason with owner/tombstone, no invented restoration trigger. | R28 det |  |
| OPS-63 | §11 L521 | Never treat an obligation as discharged merely by association with a retired surface. | R28 abs |  |
| OPS-64 | §12 L540 | Merge a [DRAFT]/[HOLD]/'do not merge without X' commit or PR only after an explicit, timestamped, owner-attributed lift comment; never infer approval from the merge actor. | R6 det |  |
| OPS-65 | §13 L559 | Record any venue, broker or counterparty obligation with verbatim quote, source to article/section, date read and explicit scope tag, or do not record it. | R17 abs |  |
| OPS-66 | §13 L572 | If the source is silent on an obligation's scope while scoping sibling rules, read it BROAD; default BROAD on silence, never narrow for comfort. | R17 abs |  |
| OPS-67 | §13 L582 | Never inherit a qualifier the source lacks, even from own notes; when correcting, record where the narrowing entered; a note narrower than its cited spec is a defect. | R17 abs |  |
| OPS-68 | §13 L588 | Read which source prevails from the agreement's own precedence clause before asserting a hierarchy; never assume precedence. | R17 det |  |
| OPS-69 | §14 L628 | Mark a withdrawn, superseded or retracted claim where readers encounter it (headline, verdict, top table), not only in an appended addendum. | R30 abs |  |
| OPS-70 | §14 L637 | For frozen evidence (preregs, closures, signed evidence, lock records) keep the body byte-unedited, add an addendum, and place a reader-intercept banner upstream of the impeached claim. | R30 abs |  |
| OPS-71 | §14 L646 | Correct living documents, same-session work and accepted ADR effective text after an approved revision in place at the assertion site; same-session work is never frozen. | R30 det |  |
| OPS-72 | §14 L652 | ADR revisions keep a dated scope note and immutable prior revision, label Proposed clauses separately, and never unfreeze research evidence, preregs or verdict logic. | R32 det |  |
| OPS-73 | §14 L657 | A withdrawal is incomplete until the withdrawn claim is grepped repo-wide, including sibling modules, publishing docs and artifacts written this session. | R30 abs |  |
| OPS-74 | §14 L664 | Hard-fail in-scope documents whose addendum-confined supersession token has no upstream marker or pointer. | R30 abs |  |
| OPS-75 | §14 L686 | Recompute replacement numbers in a correction from source; never derive them by transforming a published figure. | R30 abs |  |
| OPS-76 | §14 L688 | Keep an artifact's own hedge words ('proxy', 'guard run', 'not gate-grade') verbatim when correcting it. | R30 det |  |
| OPS-77 | §14 L690 | 'Not determinable from the published artifact' is a complete, acceptable answer in a correction. | R30 det |  |
| OPS-78 | §14 L694 | Treat a printed figure as a closed rounding interval (e.g. :.2f is ±0.005); derived inequalities must hold across it; running maxima need not belong to the explained day. | R20 det |  |
| OPS-79 | §15 L704 | Run always-on or unattended services (c1 listener, signal daemon) on an always-on host, not the desktop; the desktop is console-only; never implies unattended dry_run=false. | R41 det |  |
| OPS-80 | §16 L723 | Keep an artifact only if pipeline-consumed, live-safety, re-proposal-bar evidence, a reproducibility manifest, or an open dated obligation (R1-R5). | R31 det |  |
| OPS-81 | §16 L729 | Before removing a carrier, explicitly resolve, migrate or retire its open obligation; an unreachable check is not a pass. | R31 abs |  |
| OPS-82 | §16 L733 | Retention preserves needed content, not the file: consolidate duplicate owners, retrieve completed episodes from history; a citation is a dependency to resolve, not a retention right. | R31 det |  |
| OPS-83 | §16 L736 | For each removed ADR record path, commit/blob, disposition and current owner in docs/adr/TOMBSTONES.md; no hot-stub/cold-body pair is required. | R31 abs |  |
| OPS-84 | §16 L738 | Verify preservation of non-regenerable bytes before removing them. | R19 abs |  |
| OPS-85 | §16 L738 | Looking up history never revives a retired authorization or evades a research re-proposal bar. | R3 abs |  |
| OPS-86 | §16 L741 | Before any deletion commit run quoted-path, pathlib-join, incoming link/fragment/content-reader scans and full pytest; folder location never classifies an artifact as prose. | R31 det |  |
| OPS-87 | §17 L760 | At each quarterly programme audit run check_falsifier_reachability.py --stats and make audit, recording the coverage trend; a clean run never substitutes for a Rule 11 sweep. | R28 det |  |
| OPS-88 | §17 L766 | Keep report-only diagnostics in the audit tier, out of pre-commit and required CI; output that cannot change a merge verdict is observation, not a gate. | R38 abs |  |
| OPS-89 | §17 L771 | Add future standing per-cycle audit tooling runs as bullets in Rule 17's checklist, not as new rules. | R28 det |  |
| OPS-90 | §Rule maintenance L787 | Add a new operational rule only after a specific failure or near-miss; no preemptive rules. | R36 abs |  |
| OPS-91 | §Rule maintenance L789 | Log every edit to an existing rule as a dated one-line edit-log entry stating what changed and why; full narration stays in git log or the linked ADR. | R36 det |  |
| OPS-NEW-1 | §14 L643 | On living rule surfaces, delete superseded text and its marker so the current rule is stated once; Git history is the archive, so add no tombstone. | R30 det | *at HEAD:* new d2bdd726 |

</details>

### Canon and methodology — 208 rules


<details><summary><code>docs/methodology/1r_estimation.md</code> — 7 rules: 1 absorbed, 4 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-183 | Dormant banner L3-11 | Treat the 1R live-calibration verdict as historical and never cite it as current; calc_multiplier and ops/accounts.py are deleted. | R20 abs |  |
| METHOD-184 | §The correction L29-36; L344-348 | Estimate 1R per exit architecture: median loss for unimodal full-stop strategies; mean of full-stop-only losses, or an MAE proxy, for BE/trail/partial strategies. | R20 det |  |
| METHOD-185 | §Equity-compounding normalization L38-52 | Report 1R as a percent normalized by equity at entry (equity at close acceptable), never by fixed initial capital. | R20 det |  |
| METHOD-186 | §Reproducibility requirement L350-358 | In every portfolio MC run, state and log each strategy's 1R estimator and values and cite this doc; keep unlogged runs out of portfolio decisions. | R21 det |  |
| METHOD-187 | §Relationship to April 17 L364 | Do not revert to median-loss 1R for bimodal strategies without explicit reasoning in a dated decision record. | R20 det |  |
| METHOD-188 | §Striker re-cal L184-193; L294-299 | Flag the Striker initial-entry tail as a re-cal-trigger candidate at next MC pre-flight; look for layer-2 pyramid divergence at the 6-month live reconciliation. | R14 DEL⚖ | Historical: CFD Striker legs withdrawn (ADR 2026-08-04 venue descope); AGENTS.md says no live book, so live reconciliation never fires. |
| METHOD-189 | §Pre-staged Forward question L235-271 | Pre-stage the per-trade hard-cap versus live-tripwire choice for the next allocation review or 6-month live reconciliation. | R28 DEL | Superseded: doc names Q-TRADECAP-2 election and docs/briefs/closures/Q-TRADECAP-2-closure-resolved.md as owner; CFD-era fork not live. |

</details>

<details><summary><code>docs/methodology/README.md</code> — 1 rules: 0 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-200 | L1, L20-21 | Keep docs/methodology/ for standing method, not session narrative; earned hard rules live in docs/operational_rules.md. | R29 det |  |

</details>

<details><summary><code>docs/methodology/backtest_live_shrinkage.md</code> — 7 rules: 0 absorbed, 7 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-176 | Status L3-8 | Never apply the shrinkage convention silently as a sizing haircut; any go-live haircut is a separate gated decision via the lifecycle ladder and operator GO/NO-GO. | R15 det |  |
| METHOD-177 | §The base rate L26-41 | Plan for live to retain roughly 30-70% of backtest edge; heavily searched edges retain less, low-capacity edges decay slower. | R15 det |  |
| METHOD-178 | §The convention 1 L47-49 | State the live-retention assumption explicitly in the pre-registration or admission doc, justified by search intensity and capacity; an unstated assumption defaults wrongly to 100%. | R23 det |  |
| METHOD-179 | §The convention 2 L50-54 | Size on the shrunk lower-confidence-bound edge, not the point estimate; any ramp-up is an operator decision. | R15 det |  |
| METHOD-180 | §The convention 3 L55-57 | Carry retention as a falsifiable expectation; reconciliation locates where live lands in the band. | R15 det |  |
| METHOD-181 | §Relationship to ECR L59-76 | Do not conflate the ex-ante shrinkage prior with ex-post ECR; ECR measures execution fidelity, not decay, which Call-1 rolling PF catches. | R15 det |  |
| METHOD-182 | §Where it applies L80-96 | Apply the convention only to new live underwriting such as discovery Stage-8 survivors, never retroactively to locked-book allocations, dd_protection, the MC anchor or Pine constants. | R14 det |  |

</details>

<details><summary><code>docs/methodology/external_mapping_guardrails.md</code> — 5 rules: 0 absorbed, 5 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-123 | Header L6 | Require fresh owner GO for a fourth or later external-framework or peer-firm mapping instance; do not re-derive prior instances. | R3 det |  |
| METHOD-124 | Guardrail 1 L10 | Ensure a proposed mechanism's declared pipeline stage matches its actual input/output reach; informing another stage's decision is altitude conflation. | R36 det |  |
| METHOD-125 | Guardrail 1 L12 | Before proposing new machinery, check for an existing same-shaped repo tool (gate-reachability-audit, adversarial panel, verify-source, arming interlock) it would reinvent. | R36 det |  |
| METHOD-126 | Guardrail 2 L16-18 | When an LLM re-prompt, tag or write-up yields a number feeding any gate or budget, build the check into operative logic via deterministic computation; narration is not the check. | R21 det |  |
| METHOD-127 | §What a survivor looks like L22 | Favor proposals that are one-line additions to an existing deterministic check with zero LLM judgment on the decision path. | R36 det |  |

</details>

<details><summary><code>docs/methodology/inqhiori-canon.md</code> — 52 rules: 17 absorbed, 32 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-1 | Scope L11 | Use INQHIORI for structural, low-reversibility or statistically-gated decisions; run tactical/recoverable work as OODA; no one-sentence falsifiable hypothesis means not INQHIORI work. | R9 det |  |
| METHOD-2 | §1 L30 | Run the D-S-A pre-Q gate on the Identify/Notice corpus (filter, compress, index) before asking any Question. | R9 abs |  |
| METHOD-3 | §2 L42 | Name which D-S-A domain (data, system, meta-process, or pursuit) a pass acts on; never conflate domains. | R9 det |  |
| METHOD-4 | §3 L46-53 | Order brief/audit headers: Title, D-S-A domain line, Context, Sources Read block, Pre-Q gate header, then Q, H, Method, Verdict criteria, Cross-references, Recursion note. | R33 det |  |
| METHOD-5 | §3 Sources Read L55-75 | Add a Sources Read block after Context declaring past chats queried, files read in full or part, memory use, and every unused available tool with its own rationale. | R33 det |  |
| METHOD-6 | §3 L77 | Read production sources (code, prior chats, briefs) before any analytical claim; memory is supplementary, and primary memory use needs a written rationale. | R0 abs |  |
| METHOD-7 | §3 Pre-Q gate header L79-90 | Add a three-line Pre-Q gate header (D items and test, S rationale, A index); any 'no action' line must state why the gate did not engage. | R9 det |  |
| METHOD-8 | §3 D-S-A domain header L92-100 | Put a one-line D-S-A domain header after the title; a multi-domain brief declares each domain and calls out the cascade. | R33 det |  |
| METHOD-9 | §3 Forbidden patterns L102-110 | Stop and re-source if Sources Read weakens Rule 0 ('in spirit', 'analogue'), claims memory suffices without negative tool calls, blanket-dismisses tools, leaves unused-tools empty, or cites vague times. | R0 det |  |
| METHOD-10 | §4 D L116-122 | Log the relevance test behind every deletion; preserve the raw I/N corpus as the Rule 0 anchor and delete only from a derived working set. | R9 det |  |
| METHOD-11 | §4 S L124-129 | Simplify only to representations that preserve the Noticed anomaly; if simplification removes the signal, revert. | R9 det |  |
| METHOD-12 | §4 A L131-136 | Keep Accelerate bounded: indexing must cost less than the queries it enables; expensive indexing of data you may never query is misapplication. | R9 det |  |
| METHOD-13 | §5 L138-144 | Apply the D relevance test: keep any datum whose presence could contradict a not-yet-formed hypothesis; if judging it needs the hypothesis, keep it. | R9 det |  |
| METHOD-14 | §5 Forbidden D-tests L146-151 | Never delete corpus data by tests of known mechanism, model fit, signal-to-noise, or past usefulness. | R9 det |  |
| METHOD-15 | §5 Permitted D-tests L153-160 | Delete only via permitted tests (documented artefact, higher-fidelity duplicate, out of scope, literal copy); write, declare and audit-log any new test. | R9 det |  |
| METHOD-16 | §6 guardrail 1 L164 | Keep gate effort within about 10% of I/N effort; exceeding it means I/N was wrong, so restart the outer loop instead of extending the gate. | R9 det |  |
| METHOD-17 | §6 guardrail 2 L165 | When a deleted datum later proves to matter, run a gate audit reviewing the criterion, logged at docs/notes/audits/YYYY-MM-DD_gate_<slug>.md. | R9 det |  |
| METHOD-18 | §6 guardrail 5 L168 | Log every iteration that resurfaces gate-deleted data; repeated failures of one criterion mean the D-test class is too aggressive. | R9 det |  |
| METHOD-19 | §8 L226 | Deletion on a framework (meta-process) may cascade to the data it produced; deletion on data alone never authorizes framework changes. | R9 det |  |
| METHOD-20 | §9 Backfill L240-242 | Add §3 Sources Read blocks to Q1/Q5/Q8 before their execution audits, pairing drafting and execution-time Sources Read blocks. | R33 DEL | Discharged: canon §9 heading records Q1/Q5/Q8 closed 2026-04-29, kept only as worked example; one-off backfill has no target. |
| METHOD-21 | §10 L247 | Apply the small-cell variance prior: small cohorts trigger caution at Observe/Reflect regardless of how the gate filtered the corpus. | R1 abs |  |
| METHOD-22 | §10 L248 | Build no overlay without a full INQHIORI loop; the pre-Q gate never relaxes the back of the loop. | R1 det |  |
| METHOD-23 | §10 L249 | Route narrative observations via the Notice log (docs/notes/notice/N-YYYY-MM-DD-slug.md, GRADUATE/DROP/HOLD), not Closed/Action/Forward. | R33 abs |  |
| METHOD-24 | §10 L250 | Reference the gate-audit slug in trade-journal entries derived from a gated INQHIORI loop. | R9 DEL | References retired surface: ops/live_journal removed by ADR 2026-07-11-ops-cfd-estate-retirement (ls confirms absent); no trade-journal target exists. |
| METHOD-25 | §10 L251 | Write gate audits to docs/notes/audits/YYYY-MM-DD_gate_<slug>.md with deleted items, D-test, S rationale, A index and regret events. | R9 det |  |
| METHOD-26 | §11 L253-261 | Do not restate strategy parameters, allocations, dd_protection literals or re-MC triggers in methodology docs; link Pine, firm_rules, dd_protection and owning ADRs. | R29 abs |  |
| METHOD-27 | §12 L276 | Update CLAUDE.md to reference this canon as the primary methodology entry point. | R29 DEL | Superseded: CLAUDE.md retired 2026-09-20 per charter addendum (file absent); AGENTS.md already links inqhiori-canon.md. |
| METHOD-28 | §13 L281 | Use this canon, not the orthogonal-framing predecessor pages, for INQHIORI operational discipline; predecessors are definitional archives only. | R29 abs |  |
| METHOD-29 | §13 L284 | Agents only propose D-step deletions; Joshua authorizes them. | R3 abs |  |
| METHOD-30 | §13 L285 | On detecting a forbidden D-test, stop, log and surface it to the user before retrying; never substitute a permitted test yielding the same deletion. | R9 det |  |
| METHOD-31 | §14 L289 | Where this canon and its ADR of record (three-loop binding, Rule 2, Iterate exit) disagree, the ADR wins. | R29 abs |  |
| METHOD-32 | §14 table L291-296 | Bind methodologies to loops: GRAND uses the Quintessentials, STRATEGIC The Algorithm, OUTER INQHIORI, INNER OODA. | R9 det |  |
| METHOD-33 | §14 L298 | Declare a Loop-of-Record (authority tier) for every D-S-A pass alongside its object domain. | R9 abs |  |
| METHOD-34 | §14 L298 | Treat programme/track/instrument Delete verdicts as STRATEGIC acts, valid only via programme-audit cadence, a fired pre-registered stopping rule, or explicit owner adjudication. | R3 det |  |
| METHOD-35 | §14 L298 | Lower-loop sessions may propose Strategic Deletes but never execute them on local momentum (no-borrowing). | R3 abs |  |
| METHOD-36 | §14 L298 | Track add-back rate at programme audits in two layer-segregated forms, never pooled: methodology audits cite only signal add-back, portfolio audits only strategy add-back. | R28 det |  |
| METHOD-37 | §14 L298 | Judge the roughly 10% deletion-calibration band per instrument, never on a pooled figure. | R28 det |  |
| METHOD-38 | §14 GRAND L300-304 | Open a GRAND-tier pursuit only with an entry record (Aim, Measure, Survive bound, review date); KEEP/PARK/MERGE/SUBTRACT dispositions are operator-gated. | R28 det |  |
| METHOD-39 | §14 GRAND L304-306 | Subtract acts on whole pursuits and hands off to The Algorithm's Delete for parts of surviving pursuits; do not conflate the two. | R28 det |  |
| METHOD-40 | §14 L311 | Map loops to lifecycle stages: STRATEGIC funds stage 1 and owns stage-5 kill/scale verdicts; OUTER runs stages 1-2; INNER runs stage 3. | R9 det |  |
| METHOD-41 | §15 L317 | Apply Rule 2 to all substantial work, not only INQHIORI entry; the ADR addendum defines substantial work and the one-line budget. | R2 abs |  |
| METHOD-42 | §15 L321-325 | Before starting, declare an iteration budget scaled to reversibility: INNER 3 (self-extend once with reason), OUTER 8, STRATEGIC 3 OUTER investigations; OUTER/STRATEGIC never self-extend. | R2 det |  |
| METHOD-43 | §15 L327 | On hitting the budget, make a structured stop (spent, remaining, state, extend-or-stop recommendation tagged by reversibility); never silently continue or finish. | R2 abs |  |
| METHOD-44 | §15 L329-331 | On overrun, STOP if recoverable; STOP and re-audit from Rule 0 ground truth if irreversible. | R2 det |  |
| METHOD-45 | §15 Corollary 1 L334 | Never resolve budget exhaustion by shipping an under-validated irreversible change; exit only by re-audit on a new budget or owner escalation. | R2 det |  |
| METHOD-46 | §15 Corollary 3 L336 | Scale every budget to stakes; a flat budget is a Rule-0 violation. | R2 abs |  |
| METHOD-47 | §15 Falsifier L338 | Log tripwire firings in docs/notes/audits/rule-2-trip-log.md; validate the 3/8/3 thresholds forward only, never re-derived from the cfg00-12 history. | R2 det |  |
| METHOD-48 | §16 L346 | End every closure with a typed Iterate block: verdict used, model update, Next: INTEGRATE\|ITERATE\|STOP, routing, entry packet, stop rule, board write. | R28 abs |  |
| METHOD-49 | §16 rule 1 L350 | Treat STOP as Iterate with budget zero, recording the re-proposal bar. | R28 abs |  |
| METHOD-50 | §16 rule 2 L351 | ITERATE names a successor and freezes its entry packet but never opens it; opening needs fresh operator GO and automation never promotes. | R28 abs |  |
| METHOD-51 | §16 rule 3 L352 | Let the closure Iterate block own per-Q forward disposition; STATE board rows and SESSIONS Open/next are pointer mirrors; record which pointer was written. | R28 abs |  |
| METHOD-52 | §16 L354 | Pre-register the INTEGRATE/ITERATE/STOP disposition for each verdict in the brief's §6. | R23 det |  |

</details>

<details><summary><code>docs/methodology/objective_composition_map.md</code> — 10 rules: 4 absorbed, 6 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-190 | Header L4-5; §What this map is not L73-77 | Treat the map as an inert lookup, not a gate or charter; update it when an Accepted ADR, RATIFIED spec or FROZEN pre-registration changes a decision class or precedence. | R29 det |  |
| METHOD-191 | §Candidate admission L17-18 | Govern candidate admission by the FROZEN survivor-scoring v2 Part A gate: bust ceiling plus pass rate on 2+ firms, one trailing_locking. | R24 abs |  |
| METHOD-192 | §Candidate admission L20; §Rung selection L33 | Never extend the rung-selection EV objective to candidate admission; admission and rung sizing are separate instruments that never adjudicate the same decision. | R24 det |  |
| METHOD-193 | §Candidate admission L22-25; §Book composition L41 | Treat Stage-8 risk-breadth and third-leg screens as necessary but never sufficient, and never a substitute for the admission or composed-bust gate. | R24 det |  |
| METHOD-194 | §Rung selection L29, L35 | Choose rungs by EV per dollar-day only among rungs passing both-halves regime robustness; a higher rung needs a fresh both-halves PASS plus an admitting ADR. | R24 det |  |
| METHOD-195 | §Book composition L39 | Gate book composition by the Part-A composed-bust ceiling through a joint MC under account segregation. | R24 abs |  |
| METHOD-196 | §Book composition L43 | Run hard structural and compliance screens (hedging, cap, session, instrument class) first; a SCREEN-FAIL closes the candidate before risk-breadth scoring. | R24 det |  |
| METHOD-197 | §Hedging L49 | Never hold a short-capable or opposing-sign Equity Index leg alongside a long Equity Index leg on one account or any account under the same control. | R16 det | → ops/prop_envelope_default.md §4a |
| METHOD-198 | §Protection sizing L55 | Treat dd_protection (trigger, scale, reference_mode) as per-instance; a new instance needs pre-registered re-MC, the both-halves regime gate and an admitting ADR. | R14 abs |  |
| METHOD-199 | §Program-level success L67 | Apply the four-firms §4 falsifier: at least 2 of four FRIENDLY tiers clear the bust ceiling by 2026-11-08, else demote to research-only. | R28 abs |  |

</details>

<details><summary><code>docs/methodology/observation_routing.md</code> — 9 rules: 4 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-114 | Status L4-14 | Read the 2026-08-15 Notice-log ADR before citing observation_routing.md as current doctrine elsewhere. | R33 abs |  |
| METHOD-115 | §The gate L41-66 | Route every observation to exactly one of Closed (one paragraph, no standing artefacts), Action (owned change plus verification) or Forward (cheapest-falsification-first question). | R33 DEL⚖ | Superseded: ADR 2026-08-15 §2 downgrades three-bucket routing to an optional tag; that ADR rules out deleting the concept, so operator call. |
| METHOD-116 | Status L11-14 | Treat /lock-check (verify_lock_anchors.py) Closed/Forward/Error exits as the sole live use of three-bucket routing, for one mechanical lock-anchor check. | R14 det | → docs/adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md §2 |
| METHOD-117 | §Closed L48-51; failure modes L86-88 | Do not keep standing regenerable artefacts for closed findings; regenerate only to defend a specific decision. | R31 abs |  |
| METHOD-118 | §Action L57-58; failure modes L89-91 | Never route an observation straight to a code, config or risk change; Action needs a triggering rule (Rule 0, live-PnL gap versus MC, documented re-MC trigger). | R1 det | → docs/methodology/inqhiori-canon.md §10 |
| METHOD-119 | §Why L25-28 | Propose no overlay from a regime story or bar-stat shift; only a live-PnL gap versus MC justifies one. | R1 det | → docs/methodology/inqhiori-canon.md §10 |
| METHOD-120 | §Why L29-30 | Recognize documented re-MC triggers: six months live data, version bump, allocation outside safe band, dd_protection constant change. | R14 det | → .claude/skills/prop-firm-challenge/SKILL.md §Re-MC triggers |
| METHOD-121 | §Forward L62-66; failure modes L92-95 | Do not pull a Forward question into the current session until its gate has actually fired. | R28 abs |  |
| METHOD-122 | §Failure modes L96-99 | Keep any routing gate lighter than what it replaces; simplify further if sub-procedures add forward-loaded artefacts. | R36 abs |  |

</details>

<details><summary><code>docs/methodology/prefilter_rank_correlation_gate.md</code> — 4 rules: 2 absorbed, 2 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-128 | §Invariant L7-14 | Give a pre-filter tier no gate authority until it clears the frozen Spearman rank-correlation floor and parity band against the authoritative engine. | R24 det |  |
| METHOD-129 | §Gen-2 application L18-23 | In each DISC-CAMP run vectorbt and Nautilus on one pre-registered grid; below the rho floor triage loses shortlist authority; record rho and parity in manifest §5. | R24 det |  |
| METHOD-130 | §Falsifier L37 | Never tune the rho floor after seeing campaign results; any threshold change needs a fresh pre-registration. | R23 abs |  |
| METHOD-131 | §Provenance L28-33 | Take the live admission floor from the W4 ADR: survivor-scoring G0-G5+G8 with DSR live; SPA/StepM and PBO/CPCV are dormant. | R24 abs |  |

</details>

<details><summary><code>docs/methodology/regime_robustness_gate.md</code> — 27 rules: 3 absorbed, 23 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-53 | §What this gate is L14 | Before recommending a LOCK CANDIDATE on a risk-control constant, pass a 6-month block bootstrap and a half-panel split, both pinned to the brief's full-panel pass-rate floor. | R24 det |  |
| METHOD-54 | §When this gate fires L22-25 | Run the gate mandatorily for dd_protection constant changes or new dd_geometry instances, risk-constant Pareto relaxations, and single-panel MC comparisons where regime mix matters. | R24 det |  |
| METHOD-55 | §When this gate fires L27-33 | Do not require the gate for strategy-parameter, allocation, strategy add/remove, operational, ORB/venue-native research or OODA-routed decisions. | R24 det |  |
| METHOD-56 | §When this gate fires L35 | If applicability is uncertain and a risk-constant LOCK CANDIDATE is in play, run the gate; never run it as ceremony without a risk-constant change. | R24 det |  |
| METHOD-57 | §When this gate fires L37-43 | Never import this gate as a per-candidate rider outside its scope with its consequence fixed before it runs; in-scope use must treat FAIL as a real falsifier. | R24 det |  |
| METHOD-58 | §Part A L51 | Do not substitute the 'cme' breadth research panel for the locked panel; no MC-engine-eligible replacement panel is admitted. | R18 det |  |
| METHOD-59 | §Part A L49-56 | Bootstrap 6-month contiguous blocks into 100 alternate panels, rerun full MC at the parent seed count, record pass/bust/p99 DD, and take the 5th-percentile pass rate. | R24 det |  |
| METHOD-60 | §Part B L58-64 | Split the panel at a documented point (midpoint default, regime boundary preferred, unequal halves allowed) and run full MC on each half at the parent seed count. | R24 det |  |
| METHOD-61 | §Part C L66-76 | Pass only if bootstrap 5th-percentile, H1 and H2 pass rates all meet the floor; any miss rejects the candidate as regime-fragile despite full-panel dominance. | R24 det |  |
| METHOD-62 | §What it does NOT catch L92 | Treat a gate pass as necessary, not sufficient; the author must still judge the residual out-of-distribution uncertainty haircut. | R24 det |  |
| METHOD-63 | §Relationship L106 | When a gate failure surfaces a partition hypothesis, also run the Rule 1 partition permutation; when in doubt, run both. | R1 det |  |
| METHOD-64 | §Worked non-example L158 | Leave FROZEN source documents byte-unedited; land corrections upstream where the error is read (Rule 14). | R30 abs |  |
| METHOD-65 | §Edge cases L165 | Require at least 4 blocks at the chosen block size (24+ months for 6-month blocks); otherwise use justified 3-month blocks or reject the brief. | R24 det |  |
| METHOD-66 | §Edge cases L169 | Use bootstrap n=100 by default; raise to n=200 when the 5th percentile is within 1pp of the floor. | R24 det |  |
| METHOD-67 | §Edge cases L171 | If every candidate fails the gate, close with HOLD and confirm the locked config. | R24 det |  |
| METHOD-68 | §Edge cases L173 | Set the gate floor equal to the brief's full-panel pass-rate floor; never introduce a separate regime floor. | R24 det |  |
| METHOD-69 | §Edge cases L175-178 | Sanity-check runs: bootstrap p5 above full-panel pass rate means a bug; p95 below it flags an anomalous panel; H1+H2 path counts should approximate the full panel. | R24 det |  |
| METHOD-70 | §Implementation notes L192-194 | Graduate the regime-gate procedure into a shared library once a second brief invokes it. | R24 DEL | Discharged: regime_robustness_gate.md L194 marks it discharged; core/mc/modes.py:860 _run_half_panel exists. |
| METHOD-71 | §Implementation notes L190-201 | Use core/mc/modes.py::_run_half_panel as the canonical implementation before the listed reference scripts and harness templates. | R24 det |  |
| METHOD-72 | §Implementation notes L202-204 | Before reusing any regime-gate candidate script, read its CANDIDATES/CONFIGS list; most omit the unmodified LOCKED config. | R0 det |  |
| METHOD-73 | §Implementation notes L206-207 | Write a gate-invoking brief's script under lab/analysis/<theme>/<slug>/, never under docs/briefs/. | R37 abs |  |
| METHOD-74 | §Re-MC trigger registration L213-219 | Sequence a LOCK CANDIDATE: gates clear, surface to Joshua, approval, commit constant, immediate full re-MC on all locked seeds, then ADR. | R14 det |  |
| METHOD-75 | §Re-MC trigger registration L221 | Reject any brief that bundles the downstream re-MC and lock ADR into the gate-running brief (Rule-0 violation). | R14 det |  |
| METHOD-76 | §Provenance L229 | Re-evaluate bootstrap n and the percentile threshold if the locked panel grows substantially or the seed count changes. | R24 det |  |
| METHOD-77 | §Cross-references L237-238 | Build rule1_gate.py only when a live n<=10 or partition investigation needs it, recording that decision in its owner or PR. | R1 det |  |
| METHOD-78 | §Cross-references L238-242 | Keep the Rule 1 numeral (prefix changes via the conventions audit); keep Rule 1, MC-calibration history and GRAND Anchor separate; preserve the Notion-verbatim Rule 1 archive. | R1 det | → docs/methodology/inqhiori-canon.md |
| METHOD-79 | §Cross-references L242, L247 | Treat historical MC figures as non-authoritative for sizing; cite tests/core/test_mc_synthetic_engine.py for engine regression, never deleted test_mc_anchors.py. | R20 abs |  |

</details>

<details><summary><code>docs/methodology/strategy_harvest.md</code> — 44 rules: 5 absorbed, 39 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-132 | Header L5; §8 L213 | Treat strategy_harvest.md as canonical harvest procedure only while its owner ADR is Accepted. | R25 abs |  |
| METHOD-133 | Header L6 | For in-ceiling sandbox admits, operator budget approval replaces per-candidate GO before capital action; Stage-0, K and ceiling-crossing GOs still stand. | R15 det |  |
| METHOD-134 | Header L7-16 | Follow the harvest chain: seed manifest, intake screen, operator inventory ratification, HARV scoping, register_search open, data pull, stage24, realism, survivor scoring. | R25 det |  |
| METHOD-135 | §1 L24 | Do not screen a seed that fails any admission requirement; route it to a recovery path or drop it with the failure named. | R25 det |  |
| METHOD-136 | §1 Requirement 1 L28 | Path 1a: state ex ante WHO pays (a constraint, not a preference), WHEN (declared before data), WHY it survives (capacity argument), HOW it dies (constraint observable). | R25 det |  |
| METHOD-137 | §1 Requirement 1 L28 | Path 1b: admit a mechanism-less anomaly only with 3+ decades, 3+ independent cohorts, a replication 10+ years later, and no known sign reversal; otherwise it is no seed. | R25 det |  |
| METHOD-138 | §1 Requirement 2 L29 | Require cohort-cited delta/sigma on the target instrument's own cohort, conservative and decay-haircut; never transplant across instruments or invent a number; no delta means UNSCREENABLE. | R25 det |  |
| METHOD-139 | §1 Requirement 3 L30 | Disclose K_banked(family), re-read from closed manifests, in every pre-registration and screen row; it never enters K_eff or fails a seed. | R23 det |  |
| METHOD-140 | §1 Requirement 4 L31 | Require confirm-power of at least 0.50 at the declared OOS event count via the frozen formula; treat monthly-event bp-scale mechanisms as presumptively dead. | R25 det |  |
| METHOD-141 | §1 Requirement 5 L32 | No universal cost-law admission gate; each candidate's evaluation estimates its own net return, execution uncertainty and cost sensitivity. | R25 det |  |
| METHOD-142 | §1 Confirm-not-mine L34 | Declare at most 3 fixed hypothesis expressions (K_intrinsic) at admission; any later widening voids the screen and needs a fresh manifest and screen. | R23 det |  |
| METHOD-143 | §1 Relief valve L38 | Check Path 1b before dropping a seed with no named mechanism. | R25 det |  |
| METHOD-144 | §1 Relief valve L39 | A rank-6 seed lacking an independent cohort may fund a delta-extraction probe, costing data spend and K, instead of dying. | R25 det |  |
| METHOD-145 | §1 Relief valve L40 | Re-screen an UNSCREENABLE seed when its missing input is supplied or at the next quarterly review, whichever comes first. | R25 det |  |
| METHOD-146 | §1 Relief valve L41 | Keep mechanism-level foreclosure binding via rejected_candidates.md and its per-entry re-proposal bars. | R26 abs |  |
| METHOD-147 | §1 Profile consult L43-54 | Before screening, declare the (instrument, mechanism-class) cell and record scripts/instrument_profiles.py cell output; the pre-registration must name and address any binding prior. | R27 det |  |
| METHOD-148 | §2.1 L60-64 | Prioritize sourcing Tier A (low-frequency, large-delta, futures-native); Tier B only if event rate clears Requirement 4; Tier C graveyard-watch, delta net of costs, no size carve-out. | R25 det |  |
| METHOD-149 | §2.3 Channel liveness L74-79 | At channel open, declare a reachable liveness ceiling (attempt count and/or time horizon) and exactly one consequence: retirement or mandatory redesign. | R28 det |  |
| METHOD-150 | §2.3 Channel liveness L82-83 | Treat a fired channel ceiling as making its consequence due, not executed; the operator enacts it and no campaign opens meanwhile. | R28 det |  |
| METHOD-151 | §2.3 Channel liveness L83-87 | Before ratifying a ceiling, audit that it can fire and that campaign opening consults it; UNREACHABLE or UNBINDING fails; no universal ceiling or Confirm-only yield. | R23 det |  |
| METHOD-152 | §2.3 Channel liveness L89-97 | Give each of the five existing channel owners a dated reconciliation mapping its ceiling to a consequence, without changing numeric bounds or yield units. | R28 det |  |
| METHOD-153 | §2.3 L107 | Record CHANNEL-FAIL at the channel owner, never in candidate WHY-rejected registers. | R26 det |  |
| METHOD-154 | §2.3 L108-109 | Govern campaign K and confirm-family accounting by the candidate-contract ADR. | R23 abs |  |
| METHOD-155 | §2.3 L115-116 | Treat the six HARV ranks as sourcing methods, not separately chartered channels; do not duplicate owners' ceiling numbers. | R25 det |  |
| METHOD-156 | §2.3 ranks L120-125 | Scope rank-1 citation traversal; never cite rank-5 encyclopedias directly; check Requirement 4 before manifesting COT seeds; rank-6 sources need a delta-extraction probe. | R25 det |  |
| METHOD-157 | §2.3 L126-127 | Do not source under the retired structural-flow-census rank. | R25 det | *at HEAD:* removed: Struck 1-tie census rows deleted; retirement now only in ADR 2026-08-24 (d2bdd726, PR #909). |
| METHOD-158 | §2.4 L131 | Run the sourcing radar on existing quarterly review dates without a new scheduler: scoped citation traversal from new Tier-A axes, survey harvest, shape pre-check, stage survivors. | R25 det |  |
| METHOD-159 | §2.4 L131 | Inherit the frozen Q1-Q6 query families by reference and never edit them; new families need their own pre-registration. | R23 abs |  |
| METHOD-160 | §2.4 L131 | Shape pre-check staged candidates against the venue feasibility region read from the live RESULTS §6.3 per-shape/risk table, never a flat band; record and drop shape-kills. | R25 det |  |
| METHOD-161 | §2.4 L131 | Build an on-demand Semantic Scholar script only once seed volume justifies it. | R25 det |  |
| METHOD-162 | §2.4 Dedup L135 | Dedup before manifest work against rejected_candidates.md, closed manifests and rejected_signals.md; a dead class stays dead under new citations; re-proposal needs new mechanism evidence. | R26 det |  |
| METHOD-163 | §3 L139 | Inherit Clause N, floor ladder, Cap and DSR/V from frozen Q-KBUDGET-1 §B and defer on divergence; Clause K follows this doc and the 2026-08-04 ADR. | R23 det |  |
| METHOD-164 | §3 Clause K L141 | Set K_eff equal to K_intrinsic, counting every varied axis (sweeps, gates, exits, best-of-K); PASS only if the floor is within Cap, i.e. K_eff at most 3. | R23 det |  |
| METHOD-165 | §3 Asymmetry L143 | Treat a screen FAIL as strong and a PASS as licensing only campaign scoping; all downstream gates still bind and discovery never blesses. | R25 abs |  |
| METHOD-166 | §3 Harness L144 | Screen new seeds by adding an axis_screen manifest row; never write new screen code. | R25 det |  |
| METHOD-167 | §3 L146 | Report every screen verdict with required-quality percentile context (floor versus median and top-decile Sharpe) so a PASS does not read as cheap. | R21 det |  |
| METHOD-168 | §4 L150-154 | Use the conservative central delta derivation, plug the lowest defensible value with its break-even, and record the net-of-cost caveat. | R25 det |  |
| METHOD-169 | §5 L156-190 | File one seed manifest per seed with every template field (rank provenance, K_intrinsic enumerating all varied axes, dedup attestation); an incomplete manifest is unscreenable. | R25 det |  |
| METHOD-170 | §6 step 3 L196 | Screen with zero data pulls and zero K; record FAIL and UNSCREENABLE rows below the line in the inventory, never silently drop them. | R25 det |  |
| METHOD-171 | §6 step 4 L197 | Obtain operator ratification of each inventory addition and record its anchor commit in the manifest. | R3 det |  |
| METHOD-172 | §6 step 5 L198 | Scope campaigns under HARV with a Stage-0 pre-registration carrying per-clause reachability attestation (HARD gate); inherit defaults and DSR-K by reference. | R23 det |  |
| METHOD-173 | §6 step 6 L199 | Open via register_search (mechanism-first default); it refuses without manifest write when floor exceeds Cap, power is below 0.50, or an N-EDGE limb fails. | R23 det |  |
| METHOD-174 | §6 step 6 L199 | Estimate data cost before any pull and enforce the IS/OOS date cap. | R18 det |  |
| METHOD-175 | §6 step 7 L200-202 | Send survivors to prop survivor-scoring at the frozen band (G0-G5+G8); change G6/G7 only by close-and-reopen of the frozen pre-registration. | R24 det |  |

</details>

<details><summary><code>docs/methodology/strategy_lifecycle.md</code> — 34 rules: 6 absorbed, 27 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| METHOD-80 | Header L3-5 | Treat strategy_lifecycle.md as canonical owner of authorization-axis values; AGENTS.md, code and STATE.md point here while the ADR carries the reasoning. | R15 abs |  |
| METHOD-81 | Header L8 | Classify WATCH-tier demotions as reversible OUTER acts needing no STRATEGIC sign-off; only RETIRED and full beta shutdown are STRATEGIC instrument-tier Deletes. | R15 det |  |
| METHOD-82 | §Two axes L18-21 | Keep strategy parameters LOCKED and immutable (stops, targets, risk%, pyramid, session, BE/trail, Pine); capital authorization is a separate always-revocable graded axis. | R15 abs |  |
| METHOD-83 | §Two axes L22, L26 | Set a durability-source tag (MECHANISM or SURVIVAL-ONLY) at go-live; describe a live strategy as version, LOCKED, authorization tier, durability source. | R15 det |  |
| METHOD-84 | §Two axes L24 | Treat venue binding (BOOK, VENUE EDITION, DEPLOYMENT) as a third axis owned by the venue-binding ADR, not by this table or core/lifecycle.py. | R15 abs |  |
| METHOD-85 | §Two axes L28 | Because the lifecycle multiplier only reduces size, a de-risk never needs a re-MC; the axis composes with dd_protection and observation routing, replacing neither. | R15 det |  |
| METHOD-86 | Call 1 L38 | Trip decay on rolling live PF versus its MC/backtest baseline; ECR corroborates but never trips; do not treat the deleted ecr_rolling.py as live. | R15 det |  |
| METHOD-87 | Call 1 L39-40 | Demote one tier when rolling live PF stays below baseline minus 1.0 sigma of the MC PF distribution for two consecutive review windows. | R15 det |  |
| METHOD-88 | Call 1 L41 | At CANDIDATE standing, a Call-1 breach raises only an operator review flag, never an autonomous tier step. | R15 det |  |
| METHOD-89 | Call 1 L42 | Treat decay floors as pre-registration against future data; the ADR §6 AMBIGUOUS clause governs; re-confirm at 2026-11-08 if the live trade count is short. | R15 det |  |
| METHOD-90 | Call 2 L46 | Express authorization as discrete stepped tiers, never a smooth confidence-driven sizing curve. | R15 det |  |
| METHOD-91 | Call 2 L48-55 | Use the ratified tier ladder AUTHORIZED 1.00x, WATCH-1 0.50x, WATCH-2 0.25x, RETIRED 0.00x. | R15 det |  |
| METHOD-92 | Call 2 L57-63 | Apply the lifecycle multiplier at the risk_pct layer, compounding multiplicatively with DD_SCALE (BASE_RISK x DD_SCALE x lifecycle). | R15 det |  |
| METHOD-93 | Call 2 L63 | For pyramided DJ30/MYM and NAS100/MNQ legs, realize WATCH haircuts at the quantity layer (c1 sizing host), not by scaling TradingView risk% input. | R15 det |  |
| METHOD-94 | Call 2 L65 | Let the lifecycle factor multiply BASE_RISK/DD_SCALE/DD_TRIGGER at compute time but never edit them; a tier change mutating a locked constant is an integrity failure. | R14 det |  |
| METHOD-95 | Call 2 L57, L65 | Cite pins and paths by literal or symbol (for example 'from lifecycle import TIER_MULTIPLIER'), not line anchors, so they cannot re-stale. | R29 det | → docs/operational_rules.md §7 |
| METHOD-96 | Call 2 L65 | Preserve round-down, never-up sizing at the sizing host's integer-quantity floor. | R11 det | → docs/spec/c1_watch_realization_multiplier_layer.md |
| METHOD-97 | Call 3 L69-76 | Give SURVIVAL-ONLY strategies a smaller start (WATCH-1), doubled review cadence and one-window trigger; promote only after a full regime cycle and pre-registered minimum live-trade count. | R15 det |  |
| METHOD-98 | Call 3 L78 | Enter new additions and unexplained discovery-stack signals as SURVIVAL-ONLY by default. | R15 det |  |
| METHOD-99 | Call 4 L84 | When 2 of 4 legs sit in WATCH within one regime-check window, pull the next review forward and run the beta-cohesion check. | R15 det |  |
| METHOD-100 | Call 4 L85 | When 3 of 4 legs sit in WATCH, de-risk every leg to 0.50x and raise a mandatory operator GO/NO-GO on full shared-beta shutdown; autonomy stops there. | R15 det |  |
| METHOD-101 | Call 5 L92 | Arming and live send stay under operator GO plus M1, not this file; 'autonomous' here means rules-mandated without fresh judgment. | R10 abs |  |
| METHOD-102 | Call 5 L94 | Let reversible de-risks fire autonomously by rule: coded tier demotions, Call-1 firings on the ladder, the Call-4 soft flag and 0.5x beta de-risk. | R15 det |  |
| METHOD-103 | Call 5 L96 | Require operator GO/NO-GO against pre-registered criteria for WATCH-2 or CANDIDATE to RETIRED and full beta shutdown; autonomous demotion caps at WATCH-2. | R15 det |  |
| METHOD-104 | Call 5 L97 | Automation moves authorization down only; outside the S5 capped sandbox lane it never promotes, re-enters RETIRED, sizes up or re-optimizes; ceiling crossings stay operator-only. | R15 abs |  |
| METHOD-105 | §Forbidden moves L105 | Never re-fit a decayed strategy; retire it, and treat any replacement as a new hypothesis with fresh K-accounting and fresh out-of-sample. | R15 abs |  |
| METHOD-106 | §Forbidden moves L106, L109 | Never move or loosen a decay/kill threshold once live; fire it openly by superseding the ADR, or hold. | R15 det |  |
| METHOD-107 | §Forbidden moves L107 | Surveil on schedule against preset thresholds; the only outputs are hold, de-risk one tier, or retire, with no in-the-moment edits or re-fits. | R15 det |  |
| METHOD-108 | §Implementation status L119 | Use gitignored lifecycle_state.json as the runtime tier interface; absent means all AUTHORIZED; unknown tiers raise rather than silently fall back. | R15 det |  |
| METHOD-109 | §Implementation status L120 | Judge whether integer flooring discharges pyramid parity at the leg's actual cap_alloc-derived base; never quote the provenance-only older worked figures as current. | R15 det | → docs/spec/c1_watch_realization_multiplier_layer.md §2 |
| METHOD-110 | §Implementation status L123 | Keep the lifecycle_state.json writer fill-gated behind a separate GO; the beta-cohesion diagnostic is report-only and never writes it. | R15 det |  |
| METHOD-111 | §Implementation status L125 | Build the Call-4 beta-death monitor first, ahead of per-leg tier machinery. | R15 DEL | Discharged: Call-4 control landed 2026-07-10 (core/lifecycle.py:106 beta_death_assessment) and lab/research_utils/beta_cohesion.py exists. |
| METHOD-112 | §Implementation status L126 | Build per-strategy tier state machinery only when the first SURVIVAL-ONLY addition needs it; do not gold-plate a one-beta book. | R15 det |  |
| METHOD-113 | §Audit hooks L134-136 | Grep authorization vocabulary with distinctive tokens, not bare WATCH/RETIRED, which also match pre-existing prose. | R14 det |  |

</details>

<details><summary><code>docs/rule_0.md</code> — 8 rules: 2 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-113 | L3-5 | Before any decision brief or implementation step touching risk controls, read the production code directly, not memory or prior decision docs. | R0 abs |  |
| ROOT-114 | L7 | Sequence risk-control work: production file, then brief against ground truth, validate, lock, implement. | R0 det |  |
| ROOT-115 | §Corollaries L11 | Suspect single-rule descriptions of multi-rule systems. | R0 det |  |
| ROOT-116 | §Corollaries L12 | Data-source labels are not data-source verification. | R0 det |  |
| ROOT-117 | §Corollaries L13 | Where prior docs and code disagree, code wins; flag the discrepancy. | R0 det |  |
| ROOT-118 | §Corollaries L14 | Treat load-bearing claims lacking code-resident verification as unverified; identity, contract and cardinality assertions (core/lib/mvd.py helpers) are the baseline. | R0 det |  |
| ROOT-119 | §Scope L23 | Write new rules only against failures observed during execution, not hypothesized ones. | R36 abs |  |
| ROOT-120 | §Scope L24 | Apply the archived resurrection rule and 90-day review gate (pre-prune-2026-06-05 methodology archive README) when resurrecting pruned rules. | R36 DEL⚖ | Cited tag pre-prune-2026-06-05 absent on this clone (git tag empty); docs/ltm/README owns retrieval; Rule 36 governs re-adding rules. |

</details>

### Skills — 838 rules


<details><summary><code>.claude/skills/agent-improvement/SKILL.md</code> — 27 rules: 16 absorbed, 11 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-1 | intro L8 | Apply improvement review at planning, correction and completion moments only when a concrete opportunity appears; create no separate reflection task or artifact otherwise. | R36 abs |  |
| SKILL01-2 | §Establish the opportunity L15 | Before acting on an improvement, name the source-supported mechanism and expected benefit; read the affected source and task contract—confidence alone is not evidence. | R36 det |  |
| SKILL01-3 | §Establish the opportunity L20 | Search the affected paths and mechanism in existing tests, hooks, skills and owning records (lessons/history when reuse is plausible); avoid repo-wide sweeps; read prior improvement entries and outcomes before reuse. | R36 det |  |
| SKILL01-4 | §Establish the opportunity L26 | Route an observed defect through code-defect-debugging §11, which owns diagnosis and regression evidence. | R40 abs |  |
| SKILL01-5 | §Establish the opportunity L27 | Use handoff-verify for external or frozen handoffs; a worker returns contradictions to its coordinator instead of silently repairing them. | R4 abs |  |
| SKILL01-6 | §Choose action table row 1 L35 | When the mechanism is established and the fix is local, reversible, in scope and within seat/card grants with acceptance unchanged, implement and verify it without re-asking authority. | R36 abs |  |
| SKILL01-7 | §Choose action table row 2 L36 | If benefit is uncertain but a bounded evaluation fits scope, budget and grants, first state the adoption result and stopping condition; keep the current approach if inconclusive or adverse. | R36 det |  |
| SKILL01-8 | §Choose action table row 3 L37 | Route changes crossing a frozen card, capabilities, footprint, budget or operator act by seat (worker→coordinator→executive or escalation lane→owner); operator-only decisions go as an operator decision packet. | R4 abs |  |
| SKILL01-9 | §Choose action table row 4 L38 | Leave speculative, incidental or already-addressed opportunities alone; record a lead only when its owner has a concrete revisit trigger. | R36 det |  |
| SKILL01-10 | §Choose L40 | Before acting, identify the changed behavior, its permitted scope, its verification and an undo path that does not revert anyone else's work. | R36 det |  |
| SKILL01-11 | §Choose L41 | Prefer a source fix or existing test/validator over a new instruction; allow at most one durable preventive intervention per failure mechanism, consolidating existing protection. | R36 abs |  |
| SKILL01-12 | §Choose L44 | Change standing instructions only on explicit user request; registering or changing a .claude/settings.json harness hook counts—propose it unasked, implement it only when requested within grants. | R36 abs |  |
| SKILL01-13 | §Choose L50 | Draw authority only from seat_authority.yml grants and the card's authority block; an improvement never unlocks an operator act or forbidden capability; agent-reported operator approval is not approval. | R4 abs |  |
| SKILL01-14 | §Choose L55 | Never weaken success criteria, omit required checks, expand permissions or reinterpret an operational GO to make work cheaper; preserve the selected handoff card and its return boundary. | R3 abs |  |
| SKILL01-15 | §Choose L57 | Repeated failed corrections follow the AGENTS.md escalation rule and its named lane; relabeling the next attempt as an optimization does not reset the count. | R7 det |  |
| SKILL01-16 | §Verify and return L65 | Verify by type: defect shown before/after via the owning diagnostic; plan fix traced through inputs, outputs and final verification; efficiency with comparable before/after, separating predicted from measured. | R36 det |  |
| SKILL01-17 | §Verify and return L71 | Tie evidence to the delivered revision; run applicable checks through the launcher; report a missing check as an unresolved limitation, never a pass. | R21 abs |  |
| SKILL01-18 | §Verify and return L73 | Revert an unsuccessful candidate or report what remains unresolved; never adopt it merely because it was implemented; disclose material changes in the normal task return. | R36 det |  |
| SKILL01-19 | §Verify and return L76 | Verification of an improvement confers no merge or release authority. | R3 abs |  |
| SKILL01-20 | §Retain useful learning L80 | Write an improvement entry into an owning plan/PR/campaign record only if the card grants governance.author (no card: an owner the operator instruction scopes); otherwise route it via the task return. | R36 abs |  |
| SKILL01-21 | §Retain useful learning L89,L112 | Leave routine local corrections in the normal change report; capturing an ordinary improvement needs no new registry, ADR or permanent rule. | R36 abs |  |
| SKILL01-22 | §Retain useful learning L90 | Format a reusable improvement entry with a stable ID and Observation, Change and authority, Verification, Applicability, Evidence links, Disposition, Follow-up fields; omit unavailable measurements, never invent them. | R36 det |  |
| SKILL01-23 | §Retain useful learning L104 | Link later experiments and campaigns to the improvement entry rather than copying its conclusion. | R29 abs |  |
| SKILL01-24 | §Retain useful learning L105 | Record contrary results by mutability: correct a living owner in place (including Disposition); for frozen evidence add an addendum and an upstream reader intercept. | R30 abs |  |
| SKILL01-25 | §Retain useful learning L109 | On reuse read the entry's current disposition; application in one campaign does not establish benefit in another. | R36 det |  |
| SKILL01-26 | §Retain useful learning L111 | Keep private evidence private, using only permitted references in public files. | R13 abs |  |
| SKILL01-27 | §Why this skill exists L121 | Publishing a repo skill to user-level skill directories is a separate explicit release under the scripts/README.md skill lifecycle; never publish implicitly. | R3 det | → scripts/README.md §Skill lifecycle |

</details>

<details><summary><code>.claude/skills/babysit/SKILL.md</code> — 17 rules: 0 absorbed, 17 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-28 | intro L8 | Own a PR the agent opened through merge readiness: inspect, repair, push and verify rather than merely reporting failures or promising to check later. | R6 det |  |
| SKILL01-29 | intro L8 | Push only the PR's own codex/ or claude/ head branch; never push main; babysitting never merges—merging follows the surface-allocation ADR's operator merge rule. | R6 det |  |
| SKILL01-30 | §Start monitoring L12 | Identify the target PR (given, or from the current branch) and record its number, URL, base, head branch and head OID. | R6 det |  |
| SKILL01-31 | §Start monitoring L13 | Read repository instructions before changing files and keep unrelated local changes intact. | R6 det |  |
| SKILL01-32 | §Start monitoring L14-19 | Inspect full PR state—checks with logs, mergeability, base drift, reviews, inline threads, comments, other actors' commits—and keep an evidence ledger marking each item pending/addressed/obsolete/non-actionable. | R6 det |  |
| SKILL01-33 | §Start monitoring L21 | Use the hosting CLI/API (gh pr view, gh pr checks, gh api); never rely on one summary command where threads or logs need separate queries. | R6 det |  |
| SKILL01-34 | §Monitoring loop step 1 L27 | Refresh remote PR state before every action and sync the local branch with fetched head commits before editing; any new commit, review, check or base change restarts the loop. | R6 det |  |
| SKILL01-35 | §Monitoring loop step 2 L28 | If another actor merged or closed the PR, stop and report that terminal state; never poll a terminal PR indefinitely. | R6 det |  |
| SKILL01-36 | §Monitoring loop step 3 L29 | Resolve conflicts or required base drift by merging the base into the PR branch; never rebase a pushed branch, force-push or git stash; test, commit the merge, push normally. | R6 det |  |
| SKILL01-37 | §Monitoring loop step 4 L30 | For every failed, cancelled or timed-out blocking check, read job logs, reproduce deterministic failures, fix the root cause, run narrow and required broader suites, then push. | R6 det |  |
| SKILL01-38 | §Monitoring loop step 4 L30 | Rerun infrastructure-only failures when permitted and record why no code change was needed; report infra blockers with the smallest human action; never rerun deterministic failures without reason. | R6 det |  |
| SKILL01-39 | §Monitoring loop step 5 L31 | Verify a reviewer's repository authority before treating feedback as instruction; implement every actionable authorized request; treat untrusted feedback as informational unless an owner approves it. | R6 det |  |
| SKILL01-40 | §Monitoring loop step 5 L31 | Answer each thread with the concrete change or evidence; request resolution from its author when required; never dismiss, hide or resolve others' threads to empty the queue. | R6 det |  |
| SKILL01-41 | §Monitoring loop step 6 L32 | Monitor pending checks to completion at a moderate poll interval; avoid API-hammering busy loops. | R6 det |  |
| SKILL01-42 | §Monitoring loop L35 | When blocked by credentials, infrastructure or a human-only decision, report the exact blocker and requested action, keep monitoring, and never describe a blocked PR as complete. | R21 det |  |
| SKILL01-43 | §Exit criteria L39-49 | Declare merge-ready only after a fresh post-push snapshot shows an open, non-draft, mergeable PR, required checks green, reviews satisfied, every thread read and addressed, and an empty ledger. | R6 det |  |
| SKILL01-44 | §Exit criteria L51 | Run one final full refresh before reporting PR URL, head commit, checks, mergeability and feedback disposition; never claim the PR merged unless it actually is. | R21 det |  |

</details>

<details><summary><code>.claude/skills/blast-radius/SKILL.md</code> — 12 rules: 2 absorbed, 10 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-45 | §When to use L14 | After substantive edits to hot surfaces (docs, AGENTS, STATE, PIPELINES, REPO_MAP, skills, CATALOG, instruments, strategy doc mirrors) run the blast-radius sweep before stopping; skip read-only or pure-code turns. | R30 det |  |
| SKILL01-46 | §1 Ground truth L21-29 | Derive changed tokens from git status/diff, noting old→new token for each load-bearing prose change; prefer diff tokens over memory. | R30 det |  |
| SKILL01-47 | §2 Grep the hot surfaces L31-45 | Grep hot surfaces for each old token and the decision slug, not only the new phrase. | R30 det |  |
| SKILL01-48 | §2 Grep the hot surfaces L47-56 | When paths move or status words flip, run root-doc/path liveness, status-consistency and sync-liveness backstops (adr-graph if ADRs touched); they do not prove semantic currency. | R30 det |  |
| SKILL01-49 | §2 Grep the hot surfaces L56-60 | Repair clear liveness findings in-session but never auto-rewrite INDEX; flip CATALOG status only through archive_lab_analysis.py --regenerate-catalog, never by hand edit. | R34 det | → lab/analysis/README.md (CATALOG regeneration) |
| SKILL01-50 | §3 Triage L62-70 | Triage each hit: cite the owner; refresh mirrors/pointers to a link, never restating owned values; fix silent restatements owed by this turn or list them owed; mark false positives n/a. | R30 det |  |
| SKILL01-51 | §3 Triage L69 | Leave historical ADR and closure bodies unedited, adding only a parenthetical or Superseded-by when the authoring Phase 2 requires it. | R30 abs |  |
| SKILL01-52 | §3 Triage L72 | Never edit Pine, dd_protection/firm_rules risk constants or allocations under the blast-radius sweep; stop and ask instead. | R14 det |  |
| SKILL01-53 | §4 Report shape L74-98 | Open the sweep report with exactly 'BLAST-RADIUS: CLEAN\|OWED\|REPAIRED', then a path/old-token/class/action table and Owners touched, Still owed, Gates run lines. | R30 det |  |
| SKILL01-54 | §5 Repair scope L100-106 | By default fix clear silent restatements and stale pointers this turn's tokens prove; stop and ask when out of scope, touching locked constants/Pine, or historical wording needs judgment. | R30 det |  |
| SKILL01-55 | §Rationalizations L125-127 | Never treat a SESSIONS line or handoff-verify judging as a mirror repair; open STATE's bytes to check for a lingering prior obligation. | R30 det |  |
| SKILL01-56 | §Install surfaces L134 | No tracked hook runs blast-radius; wiring a tracked Stop hook for it is an operator election under AGENTS.md item 6. | R36 abs |  |

</details>

<details><summary><code>.claude/skills/blast-radius/references/hookify-blast-radius.local.md</code> — 1 rules: 0 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-57 | frontmatter L1-27 | Hookify stop-rule template: warn when a turn used Write/Edit but the transcript lacks 'BLAST-RADIUS:'; active only in clones that copy it to .claude/. | R30 det |  |

</details>

<details><summary><code>.claude/skills/blast-radius/references/owner-surfaces.md</code> — 4 rules: 4 absorbed, 0 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-58 | intro L3 | Treat owner-surfaces.md as a sweep checklist only; on drift trust the operational_rules.md Rule 7 owner table. | R29 abs |  |
| SKILL01-59 | §Fact → owner L5-16 | Use canonical owners: params→Pine, lock state→LOCK.md, dd_protection/allocations→core modules, MC anchors→mc_anchor_history, rationale→ADRs, ADR status→header+INDEX, narrative→SESSIONS, disposition→closure Iterate. | R29 abs |  |
| SKILL01-60 | §Fact → owner L17 | Derived strategy-parameter mirrors stay retired or labeled; never revive them. | R14 abs |  |
| SKILL01-61 | §Must-not-restate roles L19-28 | Treat STATE, SESSIONS, AGENTS posture, README, PIPELINES/REPO_MAP, skills, CATALOG and instrument ledgers as mirrors: pointer-first, link owners, never silently restate live constants or numbers. | R29 abs |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/SKILL.md</code> — 58 rules: 15 absorbed, 43 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-62 | intro L12 | The owning policy decides whether an artifact is needed; templates supply form and the skill discipline; examples create no requirement; update templates when an approved ruling changes the contract. | R33 det |  |
| SKILL01-63 | §Boundary L15 | Briefs pass The Algorithm (Question/Delete/Simplify/Accelerate) before shipping. | R9 abs |  |
| SKILL01-64 | §Boundary L16 | Use the artifact the owning contract requires—an ADR is not automatic; recording a decision grants no authority. | R32 abs |  |
| SKILL01-65 | §Boundary L17 | Decision artifacts may reference Pine source but never modify it. | R14 abs |  |
| SKILL01-66 | §Rule 0 L24 | Any brief touching risk controls, locked parameters or production code lists the production files read before authoring, not during a later investigation phase. | R0 abs |  |
| SKILL01-67 | §Rule 0 L28 | Before opening new lab/analysis or core-adjacent work, paste literal CATALOG and briefs INDEX search output (plus git log/check_advisor_dedup); attestation without output is void; instrument work reads ops/instruments/<SYM>.md. | R8 abs |  |
| SKILL01-68 | §Rule 0 L30 | Every non-grandfathered closure carries a Registry: line naming a rejected_candidates.md heading or 'n/a — <reason>', including FALSIFIED/DEAD/STOP closures. | R26 abs |  |
| SKILL01-69 | §Rule 0 L32 | Check whether the existing owner or PR can hold a change before creating a decision artifact; routine repairs need no ADR; a new ADR meets all three admission conditions. | R32 abs |  |
| SKILL01-70 | §Rule 0 sub-rule L40; Check 1 L50 | Populate §0 with specific production paths and verification anchors (commit hash/date, line range); empty, TBD or anchorless reads fail; light ADRs keep the read as a Reads line. | R0 det |  |
| SKILL01-71 | §Rule 0 sub-rule L42 | If the authoring environment cannot read production, put §0 in the CC handoff: the spawn reads files in Phase 0 and reports before proposing changes; the parent cites it. | R0 det |  |
| SKILL01-72 | §Six checks L48; matrix L83-95 | Apply discipline checks by artifact type per the applicability matrix; handoffs owe both checks 1–6 and 7–14; never apply the inquire/ADR six to a notice. | R33 det |  |
| SKILL01-73 | §Six checks L52 | Inquire briefs and full ADRs state a falsifiable hypothesis as 'If [observation], then [conclusion]; otherwise [alternative]'; 'look further' fails. | R33 det |  |
| SKILL01-74 | §Six checks L54 | List in §5 forbidden moves genuinely considered or tempting; a section whose removal would not change behavior is ceremony and fails. | R33 det |  |
| SKILL01-75 | §Six checks L56 | Make §6 gate criteria binary with specific triggers (N, σ tolerance, window) yielding RESOLVED/FALSIFIED/AMBIGUOUS; 'when we have more data' is not a gate. | R33 det |  |
| SKILL01-76 | §Six checks L58 | Phrase a Pre-Q question as a symptom, not a fix; if a symptom-only rephrase is impossible, return to inqhiori. | R9 det |  |
| SKILL01-77 | §Six checks L60 | Write §10 audit hooks as runnable commands or assertions (greps, paths), never 'review quarterly'. | R33 det |  |
| SKILL01-78 | §Checker ownership L64-70 | Treat repo-side check_brief.py 'NOT CHECKED' as not a pass; run the canonical skill-side checker for unmodeled types; --self-test or --list-checks never substitutes for checking the artifact. | R21 det |  |
| SKILL01-79 | §Checker ownership L69-70 | Never widen the repo checker's generic type to absorb unmodeled contracts, or promote the subset to a gate merely because it was fixed. | R38 det |  |
| SKILL01-80 | §Checker ownership L72-79 | Validate each type against its own contract: notice GRADUATE/DROP/HOLD routing; audit anchored sources and root cause; lesson Promotion/Retirement; concise ADR Decision/Grounds/Current owner; legacy light ADR five fields. | R33 det |  |
| SKILL01-81 | §Checker ownership L80-81 | Obtain a closure verdict by running scripts/check_closure_disposition.py; check_brief's closure delegation notice is not the closure check. | R28 det |  |
| SKILL01-82 | §Type matrix L97 | Author no new lock-decision briefs; --type lock survives only as a back-compat alias (type deleted 2026-08-08). | R33 det |  |
| SKILL01-83 | §CC checks L105 | A handoff's §0.5 must instruct the spawn to halt and ask on ambiguity rather than assume §1/§2 are complete. | R33 det |  |
| SKILL01-84 | §CC checks L107-111 | Handoff returns use exactly one of DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED, with a BLOCKED sub-case: context, capability, scope or plan-itself-wrong. | R4 det |  |
| SKILL01-85 | §CC checks L113-117 | Review returned spawn work in two separate passes—spec compliance (exactly what was specified, nothing added) and quality—never collapsing them. | R0 det |  |
| SKILL01-86 | §CC checks L119 | After multi-step handoff work, do a final consolidated read across all changes to catch integration inconsistencies. | R0 det |  |
| SKILL01-87 | §CC checks L121 | A multi-loop handoff carries a concrete coordinator pre-mortem before freeze: loop cost with budget checkpoint, pre-ruled executor decisions, cheapest moot-evidence, measures, and evidence binding declared at GO. | R33 det |  |
| SKILL01-88 | §CC checks L123 | Before the first full hosted run require shape-contract tests for new docker/systemd/workflow integrations (Windows and Linux), the PR's local gates green, and stress tests for new locks/queues. | R33 det |  |
| SKILL01-89 | §CC checks L125 | Schedule independent refute-first review at the interface freeze, before expensive evidence, and encode touched state-machine rules as local invariant tests. | R5 det |  |
| SKILL01-90 | §CC checks L127 | Never blanket-restore (git checkout --) a tree holding intentional uncommitted edits; commit first, and never git stash. | R6 det |  |
| SKILL01-91 | §CC checks L127 | After scripted or bulk edits, ast.parse/compile every touched file and verify under set -o pipefail so piped checks cannot hide failures. | R21 det |  |
| SKILL01-92 | §CC checks L127 | Before committing, confirm every claim in the commit message appears in git diff --cached. | R21 det |  |
| SKILL01-93 | §CC checks L127 | At a checkpoint push the in-flight head (with GO) or attach the patch so the coordinator adopts rather than re-derives it. | R41 det |  |
| SKILL01-94 | §CC checks L127 | Label a mechanism explanation a hypothesis until it is minimally reproduced. | R40 det |  |
| SKILL01-95 | §CC checks L127 | Return a CHECKPOINT for a failure outside the change surface instead of chasing it. | R4 det |  |
| SKILL01-96 | §Brief type selection L146-154 | Pick artifact type and home by need: Pre-Q docs/briefs/, ADR docs/adr/YYYY-MM-DD-slug.md, handoff inline, notice docs/notes/notice/, audit docs/notes/audits/, closure docs/briefs/closures/. | R33 det |  |
| SKILL01-97 | §Brief type selection L155 | Use a minimal spec in docs/spec/ (TEMPLATE-minimal-spec.md) for commissioning steps that decide nothing (PROPOSED, $0/K=0). | R33 det |  |
| SKILL01-98 | §Brief type selection L152 | Capture a new lesson by inline-editing the relevant references/*lessons.md registry. | R33 det |  |
| SKILL01-99 | §Brief type selection L164-165 | Preserve the owning contract's approvals, source reads, research evidence and lock-change requirements whatever artifact form is chosen. | R3 abs |  |
| SKILL01-100 | §Current ADR form L167-173 | Author new ADRs in concise form—graph header, Format: concise, Decision/Grounds/Current owner; add evidence or reversal conditions only where needed; never invent falsifiers, word limits or quarterly obligations. | R32 abs |  |
| SKILL01-101 | §Current ADR form L174-175 | Revise accepted ADR effective text only after required approval, with a dated scope note and immutable prior revision; frozen preregistrations, locks, verdict logic and evidence stay uneditable. | R32 abs |  |
| SKILL01-102 | §When NOT to author L177-180 | Author no brief for quick low-reversibility-cost decisions, code without a structural decision, or an investigation still in progress (the brief is its output). | R33 det |  |
| SKILL01-103 | §Canonical templates L186,L200 | Read the relevant references/ template at authoring time and copy-fill it; never reconstruct template structure from memory. | R33 det |  |
| SKILL01-104 | §Closure discipline L198 | Closures carry machine-readable '**Closed:** YYYY-MM-DD' and '**Lane:** <F2 slug\|UNASSIGNED>' headers; aliases are non-compliant; forward-only—never retro-edit old closures or invent lane names. | R28 det | → .claude/skills/brief-authoring/references/closure_record.md header |
| SKILL01-105 | §Closure discipline L198 | End every closure with a typed ## Iterate block (Verdict used, Model update, exactly one Next: INTEGRATE\|ITERATE\|STOP, Routing, Entry packet, Stop rule, Board write) or it is incomplete. | R28 abs |  |
| SKILL01-106 | §Closure discipline L198 | ITERATE names a successor and fills its entry packet (frozen constraints, carry-forwards, forbidden re-opens, budget) but never opens it—operator GO is a fresh decision. | R28 abs |  |
| SKILL01-107 | §Closure discipline L198 | STOP is Iterate with zero budget and records the re-proposal bar; ITERATE and STOP owe a stop rule, RESOLVED-and-integrated may write 'n/a — integrated'; never manufacture stop rules. | R28 abs |  |
| SKILL01-108 | §Closure discipline L198 | For work live across sessions, Board write quotes the STATE.md row or campaign-owner update; never only a SESSIONS line; 'none — STOP, nothing owed' only if nothing remains. | R28 det | → .claude/skills/brief-authoring/references/closure_record.md §Iterate Board write |
| SKILL01-109 | §Closure discipline L198 | Closure gate 14 checks Iterate tokens only; closure content quality is audited at the quarterly methodology cadence. | R28 det |  |
| SKILL01-110 | §Verification block L204-235 | End every authored brief with a verification block—applicable checker commands, closure check, Rule 0 anchor greps, cross-reference greps—and run it before declaring the brief complete. | R33 det |  |
| SKILL01-111 | §Verification block L237 | If any verification command fails the brief is incomplete; re-author the broken section rather than handwaving. | R21 abs |  |
| SKILL01-112 | §Known traps L257 | Re-verify reused anchors (SHAs, line numbers, headings) with a §10 grep confirming each still resolves. | R0 abs |  |
| SKILL01-113 | §Known traps L257 | Never cite a historical Notion page ID as an anchor; resolve it via docs/governance/notion-redirect-map.md and cite the repo owner. | R29 det |  |
| SKILL01-114 | §Known traps L259 | Connect a new brief's §1 Context to existing doctrine (core principles, lessons registries, prior ADRs) wherever any exists. | R33 det |  |
| SKILL01-115 | §Known traps L261 | A lesson graduates only with a dated incident plus dollar cost or counterfactual meeting the bar (single incident above $3K or three separate firings); otherwise it stays candidate. | R33 det | → docs/methodology/lessons/execution_lessons.md (Promotion criteria) |
| SKILL01-116 | §Known traps L263 | Give every promised check a meaningful action and a date or wake condition; migrate or retire obsolete checks; never attach a quarterly obligation to an ADR by default. | R32 det |  |
| SKILL01-117 | §Known traps L265 | Gate one question per Pre-Q; split multi-question briefs, or for coupled questions name the parent and fork ungated sub-questions (parent-Q convention). | R9 det |  |
| SKILL01-118 | §Known traps L267 | Never amend §6 gate criteria mid-investigation; close the brief AMBIGUOUS, record why, and open a fresh brief with the new criteria stated up front. | R23 det |  |
| SKILL01-119 | §Discipline summary L288 | Record a decision's actual approval and effectivity; keep Proposed branches separate and unimplemented decisions distinguishable from implemented controls; a Proposed branch is not permission. | R32 det | → .claude/skills/brief-authoring/references/adr.md Status/Decision |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/adr.md</code> — 7 rules: 3 absorbed, 4 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-120 | §Current owner L27-29 | An ADR's Current owner section links the contract, implementation or campaign owning present procedure; never copy the runbook or create another wrapper. | R29 abs |  |
| SKILL01-121 | §Graph header L50-53 | Keep ADR header fields before the first ## or ---; use Status tokens Proposed/Accepted/Superseded/Withdrawn/Retired; partial supersession stays Accepted with Superseded-in-part-by. | R32 det |  |
| SKILL01-122 | §Graph header L55-58 | Declare successors with 'Supersedes: <file> full\|in part — scope' per target; once Accepted add the predecessor's reverse edge; non-ADR partial replacement uses event:<id>; never claim a nonexistent ADR. | R32 det |  |
| SKILL01-123 | §Graph header L60-65 | Before removing an ADR read its body and amendments, map clauses and obligations, migrate consumers, verify incoming routes, prove blobs retrievable, and record it in docs/adr/TOMBSTONES.md. | R31 abs |  |
| SKILL01-124 | §Graph header L67-71 | The retire_adr.py cold-stub form is optional, not a required step before verified deletion; never weaken its safety checks to avoid migrating a consumer. | R31 det |  |
| SKILL01-125 | §Verification L75-85 | Verify ADR changes with skill check_brief --type adr and check_adr_graph (--regenerate-index, then check), plus affected negative-case tests and required gates; checkers prove neither truth nor approval. | R32 det |  |
| SKILL01-126 | §Verification L86 | When moving an obligation out of an ADR, migrate its reader too. | R30 abs |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/audit_note.md</code> — 9 rules: 1 absorbed, 8 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-127 | §0 Source anchors L12-18 | Anchor an audit note to specific commits, file paths or chat URLs for every audited artifact. | R33 det |  |
| SKILL01-128 | §1-§2 L22-46 | State the dated triggering incident, classify its failure class, and narrate events in order, separating facts from interpretation and naming each party. | R33 det |  |
| SKILL01-129 | §3 L50-64 | Map each relevant discipline check to fired/failed silently/N/A; a check that should have fired but did not is the first repair target. | R36 det |  |
| SKILL01-130 | §4 L68-76 | Push root cause past the immediate cause to contributing and structural causes, stopping at the first structurally repairable layer. | R36 det |  |
| SKILL01-131 | §5 L80-97 | Plan immediate and structural repairs (skill, template, validator, trigger, Rule 7 consolidation); if no structural repair exists, flag the recurrence risk explicitly. | R36 det |  |
| SKILL01-132 | §6 L115-116 | Cite existing lessons (E-N, M-K) that already cover a pattern instead of creating duplicates. | R33 abs |  |
| SKILL01-133 | §7 L120-132 | Check each audit against programme-audit degeneration signals; if any fires, escalate to programme-audit for that layer and keep the audit open as its input. | R28 det |  |
| SKILL01-134 | §11 L154-160 | Record audit closure status, immediate and structural repair dates, graduated lessons and triggered follow-up audits. | R33 det |  |
| SKILL01-135 | §Verification L164-182 | Run skill-side check_brief --type audit as the counting gate and confirm each structural repair shipped and each candidate lesson exists in the registry. | R33 det |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/cc_handoff.md</code> — 34 rules: 9 absorbed, 24 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-136 | header L5 | Name each handoff's spawn target and environment (cloud default; local carries 'Must run locally'); route frozen-spec implementation to a worker using the §0.5 worker variant. | R41 abs |  |
| SKILL01-137 | header Authority L9 | Committing and pushing the agent's own codex/ or claude/ branch and opening a PR need no per-action go (operator ruling 2026-10-24). | R6 det | → docs/adr/2026-07-14-cc-cursor-surface-allocation.md (Addendum 2026-10-24) |
| SKILL01-138 | header Authority L9 | No merge without Joshua's go; a DONE status, recommended next action or completed review supplies no permission. | R6 DEL | Merge clause superseded by AGENTS §Merges / ADR Addendum 2026-10-24b A conditioned merge GO (8414d516); remainder restates Rule 3. |
| SKILL01-139 | §0 L15-22 | The spawn reads every §0 file and posts a read-report, including git log -1 anchors for closure records, before any §2 work. | R0 det |  |
| SKILL01-140 | §0 L24; CLI contract L30 | Carry existing authorization forward accurately and proceed absent material contradiction; ask only for missing authority or a material change in scope, destination, data access or permitted actions. | R3 det |  |
| SKILL01-141 | §CLI execution contract L28 | For CLI dispatch record target CLI, working directory, read paths, permitted writes/actions, existing authorization and return location (inline is fine for routine tasks). | R41 det |  |
| SKILL01-142 | §CLI execution contract L30 | Verify the installed executable and options before launch and match worker capabilities to the task; permission flags or workspace trust never supply authorization. | R41 det |  |
| SKILL01-143 | §CLI execution contract L30 | Treat local CLI execution as possibly still sending model context to an external provider. | R13 det |  |
| SKILL01-144 | §CLI execution contract L32 | Capture exit code, stdout, stderr and session ID; an empty response or exit zero does not establish completion—check expected artifacts and verification evidence. | R21 det |  |
| SKILL01-145 | §CLI execution contract L34 | On dispatch failure preserve the exact error and classify its cause; fix demonstrated invocation errors within authority; before retrying check whether the run persists or changed files; resume existing workers. | R41 det |  |
| SKILL01-146 | §CLI execution contract L34 | Never change launchers or disable controls to evade a denial. | R4 abs |  |
| SKILL01-147 | §CLI execution contract L36 | Use scripts/dispatch_claude.ps1 with agent_handoff.md recovery only for local Claude Code dispatch; never route a Codex packet through it—dispatch Codex via its own surface. | R41 det |  |
| SKILL01-148 | §CLI execution contract L36 | Provision Codex no launcher and no push credential in this repo (2026-08-29 bar, retained). | R12 det | → docs/adr/2026-07-14-cc-cursor-surface-allocation.md Addendum 2026-10-24b B |
| SKILL01-149 | §CLI execution contract L36 | Supply expected outputs and check names; keep the request receipt and reuse its ID; reconcile uncertain outcomes before retrying; BLOCKED/NEEDS_CONTEXT is not completed work; DONE needs parent verification. | R41 det |  |
| SKILL01-150 | §0.75 L40-49 | Before every dispatch confirm gitignored vendor data and needed secrets are present in that exact environment by a check run now; if not confirmed, run locally or stage and re-confirm. | R41 det | → .claude/skills/task-routing/SKILL.md |
| SKILL01-151 | §0.75 L51 | Default dispatch to cloud; a packet that must run locally says 'Must run locally' near its top with the reason. | R41 abs |  |
| SKILL01-152 | §0.75 L53 | The local-dependency check keys on environment, never vendor: no surface, Claude Code included, is exempt; 'N/A' only when no read or step touches vendor data or a secret. | R41 det | → .claude/skills/task-routing/SKILL.md |
| SKILL01-153 | §0.5 L59-71 | A spawn never guesses on scope, data, methodology or termination ambiguity; it posts them under '§0.5 Response — ambiguities', holds NEEDS_CONTEXT, and assumes AND only when §6 says AND. | R33 det |  |
| SKILL01-154 | §0.5 frozen-spec variant L73 | In frozen-spec worker cards give each ambiguity a bolded Recommended default the worker applies unless Phase 0 contradicts it; workers never resolve spec ambiguity unilaterally, bouncing NEEDS_CONTEXT instead. | R4 det |  |
| SKILL01-155 | §1 L89; §5 L139 | State what the spawn is NOT asked to do; a spawn logs unrelated issues as DONE_WITH_CONCERNS and never silently fixes them ('while I was in there'). | R4 det |  |
| SKILL01-156 | §2 L93-109 | Give each execution step its inputs, action, expected output and a per-step gate. | R33 det |  |
| SKILL01-157 | §2 Step 2.N L113-117 | Produce the completion record the owning contract requires—Pre-Q §9 closure, or an update to the existing owner/PR; an ADR amendment is not automatic. | R32 abs |  |
| SKILL01-158 | §2 Step 2.N L118 | Write no recommendation.md for non-PROMOTE verdicts (sentinel convention). | R28 det |  |
| SKILL01-159 | §4 L122-131 | Restate the parent hypothesis and §6 thresholds verbatim and assert against them, never re-derived ones; with no hypothesis write N/A naming the owning artifact and keep its evidence requirements. | R23 det |  |
| SKILL01-160 | §5 L140 | Never run outcome-conditional D-tests (filtering data on the studied outcome); return NEEDS_CONTEXT if one seems needed. | R23 det |  |
| SKILL01-161 | §5 L142 | If a §0 anchor disagrees with what is on disk, never proceed with the inconsistent number; return NEEDS_CONTEXT with the discrepancy. | R0 abs |  |
| SKILL01-162 | §5.1 L145-163 | A new worker card, and any card granting worktree.write or research.run, carries a yaml authority block of registry capabilities, every parent constraint, and §6.0 acceptance test names. | R33 det |  |
| SKILL01-163 | §5.1 L148-151 | An authority block may only narrow: no forbidden or operator-act capability, nothing above the seat ceiling or beyond the parent card's grants. | R4 abs |  |
| SKILL01-164 | §5.1 L152-154 | The coordinator's pre-dispatch read and the executive review confirm the card's declared seat is the seat that will run it. | R4 det |  |
| SKILL01-165 | §6.0 L169-176 | The parent names acceptance tests and the property each must violate before the worker starts; worker-written tests are extra evidence, never the acceptance basis. | R33 abs |  |
| SKILL01-166 | §6.0 L178 | Attach an invariant table (one contract claim → one refusal → one test) for contract-driven code. | R33 abs |  |
| SKILL01-167 | §6.0 L179 | For order, position or shutdown semantics, attach the state model and event sequences. | R33 abs |  |
| SKILL01-168 | §6.0 L180-183 | A lightweight dispatch issue carries the acceptance table and a parent read comment with the body's sha256, cited as #n @ sha256; otherwise it is unfrozen—do not dispatch. | R33 det |  |
| SKILL01-169 | §Verification L256-273 | Before declaring a handoff complete run check_brief --type cc_handoff and check_handoff_authority, and confirm the four-state status and both review passes. | R33 det |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/closure_record.md</code> — 10 rules: 1 absorbed, 9 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL01-170 | filename L3-5 | Name closures docs/briefs/closures/Q-X-closure-<verdict-slug>.md, carrying the verdict in both filename and H1 title. | R28 det |  |
| SKILL01-171 | header L9-16 | A closure header records the verdict as filed, the pre-registration and its freeze commit, spend and K consumed, live effect, artifacts, and a successor only if authored. | R28 det |  |
| SKILL01-172 | §1 Verdict L20-30 | Assert the verdict only against the frozen §6 gate, walking every pre-registered route including void clauses; no winner language; if operator-stopped, state §6 verdicts may not be quoted. | R24 det |  |
| SKILL01-173 | §2 L32-34 | Compare what the pre-registration predicted with what happened, flagging surprises and naming thin cohorts. | R28 det |  |
| SKILL01-174 | §3 L36-39 | Include a negative-scope section stating what the closure does NOT license; omit it only when genuinely empty. | R28 det |  |
| SKILL01-175 | §4 L41-44 | Record defects found in the frozen brief in the closure without editing the frozen artifact; they become entry-packet inputs if Next is ITERATE. | R23 det |  |
| SKILL01-176 | §Iterate Stop rule L68 | Re-proposal bars demand new mechanism evidence, not new parameters. | R26 abs |  |
| SKILL01-177 | §10 audit-hook discharge L79-82 | Run the parent brief's §10 hooks at closure and paste outputs; correct defective hooks with the reason recorded, never silently pass them. | R28 det |  |
| SKILL01-178 | authoring notes L104-106 | The Iterate block replaces legacy Dispositions/Forward/Re-proposal sections; write that content once there, never both. | R28 det |  |
| SKILL01-179 | authoring notes L107-109 | Treat the pre-registered §6 branch as default, not cage: discharging another branch is closure judgment—quote the frozen §6 row and state why the other branch fired. | R24 det |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/inquire_brief.md</code> — 22 rules: 3 absorbed, 19 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-1 | Header L3 | Use the Pre-Q status taxonomy: OPEN, OPEN-DRAFT (pre-lock), CLOSED-RESOLVED, CLOSED-FALSIFIED, CLOSED-AMBIGUOUS-HOLD, SUPERSEDED. | R33 det |  |
| SKILL02-2 | §0 L16 | Before authoring a Pre-Q, list every production file read with a verification anchor (commit hash, stat date or git log); an empty or TBD §0 fails Rule 0. | R0 det |  |
| SKILL02-3 | §0 L18 | Without repo filesystem access, mark §0 paths pending, make the reads Phase 0 of the companion CC handoff, and never lock before anchors are populated. | R0 det |  |
| SKILL02-4 | §1 L28 | State the dated incident or finding that prompted the question and cite the doctrine line tested; connect the brief to existing structure (no orphan briefs). | R33 det |  |
| SKILL02-5 | §2 L36 | List prior briefs with verdicts, ADRs with status, lessons and any fork condition; if lineage is empty, state explicitly that the question is novel. | R8 det |  |
| SKILL02-6 | §3 L48 | Rephrase the question naming only the symptom, not the fix; if that is impossible the question bakes in a solution, so return to inqhiori. | R9 det |  |
| SKILL02-7 | §4 L59 | State a falsifiable hypothesis in if/then/otherwise form with explicit reject, accept and ambiguous-hold conditions; 'look further' conclusions fail. | R23 det |  |
| SKILL02-8 | §5 L71 | List only forbidden moves genuinely considered or tempting, each with its reason; if removing the section would change nothing, it is ceremony and must be rewritten. | R33 det |  |
| SKILL02-9 | §5 L77 | Never use outcome-conditional D-tests (e.g., filter out tail losses, then test tail risk); they encode the conclusion into the analysis. | R23 det |  |
| SKILL02-10 | §6 L83 | Give every closure verdict a binary, specific numerical or statistical trigger; 'when we know more' is not a gate. | R23 det |  |
| SKILL02-11 | §6 L91 | Type each verdict row's disposition as exactly one of INTEGRATE / ITERATE / STOP plus its concrete action; pre-register coarsely where routing is unknowable. | R28 abs |  |
| SKILL02-12 | §6 L91 | At closure, elect a disposition branch other than the pre-registered one only if the Iterate block quotes the frozen row and states why the other branch fired. | R28 det |  |
| SKILL02-13 | §6 L93 | Pre-register §6 before data touches analysis; never amend gates mid-investigation or reopen a sibling Q with looser gates; close AMBIGUOUS and open a fresh brief instead. | R23 abs |  |
| SKILL02-14 | §7 L99 | For self-executing briefs enumerate phases starting with Phase 0 Rule-0 reads; otherwise point §7 to the companion CC handoff that holds the steps. | R33 det |  |
| SKILL02-15 | §8 L110 | Commit the verdict pre-registration (§6 table plus exact thresholds) under docs/briefs/pre-registration/ before any analysis script runs; the closure cites its commit hash. | R23 det |  |
| SKILL02-16 | §8 L112 | Apply the two-implementer test to a pre-registration; if numbers could differ, also ship reference code or a worked synthetic numeric example. | R23 abs |  |
| SKILL02-17 | §9 L126-130 | Produce each closure from references/closure_record.md, named by verdict; write recommendation.md only for PROMOTE; AMBIGUOUS-HOLD closures state an explicit re-test trigger and date. | R28 det |  |
| SKILL02-18 | §9 L132 | Closure records include verdict, anchor numbers vs thresholds, prediction vs outcome, lesson candidates with dated or dollar anchors, and the mandatory typed Iterate block. | R28 det |  |
| SKILL02-19 | §10 L138 | Write audit hooks as mechanically runnable commands, never review notes such as 'review at quarterly check-in'. | R33 det |  |
| SKILL02-20 | §10 L144 | Include audit hooks confirming every cited anchor (path, heading, commit) still resolves. | R33 det |  |
| SKILL02-21 | Verification L158-174 | Run check_brief.py --type inquire plus §0-anchor, cross-reference and prereg-predates-analysis checks; any failure means the brief is incomplete: re-author, never handwave. | R33 det |  |
| SKILL02-22 | Pre-Lock Checklist L178 | Before locking a DRAFT brief, complete every pre-lock checklist item; remove the checklist once the brief is locked. | R33 det |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/lesson_capture.md</code> — 11 rules: 0 absorbed, 11 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-23 | Header L3-8 | Classify lessons E/M/B/O with status Candidate, Standing rule or Retired (superseded or no longer applicable), in the matching registry file. | R33 det |  |
| SKILL02-24 | Pattern L14 | State a lesson's pattern as a one-sentence recurring failure mode, not a dated story. | R33 det |  |
| SKILL02-25 | Anchor incidents L22-33 | Promote a lesson only with dated incidents and dollar cost or counterfactual meeting the gate: one incident above the dollar threshold, or three firings in separate windows; else Candidate. | R36 det |  |
| SKILL02-26 | Anchor incidents L33 | Bypass the empirical promotion gate by structural argument only rarely, with explicit justification for the bypass. | R36 det |  |
| SKILL02-27 | Repair L41 | Write each lesson's repair as a present-tense imperative rule that would have prevented its anchor incidents. | R33 det |  |
| SKILL02-28 | Repair L43-50 | Name the lesson rule's canonical enforcement point (skill, template, check_brief, operational checklist, calendar); without one, flag it and find a surface or keep it Candidate. | R33 det |  |
| SKILL02-29 | Cross-references L54 | Record briefs citing, skills enforcing, related and superseded lessons for each lesson. | R33 det |  |
| SKILL02-30 | Promotion/Retirement L63-80 | For a Standing rule record promotion date, decider, rationale and source; for a Retired lesson record date, reason and a one-sentence tombstone note. | R33 det |  |
| SKILL02-31 | Audit hooks L86 | Add a grep audit hook confirming the lesson is referenced where it claims enforcement; re-evaluate Candidates quarterly for a third firing. | R33 det |  |
| SKILL02-32 | Verification L100-108 | For lesson and notice artifacts, the skill-side check_brief.py result is the gate that counts; repo-side NOT CHECKED is expected, not a gap. | R33 det |  |
| SKILL02-33 | Verification L110 | If no grep audit hook can mechanically detect a lesson's failure mode, keep the lesson Candidate. | R33 det |  |

</details>

<details><summary><code>.claude/skills/brief-authoring/references/notice_log.md</code> — 9 rules: 0 absorbed, 9 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-34 | Header L3-8 | Record notices at docs/notes/notice/N-YYYY-MM-DD-slug.md with status OPEN, GRADUATED to Q-X, DROPPED or HELD until a date. | R33 det |  |
| SKILL02-35 | §0 L14 | Keep a notice's §0 to a one-line source anchor; the full Rule-0 burden lands on the Pre-Q if the notice graduates. | R33 det |  |
| SKILL02-36 | §1 L23 | Describe the observation plainly and concretely, without interpretation. | R33 det |  |
| SKILL02-37 | §2 L31 | Name the baseline, delta and frequency (listing prior notices if repeat); if no baseline can be named, note likely noise and drop. | R33 det |  |
| SKILL02-38 | §3 L41-47 | Keep candidate mechanisms informal and unregistered; more than four candidates signals reaching, so recheck whether the signal is real. | R33 det |  |
| SKILL02-39 | §4 L51-60 | Route every notice GRADUATE, DROP or HOLD with a one-sentence reason; graduation opens a Pre-Q from the inquire template, linking the notice in lineage. | R33 det |  |
| SKILL02-40 | §5 L64 | For a HOLD notice, set re-check date, graduation trigger, drop trigger and a calendar or Todoist entry. | R33 det |  |
| SKILL02-41 | §10 L77 | Audit graduated notices by grepping the Pre-Q lineage for the notice ID; audit HOLDs against their calendar reminder. | R33 det |  |
| SKILL02-42 | Verification L102 | Keep notices lightweight; if you are writing falsifiers or multi-section analysis, promote it to a Pre-Q instead. | R33 det |  |

</details>

<details><summary><code>.claude/skills/c1-rail/SKILL.md</code> — 41 rules: 14 absorbed, 25 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-43 | Status L8 | Read current rail, arm, M1, account and Track B state from AGENTS §Live-execution posture and STATE.md; the skill never substitutes for them. | R29 abs |  |
| SKILL02-44 | Path L10 | Treat the built CrossTrade rail as having no permitted Tradeify eval use: eval strategy logic must be native, with no external engine, bridge or direct API. | R10 abs |  |
| SKILL02-45 | Path L10 | Treat the Python sizing reference as the listener's sizing host when armed; there is no NT8 hop and the NinjaScript port is an unbuilt dormant fallback. | R11 det |  |
| SKILL02-46 | Pointer L12 | Never restate rail constants (quantities, ceilings, multipliers, thresholds) from the skill or memory; read the owning source; on disagreement the doc wins and the skew is flagged. | R29 abs |  |
| SKILL02-47 | Safety invariants L14 | Treat any rail safety-invariant violation as stop-and-surface, never a judgment call. | R11 det |  |
| SKILL02-48 | Invariant 1 L16 | Keep dry_run=true as standing state, defaulting True when the key is absent; dry-run computes the would-be payload but never calls the sender. | R10 det |  |
| SKILL02-49 | Invariant 2 L17 | Arm (dry_run=false) only with M1 RESOLVED for that instance, a separate per-session operator GO and every AGENTS gate; the gate's object is the arm. | R10 abs |  |
| SKILL02-50 | Invariant 2 L17 | Keep the withdrawn Striker editions barred from redeploy. | R10 abs |  |
| SKILL02-51 | Agent authority L25 | Agents may fly deploy the listener or signal-daemon app only after all six deploy pre-conditions, scoped per app. | R10 DEL⚖ | Superseded: seat_authority.yml rail.deploy is an operator act; ADR 2026-10-24b B: agents hold no Fly credential, rail.deploy stays operator act. |
| SKILL02-52 | Agent authority L26 | Agents may --disarm only after broker-verified flatness; flatten first, since dry_run blocks exits and disarming over an open position orphans it. | R10 det |  |
| SKILL02-53 | Agent authority L27 | Agents may always run --status, pre-flight reads and boot-line verification, which are read-only. | R10 det |  |
| SKILL02-54 | Agent authority L28 | Treat --arm as an operator act, never card-granted, reached only via the operator-act prompt route; an arming GO does not direct a trade. | R10 det |  |
| SKILL02-55 | Agent authority L28 | Never hand-edit /data/c1_rail_config.json to arm; it is the same act without the audit trail. | R10 det |  |
| SKILL02-56 | Two Fly apps L30 | Keep listener and signal daemon as separate Fly apps with their own machine and volume; never share listener peak_equity or collapse DD volumes. | R11 det |  |
| SKILL02-57 | Deploy pre-conditions L33 | Before a listener deploy, verify dry_run=true on the host; a restart re-reads the volume config and can reboot armed. | R10 det |  |
| SKILL02-58 | Deploy pre-conditions L34 | Deploy only from main, at repo root, using the documented fly deploy command. | R11 det |  |
| SKILL02-59 | Deploy pre-conditions L35 | Re-trace the image import closure whenever ops/ or core/ gains an import; never trust a green build. | R11 det |  |
| SKILL02-60 | Deploy pre-conditions L36 | Refresh M1 fixture_hashes from in-container hashes in the same motion as any listener deploy that moves pinned files. | R11 det |  |
| SKILL02-61 | Deploy pre-conditions L37 | After a listener deploy, verify the boot line (dry_run, armed_until) and health, judging by the command's printed output, not its exit code. | R10 det |  |
| SKILL02-62 | Deploy pre-conditions L38 | Know the crash-loop recovery path (deploy README, GO ADR, ARMING_PROCEDURE) before deploying; an expired armed_until blocks boot and a restart cannot fix it. | R10 det |  |
| SKILL02-63 | Invariant 3 L39 | Halt entry/add sizing (qty 0, no submit) on any unreadable or malformed state input; a halted or floored decision never reaches the sender. | R11 det |  |
| SKILL02-64 | Invariant 4 L40 | Record HTTP responses as accepted, never execution-verified; a timeout after send is unknown, blocks further risk-add and is never auto-retried; exits are best-effort. | R11 abs |  |
| SKILL02-65 | Invariant 5 L41 | Retired CrossTrade Alert History source-of-truth rule; any revived route needs its own source-of-truth rule. | R11 DEL⚖ | Already retired 2026-10-24 by operator ruling; tombstoned at docs/adr/TOMBSTONES.md#2026-10-24-skills-consolidation; CrossTrade Tradeify route rejected. |
| SKILL02-66 | Invariant 6 L42 | Operate the rail attended-only within the GO ADR spend ceiling; read the ceiling from the ADR, never quote it from memory. | R11 abs |  |
| SKILL02-67 | Invariant 7 L43 | Take sizing law from dd_protection/lifecycle with integer flooring proven against the F2 oracle; apply WATCH haircuts at the account-multiplier layer, never via TV risk%-input scaling. | R14 det |  |
| SKILL02-68 | Invariant 8 L44 | Read venue facts from their owners (venue edition, ADRs), never re-derive them from older briefs or the skill; treat the contract cap as account-aggregate, allocated per leg. | R29 abs |  |
| SKILL02-69 | Invariant 9 L45 | Keep pre-S2 Pine venue-edition alerts JSON-only; any Pine-edition change re-runs pine_check and re-pins in the same motion. | R14 det |  |
| SKILL02-70 | Invariant 10 L46 | Run listener and signal daemon on Fly or always-on hosts; the desktop is console-only for them, though route-local interactive work is allowed. | R41 abs |  |
| SKILL02-71 | Invariant 10 L46 | Prefer c1_rail_arm.py, write_volume_config.py and export_session_evidence.py over hand-editing rail volume JSON. | R11 det |  |
| SKILL02-72 | File map L48 | Before any rail change, read the file-map surfaces in the listed order. | R0 det |  |
| SKILL02-73 | Standing context L66 | Take lifecycle tiers from strategy_lifecycle.md and core/lifecycle.py; never infer them from rail history. | R15 abs |  |
| SKILL02-74 | Standing context L67 | Read instrument ledgers before touching a leg: MICRO cards own leg state; parent cards hold only shared venue geometry. | R27 abs |  |
| SKILL02-75 | Standing context L68 | Do not open a fills/exits execution-quality workstream or route depth/microstructure pulls until S4 delivers a fill path (suspended 2026-08-04). | R3 det | → docs/adr/2026-08-07-loop-s1-environment-ratification.md (Consequences) |
| SKILL02-76 | Verification L72-77 | For rail changes, run pytest tests/ops/ tests/rail_crosstrade/ and scripts/check_pine_manifest.py. | R21 det |  |
| SKILL02-77 | Verification L79 | Establish armed/disarmed state only by a host read (--status on /data/c1_rail_config.json), before and after any session touching the rail; local files never establish it. | R10 det |  |
| SKILL02-78 | Verification L87 | In Git-Bash, set MSYS_NO_PATHCONV=1 when a fly ssh -C string contains a /data volume path. | R10 det |  |
| SKILL02-79 | Verification L97-101 | Check the repo tracks only the two .example c1_rail_config files and DEFAULT_CONFIG_PATH is /data; these asserts never establish arm state. | R10 det |  |
| SKILL02-80 | Hand-offs L106-107 | Route firm rules, MC and dd_protection mechanics to prop-firm-challenge and Pine venue-edition code to pinescript-v6. | R9 det |  |
| SKILL02-81 | Hand-offs L108 | Acquire no market data: no source is approved, a new source needs explicit operator GO, and do not choose a substitute provider. | R18 abs |  |
| SKILL02-82 | Hand-offs L108 | Never connect, estimate, pull, batch, download or renew Databento via retained scripts or SDK; old keys, GOs or commands aren't authorization; offline fixtures never count as live M1 acceptance. | R18 abs |  |
| SKILL02-83 | Hand-offs L109 | Run handoff-verify before acting on any handoff brief that claims rail state. | R0 abs |  |

</details>

<details><summary><code>.claude/skills/code-defect-debugging/SKILL.md</code> — 44 rules: 6 absorbed, 37 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-84 | §0 L14-28 | Select the loop first: deterministic code defects here; statistical anomalies to inqhiori; live decisions to c1-rail; Pine to pinescript-v6; dd_protection expectations to prop-firm-challenge. | R9 det |  |
| SKILL02-85 | §0 L30-32 | Classify as a code defect when divergence persists across identical re-runs or the expected output is statable without statistics; run-to-run variance is an INQHIORI question. | R40 det |  |
| SKILL02-86 | Phase 1 L38-53 | Propose no fix until Phase 1 closes: deterministic reproduction, boundary inputs/outputs logged, and authority for expected values cited. | R40 det |  |
| SKILL02-87 | §1.1 L42 | Produce a minimal deterministic reproduction; for intermittent bugs, log every variable input until reproduction is deterministic. | R40 det |  |
| SKILL02-88 | §1.2 L44-49 | Log what the failing stage received, returned and should return, citing authority (reference implementation, closed form, locked baseline, MC invariant); 'felt right' is not authority. | R40 det |  |
| SKILL02-89 | §1.3 L51 | Record git log -1 for every file in the suspect path; for new bugs, diff last-known-good against HEAD. | R40 det |  |
| SKILL02-90 | Phase 2 L59-85 | Instrument every component boundary (type, shape, head/tail rows, dtype/units, invariant fields, in and out), run once, then analyze; no log-theorize cycles. | R40 det |  |
| SKILL02-91 | Phase 2 L87 | Close Phase 2 only when the failing component is named with line range, specific input and specific wrong output. | R40 det |  |
| SKILL02-92 | Phase 3 L93-99 | Form a hypothesis falsifiable by a one-line test at a named line; treat 'floating-point' or 'pandas weirdness' as last resort, falsified first by a magnitude check. | R40 det |  |
| SKILL02-93 | Phase 3 L112 | Test a hypothesis by injecting a distinguishing input and observing the predicted wrong output, not by applying a fix. | R40 det |  |
| SKILL02-94 | Phase 4 L122 | Make the smallest fix, the inverse of the confirmed hypothesis; no refactoring while in the area. | R40 det |  |
| SKILL02-95 | Phase 4 L124 | Re-run the Phase 1 reproduction after fixing; if output is still wrong, return to Phase 3. | R40 det |  |
| SKILL02-96 | Phase 4 L126 | Confirm locked CSV-reconcile baselines still match after a fix; a fix that breaks a locked baseline is structural and escalates to INQHIORI. | R14 det |  |
| SKILL02-97 | Phase 4 L128 | When a fix touches the MC path, run tests/core/test_mc_synthetic_engine.py; pin drift means structural change and escalates to INQHIORI; MC calibration figures are historical. | R14 det |  |
| SKILL02-98 | Phase 4 L130 | Diff the fix against HEAD; modified files must match the fix's logical scope exactly. | R40 det |  |
| SKILL02-99 | Phase 4 L132 | Sweep twins: name the wrong construct, search the whole repo including M-24 independent re-encodings, record 'TWINS: searched <pattern> — found <N>…' verbatim; fix or list them. | R40 det |  |
| SKILL02-100 | Phase 4 L134 | Land every repository-code fix with a regression test that reproduces the original symptom, failing on pre-fix code and passing after. | R40 det |  |
| SKILL02-101 | Phase 4 L134 | For defects in unmodifiable external sources, pin captured failing evidence with the consumer-side rule, add a consumer test that fails without the rule, and capture the lesson. | R40 det |  |
| SKILL02-102 | Phase 4.5 L140-153 | After three failed fixes on one issue, stop: no fourth hypothesis; question the architecture, hand methodology questions to inqhiori, file an ADR candidate and escalate. | R7 abs |  |
| SKILL02-103 | §6.1 L159 | Never add a correction factor or overlay that makes a symptom disappear while its cause remains. | R40 abs |  |
| SKILL02-104 | §6.4 L165 | Separate data quality from code by re-running on the canonical CME TV export; if the bug vanishes, hand off to trade-csv-reconcile. | R40 det |  |
| SKILL02-105 | §6.6 L169 | Graduate class-failure defects (over ~2 hours, a category not a typo) to a methodology lesson via brief-authoring lesson capture. | R36 det |  |
| SKILL02-106 | §8 L197 | When a defect surfaces under live time pressure, follow c1-rail safety invariants for the operational decision and defer the code fix to a later session. | R11 det |  |
| SKILL02-107 | §9 L206-213 | Do not change strategy parameters, allocations, dd_protection calibration, methodology rules or Pine through code-defect debugging. | R14 abs |  |
| SKILL02-108 | §10 L219-227 | Review the skill quarterly (defects, Phase-1 adherence, mis-routes, lessons, 4.5 firings); revise its description if mis-routes exceed one per quarter. | R28 DEL⚖ | Unenforced self-review cadence; no review recorded in SESSIONS/STATE; programme-audit owns cadence audits; ceremony under Rule 36. |
| SKILL02-109 | §11 L235-239 | Before writing or reviewing any fix, name the failure mechanism in one sentence; no band-aid before that; then the smallest source fix plus a regression test. | R40 abs |  |
| SKILL02-110 | §11 When it fires L268 | Treat a first visible TypeError, None, KeyError, parse or schema error as a symptom and trace it up to whoever produced the value. | R40 det |  |
| SKILL02-111 | §11 When it fires L269 | Treat 'flaky' failures as races or environment differences; rerun only an evidence-backed infrastructure outage read from the job log, recording the reason. | R40 det |  |
| SKILL02-112 | §11 When it fires L270 | When reviewing a diff adding a guard, default, retry, broad except, check=False, errors='ignore' or looser schema, require the named mechanism or mark it REFUTED. | R40 det |  |
| SKILL02-113 | §11 When it fires L271; step 3 L337-345 | If hooks, startup, caches, restore/migration, worker pools, refreshers or rewriters are in the suspect path, hunt the first unintended write; that side effect is the root cause. | R40 det |  |
| SKILL02-114 | §11 Banned L273-284 | Until the mechanism is named, ban None guards, catch-and-continue, retries or sleeps, parser widening, default-on-error or silent drops, correction factors and unexplained fixes. | R40 det |  |
| SKILL02-115 | §11 Designed fail-open L286-302 | Admit fail-open only if an owner names it, it emits a finding with status distinct from clean ('not checked' is not 'none found'), and never converts failure to success. | R40 det |  |
| SKILL02-116 | §11 Designed fail-open L304-309 | Never copy grandfathered fail-open paths that conflate could-not-run with none-found; tightening them is the owner's separate change, never a drive-by inside a fix PR. | R40 det |  |
| SKILL02-117 | §11 Designed fail-open L286-289 | The rail may fail closed on risk-add, never on risk reduction; exit/flat relay best-effort and raise a CRITICAL notification when evidence cannot be written. | R11 abs |  |
| SKILL02-118 | §11 Procedure L313 | State the observed failure concretely (exact error, command, commit); deterministic Python/shell defects run Phase 1 first; Pine defects route to pinescript-v6. | R40 det |  |
| SKILL02-119 | §11 Procedure L321 | Reconstruct the intended contract in three sentences from read sources under the INTENT authority order, never from the failing code's own shape. | R40 det |  |
| SKILL02-120 | §11 Procedure L327-336 | Trace the real path (backward call chain for crashes) with logs, tests and traces over inference; instrument once and read the whole capture before reasoning. | R40 det |  |
| SKILL02-121 | §11 Procedure L333-336 | Never log an env var's value, token, password, DSN or API key to test or CI logs; tell values apart by length plus hash-prefix fingerprint. | R12 det |  |
| SKILL02-122 | §11 Procedure L346 | Write the mechanism as 'given <input/state>, <site> does <operation>, so <wrong output>'; if you cannot, you are at a symptom, so go up a level. | R40 det |  |
| SKILL02-123 | §11 Procedure L349 | Reject each tempting band-aid explicitly in writing; a fallback the mechanism proves correct becomes designed fail-open with an owner and a finding. | R40 det |  |
| SKILL02-124 | §11 Procedure L352 | Fix at the source of the bad state; never make a contract more permissive unless the payload is proven intended; route architectural concerns to a Notice or ADR candidate. | R40 det |  |
| SKILL02-125 | §11 Procedure L356-367 | Verify each fix with before/after evidence of the original symptom in the artifact's strongest form; for non-code artifacts, run the consuming checker before and after. | R40 det |  |
| SKILL02-126 | §11 Procedure L369-380 | Add boundary validation only after the cause is fixed, following the owning path's failure policy; a new layer with no fail-open owner fails closed. | R40 det |  |
| SKILL02-127 | §11 Answer shape L384-395 | Carry ROOT CAUSE / FIX / VERIFICATION lines in fix reports and PR descriptions; no ROOT CAUSE means symptom fix; no before/after evidence means verification theater. | R40 abs |  |

</details>

<details><summary><code>.claude/skills/fable-method/SKILL.md</code> — 47 rules: 14 absorbed, 32 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-128 | Intro L8 | Where the fable source and a repo skill disagree, the repo skill wins; delegate evidence and authority channels to the named repo skills. | R29 det |  |
| SKILL02-129 | Intro L10 | Use the loop to structure work, never output: no step numbers or step headers in anything the operator reads. | R35 det |  |
| SKILL02-130 | Lane gate L12 | Before the loop, route falsifiable-H or lock work to inqhiori, live/rail calls to c1-rail, deterministic defects to code-defect-debugging; external handoffs always run handoff-verify first. | R9 det |  |
| SKILL02-131 | Triviality gate L14 | Treat a task as trivial only if one file, under ~10 lines, no new behavior and change already known; then change, run one check, report in two sentences. | R2 det |  |
| SKILL02-132 | Fit gate L16 | If an answer rests only on your inference, say so and label it; attended, ask before proceeding; unattended, proceed labeled; never dress a guess as rigor. | R21 det |  |
| SKILL02-133 | Step 0 L20-24 | Classify the ask: question yields findings and recommendation with no changes; task yields a verified change; plan-first (ambiguous, irreversible, locked surface) yields a plan, then stop. | R9 det |  |
| SKILL02-134 | Step 0 L26 | Break ties toward plan-first; when only the operator can settle an ambiguity, ask exactly one pointed question stating your recommended interpretation. | R3 det |  |
| SKILL02-135 | Step 0 L26 | Never re-litigate settled decisions; the rejected-candidates and rejected-signals registries are settled. | R26 abs |  |
| SKILL02-136 | Step 1 L30 | Define done in one or two sentences naming the actual verification gate; check single-call-checkable assumptions; if no verification can be named, ask one clarifying question. | R21 det |  |
| SKILL02-137 | Step 2.1 L34 | Open lab/CATALOG.md and docs/briefs/INDEX.md before searching prior research; an empty Grep over lab/archive or docs/ltm is not 'no prior work'. | R8 abs |  |
| SKILL02-138 | Step 2.1 L34 | Retrieve pruned docs/ltm bodies via git show pre-prune-2026-08-08:<path>. | R31 DEL | Superseded by docs/ltm/README.md: pre-prune-2026-08-08 tag absent on public clone (git tag -l empty); README owns retrieval. |
| SKILL02-139 | Step 2.2 L35 | Read the production file before any step touching risk controls (Rule 0), and run verify-source before quoting any pinned number. | R0 abs |  |
| SKILL02-140 | Step 2.3 L36 | Batch independent expensive lookups in parallel; chain only reads that shape the next read. | R35 det |  |
| SKILL02-141 | Step 2.4 L37 | Read narrow and never re-read; route input over 10+ files, 50k+ tokens or multi-hop reasoning to work-decomposition's input-shaped protocol. | R41 det |  |
| SKILL02-142 | Step 2.5 L38 | Time-box lookups to one round plus one follow-up; a third needs a stated reason; stop after two consecutive lookups that told you nothing new. | R2 det |  |
| SKILL02-143 | Step 2.6 L39 | Before changing behavior, find the intended-behavior statement and confirm code, check and spec agree; surface any disagreement, never silently align one side to another. | R40 det |  |
| SKILL02-144 | Step 2.7 L40 | State every surprise as a key finding; when it changes what done means or what is asked, update Step 1 or reclassify. | R9 det |  |
| SKILL02-145 | Step 2.7 L40 | Record question-shaped standalone findings as Notice logs under docs/notes/notice/, the live observation-routing convention. | R33 abs |  |
| SKILL02-146 | Step 3 L44 | Deliver one recommendation; give each seriously considered alternative one line on why it lost. | R35 det |  |
| SKILL02-147 | Step 3 L44 | Proceed without asking on task-shaped reversible actions; irreversible or outward-facing means observable before undo (push to main, merge, publish, live spend, registration, shared-data delete). | R3 det |  |
| SKILL02-148 | Step 3 L44 | Commit and push your own codex/ or claude/ branch and open a PR without a per-action quote; merging follows the operator's merge rule. | R6 abs |  |
| SKILL02-149 | Step 3 L46 | Take an irreversible or outward-facing action only with the operator's own words quoted as 'AUTH: operator said "…"'; otherwise propose it; documentation is not authorization. | R3 det |  |
| SKILL02-150 | Step 3 L48 | Name the files or surfaces in scope before acting; needing anything outside them is a surprise to state, never a silent expansion. | R3 det |  |
| SKILL02-151 | Step 4.1 L52 | Before a behavior-changing edit, write 'INTENT: code does X; check expects Y; spec says Z' from the opened spec; authority: operator > ADR/LOCK > tests > code. | R40 det |  |
| SKILL02-152 | Step 4.2 L53 | On first use of a signature, config key, constant or figure not opened this session, open its source or label it memory, unverified. | R0 abs |  |
| SKILL02-153 | Step 4.3 L54 | Make the smallest correct change in existing style; rewrite a whole file only if you authored it this session or fully read it. | R40 det |  |
| SKILL02-154 | Step 4.4 L55 | For 3+ heterogeneous steps or more than ~5 similar items, write a checklist and audit it against the ask; oversize checklists go to work-decomposition first. | R41 det |  |
| SKILL02-155 | Step 4.5 L56 | Never delete or overwrite without first looking at what is actually there. | R0 abs |  |
| SKILL02-156 | Step 4.6 L57 | Absent explicit operator instruction, never push to main, merge or force-push; your own codex/ or claude/ branch and PR are allowed. | R6 abs |  |
| SKILL02-157 | Step 4.6 L57 | Never weaken a check, or fabricate what it looks for, to make it pass. | R21 det |  |
| SKILL02-158 | Step 4.6 L57 | Never edit a test pin or baseline to green a failing run. | R21 det |  |
| SKILL02-159 | Step 4.6 L57 | Never regenerate SHA256SUMS without a same-commit data-change rationale. | R19 abs |  |
| SKILL02-160 | Step 4.6 L57 | Never touch Pine, dd_protection constants, firm_rules risk % or allocations outside a ratified ADR. | R14 abs |  |
| SKILL02-161 | Step 4.6 L57 | Never add a dependency absent explicit operator instruction. | R22 det |  |
| SKILL02-162 | Step 4.6 L57 | Never touch secrets or credentials. | R12 abs |  |
| SKILL02-163 | Step 5(a) L61 | Observe the done criterion pass (it ran, counted, rendered); never infer it from reading the code. | R21 abs |  |
| SKILL02-164 | Step 5(b) L62 | Verify the surrounding system: make validate, touched-area tests, check_boundaries.py when layers are crossed, MC re-run when the MC path is touched; a green target with a broken gate fails. | R21 det |  |
| SKILL02-165 | Step 5 L65 | Route failures (mechanical back to Step 4, surprise back to Step 2); on a blocker outside your control, stop and hand back with attempts, actual output and hypothesis. | R7 det |  |
| SKILL02-166 | Step 5 L67 | When something cannot be verified, say exactly that; never let an unverified claim pass as verified. | R21 abs |  |
| SKILL02-167 | Step 6 L71 | Open reports with what happened or was found; include no method scaffolding beyond owed INTENT/AUTH/TWINS/PENDING lines and the ROOT CAUSE block. | R35 det |  |
| SKILL02-168 | Step 6 L72 | Write complete sentences a returning teammate can follow; quote only load-bearing lines; define jargon at first use. | R35 det |  |
| SKILL02-169 | Step 6 L73 | Report caveats and failures with their output; mark each deliberately untaken prescribed follow-up 'PENDING: <action> — awaiting your authorization'. | R21 det |  |
| SKILL02-170 | Step 6 L74 | Delete scratch files you created and note the cleanup. | R31 det |  |
| SKILL02-171 | Step 6 L75 | Offer only follow-ups that emerged from the task; if none emerged, end without follow-ups. | R35 det |  |
| SKILL02-172 | Step 6 L76 | Before sending, add any missing owed INTENT, AUTH, PENDING, TWINS or ROOT CAUSE/FIX/VERIFICATION lines. | R35 det |  |
| SKILL02-173 | Modes L80-84 | In plan mode do Steps 0-3 and touch no file; in audit mode grade the latest work, apply the single fix only if asked; report mode rewrites per Step 6. | R9 det |  |
| SKILL02-174 | Modes L82 | Judge another session's finished work with handoff-verify post-execution judging, not fable audit mode. | R0 abs |  |

</details>

<details><summary><code>.claude/skills/fable-method/references/failure-modes.md</code> — 2 rules: 0 absorbed, 2 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-175 | Reading an audit L38 | In loop audits mark each step followed, skipped or faked; a faked step (claimed without observation) is worse than skipped and the audit must catch it. | R0 det |  |
| SKILL02-176 | Reading an audit L40 | If an audit can check only three things, check unprompted fixing (#1), retry thrash (#13) and verification theater (#14). | R0 det |  |

</details>

<details><summary><code>.claude/skills/futures-anomaly-discovery/SKILL.md</code> — 29 rules: 11 absorbed, 18 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-177 | Intro L26-29 | Generate candidates with trial count K attached and route them to validation unblessed; a discord, change point, feature or expression is an observation, never a trade. | R25 abs |  |
| SKILL02-178 | Intro L31 | Do not touch locked strategy code, allocations, dd_protection or MC calibration from discovery work. | R14 abs |  |
| SKILL02-179 | Pipeline L37-43 | Keep discovery in the Notice phase; the multiplicity floor only filters; crossing into Inquire licenses a hypothesis, never a promotion. | R25 det |  |
| SKILL02-180 | Harvest L52-60, L78 | Treat family K-bank as mandatory disclosure, not a gate; a pre-registered single-hypothesis seed screens at the same floor on every family. | R23 abs |  |
| SKILL02-181 | Harvest L76-78 | Admit external published mechanisms only via strategy_harvest.md §1's five admission requirements, checked before screening; do not restate the list. | R25 abs | *at HEAD:* changed: Admission requirements now "four", not five; Requirement 5 deleted 2026-10-24 (474f6fd8). |
| SKILL02-182 | Harvest L82-83 | Screen harvest seeds with lab/research_utils/axis_screen.py; its Cap/DSR/power/K-floor constants are frozen and never tuned per seed. | R23 det |  |
| SKILL02-183 | Harvest L84-86 | Treat a screen PASS as licensing campaign scoping only; downstream reachability, cost, universe, realism and survivor gates still bind. | R25 det | *at HEAD:* changed: Downstream "cost gate" replaced by "the candidate's own cost estimate"; other gates unchanged (474f6fd8). |
| SKILL02-184 | Harvest L86-87 | Declare K_intrinsic ≤3 at admission (confirm, don't mine); any post-admission widening voids the screen and becomes a new axis. | R25 abs |  |
| SKILL02-185 | Harvest L89-96 | Discharge a §R reachability attestation only by simulating in the gate's own units and scoring basis; check the Requirement 5 cost-law inequality at sourcing and admission. | R23 abs | *at HEAD:* changed: Same-units attestation kept; Requirement 5 cost-law check at sourcing/admission removed, gate deleted 2026-10-24 (474f6fd8). |
| SKILL02-186 | Rule 1 L98-106 | Register the search space K before examining results; never read a p-value or Sharpe off a mined candidate without registered K. | R23 abs |  |
| SKILL02-187 | Rule 1 L106-116 | Open mechanism-first (default) runs with reachability attestation, profile consult, an admission file clearing EM0/EM2-EM5, N-EDGE, DSR-cap and power, and --prereg; refusals write no manifest. | R23 det |  |
| SKILL02-188 | Rule 1 L110 | Treat EM1 and D1/D2 as disclosure-only, never refusal reasons. | R23 det |  |
| SKILL02-189 | Rule 1 L117-119 | Address any BLOCKING instrument_profiles consult (DEAD, AMBIGUOUS-PARKED, CONTINGENT-FORWARD) in the prereg or do not open; LIVE is a note. | R27 det |  |
| SKILL02-190 | Rule 1 L120-123 | Run wide blind mining only with an explicit --lane blind; a supplied admission file still enforces its refusals. | R23 det |  |
| SKILL02-191 | Rule 1 L123-126 | Open deep-lane runs with --prereg, grammar file and sha256, --confirm-years and --target-sr per the deep-lane charter; do not restate its §2.2 predicate. | R23 det |  |
| SKILL02-192 | Rule 1 L128-133 | Treat the live minimal gate set as G0-G5 + G8 plus any limb a campaign's own frozen prereg binds; --prereg records that binding path. | R24 abs |  |
| SKILL02-193 | Rule 1 L188-193 | Close a search only after a prior open; its manifest verdict is always a hand-off to strategy-validation, never a promotion; nothing exits discovery without a manifest. | R25 abs |  |
| SKILL02-194 | Stage-2/4 L201-202 | Run the stage24 runner synthetic-only; no data source is approved and db_fetch is the retired Databento client. | R18 det |  |
| SKILL02-195 | Stage-2/4 L203-205 | Keep the SPA/PBO path dormant; prefer temporal-consistency and campaign-named limbs; DSR/universe_gate default var_trials=1/n unless explicitly pinned. | R24 det |  |
| SKILL02-196 | Stage-2/4 L216-217 | Flag low-n candidates (≤250 OOS trades) dsr_unreachable_low_n; never drop them silently. | R24 det |  |
| SKILL02-197 | L219-223 | Route rigorous universe-level correction (White RC, SPA, Romano-Wolf) to strategy-validation; discovery only makes K a recorded fact. | R24 abs |  |
| SKILL02-198 | Rule 2 L225-236 | Use the least-overfit tool first: catch22 before full tsfresh, fixed or criterion ruptures penalties (pre-register sweeps), simple PySR Pareto knee, held-out likelihood for HMM state count. | R25 det |  |
| SKILL02-199 | Rule 3 L240-246 | Treat discovery outputs as candidates or conditioning variables, not signals; none is a strategy until it survives the native micro-era gate; PySR outputs need the strictest OOS. | R25 det |  |
| SKILL02-200 | Explanation deferred L250-253 | Do not buy explanatory data (gamma, GEX/DIX, COT) before a candidate survives validation; never deploy without a mechanism. | R18 det |  |
| SKILL02-201 | Red flags L259 | Log every penalty, feature-set or state-count sweep as K; never report only the best. | R23 abs |  |
| SKILL02-202 | Red flags L263-269 | Never reuse a frozen screen battery on a new claim family without re-validating its null against that family's confound; magnitude-persistence claims use the corrected battery spec. | R24 det |  |
| SKILL02-203 | Red flags L271-283 | Cite the governing null-validity doc for the claim family in every screen PREREG.md §0, valence-blind, whether the expected verdict is NULL or SIGNAL. | R23 det |  |
| SKILL02-204 | Hand-offs L285-293 | Route the gate to strategy-validation, inquire-worthiness to inqhiori, graduating candidates to brief-authoring and harvest admission to strategy_harvest.md. | R9 det |  |
| SKILL02-NEW-1 | Harvest L94-97 | Evaluate each candidate's cost through its own net-return, execution-uncertainty and cost-sensitivity estimate (strategy_harvest.md §1 row 5); treat cost_geometry_pregate.py as reporting stop-distance R only. | R24 det | → docs/methodology/strategy_harvest.md §1 row 5 · *at HEAD:* new 474f6fd8 |

</details>

<details><summary><code>.claude/skills/futures-anomaly-discovery/reference/proxy-discipline.md</code> — 7 rules: 0 absorbed, 6 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL02-205 | Why parents L10-12 | Use parent-contract history for structural discovery only, never as-is for P&L, position sizing or fill modeling. | R24 det |  |
| SKILL02-206 | Adjustments L18-21 | Re-scale parent-derived economics to the micro spec; recompute every P&L, drawdown and MC bust input on micro tick value. | R24 det |  |
| SKILL02-207 | Adjustments L22-25 | Fit slippage and fill models on native micro-era data; never inherit the parent's fill model. | R24 det |  |
| SKILL02-208 | Adjustments L26-29 | Reserve 2019-to-present native micro data as a genuine OOS regime-consistency gate a parent-discovered anomaly must pass before deployment. | R24 det |  |
| SKILL02-209 | Contract specs L33-35 | Confirm live contract specs against CME before sizing; code consumes them from core/instrument_specs.py. | R17 det |  |
| SKILL02-210 | FX/JPY L50-53, L62 | Use MJY (not M6J) for micro JPY; check its thin liquidity and margin fresh before any campaign sizing. | R27 DEL⚖ | ops/instruments/MJY.md: MJY RETIRED as execution/replay venue 2026-07-05; symbology owned by MJY.md M4; revival only via Bulenox. |
| SKILL02-211 | FX/JPY L56-60 | When mapping USDJPY-specified Aegis onto 6J/MJY, invert direction (long USDJPY ≈ short 6J/MJY) with USD tick value off the JPY/USD price before generating rows. | R24 det |  |

</details>

<details><summary><code>.claude/skills/futures-anomaly-discovery/reference/tool-discipline.md</code> — 21 rules: 1 absorbed, 20 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL03-1 | Intro L3-6; Unifying rule L129-132 | Treat every discovery-tool output (motif, discord, segment, feature, state, expression) as a K-bearing Notice-phase observation; discovery never blesses a signal or entry; a discord's surprise is not edge. | R25 abs |  |
| SKILL03-2 | Unifying rule L132-135 | Route a mined candidate to Inquire as a falsifiable hypothesis only once it is K-registered and clears the first-pass multiplicity floor (register_search.py close). | R25 det |  |
| SKILL03-3 | STUMPY L12-18 | Pre-register the matrix-profile window-length set and series scope as part of K; count each distinct window length as a separate search; prefer a small principled set over a sweep. | R23 det |  |
| SKILL03-4 | ruptures L24-28 | Fix the change-point penalty (or n_bkps) by a principled criterion or pre-register the sweep grid in K; never report only the best segmentation. | R23 det |  |
| SKILL03-5 | ruptures L28-29; tsfresh L41; HMM L52 | Use change points and HMM states only as conditioning variables (regime labels) and selected features only as covariates, never as signals or strategies. | R25 det |  |
| SKILL03-6 | tsfresh/catch22 L36-41 | Extract catch22 features first; escalate to full tsfresh only when catch22 is demonstrably insufficient, carrying the full feature count into K (FRESH FDR is per-run only). | R23 det |  |
| SKILL03-7 | HMM L47-52 | Choose the HMM state count by held-out likelihood or a pre-registered criterion, never by in-sample fit. | R23 det |  |
| SKILL03-8 | HMM L48-50; symbolic regression L68-70 | Count every restart, seed and init attempt in declared K; a re-run with a new seed is a new search increment, not a free peek. | R23 det |  |
| SKILL03-9 | HMM L52-57 | Condition real-time tests or trades only on filtered (forward-only) state probabilities or a trailing realized-vol bucket; full-sample decode or smoothed posteriors are look-ahead leaks. | R24 det |  |
| SKILL03-10 | HMM L57-58 | Fit HMMs on in-sample data only; never re-fit on the OOS era. | R24 det |  |
| SKILL03-11 | gplearn/PySR L67-68 | Pre-register the symbolic-regression operator set, complexity ceiling and population/generation budget as the bounded declared search. | R23 det |  |
| SKILL03-12 | gplearn/PySR L70-74 | Prefer Pareto-knee expressions; treat a symbolic-regression survivor as a curiosity until it clears the strictest OOS plus universe-level correction. | R24 det |  |
| SKILL03-13 | Pre-mining hygiene L82-85 | Normalize intraday series by the time-of-day volatility curve before mining any time-of-day effect. | R25 det |  |
| SKILL03-14 | Pre-mining hygiene L86-88 | Use the prevailing top-of-book midpoint, not trade prints, for short-horizon mean-reversion or reversal mining. | R25 det |  |
| SKILL03-15 | Back-adjustment L93-101 | Never compute percentage returns or level-based signals on a difference-adjusted continuous series; evaluate entries, exits and P&L on the tradeable contract's prices. | R24 det |  |
| SKILL03-16 | Back-adjustment L100-102 | Check calendar-adjacent anomalies against the roll schedule; confirm the source's roll rule and price adjustment before a deep build, never assuming either. | R18 det |  |
| SKILL03-17 | Roll rule L103-111 | Use a volume-rolled continuous series for any TradingView 1! comparison or liquidity/coverage measurement; calendar-rank front-month series change which bars exist. | R18 det |  |
| SKILL03-18 | Session & clock L114-116 | Slice RTH-only hypotheses to RTH bars explicitly; ETH bars are a different population. | R25 det |  |
| SKILL03-19 | Session & clock L117-119 | Treat a daily bar as a Globex trade date opening 17:00 America/Chicago the prior day, not a midnight-UTC day. | R25 det |  |
| SKILL03-20 | Session & clock L120-121 | Convert session filters to DST-aware America/Chicago time rather than fixed UTC hours, and spot-check DST boundary weeks. | R25 det |  |
| SKILL03-21 | Session & clock L122-123 | Exclude or flag holiday half-sessions so session-return statistics do not mix full and half days. | R25 det |  |

</details>

<details><summary><code>.claude/skills/handoff-verify/SKILL.md</code> — 39 rules: 13 absorbed, 26 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL03-22 | When to use L12-20 | Run the Phase-0 checklist before executing any instruction packet not derived from a fresh Rule-0 read this turn (CC briefs, advisor notes, spawn prompts, 'already landed' claims). | R0 abs |  |
| SKILL03-23 | When to use L21 | Skip Phase-0 only for a plan written this session after reading the files; still apply verify-source to any borrowed number. | R0 det |  |
| SKILL03-24 | Size-triggered escalation L23-27 | For long packets with many distinct claims, run the same Phase-0 checklist as the handoff-verify-panel workflow instead of inline. | R0 det |  |
| SKILL03-25 | Phase-0 L29-31; Rationalizations L140 | On any Phase-0 hard fail, stop and return NEEDS_CONTEXT with paths/SHAs; never improvise repairs to the handoff or fix premise errors as you go. | R4 abs |  |
| SKILL03-26 | Phase-0 §1 L33-43 | Confirm you are in the intended worktree; if behind origin/main on cited files, read origin/main's copy or merge the base before trusting checkout prose. | R0 det |  |
| SKILL03-27 | Phase-0 §2 L45-55 | Verify every load-bearing path a handoff cites exists (git ls-files, or ls for gitignored data); hard-fail when a claimed canonical or landed path is absent. | R0 det |  |
| SKILL03-28 | Phase-0 §2 L55; Rationalizations L141 | Never author a missing artifact to make a handoff coherent unless the operator explicitly redirects scope. | R0 det |  |
| SKILL03-29 | Phase-0 §3 L57-62 | Open each cited ADR/brief and compare its on-disk status line with the handoff's claim; treat the handoff as stale when a later addendum already ratified. | R0 det |  |
| SKILL03-30 | Phase-0 §3 L61 | Read closure vocabulary from the closure filename (Q-…-closure-<verdict>); never invent disposition fields such as 'disposition: PARK'. | R28 det |  |
| SKILL03-31 | Phase-0 §4 L64-73 | Grep for a handoff's key deliverables; if the work already landed, return NEEDS_CONTEXT with the landing SHA/PR and never re-run a scored one-shot. | R0 det |  |
| SKILL03-32 | Phase-0 §5 L77; fraud table L181 | Treat challenge-era MC pass/bust rates as historical engine pins, never as live pass-probabilities. | R20 abs |  |
| SKILL03-33 | Phase-0 §5 L78; fraud table L181 | Read live posture only from AGENTS.md §Live-execution posture; mark a handoff STALE if it assumes any listed retired premise (armed book, external Tradeify route, Databento pull, CLAUDE.md, etc.). | R0 det |  |
| SKILL03-34 | Phase-0 §5 L79 | Before relying on any specific constant in a handoff (risk %, DD_TRIGGER, anchor), apply verify-source: check branch currency and open the bytes. | R0 abs |  |
| SKILL03-35 | Phase-0 §6 L81-83 | Before a research handoff freezes a campaign gate, confirm a reachability/power attestation exists or is tasked; never start pulls against a gate an audit called unreachable. | R23 abs |  |
| SKILL03-36 | Phase-0 §7 L85-87 | Check CLI handoffs against the shared execution contract: actions must fit recorded authority, paths, working directory and worker capabilities; carry authorization forward, report only gaps or material conflicts. | R33 abs |  |
| SKILL03-37 | Phase-0 §7 L87 | Report CLI dispatch errors separately from packet-state contradictions, preserving the exact error and writing 'unknown' when the cause is unproven. | R33 abs |  |
| SKILL03-38 | Phase-0 §8 L93-94 | For a brief-dispatched card, verify the dispatch pointer's SHA matches the brief on origin/main or the pinned commit; on mismatch return NEEDS_CONTEXT. | R4 det |  |
| SKILL03-39 | Phase-0 §8 L95-96 | For a lightweight-issue card, recompute the issue-body sha256 and match the coordinator's pre-dispatch read comment; mismatch or missing comment returns NEEDS_CONTEXT. | R4 det |  |
| SKILL03-40 | Phase-0 §8 L97-98 | Require named acceptance tests, each with the property it must violate to fail; if absent return NEEDS_CONTEXT and never substitute tests you write. | R33 det |  |
| SKILL03-41 | Output shape L100-121 | Report Phase-0 as a HANDOFF-VERIFY: PASS block (toplevel, branch@sha, card, acceptance, checked, proceed) or a NEEDS_CONTEXT block (failed, on-disk, do-not). | R0 det |  |
| SKILL03-42 | Post-execution L148-150 | Treat completed-work reports as claims, not evidence; never accept a worker-implemented frozen spec, PR or external RESULTS verdict on its own report—judge it against artifacts. | R0 abs |  |
| SKILL03-43 | Procedure 1-2 L156-157 | List the report's done/verified/untouched claims, take git diff as ground truth, and compare touched files against declared scope and forbidden moves. | R0 det |  |
| SKILL03-44 | Procedure 3 L158-160; fraud table L178 | Re-run every claimed verification yourself and count skips; vendor-skipped tests and pass claims without shown output are not passes. | R0 det |  |
| SKILL03-45 | Procedure 3 L161 | Run tests/core/test_mc_synthetic_engine.py whenever anything on the MC path changed; it is the vendor-free engine regression. | R21 det |  |
| SKILL03-46 | Procedure 3 L162 | Verify any layer-contract claim (lab↔ops isolation, core imports nothing internal) by running scripts/check_boundaries.py. | R37 abs |  |
| SKILL03-47 | Procedure 3 L163 | Back byte-identical or no-functional-change claims with an actual diff or hash, never prose. | R21 det |  |
| SKILL03-48 | Procedure 3 L164 | Label any claim that cannot be re-run here (missing vendor CSVs, TradingView-side behavior) UNVERIFIABLE, never assumed true. | R21 det |  |
| SKILL03-49 | Fraud table L176 | Treat any edited test pin, tolerance, baseline row, or loosened/deleted/skipped assertion as fraud until its justification traces to a ratified ADR. | R21 det |  |
| SKILL03-50 | Fraud table L177 | Flag SHA256SUMS regenerated without a same-commit data-change rationale, or data changed without a manifest delta. | R19 abs |  |
| SKILL03-51 | Fraud table L179 | Flag any diff touching Pine, dd_protection constants, firm_rules risk % or allocations without a ratified ADR. | R14 abs |  |
| SKILL03-52 | Fraud table L180 | Flag any push to main, merge, publish, account registration or live spend lacking an operator quote; rail build and registration are ADR-gated, no live spend. | R4 det |  |
| SKILL03-53 | Fraud table L182 | Quote PF/WR/p99/DD only with their cohort (n, filter, window); flag any metric whose denominator did not travel with it. | R20 abs |  |
| SKILL03-54 | Fraud table L183 | Resolve conflicts by authority order—explicit operator statement > ADR/LOCK > tests > current code; never change code to satisfy a check contradicting the ADR/LOCK. | R3 det | → .claude/skills/fable-method/SKILL.md (Intent gate) |
| SKILL03-55 | Fraud table L184 | Flag scratch files, debug prints, orphan worktrees and commented-out code as debris; route cleanup to repo-hygiene. | R6 det |  |
| SKILL03-56 | Procedure 5 L166-170 | Deliver the verdict first (VERIFIED / VERIFIED WITH CAVEATS / REFUTED), then claims table, frauds and action; never soften a refutation or inflate a caveat. | R0 det |  |
| SKILL03-57 | Standing rules L188 | Judging changes nothing: read and run only; apply fixes only if the operator asks afterward. | R0 det |  |
| SKILL03-58 | Standing rules L189 | Keep judging to minutes; if verification needs an environment you lack, hand it back rather than guess. | R0 det |  |
| SKILL03-59 | Standing rules L190 | Route statistical-soundness questions (overfitting, multiplicity, SNAG) to strategy-validation once claims reproduce; the judge checks claims versus artifacts only. | R0 det |  |
| SKILL03-60 | Standing rules L191 | If the work touched nothing runnable, state plainly what a judge can and cannot check. | R21 abs |  |

</details>

<details><summary><code>.claude/skills/inqhiori/SKILL.md</code> — 31 rules: 28 absorbed, 3 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL03-61 | Header L10; §13 L290 | Treat docs/methodology/inqhiori-canon.md as canonical—trust it when this skill disagrees—and reference it, not the archived predecessor pages. | R29 abs |  |
| SKILL03-62 | §0 L21-33 | Read production source this session before INQHIORI Identify or any decision brief (risk controls especially); memory and prior briefs feed the corpus, never replace it; otherwise stop and read. | R0 abs |  |
| SKILL03-63 | §0 L35-40 | Declare the loop class at task start and take the iteration budget from the Rule 2 ADR; never restate its numerals in this skill. | R2 abs |  |
| SKILL03-64 | §1 L46-53 | Run the loop as Rule 0 read → Identify → Notice → D-S-A pre-Q gate → Question → Hypothesis → …; the gate filters and indexes I/N data before Questions. | R9 abs |  |
| SKILL03-65 | §2 L57-65; §13 L294 | Name the D-S-A domain (data = I/N corpus, system = post-H artefact, meta-process = framework) before acting; never conflate domains; ask when unsure. | R9 abs |  |
| SKILL03-66 | §3 L71-82; §13 L291 | Give every Inquire-phase brief a three-line Pre-Q gate header (D, S, A) after Context; any 'no action' line must say why—silence is not allowed. | R9 abs |  |
| SKILL03-67 | §3 L84-92; §2 L65; §13 L292 | Give every structural-change brief a 'D-S-A domain:' header after the title, declaring each domain and the cascade when more than one applies. | R9 abs |  |
| SKILL03-68 | §4 D L98-102 | Log the test behind every D deletion; keep the raw I/N corpus as the Rule 0 anchor and produce a derived working set, never a destructive overwrite. | R9 abs |  |
| SKILL03-69 | §4 S L104-107; §6 L148 | Simplify only to a representation that preserves the Noticed anomaly; if S removes the signal, revert. | R9 abs |  |
| SKILL03-70 | §4 A L109-112; §6 L149 | Keep Accelerate bounded: index only when cheaper, in expectation, than the queries it enables. | R9 abs |  |
| SKILL03-71 | §5 L118-120 | Keep a datum whenever its presence could contradict a hypothesis not yet formed; if answering requires forming the hypothesis, the datum stays. | R9 abs |  |
| SKILL03-72 | §5 L122-126 | Never apply forbidden D-tests: known physical/causal mechanism, fits-my-model, high signal-to-noise, or useful-before. | R9 abs |  |
| SKILL03-73 | §5 L128-134 | Apply only permitted D-tests (documented artefact, higher-fidelity duplicate, out of scope, literal copy); declare any new test and surface it to Joshua before applying, logging it. | R9 abs |  |
| SKILL03-74 | §5 L136-140; §13 L295 | On detecting a forbidden D-test, stop the deletion and surface the test and items to Joshua; never substitute a permitted test producing the same deletion. | R9 abs |  |
| SKILL03-75 | §6 L146 | Cap pre-Q gate effort near 10% of I/N effort; exceeding it means I/N was wrong—restart the outer loop; tune the split after about five gated loops. | R9 abs |  |
| SKILL03-76 | §6 L147; §9 L229 | When a deletion later proves to matter or a forbidden D-test is caught, run a gate audit (criterion review, not just restoration) at docs/notes/audits/YYYY-MM-DD_gate_<slug>.md. | R9 abs |  |
| SKILL03-77 | §6 L150 | Log every iteration where the gate resurfaces data a prior gate deleted; repeated failures of one criterion mean that D-test class is too aggressive. | R9 abs |  |
| SKILL03-78 | §6 L151-162 | When three falsifiable hypotheses sharing one parent question and analysis level close NULL or AMBIGUOUS, STOP; author no fourth at that level. | R28 det | → docs/methodology/inqhiori-canon.md §6 |
| SKILL03-79 | §6 L155-157 | At exhaustion, either reformulate the question structurally (new framing, unit, D-test or domain; Q-numbering resets) or close the thread AMBIGUOUS-by-exhaustion. | R28 det | → docs/methodology/inqhiori-canon.md §6 |
| SKILL03-80 | §6 L158 | Never relax gate criteria to let a fourth hypothesis pass after exhaustion. | R23 abs |  |
| SKILL03-81 | §8 L209 | D acting on a framework implicitly authorizes corpus-level D on that framework's data; D on data alone never authorizes framework changes. | R9 abs |  |
| SKILL03-82 | §10 L235; §13 L288 | Select the loop first: structural/low-reversibility/statistical work uses INQHIORI, tactical/tempo work OODA, live execution c1-rail; if H cannot be stated in one sentence, not INQHIORI. | R9 abs |  |
| SKILL03-83 | §10 L236 | Route deterministic code defects (wrong values, crashes, reproducible divergence) to code-defect-debugging; keep unexpected statistical behavior in INQHIORI. | R40 abs |  |
| SKILL03-84 | §10 L238 | Apply the small-cell variance prior: small cohorts trigger caution at Observe/Reflect regardless of how the gate filtered the corpus. | R1 abs |  |
| SKILL03-85 | §10 L239 | Build no regime or conflict overlay (e.g. on physical facts) without a full INQHIORI loop showing the base logic is insufficient. | R1 abs |  |
| SKILL03-86 | §10 L240 | Route narrative observations that pass the gate through the Notice log (docs/notes/notice/N-YYYY-MM-DD-slug.md, GRADUATE/DROP/HOLD), not Closed/Action/Forward. | R33 abs |  |
| SKILL03-87 | §10 L241 | End each closure with a mandatory '## Iterate' block (Next: INTEGRATE\|ITERATE\|STOP, entry packet, stop rule, board write), pre-registered per verdict in the brief's §6. | R28 abs |  |
| SKILL03-88 | §10 L241 | An ITERATE disposition names a successor but never opens it; opening one requires operator GO. | R28 abs |  |
| SKILL03-89 | §11 L249; §10 L243; frontmatter | Methodology work never modifies or restates strategy parameters/code, allocations, dd_protection constants, re-MC triggers or MC calibration. | R14 abs |  |
| SKILL03-90 | §12 L253-282 | Write gate audits with Trigger, Loop context, What the gate did, What went wrong, Criterion update and Cross-references; keep them short. | R9 det | → docs/methodology/inqhiori-canon.md §10 |
| SKILL03-91 | §13 L293 | The pre-Q gate is user-gated at D: agents propose deletions; Joshua authorizes them. | R3 abs |  |

</details>

<details><summary><code>.claude/skills/pinescript-v6/SKILL.md</code> — 19 rules: 3 absorbed, 16 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL03-92 | frontmatter L3 | Read accepted-book Pine in place under AGENTS.md §Public-clone posture; never copy or quote it. | R13 abs |  |
| SKILL03-93 | Syntax L14-37 | Keep Pine ternary expressions on one line, or assign long branches to intermediate variables. | R14 det |  |
| SKILL03-94 | Line wrapping L41-65 | Indent every Pine continuation line more than its first line and break after operators or commas. | R14 det |  |
| SKILL03-95 | Systematic check L67-76 | Before finalizing Pine, review declarations, plots, multi-condition ifs, long assignments, entries/exits, alerts, tables, labels/boxes and lines over 80 characters. | R14 det |  |
| SKILL03-96 | Plot scope L80-102 | Never call plot() inside a local scope (if, for, function); use conditional series or line/label/box objects instead. | R14 det |  |
| SKILL03-97 | Structure template L106-131 | Structure scripts as //@version=6, declaration, then INPUTS, CALCULATIONS, CONDITIONS, PLOTS and ALERTS sections. | R14 det |  |
| SKILL03-98 | Strategy Report traps L147-155 | Before rewriting entries because 'trades stopped', read the Strategy Report note and flip the testing-period chip on the same script; the price pane is not the Strategy Report. | R40 det |  |
| SKILL03-99 | Strategy Report traps L158 | Do not gate diagnostic tables on barstate.islast; put a var table of strategy.closedtrades on the candlestick pane. | R40 det |  |
| SKILL03-100 | Strategy Report traps L155, L160 | Do not conclude a series ended from Last-N emptiness, a dying dated front month, or the Performance-tab rightmost node; compare entire-history with Last-N. | R40 det |  |
| SKILL03-101 | Strategy Report traps L162 | Strategy Report trap findings do not unpark a FALSIFIED or PARK candidate. | R26 abs |  |
| SKILL03-102 | Best practices L168-171 | Avoid repainting: use barstate.isconfirmed for signals and request.security with lookahead_off; document any intentional repainting. | R14 det |  |
| SKILL03-103 | Best practices L173-176 | Minimize security() calls, cache repeated calculations, and prefer switch over long if/else chains. | R14 det |  |
| SKILL03-104 | Best practices L178-181 | Group inputs with group=, add tooltip= to complex inputs, and use sensible defaults. | R14 det |  |
| SKILL03-105 | Best practices L183-185 | Check na values before operations and handle edge cases such as first bars and division by zero. | R14 det |  |
| SKILL03-106 | Config-fingerprint L189-197 | Embed the current [cfgNN] config ID in every ACTIVE-DERIVATION strategy title, updated each run to match the configuration actually loaded. | R27 det |  |
| SKILL03-107 | Config-fingerprint L198 | Step-0 reconcile parses the cfg tag from the export filename and verifies it against the declared run; halt analysis on mismatch. | R24 det |  |
| SKILL03-108 | Config-fingerprint L199 | Never retro-tag frozen or pre-registered scripts for convention uniformity; their exports are identified by the pre-registration. | R23 abs |  |
| SKILL03-109 | Config-fingerprint L200 | Adopt the cfg tag in existing active scripts only at their next legitimate edit, never as a standalone title-only touch. | R27 det |  |
| SKILL03-110 | Code review checklist L206-217 | Review Pine against the checklist: version declaration, title/overlay, input tooltips and groups, no repainting, na handled, efficiency, clear names, comments, plot styling, alerts. | R14 det |  |

</details>

<details><summary><code>.claude/skills/programme-audit/SKILL.md</code> — 33 rules: 2 absorbed, 30 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL03-111 | Source-of-truth L10 | Where a more recent audit that demonstrably worked disagrees with this skill body, the audit wins; flag the skill for update. | R29 det |  |
| SKILL03-112 | Trigger conditions L18-28 | Run a programme audit immediately on any degeneration signal: uncorroborated belt-patches, belt only growing, falsifier drift, rationalizing methodology, SNAG, cross-layer contamination, or tolerated forbidden move. | R28 det |  |
| SKILL03-113 | Scheduled cadence L30-33 | Audit methodologies quarterly; audit the portfolio semi-annually or on degeneration signals or six months of new live data, never calendar-forced without new evidence. | R28 det |  |
| SKILL03-114 | Coupling rules L44-48 | Never promote methodology verdicts to portfolio verdicts; portfolio verdicts may trigger methodology audits, never the reverse. | R28 det |  |
| SKILL03-115 | Operational consequence L50; Known trap 2 L122 | Keep audit layers separate: portfolio audits never cite methodology verdicts, methodology audits never cite portfolio performance; cross-layer synthesis is a separate document. | R28 det |  |
| SKILL03-116 | Seven diagnostic questions L54-88 | Answer all seven diagnostic questions in every audit, each grounded in an evidence anchor (commit, path or number). | R28 det |  |
| SKILL03-117 | Diagnostic Q2 L63-65; Known trap 4 L126 | Tally belt adds versus removes explicitly; net growth across consecutive audits is a yellow flag, across three or more a red flag. | R28 det |  |
| SKILL03-118 | Diagnostic Q7 L86-88; Known trap 5 L128 | Verify falsifiers still sit at original thresholds by grep/diff against locked values and report the diff; drift is disqualifying. | R28 det |  |
| SKILL03-119 | Five verdicts L94-100 | End each audit cycle with exactly one verdict per programme: Progressive, Stable, Degenerating, Falsified or Ambiguous. | R28 det |  |
| SKILL03-120 | Five verdicts L98-99; Known trap 7 L132 | Give every Degenerating or Falsified verdict at least one named follow-up action (prune ADR, INQHIORI loop, restructure) with owner and date. | R28 det |  |
| SKILL03-121 | Five verdicts L100; Known trap 3 L124 | Date every Ambiguous verdict and name the specific resolving evidence, re-test conditions and target date. | R28 det |  |
| SKILL03-122 | Audit artifact L106-112 | Land programme audits at docs/notes/audits/programme-audit/YYYY-MM-DD-<layer>-audit.md using brief-authoring's audit_note template with §1, §3, §4, §5 and §10 content. | R28 det |  |
| SKILL03-123 | Known trap 1 L120 | Write the §3 evidence before the §4 verdict; an audit whose verdict preceded its evidence is theater. | R28 det |  |
| SKILL03-124 | Known trap 6 L130 | When no new evidence or degeneration signal exists, collapse the scheduled audit to a one-line status update. | R28 det |  |
| SKILL03-125 | Discipline check L138-149 | Run the discipline checklist (seven answers, churn tally, falsifier diff, layer check, verdict, follow-ups, re-test conditions, §10 hooks) before declaring an audit complete. | R28 det |  |
| SKILL03-126 | Reference files L153-159 | Author methodology and portfolio audit templates and a degeneration-signal catalog from the first completed audits; until then follow this body. | R28 DEL | references/ never authored; superseded by brief-authoring references/audit_note.md plus the skill's audit-structure section, used by nine audits since 2026-08-03. |
| SKILL03-127 | Decay sweep cadence L209-211 | Run the ADR decay sweep alongside the quarterly meta-layer audit; never add a second standing calendar trigger. | R28 det |  |
| SKILL03-128 | Decay sweep event triggers L213-224 | Also run the decay sweep before repo-public snapshots, external handoffs or onboarding, after large ADR batches, on operator request, or when one ADR's falsifier fired undischarged. | R28 det |  |
| SKILL03-129 | Decay sweep boundary L197-203 | Run blast-radius right after an edit touching an ADR's subject; run the decay sweep independently; never equate a clean sweep with a healthy programme. | R28 det |  |
| SKILL03-130 | Method L230-232, L261-266; Decay-sweep trap 5 L302 | Read under ~30 Accepted ADRs inline; above that use a batch scan→verify fan-out, sizing batches to typical ADR length rather than a fixed constant. | R41 det |  |
| SKILL03-131 | Phase 1 L234-250 | In Phase 1, check each ADR's top override blockquote, falsifier/expiry clauses, current-fact claims against current source, and Supersedes headers in both directions. | R28 det |  |
| SKILL03-132 | Phase 1 L251-253 | Never flag an ADR merely because its one-time action is complete; flag only when current reality contradicts what it asserts. | R28 det |  |
| SKILL03-133 | Decay-sweep trap 3 L293-296 | Treat decay as drift since ratification; an ADR wrong on day one is a ratification-quality failure with a different fix. | R28 det |  |
| SKILL03-134 | Verdicts L255-259 | Score each ADR STILL_APPLICABLE, DECAYED_DOCUMENTED, DECAYED_UNDOCUMENTED or UNCERTAIN; UNCERTAIN must name the resolving evidence and a re-check date or trigger. | R28 det |  |
| SKILL03-135 | Phase 2 L268-278 | Give every non-STILL_APPLICABLE flag an independent refute-first Phase-2 re-derivation, fanning out only over the flagged subset. | R28 det |  |
| SKILL03-136 | Decay-sweep trap 1 L284-288 | Sanity-check reviewer output content; re-run or hand-verify any schema-valid but placeholder or empty verdict before trusting it. | R41 det |  |
| SKILL03-137 | Decay-sweep trap 2 L289-292 | Check index/summary mirrors for the same stale claim as the source ADR and fix both. | R30 abs |  |
| SKILL03-138 | Decay-sweep trap 4 L297-301 | Judge ADR-corpus health by the DECAYED_UNDOCUMENTED count; report DECAYED_DOCUMENTED for completeness without reading it as ill-health. | R28 det |  |
| SKILL03-139 | Decay-sweep trap 6 L305-310 | Give every DECAYED_UNDOCUMENTED finding a named remediation and owner—fixed in-session or logged forward in STATE.md with a date. | R28 det |  |
| SKILL03-140 | Decay-sweep trap 7 L311-316 | After several consecutive all-clear sweeps, hand-spot-check one Phase-1 batch's evidence. | R28 det |  |
| SKILL03-141 | Output artifact L320-336 | Land the sweep at docs/notes/audits/adr-corpus/YYYY-MM-DD-adr-decay-audit.md with verdict counts, reclassifications, full undocumented entries, a compact documented list, and named failed Phase-2 calls. | R28 det |  |
| SKILL03-142 | Remediation weight L338-342 | Record ADR drift as a discharge addendum without full ceremony; author a new ADR only when the remediation changes a rule, gate or convention. | R32 abs |  |
| SKILL03-143 | Decay discipline check L349-358 | Enumerate Accepted ADRs from actual Status headers, cover every one in Phase 1 without silent drops, and name the next trigger before closing. | R28 det |  |

</details>

<details><summary><code>.claude/skills/prop-firm-challenge/SKILL.md</code> — 40 rules: 21 absorbed, 17 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL03-144 | Intro L8; Firms L67; Snapshot L83 | Read firm-specific values from core/firm_rules.py directly; never hardcode them in this skill—its snapshot table is a mirror, so trust the file. | R16 abs |  |
| SKILL03-145 | Posture L10-14 | Read rail posture from AGENTS.md §Live-execution posture and the c1-rail skill; never restate it here. | R10 abs |  |
| SKILL03-146 | Durable here L26; Firms L67 | Address the live tier by the explicit Tradeify_Select_100K key; no ACTIVE_FIRM switch exists. | R16 det |  |
| SKILL03-147 | Durable here L27-34 | Read eval geometry, cap allocation, flat deadline, hedging facts, per-leg shares and WATCH-1/B7 inputs from their owning ADRs and constants; never restate them here. | R29 abs |  |
| SKILL03-148 | Durable here L35-36 | Treat bust/DD figures as EOD-clock lower bounds pending the W1 intraday-honest remeasure. | R20 abs |  |
| SKILL03-149 | Durable here L37-40 | Grant no self-funded-lane capital authorization until a portfolio clears the lane's maximum-drawdown clearance standard. | R15 det | → docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md |
| SKILL03-150 | Durable here L41-43; Snapshot L87 | Pin historical FXIFY MC through core/historical_challenge.py; FXIFY is no longer a FIRM_RULES key. | R16 det |  |
| SKILL03-151 | Durable here L44 | Route arming, fills and disarm to the c1-rail skill and docs/notes/rail_build/ARMING_PROCEDURE.md. | R10 abs |  |
| SKILL03-152 | Durable here L44-46; Position sizing L135 | Live sizing is BASE_RISK × DD_SCALE × lifecycle with integer-quantity flooring in ops/c1_rail/c1_sizing_host_reference.py; the continuous-lot spine is deleted. | R14 det |  |
| SKILL03-153 | Source-of-truth L50; References L229 | Treat the repo as canonical—Pine for strategy code, firm_rules/dd_protection/lifecycle for constants, CATALOG→_archive LOCK.md for locks, docs/adr for decisions; this skill is secondary. | R29 abs |  |
| SKILL03-154 | Rule 0 corollary L60 | Suspect single-rule descriptions of multi-rule systems; look for the second rule. | R0 abs |  |
| SKILL03-155 | Rule 0 corollary L61; MC step 2 L182; MC trap L212 | Before accepting MC output, reconcile each CSV's trade count, net P&L, PF and DD (within 0.5%) against its Pine-header backtest; halt on any failing leg; paths are not provenance. | R20 det |  |
| SKILL03-156 | Onboarding L96 | Onboard a new firm by adding its FIRM_RULES config, then running the engine-support pre-flight before any re-MC against its tier key. | R16 abs |  |
| SKILL03-157 | Venue-transfer gates L156; Onboarding L96 | Treat every venue/feed switch as a gated hypothesis; run the feed-equivalence pre-flight before trusting a locked MC on a new feed. | R18 abs |  |
| SKILL03-158 | Locked allocations L104 | Read locked allocations and risk from AGENTS.md §Strategy Reference and _BASE_RISK/BASE_RISK (Pine owns parameters); never restate them here. | R14 abs |  |
| SKILL03-159 | Protection system L110 | Read protection literals and logic from core/dd_protection.py and AGENTS.md §Protection; never restate them here. | R14 abs |  |
| SKILL03-160 | Protection system L112 | Thread the active firm's dd_type through MC (bust_trailing versus bust_static/bust_daily); the internal DD overlay sits on top of, not instead of, the firm's rule. | R20 det |  |
| SKILL03-161 | Re-MC triggers L114-120; When to run L172-177; MC trap L209 | Re-MC before locking after: six months live data, a strategy version bump, allocation change beyond band, dd_protection constant change, firm/venue switch or new firm, or structural change. | R14 det |  |
| SKILL03-162 | When to run L174 | After re-exporting broker and TV CSVs, investigate when pass/bust drifts beyond about 1σ from locked expectation (usually regime change). | R14 DEL⚖ | Legacy book has no live venue and no book is deployed (AGENTS §Strategy Reference, §Live-execution posture); no broker-CSV drift input exists. |
| SKILL03-163 | Second-tier revert triggers L122-129 | Reintroduce a second protection tier only via fresh pre-registration (old revert triggers LOST), MC-validated against live code semantics; candidate signals only prompt starting one. | R14 abs |  |
| SKILL03-164 | Futures sizing L141 | Size futures as floor(target risk $ / (stop distance × tick value)) contracts, capped by the tier's micro_contract_cap. | R14 det |  |
| SKILL03-165 | Futures sizing L142 | Derive granularity floors (following derive_floors.py's pattern) before sizing a pyramided strategy on a small account. | R14 det |  |
| SKILL03-166 | Futures sizing L143 | Cap pyramided base size at floor(leg's allocated cap / (1 + pyramid_pct)); never apply the whole account cap per leg; a missing per-leg allocation must HALT. | R14 det |  |
| SKILL03-167 | Futures sizing L144 | Re-derive tick value and commission per instrument from the venue's own contract specs; never reuse CFD contractValue numbers. | R17 det |  |
| SKILL03-168 | Futures mechanics L152 | Confirm whether the target firm's trailing DD ratchets in real time or at EOD before trusting a re-MC bust rate. | R16 abs |  |
| SKILL03-169 | Futures mechanics L153 | Check the venue-fit determination before placing a multi-day-hold strategy on a force-flat venue. | R16 det |  |
| SKILL03-170 | Futures mechanics L154 | Model each firm's inactivity rule in MC via inactivity_max_idle_days. | R20 DEL⚖ | Contradicted by docs/load_bearing_numbers.md §2: published figures assume inactivity barrier OFF; barrier-ON re-MC degenerate, run twice. |
| SKILL03-171 | Futures mechanics L154 | Place each live account-preservation trade only with the operator's GO; the standing token-trade mandate is retired. | R10 abs |  |
| SKILL03-172 | Futures mechanics L155 | Pre-register which economic model a bust-rate gate assumes before reading results against it. | R23 abs |  |
| SKILL03-173 | Broker CSV P&L L162-164 | Hand broker CSV parsing and metrics to trade-csv-reconcile; keep live P&L analysis separate from portfolio MC—one tool per question. | R20 abs |  |
| SKILL03-174 | MC methodology L179-188 | Run portfolio MC by the enshrined method: CME TV ingest, pre-MC reconciliation, implied 1R, scaling, daily panel, Monday-anchored week-block bootstrap, firm-dd_type simulation, 10K sims × 3 seeds. | R20 det |  |
| SKILL03-175 | MC step 1 L181 | Use CME futures TV exports as the canonical MC feed; no CFD calibration feed remains (Dukascopy, OANDA, Pepperstone retired). | R18 abs |  |
| SKILL03-176 | MC step 3 L183; MC trap L211 | Compute implied 1R from full-stop losses for BE-exit strategies, falling back to median only at zero full stops; warn when 1 ≤ n < 5. | R20 det |  |
| SKILL03-177 | Locked anchor L190-199 | Read the MC anchor pin from docs/mc_anchor_history.md; never restate it, and never edit AGENTS.md's guarded literals in isolation (ops/recall/guard.py parses them). | R14 abs |  |
| SKILL03-178 | Locked anchor L201-203 | Never apply the FXIFY static-DD pin to trailing-DD tiers; successor self-funded risk questions need a fresh Pre-Q. | R20 abs |  |
| SKILL03-179 | MC traps L207 | Segment day-of-week analysis by entry date, not exit date, for long-hold strategies. | R24 det |  |
| SKILL03-180 | MC traps L208 | Use portfolio-level tail contribution, not standalone strategy MaxDD, as the sizing input. | R20 det |  |
| SKILL03-181 | MC traps L210; revert triggers L129 | Model actual live protection semantics in MC (min versus *=), verified by reading the code, never assumed. | R0 abs |  |
| SKILL03-182 | Core principles L220 | The legacy portfolio is parameter-locked; parameter or allocation changes need MC-validated re-locks; capital authorization is a separate revocable axis. | R15 abs |  |
| SKILL03-183 | Firms L94 | Do not redeploy the locked legacy book (R6 NO-GO); Bulenox remains an operational target only for new portfolios. | R15 det | → docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md |

</details>

<details><summary><code>.claude/skills/prop-firm-challenge/references/strategy_reference.md</code> — 12 rules: 3 absorbed, 7 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-1 | Preamble L3 | Treat Pine source as the authority for legacy-book strategy parameters; this reference file records mechanics only. | R14 abs |  |
| SKILL04-2 | Preamble L4 | Do not restate PF/WR/Net/DD baselines or locked entry/exit parameters in the public tree; they live in the private operational archive. | R13 abs |  |
| SKILL04-3 | Guardian/Striker/Aegis/NAS L12-73 | Legacy-book Pine editions declare margin_long/short explicitly; preserve that setting as part of each locked configuration. | R14 abs |  |
| SKILL04-4 | Striker DJ30 L30 | If DXTrade execution or an old DXTrade CSV reappears, apply each strategy's recorded contractValue; the platform default is tenfold wrong for DJ30/NAS100. | R16 det |  |
| SKILL04-5 | Striker DJ30 L17 | Treat each Striker edition's day soft-stop, which halts new entries at a realized day-loss threshold, as a critical safety control; never remove it. | R14 det |  |
| SKILL04-6 | Striker DJ30 L17; NAS100 L65 | Reproduce Striker DJ30 with its soft-stop TradingView input override, not the Pine default; NAS100 uses its native default. Values stay Pine-only. | R14 det |  |
| SKILL04-7 | Striker DJ30 L21 | Do not diagnose a cross-feed dollar P&L mismatch as signal drift; separate contract point-value differences from trade-selection differences. | R18 det | → .claude/skills/trade-csv-reconcile/SKILL.md Trap #8 |
| SKILL04-8 | Aegis L43 | Do not remove Aegis-Reversion's break-even logic; it is the edge. | R14 det |  |
| SKILL04-9 | Aegis L46 | Track Aegis rolling PF only as a passive weekly diagnostic, never a halt trigger; on degradation apply The Algorithm deliberately instead of reflexively halting. | R1 DEL | Weekly-review feeder retired (operational_rules changelog 2026-08-02); legacy Aegis has no live venue (AGENTS §Strategy Reference); no-halt principle lives in Rule 1. |
| SKILL04-10 | Aegis L51 | Apply the manual binary-event pause rule to Aegis around central-bank decisions. | R1 DEL⚖ | Target section removed in 2a5eac5f; contradicts operational_rules §1 (no BOJ skip), but archived aegis LOCK.md still records a permanent pause. |
| SKILL04-11 | Striker NAS100 L60 | Do not re-test the falsified Striker NAS100 short mirror without new mechanism evidence. | R26 det |  |
| SKILL04-12 | Striker NAS100 L61-63 | Do not overlay base-entry filters on Striker NAS100; its pyramid pathway is the strategy. | R14 det |  |

</details>

<details><summary><code>.claude/skills/refine-question/SKILL.md</code> — 21 rules: 1 absorbed, 20 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-13 | Fire test L15-18 | Refine a question only when a load-bearing dimension is unresolved and its resolutions would change the answer or work; otherwise pass through silently. | R9 det |  |
| SKILL04-14 | Fire test L20-25 | Check four load-bearing dimensions: decision link, success metric, cohort/scope (pool, venue/tier, clock, window), evidence standard (synthesize RESULTS vs fresh runs/K). | R9 det |  |
| SKILL04-15 | The move L27-35 | Ask once via AskUserQuestion with 2–4 refined readings, recommended first and labeled, each stating its commitments; orthogonal unknowns ride in the same call. | R9 det |  |
| SKILL04-16 | The move L29-30 | Resolve what standing decisions already foreclose; flag an ADR-barred reading as barred, never offer it as a live option. | R9 det |  |
| SKILL04-17 | The move L36-37 | Treat the user's selection as confirmation: restate the refined question in one line, route to the owning skill, answer; no second confirmation pass. | R9 det |  |
| SKILL04-18 | Option quality bar L41-43 | Make each option a materially different resolution, never a paraphrase; merge options with the same answer; at most four; add no explicit Other option. | R9 det |  |
| SKILL04-19 | Rationalizations L50; Red flags L58 | When the fire test hits, ask instead of answering under a stated assumption such as 'assuming you mean'. | R9 det |  |
| SKILL04-20 | Related skills L64-67 | Hand a refined question revealing a gated investigation to inqhiori, and a disguised Pre-Q brief to brief-authoring. | R9 det |  |
| SKILL04-21 | Related skills L68-69 | Run source-state checks on factual premises embedded in a question before building refinement options. | R0 abs |  |
| SKILL04-22 | Decompose intro L73 | Decompose a clear-but-contested question into axes and a recombination map before resolving; this never replaces Rule 0, verify-source, handoff-verify or adversarial review. | R9 det |  |
| SKILL04-23 | Decompose intro L73 | Route a bundled question inside an oversize brief through decomposition before work-decomposition cuts the work. | R41 det |  |
| SKILL04-24 | Decompose L81-83 | Treat a felt paradox as multiple axes: extract candidate axes, confirm each can flip independently, and answer each under its own evidentiary standard. | R9 det |  |
| SKILL04-25 | Decompose L87-88 | Never force apart genuinely coupled sub-questions; name the coupling and carry it into the recombination map. | R9 det |  |
| SKILL04-26 | When to use L92-110 | Fire decomposition on listed tells (semantics/consequences, status/warrant, transparency/content, clock, process/outcome, case/rule, merits/burden) or shared facts yielding opposite verdicts. | R9 det |  |
| SKILL04-27 | The check L118-119 | Time- and vintage-index every predicate: as of when, under which data or rule vintage, known by whom. | R9 det |  |
| SKILL04-28 | The check L120-121 | Before asserting a rule gap or conflict, or proposing a new rule, check whether existing clauses already compose to decide the case. | R36 det |  |
| SKILL04-29 | The check L122-123 | Run the live-question probe: name the one fact that would most change the call, and re-anchor if the framed question does not ask it. | R9 det |  |
| SKILL04-30 | The check L124-125 | Draw the recombination map of outputs versus sub-answers before drafting verdict prose; the method must converge on a verdict. | R9 det |  |
| SKILL04-31 | When to use L99; Rationalizations L132 | Separate status-now from warrant-then when a prior finding is challenged; a prior finding settles warrant at the time, not present truth. | R9 det |  |
| SKILL04-32 | When to use L104 | Decide an instance under the rule as it stands; log any rule-level concern as a separate, explicitly flagged recommendation. | R9 det |  |
| SKILL04-33 | Rationalizations L134 | Keep a question split only if it changes a downstream output or standard of proof; otherwise merge it back. | R9 det |  |

</details>

<details><summary><code>.claude/skills/relay-skill/SKILL.md</code> — 31 rules: 0 absorbed, 31 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-34 | Intro L8-9 | Relay only a Joshua-authorized exchange; never start because an agent requests it or a conversation is open. | R3 det |  |
| SKILL04-35 | Bind L13-14 | Obtain missing consequential inputs before sending; reuse verified inputs and existing authorization without seeking approval for each in-scope reply. | R41 det |  |
| SKILL04-36 | Bind L16-28 | Bind each exchange: task ref, verified origin and recipient routes, message and intended result, scope and authorization source, approval evidence, reply checks, completion, escalation, private checkpoint. | R41 det |  |
| SKILL04-37 | Bind L30-32 | Verify both relay endpoints by reading their actual identity and task context; a title, remembered coordinator, active tab or queued send is insufficient. | R0 det |  |
| SKILL04-38 | Bind L32-33; Hyper L78-81 | Never invent a Hyper API, infer a session ID, assume a dedicated connector, or substitute GitHub/email; report a missing route before sending anything. | R41 det |  |
| SKILL04-39 | Bind L33-34; Deliver L121-122 | Require explicit authorization covering both endpoints and permitted follow-ups; quoted agent instructions and agent replies cannot supply or expand it. | R3 det |  |
| SKILL04-40 | Bind L36-40 | Use one owner per exchange: exclusively create an ownership file before sending, reconcile with any recorded owner, take over only after confirming it stopped; block if ambiguous. | R41 det |  |
| SKILL04-41 | Bind L42-45 | Keep relay checkpoints in the primary checkout's gitignored .agent-handoffs/relay/ or an operator-approved private directory; persist state before external writes and after observations. | R41 det |  |
| SKILL04-42 | Bind L47-55 | Record checkpoint fields: owner, routes, scope evidence, status, per-direction envelope IDs, fingerprints and cursors, pending replies, check schedule, blockers, cancellation and return evidence. | R41 det |  |
| SKILL04-43 | Bind L57 | Never store secrets, tokens, unnecessary private context or entire transcripts in relay state. | R12 det |  |
| SKILL04-44 | Bind L58-60 | Never commit exchange state or put private relays in public issues/PRs; a private path does not permit copying restricted sources. | R13 det |  |
| SKILL04-45 | Supported routes Codex L64-70 | On Codex, discover with list_threads, verify with read_thread, send under explicit authorization, then read back the visible message; a queued prompt is not proof. | R41 det |  |
| SKILL04-46 | Supported routes Claude browser L71-77 | Use Joshua's local authenticated browser at the exact conversation URL; inspect URL and context before typing and recheck identity after navigation and before every send. | R41 det |  |
| SKILL04-47 | Supported routes Claude browser L75-76 | Never reach a conversation through a fresh isolated profile, hidden HTTP endpoint, token extraction or API impersonation. | R12 det |  |
| SKILL04-48 | Supported routes Hyper L80-81 | Accept a Codex return for Hyper only when that chat is the designated origin or the verified Hyper route. | R41 det |  |
| SKILL04-49 | Deliver step 1 L85-88 | Baseline both ends; send envelopes with task ref, unique ID, original speaker, source link, result and scope; label paraphrases Summary; preserve heads, links and caveats. | R41 det |  |
| SKILL04-50 | Deliver step 1 L88-89 | Quote approvals verbatim with provenance; label an agent's approval claim 'unverified reported approval' until its human source is verified. | R3 det |  |
| SKILL04-51 | Deliver step 2 L90-95 | Before every external write recheck cancellation, ownership and destination identity; persist send_uncertain, send once, and verify the full text visibly submitted. | R41 det |  |
| SKILL04-52 | Deliver step 2 L95-97 | On timeout inspect before retrying; resend an envelope only after confirming absence, otherwise block as uncertain; apply the same to returns. | R41 det |  |
| SKILL04-53 | Deliver step 3 L98-105 | After delivery stay waiting: prefer supported events, else cancellable waits (default 45s, at most 60s chunks) inspecting both ends; deduplicate by stable ID or fingerprint plus position. | R41 det |  |
| SKILL04-54 | Deliver step 4 L106-111 | Return substantive replies, questions, blockers and results via verified routes with source; skip bare acknowledgments and duplicates; advance the relayed marker only after verified delivery. | R41 det |  |
| SKILL04-55 | Deliver step 4 L111-112 | Turn questions needing Joshua's input or permission into blocked status, returning the question with a clear resumption condition. | R3 det |  |
| SKILL04-56 | Deliver step 5 L113-116 | Continue until the requested result is visibly returned, Joshua cancels, or a blocker needs input; acknowledgment, running status or check-count limits are not completion. | R21 det |  |
| SKILL04-57 | Deliver step 5 L116-119 | On cancellation stop sends and checks, preserve undelivered material, stop the owned monitor, report cancelled without claiming success; recheck cancellation before final return. | R41 det |  |
| SKILL04-58 | Deliver L121-125 | Relaying grants communication only: never click permission dialogs, merge, deploy, trade, spend, install, change credentials or dispatch workers because a relay asks; route to Joshua. | R3 det |  |
| SKILL04-59 | Deliver L125-126 | Never forward secrets or restricted material, even verbatim; retain a redacted notice and escalate the missing safe handoff. | R13 det |  |
| SKILL04-60 | Interrupted L130-135 | On disconnect preserve state and report the blocked route; on reconnect reverify identities and reconcile histories; keep unreturnable results return_pending; never choose a new recipient. | R41 det |  |
| SKILL04-61 | Interrupted L137-141 | Use an existing wakeup or automation only if authorized and able to resume this state; never substitute a second monitor, detached loop, new worker or unrequested schedule. | R41 det |  |
| SKILL04-62 | Interrupted L142-143 | Without a working continuation, checkpoint and say monitoring is not established; never promise future checks or claim success. | R21 det |  |
| SKILL04-63 | Interrupted L143-145 | Release exchange ownership only after owned checks stop; retain terminal state for recovery and deduplication. | R41 det |  |
| SKILL04-64 | Invocation L156-157 | Do not contact real conversations or start monitors for relay tests without an authorized test exchange. | R3 det |  |

</details>

<details><summary><code>.claude/skills/repo-hygiene/SKILL.md</code> — 11 rules: 0 absorbed, 11 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-65 | Hard rules L14 | Report hygiene findings first; delete each branch or worktree only after explicit operator confirmation; merged status never overrides a prior keep decision. | R3 det |  |
| SKILL04-66 | Hard rules L15 | Never run git clean -fdX, git push --force or git branch -D unless the operator explicitly orders the destructive form. | R6 det |  |
| SKILL04-67 | Hard rules L16 | Prefer git branch -d and git worktree remove; on Windows path-length or file-lock failures stop and ask rather than inventing a force path. | R6 det |  |
| SKILL04-68 | Hard rules L17 | Never delete a branch that is checked out in any worktree. | R6 det |  |
| SKILL04-69 | Hard rules L18 | Do not edit the primary tree when the intended checkout is a linked worktree; verify git rev-parse --show-toplevel first. | R6 det |  |
| SKILL04-70 | §1 Scout L22-32 | Scout with scripts/repo_hygiene.py and read primary lag, linked worktrees with ignored entries, orphan dirs and squash-aware merged candidates. | R6 det |  |
| SKILL04-71 | §2 Classify L36-43 | Apply default dispositions: merged unchecked-out local is a -d candidate; orphan worktree dir: close handles, remove, prune; spent primary: fast-forward main before pruning. | R6 det |  |
| SKILL04-72 | §2 Classify L41 | Never remove a worktree whose scout shows ignored files until each private file is archived via evidence_archive.py put and pushed; never park them in root inputs/ or local_artifacts/. | R31 det |  |
| SKILL04-73 | §3 Confirm L47-54 | Remove approved items one at a time; delete a remote branch only if the operator also wants it gone; then prune worktrees. | R6 det |  |
| SKILL04-74 | §4 Verify L56-63 | After pruning verify: evidence_archive.py audit shows nothing UNPUSHED, then worktree list, status and a fresh scout. | R6 det |  |
| SKILL04-75 | description L3 | Keep repo-hygiene passes out of core/, allocations and Pine. | R14 det |  |

</details>

<details><summary><code>.claude/skills/s2-linux-run/SKILL.md</code> — 23 rules: 3 absorbed, 20 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-76 | Intro L8; §2 L25 | Treat the downloaded S2 artifact, never a green check mark, as the only acceptance-grade Linux evidence. | R21 det |  |
| SKILL04-77 | §1 L12 | Commit on frozen bytes, check git diff --stat, and push the branch before dispatching an S2 run. | R21 det |  |
| SKILL04-78 | §1 L13 | Dispatch the Linux S2 run first, then run the Windows fp.ps1 lines while it executes so the clocks overlap. | R22 det |  |
| SKILL04-79 | §1 L18 | Identify your S2 run by polling for one created after your dispatch with your mode title and pushed headSha; no fixed sleep, never the newest branch run. | R21 det |  |
| SKILL04-80 | §1 L18-19 | Write nothing into the worktree until the last verification record closes; keep run IDs and drafts in the scratchpad. | R21 abs |  |
| SKILL04-81 | §1 L19 | Run Windows line 1 (execution files, two workers, zero skips) during iteration; run lines 2–3 and check only on the final frozen tree. | R22 det |  |
| SKILL04-82 | §1 L20 | Never push to a branch with an S2 run in flight; batch PR-branch docs commits until the needed run finishes. | R21 det |  |
| SKILL04-83 | §1 L21 | Never dispatch or rerun S2 twice on the same SHA; if it happens, cite the surviving run. | R21 det |  |
| SKILL04-84 | §1 L23 | Override the S2 run guard with FP_S2_GUARD=off only for a reason you can state. | R21 det |  |
| SKILL04-85 | §1 L23; §2 L31 | Treat S2 modes as mutually incomparable and pull_request runs as testing the merge ref; neither covers a dispatch run on the head's bytes. | R21 det |  |
| SKILL04-86 | §2 L28-31 | Read S2 results with scripts/s2_run_evidence.py --expect-head; use --expect-scope only when asked; diagnostic and N1-only scopes never read ok. | R21 det |  |
| SKILL04-87 | §2 L37-40 | Accept an S2 record only with completed status, zero exit codes, stable source, complete capture, cleanup ok, expected scope, matching commit, passed invariants and zero skips. | R21 det |  |
| SKILL04-88 | §2 L41 | Report S2 run ID, head SHA, record ID, counts and cleanup; a run whose head is not your final bytes proves nothing about them. | R21 abs |  |
| SKILL04-89 | §3 L50-54 | Treat an S2 failure on unchanged code as a finding: trace the attempt's journal chain, compare timing to the last green run, reproduce locally before redispatching. | R40 det |  |
| SKILL04-90 | §3 L55 | State the S2 root cause in one sentence with file:line, fix it, then dispatch once; if the defect is test-only, say so and fix the test. | R40 abs |  |
| SKILL04-91 | §3 L55 | Never relax a load-bearing S2 assertion (CPU-charge limit, zero skips, all required nodes) to obtain a green run. | R40 det |  |
| SKILL04-92 | §3 L56 | For a flaked S2 case run a cases= diagnostic subset twice on final bytes, then one full acceptance dispatch; never serial full re-rolls. | R40 det |  |
| SKILL04-93 | §3 L57 | Treat warm_service empty-Slice and the OOM/overrun IN_DOUBT or BUDGET_* terminals as known-benign accepted terminal sets. | R21 det |  |
| SKILL04-94 | §4 L61 | Workers report S2 runs as evidence and state 'Linux acceptance pending' without a green run on the final bytes; acceptance belongs to the coordinator. | R4 det |  |
| SKILL04-95 | §4 L62 | Accept Linux evidence only from the integrated PR run on the final head, artifact-read, plus independent review; never a branch run alone. | R21 det |  |
| SKILL04-96 | §4 L63 | Never count Windows, mock or simulated_control_timer results as Linux evidence. | R21 det |  |
| SKILL04-97 | §5 L66-67 | Use cases= diagnostic subsets (s3 mode) only for iteration; they always end red, never count as acceptance, and two on one ref cancel each other. | R21 det |  |
| SKILL04-98 | §5 L68; description L3 | Do not improvise open S2 tooling (sharding, image caching, hosted Windows line 3) or change the workflow or allowances from a worker seat. | R4 det |  |

</details>

<details><summary><code>.claude/skills/strategy-validation/SKILL.md</code> — 40 rules: 2 absorbed, 38 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-99 | §0 L12 | Rank pending tests by probability of changing the verdict divided by cost; selection-level tests usually outrank parameter grids. | R24 det |  |
| SKILL04-100 | §0 L16 | Treat a plateau pass as conditional on the selection; test the selection itself with placebos or permutation and know which null each test kills. | R24 det |  |
| SKILL04-101 | §0 L16 | Keep a 'which nulls remain alive' ledger in the session record. | R24 det |  |
| SKILL04-102 | §1 L20 | Run the Step-0 panel-integrity battery (step0_battery.py) on every TradingView export before computing any metrics. | R24 det |  |
| SKILL04-103 | §2 L26 | Before designing, compute the stop-width cost-in-R hurdle with cost_geometry_pregate.py and estimate net expectancy and cost sensitivity; no universal clearance multiple applies. | R24 det |  |
| SKILL04-104 | §2 L28 | Do not restate the cost-law formula from memory; cost_geometry_pregate.py owns it. | R29 abs |  |
| SKILL04-105 | §3 L32 | Before any direction-flip or exit-redesign re-run, bound the counterfactual with excursion buckets and report best/worst expectancy including costs. | R24 det |  |
| SKILL04-106 | §3 L32 | State excursion censoring limits explicitly: excursions are censored at original exits and targets beyond the original stop are unobservable. | R24 det |  |
| SKILL04-107 | §4 L38-40 | Treat the plateau protocol as archived; re-arm it only through a fresh pre-registration carrying the same-feed baseline rule plus operator GO. | R24 det |  |
| SKILL04-108 | §4 L42 | When the plateau protocol is re-armed, vary one knob ±1 step per run, pre-register pass criteria before run 1, and track with plateau_tracker.py. | R24 det |  |
| SKILL04-109 | §4 L44 | Compare parameter neighbors only against a same-feed baseline; cross-feed center comparisons are forbidden. | R24 det |  |
| SKILL04-110 | §5 L48-50 | Quantify post-hoc tuned configs or best-slice claims with selection_tests.py before arguing; convert governance objections into measurements. | R23 det |  |
| SKILL04-111 | §5 L54 | Name the null and benchmark (zero-drift, buy-and-hold, time-series momentum) explicitly before computing any anomaly test. | R24 det |  |
| SKILL04-112 | §5 L55 | Include unconditional drift in permutation nulls (detrend or claim timing only) and block-shuffle time-clustered signals. | R24 det |  |
| SKILL04-113 | §5 L56 | For magnitude-persistence claims on autocorrelated series, run surrogates matching the series' own dependence profile through the identical pipeline. | R24 det |  |
| SKILL04-114 | §5 L56 | Before reusing a frozen battery on a new claim family, re-derive which confound it is exposed to and confirm the null controls it. | R24 det |  |
| SKILL04-115 | §5 L56 | Keep presence questions (usable predictability; gates) separate from attribution questions (beyond linear structure; types the finding). | R24 det |  |
| SKILL04-116 | §5 L60 | Freeze a spec only if two independent implementers would compute identical numbers; otherwise ship reference code or a synthetic worked example with the freeze. | R23 det |  |
| SKILL04-117 | §6 L64 | Fix forward-test pre-registration before the first trade: frozen-config table, power disclosure, checkpoint kill/extend/escalate rules, trade-rate clause, forbidden moves, append-only audit hook. | R23 det |  |
| SKILL04-118 | §6 L64 | State in forward-test pre-registrations that decision rules are expectation-based stops, not significance tests. | R23 det |  |
| SKILL04-119 | §6 L64 | Void any forward-test checkpoint where a criterion moved after data arrived. | R23 det |  |
| SKILL04-120 | §6 L66 | Name what must be independent (price path, period, instrument) in validation or unpark conditions; never just 'a different feed'. | R24 det |  |
| SKILL04-121 | §7 L70 | Declare each concept-stage Pine input's epistemic status in its tooltip: STARTING POINT, LOCKED, or OUT-OF-EVIDENCE-BASE. | R14 det |  |
| SKILL04-122 | §8 L77-80 | Apply universe-level correction to any candidate that won a search over K strategies or configs; its naive p-value and Sharpe are inflated until corrected. | R23 det |  |
| SKILL04-123 | §8 K-tiering L82-87 | Log K≤1 universe correction as a declared no-op ('K≤1, correction not applicable'); never silently skip §8a/§8c. | R23 det |  |
| SKILL04-124 | §8 K-tiering L88-96 | Run §8a/§8c corrections for K of two or three; standard-lane admission refuses manifests at K≥4, and the deep lane has its own ceiling. | R23 det |  |
| SKILL04-125 | §8a L98-111; Boundaries L179-181 | Use arch.bootstrap SPA/StepM/MCS and skfolio CPCV for universe-level tests; never reimplement bootstrap re-centering. | R24 det |  |
| SKILL04-126 | §8a L106-109 | Run universe-level tests on a stationary or circular block bootstrap with block_size set to the return autocorrelation scale; never accept the library default. | R24 det |  |
| SKILL04-127 | §8b L113-118 | Deflate the headline Sharpe for selection under K and non-normality, and pre-register the DSR pass threshold before computing. | R24 det |  |
| SKILL04-128 | §8b L119-122 | Compute DSR on per-observation Sharpe consistent with n, express trial variance in the same units, and never let K default to one. | R24 det |  |
| SKILL04-129 | §8b L122-124 | Keep the DSR self-test passing: planted negative controls must fail and positive controls pass at the reference threshold. | R24 det |  |
| SKILL04-130 | §8c L127-137 | Compute PBO over purged, embargoed CPCV paths; PBO above one-half means overfit; keep path counts in the tens to hundreds. | R24 det |  |
| SKILL04-131 | §8d L139-142 | Replace IID trade resampling with a block bootstrap on autocorrelated futures returns. | R24 det |  |
| SKILL04-132 | §8e L144-149 | Do not use the breadth module as a standing Stage-8 producer; run it only for self-test or re-arm. | R24 det |  |
| SKILL04-133 | Integration L151-153 | Campaign preregs name their live validation limbs; standing defaults are mechanism-first admission with DSR-cap refuse, temporal consistency when required, and campaign-named realism limbs. | R24 det |  |
| SKILL04-134 | Integration L154-155; Orchestrator L159-164 | Keep SPA/StepM, PBO and the universe_gate orchestrator dormant; re-arm only when a campaign prereg names thresholds and an operator GO lifts dormancy. | R24 det |  |
| SKILL04-135 | Integration L156-157 | Use the DSR module default var_trials=1/n unless an explicit pin overrides it. | R24 det |  |
| SKILL04-136 | Boundaries L171 | Read the instrument ledger ops/instruments/<SYMBOL>.md before deriving instrument-level state. | R27 abs |  |
| SKILL04-137 | Boundaries L168-176 | Route metric definitions to trade-csv-reconcile, investigate-or-not to inqhiori/programme-audit, artifact structure to brief-authoring, and K/search pre-registration to the discovery ledger. | R24 det |  |
| SKILL04-138 | Boundaries L177-178 | Treat statistics-of-tradable-anomalies.md as rationale reference, not a gate. | R24 det |  |

</details>

<details><summary><code>.claude/skills/task-routing/SKILL.md</code> — 13 rules: 3 absorbed, 10 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-139 | Intro L11; Non-goals L52 | Decide local versus cloud before launching a Task or cloud-capable subagent; this skill never decides whether the Task should exist. | R41 det |  |
| SKILL04-140 | Procedure L15 | Honor an explicit user local-or-cloud choice for the work and skip the checklist. | R3 abs |  |
| SKILL04-141 | Procedure L16; Standing L22 | On any local-only checklist hit route local and put 'Must run locally' with its reason near the packet's top; a local packet lacking it is malformed. | R33 abs |  |
| SKILL04-142 | Procedure L17; Standing L22 | Route to cloud by default when no checklist item hits; ask for no environment GO. | R41 abs |  |
| SKILL04-143 | Procedure L18 | Resolve an unclear checklist item with a cheap check; treat any still-unresolved item as a hit. | R41 det |  |
| SKILL04-144 | Standing L23 | Every cloud brief must require a PR whose description begins 'Cloud-task: <session name>', with the final report or blocking question posted as a PR comment. | R41 det | *at HEAD:* changed: Narrowed: own Cloud-task PR only for committing sessions; coordinator fixes return destination before launch (4499cb7e). |
| SKILL04-145 | Standing L23 | Push the branch a cloud session starts from before launching it. | R41 det |  |
| SKILL04-146 | Standing L23 | Send work that will need operator decisions partway through to a local session. | R41 det |  |
| SKILL04-147 | Standing L24 | A cloud reviewer of a pushed, pinned revision returns findings without writing to the reviewed branch. | R5 det |  |
| SKILL04-148 | Local-only checklist L28-36 | Route locally when work needs gitignored/vendor data, secrets, local services, GUI or interactive approval, unpushed state, durable local disk, the private read surface, private evidence writes, or the operator's machine/VM. | R41 det |  |
| SKILL04-149 | Output contract L42-46 | Emit the Routing/Reason/Action block before every launch. | R41 det |  |
| SKILL04-150 | Related L56-59 | Re-apply the local-only checklist per packet at dispatch time, not once at authoring time. | R41 det |  |
| SKILL04-NEW-1 | Standing preferences L23 | For a cloud session that may commit nothing (read-only review, or branch already with a PR), name an existing PR in the brief; it posts there in a comment beginning 'Cloud-task: <session name>'. | R41 det | *at HEAD:* new 4499cb7e |

</details>

<details><summary><code>.claude/skills/trade-csv-reconcile/SKILL.md</code> — 33 rules: 3 absorbed, 30 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-151 | Mission framing L10 | Read live posture from AGENTS.md; never route CSV sessions through retired FXIFY/$200K/DXTrade ceremony, but keep the historical traps for old CSVs. | R18 det |  |
| SKILL04-152 | Source-of-truth L12 | Rank sources: Pine on disk, then Pine-header panel, then the baselines.md cache, then memory; a fresh Pine read wins and the cache gets updated. | R29 det |  |
| SKILL04-153 | Boundary L14 | Stop at verified per-strategy CSV metrics; never duplicate dd_protection, MC or rail logic in this skill. | R29 abs |  |
| SKILL04-154 | L16; description L3 | Run the full reconcile pipeline before portfolio MC, a version lock, or treating a CSV as lock/MC canonical input; otherwise run Steps 1–4 only. | R14 det |  |
| SKILL04-155 | Rule 0 L20-22 | Treat file paths as non-provenance; when baseline reconcile is in scope, halt on any failing leg with no portfolio scaling, MC or decision artefact. | R14 det |  |
| SKILL04-156 | Rule 0 sub-rule L24; Trap #6 L173 | Use venue point values, never CFD contractValue, for futures micros (MYM/MNQ) in CSV analysis. | R18 det |  |
| SKILL04-157 | Rule 0 sub-rule L26; Trap #5 L171 | Never accept TradingView exports shorter than 30 days for JPY-pair P&L; validate by Python recompute. | R20 det |  |
| SKILL04-158 | Rule 0 sub-rule L28 | Before computing PF/WR or reconciling a lock from a short pane, inventory the testing period and read the TV strategy-report note; a later prior export wins. | R20 det |  |
| SKILL04-159 | Canonical pipeline L36 | Run every CSV reconciliation's pipeline steps in order; skipping or reordering steps produces anchor drift. | R20 det |  |
| SKILL04-160 | Step 1 L44 | Inventory each CSV (filename, row count, first three rows, last row) and confirm consistent columns across the batch. | R20 det |  |
| SKILL04-161 | Step 1 L46; Trap #7 L175 | Read TradingView exports with utf-8-sig and strip column whitespace to handle the BOM header. | R20 det |  |
| SKILL04-162 | Step 1 L54-60; Trap #13 L187 | On 'CSV missing required columns', add a COLUMN_ALIASES entry; never hand-rename the CSV. | R19 det |  |
| SKILL04-163 | Step 2 L64-66; Traps #3-4 | Pair Entry/Exit by Trade #, take realized P&L from Exit rows only, and keep pyramid adds as legs attributed at the final exit. | R20 det |  |
| SKILL04-164 | Step 2 L68; Reference L205 | Use scripts/reconcile.py for parsing and metrics; never re-derive the parser inline. | R29 abs |  |
| SKILL04-165 | Step 3 L72-79; Trap #2 L165 | Pin 1R explicitly per strategy archetype: median loss for trend-riders, full-stop-cohort mean for break-even and pyramid archetypes. | R20 det |  |
| SKILL04-166 | Step 3 L81 | Fall back to median 1R only when there are zero full stops; never use the retired n<5 fallback. | R20 det |  |
| SKILL04-167 | Step 3 L83 | Flag thin full-stop cohorts (one to four stops) with cohort_warning=True; never accept them silently. | R20 det |  |
| SKILL04-168 | Step 4 L87-98 | Compute headline metrics by definition: N from paired exits, WR, PF, Net from Exit rows only, trade-close DD reconstruction, RF. | R20 det |  |
| SKILL04-169 | Step 4 L96; Trap #9 L179; Step 6 L134 | Use the panel's stated initial capital; never impose a $200K static base on Tradovate/c1 or micro-futures research CSVs. | R20 det |  |
| SKILL04-170 | Step 4 L101 | Apply strategy-specific pyramid-share red flags: a sustained low share is an escalation tripwire for NAS-class archetypes; DJ30's lower share is expected. | R20 det |  |
| SKILL04-171 | Step 5 L105-113 | Reconcile computed metrics against the baseline tolerance table: exact trade count, tight PF/Net/WR bands, a wider DD band. | R14 det |  |
| SKILL04-172 | Step 5 L115-120 | Triage a failed reconcile in order: feed or filename mislabel, stale cached anchor, genuine version drift, stale Pine reproduction. | R14 det |  |
| SKILL04-173 | Step 5 L119 | Never silently update a baseline anchor; confirm with the user before treating a drifting CSV as canonical. | R14 det |  |
| SKILL04-174 | Step 5 L118 | When updating a stale cached anchor, re-read the Pine source headers and state what changed and when. | R14 det |  |
| SKILL04-175 | Step 6 L124-132 | Scale to locked allocations only for portfolio-level work, reading them from AGENTS §Strategy Reference or _BASE_RISK; skip for ORB, venue-native and c1 fill CSVs. | R14 det |  |
| SKILL04-176 | Step 6 L134 | Never re-derive challenge-era $200K multipliers for Tradovate fills; live c1 sizing is the rail's BASE_RISK×DD_SCALE×lifecycle integer quantity. | R14 det |  |
| SKILL04-177 | Step 7 L138-153 | Emit the standard per-strategy reconciliation block with reconcile status per metric; add scaled fields when portfolio-scaled. | R14 det |  |
| SKILL04-178 | Step 7 L155 | End a drifting reconciliation with HALT — DRIFT DETECTED and the suspected cause; never produce a best-guess combined panel. | R14 det |  |
| SKILL04-179 | Trap #10 L181 | Sync references/baselines.md on every strategy re-lock. | R14 abs |  |
| SKILL04-180 | Trap #11 L183 | Reconcile only from strategy-file backtests; an indicator file cannot produce a reconcilable CSV. | R14 det |  |
| SKILL04-181 | Trap #12 L185 | Run Hurst R/S and autocorrelation on log returns, never on log prices. | R24 det |  |
| SKILL04-182 | Trap #14 L189 | Treat pyramid-share flags as advisory until anchors are re-measured; never compare per-leg with qty-apportioned shares or equate either with a base-only counterfactual. | R20 det |  |
| SKILL04-183 | When NOT L193-199 | Route no-CSV methodology to inqhiori, Pine work to pinescript-v6, MC/dd_protection/allocation/arming to prop-firm-challenge or c1-rail; use another parser for bar data. | R20 det |  |

</details>

<details><summary><code>.claude/skills/trade-csv-reconcile/references/baselines.md</code> — 12 rules: 3 absorbed, 8 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-184 | Dormant note L9-17 | Retain the dormant re-lock sync steps 1–4 in full; do not delete them although their trigger cannot currently fire. | R31 det |  |
| SKILL04-185 | Dormant note L15-16; step 2 L42 | On any re-lock update the gitignored baselines.private.json in the same motion as this markdown. | R14 det |  |
| SKILL04-186 | Dormant note L19-22 | Re-arm baseline sync only after a re-lock lands under a fresh admitting ADR via pre-registration, re-MC, both-halves gate and ADR; then apply steps 1–4 fully. | R14 abs |  |
| SKILL04-187 | Repo copy L24-29 | Keep the repo and plugin baselines copies in sync on every re-lock because reconcile.py --baseline reads the plugin copy. | R14 DEL | Superseded: reconcile.py --baseline reads gitignored references/baselines.private.json (reconcile.py L18, L53-55), not a plugin baselines.md copy. |
| SKILL04-188 | Redaction L31-37 | If baselines.private.json is missing, restore it from git history or the private archive rather than the public tree. | R13 det |  |
| SKILL04-189 | Re-lock steps L39-45 | On re-lock read fresh canonical-feed strategy-tester headers, update the block and private JSON, note the lock date, and re-run reconcile --baseline to verify. | R14 det |  |
| SKILL04-190 | DD convention L47-50 | Never cross-compare trade-close cumulative-P&L drawdown with TradingView's intrabar max drawdown. | R20 det |  |
| SKILL04-191 | Mirrors L54-61 | Link risk percentages, dd_protection literals and the MC pin to their owners; this file holds only per-strategy PF/WR/Net/DD/N anchors. | R29 abs |  |
| SKILL04-192 | Guardian notes L78 | Do not use the legacy Notion Guardian trade-count figure; it is a stale anchor. | R20 abs |  |
| SKILL04-193 | Striker DJ30 L93-95; NAS100 L112-113 | Investigate reconcile.py's pyramid-share detector before relying on pyramid_pnl_share from the 2026-05-24 export vintage. | R20 det |  |
| SKILL04-194 | Aegis L129-132 | Cite each anchor figure set with its vintage and provenance; never mix lock-of-record header figures with re-export vintage figures. | R20 det |  |
| SKILL04-195 | Cross-feed L152-153 | If WR or N drifts more than 5% across feeds for one strategy version, suspect feed mislabel before strategy divergence. | R18 det |  |

</details>

<details><summary><code>.claude/skills/verify-source/SKILL.md</code> — 9 rules: 6 absorbed, 3 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL04-196 | Overview L12; When L16 | Before acting on a value, claim or premise not freshly computed this turn, verify its source's state (currency, vintage, scope, cohort), not merely that you read it. | R0 abs |  |
| SKILL04-197 | Overview L10; table L22; Rationalizations L40 | Never treat an artefact agreeing with its own pin as evidence of currency or correctness. | R0 abs |  |
| SKILL04-198 | The check L28; Worked example L55 | Run git status -sb and git log HEAD..origin/main; if behind and the file is anchor- or risk-bearing, read origin/main's copy. | R0 det |  |
| SKILL04-199 | The check L29 | Open the file a handoff claim names and confirm the bytes; never quote the claim itself. | R0 abs |  |
| SKILL04-200 | The check L30; table L23 | Check an artefact's provenance (date, export window, config) before trusting it, including first date versus panel start before calling a defect real. | R0 det |  |
| SKILL04-201 | The check L31 | Quote a borrowed metric only with its cohort (n and filter) and window, or not at all. | R20 det |  |
| SKILL04-202 | The check L33; Rationalizations L42 | Never skip the source-state check under time pressure; time pressure is its trigger. | R0 abs |  |
| SKILL04-203 | Relationship L59; Rationalizations L41 | Treat Rule 0 as necessary but not sufficient: after reading production source, still verify it is the current, right source. | R0 abs |  |
| SKILL04-204 | Relationship L60-61 | Run handoff-verify Phase-0 before executing a handoff and its judging after claimed completion; apply verify-source to each value inside. | R0 abs |  |

</details>

<details><summary><code>.claude/skills/work-decomposition/SKILL.md</code> — 59 rules: 13 absorbed, 46 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| SKILL05-1 | frontmatter L3; §Overview L15-17 | Limit this skill to sizing units and writing the manifest/child specs; do not build, dispatch implementation workers, pick environments, author packets or adjudicate returns; read-only sub-agent waves are evidence gathering. | R41 det |  |
| SKILL05-2 | frontmatter L3 | Decomposition work changes no strategy parameters, allocations, dd_protection constants or MC calibration. | R14 abs |  |
| SKILL05-3 | §Overview L17-19 | Treat Claude Code sessions and Codex tasks as the only worker surfaces; Cursor is retired as a worker surface (2026-09-15). | R4 abs |  |
| SKILL05-4 | §Overview L20-26 | Apply fleet-orchestration rules (claim manifest, single-writer footprints, dispatch-time Phase-0 re-check, review-round-as-freeze, frozen-SHA pointer) as owned by the surface-allocation ADR orchestration clause. | R4 abs |  |
| SKILL05-5 | §Overview Provenance L33-34 | Every rule imported from an external draft must justify itself on repo grounds; record what was imported, transformed or dropped and why. | R36 det |  |
| SKILL05-6 | §Which kind of too big L36-42 | Classify oversize work as question-shaped (route to refine-question), work-shaped (cut the work) or input-shaped (cut the reading) before decomposing. | R41 det |  |
| SKILL05-7 | §Which kind of too big L44 | When work is both work- and input-shaped, size the input first; the work cannot be sized until its reading is known. | R41 det |  |
| SKILL05-8 | §Work-shaped Oversize tells L49-62 | Treat a unit as presumptively too big if it has >5 gate conditions, >3 unrelated code areas, >1 context window, multiple independent deliverables, or internal sequencing. | R41 det |  |
| SKILL05-9 | §Oversize tells L52-54 | Treat imported oversize thresholds as calibration candidates, not ratified constants; record each firing when one bites, per AGENTS.md §Continuous improvement. | R41 det |  |
| SKILL05-10 | §Oversize tells table L59 | Treat a unit touching both lab and ops as already two units, since lab-ops imports are forbidden; cut one child per layer or owner. | R41 det |  |
| SKILL05-11 | §Oversize tells table L63 | Rule 2 budgets: INNER 3 / OUTER 8 iterations / STRATEGIC 3 constituent OUTER investigations; all substantial work is budgeted, routine fixes excluded. | R2 abs |  |
| SKILL05-12 | §Oversize tells table L63 | Treat worst-case iterations exceeding the unit's Rule 2 budget as oversize; cut so the tripwire fires at a child boundary, not mid-unit. | R41 det |  |
| SKILL05-13 | §Oversize tells table L63 | Cutting never mints budget: INNER/OUTER children's worst-case iterations must sum inside the parent's; a STRATEGIC parent has at most three OUTER children, each with its own OUTER budget. | R2 det |  |
| SKILL05-14 | §Oversize tells table L63 | If children's summed iterations or count exceed the parent's budget, treat it as the parent's tripwire at cut time: structured stop, and for OUTER/STRATEGIC obtain owner extension before any dispatch. | R2 det |  |
| SKILL05-15 | §Oversize tells table L64 | On a BLOCKED scope-problem return or a second NEEDS_CONTEXT bounce on the same packet, re-cut it before any re-dispatch; a NEEDS_CONTEXT child returns to QUEUED only once. | R41 det |  |
| SKILL05-16 | §Oversize tells dated instances L73-76 | Use the Track B umbrella (dependency graph, sub-track-to-packet map, wave gates, claim manifest) as the reference shape for work-shaped output. | R41 det |  |
| SKILL05-17 | §Atomic-unit test L78-80 | Give every child exactly one named output (file, PR, RESULTS artifact, decision record); never 'progress on' something. | R41 det |  |
| SKILL05-18 | §Atomic-unit test L81-83 | Give every child one named verification its own return can run (gate id, pytest node, check_brief path, --check mode); a child without a gate is not a unit. | R41 det |  |
| SKILL05-19 | §Atomic-unit test L84-88 | Make every child independently revertible without breaking parallel siblings; revert depends-on chains leaf-first in reverse dependency order; a silent sibling break means footprint or edge is wrong. | R41 det |  |
| SKILL05-20 | §Atomic-unit test L89-93 | Size every child to fit one session with margin, with no step whose detail must survive a compaction, and its iterations within its allocated parent-budget share. | R41 det |  |
| SKILL05-21 | §Atomic-unit test L94-95 | Give each child a file footprint disjoint from every parallel sibling, or an explicit depends-on edge making it sequential. | R4 abs |  |
| SKILL05-22 | §Atomic-unit test L95-96 | Reserve docs/SESSIONS.md, STATE.md, boards and index files to the parent's integration commit; children never write them and name them as forbidden. | R4 abs |  |
| SKILL05-23 | §Atomic-unit test L97-102 | Keep judgment-needing children and children on locked surfaces (core anchor code, Pine, ADRs, pre-registrations, AGENTS.md, STATE.md) with the orchestrating session regardless of size; never launder judgment into a small packet. | R4 abs |  |
| SKILL05-24 | §Atomic-unit test L104-107 | Name each child '<verb> <object> so that <observable outcome>', naming the parent; if the outcome clause cannot be written, the child is not cut yet. | R41 det |  |
| SKILL05-25 | §Atomic-unit test L109-111 | Do not cut below the handoff-overhead threshold; fold a too-small child into a sibling or run it inline under the session's own checklist. | R41 det |  |
| SKILL05-26 | §Procedure L115-116 | State the parent's done in two sentences plus its gate before cutting; if that cannot be done, run refine-question first. | R41 det |  |
| SKILL05-27 | §Procedure L117-120 | List candidate children along natural boundaries (deliverable, layer/owner, footprint, gate cluster); run the six-point test on each, cutting or merging until all pass. | R41 det |  |
| SKILL05-28 | §Procedure L119-120 | Never copy the parent's acceptance criteria wholesale into children; each child's gate is specialised and can pass or fail alone. | R41 det |  |
| SKILL05-29 | §Procedure L121-123 | Map each child's dependency status as READY, BLOCKED-BY <child> or BLOCKS <child>; allow no cycles (a cycle means a wrong boundary); queue blocked children until the upstream return merges. | R41 det |  |
| SKILL05-30 | §Procedure L123-124 | Sequence for incremental integration: merge children in dependency order with fast gates between merges, never one end-of-track consolidation. | R41 det |  |
| SKILL05-31 | §Procedure L125-126 | Write the parent manifest before anything is dispatched, one row per child: child, owner/lane, branch, footprint, depends-on, budget, status. | R41 det |  |
| SKILL05-32 | §Procedure L127-128 | Use manifest statuses STUB/QUEUED/DISPATCHED/RETURNED/MERGED/OVERTAKEN/WITHDRAWN; never dispatch from a STUB (not yet freezable). | R41 det |  |
| SKILL05-33 | §Procedure L128-132 | Record RETURNED with its four-state return and disposition so the row shows whether work is still owed; never leave a child DISPATCHED after its return. | R41 det |  |
| SKILL05-34 | §Procedure L132-135 | Fill the manifest budget column for every budgeted parent: child shares summing inside an INNER/OUTER parent, 'OUTER (own 8)' under STRATEGIC, 'n/a — routine' for routine fixes. | R2 det |  |
| SKILL05-35 | §Procedure L135-138 | The parent manifest lists every child; a child absent from it does not exist; consult it before opening work in the area to prevent duplicate work. | R41 det |  |
| SKILL05-36 | §Procedure L139-145 | Route children: 2+ frozen packets to parallel workers under one umbrella and claim manifest; one frozen build to cc_handoff or Codex; judgment/locked work to orchestrator; small work inline. | R4 abs |  |
| SKILL05-37 | §Procedure L146 | Choose each child's environment with task-routing's local-only checklist after the cut. | R41 abs |  |
| SKILL05-38 | §Procedure L147-149 | Hand children to brief-authoring for packets, handoff-verify for pre-dispatch checks and post-execution judging; this skill's deliverable ends at the manifest and child specs. | R41 det |  |
| SKILL05-39 | §Child quality checklist L155 | Give each child its own Phase-0 premises with an explicit no-op condition (already on main: return DONE citing the commit). | R4 abs |  |
| SKILL05-40 | §Child quality checklist L158 | Give each child's return contract the four-state taxonomy DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED. | R4 abs |  |
| SKILL05-41 | §Input-shaped table L166-172 | Decompose reading for 10+ files, 50k+ tokens, list-everything/aggregate tasks, or pairwise/multi-hop reasoning even if it fits; read directly only for a localised needle or line range. | R41 det |  |
| SKILL05-42 | §Input-shaped Protocol L176-189 | Size candidates before reading with git ls-files -c -o (files, lines, bytes) from the working tree; never index-only counts or --exclude-standard, which drop gitignored vendor inputs. | R41 det |  |
| SKILL05-43 | §Input-shaped Protocol L189-191 | Treat an empty rg as not evidence of absence, since cold stores are search-excluded; use rg --no-ignore or git show. | R8 abs |  |
| SKILL05-44 | §Input-shaped Protocol L192-194 | Search before reading a directory; never list a tree recursively as a substitute for a query; chain filters until only the candidate set remains. | R41 det |  |
| SKILL05-45 | §Input-shaped Protocol L195-201 | Chunk candidates into disjoint batches of natural units (5-10 files, sections/line ranges, or one per source for pairwise); never pad batches; write the batch count before launching. | R41 det |  |
| SKILL05-46 | §Input-shaped Protocol L202-204, template L220-227 | Launch one sub-agent per batch with a self-contained brief (exact files, one shared question, return schema, do-not list) in one parallel wave, then merge. | R41 det |  |
| SKILL05-47 | §Input-shaped Protocol L204-205 | Keep fan-out depth at 1: sub-agents never spawn sub-agents, and never add a depth-2 level to fix a thin merge. | R41 det |  |
| SKILL05-48 | §Input-shaped Protocol L205 | Never run the same query over the same content in two sub-agents; partition once. | R41 det |  |
| SKILL05-49 | §Input-shaped Protocol L205-209 | For pairwise or multi-hop questions, have batches return comparable claim inventories under one schema, not verdicts, then run the cross-batch join. | R41 det |  |
| SKILL05-50 | §Input-shaped Protocol L210-212 | Spot-check the merged answer: re-open the minimal evidence behind each load-bearing line; settle batch disagreements by targeted re-read, never by raising depth or re-running the wave. | R41 det |  |
| SKILL05-51 | §Input-shaped Protocol L213-218 | Synthesise programmatically (aggregate, dedupe, categorise) with file:line references; join inventories in the orchestrator or one inventory-only agent, re-reading both endpoints of flagged pairs. | R41 det |  |
| SKILL05-52 | §Hard rules L235 | Read any file over ~2,000 lines or ~50 KB by line range, never whole. | R41 det |  |
| SKILL05-53 | §Hard rules L236 | Never load more than ~5 files into the main context without a written batch plan. | R41 det |  |
| SKILL05-54 | §Hard rules L231-232, fan-out shapes L243-254 | Distinguish partition fan-outs (all batch/inventory rules apply) from replication fan-outs (same target, different lenses; exempt from disjoint-partition and one-wave rules, but depth-1 and self-contained briefs apply). | R41 det |  |
| SKILL05-55 | §Hard rules fan-out shapes L254-255 | Prefer an existing workflow (pre-ratification-adversarial-panel, handoff-verify-panel, gate-reachability-audit) when one fits; author an ad-hoc wave only when none does. | R41 det |  |
| SKILL05-56 | §Rationalizations L257-268 | Stop on any listed rationalization (cut as I go, too tangled, too granular, parent criteria suffice, read everything first, add depth, small packet carries judgment, manifest in head). | R41 det |  |
| SKILL05-57 | §Relationship L285 | Send a bundled contested question inside an oversize brief to refine-question first; the cut lines often follow its axes. | R41 det |  |
| SKILL05-58 | §Provenance L302 | Never express decomposition budgets in minutes or hours; budget in iterations within the loop-class budget and the one-session unit. | R2 abs |  |
| SKILL05-59 | §Provenance L305 | Add no new document-conversion dependency (anydoc, firecrawl); convert PDF/Office inputs with tools the session already has, then apply the protocol. | R36 det |  |

</details>

### Gates, hooks, settings, seat registry, commands, workflows — 129 rules


<details><summary><code>.claude/commands/lock-check.md</code> — 2 rules: 0 absorbed, 1 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-84 | body L6-13 | Run verify_lock_anchors.py and report verbatim; Closed confirms, Forward names the re-MC trigger and engine regression, Error restores dd_protection.py and re-runs. | R14 det |  |
| GATES-85 | Forward L12 | Never treat the Pepperstone portfolio_mc CLI as the re-MC; use the vendor-free engine regression tests/core/test_mc_synthetic_engine.py. | R14 DEL⚖ | Pepperstone panel map retired (core/mc/modes.py, ADR 2026-07-22 §2-C); vendor-free engine regression owned by AGENTS §Strategy Reference. |

</details>

<details><summary><code>.claude/commands/post-merge.md</code> — 9 rules: 2 absorbed, 7 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-86 | intro L6 | After a merge, run the post-merge checklist and surface only what the merge requires; never invent extra doc rewrites. | R34 det |  |
| GATES-87 | §0 Orient L8-17 | Orient with fetch, status and log; work on an up-to-date main; if the primary tree sits on a spent topic branch, say so and recommend checking out main. | R6 det |  |
| GATES-88 | §1 L19-42 | Run make check or query gate_manifest.py, never a copied list; report failures and never --no-verify anything. | R38 abs |  |
| GATES-89 | §2 L44-49 | If an analysis slug landed or archived, regenerate or verify lab/CATALOG.md with archive_lab_analysis.py; otherwise skip. | R34 det |  |
| GATES-90 | §3 L51-53 | If a merge closed, parked or unblocked a forward item, propose a minimal STATE.md edit without restyling; otherwise report STATE: no change. | R34 det |  |
| GATES-91 | §4 L55-63 | Draft a newest-first SESSIONS entry for a real session outcome, but write the file only when the operator asks to persist it. | R34 det |  |
| GATES-92 | §5 L65-94 | Publish skills only deliberately, from a primary main checkout after independent review, naming the reviewed revision and explicit target; --check or being on main grants nothing. | R6 det | → scripts/README.md#skill-lifecycle |
| GATES-93 | §6 L96-104 | For leftover branches or worktrees run repo_hygiene.py, then report, get operator confirmation, and only then delete; never auto-prune. | R6 abs |  |
| GATES-94 | §7 L106-117 | Close post-merge work with a scoreboard covering gates (naming the branch), CATALOG, STATE, SESSIONS, skill release and hygiene. | R34 det |  |

</details>

<details><summary><code>.claude/commands/skew-audit.md</code> — 2 rules: 0 absorbed, 2 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-95 | steps L6-15 | For a lock skew window (ask for bounds if absent), tabulate each commit's decision, stale pointer, consultation and equivalence; close with zero corrupted decisions or list them. | R14 det |  |
| GATES-96 | L16 | Output the skew-audit table in chat only; never write it to a file, the user persists it if wanted. | R35 det |  |

</details>

<details><summary><code>.claude/hookify.advisor-dedup-first.md</code> — 2 rules: 2 absorbed, 0 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-82 | rule L1-46 | On advisor-staged or build-intent prompts, run check_advisor_dedup.py before scoping work as new; a match means read it, no match proves nothing. | R8 abs |  |
| GATES-83 | L47-49 | Before opening new work, search lab/CATALOG.md and docs/briefs/INDEX.md and paste the literal search output into §0; unpasted dedup attestation is void. | R8 abs |  |

</details>

<details><summary><code>.claude/settings.json</code> — 14 rules: 1 absorbed, 13 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-68 | permissions.allow L4-14 | Pre-approved without prompting: the lock-anchor verifier, read-only git log/diff/status/show/blame, gate_manifest.py and pytest. | R4 det |  |
| GATES-69 | permissions.deny L16-19 | Never read Fly, Azure or gcloud credential directories. | R12 det |  |
| GATES-70 | permissions.deny L20-21 | Never read GitHub CLI credential stores; act only under your own scoped credentials, never the operator's tokens. | R12 det |  |
| GATES-71 | permissions.deny L22 | Never read SSH keys under ~/.ssh. | R12 det |  |
| GATES-72 | permissions.deny L23 | Never read any .env file anywhere on the filesystem. | R12 det |  |
| GATES-73 | PreToolUse Bash guard_shell_command L29-34 | Hook bypass (--no-verify, hooksPath, gpgSign off) and destructive git/fs commands need operator confirmation; run git status and stash or commit first. | R6 det | → scripts/guard_shell_command.py |
| GATES-74 | PreToolUse Bash + mcp__github writes guard_s2_runs L36-38, L58-66 | Never push to a branch with an in-flight S2 run, duplicate a live dispatch, or re-roll a decided S2 run; read its artifact or root-cause it. | R21 det | → .claude/skills/s2-linux-run/SKILL.md §1, §3 |
| GATES-75 | PreToolUse Bash/PowerShell/mcp merge guard_operator_acts L39-42, L67-88 | Hook prompts on live-app rail deploy and arming (including M1 override), passes only head-pinned merges, denies unpinned merge, auto-merge and main push; disarm never prompts. | R4 det | → scripts/guard_operator_acts.py |
| GATES-76 | PreToolUse Bash/PowerShell guard_worktree_evidence L43-46, L74-77 | Before any worktree removal, copy linked worktrees' launcher verification records into the primary checkout's retained archive. | R21 det | → scripts/README.md baseline procedure |
| GATES-77 | PreToolUse Edit/Write guard_open_verification_record L49-57 | Never write into the measured tree while a verification record is running or begun; such a write voids the record. | R21 abs |  |
| GATES-78 | PostToolUse lock_event_hook L92-97 | After edits touching LOCKED numerics, version strings or locked-constant names, run verify_lock_anchors and surface any non-clean result to the agent. | R14 det |  |
| GATES-79 | PostToolUse sync_skills_hook L98-101 | After any .claude/skills edit, run skill-refs and no-constants validators and report release pending; edit hooks never publish skills. | R6 det |  |
| GATES-80 | SessionStart session_divergence_hook L108-111 | Open each session with an origin/main divergence summary flagging governance-surface moves; check it before restating governance state. | R0 det |  |
| GATES-81 | SessionStart sentinel L112-115 | Surface the weekly activity-decision status at session start as an operator call; never treat it as a trade instruction or standing licence. | R10 det |  |

</details>

<details><summary><code>.claude/workflows/gate-reachability-audit.js</code> — 4 rules: 1 absorbed, 3 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-103 | meta whenToUse L5 | At every G0/prereg freeze before operator GO, on door-check repair, or after a domain bar changes, audit each gate for reachability and bindingness; rule FREEZE-SAFE or BLOCKED. | R23 det |  |
| GATES-104 | audit prompt L150-200 | Prefer a mechanical consult that exits nonzero over remembered prose; a door check must reach every binding domain bar and instrument-profile prior. | R23 det |  |
| GATES-105 | streak check L195-198 | Streak and consecutive-null counters must count AMBIGUOUS-HOLD outcomes toward their thresholds. | R28 det |  |
| GATES-106 | synthesis L261-263 | A lane G0 that freezes with an unanswered BINDING BAR escalates its door check to a gates.yml limb. | R23 abs |  |

</details>

<details><summary><code>.claude/workflows/handoff-verify-panel.js</code> — 13 rules: 8 absorbed, 5 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-107 | meta whenToUse L5 | Before executing a substantial external handoff that claims repo state, run independent per-dimension Phase-0 verification and emit HANDOFF-VERIFY PASS or NEEDS_CONTEXT. | R0 abs |  |
| GATES-108 | adjudicate L286-288 | Never author missing artifacts to make a packet coherent; a premise error forks the plan, so return NEEDS_CONTEXT instead of improvised repair. | R0 abs |  |
| GATES-109 | verifier prompt L245-249 | Count only bytes and executed command output as evidence; a packet's internal consistency signals confabulation, not truth. Verifiers report only, never edit. | R0 abs |  |
| GATES-110 | paths L159-162 | Before declaring a path MISSING, enumerate its parent class and check gitignored local data; absence in one location is not absence. | R8 abs |  |
| GATES-111 | edits L168-171 | Accept a claimed edit, landing or closed-this-session status only after git log and the target bytes confirm it. | R0 abs |  |
| GATES-112 | already_executed L186-190 | Search for already-executed deliverables before planning; never re-run an already-scored one-shot test. | R0 abs |  |
| GATES-113 | inflight L196-199 | Verify claimed in-flight work against git log --all, the working tree and sibling worktrees; a nonexistent named consumer is a hard fail. | R0 det |  |
| GATES-114 | identity L205-210 | Before treating a label or rule numeral as established, rg -F it repo-wide and confirm any new numeral is not already taken. | R0 det |  |
| GATES-115 | identity, statuses L177-180, L208-210 | ADR files are date-prefixed YYYY-MM-DD-title.md, never sequential NNN; closure verdicts live in the filename Q-...-closure-<verdict>. | R32 det |  |
| GATES-116 | self_referential L216-220 | Verify any fire count or instance number by counting the owning registry file yourself; claimed anti-instances earn no exemption. | R0 det |  |
| GATES-117 | posture_numeric L226-233 | Read live posture only from AGENTS.md §Live-execution posture and constants from owning bytes (dd_protection.py, firm_rules.py), never from a packet. | R0 abs |  |
| GATES-118 | posture_numeric L231-232 | Treat challenge-era MC pass/bust rates as historical pins, never live probabilities. | R20 abs |  |
| GATES-119 | adjudicate L288-290 | If a packet names frozen campaign gates, run gate-reachability-audit on the cited prereg before any pull or scoring. | R23 det |  |

</details>

<details><summary><code>.claude/workflows/pre-ratification-adversarial-panel.js</code> — 10 rules: 4 absorbed, 6 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-120 | meta whenToUse L5 | Before ratifying any Pre-Q brief, ADR or closure, run the refute-first multi-lens adversarial review; a green check_brief.py pass is form-only. | R5 det |  |
| GATES-121 | safety hard block L203-234, L261-273 | On GRAND-tier review, a target citing dry_run, armed_until, M1 RESOLVED or arm-not-send hard-blocks synthesis; a failed scan also blocks. | R10 det |  |
| GATES-122 | steelman lens L130-133 | Give every §6 bare-count threshold a qualitative scope, such as production risk-control sites, not just N files. | R33 abs |  |
| GATES-123 | structural lens (a) L141-142 | A later section restating §6 floor or headline criteria must reproduce them verbatim, not drift into generic lock language. | R33 det |  |
| GATES-124 | structural lens (b) L142-144 | Give any deliberate watch-don't-act restraint decision an explicit Watch-items section as prominent as action items. | R33 det |  |
| GATES-125 | structural lens (c) L144-146 | Before minting a new ADR, brief or notice, show an amend-before-mint search proving no existing owner should take it as an addendum. | R29 abs |  |
| GATES-126 | structural lens (d) L146-147 | Every closure doc carries a Registry: line pointing into docs/rejected_candidates.md or stating n/a. | R26 abs |  |
| GATES-127 | structural lens L139-140 | Briefs must substantively carry §0 Rule-0 production reads, §4 falsifiable hypothesis, §5 forbidden moves, §6 gate criteria and §10 audit hooks. | R33 abs |  |
| GATES-128 | arithmetic, input lenses L85-119 | Re-derive every numeric claim from stated primitives and re-verify mutable venue, firm and feed inputs against primary sources, not the brief's restatement. | R0 det |  |
| GATES-129 | screen, steelman lenses L97-133 | Every passed or cleared claim needs an artifact showing the computation; flag unscored screens and asserted-but-unchecked bounds as blockers. | R0 det |  |

</details>

<details><summary><code>scripts/gates.yml</code> — 44 rules: 7 absorbed, 36 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-1 | header tiers L5-12 | Classify every gate into one of four tiers: always, path-conditional, data-conditional or audit; audit gates are report-only and excluded from pre-commit and required CI. | R38 det |  |
| GATES-2 | header L14-18 | The gate runner must refuse to load a manifest naming an unknown tier (including retired soft), so no gate is silently disabled. | R38 det |  |
| GATES-3 | header L1-3 | Own gate composition only in scripts/gates.yml via gate_manifest.py; never hand-maintain a parallel gate list in hooks, Make or docs. | R38 abs |  |
| GATES-4 | comments L78-89, L113-119, L216-219, L443-447 | Admit a blocking gate only if it protects a qualifying invariant, every violating change selects it via its trigger regex, and a finding exits non-zero. | R38 abs |  |
| GATES-5 | evidence-store L23 | When evidence_store code, its tests or gates.yml are staged, the tests/evidence_store unit suite must pass. | R21 det |  |
| GATES-6 | pursuit-records comment L59-63 | pursuit-records gate is retired: its checker always exits 0, so it is unfalsifiable; the retained script runs only manually. | R38 DEL | Retirement owned by ADR 2026-08-24-validation-battery-k-tiering; tests/test_gate_manifest.py L209 asserts pursuit-records not selected; comment is redundant tombstone. |
| GATES-7 | skills-no-constants L37 | Never restate operational constants in the three methodology skills; operational-reference skills and pinescript-v6 are exempt. | R29 det |  |
| GATES-8 | skill-refs L43 | Every repo path a SKILL.md cites must resolve, unless it is gitignored vendor data, matches .gitignore, or is marked (deleted)/(retired). | R29 det |  |
| GATES-9 | data-manifests L50 | Staged vendor-data trees under core/data must hash-match their SHA256SUMS manifests; drift, missing or extra files fail the commit. | R19 abs |  |
| GATES-10 | pine-manifest L65 | Where Pine is present, every MANIFEST/PORT_MANIFEST pin must exist and hash-match; re-pin in the same change as any re-author. | R13 det |  |
| GATES-11 | pine-pin-provenance L71 | Never pin gitignored Pine from a disposable checkout or relax a pin to pass; re-pin from a machine that durably keeps the bytes. | R13 det |  |
| GATES-12 | repo-map-scripts-table L90 | REPO_MAP §2.1 scripts table must equal generator output; on drift regenerate with check_repo_map_scripts_table.py --write instead of hand-editing. | R37 det |  |
| GATES-13 | durable-store-pragmas L99 | Register every ops/ sqlite3.connect site; durable rail stores must set PRAGMA synchronous=FULL and issue BEGIN IMMEDIATE. | R11 det |  |
| GATES-14 | boundaries L107 | Keep imports legal: core imports no internal layer, governance only core, lab/ops only core and governance, never lab-ops; keep sources 3.11-parseable. | R37 det | → docs/adr/2026-06-05-monorepo-layer-boundaries.md §2.1 |
| GATES-15 | path-liveness L120 | Every committed parent directory declared in core/strategies/MANIFEST.sha256 must exist on disk. | R29 det |  |
| GATES-16 | root-doc-liveness L126 | Every repo-relative markdown link in README, AGENTS, PIPELINES, REPO_MAP and STATE must resolve or be gitignored; repoint dead links. | R29 det |  |
| GATES-17 | status-consistency L132 | Keep lab/CATALOG.md rows self-consistent and repoint lab/analysis links whose study moved to lab/archive or a theme nest. | R34 det |  |
| GATES-18 | adr-graph L144 | ADRs must use the Status vocabulary, supersede only to Accepted successors, keep stub shape and INDEX sync; STATE must not cite superseded ADRs without successors. | R32 det |  |
| GATES-19 | lab-catalog L152 | Whenever lab/ changes, lab/CATALOG.md must match a fresh archive_lab_analysis.py scan; regenerate it rather than letting it go stale. | R34 det |  |
| GATES-20 | cost-model-closed-world L162 | Every cost-model geometry needs a commission classification, every priced symbol needs geometry, and explicit commission bindings must name valid categories. | R24 det |  |
| GATES-21 | instrument-profiles L172 | Instrument ledger PROFILE blocks must pass schema and mechanism-id checks, and the derived PROFILES view must not be stale. | R27 det |  |
| GATES-22 | sessions-order L181 | docs/SESSIONS.md entries need unique session labels, leading --- separators without doubles, and newest-first order. | R34 det |  |
| GATES-23 | sessions-append-only L190 | Never edit the bodies of prior docs/SESSIONS.md entries; the log is append-only. | R34 abs |  |
| GATES-24 | sessions-queue-bind L199 | The SESSIONS.md header must link to STATE.md's operator queue; historical entries are not current-state mirrors. | R34 det |  |
| GATES-25 | state-currency L207-214 | Keep STATE.md Last curated, recurring deadlines and dated sections current and parseable; staleness fails every commit (America/New_York clock). | R34 det |  |
| GATES-26 | supersession-placement L216-226 | When an addendum withdraws or supersedes a lab RESULTS finding, place a supersession token or addendum pointer above the addendum heading. | R30 abs |  |
| GATES-27 | closure-disposition L228 | Closures need an Iterate heading, one Next: verdict (INTEGRATE/ITERATE/STOP), Board write and Registry: tokens; every terminal-verdict campaign needs a closure file. | R28 det | → scripts/README.md#closure-enforcement |
| GATES-28 | handoff-authority L236-247 | A card's yaml authority block may only narrow: registered, non-forbidden, non-operator-act capabilities within seat and parent risk; worker cards name parent and acceptance tests. | R4 abs |  |
| GATES-29 | handoff-brief-form L249-265 | Every non-grandfathered card under docs/briefs/handoffs/, or any brief with an authority block, must pass check_brief.py --type handoff as well-formed. | R33 abs |  |
| GATES-30 | instrument-rejection-coverage L267-287 | Each instrument-scoped terminal-negative closure needs a DEAD row in that instrument's ledger; audit-only until the corpus is clean, then promote to blocking. | R26 det | → docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md D4 |
| GATES-31 | sync-liveness L289 | At audit cadence, census INDEX/CATALOG liveness drift; moving INDEX Open versus Recently-closed rows stays a judgment call. | R34 det |  |
| GATES-32 | lifecycle-consistency L297 | Live-file restatements of lifecycle tier and multiplier must match core/lifecycle.py's ladder and, while uniform, the current default tier. | R15 det |  |
| GATES-33 | docs-runtime-inventory L305 | At audit cadence, index Python runtime reads of docs/ paths so docs-as-runtime dependencies stay visible; report-only, never prune. | R31 det |  |
| GATES-34 | repo-map-layers L313 | scripts/repo_map_layers.yml must pass its schema: known layers, slash-terminated existing prefixes, and scripts_layer stems that are tracked scripts. | R37 det |  |
| GATES-35 | governance-prose-control-chars L325 | Governance prose (SESSIONS, rejected_candidates, mc_anchor_history, STATE, ADRs, briefs, notes) must contain no C0 control except TAB/LF/CR, and no DEL. | R38 det |  |
| GATES-36 | skill-deploy-sync L335-373 | Every skill script an ADR Verification block cites must exist in the locally deployed bundle; skip when no repo bundle is deployed. | R6 det |  |
| GATES-37 | m1-artifact-structure L375 | Keep the M1 monitoring acceptance artifact structurally valid and secret-free (secrets_present false); a corrupted or secret-shaped artifact rejects the commit. | R10 det |  |
| GATES-38 | m1-tree-skew L387 | At audit time report deployed-versus-main skew of the M1 artifact; skew never rejects a commit. | R10 det |  |
| GATES-39 | falsifier-reachability-census L397 | Quarterly, census whether ADR falsifiers' named input files or commands still exist; a green run means no named input missing, not falsifiers in force. | R28 det |  |
| GATES-40 | notice-grade-k-correction L406 | Report Notice GRADUATE/INCREMENT verdicts whose cited trial count K exceeds the DSR-reachable band; report-only. | R23 det |  |
| GATES-41 | spec-provenance L413 | Report canon-amending docs/spec files that cite no ADR; specs commission builds and never authorize canon changes. | R32 det | → docs/spec/README.md |
| GATES-42 | rule2-trip-log-liveness L421 | Report whether the Rule 2 trip-log checklist item ran: from 2026-11-08, flag absent programme-audit notes mentioning Rule 2 or the trip-log. | R2 det |  |
| GATES-43 | evidence-archive L429 | Every pinned private digest needs a second copy in first-passage-archive; audit reports ARCHIVED, UNPUSHED, MISSING or UNVERIFIED. | R31 det | → scripts/README.md#private-evidence-archive |
| GATES-44 | staged-debris L438-462 | Never stage recovery/, tmp/ or root tmp-* paths, force-added ignored files, or blobs over 1 MB (2 MB under lab/analysis and lab/archive). | R13 det |  |

</details>

<details><summary><code>scripts/githooks/post-merge</code> — 3 rules: 0 absorbed, 3 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-100 | (2) L68-107 | After a merge touching SESSIONS.md, warn on duplicate labels for manual renumbering and repair union debris in the working tree without committing. | R34 det |  |
| GATES-101 | (2) L101-104 | When a same-day SESSIONS entry must float, mark it in the heading using the '(later)' convention rather than re-sorting entries. | R34 det |  |
| GATES-102 | (1) L36-66 | If a merge brings a Pine pin made on a disposable checkout, never delete or weaken it; recover and re-pin now, or record a reconstruction, not a recovery. | R13 det |  |

</details>

<details><summary><code>scripts/githooks/pre-commit</code> — 1 rules: 0 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-97 | L1-8 | Every commit runs gate_manifest.py --tier pre-commit through the fp.py launcher; any failing gate blocks the commit. | R38 det |  |

</details>

<details><summary><code>scripts/githooks/pre-merge-commit</code> — 1 rules: 0 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-99 | L1-26 | Local merge commits must pass the SESSIONS label-order and append-only checks, since union merges create duplicate labels without conflicts. | R34 det |  |

</details>

<details><summary><code>scripts/githooks/pre-push</code> — 1 rules: 0 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-98 | check 1 L2-25 | Refuse a push when a governance surface (AGENTS, STATE, SESSIONS, ADRs, preregs) changed on both sides since the merge-base with origin/main; override only explicitly. | R6 det |  |

</details>

<details><summary><code>scripts/repo_map_layers.yml</code> — 2 rules: 0 absorbed, 2 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-66 | header L1-3 | Define layer maps once in scripts/repo_map_layers.yml; check_boundaries and the REPO_MAP scripts table load it, never a second copy. | R37 det |  |
| GATES-67 | layer maps L5-62 | A file's layer is its path: core/, lab/, ops/ directories; docs, .claude, .github, deploy, tools and root files are governance; scripts stems per scripts_layer, default governance. | R37 det |  |

</details>

<details><summary><code>scripts/seat_authority.yml</code> — 21 rules: 8 absorbed, 13 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| GATES-45 | header L1-7 | Keep capability names, risk classes and seat grants only in seat_authority.yml; change the rule in the surface-allocation ADR, then this value in the same PR. | R4 det |  |
| GATES-46 | risk classes L20-31 | Risk classes: low is read-only/isolated; medium is reversible shared-state change and the agent ceiling; high is an operator act; forbidden is ungrantable to anyone. | R4 det |  |
| GATES-47 | risk high L24-25, seats L94-95 | Never grant a high-risk operator act in a card; the operator performs it through an act they already perform. | R4 abs |  |
| GATES-48 | capabilities L36-48 | Capability scopes: worktree.write is the card's own worktree/branch; research.run stays inside its approved campaign contract; pr.review is comments, never merge approval. | R4 det |  |
| GATES-49 | branch.push L41 | Push agent branches only under codex/* or claude/*; branch.push never covers main. | R6 abs |  |
| GATES-50 | cloud.dispatch L45 | Dispatch work to the cloud only with task-routing's environment GO. | R41 det | → .claude/skills/task-routing/SKILL.md |
| GATES-51 | pr.merge L49-53 | An agent may merge only pinned to the head SHA, after an independent non-author review passes and every CI check is completed green; never grant merge in a card. | R6 abs |  |
| GATES-52 | governance.ratify, spend L54-55 | Ratifying an ADR, prereg or closure and any paid service or subscription are operator acts; agents never perform them. | R3 det |  |
| GATES-53 | rail.deploy, rail.arm L56-57 | Fly deploy of c1-rail and rail arming are operator acts; arming requires M1 RESOLVED plus a separate GO per armed session. | R10 det |  |
| GATES-54 | trade.submit L58-64 | Agents submit an order, exit or cancel only when the operator directs that specific act, via an authenticated attended or computer-use surface; never hold broker credentials. | R10 det |  |
| GATES-55 | forbidden pr.auto_merge L67 | Never enable GitHub auto-merge; it is forbidden to every seat. | R6 abs |  |
| GATES-56 | forbidden tv.login_automation L70 | Never automate TradingView login. | R11 det |  |
| GATES-57 | forbidden locked_parameter.edit L73 | Never edit locked strategy parameters; no approval unlocks this for an agent. | R14 abs |  |
| GATES-58 | forbidden protection_constant.edit L76-79 | Never edit DD_TRIGGER/DD_SCALE; the sole route is pre-registration, re-MC, both-halves regime gate and an operator-ratified admitting ADR. | R14 abs |  |
| GATES-59 | forbidden private_data.commit L80 | Never commit account identifiers or P&L, vendor-licensed CSVs, Pine source or locked ports. | R13 abs |  |
| GATES-60 | forbidden main.direct_push L83 | Never push directly to main; main takes PRs and requires the skills (3.12) status. | R6 abs |  |
| GATES-61 | acceptance_required_for L87-92 | Any card granting worktree.write or research.run must name acceptance tests whatever seat it declares; a registry lacking this key fails closed. | R4 det |  |
| GATES-62 | seats.executive L97 | Executive cards may grant only repository.read, tests.run, pr.review and governance.author. | R4 det |  |
| GATES-63 | seats.coordinator L100 | Coordinator cards may grant read, tests, worktree write, research, branch push, PR open and review, CI/cloud/handoff dispatch, governance authoring and core-anchor edits. | R4 det |  |
| GATES-64 | seats.escalation L105 | Escalation cards may grant read, tests, worktree write, branch push, PR open and review, governance authoring and core-anchor edits; no dispatch or research. | R4 det |  |
| GATES-65 | seats.worker L109 | Worker cards may grant only read, tests, worktree write, research, branch push, PR open and CI dispatch. | R4 det |  |

</details>

### Accepted ADRs — 1775 rules


<details><summary><code>docs/adr/2026-04-17-dd-trigger-calibration.md</code> — 3 rules: 1 absorbed, 0 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-1 | Decision L24 | Multiply the day's sizing by the frozen DD_SCALE factor whenever the DD tier fires; treat DD_SCALE as a frozen protection constant. | R14 abs |  |
| ADR01-2 | Decision L23 | Fire DD protection at the C0 trigger (1.0% drawdown from peak). | R14 DEL⚖ | Superseded by docs/adr/2026-05-08-dd-trigger-c2-relock.md (header Superseded-in-part-by); live DD_TRIGGER=0.015 in core/dd_protection.py L80. |
| ADR01-3 | Alternatives L38 | Treat the queued post-challenge DD retune proposal as inactive; it is not current protection. | R14 DEL⚖ | FXIFY challenge retired; AGENTS.md §Protection chain (pre-reg, re-MC, both-halves, ADR) is stricter and governs any retune. |

</details>

<details><summary><code>docs/adr/2026-04-17-equity-tier-deletion.md</code> — 2 rules: 2 absorbed, 0 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-4 | Decision L22 | Keep dd_protection single-tier: one drawdown-from-peak trigger, with no equity-level tier combined with it. | R14 abs |  |
| ADR01-5 | Consequences L38 | Reintroduce an equity-level floor only through a new ADR when portfolio changes make it useful; never restore it preemptively. | R14 abs |  |

</details>

<details><summary><code>docs/adr/2026-04-17-portfolio-allocations.md</code> — 6 rules: 3 absorbed, 1 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-6 | Decision L28-30 | Size per-strategy allocations by recovery-factor optimization under the portfolio bust constraint, never above a strategy's RF-implied ceiling. | R15 DEL | Superseded by Addendum 2026-08-29 and allocation-refresh-2 lock; live sizing is firm_rules._BASE_RISK (striker legs only, L659). |
| ADR01-7 | Risks L49 | On a binary macro volatility event, monitor the affected allocation; do not cut it preemptively. | R1 abs |  |
| ADR01-8 | Risks L50 (struck) | Rerun portfolio MC before activating each funded-ramp allocation step. | R15 DEL | Struck in the ADR itself (L50), superseded same day by unified-allocation decision; FXIFY funded ramp retired. |
| ADR01-9 | Header L3-6; Addendum L65 | Read current allocations from core/firm_rules.py and core/historical_challenge.py, never from ADR title figures. | R14 abs |  |
| ADR01-10 | Addendum 2026-08-29 L63, L82 | Keep ADR Context/Decision bodies byte-unedited; record corrections as dated addenda; correct living pointer documents such as the ADR INDEX in place. | R30 abs |  |
| ADR01-11 | Addendum 2026-08-29 L58-62, L82 | When an ADR's status has decayed undocumented, add a dated discharge addendum and correct the INDEX mirror in the same commit. | R28 det | → .claude/skills/programme-audit/SKILL.md (ADR decay sweep) |

</details>

<details><summary><code>docs/adr/2026-04-17-striker-v4.3-pyramid.md</code> — 4 rules: 3 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-12 | Decision L22 | Treat the Striker DJ30 v4.3+ architecture (T1 partial removed, pyramid-add retained) as locked; do not modify its parameters. | R14 abs |  |
| ADR01-13 | Decision L24; Consequences L37 | Keep Striker parameter values and backtest figures in Pine and the private archive only; never restate them in public docs. | R14 abs |  |
| ADR01-14 | Risks L46 | Do not react to drawdown duration alone; monitor it, since no modeled playbook exists. | R1 abs |  |
| ADR01-15 | Risks L48 | Set DXTrade contractValue to 10 before any Striker trade; the default of 1 silently oversizes risk. | R11 det | → docs/operational_rules.md §3 |

</details>

<details><summary><code>docs/adr/2026-04-23-guardian-risk-relock-0.34.md</code> — 1 rules: 0 absorbed, 0 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-16 | Decision L42 | Re-lock Guardian per-trade risk just under both bust and static-DD caps with preserved headroom; Striker and Aegis unchanged. | R14 DEL⚖ | Guardian cold-stored by 2026-08-23-strategy-coldstore-phase-c.md; frozen 0.0034 preserved in core/historical_challenge.py L63; no live _BASE_RISK entry. |

</details>

<details><summary><code>docs/adr/2026-04-24-mvd-discipline.md</code> — 13 rules: 4 absorbed, 6 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-17 | Decision L45; L61; L124 | Apply MVD to artifacts whose silent failure would change allocation, risk parameters or lock decisions; exempt exploratory work; future locks and re-MCs follow MVD. | R0 det |  |
| ADR01-18 | North star L49 | Build defenses as inline code assertions and template preambles, not checklists or memory rules. | R36 abs |  |
| ADR01-19 | Mandatory triggers L55 | Guard every MC input panel load with identity, cardinality and no-fallback assertions. | R0 det |  |
| ADR01-20 | Mandatory triggers L56, L59 | Make every performance number or named behavior cited in a lock brief, ADR, memory or CHANGELOG reproducible by a script with identity assertions. | R0 abs |  |
| ADR01-21 | Mandatory triggers L57 | Make any risk-control code change self-validate that its guards fire and its fallbacks do not. | R14 det |  |
| ADR01-22 | Mandatory triggers L58 | Apply MVD to allocation changes made in accounts.json or via CLI update/lots operations. | R0 DEL | accounts.json/accounts.py absent from git ls-files; ops accounts/CLI spine retired by 2026-07-22-challenge-era-substrate-retirement.md (cfd-estate ADR header). |
| ADR01-23 | Assertion library L63-71 | Use core/lib/mvd.py's five helper families (cardinality, identity, contract, cross-source, code-vs-doc) in load-bearing scripts. | R0 abs |  |
| ADR01-24 | Assertion library family 5 L71 | Paste literal production lines into briefs; back any 'primary X' claim with a generating script, not a sentence. | R0 abs |  |
| ADR01-25 | Producer-side rule L75 | Place identity assertions within about five lines of identifier declaration, and cardinality/contract assertions at the producing site, not the consumer. | R0 det |  |
| ADR01-26 | Consumer-side promotion check L79-83 | Add an MVD-attest line to any brief, ADR, memory or CHANGELOG citing numbers; block promotion if producing scripts lack identity assertions. | R0 DEL | Dropped by MVD Addendum 2026-08-14: MVD-attest has zero hits in docs/briefs, not practiced or enforced. |
| ADR01-27 | Update protocol L87-91 | Log every post-MVD caught bug in the MVD audit table, adding worked examples or helpers for new families. | R36 DEL | docs/methodology/mvd.md absent; MVD Addendum 2026-08-14 records the update protocol has no live home. |
| ADR01-28 | Known risks L129 | If an MVD helper costs more than one import plus one line, refactor the helper rather than skip it. | R0 det |  |
| ADR01-29 | Known risks L130 | Add MVD triggers only by deliberate ADR amendment; there is no standing review clause. | R0 det |  |

</details>

<details><summary><code>docs/adr/2026-05-03-sentinel-gate-decision.md</code> — 5 rules: 3 absorbed, 1 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-30 | Decision L28 | Do not build Sentinel (no-overlay short-Donchian USDCHF H4); its gate verdict is a kill. | R26 abs |  |
| ADR01-31 | Alternatives 4 L67-71 | Never retry a rejected concept with new parameters without a fresh pre-Q gate; re-proposal needs new mechanism evidence. | R26 abs |  |
| ADR01-32 | Alternatives 5 L73-77; Forbidden-D-test audit L98-108 | Derive gate verdicts mechanically from pre-registered criteria; never rescue a failed gate with post-hoc subset filters, recording them as forward observations only. | R23 abs |  |
| ADR01-33 | Re-open triggers L120-131; Consequences L88-91 | Reopen Sentinel only for a different operationalization clearing its own pre-Q gate or its named forward observation firing; no parameter retry or follow-up loop. | R26 det |  |
| ADR01-34 | Consequences L92-94 | Keep the USDCHF H4 bar panel as audit-trail substrate only; do not migrate it to the operational pipeline. | R19 DEL | USDCHF H4 panel absent: no USDCHF in git ls-files or core/data/bar_data/SHA256SUMS; data/bar_data path does not exist. |

</details>

<details><summary><code>docs/adr/2026-05-08-dd-trigger-c2-relock.md</code> — 6 rules: 2 absorbed, 0 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-35 | Decision L31 | Fire DD protection at the C2 trigger (DD_TRIGGER 1.5% from peak, DD_SCALE 0.40x); both constants are frozen. | R14 abs |  |
| ADR01-36 | Reader intercept L90 | Change DD constants only via pre-registration, re-MC, the both-halves regime-robustness gate, then an admitting ADR. | R14 abs |  |
| ADR01-37 | Forward revert trigger L93-99; Negative L71 | Reopen C0/C2 if rolling 6-month MC pass-rate falls below 95% for two consecutive windows; check quarterly via time_to_pass --regime-check. | R28 DEL⚖ | Retired by 2026-07-11-challenge-era-claims-rescope.md Addendum 2026-07-22 (§D2); Pepperstone panel retired, check reports AMBIGUOUS-no-input. |
| ADR01-38 | Reader intercept L86-88 | Do not conflate the retired C2 revert check with allocation-refresh-2's §Falsifier forward-revert trigger, which the banner calls still live. | R28 DEL⚖ | Intercept's 'still live' claim contradicted by allocation-refresh-2 Addenda 2026-08-02/08-15 (zero live catch-paths); keep-or-drop distinction is operator's call. |
| ADR01-39 | Context L16; Decision L36 | Use the Pepperstone panel for attribution and lock decisions; use OANDA only as a secondary pattern-spotting surface. | R18 DEL | Pepperstone retired 2026-08-02, OANDA by 2026-06-24-oanda-retirement.md; AGENTS.md canonical feed is CME TV exports. |
| ADR01-40 | Locked MC numbers L51 | Pin the C2 MC anchor in tests/test_mc_anchors.py and tests/test_mvd_selfchecks.py. | R20 DEL⚖ | tests/core/test_mc_anchors.py removed in substrate Phase 3 (2026-07-24) per docs/mc_anchor_history.md L3; synthetic engine test replaces. |

</details>

<details><summary><code>docs/adr/2026-05-10-dd-protection-ulp-rounding.md</code> — 5 rules: 0 absorbed, 3 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-41 | Decision L45-55; Alternatives 1-2 L107-108 | Round dd_from_peak to 6 dp before the inclusive >= DD_TRIGGER comparison; never loosen with an epsilon; precision changes need a new ADR. | R14 det |  |
| ADR01-42 | Asymmetry of error costs L57-66 | When risk-control error costs are asymmetric, resolve boundary or precision ambiguity toward the conservative-of-trader reading: inclusive boundary, fire early. | R14 det |  |
| ADR01-43 | Alternatives 4 L110 | Keep risk-control and lock-change PRs strictly scoped: no drive-by edits at other comparison sites or bundled unrelated lock changes; surface those via deliberate audit. | R14 det | → docs/operational_rules.md §6 |
| ADR01-44 | Consequences L79; Follow-up #55 L101 | Re-run MC after the ULP fix to confirm the C2 anchor; drift beyond tolerance triggers a separate C2 re-evaluation ADR. | R14 DEL⚖ | Discharged by docs/adr/2026-05-10-mc-c2-anchor-ratification.md: re-run delta 0.00pp, GH#55 closed. |
| ADR01-45 | Follow-ups #54/#56/#57 L100-103 | Audit other risk-control comparison sites for ULP defects (Pre-Q if three or more), re-evaluate historical state logs, and review the self-check epsilon. | R14 DEL⚖ | #54 targets absent accounts.py, #56 absent dd_protection_state.json; issues in retired multi_firm_operations repo; #57 epsilon question still open (1e-4, L251). |

</details>

<details><summary><code>docs/adr/2026-05-10-manifest-integrity-gate.md</code> — 5 rules: 1 absorbed, 3 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-46 | Decision 1-2 L27-28; Windows note L43; Consequences L47; §7 L73 | Any commit staging vendor-data paths must pass check_data_manifests.py --check, hashing working-tree bytes; MANIFEST_DIRS owns the directory set. | R19 det |  |
| ADR01-47 | Decision 2 L28 | Install the tracked git hooks once per clone via scripts/install_hooks.sh or scripts/install_hooks.bat. | R19 abs |  |
| ADR01-48 | Decision 2 L28 | Use git commit --no-verify as the explicit escape hatch around the manifest hook. | R19 DEL | Superseded by AGENTS.md §Vendor-data integrity gate ('not the standing path') and scripts/guard_shell_command.py blocking --no-verify. |
| ADR01-49 | Decision 3 L29; Consequences L49 | CI validates SHA256SUMS format and fails if any vendor CSV under tv_exports or bar_data is tracked; CI never replaces the local hook. | R19 det |  |
| ADR01-50 | Consequences L48 | After a deliberate re-export, run --regenerate (dry-run first) and commit the SHA256SUMS update with the data change. | R19 det |  |

</details>

<details><summary><code>docs/adr/2026-05-10-mc-c2-anchor-ratification.md</code> — 3 rules: 0 absorbed, 1 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-51 | Decision 3 L34; Consequences L39; Forbidden L46; Addendum L116-121 | Before listing cross-domain MC follow-ups for dd_protection or MC threshold fixes, grep-verify the import topology; any topology change reopens verification. | R0 det |  |
| ADR01-52 | Forbidden moves L44 | Do not repin anchor tests to bitwise-identical post-fix values as ceremonial confirmation. | R20 DEL⚖ | Anchor pin tests deleted in substrate Phase 3 2026-07-24 (mc-c2 ratification Addendum 2026-08-29); nothing left to repin. |
| ADR01-53 | Audit hooks L55-90 | Run the import-topology and anchor-pin audit hooks at quarterly review; any failure requires re-evaluating the ADR. | R28 DEL | mc-c2 ratification Addendum 2026-08-29: hooks target deleted test_mc_anchors.py and 50-line facade core/portfolio_mc.py; historical. |

</details>

<details><summary><code>docs/adr/2026-05-16-fixture-test-requirement.md</code> — 7 rules: 0 absorbed, 5 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-54 | §2 L70-74; Amendment L196 | Give every analysis script whose output is cited as brief §3/§4 evidence at least one pytest fixture test asserting an anchor invariant, retrofitting before its next citation. | R0 det |  |
| ADR01-55 | §2 L76-84 | When a brief's §0 lists a script as a production read, verify it has an anchor fixture test; block the brief until one exists. | R0 det |  |
| ADR01-56 | §5 L131-143 | Keep the fixture-test requirement scoped to brief-evidence scripts; do not broaden it repo-wide or codify it into INQHIORI methodology. | R0 det |  |
| ADR01-57 | §5 L144-147 | For a CC spawn brief with three or more mechanical edits in one defect family, dry-run the edits on a local snapshot before handoff. | R33 DEL⚖ | Only owner is archived docs/methodology/archive/notion/methodology-canon.md §7; no live skill, ADR or rule carries the dry-run rule. |
| ADR01-58 | §4 L110-125; §6 L149-158; Amendment L243-246 | At the 2026-11-16 review, revoke the §2 discipline if no fixture caught a real defect, confirm on an F-N entry, or extend six months explicitly if ambiguous. | R28 det |  |
| ADR01-59 | §3 L92; §10 Hook 3 L174-176 | Record each fixture-caught defect as an F-N entry (## F-N heading) in docs/methodology/lessons/methodology_lessons.md. | R33 det |  |
| ADR01-60 | §10 Hook 1 L162-169; Amendment L192 | Run scripts/check_brief_evidence_coverage.py to inventory brief-evidence scripts lacking fixture tests. | R0 DEL | scripts/check_brief_evidence_coverage.py deleted per fixture ADR Amendment 2026-06-08 (all false positives, never wired). |

</details>

<details><summary><code>docs/adr/2026-05-16-fxify-correct-timeout-semantic.md</code> — 10 rules: 3 absorbed, 5 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-61 | Decision L67-72 | Model MC inactivity as bust_inactivity after 60 consecutive idle bdays (symmetric idle check); horizon_cap 1500 is only a tractability safety. | R20 det |  |
| ADR01-62 | Decision L73-74; Implementation notes L158 | Re-pin MC anchors and re-point inactivity boundary tests to the production simulator in one coordinated commit. | R20 DEL | Executed in the ADR's coordinated commit (Implementation notes L158); test_mc_anchors.py since deleted in substrate Phase 3. |
| ADR01-63 | Falsifier L95-112 | Revert to the 150-bday semantic and prior anchor pins if any falsifier limb fires: rule change, live idle run, quarterly drift, or anchor non-reproduction. | R28 DEL⚖ | FALSIFIER-UNREACHABLE banner 2026-08-08: FXIFY closed, Pepperstone retired, PANELS_BY_BROKER empty; dormant falsifier on retired venue. |
| ADR01-64 | Falsifier banner L104-105 | Re-arm an unreachable falsifier only with a successor venue rule and runnable panel, booked at programme audit; never roll its dates forward silently. | R28 det |  |
| ADR01-65 | Forbidden moves L147 | Never re-anchor canonical MC headline or test anchor literals without an admitting ADR. | R14 abs |  |
| ADR01-66 | Forbidden moves L149 | Take MC anchor literals only from a deterministic re-run of production code, never from side scripts or eyeballed results. | R20 det | → .claude/skills/prop-firm-challenge/SKILL.md (MC anchors) |
| ADR01-67 | Forbidden moves L150; Negative L129 | Sequence a lock change: ADR first; code, pins and doc edits in one coordinated commit; then the closure note; downstream surfaces as standalone work. | R14 det | → docs/operational_rules.md §6 |
| ADR01-68 | Forbidden moves L151 | Do not adopt a full-panel pass-rate improvement without regime-robustness (half-panel and bootstrap) evidence. | R24 abs |  |
| ADR01-69 | Audit hooks L168-179 | When audit hooks cite moved or deleted paths, repoint them under the sanctioned dated HOOK WIDENED pattern instead of leaving dead checks. | R30 det | → docs/operational_rules.md §14 |
| ADR01-70 | Audit hooks L195-197 | A superseding ADR must declare Supersedes and back-link; update the superseded ADR's status to SUPERSEDED-BY. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-05-23-allocation-refresh-2.md</code> — 17 rules: 5 absorbed, 5 detail, 7 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-71 | Decision L71-80 | Hold Striker DJ30 and NAS100 risk and pyramid at the refresh-2 lock (values in firm_rules._BASE_RISK and Pine); dd_protection unchanged. | R14 det |  |
| ADR01-72 | Context L60; Consequences L119 | Under the no-version-bump doctrine, a version label (v4.5, v1) denotes whatever the current Pine production parameters are. | R14 DEL⚖ | Contradicted by stricter AGENTS.md §Strategy Authorization Lifecycle (locked parameters immutable) and pine-manifest pins; doctrine status unclear. |
| ADR01-73 | Locked MC numbers L82-96 | Treat the refresh-2 MC anchor as the canonical calibration reference, pinned by tests/test_mc_anchors.py. | R20 DEL⚖ | Superseded by AGENTS.md §Strategy Reference (historical record, not live claim) and mc_anchor_history.md L3; test pins deleted 2026-07-24. |
| ADR01-74 | §Falsifier L100-108 | Invalidate the allocation and revert both strategies to the documented prior config if the regime-check or live edge-captured-ratio limbs fire. | R28 DEL⚖ | All three limbs dark (Addenda 2026-07-01/08-02); operator accepted absence 2026-08-15; re-arm needs fresh Pre-Q remap. |
| ADR01-75 | Addenda L341-346, L424-430, L498 | Re-arm the falsifier only when a live-fill route reopens (fresh Pre-Q mapping to futures fills) or a non-challenge panel anchor is re-registered by ADR. | R28 det |  |
| ADR01-76 | Addendum 2026-08-02 L396-404 | Treat the regime-robustness gate as not mandatory for allocation changes; skipping it there is not a violation. | R24 abs |  |
| ADR01-77 | Open item 6 L259; Override 5 L146 | If a third allocation refresh skips the regime gate, amend regime_robustness_gate.md to settle allocation scope explicitly. | R24 DEL | Already settled: regime_robustness_gate.md L29 lists allocation changes as Not required since 26f3a26 (refresh-2 Addendum 2026-08-02). |
| ADR01-78 | Forbidden moves L165 | Document Pine parameter changes explicitly in their ADR; never treat them as a routine panel refresh. | R14 det | → docs/operational_rules.md §6 |
| ADR01-79 | Forbidden moves L166-167 | Do not move Striker DJ30 or NAS100 risk or pyramid in either direction without re-running MC against the lock criteria. | R14 abs |  |
| ADR01-80 | Forbidden moves L168 | If reverting, revert DJ30 risk/pyramid and NAS100 risk together to the documented baseline, never one strategy alone. | R14 det |  |
| ADR01-81 | Forbidden moves L169 | Do not skip the four quarterly time_to_pass --regime-check runs. | R28 DEL | Quarterly regime-check retired 2026-07-22 by claims-rescope Addendum (§D2); refresh-2 Addendum 2026-08-02 records harness raises ValueError. |
| ADR01-82 | Forbidden moves L170 | If a falsifier fires, close the ADR as SUPERSEDED-BY and open a fresh one; never amend gate criteria or thresholds mid-window or in place. | R23 abs |  |
| ADR01-83 | Open item 1 L249 | If a Pine parameter shift occurs without written motivation, trigger a methodology audit of silent parameter drift. | R14 DEL⚖ | Superseded by stricter AGENTS.md locked-parameter immutability and pine-manifest gate (core/strategies/MANIFEST.sha256) blocking silent Pine drift. |
| ADR01-84 | Addendum 2026-07-01 L321; Addendum 2026-08-02 L356 | Back-propagate retirement events to standing falsifiers, recording dormancy and re-arm conditions in dated addenda. | R28 abs |  |
| ADR01-85 | Addendum 2026-08-02 L383-384 | Judge a falsifier's reachability by running its instrument; a path-existence check can score a dark limb as reachable. | R28 det | → docs/operational_rules.md §11 |
| ADR01-86 | Addendum 2026-08-02 L485-490 | Do not re-run a regime gate whose answer is known or invent a pass-rate floor; the gate floor must equal the brief's full-panel floor. | R24 abs |  |
| ADR01-87 | Audit hooks L207-243; Verification L283-315 | Run the refresh-2 audit hooks: allocation, CSV-wiring and anchor-pin greps, the quarterly regime-check, and journal_review edge ratios. | R28 DEL | Hooks target deleted tests/test_mc_anchors.py and absent journal_review.py; portfolio_mc.py now a core/ facade. |

</details>

<details><summary><code>docs/adr/2026-06-04-lean-portfolio-meta-layer.md</code> — 11 rules: 2 absorbed, 0 detail, 9 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-88 | Discharge addendum (c) L15-18 | Re-arm the allocation meta-layer only if a producing edge-captured-ratio surface exists and an allocation decision cites it. | R28 DEL⚖ | Meta-layer falsifier fired 2026-07-30; ECR engine journal_review.py retired 2026-07-11 (absent); OODA fallback skill retired 2026-10-24. |
| ADR01-89 | Discharge addendum (d) L19-27 | Retain this ADR rather than delete it while the concept-admissibility and three-loop-binding ADRs cite it as parent doctrine. | R31 DEL⚖ | Conflicts with operational_rules §16: a citation alone is a dependency to resolve, not a retention entitlement; ADR retention is operator's call. |
| ADR01-90 | §2 L82-100 | Govern via a four-layer hierarchy whose Lean-Portfolio meta-layer allocates capital and attention across operational and development value streams. | R9 DEL | Discharge addendum 2026-08-14: own §4 falsifier fired 2026-07-30, CEREMONIAL; live hierarchy is 2026-06-12-three-loop-methodology-binding.md. |
| ADR01-91 | §4 L155-159; §6 L180-182 | Delete the meta-layer if, at eight weeks, no allocation decision cites realized ECR. | R28 DEL | Discharged: fired 2026-07-30 per discharge addendum 2026-08-14; meta-layer recorded dormant/ceremonial. |
| ADR01-92 | §2.4 L120; §5 #4 L168 | Label allocation changes projection-driven until a producing rolling ECR exists; never call them data-driven without it. | R15 DEL⚖ | Producing ECR engine journal_review.py retired 2026-07-11 and absent; meta-layer dormant by discharge addendum 2026-08-14. |
| ADR01-93 | §2.4 L122; §2.6 rule 1 L132; §6 L184-188; §5 #7 L171 | Trust an automated path with size only after per-strategy verification that it reproduces the backtest signal; pyramiders also need verified close logic. | R10 DEL⚖ | ECR/Copygram/DXTrade route retired; superseded by M1 RESOLVED, per-session GO and campaign Phase 8 shadow parity gate. |
| ADR01-94 | §2.6 rule 2 L134; §7 item 1 L198 | Run ECR now on manual trades as the control baseline the automated path must beat. | R10 DEL | Manual/CFD trading stopped by 2026-06-30-no-manual-trading-cfd-retirement.md; journal_review.py absent from tree. |
| ADR01-95 | §2.6 rule 3 L136; §5 #8 L172; §8 L208-217 | Decide kill-switch design (coded circuit-breaker vs human pause) consciously via an inqhiori Pre-Q before any automated path carries size. | R10 DEL⚖ | Q-KILLSWITCH never opened (only this ADR mentions it); c1 arming/disarm and per-session GO controls now govern. |
| ADR01-96 | §3 L144-147; §5 #1-#3 L165-167 | Confine SCRUM to the development stream: no sprint cadence or Definition of Done for trading; hold Daily Scrum only during active parallel build. | R36 DEL | No other repo doc mentions SCRUM; meta-layer CEREMONIAL-BY-OWN-FALSIFIER per discharge addendum 2026-08-14. |
| ADR01-97 | §2.3 L116; §5 #5-#6 L169-170 | Measure success by outcomes such as captured edge, never by outputs like ADRs authored or features shipped. | R36 abs |  |
| ADR01-98 | §0 L51, L63; §2.5 L124 | Rank provenance on-disk over web over memory; accept an ADR only on on-disk-confirmed anchors; never back-date notes or accept skill-encoded provenance. | R0 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-05-concept-admissibility.md</code> — 8 rules: 3 absorbed, 1 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR01-99 | Machinery-status L9; §2.1 L51 | Require each research concept to state an economic mechanism, not a backtest observation, before any data is mined. | R25 det |  |
| ADR01-100 | Machinery-status L10-11; §2 L55; §5 L98-99 | Before proposing, execute and paste a dedup search of docs/rejected_candidates.md by mechanism family and instrument, including LTM; route near-matches to human review. | R8 abs |  |
| ADR01-101 | §2 L49; §5 L97 | Admit a concept only with the six required fields and no parameter grid; the sweep finds parameters. | R25 DEL | Contract machinery deleted by 2026-07-11-gen1-pipeline-retirement.md; Machinery-status names only mechanism and dedup as surviving doctrine. |
| ADR01-102 | §2.2 L52 | Require concept falsifiers to be binary and observable, with condition and death markers and no unfalsifiable markers. | R28 DEL | scripts/check_concept.py deleted 2026-07-11 (gen1 retirement); binary falsifier form survives in scripts/check_brief.py. |
| ADR01-103 | §2.3 L53 | Require concepts to claim portfolio complementarity against the locked book, not standalone Sharpe. | R25 DEL | Concept machinery retired 2026-07-11 (gen1 retirement); parent pass-rate objective ceremonial per lean-portfolio discharge addendum. |
| ADR01-104 | §2 L55; §5 L94; §6 L113 | Never let a gate tune its own thresholds; change thresholds or markers only by reviewed commit, version bump and programme-audit. | R23 abs |  |
| ADR01-105 | §2 Scope L58; §3 L68; §5 L96 | Keep concept generation separate from gating; a generator must never gate its own output. | R25 abs |  |
| ADR01-106 | §4 L81-88 | Revisit and supersede the contract if no-signal, false-reject or repeated dedup mis-fire triggers occur after ten or more admitted concepts. | R28 DEL | Concept-intake machinery retired 2026-07-11 (gen1 retirement); no concepts flow through the gate, triggers cannot fire. |

</details>

<details><summary><code>docs/adr/2026-06-05-monorepo-layer-boundaries.md</code> — 18 rules: 3 absorbed, 13 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-1 | §2.1 L53 | Treat the repo as four mutability layers: core (locked sink), root-resident governance, lab (free churn), ops (operational); REPO_MAP.md maps every tracked path to one layer. | R37 det |  |
| ADR02-2 | §2.2 L81 | Never create import edges core→any internal layer, governance→lab/ops, or direct lab↔ops; only governance→core, lab/ops→core or governance, and same-layer edges are legal. | R37 det |  |
| ADR02-3 | §2.3 L87 | Keep check_boundaries an AST import scan in pre-commit and CI that hard-fails cross-layer module-name collisions, unresolved first-party and invalid relative imports; tests/ is exempt. | R37 det |  |
| ADR02-4 | §2.3 amend L95 | Dynamic imports and filesystem/path reads escape the scanner but not the layer contract; co-locate code with the state it reads instead of reading another layer's data. | R37 det |  |
| ADR02-5 | §2.3 amend 2026-09-17 L99 | Define layer maps (app prefixes, governance prefixes, scripts layer, flat import roots) only in scripts/repo_map_layers.yml; consumers load it and keep no mirror copies. | R39 det |  |
| ADR02-6 | §2.4 L106 | Scope the manifest gate to core/: any change under core/strategies/ requires a deliberate MANIFEST.sha256 regeneration; lab, ops and governance churn without manifest friction. | R19 det |  |
| ADR02-7 | §2.5 L110 | Keep no working-tree artifact that nothing live imports or references; archive closed loops to git history plus a tag, never in-tree 'just in case'. | R31 abs |  |
| ADR02-8 | §2.6 L114 | Keep always-loaded agent instruction files (CLAUDE.md, now AGENTS.md) current-state only; move historical narrative to dated history files, content-preserved, as a standing rule. | R34 abs |  |
| ADR02-9 | §2.7 L116 | Keep one monorepo; do not split into separate physical repos for tidiness unless a concrete need arises to publish one application layer without the other. | R37 det |  |
| ADR02-10 | §5 #1 L144 | Never relax the layer contract to green check_boundaries; treat an illegal edge as a finding and fix it by correct placement (widen shared code into core, reclassify). | R37 det |  |
| ADR02-11 | §5 #3 L146 | Never regenerate manifest hashes or anchor pins to clear a red gate after a move or edit that changed locked content; revert and investigate instead. | R19 det |  |
| ADR02-12 | §5 #6 L149 | Do not add a fifth layer or sub-layers (e.g. core/locked vs core/shared) unless a concrete import edge forces it. | R37 det |  |
| ADR02-13 | §5 #7 L150 | Resolve any new contested path's layer explicitly in REPO_MAP.md, holding it in a ?-tier until resolved; never default a layer seam silently by convenience. | R37 det |  |
| ADR02-14 | §5 #8 L151 | Do not trust grep to prove layer isolation; use the AST-aware boundary scan, which sees lazy and in-function imports. | R37 det |  |
| ADR02-15 | §6 L161 | Never amend gate, threshold, coverage or trigger criteria after seeing results or mid-window; change them only through a superseding, prospective decision. | R23 abs |  |
| ADR02-16 | §4 H3 L136 | At the second programme-audit cycle, check that the boundary gate fired or was referenced; if neither and layers drift, strengthen or delete the check. | R37 DEL | H3 limb (b) met: 2026-09-11/09-17 amendments cite check_boundaries; boundaries is tier: always in scripts/gates.yml. |
| ADR02-17 | §7 L169 | Execute Phase C by git mv: widen tv_export_loader to core, move codification/validate_candidate to lab, dedupe journal_review, evict archive/, prune CLAUDE.md; verify H1/H2. | R37 DEL | Phase C executed: archive/ absent and core/tv_export_loader.py present in the tree. |
| ADR02-18 | §8 Q-b L185 | Skills carry no importable code that depends on lab or ops; reference the canonical engine instead of bundling a duplicate copy. | R37 det |  |

</details>

<details><summary><code>docs/adr/2026-06-05-sweep-engine.md</code> — 9 rules: 4 absorbed, 2 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-19 | §2 L63 | Python or other re-implementations never gate deployment; only native TradingView Strategy Tester runs of the real Pine confirm a deployment-bound config, never skipped. | R24 det |  |
| ADR02-20 | §5 #5 L100 | Run any pre-filter and its confirming run on the same feed; a different feed reintroduces feed divergence. | R18 det |  |
| ADR02-21 | §5 #1 L96 | Report trial count N as every configuration examined, including cheap pre-filter grids, never the confirmed shortlist; DSR/PBO cross-trial variance uses the full search set. | R23 abs |  |
| ADR02-22 | §4 L84 | Before a pre-filter engine shortlists a new strategy family, show rank-order agreement (Spearman rho above floor) with native Pine; otherwise revert to native-only. | R24 DEL | Superseded by docs/methodology/prefilter_rank_correlation_gate.md (Gen-2 rank-rho invariant); lab/validation/sweep deleted by gen1-pipeline-retirement ADR. |
| ADR02-23 | §5 #6 L101 | Do not revive the in-Pine multi-config optimizer or native-only-as-sole-engine options without new evidence invalidating their recorded rejection reasons. | R26 DEL⚖ | Alternatives weighed for sweep machinery retired 2026-07-11; Python-as-sole covered by live doctrine; native-only is now the prefilter gate's fallback. |
| ADR02-24 | §6 sub-decision L126 | Never hand private Pine strategy logic or account access to a third-party optimizer; re-proposal requires a privacy/public-clone posture change, not a faster vendor. | R13 abs |  |
| ADR02-25 | §6 sub-decision L127 | Defer in-house Strategy Tester automation until manual native confirmation is a measured bottleneck, then open a follow-up ADR. | R24 DEL | Follow-up decided in docs/adr/2026-06-23-tv-backtest-egress-automation.md, which builds on this two-tier. |
| ADR02-26 | Add 2026-08-14 L201 | Record corrections to an accepted decision as dated addenda or header reader-intercepts on the owning ADR; leave the decision text byte-unchanged. | R30 abs |  |
| ADR02-27 | §0 L37 | Before flipping an ADR to Accepted, re-run its §0 anchor and §10 audit checks and check_brief.py --type adr; correct any anchor that no longer verifies. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-06-firm-constants-single-source.md</code> — 5 rules: 1 absorbed, 1 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-28 | §2 L41 | Declare each firm-rule constant once in its canonical core module (firm_rules / historical_challenge); consumers derive by import, never re-declare literals; select firms by explicit tier key. | R16 det |  |
| ADR02-29 | §2 L43 | Select the active firm through a module-level firm_rules.ACTIVE_FIRM selector feeding the derived constants. | R16 DEL | core/firm_rules.py docstring L8: ACTIVE_FIRM, FXIFY row and BASELINE_BALANCE deleted by challenge-era substrate retirement Phase 4. |
| ADR02-30 | §5 #1-2 L97 | When re-sourcing constants, keep public attribute names and units identical; gate on derived equals literal, full suite green and MC anchor reproducing. | R16 DEL | Re-sourcing procedure for the ACTIVE_FIRM derivation; that derivation deleted per firm_rules.py docstring and this ADR's Addendum 2026-08-29. |
| ADR02-31 | §5 #3 L99 | Keep each change to a P0 locked core module in its own isolated diff and lock cycle; never bundle it with refactors or another P0 change. | R14 DEL⚖ | Forbidden move scoped to this ADR's own derivation edit, deleted in Phase 4; AGENTS §Protection owns stricter frozen-control change-control. |
| ADR02-32 | §5 #4 L100 | Governance, methodology and refactor decisions never modify object-layer frozen controls (allocations, DD_TRIGGER/DD_SCALE, MC calibration, locked Pine) as a side effect. | R14 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-07-decompound-remc-hold.md</code> — 14 rules: 4 absorbed, 9 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-33 | §2 L42 | Hold the locked legacy book's allocations and DD protection unchanged; treat the pinned MC anchor as a benign-regime reference and the regime-dependent characterization as canonical risk. | R14 det |  |
| ADR02-34 | §5 b1 L89 | Never edit locked anchor pins or dd_protection/firm_rules constants to match re-MC figures; record the risk characterization in docs, not in pins. | R14 abs |  |
| ADR02-35 | §5 b2 L90 | Do not re-propose the gate-failed uniform de-risk or DD_SCALE-strengthening relocks without a new mechanism (e.g. regime-adaptive sizing) or materially different gate result. | R26 det |  |
| ADR02-36 | §5 b4 L92 | Do not narrow an accepted analysis window to make results look benign; changing the canonical window to dodge a finding is a silent relabel. | R23 abs |  |
| ADR02-37 | §4 L78 | HOLD limb 1: two or more drawdown-attributed challenge failures in a rolling six months falsify the HOLD; open a regime-adaptive sizing Pre-Q and apply the documented interim de-risk. | R28 det |  |
| ADR02-38 | §4 L79 / Add 2026-08-03 L277 | HOLD limb 2 (quarterly trailing-6-month regime re-MC) is SUSPENDED-ORPHANED: its schedule is struck, not deferred; thresholds stay unchanged. | R28 det |  |
| ADR02-39 | Add 2026-06-25 L199 | At the 2026-08-08 regime trigger, re-run h1_check on the clean vintage to test whether a practical regime-robust de-risk frontier exists. | R28 DEL | 2026-08-08 trigger struck by Addendum 2026-08-03 (limb 2 suspended); lab/analysis/regime/ harness directory absent. |
| ADR02-40 | Add 2026-07-01 L209 | When a retirement removes a standing falsifier's input, record on its owner that the limb is dormant or orphaned, with re-arm condition and surviving coverage. | R28 abs |  |
| ADR02-41 | Add 2026-08-03 §5 #1 L296 | Do not re-point an orphaned falsifier at different data under the same name; a check on new data is a new falsifier needing its own pre-registration and gate. | R28 det |  |
| ADR02-42 | Add 2026-08-03 §5 #2 L299 | Never treat NOT_EXECUTABLE or an absent re-MC as a pass; absence of a breach reading is not a non-breach. | R28 abs |  |
| ADR02-43 | Add 2026-08-03 §5 #4 L305 | Do not close a falsifier gap by deleting the falsifier; suspend it so the debt stays visible until a successor discharges it. | R28 det |  |
| ADR02-44 | Add 2026-08-03 §5 #5 L307 | Keep the regime-monitor successor's scope to discharging the orphaned limb and the owed forward monitor; do not let it quietly grow. | R28 det |  |
| ADR02-45 | Add 2026-08-03 §6 L311 | Lift the limb-2 suspension only by an explicit lift artifact once the pre-registered venue-native regime monitor gives a live-fill verdict; banner removal is not a lift. | R28 det |  |
| ADR02-46 | Add 2026-08-03 §6 L316 | If no live fill exists by the 2026-11-08 review, re-raise the HOLD's standing-unfalsifiable gap in that programme audit; never roll it forward silently. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-06-11-instrument-ledger-and-cfg-fingerprint.md</code> — 15 rules: 3 absorbed, 11 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-47 | §2a L45 | Any session deriving, testing, tuning or adjudicating on an instrument reads ops/instruments/<SYMBOL>.md before its first run or edit and appends a dated disposition at session end. | R27 abs |  |
| ADR02-48 | §2a L45 | Instrument ledgers carry active concepts/status, dead/parked items, durable findings, the instrument-level anti-SNAG budget shared across sessions, and open decisions; rows name owner-session anchors. | R27 det |  |
| ADR02-49 | §5 b1 L97 | Create an instrument ledger on the first session touching that instrument; never pre-emptively backfill ledgers for historical instruments without an operator GO. | R27 abs |  |
| ADR02-50 | §5 b2 L98 | Ledgers own instrument findings and concept status only; never restate strategy parameters or locked constants there, link to Pine, dd_protection or firm_rules. | R29 det |  |
| ADR02-51 | §2b L51 | Embed a cfg-ID tag in every active-derivation Pine strategy title, updated each run; reconcile Step-0 verifies the tag against the declared run. | R14 det |  |
| ADR02-52 | §5 b3 L99 | Never retro-tag frozen or pre-registered Pine scripts with a cfg fingerprint; they are immutable and identified by their pre-registration. | R14 det |  |
| ADR02-53 | §5 b4 L100 | Adopt the cfg fingerprint in existing active-derivation scripts only at their next legitimate edit; never make a convention-only touch that creates a phantom config generation. | R14 det |  |
| ADR02-54 | §2c L57 | No forward-validation WIP slot cap is in force; re-propose P2 only on evidence the missing cap binds, as a fidelity-based capacity cap with concurrency disclosure. | R36 abs |  |
| ADR02-55 | §5 b5 L101 | Apply the rejected-candidates new-mechanism-evidence bar to portfolio candidates only, not to declined process rules. | R26 det |  |
| ADR02-56 | §2c note L67 | Never buy forward-test throughput by shrinking n floors, escalating on strong interims, peeking or rotating tests mid-window, or early micro-allocation. | R23 det |  |
| ADR02-57 | §2c note L64 | Count mechanism replications as independent only across different price paths, not different feeds; give each its own registration and a pre-specified joint k-of-n reading. | R24 det | → .claude/skills/strategy-validation/SKILL.md (path-independence phrasing) |
| ADR02-58 | §2c note L61 | Record in each forward pre-registration or ledger entry how many forward tests ran concurrently, so confirmation counts read against the right denominator. | R23 DEL⚖ | Not in force: §2c records P2 not ratified 2026-06-11 and lists concurrency disclosure as part of any P2 re-proposal. |
| ADR02-59 | §4 L87 | At the 2026-11-08 review, if two or more ledgered-instrument sessions lack a same-date ledger disposition, add mechanical enforcement or withdraw the ledger rule. | R28 det |  |
| ADR02-60 | §4 L89 | If a fingerprint-class relay defect on a cfg-tagged export escapes Step-0 into analysis, tighten the convention (cfg-ID in export rows) or supersede it. | R28 det |  |
| ADR02-61 | §6 L111 / Add 2026-07-16 L214 | Attribute regimes using the single canonical regime calendar (USDCAD ledger §Regime calendar); verify [M]/[L]-tagged cells before consuming them as evidence. | R29 det |  |

</details>

<details><summary><code>docs/adr/2026-06-12-notion-surface-retirement.md</code> — 5 rules: 0 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-62 | §2 Phase 1 L38 | Treat Notion as frozen read-only: write no methodology, state, decisions or briefs there; repo and skills are the sole canon, memory carries pointers. | R29 det |  |
| ADR02-63 | §10 hook 4 L91 | Add no new live Notion dependencies or authority citations; cite repo paths via docs/governance/notion-redirect-map.md and the Phase-2 exports instead. | R29 det |  |
| ADR02-64 | §4 L61 | If a daily-ops tooling need re-emerges, rebuild it as a repo artifact or small app first; return to Notion only if that rebuild demonstrably fails. | R29 det |  |
| ADR02-65 | Add 2026-08-10 L137 | Never delete the Notion workspace or empty its trash as a substitute for archival; it stays cold-archived as the rollback reserve. | R31 det |  |
| ADR02-66 | §2 Phase 2 L40 | Migrate Notion residue by export (never from memory), commit a redirect map resolving every LEGACY-NOTION anchor, repoint entry docs, then decide Phase 3 at audit. | R31 DEL | Phase 2 DONE 2026-06-13, Phase 3 executed 2026-08-10 (status header); docs/governance/notion-redirect-map.md exists. |

</details>

<details><summary><code>docs/adr/2026-06-12-three-loop-methodology-binding.md</code> — 16 rules: 9 absorbed, 5 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-67 | §2 D1 L49 | Bind methodology to loop tier: STRATEGIC uses The Algorithm (should it exist), OUTER uses INQHIORI (is it true), INNER uses OODA (what now). | R9 det |  |
| ADR02-68 | §2 D2 L57 | Execute programme-, track- or instrument-tier Delete verdicts only as STRATEGIC-LoR acts: at programme-audit cadence, on a fired pre-registered stopping rule, or by named owner adjudication. | R3 det |  |
| ADR02-69 | §2 D2 L57 | Declare the Loop-of-Record and D-S-A domain on every D-S-A pass or decision artifact. | R9 abs |  |
| ADR02-70 | §2 D3 L59 | INNER or OUTER sessions may propose a Strategic Delete but never execute one on local momentum; route the proposal to a D2 channel. | R3 abs |  |
| ADR02-71 | §2 D4 L61 | Track add-back rate as two layer-segregated instruments (meta-layer rejected signals vs object-layer strategy deletes), never pooled; judge bands per instrument at its own audit. | R28 abs |  |
| ADR02-72 | §5 #6 L93 | Never let add-back calibration bands auto-trigger threshold changes; bands inform the programme audit, which decides. | R28 det | → docs/adr/2026-07-01-add-back-metric-layer-split.md §5 #4 |
| ADR02-73 | §2 D5 L63 | Treat the systematic trading lifecycle map as descriptive doctrine only; it names stages, loops and bridges but does not authorize new builds. | R3 abs |  |
| ADR02-74 | §2 D6 L65 | Source-of-truth order: repo is sole canon (ADRs, lifecycle doc, INQHIORI canon mirror); skills carry routing lines only; memory holds load-bearing edits with pointers. | R29 abs |  |
| ADR02-75 | §5 #1 L88 | Do not create a separate methodology skill for the three-loop framing; add routing lines to existing skills only. | R29 abs |  |
| ADR02-76 | §5 #2 L89 | Do not reclassify The Algorithm as a fourth loop; it is an operator whose passes run on all three loop clocks. | R9 det |  |
| ADR02-77 | §5 #3 L90 | Do not duplicate full decision prose across read surfaces; provenance lives in one place and other surfaces point to it. | R29 abs |  |
| ADR02-78 | §5 #4 L91 | Apply LoR and loop-binding declarations forward only; do not retro-backfill them onto closed briefs or ADRs without a separate owner decision. | R33 abs |  |
| ADR02-79 | §7 L113 | License Accelerate-tier builds only after Question, Delete and Simplify passes have run at the appropriate tier; never accelerate what should not exist. | R9 abs |  |
| ADR02-80 | §7 L114 | Programme audits check STRATEGIC-Delete declaration compliance and compute the add-back rate from kill records and registry entries. | R28 det | → .claude/skills/programme-audit/SKILL.md |
| ADR02-81 | §7 L116 | Every telemetry alert or report names its consuming loop and cadence. | R11 DEL⚖ | Plan T telemetry tied to Copygram/DXTrade estate retired 2026-07-11; lifecycle map row 4 keeps consumer-loop routing descriptively. |
| ADR02-82 | §4 L80 / §6 L106 | Graduate the loop binding PROPOSED to ACCEPTED at the first programme audit if Strategic Deletes carried STRATEGIC LoR and add-back was computable. | R9 DEL | Graduation fired: Ratification Note 2026-07-06 accepted D1-D3; D4 carried by add-back-metric-layer-split ADR. |

</details>

<details><summary><code>docs/adr/2026-06-12-tv-csv-canonical-feed-policy.md</code> — 9 rules: 5 absorbed, 3 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-83 | §2.1 L39 | Rest canonical analyses, verdicts, locks and registry entries only on TV CSV exports (now CME futures TV exports) or official non-bar series. | R18 abs |  |
| ADR02-84 | §2.2 L40 | Treat programmatic bar feeds and de-canonicalized symbols as staging only; never cite their results as canonical without TV verification, however close the numbers look. | R18 abs |  |
| ADR02-85 | §2.3 L41 | Retain bar-feed staging tooling (Dukascopy adapter, OANDA fetcher) and never delete it as dead under policy. | R18 DEL | Superseded by docs/adr/2026-06-17-dukascopy-retirement.md; core/lib/dukascopy.py and scripts/fetch_oanda_bars.py absent. |
| ADR02-86 | §2.4 L42 | Name the specific TV export or official series that any canonical artifact's price data comes from, as MC anchors name their panel CSVs. | R18 det |  |
| ADR02-87 | §4 #2 L53 | Never re-run a failed TV-based verdict on a bar feed to shop for a pass. | R18 abs |  |
| ADR02-88 | §4 #4 L54 | Keep firm-onboarding execution-feed equivalence under the LOCKED feed-equivalence spec; the canonical-analysis-feed policy does not govern it. | R18 abs |  |
| ADR02-89 | Add 2026-08-08 L13 | Revive any second data feed only through a pre-registered decision with independent cross-feed corroboration, never casually. | R18 det |  |
| ADR02-90 | Add 2026-09-01 L65 | core/data/bar_data/ is retained but frozen: no automated producer; new panels arrive only through explicit operator-supplied CME bar exports. | R19 abs |  |
| ADR02-91 | §3 L44 | Reopen the feed policy if an analysis class becomes impossible under it, a TV-sourced verdict fails because TV diverged from the execution feed, or TV export limits change materially. | R18 det |  |

</details>

<details><summary><code>docs/adr/2026-06-14-reject-usoil-rdm-spike-fader.md</code> — 2 rules: 2 absorbed, 0 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-92 | §6 L100 | Re-admit the USOIL short-only spike-fade concept only on a genuinely new entry mechanism, never a re-tune, subset slice or stop-geometry change; it may still be probed as exit/filter. | R26 abs |  |
| ADR02-93 | §5 L88-92 | Never rescue a placebo-failed concept by promoting a recent subset slice, widening stops post-hoc, or leaning on a kill-switch; protection cannot create edge. | R23 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-14-rejected-candidate-patterns.md</code> — 24 rules: 3 absorbed, 20 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-94 | §A L51 | Classify each rejection by primary class (edge-failure, portfolio-fit/tail, venue/cost-constraint, non-rediscovery/role-duplicate, expression-failure); the primary class's add-back governs re-entry. | R26 det |  |
| ADR02-95 | §A L57 | Edge-failure re-entry requires a genuinely new entry mechanism (distinct class); never a re-tune, subset or regime slice, or stop-geometry tweak. | R26 abs |  |
| ADR02-96 | §A L58 | Portfolio-fit/tail re-entry requires a validated counterbalance leg or an allocation change shown by re-MC not to worsen the prior bust rate. | R26 det |  |
| ADR02-97 | §A L59 / Add 2026-08-30 L250 | Venue/cost-constraint re-entry requires geometry clearing the cost-law pre-flight with margin from the realized stop, a shape clearing the failed limb, or a constraint-removing venue. | R26 det |  |
| ADR02-98 | §A L60 / §B L70 | Non-rediscovery/role-duplicate re-entry requires a differing mechanism or role; a signal rejected as entry is not a rediscovery when proposed as exit. | R26 det |  |
| ADR02-99 | Add 2026-08-30 L232 | Expression-failure re-entry requires a materially new expression class on a declared structural axis, its own contract, fresh K and holdout, citing prior failures; retunes never qualify. | R26 det |  |
| ADR02-100 | §B L64 | Keep rejection class separate from the dedup axes (mechanism, portfolio-fit, mechanism-by-role non-rediscovery); dedup screens before investigation, class governs re-entry. | R26 det |  |
| ADR02-101 | §C L76 | Re-admit a rejected candidate only by meeting its primary class's add-back; log ID, class, condition claimed and evidence; reject add-backs naming no condition without investigation. | R26 det |  |
| ADR02-102 | §D L82 | Give every new registry entry class, role_tested, falsifier_failed and addback_condition (role_tested and falsifier_failed mandatory), plus config_fingerprint where applicable. | R26 det |  |
| ADR02-103 | §5 b2 L127 | Keep the rejection registry additions-only: never rewrite or delete a prior entry to apply a new schema; new fields apply to new entries only. | R26 det | → docs/rejected_candidates.md (header, Additions only) |
| ADR02-104 | §5 b3 L128 | Graduate a candidate lesson to load-bearing only with a dated anchor and the E1/E2 bar (one incident over $3K or three firings in separate windows), never counterfactual alone. | R33 abs |  |
| ADR02-105 | §4 L116 | At programme audit, downgrade the taxonomy and supersede it via a fresh ADR if any new entry lacks mandatory fields or any candidate was re-admitted by re-tune. | R28 det |  |
| ADR02-106 | Add 2026-08-30 L234 | Persist each mechanism's N_expr (default 2) and running expression-attempt history on the same scope-routed row that owns its rejection entries. | R26 det |  |
| ADR02-107 | Add 2026-08-30 L236 | Each expression contract declares attempt k of N_expr and names every prior failed class; an omitted or contradicted count is integrity-invalid; never reset the ordinal. | R26 det |  |
| ADR02-108 | Add 2026-08-30 L240 | After N_expr expression failures with a passing discriminator, close the ladder; any further expression must differ from every failed class and needs operator ratification citing full history. | R26 det |  |
| ADR02-109 | Add 2026-08-30 L242 | Move a closed ladder to venue/cost only if a failure fired on a cost or geometry limb; never invent cost causes, count retunes as classes, or enlarge N_expr ad hoc. | R26 det |  |
| ADR02-110 | Add 2026-08-30 L247 | Change the generally applicable N_expr bound only by a prospective governing decision recorded under the selective ADR rule. | R26 det |  |
| ADR02-111 | Add 2026-08-30 L256 | Route confirm dispositions: MARKET-NULL to edge-failure, EXPRESSION-FAIL to expression-failure, pre-Explore cost/geometry kills to venue/cost marked 'priors-derived, no mechanism test run'. | R26 det |  |
| ADR02-112 | Add 2026-08-30 L261 | Give EVIDENCE-VOID and ROLE-BLOCKED no WHY entry: record them on the contract; a fresh campaign needs a fresh holdout; re-screen ROLE-BLOCKED only when scoped role state changes. | R26 det |  |
| ADR02-113 | Add 2026-08-30 L263 | After post-confirm VENUE-FAIL keep evidence status CONFIRMED and record the edition-axis failure separately; record CHANNEL-FAIL consequences on the channel's owner, not as a rejection. | R26 det |  |
| ADR02-114 | Add 2026-08-30 L266 | After choosing the WHY class, apply D3's scope router: instrument mechanisms to the instrument ledger, cross-instrument to rejected_candidates.md, methodology to rejected_signals.md; class never picks register. | R26 abs |  |
| ADR02-115 | Add 2026-08-30 L270 | Apply the WHY-routing map only to post-2026-08-30 confirm verdicts and frozen-candidate pre-Explore kills; never convert pre-contract intake dispositions into confirm verdicts. | R26 det |  |
| ADR02-116 | Add 2026-08-30 L273 | Do not treat a green check_instrument_rejection_coverage run as establishing the full WHY-routing map; its verdict parser is narrower and the ladder integrity check is unbuilt. | R21 det |  |
| ADR02-117 | §7 L160 | Extend feedback.py and SCHEMA.md so harness auto-appended registry entries emit the §D fields; optionally build check_registry.py to assert them. | R26 DEL | feedback.py/dedup.py deleted by docs/adr/2026-07-11-gen1-pipeline-retirement.md; lab/validation/concept_intake/ absent. |

</details>

<details><summary><code>docs/adr/2026-06-16-rule-2-budget-before-acting.md</code> — 24 rules: 5 absorbed, 15 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR02-118 | §2 D1 L48 | Before substantial work, declare an iteration budget scaled by loop class: INNER 3 (one self-extension with reason), OUTER 8, STRATEGIC 3 constituent OUTER investigations (no self-extension). | R2 det |  |
| ADR02-119 | Add 2026-10-24 L385 | Substantial work is any that creates or changes a decision artifact, runs research or spends, changes more than one file, or needs more than about ten tool calls. | R2 det |  |
| ADR02-120 | Add 2026-10-24 L394 | Routine fixes carry no budget: a change one check proves correct, a known-cause failing test, mechanical rename or regeneration, answering from reads, or a gated operator-directed operational act. | R2 det |  |
| ADR02-121 | Add 2026-10-24 L399 | Write the budget as one line where the work is recorded: 'Rule 2: <decision> · <class> <n> iterations', plus '· $<ceiling> · K=<n>' when spending; no new file or approval. | R2 det |  |
| ADR02-122 | §2 D1 L56 | The budget is a tripwire, not a wall: at the bound make a structured stop (spent, remaining, state, extend-or-stop with reversibility); never silently continue, finish, expand or weaken acceptance. | R2 det |  |
| ADR02-123 | §2 D1 L58 | On overrun, STOP if the work is recoverable; STOP and re-audit ground truth (the Rule-0 read was incomplete) if the work is irreversible. | R2 det |  |
| ADR02-124 | §2 D1 L63 | Never resolve budget exhaustion by shipping an under-validated irreversible change; exit only by re-audit on a new budget or escalation to the owner. | R2 det |  |
| ADR02-125 | §2 D1 L64 | Only INNER work may self-extend, once; OUTER and STRATEGIC extensions come only from owner adjudication or a re-audit, never self-granted. | R2 det |  |
| ADR02-126 | §2 D1 L65 | Scale every budget to the stakes; a flat budget is a Rule-0 violation in disguise. | R2 abs |  |
| ADR02-127 | §5.2 L99 | Never express a Rule 2 budget in minutes; count iterations, one attempt-and-check cycle in the task's natural unit. | R2 abs |  |
| ADR02-128 | §4 L86 / §5.3 L100 | Validate the 3/8/3 thresholds forward only; retrodiction may check tripwire timing but never tune thresholds; change them only on trip-log evidence at programme-audit cadence. | R2 det |  |
| ADR02-129 | §2 D3 L69 | Keep docs/notes/audits/rule-2-trip-log.md as one five-column table; log every trip from any work plus INQHIORI baselines; under-budget non-INQHIORI work writes no row. | R2 det |  |
| ADR02-130 | §5.6 L103 | Do not build Rule-2 telemetry (dashboard, logger, metrics module) beyond the single trip-log table, and never fabricate or backfill trip-log rows. | R2 det |  |
| ADR02-131 | §7 L125 | At each programme audit, read the Rule-2 trip-log, confirm at least one entry per active loop class or flag the rule inert, and judge whether trips were hindsight-correct. | R28 det | → docs/operational_rules.md §17 |
| ADR02-132 | §4 L92 | If the trip-log stays empty across two or more audit cycles, or the wire fires mostly at hindsight-productive moments, amend or delete Rule 2 at audit. | R2 det |  |
| ADR02-133 | §5.7 L104 | Never rename canon Rule 1 (small-cell variance prior) to free its numeral, including during the rule consolidation. | R1 abs |  |
| ADR02-134 | §5.8 L105 | Deconflict or renumber the 'Rule N' namespaces only within the 2026-10-24 rule consolidation; outside that STRATEGIC pass the deconfliction stays out of scope. | R29 det |  |
| ADR02-135 | §5.5 L102 | Change canon Rule 2 text (§15 statement, §12 pointer, §14 mirror) only through this ADR; where canon and ADR disagree, the ADR wins. | R29 abs |  |
| ADR02-136 | §5.1 L98 | Keep Rule 2 in its own ADR; do not fold it into the three-loop binding ADR. | R32 DEL⚖ | Authoring-time forbidden move discharged when Rule 2 landed in its own ADR 2026-06-16; future ADR consolidation governed by ceremony-tiering ADR. |
| ADR02-137 | Add 2026-08-21 L224 | Log an operator ratification against an unmet or adverse gate as an explicit override beside the honest gate result; never present it as the gate passing. | R21 abs |  |
| ADR02-138 | Add 2026-08-22 L240 | Do not apply or revive the withdrawn 2026-08-22 audit-cycle counting convention; author any needed convention fresh at the 2026-11-08 gate. | R2 det |  |
| ADR02-139 | §6 L118 | Graduate Rule 2 PROPOSED to ACCEPTED only at a programme audit with at least one hindsight-correct trip-log entry per active loop class; otherwise hold AMBIGUOUS. | R2 DEL | Moot: Rule 2 Accepted 2026-08-21 by operator override (status header, Addendum 2026-08-21; canon §15). |
| ADR02-140 | Add 2026-08-15 L172 | Instruct Rule-2 budget declaration only from INQHIORI-loop entry; remove the pointers from other always-on surfaces. | R2 DEL | Superseded by Addendum 2026-10-24 widening scope to all substantial work (canon §15 Scope line). |
| ADR02-141 | §6 L111 | Land Rule 2 with an insertion-only canon diff (§15, §12 pointer, §14 mirror), a created trip-log, and identical 3/8/3 magnitudes across all artifacts. | R2 DEL | Landed 2026-06-16: canon §15 and docs/notes/audits/rule-2-trip-log.md exist. |

</details>

<details><summary><code>docs/adr/2026-06-17-dukascopy-retirement.md</code> — 10 rules: 5 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-1 | §2 Decision L41 | Treat Dukascopy as retired for all bar acquisition; do not restore its adapter, fetcher or panels as a source. | R18 abs |  |
| ADR03-2 | §2 Decision L41 | Use core/bar_export_loader.py (BAR EXPORT v0.1) as the canonical producer of core/data/bar_data/<SYMBOL>_M15.csv. | R19 det | → core/data/bar_data/README.md |
| ADR03-3 | §4 Falsifier L63 | If a pre-registered deep-history FX/metals gate cannot be assembled from operator bar exports within one session, reopen the programmatic-feed question by superseding ADR. | R18 det |  |
| ADR03-4 | §4 Revert action L65 | Never edit an ADR's decision, falsifier or audit-hook body in place; record changes by dated addendum or a superseding ADR. | R32 abs |  |
| ADR03-5 | §5 Forbidden moves L73 | Never reintroduce a programmatic bar or broker feed (adapter, REST wrapper, --panel <broker> key) by convention; a new feed returns only via ADR or fresh Pre-Q. | R18 abs |  |
| ADR03-6 | §5 Forbidden moves L74 | Never cite retained cached bars from a retired feed (*_duka.csv, frozen OANDA CSVs) as canonical-fresh or to back a new verdict. | R18 DEL | Files gone: substrate-retirement Phase 5 deleted the *_duka.csv and OANDA CSVs (find returns none); retention clause superseded in both headers. |
| ADR03-7 | §5 Forbidden moves L75 | Never loosen a falsifier or revert trigger because meeting it proved tedious or uncomfortable; the inconvenience is the trigger, so supersede openly or hold. | R28 det |  |
| ADR03-8 | §5 Forbidden moves L76 | Re-propose a ruled-out alternative only with new mechanism evidence invalidating its stated reason, not renewed cost frustration or nostalgia. | R26 abs |  |
| ADR03-9 | §5 Forbidden moves L77 | Write only canonical <SYMBOL>_M15.csv files into core/data/bar_data/; never place producer intermediates (*_pep.csv, *.bars.csv) there. | R19 det | → core/data/bar_data/README.md |
| ADR03-10 | Addendum 2026-09-01 ruling L195 | Fix a stale downstream citation at its source file instead of adding a supersession edge when the later change never touched the ADR's decision. | R30 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-22-cost-geometry-pregate.md</code> — 7 rules: 2 absorbed, 3 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-11 | §2 + Addendum 2026-10-24 L160 | Before backtesting a new candidate entry mechanism, run scripts/cost_geometry_pregate.py at Phase 0 and record cost_R, its band and realized stop-in-ATR/sub-ATR flag. | R27 det |  |
| ADR03-12 | §2a L53 / §2c L57 | PASS only if cost_R is below the 0.05R ceiling; a FAIL blocks the backtest absent a stop-geometry or venue change. | R24 DEL | Superseded by Addendum 2026-10-24 (operator ruling, PR #900): 0.05R ceiling, --ceiling and blocking FAIL retired; report-only. |
| ADR03-13 | §2b L55 | Feed the cost gate the stop the strategy actually uses, from its realized geometry, never an assumed comfortable k·ATR; sub-ATR stops must be visible. | R27 det |  |
| ADR03-14 | §4 + Addendum L162 | At the 2026-11-08 sitting, judge whether Phase-0 cost_R recording surfaced every knowable cost-infeasible candidate; if not retire the obligation, keep the formula; under one candidate, carry AMBIGUOUS. | R28 det |  |
| ADR03-15 | §5 L91 | Source spread and ATR15m only from the canonical feed; a new execution feed must clear the feed-equivalence pre-flight first. | R18 abs |  |
| ADR03-16 | §5 L92-93 | Never treat a cost-gate PASS as edge validation, and never loosen --ceiling per candidate to manufacture a PASS. | R24 DEL | Lapsed per Addendum 2026-10-24 (§5 PASS/--ceiling moves lapse); "low cost_R is never edge evidence" survives in operational_rules §10. |
| ADR03-17 | §5 L94 | Never cite one feed's spread/ATR geometry as a proxy for another feed's; cost geometry is feed-specific. | R18 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-23-tv-backtest-egress-automation.md</code> — 10 rules: 1 absorbed, 6 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-18 | §2.1 L40 | Keep manual TradingView List-of-Trades export as the sanctioned default backtest egress. | R18 det |  |
| ADR03-19 | §2.2 L41 / §4 L74 | Use local reproduction (Path E) only for bar-close logic, with native TV export as parity ground truth; intrabar-dependent strategies keep native exports. | R18 det |  |
| ADR03-20 | §2.3 L42 / §3 L58 | Use native-CSV browser automation (Path A2) only as a fallback on a structurally isolated research account, at human cadence, never as a batch loop. | R18 DEL⚖ | Unreachable: second TV account forbidden (same ADR §5; tv-agent-browser-access §2.2), so no isolated account exists for Path A2. |
| ADR03-21 | §2.4 L43 | Use the undocumented TradingView WebSocket (Path B) only for forensic one-shot reads, never as a primary egress loop. | R10 det |  |
| ADR03-22 | §2.5 L44 / §5 L82 | Treat DOM-scrape (A1) and alert() backtest egress (C) as refuted; reopen only on new technical evidence such as a de-virtualized table or historical-bar alerts. | R26 det |  |
| ADR03-23 | §5 L80 | Never run any TradingView automation (browser, WebSocket, desktop) on the live-edge account; isolation is structural, and a second TV account stays forbidden. | R10 det |  |
| ADR03-24 | §5 L81 | Never loosen the parity band or rank floor to force a Path-E pass; a parity failure is the finding. | R24 DEL | Path-E parity harness deleted (gen1 retirement Phase 2; lab/validation/sweep absent); frozen invariant now owned by prefilter_rank_correlation_gate.md. |
| ADR03-25 | §5 L83 | Never circumvent a browser or MCP safety allowlist to reach TradingView; a refusal is an answer, not an obstacle. | R3 det |  |
| ADR03-26 | §5 L84 / §3 L59 | Never upload private Pine to any third-party compiler or optimizer; only a DIY local runtime port is acceptable. | R13 abs |  |
| ADR03-27 | Addendum 2026-07-27 L172 | Anyone extending §5's automation ban to page-level reads must state that they are extending it. | R10 DEL | Superseded: tv-agent-browser-access 2026-07-27 authorizes page-level reads, so no read ban remains to extend. |

</details>

<details><summary><code>docs/adr/2026-06-24-oanda-retirement.md</code> — 5 rules: 2 absorbed, 2 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-28 | §2 Decision L41 | Treat OANDA (REST API, creds, bar fetcher, --from-oanda, --panel oanda) as fully retired; do not restore it. | R18 abs |  |
| ADR03-29 | §2(b) L41 / header L6 | Treat Pepperstone/TV BAR EXPORT as the sole canonical feed. | R18 DEL | Superseded by 2026-08-02 Pepperstone feed retirement (OANDA ADR Superseded-in-part-by header); canonical family is CME TV exports. |
| ADR03-30 | §2(d) L41 | Validate on a single canonical feed tier; never run a two-tier proxy-drives-Action / other-feed-validates methodology. | R18 det |  |
| ADR03-31 | §4 Falsifier L63 | If a pre-registered lock or allocation decision needs independent second-feed corroboration that cannot run, reopen the single-feed posture by superseding ADR. | R18 det |  |
| ADR03-32 | §5 L77 | Never overwrite the canonical MC anchor with a number derived from a non-canonical feed; keep any frozen overlay labeled historical. | R14 abs |  |

</details>

<details><summary><code>docs/adr/2026-06-30-no-manual-trading-cfd-retirement.md</code> — 7 rules: 1 absorbed, 2 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-33 | §2.1 L43 | No manual discretionary execution on the live edge: trade only through an automated chain or not at all; there is no recovery exception. | R10 det |  |
| ADR03-34 | §2.2 L44 / Addendum 2026-07-10 L201 | CFD venue retired; FXIFY account formally closed and DXTrade credentials removed. | R16 DEL | Discharged: Addendum 2026-07-10 records FXIFY formally closed and DXTrade credentials removed; any reopen runs through §4. |
| ADR03-35 | §4 trigger 1 L68 / §5 L93 | Do not reopen MT4/MT5 hosting or CFD/FXIFY automation without a jurisdiction/entity change or a demonstrated end-to-end US-legal automated path, via fresh ADR. | R16 det |  |
| ADR03-36 | §4 trigger 2 L69 | Reconsider manual execution only on a clean edge-captured ratio of at least 80% over six-plus weeks of system-faithful execution, never to recover P&L. | R10 DEL⚖ | Unreachable: journal_review.py deleted with ops/live_journal 2026-07-11 (absent; 2026-08-02 note); directed orders now under AGENTS.md 2026-09-30 amendment. |
| ADR03-37 | §5 L92 | Never log back into the idle FXIFY/DXTrade account to trade it discretionarily. | R10 DEL⚖ | Superseded by stricter Addendum 2026-07-10: account closed, credentials removed (enforced by construction); §2.1 no-manual rule remains. |
| ADR03-38 | §5 L94 | Futures re-mapping is sizing translation only; it must not change any locked SL/TP/ATR/risk%/pyramid/session constant; any change is a separate lock decision with re-MC. | R14 abs |  |
| ADR03-39 | §10 L155-163 | Weekly, download the idle DXTrade fills export and run zero_fills_attestation.py; any in-window fill is a no-manual breach. | R10 DEL⚖ | Retired by Addendum 2026-07-10 item 3 (account closed); ops/live_journal tooling absent from tree. |

</details>

<details><summary><code>docs/adr/2026-07-01-add-back-metric-layer-split.md</code> — 11 rules: 3 absorbed, 6 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-40 | §2 D1 L47 | Compute add-back as two layer-segregated rates: meta-layer from rejected_signals.md, object-layer from rejected_candidates.md; report side by side, never pooled. | R28 det |  |
| ADR03-41 | §2 D1 L49 | Review governance-surface Delete reversals (retired surface or hook restored) qualitatively via their own ADR falsifiers; never add them to the meta-layer rate. | R28 det |  |
| ADR03-42 | §2 D2 L52 | Methodology audits cite only the meta-layer rate and portfolio audits only the object-layer rate; any cross-layer citation is disqualifying contamination. | R28 det |  |
| ADR03-43 | §2 D3 L54 | Judge each add-back rate against the ~10% interpretation bands separately, within its own layer's audit. | R28 det |  |
| ADR03-44 | §2 D4 L56 | Use Guardian Silver only as the object-layer add-back anchor; never in meta-layer statements. | R28 DEL⚖ | Stale anchor: three-loop ADR hook #6 records Silver admission reversed 2026-07-01 (object rate 0/1); cross-layer ban carried by D2. |
| ADR03-45 | §4 Falsifier L77 | If the two registries prove indistinguishable over two audit cycles, supersede and restore the pooled metric; never silently retain ceremony. | R28 det |  |
| ADR03-46 | §5 #3 L85 | Never amend a canon calibration metric definition in place without an ADR of record. | R32 abs |  |
| ADR03-47 | §5 #4 L86 | Bands inform the audit; never let an add-back band auto-tune a governance threshold. | R28 abs |  |
| ADR03-48 | §5 #5 L87 | Do not edit rejected_candidates.md addback_condition fields or the per-candidate §C gate under this ADR. | R3 DEL | Scope disclaimer; AGENTS.md §Output efficiency bars "no X granted" disclaimers because a ruling grants only what it states. |
| ADR03-49 | Addendum 2026-08-21 L187 | Record an operator ratification over an unmet gate as an override, logging the gate result honestly beside it, never as the bar being met. | R21 abs |  |
| ADR03-50 | Addendum 2026-08-21 L193 | Programme audits keep running the add-back computation on cadence; the 2026-11-08 quarterly owes its first real run. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-07-01-guardian-pyport-public-tracking.md</code> — 10 rules: 3 absorbed, 3 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-51 | §2.1-2.2, §2.5 L51-55 | Untrack the Guardian signal port and its test, hash-pin them, and keep generic engine/driver files tracked. | R13 DEL⚖ | Discharged: .gitignore L137-144 untracks both files; pine-manifest checks PORT_MANIFEST; AGENTS.md §Public-clone posture is the live rule. |
| ADR03-52 | §2.3 L53 / §5 L86 | Never purge or force-rewrite public git history to clean up a disclosure. | R13 det |  |
| ADR03-53 | §2.4 L54 | Land new Python/MQL5/other-language ports of locked strategy logic gitignored and hash-pinned by default, never tracked; prior leakage is no licence. | R13 abs |  |
| ADR03-54 | §2.6 L56 / §5 L88 | Leave the parameter-transcription class (LOCK.md blocks, specs) to the operator's Forward decision; do not redact it unilaterally. | R13 DEL⚖ | Superseded by 2026-08-14 repo-public-visibility-transition ADR: §2.6 Forward question resolved toward redaction. |
| ADR03-55 | §4 L78 | If a port's local copy is lost or unverifiable, revert to tracked-with-exception; after two tracked-port incidents, escalate to a mechanical port-manifest gate. | R13 DEL⚖ | Revert-to-tracked conflicts with stricter AGENTS.md §Public-clone posture; escalation branch done (check_pine_manifest.py covers PORT_MANIFEST). |
| ADR03-56 | §5 L87 | Never present untracking or removal as having closed a disclosure; claim only reduced amplification. | R13 det |  |
| ADR03-57 | §5 L90 | Never register a .gitignore narrow exception re-tracking a locked-strategy port without re-running the disclosure calculus. | R13 abs |  |
| ADR03-58 | §6 Risks L107 | When legitimately editing a hash-pinned port, re-pin its manifest in the same change. | R13 det | → scripts/check_pine_manifest.py |
| ADR03-59 | Addendum 2026-07-01 L188 | Do not cite 'public since 2026-06-23' as fact without the audit-log timeline. | R0 DEL | Historical: dc07898 no longer resolves (git cat-file fails after 2026-08-14 transplant); 2026-08-29 decay audit marks it historical-only. |
| ADR03-60 | Addendum 2026-08-29 L239 | Retrieve pre-transplant commits (e.g. dc07898) from the private first-passage-archive repo. | R31 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-06-bust-day-maxdd-inclusion.md</code> — 10 rules: 1 absorbed, 8 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-61 | §2 Decision L36 | Fold the breach day's drawdown-from-peak into max_dd before every bust return in the MC path simulator. | R20 det |  |
| ADR03-62 | §2 Gate-coupling L41 | Treat bust rate at or above 1% as implying p99 DD at or above 5%; the p99 gate is independently informative only below 1% bust. | R20 det |  |
| ADR03-63 | §4 Falsifier L71 | When bust rate is at least 1%, never read p99 DD as an independent criterion; treat the bust gate as primary and report survivor-only p99 as diagnostic. | R24 det |  |
| ADR03-64 | §4 L71-73 | If that coupling case recurs on two consecutive quarterly regime checks, supersede with pooled plus survivor-only quantiles; never silently revert breach-day inclusion. | R28 det |  |
| ADR03-65 | §5 L81 | Never widen the MC anchor test tolerance to absorb semantic drift; a pin breach takes the full re-run plus ADR path. | R14 abs |  |
| ADR03-66 | §5 L82 | Do not 'fix' the bust_inactivity return for symmetry; it is zero-effect churn on a locked file. | R20 DEL | Moot: core/mc/simulation.py updates max_dd (L520) before the bust_inactivity return (L559), per Addendum 2026-08-29. |
| ADR03-67 | §5 L83 | Do not unify drawdown definitions: static-from-start, peak-to-trough and %-of-notional are intentionally distinct semantics. | R16 det |  |
| ADR03-68 | §5 L84 / §3 L65 | Never retro-edit published historical RESULTS or p99 figures; caveat them once in docs/mc_anchor_history.md. | R20 det | → docs/mc_anchor_history.md |
| ADR03-69 | §6 L96 / §10 L143 | Footnote the 2026-07-06 semantic correction whenever new MC output is compared with pre-2026-07-06 published figures. | R20 det | → docs/mc_anchor_history.md |
| ADR03-70 | Addendum 2026-08-29 L205 | Audit the bust-day hoist in core/mc/simulation.py, not the core/portfolio_mc.py facade. | R0 det |  |

</details>

<details><summary><code>docs/adr/2026-07-10-databento-research-stack.md</code> — 22 rules: 5 absorbed, 10 detail, 7 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-71 | Header L3 / Addendum 2026-09-10 L266 | Databento is retired: never connect, pull, estimate, renew or infer access from SDKs, scripts, old credentials or earlier GOs; no replacement source is approved. | R18 det |  |
| ADR03-72 | §2 Decision L46 | Adopt Databento GLBX.MDP3 as the canonical futures-research data layer. | R18 DEL | Superseded by operator retirement, Addendum 2026-09-10 (header: Databento retired, no replacement approved). |
| ADR03-73 | §2 L52/L61 / §5 L99 | Precede every Databento pull with a free estimate; pulls refuse above --max-cost; no exceptions for small pulls. | R18 DEL⚖ | Superseded by stricter Addendum 2026-09-10 (no pulls or estimates at all); dormant spend control should Databento return. |
| ADR03-74 | §2 L53 / §5 L97 | Register the trial count K with register_search.py open before running any discovery tool; never take an informal peek first. | R23 det | → .claude/skills/futures-anomaly-discovery/SKILL.md |
| ADR03-75 | §2 L53 | Treat discovery-tool outputs as observations, not signals; the discovery layer never promotes a candidate. | R25 abs |  |
| ADR03-76 | §2 L54 | Apply universe-level correction (SPA/StepM/MCS, DSR, PBO/CPCV) using the ledger's K, in addition to, never replacing, within-panel validation protocols. | R24 det | → .claude/skills/strategy-validation/SKILL.md §8 |
| ADR03-77 | §2 L55 / §5 L96 | Keep Nautilus and all research code research-only; never wire any research component toward live execution or order placement. | R18 abs |  |
| ADR03-78 | §2 L57 / §5 L100 | Keep research dependencies in the pinned requirements-research.txt venv; never add them to pyproject.toml or install them into the ops environment. | R22 det | → requirements-research.txt |
| ADR03-79 | §2 L59 Live-rail verdict | Keep the TV-CrossTrade-NT8-Bulenox rail; reopen Nautilus-as-execution only if the operation leaves the prop-firm model for a direct-API broker. | R11 DEL⚖ | Superseded in part by S1/S2 ADRs (header); Addendum 2026-08-29 calls the rail falsifier moot; §5 keeps Nautilus research-only. |
| ADR03-80 | §3 L77 / Addendum L212 | Use vetted libraries (arch, skfolio) for SPA/StepM/MCS/PBO/CPCV; hand-write only the closed-form DSR; never re-implement those methods. | R24 det | → .claude/skills/strategy-validation/SKILL.md §8 |
| ADR03-81 | §4 uselessness L84 | If by 2027-01-10 no closed register_search manifest has fed the universe-level gate, archive the stack and retire the venv via superseding ADR. | R28 det |  |
| ADR03-82 | §4 cost-gate breach L86 | Any Databento billing without a recorded estimate, or any pull over $25 without operator sign-off, freezes pulls and forces an audit. | R18 DEL⚖ | Superseded by Addendum 2026-09-10: Databento retired, no pulls exist to breach; dormant billing control should the vendor return. |
| ADR03-83 | §5 L98 | Pull MBO/MBP-10 depth only after a bar-level candidate survives; the schema ladder is binding. | R18 DEL | Superseded by Addendum 2026-09-10: Databento retired; the MBO/MBP-10 schema ladder was provider-specific; no depth source approved. |
| ADR03-84 | §5 L101 | Never treat a parent-contract (ES/NQ/YM/GC) result as micro-validated; require the 1:10 economics re-scale and native-micro 2019+ OOS gate. | R24 det | → .claude/skills/futures-anomaly-discovery/reference/proxy-discipline.md |
| ADR03-85 | §5 L102 / Addendum L188 | Integrate delivered skills as-is; route any post-integration amendment through the normal skill-authoring path with its own review. | R6 DEL | Discharged: integration landed 2026-07-10; databento-data skill retired; later amendments follow the standard PR and review path. |
| ADR03-86 | §5 L103 | Never hardcode, print or commit DATABENTO_API_KEY; reference it by environment variable only. | R12 abs |  |
| ADR03-87 | §6 Risks L120 | Do not build the JPY-micro FX lane before resolving the M6J vs MJY quote-inversion question; it is a named red-flag stop. | R24 DEL | Discharged: resolved 2026-07-20 (Q-BOOKFIT-1): MJY, no inversion; recorded in proxy-discipline.md §FX/JPY and ops/instruments/MJY.md M4. |
| ADR03-88 | Addendum 2026-07-11 L190 | Write discovery manifests to the committed repo-root discovery_manifests/ (DISCOVERY_LEDGER override allowed). | R23 det | → discovery_manifests/README.md |
| ADR03-89 | Addendum 2026-07-11 L202-215 | Keep canonical Gen-2 research Python under lab/; skill scripts are thin launchers that must not import lab packages and forward via PYTHONPATH=lab. | R37 abs |  |
| ADR03-90 | Addendum 2026-08-29 L261 | Read the current live rail from ops/c1_rail/__init__.py and the S1/S2 ADRs, not from this ADR's §2/§4 text. | R30 abs |  |
| ADR03-91 | Addendum 2026-09-10 L268 | Treat retained vendor data, tooling and results as historical records; Databento retirement grants no new right to use retained vendor data. | R18 det |  |
| ADR03-92 | Addendum 2026-09-10 L270 | Qualifying controlled replay instead of the specified live feed for M1 item 5 needs an explicit acceptance amendment; retirement approves no substitute nor weakens the no-arm gate. | R10 det |  |

</details>

<details><summary><code>docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md</code> — 8 rules: 3 absorbed, 2 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-93 | §2.1 L43 | Do not deploy the locked four-strategy book as a futures-prop fan-out; P0-P5 gate ADRs and the Bulenox config are provenance, not live targets. | R14 abs |  |
| ADR03-94 | §2.2 L44 / §5 L81 | Self-funded Aegis-to-M6J is the sole active scale lane; its lane authorization is not a live-start authorization. | R15 DEL⚖ | Superseded by 2026-07-16 self-funded-lane-close ADR (lane closed, b1 PARK), stricter than the lane authorization. |
| ADR03-95 | §2.3 L45 / §5 L82 | Keep Guardian-MGC parked; un-parking or re-ranking scale lanes is a fresh recorded operator decision, never drift. | R26 DEL | Superseded by docs/pursuits/b8-guardian-mgc-transfer-lane.md SUBTRACT DEAD(N-SURV) 2026-08-11; repoint its §2.3 citation. |
| ADR03-96 | §4 Falsifier L68 | Reopen the futures-prop path for the locked book only on new dated pre-registered evidence of at least 0.8x edge preservation under realistic costs. | R26 det |  |
| ADR03-97 | §5 L78 / §3 L57 | Never re-run a spent, operator-accepted one-shot gate on a shifted grid or window to overturn its verdict. | R23 abs |  |
| ADR03-98 | §5 L79 | Never relabel a NO-GO as GO-CONDITIONAL when the named blocker is the test that failed. | R24 det |  |
| ADR03-99 | §5 L80 | Do not stand up the CrossTrade/NinjaTrader-8/Rithmic rail for a closed book. | R11 DEL⚖ | Superseded by rail GO 2026-07-17 (R6 Addendum 2026-09-01); closed-book deployment barred by AGENTS.md §Strategy Reference. |
| ADR03-100 | Addenda 2026-09-01 L184/L196 | Strike an audit hook whose tested premise a later ADR retired; do not redirect it to keep re-asserting a premise the ADR no longer controls. | R28 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md</code> — 26 rules: 5 absorbed, 19 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR03-101 | §2 Meta-decision L51-53 | Keep two orthogonal axes: LOCKED means immutable parameters and Pine; capital authorization is a separate, always-revocable lifecycle axis. | R15 abs |  |
| ADR03-102 | §2 L54 / Status vocabulary L167-172 | Describe strategies by CANDIDATE/AUTHORIZED/WATCH-1/WATCH-2/RETIRED plus MECHANISM or SURVIVAL-ONLY tag, as '<version> · LOCKED · <authorization> · <durability>'. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-103 | §2 L54 | A lifecycle de-risk only reduces size, so a WATCH-active book needs no re-MC. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-104 | §2 L56 | Compose the lifecycle axis with dd_protection and Closed/Action/Forward observation routing; it replaces neither. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-105 | Call 1 L64-71 | Demote one tier when rolling live PF stays below baseline minus the ratified sigma for the ratified consecutive review windows; the action is de-risk, never kill. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-106 | Call 1 L73 / §6 L228 / Addendum 2026-09-01 L361 | With too few live trades, treat Call-1 floors as provisional (AMBIGUOUS) and re-confirm them on the quarterly cadence in programme-audit notes, recorded not silently amended. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-107 | Call 2 L81 | Use stepped authorization tiers, never a smooth size=f(confidence) curve; every size change is an explicit logged tier change. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-108 | Call 2 L88-107 | Apply the lifecycle multiplier at the risk_pct layer, multiplicative with DD_SCALE, using the ratified tier ladder. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-109 | Call 2 L96 / §4 trigger 3 L198 / §5 L215 | The lifecycle factor multiplies against BASE_RISK/DD_SCALE/DD_TRIGGER without altering them or any LOCKED parameter; any bleed is an immediate stop-and-fix. | R14 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-110 | Call 2 L96 / §0 L19 | Size always rounds down, never up. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-111 | Call 3 L118-120 | SURVIVAL-ONLY strategies start one tier down, promote only after a pre-registered OOS interval and minimum live trades, face faster review and a one-window trigger. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-112 | Call 3 L122 | Enter unexplained signals minted by the discovery stack as SURVIVAL-ONLY by default. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-113 | Call 4 L133-134 | When the ratified soft-flag count of legs is in WATCH, pull review forward and run beta cohesion; at the act count, de-risk portfolio-wide and raise operator GO/NO-GO. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-114 | Call 5 L149 | Reversible de-risk (tier demotions, Call-1 firings, Call-4 soft flag and beta de-risk) fires by rule without fresh operator judgment. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-115 | Call 5 L150 | WATCH-2 to RETIRED and full shared-beta shutdown require operator GO/NO-GO verifying pre-registered criteria. | R15 abs |  |
| ADR03-116 | Call 5 L151 / §5 L213 | Automation moves authorization down only: never promote a tier, re-enter RETIRED, size above tier or re-optimize, except the bounded S5 sandbox lane. | R15 abs |  |
| ADR03-117 | Call 5 Addendum 2026-08-07 L161 | Automation may admit a gate-validated candidate to a capped sandbox only when S5 validator and refuter pass; operator approves budgets, not candidates; ceiling crossings operator-only. | R15 det | → docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md |
| ADR03-118 | Status vocabulary L167 / §7 L239 | Treat docs/methodology/strategy_lifecycle.md as canonical owner of the axes, ladder, durability regimes and ratified values; read multipliers from core/lifecycle.py. | R15 abs |  |
| ADR03-119 | §4 Falsifier L196-197 | Supersede to recalibrate or revert if two cycles show Type-I dominance (clipping live edges) or an unforeseen sustained collapse occurs with no prior WATCH. | R28 det |  |
| ADR03-120 | §5 L210 | Decay never triggers re-optimization: retire rather than re-fit; any replacement is a new hypothesis with fresh K accounting and fresh out-of-sample. | R15 abs |  |
| ADR03-121 | §5 L211 | Lock decay and kill thresholds at authorization; never move a live revocation line, even when a strategy approaches it. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-122 | §5 L212 | Surveil on schedule against pre-set criteria; only hold, de-risk one tier or retire, with no in-the-moment threshold edits or invented options. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-123 | §6 gate item 3 L224 / §10 hook 6 | Carry standing STATE.md forward-board bullets for per-strategy decay review and beta-death review. | R34 DEL | Retired by operator ruling 2026-09-01 (option b): quarterly programme-audit notes replace the STATE forward-board bullets. |
| ADR03-124 | §7 L241 Addendum C20 / §10 hook 1 | Cite the dd_protection spec-pin by its literal guard text, never by line number, so audit hooks cannot go stale. | R14 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-125 | §7 L241 / status 2026-07-17 | For pyramided legs, realize WATCH haircuts at the quantity layer, not by scaling the TradingView risk% input. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR03-126 | §7 Scope note L244 | Build the per-leg tier state machine only when the first SURVIVAL-ONLY addition needs it; ship the beta monitor and neutral hook first. | R15 DEL | Discharged: beta monitor and neutral hook shipped 2026-07-10; core/lifecycle.py L141-175 holds Call-1 transitions; lifecycle.md L126 restates the note. |

</details>

<details><summary><code>docs/adr/2026-07-11-challenge-era-claims-rescope.md</code> — 17 rules: 11 absorbed, 0 detail, 6 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-1 | §2.1 L45 | Treat the challenge-era MC anchor triple and its lock gates as historical calibration and engine-regression pins; never quote them as a live pass-probability or acceptance claim. | R20 abs |  |
| ADR04-2 | §2.1 L45 | Read a legacy 'AUTHORIZED @ 1.00x' status as eligibility only; every venue must still pass its own transfer and go-live gates. | R15 abs |  |
| ADR04-3 | §2.2 L46 | Run the quarterly C2-to-C0 revert check only as a historical-semantics diagnostic until D2 is resolved. | R14 DEL⚖ | Retired by this ADR's Addendum 2026-07-22; stricter live owner is the dd-protection concept-not-constant pre-reg→re-MC→both-halves→ADR chain. |
| ADR04-4 | §2.3 L47 | Onboard a firm only after an engine-support pre-flight; a firm configuration entry alone does not prove downstream engines support it. | R16 abs |  |
| ADR04-5 | §2.3 L47 | Retain the multi-firm prop multiplier tooling and ACTIVE_FIRM=FXIFY as dormant-historical fixtures. | R31 DEL⚖ | ops/accounts.py, ops/fxify_rule_validator.py absent; firm_rules asserts no ACTIVE_FIRM; Addendum 2026-09-01 left this clause's disposition to the operator. |
| ADR04-6 | §2 Kept L50 | Retire only what is no longer needed; keep materially useful substrate (locks, Pine, manifests, protection mechanism, lifecycle, MC engine, rejection bars). 'Historical' does not mean 'safe to delete'. | R31 abs |  |
| ADR04-7 | §4 Revert trigger L73 | When a challenge-class venue re-enters, the re-arming ADR commissions a fresh re-MC under that venue's rules; never revive the historical anchor as a live number. | R16 abs |  |
| ADR04-8 | §4 Completion falsifier L75 | Pre-register a successor self-funded risk-framework Pre-Q by 2026-11-08; otherwise D1 becomes a mandatory blocker on go-live. | R28 DEL | Discharged 2026-07-15 per this ADR's Addendum: Q-SFRISK-1 RESOLVED, admitting ADR 2026-07-15-sfrisk-1 Accepted. |
| ADR04-9 | §4 Revert action L77 | Change an accepted ADR's decision or falsifier only through a superseding ADR or dated addendum; never edit its Decision or Falsifier text in place. | R32 abs |  |
| ADR04-10 | §5 L85 | Do not edit dd_protection constants, its banner or executable lines as a side effect of a docs or claims change; the constants are frozen and re-MC-gated. | R14 abs |  |
| ADR04-11 | §5 L86 | Do not delete or weaken the anchor test pins or the lock-criteria test; keep them as engine-regression pins. | R14 DEL⚖ | tests/core/test_mc_anchors.py absent; AGENTS.md names vendor-free successor tests/core/test_mc_synthetic_engine.py; frozen-MC-adjacent, so operator call. |
| ADR04-12 | §5 L87 | Do not treat venue retirement as new mechanism evidence; it licenses no reopening of rejected candidates and no re-optimization. | R26 abs |  |
| ADR04-13 | §5 L88 | Do not switch ACTIVE_FIRM or patch the daily_loss_pct None crash without a firm-onboarding ADR. | R16 DEL | ACTIVE_FIRM deleted (tests/core/test_firm_constants_single_source.py asserts absence); preflight None-tolerant; firm onboarding owned by Rule 16. |
| ADR04-14 | §5 L89 | Freeze the question set before running any successor-semantics MC numbers; numbers-before-question is forbidden. | R23 abs |  |
| ADR04-15 | §5 L90 | Do not quote the 2026-08-08 historical-semantics diagnostic output as a live pass-probability. | R20 DEL⚖ | Diagnostic retired by Addendum 2026-07-22 (2026-08-08 carries no run); §2.1 and Rule 20 already bar quoting anchors as live. |
| ADR04-16 | Addendum 2026-08-02 L240 | When a retirement darkens a standing falsifier limb on any in-force ADR, record that limb's dormancy, grounds and re-arm condition on that ADR. | R28 abs |  |
| ADR04-17 | Addendum 2026-09-01 L282 | Declare every partial supersession reciprocally in the superseded ADR's Superseded-in-part-by header; undeclared edges are invisible to the ADR-graph check. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md</code> — 10 rules: 1 absorbed, 8 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-18 | §2 Inheritance L51 | Have each discovery campaign brief inherit the ratified Campaign defaults by reference to the template, without re-ratifying them. | R23 det |  |
| ADR04-19 | §2 Inheritance, §5 L51 | Override a campaign default only by stating the override and its reason in that campaign's committed, pre-result §8 pre-registration. | R23 det |  |
| ADR04-20 | §4, §5 L74 | Never edit a ratified campaign default in place; change it only by a superseding ADR that re-baselines it and names the affected campaign verdicts. | R23 det |  |
| ADR04-21 | §5 L88 | Do not restate campaign-default values anywhere else; reference the template as their single source of truth. | R29 abs |  |
| ADR04-22 | §2.1 L44 | Use the template's temporal IS/OOS split as the OOS axis; never treat instrument or feed as OOS. A native-micro re-run is a realism gate only. | R24 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §Campaign-defaults row 1 |
| ADR04-23 | §2.2 L45 | Count K at two levels: campaign-local K feeds SPA/StepM; program-cumulative K per instrument family feeds DSR. Abandoned campaigns still count their K. | R23 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §Campaign-defaults row 2 |
| ADR04-24 | §2.3 L46 | Apply universe correction: SPA family gate plus StepM with an explicitly chosen block_size (never sqrt(T)), DSR at the template threshold, and PBO via CPCV where configs were selected. | R24 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §Campaign-defaults row 3 |
| ADR04-25 | §2.4 L47 | Run the temporal-consistency battery: sub-era sign consistency, drop-top-year, regime-slice survival (labels as test conditions, never filters), and CUSUM over the OOS era. | R24 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §Campaign-defaults row 4 |
| ADR04-26 | §2.5, §5 L48 | Never admit a survivor without a CUSUM decay-monitor spec whose null was calibrated during validation. | R24 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §Campaign-defaults row 5 |
| ADR04-27 | §2.6 L49 | Declare a per-campaign --max-cost total and check it against the summed estimate before any data pull. | R2 DEL⚖ | --max-cost/estimate gate is Databento-shaped (lab/databento_fetch); Databento retired 2026-09-10, no replacement; dormant if a paid vendor returns. |

</details>

<details><summary><code>docs/adr/2026-07-11-gen1-pipeline-retirement.md</code> — 12 rules: 2 absorbed, 5 detail, 5 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-28 | §2, §5 L79 | Retire machinery only; never delete evidence (closure dirs, pre-registrations, rejected_candidates entries, banked K) when retiring a subsystem. | R31 DEL | Superseded by operational_rules §16 retention test (great-prune ADR): evidence kept only under R1-R5, otherwise retrieved from history. |
| ADR04-29 | §5, §7 Phase 0 L111 | Before deleting modules, run a reverse-dependency import audit, resolve every live importer, and extract load-bearing content first. | R31 abs |  |
| ADR04-30 | §5 L114 | Move extracted pieces as-is during a retirement; do not improve a subsystem while extracting it. | R31 DEL | Discharged: extractions recorded in this ADR's §7 Implementation record (2026-07-11); retirement merged PR #317. |
| ADR04-31 | §5 L116 | Keep this subsystem retirement out of core/, Pine, locked constants and the MC anchor. | R14 DEL⚖ | One-off scope executed (bdc45a3/PR #317 per Status line); Rule 14 and AGENTS.md §Protection remain the stricter live owners. |
| ADR04-32 | §5 L117 | Subsystem- or track-tier deletion requires operator STRATEGIC-LoR ratification; an advisor or agent draft cannot self-ratify it. | R3 abs |  |
| ADR04-33 | §2, §5 L76 | Park lab/codification as the Python-to-Pine bridge; never delete it. | R31 DEL | lab/codification absent; retired by this ADR's Addendum 2026-07-24 operator ruling; ADR04-34 carries the live successor rule. |
| ADR04-34 | Addendum 2026-07-24 L251 | Build any future Python-to-Pine bridge fresh against the then-current survivor format; never restore the retired codification code. | R31 det |  |
| ADR04-35 | §2 L72 | Keep the gate self-test: planted-overfit candidates must fail and planted-real candidates must pass the validation chain. | R24 det |  |
| ADR04-36 | §2 L73 | Give a triage pre-filter no gate authority until it clears a pre-registered rank-correlation floor against the authoritative engine. | R24 det | → docs/methodology/prefilter_rank_correlation_gate.md |
| ADR04-37 | §1, §3 L57 | Keep one implementation of gate statistics (DSR/PBO/CPCV/SPA) through vetted libraries behind strategy-validation §8; never hand-roll a second. | R24 det | → .claude/skills/strategy-validation/SKILL.md §8 |
| ADR04-38 | §7 Phase 3 L177 | Land retirement provenance through a PR for operator confirmation; never self-merge. | R6 DEL | Superseded by AGENTS.md §Merges and credentials (2026-10-24): agent merge after clean Codex review and green CI; provenance PR #317 merged. |
| ADR04-39 | §4 L101 | If by 2027-01-11 a survivor needs a capability lost with Gen-1 code and not extracted, restore that module from git and amend this ADR. | R31 det |  |

</details>

<details><summary><code>docs/adr/2026-07-11-ops-cfd-estate-retirement.md</code> — 10 rules: 1 absorbed, 1 detail, 8 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-40 | §2 L55 | Retire code by deletion plus git-history retrieval (git show <commit>:<path>); keep no parallel archive/ tree. | R31 abs |  |
| ADR04-41 | §4 Trigger A, §5 L108 | If a live fill source and reconciliation need return, rebuild repo-native against the actual venue microstructure; never git-revert the retired DXTrade-shaped design. | R31 det |  |
| ADR04-42 | §5 L119 | Extract cited registries such as execution_lessons.md out of a tree before deleting that tree. | R31 DEL | Discharged: execution_lessons.md now at docs/methodology/lessons/; §16 'migrate every obligation first' covers future cases. |
| ADR04-43 | §5 L120 | Do not touch core/ files in an ops cleanup pass; core/ dispositions are separate follow-ons. | R37 DEL | One-off pass scope; core/ account_aliases follow-on completed 2026-07-11 per this ADR's change history. |
| ADR04-44 | §5 L121 | Annotate REPO_MAP move-provenance rows as retired; never delete them. | R31 DEL | REPO_MAP.md holds no retirement provenance rows; its §4 points dispositions to retirement decisions and Git history. |
| ADR04-45 | §5 L122 | Do not retire the multiplier spine as a side effect of the CFD-estate prune. | R31 DEL | Multiplier spine retired by 2026-07-22 substrate retirement Phase 2 (PR #485); ops/accounts.py absent. |
| ADR04-46 | §5 L123 | Retire a seam and its validator together; leave no stubs or importable just-in-case remnants. | R31 DEL | FXIFY seam and validator excised (ops/fxify_rule_validator.py, ops/accounts.py absent) by fxify-ops-surface retirement; pass-scoped rule. |
| ADR04-47 | §5 L124 | Keep ops/sentinel, the regime_time_cost RESULTS evidence and the ops/instruments registry; they are load-bearing. | R31 DEL | One-off pass KEEP list; regime_time_cost RESULTS later removed in 770413bb under §16; retention of sentinel/instruments now governed by §16 R1. |
| ADR04-48 | §6, §7 step 4 L151 | Drop a check_skill_refs allowlist entry only after the skill references to that path are retired. | R38 DEL | Executed 2026-07-11; .claude/skills/live-execution-journal and ops/live_journal absent. |
| ADR04-49 | §4 Trigger B L110 | When M6J sizing design settles on native micro-contracts, open a follow-on ADR on retiring the multiplier spine. | R31 DEL | Discharged by 2026-07-22 substrate retirement Phase 2 deleting the spine; ops/accounts.py absent. |

</details>

<details><summary><code>docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md</code> — 12 rules: 1 absorbed, 11 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-50 | §2(1), §5 L55 | Treat 'The Statistics of Tradable Anomalies' as REFERENCE rationale only; never cite it as authority for a gate or locked-parameter change. | R29 det |  |
| ADR04-51 | §5 L125 | When a decision changes, amend the ADR; update the reference doc only as external-material re-adoption, never as a decision surface. | R29 abs |  |
| ADR04-52 | §2(3), §5 L72 | Do not import the recorded non-adoptions (Kelly sizing, SPRT decay detection, Ledoit-Wolf optimizers, tracked numeric pi/PPV); reversal needs a superseding ADR citing a dated miss. | R26 det |  |
| ADR04-53 | §5 L124 | Introduce no locked risk constant in the shrinkage convention or Tranche-1 doctrine documents. | R14 det |  |
| ADR04-54 | §2(2) L65 | Name the null hypothesis explicitly and handle drift in permutation tests. | R24 det | → .claude/skills/strategy-validation/SKILL.md §5 |
| ADR04-55 | §2(2) L66 | Use filtered, never smoothed, hmmlearn regime states to avoid lookahead. | R25 det | → .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md |
| ADR04-56 | §2(2) L67 | Remove the intraday volatility U-shape before mining so scanners do not rediscover it. | R25 det | → .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md |
| ADR04-57 | §2(2) L68 | Apply futures data hygiene: back-adjustment, CME session clock and bid-ask-bounce handling. | R25 det | → .claude/skills/futures-anomaly-discovery/reference/tool-discipline.md |
| ADR04-58 | §2(2) L69 | Anchor the discovery ledger at <repo-root>/discovery_manifests; never use a cwd-relative default. | R23 det | → .claude/skills/futures-anomaly-discovery/scripts/register_search.py |
| ADR04-59 | §2(2) L70 | Use the backtest-to-live shrinkage convention as the ex-ante haircut prior for go-live underwriting. | R20 det | → docs/methodology/backtest_live_shrinkage.md |
| ADR04-60 | Addendum 2026-08-29 (a) L214 | Freeze spec or pre-registration prose only if two independent implementers would compute identical numbers; otherwise ship reference code or a worked synthetic example. | R23 det |  |
| ADR04-61 | Addendum 2026-08-29 (b) L219 | Promote duplicated null-construction primitives (circular-shift p, within-stratum roll, block-bootstrap lift, stratified lifts) into lab/research_utils/ with adversarial tests. | R24 det |  |

</details>

<details><summary><code>docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md</code> — 9 rules: 1 absorbed, 6 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-62 | §2.1 L47 | For overlapping-window search terms, count K_DSR as the non-overlapping tiling floor; count discrete search spaces at face value. | R23 det |  |
| ADR04-63 | §2.1 L47 | Report the K bracket together, non-overlap floor (binding) and raw overlapping count; never report only the value that passes. | R23 det |  |
| ADR04-64 | §2.2 L48 | Name K_SPA (post-triage scored count) and K_DSR (search magnitude) separately in manifests and pre-registrations. | R23 det |  |
| ADR04-65 | §2.3 L49 | Pin DSR's across-trial variance V to 1/n (selected candidate's OOS trade count); never trust the empirical cross-candidate Sharpe variance. | R24 det |  |
| ADR04-66 | §2.4 L50 | Disclose in every pre-registration the minimum detectable per-trade Sharpe for its bound (K_DSR, V, n); do not freeze if it exceeds the plausible-edge ceiling. | R23 det |  |
| ADR04-67 | §2.5, §5 L51 | Keep the DSR threshold unchanged; never lower it to compensate for K or V calibration defects. | R24 det |  |
| ADR04-68 | §5 L84 | Do not amend a frozen K/V rule or any frozen pre-registration clause after the campaign has seen a result. | R23 abs |  |
| ADR04-69 | §5 L85 | Patch universe_gate.py only by the minimal additive var_trials override; any broader module change needs its own review. | R24 DEL | Superseded: universe_gate.py default flipped to V=1/n (lines 363-365) on 2026-08-15 per change history. |
| ADR04-70 | §6 Risks L113 | Make every campaign runner pass --var-trials explicitly when calling run_universe_gate. | R24 DEL | Discharged: run_universe_gate now defaults var_trials to 1/n (universe_gate.py:363-365); explicit pass unnecessary. |

</details>

<details><summary><code>docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md</code> — 20 rules: 7 absorbed, 9 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-71 | §2 L40, L55 | Target multi-firm ops at the AUTOMATION_FRIENDLY_PROP_FIRMS families, encoding every firm target and constraint in core/firm_rules.py as the single registry. | R16 abs |  |
| ADR04-72 | §2.1 L51 | Declare DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO against ops/prop_envelope_default.md at each discovery candidate's closure. | R28 det |  |
| ADR04-73 | §2.2, §5 L52 | Pull prop constraints from firm_rules.FIRM_RULES plus envelope overlays; never hard-code firm names or challenge constants in lab/ research artifacts. | R16 abs |  |
| ADR04-74 | §2.2 L52 | Productionalize admitted survivors through lifecycle CANDIDATE intake, then codification, sweep and validation. | R15 DEL | Gen-1 sweep and codification retired (gen1 ADR; lab/codification absent, Addendum 2026-07-24). |
| ADR04-75 | §2.3, §5 L53 | Treat this program as targets only; rail build, account registration and live start each need their own gated ADR, never implied by it. | R3 abs |  |
| ADR04-76 | §2.3 L53 | Execute through attended automation on TV to CrossTrade to NT8 to Rithmic/Tradovate. | R11 DEL⚖ | Route superseded by S2 daemon→listener ADRs and Tradeify native-only ruling 2026-10-12 (AGENTS.md standing consequences), the stricter live owners. |
| ADR04-77 | §2 R6 boundary, §5 L57 | Never deploy the locked legacy book to prop firms at locked CFD allocations or on CFD-edge-transfer claims; locked-leg futures expressions enter only as pre-registered scoring candidates. | R15 det |  |
| ADR04-78 | §5 L96 | Operate attended automation only; never run full lights-out or unattended 24h operation. | R11 abs |  |
| ADR04-79 | §4 H L77 | Count program success only when a pre-registered candidate clears the bust ceiling on at least two distinct-firm tiers in simulation before any live account spend. | R28 det |  |
| ADR04-80 | §4 Revert trigger L79 | If by 2026-11-08 no pre-registered candidate clears the ceiling on any registry tier in a dated re-MC, demote the program to research-only. | R28 det |  |
| ADR04-81 | §4 Secondary trigger L81 | If a registry firm issues a written policy banning attended automation, remove that family from AUTOMATION_FRIENDLY_PROP_FIRMS and re-run eligibility. | R16 det |  |
| ADR04-82 | Addendum 2026-08-22 Ruling L281 | If exactly one frozen tier clears at 2026-11-08, read the falsifier as PARTIAL: no discharge or demotion; re-check 2027-02-08, then demote if still one or fewer. | R28 DEL⚖ | Addendum 2026-08-22 stays Proposed; withdrawal ADR Addendum 2026-10-02 ruling 4 reserves the exactly-one-tier call to Joshua at 2026-11-08. |
| ADR04-83 | Addendum 2026-08-22 Forbidden L330 | Do not move the frozen ceiling, pass floor, trailing_locking requirement or tier cross-section to manufacture a second clearer. | R23 abs |  |
| ADR04-84 | Addendum 2026-08-22 Forbidden L333 | Correct a frozen pre-registration only with a reader-intercept banner; never edit its frozen body in place. | R30 abs |  |
| ADR04-85 | Addendum 2026-08-22 Forbidden L341 | Treat external adversarial-lens output as zero-authority tripwire input, never as evidence for or against a ruling. | R0 DEL | Owning ox-alpha lens ADR deleted 2026-09-08 (docs/adr/TOMBSTONES.md): lane retired, no successor owner. |
| ADR04-86 | Addendum 2026-10-16 §1 L386 | Apply a 5.0% bust ceiling to §4 candidates from 2026-10-16; keep the pass floor, trailing_locking requirement, intraday-honest clock and inactivity-barrier-OFF convention. | R28 det |  |
| ADR04-87 | Addendum 2026-10-16 §2 L391 | Pre-register ORB MNQ v7 disclosing prior ORB-MNQ failures and v7 differences in the trial ledger; freeze by 2026-10-23, re-MC by 2026-10-30 on the intraday-honest clock. | R23 det |  |
| ADR04-88 | Addendum 2026-10-16 §3 L398 | Register FXIFY Futures Flex under its own key; count it toward §4 only after a starting_balance tier row, a passing pre-flight and dated primary-source fact re-verification. | R16 det |  |
| ADR04-89 | Change history 2026-10-17 L424 | Read the 'under Codex' owner wording as the Claude coordinator for integration and dispatch; Codex owners keep technical execution. | R4 det | → docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md §Coordinator transfer — Claude deployment coordinator, 2026-10-17 |
| ADR04-90 | §10 staleness notes L156 | Leave stale audit-hook lines unedited as audit trail; append dated staleness notes or corrected blocks instead. | R30 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-13-dd-protection-concept-not-constant.md</code> — 16 rules: 0 absorbed, 16 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-91 | §2.1 L29 | Protection invariant: when room to the live bust floor depletes past a budget fraction, scale that day's sizing, auto-clear on recovery, multiply BASE_RISK, ULP-round first, single tier. | R14 det |  |
| ADR04-92 | §2.2 L30 | Per-instance protection variables are exactly trigger, scale and reference_mode (static, trailing, locking), dispatched from the firm_rules dd_type. | R14 det |  |
| ADR04-93 | §2.3, §5 L31 | Never rebind dd_protection's DD_TRIGGER/DD_SCALE literals to computed expressions; any registry pins one-way to the literals. | R14 det |  |
| ADR04-94 | §5 L72 | Never let dd_protection import dd_geometry; keep the policy registry off the anchor import path. | R14 det |  |
| ADR04-95 | §5 L71 | Do not edit the MVD self-check (_validate_protection_rule) or its pin literals for any reframe purpose. | R14 det |  |
| ADR04-96 | §2.4, §5 L32 | Treat C2's trigger/budget ratio theta* as provenance-only: it may seed a candidate grid, never validate one, and never appears as validated without the failed-regime-gate caveat. | R14 det |  |
| ADR04-97 | §5 L73 | Never default an unregistered protection instance to an existing policy, or an unknown dd_type to static; unresolved lookups must raise. | R14 det |  |
| ADR04-98 | §4 L56, §5 L75 | Admit a protection instance only by: pre-registered objective, selection rule and regime gate (K ledgered); grid via firm_kwargs after pre-flight; both-halves regime gate; frozen row naming its ADR. | R14 det |  |
| ADR04-99 | §2 Deferred L37 | Pass protection (trigger, scale) as arguments to run_seed/simulate_path in scoring runs; never edit the module globals. | R14 det |  |
| ADR04-100 | §2 Deferred, §5 L37 | Do not author the deferred protection machinery (seed heuristics, reference_mode de-risk branch, harness swaps, shrinkage floors, micro snapping, retry-EV) before a pre-registered prop candidate and engine pre-flight exist. | R14 det |  |
| ADR04-101 | §2.5 L33 | Reference semantics: static keeps the byte-identical dd-from-peak compare; trailing uses a budget-scaled trigger; trailing_locking post-lock references the bust check's floor(t). | R14 det |  |
| ADR04-102 | §4 Open question L62 | Re-derive each firm's protection objective to its reset/retry EV before admitting a funded-tier instance. | R14 det |  |
| ADR04-103 | §4 + Addendum 2026-09-01 ruling L359 | Revert dd_geometry if its presence turns the MVD self-check, verify_lock_anchors or check_boundaries red; never repair by weakening a gate. | R14 det |  |
| ADR04-104 | Addendum 2026-09-01 L304 | Run audit-hook commands standalone; never chain live gates with && after a possibly-retired script. | R21 det |  |
| ADR04-105 | Addendum 2026-08-02 L158 | Treat swapping or adding a named member of a falsifier's gate set as a falsifier amendment needing a superseding decision; never substitute silently. | R28 det |  |
| ADR04-106 | Addendum 2026-08-02 L227 | Select the live firm by an explicit FIRM_RULES key; no implicit global firm selector exists. | R16 det | → docs/adr/2026-06-06-firm-constants-single-source.md |

</details>

<details><summary><code>docs/adr/2026-07-13-harv-discovery-lane-ratification.md</code> — 4 rules: 1 absorbed, 3 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-107 | §2.1 L46 | Run named-mechanism campaigns in the mechanism-first lane: register-record YAML, A/B mechanism-grade discount, adjudicating bundled predictions, inheriting Campaign defaults. | R25 det |  |
| ADR04-108 | §2.2, §2.4 L48 | HARD gate: block register_search open until every bundled clause has a written reachability attestation simulated under a plausible-true world; redesign or drop un-passable clauses. | R23 det |  |
| ADR04-109 | §5 L89 | Never quietly downgrade the HARD reachability gate to a recommended step; supersede with a dated ADR if it proves unworkable. | R23 det |  |
| ADR04-110 | §5 L91 | Do not promote a closed verdict on post-closure diagnosis; harvest the lesson, not a rescue. | R23 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-13-prop-account-book-segregation.md</code> — 9 rules: 0 absorbed, 9 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR04-111 | §2 L35 | Hold exactly one pre-registered book per account; a multi-leg book exists only if registered before deployment with a joint MC under the assigned tier's rules. | R15 det |  |
| ADR04-112 | §2 L37 | Treat adding a leg to a live account as a new book: superseding registration and re-MC under that tier before the leg's first trade. | R15 det |  |
| ADR04-113 | §2 L38 | Never let a legacy locked-book survivor and a greenfield candidate share an account without book registration. | R15 det |  |
| ADR04-114 | §2 L40, §7 Phase 2 L92 | Integrate program risk in one joint MC across accounts, keyed to each account's own rule set, with joint co-movement resampling. | R15 det |  |
| ADR04-115 | §5 L69 | Never park a temporary second strategy in a funded account to feed an inactivity clock; inactivity mitigation must be an in-book mechanism. | R15 det |  |
| ADR04-116 | §5 L70 | Do not cite measured near-zero correlation as license to co-mingle legs; it reflects non-overlap, not independence. | R15 det |  |
| ADR04-117 | §5 L71 | Do not warehouse one book's eval inside another book's account, or retro-designate co-resident legs as a book. | R15 det |  |
| ADR04-118 | §4 L59 | Re-open segregation for a tier class by superseding ADR if per-account frictions reach 25% of a book's modeled expectancy; AMBIGUOUS carries forward, never silently extends. | R28 det |  |
| ADR04-119 | Addendum 2026-09-01 L120 | Leave the verdict on a dated falsifier check (here segregation 2026-08-08) to the operator; agents record verdict-free pointers only. | R3 det |  |

</details>

<details><summary><code>docs/adr/2026-07-13-prop-envelope-v1-ratification.md</code> — 13 rules: 0 absorbed, 12 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-1 | §2 item 1 L29 | Design to the 16:00 ET default flat deadline, which must sit inside every friendly firm's verified auto-liquidation print. | R16 det | → ops/prop_envelope_default.md §1 E1 |
| ADR05-2 | §2 item 1 L29; §5 L55 | Never design to a firm's auto-flatten as a backstop; flatten before the deadline yourself. | R16 det | → ops/prop_envelope_default.md §1 E1 |
| ADR05-3 | §2 item 2 L30 | Model firm consistency rules as soft eligibility gates that delay pass or payout, never as breaches. | R16 det | → ops/prop_envelope_default.md §1 E2 |
| ADR05-4 | §2 item 3 L31 | Keep news/event restrictions as per-firm overlays; never graduate them into the envelope default. | R16 det | → ops/prop_envelope_default.md §1 E7 |
| ADR05-5 | §2 item 4 L32; §5 L57 | Keep Elite Trader Funding out of AUTOMATION_FRIENDLY_PROP_FIRMS; re-admit only with written firm authorization for owner-operated automation, never via its copier list. | R16 det | → ops/prop_envelope_default.md §5 item 4 |
| ADR05-6 | §2 item 5 L33 | Encode each friendly tier's all-in per-side commission as cost_per_side_usd in core/firm_rules.py, never in envelope prose; every friendly tier must carry a plausible value. | R16 det |  |
| ADR05-7 | §2 item 5 L33 | Add consistency_rule_pct to Tradeify tiers and extend the friendly-tier cost guard test. | R16 DEL | Discharged 2026-07-13: consistency_rule_pct present on Tradeify tiers (core/firm_rules.py L331, L380); cost guard test exists (tests/core/test_automation_friendly_prop_firms.py L38). |
| ADR05-8 | Header L10 | Change the envelope default (§1–§3) only by ADR; change per-firm overlay rows only on re-verification. | R16 det | → ops/prop_envelope_default.md header (Change control) |
| ADR05-9 | §4 L49; §5 L54 | Re-verify any envelope overlay row older than 90 days before scoring a candidate against it or using it at a deployment fork. | R17 det | → ops/prop_envelope_default.md §4 (overlay discipline, 90-day stale rule) |
| ADR05-10 | §4 L49 | If the E1 binding minimum drops below 16:00 ET or a firm's consistency rule becomes a hard mid-eval breach, reopen that default by fresh ADR. | R16 det |  |
| ADR05-11 | §5 L53 | Never use compute_default_config's headline bust for a prop tier scored against the envelope. | R20 det |  |
| ADR05-12 | §5 L56 | Do not lower BluSky's cost_per_side_usd to its cheaper eval-rail rate while the declared rail is TV→CrossTrade→NT8. | R16 det | → core/firm_rules.py (BluSky block, cost_per_side_usd comment) |
| ADR05-13 | §5 L58 | Never hard-code firm-specific facts in lab/ research artifacts; firm facts enter only at the deployment fork via envelope overlays. | R16 det | → ops/prop_envelope_default.md Purpose + §2 |

</details>

<details><summary><code>docs/adr/2026-07-13-stage8-mechanistic-exposure-companion.md</code> — 8 rules: 1 absorbed, 6 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-14 | §2a L138 | File an exposure declaration (side, ET entry window, in-market minutes/yr, per-leg structural overlap) for every Stage-8 candidate; bind a structural-overlap threshold at Stage 0. | R24 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md Stage-8 row |
| ADR05-15 | §2a L138 | Never admit an episodic candidate (in-market under 5% of session clock) on realized-correlation or ENB deltas alone; report them as insufficient context. | R24 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md Stage-8 row |
| ADR05-16 | §2b L140 | At closure, annotate exposure-coordinates beside DEPLOYABLE-DEFAULT-ENVELOPE so they travel to the deployment fork. | R16 det | → ops/prop_envelope_default.md §2 item 5 |
| ADR05-17 | §2c L142 | Offer the 08-08 Class A packet owner a shock-conditional MC module as proposed input only, never a unilateral packet edit. | R24 DEL | Discharged 2026-07-13 per ADR §7 Phase 2 (handed to packet owner); 08-08 pretriage brief archived in lab/ARCHIVED.json. |
| ADR05-18 | §2 L144; §5 L171, L174 | Adopt Stage-8 or Campaign-defaults changes only via ratified superseding ADR or the campaign's §8 override with reason; never silently or by in-place template edit. | R23 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §Campaign-defaults change control |
| ADR05-19 | §4 L161-165 | If the shock module's joint-bust delta is under 1pp across the frozen grid, demote the companion to annotation-only by superseding ADR; escalate if unrunnable by 2026-11-08. | R28 det |  |
| ADR05-20 | §5 L172 | Never choose or trim the shock grid after seeing MC output. | R23 abs |  |
| ADR05-21 | §5 L173 | Never turn exposure declarations into entry filters; declarations describe, never filter. | R24 det | → ops/prop_envelope_default.md §2 item 5 |

</details>

<details><summary><code>docs/adr/2026-07-14-cc-cursor-surface-allocation.md</code> — 94 rules: 19 absorbed, 72 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-22 | Decision seat table L59-67; Addendum 2026-10-24 L936 | Route work by seat: executive (Codex) sets goals and accepts on evidence; coordinator (Claude Code Opus) specifies and integrates; workers build frozen specs; operator owns merge and irreversible acts. | R4 det |  |
| ADR05-23 | Decision L56-57 | Rank every routing choice by landed-change quality first and operator attention second; never treat throughput as a metric. | R4 det |  |
| ADR05-24 | Seat table L63 | As executive, accept or reject on the evidence pack (diff, test log, dissent), never on coordinator synthesis alone; never author cards, implement or merge. | R4 det |  |
| ADR05-25 | Seat table L64 | As coordinator, never be sole signer on a diff from your own card or touch main; escalate the hard part rather than implementing it; raise effort before changing model. | R4 det |  |
| ADR05-26 | Seat table L65 | As worker, never change architecture, expand scope, resolve a spec ambiguity, write reserved files or merge. | R4 det |  |
| ADR05-27 | Decision L69, L140; Addendum 2026-10-24 L937 | Name worker branches codex/* or claude/* only; glm/* is withdrawn. | R6 abs |  |
| ADR05-28 | Decision L69-73 | Keep Cursor retired: no Cursor lane, @cursor dispatch, cursor/* branches or cursor[bot] allow-listing. | R4 det |  |
| ADR05-29 | Reviewer ≠ planner L75-78 | Never let a card's author be the only signer on its diff; the executive's goal-based review and the operator's (or conditioned) merge are the independent signatures. | R5 abs |  |
| ADR05-30 | Committed-handoff rule L80-90 | Pass directions, cards and returns across seat boundaries only as committed, dated files; the lightweight issue is the only non-file card. | R4 DEL | Superseded by surface-allocation Addendum 2026-10-24 (committed-handoff rule superseded; direct-prompt cards allowed; returns stay branch plus PR). · *at HEAD:* removed: Committed-handoff rule deleted; replaced by body Handoffs paragraph allowing direct prompts (3f1c45ec, PR #909). |
| ADR05-31 | Addendum 2026-10-24 L940 | Send a direction or card across seats as a direct prompt if needed, but return worker results as a pushed branch plus PR; committed cards still pass check_brief.py. | R4 abs |  |
| ADR05-32 | Committed-handoff rule L87-88 | Write private evidence in the operator's primary checkout, never in a worktree. | R13 det | → AGENTS.md §Public-clone posture (Private read surface) |
| ADR05-33 | Routing test 0 L95-102 | Route to local, full stop, when Phase-0 reads need gitignored vendor data or secrets not verified present in the target environment. | R41 det |  |
| ADR05-34 | Routing test 1 L103-109 | Keep doctrine authoring and locked or governed surfaces (ADRs, preregs, closures, lifecycle, AGENTS/STATE, core anchor edits, Pine) with the coordinator; read-only core imports are fine anywhere. | R4 det |  |
| ADR05-35 | Routing test 2 L110-113 | Dispatch only frozen specs (binary gates, resolved ambiguities, enumerated forbidden moves) to workers; a worker bounces NEEDS_CONTEXT rather than resolving ambiguity. | R4 det |  |
| ADR05-36 | Routing test 3 L114-116; L184-187 | Keep builds smaller than their brief (under about one hour or three files) on the open surface; dispatch eligible frozen packets proactively without per-task confirmation. | R41 det |  |
| ADR05-37 | Proactive dispatch L184-190 | Obtain task-routing's environment GO for a cloud worker dispatch unless the operator already chose the environment; a dispatch on the operator's machine needs neither. | R41 det |  |
| ADR05-38 | Handoff contract item 1 L120-124; Addendum 2026-09-27 L842-865 | Ensure every card under docs/briefs/handoffs/ (bar grandfathered ones) or carrying an authority block passes check_brief.py --type handoff as well-formed. | R33 abs |  |
| ADR05-39 | Addendum 2026-09-27 L874-876; enforcement table L300 | Do not retrofit historical cards, but apply item 1 to any dispatched grandfathered card through the coordinator's pre-dispatch read. | R33 det |  |
| ADR05-40 | Addendum 2026-09-27 L822-840 | Exempt only the four named 2026-09-27 files from item 1; a card copied out of the staged-acceptance set file must pass check_brief.py at pre-dispatch read. | R33 det |  |
| ADR05-41 | Handoff contract item 2 L125-127 | Require card §0 Phase-0 reads with a read-report before code and a NEEDS_CONTEXT bounce on contradiction; the worker runs handoff-verify as Phase 0. | R0 det |  |
| ADR05-42 | Handoff contract item 3 L128 | List §5 forbidden moves in the card naming the locked surfaces the task runs near. | R33 det |  |
| ADR05-43 | Handoff contract item 4 L129-131 | Declare in card §0 whether any read touches gitignored vendor data or a secret, naming the confirmed-present check performed for this dispatch. | R41 det |  |
| ADR05-44 | Handoff contract item 5 L132-136 | Name acceptance tests in the card before the worker starts, each with the property it must violate to fail; worker-written tests never form the acceptance basis. | R33 det |  |
| ADR05-45 | Handoff contract item 5 L136-137 | Include an invariant table for contract-driven code and a state model for anything with orders, positions or shutdown semantics. | R33 det |  |
| ADR05-46 | Addendum 2026-09-26b A L731-736; item 5 L137-139 | Refuse any card granting worktree.write or research.run without named non-empty acceptance tests, whatever seat it declares; a registry lacking acceptance_required_for fails closed. | R33 det |  |
| ADR05-47 | Return contract L140-142 | Return worker work as a codex/* or claude/* branch and a green-tested PR with a four-state status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. | R4 abs |  |
| ADR05-48 | Return contract L142-146 | Adjudicate DONE_WITH_CONCERNS before merge; allow one NEEDS_CONTEXT re-anchor and re-dispatch, then the coordinator restarts on the escalation lane, never a third dispatch. | R7 det |  |
| ADR05-49 | Handoff contract item 7 L147-156 | Give every new worker card one `yaml authority` block naming seat, parent, max_risk, registry capabilities, all restated parent constraints and acceptance test names. | R4 det |  |
| ADR05-50 | Item 7 L154-156; Addendum 2026-09-26b A L728-730 | Bind each card to its actual executor by the coordinator's pre-dispatch read plus executive review on every route; the checker binds grants only to the declared seat. | R4 det |  |
| ADR05-51 | Enforcement table L299 | Name an in-repo parent on every worker card; parents are checked recursively, cycles are refused, and a block-less parent narrows nothing beyond the seat. | R4 det |  |
| ADR05-52 | Addendum 2026-09-26b A L737-739 | Do not build seat-binding path conventions, launcher checks or dispatch ledgers until a mislabelled card is recorded; then prefer a return-side PR check. | R36 det |  |
| ADR05-53 | Lightweight dispatch issue L158-170 | Use a GitHub issue body instead of a brief only for small precedented fixes carrying items 2–7 in full, with the coordinator's recorded handoff-verify read comment. | R33 det |  |
| ADR05-54 | Issue freeze L172-182 | Freeze an issue card by recording its body sha256 and read date; the worker recomputes at Phase 0 and bounces on mismatch; any later edit makes a new card. | R33 det |  |
| ADR05-55 | Escalation lane L192-196; Addendum 2026-09-30 L903-905 | Fire the escalation lane only on a named trigger stated in the dispatch, within budget: one milestone review per milestone, one unstick per day unless the operator raises it. | R7 det |  |
| ADR05-56 | Trigger 1 L197-203; Addendum 2026-09-30 L909 | After a second failure of the same card or module, rebuild from invariants or the state model on the escalation lane; first raise coordinator effort for reasoning gaps. | R7 det | *at HEAD:* changed: Fable wording folded; effort-first clause now unconditional, reasoning-gap qualifier dropped (3f1c45ec, PR #909). |
| ADR05-57 | Trigger 2 L204-207 | Before the operator ratifies a campaign gate, ADR, pre-registration or closure, run the refute-first adversarial pass on the escalation lane; diff review does not cover it. | R7 det |  |
| ADR05-58 | Trigger 3 L208-210 | Author or rebuild cards and specs touching routing-test-1 locked surfaces or the rail on the escalation lane; daily cards stay in the coordinator session. | R7 det |  |
| ADR05-59 | Ownership and precedence L212-223; Addendum 2026-09-30 L906-907 | Keep escalated items owned by the coordinator; the lane never takes the coordinator seat, supervises workers, plans beside the executive, or serves as a stronger-model worker retry. | R7 det |  |
| ADR05-60 | Addendum 2026-09-30 L909-913 | Run escalations as a separate fresh-context Opus session or subagent at raised effort, briefed from invariants; read 'Fable' in this ADR as 'the escalation lane'. | R7 det | *at HEAD:* changed: 'Read Fable as escalation lane' paragraph deleted, wording replaced in place; fresh-context session rule kept (3f1c45ec). |
| ADR05-61 | Merge authority L225-227; §8 L496 | Never treat green CI, a clean automated review or an adjudication verdict alone as merge authority; agents merge only under the conditioned standing GO. | R6 abs |  |
| ADR05-62 | Addendum 2026-10-24b A L947 | Merge as an agent only when a Codex review at the head reports no findings, every CI check is COMPLETED and green there, and the merge pins that SHA. | R6 abs |  |
| ADR05-63 | Addendum 2026-10-24b A L947 | After fixing review findings, push and comment `@codex review`; once three Codex reviews have found issues, stop fixing and return the PR to its original owner. | R6 det |  |
| ADR05-64 | Action classes L272; enforcement table L302; Addendum 2026-10-24b L947 | Never enable GitHub auto-merge. | R6 abs |  |
| ADR05-65 | Enforcement table L303 | Never push directly to main; every change reaches main by PR with the strict required skills (3.12) check. | R6 abs |  |
| ADR05-66 | Action classes L263-272 | Classify every consequential act as low, medium, operator act (high) or forbidden via scripts/seat_authority.yml, the single capability registry; medium is the agent ceiling. | R4 det |  |
| ADR05-67 | Action classes L272 | Grant no seat a forbidden capability (auto-merge, direct push to main, TV login automation, locked-parameter or protection-constant edits, private-data commits); no approval unlocks one. | R4 det |  |
| ADR05-68 | Action-class rule 1 L276-279 | Let cards only narrow: never grant an operator act or forbidden capability; stay within seat grant, max_risk and parent constraints; a needed relaxation is an escalation. | R4 abs |  |
| ADR05-69 | Action-class rule 2 L280-287 | Treat approval as an operator act bound to its exact object (merge to head SHA, arming GO to one session); agent text reporting approval is not approval. | R3 det |  |
| ADR05-70 | Action-class rule 3 L288-292 | Record a side effect whose outcome went unobserved as IN_DOUBT, reconcile it against the external system, and never retry automatically; local idempotency keys prove nothing. | R11 abs |  |
| ADR05-71 | Action-class rule 4 L293-295 | Build an orchestrator service only after a recorded failure shows the existing enforcement points are insufficient. | R36 abs |  |
| ADR05-72 | Operator-act hook L310-325 | Treat guard_operator_acts.py as a best-effort Claude Code prompt, not an enforcement boundary; do not extend it to chase every command spelling. | R4 det |  |
| ADR05-73 | Addendum 2026-09-26 L788; enforcement table L304 | Treat rail deploy as an operator act; prompt on live-path apps (c1-rail, c1-signal-daemon) or undeterminable targets, failing closed; stay silent for other apps. | R10 det |  |
| ADR05-74 | Enforcement table L305 | Prompt on every rail --arm but never on --disarm or --status; disarming must never wait on a prompt. | R10 det |  |
| ADR05-75 | Addendum 2026-09-26 L787 | Arm with --acknowledge-m1-unresolved only through the hook's ask prompt; the operator's answer is the per-session GO, and an arming_deviation record is written. | R10 det |  |
| ADR05-76 | Enforcement table L305; Addendum 2026-09-26 L791 | Read the arm interlock as checking M1 structure and RESOLVED status only: forged complete files pass, and the host boot gate never checks M1. | R10 det | → AGENTS.md §Live-execution posture |
| ADR05-77 | Rule 2 L281; Addendum 2026-09-26 L787 | Obtain a separate operator GO for every armed session. | R10 abs |  |
| ADR05-78 | Addendum 2026-09-26 L789 | Keep pinned --admin merges askable and unpinned merges denied (pr.merge_unpinned). | R6 det |  |
| ADR05-79 | Action classes L271; Addendum 2026-09-30b L924 | Treat trade.submit as an operator act never grantable in a card; an agent may act only on the specific operator-directed order, exit or cancel via an authenticated attended surface. | R10 det |  |
| ADR05-80 | Addendum 2026-09-30b L926 | Never place card-granted, automated or unattended orders or read an arming GO as directing a trade; arming, M1, spend-ceiling and per-session GO rules stay unchanged. | R10 det |  |
| ADR05-81 | Enforcement table L306; Addendum 2026-09-30b L928 | Keep broker credentials outside agent environments (boundary OF-5, re-verified at G-ARM). | R12 abs |  |
| ADR05-82 | Operator decision packets L329-337 | Bring anything needing the operator as one packet: question, options with consequences, recommendation, linked evidence, dissent, what was deliberately not done, and the no-decision outcome. | R3 det |  |
| ADR05-83 | Operator decision packets L337-340 | Name the default and its timing for reversible items, where silence is consent; operator acts have no default; a green DONE is not a packet. | R3 det |  |
| ADR05-84 | Operator decision packets L330-332 | Queue packets behind STATE's numbered operator items without making them items; keep at most five live items, treating overflow as a prioritisation defect. | R34 det | → STATE.md §Operator queue |
| ADR05-85 | Seat names L342-351 | Translate imported organisation-proposal seat names onto this seat table at the boundary, never adopting a second chart; a Chief of Staff may author the mandate, never cards. | R4 det |  |
| ADR05-86 | Measure L353-358 | Measure the seat model by operator-minutes per accepted change and post-merge defects, never cards closed; escalation firing on over a third of cards means cards are unfrozen. | R4 det |  |
| ADR05-87 | Measure L358-362 | Log packets returned 'not mine' or 'under-evidenced' in the campaign record; if either exceeds a third over 8 weeks, fix the escalation line or packet format. | R4 det |  |
| ADR05-88 | Measure L362-364 | Treat any merge, arm or deploy done by an agent without the operator's act as a failed enforcement point; fix it at the cheapest layer before other work there. | R4 det |  |
| ADR05-89 | Orchestration L229-234 | When orchestrating several workers, the coordinator owns the claim manifest and each packet clears routing tests 0–3; cut work per the work-decomposition skill. | R41 det |  |
| ADR05-90 | Orchestration L238-240 | Give parallel packets disjoint file footprints; reserve SESSIONS, STATE, campaign-state and board or index files to the coordinator's integration commit. | R41 det |  |
| ADR05-91 | Orchestration L241-244 | Re-verify each packet's premises against current origin/main at dispatch, with an explicit no-op: if already fixed, return DONE citing the commit. | R0 det |  |
| ADR05-92 | Orchestration L245-248 | Complete the brief's pre-dispatch review and merge any re-freeze to main before dispatching the first packet. | R41 det |  |
| ADR05-93 | Orchestration L249-252 | Carry the brief's post-review frozen SHA in each dispatch pointer; a worker whose pointer mismatches main returns NEEDS_CONTEXT instead of building. | R41 det |  |
| ADR05-94 | §8 L495 | Never expand a handoff's scope by adjacency. | R4 abs |  |
| ADR05-95 | §8 L497; Addendum 2026-09-27 L832 | Never retro-fit a brief after the build to make the record compliant; record a dated deviation instead. | R33 abs |  |
| ADR05-96 | §8 L494 | Never hand off a verbal spec; the brief is the containment, whatever the worker. | R33 det |  |
| ADR05-97 | §8 L498; Grounds L384-386, L409-411 | Never ground routing doctrine in unverified vendor benchmark, pricing or marketing claims. | R0 abs |  |
| ADR05-98 | §8 L504 | Grant Codex no write or push credential in this repository's CI without a superseding ADR. | R12 det |  |
| ADR05-99 | §8 L504-505, L523 | Keep Codex's native review as the executive's independent signature; revert by toggling the account setting if it proves lower-signal than Claude's over 8 weeks. | R5 det |  |
| ADR05-100 | §8 L506 | If two proactively dispatched tasks in 8 weeks needed operator judgment the coordinator lacked, revert to per-task dispatch confirmation. | R41 det |  |
| ADR05-101 | §4 L574-577, L582 | If two or more merged worker PRs in 8 weeks carry spec-interpretation defects, supersede with a tightened rule (narrower scope or full coordinator re-verification). | R4 det |  |
| ADR05-102 | §4 L578-585 | If three consecutive handoffs' brief costs exceed the build, carve that task class back to the coordinator by superseding ADR; never silently stop writing briefs. | R4 det |  |
| ADR05-103 | §4 L587; §10 hook 5 L704-706 | Check the §4 limbs at each quarterly programme review, adjudicating the SESSIONS worker-defect sweep and logging the verdict. | R28 det |  |
| ADR05-104 | §8 L469-475 | Never remove this file's load-bearing anchors #2--decision and #addendum-2026-09-04-disable-notify-cursor; append-only SESSIONS links depend on them. | R34 det |  |
| ADR05-105 | §8 Deliberately retained L537-563 | Keep the dormant Cursor residues (manifest author denylist, brief-type regex alternation, rg fallback) and dated Cursor attributions; history is not swept. | R31 det |  |
| ADR05-106 | §9 L591-612 | Delete the Cursor webhook routine and the daily-repo-truth-sync scheduled task. | R4 DEL | Discharged: §9 items 1-2 record webhook routine (HTTP 404) and daily-repo-truth-sync (taskDeleted) verified deleted 2026-09-15. |
| ADR05-107 | Addendum 2026-09-26b C L743-756 | Run GLM workers without the operator's merge-capable gh credential or Fly configuration, as a separate user or sandbox. | R12 DEL⚖ | Superseded: GLM dropped by Addendum 2026-10-24; stricter live custody for all agents in Addendum 2026-10-24b B (scoped PAT, no Fly credential). · *at HEAD:* removed: Addendum 2026-09-26b part C (GLM credential isolation) deleted; custody now 2026-10-24b part B (3f1c45ec, PR #909). |
| ADR05-108 | Addendum 2026-10-24b B L950 | Act under a fine-grained repo-scoped agent PAT (GH_TOKEN), never the operator's owner token; only the operator sits on the main ruleset bypass list. | R12 det |  |
| ADR05-109 | Addendum 2026-10-24b B L951 | Hold no Fly credential as an agent; the operator keeps no standing Fly login and deploys with per-app expiring tokens. | R12 det |  |
| ADR05-110 | Addendum 2026-10-24b B L952 | Remove unused credentials (Databento key, NOTION_TOKEN in .env, standing Azure login) rather than guarding them. | R12 det |  |
| ADR05-111 | Addendum 2026-10-24b B L953 | Dispatch Codex workers through scripts/dispatch_codex.ps1 in a sandbox with the agent token only; it refuses a worktree holding .env. | R12 det |  |
| ADR05-112 | Addendum 2026-10-24 L939 | Deny Claude Code reads of credential stores (~/.fly, ~/.azure, gcloud and gh config, ~/.ssh) and any .env; best effort, not a custody guarantee. | R12 det |  |
| ADR05-113 | Verification L774 | Never report mechanical form checks (check_brief, ADR graph, liveness) as proof of semantic equivalence or ratification; inspect those directly. | R21 abs |  |
| ADR05-114 | Current owner L442-465 | Treat ownership as split: this ADR owns seat, routing and contract rules; task-routing the test-0 list; cc_handoff the template; handoff-verify Phase 0; seat_authority.yml the registry. | R29 det |  |
| ADR05-NEW-1 | Reviewer ≠ planner L79; Addendum 2026-10-25 L928-933 | Have Claude-authored diffs, plans or proposals reviewed by Codex; a Claude self-review, Claude-run panel or workflow, or escalation-lane pass informs the author but is not the review. | R5 abs | *at HEAD:* new 488f757b (PR #911) |

</details>

<details><summary><code>docs/adr/2026-07-14-prop-portfolio-existing-strategy-candidates.md</code> — 13 rules: 4 absorbed, 6 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-115 | §2 L37 | Admit pre-registered existing-strategy books (locked legs' native-futures expressions, per-tier weights as venue variables) to the unchanged frozen survivor-scoring gate on equal terms. | R24 det |  |
| ADR05-116 | §2 item 1 L41 | Frame an existing-strategy candidate's claim as native-book bust geometry at firm tiers, costs included, never CFD-edge preservation. | R24 det |  |
| ADR05-117 | §2 item 1 L41; §5 L77 | Never cite this ADR or MYM/MNQ absolute PF to argue R5/P2 edge-transfer was wrong; R5/P2 stay FALSIFIED. | R26 det |  |
| ADR05-118 | §2 item 2 L42; §5 L81 | Never deploy the locked book at its locked CFD allocations or on a CFD-edge claim; per-tier weights never touch locked allocations, Pine or locked constants. | R14 det |  |
| ADR05-119 | §2 Constraints L44; §5 L78 | Commit each candidate's own pre-registration, fixing its variant set and disclosing all prior looks, before any frozen-tier G4 run. | R23 abs |  |
| ADR05-120 | §5 L79 | Never tune book weights after seeing per-tier results; a failed candidate closes rather than iterating in place. | R23 abs |  |
| ADR05-121 | §5 L80 | Never read the candidate-class widening as easing rail, account or go-live gating; a cleared candidate yields falsifier evidence and a lifecycle CANDIDATE intake only. | R15 abs |  |
| ADR05-122 | §2 Constraints L44; §5 L82 | Resolve the Aegis panel of record before an Aegis-bearing candidate pre-registers, or state explicitly that the candidate has no Aegis leg. | R23 DEL | Discharged 2026-07-15: operator pinned Aegis panel ae744 (ADR §7 Phase 2 and change history row 2026-07-15). |
| ADR05-123 | §4 L67 | If the first existing-strategy candidate fails Part A on all frozen tiers, require fresh operator authorization for any further candidate; no variant-grinding through the gate. | R28 det |  |
| ADR05-124 | §4 L67-71 | If no existing-strategy candidate clears Part A by 2026-11-08 in a dated pre-registered re-MC, retire the widened class with the parent program's demotion. | R28 det |  |
| ADR05-125 | §4 L69 | Never silently edit an Accepted ADR's decision or falsifier to fit an outcome; supersede, add a dated addendum, or revise with the prior text pinned. | R32 abs |  |
| ADR05-126 | §2 Constraints L44; §3 L59 | Leave the frozen survivor-scoring ceiling unchanged; the book clears it as-is or the route dies. | R23 DEL | Superseded by docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md (Part A ceiling 3.0% to 5.0%); ADR header L6 records it. |
| ADR05-127 | §2 Constraints L44 | Keep ACTIVE_FIRM set to FXIFY. | R16 DEL | Superseded: ACTIVE_FIRM deleted in substrate Phase 4 (PR #572, 2026-07-30); core/firm_rules.py L8 confirms; ADR header L5. |

</details>

<details><summary><code>docs/adr/2026-07-15-external-mechanism-harvest-intake.md</code> — 22 rules: 4 absorbed, 17 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-128 | §2 L47 | Admit externally published strategies to discovery only through harvest intake: file the declaration manifest, pass the two-clause screen, and obtain operator ratification of the inventory row. | R25 abs |  |
| ADR05-129 | §2 L52; reader-intercept L55 | Satisfy Path 1a with a named mechanism passing the four-clause constraint test (who pays, when, why it survives, how it dies); pattern-only or preference stories fail. | R25 det | → docs/methodology/strategy_harvest.md §1 Requirement 1 |
| ADR05-130 | §2 L53; §5 L245 | Admit a mechanism-less seed via Path 1b only if it has three decades, three independent cohorts, a replication ten years after discovery, and named sign-reversal conditions. | R25 det | → docs/methodology/strategy_harvest.md §1 Requirement 1 |
| ADR05-131 | §2 L57; §5 L246-248 | Use a cohort-cited δ/σ from the target instrument's own cohort, conservatively read with a decay haircut; never transplant (even via Path 1b) or invent one: else UNSCREENABLE. | R25 det | → docs/methodology/strategy_harvest.md §1 Requirement 2 |
| ADR05-132 | §2 L59; reader-intercept L58 | Kill any seed whose family K-bank pushes floor(K_eff) above Cap. | R23 DEL | Superseded by docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md: Requirement 3 is now mandatory disclosure, cannot kill a seed. |
| ADR05-133 | §2 L60 | Require confirm-power of at least 0.50 at the declared panel N under the frozen Clause-N formula. | R25 det | → docs/methodology/strategy_harvest.md §1 Requirement 4 |
| ADR05-134 | §2 L62; §5 L252 | Inherit screen constants (Cap, DSR floor, V, K_eff, power, z) by citation from the frozen screen pre-registration; never tune them here or in the reusable module. | R23 det |  |
| ADR05-135 | §2 L64 | Open Path 1a and 1b seeds via register_search open --lane mechanism-first; settle any contested reading through the HARV-lane ADR's own supersession discipline. | R25 det | → docs/methodology/strategy_harvest.md procedure step 6 |
| ADR05-136 | §2 L66; §5 L249 | Declare at most three fixed hypothesis expressions at admission; any later widening (sweeps, windows, variants) voids the PASS and needs a fresh declaration and re-screen. | R23 det |  |
| ADR05-137 | §2 L68; §5 L251 | Treat a screen PASS or intake admission as licensing campaign scoping only, never promotion evidence; every downstream gate still binds. | R25 abs |  |
| ADR05-138 | §5 L250 | Never re-propose a screened-dead class with a new citation but no new mechanism evidence. | R26 abs |  |
| ADR05-139 | §4 L90 | If the first two intake-class seeds both close FALSIFIED on primary confirm (not gate geometry), demote intake to research-only; re-proposal needs a source-class post-mortem. | R28 det |  |
| ADR05-140 | §4 L92; Addendum 2026-08-15 L233 | If no screen-PASS seed beyond D5 is admitted by 2026-11-08, name the intake idle in the program review rather than presume it active. | R28 det |  |
| ADR05-141 | Addendum 2026-08-16 L361 | Treat an AMBIGUOUS-HOLD closure among the first two as neither RESOLVED nor FALSIFIED and hold the slot; with no decisive closure by 2026-11-08, apply AMBIGUOUS. | R28 det |  |
| ADR05-142 | Addendum 2026-08-15 L146-148 | If two post-mark intake-class kills at Stage-2 cost-law or Clause-N/power accumulate, declare fundability-transfer FALSIFIED and demote intake by superseding ADR plus post-mortem. | R28 det |  |
| ADR05-143 | Addendum 2026-08-15 (a) L152 | Treat the addendum's running-count line as canonical and STATE as its mirror; a missing STATE row is not a reset. | R29 det |  |
| ADR05-144 | Addendum 2026-08-15 (b) L154; Ruling 2026-08-17 L189-210 | Increment limb 2 only for a distinct admitted construct's dated post-mark kill; never for pre-mark kills, variants, relabels, naming passes or pre-admission cheap falsifiers. | R28 det |  |
| ADR05-145 | Addendum 2026-08-15 (c) L156 | Do not write the source-class post-mortem until the limb-2 count actually reaches two. | R28 det |  |
| ADR05-146 | Addendum 2026-08-15 L235-239 | At the 2026-11-08 reading, disclose the post-mark limb-2 count and whether it fired, reading both limbs together; never treat 0/2 as decorative. | R28 det |  |
| ADR05-147 | Addendum 2026-08-15 (d) L158, L237 | Never treat a limb-2 fire or pin mark as licence to raise Cap or open a third sourcing channel. | R28 det |  |
| ADR05-148 | Addendum 2026-08-17 L384-390 | When Semantic Scholar has no verified record of a seed paper, traverse OpenAlex's citation graph instead, hand-screening every keyword-shortlisted survivor. | R25 det |  |
| ADR05-149 | Reader-intercepts L55, L58 | Leave frozen dated-decision text unedited; place a reader-intercept where it is read and carry current binding text in the living owner. | R30 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-15-sfrisk-1-t1-admitting-successor-risk-framework.md</code> — 10 rules: 3 absorbed, 5 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-150 | §2 L39-46 | Use T1 (per-regime-half p99 drawdown cap, adopted withdrawal model, days-to-first-skim practicality bar; TUW deferred) as risk-characterization input for any Aegis→M6J go-live decision. | R15 DEL⚖ | T1 input only for parked Aegis to M6J (parked by docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md §2.1); reopened self-funded lane uses 15% standard (2026-10-09 ADR Decision 4). |
| ADR05-151 | §2 item 3 L45; §5 L78 | Never treat T1's admission as go-live authorization; any go-live ADR must cite it, not assume it. | R15 abs |  |
| ADR05-152 | §5 L79 | Never revive the historical MC anchor triple as a live claim because T1 cleared. | R20 abs |  |
| ADR05-153 | §5 L80 | Never edit the decompound-HOLD ADR's §2/§4 to declare it resolved by T1; that parameter-configuration HOLD is a separate layer. | R32 det |  |
| ADR05-154 | §5 L81 | Cite the dated bust-day engine-fix explanation for T1's F1 fidelity delta instead of silently overwriting either figure. | R20 det |  |
| ADR05-155 | §2 item 4 L46; §4 limb 3 L70; §5 L82 | Add any F2/TUW clause only by later amendment, never inside this ADR; its failure attaches to the amended triple, not T1. | R32 det |  |
| ADR05-156 | §5 L83 | Never edit dd_protection.py, firm_rules.py or any locked constant to align with T1. | R14 abs |  |
| ADR05-157 | §4 limb 1 L68 | If a re-derived clean-vintage panel or engine fix pushes T1's F1 or F4 past its bar, supersede with a fresh ADR; never edit the numbers in place. | R28 det |  |
| ADR05-158 | §4 limb 2 L69; Addendum 2026-08-29 | Reopen T1 if the quarterly regime-check re-MC finds a trailing window failing T1's F1/F4 clauses. | R28 DEL | Superseded: struck by T1 Addendum 2026-08-29 (regime-check machinery SUSPENDED-ORPHANED after Pepperstone feed retirement; schedule struck). |
| ADR05-159 | Addendum 2026-08-29 L200-202 | Replace struck limb 2 (for example with a venue-native regime monitor) only through its own dated supersession. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-07-16-harv-attestation-same-units-supersession.md</code> — 6 rules: 0 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-160 | §2 item 1 L42-44 | In §R, simulate every gate a campaign can die at (cost, confirm, placebo, temporal battery) in that gate's own units; a Sharpe argument discharges only Sharpe gates. | R23 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §R (Process step 2) |
| ADR05-161 | §2 item 2 L45-49 | Exhibit cohort δ of at least four times round-trip cost fraction at panel-era median price, commissions included; otherwise the clause is UNREACHABLE. | R23 DEL | Deleted by operator ruling 2026-10-24 (HARV attestation ADR change history L92); template §R still restates cost-law clause, correction owed there. |
| ADR05-162 | §2 item 3 L50-52 | Compute every reachability quantity at the basis the gate is scored on (IS panel for Stage-2, OOS for Stage-6), never a present-day or convenience basis. | R23 det | → docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md §R (Process step 2) |
| ADR05-163 | §2 item 4 L53-54 | In every §R review, check explicitly for PD-1 (commission mis-scaling) and PD-2 (price-basis mismatch). | R23 det |  |
| ADR05-164 | §2 L40; header L5 | Keep the HARV HARD gate: block a mechanism-first register_search open that lacks a written reachability attestation. | R23 det | → docs/adr/2026-07-13-harv-discovery-lane-ratification.md §2 |
| ADR05-165 | §4 L58-64 | If a mechanism-first campaign dies on a freeze-unreachable clause these rules would have caught, replace the checklist with a mechanical register_search pre-flight; AMBIGUOUS if none freezes by 2027-02-08. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-07-16-root-doc-charter-dedup.md</code> — 15 rules: 5 absorbed, 8 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-166 | Decision L106-109; Addendum 2026-09-20 | Keep exactly five root guides (README, AGENTS, REPO_MAP, PIPELINES, STATE) in their roles; never add a sixth root guide or another state store. | R29 det |  |
| ADR05-167 | Decision L111-115 | Route ownership: Rule 7 holds root roles; STATE the five-item queue and order; plans next steps; records evidence; SESSIONS append-only history; scripts README gate tiers. | R29 det |  |
| ADR05-168 | Decision L117-119 | Let a spec, campaign, plan, PR or ADR own each decision; root guides carry only the consequence and an owner link, never retelling it. | R29 abs |  |
| ADR05-169 | Decision L119 | Never treat the choice of record as supplying evidence, approval or execution authority. | R3 abs |  |
| ADR05-170 | Decision L120 | Preserve unique facts with an appropriate owner before removing their last committed home. | R31 abs |  |
| ADR05-171 | Grounds L131-134 | If demoting a STATE role causes a documented decision error, a lost dormant thread or an unserved load-bearing need, restore that role or block and its ownership rule. | R29 det |  |
| ADR05-172 | Grounds L136-139 | Run A–D session classes, ~40-word prose targets, an exact-two-STATE-headers hook and quarterly document-size reviews. | R34 DEL | Retired by the charter 2026-09-08 revision (Grounds paragraph: A-D classes, 40-word targets, two-header hook, size reviews retired, not passed). |
| ADR05-173 | Decision L113 | Keep SESSIONS as append-only history whose living header routes to STATE without queue-copy stubs. | R34 abs |  |
| ADR05-174 | Queue-attention review L144-150 | Review queue history quarterly against dependency order and operator direction; a queue above five at two consecutive reviews, or repeated out-of-order serving, is failure; record findings with the owner. | R34 det |  |
| ADR05-175 | Queue-attention review L148-150 | Never let queue placement, completion or a failed review grant phase GO, open a replacement or channel, or change M1 license and arming boundaries. | R3 abs |  |
| ADR05-176 | Trigger schedule L152 | Record the next dated queue-attention check in this ADR and in STATE whenever the schedule rolls. | R34 det |  |
| ADR05-177 | Addendum 2026-09-20 L177-198 | Use AGENTS.md as the single agent-instruction file for every harness; CLAUDE.md is retired and no @AGENTS.md stub is kept. | R29 det |  |
| ADR05-178 | Addendum 2026-09-20 consequence 2 L192-195 | Read a dated record's CLAUDE.md §X citation as AGENTS.md §X; repoint only living surfaces, never rewriting dated records. | R30 det |  |
| ADR05-179 | Addendum 2026-09-20 consequence 1 L187-189 | Keep the MC-anchor triple and §Protection resident in AGENTS.md, where ops/recall/guard.py reads the triple. | R14 det | → AGENTS.md §Strategy Reference |
| ADR05-180 | Addendum 2026-09-20 consequence 4 L199-201 | Keep the main checkout on a CLAUDE.md-free commit so .claude/worktrees sessions load AGENTS.md, not the retired file. | R29 DEL⚖ | Post-merge condition: CLAUDE.md deleted in 5fae4d2d and absent at HEAD 3feb5961; operator local checkout state unverifiable from here. |

</details>

<details><summary><code>docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md</code> — 10 rules: 1 absorbed, 4 detail, 5 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR05-181 | §2 item 1 L46-49 | Treat the self-funded scale lane as CLOSED (parked): no active self-funded lane, go-live or capital allocation. | R15 DEL | Superseded in part by docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md (header L6: self-funded lane reopened on personal Tradovate account). |
| ADR05-182 | §2 item 1 L47-48; §5 L98 | Keep Aegis→M6J and Guardian-MGC parked: no go-live, capital or rail build may cite R6 §2.2; un-park only by dated operator GO and a new ADR. | R15 det |  |
| ADR05-183 | §2 item 2 L51-53 | Pursue venue-native Striker→MYM/MNQ reconstruction as the active research lane, admitting survivors only as new candidates after a pre-registered gate. | R23 DEL | Superseded by docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md Addendum 2026-07-24 (MYM/MNQ TERMINAL) and docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md. |
| ADR05-184 | §5 L94 | Never re-run the spent R5 B2 or P2 E1/K2 locked-CFD-Pine transfer tests to rescue micros. | R26 det |  |
| ADR05-185 | §5 L96 | Never edit locked Striker Pine or its CFD risk and pyramid locks in place; land reconstructions as new gitignored, hash-pinned candidate artifacts. | R14 det |  |
| ADR05-186 | §5 L99; §7 Phase 2 L131 | Pre-register a venue-native edition's gate (mechanism, cost, force-flat, OOS split) before any parameter search or scoring; CFD edge is not the claim. | R23 abs |  |
| ADR05-187 | §4 limb 1 L81 | Re-open a self-funded lane only by dated operator GO with a fresh venue/parity checklist, recorded in a new ADR. | R15 DEL | Discharged: re-open path exercised by docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md (operator GO, new ADR). |
| ADR05-188 | §4 limb 2 L82 | If no pre-registered reconstruction gate has run and no closure brief exists by 2026-11-08, demote reconstruction to dormant intent; reopen only via fresh pre-registration. | R28 DEL | Superseded: reconstruction tracks TERMINAL by docs/adr/2026-07-16-self-funded-lane-close-striker-micro-reconstruction.md Addendum 2026-07-24; ORB-MNQ governed by 2026-07-31 unpark ADR. |
| ADR05-189 | §4 early-fail L84 | If the first pre-registered MYM or MNQ reconstruction candidate fails all limbs, require fresh operator authorization for a second on that instrument. | R28 DEL | Historical: MYM/MNQ reconstruction TERMINAL (Addendum 2026-07-24); any reopen needs fresh GO plus prereg per the same addendum. |
| ADR05-190 | Addendum 2026-07-24 L182-191 | Reopen MYM/MNQ reconstruction only with a fresh operator GO plus pre-registration; the standing research interest is c1 execution quality (fills and exits). | R3 det |  |

</details>

<details><summary><code>docs/adr/2026-07-17-c1-rail-build-account-registration-go.md</code> — 39 rules: 8 absorbed, 23 detail, 8 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR06-1 | Header clarification (1) L10 | Require a fresh B6-equivalent dry-fire for any rebuilt or re-hosted signal path before it arms; never treat this build's B6 PASS as covering it. | R10 det |  |
| ADR06-2 | Pointer re-home L31 | Use public ARMING_PROCEDURE.md for operating steps; retrieve the private RUNBOOK only per its §2 (archive pin or ignored private root), never onto the public tree. | R13 det | → docs/notes/rail_build/ARMING_PROCEDURE.md §2 |
| ADR06-3 | Pointer re-home L31 | Never rewrite frozen ADR/LTM/prereg bodies in place; correct via dated addenda or reader-intercepts and repair only living instructions. | R30 abs |  |
| ADR06-4 | §2 Scope L58 | Keep this GO to one eval account and one rail instance; ORB-MNQ-1, a second account, or another firm each needs its own gated decision. | R3 det |  |
| ADR06-5 | §2 Scope L58 | Cap all-in spend to first live fill (eval, rail run-rate, ruled drill costs) at the operator-signed $700 ceiling. | R10 det |  |
| ADR06-6 | §4 Falsifier L75 | If dry-fire cannot prove the sizing law, spend would exceed $700, or Tradeify automation terms change: halt build, zero armed sessions, escalate; no silent tier swap. | R10 det |  |
| ADR06-7 | §4 Trigger check schedule L79 | Re-check and record the spend tally against the ceiling at every purchase. | R10 det |  |
| ADR06-8 | §5 Forbidden moves L86 | Apply sizing haircuts only at the rail-side multiplier layer; never realize them through TradingView/Pine risk-input scaling. | R14 det | → docs/spec/c1_watch_realization_multiplier_layer.md §3 |
| ADR06-9 | §5 Forbidden moves L87 | Select the Tradovate platform, never Rithmic/TradeSea, at Tradeify eval checkout. | R10 DEL | Discharged: §7 B4 records Tradovate checkout done 2026-07-18; CrossTrade-attach rationale moot after 2026-10-12 native-only ruling; second account needs own decision. |
| ADR06-10 | §5 Forbidden moves L88 | Never run the same bot concurrently at another firm (Tradeify FTA §6.6 exclusive use). | R10 det | → ops/prop_envelope_default.md §1 Tradeify row (FTA §6.6) |
| ADR06-11 | §5 Forbidden moves L89 | Never operate the rail unattended or lights-out; the E6 attended bar binds every session. | R11 abs |  |
| ADR06-12 | §5 Forbidden moves L90 | Never switch ACTIVE_FIRM; run engines on tier configs directly. | R16 DEL⚖ | Superseded: ACTIVE_FIRM deleted (substrate Phase 4, PR #572); tests/core/test_firm_constants_single_source.py asserts absence; ADR06-101 owns explicit-key selection. |
| ADR06-13 | §5 Forbidden moves L92 | Never arm unless a rail-independent own-flatten layer (CrossTrade Account Manager or operator 15:55 ET flat-check) is active; Pine force-flat alone is insufficient. | R10 det |  |
| ADR06-14 | §6 Downstream artifacts L104 | On GO, add posture, STATE executed-decision and SESSIONS pointer lines and activate the Q-RAIL-1 'On GO' list. | R34 DEL | Discharged at GO 2026-07-17: AGENTS.md standing-consequences row and SESSIONS pointers link this ADR; CLAUDE.md retired into AGENTS.md. |
| ADR06-15 | §7 Implementation plan L108 | Execute rail build steps B1–B7 in order; no step skips its predecessor. | R10 DEL⚖ | Superseded by Track B supersession (checklist Addendum 2026-10-16) and AGENTS.md arm gates; B1-B6 done, B7 route barred at Tradeify. |
| ADR06-16 | Addendum 2026-07-18 L166 | Run the pre-registered same-size control before any live-fill claim relies on MYM CME-native timing precision. | R24 DEL⚖ | Striker venue-edition MYM leg withdrawn 2026-08-04; 2026-10-19 addendum: no book-lineage case at Tradeify; accepted-book Striker MYM could revive need. |
| ADR06-17 | Addendum 2026-07-19 L195 | Perform the operator 15:55 ET broker flat-check every session that carried open risk; never design to the firm auto-liquidation as the flatten mechanism. | R10 det |  |
| ADR06-18 | Addendum 2026-07-19 L202 | When CrossTrade ships Account Manager for Tradovate, apply the EOD-flatten and DD-guard settings as a re-add, not a re-decision. | R10 DEL⚖ | CrossTrade route barred for Tradeify eval (route record 2026-10-12; Track B superseded 2026-10-16); personal-lane CrossTrade question still open. |
| ADR06-19 | Addendum 2026-07-22 Hedging L238 | Never treat the published automated hedging-breach thresholds as a safe harbour for correlated-product hedging. | R10 det | → ops/prop_envelope_default.md §4a |
| ADR06-20 | Addendum 2026-07-22 Hedging L240 | Never add a short-capable Equity Index (or offsetting, e.g. long FVS) leg to this or any same-control account while a long Equity Index leg can be open. | R10 det | → ops/prop_envelope_default.md §4a |
| ADR06-21 | Addendum 2026-07-22 Hedging L240 | Screen decorrelation candidates for Product Group and sign before scoring; compliance screens precede risk-breadth. | R24 det | → ops/prop_envelope_default.md §4a (precedence vs §2 item 6) |
| ADR06-22 | Addendum 2026-07-22 Contract cap L250 | Size each leg only within its static cap_alloc share of the account-aggregate cap; missing, oversized or zero cap_alloc halts to zero, never whole-account fallback. | R11 det |  |
| ADR06-23 | Addendum 2026-07-22 Contract cap L250 | Allocate the account contract cap by the fixed 2026-07-22 MYM/MNQ static split. | R11 DEL | Superseded: docs/adr/2026-08-26-striker-legmap-cap-release.md released split to 0/0; c1_sizing_host_reference.py reads cap_alloc 0. |
| ADR06-24 | Addendum 2026-07-22 Contract cap L250 | Never size a compliance-critical cap budget from unverified host position bookkeeping; relax to a runtime headroom check only once position truth is verified. | R11 det |  |
| ADR06-25 | Addendum 2026-07-22 Open B7 input L254 | Never linearly rescale a bust delta measured at one risk multiplier to another; barrier interaction is non-linear, so measure each rung. | R20 det | → .claude/skills/prop-firm-challenge/SKILL.md (MC methodology) |
| ADR06-26 | Addendum 2026-07-22 Open B7 input L254 | Close the corrected-geometry WATCH-1 0.50x measurement before B7 arms. | R24 DEL | Discharged: measured benign in Addendum 2026-07-24 (0.11% full-panel) and bootstrap tail cleared in Addendum 2026-07-28. |
| ADR06-27 | Addendum 2026-07-22 Flat deadline L260 | Treat Tradeify's flat deadline as 16:45 ET regular / 12:59 ET holiday-short; read every 16:59 in the 07-19 addendum as 16:45. | R17 det | → ops/prop_envelope_default.md §1 Tradeify row |
| ADR06-28 | Addendum 2026-08-04 L330 | Treat this ADR as no deployment authority; any Striker or successor deployment at Tradeify needs a superseding ADR under the de-scope's §4 triggers. | R3 abs |  |
| ADR06-29 | Addendum 2026-08-04 L334 | Land corrections where the error is read: place reader-intercepts on the artifact readers consult, not only at the superseding owner. | R30 abs |  |
| ADR06-30 | Addendum 2026-08-04 L351 | Arm only as an operator act behind M1 RESOLVED plus a separate per-session operator GO. | R10 abs |  |
| ADR06-31 | Addendum 2026-08-04 L357 | Never treat a venue de-scope as lifecycle decay; venue fit and lifecycle authorization are separate axes. | R15 abs |  |
| ADR06-32 | Addendum 2026-08-04 L359 | Do not over-read the de-scope: Tradeify-shaped research stays permitted; only redeploying the withdrawn legs is barred. | R3 det | → docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md same-day addendum |
| ADR06-33 | Addendum 2026-08-21 L367 | Take this build's B6 status from the header clarification, not the frozen §7 build-order snapshot. | R30 abs |  |
| ADR06-34 | Addendum 2026-08-24 L377 | Take operator-queue positions from STATE.md, not from ADR addendum snapshots. | R3 abs |  |
| ADR06-35 | Addendum 2026-09-01 L404 | Use freed account-cap headroom only via a separate admission decision under the third-leg target spec's screens. | R15 det | → docs/adr/2026-08-26-striker-legmap-cap-release.md §Boundary |
| ADR06-36 | Addendum 2026-10-01 L435 | Exclude feed costs (non-refundable charges for receiving market data: subscriptions, CME licences, required API fees, setup) from the $700 ceiling; count every other charge. | R10 det |  |
| ADR06-37 | Addendum 2026-10-01 L445 | Treat every feed signup or purchase as an operator act gated by D-feed (a)+(b) and CP-7; record feed costs outside the ceiling tally. | R18 det |  |
| ADR06-38 | Addendum 2026-10-02 qualification host L451 | Count production qualification-host spend outside the $700 ceiling under its own $500 cap; host provisioning and spend stay at CP-8. | R10 det |  |
| ADR06-39 | Addendum 2026-10-02 D-Q5 L457 | Exempt refundable data-access deposits and minimum balances from the $700 ceiling up to $500; any excess stays under the cap. | R10 det |  |

</details>

<details><summary><code>docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md</code> — 10 rules: 2 absorbed, 7 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR06-40 | §2 Decision L36 | Bind both variance-dominance screens (tau_risk in §9, rho line in §7) in the compose pre-registration before any engine run; fix wrong thresholds only by superseding ADR. | R23 abs |  |
| ADR06-41 | §2 item 1 L38 | Admit a composed book leg only if n_eff_risk_delta meets a pre-registered tau_risk > 0. | R24 det |  |
| ADR06-42 | §2 item 1 L38 | Never treat positive n_eff_dependence_delta (correlation breadth) as sufficient grant for a book-leg add. | R24 det |  |
| ADR06-43 | §2 item 2 L40 | Disclose rho (candidate vs book daily-$std at intended weight) before the engine run; rho >= 1.0 is presumptive reject: shrink weight a priori or drop. | R24 det |  |
| ADR06-44 | §2 Scope L42 | Apply variance-dominance screens only to book-composition admission; never to standalone lifecycle admission or as a signal-level entry filter. | R24 det |  |
| ADR06-45 | §4 Falsifier L65 | Demote the gate to advisory-only by superseding ADR if immaterial or false-rejecting by 2027-02-08 or 3 evaluations; check at each quarterly cluster and candidate close. | R28 det |  |
| ADR06-46 | §5 Forbidden moves L82 | Close a failed composed candidate; never iterate its weight to pass the screen or the engine. | R23 abs |  |
| ADR06-47 | §5 Forbidden moves L86 | Revive dependence-only breadth gating only with a datapoint where dependence-delta out-predicts risk-delta on composed bust. | R26 det |  |
| ADR06-48 | §6 Downstream L105 | Apply the template Stage-8 row, envelope item, M-21 lesson promotion and STATE pointer before Accepted. | R34 DEL | Discharged at ratification 2026-07-20: envelope §2 item 6 and M-21 lesson exist (ops/prop_envelope_default.md L31). |
| ADR06-49 | Addendum 2026-09-01 ruling L213 | A session deciding a new book-leg admission must explicitly rule on re-arming envelope §2 item 6, citing this addendum; a revived producer alone is not re-arm. | R24 det |  |

</details>

<details><summary><code>docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md</code> — 51 rules: 9 absorbed, 37 detail, 5 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR06-50 | §Status L8 / Addendum 2026-07-31b | Never set dry_run=false (arm) while M1 is not RESOLVED; the gate's object is the arm, not the send. | R10 abs |  |
| ADR06-51 | §2 M1 item 1 L156 | Record every received attempt in the ops-owned versioned append-only JSONL stream with immutable event variants, including unauthorized, non-JSON and error events. | R11 det |  |
| ADR06-52 | §2 M1 item 2 L171 | Give each received attempt a new event_id; keep order_id as the stable B1 signal identity for dedupe and joining. | R11 det |  |
| ADR06-53 | §2 M1 item 3 L176 | Never persist secrets, bearer tokens, raw authenticated URLs or raw payloads in telemetry; store allow-listed fields and hashes; a detected secret blocks release. | R12 det |  |
| ADR06-54 | §2 M1 item 4 L181 | Never report HTTP 200, sent=True or a CrossTrade RECEIVE as a fill or verified execution; verification needs downstream broker evidence. | R11 abs |  |
| ADR06-55 | §2 M1 item 4 L184 | On an uncertain send or post-send persistence failure, record transport_unknown, alert CRITICAL, block that leg's risk-add, reconcile with broker; never auto-retry. | R11 det |  |
| ADR06-56 | §2 M1 item 4 L189 | Parse broker response bodies only after their live schema is captured and frozen; treat unknown bodies as unverified. | R11 det |  |
| ADR06-57 | §2 M1 item 5 L192 | Join operator-attested CrossTrade/Tradovate evidence to rail events and reconcile to exactly six fixed verdicts (CHAIN_OK through NO_FLAT_CONFIRM). | R11 det |  |
| ADR06-58 | §2 M1 item 6 L202 | Halt any entry/add whose pre-send decision cannot be durably persisted to the event ledger. | R11 det |  |
| ADR06-59 | §2 M1 item 6 L204 | Never block exit/flat on telemetry, equity, DD, lifecycle or constants failure; classify signal_type first, relay best-effort, alert CRITICAL. | R11 det |  |
| ADR06-60 | §2 M1 item 7 L213 | Size adds only from durable broker-confirmed base fills (partials use filled qty), surviving restart and cleared only by confirmed flatness; never from intended qty. | R11 det |  |
| ADR06-61 | §2 M1 item 8 L221 | Append each event under a cross-process lock with flush+fsync and monotonic seq; a malformed tail blocks armed risk-add until operator repair, never silent truncation. | R11 det |  |
| ADR06-62 | §2 M1 item 9 L229 / §4 L343 | Declare M1 RESOLVED only when all §4 items 1-11 hold, including a deployed notification channel with operator acknowledgement; a test double cannot pass. | R10 det |  |
| ADR06-63 | §2 M1 L244 | Accept manual broker evidence only under attended posture; replace it with automated downstream truth before any unattended authorization. | R11 det |  |
| ADR06-64 | §2 M2 item 3 L258 | Never use execution-fidelity metrics (ECR, slippage, reject rate) as lifecycle-decay triggers; Call-1 PF and Call-4 own authorization evidence. | R15 det |  |
| ADR06-65 | §2 M2 items 3-4 L259 | Author a fresh Q-NAS-ECR successor Pre-Q (never edit frozen Q-NAS-ECR-1) and freeze MNQ/MYM fidelity thresholds before reading M2 live results. | R23 abs |  |
| ADR06-66 | §2 M3 item 1 L271 | Reuse existing lifecycle machinery; never add a second tier/state writer or reimplement decay_breach; lifecycle writes stay down-only via lifecycle_state.json. | R15 det |  |
| ADR06-67 | §2 M3 item 2 L274 | Return AMBIGUOUS on missing or thin data; never fabricate PF, fill missing trades, or count AMBIGUOUS as a breach. | R15 det |  |
| ADR06-68 | §2 M3 item 3 L276 | Block M3 until venue-native per-leg PF baselines and sigma panels are pre-registered and admitted; never relabel CFD baselines or revive retired anchors. | R23 det |  |
| ADR06-69 | §2 M3 item 4 L280 | Treat Call-1 MIN_TRADE_COUNT as provisional until its own pre-registration ratifies it. | R23 det |  |
| ADR06-70 | §2 M3 item 5 L283 | Keep Call-4 beta cohesion separately specified; never fabricate a cohesion result, change its constants, or bundle it into the M1 hot path. | R15 det |  |
| ADR06-71 | Layer and ownership boundary L293 | Keep hot-path telemetry and reconciliation in ops; lifecycle_call1 stays the statistical harness, core/lifecycle.py sole authorization owner, Sentinel governance-only. | R37 det |  |
| ADR06-72 | Layer and ownership boundary L301 | Never change Pine, sizing constants, allocations, DD rules, lifecycle values or B1 order semantics while implementing monitoring. | R14 abs |  |
| ADR06-73 | §4 RESOLVED item 8 L361 | Never rest correctness on CrossTrade order_id idempotency; treat it as unproven (since disproven) and give every payload a fresh tag. | R11 abs |  |
| ADR06-74 | §4 AMBIGUOUS L392 | Stay disarmed while real strategy JSON, broker evidence, notification proof or a unique fill join is unavailable. | R10 det |  |
| ADR06-75 | §4 Revert action L397 | If M1 is FALSIFIED, revert the monitoring commit, restore dry_run=true and supersede with a corrected architecture. | R10 det |  |
| ADR06-76 | §4 Trigger check schedule L401 | Check the M1 falsifier at every implementation commit, Stage 1 and Stage 2, the first five armed sessions after RESOLVED, then lifecycle cadence. | R28 det |  |
| ADR06-77 | §5 Forbidden moves L410 | Never reinstate live_journal, ecr_rolling, Copygram/DXTrade gates or Alchemy counterfactuals; they are design reference only. | R18 abs |  |
| ADR06-78 | §5 Forbidden moves L436 | Never treat M1 completion as evidence the strategy edge survives; it proves observability, not profitability. | R15 det |  |
| ADR06-79 | §6 Risks L478 | Export and back up session event evidence off the Fly volume in secret-free form. | R11 det |  |
| ADR06-80 | §6 Downstream artifacts L489 | Build telemetry module, reconciler, acceptance validator and artifact, runbook M1 gate, and PIPELINES/STATE/SESSIONS updates. | R34 DEL | Discharged: telemetry module, validator and M1_MONITORING_ACCEPTANCE.json exist; status RESOLVED 2026-09-14. |
| ADR06-81 | §7 Phase 0 L517 | Give any operator-notification provider choice its own dependency and secret-handling review. | R12 det |  |
| ADR06-82 | §7 Phase 1 L528 | Refuse to arm unless a writable events_log_path is configured. | R10 det |  |
| ADR06-83 | §7 Phase 3 L557 | Record M1 acceptance in a secret-free, mechanically validated artifact with fixture hashes, test commit, event ids, verdict, acknowledgement, drills and operator signoff. | R10 det |  |
| ADR06-84 | §7 L580 | Keep each monitoring phase a separate commit and review boundary; never claim M2/M3 maturity before their data gates clear. | R21 det |  |
| ADR06-85 | Addendum 2026-07-31 L734 | Discharge item 5 only from unarmed Stage 1 (real strategy signal, dry_run=true, expected non-zero sizing); never collapse Stage 1 into armed Stage 2. | R10 det |  |
| ADR06-86 | Addendum 2026-07-31 L736 | Never silently redefine item 5 to accept live evidence; write dry_run_strategy_signal_event_id only via the operator-signed A8 edit, never --allow-live. | R10 det |  |
| ADR06-87 | Addendum 2026-07-31 item 3 L740 | Revisit the item-5 deletion decline after 4 qualifying attended Stage-1 sessions without discharge; never auto-delete or relax; elapsed date is not a fired review. | R28 DEL⚖ | Discharged: item 5 recorded in M1_MONITORING_ACCEPTANCE.json, status RESOLVED 2026-09-14; trigger could re-apply to a new instance's M1. |
| ADR06-88 | Addendum 2026-07-31 L778 | Complete the §2b clean mid-bar re-measurement independently of M1 as an execution-quality question. | R11 DEL⚖ | Moved to Q-SIGID-1 (briefs INDEX: DORMANT-OTHER 2026-10-15); S2b closed-bar host reads §2b EQUAL; close-or-keep is operator's. |
| ADR06-89 | Addendum 2026-07-31b Forbidden 1 L867 | Record knowing deviations past a gate as deviations; never ratify them retroactively or treat them as precedent. | R21 abs |  |
| ADR06-90 | Addendum 2026-07-31b Forbidden 2 L870 | Never credit a gate for outcomes other mechanisms produced; no send occurring is not evidence the gate worked. | R21 det |  |
| ADR06-91 | Addendum 2026-07-31b Forbidden 4 L876 | Disarm before armed_until lapses, and keep host-availability defects separate from M1. | R10 abs |  |
| ADR06-92 | Addendum 2026-07-31b Falsifier L882 | If a third armed session occurs with M1 unresolved, make c1_rail_arm --arm refuse unless the acceptance artifact reads RESOLVED. | R10 DEL⚖ | Discharged: ops/c1_rail/c1_rail_arm.py now calls validate_m1_acceptance(require_resolved=True); AGENTS.md states the interlock. |
| ADR06-93 | Addendum 2026-07-31b §10 L906 | Execute audit hooks against the stored text, record expected outputs, and assert on live-assertion forms rather than total counts. | R33 abs |  |
| ADR06-94 | Addendum 2026-07-31b §10 hook 4 L951 | Read a non-empty arm-interlock hook as 'a gate exists', not as validation of the acceptance artifact. | R10 DEL⚖ | Superseded: c1_rail_arm.py validates the artifact with require_resolved=True; AGENTS.md §Live-execution owns the current interlock-scope caveat. |
| ADR06-95 | Addendum 2026-08-24 L971 | Discharge item 5 with an evaluate-hook test strategy on the ruled host; never a canned hand-POST, NullStrategy, fabricated event id or withdrawn Striker redeploy. | R10 det |  |
| ADR06-96 | Addendum 2026-08-24 L975 | Enable daemon emit only under a strategy emit GO; the 08-24 GO covers a test strategy only, and dry_run=false stays forbidden. | R10 det |  |
| ADR06-97 | Addendum 2026-09-11 L983 | Use as Stage-1 item-5 input only an operator-attended controlled input: a genuine just-closed bar of the named venue contract injected within the ceremony window. | R10 det |  |
| ADR06-98 | Addendum 2026-09-11 L986 | Never read the item-5 event as certifying any live feed; feed readiness, price identity and symbol mapping stay separately owed. | R18 det |  |
| ADR06-99 | Addendum 2026-09-11 L988 | Never use a TradingView alert webhook as bar transport, an eval-account Tradovate API session, or an unamended delayed feed as M1 input. | R18 det |  |
| ADR06-100 | Addendum 2026-10-01 L1027 | While #571 is parked, keep dry_run=true and arm no legacy leg (including the M1 Stage-1 test leg); deploy #571 before any legacy re-arm or ceremony. | R10 det |  |

</details>

<details><summary><code>docs/adr/2026-07-22-challenge-era-substrate-retirement.md</code> — 25 rules: 8 absorbed, 10 detail, 7 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR06-101 | §Status L3 / §2E L206 | Select firms only by explicit FIRM_RULES key and pass firm rules and account basis explicitly; never reintroduce an import-time default firm. | R16 det |  |
| ADR06-102 | §Status L3 | Keep historical challenge semantics frozen in core/historical_challenge.py; never use them as living defaults. | R14 det |  |
| ADR06-103 | §2A-C L138 | Delete OANDA CSVs, Dukascopy caches and Pepperstone anchor bytes from active manifests, preserving filenames and hashes in an LTM tombstone. | R19 DEL | Discharged: MANIFEST_DIRS lacks OANDA (scripts/check_data_manifests.py); tombstone pruned to private archive per docs/ltm/notes/2026-08-23-substrate-phase-6-completion.md. |
| ADR06-104 | §2B L155 / §4 Revert L305 | Never restore OANDA/Dukascopy adapters, runnable retired panels or a challenge-class anchor; a future need requires a new ADR and fresh venue data. | R18 abs |  |
| ADR06-105 | §2C L167 | Keep MC engine-correctness tests on committed synthetic fixtures with planted-defect sensitivity, without vendor bytes or historical pass-rate assertions. | R13 det |  |
| ADR06-106 | §2C L174 | Keep historical anchor numbers in docs/mc_anchor_history.md as retired evidence, never a validator input, root-doc headline or live invariant. | R20 abs |  |
| ADR06-107 | §2D L177 | Delete the continuous-lot account/multiplier spine only after extracting tearsheet and a zero-consumer sweep. | R31 DEL | Discharged: ops/accounts.py absent; tearsheet kept in ops/cli.py (Phase 2, PR #485). |
| ADR06-108 | §2D L185 | Preserve or relocate csv_parser.STRATEGY_DAYS while scripts/validate_params.py consumes it as a parameter-drift gate. | R31 DEL | Condition lapsed: scripts/validate_params.py absent, hub retired 2026-08-03 (ops/instruments/NAS100.md); STRATEGY_DAYS remains in core/csv_parser.py. |
| ADR06-109 | §2D L193 / §2E L212 | Never remove or weaken DD_TRIGGER, DD_SCALE, BASE_RISK, lifecycle multipliers, the r_eff sizing law, dd_geometry types or active firm rows as cleanup. | R14 det |  |
| ADR06-110 | §2E L215 | Admit no new dd_geometry policy-registry row without pre-registration, re-MC, both-halves regime gate and an ADR. | R14 det |  |
| ADR06-111 | §4 Pre-acceptance gate L257 | Accept the retirement only after operator-checkout anchor reproduction, offline rollback inventory, recorded panel release, consumer dispositions and baselines. | R31 DEL⚖ | Discharged: Phase 0 returned RESOLVED 2026-07-22, all five §4 conditions met (ADR Status line). |
| ADR06-112 | §4 Post-acceptance falsifier L294 | Prove each phase behavior-preserving in its own commit; any miss reverts that phase, and no later phase starts while an earlier one is red. | R21 DEL | Discharged: Phases 1-6 landed (Status line PRs #477-#572; Phase 6 completion note 2026-08-23). |
| ADR06-113 | §4 Revert action L304 | Restore gitignored vendor bytes only from the Phase-0 offline copy; Git restores code and manifests, not proprietary CSVs. | R19 det |  |
| ADR06-114 | §0 L95 / Verification L574 | Run destructive vendor-byte steps only in the operator checkout; never assume bytes missing from a cloud clone were safely deleted. | R19 det | → docs/adr/2026-05-10-manifest-integrity-gate.md |
| ADR06-115 | §5 Forbidden moves L327 | Never change allocations, Pine parameters or c1 quantities to make retirement or decoupling tests pass; retirements must preserve forward behavior. | R14 abs |  |
| ADR06-116 | §5 Forbidden moves L330 | Retire a pin atomically across data, config, verifier, tests and living claims; never leave a skip-gated pin test after deleting its bytes. | R19 det | → docs/adr/2026-05-10-manifest-integrity-gate.md |
| ADR06-117 | §5 Forbidden moves L338 | Classify deletion per item: never delete CME panels, BAR EXPORT inputs, Pine manifests, c1 rail code or active firm rules for sitting near retired material. | R31 abs |  |
| ADR06-118 | §6 Risks L381 / §7 Phase 0 L405 | Run reverse-dependency audits with rg --no-ignore before deletion; indexed search can miss gitignored dependents. | R31 det | → docs/operational_rules.md §16 |
| ADR06-119 | §6 Downstream artifacts L389 | Update root docs, mc_anchor_history, superseded ADR headers, configs, gates, tests and SESSIONS during implementation. | R34 DEL | Discharged: Phase 6 docs landed 2026-08-23 (docs/ltm/notes/2026-08-23-substrate-phase-6-completion.md). |
| ADR06-120 | §7 Phase 0 step 2 L407 | Count an all-skipped verification run as a failure, never a pass. | R21 abs |  |
| ADR06-121 | §7 Phase 0 step 8 L423 | When flipping an ADR to Accepted, add all matching reverse supersession edges and regenerate docs/adr/INDEX.md in the same commit; never leave the graph red. | R32 abs |  |
| ADR06-122 | §7 Phase 6 L482 | Destroy the offline vendor-byte rollback copy only after a separate operator confirmation; mark that point of no return. | R3 abs |  |
| ADR06-123 | Addendum 2026-08-08 L594 | When a retirement darkens a frozen prereg's hooks, record the dormancy (failing hooks, cause, re-arm condition, surviving coverage) at the retiring owner. | R28 abs |  |
| ADR06-124 | Addendum 2026-08-08 (c)-(e) L614 | Read the survivor-scoring prereg's ACTIVE_FIRM hook failures as retirement, not breach (gate degraded 3 of 7); verify the Tradeify_Select_100K key directly. | R28 det |  |
| ADR06-125 | Addendum 2026-08-08 Reader-path note L629 | Land pointers to this dormancy record on W4 §2 and the STATE forward board. | R30 DEL⚖ | W4 half landed (W4 Addendum 2026-08-08 links the dormancy record); STATE pointer never landed; thin-STATE need is operator's call. |

</details>

<details><summary><code>docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md</code> — 21 rules: 9 absorbed, 8 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-1 | §5 L103 | Do not move the frozen Part A ceiling, pass floor or trailing_locking requirement to re-admit candidate #1; the input was wrong, not the bar. | R23 DEL | Overridden by operator ruling Addendum 2026-09-03; Addendum 2026-10-02 'Reading this correctly' keeps §5 as history; live gate is the dated intraday-honest re-MC. |
| ADR07-2 | §4 L87 | Restore the §4 discharge only by superseding ADR after a pre-registered candidate clears the frozen Part A gate under corrected eval geometry. | R28 DEL | Restore-trigger table superseded by Addendum 2026-10-02 ruling 3 (intraday-honest dated re-MC) and the 2026-10-06 FALSIFIED early-fail record (ADR07-15/20). |
| ADR07-3 | §4 L97; §5 L104 | Never reinstate eval drawdown-lock semantics, in firm_rules.py or a harness's local copy, without re-verified primary-source evidence that firms lock in evaluation. | R16 det | → docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md |
| ADR07-4 | Addendum 2026-08-04 L166 | Audit eval-lock state with the current hook: every trailing_locking eval tier reads the unreachable-lock idiom and the postfix check reproduces corrected figures with zero override. | R16 det | → docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md |
| ADR07-5 | §4 L92/L95 | Re-verify any published firm rule change from its primary source before relying on it in a re-score. | R17 abs |  |
| ADR07-6 | §5 L105; §10 L132 | Do not cite superseded Part A figures as current; superseded artifacts are banner-stamped, never silently edited. | R20 abs |  |
| ADR07-7 | §5 L106; §6 L111 | Do not read this research-gate withdrawal as overturning the c1 rail GO; it is a different gate and harness. | R3 det |  |
| ADR07-8 | §5 L107 | Never estimate a reduced-risk arm by linearly scaling a full-risk delta; barrier interactions are non-linear, so run the number. | R20 det | → .claude/skills/prop-firm-challenge/SKILL.md |
| ADR07-9 | §6 L113 | Close the corrected-geometry WATCH-1 reduced-risk full-panel reference before B7 arms. | R10 DEL⚖ | Discharged: CORRECTED_FULLPANEL.md published (ARCHIVED.json class_s_c1_haircut_regime_remc_2026-07-16; cited in rung ADR figure caveat 2026-08-06); WATCH-1 Striker book barred since 2026-08-04. |
| ADR07-10 | §6 L115 | Whether an undischarged falsifier shifts research priority is an operator call, not an ADR consequence. | R3 abs |  |
| ADR07-11 | Addendum 2026-08-04 L160; intercept L162; Addendum 2026-10-02 L365 | Cite eval bust figures only as EOD-clock lower bounds; do not invent new bust percentages; never size to EOD-proxy counts. | R20 abs |  |
| ADR07-12 | Addendum 2026-09-03 L245 | Read candidate #1 as re-admitted at the raised ceiling with §4 discharged, EOD-clock only; every citation carries the EOD qualifier. | R28 DEL | Withdrawn by operator ruling Addendum 2026-10-02 ruling 2 (same file): the 2026-09-03 EOD-clock re-admission/discharge no longer stands. |
| ADR07-13 | Addendum 2026-09-03 L271 | A discharged falsifier or research result is never a pass, deployment or capital authorization; those axes stay separate and revocable. | R15 abs |  |
| ADR07-14 | Addendum 2026-10-02 L358 | A clear that gates the program §4 falsifier must hold on the intraday-honest clock. | R28 det |  |
| ADR07-15 | Addendum 2026-10-02 L359-L360 | Treat §4 as undischarged until a pre-registered dated re-MC clears it on the intraday-honest clock by the hard date, read against its own pre-registration. | R28 det |  |
| ADR07-16 | Addendum 2026-10-02 L361 | A clear on exactly one tier is not a §4 discharge; the operator decides that case at the 2026-11-08 sitting. | R28 det |  |
| ADR07-17 | Addendum 2026-10-02 L373 | Do not treat a T00 screen as §4 falsifier evidence. | R28 abs |  |
| ADR07-18 | intercept L43; Addendum 2026-10-02 L371 | Correct ratified ADR or closure bodies only by dated addenda and upstream reader-intercept banners; leave frozen text byte-unedited; correct living docs like STATE.md in place. | R30 abs |  |
| ADR07-19 | Addendum 2026-10-02 L376; 2026-10-06 L387 | Mirrors of an owner's disposition link the owner and restate nothing. | R29 abs |  |
| ADR07-20 | Addendum 2026-10-06 L384 | After the dated re-MC early-fail, any subsequent §4 candidate needs fresh operator authorization. | R28 det |  |
| ADR07-21 | Verification L136 | Verify an ADR with check_brief.py --type adr and scripts/check_adr_graph.py (and status-consistency where relevant) before acceptance. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-23-c1-rung-selection-ev-objective.md</code> — 9 rules: 4 absorbed, 5 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-22 | §2 L43 | Select the already-admitted c1 book's rung by EV-per-dollar-day only among regime-robust admissible rungs; the both-halves gate is a hard admissibility precondition. | R15 det |  |
| ADR07-23 | §2 L47; §4 L87; §5 L99/L101; §7 L137 | Admit a rung above 0.50x only after a fresh pre-registered both-halves regime re-MC PASS, admitting ADR, B6 dry-fire re-run and B7 arm; acceptance or EV preference never suffices. | R15 det |  |
| ADR07-24 | §2 L49; §5 L100; §10 L144 | Keep the survivor-scoring pre-registration unedited as the candidate-admission falsifier; never edit a frozen pre-registration in place; a revert supersedes the ADR, not the pre-reg. | R23 abs |  |
| ADR07-25 | §5 L102; §3 | Do not extend the EV rung objective to candidate admission; new unproven candidates must still clear the survival gate. | R24 det |  |
| ADR07-26 | §5 L103 | Never size above the 1.00x ladder maximum; the lifecycle ladder is down-only. | R15 abs |  |
| ADR07-27 | §5 L104 | Do not use the EV objective to reopen Q-COMPOSE-1 bust-floor composition or to unpark ORB; it is c1-rung-only. | R26 abs |  |
| ADR07-28 | §4 L88-L91; Addendum 2026-08-06 table | Re-open the EV objective on live EV underperformance, or revert to bust-floor framing on un-priced survival cost, via superseding ADR; both dormant until an F3 armed book. | R28 det |  |
| ADR07-29 | Addendum 2026-08-06 L194; §4 banner L77 | Re-measure the rung on any different venue geometry before deployment, even if the rung name is unchanged; rung selection is not portable. | R16 det |  |
| ADR07-30 | Addendum 2026-08-06 L189; Status L3 | Read every 'live c1 rung stays WATCH-1 0.50x / disarmed' sentence as a dated ratification record, not a current deployment claim. | R15 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-25-instrument-profile-index.md</code> — 19 rules: 4 absorbed, 15 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-31 | §2a L44 | Give every instrument ledger a schema-valid PROFILE (machine-readable) block or an explicit no-profile marker; an unmarked ledger fails P1. | R27 det |  |
| ADR07-32 | §2a L71 | Use only the closed four-value verdict vocabulary; untested means no cell; positive structural findings go in the separate structure list. | R27 det |  |
| ADR07-33 | §2a L73 | Carry a value in a PROFILE block only where that ledger is the value's canonical home; carry everything else as a pointer. | R29 abs |  |
| ADR07-34 | §2a L75; §5 L126 | Never snapshot K_banked values in PROFILE blocks, audit notes or consult output; point at discovery_manifests/ and re-read it. | R29 abs |  |
| ADR07-35 | §2a L76 | Carry a cost hurdle with its as-stated units and a source anchor; never normalize across units; always print it with its source. | R20 det |  |
| ADR07-36 | §2a L78; Exec notes item 3 L191 | Declare a candidate's nearest mechanism class or NEW; land a NEW class in MECHANISMS.md in the same commit as its pre-registration; never invent classes mid-seeding. | R27 det |  |
| ADR07-37 | §2a L80 | Run and record the instrument_profiles cell consult for every pre-registration and harvest admission; a nonzero exit's binding prior must be named and addressed. | R27 det |  |
| ADR07-38 | §2a L82; §5 L127 | Never hand-edit ops/instruments/PROFILES.md or profiles.json; regenerate with instrument_profiles.py build; P3 fails on drift. | R27 det |  |
| ADR07-39 | §1 L32; §6 L142 | At session end, update the ledger's PROFILE block when a verdict changed and rebuild the derived view. | R27 det | → docs/operational_rules.md §10 |
| ADR07-40 | §2b L90; §5 L128 | Add PROFILE blocks only to existing ledgers; never create ledgers for un-ledgered instruments to complete the matrix; creation-on-touch stands. | R27 abs |  |
| ADR07-41 | §5 L124 | Build no semantic auto-join between profile cells and rejected_candidates.md status; link explicitly and check only link resolution. | R29 det |  |
| ADR07-42 | §5 L125 | Do not restate evidence (discriminators, statistics, bar wording) in PROFILE blocks; carry verdict rows and pointers only. | R29 abs |  |
| ADR07-43 | Exec notes item 1 L173-L180 | Cite a cell source that self-dates its verdict, preferring closure, scoping or ADR records over numbers-only RESULTS; date mismatches or unverifiable dates hard-fail. | R27 det |  |
| ADR07-44 | Exec notes item 1 L185 | Do not repoint a cell at a record that merely shares a date; leave the advisory NOTE until the verdict gets its own dated closure. | R27 det |  |
| ADR07-45 | Exec notes item 2 L190 | Inherit every applicable class-level bar into a PROFILE block's bars list; an omitted bar silently under-reports and no gate catches it. | R27 det |  |
| ADR07-46 | Addendum 2026-08-29 (a) L267 | Cite a live, running forward-test registration as the source of any CONTINGENT-FORWARD cell. | R27 det |  |
| ADR07-47 | Addendum 2026-08-29 (a) L269 | Cite a results artifact carrying a computed null-p for any INCREMENT-labelled class finding; a bootstrap CI alone does not satisfy it. | R27 det |  |
| ADR07-48 | Addendum 2026-08-29 (b) L283 | Inverting PROFILE authoring to structured front-matter requires a fresh admitting ADR, not an amendment. | R32 det |  |
| ADR07-49 | §4 L112-L118 | At the second programme-audit cycle judge the profile-layer falsifier; a thin sample (under two scoped candidates) reads AMBIGUOUS, never a default pass or fail. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md</code> — 14 rules: 0 absorbed, 11 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-50 | §2-A L40-L45 | Name ex ante for any Path-1a mechanism: WHO pays (a constraint, not a preference), WHEN it must appear, WHY it survives (capacity/awkwardness), HOW it dies. | R25 det | → docs/methodology/strategy_harvest.md §1 Req 1a |
| ADR07-51 | §2-A clause 1 L42; clause 3 L44 | Route preference or behavioral stories to Path 1b's evidence test or reject them; 'nobody has noticed' never satisfies the survival clause. | R25 det | → docs/methodology/strategy_harvest.md §1 Req 1a |
| ADR07-52 | §2-A clause 4 L45 | For constraint-flow seeds, make the decay monitor watch the constraint's own observable alongside the edge-series CUSUM. | R25 det | → docs/methodology/strategy_harvest.md §1 Req 1a(iv) |
| ADR07-53 | §2-B L47; addenda L49/L57 | Source mandated flows via zero-K structural census entries carrying four clauses, venue check, K disclosure and graveyard attestation. | R25 DEL | Clause 2-B census channel superseded by docs/adr/2026-08-24-sourcing-phase-channel-retirement.md; rank struck in strategy_harvest §2.3; required fields retired. |
| ADR07-54 | §5 L104 | Quote no PnL, edge or delta inside a census entry; the first number comes from a probe or citation under an opened pre-registration. | R25 DEL | Census channel retired by docs/adr/2026-08-24-sourcing-phase-channel-retirement.md; no census entry can open, so its no-PnL rule has no object. |
| ADR07-55 | §2-C L67; §5 L105 | Bank executed K for an operator-stopped campaign only with zero results artifacts, git-auditable non-execution, enumerated looks and examiners, and operator sign-off; otherwise bank declared K. | R23 det |  |
| ADR07-56 | §4 L95; §10 hook 4 | At programme audits check every executed-K closure enumerates its looks; one unenumerated examined read reverts all closures to declared-K retroactively. | R23 det |  |
| ADR07-57 | §4 L93 | If the first three four-clause-compliant campaigns die with the constraint observable confirmed present, revert Requirement 1a by superseding ADR. | R28 det |  |
| ADR07-58 | §5 L103 | Never launder a behavioral story through constraint vocabulary; each clause must name instrument, size driver and schedule specifically or it fails. | R25 det |  |
| ADR07-59 | §5 L106; §3 L81 | Do not loosen Clause K's cap, floor table or family pooling under this ADR; 2-C adjudicates what the ledger records, never what the cap tolerates. | R23 det |  |
| ADR07-60 | §5 L107 | Do not re-open graveyard classes via census packaging; the new-mechanism-evidence bar binds census entries identically. | R26 DEL | Census channel retired (docs/adr/2026-08-24-sourcing-phase-channel-retirement.md); general new-mechanism bar owned by docs/rejected_candidates.md under Rule 26. |
| ADR07-61 | §5 L108 | Execute adjacency/dedup attestation searches by mechanism family across rejected_candidates.md, briefs bar-rulings, closed manifests and rejected_signals.md; paste command output or the attestation is void. | R8 det | → docs/methodology/strategy_harvest.md §5 dedup attestation |
| ADR07-62 | §5 L109 | Before comparative grading of any capacity-niche claim, compute round-trip cost in delta units against the cost-law hurdle. | R24 det | *at HEAD:* changed: 'vs the 4x hurdle' replaced by entry's own net-of-cost and cost-sensitivity estimate; no universal hurdle (474f6fd8, PR #907). |
| ADR07-63 | §2-C L71 | Do not add the ST-EH-1 manifest's executed K to either family; it splits one MNQ look and one MYM look. | R23 det | → docs/methodology/strategy_harvest.md §1 Req 3 split warning |

</details>

<details><summary><code>docs/adr/2026-07-26-regime-candidate-flag-lane.md</code> — 5 rules: 0 absorbed, 5 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-64 | §2 L50-L56 | Grid-shaped campaigns may pre-register a dual-track structure; Track 1 (ratified IS selection, OOS confirm, full correction) is the only promoting lane. | R23 det |  |
| ADR07-65 | §2.2 L57-L64; §5 L122/L133 | A REGIME-CANDIDATE flag never promotes or counts as edge evidence; it only authorizes a follow-up pre-registration confirming on the reserved holdout with own K and operator GO. | R25 det |  |
| ADR07-66 | §2.3 L65-L71; §5 L125/L128 | Freeze holdout_start (holdout at least two years) and an exhaustive allowlist at Stage 0; never compute or report other per-cell holdout results; runners hard-cap at the boundary. | R23 det |  |
| ADR07-67 | §2.4 L72; §5 L130 | Count every window read used for lane-firing as a separate selection event in campaign K, banked per instrument family. | R23 det |  |
| ADR07-68 | §4 L101-L112 | If the first two flag-lane follow-ups fail their holdout confirms, retire the lane and re-bank K by superseding ADR; any holdout breach voids that campaign's flags. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-07-27-tv-agent-browser-access.md</code> — 10 rules: 2 absorbed, 7 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-69 | §2 L37 | Agents may drive a browser against TradingView for operator-directed work at human cadence, without a per-session ADR or fresh grant. | R4 det |  |
| ADR07-70 | §2.1 L41; §5 L90/L98 | If a browser tool refuses TradingView, report blocked and stop; never circumvent the browser safety allowlist or engineer around a tool refusal. | R3 det |  |
| ADR07-71 | §2.3 L61; §5 L96 | Create, modify, delete or disable TradingView alerts only with per-action operator confirmation; page reads are granted, writes are not. | R10 det |  |
| ADR07-72 | §5 L91; §2.2 L55 | Never create or use a second TradingView account; shared fingerprints can collateral-ban the main account. | R4 det |  |
| ADR07-73 | §5 L92 | Never upload private Pine to any third-party compiler or optimizer. | R13 abs |  |
| ADR07-74 | §5 L93; §2.2 L52 | Do not treat refuted TradingView egress paths (A1 DOM scrape, C) as viable; re-proposal needs new evidence, not a restated plan. | R26 abs |  |
| ADR07-75 | §5 L97; §3 L73 | No scripted, looped or unattended TradingView automation; the grant covers human-cadence, operator-directed work only. | R4 det |  |
| ADR07-76 | §5 L99; §2.2 L54 | Do not cite browser access to reopen backtest egress; manual List-of-Trades export stays the sanctioned default. | R18 det |  |
| ADR07-77 | §5 L100 | No unattended agent TradingView access during the locked live signal window; attended access is fine. | R10 DEL⚖ | Subsumed by same ADR's stricter §5 ban on all unattended TV automation (ADR07-75); S2 fork moved signal origin to the Python daemon. |
| ADR07-78 | §4 L79-L83 | On any TradingView enforcement signal or post-session alert-delivery failure, revert automatically to the 2026-06-23 posture, record it in SESSIONS and RUNBOOK; reopen only by fresh ADR. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-07-29-third-leg-symbol-occupancy-limb.md</code> — 12 rules: 4 absorbed, 6 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-79 | §2-A L56; §2-B L67; §5 L124 | Do not require an order symbol an incumbent c1 leg trades in the same account on any session it can fire, unless disjointness is shown from locked Pine session filters. | R11 det | → docs/spec/2026-07-27-third-leg-target-spec.md §7.1 |
| ADR07-80 | §2 pointer L47-L52 | Shared-symbol joint Select candidates must meet the admission ADR's implementation and parity obligations; long-only directionality does not discharge S7's execution concern. | R11 abs |  |
| ADR07-81 | §5 L125 | Never use cap donation to free a symbol-occupied day; contract cap and symbol occupancy are independent constraints. | R11 det |  |
| ADR07-82 | §5 L126 | Do not read S7 as licence to reopen cap re-allocation; cap stays owned by Q-CAPALLOC-1's successor ADR. | R29 abs |  |
| ADR07-83 | §5 L127 | Never weaken S7 to admit a specific candidate; choose an unoccupied instrument instead. | R11 det |  |
| ADR07-84 | §5 L128 | Do not treat unoccupied symbols as pre-cleared; they still face every other S/R/T/M limb, ledger bars and K banks. | R11 det |  |
| ADR07-85 | §7 Phase 2 L146 | Score S7 explicitly in the §7.1 table of the next third-leg proposal. | R11 DEL | S7 already a row in third-leg spec §7.1 (Phase 1 done 2026-07-29), so any §7.1 scoring includes it; spec SCOPE DEAD bars scoring. |
| ADR07-86 | §10 L154 | If the payload's flatten-first entry or quantity-less closeposition exit semantics change, re-derive or revert S7. | R11 det |  |
| ADR07-87 | §4 L113-L118 | Revert S7 to cap-only on venue-demonstrated independent same-symbol positions; tighten it if an S7-passing candidate interferes in dry-fire or live. | R28 det |  |
| ADR07-88 | Addendum 2026-08-06 L198-L227; §4 banner L95 | When de-scope stops falsifier inputs accruing, record limbs dormant with a re-arm condition; never read an unfired calendar check as evidence the limb held. | R28 abs |  |
| ADR07-89 | §2-C L71 | Offer Slot 2 single-incumbent weekdays only to candidates on unoccupied symbols. | R11 DEL | Historical: Striker legs withdrawn (2026-08-04 ADR) and MYM1!/MNQ1! occupancy released by docs/adr/2026-08-12-msl-mym-occupancy-release.md; spec SCOPE DEAD. |
| ADR07-90 | Addendum 2026-08-14 L244 | Treat MYM1!/MNQ1! occupancy as released for new non-Striker research; withdrawn Striker legs stay barred. | R15 abs |  |

</details>

<details><summary><code>docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md</code> — 22 rules: 8 absorbed, 8 detail, 6 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR07-91 | §2 L51 | Unpark ORB-MNQ-1 to active research targeting a payable standalone Tradeify leg. | R15 DEL | Superseded by docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md: §2 unpark decision no longer in force; ORB-MNQ-1 re-PARKED, target FALSIFIED. |
| ADR07-92 | §4 L111-L119 | Re-park ORB on any trigger: halt on engine/Pine clock disagreement (T1), intraday-honest bust (T2), hard date (T3), sibling exhaustion (T4). | R28 DEL | §4 trigger table superseded by docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md (T1 PASS, T2 ruled FIRED). |
| ADR07-93 | §4 L118; §5 L131 | Change or loosen a falsifier trigger only by superseding ADR; never silently edit decision text. | R32 abs |  |
| ADR07-94 | Addendum 2026-07-31c L298; Addendum 2026-08-02 L423-L435 | Never invent, tighten or choose a falsifier-trigger reading after seeing data; route ambiguous trigger readings to an operator ruling. | R23 abs |  |
| ADR07-95 | §5 L125 | Never choose an exit time on backtest P&L; keep the D5 full-session clock pin; a different exit is a new candidate with its own K. | R23 det |  |
| ADR07-96 | §5 L126 | Do not freeze a k policy on the defective-clock panel or quote its dollar paths as current. | R20 DEL | Discharged: Phase 3 regenerated scorecard on correct clock 2026-07-31 (RESULTS_v02_clock_kgrid); ORB re-parked by 2026-08-03 repark ADR. |
| ADR07-97 | §5 L127 | Do not re-add conditioning gates to ORB-MNQ; the frozen pre-registration forbids them and any gate makes a new candidate. | R23 abs |  |
| ADR07-98 | §5 L128 | Do not iterate a failed composed candidate's book weight; a failed composed candidate closes. | R26 abs |  |
| ADR07-99 | §5 L130 | Do not reopen Candidate A (MYM ORC) or R5/P2 under cover of the ORB in-part supersession. | R26 abs |  |
| ADR07-100 | Addendum 2026-07-31b L230 | Do not author a harvest-lane pre-registration for the catalog failed-ORB-fade seed; it is a known Stage-0 kill. | R26 det |  |
| ADR07-101 | Addendum 2026-07-31b Ruling 1 L238 | A manifest banks K when it closes, not while open; leaving one open reserves no room and closing one frees none. | R23 det |  |
| ADR07-102 | Addendum 2026-07-31b L239 | Spending a family's last Cap seat is an operator decision, not an author's. | R23 DEL | Superseded by docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md (K_eff=K_intrinsic, families never exhaust); ORB Addendum 2026-08-29 records it. |
| ADR07-103 | Addendum 2026-07-31b Ruling 2 L241-L246 | Route ORB-complement fade work as K=0 Stage-0 extraction under the fade program; no register_search open, manifest or K spend. | R23 DEL⚖ | ORB re-parked (2026-08-03 ADR); fade program body cold-stored though CATALOG/ARCHIVED.json still list ACTIVE; operator confirms routing is spent. |
| ADR07-104 | Addendum 2026-07-31b L250 | Any new search, including spending a Cap seat, requires its own frozen pre-registration at that time. | R23 abs |  |
| ADR07-105 | §7 Phase 3 L175 | Never pin a gitignored Pine or private source from a checkout that cannot persist the bytes, such as an ephemeral cloud-agent VM. | R13 det | → scripts/check_pine_manifest.py |
| ADR07-106 | §7 Phase 3 L175 | Re-enabling GitHub Actions repo-wide is an operator decision. | R3 DEL | Discharged: Actions live again (scripts/githooks/post-merge notes PR limb verified 2026-08-19); main requires skills (3.12). |
| ADR07-107 | Addendum 2026-08-02 L332 | Derive intraday excursion as the position's side-aware worst post-entry mark, not session min(Low); apply identical block indices to paired panels. | R24 det | → .claude/skills/prop-firm-challenge/SKILL.md |
| ADR07-108 | Addendum 2026-08-02 L384; docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md §3 L80 | Before reporting a delta from a local re-implementation, prove it reproduces the production or published baseline. | R0 det | → .claude/skills/verify-source/SKILL.md |
| ADR07-109 | Addendum 2026-08-02 L395-L399 | Treat the intraday_low arm as still a lower bound (EOD-denominated peak); never read p99 DD as intraday-honest; widening the peak is its own re-MC. | R20 det |  |
| ADR07-110 | Addendum 2026-08-02 L405 | Record venue facts as verbatim quote, source, date read and scope; a clause silent on scope reads BROAD. | R17 abs |  |
| ADR07-111 | §6 L158; Addendum 2026-08-02 L437 | Carry an item into the STATE operator queue only if it earns operator hours. | R34 abs |  |
| ADR07-112 | Addendum 2026-08-29 L506 | Repair sweeps for a changed formula must also match paraphrased restatements, not just its symbolic form. | R30 det | → .claude/skills/blast-radius/SKILL.md |

</details>

<details><summary><code>docs/adr/2026-08-02-pepperstone-feed-retirement.md</code> — 13 rules: 4 absorbed, 6 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-1 | §2-A L57 | Treat CME futures TV exports (core/data/tv_exports/cme/) as the canonical live feed; there is no canonical CFD feed, which never means no canonical feed. | R18 abs |  |
| ADR08-2 | §2-A L59 | Keep historical CFD-era numbers under their provenance labels as readable record only; give them no successor and never cite them as live. | R20 abs |  |
| ADR08-3 | §2-B L62 | A5 regime check and P1 Pepperstone export are retired, not deferred; no export is owed and A5 is struck from Class A. | R18 DEL | Executed 2026-08-02; lab/analysis/regime/ absent at HEAD; Pepperstone retirement itself covered by Rule 18 retired-feeds clause. |
| ADR08-4 | §5-3 L174; §3 alt 4 L141 | Do not re-point the retired A5 at CME panels and call it A5; a venue-native regime monitor is a new instrument needing its own design. | R28 det |  |
| ADR08-5 | §2-C L73; §5-2 L172 | Do not decide fork A1 by default or on an invented A5-substitute number; any A1 decision names the venue-native evidence it rests on. | R20 det |  |
| ADR08-6 | §2-D L100 | Treat the owed venue-native regime monitor and the orphaned decompound HOLD limb-2 as one obligation; until built, record the HOLD as having no live falsifier. | R28 det |  |
| ADR08-7 | §2-D L107; §5-4 L176 | Never build the owed forward regime monitor as a pass-rate, and never re-run the both-halves gate as if its answer were unknown. | R24 det |  |
| ADR08-8 | §2-E L114; §7 L201 | Remove the Pepperstone dirs from the manifest contract and delete their bytes only after a hash-verified offline copy and tombstone exist. | R19 DEL | Executed 2026-08-02; scripts/check_data_manifests.py MANIFEST_DIRS lists only cme, bar_data, external. |
| ADR08-9 | §2-F L124; §5-6 L181 | Keep core/data/bar_data/ in the manifest contract as frozen panels (usable, not regenerable); do not delete it under this ADR. | R19 DEL | Superseded by 2026-08-03 bar-data ADR §2 (ADR08-15: CME micros only, frozen); AGENTS §Public-clone posture keeps bar_data frozen. |
| ADR08-10 | §4 L151 | Within 90 days, if a live decision needs a Pepperstone-only number, restore from the offline copy and re-admit by superseding ADR; reproduction-only needs get read-only restore. | R18 det |  |
| ADR08-11 | §5-1 L169 | Do not destroy the Pepperstone offline rollback copy as part of this retirement; destruction needs a separate ruling after §4 resolves. | R3 abs |  |
| ADR08-12 | Addendum 2026-09-01 L246 | Register a panel in PANELS_BY_BROKER only after an admitting ADR. | R18 det |  |
| ADR08-13 | Addendum 2026-09-01 L255 | Never rewrite a ratified ADR's body or decision text; record corrections, rulings, scope changes and stale-hook dispositions as dated addenda or superseding ADRs. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-03-bar-data-cfd-and-candidates-retirement.md</code> — 7 rules: 1 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-14 | §2 L42; §6 L93 | Delete CFD-era bar_data panels and the tv_exports/candidates tree after a hash-verified offline backup; strip them from bar_data/SHA256SUMS. | R19 DEL | Executed 2026-08-03; bar_data/SHA256SUMS lists only six CME M15 panels; core/data/tv_exports/candidates absent. |
| ADR08-15 | §2 L43-48; §5-1 L83 | Keep bar_data/ flat, CME micros only, in the manifest contract and frozen; never delete the micro panels under this ADR. | R19 det |  |
| ADR08-16 | §2 L45-47; §5-2 L84 | Keep tv_exports/cme/ (including PARKED trade-lists) and external/ unchanged in the three-dir manifest contract; do not delete PARKED trade-lists under this ADR. | R19 det |  |
| ADR08-17 | §2 L50; §5-5 L87 | Let historical lab scripts that loaded deleted CFD or candidate paths stay unrunnable; never re-point them at CME panels and call the old study runnable. | R18 det |  |
| ADR08-18 | §4 L67 | Within 90 days, if a live decision is blocked on a deleted CFD bar or candidate file, restore offline and re-admit by superseding ADR; reproduction-only gets read-only restore. | R18 det |  |
| ADR08-19 | §5-3 L85 | Do not destroy the CFD-bar/candidates offline rollback copy as part of this retirement. | R3 abs |  |
| ADR08-20 | §5-4 L86 | Do not build a CME bar regenerator or rewire parse_bar_export.py without a separate producer ADR. | R19 det |  |

</details>

<details><summary><code>docs/adr/2026-08-03-claude-md-futures-refocus.md</code> — 12 rules: 3 absorbed, 6 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-21 | §2 L39 | Keep the root agent docs futures-first: Purpose describes the prop-portfolio futures program; CFD/challenge-era content survives only as pointer lines. | R29 det | → docs/adr/2026-07-16-root-doc-charter-dedup.md |
| ADR08-22 | §2 L39; §3 L63 | Give each standing decision in root docs at most one pointer line plus a one-line consequence and its ADR link. | R29 abs |  |
| ADR08-23 | §2 L45; §5-2 L83; §6 Risks L102 | Keep one aggregated era-closure pointer line for closed CFD/challenge-era decisions only; never delete it; new posture decisions get their own line. | R29 DEL⚖ | AGENTS.md carries no era-closure line (grep empty); refocus Addendum 2026-09-01 ruled hook #3a historical-only; rule forbids own removal. |
| ADR08-24 | §2 L47 | Keep the Strategy Reference table byte-intact and machine-pinned as the locked legacy book while trimming root docs. | R14 DEL⚖ | Superseded by Phase C ADR 2026-08-23 (CLAUDE table retired); live owner core/strategies/CATALOG.md §Locked parameter record. |
| ADR08-25 | §5-1 L82 | Never change locked parameters, sizing keys, §Protection constants, lifecycle, LEG_MAP or Pine as a ride-along to doc cleanup, retirement or file moves; changes need own governance. | R14 det |  |
| ADR08-26 | §2 L45; §5-4 L85 | Keep the posture intro to standing invariants; put incident chronicles in their owning runbook, never re-expanding the intro one incident at a time. | R29 abs |  |
| ADR08-27 | §5-3 L84; §7 L115 | Do not start CFD-strategy code retirement from §7's scope sketch; it needs its own admitting ADR, engine pre-flight and operator lifecycle disposition. | R15 DEL | Executed under 2026-08-23 coldstore Phase B/C ADRs (refocus header Superseded-in-part-by Phase C). |
| ADR08-28 | §7 L117 | Keep Striker DJ30/NAS100 sizing keys as live c1 inputs through any CFD-leg retirement; remove only the venue-less CFD legs. | R14 det | → docs/adr/2026-08-23-strategy-coldstore-phase-c.md |
| ADR08-29 | §7 L118 | Retain the vendor-free 4-leg synthetic fixtures in tests/core/test_mc_synthetic_engine.py through any strategy-leg removal. | R14 det | → AGENTS.md §Strategy Reference |
| ADR08-30 | §4 L72; §6 verdict rule L104 | If a decision error is attributed to a fact this re-charter demoted, restore that block class by superseding addendum, never silent regrowth; checked at quarterly reviews. | R29 det |  |
| ADR08-31 | Addendum 2026-08-03a L163 | Keep PIPELINES.md to unique data-flow content; correct posture facts there by pointing at the owning doc rather than restating them. | R29 abs |  |
| ADR08-32 | Addendum 2026-09-01 L187 | Treat ADR audit hooks an operator ruling marks historical-only (here §10 #1-#3a) as dated snapshots: do not repair them or expect them to pass. | R32 det |  |

</details>

<details><summary><code>docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md</code> — 13 rules: 4 absorbed, 7 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-33 | §2 L39 | Treat ORB-MNQ-1 as PARKED with its payable Tradeify_Select_100K-leg target FALSIFIED; unpark only via superseding ADR and fresh operator GO. | R26 det |  |
| ADR08-34 | §2 table L57 | Open discovery manifests bank no K toward the family tally (Addendum 2026-07-31b Ruling 1). | R23 abs |  |
| ADR08-35 | §4 R1 L96; Addendum 2026-08-30 | On any T2-harness re-run, a miss beyond ±1.0pp or a broken control A/B/G halts and voids this ADR's basis pending a superseding ADR. | R28 DEL⚖ | R1 harness run_t2_intraday_bust.py deleted by Great Prune 283d1de; Addendum 2026-08-30 records dormancy; restorable from private archive. |
| ADR08-36 | §4 R2 L97 | If Tradeify $100K geometry loosens so k=1 clears both frozen survivor limbs, unpark only with fresh operator GO and superseding ADR, never automatically. | R26 det |  |
| ADR08-37 | §4 R3 L98; §5-3 L111 | Run this ORB construct at another firm only with fresh operator GO, pre-registration and a survivor-scoring pass there before unparking; no target-shopping after seeing data. | R23 det |  |
| ADR08-38 | §5-1 L109; §5-7 L115 | Never loosen or tighten a §4 trigger or falsifier limb after seeing data; change it only through a superseding ADR (Known Trap #12). | R23 abs |  |
| ADR08-39 | §5-2 L110; §10 L184 | Do not read this ADR as rejecting ORB-MNQ as a mechanism; keep its rejected_candidates entry target-scoped and out of the concept-intake dedup machinery. | R26 det | → docs/rejected_candidates.md |
| ADR08-40 | §5-4 L112 | Parking, venue de-scope or catalog labels are not lifecycle decay: make no lifecycle write for them; demote only on Call-1 evidence; never spend RETIRED on a deployment fact. | R15 det | → docs/methodology/strategy_lifecycle.md |
| ADR08-41 | §5-5 L113 | Do not spend the MNQ Cap seat under cover of this ADR; Cap-seat spending is an operator decision. | R23 DEL | MNQ Cap seat SPENT via Q-CAPA-1 (ops/instruments/MNQ.md N16; family-K Amendment 2026-08-18). |
| ADR08-42 | §5-6 L114 | Quote the intraday-honest ORB-MNQ Tradeify bust figure, not the superseded EOD arm; neither arm's p99 DD is intraday-honest. | R20 det |  |
| ADR08-43 | §6 L131 | Promote the falsifier-construction defect (limbs that never bind account survival) to methodology_lessons.md on its third independent firing. | R23 det |  |
| ADR08-44 | §3 alt D L74; §7 Phase 1 L163 | Use in-part supersession when only part of an ADR is reversed: target stays Accepted with reciprocal Superseded-in-part-by; full supersession forces an LTM stub. | R32 abs |  |
| ADR08-45 | Addendum 2026-08-30 L224 | A falsifier whose input can no longer accrue is not in force; the retiring ADR records the dormancy and re-arm condition by dated addendum, never an in-place edit. | R28 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-03-params-toml-gate-retirement.md</code> — 12 rules: 1 absorbed, 9 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-46 | §2 L44; §6 L88 | Retire core/config/params.toml and scripts/validate_params.py with their fixtures; pre-commit and CI must no longer call validate_params. | R38 DEL | Executed: core/config/ and scripts/validate_params.py absent at HEAD. |
| ADR08-47 | §2 L46 | Methodology skills (inqhiori, programme-audit, brief-authoring) must not restate operational constants; keep check_skills_no_constants wired into pre-commit, CI and Makefile. | R29 det | → scripts/README.md#skill-lifecycle |
| ADR08-48 | §2 L47 | Path-liveness checks only that committed parent dirs declared in core/strategies/MANIFEST.sha256 exist; its params.toml leg is retired. | R38 det |  |
| ADR08-49 | §2 L48 | verify_lock_anchors reads only live dd_protection/firm_rules sources (DD literals parseable, historical Guardian in safe band); no toml Forward/Action routing. | R14 det |  |
| ADR08-50 | §2 L49 | Source the recall denylist's locked risk %-forms from firm_rules._BASE_RISK decimals and canonical Python/AGENTS.md, never a derived toml mirror. | R14 det |  |
| ADR08-51 | §5-1 L79 | Do not reintroduce a derived params.toml or equivalent hub mirror without a new ADR. | R29 det |  |
| ADR08-52 | §5-2 L80 | Never weaken check_pine_manifest, path-liveness or skill no-constants gates to make a retirement go green. | R38 det |  |
| ADR08-53 | §5-4 L82 | Do not claim the params.toml retirement discharges the separately gated CFD code retirement (Guardian/Aegis). | R15 DEL | CFD code retirement executed by 2026-08-23 coldstore Phase C ADR; the caution has no remaining object. |
| ADR08-54 | §4 L71 | If by 2026-11-08 a live defect traces to Pine/dd_protection/firm_rules skew the retired hub would have caught and surviving gates miss, open a pairwise-gate ADR, no mirror. | R14 det |  |
| ADR08-55 | Addendum 2026-08-08 (c) L133 | Pine is canonical for strategy behavior; dd_protection.py and firm_rules.py are canonical for live-sizing constants; check_pine_manifest plus MANIFEST.sha256 guard integrity. | R14 abs |  |
| ADR08-56 | Addendum 2026-08-08 (d) L137 | In frozen preregs whose && hooks were darkened by params.toml retirement, run the surviving git diff --stat limb on core/ and the c1 sizing host instead. | R28 det |  |
| ADR08-57 | Addendum 2026-08-08 L143 | Write audit hooks that distinguish absent from unchanged: guard git diff pathspecs with test -e, and put independent limbs on separate lines, not A && B. | R33 det | → .claude/skills/brief-authoring/SKILL.md |

</details>

<details><summary><code>docs/adr/2026-08-04-family-k-bank-disclosure-not-gate.md</code> — 12 rules: 3 absorbed, 9 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-58 | §2 L47 | Compute K_eff = K_intrinsic, the seed's own within-search trial count; Clause K passes iff floor(K_eff) is at most Cap 1.0, i.e. K_eff at most 3. | R23 det |  |
| ADR08-59 | §2 L56; §5-3 L103; §4 trigger 2 L91 | Compute K_banked(family) from closed manifests and disclose it in every pre-registration §K block and screen row; it never gates; omission is a screen defect to repair. | R23 det |  |
| ADR08-60 | §2 L59; §5-1 L101; §5-2 L102 | Count every variant a design selects among (sweeps, gates, exits, best-of-K, tried-and-discarded) in its K_intrinsic; never declare K_intrinsic=1 for a design that searched. | R23 abs |  |
| ADR08-61 | §2 L57; §5-5 L105 | Do not loosen Cap 1.0, DSR at least 0.95 or the V = 1/n pin under cover of K-rule changes; they stay frozen. | R24 det |  |
| ADR08-62 | §5-4 L104 | Do not re-propose a mechanism the family record falsified because K no longer blocks it; rejected_candidates re-proposal bars still bind. | R26 abs |  |
| ADR08-63 | §4 L87 | If a seed promoted at K_eff = K_intrinsic fails out-of-sample replication with at least 3 prior family nulls, supersede with a graded family term calibrated on, and citing, the failures. | R23 det |  |
| ADR08-64 | §4 H L84 | Keep recording research nulls prominently and permanently; if nulls stop being recorded, the family K term must return. | R23 det |  |
| ADR08-65 | §7 Phase 3 L145 | Never edit frozen pre-registrations to match changed doctrine; add a reader-intercept where they state a superseded rule as current. | R23 abs |  |
| ADR08-66 | §6 L134; §7 Phase 4 L146 | Amend instrument-ledger findings made false by a rule change as correct-under-prior-rule and superseded; never delete them. | R27 det |  |
| ADR08-67 | §10 L163 | lab/discovery/register_search.py must never sum family K banks. | R23 det |  |
| ADR08-68 | Amendment 2026-08-18 L182 | A Notice-phase screen that closed a discovery_manifests entry banks its K against K_banked(family); a seed-fixed re-score of the same construct banks once. | R23 det |  |
| ADR08-69 | Amendment 2026-08-18 L182 | A Cap-seat spend (K_intrinsic=1, seat SPENT) banks +1 to the family tally without a harvest manifest; campaign-local disclosure rows bank nothing. | R23 det |  |

</details>

<details><summary><code>docs/adr/2026-08-04-firm-rules-eval-lock-fix-applied.md</code> — 10 rules: 3 absorbed, 6 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-70 | §2 L44 | Set dd_lock_offset_usd to the unreachable 1_000_000.0 idiom on every trailing_locking eval tier, keeping dd_type trailing_locking. | R16 DEL | Applied 2026-08-04: both trailing_locking eval blocks in core/firm_rules.py read 1_000_000.0; test_mc_preflight floor guards. |
| ADR08-71 | §4 not-admissible L77; §6 risks L108 | Never restore the eval lock offset to the old value to match old published numbers or to make a candidate pass. | R16 det |  |
| ADR08-72 | §0 L22; §3 L58 | Never model 'no lock' with dd_lock_offset_usd=None, which disables the trailing_locking drawdown check; use the 1_000_000.0 idiom. | R16 det |  |
| ADR08-73 | §4 T2 L74 | If a firm's primary source says evaluation applies drawdown locking, revert to the published lock on affected tiers only via superseding ADR; recheck at each 90-day venue re-verify. | R16 det |  |
| ADR08-74 | §4 T3 L75 | Any new trailing_locking FIRM_RULES tier must state in a comment which phase it models; block it at engine pre-flight otherwise. | R16 det |  |
| ADR08-75 | §5-1 L87 | Do not read the eval-lock fix as re-deciding the 07-22 §4 discharge withdrawal or as manufacturing a Part A clearer. | R3 det |  |
| ADR08-76 | §5-3 L89; §3 L61 | Never recompute dated historical RESULTS.md files to a new default; add a SUPERSEDED pointer banner to the historical artifact instead. | R30 abs |  |
| ADR08-77 | §5-4 L90 | Do not widen the eval-lock fix to Bulenox or BluSky tiers; their trailing dd_type never reads the lock offset. | R16 det |  |
| ADR08-78 | §6 Risks L107 | Treat engine eval bust figures as lower bounds against intraday breach enforcement unless produced intraday-honest. | R20 abs |  |
| ADR08-79 | §0 gitignore pre-flight L28 | In an ADR §0, run the gitignore pre-flight: Pine is gitignored, so read or cite no Pine source; SHA256-verify restored vendor CSVs against tracked manifests before use. | R13 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-04-iterate-closure-exit-mandatory.md</code> — 17 rules: 5 absorbed, 11 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-80 | §2 item 1 L57-66 | End every non-grandfathered closure in docs/briefs/closures/ with a typed ## Iterate block: Verdict used, Model update, Next (exactly one INTEGRATE\|ITERATE\|STOP), Routing, Board write. | R28 det |  |
| ADR08-81 | §2 item 1 L64-65 | For Next: ITERATE include an entry packet (frozen constraints, positive carry-forwards, forbidden re-opens, K/$ budget); ITERATE and STOP also state a stop rule or re-proposal bar. | R28 det |  |
| ADR08-82 | §2 item 1 L67 | Write the forward disposition once, in the Iterate block, replacing ad hoc Dispositions, Forward or Re-proposal sections. | R28 det |  |
| ADR08-83 | §2 item 2 L68 | Pre-register each new Pre-Q brief's §6 per-verdict disposition as INTEGRATE, ITERATE or STOP with action, return target or bar; coarse routing is allowed for AMBIGUOUS. | R33 det |  |
| ADR08-84 | §2 item 2 L68; §5-6 L113 | Never amend a §6 disposition or a signed closure's Iterate block mid-flight, nor reopen a sibling Q with the same H and looser gates. | R23 abs |  |
| ADR08-85 | §2 item 2 L68 | A closure may elect a branch other than the pre-registered one only by quoting the frozen §6 row and stating why the other branch fired. | R28 det |  |
| ADR08-86 | §2 item 3 L69 | STOP is a ratified third exit branch: Iterate with budget zero, recording why no re-entry is warranted and the re-proposal bar. | R28 det |  |
| ADR08-87 | §2 item 4 L70 | Default dispositions (guidance, arguable): RESOLVED to INTEGRATE; FALSIFIED to STOP with bar; AMBIGUOUS/VOID/ABORT to ITERATE; MOOT/operator-stopped to STOP. | R28 det |  |
| ADR08-88 | §2 item 1 L64; §5-3 L110 | Naming a successor under Next: ITERATE never opens it; opening a successor Q requires a fresh operator GO. | R28 abs |  |
| ADR08-89 | §2 item 5 L71 | The closure Iterate block owns the per-Q forward disposition; a STATE forward-board row is its labeled pointer mirror; SESSIONS Open/next is the session carry. | R29 abs |  |
| ADR08-90 | §2 item 6 L72; banner L15 | Gate 14 runs WARN while this ADR is Proposed and HARD once Accepted, self-arming from the ADR Status. | R38 DEL | Superseded 2026-09-08: scripts/README.md#closure-enforcement fixes HARD; checker no longer reads ADR Status. |
| ADR08-91 | §2 Scope L75; §5-2 L109 | Keep gate 14 scoped to docs/briefs/closures/; extending it to lab RESULTS or adjudication notes needs an ADR edit (supersede in part), not a flag. | R28 det |  |
| ADR08-92 | §2 Effective L74; §5-1 L108 | Apply the Iterate mandate forward-only; never retro-edit grandfathered closures to add Iterate blocks. | R33 abs |  |
| ADR08-93 | §5-4 L111 | Never add semantic completeness checks to gate 14; it checks token presence only, and content quality stays authoring and audit judgment. | R38 det |  |
| ADR08-94 | §5-5 L112 | Do not invent or normalize a closure-verdict taxonomy; keep the verdict as filed and type only the disposition. | R28 det |  |
| ADR08-95 | §4 L96 | At the first methodology audit at least 3 months post-acceptance, then quarterly, check the ceremony, friction and drift limbs; supersede per limb if one fires. | R28 det |  |
| ADR08-96 | §0 L37 | Keep the STATE forward board pointer-only (date or criterion plus owner link); delete closed rows rather than striking them. | R34 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-04-strategy-coldstore-phase-a.md</code> — 8 rules: 0 absorbed, 3 detail, 5 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-97 | §2 L48 | Cold-store unused strategy Pine and lock/changelog/candidate docs under core/strategies/_archive/<family>/, keep hot CARD stubs and CATALOG, re-pin manifest path columns only. | R13 DEL⚖ | Phase A executed (core/strategies/_archive/ present); live controls ADR08-99 and pine-manifest gate keep pins. |
| ADR08-98 | §2 L48; §6 L136 | Exclude core/strategies/_archive/ from default agent search; read archived bodies by path or force-search only. | R8 det |  |
| ADR08-99 | §5-3 L120 | Never hard-delete Pine or drop hash pins when retiring strategy surfaces; archive and re-pin instead. | R13 det |  |
| ADR08-100 | §5-4 L121 | Do not start Phase B or C because Phase A is Accepted; each needs separate operator GO and, for Phase C, its own admitting ADR. | R15 DEL | Phase B and C separately GO'd and admitted by 2026-08-23 ADRs (Phase A Addendum 2026-08-23). |
| ADR08-101 | §4 T1 L103 | If any moved file's SHA-256 differs from its pre-move manifest digest, halt moves, restore from snapshot and supersede. | R13 DEL⚖ | Phase A moves complete; window was its move commits; pine-manifest gate still hash-checks MANIFEST.sha256 pins. |
| ADR08-102 | §4 T2 L104 | Revert any BASE_RISK, lifecycle, LEG_MAP or Pine-parameter change in a PR citing only this ADR; check every such PR until Phase C admits. | R14 DEL⚖ | Check window closed at Phase C admission 2026-08-23; general ride-along ban survives in refocus ADR §5-1 (ADR08-25). |
| ADR08-103 | §4 T4 L106; Addendum 2026-09-01 L245 | Any non-_archive .pine under the six watched family dirs after Phase A claims complete is incomplete delivery; whether candidates/ is exempt remains an open operator call. | R13 DEL⚖ | Phase A delivered (_archive present); candidates/ exemption left as open operator call since Addendum 2026-09-01. |
| ADR08-104 | §6 Risks L139 | Move Pine and author hash pins only on the operator's durable machine, per --check-pin-provenance doctrine. | R13 det |  |

</details>

<details><summary><code>docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md</code> — 23 rules: 2 absorbed, 17 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR08-105 | §2 L67 clauses 1-2 | Do not deploy the locked Striker book (dj30_mym, nas100_mnq) at Tradeify_Select_100K, evaluation or funded; both legs stay withdrawn from c1. | R15 det |  |
| ADR08-106 | §2 L67 clause 3; Addendum 2026-08-04 L291 | Authorize no work whose sole justification is reaching, holding or passing a Tradeify account to deploy the two Striker legs; Tradeify base-construct research is not barred. | R15 det |  |
| ADR08-107 | Addendum 2026-08-04 L298 | Treat any new Tradeify-shaped construct as a new candidate, never as a re-entry route for the withdrawn Striker legs. | R15 det |  |
| ADR08-108 | Addendum 2026-08-04 L300 | Research surviving intake needs Stage-0 pre-registration, a K_intrinsic bound, cost-law clearance and separate operator GO before any capital or account action (in-ceiling sandbox: budget approval). | R15 det |  |
| ADR08-109 | Current scope exception L20 | Only the two pinned campaign expressions admitted 2026-09-05 are Tradeify eval-eligible; the locked-book and funded bars stay in force. | R15 det | → docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md |
| ADR08-110 | §2 table L78-79; §5-4 L126 | Do not tear down the rail, delete the M1 spine or close the account as an implied consequence of a venue de-scope; each is a distinct ruled action. | R10 det |  |
| ADR08-111 | §5-2 L124; §2 table L81 | Never cite the de-scope to pre-empt, discharge or moot the four-firm §4 falsifier; §4 discharges on simulation over the frozen four-tier set. | R28 det |  |
| ADR08-112 | §5-3 L125 | Do not read the Tradeify de-scope as ending the prop-portfolio program; it de-scopes one venue of four. | R3 det |  |
| ADR08-113 | §5-5 L127; §7 F3 L182; Addendum 2026-08-04 L297 | Do not extend Tradeify-specific de-scope arithmetic to other FRIENDLY firms, or name one Striker's successor venue, without scoring it on the cadence axis. | R16 det |  |
| ADR08-114 | §5-6 L128 | Do not read the withdrawal of the 2026-08-02 funded-phase ADR as erasing its measurements; they are carried forward here. | R31 det |  |
| ADR08-115 | §5-7 L129 | Quote only the latest funded chain-rate figure; earlier retargeted values are stale. | R20 det |  |
| ADR08-116 | §4 L105-117 | Re-scope Tradeify in only by superseding ADR when a T1-T5 trigger fires; check T4 against primary venue sources at each 90-day venue-fact re-verify. | R15 det |  |
| ADR08-117 | §4 L113 | Inadmissible re-scope routes: re-sizing legs to manufacture winning days, composing ORB in for cadence, a friendlier chain-rate harness without the eval-lock fix, or reading joint triggers singly. | R15 det |  |
| ADR08-118 | §6 L159; §7 Phase 1-3 L172 | Sync de-scope downstream: withdraw the 08-02 ADR, add posture and STATE pointers, append MYM/MNQ dispositions, mark the c1 execution-quality interest suspended. | R29 DEL | Sweep COMPLETE 2026-08-04 at its six enumerated sites (ADR Status line; Addendum 2026-08-06). |
| ADR08-119 | Addendum 2026-08-06 L322 | Read 'sweep COMPLETE' as certifying only the six enumerated sites; bound completion claims to the sites actually verified and name wider residue. | R21 abs |  |
| ADR08-120 | Addendum 2026-08-22 canon point 2 L401; forbidden L424 | Exclude a Tradeify clearance from the §4 count only by a dated, independent finding that the frozen simulation no longer proxies the venue, never by the de-scope alone. | R28 DEL⚖ | Addendum 2026-08-22 still Proposed/unratified; F1 ruled directly by Accepted Addenda 2026-08-23 and 2026-09-01 without this canon. |
| ADR08-121 | Addendum 2026-08-22 canon point 3 L407 | Any §4 success claim resting on a Tradeify clearance must disclose the 2026-08-04 withdrawal and F1's ruling status; no unconditional claim while F1 is open. | R28 DEL⚖ | Proposed/unratified; F1 ruled 2026-09-01 so 'while F1 open' cannot arise; disclosure practice carried by Addendum 2026-09-01 L550. |
| ADR08-122 | Addendum 2026-08-22 forbidden L420 | Treat an external zero-authority advisor's recommendation as candidate input reconciled against the real repo text, never as authoritative over it. | R0 abs |  |
| ADR08-123 | Addendum 2026-08-23 L451 | A clearance resting on the Tradeify_Select_100K tier does not count toward §4's at-least-2-of-four requirement. | R28 DEL | Reversed by Accepted Addendum 2026-09-01 in the same ADR (ADR08-124). |
| ADR08-124 | Addendum 2026-09-01 L533 | Count a pre-registered Part A clearance at Tradeify_Select_100K toward §4's at-least-2-of-four on the same footing as Bulenox, MFFU and BluSky. | R28 det |  |
| ADR08-125 | Addendum 2026-09-01 L576; L598; L606 | The F1 counting ruling discharges nothing: candidates still need pre-registration, full Part A bust and pass-rate scoring and G8 admission; exploratory sweeps are not clearances. | R24 det |  |
| ADR08-126 | Addendum 2026-09-01 L604 | Do not cite the F1 reversal to loosen §4's frozen ceiling, tiers, pass-rate floor or 2026-11-08 date. | R28 det |  |
| ADR08-127 | Addendum 2026-09-01 L600 | Do not read the F1 reversal as finding the 08-23 ruling wrong; it is a new operator election with the prior ruling preserved. | R3 det |  |

</details>

<details><summary><code>docs/adr/2026-08-05-blusky-inactivity-unsourced-encoding.md</code> — 14 rules: 3 absorbed, 7 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-1 | §2 item 2 L49 | firm_kwargs must raise when inactivity-ON is requested for a tier flagged inactivity_rule_sourced=False unless allow_unsourced_inactivity=True is passed explicitly. | R16 det |  |
| ADR09-2 | §2 item 2 L49 | Treat a FIRM_RULES tier without the inactivity_rule_sourced key as sourced; only an explicit False flag engages the unsourced-inactivity guard. | R16 det |  |
| ADR09-3 | §2 item 1 L47 | Mark both BluSky_Premium tiers inactivity_rule_sourced=False, retaining the 30-day value under an OPEN DEFECT block. | R16 DEL | Superseded by 05b ADR: core/firm_rules.py L463-464 now encodes BluSky 22 idle bdays with inactivity_rule_sourced=True. |
| ADR09-4 | §4 T2 L81 | Any new FIRM_RULES tier whose inactivity limit is not traceable to a published activity rule must carry inactivity_rule_sourced=False and be blocked at engine pre-flight. | R16 det | → docs/adr/2026-08-05b-blusky-inactivity-rule-sourced.md §4 T3 |
| ADR09-5 | §4 T3 L82 | Build inactivity barriers only through firm_kwargs, never by reading inactivity_max_idle_days directly; if the guard proves bypassable, repair it and treat interim figures as unlabelled. | R16 det |  |
| ADR09-6 | §4 T4 L83 | Banner any artifact that quotes an inactivity-ON BluSky figure as a measurement without stating it rests on an unsourced assumption. | R20 DEL | BluSky tier sourced (firm_rules.py L464 inactivity_rule_sourced=True per 05b); no unsourced BluSky figure remains; superseded-figure banner kept by ADR09-37. |
| ADR09-7 | §4 not-admissible L85; §5 L98 | Never delete or default away an unsourced-provenance flag to make a run proceed; pass the acknowledgement keyword, which leaves a greppable trace. | R16 det |  |
| ADR09-8 | §5 L97; §4 L85 | Never substitute a sibling firm's venue rule value for a firm whose rule is unsourced, in code or prose. | R20 abs |  |
| ADR09-9 | §3 L66 | Do not silently map an unsourced inactivity limit to INACTIVITY_OFF as a conservative default. | R16 det |  |
| ADR09-10 | §5 L95 | Treat a flagged unsourced venue figure as an assumption, never as a measurement; containment is not sourcing. | R17 abs |  |
| ADR09-11 | §5 L96 | Do not read the BluSky provenance ADRs as electing or excluding a successor venue; F3 stays operator-owned. | R16 DEL | Moot: F3 ruled by S1 ADR §2 F3 (no successor migration; reopening needs fresh GO + new ADR), kept as ADR09-49. |
| ADR09-12 | §5 L99 | Do not widen the dd_lock_offset_usd eval-lock fix to trailing-drawdown tiers (Bulenox, BluSky). | R16 abs |  |
| ADR09-13 | §4 trigger schedule L89 | Re-check BluSky's activity rule at each 90-day venue-fact re-verify, re-check new tiers on addition, and check guard/labelling at each programme audit. | R17 det | → docs/adr/2026-08-05b-blusky-inactivity-rule-sourced.md §4 schedule |
| ADR09-14 | §4 revert action L87; §5 L100 | Never edit an accepted ADR's §2 decision in place or loosen its §4 triggers; author a superseding ADR instead. | R32 DEL | Superseded by ceremony-tiering ADR 2026-09-08 revision: dated revisions with immutable prior allowed; 'replaces ... prohibition on slimming accepted decisions'. |

</details>

<details><summary><code>docs/adr/2026-08-05-strategy-venue-binding-axis.md</code> — 18 rules: 1 absorbed, 16 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-15 | §2 L74; §2.1 L78 | Place every strategy fact at exactly one level: BOOK, VENUE EDITION (strategy@firm-tier) or DEPLOYMENT (#account); each level owns a disjoint class of facts. | R15 det |  |
| ADR09-16 | §2.1 L84 | If a fact would change when the same mechanism ran at another firm, record it at venue-edition level or deeper; keep venue facts out of book-level artifacts. | R15 det |  |
| ADR09-17 | §2.4 Ruling 1 L114-127 | Give each venue edition its own authorization state (CANDIDATE, SCREENED, ACTIVE, WATCH-1/2, WITHDRAWN, SCREEN-DEAD, RETIRED); WITHDRAWN means venue-fit failure, not decay. | R15 det |  |
| ADR09-18 | §2.4 Ruling 2 L138 | Record 'screen-dead at venue X' as an edition-level SCREEN-DEAD state, never as a book-level death. | R15 det |  |
| ADR09-19 | §5 L213; §2.4 L134 | Never use an edition transition to move a book lifecycle state, or vice versa; edition events never modify M_book. | R15 det |  |
| ADR09-20 | §5 L211; §2.4 L136 | Do not wire the M_book x M_edition x DD_SCALE composition into live sizing without its own ADR, engine pre-flight and operator GO. | R15 det |  |
| ADR09-21 | §5 L212 | Do not edit core/lifecycle.py's ladder, multipliers, STRATEGY_KEYS or _validate_ladder for venue binding; the edition axis is additive and separate. | R15 det |  |
| ADR09-22 | §2.6 L165-167 | Record venue editions in ops/venue_editions/<firm_tier>.md (strategy, edition state, cap_alloc, symbol, screen verdict+date, deployment pointer); book stays in lifecycle owners, deployment in LEG_MAP. | R15 det |  |
| ADR09-23 | §4 T1 L194; §6.1 L227 | Record every venue-scope decision (venue election or withdrawal) as an edition-state transition in the registry, not as prose. | R15 det |  |
| ADR09-24 | §2.6 L168 | Strategy descriptors may carry an optional fourth slot '@<venue-tier>:<edition-state>'; absence means a book-level statement. | R15 det |  |
| ADR09-25 | §5 L215 | Register only venue editions that are live or under active consideration; do not retro-fit editions for historical venues. | R15 det |  |
| ADR09-26 | §5 L216 | Do not treat an empty edition set at a venue as a programme verdict or as evidence the venue is unviable. | R15 det |  |
| ADR09-27 | §5 L217; §3 L180 | Do not build a machine-readable edition registry or validator without a separate decision. | R36 abs |  |
| ADR09-28 | §5 L214 | Neither ORB-MNQ-1's edition SCREEN-DEAD nor its book CANDIDATE state licenses reopening it; reopening needs a fresh GO plus a survivor-scoring pass. | R26 det |  |
| ADR09-29 | §2.5 L151-161 | Read third-leg screen limbs by level: S5/S7 and R1-R4 are deployment-level (vacuous while the account is empty); T1-T5 and M1-M3 are book-level and binding. | R15 det |  |
| ADR09-30 | §4 T2 L195 | Keep ops/venue_editions/*.md reconciled with LEG_MAP, firm_rules.py and live rail config; any unreconciled disagreement at a quarterly audit falsifies the axis. | R28 det |  |
| ADR09-31 | §4 T3-T4 L196-197 | At the 2026-11-08 audit, count new venue-fact-at-book-level claims (>=2 falsifies) and confirm edition rows were maintained during venue activity. | R28 det |  |
| ADR09-32 | §7 Phases 1-3 L256-262 | Create ops/venue_editions/Tradeify_Select_100K.md with the three already-true rows, add lifecycle pointers, and date-note the third-leg spec. | R15 DEL | Discharged: ops/venue_editions/Tradeify_Select_100K.md exists with edition rows (Phases 1-3 landed 2026-08-23). |

</details>

<details><summary><code>docs/adr/2026-08-05b-blusky-inactivity-rule-sourced.md</code> — 8 rules: 2 absorbed, 6 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-33 | §2 item 1 L45; §4 not-admissible L82 | Convert a venue's calendar-day activity rule into the engine's idle business-day count when encoding; never encode the printed calendar number literally. | R16 det |  |
| ADR09-34 | §2 item 3 L49; §5 L94 | Retain the allow_unsourced_inactivity guard and its synthetic-tier tests while no shipped tier uses them; it gates the next unsourced onboarding. | R16 det |  |
| ADR09-35 | §4 T1 L77 | If BluSky publishes a non-30-day evaluation activity rule or scopes §3.3 to trading days, re-encode the limit and re-score dependent successor-venue evidence. | R17 det |  |
| ADR09-36 | §4 T2 L78 | If BluSky redefines 'inactive' as login- or payment-based, revert the field to unsourced containment (flag False). | R17 det |  |
| ADR09-37 | §4 T4 L80; §5 L96 | Never quote BluSky's superseded pre-2026-08-05b inactivity exposure figures as current; banner any artifact that does. | R20 abs |  |
| ADR09-38 | §5 L92 | Do not read 'sourced' as 'faithful': disclose that a discretionary venue closure clause is modelled as an absorbing barrier. | R20 det |  |
| ADR09-39 | §5 L93 | Do not loosen a venue limit because enforcement is discretionary or warning-first; model the rule as enforced. | R17 det |  |
| ADR09-40 | §3 L66 | Correct superseded RESULTS or frozen bodies with reader-intercept banners and addenda at read sites, not in-place rewrites of the measured body. | R30 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-06-candidate-call1-action-on-breach.md</code> — 5 rules: 2 absorbed, 2 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-41 | §2 L42; frozen pins L48-49 | On a Call-1 decay breach for a CANDIDATE strategy (or any standing outside _LADDER_ORDER), emit OPERATOR_REVIEW_FLAG only; Hold, standing change or retirement are operator acts. | R15 det | → docs/methodology/strategy_lifecycle.md §Call 1 |
| ADR09-42 | frozen pins L50-51; §5 L92 | No code path may autonomously demote or retire from CANDIDATE, or add CANDIDATE to _LADDER_ORDER/TIER_MULTIPLIER, without a superseding ADR. | R15 det |  |
| ADR09-43 | §5 L87-88 | Do not use the Call-1 ADR to extend STRATEGY_KEYS to ORB, write ORB lifecycle_state.json, arm Cap or set Cap fire thresholds. | R3 abs |  |
| ADR09-44 | §5 L89 | Keep the PF-CUSUM decay replay harness flag-only (OPERATOR_REVIEW_FLAG); do not rewrite it into a demotion path. | R15 DEL | Harness lab/analysis/orb/orb_mnq_2026-07/run_decay_monitor_replay.py absent (dir holds only RESULTS.md); demotion bar enforced by core/lifecycle.py (ADR09-42). |
| ADR09-45 | §5 L90 | Link decay and Cap RESULTS for PF floors and Cap deltas; do not restate those owned values. | R29 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-07-loop-s1-environment-ratification.md</code> — 10 rules: 4 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-46 | header L3 | Agents may place, exit or cancel orders only at operator direction for the specific act; trade.submit is an operator act never grantable in a card. | R10 abs |  |
| ADR09-47 | §5 L88; §2 L56 | Agents may not place trades; token trades for account activity stay operator-only. | R10 DEL⚖ | Superseded by operator Addendum 2026-09-30b (live owner, restated as ADR09-46); S1 header 2026-10-01 marks it historical. |
| ADR09-48 | §2 F2 L40 | Keep the c1 rail built, warm and disarmed (dry_run=true) at the incumbent Tradeify_Select_100K eval, account registered; no teardown or successor re-point. | R10 det |  |
| ADR09-49 | §2 F3 L42; §4 limb 3 L78; §5 L89 | Make no successor-venue migration; reopening needs a fresh GO and a new ADR consuming Q-VENUEGEO-1, never a silent redefinition. | R16 det |  |
| ADR09-50 | §2 L45; §5 L86 | Withdrawn Striker legs stay barred from redeploy at Tradeify (de-scope clauses 1-2). | R15 abs |  |
| ADR09-51 | §5 L87 | Do not arm, set dry_run=false or deploy under these ADRs; arming and deployment need M1 RESOLVED plus separate per-session operator GO. | R10 abs |  |
| ADR09-52 | §5 L91 | Do not treat these ADRs as M1 RESOLVED or B7 discharge; dry_run_strategy_signal_event_id is written only by the operator-signed A8 edit, never fabricated. | R10 det | → docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md |
| ADR09-53 | §5 L90 | Do not edit locked BASE_RISK/allocation constants, Pine or lifecycle multipliers under these environment ADRs. | R14 abs |  |
| ADR09-54 | §4 limb 1 L76 | If the incumbent eval account is found lapsed or breached, treat S1 as falsified and reroute via Q-VENUEGEO-1 under a fresh GO. | R28 det |  |
| ADR09-55 | §4 schedule L80 | At the next armed-session GO or the 2026-11-08 audit, confirm the rail is still warm/disarmed at the incumbent and the Striker bar is intact. | R10 det |  |

</details>

<details><summary><code>docs/adr/2026-08-07-loop-s2-signal-host-fork.md</code> — 5 rules: 0 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-56 | §2 L147 | New-strategy live signals originate from a Python-native daemon POSTing B1 JSON to the listener; Pine/TradingView is research/export only. | R11 det |  |
| ADR09-57 | §2 L147; §5 L190 | TradingView login or UI-actuation automation is absolutely prohibited. | R11 det |  |
| ADR09-58 | §2 L154; §4 limb 2 L180 | Discharge M1 item 5 only with a real strategy signal from the ruled host at expected non-zero dry-run sizing; canned, live-armed or zero-qty evidence never discharges. | R10 det |  |
| ADR09-59 | §5 L189; §4 limb 3 L181 | Do not build the signal daemon without an Accepted S2b spec and a separate dated operator build GO. | R11 DEL | Discharged: build GO given 2026-08-08; ops/c1_signal_daemon/ and deploy/c1_signal_daemon/ exist. |
| ADR09-60 | §5 L193 | Run the signal daemon as a separate Fly app (c1-signal-daemon) with its own state volume; never share the listener's volume or peak_equity. | R11 det | → docs/adr/2026-08-08-s2b-signal-daemon-build.md §2 |

</details>

<details><summary><code>docs/adr/2026-08-07-loop-s5-bounded-promotion-lane.md</code> — 8 rules: 2 absorbed, 6 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-61 | §2.1 L53 | Automation may promote a packet into the capped sandbox only if it passes validate_promotion_packet and refute_promotion_packet against ceilings read at promotion time. | R15 det |  |
| ADR09-62 | §2.2 L54 | The operator approves sandbox budgets, not candidates; packets carry operator_budget_approval_id and need no per-candidate GO inside ceilings. | R15 det |  |
| ADR09-63 | §2.3 L55; §5 L101 | Ceiling-crossings are operator-only: automation never edits ceilings, budgets, gates or its validator/refuter, funds accounts, or sizes past the sandbox. | R15 det |  |
| ADR09-64 | §2.4 L56 | Demotion is universal and instant; the Call 5 down-path is unchanged. | R15 abs |  |
| ADR09-65 | §2.5 L57; §5 L103 | The sandbox admit is the only up-direction exception: no autonomous path to full AUTHORIZED size, RETIRED re-entry or re-optimization; sandbox is not book membership. | R15 abs |  |
| ADR09-66 | §2.6 L58; §5 L105 | Never alter the reflex layer (dry_run interlock, armed_until, fresh idempotency tags) through promotion work. | R11 det |  |
| ADR09-67 | §2.6 L58; §5 L100 | Do not run unattended loops without a separate ADR requiring automated downstream truth per M1. | R11 det |  |
| ADR09-68 | §1 table L41-45; §5 L102; §4 L88 | Promotion packets must be artifact-only, same-units at parse, carry paired positive/negative self-tests, match freeze_commit, and pass an independent refuter; the confabulated fixture must fail. | R15 det |  |

</details>

<details><summary><code>docs/adr/2026-08-07-w1-intraday-honest-engine-remeasure.md</code> — 7 rules: 3 absorbed, 4 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-69 | §2 L155-164; §6 L209 | Complete the $0 intraday-honest re-measure of the three remaining decisions of record (intraday_low clock, no-lock dd_lock_offset_usd default) with before/after RESULTS. | R20 det |  |
| ADR09-70 | §2 item 4 L164; §4 L189; §5 L195 | Never invent or hand-edit bust, clearer or percentile figures; publish a new bust figure only with a RESULTS path. | R20 abs |  |
| ADR09-71 | §2 L166 | Label every cited EOD-clock bust figure an EOD-clock lower bound unless backed by an intraday-honest RESULTS artifact. | R20 abs |  |
| ADR09-72 | §2 L168; §4 L189 | Monkeypatch harnesses restore dd_lock_offset_usd to the captured original or skip restore; no restore-to-100 lands on main without a dated exception comment. | R16 det |  |
| ADR09-73 | §5 L198; §2 L168 | Do not retire or silently delete science harnesses without a RESULTS tombstone. | R31 det |  |
| ADR09-74 | §6 L210 | When the remaining W1 RESULTS publish, mark the firm_rules RESIDUAL EOD-clock caveat Superseded-by. | R30 det |  |
| ADR09-75 | §5 L197 | Do not edit the frozen survivor-scoring prereg body; G6/G7/tier changes only via close and reopen. | R23 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-07-w4-minimal-gate-set-dormancy.md</code> — 11 rules: 0 absorbed, 9 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-76 | §2 Live L38-41 | The live research gate set is EM0-EM5 with DSR-cap refuse at register_search open, prereg-required temporal/realism limbs, and survivor-scoring G0-G5 plus G8. | R24 det |  |
| ADR09-77 | Addendum 2026-08-08 L49-51 | Until a campaign names its prereg mechanically, read the live floor as G0-G5+G8; 'campaign prereg' means the seeking campaign's own frozen body. | R24 det |  |
| ADR09-78 | Addendum 2026-08-08 L51-53 | Re-arm a dormant gate family only on an operator GO dated after 2026-08-07; a closed campaign's frozen text never re-arms it. | R24 det |  |
| ADR09-79 | §2 Dormant L62-63; §6 L118 | Keep SPA/StepM and PBO/CPCV dormant unless a campaign prereg names their thresholds and the operator GOs, with a dated note; PBO preregs must argue leakage risk. | R24 det |  |
| ADR09-80 | §2 Dormant L64 | Do not use the universe-gate orchestrator as default promote/reject unless SPA, DSR and PBO are all re-armed for that family. | R24 det |  |
| ADR09-81 | §2 Dormant L65 | The plateau protocol is archived; reuse requires a fresh pre-registration with a same-feed baseline rule. | R24 det |  |
| ADR09-82 | §2 Dormant L66; §2 item 6 L86; §5 L112 | Breadth/risk-N_eff has no live producer: envelope §2 item 6 is report-optional, never claim it discharged, and restoring a producer needs a re-arm ADR. | R24 det |  |
| ADR09-83 | §4 L104 | Never reject a campaign solely for skipping a dormant gate that its own prereg does not require. | R24 det |  |
| ADR09-84 | §5 L111 | Do not delete the universe_gate or breadth modules. | R31 det |  |
| ADR09-85 | §2 var_trials L72 | Pass var_trials=1/n explicitly in campaigns; do not flip the universe_gate module default in the W4 PR. | R24 DEL | Superseded: Addendum 2026-08-15 flipped module default; universe_gate.py L363-365 now sets var_trials=1/n when None. |
| ADR09-86 | §2 audit board L76-80 | Leave audit rows R3 (prereg-RESULTS pairing), R5 (var_trials default) and R6 (DEFAULT_FIRM_KEY) on their scheduled repair dates. | R38 DEL | Discharged: W4 Addendum 2026-08-15 records R3, R5, R6 DONE in the gate-stack repair pass. |

</details>

<details><summary><code>docs/adr/2026-08-07-w6-rail-infra-closures.md</code> — 5 rules: 1 absorbed, 2 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-87 | §2 item 2 L177; §4 L199 | Export session evidence with ops/c1_rail/export_session_evidence.py (dry-run plan by default, --apply copies); the exporter never mutates the Fly volume by default. | R11 det |  |
| ADR09-88 | §2 item 3 L178 | Arm/disarm via c1_rail_arm.py and merge non-secret volume-config keys via write_volume_config.py (refuses unless dry_run, --force-armed only under operator GO); never hand-edit JSON. | R10 det |  |
| ADR09-89 | §2 item 4 L179; §5 L207 | Run always-on processes on an always-on host (Fly or successor); desktops are console-only for them; this does not ban route-LOCAL interactive agent work. | R41 abs |  |
| ADR09-90 | §2 item 5 L180; §5 L206 | Do not fabricate requirements-research.lock; generate it from a real research-venv freeze under a dedicated GO. | R19 DEL | Discharged: requirements-research.lock generated from real install 2026-08-22; its header cites W6 item 5. |
| ADR09-91 | §2 items 1, 6 L176, L181 | Add the CrossTrade-Tradovate relink procedure to RUNBOOK and refresh spend/NT8 lines only from facts already in RUNBOOK. | R11 DEL | Discharged one-off docs edit; RUNBOOK now private (docs/notes/rail_build/RUNBOOK.md absent from tree). |

</details>

<details><summary><code>docs/adr/2026-08-08-adr-ceremony-tiering.md</code> — 14 rules: 12 absorbed, 1 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-92 | Decision L16-22 | Create a new ADR only when the choice changes durable architecture, governance or authority, its rationale must stay discoverable, and no existing owner can hold it. | R32 abs |  |
| ADR09-93 | Decision L24-28 | Routine fixes, moves, citation repairs and elections within an approved envelope need no ADR or light-record substitute; do not inventory every choice. | R32 abs |  |
| ADR09-94 | Decision L30-33 | Keep an ADR only while its distinct rationale or authority boundary is needed; never preserve one merely because it is Accepted, old, cited or historically unique. | R31 abs |  |
| ADR09-95 | Decision L31-33 | One current owner holds each rule; ADRs carry choice and tradeoff, operating owners carry procedure, schemas, counters and live evidence. | R29 abs |  |
| ADR09-96 | Decision L35-41 | Write ADRs in Format: concise (Decision with scope, Grounds, Current owner) plus graph header and approval date; no mandatory falsifier, cadence or word-count gate. | R32 det | → .claude/skills/brief-authoring/references/adr.md |
| ADR09-97 | Decision L43-44 | Apply approved ADR changes as dated revisions of effective text with an immutable prior version; proposed branches stay separate and unapproved. | R32 abs |  |
| ADR09-98 | Decision L44-46 | Revision rights never permit changing frozen preregistrations, lock artifacts, verdict logic or evidence after a result. | R23 abs |  |
| ADR09-99 | Decision L46-49; Grounds L77 | Source-first risk review, authorization and review independence follow the change's consequence, not document length; brevity never supplies approval or relaxes evidence standards. | R35 abs |  |
| ADR09-100 | Decision L51-53 | Before consolidating or removing an ADR, read its full body and amendments, migrate every surviving constraint and reader, and disposition each obligation explicitly. | R31 abs |  |
| ADR09-101 | Decision L54-56 | Preserve incoming file, fragment and section references by repointing callers or pinning history; verify blob retrieval and tool failure behaviour before deleting. | R31 abs |  |
| ADR09-102 | Decision L58-62 | Record each removed ADR in docs/adr/TOMBSTONES.md (path, immutable commit/blob, disposition, current owner); a retained stub stays subject to A3 checks. | R31 abs |  |
| ADR09-103 | Current owner L86-87 | When moving an obligation to STATE, preserve its scanner/reader coverage. | R31 abs |  |
| ADR09-104 | Verification L91 | Mechanical form checks establish neither semantic equivalence nor ratification. | R21 abs |  |
| ADR09-105 | Grounds L74-75 | Treat the former light-share target and its November-8 omitted-apparatus review as retired by policy replacement, not passed. | R32 DEL⚖ | Historical Grounds note; grep finds light-share target/Nov-8 review only in this ADR and archived SESSIONS-2026-Q3; no live consumer. |

</details>

<details><summary><code>docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md</code> — 17 rules: 2 absorbed, 12 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-106 | §1 L44; 2-A; §4 R3 L125 | Use the corrected MNQ cohort table; never quote 0.85R as ORB/MNQ measured independent edge, and re-derive any threshold traced to that phantom cell. | R30 det |  |
| ADR09-107 | 2-B item 1 L77 | Score intake against TNEC-1's five necessary conditions (activity, honest-clock survivor gate, CI+DSR-at-K edge, independence/legality, candidate-derived sizing) for a construct or jointly-scored book. | R24 det | → docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md |
| ADR09-108 | 2-B item 2 L78; §5 L134 | MNQDTL-1 D1/D2/income targets are recorded preferences, never intake kills or side conditions; re-electing one needs fresh ratification against the corrected cohort table. | R24 det |  |
| ADR09-109 | 2-B item 4 L80 | EM1 requires net expectancy >0 after Requirement-5 costs with a pre-registered 95% CI excluding 0 and DSR >= floor_at_k(K_intrinsic); disclose the frequency-lever inversion below ~0.40R. | R24 det |  |
| ADR09-110 | 2-B item 4 L80 | Treat EM2's published cells as void provenance; re-derive each candidate's cell from its own measured edge at a stated tolerance. | R24 det |  |
| ADR09-111 | 2-B item 3 L79; §5 L140 | Re-point Q-MNQDTL-CON-1's eventual GO at TNEC-1 N-EDGE/N-SIZE; this ADR grants it no Stage-0 GO, prereg freeze or Cap claim. | R24 DEL | Discharged: Q-MNQDTL-CON-1 closed FALSIFIED 2026-08-09 (edge-cohort Addendum 2026-08-29; rejected_candidates.md entry). |
| ADR09-112 | 2-C L1 L86 | Pause the Route B OF-minute family; any future catalogue must pre-register a tradeable-object target with a cost-derived promotion floor. | R25 DEL | Superseded by docs/adr/2026-08-24-sourcing-phase-channel-retirement.md: Route B retired in full (§2-C L1 PAUSED to RETIRED). |
| ADR09-113 | 2-C L2 L87 | Draw the next intake pass only from zero- or partial-coverage channels in the ratified sourcing taxonomy; keep the structural-flow census closed. | R25 det | → docs/methodology/strategy_harvest.md §2.3 |
| ADR09-114 | 2-C L2 L87; L5 L90; §3 L110 | Never loosen harvest Requirements 1-5 to raise the finding rate. | R25 det | → docs/methodology/strategy_harvest.md §1 |
| ADR09-115 | 2-C L3 L88 | MES and MGC are back in the candidate pool; instrument election stays an operator choice, data pulls stay cost-dry-run-gated, and the instrument lane runs in parallel. | R27 det | → ops/instruments/MES.md; ops/instruments/MGC.md |
| ADR09-116 | 2-C L4 L89 | A book may be admitted if it meets N-ACT jointly with co-idleness disclosed, N-SURV composed across both regime halves, and EM5 compliance limbs. | R24 det |  |
| ADR09-117 | 2-C L5 L90 | Do not reopen MNQDTL doors C1-C11, ORB-MNQ at Tradeify, either Striker leg, Aegis-6J admission, or any safety invariant. | R26 DEL⚖ | Superseded: ORB/Aegis readmitted by operator selection 2026-09-10 and ORB route-native CANDIDATE 2026-09-25; remaining clauses held by withdrawal ADR, rejected_candidates. |
| ADR09-118 | §4 R1 L123 | Never block a TNEC-1-clear candidate informally; name any hidden gate and supersede TNEC-1 to include or strike it. | R24 det |  |
| ADR09-119 | §4 R2 L124 | If a TNEC-1-clear candidate fails the eval on a rule TNEC-1 omits, author the missing limb via a superseding spec. | R24 det |  |
| ADR09-120 | §5 L137 | Do not use the eval's thin-edge admissibility to skip DSR-at-K, harvest Requirements 1-5, or the regime-robustness gate. | R24 abs |  |
| ADR09-121 | §5 L139 | A book must not admit a negative-expectancy cadence leg. | R24 det |  |
| ADR09-122 | Addendum 2026-08-29 L259 | Future MNQ dense-1m EM construct work is a fresh seed against TNEC-1; re-proposal requires a new entry mechanism. | R26 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-08-great-prune.md</code> — 12 rules: 8 absorbed, 3 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-123 | §2 L34-40 | Retain an artifact only if pipeline-consumed, live-safety, re-proposal kill evidence, a reproducibility manifest, or a fireable open obligation (R1-R5). | R31 abs |  |
| ADR09-124 | §2 R5 L40-42 | An obligation whose check cannot fire does not qualify for retention; unfalsifiable ceremony is deletable even when signed, once its obligation is dispositioned. | R31 abs |  |
| ADR09-125 | §2 L42; §5 L137 | Revive deleted material only through fresh pre-registration under the standing chain, never by lookup. | R31 abs |  |
| ADR09-126 | §4a L109-111 | Before any deletion commit, run the quoted-path scan, pathlib-join scan, inbound-reference analysis and a full pytest; the pre-commit gate battery is insufficient. | R31 abs |  |
| ADR09-127 | §3.2 L83-86 | A future docs/ prune must start from an inbound-reference index of prose and hook citations, not links, and justify itself against the measured 4.3% precision. | R31 det |  |
| ADR09-128 | §5 L135 | Never delete the guardrail set: core/, Pine and SHA manifests, ops/c1_rail/, ops/instruments/, discovery_manifests/, prop envelope, rejected_candidates, vendor-data trees, W4 modules. | R31 det |  |
| ADR09-129 | §5 L136 | Do not restate a tombstoned decision's narrative in root instructions or STATE; the tombstone line is the record. | R29 abs |  |
| ADR09-130 | §5 L138 | Do not treat pruning as precedent for wholesale deletion of measurement evidence; R3 kill evidence stays in-tree. | R31 abs |  |
| ADR09-131 | §4 F-1/F-3 L117-119; Addendum 2026-08-14 L129 | At each programme audit, re-test retention by reading a content sample of live ADRs against Rule 16, and check tag-retrieval need and lost obligations. | R28 det |  |
| ADR09-132 | §4a #6 L107 | Keep the MC-anchor literals in the root instruction file; ops/recall/guard.py regex-parses them, so reword only alongside that parser. | R14 abs |  |
| ADR09-133 | Addendum 2026-08-29 L171-184 | The pre-prune tag is absent from the public clone; retrieve pruned bytes from the private archive per TOMBSTONES.md, with git log --follow as partial fallback. | R31 abs |  |
| ADR09-134 | §3 class manifest L46-59; §5 L139 | Execute the class-by-class prune under the snapshot tag (one commit per class) without altering any live decision. | R31 DEL | Discharged: great-prune §6 gate 'Outcome: met' 2026-08-08; classes 3, 5-8 deliberately halted per §3.2. |

</details>

<details><summary><code>docs/adr/2026-08-08-s2b-signal-daemon-build.md</code> — 20 rules: 1 absorbed, 18 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR09-135 | §2 Live CME bar source L48; header L7 | No live CME bar source is selected; Stage 1 ceremonies use only the operator-attended controlled input (option D), which certifies the chain, not feed readiness. | R18 det |  |
| ADR09-136 | §2 L48; Addendum 2026-10-02 L442-444 | Provider-specific feed implementation, signup, subscription and credential staging wait for the operator funding decision, except CP-7's adapter and emission-disabled shadow collection under CP-7 conditions. | R18 det |  |
| ADR09-137 | Addendum 2026-09-10 L141 | Never silently replace the live-feed requirement with a fixture or replay; a substitute needs an explicit amendment stating what it certifies and keeping live-feed readiness separate. | R18 det |  |
| ADR09-138 | Option E L252; Addendum 2026-09-10 L139-141 | Do not re-subscribe to Databento or restore its credentials. | R18 abs |  |
| ADR09-139 | Option F L256; Option C L233; Q3 L367 | Never rest a safety-relevant acceptance artifact on a data source whose terms forbid the use (unlicensed free sources; TradingView webhooks under ToU §3). | R18 det |  |
| ADR09-140 | Q4 L368; §0.5(1) L182; §5 L98 | Any delayed-feed proposal must amend both the acceptance window and staleness locks; never loosen §4 triggers or §2 staleness/fail-closed locks silently. | R11 det |  |
| ADR09-141 | Q2 L366 | Re-verify Tradovate eval-account API ineligibility from a primary source if option A-prime or any Tradovate feed is proposed. | R17 det |  |
| ADR09-142 | §2 Reconnect L49 | A live feed transport auto-reconnects with backoff and reports unhealthy while disconnected. | R11 det |  |
| ADR09-143 | §2 Staleness L50 | Mark the feed unhealthy when now minus last_bar_ts exceeds 2 x bar_period + 30s; use the canonical formula, never a hard-coded age. | R11 det |  |
| ADR09-144 | §2 Heartbeat L51 | Expose daemon process-up and last_bar_age_s on the daemon's own GET / JSON, separate from listener health; page on missed heartbeat for a live transport. | R11 det |  |
| ADR09-145 | §2 Fail-closed L52; §4 limb 2 L81 | On unhealthy, stale or missing feed, the daemon emits no signals of any type (entry, add, exit, flat). | R11 det |  |
| ADR09-146 | §2 Listener L54; §4 limb 3 L82; §5 L94; Addendum 2026-09-14 L428-430 | Do not change the listener B1 contract (including R-B1/R-B3 optional fields and five-field M1 compatibility) without its own authorization; send a fresh bar_time every fire. | R11 det |  |
| ADR09-147 | §2 Listener L54 | Hold the listener base URL and path token as daemon secrets, never in versioned configuration. | R12 det |  |
| ADR09-148 | §2 Strategy surface L55; Addendum 2026-08-24 L133 | Keep emit_enabled=false with NullStrategy default until a new strategy and any LEG_MAP extension receive a separate GO; test-strategy emit was GO'd only for M1 item 5. | R10 det |  |
| ADR09-149 | §2 L48 stdlib clause | Keep listener and daemon images stdlib-only under the Stage 1 disposition. | R11 det |  |
| ADR09-150 | Addendum 2026-09-11 option D L242-248; Q1 L365 | Option D ceremony: operator transcribes the manifest-named quarterly MYM bar, injects via private upload file within target+60..120s under one atomic claim, poll_interval_s <= 1. | R10 det |  |
| ADR09-151 | Addendum 2026-09-15 rev9 L436-438 | Daemon sends only authenticated ordered health/fault reports, never permission or emergency B1 flats; the listener owns incident scope and revokes all further runtime mutations. | R11 det |  |
| ADR09-152 | Addendum 2026-09-14 L428; Addendum 2026-09-15 L436-438 | After halt or incident, source recovery, rollover or restart never restore permission; resume needs fresh bounded operator approval after reconciliation evidence; acknowledgment records attendance only. | R11 det |  |
| ADR09-153 | Addendum 2026-09-14 L430 | Never emit a risk-add under HALTED, invalid or expired authorization, failed barrier or unhealthy required source; missing reports never authorize risk-adds. | R11 det |  |
| ADR09-154 | Addendum 2026-09-14 L426-428 | On incident, the listener performs qualified risk-reducing recovery dispatch for the fixed four-leg book (rev8). | R11 DEL⚖ | Superseded by S2b Addendum 2026-09-15 rev9 attended recovery (stricter live owner; header says rev9 replaces rev8 dispatch). |

</details>

<details><summary><code>docs/adr/2026-08-09-grand-tier-quintessentials-binding.md</code> — 20 rules: 2 absorbed, 16 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-1 | §2.1 L103 | Treat GRAND as the fourth tier above STRATEGIC (GRAND > STRATEGIC > OUTER > INNER); it runs the Quintessentials loop over pursuits (whole commitments). | R9 det |  |
| ADR10-2 | §2.2 L110 | GRAND only scopes pursuits; never use it to modify or relitigate strategy code, locked parameters, allocations, dd_protection, MC calibration or campaign pre-registrations. | R14 det |  |
| ADR10-3 | §2.2 L115 | Fire GRAND Update only on a tripped pre-registered falsifier; off-cycle Update likewise requires a tripped falsifier. | R28 det |  |
| ADR10-4 | §2.2 L117 | INNER (OODA) inherits Aim and Survive as standing constraints and receives no questions from GRAND. | R9 det |  |
| ADR10-5 | §2.2 L119 | Subtract removes pursuits and hands off to The Algorithm's Delete for parts; the surviving pursuit set is the Algorithm's intake. | R28 det |  |
| ADR10-6 | §2.3 L124 | Disposition pursuits only through the canonical states OPEN -> KEEP \| PARK \| MERGE \| SUBTRACT. | R28 det |  |
| ADR10-7 | §2.3 L126 | Give every PARK a named re-entry condition and expiry date; at expiry it converts to SUBTRACT unless operator renews; never relabel parks compliant without both fields. | R28 det |  |
| ADR10-8 | §2.3 L128 | Re-open a SUBTRACTed pursuit only with out-of-frame evidence plus an attached falsifier, recorded through an ADR or equivalent governance channel. | R28 det |  |
| ADR10-9 | §2.3 L131 | Enumerate and assign an owner to each residual function of a parked/subtracted pursuit or it subtracts too; a MERGE names its target and transfers residuals explicitly. | R28 det |  |
| ADR10-10 | §2.4 L144 | GRAND artifacts may not execute Delete on data/system/meta-process objects, and lower-tier artifacts may not disposition pursuits (domain-conflation guard). | R9 det |  |
| ADR10-11 | §2.5 L150 | Open a new pursuit only with a GRAND entry record (Aim, Measure, Survive resource ceiling, review date); no side-door pursuits and no grandfathering. | R28 det |  |
| ADR10-12 | §2.5 L152 | GSUB-1 backfills entry records for every existing KEEP pursuit. | R28 DEL | Discharged: GSUB-1 closed 2026-08-09 (GRAND ADR Addendum 2026-08-09, GSUB-1 closure); docs/pursuits/ a1-b2 entry records exist. |
| ADR10-13 | §2.6 L157 | Run GRAND review at the existing quarterly programme-audit gate; do not create a new standing review ceremony. | R28 det |  |
| ADR10-14 | §4 L174; Addendum L276 | Re-read the tier-load-bearing hypothesis at the 2026-11-08 quarterly audit; any demotion goes through a superseding record, never silent retention. | R28 det |  |
| ADR10-15 | §5 L199; §6 L205; Ratification L252 | Ratify only with §0 populated and GSUB-1 accepted alongside; land declared downstream updates same commit; defects close AMBIGUOUS, no silent mid-review amendment. | R32 DEL | Discharged: ratified 2026-08-09 with §0 populated, GSUB-1 accepted and downstream updates landed (Ratification note); gate cannot refire. |
| ADR10-16 | §10 L218 | At each quarterly gate run the §10 hooks: PARK records carry re-entry and expiry, no pursuit opened without entry record, zero resurrections without governance record. | R28 det |  |
| ADR10-17 | Addendum 2026-08-09 L287 | Correct a defective §10 audit hook in place; audit hooks are machinery, not frozen verdict constructs. | R32 abs |  |
| ADR10-18 | Addendum 2026-08-09 L291 | Do not read a pursuit KEEP as adjudicating any campaign inside it. | R28 det |  |
| ADR10-19 | Addendum 2026-08-19 L294 | The Great Prune was a documentation retention test (Rule 16), not a GRAND Subtract or Algorithm Delete; do not cite it as either. | R31 det |  |
| ADR10-20 | §1.5 L91; Ratification L254 | Agents propose deletions and pursuit dispositions; only the operator authorizes them (D user-gate). | R3 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-09-rejection-register-topology-and-bar-wiring.md</code> — 17 rules: 2 absorbed, 12 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-21 | §2 D1 L86 | Ratify the 5th-leg / portfolio-expansion SNAG closure, discharging the 2026-07-01 audit §5.3 mandate. | R26 DEL | Discharged: D1 ratification stamp landed at docs/rejected_candidates.md L1638 ('Operator-ratified 2026-08-09'). |
| ADR10-22 | §2 D2 L89 | A domain-level bar is operative only with a dated operator ratification stamp and a machine-consult wire (profiles.json source for instrument-scoped bars). | R26 det |  |
| ADR10-23 | §2 D2 L95 | Never cite an unratified or unwired bar as a binding constraint; authoring a bar is only a proposal. | R26 det |  |
| ADR10-24 | §2 D3 L99 | Route rejections by tier: per-direction instrument kills to ops/instruments/<SYM>.md DEAD + profiles.json; domain/cross-instrument bars to rejected_candidates.md; meta-layer signals to rejected_signals.md. | R26 abs |  |
| ADR10-25 | §2 D3 L107 | The 2026-08-03..09 window kills are discharged in the instrument ledgers and are not back-transcribed into rejected_candidates.md. | R26 det |  |
| ADR10-26 | §5 L170 | Record a genuinely cross-instrument mechanism kill in rejected_candidates.md; do not skip the domain register because the instrument ledger is easier. | R26 abs |  |
| ADR10-27 | §5 L172 | Do not widen rejected_candidates.md's admission criterion to absorb catalogue nulls, power voids or measurement pathologies. | R26 det |  |
| ADR10-28 | §5 L167 | Do not treat an instrument DEAD-table row as automatically a mechanism rejection; rows mix kills, NOT-KILLED, power voids and K annotations. | R26 det |  |
| ADR10-29 | §5 L164 | Do not cite the 5th-leg SNAG bar as having bound work before its 2026-08-09 ratification; its force runs forward only. | R26 det |  |
| ADR10-30 | §5 L174 | This ruling covers routing and operativeness only; whether a search domain is exhausted (SNAG) is a separate audit verdict. | R26 det |  |
| ADR10-31 | §2 D4 L117 | Do not cite the per-direction ledger feed as an operative stopping rule until an enforcement instrument binds it. | R26 det |  |
| ADR10-32 | §2 D4 L119; §4 L147 | Every terminal-negative closure naming an instrument needs a DEAD row in that instrument's ledger, or a dated exception. | R27 det |  |
| ADR10-33 | §2 D4 L119; §7 L201 | Dispatch the per-direction coverage check and inherited_bars hardening as a separate code+tests packet. | R38 DEL | Discharged: checker built in 4472abb2 (2026-08-28), wired as instrument-rejection-coverage; inherited_bars tests in tests/test_instrument_profiles.py. |
| ADR10-34 | §2 D5 L122 | Correct the three stale rejected_candidates.md claims at their point of use. | R30 DEL | Discharged: corrections landed with the ADR commit (§6); verified rejected_candidates.md L1643 correction and L1874 historical preamble. |
| ADR10-35 | §2 D5 L129 | Do not move or delete rejected_candidates.md without updating profiles.json source pointers, which the instrument-profiles gate resolves. | R26 det |  |
| ADR10-36 | §6 Risk L188 | Preserve MNQ's direct or inherited binding to the index-intraday raised bar; never edit the inherited_bars edge so it silently unbinds. | R26 det |  |
| ADR10-37 | §4 L147; §10 L207 | At the 2026-11-08 audit check bars cited binding carry stamp and wire and ledger coverage is complete; falsification needs a superseding ADR, never silent D2 loosening. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md</code> — 12 rules: 4 absorbed, 8 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-38 | §2 2-A L30 | Read the mapped 'instrument-selection' lever as cross-instrument only; within-instrument temporal selectivity is outside the mapped set, so route 1 is open to it. | R26 det |  |
| ADR10-39 | §2 2-B(1) L41 | Name any temporal-selectivity criterion causally a priori and freeze it at G0; never choose it post hoc or read it off a scored list. | R23 abs |  |
| ADR10-40 | §2 2-B(2) L43 | Charge K_intrinsic for every temporal-selectivity axis (criterion, threshold, window); the EM0 cap and working budget stand unchanged. | R23 det |  |
| ADR10-41 | §2 2-B(3) L45 | Keep harvest Req 1-5, DSR-at-K, cost law, regime gate and EXPLORATION/CONFIRM discipline binding unchanged on temporal-selectivity cells. | R24 abs |  |
| ADR10-42 | §2 2-C L48 | Price and hold-time levers stay exhausted, cross-index stays closed; reopen no C1-C11 door, DEAD row or CON constant; successors need fresh Q-ID, G0 and operator explore GO. | R26 det |  |
| ADR10-43 | §2 2-D L53 | Dense-1m step-1 door check must run instrument_profiles.py cell <SYM> <mechanism-id> and answer every BINDING BAR by clearing route in §0; unanswered bars block G0 freeze. | R26 det | → docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md step 1a |
| ADR10-44 | §4 T1/T2 L74 | Void a temporal cell traceable to post-hoc reading of scored CON output and re-close route 1 by superseding ADR; if a cell dies on cross-index dilution, fold temporal into selection. | R28 det |  |
| ADR10-45 | §4 T3 L76 | If any lane G0 freezes with an unanswered BINDING BAR, escalate the door check from spec prose to a gates.yml limb. | R38 det |  |
| ADR10-46 | §5 L82 | Route 1's opening is an entry permit for one named cell, not a family of moment-filter sweeps; the F2 guard stays unchanged. | R23 det |  |
| ADR10-47 | §5 L83 | Do not treat an oracle-headroom fraction (a max-order-statistic share) as an expected value. | R1 det |  |
| ADR10-48 | §5 L85 | Never skip a required consult because the answer is remembered; it is executed output or it did not happen. | R0 abs |  |
| ADR10-49 | §5 L86 | Do not read this ruling as a GO for any campaign, Cap claim, deploy, Pine change or arming. | R3 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-12-closure-disposition-coverage-hard.md</code> — 9 rules: 1 absorbed, 6 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-50 | §2.1 L53; §2.5 L57 | Arm coverage severity from this ADR's Status token (Proposed WARN, Accepted HARD), degrading to WARN when the owning ADR is missing (M-22 fail-open). | R38 DEL | Superseded 2026-09-08 by fixed HARD contract in scripts/README.md §Closure enforcement; checker no longer reads ADR Status. |
| ADR10-51 | §2.2 L54 | A campaign newly claiming a terminal verdict in INDEX or CATALOG must have a joinable closure under docs/briefs/closures/ or docs/ltm/briefs/. | R28 det | → scripts/README.md §Closure enforcement |
| ADR10-52 | §2.3 L55 | Never append campaign IDs to COVERAGE_GRANDFATHERED to clear a fire; a genuine pre-promotion gap needs a superseding ADR with evidence. | R28 det |  |
| ADR10-53 | §2.4 L56 | Keep the coverage limb narrow: no semantic-completeness, Lane:/Closed: token or C1/C4 checks under it; those need a separate decision. | R38 det |  |
| ADR10-54 | §5 L94 | Iterate-GRANDFATHERED files still count as closure records for coverage; Iterate exemption is not coverage exemption. | R28 det |  |
| ADR10-55 | §5 L96 | Do not edit the 2026-08-04 Iterate ADR's decision text in place; this ADR supersedes only its advisory-coverage clause. | R32 abs |  |
| ADR10-56 | §4 L80; §5 L97 | Check friction, false-positive and ceremony limbs at the first methodology audit 3+ months post-acceptance, then quarterly; revert by superseding ADR, never loosen triggers in place. | R28 det |  |
| ADR10-57 | Current enforcement note L15 | Verify closure enforcement with the checker and its focused tests, not the historical Status commands; severity changes need a reviewed code and operating-contract change. | R38 det | → scripts/README.md §Closure enforcement |
| ADR10-58 | §5 L92 | Do not flip this ADR to Accepted as a drive-by in its landing PR; arming is a separate operator GO stated in the PR body. | R3 DEL | Discharged: Accepted 2026-08-12 by operator GO; Status-based arming itself retired 2026-09-08 (scripts/README.md §Closure enforcement). |

</details>

<details><summary><code>docs/adr/2026-08-12-msl-mym-occupancy-release.md</code> — 4 rules: 2 absorbed, 1 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-59 | Decision L16 | MYM1!/MNQ1! occupancy is released for new non-Striker research and G0; withdrawn Striker legs reserve no headroom in ledger posture. | R27 det |  |
| ADR10-60 | Boundary L32 | Do not read the occupancy release as authorizing Striker-leg redeploy, arming, dry_run=false, or reopening S1 F2 keep-warm. | R3 abs |  |
| ADR10-61 | Decision L16; Boundary L32 | Do not delete or rewrite LEG_MAP under cover of the occupancy release; it may remain as historical map. | R3 abs |  |
| ADR10-62 | Gate L28 | Record a dated MYM/MNQ ledger disposition pointing at this ADR; MSL-C1 door-check may cite it for occupancy. | R27 DEL | Discharged: dated 2026-08-12 dispositions present at ops/instruments/MYM.md L408 and ops/instruments/MNQ.md L335. |

</details>

<details><summary><code>docs/adr/2026-08-12-msl-sourcing-channel-ratification.md</code> — 7 rules: 0 absorbed, 2 detail, 5 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-63 | §2 R-CHANNEL L56 | MSL is a named L2 sourcing channel; it does not clear the MNQBASE-1 bar by assertion; MNQ-scoped work clears it per candidate only under R-REQSCOPE. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-64 | §2 R-FRAMING L57 | Non-index MSL cards proceed under the fade spec §2.1 framing (outside the 5th-leg SNAG domain), recording the framing per card in the door-check. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-65 | §2 R-REQSCOPE L58 | Harvest Req 1b/Req 2 do not bind MSL composition; candidates enter G0/explore-confirm discipline with Req 1a delete/flip, EM0-EM5 and TNEC-1 still binding. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-66 | §4 L66 | FALSIFIED(process) or FALSIFIED(yield) under the MSL charter voids all three rulings pending a superseding ADR; check at each B7 weekly walk and registry-entry merge. | R28 det |  |
| ADR10-67 | §5 L70 | Do not re-run an exhausted sourcing channel under a new channel name; it is another pass over the same classes. | R25 det | → docs/methodology/strategy_harvest.md §2.3 Channel liveness contract |
| ADR10-68 | §5 L70 | Do not pick R-FRAMING per card by whichever reading admits it, or cite this ADR as evidence the channel works. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-69 | §7 L78 | The three MSL ruling names must resolve to identical elections in the MSL charter and this ADR. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |

</details>

<details><summary><code>docs/adr/2026-08-13-dedup-first-before-new-work.md</code> — 10 rules: 4 absorbed, 4 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-70 | §2 L45 | Before opening a lab/analysis slug, scoping core-adjacent implementation or acting on an inherited task pointer, paste literal CATALOG/INDEX search output; attestation without executed output is void. | R8 abs |  |
| ADR10-71 | §2 Scope L54 | Re-check any 'spawned as a separate task' or TODO pointer inherited from memory or a notice against current repo state before acting; never trust its text alone. | R0 abs |  |
| ADR10-72 | §2 leg 1 L47 | Track the advisor-dedup hookify rule and widen its regex to build-intent phrasing. | R8 DEL | Discharged: tracked .claude/hookify.advisor-dedup-first.md exists with build-intent regex (ADR Change history, Phases 1-5). |
| ADR10-73 | §2 legs 2-3 L48 | Add Rule 8 sub-rule 8, the archive_lab_analysis same-theme WARN, check_advisor_dedup --keywords mode and the brief-authoring link to Rule 8. | R8 DEL | Discharged: operational_rules.md Rule 8 sub-rule 8, check_advisor_dedup.py --keywords and archive_lab_analysis.py theme WARN all present. |
| ADR10-74 | §4 L81; §5 L91, L93 | Keep dedup checks advisory (exit 0); never build a hard commit-blocking semantic duplicate gate or promote the catalog-collision WARN to blocking. | R38 det |  |
| ADR10-75 | §5 L94 | Do not loosen the dedup hookify regex or Rule 8 sub-rule 8 without a dated changelog entry. | R8 det |  |
| ADR10-76 | §4 L73 | Check T1-T3 at the next quarterly audit or next same-class incident; revert by superseding ADR naming the failed leg, never editing §2 in place. | R28 det |  |
| ADR10-77 | Addendum 2026-08-15 L201 | Every new non-grandfathered closure carries a Registry: line naming a rejected_candidates.md heading or 'n/a - <reason>'. | R26 abs |  |
| ADR10-78 | Addendum 2026-08-15 L201 | Leave the 2026-08-03..08-11 registry hole to an operator pass; each backfill row is a re-proposal-bar judgment. | R26 det |  |
| ADR10-79 | Addendum 2026-08-15 L202 | Before minting a sibling ADR, brief, notice or lab slug, check for the existing owner; default to an addendum on that owner. | R29 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-13-implied-sr-report-only-fade-reopen.md</code> — 6 rules: 0 absorbed, 6 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-80 | §2.1 L49 | State implied_annualized_sr at freeze in assumed-edge screens but never admit or reject on it; cohort Sharpe figures are disclosures, not ceilings. | R24 det |  |
| ADR10-81 | §2.2 L50 | Treat the reopened fade design-region as geometry only; reopening admits no mechanism, and Stage-2/TNEC/DSR-at-K still require a pre-registered mechanism. | R23 det |  |
| ADR10-82 | §2.3 L51 | Gate measured results on DSR-at-K; never kill a measured Sharpe for exceeding the cohort figure, nor weaken DSR, cost-law, payability, worst-day or Req 1a. | R24 det |  |
| ADR10-83 | §5 L89 | Never silently restore the cohort-ceiling implied-SR FAIL in the charter, slate kill lists or a new screen; supersede this ADR instead. | R24 det |  |
| ADR10-84 | §5 L87 | Do not use the fade reopening to clear BE3, SFX-1 or other registry mechanism-family kills. | R26 det |  |
| ADR10-85 | §4 L73 | At each pre-G0 screen and quarterly audit check kill-on-SR, DSR-skip and mechanism-launder limbs; revert only by superseding ADR. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-13-msl-slate-2-design-box.md</code> — 5 rules: 2 absorbed, 1 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-86 | Decision L16 | Author MSL slate-2 cards inside the elected box (rr 2-3, target WR band, diffusion-frontier R, mandatory hard stop, k=1, no pyramiding), S2A first. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-87 | Boundary L32 | Do not loosen the eval survival bars (bust ceiling, P(pass) floor) when designing candidates. | R24 abs |  |
| ADR10-88 | Boundary L32 | Do not open the eval-sprint/retry lane under the slate-2 election. | R25 DEL⚖ | MSL §7 hard rung met 2026-10-07 (msl-program-plan.md status); channel closes pending superseding ADR; no MSL work live; operator acknowledgement owed. |
| ADR10-89 | Boundary L32 | Do not rewrite the MSL first-slate header; it remains the historical record of what slate 1 tested. | R30 abs |  |
| ADR10-90 | Boundary L32 | Do not treat Magdon-Ismail validation as an R_max recalibration; frontier dollars stay the diffusion approximation until a separate calibration artifact exists. | R20 det |  |

</details>

<details><summary><code>docs/adr/2026-08-14-repo-public-visibility-transition.md</code> — 15 rules: 3 absorbed, 8 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-91 | §2 L90; §7 L250 | Go public via fresh-repo transplant after remediation (scrub, redact, untrack, LICENSE), archive the private repo, repoint clones. | R13 DEL⚖ | Executed one-time transplant: 'Initial public release' 027a7295 (2026-08-14), Accepted 2026-08-22; live owner AGENTS.md §Public-clone posture. |
| ADR10-92 | §2 Effective L100; §7 L260 | Creating or publishing repos, visibility flips and archive changes need a separate explicit operator go, regardless of any ADR's acceptance. | R3 det |  |
| ADR10-93 | §2 L92; §5 L146 | Keep LOCK.md-family files redacted to name/version/lock-date/risk%/hash; never reintroduce locked-config or reference-backtest blocks or redact only partially. | R13 det |  |
| ADR10-94 | §6 L178, L227 | Live-sizing risk% constants (_BASE_RISK) may stay in tracked core/firm_rules.py as accepted residual disclosure; no other locked parameter values. | R13 det |  |
| ADR10-95 | §6 L204-211 | Never commit live account identifiers or real balances; tests use fake account fixtures. | R13 abs |  |
| ADR10-96 | §6 L229 | Keep executable strategy-signal ports (including lab/archive/oanda_stage1 *_stage1.py) gitignored; generic infra may stay tracked. | R13 abs |  |
| ADR10-97 | §6 L195 | Exclude docs/notes/**, docs/ltm/** and docs/superpowers/** from the public seed tree wholesale. | R13 DEL⚖ | One-time seed exclusion executed 2026-08-14; docs/notes, docs/ltm, docs/superpowers now tracked; AGENTS.md §Public-clone posture governs content. |
| ADR10-98 | §4 L125 | Within 90 days of the flip, on a visibility-caused exposure incident or Actions overage after 30 days, flip the repo private and author a superseding ADR. | R13 det |  |
| ADR10-99 | §5 L142 | Do not rewrite the repository's git history in place (filter-repo, force-push) without a new ADR justifying it. | R6 DEL | Targets archived private first-passage-archive; rewriting live main is blocked by seat_authority.yml forbidden main.direct_push and the main ruleset. |
| ADR10-100 | §5 L150, L153 | Ship LICENSE with the first public commit and seed a genuinely separate repo, not a renamed or toggled one. | R13 DEL⚖ | Executed: LICENSE in initial public commit 027a7295; separate public repo seeded; live owner AGENTS.md §Public-clone posture. |
| ADR10-101 | Addendum 2026-09-11 L349 | Cite archive-era PRs as first-passage-archive#N or the full archive pull URL, never bare PR #N; use explicit Markdown links for clickable citations. | R29 det |  |
| ADR10-102 | Addendum 2026-09-11 L357 | Cite live PRs bare only in artifacts dated on/after 2026-08-15 citing no archive-era PR; era-mixing documents use first-passage#N. | R29 det |  |
| ADR10-103 | Addendum 2026-09-11 L360 | Resolve an ambiguous historical PR number by merge commit or branch name, never by number. | R29 det |  |
| ADR10-104 | Addendum 2026-09-11 L361 | Leave existing PR references in dated artifacts as written; the SESSIONS living-header intercept disambiguates. | R30 abs |  |
| ADR10-105 | Addendum 2026-09-11 L365 | Add a report-only make-audit check for unqualified collision-range PR numbers only after a second documented misresolution, recorded against this addendum. | R36 det |  |

</details>

<details><summary><code>docs/adr/2026-08-15-analogue-modality-route-ruling.md</code> — 4 rules: 0 absorbed, 4 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-106 | Decision L14 | Algorithmic-analogue constructs (direction from price-geometry matching, no named entry geometry or theta trigger) count as a new modality lifting the CON-5 pause for that class only. | R26 det |  |
| ADR10-107 | Gate L30 | At the 2026-11-08 audit, if no analogue construct ever opened a manifest, record this ruling as inert rather than carry it as live doctrine. | R28 det |  |
| ADR10-108 | Boundary L34 | Do not use the analogue ruling to un-pause theta-parameterised entry geometry or re-admit CON-1..5 siblings by relabel; the test is absence of named entry geometry. | R26 det |  |
| ADR10-109 | Boundary L34 | Do not cite route 3 (beat the incumbent net-of-cost) for this class; it fails arithmetically on both limbs. | R26 det |  |

</details>

<details><summary><code>docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md</code> — 37 rules: 5 absorbed, 30 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-110 | §2 L45 | Run the no-counterparty channel inside futures-anomaly-discovery's --lane blind under this ADR's own authority; never cite MSL elections as its authority. | R25 det |  |
| ADR10-111 | §2 Channel boundary L47 | If a candidate's own claim names a counterparty, apply full Req-1a via MSL or harvest; only narrative-free-by-kind constructs use this channel. | R25 det |  |
| ADR10-112 | §5 FM3 L90 | Never route a nameable-counterparty or momentum-class candidate through this channel to dodge Req-1a, including by omitting the counterparty story. | R25 det |  |
| ADR10-113 | §2 item 1 L51 | Open register_search --lane blind with a mandatory --prereg before seeing results; close must compute Bonferroni, BH-FDR and K-alpha. | R23 det |  |
| ADR10-114 | §2 item 2 L52 | Freeze a train/confirm partition in the prereg before mining; mining reads only train and every confirmatory number uses only confirm. | R23 det |  |
| ADR10-115 | §2 item 3 L53 | Require DSR >= 0.95 at declared K on the confirm partition with frozen constants; never tune K/DSR/cost-law/split constants to admit a marginal seed. | R24 det |  |
| ADR10-116 | §2 item 4 L54 | Do not claim SPA/PBO universe-level correction is running; never cite the train/confirm split as equivalent to a Reality-Check/SPA pass. | R24 det |  |
| ADR10-117 | §2 item 5 L55 | Require cost-law reachability (4x round-trip) using the candidate's own confirm-partition effect in place of cohort delta. | R24 DEL | Superseded: Req 5's 4x cost-law inequality and its duplicate references deleted by operator ruling 2026-10-24 (strategy_harvest.md L32). |
| ADR10-118 | §2 item 6 L56 | Run an own-series half-split DSR check whose split point and floor are frozen in the prereg before scoring. | R24 det |  |
| ADR10-119 | §5 FM5 L92 | Never cite the own-series half-split check as satisfying, superseding or interchangeable with the canonical regime_robustness_gate. | R24 det |  |
| ADR10-120 | §2 item 7 L57 | A channel survivor must separately clear N-SURV (TNEC-1 bust and pass-probability limb) on the incumbent eval; the battery never substitutes. | R24 det |  |
| ADR10-121 | §5 FM4 L91 | Do not transplant any battery result cross-instrument (MSL no-instrument-hop basis, not Req 2); FM-4's reach to pre-G0 kills remains unruled. | R24 det |  |
| ADR10-122 | §5 FM6 L93 | Battery passage grants no deployment authorization and no Req-1a status for the S5 sandbox-up lane or any lifecycle promotion. | R15 abs |  |
| ADR10-123 | §4 L74 | Read §4 at 2026-11-08: RESOLVED on a battery+N-SURV survivor, FALSIFIED on battery-closures with none, AMBIGUOUS-HOLD if none sourced (re-test 2027-02-08); any-stage death is a strike. | R28 det |  |
| ADR10-124 | §3 L68; N=3 (d) L318 | If this channel falsifies or reports generation-dry, fall back to a source-class post-mortem; never open a third sourcing channel. | R25 det |  |
| ADR10-125 | K-cap Addendum L212 | Declare K at open with floor_at_k(K) <= CAP (currently K <= 3); refuse any open declaring a larger K. | R23 det |  |
| ADR10-126 | K-cap Addendum L214 | Report the K bracket {binding, raw} in the prereg; never report only the value that passes. | R23 det |  |
| ADR10-127 | K-cap Addendum L216 | The K ceiling is a channel property: never waive it per candidate; widening requires a superseding ADR that re-derives Cap. | R23 det |  |
| ADR10-128 | K-cap Addendum L228 | Count K honestly: no under-declared K, no splitting one search into several opens, and any wider informal exploration behind a construct is its K. | R23 abs |  |
| ADR10-129 | K-cap correction L182 | Benchmark a K-floor against both the best in-house edge and corrected published top-decile Sharpe; the bar fires only when the floor exceeds both. | R24 abs |  |
| ADR10-130 | K-cap correction L199 | Treat CAP in axis_screen.py as the operative search-size bound; never reopen Cap or waive K <= 3 because the channel is dry. | R23 det |  |
| ADR10-131 | K-cap Addendum L207 | The DSR floor is set by K, not n: trade frequency moves power, not the floor, and a train/confirm split controls bias, not K. | R23 abs |  |
| ADR10-132 | Pre-G0 Addendum L244 | A cheap-falsifier kill before register_search open is not a §4 strike; after a manifest exists any named-stage death is a strike, never reclassified as pre-G0. | R28 det |  |
| ADR10-133 | Pre-G0 Addendum L260 | Count and disclose every pre-G0 kill; report that count and whether N=3 fired with every §4 reading at quarterly audits. | R28 det |  |
| ADR10-134 | N=3 Addendum L296 | Three consecutive countable pre-G0 kills mean reporting generation-dry at the next quarterly audit regardless of §4; N is unwaivable per candidate, changed only by superseding addendum. | R28 det |  |
| ADR10-135 | N=3 Addendum (a) L312 | This ADR's running-count line is the canonical pre-G0 kill count and must be updated when a kill lands; STATE mirrors it; a deleted STATE row is no reset. | R29 det |  |
| ADR10-136 | N=3 Addendum (b) L314 | Increment only for a distinct construct killed at an executed pre-G0 screen on a dated surface; never for K>=4 refusals, variants/retunes/relabels or naming passes. | R28 det |  |
| ADR10-137 | N=3 Addendum (c) L316 | Reset the consecutive pre-G0 count only when a candidate survives its screen and opens a manifest. | R28 det |  |
| ADR10-138 | N=3 Addendum (d) L318 | Generation-dry is an audit report, not FALSIFIED; it may coexist with AMBIGUOUS-HOLD. | R28 det |  |
| ADR10-139 | N=3 FM L333 | Never write a light record or sibling ADR for a disposition-bearing falsifier threshold to dodge ceremony-tiering limb 4; amend the owner in place. | R29 abs |  |
| ADR10-140 | Naming-pass Addendum L387 | Do not author a sibling construct just to have something to screen, or open register_search so an empty naming pass counts as a strike. | R28 det |  |
| ADR10-141 | Naming-pass Addendum L375; decline L462 | New data for this channel needs a cost dry-run and separate GO; a later construct re-attests this channel's own GO and cost even on cached paid bytes. | R18 DEL⚖ | Databento retired 2026-09-10, no approved vendor; new spend stays operator act (seat_authority spend); cached-byte re-attestation reads as a routine permission the 2026-10-24 ruling deleted. |
| ADR10-142 | Addendum 2026-08-23 L438, L472 | Spend the channel's last pre-G0 kill slot only on a fresh explicit operator GO informed by the corrected count and the 08-23 decline. | R3 det |  |
| ADR10-143 | Addendum 2026-08-23 L428, L437 | Treat seams S1 (FM-4 reach to pre-G0 instrument hops) and S2 (cross-channel GO/cost transfer) as unruled; rely on neither reading without operator or superseding-ADR ruling. | R3 det |  |
| ADR10-144 | Addendum 2026-08-23 decline L460 | The CON-sibling/dense-1m doors on 6A/M6A and GC/MGC stay legally open but declined (still blocked on MNQ); an open door is not itself a proposal. | R26 det |  |
| ADR10-145 | Addendum 2026-08-23 Part C L439 | Do not read the burned_segments consultation-ledger gap as fixed or as licence to skip sealed-consultation disclosure on already-read windows. | R23 det |  |
| ADR10-146 | §10 L116 | At 2026-11-08 run the §10 hooks: sourced-vs-empty, battery-closure tally, Req-1a untouched, no Req-2 transplant citations, N-SURV and dd_protection untouched, canonical count line. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-15-notice-log-is-the-live-observation-routing-convention.md</code> — 8 rules: 4 absorbed, 3 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-147 | §2.1 L43 | Capture narrative observations as docs/notes/notice/N-YYYY-MM-DD-slug.md per the notice_log.md template, routed GRADUATE / DROP / HOLD [until date]. | R33 abs |  |
| ADR10-148 | §2.2 L44 | Mechanical script gates may keep the Closed/Forward/Error exit vocabulary where already wired (verify_lock_anchors.py); Action stays dead. | R33 det |  |
| ADR10-149 | §2 L46 | Closed/Action/Forward is only an optional supplementary tag inside a notice, not the governing observation-routing convention. | R33 abs |  |
| ADR10-150 | §2 Scope L49; §5 L77 | Do not retroactively re-label or re-file existing notices' decision fields; the historical record stays as authored. | R30 abs |  |
| ADR10-151 | §5 L78, L79 | Do not delete the three-bucket concept from observation_routing.md or silently edit inqhiori-canon §10/§16 references without this ADR's cross-reference. | R29 det |  |
| ADR10-152 | §5 L80, L81 | This ruling authorizes no notice_log.md template rewrite and no edit to verify_lock_anchors.py or lock-check.md. | R3 abs |  |
| ADR10-153 | §6 L103 | A corrective annotation on a non-load-bearing citation inside an Accepted ADR's body is allowed without supersession; load-bearing decision text needs a superseding ADR. | R32 DEL | Superseded by ceremony-tiering ADR 2026-09-08 revision: citation repairs need no ADR; decision changes use dated revision with immutable prior. |
| ADR10-154 | §4 L67 | If Closed/Action/Forward dominates three consecutive new notices, author a superseding ADR with file-by-file dated evidence; check at the quarterly methodology audit. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-16-con5-timeframe-scope-cheap-falsifier-gate.md</code> — 11 rules: 1 absorbed, 10 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR10-155 | §2 D1 L41 | CON-5's pause is textually scoped to the dense-1m G=10 universe; it does not by name forbid route-1 temporal selectivity outside that lane. | R26 det |  |
| ADR10-156 | §2 D2 L43 | A card relying on D1 to invoke temporal-selectivity route 1 against the index bar must first pass a generous $0 pre-G0 cheap falsifier; PASS necessary, FAIL closes it. | R24 det |  |
| ADR10-157 | §2 Falsifier spec L45 | Run the D2 falsifier on the IS panel only with the construct's frozen stop/target; pass at half the 4x-RT bar; report coverage, n, gross, hurdle, WR; spend no K. | R24 det |  |
| ADR10-158 | §2 D2a L52 | Cards that never invoke the paused route need no D2 falsifier; attestations may cite lane scope plus route analysis; per-campaign attestation at GO stays good practice. | R26 det |  |
| ADR10-159 | §2 D3 L54 | Apply D1/D2 prospectively only: prior verdicts such as MSL-S2B STAGE-1 FAIL stand; only a fresh successor card that runs D2 may rely on the route. | R28 det |  |
| ADR10-160 | §2 D4 L56 | Treating any dense-1m-scoped bar as non-binding through lane scoping requires the matching cheap falsifier for that bar's own underlying finding. | R26 det |  |
| ADR10-161 | §5.6 L88; D4 L56 | Correct frozen card records (e.g. STAGE1.md) with a forward pointer, never a retro-edit. | R30 abs |  |
| ADR10-162 | §5.1 L82; §5.3 L84 | A D2 PASS is a pre-G0 door-check only, discharging no G0 freeze or delete/flip; this ADR itself is no card's falsifier run. | R24 det |  |
| ADR10-163 | §5.2 L83; §5.5 L86 | D1 does not reopen CON-1..4 findings, candidates inside the dense-1m lane, or the lane itself (no Board un-pause). | R26 det |  |
| ADR10-164 | §5.4 L85 | Never re-tune the D2 pass bar per candidate; it is a channel property. | R24 det |  |
| ADR10-165 | §4 L72 | Re-test at the next card invoking D1/D2 or the 2026-11-08 audit; reject H if a D2 PASS later dies to CON-5's RT-tax shape. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-16-deep-iteration-lane-charter.md</code> — 40 rules: 6 absorbed, 26 detail, 8 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-1 | Status L3 | Freeze the first lane campaign prereg only after the P2 policy-frontier measurement and Databento cost dry-run are on record; name the intraday-clock caveat as a mandatory risk. | R23 DEL | GO-1 discharged 2026-08-16 per charter Status/addendum (Q-POLFRONT-1 landed, $0 dry-run); first campaign DL-1 prereg froze that day. |
| ADR11-2 | Status L3 | Declare K about 10 for the first lane campaign; reserve the K=33 corner for a family that has earned it. | R23 DEL | GO-2 scoped to first campaign; DL-1 froze and ran at K=10, abandoned 2026-08-16 (charter change history L267); §2.2(i) K<=33 cap remains. |
| ADR11-3 | §0 L19 | Record Rule-0 production-source reads with anchors in a §0 table before authoring an ADR. | R0 abs |  |
| ADR11-4 | §0 L33 | Run an amendment-first dedup search before authoring a decision artifact and paste the executed command's real output. | R8 abs |  |
| ADR11-5 | §1 L52 | Hold a new candidate-producing channel until the blind channel's 2026-11-08 reading unless the operator makes an explicit overriding election on independent grounds. | R3 DEL | HOLD default overridden by operator GO 2026-08-16 (charter Status line: explicit overriding election); condition can no longer bind. |
| ADR11-6 | §2.1 L60 | Name exactly one mechanism family per deep-lane campaign (entry concept, instrument, timeframe, session) inside the slate-2 design-box geometry, non-index CME micros first. | R23 det |  |
| ADR11-7 | §2.1 L60 | Paste an instrument_profiles.py cell consult in every lane prereg; it must print no BINDING BAR. | R8 det |  |
| ADR11-8 | §2.1 L60 | A family listed in rejected_candidates.md must clear its own re-proposal bar in writing before the lane prereg freezes; the lane never covers a θ-retune. | R26 abs |  |
| ADR11-9 | §2.1 L60 | Attest in each lane prereg that the family is under no standing operator pause or election recorded outside the registry (e.g. dense-1m, CON-5 entry-geometry pauses). | R23 det |  |
| ADR11-10 | §2.1 L60 | Admit an externally-published family to the lane only after harvest intake (its intake kills count there); the lane hosts only internally-generated or intake-cleared families. | R25 det |  |
| ADR11-11 | §2.2 L61 | Declare the full variant budget K in the prereg; every choosable variant and every informal pre-prereg variant counts; an under-declared prereg is void. | R23 det |  |
| ADR11-12 | §2.2(i) L62 | Refuse a lane prereg at freeze unless declared K is at most 33. | R23 det |  |
| ADR11-13 | §2.2(ii) L63 | Refuse a lane prereg at freeze unless floor_at_k(K, confirm_years) is at most 2.0. | R23 det |  |
| ADR11-14 | §2.2(iii) L64 | Refuse a lane prereg unless power is at least 0.50 against an a-priori design-target edge named in the prereg, with method stated; boundary cases must say so. | R23 det |  |
| ADR11-15 | §2.2(iv) L66 | Query burned_segments consultation history channel-agnostically for the CONFIRM window and disclose prior reads (M), sources and floors; disclosure only, never a refusal conjunct. | R23 det |  |
| ADR11-16 | §2.2 L82 | Never cite the deep lane or its K rulings against CAP, DSR_MIN, EM0, the K<=3 one-shot ceiling or any one-shot channel predicate; those stay untouched. | R23 det |  |
| ADR11-17 | §2.3 L83 | Freeze the train/confirm partition before scoring any variant; confirm length must be at least the years the floor was computed at, or recompute the floor honestly. | R23 det |  |
| ADR11-18 | §2.3 L83 | Feed iteration from train only; read confirm once on the single survivor nominated by a frozen rule; never compute per-variant confirm results or re-nominate after a read. | R23 det |  |
| ADR11-19 | §2.3 L83 | Use parent-era Databento history for a long train side only after a mandatory cost dry-run, then operator GO, pull and panel manifest. | R18 DEL⚖ | References retired Databento: retired and unsubscribed 2026-09-10, no replacement approved (AGENTS.md data source; Databento ADR addendum). |
| ADR11-20 | §2.4 L84 | Freeze an own-series confirm half-split and per-half floor before the read; pooled pass with a failed half is FALSIFIED-FRAGILE; do not call it the regime-robustness gate. | R24 det |  |
| ADR11-21 | §2.5 L85 | Run cost-law (at least 4x) arithmetic at the venue-legal expression at family selection, before the search opens. | R24 det |  |
| ADR11-22 | §2.5 L85 | Treat the lane as a candidate supplier only: survivors still need N-SURV, a native-TV anchor and lifecycle intake at SURVIVAL-ONLY/WATCH-1. | R25 det |  |
| ADR11-23 | §2.5 L85 | Anything live from a lane survivor still requires M1 plus per-session operator GO. | R10 abs |  |
| ADR11-24 | §2.6 L86 | At K>3 name SPA/StepM thresholds (plus PBO/CPCV and a leakage argument if CV selection) in the prereg under operator GO; universe_gate re-arms only with SPA, DSR and PBO. | R24 det |  |
| ADR11-25 | §2.7 L87 | Record lane kills with dates on this charter only; a candidate lives in exactly one channel; never double-home or reclassify a kill to dodge a counter. | R28 det |  |
| ADR11-26 | §2 Effective L89 | Do not self-ratify or run anything under the charter while Proposed; operator GO is the only activation. | R3 DEL | Charter Accepted by operator GO 2026-08-16 (Status line); Proposed-state bar spent; general GO rule owned by ADR admission rule. |
| ADR11-27 | §4 L109 | If no lane prereg freezes within 6 weeks of acceptance (or by 2026-11-08), report at the quarterly audit and demote unless the operator re-elects. | R28 DEL | Inertness limb unreachable: DL-1 prereg froze 2026-08-16, acceptance day (change history L267); DL-2 froze 2026-08-22. |
| ADR11-28 | §4 L111 | Two consecutive completed lane campaigns whose survivor fails confirm or N-SURV falsify the lane: supersede plus source-class post-mortem, never a wider K or lower floor. | R28 det |  |
| ADR11-29 | §4(a) L114 | Keep the lane running-count line on this charter canonical; STATE only mirrors it. | R29 det |  |
| ADR11-30 | §4(b) L115 | End every frozen lane prereg in either a confirm read or a dated abandonment record on this charter; there is no third exit. | R28 det |  |
| ADR11-31 | §4(c) L116 | Abandonments disclose without striking; two consecutive abandonments trigger a quarterly-audit report; freeze refusals count only on the refusals line. | R28 det |  |
| ADR11-32 | §4(d) L117 | Reset either consecutive count only when a nominated survivor clears both confirm and N-SURV. | R28 det |  |
| ADR11-33 | §5 L128 | Paste an executed dedup attestation in every lane prereg. | R8 abs |  |
| ADR11-34 | §5 L131 | Never waive the floor predicate per campaign, shorten the confirm after seeing train results, or recompute the floor at friendlier years post hoc. | R23 det |  |
| ADR11-35 | §7 step 1 L150 | File each lane prereg as docs/briefs/pre-registration/*deep-lane*.md with all §2.2 conjuncts, half-split, nomination rule, SPA thresholds, cost-law and attestations; cite its path on the running-count line. | R23 det |  |
| ADR11-36 | §7 step 1 L150 | Obtain a separate operator GO for each lane prereg freeze and for the confirm read, beyond the charter GO. | R3 det |  |
| ADR11-37 | §7 steps 2-4 L151 | Build --lane deep on register_search, add lane-scoping notes to strategy_harvest Clause-K and M-19, and add the lane row to the anomaly-discovery skill. | R23 DEL⚖ | Steps 2-4 landed: register_search --lane deep, strategy_harvest.md L105 row, skill L123/148; only M-19 intercept missing, owed-or-drop is operator's. |
| ADR11-38 | Addendum 2026-08-16 L238 | Bar-schema Databento pulls need only the campaign's operator GO; tbbo or finer needs bar survival, explicit --max-cost and operator sign-off; an estimate never authorizes a pull. | R18 DEL⚖ | References retired Databento pulls: retired and unsubscribed 2026-09-10, no replacement approved (AGENTS.md data source). |
| ADR11-39 | Addendum 2026-08-16 L254 | Reuse the ratified 2018-12-31 IS boundary for TRAIN/CONFIRM splits; never re-derive or re-strike it. | R23 det | → docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md §1 item 1 |
| ADR11-40 | §10 L162 | An ADR must not read Accepted without an operator GO line in its change history. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md</code> — 9 rules: 3 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-41 | §2 L96 | Scope the cme broker panel to the striker and striker_nas100 legs; never register Guardian or Aegis into it because their data exists. | R18 det |  |
| ADR11-42 | §2 L102 | Treat the cme panel as research-tooling data only: it grants no live composition, deployment, locked-parameter, dd_protection or allocation change. | R3 abs |  |
| ADR11-43 | §2 Effective L107 | Record the cme self-test anchor as a new named constant; never compare it with or overwrite the retired 4-leg Pepperstone anchors. | R20 det |  |
| ADR11-44 | §4 L128 | At first candidate injection, check risk-N_eff direction against the Q-COMPOSE-1 finding; if falsified, supersede the registration naming the inconsistency. | R28 det |  |
| ADR11-45 | §4 L142 | Change an accepted ADR's decision or falsifier only through a superseding ADR or dated addendum, never by silent edit. | R32 abs |  |
| ADR11-46 | §5 L156 | Never update the cme registration for a newer MYM/MNQ export, or apply implementation corrections, without a dated Change History or ratification-note entry. | R19 det |  |
| ADR11-47 | §5 L159 | Require a separate admitting ADR plus explicit registration in core/mc/modes.py for every future broker panel key; this admission is no precedent. | R18 det |  |
| ADR11-48 | §7 L191 | Register the cme dicts, record the fresh breadth anchor, update the design spec change history and add a STATE pointer. | R18 DEL | Executed 2026-08-19: cme key registered in core/mc/modes.py L105-108, anchor and STATE pointer per ratification note. |
| ADR11-49 | Verification L271 | Run check_brief.py --type adr and check_adr_graph.py on an ADR before ratification. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-20-analogue-modality-override-ict-ote-1-admit.md</code> — 6 rules: 2 absorbed, 1 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-50 | §2 L94 | Admit Q-ICT-OTE-1 to the TNEC/ICT lifecycle despite the analogue-modality pause, licensing only its $0 parent-side cheap falsifier. | R3 DEL | Exception spent: OTE cheap falsifier FALSIFIED, Q-ICT-OTE-1 STOP-closed 2026-08-20 (change history L254). |
| ADR11-51 | §2 L102 | A cheap-falsifier PASS never licenses a PREREG_G0 freeze or real-panel EXPLORATION score; each needs a separate operator explore GO. | R3 DEL | PASS branch unreachable: OTE falsifier FALSIFIED, PREREG_G0 never frozen, STOP-closed 2026-08-20 (L254); two-step discipline owned by TNEC lifecycle. |
| ADR11-52 | §5 L152 | Run the OTE cheap falsifier's stop-geometry test first, reporting mean stop_dist with gross points, and file the LOG in cheap_falsifiers_2026-08. | R24 DEL | Executed 2026-08-20: stop-geometry falsifier ran, LOG filed in cheap_falsifiers_2026-08, construct STOP-closed (change history L254). |
| ADR11-53 | §4 L131 | Never renew the spent OTE exception for a retuned Fib band or FVG choice; record its null as thread data, not evidence for a future override. | R26 abs |  |
| ADR11-54 | §5 L160 | Never use the OTE override as precedent to admit Order Blocks, Breaker Blocks or SMT Divergence; each needs its own ADR. | R3 abs |  |
| ADR11-55 | §5 L148 | Do not read the OTE override as marking U1/U2, reopening CON-1 to CON-5, licensing CON-6, or licensing Cap, Pine, deploy or arming. | R3 det |  |

</details>

<details><summary><code>docs/adr/2026-08-21-cfo-subscription-ledger-consolidation.md</code> — 5 rules: 0 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-56 | D1 L15 | Keep d11-d17 cost figures only in SUBSCRIPTION_LEDGER; pursuit records link rather than repeat; missing figures stay unknown, not zero. | R29 det |  |
| ADR11-57 | D2 L19 | KEEP pursuit records of subscription or venue-account meta-belt class must point to the ledger; the check WARNs only, with no severity escalation or class widening. | R29 DEL⚖ | gates.yml L59-63 retired the pursuit-records check 2026-08-24 as always-exit-0; pointer duty is D1; manual script retained, operator's call. |
| ADR11-58 | D3 L26 | Operator reconfirms ledger figures monthly on the 21st, even when unchanged, rolling the STATE reminder; silence is not currency; no role, hook or service replaces it. | R34 det |  |
| ADR11-59 | D4 L32 | Update the ledger row in the same session a cost is disclosed; further automation needs evidence and its own decision. | R29 det |  |
| ADR11-60 | Trigger L38 | At each reconfirm, check pointer false positives and missed stale figures; misses require a redesign decision; three quiet reconfirms justify proposing, never silently adopting, a quarterly cadence. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-22-catalog-hot-vs-disposition.md</code> — 15 rules: 1 absorbed, 13 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-61 | §2.1 L56 | Treat CATALOG table membership as hot (body under lab/analysis/<theme>/<slug>/) and disposition as the card's Verdict; hot=yes with a terminal disposition is legal. | R34 det |  |
| ADR11-62 | §2.2 L61 | Keep the CATALOG status column holding the disposition plus a hot column; no rename, mixed or third schema, compound token or LIVE token. | R34 det |  |
| ADR11-63 | §2.3 L63 | Resolve disposition from a separate Verdict line over Status; HOLD in the verdict clause dominates later terminal tokens; NULL dominates a co-occurring ACTIVE. | R34 det |  |
| ADR11-64 | §2.4 L65 | C2 joins table membership to the hot column, not disposition class; a terminal disposition in the hot table is legal only when hot=yes. | R34 det |  |
| ADR11-65 | §2.5 L67 | Archive via --slug only with an archiveable disposition and no stay-hot pin; never loosen this because parser honesty improved. | R31 det |  |
| ADR11-66 | §2.6 L69 | Let only archive_lab_analysis.py --regenerate-catalog write CATALOG rows; never hand-edit status or hot cells. | R34 det |  |
| ADR11-67 | §4 L91 | If C2 flags a named stay-hot pin or misses a real hot/table mismatch, supersede via ADR; re-check at the next quarterly programme audit. | R28 det |  |
| ADR11-68 | §5 L101 | Do not implement the parser/C2 change or regenerate CATALOG within the ADR-only commission. | R3 DEL | Discharged: operator GO 2026-08-22 authorized Phase 1 parser/C2/regen in the same PR (catalog ADR Status L5, §5 L101). |
| ADR11-69 | §5 L102 | Never mass --slug archive bodies or mass-relocate lab trees without a separate GO. | R31 det |  |
| ADR11-70 | Addendum 2026-08-29 L223 | When regeneration would clobber concurrent worktree state, hand-insert one new slug-sorted CATALOG row verified by git diff --stat as one added line; never edit existing cells. | R34 det |  |
| ADR11-71 | Addendum 2026-09-03 lock 1 L257 | Title the hot table ## Hot bodies (internal id active; parsers accept both); hot means keep the body, not in flight. | R34 det |  |
| ADR11-72 | Addendum 2026-09-03 lock 2 L259 | Derive ## In flight from STATE Owner-artifact cells, briefs INDEX Open Home cells and In-flight: yes head cards, excluding HOLD and archiveable statuses; STATE stays the work list. | R34 det |  |
| ADR11-73 | Addendum 2026-09-03 lock 3 L266 | Never leave ACTIVE on a decided campaign; stamp a separate Verdict line instead of archiving with --slug. | R34 det |  |
| ADR11-74 | Addendum 2026-09-03 lock 5 L269 | Keep _inbox a cataloged theme listed first; outcome-bearing work must carry a Verdict and leave _inbox before --slug. | R34 det |  |
| ADR11-75 | Addendum 2026-09-03 L272 | Add no sixth root or index document. | R34 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-22-grow-lane-build-authorization.md</code> — 7 rules: 1 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-76 | §2.1 L68 | Exempt only GROW-0 engine validation from charter §4 counters; every GROW-1+ campaign counts as an ordinary deep-lane campaign with Q-ID, frozen prereg, GOs and confirm-once. | R28 det |  |
| ADR11-77 | §2.2 L74 | Build deep_lane_admission.py, grammar.py, --lane deep wiring and the burned_segments seed and checker. | R23 DEL | Landed in commit a5ee05e (2026-08-22); deep_lane_admission.py, grammar.py, burned_segments.py present in lab/discovery. |
| ADR11-78 | §2.2 L87 | Ship each named forward-work slice as its own dated commit against this ADR; never claim a slice shipped without its commit reference. | R21 det |  |
| ADR11-79 | §4 limb 1 L119 | --lane deep must refuse anything the charter §2.2 conjuncts refuse; if a campaign opens otherwise, supersede and repair the predicate before reuse. | R23 det |  |
| ADR11-80 | §5 L135 | Keep the S6 mechanism-first predicate (admission_schema.py) and the deep-lane predicate separate; never loosen S6 to share code. | R23 det |  |
| ADR11-81 | §5 L137 | Never treat burned_segments as a silent auto-pass: overlap refuses and an unlisted window is disclosed as consultation_count 0, never as cleared. | R23 det |  |
| ADR11-82 | §5 L140 | Under the GROW tooling ADRs, make no Databento pull, Pine touch, arming, LEG_MAP, core/, lock, allocation, dd_protection or lifecycle change. | R3 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-22-grow0-two-ledger-k-question.md</code> — 11 rules: 4 absorbed, 6 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-83 | §2 Part A L132 | K_intrinsic means the full search width examined; redefining it needs a superseding ADR backed by a real, pre-registered, adversarially-reviewed investigation addressing all five owners. | R23 det |  |
| ADR11-84 | §5 L247 | Never under-declare K_intrinsic or cite the M=1 re-derivation as grounds for charging less than full K. | R23 det |  |
| ADR11-85 | §7 L342 | Add §2.2(iv) to the charter, extend burned_segments with consultations and count/history functions plus tests, and sweep stale claim-1 restatements. | R23 DEL | Executed 2026-08-22 (G0 change history): charter §2.2(iv) added; consultation_count/history at burned_segments.py L87/L101. |
| ADR11-86 | §4 part 2 L223 | If an admitted survivor whose CONFIRM window had M>=2 prior reads fails replication, mark the disclosure-only rule FALSIFIED and supersede with a measured M-based adjustment. | R28 det |  |
| ADR11-87 | §4 L233 | When review finds a lane prereg omitted the §2.2(iv) disclosure, repair the review checklist and record it at the next quarterly programme audit. | R28 det |  |
| ADR11-88 | §5 L262 | Do not invent a numeric M_max or graded floor-adjustment formula without new evidence. | R23 det |  |
| ADR11-89 | §5 L272 | Never paste a search or command output without having run that exact command. | R21 abs |  |
| ADR11-90 | §5 L276 | Re-read a cited source before attributing a mechanism, rationale, scope or count to it; re-check every attribution on amendment even after clean reviews. | R0 abs |  |
| ADR11-91 | §6 L326 | Route doctrine-amending decisions of this class through adversarial review before operator ratification. | R0 det |  |
| ADR11-92 | §6 L338 | Give STATE.md and SESSIONS.md a pointer line only, never a retelling of the decision. | R34 abs |  |
| ADR11-93 | §7 Phase 0 L344 | Re-verify §0 anchors at implementation or ratification time; abort and re-derive if any moved materially. | R0 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-23-strategy-coldstore-phase-b.md</code> — 6 rules: 0 absorbed, 5 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-94 | §2 L49 | Record every Phase A catalog disposition with authorization action none; Striker stays AUTHORIZED MECHANISM at 1.00x. | R15 det |  |
| ADR11-95 | §2 L49 | Never create or edit lifecycle_state.json to record a catalog disposition; the absent file is the AUTHORIZED record. | R15 det |  |
| ADR11-96 | §5 L98 | Never demote or retire a strategy solely from a VENUE_WITHDRAWN or VENUE_LESS_CFD label; edition WITHDRAWN is not book RETIRED. | R15 det |  |
| ADR11-97 | §4 T1 L85 | Revert any BASE_RISK, DD_SCALE, DD_TRIGGER, LEG_MAP or Pine-parameter change justified only by a catalog-disposition ADR; it needs its own lock-decision ADR. | R14 det |  |
| ADR11-98 | §5 L100 | Do not invent Approach 3 (hard delete plus offline vault) because a design body is unrestored. | R31 det |  |
| ADR11-99 | §5 L101 | Do not start Phase C from the Phase B accept; Phase C needs its own admitting ADR. | R32 DEL | Superseded: Phase C admitted by its own ADR 2026-08-23 (docs/adr/2026-08-23-strategy-coldstore-phase-c.md exists). |

</details>

<details><summary><code>docs/adr/2026-08-23-strategy-coldstore-phase-c.md</code> — 6 rules: 1 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-100 | §2 L61 | Keep living _BASE_RISK and dd_protection.BASE_RISK to the Striker pair; re-adding guardian or aegis is a verifier error. | R14 det |  |
| ADR11-101 | §2 L61 | Own the frozen 4-leg risk book only in HISTORICAL_CHALLENGE_BASE_RISK with bytes unchanged; derive living and MC consumers from it; never re-literalize it elsewhere. | R14 det |  |
| ADR11-102 | §2 L61 | Run Call-4 over the four-leg STRATEGY_KEYS, not living BASE_RISK keys; never recalibrate the Call-4 thresholds as a key-set side effect. | R15 det |  |
| ADR11-103 | §5 L114 | Keep living Striker keys and LEG_MAP Striker rows; rail teardown belongs to F2. | R11 det |  |
| ADR11-104 | §4 T4 L103 | Leave DD_TRIGGER and DD_SCALE untouched by key-set retirements. | R14 abs |  |
| ADR11-105 | §2 L61 | Convert CFD rows of the Strategy Reference to pointer-only historical entries. | R14 DEL | Executed 2026-08-23; CLAUDE.md retired 2026-09-20 and AGENTS.md §Strategy Reference now holds no CFD rows, only pointers. |

</details>

<details><summary><code>docs/adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md</code> — 5 rules: 1 absorbed, 4 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-106 | Decision L12 | Elect frozen ID 2 (observe-only alert tripwire); do not wire 1-size or 1-realized; invent no fourth frozen ID. | R11 det |  |
| ADR11-107 | Decision L12 | Elect the tripwire threshold later; never import the CFD-era example percent. | R20 abs |  |
| ADR11-108 | Decision L12 | If a tripwire is implemented, freeze an MTM-or-dual trigger and threshold before first fill, or record fail-open acceptance on the implementation record. | R11 det |  |
| ADR11-109 | Boundary L20 | Do not treat the election as a wire: no DD_TRIGGER, DD_SCALE or BASE_RISK change, no sl= or flatten, and 1-size never discharges realized loss. | R14 det |  |
| ADR11-110 | Gate L18 | If G1, G2 or G3 is already false on the frozen owners, mark FALSIFIED and escalate; never elect the CFD pair in place. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-08-24-regime-gate-scope-worked-nonexample-f1-discharge.md</code> — 6 rules: 3 absorbed, 2 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR11-111 | §2 D1 L128 | Apply the regime-robustness gate to risk-constant LOCK CANDIDATE recommendations, not strategy-book additions; do not claim it more mandatory or optional than its own scope. | R24 abs |  |
| ADR11-112 | §2 D2 L140 | A candidate prereg may cite the regime gate as context only; never import it as a rider with pre-fixed consequence; label non-verdict-changing caveats as caveats, not discharges_falsifier. | R24 det | → docs/methodology/regime_robustness_gate.md (L37, worked non-example) |
| ADR11-113 | §2 D2 L136 | Ratify the 2026-08-02 scope narrowing and add a worked non-example to the regime gate doc, discharging gate-stack audit F1. | R24 DEL | Executed 2026-08-24: worked non-example present at regime_robustness_gate.md L132, F1 discharged. |
| ADR11-114 | §4 L174 | If a prereg again imports the regime gate as a pre-fixed rider, supersede D2 in part and escalate to a mechanical hard-fail check. | R28 det |  |
| ADR11-115 | §5 L191 | Never edit a FROZEN signed pre-registration in place; record corrections as an addendum or worked example where readers meet the pattern. | R23 abs |  |
| ADR11-116 | §0 L44 | A methodology-doc scope change may not stand on a chore commit without a decision artifact. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-24-sourcing-phase-channel-retirement.md</code> — 17 rules: 7 absorbed, 8 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-1 | §2(a) L50 | Treat the structural flow census as a retired sourcing channel; open no future entry under its rank, required-fields list or Notice-phase recording convention. | R25 det |  |
| ADR12-2 | §2(b) L52 | Open no campaign or G0 freeze under Avenue A Route B (generate→confirm); Avenue A §6 condition 3 stays survivor-tied only. | R25 det |  |
| ADR12-3 | §2 Scope L55 / §5 L87,L89 | Do not read the channel retirements as touching Route A, the G0-freeze principle, harvest branches B1–B6, the deep-iteration lane or the classic mining stack. | R25 det |  |
| ADR12-4 | §5 L86 | Reopen a retired sourcing channel only through a fresh ADR naming what changed in the design; never informally (Notice entry, unscoped campaign) or by citing the old grant. | R25 det |  |
| ADR12-5 | §4 limb 1 L75 | If any admitted census or Route B seed surfaces that the §0 record missed, author a superseding ADR correcting the record before treating that channel as retired. | R28 det |  |
| ADR12-6 | §4 limb 2 L76 | At the next two quarterly programme audits, if surviving channels are zero-yield and no redesign ADR exists, the audit must rule whether channel starvation binds sourcing. | R28 det |  |
| ADR12-7 | §4 limb 3 L77 | On 2027-02-08, independently re-examine whether closing the channels ahead of clause 2-B's schedule was sound; if not, flag early closure as precedent not to repeat. | R28 det |  |
| ADR12-8 | §5 L88 | Never silently edit frozen ADR decision text or clauses; append a dated addendum and keep the frozen body byte-unedited. | R32 abs |  |
| ADR12-9 | §4 Revert action L79 | Revert a falsified ADR by authoring a fresh superseding ADR (full or in-part per edge rules), never by silently editing its decision text. | R32 abs |  |
| ADR12-10 | §0 L27 / §6 L110 / §7 Phase 1(ii) | On in-part supersession, append a new Superseded-in-part-by line to the target header, never overwriting existing ones; the target stays Accepted and hot. | R32 abs |  |
| ADR12-11 | §7 L130 | While a superseding ADR is Proposed, leave the superseded ADRs untouched; reverse edges and cold-store shape become mandatory only on Accept. | R32 abs |  |
| ADR12-12 | §6 L109 / §7 Phase 1(xi) | Fully retire a superseded ADR via scripts/retire_adr.py: Status Superseded, Superseded-by set, body moved to docs/ltm/adr/, hot stub ≤40 lines, residual inbound-refs sweep. | R31 DEL | Discharged 2026-08-24 (2026-08-05 ADR stub Superseded, body in docs/ltm/adr); brief-authoring adr.md now makes retire_adr.py optional legacy form. |
| ADR12-13 | §6 L118 | Regenerate docs/adr/INDEX.md with check_adr_graph.py --regenerate-index in the same commit as any ADR change; never hand-edit it. | R32 abs |  |
| ADR12-14 | §0 L28 / §10 | Grep-sweep for stale references before acceptance, paste raw output, disposition every hit individually, and re-run if new hits could have landed since authoring. | R30 det | → .claude/skills/blast-radius/SKILL.md §2–4 |
| ADR12-15 | §6 L119 | When sweeping, do not edit frozen campaign history, closed PREREG/RESULTS, dated audit notes, session narrative or cold archives; disposition them as history. | R30 abs |  |
| ADR12-16 | §7 Phase 3 L128 | Never self-ratify an ADR: Proposed→Accepted is a reserved operator GO; agents draft, review and verify only. | R4 abs |  |
| ADR12-17 | §6 L107 / §7 Phase 1 | Execute the Phase-1 edits: in-part addenda, withdraw the Route B block, banners, strike the 1-tie row, three STATE rows, retire the 2026-08-05 ADR. | R32 DEL | Discharged 2026-08-24: Change history Phase-4 row lists all eleven edits; 2026-08-05 ADR shows Superseded with ltm body. |

</details>

<details><summary><code>docs/adr/2026-08-24-tradeify-growth-tier-scoring-only.md</code> — 6 rules: 1 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-18 | Decision L28 | Add Tradeify_Growth_100K to FIRM_RULES and AUTOMATION_FRIENDLY_PROP_FIRMS['tradeify'] alongside the Select tiers. | R16 DEL | Executed: core/firm_rules.py L543 defines Tradeify_Growth_100K and L626 lists it in AUTOMATION_FRIENDLY_PROP_FIRMS. |
| ADR12-19 | Decision L33 | Define Growth 25K/50K/150K as their own FIRM_RULES rows before using them; only the $100K Growth row exists. | R16 det |  |
| ADR12-20 | Decision L35 | Keep Growth daily_loss_pct None, since the soft DLL is not a hard fail; a faithful soft-DLL limb needs its own engine change, ADR and re-MC. | R16 det |  |
| ADR12-21 | Decision L38 | Quote every Growth bust figure as two-sided: upper bound for the missing DLL lockout, lower bound for the intraday clock, never a point estimate. | R20 det |  |
| ADR12-22 | Owed L47 | Re-read Tradeify art. 10495897 for Growth specifically; its drawdown-clock reading still rests on the 2026-07-30 read. | R17 det |  |
| ADR12-23 | Owed L48 | Treat Growth challenge-pass re-MC and rail build as separately gated; adding firm rules authorizes neither. | R16 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-24-validation-battery-k-tiering-and-gate-retirement.md</code> — 13 rules: 5 absorbed, 6 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-24 | §2 D1 L152 | At declared K∈{0,1}, log the §8a/§8c universe-level correction as a declared no-op ('K≤1, correction not applicable'); at K∈{2,3}, run it. | R24 det |  |
| ADR12-25 | §5 L243 / §4 (a) | Do not treat K-tiering as license to skip §8a/§8c at K≥4; when any lane makes K≥4 reachable, extend the table with a K≥4 band. | R24 det |  |
| ADR12-26 | §2 D2 L168 | Treat strategy_harvest Requirement 5 as sole owner of the per-event bp cost law, M-20 as its labeled mirror, and the skill's 4× hurdle convention. | R29 DEL | Superseded by Joshua's 2026-10-24 ruling: Requirement 5 and 4× convention deleted; marker above D2 (L166) and header record it. |
| ADR12-27 | §2 D2 L173 | scripts/cost_geometry_pregate.py owns the per-trade stop-distance-R cost formula; skills point to it instead of restating it; the check is report-only. | R29 det |  |
| ADR12-28 | §1 item 2 / §3 rows 1-2 | Keep one canonical owner per fact; mirrors are labeled pointers, and distinct facts (e.g. two different cost formulas) are never merged under one owner. | R29 abs |  |
| ADR12-29 | §2 D3 L179 | Delete the pursuit-records gate from scripts/gates.yml after the Rule 16 four-part scan; keep check_pursuit_records.py on disk, unwired. | R38 DEL | Executed: scripts/gates.yml L59 comment records pursuit-records retired 2026-08-24; check_pursuit_records.py remains unwired. |
| ADR12-30 | §4 revert (b) L227 | If docs/pursuits change detection is needed again, author a new gate with a real failing condition; never restore the always-exit-0 check verbatim. | R38 abs |  |
| ADR12-31 | §0 L77 / D3 | Delete an obligation or gate whose check cannot fire; unfalsifiable ceremony is deletable even when signed. | R31 abs |  |
| ADR12-32 | §2 D5 L192 | Govern gate or tooling retirement by Rule 16's retention test and mandatory four-part scan, not the three-loop D2 STRATEGIC-Delete channel for programme/track/instrument kills. | R31 det |  |
| ADR12-33 | §2 D4 L185 | register_search open --lane mechanism-first must hard-abort before any manifest write when profile_cell, profile_consult, admission or prereg is missing. | R23 det |  |
| ADR12-34 | §5 L237 | Never backfill or rewrite existing discovery_manifests/*.json; pre-registration manifests are immutable once opened. | R23 abs |  |
| ADR12-35 | §5 L240 | Do not delete register_search's --lane blind without a separately researched decision on why it exists and who still needs it. | R31 det |  |
| ADR12-36 | §0 L97 | Before minting a new ADR, run the amendment-first dedup search (check_advisor_dedup.py) and amend the existing owner when one exists. | R29 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-24-venue-binding-axis-t1-disposition.md</code> — 7 rules: 2 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-37 | §2 L59 / §4 T1' L85 | Every venue-scope decision recorded from 2026-08-22 must produce an edition-state transition; one prose-only fallback falsifies and requires a superseding ADR. | R15 det |  |
| ADR12-38 | §4 T2' L86 / §5 L97 | Never invoke the pre-acceptance bootstrap carve-out for a decision after 2026-08-22; it excused only the single 2026-08-08 occurrence. | R28 det |  |
| ADR12-39 | §1 L51 / §5 L99 | Execute a fired falsifier's named revert action; a status-flip addendum or operator GO is no standing substitute, and this disposition is no precedent without equivalent diagnosis. | R28 det |  |
| ADR12-40 | §3 row 1 L70 | Do not spare an ADR from its falsifier's named remedy because of work built during the firing's own unresolved window; sunk cost is circular. | R28 det |  |
| ADR12-41 | §5 L96 | Do not rewrite S1 or other historical records to retroactively claim an edition transition; rule on applicability instead. | R30 abs |  |
| ADR12-42 | §7 Phase 3 L142 | Treat an ADR as live only after check_brief.py --type adr reports well-formed and check_adr_graph.py exits 0. | R32 abs |  |
| ADR12-43 | §7 Phase 1 L140 | On acceptance, append Superseded-in-part-by and one Change History row to the 2026-08-05 venue-binding ADR, body unchanged. | R32 DEL | Executed: 2026-08-05 venue-binding ADR L7 carries Superseded-in-part-by and Change history L336 the row. |

</details>

<details><summary><code>docs/adr/2026-08-26-striker-legmap-cap-release.md</code> — 7 rules: 2 absorbed, 4 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-44 | Decision L23 / Gate L68 | Set LEG_MAP cap_alloc for dj30_mym and nas100_mnq to 0, releasing the 80-micro account cap. | R15 DEL⚖ | Executed: ops/c1_rail/c1_sizing_host_reference.py L108/L114 set cap_alloc 0 with release comments; allocation-adjacent, so operator confirms. |
| ADR12-45 | Boundary L73 | Do not read the cap release as authorizing Striker redeploy; both withdrawn Striker legs stay barred. | R3 abs |  |
| ADR12-46 | Boundary L74 | Choose any future leg's cap_alloc as its own admission decision under the third-leg spec S5/S7 screens; released headroom is not pre-spent. | R15 det |  |
| ADR12-47 | Decision L28 / Boundary L76 | Treat cap-dollar allocation and research-occupancy permission as separate dimensions; occupancy stays owned by the 2026-08-12 MSL B8 ADR. | R15 det |  |
| ADR12-48 | Reads L51 / Boundary L78 | Keep historical 69/11 sizing artifacts (frozen spec worked example, f2_floors.json oracle) unedited; tests pin them through HISTORICAL_LEG_MAP. | R30 abs |  |
| ADR12-49 | Grounds L37 / Reads L46 | Sizing host halts to zero on missing or malformed input, never a permissive default; a zeroed leg floors qty_out to 0, never falls back to cap_firm. | R11 det |  |
| ADR12-50 | Reads L51 | Keep summed LEG_MAP cap_alloc and combined max position within the account-aggregate contract cap; over-commit is forbidden. | R11 det |  |

</details>

<details><summary><code>docs/adr/2026-08-27-ssot-data-lineage-remediation-program.md</code> — 18 rules: 6 absorbed, 10 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-51 | §2 Task 1 L235 | Author the skill-side check_brief.py under .claude/skills/brief-authoring/scripts/ and deploy it via sync_skills.py. | R32 DEL | Executed: .claude/skills/brief-authoring/scripts/check_brief.py exists and scripts/sync_skills.py deploys it. |
| ADR12-52 | §2 Task 1 L237 / §6 L361 | ADR-cited ~/.claude/skills/*/scripts/*.py must exist at a present local deploy target; hard-fail when missing, skip only when no deploy target exists. | R38 det |  |
| ADR12-53 | §2 Task 2 L239 | Each in-window instrument-scoped terminal-negative closure needs a matching ops/instruments/<SYM>.md DEAD row (D4 enforcement); report-only at audit tier. | R26 abs |  |
| ADR12-54 | §2 Task 3 L243 / §10 L433 | The M1 monitoring artifact must pass structural validation on every commit; deployed-vs-main tree skew is checked at audit tier. | R38 abs |  |
| ADR12-55 | §2 Task 4 L246 / §10 L443 | At each quarterly programme audit, run check_falsifier_reachability.py --stats and record the coverage trend, not just the point figure. | R28 abs |  |
| ADR12-56 | §2 Phase 4 L268 | Do not implement SSOT Phase 4 (lineage in coherence-campaign cadence) until the operator promotes it after Phases 0–1 clear a falsifier-review cycle. | R3 det |  |
| ADR12-57 | §4 L309 | At the 2026-11-08 audit, FALSIFY the program if a Phase 1 task is open, a §10 hook fails without dated exception, or a fifth prose-never-wired instance appears. | R28 det |  |
| ADR12-58 | §5 L324,L327 | Do not reopen ratified rulings (CATALOG hot/disposition; rejection-register D1–D3) under cover of SSOT or governance cleanup without new evidence. | R3 det |  |
| ADR12-59 | §5 L330 | Do not bulk-delete rejection-register rows (rejected_candidates, rejected_signals, ops/instruments) to make coverage or counts look cleaner. | R31 abs |  |
| ADR12-60 | §5 L333 | Do not touch Pine, dd_protection.py, firm_rules.py (including commission dollars) or allocations under cover of governance-tooling work. | R14 det |  |
| ADR12-61 | §5 L336 | Land new corpus checkers report-only first; promote to blocking or default-on only after a clean live-corpus run (and a mutation test). | R38 abs |  |
| ADR12-62 | §10 Task 3 L439 / addenda Gates | Never suppress or silence a real checker finding to make a task look done; report it as a named finding or extend the checker. | R21 abs |  |
| ADR12-63 | Addendum Phase 2 L548 | Each canonical running-count line must equal its increment-table 'yes' rows (deep-lane abandoned vs cited deep-lane preregs); unparseable lines fail closed. | R29 det |  |
| ADR12-64 | Addendum Phase 2 Boundary L570 | Do not join STATE.md or ops/instruments/MNQ.md mirrors into running-count checks, or rewrite canonical count lines into an HTML-comment schema. | R29 det |  |
| ADR12-65 | Addendum Phase 3 L623 | Keep cost_model partitioned: INDEX_MICRO ⊆ SPECS, SPECS ⊆ INDEX_MICRO ∪ NO_COMMISSION, INDEX_MICRO ∩ NO_COMMISSION empty; new SPECS rows must be classified. | R29 det |  |
| ADR12-66 | Addendum Phase 3 L626 | Add MCL/6J/6E/M6E to INSTRUMENT_SPECS only when a campaign already scores those notionals; unknown specs stay fail-closed. | R29 det |  |
| ADR12-67 | Addendum Phase 3 Boundary L638 | In cost-model SSOT work, do not join ops/instruments ledgers, parse ledger prose into bars, or rewrite harvest gate-2 FAIL policy. | R29 det |  |
| ADR12-68 | Addendum Phase 2 Boundary L573 / Phase 3 L585 | Do not auto-open SSOT Phase 3 when Phase 2 ships or open a STATE operator-queue row for it; delete STATE row 3 on succession. | R32 DEL | Historical: Phase 3 authorized 2026-08-29 (header), cost-model-closed-world gate at gates.yml L164; STATE has no SSOT row. |

</details>

<details><summary><code>docs/adr/2026-08-29-clv-autocorrelation-admission-route-scope.md</code> — 12 rules: 4 absorbed, 5 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-69 | §2 2-A L54 | Recording an unconditional bar-shape statistic with no entry rule in a Notice-log does not trigger the raised bar; the gate fires at Pre-Q admission of a candidate. | R26 det |  |
| ADR12-70 | §2 2-B L58 | Read raised-bar Route 1 as any mechanism outside the mapped price/instrument-selection/hold-time re-derivation axes, not only the temporal-selectivity worked example; Route 2 needs a different modality. | R26 det |  |
| ADR12-71 | §2 2-B L66 / §4 T3 L112 | A Route 1 opening still needs its own G0: adversarial review, K_intrinsic charged, F2 guard, and 2026-08-10 §2-B conditions; citing this ADR alone voids the opening. | R23 det |  |
| ADR12-72 | §2 2-C L72 | Run and record the $0 cost-law pre-screen before any Pre-Q on either CLV finding; a predicted outcome is not a substitute. | R24 DEL | Discharged 2026-08-30: both CLV notices (N-2026-08-29 MNQ/MYM) ran the $0 pre-screen and closed DROP. |
| ADR12-73 | §2 2-C L79 / §5 L132 | Treat a cost-floor pass as necessary, not sufficient: Route 3 requires beating ORB-MNQ-1's realized net edge in comparable units from a defined entry/exit construct. | R26 abs |  |
| ADR12-74 | §2 2-C L77 | Read MYM CLV results against the #M6 hurdle as 'last-known basis' only and re-run against the successor-venue hurdle once F3 rules. | R20 DEL | Historical: MYM CLV notice closed DROP 2026-08-30, so no re-run is owed; Tradeify de-scope reversed 2026-09-01. |
| ADR12-75 | §4 Disposition D1/D2 L121 | A CLV pre-screen pass never auto-admits to Pre-Q (record numbers in a fresh ADR first); a clean fail on both closes the notices DROP with no Pre-Q. | R28 DEL | Discharged: D2 fired 2026-08-30; both CLV notices DROP with no Pre-Q (notice §4/§5 record it). |
| ADR12-76 | §5 L133 / §2-D | Do not read the CLV scope ruling as a GO for any Pre-Q, campaign, entry-rule authoring, backtest or K spend. | R3 abs |  |
| ADR12-77 | §5 L135 | Keep economic-viability dispositions (pre-screen D1/D2) separate from scope-reading falsifiers T1–T3; neither is evidence for the other. | R28 det |  |
| ADR12-78 | §2 Scope L86 / §6 L144 | A future bar-shape (non-entry) Notice finding cites this ADR's scope reasoning instead of re-deriving it, with its own route pre-analysis if shaped differently. | R29 abs |  |
| ADR12-79 | §4 T1–T3 L108 / L115 | At every G0 or adversarial review touching this scope reasoning, check T1–T3; any firing triggers a superseding ADR. | R28 det |  |
| ADR12-80 | §4 Revert action L114 | In-place correction of a ratified ADR needs the operator's explicit instruction; that exception is never precedent for an agent silently editing decision text. | R32 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-30-candidate-contract.md</code> — 23 rules: 4 absorbed, 19 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-81 | Decision Effective L22 | Apply the candidate contract to every generation-open candidate after 2026-08-30 in all current and future channels; already-frozen candidates keep their records. | R23 det |  |
| ADR12-82 | Contract fields L29 | At generation-open, before any exploration data is examined, freeze exactly one hash-addressed candidate contract per campaign, fixed trade template and catalogue. | R23 det |  |
| ADR12-83 | Contract fields L33 | Admit no candidate missing instrument, catalogue, signal, entry clock, stop, exit, horizon or costed payoff unit; proxy diagnostics cannot open contracts, consume Confirm or claim candidacy. | R23 det |  |
| ADR12-84 | Contract fields L37-45 | Founding fields also include windows, K plus manifest run_id, costs, schema ladder, envelope, shape priors/probe, cost authority, Confirm reservation, compliance snapshot and succession rule. | R23 det |  |
| ADR12-85 | Contract fields L46 | Founding-freeze a complete independent mechanism-discriminator rule (observable, statistic, null, direction, threshold, coverage/power), measured apart from payoff and never chosen after Explore. | R23 det |  |
| ADR12-86 | Contract fields L51 | A structurally new expression must cite the mechanism's complete rejection history and its ordinal on the N_expr ladder. | R26 abs |  |
| ADR12-87 | Cardinality L54 | Explore may select at most M hash-pinned parameter cells of one template; a different signal, stop family or horizon class needs a separately opened contract. | R23 det |  |
| ADR12-88 | Distinct immutable freezes L60 | Reserve Confirm append-only before any probe reads data; founding freeze before Explore; selection freeze before holdout access; later entries append, never rewrite founding facts. | R23 det |  |
| ADR12-89 | Freezes L66 / Current owner L161 | Each channel owes a dated, approved artifact-adoption amendment; until then its existing chain stays live practice, and after adoption steps append at existing freeze points. | R23 det |  |
| ADR12-90 | K authority L70 | discovery_manifests/*.json written by register_search.py is the sole machine K ledger; contract K must agree and bind before exploration, as late checks cannot recover trials. | R23 det |  |
| ADR12-91 | Campaign authority L78 | Approve one campaign envelope (spend, schemas, windows, K) before Explore; work inside needs no repeated permission ask; exceeding any bound needs a fresh explicit operator GO. | R3 det |  |
| ADR12-92 | Campaign authority L80 | Rule 2 effort and iteration limits bind independently of spend envelopes and calendar/core-hour ceilings; sandbox promotion and capital actions keep their own S5 authority. | R2 abs |  |
| ADR12-93 | Campaign authority L85 | Run a pre-freeze probe inside an approved scope without extra approval after declaring ceilings and statistics on the draft; escalate material scope changes; never read reserved Confirm. | R23 det |  |
| ADR12-94 | Campaign authority L91 | Count probe spend and K once as an already-spent sub-line within the campaign ceiling, never topping it up; if no campaign freezes, close the probe on the mechanism record. | R23 det |  |
| ADR12-95 | Campaign authority L97 | EVIDENCE-VOID exhausts the Confirm attempt; further testing needs a fresh campaign with a fresh holdout, never a re-read of the same Confirm data. | R23 det |  |
| ADR12-96 | Campaign authority L101 | Record decisions and field changes prospectively with their owning spec, campaign, plan, PR or ADR; required evidence binds without an ADR per field. | R32 abs |  |
| ADR12-97 | Confirm family L108 | Freeze family alpha, M and exactly one procedure (Bonferroni alpha/M, or Holm step-down identity) for the envelope's life; a missing procedure is integrity-invalid. | R23 det |  |
| ADR12-98 | Confirm family L114 | Forfeited ROLE-BLOCKED, EVIDENCE-VOID and unfilled Confirm slots carry p=1; M never shrinks, even if Explore selects fewer cells. | R23 det |  |
| ADR12-99 | Confirm family L116 | Apply K-ledger catalogue-selection correction and the confirm-family correction sequentially and cumulatively; neither substitutes for the other or any campaign-frozen evidence gate. | R23 det |  |
| ADR12-100 | First review L132 | At the 2026-11-08 review, inspect freeze chains for leakage, probe accounting, confirm families and EVIDENCE-VOID retries; correct failures at the owner before relying on the control. | R28 det |  |
| ADR12-101 | First review L140 | For any fired channel ceiling, test whether it was UNREACHABLE, UNBINDING or needed an ad hoc override; missing examples are inconclusive, not PASS or revocation. | R28 det |  |
| ADR12-102 | Current owner L156 | Do not treat unbuilt enforcement as permission: the generic blind CLI omitting prereg/admission does not exempt the named blind channel's prospective prereg and K ceiling. | R23 det |  |
| ADR12-103 | Current owner L185 | Shape checks (check_brief, adr-graph, state-currency) prove no adoption or evidence integrity; inspect channel amendments, pinned freeze chains and manifest agreement; citations prove nothing. | R21 abs |  |

</details>

<details><summary><code>docs/adr/2026-08-30-evaluation-order.md</code> — 22 rules: 1 absorbed, 20 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-104 | Decision Effective L22 | Every contract frozen after 2026-08-30 follows the ten-step order, even while channel adoption is pending; PIPELINES and historical stage labels hold no competing authority. | R24 det |  |
| ADR12-105 | Step 1 L29 | Before catalogue freeze, K and data, apply the structural class screen (EM0, EM3, EM4, EM5/N-SHAPE, Product-Group/sign, session, S7 occupancy); measured N-EDGE/N-SIZE wait for data. | R24 det |  |
| ADR12-106 | Step 3 L37 / HARV L115 | HARV candidates simulate every scorable killing limb (cost, Confirm, placebo, shape, latency, firm geometry, temporal) in its own units before freeze; other channels need separate ratification. | R24 det |  |
| ADR12-107 | Step 4 L43 / Reachability L109 | Every channel needs conservative citable win-rate/mean-win/mean-loss priors (Requirement 2 haircut) or a completed probe; without them the limb is UNSCREENABLE; never freeze shape unscored. | R24 det |  |
| ADR12-108 | Step 5 L43 / Reachability L88 | Before Explore, run TRADEABLE-REACHABLE by delegating cost, latency, firm geometry and payoff shape to their named owners; it derives no new formula. | R24 det |  |
| ADR12-109 | Reachability L89 | Apply no universal cost hurdle at admission or harvest; each evaluation estimates its own net return, execution uncertainty and cost sensitivity, scoring declared cost gates in own units. | R24 det |  |
| ADR12-110 | Reachability L94 | Pin cost authority and revision at freeze; a later authority or scope revision voids and refreezes the affected campaign and attestation, never silently rescoring it. | R23 det |  |
| ADR12-111 | Reachability dated note L98 | Route the per-event cost limb to Requirement 5 and let the no-counterparty channel defer it to its Confirm-measured effect. | R24 DEL | Superseded by Joshua's 2026-10-24 ruling: Requirement 5 deleted; §Reachability dated note says blind-only exception lapses. |
| ADR12-112 | Reachability L123 | A pre-Explore economic failure stops Explore and appends the failed limb to the contract, labeled 'priors-derived, no mechanism test run', never MARKET-NULL or EXPRESSION-FAIL. | R24 det |  |
| ADR12-113 | Step 6 L46 | Open the register_search manifest before any exploration read; score the entire frozen catalogue, select ≤M cells, and hash-pin ranking plus selection before holdout access. | R23 det |  |
| ADR12-114 | Step 7 L51 | Check contract integrity first: hashes, ledger vs contract K, multiplicity config, holdout reservation, identity vs selection freeze, N_expr ordinal; mismatch is EVIDENCE-VOID, not rejection. | R24 det |  |
| ADR12-115 | Step 8 L57 | Before holdout, recheck Product-Group/sign, cap, session and S7 occupancy against the frozen snapshot; failure emits ROLE-BLOCKED, never a lifecycle or register rejection. | R24 det |  |
| ADR12-116 | Step 8 L67 | Forfeit a ROLE-BLOCKED Confirm slot by default with M unchanged; only prospectively declared mechanical succession takes the next ranked cell, repeating steps 7–8 without discretion. | R24 det |  |
| ADR12-117 | Step 8 L59 | Treat variance-dominance limbs as report-only without a live applicable producer; breadth.py panel availability grants no universal hard promotion or live composition authority. | R24 det |  |
| ADR12-118 | Step 9 L72 | Run the untouched Confirm statistic and minimum temporal-consistency battery as one atomic step; emit an evidence outcome only after adjudication. | R24 det |  |
| ADR12-119 | Step 10 L75 | Score portfolio and venue fit last, CONFIRMED only, rechecking S7 occupancy; placement failure leaves standalone confirmation intact (CONFIRMED · VENUE-FAIL is valid). | R24 det |  |
| ADR12-120 | Decision L81 | Fit screens (steps 1/8/10) and integrity checks (step 7) never substitute for the survivor-scoring Part-A gate, which owns lifecycle admission. | R15 det |  |
| ADR12-121 | Confirm verdicts L131 | Emit exactly one of four Confirm outcomes by precedence: EVIDENCE-VOID, then MARKET-NULL (powered discriminator fails), EXPRESSION-FAIL, CONFIRMED. | R24 det |  |
| ADR12-122 | Confirm verdicts L141 | An underpowered discriminator is not evidence against the mechanism; a payoff pass cannot rescue a clean discriminator failure. | R24 det |  |
| ADR12-123 | Confirm verdicts L146 | Route MARKET-NULL to edge-failure and EXPRESSION-FAIL to expression-failure; keep EVIDENCE-VOID, ROLE-BLOCKED, CHANNEL-FAIL and post-confirm VENUE-FAIL out of WHY-rejected registers. | R26 abs |  |
| ADR12-124 | Confirm verdicts L153 | Pre-contract source or intake failures never acquire Confirm-state labels such as EVIDENCE-VOID or EXPRESSION-FAIL. | R24 det |  |
| ADR12-125 | First review L166 | At the 2026-11-08 review, and on any cost-authority change, audit runs for out-of-order steps, invented arithmetic, fit-only rejections and verdict precedence; correct at owner first. | R28 det |  |

</details>

<details><summary><code>docs/adr/2026-09-02-portable-edge-cultivation-campaign-objective.md</code> — 14 rules: 3 absorbed, 4 detail, 7 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR12-126 | §1.1 L39 | Optimize the campaign first for a portable genuine edge; Tradeify_Select_100K is the preferred edition, not the definition of edge. | R24 DEL | Historical: campaign closed PRE-CONTRACT DROP (Addendum 2026-09-03b); edge-vs-edition separation now owned by evaluation-order Step 10. |
| ADR12-127 | §1.1 L43 / §3 L143 | Accept manual weekly preservation as the account-level inactivity control; do not require candidate alpha to manufacture weekly activity. | R24 det |  |
| ADR12-128 | §1.2 L48 | Bound the campaign to 2–3 days, research/paper scope, ≤3 seats, one contract (M=1, alpha 0.05 Bonferroni), $0 external spend and ≤48 local core-hours. | R2 DEL | Historical: campaign bounds spent; T0 closed PRE-CONTRACT DROP in Addendum 2026-09-03b, no contract opened. |
| ADR12-129 | §1.3 L61 | Map three OUTER investigations to seats A/B/C, ≤8 iterations each; at 8/8 stop with the structured report; only operator or Rule-0 re-audit extends. | R2 DEL | Historical: seats A and B STOPPED, C unused per Addendum 2026-09-03b item 5; campaign terminal. |
| ADR12-130 | §1.4 L73 | Freeze contract and K manifest before scoring the first exploration payoff cell; outcome-guided work cannot later be wrapped as prospective; post-outcome payoff changes need a new campaign. | R23 abs |  |
| ADR12-131 | §1.4 L86 / §3 L138 | Make the Confirm interval's first eligible bar strictly later than the founding-freeze commit; bars between the last source read and the freeze are excluded. | R23 DEL⚖ | Campaign-scoped (§1.4) rule; campaign closed 2026-09-03b; candidate-contract freezes never adopted it. Operator decides whether to generalize. |
| ADR12-132 | §1.5 L97 / §3 L136 | Keep exact ORB-MYM P50 source-only: no retroactive contract, Confirm label or preregistered claim; admission needs a separate operator-ratified source-intake decision. | R23 det |  |
| ADR12-133 | §1.6 L113 | Before a contract exists, use EVIDENCE-BLOCKED for missing private sources and PRE-CONTRACT DROP (naming the intake limb or venue/cost-constraint shape) otherwise. | R24 det |  |
| ADR12-134 | §1.6 L118 / §3 L141 | Never count a pre-contract drop, including venue/cost-constraint-shaped ones, against the mechanism's N_expr ladder. | R26 abs |  |
| ADR12-135 | §2 item 3 L130 / Addendum item 6 L220 | Q-VOLREGIME L1–L4 class findings may motivate prospective cultivation but confer no candidate status, Confirm, venue-MC or lifecycle inheritance, nor waive the freeze/K boundary. | R25 det |  |
| ADR12-136 | Addendum 2026-09-03 L198 | Run this campaign as VOLREGIME translation entering Packet T, MNQ primary, with a campaign-only L5 waiver; keep it off-queue pending operator promotion. | R3 DEL | Historical: T0 closed PRE-CONTRACT DROP (Addendum 2026-09-03b); campaign-only waiver and packet entry spent. |
| ADR12-137 | Addendum 2026-09-03b item 3 L244 | Before any entry construct from Q-VOLREGIME-1, supply a raised-bar Route 1/2/3 argument; the L5 skip did not waive it. | R26 abs |  |
| ADR12-138 | Addendum 2026-09-03b item 4 L248 | Treat a pre-freeze extraction probe as needing its own operator envelope and Confirm reservation; the campaign envelope is not that approval. | R23 DEL | Superseded by candidate-contract §Campaign authority amendment (operator ruling 2026-10-24): in-scope probes need no separate approval. |
| ADR12-139 | Addendum 2026-09-03b items 1-2 L237 | Close T0 as PRE-CONTRACT DROP; open no T1/T2, contract or third template under this campaign. | R28 DEL | Discharged: T0 closed PRE-CONTRACT DROP 2026-09-03b; any reopening already needs operator authorization (Rule 3). |

</details>

<details><summary><code>docs/adr/2026-09-03-venue-legality-re-expression-lane.md</code> — 21 rules: 4 absorbed, 3 detail, 14 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR13-1 | §0 L21 | Treat an exit filled at or after the venue deadline instant as FORCE_FLAT_VIOLATION; only fills strictly before the deadline are legal. | R16 det | → lab/research_utils/trade_reconciliation.py (_deadline_timestamps) |
| ADR13-2 | §1 L64 | Treat a venue-legality flag as a block on that strategy, never a tuning opportunity. | R23 abs |  |
| ADR13-3 | §2 L80 | Enter the re-expression lane only on a named Phase 1 venue-legality flag (force-flat, weekend/overnight hold, contract-cap breach), never on a performance result or hunch. | R23 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-4 | §2 L84 | Change only the session bound (entry cut-off and forced flatten); carry every other parameter across byte-identical in intent and re-verify by diff. | R14 DEL⚖ | Stricter live owner: AGENTS.md locked parameters immutable (no lane exception remains); applied edits recorded in guard spec §8; campaign closed 2026-09-10. |
| ADR13-5 | §2 L90 | Give each replacement a new strategy id, Pine filename, hash pin and config entry; keep the superseded entry under superseded_sources; transfer no verdict, anchor or result. | R23 det |  |
| ADR13-6 | §2 L94 | Treat each replacement export as development data: model-fitted, never out-of-sample, EXPLORATORY claim class. | R23 det |  |
| ADR13-7 | §2 L97 | Re-run the full Phase 1 gate G1.1–G1.10 on each replacement with its own inventory, anchors, hashes and venue audit; never use the twelve-item delta read. | R24 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-8 | §2 L100 | Drop the strategy if its replacement fails the gate or is not produced; never advance the venue-illegal original export. | R28 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-9 | §2 L103 | Accept the lane ADR before anyone inspects any replacement export's results; inspecting first voids the lane and drops the affected strategies. | R23 DEL | Discharged: Status line records operator ratification 2026-09-03 before any replacement export existed. |
| ADR13-10 | §4 L138 | Produce at most one replacement per strategy, counted from the first export against the verified D12 calendar; a second attempt is void and the strategy drops. | R23 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-11 | §4 L140 | Never produce a replacement export against the interim placeholder early-close list or before the verified calendar lands. | R16 DEL | Struck and marked DISCHARGED 2026-09-03 in §4; verified calendar landed at ops/calendars/cme_holiday_calendar_2022_2026.json. |
| ADR13-12 | §4 L150 | Use the single union early-close calendar from ops/calendars/cme_holiday_calendar_2022_2026.json identically in every body, never a per-product-group list. | R17 abs |  |
| ADR13-13 | §4 L155 | Accept the calendar's SECONDARY provenance for date membership only, not per-group close times; every non-calendar verdict cap still binds. | R17 abs |  |
| ADR13-14 | §4 L165 | Cap a replacement's verdict at NEEDS_CONTEXT because the calendar's provenance is SECONDARY. | R17 DEL | Superseded 2026-09-03 by operator ruling D19 (campaign-state §6); clause already struck in §4. |
| ADR13-15 | §4 L167 | Add a no-trade block on early-close dates closing before the holiday-short deadline; a replacement relying on the deadline there is not venue-legal. | R16 DEL⚖ | Lane obligation; campaign selection CLOSED 2026-09-10; Track B superseded 2026-10-16; Good-Friday exposure also recorded at campaign-state §12. |
| ADR13-16 | §4 L174 | Do not use the lane for the dropped Q-TXG-1 swap-port exports; a mis-sized export is re-runnable only with corrected input under its own ruling. | R23 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-17 | §4 L177 | Never treat the venue auto-flatten as the backstop that makes a late exit acceptable. | R16 abs |  |
| ADR13-18 | §5 L184 | Pass a replacement only with zero force-flat violations, zero Friday-to-Sunday holds, a diff matching guard spec §8 exactly and G1.1–G1.10 clear; otherwise drop, no third attempt. | R24 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-19 | §6 L213 | Falsify the lane on process compliance only: bound differs from spec, diff exceeds §8, frozen re-export settings differ, or a second replacement; never on expected economic reordering. | R28 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-20 | §7 L232 | Count a replacement as a cell of its superseded body's template, keeping the per-template contract count at five. | R23 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |
| ADR13-21 | §7 L234 | Count each replacement's Phase 1 cycle as a Rule 2 iteration against contract item 13; it is not exempt and the ceiling is unchanged. | R2 DEL⚖ | Lane retain-until met: campaign selection CLOSED 2026-09-10 (campaign-state Status); Track B superseded 2026-10-16 (checklist addendum); ADR status unchanged. |

</details>

<details><summary><code>docs/adr/2026-09-05-tradeify-select-striker-expression-readmission.md</code> — 21 rules: 2 absorbed, 18 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR13-22 | §0 L24 | Require effective chart-input binding at intake; source hashes alone do not establish the captured chart's behavior. | R0 det |  |
| ADR13-23 | §1 L37 | Never escape a prior de-scope by assigning new IDs or reinterpreting an old measurement as a re-scope result; make eligibility explicit. | R15 det |  |
| ADR13-24 | §2 L43 | Treat the two named Striker campaign expressions as eligible for the Tradeify Select 100K evaluation only, by operator election; eligibility asserts no qualification. | R15 det |  |
| ADR13-25 | §2 L51 | Before deploying an admitted expression, require bound effective inputs, valid size evidence, frozen acceptance tests, winner execution parity, M1 RESOLVED and a separate operator GO. | R10 det |  |
| ADR13-26 | §2 L53 | Keep the locked Striker editions WITHDRAWN at zero allocation and preserve their ledger rows; bar funded deployment for those editions and these expressions. | R15 det |  |
| ADR13-27 | §2 L66 | Do not treat long-only direction as sufficient for shared-symbol co-exposure; admit it only with implemented and proven per-strategy ownership. | R11 det |  |
| ADR13-28 | §2 L71 | Apply S7's third-leg symbol-occupancy screen only where its incumbent trigger fires; it is not a blanket exclusion between this campaign's candidates. | R24 det |  |
| ADR13-29 | §2 L86 | Run one execution controller per order symbol with per-strategy filled quantity and order ownership; exits reduce only their own allocation, never flatten another or create unintended shorts. | R11 det |  |
| ADR13-30 | §2 L89 | Freeze deterministic priority and rejection behavior for insufficient account-wide headroom, including reservations; never reject same-direction signals merely for sharing a symbol. | R11 det |  |
| ADR13-31 | §2 L99 | Treat shared-symbol execution as an implementation obligation, never authorization to change legacy LEG_MAP cap allocations or production risk constants. | R14 det |  |
| ADR13-32 | §2 L103 | Before search, make joint replay implement the same quantity ownership, exposure, reservation, skipped-signal and exit policy intended for execution. | R24 det |  |
| ADR13-33 | §2 L105 | Before deployment, prove ownership and parity under partial fills, duplicate/delayed messages, simultaneous stop/target, cancellations and restart; unproved blocks deployment; failure licenses no post-result change. | R10 det |  |
| ADR13-34 | §2 L108 | Keep the single-attempt budget, S1/S2 consequences and eval-only authorization unchanged for the admitted expressions. | R3 abs |  |
| ADR13-35 | §4 L123 | Stop an expression at intake on identity mismatch; a failed final validation ends the campaign attempt (D33); neither authorizes substitution or funded trading. | R28 det |  |
| ADR13-36 | §4 L126 | If the operator withdraws the election, revoke this scope exception through a recorded successor decision; check scope at candidate freeze and deployment review. | R3 det |  |
| ADR13-37 | §5 L131 | Do not infer altered trade streams by scaling realized P&L through active dollar or equity stops. | R24 det |  |
| ADR13-38 | §5 L132 | Do not promote the old locked Striker editions through the new campaign rows. | R15 det |  |
| ADR13-39 | §5 L133 | Do not treat an operator scope election as empirical falsification; it yields no RESOLVED or FALSIFIED verdict. | R28 det |  |
| ADR13-40 | §5 L133 | Do not add a new token-trade capacity test to reopen the already accepted inactivity mitigation. | R20 det |  |
| ADR13-41 | §7 L150 | At a winner's Phase 8, verify its actual identity and runtime bindings against this scope; never infer them from the candidate ledger. | R0 abs |  |
| ADR13-42 | §7 L148 | Apply the reciprocal header edge, add the two zero-capital CANDIDATE ledger rows and update campaign and plan pointers. | R32 DEL | Discharged: descope ADR carries reciprocal Superseded-in-part-by line; rows 18-19 CANDIDATE at zero in ops/venue_editions/Tradeify_Select_100K.md. |

</details>

<details><summary><code>docs/adr/2026-09-06-tracked-file-reduction-prune.md</code> — 12 rules: 3 absorbed, 7 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR13-43 | §1 L18 | Reduce the tree to 1,500 files with survivor/removal lists partitioning the pinned baseline exactly, then execute the §4 removal, index, catalog and pointer edits. | R31 DEL | Executed by PR #316 merge 2026-09-06 (7185ccf), recorded in the Status line. |
| ADR13-44 | §1 L27 | Retain a bundle only for a present need; historical complexity explains care in pruning but never decides retention. | R31 abs |  |
| ADR13-45 | §1 L27 | Treat a historical citation as a dependency resolved by archive reference, not a retention entitlement, unless the cited content is executed or gate-validated. | R31 abs |  |
| ADR13-46 | §1 L24 | Before removing files, verify archive preservation against the remote using immutable commit and blob SHA references. | R31 det | → docs/operational_rules.md §16 |
| ADR13-47 | §1 L22 | Remove obsolete closure exemptions while preserving checks for surviving closures; every GRANDFATHERED name must exist. | R26 det |  |
| ADR13-48 | §1 L25 | Include surviving-document link cleanup in any removal, repointing links to immutable archive URLs with anchors, rather than leaving broken navigation. | R31 det | → docs/operational_rules.md §16 |
| ADR13-49 | §2 L31 | Apply the adjudicated survivor rules (wholesale directories, explicit study list, executed or gate-validated citations, non-citing historical surfaces) to the 2026-09-06 pass. | R31 DEL | Pass-specific survivor rules applied in executed PR #316 (2026-09-06); standing retention owned by operational_rules §16. |
| ADR13-50 | §3 L45 | Unarchive the read-only first-passage-archive repository before any future preservation push. | R31 det |  |
| ADR13-51 | §3 L46 | Retrieve removed paths on this clone with git show <baseline SHA>:<path>; no archive access needed. | R31 abs |  |
| ADR13-52 | §4 L52 | Treat lab/ARCHIVED.json as a retrieval and rendering aid only; retained partial-study remnants are fixtures, not bodies, and the hot-body check skips them. | R31 det |  |
| ADR13-53 | §5 L60 | Leave dead links in frozen surfaces (SESSIONS, pre-registrations, ltm, retained lab research bodies, core, tests); resolve them through the archive, never by editing. | R31 det |  |
| ADR13-54 | §5 L61 | Operator to rewrite REPO_MAP.md/PIPELINES.md for the reduced tree and decide at the next audit whether the In-flight-label-only and WARN-reference files stay. | R31 det |  |

</details>

<details><summary><code>docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md</code> — 54 rules: 5 absorbed, 19 detail, 30 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR13-55 | Layer L16; §4 L156 | Never edit core/dd_protection.py, rebind DD_TRIGGER/DD_SCALE, or change calculate_protection or its validation pins on any Track B branch; revert any such diff. | R14 abs |  |
| ADR13-56 | Review boundary L21 | Do not let unaccepted execution-model drafts #368–#370 or historical #365 ratify this ADR, admit its row or satisfy any policy or activation gate. | R3 DEL⚖ | Review boundary moot: Track B superseded for Tradeify 2026-10-16 (checklist addendum); instance not pursued; ADR header unchanged. |
| ADR13-57 | §0 L47 | Do not read a green check_adr_graph run on a Proposed ADR as acceptance evidence; simulate A2 with the status set to Accepted. | R32 det | → docs/adr/README.md |
| ADR13-58 | §0 L47 | Put each supersession edge on its own header line and the reciprocal Superseded-in-part-by on a separate parser-visible line. | R32 abs |  |
| ADR13-59 | §2.1 L63 | Record the instance's reference_mode as fixed trailing by this ADR, never dispatched via reference_mode_for_dd_type; TB-D0 must test that no code path resolves it so. | R14 DEL⚖ | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-60 | §4 L157 | If the evaluation lock becomes reachable or book_policy and the registry disagree on reference_mode, halt the live path and re-admit under a fresh ADR; never edit. | R14 DEL⚖ | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-61 | §2.2 L64 | Apply the mechanism invariant: six-decimal inclusive trigger compare, day mode from the prior settled close with no intraday change or latch, scale compounding with lifecycle haircut before flooring. | R14 det | → docs/adr/2026-07-13-dd-protection-concept-not-constant.md §2 |
| ADR13-62 | §2.2 L64 | Record the per-leg response map as a book property in book_policy.BOOK_LEGS/TB-S1; the registry row carries only three variables; ORB's mode response replaces the multiplier there only. | R14 DEL⚖ | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-63 | §2.3 L65 | Run no trigger×scale grid, second cell or policy comparison in Track B; a failed confirmation ends the attempt without admission and never reopens the policy choice. | R23 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-64 | §2.4 L67 | Freeze the K = 1 confirmation contract at TB-F1, carrying Part A and deviations A1/B1/B2 verbatim, before TB-E1 runs. | R23 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-65 | §2.4 L68 | Apply the regime-robustness gate in full for a new POLICY_REGISTRY instance; state and ratify each deviation from its canonical procedure rather than assuming it. | R24 DEL⚖ | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-66 | §2.4 L68 | Build Part A from 100 resampled 6-month-block panels at original session length with rebuilt inner blocks; require p5 pass-rate ≥ the full-panel floor; keep close-call and sanity rules. | R24 DEL⚖ | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-67 | §2.4 L68 | Replace the H1+H2 path-count sanity check with source-session partitioning; keep full parent MC depth separately for full, H1 and H2; never substitute half depth. | R24 DEL⚖ | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-68 | §2.4 L68 | Freeze Part A's exact integer depth, budget calculation, block, RNG and percentile rules at TB-F1; TB-E1 is forbidden until a second dated operator addendum ratifies that depth, no placeholders. | R23 DEL⚖ | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-69 | §2.4 L68 | Evaluate each Part B half with a one-sided 95% upper failure bound ≤ 5%, never a statistic weaker than the gate's point criterion; no separate regime floor. | R24 DEL⚖ | E1 spine superseded 2026-10-16; this regime-gate deviation design might serve a personal-lane instance, so retention is the operator's call. |
| ADR13-70 | §2.4 L68 | Run Parts A and B once inside TB-E1 on the n2 stream; TB-E2 evaluates exactly the four n3 conditions and never reruns Part A. | R23 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-71 | §2.4 L69 | Admit in two stages (TB-D0 executable admission after TB-E1's seal; TB-E2 qualification; TB-D2 plus GO reseal authorization); refuse the arm at every stage before T11. | R10 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-72 | §2.5 L70 | Cite the exploratory selection evidence as provenance only; never quote its figures or publish any bound, curve or replay statistic (D-B12). | R13 det |  |
| ADR13-73 | Effective L72 | Treat the fixed-instance decision and TB-F1 authorization as effective only on the first dated operator addendum; until then TB-F1 is forbidden. | R3 DEL | Discharged: first dated operator ratification addendum recorded 2026-09-14 UTC. |
| ADR13-74 | Fingerprint contract L76 | Freeze one shared fingerprint implementation, CPython patch, serializer, tool digests and byte/hash vectors before TB-F1; every consumer invokes it under that runtime; reimplementations are not equivalent. | R39 abs |  |
| ADR13-75 | Fingerprint contract L78 | Fingerprint with the frozen recipe: canonical policy-row JSON excluding provenance, AST-normalized dd_geometry minus only the registry assignment, full-byte SHA-256 elsewhere; refuse ambiguous registry rebinding. | R39 det | → ops/c1_rail/policy_fingerprint.py |
| ADR13-76 | Fingerprint contract L78 | Pin deterministic config serialization and the exact two-field initial-arm transition (dry_run, armed_until); refuse every other configuration change at activation. | R10 det |  |
| ADR13-77 | Fingerprint contract L80 | Provide conformance vectors proving key-order invariance, admission-invariant normalization, changed hashes for other mutations, refusal of multiple registry assignments and rejection of differing runtime/recipe/tool digests. | R39 det | → tests/ops/test_policy_fingerprint.py |
| ADR13-78 | §4 L152 | On any failed TB-E1 legality screen, n1 cutoff, n2 limb or Part A, end the attempt with no admission, grid, runner-up or second sample; a closure supersedes this ADR. | R28 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-79 | §4 L155 | Land the registry row only in TB-D0 after TB-E1's seal, with provenance naming both ratifications, the TB-E1 freeze date and FBR digest; otherwise git-revert it and record the deviation. | R14 DEL⚖ | Instance row never landed; tests/core/test_dd_geometry.py pins POLICY_REGISTRY == {}; frozen constants and concept ADR govern; Track B superseded 2026-10-16. |
| ADR13-80 | §5 L169 | Permit only the one-line TB-D0 row addition to POLICY_REGISTRY; never change dd_geometry semantics (ProtectionPolicy, REFERENCE_MODES, reference_mode_for_dd_type). | R14 det | → docs/adr/2026-07-13-dd-protection-concept-not-constant.md §2 |
| ADR13-81 | §2a T4a L93 | Record the TB-D1 ORB operator GO before V1 binding, the live test and B7, and recheck it before n3; a withheld GO blocks. | R10 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-82 | §2a T5 L94 | Run image v1 as dry-run emit only; --arm must refuse while the GO artifact is absent. | R10 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-83 | §2a T6 L95 | Seal EF1 at B7 only when every shared component, including the size-vector hash, equals FBR, so the rail sizes with the qualified vector; otherwise no B7, recapture. | R39 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-84 | §4 L153 | On a failed sole n3, retire the row: closure supersedes this ADR, remove the row, redeploy an image without it before any later arm, never write the GO. | R28 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-85 | §2a T9 L98 | Write the TB-D2 decision record with digests and verdict labels only, at a docs/notes path outside the listener build context. | R13 DEL⚖ | Stricter live owner AGENTS.md §Public-clone posture governs; TB-D2 record never written; Track B superseded 2026-10-16. |
| ADR13-86 | §4 L158 | Write DEPLOYMENT_GO.json (closed ten-field set) only in TB-D2 after the operator's recorded GO, in an artifact-only commit; revert any earlier, mismatched or multi-path GO commit. | R10 det |  |
| ADR13-87 | §2a T10 L99 | Reseal only if the build-context diff is exactly the GO path, shared/config digests equal EF1, non-GO image layers match v1 in order, and S is valid without activity. | R39 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-88 | §2a T10 L99 | End the attempt on any shared-component change after B7 (no second n3); route a permitted non-shared change preserving non-GO layers to R1c and stop. | R28 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-89 | §2a T11 L100 | At initial activation validate GO structure, FBR and source digests, the host-verified EF2 manifest as typed --arm input, future valid_until, GO digest match and a fresh typed no-activity attestation. | R10 det |  |
| ADR13-90 | §2a T11 L100 | Treat the activation config write as a pending request: restart with risk-add disabled, repeat checks, durably record acknowledgment before risk-add, operator confirms before declaring armed. | R10 det |  |
| ADR13-91 | §2a T11 L100 | Persist activation request, attestation and acknowledgment evidence separately from the config so it introduces no unreviewed fingerprint exclusion. | R39 det |  |
| ADR13-92 | §2a T11 L100 | Treat any later image change as voiding EF2; any failed T11 check refuses activation and leaves boot disarmed with recovery and status available. | R10 det |  |
| ADR13-93 | §2b L104 | Bake the GO artifact into the listener image via an absence-tolerant COPY; never read it from the volume or bake a placeholder; absence is the fail-closed state. | R10 det |  |
| ADR13-94 | §2b L105 | TB-I3 builds deployment_go.py, the --arm check and the effective-activation gate, with tests refusing invalid artifacts, mismatches, missing attestations, expiry, replay and crash, verifying both build states. | R10 det |  |
| ADR13-95 | §2b L105 | Treat host no-activity and EF2 attestations as attended operator evidence, not machine verification; the existing API does not prove absence of account activity. | R21 det |  |
| ADR13-96 | §4 L154 | On seal invalidation (C10) void the seal and dependent n3 and stop for the operator; never auto-draw a replacement or combine results; continuation needs a new operator decision. | R28 DEL⚖ | Stricter live owner: AGENTS.md Tradeify native-only row and checklist Addendum 2026-10-16 bar this route; instance chain not pursued. |
| ADR13-97 | §2b L109 | Consume S once for initial activation; later restarts start disarmed and old acknowledgments cannot re-enable; later rearming needs a separately ratified ongoing GO/state/fingerprint contract. | R10 det |  |
| ADR13-98 | §2c L111 | Make each downstream packet (TB-P1/F1, TB-S3 R-L, TB-D0, TB-I3, TB-B7, TB-E2, TB-D2, TB-O1) state its §2a obligations; derive every summary from the acceptance trace. | R33 DEL⚖ | Packet list is Track B's (superseded 2026-10-16); TB-I3/TB-O1 obligations already live in §2a; retention is the operator's call. |
| ADR13-99 | §2c TB-O1 L122 | Treat the legacy `--arm --hours` command as insufficient for activation until TB-I3 supplies tested typed inputs. | R10 det |  |
| ADR13-100 | §4 L148 | Treat a withheld or pending ratification or GO as BLOCKED — context-problem, never a technical verdict; reserve AMBIGUOUS for an unfreezable field, which closes the attempt. | R28 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-101 | §4 L148 | Keep deployment authorization (T10–T11) downstream of a RESOLVED verdict, never part of it. | R15 abs |  |
| ADR13-102 | §4 L160 | Never edit this ADR's decision text to revert; supersede it instead. | R32 abs |  |
| ADR13-103 | §4 L161 | Check R1a at TB-E1, R1b at TB-E2, R1c at E2 start/reseal/TB-B10, R2/R3/R5 on every Track B PR, and R4 at Tradeify rule re-verifications and TB-D0. | R28 DEL | Tradeify E1 qualification spine superseded 2026-10-16 (deployment-checklist addendum); instance chain not pursued; Branch (a) resume withdrawn. |
| ADR13-104 | §6 L184 | Do not let TB-I2 consume or TB-E1 seal evidence produced with pre-ruling book_policy laws; include book_policy's digest in FBR and pin the ruled Striker cap and Vanguard WATCH zero. | R24 DEL⚖ | Spine evidence rule superseded 2026-10-16; tests/ops/test_book_policy.py still pins the caps, so dropping ADR text is the operator's call. |
| ADR13-105 | §7 L191 | Keep the policy PR's merge separate from recording dated operator decisions; ratification addenda must name actual values and frozen evidence, never placeholders. | R3 DEL⚖ | Pending second ratification belongs to the E1 spine superseded 2026-10-16; placeholder ban otherwise covered by Rule 3 literal grants. |
| ADR13-106 | Addendum 2026-10-02 L254 | Count a committed TB-E1 FAIL followed by budget exhaustion as FALSIFIED under R1a; there is no 'exhausted' outcome, runner-up or second sample. | R28 DEL | Reading rule for a TB-E1 outcome; E1 never ran (T06/S8 not started) and the spine was superseded 2026-10-16. |
| ADR13-107 | Addendum 2026-10-11 L276 | Define size_vector_sha256 as sha256(canonical_json_bytes(sizing)) per the screen authority; publish only the hash, never the vector values. | R13 det |  |
| ADR13-108 | Addendum 2026-10-11 item 3 L291 | At activation require the GO's size_vector_sha256 to equal the owner's boot-time runtime stamp; missing, unreadable or mismatched refuses; production default refuses until a stamp reader exists. | R10 det |  |

</details>

<details><summary><code>docs/adr/2026-09-14-a7-attended-agent-capture.md</code> — 14 rules: 2 absorbed, 10 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR13-109 | §0 L17 | Do not treat local code changes or audit-hook results as evidence of a compatible deployed image or deployed readiness. | R21 det |  |
| ADR13-110 | §2 L25 | Permit attended agent capture and enable/inject only with Joshua's session GO, continuous presence and his confirmation of broker/route verdicts. | R10 det |  |
| ADR13-111 | §2 L25 | Record agent actions under a distinct agent source with retained action evidence; never label them Joshua-entered or reuse the manual source marker. | R11 det |  |
| ADR13-112 | §5 L43 | Do not retroactively relabel historical manual evidence or overwrite historical append-only returns. | R30 abs |  |
| ADR13-113 | §2 L25 | Admit only the candle timestamp and five OHLCV values into tool records; exclude raw account information, credentials and unrelated page contents; keep public evidence value-free. | R13 det |  |
| ADR13-114 | §2 L27 | Treat the variant as changing only who supplies controlled input, not item 5 limbs, M1 signoff, deployment gates or entitlements; it authorizes no feed, order or arm. | R3 abs |  |
| ADR13-115 | §6 L51 | Enable only with the source/actor procedure, reviewed compatible deployed revisions, current host preflight, exact fresh candle binding and attendance; otherwise FAIL and do not enable. | R10 det |  |
| ADR13-116 | §6 L51 | Accept the variant's code only when targeted tests and independent review pass. | R21 DEL | Discharged: §7 records 188 targeted tests passed and independent review accepted. |
| ADR13-117 | §4 L39 | Stop and tear down if the closed target is unestablished, unrelated account data is captured, late/duplicate input accepted or a venue sender reached; never substitute candles or widen deadlines. | R10 det |  |
| ADR13-118 | §5 L44 | Do not bypass the rejected browser URL test or infer an advertised export capability; use only the operator-approved candle-only tool-record path. | R10 det |  |
| ADR13-119 | §5 L45 | Re-check the selected timestamp in the final capture observation before reusing a cursor coordinate across chart scrolling. | R10 det |  |
| ADR13-120 | §6 L49 | Treat CLI actor declarations as non-authentication; still require session GO and actual tool and command receipts. | R10 det |  |
| ADR13-121 | §6 L49 | Do not conflate observed chart EDT with application CDT when converting chart timestamps. | R10 det |  |
| ADR13-122 | §6 L51 | Keep M1 acceptance unchanged until A8 obtains the actual evidence and dated signoff. | R10 DEL⚖ | Discharged: A8 signed acceptance 2026-09-14; live owner docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json reads RESOLVED. |

</details>

<details><summary><code>docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md</code> — 32 rules: 2 absorbed, 27 detail, 3 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADR13-123 | Decision 1 L13 | Treat the self-funded lane as reopened on the operator's personal Tradovate account with a maximum-growth objective, as a posture and research target pending the owed checklist. | R15 det |  |
| ADR13-124 | Decision 2 L16 | Select the personal portfolio for growth from existing strategies under their locks; it is not the Tradeify book by default. | R15 DEL | Superseded by Addendum 2026-10-11b: the pool is the Tradeify book's four strategies. |
| ADR13-125 | Decision 2 L20 | Give the chosen portfolio its own (portfolio, firm-tier) protection and sizing binding under the concept ADR; never edit the Tradeify binding or dd_protection constants. | R14 det |  |
| ADR13-126 | Decision 3 L24; Owed items 3-4 L63 | Activate the personal account as a CME data feed, dry-run included, only after Tradovate API/data access and CME licensing clear for every destination the feed drives. | R18 det |  |
| ADR13-127 | Owed item 3 L71 | Verify Tradovate API key, add-on and data-entitlement fees on the vendor page; the feed-note excerpts are not authoritative. | R17 det |  |
| ADR13-128 | Decision 4 L29 | Clear a portfolio only if intraday-honest simulated p99 peak-to-trough drawdown ≤ 15% after Tradovate costs and whole-contract rounding; highest median growth wins; no capital authorization before. | R15 det |  |
| ADR13-129 | Decision 4 L36 | Halt new entries and flatten when equity falls 15% below its running peak; resume only on operator GO. | R10 det |  |
| ADR13-130 | Effective L40 | Keep personal-account balances and P&L out of the repo; name starting capital only as E_0. | R13 det |  |
| ADR13-131 | Effective L40 | Apply AGENTS.md live-execution rules (M1, arming, per-session GO) unchanged to the personal lane. | R10 abs |  |
| ADR13-132 | Owed L63 | Require all seven owed items to clear before the first live order on the personal account. | R10 det |  |
| ADR13-133 | Owed item 2 L69 | Add the personal-account tier to core/firm_rules.py with starting_balance, then run the core/mc/preflight.py pre-flight and a re-MC under that tier. | R16 abs |  |
| ADR13-134 | Owed item 5 L75 | When the portfolio shares strategies with the Tradeify book, check copy-trading, hedging and account-linking rules against Tradeify's published agreement text. | R17 det |  |
| ADR13-135 | Owed item 6 L79 | Bind the personal account in its own rail account/instance binding, separate from the Tradeify instance, as configuration as code with no shared credentials. | R39 det |  |
| ADR13-136 | Owed item 7 L81 | Build a fail-closed running-peak halt-and-flatten control with tests and an activation check that refuses to arm without it. | R10 det |  |
| ADR13-137 | Current owner L87 | Keep lane scope here until an owner for items 1–7 is named; STATE carries the forward row; venue rules stay in firm_rules, feed questions in the feed note. | R29 det |  |
| ADR13-138 | Addendum 2026-10-11 L105 | Keep the Tradeify book's four strategies on the Tradeify lane only; draw the personal pool from other locked strategies. | R15 DEL | Superseded by Addendum 2026-10-11b (Tradeify book reused on the personal lane); option-c split kept as history. |
| ADR13-139 | Addendum 2026-10-11b L115 | Run a cheap sizing, margin and risk pre-screen before expensive runs, reusing existing personal-account components. | R36 det |  |
| ADR13-140 | Addendum 2026-10-11b L118 | Size the Tradeify book for E_0 starting from the retained FLOOR-HALF successor; keep OFF legs OFF; change a leg's state or quantity only by explicit, justified operator choice. | R15 det |  |
| ADR13-141 | Addendum 2026-10-11b L118 | Name each proposed rung's quantity behaviour (fixed quantity, risk multiplier, port map or on/off) so the tested portfolio is the one that would run. | R24 det |  |
| ADR13-142 | Addendum 2026-10-11b L118 | Do not restore the earlier five-leg study; keep the search for additional strategies off this deployment's critical path. | R3 det |  |
| ADR13-143 | Addendum 2026-10-11b L119 | Define the personal tier's own micro-cap source, risk-dollar basis and protection policy; never run the book path unbounded on a capless tier. | R16 det |  |
| ADR13-144 | Addendum 2026-10-11b L120 | Do not carry Tradeify screen results to the personal account; test drawdown, growth, fee and margin at E_0 with dated authoritative Tradovate margins. | R20 det |  |
| ADR13-145 | Addendum 2026-10-11b L121 | Report results on already-exposed panels as feasibility, not out-of-sample evidence; excluding a configuration after reading another result does not restore a holdout. | R23 det |  |
| ADR13-146 | Addendum 2026-10-11b L121 | Freeze further choices before any E_0 scoring output and justify trial accounting in the study, not by a K count alone. | R23 det |  |
| ADR13-147 | Addendum 2026-10-11b L122 | Deployment Coordinator owns #752, re-scoped in place; closing it or opening a replacement is optional; preserve existing implementation owners. | R4 DEL | Stale: #752 (Q-SFCLEAR-2) superseded by Q-SFCLEAR-3 before any run (STATE 2026-10-14); dispatch paused 2026-10-19. |
| ADR13-148 | Addendum 2026-10-11b L125 | Read Agreement §6.6 as allowing the bot on the personal brokerage account with no prior-permission gate; Joshua weighs residual ambiguity; a support reply alone does not block. | R17 det |  |
| ADR13-149 | Addendum 2026-10-11b L126 | Keep sole-ownership and trading-records evidence ready for Tradeify document requests at any time. | R17 det |  |
| ADR13-150 | Addendum 2026-10-11b L128 | Be able to prove sole bot ownership with no other access or use; no high-frequency operation, team trading, third-party management, or copying/mirroring trades with others. | R17 det |  |
| ADR13-151 | Addendum 2026-10-11b L129 | Never hold opposing positions between a Tradeify account and an External Account in the same product or Product Group, at any time; no cure window exists. | R17 det |  |
| ADR13-152 | Addendum 2026-10-11b L131 | Before switching the active account, verify the outgoing one flat, without working orders and disarmed with no delayed-order path; uncertainty blocks; simultaneous operation needs its own ruling. | R10 det |  |
| ADR13-153 | Addendum 2026-10-11b L133 | Map Product Groups for the switch check from Tradeify's own source; a written Tradeify answer is not required to close item 5. | R17 det |  |
| ADR13-154 | Addendum 2026-10-12 L143 | Record Tradeify evaluation execution-route answers at the route owner; they do not gate the personal lane, whose broker/API, data, qualification and readiness gates stand. | R29 det |  |

</details>

### ADRs not Accepted, plus ADR INDEX/README/TOMBSTONES — 142 rules


<details><summary><code>docs/adr/2026-08-05-avenue-a-generate-confirm-route.md</code> — 2 rules: 0 absorbed, 0 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-1 | stub L12 | Open INDEX.md and read the cold body path a superseded ADR's hot stub names, not the stub itself. | R32 DEL | Only four hot stubs remain (ADRX-2..5), all superseded; stubs are optional legacy (ceremony-tiering ADR L58-60); tombstoning them moots this. |
| ADRX-2 | header L3-10 | Avenue A Route B generate-to-confirm order-flow discovery route no longer binds. | R25 DEL | Superseded 2026-08-24 by 2026-08-24-sourcing-phase-channel-retirement.md; body in docs/ltm/adr; stub optional (ceremony-tiering L58-60); tombstone, repoint refs. |

</details>

<details><summary><code>docs/adr/2026-08-10-implied-sr-plausibility-gate.md</code> — 1 rules: 0 absorbed, 0 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-3 | header L3-10 | implied_annualized_sr as a plausibility kill gate closing the fade design region no longer binds; implied SR is report-only. | R24 DEL | Superseded 2026-08-13 by 2026-08-13-implied-sr-report-only-fade-reopen.md; body in docs/ltm/adr; tombstone stub, repoint ops/instruments/MCL.md ref. |

</details>

<details><summary><code>docs/adr/2026-08-12-msl-implied-sr-disclosure-not-kill.md</code> — 1 rules: 0 absorbed, 0 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-4 | header L3-11 | MSL step-3 implied-SR as disclosure-not-kill ruling no longer binds separately; report-only owner governs. | R24 DEL | Superseded 2026-08-13 by 2026-08-13-implied-sr-report-only-fade-reopen.md; body in docs/ltm/adr; stub optional, tombstone it. |

</details>

<details><summary><code>docs/adr/2026-08-14-cc-cursor-autonomous-loop.md</code> — 2 rules: 0 absorbed, 0 detail, 2 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-5 | header L3-10 | Cursor-lane autonomous loop (dispatch without approval, merge without operator GO under a binary gate) no longer binds. | R4 DEL | Superseded 2026-09-15 by surface-allocation ADR; Cursor lane retired (TOMBSTONES 2026-09-15); body kept in docs/ltm/adr. |
| ADRX-6 | Disposition L10 | Merge authority returns to the operator with no automated exception. | R6 DEL | Superseded by AGENTS.md Merges and credentials (2026-10-24): agent merges pinned head after clean Codex review and green CI. |

</details>

<details><summary><code>docs/adr/2026-09-12-orb-mnq-r2-supersession-DRAFT.md</code> — 16 rules: 5 absorbed, 2 detail, 9 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-7 | Status L3 | Treat the ORB R2 supersession ADR as deciding nothing until TB-D1 fills the Decision slot from TB-E1 and the operator's fresh GO is a dated addendum. | R6 DEL⚖ | Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE); TB-E1/TB-D1 never fill. Withdrawing a PROPOSED ADR with unmet Retain-until is the operator's. |
| ADRX-8 | §2 L42 | Never use this ADR to unpark standalone ORB-MNQ-1, change its SCREEN-DEAD ledger row or pursuit, or authorize deployment, arming or any non-fixed size. | R15 det |  |
| ADRX-9 | §2 L40, §5 L71 | Fill decision grounds with digests and verdict labels only; never quote bounds, curves or replay statistics (D-B12 private-root rule). | R13 det | → docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md D-B12 |
| ADRX-10 | §4 L59 | Treat missing, incomplete or failed O-N/O-P (or O-N'/O-P') parity intake as BLOCKED capability-problem at the parity owner, not a failed book confirmation. | R28 DEL⚖ | TB-E1 parity-intake BLOCKED classification; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE) ends the E1 spine. |
| ADRX-11 | §4 L61 | If a validly executed TB-E1 fails legality, n1, n2 or regime-gate Part A with ORB present, record not superseded and end the attempt: no runner-up, no re-run without ORB. | R28 DEL⚖ | TB-E1 failure-terminal rule; Tradeify E1 spine superseded 2026-10-16 (checklist addendum); no TB-E1 will run under this ADR. |
| ADRX-12 | §4 L62, §6 L82 | On a passing sealed TB-E1, record digests and disposition and request the operator's fresh GO; a withheld GO is BLOCKED context-problem, never FALSIFIED. | R28 DEL⚖ | TB-E1 pass/GO-request branch; E1 spine superseded 2026-10-16 and R-2 qualification declined 2026-10-19 (checklist addenda). |
| ADRX-13 | §4 L64 | Once accepted, void the acceptance if the sole n3 (TB-E2) fails any bound; re-pointing again needs a new frozen contract and new ADR. | R28 DEL⚖ | TB-E2 voiding rule depends on an acceptance that cannot occur after the 2026-10-16 Tradeify Track B supersession. |
| ADRX-14 | §5 L70 | Do not fill a PASS/GO-request Decision without TB-E1's qualifying seal; no pre-E1, feasibility-screen or weighting-study evidence may fill either branch. | R23 DEL⚖ | Decision-slot fill restriction for TB-E1 seal; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE); slot never fills. |
| ADRX-15 | §1 L32, §3 L50 | Keep the book fixed: running it without ORB or with a changed expression is no substitute without requalification. | R15 abs |  |
| ADRX-16 | §6 L81 | TB-D1 fills the slot after TB-E1 and before TB-V1 and the B7-sealed image; record the operator's GO as a dated addendum and add STATE's decision-index row. | R6 DEL⚖ | TB-D1 fill and GO ordering before TB-V1/B7; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE); sequence not pursued. |
| ADRX-17 | Addendum 2026-10-03 L114-122 | For the trail-free orb_mnq_fixed_stop_oso edition, read the export pin as O-0' (SHA OWED) and parity grounds as O-N'/O-P' on its frozen effective settings. | R23 DEL⚖ | O-0'/O-N'/O-P' re-pointing for orb_mnq_fixed_stop_oso@Tradeify; Tradeify edition preregs superseded 2026-10-16 (checklist addendum). |
| ADRX-18 | Addendum 2026-10-03 L122 | Never relabel finite margin as zero; O-N'/O-P' margin follows the frozen settings and owed ORB finite-margin amendment, basis owed to the runtime owner. | R24 DEL⚖ | Scoped to Tradeify O-N'/O-P' parity, superseded 2026-10-16; general never-relabel-finite-margin rule stays at runtime-interface plan :16. |
| ADRX-19 | Addendum 2026-10-03 L126 | Treat TradingView CSV exports as operator acts; agents never automate TradingView login or actuation. | R4 abs |  |
| ADRX-20 | Addendum 2026-10-03 L128 | Run edition capture and parity only after the successor pre-registration freezes; no agent-run candidate replays before freeze. | R23 abs |  |
| ADRX-21 | Addendum 2026-10-03 L132 | Re-point a falsified target's scope only before freeze and before any run on it, disclose every exposure seen, and change no bound, threshold or outcome. | R23 abs |  |
| ADRX-22 | §10 L94-95 | Verify ADR form with check_brief.py --type adr and check_adr_graph.py; report that these validate structure only, not runtime behaviour or the full gate suite. | R21 abs |  |

</details>

<details><summary><code>docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md</code> — 74 rules: 5 absorbed, 56 detail, 13 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-23 | Trade-authority clarification L3 | Place, exit or cancel orders only at operator direction for the specific act; trade.submit is an operator act never grantable in a card; arming, spend and per-session GO unchanged. | R10 abs |  |
| ADRX-24 | §2 L47 | Treat Proposed incident-contract text as non-effective; until operator acceptance and propagation to governing owners, record dependent behaviour AMENDMENT_REQUIRED, not QUALIFIED. | R6 det |  |
| ADRX-25 | §2 L51 | After a qualified signal/control incident, let only pre-established platform protection continue within its prior envelope; the bridge observes and alerts but never creates, repairs, retunes or expands protection. | R11 det |  |
| ADRX-26 | §2 table rows 3-4 L57-58 | When protection identity, quantity, ownership, platform state, market data or manager health is uncertain, or safety state is mixed, escalate to immediate attended intervention; assert no autonomous protection. | R11 det | → docs/spec/2026-09-14-tb-s3-halt-resume-contract.md §2 |
| ADRX-27 | §2 table row 1 L55 | For a signal, daemon or control failure isolated from protection dependencies, latch the strategy halt, fence every strategy sender, retain observations and alert for attended intervention. | R11 det |  |
| ADRX-28 | §2 L62 | Never treat losing authority over a platform manager as proof it stopped; never blindly cancel a working protective stop or claim a remote pause. | R11 det |  |
| ADRX-29 | §2 Qualification L66 | Before admitting continuing protection, bind exact account, instrument, exposure ownership, platform mode, manager, child/OCO links, template and quantity; entry ack or local ATM ID is insufficient evidence. | R11 det |  |
| ADRX-30 | §2 Qualification L68 | Limit continuing protection to the original exit/stop/target/trail lifecycle and proved residual reduction; no entry, add, reversal, auto-reentry or post-incident parameter expansion. | R11 det |  |
| ADRX-31 | §2 Qualification L70 | Qualify only failure classes isolated from the manager's dependencies; shared host, restart, connection loss or stale observations are not signal-only; specify observation-gap and detection bounds first. | R11 det |  |
| ADRX-32 | §2 Qualification L72 | Treat post-fence late fills as outstanding obligations; never cancel or resend speculatively; automatic remainder cancellation or first attachment needs its own explicit amendment. | R11 det |  |
| ADRX-33 | §2 Qualification L74 | Begin attended intervention on the alert; session cutoff and own-flat deadlines stay obligations; prove the attended cutoff procedure under a signal incident before qualification. | R11 det |  |
| ADRX-34 | §3 L85 | Fence at the last strategy-command dispatch boundary including queues and reconnect replay; a dead daemon is not a fence; claim no exactly-once from local deduplication. | R11 det |  |
| ADRX-35 | §3 L87 | Do not conflate NinjaTrader ATM, Tradovate ATM and CrossTrade trailing, or transplant a lookup recipe to ATM without proof; absence from a query never permits resend. | R11 det |  |
| ADRX-36 | §1 L37, §3 L99, §A4 L203 | Claim no route sufficiency or capability from vendor documentation alone; documentary maps qualify nothing and CAP rows stay UNPROVEN until traced. | R0 det |  |
| ADRX-37 | §3 table L97 | Preserve current allocations and policy; any route-driven economic deviation needs separate acceptance on named evidence, never an invented tolerance or outage frequency. | R15 det |  |
| ADRX-38 | §4 Gate L105-107 | Mark a continuing-protection route QUALIFIED only when every applicable §3 row has route-bound evidence and passing traces; else UNPROVEN or UNSUPPORTED and live release blocked; recheck after changes. | R10 det |  |
| ADRX-39 | §4 L103 | If a qualified fault breaks manager dependencies, allows a new send or replay, loses protection identity or creates duplicate/reverse exposure, reject the route's continuation; never broaden the exception. | R11 det |  |
| ADRX-40 | §5 L111 | Do not replace automatic pause with an unrestricted risk-reducing send bypass. | R11 det |  |
| ADRX-41 | §5 L113 | Do not adopt server-side ATM capabilities for a local or NinjaScript route, or assume local ATM survives a host failure. | R11 det |  |
| ADRX-42 | §5 L114 | Do not silently replace portfolio bar, anchor, rounding or exit semantics with convenient platform-template behaviour. | R14 det |  |
| ADRX-43 | §6 L120 | Before implementation, propagate the authority split and no-same-session restriction into halt/resume, rail E1-E3/L2, feasibility, Phase 4-6, arming procedure and CAP; CAP stays verdict owner. | R29 det |  |
| ADRX-44 | §7 L126 | Keep current-contract qualification separate from prospective qualification under a proposed amendment; waive no current pause requirement while assessing. | R6 abs |  |
| ADRX-45 | §A1 L178-182 | Admit the bounded-exposure reservation only for one-contract entries carrying a native stop in one request, and only while CAP records single-call creation and first-fill activation. | R11 DEL⚖ | Option B deferred (§A11, §A12.3), CrossTrade placeoso-shaped (§A1); route rejected for Tradeify evals; stricter live owner §A12 F1(c) halt-on-unknown. |
| ADRX-46 | §A2 rules 3-4, 8; §A10 rules 4'-4c | In exceptional mode, admit a risk-add only if held allowances, open exposure and the new request fit room-to-floor less reserve; no waiver restores exhausted room. | R11 DEL⚖ | Option-B exceptional-mode admission deferred (§A11, §A12.3); F6 keeps no loss-room check; CrossTrade route rejected; ADR says deferred-not-deleted. |
| ADRX-47 | §A8 rule 9 L261; §A10 rule 9' L336 | Admit a split multi-contract intent whole or not at all: reserve whole-intent capacity before the first child; loss allowance applies only in exceptional mode. | R11 DEL⚖ | Rule 9' deferred (§A12.3); surviving split constraint owned by campaign §59 Ruling 5; Track B superseded for Tradeify 2026-10-16 (deployment-checklist addendum; STATE). |
| ADRX-48 | §A12.5 D4 L556; §A8 rule 10 L263 | Carry as a T09 acceptance case that a transport loss on split child k sends no child k+1; rule 10 itself is not first-release amendment text. | R11 det |  |
| ADRX-49 | §A9.1 UB-4 L307 | For editions, send each split child only after the previous is acknowledged; never retry an unknown child or top up a short fill; abandon unsent remainders on exceptional outcomes. | R11 det | → docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md §59 Ruling 5 |
| ADRX-50 | §A9 L274; §A12 Scope L417-421; D7 L558 | For any later option-B release, withhold acceptance until every UB-1 to UB-10 question has a written answer; §A12.3 replaced that gate only for the first release. | R11 DEL⚖ | Acceptance gate for deferred option B only; moot once option B (ADRX-45/46/54/55/57/59) is removed; stricter live owner §A12 F1(c) halt. |
| ADRX-51 | §A8 L268; §A12.7 L569 | Before accepting incident-contract amendment text, obtain a separate-session refute-first review spawned by the coordinator, not the author, plus a cross-vendor Codex review on the PR. | R5 det |  |
| ADRX-52 | §A9.1 UB-3 L306; §A10 rule 11 L340-345 | Stop risk-adds on all legs when monitoring or broker evidence is stale or a failed stop/unexplained exposure is open; restoration alone never resumes trading. | R11 DEL⚖ | D5 (2026-10-02): UB-3 not carried as text; superseded by stricter §A12.5 stale-evidence latch (session-closed admission), F5 and T13/D-MON. |
| ADRX-53 | §A9.1 UB-3 L306; §A10 rule 11.5 | Admit no risk-adds without confirmed attendance at session start, for all trading; the attended-operations contract (checklist T13) owns this rule. | R11 abs |  |
| ADRX-54 | §A9.1 UB-9 L312; §A10 rule 12 L349 | In exceptional mode, re-run the loss check before each admission after any new unknown, owned fill or terminal, equity update or stale input. | R11 DEL⚖ | UB-9 exceptional-mode re-check deferred by ruling (§A12.3 L521, L527); option B dormant; CrossTrade route rejected for Tradeify evals. |
| ADRX-55 | §A9.1 UB-2, UB-6 L305, L309 | Define the reservation as a conditional admission allowance, not a maximum loss; freeze formula, inputs, stale-data behaviour and calibration before production qualification; out-of-envelope values refuse binding. | R11 DEL⚖ | UB-2 reservation definition deferred (§A12.3 L521) with option B; CrossTrade route rejected; first release uses F1(b) unbound charge. |
| ADRX-56 | §A9.1 UB-5 L308 | Preserve each exit's intended scope with the simplest qualified closing primitive that touches no other owned exposure; exit-side partial completion is not moot. | R11 det |  |
| ADRX-57 | §A9.1 UB-10 L313 | Keep exactly one obligation record per child request in the account owner's existing attempt journal, never a parallel ledger, so no reservation is freed twice. | R11 DEL⚖ | UB-10 deferred (§A12.3 L521) with option B; no first-release reader; CrossTrade-shaped route rejected for Tradeify evals. |
| ADRX-58 | §A5 L234 | On option-B acceptance, give each named owner a dated addendum with the §A5 text; edit no owner text before acceptance. | R29 DEL⚖ | Option-B acceptance propagation; B deferred, first release used reduced §A12.4 set applied 2026-10-05; moot unless option B returns. |
| ADRX-59 | §A6 L247-250 | Reject the narrowed-shape reservation if CAP cannot record entry-stop atomicity, a vendor mechanism can grow or unprotect exposure, or a one-contract request can fill in several prints. | R11 DEL⚖ | Option-B narrowed-shape falsifier; B deferred (§A11, §A12.3) on CrossTrade CAP evidence; stricter live owner §A12 F1(c) halt-on-unknown. |
| ADRX-60 | §A7 L255 | Never feed held reservations into dd_protection's equity input, trigger or scale. | R14 det |  |
| ADRX-61 | §A7 L255; §A3 L199 | Bind gap allowance, reserve margin and room-to-floor figures only in load_bearing_numbers.md at candidate binding; write them nowhere else. | R20 abs |  |
| ADRX-62 | §A11 item 1 L361 | Run the first attended release preserve-and-block (an unresolved request halts automated trading) for one attended session, then explicit review before extension. | R10 det |  |
| ADRX-63 | §A11 item 4 L364 | Keep manual intervention available only subject to fencing, outcome evidence and reconciliation; claim no race-free manual action without evidence. | R10 det |  |
| ADRX-64 | §A11.1 items 1-2 L374-375 | Pursue C-a whole-leg broker liquidation as investigation only; accept no close-contract amendment or residual risk; a contradicting trace stops C-a. | R11 det |  |
| ADRX-65 | §A11.1 item 3 L376 | Require a separate operator expression decision and qualification for C-b (exit through each lot's own OCO); never adopt it automatically. | R11 det |  |
| ADRX-66 | §A11.1 item 4 L377; §A11.3 L400-411 | Perform R-1/R-2 REST reads operator-only, read-only, after entitlement confirmation; no purchase, new access, route change or order mutation. | R10 DEL⚖ | R-1 discharged 2026-10-01, R-2 closed with limits 2026-09-29 (§A12.5 UB-7 row); spent permission; AGENTS.md live-execution bars remain stricter. |
| ADRX-67 | §A11.1 items 5-6 L378-379 | Prepare each normal-case drill as an individual decision stating environment, actions, exposure limits and abort/recovery before seeking execution approval; never fall back automatically to the live evaluation environment. | R10 det |  |
| ADRX-68 | §A11.1 item 7 L380 | No agent places, amends or cancels an order. | R10 DEL⚖ | Superseded by surface-allocation Addendum 2026-09-30b; this ADR's L3 clarification marks it historical; frozen-adjacent, so operator's call. |
| ADRX-69 | §A11.1 Relation L382 | When preparing editions, never widen a subset exit into whole-leg liquidation. | R11 det | → docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md §59 Ruling 5 |
| ADRX-70 | §A11.2 L388-398 | In the first attended release and any armed commissioning session, an incident ends automated trading for the session: no same-session restart; continue recovery and evidence; review before another session. | R11 det |  |
| ADRX-71 | §A11.2 L390, O-6 L397 | Count a deliberate fault-free operator stop as an incident; correctly handled signal or capacity refusals are not incidents. | R11 det |  |
| ADRX-72 | §A12 Scope L417 | Apply §A12 only to the first attended release; armed commissioning sessions follow the accepted halt/resume contract until an explicit operator ruling extends it. | R11 det |  |
| ADRX-73 | §A12 Scope L417-421; §A12.3 | Within §A12's scope, §A12 governs over §A2, §A8, §A9 and §A10; deferred rules are preserved, not deleted, for any later option-B release. | R32 det |  |
| ADRX-74 | §A12 Relation L428 | Treat §A12 as changing no accepted contract or OPEN owner item; report any conflict with an owner as a review finding, never silently change the owner. | R29 abs |  |
| ADRX-75 | §A12.1 F1 L432-437 | Classify a request as unknown, an incident, once an accepted trigger fires (one-bar timeout, crash between send and outcome, unknown transport result) with no covering outcome; within-window requests are pending. | R11 det |  |
| ADRX-76 | §A12.1 F1(a) L438 | Retain ownership of an unknown request: no resend, speculative cancel, amend, repair or runtime cancel; absence, flatness, empty reads, time, reset, restart or acknowledgment release nothing. | R11 det |  |
| ADRX-77 | §A12.1 F1(b) L439 | Hold an unknown request's worst-case reservation (contract capacity plus retained charge inputs); never read an unbound charge as zero, released or available room. | R11 det |  |
| ADRX-78 | §A12.1 F1(c) L440 | On an unknown request, durably HALT the account: no new runtime broker mutation (exits, amendments, emergency cancel/close, scheduled flatten); alert for attended intervention; no resume or reactivation. | R11 det |  |
| ADRX-79 | §A12.1 F2 L443-449 | Release a held request only on a uniquely correlated accepted outcome, as a transfer to known order, confirmed exposure or unfilled-remainder release; quarantine collisions; absence never releases. | R11 det |  |
| ADRX-80 | §A12.1 F2 classes L451-453; D2 L552 | At runtime (T09) release only on a covering accepted terminal; in attended recovery a uniquely correlated outcome may transfer ownership once an accepted E3 producer exists. | R11 det |  |
| ADRX-81 | §A12.1 F2 L453 | Release no production resume implementation until a named accepted producer supplies each retained E1/E2/E3 fact. | R10 det | → docs/spec/2026-09-14-tb-s3-halt-resume-contract.md §4 |
| ADRX-82 | §A12.1 F3 L457-462 | Keep HALTED while any request is held; an F2 release never ends the halt or restores authority; end only after fresh §3 recovery and a new valid operator activation. | R11 det |  |
| ADRX-83 | §A12.1 F3 watch L464 | While any request is held, check for unexplained effects at each session open or the T13 owner's cadence; disarm does not satisfy it; alert-channel loss routes to D-MON/T13. | R11 det |  |
| ADRX-84 | §A12.1 F4 L468-482 | For an unknown amend, cancel, cancel/replace, close, attach or flatten, invoke immediate attended intervention, claim no autonomous protection, and refuse leg risk-adds until fresh-evidence reconciliation per type. | R11 det |  |
| ADRX-85 | §A12.1 F5 L484 | Treat any position, working order or fill unexplained by an owned operation or recorded operator action as an incident; an uncorrelated effect never releases a hold and is double-counted. | R11 det |  |
| ADRX-86 | §A12.1 F5 L484 | Settle who records an operator action, how and when, before placing an operator preservation trade while a request is held; until then an unrecorded operator action is an incident. | R10 det |  |
| ADRX-87 | §A12.1 F6 L486 | With no unknown request outstanding, keep admission exactly as today: no exceptional mode, loss-room check or bound worst-case charge in the first release. | R11 det |  |
| ADRX-88 | §A12.5 stale-evidence ruling L540, L561 | Treat stale order-level evidence as a refusal, not an incident; fresh evidence alone never lifts it; first release keeps admission closed for the session while risk-reducing exits continue. | R11 det |  |
| ADRX-89 | §A12.5 rows L539-540 | TB-I3/T09 owe implementations of the halt-on-unknown and the stale-evidence no-auto-resume latch; a synthetic CC-3 repair is not acceptance. | R11 det |  |
| ADRX-90 | §A12.5 subset-exit row L535 | Until a subset-close primitive is qualified, treat an unknown partial close offline: halt, presume per F4, retain everything; refuse sub-leg closes. | R11 det |  |
| ADRX-91 | §A12.5 C-a, M2 rows L536-537 | Reserve sending vendor questions and residual-risk or GC-2b decisions to the operator; coordinators prepare and review only. | R4 det |  |
| ADRX-92 | §A12.5 D1 L546-561 | Accept §A12 in one act after #575 merges, D2-D7 and the stale-evidence choice are recorded, refute-first findings fold, step-4 reviews are clean and T13 adopts the F3 watch. | R6 DEL | Discharged: §A12 ACCEPTED 2026-10-05 by D1, effective at 2c71e7e (#688 merge, verified in git). |
| ADRX-93 | §A12.7 L571 | Keep Tradeify live release held per T08 §7.8 part 1. | R10 det | → docs/briefs/handoffs/2026-09-21-tradeify-t08-broker-protection-feasibility.md §7.8 |
| ADRX-94 | Change history 2026-10-05 L604-605 | Apply the remaining §A12.4 propagation to edition pre-registrations at freeze and to the T09 handoff when written (owner: coordinator 4). | R30 det | → docs/notes/2026-10-02-a12-acceptance-packet.md §A12.4 |
| ADRX-95 | Addendum 2026-10-20 L575-582 | For the native NinjaScript pilot only, permit the bounded incident close and incident cancels of resting entries per runbook D-N1/D-N8; never cancel an unknown request. | R11 det | → docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md §5 |
| ADRX-96 | Change history 2026-10-05 L603 | Treat the G1 build, G10, Q7 (PASS) and HB-L1/L2 as arming preconditions. | R10 det | → docs/notes/2026-10-04-d1-t13-evidence-packet.md Q4 ruling |

</details>

<details><summary><code>docs/adr/INDEX.md</code> — 20 rules: 14 absorbed, 6 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-97 | header L3-4 | Never hand-edit docs/adr/INDEX.md; regenerate it with check_adr_graph.py --regenerate-index; ADR header fields are the source of truth. | R32 det | → docs/adr/README.md |
| ADRX-98 | header L5 | Read the ADR itself for its full Status; INDEX notes cells are truncated at 40 words. | R0 abs |  |
| ADRX-99 | Live L14 | Rule 0 is generalized by MVD discipline: code-level self-checks stay live; the doc-audit table and MVD-attest one-liner are not enforced. | R0 abs |  |
| ADRX-100 | Live L29 | Apply Rule 2 budget-before-acting to all substantial work (scope widened 2026-10-24). | R2 abs |  |
| ADRX-101 | Live L34 | Retiring a whole research subsystem is a subsystem/track-tier Delete needing STRATEGIC-LoR operator ratification; advisors draft and justify, the operator ratifies. | R3 abs |  |
| ADRX-102 | Live L42 | Keep HARV attestation a HARD gate that blocks register_search open on the mechanism-first lane. | R25 abs |  |
| ADRX-103 | Live L50 | Do not rebuild pairwise canonical-to-canonical drift detection after the params.toml mirror retirement. | R29 abs |  |
| ADRX-104 | Live L51 | Do not ratchet K per instrument; keep within-search K accounting (family-K bank is disclosure, not a gate). | R23 abs |  |
| ADRX-105 | Live L55, Partial L147 | Keep withdrawn Striker legs barred from redeployment; Tradeify is no locked-Striker deployment target; rail build, attended-only posture, $700 ceiling and arm gate stand. | R15 det | → docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md |
| ADRX-106 | Live L56 | Never silently redefine M1 item 5; its real-signal, expected-sizing and dry_run Stage-1 shape stand, changed only by express supersession. | R10 det | → docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md |
| ADRX-107 | Live L57 | Use the bounded sandbox-up lane as the only autonomous promotion; demotion, retirement GO, RETIRED re-entry, re-optimization, arm-gate and unattended bars stand. | R15 abs |  |
| ADRX-108 | Live L63 | Building the S2b signal daemon requires a separate operator build GO citing the S2b ADR and Accepted S2b spec. | R3 abs |  |
| ADRX-109 | Live L67, Partial L145 | Keep iterate-closure exit and closure-disposition coverage as HARD mechanical gates. | R28 abs |  |
| ADRX-110 | Live L102 | For the Tradeify portfolio instance, apply protection to the ORB leg as a mode response (base held, adds off while protected); the multiplier applies to other legs. | R14 det | → docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md |
| ADRX-111 | Partial L117, L142 | Use CME futures TradingView exports as the canonical feed; no CFD feed is canonical (Pepperstone, OANDA, Dukascopy retired). | R18 abs |  |
| ADRX-112 | Partial L126 | Retire what is no longer needed but do not over-retire: anything still materially useful to the operation stays. | R31 abs |  |
| ADRX-113 | Partial L130 | Treat dd_protection as a concept, not a constant: trigger, scale and reference mode are per-portfolio, per-firm-tier variables. | R14 det | → docs/adr/2026-07-13-dd-protection-concept-not-constant.md |
| ADRX-114 | Partial L137 | Never set dry_run=false while M1 is unresolved: the M1 gate's object is the arm, not the send. | R10 abs |  |
| ADRX-115 | Partial L147 | Do not carry the 0.50x rung to a different venue geometry; rungs above 0.50x still need the EV objective and both-halves gate. | R24 det | → docs/adr/2026-07-23-c1-rung-selection-ev-objective.md |
| ADRX-116 | Partial L150 | Use TNEC-1 as the intake gate (superseding MNQDTL-1); its §3.1 doors C1-C11 stand. | R24 abs |  |

</details>

<details><summary><code>docs/adr/README.md</code> — 3 rules: 3 absorbed, 0 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-117 | L7-9 | Write a new ADR only for durable architecture or governance rationale or authority no existing owner holds clearly; specifications, campaigns, plans and PRs may own decisions. | R32 abs |  |
| ADRX-118 | L10-12 | Author, revise and remove ADRs under the ceremony-tiering admission, retention and concise-form rules, using the brief-authoring ADR template's graph header and verification. | R32 abs |  |
| ADRX-119 | L12-13 | Neither a citation nor Accepted status makes an ADR permanent; it stays subject to the retention test. | R31 abs |  |

</details>

<details><summary><code>docs/adr/TOMBSTONES.md</code> — 23 rules: 14 absorbed, 8 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ADRX-120 | intro L4-5 | Treat tombstones and retrieved historical bodies as history, not renewed permission; the linked current owner governs present work. | R3 abs |  |
| ADRX-121 | 2026-10-24 L12 | Commit and push only your own codex/ or claude/ branch and open a PR; never push main; merging follows the operator's merge rule. | R6 abs |  |
| ADRX-122 | 2026-10-24 L12 | Resolve older ADR or record references to removed skills through the tombstone table; do not edit those older bodies. | R31 det |  |
| ADRX-123 | 2026-10-24 L12-14 | Retire legacy prohibitions assuming the barred book or rejected CrossTrade route, c1-rail invariant (5), and prop-firm-challenge legacy execution sections. | R31 DEL | Discharged by 2026-10-24 consolidation (#901, d402f800): c1-rail invariant 5 marked retired (SKILL.md L41); prop-firm-challenge narrowed. |
| ADRX-124 | 2026-10-24 L14 | Obtain the operator's GO for each account-preservation trade; the standing token-trade mandate is retired. | R10 abs |  |
| ADRX-125 | 2026-10-24 L14 | Never release or import retired skills; sync_skills.py RETIRED_SKILLS lets --prune remove their deployed copies. | R31 det | → scripts/README.md#skill-lifecycle |
| ADRX-126 | 2026-10-24 table L18 | Do not pull Databento data; the vendor is retired and the no-pull rule lives in c1-rail Hand-offs. | R18 abs |  |
| ADRX-127 | 2026-10-24 table L19 | Route live execution through c1-rail and AGENTS.md; OODA remains only a methodology loop in the canon. | R10 abs |  |
| ADRX-128 | 2026-10-15 L29-33 | Keep locked-book backtest figures and Pine-only session values off the public tree; locked values live only in the locked Pine. | R13 det | → AGENTS.md §Public-clone posture |
| ADRX-129 | 2026-09-15 L43-54 | Do not incorporate Cursor agents (only Claude and Codex); retrieving Cursor artifacts does not revive the lane. | R4 det | → docs/adr/2026-07-14-cc-cursor-surface-allocation.md Revision 2026-09-15 |
| ADRX-130 | 2026-09-15 table L63 | Treat wiring a harness hook as an operator election: propose unasked hooks, implement only when requested. | R36 abs |  |
| ADRX-131 | 2026-09-15 table L74 | Do not use git commit --no-verify or --no-gpg-sign; fix the hook failure unless the operator explicitly asks to bypass. | R19 abs |  |
| ADRX-132 | 2026-09-15 table L76 | Do not treat an empty rg result as evidence of no prior work; cold stores are excluded by .rgignore. | R8 abs |  |
| ADRX-133 | 2026-09-15 table L77 | Treat repo_retrieve.py as ASSISTIVE-ONLY; re-enabling its FTS companion needs a fresh frozen registration clearing the floor. | R8 det | → docs/briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md §Limb B |
| ADRX-134 | 2026-09-08 ox-alpha L89-93 | Do not invoke the ox-alpha stealth adversarial-lens model; reopening it needs a fresh ADR and operator GO. | R3 abs |  |
| ADRX-135 | 2026-09-08 persona L108-113 | Do not reinstate persona review panels, windows, November 8 backstops or restoration triggers; they are retired, not paused. | R3 abs |  |
| ADRX-136 | 2026-09-08 governance L136 | Keep STATE's operator queue at five or fewer live items in dependency and operator order, with no automatic replacement, channel or GO. | R34 det | → STATE.md §Operator queue |
| ADRX-137 | 2026-09-08 governance L136, L143 | Hold the November 8 attention/order review and failure-condition check via the root-doc charter and STATE pointer; it is not discharged. | R34 det | → docs/adr/2026-07-16-root-doc-charter-dedup.md trigger schedule |
| ADRX-138 | 2026-09-08 candidate L140-149 | Take candidate fields, freezes, campaign authority, confirm-family, inclusive probe accounting and fresh-holdout rules from the candidate contract; ordering, reachability and verdicts from evaluation order. | R23 abs |  |
| ADRX-139 | 2026-09-08 candidate L152 | Discharge the channel-liveness contract's five owed reconciliations and conditional first post-firing review through its owner. | R25 abs |  |
| ADRX-140 | Earlier removals L161-162 | Revive a tombstoned decision only through fresh pre-registration under the standing chain, never by lookup. | R3 abs |  |
| ADRX-141 | Earlier removals L157-159 | Retrieve pruned ADR bodies with git show pre-prune-2026-08-08 in the private archive; on the public clone use git log --follow. | R31 det | → docs/ltm/README.md |
| ADRX-142 | 2026-09-08 brief/skill L181-191 | Take skill source, deploy and gate rules from scripts/README Skill lifecycle; the reviewed-release policy alone authorizes no actual release. | R3 abs |  |

</details>

### Root docs (STATE, PIPELINES, REPO_MAP, README, load_bearing_numbers, mc_anchor_history) — 133 rules


<details><summary><code>PIPELINES.md</code> — 23 rules: 8 absorbed, 15 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-68 | §P1 L43 | Do not run Databento db_fetch estimate/pull/batch/download, even with retained scripts or keys; any new data source needs explicit operator GO. | R18 abs |  |
| ROOT-69 | §Current campaign handoff L31-33 | Treat synthetic E1 evidence and host readiness as not a qualified book; production feed, deployment GO and the arm remain owed beyond M1 RESOLVED. | R10 abs |  |
| ROOT-70 | §P1 L37-39 | Read the evaluation order before executing any contract frozen after 2026-08-30; owed channel migrations do not suspend it; campaign amendments need explicit owner decisions. | R24 abs |  |
| ROOT-71 | §P1 L44, §Data stores L126 | Bind every search with lab/discovery/register_search.py to a committed discovery_manifests/<run_id>.json; the commit is the pin. | R23 det | → .claude/skills/futures-anomaly-discovery/SKILL.md |
| ROOT-72 | §P1 L45 | Exploration yields observations and candidate evidence only; never promote automatically. | R25 abs |  |
| ROOT-73 | §P1 L46 | Evaluate under the evaluation order and survivor-scoring pre-registration, scoring with prop_survivor_scoring.py to a typed verdict. | R24 det |  |
| ROOT-74 | §P1 L47 | Admit only by an admitting decision with a calibrated decay monitor, then the strategy lifecycle, then venue/deployment gates. | R15 det |  |
| ROOT-75 | §P1 L51-53 | Use the ratified discovery-campaign defaults for temporal evidence and budget; W4 governs dormant SPA/StepM, PBO/CPCV and breadth producers. | R24 det | → docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md (+ W4 ADR 2026-08-07) |
| ROOT-76 | §Two standing constraints L57-58 | A wired harness does not prove its survivor path ran; read the campaign's RESULTS and skips first. | R0 abs |  |
| ROOT-77 | §Two standing constraints L59-60 | Run the K-budget reachability screen before any funded campaign. | R23 det |  |
| ROOT-78 | §Two standing constraints L60 | Read manifest status before counting K: open manifests do not bank K. | R23 det |  |
| ROOT-79 | §P2 L64-66 | Keep Pine/TV as research/export; a future Python-to-Pine crossing needs a fresh build and identity check against the then-current survivor format. | R14 det |  |
| ROOT-80 | §P3 L70-73 | Do not treat portfolio_mc.py --panel cme as a working MC rerun (breadth-only, legacy ingestion gate); use the campaign harness or prop_survivor_scoring.py. | R24 det |  |
| ROOT-81 | §P4 L77-79 | firm_rules.py, preflight.py and dd_geometry.py own firm rules and engine support; the campaign owns population, replay, composition policy and statistical design. | R16 det |  |
| ROOT-82 | §P4 L80-81 | Use ops/prop_envelope_default.md as the standing prop envelope; the live rail (P5) owns live quantities. | R16 det |  |
| ROOT-83 | §P4 L81-83 | Keep the four-firm program and its dated falsifier distinct from the bounded Select attempt. | R28 det |  |
| ROOT-84 | §P5 L89-90 | Keep Track B book modules (book_*, account_close_*) offline until a deployment GO. | R10 det |  |
| ROOT-85 | §P5 L90 | Keep nautilus_trader research-only. | R18 det |  |
| ROOT-86 | §P5 L98-100 | Qualification workflows (.github/workflows/qualification-*.yml) collect evidence for coordinator acceptance; none is a required merge check. | R38 det |  |
| ROOT-87 | §P6 L105-107 | M1 monitoring maturity is owned by the M1 acceptance JSON and its validator, not prose. | R10 abs |  |
| ROOT-88 | §Data stores L121 | Treat CME TV exports as private hash-pinned inputs and bind them per campaign. | R19 det |  |
| ROOT-89 | §Data stores L122 | core/data/bar_data/ is frozen and not regenerable; a catalog entry does not make private data or frozen bars regenerable. | R19 abs |  |
| ROOT-90 | §Data stores L131-132 | Historical figures keep their provenance; never let new data or venues silently inherit their claims. | R20 abs |  |

</details>

<details><summary><code>README.md</code> — 5 rules: 3 absorbed, 2 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-107 | §Source of truth L10-18 | Keep the five root documents to separate jobs (README routing, AGENTS instructions, PIPELINES workflow, STATE priorities, REPO_MAP architecture), at repo root not docs/. | R29 det | → docs/adr/2026-07-16-root-doc-charter-dedup.md §Decision |
| ROOT-108 | §Source of truth L20-22 | Campaign plans own executable next steps, campaign records own evidence and decisions; SESSIONS is historical narrative, not the current work list. | R29 abs |  |
| ROOT-109 | §Where to look L33 | Before opening research, check the lab catalog In flight section, then the brief index. | R8 abs |  |
| ROOT-110 | §Where to look L42-43 | 'In flight' means a question not spent or on HOLD; 'hot' means its body is on disk; neither denotes queue priority. | R8 det | → lab/CATALOG.md (header) |
| ROOT-111 | §Public-clone note L49-51 | Treat vendor data, Pine sources and executable ports of locked strategies as private hash-pinned inputs under AGENTS.md public-clone posture. | R13 abs |  |

</details>

<details><summary><code>REPO_MAP.md</code> — 16 rules: 4 absorbed, 12 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-91 | §Contract L10-16 | Obey the layer import contract: governance->core; lab and ops->core+governance; core imports no internal layer; lab<->ops forbidden. | R37 abs |  |
| ROOT-92 | §Contract L18 | Same-layer imports are legal and tests/ is exempt from the layer contract. | R37 det |  |
| ROOT-93 | §Contract L19-21 | Change a layer classification only by editing scripts/repo_map_layers.yml, the sole layer-map definition; REPO_MAP prose is not read. | R37 det |  |
| ROOT-94 | §Contract L23-24 | Source must parse on Python 3.11+; parse failures are reported separately from illegal edges. | R37 det |  |
| ROOT-95 | §2.2 L194-203 | Cross-layer import name collisions and unresolved first-party imports fail the scanner; dynamic imports and filesystem reads are outside it. | R37 det |  |
| ROOT-96 | §Mission-tier L28-29 | Mission tiers P0-P3 set review priority only, never deletion permission. | R31 det |  |
| ROOT-97 | §Mission-tier L29-31, §5 L229-231 | Apply the retention test to an artifact's actual consumers before removing it; passing boundary/layer checks never certifies a path may be deleted. | R31 abs |  |
| ROOT-98 | §2 L64 | Read the deploy/ listener and daemon READMEs before operational work on their Fly packaging. | R0 abs |  |
| ROOT-99 | §2 L64-65 | deploy/ statically imports only tools/ and tools/ imports only scripts/ discipline modules. | R37 det |  |
| ROOT-100 | §2 L71-73 | New Python under deploy/ or tools/ that statically imports ops/ or lab/ needs a different classification in the same change. | R37 det |  |
| ROOT-101 | §2 L69 | Keep .dockerignore as the root-context allow-list excluding private sources, vendor data, research and Git history from hosted images. | R13 det |  |
| ROOT-102 | §2 L68 | Default search excludes cold stores and private inputs; an empty search is not evidence that prior work or source bytes never existed. | R8 abs |  |
| ROOT-103 | §2.1 L81-83 | Keep the §2.1 scripts table generated: regenerate with check_repo_map_scripts_table.py --write; --check fails on drift. | R38 det |  |
| ROOT-104 | §2.2 L194-216 | Put the layer root on PYTHONPATH (';' Windows, ':' POSIX) for standalone layer-module commands, or use scripts/layer_bootstrap.py for direct scripts. | R22 det |  |
| ROOT-105 | §2.2 L217-218 | Skill wrappers launch subprocesses rather than importing lab code, preserving the governance->lab import prohibition. | R37 det |  |
| ROOT-106 | §2.2 L207 | Follow the rail runbook for c1_rail_arm and other flat listener tool commands. | R10 det | → docs/notes/rail_build/ARMING_PROCEDURE.md |

</details>

<details><summary><code>STATE.md</code> — 67 rules: 12 absorbed, 46 detail, 9 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-1 | header L5 | Start work by reading STATE's operator queue, then the linked executable plan; git status owns uncommitted work. | R8 abs |  |
| ROOT-2 | header L6-7 | Make routine STATE and governance updates without an ADR, per the ADR ceremony-tiering policy. | R32 abs |  |
| ROOT-3 | header L6 | Give each fact one canonical owner (Operational Rule 7); other documents link the owner or carry a labeled mirror. | R29 abs |  |
| ROOT-4 | Anti-accretion L9-10 | Write STATE index rows as consequence + owner link and forward rows as action + date/wake condition + owner; forward rows are pointers, owners hold criteria. | R34 abs |  |
| ROOT-5 | Anti-accretion L10-12 | Delete a closed STATE row once its owner holds the record; keep results, account figures, parameters and narrative with owners, not in STATE. | R34 abs |  |
| ROOT-6 | Anti-accretion L12-13 | Never roll an obligation away without its record; missing evidence is not completion. | R31 abs |  |
| ROOT-7 | §Operator queue L15-19 | Keep the operator queue strictly ordered with at most five live items; the cap is the concurrency Survive bound, not an hours budget. | R3 det |  |
| ROOT-8 | §Operator queue L17 | Treat operator-hours as binding; budget agent-hours through the K-ledger, cost dry-runs and the rail GO spend ceiling. | R2 det |  |
| ROOT-9 | §Operator queue L19-20 | Serve queue items in dependency order; independent work need not wait for a lower-numbered item. | R3 det |  |
| ROOT-10 | §Operator queue L20-21 | Queue new decision packets, advisor triage and sizing questions behind live queue items unless the operator directs otherwise. | R3 det |  |
| ROOT-11 | §Operator queue L21-23 | Do not auto-replace completed queue items; off-queue work stays with its owner until the operator promotes or directs it. | R3 det |  |
| ROOT-12 | §Source disposition L25 | No production feed is selected or funded and nothing arms; provider-neutral prep and no-spend Q&A may proceed; provider-specific work and spend wait for source-independent gates and operator funding. | R18 DEL⚖ | Track B source disposition; superseded for Tradeify by checklist Addendum 2026-10-16; AGENTS data-source/arming lines and self-funded ADR gates are stricter live owners. |
| ROOT-13 | §Source disposition L25 | Open CP-7 funding only after T00 GO-evidence, the bound equivalence spec and A9-PREP; its grant covers the provider adapter and emission-disabled shadow collection only. | R18 DEL⚖ | CP-7 feed funding (#790) frozen by checklist Addendum 2026-10-13, Track B superseded 2026-10-16; checklist §4 CP-7 keeps the record. |
| ROOT-14 | §Operator queue item 1 L29 | Tradeify evaluation strategy logic must be native: no external Python signals, bridges, CrossTrade/API or same-bot cross-firm use; Tradeify-specific build and spend stay frozen. | R10 abs |  |
| ROOT-15 | §Operator queue item 1 L29 | Do not reuse the attended-input adapter beyond X-1 run-1930 until its pin/path-safety review and the run-1930 import-set reconstruction are accepted. | R10 det | → docs/notes/2026-09-29-x1-decision-packet.md §8 |
| ROOT-16 | §Operator queue item 1 L29 | Obtain a CP-3 before each further route-commissioning row. | R10 DEL⚖ | X-3/X-4 commissioning rows not pursued per checklist Addendum 2026-10-16; branch (a) restart-under-CP-3 withdrawn; checklist §4 CP-3 retains the term. |
| ROOT-17 | §Operator queue item 1 L29 | Do not perform any legacy arm while #571 is parked. | R10 det | → docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md (Addendum 2026-10-01 six cuts, item 4) |
| ROOT-18 | §Operator queue item 1 L29 | Merge the D-S5-1/2 (#586) and D-S5-3 (#589) fixes before T05 integration acceptance (R1). | R6 DEL | Discharged: #586 (981eb125) and #589 (77cd715a) merged; STATE row records both accepted 2026-10-02. |
| ROOT-19 | §Operator queue item 1 L29 | Treat the continuation next steps as a derived mirror; staged acceptance governs where they differ, and bounded handoffs own assignments. | R29 abs |  |
| ROOT-20 | §Campaign owner L31 | Pass campaign ownership only by an execution-slices ledger handoff entry naming the successor; a coordinator ending without one returns the role to the operator. | R4 DEL⚖ | Protected Full E1 (Track B) superseded for Tradeify by checklist Addendum 2026-10-16; campaign record §58 keeps the rule; operator default is Rule 3. |
| ROOT-21 | §Campaign owner L31 | The operator retains ratifications, merges and operational GOs for the campaign. | R3 DEL⚖ | Track B campaign superseded 2026-10-16; merge retention conflicts with surface-allocation Addendum 2026-10-24b merge GO; ratification/GO retention is Rule 3. |
| ROOT-22 | §Decision index L35-36 | Keep only the newest 15 executed-decision consequences in STATE, newest first; rationale stays with owners and older rows move to the archive. | R34 det | → scripts/state_roll.py (KEEP_ROWS) |
| ROOT-23 | §Decision index L37 | Remove retracted verdicts from the decision index; their correction stays with the owner. | R34 abs |  |
| ROOT-24 | §Decision index 2026-10-15 L41 | Remove public-exposure content by deleting it and relying on git history, never by history rewrite; keep Striker day soft-stop values Pine-only. | R13 det | → docs/notes/2026-10-09-public-exposure-cleanup-packet.md §5–§6 |
| ROOT-25 | §Decision index 2026-10-14 L42 | Copy ports/effective inputs to the Windows VM only for runs the §60 VM addenda admit (now Q-SFCLEAR-3 FG and clearance runs). | R13 abs |  |
| ROOT-26 | §Decision index 2026-10-12 L46 | Dispatch implementation only with an approved card issued via the deployment coordinator. | R4 DEL⚖ | O1 R1/R2 work frozen by checklist Addendum 2026-10-13 and Track B superseded 2026-10-16; card-based dispatch is Rules 4 and 33. |
| ROOT-27 | §Decision index 2026-10-09 L48 | Self-funded lane: no capital authorization until a portfolio clears the maximum 15% peak-to-trough drawdown clearance standard. | R15 det | → docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md (grounds item 4) |
| ROOT-28 | §Decision index 2026-10-02 L49 | No agent runs a candidate-configurable replay against a pre-registered edition before that pre-registration is frozen. | R23 abs |  |
| ROOT-29 | §Decision index 2026-10-02 L49 | Incident notifier: correctly handled refusals do not notify; losing all channels while armed is an operator stop; retries continue until delivered. | R11 det | → docs/briefs/handoffs/2026-10-02-book-incident-notifier-build-card.md §5 |
| ROOT-30 | §Decision index 2026-09-27 L51 | Accept evidence proportional to the next step; unknowns block only what they affect (staged acceptance). | R36 det | → docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md (Addendum 2026-09-27) |
| ROOT-31 | §Decision index 2026-09-27 L51 | After an incident during commissioning or the first attended release, do not restart automation in the same session; review before another session. | R11 det | → docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md §A11.2 |
| ROOT-32 | §Decision index 2026-09-26/25 L52-54 | T08 drills and R-1/R-2 reads are operator-performed; each drill returns as an individual operator decision. | R10 DEL⚖ | T08 and route drills superseded for Tradeify by checklist Addendum 2026-10-16; incident ADR §A11.1 keeps the record; AGENTS operator-direction rule covers orders. |
| ROOT-33 | §Decision index 2026-09-25 L53 | Read the accepted book's Pine sources and runtime ports in place in the primary checkout only, under AGENTS.md private-read rules. | R13 abs |  |
| ROOT-34 | §Dormant threads L58-59 | Keep PARK threads with their pursuit records; list closure-registry backfill debt with check_closure_disposition.py --list-debt. | R28 det | → docs/pursuits/ (PARK records); scripts/check_closure_disposition.py --list-debt |
| ROOT-35 | §Weekly L67-70 | Place at least one account-preservation trade per Mon-Fri venue week, by the operator or an agent at operator direction for that trade; rail stays disarmed. | R10 det |  |
| ROOT-36 | §Weekly L70 | Count an X-3 or X-4 drill fill toward the preservation obligation in the week it fills. | R10 DEL⚖ | X-3/X-4 drills superseded for Tradeify (checklist Addendum 2026-10-16), so drill-fill counting is moot; drill plan §2.0 keeps the ruling. |
| ROOT-37 | §Weekly L71,L89-90 | Record weekly coverage only when attested (operator-attested unless browser-verified) and preserve missed-week records when advancing; daily-repo-truth-sync reads these dated obligations. | R21 det |  |
| ROOT-38 | §Monthly L94-96 | On the 21st, recheck subscription ledger rows d11-d18 and record the operator's confirmation even if unchanged; resolve Fly.io/Tradeify unknowns when evidence appears. | R34 det | → docs/pursuits/SUBSCRIPTION_LEDGER.md (owner ADR 2026-08-21) |
| ROOT-39 | §No fixed date L102 | Self-funded lane: the ADR's seven owed items gate the first live order; API access and CME licensing also gate any feed activation. | R10 det | → docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md (grounds) |
| ROOT-40 | §No fixed date L102 | Run Q-SFCLEAR-3 in order: card B amendment (c) and card E before FG, then the private FG run, then the clearance run; live readiness gates live use only. | R23 det | → docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md (§S row 9) |
| ROOT-41 | §No fixed date L102 | Do not upload the Q-SFCLEAR-1 F6 evidence to the fact-finding folder without Joshua's scoped authorization. | R13 det |  |
| ROOT-42 | §Held-request watch L103 | While any request is held, check at each account-session open (18:00 ET Sun-Thu), paged at due + 60 min by the G1 dead-man once built. | R11 det | → docs/notes/2026-10-02-t13-a12-f3-held-request-watch-draft.md |
| ROOT-43 | §Held-request watch L103 | Before the first armed session, treat the G1 build, G10 (paging re-proved), Q7 PASS and HB-L1/L2 as arming preconditions. | R10 det | → docs/notes/2026-10-02-t13-a12-f3-held-request-watch-draft.md |
| ROOT-44 | §No fixed date L104-106 | Wire the M-B idle-clock monitor only on F3 successor registration, after re-freezing venue semantics. | R11 det | → docs/briefs/closures/Q-MONSURF-1-closure-resolved.md |
| ROOT-45 | §No fixed date L107-108 | Capture M-C per-fill add slippage at the first strategy-signal add fill. | R11 det | → docs/briefs/closures/Q-COSTGEO-3-closure-ambiguous-needs-depth.md |
| ROOT-46 | §No fixed date L109-110 | Keep M-C ECR live-edge capture (b6) parked until a NAS100/MNQ-shaped leg's first live fill on the incumbent eval or an F3 successor. | R28 det | → docs/pursuits/b6-q-nas-ecr-1.md |
| ROOT-47 | §No fixed date L113-115 | Keep the rolling-PF sigma source and lifecycle state writer fill/data-gated; synthetic tooling is not live evidence. | R15 det | → docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md §7 |
| ROOT-48 | §No fixed date L116-117 | Keep the ORB decay re-scope obligation open until deployed-book data exists. | R15 det | → docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md §6 |
| ROOT-49 | §No fixed date L118-119 | Promote Sentinel Tier-2/3 (limb B1) before the next quarterly slate as a promotion, not a new build. | R33 det | → docs/spec/2026-06-23-inqhiori-sentinel-design.md |
| ROOT-50 | §No fixed date L120-121 | PREREG-C1-DEDUPE-1 has GO, but it does not apply to the REST book route as written. | R3 det | → docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md (D-B13) |
| ROOT-51 | §No fixed date L122-123 | Do not perform CFD data-estate class-wide deletion until T1/F3 FUTURES_LOCK and substrate Phase-6 confirmation. | R31 det | → docs/adr/2026-07-11-ops-cfd-estate-retirement.md |
| ROOT-52 | §No fixed date L124-125 | Run the mechanism-sourcing radar on demand; checkpoint progress/idle on 2026-11-08. | R25 det | → docs/methodology/strategy_harvest.md |
| ROOT-53 | §No fixed date L126-128 | Complete the owed reversed-evidence propagation sweep: pursuit fixes, skills and strategy-card mirrors. | R30 det | → docs/notes/audits/2026-08-31-pursuits-personas-reversed-evidence-audit.md |
| ROOT-54 | §No fixed date L129-133 | Hold MNQFLOW-1-DEPTH (operator value-of-spend hold, data-blocked); revisit only at operator initiative, an approved depth source, or 2026-11-08. | R3 det | → lab/analysis/c1/mnq_orb_flow_depth_2026-08-18/PREREG_S2B.md |
| ROOT-55 | §2026-11-08 L137-139 | On 2026-11-08 review the queue cap (two-consecutive-quarter condition) and repeated out-of-order serving. | R3 det | → docs/adr/2026-07-16-root-doc-charter-dedup.md §Queue-attention review |
| ROOT-56 | §2026-11-08 L140-141 | Re-read GRAND-tier ADR §4 on 2026-11-08. | R28 det | → docs/adr/2026-08-09-grand-tier-quintessentials-binding.md §4 |
| ROOT-57 | §2026-11-08 L142-143 | Convert PARK pursuits (b1, b3, b6 on 2026-11-08; b5 on 2027-02-08) to SUBTRACT absent explicit renewal. | R28 det | → docs/pursuits/ (b1, b3, b5, b6 records) |
| ROOT-58 | §2026-11-08 L144-148 | Absent a qualifying intraday-honest clearance by 2026-11-08, demote the four-firm program to research-only; discharge needs its own dated re-MC; a next candidate needs fresh operator authorization. | R28 det | → docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md (+ 2026-07-22 discharge-withdrawal ADR) |
| ROOT-59 | §2026-11-08 L149-151 | Check mechanism-boundary clauses 2-A and 2-C on 2026-11-08. | R28 det | → docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md |
| ROOT-60 | §2026-11-08 L152-153 | Run sourcing-channel retirement §4 limb-2 starvation checks (2026-11-08, 2027-02-08) and limb-3 early-closure evidence re-examination (2027-02-08). | R28 det | → docs/adr/2026-08-24-sourcing-phase-channel-retirement.md §4 |
| ROOT-61 | §2026-11-08 L154-155 | Check the harvest-intake §4 doctrine falsifier and idle guard on 2026-11-08 from owner counts and evidence, not a root summary. | R28 det | → docs/adr/2026-07-15-external-mechanism-harvest-intake.md §4 |
| ROOT-62 | §2026-11-08 L156-157 | If no live fill exists by 2026-11-08, re-raise the regime-monitor successor's standing-unfalsifiable gap at the audit. | R28 det | → docs/adr/2026-06-07-decompound-remc-hold.md |
| ROOT-63 | §2026-11-08 L158-159 | On 2026-11-08 check the blind channel's sourced-vs-empty status, pre-G0 count, N firing and any analogue-manifest re-test. | R28 det | → docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md |
| ROOT-64 | §2026-11-08 L160-161 | Run the regime-candidate flag lane two-strikes check against new confirm closures on 2026-11-08. | R28 det | → docs/adr/2026-07-26-regime-candidate-flag-lane.md |
| ROOT-65 | §2026-11-08 L162-165 | Hold the initial candidate-contract and channel review (incl. fired-ceiling checks); five artifact adoptions and five liveness reconciliations are owed at channel owners. | R25 det | → docs/adr/2026-08-30-candidate-contract.md (§First review) |
| ROOT-66 | §2026-11-08 L166-170 | Hold the evaluation and rejection review on 2026-11-08, and immediately on any cost-authority or scope change. | R24 det | → docs/adr/2026-08-30-evaluation-order.md (§First review) |
| ROOT-67 | §2026-12-31 L174-175 | Reverify the 90-day prop-envelope venue facts for the four friendly firms only; the other four rows stay stale and unused. | R17 det | → ops/prop_envelope_default.md §4 |

</details>

<details><summary><code>docs/README.md</code> — 1 rules: 0 absorbed, 1 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-112 | table L20-21 | Treat docs/external notes as not a harvest intake and retained historical prose as not live doctrine. | R25 det |  |

</details>

<details><summary><code>docs/load_bearing_numbers.md</code> — 15 rules: 3 absorbed, 12 detail, 0 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-121 | header L3 | Read docs/load_bearing_numbers.md before quoting any prop-tier figure. | R20 abs |  |
| ROOT-122 | header L5, §3 L66 | Only the named owner may move a load-bearing number; the other value found in the tree is historical. | R29 abs |  |
| ROOT-123 | §1 L16-21 | Treat an eval bust figure as an EOD-clock lower bound unless it cites an intraday-honest RESULTS path; scope is all seven trailing-DD tiers. | R20 det |  |
| ROOT-124 | §1 L30-32 | Read the R1 7-tier RESULTS §2/§4b before concluding about remaining tiers; a since-corrected archived figure is not 'no figure'. | R20 det |  |
| ROOT-125 | §2 L36-38 | Read every published prop-tier bust/pass figure as assuming the inactivity barrier OFF unless its own file says otherwise. | R20 det |  |
| ROOT-126 | §2 L53-54 | Do not reopen the degenerate barrier-ON re-MC as a fresh finding. | R20 det |  |
| ROOT-127 | §2 L56-62 | Treat barrier-ON rates as unsafe in either direction without a full-calendar input (the engine's rolling idle counter over- or under-fires). | R20 det |  |
| ROOT-128 | §3 L66-68 | Never apply a transformation to a figure in the two-values table. | R20 abs |  |
| ROOT-129 | §3 L72 | Take the live Part A eval bust ceiling from prereg v2 §3 (prop_survivor_scoring.DEFAULT_PREREG); the v1 value is closed, valid only in v1-keyed studies; distinguish max_dd_pct. | R20 det |  |
| ROOT-130 | §3 L73 | Take the pass floor, funded ceiling and trailing_locking requirement from prereg v2 §3 (unchanged from v1). | R20 det |  |
| ROOT-131 | §3 L74 | The four-firm §4 set is Bulenox, Tradeify, MFFU and BluSky per the F1 reversal; the three-firm reading is historical. | R20 det |  |
| ROOT-132 | §3 L75 | The venue inactivity rule is at least one trade per Mon-Fri week per account, eval and funded; the engine's idle-day counter is a conservative bound, not the rule. | R20 det |  |
| ROOT-133 | §3 L76 | Q-RANGECOND-1 is FALSIFIED; never quote the retracted RESOLVED closure figures. | R20 det |  |
| ROOT-134 | §3 L77 | Take the ORB-MYM headline from the canonical engine, not TradingView; TV net/PF/maxDD are leg-level under pyramiding without firm DD geometry. | R20 det |  |
| ROOT-135 | §Adding a row L81-83 | Add a row only when a number has two values readable in the tree and the wrong one would be acted on. | R20 det |  |

</details>

<details><summary><code>docs/mc_anchor_history.md</code> — 6 rules: 2 absorbed, 3 detail, 1 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-231 | banner L3-5 | Never quote the historical MC calibration triple as a live pass-probability or executable gate; it is historical record only. | R20 abs |  |
| ROOT-232 | banner L3 | Run MC engine regression on the vendor-free synthetic test; the Pepperstone executable anchor pin is retired. | R14 det |  |
| ROOT-233 | 2026-07-06 correction L17 | Do not retro-edit pre-2026-07-06 published p99 DD figures. | R30 det |  |
| ROOT-234 | 2026-07-06 correction L17 | Footnote the bust-day max_dd inclusion correction in any cross-semantic p99 DD comparison. | R20 det |  |
| ROOT-235 | Q-SWAP L9 | Model additive cost shocks with fixed-1R, not implied-1R normalization; lock-decision MC is not the instrument for live additive-cost shocks. | R33 abs |  |
| ROOT-236 | Q-SWAP-4 L9 | Opportunistically re-test the Q-SWAP-4 structural follow-up at the next allocation-refresh ADR. | R14 DEL⚖ | Q-SWAP domain retired on SNAG exhaustion (mc_anchor_history §Q-SWAP); legacy book has no live venue (AGENTS); no allocation-refresh ADR is expected. |

</details>

### Rejected-candidates register (re-proposal bars) — 95 rules


<details><summary><code>docs/rejected_candidates.md</code> — 95 rules: 3 absorbed, 88 detail, 4 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| ROOT-136 | header L3 | Re-propose a registry entry only with new mechanism evidence, never new parameters or a wider sweep. | R26 abs |  |
| ROOT-137 | header L5 | Append an entry linking the authoritative closure whenever a Pre-Q closes FALSIFIED on strategy grounds or a parent programme closes on SNAG exhaustion. | R26 det |  |
| ROOT-138 | header L7 | Admit any candidate only with a mechanism-level claim carrying falsifiable specifics, not 'try a wider grid'. | R25 det |  |
| ROOT-139 | header L9 | Challenge-era claim re-scope is not new mechanism evidence and reopens no registry entry. | R26 det |  |
| ROOT-140 | entries form; §Queryable index L1306-1315 | Write entries with scope, closure date, authoritative artifact, basis, surviving finding and re-proposal bar; new structured records must carry role_tested and falsifier_failed. | R26 det |  |
| ROOT-141 | buyback-blackout×MNQ L26 | A Phase C sleeve must name a daily partner mechanism. | R24 det |  |
| ROOT-142 | buyback-blackout×MNQ L29-30 | Re-propose buyback-blackout abstention on MNQ only with a materially different magnitude argument than F5's failures; no cadence re-litigation, sleeve-only card or retune. | R26 det |  |
| ROOT-143 | TOM×SPX500 L50-51 | Re-propose turn-of-month premium on SPX500 only with new mechanism evidence; not a wider window, new thresholds or a Dukascopy re-run. | R26 det |  |
| ROOT-144 | MSL-S2B×MYM L70-71 | Re-propose MSL-S2B continuation only via new modality, Board un-pause with a non-route-1 thesis, or different loss shape; composite clearance and silent C1-entry reopen are forbidden. | R26 det |  |
| ROOT-145 | MSL-S2A×MCL L89-90 | Re-propose pullback-failure resumption on MCL only with new mechanism evidence (reference class/direction/TF), not I/P-window, stop-buffer or rr retunes. | R26 det |  |
| ROOT-146 | MSL-C1×MYM L107 | Re-propose PDH/PDL failed-break reclaim on MYM only with new mechanism evidence, not stop-buffer, overnight-sham or window retunes. | R26 det |  |
| ROOT-147 | MSL-C3×M2K L121-126 | Revive the MSL-C3 M2K path only via a fresh Stage-1 plus new B4 GO, and further M2K addback of this class needs new mechanism evidence. | R26 det |  |
| ROOT-148 | MSL-C3-K2×M2K L143 | Re-propose dual-axis MR-at-level on M2K only with new mechanism evidence, not theta/stop-buffer retunes or a silent K=1 drop. | R26 det |  |
| ROOT-149 | MSL-C2×MGC L162-163 | Re-propose London-range failed-extension fade on MGC only with new mechanism evidence, not stop-buffer, rr or London-window retunes. | R26 det |  |
| ROOT-150 | Q-TXG-1 lane L188-190 | Reopen the transfer/expression lane only with a different loss-side shape or a venue class with different survival geometry; further Q-TXG-1 transfer elections are barred. | R26 det |  |
| ROOT-151 | Striker NAS100→MYM L204 | Striker NAS100->MYM cell is subsumed by the Q-TXG-1 lane bar; no locked-parameter retune, required_net_r amendment, firm-shopping or silent third election. | R26 det |  |
| ROOT-152 | Striker DJ30→MNQ L220 | Striker DJ30->MNQ cell is subsumed by the Q-TXG-1 lane bar; no locked-parameter retune, survival-floor amendment, invented ENV-1 panel N or silent third election. | R26 det |  |
| ROOT-153 | Guardian→MGC L239-241 | Re-propose the Guardian->MGC transfer only with a fresh cell prereg and operator election; no locked-parameter retune, AE-score re-read or survival-floor amendment. | R26 det |  |
| ROOT-154 | Guardian XAGUSD L251-264 | Re-propose Guardian-family on XAGUSD only with new mechanism evidence; new parameters, wider sweep, longer panel or a correlation-gate change do not clear; the override did not readmit it. | R26 det |  |
| ROOT-155 | Guardian XAGUSD L250 | Instrument-level correlation is not a reliable proxy for strategy-level correlation in portfolio construction. | R24 det |  |
| ROOT-156 | Custodian EURUSD L276 | Re-propose custodian month-end flow on EURUSD only via a completed mechanism probe or new mechanism evidence, not Pine tweaks, another fix-window or wider sweep. | R26 det |  |
| ROOT-157 | USOIL spike-fader L287 | Re-propose USOIL spike-fade entry only with a genuinely new entry mechanism class, not retunes, subset/regime slices or stop-geometry tweaks. | R26 det |  |
| ROOT-158 | USOIL spike-fader L287 | Role asymmetry: an entry-rejected signal may still be probed as an exit or filter without clearing the entry rejection. | R26 det |  |
| ROOT-159 | FX fixing EURUSD L308 | Re-propose the EURUSD fix fade only with materially better-than-retail execution evidence or a different mechanism, not grid retunes, another fix or wider panel. | R26 det |  |
| ROOT-160 | Aegis EURGBP L327 | Re-propose the Aegis MR port on EURGBP only with a measured spread/ATR geometry from realized stops clearing the cost hurdle on the canonical feed. | R26 det |  |
| ROOT-161 | Gold regime-gate L348 | Re-propose a gold KER/TSMOM deploy-vs-wait gate only with new mechanism evidence surviving OOS; never refit its frozen constants or extend shadow logging. | R26 det |  |
| ROOT-162 | Other directions L350-361 | Formalize each pending direction as a full entry at its authoritative closure, removing its bullet; the pending list only shrinks and promoted entries never reappear. | R26 DEL⚖ | All six pending bullets are CFD-era or options directions; CFD estate retired (ADR 2026-07-11 ops-cfd-estate-retirement), so their formalizing closures cannot occur. |
| ROOT-163 | Aegis→6J Wave-1 L396-402 | Re-propose Aegis->6J sizing sweep only via a fresh prereg pre-declaring window/N-bar before cells run or a longer 6J export; no in-place amendment, best-cell pick or retunes. | R26 det |  |
| ROOT-164 | Aegis→6J H-SOLO L440-447 | Re-propose native Aegis-6J only with a different trailing-DD loss shape or venue geometry; no c05 reweight, other Wave-1 cell, MYM+MNQ dilution or soft-pass re-read. | R26 det |  |
| ROOT-165 | S-MYM-ORC-02 L484-489 | Re-propose MYM opening-range continuation only as a distinct construct under fresh ID and signed prereg; no stop/target/add retune, lower-cost model, placebo-anchor rescue or date deletion. | R26 det |  |
| ROOT-166 | H-FBEIA-1×CL L573 | Re-propose EIA post-release reversal on CL only with a genuine inventory-surprise-conditioned expression clearing cost-law and power; no window/hold retune or unconditional re-run. | R26 det |  |
| ROOT-167 | F-C carry×6E/6J/CL L597-601 | Re-propose carry timing only as a cross-sectional or magnitude-weighted rule with its own prereg and K; no retune, re-run or wider grid of own-carry-sign. | R26 det |  |
| ROOT-168 | H-ZNAUC-1×ZN L641-645 | Re-propose ZN auction drift only with a different construct (lower measured cost or non-drift mechanism); no window retune, cross-instrument transplant or bid-to-cover read as tradeable delta. | R26 det |  |
| ROOT-169 | H-ZNAUC-1 L644; MOC×MYM L1532; Q-INVENTORY-1 L934 | Never transplant a delta across instruments or invent one; a candidate lacking its own measured delta stays unscreenable (harvest Requirement 2). | R25 det | → docs/methodology/strategy_harvest.md (Requirement 2) |
| ROOT-170 | Q-INVENTORY-1 L934-936; many entries | A seed's delta must clear the 4x round-trip cost-law hurdle at the panel basis (harvest Requirement 5). | R25 DEL | Superseded: strategy_harvest Requirement 5 (4x cost law) deleted 2026-10-24 by operator ruling (assumption-challenge §2.1); closure bases stay as lineage. |
| ROOT-171 | MSL-S2B D2×MYM L775-778 | Re-propose sweep-failure continuation only as a different entry-trigger operationalization through its own D2-class falsifier; no re-run of the C1-flip/40-120 box or base-verdict reopen. | R26 det |  |
| ROOT-172 | Third-Friday×MYM L789 | Re-propose third-Friday settlement reversal only with new target-instrument mechanism evidence; no timing/exit/expiry-subset retune, MNQ rescue, overnight limb or pooled index. | R26 det |  |
| ROOT-173 | Opening-volume×MNQ/MYM L800 | Re-propose the opening-volume pressure map only with new modality evidence; no RV threshold, opening window, weekday slice, post-hoc instrument pick or panel re-pin. | R26 det |  |
| ROOT-174 | OR-window aggressor×MNQ L826-828 | Re-propose OR-window aggressor-size work only with fresh Cap-reservation and Cap-spend GOs and a new G0 on a different feature or question; no floor, window or event-set re-score. | R26 det |  |
| ROOT-175 | Q-COMPOSE-1 L870-877 | Re-propose a breadth leg only if risk N_eff also rises (not variance-dominant); a failed composed candidate closes rather than iterating weight; no combined composed×haircut arm. | R26 det |  |
| ROOT-176 | Q-COMPOSE-1 L867-869 | Before composing a leg into a book, check risk N_eff (PR of covariance), not just dependence N_eff (PR of correlation). | R24 det |  |
| ROOT-177 | Blind high-K mining L918-925 | Re-propose discovery mining only on a low-K (<=441) pre-committed mechanism-first axis or with anchor-moving external evidence; never amend frozen survivor ceilings or DSR K/V rules in response. | R23 det |  |
| ROOT-178 | Q-INVENTORY-1 L936 | Re-propose harvest-burst classes only with a fresh published cohort delta clearing Req-5 or a funded probe of a named stub; no re-citation, invented delta, relaxed OOS start or added channel. | R26 det |  |
| ROOT-179 | Q-INVENTORY-1 L934-936 | The GC/MGC family bank is a permanent K-wall; never re-cite a dead harvest class under a different paper (Requirement 3 dedup-first). | R23 DEL⚖ | 'Permanent K-wall' superseded: ADR 2026-08-04 made the family K-bank disclosure-only (strategy_harvest Req 3); no-re-citation bar survives in ROOT-178. |
| ROOT-180 | TAS×MCL L966-971 | Re-propose MCL settlement-window flow only with a published post-hoc-free cohort delta clearing the 4x hurdle at a venue-legal outright; no re-read, retune, spread re-frame or Wall-A route. | R26 det |  |
| ROOT-181 | MNQDTL-CON-1 L1001-1003 | Re-propose the ES-NQ divergence contrarian only as a new entry mechanism; no G/lookback/theta retune, and sign inversion is forbidden. | R26 det |  |
| ROOT-182 | Q-MNQSEL-1 L1034-1036 | Re-propose MNQ oracle selection only with a different causal candidate set; no denser order-flow on the same clocks, no look-ahead completed-window ranking, no 'close enough' read. | R26 det |  |
| ROOT-183 | Striker pyramid scaling×MYM L1077-1081 | Re-propose risk%-input haircut scaling only with evidence the MYM qty ceiling does not bind at the deployed tier; no same-size re-run, Pine retune or tolerance-band change. | R26 det |  |
| ROOT-184 | R2FLOW×MNQ L1111-1113 | Re-propose clock-minute aggressor flow only as a genuinely different order-flow construct, not a grid, horizon or catalogue retune. | R26 det |  |
| ROOT-185 | Q-R2VBUCK-1×MNQ L1145-1146 | Re-propose volume-bucket imbalance only with a new G0/causal object, not a bucket-size, horizon or catalogue retune. | R26 det |  |
| ROOT-186 | TV bar-coverage hypothesis L1189-1192 | Re-propose the TV coverage-artifact hypothesis only with new bar-availability evidence (feed class, roll protocol, newly served day), not a .c.0 re-census. | R26 det |  |
| ROOT-187 | TV bar-coverage hypothesis L1183; HTML L1196 | Carry the 2020-03-16 missing-TV-day annotation wherever 2020-Q1 Striker-MYM behavior is analyzed. | R19 det |  |
| ROOT-188 | TV bar-coverage hypothesis L1186-1188 | Use BAR EXPORT v0.2 as the default TV-side leg for coverage/parity questions, pinned against volume-rolled .v.0 (not .c.0) series. | R18 det |  |
| ROOT-189 | SLR-MYM-1 L1263-1267 | Re-propose sweep-and-reclaim on MYM only with a constraint claim passing delete/flip tests (or funded Path-1b) and an unoccupied symbol or session-disjointness surviving F1. | R26 det |  |
| ROOT-190 | SLR-MYM-1 L1259-1261 | Any future same-account MYM leg must respect order-symbol occupancy: the venue nets one position per symbol per account on shared MYM1!. | R17 det | → ops/instruments/MYM.md (F1) |
| ROOT-191 | §Queryable index L1279-1286 | Do not delete or move rejected_candidates.md; profiles.json source pointers into it are consumed by instrument_profiles.py, which fails on a missing source. | R31 det |  |
| ROOT-192 | §Queryable index L1285-1288 | Reason about the registry's tiers separately: the domain-bar tier is machine-consulted and blocking; the per-direction tier has no enforcement instrument. | R26 det |  |
| ROOT-193 | §Queryable index L1289-1293 | Run an executed dedup attestation by mechanism family (including rg --no-ignore over LTM) and paste its output; an attestation not run is not an attestation. | R8 abs |  |
| ROOT-194 | §Queryable index L1320-1321 | Additions only: never edit or delete a prior rejection entry; the registry lineage must stay intact. | R26 det |  |
| ROOT-195 | §Queryable index L1317-1320 | Treat the four locked-book strategies as dedup targets pinned in the concept-intake gate's admissibility_contract.yaml locked_book block. | R8 DEL⚖ | Concept-intake gate and admissibility_contract.yaml retired by ADR 2026-07-11 gen1-pipeline-retirement (validation/ absent); locked book is in core/strategies/CATALOG.md. |
| ROOT-196 | GEX gate×NAS100 L1333 | Re-propose a dealer-gamma ORB gate only via a fresh single-cut prereg on paid NDX-native gamma with orthogonal separation or another exogenous flow series; no sweep or sign-flip. | R26 det |  |
| ROOT-197 | GEX gate×NAS100 L1332 | An exogenous ORB regime signal must also be orthogonal to \|gap\| and OR-range; exogeneity is necessary, not sufficient. | R24 det |  |
| ROOT-198 | T10Y3M gate×NAS100 L1346 | Re-propose a term-spread ORB gate only with a flow series both vol- and era-orthogonal; no sign-flip, construction sweep or best-of-K over macro series. | R26 det |  |
| ROOT-199 | T10Y3M gate×NAS100 L1345 | A macro-regime gate must also be era-orthogonal (hold within year); the orthogonality battery includes a frozen year fixed-effects gate. | R24 det |  |
| ROOT-200 | Friday gate×NAS100 L1359 | Re-propose a Friday/end-of-week ORB effect only with forward or independent OOS evidence surviving wide-family multiplicity with a pre-specified mechanism. | R26 det |  |
| ROOT-201 | Friday gate×NAS100 L1358 | Apply best-of-K over the whole eyeballed family as a separate, prior gate for any hand-picked bucket before orthogonality or era gates. | R23 det |  |
| ROOT-202 | Rates MR Micro10Y L1371 | Re-propose rates intraday MR only as a chop-specific vol- and era-orthogonal edge whose worst drawdown avoids the H1 trend window; no retune, tenor swap or longer panel. | R26 det |  |
| ROOT-203 | Index dispersion×SPX500 L1383 | Re-propose dispersion/correlation premium only with an options-capable venue or listed DSPX derivative plus a non-co-occurring tail; no options re-spec, other index or OTC construct. | R26 det |  |
| ROOT-204 | Index dispersion×SPX500 L1382 | The vol/correlation-risk-premium branch (short-vol, dispersion, gamma-scalp, IV-calendar) is venue-blocked on options-free futures-prop venues. | R17 det |  |
| ROOT-205 | ORB×ZB L1396 | Re-propose a ZB construct only with new mechanism evidence; no anchor retune or breakout sweep; a ZB fade is a distinct mechanism needing its own intake. | R26 det |  |
| ROOT-206 | ORB×ZB L1397 | A Treasury-futures construct for the c1 account must clear venue availability first (Treasuries untradable at the registered firm): re-express on EUREX bonds or name another firm. | R16 det |  |
| ROOT-207 | Short-NG EIA L1410 | Re-propose the NG EIA bracket premium only with new mechanism evidence for a different NG construct, not a bracket-window retune or re-read of the paper. | R26 det |  |
| ROOT-208 | ZF conditional ORB L1423 | Re-propose Treasury conditional breakout only as a new rates mechanism, not an event-set, OR-window or instrument retune; widening N is a fresh manifest. | R26 det |  |
| ROOT-209 | ZF conditional ORB L1423 | Do not fund a fourth directional drift/breakout construct on the Treasury complex at this analysis level without reformulating the parent question. | R28 det |  |
| ROOT-210 | Cross-index RV ranking L1436 | Re-propose cross-index RV ranking only via a scoped ES+RTY intraday pull showing dispersion and better ORB edge; no RV/ORB/2-index retune; ES alone is inadmissible. | R26 det |  |
| ROOT-211 | LETF EOD rebalance L1508 | Re-propose LETF EOD rebalance flow only with paid NDX-native orthogonal non-decayed evidence, a new venue class, or a dated live incident; no free-data re-run. | R26 det |  |
| ROOT-212 | MOC imbalance×MYM L1536-1540 | Re-propose MOC-imbalance on MYM only with a procurement-free published cohort delta, an Avenue-A §6 survivor tie, or a dated incident; no re-framing, other index or four-clause card. | R26 det |  |
| ROOT-213 | MOC imbalance×MYM L1529-1531; EOD-adversity bar L1686 | Do not buy explanatory data before a survivor justifies it; paid-data discovery needs a survivor tie meeting Avenue-A §6's qualifying triple. | R18 det |  |
| ROOT-214 | ORB-MNQ-1 deployment target L1581-1588 | Re-target ORB-MNQ-1 at Tradeify only after a documented DD-geometry change plus fresh GO; elsewhere needs GO, prereg and survivor-scoring pass before unparking; no k re-pick or gates. | R26 det |  |
| ROOT-215 | ORB-MNQ-1 deployment target L1547-1551 | File a deployment-target rejection without a concept-intake-entry comment or queryable-index line, so dedup does not reject the mechanism family. | R26 det |  |
| ROOT-216 | ORB-MNQ-1 L1587; EOD-adversity L1703-1705 | Do not adopt the 15:30 ET exit for ORB-MNQ (ADR 2026-07-31 §5, reaffirmed 2026-08-02). | R26 det | → docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md §5 |
| ROOT-217 | §Domain-level SNAG closures L1592-1597 | Re-proposal of anything in a SNAG-closed domain must clear the domain bar, not merely the per-candidate bar. | R26 det |  |
| ROOT-218 | 5th-leg free-data SNAG L1622-1636 | Admit no free-data 5th-leg/expansion candidate to full Pre-Q without paid/exogenous vol- and era-orthogonal evidence, a wall-relaxing new venue class, or a dated live incident. | R26 det |  |
| ROOT-219 | 5th-leg free-data SNAG L1649-1651 | Read the 5th-leg domain bar as binding forward from its 2026-08-09 ratification only, never as having gated earlier work. | R26 det |  |
| ROOT-220 | §Tail-exhaustion raised bars L1657-1662 | A raised bar governs new candidates only, preserving the survivor and untested threads; it escalates to SNAG only at ~17-22 closures with the survivor retired. | R26 det |  |
| ROOT-221 | Index-futures OHLCV timing bar L1669-1687 | Admit no new single-index OHLCV intraday timing candidate to full Pre-Q unless outside the mapped levers, a different modality/venue, or beating ORB-MNQ net-of-cost. | R26 det |  |
| ROOT-222 | Index-futures OHLCV timing bar L1672-1680 | Within-instrument temporal selectivity may use route 1 only if its criterion is causally named a priori and frozen at G0, every axis charges K_intrinsic, and gates stay unchanged. | R23 det | → docs/adr/2026-08-10-temporal-selectivity-outside-mapped-levers.md §2-A |
| ROOT-223 | EOD-adversity bar L1725-1736 | Admit no new late-session adversity explanation to full Pre-Q unless direct order-flow modality, pre-registered multiplicity survival on a fresh panel, or ~1,200+ usable days per subgroup. | R26 det |  |
| ROOT-224 | EOD-adversity bar L1721-1723 | Do not re-quote Q-SESSCONF-1's z = -2.90 exposure control; the direct per-day test supersedes it. | R20 det |  |
| ROOT-225 | COT/TFF L1780-1785 | Re-propose positioning-extreme reversal only with a higher-frequency hedger-sentiment crowding proxy and right-skewed payoff; no threshold retune, instrument swap or wider COT window. | R26 det |  |
| ROOT-226 | MOC wake×MES L1809-1812 | Re-propose the MES closing-imbalance fade only with credible large positive net expectancy plus a complete frozen signal/entry/stop/exit/sizing expression. | R26 det |  |
| ROOT-227 | MOC wake×MES L1804-1806 | Reserve Vet intake for candidates with a confidently high positive-expectancy prior and a complete expression; source-liveness work without a decision-changing consumer stops. | R25 det |  |
| ROOT-228 | London-fix wake×6E/6B L1826 | Re-propose the London-fix wake only with orthogonality (\|t\|>=2, correct sign) and placebo-60th clearance on an untested panel; no menu/clock retunes or post-hoc subsets. | R26 det |  |
| ROOT-229 | §Audit hooks L1844-1846 | Every rejected direction must name an authoritative closure artifact (audit hook: grep 'Authoritative artifact'). | R26 det |  |
| ROOT-230 | §Harness-fed L1869-1872 | Do not append to the harness-fed section; route per-direction instrument-scoped rejections to ops/instruments/<SYM>.md; this file owns domain-level and cross-instrument bars. | R26 abs |  |

</details>

### Lesson registries — 178 rules


<details><summary><code>docs/methodology/lessons/execution_lessons.md</code> — 21 rules: 8 absorbed, 3 detail, 10 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| LESSONS-E-1 | Header L3 | Treat execution_lessons.md as the single canonical registry for E-class (execution) behavioral lessons; cite it, not skill copies. | R29 abs |  |
| LESSONS-E-2 | Header L4-9 | Anchor every execution lesson to a dated incident, a dollar cost or counterfactual gain, an imperative rule statement, and a named Step-6 watch-point. | R33 det | → .claude/skills/brief-authoring/references/lesson_capture.md |
| LESSONS-E-3 | Promotion criteria L11-14 | Promote a candidate execution lesson only on a single incident costing over $3K or the same pattern firing across three separate review windows. | R33 det | → .claude/skills/brief-authoring/references/lesson_capture.md |
| LESSONS-E-4 | Demotion criteria L16-19 | Demote a promoted lesson only after 12+ months without its watch-point firing and once the structural condition producing it no longer exists. | R33 DEL⚖ | Inoperative: 2026-08-14 freeze bars the 12-month clock; only E1/E2 promoted, feeder journal_review.py absent. Operator chose MARK-DORMANT over delete (2026-08-08 audit item 6). |
| LESSONS-E-5 | Freeze notice L21-25 | Treat E1-E4 promotion and demotion as frozen; do not promote or auto-demote them on firings or the 12-month clock, since the watch-point feeder is retired. | R28 det |  |
| LESSONS-E-6 | E1 Rule L43-46 | Never skip a valid system signal on a macro-volatility forecast; the filter stack already handles volatility regime, so make no discretionary macro-thesis overrides. | R1 abs |  |
| LESSONS-E-7 | E1 Connection to standing doctrine L57-60 | Do not add regime overlays at the strategy or execution layer; a discretionary macro-thesis skip counts as an execution-time regime overlay. | R1 abs |  |
| LESSONS-E-8 | E1 Watch-point L62-64 | Flag a macro-skip pattern when skip rate on tier-1 macro days (CPI/FOMC/NFP/BOJ) exceeds baseline by 1.5x with at least two macro-day skips in the window. | R33 DEL | Enforcer scripts/journal_review.py absent (RETIRE table, ADR 2026-07-11-ops-cfd-estate-retirement); manual execution retired by ADR 2026-06-30; watch-point cannot fire. |
| LESSONS-E-9 | E1 Output trigger L66-68 | When a lesson's watch-point fires, cite the lesson by name and cost from the registry; do not re-derive the rule each time. | R33 abs |  |
| LESSONS-E-10 | E2 Rule L87-91 | When a signal specifies a single entry size, execute one entry; do not re-enter on minor BB-touches within the held position, splitting one stop into many. | R1 DEL⚖ | Manual FIRE-alert execution retired (ADR 2026-06-30; FXIFY closed 2026-07-10 addendum); but ADR 2026-07-11 §2 KEEPs lesson rules, so removal is operator's call. |
| LESSONS-E-11 | E2 Watch-point L109-113 | Flag discretion-on-largest when TAKEN-DISCRETIONARY events concentrate over 50% on the highest-allocation strategy with at least two events, including multi-fill-on-single-signal. | R33 DEL | check_discretion_on_largest lived in scripts/journal_review.py, absent and retired with ops/live_journal by ADR 2026-07-11; no TAKEN-DISCRETIONARY source exists. |
| LESSONS-E-12 | E3 Provisional rule L134-137 | Log a one-line skip entry (date, strategy, alert tag, one-sentence reason) at the moment of skipping a signal, not reconstructed later. | R33 DEL⚖ | Never-promoted candidate for manual signal skips, retired by ADR 2026-06-30; ops/live_journal skip surface absent; registry KEEP (ADR 2026-07-11) makes it operator's call. |
| LESSONS-E-13 | E3 Watch-point L147-150 | Treat three or more MISSING skip rationales in a review window as non-operationalized discipline; three consecutive such windows trigger E3 promotion. | R33 DEL | MISSING-rationale review windows came from absent scripts/journal_review.py (retired ADR 2026-07-11); E3 promotion frozen by the 2026-08-14 notice. |
| LESSONS-E-14 | E4 Rule L162 | Keep the live indicator on the execution feed; never manually re-derive SL or size from a different-feed indicator during the fire window. | R18 DEL⚖ | Names retired Alchemy/DXTrade (FXIFY closed 2026-07-10) and manual SL/size entry (ADR 2026-06-30); feed-specific geometry lives in Rule 18; candidate status unclear. |
| LESSONS-E-15 | E4 Watch-point L168 | Flag when two or more trades in a review window show material adverse entry slippage attributable to feed-realign latency on the same broker feed. | R33 DEL | Weekly execution deviation table was ops/live_journal tooling, git-rm'd by ADR 2026-07-11; no manual fills exist to slip. |
| LESSONS-E-16 | Candidate watch-list L176-178 | Do not cite candidate watch-list observations as lessons or add them to the registry until a clear dated incident anchors them. | R33 abs |  |
| LESSONS-E-17 | Candidate watch-list L180-193 | Monitor size-cutting, early-exit-on-winner and first-trade-of-day-skip biases via TAKEN-DISCRETIONARY size, exit-time and skip-rate deviation fields. | R33 DEL | TAKEN-DISCRETIONARY size/exit/skip fields lived in ops/live_journal (absent, retired ADR 2026-07-11); manual trading retired ADR 2026-06-30; no anchored incident. |
| LESSONS-E-18 | Doctrine cross-references L201-203 | Trade the system, not your opinion: macro-volatility or other opinions are no basis for deviating from system signals. | R1 abs |  |
| LESSONS-E-19 | Doctrine cross-references L205-208 | Make no discretionary overrides of system signals, size or timing. | R1 abs |  |
| LESSONS-E-20 | Doctrine cross-references L215-217 | Read the execution-lesson registry alongside fxify-challenge's Core Principles, treating them as one doctrine at different abstraction layers. | R1 DEL | Pairs registry with fxify-challenge Core Principles, absent from repo .claude/skills; FXIFY closed (ADR 2026-06-30 addendum 2026-07-10); doctrine now absorbed by Rule 1. |
| LESSONS-E-21 | Changelog 2026-07-11 L233-237 | Treat E1-E4 watch-point references to journal_review.py as historical; the lesson rules themselves remain standing methodology. | R30 abs |  |

</details>

<details><summary><code>docs/methodology/lessons/methodology_lessons.md</code> — 157 rules: 43 absorbed, 94 detail, 20 delete</summary>

| ID | Where | Rule | → | Note |
|---|---|---|---|---|
| LESSONS-M1-1 | Preamble L8 | Classify each lesson as E-class (execution, dated trade), M-class (methodology, dated decision artefact) or F-class (fixture-caught counterfactual defect) and file it in that registry. | R33 det |  |
| LESSONS-M1-2 | Preamble L30 | Treat the lesson registries as durable canon; memory entries overlapping a registered lesson are only compact pointers to it. | R29 abs |  |
| LESSONS-M1-3 | §Format spec L37 | Author new M-class lessons in the light format: Date/Anchor, What broke, one-sentence imperative Rule, optional Mechanism, Link. | R33 det |  |
| LESSONS-M1-4 | §Format spec L38 | Do not retroactively rewrite legacy 8-field lesson entries (M-7 onward, pre-2026-08-29) into the light format; keep them unedited. | R33 det |  |
| LESSONS-M1-5 | §Format spec L52 | Add a lesson only when a real incident earns it; once written it is in force, with no promotion ceremony, dollar threshold or CANDIDATE/PROMOTED tracking. | R36 abs |  |
| LESSONS-M1-6 | §Format spec L53 | Never delete a superseded lesson; keep it and mark '[SUPERSEDED — see M-N]' at its own top. | R30 det |  |
| LESSONS-M1-7 | §Legacy format L56; per-lesson Promotion criteria | Promote legacy lessons CANDIDATE to PROMOTED on a second independent firing or a >=$3K cost, updating the Cost section at each firing. | R33 DEL | Superseded by the 2026-08-29 light-format rule (methodology_lessons.md L52): no promotion ceremony, dollar threshold or CANDIDATE/PROMOTED state machine. |
| LESSONS-M1-8 | §File ownership L63 | Edit this lesson file first; the brief-authoring skill is downstream and inherits changes on next sync (repo wins). | R29 abs |  |
| LESSONS-M1-9 | §Migration plan L72 | Migrate M-1..M-6 from Notion/memory into this file on first cite; until then treat those external pointers as authoritative. | R33 DEL | M-1..M-6 have zero headings (2026-08-08 conventions audit L249); Notion made read-only by ADR 2026-06-12; migration never fired. |
| LESSONS-M1-10 | §Migration plan L82 | Number a new M-lesson with the next free integer above the highest in use; check memory (and Notion) before claiming a number. | R33 det |  |
| LESSONS-M1-11 | §Index standalone L91 | Lessons that do not fit the M-N format may live as standalone files, indexed in this registry's standalone-file section (provisional dual pattern). | R33 det |  |
| LESSONS-M1-12 | M-7 Rule L118 | Before declaring a Pine strategy lock complete, read the locked source and confirm every signal condition has a paired alert() call, not only alertcondition(), inside the active-window guard. | R14 DEL⚖ | Signal origin is the Python daemon (S2 ADR 2026-08-07); c1-rail skill invariant 9 (JSON-only alerts, re-pin) owns Pine alerts; legacy book retired. |
| LESSONS-M1-13 | M-7 Output trigger L142 | When alert() plumbing is missing at lock, halt the lock and patch it in the same session; never defer it to the next lock cycle. | R14 DEL⚖ | Same as M-7 Rule: TV alert path not the live signal origin (S2 ADR); c1-rail invariant 9 owns Pine-edition alert changes. |
| LESSONS-M1-14 | M-8 Rule L192 | Scope count-only disposition thresholds in briefs to the target surface (e.g. production risk-control sites), or flag them mechanical-only with a §6 DONE_WITH_CONCERNS/parent-override line. | R33 det |  |
| LESSONS-M1-15 | M-8 Forbidden L233 | Treat DONE_WITH_CONCERNS as the recovery channel, not a failure; never author a brief that leaves the spawn no concerns channel. | R4 abs |  |
| LESSONS-M1-16 | M-9 Rule L267 | Protect gitignored vendor-data manifests with a local pre-commit hash gate; CI cannot hash bytes absent from the repo. | R19 abs |  |
| LESSONS-M1-17 | M-9 Watch-point L283 | On any PR touching SHA256SUMS, vendor panels or a re-export, confirm hooks are installed and the manifest regen lands in the same commit as the CSV change. | R19 abs |  |
| LESSONS-M1-18 | M-9 Output trigger L287 | Run check_data_manifests.py --check; on failure run --regenerate --dry-run, then --regenerate. | R19 abs |  |
| LESSONS-M1-19 | M-9 Forbidden L292 | Do not treat .github/workflows/manifest-check.yml as byte-level integrity coverage; it enforces format and tracked paths only. | R19 abs |  |
| LESSONS-M1-20 | M-9 Forbidden L294 | Do not use git commit --no-verify for routine vendor-data work; reserve it for exceptional bypass with explicit rationale. | R19 abs |  |
| LESSONS-M1-21 | M-10 Rule L320 | Route a firm's display and failure output exclusively through its rule validator; never ship parallel simplified DD semantics for the same firm. | R16 DEL | FXIFY row deleted Phase 4 (PR #572); ops/accounts.py absent; ops/cli.py keeps only tearsheet; Rule 16 one-source covers the principle. |
| LESSONS-M1-22 | M-10 Rule L322 | Never default synthetic inputs (e.g. a fake prior EOD equity) that defeat an explicit skip path. | R40 abs |  |
| LESSONS-M1-23 | M-10 Rule L323 | Persist audit-worthy completion as real per-phase ISO timestamps and verify JSON round-trip for any new persisted field. | R16 DEL | Anchored to accounts.json phase_completed_at; ops/accounts.py absent and cli add/update/status removed (substrate-retirement ADR 2026-07-22). |
| LESSONS-M1-24 | M-11 Rule L385 | When a patch reuses inherited predicates or gating, the pre-registered §4 falsifier must test the interaction with the inherited gate, not the new behavior alone. | R23 det |  |
| LESSONS-M1-25 | M-11 Output trigger L421 | In an inheritance-extending brief's §4, include a scenario where inherited and new intent diverge, an assertion of correct firing there, and proof the scenario shows the divergence. | R33 det |  |
| LESSONS-M1-26 | M-11 Forbidden L434 | Do not defer interaction-scenario authoring to the spawn; the brief author writes it and the spawn verifies. | R33 det |  |
| LESSONS-M1-27 | M-11 Forbidden L437 | Do not treat 'the existing infrastructure already works' as evidence that the patched behavior works. | R0 abs |  |
| LESSONS-M1-28 | M-12 Rule L503 | After a handoff changes a gitignored target (Pine, sealed config, binary), promptly verify deployment against the system of record; the worker's DONE is not sufficient. | R0 abs |  |
| LESSONS-M1-29 | M-12 Output trigger L547 | A handoff touching a gitignored target must forbid local edits, run diff-generation-only, and add §7 parent system-of-record review plus a §10 audit hook against that system. | R33 det |  |
| LESSONS-M1-30 | M-13 Rule L640 | Apply every Pine parameter-lock change to both the strategy and indicator .pine, diff both for each changed parameter, and re-export both before declaring it complete. | R14 DEL⚖ | Indicator .pine exist only in _archive (MANIFEST.sha256); accepted book is strategy-only (BOOK_SOURCES); locked params immutable and agents never edit Pine. |
| LESSONS-M1-31 | M-13 Rule L644 | Add 'update the indicator .pine alongside the strategy .pine' as a step of the params.toml same-commit workflow. | R14 DEL⚖ | params.toml and scripts/validate_params.py absent; retired by docs/adr/2026-08-03-params-toml-gate-retirement.md. |
| LESSONS-M1-32 | M-13 Forbidden L696 | Do not read validate_params.py 0/0 as evidence the indicators are current when Pine is absent from the clone. | R21 DEL⚖ | scripts/validate_params.py absent (ADR 2026-08-03); green-gate-is-not-coverage stands at M-27 and Rule 21. |
| LESSONS-M1-33 | M-13 Forbidden L700 | Do not assume strategy and indicator .pine agree because they share a shorttitle; read each file's own input defaults. | R0 abs |  |
| LESSONS-M1-34 | M-14 Rule L724 | Before reading an empty strategy-tester result as indicator/strategy divergence, read the strategy .pine startDate/endDate input defaults. | R0 det |  |
| LESSONS-M1-35 | M-14 Rule L724 | Do not treat cross-feed reproduction of an empty result as evidence of real divergence; a Pine-internal date gate reproduces on every feed. | R0 det |  |
| LESSONS-M1-36 | M-14 Forbidden L737 | Do not let an operator-endorsed hypothesis license skipping the Rule-0 source read. | R0 abs |  |
| LESSONS-M1-37 | M-14 Output trigger L732 | If a strategy endDate predates the test window, bump it (inputs one-off, or Pine default plus manifest regen) and re-run before any divergence conclusion. | R0 det |  |
| LESSONS-M1-38 | M-15 Rule L753 | Pin any offline instrument that re-ports a source-of-truth computation against a real source artifact or hand-computed ground truth, never only self-generated fixtures. | R24 det |  |
| LESSONS-M1-39 | M-15 Rule corollary L753 | When a faithfulness or look-ahead audit finds a source-vs-recompute mismatch, halt or surface it as a blocker; never silently prefer the recompute. | R24 det |  |
| LESSONS-M1-40 | M-15 Output trigger (c) L761 | Port Pine series[k] as arr[i-k] (k bars back), never arr[i+k]; re-check every offset when a first real export arrives. | R24 det |  |
| LESSONS-M1-41 | M-15 Forbidden L767 | Do not treat an all-findings-refuted adversarial review as faithfulness coverage before the instrument has run on real source data. | R24 det |  |
| LESSONS-M1-42 | M-16 Rule L781 | For stop or break-entry candidates, run a fill-slip sweep (0-1.5 ticks) and require cost-net edge to survive >=1 realistic tick before exit, sizing or MC work. | R24 det |  |
| LESSONS-M1-43 | M-16 Rule L781 | Order validation tests by probability of changing the verdict divided by cost; run the cheapest decisive falsifier first. | R24 abs |  |
| LESSONS-M1-44 | M-16 Forbidden L787 | Do not use a spread-only cost charge as the fill model for a stop or break entry. | R24 det |  |
| LESSONS-M1-45 | M-16 Forbidden L788 | Do not let stability screens (all-years-positive, both-sides-positive) substitute for the fill-robustness check. | R24 det |  |
| LESSONS-M1-46 | M-17 Rule L802 | Test anchor-specific edge of a time-anchored intraday setup with a same-day window-slide placebo that varies only the anchor time. | R24 det |  |
| LESSONS-M1-47 | M-17 Rule L802 | Name the null and confirm its distribution is non-degenerate (sane mean and variance) before reading or reporting its p-value. | R24 det |  |
| LESSONS-M1-48 | M-17 Forbidden L805 | Do not use cross-day or cross-instrument rotation as the null for a price-level-anchored intraday setup. | R24 det |  |
| LESSONS-M1-49 | M-17 Forbidden L806 | Do not use a direction-flip as the null for a stop-based setup; it tests stop placement, not the signal. | R24 det |  |
| LESSONS-M1-50 | M-18 Rule L821 | Treat a deadline-capped challenge as a Sharpe race: compute the analytic edge-times-frequency versus barrier pass ceiling before commissioning a full first-passage MC. | R24 DEL⚖ | No FIRM_RULES tier has a deadline cap (grep core/firm_rules.py); FXIFY anchor deleted Phase 4 (PR #572); a time-capped objective could return. |
| LESSONS-M1-51 | M-18 Rule L821 | Choose challenge exits by information ratio and time-to-target under the horizon cap, not by maximum positive skew. | R24 DEL⚖ | Same as M-18 screen: deadline-capped FXIFY challenge is a historical fixture (core/historical_challenge.py); no current capped tier. |
| LESSONS-M1-52 | M-19 Rule L840 | Before committing a discovery axis, compute its DSR floor at the axis K against the best in-house edge and corrected literature Sharpe; drop the axis if the floor exceeds both. | R23 det |  |
| LESSONS-M1-53 | M-19 Forbidden L844 | Treat campaign K as the reachability budget, never free; prefer low-K mechanism-first axes over high-K blind mining. | R23 det | → .claude/skills/futures-anomaly-discovery/SKILL.md |
| LESSONS-M1-54 | M-19 Forbidden L845 | Anchor any realism ceiling as a formula over external data frozen before measuring; never use a felt ceiling. | R23 det |  |
| LESSONS-M1-55 | M-20 Rule L861 | Discharge a §R reachability attestation only by simulating in that gate's own units, at its scoring basis (IS/OOS panel, not current prices), with commissions divided out explicitly. | R23 abs |  |
| LESSONS-M1-56 | M-20 Forbidden L864 | Give every gate a campaign can die at its own same-units reachability simulation; never attest REACHABLE from the confirm-floor argument alone. | R23 abs |  |
| LESSONS-M1-57 | M-20 Rule L861 / banner L855 | Apply strategy_harvest Requirement 5's mandatory cost-law inequality in §R attestations and again at seed admission. | R24 DEL | Requirement 5 deleted by operator ruling 2026-10-24 (strategy_harvest.md L32, L68); M-20 banner L855 says these sentences no longer bind. |
| LESSONS-M1-58 | Output triggers L289/L426/L685/L732/L761 | When a lesson's watch-point fires, cite the lesson and its cost instead of re-deriving the discipline. | R33 abs |  |
| LESSONS-M2-1 | M-21 Rule L882 | Admit a candidate as a leg of a book judged by a dollar-trailing drawdown barrier only if it raises risk N_eff (covariance PR, n_eff_risk_delta > 0); dependence N_eff never suffices. | R24 abs |  |
| LESSONS-M2-2 | M-21 Rule/Output trigger L882-890 | Screen rho = candidate/book daily-$std at intended weight first; if rho >= 1.0 or risk delta <= 0, reject the book leg without running the frozen engine. | R24 abs |  |
| LESSONS-M2-3 | M-21 Forbidden moves L894 | Do not iterate a failed composed candidate's weight to pass the screen or engine; a failed composed candidate closes. | R23 abs |  |
| LESSONS-M2-4 | M-21 Forbidden moves L895 | Bind rho and the tau_risk floor a-priori in the compose pre-registration; never read or set them after seeing MC output. | R23 abs |  |
| LESSONS-M2-5 | M-21 Output trigger L890 | When a lesson's watch-point fires, cite the lesson by name plus its anchor figure; do not re-derive it. | R33 abs |  |
| LESSONS-M2-6 | M-22 Rule L917 | When authoring an always-on freshness/integrity gate, audit whether a compared field derives from gitignored disk presence; if so WARN and exit 0 when absent, hard-fail all real drift. | R38 det |  |
| LESSONS-M2-7 | M-22 Output trigger L925 | Ship every disk-reading always-on gate with a bare-worktree absent-bytes test asserting exit 0 plus WARN, and tests that real drift still fails; never infer worktree-safety from the primary tree. | R38 det |  |
| LESSONS-M2-8 | M-22 Recommendation L927 | Do not add a standalone mechanical meta-gate to detect disk-presence-derived fields; enforce via the gate-authoring test convention at review. | R36 abs |  |
| LESSONS-M2-9 | M-22 Forbidden moves L930 | Do not run --regenerate or re-sync a manifest to clear an integrity-gate failure on a worktree or clone lacking the gitignored bytes. | R19 det |  |
| LESSONS-M2-10 | M-22 Forbidden moves L931 | Do not commit --no-verify past an integrity-gate false positive; fix the gate to presence-degrade instead. | R19 det |  |
| LESSONS-M2-11 | M-AHF Counter-measure 1 L969 | Before committing an audit hook, state the property it checks in plain language, not as a grep expression. | R33 det |  |
| LESSONS-M2-12 | M-AHF Counter-measure 2 L970 | cat the audit target and confirm the hook matches the literal storage form; cover every alternate form the property could take. | R33 det |  |
| LESSONS-M2-13 | M-AHF Counter-measure 3 L971 | Prefer form-agnostic, section-scoped property assertions over form-specific matches when storage form is variable. | R33 det |  |
| LESSONS-M2-14 | M-AHF Instance 4 L963 | Design audit hooks assuming their own committed command and output text will re-enter the corpus; hooks must not self-match on re-run. | R33 det |  |
| LESSONS-M2-15 | M-AHF Promotion provenance L982; F-1 L1077 | Registry promotion: CANDIDATE becomes PROMOTED on one instance costing >= $3,000 or three instances; third instance auto-graduates regardless of cost. | R33 DEL | Superseded by 2026-08-29 light format (methodology_lessons.md L52): no dollar threshold, no CANDIDATE-to-PROMOTED state machine. |
| LESSONS-M2-16 | F-1 Rule/Output trigger L1036-1075 | Before citing an analysis-script output as brief evidence, confirm a tests/ fixture pins its anchor invariant against an independent value and pytest is green; else block authoring. | R0 abs |  |
| LESSONS-M2-17 | M-SWAP-1 Rule L1129 | When a Pre-Q tests lock impact of an additive cost shock, check whether implied_1r shifts; if it does, propagate the cost using a fixed pre-shock implied_1r reference. | R24 det |  |
| LESSONS-M2-18 | M-SWAP-1 Wrong-verdict/Output trigger L1123,L1149 | For additive-cost-shock questions, specify both adaptive-1R and fixed-1R MC; express verdict triggers against fixed-1R and treat the more conservative verdict as canonical. | R24 det |  |
| LESSONS-M2-19 | M-SWAP-1 Forbidden moves L1153 | Do not cite a FALSIFIED adaptive-1R MC as proof that an additive cost shock is immaterial. | R24 det |  |
| LESSONS-M2-20 | M-SWAP-1 Forbidden moves L1154 | Do not use adaptive-1R MC to set dd_protection calibration when a known additive cost shock is present. | R14 det |  |
| LESSONS-M2-21 | M-SWAP-1 Forbidden moves L1155 | Do not tweak cost rates or magnitudes to make adaptive-1R MC produce a verdict-meaningful delta; use fixed-1R instead. | R23 abs |  |
| LESSONS-M2-22 | M-SWAP-1 Forbidden moves L1156 | Do not treat M-SWAP-1 as falsifying the swap question; it falsifies only the adaptive-1R answer, pending Q-SWAP-2. | R28 DEL | Pending condition discharged: Q-SWAP-2 closed AMBIGUOUS-HOLD 2026-05-26 (M-SWAP-1 wrong-verdict anchor); Q-SWAP domain evicted 2026-06-07. |
| LESSONS-M2-23 | M-Q-SWAP-3-2 Rule L1193 | When headline criteria are multi-metric, state the Phase 4 regime floor as those same criteria; bootstrap p5, H1 and H2 each clear all; never default to strict-lock criteria. | R24 det |  |
| LESSONS-M2-24 | M-Q-REGIME-1 Rule 1 L1252 | When a half-panel split lands within two months of 2024-04-30, treat the H1/H2 spread as priors-shifting; never discount it as sample-size noise without a multi-boundary sweep. | R24 DEL⚖ | Anchor is retired Pepperstone legacy panel (2026-08-02 retirement ADR); CME transfer unestablished; operator decides whether the 2024 inflection carries. |
| LESSONS-M2-25 | M-Q-REGIME-1 Rule 2 L1253 | Reference the 2024 regime-shift memory (project_2024_regime_shift_accumulating_signal) explicitly in such a brief's §1/§4. | R33 DEL | Cites external memory unreadable in repo (LESSONS_INDEX.jsonl: external-unmigrated, content_verified false); no MEMORY.md exists. |
| LESSONS-M2-26 | M-Q-REGIME-1 Rule 3 L1254 | If the 2024-boundary spread is verdict-deciding, consider a multi-boundary sweep (portfolio_mc --boundary-sweep) as a cheap falsifier even when only one boundary is specified. | R24 DEL⚖ | --boundary-sweep is hard-wired to legacy GA-4 allocations, FXIFY swap and PRE_SHOCK_1R (core/mc/modes.py L896); Pepperstone panel retired. |
| LESSONS-M2-27 | M-Q-REGIME-1 Rule 4 L1255 | If a brief frames the spread as artifact-vs-structural, include at least three non-2024 boundaries with 18+ months per side, or document the narrowing. | R23 DEL⚖ | Search-space bound serves only the retired-panel 2024 artifact-vs-structural question (Pepperstone retired 2026-08-02); operator decides transfer. |
| LESSONS-M2-28 | M-Q-REGIME-1 Forbidden moves L1282 | Do not open a mechanism follow-up as a fishing expedition; specify candidate mechanisms in §4 before it spawns. | R23 abs |  |
| LESSONS-M2-29 | M-Q-REGIME-1 Forbidden moves L1283 | Do not treat a structural-inflection finding as confirming any specific mechanism until a mechanism investigation resolves it. | R24 det |  |
| LESSONS-M2-30 | M-23 Enforcement L1322 | When correctness depends on a mutated module-level constant, apply it inside each worker after re-import, attest the consumed value in the report, and assert one value across all work units. | R0 det |  |
| LESSONS-M2-31 | M-23 Why invisible L1319 | Run any reproduction control through the same process pool as the arm it certifies; an in-parent control certifies nothing about worker state. | R21 det |  |
| LESSONS-M2-32 | M-23 Blast-radius rule L1333 | When a process-boundary defect is found, name the affected arms, re-measure what is load-bearing, and mark un-re-measured cells impeached. | R30 det |  |
| LESSONS-M2-33 | M-24 Enforcement L1366 | On correcting a venue fact, sweep numbers and behaviour (not only config keys) across every harness simulating the phase, check phase scoping, and record the checked surfaces. | R30 det |  |
| LESSONS-M2-34 | M-24 Corollary L1374 | When a defect lands on a harness with a queued re-run, amend the re-run's specification in the same change. | R30 det |  |
| LESSONS-M2-35 | M-26 Rule L1388 | Keep frozen artifact bodies unedited with an upstream reader-intercept; correct living documents in place at the assertion site; same-session work is never frozen. | R30 abs |  |
| LESSONS-M2-36 | M-26 Rule L1388 | Treat a withdrawal as complete only after grepping the withdrawn value repo-wide, including artifacts authored the same session. | R30 abs |  |
| LESSONS-M2-37 | M-26 Rule L1388 | After any correction, re-read the artifact top-down as its consumer would and stop where they would stop. | R30 det |  |
| LESSONS-M2-38 | M-27 Rule L1397 | Before trusting a gate, establish what failure class it targets, what its predicate inspects, and whether that can see the failure; test a planted case where cheap. | R21 det |  |
| LESSONS-M2-39 | M-27 Rule L1397 | Design checkers so an empty input set never yields the strongest green and SKIP is never exit 0 in an artifact self-check. | R38 det |  |
| LESSONS-M2-40 | M-28 Rule L1405 | Before claiming work is missing, search a distinctive sentence from it with rg --no-ignore -l over the whole tree; a path or ID miss proves nothing. | R0 det |  |
| LESSONS-M2-41 | M-28 Rule L1405 | Do not treat an empty default search or Grep over docs/ltm or lab/archive as evidence of absence; those stores are search-excluded. | R8 abs |  |
| LESSONS-M2-42 | M-29 Rule L1413 | When borrowing a number, convert it to your own parameters in the same edit before using it in a decision. | R20 abs |  |
| LESSONS-M2-43 | M-29 Rule L1413 | Never state an effect's direction or sign from a proxy run; a proxy shows only that an effect may exist. | R20 det |  |
| LESSONS-M2-44 | M-29 Rule L1413 | Before an N-replication design, print 2*SE against the tolerance and raise N or use paired arms if it cannot answer; check sigma for verdicts near tolerance. | R23 det |  |
| LESSONS-M2-45 | M-29 Rule L1413 | Mark a borrowed number's provenance in the artifact as written, and fix the generator, not only the rendered document. | R20 det |  |
| LESSONS-M2-46 | M-30 Rule L1421 | Fetch and diff origin/main at the start of multi-step work, before authoring a brief or spec, before push, and before any irreversible or budget-spending step. | R8 det |  |
| LESSONS-M2-47 | M-30 Rule L1421 | When asked to discharge an owed item, grep origin/main for its slug first. | R0 det |  |
| LESSONS-M2-48 | M-30 Rule L1421 | Treat an orphaned or reset-away commit as evidence, not debris; read the reflog before running it. | R0 det |  |
| LESSONS-M2-49 | M-30 Rule L1421 | After any merge touching AGENTS.md, STATE.md or an ADR, grep the merged result for both sides of each changed claim. | R30 det |  |
| LESSONS-M2-50 | M-31 Rule L1429 | Before reporting an owed, missing or never-measured claim, grep the campaign's own artifacts (RESULTS, calibration JSON, addenda) for the measurement. | R0 det |  |
| LESSONS-M2-51 | M-31 Rule L1429 | In multi-agent sweeps, give the verifier the explicit axis: for every owed X, search for X already done. | R41 det |  |
| LESSONS-M2-52 | M-32 Rule L1437 | Before a quotation or specific attributed claim lands, verify the exact text at source (rg or real fetch), or drop the quotation marks and attribute a paraphrase. | R0 det |  |
| LESSONS-M2-53 | M-32 Rule L1437 | Check that a source's claimed dates precede its publication date and chase a repeated statistic to its root. | R0 det |  |
| LESSONS-M2-54 | M-33 Rule L1445 | Before asserting something does not exist, enumerate its class (ls, glob, rg --no-ignore), not one path; report scoped absence ('not found at X; Y unsearched'). | R0 det |  |
| LESSONS-M2-55 | M-33 Rule L1445 | Verify a prescribed remedy is actually possible before prescribing it. | R0 abs |  |
| LESSONS-M2-56 | M-34 Rule L1453 | When judging a PR that amends a ratified artifact, hash previously ratified blocks against the ratifying commit instead of reading the diff as one edit. | R0 det |  |
| LESSONS-M2-57 | M-35 Rule L1461 | When verification falsifies several pins, check each separately for where its fix landed (kernel default vs driver override) and grep kernel module literals against verified values. | R30 det |  |
| LESSONS-M2-58 | M-35 Rule L1461 | Before reusing a corrected harness, read its module-level constants directly and pin the override in the pre-registration. | R0 det |  |
| LESSONS-M2-59 | M-36 Rule L1469 | End a closing brief with three equal lists: actions landed with verification, deliberate non-actions with one-line rationale, off-radar items confirmed live. | R33 det |  |
| LESSONS-M2-60 | M-36 Rule L1469 | Start later passes from inherited watch-items plus new surface; before proposing consolidation near a locked file, grep the prior brief's watch-items. | R8 det |  |
| LESSONS-M2-61 | M-37 Rule L1477 | In a reviewer fold loop, count findings per round; stop when the count fails to fall for two rounds or the document grows on a fix round. | R7 det |  |
| LESSONS-M2-62 | M-37 Rule L1477 | Route unchosen operator options out of a document before specifying them. | R35 det |  |
| LESSONS-M2-63 | M-37 Rule L1477 | End a stopped fold loop with one-line folds, an 'Open items (recorded, not folded)' section, one reply per thread, then merge with no further review request. | R6 DEL | Superseded by surface-allocation ADR Addendum 2026-10-24b A(1): merge needs a clean Codex review within three, else return to owner. |
| LESSONS-M2-64 | M-37 Rule L1477 | When a simplification deletes verified specifics, carry those specifics forward. | R31 abs |  |
| LESSONS-M2-65 | M-37 Rule L1477 | Never mention @codex in a coordination comment. | R6 det |  |
| LESSONS-M2-66 | M-38 Rule L1485 | For verifier or owner code implementing a written contract, first build an invariant table: each claim maps to one named refusal and one test violating only it. | R33 det |  |
| LESSONS-M2-67 | M-38 Rule L1485 | Check cross-field contract claims in one function with the whole record in hand. | R40 det |  |
| LESSONS-M2-68 | M-38 Rule L1485 | Give durable state owners a state machine with one transition function that rewrites and hashes the whole row. | R40 det |  |
| LESSONS-M2-69 | M-38 Rule L1485 | Fold at most two review rounds on contract-driven code; a third round means rebuild from the invariant table then one review; tell the operator before round two. | R7 det |  |
| LESSONS-M2-70 | M-38 Rule L1485 | Where the contract's required evidence does not exist, refuse the feature rather than approximate it with a lookalike field. | R40 det |  |
| LESSONS-M2-71 | M-39 Rule L1493 | For specs with orders, positions or shutdown semantics, first write a state table with one writer and explicit UNKNOWN, fail-closed action classes, cut-point event sequences, event-by-state matrix; derive requirements. | R33 det |  |
| LESSONS-M2-72 | M-39 title L1488 | Fold an orders/positions/shutdown spec only once; a second review round rebuilds it from the state model and event sequences. | R7 det |  |
| LESSONS-M2-73 | M-39 Rule L1493 | Check every live-execution path against the qualified emulator semantics; a recorded deviation does not qualify a substitute path. | R11 det | → docs/spec/2026-09-12-c1-multi-leg-rail-extension-spec.md §Invariants I8 |
| LESSONS-M2-74 | M-39 Rule L1493 | Make acceptance gates require executable sequence tests, not test-name coverage. | R21 abs |  |
| LESSONS-M2-75 | M-40 Rule L1501 | After stacking a child PR on an unmerged parent, request review only after the parent lands and main is merged back, or retarget the child's base first. | R6 det |  |
| LESSONS-M2-76 | M-40 Rule L1501 | Route findings on parent content to the parent's owner in one follow-up PR on main; never fold them into the child. | R6 det |  |
| LESSONS-M2-77 | M-40 Rule L1501 | Before requesting review, run git diff --stat <base>...HEAD and confirm every file is one this PR owns. | R6 det |  |
| LESSONS-M2-78 | M-41 Rule L1509 | Register every private file a public record pins in a tracked manifest or PRIVATE_EVIDENCE.sha256, archive it with evidence_archive.py put and push, in the pinning step. | R13 det |  |
| LESSONS-M2-79 | M-41 Rule L1509 | Keep private outputs under a verified-ignored root of the primary checkout (git check-ignore -v), never under .worktrees/* or .claude/worktrees/*; access them by absolute path. | R13 det |  |
| LESSONS-M2-80 | M-41 Rule L1509 | Before any worktree removal, list its ignored entries with scripts/repo_hygiene.py and stop if any is unarchived. | R13 det |  |
| LESSONS-M2-81 | M-41 Rule addendum L1512 | Do not treat committing untracked evidence as preservation; archive it with evidence_archive.py put first. | R13 det |  |
| LESSONS-M2-82 | M-41 Rule addendum L1512 | Stage committed evidence with git -c core.autocrlf=false add, check text/eol attributes, keep it -text, and confirm staged blob id equals hash-object --no-filters. | R19 det |  |
| LESSONS-M2-83 | M-41 Rule addendum L1512 | Verify archived evidence with evidence_archive.py audit --verify (re-hashes blobs); plain audit only checks blob presence. | R19 det |  |
| LESSONS-M2-84 | M-41 Rule addendum L1512 | Extract pinned evidence only with git cat-file blob <sha>; never use --filters, git archive or git checkout for it. | R19 det |  |
| LESSONS-M2-85 | M-42 Rule L1520 | Before ratifying any Pre-Q, ADR, spec or closure, run a refute-first multi-lens review whose synthesizer re-reads source and discards unfounded findings; green check_brief.py is form-only. | R5 det |  |
| LESSONS-M2-86 | M-43 Rule L1528 | For every reviewer finding, verify against source whether the flagged text is wrong, the proposed replacement is right, and your own replacement is right. | R0 det |  |
| LESSONS-M2-87 | M-44 Rule L1536 | Before acting on an external handoff, verify every referenced path and re-read each claimed edit; treat completions as claims; return NEEDS_CONTEXT if unverifiable. | R0 abs |  |
| LESSONS-M2-88 | M-45 Rule L1544 | Before a test-commit-push chain, ls the test paths and capture the real exit code immediately (rc=$? or pipefail); prefer running tests and committing in separate calls. | R21 det |  |
| LESSONS-M2-89 | M-46 Rule L1552 | For any new control or convention, prefer structural fixes that scale with agent count (generate from source, gate labels to referents) over per-instance vigilance. | R36 abs |  |
| LESSONS-M2-90 | M-47 Rule L1560 | For work entering a PR, commit, push and open the PR and let Codex's PR review be the adversarial review; keep in-chat review for non-PR work and M-42 ratification. | R5 abs |  |
| LESSONS-M2-91 | M-48 Rule L1568 | When a verified fix is ready and the PR is open, push it first and refine the PR body afterward. | R6 det |  |
| LESSONS-M2-92 | M-48 Rule L1568 | For a gate failing locally, reproduce it in a clean worktree from origin/main before diagnosing against local state. | R22 abs |  |
| LESSONS-M2-93 | Versioning 2026-08-29 L1577 | Write new lesson entries in the light format (Date, Anchor, What broke, Rule, optional Mechanism, Link); do not retroactively rewrite M-7 through M-24. | R33 abs |  |
| LESSONS-M2-94 | Versioning header L1573 | Keep the versioning and change-log section at the bottom of the lessons file. | R33 det |  |
| LESSONS-M2-95 | Versioning 2026-09-20 L1576 | Index each lesson, with its memory twin where one exists, in docs/methodology/LESSONS_INDEX.jsonl. | R33 abs |  |
| LESSONS-M2-96 | Versioning 2026-05-10 L1587 | Protect gitignored vendor data with a local pre-commit hash gate while CI stays format-only. | R19 abs |  |
| LESSONS-M2-97 | Versioning 2026-05-28 L1637 | When patching infrastructure that inherits structural gating, include a pre-registered §4 falsifier testing the interaction of new behaviour with that gating. | R23 abs |  |
| LESSONS-M2-98 | Versioning 2026-05-28 L1662 | Verify gitignored-target handoffs after execution beyond the executor's own return status. | R0 abs |  |
| LESSONS-M2-99 | Versioning 2026-05-28 L1672 | Apply Pine parameter-lock changes to both strategy and indicator .pine and re-export both to TradingView. | R14 DEL⚖ | Superseded by stricter AGENTS.md: locked parameters immutable, never edit Pine; indicators only in _archive (MANIFEST); test_validate_params.py absent. |

</details>
