# Programme audit — strategy-candidate admission/validation gate stack (meta layer)

**Layer:** meta (methodology). The gate stack is a set of **epistemic moves that generate decisions**, not the portfolio.
**Audit date:** 2026-08-03 · **Repo anchor:** `a1123b8`, worktree clean.
**Window:** 2026-05-06 (regime-gate canonization, earliest gate in the stack) → 2026-08-03.
**Trigger:** degeneration-signal review requested by the operator — *"I want to make sure the gates are pertinent to the challenge at hand."* A 2026-08-03 **portfolio-layer** measurement prompted the question. Per the two-layer coupling rule a portfolio verdict **may trigger** a methodology audit but **may not supply its evidence**; that measurement appears nowhere below as evidence.
**Method:** 20-agent adversarial workflow — 4 gate-cluster mappers → lineage/window → 7 Lakatos diagnostics → 7 hostile verifiers (refute-by-default; auto-refute on cross-layer citation) → synthesis over surviving findings only. 837 tool calls. Findings that failed verification were dropped; where a verifier supplied a narrower surviving form, that form is used verbatim.

**Programmes audited (10):** G1 frozen prop survivor-scoring · G2 DSR demonstrability floor / Clause K · G3 cost-law pre-screen · G4 regime-robustness gate · G5 prop_envelope v1.0 (E1–E7) · G6 statistical validation battery (Stage 2–8) · G7 K accounting + pre-registration manifest · G8 instrument-ledger class bar M1 · G9 strategy authorization lifecycle · G10 external-mechanism harvest intake.

---

## §0 — Rule 0 reads (verified 2026-08-03 at `a1123b8`)

Gate-defining artifacts were read by the mapping agents; every finding below carries its own anchor inline. Parent-session reads establishing scope and layer discipline:

| Source | Anchor | Supplies |
|---|---|---|
| `.claude/skills/programme-audit/SKILL.md` | worktree | Two-layer architecture, seven diagnostics, five verdicts, traps #1–#7. |
| `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` | `be6dda6` 2026-07-13 | G1 frozen thresholds; blob-identity verified in §3.7. |
| `core/lifecycle.py` | `4441c72` 2026-07-11 | G9 ladder + L180 import-time self-check. |
| `core/mc/simulation.py` | `fc14682` 2026-07-30 | `intraday_low`; the "LOWER BOUND" docstring load-bearing in §3.1/§3.6. |
| `core/firm_rules.py` | `89a069a` 2026-08-02 | The two OPEN DEFECT blocks on `dd_lock_offset_usd`. |
| `docs/notes/audits/programme-audit/` (7 prior notes) | listed | Audit lineage; prior follow-up execution checked in §3. |

**Layer-discipline attestation:** no verdict below cites strategy Sharpe, PF, win rate, book drawdown, eval pass/bust rate, or P&L as evidence. Cross-layer contamination is degeneration signal #6 and was enforced mechanically via a per-finding `cross_layer_clean` flag.

