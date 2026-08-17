export const meta = {
  name: 'gate-reachability-audit',
  description: 'Audit every gate in a prereg/G0/lane-spec for reachability AND bindingness before freeze',
  whenToUse:
    'At every G0/pre-registration freeze (before operator GO), when repairing a lane door-check, or after a domain bar changes under a running campaign. A frozen gate fails two independent ways (lesson_gate_reachability_preregistration, 5 firings as of 2026-08-10): UNREACHABLE -- cannot fire at the declared N/power/threshold (Q-HARV-0; DISC-CAMP-0 k_dsr=3177; MNQPROX-2 n_paired=15) -- or UNBINDING -- live, even machine-enforced, but the campaign choreography never consults it (dense-1m step-1 door check never reached the tier=always index-intraday domain bar; two campaigns ran unbound). Pass args.targetPath = the PREREG/G0/lane-spec/charter doc; optional args.campaignDir = the lab/ campaign directory.',
  phases: [
    { title: 'Extract', detail: 'enumerate every gate + the door-check scope' },
    { title: 'Audit', detail: 'per-gate reachability + bindingness; independent domain-bar sweep' },
    { title: 'Verify', detail: 'skeptic pass on flagged gates' },
    { title: 'Synthesize', detail: 'per-gate verdicts, repairs, freeze ruling' },
  ],
}

// ---- input handling -------------------------------------------------------

const cfg = args && typeof args === 'object' && !Array.isArray(args) ? args : { targetPath: args }
if (!cfg || !cfg.targetPath) {
  throw new Error(
    'gate-reachability-audit requires args.targetPath (or args as a bare path string) pointing to the ' +
      'PREREG/G0/lane-spec/charter doc, e.g. Workflow({ name: "gate-reachability-audit", ' +
      'args: { targetPath: "docs/briefs/pre-registration/<prereg>.md" } })'
  )
}
const targetPath = cfg.targetPath
const campaignDirLine = cfg.campaignDir
  ? `\nThe campaign working directory is ${cfg.campaignDir} -- list it and read its PREREG/STAGE/RESULTS artifacts too.`
  : ''

// ---- schemas --------------------------------------------------------------

const EXTRACT_SCHEMA = {
  type: 'object',
  properties: {
    campaign: { type: 'string', description: 'campaign id / Q-ID / lane name' },
    instruments: { type: 'array', items: { type: 'string' } },
    mechanism_family: { type: 'string' },
    door_check: {
      type: 'string',
      description: 'the door-check / step-1 prior-consult choreography near-verbatim, INCLUDING its declared scope, or NONE',
    },
    gates: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          kind: {
            type: 'string',
            description: 'falsifier-limb | stop-rule | streak-counter | dsr-floor | cost-law | placebo | n-surv | door-check | k-conjunct | regime-gate | other',
          },
          declaration: { type: 'string', description: 'the gate near-verbatim' },
          threshold: { type: 'string' },
          declared_inputs: { type: 'string', description: 'N / K / trial budget / power / window the gate is declared against' },
          executor: { type: 'string', description: 'what the doc says executes/consults this gate, or UNSTATED' },
          location: { type: 'string', description: 'section / line in the source doc' },
        },
        required: ['id', 'kind', 'declaration', 'threshold', 'declared_inputs', 'executor', 'location'],
      },
    },
  },
  required: ['campaign', 'instruments', 'mechanism_family', 'door_check', 'gates'],
}

const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    results: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          gate_id: { type: 'string' },
          reachability: { type: 'string', enum: ['REACHABLE', 'UNREACHABLE', 'UNVERIFIABLE'] },
          reachability_arithmetic: { type: 'string', description: 'the re-derivation from primitives, or what input is missing' },
          bindingness: { type: 'string', enum: ['BINDING', 'UNBINDING', 'UNVERIFIABLE'] },
          executor_evidence: {
            type: 'string',
            description: 'the mechanical consult found + pasted executed output, or the prose-only / never-reached finding',
          },
          flagged: { type: 'boolean', description: 'true unless both REACHABLE and BINDING' },
          repair: { type: 'string', description: 'for flagged gates: the specific repair; else n/a' },
        },
        required: ['gate_id', 'reachability', 'reachability_arithmetic', 'bindingness', 'executor_evidence', 'flagged', 'repair'],
      },
    },
  },
  required: ['results'],
}

