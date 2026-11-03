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

**Host status, 2026-11-03:** verification and scale-to-zero are blocked because
`fly apps list --json` returned `no access token available`. No host change was
made. Fly cost remains unknown in the [subscription owner](../docs/pursuits/d13-flyio-subscription.md).
