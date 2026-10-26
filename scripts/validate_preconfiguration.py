#!/usr/bin/env python3
"""Fail-closed validation for Shed-Z configuration templates and promotion evidence.

This script validates configuration structure and declared evidence references. It
does not execute an agent, deploy services, or independently prove that referenced
security tests were performed correctly.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta
from math import isfinite
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
CONFIG_FILES = {
    "preconfiguration": ("preconfiguration.json", "local-preconfiguration.json"),
    "action_policy": ("action-policy.json", "local-action-policy.json"),
    "job_catalog": ("job-catalog.json", "local-job-catalog.json"),
}
EVIDENCE_PATH = CONFIG_DIR / "local-promotion-evidence.json"

ALLOWED_DECISIONS = {"DENY", "APPROVAL_REQUIRED", "ALLOW"}
HOST_TYPES = {"existing_computer", "virtual_machine", "cloud_vm"}
MODEL_MODES = {"hosted", "local", "hybrid"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EVIDENCE_REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{1,511}$")

REQUIRED_ACTION_DECISIONS = {
    "read_allowlisted_repository": "ALLOW",
    "read_ci_logs_and_artifacts": "ALLOW",
    "run_tests_in_disposable_worker": "ALLOW",
    "write_scratch_worktree": "ALLOW",
    "create_branch_or_commit": "APPROVAL_REQUIRED",
    "open_or_update_pull_request": "APPROVAL_REQUIRED",
    "merge_pull_request": "DENY",
    "deploy_or_release": "DENY",
    "send_external_message": "DENY",
    "delete_data_or_resources": "DENY",
    "change_permissions_or_credentials": "DENY",
    "read_personal_files_or_browser_profiles": "DENY",
    "read_secret_stores_or_private_keys": "DENY",
    "install_unreviewed_extension_or_mcp_server": "DENY",
    "create_paid_resource_or_subscription": "DENY",
    "access_unlisted_network_destination": "DENY",
    "unknown_action": "DENY",
}
REQUIRED_JOB_IDS = {"J-001", "J-002", "J-003"}
REQUIRED_EVIDENCE_CHECKS = {
    "host_hardening",
    "private_access_approved_device",
    "unapproved_device_denied",
    "unlisted_egress_denied",
    "policy_enforcement_before_side_effect",
    "approval_binding",
    "audit_tamper_resistance",
    "credential_revocation",
    "backup_restore",
    "independent_stop_control",
    "worker_data_isolation",
    "budget_hard_stop",
    "bounded_job_acceptance_replay",
    "malformed_input_and_missing_resource",
    "timeout_cancel_and_worker_failure",
    "durable_state_checkpoint_recovery",
    "dependency_inventory_and_pin_verification",
}
SENSITIVE_VALUE_KEYS = {
    "api_key", "apikey", "access_token", "refresh_token", "bearer_token",
    "token", "password", "passwd", "secret", "secret_value",
    "password_value", "private_key", "private_key_value", "client_secret",
    "credential", "credentials", "authorization", "auth_header",
    "connection_string", "database_url",
}
SENSITIVE_KEY_SUFFIXES = (
    "_api_key", "_access_token", "_refresh_token", "_bearer_token",
    "_password_value", "_secret_value", "_private_key_value", "_client_secret",
)
PLACEHOLDERS = {"change_me", "set_outside_repo", "replace_me", "placeholder"}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys instead of silently accepting last-key-wins."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON numeric constant is not allowed: {value}")


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve(strict=False).relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    label = _display_path(path)
    if path.is_symlink():
        raise ValueError(f"configuration path must not be a symlink: {label}")
    try:
        resolved = path.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ValueError(f"required file is missing: {label}") from exc
    try:
        resolved.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"configuration path escapes repository root: {label}") from exc
    if not resolved.is_file():
        raise ValueError(f"configuration path is not a regular file: {label}")

    try:
        value = json.loads(
            resolved.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_nonstandard_constant,
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {label} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"configuration is not valid UTF-8: {label}") from exc
    except ValueError as exc:
        raise ValueError(f"invalid JSON in {label}: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value must be an object: {label}")
    return value


def load_effective_config(name: str) -> dict[str, Any]:
    base_name, local_name = CONFIG_FILES[name]
    local_path = CONFIG_DIR / local_name
    # Local copies are ignored by Git and override tracked templates when present.
    # A broken symlink is rejected rather than silently ignored.
    chosen = local_path if (local_path.exists() or local_path.is_symlink()) else CONFIG_DIR / base_name
    return load_json(chosen)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def positive_number(value: Any) -> bool:
    return type(value) in (int, float) and isfinite(value) and value > 0


def nonnegative_number(value: Any) -> bool:
    return type(value) in (int, float) and isfinite(value) and value >= 0


def positive_integer(value: Any) -> bool:
    return type(value) is int and value > 0


def nonnegative_integer(value: Any) -> bool:
    return type(value) is int and value >= 0


def string_list(value: Any, *, allow_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(nonempty(item) for item in value)
    )


def section(parent: dict[str, Any], key: str, label: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"{label} must be a JSON object")
        return {}
    return value


def valid_utc_timestamp(value: Any) -> bool:
    if not nonempty(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timedelta(0)


def is_sensitive_value_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_").replace(" ", "_")
    return normalized in SENSITIVE_VALUE_KEYS or normalized.endswith(SENSITIVE_KEY_SUFFIXES)


def scan_for_secret_values(value: Any, label: str, errors: list[str]) -> None:
    """Detect obvious credential-like fields, not every possible secret encoding."""
    if isinstance(value, dict):
        for key, child in value.items():
            if is_sensitive_value_key(str(key)):
                if isinstance(child, str):
                    populated = bool(child.strip())
                    placeholder = child.strip().lower() in PLACEHOLDERS
                    if populated and not placeholder:
                        errors.append(f"possible secret value stored in {label}.{key}")
                elif child is not None and child != "" and child is not False:
                    errors.append(f"credential-like field must not contain a value: {label}.{key}")
            scan_for_secret_values(child, f"{label}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_for_secret_values(child, f"{label}[{index}]", errors)


def validate_preconfiguration(cfg: dict[str, Any], errors: list[str]) -> None:
    require(type(cfg.get("schema_version")) is int and cfg.get("schema_version") == 1,
            "preconfiguration schema_version must equal integer 1", errors)
    require(cfg.get("project") == "Shed-Z", "project must equal 'Shed-Z'", errors)
    require(cfg.get("stage") in {"preconfiguration", "promotion_candidate"},
            "stage must be 'preconfiguration' or 'promotion_candidate'", errors)
    require(type(cfg.get("deployment_enabled")) is bool,
            "deployment_enabled must be a boolean", errors)

    host = section(cfg, "host", "host", errors)
    network = section(cfg, "network", "network", errors)
    execution = section(cfg, "execution", "execution", errors)
    model = section(cfg, "model", "model", errors)
    policy = section(cfg, "policy", "policy", errors)
    budget = section(cfg, "budget", "budget", errors)
    observability = section(cfg, "observability", "observability", errors)
    recovery = section(cfg, "recovery", "recovery", errors)
    state = section(cfg, "state", "state", errors)

    for key in ("target_type", "hostname", "os_family", "service_identity"):
        value = host.get(key)
        require(value is None or nonempty(value), f"host.{key} must be null or a non-empty string", errors)
    require(host.get("target_type") is None or host.get("target_type") in HOST_TYPES,
            "host.target_type must be null or a recognized host type", errors)
    value = host.get("service_identity_is_non_admin")
    require(value is None or type(value) is bool,
            "host.service_identity_is_non_admin must be null or boolean", errors)
    fingerprint = host.get("config_fingerprint_sha256")
    require(fingerprint is None or (nonempty(fingerprint) and SHA256_RE.fullmatch(fingerprint) is not None),
            "host.config_fingerprint_sha256 must be null or a lowercase SHA-256 hex digest", errors)

    for key in ("private_only_required", "policy_reviewed", "public_ingress_enabled"):
        require(type(network.get(key)) is bool, f"network.{key} must be a boolean", errors)
    require(network.get("private_only_required") is True,
            "private-only network access must be required", errors)
    require(network.get("public_ingress_enabled") is False,
            "public ingress must be disabled", errors)
    require(network.get("egress_mode") == "deny_unlisted",
            "network egress must deny unlisted destinations", errors)
    remote_provider = network.get("remote_access_provider")
    require(remote_provider is None or nonempty(remote_provider),
            "network.remote_access_provider must be null or a non-empty string", errors)
    destinations = network.get("allowed_destinations")
    require(string_list(destinations, allow_empty=True),
            "network.allowed_destinations must be a list of non-empty strings (or an empty list)", errors)
    if isinstance(destinations, list):
        for destination in destinations:
            if isinstance(destination, str):
                require("*" not in destination and not any(ch.isspace() for ch in destination),
                        "network.allowed_destinations must not contain wildcards or whitespace", errors)

    require(type(execution.get("enabled")) is bool, "execution.enabled must be a boolean", errors)
    require(execution.get("max_concurrent_jobs") == 1 and type(execution.get("max_concurrent_jobs")) is int,
            "preconfiguration must cap max_concurrent_jobs at integer 1", errors)
    require(positive_integer(execution.get("default_timeout_seconds")),
            "execution.default_timeout_seconds must be a positive integer", errors)
    require(nonnegative_integer(execution.get("max_retries")) and execution.get("max_retries") <= 3,
            "execution.max_retries must be an integer from 0 through 3", errors)
    for key in ("agent_runtime", "session_manager"):
        value = execution.get(key)
        require(value is None or nonempty(value), f"execution.{key} must be null or a non-empty string", errors)
    for key in ("per_job_cpu_limit", "per_job_memory_mb", "per_job_process_limit", "per_job_disk_mb"):
        value = execution.get(key)
        require(value is None or positive_number(value),
                f"execution.{key} must be null or a positive number", errors)
        if key != "per_job_cpu_limit" and value is not None:
            require(type(value) is int and value > 0,
                    f"execution.{key} must be null or a positive integer", errors)

    mode = model.get("mode")
    require(mode is None or mode in MODEL_MODES,
            "model.mode must be null or one of hosted/local/hybrid", errors)
    for key in ("provider", "model_id", "local_server_url", "cost_limit_currency"):
        value = model.get(key)
        require(value is None or nonempty(value), f"model.{key} must be null or a non-empty string", errors)
    require(model.get("automatic_fallback") is False,
            "automatic model fallback must be disabled unless separately designed and tested", errors)
    require(model.get("per_task_token_limit") is None or positive_integer(model.get("per_task_token_limit")),
            "model.per_task_token_limit must be null or a positive integer", errors)
    require(model.get("per_task_cost_limit") is None or positive_number(model.get("per_task_cost_limit")),
            "model.per_task_cost_limit must be null or a positive number", errors)
    if model.get("per_task_cost_limit") is not None:
        require(nonempty(model.get("cost_limit_currency")),
                "a per-task monetary limit requires model.cost_limit_currency", errors)
    if mode in {"hosted", "hybrid"}:
        require(nonempty(model.get("provider")) and nonempty(model.get("model_id")),
                "hosted/hybrid inference requires model.provider and model.model_id", errors)
    if mode == "local":
        require(nonempty(model.get("model_id")) or nonempty(model.get("local_server_url")),
                "local inference requires model.model_id or a reviewed model.local_server_url", errors)

    require(policy.get("enforcement_boundary") == "outside_model",
            "policy enforcement must sit outside model instructions", errors)
    require(policy.get("unknown_actions") == "DENY", "unknown actions must default to DENY", errors)
    require(policy.get("personal_data_access") is False, "personal-data access must be disabled by default", errors)
    require(policy.get("secrets_available_to_worker") is False, "secrets must not be exposed to workers by default", errors)
    require(policy.get("unreviewed_extensions_allowed") is False, "unreviewed extensions must be disabled", errors)
    require(policy.get("high_impact_action_requires_approval") is True,
            "high-impact actions must require approval", errors)

    require(type(budget.get("spending_authorized")) is bool, "budget.spending_authorized must be a boolean", errors)
    require(budget.get("approved_monthly_limit") is None or nonnegative_number(budget.get("approved_monthly_limit")),
            "budget.approved_monthly_limit must be null or a finite non-negative number", errors)
    require(budget.get("one_time_purchase_limit") is None or nonnegative_number(budget.get("one_time_purchase_limit")),
            "budget.one_time_purchase_limit must be null or a finite non-negative number", errors)
    currency = budget.get("approved_currency")
    require(currency is None or (isinstance(currency, str) and re.fullmatch(r"[A-Z]{3}", currency) is not None),
            "budget.approved_currency must be null or a three-letter uppercase currency code", errors)
    require(budget.get("hard_stop_required") is True, "a budget hard stop must be required", errors)
    alert = budget.get("alert_at_percent")
    require(type(alert) is int and 1 <= alert <= 100,
            "budget.alert_at_percent must be an integer from 1 through 100", errors)
    if budget.get("spending_authorized") is True:
        require(nonnegative_number(budget.get("approved_monthly_limit")),
                "spending authorization requires an explicit non-negative monthly limit", errors)
        require(nonempty(currency) and re.fullmatch(r"[A-Z]{3}", currency) is not None,
                "spending authorization requires an approved currency", errors)
        require(nonnegative_number(budget.get("one_time_purchase_limit")),
                "spending authorization requires a non-negative one-time purchase limit (zero is valid)", errors)

    for key in ("structured_events_required", "redact_sensitive_values", "independent_audit_sink_configured"):
        require(type(observability.get(key)) is bool, f"observability.{key} must be a boolean", errors)
    require(observability.get("structured_events_required") is True,
            "structured audit events must be required", errors)
    require(observability.get("redact_sensitive_values") is True,
            "sensitive-value redaction must be required", errors)
    audit_ref = observability.get("audit_sink_ref")
    require(audit_ref is None or nonempty(audit_ref),
            "observability.audit_sink_ref must be null or a non-empty reference", errors)

    for key in ("backup_configured", "restore_tested", "independent_stop_control_configured"):
        require(type(recovery.get(key)) is bool, f"recovery.{key} must be a boolean", errors)
    for key in ("backup_ref", "stop_control_ref"):
        value = recovery.get(key)
        require(value is None or nonempty(value), f"recovery.{key} must be null or a non-empty reference", errors)

    for key in ("durable_task_state_enabled", "encryption_at_rest_verified",
                "checkpointing_enabled", "idempotency_store_enabled"):
        require(type(state.get(key)) is bool, f"state.{key} must be a boolean", errors)
    store = state.get("store")
    require(store is None or nonempty(store), "state.store must be null or a non-empty string", errors)
    retention = state.get("retention_days")
    require(retention is None or positive_integer(retention),
            "state.retention_days must be null or a positive integer", errors)


def validate_action_policy(policy: dict[str, Any], errors: list[str]) -> None:
    require(type(policy.get("schema_version")) is int and policy.get("schema_version") == 1,
            "action-policy schema_version must equal integer 1", errors)
    require(policy.get("default_decision") == "DENY", "action policy must default to DENY", errors)
    require(nonempty(policy.get("policy_version")), "action policy must specify policy_version", errors)
    values = policy.get("decision_values")
    require(isinstance(values, list) and all(isinstance(item, str) for item in values)
            and set(values) == ALLOWED_DECISIONS and len(values) == len(ALLOWED_DECISIONS),
            "decision_values must list exactly DENY, APPROVAL_REQUIRED and ALLOW", errors)

    actions = policy.get("actions")
    require(isinstance(actions, list) and bool(actions), "action policy must contain a non-empty actions list", errors)
    if not isinstance(actions, list):
        actions = []

    action_ids: list[str] = []
    observed: dict[str, str] = {}
    for item in actions:
        if not isinstance(item, dict):
            errors.append("each action policy entry must be an object")
            continue
        action_id = item.get("action")
        require(nonempty(action_id), "every action policy entry must have a non-empty action name", errors)
        if not nonempty(action_id):
            continue
        action_ids.append(action_id)
        decision = item.get("decision")
        require(decision in ALLOWED_DECISIONS, f"invalid decision for action {action_id!r}", errors)
        observed[action_id] = decision
        if decision == "ALLOW":
            conditions = item.get("conditions")
            require(nonempty(item.get("scope")) or string_list(conditions),
                    f"allowed action {action_id!r} must have an explicit scope or non-empty conditions", errors)
        if decision == "APPROVAL_REQUIRED":
            require(string_list(item.get("approval_binding")),
                    f"approval-gated action {action_id!r} must bind approval to explicit fields", errors)

    require(len(action_ids) == len(set(action_ids)), "action policy contains duplicate action names", errors)
    expected = set(REQUIRED_ACTION_DECISIONS)
    actual = set(action_ids)
    for missing in sorted(expected - actual):
        errors.append(f"required action policy entry is missing: {missing}")
    for extra in sorted(actual - expected):
        errors.append(f"unrecognized action policy entry requires validator review: {extra}")
    for action_id, decision in REQUIRED_ACTION_DECISIONS.items():
        require(observed.get(action_id) == decision,
                f"action {action_id!r} must be set to {decision}", errors)

    enforcement = section(policy, "runtime_enforcement", "action-policy.runtime_enforcement", errors)
    require(enforcement.get("status") in {"not_implemented", "candidate", "verified"},
            "action-policy.runtime_enforcement.status must be not_implemented, candidate or verified", errors)
    for key in ("implementation_ref", "version", "independent_test_evidence_ref"):
        value = enforcement.get(key)
        require(value is None or nonempty(value),
                f"action-policy.runtime_enforcement.{key} must be null or a non-empty reference", errors)


def validate_job_catalog(catalog: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    require(type(catalog.get("schema_version")) is int and catalog.get("schema_version") == 1,
            "job-catalog schema_version must equal integer 1", errors)
    require(catalog.get("runtime_default_enabled") is False,
            "job catalog runtime_default_enabled must remain false", errors)
    jobs = catalog.get("jobs")
    require(isinstance(jobs, list) and bool(jobs), "job catalog must contain a non-empty jobs list", errors)
    if not isinstance(jobs, list):
        jobs = []

    ids: list[str] = []
    valid_jobs: list[dict[str, Any]] = []
    for job in jobs:
        if not isinstance(job, dict):
            errors.append("each job entry must be an object")
            continue
        valid_jobs.append(job)
        job_id = job.get("id")
        require(nonempty(job_id), "every job must have a non-empty id", errors)
        if nonempty(job_id):
            ids.append(job_id)
        require(nonempty(job.get("name")), f"job {job_id!r} must have a name", errors)
        require(nonempty(job.get("execution_plane")), f"job {job_id!r} must name its execution plane", errors)
        require(job.get("enabled_by_default") is False,
                f"job {job_id!r} must be disabled by default", errors)
        require(type(job.get("enabled")) is bool, f"job {job_id!r} enabled must be a boolean", errors)
        require(string_list(job.get("permissions"), allow_empty=True),
                f"job {job_id!r} permissions must be a list of non-empty strings", errors)
        require(string_list(job.get("acceptance")),
                f"job {job_id!r} must have non-empty acceptance criteria", errors)
        require(string_list(job.get("external_effects")) or string_list(job.get("forbidden_effects")),
                f"job {job_id!r} must document external effects or forbidden effects", errors)
        if job_id in {"J-002", "J-003"}:
            require(string_list(job.get("required_inputs")),
                    f"job {job_id!r} must declare required_inputs", errors)
        if job_id == "J-003":
            require(string_list(job.get("forbidden_effects")),
                    "J-003 must explicitly list forbidden_effects", errors)

    require(len(ids) == len(set(ids)), "job catalog contains duplicate job IDs", errors)
    actual_ids = set(ids)
    for missing in sorted(REQUIRED_JOB_IDS - actual_ids):
        errors.append(f"required job catalog entry is missing: {missing}")
    for extra in sorted(actual_ids - REQUIRED_JOB_IDS):
        errors.append(f"unrecognized job ID requires validator review: {extra}")
    return valid_jobs


def validate_promotion_evidence(
    cfg: dict[str, Any],
    policy: dict[str, Any],
    errors: list[str],
) -> None:
    try:
        evidence = load_json(EVIDENCE_PATH)
    except ValueError as exc:
        errors.append(f"promotion requires a valid local evidence manifest: {exc}")
        return

    scan_for_secret_values(evidence, "promotion_evidence", errors)
    require(type(evidence.get("schema_version")) is int and evidence.get("schema_version") == 1,
            "promotion evidence schema_version must equal integer 1", errors)
    fingerprint = evidence.get("target_fingerprint_sha256")
    require(nonempty(fingerprint) and SHA256_RE.fullmatch(fingerprint) is not None,
            "promotion evidence requires a lowercase SHA-256 target fingerprint", errors)
    host = cfg.get("host", {}) if isinstance(cfg.get("host"), dict) else {}
    require(fingerprint == host.get("config_fingerprint_sha256"),
            "promotion evidence target fingerprint must match host.config_fingerprint_sha256", errors)
    execution = cfg.get("execution", {}) if isinstance(cfg.get("execution"), dict) else {}
    require(evidence.get("runtime_version") == execution.get("agent_runtime") and nonempty(evidence.get("runtime_version")),
            "promotion evidence runtime_version must match the configured agent_runtime version", errors)
    require(evidence.get("policy_version") == policy.get("policy_version") and nonempty(evidence.get("policy_version")),
            "promotion evidence policy_version must match action-policy.policy_version", errors)
    enforcement = policy.get("runtime_enforcement", {}) if isinstance(policy.get("runtime_enforcement"), dict) else {}
    require(evidence.get("policy_enforcement_version") == enforcement.get("version")
            and nonempty(evidence.get("policy_enforcement_version")),
            "promotion evidence policy_enforcement_version must match the reviewed enforcement version", errors)
    require(nonempty(evidence.get("reviewer")), "promotion evidence requires a reviewer identifier", errors)
    require(valid_utc_timestamp(evidence.get("reviewed_at_utc")),
            "promotion evidence reviewed_at_utc must be an ISO-8601 UTC timestamp", errors)

    checks = evidence.get("checks")
    require(isinstance(checks, dict), "promotion evidence checks must be a JSON object", errors)
    if not isinstance(checks, dict):
        checks = {}
    for missing in sorted(REQUIRED_EVIDENCE_CHECKS - set(checks)):
        errors.append(f"promotion evidence is missing required check: {missing}")
    for extra in sorted(set(checks) - REQUIRED_EVIDENCE_CHECKS):
        errors.append(f"unrecognized promotion evidence check requires validator review: {extra}")
    for check_name in sorted(REQUIRED_EVIDENCE_CHECKS & set(checks)):
        item = checks[check_name]
        if not isinstance(item, dict):
            errors.append(f"promotion evidence check {check_name!r} must be an object")
            continue
        require(item.get("status") == "PASS",
                f"promotion evidence check {check_name!r} must have status PASS", errors)
        reference = item.get("evidence_ref")
        require(
            nonempty(reference)
            and len(reference) <= 512
            and EVIDENCE_REF_RE.fullmatch(reference) is not None
            and "?" not in reference
            and "#" not in reference
            and "/../" not in reference
            and not reference.startswith("../")
            and not reference.endswith("/.."),
            f"promotion evidence check {check_name!r} must point to a safe, non-empty evidence reference", errors,
        )
        require(valid_utc_timestamp(item.get("observed_at_utc")),
                f"promotion evidence check {check_name!r} requires an ISO-8601 UTC observed_at_utc", errors)

    policy_check = checks.get("policy_enforcement_before_side_effect")
    if isinstance(policy_check, dict):
        require(enforcement.get("independent_test_evidence_ref") == policy_check.get("evidence_ref"),
                "action policy independent_test_evidence_ref must match the policy-enforcement evidence check", errors)


def validate() -> tuple[list[str], bool]:
    errors: list[str] = []
    cfg = load_effective_config("preconfiguration")
    policy = load_effective_config("action_policy")
    catalog = load_effective_config("job_catalog")

    scan_for_secret_values(cfg, "preconfiguration", errors)
    scan_for_secret_values(policy, "action_policy", errors)
    scan_for_secret_values(catalog, "job_catalog", errors)

    validate_preconfiguration(cfg, errors)
    validate_action_policy(policy, errors)
    jobs = validate_job_catalog(catalog, errors)

    execution = cfg.get("execution", {}) if isinstance(cfg.get("execution"), dict) else {}
    stage = cfg.get("stage")
    promotion_requested = (
        stage != "preconfiguration"
        or cfg.get("deployment_enabled") is not False
        or execution.get("enabled") is not False
        or any(job.get("enabled") is not False for job in jobs)
    )

    if not promotion_requested:
        for job in jobs:
            if job.get("enabled") is not False:
                errors.append(f"job {job.get('id')!r} must remain disabled until promotion")
    else:
        require(stage == "promotion_candidate",
                "promotion requires stage='promotion_candidate'; this validator does not perform deployment", errors)
        require(cfg.get("deployment_enabled") is True and execution.get("enabled") is True,
                "deployment_enabled and execution.enabled must both be true for a promotion candidate", errors)

        host = cfg.get("host", {}) if isinstance(cfg.get("host"), dict) else {}
        network = cfg.get("network", {}) if isinstance(cfg.get("network"), dict) else {}
        model = cfg.get("model", {}) if isinstance(cfg.get("model"), dict) else {}
        policy_config = cfg.get("policy", {}) if isinstance(cfg.get("policy"), dict) else {}
        budget = cfg.get("budget", {}) if isinstance(cfg.get("budget"), dict) else {}
        observability = cfg.get("observability", {}) if isinstance(cfg.get("observability"), dict) else {}
        recovery = cfg.get("recovery", {}) if isinstance(cfg.get("recovery"), dict) else {}
        state = cfg.get("state", {}) if isinstance(cfg.get("state"), dict) else {}

        require(host.get("target_type") in HOST_TYPES, "promotion requires a recognized host.target_type", errors)
        require(nonempty(host.get("hostname")), "promotion requires host.hostname", errors)
        require(nonempty(host.get("os_family")), "promotion requires host.os_family", errors)
        require(nonempty(host.get("service_identity")) and host.get("service_identity_is_non_admin") is True,
                "promotion requires an explicitly verified non-admin service identity", errors)
        require(nonempty(host.get("config_fingerprint_sha256"))
                and SHA256_RE.fullmatch(host.get("config_fingerprint_sha256", "")) is not None,
                "promotion requires host.config_fingerprint_sha256", errors)

        destinations = network.get("allowed_destinations")
        require(network.get("private_only_required") is True and network.get("policy_reviewed") is True,
                "promotion requires reviewed private-only network access", errors)
        require(nonempty(network.get("remote_access_provider")),
                "promotion requires a selected remote-access provider", errors)
        require(network.get("public_ingress_enabled") is False and network.get("egress_mode") == "deny_unlisted",
                "promotion requires no public ingress and deny-unlisted egress", errors)
        require(string_list(destinations), "promotion requires an explicit non-empty network destination allowlist", errors)

        require(positive_number(execution.get("per_job_cpu_limit")),
                "promotion requires a positive per-job CPU limit", errors)
        require(positive_integer(execution.get("per_job_memory_mb")),
                "promotion requires a positive per-job memory limit", errors)
        require(positive_integer(execution.get("per_job_process_limit")),
                "promotion requires a positive per-job process limit", errors)
        require(positive_integer(execution.get("per_job_disk_mb")),
                "promotion requires a positive per-job disk limit", errors)
        require(positive_integer(execution.get("default_timeout_seconds")),
                "promotion requires a positive job timeout", errors)
        require(nonempty(execution.get("agent_runtime")),
                "promotion requires a selected and versioned agent runtime", errors)
        require(nonempty(execution.get("session_manager")),
                "promotion requires a selected and versioned session manager", errors)
        require(nonnegative_integer(execution.get("max_retries")) and execution.get("max_retries") <= 3,
                "promotion requires a bounded retry count from 0 through 3", errors)

        require(model.get("mode") in MODEL_MODES, "promotion requires a documented model inference mode", errors)
        if model.get("mode") in {"hosted", "hybrid"}:
            require(
                positive_integer(model.get("per_task_token_limit")) or positive_number(model.get("per_task_cost_limit")),
                "hosted/hybrid inference requires a per-task token or monetary ceiling", errors,
            )
        require(policy_config.get("personal_data_access") is False
                and policy_config.get("secrets_available_to_worker") is False
                and policy_config.get("unreviewed_extensions_allowed") is False,
                "promotion requires personal-data, secret and unreviewed-extension access to remain disabled", errors)

        require(budget.get("spending_authorized") is True,
                "promotion requires explicit spending authorization, including an explicit zero ceiling if applicable", errors)
        require(nonnegative_number(budget.get("approved_monthly_limit"))
                and nonempty(budget.get("approved_currency"))
                and nonnegative_number(budget.get("one_time_purchase_limit"))
                and budget.get("hard_stop_required") is True,
                "promotion requires monthly and one-time ceilings, currency and a required hard stop", errors)

        require(observability.get("independent_audit_sink_configured") is True
                and nonempty(observability.get("audit_sink_ref")),
                "promotion requires a separately configured audit sink reference", errors)
        require(recovery.get("backup_configured") is True
                and recovery.get("restore_tested") is True
                and nonempty(recovery.get("backup_ref")),
                "promotion requires configured backup, a tested restore and a backup evidence reference", errors)
        require(recovery.get("independent_stop_control_configured") is True
                and nonempty(recovery.get("stop_control_ref")),
                "promotion requires an independently reachable stop-control reference", errors)
        require(state.get("durable_task_state_enabled") is True
                and nonempty(state.get("store"))
                and state.get("encryption_at_rest_verified") is True
                and state.get("checkpointing_enabled") is True
                and state.get("idempotency_store_enabled") is True
                and positive_integer(state.get("retention_days")),
                "promotion requires encrypted durable task state, checkpointing, idempotency and a retention period", errors)

        require(any(job.get("enabled") is True for job in jobs),
                "promotion requires at least one explicitly enabled job", errors)
        for job in jobs:
            if job.get("enabled") is True:
                require(job.get("enabled_by_default") is False,
                        f"promoted job {job.get('id')!r} must remain disabled by default", errors)
                require(string_list(job.get("acceptance")),
                        f"promoted job {job.get('id')!r} must have acceptance criteria", errors)

        enforcement = policy.get("runtime_enforcement", {}) if isinstance(policy.get("runtime_enforcement"), dict) else {}
        require(enforcement.get("status") == "verified",
                "promotion requires runtime_enforcement.status='verified'", errors)
        require(nonempty(enforcement.get("implementation_ref"))
                and nonempty(enforcement.get("version"))
                and nonempty(enforcement.get("independent_test_evidence_ref")),
                "promotion requires a named policy-enforcement implementation, version and independent test evidence", errors)
        validate_promotion_evidence(cfg, policy, errors)

    return errors, promotion_requested


def main() -> int:
    try:
        errors, promotion_requested = validate()
    except ValueError as exc:
        print(f"Preconfiguration validation failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        print(f"Preconfiguration validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    if promotion_requested:
        print(
            "Promotion candidate passed static configuration and evidence-manifest checks only. "
            "No installation, deployment, agent execution or independent evidence verification was performed."
        )
    else:
        print(
            "Preconfiguration validation passed. Deployment, runtime and Shed-Z jobs remain disabled; "
            "no host capability or runtime security is implied."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
