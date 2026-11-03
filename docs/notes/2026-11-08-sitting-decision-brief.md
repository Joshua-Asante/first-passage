# 2026-11-08 sitting: decision brief

**Status:** prep only, for Joshua's 2026-11-08 sitting. It decides nothing, edits no owner, and every disposition is his. Read from public `main` at `18e24bc` (2026-11-03). No private surface was read; private records that decide an item are named, not read. Companion to the [research checks prep packet](2026-11-08-research-checks-prep.md), whose readings it corrects where marked.
**Groups:** **A** = can be ruled now (the evidence exists); **B** = waits for this week's S-PAIR result or for data not in the repo.
**Method:** five read-only subagents gathered evidence per cluster. The coordinator re-checked every claim that changes a recommendation (listed under *Limits*).

## Findings that change the earlier reading

1. **The ORB+Aegis pair is already inside the 10-19 finding.** `discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json:3,6` is `open` at **K = 13**. Trial 13 is ORB MNQ v7 plus Aegis A-0, counted under ruling 1b(i) of 2026-10-25: "Treat B as book lineage: #876 stands and extends to it." The checklist's 10-28 addendum (`:1022`) and the 10-31 reconciliation row 2 still say "not ruled"; the checklist says K = 12 (`:1001`).
2. **Builder R1 cannot run on the current engine as registered.** R1 pins engine `a0d33b6` (`docs/briefs/pre-registration/2026-11-01-builder-r1-mcl-orb-registration.md:9`). The current parser requires `calendar`, `k_scope` and a per-instrument `split` (`lab/builder/run.py:41,93-95`). R1 runs only on the old engine (without the causal-exit fix, `dfe8900`) or is re-registered. The private run spec was not read, so the refusal is inferred from the schema.
3. **The `state-currency` gate fails from 11-07.** Run with `STATE_CURRENCY_TODAY`: 11-07 fails on the weekly deadline 2026-11-06; 11-09 also fails on `### 2026-11-08` not DISCHARGED. Tier `always` (`scripts/gates.yml:229`).
4. **Prep packet readings that do not hold:**
   - §3: AMBIGUOUS needs two consecutive audits (`docs/adr/2026-08-24-sourcing-phase-channel-retirement.md:77`); 11-08 is the first observation.
   - §4: the 08-17 ruling defines "admitted" (`docs/adr/2026-07-15-external-mechanism-harvest-intake.md:370`). H-OD-1 and H-TSMOM-1 meet it, so the idle guard was not triggered. L357 misstates D5.
   - §1: b6's prereg cannot be re-pointed to MNQ fills ("requires a fresh Pre-Q", `docs/spec/PREREG-NAS-ECR-1-live-edge-capture.md:14`).
   - §2: the ORB manifest's verdict banks 0 "per ADR 2026-07-26 clause 2-C", while its `executed_looks` ("none") acknowledges payability/T2 reads held under separate paths. The packet's "not fired" reading for 2-C does not hold without reconciling the two (A6).

## Week by deadline

| Date | Event |
|---|---|
| Wed 11-04 | Weekly preservation trade (bucket 11-02→11-06); keep it off the NinjaTrader host |
| Thu 11-05 | S-PAIR on Sim101; top-up rule applied that night |
| Fri 11-06 | Weekly STATE roll must land, or the gate fails from 11-07 |
| Sun 11-08 | Sitting; `### 2026-11-08` must be DISCHARGED that day (ET). The cleanup spec calls it Saturday (`docs/superpowers/specs/2026-10-28-org-cleanup-programme-spec.md:22,357`) |
| Mon 11-09 | ORB evaluation build replaces the canary build; edition build starts (`docs/briefs/pre-registration/2026-11-01-orb-horizon-edition-registration-v11.md:17,21`) |
| ~11-17 | Fly rollback window ends (`docs/adr/2026-07-17-c1-rail-build-account-registration-go.md`, Stage 1 record) |

## Recommended order

A1 STATE discharge (hard-date items recorded, not carried) → A2 builder → A3 four-firm §4 → A4 draft branches and the pair → A5 PARK expiries → A6 research batch → A7 expenses → A8 programme-audit note → A9 queue review. Group B: S-PAIR top-up, mini PC timing, agent tiers, edge-source L3 and D-A.

## Group A

### A1 — STATE `### 2026-11-08` discharge

