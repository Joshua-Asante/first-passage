# Q-SFCLEAR-3 — Personal clearance of the Tradeify book at R1: verdict pre-registration (successor)

**Status:** DRAFT — NOT RATIFIED
**Supersedes:** [Q-SFCLEAR-2](Q-SFCLEAR-2-verdict-preregistration.md) at freeze commit F₂ `83867f0d362931c2a516a62b990bb1c209372527`, SUPERSEDED-BEFORE-RUN 2026-10-13. Its frozen design cannot execute on the bound data (§S row 1). No replay, export or route scoring ran under it and no run record exists; its freeze record's G1, G3 and drift cells were computed (2026-10-12T17:19:04Z) and are reused here (§S rows 6–6b). A new file, not an amendment, because Q-SFCLEAR-2 §12 step 6 makes any change a new pre-registration.
**Authority:** Joshua, 2026-10-13, directly to the Deployment Coordinator, verbatim: "go with B, draft the successor pre-registration", choosing option B of the coordinator's packet (successor pre-registration; same R1 tuple; 15:55 flatten priced at the adverse intrabar placement, exposed legs only).
**Authored:** 2026-10-13, Deployment Coordinator. Joshua owns the ratification.

**Incorporation.** The text of Q-SFCLEAR-2 at F₂ governs this study in full, including the privacy rule and every ruling it records, **except where §S changes it**. F₂ is an immutable commit; "Q-SFCLEAR-2 §n" below means that text at F₂. Where Q-SFCLEAR-2 names itself, its freeze, its hooks or its run records, read Q-SFCLEAR-3 and §S.

## §D — Disclosure: what was seen before this successor was written

- Everything in Q-SFCLEAR-2 §D and §8 (exposure log entries 1–14), unchanged.
- **2026-10-13, Deployment Coordinator (this session):** read card B's build at `9a899a3` (#833, public code) and found the §S row 1 defect; read in place the two private ports' `checkpoint()` structure (no value; card B amendment, #831); read `R1_TUPLE.json`'s key names and types and the `E_0` file's encoding shape (no value; card B addendum (b), #831). No export, replay, screen, MC, growth, hit, MAE, T00 step-3 or trial-9 output was read; the T00 step-3 verdict label is the only result known (public).
- No replay, export or route scoring has run under Q-SFCLEAR-2 or this file. The Q-SFCLEAR-2 freeze record's G1, G3, window-maximum and drift values exist; **this coordinator has not read them** (only the record's hash and its `PRIVATE_EVIDENCE` row). Joshua's and the 2026-10-12 coordinator's exposure to them is attested at §12 step 5.
- **Outcome label bearing on (s1):** the public T00 step-3 label `NO-GO-evidence-UNDETERMINED-dependent` arose from the same bracket convention on the same panels, where R1 and R2 disagreed. Choosing R1 alone removes UNDETERMINED by construction, so (s1) is a design choice made after an outcome label on that dimension. Disclosed here; Joshua's step 5 re-confirmation names (s1).

## §S — What this successor changes

