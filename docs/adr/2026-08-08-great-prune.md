# ADR 2026-08-08 — The Great Prune: obligation-first documentation deletion

**Status:** `Accepted` — operator (JA) approved the prune plan in-session 2026-08-08; merge of the prune PR is the executed ratification. **Tier: full** — doctrine limb fires (standing retention law + mass deletion of decision records).
**Decision date:** 2026-08-08
**Authors:** Joshua (direction) + Claude Code (audit + plan + execution)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none — standing law; §4 falsifiers ride the 2026-11-08 audit
**Operator direction (verbatim):** *"there is a lot of unnecessary documentation that introduces undue friction in our research and deployment pipeline. I want to do an aggressive deletion of docs that are not aiding in the mission of the strategy pipeline, which is to generate → evaluate → deploy → measure → update. … I expect the total repo size to reduce by 25-50%."*
**Snapshot tag:** `pre-prune-2026-08-08` (annotated, pushed; = `origin/main` @ `71b516c` branch point). **Every deleted byte is retrievable:** `git show pre-prune-2026-08-08:<path>`.
**Evidentiary basis:** [`2026-08-08 quarterly audit`](../notes/audits/programme-audit/2026-08-08-quarterly-audit.md) — both layers **Degenerating**; this prune is the named repair action the protocol requires.

---

## §0 — Rule-0 reads (verified this session, at `origin/main` `71b516c` unless noted)

| Source | What it grounds |
|---|---|
| `git ls-tree -r origin/main --long` aggregation | Baseline: **2,386 tracked files / 29.5 MB**; per-tree table in §3. |
| Sentinel enumeration (post-fix, `dc3f158`) | 47 field-form 2026-08-08 riders; partition 2/37/3/5 (audit note §2). |
| `docs/briefs/INDEX.md` @ origin/main | **4 open briefs:** Q-XMEM-1 · Q-SIGID-1 · Q-FILLTAX-1 · Q-R2FLOW-1. |
| `lab/CATALOG.md` status column | 68 "ACTIVE" vs 4 open briefs — **CATALOG liveness is stale prose-token heuristic; not used as a classifier input.** |
| `core/dd_protection.py:78-79,292-304` · `core/firm_rules.py` · `ops/c1_rail/c1_sizing_host_reference.py` | Live constants + import-time guard + rail consumption — none touched by this ADR. |
| [`W4 ADR`](2026-08-07-w4-minimal-gate-set-dormancy.md) §5 | Forbidden to delete `lab/research_utils` universe_gate/breadth modules — excluded from every delete class. |
| 2026-06-05 prune precedent (`pre-prune-2026-06-05`) | The established delete-under-tag mechanism this ADR scales up. |

## §1 — Decision

Delete every tracked artifact that fails the §2 retention test, under the snapshot tag, in one PR with one commit per class (§3). Adopt the retention test as **standing law** (mirrored into `docs/operational_rules.md`). Collapse the ADR corpus to a live-decision set (~26) plus a one-line-per-ADR tombstone index. Rewrite the root docs to pointer form. The mission pipeline — **generate → evaluate → deploy → measure → update** — is the criterion; documentation exists to serve it, not to be maintained by it.

## §2 — Retention test (standing law after merge)

An artifact SURVIVES iff at least one holds:

- **R1 — pipeline-consumed:** read at decision time by the live pipeline (intake screens EM0–EM5 / envelope / harvest; instrument ledgers; `docs/rejected_candidates.md`; open briefs & their preregs; `discovery_manifests/`; gate scripts that fire).
- **R2 — live safety:** carries a live safety invariant for real money / the rail (M1 chain, RUNBOOK, compliance, arming rules; dd_protection/firm_rules owners and their change-control chain).
- **R3 — re-proposal bar:** primary kill evidence (RESULTS\* + PREREG\* of falsified campaigns; any file an instrument-ledger DEAD row or `rejected_candidates.md` cites as the kill source).
- **R4 — reproducibility manifest:** for non-regenerable bytes (SHA256SUMS, Pine MANIFEST, PORT_MANIFEST).
- **R5 — open obligation:** operator-signed decision with a still-open, dated, *fireable* obligation. An obligation whose check **cannot fire** (audit §2 unfalsifiable census) does not qualify — it tombstones with its disposition recorded in the audit note.

Deliberate consequence of R5: **unfalsifiable ceremony is deletable even when signed.** Revival of anything deleted requires fresh pre-registration under the standing chain — never a lookup (this is already law; the tag makes it cheap).

