# P-L4: size-vector amendments to the TB-I3 cards (PROPOSAL)

**Date:** 2026-10-11 · **Base:** `origin/main` `b5571a9` (no change to either TB-I3 card or to `ops/` through `613daf6`) · **For:** the Deployment Coordinator ("Portfolio deployment coordination")

**Status:** a PROPOSAL. Neither card is edited by this note:
- The [TB-I3 interlock card](../briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md) is a DRAFT owned by its freezing coordinator. It takes amendments only at its freeze.
- The [TB-I3-HOST card](../briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md) is FROZEN (2026-10-06), and a frozen card stays frozen (AGENTS.md "Continuous improvement" item 2).

This note authorizes nothing.

**Parent:** the [scope note](2026-10-11-live-size-vector-wiring-scope.md) §2 ("Activation proof") and §5 row P-L4. This note **corrects** that row. Siblings: [P-L1](../briefs/handoffs/2026-10-11-live-size-vector-p-l1-sizing-context-card-DRAFT.md) and [P-L2](../briefs/handoffs/2026-10-11-live-size-vector-p-l2-owner-binding-card-DRAFT.md).

## 1. Finding that reshapes P-L4

The scope note put the size-vector loader in TB-I3-HOST's `book_host.py`. That was wrong:
- The HOST card's host "builds nothing it runs: the loop, the owner status reader, the notifier … are all injected" (§1). It receives an already-bound `FourLegEvaluateLoop`.
- Its §5 forbids `ops/c1_rail/book_account_owner.py`, `daemon.py`, `__main__.py`, `book_runtime.py` and `deploy/**`.
- Registration "belongs to the live route packet (R-A1/R-H)" (§5; multi-leg spec R-A1 `:144`, R-H `:157`).

So whoever constructs the owner binding is the live route packet. That packet's card is not yet written. The two TB-I3 cards therefore divide as follows:

| Card | P-L4 amendment |
|---|---|
| TB-I3 interlock (DRAFT) | **A-1 to A-4** below: the GO carries the vector hash, plus a synthetic, production-refusing equality seam at arm and boot |
| TB-I3-HOST (FROZEN) | **None.** It does not build, read or forward the owner binding, so nothing in it can carry the vector. Amending a frozen card would add a footprint its §5 forbids |
| Live route packet (unwritten) | **R-SV** (§4): the loader and the stamp read-back. It is carried into that card when it is written |

## 2. Where the expected hash lives (decision D-A, Joshua)

The interlock compares the owner's stamped `size_vector_sha256` (P-L2) with an **expected** value fixed before activation. That value can live in one of two places.

| Option | Where | What it changes | Assessment |
|---|---|---|---|
| **A (recommended)** | A new GO field, `size_vector_sha256` | The [admission ADR](../adr/2026-09-12-tradeify-book-protection-instance-admission.md) T10 field set (`:99`) is closed, so this needs an ADR addendum ratified by Joshua. TB-D2 writes the field from the decision record (T9), after n3, when the vector is long frozen | Reuses the one baked artifact that both gates already read (§2b `:104`). The reseal proof is unchanged: the GO is still the only path in the c1→c2 build-context diff |
| B | The admitted registry row's `provenance` (TB-D0, ADR §2.1) | The row format and its governance-chain test | Ties the vector to the qualification row, but adds a `core/dd_geometry.py` row field and a second parser for the comparison |

*Recommend A.* Under either option, TB-D2 (or TB-D0) must verify, before writing, that the hash equals:
- the screen authority's `parameters.expressions.size_vector_sha256` (`screen_authority.py:401-432`);
- the `sizing` of the startup policy that production E1 replays (FBR, checklist T15).

That chain check is a T15/T16 record item. It is not a code change in TB-I3.

## 3. Amendments to the TB-I3 interlock card (fold at freeze, S1 only)

All four are synthetic scope, like the rest of S1. None adds a file. The §2.7 footprint and S2 are unchanged.

- **A-1. GO schema (§2.1; requires D-A = A and its ADR addendum).**
  - Add `size_vector_sha256` to the closed field set, as 64 lowercase hex characters. The missing or extra field rules are unchanged.
  - `validate` checks shape only. It never reads a vector value.
- **A-2. Equality seam (§2.1, consumed by §2.3).**
  - `deployment_go.size_vector_reason(go, *, stamped_source) -> str | None`. It refuses unless the GO's `size_vector_sha256` equals the hash returned by `stamped_source()`.
  - `stamped_source` is the owner's latest `runtime_bindings` value, `size_vector_sha256` (P-L2 LB4).
  - **The production default refuses** with "owner size-vector stamp not wired: live route packet". This is the same construction as `activation_ack_reason`'s refusing default (§2.3, D-5). Tests inject a synthetic source. No code in this card reads an owner database.
