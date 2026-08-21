# S7 alignment manifest — TOMBSTONE (public tree)

**Status:** tombstone · 2026-08-21 · does **not** discharge any S7 row
**Owner (discipline):** [`docs/spec/2026-08-07-loop-s7-repo-alignment-spec.md`](../spec/2026-08-07-loop-s7-repo-alignment-spec.md)
**Why this file exists:** live ADRs and the S7 spec linked here as if the ~70-row Posture-A propagation manifest were on disk. It is not. The public clone started from the 2026-08-14 seed; `git show 45e3ceac:docs/notes/2026-08-07-posture-a-alignment-manifest.md` is **not a valid object** in this repository (`fatal: invalid object name '45e3ceac'`).

**Do not** treat a missing row as discharged. S7 `RESOLVED` remains blocked until the original body is restored from the private archive (or a fresh manifest is authored under a new ADR).

**What still stands without the row body:** W4/W5/W6 same-PR sweeps recorded on those ADRs; W1 RESULTS, CI-from-`gates.yml`, and `requirements-research.lock` remain **owed** on the S7 spec progress line.

Campaign register: [`docs/notes/audits/2026-08-21-coherence-campaign.md`](audits/2026-08-21-coherence-campaign.md) C-P0-01 / C-P5-03.
