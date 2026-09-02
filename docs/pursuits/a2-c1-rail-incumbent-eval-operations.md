# c1 rail + incumbent-eval operations — KEEP

**Class:** (a) active campaign · **Standing:** KEEP
**Aim served:** A1/A3 — deploy + operate-safely on the Tradeify incumbent eval, rail warm/disarmed
**Measure:** M1 `RESOLVED` reached honestly (validator-backed, not status-only); weekly token-trade obligation discharged each week it falls due
**Survive bound:** $700 spend ceiling (rail GO ADR); one operator token-trade decision per week (unrecoverable if missed) — this is the binding weekly cost, not hours
**Review date:** ongoing — no fixed expiry; M1 gate is the arming precondition, not a review date
**Ratified:** 2026-08-09 (GSUB-1 Phase 3)

**Owner artifacts:** [`S1 environment ratification`](../adr/2026-08-07-loop-s1-environment-ratification.md) ·
[`S2 signal-host fork`](../adr/2026-08-07-loop-s2-signal-host-fork.md) ·
[`rail GO`](../adr/2026-07-17-c1-rail-build-account-registration-go.md) ·
[`M1`](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md)

**Open residual — CLOSED 2026-08-16:** weekly-recurrence was UNRULED; ruled fresh-decision-per-week
is the standing design (STATE.md decision index, 2026-08-16). The weekly obligation itself is
unchanged — still owned here, still tracked at `STATE.md` §Scheduled forward triggers → *Weekly —
recurring*.

⚠ **Corrected 2026-08-09 — "R8" was a misnomer and this record propagated it.** R8 was a
*Bulenox-scoped* hygiene track, **closed 2026-07-10** (R6 NO-GO ADR §2), whose six items never
included a token trade or any scheduled instrument. The real artifact is the **idle-clock
observer** ([`spec`](../superpowers/specs/2026-08-02-idle-clock-tracking-spec.md)). **The
observation gap is now closed** — the obligation is booked in `STATE.md` §Scheduled forward
triggers → *Weekly — recurring*, which the existing daily 07:04 `daily-repo-truth-sync`
forward-obligation radar reads. It was previously invisible only because queue-table rows carry no
date and that radar scans the forward-triggers section. No new standing config was required.

**Source:** [`GSUB-1 inventory`](../briefs/programs/GSUB-1-inventory-and-dispositions.md) row a2
