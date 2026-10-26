# 17 — Available resource and constraint inventory

**Status:** initial inventory; several entries are user-reported or unknown.  
**Last inspected:** 2026-10-26.

## Principle

Design around resources that can be verified now. Do not convert a remembered device specification, a visible integration, or an account's apparent availability into an assumption about actual runtime capacity, credentials or permissions.

## Inventory

| Resource / constraint | Current evidence | Status | Implication / next check |
|---|---|---|---|
| Shed-Z repository | Public repository Loofy147/Shed-Z; default branch main; connected GitHub integration reported admin/maintain/push permissions for the authenticated owner | FACT — observed via GitHub connector | Treat repository state and CI evidence as the project record; verify branch and permissions before any mutation |
| Documentation validation | Dependency-free Python checker and GitHub Actions workflow exist on the foundation PR branch; one run completed successfully | FACT — CI run observed | Use existing CI to validate docs before introducing a separate runner |
| PR-based documentation changes | PR #1 exists and is reviewable; it is not merged | FACT — observed | Additional preparation can continue on the same branch; do not describe main as containing the new changes until merged |
| Operator client | Android phone / Chrome use previously reported by owner | USER_REPORTED | Prefer low-friction review links and commands; remote shell work should not depend on phone-only interaction |
| Available computer | Owner has now confirmed that no computer is currently available for Shed-Z use. Earlier reports mentioned an Intel i5 7th-generation system, 8 GB RAM and a possible GTX 1080, but that hardware is not an available target resource at present. | USER_REPORTED — current availability statement | Keep host-dependent configuration unset. Do not design around the earlier reported specifications, claim local inference capacity, or begin host installation until a target machine is actually available. |
| Existing local credentials | Not inspected | UNKNOWN / OPEN | Do not copy personal credentials to a worker; confirm whether an isolated service identity is available |
| Tailscale account / tailnet | Referenced by the AI-shed design; actual owner devices, policies, ACL/grants and device approval not inspected | UNKNOWN / OPEN | Do not presume private remote access has been configured |
| Cloud VM / always-on host | No provisioned host was confirmed in the inspected repository | UNKNOWN / OPEN | Do not create a paid host until the first jobs and budget are approved |
| Local model runtime / GPU support | No runtime or benchmark evidence inspected | UNKNOWN / OPEN | Local inference is optional; defer until a representative benchmark shows a benefit |
| Hosted model/API access | Provider and account entitlement were not inspected here | UNKNOWN / OPEN | Do not assume a paid API key, free quota or subscription entitlement |
| Scheduler / durable task database | Specified in architecture documents but not shown as deployed code | NOT IMPLEMENTED / UNVERIFIED | Use CI only for CI-appropriate triggers; do not claim general scheduling or durable task recovery |
| Audit sink / notification destination | Proposed in docs but not verified as configured | UNKNOWN / OPEN | Design outputs first; connect external notifications only after scope and credentials are approved |
| Backup and restore | No recovery drill evidence found in the repository reviewed | NOT TESTED | No production readiness claim until a clean restoration test exists |

## What can be done with current evidence

1. Continue source-backed design, repository review and document validation directly in GitHub.
2. Use the existing GitHub Actions workflow for documentation integrity while its permissions remain read-only.
3. Define workload and risk contracts before selecting the execution host.
4. Produce a host-inspection checklist that can be run locally without sending secrets or personal files to an agent.
5. Keep local inference, a public dashboard, a new cloud VM, and a scheduler out of the critical path until workload evidence justifies them.

## Host inspection record template

Complete this table only on the actual intended host. Do not paste secrets or personal data.

| Field | Recorded value |
|---|---|
| Inventory ID / date / operator | OPEN |
| Host type: physical / VM / cloud | OPEN |
| OS and version / patch state | OPEN |
| CPU model and available cores | OPEN |
| Total and available RAM | OPEN |
| GPU model, VRAM and driver (if any) | OPEN |
| Free disk by filesystem; backup destination | OPEN |
| Power/uptime constraints | OPEN |
| Network type, inbound rules and outbound restrictions | OPEN |
| Tailscale installed, device name and policy review | OPEN |
| Service account / privilege level | OPEN |
| Existing runtimes/tools and exact versions | OPEN |
| Secret storage approach (no secret values) | OPEN |
| Recovery access independent of the agent | OPEN |
| Monthly incremental operating cost | OPEN |
| Evidence location / configuration fingerprints | OPEN |

## Readiness rule

A device specification is not evidence that it is a suitable host. Record testable facts from the target machine, benchmark the first bounded job, and keep the actual run artifacts. If current hardware is insufficient, decide between smaller scope, hosted inference and a separately approved host only after measurement.
