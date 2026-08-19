# Panel Mechanics Implementation Plan (Phase 2 of 3)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `.claude/workflows/pre-ratification-adversarial-panel.js` to support a persona-driven
review mode (design spec §6) as an **opt-in addition** to its existing generic 6-lens mode — every
current caller of this workflow keeps working unmodified.

**Architecture:** The script branches on whether `args.tier`/`args.personas` are supplied. Absent:
unchanged existing behavior (6 hardcoded lenses). Present: builds a persona-driven lens list from the
Phase-1 roster, auto-adds `cro` on every `tier:'GRAND'` call (design spec §4's mandatory-CRO rule),
and adds a deterministic (non-LLM) hard-block check on CRO findings that cite a CLAUDE.md safety
invariant. Independence (design spec §6.2) is already structurally satisfied by the existing
`pipeline()` call — each lens/persona is already spawned as an isolated `agent()` with no shared
context — this plan does not need to build that property, only point new prompts at it.

**Tech Stack:** Workflow-tool JavaScript (plain JS, no filesystem/Node APIs, no `Date`/`Math.random`
inside the script — see Global Constraints).

## Global Constraints

- **Depends on Phase 1** (`docs/superpowers/plans/2026-08-18-persona-roster.md`) being merged first —
  every persona slug referenced here must resolve to a real file under `docs/personas/`.
- Workflow scripts have **no filesystem access** — a persona's definition/log is read by the spawned
  `agent()` itself (via its own Read tool), never by the orchestrating script. The script only builds
  prompt strings and a small structural registry (slug → role/tier/office), not the full persona
  mandate text — that stays canonical in `docs/personas/*.md`, never duplicated into the script.
- Workflow scripts **cannot call `Date.now()`/`new Date()`/`Math.random()`** — they throw. Log-entry
  timestamps are stamped by the *calling* session after the workflow returns, not inside the script.
- **Zero behavior change for existing (non-persona-mode) callers** — every existing invocation of this
  workflow with just `{targetPath, extraContext}` must produce byte-identical behavior to today.
- The CRO safety-invariant hard block is implemented as **deterministic JS logic on structured
  findings data**, not as an instruction the synthesis LLM is trusted to follow correctly — matching
  this repo's own safety-invariant enforcement pattern (`validate_c1_monitoring_acceptance.validate`
  is a Python function, not a prompt).

## File Structure

Single file, modified in place:
```
.claude/workflows/pre-ratification-adversarial-panel.js   <- modify (all 3 tasks)
```

---

### Task 1: Persona registry + input validation (persona-mode branch)

**Files:**
- Modify: `.claude/workflows/pre-ratification-adversarial-panel.js:14-28` (input handling)

**Interfaces:**
- Consumes: persona slugs from Phase 1's `docs/personas/INDEX.md` (`cro`, `cio`, `coo`, `cfo`,
  `head-of-research`, `head-of-execution`, `head-of-risk-sizing`, `head-of-validation`,
  `head-of-engineering`, `head-of-governance`).
- Produces: `personaMode` (boolean), `personaSlugs` (array, persona-mode only) — consumed by Task 2.

- [ ] **Step 1: Replace the input-handling block (lines 14-28) with the branching version**

Current (lines 14-28):
```js
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
```

Replace with:
```js
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
```

- [ ] **Step 2: Verify existing (non-persona-mode) behavior is unchanged**

Call the Workflow tool with the exact args shape any existing caller already uses:
`Workflow({ scriptPath: '.claude/workflows/pre-ratification-adversarial-panel.js', args: { targetPath: 'docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md' } })`
Expected: `personaMode` evaluates `false` (no `tier`/`personas` in args), execution falls through to
the unmodified generic-lens code below — no new errors, no new required args. This is a real,
non-trivial-cost run (spends real lens/verify/synthesis agent calls) since it exercises the full
existing pipeline — acceptable one-time cost to prove no regression.

- [ ] **Step 3: Verify persona-mode validation fires correctly, at zero agent spend**

Call the Workflow tool three times with deliberately bad args — each should throw before any
`agent()` call is reached, so these cost nothing:
1. `args: { targetPath: 'docs/pursuits/a3-mnq-discovery-pipeline.md', tier: 'GRAND' }` (personas
   omitted) — expect the "requires args.personas" error.
2. `args: { targetPath: 'docs/pursuits/a3-mnq-discovery-pipeline.md', personas: ['cio'] }` (tier
   omitted, but personas present so personaMode=true) — expect the "requires args.tier" error.
