# ORB O-0 horizon edition: committed registration, specification v6

**Status:** `REGISTERED 2026-10-31`. This supersedes the [v3 registration](2026-10-31-orb-horizon-edition-registration.md) for every check not yet run. Rule 23 requires it before any new acceptance check produces a result.

| Item | Value |
|---|---|
| Specification | ORB O-0 horizon edition, draft v6 (private) |
| Private specification | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-SPEC-DRAFT-v6.md` |
| Private specification sha256 | `5987ff490b1e14e3f5692b4d913b25936819dc59cabd111fe51296bf6bd057d3` |
| Private freeze record | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-FREEZE-v2.json` |
| Private freeze record sha256 | `be8c01568f61f3c0b317348cdc4dc7948e3b4326e611efbd9f67c8bbff5a6b13` |
| Grandfathered result | Evidence-provenance check C1, PASS under v3, unchanged criterion: `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-C1-PROVENANCE-20261031.md` |
| Grandfathered result sha256 | `02206c3e5f41b728843d73ddd704eb06f55655eaf625ed47fa9cb31a2320f4d2` |
| Hash index | All three files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py` |
| Authority | Joshua, 2026-10-31: "GO route b", then "Draft v4" |

**Why a new version.** v3's calendar check could never pass: CME finalizes holiday hours about two weeks before each holiday, so a whole future year cannot be verified in advance. v6 splits the check in two:
- **Before the build:** a reference check against the published multi-year exchange holiday calendar, derived in the repo's admitted CME calendar schema, with exact equality per covered year.
- **After admission:** a standing pre-session confirmation. ORB does not trade a session whose CME hours are unconfirmed, revised or newly exceptional.

Nothing else in the criteria changes. The specification passed Codex review, READY in round 3 of 3. It carries no figures, parameter values or account data (Rule 13).

**Binding.** No new check result existed at registration; the C1 result above is the only one carried forward. Changing the criteria needs a new version, a new review and a new registration. A failed check stops the edition and returns it to Joshua. Admitting the edition as ORB O-0's successor is Joshua's separate act.

**Superseded 2026-10-31** for every check not yet run: see the [v8 registration](2026-10-31-orb-horizon-edition-registration-v8.md). Its calendar reference check failed against the accepted entries.