- **Decides:** what happens on Sunday to an 11-08 check that no owner has recorded.
- **Mechanism:** the gate checks only for the DISCHARGED token (`scripts/check_state_currency.py:142-151,164-209`). STATE forbids rolling an obligation away without its record (`STATE.md:11-12`).
- **Hard-date items cannot be carried.** Some checks are decided by the date itself: the four-firm §4 trigger fires on no verdict (O-13, A3), and the PARK records lapse absent renewal (A5). For these, the 11-08 record is the due verdict, expiry and remedy. Carrying the check would defer a falsifier (Rule 28).
- **Options:**
  - *Record, then discharge with carry:* green. Every hard-date verdict, expiry and remedy is recorded at its owner on 11-08. Only follow-up work moves to 2027-02-08, with its owner named; the PR lists each item.
  - *Extend:* a hand edit the owner must justify (spec `:357`), and it cannot extend the hard-date items. `ops/sentinel/scan.py:292` `SLATE_DATE = 2026-11-08` does not move with it.
  - *Leave:* every PR is red from 11-09.
- **Recommend:** record, then discharge with carry for follow-up work only, and roll sentinel's `SLATE_DATE`.
- **Question:** "On 11-08, are the hard-date verdicts and expiries (four-firm §4, PARK b1/b3/b6) recorded at their owners, with only follow-up work carried to 2027-02-08, the heading discharged and sentinel's slate date rolled?"

### A2 — Builder: channel, K authority, evaluation order

**Facts:**
- Contract: `discovery_manifests/*.json` is "the sole machine K ledger" (`docs/adr/2026-08-30-candidate-contract.md:70`); a missing confirm procedure is integrity-invalid (`:112`).
- The builder keeps its own ledger and declares no alpha, M, procedure or liveness ceiling (`lab/builder/README.md:9,25`).
- 5g kills a card before the holdout; step 10 rejects a placement only on CONFIRMED candidates (`docs/adr/2026-08-30-evaluation-order.md:75-79`).
- 5b always passes (`lab/builder/gates.py:190`); 5e gates despite its "descriptive" label (`:193-195`); 5h is unwired.
- The evaluation-order review has been owed immediately since the 10-24 cost-authority change.

**Options:**
- *Channel, and an expression of the ten-step order:* one authority (Rule 29). Needs an evaluation-order addendum mapping 5a–5h with listed exceptions, or 5g moved after the holdout. R1's re-registration carries the contract fields and a liveness ceiling (an owning record suffices, `docs/methodology/strategy_harvest.md:79-80`), plus a `register_search` manifest or an admitted second ledger. No net delay, since R1 must be re-registered anyway.
- *Separately owned order:* faster for R1. Needs a public owning spec (none on main) and a scoped Effective clause. Creates a second verdict vocabulary.
- *Not a channel:* only the channel-specific liveness question goes away. K accounting still binds: Rule 25 requires discovery output to "carry the manifest and K into validation" (`docs/operational_rules.md:128`), whatever the generator is called, and the builder already uses ledgered K at gate 5f.

Under every option the builder needs an explicit, compliant K-ledger disposition: a `register_search` manifest, or its own ledger admitted as a K authority.

**Recommend:** a channel, and an expression of the ten-step order with listed exceptions. R1 is re-registered on the current engine.

**Question:** "Is the builder a sourcing channel; are its gates an expression of the ten-step order; and is R1 re-registered on the current engine with a liveness ceiling and a named K ledger?"

### A3 — Four-firm §4 primary falsifier; ORB v7's candidacy

**Why now:**
- The only dated re-MC is FALSIFIED early-fail (`docs/adr/2026-07-22-prop-portfolio-s4-discharge-withdrawal.md:379-385`).
- ORB v7's prereg is NOT_READY and must run locally (`docs/briefs/pre-registration/2026-10-17-orb-mnq-v7-s4-prereg-DRAFT.md:3-4`).
- O-13 fires the trigger on no verdict (`docs/briefs/pre-registration/2026-10-02-four-firm-dated-remc-prereg-DRAFT.md:111,141`).
- Sim101 canaries are not dated lab re-MCs.

**What the record says the remedy is:**
- §4 demotes "this program" and supersedes the ADR (`docs/adr/2026-07-12-prop-portfolio-four-friendly-firms.md:81,85`).
- The 10-29 addendum makes the Select 100K evaluation the program's first step (`:430-431`) and keeps the demotion rule (`:438`).
- The 10-28 addendum exempts the account's objective from the **5.0% ceiling** only (`:415-418`). It does not exempt the account from the program or its demotion.

