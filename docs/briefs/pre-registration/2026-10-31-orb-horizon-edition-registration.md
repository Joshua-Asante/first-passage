# ORB O-0 horizon edition: committed registration

**Status:** `REGISTERED 2026-10-31`. This is the committed registration Rule 23 requires before any acceptance check of the ORB O-0 horizon edition produces a result.

| Item | Value |
|---|---|
| Specification | ORB O-0 horizon edition, draft v3 (private) |
| Private specification | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-SPEC-DRAFT-v3.md` |
| Private specification sha256 | `f70d052b39f8f14672b3f314b8d95521d57bbe87b26c37fcaa0cd2d2cbe01af3` |
| Private freeze record | `local_artifacts/book-repair-2026-10/orb-edition/ORB-EDITION-HORIZON-FREEZE-v1.json` |
| Private freeze record sha256 | `0ef759cd73bbf481c3d3230390b3484d5ac23a6975a688034d389e406c15594b` |
| Hash index | Both files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py` |
| Authority | Joshua, 2026-10-31: "ORB stays in the book past January", then "GO route b" |

**What the hashes bind.** ORB's accepted Pine has a date-window input, inherited as a backtest window, that stops new base entries after a fixed end. The edition is a new Pine file and a new native engine. Each differs from its accepted predecessor only in that end, which moves to the horizon of a CME-verified early-close calendar. The pinned sources stay unchanged. The specification fixes the acceptance checks, their order and the failure policy: evidence provenance, a calendar check against CME's published schedule, single-line source diffs, offline replay identity, the native acceptance rerun and signature. No historical trade changes, so no new trial is counted (K += 0). The specification is private under Rule 13: this file carries no figures, parameter values or account data. The specification passed Codex review in round 3 of 3.

**Binding.** No check result existed at registration. Changing the criteria needs a new version, a new review and a new registration. A failed check stops the edition and returns it to Joshua. Admitting the edition as ORB O-0's successor is Joshua's separate act. The forward stop rule ([registration](2026-10-31-tradeify-forward-stop-rule-registration.md)) changes only by its own signed addendum.
