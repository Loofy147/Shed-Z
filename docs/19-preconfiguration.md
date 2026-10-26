# 19 — Preconfiguration pack

**Status:** machine-independent baseline prepared; deployment intentionally disabled.  
**Last updated:** 2026-10-26.

## Purpose

Prepare the configuration boundaries before a computer exists. This pack defines what must be decided, the safe defaults to preserve, and a standard-library validator that can run in GitHub Actions or later on the target host. It does not require installing an agent, creating a VM, exposing a port, or providing credentials.

## Files

- `config/preconfiguration.json` — target, networking, runtime, model, budget, audit and recovery fields. Unknown environment values remain null.
- `config/action-policy.json` — action-level baseline. Unknown actions, external effects and high-impact capabilities are denied or require explicit approval.
- `config/job-catalog.json` — candidate jobs and acceptance criteria. All Shed-Z runtime jobs are explicitly disabled; a separate `enabled` field is required for a later reviewed promotion.
- `scripts/validate_preconfiguration.py` — offline checks for configuration integrity and safe defaults.
- `scripts/check_docs.py` — existing document link and research source-reference check.

## Non-negotiable defaults

1. Deployment and agent execution are disabled.
2. Network is private-only, public ingress is false, and unlisted egress is denied.
3. Unknown actions are denied and enforcement must sit outside model instructions.
4. Personal files, secrets and unreviewed extensions are not available to workers.
5. Model routing does not silently fall back to a different model/provider.
6. New paid resources and subscriptions are denied until an explicit spend limit is approved.
7. High-impact actions have no implicit approval.
8. No job is enabled by default. The catalog records candidates, not active autonomous workloads.
9. A worker is not promoted to unattended use until a non-admin service identity, resource limits, reviewed remote access, independent audit storage, tested backup/restore and an independent stop control are evidenced.

## Validate without a computer

The validation script uses only Python's standard library. It can be run in CI:

```sh
python scripts/validate_preconfiguration.py
python scripts/check_docs.py
```

The checks are configuration-integrity checks, not a security certification. They do not test a host, firewall, agent, model provider, authorization service, secret manager or recovery drill.

## Binding a host later

After an actual target machine becomes available:

1. Record its type, hostname, OS, resource capacity, service identity and recovery access in the inventory document.
2. Select one private remote-access mechanism and capture the reviewed policy evidence.
3. Update configuration with only measured limits; do not guess CPU/RAM/GPU or uptime.
4. Select an initial job and inference mode. Hosted inference requires provider/model identification and a documented data/budget decision. Local inference requires a real benchmark on the target hardware.
5. Record explicit monthly/one-time spending authorization. A missing limit is not permission to spend.
6. Implement and test enforcement, worker isolation and an independent stop path before enabling any job.
7. Promote only after the configuration validator passes and the deployment/recovery security tests have recorded results.

Do not paste secret values into tracked files. Later credentials must enter via a separately reviewed secret mechanism; the exact mechanism is deliberately open until the host and runtime are selected.

## Promotion gate

The baseline validator intentionally rejects a partially enabled deployment. Switching runtime flags alone is insufficient. A deployed configuration must name its host, OS and non-admin service identity; prove reviewed private access; set CPU/memory/time limits; select a model mode; record explicit spend authorization; configure independent audit and backup/restore; and define at least one job. Human review of the resulting evidence is still required.

## Current state

The target computer does not exist yet, so host-specific fields intentionally remain unset. This is not a blocker for preparing the policy contract, job definitions, config validator and CI checks. It is a blocker for installation, capacity claims, remote-access claims and deployment-readiness claims.
