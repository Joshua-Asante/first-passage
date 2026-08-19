export const meta = {
  name: 'pre-ratification-adversarial-panel',
  description: 'Refute-first multi-lens adversarial review of a brief/ADR/closure before operator ratification',
  whenToUse:
    'Before ratifying any Pre-Q brief, ADR, lock decision, or closure doc in First Passage -- a green check_brief.py pass is FORM-only and has missed real BLOCKERs before (doubled multiplier, unread ADR clause, claimed-but-unscored screen, missing dedup attestation, false bounding claim -- see MEMORY.md feedback_adversarial_review_before_ratification.md). Pass args.targetPath (or args as a bare path string) pointing to the doc under review; optionally args.extraContext as an array of additional cited file paths reviewers must read in full.',
  phases: [
    { title: 'Form Check', detail: 'mechanical check_brief.py pass, FORM-only' },
    { title: 'Review', detail: '6 independent refute-first lenses read the target + cited doctrine' },
    { title: 'Verify', detail: '2 independent skeptics attempt to refute every non-NIT finding' },
    { title: 'Synthesize', detail: 'final adjudicator re-reads source, issues ratification verdict' },
  ],
}

// ---- input handling -------------------------------------------------------

const cfg = args && typeof args === 'object' && !Array.isArray(args) ? args : { targetPath: args }
if (!cfg || !cfg.targetPath) {
  throw new Error(
    'pre-ratification-adversarial-panel requires args.targetPath (or args as a bare path string) ' +
      'pointing to the brief/ADR/closure doc to review, e.g. ' +
      'Workflow({ name: "pre-ratification-adversarial-panel", args: { targetPath: "docs/adr/2026-08-17-example.md" } })'
  )
}
const targetPath = cfg.targetPath
const extraContext = Array.isArray(cfg.extraContext) ? cfg.extraContext : []
const extraContextLine = extraContext.length
  ? `\n\nThe operator has additionally flagged these cited documents as required full reads for this review: ${extraContext.join(', ')}.`
  : ''

// ---- persona mode (design spec §6) -----------------------------------------
// Structural registry only -- slug/role/tier/office. The full mandate/independence-rule
// prose stays canonical in docs/personas/*.md; each spawned agent reads its own file.
const PERSONA_REGISTRY = {
  cro: { role: 'CRO', tier: 'GRAND', office: 'Middle' },
  cio: { role: 'CIO', tier: 'GRAND', office: 'Front' },
  coo: { role: 'COO', tier: 'GRAND', office: 'Back' },
  cfo: { role: 'CFO', tier: 'GRAND', office: 'Cross-office' },
  'head-of-research': { role: 'Head of Research', tier: 'STRATEGIC', office: 'Front' },
  'head-of-execution': { role: 'Head of Execution', tier: 'STRATEGIC', office: 'Front' },
  'head-of-risk-sizing': { role: 'Head of Risk & Sizing', tier: 'STRATEGIC', office: 'Middle' },
  'head-of-validation': { role: 'Head of Validation', tier: 'STRATEGIC', office: 'Middle' },
  'head-of-engineering': { role: 'Head of Engineering', tier: 'STRATEGIC', office: 'Back' },
  'head-of-governance': { role: 'Head of Governance', tier: 'STRATEGIC', office: 'Back' },
}

const personaMode = Boolean(cfg.tier || (Array.isArray(cfg.personas) && cfg.personas.length))
let personaSlugs = []

