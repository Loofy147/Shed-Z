# 05 — Operating model

**Status:** proposed operating contract; not implemented or deployed.

## Operating principle

Every task must pass through a controlled lifecycle. The agent can propose actions and produce artifacts, but it cannot rewrite the system's policy or approve its own high-impact actions. Durable records—not the prompt, chat transcript or terminal session—are the authority for task state, policy version and approval outcomes.

## Task lifecycle

1. **Receive:** assign a unique task ID and preserve the original request and source.
2. **Classify:** identify task class, target resources, data sensitivity, potential external effects, reversibility, cost ceiling and acceptance criteria.
3. **Authorize:** evaluate each requested tool/action as **DENY**, **APPROVAL_REQUIRED** or **ALLOW**. Reject requests outside the supported scope.
4. **Queue and claim:** persist policy version, task owner, deadlines, resource limits and claim/lease information before execution.
5. **Execute:** run in a worker with a narrow filesystem, identity, tool set and network egress policy. Session state is only a convenience.
6. **Verify:** run predefined deterministic checks and obtain independent evidence appropriate to the task's impact.
7. **Record:** persist results, diffs, action receipts, errors, model/runtime versions, costs and evidence links; redact secrets.
8. **Close or recover:** mark the task successful only when acceptance evidence passes. Otherwise fail, block, cancel or enter manual recovery.

## Canonical task states

| State | Meaning | Allowed transition examples |
|---|---|---|
| RECEIVED | Request durably recorded; not yet classified. | CLASSIFYING, REJECTED |
| CLASSIFYING | Task class, scope and impact are being determined. | AWAITING_APPROVAL, QUEUED, REJECTED |
| AWAITING_APPROVAL | A specific action needs human authorization. | QUEUED, REJECTED, CANCELLED, EXPIRED |
| QUEUED | Authorized and eligible for a worker claim. | RUNNING, CANCELLED, EXPIRED |
| RUNNING | Worker execution is active. | VERIFYING, BLOCKED, CANCEL_REQUESTED, FAILED, RECOVERY_REQUIRED |
| VERIFYING | Acceptance checks and evidence collection are running. | SUCCEEDED, FAILED, BLOCKED, RECOVERY_REQUIRED |
| BLOCKED | Needs input, approval or a dependency before safe continuation. | A policy-checked return to QUEUED, or CANCELLED |
| CANCEL_REQUESTED | Cancellation requested; external effects may still be in flight. | CANCELLED, RECOVERY_REQUIRED, SUCCEEDED if outcome proves committed |
| CANCELLED | Stopped and reconciled to the extent possible. | Terminal unless a new task is created |
| SUCCEEDED | Acceptance checks passed and evidence was stored. | Terminal; corrections use a new task/version |
| FAILED | Task failed and no safe automatic recovery is permitted. | Terminal; retry requires an explicit new attempt record |
| RECOVERY_REQUIRED | Side effects or state are uncertain; stop automatic retries. | Human or reconciler resolves to an evidence-backed outcome |
| REJECTED / EXPIRED | Policy declined the task or approval/lease expired. | Terminal; a new request may be submitted |

The implementation may use a smaller internal set, but it must preserve these distinctions in its observable records. Never map a timeout or lost acknowledgement to success by assumption.

## Action authorization contract

Each action request should carry at least:

- task and action IDs;
- actor/runtime identity and active policy version;
- tool name, normalized arguments and exact resource target;
- data classification and expected external effects;
- requested permission state, deadline and budget;
- an idempotency key or an explicit statement that the action is not safely repeatable;
- approval record, if required.

Approval must bind to the action's normalized arguments and target. Any material change invalidates the approval. Approval expires and cannot be reused to authorize a different action. The agent itself cannot mint or satisfy its own approval.

Use the least authority that achieves the task. Start with **DENY** for unknown tools, unknown network destinations and high-impact writes. **ALLOW** is limited to a documented scope and quota. **APPROVAL_REQUIRED** pauses before the external side effect, not after it.

## Roles and separation of duties

The roster in [11-agent-roster.md](11-agent-roster.md) defines responsibilities. A role is a contract, not a requirement to launch a separate autonomous model instance. Multiple roles can initially be implemented as human review steps, deterministic services or instructions executed by one constrained worker.

- **Coordinator:** decomposes approved work; cannot weaken policy.
- **Architecture steward:** checks boundary and design consistency; cannot grant unsafe permissions.
- **Security gatekeeper:** challenges risks and control evidence; cannot waive controls unilaterally.
- **Implementation engineer:** changes code only within an approved task and repository scope.
- **Verification engineer:** records independent test outcomes and counter-evidence.
- **Evidence analyst / documentation curator:** maintain sources, artifacts, claims and decisions; do not silently turn hypotheses into facts.
- **Stateful services:** hold policy versions, tasks, approvals and evidence but do not make unreviewable decisions.

For consequential tasks, the same actor should not both propose and approve the risky action. Independence can be limited by budget and staffing; disclose the limitation and increase deterministic verification accordingly.

## Operational modes

- **Read-only:** repository/file inspection and bounded analysis; no external state change.
- **Sandboxed write:** changes limited to an isolated worktree or temporary workspace; no production credentials.
- **Review required:** agent prepares a diff or action plan; a human approves the exact resulting action.
- **Unattended bounded job:** only a pre-approved job class with explicit resource, network, time and impact boundaries.
- **Stop / incident mode:** stop new claims, revoke relevant credentials/access, preserve logs, and reconcile actions whose effects are uncertain.

Unattended mode is a property of a specific task class and configuration, not a global switch that makes arbitrary prompts safe.

## Retry, cancellation and partial effects

- Retry only failures whose classification permits it.
- Use idempotency keys where supported and save external receipts.
- After a request timeout, query the external system before repeating a potentially non-idempotent action.
- Cancellation prevents new work where possible; it does not prove an in-flight side effect was rolled back.
- If an action may have committed but its receipt is missing, enter RECOVERY_REQUIRED and reconcile before retry.
- Keep the original failed attempt and evidence. Do not overwrite failure with a later success; link attempts under one logical task.
- Provide a stop control outside the agent runtime and test it independently.

## Minimum run record

Persist task ID, initiating identity, timestamps, classification, policy version, approval IDs, selected model/runtime and versions, worker identity, tool calls, exit status, test results, cost/resource usage, artifact digests, external receipts, redacted logs and final disposition. Do not store raw secrets or unrestricted private content merely because it is useful for debugging.
