# 08 — Evidence-gated roadmap

The roadmap advances only when the prior phase's exit criteria are met. Dates are intentionally omitted until the host, task scope and resource budget are selected.

## Phase 0 — Foundation (current)

- [x] Define the working concept and distinguish source facts from inference.
- [x] Research the original usage, Herdr capabilities, Tailscale controls and agent-security guidance.
- [x] Create the reference architecture, threat model, operating contract and validation plan.
- [x] Record unresolved choices rather than silently selecting a stack.
- [ ] Add a real workload inventory and impact classification.
- [ ] Record available host/network constraints and an operating-cost ceiling.

**Exit gate:** the owner accepts the first two real jobs, non-goals and safety boundary; no runtime is installed just to make the concept feel concrete.

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