**Options:**
- *Fire and demote as written:*
  - The program, including its Select 100K first step as program work, becomes research-only.
  - Record separately what continues on independent authority, with each owner: the retained evaluation, the weekly preservation trade, and the native route's own records. "Research-only" bars an execution ADR citing this one as mandate; only the retired c1 GO does today (rail ADR `:27`).
  - The revert action's "restore R6" (`:85`) points at a closed lane, so the superseding record declines it.
  - Mirrors to amend: `AGENTS.md:6,122`, `STATE.md:146-150`, `PIPELINES.md:8,72`, the `core/firm_rules.py:647` comment, `docs/pursuits/a1-four-firms-prop-portfolio-program.md:7`.
  - Open: does the $700 ceiling (`AGENTS.md:120`) survive?
- *Fire with a narrower consequence (a requested change, not a reading):* keeping operational scaling within Tradeify (`:432`) under the program while superseding only the multi-firm claim is not the recorded remedy. It would be a new ruling by Joshua, changing the preserved falsifier consequence, and it must be disclosed as such in the superseding record.
- *Extend:* moves a falsifier (Rule 28). Unavailable.

**ORB v7's §4 candidacy:**
- Keeping it fails native-lane G0 item 2 for ORB (`docs/briefs/pre-registration/2026-10-26-tradeify-native-lane-prereg-DRAFT.md:44`) and keeps reconciliation row 6 open.
- Withdrawing it closes the v7 prereg and loses the only half-built route back into §4.
- A fresh candidate must be distinct from anything released at Tradeify; none exists.

**Recommend:** fire on 11-08 and demote as written, with R6 declined. Record which account activity continues on independent authority and who owns it. If Joshua wants scaling within Tradeify to stay program work, that is a separate, disclosed change to the consequence. Withdraw ORB v7 as the candidate; rule on the $700 ceiling.

**Question:** "Record §4 fired on 11-08 and demote the program as written (R6 declined), listing what continues on independent authority? Or do you rule a narrower consequence, disclosed as a change? Withdraw ORB MNQ v7 as the §4 candidate? Does the $700 ceiling survive?"

### A4 — Draft 11-08 branches and the pair

**Facts:**
- (a) is withdrawn, (b) is granted, (c)'s lane is closed (`docs/adr/2026-10-09-self-funded-tradovate-lane-reopen.md:164-165`).
- (d) read literally ("park") would park the pair.
- The native-lane draft says the lineage was "closed on 2026-10-19" (`:46`) and cites the pre-amendment Rule 26.

**Options:**
- *Retire the draft; (d) parks nothing:* clears reconciliation row 12; row 3 is moot. Pointer updates: routing note, STATE item 1, `AGENTS.md:123`.
- *Pair inside 10-19 as an advisory prior* (amended Rule 26, `docs/operational_rules.md:134-139`): consistent with 1b(i); clears row 2. Native-lane G0 item 3 needs amending, or the framework is ruled not to gate this account (row 4).
- *Pair outside 10-19:* reverses 1b(i) and needs an explicit reason.
- *Ledger:* closing it orphans K for the ORB O-0 horizon edition and third-leg research. "Closed" can only mean frozen at 13 with carry-forward.

**Recommend:** retire the draft; confirm 1b(i) with the finding as an advisory prior; keep the ledger open at 13. This withdraws the earlier advice to close it at 12 and rule the pair outside.

**Reconciliation rows by timing:**
- Public now: rows 2, 3 and 12.
- Joshua's ruling only: rows 6, 9, 11 and 11a.
- Private records: rows 1, 4 and 7.
- Need canary results: rows 5, 8, 10, 11 and 13.
- No first armed session is possible on 11-09 in any case (runbook `:119`).

**Question:** "Withdraw the draft 11-08 rules, with (d) parking nothing; confirm 1b(i) with the 10-19 finding read as an advisory prior; keep the T00 ledger open at K = 13?"

### A5 — PARK expiries b1, b3, b6; a4 review

All lapse on 11-08 absent renewal (`docs/adr/2026-08-09-grand-tier-quintessentials-binding.md:127-133`).

- **b1:**
  - No effect on the release, which uses `aegis_6j1` (`ops/instruments/6J.md:44`).
  - Its re-entry text (`b1:4`) will read as met once the pair is armed; the record must say that seat does not re-open b1.
  - Amend `docs/methodology/strategy_lifecycle.md:77`.
  - "Retained hot" (`b1:12`) is stale: both directories were archived 09-06.
  - Recommend: lapse.
