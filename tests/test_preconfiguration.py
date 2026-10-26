"""Regression tests for the fail-closed preconfiguration gate."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG_FILES = (
    "preconfiguration.json",
    "action-policy.json",
    "job-catalog.json",
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

    def read_config(self, name: str) -> dict:
        path = self.root / "config" / name
        return json.loads(path.read_text(encoding="utf-8"))

    def write_config(self, name: str, value: dict) -> None:
        path = self.root / "config" / name
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "validate_preconfiguration.py")],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_checked_in_baseline_passes(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Runtime and jobs remain disabled", result.stdout)

    def test_incomplete_runtime_promotion_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["deployment_enabled"] = True
        cfg["execution"]["enabled"] = True
        self.write_config("preconfiguration.json", cfg)

        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("promoting requires", result.stderr)

    def test_merge_cannot_be_enabled_in_baseline_policy(self) -> None:
        policy = self.read_config("action-policy.json")
        action = next(item for item in policy["actions"] if item["action"] == "merge_pull_request")
        action["decision"] = "ALLOW"
        self.write_config("action-policy.json", policy)

        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("merge_pull_request", result.stderr)

    def test_job_cannot_be_enabled_before_runtime_promotion(self) -> None:
        catalog = self.read_config("job-catalog.json")
        catalog["jobs"][0]["enabled"] = True
        self.write_config("job-catalog.json", catalog)

        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must remain disabled until runtime promotion", result.stderr)

    def test_public_ingress_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["network"]["public_ingress_enabled"] = True
        self.write_config("preconfiguration.json", cfg)

        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("public ingress must be disabled", result.stderr)

    def test_secret_value_in_tracked_config_is_rejected(self) -> None:
        cfg = self.read_config("preconfiguration.json")
        cfg["api_key"] = "not-a-real-key-test-fixture"
        self.write_config("preconfiguration.json", cfg)

        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("possible secret value", result.stderr)


if __name__ == "__main__":
    unittest.main()
