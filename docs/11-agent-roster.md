# 11 — Agent roster

This repository defines a full project roster so the system can be extended without blurring boundaries.

## Core control agents

| Agent | Purpose | Boundary |
|---|---|---|
| Coordinator | Turns the foundation into an ordered work plan and routes questions to specialists. | Does not decide architecture or safety on its own. |
| Architecture Steward | Checks component boundaries, roadmap logic, and design consistency. | Does not approve unsafe actions or publish changes by itself. |
| Security Gatekeeper | Reviews threats, evidence gates, approvals, and residual risk. | Does not implement features or weaken controls. |
| Repository Packager | Shapes the repository, reading order, and publication structure. | Does not overrule architecture or security decisions. |

## Coding and execution agents

| Agent | Purpose | Boundary |
|---|---|---|
| Implementation Engineer | Builds project code against approved specs and tasks. | Must not redefine architecture or security policy. |
| Integration / Tooling Engineer | Builds CI, automation, adapters, and environment glue. | Follows existing policy and repo conventions. |
| Test / Verification Engineer | Creates tests, smoke checks, drills, and reproducibility checks. | Reports evidence; does not decide design intent. |
| Documentation / ADR Curator | Maintains docs, runbooks, ADRs, and decision history. | Documents decisions; does not silently change them. |
| Research / Evidence Analyst | Collects source material, citations, and supporting evidence. | Provides evidence only; does not convert it into policy. |

## Stateful services

These are not reasoning roles. They hold durable state the agents rely on.

| Service | Purpose | Boundary |
|---|---|---|
| Policy Registry | Stores the active instruction set, version map, and compatibility rules. | Versioned and auditable; not a reasoning layer. |
| Evidence Ledger | Stores approvals, receipts, test artifacts, and citations. | Append-only; not a decision-maker. |
| Durable Task Store | Tracks tasks, transitions, ownership, and recovery state. | Must persist outside the session layer. |
| Herdr Session Layer | Preserves interactive workspaces and session continuity. | Useful for continuity, not a durability or security boundary. |

## Roster rules

- One role owns one primary concern.
- No role should combine policy authority and unrestricted execution.
- Builders can act only within approved scope.
- Every consequential action needs a durable record.
- Session continuity is helpful, but durable state lives elsewhere.

## System view

The full system is intended to behave like this:

**plan → review → approve → execute → verify → record → recover**

If a step cannot be recorded, verified, or recovered, it does not belong in unattended operation.
