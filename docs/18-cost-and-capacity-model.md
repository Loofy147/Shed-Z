# 18 — Cost and capacity model

**Status:** measurement framework; no spend ceiling, provider, host or usage price has been approved.  
**As of:** 2026-10-25.

## Rule before spending

The available resources are the centre of gravity. Reuse existing permitted capabilities first and measure representative work before adding infrastructure.

**Current authorization:** incremental paid spend is NOT APPROVED because the owner has not recorded a hard budget ceiling in this repository. This does not mean existing services are free or unlimited. Verify current plan terms, quotas and prices before enabling any metered service.

Do not provision a new VM, buy hardware, enable a paid model/API, add a subscription or switch on recurring execution just to advance the roadmap. A proposed spend must state the purpose, ceiling, expected usage, stop condition and cheaper alternatives.

## Cost categories

| Cost category | What to measure | Possible billing/operating risk | Control |
|---|---|---|---|
| Host hardware | One-time purchase, replacement, expected useful life | Unnecessary capital cost before job fit is known | No purchase until a benchmark shows a clear need |
| Cloud VM / storage | Hourly/monthly compute, disks, snapshots, egress and idle time | Recurring spend when no tasks run | Explicit budget, automatic stop where safe, alerts and owner-visible billing |
| Model inference | Input/output tokens, cached tokens, calls and model-specific price | Long context, retry loops and parallel agents multiply usage | Per-task token/cost cap, retry limit, model allowlist and global monthly cap |
| Hosted services | Workflow minutes, artifact storage, data transfer, API calls and plan limits | Free-tier assumptions may expire or be exceeded | Verify current terms and quota before relying on them |
| Network / remote access | Plan limits, relay/egress needs, DNS and certificate requirements | Hidden dependency on plan features or public exposure | Private-only design, plan/feature verification and explicit network policy |
| Local inference | Hardware purchase or depreciation, electricity, cooling, model storage and maintenance | Slow/low-quality results or resource contention | Benchmark end-to-end quality, latency, memory and power before selection |
| Operations | Updates, backups, monitoring, recovery time, incident response | Human time may exceed compute cost | Track intervention time and failure/repair effort |
| External effects | Messages, API operations, deployment, cloud resources or purchases | Duplicate actions, unauthorized spend or irreversible changes | Action-bound approval, idempotency/reconciliation and separate limits |

## Measurement formulae

For a reporting interval:

- **Incremental monthly cost** = metered host + storage/egress + model/API use + additional subscriptions + other attributable service charges.
- **Cost per verified successful job** = incremental cost attributed to the job set / number of jobs passing the predefined acceptance checks.
- **Total operating cost** = incremental cash cost + recorded operator/maintenance time, reported separately if time cannot be credibly priced.
- **Cost variance** = actual cost minus preregistered expected cost; investigate positive variance above the approved tolerance.

Never count failed jobs as successful merely because they consumed less, and do not hide retried or human-repaired runs from the denominator.

## Capacity and quota controls

Each enabled job class must declare:

- maximum concurrent tasks and agents;
- per-task wall-clock timeout and global stop behavior;
- memory, CPU, disk and process limits appropriate to its isolation boundary;
- model/provider and allowed model-routing choices;
- per-task token or monetary ceiling where provider cost is metered;
- retry count and eligible retry categories;
- network destination allowlist and expected data egress;
- maximum artifact/log retention and redaction rules;
- response to provider, host, queue or audit-sink outage.

A task that reaches its cap should stop safely and record a budget-exhausted or recovery-required state. It must not silently switch to a more expensive model or less restricted execution path.

## Budget approval record

Complete before enabling any incremental paid or recurring resource.

| Field | Required value |
|---|---|
| Approval ID / owner / date | OPEN |
| Workload(s) being enabled | OPEN |
| Approved incremental monthly ceiling and currency | OPEN |
| One-time purchase ceiling, if applicable | OPEN |
| Expected usage and pricing source/date | OPEN |
| Worst-case monthly spend estimate | OPEN |
| Alert threshold and hard-stop threshold | OPEN |
| Existing/cheaper alternative evaluated | OPEN |
| Data-location and privacy implications | OPEN |
| Renewal/cancellation owner | OPEN |
| Conditions to stop or revisit | OPEN |

The hard stop must be lower than or equal to the owner's explicitly approved ceiling. If the provider cannot enforce a hard stop, document the residual risk and require a smaller exposure or manual approval before use.

## Benchmark before selection

Use the same preregistered job set for every option. Capture verified success, completion latency, intervention rate, token/compute usage, cost per verified success, quality defects and recovery behavior.

Compare at least:

1. Current permitted tools and existing CI with no new infrastructure.
2. Existing computer used as an isolated host, only after its specifications and security posture are verified.
3. A cloud VM or hosted runner, only after its full recurring cost and access model are known.
4. Local inference only if the available hardware is confirmed and the workload benchmark is meaningful.

Do not compare raw token price or model latency alone. Include human repair, waiting, failures, data-handling requirements and ongoing maintenance.

## Current unresolved items

- The owner-approved monthly and one-time spend ceilings are OPEN.
- Host specs and uptime are not independently verified.
- Provider accounts, quotas, prices and data terms have not been selected or checked for a specific workload.
- No local-versus-hosted benchmark has been run.
- Therefore no specific host/model configuration is recommended yet.
