# ORB lifecycle L1: integrated acceptance packet (2026-10-02)

**Status:** PROPOSED. It is returned through the coordinator for the operator's acceptance of the integrated L1 change, which [§59 Ruling 6](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-6--orb-resting-entry-lifecycle-l1-2026-09-26) requires before edition freeze ("the integrated change and its verification are returned for acceptance before edition freeze"). This note assembles the parts and their evidence. It accepts, freezes, qualifies and authorizes nothing.

**Executor:** cloud worker (Claude Code, Opus 5.5), ticket K, branch `claude/railspec-ca-close-contract`, cut from `origin/main` `bd30646`. Line numbers are at `bd30646` unless a commit is named. The AC-3 part is on this branch at `e53c8de`; the rail-spec markers on this branch are appended in place, so rail-spec line numbers are the same on both.

## Decision requested

Accept the five parts below as the integrated L1 change of §59 Ruling 6, as reaffirmed by [Ruling 7(a)](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#ruling-7--orb-lifecycle-l1-reaffirmed-and-the-account-fence-classification-contract-2026-09-27): ORB's base entry is placed once and rests until it fills or an applicable cancellation ends it, with no one-bar expiry, no periodic reissue, and the earlier operational cutoff still applying.

Acceptance would discharge Ruling 6's *Return* and the successor pre-registration's §8 step 1 condition (["before freeze, the integrated ORB-1/RC-9/rail S2/qualification replay change and its verification are returned to the operator for acceptance"](../briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md), `:143`). It would adopt the AC-3 correction (part 5). It would **not** freeze an edition, word ORB-1's final text (OWED at freeze), run a replay or E1, or accept the fence obligation of Ruling 7(b).

## The five parts

| # | Part | Where | Authority | Applied by, and status | Verification evidence |
|---|---|---|---|---|---|
| 1 | **ORB-1** (edition pre-registration) | Successor [pre-registration](../briefs/pre-registration/2026-10-02-tradeify-route-native-editions-successor-prereg.md) `:86` (the ORB-1 row, with the Ruling 6 and 7(a) markers), `:93` (the "open before freeze" marker), `:143` (§8 step 1). The closed original carries the same markers at `2026-09-25-tradeify-route-native-editions-prereg.md:51`, `:58` | Ruling 6 ("bounded amendments to ORB-1"); Ruling 7(a) ("ORB-1 … states the lifecycle in words") | H3, 2026-09-27, on the original; carried into the successor (DRAFT). Final wording **OWED at freeze** | Text only. It states L1 in the ruling's words and reads "as declared, S2" on rail S2 as amended 2026-09-27 |
| 2 | **RC-9** (replay spec) | [Replay spec](../spec/2026-09-12-tradeify-synchronized-replay-spec.md) `:5` (header callout), `:55` (RC-9 marker) | Ruling 6 ("replay-spec RC-9"); Ruling 7(a) | H3, 2026-09-27 (dated marker; RC-9's other clauses unchanged) | Text only. The marker exempts ORB's base entry from the one-bar cancel and names H4 (R) as the implementation |
| 3 | **Rail S2, S4 and AC-8 markers** | [Rail spec](../spec/2026-09-12-c1-multi-leg-rail-extension-spec.md) `:3`–`:18` (amendment callout), `:73` (S2: the one-bar sentence struck for ORB's base entry), `:77` (S4: ORB's base entry is not a "stale resting entry" by age), `:114` (AC-8: the L1 case, outcome unchanged), Change history 2026-09-27 entry | Ruling 6 ("rail-spec S2"); Ruling 7(a) ("corresponding specification correction"). Ruling 6 does not name S4 or AC-8; H3 aligned them under 7(a) ([disposition](2026-09-27-orb-fence-ruling6-disposition.md) §2) | H3, 2026-09-27, applied under Ruling 7's authorization | Text only. The same callout also carries the Ruling 7(b) fence markers (`:44`, §5 entry `:188`); those belong to the separate fence obligation, not to this packet |
| 4 | **Qualification replay correction** (H4 checkpoint R) | `ops/c1_rail/qualification/replay.py:27`–`:35` (`L1_BASE_ENTRY_LEGS = {"orb_mnq_v7"}`, `_one_bar_cancel_applies`), call site `:553`. Commit `18b8b60`, merged in [PR #522](https://github.com/Joshua-Asante/first-passage/pull/522) (`38e62ee`) | Ruling 6 ("the qualification replay, with the affected tests and freeze identities updated"); Ruling 7(a) ("corrected as a bounded change") | H4, coordinator-accepted 2026-09-27, synthetic scope ([H4 card](../briefs/handoffs/2026-09-27-h4-fence-classification-orb-l1-repair.md) `:296`, *Coordinator acceptance of the return*; commit `deb6a23`). Scope is the Q3 default: only ORB's base entry is exempt, and the one-bar cancel still applies to every other resting entry or add | **Tests** (`tests/ops/qualification/test_replay.py`): `:247` not cancelled one bar after admission (replaces the old pin at `:214`–`:223`); `:260` fills on a later-bar crossing; `:271` ends on the port's session-end cancel and releases capacity; `:282` cancelled at the scheduled cutoff; `:301` one-bar cancel unchanged for other resting orders; `:321` matches the emulator with no schedule overlay.<br>**Coordinator re-verification** at `18b8b608`: 116 new or changed nodes passed; 725 related-suite nodes passed, 6 skipped; PR CI green, including the Linux qualification jobs. At `9e18d85` (comments only): 116 passed.<br>**Re-run for this packet** at `bd30646`: `.\fp.ps1 python -m pytest tests/ops/qualification/test_replay.py -k "orb_base_entry or one_bar_cancel_still_applies"`, ops env Python 3.13.2 (doctor: 62 locked packages matched, signing dependency present): **9 passed, 96 deselected**; record `status: completed`, `verification_exit_code: 0`, `source_stable: true`, commit `bd30646`. The record sits under this worktree's ignored `.cache/fp-verification/20261002T194729Z-131942c30763/` and does not survive the worktree; the coordinator's acceptance above is the durable record |
| 5 | **Rail AC-3 correction** | Rail spec `:109`, PROPOSED marker in the AC-3 row; branch commit `e53c8de` | Ruling 6 ("correction of rail-spec AC-3's market-add description"); Ruling 7, *Relation to Ruling 6* ("owed with the integrated change") | This branch, **PROPOSED, not adopted**. The ratified AC-3 text stays in force until acceptance | Text, against source evidence. The accepted port's add is a market order with close-time timing and never rests ([lifecycle evidence](2026-09-26-orb-lifecycle-evidence.md) row 2 at `:25`, C3 at `:51`); S1 (`:71`) lists the ORB add as a market add; R-Q gives the ORB add 0 in PROTECTED. No code or test changes: TB-I3's `test_ac_3_*` encodes the corrected case when it is built |

## Consistency read

The five parts state the same lifecycle:
- placed once;
- no one-bar expiry and no periodic reissue;
- the earlier operational cutoff still applies (halt/resume §5; RC-8 in replay);
- the "applicable cancellations" given as examples are the same in each text: the port's own session-end cancel, the scheduled cutoff, a takeover's cancel of a displaced entry, and incident handling. The replay code's comment (`replay.py:27`–`:30`) names the same four.

Ruling 7 does not define "applicable cancellation". Every text lists examples and none claims to be exhaustive.

Only AC-3 needed more than a lifecycle edit. Its problem was the add's order type, not the entry's lifetime (lifecycle evidence C3; disposition §2, "C3 (separate)").

## Not in this packet, and still open

| Item | Owner | Status |
|---|---|---|
| S4's example "ORB adds at a mode change through `set_mode`" (rail spec `:77`). Under the corrected AC-3 there is no resting ORB add for a mode change to cancel. Ruling 6 does not name S4's example | Rail spec | Not amended here. Returned for the operator to say whether part 5 should also cover it |
| ORB-1 says "one contract per base or add" but does not say the add is a market order | Successor pre-registration | Final wording OWED at freeze |
| The takeover-cancel and incident-handling ends of a resting ORB base entry in the replay. H4's named tests cover the port's cancel and the cutoff; whether other replay tests cover a takeover cancel of a resting ORB base entry was not checked here | Coordinator | Not checked |
| RC-9's duplicate key `(leg, kind, bar_time)` against the replay's `path_time` | Replay spec | STILL OPEN (disposition §2; not a lifecycle item) |
| The broker's day-order expiry (time-in-force) for an entry that now rests for hours | Commissioning §3.7 documentary step; X-4 step-4 read | STILL OPEN (disposition §2) |
| GC-4: whether cancelling a resting stop entry ends its suspended children | X-4 | Trace owed |
| The trailing parameters in AC-3's inputs, which the route-native ORB edition removes (§59 Ruling 3) | Rail spec / edition | Not decided by the AC-3 correction |
| The freeze inventory. No inventory is fixed yet: H4's card §5 has both checkpoints land before it is fixed (CP-6). The corrected `replay_kernel` (`trust_domain.py:142`) is what enters it. A later S2/S4 Linux refresh is a coordinator dispatch decision (H4 acceptance) | Coordinator | At CP-6 |
| The Ruling 7(b) fence obligation: the real producer, route integration, the CC-3 halt and E2/E3 quarantine | T09/TB-I3 | Separate; not part of L1 acceptance |

**Not granted by this note:** edition freeze, ORB-1's final wording, replay or E1 dispatch, a private-port run, T09 dispatch, gate B–D acceptance, deployment, arming or GO.