**Post-authoring merge (recorded, not re-stamped).** All reads above were performed at `a1123b8`. The branch subsequently merged `origin/main` `d4a1cc9` (PR #624, params.toml gate retirement). Every file anchor cited above was re-verified unchanged across that merge; `scripts/validate_params.py` was deleted by #624 and the §10 hooks were repaired accordingly.

**Prediction registered before the audit ran, and its outcome.** The parent session predicted (a) G2 would return *healthy-but-mis-aimed*, and (b) the absence of a cadence limb would surface under diagnostic #1 or #5. **Both were wrong.** The audit finds G2's demonstrability denomination is **correct scoping, not a defect** — G2 explicitly disclaims the survival question and routes it to G1 — so the stack is *layered*, not mis-aimed. No cadence finding survived verification. Recorded per trap #1: the prediction is preserved rather than retrofitted.

---

# §3 — Diagnostics

## §3.1 Hard-core integrity

**No gate's acceptance criterion was substituted, waived, or applied in a form its hard core forbids.** Every candidate admitted or rejected in the window was scored against the criterion its gate actually states. What the verification pass found instead is a cluster of *labelling, staleness and bindingness* defects sitting on top of intact criteria.

Confirmed defects (all survived adversarial re-verification):

- **G1 — stale measurement-fidelity label on live-consequence outputs.** G1's frozen §3 reserves the "optimistic-lower-bounds" label for Bulenox/BluSky and calls `trailing_locking` "the engine-faithful geometry", but since 2026-07-30 the engine's own docstring makes EVERY bust figure computed without `intraday_low` a lower bound — including both `trailing_locking` tiers. Executed checks confirm no G1 consumer carries an intraday caveat and none feeds the argument, so the two 50K figures currently defeating the 11-08 demotion clause are unannotated lower bounds. This is stale labelling on live-consequence outputs, not a substituted acceptance criterion. `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md:133` (`be6dda6 2026-07-13`); `core/mc/simulation.py:84` (`fc14682 2026-07-30`); `lab/analysis/c1/c1_band_rescore_2026-07-24/RESULTS.md` (`c271411 2026-08-03`).
- **G8 — the mandated consult has never mechanically fired.** G8's mandated `cell` consult has no recorded execution anywhere — zero of 8 manifests carry `profile_cell`, and zero pre-registrations (including post-ADR candidate briefs) record consult output — while `--lane` defaults to `"blind"` and the consult gate fires only on `mechanism-first`. Pre-registrations do cite profile blocks in prose, so the ledger is not ignored; the mechanical, recorded gate is what has never fired. `lab/discovery/register_search.py:207,231,283,493`; `docs/adr/2026-07-25-instrument-profile-index.md:80`.
- **G9 — canonical owner routes to deleted code.** `docs/methodology/strategy_lifecycle.md:113` still reads "realize a WATCH-tier haircut at the **account-multiplier layer** (`ops/accounts.py` / `cli.py lots`)"; `ls ops/accounts.py` → *No such file or directory* (deleted `ff3510d 2026-07-24`). Verification found the dangling reference at **three** sites, not one — `:52`, `:60`, `:113` — including the ratified "Integration layer (corrected against production)" paragraph. Doc anchor `ae91ddd 2026-07-17`, i.e. stale rather than wrong-at-authoring.

Narrowed on verification (use these forms, not the stronger originals):

- **G4 — a bindingness gap in the importing brief, not a hard-core violation.** The regime gate was imported as a rider by G1 §7(7) into a decision class the gate's own scope section marks "Not required", and the consuming candidate-1 pre-registration (`:213-217`, `58fff1d`) fixed its bindingness at zero in advance — so when the gate returned GATE FAIL (regime-fragile) on BOTH discharge tiers, the candidate was still recorded `discharges_falsifier: True` and admitted to G8 with a caveat. G4's hard core governs risk-constant LOCK CANDIDATE recommendations, not strategy-book additions.
- **G3 — venue basis, disclosed and non-determinative.** ORB-MNQ-1's Stage-2 cost-law threshold was pre-registered at Bulenox $0.61/side for cross-campaign comparability while the registered account is Tradeify at $0.91/side, and that specific Stage-2 gate was never formally re-run at the registered venue's schedule — though the arithmetic implies it would still clear (≈4.18× vs the 4.0× floor), and Stage-7 onward the campaign did compute at Tradeify economics.
- **G6 — Stage-6 PASS is venue-scoped, and said so in its own verdict line.** ORB-MNQ-1's Stage-6 RESOLVED clears its full-window limb only at Bulenox economics; at Tradeify $0.91/side the full window fails the annSR ≥ 0.85 limb (+0.835). The scoping was disclosed in Stage-6's own verdict line and quantified at Stage-7, and Tradeify passes on the pre-registered 2021+ window — a disclosed, self-run sensitivity, not a criterion swapped under the gate's name.
- **G5 — the annotation was never written; the criterion was computed.** The literal closure-time `DEPLOYABLE-DEFAULT-ENVELOPE: YES/NO` annotation required by `prop_envelope_default.md:26` was never written for ORB-MNQ-1 (`rg` exit 1 across the campaign directory), even though the underlying 4× cost hurdle at the deployable round-trip count was computed at Stage-2 and per firm at Stage-7. Separately, every recorded envelope verdict repo-wide is YES; a NO appears only in contract text.
- **G9 — a doc inconsistency, not a ladder defect.** The ADR's axis prose lists `CANDIDATE` with a multiplier; the ratified Call-2 table it designates canonical omits it. The code matches the ratified table; the "@ 1.00×" on admissions is the documented absent-entry default, disclosed in ADMISSION.md as carrying no `lifecycle.py` write.
- **G8 — a pre-declared limitation, now realised.** M2K's PROFILE block still carries `cost_hurdle: 9.81` while its M2 prose row records the 2026-07-28 recomputation at 11.89 bp/RT, and `check` cannot detect the mismatch — a drift risk `docs/adr/2026-07-25-instrument-profile-index.md` §2a explicitly ratified in advance, with the consult output carrying both the ILLUSTRATIVE basis string and a "VERIFY at #M2" pointer.

**Contrary to the audit's own priors:** G1's anti-drift enforcement is real. `load_scoring_thresholds` is imported by **12 active `lab/analysis` harnesses** plus its own test, the frozen pre-registration is blob-identical to its single freeze commit, and the parser raises `ValueError("...refusing to guess a default")` rather than defaulting. This is structural anti-drift at the definition layer only.

## §3.2 Belt churn — numbers

Inventory derived from this audit's gate map (§2), with two verified corrections applied. **No pre-existing repo artifact enumerates belt events; this table is the audit's own construction.**

| Gate | ADD | REVISE | REMOVE | Net |
|---|---:|---:|---:|---:|
| G1 survivor-scoring | 5 | 2 | 1 | +4 |
| G2 DSR floor / Clause K | 5 | 4 | 0 | +5 |
| G3 cost-law | 8 | 0 | **0** | +8 |
| G4 regime-robustness | 6 | 1 | 1 | +5 |
| G5 prop_envelope | 4 | 6 | 2 | +2 |
| G6 validation battery | 6 | 2 | 1 | +5 |
| G7 K accounting | 6 | 4 | 0 | +6 |
| G8 instrument-ledger bar | 9 | 2 | 1 | +8 |
| G9 lifecycle | 2 | 2 | 1 | +1 |
| G10 harvest intake | 5 | 3 | 0 | +5 |
| **STACK** | **56** | **26** | **7** | **+49** |

Add:remove ratio **8:1**. **Four gates have removed nothing ever: G2, G3, G7, G10.** No gate is net-neutral or net-negative.

Two corrections that changed the arithmetic, both against the programme:

1. **G3's only logged removal is disproven.** `lab/discovery/cost_mnq.py:23` still reads `DEFAULT_FIRM_KEY = "Bulenox_100K"` at HEAD, has exactly one commit ever (`e1c51f0 2026-07-16`), is blob-identical to it, and is still imported by two live runners (`d5_nq_intraday_mom_2026-07/run_stage2_4.py:24`, `d5_recost_2026-07/run_recost.py:33`). `cost_model.py:8-13` states verbatim that it "does NOT supersede the frozen per-campaign `cost_*.py` files." G3 is **8 adds / 0 removals**.
2. **The self-critical prune count is zero.** NONE of the removals is a genuine self-critical prune of live belt. The event nominated as the sole prune (G8's session-confluence carve-out, `6ef7d8a 2026-08-02`) removed nothing: it is **+58/−0**, the carve-out text survives verbatim at HEAD, and the falsification was recorded as an appended annotation rather than a strike. The true self-critical prune count across the window is **ZERO**.

Direction of the removals that do exist:

- **G4's single removal removes an argument FOR running the gate.** `cd8b617 2026-08-02` deleted "The gate is cheap (typically <30min wall-clock)" while adding an exemption and conditioning the default-to-run rule. Verification found **three** narrowings in that one hunk, not one (the Pareto limb also gained "for a risk constant").
- **G5's mini+micro removal net-ADDED constraints** — the same commit (`2fbc996 2026-07-24`) added "NO US Treasuries", the account-aggregate cap, hedging prohibition, and the whole §4a section. Firm-driven fact correction, not self-criticism.
- **Two removals are collateral rot** — gates silently stopped being able to fire. `grep -n "^ACTIVE_FIRM = " core/firm_rules.py` → exit 1, and `strategy_lifecycle.md:113` routes to code deleted ten days before this audit.

Structural pattern: **pruning happens only at generation boundaries.** Gen-2 gate machinery has had zero file deletions ever (`lab/research_utils` 0 deleted / 12 live; `lab/discovery` 0 deleted / 17 live), while Gen-1 was wiped wholesale (`bdc45a3`: 67 files, 11,212 deletions in one commit) and the wider repo prunes heavily (207 deleted paths under `docs/methodology`, 110 unique under `ops`, 9 retirement ADRs).

Growth rate is **flat, not accelerating**: 2026-08-01→08-03 carries ~2.33 events/day against July's ~2.35/day. Two new belt artifacts were authored on the audit date and remain **untracked at HEAD** — a `Proposed` WATCH-1H rung for G9's ladder and a `FROZEN` c1-cadence pre-registration — so the stack has not reached equilibrium.

**Counter-evidence:** growth is accretion around frozen cores. Five gate artifacts are blob-identical to creation and no threshold number drifted (§3.7). But value-stability is not test-stability: G4 was weakened on 2026-08-02 by scope narrowing alone with no number touched, and `COST_LAW_MULTIPLE 4.0` was demoted from gate to "T1 pre-screen constant, NOT a ratified gate" at `lab/analysis/c1/tradeify_fade_stage0_2026-07-30/design_law.py:11` while keeping its value.

## §3.3 Progressive evidence

Two clean instances, both of the stack correctly predicting **its own** failure modes rather than the domain's behaviour.

1. **G9 — Q-PYRPARITY-1 (the only prediction anchored by a provably prior commit).** The lifecycle ADR's ratification commit `aff350f 2026-07-10 20:10:30` already contained: "confirm scaling the input `risk_pct` scales the whole pyramided stack proportionally (if it does not, the haircut must be applied at the account-multiplier layer instead — the operational fallback)." Tested 2026-07-17 against an accept band 0.500 ± 0.005 frozen before data; returned FALSIFIED-NONPROPORTIONAL (MYM base median 0.8707 / add 0.9164); the pre-committed fallback was invoked; the closure records "No criterion moved after data (Trap #12 clean)". Outcome predicted, cause not (a TV/symbol qty ceiling, not Pine non-linearity).
2. **G1 — the sub-100K realizable-book pre-registration attacked its own load-bearing numbers and reported the adverse reading.** Freeze `e5dc06d` strictly precedes the run. Every sub-100K FRIENDLY tier degenerates to a 1-leg MYM book missing Part A (4.5367% / 4.2933% vs 3.0%); B-cells reproduced to +0.00pp; and novel corroborated content emerged that §4 explicitly declined to predict — "Removing the low-variance MNQ leg RAISES bust roughly 4×… The second leg is not ballast; it is what makes the sub-100K band clear at all." The RESULTS volunteers its own adverse rider rather than suppressing it (`lab/analysis/c1/band_quantization_2026-08-02/RESULTS_realizable_scoring.md`, `c707223 2026-08-03`).

Also verified, and cutting against a pessimistic read: **Q-HARV-0 (closed 2026-07-12) records a corroborated positive** — "The mechanism's primary prediction is corroborated at H1" (+19.21 bp, permutation p = 0.0129, clearing the 4× cost hurdle 6.84 bp, GC negative control clean p = 0.70, covariance monotone, native-MES micro-OOS same-signed).

What does **not** count, on verification:

- **No PASS the stack has emitted has survived downstream.** The 2026-07-15 Class-S candidate #1 `RESOLVED (DISCHARGED)` was withdrawn 2026-07-22 on a defective input; the 2026-07-16 ORB-MNQ Stage-6 RESOLVED was rejected as a book leg on 2026-07-17 (Q-COMPOSE-1, pre-reg frozen at `970b5ed 2026-07-16 23:31:51`, a genuine pre-run commit). G5's envelope has emitted zero NO verdicts repo-wide and the profile-consult gate has bound 0 of 8 manifests.
- **G2's §R attestation limb failed twice on 2026-07-16** (D5, H-OD-1): both attestations declared REACHABLE while arguing in Sharpe space against a bp-space cost gate, costing two full freeze→GO→register→pull→screen cycles and two banked family-K. The remedy was the same-day supersession ADR — belt repair after anomaly, not prediction.
- **G3's D5 kill survived a well-motivated re-open** on the strongest contrary grounds available (D5-RECOST-1 repriced the hurdle 3.7× in the candidate's favour, 11.063 → 3.006 bp, and it still died at OOS mean −0.33 bp). The corroborated content is the candidate's death and the pre-recorded "gross ≠ net on MNQ" caution — not the cost-law criterion, which the RESULTS itself calls moot as the binding cause — and the corroborating run is in-house, not independent.
- **G10's Requirement 5 produced real economy, not the predicted mechanism.** The three post-Req-5 seeds (ORB-ZB-1, NG-EIA-1, RATES-EV-ZF-1) all closed FALSIFIED at Phase-0 with $0.00 Databento spend, K = 0 and no manifest — a genuine improvement on the two pre-Req-5 campaigns, which each burned a full cycle and banked family K. They did not die "for the cost of one division": each required an operator GO, a multi-million-row pull and a bespoke Phase-0 harness.
- **G2's Cap freeze was real but its corroboration is entailed, not risky.** `453148a 2026-07-14 14:05:36` froze the realism-band formula "before any anchor is measured." The low-K prediction follows from the same deterministic floor arithmetic. And the claim that every post-freeze manifest is K ≤ 2 is false: `st_eh_supertrend_grid.json` opened 2026-07-26 with `declared_K = 84` and was halted by operator direction, not by the gate.
- **G8's session-confluence discharge is honest scoping, not prediction.** The bar recorded the thread as "untested"; Q-SESSCONF-1 then measured it at $0/K=0 against a threshold frozen before the run (Δ* = +0.124; measured +0.091).
- **G5's overlay re-verify is an error-catch, not prediction.** The 90-day schedule contributed nothing — the defect found was our own config carrying a funded-stage mechanism into eval rows, not firm drift.
- **G6's DSR self-test is implementation verification.** Re-run this session: planted-overfit 0.3079 (< 0.95), planted-real 0.9935, 6 tests passing. Non-vacuous, which rules out the empty-assert failure mode — but both controls are generated in-repo.

## §3.4 Degeneration evidence — was anything patched to rescue a conclusion?

**No threshold was moved to rescue a conclusion anywhere in the stack.** Three genuine degeneration-shaped events, all in scope/accounting space:

1. **G7 — K-banking revised twice in six days, each reducing what the MNQ family had banked.** Clause 2-C (executed-K closure) was drafted `80133f2 2026-07-26 23:24:54` and ratified `31d7df0 23:57:32` — the same night the campaign it was first applied to was stopped (`st_eh_supertrend_grid.json` closed 2026-07-27T03:47:44Z = 23:47 EDT 07-26), banking K = 2 against `declared_K = 84`. It reversed prior ratified doctrine ("abandoned campaigns still count their K", `2026-07-11-discovery-campaign-defaults-ratified.md:45`) and an executed `git log --all -S` search over `executed K` / `declared_K` / `operator-stopped` before 2026-07-26 returns nothing — **not predicted by any prior artifact**. It reopens exactly the families the declared count would have killed (MNQ floor 0.98, MYM 0.85 vs ~1.44). Mitigating and load-bearing: the ADR's own §3 names the tempting alternative and disqualifies it — "Methodology-layer p-hacking, and this session banked the K in question — the optics alone disqualify it" — ships 10 adversarial guard tests, and carries a retroactive-revert falsifier. The second revision (2026-07-31, open manifests bank nothing) conforms practice to text that already existed at `strategy_harvest.md:26` since 2026-07-15.
2. **G4 — firing scope narrowed inside a commit whose governing brief authorized only a pin repair.** `git diff cd8b617^ cd8b617 -- docs/methodology/regime_robustness_gate.md` adds "ORB-MNQ / venue-native research that does not change locked risk constants" to the Not-required list, conditions the default-to-run rule on "a risk-constant LOCK CANDIDATE is in play", adds "Do not fire it as ceremony", and deletes the cheapness rationale. The durable brief rows (`docs/briefs/programs/2026-08-02-...-prune.md:24,76,88`) and the SESSIONS entry describe this file's change as a pin repair only; the brief's §4 falsifier limb tests only that the pin resolves. `git show --stat cd8b617` touches two ADRs; neither mentions the regime gate.
3. **G1 — freeze integrity is self-attested and the mechanical guard is structurally blind.** `git show --name-status 153b64e` returns five `A` entries: the 268-line prereg, RESULTS.md, the report JSON and both runners, all added together; `git log --all` on the prereg returns only that commit. Re-implementing `ops/sentinel/scan.py::_corresponds` and running it on the pair returns `False` — both `_qids` sets are empty. 25 of 47 pre-registrations carry no Q-ID. Verification found the gap is **wider than claimed**: because `lab/analysis` RESULTS basenames also carry no Q-ID, **no pre-registration filed in the repo's prereg directory can ever pair with a lab/analysis result** — the guard only ever fires on same-directory pairs.

Narrowed and largely defused on verification:

- **G9's WATCH-1H rung is Proposed and untracked; no code changed.** `git ls-files` returns empty; `core/lifecycle.py` is unchanged since `4441c72 2026-07-11` with the four-rung ladder and its L180 self-check intact. The rung VALUE is post-measurement, but the SELECTION RULE was pre-committed 11 days earlier by `docs/adr/2026-07-23-c1-rung-selection-ev-objective.md` (`Accepted`, `9ab2e8b`). The sharper defect is that the 08-03 ADR never cites that ADR and does not present the both-halves regime PASS it makes a hard precondition.
- **G3's status downgrade was superseded the next day.** `docs/notes/2026-07-31-fade-stage1-frozen-rulings.md` (`fca5ba6`) ruling `COST-MULT-4X-2026-07-31` fixed 4× as the program's governing admission multiple — unchanged in value, frozen before any mechanism was scored, $0 spent, K unchanged — and corrected the "may be empty" premise as "wrong as stated". Residual: doc staleness at the design spec, line 277.
- **G5's E6 edit is a literal change-control breach** (`ops/prop_envelope_default.md:6` says §1–§3 change only by ADR) with no covering ADR, but the edit tightens rather than loosens, was declared in brief/commit-message/SESSIONS, was operator-merged in PR #612, and matches prior practice (`2fbc996` edited the E1 default row the same way).

## §3.5 Boundary respected

**Held under direct pressure, verified:**

- `docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md:63,88` pre-forbids "Loosen Clause K's cap or family pooling to reopen MNQ/MYM" and "Touching Clause K's cap (K_eff ≤ 3), the floor table, or family pooling", and `git show b304f2c:...Q-KBUDGET-1-screen-preregistration.md | sed -n '24,25p'` is byte-identical to HEAD at the same line numbers.
- `docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md:108` declines a falsifier **tightening** on the audit date: "tightening a falsifier after seeing the data is the mirror image of loosening it."
- **G8's §5 no-backfill heuristic was crossed twice, both times correctly.** Each crossing is declared, scoped, operator-approved and carries an explicit "What this override does NOT permit" boundary (`2026-06-11-...-cfg-fingerprint.md:194-196`; `2026-07-25-instrument-profile-index.md:84-90`).

**Crossed and unrepaired:**

- **Rule 8 sub-rule 7 (prereg freeze must be an earlier commit than results) crossed at least three times in the G1 family, none flagged.** `--diff-filter=A --follow` shows `df13e74 2026-07-16`, `153b64e 2026-07-24` and `9933555 2026-07-30` each introduce prereg and RESULTS together; `rg '153b64e|9933555|df13e74' docs/notes/sentinel/queue.md` → exit 1. All three postdate the rule's 2026-07-02 shipping. Root cause is §3.4 item 3. (`PREREG-SAMECOMMIT` is defined at `docs/operational_rules.md:272`.)
- **G4's 2026-08-02 narrowing has no decision artifact.** `rg --no-ignore 'ORB-MNQ / venue-native research'` returns exactly one hit — the gate doc itself.
- **Rule 11 back-propagation reached 2 of 4 affected artifacts** after the Phase-4 `ACTIVE_FIRM` deletion. Repaired: `2026-07-12-prop-portfolio-four-friendly-firms.md:155-162` and the dedicated record `docs/notes/2026-07-24-class-s-scoring-chain-coupling-and-stale-hooks.md` §1 (which executes Rule 11 (a)-(d) properly, quotes the hook, names the retiring event, supplies the substitute reading, and pre-forbids the tempting repair). Unswept: `2026-07-13-prop-envelope-v1-ratification.md:88` (raises `AttributeError`, header still reads `Superseded-in-part-by: none`) and `2026-07-23-c1-rung-selection-ev-objective.md:129` (still annotates the grep `# unchanged`). Second-order: both repair records describe the Phase-1 state, so they are themselves one retirement stale.

**Alleged crossing that is not one:** the G3 Bulenox cost-basis forbidden move (`D5-RECOST-1-...-scoping.md:73`, committed `e2658bf 2026-07-21`) postdates the ZB/ZF closures it was said to govern, is scoped to its own re-derivation, and its actual prohibition ("without disclosing the sensitivity") is exactly what `docs/rejected_candidates.md:240` satisfies.

## §3.6 Theory comparison — did the chosen design outperform?

**Five instances of the same shape: winning theory documented, losing theory still executable.**

1. **Eval drawdown-lock constant.** SIX `trailing_locking` tiers (4 Tradeify + 2 MFFU) return `dd_lock_offset_usd = 100` at HEAD, twelve days after primary sources falsified it, carrying two OPEN DEFECT blocks (`core/firm_rules.py:266-292` and `:354ff`, `89a069a`) that state the magnitude (2.65% → 4.74%, Part A PASS→FAIL) and direction ("OPTIMISTIC"), while **ten** downstream analysis directories each re-apply the correction as a per-run monkeypatch. M-23 records one measured harm (4.54% → 6.69%, optimistic, undetected four days). It is NOT a lost theory-comparison: the correction's own RESULTS §1 records the eval rows carried a funded-stage mechanism by oversight.
2. **Barrier clock.** `grep -n intraday_low lab/discovery/prop_survivor_scoring.py` exits 1 and the file is untouched since `97011c1 2026-07-13`, seventeen days before `core/mc/simulation.py:68` gained the argument. The §4-discharge, withdrawal and 50K-band figures all ran close-only. Not universally quantified: the 2026-08-03 ORB T2 driver threads the intraday clock while consuming G1's frozen thresholds, so the winning model was adopted in a G1-thresholded measurement within four days — and the historical figures predate the model's existence.
3. **V-estimator (G6).** Three designs tested, the conditional rejected, `V = 1/n` pinned — yet `lab/research_utils/universe_gate.py:369-370` still defaults `var_trials=None` to the empirical estimator, which the ratifying ADR itself records collapses to `0.0` at `K_SPA = 1`, "the plausible outcome of Stage 4's own cost-law 4× hurdle", and the ADR discloses verbatim that "Any caller… that omits `--var-trials` inherits the known-biased default."
4. **Cost basis (G3).** The strict design (`firm_key` required, raises rather than substitutes) landed in the *new* module `cost_model.py:124-142` (`379bbb8 2026-07-26`); the losing `DEFAULT_FIRM_KEY = "Bulenox_100K"` is unchanged and still imported by two live drivers.
5. **H-TSMOM-1 window fork (G2).** Pinned to the strict reading (c) on 2026-07-16 (N ≈ 86, power 0.34, Clause-N FAIL), but `floor_scan.py:85-89` — untouched since `3135a0a 2026-07-15`, one day before the pin — still encodes `clause_n="PASS: power=0.638 at N=192"` and re-executes today printing H-TSMOM-1 as PASS (6 FAIL / 3 PASS where the pin implies 7 FAIL / 2 PASS). The scoping brief's §3 names citing this stale PASS as a forbidden move.

**Comparisons that are open, not won:**

- **K-banking** is currently UNANSWERABLE. Both conventions were priced in advance with consequences stated; executed-K was ratified 2026-07-26 and loosened again 2026-07-31. Verified subsequent evidence: 8 manifests total, latest `opened_at` 2026-07-26T19:35:22Z, and the 07-31 ADR records the freed seat "stays unspent". Eight days with no new campaign is too short and too confounded to be diagnostic.
- **G2's Cap** was resolved at the tight end through a documented adversarial workflow that refused to tune it to a downstream screen's convenience. Re-executing `floor_scan.py`, Cap 2.0 would clear D6 (1.835) and D2-low (1.925) that Cap 1.0 kills. But **no subsequent evidence discriminates**: DISC-CAMP-0 sits at floor 2.05, excluded under both caps, and opened and closed 2026-07-13, before the Cap was resolved.
- **G4 blocking vs non-blocking.** The counterfactual is not established. The 07-15 rider's FAIL was driven by a bust limb the canonical Part C does not contain (its three criteria are pass-rate tests, and the measured H1/H2 pass-rates of 95.47% / 98.30% clear the brief's 50% floor); the bootstrap limb was `nan`; the canonical gate's jurisdiction is risk-constant Pareto sweeps; and the rider's non-blocking status was pre-registered before the run. **The prop lane's rider was stricter on criteria than the canonical gate while relaxing the consequence.**

