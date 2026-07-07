#!/usr/bin/env python3
"""Generate a GitHub repository activity digest with dry-run support."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml


API_ROOT = "https://api.github.com"


@dataclass(frozen=True)
class GitHubConfig:
    owner: str
    repo: str
    digest_days: int = 7


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
    if not isinstance(config, dict):
        raise ValueError("config must parse to a mapping")
    return config


def github_config_from_file(path: Path) -> GitHubConfig:
    config = load_config(path)
    github = config.get("github", {})
    return GitHubConfig(
        owner=str(github.get("owner", "example-org")),
        repo=str(github.get("repo", "example-repo")),
        digest_days=int(github.get("digest_days", 7)),
    )


class GitHubClient:
    def __init__(self, token: str | None = None, api_root: str = API_ROOT) -> None:
        self.token = token
        self.api_root = api_root.rstrip("/")

    def get_json(self, path: str) -> Any:
        request = urllib.request.Request(f"{self.api_root}{path}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"GitHub API request failed: {exc.code} {exc.reason}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"GitHub API request failed: {exc.reason}") from exc

    def repository(self, config: GitHubConfig) -> dict[str, Any]:
        return self.get_json(f"/repos/{config.owner}/{config.repo}")

    def issues(self, config: GitHubConfig) -> list[dict[str, Any]]:
        data = self.get_json(f"/repos/{config.owner}/{config.repo}/issues?state=all&per_page=10")
        return [item for item in data if "pull_request" not in item]

    def pull_requests(self, config: GitHubConfig) -> list[dict[str, Any]]:
        return self.get_json(f"/repos/{config.owner}/{config.repo}/pulls?state=all&per_page=10")

    def releases(self, config: GitHubConfig) -> list[dict[str, Any]]:
        return self.get_json(f"/repos/{config.owner}/{config.repo}/releases?per_page=5")


def dry_run_payload(config: GitHubConfig) -> dict[str, Any]:
    return {
        "repository": {
            "full_name": f"{config.owner}/{config.repo}",
            "description": "Dry-run repository metadata for portfolio demonstration.",
            "open_issues_count": 3,
            "default_branch": "main",
        },
        "issues": [
            {"number": 12, "title": "Review account research prompt metadata", "state": "open"},
            {"number": 11, "title": "Document restricted environment setup", "state": "closed"},
        ],
        "pull_requests": [
            {"number": 8, "title": "Add weekly digest workflow", "state": "open"},
        ],
        "releases": [
            {"tag_name": "v0.1.0", "name": "Initial delivery kit release", "draft": False},
        ],
    }


def live_payload(client: GitHubClient, config: GitHubConfig) -> dict[str, Any]:
    return {
        "repository": client.repository(config),
        "issues": client.issues(config),
        "pull_requests": client.pull_requests(config),
        "releases": client.releases(config),
    }


def item_line(item: dict[str, Any], label: str = "#") -> str:
    number = item.get("number")
    title = item.get("title") or item.get("name") or item.get("tag_name") or "Untitled"
    state = item.get("state")
    prefix = f"{label}{number}" if number is not None else str(item.get("tag_name", "-"))
    suffix = f" ({state})" if state else ""
    return f"- {prefix}: {title}{suffix}"


def generate_digest(payload: dict[str, Any], config: GitHubConfig, generated_on: date | None = None) -> str:
    generated_on = generated_on or date.today()
    repository = payload["repository"]
    issues = payload.get("issues", [])
    pull_requests = payload.get("pull_requests", [])
    releases = payload.get("releases", [])

    lines = [
        f"# Weekly GitHub Digest: {repository.get('full_name', f'{config.owner}/{config.repo}')}",
        "",
        f"Generated on: {generated_on.isoformat()}",
        f"Digest window: last {config.digest_days} days",
        "",
        "## Repository",
        "",
        f"- Description: {repository.get('description') or 'No description provided'}",
        f"- Default branch: {repository.get('default_branch', 'unknown')}",
        f"- Open issues count: {repository.get('open_issues_count', 'unknown')}",
        "",
        "## Issues",
        "",
        *(item_line(item) for item in issues),
        "",
        "## Pull Requests",
        "",
        *(item_line(item) for item in pull_requests),
        "",
        "## Releases",
        "",
        *(item_line(item, label='') for item in releases),
        "",
        "## Delivery Notes",
        "",
        "- Review open issues for delivery blockers.",
        "- Confirm prompt and documentation changes before client handoff.",
        "- Keep secrets in environment variables or approved secret managers.",
    ]
    return "\n".join(lines).strip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=Path("client-config.example.yaml"),
        type=Path,
        help="Path to client config YAML.",
    )
    parser.add_argument("--owner", help="Override GitHub owner from config.")
    parser.add_argument("--repo", help="Override GitHub repository from config.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Use sample data and avoid network access.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output Markdown path.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = github_config_from_file(args.config)
    if args.owner:
        config = GitHubConfig(args.owner, config.repo, config.digest_days)
    if args.repo:
        config = GitHubConfig(config.owner, args.repo, config.digest_days)

    token = os.environ.get("GITHUB_TOKEN")
    use_dry_run = args.dry_run or not token
    payload = dry_run_payload(config) if use_dry_run else live_payload(GitHubClient(token), config)
    digest = generate_digest(payload, config)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(digest, encoding="utf-8")
        print(f"Wrote digest to {args.output}")
    else:
        print(digest)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
