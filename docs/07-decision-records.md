# 07 — Architecture decision records

**Purpose:** preserve why a decision was made, which evidence supports it, and what would trigger reconsideration. Decisions about implementation remain open until the required evidence exists.

## Decision register

| ID | Subject | Status | Decision / current position |
|---|---|---|---|
| ADR-0001 | Documentation-first, evidence-gated development | **Accepted** | The repository is a foundation only. Runtime selection and unattended execution wait for a workload inventory, risk classification and explicit phase exit criteria. |
| ADR-0002 | Herdr's role | **Accepted as a boundary; product choice open** | Herdr may be used as a session/interaction layer. It is not assumed to provide durable task queue semantics, action authorization or exactly-once external effects. |
| ADR-0003 | Model inference location | **Open** | Hosted, local and hybrid inference remain candidates. Choose only after representative workload quality, privacy, latency, cost and hardware measurements. |
| ADR-0004 | Physical host vs cloud VM | **Open** | Neither is selected. Compare availability, remote access, local hardware, recovery, privacy and recurring cost for the actual task set. |
| ADR-0005 | Policy enforcement boundary | **Accepted as a design requirement** | DENY, APPROVAL_REQUIRED and ALLOW must be enforced outside model-generated instructions. High-impact approval must bind to exact action parameters and target. |
| ADR-0006 | Durable state vs session state | **Accepted as a design requirement** | Task intent, state transitions, approvals, evidence and recovery cursors must be persisted outside the session manager. Process continuity alone is not durable task recovery. |
| ADR-0007 | Production-readiness claim | **Accepted** | Production readiness may be claimed only for tested task classes, configuration and versions that pass the checklist and retain evidence. Plans and documentation do not count as deployment proof. |
| ADR-0008 | Add-on architecture | **Proposed** | Keep scheduler, task journal, approvals, audit, recovery, model routing and connectors as explicit modules with contracts. Do not implement all add-ons before the first workload demonstrates need. |

“Accepted as a design requirement” records a boundary for future implementation; it does not claim the control is implemented. The status of a product choice may remain open even when the desired boundary is accepted.

## What evidence can change a decision?

- New first-party documentation or a security advisory that affects a dependency.
- A reproducible test that contradicts an assumed behavior.
- Representative workload measurements showing a material difference in quality, latency, cost or interventions.
- A threat-model update showing an existing boundary is insufficient.
- A recovery or failure-injection result that demonstrates unexpected side effects.
- A maintenance, licensing or access constraint that makes a candidate impractical.

Repeated discussion, product popularity or a successful demonstration alone is not enough to upgrade a claim.

## ADR lifecycle

Use Proposed → Accepted, Rejected, or Superseded. A superseding record links to the prior ADR. Accepted records are not silently edited to change rationale; append a dated correction or create a new ADR. Include status, owner, date, context, options, evidence, consequences, risks, verification and reconsideration triggers.

## Reusable ADR template

Copy this template into a new file under docs/adr/ or append a new record to this register.

- **ID and title:**
- **Status:** Proposed / Accepted / Rejected / Superseded
- **Date / owner:**
- **Context and problem:**
- **Constraints and non-goals:**
- **Options considered:**
- **Evidence and claim statuses:**
- **Decision and rationale:**
- **Security, privacy and operational consequences:**
- **Acceptance tests / revalidation:**
- **Reconsideration triggers:**
- **Supersedes / superseded by:**

## Open decisions blocking implementation

The immediate evidence gaps are the supported first workloads, impact classes, host/network constraints, resource and cost ceiling, and quantitative acceptance thresholds. These are Phase 0 exit criteria in [08-roadmap.md](08-roadmap.md), not choices to infer from the AI-shed label.