**Won, and the strongest positive in the set:** the **3.0% eval-bust ceiling** is the one threshold attacked from a direction that pointed LOOSER, with retention chosen anyway and no edit made. Q-BUSTGATE-1 closed FALSIFIED 2026-07-23: fee/upside asymmetry ≈ 12-36:1, EV-optimal rung busts 4.37% H1 / 10.37% bootstrap-95th, Fork A declined, ceiling "RETAINED, unedited". The *corroboration* claimed from the regime gate does **not** hold — that gate's floor is explicitly inherited from the same frozen 3.0% ceiling ("Nothing here re-decides the floor"; "no separate regime floor is permitted"), so it is the same threshold on sub-partitions of the same measurement.

## §3.7 Falsifier check — executed

**Zero numeric threshold drift in every gate constant checked.**

```
$ git rev-parse be6dda6:docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
86e90387cb164324a5e76d7ab355944eefc2b2ad
$ git rev-parse HEAD:docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md
86e90387cb164324a5e76d7ab355944eefc2b2ad
$ git log --oneline -- docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md | wc -l
1
# line 119: headline bust <= 3.0% ; line 121: P(pass) >= 50% ; line 123: Part B bust <= 1.0%

$ diff <(git show 26f3a26:docs/methodology/regime_robustness_gate.md | sed -n '/## Procedure/,/## What this gate catches/p') \
       <(sed -n '/## Procedure/,/## What this gate catches/p' docs/methodology/regime_robustness_gate.md)
(no output)   # Part A/B/C acceptance test byte-identical to canonization 2026-05-06

$ grep -n '^CAP\|^DSR_MIN\|^POWER_MIN' lab/research_utils/axis_screen.py
# ⚠ APPENDED CORRECTION 2026-08-04 (not a strike — Trap #12). The two commands above are
# now STALE AS STATED: at 289535d the prereg has TWO commits, not one, and its blob is
# 25c7803, not 86e9038. Cause: 91137fb "docs(lab): Wave 4 citation repair" rewrote ONE line
# inside the prereg's own §10 hook when the lab theme-nest moved the directory
#   -  grep -n "17.70\|17.7" lab/analysis/tradeify_futures3_remc_2026-07-11/RESULTS.md
#   +  grep -n "17.70\|17.7" lab/analysis/c1/tradeify_futures3_remc_2026-07-11/RESULTS.md
# `git diff be6dda6 HEAD` on this file is that one line and nothing else. The THRESHOLDS are
# byte-identical (3.0% / 50% / 1.0% verified at HEAD lines 117-125), so §3.7's CONCLUSION
# (zero numeric threshold drift) and G1's Progressive verdict both stand unchanged. What is
# wrong is only the evidence's phrasing: "blob-identical to its single freeze commit" must
# now read "thresholds byte-identical; single non-threshold path repair at 91137fb".
# Re-run as:  git diff be6dda6 HEAD -- <prereg> --stat   # expect exactly 1 line changed
31:CAP = 1.0
32:DSR_MIN = 0.95
33:POWER_MIN = 0.50

$ rg -n "COST_LAW_MULTIPLE\s*=" lab/ --no-ignore
lab/discovery/cost_model.py:35:COST_LAW_MULTIPLE = 4.0
lab/discovery/cost_es.py:28:COST_LAW_MULTIPLE = 4.0
lab/discovery/cost_mnq.py:25:COST_LAW_MULTIPLE = 4.0
lab/discovery/cost_mgc.py:17:COST_LAW_MULTIPLE = 4.0
lab/analysis/c1_thirdleg_instrument_map_2026-07-27/instrument_map.py:49:COST_LAW_MULTIPLE = 4.0

$ python -c "import lifecycle; print(lifecycle.TIER_MULTIPLIER)"
{'AUTHORIZED': 1.0, 'WATCH-1': 0.5, 'WATCH-2': 0.25, 'RETIRED': 0.0}
$ grep -n 'DD_TRIGGER\|DD_SCALE' core/dd_protection.py | head -2
78:DD_TRIGGER = 0.015
79:DD_SCALE = 0.40
```

