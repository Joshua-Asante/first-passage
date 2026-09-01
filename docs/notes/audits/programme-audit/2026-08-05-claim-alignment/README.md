# Programme audit — post-de-scope claim alignment (object + meta layers)

**Status:** `Complete, two rounds. Every finding is a RECOMMENDATION pending operator ruling, except the four marked FIXED / RULED in §5 below.`
**Audit date:** 2026-08-05 · **Repo anchor:** `e031225`, worktree clean. Round-1 artifact committed `06caf3a`; the section set was written and its hooks re-executed at HEAD `0af62ec`.
**Layers:** **object** (the prop-portfolio / venue / deployment claim estate) and **meta** (the correction machinery and gate estate), answered separately throughout per the two-layer coupling rule.
**Window:** 2026-07-12 (prop-portfolio programme reopened) → 2026-08-05, with the pivotal event at 2026-08-04.

**This file is the entry point.** It carries the navigation table, the combined counts, the two disposition verdicts, and the bars. It carries **no findings** — those live in `02`–`06`, one section per tier, and each is openable and actionable on its own.

---

## §1 — Trigger: a degeneration signal, not scheduled cadence

On 2026-08-05 two constraints were read as binding when neither was:

1. `docs/spec/2026-07-27-third-leg-target-spec.md`'s **S5** cap table, **S7** order-symbol bar and **R1** σ ceiling — all of which reserve, bar, or budget against a two-leg book withdrawn from deployment the previous day.
2. `STATE.md`'s queue-reset claim that B7-REFIRE Stage 1 is *"permanently owed and permanently undischargeable at this venue"* — which reads as a standing rule when the underlying reason (no deployed strategy can emit a signal) is **contingent**.

Both exemplars are **calibration only and are excluded from the findings set.** The signal they name is the audited class: **premise-dead claims surviving a deployment-scope decision that changed no code.**

**The pivotal event.** ADR [`2026-08-04-tradeify-venue-descope-eval-included.md`](../../../../adr/2026-08-04-tradeify-venue-descope-eval-included.md) de-scoped the Tradeify venue as a deployment target for the locked Striker book, **evaluation included**, withdrawing both Striker legs (DJ30→MYM, NAS100→MNQ) from the c1 eval deployment. It touched no code, no `LEG_MAP` entry, no lifecycle state and no allocation; lifecycle stayed `AUTHORIZED · MECHANISM @ 1.00×` (*"venue-fit is not decay"*); a same-day Addendum narrowed the bar to **redeploying those two legs**, not to Tradeify-shaped research. Three forks were left open: **F1** (§4 reading of a de-scoped firm, 2026-11-08) · **F2** (rail disposition, 2026-08-08) · **F3** (successor venue, 2026-08-08).

**Because the decision changed deployment state and not any document or schema, nothing forced a re-read.** Every claim derived from the pre-08-04 configuration — two legs deployed, cap allocated MYM 69 / MNQ 11, `MNQ1!`/`MYM1!` occupied, a $273/day book to compose against — survived unexamined. That is the failure class both rounds hunted.

**This audit does not discharge the 2026-08-08 obligation.** It is an unscheduled response to a dated discovery; the nearest scheduled vehicle is three days out.

---

## §2 — Navigation

**Why the split exists:** the round-1 artifact was one 1020-line file and was not navigable. Round 2 then swept the seven surfaces round 1 admitted it had missed, and both rounds are integrated here. **A remediator should open exactly one section file and be able to act from it** — every row names its target file, its anchor, and the exact edit.