const SWEEP_SCHEMA = {
  type: 'object',
  properties: {
    bars: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          bar_id: { type: 'string' },
          scope: { type: 'string', description: 'the bar\'s own scope line, quoted' },
          source: { type: 'string', description: 'file:line' },
          consult_output: { type: 'string', description: 'command + exit code + output if a mechanical consult was run, else n/a' },
          binds_campaign: { type: 'boolean' },
          reached_by_door_check: { type: 'boolean' },
        },
        required: ['bar_id', 'scope', 'source', 'consult_output', 'binds_campaign', 'reached_by_door_check'],
      },
    },
    summary: { type: 'string' },
  },
  required: ['bars', 'summary'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    refuted: { type: 'boolean' },
    rationale: { type: 'string' },
  },
  required: ['refuted', 'rationale'],
}

// ---- Extract --------------------------------------------------------------

phase('Extract')
log(`Gate-reachability audit starting on ${targetPath}`)

const manifest = await agent(
  `Read the ENTIRE campaign document at ${targetPath} in the First Passage repo (a futures prop-trading ` +
    `research/ops monorepo).${campaignDirLine}\n` +
    `Enumerate EVERY gate the campaign declares or depends on: section-4 falsifier limbs, stop-rules, ` +
    `streak/consecutive-null counters, DSR floors (with their K), cost-law / cost-geometry gates, placebo ` +
    `clauses, N-SURV / bust gates, door-checks (step-1 style prior-consult choreography), K conjuncts, regime ` +
    `gates, and any "if X then STOP/KILL/HOLD" clause. For each, record: a short id; its kind; the declaration ` +
    `near-verbatim; the numeric threshold; the declared inputs it must fire against (N, K, trial budget, power, ` +
    `sample window); WHAT THE DOC SAYS EXECUTES OR CONSULTS IT (a named script, a checklist step, a pre-commit ` +
    `gate -- or UNSTATED if the doc never says); and its location. Also record the campaign id, the instruments ` +
    `involved, the mechanism family, and the door-check choreography near-verbatim INCLUDING exactly what scope ` +
    `of prior bars/registries it consults (or NONE if there is no door-check). Do not editorialize about whether ` +
    `gates are sound -- that is a later stage. Extraction must be complete: a gate you omit is a gate the audit ` +
    `cannot check.`,
  { label: 'extract', phase: 'Extract', schema: EXTRACT_SCHEMA }
)
if (!manifest) throw new Error('gate extraction agent returned no result -- cannot audit')
log(`${manifest.gates.length} gates extracted for ${manifest.campaign}; instruments: ${manifest.instruments.join(', ') || '(none listed)'}`)

// ---- Audit ----------------------------------------------------------------

phase('Audit')

const sweepPromise = agent(
  `Independent domain-bar sweep for campaign ${manifest.campaign} (instruments: ${manifest.instruments.join(', ') || 'unstated'}; ` +
    `mechanism family: ${manifest.mechanism_family}) in the First Passage repo. IGNORE the campaign doc's own ` +
    `gate table -- your job is to enumerate the bars that SHOULD bind this campaign from the repo's own ` +
    `registries, then check whether the campaign's door-check as written reaches them. The 5th firing of ` +
    `lesson_gate_reachability_preregistration happened exactly here: a door check scoped to an instrument list ` +
    `never consulted a domain-level tier=always bar, and two campaigns ran unbound by a machine-consulted gate.\n` +
    `1. Grep docs/rejected_candidates.md for raised bars / tier=always entries whose scope covers these ` +
    `instruments, this mechanism family, or the domain (e.g. index-intraday-ohlcv bars). Quote each bar with its ` +
    `own scope line and file:line.\n` +
    `2. Read scripts/instrument_profiles.py (its argparse/usage -- do not guess the CLI) and run its cell/check ` +
    `consult for each relevant instrument-mechanism combination; paste command + exit code + output verbatim. It ` +
    `is designed to exit 1 when a prior binds.\n` +
    `3. Read the door-check choreography from ${targetPath} (recorded as: ${JSON.stringify(manifest.door_check)}) ` +
    `and mark every bar from steps 1-2 that the door check as written would NEVER consult -- those are unbinding ` +
    `candidates regardless of what the doc's own gate table says.\n` +
    `Report every bar found with its consult output and whether the door check reaches it.`,
  { label: 'domain-bar-sweep', phase: 'Audit', schema: SWEEP_SCHEMA }
)

