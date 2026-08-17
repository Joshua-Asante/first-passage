export const meta = {
  name: 'handoff-verify-panel',
  description: 'Fan-out Phase-0 verification of an external handoff packet before any step executes',
  whenToUse:
    'Before executing any substantial external handoff -- web-advisor note, CC spawn brief, Cursor Phase-0 packet, Downloads-staged artifact -- that claims repo state. The single most-fired lesson in memory (feedback_web_advisor_handoff_confabulates_repo_state, 7 documented instances 2026-06-06 through 2026-07-11): handoffs narrate phantom files, unlanded edits, already-executed programs, fictional in-flight work, fabricated labels, and wrong self-referential fire counts. The handoff-verify SKILL stays the quick inline gate; this workflow is the heavy edition for packets with many claims -- same Phase-0 checks, run as independent parallel verifiers. Pass args.targetPath = path to the handoff doc, OR args.handoffText = the pasted packet text.',
  phases: [
    { title: 'Extract', detail: 'claim manifest + checkout currency' },
    { title: 'Verify', detail: 'one independent verifier per claim dimension' },
    { title: 'Adjudicate', detail: 're-check hard fails, emit PASS / NEEDS_CONTEXT' },
  ],
}

// ---- input handling -------------------------------------------------------

const cfg = args && typeof args === 'object' && !Array.isArray(args) ? args : { targetPath: args }
if (!cfg || (!cfg.targetPath && !cfg.handoffText)) {
  throw new Error(
    'handoff-verify-panel requires args.targetPath (path to the handoff doc) or args.handoffText (the pasted ' +
      'packet text), e.g. Workflow({ name: "handoff-verify-panel", args: { targetPath: "docs/briefs/handoffs/<packet>.md" } })'
  )
}
const sourceRef = cfg.targetPath || '(inline handoff text)'
const sourceInstruction = cfg.targetPath
  ? `Read the ENTIRE handoff packet at ${cfg.targetPath}.`
  : `The handoff packet text follows between the markers:\nBEGIN HANDOFF PACKET\n${cfg.handoffText}\nEND HANDOFF PACKET`

// ---- schemas --------------------------------------------------------------

const claimList = (itemProps, required) => ({
  type: 'array',
  items: { type: 'object', properties: itemProps, required },
})

const MANIFEST_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string', description: 'one-paragraph neutral summary of what the handoff asks to be done' },
    paths: claimList(
      { path: { type: 'string' }, quote: { type: 'string' } },
      ['path', 'quote']
    ),
    edits: claimList(
      { claim: { type: 'string' }, target: { type: 'string', description: 'the file/region claimed edited' }, quote: { type: 'string' } },
      ['claim', 'target', 'quote']
    ),
    statuses: claimList(
      { doc: { type: 'string' }, claimed_status: { type: 'string' }, quote: { type: 'string' } },
      ['doc', 'claimed_status', 'quote']
    ),
    already_executed_risk: claimList(
      { deliverable: { type: 'string' }, search_terms: { type: 'string', description: 'unique symbols/titles to grep for' }, quote: { type: 'string' } },
      ['deliverable', 'search_terms', 'quote']
    ),
    inflight_premises: claimList(
      { claim: { type: 'string' }, quote: { type: 'string' } },
      ['claim', 'quote']
    ),
    identity_premises: claimList(
      { claim: { type: 'string' }, quote: { type: 'string' } },
      ['claim', 'quote']
    ),
    self_referential: claimList(
      { claim: { type: 'string' }, registry_file: { type: 'string', description: 'the on-disk file that owns the true count/record' }, quote: { type: 'string' } },
      ['claim', 'registry_file', 'quote']
    ),
    posture_numeric: claimList(
      { claim: { type: 'string' }, quote: { type: 'string' } },
      ['claim', 'quote']
    ),
    frozen_gates: claimList(
      { gate: { type: 'string' }, quote: { type: 'string' } },
      ['gate', 'quote']
    ),
  },
  required: [
    'summary', 'paths', 'edits', 'statuses', 'already_executed_risk', 'inflight_premises',
    'identity_premises', 'self_referential', 'posture_numeric', 'frozen_gates',
  ],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    checked_count: { type: 'number' },
    clean: { type: 'boolean' },
    contradictions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          on_disk: { type: 'string', description: 'what the repo actually shows: path @ sha, MISSING, actual status, actual count' },
          severity: { type: 'string', enum: ['HARD_FAIL', 'STALE', 'NOTE'] },
          evidence: { type: 'string', description: 'the executed command output or exact file bytes' },
        },
        required: ['claim', 'on_disk', 'severity', 'evidence'],
      },
    },
    notes: { type: 'string' },
  },
  required: ['checked_count', 'clean', 'contradictions', 'notes'],
}

