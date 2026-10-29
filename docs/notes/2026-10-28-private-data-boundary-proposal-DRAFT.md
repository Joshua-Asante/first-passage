# Data movement policy proposal

**Status:** Codex return (2026-10-28) for the [handoff](../briefs/handoffs/2026-10-28-private-data-boundary-public-archive-DRAFT.md), committed unedited below this line at Joshua's direction as an unruled draft. Since ruled: derived-output release, option B (named fields; [AGENTS.md](../../AGENTS.md) *Derived outputs*, PR #963). The other open choices await Joshua.

Draft only. No permission, disclosure scope or implementation is approved by this proposal. Existing rulings remain binding. Evidence and source details are held separately.

## Findings and ownership

The current rules already cover research backtest dollars, archive links, archive extraction, registered frozen inputs and the principal provider boundary. Amend AGENTS.md's Public-clone posture as the class-policy owner; Rule 13 in docs/operational_rules.md should point there. Campaign section 60 owns the narrow source-read and per-run VM exceptions. Rule 12 and the surface-allocation ADR's credential-custody addendum own credentials. Avoid creating a competing policy owner.

## Data class and recipient table

PERMITTED means only within the cited conditions, not a general transfer grant. UNRULED means no read or disclosure grant follows. The VM is a destination and execution surface, not a model provider. Another service requires its own recipient permission. This task additionally forbids Codex from reading every private class, even where standing policy could otherwise allow a task-specific read.

| Class | Claude / Anthropic | Codex / OpenAI | Designated VM | Public disclosure | Owner |
|---|---|---|---|---|---|
| Account data, including account P&L | PERMITTED only for a task naming it; never quote or hand off | FORBIDDEN | PERMITTED only as opaque input to the specifically admitted verified envelope; human or agent inspection FORBIDDEN | FORBIDDEN | AGENTS.md class rules; Rule 13; campaign section 60 VM addenda |
| Research backtest dollars | PERMITTED when authorized; locked-book figures retain their stricter prohibition | PERMITTED for public research figures in reviewed PRs; other private research dollars FORBIDDEN in this task, standing scope UNRULED | PERMITTED only within a named run admission | PERMITTED only in lab RESULTS, subject to locked-book restrictions; elsewhere cite owner | AGENTS.md class rules; Rule 13 |
| Vendor bar and trade data | UNRULED as a general provider grant; named task, licensing and specific admissions must establish permission | FORBIDDEN in this task; general private vendor-data provider admission UNRULED | PERMITTED only for the inputs and runs explicitly admitted | FORBIDDEN for vendor CSV bodies | Rule 13; campaign section 60; VM policy |
| Pine | PERMITTED only for the accepted sources, read in place under section 60 | FORBIDDEN | FORBIDDEN | FORBIDDEN for source and protected values | Rule 13; campaign section 60, including provider amendment |
| Runtime ports and effective inputs | PERMITTED only for the accepted sources, read in place | FORBIDDEN | PERMITTED only by named run admission, direct transfer and teardown terms | FORBIDDEN for bodies and protected values | Rule 13; campaign section 60 |
| Non-account source identities and hashes | PERMITTED as admitted metadata; no authority to read the underlying content follows | PERMITTED as the limited archive handoff fields, alongside windows and counts; no content grant follows | PERMITTED as necessary admitted-run metadata | PERMITTED for approved input citations; this draft intentionally omits actual metadata | AGENTS.md archive and private-input class rules |
| Private locations and archive links | PERMITTED for authorized references; protected identifiers remain forbidden | PERMITTED for committed governance metadata only in this task | PERMITTED only within named input and host terms | PERMITTED for archive links and relative input citations with digest; absolute home locations FORBIDDEN in new public text | AGENTS.md class rules; Rule 13; retrieval guide; visibility ADR citation addendum |
| Credentials belonging to the operator, broker or restricted host | FORBIDDEN to receive or hold | FORBIDDEN to receive or hold | Operator provisions access; agent receipt FORBIDDEN | FORBIDDEN | Rule 12; credential-custody addendum; VM policy |
| Agent-owned scoped repository credential | PERMITTED for authorized authentication, never quote or log | PERMITTED for authorized authentication, never quote or log; this task permits only source/login diagnostics | UNRULED for transfer to VM; no grant inferred | FORBIDDEN | Rule 12; credential-custody addendum |

Identifiers belonging to an account never enter the metadata exception. Public research figures do not make their private source exports readable. A provider may receive only what its agent may read; running locally does not change that boundary.

## Proposed amendments, pending decision

Retain the existing class rules and add the following to their owner only after the operator resolves the choices below:

“A handoff names each private input's digest, class, permitted readers and providers, owning admission, and allowed purpose. A location is a lookup hint, not authority. Resolve and verify bytes before use; a mismatch or unknown permission blocks that input. Class labels carry the ruling and its scope; newer operator restrictions override older labels. A recipient checks current authorization before access.”

“Derived outputs retain the strictest source restrictions unless a named, scoped release rule authorizes specified fields and destinations. The existing archive-to-Codex metadata allowance remains narrow. It does not release arbitrary derived statistics for public disclosure. Approved release records identify lineage, transformation, permitted fields, recipient and policy owner without reproducing protected content.”

“Archive extraction follows the extracted content's class, independent of where it was stored. Source identities unrelated to an account, digests, windows and counts may enter an authorized Codex ticket under the existing archive rule. Source bodies, prices, account information and protected values do not travel through that exception. Public publication requires a separate class-specific permission.”

These additions are proposals, including the general derived-output default; they are not retroactive readings of an existing rule. Preserve the existing relative-location-plus-digest citation requirement unless the operator expressly replaces it. Keep source and host exceptions with their current owners.

