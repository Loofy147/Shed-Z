# Production-readiness checklist

This checklist is a gate, not a progress decoration. A checked item requires retained evidence.

## Scope and authority
- [ ] Supported task classes and explicit non-goals are documented.
- [ ] Each tool/action has a declared resource scope and `DENY`, `APPROVAL_REQUIRED` or `ALLOW` policy.
- [ ] Approval is bound to exact action arguments and target.
- [ ] High-impact actions cannot be self-approved by the agent.

## Host and network
- [ ] Dedicated host/VM and non-admin service identity are in place.
- [ ] Operator personal files, browser sessions and password stores are inaccessible by default.
- [ ] Remote access is private-only and tailnet/device policies are tested.
- [ ] No unintended public ports/tunnels are reachable.
- [ ] OS, runtime, tools and extensions are pinned/inventoried.

## Task durability
- [ ] Task state persists outside the worker process.
- [ ] Timeout, cancellation, retry, deduplication and unknown-side-effect behavior are defined and tested.
- [ ] Agent/session status is not treated as a quality check.
- [ ] Every task has acceptance checks and an independent evidence artifact.

## Security
- [ ] Prompt-injection fixture is blocked from expanding tool authority.
- [ ] Cross-project filesystem access tests pass.
- [ ] Secret-canary and egress tests pass.
- [ ] Unreviewed extensions/MCP servers are blocked.
- [ ] Independent audit records cannot be modified by the worker.
- [ ] Revocation, stop-all and rebuild procedures have been exercised.

## Operations
- [ ] Cost, wall-clock, concurrency, memory and disk limits have tested behavior.
- [ ] Alerts cover failures, timeouts, budget exhaustion, host outage and unexpected configuration changes.
- [ ] Backup restoration has been tested on a clean environment.
- [ ] Upgrade/rollback tests pass after runtime/configuration changes.
- [ ] Incident runbook and task-owner escalation path exist.

## Evidence bundle
- [ ] Environment and configuration fingerprints recorded.
- [ ] Test commands, outcomes, logs and artifacts are retained and redacted.
- [ ] Failed/inconclusive tests are listed rather than omitted.
- [ ] Residual risks and approved exceptions are documented.
- [ ] An independent reviewer signs the release decision.
