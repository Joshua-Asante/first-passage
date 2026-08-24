# Notice — Ox-alpha on the per-trade bound election: surviving rows travel with the election; they do not elect

**Notice ID:** N-2026-08-24-ox-alpha-per-trade-bound-election
**Observed:** 2026-08-24
**Author:** Cursor Cloud Agent (commission: send the crux of the Q-TRADECAP-2 problem to `stealth/ox-alpha`, sanitized, with enough context)
**Source:** OpenRouter `stealth/ox-alpha` chat-completions, one sanitized adversarial review of a genericized election packet. Reconciled against the real brief before any row is a finding.
**Status:** `RESOLVED` — elect-2 [`Accepted`](../../adr/2026-08-24-q-tradecap-2-elect-alert-tripwire.md); O4/O5/O6/O7/O9 disposed there
**Lives in:** `docs/notes/notice/N-2026-08-24-ox-alpha-per-trade-bound-election.md`

Lane: [`2026-08-22-ox-alpha-adversarial-lens-scope.md`](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md) §2 (adversarial lens on a decision-authoring artifact — not the candidate-generation carve-out). Zero authority; objections are not findings until the table below. Frozen option set is not amended.

---

## §0 — Source anchor

- **Source:** sanitized prompt sha256 `2aeefcc66c16a8bccbbe77ba4996371b05eae5c6dd4dc9f7ef2e27ee3a57b3ef` (3,836 bytes). Model `stealth/ox-alpha` via `https://openrouter.ai/api/v1/chat/completions`, `$OPEN_ROUTER_API`, no `HTTP-Referer` / `X-Title`. HTTP 200 after an initial 429, `finish=length`, 952 prompt / 8,000 completion tokens, `$0`. Content channel empty; numbered O1–O9 sit in the reasoning channel (same class as Use 2). Fingerprint sweep on outgoing text: CLEAN (no operator name, no INQHIORI, no `dd_protection`, no strategy/firm names, no dates, no dollar figures, no repo slug, no vendor/product names).
- **Reconciled against:** [`Q-TRADECAP-2`](../../briefs/Q-TRADECAP-2-per-trade-bound-election.md) @ `adb090f` (2026-08-24); [pre-reg](../../briefs/pre-registration/Q-TRADECAP-2-verdict-preregistration.md) @ `4d6761b` (2026-08-24); [`Q-TRADECAP-1 closure`](../../briefs/closures/Q-TRADECAP-1-closure-resolved.md) @ `afa0d56` (2026-08-23).
- **Observed at:** 2026-08-24. No transcript stored in-repo (reasoning-channel dump; sanitization bar). This notice holds the objection table.

Amendment-first (this session, literal):

```
$ rg -n 'Q-TRADECAP-2' lab/CATALOG.md docs/briefs/INDEX.md docs/rejected_candidates.md
# INDEX Open row + recently-closed parent pointer; no CATALOG / rejected row

$ python scripts/check_advisor_dedup.py --keywords "ox-alpha per-trade bound TRADECAP"
# nearest: Q-TRADECAP-1 closure (parent); Q-TRADECAP-2 session entry. No ox-alpha consult owner.
```

New notice required. Do not amend the frozen pre-reg.

---

## §1 — The observation

A genericized election packet (confirmed per-trade realized-loss gap; three frozen closes; recommended default ID **2**) was sent under §2. The lens returned a numbered draft that was cut at O9 by `finish=length`. Reconciled against the real brief, four rows survive as election-carry; none elect a close; none invent a fourth frozen ID.

---

## §2 — Why it stands out (the N signal)

- **Baseline:** every objection is candidate input until checked against the unsanitized artifact. Mixed-quality “find everything” output is expected ([validation addendum](../../adr/2026-08-22-ox-alpha-adversarial-lens-scope.md)).
- **Delta:** the surviving cluster is fail-open / false-discharge / threat-model precision on ID **2**, plus a reminder that **1-size** adds nothing unless it is tighter than the existing qty law. That informs Phase 1 wording; it does not flip H-GEO or the frozen set.
- **Frequency:** additional production use of the lane. Several objections survived, so revert trigger (b) does not tick. The Use-N ledger remains incomplete across concurrent sessions.

---

## §3 — Reconciliation (not findings until this table)

Verdicts: **SURVIVES** (carries into the unpaid election) · **PARTIAL** · **DISCHARGED** · **DECLINED**.