3. `args: { targetPath: 'docs/pursuits/a3-mnq-discovery-pipeline.md', tier: 'GRAND', personas: ['ceo'] }`
   (`ceo` is a real Phase-1 file but not a spawnable persona — not in `PERSONA_REGISTRY`) — expect
   the "Unknown persona slug 'ceo'" error.

- [ ] **Step 4: Commit**

```bash
git add .claude/workflows/pre-ratification-adversarial-panel.js
git commit -m "feat(panel): add persona-mode input branch + registry (no lens changes yet)"
```

---

### Task 2: Persona-driven lens list + deterministic CRO hard-block

**Files:**
- Modify: `.claude/workflows/pre-ratification-adversarial-panel.js:65-148` (LENSES array — leave
  untouched, add alongside) and `:150-200` (add `croHardBlockFires` near `verifyLensFindings`)

**Interfaces:**
- Consumes: `personaMode`, `personaSlugs`, `PERSONA_REGISTRY` from Task 1.
- Produces: `PERSONAS` (array, persona-mode only, same shape as `LENSES` so it can be passed to the
  same `pipeline()` call unchanged in Task 3) and `croHardBlockFires(lensResults)` — consumed by Task 3.

- [ ] **Step 1: Add the persona-driven lens builder immediately after the existing `LENSES` array (after line 148)**

```js
// ---- persona-mode lenses (design spec §6.2) --------------------------------
// Each persona is spawned exactly like a LENSES entry -- independent agent() call via
// pipeline(), no shared context with any other persona. This is what makes the SR-11-7 /
// 18f-4 independence property (reviewer never sees the proposer's live reasoning, or any
// other reviewer's draft opinion) already true here, not something new to build.
const PERSONAS = personaMode
  ? personaSlugs.map((slug) => ({
      key: slug,
      build: () =>
        `You are the ${PERSONA_REGISTRY[slug].role} persona reviewing ${targetPath} in the First Passage repo ` +
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
```

- [ ] **Step 2: Add the deterministic CRO hard-block function immediately after `verifyLensFindings` (after line 200)**

```js
// ---- CRO safety-invariant hard block (design spec §6.3) --------------------
// Deterministic, not LLM-judgment-dependent -- mirrors this repo's own pattern of
// enforcing non-negotiable safety invariants in code, not in a prompt (see
// validate_c1_monitoring_acceptance.validate in ops/c1_rail/, a Python function, not an
// instruction). Runs on CRO's own structured findings, already in memory from the pipeline.
const SAFETY_INVARIANT_KEYWORDS = /dry_run|armed_until|M1[^.]{0,15}RESOLVED|\barm(ing)?\b[^.]{0,25}\bnot\b[^.]{0,25}\bsend\b/i

function croHardBlockFires(lensResults) {
  const croResult = lensResults.find((r) => r && r.key === 'cro')
  if (!croResult) return { fires: false, citing: [] }
  const candidates = [...croResult.confirmed, ...croResult.disputed]
  const citing = candidates.filter(
    (v) => SAFETY_INVARIANT_KEYWORDS.test(v.finding.claim) || SAFETY_INVARIANT_KEYWORDS.test(v.finding.evidence)
  )
  return { fires: citing.length > 0, citing }
}
```

- [ ] **Step 2b: Sanity-check the regex against synthetic data, outside the Workflow tool (cheap, deterministic, zero agent spend)**

Run via Bash:
```bash
node -e "
const SAFETY_INVARIANT_KEYWORDS = /dry_run|armed_until|M1[^.]{0,15}RESOLVED|\barm(ing)?\b[^.]{0,25}\bnot\b[^.]{0,25}\bsend\b/i;
const cases = [
  ['dry_run may not be set while M1 is not RESOLVED', true],
  ['Gate trigger is arm, not send', true],
  ['M1 is RESOLVED per the acceptance artifact', true],
  ['the DD tier trigger fires at -1.5% drawdown', false],
  ['subscription spend exceeds the ceiling', false],
];
let fail = 0;
for (const [text, expected] of cases) {
  const got = SAFETY_INVARIANT_KEYWORDS.test(text);
  if (got !== expected) { console.log('FAIL:', JSON.stringify(text), 'expected', expected, 'got', got); fail++; }
}
console.log(fail === 0 ? 'PASS: all 5 cases' : \`FAIL: \${fail}/5 cases\`);
"
```
Expected: `PASS: all 5 cases`

