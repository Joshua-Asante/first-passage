# Q-SFCLEAR-3 — Personal clearance of the Tradeify book at R1: verdict pre-registration (successor)

**Status:** DRAFT — NOT RATIFIED
**Supersedes:** [Q-SFCLEAR-2](Q-SFCLEAR-2-verdict-preregistration.md) at freeze commit F₂ `83867f0d362931c2a516a62b990bb1c209372527`, SUPERSEDED-BEFORE-RUN 2026-10-13. Its frozen design cannot execute on the bound data (§S rows 1 and 1b). No replay, export or route scoring ran under it and no run record exists. Its private freeze record (G1, G3 and drift cells computed 2026-10-12T17:19:04Z) is **not used**: this study computes its own (§S row 6). A new file, not an amendment, because Q-SFCLEAR-2 §12 step 6 makes any change a new pre-registration.
**Authority:** Joshua, 2026-10-13, directly to the Deployment Coordinator, verbatim: "go with B, draft the successor pre-registration", choosing option B of the coordinator's packet (successor pre-registration; same R1 tuple; 15:55 flatten priced at the adverse intrabar placement, exposed legs only).
**Authored:** 2026-10-13, Deployment Coordinator. Joshua owns the ratification.

**Incorporation.** The text of Q-SFCLEAR-2 at F₂ governs this study in full, including the privacy rule and every ruling it records, **except where §S changes it**. F₂ is an immutable commit; "Q-SFCLEAR-2 §n" below means that text at F₂. Where Q-SFCLEAR-2 names itself, its freeze, its freeze record, its hooks or its run records, read Q-SFCLEAR-3 and §S.

## §D — Disclosure: what was seen before this successor was written

- Everything in Q-SFCLEAR-2 §D and §8 (exposure log entries 1–14), unchanged.
- **2026-10-13/14, Deployment Coordinator (this session):** read card B's build (#833, public code) and found the §S row 1 defect; read in place the two private ports' `checkpoint()` structure (no value; card B amendment, #831); read `R1_TUPLE.json`'s key names and types and the `E_0` file's encoding shape (no value; card B addendum (b), #831); counted panel timestamps per leg and session window (no price, volume or outcome; §S row 1b); built the private source bundle (`t00-step3-console/sfclear3-source-20261014T041540Z/`, which reads panel OHLC, port parameters and cost terms and printed only counts and hashes); read the bound calculator's code structure, not its outputs. No export, replay, screen, MC, growth, hit, MAE, T00 step-3 or trial-9 output was read; the T00 step-3 verdict label is the only result known (public).
- **Q-SFCLEAR-2's freeze record** exists with G1, G3, window-maximum and drift values. **This coordinator has not read them** (only the record's hash and its `PRIVATE_EVIDENCE` row). The 2026-10-12 coordinator session that ran the calculator is **presumed to have seen them** unless its session record shows otherwise. Joshua's exposure is attested at §12 step 5. This study does not use that record (§S row 6).
- **Outcome label bearing on (s1):** the public T00 step-3 label `NO-GO-evidence-UNDETERMINED-dependent` arose from the same bracket convention on the same panels, where R1 and R2 disagreed. Choosing R1 alone removes UNDETERMINED by construction, so (s1) is a design choice made after an outcome label on that dimension. Joshua's step 5 re-confirmation names (s1).
- **Outcome facts bearing on (s3):** (s3) was delegated to and chosen by this coordinator knowing the public 2026-10-10 T00 build-card facts that the 5-minute evidence's needed-split yield is about 52% and that all 190 unlocated needed splits fail under the evidence-located convention. Joshua's step 5 re-confirmation names (s3).

## §S — What this successor changes

