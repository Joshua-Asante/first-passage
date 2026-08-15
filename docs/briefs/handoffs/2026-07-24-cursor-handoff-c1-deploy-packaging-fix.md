# Cursor Handoff — c1 rail deploy packaging fix (M1 telemetry modules missing from image)

> **STATUS 2026-07-24: DISCHARGED — DO NOT DISPATCH.** The defect was fixed
> independently on `main` before this brief could be dispatched: branch
> `fix/c1-rail-docker-m1-telemetry` (`7bda4a6`) added `ops/c1_rail/c1_rail_telemetry.py`
> + `core/lib/file_lock.py` to both the Dockerfile COPY list and the
> `.dockerignore` allow-list, verified by a staged COPY-set import probe
> (pre-fix `ModuleNotFoundError: c1_rail_telemetry`; post-fix clean) — i.e.
> exactly the §2.1 fix and the §0.5(B) no-Docker fallback gate this brief
> specifies. Verified on the merged tree 2026-07-24: `Dockerfile:34` carries
> `core/lib/file_lock.py`, `.dockerignore:17/:29` carry both allow-lines. This
> brief's Phase-0 step 0.0 was written to catch exactly this case and its
> prescribed return is `DONE` (no-op). Retained as the review record + its §10
> audit hooks, which remain the standing regression check.

**Date:** 2026-07-24
**Parent session:** Claude Code operator session (Joshua + Claude) — Algorithm repo review (14-agent adversarial survey + cross-check, 2026-07-24; umbrella: `docs/notes/2026-07-24-algorithm-repo-review-handoff-series.md`).
**Spawn target:** Cursor
**Repo:** `multi_firm_operations`
**Brief type:** Cursor handoff (single-step)
**Parent question:** N/A — defect repair on the R1 live surface; no Pre-Q.
**Authority:** Joshua (CEO). No commit/merge without Joshua's go. **No `core/` logic edit, no arming-config touch (`dry_run` stays `true`), no `fly deploy`.** Packaging fix only.
**Dispatch priority:** FIRST of the series — this blocks any M1 SIM drill that redeploys, and M1 `RESOLVED` gates B7 (ADR `docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md`).
**Prior-attempt note:** a background fix task for this same defect was started and its session deleted on 2026-07-24 without landing. Phase 0 step 0.0 therefore re-verifies current state; if the defect is already fixed on `origin/main`, stop and return `DONE` (no-op) with the fixing commit cited.

---

## Routing-test self-check (per `docs/adr/2026-07-14-cc-cursor-surface-allocation.md`, applied by the parent session)

- **Test 0 (dispatch-environment bytes/credentials):** No gitignored vendor data, no secrets. Docker is optional for verification (Step 2.1 gate has a no-Docker fallback). Cloud or local dispatch both eligible.
- **Test 1 (locked/governed surface):** No. Files touched: `deploy/c1_rail/Dockerfile`, `.dockerignore`. Neither is anchor-path `core/` code, Pine, or a governance doc. The two modules being ADDED to the image (`ops/c1_rail/c1_rail_telemetry.py`, `core/lib/file_lock.py`) are copied, not edited.
- **Test 2 (spec frozen):** Yes — the edit is fully enumerated in §2; the only judgment point (transitive import closure) has a mechanical resolution procedure (Step 2.1).
- **Test 3 (overhead threshold):** Marginal (2 files) — routed to Cursor anyway by operator direction (this brief is part of a dispatched series; the parent session is closing).

---

## §0 — Rule 0 reads (PHASE 0 — execute BEFORE any edit)

All anchors verified by the parent session at commit `33356ea` (2026-07-24). Read targets: `deploy/c1_rail/Dockerfile`, `.dockerignore`, `ops/c1_rail/c1_rail_listener.py`, `ops/c1_rail/c1_rail_http_server.py`, `ops/c1_rail/c1_rail_telemetry.py`, `core/lib/file_lock.py`. Cursor: read each item and post a read-report in your first response before editing. If repo state contradicts an anchor, return `NEEDS_CONTEXT` with the discrepancy quoted.