- [ ] **Step 3: Commit**

```bash
git add .claude/workflows/pre-ratification-adversarial-panel.js
git commit -m "feat(panel): persona-driven lens list + deterministic CRO hard-block check"
```

---

### Task 3: Wire persona mode into the run section + synthesis + return value

**Files:**
- Modify: `.claude/workflows/pre-ratification-adversarial-panel.js:202-261` (run section)

**Interfaces:**
- Consumes: `personaMode`, `PERSONAS`, `croHardBlockFires` from Tasks 1-2.
- Produces: extended return value (`personaSlugs`, `croHardBlock`) that Phase 3's dry run and the
  post-workflow log-append procedure below both consume. Also produces the frozen-artifact
  precondition gate (design spec §6.1/§7) — a real requirement missed in the first draft of this
  plan and added here on self-review.

- [ ] **Step 0: Add the frozen-artifact precondition check (design spec §6.1 — "panel does not run
  without a committed artifact"; §7 row 1)**

This must run *after* `phase('Form Check')` starts (it needs one `agent()` call, so it can't live in
Task 1's synchronous input-validation block) but *before* `phase('Review')`'s expensive pipeline, so a
failed precondition costs one cheap check, not a full 4-persona review.

Add this schema near the existing `VERIFY_SCHEMA` definition:
```js
const PRECONDITION_SCHEMA = {
  type: 'object',
  properties: {
    uncommittedChanges: { type: 'boolean', description: 'true if `git status --porcelain` shows any output for this path' },
    hasCommitHistory: { type: 'boolean', description: 'true if `git log -1` for this path returns at least one commit' },
    rawOutput: { type: 'string', description: 'the verbatim output of both commands' },
  },
  required: ['uncommittedChanges', 'hasCommitHistory', 'rawOutput'],
}
```

Insert this immediately after the existing `phase('Form Check')` / `formCheckPromise` lines (after
line 215 in the original file) and before `phase('Review')`:
```js
if (personaMode) {
  const precondition = await agent(
    `Run exactly these two commands against the First Passage repo and report the results, nothing else: ` +
      `(1) \`git status --porcelain -- ${targetPath}\` (2) \`git log -1 --oneline -- ${targetPath}\`. ` +
      `Report whether command (1) produced any output (uncommittedChanges) and whether command (2) produced ` +
      `at least one line (hasCommitHistory), plus the verbatim combined output.`,
    { label: 'precondition-check', phase: 'Form Check', effort: 'low', schema: PRECONDITION_SCHEMA }
  )
  if (precondition.uncommittedChanges || !precondition.hasCommitHistory) {
    throw new Error(
      `pre-ratification-adversarial-panel persona mode requires ${targetPath} to be a frozen, committed ` +
        `artifact (design spec §6.1) -- ${precondition.uncommittedChanges ? 'it has uncommitted changes' : 'it has no commit history'}. ` +
        `Raw check output: ${precondition.rawOutput}. Commit the artifact first, then re-run.`
    )
  }
}
```

- [ ] **Step 0b: Verify the precondition gate fires correctly**

Two real (cheap — one agent call each, no Review/Verify/Synthesis spend since it throws before
reaching them) test invocations:
1. Against an uncommitted scratch file (`echo "test" > docs/personas/_scratch.md`, do not `git add`
   it) with `tier: 'GRAND', personas: ['coo']` — expect the "has uncommitted changes" error. Clean up
   with `rm docs/personas/_scratch.md` afterward.
2. Against a real committed file, e.g. `docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md`
   — expect the precondition check to pass and execution to proceed into `phase('Review')` (which will
   then spend real tokens on the 4-persona-equivalent review — acceptable here since it also validates
   Steps 1-3 below in the same call).

- [ ] **Step 1: Replace the lens-selection line in the Review phase (originally line 218-222) to branch on `personaMode`**

Current (lines 217-222):
```js
phase('Review')
const lensResults = await pipeline(
  LENSES,
  (lens) => agent(lens.build(), { label: `review:${lens.key}`, phase: 'Review', schema: LENS_FINDINGS_SCHEMA }),
  (reviewResult, lens) => verifyLensFindings(reviewResult, lens)
)
```

Replace with:
```js
phase('Review')
const activeLenses = personaMode ? PERSONAS : LENSES
const lensResults = await pipeline(
  activeLenses,
  (lens) => agent(lens.build(), { label: `review:${lens.key}`, phase: 'Review', schema: LENS_FINDINGS_SCHEMA }),
  (reviewResult, lens) => verifyLensFindings(reviewResult, lens)
)
```

- [ ] **Step 2: Compute the hard-block result and fold it into the synthesis prompt (originally lines 230-257)**

Insert immediately before the existing `phase('Synthesize')` block:
```js
const hardBlock = personaMode ? croHardBlockFires(lensResults) : { fires: false, citing: [] }
const hardBlockLine = hardBlock.fires
  ? `\n\nCRO SAFETY-INVARIANT HARD BLOCK: CRO's review confirmed or disputed a finding citing a CLAUDE.md ` +
    `non-negotiable safety invariant (dry_run/armed_until/M1-RESOLVED/arm-not-send). Per design spec §6.3, this ` +
    `is a HARD BLOCK on synthesis -- state "Overall disposition: BLOCKED" at the top of your memo regardless of ` +
    `what any other persona found, and do not let any other finding soften this. Citing finding(s): ` +
    `${JSON.stringify(hardBlock.citing.map((c) => c.finding))}`
  : ''
