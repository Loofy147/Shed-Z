# 01 — Research findings

**As of:** 2026-10-25
**Research status:** Initial multi-angle investigation; update sources before implementation.

## Executive finding

The most defensible interpretation of an **AI shed** is an always-on, remotely accessible host that keeps agent processes and their working environment alive beyond the operator's active laptop session. The phrase was used by David Heinemeier Hansson (DHH) on 4 October 2026: “An always-on machine running on their tailscale network where the majority of their herdr agents are running.” The source is the original X post, with the wording cross-checked against contemporaneous mirrors and secondary records [S1–S3].

That wording describes a deployment pattern, not a complete software product or security model. The host, remote-access network, terminal/session manager, agent runtime, task scheduler, model provider, tools, and observability layer are separable components.

## Findings and claim status

| ID | Claim | Status | Evidence and limits |
|---|---|---|---|
| R-001 | “AI shed” was used by DHH on 2026-10-04 to mean an always-on Tailscale-connected machine running most of his Herdr agents. | **FACT** | Exact wording is available from a mirror of the post and is corroborated by contemporaneous aggregators [S1–S3]. Direct X fetch was not necessary for the wording to appear, but the first-party permalink is included in the source register. |
| R-002 | The term is an emerging practitioner label rather than a formally standardized architecture. | **INFERENCE** | The reviewed sources provide a social-post definition and implementation guides, not a standard, reference specification, conformance test, or agreed set of required components. This is a bounded literature finding, not proof that no other specification exists. |
| R-003 | Herdr is a terminal/workspace manager for agent work, not a complete trust or authorization system. | **ESTABLISHED + INFERENCE** | Herdr documents workspaces, panes, agent lifecycle inspection/control, terminal I/O and persistent server sessions [S4–S6]. Those capabilities do not by themselves establish fine-grained authorization for arbitrary external effects. Do not infer controls that are not documented and tested. |
| R-004 | Detaching from a live Herdr server preserves running processes; a full server restart does not preserve arbitrary processes, although layout can be restored and certain agents may resume via their own session mechanisms. | **ESTABLISHED** | Explicitly distinguished in Herdr's session-state documentation [S5]. “Always on” is therefore not the same as “crash-proof” or “every task resumes exactly once.” |
| R-005 | Tailscale provides private connectivity, but authorization policy still matters; some default tailnet policies allow broad device-to-device connectivity. | **ESTABLISHED** | Tailscale documents grants/ACLs, Serve, SSH, and the default-policy caveat [S7–S9]. Never describe “installed Tailscale” as equivalent to least privilege. |
| R-006 | Long-running agents that read untrusted content and use durable credentials can expose data, poison memory, or execute attacker-influenced code. | **ESTABLISHED** | Microsoft Security Research describes these risks in a 2026 analysis of OpenClaw [S10]. OWASP's Agentic Applications 2026 risk taxonomy includes goal hijacking, tool misuse, identity/privilege abuse, supply-chain risks, unexpected code execution, and memory/context poisoning [S11]. The exact risk depends on the runtime and permissions. |
| R-007 | A safe baseline requires isolation, least privilege, restricted network egress, human approval for high-impact actions, budgets, auditability, and a recovery plan. | **ESTABLISHED recommendation** | These controls converge across OWASP, Microsoft Security Research, and vendor deployment guidance [S10–S13]. They are design requirements for this project, not controls already implemented here. |
| R-008 | The model must run locally for a setup to qualify as an AI shed. | **INFERENCE — not implied by the reviewed definition** | DHH's definition is about the always-on machine and agent sessions, not a local inference requirement [S1]. Model inference can be remote or local. This foundation leaves the choice open. |
| R-009 | Herdr alone provides a durable job queue, schedule guarantees, exactly-once external effects, or policy enforcement. | **UNKNOWN / unsupported** | The reviewed Herdr docs establish terminal/session lifecycle and agent control primitives, not these guarantees. Any such requirement needs a separate mechanism and tests. |
| R-010 | The ideal host, cost, model, degree of concurrency, and best runtime for this user's workload are known. | **UNKNOWN / OPEN** | No workload inventory, host inventory, cost measurements, quota tests, or failure-injection results have yet been collected. |

## Important technical distinctions

### Persistent process vs durable task

A terminal manager can keep a process alive while a client disconnects. A durable task system must also record intent, owner/claim, progress, side effects, retries, cancellation, and recovery behavior. Those are different guarantees. Herdr's own documentation distinguishes live process continuity from restoring session layout after a server restart [S5].

### Agent runtime vs model inference

The agent runtime manages prompts, tool calls, state and action loops. Model inference may be performed by a hosted API or a local model server. Hosting agents on a small server does not imply that the model runs on that server, nor does hosting the model make agent execution safe by itself.

### Network reachability vs permission to act

A tailnet controls which devices can connect to a service. The agent also needs application-level permissions: what files it can read, which commands it may run, which APIs it can call, which repositories or branches it may change, and when human approval is mandatory. Network controls and tool-level policies must be layered.

### An observable “done” state vs evidence of success

An agent's status indicator is a runtime signal, not proof that the requested outcome is correct. Require evidence such as passing tests, a clean diff, a validated report, a successful API state check, or an independently reviewed artifact.

## Research method

- Split the search into five angles: original definition, practitioner implementation, agent-runtime architecture, agent security research, and remote-access controls.
- Requested up to 50 Exa results across those search streams, then cross-checked the most relevant official documentation and security sources with direct page retrieval/search.
- Preferred original statements, product documentation, standards and security research over unverified social reposts.
- Secondary implementation write-ups were treated as leads, not as proof of guarantees.

This was a targeted investigation, not an exhaustive systematic review. No benchmark was run and no host or repository was inspected/deployed for this documentation package.

## Open questions for the next evidence pass

1. What exact jobs should run unattended, and what is the cost of a wrong action for each job?
2. Which host is available, where is it located, and what uptime, storage and network reliability can it sustain?
3. Does the first prototype need coding agents only, or also chat ingress, browser automation, inbox access, scheduled monitoring or MCP tools?
4. Which model/API plans may be used, and what are their quotas, provider terms and per-task costs?
5. What state must survive crashes: terminal sessions, task records, partial artifacts, or external side effects?
6. How will logs be protected from secrets, and where will the independent audit record live?
7. What is the tested recovery process after power loss, disk exhaustion, provider outage, corrupted state or a compromised agent?
