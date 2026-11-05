# R3 dossiers: dedup search (Rule 8)

Run 2026-11-04 on `claude/r3-cost-headroom-dossiers` (base `main` at `fd688b1`), before any screen arithmetic. Output pasted as printed; empty output means no hit.

```text
$ git ls-files | grep -i -E "dossiers/R3|cost.headroom|cost-headroom"

$ grep -rIl -i "cost headroom\|R3 dossier\|PREREG-BUILDER-R3" --include=*.md .

$ git branch -r | grep -i -E "r3|headroom|dossier"
  origin/claude/r2-cell-dossiers
  origin/codex/pr395-calculation
  origin/codex/pr395-calendar
  origin/codex/pr395-evidence
  origin/codex/sfclear3-fixed-leg-live-sizing

$ gh api -X GET search/issues -f q='headroom repo:Joshua-Asante/first-passage is:pr' --jq '.items[] | [.number,.state,.title] | @tsv'
1043	open	docs(state): discharge the 2026-11-08 slate; carry follow-ups to 2027-02-08; roll sentinel SLATE_DATE
960	closed	fix(hooks): base check measures the session's checkout (cleanup P0.6)
1014	closed	feat(gates): wire md-anchors and doc-budgets (cleanup P1.1)
551	closed	docs: X-1 decision packet (preparation only; no CP-3)
567	closed	docs(qualification): S5 C3 re-verification, memory stop, rulings and the green full selection
569	closed	docs(qualification): S5 Stage 2 / PA-5 from run 36766144433 — k = 4.0789, RE-APPLY, ceilings unchanged
1035	closed	docs: correct entry docs for the retired c1 route and closed personal lane
709	closed	docs(handoff): four-firm re-MC timing card + I-15 figure (step 2(d))
722	closed	docs(t00 card): step-12 VM route withdrawn; local run at W=8
586	closed	fix(qualification): S5 TEST_ONLY defects D-S5-1 and D-S5-2
556	closed	docs(qualification): S5 C3 step 1 record - harness read, §7 rulings, bind_budget evidence
450	closed	docs(research): wall-clock cost decomposition + offline reranker oracle ceiling
783	closed	lab(sfgrowth): synthetic acceptance cases
429	closed	Add S2 supervision candidate and durable recovery authority barriers
431	closed	docs: Jev handoff disposition (not executed) + Limb B measured-shipped drift
147	closed	Phase A GO (A1+A2) + §4 firm-model-repair Q (R1+R2)
312	closed	Add exact funding evidence for supplied candidate executions
397	closed	docs: Tradeify attended-system simplification review (P1–P9 proposals)
284	closed	Campaign state: Phase 1 returned on PR #283 — gate verdict NEEDS_CONTEXT; D10–D14 raised; D11 narrowed to drop-only
753	closed	redact: remove Striker DJ30 v4.5 Pine-only values repo-wide
340	closed	docs(adr): Track A / A1 + A1r — Stage 1 input source: packet + option D RATIFIED 2026-09-11 (S2b build ADR, M1 ADR)
295	closed	Campaign orchestration 2026-09-04: thirteen Codex rounds, D23–D33, and a disclosure remediation

$ gh api -X GET search/issues -f q='dossier repo:Joshua-Asante/first-passage is:pr is:open' --jq '.items[] | [.number,.state,.title] | @tsv'
1061	open	docs(dossiers): R2 cell dossiers, two per instrument, ranked (K = 0)
1051	open	docs(prereg): builder round template — task chain T1–T8, private/public split
1064	open	docs: record 11-04 FX mapping, R2 composition and the same-pair spot-cohort ruling

$ grep -rIl -i -E "lucca|pre-FOMC|pre_fomc|fomc.drift" --include=*.md . | head
./docs/methodology/references/statistics-of-tradable-anomalies.md
./docs/notes/research/2026-10-21-tradeify-published-rule-candidates.md
./docs/rejected_candidates.md
./docs/briefs/rnd-pipeline/RATES-EV-ZF-1-conditional-event-breakout-scoping.md
$ gh api -X GET search/issues -f q='R3 dossier repo:Joshua-Asante/first-passage is:pr' --jq '.items[] | [.number,.state,.title] | @tsv'

$ gh api -X GET search/issues -f q='FOMC repo:Joshua-Asante/first-passage is:pr' --jq '.items[] | [.number,.state,.title] | @tsv'
891	closed	fix(lab): correct two FOMC dates in the shared archived list
888	closed	docs(research): published-rule candidates for a Tradeify-only strategy (sourcing pass, zero-K)
43	closed	feat(lab): ECON EXPORT v0.1 request.economic calendar-provenance check

```

**Reading:**
- No R3 or cost-headroom work exists. The only dossier work is R2 (PR #1061, open), which this wave re-aims; its index and 6J/M6E cost sections were read in full and its verified figures are reused, not re-derived.
- The `pre-FOMC` hits are priors, not duplicates: [Q-INVENTORY-1](../../../rejected_candidates.md) priced pre-FOMC ES, announcement-day SPX and FX fixing-window drifts on 2026-07-17 under the since-deleted 4× cost law; the 2026-10-21 Tradeify published-rule note rated pre-FOMC dead (overnight hold). Both are shown beside the R3 rows (Rule 26).
- PR #888 (published-rule candidates, closed) and PR #43/#891 (FOMC date list, econ export check) are inputs, not overlapping work.
