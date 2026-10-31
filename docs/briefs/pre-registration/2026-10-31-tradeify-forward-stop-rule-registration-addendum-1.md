# Tradeify Select 100K forward stop rule: registration of Addendum 1 (ORB horizon edition)

**Status:** `REGISTERED 2026-10-31`. This registers Addendum 1 to the forward stop rule registered in [2026-10-31-tradeify-forward-stop-rule-registration.md](2026-10-31-tradeify-forward-stop-rule-registration.md), before the first forward session of the owned Select 100K attempt, as the addendum requires.

| Item | Value |
|---|---|
| Private addendum | `local_artifacts/book-repair-2026-10/FORWARD-STOP-RULE-ADDENDUM-1-ORB-HORIZON-DRAFT-v3.md` |
| Addendum sha256 | `7d2ce3e1f74b4b97133ccc6cf89ff4846918599a65bc50b15b2e250c8bcadc5b` |
| Private signature record | `local_artifacts/book-repair-2026-10/FORWARD-STOP-RULE-ADDENDUM-1-SIGNATURE-20261031.md` |
| Signature record sha256 | `dd6d16a453e6610d0ad8474b9341d17ed9adb8f05ff964493aaa0fa5bc875f2d` |
| Hash index | Both files are registered in [`docs/evidence/PRIVATE_EVIDENCE.sha256`](../../evidence/PRIVATE_EVIDENCE.sha256) and archived with `scripts/evidence_archive.py` |
| Signed | 2026-10-31, by Joshua (Part B) |

**What it registers.** A **conditional expiry mechanism.** The rule ends ORB's test at ORB's date gate. If Joshua admits the ORB horizon edition as ORB's successor, that date gate becomes the edition's date gate from the moment of admission. The change touches no threshold, observation or falsifier, and it cannot revive a strategy that was already dropped or ended. Admission after the first forward session implements this registered condition and is not a further change to the rule. Part A of the addendum is a correction of a stated month and changes no behaviour.

Like the original registration, this file carries no figures, parameters or account data (Rule 13).
