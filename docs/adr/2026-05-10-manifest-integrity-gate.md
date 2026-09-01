# ADR: Vendor manifest integrity gate (pre-commit + format CI)

**Date:** 2026-05-10  
**Status:** Accepted  
**Decision date:** 2026-05-10
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Issue:** [GH #62](https://github.com/Joshua-Asante/multi_firm_operations/issues/62)  
**Phase A anchor:** `2026-05-10-pr59-manifest-drift-rca.md` (evicted 2026-06-05; retrieve via `git show pre-prune-2026-06-05:archive/docs/briefs/programs/2026-05-10-pr59-manifest-drift-rca.md`)

## Context

PR [#59](https://github.com/Joshua-Asante/multi_firm_operations/pull/59) established the public-clone posture: vendor CSVs under `data/tv_exports/`, `data/bar_data/`, and `data/external/` stay gitignored; per-directory `SHA256SUMS` files are tracked. Phase A (RCA above) found manifest vs on-disk skew in a narrow time window and concluded **H2** — on-disk rewrites between commit and later verification — with NAS100USD.csv as the conclusive missing-file case.

**Phase A H2 hypothesis (verbatim from RCA §1):**

> **H2 — on-disk rewrites in window.** Manifest correct at b71e4a4 11:12 EDT; on-disk CSVs were modified between 11:12 EDT and the spawn pre-flight ~12:10 EDT (or the sync at 12:21 EDT).

Phase A aggregate verdict (RCA §3) adopts H2 as the operational explanation for the drift pattern, with NAS100USD as decisive.

There was **no** manifest-generation script in `scripts/` at Phase A; Phase B **creates** the reproducible check/regenerate tool and wires it into git + CI at the format boundary.

## Decision

1. Add [`scripts/check_data_manifests.py`](../../scripts/check_data_manifests.py) (stdlib only): `--check` (default), `--regenerate`, `--regenerate --dry-run`, walking the four directories that hold tracked `SHA256SUMS`.
2. Add a **git-native** `pre-commit` hook (tracked template at [`scripts/githooks/pre-commit`](../../scripts/githooks/pre-commit)) installed per clone via [`scripts/install_hooks.sh`](../../scripts/install_hooks.sh) or [`scripts/install_hooks.bat`](../../scripts/install_hooks.bat). The hook runs `--check` when any staged path is under `data/tv_exports/`, `data/bar_data/`, or `data/external/`. `git commit --no-verify` remains the explicit escape hatch.
3. Add [`.github/workflows/manifest-check.yml`](../../.github/workflows/manifest-check.yml): **format-only** validation of `SHA256SUMS` lines plus enforcement that no `data/tv_exports/**/*.csv` or `data/bar_data/**/*.csv` is **tracked**. Hash equality against bytes is **local-only** — CI does not have gitignored CSVs.
4. Document the standing regen-with-data workflow in [`CLAUDE.md`](../../CLAUDE.md).
5. Graduate methodology lesson **M-9** in [`docs/methodology/lessons/methodology_lessons.md`](../methodology/lessons/methodology_lessons.md).

## Trade-offs

| Approach | Outcome |
|----------|---------|
| Hash validation in GitHub Actions | **Rejected** — vendor bytes are not in the repo; runners cannot recompute ground truth. |
| Ungitignore CSVs | **Rejected** — violates PR #59 / public-prep contract (redistribution). |
| `pre-commit` framework / husky / lefthook | **Rejected this round** — single-developer overhead; separate ADR if the project outgrows shell hooks. |
| Runtime verification in `portfolio_mc.py` / TV loaders | **Rejected** — too late, repeats work every run; integrity belongs at commit boundary. |
| Backfill “historical correct” manifest at `b71e4a4` | **Rejected** — bytes unrecoverable; reconstruction error risk. |

**Windows note:** `core.autocrlf=true` (confirmed on the authoring machine) means the checker must hash **working-tree** bytes read via `open(..., "rb")`, not git blobs — consistent with GNU `sha256sum` on the same checkout.

## Consequences

- Any normal commit that stages vendor-tree paths must pass `check_data_manifests.py --check` or the commit aborts.
- After deliberate re-exports, the operator runs `--regenerate` (dry-run first) and commits manifest updates **with** the data change.
- CI catches malformed manifest lines and accidental `git add -f` of vendor CSVs; it does **not** replace the hook.

## GH #62 closing comment (template)

Paste when merging / closing the issue:

---

**Verdict:** Phase A **H2** — manifest correct at b71e4a4 11:12 EDT; on-disk CSVs modified between 11:12 EDT and the spawn pre-flight ~12:10 EDT (RCA §1). Phase B closes the loop with a load-bearing **git pre-commit** gate + **format-only** CI.

**ADR:** [`docs/adr/2026-05-10-manifest-integrity-gate.md`](docs/adr/2026-05-10-manifest-integrity-gate.md)

**Lesson:** **M-9** — Gitignored vendor-data manifests need a local pre-commit hash gate. CI cannot replace it when the bytes aren't in the repo. Manual regen drifts silently. [`docs/methodology/lessons/methodology_lessons.md`](../methodology/lessons/methodology_lessons.md)

**NAS100USD.csv:** Tracking-only case already resolved by **93865f8** (manifest entry dropped). No further code action; if `fetch_oanda_bars.py` is run later, `--regenerate` picks up the new file.

---

## §7 Audit hooks

Verified 2026-05-10 at `3965cc8424f13ed8614808798cc61f1ca8f683c2` (Python 3.14.3, `core.autocrlf=true`). Phase B's file set matches Decision items 1-5, plus the archived Phase A RCA and this ADR.

The validator was exercised against each failure mode it detects — MISMATCH (truncated file), EXTRA (untracked file), MISSING (renamed-away file), and the baseline partial-tree case — each correctly flagged the affected path, exited 1 with the regen hint, and was restored afterward. `--regenerate --dry-run` produced correct proposed `SHA256SUMS` content with no files written. The installed pre-commit hook blocked a commit staging a tampered CSV, printing the same MISMATCH output.

Directory set is canonically owned by `scripts/check_data_manifests.py`'s `MANIFEST_DIRS` (+ inline comments for the retirement history behind the dir-count change) — not this section's original example paths.

`pytest tests/ -q`: 105 passed (2026-05-10, ~75s). CI spot-check (operator, per spawn §5): a draft PR with a malformed `SHA256SUMS` line failed the `format` job as expected; closed without merging.
