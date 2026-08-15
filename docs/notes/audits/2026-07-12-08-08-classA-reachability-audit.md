# Audit — gate reachability of the ratified 08-08 Class-A slate

**Date:** 2026-07-12
**Scope:** the five Class-A items in [`docs/briefs/2026-07-12-08-08-packet-pretriage.md`](../../briefs/2026-07-12-08-08-packet-pretriage.md) §2 (operator-ratified, §2.6). This note grades **reachability** — does a real harness + real inputs exist to decide each item as scoped — per the mandatory gate-reachability rule established by [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](../../adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) (lesson lineage: Q-HARV-0's structurally un-passable placebo clause; DISC-CAMP-0's unreachable DSR K-rule).
**No-cascade:** classification is frozen (pre-triage §3.1/§4); this note re-classifies nothing, fixes nothing, pulls no data, authors no ADR.
**Worktree:** `claude/class-a-gate-reachability-audit-cd2889` @ `4d05a63` (= `origin/main` tip at audit time; verified clean, no divergence).
**Concurrency:** no path under `lab/discovery/**`, `.claude/skills/futures-anomaly-discovery/**`, `discovery-campaign-template.md`, `DISC-CAMP-0-preregistration.md`, or `STATE.md` touched by this audit.

---

## §0.5 Response — clarifying questions, resolved from source

**(A) Panel definition for A5 — trailing-6-month coverage.** The four legs have been off-venue since 2026-06-30 (no live fills), so the "trailing 6 months" for the §4 limb-2 trigger can only be a **backtest re-export**, not live data. Newest **committed/manifested** (`core/data/tv_exports/pepperstone/SHA256SUMS`) export per strategy: Guardian `2026-06-25`, Aegis `2026-06-26`, NAS100 `2026-06-26`, DJ30 `2026-07-08` (newest of the four). **None reach 2026-08-08**, and three of four are ~6 weeks short of it. **A fresh 4-strategy operator TV/Pepperstone export is needed** to bring the panel current enough to be a genuine "trailing 6 months as of the 08-08 review" — this is a top-line finding, not a footnote (folded into the A5 grade below).

**(B) Panel restorability.** Two distinct restore questions, kept separate per the handoff's instruction:
- The **existing** decompound-vintage inputs (2026-06-07 stitched vintage read by `regime_gate.py`/`h1_check.py`; 2026-06-25 clean vintage read by `remc_cleanvintage.py`) are **absent in this worktree** — `lab/analysis/regime/decompound_remc_2026-06-07/inputs/` contains only `README.md`. Per Rule 9's *principle* (gitignored data does not propagate across worktrees — see the Rule-9 scope note below), this is a **cheap local copy** from the operator's primary checkout (CLAUDE.md: "Locally Joshua has both sets"), not a fresh pull. It is a restore, not a procurement.
- A **trailing-window-through-08-08** panel does not exist **at all**, restored or not (§A) — no restore closes that gap; only a fresh export does.
- **Rule-9 scope note (precision, not a nitpick):** `docs/operational_rules.md` Rule 9 is titled "Pine-dependent work in a git worktree requires a Pine sync pre-flight" and is written specifically about `**/*.pine` files (verbatim below). Q-DECAY-1/Q-PERSIST-1's closures — and this handoff — invoke "Rule 9" for absent **vendor-CSV** panels by analogy to its gitignored-data-doesn't-cross-worktrees principle, not its literal Pine scope. The analogy is sound (same mechanism: `.gitignore` + `git worktree add`), but it is an analogy, not the rule's literal subject — flagged here so the citation isn't mistaken for a second, CSV-specific rule that doesn't exist.

**(C) Scope boundary.** Understood and honored: every non-REACHABLE finding below is a finding + an owed fix, never a reclassification. No Class-A item is moved to B/C; no item is resolved early; A2's own scope ("decidable-to-OPEN only") is graded as literally written, not second-guessed.

---

## Rule 9 (verbatim, `docs/operational_rules.md`)