// ---- Extract --------------------------------------------------------------

phase('Extract')
log(`Handoff-verify panel starting on ${sourceRef}`)

const checkoutPromise = agent(
  `Run the checkout-currency check for a handoff-verification panel in the First Passage repo (a futures ` +
    `prop-trading research/ops monorepo). Execute and paste the output of each: "git fetch origin", ` +
    `"git status -sb", "git rev-parse --show-toplevel", "git rev-parse --abbrev-ref HEAD", ` +
    `"git log --oneline HEAD..origin/main | head -20", "git worktree list". Report: which worktree/branch this ` +
    `session is in, whether it is behind origin/main and on which files, and any sibling worktrees with ` +
    `uncommitted state -- memory-tier session records can be AHEAD of git, so a handoff may reference artifacts ` +
    `sitting uncommitted in a sibling worktree (both directions matter). Report only; change nothing.`,
  { label: 'checkout-currency', phase: 'Extract', effort: 'low' }
)

const manifest = await agent(
  `You are the claim extractor for a Phase-0 handoff-verification panel in the First Passage repo (a futures ` +
    `prop-trading research/ops monorepo). ${sourceInstruction}\n\n` +
    `External handoffs (web-advisor notes, cross-session briefs) have confabulated repo state 7 documented ` +
    `times. Your job is extraction ONLY -- do not verify anything, do not judge plausibility. Decompose the ` +
    `packet into every checkable claim, sorted into these dimensions (empty arrays are fine):\n` +
    `- paths: every file/dir the packet treats as existing or load-bearing (scripts, ADRs, templates, RESULTS, ` +
    `skills, data files).\n` +
    `- edits: every claim that an edit/landing already happened ("stamped", "backfilled", "landed", "merged", ` +
    `"mirrored to", "committed", "closed this session"), with the target file/region.\n` +
    `- statuses: every claimed ADR/brief/closure status (Accepted, Proposed, SUPERSEDED, a closure verdict, ` +
    `"still open call").\n` +
    `- already_executed_risk: every work item the packet PLANS that could already have run in-repo (deliverable ` +
    `name + unique grep terms) -- a whole proposed program can already be substantially executed.\n` +
    `- inflight_premises: every claim that named work is currently in progress or planned-as-active ("an ` +
    `Algorithm pass is in progress", "hand results to X"), including downstream consumers the packet feeds.\n` +
    `- identity_premises: structural/identity claims about the repo -- headings or rule numerals said to exist, ` +
    `naming conventions assumed (ADR numbering), labels/phrases presented as established repo vocabulary ` +
    `("VENUE-DEAD", "positive control", a named standing gate).\n` +
    `- self_referential: fire counts, instance numbers, "already at N" claims about lessons/registries, with the ` +
    `on-disk file that owns the true record.\n` +
    `- posture_numeric: live-posture assumptions (what is deployed/armed/open) and specific constants (risk %, ` +
    `DD_TRIGGER, anchors, prices).\n` +
    `- frozen_gates: any campaign gate the packet freezes or relies on (DSR K, placebo clause, family size).\n` +
    `Quote the packet verbatim for every claim -- the verifiers must be able to check the exact assertion, not ` +
    `your paraphrase of it.`,
  { label: 'extract-claims', phase: 'Extract', schema: MANIFEST_SCHEMA }
)
if (!manifest) throw new Error('claim extraction agent returned no result -- cannot verify')

// ---- Verify ---------------------------------------------------------------

phase('Verify')

