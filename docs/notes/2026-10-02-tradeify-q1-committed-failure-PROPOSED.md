# Tradeify Q1 committed failure decision

**PROPOSED for the statistical owner and Joshua.** Source pin: `5eb800b50792dd204741f81e668c02f562b59a29` (origin/main inspected 2026-10-02). Q1 remains due before T06/S8; C3 acceptance did not adopt this classification. [Ledger :1937](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L1937)

Recommend counting a valid committed assessment of a named falsifier criterion as FALSIFIED despite later exhaustion. This preserves the criterion-based gate without inventing aggregate publication.

## Current contract and runtime trace

ADR §4 rejects on a failed legality screen, N1 cutoff, N2 limb or Part A; it does not expressly require aggregate result commit for rejection. [Admission ADR :148](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/adr/2026-09-12-tradeify-book-protection-instance-admission.md#L148)

The full-E1 contract preserves committed FAIL after exhaustion, forbids post-exhaustion result/seal commits, and separates statistical accounting from present authority. [Spec :137](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md#L137)

The checkpoint transaction binds predecessor/capture, persisted intent and receipt; it advances the checkpoint family to COMMITTED. Later settlement can replace the progression state with exhaustion while retaining the receipt as history. Exact historical lookup returns the saved receipt with current validity. This is support for the accounting distinction, not an implemented FALSIFIED classifier. [Store :1007](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/campaign_store.py#L1007) [Store :1037](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/campaign_store.py#L1037) [Store :1100](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/campaign_store.py#L1100) [Store :1170](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/campaign_store.py#L1170) [Store :2768](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/ops/c1_rail/qualification/execution/campaign_store.py#L2768)

## Options and proposed wording

**A — Count committed criterion failure, recommended.** Exhaustion cannot erase unfavorable evidence. Classification need not wait for a publication operation that the exhausted campaign cannot perform.

**B — Require aggregate publication.** Creates an exhausted-with-committed-FAIL category. The failure must remain binding and accounted for; this option needs explicit reconciliation with the criterion-based ADR rather than permission to rerun.

**C — Case-by-case disposition.** Leaves Q1 open and therefore does not satisfy its before-T06/S8 decision gate. [Ledger :1937](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L1937)

Proposed addition to ADR §4, referenced from full-E1 §2.5:

> A valid authenticated assessment committed under the frozen contract before exhaustion, establishing failure of a criterion named in this section, counts as FALSIFIED and closes the attempt even when exhaustion prevents aggregate result commit. Retain the assessment evidence, receipt and operational exhaustion state; do not fabricate a result receipt. Exhaustion without a committed criterion failure establishes no statistical verdict. This classification confers no continuation, replacement draw, seal or activation authority.

## Contradictory cases and remaining decision

Proposed acceptance cases: committed N1 FAIL then exhaustion → FALSIFIED plus operational exhaustion; captured but uncommitted FAIL → no verdict under this clause; committed PASS then exhaustion → no RESOLVED; timer/resource interruption alone → operational terminal. These preserve the existing committed-evidence rule and prohibition on converting interruption to FAIL. [Spec :137](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md#L137) [Spec :200](https://github.com/Joshua-Asante/first-passage/blob/5eb800b50792dd204741f81e668c02f562b59a29/docs/superpowers/specs/2026-09-17-protected-full-e1-campaign.md#L200)

**Dependency:** root relayed approval of term 8: joint N2/PART_B FAIL-pattern reconciliation in all three result validators and result-role/fault evidence. Its documentary mirror is PR #610, not this main pin. Q1 cannot stand in for authentic prefix publication; that dependency belongs to the separately dispatched H9 integration. [Pending mirror :693](https://github.com/Joshua-Asante/first-passage/blob/497b937aa01ebc381d6b0b025eafaee454bc5d1e/docs/superpowers/plans/2026-09-18-full-e1-execution-slices.md#L693)

**Decision requested:** statistical-owner/Joshua disposition of A/B/C and closure wording. S6 approval is not Q1 adoption. Source review only; runtime tests are unnecessary for this proposed accounting text and were not run.
