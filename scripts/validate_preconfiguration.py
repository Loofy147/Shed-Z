#!/usr/bin/env python3
"""Validate Shed-Z preconfiguration artifacts using Python's standard library only."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
ALLOWED_DECISIONS = {"DENY", "APPROVAL_REQUIRED", "ALLOW"}
HOST_TYPES = {"existing_computer", "virtual_machine", "cloud_vm"}
MODEL_MODES = {"hosted", "local", "hybrid"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Required file is missing: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)} at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Top-level JSON value must be an object: {path.relative_to(ROOT)}")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate() -> list[str]:
    errors: list[str] = []
    cfg = load_json(CONFIG_DIR / "preconfiguration.json")
    policy = load_json(CONFIG_DIR / "action-policy.json")
    catalog = load_json(CONFIG_DIR / "job-catalog.json")

    require(cfg.get("schema_version") == 1, "preconfiguration schema_version must equal 1", errors)
    require(cfg.get("stage") == "preconfiguration", "stage must remain 'preconfiguration' in this template", errors)
    require(cfg.get("policy", {}).get("unknown_actions") == "DENY", "unknown actions must default to DENY", errors)
    require(cfg.get("policy", {}).get("enforcement_boundary") == "outside_model", "policy enforcement must be outside model instructions", errors)
    require(cfg.get("policy", {}).get("personal_data_access") is False, "personal-data access must be disabled by default", errors)
    require(cfg.get("policy", {}).get("secrets_available_to_worker") is False, "secrets must not be exposed to workers by default", errors)
    require(cfg.get("policy", {}).get("unreviewed_extensions_allowed") is False, "unreviewed extensions must be disabled", errors)
    require(cfg.get("network", {}).get("private_only_required") is True, "private-only network access must be required", errors)
    require(cfg.get("network", {}).get("public_ingress_enabled") is False, "public ingress must be disabled", errors)
    require(cfg.get("network", {}).get("egress_mode") == "deny_unlisted", "network egress must deny unlisted destinations", errors)
    require(cfg.get("model", {}).get("automatic_fallback") is False, "automatic model fallback must be disabled unless separately tested and approved", errors)
    require(cfg.get("budget", {}).get("spending_authorized") is False or (
        isinstance(cfg.get("budget", {}).get("approved_monthly_limit"), (int, float))
        and cfg["budget"]["approved_monthly_limit"] >= 0
        and nonempty(cfg.get("budget", {}).get("approved_currency"))
        and cfg.get("budget", {}).get("hard_stop_required") is True
    ), "spending authorization requires a non-negative monthly limit, currency, and hard stop", errors)
    require(cfg.get("budget", {}).get("hard_stop_required") is True, "a budget hard stop must be required", errors)
    require(cfg.get("execution", {}).get("max_concurrent_jobs") == 1, "preconfiguration must keep max_concurrent_jobs at 1", errors)

    require(policy.get("schema_version") == 1, "action-policy schema_version must equal 1", errors)
    require(policy.get("default_decision") == "DENY", "action policy must default to DENY", errors)
    actions = policy.get("actions", [])
    require(isinstance(actions, list) and bool(actions), "action policy must contain a non-empty actions list", errors)
    action_ids: list[str] = []
    for item in actions if isinstance(actions, list) else []:
        if not isinstance(item, dict):
            errors.append("each action policy entry must be an object")
            continue
        action_id = item.get("action")
        require(nonempty(action_id), "every action policy entry must have an action name", errors)
        if nonempty(action_id):
            action_ids.append(action_id)
        require(item.get("decision") in ALLOWED_DECISIONS, f"invalid decision for action {action_id!r}", errors)
    require(len(action_ids) == len(set(action_ids)), "action policy contains duplicate action names", errors)
    require(any(a.get("action") == "unknown_action" and a.get("decision") == "DENY" for a in actions if isinstance(a, dict)), "unknown_action must explicitly be denied", errors)

    require(catalog.get("schema_version") == 1, "job-catalog schema_version must equal 1", errors)
    require(catalog.get("runtime_default_enabled") is False, "job catalog runtime_default_enabled must remain false", errors)
    jobs = catalog.get("jobs", [])
    require(isinstance(jobs, list) and bool(jobs), "job catalog must contain a non-empty jobs list", errors)
    job_ids: list[str] = []
    for job in jobs if isinstance(jobs, list) else []:
        if not isinstance(job, dict):
            errors.append("each job entry must be an object")
            continue
        job_id = job.get("id")
        require(nonempty(job_id), "every job must have an id", errors)
        if nonempty(job_id):
            job_ids.append(job_id)
        require(job.get("enabled_by_default") is False, f"job {job_id!r} must be disabled by default", errors)
        if cfg.get("deployment_enabled") is not True or cfg.get("execution", {}).get("enabled") is not True:
            require(job.get("enabled") is False, f"job {job_id!r} must remain disabled until runtime promotion", errors)
        require(nonempty(job.get("name")), f"job {job_id!r} must have a name", errors)
        require(bool(job.get("acceptance")), f"job {job_id!r} must have acceptance criteria", errors)
    require(len(job_ids) == len(set(job_ids)), "job catalog contains duplicate job IDs", errors)

    # The preconfiguration file may only enable runtime after all deployment gates
    # are explicitly populated. In the checked-in baseline, this remains false.
    if cfg.get("deployment_enabled") is True or cfg.get("execution", {}).get("enabled") is True:
        host = cfg.get("host", {})
        network = cfg.get("network", {})
        execution = cfg.get("execution", {})
        model = cfg.get("model", {})
        budget = cfg.get("budget", {})
        observability = cfg.get("observability", {})
        recovery = cfg.get("recovery", {})
        require(cfg.get("deployment_enabled") is True and execution.get("enabled") is True, "deployment_enabled and execution.enabled must both be true when promoting", errors)
        require(host.get("target_type") in HOST_TYPES, "promoting requires a recognized host.target_type", errors)
        require(nonempty(host.get("hostname")), "promoting requires host.hostname", errors)
        require(nonempty(host.get("os_family")), "promoting requires host.os_family", errors)
        require(nonempty(host.get("service_identity")) and host.get("service_identity_is_non_admin") is True, "promoting requires a non-admin service identity", errors)
        require(nonempty(network.get("remote_access_provider")) and network.get("policy_reviewed") is True, "promoting requires reviewed private remote access", errors)
        require(network.get("public_ingress_enabled") is False and network.get("egress_mode") == "deny_unlisted", "promoting requires no public ingress and deny-unlisted egress", errors)
        require(isinstance(execution.get("per_job_cpu_limit"), (int, float)) and execution["per_job_cpu_limit"] > 0, "promoting requires a positive per-job CPU limit", errors)
        require(isinstance(execution.get("per_job_memory_mb"), int) and execution["per_job_memory_mb"] > 0, "promoting requires a positive per-job memory limit", errors)
        require(isinstance(execution.get("default_timeout_seconds"), int) and execution["default_timeout_seconds"] > 0, "promoting requires a positive job timeout", errors)
        require(nonempty(execution.get("agent_runtime")), "promoting requires a selected agent runtime", errors)
        require(model.get("mode") in MODEL_MODES, "promoting requires a documented model inference mode", errors)
        if model.get("mode") in {"hosted", "hybrid"}:
            require(nonempty(model.get("provider")) and nonempty(model.get("model_id")), "hosted/hybrid inference requires provider and model_id", errors)
        if model.get("mode") == "local":
            require(nonempty(model.get("model_id")) or nonempty(model.get("local_server_url")), "local inference requires a model_id or reviewed local server URL", errors)
        require(budget.get("spending_authorized") is True and isinstance(budget.get("approved_monthly_limit"), (int, float)) and budget["approved_monthly_limit"] >= 0 and nonempty(budget.get("approved_currency")), "promoting requires explicit monthly spending authorization and ceiling", errors)
        require(observability.get("independent_audit_sink_configured") is True, "promoting requires an independent audit sink", errors)
        require(recovery.get("backup_configured") is True and recovery.get("restore_tested") is True, "promoting requires configured and tested backup/restore", errors)
        require(recovery.get("independent_stop_control_configured") is True, "promoting requires an independent stop control", errors)
        require(any(isinstance(job, dict) and job.get("enabled") is True for job in jobs), "promoting requires at least one explicitly enabled and specified job", errors)

    # Fail closed if obvious secret-value fields are introduced into tracked JSON.
    secret_key_fragments = {"api_key", "secret_value", "password_value", "token_value", "private_key_value"}
    def walk(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                normalized = str(key).lower().replace("-", "_")
                if normalized in secret_key_fragments and child not in (None, "", "CHANGE_ME", "SET_OUTSIDE_REPO"):
                    errors.append(f"possible secret value stored in configuration field {path}.{key}")
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            for idx, child in enumerate(value):
                walk(child, f"{path}[{idx}]")
    walk(cfg, "preconfiguration")
    walk(policy, "action_policy")
    walk(catalog, "job_catalog")

    return errors


def main() -> int:
    try:
        errors = validate()
    except ValueError as exc:
        print(f"Preconfiguration validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        print(f"Preconfiguration validation failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1
    print("Preconfiguration validation passed. Runtime and jobs remain disabled; no deployment or host capability is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
