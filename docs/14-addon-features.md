# 14 — Add-on features

This section names the feature set that extends the foundation into a full system. Each feature stays separate from the others so the system can evolve without collapsing boundaries.

## Feature catalog

| Feature | Why it exists | Depends on current docs |
|---|---|---|
| Control surface | Gives the operator a narrow entry point for task intake, status, and approvals without exposing a raw shell. | `03-reference-architecture.md`, `04-threat-model.md`, `08-roadmap.md`, `10-production-readiness.md` |
| Task journal | Persists task intent, ownership, state transitions, deadlines, retries, and receipts outside the worker process. | `03-reference-architecture.md`, `01-research-findings.md`, `04-threat-model.md`, `08-roadmap.md` |
| Scheduler | Triggers scheduled or retryable jobs and keeps them independent from the session manager. | `03-reference-architecture.md`, `01-research-findings.md`, `08-roadmap.md` |
| Approvals | Binds human approval to exact action, arguments, and target for high-impact operations. | `03-reference-architecture.md`, `04-threat-model.md`, `08-roadmap.md`, `10-production-readiness.md` |
| Audit | Stores append-only evidence of policy decisions, state changes, tool actions, and receipts in a place the worker cannot edit. | `03-reference-architecture.md`, `04-threat-model.md`, `08-roadmap.md`, `10-production-readiness.md` |
| Recovery | Covers backup, restore, revoke, stop-all, and rebuild drills so recovery is tested rather than assumed. | `03-reference-architecture.md`, `04-threat-model.md`, `08-roadmap.md`, `10-production-readiness.md` |
| Model routing | Routes work to hosted, local, or hybrid inference based on task class, cost, and risk. | `03-reference-architecture.md`, `01-research-findings.md`, `08-roadmap.md` |
| Tool registry | Maintains the approved tool, MCP, and extension inventory, versions, and scopes. | `03-reference-architecture.md`, `04-threat-model.md`, `10-production-readiness.md` |
| Observability | Provides metrics, state visibility, costs, alerts, and receipts so “done” is evidence-backed. | `03-reference-architecture.md`, `08-roadmap.md`, `10-production-readiness.md` |
| Notifications | Emits operator-facing alerts for failures, timeouts, budget exhaustion, host outage, and unexpected configuration changes. | `08-roadmap.md`, `10-production-readiness.md` |
| Runbooks | Gives each supported job class an explicit operating and escalation path, including incident handling and recovery steps. | `08-roadmap.md`, `10-production-readiness.md` |

## Feature group boundaries

- Herdr/session layer vs. durable orchestration
- Control surface vs. worker execution
- Approvals vs. observability
- Audit vs. notifications
- Model routing vs. tool registry
- Recovery vs. normal task flow

## Operating rule

No feature should claim readiness until its corresponding evidence gate is satisfied and the required artifacts are retained.
