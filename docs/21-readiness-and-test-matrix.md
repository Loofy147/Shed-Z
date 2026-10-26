# 21 — Readiness audit and verification matrix

**Status:** repository-level preparation verified by CI; operational runtime verification remains NOT STARTED.
**Last reviewed:** 2026-10-26.

## Decision boundary

No computer is currently available for Shed-Z use. This document separates properties proven by repository tests from checks that require a real host and an actual policy-enforcement implementation.

A green CI result is evidence for the executed checks only. It does not prove host isolation, firewall behavior, denied network egress, real approval enforcement, tamper-resistant auditing, independent stopping or recoverability.

## Verification layers

| Layer | What is checked | Evidence source | Current status |
|---|---|---|---|
| L1 — Repository integrity | Local Markdown links, source IDs, UTF-8 input and repository-path containment | scripts/check_docs.py and tests/test_check_docs.py | Automated in CI |
| L2 — Configuration integrity | Strict JSON parsing, duplicate-key rejection, explicit types, safe defaults, policy/job invariants and obvious secret-value fields | scripts/validate_preconfiguration.py | Automated in CI |
| L3 — Fail-closed regression behavior | Attempts to weaken rules, add unknown allowed actions, enable incomplete jobs, use wildcard egress or partially promote configuration | tests/test_preconfiguration.py | Automated in CI |
| L4 — Promotion-manifest completeness | Required security-check keys, PASS statuses, host fingerprint and runtime/policy/enforcement version binding | Synthetic promotion-candidate fixtures | Automated static validation only |
| L5 — Runtime security | Actual private access, isolation, egress filtering, policy denial before effects, approval binding, audit integrity, revocation, independent stop and restore | Host-bound evidence reviewed by a human | NOT RUN |
| L6 — Workload quality and resilience | Representative task success, retries, timeout/cancel, provider outage, worker/host restart, cost and intervention rate | Preregistered real workload runs and retained artifacts | NOT RUN |

## What the tests now cover

The automated regression suite includes malformed JSON, duplicate keys, non-standard JSON numbers, wrong top-level types, malformed nested sections, type-coercion attempts, non-string enum values, missing/duplicate/changed action-policy entries, unrecognized allowed actions, duplicate job IDs, invalid acceptance criteria, wildcard egress, obvious nested credential fields, incomplete spend ceilings, partial promotion, missing or failed evidence checks, different host fingerprints and changes to configuration after fingerprinting.

Documentation-checker fixtures cover a valid link/source pair, broken local links, paths escaping the repository, unknown source IDs, missing source registers, incomplete source ranges and invalid UTF-8.

The passing promotion candidate is entirely synthetic. It exercises the validator's happy path and demonstrates that drift or missing evidence is rejected. It is not a record that any actual security test has passed.

## Machine-local configuration

Do not insert real hostnames, environment-specific values, private network details or credentials into tracked templates. Once a target computer is available, create local copies of these three files:

- config/local-preconfiguration.json
- config/local-action-policy.json
- config/local-job-catalog.json

Each is covered by the existing config/local*.json ignore rule. The validator selects a local copy when present. Inspect version-control status before sharing changes, and never put secret values, full environment dumps, browser profiles or personal files in the evidence manifest.

After completing the candidate fields and selecting one job, run the validator with the --print-fingerprint argument. It requires all three local files and a valid candidate stage. It prints a SHA-256 digest over canonical effective preconfiguration, action policy and job catalog, excluding only the digest field itself. Put the digest into host.config_fingerprint_sha256 and the local promotion evidence's target_fingerprint_sha256. Subsequent config or policy changes alter the digest and fail the promotion check.

The separate ignored evidence file is config/local-promotion-evidence.json. Use config/promotion-evidence.example.json as the shape reference. It records runtime and policy/enforcement versions, a reviewer, UTC timestamps and safe references to each required test artifact. The manifest must not contain credentials or sensitive log contents.

The validator checks format, required entries, statuses and binding. It cannot determine whether a referenced artifact is genuine or adequate; the underlying results must be opened and reviewed. A field set to PASS is a claim, not proof on its own.

## Required host-bound test evidence

Before any job can be enabled, the evidence record must cover:

1. Host hardening and access through an approved device, plus rejection of an unapproved device.
2. Blocking unlisted outbound destinations and confirming public ingress remains disabled.
3. Policy denial before a forbidden side effect, and approvals bound to the exact action, arguments and target.
4. Audit tamper resistance and proof that credential revocation stops access.
5. Worker isolation from personal data, browser sessions, host credentials and unrelated secrets.
6. Configured backup and a successful clean restore; durable-state checkpoint and idempotency recovery.
7. Independent stop control, timeout, cancellation, worker failure and bounded retries.
8. Explicit per-task and monthly cost caps with a tested hard stop where a metered provider exists.
9. Identified/pinned dependencies and runtime versions, with test artifacts tied to the same config fingerprint and version set.
10. Acceptance replay for the chosen bounded job, including malformed input and missing resources.

A separately enforceable policy component must exist. The tracked action policy states runtime_enforcement.status is not_implemented. Editing the field to verified does not implement enforcement; it must identify actual code/version and an independently reviewable test result.

## Initial workload sequence

- **J-001 — Documentation integrity:** implemented as repository CI, not a running Shed-Z agent job. The job catalog keeps it disabled in the Shed-Z runtime.
- **J-002 — Read-only repository assessment:** candidate first host-bound agent workload, one repository and a pinned ref. It remains disabled pending host/security gates and owner confirmation.
- **J-003 — Isolated code/test repair:** deferred until the read-only assessment meets acceptance thresholds; disposable workspace only, no production credentials, no direct merge or deploy.

## Readiness decision

Repository preparation can continue, but deployment cannot. Keep tracked configuration disabled, spending authorization false, host fields unset, and runtime enforcement marked not implemented until the target environment and actual evidence exist. Passing static validation is not production readiness.
