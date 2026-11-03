# `deploy/` - retired c1 packaging

The [c1 retirement ruling](../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-10-29--c1-retired-as-an-execution-route-staged-decommission)
retires the Python listener, signal daemon and CrossTrade route.

The two Dockerfiles and their dedicated image-validation workflow, shell runner
and packaging tests were removed on 2026-11-03. Retrieve them through the
[removal ledger](../docs/ltm/README.md#removal-batches).

The per-app [listener](c1_rail/README.md) and [daemon](c1_signal_daemon/README.md)
runbooks are historical. Their manifests identify the apps for shutdown; example
configs are not evidence of host state. The runtime, shutdown utilities, M1
records and fixtures remain pending consumer-by-consumer retirement.

**Host status, 2026-11-03:** this session's earlier `fly apps list --json`
attempt failed with `no access token available` and made no host changes.
The later operator-run [Stage 1 record](https://github.com/Joshua-Asante/first-passage/blob/4af558dc0692834ff4daa8b314fa4a19503b4489/docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#stage-1-record--2026-11-03)
reports both apps disarmed and scaled to zero, empty machine lists, and endpoint
timeouts at 14:55 UTC. This reconciliation did not independently query Fly.
That report starts the approximately two-week rollback window on November 3
(review around November 17); Stage 2 remains a separate operator decision.
Fly billing and remaining resources are unverified; see the
[subscription owner](../docs/pursuits/d13-flyio-subscription.md).
