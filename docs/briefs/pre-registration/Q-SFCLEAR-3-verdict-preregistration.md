# Q-SFCLEAR-3 — Personal clearance of the Tradeify book at R1: verdict pre-registration (successor)

**Status:** DRAFT — NOT RATIFIED
**Supersedes:** [Q-SFCLEAR-2](Q-SFCLEAR-2-verdict-preregistration.md) at freeze commit F₂ `83867f0d362931c2a516a62b990bb1c209372527`, SUPERSEDED-BEFORE-RUN 2026-10-13. Its frozen design cannot execute on the bound data (§S row 1). Nothing was scored, exported or replayed under it, and no run record exists.
**Authority:** Joshua, 2026-10-13, directly to the Deployment Coordinator, verbatim: "go with B, draft the successor pre-registration", choosing option B of the coordinator's packet (successor pre-registration; same R1 tuple; 15:55 flatten priced at the adverse intrabar placement, exposed legs only).
**Authored:** 2026-10-13, Deployment Coordinator. Joshua owns the ratification.

**Incorporation.** The text of Q-SFCLEAR-2 at F₂ governs this study in full, including the privacy rule and every ruling it records, **except where §S changes it**. F₂ is an immutable commit; "Q-SFCLEAR-2 §n" below means that text at F₂. Where Q-SFCLEAR-2 names itself, its freeze, its hooks or its run records, read Q-SFCLEAR-3 and §S.

## §D — Disclosure: what was seen before this successor was written