| ID | Ox-alpha claim (compressed) | Against the real artifact | Verdict |
|---|---|---|---|
| O1 | Only the missing actuator blocks a realized-loss cap; G1/G2 are calibration | The brief already split **1-realized** (gated on Phase 0a + `sl=`) from Option 1-as-staged (G1∧G2∧G3). Joint predicates gate the *legacy staging*, not every realized cap | PARTIAL — do not let G1/G2 be read as blocking **1-realized** |
| O2 | G2 mixes starting-equity % with a peak-relative trail | G2 is a start-of-eval geometry check that the legacy example is not conservative. It does not flip H-GEO. Forbidden move “do not import the legacy %” still holds | PARTIAL |
| O3 | “As-staged is not startable” is vacuous / restates G1 | That headline *is* Phase 0: it blocks importing the CFD pair unmodified. Phase 1 is the election among the frozen three | DISCHARGED |
| O4 | “Unbounded” fights an intraday-enforced trail (venue flatten exists) | Parent “unbounded” means no *per-trade* bound inside the trail, not “loss can exceed the trail.” ID **2**’s real job is pre-breach warning | SURVIVES — precision on the threat model; do not re-litigate absence |
| O5 | ID **2**’s “realized loss” trigger is blind to unrealized bleed | Unspecified on the brief. Scale-in / open MAE can miss the tripwire until after a venue breach | SURVIVES — if **2** is elected, name MTM vs realized before first fill |
| O6 | ID **2** fails open on first fill (no threshold, no feed watchdog, no ack) | Brief: tripwire is dark until a fill; threshold is a later election. That is fail-open as specified | SURVIVES — if **2** is elected, freeze threshold-before-fill or accept fail-open on the light ADR |
| O7 | Electing observe-only as the “close” ratchets the gap shut in prose | Brief forbids treating **1-size** as discharging realized loss; it does not hang the same non-discharge label on **2** | SURVIVES — if **2** is elected, record observe-only, not a close of the gap |
| O8 | Single-operator alert has no responder in the hazard | Already the estate’s operator-hour constraint. Not a fourth close | PARTIAL |
| O9 | **1-size** may add nothing over the existing qty law (truncated) | Sizing already uses stop-distance to set qty. **1-size** is only new if it is a tighter named $ ceiling | SURVIVES — do not sell **1-size** as new protection unless it is tighter |
| OPT | Send-site stop, or hold arming until an actuated bound, as a fourth close | Send-site `sl=` is **1-realized**’s broker-stop mode (already frozen; gated). Arming-hold is sequencing, not a close | DISCHARGED as a fourth ID |

---

## §4 — Routing decision

**RESOLVED** — elect-2 is `Accepted`. Do not graduate a new Q. Do not amend the frozen pre-reg. Do not wire a tripwire or cap from this notice.

Decision: RESOLVED
Reason: surviving rows disposed on the Accepted ADR.

---

## §5 — If HOLD: re-check trigger

- **Re-check date:** elect-2 ADR `Accepted` or declined, or disaster-stop Phase 0a `PASS`, whichever first
- **Trigger condition:** the Accepted write-up disposes O4/O5/O6/O7/O9 or explicitly declines them
- **Drop trigger:** operator declines the Proposed ADR and deletes STATE queue row 2 (parent `AMBIGUOUS-HOLD`)
- **Calendar entry:** none — board write is the elect-2 ADR

---

## §10 — Audit hooks

```bash
# Outgoing payload was sanitized
rg -n -i 'Joshua|INQHIORI|dd_protection|first-passage|Tradeify|Striker' \
  /opt/cursor/artifacts/ox_alpha_per_trade_bound_outgoing_sanitized.md
# Expected: empty

sha256sum /opt/cursor/artifacts/ox_alpha_per_trade_bound_outgoing_sanitized.md
# Expected: 2aeefcc66c16a8bccbbe77ba4996371b05eae5c6dd4dc9f7ef2e27ee3a57b3ef

# Consult recorded; pre-reg frozen
rg -n "ox-alpha-per-trade-bound-election" docs/adr/2026-08-22-ox-alpha-adversarial-lens-scope.md
rg -n "N-2026-08-24-ox-alpha-per-trade-bound-election" docs/briefs/Q-TRADECAP-2-per-trade-bound-election.md
test -f docs/briefs/pre-registration/Q-TRADECAP-2-verdict-preregistration.md
```

---

## Verification

```bash
$ python scripts/check_brief.py docs/notes/notice/N-2026-08-24-ox-alpha-per-trade-bound-election.md --type notice
# Expected: RESULT: NOT CHECKED
```