| # | Finding | Change |
|---|---|---|
| 1 | Q-SFCLEAR-2 §7 PR applies TB-S3 §5 semantics, "flatten at flatten start with market fill". On every PERMITTED row flatten start is 15:55 ET (Q-SFCLEAR-2 §3), strictly inside the 15:45–16:00 M15 bar; the bound panels are M15 only. Finer same-feed evidence exists only in part: the private 5-minute evidence used by T00 locates about 52% of needed intrabar splits, and there are no 1-minute exports (T00 build card, 2026-10-10 entries). Card B (#833, row B5) refuses a session without finer chronology at each schedule instant, so the frozen run cannot start on any day | **§7-A (new):** the 15:55 flatten-start instant is placed by the **ratified path-position bracket convention** ([schedule-execution evidence, addendum 2026-09-23](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23); `ops/c1_rail/qualification/bracket.py`), **run R1 only**, for each leg exposed at that instant (signed position ≠ 0, a broker-pending order, or a capacity reservation): a position is placed at its adverse path vertex (low for a long, high for a short); a pending-only leg at the close vertex (the fill chronology). The flatten fills at the placed `prefix.close` under the existing reference cost model. An unexposed leg needs no split and consumes no 15:55 price. A reservation implies a pending order; a reservation-only, or ledger/broker-divergent, leg aborts the replay (`ReplayNeedsContext`, so FG not PASS and VOID) and is not counted as a missing split. Cutoff 15:45 and own-flat 16:00 are bar boundaries and keep Q-SFCLEAR-2's rules unchanged. **Evidence-located rows are excluded:** the [evidence-located placement](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-10-08--evidence-located-placement-ratified-2026-10-09) (ratified 2026-10-09) is not used, so every exposed 15:55 instant takes the R1 vertex, including where 5-minute bars would tile it. Reason: coverage is partial (about 52% on T00), Joshua held R1/R2 with no convention change on 2026-10-10 after that measurement, the FLOOR-HALF successor was judged on the pessimistic assignment, and one rule for every day needs no private 5-minute input or provenance binding in the replay |
| 2 | The ratified convention is a two-run bracket whose verdict counts a path only where R1 and R2 agree (UNDETERMINED otherwise); Joshua chose the bracket over adverse-only for T00 (2026-09-23) | This study uses **R1 alone**. Its direction on the verdict is **not established**: (i) R1's adverse vertex is an adverse placement on the accepted path, **not a proven worst case** (the path can reach a favourable fill first); (ii) for a pending-only leg the convention labels neither run adverse; (iii) legs are placed independently; (iv) an adverse 15:55 fill lowers Vanguard's paper equity `E_p`, so the drift multiple m\* = max(1, max `E_p` ÷ paper capital) can only shrink, which makes G1-D/G3-D easier to pass, and lower equity shrinks later Vanguard sizes, which can lower drawdown exposure. The effect's size is unmeasured. Joshua ruled (s1) (§12); no R2 run enters the verdict |
| 3 | Label | A RESOLVED verdict reads "clears on exposed history (model-fitted; 15:55 flatten at the R1 adverse intrabar placement)". No out-of-sample claim. A NOT CLEARED means not cleared under this placement, not proof that the book fails |
| 4 | Fidelity gate | **FG item 5 (new; Q-SFCLEAR-2 §7 FG list; item 4 was dropped under ruling (j)):** on the full R1 PR replay, every 15:55 instant inside a bar is split exactly when the leg is exposed, every split is the R1 placement for that leg's exposure, and no unexposed leg is split. PASS = 100% conformity with zero missing and zero extra splits, the expected splits re-derived from the exposure log and the M15 bars independently of `placement()`; the split count stays private. Items 1–3 are unchanged |
| 5 | Forbidden moves (adds to Q-SFCLEAR-2 §5) | Running, reporting or consulting an R2 placement, or any other 15:55 placement, as a verdict input; changing the placement after any output exists; interpolating a 15:55 price; previous-close pricing or next-bar flatten (excluded by the convention). Optional private R2 sensitivity only if §12 step 1 (s2) admits it |
| 6 | Freeze record | Q-SFCLEAR-2's private freeze record (sha256 `91c2754e6373f39ed8ae2f522854fed5333568213157d23d33bb31ad7b1e5425`, pinned in F₂) is **reused by hash**: its G1, G3 and Vanguard drift values come from the bound calculator on stop distances and bar-open gaps, which §S row 1 does not touch. Its fee and margin snapshot hashes carry; a snapshot older than 30 days at this file's freeze is re-taken and hashed into a new nonce'd private record pinned in F₃ (Q-SFCLEAR-2 §4 item 2) |
| 6b | Q-SFCLEAR-2 §6's FREEZE INVALID row requires the freeze record "pinned in F", and §4 item 7 and §12 step 3 order G1/G3 after ratification "under this file"; read with F = F₃, both fail by construction for a reused record | **Replaces, for this study only:** the freeze record must be pinned in F₂ (row `91c2754e…` in `PRIVATE_EVIDENCE.sha256`) and present at F₃; a re-taken snapshot record is pinned by a row F₃ adds, matching `t00-step3-console/sfclear3-snapshots-<UTC>/SNAPSHOTS.json`. The (d)-1 ordering for the reused cells is satisfied by Q-SFCLEAR-2's ratification (F₂). Step 5 and hook 4 implement this |
| 7 | Trial accounting (Q-SFCLEAR-2 §8) | **K stays 12.** The tuple is unchanged (`62d7ae19…671f`), so trial 10 carries, on the ground Q-SFCLEAR-2 §6 states ("the trial ledger is unchanged if the successor keeps the tuple"). Q-SFCLEAR-2's freeze record computed G1/G3 but no route scoring ran; the manifest lists F₂ under trial 10 `superseded_before_run_freezes` and receives F₃ as `successor_freeze_commit` |
| 8 | Run records and closure | Run records stay at `lab/analysis/c1/sfclear_2026-10/run_records/` and must descend from F₃ (§10 hook 4). The closure is `docs/briefs/closures/Q-SFCLEAR-3-*`. Q-SFCLEAR-2 gets no run record and no verdict |
| 9 | Code consequences (not scoring items) | Card B amendment (c) replaces its unconditional finer-chronology refusal at 15:55 with the R1 placement for exposed legs via `bracket.py`; the source bundle's `splits` become unused for 15:55; FG executor card #808 (FROZEN) gains item 5 and binds F₃ by a dated amendment carrying Joshua's words, as card B was amended; cards D and E bind F₃. Each lands as its own reviewed change before FG |

Everything not listed — book identity and R1 (§2), the binding gates and calculator (§3), the hypothesis, the 18 drawdown, 3 growth, G1, G3, G1-D, G3-D and B2 cells, seeds, windows, fees, margin, G0 and G4 (§4), the verdict table (§6), routes PR for all legs (§7, item 4 ruling), deployment preconditions (§9) and the privacy rule — is Q-SFCLEAR-2's, unchanged.

## §0 — Reads

Q-SFCLEAR-2 §0, plus public reads at `origin/main` `3703f0a`: `ops/c1_rail/qualification/personal_replay.py` at PR #833 head `9a899a3` (not on main) (the 15:55 refusal, `verify_inputs`/`_verify_retained`); `ops/c1_rail/qualification/bracket.py` and `replay.py:184` (`accepted_path`); `production_source.py:390-428` (`vertex_split`, `placement`, `_require_exposure`); the [convention addendum](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23); `core/data/bar_data/` (M15 panels only). Private reads: §D.

## §1 — Context and rulings

Q-SFCLEAR-2 §1 unchanged (O2, D2–D10, rulings (a)–(d), the E0-bound ruling), plus the authority line above and the 2026-09-23 ratification of the path-position bracket convention (its R1 run is used alone here, §S row 2).

## §4 — Hypothesis and clearance tests

**H-SFCLEAR-3:** if the Tradeify book at R1 under P0 is fit for the personal account at `E_0`, then on the exposed history, with the 15:55 flatten placed by §S row 1, it meets every binding cell of Q-SFCLEAR-2 §4 (18 drawdown cells, 3 growth cells, G1, G3, G1-D, G3-D, B2, item 7, no Striker total-DD trip). **Reject (NOT CLEARED) if** any binding cell fails. The statistic, cells, seeds and windows are Q-SFCLEAR-2 §4's, unchanged; the label is §S row 3.

## §5 — Forbidden moves

Q-SFCLEAR-2 §5 unchanged, plus:

- Running, reporting or consulting an R2 placement, or any other 15:55 placement, as a verdict input.
- Changing the 15:55 placement, or splitting an unexposed leg, after any output exists.
- Interpolating a 15:55 price, previous-close pricing or next-bar flatten.
- Using an evidence-located (5-minute or other finer) row for any 15:55 instant.
- Producing the R2 sensitivity report unless §12 step 1 (s2) admits it.

## §6 — Verdict table

Q-SFCLEAR-2 §6 unchanged: FREEZE INVALID (judged by §10 hook 4 below), then VOID (with "FG not PASS" including item 5, §S row 4), then RESOLVED or NOT CLEARED. Gate mapping for the coordinator: RESOLVED → RESOLVED; NOT CLEARED → FALSIFIED for R1 under this placement; FREEZE INVALID or VOID → AMBIGUOUS (no standing).

## §10 — Audit hooks

Hooks 1–3, 5 and 6 are Q-SFCLEAR-2 §10's, unchanged. Hook 5 expects `12 [10, 11, 12]`; trial 10's `successor_freeze_commit` reads F₂ until the F₃ metadata commit, then F₃, with F₂ listed under `superseded_before_run_freezes`. Hook 4 is replaced:

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
  git show 83867f0d362931c2a516a62b990bb1c209372527 -- docs/evidence/PRIVATE_EVIDENCE.sha256 | grep -q '^+91c2754e6373f39ed8ae2f522854fed5333568213157d23d33bb31ad7b1e5425  t00-step3-console/sfclear2-freeze-' || echo 'REUSED FREEZE RECORD NOT PINNED IN F2'
  git show "$F:docs/evidence/PRIVATE_EVIDENCE.sha256" | grep -q '^91c2754e6373f39ed8ae2f522854fed5333568213157d23d33bb31ad7b1e5425 ' || echo 'REUSED FREEZE RECORD ABSENT AT F3'
  git diff "$F^" "$F" -- docs/evidence/PRIVATE_EVIDENCE.sha256 | grep '^+[0-9a-f]' | grep -vq '  t00-step3-console/sfclear3-snapshots-[0-9TZ]*/SNAPSHOTS.json$' && echo 'F3 ADDS A PRIVATE_EVIDENCE ROW OTHER THAN A SNAPSHOT RECORD'
  RL=$(git show "83867f0d362931c2a516a62b990bb1c209372527:docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md" | grep '^\*\*G4 roll-date list:\*\*'); RH=$(echo "$RL" | grep -oE '[0-9a-f]{64}' | head -1); RP=$(echo "$RL" | grep -oE 'lab/analysis/c1/sfclear_2026-10/schedule/roll_dates[^` ]+' | head -1)
  { [ -n "$RH" ] && [ -n "$RP" ] && [ "$(git show "$F:$RP" | sha256sum | cut -c1-64)" = "$RH" ]; } || echo 'ROLL-DATE LIST AT F3 DIFFERS FROM THE F2 BINDING'
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
  if ls docs/briefs/closures/Q-SFCLEAR-3-* >/dev/null 2>&1 && ! ls "$S"/run_records/*.json >/dev/null 2>&1; then echo 'CLOSURE WITHOUT RUN RECORD'; fi
fi
```

## §11 — Open facts (carried)

Q-SFCLEAR-2 §11 items 6, 7, 8 (G1-D/G3-D after the run), 9, 12 and 14 carry unchanged; item 11 is discharged for the study by #817 and #823 (personal forward calendar and its ratification rows); items 1, 2, 3, 4, 10 and 13 are being discharged by the run-path cards (A, C merged; B in review). New: card B amendment (c) and #808 item 5 (§S row 9).

## §12 — Freeze procedure

Status stays **DRAFT — NOT RATIFIED** until Joshua acts:

1. Joshua confirms, in Joshua's own words, the §S changes, and rules:
   - **(s1)** the 15:55 instant uses the convention's R1 run alone, with the §S row 2 disclosures; or the full two-run bracket, where any path whose verdict depends on the run is UNDETERMINED (which would need its own verdict rule, added to this file);
   - **(s2)** whether a private, non-binding R2 sensitivity report (the same run with R2 placement, cell values private, standings never public, no verdict effect) is produced after the binding run; default **no**.
   - **Ruled 2026-10-13 (Joshua, directly to the Deployment Coordinator, verbatim: "R1 alone, no R2 report"):** (s1) R1 alone; (s2) no R2 sensitivity report. §S rows 2 and 5 apply as drafted; any R2 run is a forbidden move.
   - **(s3) Evidence-located rows:** excluded (§S row 1). Joshua, 2026-10-14, directly to the Deployment Coordinator, verbatim: "go with your best recommendation on 2", delegating the choice between (i) R1 at every exposed 15:55 instant with evidence-located rows excluded and (ii) evidence-located where 5-minute bars tile, R1 elsewhere; the coordinator recommended and applied (i).
2. **Required, recorded:** Joshua re-hashes `R1_TUPLE.json` personally (Q-SFCLEAR-2 §10 hook 1) and states the full 64-hex digest verbatim.
3. Joshua states "ratify Q-SFCLEAR-3 at <40-hex commit>", naming the committed draft he reviewed.
4. The coordinator checks the reused freeze record's `PRIVATE_EVIDENCE` row and the fee and margin snapshot ages; a snapshot older than 30 days is re-taken into a new nonce'd private record, `t00-step3-console/sfclear3-snapshots-<UTC>/SNAPSHOTS.json` (§S rows 6–6b).
5. **Freeze commit F₃** changes only this file's Status line (and, only if step 4 re-took a snapshot, adds that record's one `PRIVATE_EVIDENCE.sha256` row), to ``**Status:** `FROZEN <date>` `` followed by Joshua's step 1–3 words verbatim and an **exposure attestation** complete through F₃: Joshua's and the coordinator's statement of every T00 step-3, trial-9 replay, screen or MC output either has seen, naming the 2026-10-11T23:39:57Z opening (Q-SFCLEAR-2 §D), and stating whether either has seen any of the Q-SFCLEAR-2 freeze record's G1, G3, window-maximum or drift values, with Joshua's re-confirmation in Joshua's own words of (s1) and (s2) knowing the §D disclosures. A later metadata commit records `Q-SFCLEAR-3 pre-registration commit hash: \`<F₃>\`` in the parent brief and F₃ in the lineage manifest (trial 10). §10 hook 4 then prints nothing.
6. After the freeze no constant moves; a change is a new pre-registration.