const chunkSize = Math.max(1, Math.ceil(manifest.gates.length / 8))
const chunks = []
for (let i = 0; i < manifest.gates.length; i += chunkSize) chunks.push(manifest.gates.slice(i, i + chunkSize))
log(`auditing ${manifest.gates.length} gates in ${chunks.length} chunk(s) of up to ${chunkSize} -- no gates dropped`)

const auditPrompt = (chunk) =>
  `You are auditing gates from the campaign doc ${targetPath} (First Passage repo, a futures prop-trading ` +
  `research/ops monorepo) for the two independent defect classes in lesson_gate_reachability_preregistration ` +
  `(5 firings as of 2026-08-10):\n` +
  `1. UNREACHABLE -- the gate cannot fire at its declared threshold given the campaign's actual N / trial ` +
  `budget / power. Historical instances: Q-HARV-0; DISC-CAMP-0's k_dsr=3177 (a trial count no campaign could ` +
  `accumulate); MNQPROX-2's n_paired=15 (too few pairs for the declared test).\n` +
  `2. UNBINDING -- the gate is live, correct, possibly machine-enforced, but nothing in the campaign's own ` +
  `choreography ever consults it before scoring/freeze.\n\n` +
  `Gates to audit (JSON): ${JSON.stringify(chunk, null, 2)}\n\n` +
  `Read ${targetPath} in full first. Then for EACH gate answer both questions with evidence:\n` +
  `(a) CAN IT FIRE? Re-derive from primitives: find the campaign's actual N / trial budget / window in the doc ` +
  `(or its campaign dir), compute whether the declared threshold is attainable, and show the arithmetic. If the ` +
  `inputs needed for the derivation are stated nowhere, verdict UNVERIFIABLE and name the missing input.\n` +
  `(b) WHAT EXECUTES IT, AND WILL THAT RUN? Find the executor: if a script is named (or plausibly exists under ` +
  `scripts/ or in scripts/gates.yml), READ it, check its consult semantics (does it exit nonzero when the gate ` +
  `binds?), and if it is runnable read-only, RUN it and paste the actual output -- the lesson prefers a ` +
  `mechanical consult that exits nonzero over prose a reader is trusted to remember. Then check the ` +
  `choreography: does any step of THIS campaign's declared procedure actually reach this gate before ` +
  `scoring/freeze? An executor that exists but is never reached is UNBINDING.\n` +
  `Special check for streak/consecutive counters: verify the counting rule explicitly counts ` +
  `AMBIGUOUS-HOLD-class outcomes toward the threshold (ADR ` +
  `2026-08-16-ambiguous-hold-counts-toward-null-run-thresholds) -- an uncounted outcome class is the unbinding ` +
  `failure in counter form (the CON-2 through CON-5 sequence ran past the old counter uncounted).\n` +
  `Set flagged=true for any gate that is not both REACHABLE and BINDING. For flagged gates, state the specific ` +
  `repair: the mechanical consult to add, the threshold to recompute, or the door-check scope to widen.`