**0.0 — Blocking staleness check (FIRST):**
```bash
git fetch origin && git log origin/main -1 --format='%h %ci'
grep -n "c1_rail_telemetry" deploy/c1_rail/Dockerfile .dockerignore
```
If both files already reference `c1_rail_telemetry.py`, the defect was fixed after this brief was authored — return `DONE` (no-op) citing the fixing commit. Otherwise continue.

- `deploy/c1_rail/Dockerfile` — report the full COPY block (anchored lines 30–33 at `33356ea`: copies `ops/c1_rail/c1_rail_http_server.py`, `ops/c1_rail/c1_rail_listener.py`, `core/dd_protection.py`, `core/firm_rules.py`, `core/lifecycle.py`, `core/lib/{atomic_io,mvd,validation}.py`) and how the image lays out `ops/` vs `core/` on `sys.path` (the listener imports `from c1_rail_telemetry import ...` top-level and telemetry imports `from lib.file_lock import ...`, so report which directories land on the import path).
- `.dockerignore` — report the allow-list (anchored lines 14–29: `!ops/c1_rail/c1_rail_http_server.py`, `!ops/c1_rail/c1_rail_listener.py`, `!ops/c1_rail/c1_sizing_host_reference.py`, `!ops/c1_rail/crosstrade_payload.py`, `!core/lib/atomic_io.py`, `!core/lib/mvd.py`, `!core/lib/validation.py` — note `ops/c1_rail/c1_rail_telemetry.py` and `core/lib/file_lock.py` are absent).
- `ops/c1_rail/c1_rail_listener.py:42` and `ops/c1_rail/c1_rail_http_server.py:54` — report the `from c1_rail_telemetry import (...)` statements (both unconditional).
- `ops/c1_rail/c1_rail_telemetry.py:33` — report `from lib.file_lock import exclusive_file_lock`, then report the module's FULL import list (stdlib vs repo-internal) so the transitive closure is explicit.
- `core/lib/file_lock.py` — report its import list (expect stdlib-only; if it imports another repo module, that module joins the COPY fix).
- `git log -1 --format='%h %ci' -- deploy/c1_rail/Dockerfile .dockerignore` — expect the only prior touch to be the 2026-07-18 scaffolding commit (`d40f5a7` lineage); the M1 telemetry landing (`54b1489`, 2026-07-23) postdates it.

---

## §0.5 — Clarifying questions (Cursor variant — parent-recommended defaults)

