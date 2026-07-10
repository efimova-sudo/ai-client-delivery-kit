import io
import json
import sys
import urllib.error
import urllib.request
from datetime import date
from email.message import Message

import pytest

from scripts import github_client
from scripts.github_client import (
    GitHubClient,
    GitHubConfig,
    GitHubRateLimitError,
    dry_run_payload,
    generate_digest,
    github_config_from_file,
)


def test_dry_run_payload_uses_config_repository_name() -> None:
    config = GitHubConfig(owner="example-org", repo="example-repo")

    payload = dry_run_payload(config)

    assert payload["repository"]["full_name"] == "example-org/example-repo"


def test_generate_digest_includes_core_sections() -> None:
    config = GitHubConfig(owner="example-org", repo="example-repo", digest_days=7)
    payload = dry_run_payload(config)

    digest = generate_digest(payload, config, generated_on=date(2026, 7, 7))

    assert "# Weekly GitHub Digest: example-org/example-repo" in digest
    assert "Generated on: 2026-07-07" in digest
    assert "## Issues" in digest
    assert "## Pull Requests" in digest
    assert "## Releases" in digest
    assert "Keep secrets in environment variables" in digest


def test_config_parses_string_include_flags(tmp_path) -> None:
    config_path = tmp_path / "client-config.yaml"
    config_path.write_text(
        """
github:
  owner: example-org
  repo: example-repo
  include:
    issues: "false"
    pull_requests: "no"
    releases: "true"
""".strip(),
        encoding="utf-8",
    )

    config = github_config_from_file(config_path)

    assert config.include_issues is False
    assert config.include_pull_requests is False
    assert config.include_releases is True


def test_live_client_builds_authenticated_issue_request(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str | int | None] = {}

    class FakeResponse:
        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                [
                    {"number": 3, "title": "Live issue", "state": "open"},
                    {
                        "number": 4,
                        "title": "PR returned by issues endpoint",
                        "pull_request": {},
                    },
                ]
            ).encode("utf-8")

    def fake_urlopen(request: urllib.request.Request, timeout: int) -> FakeResponse:
        captured["url"] = request.full_url
        captured["authorization"] = request.get_header("Authorization")
        captured["accept"] = request.get_header("Accept")
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    client = GitHubClient(token="secret-token", api_root="https://api.github.test")
    issues = client.issues(GitHubConfig(owner="example-org", repo="example-repo"))

    assert issues == [{"number": 3, "title": "Live issue", "state": "open"}]
    assert captured["url"] == (
        "https://api.github.test/repos/example-org/example-repo/issues"
        "?state=all&per_page=30&sort=updated&direction=desc"
    )
    assert captured["authorization"] == "Bearer secret-token"
    assert captured["accept"] == "application/vnd.github+json"
    assert captured["timeout"] == 20


def test_generate_digest_filters_items_outside_digest_window() -> None:
    config = GitHubConfig(owner="example-org", repo="example-repo", digest_days=7)
    payload = {
        "repository": {
            "full_name": "example-org/example-repo",
            "description": "Repository metadata",
            "open_issues_count": 1,
            "default_branch": "main",
        },
        "issues": [
            {
                "number": 12,
                "title": "Recent issue",
                "state": "open",
                "updated_at": "2026-07-06T10:00:00Z",
            },
            {
                "number": 11,
                "title": "Old issue",
                "state": "open",
                "updated_at": "2026-06-01T10:00:00Z",
            },
        ],
        "pull_requests": [
            {
                "number": 8,
                "title": "Recent pull request",
                "state": "open",
                "updated_at": "2026-07-03T10:00:00Z",
            },
            {
                "number": 7,
                "title": "Old pull request",
                "state": "closed",
                "updated_at": "2026-05-20T10:00:00Z",
            },
        ],
        "releases": [
            {
                "tag_name": "v0.2.0",
                "name": "Recent release",
                "published_at": "2026-07-07T10:00:00Z",
            },
            {
                "tag_name": "v0.1.0",
                "name": "Old release",
                "published_at": "2026-05-01T10:00:00Z",
            },
        ],
    }

    digest = generate_digest(payload, config, generated_on=date(2026, 7, 7))

    assert "Recent issue" in digest
    assert "Recent pull request" in digest
    assert "Recent release" in digest
    assert "Old issue" not in digest
    assert "Old pull request" not in digest
    assert "Old release" not in digest


def test_live_client_reports_rate_limit_without_token_leak(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    headers = Message()
    headers["X-RateLimit-Remaining"] = "0"
    headers["X-RateLimit-Reset"] = "1780000000"

    def fake_urlopen(request: urllib.request.Request, timeout: int) -> object:
        raise urllib.error.HTTPError(
            request.full_url,
            403,
            "Forbidden",
            headers,
            io.BytesIO(b'{"message": "API rate limit exceeded for token secret-token"}'),
        )

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    client = GitHubClient(token="secret-token", api_root="https://api.github.test")
    with pytest.raises(GitHubRateLimitError) as excinfo:
        client.repository(GitHubConfig(owner="example-org", repo="example-repo"))

    message = str(excinfo.value)
    assert "rate limit exceeded" in message
    assert "secret-token" not in message


def test_live_mode_requires_github_token(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        ["github_client.py", "--config", "client-config.example.yaml", "--live"],
    )

    exit_code = github_client.main()

    assert exit_code == 2
    assert "--live requires GITHUB_TOKEN" in capsys.readouterr().err
