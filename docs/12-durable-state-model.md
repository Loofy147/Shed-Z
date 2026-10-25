# 12 — Durable state model

The system needs durable state for safety, replay, and recovery. Anything that affects authority, execution, verification, or audit must live outside the agent prompt/session.

## Minimum durable state objects

### 1) Project manifest / policy baseline
Purpose: the authoritative operating frame for Shed-Z.

**High-level fields**
- `project_id`
- `schema_version`
- `operating_mode`
- `policy_version`
- `allowed_actions`
- `tool_allowlist`
- `tool_denylist`
- `egress_limits`
- `isolation_requirements`
- `evidence_requirements`
- `retention_class`
- `created_at`, `updated_at`

**Rule**
- Versioned only; never silently edited in place.

### 2) Task / work-item record
Purpose: track the ordered work plan and its current status.

**High-level fields**
- `task_id`
- `title`
- `description`
- `dependencies`
- `status`
- `priority`
- `owner`
- `originating_request`
- `acceptance_criteria`
- `linked_decisions`
- `linked_evidence`
- `created_at`, `updated_at`, `closed_at`

**Rule**
- Keep task history append-only; derive the current view from history plus snapshot.

### 3) Decision / ADR record
Purpose: preserve explicit choices and keep open decisions separate from facts.

**High-level fields**
- `decision_id`
- `subject`
- `context`
- `options_considered`
- `chosen_option`
- `rationale`
- `evidence_refs`
- `status`
- `supersedes_decision_id`
- `decided_by`
- `decided_at`

**Rule**
- Immutable once accepted; corrections happen through a superseding record.

### 4) Approval record
Purpose: bind approvals to exact actions and consequences.

**High-level fields**
- `approval_id`
- `action_id` or `task_id`
- `scope_of_approval`
- `risk_level`
- `approver`
- `approval_result`
- `conditions`
- `valid_until`
- `evidence_refs`
- `created_at`

**Rule**
- Signed approvals are immutable.

### 5) Evidence receipt / artifact ledger
Purpose: prove that something happened, not merely that it was claimed.

**High-level fields**
- `evidence_id`
- `evidence_type`
- `source_system`
- `tool_name`
- `input_hash`
- `output_hash`
- `artifact_uri`
- `content_digest`
- `linked_task_id`
- `linked_decision_id`
- `linked_approval_id`
- `captured_at`
- `captured_by`

**Rule**
- Append-only.

### 6) Audit event log
Purpose: provide tamper-evident history across the whole system.

**High-level fields**
- `event_id`
- `aggregate_type`
- `aggregate_id`
- `event_type`
- `actor`
- `timestamp`
- `payload_hash`
- `previous_event_hash`
- `correlation_id`
- `causation_id`

**Rule**
- Strictly append-only.

### 7) Recovery / checkpoint state
Purpose: allow restart, replay, and safe continuation after interruption.

**High-level fields**
- `checkpoint_id`
- `session_id` or `run_id`
- `last_committed_event_id`
- `last_safe_task_state`
- `last_verified_approval_id`
- `last_verified_evidence_id`
- `recovery_cursor`
- `created_at`
- `created_by`

**Rule**
- Checkpoints are immutable snapshots.

### 8) Risk / exception register
Purpose: surface residual risk explicitly.

**High-level fields**
- `risk_id`
- `description`
- `severity`
- `likelihood`
- `status`
- `mitigation`
- `acceptance_approval_id`
- `review_due_at`
- `linked_evidence_refs`
- `created_at`, `closed_at`

**Rule**
- Risk transitions should be append-only and tied to durable approval references.

## What must be immutable or append-only

At minimum:

- Audit log
- Evidence receipts
- Approvals
- Decision records
- Policy baseline versions
- Recovery checkpoints
- Task history

A safe rule is:
- current state may be mutable only as a derived view or cache
- source-of-truth records must be append-only or versioned

## What must never live only in the prompt/session

- Current task list and dependencies
- Open questions and unresolved decisions
- Policy allowlists and denylists
- Approval outcomes and approval conditions
- Evidence links and verification results
- Risk acceptances and exceptions
- Recovery cursor and last safe checkpoint
- Tool-use receipts and auditable outputs
- Ownership and accountability assignments
- Any destructive-action confirmation
- Any state required to resume without re-deriving from scratch

## Why this matters

Herdr can preserve a working session, but the architecture already treats it as a session layer, not a durability or security boundary. Anything that must survive restart, support audit, or enforce safety needs a durable record outside the session.
