# Shed-Z

Shed-Z is an evidence-gated foundation for an always-on, privately reachable agent host.

**Current status:** foundation only. The architecture is proposed, the components are not yet selected or deployed, and nothing here should be treated as production-ready.

## What this repository contains
- Research findings and claim status
- Source register and evidence trail
- Reference architecture and component boundaries
- Threat model and required controls
- Roadmap with evidence gates
- Production-readiness checklist

## Core logic in one sentence
Remote access leads to a policy gate, then a durable task journal and scheduler, then an isolated worker, then a session manager (Herdr as a candidate), then the agent runtime, tools, model inference, external systems, and audit/backup.

## Reading order
1. `docs/01-research-findings.md`
2. `docs/09-source-register.md`
3. `docs/03-reference-architecture.md`
4. `docs/04-threat-model.md`
5. `docs/08-roadmap.md`
6. `docs/10-production-readiness.md`

## Safety posture
- Least privilege and private-only access
- Explicit approvals for high-impact actions
- Independent audit records
- Tested recovery before unattended use

## Repo policy
This repository is documentation-first. Implementation work should not begin until the evidence gates in the roadmap and checklist are satisfied.
