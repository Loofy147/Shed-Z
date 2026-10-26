"""Negative-fixture tests for the documentation integrity checker."""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import check_docs  # noqa: E402


class DocumentationCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        self.old_root = check_docs.ROOT
        check_docs.ROOT = self.root
        self.addCleanup(self.restore_root)
        self.addCleanup(self.temp.cleanup)

    def restore_root(self) -> None:
        check_docs.ROOT = self.old_root

    def write(self, relative: str, value: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, bytes):
            path.write_bytes(value)
        else:
            path.write_text(value, encoding="utf-8")
        return path

    def write_source_register(self, rows: str = "| S1 | Example | https://example.invalid |") -> None:
        self.write("docs/09-source-register.md", "# Sources\n\n" + rows + "\n")

    def run_checker(self) -> tuple[int, str]:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            code = check_docs.main()
        return code, stderr.getvalue()

    def test_valid_local_link_and_registered_source_pass(self) -> None:
        self.write("docs/page.md", "[target](target.md) and source S1")
        self.write("docs/target.md", "# Target\n")
        self.write_source_register()
        self.write("docs/01-research-findings.md", "# Findings\nS1 supports this finding.\n")
        code, error = self.run_checker()
        self.assertEqual(code, 0, error)

    def test_broken_local_link_fails_checker(self) -> None:
        self.write("docs/page.md", "[missing](does-not-exist.md)")
        self.write_source_register()
        self.write("docs/01-research-findings.md", "# Findings\n")
        code, error = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("broken local link", error)

    def test_link_that_escapes_repository_is_rejected(self) -> None:
        self.write("docs/page.md", "[outside](../../outside.md)")
        self.write_source_register()
        self.write("docs/01-research-findings.md", "# Findings\n")
        code, error = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("link escapes repository", error)

    def test_unknown_research_source_id_fails_checker(self) -> None:
        self.write("docs/page.md", "A normal page")
        self.write_source_register()
        self.write("docs/01-research-findings.md", "# Findings\nThis claim cites S99.\n")
        code, error = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("S99", error)

    def test_source_range_requires_every_id_in_range(self) -> None:
        self.write("docs/page.md", "A normal page")
        self.write_source_register("| S1 | One | https://example.invalid |\n| S3 | Three | https://example.invalid |")
        self.write("docs/01-research-findings.md", "# Findings\nSources S1–S3.\n")
        code, error = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("S2", error)

    def test_missing_source_register_fails_checker(self) -> None:
        self.write("docs/01-research-findings.md", "# Findings\nS1\n")
        code, error = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("source-reference check requires", error)

    def test_invalid_utf8_markdown_fails_checker(self) -> None:
        self.write("docs/page.md", b"\xff\xfe\xfa")
        self.write_source_register()
        self.write("docs/01-research-findings.md", "# Findings\n")
        code, error = self.run_checker()
        self.assertEqual(code, 1)
        self.assertIn("not valid UTF-8", error)


if __name__ == "__main__":
    unittest.main()