if (personaMode) {
  if (cfg.tier !== 'GRAND' && cfg.tier !== 'STRATEGIC') {
    throw new Error(
      `pre-ratification-adversarial-panel persona mode requires args.tier of 'GRAND' or 'STRATEGIC', got '${cfg.tier}'. ` +
        'Omit both args.tier and args.personas entirely to use the original generic-lens mode.'
    )
  }
  if (!Array.isArray(cfg.personas) || cfg.personas.length === 0) {
    throw new Error(
      'pre-ratification-adversarial-panel persona mode requires args.personas: a non-empty array of persona ' +
        'slugs from docs/personas/INDEX.md, e.g. args: { targetPath: "...", tier: "GRAND", personas: ["cio", "coo"] }'
    )
  }
  for (const slug of cfg.personas) {
    if (!PERSONA_REGISTRY[slug]) {
      throw new Error(
        `Unknown persona slug '${slug}' -- not in PERSONA_REGISTRY. Valid slugs: ${Object.keys(PERSONA_REGISTRY).join(', ')}. ` +
          'Check docs/personas/INDEX.md.'
      )
    }
  }
  // Mandatory-CRO rule (design spec §4): every GRAND-tier decision gets CRO review, no exceptions.
  personaSlugs = cfg.tier === 'GRAND' && !cfg.personas.includes('cro')
    ? [...cfg.personas, 'cro']
    : [...cfg.personas]
}

// ---- schemas ----------------------------------------------------------

const LENS_FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    clean: { type: 'boolean', description: 'true if this lens found nothing worth flagging' },
    notes: { type: 'string', description: 'short summary of what was checked, even if clean' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          title: { type: 'string' },
          severity: { type: 'string', enum: ['BLOCKER', 'CONCERN', 'NIT'] },
          location: { type: 'string', description: 'file:line or section this finding is about' },
          claim: { type: 'string', description: 'what the brief asserts' },
          evidence: { type: 'string', description: 'the specific contradicting evidence, with file:line citation' },
          why_wrong: { type: 'string' },
        },
        required: ['title', 'severity', 'location', 'claim', 'evidence', 'why_wrong'],
      },
    },
  },
  required: ['clean', 'findings'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean' },
    rationale: { type: 'string' },
  },
  required: ['refuted', 'rationale'],
}

const PRECONDITION_SCHEMA = {
  type: 'object',
  properties: {
    uncommittedChanges: { type: 'boolean', description: 'true if `git status --porcelain` shows any output for this path' },
    hasCommitHistory: { type: 'boolean', description: 'true if `git log -1` for this path returns at least one commit' },
    rawOutput: { type: 'string', description: 'the verbatim output of both commands' },
  },
  required: ['uncommittedChanges', 'hasCommitHistory', 'rawOutput'],
}

// ---- the six adversarial lenses ----------------------------------------