## §3 — Class manifest (one commit each; keep-sets are exhaustive per class)

| # | Class | Action |
|---|---|---|
| 1 | `lab/archive/` + `docs/ltm/` + `docs/analytics/mc_anchor_evolution/` + `docs/audits/` + `docs/methodology_audit/` | Delete cold mass (~9.3 MB). ⚠ **Amended in-flight — not whole trees.** `docs/ltm/` retains two frozen pre-registrations (`DISC-CAMP-0`, `Q-FEED-1`) and `mc_anchor_evolution/` retains `plot.py`: all three are **R1 pipeline-consumed** (read at runtime as pinned threshold sources / imported), and deleting them broke 11 tests before restoration. See §4a. |
| 2 | `lab/analysis/` closed campaigns | Keep `RESULTS*` + `PREREG*` + `CARD.md` per dir; delete harnesses/panels/tests. **Untouched:** dirs of open briefs (`parity_gen2_2026-08`, `mnq_r2flow_routeb_2026-08`) and harness-protected dirs — any dir a surviving ADR/spec names as executable input to an owed re-run (W1 spec → `class_s_c1_haircut_regime_remc_2026-07-16`; MNQDTL §3.3 → `mnq_stop_distribution_2026-08-02`). |
| 3 | `docs/briefs/` | Delete `closures/`, closed Pre-Qs, spent handoffs, spent 08-08 planning packets, preregs of closed campaigns **except** R3-cited kill sources. Keep: INDEX.md (rewritten), the 4 open briefs, dormant packets with live re-entry conditions named by surviving STATE rows. |
| 4 | `docs/adr/` | Keep §3.1 live set; write `docs/adr/TOMBSTONES.md` (one line each: `date · title · consequence-now · git show pre-prune-2026-08-08:docs/adr/<file>`); delete the rest. ⚠ **Executed narrowly (§3.2):** 10 tombstoned (5 Retired/Superseded/Withdrawn stubs + the 5 hard-core P-gates by operator ruling). The remaining corpus is **retained** — see §3.2. |
| 3, 5–8 | `docs/briefs` · `docs/notes` · `docs/superpowers` · `docs/spec` · `docs/methodology` | ⚠ **HALTED — not executed.** See §3.2. |
| 5 | `docs/notes/` | Keep `rail_build/` + compliance + this cycle's audit note + sentinel queue (truncated to current run) + live notices. Delete dated notes, prior audit bodies, absorbed rulings. |
| 6 | `docs/superpowers/` | Keep `2026-08-02-venue-native-regime-monitor-design.md` + `2026-07-16-mechanism-sourcing-strategy-design.md` (live board refs). Delete the rest. |
| 7 | `docs/spec/` | Keep live screens/targets (EM, MNQDTL-1, third-leg, S-series + index + minimal-spec template, feed-equivalence LOCKED, Phase-4 W1 spec), open preregs (NAS-ECR, C1-DEDUPE). Delete withdrawn/superseded/spent. |
| 8 | `docs/methodology/` | Keep lifecycle · harvest · regime gate · observation routing · 1R estimation · INQHIORI canon · lessons · rejected_signals. Delete Notion mirrors/archive stubs. |
| 9 | `docs/SESSIONS.md` | Truncate to newest 20 entries (history = git). |
| 10 | `tests/` | Delete tests bound to deleted harnesses/scripts only. Keep engine regression (`tests/core/test_mc_synthetic_engine.py`), governance suite, surviving-gate tests. |
| 11 | Root docs | CLAUDE.md → pointer form (~8–10 KB); STATE.md board prune; REPO_MAP; `.rgignore`/`.cursorindexingignore`; retention test into `operational_rules.md`. |

### §3.2 — Why classes 3, 5–8 were HALTED (the prune's own falsifier fired, in-flight)

A 166-file delete set was assembled for `docs/briefs` · `docs/notes` · `docs/superpowers` · `docs/spec` ·
`docs/methodology` — every file surviving three mechanical guards (quoted-path scan, pathlib-join scan,
inbound-markdown-link analysis from survivors). It was then put through a six-agent adversarial review with
the stance *"prove each file is dead."*

