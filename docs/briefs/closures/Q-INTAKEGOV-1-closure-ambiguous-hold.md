# Q-INTAKEGOV-1 — CLOSURE: `AMBIGUOUS-HOLD` (limbs split — B2 holds, D2 confirms, C4 confirms)

**Verdict:** `AMBIGUOUS-HOLD` — combined verdict per parent §6; per-limb split recorded verbatim, not averaged
**Closed:** 2026-08-23
**Lane:** UNASSIGNED
**Pre-registration:** [`Q-INTAKEGOV-1-verdict-preregistration.md`](../pre-registration/Q-INTAKEGOV-1-verdict-preregistration.md) — frozen 2026-08-23, before Phase 1 results read
**Successor:** none named — Forbidden Move #4 bars proposing or naming remediation under this brief; see Iterate block for what a future operator-elected decision packet would carry
**Spend / K:** $0.00 · K consumed: 0 (pure-read audit; `check_advisor_dedup.py --keywords` run is $0)
**Live effect:** none — governance/methodology-coverage question only; no `core/`, `dd_protection`, Pine, allocation, or rail content touched
**Artifacts:** none new — this closure + its pre-registration are the only artifacts; all evidence is inline citations against existing files

---

## 1. Verdict (§6 asserted against actual numbers)

| §6 route | Trigger | Actual | Fired? |
|---|---|---|---|
| `RESOLVED` | All three limbs `hold` | B2 holds; D2 confirms; C4 confirms | — |
| `FALSIFIED` | All three limbs `confirm` | B2 holds (not confirm) | — |
| `AMBIGUOUS-HOLD` | Limbs split (mixed confirm/hold) | **B2 = holds** (no undercount found in the 14 available ledgered runs); **D2 = confirms** (mechanism-level dedup query returns no genuine hit for MNQ-ANALOGUE-1 despite `docs/adr/` carrying the answer); **C4 = confirms** (no scheduled/symmetric re-examination mechanism exists anywhere for a standing REJECTED verdict — one candidate check of that shape was built and then dropped) | ✓ |

## 2. What the pre-registration predicted vs what happened

- **B2 predicted:** at least one ledgered `K_intrinsic` undercount, cross-checked against prose or commit history. **Actual:** all 14 closed ledger runs' declared K matched their own prose/params disclosure on inspection; the two runs with the largest apparent K-tension (`st_eh_supertrend_grid` 84→2, `disccamp0_gc_2010_18` 154,912→3,177) turned out to be transparently disclosed provenance splits, not hidden undercounts. **Surprise:** a real, automated K cross-check *does* now exist in the tool (`_require_deep_admission`, `register_search.py:484`, `K == grammar.generation_budget`) — but it landed via a later ADR (2026-08-16/22) and governs zero of the 14 completed runs; the self-report exposure the brief named remains live for every run opened under the older lanes, including anything opened after this session. Git-log cross-check (the pre-registration's second branch) was structurally unavailable for all 14 runs — the repo's pre-2026-08-14 history is squashed to one "Initial public release" commit.
- **D2 predicted:** zero/near-zero dedup-query score for a docs/adr/-only construct. **Actual:** the literal score was not zero (10, on `ops/instruments/MNQ.md`) — but verified by direct grep that "hit" is pure keyword noise (that file never mentions MNQ-ANALOGUE-1 or "analogue"); the one corpus file that legitimately names the construct (`docs/SESSIONS.md`) doesn't rank in the top 30. Substance test (does the query surface *genuine* prior art) failed cleanly, confirming the limb despite the literal score not being exactly zero.
- **C4 predicted:** no hook beyond counting, no re-examine-shaped diagnostic. **Actual:** confirmed, plus one piece of corroborating evidence the brief didn't anticipate: `scripts/check_status_consistency.py`'s own docstring records that a "C1 status-contradiction check" — the shape closest to what C4 is asking for — was designed, built, run once, and explicitly dropped for false-positive reasons. The repo's tooling has already tried this and backed away from it, which is stronger evidence than a mere absence.

