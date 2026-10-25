# 04 — Threat model

**Security posture:** assume the agent can be wrong, manipulated by untrusted content, or induced to misuse any authority exposed to it.

## Assets to protect

- Source code, private repositories and unpublished work.
- API tokens, provider credentials, SSH credentials, webhook secrets and CI credentials.
- Personal files, browser sessions, email, identity-provider accounts and password stores.
- Integrity of agent prompts, memory, configuration, tasks and logs.
- External systems: GitHub, deployments, cloud accounts, messaging, databases, commerce and billing.
- Availability and cost ceilings: host uptime, disk, API budgets, concurrency and provider quotas.

## Trust boundaries

1. Operator device ↔ remote-access network.
2. Remote-access network ↔ host services.
3. Control surface ↔ task/policy service.
4. Task broker ↔ worker sandbox.
5. Agent runtime ↔ shell/filesystem/browser/MCP tools.
6. Agent ↔ untrusted web pages, issue text, repository content, email and tool results.
7. Worker ↔ model provider and external APIs.
8. Agent-controlled runtime ↔ independent audit and backup systems.

## Threat and required control register

| Threat | Example impact | Required controls before unattended use | Verification evidence |
|---|---|---|---|
| Indirect prompt injection | A repository README instructs an agent to upload secrets or push code. | Treat retrieved content as data; never let content expand authority; narrow tools; restrict egress; require approval for external writes. | Adversarial fixture fails to read secret paths or send data to an unapproved destination. |
| Credential theft/exfiltration | Agent reads `.env`, SSH keys or environment variables and sends them out. | No personal credentials in worker; dedicated scoped credentials; secret broker where possible; tool-specific credentials; egress allowlist; redacted logs. | Secret canaries are inaccessible to the agent and absent from network/action logs. |
| Excessive agency | Agent deploys, deletes, merges or sends without explicit authorization. | DENY by default for high-impact operations; approval must bind exact action, arguments and target; approval service independent from agent. | Test each prohibited action; verify no side effect before approval. |
| Malicious extension/MCP server | Third-party code reads worker files or credentials. | Vet source/license/permissions; pin versions and digests; isolated execution; approved server inventory; dependency scanning. | Reproducible lockfile/image digest plus reviewed manifests. |
| Memory/context poisoning | Persistent instruction or summary steers future agents. | Source and timestamp for stored memory; separate facts from instructions; integrity checks and review; bounded retention; treat retrieved memory as untrusted. | Poisoned memory fixture does not override system/policy; changes are recorded. |
| Cross-project contamination | One agent reads another repo's secrets or changes unrelated branches. | Separate OS users/containers/worktrees; minimal mounts; one task/repository identity; clean workspaces. | Cross-workspace read/write test fails. |
| Public ingress or weak tailnet policy | Dashboard/SSH is reachable by unintended devices or internet. | No public ingress by default; explicit grants/ACLs; access only from operator devices; restrict SSH users/ports; verify firewall independently. | Remote scan and policy tests show only approved path/device can connect. |
| Duplicate or partial execution | Retry sends a message twice or redeploys after uncertain timeout. | Persist task IDs, action IDs and external receipts; idempotency keys where supported; retry only known-safe operations; recovery states. | Kill worker between action and acknowledgement; prove duplicate does not occur or job enters manual recovery. |
| Silent failure or false completion | Agent reports “done” although tests fail or no artifact exists. | Completion contract with checks; independent test/reviewer; observable state transitions; timeouts and alerting. | Deliberately broken task is failed, not marked successful. |
| Runaway spend/resources | Parallel agents consume quota, memory, disk or provider budget. | Per-task token/cost ceilings, concurrency limits, timeouts, disk quotas, backpressure and a global kill switch. | Budget/concurrency exhaustion tests stop new work predictably. |
| Host compromise | Arbitrary command or dependency compromises the host. | Dedicated VM/host; non-root service; OS sandbox/container/VM; no broad home-directory mounts; patch/rebuild procedure. | Containment test plus rebuild-and-restore drill. |
| Audit tampering | Agent edits or removes its evidence. | Send events to a separate append-only or access-separated log sink; restrict worker write permissions. | Agent cannot mutate prior audit events; hashes/receipts reconcile. |

## Risk-class authorization defaults

Use the following policy states for every tool/action category:

- **DENY** — not permitted in this environment, even if the model asks for it.
- **APPROVAL_REQUIRED** — the action can execute only after an explicit human approval that identifies exact parameters, target and consequences.
- **ALLOW** — a narrow operation can proceed automatically within a stated scope and limit.

Initial examples:

| Action | Default |
|---|---|
| Read an allowlisted repository and run allowlisted tests in a sandbox | ALLOW |
| Read arbitrary personal home directories, browser profiles or password stores | DENY |
| Install an unreviewed skill, extension or MCP server | DENY |
| Send an external message, create a public post, spend money or change permissions | APPROVAL_REQUIRED or DENY, depending on scope |
| Push a branch, merge, release or deploy | APPROVAL_REQUIRED |
| Delete data or rotate/revoke credentials | APPROVAL_REQUIRED; separate recovery process |
| Access a new network destination | APPROVAL_REQUIRED and update allowlist only after review |

The policy is enforced outside the model prompt. Prompt text alone is not a security control.

## Minimum acceptable isolation

- Dedicated VM/physical host, or a separately isolated worker environment.
- Dedicated non-admin OS identity.
- No mount of the operator's home directory by default.
- No access to personal browser sessions or password manager files.
- Secrets delivered only to the exact tool/process that needs them, never in chat transcripts.
- Network policy that restricts inbound and, where feasible, outbound traffic.
- Reviewed/pinned extensions and MCP servers.
- A tested stop/disable/revoke/rebuild procedure.

Microsoft's 2026 OpenClaw analysis is a strong warning that self-hosted agent runtimes should be treated as potentially untrusted code execution with persistent credentials; its runtime-specific findings should not be generalized as a claim that all agents have the same vulnerabilities [S10]. The project adopts the defensive posture because the consequences of a bad action can be high.