**Result: 66 of 69 reviewed files were rescued — classifier precision 4.3%.** Nine rescues would have broken
running code, a live gate, or a live test. The sharpest: deleting
`docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md` makes
`register_search.py::_require_reachability_attestation` **abort**, because
`discovery_manifests/h_od_1_es_overnight_drift.json` names it as a reachability attestation.
`2026-07-15-existing-strategy-book-candidate-2-prereg.md` is reached by **pathlib joins** at
`run_class_s_c2_scoring.py:50-55`. `docs/spec/2026-06-23-inqhiori-sentinel-plan.md` is named by
`ops/sentinel/scan.py:136-140` as the authority for the live scanner's obligation surface.

**Failure mode #5 (the one §4a predicted but could not pre-empt):** references to these documents are
**not markdown links**. They appear as backticked prose paths, `{design,plan}` brace notation, runnable
`rg -n <path>` audit-hook commands inside RATIFIED specs, and `**Related:**` evidence lines in surviving
ADRs. An ADR routinely cites a spec as the *derivation* its own conclusions rest on — deleting the spec
re-creates the phantom-anchor defect that several of those ADRs were written to fix.

**Ruling:** `docs/` is **not** a low-coupling tree. At 4.3% precision no patch to the heuristic is
trustworthy, and the remaining ~3 MB is not worth a live-gate outage. Classes 3, 5–8 are **not executed**
and are **not** deferred as owed work — a future prune of this material must start from an
inbound-reference index built from *prose and hook* citations, not links, and must justify itself against
this measured precision. The delivered reduction (§6) comes from the classes that were safe.

Safety/rail (R2): `2026-07-17-c1-rail-build-account-registration-go` · `2026-07-22-c1-venue-native-monitoring-maturity` · `2026-05-08-dd-trigger-c2-relock` · `2026-08-08-s2b-signal-daemon-build` · `2026-08-07-loop-s2-signal-host-fork` · `2026-08-07-loop-s1-environment-ratification` · `2026-08-07-loop-s5-bounded-promotion-lane`.
Open obligations (R5): `2026-08-04-tradeify-venue-descope-eval-included` (F1, T4) · `2026-07-12-prop-portfolio-four-friendly-firms` (§4 11-08) · `2026-07-22-prop-portfolio-s4-discharge-withdrawal` · `2026-08-07-w1-intraday-honest-engine-remeasure` · `2026-06-07-decompound-remc-hold` (standing HOLD on live posture) · `2026-07-26-mechanism-counterparty-constraint-boundaries` (11-08) · `2026-07-15-external-mechanism-harvest-intake` (11-08) · `2026-08-03-params-toml-gate-retirement` (falsifier window → 11-08; zero-exposure recorded).
Live doctrine/gates (R1): `2026-08-04-family-k-bank-disclosure-not-gate` · `2026-08-05-avenue-a-generate-confirm-route` · `2026-07-12-dsr-k-rule-and-variance-floor-supersession` · `2026-07-10-strategies-never-locked-lifecycle-governance` · `2026-07-13-dd-protection-concept-not-constant` · `2026-08-08-adr-ceremony-tiering` · `2026-08-07-w5-governance-diet` · `2026-08-07-w4-minimal-gate-set-dormancy` · `2026-08-04-iterate-closure-exit-mandatory` · `2026-05-10-manifest-integrity-gate` · `2026-07-01-guardian-pyport-public-tracking` · `2026-06-05-monorepo-layer-boundaries` · **this ADR**.
Operator ruling at PR review: `2026-07-03-hardcore-p1` and `-p3` keep-or-tombstone (default tombstone; obligations recorded in audit note §2). P2/P4/P5 tombstone (moot/unfalsifiable).

## §4a — Classifier failure log (recorded because the retention test is now standing law)

The delete classifier failed **four times in execution**, each time on the same root cause: *a
documentation-shaped file that running code reads.* Recorded so the standing rule is applied with
the right instrument, not the intuition that burned it.