**Drift by another route — falsifiers that cannot fire, or fire against nothing:**

```
# G1 frozen prereg §10 hook 7 -- dead since ACTIVE_FIRM was deleted (fc14682 2026-07-30)
$ grep -n "^ACTIVE_FIRM = " core/firm_rules.py        # prereg expects FXIFY
[exit=1 -- no output]
$ grep -c cost_per_side_usd core/firm_rules.py         # sibling hooks still live
18
$ grep -cE 'summarize_outcomes|bust_trailing' core/mc/preflight.py
8

# G5 ratifying ADR's own runnable audit block (2026-07-13-prop-envelope-v1-ratification.md:88)
$ python -c "import sys; sys.path.insert(0,'core'); import firm_rules; assert firm_rules.ACTIVE_FIRM=='FXIFY'; print('FXIFY fixture OK')"
AttributeError: module 'firm_rules' has no attribute 'ACTIVE_FIRM'    [exit=1]
$ grep -c '2026-07-13' ops/prop_envelope_default.md    # staleness hook -- no expected count ever recorded
12

# G1 measurement fidelity
$ grep -n intraday_low lab/discovery/prop_survivor_scoring.py
[exit=1]
$ grep -n 'LOWER BOUND' core/mc/simulation.py
84:    without this argument is therefore a LOWER BOUND, not an estimate.

# G7 -- three gates added 2026-07-26 have bound zero campaigns; blind default bypasses them
$ rg -n --no-ignore 'profile_cell|profile_consult|reachability_clauses' discovery_manifests/
[exit=1]
$ ls discovery_manifests/*.json | wc -l
8
$ grep -n 'default="blind"' lab/discovery/register_search.py
493:    o.add_argument("--lane", choices=["blind","mechanism-first"], default="blind", ...)

# G5 -- zero NO verdicts in the gate's entire history
$ rg --no-ignore 'DEPLOYABLE-DEFAULT-ENVELOPE:?\s*\*?\*?NO' .
[exit=1]   # 'NO' appears only in contract/template text

# G4 -- the 2026-05-23 override's only named safety net, retired 2026-07-22, nothing re-armed
$ grep -n 'regime.robustness' STATE.md
[exit=1]
$ find . -name 'regime_robustness_gate*.py' -not -path './.git/*'
[no results]    # library-graduation clause unmet after >=6 invocations (cost: M-23)

# G9 -- Call-1 decay falsifier has never been evaluable
$ ls core/lifecycle_state.json
[exit=2]
$ ls ops/accounts.py
ls: cannot access 'ops/accounts.py': No such file or directory
```