const DIMENSIONS = [
  {
    key: 'paths',
    title: 'Named paths exist',
    guidance:
      'For each claimed path: run "git ls-files -- <path>" and Glob it; for gitignored-but-expected local data ' +
      '(vendor CSVs, Pine) use "rg --no-ignore --files" or a direct existence check, and remember absence in one ' +
      'named location is not absence -- enumerate the parent class (ls -d parent/*) before declaring MISSING. A ' +
      'load-bearing path that is absent is HARD_FAIL. Do NOT create anything to make the packet coherent.',
  },
  {
    key: 'edits',
    title: 'Claimed edits actually landed',
    guidance:
      'For each claimed edit/landing: run "git log --oneline -- <target>" and re-Read the target region to ' +
      'confirm the claimed bytes are actually there. A revision claiming "closed/backfilled/stamped this ' +
      'session" is unverified until git log + the bytes confirm it -- a handoff author has no more disk access ' +
      'than the original. A claimed edit with no matching commit and no matching bytes is HARD_FAIL.',
  },
  {
    key: 'statuses',
    title: 'ADR/brief status vs claim',
    guidance:
      'Open each cited ADR/brief and read the on-disk status line and any Addendum. Closure vocabulary in this ' +
      'repo is the FILENAME: Q-...-closure-<verdict> with verdicts like hold|scope-split|ambiguous|moot|' +
      'resolved-... -- an invented field like "disposition: PARK" is itself a contradiction. A packet saying ' +
      '"open call"/"still Proposed" when an Addendum already ratified is STALE; a fabricated status is HARD_FAIL.',
  },
  {
    key: 'already_executed_risk',
    title: 'Premises not already executed',
    guidance:
      'For each planned deliverable: rg the unique terms across lab/, docs/, scripts/, .claude/skills/; check ' +
      '"git log --all --oneline" for matching landings and look for on-disk RESULTS/closures. Open the artifact ' +
      'each follow-up cites -- not just audit prose -- and check whether it ALREADY satisfies the ask (an author ' +
      'may cite by path without reading the section). Re-running an already-scored one-shot test is the worst ' +
      'outcome this panel exists to prevent: already-executed work is HARD_FAIL.',
  },
  {
    key: 'inflight_premises',
    title: 'Named in-flight work exists',
    guidance:
      'For each in-progress/planned-active claim: check "git log --all" recent history, the working tree, and ' +
      '"git worktree list" (then inspect sibling worktrees for uncommitted state -- memory-tier records can be ' +
      'AHEAD of git in a sibling tree). A downstream consumer that does not exist ("hand results to the pass in ' +
      'progress") is HARD_FAIL; work that exists under a different shape/name is STALE with the real shape named.',
  },
  {
    key: 'identity_premises',
    title: 'Structural/identity premises hold',
    guidance:
      'For each structural claim: verify headings/numerals actually exist where claimed (and that a claimed-new ' +
      'numeral is not already taken -- committing a second "Rule 1" once nearly created two conflicting rules); ' +
      'rg -F the exact label/phrase repo-wide before treating it as established vocabulary (zero hits for a ' +
      'confidently-used label like "VENUE-DEAD" is HARD_FAIL); ADR convention here is date-prefixed ' +
      'YYYY-MM-DD-title.md, never sequential NNN -- an NNN scheme in the packet is a reliable tell of a ' +
      'no-repo-read authoring environment and at minimum STALE.',
  },
  {
    key: 'self_referential',
    title: 'Self-referential counters match the registry',
    guidance:
      'For each fire count / instance number / "already at N": open the named registry/memory file on disk and ' +
      'COUNT the actual instances yourself. The packet author cannot read that file, so its counters are as ' +
      'confabulatable as a path -- one packet claimed a lesson was at count 7 when the disk showed 6, inside a ' +
      'document billing itself as the anti-instance of that very lesson. An artifact claiming to be the ' +
      'anti-instance of a confabulation lesson earns no exemption. Wrong count is HARD_FAIL.',
  },
  {
    key: 'posture_numeric',
    title: 'Live posture + constants',
    guidance:
      'Live posture is owned by CLAUDE.md section "Live-execution posture" -- read it there, never trust the ' +
      'packet. The packet is STALE (or HARD_FAIL if the plan depends on it) if it assumes any of: an open FXIFY ' +
      'challenge; an active Aegis->M6J lane; an unbuilt CrossTrade rail; the Striker MYM/MNQ legs deployed at ' +
      'Tradeify; an armed live book. Challenge-era MC pass/bust rates are historical pins, not live ' +
      'probabilities. For any specific constant (risk %, DD_TRIGGER, anchor, price): open the owning bytes ' +
      '(core/dd_protection.py, core/firm_rules.py, or the cited spec/note) and compare.',
  },
]