> ## 9. Pine-dependent work in a git worktree requires a Pine sync pre-flight
>
> `**/*.pine` is gitignored (the live edge is held privately — CLAUDE.md "Public-clone posture"). Gitignored files are **not** shared across git worktrees: the locked `.pine` live only in the primary checkout. Any worktree from `git worktree add` starts with `core/strategies/*/*.pine` **absent**, which silently blocks every Pine-dependent task — codification / scaffold extraction, any decision-brief §0 that reads `*.pine`, and `scripts/validate_params.py`'s Pine-default cross-check (which no-ops to WARN when Pine is missing, so the gap is invisible).
>
> **Procedure (run at the start of any Pine-dependent task):**
> 1. **Pre-flight gate.** `python scripts/sync_pine_to_worktree.py --check` — exit 0 if the locked Pine is present in the current tree, exit 1 if you are in a worktree without it.
> 2. **Remedy.** `python scripts/sync_pine_to_worktree.py [--verify]` copies the locked `.pine` from the auto-detected primary worktree into the current worktree.
> 3. **Fallback** when no local checkout has the Pine at all: use the brief-authoring §0 citation-chain sub-rule.

(As noted in §0.5(B), the two 2026-07-10 closures apply this rule's *principle* to gitignored vendor CSVs, not its literal Pine subject.)

---

## Grade summary

| Item | Grade | One-line why |
|---|---|---|
| **A1** — Accept-beta fork | **REACHABLE** | Pure synthesis of two CLOSED analyses; both name 08-08 as their consumer; no computation needed. |
| **A2** — D2 scope-to-OPEN | **REACHABLE** (as literally scoped) | The 08-08 ask is "frame D2," not "resolve D2" — resolution is explicitly forbidden before the 11-08 Pre-Q. Scoping inputs all exist. |
| **A3** — Lifecycle Call 1 | **DATA-BLOCKED** (expected/self-declared) | Two of three `decay_breach()` inputs (`rolling_pf`, `pf_sigma`) do not exist anywhere in the repo. Matches the ADR's own pre-declared AMBIGUOUS clause. |
| **A3** — Lifecycle Call 4 | **VACUOUS-BY-CONSTRUCTION** (verified by execution) | Ran `beta_death_assessment` live in this worktree: `watch_count=0`, no crash. The null is genuinely recordable, not just plausible. |
| **A4** — Q-HARV-0 fork | **REACHABLE** | Closure + RESULTS.md exist and carry the exact adjudication inputs; a qualitative fork, no code run. |
| **A5** — Decompound-HOLD §4 limb-2 | **HARNESS-MISSING**, compounded by **DATA-BLOCKED** | No existing script evaluates "LOCKED config, trailing-6-month window, p99≥5%/bust≥1%" as literally specified — confirmed by reading all three candidate scripts. The panel to run it on doesn't exist either (§0.5-A). **This is the load-bearing finding.** |

**H (§4 of the handoff) is CONFIRMED**: A5 is not reachable as scoped; A3-Call-1 is data-blocked (but that is the pre-triage's own expectation, so it does not add to the confirmation — only A5 does).

---

## A1 — Accept-beta fork (Q-DECAY-1 cost × Q-PERSIST-1 probability)

**Criterion (pre-triage, verbatim):** *"Both paired closures route here; the decompound HOLD has ridden two quarters — a third park is the 'HOLD dying quietly' the R6 ADR forbids... Fully decidable — a synthesis of two closed analyses; no live data required."*

**Harness:** none required — this is a synthesis, not a computation.

**Inputs and their state:**
- [`docs/briefs/Q-DECAY-1-closure-scope-split.md`](../../briefs/Q-DECAY-1-closure-scope-split.md) — Status: `CLOSED — SCOPE-SPLIT`. Its own **Re-check hook** (line 48-50): *"2026-08-08 quarterly regime check: feed this closure into the accept-beta fork as the 'does accepting a shared-mechanism family come with common-mode blindness, and at what drawdown cost' input. Answer: yes — common-mode is UNCOVERED; the cost is a bust-line drawdown before any signal."* Cost figure (line 20): common-mode earliest signal arrives only after **median max DD ~11.7%** — past the 5% firm bust line.
- [`docs/briefs/Q-PERSIST-1-closure-moot.md`](../../briefs/Q-PERSIST-1-closure-moot.md) — Status: `CLOSED at §2.1 — MOOT / ALREADY-ANSWERED`. Its own **Re-check hook** (line 52-53): *"2026-08-08 quarterly regime check: pair with Q-DECAY-1... the MC understates how likely that tail is — directionally yes, by +0.46pp on the tail-relevant decompounded panel, bounded-small and feasibility-unmeasured on the locked 2022-26 anchor."*

Both artifacts exist, are readable, and their own text names the 08-08 accept-beta fork as consumer — the pre-triage's "evidence to pre-assemble" line for A1 is a verbatim match to what these two closures actually say. Both closures' underlying computations were feasibility-limited by an absent panel (Rule 9-by-analogy, §0.5-B) — but that limited the *original* analyses, not this synthesis: A1 re-runs nothing, it reads two already-published verdicts.

**Grade: REACHABLE.** No fix owed.

---

## A2 — D2: `dd_protection` objective re-derivation (scope-to-OPEN only)

**Criterion (pre-triage, verbatim):** *"Decidable-to-OPEN only. Scope/frame D2 at 08-08; resolution is gated on the 11-08 successor Pre-Q (numbers-before-question forbidden). Constants stay frozen until then."*

**Governing constraint** — [`docs/adr/2026-07-11-challenge-era-claims-rescope.md`](../../adr/2026-07-11-challenge-era-claims-rescope.md) §5 forbidden moves (verbatim): *"Running successor-semantics MC numbers before the D1 Pre-Q freeze. Numbers-before-question is the family's own pre-registration violation; the first self-funded MC result must land against a frozen question set."* Its §4 completion falsifier (line 72) hard-dates the successor Pre-Q (D1, which feeds D2) to **2026-11-08**.

The companion audit note ([`docs/notes/audits/programme-audit/2026-07-11-core-fxify-anchoring-audit.md`](programme-audit/2026-07-11-core-fxify-anchoring-audit.md) line 70) names D2's scoping inputs directly: *"D2 | dd_protection objective re-derivation (no pass-time term). | Inputs carry over: Q-DDTRIG-1 (1.0% passes §4, fails regime gate → HOLD), Q-DDP-1 sweep, regime-robustness gate. Operator decision at 08-08; any constant change stays re-MC + ADR-gated."*

**Inputs and their state:**
- `docs/ltm/briefs/Q-DDTRIG-1-closure-hold.md` — tracked, readable.
- Q-DDP-1 sweep recommendation — **evicted from disk 2026-06-05** (pruned); retrievable verbatim via `git show pre-prune-2026-06-05:archive/docs/briefs/Q-DDP-1/recommendation.md` — **verified this session** (command returns the document). A minor friction (one of three inputs needs a historical git-show, not a direct file open) but not a blocker.
- `docs/methodology/regime_robustness_gate.md` — tracked, readable.

**What is and is not being graded:** the criterion asked of A2 at 08-08 is explicitly *"scope, not resolve"* — the ADR itself forbids producing successor-semantics numbers before 11-08. So "is A2 reachable" means "can D2 be **framed** at 08-08 from existing closed inputs," not "can the dd_protection question be **answered** at 08-08" (it structurally cannot be, by design, and that is not a defect). All three scoping inputs exist and are readable (one via a documented historical-retrieval command).

**Grade: REACHABLE** (as literally scoped — framing only). Full resolution is out of scope by the ADR's own forbidden-move clause, not a reachability gap.

---

## A3 — Lifecycle Calls 1 & 4 first evaluation

### Call 1 (decay-detection threshold)

**Criterion** ([`docs/methodology/strategy_lifecycle.md`](../../methodology/strategy_lifecycle.md) Call 1, line 35): *"rolling live PF below [baseline PF − 1.0σ of the MC PF distribution] for 2 consecutive review windows → demote one tier."* Code signature ([`core/lifecycle.py`](../../../core/lifecycle.py):139-146): `decay_breach(rolling_pf, baseline_pf, pf_sigma, k_sigma=1.0)` — **three** required inputs.

**Input state, checked individually:**
1. `rolling_pf` (live PF) — **does not exist**. All four legs have been off-venue since 2026-06-30; zero fills accrue anywhere.
2. `baseline_pf` — **exists**. [`.claude/skills/trade-csv-reconcile/references/baselines.md`](../../../.claude/skills/trade-csv-reconcile/references/baselines.md) carries multiple per-strategy PF point estimates across CSV vintages (e.g. Guardian PF 3.750/3.7717/3.5327 across snapshots).
3. `pf_sigma` — **does not exist anywhere in the repo.** A full-file grep of `baselines.md` for `sigma|σ|std` returns zero hits; `strategy_lifecycle.md`'s own Implementation status (line 115) confirms: *"Pending — data-dependent Phase 2 code: (a) Call-1 σ-source + harness (reads baselines.md + a live-PF source; applies decay_breach/autonomous_demote; writes demotions into lifecycle_state.json) — σ-source design in flight."*

This is **not** merely "the live count is short" (a soft AMBIGUOUS) — the σ input has never been computed or published at all, independent of the live-fills problem. The ADR/lifecycle doc's own text pre-declares the outcome (line 37): *"these floors are pre-registration against future data, not live-evaluable at 2026-08-08 — the ADR §6 AMBIGUOUS clause governs, re-confirm at 2026-11-08 if the count is short."*

**Grade: DATA-BLOCKED**, but **expected/self-declared** by the governing lifecycle doc — this confirms the pre-triage's own prediction rather than surfacing a surprise, so it does not independently confirm H (§4). Cross-reference: this is the **same undelivered artifact** as the pre-triage's C3 note on the T4 rolling-PF σ-harness ("one item, two homes").

### Call 4 (beta-death portfolio trigger)

**Criterion** (strategy_lifecycle.md Call 4, line 79-80): soft flag at ≥2/4 legs in WATCH; beta-death (portfolio-wide 0.50× de-risk + mandatory operator GO/NO-GO) at ≥3/4.

**Verified by direct execution** (not inference) in this worktree:
```
$ py -3 -c "import sys; sys.path.insert(0,'core'); import lifecycle as L; \
  m = L.get_lifecycle_multipliers(L.STRATEGY_KEYS); print(m); print(L.beta_death_assessment(m))"
multipliers: {'Guardian': 1.0, 'Striker NAS100': 1.0, 'Aegis': 1.0, 'Striker': 1.0}
beta_death_assessment: {'n_legs': 4, 'watch_count': 0, 'soft_flag': False, 'beta_death': False,
                          'portfolio_multiplier': 1.0, 'operator_go_nogo': False}
```
`lifecycle_state.json` is absent (gitignored, no strategy ever demoted); `load_lifecycle_state()` ([`core/lifecycle.py`](../../../core/lifecycle.py):58-73) returns `{}` on a missing file rather than erroring, and `DEFAULT_TIER = "AUTHORIZED"` (line 39) makes every unlisted strategy default to 1.0×. The code path runs clean to a `watch_count=0` result — no exception, no manual data assembly.

**Grade: VACUOUS-BY-CONSTRUCTION** — and confirmed **recordable**, not merely inferred-vacuous: the CLI-equivalent call actually executes and emits the null cleanly. This is exactly the pre-triage's own expected outcome for A3/Call 4 ("record the null explicitly") — it does not confirm H.

---

## A4 — Q-HARV-0 buy-positioning-data fork

**Criterion (pre-triage, verbatim):** *"The AMBIGUOUS close (+19.2 bp, p=0.013, placebo clause proven structurally un-passable) upgrades the fork to 'flow data adjudicates crowded-expression vs mechanism-death, which price data cannot' — a data-procurement decision... Decidable — a qualitative adjudication fed at 08-08, no code run."*

**Evidence, verified:**
- [`docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md`](../../briefs/closures/Q-HARV-0-month-end-rebalance-ES.md) — Verdict: **AMBIGUOUS**. Verbatim: *"the sign-aligned conditional fade of the intra-month ES-vs-ZN outperformer over T-3→T-1 is +19.21 bp, permutation p=0.0129... clearing the 4× cost hurdle... But it is not RESOLVED."* Placebo trigger, verbatim: *"the placebo magnitude clause was structurally un-passable at registration — the primary would have needed to be ~60–80 bp (no calendar effect is that large) for RESOLVED to be reachable."*
- [`lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md`](../../../lab/archive/harv_0_month_end_rebalance_es_2026-07/RESULTS.md) — tracked, exists (full backing detail for the closure summary above).

The fork itself ("flow data would adjudicate crowded-expression vs mechanism-death, which price data structurally cannot, given the placebo geometry") is answerable directly from these two documents — a purchase-decision adjudication, not a computation. No live data pull is implied by *grading* this reachable; the decision itself (whether to actually buy flow data) remains the operator's 08-08 call.

**Grade: REACHABLE.** No fix owed.

---

## A5 — Decompound-HOLD §4 limb-2 regime re-MC (highest-stakes item)

**Criterion, verbatim** ([`docs/adr/2026-06-07-decompound-remc-hold.md`](../../adr/2026-06-07-decompound-remc-hold.md) §4, line 66): *"a quarterly regime-check finds the trailing-6-month panel resembles H1 — re-run `regime_gate.py` on the trailing 6-month window at the locked config and observe **p99 DD ≥ 5% OR bust ≥ 1%**."* Revert action on breach: open a regime-adaptive-sizing Pre-Q **+ apply a k≈0.55 haircut on all four allocations operationally** — a live allocation event.

**The ADR's own audit hook already hedges this** (§10, line 125-127): *"python lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py 100 — Expected at HOLD: both candidates still GATE FAIL... (**the trigger fires if a TRAILING-6mo window, substituted into the harness, clears/breaches**)."* "Substituted into the harness" is the tell the parent handoff flagged — it anticipates a manual code change at decision time, which is exactly the un-pre-registered-edit-at-decision-time hazard the gate-reachability rule exists to prevent (same class as DISC-CAMP-0's K-rule and Q-HARV-0's placebo clause).

**Read the actual source of every candidate harness, not the ADR's prose about it:**

1. **`lab/analysis/regime/decompound_remc_2026-06-07/regime_gate.py`** (the named script, read in full):
   - `N_PANELS = int(sys.argv[1])` (line 45) is the **bootstrap panel count**; there is no window-slicing / date-cutoff parameter anywhere in the file.
   - `CANDIDATES = [("C1 k=0.55", {...LOCKED*0.55}, 0.015, 0.40), ("C2 DDscale0.20", dict(LOCKED), 0.015, 0.20)]` (lines 48-51) — **both entries are the two REJECTED de-risk alternatives.** Neither entry is the actual production config (LOCKED allocations, `DD_TRIGGER=0.015`, `DD_SCALE=0.40`, unmodified). There is no "run the locked config" candidate in this file at all.
   - It runs against `_STATIC` (line 40), the **full 2020-2026 decompounded static panel** — a fixed historical block-bootstrap + H1/H2 half-split, not a "trailing 6 months as of now" slice.
   - **Conclusion: this script cannot evaluate "the locked config, trailing 6 months" without two separate code additions** — (a) window-slicing logic, (b) a LOCKED candidate tuple. Neither exists.

2. **`lab/analysis/regime/decompound_remc_2026-06-07/h1_check.py`** (sibling, read in full) — `CONFIGS` (lines 51-60) sweeps deep de-risk levels (k=0.55 down to k=0.20, plus DD-trigger variants); again **no unmodified-LOCKED entry**, and its window is a fixed `panel.index < mid` split of the full historical panel (line 41-42) — the older calendar half, not a trailing window ending near a review date.

3. **`lab/analysis/regime/decompound_remc_2026-06-07/remc_cleanvintage.py`** (sibling, clean 2026-06-25 vintage, read in full) — `half_panels()` (line 120) **does** include `("LOCKED k=1.0", LOCKED, 0.015, 0.40)` — this is where the ADR's own Addendum figure (locked-config H1 bust 13.84% / p99 7.76%, `RESULTS_cleanvintage_2026-06-25.md` line 36) actually came from. But: (i) its split is still the fixed historical H1(older-half)/H2(newer-half) of the full 2020-2026 panel, **not** a trailing-6-month window ending near 2026-08-08; (ii) its `main()` hard-requires local CSVs under `inputs/` (line 174-176: `missing = [f for f in NEW_FILES.values() if not (_INPUTS / f).exists()]; if missing: sys.exit(...)`) — those files are **absent in this worktree** (only `README.md` present, and that README documents the *older* 2026-06-07 stitched-vintage filenames, not the 2026-06-25 `NEW_FILES` this script actually needs — a secondary, minor doc-staleness finding, not separately actioned here).

4. **`lab/analysis/time_to_pass.py --regime-check`** (the **C1** harness — confirmed a genuinely distinct code path, per the pre-triage's "do not conflate" instruction): `regime_check()` (lines 146-224) **does** implement proper trailing-window slicing — `mid = end - pd.DateOffset(months=WINDOW_MONTHS)` (line 166), `WINDOW_MONTHS=6` (line 45) — proving the "trailing N months ending at panel-max-date" concept is implementable in this codebase. But it evaluates **pass_rate < 95%** on the **live-extended compounded** Pepperstone panel via `portfolio_mc`'s own pass/bust semantics — a structurally different metric (pass-rate, not p99 DD/bust-rate against the HOLD's 5%/1% floor) and a different panel basis (compounded, not the HOLD's decompounded-static framework). Confirming the windowing *pattern* exists elsewhere sharpens, rather than closes, the A5 gap: the pieces to build a correct trailing-window LOCKED-config regime_gate exist scattered across three files, but none of them is assembled, and assembling them at decision time is precisely the hazard flagged above.

**Data layer, independently of the harness gap** (§0.5-A): even a fixed harness has nothing current to run against. Newest committed export per strategy (`core/data/tv_exports/pepperstone/SHA256SUMS`): Guardian `2026-06-25`, Aegis `2026-06-26`, NAS100 `2026-06-26`, DJ30 `2026-07-08`. None reach 2026-08-08; three of four sit roughly 6 weeks short.

**Grade: HARNESS-MISSING** (as literally scoped — no existing script evaluates the named criterion on the named config/window without a code change), **compounded by DATA-BLOCKED** (the trailing-6-month-through-08-08 panel does not exist yet, restored or not). This is not an inference from the ADR's hedge language alone — it is confirmed by reading all three candidate scripts' actual `CANDIDATES`/`CONFIGS` lists and windowing logic.

**Fix owed (see table below for owners/lead times):**
1. A small, **pre-registered** harness extension (new sibling script or an explicit patch to `regime_gate.py`) that (a) accepts a trailing-window cutoff, (b) evaluates the unmodified LOCKED config as its own candidate. Per Rule 8 sub-rule 7 (pre-registration must be a separate, earlier commit than the run), this must land as a frozen commit **before** the 08-08 run, not authored same-day at the gate — writing the window logic live at the review is exactly the researcher-degrees-of-freedom hazard this audit exists to catch.
2. A fresh 4-strategy Pepperstone TV export extending coverage through ~2026-08-08, followed by `scripts/check_data_manifests.py --regenerate` and a committed `SHA256SUMS` delta.
3. (Lower priority, cheap) a local restore of the existing decompound-vintage inputs into any worktree that needs to reproduce the *historical* H1/H2 finding — a copy from the operator's primary checkout, not a new pull.

---

## §ε — grounding basis note (Pass 2 self-check)

Every grade above rests on a quoted line from the actual source file or brief — the pre-triage's classification text, the ADR's §4/§10 lines, the three regime-gate-family scripts' `CANDIDATES`/`CONFIGS`/window-slicing code, `core/lifecycle.py`'s function signatures (plus a live execution of `beta_death_assessment`), `strategy_lifecycle.md`'s Implementation-status line, a full-file grep of `baselines.md`, and the HARV-0 closure's own verdict text. The A5 grade in particular does **not** rest on the ADR's "substituted into the harness" prose alone — that phrase is corroborated, not merely repeated, by independently reading all three candidate scripts and confirming none of them assembles the criterion as specified.

---

## §Owed-before-08-08 table (ordered by lead time, longest first)

| # | Owed fix | Owner | Lead time | Consequence if it slips |
|---|---|---|---|---|
| 1 | **A5 harness** — pre-registered trailing-window + LOCKED-candidate extension to the regime-gate family (new sibling script or patch, frozen commit ahead of the run) | CC (build) + operator (review/ratify pre-reg) | **Longest — must start now.** Needs its own reviewed pre-registration commit *before* the 08-08 run per Rule 8 sub-rule 7; writing it same-day is the exact hazard this audit exists to prevent. | A5 either doesn't run at all, or runs against an un-pre-registered same-day code edit — the highest-stakes item on the slate (a live 55% allocation haircut) decided on the weakest evidentiary footing. |
| 2 | **A5 data** — fresh 4-strategy Pepperstone TV export extending through ~2026-08-08 | Operator (requires an active TV/Pepperstone session) | **One operator session**, but must be scheduled with enough notice before 08-08 that CC can wire the harness (item 1) against real files and sanity-check it pre-review. Roughly 4 operator weekends remain before 08-08 — this should not be the last one. | Item 1's harness has nothing current to run against; A5 falls back to the stale (04-26/06-25/06-26) window, which is not "trailing 6 months as of the review." |
| 3 | **A3/Call-1 pf_sigma source design** ("σ-source design in flight," `strategy_lifecycle.md` line 115 — same undelivered artifact as the pre-triage's C3 T4-rolling-PF-σ-harness note) | Operator + Cursor (per Q-DECAY-1's "output for the operator + Cursor" framing) | Not required for 08-08 — DATA-BLOCKED is the expected, pre-declared outcome there. Owed toward the 11-08 re-confirm. | If undelivered by 11-08, Call-1 re-confirms AMBIGUOUS again with no new information — a second quiet park of the same gap. |
| 4 | **Local restore of existing decompound-vintage inputs** (`lab/analysis/regime/decompound_remc_2026-06-07/inputs/*.csv`, both the 2026-06-07 stitched and 2026-06-25 clean vintages) into any worktree reproducing the *historical* H1/H2 finding | Operator (cheap copy from primary checkout) | Trivial — only blocks reproduction in a fresh worktree, not the operator's primary environment where these files already exist. | Cosmetic only; does not block 08-08 if item 1's dev happens in the primary checkout. |

No item above re-classifies a Class-A slate entry; every row is a fix owed against a grade already assigned above, and every non-REACHABLE grade above has exactly one row here (bidirectional check: 4 non-REACHABLE findings — A5 harness, A5 data, A3-Call1 data, A5 local-restore residual — 4 rows).

---

## Closure

- **H (§4 of the handoff):** **CONFIRMED** — A5 is not reachable as scoped (HARNESS-MISSING + DATA-BLOCKED). A3-Call-1's DATA-BLOCKED grade matches the governing ADR's own pre-declared expectation and does not independently add to the confirmation; A1/A2/A4 grade REACHABLE; A3-Call-4 grades VACUOUS-BY-CONSTRUCTION as expected.
- No Cursor-owned path touched. No classification changed. No fix applied. No data pulled. No ADR authored. This file is the sole write.