| Section | What it covers | Rows | Evidential standing |
|---|---|---:|---|
| [`01-diagnostics.md`](01-diagnostics.md) | The Programme Audit Protocol's **seven diagnostic questions**, answered separately per layer — hard core, belt churn, progressive evidence, degeneration evidence, boundary, theory comparison, falsifier check. Ends with the audit's sharpest structural result: **six gates stopped binding with zero threshold movement**. | **14** layer-separated answers · **16** table rows (object belt 4 · meta belt 3 · threshold changes 3 · gates that stopped binding 6) | Round-1 body, ported and re-verified at `e031225`; round-2 evidence integrated at **four** points and marked `[R2]` inline. Four findings it reports as *found* carry a `✅` disposition line. |
| [`02-blockers.md`](02-blockers.md) | Every **BLOCKER** either round produced — `B1`, `B2`, `B3` — with what was claimed, what was verified, what was actually done, and what residue survives. **All three are FIXED and committed.** Round 2 raised **zero** new BLOCKERs. | **3** findings across **7** target files and **3** commits · **8** named residue items, none at BLOCKER severity | **Highest in the set.** All three are round-1 findings raised against a 21.4% refutation rate, each survived the adversarial pass, each carried a hook executed at `e031225` — and every hook was **re-executed at HEAD** with its output pasted. |
| [`03-agent-facing.md`](03-agent-facing.md) | Round 2's findings on surfaces consumed by an **AI agent or by an operator mid-task** — `deploy/` runbooks, `.claude/skills/`, `.claude/` hooks and commands, `.cursor/` rules, `scripts/` usage text and docstrings, and the `docs/` instruction estate. A stale instruction here causes an **action**, not merely a belief. | **49 rows** (one per target file) · **76** adjudication records · **71** findings. Verdicts: 34 KEEP-CORRECTED · 25 SIMPLIFY · 16 DELETE · 1 KEEP-AS-IS | **Round 2** — see the standing caveat in §3. Every row that rests on a guard **names the guard** and is bounded by it; the four rows with **no guard** are called out to land first. |
| [`04-misleading.md`](04-misleading.md) | **MISLEADING** findings whose consumer is a *reader* — an operator, an author, a future triage. This is the tier where a stale claim can cause a wrong deployment, a wrong clearance, a wrong gate reading, or (at **M15**) a real-money action. | **50 rows** across **42** primary target files · **54** findings (43 round-1 `M1`–`M43`, 11 round-2). One row (`M13`) is struck **MOOT**, not dropped | **Mixed and marked per row** — `(R1)` rows against a 21.4% refutation rate, `(R2)` rows against 9.7%. Round-2 rows resting on a mechanical check name the check so it can be re-run. |
| [`05-cosmetic.md`](05-cosmetic.md) | **COSMETIC**, non-agent-facing. Low consequence — nothing here can cause a wrong deployment, a wrong clearance, or a real-money action. That is the whole content of the label, and it is why this tier is deferrable to the 2026-11-08 checkpoint. | **45 rows** · **71** findings (48 round-1 `C1`–`C31`, 23 round-2 `C32`–`C45`) · **12** absorbed rows deliberately not re-rowed | **Mixed.** Round-1 verdict tally is *countable* here rather than hand-tallied (23 KEEP-CORRECTED · 20 SIMPLIFY · 17 DELETE · 2 KEEP-AS-IS over 62). **Nine of the 23 round-2 rows are load-bearing** — COSMETIC is a consequence rating, not a precision one. |
| [`06-operator-judgement.md`](06-operator-judgement.md) | The three places the audit **declines to decide**: tier 1 verified-but-undecided (`O-A`–`O-J`), tier 2 confirmed-but-unadjudicated (`U1`, `U2`), tier 3 completeness-critic candidates (`G1`–`G22`). Plus the FU-1 ruling, recorded closed. | **34 rows** — 10 tier-1 (1 **CLOSED**, 9 open) · 2 tier-2 · 22 tier-3 (**18 superseded** by round 2 or already promoted; **4 residual limbs**) | **Three tiers, deliberately not merged.** Tier 1 = verified fact, unmade decision. Tier 2 = verified fact, **no** Algorithm verdict (none is invented to square a count). Tier 3 **never faced a refutation pass at all.** Collapsing them would destroy this file's only load-bearing property. |
| [`07-followups.md`](07-followups.md) | The spawned actions — round 1's `FU-1`–`FU-13` updated to the state of the tree, plus six round-2 additions `FU-14`–`FU-19`. Each carries an owner, a date, and the reason that date and not another. | **19 rows** — **4 closed**, 15 open · **7** residue rows carried from the closed four | Mixed; `(R2)` rows marked. **Six rows are mandatory outputs of the meta layer's `DEGENERATING` verdict**, not optional suggestions — each names the evidence limb it discharges. |
| [`08-hooks.md`](08-hooks.md) | Every **runnable** check: round 1's `H1`–`H25` re-executed at HEAD rather than carried on trust, `R1`–`R21` for the round-2 surfaces, `X1` (re-derive the counts) and `X2` (the section set is intact), and three **deliberately discarded** hooks with their reasoning. | **48** hooks (25 + 21 + 2) · **3** documented discards · **6** hooks repaired because they did not support their claim on first execution | **Executed, not asserted** — every fence was pasted from a terminal at `0af62ec`. Three hooks were found to be the exact trap they were written against: `H9` flipped green on a still-open finding, `R12` returns 17 where its ADR says *"Expected: empty"*, `R13` raises an IO error where it was written to print PASS. |

**Reading order if you have five minutes:** this file, then `02` (what is already closed), then `07` §7.2 (what is genuinely forced before 08-08). **If you are remediating:** work from `03` and `04`, honour `04`'s Handoffs block and `05`'s commit clusters so no file is opened twice, and re-run the relevant hook in `08` afterwards.

---

## §3 — Method, and the honest counts

**Round 1.** 12-domain parallel survey → adversarial refutation pass → The Algorithm (Question → Delete → Simplify → Accelerate) over survivors → completeness critic. All 12 domains returned results.
**Round 2.** The same pipeline over the **seven surfaces round 1 admitted it had not swept**: `.claude/`, `.cursor/`, `deploy/`, root docs + build files, `scripts/`, the `lab/analysis` RESULTS corpus, and specs/plans.