| # | Finding | Change |
|---|---|---|
| 1 | Q-SFCLEAR-2 §7 PR applies TB-S3 §5 semantics, "flatten at flatten start with market fill". On every PERMITTED row flatten start is 15:55 ET (Q-SFCLEAR-2 §3), strictly inside the 15:45–16:00 M15 bar; the bound panels are M15 only. Finer same-feed evidence exists only in part: the private 5-minute evidence used by T00 locates about 52% of needed intrabar splits, and there are no 1-minute exports (T00 build card, 2026-10-10 entries). Card B (#833, row B5) refuses a session without finer chronology at each schedule instant, so the frozen run cannot start on any day | **§7-A (new):** the 15:55 flatten-start instant is placed by the **ratified path-position bracket convention** ([schedule-execution evidence, addendum 2026-09-23](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23); `ops/c1_rail/qualification/bracket.py`), **run R1 only**, for each leg exposed at that instant (signed position ≠ 0, a broker-pending order, or a capacity reservation): a position is placed at its adverse path vertex (low for a long, high for a short); a pending-only leg at the close vertex (the fill chronology). The flatten fills at the placed `prefix.close` under the existing reference cost model. An unexposed leg needs no split and consumes no 15:55 price. A capacity reservation without a broker-pending order aborts the replay (`_capture_exposure` / `_require_exposure`: `ReplayNeedsContext`, so FG not PASS and VOID); no further ledger/broker position reconciliation is asserted. Cutoff 15:45 and own-flat 16:00 are bar boundaries and keep Q-SFCLEAR-2's rules unchanged. **Evidence-located rows are excluded:** the [evidence-located placement](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-10-08--evidence-located-placement-ratified-2026-10-09) (ratified 2026-10-09) is not used, so every exposed 15:55 instant takes the R1 vertex, including where 5-minute bars would tile it. Reason: coverage is partial (about 52% on T00), Joshua held R1/R2 with no convention change on 2026-10-10 after that measurement, the FLOOR-HALF successor was judged on the pessimistic assignment, and one rule for every day needs no private 5-minute input or provenance binding in the replay |
| 1b | Q-SFCLEAR-2 has no rule for a PERMITTED day whose bound panels lack a bar inside the session; card B needs every bar for all four legs and refuses the run. A panel-completeness count (timestamps only, 2026-10-14) over the four legs' admitted panels (the T00 source pack's: 6J with attested prefix, MYM, MGC, MNQ) found one such day, 2026-02-25 (MGC, 13:15–14:30 ET), which T00 also excluded (`missing_active_bar`), and a leading absence on 2022-09-01 before the panels begin | **§4-A (new).** *Expected grid:* for each PERMITTED account date d, the M15 bar opens at every 15 minutes from max(18:00 ET on d − 1, the panels' common first bar) through 15:45 ET on d inclusive (opens before own-flat 16:00), on the :00/:15/:30/:45 grid. (i) If any leg's admitted panel lacks any expected open, d is a **data-exclusion zero day**: every leg's bars of that session are withheld from every adapter (no bar is fed; adapters are not reset; exactly as for a DENIED row), no entry or add, zero P&L, and it stays a weekday of the §4 item 3 calendar; it is listed in the source bundle with leg and reason `missing_active_bar`. No position can carry into it because every leg is flat by 16:00 (G0). (ii) A session whose window begins before the panels' common first bar starts at that bar. The rule reads panel timestamps only and is fixed before any output; the source-bundle builder that applies it is reviewed and hash-bound like the run drivers. Bound-schedule DENIED rows are unchanged (Q-SFCLEAR-2 §4 item 3) |
| 2 | The ratified convention is a two-run bracket whose verdict counts a path only where R1 and R2 agree (UNDETERMINED otherwise); Joshua chose the bracket over adverse-only for T00 (2026-09-23) | This study uses **R1 alone**. Its direction on the verdict is **not established**: (i) R1's adverse vertex is an adverse placement on the accepted path, **not a proven worst case** (the path can reach a favourable fill first); (ii) for a pending-only leg the convention labels neither run adverse; (iii) legs are placed independently; (iv) a different 15:55 fill changes Vanguard's paper-equity path `E_p` and its later equity-dependent sizes, so its effect on the drift multiple m\* = max(1, max `E_p` ÷ paper capital), on G1-D/G3-D and on the drawdown cells can go either way. The effect's size is unmeasured. Joshua ruled (s1) (§12); no R2 run enters the verdict |
| 3 | Label | A RESOLVED verdict reads "clears on exposed history (model-fitted; 15:55 flatten at the R1 adverse intrabar placement)". No out-of-sample claim. A NOT CLEARED means not cleared under this placement, not proof that the book fails |
| 4 | Fidelity gate | Two new FG items (Q-SFCLEAR-2 §7 FG list; item 4 was dropped under ruling (j)). **Item 5:** on the full R1 PR replay, every exposed leg's 15:55 instant is split at the R1 placement and no unexposed leg is split; expected splits are re-derived from the exposure log and the M15 bars independently of `placement()`. PASS = 100% conformity, zero missing, zero extra; the split count stays private. **Item 6:** the §4-A day set re-derived independently from the panels and the expected grid equals the source bundle's `data_exclusions`, and the route output has zero fills and zero P&L on each such day, which remains a calendar weekday; and, through card B's session-boundary signal (amendment (c)), no leg's adapter receives a bar of that session, the adapter factory is called exactly once per run, and every observer call carries the same adapter instance for each leg (no feed, no re-creation). An in-place reset of an existing adapter object is not observable by this check; it is excluded by card B amendment (c)'s code review and a mutant that resets in place (recorded open item, §11). Items 1–3 are unchanged |
| 5 | Forbidden moves (adds to Q-SFCLEAR-2 §5) | See §5 |
| 6 | Freeze record | **Computed under this file** after §12 step 3 ((d)-1 ordering), by the bound calculator unchanged (sha256 `2333844dd2a9342239812baa38a119b55f4b8a65841165740a9a39633f2297bf`, Q-SFCLEAR-2 §3), on the **effective schedule**: the bound schedule with each §4-A day's permission set to DENIED (reason `DATA_EXCLUSION`), written deterministically by the source-bundle builder and bound by sha256 in the freeze record (schema `sfclear3_freeze/v1`: `nonce`, `calculator_sha256`, `calculator_output_sha256` (the calculator's output file, retained in the freeze folder), `effective_schedule_sha256`, `base_schedule_sha256`, `roll_list_sha256`, `source_build_sha256sums_sha256`, `fee_snapshot_sha256`, `margin_snapshot_sha256`, and the calculator's G1/G3/drift cells; §10 hook 4b checks it in the operator checkout); the calculator's held-bar set reads PERMITTED rows only, so §4-A days drop out of G1/G3. The record also holds the fee and margin snapshot hashes (re-taken if older than 30 days) and the roll-date list's sha256, carries a nonce, and is pinned in F₃ (Q-SFCLEAR-2 §12 steps 4–5). Q-SFCLEAR-2's freeze record is not used |
| 7 | Trial accounting (Q-SFCLEAR-2 §8) | **K stays 12.** The tuple is unchanged (`62d7ae19…671f`), so trial 10 carries, on the ground Q-SFCLEAR-2 §6 states ("the trial ledger is unchanged if the successor keeps the tuple"). The manifest lists F₂ under trial 10 `superseded_before_run_freezes` and receives F₃ as `successor_freeze_commit` |
| 8 | Run records and closure | Run records stay at `lab/analysis/c1/sfclear_2026-10/run_records/` and must descend from F₃ (§10 hook 4). The closure is `docs/briefs/closures/Q-SFCLEAR-3-*`. Q-SFCLEAR-2 gets no run record and no verdict |
| 9 | Code consequences (not scoring items) | Card B amendment (c): the R1 placement via `bracket.py` (with its one trust-domain inventory entry), empty `splits`, the §4-A zero day and post-seam contracts; FG executor card #808 (FROZEN) gains items 5 and 6 and binds F₃ by a dated amendment carrying Joshua's words, with its authority block extended; cards D and E bind F₃. Each lands as its own reviewed change before FG |

