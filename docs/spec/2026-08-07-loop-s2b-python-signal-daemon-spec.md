# SPEC S2b: Python signal daemon (minimal)

Status: Accepted · 2026-08-08 · authorizes nothing ($0 · K=0) · depends: S2 (Accepted)
Objective: Specify the Python-native signal daemon that POSTs B1 JSON to the existing
listener — bar source, signal contract, heartbeat, fail-closed on feed loss, second Fly app
— without authorizing a build.

Steps:
1. **Bar source:** name a live CME bar feed for the daemon’s evaluate loop (research panels
   / TV exports are not the live feed); document reconnect + staleness thresholds in the
   build ADR, not here.
2. **Signal contract:** emit the existing B1 JSON shape to `POST /c1/<path_token>` on the
   listener app (same fields the TV path used); no listener contract change; fresh
   `order_id`/bar_time tags every fire.
3. **Heartbeat:** expose operator-visible liveness (process up + last-bar age); page/log on
   missed heartbeat per build ADR thresholds.
4. **Fail-closed on feed loss:** on feed unhealthy/stale/missing, **emit no entry/add
   signals** (kill-on-feed-loss); exits/flats policy deferred to the build ADR under
   fail-closed default.
5. **Second Fly app:** deploy as a **separate** Fly app with its own machine/volume/state —
   never share the listener’s `peak_equity` volume; “single machine” remains **per app**
   (DD-locality invariant stands).
6. Build requires a separate operator GO after this spec is Accepted (or absorbed into a
   build ADR); this spec alone authorizes **no** code, image, or deploy.

Gate: RESOLVED if an Accepted build ADR (or explicit operator build GO citing this spec)
lands the daemon under steps 1–5; FALSIFIED if a daemon is built that collapses into the
listener app, skips fail-closed, or alters the B1 listener contract without a superseding ADR.
Boundary: no build authorized by this spec alone · no arming · no TV login/actuation
automation · no Striker redeploy · listener DD-locality never collapsed.
Reads: [S2 ADR](../adr/2026-08-07-loop-s2-signal-host-fork.md) ·
`ops/c1_rail/c1_rail_http_server.py` @ `2345095` · `deploy/c1_rail/fly.toml` (single-machine
note) · [M1 ADR item-5 origin](../adr/2026-07-22-c1-venue-native-monitoring-maturity.md)
Owner: S2 signal-host fork.
