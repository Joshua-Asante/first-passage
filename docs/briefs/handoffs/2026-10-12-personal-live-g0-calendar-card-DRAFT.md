# Personal lane live G0: forward session calendar for the personal instance (worker build card)

**Type:** cc_handoff (worker build card)

**Status:** **DRAFT, not frozen, not dispatchable.** Drafted 2026-10-12 by a drafting worker for the Deployment Coordinator. It closes nothing until Joshua rules the decisions in the [decision list](../../notes/2026-10-12-personal-live-g0-g4-decisions.md) (G0-1 to G0-5) and the coordinator freezes a revision under the committed-handoff rule.

**Base:** `origin/main` `158bf2a`. Every `file:line` is at that commit.

**Gap closed (coordinator readiness return, item C4):** no personal forward calendar exists. [Q-SFCLEAR-2 §3 G0][prereg] says "**Live:** a ratified forward calendar under the same `schedule_rule`", and §11 item 11 records that it is not built. Under the first-release policy, the live calendar also denies the evidence classes UNCERTAIN_ADJACENT and MISSING_SOURCE, which the replay schedule does not (§3 "Live/replay difference", disclosed; step 1 (g) ruled "keep").

**Parent:** the [personal-lane card](2026-10-11-personal-lane-items-2-6-7-card-DRAFT.md). Its P4 row owns the live gates: arm refusal, the entry gate and the flatten executor. This card adds the calendar input that P4 consumes. It does not widen P4.

