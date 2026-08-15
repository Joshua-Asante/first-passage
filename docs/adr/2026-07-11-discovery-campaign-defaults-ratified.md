# ADR 2026-07-11 — Discovery campaign defaults ratified (operator)

**Status:** Accepted (operator executive decision, recorded)
**Superseded-by:** none
**Retain-until:** none
**Superseded-in-part-by:** `2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` - Campaign-default #3 (Universe-correction row) DSR K/V inputs re-baselined; the rest of the campaign defaults stand.
**Decision date:** 2026-07-11
**Authors:** Joshua (ratification) + claude.ai (recorder) + Claude Code (§0 verification + chain landing)
**Supersedes:** none. **Ratifies** the standing "Campaign defaults" table defined in `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` §Campaign-defaults — moving those defaults from *proposed* to *operator-ratified standing policy* that discovery campaigns inherit by reference.
**Related:** `docs/adr/2026-07-10-databento-research-stack.md` (the stack these defaults govern); `docs/adr/2026-07-10-r6-nogo-futures-residual-disposition.md` (discovery-first is the sole new-leg path — these defaults are its rules of evidence); `docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md` (the admission route a survivor exits into); `docs/methodology/references/statistics-of-tradable-anomalies.md` (the field guide whose Domains 4–8 are the rationale for each default); memories `project_futures_prop_pivot`, Q-NEFF-1 / Q-DECAY-1 closures.
**Layer:** methodology (research rules of evidence only). **No** strategy/risk-control parameter, allocation, `dd_protection` constant, `portfolio_mc.py`, or Pine source is touched. Locked MC anchor 99.83/0.17/4.37 untouched.

---

## §0 — Rule 0 reads (production-source verification)

