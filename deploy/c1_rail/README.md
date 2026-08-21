# c1 rail sizing host — Fly.io deploy runbook

**Status 2026-08-05 — nothing in this file may be used to arm.** Two bars are currently binding and neither is described below: (a) `dry_run=false` may not be **set** while M1 monitoring is not `RESOLVED` — it reads `CODE_LANDED` (ADR `2026-07-22-c1-venue-native-monitoring-maturity.md` Addendum 2026-07-31b; enforced **only** in `ops/c1_rail/c1_rail_arm.py::m1_acceptance_reason`, so a hand-edit of `/data/c1_rail_config.json` bypasses it and is barred); (b) both Striker legs were **withdrawn from the c1 eval deployment 2026-08-04** and redeploying them is barred (ADR `2026-08-04-tradeify-venue-descope-eval-included.md`). No strategy is deployed. Rail disposition is **F2 ruled** ([S1](../../docs/adr/2026-08-07-loop-s1-environment-ratification.md) — warm/disarmed at the incumbent eval). This file covers host standup only, and its Status banner covers the state seeds at L46-48 and the arming section at L76-82.


Deploys [`ops/c1_rail/c1_rail_http_server.py`](../../ops/c1_rail/c1_rail_http_server.py) (Option C, spec [`docs/spec/c1_nt8_sizing_host_impl.md`](../../docs/spec/c1_nt8_sizing_host_impl.md) §2.5) as an always-on host. **Forward path (S2):** Python daemon → `https://<app>.fly.dev/c1/<path_token>` → this listener computes qty → CrossTrade → Tradovate. Historical TV-alert path used the same listener.

**Nothing here arms trading.** `dry_run` stays `true`. ⚠ **Deployment authority is SUPERSEDED IN PART (2026-08-04) — its deployment limb only** ([`2026-08-04-tradeify-venue-descope-eval-included.md`](../../docs/adr/2026-08-04-tradeify-venue-descope-eval-included.md)): Tradeify was de-scoped as a deployment target **evaluation included** and both Striker legs were withdrawn. **`dry_run=false` may not be set** while M1 monitoring is not `RESOLVED` (it reads `CODE_LANDED`; ADR [`2026-07-22-c1-venue-native-monitoring-maturity.md`](../../docs/adr/2026-07-22-c1-venue-native-monitoring-maturity.md) Addendum 2026-07-31b). The rail is **DISARMED and pointed at the incumbent eval** ([S1](../../docs/adr/2026-08-07-loop-s1-environment-ratification.md); F2 ruled). **Do not read any step here as authorization to arm or deploy.** This runbook only stands the host up. Public procedure owner is this file + the GO ADR — `docs/notes/rail_build/RUNBOOK.md` is not on the public tree.

## What's in this folder
| File | Purpose |
|---|---|
| `Dockerfile` | Stdlib-only image; COPYs the traced sizing-host + operator-CLI subset (`c1_rail_arm`, `c1_rail_slippage`), preserving `core/`+`ops/` layout. |
| `fly.toml` | Always-on single machine, edge TLS, `/data` volume mount, `GET /` health check. |
| `c1_rail_config.fly.example.json` | Config template for the volume (bind `0.0.0.0:8080`, `/data` paths). Fill secrets locally, never commit. |
| (repo root) `.dockerignore` | Default-excludes everything but the traced files, so no Pine/CSV/research reaches Fly's builder. |

## Prerequisites
```bash
# flyctl (Windows PowerShell):  pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
fly auth login          # account already created
```
No local Docker required — `fly deploy` builds on Fly's remote builder.

## One-time setup (from repo root)
```bash
# 1. Create the app, then set `app = "<name>"` in deploy/c1_rail/fly.toml
fly apps create c1-rail-<suffix>

# 2. Create the persistent volume (1 GB is ample; keep it ONE machine)
fly volumes create c1_rail_data --size 1 --region iad -a c1-rail-<suffix>
```

> ⚠ **Scoping note 2026-08-07 (S2b):** this directory is the **listener** app only. The Python signal daemon (when built) is a **second** Fly app with its own `fly.toml` / volume / machine. “Single machine” and DD-locality (`peak_equity` on this volume) are **per app** — never scale this app to 2, and never co-locate the daemon onto this volume.

## Deploy (from repo root — context must be repo root so COPY reaches ops/ + core/)
```bash
fly deploy . --config deploy/c1_rail/fly.toml --dockerfile deploy/c1_rail/Dockerfile
```

⚠ A redeploy is not free. Satisfy the six deploy pre-conditions in `.claude/skills/c1-rail/SKILL.md` §Agent-session authority first (single owner — deliberately not restated here). Pre-condition 4 is load-bearing: refresh `fixture_hashes` in `M1_MONITORING_ACCEPTANCE.json` in the same motion, **from hashes read IN-CONTAINER, never from tree bytes** — a skew has been open since 2026-08-02. `Dockerfile` L46-56 COPYs that artifact into the image, so pin and deploy move together.
On first deploy the machine boots and **waits** — the entrypoint finds no `/data/c1_rail_config.json` and sleeps (logs `WAIT: ...`) instead of crash-looping, so you can load the volume.