## 3. What this closure does NOT license

- Treating B2's `holds` verdict as proof the self-report brake is safe going forward — it is a negative finding on the *available sample* (14 runs, all pre-dating this session), not a structural guarantee; 0 of those 14 runs had any automated K cross-check, and the one such check that now exists (`lane=deep`) has never governed a completed run.
- Treating D2's non-zero dedup score as evidence the corpus caught MNQ-ANALOGUE-1 — verified false positive; the genuine hit does not rank.
- Proposing, under this closure, to add `docs/adr/` to `check_advisor_dedup.py`'s corpus or a re-examination cadence to `programme-audit/SKILL.md` — barred by the parent brief's Forbidden Move #4; any remediation is a separate decision packet requiring its own operator GO.
- Reading this AMBIGUOUS-HOLD as symmetric across limbs — it is not; D2 and C4 are settled *confirmed* findings (a live gap exists), B2 is a *held* finding (no live instance found this round, exposure unresolved).

## 4. Defects found in the frozen brief (recorded, not repaired)

- Parent brief's Section 0 anchor `lab/discovery/register_search.py:599-601` is stale — current line numbers for the `--search-space-size` argument and related logic have moved (now ~440-512, 640-720, 884) as the file has grown since 2026-08-18. Content read (not line numbers) was verified directly; does not change any limb's verdict.
- Parent brief's Section 0 citation of `check_advisor_dedup.py`'s corpus as exactly five surfaces is stale — two more (`ops/instruments/`, `docs/briefs/rnd-pipeline/`) have been added since 2026-08-18. `docs/adr/` remains absent from all seven; does not change the D2 verdict.

## 5. Lesson candidates

**2026-08-23 — a governance mechanism can be theoretically-sound-on-paper and still have a live, evidenceable blind spot for the one surface (`docs/adr/`) where kills are increasingly recorded, while the self-report brake it's paired with holds up empirically on direct inspection even though it has zero automated backing.** Below the two-incident bar for a standing lesson on its own — watch alongside the family K-bank episode this brief was already scoped against (same root pattern: written-strict language, no scheduled mechanical check, discovered by chance/audit rather than by the mechanism itself).

---

## Iterate — loop exit (MANDATORY — closure incomplete without it)

- **Verdict used:** `AMBIGUOUS-HOLD` (limbs split: B2 holds, D2 confirms, C4 confirms)
- **Model update:** The self-report K brake (B2) is less leaky in practice than its structural description suggested — no live instance surfaced across every available ledgered run — but this is closer to "the sessions writing these manifests have been careful" than "the mechanism enforces it," since 0/14 runs had any automated check. The dedup corpus (D2) and the rejected-registry re-proposal gate (C4) are confirmed live gaps, not merely theoretical ones — D2 in particular is worse than the brief's own prediction shape: it doesn't just miss, it returns *plausible-looking noise* in place of the real hit, which is a more dangerous failure mode than a clean zero.
- **Next:** ITERATE
- **Routing:** ITERATE — B2 returns to Investigate (tighter test) at the next relevant touch: the next `register_search open` close, cross-check its declared K against seed-manifest prose the same way. D2 and C4 do not need re-testing (they are confirmed, not held) — their disposition is available as evidenced input to a future, separately-GO'd remediation decision packet; naming that packet is not done here per Forbidden Move #4.
- **Entry packet:** *(required — Next=ITERATE)* For B2's successor touch: carry forward that `lane=mechanism-first`/legacy is 100% self-typed K with zero automated cross-check (only `lane=deep`, added 2026-08-16/22, has one, and it has never governed a completed run); carry forward the two false-alarm patterns already cleared (operator-stop K rewrite with `declared_K` preserved; raw-vs-floor K distinction with the raw figure disclosed) so a future check doesn't re-flag them. For D2/C4 (confirmed, not re-tested): carry forward the exact MNQ-ANALOGUE-1 mechanism-term query and its false-positive/buried-hit result as a worked example; carry forward the `check_status_consistency.py` "C1 check, built then dropped" precedent as evidence a symmetric check was already attempted once.
- **Stop rule / re-proposal bar:** B2 re-tests at the next discovery run's close (per parent §6 template). D2 re-opens only with new mechanism evidence that the corpus gap has since been closed (a new surface added, or the same query re-run and now surfacing the real hit) — not a re-ask of the same question. C4 re-opens only if a genuine scheduled/symmetric re-examination mechanism is later built (would flip that limb to `holds`) — not on a mere restatement of the gap.
- **Board write:** `STATE.md` forward-board row: "Q-INTAKEGOV-1 closed AMBIGUOUS-HOLD 2026-08-23 — B2 holds (re-test at next discovery-run close), D2/C4 confirmed live gaps (dedup corpus excludes docs/adr/; no re-examination mechanism for REJECTED verdicts) — remediation not opened, operator election owed if pursued." Owner: this closure.
- **Registry:** `n/a — governance/methodology-coverage audit, not a strategy-grounds kill.` No `rejected_candidates.md` row owed.