const active = DIMENSIONS.filter((d) => (manifest[d.key] || []).length > 0)
const skipped = DIMENSIONS.filter((d) => !(manifest[d.key] || []).length)
if (skipped.length) log(`dimensions with zero claims, skipped: ${skipped.map((d) => d.key).join(', ')}`)
log(`verifying ${active.length} dimension(s): ${active.map((d) => `${d.key}(${manifest[d.key].length})`).join(', ')}`)

const verifierResults = await parallel(
  active.map((d) => () =>
    agent(
      `You are one independent verifier in a Phase-0 handoff-verification panel for an external handoff packet ` +
        `(${sourceRef}) targeting the First Passage repo (a futures prop-trading research/ops monorepo). External ` +
        `handoffs repeatedly confabulate repo state; internal consistency is the confabulation signature, so only ` +
        `bytes and executed command output count as evidence. Verify ONLY your dimension. Never repair, author, or ` +
        `edit anything -- report only.\n\n` +
        `Dimension: ${d.title}\n${d.guidance}\n\n` +
        `Claims to verify (JSON, with verbatim packet quotes): ${JSON.stringify(manifest[d.key], null, 2)}\n\n` +
        `For each claim, paste the executed command output or exact file bytes behind your verdict. Report every ` +
        `contradiction with severity HARD_FAIL (a load-bearing claim is false), STALE (was true, superseded on ` +
        `disk -- name the superseding state), or NOTE (minor). clean=true only if every claim checked out.`,
      { label: `verify:${d.key}`, phase: 'Verify', schema: VERIFY_SCHEMA }
    ).then((r) => ({ dimension: d.key, result: r }))
  )
)

const checkout = await checkoutPromise
const collected = verifierResults.filter(Boolean)
const hardFails = collected.flatMap((v) => (v.result ? v.result.contradictions.filter((c) => c.severity === 'HARD_FAIL') : []))
log(`verification done: ${hardFails.length} HARD_FAIL contradiction(s) across ${collected.length} dimension(s)`)

// ---- Adjudicate -----------------------------------------------------------

phase('Adjudicate')
const adjudication = await agent(
  `You are the adjudicator for a Phase-0 handoff-verification panel (First Passage repo). ` +
    `${sourceInstruction}\nRe-read the packet fully yourself.\n\n` +
    `Packet summary from the extractor: ${manifest.summary}\n\n` +
    `Checkout-currency report:\n${checkout}\n\n` +
    `Independent verifier results by dimension:\n${JSON.stringify(collected, null, 2)}\n\n` +
    `Frozen campaign gates named in the packet (verified separately, listed for routing): ` +
    `${JSON.stringify(manifest.frozen_gates)}\n\n` +
    `Before ruling: re-verify every HARD_FAIL contradiction yourself -- open the cited bytes or re-run the ` +
    `cited command -- and discard any that do not hold on your own read, saying so explicitly under "discarded ` +
    `on re-check". Then emit the handoff-verify output block in exactly the shape the ` +
    `.claude/skills/handoff-verify skill defines:\n\n` +
    `If no HARD_FAIL survives:\n` +
    `HANDOFF-VERIFY: PASS\ntoplevel: <path>\nbranch: <name> @ <sha>\nchecked: <bullet list of paths/ADRs/claims ` +
    `verified>\nproceed: <first implementation step>\n\n` +
    `If any HARD_FAIL survives:\n` +
    `HANDOFF-VERIFY: NEEDS_CONTEXT\nfailed: <check + contradiction, quoting the packet verbatim>\non-disk: ` +
    `<path @ sha or MISSING or the actual status/count>\ndo-not: <what the packet asked that must not be done>\n\n` +
    `Standing rules the ruling must reflect: do NOT author missing artifacts to make the packet coherent; ` +
    `premise errors fork the whole plan -- NEEDS_CONTEXT, not improvised repair; a packet may be days behind an ` +
    `ADR Addendum. After the block, list surviving STALE and NOTE items briefly. If frozen_gates is non-empty, ` +
    `add one line recommending the gate-reachability-audit workflow be run on the cited prereg before any ` +
    `pull/scoring executes.`,
  { label: 'adjudicate', phase: 'Adjudicate', effort: 'high' }
)

log(`Handoff-verify panel complete for ${sourceRef}`)
return { sourceRef, manifest, checkout, verifierResults: collected, adjudication }
