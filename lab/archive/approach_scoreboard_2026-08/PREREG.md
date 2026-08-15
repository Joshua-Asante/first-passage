# SPEC: Q-SCORE-1 — approach-level scoreboard Block 1 freeze
Status: FROZEN · 2026-08-11 · authorizes nothing ($0 · K=0) · depends: design 2026-08-11-approach-scoreboard-design.md (RATIFIED operator 2026-08-11; PR #743)
Objective: Freeze sources, one-time lane retro-map, streak thresholds, and H_A/H_B; report assignability % → H_A. Report-only; cannot close a lane.

Steps:
1. CC: author this PREREG + RETRO_MAP against all closures/manifests at HEAD; inventory Closed: coverage; answer the grandfather-concentration sub-question.
2. CC: compute assignability % → H_A in BLOCK1_RESULTS.md.
3. (likely) CC: on H_A FALSIFIED, author the forward Lane:/Closed: residue proposal + typed closure + board writes; stop (Block 2 gated off).
4. (gated) on H_A ≥80%, authorize Block 2 only — do not start the runner in this block.

Gate: H_A RESOLVED if ≥80% of closures under docs/briefs/closures/ are assignable
      (frozen lane ≠ UNASSIGNED ∧ machine-readable verdict ∧ machine-readable Closed: date)
      under the grammars in F3; FALSIFIED if <80%.
      H_B is Block 3's gate (disagreement with recollection) — frozen here, not scored here.
Boundary: report-only · no new store · no lane closure by arithmetic · no threshold tuning after
          seeing the table · no silent parser fork · no PnL/return reads · no candidate generation ·
          no edits to core/ ops/ Pine / existing closures / existing gates · artifact must stay deletable ·
          do not create lab/analysis/meta/ · do not loosen the 80% bar.
Reads: docs/superpowers/specs/2026-08-11-approach-scoreboard-design.md @ 796c7f9 ·
       scripts/check_closure_disposition.py @ 052d4a9 ·
       scripts/check_status_consistency.py @ b762078 ·
       discovery_manifests/README.md + 13 manifests @ d7c8bcb ·
       docs/briefs/closures/ (53) @ e21f7e5 ·
       lab/CATALOG.md @ b80defc ·
       docs/rejected_candidates.md (intake + domain roll-ups) @ 1b7af9b ·
       .claude/skills/programme-audit/SKILL.md signal 5 @ 1772f26 ·
       docs/adr/2026-07-10-databento-research-stack.md §4 @ ba943a1 ·
       docs/adr/2026-08-07-w5-governance-diet.md @ 45e3cea ·
       docs/spec/2026-08-09-dense1m-entry-mechanism-lane-spec.md @ d5fd9fc ·
       .claude/skills/brief-authoring/references/closure_record.md @ e144ba9
Owner: docs/superpowers/specs/2026-08-11-approach-scoreboard-design.md

## §0 Rule-0 anchors (Task 1)

| Path | HEAD tip (`git log --oneline -1`) | What was verified |
|---|---|---|
| scripts/check_closure_disposition.py | 052d4a9 fix(gate14): warn on closed campaigns with no closure record | coverage limb + GRANDFATHERED (34) + importable helpers (`campaign_id_from_closure_filename`, `closure_campaign_ids_on_disk`, `missing_closure_campaigns`, `scan_file`); no Closed:/Lane:/verdict structured parser — `scan_file` only checks Iterate-block tokens |
| scripts/check_status_consistency.py | b762078 fix(lab): repair nest path math + CI ignores after theme nest | `parse_catalog` / `scan_rejected` importable; file-head records C1 status-contradiction + C4 intra-STATE DROPPED (no semantic-dead join; bounds what a runner may claim) |
| discovery_manifests/*.json (13) | d7c8bcb research(mnq): close MNQSR-1 Phase-1 S/R structure screen (0/14 FDR) | keys present across corpus: `K` / `declared_K` (where used) / `lane` / `status` / `opened_at` / `closed_at` / `results.executed_k`; README @ 48b8cef; count at freeze = **13** (plan design-time expect 14 — main moved; freeze the observed count) |
| docs/briefs/closures/ | e21f7e5 docs(closures): author Q-ICT-CASCADE-1 / Q-TVCOV-1 / Q-USOIL-1 stubs | **53** files at freeze HEAD (design-time 50; PR #745 restored/authored the coverage backlog). F3 `Closed:` hits measured in Task 3 |
| closure_record.md | e144ba9 feat(governance): mandatory typed Iterate exit on closures — ADR Proposed, gate 14 self-arming | `**Closed:** YYYY-MM-DD` present in template; `Lane:` absent |
| design (RATIFIED §2) | 796c7f9 design(Q-SCORE-1): ratify §2 forks (operator, 2026-08-11) | flat slug `lab/archive/approach_scoreboard_2026-08/`; `lab/analysis/meta/` absent (verified); report-only; 80% H_A bar frozen |
| lab/CATALOG.md | b80defc merge(origin/main): keep NULL catalog label; retain tradeify_book heavy annotation | Active `_inbox` theme precedent: `ict_mnq_2026-08` six-column row |
| docs/rejected_candidates.md | 1b7af9b close(Q-MCLTAS-1): FALSIFIED on Wall B magnitude -- probe never run, $0/K=0 | `<!-- concept-intake-entry -->` blocks + 5th-leg / regime-detection domain roll-ups present |
| programme-audit SKILL.md | 1772f26 docs(skills): update cross-references from fxify-challenge to prop-firm-challenge | signal 5 (SNAG) is the quarterly vehicle this feeds, never replaces |
| databento ADR §4 | ba943a1 docs(adr): M1 normalize all 78 ADR headers to six-field grammar | uselessness-check shape for own falsifier (2026-11-08) |
| W5 governance diet | 45e3cea docs(loop): S1-S7 ADRs + Posture-A W streams + F2/F3 foundation | retention test every artifact here must pass |
| dense1m lane spec | d5fd9fc freeze(Q-TNEC-CON-5): impulse-pullback-VWAP-reclaim G0 | lane name already used by TNEC-CON closures |

**Parser-importability (design §12 item 1) — verified 2026-08-11 at `68fa67f`:**
- `from scripts.check_closure_disposition import …` and `from scripts.check_status_consistency import parse_catalog, scan_rejected` → `importable: OK`; `GRANDFATHERED` len=34; closure ids on disk=57; `missing_closure_campaigns()` empty.
- Neither module exposes a structured `Closed:` / `Lane:` / verdict parse. Block 2 (if reached) takes **option (b)**: minimal campaign-local reader; duplication named as a known cost. Option (a) deferred (gate-file edit needs its own justification). **No silent fork of `scan_file` Iterate regexes.**

## Freeze blocks (nothing below grows after this commit)

F0 — Parser posture (design §12 item 1): import coverage-limb + catalog/rejected helpers from the
  existing checkers. Closed:/Lane:/verdict structured parse is NOT exposed → Block 2 option (b):
  minimal campaign-local reader; duplication recorded as a known cost. No silent fork of scan_file.

F1 — Sources (read-only; the four design §2 Sources):
  (1) docs/briefs/closures/*.md — verdict token + Closed: + typed Iterate Next:
  (2) discovery_manifests/*.json — K (executed), declared_K where present, lane, status, timestamps
  (3) lab/CATALOG.md — status / theme
  (4) docs/rejected_candidates.md <!-- concept-intake-entry --> blocks — mechanism_family, class, date
  No fifth source. No hand-maintained lane list.

F2 — Lane vocabulary (closed set for the one-time retro-map; extend = new freeze):
  mnq-dense-1m-entry       — dense-1m entry-mechanism lane (docs/spec/2026-08-09-dense1m-…)
  tnec-necessary-conditions — TNEC envelope / necessary-conditions compile thread
  forced-flow-census       — forced-flow census channel (design §5)
  transfer-expression      — transfer / expression grid lane (design §5)
  external-sourcing        — external-sourcing harvest (design §1 / rejected roll-up kin)
  regime-detection         — regime-detection domain (design §1 SNAG precedent)
  fifth-leg-domain         — 5th-leg / index-intraday OHLCV directional-timing domain bar
  discovery-blind-grid     — blind / mining-shaped discovery grids (e.g. ST-EH)
  harvest-mechanism-first  — mechanism-first harvest intake screens (H-* / Req-1 path)
  reconstruction-self-funded — self-funded reconstruction lane (MYM/ORB kin)
  governance-ops           — rail / capacity / governance campaigns (not approach-exhaustion)
  UNASSIGNED               — visible residue bucket (printed, never dropped; design §4 discipline 3)
  A lane invented mid-map is a new campaign. Q-ID prefix matching is forbidden as an assignment rule.

F3 — Machine-readable grammars (load-bearing for H_A; do not "helpfully" broaden):
  Closed:  a header line matching (?m)^\*\*Closed:\*\*\s*\d{4}-\d{2}-\d{2}
           OR (?m)^Closed:\s*\d{4}-\d{2}-\d{2}
           Does NOT match: "Closed (explore record):", "Date:", "Status: … closed YYYY-MM-DD",
           or a date embedded only in a Verdict prose line.
           (Implementation note: Python 3.14 rejects inline `(?m)` mid-alternation; campaign-local
           code uses `re.compile(r'^(?:\*\*Closed:\*\*|Closed:)\s*\d{4}-\d{2}-\d{2}', re.M)` —
           same acceptor, not a grammar broaden.)
  Lane:    a header line matching (?m)^\*\*Lane:\*\*\s*.+  (forward rule; Block 1 retro-map
           is the one-time substitute for historical files).
  Verdict: the closure's own filed token (filename slug + **Verdict:** line) — quoted, never
           re-labelled (design §4 discipline 1).
  Git-commit dates and explore-record dates may be reported as LABELED FALLBACK only; they
  never count toward H_A (design §3 M-AHF: storage form ≠ mental form).

F4 — Streak + yield rules (thresholds frozen; never tuned after seeing a table):
  WATCH at consecutive zero-yield streak ≥ 3 (SNAG anchor = Q-DJ30-1/2/3).
  LEVEL-CHANGE-RECOMMENDED at streak ≥ 6.
  A close resets the streak ONLY if it yielded an admitted candidate.
  Capability-RESOLVED (measured: Q-MNQSEL-2) does NOT reset.
  AMBIGUOUS-HOLD counts as zero-yield (design §12 item 4 — held is not yielded).
  VOID / NULL / SCREEN-FAIL / INTAKE-DRY / OPERATOR-STOPPED / ABORT count as zero-yield.
  Narrative anchor (not a Block-1 retune number): MNQ short-horizon thread carries 8 consecutive
  zero-yield closes since 2026-08-08 (Q-R2VBUCK-1, Q-R2FLOW-1, Q-R2AGRUN-1, Q-MNQDTL-CON-1,
  Q-TNEC-CON-2/3/4/5); Q-MNQSEL-2 (RESOLVED 2026-08-08) resolved a capability, not a candidate.

F5 — Assignment honesty (design §12 item 3):
  Assign by the campaign's PRE-REGISTERED QUESTION (parent brief / PREREG objective), never by
  its outcome. When question-based lane ≠ the lane an outcome-reading would suggest, keep the
  question-based lane and record the row in RETRO_MAP.md §Differentials.

F6 — Hypotheses + own falsifier:
  H_A — ≥80% of docs/briefs/closures/*.md are assignable under F2+F3. Design-time pre-measure
        was 74% date coverage (13/50); HEAD verify at freeze is under the same F3 grammar and
        still <80% (Task 3 cites the live counts). Bar NOT moved. Expected verdict: FALSIFIED.
  H_B — (Block 3) scoreboard disagrees with recollection ≥1 time; else NULL and delete.
  Own falsifier — if by 2026-11-08 the scoreboard has fired zero LEVEL-CHANGE-RECOMMENDED
        signals AND has not been consulted at the quarterly audit → delete runner + RESULTS
        (databento ADR §4 shape). Clock rides 2026-11-08; no second clock.

F7 — Dispositions (Iterate block, pre-registered; design §6):
  H_A <80%  → STOP / FALSIFIED — residue = propose one-line forward Lane: + Closed: fields
              on the closure template (brief-authoring/references/closure_record.md); proposed
              here, NOT executed in this campaign. Block 2 gated off.
              Note: the same grammar also serves the queued promote-to-HARD ADR for
              check_closure_disposition.py's coverage limb (declared "ready" by PR #745) —
              one grammar serves both; this campaign does not author or ratify that ADR.
  H_B = 0   → STOP / NULL — and delete the runner (Block 3).
  H_B ≥ 1   → INTEGRATE — propose one pointer line into programme-audit signal 5
              ("run the scoreboard first"); named by the closure, never executed by it.