| # | What was nearly (or briefly) lost | Why the classifier missed it | Guard now in place |
|---|---|---|---|
| 1 | `lab/analysis` harnesses imported by sibling campaign code | "closed campaign ⇒ inert" — the tree has an import graph | full `pytest`, not the gate battery |
| 2 | `DISC-CAMP-0` + `Q-FEED-1` frozen pre-registrations | "docs/ltm is cold prose" — they are **pinned threshold sources read at runtime** | quoted-path scan across `core/ ops/ scripts/ tests/ lab/` |
| 3 | `docs/analytics/mc_anchor_evolution/plot.py` | an **executable** living under `docs/` | same scan (extension-agnostic) |
| 4 | `docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json` — **the arming-gate artifact** | `ops/c1_rail/c1_rail_arm.py` builds the path with `pathlib` joins; no string literal exists to grep | hard-protected directory list + `"docs" /` pathlib-join scan |
| 5 | 66 of 69 reviewed docs (precision 4.3%) — incl. a prereg whose absence makes `register_search.py` abort | inbound references are **not markdown links**: backticked prose paths, `{design,plan}` braces, runnable `rg` audit hooks, `**Related:**` evidence lines | classes 3, 5–8 HALTED (§3.2) |
| 6 | **CLAUDE.md's own prose** — the MC-anchor literals `99.83% pass / 0.17% bust` and `p99 DD 4.37%` | `ops/recall/guard.py:~100` **regex-parses CLAUDE.md** to build the recall denylist; the pointer-form rewrite reworded them, silently disabling the guard so it would admit the anchor as authority | literals restored **with an inline warning naming the parser**; caught by full `pytest`, invisible to every gate |

**Standing consequence:** deletion classification MUST run (a) the quoted-path scan, (b) the
pathlib-join scan, (c) inbound-markdown-link analysis from survivors, and (d) a full `pytest` before
the commit lands. The pre-commit gate battery does **not** run tests and is not sufficient evidence.

## §4 — Falsifiers (prune-specific; check at 2026-11-08 audit)

| # | Trigger | Threshold | Action |
|---|---|---|---|
| F-1 | Deleted artifact needed in anger | ≥3 distinct tag-retrievals of deleted content required for live decisions within 90 days | Retention test too aggressive on that class — restore the class, supersede this ADR's §3 row |
| F-2 | Re-accretion | tracked bytes or ADR count regrow ≥50% of the pruned delta by 2026-11-08 (audit hook measures) | The prune treated symptom not cause — escalate to a doc-budget gate (hard, counted, in `gates.yml`) |
| F-3 | Lost obligation | a genuinely live dated obligation is found to have died with a tombstoned carrier, undetected until it mattered | Restore carrier from tag + record the classifier defect here; tighten R5 |

### Addendum 2026-08-14 — F-2 disposition: fired, ruled miscalibrated-premise

**F-2 fired as measured** (`origin/main` `df2c448`: ADR count +14 ≈ 400% of trigger, files +412 ≈ 131%, bytes +2.90 MB ≈ 63%, 6 of 91 days elapsed). Per operator direction, the full live ADR corpus (126 files) was read in full and classified against the §2 retention test, then the resulting deletion candidates were adversarially tested against Rule 16's own 4-part classification instrument. Full evidence: [`2026-08-14-f2-adr-corpus-disposition.md`](../notes/audits/programme-audit/2026-08-14-f2-adr-corpus-disposition.md).

**Result: 4 of 126 (3.2%) classified as deletion candidates on content grounds; 0 of 4 survived adversarial verification.** 92% of the corpus classified KEEP on direct read (safety-critical, historical record, or live), much of it via dependencies a mechanical/keyword classifier would miss (informal supersession fields the graph gate doesn't parse, prose citations without markdown links, doctrine surviving its own implementation's retirement).

**Ruling (operator, 2026-08-14):** F-2's literal prescription — escalate to a hard doc-budget gate — is **declined**. The trigger measured accurately; the inference it was built to test (regrowth ⇒ dead-material accumulation) does not hold under direct content verification. The regrowth reflects genuine decision throughput, not degeneration. A doc-budget gate would tax the next necessary decision, not remove ceremony.

**What is adopted instead:** the falsifier's *instrument* is replaced, not its intent. At each future programme-audit cadence, F-2 is re-tested by a content sample (read N live ADRs in full against Rule 16), not a raw count/byte regrowth measurement. Six genuine partial-edit findings from this pass (dormancy/reconciliation addenda owed on specific ADRs, not deletions) are the real, smaller-than-hoped belt-tightening this cycle earned — tracked in the linked audit note §3, not restated here.

**Open, not decided here:** [`2026-08-12-closure-disposition-coverage-hard.md`](2026-08-12-closure-disposition-coverage-hard.md) self-armed a new HARD/commit-blocking gate 4 days into F-2's own trigger window — the only ADR in the corpus to do so, over a documentation-bookkeeping concern. Whether that gate was the right call sits with the operator; not re-litigated by this addendum.

## §5 — Forbidden moves

