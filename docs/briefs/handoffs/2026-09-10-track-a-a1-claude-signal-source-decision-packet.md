# Claude handoff — Track A / A1: Stage 1 signal-source decision packet

**Type:** cc_handoff (single deliverable, research + drafting; no implementation)
**Date:** 2026-09-10
**Status:** dispatch after PR #332 and PR #334 are merged
**Spawn target:** Claude Code (local session; archive reads and web research; no Fly writes)
**Parent:** [Track A plan](../../superpowers/plans/2026-09-10-track-a-m1-stage1-completion.md) §3 · parent session reviews the return
**Authority:** Joshua decides. This session produces a decision **packet** — options, costs, doctrine conflicts, exact amendment text — and recommends. It does not decide, sign up, spend, connect, or implement.

## 0. Rule 0 reads (Phase 0 — report before any drafting)

Repository currency: `git fetch origin main` and record the SHA. At authoring time `origin/main` was `47972f6`, PR #332 head `811df7c`, PR #334 head `3efdeb0`. Phase 0 hard check: `git ls-tree --name-only origin/main ops/c1_rail/ | grep m1_stage1_contract.py` must hit and `grep -n "Addendum 2026-09-10" docs/adr/2026-08-08-s2b-signal-daemon-build.md` must hit; otherwise return `NEEDS_CONTEXT: #332/#334 not merged`.

Read in full and quote the named passages in the Phase 0 report:

- `docs/adr/2026-08-08-s2b-signal-daemon-build.md` — §2 table row "Live CME bar source" (the lock that must be amended; "amend only by superseding ADR"), Addendum 2026-08-24 (test-strategy emit GO), Addendum 2026-09-10 (no replacement; fixture/replay needs "an explicit amendment identifying what the test certifies and leaving live-feed readiness separate").
- `docs/adr/2026-08-07-loop-s2-signal-host-fork.md` — §2 (TV login/actuation automation "absolutely prohibited"; item-5 origin = ruled host) and §4 limb 2 (DEAD-list: canned payloads, live-armed evidence, zero-qty floors).
- `docs/spec/2026-08-07-loop-s2b-python-signal-daemon-spec.md` — step 1 ("research panels / TV exports are not the live feed") and the Boundary line.
- `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md` — §4 item 5 and the AMBIGUOUS clause ("real strategy JSON does not arrive… stay disarmed"); Addendum 2026-08-24 ("Qualifying instrument" paragraph verbatim).
- `docs/adr/2026-07-10-databento-research-stack.md` — Addendum 2026-09-10 (retirement; "Any proposal to qualify controlled replay instead of the currently specified live feed requires an explicit acceptance amendment").
- `docs/notes/rail_build/M1_STAGE1_TEST_CONTRACT.md` — sections "What M1 does and does not require" and "Retained offline components".
- The seams a source must satisfy (read the code, report the exact interface): `ops/c1_signal_daemon/feed.py` (`BarSource`, `Bar`, staleness), `ops/c1_signal_daemon/daemon.py` (`IdleBarSource`, `build_loop`, `load_config` strategy/ceremony keys), `ops/c1_signal_daemon/m1_stage1.py` (`before_poll` calls `source.activate(manifest["source"])` / `deactivate()`, `accept_bar` uses `getattr(source, "binding")`, the `60 ≤ now − bar.ts ≤ 150` window, `bar.ts == target`), `ops/c1_signal_daemon/m1_stage1_control.py` (`validate_manifest` requires `source == OFFLINE_SOURCE`; `main` returns 2 for prepare/enable), `ops/c1_rail/m1_stage1_contract.py` (`OFFLINE_SOURCE`, frozen tuple), `ops/c1_rail/m1_stage1_control.py::project_evidence` (`qualifying_live_source=False`, no acceptance-event field).
- `docs/pursuits/SUBSCRIPTION_LEDGER.md` — post-#334 confirmed run-rate and the retired Databento row (the cost baseline for scoring).
- `docs/adr/2026-08-07-w6-rail-infra-closures.md` §2 item 1 — the CrossTrade→Tradovate **2-connection cap** fact (any option that opens a Tradovate API session must address it).
- `docs/adr/2026-07-14-cc-cursor-surface-allocation.md` §2 — routing for the follow-on A1b build.

