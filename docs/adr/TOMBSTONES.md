# ADR Tombstone Index

Current removals use explicit immutable commit/blob references below. Legacy rows
retain their original archive retrieval instructions. A tombstone records history,
not renewed permission; the linked current owner governs present work.


<a id="2026-09-15-cursor-agent-retirement"></a>

## 2026-09-15 Cursor agent retirement (PROPOSED — pending operator ratification)

Operator instruction 2026-09-15: *"cursor is being retired altogether, we will no longer be
incorporating cursor agents. it will be just claude and codex."* Already ruled for one campaign
as D-B6 (2026-09-11) and preceded by the 2026-09-10 removal from recurring spend
([`d16`](../pursuits/d16-cursor-subscription.md)). Current owner of the surviving rules:
[`2026-07-14-cc-cursor-surface-allocation.md`](2026-07-14-cc-cursor-surface-allocation.md),
Revision 2026-09-15 (§Decision, §8 disposition table, §9 operator actions).

**No ADR file was removed.** `2026-08-14-cc-cursor-autonomous-loop.md` was superseded in full and
converted to the standard hot-stub/cold-body form; its body is live at
`docs/ltm/adr/2026-08-14-cc-cursor-autonomous-loop.md`, not deleted. The rows below are the
**non-ADR** artifacts removed by the sweep. This tombstone records history, not renewed
permission: retrieval does not revive the Cursor lane.

All blobs are reachable from commit `242992b741dc44485b491aab45075ab44e1b34ef`
(`git show <blob>` retrieves any row directly).

