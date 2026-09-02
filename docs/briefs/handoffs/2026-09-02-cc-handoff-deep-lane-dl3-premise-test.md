# CC Handoff — DL-3: first real test of the deep-iteration premise

**Date:** 2026-09-02
**Parent session:** Claude Code (Fable 5.1) — GROW framework status review, 2026-09-02
**Spawn target:** Claude Code (Analyst + Tactical Ops). Not Cursor — family selection and prereg authoring are judgment work on a locked doctrine surface.
**Repo:** `first-passage` — **start from a fresh branch off `origin/main` (fetch first).** Do not reuse any existing worktree; the parent session's checkout is ~700 commits stale.
**Brief type:** CC handoff (multi-step, gated). This session's deliverable is **Phases 0–2 only** (census → prereg + contract → PR). Phases 3–4 are described so the prereg is authored with them in view; they run only after their own operator GO marks, in this or a later session.
**Parent question:** the deep-iteration lane charter's own §4 H — *"bounded-depth iteration inside one pre-registered family, survivor-measured on untouched confirm, yields at least one candidate that clears confirm + cost-law + N-SURV where the one-shot corner has yielded none."* Tested **zero** times to date: DL-1 and DL-2 both died at the train gate, confirm never read.
**Authority:** Joshua (operator). Three separate GO marks are required and none may be self-applied: (1) family election, (2) prereg + campaign-envelope GO, (3) confirm-read GO. First act after Phase 0: save this brief to `docs/briefs/handoffs/2026-09-02-cc-handoff-deep-lane-dl3-premise-test.md` on your branch so its anchors are on disk.

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any §2 work)

Read each file **on your branch** (not from memory, not from this brief's summaries — the two-ledger K ADR's drafting hit the quote-from-summary failure three times in one session). Post a read-report with the stated ranges and `git log -1 --format='%h %ci' -- <path>` anchors before doing anything else.

