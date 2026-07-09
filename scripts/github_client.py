#!/usr/bin/env python3
"""Generate a GitHub repository activity digest with dry-run support."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml


API_ROOT = "https://api.github.com"
ISSUE_DATE_FIELDS = ("updated_at", "closed_at", "created_at")
PULL_REQUEST_DATE_FIELDS = ("updated_at", "closed_at", "merged_at", "created_at")
RELEASE_DATE_FIELDS = ("published_at", "created_at")


@dataclass(frozen=True)
class GitHubConfig:
    owner: str
    repo: str
    digest_days: int = 7
    include_issues: bool = True
    include_pull_requests: bool = True
    include_releases: bool = True


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
        include_issues=bool(github.get("include", {}).get("issues", True)),
        include_pull_requests=bool(github.get("include", {}).get("pull_requests", True)),
        include_releases=bool(github.get("include", {}).get("releases", True)),
    )


class GitHubAPIError(RuntimeError):
    """Raised when the GitHub API cannot return a usable response."""


class GitHubRateLimitError(GitHubAPIError):
    """Raised when GitHub reports a primary or secondary API rate limit."""


class GitHubClient:
    def __init__(self, token: str | None = None, api_root: str = API_ROOT) -> None:
        self.token = token
        self.api_root = api_root.rstrip("/")

    def get_json(self, path: str, params: dict[str, str] | None = None) -> Any:
        url = f"{self.api_root}{path}"
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"

        request = urllib.request.Request(url)
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if self.token:
            request.add_header("Authorization", f"Bearer {self.token}")

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            message = self._error_message(exc)
            if self._is_rate_limit(exc, message):
                raise GitHubRateLimitError(self._rate_limit_message(exc)) from exc
            if exc.code in {500, 502, 503, 504}:
                raise GitHubAPIError(
                    f"Temporary GitHub API failure: {exc.code} {exc.reason}. Retry later."
                ) from exc
            detail = f": {message}" if message else ""
            raise GitHubAPIError(f"GitHub API request failed: {exc.code} {exc.reason}{detail}") from exc
        except urllib.error.URLError as exc:
            raise GitHubAPIError(f"GitHub API request failed: {exc.reason}") from exc

    @staticmethod
    def _error_message(exc: urllib.error.HTTPError) -> str:
        try:
            body = exc.read().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            return ""

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return body.strip()

        message = data.get("message") if isinstance(data, dict) else None
        return str(message) if message else ""

    @staticmethod
    def _is_rate_limit(exc: urllib.error.HTTPError, message: str) -> bool:
        remaining = exc.headers.get("X-RateLimit-Remaining")
        normalized_message = message.lower()
        return (
            exc.code == 429
            or remaining == "0"
            or "rate limit" in normalized_message
            or "too many requests" in normalized_message
        )

    @staticmethod
    def _rate_limit_message(exc: urllib.error.HTTPError) -> str:
        retry_after = exc.headers.get("Retry-After")
        if retry_after:
            return f"GitHub API rate limit exceeded; retry after {retry_after} seconds."

        reset = exc.headers.get("X-RateLimit-Reset")
        if reset and reset.isdigit():
            reset_at = datetime.fromtimestamp(int(reset), tz=timezone.utc).isoformat()
            return f"GitHub API rate limit exceeded; retry after {reset_at}."

        return "GitHub API rate limit exceeded; retry later."

    def repository(self, config: GitHubConfig) -> dict[str, Any]:
        return self.get_json(f"/repos/{config.owner}/{config.repo}")

    def issues(self, config: GitHubConfig) -> list[dict[str, Any]]:
        data = self.get_json(
            f"/repos/{config.owner}/{config.repo}/issues",
            {"state": "all", "per_page": "30", "sort": "updated", "direction": "desc"},
        )
        return [item for item in data if "pull_request" not in item]

    def pull_requests(self, config: GitHubConfig) -> list[dict[str, Any]]:
        return self.get_json(
            f"/repos/{config.owner}/{config.repo}/pulls",
            {"state": "all", "per_page": "30", "sort": "updated", "direction": "desc"},
        )

    def releases(self, config: GitHubConfig) -> list[dict[str, Any]]:
        return self.get_json(f"/repos/{config.owner}/{config.repo}/releases", {"per_page": "10"})


def dry_run_payload(config: GitHubConfig) -> dict[str, Any]:
    return {
        "repository": {
            "full_name": f"{config.owner}/{config.repo}",
            "description": "Dry-run repository metadata for delivery workflow demonstration.",
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
        "issues": client.issues(config) if config.include_issues else [],
        "pull_requests": client.pull_requests(config) if config.include_pull_requests else [],
        "releases": client.releases(config) if config.include_releases else [],
    }


def item_line(item: dict[str, Any], label: str = "#") -> str:
    number = item.get("number")
    title = item.get("title") or item.get("name") or item.get("tag_name") or "Untitled"
    state = item.get("state")
    prefix = f"{label}{number}" if number is not None else str(item.get("tag_name", "-"))
    suffix = f" ({state})" if state else ""
    return f"- {prefix}: {title}{suffix}"


def parse_github_date(value: Any) -> date | None:
    if not isinstance(value, str) or not value:
        return None

    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def item_activity_date(item: dict[str, Any], fields: tuple[str, ...]) -> date | None:
    for field in fields:
        parsed = parse_github_date(item.get(field))
        if parsed:
            return parsed
    return None


def filter_items_by_window(
    items: list[dict[str, Any]],
    generated_on: date,
    digest_days: int,
    date_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    if digest_days <= 0:
        return list(items)

    window_start = generated_on - timedelta(days=digest_days)
    filtered = []
    for item in items:
        activity_date = item_activity_date(item, date_fields)
        if activity_date is None or window_start <= activity_date <= generated_on:
            filtered.append(item)
    return filtered


def item_lines(items: list[dict[str, Any]], label: str = "#") -> list[str]:
    if not items:
        return ["- No matching items found in the digest window."]
    return [item_line(item, label=label) for item in items]


def generate_digest(payload: dict[str, Any], config: GitHubConfig, generated_on: date | None = None) -> str:
    generated_on = generated_on or date.today()
    repository = payload["repository"]
    issues = filter_items_by_window(
        payload.get("issues", []),
        generated_on,
        config.digest_days,
        ISSUE_DATE_FIELDS,
    )
    pull_requests = filter_items_by_window(
        payload.get("pull_requests", []),
        generated_on,
        config.digest_days,
        PULL_REQUEST_DATE_FIELDS,
    )
    releases = filter_items_by_window(
        payload.get("releases", []),
        generated_on,
        config.digest_days,
        RELEASE_DATE_FIELDS,
    )

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
        *item_lines(issues),
        "",
        "## Pull Requests",
        "",
        *item_lines(pull_requests),
        "",
        "## Releases",
        "",
        *item_lines(releases, label=""),
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
        "--live",
        action="store_true",
        help="Use live GitHub API data. Requires GITHUB_TOKEN.",
    )
    parser.add_argument(
        "--api-root",
        default=API_ROOT,
        help="GitHub API root URL. Override for GitHub Enterprise or tests.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output Markdown path.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.dry_run and args.live:
        parser.error("--dry-run and --live cannot be used together")

    config = github_config_from_file(args.config)
    if args.owner:
        config = GitHubConfig(
            args.owner,
            config.repo,
            config.digest_days,
            config.include_issues,
            config.include_pull_requests,
            config.include_releases,
        )
    if args.repo:
        config = GitHubConfig(
            config.owner,
            args.repo,
            config.digest_days,
            config.include_issues,
            config.include_pull_requests,
            config.include_releases,
        )

    token = os.environ.get("GITHUB_TOKEN")
    if args.live and not token:
        print("Error: --live requires GITHUB_TOKEN in the environment.", file=sys.stderr)
        return 2

    try:
        payload = (
            live_payload(GitHubClient(token, api_root=args.api_root), config)
            if args.live
            else dry_run_payload(config)
        )
    except GitHubAPIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

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
