# 09 — Source register

**Source snapshot date:** 2026-10-25. Re-check fast-moving product docs before implementation. The register distinguishes sources by role; citations are not endorsements.

## Primary statements and implementation documentation

| ID | Source | Type / date | Use in this foundation | Limitations |
|---|---|---|---|---|
| S1 | [DHH's original X post — `@dhh`](https://x.com/dhh/status/2106755814421565495) | Primary statement; 2026-10-04 | Exact compact definition of “AI shed” and direct link to Herdr/Tailscale interpretation. | The direct X page was not successfully fetched in this session; wording was cross-checked against mirrors/aggregators below. |
| S2 | [PPLL record of DHH's public posts](https://ppll.app/dhh) | Secondary mirror/aggregator; accessed 2026-10-25 | Shows the 4 October 2026 quote and date. | Aggregator, not DHH-authored documentation. |
| S3 | [Vibecoding.tech: “AI agents keep working after you disconnect: Herdr runs the session on a separate machine”](https://vibecoding.tech/news/2026/10/04/herdr-always-on-agent-machine) | Secondary implementation report; 2026-10-04 | Context around the original post and how the pattern is being interpreted by practitioners. | Treat specific hardware/setup claims as secondary reporting; not used as a required design assumption. |
| S4 | [Herdr repository](https://github.com/herdrdev/herdr) | Official implementation source; accessed 2026-10-25 | Establishes Herdr's role as a terminal/workspace manager; repository states Apache-2.0 license. | Repository presence/license do not prove a particular deployment's behavior or security. Pin a release/commit before install. |
| S5 | [Herdr: Session state and restore](https://herdr.dev/docs/session-state/) | Official product documentation; accessed 2026-10-25 | Distinguishes detach/reattach, server restart, layout snapshots, pane history and native agent resume. | Actual behavior depends on version, agent integration and failure mode; test the versions selected. |
| S6 | [Herdr: Agent automation](https://herdr.dev/docs/agent-automation/) and [Persistence and remote access](https://herdr.dev/docs/persistence-remote/) | Official product documentation; accessed 2026-10-25 | Establishes workspace/pane/agent primitives, status inspection, terminal input/output and remote attach over SSH. | Does not establish a general-purpose durable queue, universal policy gate or exactly-once side effects. |
| S7 | [Tailscale: Access control](https://tailscale.com/docs/features/access-control) | Official network documentation; accessed 2026-10-25 | Grants/ACLs and least-privilege access model. | Real settings must be checked in the actual tailnet. |
| S8 | [Tailscale: Manage permissions using ACLs](https://tailscale.com/docs/features/access-control/acls) | Official network documentation; validated 2026-01-05 | Explicit caveat that an unconfigured/default policy may permit broad connectivity; supports deny-by-default principle. | Feature syntax and plan limits can change; validate current policy. |
| S9 | [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve) and [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh) | Official product documentation; Serve validated 2026-01-20, SSH accessed 2026-10-25 | Private service access and SSH controls; Serve is tailnet-facing, while access rules still apply. | A private network is not a replacement for application authentication/authorization. Keep backend binding and proxy assumptions correct. |
| S10 | [Microsoft Security Research: Running OpenClaw safely—identity, isolation, and runtime risk](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/) | Vendor security research; 2026-02-19 | Concrete threat analysis of self-hosted agents with untrusted content, third-party skills, persistent state and credentials. | Findings focus on OpenClaw and should not be misrepresented as a test of all runtimes. Controls are nevertheless relevant as defense-in-depth. |
| S11 | [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Community security framework; published 2025-12-09 | Risk vocabulary for goal hijack, tool misuse, identity/privilege abuse, supply chain and memory/context poisoning. | Risk taxonomy, not a product certification or proof that a deployment is secure. |
| S12 | [OWASP AI Agent and MCP Security guidance](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-2-Develop/2-2-5-AI-Agent-and-MCP-Security/) | Community security guidance; current page accessed 2026-10-25 | Least agency, isolation, tool allowlists, human approval and independent audit expectations. | Specific permission syntax varies by product; copy patterns, not illustrative syntax. |
| S13 | [OWASP Agent Control Standard (ACS)](https://genai.owasp.org/resource/agent-control-standard-acs/) | Community standard/framework; 2026-09-01 | Inspectability, traceability, instrumentation and runtime control as design goals. | Emerging standard; map and test controls in the actual chosen runtime. |
| S14 | [OpenClaw: Gateway architecture](https://docs.openclaw.ai/architecture) | Official product docs; accessed 2026-10-25 | Example of a long-lived self-hosted gateway architecture connecting channels, clients, nodes and agent sessions. | Not selected as the default runtime; assess with threat model before use. |
| S15 | [OpenClaw: Agent runtime architecture](https://docs.openclaw.ai/agent-runtime-architecture) | Official product docs; accessed 2026-10-25 | Illustrates separation of agent loop, model transport, tools, sessions, plugins and runtime. | Implementation details change quickly; pin version and review security model. |
| S16 | [Anthropic: Secure your Managed Agents deployment](https://platform.claude.com/docs/en/managed-agents/secure-deployment) | Vendor security documentation; accessed 2026-10-25 | Current guidance on reducing tool sets, limiting network egress, isolating credentials, setting budgets and reviewing sessions. | Vendor-specific controls; map equivalent controls for self-hosted deployments. |

## Source-quality policy

- Prefer primary docs and standards for requirements and behavior.
- Use independent security research to identify failure modes, while preserving its stated scope.
- Use secondary reporting to discover implementations and follow up with first-party sources.
- Record publication/access date and version for fast-moving docs.
- A documented feature is not evidence that it is configured or works in the target deployment; that requires a repeatable test artifact.
- When sources disagree, preserve both claims and their scope until independently reconciled.

## Research limitations

The initial search used five thematic streams with up to 50 Exa results requested in total, then direct searches and page retrieval for relevant sources. This was not a systematic review or code audit. No source in this register establishes a universal “AI shed” standard, a default safe configuration, or production readiness of any particular combination.