const LENSES = [
  {
    key: 'doctrine-completeness',
    build: () => `Adversarially review the brief/ADR/closure at ${targetPath} in the First Passage repo (a futures ` +
      `prop-trading research/ops monorepo), acting as a skeptic whose only job is to catch doctrine misrepresentation. ` +
      `Read the ENTIRE target file first. Then identify every ADR, methodology doc, or prior decision it cites as ` +
      `authority for a claim (grep docs/adr/, docs/methodology/, STATE.md, CLAUDE.md as needed) and READ THE FULL CITED ` +
      `DOCUMENT yourself -- not just the clause the brief quotes. For each citation, check: (a) does the brief's ` +
      `paraphrase/quote match what the source actually says, (b) does the brief omit a qualifying clause, exception, or ` +
      `condition present in the source that would change the conclusion, (c) is the citation even real (does the cited ` +
      `section/line exist). This exact failure class has previously produced a real BLOCKER: an unread ADR clause that ` +
      `silently invalidated a brief's conclusion. Return findings via the schema -- one entry per doctrine mismatch, each ` +
      `classified BLOCKER (changes the ruling), CONCERN (weakens but doesn't invalidate), or NIT (cosmetic). If you find ` +
      `nothing, say so explicitly (clean:true) rather than manufacturing a weak finding.${extraContextLine}`,
  },
  {
    key: 'arithmetic-rederivation',
    build: () => `Adversarially review the brief/ADR/closure at ${targetPath} in the First Passage repo. Read the ` +
      `ENTIRE target file. Re-derive every numeric claim from its stated primitives rather than trusting the brief's ` +
      `own arithmetic -- multipliers (risk%, DD_SCALE, lifecycle multiplier compounding), percentages, sample counts ` +
      `(K trial counts, n cohort sizes), thresholds compared against a measured value, and any "N of M" or ratio claim. ` +
      `For each, redo the computation from the primitive numbers stated in the brief (or in a cited source if the ` +
      `primitive isn't inline) and flag any mismatch -- doubled/halved values, wrong N-basis (e.g. comparing a per-trade ` +
      `count against a per-day denominator), transcription errors. This failure class previously produced a real BLOCKER ` +
      `(a doubled multiplier) that survived a 6/6-green mechanical checker pass. Return findings via schema, each with the ` +
      `brief's stated value, your re-derived value, and the exact primitive inputs you used.${extraContextLine}`,
  },
  {
    key: 'screen-scoring-completeness',
    build: () => `Adversarially review the brief/ADR/closure at ${targetPath} in the First Passage repo. Read the ENTIRE ` +
      `target file. For every claim that a gate, screen, or criterion "passed," "cleared," or "was satisfied," verify ` +
      `that the brief (or a script/artifact it points to) actually SHOWS the computation -- not just asserts the verdict. ` +
      `Grep for the referenced script/output/CSV and confirm the claimed number appears in it. A "claimed-but-unscored ` +
      `screen" (the brief says a screen passed but no artifact anywhere actually computed it) is a real BLOCKER class ` +
      `that has previously survived a green mechanical checker. Also check docs/operational_rules.md Rule 8's dedup-first ` +
      `sub-rule: is the brief's dedup-first attestation an EXECUTED, pasted search-tool output, or just a claim that ` +
      `dedup was done? An attestation without executed output is void per Rule 8 sub-rule 8 -- flag as BLOCKER if the ` +
      `brief asserts dedup was done without pasted grep / check_advisor_dedup.py output. Return findings via ` +
      `schema.${extraContextLine}`,
  },
  {
    key: 'input-validity',
    build: () => `Adversarially review the brief/ADR/closure at ${targetPath} in the First Passage repo. This lens ` +
      `checks a DIFFERENT failure class than selection-effect or arithmetic review: whether the brief's EXTERNAL/MUTABLE ` +
      `input facts are still true. Read the ENTIRE target file, then identify every claim that depends on a third-party ` +
      `or mutable fact -- venue/firm rules (trailing-DD mechanics, consistency rules, activity/inactivity rules), ` +
      `fee/spread/contract specs, firm-tier starting balances, data feed provenance -- and independently re-verify each ` +
      `against the actual primary source in this repo (core/firm_rules.py, the relevant docs/spec/ file, or the cited ` +
      `vendor doc) rather than trusting the brief's restatement. A brief can pass every pre-registration / no-p-hacking / ` +
      `discriminating-gate check and still be wrong because ONE input parameter (e.g. a firm's eval-phase DD-lock rule) ` +
      `was modeled incorrectly -- this has happened before and evaded the standard selection-effect lenses entirely. ` +
      `Return findings via schema.${extraContextLine}`,
  },
  {
    key: 'steelman-the-kill',
    build: () => `Adversarially review the brief/ADR/closure at ${targetPath} in the First Passage repo. Read the ` +
      `ENTIRE target file and identify its proposed disposition (ADOPT / KILL / PARK / LOCK / other -- check the ` +
      `§6/§7 gate section or the closing section). Then construct the STRONGEST possible case for the OPPOSITE ` +
      `disposition using only evidence already present in the brief or directly checkable in the repo -- do not invent ` +
      `new data. Check whether the brief's own §5 "forbidden moves" / §6 gate criteria would actually survive ` +
      `your steelman, or whether the brief quietly assumes away the counter-case. Separately, hunt for "false bounding ` +
      `claims" -- any place the brief says a risk/effect/cost is "bounded," "capped," or "limited to X" and verify that ` +
      `bound is actually derived/checked rather than asserted. Also check this repo's M-8 discipline: any §6 ` +
      `threshold phrased as a bare count ("if count ≥ N → action") must carry a qualitative scope (e.g. ` +
      `"production risk-control sites," not just "N files") -- flag bare-count thresholds lacking qualitative scope as ` +
      `a CONCERN. Return findings via schema.${extraContextLine}`,
  },
  {
    key: 'structural-completeness',
    build: () => `Adversarially review the brief/ADR/closure at ${targetPath} in the First Passage repo. Read the ` +
      `ENTIRE target file and, if present, .claude/skills/brief-authoring/SKILL.md for the required structure. Check ` +
      `presence AND substance (not just a header) of: §0 Rule-0 production-code reads, §4 falsifiable ` +
      `hypothesis, §5 forbidden moves, §6 gate/disposition criteria, §10 audit-hooks. Additionally check: ` +
      `(a) if a later section restates §6's floor/headline criteria, does it reproduce them VERBATIM rather than ` +
      `drifting into generic "strict lock criteria" language (a documented failure mode); (b) if the brief records any ` +
      `deliberate "watch, don't act" / restraint decision, is there an explicit "Watch-items" (or equivalent) section ` +
      `giving it the same prominence as action items, not a silent omission; (c) if this is a new ADR/brief/notice, does ` +
      `it show an "amend-before-mint" search (Rule 8 sub-rule 10) confirming no existing owner document should have ` +
      `taken this as an addendum instead; (d) if this is a closure doc, does it carry a "- **Registry:**" line pointing ` +
      `into docs/rejected_candidates.md or stating n/a (Rule 8 sub-rule 9). Return findings via schema.${extraContextLine}`,
  },
]

