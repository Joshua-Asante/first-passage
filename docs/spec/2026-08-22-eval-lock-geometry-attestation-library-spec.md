# SPEC: Canonical worker-attested `dd_lock_offset_usd` patch library (F3)

Status: PROPOSED · 2026-08-22 · authorizes nothing new — discharges an already-ratified
obligation (F3, due 2026-09-01) · depends: [2026-08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)
§5.1 F3 · [M-23](../methodology/lessons/methodology_lessons.md) · [M-24](../methodology/lessons/methodology_lessons.md)
Objective: land one canonical, process-pool-safe primitive for patching + attesting the
Tradeify eval-phase drawdown-lock constant, so future campaigns stop hand-rolling the
`firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"] = …` monkeypatch that produced M-23
(defective geometry scored through a process pool, optimistic, undetected four days).

Steps:

1. **Rule 0.** Read in full before any design: `core/firm_rules.py:340-370` (the
   `DEFECT FOUND 2026-07-22, APPLIED 2026-08-04` comment block — the constant itself is
   **already fixed**, default is `1_000_000.0`/unreachable); the M-23 and M-24 lesson
   entries in full (`docs/methodology/lessons/methodology_lessons.md`); at minimum two
   existing per-brief copies of the pattern —
   `lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_eval_lock_fix.py`
   (the original correction study) and
   `lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_parameterized.py`
   (a recent one) — to confirm the shape below covers both the A/B-comparison case
   (temporarily restoring the pre-fix `100` value) and the plain corrected-default case.
2. **Sweep, don't assume the audit's site list is current.** `rg -l "dd_lock_offset_usd"
   lab/analysis/` and classify every hit into: (a) prose-only mentions (`RESULTS.md`,
   `.json` — leave untouched, they are historical record); (b) code that mutates
   `FIRM_RULES[...]["dd_lock_offset_usd"]` directly. Only (b) is in scope for migration.
3. **RED-first tests, before the build:** (a) a joblib `Parallel(prefer="processes")`
   fan-out where only the parent process patches the constant must, under the new
   primitive's attestation check, **fail loudly** (the exact M-23 shape — reproduce it
   as the negative control); (b) a fan-out where each worker patches via the new
   primitive must attest a singleton value and pass. Watch both fail/pass correctly
   before building the real thing — this is the non-vacuity guard from the W1 spec
   precedent (`2026-08-09-w1-intraday-rerun-execution-spec.md` step 2), applied here.