**The stack's largest loosening, and its unscheduled guard.** K_DSR was re-baselined ~156,500 → ~3,200 (`python -c "print(156500/3200)"` → `48.9`). It landed **pre-result** via the pre-committed superseding path, named itself in §6 Negative ("a genuinely **weaker** search-magnitude correction than originally committed"), ruled out the laundering alternative in §5 ("Lowering the DSR ≥ 0.95 threshold to compensate… Ruled out in §3"), and mandated bracket-reporting so "the discarded, larger number stays visible for review". Its §4 check rides an unscheduled vehicle.

**Scheduling failure is selective, not total:**

```
$ grep -ni 'programme audit' STATE.md
162:- Regime-monitor successor §6 gate ... re-raise as standing-unfalsifiable in that programme audit.
$ for s in 2026-06-22-cost-geometry-pregate 2026-07-11-discovery-campaign-defaults-ratified \
           2026-07-12-dsr-k-rule-and-variance-floor-supersession 2026-06-11-instrument-ledger-and-cfg-fingerprint; \
  do grep -c "$s" STATE.md; done
0
0
0
0
$ grep -rl 'Trigger check schedule.*2026-08-08' docs/adr/ | wc -l
30
```

Four named gate falsifiers (G3 cost-geometry, G6 campaign-defaults, the G2/G6 DSR-K supersession, G8 instrument-ledger) have no forward-board entry and ride a vehicle nothing schedules; several co-schedule "alongside the standing regime trigger", retired 2026-07-22. **Two are on the board under different labels** — the four-firms §4 progress check at 08-08 (which G1 operationalizes) and G9's Call-1 decay review at 08-08 — and G10's idle guard sits at 11-08.