## Load config + state onto the volume (once)
Build these locally, then sftp them to `/data`:
```bash
# constants — generated from production, never hand-typed
python -c "import sys; sys.path.insert(0,'ops'); sys.path.insert(0,'core'); \
from c1_sizing_host_reference import generate_constants; import json; \
print(json.dumps(generate_constants('Tradeify_Select_100K'), indent=2))" > c1_sizing_constants.json

# state seeds
echo '{"Striker": "WATCH-1", "Striker NAS100": "WATCH-1"}' > lifecycle_state.json
# seed AT OR BELOW current Net Liq — `ratchet_peak_equity` (`c1_rail_http_server.py` L326-351) raises peak to `max(peak, current)` on the first equity read, so a LOW seed self-corrects and a HIGH one suppresses the DD tier. The account is not pristine: cumulative realized is small and positive (exact Net Liq redacted from the public tree — see the private operational archive).
echo '{"account": "Tradeify_Select_100K", "peak_equity": 100000.0, "last_updated_utc": "<now-iso>"}' > c1_dd_state.json
echo '{"current_equity": 100000.0}' > c1_current_equity.json  # only read when `equity_source == file`; the live host is not.

# config — copy the .fly.example, fill EVERY secret + a >=32-char random path_token
cp deploy/c1_rail/c1_rail_config.fly.example.json c1_rail_config.json   # secrets locally
# Prefer writers over later hand-edits of volume JSON (W6):
#   python ops/c1_rail/c1_rail_arm.py --disarm|--arm|--status --config ...
#   python ops/c1_rail/write_volume_config.py --config ... --set KEY=VAL --dry-run

# push to the volume
fly ssh sftp shell -a c1-rail-<suffix>
  put c1_rail_config.json      /data/c1_rail_config.json
  put lifecycle_state.json     /data/lifecycle_state.json
  put c1_dd_state.json         /data/c1_dd_state.json
  put c1_current_equity.json   /data/c1_current_equity.json
  put c1_sizing_constants.json /data/c1_sizing_constants.json
  exit

# then restart so the entrypoint picks up the config
fly machine restart <machine-id> -a c1-rail-<suffix>   # id from `fly machine list`
```
Delete the local copies of files containing secrets afterward.

## Verify
```bash
fly logs -a c1-rail-<suffix>          # expect "listening on ...  dry_run=True equity_source=file"
curl https://c1-rail-<suffix>.fly.dev/   # -> {"ok":true,...}  (health, unauthenticated)
```
The health check goes green when `GET /` returns 200. Then the **TradingView webhook URL** is:
```
https://c1-rail-<suffix>.fly.dev/c1/<the path_token you set>
```
WARNING — leave TV alerts unarmed and `dry_run: true`. **There is no release condition today.** (a) `dry_run=false` may not be **set** while M1 monitoring is not `RESOLVED` — it reads `CODE_LANDED` (ADR `2026-07-22-c1-venue-native-monitoring-maturity.md` Addendum 2026-07-31b; enforced **only** in `ops/c1_rail/c1_rail_arm.py::m1_acceptance_reason`, so a hand-edit of `/data/c1_rail_config.json` bypasses it and is barred); (b) both Striker legs were **withdrawn from the c1 eval deployment 2026-08-04** and redeploying them is barred (ADR `2026-08-04-tradeify-venue-descope-eval-included.md`).

## B6 → arming — SPENT, and arming is barred (2026-08-05)

Steps 1–3 are **discharged**: equity field pinned `balance.netLiq`, `equity_source=crosstrade` deployed 2026-07-19/20, B6 dry-fire **PASSED 2026-07-20** (record: private-archive runbook §B6). Step 4 is **barred on the two independent grounds above** (M1 not `RESOLVED`; both Striker legs withdrawn 2026-08-04). `--arm` is operator-run, always — an agent declines it under any authorization (`.claude/skills/c1-rail/SKILL.md` invariant 2). Operating procedure lives in the private archive (`docs/notes/rail_build/` excluded from the public seed), not here.

## Security / operational notes
- **Always-on hosting (Rule 15 / W6):** the listener is an always-on process — it runs on Fly, not on a personal desktop. Desktop = console-only (`fly ssh`, status, attended arm/disarm). See [`docs/operational_rules.md`](../../docs/operational_rules.md) Rule 15 · [`W6 ADR`](../../docs/adr/2026-08-07-w6-rail-infra-closures.md).
- **bind `0.0.0.0` is correct here, not a mistake.** The spec/code's "keep 127.0.0.1" wording assumes a same-box reverse proxy. On Fly, TLS terminates at the *edge* and the only public ingress is Fly's proxy → the container's internal port, so the app binds `0.0.0.0:8080`. The path-token remains the app-level auth gate.
- **Runs as root in-container** (v1) to avoid the Fly-volume-ownership footgun. Hardening path: a runtime `chown /data` + privilege-drop to a non-root user.
- **Secrets live on the volume** (in `c1_rail_config.json`). Hardening path: `fly secrets set` → env → an entrypoint that renders the config from env, so secrets never rest on the volume.
- **Single machine only (per app).** `peak_equity` state is local to the volume; a second machine would fork the DD state. Do not `fly scale count 2`. The future signal-daemon app is separate and must not share this volume (S2b).
- **Deploys are manual and deliberate** (`fly deploy`), never auto-on-push — an order-placing service must not redeploy from an unrelated repo commit.
- **Config / evidence tooling:** `ops/c1_rail/write_volume_config.py` (disarmed merges) · `ops/c1_rail/export_session_evidence.py` (post-disarm export) · `ops/c1_rail/c1_rail_arm.py` (arm/disarm).
