#!/usr/bin/env python3
"""Validate prompt Markdown files with YAML frontmatter."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


REQUIRED_FIELDS = {
    "id",
    "version",
    "owner",
    "status",
    "category",
    "inputs",
    "outputs",
}
ALLOWED_STATUSES = {"draft", "stable", "deprecated"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass(frozen=True)
class PromptDocument:
    path: Path
    metadata: dict[str, Any]
    body: str


def parse_prompt(path: Path) -> PromptDocument:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")

    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("frontmatter must be closed with ---") from exc

    metadata = yaml.safe_load(frontmatter) or {}
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must parse to a mapping")

    return PromptDocument(path=path, metadata=metadata, body=body.strip())


def validate_document(document: PromptDocument, root: Path) -> list[str]:
    errors: list[str] = []
    metadata = document.metadata

    missing = sorted(REQUIRED_FIELDS - metadata.keys())
    if missing:
        errors.append(f"missing required metadata fields: {', '.join(missing)}")

    version = metadata.get("version")
    if version is not None and not SEMVER_RE.match(str(version)):
        errors.append("version must use semantic versioning, for example 1.0.0")

    status = metadata.get("status")
    if status is not None and status not in ALLOWED_STATUSES:
        errors.append(f"status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}")

    category = metadata.get("category")
    expected_category = document.path.relative_to(root).parts[0]
    if category is not None and category != expected_category:
        errors.append(
            f"category '{category}' does not match folder '{expected_category}'"
        )

    for field in ("inputs", "outputs"):
        value = metadata.get(field)
        if value is not None and (
            not isinstance(value, list) or not all(isinstance(item, str) for item in value)
        ):
            errors.append(f"{field} must be a list of strings")

    prompt_id = metadata.get("id")
    if prompt_id is not None and not isinstance(prompt_id, str):
        errors.append("id must be a string")

    if not document.body:
        errors.append("prompt body must not be empty")

    return errors


def find_prompt_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def validate_library(root: Path) -> list[str]:
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}

    if not root.exists():
        return [f"{root}: prompt root does not exist"]

    prompt_files = find_prompt_files(root)
    if not prompt_files:
        return [f"{root}: no prompt Markdown files found"]

    for path in prompt_files:
        try:
            document = parse_prompt(path)
        except ValueError as exc:
            errors.append(f"{path}: {exc}")
            continue

        for error in validate_document(document, root):
            errors.append(f"{path}: {error}")

        prompt_id = document.metadata.get("id")
        if isinstance(prompt_id, str):
            if prompt_id in seen_ids:
                errors.append(
                    f"{path}: duplicate prompt id '{prompt_id}' also used by {seen_ids[prompt_id]}"
                )
            seen_ids[prompt_id] = path

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="prompts",
        type=Path,
        help="Prompt library root directory.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    errors = validate_library(args.root)

    if errors:
        print("Prompt library validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Prompt library validation passed: {args.root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