Everything not listed — book identity and R1 (§2), the binding gates and calculator (§3), the hypothesis, the 18 drawdown, 3 growth, G1, G3, G1-D, G3-D and B2 cells, seeds, windows, fees, margin, G0 and G4 (§4), routes PR for all legs (§7, item 4 ruling), deployment preconditions (§9) and the privacy rule — is Q-SFCLEAR-2's, unchanged.

## §0 — Reads

Q-SFCLEAR-2 §0, plus public reads at `origin/main` `3703f0a`: `ops/c1_rail/qualification/personal_replay.py` at PR #833 heads `9a899a3` and `66bf3a2` (not on main) (`verify_inputs`, `_verify_retained`, the 15:55 refusal, `parse_roll_dates`); `ops/c1_rail/qualification/bracket.py` and `replay.py` (`accepted_path`, `_split`, `_capture_exposure`); `production_source.py:390-434` (`vertex_split`, `placement`, `_require_exposure`); the [convention addendum](../phase3-preparation/2026-09-15/schedule-execution-evidence.md#addendum-2026-09-23--path-position-bracket-convention-ratified-2026-09-23); `core/data/bar_data/` (M15 panels only); the roll-date list's `seams`. Private reads: §D.

## §1 — Context and rulings

Q-SFCLEAR-2 §1 unchanged (O2, D2–D10, rulings (a)–(d), the E0-bound ruling), plus the authority line above and the 2026-09-23 ratification of the path-position bracket convention (its R1 run is used alone here, §S row 2).