// ---- persona-mode lenses (design spec §6.2) --------------------------------
// Each persona is spawned exactly like a LENSES entry -- independent agent() call via
// pipeline(), no shared context with any other persona. This is what makes the SR-11-7 /
// 18f-4 independence property (reviewer never sees the proposer's live reasoning, or any
// other reviewer's draft opinion) already true here, not something new to build.
const PERSONAS = personaMode
  ? personaSlugs.map((slug) => ({
      key: slug,
      build: () =>
        `You are the ${PERSONA_REGISTRY[slug].role} persona (${PERSONA_REGISTRY[slug].office} office, ` +
        `${PERSONA_REGISTRY[slug].tier} tier) reviewing ${targetPath} in the First Passage repo ` +
        `(a futures prop-trading research/ops monorepo). First, read your own persona definition in full: ` +
        `docs/personas/${slug}.md -- this states your Domain (what you are accountable for) and your ` +
        `Independence rule. Then check whether docs/personas/${slug}-log.md exists; if it does, read it for ` +
        `your own prior review history. If it does not exist, this is your first review -- say so explicitly ` +
        `rather than fabricating history.\n\n` +
        `Now read the ENTIRE target file at ${targetPath}. Review it strictly from your persona's Domain and ` +
        `mandate -- do not opine outside it. If this decision falls entirely outside your Domain, say so ` +
        `explicitly (clean:true, notes explaining why) rather than manufacturing a finding to seem useful.\n\n` +
        `Flag every disagreement explicitly and specifically -- do not soften toward consensus. You cannot see ` +
        `any other reviewer's input; this is deliberate, matching how a real risk/validation reviewer must form ` +
        `an independent view before seeing the proposer's or any other reviewer's framing. Return findings via ` +
        `the schema, each classified BLOCKER / CONCERN / NIT.${extraContextLine}`,
    }))
  : []

// ---- verify stage: independent skeptics try to refute every non-NIT finding ----

