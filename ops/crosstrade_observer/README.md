# CrossTrade observation collector

Collect one bounded batch of read-only observations from the direct Tradovate
API. This is a diagnostic tool. Every summary reports E1, E2 and E3 as **unproven**;
`collected` means the read batch finished, not that recovery is complete.

From the repository root, with Python 3.11 or newer:

```powershell
python -m ops.crosstrade_observer --config C:\private\c1_rail_config.json --journal .crosstrade-observer/observations.sqlite3 --limit 500 --max-pages 10
```

Config requires `account`, `destination: "tradovate"`, and `secret_key` using
the existing rail config names. The tool reads the file without modifying it.
Keep credentials in that private file, never command-line arguments. API access
and a linked Tradovate account must already exist. It does not link accounts,
refresh credentials, open a WebSocket, place orders, or change the rail.

Each invocation reads snapshot, scoped positions/working orders/current-session
fills, and durable fill history. History starts from the beginning on every run,
following cursors up to `max-pages`. This deliberate overlap can detect later
captures and revisions. It does not prove completeness. History pagination limits
apply to all currently stored matching rows; increase the finite budget if needed.
Do not run batches more often than every five seconds; a one-shot call does not
schedule itself. Endpoint errors are retained; they are not automatically retried.

The default `.crosstrade-observer/` directory is ignored by Git. The SQLite file
contains private account observations; back it up, keep it access-controlled and
do not publish it. An explicitly chosen different directory needs equivalent
protection. Directory mode requests do not configure Windows ACLs. Standard output
contains run ID, counts, flags and unproven qualification states; no account name,
credential, source body or private error message. Raw JSON is retained in the
private database after credential redaction; transport parse errors retain a code.

The schema binds the journal to one configured account name. Observed numeric
account IDs are checked within each batch. Name reuse or broker-account migration
requires separate operator consideration; there is no qualified identity registry.
Responses from a snapshot may contain other linked accounts; the private journal
retains the response and the collector checks the configured account's match.

The journal stores:

- `runs`: local batch state (`running`, `collected`, `limited`). A crash leaves
  its run `running`; later runs expose `prior_unfinished_runs` without changing it.
- `observations`: request kind, local timestamps, HTTP status, body and flags.
  Order and position rows are observations only, never gross allocation proof.
- `fill_versions`: unique observed execution-ID/body pairs linked to observations.
  Fee changes are classified separately; economic conflicts remain visible in
  subsequent reports. Neither version overwrites the other.

Each observation and its fill revisions commit atomically with FULL SQLite sync.
On crash, rerun collection against the same database. No page or local timestamp
becomes a broker watermark. Cache reuse, partial responses, malformed data,
unavailable account binding, conflicting rows and bounded pagination are reported.
`history_stored_rows_exhausted` refers only to the enumerated stored rows. A history
page with incomplete or invalid rows cannot silently become complete evidence.
The observed live snapshot `asOf` lacks a timezone suffix. It is retained with
`snapshot_timezone_unavailable`; the collector does not assume UTC or use that
value to prove ordering. This limitation does not discard its valid account
binding or prevent collection of separately timestamped history fills.

Exit codes: `0` = batch collected (still unqualified; inspect warning flags and
unfinished-run count), `2` = batch finished with limitations, `1` = local failure
or invalid configuration. Argument-parser errors also exit `2` without a report.
Database errors stop collection; prior committed observations remain available.

To inspect a retained report locally without making network requests:

```python
from ops.crosstrade_observer.journal import Journal

with Journal(".crosstrade-observer/observations.sqlite3", "YOUR_ACCOUNT") as journal:
    print(journal.report("RUN_ID_FROM_THE_COLLECTOR"))
```

The collector does not expose order lifecycle requests: the approved first slice
collects the core read batch. The separate capability probe records historical
lifecycle errors and documented report limits. RecoveryOwner integration,
protection/FIFO reconstruction, E1 coherence and E3 request fencing remain outside
this diagnostic component.

Verification:

```text
python -m pytest tests/ops/test_crosstrade_observer.py -q
python -m pylint ops/crosstrade_observer --errors-only
```
