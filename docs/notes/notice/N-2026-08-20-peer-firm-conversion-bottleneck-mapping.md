# Notice — Numerai's orthogonalized-ensemble mechanism scored highest of 5 peer firms (5/5 structural fit) yet still 0/2 survives adversarial stress-test: the DROP streak is now 3-for-3

**Notice ID:** N-2026-08-20-peer-firm-conversion-bottleneck-mapping
**Observed:** 2026-08-20
**Author:** Joshua (commission: "find a company that best solves the same or similar bottlenecks that First Passage has, especially in terms of the dry discovery funnel" — refined via the `refine-question` skill to: which quant/systematic-finance firm has the funnel most structurally analogous to the conversion/expression-death bottleneck, extract its mechanism, map + adversarially stress-test as a follow-on to the Anthropic-principles exercise) + Claude Code
**Source:** workflow `wf_787ef978-ad8` (14 agents: 5 firm-survey research agents → 1 deep-dive → 1 mapping pass → 6 adversarial stress-test votes across 2 candidate mechanisms → 1 synthesis pass; full per-agent record in that run's `journal.jsonl`), cross-checked by the workflow's own agents against direct reads of `lab/discovery/ic_similarity.py`, `lab/research_utils/breadth.py`, `docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`, `docs/adr/2026-08-19-cme-broker-panel-admission-for-breadth-revival.md`, `docs/adr/2026-08-13-dedup-first-before-new-work.md`, `docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md`, `docs/briefs/closures/Q-COMPOSE-1-closure-falsified.md`, `docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md` (all 8 verified to exist by this session before being cited here) — plus [`N-2026-08-20-anthropic-training-principles-pipeline-mapping.md`](N-2026-08-20-anthropic-training-principles-pipeline-mapping.md) and [`N-2026-08-18-quintessentials-ml-lifecycle-mapping.md`](N-2026-08-18-quintessentials-ml-lifecycle-mapping.md), the two prior DROPs this streak extends.
**Status:** `OPEN` → routed below (primary: `DROP`; escalation recommendation, not just a flag this time)
**Addendum (2026-08-20):** the escalation was acted on same day — [`AUDIT-2026-08-20-external-mapping-move-class`](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md), verdict `DEGENERATING`. The Rule-2 STRATEGIC budget (3 constituent OUTER investigations) reads as exactly consumed by these three instances; a 4th requires fresh owner GO, not a self-granted continuation.
**Lives in:** `docs/notes/notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md`

> **⚠ Correction (2026-08-20, same session, post-close).** §2 and §3 below cite `Q-TRAINKILL-1`'s
> closure as naming "a specific, cheaper next step" — **Q-TRAINKILL-2** — that the killed
> candidates ignored, and imply it was available/unexploited. This is **factually wrong**: direct
> file-existence check (missed by this session's workflow agents, who read the TK1 closure's
> Iterate block — "successor named, Q-TRAINKILL-2 — not opened" — without checking whether it
> actually stayed unopened) shows `Q-TRAINKILL-2` and its own successor `Q-TRAINKILL-3` were
> **both already opened, executed, and closed same-day, 2026-08-18** — before this session's
> exercises ran. `TK2` closed `AMBIGUOUS-HOLD`; `TK3` closed `AMBIGUOUS-HOLD` → **`STOP`**, with a
> real re-proposal bar (a new panel + operator GO + K, or an operator election between
> `NEG-FAMILIES` / `KILLS-INFORMATIVE-DEP`). There was no cheap, available alternative sitting
> idle while these three instances ran — that specific thread was already properly closed out.
> The candidates' *other* defects (category mismatch with the power-vs-empty-families question;
> evidentiary-substitution and domain-conflation risk) are unaffected and still stand. Full
> correction and its consequences for the `DEGENERATING` verdict:
> [`AUDIT-2026-08-20-external-mapping-move-class`](../audits/programme-audit/2026-08-20-external-mapping-move-class-audit.md#correction-2026-08-20-same-session-post-close).

**D-S-A domain:** data (the surveyed-firm corpus + the pipeline's own governance corpus). This notice does not propose any meta-process/framework change — see §4.

---

## §0 — Source anchors

Sources read at production fidelity:
- **Files on disk (full, this session):** the 8 repo files listed above, verified to exist before citation.
- **Public sources (fetched live by the workflow's research agents, primary-source where possible):**
  - *Numerai (winner)* — [Staking docs](https://docs.numer.ai/numerai-tournament/staking), [MMC docs](https://docs.numer.ai/numerai-tournament/scoring/meta-model-contribution-mmc), [Feature Neutral Correlation docs](https://docs.numer.ai/numerai-tournament/scoring/feature-neutral-correlation), [Alpha/MPC blog post](https://blog.numer.ai/signals-alpha-and-mpc/), the 2017 Numeraire whitepaper (full text extracted via `pdftotext`), the "998 redundant" MMC-rationale blog post, plus independent forum analyses (burn-period inversion, True Contribution persistence, live-vs-validation gap).
  - *WorldQuant* — Kakushadze "101 Formulaic Alphas" ([arXiv:1601.00991](https://arxiv.org/abs/1601.00991)) and "Factor Models for Alpha Streams" ([arXiv:1406.3396](https://arxiv.org/abs/1406.3396)), both fetched in full text.
  - *Quantopian* — postmortem/history pieces including "A Brief History of Crowdsourced Hedge Funds" (documents the "Incentive Paradox"), an archived Quantopian forum thread, and a QuantCon slide deck on their pipeline stages.
  - *AQR, Man AHL* — public research pages (see survey table, §1).
- **User memory:** used as supplementary only (the "dry discovery channels" framing) — superseded by the sharper conversion-death framing already established in this program-week's own Notices.
- **Tools available but unused:** none — WebSearch/WebFetch, repo grep/read, and multi-agent adversarial review were all exercised; the mapping and stress-test agents additionally did their own unprompted repo research beyond what this session's context briefing supplied (see §1's existing-analog list, sourced from files this session did not pre-select).

---

## §1 — The observation: survey, winner, mechanism, mapping

### Survey — 5 firms scored on doc quality × structural fit to the conversion-death bottleneck specifically

| Firm | Score | Doc quality | Structural fit | One-line mechanism |
|---|---|---|---|---|
| **Numerai** (winner) | **4.60** | 4 | **5** | Meta Model Contribution: score a submission by the covariance of its *residual after orthogonalizing against the live stake-weighted ensemble* with the realized target — reward for adding non-redundant information, not standalone correlation. |
| WorldQuant | 4.00 | 4 | 4 | Sharpe-maximizing weighted combination ("mega-alpha") of many low-correlated alphas, `w_i ∝ Σ_j C⁻¹_ij·α_j` off a regularized covariance matrix — diversification absorbs individual decay. Calibrated for thousands of near-independent alphas; sqrt(N) benefit doesn't transfer to a handful of candidates. |
| Quantopian (defunct 2020) | 4.00 | 5 | 3 | A named "Alpha Combination" pipeline stage (rank-average → risk-constrained optimization → ML classifier) sitting between discovery and portfolio construction — but the fund still failed despite running it. |
| AQR | 3.80 | 4 | 3.67 | Cross-sectional/asset-class breadth-driven noise cancellation + "craftsmanship alpha" (combine imperfect definitions rather than pick one best) — breadth is cross-sectional, not single-instrument time-series stacking. |
| Man AHL | 3.40 | 3 | 3.67 | Breadth substitutes for per-instrument signal strength (same signal deployed unchanged across hundreds of markets) — structurally adjacent but no actual combination formula documented. |

Numerai won specifically because its public documentation is *formula-level* (not marketing prose) and its structural-fit reasoning is not "Numerai is good at quant finance" but a direct, quantified answer to this pipeline's own named second reading of the bottleneck: **every candidate here is evaluated and deployed as an individually-sufficient signal — no portfolio-combination layer exists that would let many individually-modest signals sum to something fundable even when none would clear the bar alone.**

### Deep-dive — Numerai's Meta Model Contribution (MMC)

**How it works:** thousands of independently-trained models submit predictions; only staked submissions feed a continuously-updated Stake-Weighted Meta Model. Each submission is scored not by raw correlation with the target but by MMC — rank-transform and gaussianize both the submission and the Meta Model, orthogonalize (residualize) the submission against the Meta Model, then take the covariance of that residual with the realized target. Payout converts via a **shared, capped pool** (`payout_factor = min(1, stake_threshold/total_at_risk)`) that decouples "does this model add unique value to the ensemble" (MMC) from "does this modeler get paid" (the capped pool). This was a 2019 redesign, built specifically because the original reward rule (pay raw correlation) caused convergence — per Numerai's own stated rationale, "only the first 1 or 2 of [1,000] submissions are really useful, and the other 998 might be redundant."

**Why it works:** orthogonalization changes the scoring objective from "is this good alone" to "does this reduce the ensemble's blind spots" — the mathematically correct portfolio-construction objective, which a standalone per-candidate gate structurally cannot express because it evaluates each candidate in isolation from the book it would join. The reference point (the Meta Model) is continuously updated from the live population, so the bar a new model must clear is self-adjusting, not fixed.

**Documented failure modes** (honestly reported, not softened): a mathematically-verified "burn-period originality inversion" (when the Meta Model itself is bad, orthogonalization can reward models that clone it); a theoretical pool-dilution attack vector (flagged, not shown resolved); a token-price-volatility failure of the incentive-compatibility proof (stakers correctly rewarded in NMR terms while losing money in USD terms); and — most relevant here — **the platform's own finer-grained successor metric (True Contribution) shows near-zero round-to-round persistence**, the identical "doesn't survive individually, only survives in aggregate" problem re-appearing one layer down, inside the very scoring system meant to solve it. (Contextual note: the business built on this mechanism was scaling as of the most recent sources — AUM ~$60M→$550M over three years, JPMorgan committing up to $500M capacity in 2025 — external validation of business viability, though not proof that MMC specifically, versus other factors, drives it.)

### Mapping — what already exists, what's missing

The mapping agent found real, specific existing repo machinery — some of it not pre-supplied in this session's briefing, independently located:

- **Already exists:** `lab/discovery/ic_similarity.py` (pairwise candidate-vs-candidate redundancy check, within one mining run's batch, advisory-only); `lab/research_utils/breadth.py` + the Q-NEFF-1 closure (N_eff participation-ratio decomposition — dependence and risk breadth); **Q-COMPOSE-1**, an already-*executed* test of composing a candidate into the live book, closed `FALSIFIED` 2026-07-17; and the harvest channel's "disclosed but not gating" pattern (requirement #3) as the repo's existing shape for "report a number that informs but doesn't decide."
- **Underpowered/unwired:** `breadth.py`'s risk-N_eff metric was, per Q-COMPOSE-1's own closure, "retroactively the finding" — computed but never a pre-registered ex-ante threshold; `ic_similarity.py` is explicitly scoped to one run's own batch and its docstring names building a cross-campaign historical corpus as "a separate, larger, deliberately deferred decision."
- **Genuinely absent, correctly identified:** a true MMC-shaped residual-vs-target orthogonality score (both existing tools stop one step short — one never touches the target, the other never computes a residual); a standing, continuously-updated reference "ensemble" object (today a candidate is scored against nothing, or a one-off frozen snapshot built for a single ad hoc investigation). Numerai's capped shared-payout-pool token economics has **no analog, and correctly none was proposed** — the mapping explicitly names importing it as exactly the domain-conflation Guardrail #1 exists to block.

---

## §2 — Why this stands out (baseline / delta / frequency)

**Baseline:** this exercise's own guardrail text carves out an explicit exception — a peer firm's published portfolio-construction/signal-combination technique is "closer in kind to a harvestable seed than to an abstract framework." Numerai scored the only 5/5 structural fit of any firm surveyed, on formula-level, primary-source documentation. This is the most favorable setup any external-mapping exercise this program-week has had.

**Delta:** despite that, zero mechanisms survived. Both candidates were independently **REFUTED** on feasibility (not merely flagged) — one for conflating signal-redundancy with the actually-named statistical-power bottleneck (Q-TRAINKILL-1's own closure already rejected the underpowered-DGP reading and named a specific, cheaper, already-scoped next step the candidate ignores), the other for being inert bookkeeping that explicitly refuses to re-license any real composition test. Both also failed **both** adversarial guardrails, and — new this run — one candidate was found to reproduce, one day late and unacknowledged, a design (automatic/standing capture) the repo's own 2026-08-19 spec had already considered and explicitly declined by name.

**Frequency:** this is the **third** external-framework/firm-mapping exercise this program-week to land on `DROP`, after the Quintessentials mapping (2026-08-09/19) and the Anthropic-training-principles mapping (2026-08-20, earlier this session). 3-for-3. This exercise had the most favorable setup of the three (a named guardrail carve-out, the highest structural-fit score of any candidate across both exercises) and still produced nothing — see §4 for why this changes the recommendation from "flag for a future audit" to "trigger one now."

---

## §3 — Candidate mechanisms: both adversarially stress-tested, 0 survived

| # | Mechanism | Stage | Killed by | Core defect |
|---|---|---|---|---|
| 1 | Residual-vs-target orthogonality pre-screen | generate | feasibility (REFUTED) + evidentiary + domain | Category mismatch: screens redundancy while the named bottleneck (Q-TRAINKILL-1) is a *power* question whose own closure already rejected the underpowered-DGP reading and named a cheaper, unrelated, already-specified next step. Requires a cross-campaign return-series corpus `ic_similarity.py`'s own docstring calls "deliberately deferred," misdescribed as arithmetic already running today. Functions as a budget-starvation kill before Clause K/N ever runs — structurally close to a semantic-duplicate gate already retired in this repo for false-positiving (`docs/adr/2026-08-13-dedup-first-before-new-work.md`). Three stage reach-arounds (deploy book composite, update dedup corpus, evaluate target-scoring) behind one declared "generate" label. |
| 2 | Standing per-candidate breadth diagnostic at survivor-scoring | evaluate | feasibility (REFUTED) + evidentiary + domain | Breadth/N_eff says nothing about H1/H2/H3 or the train-kill power ambiguity, and explicitly refuses to re-license any real composition test — inert bookkeeping, not an answer. Its grounding is stale: the repo's own 2026-08-19 design spec had *already considered and rejected by name*, one day earlier, the identical "automatic capture for every candidate" shape (chose pointer-based on-demand instead, citing an unbounded-unpruned-store risk). Reproduces the exact Forbidden Move the ratified Stage-8 ADR (`docs/adr/2026-07-20-stage8-variance-dominance-risk-neff-gate.md`) names, outside that ADR's own scope (compose-admission only, never standalone survivor-scoring). Requires live deploy-stage book state as input and targets update-stage re-proposal cognition as output — both undisclosed by its single "evaluate" label. |

Full per-candidate adversarial reasoning (all three lenses, verbatim, including the specific file citations each verdict is grounded in) is in the workflow's `journal.jsonl`, cited in §0.

---

## §4 — Routing decision

**Primary: `DROP`.** Both candidate mechanisms were independently REFUTED at the feasibility lens (not merely flagged) and both carried `risk=true` on evidentiary-substitution and domain-conflation. There is no cheap $0/K=0 pilot to propose — the defects are conceptual (wrong axis of the bottleneck; inputs the repo has explicitly deferred or already declined building), not scoping issues a tweak would fix.

**Sharpened, durable output kept despite the DROP** — this run refined both standing guardrails from the prior Notice, not just re-confirmed them:

1. **Evidentiary-substitution, sharpened.** Both killed mechanisms here were pure deterministic arithmetic (no LLM judgment in the computation) yet both still tripped `risk=true` — confirming the guardrail's real test isn't "was an LLM the generator" but "can a number, once surfaced into a decision-adjacent artifact, get read by a future human or agent as licensed evidence rather than a report." **New this run:** a "disclosed but not gating" posture neutralizes the letter of the guardrail but not the spirit if the disclosed number is the sole input a *fixed, non-extendable* investigative budget (Rule 2's 8 iterations/investigation, 3/programme) gets reallocated on — **budget-starvation is a kill by another name.**
2. **Domain-conflation, sharpened.** Both mechanisms cleared the *literal* test (one named stage, no imported cross-cutting vocabulary, reuses existing tooling) yet both still failed on a subtler mode this run surfaces as new: **altitude/stage-reach conflation** — a mechanism's INPUT dependencies (a cross-stage reference composite; live deploy-stage book state) or OUTPUT destination (a registry write meant to inform a *different* stage's decision) can reach into stages its declared label doesn't disclose, even with zero external vocabulary imported. Procedural guardrail-cleanliness is necessary but not sufficient — trace actual data dependencies and downstream reading, and **re-check current repo state, not just the exercise's own framing, for near-in-time precedent** (one killed mechanism here reproduced a design the repo had rejected by name the day before, unacknowledged).

**Escalation, not just a flag this time:** the prior Notice recommended flagging the SNAG pattern "for a future programme-audit" after 2 DROPs. This is now **3 DROPs in one program-week**, the third under the most favorable conditions of any of the three (an explicit guardrail carve-out, the single highest structural-fit score measured). Per this repo's own programme-audit trigger ("SNAG pattern — multiple null/ambiguous loops same domain"), the recommendation changes from *defer to a future audit* to **run a programme-audit pass on the "external-mechanism-mapping" move-class now**, before a fourth instance is attempted on any pretext (a different company, a different framework, a different bottleneck reading). That audit's job is not to re-litigate any of the three DROPs, but to answer the question this Notice cannot answer from inside one more instance of the same move: is this move-class itself Degenerating (per the programme-audit skill's five-way disposition), and if so, what changes before a fourth attempt — a different search altitude entirely (e.g., stop looking for an *external mechanism* and instead run the *already-scoped, already-cheaper* Q-TRAINKILL-2 CI-recovery task both this run and the prior one kept surfacing as the actual next step)?

**What this Notice does not claim:** it does not claim peer-firm research is worthless — Numerai's honestly-reported failure modes (True Contribution's near-zero persistence, in particular) are a real, useful negative data point: even the best-documented, highest-scoring "combine many weak signals" architecture found has its own version of "doesn't survive individually, only in aggregate," one layer down. What it found is that translating that architecture into a concrete, single-stage, guardrail-clean mechanism for *this* pipeline, grounded against the *actual* named bottleneck, did not succeed on this attempt.

---

## §10 — Audit hooks

```bash
# This is the third DROP in the external-mapping move-class this program-week
grep -rl "DROP" docs/notes/notice/N-2026-08-18-quintessentials-ml-lifecycle-mapping.md docs/notes/notice/N-2026-08-20-anthropic-training-principles-pipeline-mapping.md docs/notes/notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md
# Expected: all three

# Escalation recommendation is visible for a programme-audit pass
grep -n "programme-audit pass on the" docs/notes/notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md

# The already-scoped cheaper alternative both this run and the prior work surfaced
grep -rn "Q-TRAINKILL-2" docs/briefs/closures/Q-TRAINKILL-1-closure-ambiguous-hold.md
# Expected: named as the successor's scope (CI-recovery on named BOUNDED rows)

# Near-in-time precedent this run caught (verify it still holds)
grep -n "Approach B" docs/superpowers/specs/2026-08-19-cme-breadth-revival-candidate-index-design.md
# Expected: rejected by name, in favor of pointer-based/on-demand (Approach C)
```

---

## Verification

```bash
$ python C:/Users/joshu/.claude/skills/brief-authoring/scripts/check_brief.py docs/notes/notice/N-2026-08-20-peer-firm-conversion-bottleneck-mapping.md --type notice
# Expected: §0 source / §1 observation / §2 baseline+delta / routing decision all present
```