const skepticPrompt = (r) =>
  `Independent skeptic pass. A gate auditor flagged a defect in a campaign gate from ${targetPath} (First ` +
  `Passage repo):\n${JSON.stringify(r, null, 2)}\n` +
  `Try to REFUTE the flag: re-read the campaign doc and whatever executor/registry/script the finding cites, ` +
  `re-derive the arithmetic yourself from the doc's own primitives, and re-run any consult the auditor ran ` +
  `(read-only). Set refuted=true if the gate is actually fine (reachable AND binding) or the auditor's evidence ` +
  `does not hold on your own read; refuted=false only if your independent read confirms the defect.`

const audited = await pipeline(
  chunks,
  (chunk, _item, i) => agent(auditPrompt(chunk), { label: `audit:chunk-${i + 1}`, phase: 'Audit', schema: AUDIT_SCHEMA }),
  async (auditResult) => {
    if (!auditResult) return []
    return parallel(
      auditResult.results.map((r) => async () => {
        if (!r.flagged) return { ...r, skeptic: null }
        const v = await agent(skepticPrompt(r), {
          label: `skeptic:${r.gate_id}`,
          phase: 'Verify',
          schema: VERDICT_SCHEMA,
          effort: 'high',
        })
        return { ...r, skeptic: v }
      })
    )
  }
)

const sweep = await sweepPromise
const gateResults = audited.filter(Boolean).flat().filter(Boolean)
const confirmedDefects = gateResults.filter((r) => r.flagged && (!r.skeptic || !r.skeptic.refuted))
const unreachedBars = sweep ? sweep.bars.filter((b) => b.binds_campaign && !b.reached_by_door_check) : []
log(
  `audit done: ${confirmedDefects.length} confirmed gate defect(s), ` +
    `${unreachedBars.length} domain bar(s) unreached by the door check`
)

// ---- Synthesize -----------------------------------------------------------

phase('Synthesize')
const synthesis = await agent(
  `Final adjudicator for a gate-reachability/bindingness audit of ${targetPath} (First Passage repo). This ` +
    `audit exists because pre-registered gates have failed 5 documented times in two ways -- unreachable (cannot ` +
    `fire at the declared inputs) and unbinding (live but never consulted by the campaign's own choreography) -- ` +
    `and an unbinding gate reads as assurance in every artifact that cites the checklist while the predicate is ` +
    `never evaluated.\n\n` +
    `Extraction manifest:\n${JSON.stringify(manifest, null, 2)}\n\n` +
    `Per-gate audit results (skeptic-checked; a flagged finding whose skeptic.refuted=true did NOT survive):\n` +
    `${JSON.stringify(gateResults, null, 2)}\n\n` +
    `Independent domain-bar sweep:\n${JSON.stringify(sweep, null, 2)}\n\n` +
    `Before ruling, re-check every surviving flagged gate yourself -- re-read the cited doc section and re-derive ` +
    `the arithmetic or re-run the consult rather than trusting the auditor's paraphrase. Discard anything that ` +
    `does not hold on your own read and say so explicitly.\n\n` +
    `Produce a plain-text ruling for the operator:\n` +
    `- Per-gate verdict table: gate id | REACHABLE+BINDING / UNREACHABLE / UNBINDING / UNVERIFIABLE | one-line ` +
    `repair.\n` +
    `- The domain-bar sweep's unreached list, each with the widening the door check needs.\n` +
    `- Overall ruling: FREEZE-SAFE (every gate reachable+binding, no binding domain bar unreached) or ` +
    `BLOCKED-AT-FREEZE with the named unanswered BINDING BARs.\n` +
    `- Escalation note: per ADR 2026-08-10-temporal-selectivity-outside-mapped-levers section 4 T3, a lane G0 ` +
    `that freezes with an unanswered BINDING BAR escalates the door-check to a gates.yml limb -- state whether ` +
    `this audit's findings would trigger that.\n` +
    `- What was NOT verifiable and why -- no silent gaps.`,
  { label: 'synthesis', phase: 'Synthesize', effort: 'high' }
)

log(`Gate-reachability audit complete for ${targetPath}`)
return { targetPath, manifest, gateResults, sweep, synthesis }
