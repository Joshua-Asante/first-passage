# State-policy scoring — Q-EVALSEQ-1 un-dorm review (Board packet)

**Status:** `CLOSED-RESOLVED (P2 RUN + COMMISSION-FRONTIER)`
**Authored:** 2026-08-16
**Closed:** 2026-08-16
**Mark:** P2 — operator (JA) 2026-08-16 ("P2 + GO"). §6 table frozen (Trap #12). The conditional §7 b5 recommendation was elected with the mark: renew once with corrected wake conditions.
**Closure:** [STATE-POLICY-closure-resolved-p2](closures/STATE-POLICY-closure-resolved-p2.md)
**Authors:** Claude Code (recorder) — operator marked P2
**Parent:** [Q-EVALSEQ-1 pre-registration](pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) (frozen 2026-07-24; DORMANT 2026-08-04) · [S1 environment ratification](../adr/2026-08-07-loop-s1-environment-ratification.md)
**Loop:** Inquire-light Board packet — presents elections only. $0 · K=0 · nothing runs here · no arming · no deployment implication.
**Artifact path:** `docs/briefs/2026-08-16-state-policy-scoring-review.md`

---

## §0 — Rule 0 reads (this session @ `c89f261`, 2026-08-16)

| Path | Anchor | Supplies |
|---|---|---|
| [Q-EVALSEQ-1 prereg](pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) | `027a729` 2026-08-14 (public-release squash — freeze/stamp dates carried in the file header; pre-squash lineage in the frozen archive) | Frozen K=4 policy family (a) flat 0.50× control (b) linear decay 0.75×→0.25× (c) floor-distance-proportional, capped 0.75× (d) step-down-at-cushion; §6 binary gate; header: "DORMANT 2026-08-04 — not on the 08-08 slate (venue de-scoped; 'within-eval' has no eval)"; "re-usable at an F3 venue"; frozen body byte-unedited |
| [`core/dd_protection.py`](../../core/dd_protection.py) | line 198, read this session | lifecycle factor "MULTIPLIES against BASE_RISK/DD_SCALE — it never edits them" — a schedule is a fourth multiplicative risk_pct-layer factor, not a constant edit |
| [`lab/discovery/prop_survivor_scoring.py`](../../lab/discovery/prop_survivor_scoring.py) | lines 47–50, read this session | "dd_protection OFF for scoring"; `NO_PROTECTION_TRIGGER = 10.0` — every survivor-scoring run to date is constant-policy |
| [`lab/research_utils/nsurv_channel.py`](../../lab/research_utils/nsurv_channel.py) | line 24, read this session | N-SURV consumes a series "already at the sizing under test" — no policy layer exists in the channel |
| [`STATE.md`](../../STATE.md) | `fd251e3` correction | Queue row 2: "Eval live; no book deployed"; the five stranded threads re-framed as gated on "an acceptable strategy, not a missing venue" |
| [b5 PARK record](../pursuits/b5-q-fundpol-1.md) | read this session | Q-FUNDPOL-1 (the §7 funded-phase fork) expires to SUBTRACT 2026-11-08 absent renewal — **not marked here**, see §7 |
| [book-comp campaign dir](../../lab/analysis/c1/tradeify_book_composition_2026-07-23/README.md) | `ls` this session + `git ls-tree pre-prune-2026-08-08` | ⚠ Reachability changed since the prereg's attestation: `gap_stage*.py` and `out/` absent from both working trees (README layout rows stale); `inputs/` (4 CSVs) present in the main checkout; the full harness (`gap_stage1.py`–`gap_stage4.py`) is retrievable in-repo at tag `pre-prune-2026-08-08` (verified this session) and `out/daily_panel.csv` must be regenerated from it — panel span 2020-08-04 → 2026-07-21 per [Q-FUNDPOL-1 verdict prereg](pre-registration/Q-FUNDPOL-1-verdict-preregistration.md) panel-provenance block |
| [population note §6.5](../notes/notice/N-2026-08-13-external-eval-population-data.md) | present on this tree | Tradeify FTA "consistent trading sizes" flagged "Not a safe harbour" — binds live deployment of size variation, not scoring |

**Amendment-first (sub-rule 10).** Dormancy owner is the prereg's own header stamp (2026-08-04), whose authoring ruling is [claim-alignment M31](../notes/audits/programme-audit/2026-08-05-claim-alignment/04-misleading.md) — the header-stamp amendment vehicle P1 reuses. No sibling un-dorm packet exists. Executed dedup:

```
$ grep -rn "Q-EVALSEQ" docs/briefs/INDEX.md lab/CATALOG.md docs/rejected_candidates.md STATE.md
(empty — no INDEX / CATALOG / rejected-registry / STATE row exists)

# Known other homes (repo-wide grep, verified this session — none is an un-dorm packet):
#   docs/briefs/2026-07-17-0808-packet-delta-and-sequence.md        (struck-DORMANT slate row)
#   docs/notes/audits/programme-audit/2026-08-05-claim-alignment/04-misleading.md  (M31/M33 — the stamp's authoring ruling)
#   docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md + its verdict prereg  (the §7 fork)
#   lab/analysis/c1/eval_shape_diagnostics_2026-07-28/RESULTS.md    (cross-reference only)

$ grep -rln -iE "policy-augmented|state-dependent sizing|cushion-proportional|front-load" docs/briefs/ docs/adr/ docs/spec/
docs/briefs/closures/Q-FUNNEL-1-closure-resolved.md          (attempt-level policies — scored 2026-07-22)
docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md      (unrelated)
docs/briefs/pre-registration/2026-07-24-...-preregistration.md  (the subject)
docs/briefs/Q-FUNDPOL-1-funded-phase-policy-inheritance.md   (the §7 fork — dormant, PARKed)
docs/briefs/rnd-pipeline/Q-FUNNEL-1-contract-funnel-ev-scoping.md
docs/adr/2026-05-28-audit-doc-generation-doctrine.md          (unrelated)
docs/spec/2026-08-02-tradeify-activity-rule-disposition-spec.md (unrelated)
```

**Cheap falsifier (parent-side, generous).** If any within-attempt state-dependent policy had ever been scored on Tradeify eval geometry, this packet would be a re-derivation. Checked: Q-FUNNEL-1 scored *attempt-level* policies (no_retry vs retry_to_cap) — a different layer; the FXIFY-era C2 sweep scored the DD_TRIGGER→0.40× rule on *static-DD* geometry — a different barrier. **No within-attempt policy has ever been scored against the trailing-DD eval.** The packet stands.

---

## §1 — Context

Every N-SURV / Part-A survival number the estate has ever produced is a **constant-per-trade-risk** number with dd_protection deliberately disabled (§0 rows 3–4). The venue's own passer population operates attempt-retries (population note §2: median 3 evals per passing participant); the size-scheduling half is second-hand but recorded — the eval-sprint derivation quotes the population evidence as *"oversize during evals and size down once they get funded"* ([eval-sprint note §5](../notes/notice/N-2026-08-13-eval-sprint-lane-derivation.md), reader-summary grade, disclosed as such). The estate's only chartered instrument for measuring the within-attempt half of that lever — Q-EVALSEQ-1's frozen K=4 schedule family — went DORMANT 2026-08-04 with the venue de-scope, on the stated ground that "'within-eval' has no eval."

The stamped ground no longer holds for the eval-as-environment: S1 (2026-08-07) ratified the incumbent `Tradeify_Select_100K` eval as the environment for new strategies, and STATE now records "Eval live; no book deployed" (§0 row 5). The stamp's re-use clause contemplated an F3 successor venue that S1 declined, and the frozen subject (the 2-leg Striker book) stays deployment-barred at the incumbent — so the dormancy ground has lapsed **under the lever-diagnostic reading this packet adopts** (measure the scheduling lever on the panel; deploy nothing), and that reading vs. the deployment reading is exactly what P0-vs-P1 elects. Scoring requires no venue re-open, no arming, and no Striker re-entry: it is a simulation on the book-comp panel.

**What a run would and would not establish.** The frozen family's subject is the 2-leg Striker book — barred from deployment. A PASS therefore does **not** admit anything; it measures whether the within-attempt scheduling **lever** is real on this venue's geometry (the prereg's own §4: a passing lift "promotes the question to a sizing-policy Pre-Q (not an auto-adopt)"). If the lever is real, every future candidate's admissible region widens without moving any frozen threshold — the diagnostic value is candidate-independent. If it is falsified, the lever is spent and the constant-policy N-SURV numbers stand as the honest ceiling.

**Honest prior (carried from the prereg §2):** weakly negative for eval-pass — the flat-multiplier sweep degraded monotonically; the schedule's late-de-risk asymmetry is the only reason it could net positive where flat-up did not.

---

## §2 — Prior art / lineage

- [Q-EVALSEQ-1 prereg](pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md) — the subject; frozen 2026-07-24, DORMANT 2026-08-04.
- [Q-FUNNEL-1 closure](closures/Q-FUNNEL-1-closure-resolved.md) — *attempt-level* policies scored (no_retry vs retry_to_cap), CLOSED-RESOLVED 2026-07-22; its §7 cushion-proportional day-policy layer explicitly "not opened."
- FXIFY-era C2 sweep ([`core/dd_protection.py`](../../core/dd_protection.py) header) — the DD_TRIGGER→0.40× rule adopted by MC on *static-DD* geometry; not the trailing-DD eval.
- [Q-FUNDPOL-1](Q-FUNDPOL-1-funded-phase-policy-inheritance.md) — the funded-phase §7 fork; frozen, never run, PARKed (b5).
- [Two-barrier first-passage track](../methodology/two_barrier_first_passage_track.md) — chartered 2026-08-13, Session 1 unstarted; constant-policy theory.
- [Eval-sprint lane derivation](../notes/notice/N-2026-08-13-eval-sprint-lane-derivation.md) — the *declined* eval-sprint lane (2026-08-13); distinct from this packet, see §5.

---

## §3 — Question

**Symptom-only:** the estate's only chartered within-attempt policy instrument is dormant on a venue ground that no longer holds, while every survival number feeding the 2026-11-08 §4 reading is constant-policy; what does a Board mark do with that dormancy?

---

## §4 — Falsifiable hypothesis

**H:** this packet presents exactly three live elections (P0 KEEP-DORMANT / P1 RUN-AS-FROZEN / P2 RUN + COMMISSION-FRONTIER) and does not itself run the MC, edit the frozen family, recommend a schedule, or imply any deployment; a later operator mark under §6 is the only close.

**Reject H if:** any MC fires from this packet before a mark; the K=4 family is edited or extended here; a schedule is recommended here; the packet is read as Striker re-entry, arming, or an N-SURV admission for any candidate.
**Accept H if:** operator marks P0, P1, or P2 under §6.
**Ambiguous-hold if:** operator defers with a dated hold (dormancy stays).

---

## §5 — Forbidden moves (this packet's output)

- **Run before the mark.** The prereg's own §5 names run-early as the pre-registration-defeating move; a mark of P1/P2 is the gate token its lapsed "08-08 slate" line requires.
- **Edit the frozen K=4 family or add a fifth policy.** Byte-unedited body is the prereg's standing condition; an un-dorm is a header stamp, never a §6 edit (Trap #12).
- **Recommend a schedule.** This packet, like the prereg, endorses no `S*`.
- **Read P1/P2 as deployment, arming, or Striker re-entry.** De-scope clauses 1–2 and the redeploy bar stand; scoring is simulation on a panel.
- **Credit the funded floor-lock to eval pass.** Prereg §5, carried verbatim.
- **Conflate with `Q-ORB-SIZE`** (level-on-parked-ORB — sibling, distinct) **or with Q-FUNDPOL-1** (funded-phase fork — §7).
- **Treat a scoring PASS as clearing the FTA "consistent trading sizes" surface for live use.** That compliance question is live-deployment-scoped and stays open (population note §6.5).
- **Read P2 as the declined eval-sprint lane.** The eval-sprint lane (declined 2026-08-13; "Do not open the eval-sprint lane," slate-2 design box) oversizes above the frontier to buy pass-speed; P2's policy-value map leaves bust ≤ 3.0%, every admission gate, and retry economics untouched — policies only redistribute risk at or below the flat baseline.

---

## §6 — Gate (operator marks one)

| Verdict | Trigger | Disposition |
|---|---|---|
| `RESOLVED` (P0 KEEP-DORMANT) | Operator marks **P0** | `STOP` — dormancy stands; the 2026-11-08 §4 reading inherits constant-policy survival numbers only; re-raise needs a new ground, not a re-argument |
| `RESOLVED` (P1 RUN-AS-FROZEN) — **recommended, not marked** | Operator marks **P1** | `INTEGRATE` — un-dorm stamp lands on the prereg header (frozen §6 body untouched); one session recovers the pruned `gap_stage*` harness from the archive lineage, extends it with the four frozen policies, and runs the bounded MC on the incumbent geometry; verdict per the prereg's own frozen §6 (RESOLVED adopt-eligible / FALSIFIED lever-spent / AMBIGUOUS power-short), DSR/placebo at read, both-halves split |
| `RESOLVED` (P2 RUN + COMMISSION-FRONTIER) | Operator marks **P2** | `INTEGRATE` — P1, **plus** commissions (names, does not open) a fresh measurement-only campaign extending the [seed-target frontier](../../lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/RESULTS.md) with the same four policy shapes on synthetic `(w, b, r, k, d)` seed geometry — a candidate-independent policy-value map; fresh brief owed before any run; $0, no manifest |
| `FALSIFIED` | MC fired from this packet pre-mark; frozen family edited; schedule recommended; packet read as deployment | `STOP` — repair the process defect |
| `AMBIGUOUS-HOLD` | Dated deferral | `ITERATE` — re-open this packet on the hold date; dormancy stays |

**This draft elects none.**

---

## §7 — Forks (named, not marked here)

- **Q-FUNDPOL-1 PARK expiry (b5)** — converts to SUBTRACT 2026-11-08 absent explicit renewal; its own record says a successor venue needs "a fresh derivation, not this brief rescheduled," and its re-entry condition (F3 successor) is stale relative to S1's no-migration ruling. Renewal-vs-lapse is a **separate** mark riding the GSUB-1 2026-11-08 slate — flagged so the expiry is elected, not defaulted.
- **Two-barrier first-passage track Session 1** — chartered 2026-08-13, unstarted; constant-policy theory (stop/target hit-probability). Complementary, not a substitute; no mark here.
- **Funded-phase schedule** — stays with Q-FUNDPOL-1 (the prereg's own §7 boundary).

---

## §8 — Verdict pre-registration

No separate pre-reg file. The §6 mark table is **frozen at this packet's commit** (MSL-S7 / dense-1m precedent). Trap #12: do not amend §6 to match a later mark. Each mark closes via a `docs/briefs/closures/STATE-POLICY-closure-*.md` record carrying the typed `## Iterate` block; on mark, this header gains `Mark:` / `Closed:` / `Closure:` fields as the dense-1m packet's did.

---

## §10 — Audit hooks

```bash
# Dormancy stamp is still the prereg's only status (pre-mark state):
grep -n "DORMANT 2026-08-04" docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md

# Constant-policy scoring invariant (should hold until a P1/P2 run lands a policy layer):
grep -n "NO_PROTECTION_TRIGGER = 10.0" lab/discovery/prop_survivor_scoring.py
grep -n "already at the sizing under test" lab/research_utils/nsurv_channel.py

# Frozen constants untouched by any P1/P2 run (axis-separation):
grep -n "DD_TRIGGER = 0.015\|DD_SCALE = 0.40" core/dd_protection.py

# Post-mark expected (P1/P2): an un-dorm stamp on the prereg header, §6 body byte-identical:
git log --oneline -2 -- docs/briefs/pre-registration/2026-07-24-2leg-eval-frontload-schedule-preregistration.md

# b5 expiry not silently defaulted:
grep -n "expiry" docs/pursuits/b5-q-fundpol-1.md
```

## Verification

```bash
python scripts/check_brief.py docs/briefs/2026-08-16-state-policy-scoring-review.md --type inquire
```

§0 lists production paths with session anchors incl. the two constant-policy code lines ✓ · §4 H + reject/accept, binary ✓ · §5 moves genuinely tempting (run-early; extend family; recommend; read as deployment) ✓ · §6 marks binary with dispositions ✓ · §3 symptom-only ✓ · §10 runnable ✓ · reachability change (pruned harness) disclosed, not papered ✓.