- Deleting anything in the guardrail set: `core/`, Pine + SHA manifests, `ops/c1_rail/`, `ops/instruments/`, `discovery_manifests/`, `ops/prop_envelope_default.md`, `docs/rejected_candidates.md`, vendor-data trees, W4-protected modules.
- Restating a tombstoned decision's narrative in CLAUDE.md/STATE.md (the tombstone line + tag is the record; anti-accretion is the point).
- Reviving deleted material by lookup — fresh pre-registration under the standing chain, always.
- Treating this prune as precedent for deleting **measurement evidence** wholesale — R3 keeps kill evidence in-tree by design.
- Using the prune to alter any live decision (MNQDTL-1 §6, lifecycle states, F1, §4 dates all pass through unchanged).

## §6 — Gate (binary, at PR merge)

`RESOLVED` when: full gate battery green (`gate_manifest --tier pre-commit`) · full pytest green (no
prune-caused failure) · sentinel clean run · zero dangling links from the surviving tree · every §3 class
executed **or explicitly halted with its reason recorded** · tag resolvable.

**Outcome:** met. Delivered **29.5 MB → ~20.3 MB (−31%)**, 2,386 → ~1,760 files — inside the operator's
25–50% band, from classes 1, 2, 4 (narrow), 9 and 11. The ≤16 MB figure in the original plan assumed classes
3, 5–8 would execute; §3.2 records why they did not, and that shortfall is a **deliberate, evidenced stop**,
not an unmet obligation. Re-stating it as owed work would be the accretion this ADR exists to prevent.

## §7 — Standing-artifact relations

Supersedes-in-part: `2026-07-16-root-doc-charter-dedup` (charter absorbed into pointer-form CLAUDE.md); STATE's 08-08 board section (discharged by the audit note). Composes with: ceremony tiering (forward instrument), W5 diet (gate composition authority unchanged). Does **not** touch: lifecycle axis, dd_protection chain, venue posture, MNQDTL-1.

## Addendum 2026-08-19 — not a GRAND Subtract

**Does not amend §1 / §2 / §4.** Citation only.

This prune keeps or deletes documentation *parts* under the §2 retention test (object = files/classes; domain = meta-process). It is **not** a GRAND pursuit-Subtract and is not The Algorithm's Delete worked example. Handoff owner: [`2026-08-09-grand-tier-quintessentials-binding.md`](2026-08-09-grand-tier-quintessentials-binding.md) §2.2/§2.4. Live test owner: [`operational_rules.md`](../operational_rules.md) Rule 16. Ruling: [`2026-08-19-great-prune-is-not-grand-subtract.md`](2026-08-19-great-prune-is-not-grand-subtract.md).

## §10 — Audit hooks

```bash
git ls-tree -r HEAD --long | awk '$2=="blob"{s+=$4; n+=1} END {printf "%.1f MB / %d files\n", s/1e6, n}'   # ≤16 MB
ls docs/adr/*.md | wc -l                                                                # ~111 retained + 10 tombstoned (§3.2); grows with ongoing authoring
git tag -l pre-prune-2026-08-08                                                                             # resolvable
python scripts/gate_manifest.py --tier pre-commit                                                           # green
```

## Addendum 2026-08-29 — `pre-prune-2026-08-08` tag not carried into the public clone; §1/§6/§10 retrieval guarantee no longer holds here

The `pre-prune-2026-08-08` tag was **not carried into the public clone** created by
[`2026-08-14-repo-public-visibility-transition.md`](2026-08-14-repo-public-visibility-transition.md)
(fresh "Initial public release" history, not an in-place flip). Verified on this clone as of
2026-08-29: `git tag -l` and `git ls-remote --tags origin` are both **empty**.

Consequence: §1's "Every deleted byte is retrievable: `git show pre-prune-2026-08-08:<path>`" claim,
and the §6/§10 tag-resolvability gate (`git tag -l pre-prune-2026-08-08` expected "resolvable"), **no
longer hold on the public tree**. §6's `RESOLVED` status is retrospective to the pre-transition
environment in which it was evaluated and is **not reopened** by this note. Retrieval of pruned bytes
now requires the private archive (per [`docs/adr/TOMBSTONES.md`](TOMBSTONES.md)'s header) or, for
file history predating 2026-08-14, `git log --follow -- <path>` as a partial fallback — it does not
recover files already deleted before the transition's squash.

Never edit the two addenda above in place — this addendum records the tag-carry gap only.
