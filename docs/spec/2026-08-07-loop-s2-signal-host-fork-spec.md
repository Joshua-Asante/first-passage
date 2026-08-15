# SPEC S2: signal-host fork

Status: RESOLVED · 2026-08-07 · ADR Accepted [`2026-08-07-loop-s2-signal-host-fork.md`](../adr/2026-08-07-loop-s2-signal-host-fork.md) · authorizes nothing ($0 · K=0) · depends: S1
Objective: Rule the signal host for new strategies — a Python daemon POSTing the existing
payload contract straight to the listener (TV leaves the live chain, and the port-parity
problem class with it) vs Pine/TV alerts as today.

Steps:
1. Read `c1_rail_http_server.py` (the POST surface + path-token auth) +
   `c1_rail_listener.py` + `crosstrade_payload.py`; confirm the contract is
   origin-agnostic, or list the delta. ✅ origin-agnostic (path_token + JSON only).
2. Decision ADR (one page): recommendation Python-native; record the costs — live bar
   feed, daemon uptime/heartbeat, kill behavior; Pine remains a research/export surface.
   The Python branch must also rule M1 item 5 (requires a real **TV** strategy signal;
   deletion DECLINED 2026-07-31, silent redefinition barred): discharge it via TV before
   cutover, or supersede its signal-origin definition in this ADR. ✅ Python-native;
   origin expressly superseded in S2 ADR.
3. If Python wins: author S2b (daemon spec — bar source, signal contract, heartbeat,
   fail-closed on feed loss) before any build. ✅ [S2b](2026-08-07-loop-s2b-python-signal-daemon-spec.md) authored; no build.

Gate: RESOLVED if the fork is ruled either way by Accepted ADR; FALSIFIED if S1 rules the
environment away — the fork is moot.
Boundary: TV login/actuation automation stays absolutely prohibited on both branches;
no daemon build before S2b.
Reads (at HEAD `a6a5fe6` 2026-08-07): `ops/c1_rail/c1_rail_http_server.py` ·
`ops/c1_rail/c1_rail_listener.py` · `ops/c1_rail/crosstrade_payload.py` ·
[rail GO ADR](../adr/2026-07-17-c1-rail-build-account-registration-go.md) ·
[M1 ADR Addendum 2026-07-31](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md)
Owner: new (docks to the rail GO ADR).
