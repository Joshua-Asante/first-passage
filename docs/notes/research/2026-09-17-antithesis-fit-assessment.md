# Antithesis fit assessment for First Passage

**Date:** 2026-09-17  
**Status:** research recommendation; no purchase, integration, deployment, or
live-trading authorization  
**Question:** How beneficial would Antithesis be to First Passage?

## Executive decision

**Do not adopt Antithesis now. Revisit it only for a tightly bounded proof of
concept after the execution rail becomes an offline, multi-container system
with a realistic broker/transport simulator.**

Antithesis is a strong technical match for a future version of the execution
rail: it explores concurrent system states under network, process, CPU, and
clock faults, evaluates explicit properties, and deterministically reproduces a
failure. Those capabilities target exactly the difficult future questions—no
duplicate order after ambiguous delivery, conservative recovery after a crash,
single-writer state, and safe behavior through time discontinuities.

It is a weak match for most of First Passage today. The repository is primarily
Python research, deterministic Monte Carlo, governance checks, and two separately
deployed single-machine services. Antithesis says its primary use is
fault-tolerance testing of **stateful distributed systems**; all components must
be x86-64 Linux containers, the topology must be Docker Compose or Kubernetes,
the environment has no internet access, and every external dependency must be
co-deployed or mocked. First Passage has two Dockerfiles but no Compose or
Kubernetes topology, and the live path depends on hosted/external systems.
Substantial harness work would therefore precede any useful test.

The recommendation is a **deferred, evidence-gated POC**, not a rejection of the
product. Do not add its SDK, CI action, or vendor configuration yet.

## What the product is (and is not)

Antithesis runs a whole containerized system in a deterministic simulated
environment. It combines randomized workloads with guided exploration and
fault injection, checks user-authored properties over the resulting branching
timelines, and supplies reproducible debugging artifacts. Its documented faults
include asymmetric network disruption, partitions, node throttling/pause/kill,
clock jumps, CPU modulation, and custom faults.

This is broader than a Python property-testing library and narrower than a
general test runner:

- It is most valuable when correctness depends on interactions among processes,
  persistence, retries, clocks, and failures.
- It does not validate a trading strategy's economic edge, statistical method,
  broker rules, data provenance, or production behavior that a mock fails to
  model.
- The Python SDK can express `always`, `sometimes`, reachability, and
  unreachability assertions, but the platform still needs a workload that drives
  the system into meaningful states.
- Tests can launch through a web app, REST API, CLI, or GitHub Action. The
  documented minimum run is 15 minutes; the vendor describes common practice as
  roughly 30–60 minutes on mainline commits and 6–8 hours nightly.

## First Passage fit

### Where the value could be high

| First Passage risk | Antithesis contribution | Residual limitation |
|---|---|---|
| Daemon → listener delivery around timeout, retry, or asymmetric partition | Explore many fault schedules and preserve a replayable counterexample | A faithful CrossTrade/Tradovate double is required; the real services cannot be reached from the isolated environment |
| Durable state and ownership locks around crash/restart | Kill, pause, throttle, and restart containers while checking single-writer and monotonic-state properties | Current deployment keeps each service and volume on a separate Fly app; a test topology must faithfully reproduce those boundaries |
| Duplicate or uncertain transport outcomes | Check that one logical signal never creates more than the permitted intent and that ambiguity fails closed | The repository explicitly notes that CrossTrade does not idempotently deduplicate `order_id`; the harness must model acknowledgement-loss and downstream acceptance separately |
| Session/time boundaries | Inject clock jumps and CPU scheduling changes while checking that stale or out-of-session actions remain barred | Simulated time does not prove exchange-calendar or broker-clock truth; canonical calendar fixtures remain necessary |
| Recovery and safety invariants | Turn existing fail-closed rules into continuously evaluated system properties | Assertions only protect what is specified, and a passing run is exploration evidence rather than proof |

The best target is therefore the **offline execution boundary**, especially
`ops/c1_signal_daemon/` plus `ops/c1_rail/`. The Monte Carlo engine and normal
unit/governance checks should remain in the existing launcher: they are
single-process, already seedable/deterministic, and do not justify a distributed
simulation platform.

### What a hermetic topology would mean here