---

## §10 audit-hook discharge

```text
# Limb B2 — ledger read (discovery_manifests/, 14 run manifests, all closed)
ls discovery_manifests/*.json → 17 files (14 run manifests + burned_segments.json + grow0_grammar.json, both non-run auxiliary — confirmed by content, no run_id/status fields)
grep -n "search-space-size\|search_space_size\|K_intrinsic" lab/discovery/register_search.py → K==grammar.generation_budget cross-check exists only at line 484, inside _require_deep_admission() (lane=deep only); no ledgered run uses lane=deep
git log --oneline -- lab/discovery/register_search.py → 4 commits, all >= 2026-08-14 (squashed public-transition history; no per-run git-log cross-check possible for any of the 14 manifests, all opened before the squash)

# Limb D2 — dedup corpus query
python scripts/check_advisor_dedup.py --keywords "1-NN analogue direction rule no forward information leave-one-out hit rate session-block CI straddling zero"
  → top score 10 (ops/instruments/MNQ.md) — verified false positive (file never mentions MNQ-ANALOGUE-1/"analogue")
  → --top 30 rerun: docs/SESSIONS.md (which DOES carry the slug, lines 164/2387) does not appear
rg -il "1-NN|analogue direction|leave-one-out|0.5160|0.5453" docs/adr/*.md
  → docs/adr/2026-08-15-no-counterparty-statistical-sourcing-channel.md (1 file, confirmed outside every load_corpus() surface)

# Limb C4 — reactive-only re-proposal gate
grep -rn "rejected_signals.md\|rejected_candidates.md" docs/notes/audits/ → ~30 hits, all census/forward/feed-completeness/retraction-shaped, none a re-examination trigger
grep -n "REJECTED" docs/methodology/rejected_signals.md docs/rejected_candidates.md | wc -l → 3
grep -inE "re-examine|reconsider|revisit" .claude/skills/programme-audit/SKILL.md → 1 hit, L101, "Stable"-verdict continuity, confirmed unrelated
grep -rn "rejected_candidates\|rejected_signals" scripts/check_status_consistency.py → docstring records a "C1" reconsideration-shaped check "designed but DROPPED after its first real run"
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-08-23 | Closure filed — AMBIGUOUS-HOLD; B2 holds, D2 confirms, C4 confirms; no successor named per Forbidden Move #4 | Claude Code (operator GO, in-session) |

---

## Verification

```bash
python scripts/check_closure_disposition.py docs/briefs/closures/Q-INTAKEGOV-1-closure-ambiguous-hold.md
grep -c "Fired?" docs/briefs/closures/Q-INTAKEGOV-1-closure-ambiguous-hold.md
```