**A falsifier that structurally cannot engage on the observed failure mode:** G10's §4 revert trigger contains, inside the trigger sentence itself, "*a gate-geometry failure per the HARV ADR §4 routes to that falsifier instead, not this one*". Both qualifying closures (D5, H-OD-1) were so classified, moving the count **1-of-2 → 0-of-2**; `STATE.md:161` records "doctrine count still open (0-of-2 counting)". A two-strike falsifier with a defect-routing exemption can absorb unbounded closures without reaching strike one. The re-classification was documented, dated and operator-signed — the defect is structural, not concealed.

**Counter-evidence, executed:** `core/lifecycle.py:180` carries an import-time `_validate_ladder` that raises "MVD spec drift… A change needs a fresh ADR + `strategy_lifecycle.md` update, not a code edit", plus a down-only [0.0, 1.0] check and a (2, 3, 0.50) beta-constant pin; the live sizing host (`ops/c1_sizing_host_reference.py:54,202-215`) imports `TIER_MULTIPLIER` and fails closed on a missing or unknown tier — "live sizing never defaults a tier". `prop_survivor_scoring.py:155-159` raises rather than guessing. The withdrawal ADR pre-names the exact degeneration move: "*Tempting because 4.74% 'only just' misses — that framing is the degeneration move this ADR exists to block.*"

---

# §4 — Verdicts

## §4.0 The operator's question, answered directly

**"Are the gates pertinent to the challenge at hand?"** Mostly yes — but pertinence is concentrated in **one** gate, and the measurement that gate depends on has decayed.

**Mis-aimed for a fixed-dollar trailing-drawdown evaluation** (in descending severity):

1. **G5's E3 is the only genuine mis-aim, and it is the sharpest defect in the audit.** E3 is the only rule anywhere in the stack that touches the trailing barrier. It is byte-identical to the v0.1 seed, was NOT among the E1/E2/E7 rows re-verified in the 2026-07-13 primary-source pass, and has never acquired a level — "Level is firm/tier-specific — treat as a parameter, not a constant", with its only design consequence being "report MFE/MAE-style excursion stats". Meanwhile the two most-elaborated rules in the artifact (E1 at four revisions, E2 at one relaxing revision) govern clock discipline and payout eligibility. The gate nominally responsible for the drawdown barrier has never been given a number.
2. **G2, G6, G7, G10 are denominated in demonstrability, not survival** — Sharpe floors, p-values, power, K budgets, per-trade cost hurdles. A Sharpe-denominated floor is by construction indifferent to loss-side shape, and trailing-DD survival is skew-governed. **This is correct scoping, not a defect**: each of these artifacts explicitly disclaims the survival question and routes it to G1 ("a screen FAIL is strong… a PASS never blesses"; "Discovery never blesses; the gate chain does"; §8e forbids using its own breadth diagnostic as a promotion signal). Anyone reading a G6 PASS or a G2 PASS as a survival claim is over-reading it — and ORB-MNQ's own Stage-6 RESULTS says so about its own PASS.
3. **G9's trigger is PF decay over review windows.** No mechanism in it fires on "this size is over the venue's drawdown limit", which is a static geometric fact available before any trade. The 2026-08-03 Proposed WATCH-1H rung is the first artifact in the gate's history that bends the ladder toward a drawdown-survival criterion, and it has to ADD a rung to do it.

**Load-bearing — do not weaken:**

1. **G1's Part A pair (bust ≤ 3.0% ∧ P(pass) ≥ 50%) on fixed-$ trailing geometry.** This is the only gate denominated in the operation's actual objective, it was independently stress-tested against a different objective that pointed **looser**, and retention was chosen with no edit. It has fired against the operation's own interest twice. Its thresholds are parsed out of a frozen document by a parser that raises rather than guessing, and that document is blob-identical to its single freeze commit after 21 days and five sessions of pressure.
2. **G2's Clause K.** It killed blind mining *before* the spend — precisely the class this operation has a documented graveyard for.
3. **G3's 4.0× cost hurdle.** The cheapest killer in the record: never moved across five modules in six weeks, re-ratified at the same value 2026-07-31 before any mechanism was scored, and three seeds died on it for $0.00 and K = 0.
4. **G6's DSR 0.95 / SPA 0.05 / PBO 0.5 / consistency 5/7.** The H-TSMOM-1 fork is direct evidence these do not bend: two of three readings kept the candidate alive, the operator pinned the strict one, and the campaign did not proceed.
5. **G9's ladder and its meta-lock.** Live-binding and fail-closed on the only execution surface, with an import-time hard-fail and §5's explicit anti-drift commitment ("Decay/kill thresholds are themselves LOCKED at authorization… This is the meta-lock").
6. **G8's Rule 10 read/append.** It protects the K denominator that makes G2 and G7 meaningful at all.

**The honest bottom line:** the stack is not mis-aimed at the objective — it is *layered*, with survival correctly housed in G1 and demonstrability upstream. What is wrong is narrower and more fixable: **G1's survival measurement runs on a clock the firm does not use, the constant it feeds is knowingly wrong in the optimistic direction and unrepaired in production, and the one envelope rule that should own the barrier has no number.**

## §4.1 Per-gate dispositions

