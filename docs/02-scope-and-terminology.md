# 02 — Scope and terminology

**Status:** project convention; not an industry standard.  
**Last reviewed:** 2026-10-25.

## Purpose

Shed-Z documents a safe, evidence-gated way to keep agent work available on an always-on host and operate it remotely. The project separates persistent compute from agent sessions, policy enforcement, durable task state, tool access, model inference and the evidence needed to verify outcomes.

The phrase **AI shed** was used by David Heinemeier Hansson on 4 October 2026 for “an always-on machine running on their tailscale network where the majority of their herdr agents are running.” The quote is recorded in the source register as S1 and cross-checked against secondary records S2–S3. It is a practitioner description, not a formal standard or complete reference architecture.

## Scope

In scope:

- A private, always-on host or isolated VM for long-running agent sessions and jobs.
- Remote operator access with explicit device and service permissions.
- A controlled intake path from request to task classification, authorization, execution, verification and evidence.
- Session continuity plus separate durable state where work must survive worker or host failure.
- Sandboxed workers, scoped tools and credentials, action-bound approvals, audit records, cost/resource bounds and tested recovery.
- A staged evaluation of hosted, local and hybrid model inference against real workload requirements.
- Documentation, configuration fingerprints, reproducible tests and explicit residual-risk tracking.

## Non-goals

Shed-Z does not assume or promise:

- That a local language model is required.
- That a terminal or session manager is a durable scheduler, authorization engine, or security sandbox.
- That “private network” means every service or agent action is authorized.
- That a model's assertion of completion proves success.
- An unrestricted personal assistant with access to personal email, browser sessions, password stores, financial accounts or all repositories.
- Exactly-once external side effects where the external system does not provide suitable idempotency or reconciliation.
- Production readiness before the applicable tests, recovery drills and approvals pass.
- A specific vendor, model, host, database, agent framework or user interface before evidence supports the choice.

## Terminology

| Term | Meaning in this repository |
|---|---|
| AI shed | The deployment pattern: an always-on, privately reachable host used to keep agent work available beyond an active client session. |
| Host | The physical machine or virtual machine that runs the selected services. |
| Control surface | The operator-facing entry point for task submission, status, approval and stop controls. It is not a raw privileged shell. |
| Agent runtime | Software that runs the model/tool loop and manages agent-specific state. |
| Session manager | Software that preserves and exposes terminal/workspace sessions; Herdr is a candidate, not a selected dependency. |
| Durable task | A work item whose intent, ownership, state transitions, side-effect receipts and recovery status are persisted outside the worker/session process. |
| Worker | The isolated execution environment that receives bounded tasks. |
| Tool | A narrowly defined operation such as reading a repository, running tests, creating a branch, or calling an API. |
| Approval | A human authorization record bound to the exact proposed action, arguments, target, risk and validity period. |
| Evidence receipt | A traceable record or artifact that supports a claim about execution or outcome. |
| Recovery | A defined procedure to resume, reconcile, cancel, revoke or rebuild after interruption or compromise. |
| Tailnet | The private Tailscale network joining authorized devices; network reachability is only one security layer. |
| Add-on | A separately scoped capability such as a scheduler, browser automation, inbox connector, notification path or model router. |

## Claim-status vocabulary

Use these labels in research, ADRs and reports:

- **FACT:** directly supported by primary or otherwise reliable evidence within a stated scope.
- **ESTABLISHED:** documented behavior or converging high-quality evidence; re-check version-dependent behavior before relying on it.
- **EXPERIMENTALLY_SUPPORTED:** reproduced under the stated setup and recorded with artifacts.
- **USER_REPORTED:** reported by the project owner but not independently verified.
- **INFERENCE:** a reasoned interpretation that is not itself directly proved.
- **HYPOTHESIS:** a testable proposal awaiting evidence.
- **CONTRADICTED:** evidence conflicts with the claim in the stated scope.
- **UNKNOWN / OPEN:** evidence is insufficient or the decision remains unresolved.

Repeated discussion does not upgrade a claim's status. Record evidence, scope, date, uncertainty and the next validation step.

## Decision rule

When a feature or component is attractive but unproven, record it as a candidate and define the test that would justify adopting it. Do not treat diagrams, plans, README wording or successful model output as proof of an implementation.