| | Raised | Refuted | Confirmed | CONFIRMED / PARTIAL | Severity | Adjudications |
|---|---:|---:|---:|---|---|---:|
| **Round 1** (12 domains, anchored `e031225`) | **192** | **41** (21.4%) | **140** | 65 / **75** — **53.6% of survivors were NARROWED**, not upheld as filed | 3 BLOCKER · 73 MISLEADING · 64 COSMETIC | **138** |
| **Round 2** (7 previously-unswept domains) | **124** | **12** (9.7%) | **110** | — | 0 BLOCKER · 50 MISLEADING · 60 COSMETIC | **110** |
| **COMBINED** | **316** | **53** | **250** | — | 3 BLOCKER · 123 MISLEADING · 124 COSMETIC | **248** |

**71 of round 2's 110 confirmed findings (64.5%) are AGENT-FACING** — consumed by an AI agent or an operator mid-task, where a stale instruction causes an **action** rather than merely misleading a reader. Concentrated in `.claude` (**23**), `docs` (**19**), `scripts` (**16**), `deploy` (**8**), `.cursor` (**4**). They carry their own section (`03`) and are pulled forward in the remediation schedule **regardless of severity label** — 35 of them are rated COSMETIC and are still in the early band.

### ⚠ The evidential-standing caveat — stated once, here, and not repeated per row

**Round 2's refutation rate (9.7%) is less than half round 1's (21.4%).** Two readings are available and **nothing in the data distinguishes them**:

* **(a) The round-2 surfaces were never swept before and are genuinely rot-heavy.** Supported by the fact that round 1's own completeness critic, independently and before round 2 ran, flagged `.claude` as its **single largest coverage hole** — and round 2 returned 23 agent-facing confirmed findings there, the densest single-surface concentration in the audit.
* **(b) Round 2's refutation pass was simply less aggressive than round 1's.**

**Round-2 findings therefore carry slightly lower evidential standing than round-1's.** That is the whole of the caveat. It is not hedged onto individual rows — where a round-2 row rests on a measurement, the command is given so it can be re-run rather than trusted, and the standing note is a reason to **verify a quote at HEAD before editing**, not a reason to discount the row.

### What the counts can and cannot be re-derived from

Hook **X1** in [`08-hooks.md`](08-hooks.md) mechanically re-derives the section set's row and verdict distribution — `03`'s declared 49 rows / 76 records / Algorithm split all reproduce **byte-exactly**. It **cannot** reach 316 / 53 / 250: refuted findings have no row, by construction, so the 53 leave no trace in the corpus. The combined headline is a property of the adjudication passes and lives here with its provenance. Anyone quoting an Algorithm distribution must say **which one** — round 1's hand tally (±2), `H15`'s round-1 floor of 92, or `X1`'s section-set floor of 194.

---

## §4 — The two disposition verdicts

Written **after** the diagnostics, per Trap #1. The prediction round 1 registered before its sweep — that the failure would concentrate in ADRs and briefs and be dominated by BLOCKER-severity false permission — was **wrong in both limbs** and is preserved rather than retrofitted. The ADR corpus turned out to be the *best*-corrected surface; the concentration is in instrument ledgers, rail-build artifacts, closure records, root-doc inventories and agent-instruction surfaces, and the severity distribution is overwhelmingly **labelling** rather than **permission**.

**The layers are kept separate on purpose.** Cross-layer citation is degeneration signal #6 in its own right and was enforced by construction in both rounds: no meta answer cites deployment state, venue facts, cap allocation, book σ, bust rates or P&L; no object answer cites gate-script behaviour or rule-text completeness.

### §4.1 Object layer — **STABLE**

**Tested against each verdict in turn.**

* **Not Degenerating**, on all three criteria. (1) *Belt-patches without independent corroboration:* **none** — every belt event in the window is measured (chain rate, mortality, path-death, bust, cost/side), and the single loosening (`K_eff = K_intrinsic + K_banked` → `K_eff = K_intrinsic`) carries a ratified ADR with its rationale and same-session propagation to its enforcement surface. (2) *Net-positive belt growth across consecutive audits:* **cannot be established** — no prior claim-estate tally exists, so the trend limb is unavailable and is **not asserted**. (3) *Methodology invoked to rationalize a decision already made:* **no** — the de-scope ADR names using itself to pre-empt the 2026-11-08 §4 falsifier as a **forbidden move**, and no artifact does so.
* **Not Falsified.** No pre-committed falsifier fired. Every locked risk constant holds at its locked value: `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40`, `TIER_MULTIPLIER` 1.00 / 0.50 / 0.25 / 0.00, and the G1 Part A/B thresholds (3.0% / 50% / 1.0%). **Zero numeric drift.**
* **Not Ambiguous.** The evidence is ample and one-directional.
* **Not Progressive**, and this is the substance. The de-scope is genuinely strong progressive evidence — a programme **abandoning a position at recorded cost** (*"$208/$700 sunk, first live fill never occurs and strands five threads"*) on measured grounds, rather than patching to preserve a conclusion, with the lifecycle axis explicitly not moved. `ORB-MNQ-1`'s payability target was ruled FALSIFIED the day before on the same discipline. **But the estate did not track the ruling:** **112 sites still assert the withdrawn configuration**, and the one certification the machinery produced about the sweep's own completeness over-claims what its instrument can test.

