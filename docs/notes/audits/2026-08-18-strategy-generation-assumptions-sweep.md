# Audit Note — Strategy-generation pipeline assumptions sweep

**Audit ID:** AUDIT-2026-08-18-assumptions-sweep
**Date:** 2026-08-18
**Triggered by:** Operator-commissioned deep investigation ("question our assumptions... in our strategy generation research") — not a failure post-mortem. Scoped via clarifying questions: hunt **unexamined** assumptions (not re-audit closed ones), **whole pipeline**, output a **formal Inquire-phase-adjacent artifact**, **inventory + risk-triage depth only** (no new K spent, no falsifiers run this session).
**Authors:** Joshua + Claude Code
**Scope:** Whole pipeline (generate → evaluate → deploy → measure → update) + governance/gate mechanics + the INQHIORI/Algorithm meta-framework itself
**Lives in:** `docs/notes/audits/2026-08-18-strategy-generation-assumptions-sweep.md`

**D-S-A domain:** data (primary — the I/N corpus is the pipeline's own stated/inherent premises) + meta-process (secondary — two survivors, §4 items 9 and 25-tier, audit the INQHIORI canon and Rule 2 themselves)

---

### Sources Read declaration block

**Past chats:** N/A — no prior-session claim relied upon; this is a fresh investigation.
**Files / artifacts on disk (this session, direct reads before/alongside the sweep):**
`docs/operational_rules.md` (full, all 16 rules), `STATE.md` (partial — decision index through 2026-08-08), `core/dd_protection.py` (full), `core/firm_rules.py` (full), `docs/methodology/inqhiori-canon.md` (full), `docs/briefs/INDEX.md` (Q-roster, partial), `docs/rejected_candidates.md` (partial, lines 1-297 of 843) — plus every file cited in the 25 findings below, each read directly by a dedicated sweep, verify, or triage agent inside the workflow (file:line citations preserved per-finding; this is the corpus's own Rule-0 discipline pushed down to agent level).
**User memory:** Used as supplementary only — the ~90-lesson MEMORY.md index was pasted into every sweep-agent's prompt as a **do-not-resurface** exclusion list, not as evidence for any claim in this document.
**Tools available but unused:** Workflow's `parallel()` barrier pattern was available but not used for the Verify/Triage stage — `pipeline()` was used instead so triage could start on each candidate as soon as its own verify completed, rather than waiting for all 30 verifies. WebFetch/WebSearch were available to sweep agents but none used them — every claim below is grounded in repo-internal source, by design (this is an internal-consistency audit, not an external-fact audit).

**Pre-Q gate:**
- **D:** 5 of 30 merged candidates were deleted from the surviving corpus as `ALREADY_COVERED` — see §3. Test applied: *"Is this duplicated by a higher-fidelity source already in the corpus?"* (permitted D-test #2, `inqhiori-canon.md` §5) — a dedicated verifier agent per candidate searched `docs/briefs/INDEX.md`, `docs/rejected_candidates.md`, `docs/adr/`, `docs/methodology/` and had to produce a specific citation, not a hunch, to delete.
- **S:** 32 raw round-1 findings (8 lenses × ~4 each) were compressed to 25 canonical entries by a dedicated merge agent (near-duplicate statements from independent lenses collapsed into one, locations/lenses unioned); a completeness-critic pass then added 14 more raw findings from 4 gap-directed follow-ups, merged again to a final 30. Compression preserved the anomaly (the specific unexamined claim + its file:line grounding), never just a byte-count reduction.
- **A:** Indexed by `pipeline_area` and by the triage's `fragility × blast_radius` product so downstream Q-formation is O(seconds) per candidate, not O(re-read-the-sweep). See §5 for a caveat on that index's reliability.

---

## §0 — Source anchors

- `docs/operational_rules.md` — read in full this session (all 16 rules + edit log through 2026-08-15)
- `STATE.md` — read through line 258 of 370 (decision index through 2026-08-08 entries) this session
- `core/dd_protection.py` — read in full this session
- `core/firm_rules.py` — read in full this session
- `docs/methodology/inqhiori-canon.md` — read in full this session
- Workflow run `wf_f6d1f8a3-330` (task id `wci8x759t`), 70 agents, 0 errors, 8,583,426 subagent tokens, 1,386 tool calls, 69.3 minutes wall-clock. Journal: `subagents/workflows/wf_f6d1f8a3-330/journal.jsonl` (per-agent full outputs, retrievable if any citation below needs re-verification against the exact agent that produced it).

---

## §1 — Trigger

Operator asked for a session "specifically targeted towards questioning our assumptions, specifically in our strategy generation research... a deep investigation into the assumptions that are stated or inherent in our research." Four clarifying questions resolved scope before any spend: **target** = hunt unexamined (not re-audit closed), **scope** = whole pipeline, **output** = formal Inquire-phase artifact, **depth** = inventory + risk-triage only, zero new K.

**Failure class:** N/A — this is not a failure audit. Closest fit in the audit-note taxonomy: "Other — commissioned methodology sweep," structurally identical in shape to the existing `docs/notes/audits/programme-audit/` inventories (e.g. GSUB-1's 37-row pursuit inventory) rather than a single-incident root-cause audit.

---

## §2 — Method

A 7-stage Workflow (`strategy-assumptions-audit`), run because ultracode was active for this session:

1. **Sweep** (8 parallel lens agents) — generate / evaluate / deploy / measure / update / data / governance / meta-framework. Each grounded via Rule 0 (must cite file:line), explicitly told the ~90 already-closed lesson topics to *not* resurface, capped at 4 candidates each.
2. **Merge** — 32 raw → 25 canonical (dedupe near-duplicates across lenses).
3. **Critic** — a completeness-critic agent read the 25-item list and named 4 concrete coverage gaps (CI/branch-protection enforcement was completely absent from round 1; `ops/sentinel` was completely absent; the public-visibility ADR's own stale Status field was never questioned; the 1R-estimation doc's orphaned per-trade-cap question was never re-raised).
4. **Sweep-2** — 4 gap-directed agents, 14 more raw findings.
5. **Merge-2** — final merge, capped at 30 canonical entries.
6. **Verify** — the D-gate: one adversarial-novelty agent per candidate, instructed to *try hard* to prove `ALREADY_COVERED` via a real citation before accepting `UNEXAMINED`. 25 survived, 5 were caught.
7. **Triage** — survivors scored fragility (1-5) × blast_radius (1-5), shaped into a one-sentence falsifiable H, and given a cheap ($0/near-zero-K) falsifier sketch. No falsifiers were executed.

---

## §3 — D-gate deletions (already covered — not novel, cited)

These 5 were surfaced by the sweep but killed at Verify with a real citation. Recorded so a future session doesn't re-surface them as new:

1. **DD-protection multiplier permanently pinned to FXIFY-C2 static-geometry constants regardless of target firm's `dd_type`.** → `docs/adr/2026-07-13-dd-protection-concept-not-constant.md` already names the Tradeify/`trailing_locking` mismatch explicitly and rules it un-derived; `POLICY_REGISTRY == {}` by design, pending the first admitted instance.
2. **`check_pine_manifest.py`'s CI invocation never calls the function containing BAD_LINE/DUPLICATE/CROSS_MANIFEST_CONFLICT detection.** → `docs/adr/2026-08-07-w5-governance-diet.md` §2 already names "deriving CI jobs from `gates.yml`" as an explicitly owed, still-open item; the workflow file's own inline comment documents the gap and its compensating control.
3. **`sessions-order`/`sessions-append-only` gates have no CI mirror; GitHub's server-side `merge=union` is structurally invisible to any local hook.** → Same W5-ADR owed item (superset), plus `scripts/githooks/post-merge`'s own header comments already document this exact risk model as a deliberate, accepted tradeoff.
4. **Sentinel Tier 2-3 (quarterly LLM probe) has never fired once, past its own first scheduled date.** → Already a named falsifiable gate ("Limb B") in `docs/briefs/2026-07-27-hermes-agent-adoption-ruling.md` §6/§7, already logged as a `MISS ⇒ H-DELTA FALSIFIED` in `docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md`. Genuine residual (not itself novel enough to re-admit): Limb B has now missed two quarterly dates (08-08, approaching 11-08) un-dispositioned — a status-update question on a tracked item, not an unexamined assumption.
5. **Harvest Requirement 5's cost-law hurdle rests on the same unmeasured `SLIPPAGE_TICKS_PER_SIDE=1.0` constant Q-COSTGEO-1/2/3 already flagged as likely-optimistic.** → All three Q-COSTGEO pre-registrations explicitly name this as forward-only and forbid retro-application to reopen D5/H-OD-1; Q-COSTGEO-3's own closure §8c already identifies Requirement 5 by name as the constant's "direct consumer."

---

## §4 — Findings: 25 verified-unexamined assumptions

Ranked by **blast radius first, then evidentiary strength** (see §5 — the raw `fragility × blast_radius` product is *not* used as the sort key because 3 items show a scoring-scale inversion). Each entry: statement (compressed from the full triage), grounding, why it matters, falsifiable H, and the cheap-falsifier hook.

### Tier A — blast radius 5, already directly evidenced during the sweep itself (near-certain, not merely hypothesized)

**A1. `main` is entirely unprotected — the master precondition under every "the gate catches X" claim in the repo.**
`gh api repos/Joshua-Asante/first-passage/branches/main/protection` → 404 unprotected; `.../rulesets` → `[]`; owner token has `push:true`. Zero required status checks, zero required review. A direct push, an admin merge with red checks, or a GitHub-web-UI merge bypasses pre-commit (opt-in per clone), CI (advisory-only), *all 18 declared gates simultaneously* — including a `dd_protection.py`/`firm_rules.py` constant edit or a LOCKED-manifest edit.
— H: re-running the same two `gh api` calls today returns the same unprotected state. — Hook: `gh api repos/Joshua-Asante/first-passage/branches/main/protection` (expect 404 to confirm still-open); `gh api repos/Joshua-Asante/first-passage/rulesets` (expect `[]`).
> ✅ **DISCHARGED 2026-08-19 — H FALSIFIED, the finding is REMEDIATED.** The hook was re-run and the `main-protection` ruleset (id `21071355`) was authored the next day: PR required (0 approvals), force-push/deletion blocked, `skills (3.12)` required, `current_user_can_bypass: never`. Re-verified live 2026-08-24 (`rulesets` → one active branch ruleset; required contexts → exactly `skills (3.12)`). The A1 paragraph above is retained unedited as the as-of-2026-08-18 record. Note the residual: only `skills (3.12)` is required — `pytest`/`build`/`manifest-check`/`validation-controls` stay advisory, so "all 18 declared gates" are *not* individually merge-blocking. See the [`Q-GATESTACK-1` closure](../../briefs/closures/Q-GATESTACK-1-closure-falsified.md) 2026-08-19 addendum row.

**A2. The M1 "confirmed-base interlock" — the mechanism built specifically to stop a rejected/partial fill from silently authorizing a pyramid add sized off *intended* not *filled* quantity — has zero production call sites.**
`ExecutionStateStore.set_confirmed_base` / `C1SizingHostReference.confirm_executed_base` are called only from `tests/ops/*`. `ops/c1_rail/c1_rail_http_server.py` only ever *reads* the store; no CLI/script/doc documents a write procedure. First live fill is also the first time anyone learns whether an attended operator can do this correctly under time pressure with zero tooling and zero rehearsal.
— H: no code path outside `tests/ops/*` ever calls either function; every "add" signal after a real fill would halt with "no tracked executed base." — Hook: `rg -n "set_confirmed_base|confirm_executed_base" --type py` (expect 0 hits outside `tests/`); check the two past dry-fire artifacts (B6 2026-07-20, SIM 2026-07-27) for a null `confirmed_base_qty` despite a logged fill.

**A3. The live c1 sizing host never composes Call-4's portfolio-wide "beta-death" multiplier — despite `lifecycle.py`'s own docstring saying "this is what the live sizing path consumes."**
`c1_sizing_host_reference.py` imports only `TIER_MULTIPLIER`, never `get_effective_multipliers`/`beta_death_assessment`; `r_eff = base_risk × dd_scale × lifecycle_m` — no beta term anywhere in the formula. The one prior read-only display surface that showed beta caution was retired 2026-07-24 with no successor. Diagnostic CLI (`dd_protection.py main()`) *does* compose beta — an asymmetry between what a human sees and what the money-spending path computes.
— H: if ≥3 of 4 legs hit WATCH tiers simultaneously, the rail continues sizing MYM/MNQ at per-leg tier only — silently doubling effective live risk relative to doctrine at exactly the moment the shared-beta defense is supposed to engage, with no operator-visible warning. — Hook: `grep -n "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops -r` (expect 0 hits); confirmed already in this sweep.

**A4. M1's only two operator-notification channels (a process log line, a JSONL file on the Fly volume) are both pull-based; no push channel exists anywhere in `ops/`.** The one drill that "proves" reachability was the operator manually firing and immediately reading the alert — it never tested whether an attended-but-not-tailing operator notices a CRITICAL condition in real time.
— H: an operator doing ordinary unrelated work will not notice a fired CRITICAL alert within ~10 minutes, because nothing interrupts their attention. — Hook: run one unannounced self-drill; time-to-notice with a stopwatch.

**A5. Rule 6's doc/code skew audit has no analogue for the c1-rail/telemetry code the M1 ADR's own frozen §10 hooks make hard-coded factual claims about** — and this has *already recurred at least twice*, caught only by manual re-hashing. The arm interlock validates schema/status only; `--check-tree-skew` is never invoked by the interlock and `scripts/gates.yml` never wires it to any cadence.
— H: fixture-hash drift between now and the next arm attempt would still pass `require_resolved=True`. — Hook: `python scripts/validate_c1_monitoring_acceptance.py --check-tree-skew` right now, free, against current `M1_MONITORING_ACCEPTANCE.json`.

**A6. No per-trade dollar-loss cap exists anywhere in the sizing/arming path — an orphaned Forward question from `1r_estimation.md`, never re-raised against the harsher (intraday-enforced) Tradeify environment.** The one historical measured instance: a single fresh-peak Striker trade consumed 71.2% of a daily DD budget in one shot, on the *more forgiving* CFD/EOD geometry. M1's own drills are all transport/reconciliation-shaped, none risk-of-ruin-shaped.
— H: no artifact (code/ADR/spec/M1 acceptance package) defines or wires a per-trade max-loss bound; a fresh-peak or pyramid-compounded single-trade outlier is catchable only after the fact. — Hook: `rg -i "(per.?trade|single.?trade|loss.?cap|max.?loss)" core/ ops/ docs/adr/ docs/spec/` (already run: 0 hits in the live path).

### Tier B — blast radius 4-5, not yet directly confirmed but well-grounded, cheap to check

**B1. The core MC engine block-bootstraps 5-business-day week blocks IID, with replacement — zero cross-week autocorrelation assumed, never empirically validated against the actual 4-strategy panel.** Every published pass/bust/p99-DD figure, every `dd_protection` lock, every allocation ADR, the live WATCH-1 0.50× sizing decision — all trace through this one resampling unit. The repo's own statistics doctrine *names* the rigorous alternative (Politis–White 2004 automatic block-length selector) next to a qualitative endorsement instead of running it.
— H: the portfolio's weekly P&L series shows significant autocorrelation at 1-4 week lags. — Hook: `~15 lines of Python`, `statsmodels.stats.diagnostic.acorr_ljungbox` on `core/mc/ingest.py::build_week_blocks(panel)` output — zero new data, zero new K.

**B2. `K_intrinsic` — a free-text operator-typed integer — is the sole remaining multiplicity brake across the whole discovery pipeline since the 2026-08-04 K-bank was demoted to disclosure-only, and nothing cross-checks it against the actual parameter grid or session history explored.** The admitting ADR names this as "the single largest exposure the amended rule creates" and stops there.
— H: cross-checking any ledgered `K_intrinsic` against its own seed-manifest's "what we tried" prose or commit history will find at least one undercounted declaration. — Hook: pure-read audit of `register_search.py`'s ledger dir against each run's own paper trail; zero K.

**B3. The S5 bounded-promotion lane's headline safety property — "capped concurrency" — is a per-packet self-declared field compared to a static ceiling, with no cross-packet counter.** `validate_promotion_packet()` / `refute_promotion_packet()` both read `concurrency_slots` out of the same packet being validated. The S4 EventLedger that would carry real cross-packet state is explicitly not wired.
— H: N≥3 synthetic packets each declaring `concurrency_slots=1` will all Pass, silently exceeding the declared cap of 2. — Hook: clone `tests/fixtures/promotion/clean_packet.json` 3× with distinct IDs, run both validators locally — no repo mutation, $0.

**B4. Bulenox and BluSky (7 of the program's 13 firm-tiers) never received the EOD-vs-intraday breach-clock check that flipped Tradeify's own bust verdict PASS→FAIL** — same engine-generic fix mechanism, never applied. Their `dd_type="trailing"` never-locks classification also rests on absence-of-citation, not a primary-sourced denial, unlike Tradeify/MFFU's explicit found-wrong-and-corrected history.
— H: re-checking primary sources + re-running the already-built intraday-honest fix on one Bulenox tier will change either a bust verdict or the branch selection itself. — Hook: re-read the already-cited Bulenox/BluSky primary pages for lock-adjacent language; diff `bust_trailing` count with `intraday_low` populated vs `None` on one existing seed/path array.

**B5. The `2026-08-14` repo-public-visibility ADR's Status field still reads `Proposed`** (identically mirrored in `docs/adr/INDEX.md`) though the repo has been observably public with green CI for 4+ days — and the ADR's own §10 audit-hook grep commands are unsatisfiable by design (they check for headers being *gone*; the actual redaction left headers in place and replaced only body text). Nobody has confirmed the safety-relevant account-ID/dollar-figure sweep was ever re-run against the live public tree, and STATE.md's own OPERATOR QUEUE — the designated home for exactly this kind of open obligation — has zero row for it.
— H: the public repo's full working tree + git history contain zero occurrences of the real account ID / dollar figures the operator holds. — Hook: **operator-only** — paste the withheld literal values into the ADR's own §10 commands, run against `git log --all`, flip Status accordingly.

### Tier C — blast radius 4, cross-cutting or upstream-of-later-consequence

**C1. `dd_protection`'s trigger/scale constants and the allocation weights were both selected via small (5-8 config) grid searches scored on the same historical panel that reports the winner — with zero DSR/PBO/multiplicity correction ever applied to the search itself**, even though the repo runs exactly that correction religiously for strategy-candidate discovery. — H: applying a closed-form best-of-N deflation to the already-logged per-config scores would shrink the winner's margin to within the noise floor. — Hook: pure arithmetic on numbers that should already be sitting in the 2026-04-17 ADR / `core/mc/modes.py:643-658`; if the losing configs' scores were never retained, that absence is itself a second, separately-flaggable finding.

**C2. TradingView's exported OHLC *price values* (not just bar existence) for CME futures have never been tested against ground truth for any instrument** — Q-TVCOV-1 checked coverage only, for 3 symbols, with price comparison explicitly excluded as a forbidden move. MGC/MCL/M2K are already feeding closure-grade discovery verdicts without even that narrower census. — H: at least one newly-onboarded micro's exported OHLC diverges from an independent same-date reference by more than a de-minimis tolerance. — Hook: hand-diff ~10 arbitrary days' O/H/L/C against CME's free published settlement page.

**C3. Two data-integrity "safety nets" give false comfort: the mandatory feed-equivalence pre-flight tests a retired CFD pair and cannot execute anymore (flagged broken twice, no ruling), and the vendor SHA256SUMS gate — by design — cannot detect a file wrongly sourced but hashed correctly at capture time**, a limitation stated nowhere in the repo. — H: no document states the manifest gate's provenance blind spot, and no CME-era feed-equivalence replacement exists. — Hook: `rg -i "byte.stab|capture.time|wrongly sourced"` across `docs/` (already run, 0 hits).

**C4. `rejected_signals.md` / `rejected_candidates.md` are governed by a purely reactive, author-initiated re-proposal trigger with no scheduled symmetric re-examination** — and the repo's own history shows this is live, not hypothetical: the family K-bank sat as a "never softens" hard gate for weeks, foreclosing the repo's most-instrumented instrument, until an operator happened to bump into it. — H: no scheduled process anywhere re-examines a standing REJECTED verdict independent of chance. — Hook: `grep -c "Re-proposal bar"` vs any "scheduled re-check" language across both registries (already run, 0 hits on the latter).

### Tier D — blast radius 2-3, narrower or lower-consequence

**D1. Rule 7 names "MEMORY.md + memory files" as the canonical owner of durable atomic facts, injected into every session — but that path lives entirely outside the git worktree, so no Great-Prune retention category and no gate-battery check can ever reach it.** A stale memory line has zero mechanical tripwire; it just re-enters every future session as settled fact. *(Direct, load-bearing for this very audit's own Sources-Read discipline.)*

**Disposition 2026-08-23 (P2 Approach A):** Rule 7 owner demoted — see [`addendum`](../../adr/2026-06-30-state-md-role-reduction.md#addendum-2026-08-23--memory-is-assistive-only-not-the-rule-7-owner). Finding text left as the measured defect.

**D2. `scripts/check_advisor_dedup.py`'s hardcoded 5-surface corpus structurally excludes `docs/adr/`** — and dead-candidate prior art (MNQ-ANALOGUE-1, the six-lead P1-CF/P2-CF legs) increasingly lives only in ADR addenda, invisible to the mandated dedup-first check.

**D3. The Call-1 decay trigger is calibrated tight (σ=1.0 vs a kill-trigger's 2.0) on the explicit premise that a false-positive demotion is "cheap because reversible" — but no coded, ADR, or state-file mechanism exists to promote a demoted incumbent leg back up.** The only paths back are an undocumented hand-edit or a ~6-month whole-ADR revert trigger.

**D4. Three independent multiplicative de-risk factors (DD_SCALE × lifecycle × Call-4 beta-death) compose in one real production call path to a reachable 0.05-0.10× sizing regime that only the pairwise cases are ever tested.**

**D5. Notice-phase's 5-tool discovery stack's representational coverage was never itself posed as a question** — the one full end-to-end run (DISC-CAMP-0) exercised only 1 of 5 tools and returned 0/6.

**D6. Call 5 reserves operator sign-off for the one lifecycle step that zeros capital (WATCH-2→RETIRED) — but ordinary autonomous integer-floor arithmetic already reaches "zero contracts" from a routine WATCH-1 demotion, and the repo has only ever asked whether that zero is numerically correct, never whether reaching it this way should require the same sign-off.**

**D7. CLAUDE.md and two workflow files assert GitHub Actions is disabled repo-wide — false since 2026-08-14; `gh api .../actions/permissions` returns `enabled:true` and jobs have run green on every push since.** Low blast radius on its own (documentation staleness) but it's the frame every agent reads before deciding how much to trust CI — and it masks Tier A's #1 finding (branch protection) behind an obsolete "CI can't do anything yet" story.

**D8. The public-disclosure ADR accepts "a sufficiently motivated reader could partially reconstruct strategy behavior" as residual risk without ever attempting the reconstruction** — and the load-bearing sizing numbers (risk%, pyramid, instrument, timeframe, lock version) are already, by design, sitting in the public tree.

**D9. The sentinel queue (`docs/notes/sentinel/queue.md`) — assumed a complete append-only record — silently lost 11 open Action items (7 PREREG-RUNEDIT + 4 PREREG-SAMECOMMIT against MNQ studies) when the 2026-08-14 public-repo history restart recreated it from empty.** No commit, ADR, or STATE row anywhere confirms those 11 were dispositioned before the cut. *(retention_tier: `other` — this is the one finding whose only remaining $0 step needs private-archive access this session doesn't have.)*

**D10. The D-S-A pre-Q gate's own canonical text (`inqhiori-canon.md`) is stale: a live gate audit already declared a 5th permitted D-test beyond canon's stated 4, and directly falsified canon's own "D is reversible" claim for gitignored vendor bytes — neither correction was ever merged back.** This is the single most-invoked mechanism in the methodology layer, and the Great Prune's own classifier-failure log shows near-misses in exactly this domain.

---

## §5 — Scoring caveat

The Triage stage's `fragility (1-5)` field was specified as "how likely the assumption is actually wrong." Most triage agents used it that way. Three (Tier A items A2, A4-A6 above, i.e. the M1-confirmed-base-interlock, the M1-skew-audit-gap, and the c1-sizing-beta-death items) instead scored fragility **1** while stating in the same breath that they had *already directly confirmed* the gap via a zero-hit grep or direct code read — i.e., they used the field to mean "residual uncertainty in my own finding" (near-zero) rather than "probability the comfortable belief is wrong" (which their own evidence puts near-certain). This inverts the intended scale for exactly the items where the evidence is strongest. The blast-radius field (1-5, "what breaks if wrong") did not show this inconsistency and is trustworthy as scored.

**Repair applied:** §4's tiering above uses blast_radius as the primary sort key and treats "already directly evidenced during the sweep" as a confidence upgrade, not the raw fragility×blast_radius product from the workflow's own JS sort. The raw scores are preserved in the workflow journal (`journal.jsonl`) for anyone who wants the unmodified numbers.

**Candidate lesson (below the two-firing bar — watch, don't graduate yet):** a triage/scoring prompt that asks for a single "likelihood the belief is wrong" number is ambiguous when the same pass already ran the falsifier — worth splitting into two explicit fields (`prior_uncertainty` vs `post_check_confidence`) if this workflow pattern is reused.

---

## §6 — Cross-cutting pattern observed

Six of the 25 findings (A2, A3, A4, A5, A6, D6) cluster on one theme: **the c1 rail's live-safety interlocks are consistently described in prose (ADRs, acceptance packages, docstrings) with more rigor than they are wired in code.** The M1 ADR names a "confirmed-base interlock," a "bounds size vs. bounds identity" distinction, a skew-detection capability — and in each case the code path that would make the described property real either has zero production callers, is never invoked by the arm interlock, or is bypassed by the live sizing formula. This is not five unrelated bugs; it reads as one structural gap between the M1 acceptance package's own stated scope and what the arm interlock mechanically checks (`require_resolved=True` validates schema/status fields, never re-derives whether the underlying capabilities it certifies are still wired). Worth naming explicitly before `dry_run` is ever flipped, independent of which individual items above get promoted to formal Qs.

---

## §7 — Programme-audit signal check

- [ ] Belt-patches without independent corroboration? — No; this sweep *is* the independent corroboration pass, run precisely because none existed for this angle.
- [x] Belt that only grows, never prunes? — Adjacent, not squarely hit: D7/D10/B5 show three separate canonical documents (CLAUDE.md, `inqhiori-canon.md`, the public-visibility ADR) that accreted corrections elsewhere in the repo without the original document being patched — a growth-without-repair pattern at the *documentation* layer, not the gate-battery layer this diagnostic usually targets.
- [ ] Falsifier thresholds drifting toward "we'd never hit this"? — Not observed in this sweep.
- [ ] Methodology invoked to rationalize a decision already made? — Not observed.
- [ ] SNAG pattern (multiple null/ambiguous loops same domain)? — Not applicable; this is a first-pass discovery sweep, not a repeated investigation thread.
- [x] Cross-layer contamination (methodology citing portfolio evidence or vice versa)? — D10 is exactly this at one remove: the methodology-layer canon (`inqhiori-canon.md`) has an object-layer-shaped staleness (a gate audit found a correction and it never propagated back) — worth a light cross-reference to `programme-audit`'s quarterly cadence rather than a full escalation.
- [ ] Negative heuristic crossed without repair? — Not observed.

No box triggers a mandatory escalation to `programme-audit` on its own; D10 and the D7/B5 documentation-drift cluster are worth surfacing at the next scheduled methodology audit as a pointer, not a fresh full audit.

---

## §8 — Recommended routing (operator decision, not executed by this audit)

Per the parent-Q convention ("named, not opened") and this session's own Depth answer (inventory + triage only), **none of the 25 findings above have been promoted to a numbered Q or written into `docs/briefs/INDEX.md` / `STATE.md`.** That requires an explicit operator GO per item. Suggested triage, for the operator to confirm or override:

- **Promote to a formal Q now (Tier A, A1-A6):** all six are $0/near-zero-K to falsify definitively and gate a live-safety-relevant belief before `dry_run` is ever considered. A1 (branch protection) and A2 (confirmed-base interlock) in particular sit directly upstream of the M1 arming gate's own credibility.
- **Stage as a Board/forward-trigger row (Tier B):** well-grounded, cheap to check, but none is independently blocking — B1 (MC block-bootstrap validity) is the highest-leverage of this tier since every published number in the repo traces through it.
- **Leave as audit-note-resident findings, re-surface at next relevant touch (Tier C/D):** lower blast radius or narrower scope; several (D1, D9, D10) are genuinely cheap to close but need either private-archive access (D9) or a documentation-only patch (D10) rather than a falsifier.

---

## §9 — Audit hooks (aggregated, runnable)

```bash
# A1 — branch protection
gh api repos/Joshua-Asante/first-passage/branches/main/protection
gh api repos/Joshua-Asante/first-passage/rulesets

# A2 — M1 confirmed-base interlock production callers
rg -n "set_confirmed_base|confirm_executed_base" --type py

# A3 — c1 sizing host beta-death composition
grep -n "get_effective_multipliers\|beta_death_assessment\|BETA_DEATH" ops -r

# A5 — M1 tree-skew check, never wired to any cadence
python scripts/validate_c1_monitoring_acceptance.py --check-tree-skew

# A6 — per-trade loss cap, absence check
rg -i "(per.?trade|single.?trade|loss.?cap|max.?loss)" core/ ops/ docs/adr/ docs/spec/

# B2 — K_intrinsic self-report vs actual axes explored (manual per-run read, no single command)

# B3 — S5 concurrency self-declaration
# clone tests/fixtures/promotion/clean_packet.json x3 with distinct IDs, run
# validate_promotion_packet() / refute_promotion_packet() on each locally

# D7 — CI-enabled staleness in canonical docs
gh api repos/Joshua-Asante/first-passage/actions/permissions
gh run list --workflow=manifest-check.yml --limit 10
```

---

## Iterate — loop exit

- **Verdict used:** N/A (this is not a Q closure) — treated per INQHIORI canon §16 as an OUTER-loop iteration completing at I→N→[D-S-A]→Q formation for 25 candidates; H stated per candidate; ready for O (Observe, i.e. operator review of this document) → R → I.
- **Model update:** The repo's closed-Q registry is dense enough that a blind re-derivation pass would have wasted most of its budget on already-settled ground — the D-gate deleted 1-in-6 candidates precisely for this reason. The genuinely unexamined territory clusters less in "is the edge real" (extremely well-covered) and more in **the live-safety interlocks' gap between documented intent and wired code**, and in **governance artifacts whose own status/staleness is trusted without a mechanical check** (branch protection, ADR Status fields, CI-enabled claims, memory-file reach).
- **Next:** ITERATE
- **Routing:** Return to Q (reframe as 6-25 individually pre-registered falsifiable Qs, per operator election in §8) — not Identify (the corpus assembly here was thorough enough that a fresh I/N pass is not warranted before at least Tier A is dispositioned).
- **Entry packet:** *(required — Next = ITERATE)* Each of the 25 findings in §4 carries its own frozen H + cheap-falsifier sketch + file:line grounding — that IS the entry packet for whichever items the operator elects to open as numbered Qs. Forbidden re-opens: none of the 5 items in §3 (D-gate already closed them with citation; re-opening any needs new evidence beyond what this sweep found). Budget: falsifying all 6 Tier-A items is estimated at $0/near-zero-K per item (grep/local-test/one-timed-drill); no item in this audit requires a paid data pull or a new backtest.
- **Stop rule / re-proposal bar:** Any Tier C/D finding not promoted within this audit note's lifetime re-surfaces at the next relevant touch (next M1/c1-rail session for A/B tier items already promoted; next quarterly methodology audit for D10).
- **Board write:** `STATE.md` OPERATOR QUEUE — none added by this audit (queue is capped at ≤5 and already has 2 live items; promoting Tier A findings to the queue is the operator's call in §8, not pre-empted here).

---

## Verification

```bash
# Confirm the workflow run this audit is grounded in
# (journal has one {"type":"result",...} line per completed agent)
cat "C:\Users\joshu\.claude\projects\C--Users-joshu-multi-firm-operations--claude-worktrees-strategy-research-assumptions-15b4a4\aa9e0bd1-e747-4a3c-805e-c67524c0170e\subagents\workflows\wf_f6d1f8a3-330\journal.jsonl" | head -5

# Confirm no existing owner doc was silently duplicated (Rule 8 sub-rule 10 — already run pre-authoring)
rg -i "assumption.?audit|unexamined assumption" docs/
# Expected: no hits besides this file

# Spot-check one Tier-A finding against source directly
rg -n "set_confirmed_base|confirm_executed_base" --type py
# Expected: 0 hits outside tests/
```