| Gate | Verdict | Load-bearing reasoning |
|---|---|---|
| **G1** survivor-scoring | **Progressive** | §3.3: pre-registered an attack on its own load-bearing numbers with a strictly-prior freeze and reported the adverse reading, producing corroborated content §4 declined to predict. §3.6: retained 3.0% against an independent argument pointing looser. §3.7: blob-identical, parser refuses defaults, fired self-adversely twice. Defects (§3.1, §3.4, §3.6) are measurement-fidelity and freeze-hygiene, not criterion drift. |
| **G2** DSR floor / Clause K | **Stable** | §3.7 zero drift; Cap resolved at the tight end; DSR loosening explicitly forbidden; firewalled from G1. But §3.2 5/4/**0** removals, §3.3 no corroborated novel content (its sole PASS produced zero survivors), §3.6 the Cap comparison is unanswered, §3.4 the 48.9× K loosening's guard is unscheduled. |
| **G3** cost-law | **Stable** | §3.2 8 adds / 0 removals but 4.0 never moved in five modules and was re-ratified at the same value before scoring; §3.3 three seeds killed for $0.00 / K = 0; §3.5 the alleged boundary crossing is not one. Held back from Progressive by §3.6 (cheapest-firm default still executable and imported) and the unscheduled §4 check. |
| **G4** regime-robustness | **Degenerating** | §3.2: 6 adds, **every one an accommodation** (3 overrides, 1 demotion to non-blocking rider, 1 invented HALF_ONLY status, 1 scope carve-out); the single removal deletes an argument *for* running the gate. §3.4/§3.5: the 2026-08-02 narrowing has **no decision artifact** and landed one day before this audit under a `chore:` subject. §3.7: the 2026-05-23 override's sole named safety net was retired 2026-07-22 and nothing was re-armed; the library-graduation clause is unmet after ≥6 invocations, which cost M-23. Mitigating and recorded: the acceptance test is byte-identical to canonization, the gate is reachable and passing, every override preserved its dissent, and §3.6 shows the "blocking design would have won" counterfactual is **not** established. |
| **G5** prop_envelope | **Ambiguous** | §3.7 zero recorded NO verdicts in its entire history and several verdicts pre-declared "expected YES"; §3.1 the closure annotation was not written for the flagship campaign; §3.4/§3.5 its own change-control clause was breached; §3.7 its ratifying ADR's audit block raises `AttributeError`. Against that: the 90-day re-verify practice produced a genuine adverse self-correction, and the `cost_per_side_usd` guard test is mechanically enforced. Cannot distinguish "lax gate" from "candidate stream compliant by construction" on current evidence. |
| **G6** validation battery | **Stable** | §3.2 +108/−6 lines with every content add tightening and zero requirements deleted; §3.7 no threshold moved; the one ratified-default revision went through the pre-committed superseding path, loosened K while **tightening** V, retained DSR and forbade lowering it, and tested-and-discarded a more permissive draft. §3.3 no corroborated novel prediction (its self-test verifies implementation, not the world). §3.6 the biased `var_trials` default is disclosed but still live. |
| **G7** K accounting | **Ambiguous** | §3.2 +307/−1 with **zero** enforcement clauses ever deleted, and immutability/K≥1/alpha byte-unchanged — a very strong core. Against that, §3.4: two loosenings in six days, the first drafted and ratified the same night the campaign it was applied to was stopped and unpredicted by any prior artifact; §3.7: the three newest gates have bound zero campaigns and `--lane blind` bypasses them; §3.6: the comparison is currently unanswerable (8 days, no new manifests, freed seat unspent). |
| **G8** instrument-ledger bar | **Ambiguous** | The gate's own §4 ceremony-falsifier reads AMBIGUOUS on its own thin-sample clause, and §3.7 confirms zero recorded consults. Real dated kills exist at the prose layer (it bound a live scoping and named a procurement ruling), both §5 overrides are exemplary (§3.5), and the generated-view invariant is genuinely non-degenerate. But the mechanical layer has zero exposure, the gate deliberately does not parse verdicts, the class bar's last clearance is self-declared ("claimed, not adjudicated"), and §3.2 shows the one logged prune is +58/−0. |
| **G9** lifecycle | **Progressive** | §3.3: the only prediction in the stack anchored by a provably prior commit — an anticipated failure of its **own implementation** plus its remedy, pre-registered at ratification, tested against a band frozen before data, confirmed, remedy invoked, "No criterion moved after data". §3.7: every ratified value byte-identical with an import-time hard-fail; live-binding and fail-closed on the only execution surface. Defects are documentation (dangling `ops/accounts.py` at three sites) and an uncited governing ADR on an untracked draft. |
| **G10** harvest intake | **Stable** | §3.2 5/3/**0** but the two largest belt events (Requirement 5; the four-clause 1a) both **tighten**, and the one widening is zero-K and must still graduate through the unchanged five requirements. §3.7 zero drift; Clause K's cap pre-forbidden from loosening. §3.3 real economy improvement ($0.00 / K = 0 × 3). Held back by a §4 trigger that structurally cannot engage on the observed failure mode. |

## §4.2 Stack verdict — **STABLE**

Reasoning, tied to diagnostics:

- **Not Degenerating.** §3.7's executed checks found **zero numeric threshold drift** anywhere checked, across a window containing a self-adverse discharge withdrawal, a declined loosening (Q-BUSTGATE-1), a declined *tightening* on the audit date, a strict-reading pin that killed a live candidate, and three ADR-level forbidden-move lists that pre-name the exact degeneration move and were obeyed. §3.4 found no threshold moved to rescue a conclusion. The one gate that was quietly narrowed is named and carries follow-ups.
- **Not Progressive.** §3.3 yields exactly two clean predicted-and-corroborated episodes across ten gates in 89 days, and both are the stack predicting **its own** failure modes. No PASS the stack has emitted has survived downstream. §3.2 shows belt at 56 adds / 26 revisions / 7 removals (8:1), **zero genuine self-critical prunes**, four gates that have never removed anything, and the one event logged as a prune measuring +58/−0.
- **The real risk is not erosion, it is unexecuted self-review.** Four named gate falsifiers ride a vehicle nothing schedules (§3.7); three gates have zero exposure (§3.7); five instances of "winning theory documented, losing theory still executable" are live at HEAD (§3.6); the prereg-freeze guard is structurally blind to the pairs it most needs to see (§3.4). Every one of these is a maintenance failure, not a discipline failure — which is exactly the shape the audit lineage already documented: **the machinery reliably executes what it promises about the operation, and reliably does not execute what it promises about itself.**

---

# §5 — Follow-ups

## §5.1 Required — Degenerating verdict (G4)

| # | Action | Owner | Date |
|---|---|---|---|
| F1 | **Ratify or revert the 2026-08-02 scope narrowing.** Author an ADR (or an addendum to the 2026-08-02 prune brief) that records the ORB-MNQ/venue-native exemption, the LOCK-CANDIDATE conditioning, and the deleted cheapness rationale as a *decision* with grounds — or revert `cd8b617`'s three narrowings in `docs/methodology/regime_robustness_gate.md` lines 20-38. A methodology-doc scope change may not stand on a `chore:` commit with no artifact. | Operator (ruling) + CC (ADR) | **2026-08-08** |
| F2 | **Re-arm or formally release the 2026-05-23 override.** That ADR's §5 names the quarterly `time_to_pass.py --regime-check` as "the override's only retrospective safety net"; it was retired 2026-07-22 and nothing replaced it. Either register a successor check on the forward board or record explicitly that the allocation override now stands with no retrospective safety net. | Operator | **2026-08-08** |
| F3 | **Graduate the gate to a library.** The clause has been unmet through ≥6 invocations and the per-brief reimplementation habit produced M-23 (defective geometry scored through a process pool, optimistic, undetected four days). Land a single canonical implementation; delete the per-brief copies. | Cursor (frozen spec from CC) | **2026-09-01** |

## §5.2 Ambiguous — named re-test conditions and dates

**G5 prop_envelope — re-test 2026-11-08.** Measure three things: (a) any closure record carrying `DEPLOYABLE-DEFAULT-ENVELOPE: NO`; (b) any closure where the annotation was *computed at closure* rather than pre-declared in the pre-registration; (c) whether E3 has acquired a level, or an excursion-statistic requirement bound to the actual Tradeify eval barrier. **Verdict rule:** ≥1 NO **or** ≥1 closure-time-computed annotation ⇒ **Stable**. Zero of both AND E3 still level-less ⇒ **Falsified as a gate** — demote it in writing to a declaration checklist and stop calling it a gate.

**G7 K accounting — re-test 2026-11-08.** Measure: (a) has any manifest opened with `profile_cell` and `reachability_clauses` populated (i.e. the three 2026-07-26 gates have bound anything)? (b) has the ADR's own §4 falsifier been checked — any executed-K closure found to contain an un-enumerated read, which reverts all closures to declared-K retroactively? (c) how many of the MNQ/MYM Cap seats reopened by clause 2-C were spent, and on what. **Verdict rule:** ≥1 gated open with clauses recorded AND no §4 violation ⇒ **Stable**. Zero gated opens by 11-08 ⇒ the three 2026-07-26 gates are ceremony; strike them or re-point them, and set `--lane` to have no default.

**G8 instrument-ledger bar — re-test 2026-11-08** (the gate's own second-cycle date). Its own §4: FALSIFIED if no pre-registration has recorded a profile consult that altered its scoping, or if the vocabulary check obstructs a legitimate mechanism; RESOLVED if ≥1 candidate was redirected or re-scoped by a consult; <2 scoped candidates ⇒ AMBIGUOUS, carry unchanged. **Adopt that rule as written** — do not substitute a softer one. Add one measurement it does not currently make: whether any `bars:`-bound cell was opened anyway.

## §5.3 Repairs — "winning theory documented, losing theory still executable"

These are the five live instances from §3.6 plus the two dead hooks from §3.7. All are mechanical.

| # | Repair | Owner | Date |
|---|---|---|---|
| R1 | **Correct `dd_lock_offset_usd` in `core/firm_rules.py`** for all six `trailing_locking` eval tiers, retire the ten per-run monkeypatches, and annotate every published Part A figure produced under the old value. The defect is disclosed, measured, optimistic in direction, and twelve days old. | Cursor (frozen spec) | **2026-08-08** · ✔ source fix 2026-08-04; monkeypatch restore-to-100 hygiene + orientation lower-bound labels 2026-08-07 ([`W1 ADR`](../../../adr/2026-08-07-w1-intraday-honest-engine-remeasure.md)); **RESULTS re-run still owed** |
| R2 | **Thread `intraday_low` through `lab/discovery/prop_survivor_scoring.py`**, or — if that is deferred — annotate every G1 Part A output as a lower bound, starting with the two 50K figures currently defeating the 11-08 demotion clause. Also correct the frozen §3 "engine-faithful geometry" label's reading via an addendum note (the prereg itself stays blob-frozen; record the correction where it is *read*). | CC (spec) + operator (label ruling) | **2026-08-08** · ✔ lower-bound annotations 2026-08-07 (W1); threading + RESULTS still owed |
| R3 | **Fix `ops/sentinel/scan.py::_corresponds`** so a pre-registration in `docs/briefs/pre-registration/` can pair with a `lab/analysis/*/RESULTS*.md`. Today no such pair can ever fire; 25 of 47 preregs carry no Q-ID, and at least three G1-family freezes went unflagged. | Cursor | **2026-08-08** · 2026-08-07 W4: absorbed-or-redated pointer under closed-loop PREREG discipline ([`W4 ADR`](../../../adr/2026-08-07-w4-minimal-gate-set-dormancy.md)); sentinel code repair may still stand · **DONE 2026-08-15** (body Q-ID + RESULTS-cites-prereg) |
| R4 | **Update `floor_scan.py:85-89`** to the operator-pinned strict reading (c) for H-TSMOM-1 so the harness stops printing a superseded PASS its own scoping brief names as a forbidden citation. | Cursor | **2026-08-08** · **DONE 2026-08-15** (living harness; RESULTS.md snapshot unedited) |
| R5 | **Make `var_trials` default to `1/n`** in `lab/research_utils/universe_gate.py:369-370`, or hard-fail when it is omitted. The empirical default is vacuous at `K_SPA = 1`, which the ADR itself calls the plausible outcome of the cost-law hurdle. | Cursor | **2026-09-01** · 2026-08-07 W4: absorbed as standing caveat (pass V explicitly); **schedule 09-01 left standing** for module-default flip · **DONE 2026-08-15** (default flipped; self-tests rewritten) |
| R6 | **Retire `DEFAULT_FIRM_KEY` from `lab/discovery/cost_mnq.py`** (or route its two live importers to `cost_model.resolve_commission`), so the cheapest-firm default cannot be inherited silently. | Cursor | **2026-09-01** · 2026-08-07 W4: schedule left standing (not discharged by dormancy) · **DONE 2026-08-15** (`firm_key` required) |
| R7 | **Repair `strategy_lifecycle.md` lines 52 / 60 / 113** — the canonical owner still routes G9's only fired contingency to code deleted 2026-07-24. Record what actually realizes the WATCH haircut today (`ops/c1_sizing_host_reference.py` importing `TIER_MULTIPLIER`). | CC | **2026-08-08** |
| R8 | **Sweep the remaining two Rule-11 targets** — `2026-07-13-prop-envelope-v1-ratification.md:88` (raises `AttributeError`) and `2026-07-23-c1-rung-selection-ev-objective.md:129` — and re-state both existing repair records against the Phase-**4** deletion rather than the Phase-1 state. | CC | **2026-08-08** |
| R9 | **Schedule the four stranded §4 falsifier checks** (cost-geometry, campaign-defaults, DSR-K supersession, instrument-ledger) on the STATE.md forward board, and schedule the meta-layer programme audit they all ride. 30 ADRs name 2026-08-08 as a trigger date against a vehicle nothing books. | Operator | **2026-08-08** |
| R10 | **Add a second, engageable limb to G10's §4 doctrine trigger** covering the observed failure mode (closures dying at cost-law or power with the mechanism confirmed). The existing limb routes gate-geometry failures away and currently reads 0-of-2 after five-plus dead campaigns. | CC (spec) + operator (ratify) | **2026-11-08** · **ACCEPTED 2026-08-15** (operator GO). Pin marked `no` 2026-08-15; post-mark count 0/2 — not fired. Limb 1 unedited |
| R11 | **Cite the governing ADR in the WATCH-1H draft.** `docs/adr/2026-08-03-lifecycle-ladder-intermediate-rung.md` applies the selection rule ratified by `2026-07-23-c1-rung-selection-ev-objective.md` without citing it, and does not present the both-halves regime PASS that ADR makes a hard admissibility precondition. Untracked and `Proposed` — fix before it merges. | CC | before merge |

## §5.4 What this audit cannot establish, and what would settle it

1. **Whether G5 is lax or the candidate stream is compliant by construction.** Zero NO verdicts in the gate's entire life is equally consistent with both. *Settled by:* deliberately scoring one known-non-compliant candidate (e.g. an overnight-hold construct) through the envelope and observing whether a NO is produced and recorded. Cheap; can be run before 2026-11-08.
2. **Whether G7's executed-K convention is principled or convenient.** The comparison is unanswerable at 8 days with zero new manifests. *Settled by:* the next two campaign opens under the new gates, plus one adversarial audit of the ST-EH-1 closure against §2-C's four conditions (zero results artifacts, git-auditable non-occurrence, enumerated looks and examiners, operator signature).
3. **Whether G2's Cap = 1.0 was the right choice.** DISC-CAMP-0 is excluded under both caps and predates the resolution, so nothing in the record discriminates. *Settled by:* a campaign whose axis sits in the [1.0, 2.0] band — D6 (1.835) or D2-low (1.925) — being funded and closed on some other authority, which would price the counterfactual directly. No such campaign is planned, so this may remain permanently open, and that is worth recording rather than papering over.
4. **Whether the intraday clock changes any historical G1 verdict.** The engine gained the capability after the §4 discharge, the withdrawal and the band re-score were computed. *Settled by:* re-running the four decisions of record (07-15 discharge, 07-22 withdrawal, 07-24 band re-score, 08-02 realizable book) with `intraday_low` threaded and the corrected `dd_lock_offset_usd`, and publishing the deltas. This is the single highest-value measurement available to the operation right now, and it is cheap.
5. **Whether the class bar's route-1 clearance on M2K is sound.** The ledger itself records it as "claimed, not adjudicated". *Settled by:* an adjudication, or by striking the clearance and leaving the cell bar-bound.
6. **Whether the belt would prune under pressure.** The window contains zero genuine self-critical prunes, but it also contains no event that forced one — the stack was in build-out for two of its four months. *Settled by:* the next gate whose falsifier fires against it. Until then, "never prunes" and "never had to prune" are observationally identical, and this audit cannot separate them.

**Not establishable in principle by this audit:** whether the gate stack, correctly aimed and correctly measured, would produce a candidate that passes a Tradeify evaluation. That is an object-layer question. This audit's jurisdiction ends at whether the gates are aimed at it, measured honestly, and held at their stated thresholds — and on those three questions the answers are: **mostly yes** (one genuine mis-aim, G5's E3), **not yet** (the barrier clock and the lock constant), and **yes, without exception found**.