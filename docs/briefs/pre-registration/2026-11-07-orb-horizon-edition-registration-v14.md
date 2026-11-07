# ORB O-0 horizon edition: committed registration, specification v14

**Status:** `REGISTERED 2026-11-07`. This supersedes the [v11 registration](https://github.com/Joshua-Asante/first-passage/blob/9d95503/docs/briefs/pre-registration/2026-11-01-orb-horizon-edition-registration-v11.md) for every check not yet run (none had run under v11).

| Item | Value |
|---|---|
| Specification | ORB O-0 horizon edition, draft v14 (private) |
| Private specification | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-SPEC-DRAFT-v14.md` |
| Private specification sha256 | `bf2b52481a259e62ec578b9bd31033703c59f7590340b60aebdbf8858a3aaec4` |
| Private freeze record | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-FREEZE-v5.json` |
| Private freeze record sha256 | `d0421d3797eceb78af44c592765f67ab39cee28a69578bfd765017de77587ffa` |
| Baseline | The frozen eval source, pinned with the ruled delta in `ORB-EDITION-BASELINE-RECORD-v1.json` (`9682745fe72accd9747f5a8de209e8185a1e7e918df8f114dac6e865b93a0318`) |
| Reviews | Codex rounds 1–3 (v12 NOT READY, v13 NOT READY, v14 READY), hashed in the freeze record. The third was an extra round Joshua granted, run against the frozen source |
| Carried records | Unchanged from v11: C1 provenance and the C2a reference derivation |
| Hash index | All new files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py`. |
| Authority | Joshua, 2026-11-07: "Approve as drafted" and "One more round, once final", typed to the research coordinator; "Yes, start one" and "Yes, freeze src-v4", by relay |

**Why a new version.** After v11 was registered, Joshua ruled four fixes to ORB's eval source, in two runtime files. v11 rebuilds the successor from card 1's original files and allows three edits only, so the successor would lose those fixes at admission. v12 rebuilds it from the ruled eval source. It adds a check that this source differs from card 1 only by the ruled fixes, and it reruns coexistence and acceptance against it. Two additions keep the problem from recurring: a later ruled source change carries over by a dated addendum and a repeat of the affected checks, and a check at admission confirms that the baseline equals the live eval source. The window, the calendar, the identifier map and the permitted edits are v11's. The specification carries no figures, parameter values, identifiers from private sources or account data.

**Binding.** No new check result existed at registration; only the carried records are reused. Changing the criteria needs a new version, a new review and a new registration. A failed check stops the edition and returns it to Joshua. Admitting the edition as ORB O-0's successor is Joshua's separate act. The frozen source stays subject to the Sim101 check and any Tradeify condition; a ruled change follows the specification's baseline-move rule. Schedule, unchanged: build from 2026-11-09 at the earliest and 2026-11-30 at the latest, signature by 2026-12-11, admission by 2026-12-18.
