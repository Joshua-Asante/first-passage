# Tradeify Select 100K forward stop rule: committed registration

**Status:** `REGISTERED 2026-10-31`. This is the committed registration that Rule 23 requires before the first forward session of the owned Select 100K forward attempt (Aegis A-0 and ORB O-0).

| Item | Value |
|---|---|
| Rule | Forward stop rule for the owned Select 100K forward attempt, draft v11 (private) |
| Private rule text | `local_artifacts/book-repair-2026-10/FORWARD-STOP-RULE-DRAFT-v11.md` |
| Private rule text sha256 | `c31b950060e4f6f971e4b5ec982863191916582399b78494b1bec480d78184fc` |
| Private freeze record | `local_artifacts/book-repair-2026-10/FORWARD-STOP-RULE-FREEZE-v2.json` |
| Private freeze record sha256 | `f646a000091c1b0cfd3639d7ed973c44f257839124e9d1cbaa48e8cfab342698` |
| Hash index | Both files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py` |
| Signed | 2026-10-31, by Joshua |

**What the hashes bind.** The rule decides, for each strategy, whether to keep it, drop it, or halt it for a fault, by a sequential test on its forward trades. The rule text and its freeze record are private under Rule 13: this file carries no figures, parameters or account data. Before signing, the rule passed a final Codex review round, and the freeze record passed a further narrow round authorized by Joshua.

**Binding.** Any change to the rule after the first forward session ends this rule's record. A successor needs Joshua's authorization and a new registration, and its evidence starts again from zero.
