from datetime import date

from scripts.github_client import GitHubConfig, dry_run_payload, generate_digest


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
