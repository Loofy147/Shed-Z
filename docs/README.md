# Documentation index

This directory contains the Shed-Z foundation package. The documents describe a proposed system; they are not evidence that its runtime, controls or services have been implemented.

## Research and design

- `01-research-findings.md` — findings, claim statuses and limits of the initial investigation
- `02-scope-and-terminology.md` — definition, scope, non-goals and vocabulary
- `03-reference-architecture.md` — layered architecture and component boundaries
- `04-threat-model.md` — assets, trust boundaries, threats and required controls
- `05-operating-model.md` — task lifecycle, authorization, retry and recovery rules
- `06-observability-and-validation.md` — metrics, verification-independence scale and validation plan
- `07-decision-records.md` — initial ADR register and open architecture decisions
- `08-roadmap.md` — evidence-gated implementation plan
- `09-source-register.md` — sources, dates, uses, limitations and source-quality policy
- `10-production-readiness.md` — release gate and required evidence bundle

## System and feature contracts

- `11-agent-roster.md` — control roles, coding roles and stateful services
- `12-durable-state-model.md` — durable state objects and immutability rules
- `13-instruction-governance.md` — secure, versioned instruction strategy
- `14-addon-features.md` — add-on feature catalog
- `15-addon-specifications.md` — minimum behavior, non-goals and readiness evidence for add-ons

## Preparation and resource planning

- `16-workload-inventory.md` — candidate first jobs, impact classification and acceptance criteria
- `17-available-resource-inventory.md` — observed capabilities, user-reported constraints and unknowns
- `18-cost-and-capacity-model.md` — spending approval, benchmark approach, caps and cost formulas

## Preconfiguration

- `19-preconfiguration.md` — deployment-disabled configuration pack and host-binding gate
- `20-host-arrival-runbook.md` — ordered inspection, setup, security and acceptance gates when a computer becomes available
- `../config/preconfiguration.json` — host/network/runtime/model/budget placeholders
- `../config/action-policy.json` — deny-by-default action policy
- `../config/job-catalog.json` — candidate jobs, explicitly disabled by default
- `../scripts/validate_preconfiguration.py` — offline guardrail validation
- `../tests/test_preconfiguration.py` — regression tests for unsafe promotion, policy weakening, early job enablement, public ingress and secret-value detection

## Reading order

Start with 01 and 02, then 09, 03 and 04. Read 05–07 for operating, measurement and decision contracts; then 11–15 for system boundaries and feature specs. Use 16–18 to prepare the first pilot, 08 to sequence work and 10 as the release gate.

## Validation

From the repository root, run `python scripts/check_docs.py`, `python scripts/validate_preconfiguration.py` and `python -m unittest discover -s tests -v`. The first checks local Markdown links and research source IDs. The second checks configuration integrity and safe preconfiguration defaults. Neither verifies external URLs, proves research claims, or tests a deployed runtime.

## Status

All architecture and add-on descriptions are proposed specifications until their implementation and required verification artifacts exist. Keep documented findings, decisions, tests and deployment claims separate.


Phase 0 is still open until the owner confirms representative jobs, the intended host/network facts, a spending ceiling and measurable acceptance criteria.
