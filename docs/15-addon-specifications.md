# 15 — Add-on specifications

This document sets the minimum behavior and evidence expectations for the add-on features that turn the foundation into a full system.

## Common baseline for every add-on

- [ ] Supported task class and explicit non-goal are documented.
- [ ] Policy state is defined per action (`DENY` / `APPROVAL_REQUIRED` / `ALLOW`), with approval bound to exact args and target.
- [ ] Audit/log evidence is separate from the worker; logs are redacted.
- [ ] Durability and recovery are outside Herdr; Herdr is only a session/interaction layer.
- [ ] Open choices are captured in an ADR before implementation is treated as ready.

## 1) Chat ingress

- **Minimum behavior:** accept input only from approved channels or devices; convert messages to task records; classify before execution; no direct side effects from chat text; route all actions through the policy gate.
- **Non-goal:** open-ended autonomous executor or hidden privileged backchannel.
- **Ready evidence:** channel/device access policy tested; prompt-injection fixture cannot expand authority; action-bound approval works; task and audit records are retained.

## 2) Browser automation

- **Minimum behavior:** run in an isolated browser context or profile; allowed destinations and actions are explicitly listed; personal sessions and password stores are inaccessible; external writes require approval.
- **Non-goal:** general personal browsing or credentialed access to operator accounts.
- **Ready evidence:** isolated profile test; cross-site / injection fixture blocked; secret and egress tests pass; remote scan shows only approved paths.

## 3) Inbox access

- **Minimum behavior:** read only the designated mailbox; treat mail as untrusted content; support classification or task creation; send and reply actions are gated.
- **Non-goal:** personal email access or autonomous outbound email.
- **Ready evidence:** scoped mailbox credentials; secret-canary inaccessible; untrusted-mail fixture cannot expand authority; send action requires approval and leaves an audit trail.

## 4) Scheduled monitoring

- **Minimum behavior:** schedule, claim, timeout, retry, cancel, dedupe; persist state outside the worker and Herdr; emit alert/result artifacts; include a global stop switch.
- **Non-goal:** using Herdr as the durable scheduler or claiming exactly-once external effects.
- **Ready evidence:** host/worker restart drill; timeout/cancel/retry tests; duplicate or partial execution test; recovery evidence artifact.

## 5) MCP tools and extensions

- **Minimum behavior:** only reviewed/pinned servers; explicit tool allowlist and resource scope; isolated execution; version and digest pinning; no arbitrary shell passthrough.
- **Non-goal:** unreviewed extension ecosystem or blanket tool access.
- **Ready evidence:** reviewed manifest plus lockfile or digest; dependency scan; isolated execution verified; blocked-install test for an unreviewed server.

## 6) Model routing

- **Minimum behavior:** route work by task class, cost ceiling, and risk; hosted and local inference choices must be explicit and auditable.
- **Non-goal:** silent model switching based on convenience alone.
- **Ready evidence:** routing table documented; test cases show expected routing; budget and quota checks hold.

## 7) Audit and observability

- **Minimum behavior:** emit append-only receipts, metrics, and alerts outside the worker; keep redacted logs; expose completion evidence.
- **Non-goal:** using a status indicator as proof of success.
- **Ready evidence:** append-only log sink verified; completion checks produce artifacts; failed runs remain visible.

## 8) Recovery and runbooks

- **Minimum behavior:** restore, revoke, rebuild, and stop-all procedures are documented and executable; each supported job class has a runbook.
- **Non-goal:** assuming restart behavior equals safe recovery.
- **Ready evidence:** restoration drill on clean environment; revocation test; rebuild test; runbook review signed off.

## Ready-state rule

A feature is not considered ready until the spec, the evidence, and the roadmap gate all agree.