async function verifyLensFindings(reviewResult, lens) {
  if (!reviewResult) {
    return { key: lens.key, clean: true, confirmed: [], disputed: [], refuted: [], nits: [], notes: '(lens agent returned no result)' }
  }
  const findings = reviewResult.findings || []
  const nits = findings.filter((f) => f.severity === 'NIT')
  const toVerify = findings.filter((f) => f.severity !== 'NIT')
  if (toVerify.length === 0) {
    return { key: lens.key, clean: reviewResult.clean, confirmed: [], disputed: [], refuted: [], nits, notes: reviewResult.notes }
  }

  const verified = await parallel(
    toVerify.map((f) => async () => {
      const votes = await parallel(
        [1, 2].map(() => () =>
          agent(
            `Independent skeptic pass on a flagged issue in ${targetPath} (First Passage repo). A prior reviewer claims:\n` +
              `Title: ${f.title}\nSeverity: ${f.severity}\nLocation: ${f.location}\nClaim: ${f.claim}\n` +
              `Cited evidence: ${f.evidence}\nWhy the reviewer says it's wrong: ${f.why_wrong}\n\n` +
              `Your job is to try to REFUTE this finding, not confirm it. Re-read ${targetPath} yourself, and re-read ` +
              `whatever the cited location/evidence points to, from the actual files -- do not trust the prior reviewer's ` +
              `paraphrase. Set refuted:true if your own independent read shows the finding is wrong, unfounded, or you ` +
              `cannot locate the cited evidence. Set refuted:false only if your own read confirms the claim and evidence ` +
              `hold up.`,
            { label: `verify:${lens.key}`, phase: 'Verify', schema: VERIFY_SCHEMA, effort: 'high' }
          )
        )
      )
      const clean = votes.filter(Boolean)
      const survivors = clean.filter((v) => !v.refuted).length
      return {
        finding: f,
        votes: clean,
        confirmed: survivors >= 1,
        unanimous: clean.length > 0 && survivors === clean.length,
      }
    })
  )

  return {
    key: lens.key,
    clean: reviewResult.clean,
    confirmed: verified.filter((v) => v.confirmed && v.unanimous),
    disputed: verified.filter((v) => v.confirmed && !v.unanimous),
    refuted: verified.filter((v) => !v.confirmed),
    nits,
    notes: reviewResult.notes,
  }
}
// ---- CRO safety-invariant hard block (design spec §6.3) --------------------
// Deterministic, not LLM-judgment-dependent -- mirrors this repo's own pattern of
// enforcing non-negotiable safety invariants in code, not in a prompt (see
// validate_c1_monitoring_acceptance.validate in ops/c1_rail/, a Python function, not an
// instruction). Runs on CRO's own structured findings, already in memory from the pipeline.
// Scope: CRO-specific, matching design spec §6.3's own framing ("a CRO dissent"). A
// STRATEGIC-tier call that omits 'cro' from args.personas gets no automated safety-invariant
// hard block -- by design, not an oversight; CRO coverage is only guaranteed on GRAND-tier
// calls per the mandatory-CRO rule above.
// Deliberately biased toward over-triggering: a false positive costs an operator one glance at
// an unnecessary hard block, a false negative lets an actual safety-invariant citation through
// undetected. A fixed-width proximity regex (an earlier version of this check) missed realistic
// multi-clause LLM prose where the two related terms are >80 chars apart -- these check for
// co-occurrence anywhere in the field instead of requiring tight adjacency.
function citesSafetyInvariant(text) {
  if (!text) return false
  if (/dry_run/i.test(text)) return true
  if (/armed_until/i.test(text)) return true
  if (/\bM1\b/i.test(text) && /\bRESOLVED\b/i.test(text)) return true
  if (/\barm(ing)?\b/i.test(text) && /\bnot\b/i.test(text) && /\bsend\b/i.test(text)) return true
  return false
}

function croHardBlockFires(lensResults, expectCro) {
  const croResult = lensResults.find((r) => r && r.key === 'cro')
  if (!expectCro) return { fires: false, citing: [], croReviewMissing: false }
  if (!croResult || croResult.notes === '(lens agent returned no result)') {
    // Fail CLOSED, not open: CRO was required (mandatory-CRO rule above) but its review never
    // completed. A deterministic safety backstop must not silently degrade to "not blocked"
    // precisely when its own input is missing -- that is the one failure mode it exists to be
    // robust against.
    return { fires: true, citing: [], croReviewMissing: true }
  }
  const candidates = [...croResult.confirmed, ...croResult.disputed]
  const citing = candidates.filter(
    (v) => citesSafetyInvariant(v.finding.claim) || citesSafetyInvariant(v.finding.evidence)
  )
  return { fires: citing.length > 0, citing, croReviewMissing: false }
}