**Executor (proposed):** a Claude worker, single writer of `claude/personal-g0-calendar`. **Not GLM**: the module decides session admission for a live rail (the parent's `no_glm_for_trust_auth_or_private_inputs`).

**Coordinator:** the Deployment Coordinator. It owns the freeze, diff review and the PR. The merge sequencer owns merges.

```yaml authority
seat: worker
parent: docs/briefs/handoffs/2026-10-11-personal-lane-items-2-6-7-card-DRAFT.md
max_risk: medium
capabilities: [repository.read, tests.run, worktree.write, branch.push]
constraints:
  - no_main_write
  - no_merge
  - packet_write_footprint_only
  - red_first
  - no_dd_protection_edit
  - no_policy_registry_row
  - no_tradeify_binding_change
  - no_worker_file_edit
  - no_private_bytes_in_git
  - no_live_order_arm_or_credentials
  - no_glm_for_trust_auth_or_private_inputs
  - stop_at_coordinator_return
  - not_dispatchable_until_section_11_gates_recorded
  - offline_synthetic_and_public_calendar_bytes_only
  - no_ratification_row_written_by_worker
  - no_edit_to_ratified_calendar_d19_overlay_or_tradeify_registry
  - no_book_session_calendar_or_author_tool_edit
  - no_book_account_owner_arm_or_listener_edit
  - no_cmegroup_automation
  - no_pr_open
acceptance:
  - tests/ops/test_personal_calendar_binding.py
  - tests/ops/test_book_session_calendar.py
  - tests/ops/test_instance_binding.py
  - tests/ops/qualification/test_trust_domain.py
  - tests/ops/qualification/test_runtime_inventory.py
```

`test_personal_calendar_binding.py` is new. The other four exist and must stay green with no edit. The last two are listed to prove that the new module does not enter the trust domain (§3).

## 0. Phase 0: Rule-0 reads and findings returned before code

Read and report before writing a test. A contradiction with this card is a **stop** (§7).

- **(a) Loader.** `ops/c1_rail/book_session_calendar.py`. The venue block is Tradeify-bound: `account_day_basis` must be `TRADEIFY_ACCOUNT_DAY` (`:398-400`), and the venue clocks must be 16:45 and 12:59 (`:405-410`). Session IDs match `tradeify-account-day:` (`:52`). `load_ratified_calendar(path, *, overlay_path, ratified_path, repo_root)` (`:583-601`) takes the ratification registry as a **parameter** and refuses a digest that the registry does not list (`calendar_not_ratified`). `load_ratifications` (`:548-580`) accepts an empty list. Confirm all of this at the cut base.
- **(b) Artifacts.** `ops/calendars/book_session_calendar_2026-10.json` (sha256 `16e322b1…1b3b`) and `…2026-11.json` (`b89562a5…0aad7`) are ratified for the Tradeify book in `ops/calendars/RATIFIED.json`, scoped to "Book permission rows … Grants no activation". Each carries `schedule_rule` (TB-S3 §5: cap 16:00, 15, 15, 5) and `first_release_policy.deny` = HOLIDAY, SHORTENED, UNCERTAIN_ADJACENT, MISSING_SOURCE. Ratification records: [Packet 1 Step 4](../../notes/2026-09-15-packet1-step4-session-calendar.md) for 2026-09, PR #560 for 2026-10 and PR #685 for 2026-11.
- **(c) Formula equality.** On a PERMITTED row the venue deadline is V = 16:45 ET, so D = min(16:00, 16:30) = 16:00. Under the personal replay schedule, V = 17:00 (product close) and D = min(16:00, 16:45) = 16:00. Confirm that cutoff 15:45, flatten start 15:55 and own-flat 16:00 ET hold on every PERMITTED row of both files. `production_source.py:230-266` (`parse_source_calendar`) is the qualification-replay parser for `qualification-source-calendar/v1` ("deployment calendar is not a substitute"). It computes the same own-flat formula, but it is **not** a live consumer, and this card does not touch it.
- **(d) Consumers today.** Report every caller of `load_ratified_calendar`/`session_for` in `ops/`. At drafting the only callers were `account_close_assembler.py`, `account_close_calculation.py` and `book_settlement.py`. No production code builds the owner's runtime `binding["session"]`: `BookAccountOwner._validate_binding` (`book_account_owner.py:455-486`) only checks it. That construction belongs to P-L4/TB-I3 S1, not to this card.
- **(e) Trust domain.** `book_session_calendar` is a trust-domain runtime dependency (`qualification/trust_domain.py:162`, **T**). It is not a TB-I1 fingerprint component (`policy_fingerprint.py:29-32`, **F** = no). The new module must be imported by no **T** module. Report the import graph.

## 0.5. Recommended defaults (each is a Joshua decision; see the decision list)

- **(A) Calendar artifact (G0-1).** **Recommended:** the personal instance consumes the Tradeify-authored `book_session_calendar/v1` files **unchanged**, admitted only through a **separate personal ratification registry**, `ops/calendars/personal/RATIFIED.json` (schema `calendar_ratification/v1`). The Tradeify venue clocks are at least as strict as the personal ones (16:45 ≤ 17:00), and Phase 0 (c) shows identical cutoff, flatten and own-flat times on every PERMITTED row. Tradeify-sourced rows (venue `source_ids`, the Tradeify permitted-times pages) are **not required** by the personal lane, but they stay inside the reused bytes, as an extra restriction. No **T** code moves. *Alternative:* a personal venue variant of the schema. That needs edits to the loader and the author tool (**T**, which moves the Tradeify trust domain) and is out of scope for this card.
- **(B) Evidence classes (G0-2).** **Recommended:** keep all four first-release denials, as §11 item 11 and the §3 disclosure state. The personal live calendar then permits a subset of the sessions the replay permitted.
- **(C) Ratification unit (G0-3).** **Recommended:** one personal registry row per calendar digest, written only on Joshua's own words naming that digest. A Tradeify ratification never admits a personal session.

## 1. Goal

A pure, offline-tested module that gives the personal instance its G0 session decision: `PersonalCalendarBinding.session_for(now)` returns a `BookSession` or a typed refusal, using only calendars that the personal registry ratifies, under the TB-S3 §5 `schedule_rule` and the four-class first-release policy.

**Not asked:**
- Wiring into the arm, the listener or the owner's runtime binding. That is G0-b, a P4 amendment (§9).
- Authoring a new month. That stays with the existing author tool and the monthly workflow (`ops/calendars/README.md`).
- Writing a ratification row (an operator act, §11).

## 2. Scope

### 2.1 The change

1. `deploy/c1_rail_personal/calendar_binding.json` (new, schema `personal_calendar_binding/v1`). It is configuration as code, an instance-level overlay. It names: `instance: personal_tradovate`; the `schedule_rule` owner (TB-S3 §5) and its four constants; the required `first_release_policy.deny` set; `ratification_registry: ops/calendars/personal/RATIFIED.json`; the closure overlay path and sha256; and an ordered list of `{calendar_file, calendar_sha256}`. It holds no credential, account or private value.
2. `ops/calendars/personal/RATIFIED.json` (new): `{"schema": "calendar_ratification/v1", "note": "...personal instance only...", "ratifications": []}`. The worker writes the list **empty**.
3. `ops/c1_rail/personal_calendar_binding.py` (new). It:
   - loads the binding;
   - for each listed calendar, checks the file bytes against the pinned sha256 **from the binding**, never from the file;
   - calls `load_ratified_calendar(..., ratified_path=<personal registry>)`;
   - refuses a calendar whose `schedule_rule` or `first_release_policy` differs from the binding;
   - requires the coverage windows to chain with no gap (each next `coverage_start_utc` ≤ the previous `coverage_end_utc`);
   - exposes `session_for(now)`, which routes to the calendar whose coverage holds `now` (on an overlap, the later-ratified file wins) and passes through every existing typed refusal.

   Refusals it adds: `binding_digest_mismatch`, `schedule_rule_mismatch`, `first_release_policy_mismatch`, `coverage_gap`. No weekday fallback.
4. `ops/calendars/README.md`: one short section naming the personal registry and stating that a Tradeify row does not admit the personal instance.

### 2.2 What does not change

`book_session_calendar.py`, `scripts/author_book_session_calendar.py`, every `ops/calendars/book_session_calendar_*.json`, `ops/calendars/RATIFIED.json`, D19, `book_closure_overlay.json`, `instance_binding.json`/`instance_binding.py` (P3, merged), the owner, the arm and the listener.

### 2.3 Files

| Allowed | Edit |
|---|---|
| `ops/c1_rail/personal_calendar_binding.py` | new |
| `deploy/c1_rail_personal/calendar_binding.json` | new |
| `ops/calendars/personal/RATIFIED.json` | new, empty list |
| `tests/ops/test_personal_calendar_binding.py` | new |
| `ops/calendars/README.md` | one section |

**Forbidden:** every other file. Named for emphasis:
- `ops/c1_rail/book_session_calendar.py`, `scripts/author_book_session_calendar.py`, `ops/calendars/RATIFIED.json`, `ops/calendars/book_session_calendar_*.json`, `ops/calendars/cme_holiday_calendar_2022_2026.json`, `ops/calendars/book_closure_overlay.json`, `ops/calendars/evidence/*`;
- `ops/c1_rail/book_account_owner.py`, `c1_rail_arm.py`, `c1_rail_listener.py`, `c1_rail_http_server.py`, `instance_binding.py`, `deploy/c1_rail_personal/instance_binding.json`, `deploy/c1_rail/Dockerfile`;
- `book_policy.py`, `book_sizing_context.py`, `policy_fingerprint.py`, every `qualification/` file and every `core/` file;
- every `lab/` file, the Q-SFCLEAR-2 pre-registration, `STATE.md`, `docs/evidence/PRIVATE_EVIDENCE.sha256`;
- any existing test or fixture.

### 2.4 Bound footprint

| Path | T (`trust_domain.py:154-178`) | F (`policy_fingerprint.py:29-32`) |
|---|---|---|
| `personal_calendar_binding.py` (new) | No, provided no T module imports it (§0(e)); the collector re-derives imports | No |
| `book_session_calendar.py` (imported, not edited) | Yes, **unchanged** | No |
| Data files (binding, registry, README) | Not code roles | No |

No **T** or **F** byte moves. The Tradeify trust domain and policy fingerprint are unchanged.

## 3. Method

1. Phase 0 (§0). Post the findings.
2. Write the §4 rows. Run them on the base and record the **red** run (the module does not exist).
3. Build §2.1. Record the **green** run, then the acceptance list.
4. Run `python -I scripts/fp.py test-ops` once and `python -I scripts/fp.py check` once. Cite each `record.json`.
5. Stage only the §2.3 files. Check the commit message against `git diff --cached`. Push and return (§6).

## 4. Acceptance checks (falsifier-first)

**Hypothesis:** the personal instance admits a session only on a personally ratified digest, under the frozen `schedule_rule` and the four-class policy. Any row below passing on a mutant falsifies the build.

| Row | Test | Fails if | Named mutant it kills |
|---|---|---|---|
| PC1 | Real 2026-10 file, Tradeify registry lists it, personal registry empty → `calendar_not_ratified` | A Tradeify ratification admits the personal instance | M-PC1: the loader is passed `ops/calendars/RATIFIED.json` |
| PC2 | Synthetic personal registry row for the 2026-10 digest (tmp path): a PERMITTED row returns a `BookSession` with cutoff 15:45, flatten 15:55, own-flat 16:00 ET | A ratified PERMITTED session is refused or carries other times | M-PC2: a fail-closed stub that refuses every session (positive control) |
| PC3 | One flipped byte in a calendar copy → `binding_digest_mismatch` before parsing | Bytes are trusted over the pin | M-PC3: expected digest read from the file being checked |
| PC4 | Synthetic calendar with `cutoff_before_own_flat_minutes: 10` → `schedule_rule_mismatch` | The binding accepts another rule | M-PC4: the rule check is skipped |
| PC5 | Synthetic calendar whose `deny` omits MISSING_SOURCE → `first_release_policy_mismatch`; real 2026-10-12 row → `session_denied:MISSING_SOURCE` | An evidence class is dropped | M-PC5: deny set compared as a subset |
| PC6 | Two synthetic calendars with a one-day coverage gap; `now` in the gap → `coverage_gap` | A weekday fallback or the last calendar is used | M-PC6: the nearest calendar is chosen |
| PC7 | 2026-10/2026-11 overlap rows (2026-10-29, 2026-10-30) give identical sessions from either file, and the later-ratified file is selected | The overlap rows diverge or the selection is ambiguous | M-PC7: the first-listed file wins |
| PC8 | Closure overlay sha differs from the binding → refused | Overlay drift is admitted | M-PC8: the overlay check is skipped |
| PC9 | AST scan: no `ops/c1_rail` module in the trust-domain list imports `personal_calendar_binding`, and the module imports no `lab` module | The module enters **T** or crosses `lab↔ops` | M-PC9: imported from `book_session_calendar` |
| PC10 | Binding JSON key set is exact; no key named like a credential or account (the `instance_binding.INSTANCE_KEYS` names) | A secret or identity slot enters the calendar binding | M-PC10: an `account` key is added |

**Revert trigger:** any listed existing suite changes outcome.

## 5. Forbidden moves

- Writing a ratification row in either registry. Rows are Joshua's acts (§11). An agent writes one only on his explicit instruction naming the digest (the #560 precedent), and never under this card.
- Editing any ratified calendar, D19, the overlay, the Tradeify registry, the loader or the author tool (§2.3).
- Any real-data run: no price, bar, trade, export, replay, screen or MC output. Public calendar and evidence bytes are allowed.
- Any private read: `C:\Users\joshu\t00-step3-console\`, Pine, ports, `effective_inputs.json`, `E_0`.
- Any frozen-constant edit (`DD_TRIGGER`/`DD_SCALE`, `CANDIDATE_SCALE`, `BASE_RISK`, the TB-S3 §5 constants).
- Automated access to cmegroup.com (its site terms forbid it).
- GLM, a push to `main`, a merge, or opening a PR.

## 6. Return (status taxonomy)

| Status | When |
|---|---|
| `DONE` | §4 rows red on the base and green on the build; acceptance suites green; `fp test-ops` and `fp check` records completed with exit 0; footprint equals §2.3 |
| `DONE_WITH_CONCERNS` | As DONE, with a named residual (for example, a caller not listed in §0(d)) |
| `NEEDS_CONTEXT` | A §0.5 default is contradicted by a Phase-0 read, or a G0 decision is unruled |
| `BLOCKED — scope-problem` | A green run needs a §2.3-forbidden file |

**Gate verdict (coordinator):** RESOLVED when the return is `DONE` and §7's two passes reproduce it. FALSIFIED when a row cannot be made red on the base, or a revert trigger fires.

## 7. Stop conditions and parent review

**Stop and return; do not work around:**
- §0(a) shows the loader cannot take a separate registry, or §0(c) finds a PERMITTED row whose times differ from 15:45, 15:55 and 16:00 ET.
- §0(e) finds a **T** module that would import the new file.
- A listed suite fails at the base.
- A green run needs a forbidden file.
- A governance collision: another in-flight card claims a §2.3 path.

**Parent review (coordinator):**
- Pass 1, spec: the diff names exactly the §2.3 files, and the registry list is empty.
- Pass 2, quality: re-run PC1–PC10 from a clean worktree; confirm that no **T** or **F** byte moved (`git diff --stat` on `trust_domain.py`'s runtime list and on `policy_fingerprint.py`'s components).

## 8. Out of scope and decision unlocked

**Out of scope:**
- G0-b wiring (§9);
- the December 2026 and later calendars (the monthly workflow; a personal row per digest);
- a personal venue schema variant (G0-1 alternative).

**Unlocks:** P4's arm and entry-gate rows can consume a typed personal session decision. Q-SFCLEAR-2 §11 item 11 can move from "not built" to "built; awaiting personal ratification".

## 9. Sequencing and file collisions

- **G0-a (this card)** touches no file in the `book_account_owner.py` queue (P-L2 #805 in review → GC-5 → S2 → P4). It can run in parallel with that queue.
- **G0-b (consumer wiring, proposed as a P4 amendment, not a separate writer):**
  - the arm refuses a personal instance unless `session_for(now)` gives a session, or a typed refusal that permits no risk;
  - the listener's entry gate refuses on any refusal;
  - the flatten executor takes its deadlines from the same `BookSession`;
  - P-L4/TB-I3 S1 builds the owner's `binding["session"]` from this module for the personal instance.

  The files involved are `c1_rail_arm.py` (P4 and TB-I3 S1), `c1_rail_listener.py` (P4), the owner (queue) and `deploy/c1_rail/Dockerfile` COPY lines (TB-I3 S1). The coordinator orders them at P4's freeze.
- `ops/calendars/README.md` is also edited by each monthly extension. If one is in flight, rebase.

## 10. Audit hooks (runnable)

```bash
c=docs/briefs/handoffs/2026-10-12-personal-live-g0-calendar-card-DRAFT.md
python -I scripts/check_brief.py "$c" --type cc_handoff
python -I scripts/fp.py python scripts/check_handoff_authority.py "$c"
# Scope at return. Expected: exactly the §2.3 files.
git diff --name-only <cut base>..HEAD
# No T/F movement. Expected: no output.
git diff <cut base>..HEAD -- ops/c1_rail/book_session_calendar.py ops/c1_rail/qualification ops/c1_rail/policy_fingerprint.py ops/calendars/RATIFIED.json 'ops/calendars/book_session_calendar_*.json'
# Personal registry empty at return. Expected: 0.
python -I -c "import json;print(len(json.load(open('ops/calendars/personal/RATIFIED.json'))['ratifications']))"
python -I scripts/fp.py python -m pytest tests/ops/test_personal_calendar_binding.py tests/ops/test_book_session_calendar.py tests/ops/test_instance_binding.py tests/ops/qualification/test_trust_domain.py tests/ops/qualification/test_runtime_inventory.py
python -I scripts/fp.py test-ops
python -I scripts/fp.py check
```

## 11. Gates and operator acts (NOT DISPATCHABLE until G-1 to G-3 hold)

- **G-1. Joshua's decisions** G0-1, G0-2 and G0-3 ([decision list](../../notes/2026-10-12-personal-live-g0-g4-decisions.md)), in his own words.
- **G-2. Coordinator freeze** under the committed-handoff rule.
- **G-3. Dispatch** by the coordinator.

**Operator acts.** Never worker builds; never delegated by this card.
1. **Ratification:** Joshua names each digest for the personal instance. Each becomes a row in `ops/calendars/personal/RATIFIED.json`, written by him or on his explicit instruction. One per month.
2. **Source capture attestation (G0-4):** each forward month's CME holiday and clearing captures come from an operator-attended read, never agent automation of cmegroup.com. That includes the Columbus and Veterans Day notices whose absence makes a row MISSING_SOURCE.
3. **Venue-deadline attestation (G0-5):** Joshua attests, from Tradovate's published terms or its written answer, that the personal account has no mandatory flat or liquidation time earlier than 16:15 ET on a regular session for 6J, MGC, MYM and MNQ. Otherwise V moves and the D = 16:00 equality in §0(c) fails.

**Worker builds:** §2.1 (G0-a) here; G0-b inside P4; each month's calendar authoring with the existing tool.

Live use additionally needs a RESOLVED Q-SFCLEAR-2 verdict, ADR 2026-10-09 items 3–4 (destination), M1, arming, live-spend and a per-session GO. This card grants none of them.

## 12. Open decisions (coordinator at freeze)

- **D-1.** Confirm or replace §0.5 (A)–(C), per Joshua's G0-1 to G0-3 rulings.
- **D-2.** Fold G0-b into P4's card, or order it as its own packet after P4.

## Pre-mortem

- **Loop cost:** one targeted run, one `fp test-ops` and one `fp check`. A third full run is a checkpoint, not another attempt.
- **Decisions the executor will hit:** the overlap tie-break (default: the later `ratified_utc` wins; both files' overlap rows must agree, PC7).
- **What would make this moot:** Joshua choosing the personal venue variant (G0-1 alternative), or the Tradeify monthly extension stopping. A stop would leave no new digest for the personal registry to list, so the variant becomes necessary by the first uncovered month.
- **Evidence binding:** acceptance evidence is the records at the returned head only. A push after the green records voids them.

[prereg]: ../pre-registration/Q-SFCLEAR-2-verdict-preregistration.md
