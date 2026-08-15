# ADR 2026-07-26 — REGIME-CANDIDATE flag lane + reserved-holdout mechanics for grid campaigns

**Status:** `Proposed` — operator ratification pending — drafted at operator direction 2026-07-26; ST-EH-1 instantiates the structure campaign-locally under the existing override clause regardless of this ADR's fate
**Decision date:** 2026-07-26
**Authors:** Joshua (direction) + Claude Code (Fable 5, drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Amends-in-part:** [`2026-07-11-discovery-campaign-defaults-ratified.md`](2026-07-11-discovery-campaign-defaults-ratified.md) — extends Default #1 (temporal OOS axis) with a structured detection lane for modern-era edges; the IS axis, the OOS confirm role, and every threshold value are unchanged.
**Related:** [`docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md`](../briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md) (first instance); [`2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) (K-accounting conventions this extends to dual-window reads).
**Layer:** methodology (research rules of evidence only). No strategy/risk-control parameter, allocation, `dd_protection` constant, or Pine source is touched.

---

## §0 — Rule 0 reads (production-source verification)

Verified this session (2026-07-26), worktree `supertrend-harness-baseline-dd3529` up to date with `origin/main` @ `a35adcd`:

- `docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md` — anchor `7af4224` (2026-07-20). §Campaign-defaults Default #1 verbatim: IS `2010-01-01:2018-12-31` discovery+tuning; OOS `2019-05-06:present`; "Consciously accepts the pre-2019-viability selection bias, on the record" — the acknowledged cost this ADR structures a remedy for.
- `docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md` — anchor `ba943a1` (2026-07-17). §4 falsifier: defaults change by superseding/amending ADR citing closed-campaign or operator evidence, never in-place edit — this document is that vehicle.
- `ops/instruments/MNQ.md` — anchor `691fd48` (2026-07-25). N1: ORB-MNQ-1 is a **regime-conditional post-2020 edge** admitted with the conditionality as a standing caveat (Stage-7 passes on 2021+; full window cost-marginal) — the live precedent that a real modern-era edge exists which IS-2010-2018-only selection would score weakly. N5: the D5 scar (IS +1.461 bp → OOS −0.327 bp) — the window-luck failure the reserved holdout answers.
- `discovery_manifests/README.md` + manifests — K-ledger conventions (open binds K pre-result; abandoned campaigns bank K).

---

## §1 — Context

Default #1 fixes the only honest independence axis (temporal) and consciously
accepts a bias: selection confined to IS 2010-2018 is structurally blind to edges
born with the modern market structure (micro contracts 2019+, the 2020 watershed,
the 2024 structural shift). Since ratification, the record has produced a live
instance — ORB-MNQ-1's post-2020-conditional edge — showing the blind spot is not
hypothetical. The operator raised the challenge directly on 2026-07-26 during
ST-EH-1 Stage-0. The naive remedy (select on the modern window) recreates the D5
window-luck shape: "the edge didn't exist back then" is unfalsifiable when the
same window both selects and confirms. What is needed is a structure that
**detects** modern-era candidates without letting them **promote** on the window
that selected them — and that mechanically preserves a clean confirm window.

**Decision driver (one sentence):** the ratified axis's acknowledged modern-edge
blind spot now has a live counterexample and an operator challenge, and the fix
must be structural (detection lane + preserved holdout), not a per-campaign
improvisation.

---

## §2 — Decision

For any campaign whose search involves config/cell selection (grid-shaped), the
campaign MAY pre-register a **dual-track structure** with these standing
mechanics (a campaign that omits it simply runs the unamended Default #1):

1. **Track 1 — promotion (unchanged):** selection on the ratified IS; confirm on
   the ratified OOS; full inherited universe correction. The only lane that can
   promote.
2. **Track 2 — REGIME-CANDIDATE flag lane:** cells failing Track-1 IS criteria
   are additionally scored on a declared **flag window** — the OOS era truncated
   at a declared boundary (default `2019-05-06 : holdout_start`). Flag criteria
   = the campaign's promotion bar evaluated on the flag window (minus
   promotion-only corrections such as DSR), plus native-micro sign agreement.
   **A flag never promotes.** It authorizes authoring a follow-up
   pre-registration whose confirm window is the reserved holdout, with its own K
   increment and its own operator GO.
3. **Reserved holdout:** the OOS tail from `holdout_start` (default
   `2024-01-01`, chosen per campaign; the holdout must be ≥ 2 calendar years at
   freeze) to present is **not computed and not reported per-cell** in the
   flagging campaign, except for (a) pre-registered fixed baselines and
   (b) Track-1 survivors' confirm reads — an explicit allowlist frozen at
   Stage 0. Runners hard-cap grid scoring at the boundary; the discipline is
   mechanical, not aspirational.
4. **K accounting:** every window a cell is scored on for lane-firing purposes is
   a selection event; dual-window reads are counted per-window in the campaign K
   and banked per instrument family per the existing ledger conventions.

**Effective:** upon operator ratification (status → `Accepted`). ST-EH-1 runs the
identical structure campaign-locally under the template's override clause in the
meantime.
**Scope:** discovery/characterization campaigns with config selection. Not
retroactive; closed campaigns' verdicts unaffected.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Keep Default #1 unamended (status quo) | The blind spot is acknowledged in the default's own text and now has a live counterexample (ORB-MNQ-1) plus a standing operator challenge; per-campaign improvisation without a standing structure invites exactly the silent-override drift the ratification exists to prevent. |
| Flip the axis: select on the modern era, confirm on 2010-2018 | Unfalsifiable-by-construction for regime-born claims ("it didn't exist back then" excuses every historical failure in advance); recreates the D5 window-luck shape with no honest confirm window at all. |
| Walk-forward re-selection | Answers a different question (procedure viability, not fixed-cell viability); collides with the regime-detectability wall (regime-signal battery CLOSED NULL — re-selection requires detecting shifts fast enough, which the record says we cannot); a far larger redesign than the observed problem warrants. |
| Both-halves symmetric requirement (cell must pass 2010-2018 AND 2019+ independently) | Strictly *amplifies* the modern-edge blind spot (a regime-born edge fails the early half by construction) — the opposite of the challenge being addressed; already available as an extra-stringency option inside Track 1 where wanted. |
| Full-panel characterization reported through present (no reserved holdout) | Once per-cell modern-tail numbers are reported, the selector has seen them and every future "holdout" on that tail is soft-contaminated; the flag lane's follow-up confirm would be theater. |

---

## §4 — Falsifier (revert trigger)

**H:** the flag lane surfaces genuinely regime-born edges at a useful rate without
degrading promotion discipline.

**Revert trigger (binary):** **if** the first **two** flag-lane follow-up
campaigns both close with their reserved-holdout confirm FALSIFIED (the flagged
edge fails its clean window), **then** the lane is manufacturing window-luck leads
rather than detecting regime-born edges — this ADR is reverted (lane retired;
Default #1 stands unamended) via a superseding ADR that also re-banks the spent K;
**otherwise** the lane stands. Independently: **if** any campaign is shown to have
violated the reserved-holdout discipline (per-cell holdout numbers surfaced before
the follow-up froze), **then** that campaign's flags are void (downgrade to
observation-only) regardless of the lane's overall standing.

**Revert action:** superseding ADR; flagged-but-unconfirmed candidates lapse to
ordinary rejected-candidates entries with their K banked.

**Trigger check schedule:** rides the standing programme-audit dates (next
2026-11-08, then 2027-02-08) — check: any flag-lane follow-up closures since the
prior audit, and their confirm verdicts.

---

## §5 — Forbidden moves (under this ADR)

- **Promoting from the flag window** — the lane's entire legitimacy is that
  detection and admission use different data; collapsing them recreates the exact
  D5 shape the lane exists to avoid.
- **Computing the reserved holdout "for context" during the flagging campaign** —
  soft contamination is contamination; the allowlist is exhaustive, frozen at
  Stage 0.
- **Moving `holdout_start` after seeing flag-window results** — window shopping at
  the methodology layer (Trap #12); the boundary freezes at Stage 0.
- **Counting dual-window reads as one trial** because "it's the same cell" — each
  window read can fire a lane; under-banking K silently lowers every future DSR
  floor in the family.
- **Treating a fired flag as evidence of edge** in any doc, memory, or ledger
  before the follow-up confirm closes — a flag is an authorization to test, not a
  finding.

---

## §6 — Consequences

**Positive:**
- Modern-era edges become detectable without weakening promotion (the acknowledged
  Default-#1 bias gets a structured, non-promoting outlet).
- The confirm window for regime-born claims is mechanically preserved rather than
  hoped for.
- Operator challenges to the axis now have a standing answer instead of
  per-campaign re-litigation.

**Negative (real):**
- Grid campaigns lose per-cell visibility into the most recent ~2.5 years until a
  follow-up runs — a real reporting cost, accepted deliberately.
- Dual-window reads roughly double grid K, raising family DSR floors for future
  campaigns (ST-EH-1: 84 not 44).
- Two artifacts (flagging campaign + follow-up) where one full-panel campaign used
  to suffice.

**Risks:**
- A short reserved holdout (≥2 yr minimum) gives follow-up confirms modest power —
  mitigated by the flag bar being the full promotion bar (only strong modern edges
  fire), and by the §4 two-strikes falsifier.
- Holdout discipline depends on runner implementation — mitigated by the hard-cap
  requirement and the §4 voiding clause.

**Downstream artifacts on ratification:**
- `discovery-campaign-template.md` §Campaign-defaults — add the flag-lane/
  reserved-holdout row referencing this ADR (values live there per the
  single-source rule).
- `STATE.md` forward board — 11-08 audit line gains the §4 check.

---

## §7 — Implementation plan

- **Phase 0** — this draft lands `Proposed` alongside the ST-EH-1
  pre-registration (done in the same commit).
- **Phase 1 (on operator ratification)** — status → `Accepted`; template
  §Campaign-defaults row added; STATE.md forward-board line added.
- **Phase 2** — grep-sweep for campaigns citing Default #1 to confirm none
  mis-cites the lane as promoting (§10 hook 3).
- **Phase 3** — verification block passes; first §4 check rides the 2026-11-08
  audit.

---

## §10 — Audit hooks (runnable)

```bash
# 1. Status + bidirectional amendment reference
grep -n "Status:" docs/adr/2026-07-26-regime-candidate-flag-lane.md
grep -n "Amends-in-part" docs/adr/2026-07-26-regime-candidate-flag-lane.md

# 2. First instance exists and declares the lane as non-promoting
grep -n "A flag NEVER promotes" docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md

# 3. No campaign cites the flag lane as a promotion path (expect: only 'never promotes' phrasings)
grep -rniE "flag.{0,40}promot" docs/briefs/pre-registration/ docs/adr/ | grep -vi "never promot"

# 4. §4 two-strikes check (run at each programme audit): flag-lane follow-up closures + confirm verdicts
grep -rli "REGIME-FLAG" docs/briefs/closures/ 2>/dev/null

# 5. On ratification only: template row exists
grep -n "regime-candidate-flag-lane" docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md
```

---

## Verification

```bash
python scripts/check_brief.py docs/adr/2026-07-26-regime-candidate-flag-lane.md --type adr

# §0 anchors
git log -1 --format='%h %ci' -- docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md   # 7af4224
git log -1 --format='%h %ci' -- docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md   # ba943a1
git log -1 --format='%h %ci' -- ops/instruments/MNQ.md                                        # 691fd48

# Amended ADR's own change-mechanism clause (this ADR is the sanctioned vehicle)
grep -n "superseding ADR" docs/adr/2026-07-11-discovery-campaign-defaults-ratified.md | head -3
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-26 | Drafted `Proposed` at operator direction, alongside ST-EH-1 Stage-0 (first campaign-local instance). Operator ratification pending. | Joshua (direction) + Claude Code (Fable 5) |
