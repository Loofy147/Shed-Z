# 13 — Secure and evolving instruction governance

The project needs instructions that can change without becoming brittle, ambiguous, or unsafe.

## Instruction layers

Use a fixed precedence order:

1. System rules
2. Repository constitution
3. Role contract
4. Versioned policy pack
5. Task brief
6. Current evidence and artifacts

Lower layers must not silently override higher layers.

## Stable core

Keep a short, stable core that changes rarely:

- project principles
- evidence gate
- approval rules
- role boundaries
- conflict precedence
- recovery expectations

This core should be easy to read and hard to accidentally weaken.

## Versioned policy packs

Keep evolving guidance in versioned packs instead of ad hoc prompt edits.

Each pack should include:
- role contracts
- operating rules
- approval thresholds
- safety rules
- escalation rules
- deprecation notes
- compatibility notes

Suggested pattern:
- `policy/v1/`
- `policy/v1.1/`
- `policy/v2/`

## Change process

Any meaningful instruction change should go through:

1. Proposal
2. Evidence review
3. Architecture review
4. Security review
5. Merge
6. Changelog entry
7. Rollback path

That keeps instruction drift visible and auditable.

## Safety rules for instruction updates

Before activating a new instruction version:

- check for contradictions
- verify security-sensitive wording
- confirm the approval behavior still matches the policy
- smoke test the changed role behavior
- preserve the previous version for rollback

## Role contract rules

Each agent should have:
- one primary responsibility
- a clear escalation path
- no hidden authority
- no duplicated ownership of the same decision

## Session vs truth

A session can be useful, but it is not a source of truth.

- **Policy** says what should happen.
- **Evidence** says what was verified.
- **Session state** says what is currently underway.

Those three should stay separate.

## Herdr boundary

Herdr is useful as a session layer for continuity, but it is not the policy registry, the evidence ledger, or the durability boundary. The repository should say that clearly and keep the durable state elsewhere.
