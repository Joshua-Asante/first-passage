# `ops/c1_signal_daemon/` — S2b Python signal host

**Retired 2026-10-29** with the c1 rail ([rail ADR addendum](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-10-29--c1-retired-as-an-execution-route-staged-decommission),
[Stage 1 record](../../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#stage-1-record--2026-11-03)): nothing here is rebuilt, redeployed or armed; the code
stays until the Stage 3 PRs. Its last recorded state was NullStrategy with emission disabled.
Databento remains retired; retained fixtures are offline tests, never live-source evidence.
Build ADR: [`docs/adr/2026-08-08-s2b-signal-daemon-build.md`](../../docs/adr/2026-08-08-s2b-signal-daemon-build.md).
Fly standup: [`deploy/c1_signal_daemon/README.md`](../../deploy/c1_signal_daemon/README.md).

Listener leg: [`../c1_rail/`](../c1_rail/). Posture:
[`AGENTS.md`](../../AGENTS.md) §Live-execution posture.
