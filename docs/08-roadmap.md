# 08 — Evidence-gated roadmap

The roadmap advances only when the prior phase's exit criteria are met. Dates are intentionally omitted until the host, task scope and resource budget are selected.

## Phase 0 — Foundation (current)

- [x] Define the working concept and distinguish source facts from inference.
- [x] Research the original usage, Herdr capabilities, Tailscale controls and agent-security guidance.
- [x] Create the reference architecture, threat model, operating contract and validation plan.
- [x] Record unresolved choices rather than silently selecting a stack.
- [x] Define the full agent roster and stateful services.
- [x] Define the durable state model and secure instruction governance.
- [x] Define the add-on feature catalog and specifications.
- [x] Add candidate workloads and a risk/impact classification scheme in `16-workload-inventory.md`.
- [x] Inventory currently visible resources and preserve unverified constraints as UNKNOWN in `17-available-resource-inventory.md`.
- [x] Define cost, capacity and approval controls in `18-cost-and-capacity-model.md`.
- [x] Prepare a deployment-disabled config, fail-closed action policy, disabled job catalog and offline validator in `19-preconfiguration.md` and `config/`.
- [x] Separate tracked templates from ignored local configs and add a host/config fingerprint-bound promotion evidence manifest.
- [x] Expand tests for malformed JSON, duplicate keys, type coercion, policy tampering, job catalog and incomplete promotion evidence.
- [x] Add documentation negative fixtures for broken links, escaping paths, unknown source IDs, incomplete ranges and invalid UTF-8.
- [x] Pin workflow actions by full commit SHA, disable persisted checkout credentials and add weekly dependency-update checks.
- [x] Prepare a readiness/test matrix and host-arrival runbook while keeping host facts unset.
- [ ] Owner confirms the first two real jobs, output expectations and failure boundaries.
- [ ] Inspect the actual candidate host, operating system, memory, disk, GPU if present, uptime and recovery access.
- [ ] Inspect actual remote-access/Tailscale status and access policies before relying on private connectivity.
- [ ] Implement/select and independently test a real runtime policy-enforcement boundary.
- [ ] Record an owner-approved monthly incremental spend ceiling and one-time purchase ceiling, even if the approved values are zero.
- [ ] Choose acceptance thresholds for the first job set and record the evidence destination.

**Exit gate:** the owner accepts the first two jobs and their safety boundary; the target host and network are identified; the spending ceiling is explicit; acceptance criteria and evidence capture are defined. No runtime is installed just to make the concept feel concrete.

The repository has templates and a preconfiguration validator, but templates and a passing validator are not evidence that a host has been secured or that runtime controls are enforced. Phase 0 remains open until the unchecked owner/environment inputs are supported by evidence.

## Phase 1 — Safe host and remote-access lab

- [ ] Select dedicated physical host or isolated VM.
- [ ] Create an unprivileged service account and separate workspace root.
- [ ] Configure OS firewall and updates.
- [ ] Configure private overlay, restrict the tailnet policy explicitly, and verify no public ingress.
- [ ] Establish remote stop access that does not depend on the agent.
- [ ] Record host inventory, OS version, disk layout and configuration hashes.
- [ ] Test backup/restore of minimal configuration.

**Exit gate:** only approved devices reach the host; the agent cannot access operator personal data; a clean rebuild is documented.

## Phase 2 — One agent, one repository, one reversible job

- [ ] Select the agent CLI and determine whether Herdr is needed.
- [ ] Pin installation source/version and record license.
- [ ] Run one allowlisted read/test/patch task without production credentials.
- [ ] Persist task ID, lifecycle, diff, logs and exit result.
- [ ] Verify detached client behavior and restart behavior separately.
- [ ] Enforce timeout, resource cap and cancellation.
- [ ] Add independent completion checks.

**Exit gate:** 10–20 controlled runs have no unexplained outcome; failure produces an explicit status, never a silent success.

## Phase 3 — Policy and durable task operations

- [ ] Implement DENY / APPROVAL_REQUIRED / ALLOW enforcement outside model prompts.
- [ ] Add action-bound approval UI or CLI confirmation.
- [ ] Add durable task state, scheduler, retry classification and idempotency receipts as required.
- [ ] Add log redaction, independent event storage and alerts.
- [ ] Test prompt injection, prohibited file access, outbound exfiltration and unapproved external actions.
- [ ] Define budget/concurrency caps and global stop switch.

**Exit gate:** all V2 security tests pass and V3 recovery tests have a recorded result.

## Phase 4 — Controlled pilot

- [ ] Define a representative job set and success criteria before running.
- [ ] Run 20–50 jobs across routine, malformed-input, model-outage and host-restart cases.
- [ ] Publish completion quality, cost, latency, intervention, duplicate-side-effect and failure metrics.
- [ ] Keep failed runs in the data set and classify them.
- [ ] Reassess whether local inference, multi-host workers or a custom dashboard adds measurable value.

**Exit gate:** acceptance thresholds are met, remaining risks are documented, and an independent reviewer approves the pilot boundary.

## Phase 5 — Production hardening (only if justified)

- [ ] Threat model update and independent security review.
- [ ] Recovery-time and data-loss objectives defined and tested.
- [ ] Dependency/extension inventory, pinning, upgrade/rollback policy and vulnerability response process.
- [ ] Availability, disk, cost and provider quotas monitored.
- [ ] Secrets rotation and host rebuild drills tested.
- [ ] Audit retention, privacy, ownership and access control documented.
- [ ] Each supported job has a runbook and explicit authorization profile.
- [ ] Re-run full acceptance tests after material version/configuration changes.

**Exit gate:** production is declared only for the exact task classes and configuration that passed the gates. Do not generalize from a successful coding task to unrestricted autonomy.