## §4 — Hypothesis and clearance tests

**H-SFCLEAR-3:** if the Tradeify book at R1 under P0 is fit for the personal account at `E_0`, then on the exposed history, with the 15:55 flatten placed by §S row 1 and data-exclusion zero days by §S row 1b, it meets every binding cell of Q-SFCLEAR-2 §4 (18 drawdown cells, 3 growth cells, G1, G3, G1-D, G3-D, B2, item 7, no Striker total-DD trip), with G1 and G3 from this study's freeze record (§S row 6). **Reject (NOT CLEARED) if** any binding cell fails. The statistic, cells, seeds and windows are Q-SFCLEAR-2 §4's, unchanged; the label is §S row 3.

## §5 — Forbidden moves

Q-SFCLEAR-2 §5 unchanged, plus:

- Running, reporting or consulting an R2 placement, or any other 15:55 placement, as a verdict input.
- Changing the 15:55 placement, or splitting an unexposed leg, after any output exists.
- Interpolating a 15:55 price, previous-close pricing or next-bar flatten.
- Using an evidence-located (5-minute or other finer) row for any 15:55 instant.
- Excluding, filling or interpolating any day or bar beyond the bound schedule's DENIED rows and §4-A's data-exclusion days; changing the expected grid after any output exists.
- Using Q-SFCLEAR-2's freeze record, or computing this study's freeze record before §12 step 3.
- Producing an R2 sensitivity report ((s2) ruled no).

## §6 — Verdict table

Q-SFCLEAR-2 §6 unchanged, in its order: FREEZE INVALID (judged by §10 hooks 4 and 4b below: FREEZE INVALID unless both print nothing; "the freeze record" means this study's, pinned in F₃), then VOID, then RESOLVED or NOT CLEARED. **VOID also when:** FG item 5 or 6 is not PASS; or the run admits an entry, add or fill on a §4-A day, gives such a day non-zero P&L, or drops it from the calendar (a route defect, like a G0 or G4 breach). Gate mapping for the coordinator: RESOLVED → RESOLVED; NOT CLEARED → FALSIFIED for R1 under this placement; FREEZE INVALID or VOID → AMBIGUOUS (no standing).

## §10 — Audit hooks

Hooks 1–3, 5 and 6 are Q-SFCLEAR-2 §10's, unchanged (hook 5 expects `12 [10, 11, 12]`). Hook 4 is replaced and hook 4b is added; **FREEZE INVALID holds unless both print nothing** (§6, §12 step 5). Hook 4 checks these invariants, all read from committed revisions, never the working tree:

- **I1 (freeze commit).** F₃ is the first commit to set FROZEN; its Status line carries the full tuple digest, "ratify Q-SFCLEAR-3 at <40-hex R>" and the exposure attestation naming 2026-10-11T23:39:57Z; R precedes F₃ and the text at F₃'s parent equals R; F₃ changes exactly two paths: this file (one line, its single Status line) and `PRIVATE_EVIDENCE.sha256` (exactly two added lines and none removed: `FREEZE_RECORD.json` and the same folder's `SHA256SUMS`).
- **I2 (lineage).** F₃ descends from F₂; the roll-date list at F₃ hashes to the F₂ binding.
- **I3 (metadata).** At the audited commit (default `HEAD`), the parent brief records F₃ and the lineage manifest's trial 10 has `successor_freeze_commit` = F₃ with F₂ in `superseded_before_run_freezes`.
- **I4 (each run record).** With A the commit that added it: the record bytes at A equal those at the audited commit; F₃ ≤ `run_head` ≤ A by ancestry; the frozen files at `run_head` equal F₃'s; A's own diff adds the record's `PRIVATE_EVIDENCE.sha256` row.
- **I5 (each closure commit).** It descends from F₃ with the frozen files equal to F₃'s, and some run record's add-commit A is its ancestor.

