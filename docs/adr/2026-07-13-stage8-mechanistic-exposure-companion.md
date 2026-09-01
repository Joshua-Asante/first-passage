# ADR 2026-07-13 — Stage-8 breadth gains a mechanistic-exposure companion (realized-correlation blindness for episodic same-beta legs)

**Status:** `Accepted` — operator ratified 2026-07-13, **before** the DISC-CAMP-0 pre-registration freeze (superseding-ADR adoption route per template change control; no §8 override needed)
**Supersedes:** none
**Superseded-by:** none
**Superseded-in-part-by:** none
**Retain-until:** none
**Decision date:** 2026-07-13
**Authors:** claude.ai Tech Advisor (draft) · Joshua (decision)
**Related:** [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) (Stage-8 row + §Campaign-defaults change control); [`docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md`](2026-07-12-dsr-k-rule-and-variance-floor-supersession.md) (precedent: pre-freeze gate-reachability amendment via ADR); [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) §2; [`docs/adr/2026-07-13-prop-account-book-segregation.md`](2026-07-13-prop-account-book-segregation.md) (consumer of §2c); [`docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md`](../briefs/2026-07-12-08-08-packet-pretriage.md) (Class A consumer — proposed input only).
**Layer:** methodology / discovery-pipeline gate design — not locked-parameter; Campaign-defaults frozen values untouched.

---

## §0 — Rule-0 reads (2026-07-13)