“Hermetic” should not mean “put the existing two containers on a private Docker
network and call the result production-like.” It means that one versioned
topology contains every executable, fixture, dependency, configuration binding,
and test driver needed for the scenario; startup and the test make no DNS or
network call outside that topology; and a fresh host can reproduce the run from
pinned inputs. Antithesis itself supplies the isolated environment. Its Docker
Compose guidance specifically says **not** to declare an internal Compose
network, because that prevents the platform from attaching its fault-injection
network.

For First Passage, the smallest honest topology would be:

| Component | Responsibility | Durable state / boundary |
|---|---|---|
| `signal-daemon` | Read simulated bars, evaluate the frozen strategy, and send an intent to the listener | Its own volume and owner lock; never shares listener state |
| `rail-listener` | Authenticate, validate, size, enforce safety state, and send to the relay endpoint | A separate volume containing listener state; single effective writer |
| `counterparty-simulator` | Model the relay and broker protocol as distinct stages, including accepted, rejected, delayed, duplicated, and accepted-but-response-lost outcomes | An append-only acceptance ledger used as the external truth oracle |
| `market-input-simulator` | Publish deterministic bars, session transitions, stale data, malformed data, and wrong-contract inputs | Immutable scenario fixtures; no licensed or private market data |
| `workload-checker` | Select actions, query the observable state, emit properties, and declare setup ready | No production credentials and no authority outside the test topology |

The canonical source should be one Compose project plus shared, variant, and
instance bindings rather than copied YAML files. A shared definition would own
images, health checks, volumes, service names, and dependency order. A local
variant could bind locally built images and conventional deterministic tests;
an Antithesis variant could bind registry image digests, its ready signal, test
templates, and SDK output. A scenario file would bind only the chosen fixtures
and simulated outcome policy. The resolved configuration and every image digest
should be recorded together, so setup validation, fault exploration, and replay
refer to the same system identity. Secrets should be references supplied by the
runner; this topology should need none.

**Use Compose first, not Kubernetes.** The current rail is a small fixed graph
of single-instance services with local durable volumes. Compose represents that
graph with less machinery and fewer irrelevant controllers. Kubernetes becomes
useful only if First Passage needs to test Kubernetes-specific behavior—pod
rescheduling, readiness and rollout behavior, persistent-volume attachment, or
service discovery—or if Kubernetes becomes the production target. Introducing
it solely for Antithesis would add control-plane states that do not match the Fly
deployment and would make results harder, not easier, to interpret.

### Benefits before Antithesis is purchased

The topology is not throwaway vendor preparation. It would deliver value with
ordinary local and CI tests:

1. **One end-to-end contract.** Today the two images and deployment definitions
   prove their pieces separately. A Compose project would make ports, health
   conditions, startup order, configuration validation, and volume ownership an
   executable interface between them.
2. **Safe counterparty semantics.** The acceptance ledger can distinguish “the
   request was never received” from “the request was accepted but the response
   was lost.” That distinction is necessary to test the unsafe-retry risk that a
   success-only HTTP stub cannot expose.
3. **Repeatable recovery tests.** Tests can stop a container after intent
   persistence but before send, after downstream acceptance but before receipt
   persistence, or while replacing state. Fresh runs start from explicit volume
   fixtures instead of an operator's Fly volume.
4. **Enforced offline safety.** Running successfully with host egress disabled
   proves that an integration test cannot accidentally reach CrossTrade,
   Tradovate, Fly, a feed, or a package/data download. This is a test-boundary
   claim, not proof that production egress policy is correct.
5. **Faster ordinary debugging.** Developers can reproduce a cross-service
   failure with one resolved topology and scenario instead of coordinating two
   remote apps and private state. CI can retain the resolved configuration,
   image identities, fixture identity, and simulator ledger as evidence.
6. **A measurable baseline.** Conventional scripted fault cases establish what
   is already cheap and reproducible. An Antithesis trial then has to find
   schedules beyond that baseline or shorten diagnosis; “the containers ran” is
   not enough to justify the vendor.
7. **Better fault targets later.** Separate containers give Antithesis meaningful
   nodes to partition, pause, throttle, kill, and restart. Separate durable
   volumes and a checker give it observable invariants rather than mere process
   survival.