Anchor each read with `git log -1 --format=%h -- <path>` in the report.

## 0.5. Clarifications (halt on ambiguity)

Post ambiguities under `## §0.5 Response` before drafting and set `Status: NEEDS_CONTEXT` until resolved. Known ones to settle explicitly in the report rather than guess:

- Whether a **delayed** (non-real-time) but genuine market bar can satisfy item 5's "real strategy signal" limb. The sizing for `m1_stage1_test` is price-independent (fixed 1.0-pt stop; `close` only has to be finite and > 1.0), so the input's job is the **origin**, not price fidelity. State this reading and ask the operator to confirm or reject it; do not build the packet on it silently.
- Whether an operator-attended input (option D below) is a "controlled replay" in the sense the 2026-09-10 addenda forbid without amendment, or a distinct class. Draft the amendment text either way; flag the classification as the operator's call.

## 1. Context and deliverables

PR #332 landed the Stage 1 one-shot ceremony, the `m1_stage1_test` identity (MYM/`MYM1!`, one micro, entry-only, permanently dry-run-only), and a daemon that always boots `NullStrategy` + an unavailable source. PR #334 retired Databento, the only source the S2b build ADR ever named. Until a new bounded decision exists, the ceremony cannot produce the item-5 event and Track A's daemon lane is blocked.

**Deliverables (all in one PR on a `claude/*` branch, docs only):**

1. A new addendum appended to `docs/adr/2026-08-08-s2b-signal-daemon-build.md`, heading `## Addendum 2026-09-DD — Stage 1 input source: options and PROPOSED selection`, status line `**Status:** PROPOSED — operator ratification owed`. Amendment-first: this ADR owns the feed lock, so the packet is an addendum, not a new ADR file. Contents: the options table (§2), the scoring, the recommended option with its grounds, and — for every option that needs doctrine — the exact amendment text as a fenced block ready to apply.
2. For each option graded "viable", a one-page implementation sketch sufficient for the parent to freeze the A1b spec in one sitting: files touched (daemon side only), config keys, secret handling, Dockerfile/`.dockerignore` lines, tests, the `source` marker constant, expected time-to-first-event, cost.
3. The Phase 0 read-report (currency + quoted passages).

**Not asked:** implementing any source; editing tests or `ops/`; restoring Databento credentials (Track A: "Do not simply restore Databento credentials or substitute a fixture"); signing up for any service; making the decision.

## 2. Execution plan

### Step 2.1 — Option enumeration (extend, do not shrink)

Evaluate at least these classes; add any you find. For each, answer every criterion in §2.2 with a source (URL with access date, or file path) — no unsourced prices.

- **(A) Tradovate market-data API** through the existing Tradovate-backed eval: eligibility of a Tradeify eval account for API access, API fee, CME micro market-data licensing, whether a daemon session consumes a Tradovate connection slot and endangers the CrossTrade link (W6 2-connection cap), credential shape and where it would rest (daemon volume only).
- **(B) A licensed third-party CME 1m OHLCV feed** (real-time or delayed), plain-HTTP/WebSocket or Python client: enumerate vendors from public pricing pages; cost dry-run only; note licensing terms for a single personal operational use.
- **(C) TradingView alert webhook as bar transport**: a once-configured, manually created 1m "once per bar close" alert on `MYM1!` whose message body is OHLCV+time JSON, POSTed to a new authenticated daemon ingest path. Strategy logic stays in Python; no TV login/actuation automation. Address S2b step 1 (exports/panels) and S2's rationale (alert-snapshot / port-parity class) explicitly: state what this certifies and what it does not.
- **(D) Operator-attended controlled input**: at target+60…150 s the operator injects the just-closed `MYM1!` 1m bar (read from the TradingView chart) through an authenticated in-container CLI bound to the ceremony manifest; the hook fires from that bar. This is the "explicit amendment" path #334 names; it certifies hook → B1 → listener → dry-run chain on a real market bar and leaves live-feed readiness separate.
- **(E) Databento re-subscription** — record as **NOT AUTHORIZED** under Track A; include so the packet shows it was considered and why it is out.
- **(F) Unlicensed/free sources** (delayed quote scrapes, `YM=F`-style endpoints): evaluate terms of service honestly; expected disposition is exclusion, stated with the reason.

