#!/usr/bin/env python3
"""Check local Markdown links and research-source references using Python stdlib only."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SOURCE_ROW = re.compile(r"^\|\s*S(\d+)\s*\|", re.MULTILINE)
SOURCE_RANGE = re.compile(r"\bS(\d+)\s*[–-]\s*S(\d+)\b")
SOURCE_ID = re.compile(r"\bS(\d+)\b")


def markdown_files() -> list[Path]:
    excluded = {".git", ".venv", "venv", "node_modules"}
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in excluded for part in path.relative_to(ROOT).parts)
    )


def local_link_errors(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for match in MARKDOWN_LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith("<"):
            target = target[1:].split(">", 1)[0]
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        decoded_path = unquote(parts.path)
        destination = (path.parent / decoded_path).resolve()
        try:
            destination.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes repository: {target}")
            continue
        if not destination.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")
    return errors


def source_reference_errors() -> list[str]:
    findings = ROOT / "docs" / "01-research-findings.md"
    register = ROOT / "docs" / "09-source-register.md"
    if not findings.exists() or not register.exists():
        return ["source-reference check requires docs/01-research-findings.md and docs/09-source-register.md"]

    findings_text = findings.read_text(encoding="utf-8")
    register_text = register.read_text(encoding="utf-8")
    available = {int(value) for value in SOURCE_ROW.findall(register_text)}
    cited = {int(value) for value in SOURCE_ID.findall(findings_text)}

    for start, end in SOURCE_RANGE.findall(findings_text):
        left, right = int(start), int(end)
        if right >= left and right - left <= 100:
            cited.update(range(left, right + 1))

    missing = sorted(cited - available)
    if missing:
        labels = ", ".join(f"S{value}" for value in missing)
        return [f"research findings cite source IDs absent from source register: {labels}"]
    return []


def main() -> int:
    files = markdown_files()
    errors: list[str] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: not valid UTF-8: {exc}")
            continue
        errors.extend(local_link_errors(path, text))

    errors.extend(source_reference_errors())
    if errors:
        print(f"Documentation check failed with {len(errors)} issue(s):", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"Documentation check passed: {len(files)} Markdown files scanned; local links and research source IDs are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
