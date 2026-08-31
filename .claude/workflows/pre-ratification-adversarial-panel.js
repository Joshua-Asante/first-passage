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

// ---- run ----------------------------------------------------------------

phase('Form Check')
log(`Pre-ratification adversarial panel starting on ${targetPath}`)

const formCheckResult = await agent(
  `Run the mechanical brief checker against ${targetPath} in the First Passage repo (a futures prop-trading ` +
    `research/ops monorepo) and report its raw output verbatim, prefixed by the exact command you ran. Try: ` +
    `\`python scripts/check_brief.py ${targetPath}\`. If that errors because the file isn't a checkable brief type, ` +
    `run \`python scripts/check_brief.py --help\` to see if a --type flag applies, and if none does, say so plainly. ` +
    `This is a FORM-only mechanical pass -- do not editorialize or add adversarial commentary, just run it and report ` +
    `the output.`,
  { label: 'form-check', phase: 'Form Check', effort: 'low' }
)

phase('Review')
const lensResults = await pipeline(
  LENSES,
  (lens) => agent(lens.build(), { label: `review:${lens.key}`, phase: 'Review', schema: LENS_FINDINGS_SCHEMA }),
  (reviewResult, lens) => verifyLensFindings(reviewResult, lens)
)

const confirmedCount = lensResults.reduce((n, r) => n + (r ? r.confirmed.length : 0), 0)
const disputedCount = lensResults.reduce((n, r) => n + (r ? r.disputed.length : 0), 0)
log(`Review+verify done: ${confirmedCount} confirmed, ${disputedCount} disputed findings across ${LENSES.length} lenses`)

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
    `additionally covers.`,
  { label: 'synthesis', phase: 'Synthesize', effort: 'high' }
)

log(`Pre-ratification adversarial panel complete for ${targetPath}`)

return {
  targetPath,
  formCheckResult,
  lensResults,
  synthesis,
}
