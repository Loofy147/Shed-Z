# Shed-Z

Shed-Z is an evidence-gated foundation for an always-on, privately reachable agent host.

**Current status:** foundation only. The architecture is proposed, the components are not yet selected or deployed, and nothing here should be treated as production-ready.

## What this repository contains
- Research findings and claim status
- Source register and evidence trail
- Reference architecture and component boundaries
- Threat model and required controls
- Full agent roster and stateful services
- Durable state model for safe recovery
- Secure instruction-governance strategy
- Roadmap with evidence gates
- Production-readiness checklist

## Core logic in one sentence
Remote access leads to a policy gate, then a durable task store and scheduler, then an isolated worker, then a session manager (Herdr as a candidate), then the agent runtime, tools, model inference, external systems, and audit/backup.

## Project control plane
The repository now defines the full control plane for the project:
- `docs/11-agent-roster.md` — the control agents, coding agents, and stateful services
- `docs/12-durable-state-model.md` — the durable state objects and immutability rules
- `docs/13-instruction-governance.md` — the secure, evolving instruction strategy

## Reading order
1. `docs/01-research-findings.md`
2. `docs/09-source-register.md`
3. `docs/03-reference-architecture.md`
4. `docs/04-threat-model.md`
5. `docs/11-agent-roster.md`
6. `docs/12-durable-state-model.md`
7. `docs/13-instruction-governance.md`
8. `docs/08-roadmap.md`
9. `docs/10-production-readiness.md`

## Safety posture
- Least privilege and private-only access
- Explicit approvals for high-impact actions
- Durable records for decisions, approvals, and evidence
- Tested recovery before unattended use

## Repo policy
This repository is documentation-first. Implementation work should not begin until the evidence gates in the roadmap and checklist are satisfied.