4. **Build `lab/research_utils/attested_patch.py`** — a generic, reusable primitive (not
   `dd_lock_offset_usd`-specific; M-23's own enforcement rule is general to "any run whose
   correctness depends on a mutated module-level constant"):
   - `attested_patch(obj, key, value)` — context manager; must be entered **inside** the
     worker function (after the worker's own re-import), never only in the parent before
     dispatch. Patches `obj[key] = value`, reads it back from `obj[key]` (never from the
     locally-held `value`), and yields an attestation dict (`{"requested":…,
     "attested":…}`) — the attested value belongs in the worker's returned report.
   - `assert_singleton_attestation(attestations, expected)` — raises with a specific,
     diagnostic message (names the M-23 shape) if the attested set across every unit of
     work is not exactly `{expected}`.
5. **Build `lab/research_utils/eval_lock_geometry.py`** — the thin, `firm_rules`-specific
   wrapper: `patched_eval_geometry(tier, offset=UNREACHABLE)` returning
   `attested_patch(firm_rules.FIRM_RULES[tier], "dd_lock_offset_usd", offset)`, plus the
   `UNREACHABLE = 1_000_000.0` constant (mirrors `core/firm_rules.py`'s own idiom — do not
   re-derive it, import or restate the exact value with a citation comment).
6. **Migrate only what step 2 classified as in-scope AND not already closed.** For each
   candidate site, check whether its owning `lab/analysis/<theme>/<slug>/` has a
   published `RESULTS*.md` carrying a stated verdict (PASS/FAIL/FALSIFIED/RESOLVED/etc.).
   - **Closed-verdict sites: do not touch the scoring code.** Editing it and re-running
     would silently risk changing a number already on record — exactly the freeze-contract
     violation this repo's Known-Trap #12 exists to prevent. Leave them as historical
     record; note in this spec's own tracking (or a landing PR description) which sites
     were left alone and why.
   - **Open/still-mutable sites** (no published verdict yet, or the owning campaign is
     genuinely still iterating): migrate to the new primitive, and diff old-vs-new output
     on the site's own fixtures/frozen inputs before considering the migration done — any
     numeric drift is a stop-and-report event, not a thing to reconcile silently.
7. **Point new work at the library.** Add one line to the relevant methodology surface
   (candidate: `docs/methodology/regime_robustness_gate.md` "Implementation notes", or a
   pointer from `CLAUDE.md`'s Protection section — pick whichever this repo's own
   `lesson_corrections_land_where_read` rule says is actually read before a new campaign
   touches eval-phase geometry) naming `lab/research_utils/eval_lock_geometry.py` as the
   canonical import, so a new campaign has no excuse to reinvent the monkeypatch.
8. **Close F3.** Update `STATE.md` row / the 2026-08-03 audit's own F3 line to point at
   the landed module + migration list; note explicitly which sites were left untouched
   (step 6) and why, so a future reader does not read "F3 discharged" as "every site
   migrated."
9. **Full `pytest` + gate battery before the PR** — the battery does not run tests and is
   not sufficient evidence on its own (operational rule 16).

Gate: RESOLVED if `lab/research_utils/attested_patch.py` + `eval_lock_geometry.py` exist
∧ both RED-first tests (step 3) are green ∧ every in-scope open site from step 6 is
migrated with a verified no-drift diff ∧ every closed-verdict site is explicitly listed as
left-untouched (not silently skipped) ∧ the new methodology pointer (step 7) lands ∧ F3 is
closed with a citation to this spec ∧ full suite green. FALSIFIED — n/a (this is a build,
not a measurement); a closed-verdict site that turns out to need re-scoring is a **new**,
separately pre-registered probe, never a silent edit here.

Boundary: never retroactively re-score a campaign that already carries a published
`RESULTS*.md` verdict — migrating its code to the new primitive is explicitly **out of
scope** for this spec, even where the audit's own site list names it. Never touch
`core/firm_rules.py`'s already-corrected default (`1_000_000.0`) — this spec is about the
*application pattern*, not the constant, which is not in dispute. No engine change beyond
the two new `lab/research_utils/` modules. No new dependency. Do not fold in the
gap_stage2_capbound.eval_sim hard-coded-literal defect (M-24 encoding 3) — that is a
distinct, unfixed encoding of the same venue fact and needs its own scoping, not a
drive-by fix bundled into this migration.

Reads: [2026-08-03 gate-stack audit §5.1 F3](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md) ·
[M-23 / M-24 lessons](../methodology/lessons/methodology_lessons.md) ·
`core/firm_rules.py:340-370` · [regime_robustness_gate.md Implementation notes](../methodology/regime_robustness_gate.md)
(the sibling "library-graduation clause" — already discharged, for `core/mc/modes.py::_run_half_panel`;
**do not conflate the two** — that graduation covers the half-panel regime-robustness
pattern, this spec covers the dd_lock_offset_usd attestation pattern; they are different
clauses that happen to share vocabulary) ·
`lab/analysis/c1/tradeify_eval_lock_correction_2026-07-22/remc_eval_lock_fix.py` ·
`lab/analysis/c1/aegis3leg_engine_param_2026-08-20/run_aegis1p_rescore_parameterized.py`
Verify (Phase-0, Cursor runs before building): `grep -n "dd_lock_offset_usd" core/firm_rules.py | head -5`
(expect `1_000_000.0`/unreachable, confirming the constant fix already landed) ·
`rg -l "dd_lock_offset_usd" lab/analysis/ | wc -l` (expect ≈40, confirming the site count
this spec's step 2 sweep must re-classify) · `ls lab/research_utils/attested_patch.py`
(expect: does not exist yet)
Owner: [2026-08-03 gate-stack audit](../notes/audits/programme-audit/2026-08-03-gate-stack-audit.md)
§5.1 F3 (due 2026-09-01); this spec is F3's frozen execution packet, per the audit's own
Owner column ("Cursor (frozen spec from CC)").