- **b3:**
  - No effect on ORB O-0 or the v7 disclosure.
  - The ORB decay re-scope row (`STATE.md:118-119`) needs a new owner (venue-descope ADR §6).
  - Owes an MNQ ledger entry (Rule 27).
  - Residuals line is stale.
  - Recommend: lapse.
- **b6:**
  - Its prereg cannot be triggered by an MNQ fill, and its engine is not on main.
  - Recommend: lapse, and move the ECR idea to the M-C row as "fresh Pre-Q at the first native fill".
- **a4:** its review date is 11-08 (`docs/pursuits/a4-harvest-external-mechanism-intake.md:7`), which the packet missed. It follows A6's harvest and radar rulings.

**Question:** "Lapse b1 and b3 (release expressions declared distinct, decay re-scope moved); lapse b6 with ECR moved to M-C; a4 follows A6?"

### A6 — Research batch

| Check | Reading | Consequence / question |
|---|---|---|
| Boundaries 2-A / 2-C | 2-A 0/3. 2-C cross-check run: three manifests match their closures. The ORB manifest's verdict banks 0 "per … clause 2-C", while `executed_looks` acknowledges payability/T2 reads under separate paths, not enumerated as looks. Ruling 1 covered the *open* manifest and said banking happens at close; it does not authorize this zero-K close | Not decidable as "not fired". Either apply 2-C's enumeration to the payability/T2 reads and rule, with reasons, whether they were this manifest's selection looks; or record 2-C fired, which reverts to declared-K banking for all executed-K closures (ST-EH-1 to 84) by superseding ADR. The TXG1 verdict text contradicts its DEAD stop reason. *"Order the ORB enumeration check, or record 2-C fired?"* |
| Sourcing retirement limb 2 | First observation (corrected) | Record and re-read 2027-02-08. *"Wait?"* |
| Harvest intake §4 | Guard not triggered (corrected); limb 1 AMBIGUOUS via the fourth branch; limb 2 0/2 | Naming it idle is allowed; correct L233/L357. *"Name idle anyway and correct L357?"* |
| Decompound HOLD | AMBIGUOUS; no pair fill is its live fill (`docs/adr/2026-06-07-decompound-remc-hold.md:296-298`) | Retire by superseding record, also closing SFRISK-1's riding trigger; fix the dead link `:289`. *"Retire?"* |
| Blind channel | AMBIGUOUS-HOLD 2/3; the 08-29 manifest is not a candidate; analogue ruling inert | Also record the cost-law battery limb as inert. *"Accept?"* |
| Flag lane | Not fired | *"Accept?"* |
| GRAND-tier §4 | H held | Confirm. *"Confirm?"* |
| Radar | Idle since 08-24 | If retired, keep the step-4 shape pre-check. *"Retire or on demand?"* |
| MNQFLOW-1-DEPTH | HOLD; S1 is a historical MBP-10 window | Sharpen the wake to "historical MBP-10 source for S1 approved". *"Keep?"* |
| Contract: MSL | Reachable; binding inconclusive (corrected) | Folded into A2 |

### A7 — Expenses

- **GLM key:**
  - Cancelled 10-24 (`docs/pursuits/SUBSCRIPTION_LEDGER.md:26`); no repo consumer.
  - Recommend: revoke, and check the primary checkout's `.env`.
- **Azure VM:**
  - No recorded consumer remains (`docs/governance/azure-compute-vm-policy.md:10,20-32,56-59`), and it has no ledger row.
  - Recommend: delete, or keep deallocated with a ledger row.
- **Fly Stage 2:**
  - Destroying loses the `c1_rail_data` volume (event ledger, broker evidence, M1 state) and frees the app names.
  - Recommend: export the volume evidence and check external webhooks now; destroy at ~11-17.
- **Question:** "Revoke GLM; delete or ledger the VM; export and check webhooks, then Stage 2 at ~11-17?"

### A8 — Programme-audit note for off-board 11-08 checks

Owner falsifiers due at the 11-08 audit but absent from STATE's list (row IDs from `docs/superpowers/plans/2026-10-25-rule-consolidation-step-1.md`):

- **Could fire:** ADR02-59, ADR09-31 T2–T4, ADR10-37, ADR12-57.
- **Owed work:** ADR03-50 (first add-back run); ADR05-19 (shock module never run, so it escalates).
- **False premise:** ADR09-55 ("rail still warm"; it is not since 11-03).
- **Owed regardless:** GATES-42, a Rule-2 trip-log item in a note dated on or after 11-08.
- **Falsifier-reachability stats** (run 11-03): 142 ADRs, 25 anchored (23%), flat.

