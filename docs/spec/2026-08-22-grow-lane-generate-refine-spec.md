# SPEC: GROW — deep-iteration lane extension: automated grammar engine + synthetic calibration harness

Status: Part A `Accepted` — [build-authorization ADR](../adr/2026-08-22-grow-lane-build-authorization.md),
operator GO 2026-08-22 ("ratify, accept, and begin the build"); Part B resolved and ratified as
[`2026-08-22-grow0-two-ledger-k-question.md`](../adr/2026-08-22-grow0-two-ledger-k-question.md)
`Accepted` · $0 · K=0; Part A rides the charter's already-licensed §7 steps 2–4,
campaign-gated as the charter requires · depends:
[deep-iteration lane charter](../adr/2026-08-16-deep-iteration-lane-charter.md) `Accepted`
(**owner**) · [F3 attestation-library spec](2026-08-22-eval-lock-geometry-attestation-library-spec.md)
`PROPOSED` (pooled-scoring dependency)

**Review (why v2 exists):** v1 (merged via PR #96 at `a02126f`) proposed a sibling "GROW lane"
with decision points D1–D3. Same-day dual adversarial review — gate-reachability audit
**BLOCKED-AT-FREEZE**; pre-ratification panel **BLOCKED, do not ratify D1–D3** —
[full findings](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md). **D1–D3 are
withdrawn.** The Accepted charter owns the refinement thesis (v1 was an amendment-first miss:
its dedup search was never executed); D3's "reserved-but-unread CONFIRM windows" class is
empty (the shared CON window was read 2026-08-20; CON-5 carries an unread-forever election;
the dense-1m pause is lane-wide); D2 contradicted EM0/TNEC-1/S6 and the blind-channel split
clause with none of those owners in its supersession list.

Executed dedup / amend-first (Rule 8.8/8.10 — pasted, not attested):

```
$ grep -rlniE "deep.iteration|iteration lane|--lane deep" docs/adr/ docs/spec/ docs/briefs/pre-registration/
docs/adr/2026-08-16-deep-iteration-lane-charter.md
docs/adr/INDEX.md
docs/briefs/pre-registration/2026-08-16-deep-lane-dl1-mgc-orc-prereg.md
$ grep -in "grow" lab/CATALOG.md docs/briefs/INDEX.md | grep -iv growing
(no output — no GROW prior)
```

Owner found: the charter. This packet docks there and adds **no sourcing channel, no counter,
no clock** (the N=3 third-door discipline is not re-engaged).

Objective: equip the Accepted deep-iteration lane with a machine-generated variant-roster
engine and a synthetic calibration harness (GROW-0), so lane campaigns can be grown by
automation **at the charter's own declared-K discipline (K ≤ 33, fully counted)** — and name,
without proposing, the two-ledger K question that would have to be ratified before any wider
automation.

Origin: operator thesis 2026-08-22 (session record) — Striker/Aegis were filtered and sized
into profitability from seeds that would not have passed intake raw. Charter §1 already
ratifies the disciplined form of that thesis; this packet supplies the automation. Record,
stated precisely: one generated admission since 2026-07-16 (ORB-MNQ-1, later
payability-falsified at the venue), none since; the zero-yield streak among generation
campaigns continued through the MSL slate and DL-1 (all 10 variants net-negative on TRAIN;
abandonment 1/2 on the charter's counter). Sizing-policy motivation carries its label:
cushion-proportional sizing's bust 20.18% → 0.00% (Q-EVALSEQ-1) is an **EOD-clock lower-bound
figure**, and the 2026-08-17 intraday-honest remeasure (Q-POLFRONT-1 fork) collapsed the
related 5.107× headline — sizing operators stay in the grammar, scored intraday-honest only.

## Part A — engine + harness (no doctrine change; hosted by the charter)

Steps:

1. **Rule 0 (implementer, before any build).** Read in full: the charter (incl. §4 counting
   machinery + the DL-1 record), blind-channel ADR L208 (the split clause Part B would
   challenge), EM screen §2.0b + §8 change control, TNEC-1, Route B checklist,
   the dense-1m spec's two reader-intercepts, the
   [dual-panel audit note](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md),
   `prop_survivor_scoring.py` + the 2026-07-13 survivor-scoring prereg, the F3 spec.
2. **Grammar engine** (charter §7 step 2 — `--lane deep` on `register_search`, already
   licensed): the campaign prereg freezes an operator grammar — enumerated mutation-operator
   families over entry/filter conditions, exit/stop geometry, and sizing policy (flat +
   cushion-proportional included) — plus a generation budget **G**. **K = G, fully counted**
   ("every variant available to be chosen counts", charter §2.2 imported verbatim; adaptive
   generation is fine — the budget, not the enumeration, is what freezes). All three charter
   conjuncts computed and shown at freeze: K ≤ 33 · `floor_at_k(K, confirm_years)` ≤ 2.0 ·
   power ≥ 0.50 against the named design-target edge. `grammar.json` committed at G0, SHA256
   pinned in the prereg, hash recomputed at every run start, stamped into every emitted row.
   Iteration reads TRAIN only; one survivor by frozen nomination rule; confirm read once.
   `--lane deep` gets its own admission function implementing the charter §2.2 predicate
   (S6's mechanism-first path refuses K ≥ 4 by design and is not loosened — charter §2.2's
   "measured demand replaces the prior" is lane-local).
3. **Scoring discipline in the engine:** costs bound **per instrument** via the cost_model
   discipline, never the $0.91/$0.95 index literals (MGC/MCL run $1.06/$1.10 actual). Fitness
   is intraday-honest only: hard limbs coded, including **N-ACT** (≥ 1 trade per Mon–Fri week
   over a window frozen at G0) and N-SHAPE (flat-by-16:00 ET, no pyramiding,
   micro-expressible); integer sizing scored under N-SURV/N-SIZE. Every fitness term
   clock-tagged; construction raises on `clock='eod'` (⚠ `score_candidate`'s default path
   omits `intraday_blocks` — wire non-vacuously and run
   `assert_intraday_channel_nonvacuous` per campaign). Eval-geometry patching per the F3
   attested pattern: per-worker attestation dicts into the manifest; a non-singleton attested
   set hard-fails (M-23 shape). SPA/StepM thresholds named in each prereg (W4 re-arm at K > 3,
   charter §2.6); the engine emits the full K-variant TRAIN return matrix so SPA is computable.
4. **GROW-0 — synthetic calibration harness.** Engine validation, **not a lane campaign**: it
   is filed outside the charter's §4 counters — a placement this packet's ratification must
   rule explicitly, not assume. Three limbs, built RED-first:
   - **Limb A (power):** a planted DGP with net-positive intraday edge above the per-instrument
     cost floor; the loop must recover it on TRAIN and its survivor must clear the sealed
     synthetic segment at the frozen confirm bar.
   - **Limb B (calibration):** N pure-noise panels (magnitude-matched surrogates — Q-NSURV-2's
     wrapper cited as implementation style only); full pipeline per panel; sealed-segment
     clear-rate must sit at/below the frozen adjusted-α binomial envelope. **N is sized in the
     GROW-0 PREREG for ≥ 0.80 power against leakage ≥ 3× nominal α** — the bare ≥ 20 floor
     (~13–35% power) is insufficient and is not the test.
   - **RED rigs, all three on record:** a deliberately leaking pipeline (Limb B must fail), a
     powerless loop (Limb A must fail), a parent-only patch (attestation must fail).
   Machine-readable `limb_a` / `limb_b` / `red_*` tokens with nonzero exit on any FAIL;
   harness retries ledgered.
5. **Enforcement build manifest** (audit repairs — every gate names a mechanical executor;
   per-gate detail in the audit note and the workflow record):
   - campaign manifest schema: frozen K/G, grammar SHA256, `sealed_consults[]`, per-worker
     attestations; a `grow_ledger_check` exits nonzero on any unledgered or duplicate sealed
     read;
   - real-panel scoring refused without `--predecessor-verdict` naming GROW-0's filed
     RESOLVED closure (`bind_real_k` lifts only behind it);
   - survivor DSR scored at the **full declared K** with `universe_gate` verdict propagated to
     exit code, plus a k=3199 RED rig;
   - charter §4 counting machinery mechanized: a streak checker walking lane closures against
     the ADR 2026-08-16 zero-yield classes, maintaining the charter's running-count line —
     discharging the charter's own "without this, the limbs are unbinding" note;
   - door-check limb in `gates.yml`, path-conditional on deep-lane campaign dirs, requiring an
     **exit-1** `instrument_profiles.py cell` consult record (T3 ruled pre-emptively satisfied
     by the audit). A FATAL exit-2 proves execution, **not consultation** — MECHANISMS.md
     declaration + profiles build land in a commit before the consult. Adjacency consult of
     the nearest registered family for every new grammar family name (parked-not-DEAD cells
     escape DEAD-list attestation). Correct `rejected_candidates.md`'s stale tier=always
     claims (the gate is path-conditional on `^ops/instruments/`);
   - `discovery_manifests/burned_segments.json` consulted at every open — the shared CON
     window (MNQ, 2025-09-01→2026-08-05) enters it as **burned** (read 2026-08-20);
   - LOCKED-leg denylist: no Striker identity reused as a lineage ID; no redeploy;
   - Rule-0 anchor checker on each prereg §0.
6. **Domain bars, named per campaign (never a default discharge):** charter §2.1's non-index
   default avoids the index raised bar entirely. A campaign that elects an index-intraday cell
   must answer `index-intraday-ohlcv-directional-timing-2026-07-21` by a route it can show:
   route ③ (beats-incumbent-ORB-MNQ net-of-cost) **requires an explicit frozen
   incumbent-comparison term in confirm scoring** — nothing at HEAD computes it (v1's "already
   scores" claim was false), the incumbent basis on record is always-MNQ ORB +5.19 bp
   (`rejected_candidates.md` cross-index entry), and the 2026-08-10 falsifier LOG records
   route ③ as "a *results* bar — unclearable ex ante, by construction" (so only a wired
   comparison term, never a PREREG promise, can discharge it) — or route ① under the 2026-08-10
   temporal-selectivity ruling where its §2-B conditions hold. The EOD-adversity raised bar
   (2026-08-02; + ADR 2026-07-31 §5's 15:30-exit bar) binds the grammar's exit-geometry
   construct class yet sits in zero profile ledgers: register it in the index profile ledgers
   AND answer it in PREREG §0 wherever exit-geometry operators are enabled. Standing pauses
   attested per charter §2.1 — including the dense-1m temporal-selectivity pause (lane-wide
   unconditional as of 2026-08-20) and CON-5's unread-forever election.
7. **Campaigns are ordinary deep-lane campaigns** — charter Q-IDs, counters, prereg GOs,
   confirm-read GOs, falsification budget all apply unchanged; this packet adds tooling, not a
   channel. Rescue of a rejected family is already possible under charter §2.1: a campaign
   whose prereg clears that family's own re-proposal bar in writing; anything barred by a
   closure election takes the U1-style per-seed override ADR path. **No blanket exception
   exists; v1's D3 is not licensed by anything.**

## Part B — the two-ledger K question (named only; not proposed here)

The claim v1 called D2 — that for a statistic computed on a sealed segment the search never
touched, the chargeable K is the number of sealed consultations (M), not the generation width —
would supersede in part **five owners**: blind-channel ADR L208 ("Splitting is a bias control,
not a K control"), EM0 §2.0b's K_eff = K_intrinsic identity + EM screen §8 change control,
TNEC-1 N-EDGE's `floor_at_k(K_intrinsic)`, S6/`admission_schema.py`'s landed refusal
semantics, and charter §2.2(i)'s K ≤ 33. It is **filed only if GROW-0 Limb B RESOLVES at its
pinned power**, and then as its own full-tier ADR carrying all five Supersedes-in-part lines,
the Limb-B measurement as evidence, and a cross-campaign sealed-consultation accounting rule
(fresh confirm budgets on finite cached data are currently unpriced). Until such an ADR is
Accepted, **every campaign under this packet counts full K ≤ 33** and nothing in Part A
depends on Part B.

Gate: RESOLVED if GROW-0 passes Limb A ∧ Limb B at the PREREG-pinned power with all three RED
tokens `FAILED_AS_EXPECTED` on record and machine-readable limb results — resolving this
packet (engine + calibration instrument sound; Part B's filing decision then goes to the
operator). FALSIFIED if, after the RED controls run green-side, Limb A fails, Limb B exceeds
its envelope, or any RED control passes — the engine is defective; a fix re-runs GROW-0 under
a fresh ledgered PREREG, and Part B is not filed. Campaign outcomes belong to the charter's §4
counters, not to this Gate.
Boundary (each genuinely tempting): no campaign above K = 33 and no under-counted K pending a
ratified Part-B ADR · GROW-0 sits outside charter §4 counters **only if this packet's
ratification says so in writing** · no read of the burned CON segment and no v1-D3 rescue
moves (charter §2.1 bar clearance or per-seed override ADR are the only doors) · no EOD-clock
fitness term · no new sourcing channel/counter/clock · `--lane blind` is never the GROW open
path (blind opens are unbound by design — `register_search.py:357-360`) · no deploy, no Pine,
no arming, no `LEG_MAP` claim · charter §5 forbidden moves apply in full.
Reads (verified 2026-08-22 at branch HEAD `0815bba`): charter @ `85a83ba` (§2 discipline; §4
counters incl. DL-1 ABANDONED 1/2) · blind-channel ADR @ `85a83ba` (L208) · EM screen @
`85a83ba` (§2.0b; §8 L288) · TNEC-1 @ `85a83ba` · `lab/discovery/admission_schema.py` @
`85a83ba` (L61, refusal path) · `lab/discovery/register_search.py` @ `4028be7` (L357–360
blind-unbound residual; L388 `_require_admission`) · CON-4 + CON-5 closures @ `6545ad5`
(burned shared window; unread-forever election; lane-wide pause) ·
[Route B checklist](../methodology/avenue_a_generate_confirm.md) ·
[survivor-scoring prereg](../briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md)
@ `85a83ba` (frozen gate: bust ≤ 3.0% ∧ P(pass) ≥ 50%; the intraday-honest qualifier arrived
via W1/TNEC-1) · W4 dormancy ADR @ `85a83ba` (re-arm condition) · F3 spec ·
[dual-panel audit note](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md) (this
change-set) ·
[2026-08-10 falsifier LOG](../../lab/analysis/c1/cheap_falsifiers_2026-08/_cheap_falsifier_cost_geometry_2026-08-10_LOG.md)
L78 @ `85a83ba` (route ③ = results bar, unclearable ex ante; the prior STATE decision-index row
was collapsed by the 2026-08-22 nav pass — cite the LOG, not STATE) ·
`docs/rejected_candidates.md` cross-index entry (+5.19 bp incumbent basis) · Q-EVALSEQ-1 /
Q-POLFRONT-1 closures (EOD-clock bounds; 2026-08-17 remeasure)
Verify (Phase-0, implementer runs before build): `grep -n "Status:" docs/adr/2026-08-16-deep-iteration-lane-charter.md`
(expect `Accepted`) · `grep -n "Running counts"
docs/adr/2026-08-16-deep-iteration-lane-charter.md` (current counters before any campaign) ·
the charter §10 floor command (expect `1.0 0.95 1.475 2.09`) · after declaring a family in
`MECHANISMS.md` + profiles build: `python scripts/instrument_profiles.py cell <SYM> <family>`
(expect **exit 1 with BINDING BAR lines** — an exit-2 FATAL proves execution only, never
consultation) · `ls lab/research_utils/attested_patch.py` (F3 pending — inline attested
pattern until it lands)
Owner: [deep-iteration lane charter](../adr/2026-08-16-deep-iteration-lane-charter.md) (this
spec is its §7 step-2/step-4 tooling packet); campaigns dock under the charter's own Q-IDs and
counters; Part B, if ever filed, docks as a superseding ADR against the five owners named
above.

## Revision record

| Date | Change |
|---|---|
| 2026-08-22 | v1 authored as a sibling "GROW lane" (D1–D3); merged via PR #96 pre-review |
| 2026-08-22 | Dual adversarial review: gate audit BLOCKED-AT-FREEZE · panel BLOCKED (B1–B5) — [audit note](../notes/audits/2026-08-22-grow-lane-dual-panel-review.md) |
| 2026-08-22 | v2: D1–D3 withdrawn; recast as deep-iteration-lane extension packet (Part A tooling + Part B named question); all confirmed findings folded in |
| 2026-08-22 | Part A `Accepted` ([build-authorization ADR](../adr/2026-08-22-grow-lane-build-authorization.md)); slice 1 landed same day: `deep_lane_admission.py`, `grammar.py`, `--lane deep`, `burned_segments.py`/seed — 39 tests green |
| 2026-08-22 | GROW-0 harness built (Limb A/B, three RED controls, retry ledger, CLI) against its own frozen PREREG; then run for real at the frozen N=5,500/c=7 scale for the first time — Gate `RESOLVED` ([closure](../briefs/closures/GROW-0-closure-resolved.md)). Part B's filing decision (the two-ledger K question) is now unlocked for the operator per this Gate's own text |
| 2026-08-22 | Part B ADR filed and **ratified same day**: [`2026-08-22-grow0-two-ledger-k-question.md`](../adr/2026-08-22-grow0-two-ledger-k-question.md), `Accepted` (operator GO, "ratify it as-is"). Disposition: the within-campaign "K→M" claim is **rejected** (`K_intrinsic`'s ratified definition stands, unedited); the cross-campaign sealed-consultation claim is **adopted** as a new, disclosure-only charter §2.2(iv) conjunct — `lab/discovery/burned_segments.py` extended with channel-agnostic `consultation_count`/`consultation_history`. Went through three rounds of adversarial review same day before ratification, each catching a real defect in the drafting session's own reasoning (an invalid empirical inference, an invalid replacement doctrinal argument, a misattributed citation) — none in the underlying decision; documented transparently in the ADR's own Change History |