- Everything in Q-SFCLEAR-2 §D and §8 (exposure log entries 1–14), unchanged.
- **2026-10-13, Deployment Coordinator (this session):** read card B's build at `9a899a3` (#833, public code) and found the §S row 1 defect; read in place the two private ports' `checkpoint()` structure (no value; card B amendment, #831); read `R1_TUPLE.json`'s key names and types and the `E_0` file's encoding shape (no value; card B addendum (b), #831). No export, replay, screen, MC, growth, hit, MAE, T00 step-3 or trial-9 output was read; the T00 step-3 verdict label is the only result known (public).
- No replay, export or scoring has run under Q-SFCLEAR-2 or this file.

## §S — What this successor changes

| # | Finding | Change |
|---|---|---|
| 1 | Q-SFCLEAR-2 §7 PR applies TB-S3 §5 semantics, "flatten at flatten start with market fill". On every PERMITTED row flatten start is 15:55 ET (Q-SFCLEAR-2 §3), strictly inside the 15:45–16:00 M15 bar; the bound panels are M15 only and no finer historical data exists in the repo or its private stores. Card B (#833, row B5) refuses a session without finer chronology at each schedule instant, so the frozen run cannot start on any day | **§7-A (new):** the 15:55 flatten-start instant is placed by the **ratified path-position bracket convention** ([schedule-execution evidence, addendum 2026-09-23](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23); `ops/c1_rail/qualification/bracket.py`), **run R1 only**, for each leg exposed at that instant (signed position ≠ 0, a broker-pending order, or a capacity reservation): a position is placed at its adverse path vertex (low for a long, high for a short); a pending-only leg at the close vertex (the fill chronology). The flatten fills at the placed `prefix.close` under the existing reference cost model. An unexposed leg needs no split and consumes no 15:55 price. Cutoff 15:45 and own-flat 16:00 are bar boundaries and keep Q-SFCLEAR-2's rules unchanged |
| 2 | The ratified convention is a two-run bracket whose verdict counts a path only where R1 and R2 agree (UNDETERMINED otherwise); Joshua chose the bracket over adverse-only for T00 (2026-09-23) | This study uses **R1 alone** (single-run, conservative-leaning). Disclosed: R1's adverse vertex is an adverse placement on the accepted path, **not a proven worst case** (the path can reach a favourable fill first), and legs are placed independently. Joshua rules this at §12 step 1 (s1). No R2 run enters the verdict |
| 3 | Label | A RESOLVED verdict reads "clears on exposed history (model-fitted; 15:55 flatten at the R1 adverse intrabar placement)". No out-of-sample claim. A NOT CLEARED means not cleared under this placement, not proof that the book fails |
| 4 | Fidelity gate | **FG item 5 (new; Q-SFCLEAR-2 §7 FG list):** on the full R1 PR replay, every 15:55 instant inside a bar is split exactly when the leg is exposed, every split is the R1 placement for that leg's exposure, and no unexposed leg is split. PASS = 100% conformity with zero missing and zero extra splits; the split count stays private. Items 1–3 are unchanged |
| 5 | Forbidden moves (adds to Q-SFCLEAR-2 §5) | Running, reporting or consulting an R2 placement, or any other 15:55 placement, as a verdict input; changing the placement after any output exists; interpolating a 15:55 price; previous-close pricing or next-bar flatten (excluded by the convention). Optional private R2 sensitivity only if §12 step 1 (s2) admits it |
| 6 | Freeze record | Q-SFCLEAR-2's private freeze record (sha256 `91c2754e6373f39ed8ae2f522854fed5333568213157d23d33bb31ad7b1e5425`, pinned in F₂) is **reused by hash**: its G1, G3 and Vanguard drift values come from the bound calculator on stop distances and bar-open gaps, which §S row 1 does not touch. Its fee and margin snapshot hashes carry; a snapshot older than 30 days at this file's freeze is re-taken and hashed into a new nonce'd private record pinned in F₃ (Q-SFCLEAR-2 §4 item 2) |
| 7 | Trial accounting (Q-SFCLEAR-2 §8) | **K stays 12.** The tuple is unchanged (`62d7ae19…671f`), so trial 10 carries. Q-SFCLEAR-2's freeze consumed no data; the manifest lists F₂ under trial 10 `superseded_before_run_freezes` and receives F₃ as `successor_freeze_commit` |
| 8 | Run records and closure | Run records stay at `lab/analysis/c1/sfclear_2026-10/run_records/` and must descend from F₃ (§10 hook 4). The closure is `docs/briefs/closures/Q-SFCLEAR-3-*`. Q-SFCLEAR-2 gets no run record and no verdict |
| 9 | Code consequences (not scoring items) | Card B amendment (c) replaces its unconditional finer-chronology refusal at 15:55 with the R1 placement for exposed legs via `bracket.py`; the source bundle's `splits` become unused for 15:55; FG executor card #808 adds item 5; cards D and E bind F₃. Each lands as its own reviewed change before FG |

Everything not listed — book identity and R1 (§2), the binding gates and calculator (§3), the hypothesis, the 18 drawdown, 3 growth, G1, G3, G1-D, G3-D and B2 cells, seeds, windows, fees, margin, G0 and G4 (§4), the verdict table (§6), routes PR for all legs (§7, item 4 ruling), deployment preconditions (§9) and the privacy rule — is Q-SFCLEAR-2's, unchanged.

## §0 — Reads

Q-SFCLEAR-2 §0, plus (public, `origin/main` at drafting): `ops/c1_rail/qualification/personal_replay.py` at #833 head `9a899a3` (the 15:55 refusal, `verify_inputs`/`_verify_retained`); `ops/c1_rail/qualification/bracket.py` and `replay.py:184` (`accepted_path`); `production_source.py:390-428` (`vertex_split`, `placement`, `_require_exposure`); the [convention addendum](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23); `core/data/bar_data/` (M15 panels only). Private reads: §D.

## §1 — Context and rulings

Q-SFCLEAR-2 §1 unchanged (O2, D2–D10, rulings (a)–(d), the E0-bound ruling), plus the authority line above and the 2026-09-23 ratification of the path-position bracket convention (its R1 run is used alone here, §S row 2).

## §4 — Hypothesis and clearance tests

**H-SFCLEAR-3:** if the Tradeify book at R1 under P0 is fit for the personal account at `E_0`, then on the exposed history, with the 15:55 flatten placed by §S row 1, it meets every binding cell of Q-SFCLEAR-2 §4 (18 drawdown cells, 3 growth cells, G1, G3, G1-D, G3-D, B2, item 7, no Striker total-DD trip). **Reject (NOT CLEARED) if** any binding cell fails. The statistic, cells, seeds and windows are Q-SFCLEAR-2 §4's, unchanged; the label is §S row 3.

## §5 — Forbidden moves

Q-SFCLEAR-2 §5 unchanged, plus:

- Running, reporting or consulting an R2 placement, or any other 15:55 placement, as a verdict input.
- Changing the 15:55 placement, or splitting an unexposed leg, after any output exists.
- Interpolating a 15:55 price, previous-close pricing or next-bar flatten.
- Producing the R2 sensitivity report unless §12 step 1 (s2) admits it.

## §6 — Verdict table

Q-SFCLEAR-2 §6 unchanged: FREEZE INVALID (judged by §10 hook 4 below), then VOID (with "FG not PASS" including item 5, §S row 4), then RESOLVED or NOT CLEARED. Gate mapping for the coordinator: RESOLVED → RESOLVED; NOT CLEARED → FALSIFIED for R1 under this placement; FREEZE INVALID or VOID → AMBIGUOUS (no standing).

## §10 — Audit hooks

Hooks 1–3, 5 and 6 are Q-SFCLEAR-2 §10's, unchanged (hook 5 expects `12 [10, 11, 12]` and trial 10's `successor_freeze_commit` equal to F₃ once recorded). Hook 4 is replaced:

```bash
# 4. Freeze chronology for Q-SFCLEAR-3 (prints nothing when sound)
P=docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md
S=lab/analysis/c1/sfclear_2026-10
F=$(sed -n 's/^Q-SFCLEAR-3 pre-registration commit hash: `\([0-9a-f]\{40\}\)`.*/\1/p' docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md)
if [ -z "$F" ]; then echo 'NOT FROZEN: no Q-SFCLEAR-3 freeze commit recorded'; else
  L=$(git show "$F:$P" | grep '^\*\*Status:\*\* `FROZEN')
  git show "$F" -- "$P" | grep -q '^+\*\*Status:\*\* `FROZEN' || echo 'F DID NOT SET FROZEN'
  echo "$L" | grep -q 62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f || echo 'NO FULL TUPLE RE-HASH ON THE STATUS LINE'
  echo "$L" | grep -qi 'exposure attestation' || echo 'NO EXPOSURE ATTESTATION ON THE STATUS LINE'
  echo "$L" | grep -q '2026-10-11T23:39:57Z' || echo 'ATTESTATION DOES NOT NAME THE DISCLOSED T00 EXPOSURE'
  R=$(echo "$L" | sed -n 's/.*ratify Q-SFCLEAR-3 at \([0-9a-f]\{40\}\).*/\1/p')
  if [ -z "$R" ]; then echo 'NO RATIFIED DRAFT COMMIT ON THE STATUS LINE'; else
    git merge-base --is-ancestor "$R" "$F^" || echo 'RATIFIED COMMIT IS NOT BEFORE F'
    git diff --quiet "$R" "$F^" -- "$P" || echo 'TEXT CHANGED AFTER RATIFICATION'
  fi
  [ "$(git show "$F:$P" | grep -c '^\*\*Status:\*\*')" = 1 ] && [ "$(git diff --numstat "$F^" "$F" -- "$P" | cut -f1-2)" = "$(printf '1\t1')" ] || echo 'F CHANGES MORE THAN THE STATUS LINE'
  [ "$(git log --format=%H -G'^\*\*Status:\*\* .FROZEN' -- "$P" | tail -1)" = "$F" ] || echo 'F IS NOT THE FIRST COMMIT TO SET FROZEN'
  git merge-base --is-ancestor 83867f0d362931c2a516a62b990bb1c209372527 "$F" || echo 'F DOES NOT DESCEND FROM F2'
  grep -q '^91c2754e6373f39ed8ae2f522854fed5333568213157d23d33bb31ad7b1e5425  t00-step3-console/sfclear2-freeze-' docs/evidence/PRIVATE_EVIDENCE.sha256 || echo 'REUSED FREEZE RECORD NOT IN PRIVATE_EVIDENCE'
  FROZEN=("$P" docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md "$S/schedule" "$S/build_historical_schedule.py")
  for f in "$S"/run_records/*.json; do [ -e "$f" ] || continue
    read -r h s < <(python -I -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['run_head'], d['private_sha256sums_sha256'])" "$f" | tr -d '\r')
    git merge-base --is-ancestor "$F" "$h" || echo "PRE-FREEZE RUN HEAD $f"
    git diff --quiet "$F" "$h" -- "${FROZEN[@]}" || echo "FROZEN FILES CHANGED BEFORE RUN $f"
    git merge-base --is-ancestor "$F" "$(git log --diff-filter=A --format=%H -- "$f" | tail -1)" || echo "RECORD COMMITTED BEFORE FREEZE $f"
    grep -q "^$s " docs/evidence/PRIVATE_EVIDENCE.sha256 || echo "NO PRIVATE_EVIDENCE ROW $f"
  done
  for c in $(git log --format=%H -- 'docs/briefs/closures/Q-SFCLEAR-3-*'); do
    git merge-base --is-ancestor "$F" "$c" || echo "PRE-FREEZE CLOSURE $c"
    git diff --quiet "$F" "$c" -- "${FROZEN[@]}" || echo "FROZEN FILES CHANGED BEFORE CLOSURE $c"
  done
fi
```

## §11 — Open facts (carried)

Q-SFCLEAR-2 §11 items 6, 7, 9, 11, 12 and 14 carry unchanged; items 1, 2, 3, 4, 10 and 13 are being discharged by the run-path cards (A, C merged; B in review). New: card B amendment (c) and #808 item 5 (§S row 9).

## §12 — Freeze procedure

Status stays **DRAFT — NOT RATIFIED** until Joshua acts:

1. Joshua confirms, in his own words, the §S changes, and rules:
   - **(s1)** the 15:55 instant uses the convention's R1 run alone, with the "not a proven worst case" disclosure (§S row 2); or the full two-run bracket, where any path whose verdict depends on the run is UNDETERMINED (which would need its own verdict rule and a further successor);
   - **(s2)** whether a private, non-binding R2 sensitivity report (the same run with R2 placement, cell values private, standings never public, no verdict effect) is produced after the binding run; default **no**.
   - **Ruled 2026-10-13 (Joshua, directly to the Deployment Coordinator, verbatim: "R1 alone, no R2 report"):** (s1) R1 alone; (s2) no R2 sensitivity report. §S rows 2 and 5 apply as drafted; any R2 run is a forbidden move.
2. **Required, recorded:** Joshua re-hashes `R1_TUPLE.json` himself (Q-SFCLEAR-2 §10 hook 1) and states the full 64-hex digest verbatim.
3. Joshua states "ratify Q-SFCLEAR-3 at <40-hex commit>", naming the committed draft he reviewed.
4. The coordinator checks the reused freeze record's `PRIVATE_EVIDENCE` row and the fee and margin snapshot ages; a snapshot older than 30 days is re-taken into a new nonce'd private record (§S row 6).
5. **Freeze commit F₃** changes only this file's Status line, to ``**Status:** `FROZEN <date>` `` followed by Joshua's step 1–3 words verbatim and an **exposure attestation** complete through F₃: Joshua's and the coordinator's statement of every T00 step-3, trial-9 replay, screen or MC output either has seen, naming the 2026-10-11T23:39:57Z opening (Q-SFCLEAR-2 §D), with Joshua's re-confirmation in his own words. A later metadata commit records `Q-SFCLEAR-3 pre-registration commit hash: \`<F₃>\`` in the parent brief and F₃ in the lineage manifest (trial 10). §10 hook 4 then prints nothing.
6. After the freeze no constant moves; a change is a new pre-registration.
