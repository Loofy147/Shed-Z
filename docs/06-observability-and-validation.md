# 06 — Observability and validation

**Status:** measurement and verification requirements; no metrics pipeline or test harness is claimed to exist yet.

## Goals

Observability must make execution reconstructable and failures discoverable. Validation must establish whether the requested outcome actually happened and met its acceptance criteria. These are related but not interchangeable: a detailed trace can describe a bad result, while a correct-looking result can still lack adequate proof.

## Minimum event envelope

Each event should include, where relevant:

- event ID, timestamp and event schema version;
- task ID, attempt/run ID, action ID, correlation ID and causal parent ID;
- event type, component and actor/runtime identity;
- source request digest, active policy version and decision/approval reference;
- tool and target resource, normalized input digest, outcome and error category;
- model/provider and relevant tool/runtime versions;
- duration, token or provider usage, cost and resource limits;
- artifact/receipt identifiers and content digests;
- redaction and retention classification.

Use structured events rather than relying on free-form terminal text. Keep raw terminal history disabled unless a justified diagnostic need exists; when enabled, treat it as sensitive because it may contain prompts, tokens or command output. The execution worker must not be able to modify previously written audit events.

## Core metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Verified success rate | Tasks passing their predefined acceptance checks / tasks reaching verification. Report failed and inconclusive runs separately. | Prevents self-reported completion from becoming the score. |
| First-attempt success | Tasks passing without retry or human repair / attempted tasks. | Reveals reliability hidden by retries. |
| Intervention rate | Tasks requiring human input or approval / tasks started, split by reason. | Measures operational burden and autonomy boundaries. |
| Unsafe-action block rate | Known prohibited test actions blocked before side effect / prohibited test actions attempted. | Tests policy enforcement; do not treat unknown attacks as covered. |
| Recovery success | Interrupted tasks safely reconciled to a known state / interrupted tasks requiring recovery. | Measures resilience after worker/host/provider failure. |
| Duplicate-side-effect rate | Confirmed duplicate external effects / operations that could create such effects. | Detects unsafe retry and acknowledgement behavior. |
| Cost per verified success | Total attributable model/compute cost / verified successful tasks. | Compares architectures without rewarding cheap failed output. |
| Completion latency | Start-to-verified-completion duration, including queue time; report median and tail percentiles. | Captures speed that operators actually experience. |
| Availability and queue delay | Host/service availability, queue age, worker saturation and provider error rate. | Shows whether the shed is ready when needed. |
| Artifact completeness | Tasks with all required evidence receipts / closed tasks. | Reveals unverifiable closures. |

Always segment results by task class, risk, model/runtime version and failure type. Report sample size and uncertainty. A high score on easy, author-written tasks does not establish general reliability.

## Verification-independence scale

The V0–V5 labels below are a **Shed-Z project convention**, not a universal or certified scale. Report the level actually used for each material claim; do not silently promote a repeated check to independent verification.

| Level | Evidence | Limitation |
|---|---|---|
| V0 | Model/agent asserts that the result is correct. | No independent check. |
| V1 | Output schema or basic format checks pass. | Correct shape does not establish correctness. |
| V2 | Deterministic tests, static checks or a reproducible command pass. | Tests may omit the defect or share the same assumptions. |
| V3 | Separate reviewer/context checks the work against explicit criteria; reviewer authority and information access are documented. | A second model is not automatically independent. |
| V4 | External system state or integration behavior is queried and reconciled against expected effects. | The queried system or credential may still be wrong or compromised. |
| V5 | Independent evidence/artifact, replay or adversarial/failure-injection result supports the claim, with reproducible inputs and provenance. | No finite test proves universal safety; record residual uncertainty. |

For high-impact claims, prefer more independent evidence and direct state checks. A system must not use V0-only evidence to authorize production actions.

## Validation layers

1. **Documentation/configuration:** check links, schema versions, policy configuration and dependency pins.
2. **Unit/contract:** verify normalized action arguments, policy decisions, state transitions, idempotency and approval expiry.
3. **Integration:** verify real connections between task journal, worker, session layer, tool adapter and evidence store.
4. **Security/adversarial:** test prompt injection, unauthorized filesystem access, secret canaries, egress restrictions, unreviewed extension install and approval bypass.
5. **Failure injection:** interrupt the process at each side-effect boundary, kill/restart the worker, lose the response after an external action, exhaust budget/disk, revoke credentials and simulate provider outage.
6. **Recovery:** restore on a clean environment and reconcile tasks with uncertain external outcomes.
7. **Pilot evaluation:** preregister task set, acceptance thresholds, failure categories and exclusions before test execution; retain every attempted run.

Use real-world representative jobs when possible. If synthetic test tasks are used, document what they do and do not represent.

## Minimum task evidence bundle

For every evaluation run retain:

- preregistered task brief and acceptance criteria;
- immutable run/task identifiers and config/runtime fingerprints;
- inputs or privacy-safe input digests;
- chronological policy, approval and action events;
- redacted logs, exit states and external receipts;
- test results, diffs and output artifact hashes;
- cost, duration, retries, interventions and failure classification;
- reviewer identity/role, verification level and unresolved uncertainty.

Keep failures and inconclusive attempts. A successful retry does not erase an earlier failure.

## Alerts and thresholds

The project has not selected numeric thresholds yet. Choose them from real workload measurements and risk impact, then record them in an ADR or job-class profile. At minimum, alert on:

- task failure, queue-age breach, repeated retries or blocked tasks exceeding their deadline;
- provider outage, unusual latency or budget/quota exhaustion;
- unexpected configuration, binary, tool, extension or policy changes;
- any denied high-impact attempt, secret-canary access or egress-policy violation;
- audit sink failure, backup failure or recovery state that cannot be reconciled;
- host/worker outage, disk or memory pressure and global stop activation.

If the audit sink fails, decide explicitly which job classes halt; do not silently continue sensitive unattended execution without evidence.