**Question:** "Commission one programme-audit note covering these, ready by Saturday?"

### A9 — Queue attention/order review

- **Cap:** the queue peaked at 4 items (08-20) and has held 1 since 09-14, so the cap cannot fire (`docs/adr/2026-07-16-root-doc-charter-dedup.md:54`).
- **Out-of-order serving:** two serves were found, and both were directed or independent work.
- **Finding:** pass. Next check 2027-02-08.
- **Question:** "Accept as passed?"

## Group B

### B1 — S-PAIR top-up

- **Missing:** Thursday's gap list mapped to runbook §4 IDs (private canary card).
- **Rule now:** the earlier "touches protection/recovery" test always fires. Use the runbook's split instead:
  - Defer, by name, the cases that need the firm connection: U-3, U-10, U-11, U-15, U-16, U-18 (`docs/notes/2026-10-18-native-protection-recovery-pilot-runbook.md:125,131-146`).
  - Top up if U-5, U-6, U-17, the locally runnable part of U-9, or any other Sim101-runnable case is missing.
  - Split U-9. Its fault and callback checks (suppressed acknowledgment, reconnect with complete, absent and contradictory facts) can run locally. Its proof needs reads A **and** B to return `client_tag` (`:137`), and read B is the firm's web view (`:92`), so that part defers to the firm-connection stage. Partial simulation evidence is not the full U-9 proof D-N1 requires.
- **Collision:** a top-up must precede the ORB evaluation build, which keeps the canary's type names (v11 `:17`); otherwise the 11-09 start slips.
- **Accepting gaps defers:** P1 (`:116`) and D-N1 (`:152`).
- **Later conflict:** after arming, a manual preservation trade on the strategy's account is an incident (U-1, U-12, `:129,140`).
- **Question:** "Accept gaps only for firm-connection cases (including U-9's read-B proof); top up before the evaluation build if U-5, U-6, U-17 or U-9's local checks are missing?"

### B2 — Mini PC

- **Public trace:** none. The canary ran on the laptop (runbook `:60`); P1 needs its isolation steps (`:116`).
- **Timing:** buying after S-PAIR and before 11-09 is the cleanest cut, but needs a Sim101 re-check on the new host. Whether to buy can be ruled now; when waits on host failures in S-PAIR.
- **Spend:** hardware has no spend ceiling of its own.

### B3 — Agent tiers; edge-source audit

- **Tiers:** $370/month (ledger `:24-29,43`). Waits for usage and limit data since 10-31.
- **Edge-source audit:** no public trace; the public "D-A" is an unrelated 10-11 label. The public 126 appears in the native-lane horizon and the CME-fee-dependent flex binding (P4). L3 waits; D-A is ruled from the private file.

### Owned Select 100K

Superseded by private 10-24/10-25 rulings (`docs/notes/2026-10-24-assumption-challenge-rulings-proposal.md:19,89`). Nothing public remains.

## Stale records (routed, not edited)

- `STATE.md` (curated 10-29) omits the 10-31 pair release, the forward stop rule, the ORB edition, builder R1, the canary week and Fly Stage 1.
- `AGENTS.md` still says "c1 is warm"; `:123` and the routing note still show the Q-SFCLEAR-3 pause.
- The checklist gives K = 12; the native-lane draft says "closed" and cites old Rule 26.
- Reconciliation row 7: the native build authority is private and needs a public pointer.
- `docs/pursuits/b5-q-fundpol-1.md:6` still shows expiry 11-08.
- "Gates 5a–5g" is now 5a–5h. "R1" names two things.
- Rule 26 amendment date: 10-30 (R1 registration `:19`) vs 10-31 (`docs/operational_rules.md:144`).
- The cross-agent review path for the native ORB code is not visible publicly.
- The ORB v7 prereg's "UNPROVED" post-noon exposure (`:430`) needs a private check against O-0.

## Limits

- **Coordinator-verified:**
  - K = 13 and 1b(i);
  - the R1 engine pin and the required keys;
  - the `state-currency` failures;
  - the ORB manifest's verdict (2-C) and `executed_looks` (Ruling 1) text;
  - the harvest admission definition;
  - b6's "fresh Pre-Q";
  - a4's review date.
- **Subagent-only:** the 373-commit queue history; the 2-C match for the three non-ORB manifests.
- **Not run:** `check_pursuit_records.py` (launcher virtual environment missing; Rule 22).
- **Data class:** no account data, private contents, parameters or backtest dollars appear here. Dollar figures are subscription and VM-policy values from their public owners.