**The verdict's substance:** the object layer made a hard, correct, costly decision on measured grounds **and then did not carry it to the reading sites.** That is **maintenance debt, not epistemic degeneration** — and the distinction is operative, because the repair is a propagation pass, not a restructuring.

**One boundary was crossed deliberately** (FU-1's token-trade ruling, §5) — named as a crossing, reasoned, bounded to one operator-placed trade in one named week, and recorded at both sites where the constraint is read. Under this protocol that is the system working; the protocol's concern is *silent* crossing. **Four erosion tests are pre-registered** in [`01-diagnostics.md`](01-diagnostics.md) §3.5 so the next audit can test the claim rather than re-argue it.

**Watch conditions — any one converts the expected verdict to Degenerating at the next audit:** the 2026-08-08 gate runs against the uncorrected packet; a second scope decision lands before the 08-04 propagation completes; or the **P4** disposition gap is rolled forward at 08-08 without being recorded as *standing-unfalsifiable*.

> ⚠ **What `STABLE` does NOT say.** It is **not** a claim that the estate is clean. It is a claim about *epistemic conduct*. **250 confirmed misalignments sit underneath this verdict** — three of them BLOCKER, one of which (**B3**) would have reproduced a measured **1.91×** account-cap breach (MYM 76 + MNQ 77 = 153 micros against an 80 limit) at a successor venue had an implementer followed the declared spec chain. Stable means the repair is a propagation pass. It does not mean there is nothing to repair.

### §4.2 Meta layer — **DEGENERATING**

**Counter-evidence first, so this does not read as predetermined.** Rule 11 fired and **all six** sites its §6 downstream sweep enumerated landed correctly — verified. Rule 14 and gate 13 exist *because* two 2026-08-02 supersession incidents were converted into a mechanical check: the correct progressive shape, an incident becoming a gate. The pre-commit set is substantially green and genuinely binding. And the 2026-08-03 gate-stack audit's R-series repairs are dated **2026-08-08 and are not yet due**, so their non-execution is explicitly **not** counted here.

**Six grounds, all verified at HEAD and all independent of the above:**

1. **≥ 6 gates stopped binding with NO threshold ever moving — the sharpest result in the audit.** The third-leg **S5** cap table, **R1** σ ceiling and **S1 / S3 / S6** venue limbs; the **M1 4-session review trigger**; hard-core **P4**; and **Q-SIGID-1**'s §6 verdict rows all lost their subject when the legs were withdrawn. A falsifier check that reads *threshold values* returns all-green over every one of them. Worse, the failure is **two-sided**: the M1 trigger is **unreachable on its draw limb and trivially reached on its date limb** — it would "fire" on 2026-08-14 having sampled nothing. **The existing falsifier discipline has no form for either half.** `[R2]` corroborates on independent evidence from a surface round 1 never opened: **22 of 37** scripts in `scripts/*.py` are unwired or mis-scoped — the same shape (threshold intact, reach absent) arrived at by a different mechanism.
2. **Machinery is added faster than it is verified.** Gate 13 landed `c271411` 2026-08-03 12:49 and was rendered 93.2% non-binding by a reorganisation **nine and a half hours later** (`92abdbb`): it opens **5 of 73** declared files (6.8%) and prints an affirmative green line on every commit. Its companion test asserts corpus cleanliness over the same collapsed selector, with **no test pinning the selector** — the self-check inherits the defect.
3. **Gates that are structurally unable to catch what they were built for.** `check_skills_no_constants`'s `GUARDED_SKILLS` reads **4 of 21** agent surfaces and guards the four with the fewest constants. The de-scope ADR's own §10 sweep hook was **tested here** and cannot surface an untouched file — its exact pattern returns **0 hits** against the estate's most consequential stale artifact, and widening the file list was *measured* to change nothing. `skew_scan` returns `[]` from a registry that resolves to **zero live checks** and fails **open and silently**, so an empty result is indistinguishable from a clean corpus — and `[R2]`: its *documented* invocation `python -m ops.sentinel.scan` raises `ModuleNotFoundError` (canonical form: `PYTHONPATH=ops python -m sentinel`).
4. **A known-defective governance tool that caused a recorded incident is unrepaired, with no repair item.** `scripts/retire_adr.py:211-212` writes a false `Superseded-by` edge on `--reason withdrawn --by X`; the 2026-08-02 stub records in past tense that it did exactly this and was hand-corrected; `tests/test_retire_adr.py:146` exercises the reason **without** `--by`, so the failing invocation is untested. This is the one boundary crossing the audit found, and it is unbounded — any such invocation reproduces it.
5. **Belt is net +9 at 4 : 1, and 2 of the 3 removals did not propagate.** `scripts/validate_params.py` and `core/config/` are both absent from the tree while six live surfaces still cite them, and `REPO_MAP.md` §2.2 still publishes a runnable invocation of a module deleted 2026-08-02. **Second consecutive meta-layer audit** to find net-positive belt with near-zero effective prune — and `[R2]`'s 22-of-37 measurement says the effective ratio is worse than the tally credits.
6. **An ownerless class, an ownerless falsifier, and a false assurance claim.** The staleness class has **no owner**: doc discipline caught nothing across 120 object-layer findings in 24 hours, and every mechanical candidate is blind in a different direction — neither theory is winning and neither is scheduled to. `check_adr_graph --enable A7` returns **4 HARD findings** when run by hand, is excluded from `DEFAULT_ENABLED_CHECKS`, and appears in **zero** wiring files — unexamined since 2026-07-25. And `.github/workflows/skills-check.yml` describes itself as *"the pre-commit backstop"* while three hook items have no CI coverage of the real corpus — the belief that licenses `--no-verify`.

**Intervention is required, not optional.** [`07-followups.md`](07-followups.md) rows **FU-5, FU-6, FU-7, FU-8, FU-12, FU-13** — plus round-2 additions **FU-17** and **FU-18** — are the mandatory outputs of this verdict, each naming the limb it discharges. **FU-8 is the only one that stops recurrence rather than repairing damage.**

> ⚠ **What `DEGENERATING` does NOT say.** It is **not** a claim that the machinery is worthless — the counter-evidence above was *verified firing*, not assumed. It does **not** say any threshold drifted: **none did**, on either layer. It says the layer is **accumulating protective machinery faster than it verifies bindingness, and has left an incident-generating defect and an ownerless class unrepaired.** That is a shape warranting intervention. It is not a case for dismantling the belt, and no follow-up proposes removing a working gate — the meta follow-ups are **repairs to existing gates**, not additions, and §7 explicitly weighs "record it as accepted-unowned" as a legitimate outcome, because a ninth gate authored inside the audit that found the eighth unbinding is not obviously the right answer.

---

## §5 — Already FIXED or RULED — do not re-open these

Four items moved after the round-1 artifact was written. They are **committed**, and the section files reflect them rather than presenting them as open recommendations. A remediator sent at these files would be editing corrected text.

| # | What | Commit | What actually landed |
|---|---|---|---|
| **B3** | Reserve denominator `cap_firm` → `cap_alloc[leg]` — the highest-consequence item in the audit, and the **only one not de-scope-caused** (latent since the 2026-07-22 cap split) | `d84c5e4` | Fixed in **both** `docs/spec/c1_watch_realization_multiplier_layer.md` §2 and `docs/spec/c1_nt8_sizing_host_impl.md` §2.2, plus the normative **HALT** property, the constants gloss, and the worked check (**9/67 → 8/60**, the pre-split pair retained for provenance). **Production was already correct and was NOT touched** — the hook was never permitted to flip green by editing the host. Zero occurrences of the `cap_firm / (1 + …)` denominator form remain. **4 residue sites**, one live (`R-B3d`, an auto-loading agent skill). |
| **B2** | `STATE.md`'s published 08-08 rider-enumeration command under-reached | `a818b3f` | The under-reaching one-liner retired, replaced by the sentinel plus a named hand-check table. **Measured while fixing, correcting round 1's own account:** the published one-liner returns **33**; the sentinel returns **36**; **53** ADRs mention the date; the residue of **17** carries its duty in **prose with no trigger field**, of which **~10 are live obligations** and **FIVE are hard-core P-gates (P1–P5)** — the round-1 artifact said four. **Also discovered:** `python -m ops.sentinel.scan` as documented **throws** `ModuleNotFoundError`; the canonical form is `PYTHONPATH=ops python -m sentinel`. **2 residue items** — the durable additive-field fix is unratified and dated **2026-08-07**. |
| **B1** | The GO ADR carried no reader-intercept of the de-scope that spent its deployment limb | `ae5ffe7` | Reciprocal supersession edges between the GO ADR and the de-scope ADR (**DEPLOYMENT LIMB ONLY**), a dated **Addendum 2026-08-04** on the GO ADR, and the `RUNBOOK.md` Authority intercept. `check_adr_graph` passes — both header edits had to land in one commit or A2 hard-fails. The GO ADR went from **0 → 7** mentions of the de-scope. **§2, §4, §5 and all five prior addenda are byte-intact.** **2 residue sites.** |
| **FU-1** | The 2026-08-07 activity window — round 1's most time-critical item, which it **declined to act on** | `551d5c5` | **Operator ruling, verbatim:** *"We will not let the venue lapse. If no strategy has been found by Friday we will submit a token trade."* Primary path is a **deployed strategy**; fallback is **ONE operator-submitted manual token trade by 2026-08-07**, recorded as a deliberate override of the book-composition §5 forbidden move — **one trade, one named week, not a standing licence**. **The rail does not move** (`dry_run` stays `true`, M1 stays `CODE_LANDED`, no arming, no GO) and **no agent may place it**. ⚠ **The decision is closed; the act is still owed.** |

**A fifth commit is relevant but is not a fix.** `0af62ec` proposes [`docs/adr/2026-08-05-strategy-venue-binding-axis.md`](../../../../adr/2026-08-05-strategy-venue-binding-axis.md) — see §8.

---

## §6 — Coverage, stated honestly

**Round 1 swept 12 domains.** Object: root docs (`CLAUDE.md`, `STATE.md`, `PIPELINES.md`, `REPO_MAP.md`, `README.md`), the ADR corpus, open briefs / specs / pre-registrations / closure records, the rail-build artifacts, the instrument-ledger estate (`ops/instruments/`), lab RESULTS bodies (**sampled, not swept**), and the constants / envelope surfaces (`core/firm_rules.py`, `core/mc/preflight.py`, `core/dd_geometry.py`, `ops/prop_envelope_default.md`). Meta: `docs/operational_rules.md` Rules 6 / 7 / 11 / 14, the `scripts/check_*.py` gate set and its wiring (`Makefile`, `scripts/githooks/pre-commit`, `.github/workflows/`), `scripts/retire_adr.py`, the ADR-graph model and header vocabulary, `ops/sentinel/scan.py`, the ADR §10 runnable-hook convention, and `tests/governance/`.

**Round 2 swept the seven surfaces round 1 named as unswept** — `.claude/`, `.cursor/`, `deploy/`, root docs + build files, `scripts/`, the `lab/analysis` RESULTS corpus (round 1's sample became round 2's sweep), and specs/plans. **G9, the one candidate round 1 staked its direction claim on, graduated** — confirmed, not merely re-asserted.

**What remains unswept, and why:**

* **`lab/archive/` and `docs/ltm/` were EXCLUDED BY OPERATOR INSTRUCTION, not missed.** They are retired/archived by design and sit behind the repo's default search-ignore. **An empty result over those trees is not evidence of absence**, and a future reader must not record this as a coverage gap. Re-opening them is an operator decision, not an oversight to correct.
* **The object-layer belt-trend limb cannot be run at all.** No prior audit enumerated the *claim estate's* belt, so §3.2's object tally is this audit's own first construction and the protocol's "net-positive across ≥3 consecutive audits" test is **unavailable** on that layer. Stated rather than papered over — and it is why `STABLE`'s Degenerating limb (2) is recorded as *cannot be established* rather than as *passed*.
* **Four limbs are genuinely untested after both rounds** ([`06-operator-judgement.md`](06-operator-judgement.md) §5), and they share a property: **none is a file-anchored claim-alignment finding.** `R-1` turns on operator intent (not characterizable from an artifact); `R-2` was **RUN read-only and returned NULL beyond the known set — CLOSED**; `R-3` is a cross-artifact governance consequence that must be ruled with P4 at 08-08, not patched separately; `R-4` is a taxonomy proposal (a seventh failure class), **recorded and not adopted** — adopting it would itself be belt growth. **They are untested because nothing tests that shape, not because two rounds forgot to look.**
* **The `scripts/` estate was swept for claim alignment, but its dispositions are deferred.** `FU-17` carries the census (22 of 37 unwired or mis-scoped) and explicitly ships the number as a **floor**: 22 = unwired ∪ mis-scoped, and mis-scoped is not mechanically derivable.

### Known defects in this section set itself — recorded, not smoothed

* **One round-1 finding did not make the crossing.** **`M45`** (`lab/analysis/c1/c1_thirdleg_instrument_map_2026-07-27/RESULTS.md` — the K columns and the E-K / E-KCAP eliminations, `stale-figure`, `KEEP-CORRECTED`) is named twice in [`05-cosmetic.md`](05-cosmetic.md) as *"carried in the MISLEADING section"* and **has no row in [`04-misleading.md`](04-misleading.md)** or anywhere else. Its full text is retrievable at `git show 06caf3a:docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md` (round-1 §5.7). **It is owed a row in `04` §4.6**, and it should land in one commit with **C31** — same study directory, same missing-intercept class. That the loss occurred in a document *about* corrections landing in the wrong place is noted rather than dressed up.
* **Roughly 30 relative links inside `01`–`07` do not resolve** — the split moved every section one directory deeper and cross-references were carried at the old depth or written as if from the repo root. Measured by hook **X2**: 37 dead references before this file existed, of which 7 were the absent README. **The correct form from this directory is `../../../../adr/…`.** Fix them mechanically from X2's output; do not hand-verify 30 links. **Re-run X2 after this file lands** and expect `MISSING: []`, one self-referential section-ref hit in `08`, and the dangling section pointer in `05` — it names a `09-`-prefixed file that does not exist — repaired to [`06-operator-judgement.md`](06-operator-judgement.md) §3, where `U1` and `U2` actually live. **Executed after this README landed: `MISSING: []`, `EXTRA: []`, and 31 dead relative references — every one of them pre-existing in `01`–`08`. This file contributes none, and all 19 of its own outbound links resolve.**
* **This directory is gated by nothing.** `check_root_doc_liveness` resolves root-doc links only; `check_path_liveness` resolves MANIFEST parents only; gate 13 globs one level of `lab/analysis`. `X2` is the only check that reaches here, and running it is a manual discipline.

---

## §7 — What this audit does NOT license

**This section is operative, not ceremonial.** The Status line says *"recommendations pending operator ruling"*; this states exactly what that excludes, so a remediation pass reading only the Action cells cannot widen its own mandate.

**§7.1 — The frozen set. No finding in this artifact authorizes an edit here.**

| Surface | Verified at anchor | Why it is frozen |
|---|---|---|
| Locked strategy parameters — SL / TP / ATR / risk% / pyramid / session / BE / trail | unchanged | The parameter axis is immutable by charter; authorization is the separate revocable axis. Decay never authorizes editing these, and **venue-fit is not decay**. |
| Pine source (`**/*.pine`) | untouched | Canonical for strategy behaviour. No row in any section reads on Pine. |
| `core/dd_protection.py` — `DD_TRIGGER = 0.015`, `DD_SCALE = 0.40` | present | Change-control runs solely through pre-registration → re-MC → both-halves regime gate → admitting ADR. |
| `core/lifecycle.py` — `TIER_MULTIPLIER` 1.00 / 0.50 / 0.25 / 0.00 | present | The ratified Call-2 ladder. |
| Lifecycle state | `core/lifecycle_state.json` **does not exist** → both Striker keys default to `AUTHORIZED @ 1.00×` | ADR 2026-08-04 deliberately declined to move the axis and recorded why. **An audit that moved it would be executing the decision the ADR refused.** |
| `_BASE_RISK` / `BASE_RISK` allocations | unchanged | Lock lineage is ADR-borne (2026-04-17 baseline, 2026-05-23 re-allocation). |
| `LEG_MAP` and `cap_alloc` MYM **69** / MNQ **11** in `ops/c1_rail/c1_sizing_host_reference.py` | present | **B3 repaired the *spec* because production is correct.** Release-vs-retain of the withdrawn symbols and the allocation is **fork F2's**, not an editor's. |
| Frozen ADR §2 decision text, §4 falsifier tables, `[RATIFY]` lines, frozen pre-registration thresholds | unchanged | Trap #12. |
| Encoded `core/firm_rules.py` values | unchanged | A firm-rules value change needs an ADR **plus** the engine pre-flight — declined here (`O-G`, `O-H`). Rows touching `core/` are **comments and docstrings only**. |

**The most likely misreading, stated in full:** **B3 was a *specification* repair.** The spec was moved to production, never the reverse. Anyone who reads B3 as authorizing an edit to the sizing host has inverted it.

**§7.2 — Every finding is a recommendation, and none of the open ones has been applied.** The four items in §5 are the exception and say so. Where an Action cell reads as an imperative (*"Rewrite in place"*, *"Delete the field"*), the imperative is the **specification of the edit if the operator elects it** — written to that precision on purpose, because an unspecified cosmetic item is what becomes a MISLEADING one at the next sweep. **Precision of specification is not authority to execute.**

**§7.3 — DELETE means RETIRE WITH A TOMBSTONE, never silent byte removal.** Roughly a quarter of the adjudications are DELETE and the failure mode is a remediator reading the word literally. A DELETE is discharged only when **all four** hold: (1) **the bytes remain retrievable** — in git history at minimum, and at a named path where the repo's convention supplies one; (2) **the retirement is dated and attributed** — the date, the superseding event, the artifact that ruled it; (3) **a supersession record exists at the reading site**, per Rule 14, placed where the claim is *read*, not appended where the correction was *written*; (4) **what replaced it is named — or the absence is recorded as a decision.** *"Nothing replaces it"* is a legitimate outcome and must be written down as one. **DELETE never means "regenerate"** — dated bodies are retained *unregenerated* as the record of the prior regime.

**§7.4 — Dated bodies are never edited in place.** Session logs, closure notes, RESULTS bodies, frozen ADR §2 text, pre-registrations: **correct history** (Trap #12). Corrections land in addenda, amendment logs, or reader-intercept banners placed **above** the claim they intercept. Every proposed action in `02`–`06` respects this, and rows targeting such a file say so explicitly.

**§7.5 — Decisions this audit does not make.**

* **It rules no fork.** F1 (§4 reading of a de-scoped firm, 2026-11-08), F2 (rail disposition, 2026-08-08) and F3 (successor venue, 2026-08-08) are operator decisions with their own evidence. Every row touching a withdrawn symbol, the 69/11 allocation, the registered account or the rail's fate is written to say **retained-not-released** and to point at the fork. **A remediation pass that resolves any of them by choosing a branch has ruled a fork under an audit's authority.**
* **It does not reopen `ORB-MNQ-1`.** Its *payability* target is independently **FALSIFIED** (ADR 2026-08-03, §4 T2 FIRED, intraday-honest bust ≥ 67.67% against a 3.0% ceiling). Correcting a dead factual premise inside a closure **must not be executed as a re-nomination**; any unpark at a non-Tradeify venue needs a fresh GO **plus** a survivor-scoring pass first.
* **It does not re-scope the venue in either direction.** Tradeify remains 1 of the 4 firms in the frozen §4 falsifier set, and Tradeify-shaped *research* is expressly not barred by the same-day Addendum. Equally, nothing here elects a successor — F3's answer needs DP3's instrumented re-simulation, which is not run.
* **It licenses no real-money action and no arming.** The M1 arm interlock (`ops/c1_rail/c1_rail_arm.py::m1_acceptance_reason`) and the disarm-before-`armed_until` rule are unchanged and unqualified by anything here. **FU-1's ruling is the sole exception and its scope is one operator-placed trade in one named week** — not a B8 dry-fire, not a desk-card session, and **no agent may place it**.
* **It authors no new gate.** The meta follow-ups are **repairs to existing gates**. Deferred checkers are recorded **as decisions, not backlog rows**.
* **It does not retro-flip ADR 2026-08-04's ratified status.** The retro-fit question is raised and stopped there.
* **It does not discharge the 2026-08-08 obligation.**

---

## §8 — The structural answer, distinct from the per-site repairs

[`docs/adr/2026-08-05-strategy-venue-binding-axis.md`](../../../../adr/2026-08-05-strategy-venue-binding-axis.md) — **`Proposed`**, commit `0af62ec` — adds a **third orthogonal axis: BOOK → VENUE EDITION → DEPLOYMENT**, alongside the parameter axis (`LOCKED`) and the authorization axis (`AUTHORIZED → WATCH → RETIRED`), both of which are venue-agnostic.

**Why it belongs in this README rather than in a findings section.** Sections `02`–`06` repair **sites**. This repairs the **shape**. Venue facts currently have no owning level, so they settle wherever they were first written — and roughly a third of the MISLEADING rows are exactly that: a **venue fact stated at the book layer**, or a **deployment fact stated at the venue layer**. **B3 is the canonical case**: an account-aggregate venue fact (`cap_firm` vs per-leg `cap_alloc`) living inside a book-layer normative spec is invisible under a two-axis model and becomes a **visible layer error** under a three-axis one. That is a diagnosed failure mode converted into structure — the correct progressive shape.

**Three qualifications, all material.**

1. **It is `Proposed` and not in force.** Nothing in this section set treats it as binding, and **no remediation is gated on it**. Where an action re-homes a fact, prefer the level the ADR names; do not wait for it.
2. **A new axis is itself belt**, which the §3.2 tally does not yet carry and which the next audit must **price rather than assume** — the meta layer's first Degenerating limb applies to this ADR as much as to any gate.
3. **Its §4 `T1` is reachable this week.** T1 fires on any 1 occurrence of a venue-scope decision recorded **without** an edition-state transition, and **F2 on 2026-08-08 is exactly that shape of decision**. If ratification does not precede F2/F3, the ADR's only reachable falsifier this quarter passes untested.

**The per-site repairs and the structural answer are not substitutes.** Ratifying the axis corrects no existing sentence; landing the propagation pass prevents no recurrence. `FU-8` — re-keying the ADR-authoring template's Phase-2 sweep to the **pre-decision configuration's** vocabulary rather than the decision's — is the third leg, and it is the only follow-up in the register that stops recurrence rather than repairing damage.

---

**Predecessor.** The round-1 artifact at [`../2026-08-05-post-descope-claim-alignment-audit.md`](../programs/2026-08-05-post-descope-claim-alignment-audit.md) is a stub pointing here; its content is preserved and extended in this directory (see §6 for the one named exception). Its full original text is retrievable at `git show 06caf3a:docs/notes/audits/programme-audit/2026-08-05-post-descope-claim-alignment-audit.md`.
