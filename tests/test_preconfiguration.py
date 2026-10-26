"""Regression tests for fail-closed Shed-Z configuration and promotion gates."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG_FILES = ("preconfiguration.json", "action-policy.json", "job-catalog.json")
EVIDENCE_CHECKS = (
    "host_hardening", "private_access_approved_device", "unapproved_device_denied",
    "unlisted_egress_denied", "policy_enforcement_before_side_effect", "approval_binding",
    "audit_tamper_resistance", "credential_revocation", "backup_restore", "independent_stop_control",
    "worker_data_isolation", "budget_hard_stop", "bounded_job_acceptance_replay",
    "malformed_input_and_missing_resource", "timeout_cancel_and_worker_failure",
    "durable_state_checkpoint_recovery", "dependency_inventory_and_pin_verification",
)


class PreconfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        (self.root / "config").mkdir()
        shutil.copy2(REPO / "scripts" / "validate_preconfiguration.py",
                     self.root / "scripts" / "validate_preconfiguration.py")
        for name in CONFIG_FILES:
            shutil.copy2(REPO / "config" / name, self.root / "config" / name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def path(self, name: str) -> Path:
        return self.root / "config" / name

    def read_config(self, name: str) -> dict:
        return json.loads(self.path(name).read_text(encoding="utf-8"))

    def write_config(self, name: str, value: dict) -> None:
        self.path(name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "validate_preconfiguration.py"), *args],
            cwd=self.root, text=True, capture_output=True, check=False,
        )

    def test_checked_in_baseline_passes_with_runtime_disabled(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Deployment, runtime and Shed-Z jobs remain disabled", result.stdout)

    def test_malformed_json_fails_with_clear_error(self) -> None:
        self.path("preconfiguration.json").write_text('{"schema_version":', encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid JSON", result.stderr)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        self.path("preconfiguration.json").write_text(
            '{"schema_version":1,"schema_version":1}', encoding="utf-8"
        )
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate JSON key", result.stderr)

    def test_nonstandard_nan_constant_is_rejected(self) -> None:
        self.path("preconfiguration.json").write_text('{"schema_version":NaN}', encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-standard JSON numeric constant", result.stderr)

    def test_non_object_top_level_is_rejected(self) -> None:
        self.path("preconfiguration.json").write_text("[]", encoding="utf-8")
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("top-level JSON value must be an object", result.stderr)

    def test_malformed_nested_section_fails_without_traceback(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["network"] = []
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("network must be a JSON object", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_security_boolean_cannot_be_string_coerced(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["network"]["public_ingress_enabled"] = "false"
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("network.public_ingress_enabled must be a boolean", result.stderr)

    def test_merge_cannot_be_enabled_in_policy(self) -> None:
        policy = self.read_config("action-policy.json")
        item = next(entry for entry in policy["actions"] if entry["action"] == "merge_pull_request")
        item["decision"] = "ALLOW"
        self.write_config("action-policy.json", policy)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("merge_pull_request", result.stderr)

    def test_unknown_action_cannot_be_added_as_allow(self) -> None:
        policy = self.read_config("action-policy.json")
        policy["actions"].append({"action":"arbitrary_shell_execution","decision":"ALLOW","scope":"all"})
        self.write_config("action-policy.json", policy)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unrecognized action policy entry", result.stderr)

    def test_required_action_cannot_be_removed(self) -> None:
        policy = self.read_config("action-policy.json")
        policy["actions"] = [item for item in policy["actions"] if item["action"] != "unknown_action"]
        self.write_config("action-policy.json", policy)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required action policy entry is missing: unknown_action", result.stderr)

    def test_duplicate_action_ids_are_rejected(self) -> None:
        policy = self.read_config("action-policy.json")
        policy["actions"].append(dict(policy["actions"][0]))
        self.write_config("action-policy.json", policy)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate action names", result.stderr)

    def test_job_cannot_be_enabled_before_promotion(self) -> None:
        catalog = self.read_config("job-catalog.json")
        catalog["jobs"][0]["enabled"] = True
        self.write_config("job-catalog.json", catalog)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("deployment_enabled and execution.enabled must both be true", result.stderr)

    def test_duplicate_job_ids_are_rejected(self) -> None:
        catalog = self.read_config("job-catalog.json")
        catalog["jobs"].append(dict(catalog["jobs"][0]))
        self.write_config("job-catalog.json", catalog)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate job IDs", result.stderr)

    def test_empty_acceptance_criteria_are_rejected(self) -> None:
        catalog = self.read_config("job-catalog.json")
        catalog["jobs"][0]["acceptance"] = []
        self.write_config("job-catalog.json", catalog)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("acceptance criteria", result.stderr)

    def test_public_ingress_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["network"]["public_ingress_enabled"] = True
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("public ingress must be disabled", result.stderr)

    def test_wildcard_egress_destination_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["network"]["allowed_destinations"] = ["*.example.com"]
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not contain wildcards", result.stderr)

    def test_secret_value_in_nested_config_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["future_extension"] = {"api-key": "not-a-real-key-test-fixture"}
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("possible secret value", result.stderr)

    def test_spending_requires_monthly_and_one_time_ceilings(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["budget"].update({
            "spending_authorized": True, "approved_monthly_limit": 10, "approved_currency": "USD"
        })
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("one-time purchase limit", result.stderr)

    def test_partial_runtime_promotion_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["deployment_enabled"] = True
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("deployment_enabled and execution.enabled must both be true", result.stderr)
        self.assertIn("local-promotion-evidence.json", result.stderr)

    def prepare_valid_promotion_candidate(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["stage"] = "promotion_candidate"
        cfg["deployment_enabled"] = True
        cfg["host"].update({
            "target_type":"existing_computer", "hostname":"shedz-test-host", "os_family":"Linux",
            "service_identity":"shedz-worker", "service_identity_is_non_admin":True,
            "config_fingerprint_sha256":"a" * 64,
        })
        cfg["network"].update({
            "remote_access_provider":"reviewed-private-overlay", "policy_reviewed":True,
            "allowed_destinations":["github.com","api.github.com"],
        })
        cfg["execution"].update({
            "enabled":True, "agent_runtime":"candidate-runtime@1.2.3",
            "session_manager":"candidate-session@2.0.0", "default_timeout_seconds":300,
            "max_retries":1, "per_job_cpu_limit":1, "per_job_memory_mb":1024,
            "per_job_process_limit":8, "per_job_disk_mb":2048,
        })
        cfg["model"].update({
            "mode":"hosted", "provider":"test-provider", "model_id":"test-model",
            "per_task_token_limit":4000, "per_task_cost_limit":0.05, "cost_limit_currency":"USD",
        })
        cfg["budget"].update({
            "spending_authorized":True, "approved_monthly_limit":10,
            "approved_currency":"USD", "one_time_purchase_limit":0,
        })
        cfg["observability"].update({
            "independent_audit_sink_configured":True, "audit_sink_ref":"audit://independent-test-sink",
        })
        cfg["recovery"].update({
            "backup_configured":True, "restore_tested":True,
            "backup_ref":"artifact://recovery/restore-test",
            "independent_stop_control_configured":True, "stop_control_ref":"artifact://recovery/stop-test",
        })
        cfg["state"].update({
            "store":"encrypted-durable-store@1", "durable_task_state_enabled":True,
            "encryption_at_rest_verified":True, "checkpointing_enabled":True,
            "idempotency_store_enabled":True, "retention_days":30,
        })
        self.write_config("local-preconfiguration.json", cfg)

        policy = self.read_config("action-policy.json")
        policy["runtime_enforcement"] = {
            "status":"verified", "implementation_ref":"policy-gate/implementation-record",
            "version":"policy-gate@1.0.0", "independent_test_evidence_ref":"artifact://tests/policy-enforcement",
        }
        self.write_config("local-action-policy.json", policy)

        catalog = self.read_config("job-catalog.json")
        target_job = next(item for item in catalog["jobs"] if item["id"] == "J-002")
        target_job["enabled"] = True
        self.write_config("local-job-catalog.json", catalog)

        fingerprint_result = self.run_validator("--print-fingerprint")
        self.assertEqual(fingerprint_result.returncode, 0, fingerprint_result.stdout + fingerprint_result.stderr)
        fingerprint = fingerprint_result.stdout.strip()
        cfg = self.read_config("local-preconfiguration.json")
        cfg["host"]["config_fingerprint_sha256"] = fingerprint
        self.write_config("local-preconfiguration.json", cfg)

        observed = "2026-10-26T00:00:00Z"
        evidence = {
            "schema_version":1, "target_fingerprint_sha256":fingerprint,
            "runtime_version":"candidate-runtime@1.2.3", "policy_version":"1.0.0",
            "policy_enforcement_version":"policy-gate@1.0.0", "reviewer":"independent-review-record-01",
            "reviewed_at_utc":observed,
            "checks":{
                name:{
                    "status":"PASS",
                    "evidence_ref":(
                        "artifact://tests/policy-enforcement"
                        if name == "policy_enforcement_before_side_effect"
                        else f"artifact://tests/{name}"
                    ),
                    "observed_at_utc":observed,
                }
                for name in EVIDENCE_CHECKS
            },
        }
        self.write_config("local-promotion-evidence.json", evidence)

    def test_complete_local_promotion_candidate_passes_static_gates(self) -> None:
        self.prepare_valid_promotion_candidate()
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("passed static configuration and evidence-manifest checks only", result.stdout)
        self.assertIn("No installation, deployment, agent execution", result.stdout)

    def test_missing_promotion_evidence_check_blocks_candidate(self) -> None:
        self.prepare_valid_promotion_candidate()
        evidence = self.read_config("local-promotion-evidence.json")
        del evidence["checks"]["independent_stop_control"]
        self.write_config("local-promotion-evidence.json", evidence)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required check: independent_stop_control", result.stderr)

    def test_evidence_for_different_host_fingerprint_is_rejected(self) -> None:
        self.prepare_valid_promotion_candidate()
        evidence = self.read_config("local-promotion-evidence.json")
        evidence["target_fingerprint_sha256"] = "b" * 64
        self.write_config("local-promotion-evidence.json", evidence)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must match host.config_fingerprint_sha256", result.stderr)

    def test_failed_evidence_check_blocks_candidate(self) -> None:
        self.prepare_valid_promotion_candidate()
        evidence = self.read_config("local-promotion-evidence.json")
        evidence["checks"]["backup_restore"]["status"] = "FAIL"
        self.write_config("local-promotion-evidence.json", evidence)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("backup_restore' must have status PASS", result.stderr)



    def test_unhashable_stage_value_fails_without_traceback(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["stage"] = []
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("stage must be", result.stderr)

    def test_unhashable_host_type_fails_without_traceback(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["host"]["target_type"] = []
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("host.target_type", result.stderr)

    def test_unhashable_model_mode_fails_without_traceback(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["model"]["mode"] = []
        self.write_config("preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("model.mode", result.stderr)

    def test_unhashable_action_decision_fails_without_traceback(self) -> None:
        policy = self.read_config("action-policy.json")
        policy["actions"][0]["decision"] = []
        self.write_config("action-policy.json", policy)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("invalid decision", result.stderr)

    def test_unhashable_enforcement_status_fails_without_traceback(self) -> None:
        policy = self.read_config("action-policy.json")
        policy["runtime_enforcement"]["status"] = []
        self.write_config("action-policy.json", policy)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("runtime_enforcement.status", result.stderr)

    def test_unhashable_job_id_fails_without_traceback(self) -> None:
        catalog = self.read_config("job-catalog.json")
        catalog["jobs"][0]["id"] = []
        self.write_config("job-catalog.json", catalog)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("job must have a non-empty id", result.stderr)

    def test_configuration_fingerprint_detects_config_drift(self) -> None:
        self.prepare_valid_promotion_candidate()
        cfg = self.read_config("local-preconfiguration.json")
        cfg["model"]["model_id"] = "altered-after-review"
        self.write_config("local-preconfiguration.json", cfg)
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("effective configuration fingerprint", result.stderr)


if __name__ == "__main__":
    unittest.main()