// ---- run ----------------------------------------------------------------

phase('Form Check')
log(`Pre-ratification adversarial panel starting on ${targetPath}`)

const formCheckPromise = agent(
  `Run the mechanical brief checker against ${targetPath} in the First Passage repo (a futures prop-trading ` +
    `research/ops monorepo) and report its raw output verbatim, prefixed by the exact command you ran. Try: ` +
    `\`python scripts/check_brief.py ${targetPath}\`. If that errors because the file isn't a checkable brief type, ` +
    `run \`python scripts/check_brief.py --help\` to see if a --type flag applies, and if none does, say so plainly. ` +
    `This is a FORM-only mechanical pass -- do not editorialize or add adversarial commentary, just run it and report ` +
    `the output.`,
  { label: 'form-check', phase: 'Form Check', effort: 'low' }
)

// Note (known, accepted limitation): this check confirms the artifact is frozen/committed at
// this instant, but each persona later does its own live read of targetPath (see PERSONAS
// above) rather than pinning to the commit sha validated here -- a TOCTOU gap if the file is
// modified mid-run. Accepted for now given a review's short wall-clock and low collision odds;
// revisit (e.g. read via `git show <sha>:targetPath`) if this ever proves load-bearing.
if (personaMode) {
  const precondition = await agent(
    `Run exactly these two commands against the First Passage repo and report the results, nothing else: ` +
      `(1) \`git status --porcelain -- ${targetPath}\` (2) \`git log -1 --oneline -- ${targetPath}\`. ` +
      `Report whether command (1) produced any output (uncommittedChanges) and whether command (2) produced ` +
      `at least one line (hasCommitHistory), plus the verbatim combined output.`,
    { label: 'precondition-check', phase: 'Form Check', effort: 'low', schema: PRECONDITION_SCHEMA }
  )
  if (!precondition) {
    throw new Error(
      `pre-ratification-adversarial-panel persona mode: the precondition-check agent for ${targetPath} returned ` +
        `no result -- cannot verify the artifact is frozen/committed (design spec §6.1). Re-run.`
    )
  }
  if (precondition.uncommittedChanges || !precondition.hasCommitHistory) {
    throw new Error(
      `pre-ratification-adversarial-panel persona mode requires ${targetPath} to be a frozen, committed ` +
        `artifact (design spec §6.1) -- ${precondition.uncommittedChanges ? 'it has uncommitted changes' : 'it has no commit history'}. ` +
        `Raw check output: ${precondition.rawOutput}. Commit the artifact first, then re-run.`
    )
  }
}

phase('Review')
const activeLenses = personaMode ? PERSONAS : LENSES
const lensResults = await pipeline(
  activeLenses,
  (lens) => agent(lens.build(), { label: `review:${lens.key}`, phase: 'Review', schema: LENS_FINDINGS_SCHEMA }),
  (reviewResult, lens) => verifyLensFindings(reviewResult, lens)
)

const formCheckResult = await formCheckPromise

const confirmedCount = lensResults.reduce((n, r) => n + (r ? r.confirmed.length : 0), 0)
const disputedCount = lensResults.reduce((n, r) => n + (r ? r.disputed.length : 0), 0)
log(`Review+verify done: ${confirmedCount} confirmed, ${disputedCount} disputed findings across ${activeLenses.length} lenses`)