The authoring session (claude.ai advisor) could not read the repo (local
Windows-MCP unresponsive) and left these anchors `[§0-pending]`. **Claude Code
supplied the reads on 2026-07-11** in worktree `tradable-anomalies-strategy-dbf713`,
branch `claude/tradable-anomalies-strategy-dbf713`, anchor `git rev-parse --short HEAD`
= **`509f6b5`** (off current `main`; the Databento stack it extends merged at
`1316290` / PR #308, feat commit `7814ec6`).

- `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` §Campaign-defaults — **authored this session** (the advisor referenced it as existing; it did not — repo-wide grep for `Campaign-defaults` / `discovery-campaign-template` returned zero hits pre-landing). It is the single source of truth for the default *values*; this ADR references, does not restate. Landed with the `RATIFIED (operator, 2026-07-11)` header (satisfies the §2 follow-up at landing, not after).
- `docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md` — **authored this session** (same missing-file finding). The first campaign that inherits these defaults; ratification unblocks its lock.
- `docs/adr/2026-07-10-databento-research-stack.md` — read. Stack scope + the cost falsifier (§4) the per-campaign cost gate mirrors; §5 "post-integration amendments go through the normal skill-authoring path with their own review" is the authority under which this ratification + the pipeline-hardening tracks land.
- `.claude/skills/strategy-validation/SKILL.md` §8 — read. SPA/StepM/MCS via `arch.bootstrap`, DSR via `scripts/deflated_sharpe.py`, PBO/CPCV via `skfolio` — the universe correction the DSR/SPA defaults invoke. The block-bootstrap `block_size`-not-`sqrt(T)` instruction is §8a verbatim.
- `.claude/skills/databento-data/reference/proxy-discipline.md` — read. Micro-era start **2019-05-06** (index micros; MGC 2010) and the 1:10 re-scale the temporal-axis default depends on; the 2019+ native-micro OOS gate is a **realism** gate, handed to `strategy-validation`.

---

## §1 — Context

The discovery-campaign template (2026-07-10) surfaced a set of open decisions the pipeline needs pinned once — the IS/OOS axis, K semantics, the numeric gate thresholds, the temporal-consistency battery shape, the decay-monitor-at-admission requirement, and the per-campaign cost gate — and carried them as a "Campaign defaults" table marked *operator-ratifiable, not silently-locked*. Leaving them unratified means each campaign re-argues them, which is precisely the re-litigation the pre-registration discipline exists to prevent. With R6 = NO-GO, discovery-first is the only path to a new leg, so these defaults are the operation's standing rules of evidence and warrant a dated ratification rather than a per-campaign re-derivation.

**Decision driver (one sentence):** the discovery pipeline's rules of evidence must be fixed before the first campaign locks, so the operator ratifies the template's Campaign defaults as standing policy that campaigns inherit by reference and override only with a stated §8 reason.

---

## §2 — Decision

**Ratified (operator, 2026-07-11):** the Campaign defaults as defined in `discovery-campaign-template.md` §Campaign-defaults. Ratification is by reference — the template remains the single source of truth for the values; this ADR is the dated decision event. The ratified set, named for legibility (values live in the template):

1. **Temporal-not-instrument OOS axis** — discovery + all tuning on **2010-01-01→2018-12-31** (parent); **2019-05-06→present** is the statistical OOS; the native-micro re-run on that era is a *realism* gate, not an independence gate. (Respects the Jaccard-0.96 same-path scar; consciously accepts the pre-2019-viability selection bias, on the record.)
2. **Two-level K** — campaign-local K feeds SPA/StepM (needs within-campaign return series); **program-cumulative K per instrument-family** feeds DSR; abandoned campaigns still count their K.
3. **Universe correction** — SPA (family gate) + StepM (superior set), block bootstrap with an explicitly-chosen `block_size` (never sqrt(T)); **DSR ≥ 0.95**; **PBO < 0.5** via CPCV where config selection occurred.
4. **Temporal-consistency battery** — sub-era sign consistency **≥ ⌈0.7·Y⌉ of Y**; drop-top-year concentration; regime-slice survival (labels as *test conditions*, never filters — Q-REGIME-COND-1 scar); CUSUM on the candidate's own edge series over the OOS era.
5. **Decay-monitor-at-admission** — a candidate is inadmissible unless it ships with a CUSUM decay-monitor spec whose null was calibrated during validation (Q-DECAY-1: live decay coverage ≈ 0 because detectors were never designed at admission).
6. **Per-campaign cost gate** — declared `--max-cost` total, checked against the summed `estimate` before any `pull`; first campaigns inside the $125 free-credit window.

**Inheritance semantics:** a campaign brief inherits these by reference ("inherits ratified Campaign defaults per ADR 2026-07-11") and does **not** re-ratify. An override of any single default is legal only when stated with its reason in that campaign's §8 pre-registration — an in-place edit of a ratified default is forbidden (§5).

**Effective:** immediately (2026-07-11). **Scope:** research rules of evidence only.

**Follow-up (documentation) — SATISFIED at landing:** the template's §Campaign-defaults header was authored directly as "RATIFIED (operator, 2026-07-11) per ADR 2026-07-11-discovery-campaign-defaults-ratified.md" (the template did not pre-exist, so there was no "operator-ratifiable" header to replace). No deferred edit remains.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Leave defaults *proposed*, decide per campaign | Re-argues the rules of evidence every campaign — the re-litigation pre-registration exists to prevent; also lets the OOS axis or DSR threshold drift toward whatever a given campaign's result wants. |
| Restate the default values inside this ADR | Two sources of truth for the same numbers = drift (the anti-pattern programme-audit warns about). Reference-only keeps the template canonical. |
| Instrument-as-OOS default (parent-IS / micro-OOS as independence) | The Jaccard-0.96 scar: same order book, same arbitraged path. Independence must be temporal; the micro re-run is a realism gate. Ratifying the wrong axis would bake a known-false hold-out into every campaign. |
| Looser DSR / no cumulative-K | K=1 understates overfitting by construction; per-run FDR is program-contaminated (tsfresh FRESH note). Cumulative-family K is nearly free (timestamped manifests) and is the honest denominator. |

---

## §4 — Falsifier (revert / re-baseline trigger)

**H:** These defaults are the correct standing rules of evidence for discovery campaigns on CME futures.

**Falsifier (a default is wrong):** a default is falsified if a closed campaign demonstrates it systematically mis-gates — e.g., the temporal split proves to have no OOS power because 2019+ is too short for an instrument-family (sub-era count Y too small for the ⌈0.7·Y⌉ rule to discriminate), or the DSR-0.95 threshold is shown mis-calibrated for the realized trial economics. On falsification, the default is changed by a **superseding ADR** that re-baselines it and states which prior campaigns' verdicts are affected — never by an in-place edit of the template or this ADR.

**Revert action:** supersede this ADR (or amend the specific default via a new ADR citing the closed-campaign evidence). Campaigns pre-registered under the old default keep their verdicts; new campaigns inherit the new default.

**Trigger check schedule:** rides the standing quarterly programme audit — next **2026-08-08**, then 2026-11-08. Check: any closed campaign whose closure record flagged a default as mis-gating.

---

## §5 — Forbidden moves (under this ADR)

- **Editing a ratified default in place** (template value or this ADR §2) to match a campaign's emerging result — methodology-layer p-hacking. Changes go through a superseding ADR + re-baseline only.
- **A campaign overriding a default without stating the reason in its §8 pre-registration** — silent override defeats the ratification; the override and its justification must be a committed, pre-result artifact.
- **Treating instrument or feed as the OOS axis** in any campaign — the ratified axis is temporal; the micro re-run is realism, not independence.
- **Admitting a survivor without its calibrated decay monitor** — the admission requirement is ratified, not aspirational.
- **Restating the default values anywhere as a second source of truth** — reference the template; do not copy the numbers.

---

## §6 — Consequences

**Positive:** the pipeline's rules of evidence are fixed and dated; campaigns inherit by reference with zero re-derivation; overrides become explicit, committed, pre-result artifacts. Unblocks DISC-CAMP-0 lock.

**Negative (real):** ratification hardens choices made largely a priori (the block-size rule, the ⌈0.7·Y⌉ consistency fraction, DSR 0.95) before any campaign has stress-tested them; §4 is the release valve, but until a campaign closes, these are reasoned defaults, not empirically-tuned ones. The temporal split's accepted selection bias (against young regime-born anomalies) is now standing.

**Risks:** the 2019+ OOS window is short for some instrument families → the sign-consistency rule may under-discriminate; mitigated by §4's per-family falsifier and the option to override with reason.

**Downstream (documentation):** the template header carries the ratification inline (§2 follow-up satisfied at landing); no `CLAUDE.md`/`STATE.md` change required (methodology layer, surfaced in `STATE.md` forward board only as the campaign chain's landing, not as a live-decision change).

---

## §7 — Implementation plan

Policy record only — no code.
- **Phase 0** — §0 content-reads done 2026-07-11 by Claude Code (the advisor's `[§0-pending]` anchors resolved; the two referenced-but-missing files, template + shakedown, authored this session to make the chain coherent).
- **Phase 1** — this ADR + the template + the shakedown brief + the DISC-CAMP-0 pre-registration + the pipeline-hardening handoff land together at `docs/`.
- **Phase 2** — no deferred template edit (header authored ratified at landing).
- **Phase 3** — verification block runs at commit; status `Accepted`.

---

## §10 — Audit hooks (runnable)

```bash
# This ADR ratifies the template's defaults by reference (not by restating values)
grep -n "Campaign-defaults\|discovery-campaign-template" docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md

# The template header reflects ratification (authored inline at landing)
grep -n "RATIFIED (operator, 2026-07-11)" docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md

# No default value is restated here (single source of truth stays the template) — spot check
grep -nE "DSR . 0\.95|2010-01-01|2019-05-06" docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md
# (values appear as named scope only; the authoritative numbers live in the template)

# This ADR changed NO locked constant (expect empty)
git diff --stat HEAD -- core/config/params.toml core/dd_protection.py core/portfolio_mc.py

# §4 trigger reminder — next programme audit: 2026-08-08
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md --type adr
# Expected: no HARD violations

# Chain coherence (all now exist on disk)
ls docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md \
   docs/ltm/briefs/rnd-pipeline/DISC-CAMP-0-shakedown.md \
   docs/ltm/briefs/pre-registration/DISC-CAMP-0-preregistration.md
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-11 | Initial authoring + acceptance (operator ratifies the Campaign defaults by reference) | Joshua + claude.ai (recorder) |
| 2026-07-11 | §0 anchors resolved + template/shakedown authored to complete the chain (advisor referenced them blind); landed with the Tranche-1 statistics adoption | Claude Code |
