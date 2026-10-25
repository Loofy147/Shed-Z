# 16 — Initial workload inventory

**Status:** candidate inventory for Phase 0; owner validation is still required.  
**Evidence date:** 2026-10-25.

## Availability-first principle

Available capability is the centre of gravity. Start from verified devices, existing accounts, repositories and permitted execution surfaces. Do not make a new server, local model, paid service, scheduler, dashboard or agent framework a prerequisite until a representative workload proves it is needed.

This principle is a project constraint, not a claim that the current environment is sufficient for every workload. Unknown availability must stay marked as unknown until inspected.

## Evidence legend

- **FACT — repository-observed:** directly read from the current Shed-Z repository or validated through a recorded GitHub result.
- **USER_REPORTED:** context previously provided by the project owner but not yet verified in the target host/session.
- **INFERENCE:** candidate use based on the project’s purpose; requires owner confirmation.
- **UNKNOWN / OPEN:** must be inspected, selected or measured.

## Workload candidates

These are job classes to evaluate, not a declaration that the corresponding runtime is deployed.

| ID | Candidate job | Proposed inputs | Expected output and evidence | Initial risk | Initial execution mode | Status |
|---|---|---|---|---|---|---|
| W-01 | Documentation integrity check | Shed-Z Markdown files and source register | Checker output, list of links/source IDs checked, CI run URL | Low | Existing GitHub Actions workflow | **FACT:** documented checker and workflow were added on the PR branch; first CI run passed |
| W-02 | Repository evidence and architecture review | One explicitly named repository, its README, docs, tests and metadata | Evidence-backed findings, source paths/SHAs, uncertainty register and next actions | Low–medium | Read-only | **INFERENCE:** good first agent workload; owner to confirm |
| W-03 | Isolated code/test repair | One task, one repository, bounded worktree or disposable worker | Minimal diff, tests, logs, exit state and independent review | Medium | Sandboxed write; no production credentials; no automatic merge/deploy | **INFERENCE:** candidate for the first write-capable pilot |
| W-04 | CI failure triage | A workflow run and its logs/artifacts | Failure classification, linked evidence, likely cause separated from confirmed cause | Low–medium | Read-only first | **INFERENCE:** depends on GitHub permissions and data access |
| W-05 | Periodic repository health report | Explicit repository allowlist and schedule | Timestamped report, new failures, dependency/security signals and evidence links | Medium | Scheduled read-only; bounded network; a stop switch | **HYPOTHESIS:** requires scheduler, alert channel and schedule approval |
| W-06 | External side effects (merge, deploy, send, delete, spend, change permissions) | Exact proposed action and target | Action-bound approval, pre/post-state evidence and external receipt | High | Approval required or denied by default | Excluded from the initial pilot |

## Recommended first two jobs

### Job A — Documentation integrity

Purpose: establish a repeatable baseline without granting an agent broad authority.

- Trigger: pull request or push to the relevant branch.
- Scope: Markdown link targets and research source identifiers inside this repository.
- External side effects: no runtime deployment or repository mutation beyond the ordinary CI run.
- Acceptance criteria:
  1. The checker exits zero when all checked references are valid.
  2. A deliberately broken local link causes a non-zero exit.
  3. A deliberately unknown cited source ID causes a non-zero exit.
  4. Failures include the filename and an actionable message.
  5. The workflow runs with read-only repository permissions.
- Evidence: commit SHA, workflow run ID, job conclusion and, for test fixtures, expected/actual exit status.
- Limitation: this does not verify external URLs, prove research claims or test runtime security.

The first workflow pass is established for the current PR head. Negative tests for deliberately broken fixtures remain open until run.

### Job B — Read-only repository assessment

Purpose: prove an agent can inspect a bounded repository and provide useful, verifiable output before it can modify code.

- Trigger: explicit operator request.
- Scope: one selected repository and a defined set of files/metadata.
- Permissions: read-only GitHub access; no shell credentials or secret-bearing environment.
- Output: claim ledger containing claim, status, evidence URL/path, relevant commit SHA, uncertainty and suggested next check.
- Acceptance criteria:
  1. Every material repository claim points to a source artifact.
  2. Claims not supported by the inspected repository remain UNKNOWN or INFERENCE.
  3. No write, push, merge, deployment, external message or secret access occurs.
  4. The report distinguishes observed fact from proposed remediation.
  5. A reviewer can reproduce the central findings.
- Evidence: task brief, exact repository/ref, files inspected, tool results, report hash and review record.

## Candidate write-capable pilot

Only after Jobs A and B pass their gates, use Job C: a small repair in a temporary worktree or disposable worker, with no production credentials and no direct push to the protected branch.

Required controls: task timeout, CPU/memory/disk limits appropriate to the chosen environment, limited network egress, tracked diff, deterministic tests, stop control, and post-task cleanup. Failure must leave an inspectable artifact and an explicit status.

## Impact classification

| Class | Examples | Default policy |
|---|---|---|
| I0 — Read-only, reversible | Read allowlisted docs, inspect CI logs, calculate metrics | ALLOW within scope |
| I1 — Local isolated mutation | Edit a scratch worktree, run tests in a disposable worker | ALLOW only in the defined sandbox |
| I2 — Repository-visible mutation | Create branch, commit, open PR, modify issue or workflow | APPROVAL_REQUIRED until separately tested and scoped |
| I3 — Operational/external effect | Deploy, merge, send externally, alter access, delete data, spend money | APPROVAL_REQUIRED or DENY; never inferred from generic task consent |
| I4 — Secret/control-plane access | Read password stores, broad personal files, production root credentials or signing secrets | DENY for the initial project |

The labels are Shed-Z conventions. Reclassify an action if its real target or consequences differ.

## Owner inputs still required

- Confirm which two jobs have the highest practical value.
- Name the first repository/job target after documentation checking.
- Confirm whether any output must be delivered to an external channel.
- Define unacceptable failures and maximum tolerated intervention.
- Approve a monthly spending ceiling before activating paid infrastructure, provider usage or new subscriptions.

Until these are recorded, Phase 0 remains open.