- `docs/adr/2026-08-16-deep-iteration-lane-charter.md` — report: §2.1 (family rule, non-index-first, channel-origin rule), §2.2(i)–(iv) verbatim, §2.4 half-split control, §4 in full (H, inertness limb, yield limb, counting machinery, the **Running counts** line), §5, §6 steps, §7 step 1, Change history rows from 2026-08-22 onward. Expected running counts: completed 0 · falsified 0/2 · **abandoned 2 (consecutive 2/2)** · active none.
- `docs/adr/2026-08-22-grow0-two-ledger-k-question.md` — report: §2 (what was rejected vs adopted; §2.2(iv) is disclosure-only, never a refusal on its own).
- `docs/briefs/closures/GROW-0-closure-resolved.md` — report: §1 table + §3 "what this does NOT license".
- `docs/briefs/pre-registration/2026-08-24-grow-0-limb-c-marginal-effect-RESULTS.md` — report: §1 reporting table and §3 row-2 table (composite P(accept) 0.90 at target_sr=1.8 vs **0.43 at the POWER_MIN=0.50 boundary; two-consecutive-miss 0.32**).
- `docs/notes/audits/programme-audit/2026-08-23-deep-lane-supply-audit.md` — report: §3.5 census in full (incl. the 2026-08-24 conjunct-(iii) correction), §4 verdict + re-test conditions, §5.
- `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS_DESIGNBOX_EXT.md` — report: Status line and §6 headline (**80/80 design-box cells INFEASIBLE**, closest 5.05% bust).
- `lab/analysis/c1/shape_feasibility_map_2026-08/RESULTS.md` §7 — report: the three routing findings (WR floor 55–70%, mean win > low skew, $3,000 rope binds).
- `docs/notes/notice/N-2026-08-24-ox-alpha-deep-lane-design-review.md` — report: §1 rows 2, 3, 5, 8, 10, 13, 14 and §2.
- `docs/briefs/pre-registration/2026-08-22-deep-lane-dl2-m6a-pdhpdl-prereg.md` — report: full section structure (this is your structural model) and its Change-history row on the geometric-feasibility diagnostic.
- `lab/archive/dl2_m6a_pdhpdl_2026-08-22/RESULTS.md` — report: the `## Iterate` block (two structurally different failures, DL-1 candidate-level vs DL-2 geometric; the diagnostic script path `geometric_feasibility_diagnostic.py`).
- `docs/adr/2026-08-30-candidate-contract.md` §2 · `2026-08-30-evaluation-order.md` §2 (steps 1–9) · `2026-08-30-operator-approvals-campaign-envelope.md` §2 · `2026-08-30-tradeable-reachable-gate.md` §2 · `2026-08-30-terminal-taxonomy.md` §2 · `2026-08-30-channel-liveness-gate.md` §2 — report: each Decision section. These post-date the charter and bind every new candidate on every channel. Note `STATE.md`'s row that the deep lane still **owes** its candidate-contract migration and liveness-ceiling addenda — read them, comply with them, do not author them (§5).
- `docs/adr/2026-08-24-tradeify-growth-tier-scoring-only.md` — report: Decision (`Tradeify_Growth_100K` in the operational target set; its bust figures' bound caveat).
- `lab/discovery/register_search.py` — report: `open_run` deep-lane branch (`--lane deep` requires `--grammar-file --grammar-sha256 --confirm-years --target-sr`; `--search-space-size` must equal the grammar budget; burned-segment refuse/disclose path). `lab/discovery/deep_lane_admission.py` — report: `K_CEILING`, `FLOOR_CEILING`, `evaluate_deep_admission` signature. `lab/discovery/burned_segments.py` — report: `consultation_count`/`consultation_history` API and the seed window (MNQ 2025-09-01→2026-08-05, burned).
- `scripts/instrument_profiles.py` — report: `cell` subcommand contract (exit 1 with BINDING BAR lines = consulted; exit 2 FATAL = executed only, not consulted).
- `docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` §3 + `lab/research_utils/nsurv_channel.py` — report: the frozen N-SURV gate (bust ≤3.0% ∧ P(pass) ≥50%, ≥2 firms, ≥1 trailing_locking; intraday-honest clock mandatory).
- `docs/rejected_candidates.md`, `lab/CATALOG.md`, `docs/briefs/INDEX.md` — report: every row touching the families you shortlist in Phase 1 (re-proposal bars, DEAD-list rows, standing pauses).
- `STATE.md` — report: rows mentioning deep-lane / GROW / MNQFLOW / MNQTAPE / channel-liveness; the OPERATOR QUEUE (do not add to it).

Amendment-first paste (Rule 8.10), run on your branch before authoring anything:
```text
$ ls docs/briefs/pre-registration/ | grep -i deep-lane
# expected: dl1 (2026-08-16), dl2 (2026-08-22) — no dl3 exists
$ rg -n "DL-3|GROW-1" docs STATE.md
# expected: forward references only; no opened campaign
```

After Phase 0: post the read-report and any §0.5 ambiguities. **Wait for the operator's go-ahead before Phase 1.**

---

## §0.5 — Clarifying questions (HALT-ON-AMBIGUITY)

Halt with `Status: NEEDS_CONTEXT` rather than guess if any of these are unresolved after Phase 0:
- **Family already chosen?** If the operator names a family in their first reply, skip Phase 1's census and score that family against §1's six criteria only; present the score and halt for GO.
- **Non-index vs index (§1 criterion b).** The charter says non-index CME micros first; nearly all live supply is on MNQ/MYM (index). If your shortlist is index-only, say so plainly and present the raised-bar route each family would have to clear — do not silently pick either side.
- **Tier for N-SURV scoring.** Default below is the incumbent `Tradeify_Select_100K` plus a reported `Tradeify_Growth_100K` line. If the operator wants Growth as the *gating* tier, ask.
- **Spend.** Default is $0 external spend. Any Databento pull needs its own dry-run number and GO inside the campaign envelope. If the best family needs a pull, price it and halt.
- **Anything in the charter or an 08-30 ADR that conflicts** with this brief — the doctrine governs; surface the conflict.

---

## §1 — Context and what you are producing

**Why now.** The lane's tooling is validated (GROW-0 `RESOLVED`; Limb C measured the gate stack; §2.2(iv) landed; `burned_segments` is wired). The premise itself has never been tested because both real campaigns died before the confirm read — DL-1 on a dead candidate (40–70% of trades resolving to stop/target, adverse hit-rate), DL-2 on venue-infeasible geometry (85–97% of trades never reaching 1R). The supply audit's verdict is `AMBIGUOUS` — untestable until a family exists that can survive the train gate. **A third abandonment is very likely the lane's death**: the liveness-gate ADR maps the lane's yield limb to "retirement," and the channel-retirement ADR's starvation check fires at the 2026-11-08 quarterly audit if the lane is still zero-yield. A campaign that *reaches confirm and fails* costs one of the two yield-limb strikes. Choose accordingly.

**What "testing the premise" requires — the family-selection criterion (score every candidate on all six):**

a. **A one-shot baseline exists in the estate record for the same family, and it yielded none.** This is the load-bearing criterion: if the family has no prior one-shot result, a DL-3 success says "this family has an edge," not "depth found what one-shot missed." Cite the exact closure/Notice/CATALOG row. A family under a mechanism-level DEAD-list bar is admissible only if the prereg clears that bar in writing (charter §2.1) — never as a θ-retune.
b. **Charter §2.1 instrument rule.** Non-index CME micro first (no raised bar binds). An index-intraday family (MNQ/MYM/MES) must answer `index-intraday-ohlcv-directional-timing-2026-07-21` by a route you can *show*: route ① under the 2026-08-10 temporal-selectivity ruling's §2-B conditions, or route ③ with a frozen beats-incumbent term wired into confirm scoring (the 2026-08-10 falsifier LOG records route ③ as unclearable ex ante — a PREREG promise does not discharge it).
c. **Venue payoff-shape prior, before any data.** Measured/prior WR ≥55% (no cell ≤50% is `FEASIBLE` on the $3,000 rope), larger mean win preferred over tighter distribution; hard stop, session-flat, no pyramiding (N-SHAPE); ≥1 trade/week (N-ACT). **The charter's design-box geometry (WR 30–40%) scored 80/80 INFEASIBLE — do not target it.** The six generic MR-at-level fades all died with negative gross edge — not a candidate class.
d. **Geometric feasibility.** Stop+target span must be traversable inside the holding window. Run DL-2's `geometric_feasibility_diagnostic.py` shape (or its equivalent) on *prior/published range statistics or the estate's instrument ledgers* — never on the campaign's own CONFIRM window; disclose any TRAIN-window read in the contract's founding freeze.
e. **Not paused, not burned, not held.** Dense-1m temporal-selectivity pause (lane-wide); CON-5 unread-forever; the burned MNQ 2025-09-01→2026-08-05 window; `MNQFLOW-1-DEPTH` (operator HOLD, ~$150); `MNQTAPE-2` (HOLD, $308.69); the overnight-range conditioner retracted 2026-08-31 (`Q-RANGECOND-1-closure-falsified.md`) and the MYM overnight-window scope-gap correction (`Q-RANGEXFER-1`). Attest each explicitly.
f. **Data reachable inside the envelope.** Cached TV panels / already-pulled Databento at $0, or a dry-run-priced pull the operator approves. The charter's GO-1 dry-run priced bar schemas on the *design-box triad* at $0 — do not assume that carries to a new instrument or schema.

**Where to census (verify every status on disk — several verdicts moved after they were written):** `lab/CATALOG.md`, `docs/briefs/INDEX.md`, `docs/rejected_candidates.md`, `ops/instruments/*.md`; the eleven `docs/notes/notice/N-2026-08-29-m{nq,ym}-*.md` daily-geometry notices (several `GRADUATE`; the 08-31 look-ahead retraction and the MYM scope-gap correction post-date them — re-verify each); `docs/briefs/Q-VOLREGIME-1-*.md`; the supply audit §3.5; `ORB-MNQ-1` (the one admitted-then-payability-falsified candidate; index; `PARKED`); the MOC-imbalance fade (the only untested forced-counterparty member of the fitting shape class — MES, index; scrape artifacts live on a **local** worktree `claude/elastic-gauss-910e93`, not on `origin/main` — verify before citing; 235/342 days with a recoverable sign); `MNQTAPE-1` (structured near-miss, correct sign, order-flow; its larger-N prereg is HELD). Families with a *marginal or structured-near-miss* one-shot result are the best premise tests; families with a clean mechanism-level kill are the worst.

**Power requirement set by this handoff (stricter than the charter's POWER_MIN):** the prereg must declare a design-target edge with `deep_lane_power ≥ 0.90` at the frozen confirm length (DL-1/DL-2 both declared ≈0.96). Limb C measured composite P(accept | true edge) = 0.43 at the 0.50 boundary and a two-consecutive-miss probability of 0.32 — a boundary-admissible campaign would spend the lane's falsification budget on noise. If the honest target for the elected family cannot reach 0.90, report it and halt; do not declare a target the family has not earned.

**Deliverables (Phase 2, one PR):**
1. `docs/briefs/pre-registration/2026-09-DD-deep-lane-dl3-<sym>-<family>-prereg.md` — charter §7 step 1 filename pattern, DL-2's section structure, plus: §2.2(i)–(iii) computed via `evaluate_deep_admission` with the numbers pasted; §2.2(iv) disclosure via `burned_segments` (channel-agnostic query, pasted); §2.4 half-split point and per-half floor; nomination rule (argmax train net annSR, no fallback); SPA/StepM thresholds (W4 re-arm, K>3); cost-law at the venue-legal expression via `cost_model` per-instrument (never the $0.91/$0.95 literals for non-index); `instrument_profiles.py cell <SYM> <family>` output pasted (exit 1 + BINDING BAR lines, each bar answered by a named route); standing-pause attestation; executed dedup paste; GO-1's intraday-clock caveat as a named risk; the geometric-feasibility diagnostic result; the §1 six-criterion score.
2. The **candidate contract** per `2026-08-30-candidate-contract.md` §2 (founding freeze: instrument, feature catalogue = the frozen grammar, complete tradeable entry/exit object, exploration + confirm windows, K, costs, schema ladder, campaign envelope, **frozen discriminator adjudication rule** per terminal-taxonomy). Colocate with the prereg unless that ADR names a location; state the choice.
3. The **campaign-envelope request** per `2026-08-30-operator-approvals-campaign-envelope.md` §2: max spend, schemas, windows, K, and the frozen multiplicity configuration (α, M — M=1 unless argued, named procedure).
4. `grammar.json` for the family (K=G, GO-2's K≈10 default; SHA256 pinned in the prereg) and the `TRADEABLE-REACHABLE` pre-gate record (cost via harvest Requirement 5 bp-of-panel-price; latency/geometry via the owning checks; payoff-shape priors with conservative reading).
5. A `docs/SESSIONS.md` entry (`python scripts/roll_sessions.py --next-label <date>` first) and the PR. **No in-chat adversarial Workflow before the PR — Codex's PR review is the adversarial step.** Address Codex findings, then halt with `Status: DONE` and the GO request.

**What you are NOT producing:** any confirm read; any per-variant confirm statistic; the charter's owed liveness/contract addenda; a STATE.md queue row; a GROW-0 re-run; a Pine file; anything armed.

---

## §2 — Execution plan

### Step 2.0 — Phase 0 reads (§0). Gate: read-report posted, anchors match, §0.5 resolved or `NEEDS_CONTEXT`.

### Step 2.1 — Supply census (re-census; the 2026-08-23 census is stale)
- **Inputs:** the sources in §1; no campaign data.
- **Action:** enumerate every candidate family with a one-shot record; score each on criteria a–f; run the geometric-feasibility diagnostic on priors/ledgers for the top three; compute `deep_lane_power` at each family's honest target and the charter's `floor_at_k(10, years)` for the confirm length its data allows; price any pull with the `databento-data` dry-run.
- **Expected output:** a shortlist table (≤3 families × 6 criteria + power + $), one recommendation, and the non-index/index tension stated plainly.
- **Gate:** **HALT** — `Status: NEEDS_CONTEXT` (family election is the operator's). Do not open Step 2.2 until a family is elected in-chat.

### Step 2.2 — Prereg + contract + envelope (one PR)
- **Inputs:** the elected family; DL-2's prereg as structural model; the 08-30 ADRs.
- **Action:** author deliverables 1–4; run `python scripts/check_brief.py <prereg> --type inquire` (0 HARD); run the charter §10 floor command (`1.0 0.95 1.475 2.09`); confirm `register_search.py open --lane deep` **would** accept the manifest by dry-running the admission predicate (`evaluate_deep_admission`) — do not open the manifest yet (that is Phase 3, post-GO, and binds K); write the SESSIONS entry; commit; push; open the PR; address Codex.
- **Expected output:** PR URL, prereg `Status: PROPOSED (pre-lock)`, contract founding-freeze hash.
- **Gate:** **HALT** — `Status: DONE` with the envelope terms (spend / schemas / windows / K / α / M / procedure) and the exact GO wording requested. No self-marking `FROZEN`.

### Phase 3 (post-GO; own session if needed) — `register_search open --lane deep` (binds K before any read; §2.2(i)–(iii) refuse-at-freeze; (iv) disclosed; burned-segment refuse) → pulls → TRAIN scoring of every variant → nomination → gates 2a (net annSR>0 + cost-law), 2b (SPA over the full variant universe), 2c (cadence ≥1/wk), 2d (M-16 +1-tick slippage) → append-only selection freeze → **HALT for confirm-read GO**. An abandonment here is recorded on the charter's running-count line the way DL-1/DL-2 were.

### Phase 4 (post-confirm-GO) — one confirm read on the nominated survivor only → pooled + half-split against the per-half floor → intraday-honest N-SURV on `Tradeify_Select_100K` (gating) with `Tradeify_Growth_100K` reported → terminal-taxonomy verdict (`CONFIRMED` requires discriminator **and** payoff both clear) → closure with `## Iterate` block → charter running-count line, SESSIONS, STATE.

---

## §4 — Falsifiable hypothesis (verbatim from the charter; assert against these, not re-derived ones)

**H:** bounded-depth iteration inside one pre-registered family, survivor-measured on untouched confirm, yields at least one candidate that clears confirm + cost-law + N-SURV where the one-shot corner has yielded none.
**Strike (yield limb):** the nominated survivor fails the confirm read, or passes confirm and fails N-SURV. Two consecutive strikes ⇒ lane `FALSIFIED`. Current: 0/2.
**Abandonment:** discloses, does not strike; recorded on the running-count line. Current: 2 consecutive.
**This campaign's own gates:** the prereg's §4 must name target_sr, floor, years, power (≥0.90 here), half-split point + per-half floor, α/M/procedure, and the discriminator rule — all before any read.

---

## §5 — Forbidden moves (each was tempting in DL-1/DL-2 or their reviews)

- **Reading the CONFIRM window, any per-variant confirm statistic, or the burned MNQ window** — charter §5; §2.2(iv) discloses, it does not license.
- **Choosing a family for its clean governance door rather than its edge plausibility** — the audit's Q6 finding on DL-2. Criterion (a) and (c) come first; the door check comes after.
- **Declaring a boundary target (power ≈0.50) to make an otherwise-refused family admissible** — Limb C: 0.43 composite accept, 0.32 two-miss.
- **Targeting the charter's design-box geometry, or any WR ≤50% shape** — 80/80 INFEASIBLE; no cell ≤50% feasible.
- **θ-retuning DL-1's or DL-2's constructs into a "new" family** — re-proposal needs new mechanism evidence, not new parameters.
- **Authoring the charter's owed addenda, a STATE.md queue row, or "while I'm here" edits to `register_search.py` / `deep_lane_admission.py` / any `core/` file** — log in `DONE_WITH_CONCERNS`; do not touch.
- **Opening the `register_search` manifest before the prereg GO** — it binds K; Phase 3 only.
- **Any Databento pull without a pasted dry-run and an in-envelope GO; any multi-agent local simulation fan-out** — this machine is a budget laptop; heavy sims run single-threaded or in the cloud.
- **In-chat adversarial Workflow runs before the PR** — Codex reviews at PR time.
- **Restating a number from a summary, memory, or this brief instead of the production file** — every figure in the prereg cites the file and anchor it was read from.
- **Self-marking GO, FROZEN, or the family election.**

---

## §6 — Status return

Report exactly one: `DONE` · `DONE_WITH_CONCERNS` · `NEEDS_CONTEXT` · `BLOCKED — <context-problem | capability-problem | scope-problem | plan-itself-wrong>`.

```
Status: <...>
Phase reached: 0 | 1 (shortlist posted, awaiting election) | 2 (PR open, awaiting GO)
Per-step gates: 2.0 [...], 2.1 [...], 2.2 [...]
Diffs (files touched): <list — expected: prereg, contract, envelope request, grammar.json, SESSIONS.md, this handoff>
PR: <url>
Concerns surfaced: <list>
Next action recommended: <one sentence>
```

---

## §7 — Parent-session review (before any GO)

**Pass 1 — spec compliance:** diff list matches §1 deliverables exactly; no `core/`, `register_search.py`, charter, or STATE queue edits; no confirm read anywhere in the diff or the logs.
**Pass 2 — quality:** the six-criterion score cites a real file per cell; power ≥0.90 computed by the production function with the numbers pasted; `instrument_profiles cell` exited 1 (not 2); the dedup paste matches its own command; the discriminator rule is frozen before any data; Codex findings addressed, not argued away.
**Pass 3 — consolidated read:** prereg, contract, envelope, and grammar agree on instrument / windows / K / target / floor / α / M byte-for-byte.

---

## §10 — Audit hooks

```bash
# Charter unchanged and counts as expected
grep -n "Running counts (canonical, this ADR)" docs/adr/2026-08-16-deep-iteration-lane-charter.md
python -c "import sys; sys.path.insert(0,'lab'); from research_utils import axis_screen as a; print(a.CAP, a.DSR_MIN, round(a.floor_at_k(33),3), round(a.floor_at_k(33, years=3.25),3))"
# Expected: 1.0 0.95 1.475 2.09

# Prereg well-formed; power >= 0.90 at the declared target
python scripts/check_brief.py docs/briefs/pre-registration/<dl3-prereg>.md --type inquire
python -c "import sys; sys.path.insert(0,'lab'); from discovery.deep_lane_admission import deep_lane_power; from research_utils.axis_screen import floor_at_k; print(deep_lane_power(target_sr=<T>, floor_sr=floor_at_k(10, years=<Y>), years=<Y>))"

# No confirm read, no burned-window read, no manifest opened pre-GO
rg -n "confirm_stat|CONFIRM read" docs/briefs/pre-registration/<dl3-prereg>.md   # expect: design text only, no numbers
ls discovery_manifests/ | grep -i dl3                                              # expect: none before Phase 3

# Door check consulted, not merely executed
python scripts/instrument_profiles.py cell <SYM> <family>; echo "exit=$?"         # expect exit=1 + BINDING BAR lines
```

---

## Addendum 2026-09-02 — executing-session corrections (append-only; the received body above is unedited)

**Status:** recorded by the executing CC session at the Phase 0 gate, after a Codex review of
[PR #263](https://github.com/Joshua-Asante/first-passage/pull/263) returned 11 findings against the
body above. Each was verified against production before being accepted here; all 11 hold. The
brief's body is **deliberately not edited** — it is the record of what was handed over (Trap #12 /
the dated-record convention this repo uses elsewhere, e.g. the supply audit's own 2026-08-24
conjunct-(iii) correction). **Where this addendum and the body disagree, this addendum governs
execution.** $0 · K=0 · no campaign opened.

### C1 — ⚠ The N-SURV gate is **bust ≤ 5.0%**, not 3.0%. The brief's §0 read-target is CLOSED.

`docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md` carries a closure banner
at its head: **`CLOSED 2026-08-26 — superseded by v2 (ceiling 3.0% → 5.0%, operator ruling)`**.
The governing artifact is
[`2026-08-26-prop-survivor-scoring-prereg-v2.md`](../pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md)
(`Supersedes … in full (Part A eval ceiling 3.0% → 5.0% only)`), and production agrees:

```
$ python -c "import sys; sys.path.insert(0,'lab'); sys.path.insert(0,'core'); \
  from discovery.prop_survivor_scoring import DEFAULT_PREREG, load_scoring_thresholds; \
  print(DEFAULT_PREREG); print(load_scoring_thresholds())"
…/docs/briefs/pre-registration/2026-08-26-prop-survivor-scoring-prereg-v2.md
ScoringThresholds(eval_bust_ceiling=0.05, funded_bust_ceiling=0.01, pass_floor=0.5,
  tier_keys=('Bulenox_100K','Tradeify_Select_100K','MFFU_Rapid_100K','BluSky_Premium_100K'), …)
```

Every "3.0%" in the body above (§0 read-target, §1 criterion c's framing, Phase 4) reads **5.0%**.
Part B (funded, 1.0%) and the pass floor (≥50%) are unchanged. The v2 §8 is explicit that this was
an **operator risk-tolerance override, not a re-derivation finding the old ceiling wrong** — cite it
that way, never as new evidence.

**C1-followon (not raised by the review; found while verifying it) — the venue-shape map underneath
criterion (c) is scored against the superseded ceiling.** `run_region_sweep.py:77` and
`run_designbox_sweep.py` both hard-pin `DD_GATE = 0.03` and assert
`abs(thr.eval_bust_ceiling - DD_GATE) < 1e-9` at every invocation
(`run_region_sweep.py:286`, `run_designbox_sweep.py:172`). Against the live v2 prereg that assert
now **fails loudly** — which is precisely what A2's own §0 promised it would do if the prereg ever
drifted. Consequences, stated but **not acted on** (out of scope; no `lab/` harness edited here):

* A2 `RESULTS.md` §7's "no cell at win_rate ≤ 50% is `FEASIBLE`" and the 55–70% win-rate floor are
  **3.0%-ceiling findings**. The floor at 5.0% is unmeasured and is necessarily **no higher**.
* `RESULTS_DESIGNBOX_EXT.md`'s **80/80 INFEASIBLE** is likewise a 3.0%-ceiling result, and its
  closest cell (WR=35%/cd=1/frontier-R, **bust 5.05%**, 2σ lower bound 4.80%) sits *astride* the new
  line — a confident fail at 3.0%, an unresolved call at 5.0%.
* Therefore criterion (c)'s "WR ≥ 55%" prior is **not currently established at the live gate**.
  Phase 1 must present it as such and must not quote either document's verdicts as though they were
  scored at 5.0%. Re-scoring the map is its own operator-gated decision, not a DL-3 deliverable.

### C2 — Phase 4 omits mandatory pre-holdout steps 7 and 8.

`2026-08-30-evaluation-order.md` §2 requires, **before any holdout is consumed**: step 7 the
contract-integrity check (code/data hashes, manifest `K` vs contract `K`, frozen multiplicity
configuration, candidate vs the step-6 hash-pinned commit, holdout vs the step-2 reservation — a
mismatch is `EVIDENCE-VOID`, never an evidentiary rejection) and step 8 the zero-K role state-drift
re-check (Product-Group/sign, cap, session, S7 occupancy; failure emits `ROLE-BLOCKED` and follows
the contract's frozen succession rule — forfeit by default). The body's Phase 4 jumps from the
selection freeze straight to the read. **Both steps run before the confirm read**, and the
`ROLE-BLOCKED` succession/forfeit election is a founding-freeze field.

### C3 — Phase 4 must gate on the frozen four-firm cross-section, not on Select alone.

v2 §3 keeps v1's cross-section unchanged: exactly `Bulenox_100K` · `Tradeify_Select_100K` ·
`MFFU_Rapid_100K` · `BluSky_Premium_100K`, discharged only when **≥2 distinct firms** clear Part A,
**≥1 of them `trailing_locking`**; all other tiers are diagnostics only. `Tradeify_Growth_100K` is
not in the set, and — the point the body missed — Growth and Select are the **same firm**, so two
passing Tradeify tiers cannot satisfy "≥2 distinct". Score the frozen four; report Growth as a
diagnostic. This also settles the body's §0.5 tier question: making Growth *gating* is not an
operator preference this session can take, it is an amendment to a frozen prereg.

### C4 — The door-check exit-code expectation in §1 deliverable 1 and §10 is inverted.

`scripts/instrument_profiles.py::cmd_cell` returns **0** for a consulted clean cell, **1** only when
a blocking verdict or a bar is present, and **2** for FATAL (missing ledger/unknown symbol/unknown
mechanism — executed, not consulted). Charter §2.1's preferred non-index path requires *no* BINDING
BAR, i.e. **exit 0**. Requiring "exit 1 + BINDING BAR lines" would reject the preferred clean
candidate and reward a blocked one. **Consulted = exit 0 or 1; a clean route requires exit 0; only
exit 2 is a non-consultation.** Verified live: `cell MYM opening-range-continuation` → exit 0 is
wrong to expect too — that cell prints two BINDING BAR lines and a `DEAD` verdict; the real contract
is the source above, not either document's expectation.

### C5 — `M = 1` is frozen unconditionally for this lane, not "unless argued".

Charter §2.3: the confirm partition is read **once, on the single pre-nominated survivor**, and
per-variant confirm results are never computed. The general campaign-envelope ADR's `M` is a
ceiling on how many cells Explore may advance; for a deep-lane campaign that ceiling is 1 by the
charter's own selection rule. Declaring `M > 1` would mint confirm slots the lane cannot lawfully
consume. **DL-3 freezes `α` with `M = 1` and a named procedure; the "unless argued" clause in the
body's deliverable 3 is withdrawn.**

### C6 — The third-abandonment consequence in §1 is overstated.

Charter §4(c): abandonment **discloses, does not strike**; two consecutive trigger an
audit-report duty, and that duty was **already discharged 2026-08-23**. A third abandonment
therefore adds no strike and triggers no retirement. `2026-08-30-channel-liveness-gate.md` §2 maps
deep-iteration's *yield* limb to "retirement" in effect but states plainly that **neither
consequence is self-executing**, and the lane's reconciliation addendum is still owed and
unauthored (STATE 2026-11-08 row). The 2026-11-08 starvation check requires a programme-level
ruling, not an automatic close. The body's "a third abandonment is very likely the lane's death" is
**not the counter state** and must not be allowed to bias family election toward risk-seeking.
What is true: only a **confirm-read failure or a post-confirm N-SURV failure** strikes the yield
limb (0/2), and that limb is the one mapped to retirement.

### C7 — The §10 power hook must use the declared `K`, not a hardcoded 10.

`register_search` refuses unless `--search-space-size == grammar.generation_budget`. GO-2's K ≈ 10
is a default, not a literal. The audit command reads:

```bash
python -c "import sys; sys.path.insert(0,'lab'); \
  from discovery.deep_lane_admission import deep_lane_power; \
  from research_utils.axis_screen import floor_at_k; \
  print(deep_lane_power(target_sr=<T>, floor_sr=floor_at_k(<K>, years=<Y>), years=<Y>))"
# <K> = the contract's declared K; assert it equals grammar.generation_budget
```

### C8 — `evaluate_deep_admission` alone does not establish that the manifest would open.

`open_run`'s `--lane deep` path additionally validates the grammar file and its SHA-256 (drift-
checked), `K == generation_budget`, `--instrument` + `--data-window` syntax, burned-segment overlap
(a hard abort, no manifest written), and the frozen `--prereg` path — plus any supplied cost-law
inputs — all before writing. Step 2.2's pre-GO check must exercise each non-writing precondition and
report them individually, rather than equating the three-conjunct predicate with acceptance.

### C9 — Evaluation-order has **ten** steps; Phase 4 must record step 10.

The body's §0 says "steps 1–9". Step 10 (portfolio and venue fit, `CONFIRMED` candidates only) is
mandatory: re-run the step-8 role check if the deployment target moved, always re-check S7
occupancy (dynamic), then composition/aggregate/activity/drawdown/sizing. A failure there rejects
the **placement**, not the confirmed status (`CONFIRMED · VENUE-FAIL(edition)` is a valid standing
disposition). Phase 4 currently closes at the N-SURV verdict and would never record placement.

### C10 — The MOC-imbalance family is operator-closed; it is not a live census entry.

Already raised independently at the Phase 0 gate and confirmed by the review.
[`2026-09-01-next-vet-intake-decision.md`](../../notes/2026-09-01-next-vet-intake-decision.md):
B1 strategy **`DROP`**, source pursuit **`STOP`**, zero measured expectancy, no complete expression.
Its re-proposal bar requires independently credible evidence of a **large positive net** expectancy
plus a complete frozen expression, and explicitly excludes "a different index micro". The cited
`claude/elastic-gauss-910e93` worktree exists neither locally nor on `origin`. Phase 1 records the
closure and the bar; it does not shortlist the family. Likewise `MNQTAPE-2` is **`NO-GO`** (operator
declined 2026-08-23), not `HOLD`.

### C11 — Prereg vs candidate contract: unresolved, with a proposed resolution.

`2026-08-30-candidate-contract.md` §2 replaces the deep-iteration channel's freeze-chain documents
with typed appends to **one** hash-addressed contract and forbids "a new file restating fields the
contract already holds"; the review reads this as one artifact, not three. Charter §7 step 1 still
mandates a pre-registration matching the `*deep-lane*` filename pattern, whose path is recorded on
the charter's running-count line — and the deep lane's contract-migration addendum is **owed,
unauthored, and forbidden to this session** (§5). **Proposed resolution, pending the operator's
ruling:** one artifact, filed at the charter's mandatory `docs/briefs/pre-registration/*deep-lane*`
path, structured as the candidate contract's append-only freeze points, carrying the envelope entry
and the charter-specific sections (§2.2 conjuncts, half-split, nomination, SPA/StepM, forbidden
moves) — one hash, one file, both ADRs' requirements met, no field restated twice. Phase 2 will not
open until this is ruled on.

### What this addendum does NOT do

No `core/`, `lab/`, `scripts/`, charter, ADR, prereg, or STATE edit. It does not re-score the A2
map, author the lane's owed addenda, elect a family, open a campaign, bind K, or apply any GO.