```bash
# 4. Freeze chronology for Q-SFCLEAR-3 (prints nothing when sound). Usage: hook4 [AUDITED_COMMIT]
X=${1:-HEAD}
P=docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md
E=docs/evidence/PRIVATE_EVIDENCE.sha256
S=lab/analysis/c1/sfclear_2026-10
F2=83867f0d362931c2a516a62b990bb1c209372527
FROZEN=("$P" docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md "$S/schedule" "$S/build_historical_schedule.py")
F=$(git show "$X:docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md" | sed -n 's/^Q-SFCLEAR-3 pre-registration commit hash: `\([0-9a-f]\{40\}\)`.*/\1/p')
if [ -z "$F" ]; then echo 'NOT FROZEN: no Q-SFCLEAR-3 freeze commit recorded at the audited commit'; else
  git merge-base --is-ancestor "$F" "$X" || echo 'F IS NOT IN THE AUDITED HISTORY'
  # I1
  L=$(git show "$F:$P" | grep '^\*\*Status:\*\* `FROZEN')
  [ "$(git log --format=%H -G'^\*\*Status:\*\*.*FROZEN' "$X" -- "$P" | tail -1)" = "$F" ] || echo 'F IS NOT THE FIRST COMMIT TO SET FROZEN'
  echo "$L" | grep -q 62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f || echo 'NO FULL TUPLE RE-HASH ON THE STATUS LINE'
  echo "$L" | grep -qi 'exposure attestation' || echo 'NO EXPOSURE ATTESTATION ON THE STATUS LINE'
  echo "$L" | grep -q '2026-10-11T23:39:57Z' || echo 'ATTESTATION DOES NOT NAME THE DISCLOSED T00 EXPOSURE'
  for k in '(s1)' '(s2)' '(s3)' 'G1/G3' '2026-10-12 coordinator'; do echo "$L" | grep -qF "$k" || echo "ATTESTATION LACKS REQUIRED CLAUSE $k"; done
  git diff --quiet "$F" "$X" -- "${FROZEN[@]}" || echo 'FROZEN FILES CHANGED AFTER F AT THE AUDITED COMMIT'
  R=$(echo "$L" | sed -n 's/.*ratify Q-SFCLEAR-3 at \([0-9a-f]\{40\}\).*/\1/p')
  if [ -z "$R" ]; then echo 'NO RATIFIED DRAFT COMMIT ON THE STATUS LINE'; else
    git merge-base --is-ancestor "$R" "$F^" || echo 'RATIFIED COMMIT IS NOT BEFORE F'
    git diff --quiet "$R" "$F^" -- "$P" || echo 'TEXT CHANGED AFTER RATIFICATION'
  fi
  [ "$(git diff --name-only "$F^" "$F" | sort | tr '\n' ' ')" = "$(printf '%s\n' "$E" "$P" | sort | tr '\n' ' ')" ] || echo 'F CHANGES PATHS OTHER THAN THE PRE-REGISTRATION AND THE EVIDENCE LEDGER'
  [ "$(git show "$F:$P" | grep -c '^\*\*Status:\*\*')" = 1 ] && [ "$(git diff --numstat "$F^" "$F" -- "$P" | cut -f1-2)" = "$(printf '1\t1')" ] && [ "$(git diff -U0 "$F^" "$F" -- "$P" | grep -c '^-\*\*Status:\*\*')" = 1 ] || echo 'F CHANGES MORE THAN THE STATUS LINE'
  ADD=$(git diff "$F^" "$F" -- "$E" | tr -d '\r' | grep '^+[^+]')
  FR=$(echo "$ADD" | grep -oxE '\+[0-9a-f]{64}  t00-step3-console/sfclear3-freeze-[0-9]{8}T[0-9]{6}Z/FREEZE_RECORD\.json' | sed 's/^+[0-9a-f]*  //')
  { [ "$(git diff --numstat "$F^" "$F" -- "$E" | cut -f1-2)" = "$(printf '2\t0')" ] && [ -n "$FR" ] && echo "$ADD" | grep -qxE "\+[0-9a-f]{64}  ${FR%/FREEZE_RECORD.json}/SHA256SUMS"; } || echo 'F DOES NOT ADD EXACTLY THE FREEZE RECORD PAIR'
  # I2
  git merge-base --is-ancestor "$F2" "$F" || echo 'F DOES NOT DESCEND FROM F2'
  RL=$(git show "$F2:docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md" | grep '^\*\*G4 roll-date list:\*\*'); RH=$(echo "$RL" | grep -oE '[0-9a-f]{64}' | head -1); RP=$(echo "$RL" | grep -oE 'lab/analysis/c1/sfclear_2026-10/schedule/roll_dates[^` ]+' | head -1)
  { [ -n "$RH" ] && [ -n "$RP" ] && [ "$(git show "$F:$RP" | sha256sum | cut -c1-64)" = "$RH" ]; } || echo 'ROLL-DATE LIST AT F DIFFERS FROM THE F2 BINDING'
  # I3
  [ "$(git show "$X:discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json" 2>/dev/null | python -I -c "import json,sys; d=json.load(sys.stdin); p=json.loads(d['params']); t=[x for x in p['further_trial_log'] if x['trial']==10][0]; sup=t.get('superseded_before_run_freezes'); ok=t.get('successor_freeze_commit')=='$F' and isinstance(sup, list) and '$F2' in sup; print('OK' if ok else '')" 2>/dev/null | tr -d '\r')" = OK ] || echo 'TRIAL 10 MANIFEST DOES NOT RECORD F3 WITH F2 SUPERSEDED'
  # I4
  RECS=$(git ls-tree -r --name-only "$X" -- "$S/run_records/")
  for f in $RECS; do
    A=$(git log --diff-filter=A --format=%H "$X" -- "$f" | tail -1)
    [ "$(git show "$A:$f" | sha256sum)" = "$(git show "$X:$f" | sha256sum)" ] || echo "RECORD CHANGED AFTER ITS ADD COMMIT $f"
    read -r h s < <(git show "$A:$f" | python -I -c "import json,sys; d=json.load(sys.stdin); print(d['run_head'], d['private_sha256sums_sha256'])" | tr -d '\r')
    git merge-base --is-ancestor "$F" "$h" || echo "PRE-FREEZE RUN HEAD $f"
    git merge-base --is-ancestor "$h" "$A" || echo "RUN HEAD DOES NOT PRECEDE ITS RECORD COMMIT $f"
    git diff --quiet "$F" "$h" -- "${FROZEN[@]}" || echo "FROZEN FILES CHANGED BEFORE RUN $f"
    git show "$A" -- "$E" | grep -q "^+$s " || echo "PRIVATE_EVIDENCE ROW NOT ADDED IN THE RECORD COMMIT $f"
  done
  # I5
  for c in $(git log --format=%H "$X" -- 'docs/briefs/closures/Q-SFCLEAR-3-*'); do
    git merge-base --is-ancestor "$F" "$c" || echo "PRE-FREEZE CLOSURE $c"
    git diff --quiet "$F" "$c" -- "${FROZEN[@]}" || echo "FROZEN FILES CHANGED BEFORE CLOSURE $c"
    ok=; for f in $RECS; do A=$(git log --diff-filter=A --format=%H "$X" -- "$f" | tail -1); git merge-base --is-ancestor "$A" "$c" && ok=1; done
    [ -n "$ok" ] || echo "CLOSURE WITHOUT A PRIOR RUN RECORD $c"
  done
