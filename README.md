# Shed-Z

Shed-Z is an evidence-gated foundation for an always-on, privately reachable agent host.

**Current status:** foundation only. The architecture is proposed, the components are not yet selected or deployed, and nothing here should be treated as production-ready.

## What this repository contains

- Research findings, source register and claim-status vocabulary
- Scope, terminology and explicit non-goals
- Reference architecture and component boundaries
- Threat model and required controls
- Operating model and task lifecycle
- Observability, verification levels and validation plan
- Initial architecture decision records
- Evidence-gated implementation roadmap and production-readiness checklist
- Agent-role roster and stateful service boundaries
- Durable state model for safe recovery
- Secure instruction-governance strategy
- Add-on feature catalog and specifications
- Machine-independent preconfiguration, fail-closed action policy and disabled job catalog
- Offline preconfiguration validator, regression tests and documentation validation CI

## Core logic in one sentence

Remote access leads to a policy gate, then a durable task store and scheduler, then an isolated worker, then a session manager (Herdr as a candidate), then the agent runtime, tools, model inference, external systems, and audit/backup.

## Availability-first preparation

The available resources are the centre of gravity. Use verified existing capabilities first; do not assume new hardware, a paid VM, a local model, a new scheduler or extra subscriptions are required. The preparation package is:

- `docs/16-workload-inventory.md` — candidate jobs and acceptance criteria
- `docs/17-available-resource-inventory.md` — observed resources, user-reported constraints and unknowns
- `docs/18-cost-and-capacity-model.md` — cost formulae, capacity caps and budget approval record
- `docs/19-preconfiguration.md` — configuration contract, safe defaults and later host-binding steps
- `docs/20-host-arrival-runbook.md` — ordered checks for the first available computer
- `config/` — deployment-disabled configuration and action-policy/job templates

These files prepare the decision; they do not claim the target host, private network, provider entitlements or budget are verified. Phase 0 remains open until those facts and the first jobs are confirmed.

## Project control plane

The repository defines the proposed control plane across:
- `docs/05-operating-model.md` — task lifecycle, authorization and failure handling
- `docs/06-observability-and-validation.md` — metrics, verification levels and evidence requirements
- `docs/07-decision-records.md` — accepted design boundaries and open architecture choices
- `docs/11-agent-roster.md` — control roles, coding roles and stateful services
- `docs/12-durable-state-model.md` — durable records and immutability rules
- `docs/13-instruction-governance.md` — secure, evolving instruction strategy
- `docs/14-addon-features.md` — add-on feature catalog
- `docs/15-addon-specifications.md` — minimum behavior and evidence expectations

These are specifications and role contracts, not claims that separate agents or services have been deployed.

## Reading order

1. `docs/01-research-findings.md`
2. `docs/02-scope-and-terminology.md`
3. `docs/09-source-register.md`
4. `docs/03-reference-architecture.md`
5. `docs/04-threat-model.md`
6. `docs/05-operating-model.md`
7. `docs/06-observability-and-validation.md`
8. `docs/07-decision-records.md`
9. `docs/16-workload-inventory.md`
10. `docs/17-available-resource-inventory.md`
11. `docs/18-cost-and-capacity-model.md`
12. `docs/19-preconfiguration.md`
13. `docs/11-agent-roster.md`
14. `docs/12-durable-state-model.md`
15. `docs/13-instruction-governance.md`
16. `docs/14-addon-features.md`
17. `docs/15-addon-specifications.md`
18. `docs/08-roadmap.md`
19. `docs/10-production-readiness.md`

## Validate documentation

Run `python scripts/check_docs.py`, `python scripts/validate_preconfiguration.py` and `python -m unittest discover -s tests -v` locally. GitHub Actions runs these checks on pull requests and pushes to `main`. These checks validate local Markdown links, research source IDs and configuration safety defaults. They do not validate external URLs, prove technical claims, or test a deployed runtime.

## Safety posture

- Least privilege and private-only access
- Explicit approvals for high-impact actions
- Durable records for decisions, approvals, and evidence
- Tested recovery before unattended use
- No production-readiness claims without task-specific evidence

## Repo policy

This repository is documentation-first. Implementation work should not begin until the evidence gates in the roadmap and checklist are satisfied.
