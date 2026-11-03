# ORB O-0 horizon edition: committed registration, specification v11

**Status:** `REGISTERED 2026-11-01`. This supersedes the [v8 registration](2026-10-31-orb-horizon-edition-registration-v8.md) for every check not yet run (none had run under v8). Rule 23 requires it before any new acceptance check produces a result.

| Item | Value |
|---|---|
| Specification | ORB O-0 horizon edition, draft v11 (private) |
| Private specification | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-SPEC-DRAFT-v11.md` |
| Private specification sha256 | `1d056774911ac7d66595737fa5ad44842ad9dd64d8aad83c73e63b8257848e9b` |
| Private freeze record | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-FREEZE-v4.json` |
| Private freeze record sha256 | `ee6940077980e8cc880140450e43a4be5390743e5125af7563d759987e23ee2b` |
| Reviews | Codex rounds 1–3 (v9 NOT READY, v10 NOT READY, v11 READY), hashed in the freeze record |
| Carried records | Unchanged from v8: C1 provenance and the C2a reference derivation |
| Hash index | All new files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py`. |
| Authority | Joshua, 2026-10-31: "GO route b", "Draft v4", "Fix the 2027 list"; 2026-11-01: "Yes, write v9" |

**Why a new version.** After S-PAIR, ORB's evaluation build replaces the canary build on the trading host and keeps its type names. The v2 canary stage runs on Sim101 while that build is installed, so the v2 build must compile beside it, and under v8 it could not. v11 makes the v2 build a full copy of ORB's runtime files under a fixed identifier map, with a new display name. It adds a check that the v2 and evaluation builds compile together, write to disjoint locations and can generate no common order or OCO identifier. The window, the calendar and every other criterion are v8's. The specification carries no figures, parameter values, identifiers from private sources or account data (Rule 13).

**Binding.** No new check result existed at registration; only the carried records are reused. Changing the criteria needs a new version, a new review and a new registration; this specification's review budget is spent. A failed check stops the edition and returns it to Joshua. Admitting the edition as ORB O-0's successor is Joshua's separate act. Schedule: build from 2026-11-09, signature by 2026-12-11, admission by 2026-12-18.