### What the topology would not prove

- A simulator is an executable hypothesis about external behavior. It can create
  false confidence if authentication, retries, acknowledgement timing, or order
  state transitions differ from the real relay and broker. Its cases must be
  traceable to vendor contracts or sanitized observations and reviewed whenever
  those contracts change.
- Compose lifecycle, DNS, storage, TLS termination, and restart behavior are not
  identical to two separate Fly applications. Production-specific deployment
  checks remain necessary; the topology targets application-level safety under
  explicitly modeled boundaries.
- Hermetic execution does not establish market-data correctness, strategy edge,
  broker-rule compliance, or authorization to emit. It must remain incapable of
  reaching a live endpoint.
- Health checks and dependency order remove accidental startup noise, but tests
  must still exercise early/late readiness and recovery explicitly rather than
  hiding those states forever behind `depends_on`.

### Why immediate adoption has low expected return

1. **The required system shape is absent.** The two deployable services each
   have a Dockerfile and Fly definition, but there is no repository-owned
   Compose/Kubernetes environment that starts the complete rail and its
   dependencies together.
2. **Network isolation removes the real counterparties.** Antithesis requires
   internet-independent execution. Broker, relay, hosted feed, and Fly behavior
   must be replaced with local doubles. That is useful only if those doubles
   encode the failure semantics that matter.
3. **The current live posture is disarmed and attended.** The signal daemon is
   packaged separately with emission disabled, while the listener is deliberately
   single-machine and dry-run constrained. The near-term bottleneck is not
   discovering distributed production interleavings.
4. **The strongest present test assets are not its sweet spot.** Research and
   risk calculations benefit more directly from fixture quality, statistical
   validation, boundary tests, and the existing repeatable verification records.
5. **Commercial value cannot yet be calculated.** Public documentation describes
   performance tiers and core-hour usage but does not publish a price schedule.
   Contract price, included core hours, support, retention, and overage terms
   must be obtained before an ROI claim is possible.
6. **There is integration and governance overhead.** A useful trial needs a
   hermetic topology, images, workload, stable properties, secret-free fixture
   data, CI policy, report retention, and an owner. Vendor guidance estimates
   2–4 developer days for system setup plus 1–2 developer days for the initial
   test when prerequisites already exist; First Passage should budget more
   because the hermetic system and external-service doubles do not yet exist.

## Bounded POC gate

Contact the vendor for a POC only after **all** of these entry conditions hold:

1. A repository-owned, x86-64 Docker Compose topology can start the daemon,
   listener, durable state, and local counterparty simulator without internet.
2. A normal local integration test can drive a signal through that topology and
   observe accepted, rejected, delayed, duplicated, and acknowledgement-lost
   outcomes.
3. A real historical concurrency/recovery defect—or a deliberately planted
   equivalent—has a crisp externally observable symptom. This follows the
   vendor's recommended “known hard bug” POC structure and prevents a demo from
   being scored on an invented easy case.
4. Secrets, private market data, account identifiers, and production credentials
   are absent from every image, log, and uploaded configuration.
5. Procurement supplies written pricing, core-hour accounting, retention,
   support, security/data-location terms, export/deletion behavior, and POC exit
   rights.

### Proposed two-week experiment

Keep the POC off the live deployment path and out of required PR checks.

**System under test.** One daemon container, one listener container, one
counterparty simulator, and explicit durable volumes. Pin every image by digest
and record the resolved Compose configuration so setup validation and the run
refer to the same artifact.

**Workload.** Generate valid and invalid signals across session boundaries while
the simulator independently selects accept/reject/delay/drop-response behavior.
Never send an order to a real endpoint.

**Initial properties.** Use stable identifiers/messages so history is not split
when wording changes:

- `FP-AT-001`: no live or non-simulated endpoint is reachable;
- `FP-AT-002`: emission disabled implies zero outbound order intents;
- `FP-AT-003`: one logical signal produces at most one permitted downstream
  acceptance;
- `FP-AT-004`: ambiguous acknowledgement never causes an unsafe automatic retry;
- `FP-AT-005`: durable disarm/stop state survives any tested restart sequence;
- `FP-AT-006`: there is never more than one effective owner of each durable
  writer role;
