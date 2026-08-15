---
name: verify-source
description: Use when about to quote, commit, or decide on a value/claim/premise that came from somewhere other than a fresh authoritative computation this turn — a handoff or advisor note, a pinned anchor in a checked-out file, an on-disk artefact that agrees with its own test pin, a metric borrowed from another cohort, or a result whose export window you did not set. Fires hardest under time pressure ("just need the number, quick") and when the source looks internally consistent or authoritative. Methodology/ops discipline; does not modify strategy code, allocations, dd_protection, or MC constants. Sibling: `rule-0` covers the read-production-source-first channel this skill builds on.
---

# verify-source — verify the source is the RIGHT source, not just *a* source

## Overview

Rule-0 says *read the source, not memory*. This skill is the next layer: **a correctly-read source can still be the wrong source.** A number read straight off disk satisfies Rule-0 and still propagates a falsehood if the file is on a stale branch, is the wrong export vintage, came from the wrong window, or carries a metric whose cohort you never checked. Internal consistency — an artefact agreeing with its own pin — is **not** evidence of currency or correctness.

**The discipline: before you act on a value/claim/premise, verify the STATE of the source it came from — currency, vintage, scope, cohort — not merely that you read it from a source.**

## When to use

Trigger when (a) you're about to quote/commit/decide on a value, claim, or premise, and (b) it originated somewhere other than a fresh authoritative computation this turn. Each channel below is a documented burn:

| Channel | The trap |
|---|---|
| **Branch currency** | You grep a pinned anchor in the checked-out `CLAUDE.md`/file. The branch is behind `origin/main`, where the real canonical was relocked. Reading the source ≠ reading the *current* source. |
| **Handoff / advisor** | A note says "I updated X / stamped Y / it's committed." That is the label; the bytes are the source. Web-advisor handoffs confabulate repo state. |
| **Artefact ⊕ pin agreement** | An on-disk results file and its test pin both say X → looks verified. Both can encode the *same* stale or wrong-window artefact. Agreement is consistency, not correctness. |
| **Export / window** | A DD or metric "defect" that is really an export-window artifact — check the file's first date vs the panel start before calling it real. |
| **Borrowed cohort** | A PF/WR/p99/DD quoted from another analysis without its cohort (n + filter). The value propagates; the denominator doesn't. |

## The check (cheap — do it before quoting)

- **Branch:** `git status -sb` then `git log HEAD..origin/main`. If the branch is behind and the file is anchor/risk-bearing, read `origin/main`'s copy, not the checkout.
- **Handoff claim:** open the file the claim names; confirm the bytes. Never quote the claim itself.
- **Artefact:** check its provenance (date, export window, config) before trusting it — *even when its pin agrees*.
- **Borrowed metric:** state the cohort (n + filter) alongside the number, or don't quote it.

The check is O(seconds). Time pressure is the trigger for this skill, not an exemption from it.

## Rationalizations — STOP if you think one

| Rationalization | Reality |
|---|---|
| "The checked-out `CLAUDE.md`/file is the source of record." | Only if the branch is current. On a feature branch, verify vs `origin/main` first. |
| "The file and its test pin agree, so it's right." | They can encode the same stale artefact. Consistency ≠ currency ≠ correctness. |
| "I read it off disk, not from memory — that's Rule-0 satisfied." | Rule-0 is necessary, not sufficient. You read *a* source; confirm it's the *right* one. |
| "Just need the number, it's quick." | The verify is also quick. Speed is *why* the check exists, not why it's skipped. |
| "The handoff says it's committed." | The handoff is a label. Open the bytes. |

## Red flags

- About to quote a pinned anchor/number from a checked-out file on a non-`main` branch with no currency check.
- Treating "file agrees with its pin" as proof of correctness.
- Quoting a figure from a handoff/advisor note without opening the named file.
- Quoting a borrowed PF/WR/p99/DD without its cohort or window.
- "This is obviously fine, no need to check" — surfacing under time pressure.

## Worked example (the reproduced failure)

Asked to quote the canonical MC anchor from a feature branch, three fresh agents each grepped the checked-out `CLAUDE.md`, quoted the figure, and explicitly cited Rule-0 ("I did not use memory; the grep is the sourcing step") — and none ran a branch-currency check. The source was read correctly; it was the wrong *state*. The fix is one command before quoting: `git log HEAD..origin/main`, and if behind, read main's copy.

## Relationship to other skills

- **`rule-0`** (`docs/rule_0.md`) owns one channel: read production source first, not memory or prior briefs. This skill assumes Rule-0 is done and adds the source-STATE check. Rule-0 compliance can give *false confidence* — see the worked example.
- **`handoff-verify`** — before *executing* an external handoff packet (CC/advisor/Phase-0), run that skill's Phase-0 checklist; then use this skill for any specific number/claim inside it.
- **`fable-judge`** — after work is *claimed complete* (by another session, advisor, Cursor, or subagent), that skill re-runs the claimed verifications and hunts frauds; this skill is its per-value tool.
- Hand off to **`prop-firm-challenge`** for the operational facts and **`brief-authoring`** for where the verified value lands.
