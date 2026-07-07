#!/usr/bin/env python3
"""Prepare a client-specific delivery workspace from a sample config."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    if not isinstance(config, dict):
        raise ValueError("config must parse to a mapping")
    return config


def planned_paths(config: dict[str, Any]) -> list[Path]:
    output_dir = Path(config.get("automation", {}).get("output_dir", "outputs"))
    return [
        output_dir,
        output_dir / "account-research",
        output_dir / "executive-brief",
        output_dir / "quality-review",
        output_dir / "github-digest",
    ]


def bootstrap(config_path: Path, dry_run: bool = True) -> list[str]:
    config = load_config(config_path)
    messages: list[str] = []

    for path in planned_paths(config):
        if dry_run:
            messages.append(f"Would create directory: {path}")
        else:
            path.mkdir(parents=True, exist_ok=True)
            messages.append(f"Created directory: {path}")

    client_name = config.get("client", {}).get("name", "Unknown client")
    messages.append(f"Prepared workspace plan for: {client_name}")
    return messages


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=Path("client-config.example.yaml"),
        type=Path,
        help="Path to client config YAML.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print planned actions without writing output folders.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    for message in bootstrap(args.config, dry_run=args.dry_run):
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