- `FP-AT-007`: peak-equity and protective state never regress after recovery;
- `FP-AT-008`: stale, malformed, wrong-contract, or out-of-session input never
  reaches acceptance;
- `FP-AT-009`: after faults stop, the system reaches a safe quiescent state;
- `FP-AT-010`: the workload demonstrably reaches every planned outcome class.

**Acceptance bar.** Adopt only if the trial (a) reproduces the planted/historical
defect, (b) yields a deterministic replay that materially shortens diagnosis,
(c) finds at least one non-trivial actionable defect or demonstrates materially
better schedule coverage than the local fault suite, (d) reruns the fix without
the property failure, and (e) has an acceptable annualized price and maintenance
burden. Reject or defer if setup/model maintenance dominates, results merely
repeat ordinary integration tests, or counterparty realism cannot be achieved.

## Lower-cost work that should come first

1. Build the same hermetic Compose topology and simulator locally; it is a
   prerequisite for Antithesis and useful even if procurement stops.
2. Add deterministic integration cases for request accepted/response lost,
   duplicate delivery, process death between persistence and send, corrupt or
   partial state, and simultaneous startup.
3. Add clock/session-boundary cases with an injected clock rather than relying on
   wall time.
4. Run ordinary fault scripts against the topology and record which schedules
   remain difficult to reproduce. Those gaps become the POC's value baseline.
5. Reassess once the rail is unattended or has multiple independently failing
   components. That is when deterministic simulation has a stronger opportunity
   cost advantage over conventional tests.

## Due-diligence questions for Antithesis

- What is the full price and minimum commitment, and how do Standard/Fast/Turbo
  tiers translate into billable core hours for a three-container Python system?
- Can a POC and paid tenant be pinned to a region, and what are the exact image,
  log, report, replay-artifact, backup, and deletion retention terms?
- Which isolation/security attestations and customer-managed access controls are
  available? The public security page alone is not a substitute for contract
  review.
- Can all findings, property results, logs, and minimal reproductions be exported
  through supported APIs so repository evidence is not vendor-locked?
- Which fault types require a forward-deployed engineer, which are self-service,
  and which Python/thread behaviors can actually be instrumented?
- How should a two-node logical system deployed as separate Fly applications be
  represented so container, volume, DNS, restart, and network semantics remain
  honest?
- What support is included for building a stateful counterparty simulator and
  validating that its failure model is not misleading?

## Sources and confidence

Sources were accessed 2026-09-17. Product-capability and prerequisite claims are
from Antithesis's own current documentation; they are vendor claims, not an
independent performance benchmark. Repository-fit conclusions are reasoned from
the checked-in deployment and runtime sources. No Antithesis trial was run, no
quote was obtained, and no claim is made about defect-finding yield or financial
ROI.

- [How Antithesis works](https://antithesis.com/docs/introduction/how_antithesis_works/)
- [Prerequisites](https://antithesis.com/docs/faq/prerequisites/)
- [About Standard POCs](https://antithesis.com/docs/faq/poc_faq/)
- [Setup overview and hermetic dependencies](https://antithesis.com/docs/setup/overview/)
- [Docker Compose setup](https://antithesis.com/docs/setup/docker_compose/)
- [Docker Compose best practices](https://antithesis.com/docs/best_practices/docker_best_practices/)
- [Handling external dependencies](https://antithesis.com/docs/reference/dependencies/)
- [Launching tests](https://antithesis.com/docs/product/launching_tests/)
- [Python SDK](https://antithesis.com/docs/reference/sdk/python/)
- [Assertions](https://antithesis.com/docs/product/writing_tests/assertions/)
- [Fault types](https://antithesis.com/docs/product/writing_tests/controlling_faults/fault_types/)
- [Customer FAQ](https://antithesis.com/docs/faq/customer_faq/)
- [First Passage architecture map](../../../REPO_MAP.md)
- [Listener deployment posture](../../../deploy/c1_rail/README.md)
- [Signal-daemon deployment posture](../../../deploy/c1_signal_daemon/README.md)
- [Signal payload idempotency note](../../../ops/c1_signal_daemon/b1_payload.py)
