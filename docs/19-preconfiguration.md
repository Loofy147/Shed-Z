# 19 — Preconfiguration pack

**Status:** machine-independent baseline prepared; deployment intentionally disabled.  
**Last updated:** 2026-10-26.

## Purpose

Prepare the configuration boundaries before a computer exists. This pack defines what must be decided, the safe defaults to preserve, and a standard-library validator that can run in GitHub Actions or later on the target host. It does not require installing an agent, creating a VM, exposing a port, or providing credentials.

## Files

- `config/preconfiguration.json` — tracked safe template for host, network, runtime, model, budget, audit, recovery and durable-state settings.
- `config/action-policy.json` — deny-by-default policy; runtime enforcement is explicitly marked as not implemented.
- `config/job-catalog.json` — candidate job classes, disabled in the tracked baseline.
- `config/promotion-evidence.example.json` — local-only manifest shape for host-bound security tests; all required checks start unfilled.
- `scripts/validate_preconfiguration.py` — strict offline checks plus a local candidate fingerprint helper.
- `tests/test_preconfiguration.py` — regression tests for malformed config, policy tampering, invalid job states and promotion evidence binding.
- `tests/test_check_docs.py` — negative-fixture tests for documentation checking.
- `scripts/check_docs.py` — local document link and research-source reference checker.
- `.github/workflows/docs-validation.yml` — read-only workflow with full commit-SHA action pins.
- `.github/dependabot.yml` — weekly GitHub Actions dependency-update checks.

## Non-negotiable defaults

1. Deployment and agent execution are disabled.
2. Network is private-only, public ingress is false, and unlisted egress is denied.
3. Unknown actions are denied and enforcement must sit outside model instructions.
4. Personal files, secrets and unreviewed extensions are not available to workers.
5. Model routing does not silently fall back to a different model/provider.
6. New paid resources and subscriptions are denied until an explicit spend limit is approved.
7. High-impact actions have no implicit approval.
8. No job is enabled by default. The catalog records candidates, not active autonomous workloads.
9. A worker is not promoted to unattended use until measured CPU/memory/process/disk/time limits, reviewed private access, separate audit storage, encrypted durable state, tested backup/restore, independent stop controls and host-bound evidence for the exact configuration/runtime/policy versions are reviewed.

## Validate without a computer

The validation script uses only Python's standard library. It can be run in CI:

```sh
python scripts/validate_preconfiguration.py
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

The checks are configuration-integrity checks, not a security certification. They do not test a host, firewall, agent, model provider, authorization service, secret manager or recovery drill.

## Binding a host later

After an actual target machine becomes available:

1. Copy the tracked templates to the ignored local files named config/local-preconfiguration.json, config/local-action-policy.json and config/local-job-catalog.json. Keep machine-specific details out of tracked templates.
2. Record host type/name/OS, capacity, service identity, recovery access and a canonical configuration fingerprint.
3. Select one private remote-access mechanism and capture reviewed policy evidence.
4. Derive CPU, memory, process, disk and timeout limits from measured capacity; bound retries and concurrency.
5. Select model mode after privacy, quality, latency, quota and cost review; add per-task token or monetary caps where relevant.
6. Record monthly and one-time spending ceilings, currency and tested hard-stop behavior.
7. Implement and test enforcement, worker isolation, encrypted durable state, checkpointing, idempotency, independent audit and an independent stop path.
8. After completing the local candidate and selecting one job, run the validator with the --print-fingerprint argument. Copy its digest to host.config_fingerprint_sha256 and the local evidence manifest. The digest covers effective preconfiguration, action policy and job catalog but excludes its own field.
9. Fill the local evidence manifest with exact runtime/policy/enforcement versions, reviewer, UTC observation times and safe references to each required test artifact.
10. Promote only after static validation passes and a human independently reviews the actual referenced artifacts. A complete manifest is not proof that tests were performed.

## Promotion gate

The validator rejects partial promotion candidates. In addition to host/network/runtime/model/budget/state requirements, it requires a local evidence manifest with all required checks marked PASS and bound to the same host/config fingerprint and runtime/policy/enforcement versions. The fingerprint identifies the reviewed config; it does not prove test outcomes. A reviewer must inspect the underlying artifacts.

The action policy currently marks runtime enforcement as not implemented. Changing a field to verified does not implement enforcement: a real implementation and independently reviewable test result are required. Static validation is not deployment authorization.

## Current state

No computer is currently available for Shed-Z use, so the tracked template leaves host-specific fields unset. Runtime enforcement is explicitly marked not implemented. CI checks static validation and synthetic manifest behavior; they are not host/runtime tests. Installation, resource benchmarks, access-control tests, runtime security, backup/restore and deployment-readiness claims remain blocked. See docs/20-host-arrival-runbook.md and docs/21-readiness-and-test-matrix.md.
