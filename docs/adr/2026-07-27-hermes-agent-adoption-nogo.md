# ADR 2026-07-27 — Hermes Agent: NO-GO as a standing surface; design salvage retained

**Status:** `Accepted` — ratified by the operator 2026-07-27 (chat directive: "ratify the NO-GO")
**Decision date:** 2026-07-27
**Authors:** Joshua (ratification) + Claude Code (Fable 5, evaluation + drafter)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Relates-to:** [`2026-07-14-cc-cursor-surface-allocation.md`](2026-07-14-cc-cursor-surface-allocation.md) — the two-surface allocation this decision declines to extend. **Not amended.**

---

## §1 — Decision

**Hermes Agent** (Nous Research's autonomous-agent product, MIT, `github.com/NousResearch/hermes-agent` — distinct from the Hermes open-weights LLM family) is **NOT adopted** as a standing agent surface for this operation. The ratified CC/Cursor allocation stands at two surfaces.

**Scope of the exclusion — deliberately narrow.** Hermes Agent is categorically excluded from:

- any **rail-adjacent** surface (the c1 execution path, its config, telemetry, or alert artifacts);
- any **credentialed** surface (a host holding `~/.keys`, CrossTrade/Tradovate tokens, the databento key, or the Fly deploy path);
- any surface with **host execution rights inside the perimeter**, or write access to a governance surface.

**Not foreclosed:** a bounded, isolated, no-credential experiment on a throwaway account with a disposable corpus copy, should a future question genuinely require agentic judgment driving a *local* model. That lane stays open on its merits. This ADR closes adoption, not enquiry.

## §2 — Grounds

Evaluation: 19 candidate applications, generated across four lenses and scored by a three-judge panel (doctrine / feasibility / value-vs-status-quo) against a 30-claim product ledger independently verified against primary sources. Every candidate placing Hermes inside the perimeter was killed or conditioned. Full record: [`docs/briefs/2026-07-27-hermes-agent-adoption-ruling.md`](../briefs/2026-07-27-hermes-agent-adoption-ruling.md) and its [closure](../briefs/closures/2026-07-27-hermes-agent-adoption-closure-resolved.md).

**Two premise corrections did most of the work, and both narrow the case for adoption.** Each is recorded here as a *finding*; neither changes the ADR that owns the fact (Rule 7):

1. **Question 0 is a dispatch-environment test, not an egress rule.** Its owner is the [allocation ADR](2026-07-14-cc-cursor-surface-allocation.md) §2 + 2026-07-16 addendum — read there, not restated here. The correction: routing gitignored-byte tasks to `local` means **CC-local**, where the bytes are present; they still reach the Anthropic API. The common reading — that CC and Cursor are *categorically barred* from Pine/vendor-CSV work — is false, and it was the sole uniqueness claim under four candidates. With it gone, the local-inference lane is a preference, not a capability gap.
2. **Sentinel Tiers 2–3 are a promotion, not a build.** Owner: [`docs/spec/2026-06-23-inqhiori-sentinel-design.md`](../spec/2026-06-23-inqhiori-sentinel-design.md) §v1 implementation scope. They are a saved probe workflow awaiting promotion to a named quarterly workflow, budget-capped and deliberately **quarterly, not weekly**. Candidates proposing a weekly LLM tier argued against the ratified design's own reasoning.

**Product-side grounds** (verified, not vendor-reported unless marked): default approver is an auxiliary **LLM**, not a human; the default `local` backend runs with **no sandbox**; container backends **skip approvals entirely** (sandbox XOR approvals, never both); **no token or dollar spend cap exists in configuration**; loop hard-stop, checkpoints, and the memory write-gate all default **OFF**; an independent security audit ([issue #7826](https://github.com/NousResearch/hermes-agent/issues/7826), 4 Critical / 9 High, "ALLOW-ALL" default posture) is open and unanswered since 2026-04-11; a maintainer edited a third party's plagiarism allegation down to "." and closed it not-planned (confirmed via GitHub's edit log). The "no telemetry" claim is vendor self-report in primary docs only, with no independent audit.

**The decisive argument is not the vendor's defects.** It is that after correction 1, no surviving candidate satisfied all three falsifier conditions simultaneously: measurable operator-hour relief, *and* undeliverable by CC-local / Cursor / the cursor-agent bridge / a plain script, *and* requiring neither protected bytes at an external endpoint nor host execution rights inside the perimeter. A tool with a clean security record would still have failed that test.

## §3 — What is retained (design salvage)

The evaluation's value is the imports, not the product:

- **Memory architecture → the recall sidecar.** Hermes's capped-curated-file + FTS5-verbatim-search + write-approval split is the pattern; [`ops/recall/`](../../ops/recall/) is the in-stack implementation. Deterministic retrieval **deletes** the extraction-LLM/embedder exposure boundary rather than localising it, which is what let the Rule-7 denylist become a mechanical reject-list sourced at runtime from its canonical owners.
- **Fail-closed cron semantics** — snapshot expected state at job creation and skip-and-alert on drift; always alert on failure; no silent retries. To be imported when limb B lands, without the dependency.

## §4 — Falsifier

This ADR is **falsified**, and adoption reopens on its merits, if a named application is demonstrated that satisfies **all three**: (a) measurable operator-hour relief; (b) not deliverable by CC-local, Cursor, the cursor-agent bridge, or a plain script; **and** (c) requires neither protected bytes reaching an external endpoint nor a third-party agent holding host execution rights inside the perimeter.

A cheaper-token argument alone does **not** fire this falsifier: agent-hours are the explicitly non-binding resource here, so cost is not a qualifying advantage.

## §5 — Consequence

The adoption question is **closed and should not be re-litigated per session.** A future proposal must either fire §4's falsifier with a named application, or be routed to the isolated-probe lane §1 leaves open. Discovering that Hermes has fixed a §2 product defect is **not** grounds to reopen — the decisive argument in §2 is independent of them.

## §6 — Audit hooks

```bash
# The two premise corrections still hold at their owners (Rule 7 - read there, not here)
rg -n "dispatch environment|structurally cannot have those bytes" docs/adr/2026-07-14-cc-cursor-surface-allocation.md
rg -n "not new code|acceptable quarterly, not weekly" docs/spec/2026-06-23-inqhiori-sentinel-design.md

# Salvage limb 1 landed and is in-stack (no third-party runtime)
test -d ops/recall && python -m pytest tests/ops/test_recall_guard.py tests/ops/test_recall_index.py -q

# Salvage limb 2 (fail-closed cron semantics) rides limb B - open until a named workflow exists
ls .claude/workflows/ 2>/dev/null || echo "LIMB B STILL OPEN (tracked on the STATE.md forward board)"

# No Hermes runtime crept into the perimeter
rg -n "hermes" --glob '!docs/**' --glob '!*.md' . || echo "OK: no hermes runtime referenced in code"
```
