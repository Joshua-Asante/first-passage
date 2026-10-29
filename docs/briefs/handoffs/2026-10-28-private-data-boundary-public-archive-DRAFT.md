# Private-data boundary between first-passage and first-passage-archive: CC handoff

**Brief type:** CC handoff
**Status:** DRAFT r3 (2026-10-28; r2 applied Joshua's review, r3 adds the cross-session handling phase). Dispatched to Codex 2026-10-28 under a narrower ticket (no private reads by Codex); returned `DONE_WITH_CONCERNS`, §4 `RESOLVED`. Sanitized output: [proposal](../../notes/2026-10-28-private-data-boundary-proposal-DRAFT.md). Private evidence stays local, uncommitted. Committed at Joshua's direction (2026-10-28) as an unruled draft: it decides nothing.
**Must run locally.** Some later phase may need the operator's machine (gitignored private areas, the private `first-passage-archive` repo). Running locally does **not** make a read safe. Whatever this session reads goes to its model provider, so Phase 1 decides which reads are allowed before any protected file is opened.
**Requested by:** Joshua, 2026-10-28 (direct chat). Split out of the session that built the strategy data inventory (PR #945).
**Rule 2 budget:** one session, $0, K=0. Read and draft only. No commit, push or PR in this task. Stop and return after two failed corrections.

## §0. Rule-0 reads (permitted from the start: governance text only)

These are public, committed governance documents. Read them before opening anything else.

- `AGENTS.md` §Public-clone posture, §Private read surface, and Rules 12, 13, 29 and 41. Full statements are in `docs/operational_rules.md` §Core rules.
- `docs/adr/2026-08-14-repo-public-visibility-transition.md` and `docs/ltm/README.md`.
- Campaign §60 and its addenda (agent read access to Pine and ports, and the VM terms) in `docs/briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md`.
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` Addendum 2026-10-24b (credential custody), and the global `~/.claude/CLAUDE.md` §Data safety.
- `scripts/dispatch_codex.ps1` and `tests/scripts/test_dispatch_codex.py` (source only).
- The `gh` environment-variable precedence: `GH_TOKEN` / `GITHUB_TOKEN` override stored credentials (https://cli.github.com/manual/gh_help_environment).

## §0.5. Open questions (findings, not stop conditions)

Each item below was observed on 2026-10-28 at `origin/main` `ecb87d8`. Treat each one as a question to answer. A finding that an existing rule already covers a case is a result, not a reason to stop.

1. **Public commits already contain backtest dollar figures,** for example in the Phase 1 reconciliation RESULTS, the Aegis+ORB combined-book RESULTS and the Q-TXG-1 re-argument brief. Does any rule permit them, forbid them, or say nothing? Is Rule 13's "locked figures" meant to cover research backtests?
2. **Public documents link to the private archive.** Those links 404 for public readers, as expected. Are such links useful? Are they permitted in public docs? Do they reveal anything (repo name, paths, commit IDs, file names)?
3. **Archive extraction.** Is there a rule for what may be copied from the archive into the public repo, and for whether an external agent (Codex) may read the archive? On 2026-10-28 this was handled ad hoc: the coordinator read archive files itself and passed Codex only identities, hashes, windows and counts.
4. **Where private inputs live.** They are spread across `Downloads`, `private_overrides/`, `local_artifacts/`, `core/data/tv_exports/`, and the archive. Only some are hash-indexed. Is a registered location required?
5. **Provider boundary.** Which data classes may each agent read, given where its reads go: Claude sends to Anthropic, Codex to OpenAI, and a VM has its own terms? Does §60's "agents may read in place" mean transmission to the provider is permitted?
6. **Credential isolation in Codex dispatch.** Codex reported that "the connected GitHub identity is Joshua's". The agent PAT and the operator credential can both identify as Joshua, so the identity alone proves nothing.
7. **Cross-session handling.** Sessions pass private files to each other by path (in chat, tickets and scripts), but worktrees and session scratchpads are deleted, and paths move. Each session also re-decides what it may read and hand on. On 2026-10-28 a set of derived counts from private exports (trade counts, windows, deadline holds; no prices or P&L) was held in a session scratchpad pending a ruling on whether such outputs are publishable. Is there a durable home, a stable way to refer to a private file, and a rule for derived outputs?

## §1. Question and the decision it changes

**Question:** What rule governs data movement between surfaces (private local areas, the private archive, the public repo) and agents/providers (Claude, Codex, the VM)?

**Decision it changes:** what each agent may read, copy, cite, publish, or hand to another agent or session. That includes whether existing public figures and archive links are kept, what a Codex ticket may contain, and where private files live and how sessions refer to them.

## §2. Phases (in order; each phase may open only what earlier phases permit)

1. **Verify existing permissions.** Using only the §0 governance text, build a table of data class × agent/provider. Mark each cell PERMITTED (cite the rule), FORBIDDEN (cite the rule) or UNRULED. Data classes: account data, P&L / backtest dollars, vendor bar/trade data, Pine, runtime ports and effective inputs, identities and hashes, private paths and repo links, credentials. **Do not open protected files in this phase.**
2. **Inventory only permitted surfaces.** List where each class lives. For a class whose content this agent may not read, record only metadata visible without reading content: that a path exists, which index covers it (`PRIVATE_EVIDENCE.sha256`, `SHA256SUMS`, `BOOK_SOURCES.sha256`), and which committed docs cite it. If the Phase 1 table leaves a needed read UNRULED, stop that read and list it for Joshua.
3. **Credential review (question 6).** Inspect `dispatch_codex.ps1`'s credential-selection logic and the `gh` precedence rule. You may run `gh auth status` in the dispatch's environment; it reports the token **source** (environment vs keyring) without printing the token. Never print, hash or log a token, and never open `~/.codex/auth.json` or a keyring. Conclude "isolated" only if the evidence shows the operator credential cannot be selected; otherwise record **UNRESOLVED** with what is missing.
4. **Draft a data-movement policy.** Propose rule text as amendments to the owner it belongs to (Rule 29: one owner; probably Rule 13 and AGENTS.md §Public-clone posture). Cover provider boundaries, archive extraction (which fields are publishable), archive links in public docs, registered private-input locations, and the remediation options below.
5. **Remediation options (proposed, unexecuted).** For existing public exposures, classify each keep / scrub-going-forward / needs-security-response. Say plainly that deleting a file does **not** remove it from git history. The 2026-10-15 "delete, rely on history" precedent only stops new readers of the current tree. **If any actual secret is found** (token, key, credential), stop the policy work, record its location privately, and report to Joshua for a security response. Revocation or rotation comes first; history rewriting is a separate decision (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
6. **Propose the cross-session handling model (question 7).** Built on the Phase 1 table, so the data classes are not redefined. Starting hypothesis, to test against the Phase 2 inventory and amend or reject with reasons:
   - **One private store** outside every worktree and scratchpad, append-only and indexed by SHA-256. A file enters it before any session relies on it; scratchpad results worth keeping are promoted before the session ends.
   - **Refer by hash, not path.** Handoffs, tickets, public docs and memory cite `sha256 + data class`. A local lookup maps hash to location and verifies the hash before use (the pattern `run_four_firm_remc.py` already uses); a mismatch is BLOCKED.
   - **Label once, at intake.** The file's data class (from the Phase 1 table) fixes which agents/providers may read it. Sessions look the label up instead of re-deciding.
   - **Derived outputs inherit the strictest input label** unless a named rule lowers it (for example: counts, windows and hashes publishable; prices and P&L not). Each lowering rule is a candidate UNRULED item for Joshua.
   - **Consequences to state:** routing (cloud sessions and Codex receive only data their label permits; anything else is "Must run locally" with the label as the reason) and a handoff field listing private inputs as hash, label and permitted readers.
   List the options for Joshua on: the store's location (outside the repo, a gitignored area of the primary checkout, or the private archive, subject to vendor licensing), backup, and enforcement level (convention plus lookup; a small `put / get / verify` tool; or read-blocking hooks). Recommend the least enforcement that covers a concrete failure found in Phase 2. Propose only; build nothing.
7. **Joshua decides the UNRULED cases.** Return them as a list with options. Do not choose.

## §3. Outputs (two, kept separate)

- **Private evidence** (inventory rows, exact paths, private links, hashes, the credential-review notes). Write it only to a gitignored local location that Phase 1 shows is permitted, and return its path to Joshua. Never commit it, and never paste it into a public document or another agent's prompt.
- **Draft policy proposal** (sanitized). It contains the data-class table, the proposed rule text, the cross-session handling model with its options, the remediation options with exposures described by category (e.g., "N public files contain research backtest dollars"), and the UNRULED list. It names no private paths, hashes, archive URLs, figures or identifiers. Return it as a local file. **Publishing it is a later step**, after Joshua rules on the UNRULED cases and approves its disclosure scope.

## §4. Hypothesis (falsifiable)

**H:** One data-class × agent/provider table with an owner per cell covers every movement in §0.5.

**Falsified if:** some movement needs a case-by-case ruling that no class rule can express. List those cases for Joshua; do not invent rules.

## §5. Forbidden moves

- Do not read a protected file before Phase 1 marks its class PERMITTED for this agent/provider.
- No deletion, scrubbing, moving or rewriting of files or history. No force-push. No change to the archive repo, branch protection or credentials.
- No commit, push or PR in this task. No edits to AGENTS.md, `operational_rules.md`, ADRs or STATE (Rule 3: the operator decides).
- No private contents in the proposal or in any other agent's prompt. Codex may review only the sanitized proposal, and only after Joshua approves its disclosure scope.
- Never print, hash, copy or log a credential.

## §6. Gate and return status

Return one of:
- `DONE`: both outputs exist as local files, Phases 1–6 are complete, and the UNRULED list is returned.
- `DONE_WITH_CONCERNS`: as `DONE`, plus a list of concerns (e.g., a surface left un-inventoried because its read was UNRULED).
- `NEEDS_CONTEXT`: a Rule-0 read contradicts this card in a way that changes the task. Name the contradiction.
- `BLOCKED`: a needed permission or access is missing. Name it.
- `UNRULED`: the §4 hypothesis failed. List the cases.

§4 verdict: `RESOLVED` if the table covers every case, `FALSIFIED` if any case needs its own ruling, `AMBIGUOUS` if a needed read stayed UNRULED.

The later publication step (not this task): Joshua rules, a reviewer checks the full proposal diff against the data-class table, the scan below runs clean, then a PR is opened and Codex reviews it (Rule 5).

## §10. Audit hooks

- Every Phase 2 read is backed by a PERMITTED cell from Phase 1, with the cited rule.
- The proposal names no private path, hash, archive URL, figure or identifier. The publication review is a full read of the diff, not only the scan.
- The return answers each §0.5 question as covered / uncovered / UNRULED, with the evidence held in the private output.

Publication scan. It distinguishes "no matches" (`rg` exit 1) from an error (exit 2) and supplements the diff review; it does not replace it:

```bash
f="<sanitized proposal path>"
pat='(\$|USD|EUR|£|€)\s?-?[0-9][0-9,]*(\.[0-9]+)?|[0-9][0-9,]*(\.[0-9]+)?\s?(USD|dollars|k\b)|first-passage-archive|[0-9a-f]{12,64}|private_overrides|local_artifacts|Downloads|account[ _-]?(id|number)|strategy\(|indicator\(|ta\.|request\.security'
rg -n -i -e "$pat" "$f"; rc=$?
case $rc in 0) echo "REVIEW: matches above";; 1) echo "OK: no matches";; *) echo "ERROR: scan failed (rc=$rc)"; exit 2;; esac
```