- **(A) Transitive closure beyond the two named files.** **Recommended default:** add ONLY the modules the Phase-0 import trace proves necessary (`ops/c1_rail/c1_rail_telemetry.py`, `core/lib/file_lock.py`, plus anything their repo-internal imports require). Do not "future-proof" by copying extra `ops/` or `core/lib/` modules. If the trace surfaces a surprise dependency (e.g. a `core/lib/__init__.py` needed for package resolution), add it and report it.
- **(B) Verification without Docker.** **Recommended default:** if `docker build` is unavailable in the dispatch environment, run the Step 2.1 fallback (stage the COPY file-set into a temp dir replicating the image layout and run the import probe with the image's `sys.path`). A green fallback probe is acceptance-sufficient; say which path you took.

---

## §1 — Context

The M1 monitoring spine (landed `54b1489`, 2026-07-23) made `c1_rail_telemetry` a mandatory import of both rail entrypoints, but the Fly.io image definition predates it (last touched 2026-07-18) — the next `fly deploy` would crash the listener at import inside the container. The c1 rail is the sole live execution path (Tradeify Select 100K, disarmed, `dry_run=true`); M1 SIM drills require a redeploy, so this packaging gap sits directly on the path to M1 `RESOLVED` → B7.

**What Cursor produces:** a `cursor/*` branch PR editing `deploy/c1_rail/Dockerfile` + `.dockerignore` only, with the Step 2.1 verification output pasted in the PR body.
**What Cursor is NOT asked to do:** deploy, touch `fly.toml`, touch any `ops/*.py` or `core/*.py` content, change `dry_run`, or refactor anything.

---

## §2 — Execution plan

### Step 2.1 — Add the missing modules to the image definition and verify the closure

- **Inputs:** Phase-0 import trace.
- **Action:** add `ops/c1_rail/c1_rail_telemetry.py` to the Dockerfile COPY block and `!ops/c1_rail/c1_rail_telemetry.py` to the `.dockerignore` allow-list; add `core/lib/file_lock.py` to the Dockerfile `core/lib/` COPY line and `!core/lib/file_lock.py` to the allow-list; add any trace-proven transitive dependency the same way. Match existing formatting/ordering conventions in both files.
- **Expected output:** two-file diff.
- **Per-step gate:** `docker build -f deploy/c1_rail/Dockerfile .` succeeds AND a container-context import probe passes (`python -c "import c1_rail_listener"` with the image's working dir/`sys.path`), OR the no-Docker fallback: stage exactly the post-fix COPY file-set into a temp dir replicating the image layout and run the same probe green. A probe that fails on a *different* missing module → extend the fix per §0.5(A) and re-run; do not ship a partially-green probe.

### Step 2.2 — Closure

Report per §6. PR body must contain: the probe command + output, the final file list copied into the image, and the sentence "No logic, config, or arming state touched."

---

## §4 — Falsifiable hypothesis

N/A — defect repair, no hypothesis under test. The defect claim itself is falsifiable and Phase 0 step 0.0 tests it: if the current Dockerfile already packages the telemetry closure, the brief's premise is dead and the correct return is a no-op `DONE`.

---

## §5 — Forbidden moves

- **Deploying to verify.** Genuinely tempting (a `fly deploy` is the "real" test); forbidden — deploys are operator-attended and M1/B7-gated. The build/probe gate is the acceptance boundary.
- **Editing `ops/c1_rail/c1_rail_telemetry.py` to reduce its imports** (e.g. inlining the file lock) instead of packaging its dependencies. That is a live-surface logic edit; routed to CC under ADR test 1.
- **"While I was in there" hardening** (pinning base image digests, adding healthchecks). Log as a §6 concern; do not implement.
- **Touching `fly.toml` or any secret/env config.**

---

## §6 — Gate + status return

Use the four-state taxonomy from `references/cc_handoff.md` §6 verbatim (`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED — <sub-case>`), with the standard closure-report format (status, per-step gates, diff list, concerns, next action). This handoff produces no investigation verdict (no RESOLVED / FALSIFIED / AMBIGUOUS claim) — the four-state return plus the Step 2.1 probe gate is the entire closure.

---

## §7 — Parent-session review

Pass 1 (spec-compliance): diff touches exactly `deploy/c1_rail/Dockerfile` + `.dockerignore` (+ nothing else). Pass 2 (quality): probe output present and green; COPY list matches the Phase-0 trace closure exactly — no extras.

---

## §10 — Audit hooks (runnable)

```bash
# The two modules are packaged:
grep -n "c1_rail_telemetry\|file_lock" deploy/c1_rail/Dockerfile .dockerignore
# Expected: >=1 hit per file per module.

# No other files changed:
git diff origin/main..HEAD --name-only
# Expected: deploy/c1_rail/Dockerfile and .dockerignore only.

# Import closure still holds at any later date:
python -c "import ast,sys; sys.exit(0)"  # placeholder — re-run the Step 2.1 probe recipe from the PR body
```

---

## Verification (parent-side, before declaring handoff complete)

```bash
python scripts/check_brief.py docs/briefs/handoffs/2026-07-24-cursor-handoff-c1-deploy-packaging-fix.md
git log -1 --format='%h %ci' -- deploy/c1_rail/Dockerfile .dockerignore ops/c1_rail/c1_rail_telemetry.py
```
