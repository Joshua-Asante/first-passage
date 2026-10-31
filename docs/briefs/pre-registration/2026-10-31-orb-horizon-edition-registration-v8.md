# ORB O-0 horizon edition: committed registration, specification v8

**Status:** `REGISTERED 2026-10-31`. This supersedes the [v6 registration](2026-10-31-orb-horizon-edition-registration-v6.md) for every check not yet run. Rule 23 requires it before any new acceptance check produces a result.

| Item | Value |
|---|---|
| Specification | ORB O-0 horizon edition, draft v8 (private) |
| Private specification | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-SPEC-DRAFT-v8.md` |
| Private specification sha256 | `c302a206c4cb988d2cf00785945577db80cfb5332189c66df8e2ca124616ed42` |
| Private freeze record | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-FREEZE-v3.json` |
| Private freeze record sha256 | `22881c7f376763e5bd9218893dab778bc4f727e1a5bac02030e3c88b06e85a42` |
| Carried record | Calendar reference check under v6 (its sources and derived reference set carry forward; its FAIL verdict applied to the accepted list): `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-C2A-REFERENCE-20261031.md` |
| Carried record sha256 | `2324fbc61979722cd5286146b5b8de0bf1b0b9596e9ec08c961f4c11075cc869` |
| Hash index | All three files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py`. The evidence-provenance result carried since v3 stays registered under the v6 registration. |
| Authority | Joshua, 2026-10-31: "GO route b", "Draft v4", then "Fix the 2027 list" |

**Why a new version.** Under v6, the calendar reference check found that the accepted strategy's early-close entries for the newly opened year do not match the published exchange calendar: they were written before that calendar existed. v8 is a clean restart, not a patch. The edition now changes two strategy inputs:
- the date window's end;
- that year's early-close entries, set to the published-calendar reference.

Every earlier entry and every other input stays unchanged. A private check confirms that no changed entry can affect any bar before the current end, so the historical evidence is unchanged. The standing pre-session confirmation of exchange hours stays. The specification passed Codex review, READY in round 2. It carries no figures, parameter values or account data (Rule 13).

**Binding.** No new check result existed at registration; only the records named above are carried forward. Changing the criteria needs a new version, a new review and a new registration. A failed check stops the edition and returns it to Joshua. Admitting the edition as ORB O-0's successor is Joshua's separate act.
