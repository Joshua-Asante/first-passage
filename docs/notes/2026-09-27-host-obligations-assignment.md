# Production qualification host: OF-1..OF-7 assignment (RC-5), client seed-view assignment (RC-4) and host specification (2026-09-27)

**Status:** RETURNED for coordinator acceptance. **PROPOSED throughout.** This is the return of [handoff H7](../briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md#h7--production-qualification-host-specification-and-of-assignment) (card lines 352-385). It proposes the RC-4/RC-5 assignment text and a production-class host and credential specification. It edits no owner document, changes no code, rents no host, creates no credential and generates no key. The assignment becomes a record only when the coordinator writes it into the [execution-slices ledger](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27), as that entry says it will ("The coordinator records it here when handoff H7 returns"). §E gives the proposed ledger text.

**Executor:** subagent (Claude Code, Opus 5.5), branch `claude/clever-wozniak-bx0u95`, dispatch revision `521d8f2`. At the fix round HEAD is `c991d2d`, one commit later, which changes only `.claude/skills/task-routing/SKILL.md` (`git diff --stat 521d8f2 HEAD`), so no anchor below moves. All `file:line` anchors are at `521d8f2` unless prefixed with another commit. The #519 returns are cited as `8c15f18:<path>:<line>`.

**Authority for this work.** The S5 staged-gates ruling of 2026-09-27 approves "Assigning seed-view and host-check owners now, with implementation and attestations due at their specified later gates" ([ledger](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#operator-ruling--s5-staged-gates-approved-part-a-only-rule-scope-hold-kept-2026-09-27), `2026-09-18-full-e1-execution-slices.md:837`). The 2026-09-26 ruling directs "Assign seed-view implementation and host attestations to their specified gates" (same file, the 2026-09-26 entry). This seat does not choose owners; it proposes them (card line 360). The coordinator records the assignment under the 2026-09-27 ruling. The 2026-09-26 ruling entry leaves S5 draft §6 Q12 "open for the coordinator's owner-text and RC-5 work" (ledger `:810`; S5 draft `:386`, `:404`), which is the authority for the coordinator resolving Q12 in §A.1. The ruling names no assigner for the RC-4 **slice**, and the S5 draft says that slice is one "the operator names" (`:363`); §B.2 therefore treats the slice placement as an operator choice.

**Label note.** "RC-4" and "RC-5" here are the S5 release conditions of the [S5 decision draft §5](2026-09-26-s5-decision-draft.md#5-s5-release-conditions) (`:385-386`). They are **not** the replay spec's RC-4 (fill model) that the #519 lifecycle note cites (`8c15f18:docs/notes/2026-09-26-orb-lifecycle-evidence.md:29,42`). B-1..B-5 are the contract-delta audit's §5.1 rows. OF-1..OF-7 are the S5 draft §1.3 rows. "T11" has two unrelated meanings in the sources, so this note writes **ADR-T11** for the admission ADR §2a row "T11 initial effective activation (TB-B10, TB-O1 procedure)" (`2026-09-12-tradeify-book-protection-instance-admission.md:100`) and its operator host attestations, and **checklist T11** for "T11 — Production-class qualification service ready" (`2026-09-20-tradeify-deployment-checklist.md:239`).

## Answer in brief

1. **Q12 is resolved by adopting the stricter reading.** Every OF-1..OF-7 is read at host provisioning, before any production-authority release and after any access change. In addition, OF-5 is read before any arm and at each session GO, OF-6 at TB-I3, and OF-7 before F1 admission. This is the S5 draft's §1.5(a) text (`2026-09-26-s5-decision-draft.md:134`). It contains every gate of the §1.3 table (`:96-102`), so adopting it **only adds gates** and removes none (§A.1). It is a **coordinator assignment** under the 2026-09-27 ruling, not an operator ruling.
2. **Every OF is verified by an operator-attended read.** The operator records it in a two-part record: a private raw transcript, and a public attestation that carries only booleans, octal modes, role names, enumerated codes, dates and hashes, with no free-text field (§A.3). Three OFs cannot be *fully* established by a point-in-time read. They are returned as contract questions CQ-1..CQ-3 (§D.1), under the card's stop condition (card line 375). The rest of the card was completed, because those questions block no assignment.
3. **RC-4: recommend a qualification slice, not TB-F1.** The client plan-view seed change (digests only) goes in one qualification slice together with the K3 build. It is owned by the execution-slices ledger (the qualification coordinator), dispatched after S5 acceptance and landed before S8/T06 dispatch (§B). This is a **recommendation for the operator**: the S5 draft has the operator name the slice and places K3 "with TB-F1" (`:363`), so both the placement and moving K3 out of TB-F1 are operator choices (§D.3). The RC-4 assignment counts as made only once the operator accepts the placement. It depends on the full-E1 spec §2.2a amendment (S5 draft §1.5(d), `:144-146`), which RC-2 applies. This note does not apply it. §B.4 gives the F1 admission-check text.
4. **The host specification** (§C) restates what the S2-accepted boundary relies on: Ubuntu 24.04 x86_64, cgroup v2 with `cgroup.kill` and `memory.peak`, systemd transient units, a qexec polkit rule, BOOTTIME timers and Docker Engine. It covers the four principals plus the administrator and the host-level `operator` UID, file-based `0400` keys, enrollment inputs, K3 salt custody and installed-identity checks. It separates TEST_ONLY from production, and names no provider and no price. Spend is an **operator decision at CP-8**.

**Not granted:** no RC-4/RC-5 assignment is made by this note (the coordinator records it). No owner text is applied, including §1.5(a) and §1.5(d) (RC-2 governs). Nothing here provisions, rents or spends on a host, creates a credential or key, enrolls a release, or installs anything. There is no S5 release, dispatch or execution; no F1, CP-6 or CP-8 decision; no production, arm, deployment or live authority; and no account access. The attestation schema and record paths below are proposals.

---

## A. RC-5: OF-1..OF-7 assignment

### A.1 Q12 resolved to the stricter reading (coordinator assignment)

S5 draft §6 Q12 (`:404`) records that the §1.3 **When** column and the §1.5(a) proposed owner text give different gate sets for OF-5..OF-7. §1.6 (`:150`) and RC-5 (`:386`, "all before any production-authority release") read the same way as §1.5(a).

| OF | §1.3 **When** (`:96-102`) | §1.5(a) (`:134`) = adopted set | Added by adoption |
|---|---|---|---|
| OF-1..OF-4 | provisioning; before any production-authority release; after any access change | the same | none |
| OF-5 | before any arm; each session GO | provisioning; before any production-authority release; after any access change; **plus** before any arm and at each session GO | provisioning, release, access change |
| OF-6 | TB-I3 | provisioning; release; access change; **plus** TB-I3 | provisioning, release, access change |
| OF-7 | before F1 admission | provisioning; release; access change; **plus** before F1 admission | provisioning, release, access change |

**This only adds gates.** For every OF, the §1.3 gate set is a subset of the adopted set. No gate is removed or moved later. Under the 2026-09-27 ruling this is a coordinator assignment ("Assigning seed-view and host-check owners now…"). It is not an operator ruling. No further ruling is needed to add gates, because the 2026-09-26 ruling entry leaves Q12 "open for the coordinator's owner-text and RC-5 work" (ledger `:810`; S5 draft `:404`: "Open for the coordinator's owner-text or RC-5 work"). The RC-2 owner-text review still has to apply §1.5(a) to boundary spec §3.1. #519 names §3.1 "the natural owner" (`8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md:360`).

**Gate definitions (PROPOSED labels, used in §A.2):**
- **G-PROV** — provisioning of the production qualification host, taken at **CP-8** ([checklist addendum §4](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step), `2026-09-20-tradeify-deployment-checklist.md:496`), before any `OPERATOR`-class enrollment on it.
- **G-REL** — before any production-authority release. That means before installing or activating any release, instance document, trust domain or key enrollment whose `authority_class` is `OPERATOR` on that host. The code already knows exactly two classes, `TEST_ONLY` and `OPERATOR` (`ops/c1_rail/qualification/execution/release.py:25`, `keys.py:16`, `credentials.py:28`, `admission.py:51`). G-REL also covers CP-8's second half, "admit the production attempt after OF attestation" (`checklist:496`).
- **G-ACC** — after any access change (triggers in §A.2), before the next use of any production authority on the affected host or environment.
- **G-ARM** (OF-5 only) — before any `c1_rail_arm.py --arm`, and at each per-session GO. The per-session GO is standing posture: "Every armed session needs its own GO" (AGENTS.md, Live-execution posture), so each session gets its own OF-5 read. Supporting, for commissioning and the first attended release only: under [incident ADR §A11.2](../adr/2026-09-17-bounded-platform-protection-incident-contract.md#a112--operator-ruling-no-same-session-restart-of-automation-after-an-incident-2026-09-27), "during commissioning and the first attended release, an incident ends automated trading for that session" (`:381`); its scope for later releases "is not ruled" (`:384`).
- **G-TBI3** (OF-6 only) — at TB-I3, the build and acceptance of the GO validator and arm interlock ([admission ADR §2b](../adr/2026-09-12-tradeify-book-protection-instance-admission.md), `:105`).
- **G-F1** (OF-7 only) — before F1 admission of the production attempt, which means before the transaction that binds the budget and generates the salt (S5 draft §1.4, `:117-118`).

**Validity rule (PROPOSED).** An attestation satisfies a gate only if no re-verification trigger for that OF occurred between the read and the gate. A trigger voids every earlier attestation of that OF for later gates. Whether an attestation also goes stale by age alone is **not specified** by any owner; it is operator question Q-5 (§D.2).

### A.2 Assignment table

Verifier and recorder are the same in every row. The **operator** performs the attended read and writes the private transcript. The public attestation is written by the operator, or transcribed by the coordinator from the operator's relayed values in the same session and confirmed in writing by the operator. The **coordinator** checks the record for completeness only: every field present, the transcript hash present, the gate named. The coordinator then records it in the ledger. The attestation is **operator-attested, not machine-verified**, the same class as the ADR-T11 host attestations (admission ADR §2b, `:105`: "attested by the operator's host read, not machine-verified"). An agent never performs these reads on the production host, because an agent able to do so would itself falsify OF-1/OF-2.

| OF | Fact (S5 draft `:96-102`, abbreviated) | Attended read (S5 draft method, plus this note's additions marked +) | Gates (adopted set) | Public record fields (§A.3; no secrets) | Re-verification triggers |
|---|---|---|---|---|---|
| **OF-1** | No agent-hosting account or environment, including the operator's workstation account when agents run under it, can use administrator, `sudo`, `docker`-group or Docker-socket access on the production host | Host: `getent group sudo docker`; `stat /var/run/docker.sock`; `sudo -l -U <login>` for each login. Workstation: no host SSH key, token or agent-forwarded credential reachable by an agent's account. + Enumerate the agent environments against the pinned list (CQ-1) | G-PROV, G-REL, G-ACC | `all_host_logins_enumerated` (bool, must be true); `login_beyond_roles_has_admin_sudo_or_docker` (bool, must be false); `docker_group_member_roles` (role names; expected `["qexec"]`, README:95-96); `docker_socket_owner_role`, `docker_socket_group_role`, `docker_socket_mode` (octal); `agent_environments_checked` (list of environment **class** names from CQ-1); `host_admin_credential_reachable_from_agent_environment` (bool, must be false) | Any account, group, sudoers or sudoers.d change on the host; Docker install, upgrade or socket-permission change; host rebuild or reprovision; a new agent harness, agent OS account or cloud agent environment; any change on an agent-hosting workstation account to SSH keys, SSH agent or forwarding, credential helpers or remote-access tooling |
| **OF-2** | No agent can authenticate as `qexec`, `qg5`, `qseal` or the administrator; no polkit rule grants `manage-units` to an agent-reachable UID | `/etc/polkit-1/rules.d` listing; `authorized_keys` per principal. + Account lock and shell state per principal. The test harness creates locked, home-less, non-login accounts (README:95-98). + The host `operator` UID (Q-1) | G-PROV, G-REL, G-ACC | per principal (`qclient`, `qexec`, `qg5`, `qseal`, `administrator`; `operator` if Q-1 is adopted): `auth_locked` (bool), `authorized_keys_present` (bool), `login_shell` (bool); `polkit_manage_units_rules` (list of `{subject_role, rule_sha256}`; expected one rule, subject `qexec`, `campaign_host.py:88-92`); `polkit_rule_grants_agent_reachable_uid` (bool, must be false) | Any change under `/etc/polkit-1/rules.d`; any principal creation, deletion, UID change or authentication change; a polkit or systemd package upgrade; host rebuild |
| **OF-3** | Execution, result, seal and operator-VOID private keys are unreadable by agent-reachable UIDs, and absent from every worktree, every CI secret visible to an agent-editable workflow and every agent-reachable store | Key-path owner and mode read; `gh secret list` compared against the workflow files; worktree scan by filename, not content. + The code-level custody rule: owner = the signing process's euid, mode `0400`, one link, protected ancestors (`credentials.py:18-26`) | G-PROV, G-REL, G-ACC | per on-host key class (`execution`→`qexec`, `result`→`qg5`, `seal`→`qseal`): `owner_role`, `mode` (octal, expected `0400`), `single_link` (bool, must be true), `ancestors_protected` (bool), `public_fingerprint_sha256`; per off-host key class (`operator_void`, `freeze`/F1 approval, GO if E3): `custody: "off-host, operator"` and `public_fingerprint_sha256`; `ci_secret_holds_key_material` (bool, must be false); `all_worktree_roots_scanned` (bool, must be true); `key_filename_found_in_worktree` (bool, must be false); `agent_stores_checked` (class names, CQ-1) | Any key generation, rotation, enrollment or revocation; any new GitHub Actions secret (repository, environment or organization) or new workflow; a new worktree root or agent environment; host rebuild |
| **OF-4** | Key-enrollment and trust-domain inputs are writable only by the operator | Owner and mode of the enrollment files on the host. + The inputs listed in §C.4 | G-PROV, G-REL, G-ACC | per input class (release-approval registry, trust domain, release manifest plus approval, instance document, campaign-host enrollment, polkit rule file, host configuration): `owner_role` (expected `administrator`), `mode`, `group_or_other_writable` (bool, must be false), `sha256` | Any enrollment, release install, trust-domain change or instance-document change; host rebuild |
| **OF-5** | No agent holds rail-host deploy credentials (Fly token or flyctl session), write access to the rail `/data` volume, or broker credentials | Operator reads the agent environments' credential stores and the Fly access list | G-PROV, G-REL, G-ACC, **G-ARM** (before any arm; each session GO) | `scope: "agent-environments+rail-host"`; `agent_environments_checked` (class names, CQ-1); `rail_deploy_credential_in_agent_environment` (bool, must be false); `rail_data_volume_writable_by_agent` (bool, must be false); `broker_credential_in_agent_environment` (bool, must be false); `rail_deploy_members_are_operator_only` (bool, must be true). No organization, app, machine or account identifiers, and no membership count | Any Fly membership or token change; any broker credential issue or rotation; a new agent environment or cloud environment secret; a rail host redeploy by a new path; each arm; each session GO |
| **OF-6** | If E3 is adopted, the operator GO signing key is off-host and never loaded where an agent runs | Key custody record. + Current absence from every agent environment (CQ-2) | G-PROV, G-REL, G-ACC, **G-TBI3** | `e3_adopted` (bool); when false, `status: NOT_APPLICABLE` (B-4 is then "Held by OF-5/OF-6 until TB-I3", S5 draft `:87`, with the ADR-T11 checks owed at TB-I3, S5 draft `:78` and audit §5.1 B-4 row `:176`); when true: `go_key_custody: "off-host, operator"`, `go_public_fingerprint_sha256`, `present_in_agent_environment` (bool, must be false), `custody_record_sha256` | E3 adoption (an ADR §2b/§3 revision, audit row E3); any GO key generation, rotation or device change; a new agent environment; TB-I3 |
| **OF-7** | Before public reveal, the seed salt is readable only by the trusted administrator, `qexec`, the worker's read-only input and `qg5`'s private adjudication access | Mode and ownership of the salt row and objects; negative client-fetch test (S5 draft §1.6). + Before F1 admission the salt does not yet exist, so the read covers **custody configuration** only (CQ-3) | G-PROV, G-REL, G-ACC, **G-F1** | `data_tree_owner_role` (expected `qexec`), `data_tree_mode` (expected `0700`, `role_policy.py:18`); `installed_release_sha256` equals the release accepted with the RC-4/K3 negative client cases (§B.4); `client_plan_view_mode` (expected `client_view_digests_only`); `g5_private_salt_route` (Q8 choice, role-restricted bool); `worker_input_readonly_not_client_readable` (bool); `data_tree_backups_agent_reachable` (bool, must be false; Q-3) | Any release install (G-REL); any change to the data or scratch tree bindings; a qg5 route change; backup or snapshot configuration change; host rebuild |

### A.3 Where the record lands (PROPOSED)

Two parts per attended read. No record may contain secrets, private key bytes, usernames other than role names, IP addresses or host names, account identifiers, or P&L (AGENTS.md, Public-clone posture).

1. **Private raw transcript.** The command outputs exactly as read, which include usernames, UIDs and possibly addresses. Custody: the operator, **outside every repository checkout and worktree**. It is archived in `first-passage-archive`, per the [.gitignore](../../.gitignore) note that "Ignoring is not archiving: a pinned file still goes to first-passage-archive per M-41". The exact private location is the operator's choice (Q-4). The transcript is never committed or quoted, and never passed to an external service.
2. **Public attestation** (PROPOSED path and schema): `docs/notes/qualification_host/attestations/<YYYY-MM-DD>-<gate>.json`. The directory does not exist today. Canonical JSON. Schema `qualification_host_of_attestation/v1` (PROPOSED name):

```json
{
  "schema": "qualification_host_of_attestation/v1",
  "host_role": "production-qualification-host",
  "host_identity_sha256": "<SHA-256 over the app-specific machine ID, see §C.6>",
  "installed_release_sha256": "<release manifest digest, or null before any install>",
  "gate": "G-PROV | G-REL | G-ACC | G-ARM | G-TBI3 | G-F1",
  "trigger_codes": ["<codes from the enumeration below, for G-ACC; else null>"],
  "read_date_utc": "YYYY-MM-DD",
  "e3_adopted": false,
  "facts": {
    "OF-1": {"status": "VERIFIED | NOT_VERIFIED | NOT_APPLICABLE", "checks": {"...": "fields from §A.2"}},
    "OF-2": {}, "OF-3": {}, "OF-4": {}, "OF-5": {}, "OF-6": {}, "OF-7": {}
  },
  "raw_transcript_sha256": "<sha256 of the private transcript>",
  "attested_by": "operator",
  "operator_confirms_reads_as_recorded": true
}
```

- **No free-text field.** Every value is a boolean, an octal mode, a role name, an enumerated code (status, gate, trigger code, CQ-1 environment class), a date or a hash. Anything the operator wants to say in words goes into the private transcript, whose SHA-256 the attestation binds.
- **Trigger codes (PROPOSED enumeration, one per trigger class in the §A.2 column):** `HOST_ACCOUNT_OR_GROUP_CHANGE`, `SUDOERS_CHANGE`, `DOCKER_INSTALL_UPGRADE_OR_SOCKET_CHANGE`, `POLKIT_RULE_CHANGE`, `PRINCIPAL_CHANGE`, `POLKIT_OR_SYSTEMD_UPGRADE`, `KEY_LIFECYCLE_EVENT`, `CI_SECRET_OR_WORKFLOW_CHANGE`, `WORKTREE_ROOT_ADDED`, `AGENT_ENVIRONMENT_CHANGE`, `WORKSTATION_REMOTE_ACCESS_CHANGE`, `ENROLLMENT_RELEASE_TRUST_OR_INSTANCE_CHANGE`, `RAIL_PLATFORM_ACCESS_CHANGE`, `BROKER_CREDENTIAL_CHANGE`, `RAIL_REDEPLOY_NEW_PATH`, `E3_ADOPTION`, `GO_KEY_CHANGE`, `DATA_OR_SCRATCH_BINDING_CHANGE`, `G5_ROUTE_CHANGE`, `BACKUP_OR_SNAPSHOT_CHANGE`, `HOST_REBUILD`. A change that fits no code is recorded as the nearest code plus a private-transcript entry, and the missing code is returned to the coordinator.
- **Public**, because of the rule above. The operator may instead keep the whole record private and commit only its SHA-256 in the ledger. That is Q-4, and it changes no gate. `host_identity_sha256` is a stable identifier of the host across every attestation, so publishing it makes attestations of one host linkable to one another; whether that is acceptable is also part of Q-4.
- A `NOT_VERIFIED` fact is reported as "enforcement not established", never as assumed (S5 draft `:104`). A gate whose required OF is not `VERIFIED` (or `NOT_APPLICABLE` for OF-6 without E3) does not pass.
- **Ledger link.** The coordinator adds one line per attestation to the execution-slices ledger (for G-PROV, G-REL, G-ACC and G-F1) or to the arm evidence of the session concerned (G-ARM). The line holds the path, the SHA-256 and the gate. Whether TB-I3's `--arm` consumes the OF-5 attestation digest as a typed input is a TB-I3 design question, not granted here (Q-6).
- **Owner of the definitions:** boundary spec §3.1 once RC-2 applies §1.5(a). The attestation files are evidence records, not owners (Rule 7).

---

## B. RC-4: owner and slice for the client plan-view seed change

### B.1 The change, as the code stands at HEAD

- The `client` role may call `FETCH_PLAN_CHUNK` (`ops/c1_rail/qualification/execution/campaign_protocol.py:90-95`, the `client` set at `:92`). The service routes that call to the store (`service.py:385-386`; diagnostic route `:486-489`).
- The store serves any slice of the whole stored plan object with `role='plan'` (`campaign_store.py:2409-2434`, query at `:2413`).
- The plan embeds seed-input records (`checkpoint_plan.py:222-233`) built by `seed_input`, which carries the root and the `seed` value (`seed_identity.py:29-41`, `'seed':seed` at `:39`, `root_rng_namespace` at `:32,36`).
- The client verifies the whole reassembled plan against the receipt's `plan_sha256` and `plan_byte_length` (`client.py:55-93`; digest at `:68`, check at `:92-93`). The store writes those receipt fields at `campaign_store.py:1154-1155` and `:2358-2359`.
- G5 reads the plan as a checkpoint member (`g5.py:671`), not through `FETCH_PLAN_CHUNK`, so the client-view change does not touch G5's route.

#519 recorded the same status as unmet and unassigned (`8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md:359`).

### B.2 Recommended owner and slice

**Recommendation (PROPOSED): one qualification slice, "K3/RC-4 — service salt and client plan view".**
- **Owner record:** the execution-slices ledger.
- **Owner role:** the qualification coordinator. A worker implements it under a frozen card, and the coordinator accepts it with Linux evidence, to the same standard as S2–S5.
- **Placement (operator choice; recommended):** dispatched after S5 acceptance and landed before S8/T06 dispatch. The S5 draft places K3 "with TB-F1 (before F1)" and says the client plan-view change "lands before F1 in a slice the operator names (§5 RC-4)" (`2026-09-26-s5-decision-draft.md:363`). This recommendation **changes** the draft's §4 placement by moving K3 out of TB-F1 into this slice, so both the slice and the K3 move need the operator's acceptance (§D.3). Until then the placement is a proposal.
- **Sequencing owner.** "Landed before S8/T06 dispatch" is a new precondition on T06/S8, whose checklist dependency today is "T01–T05 integrated at one identity" (`2026-09-20-tradeify-deployment-checklist.md:26`). The checklist addendum "governs **sequencing**" and leaves "the execution-slices ledger owns the S5 conditions" (`:392-393`). So a ledger entry alone does not change the addendum: once the operator accepts the placement, the addendum's sequencing (the T06/S8 prerequisite, or an owner note beside the H9 and D3 slice ordering in its §3 row, `:475`) must also record it.
- **Sequencing against the D3 recovery slice** is set by the coordinator. Both touch `campaign_store.py`, and K3's reveal rule consumes D3's closure definition (S5 draft §6 Q9, `:401`).
- **Scope:**
  - the client view (§1.5(d));
  - the receipt's `client_view_sha256` and `client_view_byte_length`;
  - the salted recipe `tb-s2-rng-v3` with service-generated salt, commitment and reveal (§1.5(c));
  - the §1.6 tests;
  - the service-side admission refusal of §B.4 item 1.

**Weighing S5 draft §6 Q10 (`:402`), TB-F1 against a qualification slice:**

| Consideration | Qualification slice before S8 | TB-F1 |
|---|---|---|
| When the view protects anything | Only once v3 exists. Under v2 the root is author-chosen and draft roots are already published (audit K3), so a digests-only view alone protects nothing. **Hence the recommendation couples it to K3 in the same slice** | Same dependency; TB-F1 would carry K3 too (S5 draft §4 places K3 "with TB-F1") |
| Rework of accepted machinery | T06/S8 (full synthetic E1) and checklist T11 accept the machinery that F1 later freezes (`checklist:288` lists T06/T10/T11 as T15 prerequisites). Landing before S8 means S8 exercises the changed receipt and plan view | A receipt and plan-transport change at TB-F1 lands **after** T06 and checklist T11 accepted the old interface. *Inference, not an owner rule:* no owner states that such a change forces re-acceptance of T06 or checklist T11; this note infers that the accepted interface would no longer be the one F1 freezes |
| CP-6 input | CP-6 already lists "RC-4 change landed" as an F1 freeze input (`checklist:494`), so the change must land before CP-6 in any case | TB-F1 is the freeze itself, so the change would land at the gate that is supposed to consume it |
| Nature of the owner | An engine and receipt-schema change under `ops/c1_rail/qualification/execution/`, which the execution-slices ledger owns | TB-F1 is a Track B freeze packet (umbrella). The umbrella body is closed, and §0.8 has rows O-1..O-9 only (no O-10 exists at HEAD; `2026-09-10-track-b-qualify-accepted-book-umbrella.md:98-112`) |
| Interaction with T05 | Whether T05's result or seal chain binds the **admission** receipt bytes is **UNVERIFIED**. At `6cf2732`, `campaign_result.py` binds per-checkpoint `receipt_sha256` (`:172,194`), which this read did not trace to the admission receipt. The coordinator checks this at dispatch; if it does bind them, the slice precedes H9's R1 | — |

**Recommendation:** the qualification slice. Q10's second half (does the client-view digest join the admission receipt beside `plan_sha256`?) is answered **yes** by the §1.5(d) text itself ("The admission receipt binds the client view's own digest and byte length beside the canonical plan's", `:146`). The recommendation adopts that. **The slice placement is an operator decision** (§D.3): the operator accepts this recommendation, including moving K3 out of TB-F1, or names another slice such as TB-F1. The coordinator records whichever the operator accepts.

### B.3 The §2.2a amendment it depends on (cited, not applied)

The dependency is S5 draft §1.5(d), `2026-09-26-s5-decision-draft.md:144-146`. It is inserted into the full-E1 spec §2.2a after "Clients verify ordered offsets, total length and the reassembled SHA256." (`2026-09-17-protected-full-e1-campaign.md:84`). Its text begins "For production-class campaigns (`tb-s2-rng-v3`), the plan object served to the client is a client view: the canonical plan with each seed value replaced by its digest." **RC-2 governs applying it.** It is applied only with operator acceptance, as part of the full RC-2 owner-text set, which the 2026-09-27 staging puts at Checkpoint C3/S5 acceptance (ledger `:829`).

The S5 draft RC-4 row (`:385`) says the RC-4 scheduling text needs "the §1.5(d) amendment applied". The 2026-09-27 build-entry row (ledger `:828`) asks only for "the seed-view owner and slice, with the F1 admission-check text". The draft says "Where this table differs, the ledger entry governs" (`:376`). The ledger's own 2026-09-26 entry also says RC-4 "stays unmet until the change lands or its owner record holds the scheduling text RC-4 requires (a named owner and slice, the §2.2a client-view amendment applied, the F1 admission check)" (ledger `:810`). The later 2026-09-27 direction divides that text by stage: build entry asks for "the seed-view owner and slice, with the F1 admission-check text" (`:828`), and "The full RC-2 owner-text set accepted and applied", which includes §2.2a, is a Checkpoint C3 item (`:829`). The 2026-09-27 ruling approves that staged structure (`:842`). So at build entry RC-4 needs the assignment (with the operator-accepted slice, §B.2) and the check text below held **in the owner record itself**, and §1.5(d) is applied at C3 under RC-2. This reading is the coordinator's to confirm when recording.

**A drafting point for the RC-2 review of §1.5(d) (not a change here).** A seed is the first 8 bytes of a SHA-256, so a 64-bit value (`regime.py:24`, `.digest()[:8]`). A bare `sha256(seed)` digest therefore has a 2^64 preimage space, far below the salt's 256 bits (audit K3). §1.5(d) does not define the digest. The review should state it, for example keyed by the salt or computed over a value that already contains 256 bits of salt-derived entropy, so that the client view cannot be inverted by enumeration. This is recorded as Q-2 (§D.2).

**PROPOSED replacement wording for the RC-2 review (not applied; RC-2 governs).** In §1.5(d), replace "the canonical plan with each seed value replaced by its digest." with:

> "the canonical plan with each seed value replaced by its seed digest, HMAC-SHA256 keyed by the attempt salt over the seed record's canonical bytes, so that the digest cannot be inverted without the salt; after reveal the client recomputes each seed digest from the revealed salt."

This is one example of the property the review should state. A keyed digest also means the client can check seed digests only after reveal; whether that is acceptable, or whether another 256-bit-entropy construction is preferred, is the review's choice.

### B.4 F1 admission-check text (PROPOSED, exact)

> **F1 admission check (RC-4; AUDIT-2026-09-25-qualification-assurance-contract-delta#K3).** The production attempt is not admitted while the `client` role can fetch a seed value or the salt. Admission refuses unless every condition holds, and it evaluates them **before** the transaction that binds the F1 budget and generates the salt, so that a refusal generates no salt and consumes no attempt:
> 1. The contract's RNG recipe is `tb-s2-rng-v3`, and the installed release's plan-view mode for the `client` role is `client_view_digests_only`. The service refuses a `tb-s2-rng-v3` admission on any release without that mode.
> 2. The installed release digest equals the release named in F1, and that release was accepted with the negative client cases of S5 draft §1.6 passing on Linux on its bytes: no salt or seed value reaches `client` through `STATUS`, `FETCH_PLAN_CHUNK` or the receipt before closure.
> 3. The admission receipt schema binds `client_view_sha256` and `client_view_byte_length` beside `plan_sha256` and `plan_byte_length`. The client verifies the reassembled client view against them.
> 4. An OF-7 attestation at gate G-F1 is recorded for this host after the installed release was installed, with no OF-7 trigger since.
>
> Any failed condition refuses admission. The refusal is recorded and is not a consumed attempt.

**Where it lands (PROPOSED):**
- Condition 1 is implemented and tested in the K3/RC-4 slice.
- Conditions 1-3 are stated as one sentence in full-E1 spec §2.2a beside §1.5(d), under RC-2.
- Conditions 2-4 are checked at CP-6 and CP-8 as F1-packet items (the T10 phase-2 packet).
- The scheduling text goes in the execution-slices ledger (§E).

---

## C. Production-class host and credential specification

### C.1 Platform the accepted boundary relies on (S2 evidence)

The boundary was accepted on fresh GitHub-hosted `ubuntu-24.04` hosts.
- S2 acceptance: run 35553674384 on `4ef913a`, 15/15.
- Merge gate: run 35557000399 on `a519bfb`.
- Source: ledger "Coordinator acceptance — S2 …", `:618-648`; runner at `.github/workflows/qualification-s2-supervision.yml:68`.

The independent review of the #434 host fixes was "checked against systemd v255 and Linux v6.8 sources" (ledger `:525`). Those are the review's reference versions, **not** a pinned host inventory. Each run records the actual OS, kernel and package inventory (`tools/qualification_verification/README.md:54-57, 63-66`). The workflow also records Docker's cgroup driver and cgroup version (`qualification-s2-supervision.yml:120-121`).

| Requirement | Relied on by | Source |
|---|---|---|
| Ubuntu 24.04 x86_64, native ext4; `/usr/bin/python3` at 3.12.3; Docker Engine `docker-ce` 28.0.4 pinned | Test host configuration (`qualification_test_host/v1`) | `tools/qualification_verification/host.json:2-12`; README:30-31 |
| x86_64 timer ABI; `CLOCK_BOOTTIME` absolute `timer_create`/`timer_settime` SIGKILL before any campaign import | Original-deadline enforcement | `deploy/qualification/bootstrap.py:38-78` (ABI check `:49-50`) |
| `prctl(PR_SET_PDEATHSIG)` and an RLIMIT_CPU check for the control child | `campaign_control` | `bootstrap.py:80-95` |
| cgroup v2 at `/sys/fs/cgroup`, administrator-owned and writable, **including `cgroup.kill`** | Owned-process lifecycle, cleanup | README:324-331 |
| `memory.max`, `memory.swap.max = 0`, `memory.events`, `memory.peak`, `cpu.stat`, `cpu.max` | Common memory slice; settlement counters; OOM retention | `campaign_host.py:35-36, 65-66`; `campaign_supervisor.py:81-95, 974-1011` |
| systemd `StartTransientUnit` (busctl), `systemd-run --collect`; properties `RuntimeMaxUSec`, `CPUQuotaPerSecUSec`, `LimitCPU`, `TasksMax`, `OOMPolicy=kill`, `KillMode=control-group`, `BindsTo`, `NoNewPrivileges`, CPU and memory accounting | Kernel-bounded payload CPU (quota × RuntimeMax, because "cgroup v2 has no cumulative CPU cap") | `campaign_host.py:37-39, 112-114`; `campaign_supervisor.py:175-192, 299-340` |
| One polkit rule `49-<prefix>.rules` granting `org.freedesktop.systemd1.manage-units` to `qexec`. It is not prefix-bound for transient starts, so qexec can start arbitrary transient units | S2 trust fact accepted 2026-09-19 | `campaign_host.py:83-99`; README:283-292; ledger `:515` |
| `pidfd_open` / `pidfd_send_signal` | Verified-process kill | `campaign_supervisor.py:1056-1061` |
| Docker worker isolation: network none, read-only, no-new-privileges, private IPC/PID, PIDs limit, worker UID 65532 | Worker container | `deploy/qualification/test-profile.json` (TEST_ONLY profile) |

**Minimum kernel and systemd versions** for `cgroup.kill`, `memory.peak`, `pidfd_*` and the properties above are **UNVERIFIED** here. The production host class should equal the accepted class: Ubuntu 24.04 x86_64, with the recorded inventory. Otherwise it needs its own S2-equivalent Linux evidence before G-REL.

**Operational requirements derived from recorded facts:**
- **No unattended reboot or package upgrade while a campaign can run.** Any service restart destroys every running work, a healthy guardian included (A3, ledger `:638`). Deadlines are BOOTTIME-based (`bootstrap.py:38-78`). The harness already refuses ambient package upgrades (README:43-45).
- **Swap.** The common slice pins `memory.swap.max = 0` (`campaign_host.py:35`). H1's memory acceptance reads `memory.peak`/`MemoryPeak` "with swap off" (handoff H1 condition 2).
- **systemd-oomd.** The S2 workflow retains an oomd log (`qualification-s2-supervision.yml:160`). Whether systemd-oomd runs on the production class, and whether it may act on campaign slices, is **UNVERIFIED** (Q-7).
- **Persistent host.** Current acceptance is "for fresh disposable hosts" and "does not by itself establish shared or reused-host support" (README:376-380). A persistent production host therefore needs its own acceptance under checklist T11 (`checklist:239-248`). That is checklist T11's work, not this note's.
- **Dedicated host.** The host runs only the qualification service (boundary spec §3, `:56`: "a dedicated Linux service deployment").
- **Sizing (vCPU, RAM, disk) is UNVERIFIED and not specified here**, pending checklist T11's "realistic measured resource envelope" (`checklist:245`).
  - A production ceiling needs its own measurement on the production host class (`8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md:90-92`).
  - The runner's 4 vCPU / 16 GB is vendor documentation and not verified (`…:79`).
  - Production budgets remain separately governed (ruling 2026-09-26).
  - Known storage anchors are the 21,623,745-byte measured reference plan and the 64 MiB planner cap (full-E1 spec §2.2a, `:82, :86`).

### C.2 Principals

| Principal | Groups and access (canonical) | Source | Production note |
|---|---|---|---|
| `qclient` | no supplementary groups | `role_policy.py:6`; README:99-102 | Must not reach seed values before closure (RC-4, OF-7) |
| `qexec` | `docker` group; polkit `manage-units`; owns `data` and `scratch` (`0700`); execution key | `role_policy.py:6,18,20`; boundary spec `:153-154` | Root-equivalent through Docker (README:13-17); trusted |
| `qg5` | `qclient` group (socket access); no access to qexec's data or credentials; result key | `role_policy.py:6`; README:100-102; boundary spec `:154` | Private salt route open (S5 draft Q8) |
| `qseal` | separate process and UID; seal key | full-E1 spec §2.2 (`:74, :77`), §2.8 (`:169`) | **Not in `role_policy.py` on `main`.** The seal code exists at `6cf2732` (`seal_service.py`, `campaign_seal.py`). The real principal and its host-provisioning change are owed (handoff H9, seam row 11, line 425) |
| worker | container UID 65532, no network, read-only | `test-profile.json` | Receives the salt in its read-only input under v3 (S5 draft §1.4) |
| administrator | uid/gid 0, never a provisioned role | `role_policy.py:9-14` | Trusted by design (boundary spec §3). Its remote credential must not be usable from any agent-hosting account (OF-1). If agents run under the operator's workstation account, the administrator credential must live on a separate OS account or device (CQ-1) |
| host `operator` UID | distinct from client, g5 and service UIDs; role `operator` = `STATUS`, `VOID`; VOID also needs a detached approval of scope `VOID_QUALIFICATION_ATTEMPT` | `release.py:17, 31`; `service.py:85-89, 319` | **Not named in OF-2** (Q-1) |

Every provisioned principal: locked authentication, no home, non-login shell, primary GID equal to UID (README:95-99). qexec must run only approved supervisor code and expose no general Docker RPC to qclient (README:16-17).

**Contract-delta rows these principals carry** (audit §5.1 table, `2026-09-25-qualification-assurance-contract-delta.md:193-200`):
- **K6** (principal separation; forward cost "Production host provisioning", `:193`; "The open operational check is that no agent session holds administrator access on that host", K6 body) is checked by OF-1 and OF-2 at G-PROV, then G-REL and G-ACC.
- **K7** (independent G5 adjudication, `:194`) rests on the `qg5` principal and its private salt route: OF-2 and OF-7.
- **K8** (explicit activation and fresh reconciliation, `:195`; verification "T11 checks per ADR §2a", that is ADR-T11) and **N5** (approval packets, including the per-session GO, `:200`) meet this note at G-ARM: the OF-5 attestation joins the arm evidence of the session (§A.3). Neither is implemented by this note.

### C.3 Key storage and custody (PROPOSED custody; no key generated)

| Key | Holder | Storage rule (from code or spec) | Custody proposal |
|---|---|---|---|
| Execution signing | `qexec` | `qualification_private_credential/v1` file: owner = signing euid, mode `0400`, one link, protected ancestors (`credentials.py:12-37`); readable only by qexec and the administrator (boundary spec `:153-154`) | Generated on the host into qexec's credential directory; only the public fingerprint leaves the host (for enrollment) |
| Result (G5) | `qg5` | same file rule; "result key only by qg5" (`:154`) | same, in qg5's directory |
| Seal | `qseal` | "qseal holds the separate seal key" (full-E1 spec `:169`); same file rule | same, in qseal's directory, once the principal exists (H9) |
| Freeze / F1 and other approval keys | operator | Detached-approval format; keys for execution, freeze, result and seal disjoint by ID and fingerprint (boundary spec `:130, :144-146`) | Off-host, operator-held; never on an agent-hosting account |
| Operator-VOID | operator | VOID approval scope `VOID_QUALIFICATION_ATTEMPT` (`service.py:319`) | Off-host, operator-held; OF-3 |
| GO signing (only if E3) | operator | Audit row E3: "a detached GO signed by an operator key held off-host" | Off-host; OF-6. E3 is **not adopted** (admission ADR §2b still specifies the reseal) |

TEST_ONLY keys are ephemeral raw Ed25519 keys in separate private credential directories, whose bytes never enter logs (README:141-142). They can never become production keys, because authority classes must agree and "There is no request flag that enables test authority on an OPERATOR service" (boundary spec `:148-151`).

### C.4 Enrollment inputs (OF-4 objects)

- **Release manifest** `qualification_execution_release/v1`, generated after the image build and approved by a detached approval of scope `APPROVE_EXECUTION_RELEASE`. The administrator's protected release-approval registry is the trust root (boundary spec `:109-134`).
- **Trust domain**: `execution_key_ids`, `execution_service_id`, `execution_release_sha256`, `required_attested_checkpoints` (`:139-146`).
- **Instance document**: `qualification_execution_instance/v1|v2`, holding `authority_class`, paths, `socket_gid`, the four UIDs and `execution_credential` (`release.py:16-31`). The TEST_ONLY `qualification_test_instance/v1` is administrator-owned (README:256-259).
- **Campaign-host enrollment**: `qualification_campaign_host/v1`, `0444`, holding the polkit rule path and SHA-256 and the profile SHA-256 (`campaign_host.py:94-96`).
- **Host configuration**: the TEST `host.json` is `qualification_test_host/v1` with `"qualification_acceptance": "blocked_pending_boundary_integration"` (`host.json:2,20`). **A production host-configuration schema does not exist** and is owed by checklist T11.

### C.5 K3 salt custody (host view; D1 as ruled)

D1, in the ruling's words: "Service-generated salt; private worker/G5 access; no client disclosure while computation or recovery remains possible."
- `qexec` generates the salt with `secrets.token_bytes(32)` in the budget-binding transaction and stores it in its store, under the `data` tree (`qexec`, `0700`, `role_policy.py:18`).
- The salt reaches the worker only through its read-only input.
- `qg5` reads it through a private route (Q8 open).
- The client sees only `sha256(salt)` until closure (S5 draft §1.4, `:117-121`).
- **Host consequences:**
  - no backup, snapshot or copy of the `data` tree may be agent-reachable before reveal (Q-3);
  - OF-7 is read at G-F1;
  - the administrator can read the salt by design (S5 draft §1.7).

### C.6 Installed-identity verification

- **Before every dispatch**, the service checks the installed release digest and image identity (boundary spec `:131-134`).
- **Host observations** are exported through an allowlist that excludes the private ownership manifest and credentials (README:63-66).
- **The attestation binds three things:**
  - `installed_release_sha256`;
  - `host_identity_sha256`. PROPOSED: the systemd app-specific machine ID (`systemd-id128 machine-id --app-specific=<fixed app UUID>`), so that the raw machine ID is never published. Availability of that option on the target host is **UNVERIFIED**;
  - the gate.
- **Checklist T11** additionally requires wrong-authority, wrong-key, wrong-source, wrong-runtime and stale-approval refusals, plus installed host and source evidence (`checklist:239-248`).

### C.7 TEST_ONLY versus production

| Item | TEST_ONLY (today) | Production (owed) |
|---|---|---|
| Host | Fresh disposable GitHub-hosted `ubuntu-24.04`, provisioned with `sudo` by an agent-editable workflow; **not a boundary host** (S5 draft `:84`; workflow `:106-161`) | Dedicated, non-disposable, administrator-provisioned; no agent-editable provisioning path (OF-1) |
| Host config | `qualification_test_host/v1`, acceptance blocked (`host.json:2,20`) | Production schema owed (checklist T11) |
| Profile | `production_execution: false`, `N1_ONLY` base (`profile.py:8-14`; `test-profile.json`) | Production profile and budgets separately governed (ruling 2026-09-26) |
| Keys | Ephemeral raw Ed25519, `TEST_ONLY` class | `OPERATOR` class, custody in §C.3 |
| RNG recipe | `tb-s2-rng-v2` (`regime.py:22`) | `tb-s2-rng-v3` (K3/RC-4 slice) |
| Evidence | Diagnostic or acceptance-grade for machinery | Production E1 once (T15) after CP-8 |

### C.8 Cost and spend (operator decision at CP-8)

| Item | Needed for | Amount |
|---|---|---|
| Production qualification host (dedicated Linux VM or machine of the accepted class) for provisioning, checklist T11 acceptance, the production E1 window and retention | CP-8, checklist T11, T15 | **OPERATOR DECISION at CP-8.** No provider selected, no price stated |
| Storage and backup of retained evidence (admin-only; Q-3) | T15 retention | **OPERATOR DECISION at CP-8** |
| Off-host key custody device(s) for operator keys, if the operator chooses hardware | §C.3 | **OPERATOR DECISION at CP-8** |
| Operator time for attended reads at every gate in §A | §A | Not money; recorded for planning |

Whether host spend counts against the rail's $700 spend ceiling (AGENTS.md, standing-consequence table, "Rail build/account registration GO; spend ceiling $700") is **an operator decision** (Q-8).

### C.9 Host bill of materials (PROPOSED; no provider, no sizing)

| Item | Specification | Source in this note |
|---|---|---|
| Host class | One dedicated, persistent, administrator-provisioned Linux host of the accepted class (Ubuntu 24.04 x86_64, native ext4, cgroup v2, systemd, polkit, pinned Docker Engine, `/usr/bin/python3` 3.12); no agent-editable provisioning path | §C.1, §C.7 |
| Sizing | **UNVERIFIED**: vCPU, RAM and disk come from checklist T11's measured envelope (`checklist:245`) | §C.1, §D.4 |
| Principals | `qclient`, `qexec`, `qg5`, `qseal` (owed, H9), host `operator` UID, administrator; worker container UID 65532 | §C.2 |
| On-host key files | Execution (`qexec`), result (`qg5`), seal (`qseal`): `0400`, one link, protected ancestors | §C.3 |
| Off-host custody items | Freeze/F1 and other approval keys, operator-VOID key, GO signing key if E3; optional hardware device(s) | §C.3, §C.8 |
| Enrollment inputs | Release-approval registry, release manifest and approval, trust domain, instance document, campaign-host enrollment, polkit rule, production host configuration (schema owed by checklist T11) | §C.4 |
| Salt custody | `data` tree `qexec` `0700`; worker read-only input; `qg5` private route (S5 draft Q8 open); no agent-reachable backup | §C.5 |
| Retained-evidence storage | Administrator-only storage and backup for T15 retention; not agent-reachable (Q-3) | §C.8 |
| Attestation records | Private transcripts (operator, archived); public attestations under the §A.3 path | §A.3 |

---

## D. Open questions and UNVERIFIED items

### D.1 Contract questions (card stop condition: OFs that an attended read cannot fully verify)

- **CQ-1 (OF-1, OF-3, OF-5): "no agent-reachable credential" is verifiable only against an enumerated list.**
  - A read can establish absence in the credential stores it enumerates. It cannot establish that no other agent environment exists.
  - Proposed enumeration, pinned in the attestation schema by class name:
    - each workstation OS account that runs an agent, with its harness configuration and credential directories, SSH agent and forwarding, git credential helpers and cloud CLI tokens;
    - each cloud agent environment's configured secrets;
    - GitHub Actions secrets at repository, environment and organization level;
    - every worktree root.
  - Question for the contract owner (operator): does a complete read of the pinned enumeration satisfy the OF?
  - A consequence to decide at the same time: if agents run under the operator's own workstation account, the administrator's host credential must sit on a separate OS account or device. Whether a touch-confirmed hardware key on the same account counts as "not reachable" is an operator decision.
- **CQ-2 (OF-6): "never loaded where an agent runs" is historical.** An attended read verifies current custody and current absence only. The historical half rests on the custody record. Is that sufficient?
- **CQ-3 (OF-7): the salt does not exist at G-F1.** It is generated inside the admission transaction (S5 draft `:117-118`). A pre-admission read can therefore verify only the custody configuration: tree modes, installed release, client plan-view mode, the qg5 route and backups. Plan derivation follows the binding automatically (`campaign_supervisor.py:1456-1470, :1499`, cited by S5 draft `:118`). So an attended read of the actual salt row between binding and first use would need a new pause point, which no owner specifies. Question: does configuration-level verification at G-F1 satisfy OF-7, or is a post-binding read (and a pause point) required? The G5 route (Q8) must be decided before the OF-7 read's object list is complete.

### D.2 Other open questions

- **Q-1:** Should OF-2 name the host `operator` UID (`release.py:31`; role `operator` = `STATUS`, `VOID` at `service.py:81, 85-89`)? An agent that could run as that UID and reach the VOID approval key could VOID. The proposal adds it to the OF-2 read. That only adds a check, but amending the OF-2 text is RC-2 owner text. **PROPOSED replacement for the OF-2 clause of §1.5(a) (for RC-2; not applied):** "(OF-2) no agent can authenticate as `qexec`, `qg5`, `qseal`, the host `operator` UID or the administrator, and no polkit rule grants `manage-units` to an agent-reachable UID;"
- **Q-2:** The §1.5(d) digest definition (64-bit seed preimage), for the RC-2 review. PROPOSED wording in §B.3.
- **Q-3:** Backups and snapshots of the `data` tree before reveal, which is an OF-7 object. Proposed: admin-only and not agent-reachable. Owner: RC-2 text or checklist T11.
- **Q-4:** Public attestation file versus a private record with a public hash only; whether a public, stable `host_identity_sha256` (which links a host's attestations to one another) is acceptable; and the exact private transcript location.
- **Q-5:** Whether an attestation goes stale by age alone, in addition to triggers.
- **Q-6:** Whether TB-I3's `--arm` consumes the OF-5 attestation digest as a typed input.
- **Q-7:** systemd-oomd on the production class.
- **Q-8:** Whether host spend counts against the $700 rail ceiling.
- **S5 draft Q8** (G5 private salt route) and **Q9** (closure of a never-retried retry-eligible IN_DOUBT) stay open. They are inputs to the K3/RC-4 slice and to CQ-3.

### D.3 Operator decisions surfaced by this note

- Name the RC-4 slice (S5 draft `:363`): accept the recommendation (a qualification slice before S8, with K3 moved into it from TB-F1) or name another, such as TB-F1. The RC-4 assignment is complete only after this choice.
- The CP-8 spend line (§C.8) and Q-8.
- CQ-1..CQ-3.
- Q-4 and Q-5.

### D.4 UNVERIFIED

- The actual kernel, systemd and Docker versions of any production-class host. No production host exists (`8c15f18:…measurement-proposal.md:90`).
- The minimum kernel and systemd versions for `cgroup.kill`, `memory.peak` and `pidfd_*`.
- Whether T05's result or seal chain binds the admission receipt bytes (§B.2).
- Whether any agent environment currently holds Fly, broker or host credentials. This note read no credential store, secret list or host.
- The `systemd-id128 --app-specific` option on the target host.
- Host sizing (vCPU, RAM, disk), pending checklist T11's measured envelope (`checklist:245`; §C.1, §C.9).
- Every OF is unverified by this note. Enforcement is **not established**. That is not a finding that it is absent (S5 draft `:104`).

---

## E. Proposed ledger text (for the coordinator to record; PROPOSED, not recorded)

> ### Coordinator assignment — RC-4 seed view and RC-5 host checks, <recording date>
>
> **Source.** The operator ruling of 2026-09-27 ("Assigning seed-view and host-check owners now, with implementation and attestations due at their specified later gates"), acting on the [H7 return](2026-09-27-host-obligations-assignment.md). The RC-5 assignment and the resolution of S5 draft §6 Q12 are coordinator acts: the 2026-09-26 entry above leaves Q12 "open for the coordinator's owner-text and RC-5 work". The RC-4 **slice** is one "the operator names" (S5 draft `:363`); this entry records it as the operator accepted it on <date of operator acceptance>, or, until then, as the coordinator's proposal.
>
> **RC-5 (OF-1..OF-7).** S5 draft §6 Q12 is resolved to the stricter reading, which only adds gates: every OF is verified by an operator-attended host read at production-host provisioning (CP-8), before any production-authority release (any `OPERATOR`-class release, instance, trust-domain or key enrollment, and before CP-8 admits the production attempt), and after any access change. In addition, OF-5 is read before any arm and at each session GO, OF-6 at TB-I3 (NOT_APPLICABLE unless E3 is adopted), and OF-7 before F1 admission. Verifier: the operator (attended). Recorder: the operator; the coordinator checks completeness and records each attestation here. Record: a private raw transcript held by the operator outside every checkout and archived in `first-passage-archive`, plus a public attestation `docs/notes/qualification_host/attestations/<date>-<gate>.json` (schema `qualification_host_of_attestation/v1`: booleans, octal modes, role names, enumerated codes, dates and hashes only, no free-text field), linked here by path and SHA-256. An attestation satisfies a gate only if no trigger for that OF occurred between the read and the gate. Re-verification triggers:
>
> | OF | Triggers (each also: host rebuild or reprovision) |
> |---|---|
> | OF-1 | account, group, sudoers or sudoers.d change; Docker install, upgrade or socket-permission change; new agent harness, agent OS account or cloud agent environment; change on an agent-hosting workstation account to SSH keys, SSH agent or forwarding, credential helpers or remote-access tooling |
> | OF-2 | change under `/etc/polkit-1/rules.d`; principal creation, deletion, UID or authentication change; polkit or systemd upgrade |
> | OF-3 | key generation, rotation, enrollment or revocation; new GitHub Actions secret (repository, environment or organization) or new workflow; new worktree root or agent environment |
> | OF-4 | enrollment, release install, trust-domain or instance-document change |
> | OF-5 | Fly membership or token change; broker credential issue or rotation; new agent environment or cloud environment secret; rail redeploy by a new path; each arm; each session GO |
> | OF-6 | E3 adoption; GO key generation, rotation or device change; new agent environment; TB-I3 |
> | OF-7 | release install; data or scratch tree binding change; qg5 route change; backup or snapshot configuration change |
>
> An unverified OF is reported as "enforcement not established". The OF definitions' owner is boundary spec §3.1 once RC-2 applies S5 draft §1.5(a). Contract questions CQ-1..CQ-3 are open.
>
> **RC-4 (client plan-view seed change).** Owner: the qualification coordinator, through this ledger. Slice (proposed; the operator names it): "K3/RC-4 — service salt and client plan view", covering the digests-only client view, the receipt's `client_view_sha256`/`client_view_byte_length`, `tb-s2-rng-v3` with service-generated salt, commitment and reveal, the S5 draft §1.6 tests and the service-side refusal of condition 1 below. It moves K3 out of TB-F1, where S5 draft §4 placed it. It is dispatched after S5 acceptance and lands before S8/T06 dispatch; its order against the D3 slice is set at dispatch. That S8/T06 precondition is sequencing, which the [checklist addendum 2026-09-27](../superpowers/plans/2026-09-20-tradeify-deployment-checklist.md#addendum-2026-09-27--staged-acceptance-evidence-proportional-to-the-next-step) governs; this entry does not change the addendum, which must record it separately once the operator accepts the slice. It depends on the full-E1 spec §2.2a amendment of S5 draft §1.5(d), applied under RC-2 at Checkpoint C3 and not by this entry.
>
> **F1 admission check (RC-4; AUDIT-2026-09-25-qualification-assurance-contract-delta#K3).** The production attempt is not admitted while the `client` role can fetch a seed value or the salt. Admission refuses unless every condition holds, and it evaluates them **before** the transaction that binds the F1 budget and generates the salt, so that a refusal generates no salt and consumes no attempt:
> 1. The contract's RNG recipe is `tb-s2-rng-v3`, and the installed release's plan-view mode for the `client` role is `client_view_digests_only`. The service refuses a `tb-s2-rng-v3` admission on any release without that mode.
> 2. The installed release digest equals the release named in F1, and that release was accepted with the negative client cases of S5 draft §1.6 passing on Linux on its bytes: no salt or seed value reaches `client` through `STATUS`, `FETCH_PLAN_CHUNK` or the receipt before closure.
> 3. The admission receipt schema binds `client_view_sha256` and `client_view_byte_length` beside `plan_sha256` and `plan_byte_length`. The client verifies the reassembled client view against them.
> 4. An OF-7 attestation at gate G-F1 is recorded for this host after the installed release was installed, with no OF-7 trigger since.
>
> Any failed condition refuses admission. The refusal is recorded and is not a consumed attempt.
>
> **Status.** The 2026-09-26 entry above required RC-4's owner record to hold "a named owner and slice, the §2.2a client-view amendment applied, the F1 admission check". The 2026-09-27 direction divides that by stage: build entry needs "the seed-view owner and slice, with the F1 admission-check text", and the full RC-2 owner-text set, §2.2a included, is applied at Checkpoint C3. On that reading, and **once the operator has accepted the RC-4 slice**, this entry meets the RC-4/RC-5 **assignment** at build entry; the coordinator confirms that status on recording. The implementation (the RC-4 change landed, K3 built) and the attestations (OF-1..OF-7) remain before F1, as the 2026-09-27 direction's "Before F1" row states. *[Corrected 2026-09-27: the attestations fall due at the gates this note's RC-5 assignment sets (item 1): OF-7 before F1 admission, the full OF-1..OF-7 set at CP-8. See the ledger's RC-5 entry.]*
>
> **Not granted:** S5 release, dispatch or execution; owner text applied; host provisioning or spend; credential or key creation; F1, CP-6 or CP-8 decisions; production, arm, deployment or live authority. The hold stays **HELD**.

(Relative links in the quoted text are adjusted to resolve from this note. The recorded ledger copy uses the ledger's own relative paths.)

---

## Verification of this note

Commands actually run (read-only), at `521d8f2` in `/home/user/first-passage`:

```bash
git log --oneline -1                                          # 521d8f2d
sed -n 1,120p  docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md
sed -n 340,459p docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md   # H7 card
sed -n 375,520p docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md  # addendum §0-§5
sed -n 239,250p docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md  # T11
sed -n 286,298p docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md  # T15
sed -n 797,850p docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md       # rulings 09-25..09-27
sed -n 515,526p docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md; sed -n 618,648p …   # S2 evidence
# S5 draft read in full (§1, §4-§6, verification, coordinator review)
sed -n 143,206p docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md; sed -n 230,300p …; sed -n 370,426p …
sed -n 54,158p docs/superpowers/specs/2026-09-17-qualification-execution-boundary-design.md; sed -n 471,520p …
sed -n 65,127p docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md
grep -n "^#\|T10\|T11" docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md
grep -n "O-10\|O-9\|§0.8" docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md   # no O-10
# incident ADR §A11.2/§A11.3 and campaign-record Ruling 7 headers read at their owners
grep -n "'client':\|'g5':\|'operator':" ops/c1_rail/qualification/execution/campaign_protocol.py
sed -n 25,45p ops/c1_rail/qualification/seed_identity.py; sed -n 218,236p ops/c1_rail/qualification/checkpoint_plan.py
sed -n 2405,2436p ops/c1_rail/qualification/execution/campaign_store.py; sed -n 60,95p ops/c1_rail/qualification/execution/client.py
sed -n 8,30p ops/c1_rail/qualification/regime.py                 # seed = sha256(...)[:8]
sed -n 380,390p ops/c1_rail/qualification/execution/service.py; sed -n 480,492p …; sed -n 80,100p …
sed -n 1,40p ops/c1_rail/qualification/execution/credentials.py; sed -n 16,31p ops/c1_rail/qualification/execution/release.py
cat -n tools/qualification_verification/README.md tools/qualification_verification/host.json
cat -n tools/qualification_verification/role_policy.py | sed -n 1,24p
sed -n 1,125p tools/qualification_verification/campaign_host.py
cat -n deploy/qualification/bootstrap.py; cat deploy/qualification/test-profile.json
sed -n 175,196p ops/c1_rail/qualification/execution/campaign_supervisor.py; sed -n 295,345p …
grep -n "runs-on\|sudo" .github/workflows/qualification-s2-supervision.yml
git show 6cf2732:tools/qualification_verification/role_policy.py | sed -n 1,10p   # no qseal role
git grep -n "qseal" 6cf2732 -- tools deploy ops/c1_rail/qualification/execution
git show 6cf2732:ops/c1_rail/qualification/execution/campaign_result.py | grep -n "plan_sha256\|admission_receipt\|receipt_sha256"
git show 8c15f18:docs/notes/2026-09-26-s5-part-a-measurement-proposal.md   # :79, :84-92, :350-362 read
git show 8c15f18:<each other #519 path> | grep -n "OF-\|qexec\|RC-4\|RC-5\|credential"   # only the lifecycle note's replay-spec RC-4
python3 scripts/check_handoff_authority.py --all   # "2 card(s) with an authority block, 0 violation(s)"
# relative-link check (python: every non-http link in this note resolves from docs/notes/; the §E link from docs/superpowers/plans/)
```

- **Not run:** `make check`, `fp.py check`, any test, any Linux dispatch, any host, credential or secret read. The card's acceptance (`make check` clean) belongs to the coordinator's branch run. Per the dispatch instructions, this worker did not run the full gate suite.
- **Line anchors:** every code anchor above was re-read at `521d8f2` in this session. The S5 draft's own code anchors are at `main@24e3843`; those used here were re-read and still hold at HEAD, except that `seed_identity.py`'s `seed` field is at `:39` (the draft cites `:35-40`, which contains it).

**Fix-round verification (2026-09-27, read-only, at `c991d2d`):**

```bash
git log --oneline -5; git diff --stat 521d8f2 HEAD     # only .claude/skills/task-routing/SKILL.md changed
sed -n 355,362p docs/briefs/handoffs/2026-09-27-staged-acceptance-handoffs.md      # "proposes" at :360
sed -n 88,95p ops/c1_rail/qualification/execution/client.py                          # digest check at :92-93
sed -n 376,388p docs/adr/2026-09-17-bounded-platform-protection-incident-contract.md # §A11.2 scope (:381, :384)
sed -n 76,90p docs/notes/2026-09-26-s5-decision-draft.md; sed -n 128,150p …; sed -n 360,406p …   # :78, :87, :363, :376, :385-386, :404
sed -n 118,122p .github/workflows/qualification-s2-supervision.yml                    # cgroup driver and cgroup version
sed -n 13,18p tools/qualification_verification/README.md
grep -n "^### " docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md; sed -n 810p …; sed -n 820,850p …
sed -n 24,28p docs/superpowers/plans/2026-09-20-tradeify-deployment-checklist.md; sed -n 385,396p …; sed -n 470,500p …; sed -n 239,250p …; sed -n 286,290p …
sed -n 186,202p docs/notes/audits/2026-09-25-qualification-assurance-contract-delta.md; sed -n 270,300p …; grep -n "^| B-4" …   # B-4 row is :176
sed -n 96,105p docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md    # ADR-T11 at :100
systemd-id128 --help | grep -i app                                                    # option exists on this sandbox, not on the target host
python3 scripts/check_handoff_authority.py --all
# relative-link check: every non-http link resolves from docs/notes/; the §E quoted links from docs/superpowers/plans/
```

## Review and fix round (2026-09-27)

Each finding was re-verified against its source before it was applied.

| ID | Disposition | What changed, or why not |
|---|---|---|
| F1 | Applied | Verified: S5 draft `:363` has the operator name the slice and puts K3 with TB-F1. §B.2 now cites `:363`, marks the placement and the K3 move as operator choices, and rewrites the former "Operator decision only if the operator prefers TB-F1" sentence to agree with §D.3. §E records the slice as a proposal until the operator accepts it, and "assignment met" is conditional on that acceptance. The header and answer-in-brief item 3 were aligned |
| F2 | Applied | Verified at handoff `:360`. Changed "card line 358" to "card line 360" |
| F3 | Applied | Verified `client.py:92-93`. Anchor corrected |
| F4 | Applied | Verified §A11.2 `:381`, `:384`. G-ARM now rests on AGENTS.md "Every armed session needs its own GO". §A11.2 is cited only as supporting, with its commissioning and first-attended-release scope and the "not ruled" limit |
| F5 | Applied | Verified: `:87` says "Held by OF-5/OF-6 until TB-I3", and the T11 point is at `:78`. The OF-6 row now quotes `:87` and cites `:78` and the audit B-4 row. The audit row is at `:176`, not the `:177` the finding gave (`:177` is B-5) |
| F6 | Applied | Verified workflow `:120-121` (`CgroupDriver`, `CgroupVersion`). Now reads "cgroup driver and cgroup version" |
| F7 | Applied | Verified README `:16-17`. Reworded as the requirement it states |
| H7-R1 | Applied | §E now holds the §B.4 conditions 1-4 verbatim and a per-OF trigger table, so the owner record holds the text itself. §B.3 and §E cite the 2026-09-26 entry's RC-4 wording (ledger `:810`) and explain that the 2026-09-27 direction (`:828-829`), approved by the ruling (`:842`), applies §2.2a at C3. "Met" is now conditional and for the coordinator to confirm |
| H7-R2 | Applied | `trigger` is replaced by `trigger_codes` from a PROPOSED enumeration built from the §A.2 trigger column, and `operator_statement` by the boolean `operator_confirms_reads_as_recorded`. The note states that the schema has no free-text field and that words belong in the hash-bound private transcript. Answer item 2 and §E were updated |
| H7-R3 | Applied | One framing: the operator names the slice, and the coordinator records it (§B.2, §D.3, §E agree). §B.2 and §E note that "before S8/T06 dispatch" is sequencing, which the checklist addendum governs (`:392-393`; T06/S8 row `:26`). The ledger entry does not change the addendum, which must record the precondition once the placement is accepted |
| H7-R4 | Applied | Same fix as F4 |
| H7-R5 | Applied | Same fixes as F2 and F5 |
| H7-R6 | Applied | The label note defines ADR-T11 (admission ADR `:100`) and checklist T11 (`checklist:239`). Every T11 mention in the body now carries one of those labels |
| H7-R7 | Applied | Counts reduced to pass/fail booleans. `rail_platform_members_with_deploy` became `rail_deploy_members_are_operator_only`, and `nlink` became `single_link`. `host_identity_sha256` is now defined as the SHA-256 over the app-specific ID, and its public linkability is added to Q-4 (formerly Q-6) |
| H7-R8 | Applied | Added §C.9, the host bill of materials. Sizing is recorded as UNVERIFIED pending checklist T11's "realistic measured resource envelope" (`checklist:245`) and added to §D.4. §C.2 maps K6 to OF-1/OF-2 and G-PROV, K7 to OF-2/OF-7, and K8 and N5 to G-ARM (audit `:193-200`) |
| H7-R9 | Applied | "No ruling is needed" now cites ledger `:810` and S5 draft `:404`. PROPOSED replacement wording, for RC-2, is given for the OF-2 clause (§D.2 Q-1) and the §1.5(d) digest (§B.3). Neither is applied |
| H7-R10 | Applied | Open questions renumbered Q-1..Q-8, with every cross-reference updated. S5 draft Q8/Q9/Q10/Q12 keep their own numbers. The ledger heading date is now `<recording date>`. The TB-F1 re-acceptance consequence is labelled "Inference, not an owner rule" |

No finding was rejected. Beyond the findings, one statement was corrected: the executor line no longer says HEAD equals `521d8f2`. HEAD is `c991d2d`, and that commit touches only a skill file.

---

## Coordinator acceptance (2026-09-27)

**ACCEPTED.** Reviewer: the coordinating session. The artifact was the executor draft plus the fix round, which applied all 17 findings of two refute-first reviews. The coordinator read §A, §B.2, §C.8 and §D–§E in full.

- **RC-5 recorded:** the §E text, as the [ledger entry "Coordinator assignment — RC-5 host checks (recorded) and RC-4 seed view (slice pending the operator)"](../superpowers/plans/2026-09-18-full-e1-execution-slices.md#coordinator-assignment--rc-5-host-checks-recorded-and-rc-4-seed-view-slice-pending-the-operator-2026-09-27). The Q12 resolution to the stricter reading is a coordinator act: it only adds gates.
- **RC-4:** this note's §B.2 recommendation is put to the operator at CP-1a, as item 5 of the [H1 r2 packet](2026-09-27-s5-part-a-measurement-proposal-r2.md). The RC-4 assignment is not met until the operator names the slice.
- **Cost (cross-handoff critic X-16):** H7 did **not** resolve cost. Host spend and sizing stay owed before CP-8, pending checklist T11's measured envelope. Q-8 (whether host spend counts against the $700 ceiling) is folded into the commissioning packet's single consolidated CP-2 question F-4 (critic X-13).
- **Operator questions carried forward:** CQ-1..CQ-3, Q-1..Q-7 (§D). None blocks the assignment.

**Not granted:** unchanged from the Status line.
