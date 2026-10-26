# 20 — Host-arrival runbook

**Status:** prepared for future use. No computer is currently available for Shed-Z use.  
**Rule:** do not execute host installation steps until the target machine, owner authority and operating system are confirmed.

## Purpose

This runbook makes the first setup repeatable while leaving operating-system-specific commands until the actual host is known. It is not permission to provision a cloud VM, buy hardware, create a subscription, expose a port or install an agent.

## Gate 0 — Verify authority and availability

- [ ] Identify the actual machine and confirm the owner has authority to configure it.
- [ ] Record whether it is an existing physical computer, an isolated VM or a cloud VM.
- [ ] Confirm it may remain powered on for the intended schedule and can be securely rebooted.
- [ ] Confirm a recovery path exists that does not depend on the agent.
- [ ] Record owner-approved one-time and monthly spending ceilings, including zero if that is the decision.
- [ ] Do not copy personal files, browser profiles, password stores or unrelated credentials into the worker environment.

**Stop condition:** if the machine, authority, recovery access or budget approval is ambiguous, remain in preparation mode.

## Gate 1 — Inspect and fingerprint

Record evidence without sending secrets or personal data to an agent:

- [ ] OS name/version, patch status and architecture.
- [ ] CPU, available cores, installed/available RAM, disk capacity/free space and filesystems.
- [ ] GPU/VRAM/driver only if present; do not infer its existence from an old report.
- [ ] Power/uptime constraints, thermal behavior and network stability.
- [ ] Existing runtimes, ports, services, users, firewall and disk-encryption state.
- [ ] Backup destination and whether a clean rebuild is practical.
- [ ] Configuration fingerprint and inventory timestamp.

Use the actual inspection output to complete docs/17-available-resource-inventory.md. Do not publish credentials, sensitive public IP details, personally identifying file paths, or full environment dumps.

## Gate 2 — Protect the host before installing agents

- [ ] Apply updates and remove or disable unnecessary exposed services.
- [ ] Create a dedicated, non-admin service identity and workspace root.
- [ ] Verify operator personal files, browser sessions and password stores are inaccessible.
- [ ] Define host firewall policy and allowed outbound destinations.
- [ ] Select one private remote-access mechanism only after reviewing account/device policy. Do not use a public tunnel as a convenience shortcut.
- [ ] Test access from an approved device and confirm an unapproved device cannot connect.
- [ ] Configure an independent stop/disable path and test it.
- [ ] Record the policy/configuration, test time and evidence location.

Private connectivity is necessary but not sufficient: test application/tool permissions separately.

## Gate 3 — Bind the prepared configuration

Keep the tracked templates unchanged for machine-specific values. Copy them to the ignored local files documented in docs/19-preconfiguration.md. Edit local copies only when each value is supported by evidence.

- [ ] Fill actual host type/name/OS, non-admin service identity and configuration fingerprint.
- [ ] Fill reviewed private remote-access provider and policy status.
- [ ] Keep public ingress disabled and use deny-unlisted network egress.
- [ ] Set measured CPU, memory, process, disk, timeout and retry limits.
- [ ] Choose model mode only after privacy, quality, latency, quota and cost review; add per-task token/money limits when hosted inference is used.
- [ ] Record monthly and one-time spending ceilings, currency and a tested hard-stop behavior.
- [ ] Configure independent audit, encrypted durable task state, checkpoints, idempotency, tested backup/restore and an independent stop path.
- [ ] Keep high-impact actions denied or approval-gated.
- [ ] Keep jobs disabled until the candidate config, policy and host-bound evidence are reviewed.

Run from the repository root: python scripts/check_docs.py; python scripts/validate_preconfiguration.py; python -m unittest discover -s tests -v.

A passing check proves only that effective local configuration satisfies coded guardrails. It does not verify referenced evidence or establish runtime enforcement. The local fingerprint helper requires all three local candidate files; put the resulting digest in both local preconfiguration and local promotion evidence. Any later config, policy or job-catalog change alters the digest.

## Gate 4 — Recoverability and isolation before agent work

- [ ] Configure a backup of minimal configuration and required durable task state.
- [ ] Restore that backup into a clean location or environment and verify it.
- [ ] Verify the worker cannot read operator data or configuration secrets.
- [ ] Verify unlisted network egress is blocked.
- [ ] Verify the policy layer denies a forbidden action before the side effect.
- [ ] Verify approvals bind to the exact action, arguments and target.
- [ ] Verify the agent cannot alter independent audit history.
- [ ] Revoke a test credential and confirm access stops.
- [ ] Test durable checkpoints, idempotency and recovery after process/host interruption.
- [ ] Test timeout, cancellation, worker failure, bounded retries and spending hard stop.
- [ ] Record every result in the local evidence manifest with host fingerprint, exact runtime/policy versions, UTC timestamp and reviewable artifact reference.
- [ ] Record failures and residual uncertainty; do not accept undocumented exceptions.

## Gate 5 — First bounded job

Start with the read-only repository-assessment job in docs/16-workload-inventory.md, using one explicitly named repository and a pinned ref.

- [ ] No production credentials or broad personal-data access.
- [ ] One task at a time, a fixed timeout and a clear stop path.
- [ ] Retain task ID, repository/ref, source paths, tool events, output digest and reviewer result.
- [ ] Re-run the task on a small preregistered set of representative cases.
- [ ] Include malformed inputs, missing files, permission denial and provider/network failure.
- [ ] Compare the report to repository evidence; keep unsupported claims marked UNKNOWN or INFERENCE.

Only after the read-only job passes should a disposable-worktree patch/test job be considered. Do not jump directly to unattended multi-agent execution.

## Gate 6 — Promote narrowly, not globally

Promotion requires:

- Configuration validator passes.
- Unit/regression and integration tests pass.
- Isolation, network-egress, approval, audit and recovery evidence is retained.
- Cost/latency/quality metrics meet pre-agreed thresholds.
- A human approves the exact job class and configuration.
- Rollback, stop and credential-revocation steps are tested.

Promotion applies only to the job class, host fingerprint, runtime versions and policy version tested. New jobs, new tools, new credentials, model changes or material OS/runtime upgrades require appropriate revalidation.

## Current readiness

The runbook is ready; host inspection, installation, resource benchmarks, network-policy tests, backup/restore and agent execution remain **NOT STARTED** because a computer is not currently available for Shed-Z use.
