# 2-C enumeration check — `orb_mnq_intraday_breakout` closure

**Type:** evidence record for the 2026-11-08 sitting. **It decides nothing.** Whether the 2-C revert
trigger is recorded as fired, and any consequence, is Joshua's ruling.
**Ordered:** Joshua, 2026-11-03. **Prep owner:** [2026-11-08 research-checks prep §2](2026-11-08-research-checks-prep.md#2-mechanism-boundaries-clauses-2-a-and-2-c)
(L47 notes this cross-check "wasn't run here"). **Rule owner:** [ADR 2026-07-26](../adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md).
**Sources:** this repo at `18e24bc`, plus `first-passage-archive` (cited `archive@<sha>:path:line`;
`5d47b4dc` is the `lab/ARCHIVED.json` pin). No private surface was read (Rule 13). No figures are quoted.

**Question.** Did the 2026-08-04 closure of `discovery_manifests/orb_mnq_intraday_breakout.json`
omit a read that qualifies as examined under 2-C?

## 1. The rule, applied unchanged

- 2-C banks "**executed selection events** (reads whose results any human or artifact examined)".
  Conditions: "(i) zero results artifacts exist … (iii) the closure note enumerates every executed
  look and its examiner; (iv) the operator signs the closure"
  (`docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md:60`).
- Trigger: "any instance of a campaign closed under executed-K where a later audit finds an examined
  read not enumerated in its closure note → … revert to declared-K banking for ALL closures,
  retroactively re-banking every executed-K closure at declared K" (`…:88`).
- Forbidden move: "Using §2-C on a campaign that examined results — the clause is for
  stopped-before-looking … stretching it voids it (§4)" (`…:97`).

## 2. The closure under test

- The closure ran through 2-C. Its verdict says "Banks executed selection events (0) per ADR
  2026-07-26 clause 2-C" (`discovery_manifests/orb_mnq_intraday_breakout.json:24`), with
  `closure_mode: operator-stopped` (`:21`), `K: 0` (`:6`) and `declared_K: 1` (`:20`).
- The closure note is the manifest's `executed_looks` field. It reads "none". It cites Ruling 1 and
  says the "stage artefacts live under separate ORB analysis paths, not as multiplicity-corrected
  close through this manifest" (`:23`). It names no look and no examiner.
- The verdict wording is boilerplate. `register_search.py` writes "OPERATOR-STOPPED before declared
  reads executed" on every `--operator-stopped` close (`lab/discovery/register_search.py:847-852`).
- Closed in `archive@8a78cdea` (2026-08-04, authored under Joshua's account, `Co-authored-by: Cursor`)
  by running `register_search close --operator-stopped --executed-k 0`. The SESSIONS entry in that
  commit calls it "metadata-only". It cites Ruling 1 and the 08-03 ADR's "spends no K". It records
  no operator sign-off quote (`archive@8a78cdea:docs/SESSIONS.md`, entry "2026-08-04m").
- Ruling 1 is about an **open** manifest. It reads "a manifest banks K when it **closes**, not while
  it is open" (`docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md:234-238`). It does not say
  what K a closed manifest banks. The 08-03 ADR "spends no K and opens no manifest"
  (`docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md:57`). It doesn't rule on the
  closure's K either.

## 3. Read-by-read enumeration

"In closure note?" means named in `executed_looks` (`orb_mnq_intraday_breakout.json:23`). "Examiner" is
the commit author or co-author trailer plus any recorded operator reading.

| # | Read: what was examined | Attribution (as the artifact states it) | Examiner, date | In closure note? | Qualifies under 2-C? |
|---|---|---|---|---|---|
| 1 | **Stage-2 cost law**: gross edge vs the 4× cost hurdle, plus the within-day OR-window placebo, on native MNQ 2019-05→2026-07 (`lab/analysis/orb/orb_mnq_2026-07/RESULTS.md:12-36`) | **This manifest.** "**Campaign:** `orb_mnq_intraday_breakout` (manifest …)" (`RESULTS.md:5`); hypothesis Stage-2 limb (`orb_mnq_intraday_breakout.json:9`) | Claude Code session; committed `archive@df13e74d` 2026-07-16 in the same commit that created the manifest. Operator read it at admission: "admit it", "full-pipeline evidence in hand" (`archive@5d47b4dc:lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md:3`) | **No** | **Yes.** It is a declared read whose result a human and an artifact examined; the RESULTS file is the artifact. |
| 2 | **Stage-5/6 confirm gate**: DSR at `cumulative_k=2` + temporal battery + placebo (`archive@5d47b4dc:…/RESULTS_stage6.md:9-16`) | **This manifest.** "**Campaign:** `orb_mnq_intraday_breakout`" (`…/RESULTS_stage6.md:3`); "Manifest: stays **open** (Stages 7–8 pending" (`:87`); hypothesis Stage-6 limb (`orb_mnq_intraday_breakout.json:9`) | Same commit, `archive@df13e74d`, 2026-07-16; operator at admission (`ADMISSION.md:3`) | **No** | **Yes**, as for row 1. Stage-6 is the frozen RESOLVED gate (`RESULTS.md:74-77`). |
| 3 | **Stage-7 realism**: the gate at all four friendly firms + slip stress (`archive@5d47b4dc:…/RESULTS_stage7.md:9-14`) | **This manifest** (`…/RESULTS_stage7.md:3`; "Manifest: stays **open** (Stage 8 breadth pending)", `:77`) | `archive@df13e74d`, 2026-07-16; operator at admission (`ADMISSION.md:3`, cited at `ADMISSION.md:20-22`) | **No** | **Yes.** It is an examined read of the declared candidate. Whether a realism stage is its own "selection event" or the same candidate's look is not settled by 2-C's text. Either way, it is an examined read that the note omits. |
| 4a | **Stage-8 structural breadth** vs the prop book (`archive@5d47b4dc:…/RESULTS_stage8.md:1-14`) | **This manifest** (`…/RESULTS_stage8.md:3`) | `archive@df13e74d`, 2026-07-16; operator directed it: "run stage 8 against the prop-portfolio book" (`archive@df13e74d:docs/SESSIONS.md`, entry "2026-07-16 — ORB-MNQ-1 Stage-8 breadth") | **No** | **Yes**, as for row 3. |
| 4b | **Stage-8 realized N_eff** (`archive@5d47b4dc:…/RESULTS_stage8_neff.md:8-14`) | **This manifest** (`…/RESULTS_stage8_neff.md:3`) | Claude Code session; `archive@9620138f` 2026-07-16; operator at admission (`ADMISSION.md:23-30`) | **No** | **Yes**, as for row 3. |
| 5 | **§4 T2 intraday-honest bust** at the deployed k (`archive@5d47b4dc:…/RESULTS_t2_intraday_bust.md:1-15`) | **Separate.** It tests ADR 2026-07-31 §4 T2 (`:8-12`): "no K spend, no manifest" (`:14-15`). Same construct and cached panel. | Claude Code session; `archive@8647be85` 2026-08-02. Operator ruled "T2 FIRED" on 2026-08-03 (`:46-55`) | **No.** Covered only by the generic "Payability/T2 … live under separate ORB analysis paths" (`orb_mnq_intraday_breakout.json:23`) | **Contestable.** It was examined, but it was run under the 07-31 unpark ADR's payability target, not under this manifest's declared Stage gates. 2-C gives no attribution test for later reads of the same construct. |
| 6 | **Bulenox/BluSky/MFFU payability re-score** (`archive@5d47b4dc:…/RESULTS_bulenox_blusky_payability.md:3-18`) | **Separate.** The 08-03 ADR §4 R3 precondition (`:8-13`); "no K spend, no manifest" (`:18`) | 2026-08-24 per file date (`:5`), after the 2026-08-04 close | n/a | **No.** It postdates the closure, so the note could not omit it. |
| — | Other reads under the same path, for completeness: TV-export fill realism (`…/RESULTS_tv_export_realism.md:3-7`, "zero-run, zero-K", 2026-07-21); v0.2 clock and k-grid (`…/RESULTS_v02_clock_kgrid.md:3-6`, `…/RESULTS_v02_native_clock.md:3-6`, "no new campaign, no K spend", 2026-07-31); decay-monitor seed (`…/RESULTS_decay_monitor.md:3`, attributed to this campaign, 2026-07-24); `eodadv_mnq_2026-08` (`archive@5d47b4dc:lab/analysis/orb/eodadv_mnq_2026-08/RESULTS.md:8`, "K=0 · no manifest", its own Q-EODADV-1 prereg) | Mixed. Each declares itself zero-K or another campaign, except the decay monitor. | — | No | Not needed for the finding. The decay-monitor seed is a calibration, not a gate read. |

Other records corroborate rows 1–4. The admission note recorded "K_intrinsic=1 banked to the MNQ family"
(`archive@5d47b4dc:lab/analysis/orb/orb_mnq_2026-07/ADMISSION.md:82-83`). The ORB prereg bound
K_intrinsic=1 for this campaign (`docs/briefs/pre-registration/2026-07-16-orb-nas100-mnq-reconstruction-preregistration.md:129`).
The repo's own index carries the archived stage files under this campaign's analysis path
(`lab/ARCHIVED.json:2059-2086`).

## 4. Reading

**The evidence supports FIRED, as a reading for Joshua to accept or reject.**

- Stage-2 and stages 6–8 (rows 1–4b) were examined by artifact and by the operator. Their RESULTS
  files attribute them to this manifest's campaign by name, and the closure note enumerates none of
  them. That is the 2-C trigger as written at `…boundaries.md:88`.
- Condition (i), "zero results artifacts exist", also failed at closure. On §5's reading (L97), that
  failure alone voids the 2-C close. It is a separate route to the same consequence.
- The T2 read (row 5) is not needed for the finding, and its attribution is contestable.

**Counter-readings Joshua may weigh** (none is established by a primary source found here):

1. *Ruling 1 already set this manifest's K to zero.* Its text is about open manifests only
   (`…payability-target.md:234-238`). No ruling found here applies it to the close.
2. *The note's "separate ORB analysis paths" sentence is an enumeration.* It names no read and no
   examiner (condition iii). Rows 1–4b also contradict its attribution claim, because each of those
   files names this campaign.
3. *Stages 6–8 are one candidate's looks, not extra selection events.* This changes the executed
   count (≥1), not whether an examined read went unenumerated. Row 1 alone is enough for the trigger.

**Not checked:** whether any other executed-K closure's note under-enumerates. `st_eh_supertrend_grid`
enumerates two looks with examiners (`discovery_manifests/st_eh_supertrend_grid.json:21`). The two TXG1
closures bank executed = declared = 1, so a revert does not move them.

## 5. If ruled FIRED: owner records the prescribed re-banking would change

Listed only. Nothing is re-banked here. The trigger's consequence is recorded at each owner after the
sitting, and any change to it is Joshua's separate decision.

| Owner | Current (cite) | At declared K |
|---|---|---|
| `discovery_manifests/st_eh_supertrend_grid.json` | `K: 2` (`:6`), `declared_K: 84` (`:18`); split 1 MNQ + 1 MYM (`:21`) | 84, split MNQ 42 / MYM 42 (`docs/briefs/pre-registration/2026-07-26-st-eh-1-preregistration.md:216`, `:266-267`) |
| `discovery_manifests/orb_mnq_intraday_breakout.json` | `K: 0` (`:6`), `declared_K: 1` (`:20`) | 1 (MNQ) |
| `discovery_manifests/q_txg1_striker_mnq_20260812.json` | `K: 1` (`:6`), `declared_K: 1` (`:18`) | 1, unchanged |
| `discovery_manifests/q_txg1_striker_nas100_mym_20260812.json` | `K: 1` (`:6`), `declared_K: 1` (`:18`) | 1, unchanged |
| `ops/instruments/MNQ.md` §K_BANKED | live figure `K_banked(MNQ) = 22` (`:72`); row 2 ST-EH-1 MNQ half = 1 (`:79`); ORB "Already ruled zero" (`:88`) | row 2: 1 → 42; ORB: 0 → 1; live figure re-summed at the owner |
| `ops/instruments/MYM.md` family K bank | "1 → 6 as of 2026-08-29"; ST-EH-1 counted as 1 MYM (`:128-135`) | ST-EH-1 MYM half: 1 → 42; bank re-summed at the owner |
| ORB v7 S4 prereg K disclosure | "Original discovery manifest reports `executed_k=0`" and "MNQ family bank's last-reconciled figure is 22" (`docs/briefs/pre-registration/2026-10-17-orb-mnq-v7-s4-prereg-DRAFT.md:62`, `:69`); same text in the exact-byte ratification (`docs/briefs/pre-registration/2026-10-18-orb-mnq-v7-s4-RATIFICATION.md:38`, `:45`) | both statements go stale. The ratification is frozen, so it is corrected by addendum (Rule 30). |
| ADR 2026-07-26 2-C first application | "ST-EH-1 … banking **executed K=2**", floors per family (`docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md:64`) | dated record; reader intercept by addendum |
| ADR 2026-07-31 Ruling 1 | "`K_banked(MNQ) = 2`" (`docs/adr/2026-07-31-orb-mnq-unpark-payability-target.md:236`) | dated record; already superseded as a gate by ADR 2026-08-04; intercept only if Joshua wants it |

Under ADR 2026-08-04 the family bank is disclosure-only and does not enter `K_eff`
(`ops/instruments/MNQ.md:72`). The re-banking therefore changes disclosures, not any seed's floor.

## 6. Also noted (not fixed)

Both TXG1 manifests carry the verdict "OPERATOR-STOPPED before declared reads executed"
(`discovery_manifests/q_txg1_striker_mnq_20260812.json:22`,
`discovery_manifests/q_txg1_striker_nas100_mym_20260812.json:22`). Their `stop_reason` records a
scored panel and a DEAD verdict (`…:20` in each). The text comes from the hard-coded template at
`lab/discovery/register_search.py:847-852`, which also wrote the ORB verdict.

## Verification

Commands used (read-only):

```bash
cat -n docs/adr/2026-07-26-mechanism-counterparty-constraint-boundaries.md
grep -n '"\(K\|declared_K\|closure_mode\|stop_reason\|executed_looks\|verdict\)"' discovery_manifests/{orb_mnq_intraday_breakout,st_eh_supertrend_grid,q_txg1_striker_mnq_20260812,q_txg1_striker_nas100_mym_20260812}.json
git -C <archive> show 5d47b4dc:lab/analysis/orb/orb_mnq_2026-07/RESULTS_stage6.md | head -5   # Campaign line
git -C <archive> show --stat 8a78cdea; git -C <archive> show 8a78cdea -- docs/SESSIONS.md
sed -n 840,852p lab/discovery/register_search.py
```