### Step 2.2 — Scoring criteria (every option, every row)

| Criterion | What "answered" means |
|---|---|
| Item-5 limbs | real strategy signal from the ruled host; not canned; expected non-zero sizing; `dry_run=true`; no silent redefinition — cite the limb text |
| Doctrine conflicts | which ADR/spec line is contradicted and the exact amendment text needed (fenced block) |
| What the event certifies / leaves open | chain certified vs live-feed readiness still owed |
| Cost | monthly + one-off, sourced; compare to the retired Databento run-rate |
| Build effort | files, tests, Dockerfile lines; time-to-first-event |
| Operational risk | connection cap, secrets at rest, public ingress, fail-closed behaviour on loss |
| Reversibility | what is undone if the option is retired later |

### Step 2.3 — Recommendation

Lead with one option and its grounds. If the recommendation needs a doctrine amendment, the amendment text is part of the recommendation, not deferred. If no option satisfies item 5 without weakening a limb, say so and recommend NO-GO for the daemon lane (Track A then parks after A5).

### Step 2.4 — Verification before return

```bash
python ~/.claude/skills/brief-authoring/scripts/check_brief.py docs/adr/2026-08-08-s2b-signal-daemon-build.md --type adr
python scripts/check_adr_graph.py
git diff --stat origin/main...HEAD      # expect: the one ADR file only
```

## 4. Falsifiable hypothesis

**H:** at least one option satisfies every item-5 limb and every S2/S2b bar **without** a doctrine amendment, at or below the retired Databento run-rate, with a build confined to `ops/c1_signal_daemon/`, `deploy/c1_signal_daemon/`, `ops/c1_rail/m1_stage1_contract.py` (marker constant only), and `tests/ops/`.
**Reject** if no such option exists — then the recommendation must be an amendment-class option (C or D) with its amendment text drafted, or NO-GO. **Ambiguous** if an option's eligibility (e.g. Tradovate API access on an eval account) cannot be established from public sources — record it as an operator question, not a guess.

## 5. Forbidden moves

- Deciding. The packet recommends; the ratification line is the operator's.
- Restoring or reading Databento credentials; treating retained fixtures or replay as qualifying evidence.
- Implementing any option, editing tests, `ops/`, `deploy/`, or `.dockerignore` — tempting because the seams are obvious; A1b is a separate frozen-spec build.
- Any signup, trial, key request, or purchase.
- Proposing TradingView login/actuation automation in any form.
- Changing the listener B1 contract or anything on the listener app/volume.
- Quoting a price or eligibility claim from memory — every figure carries its source and access date.

## 6. Gate and return taxonomy

RESOLVED for this handoff = packet complete (every option scored on every criterion, recommendation stated, amendment text drafted where needed, checkers green). FALSIFIED = an option was found to violate a limb the packet had graded viable (fix the grade, do not hide it). AMBIGUOUS = an eligibility question needs the operator.

Return exactly one of: `DONE` · `DONE_WITH_CONCERNS` (packet complete, doubts named) · `NEEDS_CONTEXT` (#332/#334 not merged; §0.5 unresolved) · `BLOCKED — context-problem | capability-problem | scope-problem | plan-itself-wrong`. Include: branch, PR URL, changed files, the recommended option in one sentence, open operator questions.

## 7. Parent-session review

Pass 1 — spec compliance: docs-only diff on one ADR; no decision asserted as made; every seed option present; no implementation. Pass 2 — quality: each quoted doctrine line verified against disk; each price sourced; amendment text applies cleanly to the named section; the "what it certifies" row is honest about live-feed readiness. Then the parent drafts the A1b brief from the ratified option.

## 10. Audit hooks

```bash
grep -n "Addendum 2026-09-.. — Stage 1 input source" docs/adr/2026-08-08-s2b-signal-daemon-build.md
grep -n "PROPOSED — operator ratification owed" docs/adr/2026-08-08-s2b-signal-daemon-build.md
python scripts/check_adr_graph.py
git diff --stat origin/main...HEAD
python scripts/validate_c1_monitoring_acceptance.py docs/notes/rail_build/M1_MONITORING_ACCEPTANCE.json   # unchanged, exit 0
```