- **A-3. Gates (§2.2, §2.3).**
  - The boot gate (§2.3) adds `size_vector_reason` to the conditions for a `dry_run=false` boot. A failure is the same implicit disarm in memory, with a CRITICAL log naming the gate. It never raises or rewrites the config.
  - `--arm` (§2.2) records the GO's `size_vector_sha256` in the `arm_evidence` event.
  - `--status` reports a `size_vector_gate:` line built from the same predicate.
  - Under D-3 = U this applies to every armed boot, legacy single-leg included. Until the live route packet wires the stamp, nothing can boot armed, which is already the card's "production blocked" state.
- **A-4. Acceptance rows (§4), all in the existing `tests/ops/test_deployment_go.py` and the extended server/arm tests.**

  | Row | Refuses or passes |
  |---|---|
  | SV1 | A GO missing `size_vector_sha256`, or with a malformed value, refuses |
  | SV2 | The default `stamped_source` refuses at boot, naming the gate |
  | SV3 | An injected stamp ≠ the GO hash: implicit disarm, CRITICAL log, config bytes unchanged |
  | SV4 | An injected stamp = the GO hash, plus every other synthetic input valid: the positive control boots armed. This replaces the card's §2.3 positive control **again**, so it is still the one sanctioned outcome change |
  | SV5 | `--arm` writes the GO hash into `arm_evidence` before the config write; `--status` shows `size_vector_gate:` from the same predicate |
  | SV6 | No test or fixture contains a real vector value (a scan over `tests/` for the private sheet's SHA256SUMS name and for `"sizing"` mappings other than synthetic ones) |

**Card text to change at freeze:**
- §2.1 (schema list and the new function);
- §2.2 and §2.3 (one bullet each);
- §4 (SV1–SV6);
- §8 "Unlocked" (the stamp seam awaits the live route packet);
- §11, a new D-12 = this note's D-A.

The authority block's `acceptance` list is unchanged, because the rows extend files it already names.

## 4. R-SV: requirement for the live route packet (not a TB-I3 amendment)

When the live route packet's card is written, it carries the following.

- **Loader.**
  - The daemon config references the sizing artifact by path and `sha256`. It never holds a copy of the values.
  - The artifact is the r3d startup policy v2's `sizing`, delivered through the private overlay root that R-J already uses (`ops/c1_signal_daemon/ports/`, gitignored). This is subject to scope note Q4.
  - The loader verifies the bytes' SHA-256 and then calls `book_policy.validate_size_vector`. It does not reimplement parsing.
  - It passes the resulting `SizeVector` as the owner binding's `size_vector` (P-L2).
  - Absence, a digest mismatch or a non-canonical encoding refuses the boot to disarmed.
- **Stamp read-back.** The production `stamped_source` for A-2 reads the owner's latest `runtime_bindings.size_vector_sha256` read-only. It replaces the refusing default.
- **Activation acknowledgment** (the D-5 activation slice): the durable acknowledgment records the stamped hash, so T17's post-restart verification ("effective runtime activation, not merely a config write") reads it back.

## 5. Corrections to the parent records (made in this PR)

- **Scope note:**
  - §4's TB-I3-HOST footprint is `book_host.py` and `tests/ops/test_book_host.py` only. The earlier row listed files that card *forbids*.
  - §4's TB-I3 interlock footprint is §2.7's list, with `policy_fingerprint.py` read only.
  - §5 row P-L4 now points here.
- **P-L2 card:** §8 and §9 no longer place the loader in TB-I3-HOST, and no longer say TB-I3-HOST edits `book_account_owner.py`.

## 6. Decisions

- **D-A (Joshua; ADR owner).** The expected hash goes in a GO field (ADR T10 addendum) or in the row provenance. *Recommend:* GO field.
- **D-B (freezing coordinator).** Fold A-1 to A-4 into S1 at the interlock card's freeze, or add them as a follow-on S3 slice after S1. *Recommend:* fold, if D-A's addendum is ratified before the freeze. Otherwise S3, so that S1 is not held.
- **D-C (Joshua; scope note Q4).** The private overlay root as the sizing artifact's delivery path. *Recommend:* yes, by reference and hash. The values never enter the public repo.

## 7. Audit hooks (runnable)

```bash
# The HOST card builds nothing it runs and forbids the owner and deploy. Expected: matches at §1 (`:107`) and §5 (`:217`, `:220`).
grep -n "builds nothing it runs\|book_account_owner.py\|deploy/\*\*" docs/briefs/handoffs/2026-10-03-tb-i3-host-heartbeat-wiring-card-DRAFT.md
# The GO's field set is closed in ADR T10. Expected: the T10 row listing exactly nine fields.
grep -n "T10 GO recorded" docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md
# Neither TB-I3 card changed since this note's base. Expected: no output.
git diff --name-only b5571a9 origin/main -- docs/briefs/handoffs/2026-10-03-tb-i3-*.md
# The refusing-default pattern this note reuses. Expected: a hit in §2.3 and D-5.
grep -n "activation_ack_reason" docs/briefs/handoffs/2026-10-03-tb-i3-synthetic-interlock-card-DRAFT.md
```