## Cross-session handling model

Accept the goal of durable, indexed evidence before reliance; amend the proposed implementation to reuse the existing content-addressed evidence archive and registry where licensing and class permit. Existing source-read-in-place and run-only VM restrictions override storage convenience: an intake operation must not copy protected sources into a new store without permission. Public indexes must not acquire confidential labels or metadata merely to support this model.

Use a digest plus class as stable identity, with the existing relative citation and a restricted local locator. Verify the digest before consumption. The inspected research runner verifies pinned locations and digests, including the manifest before parsing; it does not implement a general hash-to-location resolver. Do not describe that resolver as already available.

Label once at intake with lineage, policy owner and admission scope, then check current permission at every read and handoff. A label cannot freeze a revoked permission or waive a run limitation. Promote retained scratch results before session teardown only to a class-permitted destination. Temporary run copies still require their existing teardown.

The committed evidence mechanism already supplies content-addressed preservation, registration and audit. Its source documentation records losses from disposable storage. Recommend convention plus the existing verified preservation/audit mechanism first, with a recipient permission check in the handoff. Do not build another store or tool before identifying a remaining failure it must solve. Storage location and backup remain operator choices; this recommendation selects neither.

Routing follows recipient permission. Cloud workers and Codex receive only admitted classes. If a local surface is required, mark the task Must run locally and name the admission; locality alone cannot authorize a prohibited recipient.

## Remediation options, unexecuted

The three brief-nominated public artifacts have currency-pattern matches. This is a bounded syntactic observation, not a semantic classification of every match or a repository-wide exposure count; no protected values were reproduced or reviewed to classify them.

| Category | Proposed disposition |
|---|---|
| Research dollars in eligible lab RESULTS | Keep when provenance and non-locked classification are confirmed by an authorized reviewer |
| Research dollars in briefs or other publication surfaces | Scrub going forward, replacing them with owner citations; review the nominated brief under this rule |
| Locked-book figures, source bodies, account data or vendor CSV bodies in public text | Scrub going forward under the existing prohibition; security-response need depends on the actual content and incident assessment |
| Archive links and approved input metadata | Keep when useful for authorized retrieval; explain restricted access and avoid adding protected metadata |
| An actual secret | Needs security response: revoke or rotate first, then decide history treatment separately |

No actual secret was identified in the permitted reads. This was not a secret audit. Deleting or editing a file does not remove earlier content from git history. The earlier delete-and-rely-on-history precedent only reduces exposure in the current tree. See [GitHub's sensitive-data guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

## Credential finding

UNRESOLVED. Static dispatch logic requires a candidate agent token, rejects a different token format, supplies it as the preferred environment credential and clears the secondary variable during child execution. The [CLI precedence documentation](https://cli.github.com/manual/gh_help_environment) supports that selection behavior. The source tests were inspected, not executed; they do not establish live child credential provenance or repository scope. The single permitted status attempt did not establish a token source or login. A prefix and a shared account login cannot prove ownership, scope, or that this session used the dispatch. No credential was printed, copied or hashed.

## UNRULED choices for the operator

- General derived-output release: retain source restrictions except the existing narrow metadata handoff; or admit specified aggregate fields after an authorized disclosure review. Choose fields, recipients and whether publication is allowed; counts and windows are not a universal public exception.
- General private vendor-data provider access: require named task and licensing approval for each source; or adopt an explicit class-wide recipient admission subject to licensing. No new admission is assumed here.
- Private research-dollar access outside the reviewed-public-PR exception: keep Codex excluded; or name a limited additional admission, preserving locked and account restrictions.
- Durable store location: outside all repositories; an ignored area in the primary checkout; or the existing private archive subject to licensing and existing read-in-place restrictions. Decide migration exceptions separately if needed.
- Backup: a verified existing archive copy where admitted; a separate controlled encrypted backup; or both, with retention and restore-check responsibility named.
- Enforcement: convention plus existing archive/audit and permission checks; a small authorized extension for lookup and labels; or read-blocking hooks if a concrete bypass warrants them. Prefer the first until a residual failure is evidenced.
- Credential assurance acceptance: operator attestation of agent ownership and scope plus a token-free child source diagnostic; or an independently verifiable scoped identity and corresponding child diagnostic. Until evidence meets the chosen criterion, isolation remains UNRESOLVED.

## Question coverage and hypothesis

Question 1 covered by current research-versus-locked rules; question 2 covered by link permission; question 3 covered by class-based extraction and recipient restrictions; question 4 covered by frozen-input registration; question 5 covered for explicit classes, UNRULED for general private vendor/research admissions; question 6 uncovered as a demonstrated isolation claim; question 7 UNRULED for general derivation release, durable store and enforcement choices.

Hypothesis RESOLVED at the classification-model level: all seven questions can be expressed by class, recipient, operation, purpose and named admission under one table and its owners. No observed movement requires an intrinsically unclassifiable case ruling. This is not a claim that every cell is decided or every surface inventoried. External private surfaces were intentionally not inventoried; the operator choices above remain open.

Publication remains a later step requiring operator rulings and disclosure approval, independent review and a full disclosure review in addition to a clean scan.

Scan verification: the prescribed rg command could not start because rg is unavailable. The same pattern was run using git grep with PCRE, case-insensitive matching and explicit file selection: no matches, exit 1. An initial fallback run flagged two generic policy phrases rather than disclosed values; those phrases were clarified without changing the rule. A full author read found no actual private locations, digests, archive URLs, figures or identifying values. This is author verification, not independent publication approval.
