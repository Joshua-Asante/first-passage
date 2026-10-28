# Azure compute VM policy (fp-compute-01)

Single owner of the standing rules for the Azure compute VM. Other documents
link here instead of restating them. Per-run private-data admissions stay with
[campaign §60](../briefs/programs/2026-09-03-seven-strategy-select-campaign-state.md#60--agent-read-access-to-the-accepted-books-pine-and-runtime-ports-2026-09-25).
Rulings are Joshua's, given directly; dates are when he gave them.

## Host

`fp-compute-01`: Windows Server 2025, 32 vCPU / 64 GiB, East US, about $2.90 per
running VM-hour. Joshua provisions it and holds its credentials. Agents reach it
only through Azure CLI Run Command under the `az login` Joshua opens, and never
read or store the VM admin password. The network security group has no custom
inbound rules; the public IP was removed 2026-10-25, and whether the VM still has
outbound internet access is unverified. Subscription and tenant identifiers never
appear in public commits, PRs or records.

## Cost and deallocation

- Spend ceiling **$125 per week** (2026-10-09). No monthly budget alert and no
  time-of-day shutdown (2026-10-09).
- The session that starts the VM verifies `VM deallocated` before its turn ends.
  A run may last up to **12 hours**; for multi-hour runs the local PC stays
  plugged in and [`scripts/azure_vm_watch.py`](../../scripts/azure_vm_watch.py)
  stays on for the whole allocation (2026-10-24).
- **Backstop** (design approved and deployed 2026-10-25;
  [`scripts/azure_backstop/`](../../scripts/azure_backstop/runbook.ps1)): an Azure Automation
  runbook runs every 4 hours. It deallocates the VM if it is stopped but still
  allocated, if average CPU over the last hour is under 5% (stuck, or finished and
  left on), or if it has run 12 hours since its last start; a busy VM under 12
  hours is left running. Its identity holds only a custom role on the VM: read
  status, CPU metrics and activity log, and deallocate.
- **Weekly cost check** (2026-10-25): Codex reads the actual VM hours and cost for
  the week, read-only through the Azure portal with browser tools, and compares
  them with the watcher ledger so unwatched time is caught.

## Access

Agent Azure roles are restricted and granted case by case (2026-10-25): each
grant names the identity, the actions and the scope (VM or resource group). Only
Joshua grants roles. Current grants on the VM: the backstop's `FP compute VM
backstop` role, and the VM's own identity's `Offline compute self-deallocate` role
from the PR #746 runner work.

## Private data and teardown

- Private inputs go to the VM only for runs §60 names, on its terms; Pine never.
- Each private run puts its inputs on a **dedicated data disk** that is deleted
  at teardown; the deleted disk is the proof of removal (2026-10-25).
- Teardown, in order: copies listed absent per §60, the run's data disk detached
  and deleted, the **storage account deleted** (2026-10-25), then the VM verified
  deallocated.

## Open

Where Docker/Linux runs go; a standing admission rule for public-only runs;
whether PR #746's runner is resumed or closed; removal of the existing smoke-test
debris (retained Run Command, storage account).