const expectCro = personaMode && personaSlugs.includes('cro')
const hardBlock = personaMode ? croHardBlockFires(lensResults, expectCro) : { fires: false, citing: [], croReviewMissing: false }
const hardBlockLine = hardBlock.croReviewMissing
  ? `\n\nCRO SAFETY-INVARIANT HARD BLOCK (FAIL-CLOSED): CRO was required for this GRAND-tier review but its ` +
    `review did not complete (agent failure or no result). Per design spec §6.3, a deterministic safety backstop ` +
    `must fail closed, not open, when its own input is missing -- state "Overall disposition: BLOCKED" at the ` +
    `top of your memo and note that this is a coverage failure requiring a re-run, not a substantive finding.`
  : hardBlock.fires
    ? `\n\nCRO SAFETY-INVARIANT HARD BLOCK: CRO's review confirmed or disputed a finding citing a CLAUDE.md ` +
      `non-negotiable safety invariant (dry_run/armed_until/M1-RESOLVED/arm-not-send). Per design spec §6.3, this ` +
      `is a HARD BLOCK on synthesis -- state "Overall disposition: BLOCKED" at the top of your memo regardless of ` +
      `what any other persona found, and do not let any other finding soften this. Citing finding(s): ` +
      `${JSON.stringify(hardBlock.citing.map((c) => c.finding))}`
    : ''

phase('Synthesize')
const synthesis = await agent(
  `You are the final adjudicator for a pre-ratification adversarial review of ${targetPath} in the First Passage repo ` +
    `(a futures prop-trading research/ops monorepo). This mirrors a review pattern documented in this repo's own ` +
    `memory: a careful Rule-0-compliant brief with a green mechanical checker (check_brief.py) can still carry real ` +
    `BLOCKERs invisible to that checker -- a past 14-agent adversarial pass caught 6 (doubled multiplier, unread ADR ` +
    `clause, claimed-but-unscored screen, N-basis mismatch, missing attestation, false bounding claim). Treat the ` +
    `mechanical FORM check result below as FORM-only -- it is NOT a substitute for the findings below.\n\n` +
    `FORM CHECK (check_brief.py) result:\n${formCheckResult}\n\n` +
    `Six independent adversarial lenses each reviewed ${targetPath} and had their non-NIT findings independently ` +
    `skeptic-verified (2 refuters per finding; CONFIRMED means both skeptics agree the finding survives, DISPUTED means ` +
    `the two skeptics split, REFUTED means both skeptics could not confirm it). Raw lens+verify output:\n\n` +
    `${JSON.stringify(lensResults, null, 2)}\n\n` +
    `Before finalizing, READ ${targetPath} YOURSELF (and any file/location a CONFIRMED or DISPUTED finding cites) -- do ` +
    `not trust the lens agents' paraphrases at face value. Discard any finding your own read shows to be unfounded, and ` +
    `say so explicitly under a "Findings discarded on independent re-read" section (don't silently drop).\n\n` +
    `Produce a final ratification verdict, plain text, to be read directly by the operator deciding whether to ratify:\n` +
    `- Overall disposition: BLOCKED (>=1 confirmed BLOCKER survives your own re-read) / CLEAR-WITH-CONCERNS (only ` +
    `CONCERN/NIT-level findings survive) / CLEAR (nothing survives).\n` +
    `- Confirmed findings, ranked by severity, each with: file:line, the claim, why it's wrong, and the specific fix ` +
    `needed before ratification.\n` +
    `- Disputed findings passed through for an operator judgment call, with both skeptics' rationale summarized.\n` +
    `- Findings discarded on independent re-read, with why.\n` +
    `- Any NITs, listed briefly without much discussion.\n` +
    `- One closing line noting what the mechanical check_brief.py pass covers (FORM only) vs what this panel ` +
    `additionally covers.${hardBlockLine}`,
  { label: 'synthesis', phase: 'Synthesize', effort: 'high' }
)

log(`Pre-ratification adversarial panel complete for ${targetPath}`)

return {
  targetPath,
  formCheckResult,
  lensResults,
  synthesis,
  personaMode,
  personaSlugs: personaMode ? personaSlugs : undefined,
  croHardBlock: personaMode ? hardBlock.fires : undefined,
  croReviewMissing: personaMode ? hardBlock.croReviewMissing : undefined,
}