| Removed path | Disposition / current owner | Immutable blob |
|---|---|---|
| `.claude/skills/cursor-fleet/SKILL.md` | Deleted at operator instruction. Orchestration loop restated surface-agnostically in the owning ADR's §Decision; local-only gate owned by `task-routing`; dated friction ledger remains in `docs/SESSIONS.md` and the programme audits. Residual map: [`a6`](../pursuits/a6-cursor-fleet-worker-capability.md) R1–R6. | `56f728a47d39c9a3eb172858df85f7f6ed679775` |
| `.cursor/hooks/before_shell.py` | **Migrated, not dropped** — the only hook whose discipline had no surviving owner. Ported to [`scripts/guard_shell_command.py`](../../scripts/guard_shell_command.py) with tests; wiring is an operator election (CLAUDE.md §Continuous improvement item 6). | `01021d30db9063344ed3ce617dc6e9bcecb1bca7` |
| `.cursor/hooks/after_file_edit.py` | Adapter remapping Cursor's payload into `scripts/lock_event_hook.py` + `scripts/sync_skills_hook.py`, both still registered in `.claude/settings.json`. Adapter-only; no discipline lost. | `5854d9d5465d85d67945095ed43610196e5faaa4` |
| `.cursor/hooks/blast_radius_stop.py` | Mirror of the Claude-side `warn-blast-radius` rule, which is the primary and survives. | `720a749e46ca5c24d65d4743149179771cfd4f68` |
| `.cursor/hooks/blast_radius_ledger.py` | Ledger helper for the above; state dir was gitignored. | `2faa02b48a66255f96e39d16694ecd875ac09e0c` |
| `.cursor/hooks/record_edit.py` | Ledger writer for the above. | `0af7a25080ffe58457a32ddd466a27723697c87a` |
| `.cursor/hooks.json` | Cursor hook registration only. | `041d4c17ef5af5a6e035c07d209ab323934ee2b6` |
| `.cursor/environment.json` | Cursor cloud provisioning (pip install + `scripts/install_hooks.sh`). No surviving surface reads it; Codex/Claude provisioning is not repo-owned. | `56e1b66a1c8777d5181437f8fc0e0e3fafa48d52` |
| `.cursor/settings.json` | Cursor editor plugin toggle. | `f9d35f82874f76e7d31e566b4316d9c5718fc6b9` |
| `.cursor/rules/agent-conduct.mdc` | Derived mirror; owner `CLAUDE.md` + `docs/operational_rules.md`. | `8080e1617a4f4f1026a6ab66ae9e8996761bc095` |
| `.cursor/rules/clean-code.mdc` | Derived mirror; generic style guidance. | `525af59832007da0ac30d73ce559010e9f79ec55` |
| `.cursor/rules/code-style-consistency.mdc` | Derived mirror; generic style guidance. | `0ae753b4c2f8ae2fecd33080fe482bb28e27c7b5` |
| `.cursor/rules/git-workflow.mdc` | Derived mirror; the `--no-verify` bar's owner is `CLAUDE.md` §Vendor-data integrity gate, and its enforcement moved to `scripts/guard_shell_command.py`. | `5e66fd18506377e1eec7aa936c497ec7ffdc7a76` |
| `.cursor/rules/locked-params.mdc` | Derived mirror; owner `CLAUDE.md` §Protection / §Strategy Reference and `core/dd_protection.py`. | `1e355ec9320109957a248307680f4ea5c1d62cfb` |
| `.cursor/rules/search-ltm.mdc` | Derived mirror; owner `CLAUDE.md` §Architecture ("an empty `rg` result is not evidence of no prior work") and `.rgignore`. | `208759224db2754e6c54c7138d9a83702c5f881f` |
| `.cursor/rules/session-discipline.mdc` | Derived mirror. Every clause named its own surviving owner; the `repo_retrieve.py` **`ASSISTIVE-ONLY` suspension** it carried is owned by [`Q-XMEM-1`](../briefs/Q-XMEM-1-cross-surface-memory-sidecar-pilot.md) §Limb B and the [Limb-B RESULTS](../../lab/analysis/harvest/limb_b_remeasure_2026-08/RESULTS.md), and is enforced in code at `scripts/check_advisor_dedup.py`. **The suspension stays in force**; only the mirror is gone. | `37bf9293e0ef07fbc7247ab558096727a5554a91` |
| `.cursor/rules/session-log.mdc` | Derived mirror; owner `docs/SESSIONS.md` living header + `docs/operational_rules.md` §7. | `41a98a50fffaa7c49bd0149de20e411c6fc465df` |
| `.cursorignore` | Cursor AI access-block list (venv/cache noise). No surviving surface reads it. | `d94bcdfab156f62fd57ba24a7afc4984fc0278eb` |
| `.cursorindexingignore` | Byte-identical content to `.rgignore`, which survives as sole owner of the cold-corpus exclusion. | `ef99cf49aacf63c502c349eda52d7c12669db8cb` |
| `scripts/dispatch_cursor.ps1` | Cursor CLI wrapper. `scripts/dispatch_claude.ps1` survives; `agent_handoff.py --provider` is now `claude`-only. Its `-Slug`/`-Copy`/`-ForceCommands` options retired with it (`--copy` remains on the runner). | `bbc81e04a55cd2f1c068b5975ae34305f27fa3ca` |
| `scripts/test_dispatch_cursor.ps1` | PowerShell wrapper check for the above. | `f4b3884965713286951c947077ecfef3f381f386` |
| `.github/workflows/notify-cursor.yml` | Auto-`@cursor` ping, already `if: false` + `workflow_dispatch`-only since the 2026-09-04 addendum. Its revert trigger ("operator asks to turn the ping back on") is **explicitly retired, not carried** — unreachable once the lane is gone. Replaced by a test pinning the file's absence. | `3852cfd023bacf4e3a8d344e0e716e64a7e127a4` |
| `tests/scripts/test_after_file_edit_cursor_hook.py` | Tested the deleted adapter; retired with it, not skipped. Coverage of the surviving hooks it exercised stays with `tests/` for `lock_event_hook` / `sync_skills_hook`. | `7adcad48906bfe7a6d5916e97c943412e1e925ea` |


## 2026-09-08 ox-alpha lens retirement

Operator direction 2026-09-08: delete the ox-alpha ADR; the stealth ox-alpha
adversarial-lens lane is no longer in use. Authorization to invoke that model,
its use-ledger and revert triggers are **retired**, not passed. Historical notices
and consult records remain evidence of past asks; they confer no standing lane.
No successor owner — do not reopen without a fresh ADR and operator GO.

| Removed path | Disposition / current owner | Immutable body |
|---|---|---|
| `docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md` | Retired unused stealth-model adversarial-lens scope; no current owner. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/07fecc6cceb8609fdd5feae78ae67779727ed5c6/docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md); `git show 07fecc6cceb8609fdd5feae78ae67779727ed5c6:docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md`; blob `5b9173fc928886b5ad5253dc714fdd70e1807f74` |


## 2026-09-08 citation pilot

