# ADR 2026-07-13 — HARV mechanism-first discovery lane ratification

**Status:** Accepted (operator ratified 2026-07-14 — HARD gate chosen; proceed sequence 1→2→3)
**Superseded-by:** none
**Superseded-in-part-by:** `2026-07-16-harv-attestation-same-units-supersession.md` - the §2 attestation specification only.
**Retain-until:** none
**Decision date:** 2026-07-13
**Authors:** Joshua (authority) + Cursor (assembly from Phase-0 sources) — parent triage: claude.ai advisor 2026-07-13
**Supersedes:** none — this ADR ratifies a **lane**; it does **not** supersede the discovery-campaign defaults, statistics-adoption, or DSR-K ADRs
**Related:** [`docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md`](../briefs/closures/Q-HARV-0-month-end-rebalance-ES.md) (mechanism-first evidence, AMBIGUOUS); [`docs/briefs/closures/DISC-CAMP-0-closure-falsified.md`](../briefs/DISC-CAMP-0-closure-falsified.md) (mechanism-blind shakedown, FALSIFIED / pipeline proven); [`2026-07-11-discovery-campaign-defaults-ratified.md`](2026-07-11-discovery-campaign-defaults-ratified.md); [`2026-07-11-tradable-anomalies-statistics-adoption.md`](2026-07-11-tradable-anomalies-statistics-adoption.md); [`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](2026-07-12-dsr-k-rule-and-variance-floor-supersession.md)
**Layer:** methodology (discovery-lane doctrine)

---

## §0 — Rule 0 reads (production-source verification)

Files read **before** authoring this ADR (Phase 0, 2026-07-14, off `origin/main` @ `53c27fe`):

- `docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md` — anchor: `fd17280` (2026-07-12) — primary harvest source ("Lane observations" + "What a fresh brief would need")
- `docs/briefs/closures/DISC-CAMP-0-closure-falsified.md` — anchor: `250c25e` (2026-07-13) — second evidence point (PD-1…PD-8 + FALSIFIED verdict)
- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` — anchor: `4b810a6` (2026-07-11) — standing Campaign-defaults governance (lane sits *within*)
- `docs/adr/2026-07-11-tradable-anomalies-statistics-adoption.md` — anchor: `4b810a6` (2026-07-11) — REFERENCE + Tranche-1; mechanism-first as π *argument*
- `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` — anchor: verified on disk at Phase 0 — K-floor + `V=1/n` + standing power-disclosure (partial overlap with reachability lesson; does not ratify this lane)
- `git ls-tree origin/main docs/adr/` for `harv` — **empty** (no prior HARV ADR; this draft is not a duplicate)

---

## §1 — Context

Two discovery campaigns have now closed under the 2026-07-11 governance chain, from opposite ends of the mechanism axis:

1. **Q-HARV-0** (mechanism-first, HARV-2026-001) closed **AMBIGUOUS** (2026-07-12). The primary H1 prediction cleared (sign-aligned conditional fade +19.21 bp, permutation p=0.0129, 4× cost hurdle), but the bundled placebo magnitude clause fired. Post-closure diagnosis: the frozen placebo window T-13→T-11 sat **inside** the conditioning window, so RESOLVED was structurally unreachable *before any data arrived* (~30–39 bp mechanical floor vs a 9.6 bp allowance). Neither authoring, G1 ratification, Phase-0, `check_brief`, nor the executor caught the unreachable gate until after closure. The closure's own lane harvest names this as the load-bearing lesson: a mandatory pre-registration **reachability simulation of every bundled clause under a plausible-true world** (H1-style power disclosure alone covered the primary, not the bundle).

2. **DISC-CAMP-0** (mechanism-blind pipeline shakedown) closed **FALSIFIED** on the candidate hypothesis (2026-07-13, Option B) while proving the Stage 0–7 pipeline end-to-end on real data (0 of 6 mined candidates cleared Stage-4 cost-law; 0-column Stage-5/6/7 traversal clean). Its process-defect log (PD-1…PD-8) is the complementary evidence: the *tooling* lane works when exercised; the *doctrine* lane still owes the reachability step Q-HARV-0 surfaced.

The standing defaults ADR ratifies *rules of evidence* (OOS axis, K, universe correction, temporal battery, decay-monitor-at-admission, cost gate) by reference to the campaign template — it does **not** ratify a mechanism-first discovery *lane*. The statistics ADR retains mechanism-first as the qualitative π argument and records numeric-π as a deliberate non-adoption. The DSR-K ADR operationalizes a power-disclosure requirement for the DSR gate specifically. None of the three is the HARV-lane ADR the Q-HARV-0 closure deferred.

**Decision driver (one sentence):** DISC-CAMP-0's closing cleared the last blocking condition named on the forward board for drafting this ADR; the mechanism-first lane is now evidenced from both ends and the unreachable-gate lesson is owed as standing doctrine before the next mechanism-first campaign freezes.

---

## §2 — Decision

**Decision (Accepted 2026-07-14):**

1. **Ratify the mechanism-first discovery lane as standing doctrine** for campaigns that claim a named economic mechanism (the HARV / Q-MECH-1 shape): register-record YAML + A/B mechanism-grade discount + bundled predictions that do real adjudication work (placebo / instrument / covariance / micro), inheriting the ratified Campaign defaults by reference. Mechanism-first is not optional decoration on an unconditional test — Q-HARV-0's placebo converted a clean-looking primary into a defensible AMBIGUOUS; that is the lane earning its keep.

2. **Mandate a pre-registration gate-reachability simulation of every bundled clause under a plausible-true world** before freeze / before `register_search open`. H1-style power disclosure on the primary alone is insufficient (Q-HARV-0: primary was reachable; placebo magnitude clause was not). A clause that is structurally un-passable under a true-mechanism world must be redesigned or dropped *pre-freeze* — freezing an unreachable gate wastes K and launders AMBIGUOUS as if it were an empirical miss.

3. **This ADR does not supersede** [`2026-07-11-discovery-campaign-defaults-ratified.md`](2026-07-11-discovery-campaign-defaults-ratified.md), [`2026-07-11-tradable-anomalies-statistics-adoption.md`](2026-07-11-tradable-anomalies-statistics-adoption.md), or [`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](2026-07-12-dsr-k-rule-and-variance-floor-supersession.md). It sits *within* that chain: defaults remain the evidence rules; this ADR names the mechanism-first *lane* and the reachability step those rules did not yet make mandatory for bundled clauses.

4. **HARD gate (operator pick 2026-07-14):** the reachability simulation is a **HARD gate** — it blocks `register_search open` until every bundled clause has a written reachability attestation in the campaign's pre-registration. The softer "recommended step" alternative in §3 is **ruled out** (Q-HARV-0 showed authoring + `check_brief` + executor all missed an unreachable clause when the step was informal).

**Effective:** immediately (2026-07-14).
**Scope:** mechanism-first discovery campaigns (HARV-shaped and successors); does not re-open DISC-CAMP-0's null result or rewrite Q-HARV-0's AMBIGUOUS verdict.

---

## §3 — Alternatives considered

| Alternative | Why ruled out / trade-off |
|---|---|
| **Leave lane informal** (harvest stays in the Q-HARV-0 closure appendix only) | The next mechanism-first campaign would re-derive the lesson under time pressure; unreachable gates would fire again. Status quo is worse than a dated doctrine ADR. |
| **Amend the defaults ADR in place** to add reachability | In-place edit of a ratified default is forbidden by that ADR's own §5. Reachability is a *lane* step, not a rewrite of OOS/K/DSR defaults. New ADR (this one) is the correct shape. |
| **HARD gate — reachability attestation blocks `register_search open`** (**§0.5-Q option A**) | **Chosen 2026-07-14.** Strongest protection against unreachable freezes. Cost: tooling/process overhead before every mechanism-first open; attestation format must be explicit in the campaign template (landed with this ratification). |
| **Recommended step — reachability simulation advised in pre-reg template, not a hard block** (**§0.5-Q option B**) | **Ruled out 2026-07-14.** Lower friction, but recreates the Q-HARV-0 failure mode (authoring + check_brief + executor all missed an unreachable clause when the step was informal). |
| **Treat DSR-K ADR's power-disclosure as sufficient** | That disclosure covers the DSR `(K, V, n)` cell for matrix-profile-family campaigns. Q-HARV-0's unreachable clause was a *bundled placebo magnitude* gate, not a DSR power miss. Different surface; does not substitute. |

---

## §4 — Falsifier (revert / success bar)

**H:** The mechanism-first discovery lane plus a pre-registration reachability simulation of every bundled clause is the correct standing doctrine for HARV-shaped campaigns.

**Falsifier (lane doctrine wrong):** the next mechanism-first campaign freezes with a bundled clause that later proves structurally unreachable under a plausible-true world (placebo ⊂ conditioning, magnitude floor > allowance, or equivalent geometry) — i.e. RESOLVED was unreachable *before data arrived*, again — **and** that campaign's pre-registration either omitted the reachability simulation or the simulation failed to flag the clause. On that evidence this ADR is superseded (not silently edited).

**Success bar (lane doctrine holding):** the next mechanism-first campaign's bundled clauses are all reachability-simulated pre-freeze; no post-hoc "gate measured its own conditioning overlap" diagnosis appears in its closure.

**Verdict vocabulary (binary):** **RESOLVED** if the success bar holds on the next mechanism-first closure; **FALSIFIED** if the falsifier above fires; **AMBIGUOUS** if no mechanism-first campaign closes before the 2026-11-08 audit window — then re-test at the following quarterly.

**Revert action:** superseding ADR citing the dated campaign closure; do not edit §2 in place.

**Trigger check schedule:** rides the standing quarterly programme audit — next **2026-08-08**, then 2026-11-08 — plus any mechanism-first campaign closure in between.

---

## §5 — Forbidden moves (under this ADR)

- **Quietly downgrading the HARD gate to a recommended step after acceptance** — that is a silent §2 edit; supersede with a dated ADR if the HARD gate proves unworkable.
- **Superseding or restating Campaign-default values** (OOS axis, K, DSR threshold, etc.) inside this ADR — single source of truth stays the template + defaults ADR; this ADR references, it does not copy.
- **Promoting Q-HARV-0's AMBIGUOUS verdict** on the strength of the post-closure placebo-geometry diagnosis — the closure itself forbids that (§5 of the brief / closure discipline); lane doctrine harvests the *lesson*, not a rescue.
- **Re-running or re-mining DISC-CAMP-0** under this ADR — the candidate hypothesis is closed FALSIFIED; the lane ratification does not reopen a null shakedown.
- **Freezing a mechanism-first campaign without a written reachability note for each bundled clause** once this ADR is `Accepted` under the HARD-gate option — that would be exactly the Q-HARV-0 miss.
- **Silent amendment of §4** to match an emerging unreachable-gate miss — Known Trap #12; supersede instead.

---

## §6 — Consequences

**Gate reminder (ties to §4):** doctrine check uses **RESOLVED / FALSIFIED / AMBIGUOUS** as named in §4 — not a live trading gate.

**Positive:**
- Mechanism-first becomes a dated, citable lane (not only an appendix harvest).
- Unreachable bundled gates become a named, auditable failure mode with a pre-freeze check.
- Q-HARV-0 and DISC-CAMP-0 both feed forward as evidence rather than orphan closures.

**Negative (real cost):**
- Pre-registration overhead rises for mechanism-first campaigns (reachability write-up per bundled clause).
- `register_search open` is doctrine-blocked for mechanism-first campaigns until the attestation exists (code enforcement may lag — see downstream).

**Risks:**
- Attestation format underspecified → false HARD (campaigns blocked on ceremony) — mitigated by the template row landed with this acceptance.
- Over-reading this ADR as superseding defaults / DSR-K — mitigated by §2.3 and §5.

**Downstream (Accepted 2026-07-14):**
- Campaign template Stage-0 / authoring checklist: reachability-simulation HARD-gate row (this commit).
- `STATE.md` forward board: HARV lane ADR marked Accepted.
- Optional later: mechanical `register_search open` guard (separate implementation handoff — doctrine binds now; code may lag).

---

## §7 — Implementation plan

- **Phase 0** — DONE (Rule-0 reads at draft).
- **Phase 1** — DONE (`Proposed` draft on `cursor/post-batch-doc-artifacts`).
- **Phase 2** — DONE 2026-07-14: operator Accepted + HARD gate; template + STATE downstream this commit.
- **Phase 3** — verification block at commit; no `core/` / locked-parameter touch.

---

## §10 — Audit hooks (runnable)

```bash
# Status Accepted + HARD gate chosen
grep -n "Status:" docs/adr/2026-07-13-harv-discovery-lane-ratification.md
# Expected: Accepted

grep -nE "HARD gate \(operator pick|Ruled out 2026-07-14" docs/adr/2026-07-13-harv-discovery-lane-ratification.md

# Template carries the HARD-gate row
grep -n "reachability" docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md

# Does not claim to supersede the governance chain
grep -n "does not supersede\|Supersedes: none" docs/adr/2026-07-13-harv-discovery-lane-ratification.md

# Primary evidence sources still present
test -f docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md
test -f docs/briefs/closures/DISC-CAMP-0-closure-falsified.md

# No locked constant / allocation / dd_protection / MC-anchor touch (expect empty on core/)
git diff origin/main -- core/ | grep -E "DD_TRIGGER|BASE_RISK" || echo "core clean"

# §4 trigger reminder — next programme audit: 2026-08-08
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-13-harv-discovery-lane-ratification.md --type adr
# Expected: all checks PASS; status line reads Accepted

# Phase-0 anchors
git log -1 --format='%h %ci' -- docs/briefs/closures/Q-HARV-0-month-end-rebalance-ES.md
# Expected: fd17280 …

git log -1 --format='%h %ci' -- docs/briefs/closures/DISC-CAMP-0-closure-falsified.md
# Expected: 250c25e …
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-13/14 | Initial `Proposed` draft — assembled from Q-HARV-0 lane harvest + DISC-CAMP-0 defect log; HARD vs recommended left open for operator | Joshua (authority) + Cursor (assembly) |
| 2026-07-14 | `Proposed`→`Accepted`; HARD gate chosen; recommended step ruled out; template + STATE downstream | Joshua (ratify) + Cursor (record) |
| 2026-07-16 | §4 falsifier **FIRED** — both conjuncts confirmed against the H-OD-1 closure ([`lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md`](../../lab/analysis/harvest/h_od_1_es_overnight_drift_2026-07/RESULTS.md); same defect retro-diagnosed in the D5 closure): RESOLVED was unreachable *before data arrived*, and the frozen §R reachability simulation failed to flag the clause. Per §4's own Revert action, this ADR is **superseded, not edited** — [`2026-07-16-harv-attestation-same-units-supersession.md`](2026-07-16-harv-attestation-same-units-supersession.md) strengthens the §2 attestation specification (same-units / per-gate / panel-basis) **in part**. The mechanism-first lane, the HARD gate, and the register wiring all **STAND**. (Header `Superseded-in-part-by` field added retroactively 2026-08-29 — adr-decay-audit `DECAYED_UNDOCUMENTED` finding; this row backfills the reciprocal pointer that should have landed same-day as the successor ADR, per this repo's own convention.) | Claude Code (adr-decay-audit remediation) |
