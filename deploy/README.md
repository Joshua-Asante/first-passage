# `deploy/` - retired c1 packaging

The [c1 retirement ruling](../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#addendum-2026-10-29--c1-retired-as-an-execution-route-staged-decommission)
retires the Python listener, signal daemon and CrossTrade route.

The apps and volumes were [destroyed on 2026-11-05](../docs/adr/2026-07-17-c1-rail-build-account-registration-go.md#stage-2-record--2026-11-05). No host remains.

The two Dockerfiles and their dedicated image-validation workflow, shell runner
and packaging tests are removed. Retrieve them through the
[removal ledger](../docs/ltm/README.md#removal-batches).

The per-app [listener](c1_rail/README.md) and [daemon](c1_signal_daemon/README.md)
runbooks are historical. The `fly.toml` files stay only for the deploy guard's
tests and leave with it in the last S3-2 PR.