```

Then modify the synthesis `agent()` call's prompt (append `hardBlockLine` to the existing prompt
string, right before the final backtick):
```js
phase('Synthesize')
const synthesis = await agent(
  `You are the final adjudicator for a pre-ratification adversarial review of ${targetPath} in the First Passage repo ` +
    // ... (all existing prompt text, unchanged) ...
    `- One closing line noting what the mechanical check_brief.py pass covers (FORM only) vs what this panel ` +
    `additionally covers.${hardBlockLine}`,
  { label: 'synthesis', phase: 'Synthesize', effort: 'high' }
)
```

- [ ] **Step 3: Extend the final return statement (originally line 261)**

Current:
```js
return { targetPath, formCheckResult, lensResults, synthesis }
```

Replace with:
```js
return {
  targetPath,
  formCheckResult,
  lensResults,
  synthesis,
  personaMode,
  personaSlugs: personaMode ? personaSlugs : undefined,
  croHardBlock: personaMode ? hardBlock.fires : undefined,
}
```

- [ ] **Step 4: Document the post-workflow log-append procedure**

This runs in the *calling* session after `Workflow(...)` returns — never inside the script itself,
since `Date` is unavailable there. Add this as a new section in
`docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md` under a new `## 12. Post-workflow
log-append procedure` heading (append to the spec file, do not edit its existing sections):

```markdown
## 12. Post-workflow log-append procedure (added during Phase 2 implementation)

After a persona-mode `Workflow` call returns, for each slug in `result.personaSlugs`:

1. Read `docs/personas/<slug>-log.md` if it exists; treat as empty (first entry) if not.
2. Extract that persona's verdict from `result.synthesis` (the synthesis memo names each
   persona's confirmed/disputed findings by lens key).
3. Append (never edit prior entries) a new entry using this exact template, with today's date filled
   in by the calling session (never computed inside the Workflow script):

\`\`\`markdown
## <YYYY-MM-DD> — <result.targetPath>

**Verdict:** <BLOCKED | CLEAR-WITH-CONCERNS | CLEAR, from result.synthesis for this persona>
**Confirmed findings:** <count, or "none">
**Ratified as recommended:** <Yes | No | Pending -- operator has not yet ratified>
\`\`\`

4. If `result.croHardBlock` is true, every persona's log entry for this review additionally carries
   a line: `**CRO hard block fired:** yes -- disposition is BLOCKED regardless of this persona's own verdict.`
```

- [ ] **Step 5: Commit**

```bash
git add .claude/workflows/pre-ratification-adversarial-panel.js docs/superpowers/specs/2026-08-18-loop-persona-hierarchy-design.md
git commit -m "feat(panel): wire persona mode into run/synthesis/return; document log-append procedure"
```

---

## Out of scope for this plan (Phase 3)

- Actually running the persona-mode workflow against a real decision artifact end-to-end and judging
  whether the output is *good* (not just structurally correct) — that requires real agent spend and
  is Phase 3's job.
- Creating any real `docs/personas/<slug>-log.md` file — none exist until Phase 3's dry run creates
  the first ones by following the Step 4 procedure above.
- Extending `scripts/check_personas.py` (or a sibling) to validate log-file structure — Phase 3.