- [`docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md`](../ltm/briefs/rnd-pipeline/discovery-campaign-template.md) — Stage table + §Campaign-defaults content-read 2026-07-13 (last touch `dffcb5e`). Stage-8 admission statistic today: "5th-column ENB / cross-leg-correlation delta vs the locked 4-leg frame (reproduces the Q-NEFF-1 4-leg anchor first)". Change control: frozen values move only via superseding ADR; campaign-level override lives in that campaign's §8 with reason.
- [`ops/prop_envelope_default.md`](../../ops/prop_envelope_default.md) — §2 content-read 2026-07-13 (git `802ee60`).
- [`docs/methodology/strategy_lifecycle.md`](../methodology/strategy_lifecycle.md) — working-tree Select-String read 2026-07-13: scope note "the four current legs are one beta" (ratified one-beta doctrine this ADR's evidence instantiates).
- Breadth tooling paths verified via `git ls-files` 2026-07-13: `lab/research_utils/breadth.py`, `.claude/skills/strategy-validation/scripts/breadth.py` (content read owed at implementation, not needed for this gate-design decision).
- Evidence panels (claude.ai reconcile 2026-07-13; Step-0 clean; context panels, NOT anchors; sha256 pins in [`docs/briefs/Q-TVCOV-1-tv-bar-coverage-census.md`](../briefs/Q-TVCOV-1-tv-bar-coverage-census.md) §0).

---

## §1 — Symptom (measured 2026-07-13)

Three legs of the ratified one-beta family, on their seven-year futures panels (2026-07-12 TV exports: Striker→MYM, Striker-NAS→MNQ, Aegis→6J), measure as follows. Direction census: 287/287 long, 290/290 long, 155/155 short-yen — every trade in all three books is the same macro side. Entries cluster in the NY morning; time-in-market is 0.62% / 0.67% / 0.27% of the clock; in-market overlaps in seven years: 64 (MYM×MNQ), 18 (MNQ×6J), 4 (MYM×6J); days all three traded: 6; days all three lost: 0. And yet pairwise monthly correlations on equity-deflated streams are −0.10 / +0.13 / −0.01, worst-decile-month overlap 0–1 of 9, same-day both-lose rates at or below the independence baseline, max-DD windows fully disjoint.

The zero is a sampling fact, not an exposure fact: episodic strategies are almost never in-market together, so the shared factor has no data through which to express itself. Consequences: (1) Stage-8's realized-stream statistic cannot detect same-beta duplication for exactly the strategy class the discovery engine most plausibly emits (NY-session, direction-conditional, episodic) — a candidate that is the incumbent beta with a fresh label passes by construction; (2) any bootstrap that resamples these realized streams (week-block included) mechanically reports near-independence and cannot price the common-mode event (zero occurrences in seven years to resample). The known common-mode kill path stays both uninsured and unmeasured. This finding is robust to the Q-TVCOV-1 census outcome: it is driven by structural non-overlap, which only strengthens if pre-2022 segments are discarded.

---

## §2 — Decision (proposed amendments; exact text)

**(a) Campaign template, Stage-8 row** — append a companion clause:

> …reproduces the Q-NEFF-1 4-leg anchor first. **Companion (mechanistic exposure):** every Stage-8 candidate files an exposure declaration — {unconditional or regime-conditional side; entry session window (ET); expected in-market minutes/yr; per-book-leg structural overlap = expected simultaneous-in-market minutes/yr × sign-agreement} — and the campaign pre-registration binds a structural-overlap admission threshold at Stage 0. Realized-correlation/ENB deltas remain reported but are not sufficient for breadth admission for episodic candidates (in-market < 5% of session clock).

**(b) Envelope §2** — add item 5: exposure-coordinates annotation (same fields) required at closure alongside `DEPLOYABLE-DEFAULT-ENVELOPE`, so the coordinates travel to the deployment fork.

**(c) Consumer note** — 08-08 Class A (accept-beta fork), proposed input only, packet owner accepts/rejects: the program-level MC pricing the accept-beta decision should add a shock-conditional module — impose an adverse NY-morning gap over a pre-registered grid (e.g., −1% to −5%) on a max-concurrency day, all in-market legs at entry-time sizing, evaluated against per-account rule sets — precisely because stream resampling cannot generate the event. Not a unilateral packet edit.

**Adoption route (operator picks one):** superseding-ADR route (this file, per template change control) or DISC-CAMP-0 §8 override with reason if freeze pressure dominates; silent adoption is forbidden by the template either way.

---

## §3 — Alternatives considered

| Alternative | Why ruled out |
|---|---|
| Tighten the correlation/ENB threshold | Blind is blind at any threshold — the statistic reads ≈0 for same-beta episodic legs regardless of the cut. |
| Demand longer panels before Stage 8 | Event frequency, not panel length, binds: seven years produced six all-three days. |
| Handle exposure only at the deployment fork | Too late — discovery K budget is spent re-manufacturing the incumbent beta; Stage 8 exists to gate book-level admission. |
| Drop the correlation delta entirely | Q-NEFF-1 anchor reproduction still catches dense-overlap duplication cheaply; companion, not replacement. |

---

## §4 — Falsifier (for this amendment itself)

**H (hypothesis):** the blindness is material to bust risk.

**Test (pre-registered here, before any run):** run the §2c shock-conditional module on the current three-leg family versus the stream-bootstrap estimate under identical per-account rule sets. **Falsifier:** if, at every point of the pre-registered shock grid, the joint bust-probability delta is < 1pp absolute, the companion demotes to annotation-only (declaration retained, no admission gate) via superseding ADR. Grid and rule sets frozen in the run's pre-registration; first run owed with the 08-08 packet work; hard check 2026-11-08.

**Verdict (binary):** RESOLVED (delta ≥ 1pp somewhere on the grid — companion stands) / FALSIFIED (< 1pp everywhere — demote to annotation-only) / AMBIGUOUS (module not runnable by 2026-11-08 — escalate at that gate).

---

## §5 — Forbidden moves

- Adopting into DISC-CAMP-0 after its freeze without the §8 override trail (tempting under schedule pressure).
- Choosing or trimming the shock grid after seeing MC output.
- Letting exposure declarations become entry filters — declarations describe, never filter (default #4's "test conditions, never filters" applies).
- Editing the §Campaign-defaults table or the Stage-8 row in place without this ADR's ratification event.

---

## §6 — Consequences

**Positive:** same-beta duplication caught at admission where K is cheap; the 08-08 fork priced on the actual tail mechanism; coordinates persist to the deployment fork and the segregation ADR's joint MC.

**Negative (real cost):** one more registration field per campaign + one more MC module; ceremony risk if the threshold never binds — §4 exists to kill the gate if it proves immaterial.

**Downstream updated on ratification:** campaign template Stage-8 row; envelope §2 (item 5).

**Downstream NOT changed (explicit):** Campaign-defaults frozen values (#1–#6), SPA/StepM/DSR machinery, Q-NEFF-1 anchor reproduction, locked parameters.

---

## §7 — Implementation plan

- **Phase 0** — this draft (2026-07-13). ✅
- **Phase 1** — operator disposition before DISC-CAMP-0 freeze (adopt / defer-to-§8-override / reject). ✅ **Adopted 2026-07-13.**
- **Phase 2** — apply §2a/§2b diffs + `docs/SESSIONS.md` entry; hand §2c to the 08-08 packet owner. ✅ **Applied 2026-07-13** (template Stage-8 row; envelope §2 item 5; §2c recorded as a proposed input in the 08-08 pre-triage brief — packet owner dispositions at packet assembly).

---

## §10 — Audit hooks

```bash
grep -n "exposure declaration" docs/ltm/briefs/rnd-pipeline/discovery-campaign-template.md || echo "Stage-8 companion not applied (check disposition)"
grep -n "exposure-coordinates" ops/prop_envelope_default.md || echo "envelope §2 item 5 not applied (check disposition)"
grep -n "shock-conditional" docs/briefs/programs/2026-07-12-08-08-packet-pretriage.md || echo "08-08 packet has not dispositioned §2c"
```

**Verification**

```bash
python scripts/check_brief.py docs/adr/2026-07-13-stage8-mechanistic-exposure-companion.md --type adr
```

---

## Change history

| Date | Change | By |
|---|---|---|
| 2026-07-13 | Drafted, Status Proposed | claude.ai Tech Advisor |
| 2026-07-13 | Ratified — Status `Accepted`; §2a/§2b diffs applied to template + envelope; §2c handed to 08-08 packet | Joshua (decision) · Claude Code (apply) |