| Removed path | Disposition / current owner | Immutable body |
|---|---|---|
| `docs/adr/2026-08-19-rule-1-citation-not-three-meanings.md` | Completed citation episode; Rule 1 extension, conditional script commission and distinct Anchor owners now in [regime gate](../methodology/regime_robustness_gate.md#cross-references). No risk/Pine change. | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-19-rule-1-citation-not-three-meanings.md`; blob `741138c3a23cba4866bc0ab8ff334def6f7423d8` |

## 2026-09-08 persona parents

All three persona ADRs and both cold bodies are removed. The operator reaffirmed
complete removal on 2026-09-08. The whole-panel, eight-seat and nine-seat review
windows, November 8 backstops and persona-restoration triggers are **retired**, not
passed or awaiting reactivation. Generic controls remain with their existing
owners; [independent review](../../scripts/README.md#independent-review) has no
persona dependency. Historical retrieval creates no standing role or obligation.

| Removed path | Disposition | Immutable body |
|---|---|---|
| `docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` | Superseded hot stub | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`; blob `6fcbf5aaff113eff620782bb5bb16ae5fffbeeeb` |
| `docs/adr/2026-08-21-persona-hierarchy-front-office-only.md` | Superseded hot stub | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-21-persona-hierarchy-front-office-only.md`; blob `5005dcc6403541988d7cc10e4e0279f6cc233bad` |
| `docs/ltm/adr/2026-08-19-loop-persona-hierarchy-review-panel.md` | Historical full body; persona lifecycle retired | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/ltm/adr/2026-08-19-loop-persona-hierarchy-review-panel.md`; blob `f17477ef6753cc3c1c05b2dd34678b88e0fe9f72` |
| `docs/ltm/adr/2026-08-21-persona-hierarchy-front-office-only.md` | Historical full body; persona lifecycle retired | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/ltm/adr/2026-08-21-persona-hierarchy-front-office-only.md`; blob `eecf6891efaa04e7902e159743220837e335602a` |
| `docs/adr/2026-08-31-persona-hierarchy-full-retirement.md` | Completed retirement episode; all persona reviews/restoration triggers retired by operator clarification. | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-31-persona-hierarchy-full-retirement.md`; blob `d1f665ed458befd78f01146e8ae085b49998aeb0` |

## 2026-09-08 governance consolidation

The [five-root charter](2026-07-16-root-doc-charter-dedup.md) retains the distinct
ownership rationale. [Rule 7](../operational_rules.md#7-one-canonical-owner-per-fact-every-other-mention-links-or-is-a-labeled-mirror),
the [STATE queue](../../STATE.md#operator-queue--strictly-ordered-5-live-items),
the [SESSIONS header](../SESSIONS.md), and the
[gate operating contract](../../scripts/README.md#gate-composition-and-admission)
own current procedure. Historical bodies below do not reinstate superseded procedure.

| Removed path | Disposition / current owner | Immutable body |
|---|---|---|
| `docs/adr/2026-06-30-state-md-role-reduction.md` | STATE role/snapshot exclusions, assistive-memory boundary, date-field contract and role-specific incident/dormant-thread protection retained in Rule 7 and current readers. Exact-two-header requirement superseded; redundant programme/quarterly document-maintenance review retired, not passed. No new memory store or STATE rename commissioned. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-06-30-state-md-role-reduction.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-06-30-state-md-role-reduction.md`; blob `d287d3e2ae3f72f3299368d701298a753fd3ffd8` |
| `docs/adr/2026-08-07-w5-governance-diet.md` | Manifest/runner, selector/reachability/admission and structural-M1 versus audit distinction retained in scripts guide. A–D classes/~40-word targets retired; queue-copy/stub requirements superseded September 6. H6 discharged August 23. Brief-checker unification and 26-letter exhaustion remain unresolved in scripts/SESSIONS owners. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-07-w5-governance-diet.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-07-w5-governance-diet.md`; blob `3b8d62437cd9385d69e58292a1da4620f635ca20` |
| `docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md` | ≤5 concurrency cap, dependency/operator order and no automatic replacement/channel/GO remain with STATE. November 8 attention/order review and failure condition migrate to charter plus STATE pointer; not discharged. Item-5 license already owned by [M1](2026-07-22-c1-venue-native-monitoring-maturity.md#addendum-2026-08-24--test-strategy-licensed-for-item-5-dated-08-24); arm authority unchanged. Earlier queue elections are completed history. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-09-survive-bound-is-the-queue-cap.md`; blob `cb12d7669e587676b1ab6111615d0f889347c227` |

## 2026-09-08 candidate-pipeline consolidation

Candidate fields, freezes, campaign authority and confirm-family rules remain in
[candidate contract](2026-08-30-candidate-contract.md); ordering, reachability and
confirm verdicts remain in [evaluation order](2026-08-30-evaluation-order.md).
The useful first November 8 reviews and implementation/adoption debts migrate to
those retained owners and STATE. Redundant recurring reviews of six documents are
retired, not passed. Existing channel clocks/counters and operator authority stand.

| Removed path | Disposition / current owner | Immutable body |
|---|---|---|
| `docs/adr/2026-08-30-operator-approvals-campaign-envelope.md` | [Campaign authority](2026-08-30-candidate-contract.md#campaign-authority) and [confirm family](2026-08-30-candidate-contract.md#confirm-family); inclusive probe accounting and fresh-campaign/fresh-holdout discipline retained. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-operator-approvals-campaign-envelope.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-30-operator-approvals-campaign-envelope.md`; blob `db95d49d9740515505b22e65f714d1de030d8638` |
| `docs/adr/2026-08-30-tradeable-reachable-gate.md` | [Reachability](2026-08-30-evaluation-order.md#reachability); distinct cost owners, scoped exceptions and immediate authority-change review retained. Stale EM-screen G3 pointer corrected. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-tradeable-reachable-gate.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-30-tradeable-reachable-gate.md`; blob `497340d65954ff4620ddb3dc82cd7189a7ca0af5` |
| `docs/adr/2026-08-30-terminal-taxonomy.md` | [Confirm verdicts](2026-08-30-evaluation-order.md#confirm-verdicts), plus full [expression ladder/register routing](2026-06-14-rejected-candidate-patterns.md#expression-ladder-and-register-routing); parser and ordinal enforcement remain incomplete. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-terminal-taxonomy.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-30-terminal-taxonomy.md`; blob `81bf4f0d99d309115cfa51911a2c6b94416c78ea` |
| `docs/adr/2026-08-30-channel-liveness-gate.md` | [Cross-channel contract and actual owners](../methodology/strategy_harvest.md#channel-liveness-contract); five reconciliations and conditional first post-firing review remain owed. No counter or channel consequence was executed. | [Full body](https://github.com/Joshua-Asante/first-passage/blob/4fb2b88f3b7d56d77463c43ba45c87ffadff6a31/docs/adr/2026-08-30-channel-liveness-gate.md); `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-30-channel-liveness-gate.md`; blob `e58434c361b2c03e890efa202e2b519c0b9e73cd` |

## Earlier removals

One line per pruned ADR — the decision's *current consequence* survives here; the
full body is retrievable via `git show pre-prune-2026-08-08:docs/adr/<file>`
in the **private archive** — that tag is not on this public clone
(`git log --follow -- docs/adr/<file>` is the fallback here)
(ADR [`2026-08-08-great-prune`](2026-08-08-great-prune.md) §3 class 4; retention
test R1–R5). Revival of any tombstoned decision requires fresh pre-registration
under the standing chain — never a lookup. Rows are grouped by disposition,
newest first. Obligations that died with a carrier are recorded in the
[2026-08-08 audit note](../notes/audits/programme-audit/2026-08-08-quarterly-audit.md) §2.

| Date | ADR | Consequence now | Body |
|---|---|---|---|
| 2026-07-03 | hardcore-p1-automated-execution-gate | **Tombstoned by operator ruling 2026-08-08.** §4 could only ever return AMBIGUOUS-OPERABLE (E1 unattempted — no strategy-signal fill has ever occurred) and its §6 budget clock was pegged to "90 days after R6 issues a GO", which R6's spent NO-GO makes unreachable | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p1-automated-execution-gate.md` |
| 2026-07-03 | hardcore-p2-edge-transfer-gate | **MOOT** — §4 already fired and was operator-ratified terminal 2026-07-06 ("§4 FALSIFIED-on-venue"); the Pepperstone measurement basis retired 2026-08-02, so no re-run is possible | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p2-edge-transfer-gate.md` |
| 2026-07-03 | hardcore-p3-compounding-ceiling-amendment | **Tombstoned by operator ruling 2026-08-08.** ⚠ Kill-D's per-firm `M_f` payout-extraction arithmetic was **never computed** and had been owed since its own 2026-07-06 hard date; the "RESOLVED" record was a triage label, not the work. Re-enters as a fresh dated packet if wanted — not as a revived ADR | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p3-compounding-ceiling-amendment.md` |
| 2026-07-03 | hardcore-p4-tail-survival-gate | **UNFALSIFIABLE** — both limbs dark (limb 1 dormant pending a live venue; limb 2 orphaned when the decompound HOLD's limb-2 was struck 2026-08-03); §5 forbids forking a second process | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p4-tail-survival-gate.md` |
| 2026-07-03 | hardcore-p5-source-truth-rail-gate | **UNFALSIFIABLE** — §6 struck its own calendar backstop and pegged the gate to "before R6 issues a GO", which a spent NO-GO one-shot can never satisfy | `git show pre-prune-2026-08-08:docs/adr/2026-07-03-hardcore-p5-source-truth-rail-gate.md` |
| 2026-08-02 | striker-tradeify-funded-phase-descope | Withdrawn, never ratified; wider whole-venue de-scope elected 2026-08-04 (live ADR) | `git show pre-prune-2026-08-08:docs/adr/2026-08-02-striker-tradeify-funded-phase-descope.md` |
| 2026-06-22 | nas100-orb-5th-leg | Withdrawn same-day: native TV-CSV falsified the offline harness (fills ~5.6× optimistic); no 5th leg | `git show pre-prune-2026-08-08:docs/adr/2026-06-22-nas100-orb-5th-leg.md` |
| 2026-06-12 | rnd-feed-instrument-class-split | Superseded by TV-CSV canonical-feed policy; CME futures TV exports are the live feed | `git show pre-prune-2026-08-08:docs/adr/2026-06-12-rnd-feed-instrument-class-split.md` |
| 2026-05-14 | allocation-refresh | Superseded by 2026-05-23 allocation-refresh-2 (lock lineage lives in CLAUDE.md §Strategy Reference) | `git show pre-prune-2026-08-08:docs/adr/2026-05-14-allocation-refresh.md` |
| 2026-05-11 | objective-map-section-4-tighten-falsifier | Retired with the Objective Map surface (challenge era closed) | `git show pre-prune-2026-08-08:docs/adr/2026-05-11-objective-map-section-4-tighten-falsifier.md` |

## 2026-09-08 brief and skill governance

The current [skill lifecycle](../../scripts/README.md#skill-lifecycle) and
[brief checker ownership](../../scripts/README.md#brief-checker-ownership) retain
the effective contracts, including the operator's explicit reviewed-release
policy approved 2026-09-06 and recorded 2026-09-08. That policy permits no actual
release by itself. The complete final source at `f55dcb7` includes the release
addendum; prior June/August findings retain their original `4fb2b88` source.
The June 4 quarterly expected-10-skills / old-name
reread is retired, not passed; live gates and failure tests remain. The three-skill
migration plan was already superseded by the August 29 correction and existing
GSUB-1 dispositions. The canon ruling's initial resolution is historical; its
type-aware contract remains in brief-authoring. These removals confer no authority.

| Removed path | Disposition / current owner | Immutable body |
|---|---|---|
| `docs/adr/2026-06-04-methodology-skills-under-vc.md` | Source/deploy/gate contract consolidated in [Skill lifecycle](../../scripts/README.md#skill-lifecycle); redundant census retired. | Final full body: `git show f55dcb788cacbaa9258f5358fb29c6a4a0ff5c72:docs/adr/2026-06-04-methodology-skills-under-vc.md`; blob `b09157fc0a7258cc8269d12b6fdc69c47ddf1803`. Prior history: `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-06-04-methodology-skills-under-vc.md`; blob `a81454bff43ca72c5db4ab1918e3b3b52798b1af` |
| `docs/adr/2026-08-09-check-brief-canon-ruling.md` | Canonical/subset and distinct type contracts consolidated in [brief-authoring](../../.claude/skills/brief-authoring/SKILL.md#checker-ownership); original resolution historical. | `git show 4fb2b88f3b7d56d77463c43ba45c87ffadff6a31:docs/adr/2026-08-09-check-brief-canon-ruling.md`; blob `f903867b49debb62a88e0b51c60c5098286a7ebb` |