fi
```

**Hook 4b (private, operator checkout; prints nothing when sound; prints key names and hashes only, never a cell value).** For the freeze record pinned in F₃: its bytes and its folder's `SHA256SUMS` match the two pinned rows and the folder verifies with `sha256sum -c`; it parses as `sfclear3_freeze/v1` with exactly the keys named in §S row 6; `calculator_sha256` = `2333844dd2a9342239812baa38a119b55f4b8a65841165740a9a39633f2297bf`, `base_schedule_sha256` = `ab44fada0c059c0d286798239a87c82331d8500ef075bf4cb1180ed552d5d473`, `roll_list_sha256` = `72677d254045fd35ca3da7047c8b649f47d0ae283d3fc41a402467de8de4134c`; the source-build folder named by `source_build_sha256sums_sha256` verifies and its builder in `--check-only` mode reproduces `effective_schedule_sha256`; the calculator output retained in the freeze folder matches `calculator_output_sha256` and its G1/G3/drift cells equal the record's; and the bound calculator, re-run on the recorded inputs into a fresh scratch root, reproduces those cells exactly (its output carries a fresh nonce, so cells are compared, in process and unprinted, not file digests); and the fee and margin snapshot files resolve, hash to `fee_snapshot_sha256` and `margin_snapshot_sha256`, and were captured no more than 30 days before F₃'s commit date.

## §11 — Open facts (carried)

Q-SFCLEAR-2 §11 items 6, 7, 8 (G1-D/G3-D after the run), 9, 12 and 14 carry unchanged; item 11 is discharged for the study by #817 and #823 (personal forward calendar and its ratification rows); items 1, 2, 3, 4, 10 and 13 are being discharged by the run-path cards (A, C merged; B in review). Run-record and closure auditing in hook 4 is exercised against synthetic records by card E before the run. New: card B amendment (c), #808 items 5–6, and the source-bundle builder's review and hash binding (§S rows 1b, 6, 9). **Open item (recorded, not folded; Codex at `bb25889`):** FG item 6 cannot observe an in-place reset of an existing adapter object; it is excluded by card B amendment (c)'s code (no reset path) and a mutant that resets in place, reviewed before FG.

## §12 — Freeze procedure

Status stays **DRAFT — NOT RATIFIED** until Joshua acts:

1. Joshua confirms, in Joshua's own words, the §S changes, and rules:
   - **(s1)** the 15:55 instant uses the convention's R1 run alone, with the §S row 2 disclosures; or the full two-run bracket, where any path whose verdict depends on the run is UNDETERMINED (which would need its own verdict rule, added to this file);
   - **(s2)** whether a private, non-binding R2 sensitivity report is produced after the binding run; default **no**.
   - **Ruled 2026-10-13 (Joshua, directly to the Deployment Coordinator, verbatim: "R1 alone, no R2 report"):** (s1) R1 alone; (s2) no R2 sensitivity report. §S rows 2 and 5 apply as drafted; any R2 run is a forbidden move.
   - **(s3) Evidence-located rows:** excluded (§S row 1). Joshua, 2026-10-13 (ET), directly to the Deployment Coordinator, verbatim: "go with your best recommendation on 2", delegating the choice between (i) R1 at every exposed 15:55 instant with evidence-located rows excluded and (ii) evidence-located where 5-minute bars tile, R1 elsewhere; the coordinator recommended and applied (i).
2. **Required, recorded:** Joshua re-hashes `R1_TUPLE.json` personally (Q-SFCLEAR-2 §10 hook 1) and states the full 64-hex digest verbatim.
3. Joshua states "ratify Q-SFCLEAR-3 at <40-hex commit>", naming the committed draft Joshua reviewed.
4. **Freeze record, private, after step 3:** `t00-step3-console/sfclear3-freeze-<UTC>/FREEZE_RECORD.json` with its folder `SHA256SUMS` and a nonce: the bound calculator on the effective schedule (§S row 6), the effective schedule's sha256, the fee and margin snapshot hashes (re-taken if older than 30 days), and the roll-date list's sha256 (equal to the F₂ binding). The bound schedule must still regenerate to its sha256 (hooks 2–3). No result reopens drafting or delays the freeze (Q-SFCLEAR-2 §5).
5. **Freeze commit F₃** changes only this file's Status line and adds the freeze record's two `PRIVATE_EVIDENCE.sha256` rows (`FREEZE_RECORD.json` and its folder's `SHA256SUMS`). The Status line becomes ``**Status:** `FROZEN <date>` `` followed by Joshua's step 1–3 words verbatim and an **exposure attestation** complete through F₃: Joshua's and the coordinator's statement of every T00 step-3, trial-9 replay, screen or MC output either has seen, naming the 2026-10-11T23:39:57Z opening (Q-SFCLEAR-2 §D); whether either has seen any of the Q-SFCLEAR-2 freeze record's G1, G3, window-maximum or drift values; the 2026-10-12 coordinator session that ran the calculator, as presumed exposed unless its session record shows otherwise; and Joshua's re-confirmation in Joshua's own words of (s1), (s2) and (s3) knowing the §D disclosures. The line carries the literal markers `(s1)`, `(s2)`, `(s3)`, `G1/G3` and `2026-10-12 coordinator` beside the corresponding statements (hook 4 checks them). A later metadata commit records `Q-SFCLEAR-3 pre-registration commit hash: \`<F₃>\`` in the parent brief and F₃ in the lineage manifest (trial 10 `successor_freeze_commit`, with F₂ under `superseded_before_run_freezes`). §10 hooks 4 and 4b then print nothing; the coordinator records both results before any run.
6. After the freeze no constant moves; a change is a new pre-registration.
